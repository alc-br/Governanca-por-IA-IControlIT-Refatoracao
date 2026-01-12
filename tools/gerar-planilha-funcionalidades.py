#!/usr/bin/env python3
"""
gerar-planilha-funcionalidades.py

Gera planilha consolidada de funcionalidades (RFs) do sistema.

COLUNAS:
- Cód. Funcionalidade (ex: RF006)
- Nome Funcionalidade
- Descrição (sucinta)
- Regras (parágrafo único, linguagem simples)
- Notas (vazio para anotações posteriores)

OUTPUT: D:\\IC2_Governanca\\funcionalidades.xlsx

AUTOR: Agência ALC - alc.dev.br
DATA: 2026-01-11
"""

import os
import sys
import yaml
import glob
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def extrair_rfs_yaml(documentacao_path):
    """
    Extrai todos os RFs dos arquivos YAML na estrutura de documentação.

    Returns:
        list: Lista de dicts com dados dos RFs
    """
    rfs = []

    # Buscar todos os arquivos RF*.yaml (não RL-RF*.yaml)
    pattern = os.path.join(documentacao_path, "**", "RF*.yaml")
    arquivos = glob.glob(pattern, recursive=True)

    for arquivo in arquivos:
        # Ignorar RL-RF*.yaml (Regras de Lógica)
        if os.path.basename(arquivo).startswith("RL-"):
            continue

        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                dados = yaml.safe_load(f)

            if not dados:
                continue

            # Extrair código do RF
            rf_id = dados.get('rf_id', '')
            if not rf_id:
                # Tentar extrair do nome do arquivo
                rf_id = os.path.basename(arquivo).replace('.yaml', '')

            # Extrair nome/título
            nome = dados.get('titulo', dados.get('nome', dados.get('title', '')))

            # Extrair descrição
            descricao = dados.get('descricao', dados.get('description', ''))

            # Se descricao é um dicionário, extrair campo objetivo ou problema_resolvido
            if isinstance(descricao, dict):
                descricao = descricao.get('objetivo', descricao.get('problema_resolvido', ''))

            if not descricao:
                # Tentar pegar objetivo diretamente
                objetivo = dados.get('objetivo', dados.get('objective', ''))
                if isinstance(objetivo, dict):
                    descricao = objetivo.get('texto', str(objetivo))
                else:
                    descricao = objetivo

            # Garantir que descricao é string
            if isinstance(descricao, dict):
                descricao = str(descricao)
            elif not isinstance(descricao, str):
                descricao = str(descricao) if descricao else ''

            # Extrair regras de negócio
            regras = []
            if 'regras_negocio' in dados:
                rns = dados['regras_negocio']
                if isinstance(rns, list):
                    for rn in rns:
                        if isinstance(rn, dict):
                            titulo_rn = rn.get('titulo', rn.get('descricao', ''))
                            if titulo_rn:
                                regras.append(titulo_rn)
                        elif isinstance(rn, str):
                            regras.append(rn)

            # Se não encontrou regras, tentar em RL-RF*.yaml correspondente
            if not regras:
                rl_arquivo = arquivo.replace(f"{rf_id}.yaml", f"RL-{rf_id}.yaml")
                if os.path.exists(rl_arquivo):
                    try:
                        with open(rl_arquivo, 'r', encoding='utf-8') as f:
                            rl_dados = yaml.safe_load(f)

                        if rl_dados and 'regras_negocio' in rl_dados:
                            rns = rl_dados['regras_negocio']
                            if isinstance(rns, list):
                                for rn in rns:
                                    if isinstance(rn, dict):
                                        titulo_rn = rn.get('titulo', rn.get('descricao', ''))
                                        if titulo_rn:
                                            regras.append(titulo_rn)
                    except:
                        pass

            # Formatar regras em parágrafo único
            regras_texto = ". ".join(regras) if regras else "Sem regras documentadas"
            if regras_texto and not regras_texto.endswith('.'):
                regras_texto += '.'

            # Adicionar RF à lista
            rfs.append({
                'codigo': rf_id,
                'nome': nome,
                'descricao': descricao,
                'regras': regras_texto,
                'notas': ''
            })

        except Exception as e:
            print(f"AVISO: Erro ao processar {arquivo}: {e}")
            continue

    # Ordenar por código
    rfs.sort(key=lambda x: x['codigo'])

    return rfs

