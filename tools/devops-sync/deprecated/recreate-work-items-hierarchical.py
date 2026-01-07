#!/usr/bin/env python3
# Recria Work Items no Azure DevOps com hierarquia correta:
# Area Path: iControlIT 2.0\NOME-DA-FASE
# EPIC (pai) > RFXXX (filho)

import os
import sys
import re
import glob
import requests
from datetime import datetime
from collections import defaultdict

# Configuracoes
ORG_URL = os.getenv("AZDO_ORG_URL")
PROJECT = os.getenv("AZDO_PROJECT")
TOKEN = os.getenv("AZDO_PAT")

def get_auth():
    return ("", TOKEN)

def get_headers():
    return {"Content-Type": "application/json-patch+json"}

# =====================================
# YAML PARSER
# =====================================
def parse_yaml_simple(content):
    """Parser YAML simplificado"""
    data = {}
    lines = content.split('\n')
    current_section = None
    current_subsection = None

    for line in lines:
        if line.strip().startswith('#') or not line.strip():
            continue

        if not line.startswith(' ') and ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            if value:
                if value.lower() == 'true':
                    data[key] = True
                elif value.lower() == 'false':
                    data[key] = False
                elif value.lower() == 'null':
                    data[key] = None
                else:
                    data[key] = value
            else:
                data[key] = {}
                current_section = key
                current_subsection = None

        elif line.startswith('  ') and not line.startswith('    ') and ':' in line:
            key, value = line.strip().split(':', 1)
            key = key.strip()
            value = value.strip()
            if current_section:
                if value:
                    if '#' in value:
                        value = value.split('#')[0].strip()
                    if value.lower() == 'true':
                        data[current_section][key] = True
                    elif value.lower() == 'false':
                        data[current_section][key] = False
                    elif value.lower() == 'null':
                        data[current_section][key] = None
                    else:
                        data[current_section][key] = value
                else:
                    data[current_section][key] = {}
                    current_subsection = key

        elif line.startswith('    ') and ':' in line:
            key, value = line.strip().split(':', 1)
            key = key.strip()
            value = value.strip()
            if current_section and current_subsection:
                if '#' in value:
                    value = value.split('#')[0].strip()
                if value.lower() == 'true':
                    data[current_section][current_subsection][key] = True
                elif value.lower() == 'false':
                    data[current_section][current_subsection][key] = False
                elif value.lower() == 'null':
                    data[current_section][current_subsection][key] = None
                else:
                    data[current_section][current_subsection][key] = value

    return data

def load_all_status_files():
    """Carrega todos os STATUS.yaml e organiza por Fase e EPIC"""
    pattern = "D:/IC2/docs/documentacao/**/STATUS.yaml"
    files = glob.glob(pattern, recursive=True)

    # Estrutura: {fase: {epic: [rfs]}}
    structure = defaultdict(lambda: defaultdict(list))

    for f in files:
        try:
            with open(f, 'r', encoding='utf-8') as file:
                content = file.read()

            data = parse_yaml_simple(content)

            if data and 'rf' in data:
                documentacao_raw = str(data['rf']).replace('RF', '').replace('RF-', '').zfill(3)
                documentacao_id = f"RF-{rf_raw}"

                fase = data.get('fase', 'UNKNOWN')
                epic = data.get('epic', 'UNKNOWN')
                titulo = data.get('titulo', 'Sem titulo')

                # Extrair nome completo da Fase do caminho
                fase_nome = extract_fase_nome_from_path(f, fase)
                epic_nome = extract_epic_nome_from_path(f, epic)

                structure[fase]['_nome'] = fase_nome
                structure[fase][epic].append({
                    'rf_id': documentacao_id,
                    'titulo': titulo,
                    'data': data,
                    'file_path': f,
                    'epic_nome': epic_nome
                })
        except Exception as e:
            print(f"[!!] Erro ao ler {f}: {e}")

    return structure

def extract_fase_nome_from_path(file_path, fase_code):
    """Extrai nome completo da Fase do caminho"""
    # Exemplo:  D:\IC2\documentacao\Fase-1-Fundacao-e-Cadastros-Base\...
    parts = file_path.replace('\\', '/').split('/')

    for part in parts:
        if part.startswith(fase_code):
            return part

    return fase_code

def extract_epic_nome_from_path(file_path, epic_code):
    """Extrai nome completo do EPIC do caminho"""
    # Exemplo: EPIC001-SYS-Sistema-Infraestrutura
    parts = file_path.replace('\\', '/').split('/')

    for part in parts:
        if part.startswith(epic_code):
            return part

    return epic_code

