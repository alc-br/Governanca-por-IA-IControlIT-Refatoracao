#!/usr/bin/env python3
"""
Cria Work Items no Azure DevOps para RFs que ainda nao possuem
Complementa sync-all-rfs.py (que apenas atualiza Work Items existentes)

Conforme solicitacao do usuario: criar Work Items vazios apenas com nome
para que RFs aparecam no Board do Azure DevOps mesmo sem documentacao
"""

import os
import sys
import re
import glob
import requests
from datetime import datetime

# =====================================
# CONFIGURACOES
# =====================================
ORG_URL = os.getenv("AZDO_ORG_URL")
PROJECT = os.getenv("AZDO_PROJECT")
TOKEN = os.getenv("AZDO_PAT")
STATUS_PATH = os.getenv("STATUS_PATH", "D:/IC2/docs/rf")

# Mapeamento de Fase -> Area Path
FASE_TO_AREA = {
    "Fase-1": "IControlIT\\Fase-1-Fundacao-e-Cadastros-Base",
    "Fase-2": "IControlIT\\Fase-2-Gestao-Operacional",
    "Fase-3": "IControlIT\\Fase-3-Gestao-Avancada",
    "Fase-4": "IControlIT\\Fase-4-Auditoria-Governanca",
    "Fase-5": "IControlIT\\Fase-5-Financeiro-Auditoria-e-BI",
}

# =====================================
# HELPERS
# =====================================
def fail(msg):
    print(f"\n[ERRO] {msg}\n")

def ok(msg):
    print(f"[OK] {msg}")

def info(msg):
    print(f"[INFO] {msg}")

def warn(msg):
    print(f"[WARN] {msg}")

def get_auth():
    return ("", TOKEN)

def get_headers():
    return {"Content-Type": "application/json-patch+json"}

# =====================================
# YAML PARSER SIMPLES
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
    """Carrega todos os STATUS.yaml"""
    # Processar apenas docs/rf
    patterns = [
        "D:/IC2/docs/rf/**/STATUS.yaml"
    ]

    statuses = {}
    for pattern in patterns:
        files = glob.glob(pattern, recursive=True)

        for f in files:
            try:
                with open(f, 'r', encoding='utf-8') as file:
                    content = file.read()

                data = parse_yaml_simple(content)

                if data and 'rf' in data:
                    rf_raw = str(data['rf']).replace('RF', '').replace('RF-', '').zfill(3)
                    rf_id = f"RF-{rf_raw}"
                    statuses[rf_id] = {
                        'file_path': f,
                        'data': data
                    }
            except Exception as e:
                warn(f"Erro ao ler {f}: {e}")

    return statuses

def extract_fase_from_path(file_path):
    """Extrai codigo da Fase a partir do caminho do arquivo"""
    # Exemplo: D:\IC2\docs\rf\Fase-1-Fundacao-e-Cadastros-Base\...
    parts = file_path.replace('\\', '/').split('/')

    for part in parts:
        if part.startswith('Fase-'):
            # Extrair apenas "Fase-X"
            match = re.match(r'(Fase-\d+)', part)
            if match:
                return match.group(1)

    return None

def extract_area_path(file_path, fase_code):
    """Retorna Area Path baseado na Fase"""
    if fase_code in FASE_TO_AREA:
        return FASE_TO_AREA[fase_code]
    return "IControlIT"  # Default

def create_work_item(rf_id, titulo, area_path, epic_code=None):
    """Cria Work Item Feature no Azure DevOps"""
    url = f"{ORG_URL}/{PROJECT}/_apis/wit/workitems/$Feature?api-version=7.0"

    title = f"{rf_id} - {titulo}"

    # Tags
    tags = []
    if epic_code:
        tags.append(epic_code)

    payload = [
        {
            "op": "add",
            "path": "/fields/System.Title",
            "value": title
        },
        {
            "op": "add",
            "path": "/fields/System.AreaPath",
            "value": area_path
        },
        {
            "op": "add",
            "path": "/fields/System.State",
            "value": "New"
        },
        {
            "op": "add",
            "path": "/fields/System.Description",
            "value": f"<p>Work Item criado automaticamente para {rf_id}</p><p>Aguardando documentacao e desenvolvimento</p>"
        }
    ]

    if tags:
        payload.append({
            "op": "add",
            "path": "/fields/System.Tags",
            "value": "; ".join(tags)
        })

    try:
        r = requests.post(url, json=payload, headers=get_headers(), auth=get_auth())

        if r.status_code == 200:
            work_item = r.json()
            return work_item['id']
        else:
            fail(f"Erro ao criar Work Item para {rf_id}: {r.status_code}")
            fail(f"Resposta: {r.text[:500]}")
            return None
    except Exception as e:
        fail(f"Excecao ao criar Work Item para {rf_id}: {e}")
        return None

