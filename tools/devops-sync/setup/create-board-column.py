#!/usr/bin/env python3
# Cria coluna no Board do Azure DevOps

import os
import sys
import requests
import urllib.parse
from datetime import datetime

# Configuracoes
ORG_URL = os.getenv("AZDO_ORG_URL")
PROJECT = os.getenv("AZDO_PROJECT")
TOKEN = os.getenv("AZDO_PAT")

def get_auth():
    return ("", TOKEN)

def get_headers():
    return {"Content-Type": "application/json"}

def get_board_columns():
    """Lista colunas atuais do Features board"""
    team = f"{PROJECT} Team"
    project_encoded = urllib.parse.quote(PROJECT)
    team_encoded = urllib.parse.quote(team)

    url = f"{ORG_URL}/{project_encoded}/{team_encoded}/_apis/work/boards/Features/columns?api-version=7.0"

    try:
        r = requests.get(url, auth=get_auth())
        if r.status_code == 200:
            columns = r.json().get('value', [])
            return columns
        else:
            print(f"[!!] Erro ao listar colunas: {r.status_code}")
            print(f"     Resposta: {r.text[:500]}")
            return []
    except Exception as e:
        print(f"[!!] Excecao: {e}")
        return []

def create_board_column(column_name, after_column=None):
    """Cria uma nova coluna no Board"""
    team = f"{PROJECT} Team"
    project_encoded = urllib.parse.quote(PROJECT)
    team_encoded = urllib.parse.quote(team)

    url = f"{ORG_URL}/{project_encoded}/{team_encoded}/_apis/work/boards/Features/columns?api-version=7.0"

    payload = {
        "name": column_name,
        "stateMappings": {
            "Feature": "New"
        }
    }

    try:
        r = requests.post(url, json=payload, headers=get_headers(), auth=get_auth())

        if r.status_code in [200, 201]:
            print(f"[OK] Coluna '{column_name}' criada com sucesso")
            return True
        else:
            print(f"[!!] Erro ao criar coluna '{column_name}': {r.status_code}")
            print(f"     Resposta: {r.text[:500]}")
            return False
    except Exception as e:
        print(f"[!!] Excecao ao criar coluna: {e}")
        return False

def main():
    if not all([ORG_URL, PROJECT, TOKEN]):
        print("=" * 80)
        print("CREATE BOARD COLUMN - VARIAVEIS NAO CONFIGURADAS")
        print("=" * 80)
        print("\nDefina: AZDO_ORG_URL, AZDO_PROJECT, AZDO_PAT")
        print("=" * 80)
        sys.exit(1)

    print("=" * 80)
    print("CRIACAO DE COLUNA NO BOARD")
    print("=" * 80)
    print(f"Org: {ORG_URL}")
    print(f"Project: {PROJECT}")
    print(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Listar colunas atuais
    print("[>] Listando colunas atuais do Features board...")
    columns = get_board_columns()

    if columns:
        print(f"[>] Colunas atuais ({len(columns)}):")
        for col in columns:
            print(f"    - {col.get('name', 'Unknown')}")
        print()

    # Verificar se Skeleton ja existe
    skeleton_exists = any(col.get('name') == 'Skeleton' for col in columns)

    if skeleton_exists:
        print("[>>] Coluna 'Skeleton' ja existe no Board")
        return 0

    # Criar coluna Skeleton
    print("[+] Criando coluna 'Skeleton'...")
    if create_board_column("Skeleton"):
        print("\n[OK] Coluna criada com sucesso!")
        print("\nProximo passo: Execute sync-all-rfs.py para mover RFs para Skeleton")
    else:
        print("\n[!!] Falha ao criar coluna")
        return 1

    print("=" * 80)
    return 0

if __name__ == "__main__":
    sys.exit(main())
