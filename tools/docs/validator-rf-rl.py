#!/usr/bin/env python3
r"""
validator-rf-rl.py - Validador de Conformidade RF/RL com Templates

Valida que documentos gerados (RFXXX.md, RFXXX.yaml, RL-RFXXX.md, RL-RFXXX.yaml)
estao conformes aos templates oficiais em D:\IC2\docs\templates\.

Validações:
1. RFXXX.md conforme RF.md
2. RFXXX.yaml conforme RF.yaml
3. RL-RFXXX.md conforme RL.md (se aplicável)
4. RL-RFXXX.yaml conforme RL.yaml (se aplicável)

Uso:
    python validator-rf-rl.py RFXXX
    python validator-rf-rl.py --fase 1
    python validator-rf-rl.py --all

Exit Codes:
    0  - PASS (100% conforme)
    10 - RF.md não conforme ao template
    11 - RF.yaml não conforme ao template
    20 - RL.md não conforme ao template
    21 - RL.yaml não conforme ao template
    30 - Arquivo(s) obrigatório(s) ausente(s)

Autor: Agência ALC - alc.dev.br
Versão: 1.0
Data: 2025-12-31
"""

import sys
import os
import re
import yaml
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class ValidationResult:
    """Resultado da validação de conformidade com templates"""
    rf_id: str
    rf_md_conforme: bool
    rf_yaml_conforme: bool
    rl_md_conforme: Optional[bool]
    rl_yaml_conforme: Optional[bool]
    arquivos_ausentes: List[str]
    gaps: List[Dict[str, str]]

    def to_dict(self):
        return asdict(self)

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)

    def is_compliant(self) -> bool:
        """Verifica se está 100% conforme"""
        return (
            self.rf_md_conforme and
            self.rf_yaml_conforme and
            len(self.arquivos_ausentes) == 0 and
            len([g for g in self.gaps if g.get('tipo') == 'CRÍTICO']) == 0
        )


