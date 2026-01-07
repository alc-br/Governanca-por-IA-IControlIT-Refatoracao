#!/usr/bin/env python3
"""
Script de Transição TESTES → DEPLOY (Governado por Contrato)

Contrato: CONTRATO-TRANSICAO-TESTES-PARA-DEPLOY
Tipo: DECISORIA
Autoridade: DevOps Agent (baseado em decisão QA/Tester)

Este script:
- Valida pré-requisitos no EXECUTION-MANIFEST
- Atualiza STATUS.yaml
- Registra transição no EXECUTION-MANIFEST
- NEGA execução se qualquer regra falhar
"""

import sys
import re
from pathlib import Path
from datetime import datetime

# Paths absolutos
BASE_DIR = Path(__file__).resolve().parents[2]
MANIFEST_PATH = BASE_DIR / "docs/contracts/EXECUTION-MANIFEST.md"
RF_BASE = BASE_DIR / "docs/rf"

def abort(msg):
    """Aborta execução com mensagem"""
    print(f"[ABORTADO] {msg}")
    print("[REGRA] Transição NEGADA por violação de pré-requisito")
    sys.exit(1)

def load_manifest():
    """Carrega EXECUTION-MANIFEST.md"""
    if not MANIFEST_PATH.exists():
        abort(f"EXECUTION-MANIFEST não encontrado: {MANIFEST_PATH}")

    return MANIFEST_PATH.read_text(encoding="utf-8")

def find_last_approved_test_execution(manifest_content, rf):
    """
    Encontra a última execução DECISORIA APROVADA de testes para o RF

    Retorna o bloco de execução ou None se não encontrado
    """
    # Dividir manifesto em blocos de execução
    blocks = re.split(r"\n# EXECUCAO:", manifest_content)

    approved_blocks = []

    for block in blocks:
        # Verificar se é do RF correto
        if f"RF: {rf}" not in block:
            continue

        # Verificar se é CONTRATO-EXECUCAO-TESTES
        if "CONTRATO-EXECUCAO-TESTES" not in block:
            continue

        # Verificar se tem DECISAO FORMAL com resultado APROVADO
        if "DECISAO FORMAL" not in block:
            continue

        if "resultado: APROVADO" not in block:
            continue

        # Extrair ID da execução
        match = re.search(r'^(.+)$', block, re.MULTILINE)
        if match:
            execution_id = match.group(1).strip()
            approved_blocks.append({
                'id': execution_id,
                'content': block,
                'full': f"# EXECUCAO:{block}"
            })

    if not approved_blocks:
        return None

    # Retornar o último (mais recente)
    return approved_blocks[-1]

def load_status_yaml(rf):
    """Encontra e retorna o path do STATUS.yaml do RF"""
    for path in RF_BASE.rglob("STATUS.yaml"):
        try:
            content = path.read_text(encoding="utf-8")
            if f"rf: {rf}" in content:
                return path
        except Exception:
            continue

    abort(f"STATUS.yaml não encontrado para {rf}")

def validate_status_yaml(status_path, rf):
    """Valida que STATUS.yaml está no estado correto"""
    content = status_path.read_text(encoding="utf-8")

    # Verificar se contrato_ativo é CONTRATO-EXECUCAO-TESTES
    if "contrato_ativo: CONTRATO-EXECUCAO-TESTES" not in content:
        abort(f"STATUS.yaml de {rf} não tem contrato_ativo: CONTRATO-EXECUCAO-TESTES")

    return True

def update_status_yaml(status_path, manifest_id, rf):
    """Atualiza STATUS.yaml para estado PRONTO PARA DEPLOY"""
    content = status_path.read_text(encoding="utf-8")

    # Atualizar contrato_ativo
    content = re.sub(
        r'(contrato_ativo:\s+).+$',
        r'\1CONTRATO-EXECUCAO-DEPLOY',
        content,
        flags=re.MULTILINE
    )

    # Atualizar ultimo_manifesto
    content = re.sub(
        r'(ultimo_manifesto:\s+).+$',
        f'\\1{manifest_id}',
        content,
        flags=re.MULTILINE
    )

    # Atualizar board_column
    content = re.sub(
        r'(board_column:\s+)"?[^"\n]+"?$',
        r'\1"Pronto para Deploy"',
        content,
        flags=re.MULTILINE
    )

    # Atualizar last_sync
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content = re.sub(
        r'(last_sync:\s+)"?[^"\n]+"?$',
        f'\\1"{timestamp}"',
        content,
        flags=re.MULTILINE
    )

    # Escrever arquivo atualizado
    status_path.write_text(content, encoding="utf-8")

    print(f"[OK] STATUS.yaml de {rf} atualizado")
    print(f"     - contrato_ativo: CONTRATO-EXECUCAO-DEPLOY")
    print(f"     - ultimo_manifesto: {manifest_id}")
    print(f'     - board_column: "Pronto para Deploy"')
    print(f"     - last_sync: {timestamp}")

