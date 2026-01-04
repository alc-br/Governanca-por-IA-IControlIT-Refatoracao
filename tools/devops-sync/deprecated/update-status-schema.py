#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Atualiza todos os STATUS.yaml com os novos campos para suportar o fluxo de Board.

Novos campos adicionados:
- testes_ti: Testes de TI (pos-desenvolvimento)
- documentacao_qa: Documentacao de QA
- testes_qa: Testes de QA
- devops.board_column: Coluna atual do Board
"""

import os
import glob
import re

STATUS_PATH = "D:/IC2/docs/rf"

NEW_FIELDS_TEMPLATE = """
testes_ti:
  executado: False       # True quando TI executou os testes
  resultado: null        # pass | fail | null

documentacao_qa:
  tc: False              # TC-RFXXX.md existe
  mt: False              # MT-RFXXX.md (Manual de Teste) existe

testes_qa:
  executado: False       # True quando QA executou
  aprovado: False        # True quando usuario aprovou

"""

def update_status_file(filepath):
    """Adiciona novos campos ao STATUS.yaml"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        modified = False

        # Verificar se campos ja existem
        if 'testes_ti:' not in content:
            # Inserir antes de 'devops:'
            if 'devops:' in content:
                content = content.replace(
                    'devops:',
                    NEW_FIELDS_TEMPLATE + 'devops:'
                )
                modified = True

        # Adicionar board_column no devops se nao existir
        if 'board_column:' not in content:
            if 'last_sync:' in content:
                content = re.sub(
                    r'(last_sync: .+)',
                    r'\1\n  board_column: null',
                    content
                )
                modified = True

        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True

        return False

    except Exception as e:
        print(f"[ERRO] {filepath}: {e}")
        return False

def main():
    print("="*60)
    print("ATUALIZACAO DE SCHEMA - STATUS.yaml")
    print("="*60)

    pattern = f"{STATUS_PATH}/**/STATUS.yaml"
    files = glob.glob(pattern, recursive=True)

    print(f"\nEncontrados {len(files)} arquivos STATUS.yaml")

    updated = 0
    skipped = 0
    errors = 0

    for filepath in files:
        result = update_status_file(filepath)
        if result:
            rf_match = re.search(r'(RF\d+)', filepath)
            rf = rf_match.group(1) if rf_match else filepath
            print(f"[OK] {rf}: Schema atualizado")
            updated += 1
        elif result is False:
            skipped += 1
        else:
            errors += 1

    print("\n" + "-"*60)
    print(f"Atualizados: {updated}")
    print(f"Ja atualizados: {skipped}")
    print(f"Erros: {errors}")
    print("="*60)

if __name__ == "__main__":
    main()
