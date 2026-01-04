#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Atualizacao de Status dos RFs no Azure DevOps
Conforme CONTRATO DE DEVOPS - GOVERNANCA

NOTA: Este script foi integrado ao sync-all-rfs.py
Este arquivo agora serve apenas como wrapper para manter compatibilidade.

Para uso completo, execute:
    python tools/devops-sync/sync-all-rfs.py
"""

import subprocess
import sys
import os

def main():
    print("="*60)
    print("UPDATE-RF-STATUS")
    print("="*60)
    print()
    print("[INFO] Este script foi integrado ao sync-all-rfs.py")
    print("[INFO] Redirecionando...")
    print()

    # Executar sync-all-rfs.py
    script_dir = os.path.dirname(os.path.abspath(__file__))
    main_script = os.path.join(script_dir, "sync-all-rfs.py")

    if os.path.exists(main_script):
        result = subprocess.run([sys.executable, main_script], cwd=os.getcwd())
        sys.exit(result.returncode)
    else:
        print(f"[ERRO] Script nao encontrado: {main_script}")
        sys.exit(1)

if __name__ == "__main__":
    main()
