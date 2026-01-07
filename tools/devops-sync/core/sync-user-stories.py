#!/usr/bin/env python3
# Script para sincronizar user-stories.yaml com Azure DevOps
# Cria Work Items do tipo "User Story" e faz link com a Feature (RF) pai

import os
import sys
import yaml
import requests
from pathlib import Path

ORG_URL = os.getenv("AZDO_ORG_URL")
PROJECT = os.getenv("AZDO_PROJECT")
TOKEN = os.getenv("AZDO_PAT")

def get_auth():
    return ("", TOKEN)

def get_headers():
    return {
        "Content-Type": "application/json-patch+json",
        "Accept": "application/json"
    }

def find_user_stories_yaml(rf_code):
    """Encontra o arquivo user-stories.yaml para o RF especificado"""
    base_path = Path("D:/IC2/docs/rf")

    # Procurar recursivamente
    for yaml_file in base_path.rglob("user-stories.yaml"):
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                if data.get('rf_id') == documentacao_code:
                    return yaml_file, data
        except Exception as e:
            continue

    return None, None

def get_feature_work_item(feature_id):
    """Obtem informacoes da Feature (RF) pai"""
    url = f"{ORG_URL}/{PROJECT}/_apis/wit/workitems/{feature_id}?api-version=7.0"

    try:
        r = requests.get(url, headers=get_headers(), auth=get_auth())
        if r.status_code == 200:
            return r.json()
        return None
    except:
        return None

def create_user_story(parent_feature_id, story_data, documentacao_code):
    """Cria uma User Story no Azure DevOps"""
    url = f"{ORG_URL}/{PROJECT}/_apis/wit/workitems/$User Story?api-version=7.0"

    # Construir acceptance criteria formatado
    acceptance_criteria = "\n".join([f"- {criteria}" for criteria in story_data.get('acceptance_criteria', [])])

    # Construir description completa
    description = story_data.get('description', '')
    if story_data.get('technical_notes'):
        description += f"\n\n### Technical Notes\n{story_data['technical_notes']}"

    # Payload para criacao
    payload = [
        {
            "op": "add",
            "path": "/fields/System.Title",
            "value": f"{story_data['code']}: {story_data['title']}"
        },
        {
            "op": "add",
            "path": "/fields/System.Description",
            "value": description
        },
        {
            "op": "add",
            "path": "/fields/Microsoft.VSTS.Common.AcceptanceCriteria",
            "value": acceptance_criteria
        },
        {
            "op": "add",
            "path": "/fields/Microsoft.VSTS.Scheduling.StoryPoints",
            "value": story_data.get('story_points', 0)
        },
        {
            "op": "add",
            "path": "/fields/Microsoft.VSTS.Common.Priority",
            "value": 1 if story_data.get('priority') == 'Alta' else (2 if story_data.get('priority') == 'Media' else 3)
        },
        {
            "op": "add",
            "path": "/fields/System.Tags",
            "value": f"{rf_code};{story_data.get('module', '')}"
        }
    ]

    # Adicionar link com Feature pai
    if parent_feature_id:
        payload.append({
            "op": "add",
            "path": "/relations/-",
            "value": {
                "rel": "System.LinkTypes.Hierarchy-Reverse",
                "url": f"{ORG_URL}/{PROJECT}/_apis/wit/workitems/{parent_feature_id}"
            }
        })

    try:
        r = requests.post(url, json=payload, headers=get_headers(), auth=get_auth())

        if r.status_code in [200, 201]:
            work_item = r.json()
            return work_item['id'], work_item['fields']['System.Title']
        else:
            print(f"[ERRO] Falha ao criar User Story: {r.status_code}")
            print(f"Response: {r.text}")
            return None, None
    except Exception as e:
        print(f"[ERRO] Exception ao criar User Story: {str(e)}")
        return None, None

