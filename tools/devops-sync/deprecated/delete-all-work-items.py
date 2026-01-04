#!/usr/bin/env python3
"""
Deleta TODOS os Work Items do Azure DevOps
Usado para reestruturacao completa do Board
"""

import os
import sys
import requests
from datetime import datetime

# Configuracoes
ORG_URL = os.getenv("AZDO_ORG_URL")
PROJECT = os.getenv("AZDO_PROJECT")
TOKEN = os.getenv("AZDO_PAT")

def get_auth():
    return ("", TOKEN)

def get_headers():
    return {"Content-Type": "application/json"}

def get_all_work_items():
    """Retorna IDs de todos os Work Items do projeto"""
    url = f"{ORG_URL}/{PROJECT}/_apis/wit/wiql?api-version=7.0"
    query = {"query": "SELECT [System.Id] FROM WorkItems WHERE [System.TeamProject] = @project"}

    r = requests.post(url, json=query, auth=get_auth())
    r.raise_for_status()

    items = r.json().get("workItems", [])
    return [item["id"] for item in items]

def delete_work_item(work_item_id):
    """Deleta um Work Item"""
    url = f"{ORG_URL}/{PROJECT}/_apis/wit/workitems/{work_item_id}?api-version=7.0"

    r = requests.delete(url, auth=get_auth())

    if r.status_code == 200:
        return True
    else:
        print(f"[!!] Erro ao deletar Work Item {work_item_id}: {r.status_code}")
        return False

def main():
    if not all([ORG_URL, PROJECT, TOKEN]):
        print("=" * 80)
        print("DELETE WORK ITEMS - VARIAVEIS NAO CONFIGURADAS")
        print("=" * 80)
        print("\nDefina as variaveis de ambiente:")
        print("  AZDO_ORG_URL, AZDO_PROJECT, AZDO_PAT")
        print("=" * 80)
        sys.exit(1)

    print("=" * 80)
    print("DELECAO DE TODOS OS WORK ITEMS")
    print("=" * 80)
    print(f"Org: {ORG_URL}")
    print(f"Project: {PROJECT}")
    print(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Confirmar acao
    print("[!!] ATENCAO: Esta operacao IRA DELETAR TODOS OS WORK ITEMS")
    print("[!!] Esta acao NAO PODE SER REVERTIDA")
    print()

    # Obter todos os Work Items
    print("[>] Carregando Work Items...")
    work_items = get_all_work_items()
    print(f"[>] Encontrados {len(work_items)} Work Items")
    print()

    if len(work_items) == 0:
        print("[>] Nenhum Work Item para deletar")
        return 0

    # Deletar todos
    print("[>] Deletando Work Items...")
    deleted = 0
    errors = 0

    for wi_id in work_items:
        if delete_work_item(wi_id):
            print(f"[OK] Deletado: Work Item {wi_id}")
            deleted += 1
        else:
            errors += 1

    # Resumo
    print()
    print("=" * 80)
    print("RESUMO DA DELECAO")
    print("=" * 80)
    print(f"Total de Work Items: {len(work_items)}")
    print(f"Deletados: {deleted}")
    print(f"Erros: {errors}")
    print("=" * 80)

    return 0 if errors == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
