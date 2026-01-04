#!/usr/bin/env python3
# Configura os Iteration Paths no Team para aparecerem no Sprints Directory

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

def list_iteration_paths():
    """Lista todos os Iteration Paths do projeto"""
    url = f"{ORG_URL}/{PROJECT}/_apis/wit/classificationnodes/iterations?$depth=2&api-version=7.0"

    try:
        r = requests.get(url, headers=get_headers(), auth=get_auth())
        if r.status_code == 200:
            data = r.json()
            return data
        else:
            print(f"[!!] Erro ao listar Iteration Paths: {r.status_code}")
            return None
    except Exception as e:
        print(f"[!!] Excecao: {e}")
        return None

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
        print(f"[!!] Erro ao obter team: {e}")
        return None, None

def configure_team_iterations(team_id, team_name, iterations):
    """Configura os Iteration Paths no Team"""
    project_encoded = urllib.parse.quote(PROJECT)
    team_encoded = urllib.parse.quote(team_name)

    url = f"{ORG_URL}/{project_encoded}/{team_encoded}/_apis/work/teamsettings/iterations?api-version=7.0"

    success_count = 0
    fail_count = 0

    for iteration in iterations:
        iteration_id = iteration.get('identifier')  # Changed from 'id' to 'identifier'
        iteration_name = iteration.get('name')
        iteration_path = iteration.get('path')

        # Try with path instead of id
        payload = {
            "path": iteration_path
        }

        try:
            r = requests.post(url, json=payload, headers=get_headers(), auth=get_auth())

            if r.status_code in [200, 201]:
                print(f"[OK] Iteration configurada: {iteration_name}")
                success_count += 1
            elif r.status_code == 409:
                print(f"[>>] Iteration ja configurada: {iteration_name}")
                success_count += 1
            else:
                print(f"[!!] Erro ao configurar {iteration_name}: {r.status_code}")
                print(f"     Response: {r.text[:200]}")
                fail_count += 1
        except Exception as e:
            print(f"[!!] Excecao ao configurar {iteration_name}: {e}")
            fail_count += 1

    return success_count, fail_count

def main():
    if not all([ORG_URL, PROJECT, TOKEN]):
        print("Variaveis de ambiente necessarias:")
        print("  AZDO_ORG_URL - URL da organizacao")
        print("  AZDO_PROJECT - Nome do projeto")
        print("  AZDO_PAT     - Personal Access Token")
        sys.exit(1)

    print("="*70)
    print("CONFIGURACAO DE SPRINTS NO TEAM")
    print("="*70)
    print(f"Org: {ORG_URL}")
    print(f"Project: {PROJECT}")
    print()

    # Passo 1: Listar Iteration Paths
    print("PASSO 1: Listando Iteration Paths existentes")
    print("-"*70)

    iteration_data = list_iteration_paths()
    if not iteration_data:
        print("[!!] Nenhum Iteration Path encontrado")
        sys.exit(1)

    iterations = iteration_data.get('children', [])
    print(f"[INFO] Encontrados {len(iterations)} Iteration Paths:")
    for it in iterations:
        print(f"  - {it.get('name')}")
    print()

    # Passo 2: Obter Team ID
    print("PASSO 2: Obtendo informacoes do Team")
    print("-"*70)

    team_id, team_name = get_team_id()
    if not team_id:
        print("[!!] Nao foi possivel obter o team ID")
        sys.exit(1)

    print(f"[INFO] Team: {team_name}")
    print(f"[INFO] Team ID: {team_id}")
    print()

    # Passo 3: Configurar Iterations no Team
    print("PASSO 3: Configurando Iteration Paths no Team")
    print("-"*70)

    success_count, fail_count = configure_team_iterations(team_id, team_name, iterations)

    print()
    print("="*70)
    print("RESUMO")
    print("="*70)
    print(f"Iterations configuradas: {success_count}")
    print(f"Falhas: {fail_count}")
    print()
    print("Acesse: https://dev.azure.com/IControlIT-v2/iControlIT%202.0/_sprints/directory")
    print("="*70)

if __name__ == "__main__":
    main()
