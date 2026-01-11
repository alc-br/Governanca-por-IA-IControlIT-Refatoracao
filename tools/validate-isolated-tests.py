#!/usr/bin/env python3
"""
validate-isolated-tests.py

Valida que specs de testes E2E seguem o padrão ISOLATED corretamente.

VALIDAÇÕES:
- Detecta test.describe.serial (PROIBIDO em isolated)
- Valida presença de beforeEach (OBRIGATÓRIO)
- Valida presença de afterEach (OBRIGATÓRIO)
- Valida chamada a closeAllOverlays() (OBRIGATÓRIO)
- Valida Page Object imports (OBRIGATÓRIO)

USO:
    python validate-isolated-tests.py RF006
    python validate-isolated-tests.py RF006 --verbose

REFERÊNCIA:
    CONTRATO-TESTES-E2E-ISOLADOS.md - FASE 6 (Validação)

AUTOR: Agência ALC - alc.dev.br
DATA: 2026-01-11
"""

import sys
import os
import glob
import re
from typing import List, Dict, Tuple

# Cores para output (Windows/Linux compatible)
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_error(msg: str):
    print(f"{Colors.RED}[ERROR] {msg}{Colors.END}")

def print_success(msg: str):
    print(f"{Colors.GREEN}[OK] {msg}{Colors.END}")

def print_warning(msg: str):
    print(f"{Colors.YELLOW}[WARNING] {msg}{Colors.END}")

def print_info(msg: str):
    print(f"{Colors.BLUE}[INFO] {msg}{Colors.END}")

def validar_spec_isolated(spec_file: str, verbose: bool = False) -> Tuple[bool, List[str]]:
    """
    Valida que um spec file segue o padrão ISOLATED.

    Args:
        spec_file: Caminho do arquivo spec.ts
        verbose: Se True, exibe detalhes adicionais

    Returns:
        (is_valid, falhas): Tupla com flag de validação e lista de falhas
    """
    if verbose:
        print_info(f"Validando: {os.path.basename(spec_file)}")

    falhas = []

    try:
        with open(spec_file, 'r', encoding='utf-8') as f:
            conteudo = f.read()

        # VALIDAÇÃO 1: Detectar test.describe.serial (PROIBIDO)
        # Remove comentários para evitar falsos positivos
        conteudo_sem_comentarios = re.sub(r'//.*$', '', conteudo, flags=re.MULTILINE)
        conteudo_sem_comentarios = re.sub(r'/\*.*?\*/', '', conteudo_sem_comentarios, flags=re.DOTALL)

        if 'test.describe.serial' in conteudo_sem_comentarios:
            falhas.append(
                f"PROIBIDO: Usa test.describe.serial (padrão stateful). "
                f"Use test.describe sem .serial para testes isolated."
            )

        # VALIDAÇÃO 2: Validar presença de beforeEach (OBRIGATÓRIO)
        if 'test.beforeEach' not in conteudo:
            falhas.append(
                f"AUSENTE: test.beforeEach é OBRIGATÓRIO em testes isolated. "
                f"beforeEach deve fazer login + navigate + closeAllOverlays."
            )

        # VALIDAÇÃO 3: Validar presença de afterEach (OBRIGATÓRIO)
        if 'test.afterEach' not in conteudo:
            falhas.append(
                f"AUSENTE: test.afterEach é OBRIGATÓRIO em testes isolated. "
                f"afterEach deve fazer closeAllOverlays + logout."
            )

        # VALIDAÇÃO 4: Validar chamada a closeAllOverlays() (OBRIGATÓRIO)
        if 'closeAllOverlays()' not in conteudo:
            falhas.append(
                f"AUSENTE: closeAllOverlays() é OBRIGATÓRIO (previne 67% das falhas RF006). "
                f"Deve ser chamado em beforeEach e afterEach."
            )
        else:
            # Contar quantas vezes closeAllOverlays é chamado
            count = conteudo.count('closeAllOverlays()')
            if count < 2:
                print_warning(
                    f"closeAllOverlays() chamado apenas {count}x. "
                    f"Recomendado: 2x (beforeEach + afterEach)."
                )

        # VALIDAÇÃO 5: Validar imports de Page Objects (OBRIGATÓRIO)
        if "import {" not in conteudo or "from '../pages/" not in conteudo:
            falhas.append(
                f"AUSENTE: Imports de Page Objects não encontrados. "
                f"Testes isolated devem usar Page Object Pattern."
            )

        # VALIDAÇÃO 6: Validar import de LoginPage (OBRIGATÓRIO)
        if "LoginPage" not in conteudo:
            falhas.append(
                f"AUSENTE: LoginPage não importado. "
                f"beforeEach deve fazer login via LoginPage."
            )

        # VALIDAÇÃO 7: Validar import de APIHelper (RECOMENDADO)
        if "APIHelper" not in conteudo:
            print_warning(
                f"RECOMENDADO: Importar APIHelper para criação rápida de dados via API."
            )

        # VALIDAÇÃO 8: Detectar variáveis compartilhadas entre testes (ALERTA)
        # Variáveis fora de test.describe podem causar state contamination
        linhas = conteudo.split('\n')
        in_describe = False
        for i, linha in enumerate(linhas, 1):
            if 'test.describe' in linha:
                in_describe = True
            if not in_describe and re.match(r'^let\s+\w+\s*:', linha.strip()):
                # Variável let declarada FORA de test.describe
                var_name = re.search(r'let\s+(\w+)', linha).group(1)
                # Exceções permitidas: Page Objects (recriados em beforeEach)
                if var_name not in ['loginPage', 'clientesPage', 'apiHelper', 'page']:
                    print_warning(
                        f"Linha {i}: Variável '{var_name}' declarada fora de test.describe. "
                        f"Pode causar state contamination se compartilhada entre testes."
                    )

        # VALIDAÇÃO 9: Validar comentário de tipo de teste (RECOMENDADO)
        if 'TIPO: ISOLATED' not in conteudo and 'TIPO: Isolated' not in conteudo:
            print_warning(
                f"RECOMENDADO: Adicionar comentário '* TIPO: ISOLATED' no cabeçalho do spec."
            )

        is_valid = len(falhas) == 0

        if verbose:
            if is_valid:
                print_success(f"Spec validado com sucesso: {os.path.basename(spec_file)}")
            else:
                print_error(f"Spec com {len(falhas)} falha(s): {os.path.basename(spec_file)}")

        return is_valid, falhas

    except Exception as e:
        falhas.append(f"ERRO: Falha ao ler arquivo: {str(e)}")
        return False, falhas

