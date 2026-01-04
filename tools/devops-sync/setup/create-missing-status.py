#!/usr/bin/env python3
"""
Script para criar STATUS.yaml mínimo para RFs sem Work Item
Garante que todos os RFs planejados apareçam no Board do Azure DevOps
"""

import os
import sys
import re
from pathlib import Path
from datetime import datetime

# Diretórios a processar
RF_DIRS = [
    r"D:\IC2\docs\rf"
]

def extract_rf_info(rf_path: Path) -> dict:
    """Extrai informações do RF a partir do caminho da pasta"""
    # Exemplo: Fase-1-Sistema-Base/EPIC001-SYS-Sistema-Infraestrutura/RF001-Parametros-e-Configuracoes-do-Sistema
    parts = rf_path.parts

    # Encontrar RF, EPIC e Fase
    rf_folder = parts[-1]
    epic_folder = parts[-2] if len(parts) > 1 else "UNKNOWN"
    fase_folder = parts[-3] if len(parts) > 2 else "UNKNOWN"

    # Extrair RF number e título
    rf_match = re.match(r'RF(\d+)-(.*)', rf_folder)
    if not rf_match:
        return None

    rf_num = rf_match.group(1)
    rf_title = rf_match.group(2).replace('-', ' ')

    # Extrair EPIC
    epic_match = re.match(r'(EPIC\d+)-(.*)', epic_folder)
    epic_code = epic_match.group(1) if epic_match else "UNKNOWN"

    # Extrair Fase
    fase_match = re.match(r'(Fase-\d+)-(.*)', fase_folder)
    fase_code = fase_match.group(1) if fase_match else "UNKNOWN"

    return {
        'rf': f'RF{rf_num}',
        'rf_num': rf_num,
        'titulo': rf_title,
        'epic': epic_code,
        'fase': fase_code,
        'path': rf_path
    }

def create_status_yaml(rf_info: dict) -> str:
    """Cria conteúdo de STATUS.yaml mínimo"""
    return f"""rf: RF{rf_info['rf_num'].zfill(3)}
fase: {rf_info['fase']}
epic: {rf_info['epic']}
titulo: {rf_info['titulo']}

documentacao:
  rf: False
  uc: False
  md: False
  wf: False

desenvolvimento:
  backend:
    status: not_started   # not_started | in_progress | done
    branch: null
  frontend:
    status: not_started
    branch: null

testes:
  backend: not_run        # not_run | pass | fail
  frontend: not_run
  e2e: not_run
  seguranca: not_run

documentacao_testes:
  backend: False
  frontend: False
  e2e: False
  seguranca: False

testes_ti:
  backend: not_run
  frontend: not_run
  e2e: not_run
  seguranca: not_run

testes_qa:
  executado: False       # True quando QA executou
  aprovado: False        # True quando usuario aprovou

devops:
  work_item_id: null
  test_plan_id: null
  last_sync: null
  board_column: "Backlog"

governanca:
  contrato_ativo: null
  ultimo_manifesto: null
"""

def process_rf_directories():
    """Processa todos os diretórios RF e cria STATUS.yaml onde falta"""
    created = []
    skipped = []
    errors = []

    for rf_dir_root in RF_DIRS:
        if not os.path.exists(rf_dir_root):
            print(f"[!] Diretorio nao encontrado: {rf_dir_root}")
            continue

        print(f"\n[>] Processando: {rf_dir_root}")

        # Encontrar todas as pastas RF*
        for root, dirs, files in os.walk(rf_dir_root):
            for dir_name in dirs:
                if dir_name.startswith('RF') and re.match(r'RF\d+', dir_name):
                    rf_path = Path(root) / dir_name
                    status_file = rf_path / 'STATUS.yaml'

                    # Verificar se STATUS.yaml já existe
                    if status_file.exists():
                        skipped.append(str(rf_path))
                        continue

                    # Extrair informações do RF
                    rf_info = extract_rf_info(rf_path)
                    if not rf_info:
                        errors.append(f"Não foi possível extrair info de {rf_path}")
                        continue

                    # Criar STATUS.yaml
                    try:
                        status_content = create_status_yaml(rf_info)
                        status_file.write_text(status_content, encoding='utf-8')
                        created.append(rf_info['rf'])
                        print(f"[OK] Criado: {rf_info['rf']} - {rf_info['titulo']}")
                    except Exception as e:
                        errors.append(f"Erro ao criar {status_file}: {e}")

    return created, skipped, errors

def main():
    """Função principal"""
    print("=" * 80)
    print("CRIAÇÃO DE STATUS.YAML PARA RFs SEM WORK ITEM")
    print("=" * 80)
    print(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    created, skipped, errors = process_rf_directories()

    print("\n" + "=" * 80)
    print("RELATORIO FINAL")
    print("=" * 80)
    print(f"[OK] STATUS.yaml criados: {len(created)}")
    print(f"[>>] Ja existiam (pulados): {len(skipped)}")
    print(f"[!!] Erros: {len(errors)}")

    if created:
        print(f"\n[+] RFs com STATUS.yaml criado:")
        for rf in sorted(created):
            print(f"   - {rf}")

    if errors:
        print(f"\n[!!] Erros encontrados:")
        for error in errors:
            print(f"   - {error}")

    print("\n" + "=" * 80)
    print("PRÓXIMO PASSO:")
    print("Execute: python tools/devops-sync/sync-all-rfs.py")
    print("Para criar Work Items no Azure DevOps para todos os RFs")
    print("=" * 80)

    return 0 if not errors else 1

if __name__ == '__main__':
    sys.exit(main())
