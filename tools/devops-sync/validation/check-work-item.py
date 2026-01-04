#!/usr/bin/env python3
# Verifica estado de um Work Item especifico

import os
import sys
import requests

ORG_URL = os.getenv("AZDO_ORG_URL")
PROJECT = os.getenv("AZDO_PROJECT")
TOKEN = os.getenv("AZDO_PAT")

def get_auth():
    return ("", TOKEN)

def get_work_item_details(work_item_id):
    """Busca detalhes de um Work Item"""
    url = f"{ORG_URL}/{PROJECT}/_apis/wit/workitems/{work_item_id}?$expand=all&api-version=7.0"

    try:
        r = requests.get(url, auth=get_auth())
        if r.status_code == 200:
            return r.json()
        else:
            print(f"[!!] Erro: {r.status_code}")
            return None
    except Exception as e:
        print(f"[!!] Excecao: {e}")
        return None

def main():
    if len(sys.argv) < 2:
        print("Uso: python check-work-item.py <WORK_ITEM_ID>")
        sys.exit(1)

    work_item_id = sys.argv[1]

    print(f"Verificando Work Item {work_item_id}...")
    print()

    wi = get_work_item_details(work_item_id)

    if not wi:
        print("[!!] Work Item nao encontrado")
        sys.exit(1)

    fields = wi.get('fields', {})

    print(f"Title: {fields.get('System.Title', 'N/A')}")
    print(f"State: {fields.get('System.State', 'N/A')}")
    print(f"Area Path: {fields.get('System.AreaPath', 'N/A')}")
    print(f"Iteration Path: {fields.get('System.IterationPath', 'N/A')}")
    print()

    # Listar todos os campos WEF (Kanban)
    print("Campos WEF/Kanban:")
    for field_name, field_value in fields.items():
        if 'WEF' in field_name or 'Kanban' in field_name:
            print(f"  {field_name}: {field_value}")

    print()
    print("Campos principais:")
    print(f"  System.WorkItemType: {fields.get('System.WorkItemType', 'N/A')}")
    print(f"  System.State: {fields.get('System.State', 'N/A')}")
    print(f"  System.Reason: {fields.get('System.Reason', 'N/A')}")

if __name__ == "__main__":
    main()
