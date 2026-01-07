#!/usr/bin/env python3
"""
Script para corrigir governanca.contrato_ativo em STATUS.yaml

Regras:
- Se backend done E frontend not_started → contrato_ativo = CONTRATO-EXECUCAO-BACKEND
- Se backend done E frontend done E testes not_run → contrato_ativo = CONTRATO-EXECUCAO-TESTES
- Se testes executados → manter como está
"""

import re
from pathlib import Path

def find_all_status_yaml(base_path: Path) -> list[Path]:
    """Encontra todos os arquivos STATUS.yaml recursivamente"""
    return list(base_path.rglob("STATUS.yaml"))

def get_status_info(content: str) -> dict:
    """Extrai informações de status do conteúdo"""
    info = {
        'backend_status': None,
        'frontend_status': None,
        'testes_backend': None,
        'testes_frontend': None,
        'contrato_ativo': None,
    }

    # Backend status
    match = re.search(r'backend:\s*\n\s+status:\s+(\w+)', content)
    if match:
        info['backend_status'] = match.group(1)

    # Frontend status
    match = re.search(r'frontend:\s*\n\s+status:\s+(\w+)', content)
    if match:
        info['frontend_status'] = match.group(1)

    # Testes backend
    match = re.search(r'testes:\s*\n\s+backend:\s+(\w+)', content)
    if match:
        info['testes_backend'] = match.group(1)

    # Testes frontend
    match = re.search(r'testes:\s*\n\s+backend:.*\n\s+frontend:\s+(\w+)', content, re.MULTILINE)
    if match:
        info['testes_frontend'] = match.group(1)

    # Contrato ativo
    match = re.search(r'contrato_ativo:\s+(.+)$', content, re.MULTILINE)
    if match:
        info['contrato_ativo'] = match.group(1).strip()

    return info

def determine_correct_contrato(info: dict) -> str:
    """Determina qual deve ser o contrato_ativo correto"""
    backend = info['backend_status']
    frontend = info['frontend_status']
    testes_back = info['testes_backend']
    testes_front = info['testes_frontend']

    # Se backend não está done, não tem contrato ativo de desenvolvimento
    if backend != 'done':
        return None

    # Se testes já executaram (pass ou fail), manter TESTES
    if testes_back in ['pass', 'fail'] or testes_front in ['pass', 'fail']:
        return 'CONTRATO-EXECUCAO-TESTES'

    # Se frontend done, contrato é TESTES
    if frontend == 'done':
        return 'CONTRATO-EXECUCAO-TESTES'

    # Se backend done mas frontend não, contrato é BACKEND
    if frontend in ['not_started', 'in_progress']:
        return 'CONTRATO-EXECUCAO-BACKEND'

    return None

def fix_governanca_contrato(file_path: Path) -> bool:
    """
    Corrige governanca.contrato_ativo no STATUS.yaml
    Retorna True se modificou, False caso contrário
    """
    # Ler arquivo
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extrair informações
    info = get_status_info(content)

    # Determinar contrato correto
    correct_contrato = determine_correct_contrato(info)

    if not correct_contrato:
        return False

    # Se já está correto, não faz nada
    if info['contrato_ativo'] == correct_contrato:
        return False

    # Substituir contrato_ativo
    old_pattern = r'(contrato_ativo:\s+).+$'
    new_value = f'\\1{correct_contrato}'
    new_content = re.sub(old_pattern, new_value, content, flags=re.MULTILINE)

    # Escrever arquivo modificado
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    documentacao_name = file_path.parent.name
    print(f"[OK] {rf_name} - Contrato alterado: {info['contrato_ativo']} -> {correct_contrato}")
    return True

def main():
    """Função principal"""
    base_path = Path(r"D:\IC2\docs\rf")

    if not base_path.exists():
        print(f"[ERRO] Caminho nao encontrado: {base_path}")
        return

    print("[INFO] Procurando arquivos STATUS.yaml...")
    status_files = find_all_status_yaml(base_path)
    print(f"[INFO] Encontrados {len(status_files)} arquivos STATUS.yaml")
    print()

    modified_count = 0
    for status_file in status_files:
        if fix_governanca_contrato(status_file):
            modified_count += 1

    print()
    print("[RESULTADO]")
    print(f"   Total de arquivos: {len(status_files)}")
    print(f"   Modificados: {modified_count}")
    print(f"   Ja estavam corretos: {len(status_files) - modified_count}")

if __name__ == "__main__":
    main()
