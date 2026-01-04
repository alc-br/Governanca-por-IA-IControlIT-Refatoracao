#!/usr/bin/env python3
"""
Script para adicionar campo flExcluido aos models TypeScript do frontend
Conforme ADR-004: Soft Delete com FlExcluido

Data: 2025-12-25
"""

import os
import re
from pathlib import Path

# Diretório base dos models
MODELS_DIR = Path("d:/IC2/frontend/icontrolit-app/src/app/core/models")

# Lista das 39 entidades que precisam ter flExcluido adicionado
# (baseado no log de adicionar-flexcluido-entidades.py)
ENTIDADES = [
    "andar",
    "aprovacao-delegacao",
    "contrato",
    "contrato-aditivo",
    "contrato-fatura",
    "contrato-fatura-item",
    "contrato-indice",
    "contrato-sla-operacao",
    "contrato-sla-servico",
    "contrato-status",
    "edificio",
    "email-template",
    "empresa",
    "endereco",
    "endereco-entrega",
    "endereco-entrega-tipo",
    "integracao-configuracao",
    "integracao-endpoint",
    "notificacao-dispositivo",
    "notificacao-template",
    "permission",
    "plano-contas",
    "rack",
    "rateio-item",
    "report-template",
    "role",
    "sala",
    "sistema-log-configuracao-alerta",
    "sistema-log-configuracao-retention",
    "sistema-log-metrica-customizada",
    "sistema-parametro",
    "sistema-parametro-categoria",
    "solicitacao",
    "solicitacao-fila",
    "solicitacao-fila-atendimento",
    "solicitacao-tipo",
    "usuario",
    "volumetria",
    "workflow-aprovacao-template"
]

# Contadores
arquivos_processados = 0
arquivos_alterados = 0
arquivos_nao_encontrados = 0
arquivos_ja_tinham = 0

# Log de alterações
log_lines = []

def adicionar_flexcluido_model(filepath):
    """Adiciona campo flExcluido ao model TypeScript"""
    global arquivos_processados, arquivos_alterados, arquivos_ja_tinham

    arquivos_processados += 1

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            conteudo = f.read()

        # Verificar se já tem flExcluido
        if re.search(r'flExcluido\s*:\s*boolean', conteudo, re.IGNORECASE):
            log_msg = f"[SKIP] {filepath.name}: ja tem flExcluido"
            log_lines.append(log_msg)
            print(log_msg)
            arquivos_ja_tinham += 1
            return

        # Procurar o padrão de interface principal (primeira interface export)
        # Exemplo: export interface Empresa {
        match_interface = re.search(
            r'(export\s+interface\s+\w+\s*\{[^}]*?)(\n\})',
            conteudo,
            re.DOTALL
        )

        if not match_interface:
            log_msg = f"[WARN] {filepath.name}: nao encontrou interface principal"
            log_lines.append(log_msg)
            print(log_msg)
            return

        # Preparar linhas para inserir
        # Procurar se há campo 'ativo:' para adicionar logo após
        interface_body = match_interface.group(1)

        # Verificar se tem campo 'ativo'
        if re.search(r'\bativo\s*:\s*boolean', interface_body):
            # Adicionar após o campo 'ativo'
            novo_conteudo = re.sub(
                r'(\bativo\s*:\s*boolean\s*;)',
                r'\1\n    /**\n     * Soft delete: false=ativo (nao deletado), true=excluido (deletado)\n     */\n    flExcluido: boolean;',
                conteudo,
                count=1
            )
        else:
            # Adicionar antes do fechamento da interface
            novo_conteudo = re.sub(
                r'(export\s+interface\s+\w+\s*\{[^}]*?)(\n\})',
                r'\1\n    /**\n     * Soft delete: false=ativo (nao deletado), true=excluido (deletado)\n     */\n    flExcluido: boolean;\2',
                conteudo,
                count=1
            )

        # Verificar se houve alteração
        if novo_conteudo == conteudo:
            log_msg = f"[WARN] {filepath.name}: nao conseguiu adicionar FlExcluido"
            log_lines.append(log_msg)
            print(log_msg)
            return

        # Salvar arquivo
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(novo_conteudo)

        arquivos_alterados += 1
        log_msg = f"[OK] {filepath.name}: FlExcluido adicionado"
        log_lines.append(log_msg)
        print(log_msg)

    except Exception as e:
        log_msg = f"[ERROR] {filepath.name}: {e}"
        log_lines.append(log_msg)
        print(log_msg)

def main():
    global arquivos_nao_encontrados

    print("=" * 80)
    print("ADICIONAR FlExcluido NOS MODELS TYPESCRIPT")
    print("ADR-004: Soft Delete com FlExcluido")
    print("=" * 80)
    print()

    # Processar cada entidade
    for entidade in ENTIDADES:
        # Nome do arquivo: entidade.model.ts
        model_file = MODELS_DIR / f"{entidade}.model.ts"

        if not model_file.exists():
            log_msg = f"[WARN] {entidade}.model.ts: arquivo nao encontrado"
            log_lines.append(log_msg)
            print(log_msg)
            arquivos_nao_encontrados += 1
            continue

        adicionar_flexcluido_model(model_file)

    print()
    print("=" * 80)
    print("RESUMO")
    print("=" * 80)
    print(f"Arquivos na lista: {len(ENTIDADES)}")
    print(f"Arquivos processados: {arquivos_processados}")
    print(f"Arquivos alterados: {arquivos_alterados}")
    print(f"Arquivos que ja tinham FlExcluido: {arquivos_ja_tinham}")
    print(f"Arquivos nao encontrados: {arquivos_nao_encontrados}")
    print()

    # Salvar log
    log_file = Path("d:/IC2/relatorios/2025-12-25-Adicionar-FlExcluido-Frontend-Log.txt")
    log_file.parent.mkdir(parents=True, exist_ok=True)

    with open(log_file, 'w', encoding='utf-8') as f:
        f.write("LOG - ADICIONAR FlExcluido NOS MODELS TYPESCRIPT\n")
        f.write(f"Data: 2025-12-25\n")
        f.write(f"ADR-004: Soft Delete com FlExcluido\n")
        f.write("=" * 80 + "\n\n")
        f.write("\n".join(log_lines))
        f.write("\n\n" + "=" * 80 + "\n")
        f.write(f"RESUMO:\n")
        f.write(f"- Arquivos na lista: {len(ENTIDADES)}\n")
        f.write(f"- Arquivos processados: {arquivos_processados}\n")
        f.write(f"- Arquivos alterados: {arquivos_alterados}\n")
        f.write(f"- Arquivos que ja tinham FlExcluido: {arquivos_ja_tinham}\n")
        f.write(f"- Arquivos nao encontrados: {arquivos_nao_encontrados}\n")

    print(f"Log salvo em: {log_file}")

if __name__ == "__main__":
    main()
