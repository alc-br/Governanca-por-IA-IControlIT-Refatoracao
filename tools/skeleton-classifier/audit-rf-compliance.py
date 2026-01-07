#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Auditoria Profunda: Conformidade RF vs Implementação

Para cada RF com código implementado, este script:
1. Lê o RF.md para entender o que deveria ser implementado
2. Analisa o backend para verificar conformidade
3. Analisa o frontend para verificar conformidade
4. Classifica como:
   - SKELETON: Backend/Frontend existem mas não implementam tudo do RF
   - COMPLETO: Backend/Frontend implementam tudo do RF
   - PARCIAL: Apenas backend OU apenas frontend implementado

Uso:
    python audit-rf-compliance.py
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
REPORT_FILE = f"{REPORT_PATH}/{datetime.now().strftime('%Y-%m-%d-%H%M')}-AUDITORIA-CONFORMIDADE-RFS.md"

# Estatísticas
stats = {
    "total_auditados": 0,
    "skeleton_confirmado": 0,
    "completo_confirmado": 0,
    "parcial": 0,
    "reclassificacoes": 0
}

audit_results = []

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

def extract_rf_number(path):
    """Extrai número do RF do caminho"""
    match = re.search(r'RF(\d+)', path)
    if match:
        return f"RF{int(match.group(1)):03d}"
    return None

def find_rf_md(rf_num):
    """Encontra o arquivo RF.md para um RF"""
    pattern = f"{DOCS_RF_PATH}/**/{rf_num}*.md"
    files = glob.glob(pattern, recursive=True)

    # Procurar especificamente por RF-XXX.md ou RFXXX.md
    for f in files:
        if f.endswith(f"{rf_num}.md") or f.endswith(f"{rf_num[2:]}.md"):
            return f

    return None

def extract_business_rules_from_rf(rf_md_path):
    """
    Extrai regras de negócio do RF.md
    Retorna lista de indicadores do que deveria estar implementado
    """
    if not documentacao_md_path or not os.path.exists(rf_md_path):
        return {"error": "RF.md não encontrado", "rules": []}

    try:
        with open(rf_md_path, 'r', encoding='utf-8') as f:
            content = f.read()

        indicators = {
            "has_validations": False,
            "has_states": False,
            "has_workflows": False,
            "has_business_rules": False,
            "has_calculations": False,
            "rules_count": 0,
            "validation_keywords": [],
            "state_keywords": [],
            "workflow_keywords": []
        }

        # Procurar por seções de regras
        if re.search(r'## .*Regras', content, re.IGNORECASE):
            indicators["has_business_rules"] = True
            # Contar regras numeradas
            rules = re.findall(r'^\s*\d+\.', content, re.MULTILINE)
            indicators["rules_count"] = len(rules)

        # Procurar por validações
        validation_keywords = ['validar', 'validação', 'obrigatório', 'não pode', 'deve ser']
        for keyword in validation_keywords:
            if keyword.lower() in content.lower():
                indicators["has_validations"] = True
                indicators["validation_keywords"].append(keyword)

        # Procurar por estados
        state_keywords = ['status', 'estado', 'aprovado', 'rejeitado', 'pendente', 'ativo', 'inativo']
        for keyword in state_keywords:
            if keyword.lower() in content.lower():
                indicators["has_states"] = True
                indicators["state_keywords"].append(keyword)

        # Procurar por workflows
        workflow_keywords = ['aprovar', 'rejeitar', 'workflow', 'fluxo', 'processo']
        for keyword in workflow_keywords:
            if keyword.lower() in content.lower():
                indicators["has_workflows"] = True
                indicators["workflow_keywords"].append(keyword)

        # Procurar por cálculos
        if re.search(r'calcul|cálculo|soma|total|média', content, re.IGNORECASE):
            indicators["has_calculations"] = True

        return indicators

    except Exception as e:
        return {"error": str(e), "rules": []}

