@echo off
REM Script para executar o validador no ambiente virtual
REM Uso: run-validator.bat [argumentos]
REM Exemplo: run-validator.bat --all
REM Exemplo: run-validator.bat RF001

cd /d D:\IC2
.venv\Scripts\python.exe docs\tools\docs\validator-docs.py %*
