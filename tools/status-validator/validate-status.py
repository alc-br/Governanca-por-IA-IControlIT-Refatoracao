#!/usr/bin/env python
"""
Validador de STATUS.yaml

Valida:
- Schema correto (campos obrigatorios)
- Titulo nao truncado
- contrato_ativo coerente com status de desenvolvimento
"""

import os
import sys
import re

RF_PATH = "docs/rf"

# Campos obrigatorios no STATUS.yaml
REQUIRED_FIELDS = [
    "rf",
    "fase",
    "epic",
    "titulo",
    "documentacao",
    "test_cases",
    "desenvolvimento",
    "testes",
    "devops",
    "governanca",
]

VALID_DEV_STATUS = ["not_started", "in_progress", "done"]
VALID_TEST_STATUS = ["not_run", "pass", "fail"]


def fail(msg):
    print(f"\n[FAIL] {msg}\n")
    sys.exit(1)


def warn(msg):
    print(f"[WARN] {msg}")


def ok(msg):
    print(f"[OK] {msg}")


def info(msg):
    print(f"[INFO] {msg}")


def extract_field(content, field):
    """Extrai valor de um campo YAML simples."""
    match = re.search(rf"^{field}:\s*(.+)$", content, re.MULTILINE)
    return match.group(1).strip() if match else None


def extract_nested_status(content, parent, child):
    """Extrai status de um campo aninhado."""
    pattern = rf"{parent}:\s*\n\s+{child}:\s*\n\s+status:\s*(\w+)"
    match = re.search(pattern, content)
    return match.group(1) if match else None


def validate_file(filepath):
    """Valida um arquivo STATUS.yaml."""
    errors = []

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        return [f"Erro ao ler arquivo: {e}"]

    # 1. Verificar campos obrigatorios
    for field in REQUIRED_FIELDS:
        if not re.search(rf"^{field}:", content, re.MULTILINE):
            errors.append(f"Campo obrigatorio ausente: {field}")

    # 2. Verificar titulo truncado
    titulo = extract_field(content, "titulo")
    if titulo:
        if titulo.startswith("estao"):
            errors.append(f"Titulo truncado: '{titulo}' (deveria comecar com 'Gestao')")
        if len(titulo) < 5:
            errors.append(f"Titulo muito curto: '{titulo}'")

    # 3. Verificar status de desenvolvimento
    backend_status = extract_nested_status(content, "desenvolvimento", "backend")
    frontend_status = extract_nested_status(content, "desenvolvimento", "frontend")

    if backend_status and backend_status not in VALID_DEV_STATUS:
        errors.append(f"Status backend invalido: {backend_status}")

    if frontend_status and frontend_status not in VALID_DEV_STATUS:
        errors.append(f"Status frontend invalido: {frontend_status}")

    # 4. Verificar coerencia do contrato_ativo
    contrato_match = re.search(r"contrato_ativo:\s*(.+)", content)
    contrato_ativo = contrato_match.group(1).strip() if contrato_match else None

    if contrato_ativo == "null" or contrato_ativo == "~":
        contrato_ativo = None

    expected_contract = None
    if backend_status == "not_started" and frontend_status == "not_started":
        expected_contract = None
    elif backend_status == "done" and frontend_status == "not_started":
        expected_contract = "CONTRATO-EXECUCAO-FRONTEND"
    elif backend_status == "done" and frontend_status == "done":
        expected_contract = "CONTRATO-EXECUCAO-TESTES"
    elif backend_status == "in_progress":
        expected_contract = "CONTRATO-EXECUCAO-BACKEND"
    elif frontend_status == "in_progress":
        expected_contract = "CONTRATO-EXECUCAO-FRONTEND"

    if expected_contract is not None and contrato_ativo != expected_contract:
        errors.append(
            f"contrato_ativo inconsistente: {contrato_ativo} (esperado: {expected_contract})"
        )

    # 5. Verificar RF valido
    documentacao = extract_field(content, "rf")
    if documentacao and not re.match(r"RF\d{3}$", rf):
        errors.append(f"RF invalido: {rf} (esperado: RFXXX)")

    return errors


def main():
    print("=" * 60)
    print("VALIDADOR DE STATUS.yaml")
    print("=" * 60)

    if not os.path.exists(RF_PATH):
        fail(f"Diretorio nao encontrado: {RF_PATH}")

    total_files = 0
    total_errors = 0
    files_with_errors = []

    for root, dirs, files in os.walk(RF_PATH):
        if "STATUS.yaml" in files:
            filepath = os.path.join(root, "STATUS.yaml")
            total_files += 1

            errors = validate_file(filepath)

            if errors:
                total_errors += len(errors)
                documentacao_match = re.search(r"(RF\d+)", filepath)
                documentacao_name = documentacao_match.group(1) if documentacao_match else filepath
                files_with_errors.append((rf_name, errors))

    print(f"\nArquivos analisados: {total_files}")
    print(f"Arquivos com erros: {len(files_with_errors)}")
    print(f"Total de erros: {total_errors}")

    if files_with_errors:
        print("\n" + "-" * 60)
        print("ERROS ENCONTRADOS:")
        print("-" * 60)

        for documentacao_name, errors in files_with_errors:
            print(f"\n{rf_name}:")
            for error in errors:
                print(f"  - {error}")

        print("\n")
        sys.exit(1)
    else:
        ok("Todos os STATUS.yaml estao validos")
        sys.exit(0)


if __name__ == "__main__":
    main()
