#!/usr/bin/env python3
"""
Script para mover work item 257 para coluna 'Frontend em execucao'.
"""
import os
import requests
from requests.auth import HTTPBasicAuth
import json

ORG_URL = os.environ.get('AZDO_ORG_URL', 'https://dev.azure.com/IControlIT-v2')
PROJECT = os.environ.get('AZDO_PROJECT', 'iControlIT 2.0')
PAT = os.environ.get('AZDO_PAT', '')

if not PAT:
    pat_file = 'D:\\IC2\\.azdo-pat'
    if os.path.exists(pat_file):
        with open(pat_file, 'r') as f:
            PAT = f.read().strip()

auth = HTTPBasicAuth('', PAT)

def move_to_frontend_column(work_item_id):
    """Move work item para coluna Frontend em execucao usando campo WEF"""
    url = f'{ORG_URL}/{PROJECT}/_apis/wit/workitems/{work_item_id}?api-version=7.0'

    # Campo WEF descoberto para este projeto
    wef_field = 'WEF_D45E7CD10F0643A2AA7A9C0E27E3C815_Kanban.Column'

    payload = [
        {
            'op': 'add',
            'path': f'/fields/{wef_field}',
            'value': 'Frontend em execucao'
        }
    ]

    headers = {
        'Content-Type': 'application/json-patch+json'
    }

    print(f"Atualizando work item {work_item_id}...")
    print(f"Campo: {wef_field}")
    print(f"Novo valor: Frontend em execucao")
    print(f"URL: {url}")
    print(f"Payload: {json.dumps(payload, indent=2)}")

    response = requests.patch(url, auth=auth, headers=headers, json=payload)

    print(f"\nStatus: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        fields = data.get('fields', {})
        print("\n=== SUCESSO ===")
        print(f"System.BoardColumn: {fields.get('System.BoardColumn', 'N/A')}")
        print(f"{wef_field}: {fields.get(wef_field, 'N/A')}")
        return True
    else:
        print(f"\nErro: {response.text}")

        # Tentar com acento
        print("\n--- Tentando com acento ---")
        payload[0]['value'] = 'Frontend em execu\u00e7\u00e3o'
        print(f"Novo valor: Frontend em execu\u00e7\u00e3o")

        response = requests.patch(url, auth=auth, headers=headers, json=payload)
        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            fields = data.get('fields', {})
            print("\n=== SUCESSO (com acento) ===")
            print(f"System.BoardColumn: {fields.get('System.BoardColumn', 'N/A')}")
            print(f"{wef_field}: {fields.get(wef_field, 'N/A')}")
            return True
        else:
            print(f"Erro: {response.text}")
            return False

if __name__ == '__main__':
    move_to_frontend_column(257)
