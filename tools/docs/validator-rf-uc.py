#!/usr/bin/env python3
"""
CONTRACTUAL COVERAGE VALIDATOR v2.0 - ZERO TOLERANCE
Validador de Cobertura RF → UC com Regra de ZERO TOLERÂNCIA para Gaps

Validações obrigatórias:
1) UC cobre 100% do RF
2) UC NÃO cria comportamento fora do RF (exit 11)
3) RF possui UCs obrigatórios (UC00–UC04)
4) TC cobre 100% dos UCs (granular ou fallback)
5) Nomenclatura de fluxos (FA-UCNN-NNN vs FA-NNN) ← NOVO BLOQUEANTE

Exit Codes Contratuais (ZERO TOLERANCE):
10 - RF não totalmente coberto por UC (CRÍTICO - BLOQUEANTE)
11 - UC criou comportamento fora do RF (IMPORTANTE - BLOQUEANTE)
12 - UCs obrigatórios ausentes (CRÍTICO - BLOQUEANTE)
20 - TC não cobre 100% dos UCs (IMPORTANTE - BLOQUEANTE)
30 - Nomenclatura de fluxos incorreta (CRÍTICO - BLOQUEANTE) ← NOVO
0  - PASS (100% conforme - ZERO GAPS)

REGRA DE ZERO TOLERÂNCIA:
- APROVADO = Exit code 0 (100% conforme, ZERO gaps)
- REPROVADO = Exit code != 0 (QUALQUER gap REPROVA)
- Única exceção: Exit code 99 (falha técnica do validador)
"""

from __future__ import annotations
import argparse
import json
import sys
import re
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple
import yaml

# -------------------------
# Utils
# -------------------------

