#!/usr/bin/env python3
# Verifica detalhadamente as Iterations configuradas no Team

import os
import sys
import requests
import urllib.parse
import json

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

def get_team_iterations_detailed(team_name):
    """Lista Iterations configuradas no Team com TODOS os detalhes"""
    project_encoded = urllib.parse.quote(PROJECT)
    team_encoded = urllib.parse.quote(team_name)

    url = f"{ORG_URL}/{project_encoded}/{team_encoded}/_apis/work/teamsettings/iterations?api-version=7.0"

    try:
        r = requests.get(url, headers=get_headers(), auth=get_auth())
        if r.status_code == 200:
            return r.json()
        return None
    except:
        return None

def get_team_settings(team_name):
    """Obtem configuracoes gerais do Team"""
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

def main():
    if not all([ORG_URL, PROJECT, TOKEN]):
        print("Variaveis de ambiente necessarias:")
        print("  AZDO_ORG_URL, AZDO_PROJECT, AZDO_PAT")
        sys.exit(1)

    print("="*70)
    print("VERIFICACAO DETALHADA DAS ITERATIONS DO TEAM")
    print("="*70)
    print()

    # Obter Team
    team_id, team_name = get_team_id()
    if not team_id:
        print("[!!] Nao foi possivel obter o team ID")
        sys.exit(1)

    print(f"Team: {team_name}")
    print(f"Team ID: {team_id}")
    print()

    # Obter configuracoes gerais
    print("Configuracoes Gerais do Team:")
    print("-"*70)

    team_settings = get_team_settings(team_name)
    if team_settings:
        backlog_iteration = team_settings.get('backlogIteration', {})
        default_iteration = team_settings.get('defaultIteration', {})

        print(f"Backlog Iteration:")
        print(f"  Name: {backlog_iteration.get('name', 'N/A')}")
        print(f"  Path: {backlog_iteration.get('path', 'N/A')}")
        print(f"  ID: {backlog_iteration.get('id', 'N/A')}")

        print(f"\nDefault Iteration:")
        print(f"  Name: {default_iteration.get('name', 'N/A')}")
        print(f"  Path: {default_iteration.get('path', 'N/A')}")
        print(f"  ID: {default_iteration.get('id', 'N/A')}")

        print(f"\nDefault Iteration Macro: {team_settings.get('defaultIterationMacro', 'N/A')}")

    print()

    # Obter Iterations configuradas
    print("Iterations Configuradas no Team:")
    print("-"*70)

    iterations_data = get_team_iterations_detailed(team_name)

    if not iterations_data:
        print("[!!] Nao foi possivel obter Iterations do Team")
        sys.exit(1)

    iterations = iterations_data.get('value', [])

    print(f"Total de Iterations: {len(iterations)}")
    print()

    if not iterations:
        print("[!!] NENHUMA Iteration configurada no Team!")
        print()
        print("PROBLEMA IDENTIFICADO:")
        print("  O Team nao tem Iterations selecionadas.")
        print()
        print("SOLUCAO:")
        print("  1. Acesse: https://dev.azure.com/IControlIT-v2/iControlIT%202.0/_settings/work-team")
        print("  2. Na secao 'Iterations', clique em 'Select iterations'")
        print("  3. Marque as Fases que devem aparecer nos Sprints")
        print("  4. Salve")
        sys.exit(1)

    # Analisar cada Iteration
    fases_desejadas = [
        "Fase-1-Sistema-Base",
        "Fase-2-Cadastros-e-Servicos-Transversais",
        "Fase-3-Financeiro-I-Base-Contabil",
        "Fase-4-Financeiro-II-Processos",
        "Fase-5-Service-Desk",
        "Fase-6-Ativos-Auditoria-Integracoes"
    ]

    fases_encontradas = []

    for iteration in iterations:
        name = iteration.get('name', 'N/A')
        path = iteration.get('path', 'N/A')
        iteration_id = iteration.get('id', 'N/A')
        url = iteration.get('url', 'N/A')

        attrs = iteration.get('attributes', {})
        start_date = attrs.get('startDate')
        finish_date = attrs.get('finishDate')
        time_frame = attrs.get('timeFrame', 'N/A')

        print(f"Iteration: {name}")
        print(f"  Path: {path}")
        print(f"  ID: {iteration_id}")

        if start_date and finish_date:
            print(f"  Periodo: {start_date[:10]} ate {finish_date[:10]}")
        else:
            print(f"  Periodo: SEM DATAS")

        print(f"  Time Frame: {time_frame}")
        print()

        if name in fases_desejadas:
            fases_encontradas.append(name)

    # Diagnostico
    print("="*70)
    print("DIAGNOSTICO")
    print("="*70)

    fases_faltando = [f for f in fases_desejadas if f not in fases_encontradas]

    print(f"Fases desejadas: {len(fases_desejadas)}")
    print(f"Fases configuradas no Team: {len(fases_encontradas)}")
    print(f"Fases faltando: {len(fases_faltando)}")
    print()

    if fases_faltando:
        print("[!!] PROBLEMA: Algumas Fases NAO estao configuradas no Team:")
        for fase in fases_faltando:
            print(f"  - {fase}")
        print()
        print("SOLUCAO:")
        print("  Execute: python configure-team-sprints.py")
    else:
        print("[OK] Todas as Fases estao configuradas no Team")
        print()
        print("Se Sprint Backlog ainda estiver vazio, verifique:")
        print("  1. Time Frame das Iterations (devem ser 'past', 'current' ou 'future')")
        print("  2. Se o Sprint Directory mostra as Fases")
        print("  3. Tente acessar via Sprint Directory:")
        print("     https://dev.azure.com/IControlIT-v2/iControlIT%202.0/_sprints/directory")

    print("="*70)

if __name__ == "__main__":
    main()