def analyze_backend_completeness(rf_num, documentacao_indicators):
    """
    Analisa se o backend implementou tudo do RF
    """
    # Procurar entidade no Domain
    entity_pattern = f"{BACKEND_PATH}/Domain/Entities/*.cs"
    entity_files = glob.glob(entity_pattern)

    # Procurar arquivos de Application
    app_pattern = f"{BACKEND_PATH}/Application/**/*.cs"
    app_files = glob.glob(app_pattern, recursive=True)

    all_files = entity_files + app_files

    if not all_files:
        return {"implemented": False, "details": "Nenhum arquivo backend encontrado"}

    # Analisar conteúdo
    has_complex_validators = False
    has_state_enum = False
    has_workflow_logic = False
    has_calculation_logic = False
    validator_count = 0

    for file_path in all_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Verificar validators
            if 'FluentValidation' in content:
                rule_matches = re.findall(r'RuleFor', content)
                validator_count += len(rule_matches)
                if len(rule_matches) > 5:  # Mais de 5 regras = complexo
                    has_complex_validators = True

            # Verificar estados
            if 'enum' in content and any(kw in content for kw in ['Status', 'State', 'Situacao']):
                has_state_enum = True

            # Verificar workflows
            if any(kw in content for kw in ['Approve', 'Reject', 'Process', 'Workflow']):
                has_workflow_logic = True

            # Verificar cálculos
            if any(kw in content for kw in ['Calculate', 'Compute', 'Sum', 'Total']):
                has_calculation_logic = True

        except:
            pass

    # Comparar com o que deveria ter
    gaps = []

    if documentacao_indicators.get("has_validations") and not has_complex_validators:
        gaps.append("Validações complexas esperadas mas não encontradas")

    if documentacao_indicators.get("has_states") and not has_state_enum:
        gaps.append("Estados/Status esperados mas não encontrados")

    if documentacao_indicators.get("has_workflows") and not has_workflow_logic:
        gaps.append("Workflows esperados mas não encontrados")

    if documentacao_indicators.get("has_calculations") and not has_calculation_logic:
        gaps.append("Cálculos esperados mas não encontrados")

    # Se RF tem muitas regras (>10) mas backend tem poucas validações
    if documentacao_indicators.get("rules_count", 0) > 10 and validator_count < 5:
        gaps.append(f"RF tem {rf_indicators['rules_count']} regras mas backend tem apenas {validator_count} validações")

    is_complete = len(gaps) == 0

    return {
        "implemented": len(all_files) > 0,
        "is_complete": is_complete,
        "gaps": gaps,
        "details": {
            "files_count": len(all_files),
            "has_complex_validators": has_complex_validators,
            "validator_count": validator_count,
            "has_state_enum": has_state_enum,
            "has_workflow_logic": has_workflow_logic,
            "has_calculation_logic": has_calculation_logic
        }
    }

def analyze_frontend_completeness(rf_num):
    """
    Analisa se o frontend está implementado
    """
    # Procurar componentes
    pattern = f"{FRONTEND_PATH}/modules/admin/management/**/*.ts"
    files = glob.glob(pattern, recursive=True)

    if not files:
        return {"implemented": False, "details": "Nenhum arquivo frontend encontrado"}

    has_advanced_validations = False
    has_state_management = False
    has_workflow_ui = False

    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Verificar validações avançadas
            if 'Validators.pattern' in content or 'Validators.email' in content:
                has_advanced_validations = True

            # Verificar gerenciamento de estados
            if any(kw in content.lower() for kw in ['status', 'state', 'aprovado', 'rejeitado']):
                has_state_management = True

            # Verificar UI de workflow
            if any(kw in content.lower() for kw in ['aprovar', 'rejeitar', 'workflow']):
                has_workflow_ui = True

        except:
            pass

    return {
        "implemented": len(files) > 0,
        "details": {
            "files_count": len(files),
            "has_advanced_validations": has_advanced_validations,
            "has_state_management": has_state_management,
            "has_workflow_ui": has_workflow_ui
        }
    }

