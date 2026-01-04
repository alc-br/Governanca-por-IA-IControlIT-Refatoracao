#!/usr/bin/env python3
r"""
validator-uc-wf-md.py - Validador de Conformidade UC/WF/MD com Templates

Valida que documentos gerados (UC-RFXXX.md, UC-RFXXX.yaml, WF-RFXXX.md, MD-RFXXX.yaml)
estao conformes aos templates oficiais em D:\IC2\docs\templates\.

Validacoes:
1. UC-RFXXX.md conforme UC.md
2. UC-RFXXX.yaml conforme UC.yaml
3. WF-RFXXX.md conforme WF.md
4. MD-RFXXX.yaml conforme MD.yaml

Uso:
    python validator-uc-wf-md.py RFXXX
    python validator-uc-wf-md.py --fase N
    python validator-uc-wf-md.py --all

Exit Codes:
    0  - PASS (100% conforme)
    10 - UC.md nao conforme ao template
    11 - UC.yaml nao conforme ao template
    20 - WF.md nao conforme ao template
    30 - MD.yaml nao conforme ao template
    40 - Arquivo(s) obrigatorio(s) ausente(s)

Autor: Agencia ALC - alc.dev.br
Versao: 1.0
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
    """Resultado da validacao de conformidade com templates"""
    rf_id: str
    uc_md_conforme: bool
    uc_yaml_conforme: bool
    wf_md_conforme: bool
    md_yaml_conforme: bool
    arquivos_ausentes: List[str]
    gaps: List[Dict[str, str]]

    def to_dict(self):
        return asdict(self)

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)

    def is_compliant(self) -> bool:
        """Verifica se esta 100% conforme"""
        return (
            self.uc_md_conforme and
            self.uc_yaml_conforme and
            self.wf_md_conforme and
            self.md_yaml_conforme and
            len(self.arquivos_ausentes) == 0 and
            len([g for g in self.gaps if g.get('tipo') == 'CRITICO']) == 0
        )


class ValidadorUCWFMD:
    """Validador de Conformidade UC/WF/MD com Templates"""

    # Secoes obrigatorias no UC.md
    UC_MD_SECOES_OBRIGATORIAS = [
        "1. OBJETIVO DO DOCUMENTO",
        "2. SUMÁRIO DE CASOS DE USO",
        "3. PADRÕES GERAIS APLICÁVEIS A TODOS OS UCs",
        "UC00",
        "UC01",
        "UC02",
        "UC03",
        "UC04",
        "4. MATRIZ DE RASTREABILIDADE",
    ]

    # Campos obrigatorios no UC.yaml
    UC_YAML_CAMPOS_OBRIGATORIOS = [
        "uc.rf",
        "uc.versao",
        "uc.data",
        "casos_de_uso",
    ]

    # Secoes obrigatorias no WF.md
    WF_MD_SECOES_OBRIGATORIAS = [
        "1. OBJETIVO DO DOCUMENTO",
        "2. PRINCÍPIOS DE DESIGN (OBRIGATÓRIOS)",
        "3. MAPA DE TELAS (COBERTURA TOTAL DO RF)",
        "4. WF-01",
        "5. WF-02",
        "6. WF-03",
        "7. WF-04",
        "8. WF-05",
        "9. NOTIFICAÇÕES",
        "10. RESPONSIVIDADE (OBRIGATÓRIO)",
        "11. ACESSIBILIDADE (OBRIGATÓRIO)",
        "12. RASTREABILIDADE",
        "13. NÃO-OBJETIVOS (OUT OF SCOPE)",
        "14. HISTÓRICO DE ALTERAÇÕES",
    ]

    # Campos obrigatorios no MD.yaml
    MD_YAML_CAMPOS_OBRIGATORIOS = [
        "metadata.versao",
        "metadata.data",
        "metadata.autor",
        "metadata.rf_relacionado.id",
        "metadata.rf_relacionado.nome",
        "entidades",
        "observacoes",
        "historico",
    ]

    # UCs obrigatorios (minimo)
    UCS_OBRIGATORIOS = ["UC00", "UC01", "UC02", "UC03", "UC04"]

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

        raise FileNotFoundError(f"RF {rf_id} nao encontrado em {self.base_path}")

    def validar_secoes_md(
        self,
        arquivo_md: Path,
        secoes_obrigatorias: List[str],
        tipo: str
    ) -> Tuple[bool, List[Dict[str, str]]]:
        """Valida que um arquivo .md contem todas as secoes obrigatorias"""
        if not arquivo_md.exists():
            return False, [{
                "tipo": "CRITICO",
                "mensagem": f"Arquivo {arquivo_md.name} nao encontrado"
            }]

        gaps = []
        content = arquivo_md.read_text(encoding='utf-8')

        # Extrair titulos de secoes (linhas comecando com ##)
        secoes_encontradas = set()
        for line in content.split('\n'):
            line_stripped = line.strip()
            if line_stripped.startswith('## '):
                # Remover "## " e pegar titulo
                titulo = line_stripped[3:].strip()
                secoes_encontradas.add(titulo)

        # Verificar secoes obrigatorias
        for secao in secoes_obrigatorias:
            # Para UCs, aceitar variacoes (UC00 — Nome)
            if secao.startswith('UC'):
                # Verificar se existe alguma secao que comece com o UC
                found = any(s.startswith(secao) for s in secoes_encontradas)
                if not found:
                    gaps.append({
                        "tipo": "CRITICO",
                        "arquivo": arquivo_md.name,
                        "mensagem": f"Secao obrigatoria ausente: '{secao}'"
                    })
            else:
                if secao not in secoes_encontradas:
                    gaps.append({
                        "tipo": "CRITICO",
                        "arquivo": arquivo_md.name,
                        "mensagem": f"Secao obrigatoria ausente: '{secao}'"
                    })

        # Verificar cabecalho (metadados)
        header_patterns = {
            "Versao": r'\*\*Versao\*\*:',
            "Data": r'\*\*Data\*\*:',
            "Autor": r'\*\*Autor\*\*:',
        }

        if tipo == "UC":
            header_patterns["RF"] = r'\*\*RF\*\*:'
        elif tipo == "WF":
            header_patterns["RF Relacionado"] = r'\*\*RF Relacionado\*\*:'

        for campo, pattern in header_patterns.items():
            if not re.search(pattern, content):
                gaps.append({
                    "tipo": "IMPORTANTE",
                    "arquivo": arquivo_md.name,
                    "mensagem": f"Campo de cabecalho ausente ou incorreto: '{campo}'"
                })

        return len([g for g in gaps if g['tipo'] == 'CRITICO']) == 0, gaps

    def validar_campos_yaml(
        self,
        arquivo_yaml: Path,
        campos_obrigatorios: List[str]
    ) -> Tuple[bool, Dict, List[Dict[str, str]]]:
        """Valida que um arquivo .yaml contem todos os campos obrigatorios"""
        if not arquivo_yaml.exists():
            return False, {}, [{
                "tipo": "CRITICO",
                "mensagem": f"Arquivo {arquivo_yaml.name} nao encontrado"
            }]

        gaps = []

        try:
            with open(arquivo_yaml, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            return False, {}, [{
                "tipo": "CRITICO",
                "arquivo": arquivo_yaml.name,
                "mensagem": f"YAML invalido: {str(e)}"
            }]
        except Exception as e:
            return False, {}, [{
                "tipo": "CRITICO",
                "arquivo": arquivo_yaml.name,
                "mensagem": f"Erro ao ler arquivo: {str(e)}"
            }]

        # Verificar campos obrigatorios (suporta nested paths com ".")
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
                    "tipo": "CRITICO",
                    "arquivo": arquivo_yaml.name,
                    "mensagem": f"Campo obrigatorio ausente: '{campo_path}'"
                })

        return len([g for g in gaps if g['tipo'] == 'CRITICO']) == 0, data, gaps

    def validar_uc_md(self, rf_path: Path) -> Tuple[bool, List[Dict[str, str]]]:
        """Valida UC-RFXXX.md conforme template UC.md"""
        rf_id = rf_path.name.split('-')[0]
        uc_md = rf_path / f"UC-{rf_id}.md"

        return self.validar_secoes_md(
            uc_md,
            self.UC_MD_SECOES_OBRIGATORIAS,
            tipo="UC"
        )

    def validar_uc_yaml(self, rf_path: Path) -> Tuple[bool, Dict, List[Dict[str, str]]]:
        """Valida UC-RFXXX.yaml conforme template UC.yaml"""
        rf_id = rf_path.name.split('-')[0]
        uc_yaml = rf_path / f"UC-{rf_id}.yaml"

        conforme, data, gaps = self.validar_campos_yaml(
            uc_yaml,
            self.UC_YAML_CAMPOS_OBRIGATORIOS
        )

        # Validacao adicional: verificar casos_de_uso contem UCs obrigatorios
        if conforme and data and 'casos_de_uso' in data:
            casos_de_uso = data['casos_de_uso']
            if isinstance(casos_de_uso, list):
                ucs_encontrados = set()
                for uc in casos_de_uso:
                    if isinstance(uc, dict) and 'id' in uc:
                        ucs_encontrados.add(uc['id'])

                ucs_faltando = set(self.UCS_OBRIGATORIOS) - ucs_encontrados
                if ucs_faltando:
                    gaps.append({
                        "tipo": "CRITICO",
                        "arquivo": uc_yaml.name,
                        "mensagem": f"UCs obrigatorios ausentes: {', '.join(sorted(ucs_faltando))}"
                    })
                    conforme = False

        return conforme, data, gaps

    def validar_wf_md(self, rf_path: Path) -> Tuple[bool, List[Dict[str, str]]]:
        """Valida WF-RFXXX.md conforme template WF.md"""
        rf_id = rf_path.name.split('-')[0]
        wf_md = rf_path / f"WF-{rf_id}.md"

        return self.validar_secoes_md(
            wf_md,
            self.WF_MD_SECOES_OBRIGATORIAS,
            tipo="WF"
        )

    def validar_md_yaml(self, rf_path: Path) -> Tuple[bool, Dict, List[Dict[str, str]]]:
        """Valida MD-RFXXX.yaml conforme template MD.yaml"""
        rf_id = rf_path.name.split('-')[0]

        # MD pode ter multiplos arquivos (MD-XXX-*.yaml)
        # Vamos buscar o primeiro MD-*.yaml
        md_files = list(rf_path.glob(f"MD-*.yaml"))

        if not md_files:
            return False, {}, [{
                "tipo": "CRITICO",
                "mensagem": f"Nenhum arquivo MD-*.yaml encontrado"
            }]

        # Validar o primeiro arquivo encontrado
        md_yaml = md_files[0]

        conforme, data, gaps = self.validar_campos_yaml(
            md_yaml,
            self.MD_YAML_CAMPOS_OBRIGATORIOS
        )

        # Validacao adicional: verificar entidades tem campos obrigatorios
        if conforme and data and 'entidades' in data:
            entidades = data['entidades']
            if isinstance(entidades, list):
                for i, entidade in enumerate(entidades, 1):
                    if not isinstance(entidade, dict):
                        continue

                    nome_entidade = entidade.get('nome', f'Entidade #{i}')

                    # Verificar campos obrigatorios da entidade
                    if 'campos' not in entidade:
                        gaps.append({
                            "tipo": "CRITICO",
                            "arquivo": md_yaml.name,
                            "mensagem": f"Entidade '{nome_entidade}' sem campo 'campos'"
                        })
                        conforme = False

        return conforme, data, gaps

    def validar_rf(self, rf_id: str) -> ValidationResult:
        """Valida conformidade completa de UC/WF/MD com templates"""
        try:
            rf_path = self.encontrar_rf(rf_id)
        except FileNotFoundError as e:
            return ValidationResult(
                rf_id=rf_id,
                uc_md_conforme=False,
                uc_yaml_conforme=False,
                wf_md_conforme=False,
                md_yaml_conforme=False,
                arquivos_ausentes=[],
                gaps=[{"tipo": "CRITICO", "mensagem": str(e)}]
            )

        all_gaps = []
        arquivos_ausentes = []

        # Verificar arquivos obrigatorios
        uc_md_path = rf_path / f"UC-{rf_id}.md"
        uc_yaml_path = rf_path / f"UC-{rf_id}.yaml"
        wf_md_path = rf_path / f"WF-{rf_id}.md"
        md_yaml_files = list(rf_path.glob("MD-*.yaml"))

        if not uc_md_path.exists():
            arquivos_ausentes.append(f"UC-{rf_id}.md")
        if not uc_yaml_path.exists():
            arquivos_ausentes.append(f"UC-{rf_id}.yaml")
        if not wf_md_path.exists():
            arquivos_ausentes.append(f"WF-{rf_id}.md")
        if not md_yaml_files:
            arquivos_ausentes.append(f"MD-*.yaml")

        # Validacao 1: UC.md
        uc_md_conforme, gaps_uc_md = self.validar_uc_md(rf_path)
        all_gaps.extend(gaps_uc_md)

        # Validacao 2: UC.yaml
        uc_yaml_conforme, uc_data, gaps_uc_yaml = self.validar_uc_yaml(rf_path)
        all_gaps.extend(gaps_uc_yaml)

        # Validacao 3: WF.md
        wf_md_conforme, gaps_wf_md = self.validar_wf_md(rf_path)
        all_gaps.extend(gaps_wf_md)

        # Validacao 4: MD.yaml
        md_yaml_conforme, md_data, gaps_md_yaml = self.validar_md_yaml(rf_path)
        all_gaps.extend(gaps_md_yaml)

        return ValidationResult(
            rf_id=rf_id,
            uc_md_conforme=uc_md_conforme,
            uc_yaml_conforme=uc_yaml_conforme,
            wf_md_conforme=wf_md_conforme,
            md_yaml_conforme=md_yaml_conforme,
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
    """Gera relatorio em Markdown"""
    total = len(results)
    conformes = sum(1 for r in results if r.is_compliant())
    taxa_conformidade = (conformes / total * 100) if total > 0 else 0

    lines = [
        "# Relatorio de Conformidade UC/WF/MD com Templates",
        "",
        f"**Data:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"**Total de RFs:** {total}",
        f"**Conformes:** {conformes} ({taxa_conformidade:.1f}%)",
        "",
        "---",
        "",
        "## Resumo por RF",
        "",
        "| RF | UC.md | UC.yaml | WF.md | MD.yaml | Arquivos Ausentes | Status |",
        "|-----|-------|---------|-------|---------|-------------------|--------|"
    ]

    for result in results:
        status = "[OK] CONFORME" if result.is_compliant() else "[GAPS]"
        uc_md_icon = "[OK]" if result.uc_md_conforme else "[X]"
        uc_yaml_icon = "[OK]" if result.uc_yaml_conforme else "[X]"
        wf_md_icon = "[OK]" if result.wf_md_conforme else "[X]"
        md_yaml_icon = "[OK]" if result.md_yaml_conforme else "[X]"
        ausentes = ", ".join(result.arquivos_ausentes) if result.arquivos_ausentes else "-"

        lines.append(
            f"| {result.rf_id} | {uc_md_icon} | {uc_yaml_icon} | {wf_md_icon} | "
            f"{md_yaml_icon} | {ausentes} | {status} |"
        )

    lines.extend(["", "---", "", "## Gaps Identificados", ""])

    for result in results:
        if result.gaps:
            lines.append(f"### {result.rf_id}")
            lines.append("")

            # Agrupar por tipo
            criticos = [g for g in result.gaps if g.get('tipo') == 'CRITICO']
            importantes = [g for g in result.gaps if g.get('tipo') == 'IMPORTANTE']
            menores = [g for g in result.gaps if g.get('tipo') == 'MENOR']

            if criticos:
                lines.append("**[CRITICO]:**")
                for gap in criticos:
                    lines.append(f"- {gap.get('mensagem')}")
                    if 'arquivo' in gap:
                        lines.append(f"  - Arquivo: {gap['arquivo']}")
                lines.append("")

            if importantes:
                lines.append("**[IMPORTANTE]:**")
                for gap in importantes:
                    lines.append(f"- {gap.get('mensagem')}")
                    if 'arquivo' in gap:
                        lines.append(f"  - Arquivo: {gap['arquivo']}")
                lines.append("")

            if menores:
                lines.append("**[MENOR]:**")
                for gap in menores:
                    lines.append(f"- {gap.get('mensagem')}")
                    if 'arquivo' in gap:
                        lines.append(f"  - Arquivo: {gap['arquivo']}")
                lines.append("")

    content = "\n".join(lines)

    if output_path:
        Path(output_path).write_text(content, encoding='utf-8')
        print(f"\n[OK] Relatorio salvo em: {output_path}")

    return content


def main():
    if len(sys.argv) < 2:
        print("Uso:")
        print("  python validator-uc-wf-md.py RFXXX")
        print("  python validator-uc-wf-md.py --fase N")
        print("  python validator-uc-wf-md.py --all")
        sys.exit(1)

    validador = ValidadorUCWFMD()
    results = []

    arg = sys.argv[1]

    if arg == '--all':
        print("Validando TODOS os RFs do projeto...")
        results = validador.validar_todos()
        output_file = "D:\\IC2\\relatorios\\validacao-conformidade-uc-wf-md-completa.md"

    elif arg == '--fase':
        if len(sys.argv) < 3:
            print("[ERRO] Especifique o numero da fase: --fase N")
            sys.exit(1)

        fase_num = int(sys.argv[2])
        print(f"Validando RFs da Fase {fase_num}...")
        results = validador.validar_fase(fase_num)
        output_file = f"D:\\IC2\\relatorios\\validacao-conformidade-uc-wf-md-fase{fase_num}.md"

    else:
        # Validar RF unico
        rf_id = arg
        print(f"Validando {rf_id}...")
        result = validador.validar_rf(rf_id)
        results = [result]
        output_file = None

        # Exibir resultado no console
        print("\n" + "="*60)
        print(f"RESULTADO: {rf_id}")
        print("="*60)
        print(f"UC.md Conforme: {'[OK]' if result.uc_md_conforme else '[X]'}")
        print(f"UC.yaml Conforme: {'[OK]' if result.uc_yaml_conforme else '[X]'}")
        print(f"WF.md Conforme: {'[OK]' if result.wf_md_conforme else '[X]'}")
        print(f"MD.yaml Conforme: {'[OK]' if result.md_yaml_conforme else '[X]'}")

        if result.arquivos_ausentes:
            print(f"\n[X] Arquivos Ausentes: {', '.join(result.arquivos_ausentes)}")

        if result.gaps:
            print(f"\nGaps Encontrados: {len(result.gaps)}")
            for gap in result.gaps:
                tipo = gap.get('tipo', 'INFO')
                msg = gap.get('mensagem', '')
                icon = {"CRITICO": "[X]", "IMPORTANTE": "[!]", "MENOR": "[i]"}.get(tipo, "[-]")
                print(f"  {icon} [{tipo}] {msg}")
                if 'arquivo' in gap:
                    print(f"      Arquivo: {gap['arquivo']}")
        else:
            print("\n[OK] Nenhum gap encontrado!")

        print("\n" + "="*60)
        print("STATUS FINAL:")
        print("="*60)
        if result.is_compliant():
            print("[OK] CONFORME - UC/WF/MD estao 100% aderentes aos templates")
            exit_code = 0
        else:
            print("[X] NAO CONFORME - UC/WF/MD possuem gaps em relacao aos templates")
            # Determinar exit code especifico
            if result.arquivos_ausentes:
                exit_code = 40
            elif not result.uc_md_conforme:
                exit_code = 10
            elif not result.uc_yaml_conforme:
                exit_code = 11
            elif not result.wf_md_conforme:
                exit_code = 20
            elif not result.md_yaml_conforme:
                exit_code = 30
            else:
                exit_code = 1

        # JSON output
        print("\n" + "="*60)
        print("JSON:")
        print("="*60)
        print(result.to_json())

        sys.exit(exit_code)

    # Gerar relatorio se multiplos RFs
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
