@echo off
REM Script para configurar ambiente virtual e instalar dependências
REM Executar este script uma vez antes de usar o validador

echo ========================================
echo Configurando ambiente virtual...
echo ========================================

cd /d D:\IC2

REM Criar venv se não existir
if not exist .venv (
    echo Criando ambiente virtual...
    python -m venv .venv
) else (
    echo Ambiente virtual ja existe.
)

REM Atualizar pip
echo Atualizando pip...
.venv\Scripts\python.exe -m pip install --upgrade pip --quiet

REM Instalar dependências
echo Instalando dependencias...
.venv\Scripts\python.exe -m pip install -r docs\tools\docs\requirements.txt

echo.
echo ========================================
echo Configuracao concluida!
echo ========================================
echo.
echo Para usar o validador:
echo   docs\tools\docs\run-validator.bat --all
echo   docs\tools\docs\run-validator.bat RF001
echo   docs\tools\docs\run-validator.bat --fase 2
echo.
pause
