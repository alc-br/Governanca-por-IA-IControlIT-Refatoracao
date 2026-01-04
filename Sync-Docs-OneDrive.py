#!/usr/bin/env python3
r"""
Sincroniza documentos Markdown selecionados para o OneDrive convertendo-os para DOCX.

Regras:
  - Origem:  D:\IC2\docs\Fases
  - Destino: C:\Users\Administrator\OneDrive - K2A PARTNERS CONSULTORIA LTDA\IControlIT 2.0\Fases
  - Apenas arquivos de RF, UC (Casos de Uso) e MD são convertidos.
  - Diretórios contendo "Testes" são ignorados.
  - A árvore de pastas é mantida; apenas arquivos DOCX são gravados no destino.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path
from typing import Iterable, Set


SOURCE_ROOT = Path(r"D:\IC2\docs\Fases")
DEST_ROOT = Path(
    r"C:\Users\Administrator\K2A PARTNERS CONSULTORIA LTDA\Base K2A - IControlIT 2.0\Fases"
)

# Padrões permitidos
RF_PATTERN = re.compile(r"^RF-[A-Z0-9-]+\.md$", re.IGNORECASE)
MD_PATTERN = re.compile(r"^MD-[A-Z0-9-]+\.md$", re.IGNORECASE)
UC_PATTERN = re.compile(r"^UC\d{2}-[A-Z0-9-]+\.md$", re.IGNORECASE)

SKIP_DIR_NAME = "Testes"

# Formatos de entrada tentados (em ordem)
PANDOC_INPUT_FORMATS = [
    "markdown",
    "gfm",
    "markdown-yaml_metadata_block",
]


class SyncError(Exception):
    """Erro durante a sincronização/conversão."""


def log(message: str) -> None:
    print(message, flush=True)


def is_allowed_markdown(path: Path) -> bool:
    """Verifica se o arquivo atende aos padrões de RF, MD ou UC."""
    name = path.name
    return any(
        pattern.match(name)
        for pattern in (RF_PATTERN, MD_PATTERN, UC_PATTERN)
    )


def contains_skip_dir(path: Path) -> bool:
    """Retorna True se o caminho contém diretórios a serem ignorados."""
    return any(part.lower() == SKIP_DIR_NAME.lower() for part in path.parts)


def iter_markdown_files(root: Path) -> Iterable[Path]:
    """Itera sobre arquivos Markdown elegíveis na raiz fornecida."""
    for md_path in root.rglob("*.md"):
        if contains_skip_dir(md_path):
            continue
        if is_allowed_markdown(md_path):
            yield md_path


def ensure_pandoc_available() -> None:
    """Garante que o Pandoc esteja disponível no PATH."""
    try:
        result = subprocess.run(
            ["pandoc", "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
        if not result.stdout:
            raise SyncError("Pandoc encontrado, mas não retornou versão.")
    except FileNotFoundError as exc:
        raise SyncError(
            "Pandoc não encontrado. Instale-o ou adicione ao PATH."
        ) from exc
    except subprocess.CalledProcessError as exc:
        raise SyncError(
            f"Falha ao executar pandoc --version: {exc.stderr}"
        ) from exc


def convert_markdown_to_docx(source_md: Path, dest_docx: Path) -> None:
    """Converte um arquivo Markdown em DOCX utilizando o Pandoc."""
    dest_docx.parent.mkdir(parents=True, exist_ok=True)
    errors: list[str] = []
    for input_format in PANDOC_INPUT_FORMATS:
        cmd = [
            "pandoc",
            str(source_md),
            f"--from={input_format}",
            "--to=docx",
            "--output",
            str(dest_docx),
        ]
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if result.returncode == 0:
            return
        errors.append(f"[{input_format}] {result.stderr.strip()}")

    if dest_docx.exists():
        dest_docx.unlink(missing_ok=True)
    raise SyncError(
        f"Erro convertendo {source_md} -> {dest_docx}:\n" + "\n".join(errors)
    )


def cleanup_destination(dest_root: Path, expected_files: Set[Path]) -> None:
    """Remove arquivos no destino que não constem como esperados."""
    for item in dest_root.rglob("*"):
        if item.is_dir():
            continue
        if item.suffix.lower() != ".docx":
            log(f"Removendo arquivo não suportado: {item}")
            item.unlink(missing_ok=True)
            continue
        resolved_item = item.resolve()
        if resolved_item not in expected_files:
            log(f"Removendo DOCX desatualizado: {item}")
            item.unlink(missing_ok=True)


def sync() -> None:
    if not SOURCE_ROOT.exists():
        raise SyncError(f"Diretório de origem não encontrado: {SOURCE_ROOT}")
    DEST_ROOT.mkdir(parents=True, exist_ok=True)

    ensure_pandoc_available()

    expected_docx: Set[Path] = set()
    markdown_files = list(iter_markdown_files(SOURCE_ROOT))
    if not markdown_files:
        log("Nenhum arquivo elegível encontrado. Nada a sincronizar.")
        return

    log(f"{len(markdown_files)} arquivos Markdown elegíveis encontrados.")

    for md_file in markdown_files:
        relative = md_file.relative_to(SOURCE_ROOT)
        dest_docx = (DEST_ROOT / relative).with_suffix(".docx")
        log(f"Convertendo {md_file} -> {dest_docx}")
        convert_markdown_to_docx(md_file, dest_docx)
        expected_docx.add(dest_docx.resolve())

    cleanup_destination(DEST_ROOT, expected_docx)
    log("Sincronização concluída com sucesso.")


def main() -> int:
    try:
        sync()
    except SyncError as exc:
        log(f"ERRO: {exc}")
        return 1
    except Exception as exc:  # noqa: BLE001
        log(f"ERRO inesperado: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
