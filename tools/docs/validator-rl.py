#!/usr/bin/env python3
"""
validator-rl.py - Validador de Separação RF/RL

Valida que:
1. RFXXX.md não contém conteúdo legado misturado
2. RL-RFXXX.yaml existe e está bem formado
3. Cada item em RL tem campo 'destino' preenchido
4. Itens com destino=descartado têm justificativa
5. Itens com destino=assumido têm rf_item_relacionado

Uso:
    python validator-rl.py RFXXX
    python validator-rl.py --fase 1
    python validator-rl.py --all

Autor: Agência ALC - alc.dev.br
Versão: 1.0
Data: 2025-12-29
"""

import sys
import os
import re
import yaml
import json
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass, asdict


@dataclass
class ValidationResult:
    """Resultado da validação de um RF"""
    rf_id: str
    separacao_valida: bool
    rl_estruturado: bool
    itens_legado: int
    itens_com_destino: int
    gaps: List[Dict[str, str]]

    def to_dict(self):
        return asdict(self)

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)


class ValidadorRL:
    """Validador de Separação RF/RL"""

    # Palavras-chave de legado proibidas em RF.md
    KEYWORDS_LEGADO = [
        'VB.NET', 'VB .NET', 'Visual Basic',
        'ASP.NET Web Forms', 'Web Forms', 'WebForms',
        '.aspx', 'ASPX',
        'GridView', 'DataGrid',
        'ViewState', 'Session',
        'Server.Transfer', 'Response.Redirect',
        'ic1_legado', 'IControlIT legado',
        'código legado', 'sistema legado',
        'migrar do legado', 'baseado no legado',
    ]

    # Destinos válidos para itens RL
    DESTINOS_VALIDOS = ['assumido', 'substituido', 'descartado', 'a_revisar']

    def __init__(self, base_path: str = "D:\\IC2\\docs\\rf"):
        self.base_path = Path(base_path)

    def encontrar_rf(self, rf_id: str) -> Path:
        """Encontra a pasta do RF (tolerante a diferentes padrões de estrutura)"""
        # Tentar múltiplos padrões de EPIC
        epic_patterns = ["EPIC*", "EPIC-*", "EPIC[0-9]*"]

        for fase_dir in self.base_path.glob("Fase-*"):
            for epic_pattern in epic_patterns:
                for epic_dir in fase_dir.glob(epic_pattern):
                    # Procurar RF com diferentes padrões
                    rf_patterns = [f"{rf_id}-*", f"{rf_id}"]
                    for rf_pattern in rf_patterns:
                        for rf_dir in epic_dir.glob(rf_pattern):
                            # Verificar se é realmente a pasta do RF
                            if rf_dir.is_dir() and rf_dir.name.startswith(rf_id):
                                return rf_dir

        raise FileNotFoundError(f"RF {rf_id} não encontrado em {self.base_path}")

    def validar_rf_limpo(self, rf_path: Path) -> Tuple[bool, List[Dict[str, str]]]:
        """Valida que RF.md não contém palavras-chave de legado"""
        rf_md = rf_path / f"{rf_path.name.split('-')[0]}.md"

        if not rf_md.exists():
            return False, [{"tipo": "CRÍTICO", "mensagem": f"Arquivo {rf_md.name} não encontrado"}]

        gaps = []
        content = rf_md.read_text(encoding='utf-8')

        # Verificar cada palavra-chave
        for keyword in self.KEYWORDS_LEGADO:
            # Busca case-insensitive
            pattern = re.compile(re.escape(keyword), re.IGNORECASE)
            matches = pattern.findall(content)

            if matches:
                # Encontrar linha(s) onde aparece
                lines = content.split('\n')
                line_numbers = []
                for i, line in enumerate(lines, 1):
                    if pattern.search(line):
                        line_numbers.append(i)

                gaps.append({
                    "tipo": "CRÍTICO",
                    "arquivo": rf_md.name,
                    "mensagem": f"Palavra-chave legado encontrada: '{keyword}'",
                    "linhas": line_numbers,
                    "ocorrencias": len(matches)
                })

        return len(gaps) == 0, gaps

    def validar_rl_yaml(self, rf_path: Path) -> Tuple[bool, Dict, List[Dict[str, str]]]:
        """Valida que RL-RFXXX.yaml existe e está bem formado"""
        rf_id = rf_path.name.split('-')[0]
        rl_yaml = rf_path / f"RL-{rf_id}.yaml"

        if not rl_yaml.exists():
            return False, {}, [{
                "tipo": "CRÍTICO",
                "mensagem": f"Arquivo RL-{rf_id}.yaml não encontrado"
            }]

        gaps = []

        try:
            with open(rl_yaml, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            return False, {}, [{
                "tipo": "CRÍTICO",
                "arquivo": rl_yaml.name,
                "mensagem": f"YAML inválido: {str(e)}"
            }]
        except Exception as e:
            return False, {}, [{
                "tipo": "CRÍTICO",
                "arquivo": rl_yaml.name,
                "mensagem": f"Erro ao ler arquivo: {str(e)}"
            }]

        # Validar estrutura obrigatória
        if 'rf_id' not in data:
            gaps.append({"tipo": "CRÍTICO", "mensagem": "Campo 'rf_id' ausente"})
        elif data['rf_id'] != rf_id:
            gaps.append({
                "tipo": "IMPORTANTE",
                "mensagem": f"rf_id '{data['rf_id']}' não corresponde ao esperado '{rf_id}'"
            })

        if 'referencias' not in data:
            gaps.append({"tipo": "CRÍTICO", "mensagem": "Seção 'referencias' ausente"})
            return False, data, gaps

        if not isinstance(data['referencias'], list):
            gaps.append({"tipo": "CRÍTICO", "mensagem": "Seção 'referencias' deve ser uma lista"})
            return False, data, gaps

        return True, data, gaps

    def validar_itens_rl(self, data: Dict) -> Tuple[int, int, List[Dict[str, str]]]:
        """Valida itens da seção 'referencias' do RL"""
        gaps = []
        referencias = data.get('referencias', [])
        total_itens = len(referencias)
        itens_com_destino = 0

        for i, item in enumerate(referencias, 1):
            item_id = item.get('id', f'Item #{i}')

            # Validar campos obrigatórios
            campos_obrigatorios = ['id', 'tipo', 'nome', 'caminho', 'descricao', 'destino']
            for campo in campos_obrigatorios:
                if campo not in item:
                    gaps.append({
                        "tipo": "CRÍTICO",
                        "item": item_id,
                        "mensagem": f"Campo obrigatório '{campo}' ausente"
                    })

            # Validar destino
            if 'destino' in item:
                destino = item['destino']

                if destino not in self.DESTINOS_VALIDOS:
                    gaps.append({
                        "tipo": "CRÍTICO",
                        "item": item_id,
                        "mensagem": f"Destino inválido '{destino}'. Valores válidos: {', '.join(self.DESTINOS_VALIDOS)}"
                    })
                else:
                    itens_com_destino += 1

                    # Se destino = descartado, justificativa é obrigatória
                    if destino == 'descartado' and not item.get('justificativa'):
                        gaps.append({
                            "tipo": "IMPORTANTE",
                            "item": item_id,
                            "mensagem": "Item descartado DEVE ter justificativa"
                        })

                    # Se destino = assumido, rf_item_relacionado é recomendado
                    if destino == 'assumido' and not item.get('rf_item_relacionado'):
                        gaps.append({
                            "tipo": "MENOR",
                            "item": item_id,
                            "mensagem": "Item assumido DEVERIA ter 'rf_item_relacionado' para rastreabilidade"
                        })

            # Validar tipo
            tipos_validos = ['tela', 'webservice', 'stored_procedure', 'regra_negocio', 'componente']
            if 'tipo' in item and item['tipo'] not in tipos_validos:
                gaps.append({
                    "tipo": "IMPORTANTE",
                    "item": item_id,
                    "mensagem": f"Tipo '{item['tipo']}' não é padrão. Tipos recomendados: {', '.join(tipos_validos)}"
                })

        return total_itens, itens_com_destino, gaps

    def validar_rf(self, rf_id: str) -> ValidationResult:
        """Valida um RF completo"""
        try:
            rf_path = self.encontrar_rf(rf_id)
        except FileNotFoundError as e:
            return ValidationResult(
                rf_id=rf_id,
                separacao_valida=False,
                rl_estruturado=False,
                itens_legado=0,
                itens_com_destino=0,
                gaps=[{"tipo": "CRÍTICO", "mensagem": str(e)}]
            )

        all_gaps = []

        # Validação 1: RF.md limpo
        rf_limpo, gaps_rf = self.validar_rf_limpo(rf_path)
        all_gaps.extend(gaps_rf)

        # Validação 2: RL.yaml estruturado
        rl_valido, rl_data, gaps_rl = self.validar_rl_yaml(rf_path)
        all_gaps.extend(gaps_rl)

        # Validação 3: Itens RL completos
        total_itens = 0
        itens_com_destino = 0

        if rl_valido and rl_data:
            total_itens, itens_com_destino, gaps_itens = self.validar_itens_rl(rl_data)
            all_gaps.extend(gaps_itens)

        # Resultado final
        separacao_valida = rf_limpo and rl_valido
        rl_estruturado = rl_valido and (total_itens == itens_com_destino)

        return ValidationResult(
            rf_id=rf_id,
            separacao_valida=separacao_valida,
            rl_estruturado=rl_estruturado,
            itens_legado=total_itens,
            itens_com_destino=itens_com_destino,
            gaps=all_gaps
        )

    def validar_fase(self, fase_num: int) -> List[ValidationResult]:
        """Valida todos os RFs de uma fase"""
        results = []
        fase_dir = self.base_path / f"Fase-{fase_num}"

        if not fase_dir.exists():
            print(f" Fase {fase_num} não encontrada em {self.base_path}")
            return results

        # Iterar sobre EPICs e RFs
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


def gerar_relatorio_markdown(results: List[ValidationResult], output_path: str = None):
    """Gera relatório em Markdown"""
    from datetime import datetime

    total = len(results)
    conformes = sum(1 for r in results if r.separacao_valida and r.rl_estruturado)
    taxa_conformidade = (conformes / total * 100) if total > 0 else 0

    lines = [
        "# Relatório de Validação RF/RL",
        "",
        f"**Data:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"**Total de RFs:** {total}",
        f"**Conformes:** {conformes} ({taxa_conformidade:.1f}%)",
        "",
        "---",
        "",
        "## Resumo por RF",
        "",
        "| RF | Separação Válida | RL Estruturado | Itens Legado | Itens com Destino | Status |",
        "|-----|------------------|----------------|--------------|-------------------|--------|"
    ]

    for result in results:
        status = " CONFORME" if (result.separacao_valida and result.rl_estruturado) else " GAPS"
        sep_icon = "" if result.separacao_valida else ""
        rl_icon = "" if result.rl_estruturado else ""

        lines.append(
            f"| {result.rf_id} | {sep_icon} | {rl_icon} | "
            f"{result.itens_legado} | {result.itens_com_destino} | {status} |"
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
                lines.append("**CRÍTICO:**")
                for gap in criticos:
                    lines.append(f"- {gap.get('mensagem')}")
                    if 'item' in gap:
                        lines.append(f"  - Item: {gap['item']}")
                    if 'arquivo' in gap:
                        lines.append(f"  - Arquivo: {gap['arquivo']}")
                    if 'linhas' in gap:
                        lines.append(f"  - Linhas: {gap['linhas']}")
                lines.append("")

            if importantes:
                lines.append("**IMPORTANTE:**")
                for gap in importantes:
                    lines.append(f"- {gap.get('mensagem')}")
                    if 'item' in gap:
                        lines.append(f"  - Item: {gap['item']}")
                lines.append("")

            if menores:
                lines.append("**MENOR:**")
                for gap in menores:
                    lines.append(f"- {gap.get('mensagem')}")
                    if 'item' in gap:
                        lines.append(f"  - Item: {gap['item']}")
                lines.append("")

    content = "\n".join(lines)

    if output_path:
        Path(output_path).write_text(content, encoding='utf-8')
        print(f"\n Relatório salvo em: {output_path}")

    return content


def main():
    if len(sys.argv) < 2:
        print("Uso:")
        print("  python validator-rl.py RFXXX")
        print("  python validator-rl.py --fase N")
        print("  python validator-rl.py --all")
        sys.exit(1)

    validador = ValidadorRL()
    results = []

    arg = sys.argv[1]

    if arg == '--all':
        print("Validando TODOS os RFs do projeto...")
        results = validador.validar_todos()
        output_file = "D:\\IC2\\relatorios\\validacao-rl-completa.md"

    elif arg == '--fase':
        if len(sys.argv) < 3:
            print(" Especifique o número da fase: --fase N")
            sys.exit(1)

        fase_num = int(sys.argv[2])
        print(f"Validando RFs da Fase {fase_num}...")
        results = validador.validar_fase(fase_num)
        output_file = f"D:\\IC2\\relatorios\\validacao-rl-fase{fase_num}.md"

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
        print(f"Separação Válida: {'' if result.separacao_valida else ''}")
        print(f"RL Estruturado: {'' if result.rl_estruturado else ''}")
        print(f"Itens Legado: {result.itens_legado}")
        print(f"Itens com Destino: {result.itens_com_destino}")

        if result.gaps:
            print(f"\nGaps Encontrados: {len(result.gaps)}")
            for gap in result.gaps:
                tipo = gap.get('tipo', 'INFO')
                msg = gap.get('mensagem', '')
                print(f"  [{tipo}] {msg}")
                if 'item' in gap:
                    print(f"    Item: {gap['item']}")
        else:
            print("\n Nenhum gap encontrado!")

        # JSON output
        print("\n" + "="*60)
        print("JSON:")
        print("="*60)
        print(result.to_json())

    # Gerar relatório se múltiplos RFs
    if len(results) > 1:
        gerar_relatorio_markdown(results, output_file)

        # Resumo no console
        total = len(results)
        conformes = sum(1 for r in results if r.separacao_valida and r.rl_estruturado)
        print(f"\n{'='*60}")
        print(f"RESUMO: {conformes}/{total} RFs conformes ({conformes/total*100:.1f}%)")
        print('='*60)


if __name__ == '__main__':
    main()