def gerar_planilha_excel(rfs, output_path):
    """
    Gera planilha Excel com formatação profissional.

    Args:
        rfs: Lista de RFs extraídos
        output_path: Caminho do arquivo de saída
    """
    wb = Workbook()
    ws = wb.active
    ws.title = "Funcionalidades"

    # Cores
    cor_cabecalho = "366092"  # Azul escuro
    cor_texto_branco = "FFFFFF"

    # Estilos
    fonte_cabecalho = Font(name='Calibri', size=11, bold=True, color=cor_texto_branco)
    fonte_dados = Font(name='Calibri', size=10)

    preenchimento_cabecalho = PatternFill(start_color=cor_cabecalho,
                                          end_color=cor_cabecalho,
                                          fill_type="solid")

    alinhamento_cabecalho = Alignment(horizontal='center',
                                     vertical='center',
                                     wrap_text=True)

    alinhamento_dados = Alignment(horizontal='left',
                                  vertical='top',
                                  wrap_text=True)

    borda = Border(left=Side(style='thin', color='000000'),
                   right=Side(style='thin', color='000000'),
                   top=Side(style='thin', color='000000'),
                   bottom=Side(style='thin', color='000000'))

    # Cabeçalhos
    cabecalhos = [
        'Cód. Funcionalidade',
        'Nome Funcionalidade',
        'Descrição',
        'Regras',
        'Notas'
    ]

    for col, cabecalho in enumerate(cabecalhos, 1):
        celula = ws.cell(row=1, column=col, value=cabecalho)
        celula.font = fonte_cabecalho
        celula.fill = preenchimento_cabecalho
        celula.alignment = alinhamento_cabecalho
        celula.border = borda

    # Altura da linha do cabeçalho
    ws.row_dimensions[1].height = 30

    # Dados
    for row_idx, rf in enumerate(rfs, 2):
        # Cód. Funcionalidade
        celula = ws.cell(row=row_idx, column=1, value=rf['codigo'])
        celula.font = Font(name='Calibri', size=10, bold=True)
        celula.alignment = Alignment(horizontal='center', vertical='center')
        celula.border = borda

        # Nome Funcionalidade
        celula = ws.cell(row=row_idx, column=2, value=rf['nome'])
        celula.font = fonte_dados
        celula.alignment = alinhamento_dados
        celula.border = borda

        # Descrição
        celula = ws.cell(row=row_idx, column=3, value=rf['descricao'])
        celula.font = fonte_dados
        celula.alignment = alinhamento_dados
        celula.border = borda

        # Regras
        celula = ws.cell(row=row_idx, column=4, value=rf['regras'])
        celula.font = fonte_dados
        celula.alignment = alinhamento_dados
        celula.border = borda

        # Notas (vazio)
        celula = ws.cell(row=row_idx, column=5, value=rf['notas'])
        celula.font = fonte_dados
        celula.alignment = alinhamento_dados
        celula.border = borda

        # Altura da linha (auto-ajuste baseado em conteúdo)
        ws.row_dimensions[row_idx].height = 40

    # Larguras das colunas
    ws.column_dimensions['A'].width = 18  # Cód. Funcionalidade
    ws.column_dimensions['B'].width = 40  # Nome Funcionalidade
    ws.column_dimensions['C'].width = 60  # Descrição
    ws.column_dimensions['D'].width = 80  # Regras
    ws.column_dimensions['E'].width = 30  # Notas

    # Congelar primeira linha (cabeçalho)
    ws.freeze_panes = 'A2'

    # Filtro automático
    ws.auto_filter.ref = f"A1:E{len(rfs) + 1}"

    # Salvar
    wb.save(output_path)
    print(f"\n[OK] Planilha gerada com sucesso: {output_path}")
    print(f"[INFO] Total de funcionalidades: {len(rfs)}")

def main():
    print("=" * 80)
    print("GERADOR DE PLANILHA DE FUNCIONALIDADES")
    print("=" * 80)
    print()

    documentacao_path = r"D:\IC2_Governanca\documentacao"
    output_path = r"D:\IC2_Governanca\funcionalidades.xlsx"

    if not os.path.exists(documentacao_path):
        print(f"[ERRO] ERRO: Diretório de documentação não encontrado: {documentacao_path}")
        sys.exit(1)

    print(f"[INFO] Lendo RFs de: {documentacao_path}")
    print()

    # Extrair RFs
    rfs = extrair_rfs_yaml(documentacao_path)

    if not rfs:
        print("[ERRO] ERRO: Nenhum RF encontrado!")
        sys.exit(1)

    print(f"[OK] {len(rfs)} RFs extraídos")
    print()

    # Gerar planilha
    print("[INFO] Gerando planilha Excel...")
    gerar_planilha_excel(rfs, output_path)
    print()

    # Estatísticas
    print("=" * 80)
    print("ESTATÍSTICAS")
    print("=" * 80)
    print(f"Total de RFs: {len(rfs)}")
    print(f"RFs com descrição: {sum(1 for rf in rfs if rf['descricao'])}")
    print(f"RFs com regras: {sum(1 for rf in rfs if rf['regras'] != 'Sem regras documentadas')}")
    print()

    # Primeiros 5 RFs como amostra
    print("AMOSTRA (5 primeiros RFs):")
    print("-" * 80)
    for rf in rfs[:5]:
        print(f"  {rf['codigo']}: {rf['nome']}")
    print()

    print("=" * 80)
    print("[OK] CONCLUÍDO")
    print("=" * 80)

if __name__ == '__main__':
    main()
