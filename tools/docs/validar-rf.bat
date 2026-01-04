@echo off
REM Script para validar RF específico com filtro opcional de tipo de documento
REM Uso: validar-rf.bat RFXXX [TIPO]
REM Saída: D:\IC2\relatorios\rfXXX\[tipo\]auditoria.json

if "%~1"=="" (
    echo.
    echo ╔════════════════════════════════════════════════════════════╗
    echo ║  VALIDADOR DE RF INDIVIDUAL                                ║
    echo ╚════════════════════════════════════════════════════════════╝
    echo.
    echo Uso: validar-rf.bat RFXXX [TIPO]
    echo.
    echo Parâmetros:
    echo   RFXXX - ID do RF (ex: RF001, RF028)
    echo   TIPO  - Opcional: RF, RL, UC, WF, MD, TC, MT, STATUS
    echo.
    echo Exemplos:
    echo   validar-rf.bat RF001           (todos os documentos)
    echo   validar-rf.bat RF001 UC        (apenas UC)
    echo   validar-rf.bat RF001 WF        (apenas WF)
    echo   validar-rf.bat RF028 MD        (apenas MD)
    echo.
    echo Saída:
    echo   Sem filtro:  relatorios\rfXXX\auditoria.json
    echo   Com filtro:  relatorios\rfXXX\TIPO\auditoria.json
    echo.
    exit /b 1
)

cd /d D:\IC2

if "%~2"=="" (
    REM Sem filtro - validar todos os documentos do RF
    echo Validando todos os documentos do %1...
    .venv\Scripts\python.exe docs\tools\docs\validator-docs.py --rf %1

    echo.
    echo ═══════════════════════════════════════════════════════════════
    echo Para ver o relatório completo:
    echo   type relatorios\%1\auditoria.json
    echo   code relatorios\%1\auditoria.json
    echo ═══════════════════════════════════════════════════════════════
    echo.
) else (
    REM Com filtro - validar apenas tipo especificado
    echo Validando %1 - documento %2...
    .venv\Scripts\python.exe docs\tools\docs\validator-docs.py --rf %1 --doc %2

    set RF_LOWER=%1
    set DOC_LOWER=%2

    echo.
    echo ═══════════════════════════════════════════════════════════════
    echo Para ver o relatório de %2:
    echo   type relatorios\%RF_LOWER%\%DOC_LOWER%\auditoria.json
    echo   code relatorios\%RF_LOWER%\%DOC_LOWER%\auditoria.json
    echo ═══════════════════════════════════════════════════════════════
    echo.
)
