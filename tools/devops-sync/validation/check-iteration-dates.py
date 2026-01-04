#!/usr/bin/env python3
# Verifica as datas dos Iteration Paths especificos das Fases

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

def get_iteration_details(iteration_name):
    """Busca detalhes de um Iteration Path especifico"""
    url = f"{ORG_URL}/{PROJECT}/_apis/wit/classificationnodes/iterations/{iteration_name}?api-version=7.0"

    try:
        r = requests.get(url, auth=get_auth())
        if r.status_code == 200:
            return r.json()
        else:
            return None
    except Exception as e:
        return None

def main():
    if not all([ORG_URL, PROJECT, TOKEN]):
        print("Variaveis de ambiente necessarias:")
        print("  AZDO_ORG_URL - URL da organizacao")
        print("  AZDO_PROJECT - Nome do projeto")
        print("  AZDO_PAT     - Personal Access Token")
        sys.exit(1)

    fases = [
        "Fase-1-Sistema-Base",
        "Fase-2-Cadastros-e-Servicos-Transversais",
        "Fase-3-Financeiro-I-Base-Contabil",
        "Fase-4-Financeiro-II-Processos",
        "Fase-5-Service-Desk",
        "Fase-6-Ativos-Auditoria-Integracoes"
    ]

    print("="*70)
    print("VERIFICACAO DE DATAS DOS ITERATION PATHS DAS FASES")
    print("="*70)
    print()

    for fase in fases:
        iteration = get_iteration_details(fase)

        if iteration:
            attrs = iteration.get('attributes', {})
            start = attrs.get('startDate', 'NAO DEFINIDA')
            finish = attrs.get('finishDate', 'NAO DEFINIDA')
            path = iteration.get('path', 'N/A')

            print(f"Fase: {fase}")
            print(f"  Path: {path}")
            print(f"  Inicio: {start}")
            print(f"  Termino: {finish}")
            print()
        else:
            print(f"Fase: {fase}")
            print(f"  [!!] NAO ENCONTRADA ou erro ao buscar")
            print()

    print("="*70)
    print("DIAGNOSTICO")
    print("="*70)
    print()
    print("Se as datas estiverem como 'NAO DEFINIDA',")
    print("e necessario atualiza-las usando o script:")
    print("  python assign-items-to-sprints.py")
    print()
    print("="*70)

if __name__ == "__main__":
    main()
