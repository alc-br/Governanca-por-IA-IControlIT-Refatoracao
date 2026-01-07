#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Sincronizacao Completa: Todos STATUS.yaml -> Azure DevOps Columns

Este script sincroniza TODOS os RFs do projeto.
Para sincronizar apenas um RF, use sync-rf.py

Uso:
    python sync-all-rfs.py

Conforme CONTRATO DE DEVOPS - GOVERNANCA
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

# Campo WEF para controlar coluna do Board (descoberto dinamicamente)
WEF_KANBAN_COLUMN_FIELD = None  # Sera preenchido em runtime

# =====================================
# MAPEAMENTO DE COLUNAS
# =====================================
COLUMNS = {
    "Backlog": {"state": "New", "order": 0},
    "Documentação": {"state": "Active", "order": 1},
    "Backend": {"state": "Active", "order": 2},
    "Frontend": {"state": "Active", "order": 3},
    "Documentacao Testes": {"state": "Active", "order": 4},
    "Testes TI": {"state": "Active", "order": 5},
    "Testes QA": {"state": "Testing", "order": 6},
    "Resolvido": {"state": "Resolved", "order": 7},
    "Finalizado": {"state": "Closed", "order": 8},
}

# Estados protegidos (automacao NAO altera)
PROTECTED_STATES = ["Resolved", "Closed"]

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

def discover_wef_field_from_board():
    """Descobre o campo WEF correto a partir do Features board"""
    global WEF_KANBAN_COLUMN_FIELD

    import urllib.parse
    team = f"{PROJECT} Team"
    project_encoded = urllib.parse.quote(PROJECT)
    team_encoded = urllib.parse.quote(team)

    # Get Features board settings
    board_url = f"{ORG_URL}/{project_encoded}/{team_encoded}/_apis/work/boards/Features?api-version=7.0"
    r = requests.get(board_url, auth=get_auth())

    if r.ok:
        board = r.json()
        fields = board.get('fields', {})
        column_field = fields.get('columnField', {})
        WEF_KANBAN_COLUMN_FIELD = column_field.get('referenceName')
        if WEF_KANBAN_COLUMN_FIELD:
            info(f"Campo WEF do Features board: {WEF_KANBAN_COLUMN_FIELD}")
            return WEF_KANBAN_COLUMN_FIELD

    warn("Campo WEF Kanban.Column nao encontrado no Features board")
    return None

# =====================================
# DETERMINACAO DE COLUNA
# =====================================
def determine_column(status_data):
    """
    Determina a coluna do Board baseado no STATUS.yaml.
    Retorna (coluna, state).

    NOVO FLUXO:
    - Frontend done -> Documentacao Testes (criar TC docs)
    - Todos TC docs existem -> Testes TI (executar testes)
    - Todos testes TI passaram -> Testes QA
    """
    docs = status_data.get('documentacao', {})
    dev = status_data.get('desenvolvimento', {})

    # Novo schema: documentacao_testes (TC files)
    doc_testes = status_data.get('documentacao_testes', {})

    # Novo schema: testes_ti com backend/frontend/e2e/seguranca
    testes_ti = status_data.get('testes_ti', {})

    # Status de desenvolvimento
    backend_status = dev.get('backend', {}).get('status', 'not_started')
    frontend_status = dev.get('frontend', {}).get('status', 'not_started')
    backend_done = backend_status == 'done'
    frontend_done = frontend_status == 'done'

    # Documentacao completa (RF, UC, MD, WF)
    all_docs = (
        docs.get('rf', False) and
        docs.get('uc', False) and
        docs.get('md', False) and
        docs.get('wf', False)
    )

    # Documentacao de Testes - todos os 4 TC docs existem
    all_tc_docs = (
        doc_testes.get('backend', False) and
        doc_testes.get('frontend', False) and
        doc_testes.get('e2e', False) and
        doc_testes.get('seguranca', False)
    )

    # Testes TI - todos os 4 testes passaram
    all_ti_passed = (
        testes_ti.get('backend', 'not_run') == 'pass' and
        testes_ti.get('frontend', 'not_run') == 'pass' and
        testes_ti.get('e2e', 'not_run') == 'pass' and
        testes_ti.get('seguranca', 'not_run') == 'pass'
    )

    # ========================================
    # LOGICA DE DETERMINACAO (mais avancado primeiro)
    # ========================================

    # 6. Testes QA - todos testes TI passaram
    if all_ti_passed and frontend_done and backend_done:
        return "Testes QA", "Testing"

    # 5. Testes TI - todos TC docs existem (executar testes)
    if all_tc_docs and frontend_done and backend_done:
        return "Testes TI", "Active"

    # 4. Documentacao Testes - frontend done (criar TC docs)
    if frontend_done and backend_done:
        return "Documentacao Testes", "Active"

    # 3. Frontend - backend done
    if backend_done and not frontend_done:
        return "Frontend", "Active"

    # 2. Backend - todos docs prontos, backend nao done
    if all_docs and not backend_done:
        return "Backend", "Active"

    # 1. Documentação - RF.md existe mas falta algum doc
    if docs.get('rf', False) and not all_docs:
        return "Documentação", "Active"

    # 0. Backlog - nada iniciado
    return "Backlog", "New"

