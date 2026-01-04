#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Análise Cirúrgica: Classificar RFs como Skeleton ou Completo

Este script analisa TODOS os RFs em D:\\IC2\\docs\\rf e determina
se cada um é apenas Skeleton (CRUD básico) ou implementação completa.

Critérios de classificação:
- Skeleton: Apenas entidade, CRUD básico, endpoints HTTP, formulário básico
- Completo: Regras de negócio, validações complexas, estados, workflows

Uso:
    python classify-all-rfs.py
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
REPORT_FILE = f"{REPORT_PATH}/{datetime.now().strftime('%Y-%m-%d')}-CLASSIFICACAO-RFS.md"

# Estatísticas
stats = {
    "total": 0,
    "skeleton": 0,
    "completo": 0,
    "not_started": 0,
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
            key, value = line.strip().split(':', 1)
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
            key, value = line.strip().split(':', 1)
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

def check_backend_implementation(rf_num):
    """
    Verifica implementação do backend.
    Retorna: (exists, is_skeleton, details)
    """
    # Mapear RF para entidade
    # Exemplo: RF024 -> Departamento, RF028 -> SlaOperacao, etc.

    # Procurar por arquivos relacionados ao RF
    search_patterns = [
        f"{BACKEND_PATH}/Domain/Entities/*{rf_num}*.cs",
        f"{BACKEND_PATH}/Application/**/*{rf_num}*.cs",
    ]

    files_found = []
    for pattern in search_patterns:
        files_found.extend(glob.glob(pattern, recursive=True))

    if not files_found:
        return False, False, "Nenhum arquivo backend encontrado"

    # Analisar complexidade dos arquivos
    has_complex_validations = False
    has_states = False
    has_business_rules = False

    for file_path in files_found:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

                # Indicadores de implementação completa
                if 'FluentValidation' in content and 'RuleFor' in content:
                    # Contar regras de validação
                    rule_count = content.count('RuleFor')
                    if rule_count > 3:  # Mais de 3 regras = complexo
                        has_complex_validations = True

                if 'enum' in content and 'Status' in content:
                    has_states = True

                if any(keyword in content for keyword in ['Calculate', 'Process', 'Approve', 'Reject', 'Workflow']):
                    has_business_rules = True
        except:
            pass

    is_skeleton = not (has_complex_validations or has_states or has_business_rules)

    details = f"Arquivos: {len(files_found)}, Validações complexas: {has_complex_validations}, Estados: {has_states}, Regras: {has_business_rules}"

    return True, is_skeleton, details

def check_frontend_implementation(rf_num):
    """
    Verifica implementação do frontend.
    Retorna: (exists, is_skeleton, details)
    """
    # Procurar por componentes relacionados ao RF
    search_patterns = [
        f"{FRONTEND_PATH}/modules/admin/management/**/*{rf_num.lower()}*/**/*.ts",
        f"{FRONTEND_PATH}/modules/admin/management/**/*{rf_num.lower()}*/**/*.html",
    ]

    files_found = []
    for pattern in search_patterns:
        files_found.extend(glob.glob(pattern, recursive=True))

    if not files_found:
        return False, False, "Nenhum arquivo frontend encontrado"

    # Analisar complexidade
    has_workflows = False
    has_states = False
    has_advanced_validations = False

    for file_path in files_found:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

                # Indicadores de implementação completa
                if 'workflow' in content.lower():
                    has_workflows = True

                if 'status' in content.lower() and ('approved' in content.lower() or 'rejected' in content.lower()):
                    has_states = True

                if 'Validators' in content and '.pattern(' in content:
                    has_advanced_validations = True
        except:
            pass

    is_skeleton = not (has_workflows or has_states or has_advanced_validations)

    details = f"Arquivos: {len(files_found)}, Workflows: {has_workflows}, Estados: {has_states}, Validações avançadas: {has_advanced_validations}"

    return True, is_skeleton, details

def classify_rf(status_yaml_path):
    """
    Classifica um RF como Skeleton ou Completo.
    Retorna: (classification, details)
    """
    rf_num = extract_rf_number(status_yaml_path)
    if not rf_num:
        return "ERROR", "Não foi possível extrair número do RF"

    # Ler STATUS.yaml
    try:
        with open(status_yaml_path, 'r', encoding='utf-8') as f:
            status_data = parse_yaml_simple(f.read())
    except Exception as e:
        return "ERROR", f"Erro ao ler STATUS.yaml: {str(e)}"

    # Verificar desenvolvimento
    dev = status_data.get('desenvolvimento', {})
    backend_status = dev.get('backend', {}).get('status', 'not_started')
    frontend_status = dev.get('frontend', {}).get('status', 'not_started')

    # Se ambos not_started, é NOT_STARTED
    if backend_status == 'not_started' and frontend_status == 'not_started':
        return "NOT_STARTED", "Backend e Frontend não iniciados"

    # Analisar backend
    backend_exists, backend_is_skeleton, backend_details = check_backend_implementation(rf_num)

    # Analisar frontend
    frontend_exists, frontend_is_skeleton, frontend_details = check_frontend_implementation(rf_num)

    # Determinar classificação
    if not backend_exists and not frontend_exists:
        classification = "NOT_STARTED"
        details = "Nenhuma implementação encontrada"
    elif backend_is_skeleton and frontend_is_skeleton:
        classification = "SKELETON"
        details = f"Backend: {backend_details} | Frontend: {frontend_details}"
    elif backend_status == 'done' and frontend_status == 'done':
        classification = "COMPLETO"
        details = f"Backend: {backend_details} | Frontend: {frontend_details}"
    else:
        # Analisar caso a caso
        if backend_is_skeleton or frontend_is_skeleton:
            classification = "SKELETON"
        else:
            classification = "COMPLETO"
        details = f"Backend: {backend_details} | Frontend: {frontend_details}"

    return classification, details

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
                    if i + 2 < len(lines) and '  data_criacao:' in lines[i + 2]:
                        lines[i + 2] = f'  data_criacao: "{datetime.now().strftime("%Y-%m-%d")}"\n'
                    if i + 3 < len(lines) and '  observacao:' in lines[i + 3]:
                        if classification == 'SKELETON':
                            lines[i + 3] = f'  observacao: "Skeleton criado. Aguarda CONTRATO DE REGULARIZAÇÃO DE BACKEND."\n'
                        else:
                            lines[i + 3] = f'  observacao: "RF completo ou não iniciado."\n'
                    break
        else:
            # Adicionar nova seção skeleton
            skeleton_section = [
                "\n",
                "skeleton:\n",
                f"  criado: {'True' if classification == 'SKELETON' else 'False'}\n",
                f'  data_criacao: "{datetime.now().strftime("%Y-%m-%d")}"\n',
            ]

            if classification == 'SKELETON':
                skeleton_section.append(f'  observacao: "Skeleton criado. Aguarda CONTRATO DE REGULARIZAÇÃO DE BACKEND."\n')
            else:
                skeleton_section.append(f'  observacao: "RF completo ou não iniciado."\n')

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
        f.write(f"# RELATÓRIO DE CLASSIFICAÇÃO DE RFS\n\n")
        f.write(f"**Data:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"---\n\n")
        f.write(f"## ESTATÍSTICAS\n\n")
        f.write(f"| Categoria | Quantidade | Percentual |\n")
        f.write(f"|-----------|------------|------------|\n")
        f.write(f"| Total de RFs | {stats['total']} | 100% |\n")
        f.write(f"| **Skeleton** | **{stats['skeleton']}** | **{stats['skeleton']/stats['total']*100:.1f}%** |\n")
        f.write(f"| Completo | {stats['completo']} | {stats['completo']/stats['total']*100:.1f}% |\n")
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
                f.write(f"| {result['rf']} | {result['titulo']} | {result['details']} |\n")
            f.write(f"\n")

        # Completo
        if 'COMPLETO' in by_classification:
            f.write(f"### RFs Completos ({len(by_classification['COMPLETO'])})\n\n")
            f.write(f"| RF | Título | Detalhes |\n")
            f.write(f"|----|--------|----------|\n")
            for result in by_classification['COMPLETO']:
                f.write(f"| {result['rf']} | {result['titulo']} | {result['details']} |\n")
            f.write(f"\n")

        # Não Iniciado
        if 'NOT_STARTED' in by_classification:
            f.write(f"### RFs Não Iniciados ({len(by_classification['NOT_STARTED'])})\n\n")
            f.write(f"| RF | Título | Detalhes |\n")
            f.write(f"|----|--------|----------|\n")
            for result in by_classification['NOT_STARTED']:
                f.write(f"| {result['rf']} | {result['titulo']} | {result['details']} |\n")
            f.write(f"\n")

        # Erros
        if 'ERROR' in by_classification:
            f.write(f"### RFs com Erro ({len(by_classification['ERROR'])})\n\n")
            f.write(f"| RF | Título | Detalhes |\n")
            f.write(f"|----|--------|----------|\n")
            for result in by_classification['ERROR']:
                f.write(f"| {result['rf']} | {result['titulo']} | {result['details']} |\n")
            f.write(f"\n")

        f.write(f"---\n\n")
        f.write(f"## PRÓXIMOS PASSOS\n\n")
        f.write(f"### Para RFs em Skeleton ({stats['skeleton']})\n\n")
        f.write(f"1. Executar **CONTRATO DE REGULARIZAÇÃO DE BACKEND**\n")
        f.write(f"2. Implementar regras de negócio completas\n")
        f.write(f"3. Executar **CONTRATO DE TESTER-BACKEND**\n")
        f.write(f"4. Completar frontend\n\n")
        f.write(f"### Para RFs Completos ({stats['completo']})\n\n")
        f.write(f"1. Validar conformidade com RF/UC/MD\n")
        f.write(f"2. Executar testes E2E\n")
        f.write(f"3. Preparar para deploy\n\n")
        f.write(f"### Para RFs Não Iniciados ({stats['not_started']})\n\n")
        f.write(f"1. Priorizar backlog\n")
        f.write(f"2. Criar documentação (RF, UC, MD, WF)\n")
        f.write(f"3. Iniciar implementação\n\n")
        f.write(f"---\n\n")
        f.write(f"**FIM DO RELATÓRIO**\n")

    print(f"\n[OK] Relatório gerado: {REPORT_FILE}")

def main():
    print("=" * 80)
    print("ANÁLISE CIRÚRGICA: CLASSIFICAÇÃO DE RFs")
    print("=" * 80)
    print()

    # Listar todos os STATUS.yaml
    status_files = glob.glob(f"{DOCS_RF_PATH}/**/STATUS.yaml", recursive=True)
    stats['total'] = len(status_files)

    print(f"[INFO] Encontrados {stats['total']} RFs para analisar")
    print()

    # Analisar cada RF
    for i, status_yaml_path in enumerate(sorted(status_files), 1):
        rf_num = extract_rf_number(status_yaml_path)
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
        elif classification == "ERROR":
            stats['errors'] += 1

        # Atualizar STATUS.yaml
        if classification in ["SKELETON", "COMPLETO", "NOT_STARTED"]:
            if update_status_yaml(status_yaml_path, classification):
                print(f"OK {classification}")
            else:
                print(f"WARN {classification} (erro ao atualizar)")
        else:
            print(f"ERROR {classification}")

        # Armazenar resultado
        results.append({
            'rf': rf_num,
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
    print("2. Sincronizar com DevOps: python tools/devops-sync/sync-all-rfs.py")
    print("3. Validar board no Azure DevOps")

if __name__ == "__main__":
    main()
