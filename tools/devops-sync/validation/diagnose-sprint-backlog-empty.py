#!/usr/bin/env python3
# Diagnostica por que Sprint Backlog esta vazio

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

def get_team_settings(team_name):
    """Obtem configuracoes do Team incluindo Area Paths"""
    project_encoded = urllib.parse.quote(PROJECT)
    team_encoded = urllib.parse.quote(team_name)

    url = f"{ORG_URL}/{project_encoded}/{team_encoded}/_apis/work/teamsettings?api-version=7.0"

    try:
        r = requests.get(url, headers=get_headers(), auth=get_auth())
        if r.status_code == 200:
            return r.json()
        return None
    except:
        return None

def get_team_field_values(team_name):
    """Obtem os Area Paths configurados no Team"""
    project_encoded = urllib.parse.quote(PROJECT)
    team_encoded = urllib.parse.quote(team_name)

    url = f"{ORG_URL}/{project_encoded}/{team_encoded}/_apis/work/teamsettings/teamfieldvalues?api-version=7.0"

    try:
        r = requests.get(url, headers=get_headers(), auth=get_auth())
        if r.status_code == 200:
            return r.json()
        return None
    except:
        return None

def query_work_items_fase1():
    """Busca Work Items da Fase-1 com detalhes completos"""
    url = f"{ORG_URL}/{PROJECT}/_apis/wit/wiql?api-version=7.0"

    wiql = {
        "query": """
            SELECT [System.Id], [System.Title], [System.State], [System.WorkItemType],
                   [System.AreaPath], [System.IterationPath]
            FROM WorkItems
            WHERE [System.TeamProject] = @project
            AND [System.IterationPath] = 'iControlIT 2.0\\Fase-1-Sistema-Base'
            ORDER BY [System.Id]
        """
    }

    try:
        r = requests.post(url, json=wiql, headers=get_headers(), auth=get_auth())

        if r.status_code == 200:
            result = r.json()
            work_items = result.get('workItems', [])
            return [wi['id'] for wi in work_items]
        return []
    except:
        return []

def get_work_item_details(work_item_ids):
    """Busca detalhes completos dos Work Items"""
    if not work_item_ids:
        return []

    ids_str = ','.join(str(id) for id in work_item_ids)
    url = f"{ORG_URL}/{PROJECT}/_apis/wit/workitems?ids={ids_str}&api-version=7.0"

    try:
        r = requests.get(url, headers=get_headers(), auth=get_auth())

        if r.status_code == 200:
            result = r.json()
            return result.get('value', [])
        return []
    except:
        return []

def get_team_id():
    """Obtem o ID do team principal"""
    url = f"{ORG_URL}/_apis/projects/{PROJECT}/teams?api-version=7.0"

    try:
        r = requests.get(url, headers=get_headers(), auth=get_auth())
        if r.status_code == 200:
            teams = r.json().get('value', [])
            if teams:
                team = teams[0]
                return team.get('id'), team.get('name')
        return None, None
    except:
        return None, None

