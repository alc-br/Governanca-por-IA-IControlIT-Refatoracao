#!/usr/bin/env python3
"""
Script para adicionar FlExcluido nas entidades que usam apenas Ativo
Opcao A: Manter Ativo como flag funcional + adicionar FlExcluido para soft delete

Data: 2025-12-25
ADR-004: Soft Delete com FlExcluido
"""

import os
import re
from pathlib import Path

# Diretório base
ENTITIES_DIR = Path("d:/IC2/backend/IControlIT.API/src/Domain/Entities")

# Lista das 39 entidades que precisam de FlExcluido
ENTIDADES_ALVO = [
    "Andar.cs", "AprovacaoDelegacao.cs", "Contrato.cs", "ContratoAditivo.cs",
    "ContratoFatura.cs", "ContratoFaturaItem.cs", "ContratoIndice.cs",
    "ContratoSLAOperacao.cs", "ContratoSLAServico.cs", "ContratoStatus.cs",
    "Edificio.cs", "EmailTemplate.cs", "Empresa.cs", "Endereco.cs",
    "EnderecoEntrega.cs", "EnderecoEntregaTipo.cs", "IntegracaoConfiguracao.cs",
    "IntegracaoEndpoint.cs", "NotificacaoDispositivo.cs", "NotificacaoTemplate.cs",
    "Permission.cs", "PlanoContas.cs", "Rack.cs", "RateioItem.cs",
    "ReportTemplate.cs", "Role.cs", "Sala.cs", "SistemaLogConfiguracaoAlerta.cs",
    "SistemaLogConfiguracaoRetention.cs", "SistemaLogMetricaCustomizada.cs",
    "SistemaParametro.cs", "SistemaParametroCategoria.cs", "Solicitacao.cs",
    "SolicitacaoFila.cs", "SolicitacaoFilaAtendimento.cs", "SolicitacaoTipo.cs",
    "Usuario.cs", "Volumetria.cs", "WorkflowAprovacaoTemplate.cs"
]

# Contadores
arquivos_processados = 0
arquivos_alterados = 0
arquivos_com_erro = 0

# Log
log_file = Path("d:/IC2/relatorios/2025-12-25-Adicionar-FlExcluido-Log.txt")
log_lines = []

def adicionar_flexcluido(filepath):
    """Adiciona propriedade FlExcluido após o campo Ativo"""
    global arquivos_processados, arquivos_alterados, arquivos_com_erro

    arquivos_processados += 1
    nome_arquivo = filepath.name

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            linhas = f.readlines()

        # Procurar a linha que contém "public bool Ativo"
        indice_ativo = -1
        for i, linha in enumerate(linhas):
            if re.search(r'public\s+bool\s+Ativo\s*\{', linha):
                indice_ativo = i
                break

        if indice_ativo == -1:
            log_msg = f"[WARN] {nome_arquivo}: Campo 'Ativo' nao encontrado"
            log_lines.append(log_msg)
            print(log_msg)
            return

        # Verificar se já tem FlExcluido (não deveria ter)
        conteudo_completo = ''.join(linhas)
        if 'FlExcluido' in conteudo_completo:
            log_msg = f"[SKIP] {nome_arquivo}: Ja possui FlExcluido"
            log_lines.append(log_msg)
            print(log_msg)
            return

        # Encontrar o fechamento da propriedade Ativo (linha com "}")
        # E adicionar FlExcluido logo após
        indice_insercao = indice_ativo + 1

        # Verificar se há comentário XML antes de Ativo
        tem_xml_comment = False
        if indice_ativo > 0 and '///' in linhas[indice_ativo - 1]:
            tem_xml_comment = True

        # Preparar linhas para inserir
        novas_linhas = []

        # Adicionar linha em branco
        novas_linhas.append('\n')

        # Adicionar comentário XML
        novas_linhas.append('    /// <summary>\n')
        novas_linhas.append('    /// Soft delete: false=ativo (nao deletado), true=excluido (deletado)\n')
        novas_linhas.append('    /// </summary>\n')

        # Adicionar propriedade FlExcluido
        novas_linhas.append('    public bool FlExcluido { get; set; } = false;\n')

        # Inserir as novas linhas
        linhas[indice_insercao:indice_insercao] = novas_linhas

        # Salvar arquivo
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(linhas)

        arquivos_alterados += 1
        log_msg = f"[OK] {nome_arquivo}: FlExcluido adicionado apos linha {indice_ativo + 1}"
        log_lines.append(log_msg)
        print(log_msg)

    except Exception as e:
        arquivos_com_erro += 1
        log_msg = f"[ERROR] {nome_arquivo}: {e}"
        log_lines.append(log_msg)
        print(log_msg)

def main():
    print("=" * 80)
    print("ADICIONAR FlExcluido NAS ENTIDADES")
    print("ADR-004: Opcao A - Manter Ativo como flag funcional")
    print("=" * 80)
    print()

    print(f"Entidades alvo: {len(ENTIDADES_ALVO)}")
    print()

    for entity_name in ENTIDADES_ALVO:
        filepath = ENTITIES_DIR / entity_name
        if filepath.exists():
            adicionar_flexcluido(filepath)
        else:
            log_msg = f"[WARN] {entity_name}: Arquivo nao encontrado"
            log_lines.append(log_msg)
            print(log_msg)

    print()
    print("=" * 80)
    print("RESUMO")
    print("=" * 80)
    print(f"Arquivos processados: {arquivos_processados}")
    print(f"Arquivos alterados: {arquivos_alterados}")
    print(f"Arquivos com erro: {arquivos_com_erro}")
    print()

    # Salvar log
    log_file.parent.mkdir(parents=True, exist_ok=True)
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write("LOG - ADICIONAR FlExcluido NAS ENTIDADES\n")
        f.write(f"Data: 2025-12-25\n")
        f.write(f"ADR-004: Opcao A - Manter Ativo como flag funcional\n")
        f.write("=" * 80 + "\n\n")
        f.write("\n".join(log_lines))
        f.write("\n\n" + "=" * 80 + "\n")
        f.write(f"RESUMO:\n")
        f.write(f"- Arquivos processados: {arquivos_processados}\n")
        f.write(f"- Arquivos alterados: {arquivos_alterados}\n")
        f.write(f"- Arquivos com erro: {arquivos_com_erro}\n")

    print(f"Log salvo em: {log_file}")
    print()
    print("PROXIMOS PASSOS:")
    print("1. Compilar backend: cd backend/IControlIT.API && dotnet build")
    print("2. Criar migration: dotnet ef migrations add AdicionarFlExcluidoSoftDelete")
    print("3. Atualizar queries, validators, DTOs")

if __name__ == "__main__":
    main()
