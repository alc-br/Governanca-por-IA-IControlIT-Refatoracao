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
DATA: 2026-01-12
VERSÃO: 2.0
"""

import os
import sys
import yaml
import glob
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def extrair_texto(valor):
    """
    Extrai texto de uma estrutura YAML que pode ser string, dict ou outro tipo.

    Args:
        valor: Valor a extrair (string, dict, list, etc)

    Returns:
        str: Texto extraído ou vazio
    """
    if not valor:
        return ''

    if isinstance(valor, str):
        return valor.strip()

    if isinstance(valor, dict):
        # Tenta campos comuns
        for campo in ['objetivo', 'problema_resolvido', 'descricao', 'texto', 'resumo']:
            if campo in valor and valor[campo]:
                return extrair_texto(valor[campo])
        # Se não encontrou, converte dict para string legível
        return str(valor)

    if isinstance(valor, list):
        # Junta itens da lista
        return '. '.join(str(item) for item in valor if item)

    return str(valor)

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
                # Tentar extrair de estrutura aninhada rf.id
                if 'rf' in dados and isinstance(dados['rf'], dict):
                    rf_id = dados['rf'].get('id', '')
            if not rf_id:
                # Tentar extrair do nome do arquivo
                rf_id = os.path.basename(arquivo).replace('.yaml', '')

            # Extrair nome/título
            nome = dados.get('titulo', dados.get('nome', dados.get('title', '')))
            if not nome:
                # Tentar extrair de estrutura aninhada rf.nome
                if 'rf' in dados and isinstance(dados['rf'], dict):
                    nome = dados['rf'].get('nome', '')

            # Garantir que nome é string
            nome = extrair_texto(nome)

            # Extrair descrição (prioridade: resumo_executivo > descricao > objetivo)
            descricao = ''

            # 1. Tentar resumo_executivo (mais direto)
            if 'resumo_executivo' in dados:
                descricao = extrair_texto(dados['resumo_executivo'])

            # 2. Se vazio, tentar descricao (pode ser dict ou string)
            if not descricao and 'descricao' in dados:
                descricao_raw = dados['descricao']
                if isinstance(descricao_raw, dict):
                    # Prioridade: objetivo > problema_resolvido > publico_afetado
                    descricao = extrair_texto(descricao_raw.get('objetivo', ''))
                    if not descricao:
                        descricao = extrair_texto(descricao_raw.get('problema_resolvido', ''))
                else:
                    descricao = extrair_texto(descricao_raw)

            # 3. Se ainda vazio, tentar objetivos (lista)
            if not descricao and 'objetivos' in dados:
                objetivos_list = dados['objetivos']
                if isinstance(objetivos_list, list) and len(objetivos_list) > 0:
                    primeiro_obj = objetivos_list[0]
                    if isinstance(primeiro_obj, dict):
                        descricao = extrair_texto(primeiro_obj.get('descricao', ''))

            # 4. Se ainda vazio, tentar objetivo direto
            if not descricao and 'objetivo' in dados:
                descricao = extrair_texto(dados['objetivo'])

            # Limitar descrição a ~200 caracteres (sucinta)
            if len(descricao) > 200:
                descricao = descricao[:197] + '...'

            # Extrair regras de negócio (SIMPLIFICADAS para coordenação)
            regras = []

            # Tentar estrutura nova: regras_negocio.regras[]
            if 'regras_negocio' in dados:
                rns_obj = dados['regras_negocio']

                # Se é dict com campo regras
                if isinstance(rns_obj, dict) and 'regras' in rns_obj:
                    regras_list = rns_obj['regras']
                    if isinstance(regras_list, list):
                        for rn in regras_list:
                            if isinstance(rn, dict):
                                # Usar apenas o título (sem detalhes técnicos)
                                titulo_rn = rn.get('titulo', '')
                                if titulo_rn:
                                    regras.append(titulo_rn)

                # Se é lista direta
                elif isinstance(rns_obj, list):
                    for rn in rns_obj:
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

            # Formatar regras em parágrafo único (linguagem simples, nível coordenação)
            if regras:
                # Limitar a 5 primeiras regras (mais importantes)
                regras_top5 = regras[:5]
                regras_texto = ". ".join(regras_top5)
                if not regras_texto.endswith('.'):
                    regras_texto += '.'
            else:
                regras_texto = "Regras de negócio não documentadas."

            # Adicionar RF à lista
            rfs.append({
                'codigo': rf_id,
                'nome': nome if nome else "Nome não disponível",
                'descricao': descricao if descricao else "Descrição não disponível.",
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
    print("GERADOR DE PLANILHA DE FUNCIONALIDADES v2.0")
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
    print(f"RFs com nome preenchido: {sum(1 for rf in rfs if rf['nome'] != 'Nome não disponível')}")
    print(f"RFs com descrição preenchida: {sum(1 for rf in rfs if rf['descricao'] != 'Descrição não disponível.')}")
    print(f"RFs com regras: {sum(1 for rf in rfs if rf['regras'] != 'Regras de negócio não documentadas.')}")
    print()

    # Primeiros 5 RFs como amostra
    print("AMOSTRA (5 primeiros RFs):")
    print("-" * 80)
    for rf in rfs[:5]:
        # Remover caracteres especiais que causam erro de encoding
        nome_safe = rf['nome'].encode('ascii', 'ignore').decode('ascii')
        desc_safe = rf['descricao'][:80].encode('ascii', 'ignore').decode('ascii')
        regras_safe = rf['regras'][:80].encode('ascii', 'ignore').decode('ascii')

        print(f"  {rf['codigo']}: {nome_safe}")
        print(f"    Descricao: {desc_safe}...")
        print(f"    Regras: {regras_safe}...")
        print()

    print("=" * 80)
    print("[OK] CONCLUÍDO")
    print("=" * 80)

if __name__ == '__main__':
    main()
