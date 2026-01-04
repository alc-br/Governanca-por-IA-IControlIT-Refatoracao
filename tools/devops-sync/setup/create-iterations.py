#!/usr/bin/env python3
# Cria Iteration Paths (Sprints) para as Fases do projeto

import os
import sys
import requests
from datetime import datetime

ORG_URL = os.getenv("AZDO_ORG_URL")
PROJECT = os.getenv("AZDO_PROJECT")
TOKEN = os.getenv("AZDO_PAT")

def get_auth():
    return ("", TOKEN)

def get_headers():
    return {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

# Definicao das Fases com datas de inicio e termino
ITERATIONS = [
    {
        "name": "Fase-3-Financeiro-I-Base-Contabil",
        "start_date": "2024-12-27",  # Hoje
        "finish_date": "2025-01-31"
    },
    {
        "name": "Fase-4-Financeiro-II-Processos",
        "start_date": "2025-02-01",
        "finish_date": "2025-02-28"
    },
    {
        "name": "Fase-5-Service-Desk",
        "start_date": "2025-03-01",
        "finish_date": "2025-03-31"
    },
    {
        "name": "Fase-6-Ativos-Auditoria-Integracoes",
        "start_date": "2025-04-01",
        "finish_date": "2025-04-30"
    }
]

def create_iteration(iteration_name, start_date, finish_date):
    """Cria um Iteration Path (Sprint)"""
    url = f"{ORG_URL}/{PROJECT}/_apis/wit/classificationnodes/iterations?api-version=7.0"

    payload = {
        "name": iteration_name,
        "attributes": {
            "startDate": start_date,
            "finishDate": finish_date
        }
    }

    try:
        r = requests.post(url, json=payload, headers=get_headers(), auth=get_auth())

        if r.status_code in [200, 201]:
            print(f"[OK] Iteration criada: {iteration_name}")
            print(f"     Inicio: {start_date}")
            print(f"     Termino: {finish_date}")
            return True
        elif r.status_code == 409:
            print(f"[>>] Iteration ja existe: {iteration_name}")
            # Tentar atualizar as datas
            return update_iteration(iteration_name, start_date, finish_date)
        else:
            print(f"[!!] Erro ao criar Iteration {iteration_name}: {r.status_code}")
            print(f"     Resposta: {r.text[:500]}")
            return False
    except Exception as e:
        print(f"[!!] Excecao ao criar Iteration {iteration_name}: {e}")
        return False

def update_iteration(iteration_name, start_date, finish_date):
    """Atualiza um Iteration Path existente"""
    url = f"{ORG_URL}/{PROJECT}/_apis/wit/classificationnodes/iterations/{iteration_name}?api-version=7.0"

    payload = {
        "attributes": {
            "startDate": start_date,
            "finishDate": finish_date
        }
    }

    try:
        r = requests.patch(url, json=payload, headers=get_headers(), auth=get_auth())

        if r.status_code == 200:
            print(f"[OK] Iteration atualizada: {iteration_name}")
            print(f"     Inicio: {start_date}")
            print(f"     Termino: {finish_date}")
            return True
        else:
            print(f"[!!] Erro ao atualizar Iteration {iteration_name}: {r.status_code}")
            print(f"     Resposta: {r.text[:500]}")
            return False
    except Exception as e:
        print(f"[!!] Excecao ao atualizar Iteration {iteration_name}: {e}")
        return False

def main():
    if not all([ORG_URL, PROJECT, TOKEN]):
        print("Variaveis de ambiente necessarias:")
        print("  AZDO_ORG_URL - URL da organizacao (ex: https://dev.azure.com/org)")
        print("  AZDO_PROJECT - Nome do projeto")
        print("  AZDO_PAT     - Personal Access Token")
        sys.exit(1)

    print("="*70)
    print("CRIACAO DE ITERATION PATHS (SPRINTS)")
    print("="*70)
    print(f"Org: {ORG_URL}")
    print(f"Project: {PROJECT}")
    print()

    success_count = 0
    fail_count = 0

    for iteration in ITERATIONS:
        if create_iteration(
            iteration["name"],
            iteration["start_date"],
            iteration["finish_date"]
        ):
            success_count += 1
        else:
            fail_count += 1
        print()

    print("="*70)
    print("RESUMO")
    print("="*70)
    print(f"Iterations criadas/atualizadas: {success_count}")
    print(f"Falhas: {fail_count}")
    print("="*70)

if __name__ == "__main__":
    main()