# =====================================
# YAML PARSER (sem dependencias)
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
    pattern = f"{STATUS_PATH}/**/STATUS.yaml"
    files = glob.glob(pattern, recursive=True)

    statuses = {}
    for f in files:
        try:
            with open(f, 'r', encoding='utf-8') as file:
                content = file.read()

            data = parse_yaml_simple(content)

            if data and 'rf' in data:
                documentacao_raw = str(data['rf']).replace('RF', '').zfill(3)
                documentacao_id = f"RF-{rf_raw}"
                statuses[rf_id] = {
                    'file_path': f,
                    'data': data
                }
        except Exception as e:
            warn(f"Erro ao ler {f}: {e}")

    return statuses

def update_status_file(file_path, work_item_id, column):
    """Atualiza STATUS.yaml com work_item_id, last_sync e board_column"""
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
            # Inserir antes de governanca
            content = content.replace(
                'governanca:',
                f'  board_column: "{column}"\n\ngovernanca:'
            )
        else:
            content = re.sub(r'board_column: .*', f'board_column: "{column}"', content)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return True
    except Exception as e:
        fail(f"Erro ao atualizar {file_path}: {e}")
        return False

# =====================================
# AZURE DEVOPS API
# =====================================
def get_existing_items():
    """Retorna dicionario de titulos -> IDs existentes"""
    url = f"{ORG_URL}/{PROJECT}/_apis/wit/wiql?api-version=7.0"
    query = {"query": "SELECT [System.Id], [System.Title] FROM WorkItems WHERE [System.TeamProject] = @project"}

    r = requests.post(url, json=query, auth=get_auth())
    r.raise_for_status()

    items = r.json().get("workItems", [])
    if not items:
        return {}

    ids = [str(i["id"]) for i in items]

    existing = {}
    for i in range(0, len(ids), 200):
        batch = ids[i:i+200]
        details_url = f"{ORG_URL}/{PROJECT}/_apis/wit/workitems?ids={','.join(batch)}&fields=System.Id,System.Title,System.State&api-version=7.0"
        dr = requests.get(details_url, auth=get_auth())

        for wi in dr.json().get("value", []):
            existing[wi["fields"]["System.Title"]] = {
                "id": wi["fields"]["System.Id"],
                "state": wi["fields"].get("System.State", "New")
            }

    return existing

def update_work_item(wi_id, documentacao_id, column, state, status_data):
    """Atualiza work item com nova coluna e estado"""
    url = f"{ORG_URL}/{PROJECT}/_apis/wit/workitems/{wi_id}?api-version=7.0"

    data = status_data.get('data', {})

    # Status de desenvolvimento
    backend_status = data.get('desenvolvimento', {}).get('backend', {}).get('status', 'not_started')
    frontend_status = data.get('desenvolvimento', {}).get('frontend', {}).get('status', 'not_started')

    # Icones
    def get_icon(s):
        return "✅" if s == 'done' else ("🟡" if s == 'in_progress' else "⬜")

    # Documentacao
    docs = data.get('documentacao', {})
    docs_icons = {
        'RF': '✅' if docs.get('rf') else '⬜',
        'UC': '✅' if docs.get('uc') else '⬜',
        'MD': '✅' if docs.get('md') else '⬜',
        'WF': '✅' if docs.get('wf') else '⬜',
    }

    description = f"""
<h2>📊 Status de Desenvolvimento</h2>
<table border="1" cellpadding="8" style="border-collapse: collapse;">
<tr style="background-color: #e0e0e0;"><th>Camada</th><th>Status</th></tr>
<tr><td><b>Backend</b></td><td>{get_icon(backend_status)} {backend_status.replace('_', ' ').title()}</td></tr>
<tr><td><b>Frontend</b></td><td>{get_icon(frontend_status)} {frontend_status.replace('_', ' ').title()}</td></tr>
</table>

<h2>📄 Documentacao</h2>
<table border="1" cellpadding="8" style="border-collapse: collapse;">
<tr><td>{docs_icons['RF']} RF.md</td><td>{docs_icons['UC']} UC.md</td><td>{docs_icons['MD']} MD.md</td><td>{docs_icons['WF']} WF.md</td></tr>
</table>

<h2>🔄 Board</h2>
<table border="1" cellpadding="8" style="border-collapse: collapse;">
<tr><td><b>Coluna</b></td><td>{column}</td></tr>
<tr><td><b>State</b></td><td>{state}</td></tr>
<tr><td><b>Ultima Sync</b></td><td>{datetime.now().strftime('%Y-%m-%d %H:%M')}</td></tr>
</table>
"""

    payload = [
        {"op": "add", "path": "/fields/System.State", "value": state},
        {"op": "add", "path": "/fields/System.Description", "value": description},
    ]

    # Adicionar campo WEF para mover entre colunas com mesmo State
    if WEF_KANBAN_COLUMN_FIELD:
        payload.append({
            "op": "add",
            "path": f"/fields/{WEF_KANBAN_COLUMN_FIELD}",
            "value": column
        })

    r = requests.patch(url, json=payload, headers=get_headers(), auth=get_auth())

    if r.status_code == 200:
        return True
    else:
        fail(f"Falha ao atualizar {rf_id}: {r.status_code} - {r.text[:200]}")
        return False

