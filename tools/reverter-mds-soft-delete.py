#!/usr/bin/env python3
"""
Script para reverter mudanças incorretas de soft delete nos MDs
- Ativo BIT (soft delete) -> FlExcluido BIT
- Corrigir comentarios de semântica

Data: 2025-12-25
Motivo: ADR-004 definiu FlExcluido como padrão de soft delete
"""

import os
import re
from pathlib import Path

# Diretório base
BASE_DIR = Path("d:/IC2/docs/documentacao/Fase-2-Servicos-Essenciais")

# Contadores
arquivos_processados = 0
arquivos_alterados = 0
total_substituicoes = 0

# Log de alterações
log_file = Path("d:/IC2/relatorios/2025-12-25-Reversao-MDs-SoftDelete-Log.txt")
log_lines = []

def processar_md(filepath):
    global arquivos_processados, arquivos_alterados, total_substituicoes

    arquivos_processados += 1

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            conteudo_original = f.read()

        conteudo_novo = conteudo_original
        substituicoes_arquivo = 0

        # 1. DDL: Ativo BIT NOT NULL DEFAULT true -> FlExcluido BIT NOT NULL DEFAULT 0
        conteudo_novo, count = re.subn(
            r'Ativo\s+BIT\s+NOT\s+NULL\s+DEFAULT\s+true',
            r'FlExcluido BIT NOT NULL DEFAULT 0',
            conteudo_novo
        )
        substituicoes_arquivo += count

        # 2. DDL: Ativo BIT NOT NULL DEFAULT 1 -> FlExcluido BIT NOT NULL DEFAULT 0
        conteudo_novo, count = re.subn(
            r'Ativo\s+BIT\s+NOT\s+NULL\s+DEFAULT\s+1',
            r'FlExcluido BIT NOT NULL DEFAULT 0',
            conteudo_novo
        )
        substituicoes_arquivo += count

        # 3. Comentário confuso: true=Ativo, false=Inativo (soft delete) -> Soft delete: false=ativo, true=excluído
        conteudo_novo, count = re.subn(
            r'true=Ativo,\s*false=Inativo\s*\(soft delete\)',
            r'Soft delete: false=ativo, true=excluído',
            conteudo_novo
        )
        substituicoes_arquivo += count

        # 4. Índices: WHERE Ativo = true -> WHERE FlExcluido = 0
        conteudo_novo, count = re.subn(
            r'WHERE\s+Ativo\s*=\s*true',
            r'WHERE FlExcluido = 0',
            conteudo_novo
        )
        substituicoes_arquivo += count

        # 5. Índices: WHERE Ativo = 1 -> WHERE FlExcluido = 0
        conteudo_novo, count = re.subn(
            r'WHERE\s+Ativo\s*=\s*1',
            r'WHERE FlExcluido = 0',
            conteudo_novo
        )
        substituicoes_arquivo += count

        # 6. Comentários em tabelas markdown: | Ativo | BIT | (soft delete context)
        # Padrão: | Ativo | BIT | <qualquer coisa com "soft delete" ou "excluído">
        conteudo_novo, count = re.subn(
            r'\|\s*Ativo\s*\|\s*BIT\s*\|\s*([^|]*(?:soft delete|exclu[íi]do|deletado)[^|]*)\|',
            r'| FlExcluido | BIT | \1|',
            conteudo_novo,
            flags=re.IGNORECASE
        )
        substituicoes_arquivo += count

        # 7. Índices compostos: (FornecedorId, Ativo) -> (ClienteId, FlExcluido)
        conteudo_novo, count = re.subn(
            r'\(ClienteId,\s*Ativo\)',
            r'(ClienteId, FlExcluido)',
            conteudo_novo
        )
        substituicoes_arquivo += count

        # 8. Índices compostos: (EmpresaId, Ativo) -> (EmpresaId, FlExcluido)
        conteudo_novo, count = re.subn(
            r'\(EmpresaId,\s*Ativo\)',
            r'(EmpresaId, FlExcluido)',
            conteudo_novo
        )
        substituicoes_arquivo += count

        # Salvar se houve alterações
        if conteudo_novo != conteudo_original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(conteudo_novo)

            arquivos_alterados += 1
            total_substituicoes += substituicoes_arquivo

            log_msg = f"[OK] {filepath.relative_to(BASE_DIR)}: {substituicoes_arquivo} substituicoes"
            log_lines.append(log_msg)
            print(log_msg)
        else:
            log_msg = f"[SKIP] {filepath.relative_to(BASE_DIR)}: sem alteracoes necessarias"
            log_lines.append(log_msg)

    except Exception as e:
        log_msg = f"[ERROR] {filepath.relative_to(BASE_DIR)}: ERRO - {e}"
        log_lines.append(log_msg)
        print(log_msg)

def main():
    print("=" * 80)
    print("REVERSAO MDs - SOFT DELETE")
    print("ADR-004: Ativo (incorreto) -> FlExcluido (correto)")
    print("=" * 80)
    print()

    # Encontrar todos os MD-*.md na Fase 2
    md_files = list(BASE_DIR.rglob("MD-*.md"))

    print(f"Arquivos MD encontrados: {len(md_files)}")
    print()

    for md_file in md_files:
        processar_md(md_file)

    print()
    print("=" * 80)
    print("RESUMO")
    print("=" * 80)
    print(f"Arquivos processados: {arquivos_processados}")
    print(f"Arquivos alterados: {arquivos_alterados}")
    print(f"Total de substituicoes: {total_substituicoes}")
    print()

    # Salvar log
    log_file.parent.mkdir(parents=True, exist_ok=True)
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write("LOG DE REVERSAO MDs - SOFT DELETE\n")
        f.write(f"Data: 2025-12-25\n")
        f.write(f"ADR-004: FlExcluido e padrao de soft delete\n")
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
