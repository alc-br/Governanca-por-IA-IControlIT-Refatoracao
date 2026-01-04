#!/usr/bin/env python3
# Verifica quais Iteration Paths estao configurados no Team Settings

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

def list_all_iteration_paths():
    """Lista todos os Iteration Paths do projeto"""
    url = f"{ORG_URL}/{PROJECT}/_apis/wit/classificationnodes/iterations?$depth=2&api-version=7.0"

    try:
        r = requests.get(url, headers=get_headers(), auth=get_auth())
        if r.status_code == 200:
            data = r.json()
            iterations = data.get('children', [])
            return iterations
        else:
            print(f"[!!] Erro ao listar Iteration Paths: {r.status_code}")
            return []
    except Exception as e:
        print(f"[!!] Excecao: {e}")
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
        print(f"[!!] Erro ao obter team: {e}")
        return None, None

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
            print(f"[!!] Erro ao obter team iterations: {r.status_code}")
            print(f"     Response: {r.text[:500]}")
            return []
    except Exception as e:
        print(f"[!!] Excecao ao obter team iterations: {e}")
        return []

def main():
    if not all([ORG_URL, PROJECT, TOKEN]):
        print("Variaveis de ambiente necessarias:")
        print("  AZDO_ORG_URL - URL da organizacao")
        print("  AZDO_PROJECT - Nome do projeto")
        print("  AZDO_PAT     - Personal Access Token")
        sys.exit(1)

    print("="*70)
    print("VERIFICACAO DE SPRINTS NO TEAM")
    print("="*70)
    print(f"Org: {ORG_URL}")
    print(f"Project: {PROJECT}")
    print()

    # Passo 1: Listar todos os Iteration Paths do projeto
    print("PASSO 1: Iteration Paths existentes no projeto")
    print("-"*70)

    all_iterations = list_all_iteration_paths()
    print(f"[INFO] Total de Iteration Paths criados: {len(all_iterations)}")

    iteration_names = []
    for it in all_iterations:
        name = it.get('name')
        path = it.get('path')
        start = it.get('attributes', {}).get('startDate', 'N/A')
        finish = it.get('attributes', {}).get('finishDate', 'N/A')

        iteration_names.append(name)
        print(f"  - {name}")
        print(f"    Path: {path}")
        print(f"    Periodo: {start} ate {finish}")
    print()

    # Passo 2: Obter Team ID
    print("PASSO 2: Informacoes do Team")
    print("-"*70)

    team_id, team_name = get_team_id()
    if not team_id:
        print("[!!] Nao foi possivel obter o team ID")
        sys.exit(1)

    print(f"[INFO] Team: {team_name}")
    print(f"[INFO] Team ID: {team_id}")
    print()

    # Passo 3: Listar Iterations configuradas no Team
    print("PASSO 3: Iteration Paths configurados no Team Settings")
    print("-"*70)

    team_iterations = get_team_iterations(team_name)
    print(f"[INFO] Total de Iterations configurados no Team: {len(team_iterations)}")

    configured_names = []
    if team_iterations:
        for it in team_iterations:
            name = it.get('name')
            path = it.get('path')
            configured_names.append(name)
            print(f"  - {name}")
            print(f"    Path: {path}")
    else:
        print("  [!!] NENHUMA Iteration configurada no Team!")
    print()

    # Passo 4: Comparacao
    print("="*70)
    print("DIAGNOSTICO")
    print("="*70)

    missing = [name for name in iteration_names if name not in configured_names]

    if missing:
        print(f"[!!] {len(missing)} Iteration Paths NAO CONFIGURADOS no Team:")
        for name in missing:
            print(f"     - {name}")
        print()
        print("CAUSA RAIZ IDENTIFICADA:")
        print("  Os Iteration Paths existem no projeto,")
        print("  mas NAO estao configurados no Team Settings.")
        print("  Por isso, os Sprint Backlogs aparecem vazios.")
        print()
        print("="*70)
        print("SOLUCAO MANUAL")
        print("="*70)
        print("1. Acesse:")
        print(f"   https://dev.azure.com/IControlIT-v2/{urllib.parse.quote(PROJECT)}/_settings/work-team")
        print()
        print("2. Na secao 'Iterations', clique em '+ Select iteration(s)'")
        print()
        print("3. Marque as seguintes Iterations:")
        for name in missing:
            print(f"   [ ] {name}")
        print()
        print("4. Clique em 'Save and close'")
        print()
        print("5. Apos salvar, os Sprint Backlogs vao exibir os Work Items")
        print("="*70)
    else:
        print("[OK] Todas as Iterations estao configuradas no Team!")
        print()
        print("Se os Sprint Backlogs ainda estiverem vazios,")
        print("o problema pode ser de cache do navegador.")
        print("Tente:")
        print("  - Atualizar a pagina (Ctrl+F5)")
        print("  - Limpar cache do navegador")
        print("  - Abrir em aba anonima")
        print("="*70)

if __name__ == "__main__":
    main()
