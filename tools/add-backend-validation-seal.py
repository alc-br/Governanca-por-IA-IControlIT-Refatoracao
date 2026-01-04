#!/usr/bin/env python3
"""
Script para adicionar selo de validação de contrato backend em STATUS.yaml

Este script adiciona os campos:
- contrato_validado: true
- contrato: CONTRATO-EXECUCAO-BACKEND
- versao_contrato: v1.0

Apenas em RFs onde desenvolvimento.backend.status == 'done'
"""

import os
import re
from pathlib import Path

def find_all_status_yaml(base_path: Path) -> list[Path]:
    """Encontra todos os arquivos STATUS.yaml recursivamente"""
    return list(base_path.rglob("STATUS.yaml"))

def has_backend_done(content: str) -> bool:
    """Verifica se backend tem status done"""
    # Procura por padrão:
    #   backend:
    #     status: done
    pattern = r'backend:\s*\n\s+status:\s+done'
    return bool(re.search(pattern, content))

def already_has_seal(content: str) -> bool:
    """Verifica se já tem o selo de validação"""
    return 'contrato_validado' in content

def add_validation_seal(file_path: Path) -> bool:
    """
    Adiciona selo de validação ao STATUS.yaml
    Retorna True se modificou, False caso contrário
    """
    # Ler arquivo
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Verificar se precisa modificar
    if not has_backend_done(content):
        return False

    if already_has_seal(content):
        print(f"[SKIP] {file_path.parent.name} - Ja possui selo")
        return False

    # Encontrar a linha "status: done" dentro de backend
    lines = content.split('\n')
    modified_lines = []
    in_backend_section = False
    status_line_found = False

    for i, line in enumerate(lines):
        modified_lines.append(line)

        # Detectar início da seção backend
        if re.match(r'^  backend:\s*$', line):
            in_backend_section = True
            continue

        # Detectar fim da seção backend (outra seção no mesmo nível que não seja frontend)
        if in_backend_section and re.match(r'^  \w+:\s*$', line) and 'frontend' not in line:
            in_backend_section = False

        # Se estamos em backend e encontramos status: done
        if in_backend_section and re.match(r'^\s+status:\s+done\s*(?:#.*)?$', line):
            status_line_found = True
            # Adicionar as 3 novas linhas logo após status: done
            indent = '    '  # 4 espaços (mesmo nível de status, branch)
            modified_lines.append(f'{indent}contrato_validado: true')
            modified_lines.append(f'{indent}contrato: CONTRATO-EXECUCAO-BACKEND')
            modified_lines.append(f'{indent}versao_contrato: v1.0')
            in_backend_section = False  # Já processamos, não precisamos mais

    if not status_line_found:
        print(f"[WARN] {file_path.parent.name} - Backend done mas nao encontrou linha 'status: done'")
        return False

    # Escrever arquivo modificado
    new_content = '\n'.join(modified_lines)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    rf_name = file_path.parent.name
    print(f"[OK] {rf_name} - Selo de validacao adicionado")
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
        if add_validation_seal(status_file):
            modified_count += 1

    print()
    print("[RESULTADO]")
    print(f"   Total de arquivos: {len(status_files)}")
    print(f"   Modificados: {modified_count}")
    print(f"   Ja tinham selo ou backend != done: {len(status_files) - modified_count}")

if __name__ == "__main__":
    main()
