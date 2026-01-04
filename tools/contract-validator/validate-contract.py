import os
import sys
import subprocess
import yaml
import re

ROOT = os.getcwd()

MANIFEST_PATH = "docs/contracts/EXECUTION-MANIFEST.md"
TRANSITIONS_PATH = "docs/contracts/contract-transitions.yaml"

# -----------------------------
# DEFINIÇÃO DOS CONTRATOS
# -----------------------------
CONTRACTS = {
    "DEBUG": {
        "key": "debug",
        "contract": "docs/contracts/CONTRATO-DEBUG-CONTROLADO.md",
        "checklist": "docs/checklists/CHECKLIST-CONTRATO-DEBUG.yaml",
        "allow_commits": False,
    },
    "TESTES": {
        "key": "testes",
        "contract": "docs/contracts/CONTRATO-EXECUCAO-TESTES.md",
        "checklist": "docs/checklists/CHECKLIST-CONTRATO-TESTES.yaml",
        "allow_commits": False,
    },
    "FRONTEND": {
        "key": "frontend",
        "contract": "docs/contracts/CONTRATO-EXECUCAO-FRONTEND.md",
        "checklist": "docs/checklists/CHECKLIST-CONTRATO-FRONTEND.yaml",
        "allow_commits": True,
    },
    "BACKEND": {
        "key": "backend",
        "contract": "docs/contracts/CONTRATO-EXECUCAO-BACKEND.md",
        "checklist": "docs/checklists/CHECKLIST-CONTRATO-BACKEND.yaml",
        "allow_commits": True,
    },
    "MANUTENCAO": {
        "key": "manutencao",
        "contract": "docs/contracts/CONTRATO-MANUTENCAO-CORRECAO-CONTROLADA.md",
        "checklist": "docs/checklists/CHECKLIST-CONTRATO-MANUTENCAO.yaml",
        "allow_commits": True,
    },
    "DEVOPS": {
        "key": "devops",
        "contract": "docs/contracts/CONTRATO-DEVOPS-GOVERNANCA.md",
        "checklist": "docs/checklists/CHECKLIST-CONTRATO-DEVOPS.yaml",
        "allow_commits": True,
    },
    "DOCUMENTACAO": {
        "key": "documentacao",
        "contract": "docs/contracts/CONTRATO-DOCUMENTACAO-GOVERNADA.md",
        "checklist": "docs/checklists/CHECKLIST-CONTRATO-DOCUMENTACAO.yaml",
        "allow_commits": False,
    },
}

# -----------------------------
# HELPERS DE OUTPUT
# -----------------------------
def fail(msg):
    print(f"\n❌ CONTRACT VALIDATION FAILED\n{msg}\n")
    sys.exit(1)


def ok(msg):
    print(f"✅ {msg}")


def info(msg):
    print(f"ℹ️ {msg}")


# -----------------------------
# VALIDAÇÕES BÁSICAS
# -----------------------------
def file_must_exist(path, description):
    if not os.path.exists(path):
        fail(f"{description} não encontrado: {path}")
    ok(f"{description} encontrado")


# -----------------------------
# EXTRAÇÃO DE CONTRATO E RF
# -----------------------------
def extract_contract_and_rf(content, source):
    contract = None
    rf = None

    for name in CONTRACTS.keys():
        if re.search(rf"CONTRATO:\s*{name}", content):
            contract = name

    rf_match = re.search(r"Requisito Funcional.*:\s*(RF\d+)", content)

    if rf_match:
        rf = rf_match.group(1)

    if not contract:
        fail(f"Nenhum contrato válido encontrado em {source}")

    ok(f"Contrato identificado ({source}): {contract}")

    if rf:
        ok(f"RF identificado ({source}): {rf}")
    else:
        info("Nenhum RF identificado no manifesto")

    return contract, rf


# -----------------------------
# LEITURA DE MANIFESTOS
# -----------------------------
def read_manifest_from_pr():
    file_must_exist(MANIFEST_PATH, "Execution Manifest (PR)")
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        return extract_contract_and_rf(f.read(), "PR")


def read_manifest_from_base_branch():
    base_branch = os.getenv("SYSTEM_PULLREQUEST_TARGETBRANCH")

    if not base_branch:
        info("Execução fora de PR — transição de contrato ignorada")
        return None, None

    base_branch = base_branch.replace("refs/heads/", "origin/")

    try:
        content = subprocess.check_output(
            ["git", "show", f"{base_branch}:{MANIFEST_PATH}"],
            stderr=subprocess.STDOUT,
            text=True,
        )
    except subprocess.CalledProcessError:
        fail(
            f"Não foi possível ler EXECUTION-MANIFEST.md da branch base ({base_branch})"
        )

    return extract_contract_and_rf(content, f"branch base ({base_branch})")


