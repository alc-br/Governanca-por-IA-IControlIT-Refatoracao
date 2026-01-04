#!/usr/bin/env python3
"""
Script para reclassificar RFs de Skeleton para Completo
baseado nos resultados da auditoria profunda.

Data: 2025-12-27
Objetivo: Atualizar STATUS.yaml dos 7 RFs que foram incorretamente classificados como Skeleton
"""

import os
from datetime import datetime

# RFs que precisam ser reclassificados (resultado da auditoria)
RFS_TO_RECLASSIFY = {
    'RF042': 'd:/IC2/docs/rf/Fase-4-Financeiro-II-Processos/EPIC007-FIN-Financeiro-Processos/RF042-Gestao-de-Notas-Fiscais-Estoque/STATUS.yaml',
    'RF053': 'd:/IC2/docs/rf/Fase-5-Service-Desk/EPIC008-SD-Service-Desk/RF053-Gestao-de-Solicitacoes/STATUS.yaml',
    'RF055': 'd:/IC2/docs/rf/Fase-4-Financeiro-II-Processos/EPIC007-FIN-Financeiro-Processos/RF055-Gestao-de-Rateio/STATUS.yaml',
    'RF057': 'd:/IC2/docs/rf/Fase-4-Financeiro-II-Processos/EPIC007-FIN-Financeiro-Processos/RF057-Gestao-de-Itens-Rateio/STATUS.yaml',
    'RF061': 'd:/IC2/docs/rf/Fase-5-Service-Desk/EPIC008-SD-Service-Desk/RF061-Gestao-Ordens-Servico/STATUS.yaml',
    'RF062': 'd:/IC2/docs/rf/Fase-5-Service-Desk/EPIC008-SD-Service-Desk/RF062-Gestao-Fornecedores-Parceiros/STATUS.yaml',
    'RF067': 'd:/IC2/docs/rf/Fase-2-Cadastros-e-Servicos-Transversais/EPIC005-NOT-Notificacoes/RF067-Central-Emails/STATUS.yaml',
}


def reclassify_status_yaml(rf_num, file_path):
    """
    Atualiza o STATUS.yaml para remover classificação Skeleton.

    Mudanças:
    - skeleton.criado: True -> False
    - skeleton.data_criacao: "2025-12-27" -> null
    - skeleton.observacao: atualiza com resultado da auditoria
    """

    if not os.path.exists(file_path):
        print(f"[ERRO] {rf_num}: Arquivo não encontrado: {file_path}")
        return False

    # Ler arquivo
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Processar linhas
    updated_lines = []
    in_skeleton_section = False

    for i, line in enumerate(lines):
        # Detectar seção skeleton
        if line.strip() == 'skeleton:':
            in_skeleton_section = True
            updated_lines.append(line)
            continue

        # Dentro da seção skeleton
        if in_skeleton_section:
            # Detectar fim da seção (linha sem indentação ou nova seção)
            if line and not line.startswith(' ') and not line.startswith('\t'):
                in_skeleton_section = False
                updated_lines.append(line)
                continue

            # Atualizar campos
            if 'criado:' in line:
                updated_lines.append('  criado: False\n')
            elif 'data_criacao:' in line:
                updated_lines.append('  data_criacao: null\n')
            elif 'observacao:' in line:
                observacao = f'  observacao: "Reclassificado de Skeleton para Completo apos auditoria profunda (2025-12-27). Backend implementou todas as regras do RF."\n'
                updated_lines.append(observacao)
            else:
                updated_lines.append(line)
        else:
            updated_lines.append(line)

    # Salvar arquivo atualizado
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(updated_lines)

    print(f"[OK] {rf_num}: Reclassificado com sucesso")
    return True


def main():
    """Reclassifica todos os RFs identificados pela auditoria."""

    print("=" * 80)
    print("RECLASSIFICAÇÃO: SKELETON -> COMPLETO")
    print("=" * 80)
    print()

    total = len(RFS_TO_RECLASSIFY)
    success = 0
    failed = 0

    for rf_num, file_path in RFS_TO_RECLASSIFY.items():
        if reclassify_status_yaml(rf_num, file_path):
            success += 1
        else:
            failed += 1

    print()
    print("=" * 80)
    print("RESULTADO")
    print("=" * 80)
    print(f"Total:    {total}")
    print(f"Sucesso:  {success}")
    print(f"Falha:    {failed}")
    print()

    if success == total:
        print("[OK] Todos os RFs foram reclassificados com sucesso!")
        print()
        print("Proximo passo: Executar sincronizacao com DevOps")
        print("  python tools/devops-sync/sync-board.py")
    else:
        print(f"[ATENCAO] {failed} RFs falharam na reclassificacao")


if __name__ == '__main__':
    main()
