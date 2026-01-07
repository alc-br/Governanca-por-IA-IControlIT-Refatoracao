#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Análise Cirúrgica V2: Classificar RFs baseado no STATUS.yaml existente

Estratégia simplificada:
1. Ler STATUS.yaml de cada RF
2. Se backend.status ou frontend.status != 'not_started', analisar implementação
3. Determinar se é Skeleton ou Completo baseado em:
   - backend.status = 'done' + frontend.status = 'done' → COMPLETO
   - backend.status in ['in_progress', 'done'] mas código é básico → SKELETON
4. Atualizar STATUS.yaml com campo skeleton

Uso:
    python classify-rfs-v2.py
"""

import os
import sys
import glob
import re
from datetime import datetime
from pathlib import Path

# Configurações
DOCS_RF_PATH = "D:/IC2/docs/rf"
BACKEND_PATH = "D:/IC2/backend/IControlIT.API/src"
FRONTEND_PATH = "D:/IC2/frontend/icontrolit-app/src/app"

# Relatório
REPORT_PATH = "D:/IC2/relatorios"
REPORT_FILE = f"{REPORT_PATH}/{datetime.now().strftime('%Y-%m-%d-%H%M')}-CLASSIFICACAO-RFS-V2.md"

# Estatísticas
stats = {
    "total": 0,
    "skeleton": 0,
    "completo": 0,
    "not_started": 0,
    "in_progress": 0,
    "errors": 0
}

results = []

def parse_yaml_simple(content):
    """Parser YAML simplificado"""
    data = {}
    lines = content.split('\n')
    current_section = None
    current_subsection = None

    for line in lines:
        if line.strip().startswith('#') or not line.strip():
            continue

        if not line.startswith(' ') and ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            if value:
                if value.lower() == 'true':
                    data[key] = True
                elif value.lower() == 'false':
                    data[key] = False
                elif value.lower() == 'null':
                    data[key] = None
                else:
                    data[key] = value.strip('"')
            else:
                data[key] = {}
                current_section = key
                current_subsection = None

        elif line.startswith('  ') and not line.startswith('    ') and ':' in line:
            parts = line.strip().split(':', 1)
            if len(parts) != 2:
                continue
            key, value = parts
            key = key.strip()
            value = value.strip()
            if current_section:
                if value:
                    if '#' in value:
                        value = value.split('#')[0].strip()
                    if value.lower() == 'true':
                        data[current_section][key] = True
                    elif value.lower() == 'false':
                        data[current_section][key] = False
                    elif value.lower() == 'null':
                        data[current_section][key] = None
                    else:
                        data[current_section][key] = value.strip('"')
                else:
                    data[current_section][key] = {}
                    current_subsection = key

        elif line.startswith('    ') and ':' in line:
            parts = line.strip().split(':', 1)
            if len(parts) != 2:
                continue
            key, value = parts
            key = key.strip()
            value = value.strip()
            if current_section and current_subsection:
                if '#' in value:
                    value = value.split('#')[0].strip()
                if value.lower() == 'true':
                    data[current_section][current_subsection][key] = True
                elif value.lower() == 'false':
                    data[current_section][current_subsection][key] = False
                elif value.lower() == 'null':
                    data[current_section][current_subsection][key] = None
                else:
                    data[current_section][current_subsection][key] = value.strip('"')

    return data

def extract_rf_number(status_yaml_path):
    """Extrai número do RF do caminho"""
    match = re.search(r'RF(\d+)', status_yaml_path)
    if match:
        return f"RF{int(match.group(1)):03d}"
    return None

def classify_rf(status_yaml_path):
    """
    Classifica um RF baseado no STATUS.yaml e análise simples.
    Retorna: (classification, details)
    """
    documentacao_num = extract_rf_number(status_yaml_path)
    if not documentacao_num:
        return "ERROR", "Não foi possível extrair número do RF"

    # Ler STATUS.yaml
    try:
        with open(status_yaml_path, 'r', encoding='utf-8') as f:
            status_data = parse_yaml_simple(f.read())
    except Exception as e:
        return "ERROR", f"Erro ao ler STATUS.yaml: {str(e)}"

    # Verificar desenvolvimento
    dev = status_data.get('desenvolvimento', {})
    if isinstance(dev, dict):
        backend_info = dev.get('backend', {})
        frontend_info = dev.get('frontend', {})
    else:
        return "ERROR", "Estrutura de desenvolvimento inválida"

    if isinstance(backend_info, dict):
        backend_status = backend_info.get('status', 'not_started')
    else:
        backend_status = str(backend_info) if backend_info else 'not_started'

    if isinstance(frontend_info, dict):
        frontend_status = frontend_info.get('status', 'not_started')
    else:
        frontend_status = str(frontend_info) if frontend_info else 'not_started'

    # Classificação baseada em STATUS.yaml
    # Regra 1: Se ambos not_started → NOT_STARTED
    if backend_status == 'not_started' and frontend_status == 'not_started':
        return "NOT_STARTED", f"Backend: {backend_status}, Frontend: {frontend_status}"

    # Regra 2: Se ambos 'done' → assumir COMPLETO (pode ser ajustado manualmente)
    if backend_status == 'done' and frontend_status == 'done':
        return "COMPLETO", f"Backend: done, Frontend: done"

    # Regra 3: Se um dos dois está em progresso ou skeleton → SKELETON
    if backend_status in ['in_progress', 'skeleton'] or frontend_status in ['in_progress', 'skeleton']:
        return "SKELETON", f"Backend: {backend_status}, Frontend: {frontend_status}"

    # Regra 4: Se backend done mas frontend not_started → SKELETON (backend pronto, aguarda frontend)
    if backend_status == 'done' and frontend_status == 'not_started':
        return "SKELETON", f"Backend completo, Frontend não iniciado"

    # Regra 5: Se frontend done mas backend not_started → improvável, mas classificar como IN_PROGRESS
    if frontend_status == 'done' and backend_status == 'not_started':
        return "IN_PROGRESS", f"Frontend completo, Backend não iniciado (situação atípica)"

    # Regra 6: Qualquer outra combinação → IN_PROGRESS
    return "IN_PROGRESS", f"Backend: {backend_status}, Frontend: {frontend_status}"

def update_status_yaml(status_yaml_path, classification):
    """
    Atualiza STATUS.yaml com campo skeleton.
    """
    try:
        with open(status_yaml_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Encontrar posição para inserir campo skeleton
        # Inserir após 'titulo:' e antes de 'documentacao:'
        insert_index = -1
        for i, line in enumerate(lines):
            if line.startswith('documentacao:'):
                insert_index = i
                break

        if insert_index == -1:
            print(f"[WARN] Não encontrou seção 'documentacao:' em {status_yaml_path}")
            return False

        # Verificar se já existe seção skeleton
        has_skeleton = any('skeleton:' in line for line in lines)

        if has_skeleton:
            # Atualizar seção existente
            for i, line in enumerate(lines):
                if line.startswith('skeleton:'):
                    # Atualizar linhas seguintes
                    if i + 1 < len(lines) and '  criado:' in lines[i + 1]:
                        lines[i + 1] = f"  criado: {'True' if classification == 'SKELETON' else 'False'}\n"
                    else:
                        lines.insert(i + 1, f"  criado: {'True' if classification == 'SKELETON' else 'False'}\n")

                    if i + 2 < len(lines) and '  data_criacao:' in lines[i + 2]:
                        date_str = datetime.now().strftime('%Y-%m-%d')
                        lines[i + 2] = f'  data_criacao: "{date_str}"\n'
                    else:
                        date_str = datetime.now().strftime('%Y-%m-%d')
                        lines.insert(i + 2, f'  data_criacao: "{date_str}"\n')

                    if i + 3 < len(lines) and '  observacao:' in lines[i + 3]:
                        if classification == 'SKELETON':
                            lines[i + 3] = f'  observacao: "Skeleton criado. Aguarda CONTRATO DE REGULARIZAÇÃO DE BACKEND."\n'
                        else:
                            lines[i + 3] = f'  observacao: "RF {classification.lower()}."\n'
                    else:
                        if classification == 'SKELETON':
                            lines.insert(i + 3, f'  observacao: "Skeleton criado. Aguarda CONTRATO DE REGULARIZAÇÃO DE BACKEND."\n')
                        else:
                            lines.insert(i + 3, f'  observacao: "RF {classification.lower()}."\n')
                    break
        else:
            # Adicionar nova seção skeleton
            date_str = datetime.now().strftime('%Y-%m-%d')
            skeleton_section = [
                "\n",
                "skeleton:\n",
                f"  criado: {'True' if classification == 'SKELETON' else 'False'}\n",
                f'  data_criacao: "{date_str}"\n',
            ]

            if classification == 'SKELETON':
                skeleton_section.append(f'  observacao: "Skeleton criado. Aguarda CONTRATO DE REGULARIZAÇÃO DE BACKEND."\n')
            else:
                skeleton_section.append(f'  observacao: "RF {classification.lower()}."\n')

            lines = lines[:insert_index] + skeleton_section + lines[insert_index:]

        # Escrever arquivo atualizado
        with open(status_yaml_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)

        return True

    except Exception as e:
        print(f"[ERROR] Erro ao atualizar {status_yaml_path}: {str(e)}")
        return False

def generate_report():
    """Gera relatório final de classificação"""
    os.makedirs(REPORT_PATH, exist_ok=True)

    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write(f"# RELATÓRIO DE CLASSIFICAÇÃO DE RFS (V2)\n\n")
        f.write(f"**Data:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**Estratégia:** Classificação baseada em STATUS.yaml existente\n\n")
        f.write(f"---\n\n")
        f.write(f"## ESTATÍSTICAS\n\n")
        f.write(f"| Categoria | Quantidade | Percentual |\n")
        f.write(f"|-----------|------------|------------|\n")
        f.write(f"| Total de RFs | {stats['total']} | 100% |\n")
        f.write(f"| **Skeleton** | **{stats['skeleton']}** | **{stats['skeleton']/stats['total']*100:.1f}%** |\n")
        f.write(f"| Completo | {stats['completo']} | {stats['completo']/stats['total']*100:.1f}% |\n")
        f.write(f"| Em Progresso | {stats['in_progress']} | {stats['in_progress']/stats['total']*100:.1f}% |\n")
        f.write(f"| Não Iniciado | {stats['not_started']} | {stats['not_started']/stats['total']*100:.1f}% |\n")
        f.write(f"| Erros | {stats['errors']} | {stats['errors']/stats['total']*100:.1f}% |\n")
        f.write(f"\n---\n\n")
        f.write(f"## CLASSIFICAÇÃO DETALHADA\n\n")

        # Agrupar por classificação
        by_classification = {}
        for result in results:
            classification = result['classification']
            if classification not in by_classification:
                by_classification[classification] = []
            by_classification[classification].append(result)

        # Skeleton
        if 'SKELETON' in by_classification:
            f.write(f"### RFs em Estado Skeleton ({len(by_classification['SKELETON'])})\n\n")
            f.write(f"| RF | Título | Detalhes |\n")
            f.write(f"|----|--------|----------|\n")
            for result in by_classification['SKELETON']:
                f.write(f"| {result['rf']} | {result['titulo'][:50]} | {result['details']} |\n")
            f.write(f"\n")

        # Completo
        if 'COMPLETO' in by_classification:
            f.write(f"### RFs Completos ({len(by_classification['COMPLETO'])})\n\n")
            f.write(f"| RF | Título | Detalhes |\n")
            f.write(f"|----|--------|----------|\n")
            for result in by_classification['COMPLETO']:
                f.write(f"| {result['rf']} | {result['titulo'][:50]} | {result['details']} |\n")
            f.write(f"\n")

        # Em Progresso
        if 'IN_PROGRESS' in by_classification:
            f.write(f"### RFs Em Progresso ({len(by_classification['IN_PROGRESS'])})\n\n")
            f.write(f"| RF | Título | Detalhes |\n")
            f.write(f"|----|--------|----------|\n")
            for result in by_classification['IN_PROGRESS']:
                f.write(f"| {result['rf']} | {result['titulo'][:50]} | {result['details']} |\n")
            f.write(f"\n")

        # Não Iniciado
        if 'NOT_STARTED' in by_classification:
            f.write(f"### RFs Não Iniciados ({len(by_classification['NOT_STARTED'])})\n\n")
            f.write(f"| RF | Título | Detalhes |\n")
            f.write(f"|----|--------|----------|\n")
            for result in by_classification['NOT_STARTED']:
                f.write(f"| {result['rf']} | {result['titulo'][:50]} | {result['details']} |\n")
            f.write(f"\n")

        # Erros
        if 'ERROR' in by_classification:
            f.write(f"### RFs com Erro ({len(by_classification['ERROR'])})\n\n")
            f.write(f"| RF | Título | Detalhes |\n")
            f.write(f"|----|--------|----------|\n")
            for result in by_classification['ERROR']:
                f.write(f"| {result['rf']} | {result['titulo'][:50]} | {result['details']} |\n")
            f.write(f"\n")

        f.write(f"---\n\n")
        f.write(f"**FIM DO RELATÓRIO**\n")

    print(f"\n[OK] Relatório gerado: {REPORT_FILE}")

def main():
    print("=" * 80)
    print("ANÁLISE CIRÚRGICA V2: CLASSIFICAÇÃO DE RFs")
    print("Estratégia: Baseado em STATUS.yaml existente")
    print("=" * 80)
    print()

    # Listar todos os STATUS.yaml
    status_files = glob.glob(f"{DOCS_RF_PATH}/**/STATUS.yaml", recursive=True)
    stats['total'] = len(status_files)

    print(f"[INFO] Encontrados {stats['total']} RFs para analisar")
    print()

    # Analisar cada RF
    for i, status_yaml_path in enumerate(sorted(status_files), 1):
        documentacao_num = extract_rf_number(status_yaml_path)
        print(f"[{i}/{stats['total']}] Analisando {rf_num}...", end=" ")

        # Ler título do RF
        try:
            with open(status_yaml_path, 'r', encoding='utf-8') as f:
                status_data = parse_yaml_simple(f.read())
            titulo = status_data.get('titulo', 'Sem título')
        except:
            titulo = 'Erro ao ler título'

        # Classificar
        classification, details = classify_rf(status_yaml_path)

        # Atualizar estatísticas
        if classification == "SKELETON":
            stats['skeleton'] += 1
        elif classification == "COMPLETO":
            stats['completo'] += 1
        elif classification == "NOT_STARTED":
            stats['not_started'] += 1
        elif classification == "IN_PROGRESS":
            stats['in_progress'] += 1
        elif classification == "ERROR":
            stats['errors'] += 1

        # Atualizar STATUS.yaml
        if classification in ["SKELETON", "COMPLETO", "NOT_STARTED", "IN_PROGRESS"]:
            if update_status_yaml(status_yaml_path, classification):
                print(f"OK {classification}")
            else:
                print(f"WARN {classification} (erro ao atualizar)")
        else:
            print(f"ERROR {classification}")

        # Armazenar resultado
        results.append({
            'rf': documentacao_num,
            'titulo': titulo,
            'classification': classification,
            'details': details,
            'path': status_yaml_path
        })

    print()
    print("=" * 80)
    print("ESTATÍSTICAS FINAIS")
    print("=" * 80)
    print(f"Total de RFs:    {stats['total']}")
    print(f"Skeleton:        {stats['skeleton']} ({stats['skeleton']/stats['total']*100:.1f}%)")
    print(f"Completo:        {stats['completo']} ({stats['completo']/stats['total']*100:.1f}%)")
    print(f"Em Progresso:    {stats['in_progress']} ({stats['in_progress']/stats['total']*100:.1f}%)")
    print(f"Não Iniciado:    {stats['not_started']} ({stats['not_started']/stats['total']*100:.1f}%)")
    print(f"Erros:           {stats['errors']} ({stats['errors']/stats['total']*100:.1f}%)")
    print("=" * 80)
    print()

    # Gerar relatório
    generate_report()

    print()
    print("[OK] Análise concluída com sucesso!")
    print(f"[OK] Relatório disponível em: {REPORT_FILE}")
    print()
    print("PRÓXIMOS PASSOS:")
    print("1. Revisar relatório gerado")
    print("2. Ajustar manualmente classificações se necessário")
    print("3. Sincronizar com DevOps: python tools/devops-sync/sync-all-rfs.py")

if __name__ == "__main__":
    main()
