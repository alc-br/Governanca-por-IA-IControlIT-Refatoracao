#!/usr/bin/env python3
# Atribui Work Items aos Iteration Paths (Sprints) baseado na Fase

import os
import sys
import requests
import glob

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

def get_headers_patch():
    return {
        "Content-Type": "application/json-patch+json",
        "Accept": "application/json"
    }

# Mapeamento completo de Fases com datas
ITERATIONS = {
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

def create_iteration(iteration_name, start_date, finish_date):
    """Cria ou atualiza um Iteration Path"""
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
            return True
        elif r.status_code == 409:
            # Ja existe, tentar atualizar
            return update_iteration(iteration_name, start_date, finish_date)
        else:
            print(f"[!!] Erro ao criar Iteration {iteration_name}: {r.status_code}")
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
            return True
        return False
    except:
        return False

def load_all_status_files():
    """Carrega todos os STATUS.yaml e mapeia work_item_id -> Fase"""
    pattern = "D:/IC2/docs/rf/**/STATUS.yaml"
    files = glob.glob(pattern, recursive=True)

    work_item_to_fase = {}

    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Parse simples do YAML
            work_item_id = None
            fase = None

            for line in content.split('\n'):
                if line.strip().startswith('work_item_id:'):
                    work_item_id = line.split(':')[1].strip()
                elif line.strip().startswith('fase:'):
                    fase = line.split(':')[1].strip()

            if work_item_id and fase and work_item_id.isdigit():
                work_item_to_fase[int(work_item_id)] = fase

        except Exception as e:
            print(f"[!!] Erro ao processar {file_path}: {e}")
            continue

    return work_item_to_fase

def assign_work_item_to_iteration(work_item_id, fase):
    """Atribui um Work Item a um Iteration Path"""
    iteration_path = f"{PROJECT}\\{fase}"

    url = f"{ORG_URL}/{PROJECT}/_apis/wit/workitems/{work_item_id}?api-version=7.0"

    payload = [
        {
            "op": "replace",
            "path": "/fields/System.IterationPath",
            "value": iteration_path
        }
    ]

    try:
        r = requests.patch(url, json=payload, headers=get_headers_patch(), auth=get_auth())

        if r.status_code == 200:
            return True
        else:
            print(f"[!!] Erro ao atribuir WI {work_item_id} a {fase}: {r.status_code}")
            print(f"     Response: {r.text[:200]}")
            return False
    except Exception as e:
        print(f"[!!] Excecao ao atribuir WI {work_item_id}: {e}")
        return False

def main():
    if not all([ORG_URL, PROJECT, TOKEN]):
        print("Variaveis de ambiente necessarias:")
        print("  AZDO_ORG_URL - URL da organizacao")
        print("  AZDO_PROJECT - Nome do projeto")
        print("  AZDO_PAT     - Personal Access Token")
        sys.exit(1)

    print("="*70)
    print("CRIACAO DE SPRINTS E ATRIBUICAO DE WORK ITEMS")
    print("="*70)
    print(f"Org: {ORG_URL}")
    print(f"Project: {PROJECT}")
    print()

    # Passo 1: Criar todos os Iteration Paths
    print("PASSO 1: Criando Iteration Paths (Sprints)")
    print("-"*70)

    for fase_nome, dates in ITERATIONS.items():
        if create_iteration(fase_nome, dates['start'], dates['finish']):
            print(f"[OK] {fase_nome}")
        else:
            print(f"[!!] Falha: {fase_nome}")

    print()

    # Passo 2: Carregar mapeamento Work Item -> Fase
    print("PASSO 2: Carregando mapeamento Work Items -> Fases")
    print("-"*70)

    work_item_to_fase = load_all_status_files()
    print(f"[INFO] {len(work_item_to_fase)} Work Items mapeados")
    print()

    # Passo 3: Atribuir Work Items aos Iteration Paths
    print("PASSO 3: Atribuindo Work Items aos Sprints")
    print("-"*70)

    success_count = 0
    fail_count = 0

    # Agrupar por fase para melhor visualizacao
    fase_counts = {}
    for work_item_id, fase in sorted(work_item_to_fase.items()):
        if assign_work_item_to_iteration(work_item_id, fase):
            success_count += 1
            fase_counts[fase] = fase_counts.get(fase, 0) + 1
            print(f"[OK] WI {work_item_id} -> {fase}")
        else:
            fail_count += 1

    print()
    print("="*70)
    print("RESUMO")
    print("="*70)
    print(f"Work Items atribuidos: {success_count}")
    print(f"Falhas: {fail_count}")
    print()
    print("Distribuicao por Fase:")
    for fase, count in sorted(fase_counts.items()):
        print(f"  {fase}: {count} Work Items")
    print("="*70)

if __name__ == "__main__":
    main()