def audit_rf(status_yaml_path):
    """
    Audita um RF comparando especificação com implementação
    """
    documentacao_num = extract_rf_number(status_yaml_path)
    if not documentacao_num:
        return None

    # Ler STATUS.yaml
    try:
        with open(status_yaml_path, 'r', encoding='utf-8') as f:
            status_data = parse_yaml_simple(f.read())
    except:
        return None

    # Verificar se tem implementação
    dev = status_data.get('desenvolvimento', {})
    backend_status = dev.get('backend', {}).get('status', 'not_started')
    frontend_status = dev.get('frontend', {}).get('status', 'not_started')

    # Só auditar se houver alguma implementação
    if backend_status == 'not_started' and frontend_status == 'not_started':
        return None

    titulo = status_data.get('titulo', 'Sem título')

    # Encontrar RF.md
    documentacao_md_path = find_rf_md(rf_num)

    # Extrair regras do RF
    documentacao_indicators = extract_business_rules_from_rf(rf_md_path)

    # Analisar backend
    backend_analysis = analyze_backend_completeness(rf_num, documentacao_indicators)

    # Analisar frontend
    frontend_analysis = analyze_frontend_completeness(rf_num)

    # Determinar classificação
    backend_impl = backend_analysis["implemented"]
    frontend_impl = frontend_analysis["implemented"]
    backend_complete = backend_analysis.get("is_complete", False)

    if backend_impl and frontend_impl:
        if backend_complete:
            classification = "COMPLETO"
        else:
            classification = "SKELETON"
    elif backend_impl or frontend_impl:
        classification = "PARCIAL"
    else:
        classification = "NOT_STARTED"

    # Classificação atual
    current_classification = "SKELETON" if status_data.get('skeleton', {}).get('criado', False) else None
    if backend_status == 'done' and frontend_status == 'done':
        current_classification = "COMPLETO"

    needs_reclassification = current_classification != classification

    return {
        "rf": documentacao_num,
        "titulo": titulo,
        "rf_md_path": documentacao_md_path,
        "rf_indicators": documentacao_indicators,
        "backend_analysis": backend_analysis,
        "frontend_analysis": frontend_analysis,
        "classification": classification,
        "current_classification": current_classification,
        "needs_reclassification": needs_reclassification,
        "status_yaml_path": status_yaml_path
    }