def create_epic_work_item(epic_code, epic_nome, area_path):
    """Cria Work Item Epic"""
    url = f"{ORG_URL}/{PROJECT}/_apis/wit/workitems/$Epic?api-version=7.0"

    # Titulo do EPIC
    title = epic_nome

    payload = [
        {"op": "add", "path": "/fields/System.Title", "value": title},
        {"op": "add", "path": "/fields/System.AreaPath", "value": area_path},
        {"op": "add", "path": "/fields/System.State", "value": "New"}
    ]

    try:
        r = requests.post(url, json=payload, headers=get_headers(), auth=get_auth())

        if r.status_code == 200:
            work_item = r.json()
            return work_item['id']
        else:
            print(f"[!!] Erro ao criar EPIC {epic_code}: {r.status_code}")
            print(f"     Resposta: {r.text[:500]}")
            return None
    except Exception as e:
        print(f"[!!] Excecao ao criar EPIC {epic_code}: {e}")
        return None

def create_rf_work_item(rf_id, titulo, area_path, parent_epic_id, documentacao_data):
    """Cria Work Item Feature (RF) como filho do EPIC"""
    url = f"{ORG_URL}/{PROJECT}/_apis/wit/workitems/$Feature?api-version=7.0"

    title = f"{rf_id} - {titulo}"

    # Gerar description inicial
    description = generate_description(rf_data)

    payload = [
        {"op": "add", "path": "/fields/System.Title", "value": title},
        {"op": "add", "path": "/fields/System.AreaPath", "value": area_path},
        {"op": "add", "path": "/fields/System.State", "value": "New"},
        {"op": "add", "path": "/fields/System.Description", "value": description}
    ]

    # Adicionar Parent Link (RF filho do EPIC)
    if parent_epic_id:
        payload.append({
            "op": "add",
            "path": "/relations/-",
            "value": {
                "rel": "System.LinkTypes.Hierarchy-Reverse",
                "url": f"{ORG_URL}/_apis/wit/workitems/{parent_epic_id}"
            }
        })

    try:
        r = requests.post(url, json=payload, headers=get_headers(), auth=get_auth())

        if r.status_code == 200:
            work_item = r.json()
            return work_item['id']
        else:
            print(f"[!!] Erro ao criar RF {rf_id}: {r.status_code}")
            print(f"     Resposta: {r.text[:500]}")
            return None
    except Exception as e:
        print(f"[!!] Excecao ao criar RF {rf_id}: {e}")
        return None

def generate_description(rf_data):
    """Gera HTML description padronizado"""
    data = documentacao_data.get('data', {})

    # Status desenvolvimento
    dev = data.get('desenvolvimento', {})
    backend_status = dev.get('backend', {}).get('status', 'not_started')
    frontend_status = dev.get('frontend', {}).get('status', 'not_started')

    def get_icon(status):
        if status == 'done':
            return '✅'
        elif status == 'in_progress':
            return '🟡'
        else:
            return '⬜'

    def format_status(status):
        return status.replace('_', ' ').title()

    # Documentacao
    docs = data.get('documentacao', {})
    documentacao_icon = '✅' if docs.get('rf') else '⬜'
    uc_icon = '✅' if docs.get('uc') else '⬜'
    md_icon = '✅' if docs.get('md') else '⬜'
    wf_icon = '✅' if docs.get('wf') else '⬜'

    # Board info
    board_column = data.get('devops', {}).get('board_column', 'Backlog')
    state = 'New'
    now = datetime.now().strftime('%Y-%m-%d %H:%M')

    html = f"""
<h2>📊 Status de Desenvolvimento</h2>
<table border="1" cellpadding="8" style="border-collapse: collapse;">
<tr style="background-color: #e0e0e0;"><th>Camada</th><th>Status</th></tr>
<tr><td><b>Backend</b></td><td>{get_icon(backend_status)} {format_status(backend_status)}</td></tr>
<tr><td><b>Frontend</b></td><td>{get_icon(frontend_status)} {format_status(frontend_status)}</td></tr>
</table>

<h2>📄 Documentacao</h2>
<table border="1" cellpadding="8" style="border-collapse: collapse;">
<tr><td>{rf_icon} RF.md</td><td>{uc_icon} UC.md</td><td>{md_icon} MD.md</td><td>{wf_icon} WF.md</td></tr>
</table>

<h2>🔄 Board</h2>
<table border="1" cellpadding="8" style="border-collapse: collapse;">
<tr><td><b>Coluna</b></td><td>{board_column}</td></tr>
<tr><td><b>State</b></td><td>{state}</td></tr>
<tr><td><b>Ultima Sync</b></td><td>{now}</td></tr>
</table>
"""
    return html

