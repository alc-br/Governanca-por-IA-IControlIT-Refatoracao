#!/usr/bin/env python3
"""
Analisa RFs sem nome extraído para identificar padrões.
"""

import os
import sys
import yaml
import glob

def analisar_rf(arquivo):
    """Analisa estrutura de um RF."""
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

        # Tentar extrair nome
        nome = dados.get('titulo', dados.get('nome', dados.get('title', '')))
        if not nome:
            if 'rf' in dados and isinstance(dados['rf'], dict):
                nome = dados['rf'].get('nome', dados['rf'].get('titulo', ''))

        return {
            'rf_id': rf_id,
            'arquivo': arquivo,
            'nome': nome,
            'tem_rf_nested': 'rf' in dados,
            'campos_raiz': list(dados.keys())[:10]
        }
    except Exception as e:
        return {
            'rf_id': os.path.basename(arquivo).replace('.yaml', ''),
            'arquivo': arquivo,
            'nome': '',
            'erro': str(e)
        }

def main():
    documentacao_path = r"D:\IC2_Governanca\documentacao"
    pattern = os.path.join(documentacao_path, "**", "RF*.yaml")
    arquivos = glob.glob(pattern, recursive=True)

    # Ignorar RL-RF*.yaml
    arquivos = [a for a in arquivos if not os.path.basename(a).startswith("RL-")]

    print(f"Analisando {len(arquivos)} RFs...\n")

    rfs_sem_nome = []
    rfs_com_nome = []

    for arquivo in arquivos:
        info = analisar_rf(arquivo)
        if info:
            if not info['nome']:
                rfs_sem_nome.append(info)
            else:
                rfs_com_nome.append(info)

    print(f"RFs COM nome: {len(rfs_com_nome)}")
    print(f"RFs SEM nome: {len(rfs_sem_nome)}\n")

    if rfs_sem_nome:
        print("=" * 80)
        print("RFs SEM NOME EXTRAÍDO:")
        print("=" * 80)
        for rf in rfs_sem_nome[:10]:  # Mostrar primeiros 10
            print(f"\nRF: {rf['rf_id']}")
            print(f"Arquivo: {os.path.basename(rf['arquivo'])}")
            print(f"Tem estrutura rf nested: {rf.get('tem_rf_nested', False)}")
            if 'campos_raiz' in rf:
                print(f"Campos raiz: {rf['campos_raiz']}")
            if 'erro' in rf:
                print(f"ERRO: {rf['erro']}")

        if len(rfs_sem_nome) > 10:
            print(f"\n... e mais {len(rfs_sem_nome) - 10} RFs sem nome.")

    print("\n" + "=" * 80)
    print("ANÁLISE DE ESTRUTURAS:")
    print("=" * 80)

    # Contar estruturas
    nested_count = sum(1 for rf in rfs_com_nome if rf.get('tem_rf_nested', False))
    flat_count = len(rfs_com_nome) - nested_count

    print(f"RFs com estrutura nested (rf.nome): {nested_count}")
    print(f"RFs com estrutura flat (nome direto): {flat_count}")

if __name__ == '__main__':
    main()
