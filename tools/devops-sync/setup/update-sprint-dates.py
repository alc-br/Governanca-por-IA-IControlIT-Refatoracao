#!/usr/bin/env python3
"""
Atualiza datas de sprints no Azure DevOps.

Uso:
    python update-sprint-dates.py direct
    python update-sprint-dates.py hierarchy
    python update-sprint-dates.py by-id <iteration_id>

Modos:
    direct      - Atualiza datas diretamente via API (mais rápido)
    hierarchy   - Atualiza respeitando hierarquia de iterações
    by-id       - Atualiza uma iteração específica por ID

Este script consolida a lógica dos 3 scripts antigos:
    - update-sprint-dates-direct.py
    - update-sprint-dates-hierarchy.py
    - update-sprint-dates-by-id.py
"""

import os
import sys
import requests
from datetime import datetime, timedelta
from base64 import b64encode

# Configurações Azure DevOps
ORGANIZATION = "icontrolit"
PROJECT = "IControlIT"
PAT = os.getenv("AZURE_DEVOPS_PAT")

if not PAT:
    print("❌ ERRO: Variável de ambiente AZURE_DEVOPS_PAT não configurada")
    sys.exit(1)

# Headers autenticação
AUTH_HEADER = b64encode(f":{PAT}".encode()).decode()
HEADERS = {
    "Authorization": f"Basic {AUTH_HEADER}",
    "Content-Type": "application/json"
}

BASE_URL = f"https://dev.azure.com/{ORGANIZATION}/{PROJECT}/_apis"


def get_iterations():
    """Obtém todas as iterações do projeto"""
    url = f"{BASE_URL}/work/teamsettings/iterations?api-version=7.1-preview.1"
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        print(f"❌ Erro ao obter iterações: {response.status_code}")
        print(response.text)
        return []

    return response.json().get("value", [])


def update_iteration_direct(iteration_id, start_date, finish_date):
    """Atualiza iteração diretamente via PATCH"""
    url = f"{BASE_URL}/work/teamsettings/iterations/{iteration_id}?api-version=7.1-preview.1"

    payload = {
        "attributes": {
            "startDate": start_date.isoformat(),
            "finishDate": finish_date.isoformat()
        }
    }

    response = requests.patch(url, json=payload, headers=HEADERS)

    if response.status_code in [200, 204]:
        print(f"✅ Iteração {iteration_id} atualizada: {start_date.date()} → {finish_date.date()}")
        return True
    else:
        print(f"❌ Erro ao atualizar iteração {iteration_id}: {response.status_code}")
        print(response.text)
        return False


def update_direct_mode():
    """Modo direto: atualiza todas as iterações sequencialmente"""
    print("\n🔧 Modo: Atualização Direta")
    print("=" * 60)

    iterations = get_iterations()

    if not iterations:
        print("❌ Nenhuma iteração encontrada")
        return

    print(f"📊 Total de iterações: {len(iterations)}\n")

    # Data base: hoje
    current_date = datetime.now()

    for i, iteration in enumerate(iterations, 1):
        name = iteration.get("name", "Sem nome")
        iteration_id = iteration.get("id")

        # Cada sprint = 2 semanas
        start_date = current_date + timedelta(weeks=(i-1) * 2)
        finish_date = start_date + timedelta(days=13)  # 14 dias (2 semanas)

        print(f"[{i}/{len(iterations)}] {name}")
        update_iteration_direct(iteration_id, start_date, finish_date)

    print("\n✅ Atualização direta concluída")


def update_hierarchy_mode():
    """Modo hierárquico: atualiza respeitando parent/child"""
    print("\n🔧 Modo: Atualização Hierárquica")
    print("=" * 60)

    iterations = get_iterations()

    if not iterations:
        print("❌ Nenhuma iteração encontrada")
        return

    # Agrupar por parent
    root_iterations = []
    child_iterations = {}

    for iteration in iterations:
        parent_id = iteration.get("parentId")
        if parent_id:
            if parent_id not in child_iterations:
                child_iterations[parent_id] = []
            child_iterations[parent_id].append(iteration)
        else:
            root_iterations.append(iteration)

    print(f"📊 Iterações raiz: {len(root_iterations)}")
    print(f"📊 Total de iterações: {len(iterations)}\n")

    current_date = datetime.now()

    def update_with_children(iteration, base_date, level=0):
        """Atualiza iteração e seus filhos recursivamente"""
        indent = "  " * level
        name = iteration.get("name", "Sem nome")
        iteration_id = iteration.get("id")

        # Definir datas
        start_date = base_date
        finish_date = base_date + timedelta(days=13)

        print(f"{indent}📅 {name}")
        update_iteration_direct(iteration_id, start_date, finish_date)

        # Atualizar filhos
        children = child_iterations.get(iteration_id, [])
        child_date = finish_date + timedelta(days=1)

        for child in children:
            child_date = update_with_children(child, child_date, level + 1)

        return finish_date + timedelta(days=1)

    # Processar cada árvore
    for root in root_iterations:
        current_date = update_with_children(root, current_date)

    print("\n✅ Atualização hierárquica concluída")


def update_by_id_mode(iteration_id):
    """Modo por ID: atualiza uma iteração específica"""
    print(f"\n🔧 Modo: Atualização por ID ({iteration_id})")
    print("=" * 60)

    # Data base: hoje
    start_date = datetime.now()
    finish_date = start_date + timedelta(days=13)

    success = update_iteration_direct(iteration_id, start_date, finish_date)

    if success:
        print("\n✅ Iteração atualizada com sucesso")
    else:
        print("\n❌ Falha ao atualizar iteração")


def main():
    """Ponto de entrada principal"""
    if len(sys.argv) < 2:
        print("❌ Uso: python update-sprint-dates.py [direct|hierarchy|by-id <id>]")
        sys.exit(1)

    mode = sys.argv[1].lower()

    if mode == "direct":
        update_direct_mode()
    elif mode == "hierarchy":
        update_hierarchy_mode()
    elif mode == "by-id":
        if len(sys.argv) < 3:
            print("❌ Uso: python update-sprint-dates.py by-id <iteration_id>")
            sys.exit(1)
        iteration_id = sys.argv[2]
        update_by_id_mode(iteration_id)
    else:
        print(f"❌ Modo inválido: {mode}")
        print("Modos disponíveis: direct, hierarchy, by-id")
        sys.exit(1)


if __name__ == "__main__":
    main()
