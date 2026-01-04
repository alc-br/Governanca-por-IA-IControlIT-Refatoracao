#!/usr/bin/env python3
# Verifica diretamente os classification nodes para ver as datas

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

def get_iteration_node(iteration_name):
    """Busca um classification node especifico"""
    iteration_encoded = urllib.parse.quote(iteration_name)
    url = f"{ORG_URL}/{PROJECT}/_apis/wit/classificationnodes/iterations/{iteration_encoded}?api-version=7.0"

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
        print("  AZDO_ORG_URL, AZDO_PROJECT, AZDO_PAT")
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
    print("VERIFICACAO DIRETA DOS CLASSIFICATION NODES")
    print("="*70)
    print()

    for fase in fases:
        node = get_iteration_node(fase)

        print(f"Fase: {fase}")

        if node:
            attrs = node.get('attributes', {})
            path = node.get('path', 'N/A')
            start = attrs.get('startDate', 'NAO DEFINIDA')
            finish = attrs.get('finishDate', 'NAO DEFINIDA')

            print(f"  Path completo: {path}")
            print(f"  Inicio: {start}")
            print(f"  Termino: {finish}")

            if start != 'NAO DEFINIDA' and finish != 'NAO DEFINIDA':
                print(f"  [OK] Datas configuradas!")
            else:
                print(f"  [!!] SEM datas")
        else:
            print(f"  [!!] NAO ENCONTRADO ou erro")

        print()

    print("="*70)

if __name__ == "__main__":
    main()
