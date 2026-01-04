#!/usr/bin/env python3
"""
Script para padronizar soft delete no backend conforme ADR-004
- Renomear FlExcluido -> Ativo
- Inverter lógica (false -> true)
- Atualizar comentários

Data: 2025-12-25
"""

import os
import re
from pathlib import Path

# Diretório base
ENTITIES_DIR = Path("d:/IC2/backend/IControlIT.API/src/Domain/Entities")

# Entidades com FlExcluido
ENTITIES_WITH_FLEXCLUIDO = [
    "Ativo.cs", "Categoria.cs", "CategoriaAtributo.cs", "CategoriaTemplate.cs",
    "ChipSIMEstoque.cs", "Cliente.cs", "EntityStatus.cs", "EntityType.cs",
    "Fornecedor.cs", "LinhaTelefonica.cs", "MenuHardcodedReferencia.cs",
    "PlanoTarifario.cs", "Servico.cs", "SistemaCategoria.cs",
    "SistemaConfiguracao.cs", "SistemaConfiguracaoCategoria.cs",
    "SistemaConfiguracaoDependencia.cs", "SistemaFeatureFlag.cs",
    "SistemaFeatureFlagAvancado.cs", "SistemaFuncionalidade.cs",
    "SistemaFuncionalidadeAcao.cs", "SolicitacaoLinha.cs"
]

# Contadores
arquivos_processados = 0
arquivos_alterados = 0
total_substituicoes = 0

# Log de alterações
log_file = Path("d:/IC2/relatorios/2025-12-25-Refatoracao-Backend-SoftDelete-Log.txt")
log_lines = []

def refatorar_entidade(filepath):
    global arquivos_processados, arquivos_alterados, total_substituicoes

    arquivos_processados += 1

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            conteudo_original = f.read()

        conteudo_novo = conteudo_original
        substituicoes_arquivo = 0

        # 1. Propriedade FlExcluido -> Ativo
        # Padrão: public bool FlExcluido { get; set; } = false;
        conteudo_novo, count = re.subn(
            r'public\s+bool\s+FlExcluido\s*\{\s*get;\s*set;\s*\}\s*=\s*false;',
            r'public bool Ativo { get; set; } = true;',
            conteudo_novo
        )
        substituicoes_arquivo += count

        # Caso sem default
        conteudo_novo, count = re.subn(
            r'public\s+bool\s+FlExcluido\s*\{\s*get;\s*set;\s*\}',
            r'public bool Ativo { get; set; }',
            conteudo_novo
        )
        substituicoes_arquivo += count

        # 2. XML Doc Comments
        # /// <summary>
        # /// Soft delete...
        # /// </summary>
        conteudo_novo, count = re.subn(
            r'///\s*Soft delete.*FlExcluido.*',
            r'/// true=Ativo, false=Inativo (soft delete)',
            conteudo_novo
        )
        substituicoes_arquivo += count

        # 3. Comentários inline
        conteudo_novo, count = re.subn(
            r'//\s*Soft delete.*',
            r'// true=Ativo, false=Inativo',
            conteudo_novo
        )
        substituicoes_arquivo += count

        # 4. Outros comentários com FlExcluido
        conteudo_novo, count = re.subn(
            r'FlExcluido',
            r'Ativo',
            conteudo_novo
        )
        substituicoes_arquivo += count

        # 5. Métodos que usam FlExcluido (se houver)
        # Exemplo: IsAtivo() => !FlExcluido  ->  IsAtivo() => Ativo
        conteudo_novo, count = re.subn(
            r'!\s*FlExcluido',
            r'Ativo',
            conteudo_novo
        )
        substituicoes_arquivo += count

        # Salvar se houve alterações
        if conteudo_novo != conteudo_original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(conteudo_novo)

            arquivos_alterados += 1
            total_substituicoes += substituicoes_arquivo

            log_msg = f"[OK] {filepath.name}: {substituicoes_arquivo} substituicoes"
            log_lines.append(log_msg)
            print(log_msg)
        else:
            log_msg = f"[SKIP] {filepath.name}: sem alteracoes necessarias"
            log_lines.append(log_msg)
            print(log_msg)

    except Exception as e:
        log_msg = f"[ERROR] {filepath.name}: ERRO - {e}"
        log_lines.append(log_msg)
        print(log_msg)

def main():
    print("=" * 80)
    print("REFATORACAO BACKEND - SOFT DELETE")
    print("ADR-004: FlExcluido -> Ativo")
    print("=" * 80)
    print()

    print(f"Entidades a processar: {len(ENTITIES_WITH_FLEXCLUIDO)}")
    print()

    for entity_file in ENTITIES_WITH_FLEXCLUIDO:
        filepath = ENTITIES_DIR / entity_file
        if filepath.exists():
            refatorar_entidade(filepath)
        else:
            log_msg = f"[WARN] {entity_file}: arquivo nao encontrado"
            log_lines.append(log_msg)
            print(log_msg)

    print()
    print("=" * 80)
    print("RESUMO")
    print("=" * 80)
    print(f"Arquivos processados: {arquivos_processados}")
    print(f"Arquivos alterados: {arquivos_alterados}")
    print(f"Total de substituicoes: {total_substituicoes}")
    print()

    # Salvar log
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write("LOG DE REFATORACAO BACKEND - SOFT DELETE\n")
        f.write(f"Data: 2025-12-25\n")
        f.write(f"ADR-004: FlExcluido -> Ativo\n")
        f.write("=" * 80 + "\n\n")
        f.write("\n".join(log_lines))
        f.write("\n\n" + "=" * 80 + "\n")
        f.write(f"RESUMO:\n")
        f.write(f"- Arquivos processados: {arquivos_processados}\n")
        f.write(f"- Arquivos alterados: {arquivos_alterados}\n")
        f.write(f"- Total de substituicoes: {total_substituicoes}\n")

    print(f"Log salvo em: {log_file}")

    # Próximos passos
    print()
    print("=" * 80)
    print("PROXIMOS PASSOS")
    print("=" * 80)
    print("1. Compilar backend: dotnet build")
    print("2. Criar migration: dotnet ef migrations add PadronizarSoftDeleteAtivo")
    print("3. Atualizar queries, validators, DTOs que usam FlExcluido")
    print("4. Executar testes de regressao")

if __name__ == "__main__":
    main()
