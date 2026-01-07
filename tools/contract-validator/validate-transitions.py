#!/usr/bin/env python3
"""
Script de Validação de Transições de Contratos

Valida que a ordem de execução de contratos está conforme CONTRATO-ORQUESTRACAO
e contract-transitions.yaml.

Este script implementa as regras de governança de ordem de execução.
"""

import sys
import yaml
from pathlib import Path

# Paths absolutos
BASE_DIR = Path(__file__).resolve().parents[2]
TRANSITIONS_FILE = BASE_DIR / "docs/contracts/contract-transitions.yaml"
STATUS_BASE = BASE_DIR / "docs/rf"

def load_transitions():
    """Carrega matriz de transições permitidas"""
    if not TRANSITIONS_FILE.exists():
        print(f"[ERRO] Arquivo de transições não encontrado: {TRANSITIONS_FILE}")
        sys.exit(1)

    with open(TRANSITIONS_FILE, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def load_status_yaml(rf):
    """Carrega STATUS.yaml de um RF"""
    for path in STATUS_BASE.rglob("STATUS.yaml"):
        try:
            content = path.read_text(encoding='utf-8')
            if f"rf: {rf}" in content:
                with open(path, 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f), path
        except Exception:
            continue

    return None, None

def validate_transition(current_contract, next_contract, transitions):
    """
    Valida se a transição do contrato atual para o próximo é permitida

    Returns:
        (bool, str) - (válido, mensagem)
    """
    # Normalizar nomes (remover "CONTRATO-" se houver)
    current_normalized = current_contract.replace("CONTRATO-", "")
    next_normalized = next_contract.replace("CONTRATO-", "")

    # Buscar no YAML
    if current_normalized not in transitions:
        return False, f"Contrato '{current_normalized}' não está definido em contract-transitions.yaml"

    current_def = transitions[current_normalized]

    # Verificar se próximo contrato está na lista de permitidos
    allowed_next = current_def.get('allowed_next', [])

    if next_normalized in allowed_next:
        return True, f"Transição permitida: {current_normalized} → {next_normalized}"

    # Verificar aliases/variações de nome
    # Ex: EXECUCAO-TESTES pode ser TESTES
    for allowed in allowed_next:
        if allowed in next_normalized or next_normalized in allowed:
            return True, f"Transição permitida (variação de nome): {current_normalized} → {next_normalized}"

    return False, f"Transição NÃO permitida: {current_normalized} → {next_normalized}. Permitidos: {', '.join(allowed_next)}"

def validate_rf_transition(rf, next_contract):
    """
    Valida se um RF pode transicionar para o próximo contrato

    Args:
        documentacao: ID do RF (ex: RF015)
        next_contract: Próximo contrato a ser executado

    Returns:
        (bool, str, dict) - (válido, mensagem, status_atual)
    """
    # Carregar transições
    transitions = load_transitions()

    # Carregar STATUS.yaml do RF
    status_data, status_path = load_status_yaml(rf)

    if not status_data:
        return False, f"STATUS.yaml não encontrado para {rf}", None

    # Obter contrato atual
    current_contract = status_data.get('governanca', {}).get('contrato_ativo')

    if not current_contract:
        return False, f"Campo governanca.contrato_ativo não encontrado em STATUS.yaml de {rf}", status_data

    # Validar transição
    valid, message = validate_transition(current_contract, next_contract, transitions)

    return valid, message, status_data

def main():
    """Função principal"""
    if len(sys.argv) < 3:
        print("USO:")
        print("  python validate-transitions.py RFXXX PROXIMO-CONTRATO")
        print()
        print("EXEMPLOS:")
        print("  python validate-transitions.py RF015 CONTRATO-EXECUCAO-TESTES")
        print("  python validate-transitions.py RF015 CONTRATO-TRANSICAO-TESTES-PARA-DEPLOY")
        print()
        print("DESCRIÇÃO:")
        print("  Valida se a transição do contrato atual (em STATUS.yaml)")
        print("  para o próximo contrato é permitida conforme contract-transitions.yaml")
        sys.exit(1)

    documentacao = sys.argv[1]
    next_contract = sys.argv[2]

    print(f"[VALIDAÇÃO] Verificando transição para {rf}")
    print(f"[VALIDAÇÃO] Próximo contrato: {next_contract}")
    print()

    # Validar transição
    valid, message, status = validate_rf_transition(rf, next_contract)

    if valid:
        print(f"[OK] {message}")
        print()
        print("APROVADO: Transição pode prosseguir")
        sys.exit(0)
    else:
        print(f"[BLOQUEADO] {message}")
        print()
        if status:
            current = status.get('governanca', {}).get('contrato_ativo', 'DESCONHECIDO')
            print(f"Estado atual de {rf}:")
            print(f"  - Contrato ativo: {current}")
            print(f"  - Backend: {status.get('desenvolvimento', {}).get('backend', {}).get('status', 'N/A')}")
            print(f"  - Frontend: {status.get('desenvolvimento', {}).get('frontend', {}).get('status', 'N/A')}")
        print()
        print("NEGADO: Transição viola regras de governança")
        print("AÇÃO: Verifique contract-transitions.yaml para transições permitidas")
        sys.exit(1)

if __name__ == "__main__":
    main()
