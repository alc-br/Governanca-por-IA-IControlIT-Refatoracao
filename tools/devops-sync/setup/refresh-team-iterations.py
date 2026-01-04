#!/usr/bin/env python3
# Remove e re-adiciona Iterations no Team para forcar sincronizacao

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

def get_team_iterations(team_name):
    """Lista Iterations configuradas no Team"""
    project_encoded = urllib.parse.quote(PROJECT)
    team_encoded = urllib.parse.quote(team_name)

    url = f"{ORG_URL}/{project_encoded}/{team_encoded}/_apis/work/teamsettings/iterations?api-version=7.0"

    try:
        r = requests.get(url, headers=get_headers(), auth=get_auth())
        if r.status_code == 200:
            return r.json().get('value', [])
        return []
    except:
        return []

def delete_team_iteration(team_name, iteration_id):
    """Remove uma Iteration do Team"""
    project_encoded = urllib.parse.quote(PROJECT)
    team_encoded = urllib.parse.quote(team_name)

    url = f"{ORG_URL}/{project_encoded}/{team_encoded}/_apis/work/teamsettings/iterations/{iteration_id}?api-version=7.0"

    try:
        r = requests.delete(url, headers=get_headers(), auth=get_auth())
        return r.status_code == 204
    except:
        return False

def add_team_iteration(team_name, iteration_path):
    """Adiciona uma Iteration ao Team"""
    project_encoded = urllib.parse.quote(PROJECT)
    team_encoded = urllib.parse.quote(team_name)

    url = f"{ORG_URL}/{project_encoded}/{team_encoded}/_apis/work/teamsettings/iterations?api-version=7.0"

    payload = {
        "path": iteration_path
    }

    try:
        r = requests.post(url, json=payload, headers=get_headers(), auth=get_auth())
        return r.status_code in [200, 201]
    except:
        return False

def main():
    if not all([ORG_URL, PROJECT, TOKEN]):
        print("Variaveis de ambiente necessarias:")
        print("  AZDO_ORG_URL, AZDO_PROJECT, AZDO_PAT")
        sys.exit(1)

    print("="*70)
    print("REFRESH DE ITERATIONS NO TEAM")
    print("="*70)
    print("Este script ira REMOVER e RE-ADICIONAR as Iterations")
    print("para forcar a sincronizacao com o Azure DevOps.")
    print()

    # Obter Team
    team_id, team_name = get_team_id()
    if not team_id:
        print("[!!] Nao foi possivel obter o team ID")
        sys.exit(1)

    print(f"Team: {team_name}")
    print()

    # Listar Iterations atuais
    print("PASSO 1: Listando Iterations atuais")
    print("-"*70)

    iterations = get_team_iterations(team_name)
    print(f"Iterations encontradas: {len(iterations)}")

    fases_para_refresh = []

    for it in iterations:
        name = it.get('name', '')
        if name.startswith('Fase-'):
            fases_para_refresh.append({
                'id': it.get('id'),
                'name': name,
                'path': it.get('path')
            })
            print(f"  - {name}")

    if not fases_para_refresh:
        print("[!!] Nenhuma Fase encontrada para refresh")
        sys.exit(1)

    print()

    # Remover Iterations
    print("PASSO 2: Removendo Iterations temporariamente")
    print("-"*70)

    for fase in fases_para_refresh:
        print(f"Removendo: {fase['name']}...", end=' ')
        if delete_team_iteration(team_name, fase['id']):
            print("[OK]")
        else:
            print("[FALHOU]")

    print()

    # Aguardar
    print("Aguardando 3 segundos...")
    import time
    time.sleep(3)
    print()

    # Re-adicionar Iterations
    print("PASSO 3: Re-adicionando Iterations")
    print("-"*70)

    success_count = 0
    fail_count = 0

    for fase in fases_para_refresh:
        print(f"Adicionando: {fase['name']}...", end=' ')
        if add_team_iteration(team_name, fase['path']):
            print("[OK]")
            success_count += 1
        else:
            print("[FALHOU]")
            fail_count += 1

    print()
    print("="*70)
    print("RESUMO")
    print("="*70)
    print(f"Iterations re-adicionadas: {success_count}")
    print(f"Falhas: {fail_count}")
    print()

    if success_count > 0:
        print("PROXIMO PASSO:")
        print("  1. Aguarde 1-2 minutos")
        print("  2. Acesse o Sprint Directory:")
        print("     https://dev.azure.com/IControlIT-v2/iControlIT%202.0/_sprints/directory")
        print("  3. Clique em uma das Fases")
        print("  4. Verifique se os Work Items aparecem")

    print("="*70)

if __name__ == "__main__":
    main()
