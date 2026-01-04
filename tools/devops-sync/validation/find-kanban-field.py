#!/usr/bin/env python3
"""
Script para descobrir o campo WEF correto para colunas Kanban no Azure DevOps.
"""
import os
import requests
from requests.auth import HTTPBasicAuth

ORG_URL = os.environ.get('AZDO_ORG_URL', 'https://dev.azure.com/IControlIT-v2')
PROJECT = os.environ.get('AZDO_PROJECT', 'iControlIT 2.0')
PAT = os.environ.get('AZDO_PAT', '')

if not PAT:
    pat_file = 'D:\\IC2\\.azdo-pat'
    if os.path.exists(pat_file):
        with open(pat_file, 'r') as f:
            PAT = f.read().strip()

auth = HTTPBasicAuth('', PAT)
headers = {'Content-Type': 'application/json'}

def get_work_item_fields(work_item_id):
    """Busca todos os campos de um work item para encontrar campos WEF"""
    url = f'{ORG_URL}/{PROJECT}/_apis/wit/workitems/{work_item_id}?$expand=all&api-version=7.0'
    response = requests.get(url, auth=auth, headers=headers)

    if response.status_code == 200:
        data = response.json()
        print("=== TODOS OS CAMPOS DO WORK ITEM 257 ===\n")

        fields = data.get('fields', {})
        wef_fields = []
        board_fields = []

        for key, value in sorted(fields.items()):
            if 'WEF' in key or 'wef' in key.lower():
                wef_fields.append((key, value))
            if 'Board' in key or 'board' in key.lower() or 'Column' in key or 'column' in key.lower():
                board_fields.append((key, value))
            if 'Kanban' in key or 'kanban' in key.lower():
                board_fields.append((key, value))

        print("--- CAMPOS WEF ---")
        for key, value in wef_fields:
            print(f"  {key}: {value}")

        print("\n--- CAMPOS BOARD/COLUMN/KANBAN ---")
        for key, value in board_fields:
            print(f"  {key}: {value}")

        print("\n--- TODOS OS CAMPOS (para referência) ---")
        for key, value in sorted(fields.items()):
            print(f"  {key}: {value}")
    else:
        print(f"Erro {response.status_code}: {response.text}")

def list_all_fields():
    """Lista todos os campos disponíveis no projeto"""
    url = f'{ORG_URL}/{PROJECT}/_apis/wit/fields?api-version=7.0'
    response = requests.get(url, auth=auth, headers=headers)

    if response.status_code == 200:
        data = response.json()
        print("\n\n=== CAMPOS DISPONÍVEIS NO PROJETO ===\n")

        wef_fields = []
        board_fields = []

        for field in data.get('value', []):
            name = field.get('referenceName', '')
            display = field.get('name', '')

            if 'WEF' in name or 'wef' in name.lower():
                wef_fields.append((name, display))
            if 'Board' in name or 'board' in name.lower() or 'Column' in name or 'column' in name.lower():
                board_fields.append((name, display))
            if 'Kanban' in name or 'kanban' in name.lower():
                board_fields.append((name, display))

        print("--- CAMPOS WEF DISPONÍVEIS ---")
        for ref, display in wef_fields:
            print(f"  {ref} ({display})")

        print("\n--- CAMPOS BOARD/COLUMN/KANBAN DISPONÍVEIS ---")
        for ref, display in board_fields:
            print(f"  {ref} ({display})")
    else:
        print(f"Erro {response.status_code}: {response.text}")

def get_board_columns():
    """Busca as colunas do board"""
    # Primeiro, buscar os boards disponíveis
    url = f'{ORG_URL}/{PROJECT}/_apis/work/boards?api-version=7.0'
    response = requests.get(url, auth=auth, headers=headers)

    print("\n\n=== BOARDS DISPONÍVEIS ===\n")
    if response.status_code == 200:
        data = response.json()
        for board in data.get('value', []):
            print(f"  Board: {board.get('name')} (id: {board.get('id')})")

            # Buscar colunas deste board
            board_id = board.get('id')
            cols_url = f'{ORG_URL}/{PROJECT}/_apis/work/boards/{board_id}/columns?api-version=7.0'
            cols_response = requests.get(cols_url, auth=auth, headers=headers)

            if cols_response.status_code == 200:
                cols_data = cols_response.json()
                print(f"    Colunas:")
                for col in cols_data.get('value', []):
                    print(f"      - {col.get('name')} (id: {col.get('id')}, stateMappings: {col.get('stateMappings')})")
    else:
        print(f"Erro {response.status_code}: {response.text}")

if __name__ == '__main__':
    print("Buscando informações do Azure DevOps...\n")
    get_work_item_fields(257)
    list_all_fields()
    get_board_columns()