def load_yaml(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

def norm_id(x: str) -> str:
    return str(x).strip()

# -------------------------
# RF
# -------------------------

def collect_rf_items(rf: Dict[str, Any]) -> Tuple[Set[str], Dict[str, Dict[str, Any]]]:
    """
    Coleta itens do RF (Requisito Funcional).
    Suporta AMBOS os formatos:
    - regras_negocio (PADRÃO OFICIAL v2.0 - PREFERENCIAL)
    - catalog (LEGADO - retrocompatibilidade)

    Prioridade: regras_negocio > catalog
    """
    all_items: Set[str] = set()
    meta: Dict[str, Dict[str, Any]] = {}

    # PRIORIDADE 1: regras_negocio (padrão oficial)
    regras_negocio = rf.get("regras_negocio", [])
    if regras_negocio and isinstance(regras_negocio, list):
        for rn in regras_negocio:
            if not isinstance(rn, dict):
                continue
            _id = norm_id(rn.get("id", ""))
            if not _id:
                continue

            required = bool(rn.get("required", True))
            meta[_id] = {
                "group": "regras_negocio",
                "title": rn.get("titulo", "") or rn.get("title", ""),
                "description": rn.get("descricao", "") or rn.get("description", ""),
                "required": required,
                "source": "regras_negocio"  # Marca origem
            }
            all_items.add(_id)

        return all_items, meta

    # PRIORIDADE 2: catalog (retrocompatibilidade com formato legado)
    catalog = rf.get("catalog", {})
    if catalog:
        for group, items in catalog.items():
            if not isinstance(items, list):
                continue
            for it in items:
                if not isinstance(it, dict):
                    continue
                _id = norm_id(it.get("id", ""))
                if not _id:
                    continue

                required = bool(it.get("required", True))
                meta[_id] = {
                    "group": group,
                    "title": it.get("title") or "",
                    "description": it.get("description") or "",
                    "required": required,
                    "source": "catalog"  # Marca origem
                }
                all_items.add(_id)

    return all_items, meta

# -------------------------
# UC
# -------------------------

def collect_uc_coverage(uc: Dict[str, Any]):
    # Suporta ambas as chaves: "casos_de_uso" (padrão atual) e "ucs" (legado)
    ucs = uc.get("casos_de_uso", []) or uc.get("ucs", []) or []

    documentacao_items_covered: Set[str] = set()
    uc_ids: Set[str] = set()
    uc_items_required: Set[str] = set()
    ucitem_meta: Dict[str, Dict[str, Any]] = {}

    for u in ucs:
        if not isinstance(u, dict):
            continue

        uc_id = norm_id(u.get("id", ""))
        if not uc_id:
            continue

        uc_ids.add(uc_id)

        covers = u.get("covers", {}) or {}
        for rid in covers.get("rf_items", []) or []:
            documentacao_items_covered.add(norm_id(rid))

        for item in covers.get("uc_items", []) or []:
            if not isinstance(item, dict):
                continue
            iid = norm_id(item.get("id", ""))
            if not iid:
                continue

            required = bool(item.get("required", True))
            ucitem_meta[iid] = {
                "uc_id": uc_id,
                "title": item.get("title") or "",
                "required": required
            }
            if required:
                uc_items_required.add(iid)

    return documentacao_items_covered, uc_ids, uc_items_required, ucitem_meta

# -------------------------
# TC
# -------------------------

def collect_tc_coverage(tc: Dict[str, Any]):
    test_cases = tc.get("test_cases", []) or []

    ucs_tested: Set[str] = set()
    uc_items_tested: Set[str] = set()

    for t in test_cases:
        if not isinstance(t, dict):
            continue

        uc_ref = t.get("uc_ref") or ""
        if uc_ref:
            ucs_tested.add(norm_id(uc_ref))

        covers = t.get("covers", {}) or {}
        for iid in covers.get("uc_items", []) or []:
            uc_items_tested.add(norm_id(iid))

    return ucs_tested, uc_items_tested

# -------------------------
# NOVO: Validação Nomenclatura Fluxos
# -------------------------

def validate_flow_nomenclature(uc_md_path: str) -> Tuple[int, List[str]]:
    """
    Valida nomenclatura de fluxos no UC.md
    Retorna: (total_violations, examples)
    """
    if not Path(uc_md_path).exists():
        return 0, []

    with open(uc_md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Buscar violações: FA-001, FE-001 (padrão antigo - INCORRETO)
    violations_fa = re.findall(r'\*\*(FA)-(\d{3}):\*\*', content)
    violations_fe = re.findall(r'\*\*(FE)-(\d{3}):\*\*', content)

    total_violations = len(violations_fa) + len(violations_fe)

    examples = []
    for tipo, num in violations_fa[:3]:  # Mostrar até 3 exemplos
        examples.append(f"FA-{num}")
    for tipo, num in violations_fe[:3]:
        examples.append(f"FE-{num}")

    return total_violations, examples

# -------------------------
# Exclusions
# -------------------------

def apply_exclusions(items: Set[str], exclusions: List[Dict[str, Any]]) -> Set[str]:
    remaining = set(items)
    for ex in exclusions or []:
        ex_id = norm_id(ex.get("id", ""))
        if ex_id in remaining:
            remaining.remove(ex_id)
    return remaining

# -------------------------
# Main
# -------------------------

def main():
    ap = argparse.ArgumentParser(
        description="Validador RF → UC com ZERO TOLERANCE (v2.0)"
    )
    ap.add_argument("--rf", required=True, help="Caminho para RF.yaml")
    ap.add_argument("--uc", required=True, help="Caminho para UC.yaml")
    ap.add_argument("--tc", required=False, default=None, help="Caminho para TC.yaml (opcional)")
    ap.add_argument("--out", default="coverage-report.md", help="Relatório Markdown")
    ap.add_argument("--out-json", default="coverage-report.json", help="Relatório JSON")
    args = ap.parse_args()

    try:
        documentacao = load_yaml(args.rf)
        uc = load_yaml(args.uc)
        tc = load_yaml(args.tc) if args.tc else {}
    except Exception as e:
        print(f"❌ ERRO TÉCNICO: Falha ao carregar arquivos YAML: {e}", file=sys.stderr)
        sys.exit(99)  # Exit code 99 = Falha técnica do validador

    # RF
    documentacao_all, documentacao_meta = collect_rf_items(rf)
    documentacao_required = {i for i in documentacao_all if documentacao_meta[i]["required"]}
    documentacao_required = apply_exclusions(
        documentacao_required,
        rf.get("exclusions", {}).get("rf_items", [])
    )

    # UC
    documentacao_items_covered, uc_ids, uc_items_required, ucitem_meta = collect_uc_coverage(uc)

    # CONTRATO: UCs obrigatórios
    MANDATORY_UCS = {"UC00", "UC01", "UC02", "UC03", "UC04"}
    missing_mandatory_ucs = MANDATORY_UCS - uc_ids

    # CONTRATO: UC não cria comportamento fora do RF
    uc_outside_rf = documentacao_items_covered - documentacao_required

    # NOVO: Validar nomenclatura de fluxos
    uc_md_path = args.uc.replace(".yaml", ".md")
    flow_violations, flow_examples = validate_flow_nomenclature(uc_md_path)

    # TC
    ucs_tested, uc_items_tested = collect_tc_coverage(tc)

    # TC granular se existir
    use_granular = len(uc_items_required) > 0
    uc_items_required = apply_exclusions(
        uc_items_required,
        uc.get("exclusions", {}).get("uc_items", [])
    )

    if use_granular:
        tc_missing = uc_items_required - uc_items_tested
    else:
        tc_missing = uc_ids - ucs_tested

    # -------------------------
    # Report (JSON)
    # -------------------------

    report = {
        "validator_version": "2.0-ZERO-TOLERANCE",
        "zero_tolerance": True,
        "checks": {
            "uc_covers_rf": {
                "required": sorted(rf_required),
                "covered": sorted(rf_items_covered & documentacao_required),
                "missing": sorted(rf_required - documentacao_items_covered),
                "severity": "CRÍTICO",
                "blocker": True
            },
            "uc_outside_rf": {
                "extra_items": sorted(uc_outside_rf),
                "severity": "IMPORTANTE",
                "blocker": True
            },
            "mandatory_ucs": {
                "required": sorted(MANDATORY_UCS),
                "present": sorted(uc_ids),
                "missing": sorted(missing_mandatory_ucs),
                "severity": "CRÍTICO",
                "blocker": True
            },
            "flow_nomenclature": {
                "violations": flow_violations,
                "examples": flow_examples,
                "severity": "CRÍTICO" if flow_violations > 0 else "OK",
                "blocker": flow_violations > 0
            },
            "tc_covers_uc": {
                "missing": sorted(tc_missing),
                "mode": "granular" if use_granular else "uc_only",
                "severity": "IMPORTANTE",
                "blocker": args.tc is not None and len(tc_missing) > 0
            }
        },
        "summary": {
            "total_checks": 5,
            "passed": 0,
            "failed": 0,
            "gaps_critical": 0,
            "gaps_important": 0,
            "gaps_minor": 0
        }
    }

    # Contar passes/fails
    checks_status = [
        len(report['checks']['uc_covers_rf']['missing']) == 0,
        len(report['checks']['uc_outside_rf']['extra_items']) == 0,
        len(report['checks']['mandatory_ucs']['missing']) == 0,
        flow_violations == 0,
        not (args.tc and tc_missing)
    ]

    report['summary']['passed'] = sum(checks_status)
    report['summary']['failed'] = len(checks_status) - sum(checks_status)

    # Contar gaps por severidade
    if report['checks']['uc_covers_rf']['missing']:
        report['summary']['gaps_critical'] += 1
    if report['checks']['uc_outside_rf']['extra_items']:
        report['summary']['gaps_important'] += 1
    if report['checks']['mandatory_ucs']['missing']:
        report['summary']['gaps_critical'] += 1
    if flow_violations > 0:
        report['summary']['gaps_critical'] += 1
    if args.tc and tc_missing:
        report['summary']['gaps_important'] += 1

    # -------------------------
    # Report (Markdown)
    # -------------------------

    md = []
    md.append("# RELATÓRIO DE VALIDAÇÃO RF → UC")
    md.append(f"**Validador:** v2.0 - ZERO TOLERANCE")
    md.append(f"**RF:** {Path(args.rf).name}")
    md.append(f"**UC:** {Path(args.uc).name}")
    md.append("")
    md.append("---")
    md.append("")

    # RESUMO EXECUTIVO
    md.append("## RESUMO EXECUTIVO")
    md.append("")
    md.append("| Validação | Status | Severidade | Resultado |")
    md.append("|-----------|--------|------------|-----------|")

    # Validação 1: Cobertura RN → UC
    missing_count = len(report['checks']['uc_covers_rf']['missing'])
    total_count = len(rf_required)
    covered_count = len(report['checks']['uc_covers_rf']['covered'])
    status_1 = "✅ PASS" if missing_count == 0 else "❌ FAIL"
    md.append(f"| 1. Cobertura RN → UC | {status_1} | CRÍTICO | {covered_count}/{total_count} ({100*covered_count//total_count if total_count > 0 else 0}%) |")

    # Validação 2: UC não cria comportamento fora do RF
    extra_count = len(report['checks']['uc_outside_rf']['extra_items'])
    status_2 = "✅ PASS" if extra_count == 0 else "❌ FAIL"
    md.append(f"| 2. UC não cria comportamento fora RF | {status_2} | IMPORTANTE | {extra_count} itens extras |")

    # Validação 3: UCs obrigatórios
    missing_uc_count = len(report['checks']['mandatory_ucs']['missing'])
    status_3 = "✅ PASS" if missing_uc_count == 0 else "❌ FAIL"
    md.append(f"| 3. UCs obrigatórios (UC00-UC04) | {status_3} | CRÍTICO | {5 - missing_uc_count}/5 presentes |")

    # Validação 3.5: Nomenclatura de fluxos
    status_35 = "✅ PASS" if flow_violations == 0 else "❌ FAIL"
    md.append(f"| **3.5. Nomenclatura de fluxos** | **{status_35}** | **CRÍTICO** | **{flow_violations} violações** |")

    # Validação 4: TC cobre UC (se TC fornecido)
    if args.tc:
        tc_missing_count = len(tc_missing)
        status_4 = "✅ PASS" if tc_missing_count == 0 else "❌ FAIL"
        md.append(f"| 4. TC cobre 100% dos UCs | {status_4} | IMPORTANTE | {tc_missing_count} itens faltando |")
    else:
        md.append(f"| 4. TC cobre 100% dos UCs | N/A | IMPORTANTE | TC não fornecido |")

    md.append("")
    md.append(f"**PONTUAÇÃO FINAL:** {report['summary']['passed']}/{report['summary']['total_checks']} PASS ({100*report['summary']['passed']//report['summary']['total_checks']}%)")
    md.append("")

    # VEREDICTO
    all_pass = report['summary']['failed'] == 0
    if all_pass:
        md.append("**VEREDICTO:** ✅ **APROVADO** - UC-RFXXX está 100% conforme (ZERO GAPS)")
    else:
        md.append("**VEREDICTO:** ❌ **REPROVADO** - Gaps detectados (ZERO TOLERANCE)")
        md.append("")
        md.append(f"**Gaps CRÍTICOS:** {report['summary']['gaps_critical']}")
        md.append(f"**Gaps IMPORTANTES:** {report['summary']['gaps_important']}")
        md.append(f"**Gaps MENORES:** {report['summary']['gaps_minor']}")

    md.append("")
    md.append("---")
    md.append("")

    # GAPS IDENTIFICADOS (se houver)
    if not all_pass:
        md.append("## GAPS IDENTIFICADOS")
        md.append("")

        # Gap 1: RNs não cobertas
        if missing_count > 0:
            md.append(f"### Gap 1: RNs Não Cobertas ({missing_count})")
            md.append(f"**Severidade:** CRÍTICO (BLOQUEANTE)")
            md.append("")
            md.append("**RNs faltando:**")
            for rn_id in sorted(report['checks']['uc_covers_rf']['missing']):
                meta = documentacao_meta.get(rn_id, {})
                title = meta.get('title', 'N/A')
                md.append(f"- `{rn_id}`: {title}")
            md.append("")
            md.append("**Ação:** Criar UCs para cobrir estas RNs.")
            md.append("")

        # Gap 2: UC cria comportamento fora do RF
        if extra_count > 0:
            md.append(f"### Gap 2: UC Cria Comportamento Fora do RF ({extra_count})")
            md.append(f"**Severidade:** IMPORTANTE (BLOQUEANTE)")
            md.append("")
            md.append("**Itens extras no UC que não existem no RF:**")
            for item_id in sorted(report['checks']['uc_outside_rf']['extra_items']):
                md.append(f"- `{item_id}`")
            md.append("")
            md.append("**Ação:** Remover estes itens do UC.yaml ou adicionar ao RF.yaml.")
            md.append("")

        # Gap 3: UCs obrigatórios ausentes
        if missing_uc_count > 0:
            md.append(f"### Gap 3: UCs Obrigatórios Ausentes ({missing_uc_count})")
            md.append(f"**Severidade:** CRÍTICO (BLOQUEANTE)")
            md.append("")
            md.append("**UCs faltando:**")
            for uc_id in sorted(report['checks']['mandatory_ucs']['missing']):
                md.append(f"- `{uc_id}`")
            md.append("")
            md.append("**Ação:** Criar os UCs obrigatórios (UC00-UC04).")
            md.append("")

        # Gap 3.5: Nomenclatura de fluxos incorreta
        if flow_violations > 0:
            md.append(f"### Gap 3.5: Nomenclatura de Fluxos Incorreta ({flow_violations} violações)")
            md.append(f"**Severidade:** CRÍTICO (BLOQUEANTE)")
            md.append("")
            md.append("**Padrão incorreto encontrado:**")
            for example in flow_examples:
                md.append(f"- `{example}` (deve ser `{example[:2]}-UC00-{example[3:]}` ou similar)")
            md.append("")
            md.append("**Ação:** Executar script de migração de nomenclatura:")
            md.append("```bash")
            md.append(f"python .temp_ia/migrate_flow_nomenclature.py {Path(args.uc).stem}")
            md.append("```")
            md.append("")

        # Gap 4: TC não cobre UCs
        if args.tc and tc_missing:
            tc_missing_count = len(tc_missing)
            md.append(f"### Gap 4: TC Não Cobre 100% dos UCs ({tc_missing_count})")
            md.append(f"**Severidade:** IMPORTANTE (BLOQUEANTE)")
            md.append("")
            md.append("**Itens faltando cobertura de testes:**")
            for item_id in sorted(tc_missing)[:10]:  # Mostrar até 10
                md.append(f"- `{item_id}`")
            if tc_missing_count > 10:
                md.append(f"... e mais {tc_missing_count - 10} itens")
            md.append("")
            md.append("**Ação:** Criar casos de teste para cobrir estes itens.")
            md.append("")

    else:
        md.append("## GAPS IDENTIFICADOS")
        md.append("")
        md.append("**Nenhum gap identificado.** ✅")
        md.append("")

    md.append("---")
    md.append("")

    # RECOMENDAÇÕES
    if all_pass:
        md.append("## RECOMENDAÇÕES")
        md.append("")
        md.append("Nenhuma ação corretiva necessária. UC-RFXXX pode prosseguir para próximo contrato.")
    else:
        md.append("## RECOMENDAÇÕES")
        md.append("")
        md.append("**BLOQUEIO:** RF NÃO pode prosseguir até corrigir TODOS os gaps.")
        md.append("")
        md.append("**Ações obrigatórias:**")
        if missing_count > 0:
            md.append(f"1. Criar UCs para cobrir {missing_count} RNs faltando")
        if extra_count > 0:
            md.append(f"2. Remover {extra_count} itens do UC que não existem no RF")
        if missing_uc_count > 0:
            md.append(f"3. Criar {missing_uc_count} UCs obrigatórios (UC00-UC04)")
        if flow_violations > 0:
            md.append(f"4. Corrigir {flow_violations} violações de nomenclatura de fluxos")
        if args.tc and tc_missing:
            md.append(f"5. Criar testes para cobrir {tc_missing_count} itens")
        md.append("")
        md.append("**Após correções:** Re-executar validador até exit code 0.")

    md.append("")
    md.append("---")
    md.append("")
    md.append("**Fim do Relatório**")

    # -------------------------
    # Outputs
    # -------------------------

    with open(args.out_json, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    with open(args.out, "w", encoding="utf-8") as f:
        f.write("\n".join(md))

    # -------------------------
    # EXIT CODES CONTRATUAIS (ZERO TOLERANCE)
    # -------------------------

    # CRÍTICO: UCs obrigatórios ausentes
    if missing_mandatory_ucs:
        print(f"❌ EXIT CODE 12: UCs obrigatórios ausentes ({len(missing_mandatory_ucs)})", file=sys.stderr)
        sys.exit(12)

    # IMPORTANTE: UC criou comportamento fora do RF
    if uc_outside_rf:
        print(f"❌ EXIT CODE 11: UC criou comportamento fora do RF ({len(uc_outside_rf)} itens)", file=sys.stderr)
        sys.exit(11)

    # CRÍTICO: RF não totalmente coberto
    if report["checks"]["uc_covers_rf"]["missing"]:
        print(f"❌ EXIT CODE 10: RF não totalmente coberto ({len(report['checks']['uc_covers_rf']['missing'])} RNs faltando)", file=sys.stderr)
        sys.exit(10)

    # NOVO: CRÍTICO: Nomenclatura de fluxos incorreta
    if flow_violations > 0:
        print(f"❌ EXIT CODE 30: Nomenclatura de fluxos incorreta ({flow_violations} violações)", file=sys.stderr)
        sys.exit(30)

    # IMPORTANTE: TC não cobre 100% (só valida se TC fornecido)
    if args.tc and tc_missing:
        print(f"❌ EXIT CODE 20: TC não cobre 100% dos UCs ({len(tc_missing)} itens faltando)", file=sys.stderr)
        sys.exit(20)

    # APROVADO: Exit code 0
    print("✅ EXIT CODE 0: APROVADO - 100% conforme (ZERO GAPS)")
    sys.exit(0)

if __name__ == "__main__":
    main()
