#!/usr/bin/env python3
# Verifica as datas dos Iteration Paths corretos (diretamente sob iControlIT 2.0)

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

def get_team_iterations(team_name):
    """Lista os Iteration Paths configurados no Team"""
    project_encoded = urllib.parse.quote(PROJECT)
    team_encoded = urllib.parse.quote(team_name)

    url = f"{ORG_URL}/{project_encoded}/{team_encoded}/_apis/work/teamsettings/iterations?api-version=7.0"

    try:
        r = requests.get(url, headers=get_headers(), auth=get_auth())
        if r.status_code == 200:
            iterations = r.json().get('value', [])
            return iterations
        else:
            return []
    except Exception as e:
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
    except Exception as e:
        return None, None

def main():
    if not all([ORG_URL, PROJECT, TOKEN]):
        print("Variaveis de ambiente necessarias:")
        print("  AZDO_ORG_URL - URL da organizacao")
        print("  AZDO_PROJECT - Nome do projeto")
        print("  AZDO_PAT     - Personal Access Token")
        sys.exit(1)

    print("="*70)
    print("VERIFICACAO FINAL DOS SPRINTS")
    print("="*70)
    print(f"Org: {ORG_URL}")
    print(f"Project: {PROJECT}")
    print()

    # Obter Team ID
    team_id, team_name = get_team_id()
    if not team_id:
        print("[!!] Nao foi possivel obter o team ID")
        sys.exit(1)

    print(f"Team: {team_name}")
    print()

    # Listar Iterations configuradas no Team (com datas)
    print("Sprints configurados no Team:")
    print("-"*70)

    team_iterations = get_team_iterations(team_name)

    if not team_iterations:
        print("[!!] Nenhuma Iteration configurada no Team!")
        sys.exit(1)

    all_have_dates = True

    for it in team_iterations:
        name = it.get('name')
        path = it.get('path')
        attrs = it.get('attributes', {})
        start = attrs.get('startDate')
        finish = attrs.get('finishDate')

        print(f"\n{name}")
        print(f"  Path: {path}")

        if start and finish:
            print(f"  Inicio: {start[:10]}")  # Pegar apenas YYYY-MM-DD
            print(f"  Termino: {finish[:10]}")
            print(f"  [OK] Datas configuradas!")
        else:
            print(f"  [!!] SEM DATAS definidas")
            all_have_dates = False

    print()
    print("="*70)
    print("RESULTADO FINAL")
    print("="*70)

    if all_have_dates:
        print("[OK] TODOS OS SPRINTS TEM DATAS CONFIGURADAS!")
        print()
        print("Os Sprint Backlogs agora devem exibir os Work Items.")
        print()
        print("Links de verificacao:")
        print("  - Sprint Directory:")
        print("    https://dev.azure.com/IControlIT-v2/iControlIT%202.0/_sprints/directory")
        print()
        print("  - Sprint Backlogs:")
        print("    Fase-1: https://dev.azure.com/IControlIT-v2/iControlIT%202.0/_sprints/backlog/iControlIT%202.0%20Team/iControlIT%202.0/Fase-1-Sistema-Base")
        print("    Fase-2: https://dev.azure.com/IControlIT-v2/iControlIT%202.0/_sprints/backlog/iControlIT%202.0%20Team/iControlIT%202.0/Fase-2-Cadastros-e-Servicos-Transversais")
        print("    Fase-3: https://dev.azure.com/IControlIT-v2/iControlIT%202.0/_sprints/backlog/iControlIT%202.0%20Team/iControlIT%202.0/Fase-3-Financeiro-I-Base-Contabil")
    else:
        print("[!!] ALGUNS SPRINTS AINDA NAO TEM DATAS")
        print("    Execute novamente: python update-sprint-dates-direct.py")

    print("="*70)

if __name__ == "__main__":
    main()