def validar_rf(rf_numero: str, verbose: bool = False) -> int:
    """
    Valida todos os specs de um RF.

    Args:
        rf_numero: Número do RF (ex: '006')
        verbose: Se True, exibe detalhes adicionais

    Returns:
        0 se todos os specs são válidos, 1 se algum spec é inválido
    """
    print(f"\n{Colors.BOLD}=== Validação de Testes Isolated - RF{rf_numero} ==={Colors.END}\n")

    # Procurar specs do RF
    spec_pattern = f"D:\\IC2\\frontend\\icontrolit-app\\e2e\\specs\\TC-RF{rf_numero}*.spec.ts"
    spec_files = glob.glob(spec_pattern)

    if not spec_files:
        print_error(f"Nenhum spec encontrado para RF{rf_numero} em: {spec_pattern}")
        return 1

    print_info(f"Encontrados {len(spec_files)} spec(s) para RF{rf_numero}:\n")

    total_specs = len(spec_files)
    specs_validos = 0
    specs_invalidos = 0
    todas_falhas = {}

    for spec_file in spec_files:
        is_valid, falhas = validar_spec_isolated(spec_file, verbose)

        if is_valid:
            specs_validos += 1
            print_success(f"[PASS] {os.path.basename(spec_file)}")
        else:
            specs_invalidos += 1
            print_error(f"[FAIL] {os.path.basename(spec_file)}")
            todas_falhas[spec_file] = falhas

    # Relatório final
    print(f"\n{Colors.BOLD}=== Relatório de Validação ==={Colors.END}\n")
    print(f"Total de specs analisados: {total_specs}")
    print_success(f"Specs válidos: {specs_validos}")

    if specs_invalidos > 0:
        print_error(f"Specs inválidos: {specs_invalidos}\n")

        print(f"{Colors.BOLD}Detalhamento de Falhas:{Colors.END}\n")
        for spec_file, falhas in todas_falhas.items():
            print(f"{Colors.RED}Arquivo: {os.path.basename(spec_file)}{Colors.END}")
            for i, falha in enumerate(falhas, 1):
                print(f"  {i}. {falha}")
            print()

        print_error("VALIDAÇÃO FALHOU: Corrija as falhas acima antes de prosseguir.\n")
        return 1
    else:
        print_success("\nVALIDAÇÃO PASSOU: Todos os specs seguem o padrão ISOLATED corretamente.\n")
        return 0

def main():
    if len(sys.argv) < 2:
        print("Uso: python validate-isolated-tests.py <RF_NUMERO> [--verbose]")
        print("Exemplo: python validate-isolated-tests.py 006")
        print("Exemplo: python validate-isolated-tests.py 006 --verbose")
        sys.exit(1)

    rf_numero = sys.argv[1].replace('RF', '').replace('rf', '')
    verbose = '--verbose' in sys.argv or '-v' in sys.argv

    exit_code = validar_rf(rf_numero, verbose)
    sys.exit(exit_code)

if __name__ == '__main__':
    main()
