#!/usr/bin/env python3
"""
Script para renomear flAtivo → flExcluido em services, components e templates
Conforme ADR-004: Soft Delete com FlExcluido (Opção A)

Data: 2025-12-25
"""

import os
import re
from pathlib import Path

# Diretório base do frontend
FRONTEND_DIR = Path("d:/IC2/frontend/icontrolit-app/src")

# Contadores
arquivos_processados = 0
arquivos_alterados = 0
total_substituicoes = 0

# Log de alterações
log_lines = []

def renomear_flatvo_flexcluido_arquivo(filepath):
    """Renomeia flAtivo para flExcluido em arquivo TypeScript ou HTML"""
    global arquivos_processados, arquivos_alterados, total_substituicoes

    arquivos_processados += 1

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            conteudo_original = f.read()

        # Verificar se tem flAtivo
        if 'flAtivo' not in conteudo_original:
            return

        conteudo_novo = conteudo_original
        substituicoes_arquivo = 0

        # 1. Renomear propriedades em interfaces/types: flAtivo: boolean
        conteudo_novo, count = re.subn(
            r'\bflAtivo\s*:\s*boolean',
            r'flExcluido: boolean',
            conteudo_novo
        )
        substituicoes_arquivo += count

        # 2. Renomear acesso a propriedade: objeto.flAtivo
        conteudo_novo, count = re.subn(
            r'\.flAtivo\b',
            r'.flExcluido',
            conteudo_novo
        )
        substituicoes_arquivo += count

        # 3. Renomear parâmetros de função: flAtivo: boolean
        conteudo_novo, count = re.subn(
            r'\(flAtivo:\s*boolean\)',
            r'(flExcluido: boolean)',
            conteudo_novo
        )
        substituicoes_arquivo += count

        # 4. Renomear em mat-sort-header: mat-sort-header="flAtivo"
        conteudo_novo, count = re.subn(
            r'mat-sort-header="flAtivo"',
            r'mat-sort-header="flExcluido"',
            conteudo_novo
        )
        substituicoes_arquivo += count

        # 5. Renomear em matColumnDef: matColumnDef="flAtivo"
        conteudo_novo, count = re.subn(
            r'matColumnDef="flAtivo"',
            r'matColumnDef="flExcluido"',
            conteudo_novo
        )
        substituicoes_arquivo += count

        # 6. Renomear em FormControls: flAtivo: [valor]
        conteudo_novo, count = re.subn(
            r'\bflAtivo:\s*\[',
            r'flExcluido: [',
            conteudo_novo
        )
        substituicoes_arquivo += count

        # 7. Renomear em desestruturação/atribuição: { flAtivo }
        conteudo_novo, count = re.subn(
            r'\{\s*flAtivo\s*\}',
            r'{ flExcluido }',
            conteudo_novo
        )
        substituicoes_arquivo += count

        # 8. Renomear em comentários/strings que referenciem o campo
        # (preservar comentários explicativos sobre semântica)

        # Salvar se houve alterações
        if conteudo_novo != conteudo_original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(conteudo_novo)

            arquivos_alterados += 1
            total_substituicoes += substituicoes_arquivo

            log_msg = f"[OK] {filepath.relative_to(FRONTEND_DIR)}: {substituicoes_arquivo} substituicoes"
            log_lines.append(log_msg)
            print(log_msg)

    except Exception as e:
        log_msg = f"[ERROR] {filepath.relative_to(FRONTEND_DIR)}: {e}"
        log_lines.append(log_msg)
        print(log_msg)

def main():
    print("=" * 80)
    print("RENOMEAR flAtivo -> flExcluido EM SERVICES, COMPONENTS E TEMPLATES")
    print("ADR-004: Opcao A - Alinhamento Total com Backend")
    print("=" * 80)
    print()

    # Processar arquivos TypeScript (.ts) e HTML (.html)
    tipos_arquivos = ["**/*.ts", "**/*.html"]

    for pattern in tipos_arquivos:
        for filepath in FRONTEND_DIR.glob(pattern):
            # Ignorar arquivos da pasta node_modules
            if 'node_modules' in str(filepath):
                continue

            renomear_flatvo_flexcluido_arquivo(filepath)

    print()
    print("=" * 80)
    print("RESUMO")
    print("=" * 80)
    print(f"Arquivos processados: {arquivos_processados}")
    print(f"Arquivos alterados: {arquivos_alterados}")
    print(f"Total de substituicoes: {total_substituicoes}")
    print()

    # Salvar log
    log_file = Path("d:/IC2/relatorios/2025-12-25-Renomear-FlAtivo-Services-Components-Log.txt")
    log_file.parent.mkdir(parents=True, exist_ok=True)

    with open(log_file, 'w', encoding='utf-8') as f:
        f.write("LOG - RENOMEAR flAtivo -> flExcluido EM SERVICES/COMPONENTS/TEMPLATES\n")
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
