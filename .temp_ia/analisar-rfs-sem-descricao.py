#!/usr/bin/env python3
"""
Analisa RFs sem descrição extraída para identificar padrões.
"""

import os
import sys
import yaml
import glob

def analisar_rf_descricao(arquivo):
    """Analisa campos de descrição de um RF."""
    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            dados = yaml.safe_load(f)

        if not dados:
            return None

        rf_id = dados.get('rf_id', '')
        if not rf_id:
            if 'rf' in dados and isinstance(dados['rf'], dict):
                rf_id = dados['rf'].get('id', '')
        if not rf_id:
            rf_id = os.path.basename(arquivo).replace('.yaml', '')

        # Verificar campos de descrição disponíveis
        campos_disponiveis = []

        if 'resumo_executivo' in dados:
            campos_disponiveis.append('resumo_executivo')
        if 'descricao' in dados:
            campos_disponiveis.append('descricao')
        if 'objetivo' in dados:
            campos_disponiveis.append('objetivo')
        if 'objetivos' in dados:
            campos_disponiveis.append('objetivos')
        if 'visao_geral' in dados:
            campos_disponiveis.append('visao_geral')
        if 'escopo' in dados:
            campos_disponiveis.append('escopo')
        if 'metadata' in dados and isinstance(dados['metadata'], dict):
            if 'descricao' in dados['metadata']:
                campos_disponiveis.append('metadata.descricao')
            if 'resumo' in dados['metadata']:
                campos_disponiveis.append('metadata.resumo')

        return {
            'rf_id': rf_id,
            'arquivo': os.path.basename(arquivo),
            'campos_disponiveis': campos_disponiveis
        }
    except Exception as e:
        return {
            'rf_id': os.path.basename(arquivo).replace('.yaml', ''),
            'arquivo': os.path.basename(arquivo),
            'erro': str(e)
        }

def main():
    documentacao_path = r"D:\IC2_Governanca\documentacao"
    pattern = os.path.join(documentacao_path, "**", "RF*.yaml")
    arquivos = glob.glob(pattern, recursive=True)

    # Ignorar RL-RF*.yaml
    arquivos = [a for a in arquivos if not os.path.basename(a).startswith("RL-")]

    print(f"Analisando {len(arquivos)} RFs...\n")

    rfs_info = []
    for arquivo in arquivos:
        info = analisar_rf_descricao(arquivo)
        if info:
            rfs_info.append(info)

    # RFs sem campos de descrição
    rfs_sem_campos = [rf for rf in rfs_info if not rf.get('campos_disponiveis', [])]

    # RFs com campos de descrição
    rfs_com_campos = [rf for rf in rfs_info if rf.get('campos_disponiveis', [])]

    print(f"RFs COM campos de descrição: {len(rfs_com_campos)}")
    print(f"RFs SEM campos de descrição: {len(rfs_sem_campos)}\n")

    if rfs_sem_campos:
        print("=" * 80)
        print("RFs SEM CAMPOS DE DESCRIÇÃO:")
        print("=" * 80)
        for rf in rfs_sem_campos[:15]:
            print(f"\nRF: {rf['rf_id']}")
            print(f"Arquivo: {rf['arquivo']}")
            if 'erro' in rf:
                print(f"ERRO: {rf['erro']}")

        if len(rfs_sem_campos) > 15:
            print(f"\n... e mais {len(rfs_sem_campos) - 15} RFs sem campos.")

    # Estatísticas de campos disponíveis
    print("\n" + "=" * 80)
    print("ESTATÍSTICAS DE CAMPOS DISPONÍVEIS:")
    print("=" * 80)

    campos_count = {}
    for rf in rfs_com_campos:
        for campo in rf.get('campos_disponiveis', []):
            campos_count[campo] = campos_count.get(campo, 0) + 1

    for campo, count in sorted(campos_count.items(), key=lambda x: x[1], reverse=True):
        print(f"{campo}: {count} RFs")

if __name__ == '__main__':
    main()
