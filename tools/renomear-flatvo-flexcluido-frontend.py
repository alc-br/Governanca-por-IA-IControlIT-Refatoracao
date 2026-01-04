#!/usr/bin/env python3
"""
Script para renomear flAtivo → flExcluido nos models TypeScript do frontend
Conforme ADR-004: Soft Delete com FlExcluido (Opção A)

Data: 2025-12-25
"""

import os
import re
from pathlib import Path

# Diretório base dos models
MODELS_DIR = Path("d:/IC2/frontend/icontrolit-app/src/app/core/models")

# Contadores
arquivos_processados = 0
arquivos_alterados = 0
total_substituicoes = 0

# Log de alterações
log_lines = []

def renomear_flatvo_flexcluido(filepath):
    """Renomeia flAtivo para flExcluido no model TypeScript"""
    global arquivos_processados, arquivos_alterados, total_substituicoes

    arquivos_processados += 1

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            conteudo_original = f.read()

        # Verificar se tem flAtivo
        if not re.search(r'\bflAtivo\s*:\s*boolean', conteudo_original):
            log_msg = f"[SKIP] {filepath.name}: nao tem flAtivo"
            log_lines.append(log_msg)
            print(log_msg)
            return

        conteudo_novo = conteudo_original
        substituicoes_arquivo = 0

        # 1. Renomear flAtivo: boolean → flExcluido: boolean
        # Adicionar comentário JSDoc antes da propriedade
        conteudo_novo, count = re.subn(
            r'(\s*)flAtivo\s*:\s*boolean\s*;',
            r'\1/**\n\1 * Soft delete: false=ativo (nao deletado), true=excluido (deletado)\n\1 */\n\1flExcluido: boolean;',
            conteudo_novo
        )
        substituicoes_arquivo += count

        # 2. Se já havia comentário antes de flAtivo, remover duplicação
        # Padrão: comentário existente + comentário novo + flExcluido
        conteudo_novo = re.sub(
            r'(/\*\*[^*]*\*/)(\s*/\*\*\s*\n\s*\*\s*Soft delete[^*]*\*/\s*\n\s*flExcluido\s*:\s*boolean;)',
            r'\2',
            conteudo_novo
        )

        # Salvar se houve alterações
        if conteudo_novo != conteudo_original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(conteudo_novo)

            arquivos_alterados += 1
            total_substituicoes += substituicoes_arquivo

            log_msg = f"[OK] {filepath.name}: {substituicoes_arquivo} substituicoes (flAtivo -> flExcluido)"
            log_lines.append(log_msg)
            print(log_msg)
        else:
            log_msg = f"[SKIP] {filepath.name}: sem alteracoes necessarias"
            log_lines.append(log_msg)

    except Exception as e:
        log_msg = f"[ERROR] {filepath.name}: {e}"
        log_lines.append(log_msg)
        print(log_msg)

def main():
    print("=" * 80)
    print("RENOMEAR flAtivo -> flExcluido NOS MODELS TYPESCRIPT")
    print("ADR-004: Opcao A - Alinhamento Total com Backend")
    print("=" * 80)
    print()

    # Processar todos os models TypeScript
    for model_file in MODELS_DIR.glob("*.model.ts"):
        renomear_flatvo_flexcluido(model_file)

    print()
    print("=" * 80)
    print("RESUMO")
    print("=" * 80)
    print(f"Arquivos processados: {arquivos_processados}")
    print(f"Arquivos alterados: {arquivos_alterados}")
    print(f"Total de substituicoes: {total_substituicoes}")
    print()

    # Salvar log
    log_file = Path("d:/IC2/relatorios/2025-12-25-Renomear-FlAtivo-FlExcluido-Log.txt")
    log_file.parent.mkdir(parents=True, exist_ok=True)

    with open(log_file, 'w', encoding='utf-8') as f:
        f.write("LOG - RENOMEAR flAtivo -> flExcluido NOS MODELS TYPESCRIPT\n")
        f.write(f"Data: 2025-12-25\n")
        f.write(f"ADR-004: Opcao A - Alinhamento Total com Backend\n")
        f.write("=" * 80 + "\n\n")
        f.write("\n".join(log_lines))
        f.write("\n\n" + "=" * 80 + "\n")
        f.write(f"RESUMO:\n")
        f.write(f"- Arquivos processados: {arquivos_processados}\n")
        f.write(f"- Arquivos alterados: {arquivos_alterados}\n")
        f.write(f"- Total de substituicoes: {total_substituicoes}\n")

    print(f"Log salvo em: {log_file}")

if __name__ == "__main__":
    main()
