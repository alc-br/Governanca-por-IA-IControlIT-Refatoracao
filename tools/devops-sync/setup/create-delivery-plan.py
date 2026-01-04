#!/usr/bin/env python3
# Cria um Delivery Plan para as Fases do projeto

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

def get_team_id():
    """Obtem o ID do team principal"""
    url = f"{ORG_URL}/_apis/projects/{PROJECT}/teams?api-version=7.0"

    try:
        r = requests.get(url, headers=get_headers(), auth=get_auth())
        if r.status_code == 200:
            teams = r.json().get('value', [])
            if teams:
                # Pegar o team principal (geralmente o primeiro)
                team = teams[0]
                print(f"[INFO] Team encontrado: {team.get('name')}")
                return team.get('id')
        return None
    except Exception as e:
        print(f"[!!] Erro ao obter team: {e}")
        return None

def create_delivery_plan():
    """Cria um Delivery Plan"""
    team_id = get_team_id()
    if not team_id:
        print("[!!] Nao foi possivel obter o team ID")
        return False

    # URL para criar Delivery Plan
    url = f"{ORG_URL}/{PROJECT}/_apis/work/plans?api-version=7.0"

    # Payload do Delivery Plan com properties minimas necessarias
    properties = {
        "criteriaStatus": {
            "type": "WorkItemTracking",
            "value": "[]"
        },
        "teams": json.dumps([{
            "teamId": team_id,
            "backlogIteration": None,
            "iterations": []
        }]),
        "markers": json.dumps([])
    }

    payload = {
        "name": "Roadmap de Entrega - 2025",
        "description": "Planejamento de entrega das Fases 3, 4, 5 e 6 do projeto iControlIT 2.0",
        "type": "DeliveryTimelineView",
        "properties": properties
    }

    try:
        r = requests.post(url, json=payload, headers=get_headers(), auth=get_auth())

        if r.status_code in [200, 201]:
            plan_data = r.json()
            plan_id = plan_data.get('id')
            print(f"[OK] Delivery Plan criado com sucesso!")
            print(f"     ID: {plan_id}")
            print(f"     Nome: {payload['name']}")
            print(f"     URL: {ORG_URL}/{PROJECT}/_deliveryplans/plans/{plan_id}")
            return True
        else:
            print(f"[!!] Erro ao criar Delivery Plan: {r.status_code}")
            print(f"     Resposta: {r.text[:1000]}")
            return False
    except Exception as e:
        print(f"[!!] Excecao ao criar Delivery Plan: {e}")
        return False

def list_existing_plans():
    """Lista os Delivery Plans existentes"""
    url = f"{ORG_URL}/{PROJECT}/_apis/work/plans?api-version=7.0"

    try:
        r = requests.get(url, headers=get_headers(), auth=get_auth())
        if r.status_code == 200:
            plans = r.json().get('value', [])
            if plans:
                print("\n[INFO] Delivery Plans existentes:")
                for plan in plans:
                    print(f"  - {plan.get('name')} (ID: {plan.get('id')})")
                    print(f"    URL: {ORG_URL}/{PROJECT}/_deliveryplans/plans/{plan.get('id')}")
                return True
            else:
                print("\n[INFO] Nenhum Delivery Plan encontrado")
                return False
        else:
            print(f"[!!] Erro ao listar Delivery Plans: {r.status_code}")
            return False
    except Exception as e:
        print(f"[!!] Erro ao listar plans: {e}")
        return False

def main():
    if not all([ORG_URL, PROJECT, TOKEN]):
        print("Variaveis de ambiente necessarias:")
        print("  AZDO_ORG_URL - URL da organizacao (ex: https://dev.azure.com/org)")
        print("  AZDO_PROJECT - Nome do projeto")
        print("  AZDO_PAT     - Personal Access Token")
        sys.exit(1)

    print("="*70)
    print("CRIACAO DE DELIVERY PLAN")
    print("="*70)
    print(f"Org: {ORG_URL}")
    print(f"Project: {PROJECT}")
    print()

    # Listar plans existentes
    list_existing_plans()
    print()

    # Criar novo plan
    print("Criando novo Delivery Plan...")
    create_delivery_plan()

    print("\n" + "="*70)
    print("PROXIMO PASSO:")
    print("="*70)
    print("1. Acesse o Delivery Plan criado no Azure DevOps")
    print("2. Configure as Iterations (Sprints) manualmente:")
    print("   - Fase-3-Financeiro-I-Base-Contabil (27/12/2024 - 31/01/2025)")
    print("   - Fase-4-Financeiro-II-Processos (01/02/2025 - 28/02/2025)")
    print("   - Fase-5-Service-Desk (01/03/2025 - 31/03/2025)")
    print("   - Fase-6-Ativos-Auditoria-Integracoes (01/04/2025 - 30/04/2025)")
    print("="*70)

if __name__ == "__main__":
    main()