# =====================================
# RF NAMES (fallback)
# =====================================
RF_NAMES = {
    "RF-001": "Parametros e Configuracoes do Sistema",
    "RF-002": "Configuracoes e Parametrizacao",
    "RF-003": "Logs Monitoramento Observabilidade",
    "RF-004": "Auditoria Logs Sistema",
    "RF-005": "i18n Orcamento Provisao",
    "RF-006": "Gestao de Clientes",
    "RF-007": "Login e Autenticacao",
    "RF-008": "Gestao Criptografia CERT",
    "RF-009": "Segregacao de Funcoes CERT",
    "RF-010": "Gestao Incidentes Seguranca CERT",
    "RF-011": "Monitoramento Continuo CERT",
    "RF-012": "Gestao de Usuarios",
    "RF-013": "Gestao de Perfis de Acesso",
    "RF-014": "Configuracoes do Usuario",
    "RF-015": "Gestao Locais Enderecos",
    # ... adicionar mais conforme necessario
}

# =====================================
# MAIN
# =====================================
def main():
    if not all([ORG_URL, PROJECT, TOKEN]):
        print("Variaveis de ambiente necessarias:")
        print("  AZDO_ORG_URL - URL da organizacao (ex: https://dev.azure.com/org)")
        print("  AZDO_PROJECT - Nome do projeto")
        print("  AZDO_PAT     - Personal Access Token")
        sys.exit(1)

    print("="*70)
    print("SINCRONIZACAO BOARD: STATUS.yaml -> Azure DevOps Columns")
    print("="*70)
    print(f"Org: {ORG_URL}")
    print(f"Project: {PROJECT}")
    print(f"Status Path: {STATUS_PATH}")
    print()

    # Carregar STATUS.yaml
    info("Carregando arquivos STATUS.yaml...")
    statuses = load_all_status_files()
    info(f"Encontrados {len(statuses)} STATUS.yaml")

    # Obter itens existentes
    info("Carregando itens do Azure DevOps...")
    existing = get_existing_items()
    info(f"Encontrados {len(existing)} work items")

    # Descobrir campo WEF do Features board para controle de colunas
    discover_wef_field_from_board()

    # Contadores
    updated = 0
    skipped_protected = 0
    not_found = 0
    errors = 0
    column_stats = {col: 0 for col in COLUMNS.keys()}

    print("\n" + "-"*70)
    print("PROCESSANDO RFs")
    print("-"*70)

    for documentacao_id, status_info in sorted(statuses.items()):
        data = status_info['data']
        titulo = data.get('titulo', documentacao_id)

        # Encontrar work item
        documentacao_title = f"{rf_id} - {titulo}"

        # Tentar variantes do titulo
        wi_info = None
        for title_variant in [rf_title, f"{rf_id} - {RF_NAMES.get(rf_id, titulo)}"]:
            if title_variant in existing:
                wi_info = existing[title_variant]
                break

        # Buscar por RF-XXX no inicio do titulo
        if not wi_info:
            for title, info_data in existing.items():
                if title.startswith(rf_id):
                    wi_info = info_data
                    break

        if not wi_info:
            warn(f"{rf_id}: Nao encontrado no Azure DevOps")
            not_found += 1
            continue

        wi_id = wi_info["id"]
        current_state = wi_info["state"]

        # Verificar se estado e protegido
        if current_state in PROTECTED_STATES:
            info(f"{rf_id}: Estado protegido ({current_state}), ignorando")
            skipped_protected += 1
            continue

        # Determinar nova coluna
        column, state = determine_column(data)
        column_stats[column] += 1

        # Atualizar work item
        if update_work_item(wi_id, documentacao_id, column, state, status_info):
            ok(f"{rf_id} -> {column} ({state})")
            updated += 1

            # Atualizar STATUS.yaml
            update_status_file(status_info['file_path'], wi_id, column)
        else:
            errors += 1

    # Resumo
    print("\n" + "="*70)
    print("RESUMO DA SINCRONIZACAO")
    print("="*70)
    print(f"\nRFs processados: {len(statuses)}")
    print(f"Atualizados: {updated}")
    print(f"Protegidos (ignorados): {skipped_protected}")
    print(f"Nao encontrados: {not_found}")
    print(f"Erros: {errors}")

    print(f"\nDISTRIBUICAO POR COLUNA:")
    print("-"*40)
    for col in ["Backlog", "Documentação", "Backend", "Frontend",
                "Documentacao Testes", "Testes TI", "Testes QA"]:
        count = column_stats.get(col, 0)
        bar = "#" * min(count, 30)
        print(f"  {col:20} {count:3} {bar}")

    print("="*70)

if __name__ == "__main__":
    main()
