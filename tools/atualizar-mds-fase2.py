#!/usr/bin/env python3
"""
Script para atualizar MDs da Fase 2 conforme ADR-003 e ADR-004
- ADR-003: FornecedorId → ClienteId/EmpresaId
- ADR-004: FlExcluido → Ativo

Data: 2025-12-25
"""

import os
import re
from pathlib import Path

# Diretório base
BASE_DIR = Path("d:/IC2/docs/rf/Fase-2-Servicos-Essenciais")

# Contadores
arquivos_processados = 0
arquivos_alterados = 0
total_substituicoes = 0

# Log de alterações
log_file = Path("d:/IC2/relatorios/2025-12-25-Atualizacao-MDs-Log.txt")
log_lines = []

def processar_md(filepath):
    global arquivos_processados, arquivos_alterados, total_substituicoes

    arquivos_processados += 1

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            conteudo_original = f.read()

        conteudo_novo = conteudo_original
        substituicoes_arquivo = 0

        # ADR-003: FornecedorId → ClienteId (ou EmpresaId conforme contexto)
        # Regra: Manter EmpresaId se já existe, senão usar ClienteId

        # 1. Tabelas de definição (seção de campos)
        # Padrão: | FornecedorId | UNIQUEIDENTIFIER | ...
        if 'EmpresaId' not in conteudo_novo:
            # Se não tem EmpresaId, usar ClienteId
            conteudo_novo, count = re.subn(
                r'(\|\s*)FornecedorId(\s*\|)',
                r'\1ClienteId\2',
                conteudo_novo
            )
            substituicoes_arquivo += count

        # 2. DDL (CREATE TABLE)
        # Padrão: FornecedorId UNIQUEIDENTIFIER
        if 'EmpresaId' not in conteudo_novo:
            conteudo_novo, count = re.subn(
                r'\bFornecedorId\s+(UNIQUEIDENTIFIER|UUID|GUID)',
                r'ClienteId \1',
                conteudo_novo
            )
            substituicoes_arquivo += count

        # 3. Foreign Keys
        # Padrão: FOREIGN KEY (FornecedorId) REFERENCES Fornecedor(Id)
        if 'EmpresaId' not in conteudo_novo:
            conteudo_novo, count = re.subn(
                r'FOREIGN KEY \(FornecedorId\) REFERENCES Fornecedor\(Id\)',
                r'FOREIGN KEY (ClienteId) REFERENCES Cliente(Id)',
                conteudo_novo
            )
            substituicoes_arquivo += count

            conteudo_novo, count = re.subn(
                r'FK para Fornecedor',
                r'FK para Cliente (multi-tenancy raiz)',
                conteudo_novo
            )
            substituicoes_arquivo += count

        # 4. Comentários e descrições
        if 'EmpresaId' not in conteudo_novo:
            conteudo_novo, count = re.subn(
                r'Fornecedor \(multi-tenancy\)',
                r'Cliente (multi-tenancy raiz)',
                conteudo_novo
            )
            substituicoes_arquivo += count

        # ADR-004: FlExcluido → Ativo (inverter lógica)

        # 1. Definições de campos
        # Padrão: | FlExcluido | BIT | NÃO | 0 | Soft delete |
        conteudo_novo, count = re.subn(
            r'(\|\s*)FlExcluido(\s*\|\s*BIT\s*\|\s*NÃO\s*\|\s*)0(\s*\|\s*Soft delete)',
            r'\1Ativo\2true\3',
            conteudo_novo
        )
        substituicoes_arquivo += count

        # 2. DDL
        # Padrão: FlExcluido BIT NOT NULL DEFAULT 0
        conteudo_novo, count = re.subn(
            r'\bFlExcluido\s+BIT\s+(NOT\s+NULL\s+)?DEFAULT\s+0',
            r'Ativo BIT \1DEFAULT true',
            conteudo_novo
        )
        substituicoes_arquivo += count

        # 3. Comentários
        conteudo_novo, count = re.subn(
            r'Soft delete',
            r'true=Ativo, false=Inativo (soft delete)',
            conteudo_novo
        )
        substituicoes_arquivo += count

        # 4. WHERE clauses
        conteudo_novo, count = re.subn(
            r'WHERE FlExcluido = 0',
            r'WHERE Ativo = true',
            conteudo_novo
        )
        substituicoes_arquivo += count

        # 5. Índices
        conteudo_novo, count = re.subn(
            r'(\w+), FlExcluido\)',
            r'\1, Ativo)',
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
            print(log_msg)

    except Exception as e:
        log_msg = f"[ERROR] {filepath.relative_to(BASE_DIR)}: ERRO - {e}"
        log_lines.append(log_msg)
        print(log_msg)

def main():
    print("=" * 80)
    print("ATUALIZACAO DE MDs DA FASE 2")
    print("ADR-003: FornecedorId -> ClienteId/EmpresaId")
    print("ADR-004: FlExcluido -> Ativo")
    print("=" * 80)
    print()

    # Encontrar todos os MD-*.md na Fase 2
    md_files = sorted(BASE_DIR.rglob("MD-*.md"))

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
    print(f"Total de substituições: {total_substituicoes}")
    print()

    # Salvar log
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write("LOG DE ATUALIZAÇÃO DE MDs - FASE 2\n")
        f.write(f"Data: 2025-12-25\n")
        f.write(f"ADR-003: FornecedorId → ClienteId/EmpresaId\n")
        f.write(f"ADR-004: FlExcluido → Ativo\n")
        f.write("=" * 80 + "\n\n")
        f.write("\n".join(log_lines))
        f.write("\n\n" + "=" * 80 + "\n")
        f.write(f"RESUMO:\n")
        f.write(f"- Arquivos processados: {arquivos_processados}\n")
        f.write(f"- Arquivos alterados: {arquivos_alterados}\n")
        f.write(f"- Total de substituições: {total_substituicoes}\n")

    print(f"Log salvo em: {log_file}")

if __name__ == "__main__":
    main()