def generate_report():
    """Gera relatório de auditoria"""
    os.makedirs(REPORT_PATH, exist_ok=True)

    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write("# RELATÓRIO DE AUDITORIA DE CONFORMIDADE\n\n")
        f.write(f"**Data:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("**Objetivo:** Validar se implementação está conforme RF especificado\n\n")
        f.write("---\n\n")
        f.write("## ESTATÍSTICAS\n\n")
        f.write(f"| Categoria | Quantidade |\n")
        f.write(f"|-----------|------------|\n")
        f.write(f"| Total Auditados | {stats['total_auditados']} |\n")
        f.write(f"| **Skeleton Confirmado** | **{stats['skeleton_confirmado']}** |\n")
        f.write(f"| Completo Confirmado | {stats['completo_confirmado']} |\n")
        f.write(f"| Parcial | {stats['parcial']} |\n")
        f.write(f"| **Reclassificações Necessárias** | **{stats['reclassificacoes']}** |\n")
        f.write("\n---\n\n")

        # RFs que precisam reclassificação
        needs_reclass = [r for r in audit_results if r["needs_reclassification"]]
        if needs_reclass:
            f.write(f"## RFS QUE PRECISAM RECLASSIFICAÇÃO ({len(needs_reclass)})\n\n")
            for result in needs_reclass:
                f.write(f"### {result['rf']} - {result['titulo'][:50]}\n\n")
                f.write(f"**Classificação Atual:** {result['current_classification']}\n")
                f.write(f"**Classificação Correta:** {result['classification']}\n\n")

                if result['backend_analysis']['gaps']:
                    f.write(f"**Gaps no Backend:**\n")
                    for gap in result['backend_analysis']['gaps']:
                        f.write(f"- {gap}\n")
                    f.write("\n")

                f.write("---\n\n")

        # Skeleton Confirmados
        skeletons = [r for r in audit_results if r["classification"] == "SKELETON"]
        if skeletons:
            f.write(f"## RFS SKELETON CONFIRMADOS ({len(skeletons)})\n\n")
            f.write("| RF | Título | Gaps Backend |\n")
            f.write("|----|--------|-------------|\n")
            for result in skeletons:
                gaps_summary = "; ".join(result['backend_analysis']['gaps'][:2])
                if len(result['backend_analysis']['gaps']) > 2:
                    gaps_summary += "..."
                f.write(f"| {result['rf']} | {result['titulo'][:30]} | {gaps_summary} |\n")
            f.write("\n")

        # Completos Confirmados
        completos = [r for r in audit_results if r["classification"] == "COMPLETO"]
        if completos:
            f.write(f"## RFS COMPLETOS CONFIRMADOS ({len(completos)})\n\n")
            f.write("| RF | Título | Backend | Frontend |\n")
            f.write("|----|--------|---------|----------|\n")
            for result in completos:
                backend_ok = "OK" if result['backend_analysis']['is_complete'] else "Gaps"
                frontend_ok = "OK" if result['frontend_analysis']['implemented'] else "Não impl"
                f.write(f"| {result['rf']} | {result['titulo'][:30]} | {backend_ok} | {frontend_ok} |\n")
            f.write("\n")

        f.write("---\n\n")
        f.write("**FIM DO RELATÓRIO**\n")

    print(f"\n[OK] Relatório gerado: {REPORT_FILE}")

def main():
    print("=" * 80)
    print("AUDITORIA PROFUNDA: CONFORMIDADE RF vs IMPLEMENTAÇÃO")
    print("=" * 80)
    print()

    # Listar todos os STATUS.yaml
    status_files = glob.glob(f"{DOCS_RF_PATH}/**/STATUS.yaml", recursive=True)

    print(f"[INFO] Encontrados {len(status_files)} RFs")
    print()

    # Auditar cada RF
    for i, status_yaml_path in enumerate(sorted(status_files), 1):
        documentacao_num = extract_rf_number(status_yaml_path)
        print(f"[{i}/{len(status_files)}] Auditando {rf_num}...", end=" ")

        result = audit_rf(status_yaml_path)

        if result:
            stats['total_auditados'] += 1

            if result['classification'] == 'SKELETON':
                stats['skeleton_confirmado'] += 1
            elif result['classification'] == 'COMPLETO':
                stats['completo_confirmado'] += 1
            elif result['classification'] == 'PARCIAL':
                stats['parcial'] += 1

            if result['needs_reclassification']:
                stats['reclassificacoes'] += 1
                print(f"RECLASS {result['current_classification']} -> {result['classification']}")
            else:
                print(f"OK {result['classification']}")

            audit_results.append(result)
        else:
            print("SKIP (não implementado)")

    print()
    print("=" * 80)
    print("ESTATÍSTICAS FINAIS")
    print("=" * 80)
    print(f"Total Auditados:         {stats['total_auditados']}")
    print(f"Skeleton Confirmado:     {stats['skeleton_confirmado']}")
    print(f"Completo Confirmado:     {stats['completo_confirmado']}")
    print(f"Parcial:                 {stats['parcial']}")
    print(f"Reclassificações:        {stats['reclassificacoes']}")
    print("=" * 80)
    print()

    # Gerar relatório
    generate_report()

    print()
    print("[OK] Auditoria concluída!")
    print(f"[OK] Relatório: {REPORT_FILE}")

if __name__ == "__main__":
    main()
