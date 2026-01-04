#!/usr/bin/env python3
# Atualiza as datas dos Iteration Paths diretamente sob iControlIT 2.0 (sem /Iteration/)

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

# Datas corrigidas conforme usuario especificou
ITERATIONS_WITH_DATES = {
    "Fase-1-Sistema-Base": {
        "start": "2024-01-01",
        "finish": "2024-11-30"  # Terminou ultimo dia de Novembro
    },
    "Fase-2-Cadastros-e-Servicos-Transversais": {
        "start": "2024-12-01",
        "finish": "2024-12-31"  # Termina 31 de Dezembro
    },
    "Fase-3-Financeiro-I-Base-Contabil": {
        "start": "2025-01-01",
        "finish": "2025-01-31"  # 31 de Janeiro
    },
    "Fase-4-Financeiro-II-Processos": {
        "start": "2025-02-01",
        "finish": "2025-02-28"  # 28 de Fevereiro
    },
    "Fase-5-Service-Desk": {
        "start": "2025-03-01",
        "finish": "2025-03-31"  # 31 de Marco
    },
    "Fase-6-Ativos-Auditoria-Integracoes": {
        "start": "2025-04-01",
        "finish": "2025-04-30"  # 30 de Abril
    }
}

def update_iteration_dates(iteration_name, start_date, finish_date):
    """Atualiza as datas de um Iteration Path usando PATCH"""
    # Encode the iteration name for URL
    iteration_encoded = urllib.parse.quote(iteration_name)

    url = f"{ORG_URL}/{PROJECT}/_apis/wit/classificationnodes/iterations/{iteration_encoded}?api-version=7.0"

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
            return False, f"HTTP {r.status_code}: {r.text[:200]}"
    except Exception as e:
        return False, f"Exception: {e}"

def main():
    if not all([ORG_URL, PROJECT, TOKEN]):
        print("Variaveis de ambiente necessarias:")
        print("  AZDO_ORG_URL - URL da organizacao")
        print("  AZDO_PROJECT - Nome do projeto")
        print("  AZDO_PAT     - Personal Access Token")
        sys.exit(1)

    print("="*70)
    print("ATUALIZACAO DE DATAS DOS SPRINTS")
    print("="*70)
    print(f"Org: {ORG_URL}")
    print(f"Project: {PROJECT}")
    print()

    success_count = 0
    fail_count = 0

    for fase_nome, dates in ITERATIONS_WITH_DATES.items():
        start = dates['start']
        finish = dates['finish']

        print(f"Atualizando: {fase_nome}")
        print(f"  Inicio: {start}")
        print(f"  Termino: {finish}")

        success, message = update_iteration_dates(fase_nome, start, finish)

        if success:
            print(f"  [OK] Datas atualizadas com sucesso!")
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
        print("PROXIMO PASSO:")
        print("  1. Aguarde alguns segundos para sincronizacao")
        print("  2. Acesse os Sprint Backlogs:")
        print("     - Fase-1: https://dev.azure.com/IControlIT-v2/iControlIT%202.0/_sprints/backlog/iControlIT%202.0%20Team/iControlIT%202.0/Fase-1-Sistema-Base")
        print("     - Fase-2: https://dev.azure.com/IControlIT-v2/iControlIT%202.0/_sprints/backlog/iControlIT%202.0%20Team/iControlIT%202.0/Fase-2-Cadastros-e-Servicos-Transversais")
        print("     - Fase-3: https://dev.azure.com/IControlIT-v2/iControlIT%202.0/_sprints/backlog/iControlIT%202.0%20Team/iControlIT%202.0/Fase-3-Financeiro-I-Base-Contabil")
        print("  3. Verifique se os Work Items aparecem agora")
        print("  4. Acesse o Sprint Directory:")
        print("     https://dev.azure.com/IControlIT-v2/iControlIT%202.0/_sprints/directory")

    print("="*70)

if __name__ == "__main__":
    main()
