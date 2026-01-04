#!/usr/bin/env python3
# Atualiza datas buscando primeiro o ID do no e depois atualizando pelo ID

import os
import sys
import requests

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

ITERATIONS_WITH_DATES = {
    "Fase-1-Sistema-Base": {
        "start": "2024-01-01T00:00:00Z",
        "finish": "2024-11-30T23:59:59Z"
    },
    "Fase-2-Cadastros-e-Servicos-Transversais": {
        "start": "2024-12-01T00:00:00Z",
        "finish": "2024-12-31T23:59:59Z"
    },
    "Fase-3-Financeiro-I-Base-Contabil": {
        "start": "2025-01-01T00:00:00Z",
        "finish": "2025-01-31T23:59:59Z"
    },
    "Fase-4-Financeiro-II-Processos": {
        "start": "2025-02-01T00:00:00Z",
        "finish": "2025-02-28T23:59:59Z"
    },
    "Fase-5-Service-Desk": {
        "start": "2025-03-01T00:00:00Z",
        "finish": "2025-03-31T23:59:59Z"
    },
    "Fase-6-Ativos-Auditoria-Integracoes": {
        "start": "2025-04-01T00:00:00Z",
        "finish": "2025-04-30T23:59:59Z"
    }
}

def get_iteration_tree():
    """Busca toda a arvore de iterations"""
    url = f"{ORG_URL}/{PROJECT}/_apis/wit/classificationnodes/iterations?$depth=10&api-version=7.0"

    try:
        r = requests.get(url, headers=get_headers(), auth=get_auth())
        if r.status_code == 200:
            return r.json()
        return None
    except:
        return None

def find_iteration_id(tree, iteration_name):
    """Busca o ID de um iteration pelo nome na arvore"""
    if tree.get('name') == iteration_name:
        return tree.get('id'), tree.get('path')

    children = tree.get('children', [])
    for child in children:
        result = find_iteration_id(child, iteration_name)
        if result:
            return result

    return None

def update_iteration_by_id(iteration_id, iteration_path, start_date, finish_date):
    """Atualiza um iteration usando seu path"""
    # Extrair apenas o nome do ultimo componente do path
    # Path: \iControlIT 2.0\Iteration\Fase-1-Sistema-Base
    # Precisamos apenas: Fase-1-Sistema-Base
    path_parts = iteration_path.split('\\')
    iteration_name = path_parts[-1]

    import urllib.parse
    encoded_name = urllib.parse.quote(iteration_name)

    url = f"{ORG_URL}/{PROJECT}/_apis/wit/classificationnodes/iterations/{encoded_name}?api-version=7.0"

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
        print("  AZDO_ORG_URL, AZDO_PROJECT, AZDO_PAT")
        sys.exit(1)

    print("="*70)
    print("ATUALIZACAO DE DATAS POR ID DO NO")
    print("="*70)
    print(f"Org: {ORG_URL}")
    print(f"Project: {PROJECT}")
    print()

    # Buscar arvore completa
    print("Buscando arvore de Iteration Paths...")
    tree = get_iteration_tree()

    if not tree:
        print("[!!] Nao foi possivel obter a arvore")
        sys.exit(1)

    print(f"[OK] Arvore obtida")
    print()

    success_count = 0
    fail_count = 0

    for fase_nome, dates in ITERATIONS_WITH_DATES.items():
        start = dates['start']
        finish = dates['finish']

        print(f"Processando: {fase_nome}")

        # Buscar ID do no
        result = find_iteration_id(tree, fase_nome)

        if not result:
            print(f"  [!!] NAO ENCONTRADO na arvore")
            fail_count += 1
            print()
            continue

        iteration_id, iteration_path = result
        print(f"  ID: {iteration_id}")
        print(f"  Path: {iteration_path}")
        print(f"  Inicio: {start}")
        print(f"  Termino: {finish}")

        success, message = update_iteration_by_id(iteration_id, iteration_path, start, finish)

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
        print("Apos verificacao, acesse:")
        print("  https://dev.azure.com/IControlIT-v2/iControlIT%202.0/_sprints/directory")

    print("="*70)

if __name__ == "__main__":
    main()
