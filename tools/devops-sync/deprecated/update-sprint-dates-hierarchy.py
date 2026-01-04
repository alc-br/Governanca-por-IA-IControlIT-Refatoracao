#!/usr/bin/env python3
# Atualiza datas usando o path hierarquico correto (Iteration/Fase-X)

import os
import sys
import requests
import urllib.parse

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

# Datas corretas conforme usuario
ITERATIONS_WITH_DATES = {
    "Fase-1-Sistema-Base": {
        "start": "2024-01-01",
        "finish": "2024-11-30"
    },
    "Fase-2-Cadastros-e-Servicos-Transversais": {
        "start": "2024-12-01",
        "finish": "2024-12-31"
    },
    "Fase-3-Financeiro-I-Base-Contabil": {
        "start": "2025-01-01",
        "finish": "2025-01-31"
    },
    "Fase-4-Financeiro-II-Processos": {
        "start": "2025-02-01",
        "finish": "2025-02-28"
    },
    "Fase-5-Service-Desk": {
        "start": "2025-03-01",
        "finish": "2025-03-31"
    },
    "Fase-6-Ativos-Auditoria-Integracoes": {
        "start": "2025-04-01",
        "finish": "2025-04-30"
    }
}

def update_iteration_with_hierarchy(iteration_name, start_date, finish_date):
    """Atualiza usando path hierarquico: Iteration\Fase-X"""
    # Path hierarquico completo
    iteration_path = f"Iteration\\{iteration_name}"
    path_encoded = urllib.parse.quote(iteration_path)

    url = f"{ORG_URL}/{PROJECT}/_apis/wit/classificationnodes/iterations/{path_encoded}?api-version=7.0"

    payload = {
        "attributes": {
            "startDate": start_date,
            "finishDate": finish_date
        }
    }

    try:
        r = requests.patch(url, json=payload, headers=get_headers(), auth=get_auth())

        if r.status_code == 200:
            return True, "OK"
        else:
            return False, f"HTTP {r.status_code}: {r.text[:300]}"
    except Exception as e:
        return False, f"Exception: {e}"

def main():
    if not all([ORG_URL, PROJECT, TOKEN]):
        print("Variaveis de ambiente necessarias:")
        print("  AZDO_ORG_URL, AZDO_PROJECT, AZDO_PAT")
        sys.exit(1)

    print("="*70)
    print("ATUALIZACAO DE DATAS (PATH HIERARQUICO)")
    print("="*70)
    print(f"Org: {ORG_URL}")
    print(f"Project: {PROJECT}")
    print()

    success_count = 0
    fail_count = 0

    for fase_nome, dates in ITERATIONS_WITH_DATES.items():
        start = dates['start']
        finish = dates['finish']

        print(f"Atualizando: Iteration\\{fase_nome}")
        print(f"  Inicio: {start}")
        print(f"  Termino: {finish}")

        success, message = update_iteration_with_hierarchy(fase_nome, start, finish)

        if success:
            print(f"  [OK] Datas atualizadas!")
            success_count += 1
        else:
            print(f"  [!!] Erro: {message}")
            fail_count += 1

        print()

    print("="*70)
    print("RESUMO")
    print("="*70)
    print(f"Atualizacoes bem-sucedidas: {success_count}")
    print(f"Falhas: {fail_count}")
    print()

    if success_count > 0:
        print("VERIFICAR RESULTADO:")
        print("  python list-all-iterations.py")
        print()
        print("Se tudo estiver correto, acesse:")
        print("  https://dev.azure.com/IControlIT-v2/iControlIT%202.0/_sprints/directory")

    print("="*70)

if __name__ == "__main__":
    main()