def register_transition_in_manifest(rf, manifest_id):
    """Registra a transição no EXECUTION-MANIFEST"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    execution_id = f"{rf}-TRANSITION-TESTS-TO-DEPLOY-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

    transition_block = f"""

# EXECUCAO: {execution_id}

## TIPO DE EXECUCAO

- Tipo: DECISORIA

## CONTRATO ATIVO

- Contrato: CONTRATO-TRANSICAO-TESTES-PARA-DEPLOY
- RF: {rf}
- Data: {timestamp}
- Executor: DevOps Agent (Automated)

## PRE-REQUISITOS VALIDADOS

- [x] Testes aprovados no manifesto (ID: {manifest_id})
- [x] STATUS.yaml em estado válido
- [x] Contrato ativo era CONTRATO-EXECUCAO-TESTES

## ACAO EXECUTADA

- STATUS.yaml atualizado
- Contrato ativo alterado para CONTRATO-EXECUCAO-DEPLOY
- Board column alterado para "Pronto para Deploy"
- Timestamp de sincronização atualizado

## DECISAO FORMAL

decision:
  resultado: APROVADO
  autoridade: DevOps-Agent
  contrato: CONTRATO-TRANSICAO-TESTES-PARA-DEPLOY
  baseado_em: {manifest_id}

---
"""

    # Adicionar ao final do manifesto
    manifest_content = MANIFEST_PATH.read_text(encoding="utf-8")
    manifest_content += transition_block
    MANIFEST_PATH.write_text(manifest_content, encoding="utf-8")

    print(f"[OK] Transição registrada no EXECUTION-MANIFEST")
    print(f"     - ID: {execution_id}")

def main():
    """Função principal"""
    # Validar argumentos
    if len(sys.argv) != 2:
        print("USO:")
        print("  python apply_tests_to_deploy_transition.py RFXXX")
        print()
        print("EXEMPLO:")
        print("  python apply_tests_to_deploy_transition.py RF001")
        sys.exit(1)

    documentacao = sys.argv[1]

    print(f"[INFO] Iniciando transição TESTES → DEPLOY para {rf}")
    print(f"[INFO] Contrato: CONTRATO-TRANSICAO-TESTES-PARA-DEPLOY")
    print()

    # 1. Carregar EXECUTION-MANIFEST
    print("[1/5] Carregando EXECUTION-MANIFEST...")
    manifest_content = load_manifest()
    print("      OK")

    # 2. Validar existência de execução de testes aprovada
    print(f"[2/5] Validando execução de testes aprovada para {rf}...")
    approved_test = find_last_approved_test_execution(manifest_content, rf)

    if not approved_test:
        abort(f"Nenhuma execução de testes APROVADA encontrada para {rf}")

    manifest_id = approved_test['id']
    print(f"      OK - Encontrado: {manifest_id}")

    # 3. Localizar STATUS.yaml
    print(f"[3/5] Localizando STATUS.yaml de {rf}...")
    status_path = load_status_yaml(rf)
    print(f"      OK - {status_path}")

    # 4. Validar estado do STATUS.yaml
    print(f"[4/5] Validando estado do STATUS.yaml...")
    validate_status_yaml(status_path, rf)
    print("      OK - Estado válido")

    # 5. Executar transição
    print(f"[5/5] Executando transição...")
    update_status_yaml(status_path, manifest_id, rf)
    register_transition_in_manifest(rf, manifest_id)

    print()
    print("=" * 70)
    print(f"[SUCESSO] Transição TESTES → DEPLOY concluída para {rf}")
    print("=" * 70)
    print()
    print("PRÓXIMO PASSO:")
    print(f"  - Contrato ativo: CONTRATO-EXECUCAO-DEPLOY")
    print(f'  - Board column: "Pronto para Deploy"')
    print()
    print("Para executar o deploy:")
    print(f"  python tools/devops-sync/execute_deploy.py {rf}")
    print()

if __name__ == "__main__":
    main()
