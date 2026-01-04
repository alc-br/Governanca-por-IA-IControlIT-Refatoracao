#!/usr/bin/env python3
# Verifica quais niveis de backlog estao habilitados no Team

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

def get_team_field_values(team_name):
    """Obtem configuracoes de backlog do Team"""
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

def get_backlog_configuration(team_name):
    """Obtem configuracao de niveis de backlog"""
    project_encoded = urllib.parse.quote(PROJECT)
    team_encoded = urllib.parse.quote(team_name)

    url = f"{ORG_URL}/{project_encoded}/{team_encoded}/_apis/work/backlogs?api-version=7.0"

    try:
        r = requests.get(url, headers=get_headers(), auth=get_auth())
        if r.status_code == 200:
            return r.json()
        return None
    except:
        return None

def main():
    if not all([ORG_URL, PROJECT, TOKEN]):
        print("Variaveis de ambiente necessarias:")
        print("  AZDO_ORG_URL, AZDO_PROJECT, AZDO_PAT")
        sys.exit(1)

    print("="*70)
    print("VERIFICACAO DE NIVEIS DE BACKLOG DO TEAM")
    print("="*70)
    print(f"Org: {ORG_URL}")
    print(f"Project: {PROJECT}")
    print()

    # Obter Team
    team_id, team_name = get_team_id()
    if not team_id:
        print("[!!] Nao foi possivel obter o team ID")
        sys.exit(1)

    print(f"Team: {team_name}")
    print(f"Team ID: {team_id}")
    print()

    # Obter configuracoes do Team
    print("Configuracoes do Team:")
    print("-"*70)

    team_settings = get_team_field_values(team_name)
    if team_settings:
        backlog_iteration = team_settings.get('backlogIteration', {})
        print(f"Backlog Iteration: {backlog_iteration.get('name', 'N/A')}")
        print(f"Default Iteration: {team_settings.get('defaultIteration', {}).get('name', 'N/A')}")
        print(f"Default Iteration Macro: {team_settings.get('defaultIterationMacro', 'N/A')}")
    print()

    # Obter niveis de backlog
    print("Niveis de Backlog habilitados:")
    print("-"*70)

    backlog_config = get_backlog_configuration(team_name)
    if backlog_config:
        backlogs = backlog_config.get('value', [])

        for backlog in backlogs:
            name = backlog.get('name', 'N/A')
            backlog_type = backlog.get('type', 'N/A')
            is_hidden = backlog.get('isHidden', False)

            status = "[OCULTO]" if is_hidden else "[VISIVEL]"

            print(f"  - {name} ({backlog_type}) {status}")

            # Work Item Types suportados
            work_item_types = backlog.get('workItemTypes', [])
            if work_item_types:
                print(f"    Work Item Types:")
                for wit in work_item_types:
                    wit_name = wit.get('name', 'N/A')
                    print(f"      * {wit_name}")

        print()

    print("="*70)
    print("DIAGNOSTICO")
    print("="*70)

    # Verificar se Features esta visivel
    features_visible = False
    if backlog_config:
        for backlog in backlog_config.get('value', []):
            if 'Feature' in backlog.get('name', ''):
                if not backlog.get('isHidden', False):
                    features_visible = True
                    break

    if features_visible:
        print("[OK] Features ESTAO VISIVEIS no backlog do Team")
        print()
        print("Os Work Items do tipo Feature DEVEM aparecer em:")
        print("  - Features Backlog")
        print("  - Sprint Backlogs (se tiverem IterationPath)")
        print()
        print("Mas Features NAO APARECEM em:")
        print("  - Sprint Taskboard (comportamento esperado)")
    else:
        print("[!!] Features estao OCULTAS no backlog do Team")
        print()
        print("SOLUCAO:")
        print("  1. Acesse: https://dev.azure.com/IControlIT-v2/iControlIT%202.0/_settings/work-team")
        print("  2. Va em 'Backlog navigation levels'")
        print("  3. Marque a checkbox 'Features'")
        print("  4. Salve as alteracoes")
        print()
        print("Apos isso, Features aparecerao nos Sprint Backlogs.")

    print()
    print("NOTA IMPORTANTE:")
    print("  Sprint TASKBOARD nunca mostra Features.")
    print("  Use Sprint BACKLOG para ver Features.")
    print("="*70)

if __name__ == "__main__":
    main()