class ValidadorRFRL:
    """Validador de Conformidade RF/RL com Templates"""

    # Seções obrigatórias no RF.md
    RF_MD_SECOES_OBRIGATORIAS = [
        "1. OBJETIVO DO REQUISITO",
        "2. ESCOPO",
        "3. CONCEITOS E DEFINIÇÕES",
        "4. FUNCIONALIDADES COBERTAS",
        "5. REGRAS DE NEGÓCIO",
        "6. ESTADOS DA ENTIDADE",
        "7. EVENTOS DE DOMÍNIO",
        "8. CRITÉRIOS GLOBAIS DE ACEITE",
        "9. SEGURANÇA",
        "10. ARTEFATOS DERIVADOS",
        "11. RASTREABILIDADE",
    ]

    # Campos obrigatórios no RF.yaml
    RF_YAML_CAMPOS_OBRIGATORIOS = [
        "rf.id",
        "rf.nome",
        "rf.versao",
        "rf.data",
        "rf.fase",
        "rf.epic",
        "rf.status",
        "descricao.objetivo",
        "escopo.incluso",
        "entidades",
        "regras_negocio",
        "permissoes",
    ]

    # Seções obrigatórias no RL.md
    RL_MD_SECOES_OBRIGATORIAS = [
        "1. CONTEXTO DO LEGADO",
        "2. TELAS DO LEGADO",
        "3. WEBSERVICES / MÉTODOS LEGADOS",
        "4. TABELAS LEGADAS",
        "5. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO",
        "6. GAP ANALYSIS (LEGADO x RF MODERNO)",
        "7. DECISÕES DE MODERNIZAÇÃO",
        "8. RISCOS DE MIGRAÇÃO",
        "9. RASTREABILIDADE",
    ]

    # Campos obrigatórios no RL.yaml
    RL_YAML_CAMPOS_OBRIGATORIOS = [
        "rf_id",
        "titulo",
        "legado.sistema",
        "referencias",
    ]

    def __init__(
        self,
        base_path: str = "D:\\IC2\\docs\\rf",
        templates_path: str = "D:\\IC2\\docs\\templates"
    ):
        self.base_path = Path(base_path)
        self.templates_path = Path(templates_path)

    def encontrar_rf(self, rf_id: str) -> Path:
        """Encontra a pasta do RF"""
        for fase_dir in self.base_path.glob("Fase-*"):
            for epic_dir in fase_dir.glob("EPIC*"):
                for rf_dir in epic_dir.glob(f"{rf_id}*"):
                    if rf_dir.is_dir() and rf_dir.name.startswith(rf_id):
                        return rf_dir

        raise FileNotFoundError(f"RF {rf_id} não encontrado em {self.base_path}")

    def validar_secoes_md(
        self,
        arquivo_md: Path,
        secoes_obrigatorias: List[str],
        tipo: str
    ) -> Tuple[bool, List[Dict[str, str]]]:
        """Valida que um arquivo .md contém todas as seções obrigatórias"""
        if not arquivo_md.exists():
            return False, [{
                "tipo": "CRÍTICO",
                "mensagem": f"Arquivo {arquivo_md.name} não encontrado"
            }]

        gaps = []
        content = arquivo_md.read_text(encoding='utf-8')

        # Extrair títulos de seções (linhas começando com ##)
        secoes_encontradas = set()
        for line in content.split('\n'):
            if line.strip().startswith('## '):
                # Remover "## " e pegar título
                titulo = line.strip()[3:].strip()
                secoes_encontradas.add(titulo)

        # Verificar seções obrigatórias
        for secao in secoes_obrigatorias:
            if secao not in secoes_encontradas:
                gaps.append({
                    "tipo": "CRÍTICO",
                    "arquivo": arquivo_md.name,
                    "mensagem": f"Seção obrigatória ausente: '{secao}'"
                })

        # Verificar cabeçalho (metadados)
        header_patterns = {
            "Versão": r'\*\*Versão\*\*:',
            "Data": r'\*\*Data\*\*:',
            "Autor": r'\*\*Autor\*\*:',
        }

        if tipo == "RF":
            header_patterns.update({
                "EPIC": r'\*\*EPIC\*\*:',
                "Fase": r'\*\*Fase\*\*:',
            })

        for campo, pattern in header_patterns.items():
            if not re.search(pattern, content):
                gaps.append({
                    "tipo": "IMPORTANTE",
                    "arquivo": arquivo_md.name,
                    "mensagem": f"Campo de cabeçalho ausente ou incorreto: '{campo}'"
                })

        return len([g for g in gaps if g['tipo'] == 'CRÍTICO']) == 0, gaps

    def validar_campos_yaml(
        self,
        arquivo_yaml: Path,
        campos_obrigatorios: List[str]
    ) -> Tuple[bool, Dict, List[Dict[str, str]]]:
        """Valida que um arquivo .yaml contém todos os campos obrigatórios"""
        if not arquivo_yaml.exists():
            return False, {}, [{
                "tipo": "CRÍTICO",
                "mensagem": f"Arquivo {arquivo_yaml.name} não encontrado"
            }]

        gaps = []

        try:
            with open(arquivo_yaml, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            return False, {}, [{
                "tipo": "CRÍTICO",
                "arquivo": arquivo_yaml.name,
                "mensagem": f"YAML inválido: {str(e)}"
            }]
        except Exception as e:
            return False, {}, [{
                "tipo": "CRÍTICO",
                "arquivo": arquivo_yaml.name,
                "mensagem": f"Erro ao ler arquivo: {str(e)}"
            }]

        # Verificar campos obrigatórios (suporta nested paths com ".")
        for campo_path in campos_obrigatorios:
            partes = campo_path.split('.')
            valor = data
            campo_existe = True

            for parte in partes:
                if isinstance(valor, dict) and parte in valor:
                    valor = valor[parte]
                else:
                    campo_existe = False
                    break

            if not campo_existe:
                gaps.append({
                    "tipo": "CRÍTICO",
                    "arquivo": arquivo_yaml.name,
                    "mensagem": f"Campo obrigatório ausente: '{campo_path}'"
                })

        return len([g for g in gaps if g['tipo'] == 'CRÍTICO']) == 0, data, gaps

    def validar_rf_md(self, rf_path: Path) -> Tuple[bool, List[Dict[str, str]]]:
        """Valida RFXXX.md conforme template RF.md"""
        rf_id = rf_path.name.split('-')[0]
        rf_md = rf_path / f"{rf_id}.md"

        return self.validar_secoes_md(
            rf_md,
            self.RF_MD_SECOES_OBRIGATORIAS,
            tipo="RF"
        )

    def validar_rf_yaml(self, rf_path: Path) -> Tuple[bool, Dict, List[Dict[str, str]]]:
        """Valida RFXXX.yaml conforme template RF.yaml"""
        rf_id = rf_path.name.split('-')[0]
        rf_yaml = rf_path / f"{rf_id}.yaml"

        return self.validar_campos_yaml(rf_yaml, self.RF_YAML_CAMPOS_OBRIGATORIOS)

    def validar_rl_md(self, rf_path: Path) -> Tuple[Optional[bool], List[Dict[str, str]]]:
        """Valida RL-RFXXX.md conforme template RL.md (se existir)"""
        rf_id = rf_path.name.split('-')[0]
        rl_md = rf_path / f"RL-{rf_id}.md"

        # RL.md é opcional
        if not rl_md.exists():
            return None, []

        conforme, gaps = self.validar_secoes_md(
            rl_md,
            self.RL_MD_SECOES_OBRIGATORIAS,
            tipo="RL"
        )

        return conforme, gaps

    def validar_rl_yaml(self, rf_path: Path) -> Tuple[Optional[bool], Optional[Dict], List[Dict[str, str]]]:
        """Valida RL-RFXXX.yaml conforme template RL.yaml (se existir)"""
        rf_id = rf_path.name.split('-')[0]
        rl_yaml = rf_path / f"RL-{rf_id}.yaml"

        # RL.yaml é opcional
        if not rl_yaml.exists():
            return None, None, []

        conforme, data, gaps = self.validar_campos_yaml(
            rl_yaml,
            self.RL_YAML_CAMPOS_OBRIGATORIOS
        )

        # Validação adicional: cada item em 'referencias' deve ter campo 'destino'
        if conforme and data and 'referencias' in data:
            for i, item in enumerate(data['referencias'], 1):
                item_id = item.get('id', f'Item #{i}')
                if 'destino' not in item:
                    gaps.append({
                        "tipo": "CRÍTICO",
                        "item": item_id,
                        "mensagem": "Campo 'destino' obrigatório ausente em item de referência"
                    })
                    conforme = False

        return conforme, data, gaps

    def validar_rf(self, rf_id: str) -> ValidationResult:
        """Valida conformidade completa de um RF com templates"""
        try:
            rf_path = self.encontrar_rf(rf_id)
        except FileNotFoundError as e:
            return ValidationResult(
                rf_id=rf_id,
                rf_md_conforme=False,
                rf_yaml_conforme=False,
                rl_md_conforme=None,
                rl_yaml_conforme=None,
                arquivos_ausentes=[],
                gaps=[{"tipo": "CRÍTICO", "mensagem": str(e)}]
            )

        all_gaps = []
        arquivos_ausentes = []

        # Verificar arquivos obrigatórios
        rf_md_path = rf_path / f"{rf_id}.md"
        rf_yaml_path = rf_path / f"{rf_id}.yaml"

        if not rf_md_path.exists():
            arquivos_ausentes.append(f"{rf_id}.md")
        if not rf_yaml_path.exists():
            arquivos_ausentes.append(f"{rf_id}.yaml")

        # Validação 1: RF.md
        rf_md_conforme, gaps_rf_md = self.validar_rf_md(rf_path)
        all_gaps.extend(gaps_rf_md)

        # Validação 2: RF.yaml
        rf_yaml_conforme, rf_data, gaps_rf_yaml = self.validar_rf_yaml(rf_path)
        all_gaps.extend(gaps_rf_yaml)

        # Validação 3: RL.md (opcional)
        rl_md_conforme, gaps_rl_md = self.validar_rl_md(rf_path)
        all_gaps.extend(gaps_rl_md)

        # Validação 4: RL.yaml (opcional)
        rl_yaml_conforme, rl_data, gaps_rl_yaml = self.validar_rl_yaml(rf_path)
        all_gaps.extend(gaps_rl_yaml)

        return ValidationResult(
            rf_id=rf_id,
            rf_md_conforme=rf_md_conforme,
            rf_yaml_conforme=rf_yaml_conforme,
            rl_md_conforme=rl_md_conforme,
            rl_yaml_conforme=rl_yaml_conforme,
            arquivos_ausentes=arquivos_ausentes,
            gaps=all_gaps
        )

    def validar_fase(self, fase_num: int) -> List[ValidationResult]:
        """Valida todos os RFs de uma fase"""
        results = []
        fase_dir = self.base_path / f"Fase-{fase_num}"

        if not fase_dir.exists():
            print(f"[ERRO] Fase {fase_num} nao encontrada em {self.base_path}")
            return results

        for epic_dir in sorted(fase_dir.glob("EPIC-*")):
            for rf_dir in sorted(epic_dir.glob("RF*")):
                rf_id = rf_dir.name.split('-')[0]
                print(f"Validando {rf_id}...")
                result = self.validar_rf(rf_id)
                results.append(result)

        return results

    def validar_todos(self) -> List[ValidationResult]:
        """Valida todos os RFs do projeto"""
        results = []

        for fase_dir in sorted(self.base_path.glob("Fase-*")):
            fase_match = re.match(r'Fase-(\d+)', fase_dir.name)
            if fase_match:
                fase_num = int(fase_match.group(1))
                print(f"\n{'='*60}")
                print(f"FASE {fase_num}: {fase_dir.name}")
                print('='*60)
                fase_results = self.validar_fase(fase_num)
                results.extend(fase_results)

        return results


def gerar_relatorio_markdown(results: List[ValidationResult], output_path: str = None) -> str:
    """Gera relatório em Markdown"""
    total = len(results)
    conformes = sum(1 for r in results if r.is_compliant())
    taxa_conformidade = (conformes / total * 100) if total > 0 else 0

    lines = [
        "# Relatório de Conformidade RF/RL com Templates",
        "",
        f"**Data:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"**Total de RFs:** {total}",
        f"**Conformes:** {conformes} ({taxa_conformidade:.1f}%)",
        "",
        "---",
        "",
        "## Resumo por RF",
        "",
        "| RF | RF.md | RF.yaml | RL.md | RL.yaml | Arquivos Ausentes | Status |",
        "|-----|-------|---------|-------|---------|-------------------|--------|"
    ]

    for result in results:
        status = "[OK] CONFORME" if result.is_compliant() else "[GAPS]"
        rf_md_icon = "[OK]" if result.rf_md_conforme else "[X]"
        rf_yaml_icon = "[OK]" if result.rf_yaml_conforme else "[X]"
        rl_md_icon = "[OK]" if result.rl_md_conforme else ("[X]" if result.rl_md_conforme is False else "N/A")
        rl_yaml_icon = "[OK]" if result.rl_yaml_conforme else ("[X]" if result.rl_yaml_conforme is False else "N/A")
        ausentes = ", ".join(result.arquivos_ausentes) if result.arquivos_ausentes else "-"

        lines.append(
            f"| {result.rf_id} | {rf_md_icon} | {rf_yaml_icon} | {rl_md_icon} | "
            f"{rl_yaml_icon} | {ausentes} | {status} |"
        )

    lines.extend(["", "---", "", "## Gaps Identificados", ""])

    for result in results:
        if result.gaps:
            lines.append(f"### {result.rf_id}")
            lines.append("")

            # Agrupar por tipo
            criticos = [g for g in result.gaps if g.get('tipo') == 'CRÍTICO']
            importantes = [g for g in result.gaps if g.get('tipo') == 'IMPORTANTE']
            menores = [g for g in result.gaps if g.get('tipo') == 'MENOR']

            if criticos:
                lines.append("**[CRITICO]:**")
                for gap in criticos:
                    lines.append(f"- {gap.get('mensagem')}")
                    if 'item' in gap:
                        lines.append(f"  - Item: {gap['item']}")
                    if 'arquivo' in gap:
                        lines.append(f"  - Arquivo: {gap['arquivo']}")
                lines.append("")

            if importantes:
                lines.append("**[IMPORTANTE]:**")
                for gap in importantes:
                    lines.append(f"- {gap.get('mensagem')}")
                    if 'item' in gap:
                        lines.append(f"  - Item: {gap['item']}")
                    if 'arquivo' in gap:
                        lines.append(f"  - Arquivo: {gap['arquivo']}")
                lines.append("")

            if menores:
                lines.append("**[MENOR]:**")
                for gap in menores:
                    lines.append(f"- {gap.get('mensagem')}")
                    if 'item' in gap:
                        lines.append(f"  - Item: {gap['item']}")
                lines.append("")

    content = "\n".join(lines)

    if output_path:
        Path(output_path).write_text(content, encoding='utf-8')
        print(f"\n[OK] Relatorio salvo em: {output_path}")

    return content


def main():
    if len(sys.argv) < 2:
        print("Uso:")
        print("  python validator-rf-rl.py RFXXX")
        print("  python validator-rf-rl.py --fase N")
        print("  python validator-rf-rl.py --all")
        sys.exit(1)

    validador = ValidadorRFRL()
    results = []

    arg = sys.argv[1]

    if arg == '--all':
        print("Validando TODOS os RFs do projeto...")
        results = validador.validar_todos()
        output_file = "D:\\IC2\\relatorios\\validacao-conformidade-rf-rl-completa.md"

    elif arg == '--fase':
        if len(sys.argv) < 3:
            print("[ERRO] Especifique o numero da fase: --fase N")
            sys.exit(1)

        fase_num = int(sys.argv[2])
        print(f"Validando RFs da Fase {fase_num}...")
        results = validador.validar_fase(fase_num)
        output_file = f"D:\\IC2\\relatorios\\validacao-conformidade-rf-rl-fase{fase_num}.md"

    else:
        # Validar RF único
        rf_id = arg
        print(f"Validando {rf_id}...")
        result = validador.validar_rf(rf_id)
        results = [result]
        output_file = None

        # Exibir resultado no console
        print("\n" + "="*60)
        print(f"RESULTADO: {rf_id}")
        print("="*60)
        print(f"RF.md Conforme: {'[OK]' if result.rf_md_conforme else '[X]'}")
        print(f"RF.yaml Conforme: {'[OK]' if result.rf_yaml_conforme else '[X]'}")
        print(f"RL.md Conforme: {'[OK]' if result.rl_md_conforme else ('[X]' if result.rl_md_conforme is False else 'N/A')}")
        print(f"RL.yaml Conforme: {'[OK]' if result.rl_yaml_conforme else ('[X]' if result.rl_yaml_conforme is False else 'N/A')}")

        if result.arquivos_ausentes:
            print(f"\n[X] Arquivos Ausentes: {', '.join(result.arquivos_ausentes)}")

        if result.gaps:
            print(f"\nGaps Encontrados: {len(result.gaps)}")
            for gap in result.gaps:
                tipo = gap.get('tipo', 'INFO')
                msg = gap.get('mensagem', '')
                icon = {"CRITICO": "[X]", "IMPORTANTE": "[!]", "MENOR": "[i]"}.get(tipo, "[-]")
                print(f"  {icon} [{tipo}] {msg}")
                if 'item' in gap:
                    print(f"      Item: {gap['item']}")
                if 'arquivo' in gap:
                    print(f"      Arquivo: {gap['arquivo']}")
        else:
            print("\n[OK] Nenhum gap encontrado!")

        print("\n" + "="*60)
        print("STATUS FINAL:")
        print("="*60)
        if result.is_compliant():
            print("[OK] CONFORME - RF esta 100% aderente aos templates")
            exit_code = 0
        else:
            print("[X] NAO CONFORME - RF possui gaps em relacao aos templates")
            # Determinar exit code específico
            if result.arquivos_ausentes:
                exit_code = 30
            elif not result.rf_md_conforme:
                exit_code = 10
            elif not result.rf_yaml_conforme:
                exit_code = 11
            elif result.rl_md_conforme is False:
                exit_code = 20
            elif result.rl_yaml_conforme is False:
                exit_code = 21
            else:
                exit_code = 1

        # JSON output
        print("\n" + "="*60)
        print("JSON:")
        print("="*60)
        print(result.to_json())

        sys.exit(exit_code)

    # Gerar relatório se múltiplos RFs
    if len(results) > 1:
        gerar_relatorio_markdown(results, output_file)

        # Resumo no console
        total = len(results)
        conformes = sum(1 for r in results if r.is_compliant())
        print(f"\n{'='*60}")
        print(f"RESUMO: {conformes}/{total} RFs conformes ({conformes/total*100:.1f}%)")
        print('='*60)

        # Exit code baseado em conformidade geral
        if conformes == total:
            sys.exit(0)
        else:
            sys.exit(1)


if __name__ == '__main__':
    main()
