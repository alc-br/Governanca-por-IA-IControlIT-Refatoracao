#!/usr/bin/env python3
"""
Script para corrigir devops.board_column em STATUS.yaml

Regras:
- Se contrato_ativo = CONTRATO-EXECUCAO-BACKEND → board_column = "Backend Validado"
- Se contrato_ativo = CONTRATO-EXECUCAO-TESTES → board_column = "Testes Pendentes"
- Se contrato_ativo = CONTRATO-EXECUCAO-FRONTEND → board_column = "Frontend em Desenvolvimento"
"""

import re
from pathlib import Path

def find_all_status_yaml(base_path: Path) -> list[Path]:
    """Encontra todos os arquivos STATUS.yaml recursivamente"""
    return list(base_path.rglob("STATUS.yaml"))

def get_contrato_ativo(content: str) -> str:
    """Extrai o contrato_ativo do conteúdo"""
    match = re.search(r'contrato_ativo:\s+(.+)$', content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return None

def get_board_column(content: str) -> str:
    """Extrai o board_column do conteúdo"""
    match = re.search(r'board_column:\s+"?([^"\n]+)"?$', content, re.MULTILINE)
    if match:
        return match.group(1).strip().strip('"')
    return None

def determine_correct_board_column(contrato_ativo: str) -> str:
    """Determina qual deve ser o board_column correto"""
    mapping = {
        'CONTRATO-EXECUCAO-BACKEND': 'Backend Validado',
        'CONTRATO-EXECUCAO-FRONTEND': 'Frontend em Desenvolvimento',
        'CONTRATO-EXECUCAO-TESTES': 'Testes Pendentes',
    }
    return mapping.get(contrato_ativo, None)

def fix_board_column(file_path: Path) -> bool:
    """
    Corrige devops.board_column no STATUS.yaml
    Retorna True se modificou, False caso contrário
    """
    # Ler arquivo
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extrair informações
    contrato_ativo = get_contrato_ativo(content)
    current_board_column = get_board_column(content)

    if not contrato_ativo:
        return False

    # Determinar coluna correta
    correct_board_column = determine_correct_board_column(contrato_ativo)

    if not correct_board_column:
        return False

    # Se já está correto, não faz nada
    if current_board_column == correct_board_column:
        return False

    # Substituir board_column
    old_pattern = r'(board_column:\s+)"?[^"\n]+"?$'
    new_value = f'\\1"{correct_board_column}"'
    new_content = re.sub(old_pattern, new_value, content, flags=re.MULTILINE)

    # Escrever arquivo modificado
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    rf_name = file_path.parent.name
    print(f"[OK] {rf_name} - Board alterado: {current_board_column} -> {correct_board_column}")
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
        if fix_board_column(status_file):
            modified_count += 1

    print()
    print("[RESULTADO]")
    print(f"   Total de arquivos: {len(status_files)}")
    print(f"   Modificados: {modified_count}")
    print(f"   Ja estavam corretos: {len(status_files) - modified_count}")

if __name__ == "__main__":
    main()