def update_status_yaml(file_path, work_item_id):
    """Atualiza STATUS.yaml com work_item_id e last_sync"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Atualizar work_item_id
        if 'work_item_id: null' in content:
            content = content.replace('work_item_id: null', f'work_item_id: {work_item_id}')
        elif 'work_item_id:' in content:
            content = re.sub(r'work_item_id: \d+', f'work_item_id: {work_item_id}', content)

        # Atualizar last_sync
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if 'last_sync: null' in content:
            content = content.replace('last_sync: null', f'last_sync: "{now}"')
        elif 'last_sync:' in content:
            content = re.sub(r'last_sync: .*', f'last_sync: "{now}"', content)

        # Adicionar board_column se nao existir
        if 'board_column:' not in content:
            content = content.replace(
                'governanca:',
                f'  board_column: "Backlog"\n\ngovernanca:'
            )
        else:
            # Se ja existe mas esta vazio, atualizar
            if 'board_column: null' in content or 'board_column: ""' in content:
                content = re.sub(r'board_column: .*', 'board_column: "Backlog"', content)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return True
    except Exception as e:
        fail(f"Erro ao atualizar {file_path}: {e}")
        return False

# =====================================
# MAIN
# =====================================
def main():
    if not all([ORG_URL, PROJECT, TOKEN]):
        print("=" * 80)
        print("CRIACAO DE WORK ITEMS - VARIAVEIS NAO CONFIGURADAS")
        print("=" * 80)
        print("\nVariaveis de ambiente necessarias:")
        print("  AZDO_ORG_URL - URL da organizacao (ex: https://dev.azure.com/org)")
        print("  AZDO_PROJECT - Nome do projeto")
        print("  AZDO_PAT     - Personal Access Token")
        print("\nDefina usando:")
        print("  set AZDO_ORG_URL=https://dev.azure.com/sua-org")
        print("  set AZDO_PROJECT=IControlIT")
        print("  set AZDO_PAT=seu-token")
        print("=" * 80)
        sys.exit(1)

    print("=" * 80)
    print("CRIACAO DE WORK ITEMS PARA RFs SEM work_item_id")
    print("=" * 80)
    print(f"Org: {ORG_URL}")
    print(f"Project: {PROJECT}")
    print(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Carregar STATUS.yaml
    info("Carregando arquivos STATUS.yaml...")
    statuses = load_all_status_files()
    info(f"Encontrados {len(statuses)} STATUS.yaml")

    # Filtrar RFs sem work_item_id
    rfs_without_wi = {}
    for rf_id, status_info in statuses.items():
        data = status_info['data']
        devops = data.get('devops', {})
        work_item_id = devops.get('work_item_id')

        if not work_item_id or work_item_id == 'null':
            rfs_without_wi[rf_id] = status_info

    info(f"RFs sem Work Item: {len(rfs_without_wi)}")

    if len(rfs_without_wi) == 0:
        print("\n" + "=" * 80)
        print("Todos os RFs ja possuem Work Items!")
        print("=" * 80)
        return 0

    # Contadores
    created = 0
    errors = 0

    print("\n" + "-" * 80)
    print("CRIANDO WORK ITEMS")
    print("-" * 80)

    for rf_id, status_info in sorted(rfs_without_wi.items()):
        data = status_info['data']
        titulo = data.get('titulo', 'Sem titulo')
        epic = data.get('epic', None)
        file_path = status_info['file_path']

        # Extrair Fase e Area Path
        fase_code = extract_fase_from_path(file_path)
        area_path = extract_area_path(file_path, fase_code)

        print(f"\n[+] {rf_id}: {titulo}")
        print(f"    Fase: {fase_code}")
        print(f"    Area: {area_path}")

        # Criar Work Item
        work_item_id = create_work_item(rf_id, titulo, area_path, epic)

        if work_item_id:
            ok(f"Work Item criado: ID {work_item_id}")

            # Atualizar STATUS.yaml
            if update_status_yaml(file_path, work_item_id):
                ok(f"STATUS.yaml atualizado")
                created += 1
            else:
                warn(f"Work Item criado mas falha ao atualizar STATUS.yaml")
                errors += 1
        else:
            errors += 1

    # Resumo
    print("\n" + "=" * 80)
    print("RESUMO DA CRIACAO")
    print("=" * 80)
    print(f"RFs sem Work Item: {len(rfs_without_wi)}")
    print(f"Work Items criados: {created}")
    print(f"Erros: {errors}")

    if created > 0:
        print("\n" + "-" * 80)
        print("PROXIMO PASSO:")
        print("Execute: python tools/devops-sync/sync-all-rfs.py")
        print("Para sincronizar colunas do Board com STATUS.yaml")
        print("-" * 80)

    print("=" * 80)

    return 0 if errors == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
