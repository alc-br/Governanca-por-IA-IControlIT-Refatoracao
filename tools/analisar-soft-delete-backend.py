#!/usr/bin/env python3
"""
Script para analisar uso de soft delete em entidades backend
Identifica:
- Entidades com APENAS Ativo (precisam FlExcluido)
- Entidades com APENAS FlExcluido (OK)
- Entidades com AMBOS (verificar semântica)
- Entidades sem nenhum (verificar necessidade)

Data: 2025-12-25
"""

import os
import re
from pathlib import Path

# Diretório base
ENTITIES_DIR = Path("d:/IC2/backend/IControlIT.API/src/Domain/Entities")

# Categorias
apenas_ativo = []
apenas_flexcluido = []
ambos = []
nenhum = []

def analisar_entidade(filepath):
    """Analisa uma entidade para identificar campos de soft delete"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            conteudo = f.read()

        # Procurar propriedades
        tem_ativo = bool(re.search(r'public\s+bool\s+Ativo\s*\{', conteudo))
        tem_flexcluido = bool(re.search(r'public\s+bool\s+FlExcluido\s*\{', conteudo))

        nome_arquivo = filepath.name

        if tem_ativo and tem_flexcluido:
            ambos.append(nome_arquivo)
        elif tem_ativo and not tem_flexcluido:
            apenas_ativo.append(nome_arquivo)
        elif not tem_ativo and tem_flexcluido:
            apenas_flexcluido.append(nome_arquivo)
        else:
            nenhum.append(nome_arquivo)

    except Exception as e:
        print(f"[ERROR] {filepath.name}: {e}")

def main():
    print("=" * 80)
    print("ANALISE SOFT DELETE - ENTIDADES BACKEND")
    print("=" * 80)
    print()

    # Processar todas as entidades .cs
    for entity_file in ENTITIES_DIR.glob("*.cs"):
        # Ignorar classes base
        if entity_file.name.startswith("Base"):
            continue
        analisar_entidade(entity_file)

    # Ordenar listas
    apenas_ativo.sort()
    apenas_flexcluido.sort()
    ambos.sort()
    nenhum.sort()

    # Exibir resultados
    print(f"Total de entidades analisadas: {len(apenas_ativo) + len(apenas_flexcluido) + len(ambos) + len(nenhum)}")
    print()

    print("=" * 80)
    print("1. ENTIDADES COM APENAS 'Ativo' (PRECISAM ADICIONAR FlExcluido)")
    print("=" * 80)
    print(f"Total: {len(apenas_ativo)}")
    print()
    for entidade in apenas_ativo:
        print(f"  - {entidade}")
    print()

    print("=" * 80)
    print("2. ENTIDADES COM APENAS 'FlExcluido' (OK - PADRAO CORRETO)")
    print("=" * 80)
    print(f"Total: {len(apenas_flexcluido)}")
    print()
    for entidade in apenas_flexcluido:
        print(f"  - {entidade}")
    print()

    print("=" * 80)
    print("3. ENTIDADES COM AMBOS 'Ativo' E 'FlExcluido' (VERIFICAR SEMANTICA)")
    print("=" * 80)
    print(f"Total: {len(ambos)}")
    print()
    for entidade in ambos:
        print(f"  - {entidade}")
    print()

    print("=" * 80)
    print("4. ENTIDADES SEM NENHUM (VERIFICAR NECESSIDADE)")
    print("=" * 80)
    print(f"Total: {len(nenhum)}")
    print()
    for entidade in nenhum:
        print(f"  - {entidade}")
    print()

    # Salvar relatório
    relatorio_file = Path("d:/IC2/relatorios/2025-12-25-Analise-SoftDelete-Backend.md")
    relatorio_file.parent.mkdir(parents=True, exist_ok=True)

    with open(relatorio_file, 'w', encoding='utf-8') as f:
        f.write("# Analise de Soft Delete - Entidades Backend\n\n")
        f.write("**Data:** 2025-12-25\n")
        f.write("**Objetivo:** Identificar entidades que precisam adicionar FlExcluido conforme ADR-004\n\n")
        f.write("---\n\n")

        f.write(f"## Resumo\n\n")
        f.write(f"- **Total de entidades:** {len(apenas_ativo) + len(apenas_flexcluido) + len(ambos) + len(nenhum)}\n")
        f.write(f"- **Apenas Ativo (precisam FlExcluido):** {len(apenas_ativo)}\n")
        f.write(f"- **Apenas FlExcluido (OK):** {len(apenas_flexcluido)}\n")
        f.write(f"- **Ambos (verificar):** {len(ambos)}\n")
        f.write(f"- **Nenhum:** {len(nenhum)}\n\n")

        f.write("---\n\n")
        f.write("## 1. Entidades com APENAS 'Ativo' (PRECISAM ADICIONAR FlExcluido)\n\n")
        f.write(f"Total: {len(apenas_ativo)}\n\n")
        for entidade in apenas_ativo:
            f.write(f"- [ ] {entidade}\n")
        f.write("\n")

        f.write("---\n\n")
        f.write("## 2. Entidades com APENAS 'FlExcluido' (OK - PADRAO CORRETO)\n\n")
        f.write(f"Total: {len(apenas_flexcluido)}\n\n")
        for entidade in apenas_flexcluido:
            f.write(f"- [x] {entidade}\n")
        f.write("\n")

        f.write("---\n\n")
        f.write("## 3. Entidades com AMBOS 'Ativo' E 'FlExcluido' (VERIFICAR SEMANTICA)\n\n")
        f.write(f"Total: {len(ambos)}\n\n")
        f.write("Estas entidades usam:\n")
        f.write("- `Ativo`: Flag funcional (habilitado/desabilitado)\n")
        f.write("- `FlExcluido`: Soft delete (deletado/nao deletado)\n\n")
        f.write("Status: OK se semântica estiver correta\n\n")
        for entidade in ambos:
            f.write(f"- [ ] {entidade} - verificar comentarios/semantica\n")
        f.write("\n")

        f.write("---\n\n")
        f.write("## 4. Entidades SEM NENHUM (VERIFICAR NECESSIDADE)\n\n")
        f.write(f"Total: {len(nenhum)}\n\n")
        f.write("Estas entidades podem:\n")
        f.write("- Nao precisar de soft delete (entidades de configuracao imutaveis)\n")
        f.write("- Precisar de soft delete mas falta implementar\n\n")
        for entidade in nenhum:
            f.write(f"- [ ] {entidade}\n")
        f.write("\n")

        f.write("---\n\n")
        f.write("## Proximos Passos\n\n")
        f.write("1. Adicionar `FlExcluido` nas entidades da Categoria 1\n")
        f.write("2. Verificar semantica das entidades da Categoria 3\n")
        f.write("3. Criar migration para adicionar coluna FlExcluido\n")
        f.write("4. Atualizar queries, validators, DTOs\n")
        f.write("5. Executar testes de regressao\n")

    print(f"Relatorio salvo em: {relatorio_file}")

if __name__ == "__main__":
    main()