def main():
    if not all([ORG_URL, PROJECT, TOKEN]):
        print("Variaveis de ambiente necessarias:")
        print("  AZDO_ORG_URL, AZDO_PROJECT, AZDO_PAT")
        sys.exit(1)

    print("="*70)
    print("DIAGNOSTICO: POR QUE SPRINT BACKLOG ESTA VAZIO?")
    print("="*70)
    print(f"Org: {ORG_URL}")
    print(f"Project: {PROJECT}")
    print(f"Sprint: Fase-1-Sistema-Base")
    print()

    # Obter Team
    team_id, team_name = get_team_id()
    if not team_id:
        print("[!!] Nao foi possivel obter o team ID")
        sys.exit(1)

    print(f"Team: {team_name}")
    print()

    # Verificar configuracao de Area Paths do Team
    print("PASSO 1: Verificando Area Paths do Team")
    print("-"*70)

    team_field_values = get_team_field_values(team_name)
    team_settings = get_team_settings(team_name)

    if team_field_values:
        default_value = team_field_values.get('defaultValue')
        values = team_field_values.get('values', [])

        print(f"Default Area Path: {default_value}")
        print(f"Area Paths incluidos: {len(values)}")

        for val in values[:10]:  # Primeiros 10
            print(f"  - {val.get('value', 'N/A')} (includeChildren: {val.get('includeChildren', False)})")

        if len(values) > 10:
            print(f"  ... e mais {len(values) - 10} Area Paths")

    print()

    # Verificar Backlog Iteration
    print("PASSO 2: Verificando Backlog Iteration")
    print("-"*70)

    if team_settings:
        backlog_iteration = team_settings.get('backlogIteration', {})
        print(f"Backlog Iteration: {backlog_iteration.get('name', 'N/A')}")
        print(f"Path: {backlog_iteration.get('path', 'N/A')}")

    print()

    # Buscar Work Items da Fase-1
    print("PASSO 3: Buscando Work Items da Fase-1")
    print("-"*70)

    work_item_ids = query_work_items_fase1()
    print(f"Work Items encontrados: {len(work_item_ids)}")

    if not work_item_ids:
        print("[!!] NENHUM Work Item encontrado para Fase-1")
        print("    Isso nao deveria acontecer!")
        sys.exit(1)

    # Buscar detalhes
    work_items = get_work_item_details(work_item_ids)

    print()
    print("PASSO 4: Analisando Area Paths dos Work Items")
    print("-"*70)

    area_paths = {}
    mismatches = []

    for wi in work_items:
        fields = wi.get('fields', {})
        wi_id = fields.get('System.Id')
        area_path = fields.get('System.AreaPath', 'N/A')
        iteration_path = fields.get('System.IterationPath', 'N/A')
        title = fields.get('System.Title', 'N/A')

        # Contar por Area Path
        if area_path not in area_paths:
            area_paths[area_path] = 0
        area_paths[area_path] += 1

        # Verificar se esta no Area Path do Team
        if team_field_values and default_value:
            if not area_path.startswith(default_value):
                mismatches.append({
                    'id': wi_id,
                    'title': title,
                    'area': area_path,
                    'iteration': iteration_path
                })

    print(f"Distribuicao por Area Path:")
    for area, count in sorted(area_paths.items()):
        print(f"  {area}: {count} Work Items")

    print()

    # Diagnostico final
    print("="*70)
    print("DIAGNOSTICO FINAL")
    print("="*70)

    if mismatches:
        print(f"[!!] PROBLEMA IDENTIFICADO!")
        print()
        print(f"{len(mismatches)} Work Items NAO estao no Area Path do Team:")
        print(f"Team Area Path esperado: {default_value}")
        print()
        print("Work Items com Area Path incorreto:")
        for item in mismatches[:5]:
            print(f"  - ID {item['id']}: {item['title'][:50]}")
            print(f"    Area Path atual: {item['area']}")
            print(f"    Area Path esperado: {default_value}\\...")

        if len(mismatches) > 5:
            print(f"  ... e mais {len(mismatches) - 5} Work Items")

        print()
        print("SOLUCAO:")
        print("  Os Work Items precisam ter Area Path compativel com o Team.")
        print()
        print("  Opcao 1: Atualizar Area Path dos Work Items")
        print(f"    - Alterar para: {default_value}\\Fase-1-Sistema-Base")
        print()
        print("  Opcao 2: Adicionar Area Paths no Team Settings")
        print("    - Acesse: https://dev.azure.com/IControlIT-v2/iControlIT%202.0/_settings/work-team")
        print("    - Adicione os Area Paths usados pelos Work Items")

    else:
        print("[OK] Todos os Work Items estao no Area Path do Team")
        print()
        print("Outros possiveis problemas:")
        print("  1. Cache do navegador - Tente Ctrl+F5")
        print("  2. Delay de sincronizacao - Aguarde alguns minutos")
        print("  3. Filtros ativos no Sprint Backlog - Limpe os filtros")

    print("="*70)

if __name__ == "__main__":
    main()