# -----------------------------
# CHECKLIST E TRANSIÇÕES
# -----------------------------
def validate_contract_files(contract_name):
    cfg = CONTRACTS[contract_name]
    file_must_exist(cfg["contract"], "Contrato")
    file_must_exist(cfg["checklist"], "Checklist")
    return cfg


def load_checklist(checklist_path):
    with open(checklist_path, "r", encoding="utf-8") as f:
        checklist = yaml.safe_load(f)

    if not checklist:
        fail("Checklist está vazio ou inválido")

    ok("Checklist carregado com sucesso")
    return checklist


def load_transitions():
    file_must_exist(TRANSITIONS_PATH, "Mapa de Transições de Contrato")

    with open(TRANSITIONS_PATH, "r", encoding="utf-8") as f:
        transitions = yaml.safe_load(f)

    if not transitions or "transitions" not in transitions:
        fail("Arquivo de transições inválido")

    ok("Mapa de transições carregado")
    return transitions["transitions"]


def validate_transition(previous_contract, current_contract, transitions):
    if not previous_contract:
        info("Sem contrato anterior (build direto) — transição ignorada")
        return

    if previous_contract not in transitions:
        fail(f"Contrato anterior sem regra de transição: {previous_contract}")

    allowed = transitions[previous_contract].get("allowed_next", [])

    if current_contract not in allowed:
        fail(
            f"""
❌ TRANSIÇÃO DE CONTRATO INVÁLIDA

Contrato anterior: {previous_contract}
Contrato atual:     {current_contract}

Transições permitidas:
{allowed}

➡️ Atualize o EXECUTION-MANIFEST.md ou ajuste o fluxo corretamente.
"""
        )

    ok(f"Transição válida: {previous_contract} → {current_contract}")


# -----------------------------
# VALIDAÇÃO DO DIFF
# -----------------------------
def get_changed_files():
    base_branch = os.getenv("SYSTEM_PULLREQUEST_TARGETBRANCH")

    if not base_branch:
        info("Execução fora de PR — validação de diff ignorada")
        return []

    base_branch = base_branch.replace("refs/heads/", "origin/")

    output = subprocess.check_output(
        ["git", "diff", "--name-only", f"{base_branch}"],
        text=True,
    )

    files = [f.strip() for f in output.splitlines() if f.strip()]
    info("Arquivos alterados no PR:")
    for f in files:
        print(f" - {f}")

    return files


def validate_diff_against_contract(contract_name):
    cfg = CONTRACTS[contract_name]
    changed_files = get_changed_files()

    if not changed_files:
        info("Nenhuma alteração de arquivo detectada")
        return

    if not cfg["allow_commits"]:
        illegal = [f for f in changed_files if not f.startswith("docs/")]

        if illegal:
            fail(
                f"""
❌ ALTERAÇÕES PROIBIDAS PELO CONTRATO {contract_name}

Este contrato NÃO permite alterações de código.

Arquivos ilegais detectados:
{illegal}

➡️ Use DEBUG ou TESTES apenas para investigação.
➡️ Troque para FRONTEND / BACKEND / MANUTENCAO para alterar código.
"""
            )

        ok("Nenhuma alteração de código detectada (contrato read-only)")


# -----------------------------
# VALIDAÇÃO DE BRANCH POR RF
# -----------------------------
def validate_branch_against_rf(contract, rf):
    if not rf:
        info("Sem RF declarado — validação de branch ignorada")
        return

    branch = os.getenv("BUILD_SOURCEBRANCHNAME", "")

    if contract in ("FRONTEND", "BACKEND"):
        if rf not in branch:
            fail(
                f"""
❌ BRANCH INVÁLIDO PARA O RF

Contrato: {contract}
RF:       {rf}
Branch:   {branch}

➡️ O branch DEVE conter o identificador do RF.
Exemplos válidos:
- feature/{rf}-frontend
- feature/{rf}-backend
"""
            )

        ok(f"Branch validado para o RF {rf}")


# -----------------------------
# MAIN
# -----------------------------
def main():
    ok("Iniciando validação de contrato")

    current_contract, current_rf = read_manifest_from_pr()
    previous_contract, _ = read_manifest_from_base_branch()

    validate_contract_files(current_contract)
    load_checklist(CONTRACTS[current_contract]["checklist"])

    transitions = load_transitions()
    validate_transition(previous_contract, current_contract, transitions)

    validate_branch_against_rf(current_contract, current_rf)
    validate_diff_against_contract(current_contract)

    ok("Contrato, checklist, transição, branch e diff estão coerentes")
    ok("Validação de contrato concluída com sucesso")


if __name__ == "__main__":
    main()
