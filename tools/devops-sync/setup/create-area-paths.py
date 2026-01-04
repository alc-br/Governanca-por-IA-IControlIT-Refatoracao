#!/usr/bin/env python3
# Cria Area Paths para as Fases no Azure DevOps

import os
import sys
import requests
from datetime import datetime

# Configuracoes
ORG_URL = os.getenv("AZDO_ORG_URL")
PROJECT = os.getenv("AZDO_PROJECT")
TOKEN = os.getenv("AZDO_PAT")

# Area Paths a serem criados (nomes das Fases)
AREA_PATHS = [
    "Fase-1-Sistema-Base",
    "Fase-2-Cadastros-e-Servicos-Transversais",
    "Fase-3-Financeiro-I-Base-Contabil",
    "Fase-4-Financeiro-II-Processos",
    "Fase-5-Service-Desk",
    "Fase-6-Ativos-Auditoria-Integracoes"
]

def get_auth():
    return ("", TOKEN)

def get_headers():
    return {"Content-Type": "application/json"}

def create_area_path(area_name):
    """Cria um Area Path no Azure DevOps"""
    url = f"{ORG_URL}/{PROJECT}/_apis/wit/classificationnodes/Areas?api-version=7.0"

    payload = {
        "name": area_name
    }

    try:
        r = requests.post(url, json=payload, headers=get_headers(), auth=get_auth())

        if r.status_code in [200, 201]:
            return True
        elif r.status_code == 409:
            print(f"[>>] Area Path ja existe: {area_name}")
            return True
        else:
            print(f"[!!] Erro ao criar Area Path {area_name}: {r.status_code}")
            print(f"     Resposta: {r.text[:500]}")
            return False
    except Exception as e:
        print(f"[!!] Excecao ao criar Area Path {area_name}: {e}")
        return False

def main():
    if not all([ORG_URL, PROJECT, TOKEN]):
        print("=" * 80)
        print("CREATE AREA PATHS - VARIAVEIS NAO CONFIGURADAS")
        print("=" * 80)
        print("\nDefina: AZDO_ORG_URL, AZDO_PROJECT, AZDO_PAT")
        print("=" * 80)
        sys.exit(1)

    print("=" * 80)
    print("CRIACAO DE AREA PATHS PARA FASES")
    print("=" * 80)
    print(f"Org: {ORG_URL}")
    print(f"Project: {PROJECT}")
    print(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    created = 0
    errors = 0

    for area_name in AREA_PATHS:
        print(f"[+] Criando Area Path: {PROJECT}\\{area_name}")
        if create_area_path(area_name):
            print(f"    [OK] Area Path criado/existente")
            created += 1
        else:
            errors += 1

    print()
    print("=" * 80)
    print("RESUMO")
    print("=" * 80)
    print(f"Area Paths criados/existentes: {created}")
    print(f"Erros: {errors}")
    print("=" * 80)

    return 0 if errors == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