def update_user_stories_yaml(yaml_path, updated_data):
    """Atualiza o arquivo user-stories.yaml com IDs criados"""
    try:
        with open(yaml_path, 'w', encoding='utf-8') as f:
            yaml.dump(updated_data, f, allow_unicode=True, sort_keys=False, default_flow_style=False)
        return True
    except Exception as e:
        print(f"[ERRO] Falha ao atualizar YAML: {str(e)}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Uso: python sync-user-stories.py RFXXX")
        print("Exemplo: python sync-user-stories.py RF001")
        sys.exit(1)

    documentacao_code = sys.argv[1].upper()

    if not all([ORG_URL, PROJECT, TOKEN]):
        print("Variaveis de ambiente necessarias:")
        print("  AZDO_ORG_URL, AZDO_PROJECT, AZDO_PAT")
        sys.exit(1)

    print("="*70)
    print("SINCRONIZACAO DE USER STORIES COM AZURE DEVOPS")
    print("="*70)
    print(f"RF: {rf_code}")
    print(f"Org: {ORG_URL}")
    print(f"Project: {PROJECT}")
    print()

    # Encontrar arquivo user-stories.yaml
    print("PASSO 1: Localizando user-stories.yaml")
    print("-"*70)

    yaml_path, data = find_user_stories_yaml(rf_code)

    if not yaml_path:
        print(f"[ERRO] Arquivo user-stories.yaml nao encontrado para {rf_code}")
        sys.exit(1)

    print(f"Arquivo encontrado: {yaml_path}")
    print()

    # Verificar Feature pai
    print("PASSO 2: Verificando Feature pai")
    print("-"*70)

    feature_id = data.get('feature_work_item_id')

    if not feature_id:
        print("[AVISO] feature_work_item_id nao definido no YAML")
        print("As User Stories serao criadas SEM link com Feature pai")
        print()
    else:
        feature = get_feature_work_item(feature_id)
        if feature:
            print(f"Feature ID: {feature_id}")
            print(f"Feature Title: {feature['fields']['System.Title']}")
            print()
        else:
            print(f"[AVISO] Feature {feature_id} nao encontrada")
            feature_id = None
            print()

    # Criar User Stories
    print("PASSO 3: Criando User Stories")
    print("-"*70)

    user_stories = data.get('user_stories', [])
    created_count = 0
    skipped_count = 0
    failed_count = 0

    for story in user_stories:
        story_code = story.get('code', 'N/A')
        story_title = story.get('title', 'N/A')

        # Verificar se ja foi criada
        if story.get('id'):
            print(f"[SKIP] {story_code}: ja possui ID {story['id']}")
            skipped_count += 1
            continue

        print(f"Criando: {story_code} - {story_title}...", end=' ')

        work_item_id, work_item_title = create_user_story(feature_id, story, documentacao_code)

        if work_item_id:
            print(f"[OK] ID: {work_item_id}")
            story['id'] = work_item_id
            created_count += 1
        else:
            print("[FALHOU]")
            failed_count += 1

    print()

    # Atualizar YAML com IDs criados
    if created_count > 0:
        print("PASSO 4: Atualizando user-stories.yaml com IDs criados")
        print("-"*70)

        if update_user_stories_yaml(yaml_path, data):
            print(f"[OK] {yaml_path} atualizado")
        else:
            print(f"[ERRO] Falha ao atualizar {yaml_path}")
        print()

    # Resumo
    print("="*70)
    print("RESUMO")
    print("="*70)
    print(f"User Stories criadas: {created_count}")
    print(f"User Stories ja existentes: {skipped_count}")
    print(f"Falhas: {failed_count}")
    print()

    if created_count > 0:
        print("PROXIMO PASSO:")
        print("  1. Verifique as User Stories criadas no Azure DevOps")
        print("  2. Ajuste Iteration Paths se necessario")
        print("  3. Atribua para desenvolvedores")
        print()

    print("="*70)

if __name__ == "__main__":
    main()
