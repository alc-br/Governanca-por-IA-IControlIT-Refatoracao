#!/usr/bin/env python3
# Valida se os Work Items realmente aparecem nos Sprint Backlogs
# Simula a query que o Azure DevOps faz para exibir Sprint Backlogs

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

def query_work_items_by_iteration(iteration_path):
    """Busca Work Items por Iteration Path usando WIQL"""
    url = f"{ORG_URL}/{PROJECT}/_apis/wit/wiql?api-version=7.0"

    # Query WIQL que o Sprint Backlog usa
    wiql = {
        "query": f"""
            SELECT [System.Id], [System.Title], [System.State], [System.WorkItemType]
            FROM WorkItems
            WHERE [System.TeamProject] = @project
            AND [System.IterationPath] = '{iteration_path}'
            ORDER BY [System.Id]
        """
    }

    try:
        r = requests.post(url, json=wiql, headers=get_headers(), auth=get_auth())

        if r.status_code == 200:
            result = r.json()
            work_items = result.get('workItems', [])
            return [wi['id'] for wi in work_items]
        else:
            return None
    except Exception as e:
        return None

def get_work_item_details(work_item_ids):
    """Busca detalhes de multiplos Work Items"""
    if not work_item_ids:
        return []

    ids_str = ','.join(str(id) for id in work_item_ids)
    url = f"{ORG_URL}/{PROJECT}/_apis/wit/workitems?ids={ids_str}&fields=System.Id,System.Title,System.State,System.WorkItemType&api-version=7.0"

    try:
        r = requests.get(url, headers=get_headers(), auth=get_auth())

        if r.status_code == 200:
            result = r.json()
            return result.get('value', [])
        return []
    except:
        return []

def main():
    if not all([ORG_URL, PROJECT, TOKEN]):
        print("Variaveis de ambiente necessarias:")
        print("  AZDO_ORG_URL, AZDO_PROJECT, AZDO_PAT")
        sys.exit(1)

    fases = {
        "Fase-1-Sistema-Base": "iControlIT 2.0\\Fase-1-Sistema-Base",
        "Fase-2-Cadastros-e-Servicos-Transversais": "iControlIT 2.0\\Fase-2-Cadastros-e-Servicos-Transversais",
        "Fase-3-Financeiro-I-Base-Contabil": "iControlIT 2.0\\Fase-3-Financeiro-I-Base-Contabil",
        "Fase-4-Financeiro-II-Processos": "iControlIT 2.0\\Fase-4-Financeiro-II-Processos",
        "Fase-5-Service-Desk": "iControlIT 2.0\\Fase-5-Service-Desk",
        "Fase-6-Ativos-Auditoria-Integracoes": "iControlIT 2.0\\Fase-6-Ativos-Auditoria-Integracoes"
    }

    print("="*70)
    print("VALIDACAO FINAL DOS SPRINT BACKLOGS")
    print("="*70)
    print(f"Org: {ORG_URL}")
    print(f"Project: {PROJECT}")
    print()
    print("Simulando consulta que o Sprint Backlog faz...")
    print()

    total_work_items = 0
    total_phases_with_items = 0

    for fase_nome, iteration_path in fases.items():
        print(f"Fase: {fase_nome}")
        print(f"  Iteration Path: {iteration_path}")

        # Buscar Work Items
        work_item_ids = query_work_items_by_iteration(iteration_path)

        if work_item_ids is None:
            print(f"  [!!] ERRO ao consultar Work Items")
            print()
            continue

        if not work_item_ids:
            print(f"  [!!] NENHUM Work Item encontrado")
            print(f"  [!!] Sprint Backlog estara VAZIO")
            print()
            continue

        # Buscar detalhes
        work_items = get_work_item_details(work_item_ids)

        print(f"  [OK] {len(work_items)} Work Items encontrados:")
        total_work_items += len(work_items)
        total_phases_with_items += 1

        # Mostrar primeiros 5
        for i, wi in enumerate(work_items[:5]):
            fields = wi.get('fields', {})
            wi_id = fields.get('System.Id', 'N/A')
            title = fields.get('System.Title', 'N/A')
            state = fields.get('System.State', 'N/A')
            wi_type = fields.get('System.WorkItemType', 'N/A')

            print(f"    - ID {wi_id}: {title[:50]}... [{wi_type}] ({state})")

        if len(work_items) > 5:
            print(f"    ... e mais {len(work_items) - 5} Work Items")

        print()

    print("="*70)
    print("RESULTADO FINAL DA VALIDACAO")
    print("="*70)
    print(f"Total de Work Items nos Sprint Backlogs: {total_work_items}")
    print(f"Fases com Work Items: {total_phases_with_items} de {len(fases)}")
    print()

    if total_phases_with_items == len(fases) and total_work_items > 0:
        print("[OK] VALIDACAO BEM-SUCEDIDA!")
        print()
        print("Os Sprint Backlogs devem exibir os Work Items corretamente.")
        print()
        print("Links para verificacao visual:")
        print("  Sprint Directory:")
        print("    https://dev.azure.com/IControlIT-v2/iControlIT%202.0/_sprints/directory")
        print()
        print("  Sprint Backlogs:")
        print("    Fase-1: https://dev.azure.com/IControlIT-v2/iControlIT%202.0/_sprints/backlog/iControlIT%202.0%20Team/iControlIT%202.0/Fase-1-Sistema-Base")
        print("    Fase-2: https://dev.azure.com/IControlIT-v2/iControlIT%202.0/_sprints/backlog/iControlIT%202.0%20Team/iControlIT%202.0/Fase-2-Cadastros-e-Servicos-Transversais")
        print("    Fase-3: https://dev.azure.com/IControlIT-v2/iControlIT%202.0/_sprints/backlog/iControlIT%202.0%20Team/iControlIT%202.0/Fase-3-Financeiro-I-Base-Contabil")
    else:
        print("[!!] VALIDACAO FALHOU")
        print()
        print("Algumas Fases nao tem Work Items ou houve erro na consulta.")
        print("Verifique:")
        print("  1. Se os Work Items tem IterationPath correto")
        print("  2. Se as Iterations estao configuradas no Team Settings")
        print("  3. Se as datas dos Sprints estao definidas")

    print("="*70)

if __name__ == "__main__":
    main()
