#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Verificar configuracao das variaveis de ambiente"""
import os

print("=== VERIFICACAO DE AMBIENTE ===")
print()

org = os.getenv("AZDO_ORG_URL", "NAO CONFIGURADO")
proj = os.getenv("AZDO_PROJECT", "NAO CONFIGURADO")
pat = os.getenv("AZDO_PAT", "")

print(f"AZDO_ORG_URL: {org}")
print(f"AZDO_PROJECT: {proj}")
print(f"AZDO_PAT: {'*** (configurado)' if pat else 'NAO CONFIGURADO'}")

if not pat:
    print()
    print("INSTRUCOES:")
    print("1. Abra um terminal PowerShell")
    print("2. Execute os comandos:")
    print()
    print('   $env:AZDO_ORG_URL = "https://dev.azure.com/IControlIT-v2"')
    print('   $env:AZDO_PROJECT = "iControlIT 2.0"')
    print('   $env:AZDO_PAT = "<seu_pat_aqui>"')
    print()
    print("3. Entao execute:")
    print("   python D:\\IC2\\tools\\devops-sync\\sync-all-rfs.py")