def update_status_yaml(file_path, work_item_id):
    """Atualiza STATUS.yaml com work_item_id"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Atualizar work_item_id
        if 'work_item_id: null' in content or 'work_item_id:' not in content:
            content = re.sub(r'work_item_id:.*', f'work_item_id: {work_item_id}', content)
        else:
            content = re.sub(r'work_item_id: \d+', f'work_item_id: {work_item_id}', content)

        # Atualizar last_sync
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if 'last_sync:' in content:
            content = re.sub(r'last_sync:.*', f'last_sync: "{now}"', content)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return True
    except Exception as e:
        print(f"[!!] Erro ao atualizar {file_path}: {e}")
        return False

def main():
    if not all([ORG_URL, PROJECT, TOKEN]):
        print("=" * 80)
        print("RECRIACAO HIERARQUICA - VARIAVEIS NAO CONFIGURADAS")
        print("=" * 80)
        print("\nDefina: AZDO_ORG_URL, AZDO_PROJECT, AZDO_PAT")
        print("=" * 80)
        sys.exit(1)

    print("=" * 80)
    print("RECRIACAO HIERARQUICA DE WORK ITEMS")
    print("Estrutura: Area Path > EPIC > RFs")
    print("=" * 80)
    print(f"Org: {ORG_URL}")
    print(f"Project: {PROJECT}")
    print(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Carregar estrutura
    print("[>] Carregando STATUS.yaml files...")
    structure = load_all_status_files()

    total_fases = len(structure)
    total_epics = sum(len([k for k in v.keys() if k != '_nome']) for v in structure.values())
    total_rfs = sum(len(rfs) for fase_data in structure.values() for epic, rfs in fase_data.items() if epic != '_nome')

    print(f"[>] Estrutura identificada:")
    print(f"    Fases: {total_fases}")
    print(f"    EPICs: {total_epics}")
    print(f"    RFs: {total_rfs}")
    print()

    # Criar Work Items
    print("[>] Criando Work Items...")
    print()

    epics_created = 0
    rfs_created = 0
    errors = 0

    epic_ids = {}  # {epic_code: work_item_id}

    for fase_code, fase_data in sorted(structure.items()):
        fase_nome = fase_data.get('_nome', fase_code)
        # Usar Area Path da Fase
        area_path = f"{PROJECT}\\{fase_nome}"

        print(f"\n{'='*70}")
        print(f"FASE: {fase_nome}")
        print(f"Area Path: {area_path}")
        print(f"{'='*70}")

        for epic, rfs in sorted(fase_data.items()):
            if epic == '_nome':
                continue

            epic_nome = rfs[0]['epic_nome'] if rfs else epic

            # Criar EPIC
            print(f"\n[+] Criando EPIC: {epic_nome}")
            epic_id = create_epic_work_item(epic, epic_nome, area_path)

            if epic_id:
                print(f"    [OK] EPIC criado: ID {epic_id}")
                epic_ids[epic] = epic_id
                epics_created += 1

                # Criar RFs filhos
                for documentacao_info in sorted(rfs, key=lambda x: x['rf_id']):
                    documentacao_id = documentacao_info['rf_id']
                    titulo = documentacao_info['titulo']

                    print(f"    [+] Criando RF: {rf_id}")
                    documentacao_wi_id = create_rf_work_item(
                        documentacao_id, titulo, area_path, epic_id, documentacao_info
                    )

                    if documentacao_wi_id:
                        print(f"        [OK] RF criado: ID {rf_wi_id}")
                        rfs_created += 1

                        # Atualizar STATUS.yaml
                        update_status_yaml(rf_info['file_path'], documentacao_wi_id)
                    else:
                        errors += 1
            else:
                print(f"    [!!] Falha ao criar EPIC")
                errors += 1

    # Resumo
    print("\n" + "=" * 80)
    print("RESUMO DA RECRIACAO")
    print("=" * 80)
    print(f"EPICs criados: {epics_created}")
    print(f"RFs criados: {rfs_created}")
    print(f"Erros: {errors}")
    print("=" * 80)

    return 0 if errors == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
