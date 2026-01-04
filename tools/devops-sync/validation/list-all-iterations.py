#!/usr/bin/env python3
# Lista TODA a arvore de Iteration Paths

import os
import sys
import requests
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

def list_iterations_tree():
    """Lista toda a arvore de Iteration Paths"""
    url = f"{ORG_URL}/{PROJECT}/_apis/wit/classificationnodes/iterations?$depth=10&api-version=7.0"

    try:
        r = requests.get(url, headers=get_headers(), auth=get_auth())
        if r.status_code == 200:
            return r.json()
        else:
            print(f"[!!] Erro: {r.status_code}")
            return None
    except Exception as e:
        print(f"[!!] Excecao: {e}")
        return None

def print_iteration_node(node, indent=0):
    """Imprime um no da arvore recursivamente"""
    name = node.get('name', 'N/A')
    path = node.get('path', 'N/A')
    attrs = node.get('attributes', {})
    start = attrs.get('startDate', 'SEM DATA')
    finish = attrs.get('finishDate', 'SEM DATA')

    prefix = "  " * indent

    print(f"{prefix}- {name}")
    print(f"{prefix}  Path: {path}")

    if start != 'SEM DATA' and finish != 'SEM DATA':
        print(f"{prefix}  Periodo: {start[:10]} ate {finish[:10]} [OK]")
    else:
        print(f"{prefix}  Periodo: SEM DATAS [!!]")

    # Processar filhos
    children = node.get('children', [])
    if children:
        for child in children:
            print_iteration_node(child, indent + 1)

def main():
    if not all([ORG_URL, PROJECT, TOKEN]):
        print("Variaveis de ambiente necessarias:")
        print("  AZDO_ORG_URL, AZDO_PROJECT, AZDO_PAT")
        sys.exit(1)

    print("="*70)
    print("ARVORE COMPLETA DE ITERATION PATHS")
    print("="*70)
    print()

    tree = list_iterations_tree()

    if tree:
        print_iteration_node(tree)
    else:
        print("[!!] Nao foi possivel obter a arvore de Iteration Paths")

    print()
    print("="*70)

if __name__ == "__main__":
    main()
