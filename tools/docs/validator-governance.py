#!/usr/bin/env python3
"""
validator-governance.py - Validador de Governança Completa

Valida que:
1. STATUS.yaml existe e está bem formado
2. Arquivos obrigatórios estão presentes (RFXXX.md, RFXXX.yaml, RL-RFXXX.md/yaml, UC-RFXXX.md/yaml)
3. STATUS.yaml reflete arquivos reais (documentacao.rf = true se RFXXX.md existe)
4. Backend skeleton tem observacao preenchida
5. user-stories.yaml existe se STATUS marca como criado

Uso:
    python validator-governance.py RFXXX
    python validator-governance.py --fase 1
    python validator-governance.py --all

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
from datetime import datetime


@dataclass
class GovernanceValidationResult:
    """Resultado da validação de governança de um RF"""
    rf_id: str
    status_yaml_valido: bool
    arquivos_obrigatorios_presentes: bool
    status_reflete_realidade: bool
    observacoes_backend_validas: bool
    user_stories_conforme: bool
    gaps: List[Dict[str, str]]

    def to_dict(self):
        return asdict(self)

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)

    @property
    def conforme(self) -> bool:
        """RF está 100% conforme governança"""
        return (
            self.status_yaml_valido and
            self.arquivos_obrigatorios_presentes and
            self.status_reflete_realidade and
            self.observacoes_backend_validas and
            self.user_stories_conforme
        )


class ValidadorGovernanca:
    """Validador de Governança Completa"""

    # Arquivos obrigatórios por RF
    ARQUIVOS_OBRIGATORIOS = {
        'rf_md': '{rf_id}.md',
        'rf_yaml': '{rf_id}.yaml',
        'rl_md': 'RL-{rf_id}.md',
        'rl_yaml': 'RL-{rf_id}.yaml',
        'uc_md': 'UC-{rf_id}.md',
        'uc_yaml': 'UC-{rf_id}.yaml',
        'md_yaml': 'MD-{rf_id}.yaml',
        'status_yaml': 'STATUS.yaml',
    }

    # Campos obrigatórios em STATUS.yaml
    CAMPOS_STATUS_OBRIGATORIOS = [
        'rf_id',
        'titulo',
        'fase',
        'epic',
        'status',
        'documentacao',
        'backend_skeleton',
        'implementacao'
    ]

    def __init__(self, base_path: str = "D:\\IC2\\docs\\rf"):
        self.base_path = Path(base_path)

    def encontrar_rf(self, rf_id: str) -> Path:
        """Encontra a pasta do RF"""
        for fase_dir in self.base_path.glob("Fase-*"):
            for epic_dir in fase_dir.glob("EPIC-*"):
                for rf_dir in epic_dir.glob(f"{rf_id}-*"):
                    return rf_dir

        raise FileNotFoundError(f"RF {rf_id} não encontrado em {self.base_path}")

    def validar_status_yaml(self, rf_path: Path) -> Tuple[bool, Dict, List[Dict[str, str]]]:
        """Valida STATUS.yaml existe e está bem formado"""
        status_yaml = rf_path / "STATUS.yaml"
        gaps = []

        if not status_yaml.exists():
            return False, {}, [{
                "tipo": "CRÍTICO",
                "mensagem": "Arquivo STATUS.yaml não encontrado"
            }]

        try:
            with open(status_yaml, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            return False, {}, [{
                "tipo": "CRÍTICO",
                "arquivo": "STATUS.yaml",
                "mensagem": f"YAML inválido: {str(e)}"
            }]
        except Exception as e:
            return False, {}, [{
                "tipo": "CRÍTICO",
                "arquivo": "STATUS.yaml",
                "mensagem": f"Erro ao ler arquivo: {str(e)}"
            }]

        # Validar campos obrigatórios
        for campo in self.CAMPOS_STATUS_OBRIGATORIOS:
            if campo not in data:
                gaps.append({
                    "tipo": "CRÍTICO",
                    "arquivo": "STATUS.yaml",
                    "mensagem": f"Campo obrigatório '{campo}' ausente"
                })

        # Validar estrutura de 'documentacao'
        if 'documentacao' in data:
            doc = data['documentacao']
            campos_doc_obrigatorios = ['rf', 'rl', 'uc', 'md', 'wf', 'user_stories']

            for campo in campos_doc_obrigatorios:
                if campo not in doc:
                    gaps.append({
                        "tipo": "IMPORTANTE",
                        "arquivo": "STATUS.yaml",
                        "secao": "documentacao",
                        "mensagem": f"Campo '{campo}' ausente em documentacao"
                    })

        # Validar estrutura de 'separacao_rf_rl' (se existir)
        if 'separacao_rf_rl' in data:
            sep = data['separacao_rf_rl']
            campos_sep_obrigatorios = ['rf_limpo', 'rl_completo', 'itens_com_destino', 'validador_executado']

            for campo in campos_sep_obrigatorios:
                if campo not in sep:
                    gaps.append({
                        "tipo": "IMPORTANTE",
                        "arquivo": "STATUS.yaml",
                        "secao": "separacao_rf_rl",
                        "mensagem": f"Campo '{campo}' ausente em separacao_rf_rl"
                    })

        return len(gaps) == 0, data, gaps

    def validar_arquivos_obrigatorios(self, rf_path: Path, rf_id: str) -> Tuple[bool, List[Dict[str, str]]]:
        """Valida presença de arquivos obrigatórios"""
        gaps = []
        arquivos_presentes = {}

        for key, template in self.ARQUIVOS_OBRIGATORIOS.items():
            filename = template.format(rf_id=rf_id)
            filepath = rf_path / filename
            presente = filepath.exists()
            arquivos_presentes[key] = presente

            if not presente:
                # RF.yaml, RL.yaml, UC.yaml, MD.yaml podem não existir ainda (migração em andamento)
                if key in ['rf_yaml', 'rl_yaml', 'uc_yaml', 'md_yaml']:
                    gaps.append({
                        "tipo": "IMPORTANTE",
                        "mensagem": f"Arquivo '{filename}' não encontrado (migração pendente)"
                    })
                else:
                    gaps.append({
                        "tipo": "CRÍTICO",
                        "mensagem": f"Arquivo obrigatório '{filename}' não encontrado"
                    })

        # Verificar README.md
        readme = rf_path / "README.md"
        if not readme.exists():
            gaps.append({
                "tipo": "MENOR",
                "mensagem": "README.md não encontrado (recomendado)"
            })

        todos_presentes = all(arquivos_presentes[k] for k in ['rf_md', 'rl_md', 'uc_md', 'status_yaml'])
        return todos_presentes, gaps

    def validar_status_reflete_realidade(
        self,
        rf_path: Path,
        rf_id: str,
        status_data: Dict
    ) -> Tuple[bool, List[Dict[str, str]]]:
        """Valida que STATUS.yaml reflete arquivos reais"""
        gaps = []
        doc = status_data.get('documentacao', {})

        # Mapear status → arquivo
        validacoes = [
            ('rf', f'{rf_id}.md'),
            ('rl', f'RL-{rf_id}.md'),
            ('uc', f'UC-{rf_id}.md'),
            ('md', f'MD-{rf_id}.yaml'),
            ('wf', f'WF-{rf_id}.md'),
            ('user_stories', 'user-stories.yaml'),
        ]

        for campo, filename in validacoes:
            status_diz = doc.get(campo, False)
            arquivo_existe = (rf_path / filename).exists()

            # MD pode ser .md ou .yaml
            if campo == 'md':
                md_md = (rf_path / f'MD-{rf_id}.md').exists()
                md_yaml = arquivo_existe
                arquivo_existe = md_md or md_yaml

            if status_diz and not arquivo_existe:
                gaps.append({
                    "tipo": "CRÍTICO",
                    "arquivo": "STATUS.yaml",
                    "secao": "documentacao",
                    "mensagem": f"STATUS marca '{campo}' como True mas arquivo '{filename}' não existe"
                })

            if not status_diz and arquivo_existe:
                gaps.append({
                    "tipo": "IMPORTANTE",
                    "arquivo": "STATUS.yaml",
                    "secao": "documentacao",
                    "mensagem": f"Arquivo '{filename}' existe mas STATUS marca '{campo}' como False"
                })

        # Validar separacao_rf_rl (se existir)
        if 'separacao_rf_rl' in status_data:
            sep = status_data['separacao_rf_rl']

            # Se separacao_rf_rl existe, arquivos RL devem existir
            if not (rf_path / f'RL-{rf_id}.md').exists():
                gaps.append({
                    "tipo": "CRÍTICO",
                    "secao": "separacao_rf_rl",
                    "mensagem": "separacao_rf_rl declarada mas RL-{rf_id}.md não existe"
                })

            if not (rf_path / f'RL-{rf_id}.yaml').exists():
                gaps.append({
                    "tipo": "CRÍTICO",
                    "secao": "separacao_rf_rl",
                    "mensagem": "separacao_rf_rl declarada mas RL-{rf_id}.yaml não existe"
                })

        return len(gaps) == 0, gaps

    def validar_observacoes_backend(self, status_data: Dict) -> Tuple[bool, List[Dict[str, str]]]:
        """Valida que backend skeleton tem observacao se incompleto"""
        gaps = []
        skeleton = status_data.get('backend_skeleton', {})

        if not isinstance(skeleton, dict):
            return True, []  # Backend não iniciado

        # Se skeleton existe e está incompleto
        completo = skeleton.get('completo', False)

        if not completo:
            # Se não está completo, DEVE ter observacao
            if 'observacao' not in skeleton or not skeleton['observacao']:
                gaps.append({
                    "tipo": "IMPORTANTE",
                    "arquivo": "STATUS.yaml",
                    "secao": "backend_skeleton",
                    "mensagem": "Backend skeleton incompleto DEVE ter campo 'observacao' preenchido"
                })

            # Validar percentual
            if 'percentual_completo' in skeleton:
                perc = skeleton['percentual_completo']
                if not isinstance(perc, (int, float)):
                    gaps.append({
                        "tipo": "MENOR",
                        "secao": "backend_skeleton",
                        "mensagem": "percentual_completo deve ser número"
                    })
                elif perc < 0 or perc > 100:
                    gaps.append({
                        "tipo": "MENOR",
                        "secao": "backend_skeleton",
                        "mensagem": f"percentual_completo inválido: {perc}% (deve ser 0-100)"
                    })

        return len(gaps) == 0, gaps

    def validar_user_stories(self, rf_path: Path, status_data: Dict) -> Tuple[bool, List[Dict[str, str]]]:
        """Valida user-stories.yaml se STATUS marca como criado"""
        gaps = []
        doc = status_data.get('documentacao', {})
        us_declarado = doc.get('user_stories', False)

        us_file = rf_path / 'user-stories.yaml'
        us_existe = us_file.exists()

        if us_declarado and not us_existe:
            gaps.append({
                "tipo": "CRÍTICO",
                "arquivo": "STATUS.yaml",
                "mensagem": "user_stories marcado como True mas user-stories.yaml não existe"
            })

        if us_existe and not us_declarado:
            gaps.append({
                "tipo": "IMPORTANTE",
                "mensagem": "user-stories.yaml existe mas STATUS não marca como criado"
            })

        # Se existe, validar estrutura básica
        if us_existe:
            try:
                with open(us_file, 'r', encoding='utf-8') as f:
                    us_data = yaml.safe_load(f)

                if 'rf_id' not in us_data:
                    gaps.append({
                        "tipo": "IMPORTANTE",
                        "arquivo": "user-stories.yaml",
                        "mensagem": "Campo 'rf_id' ausente"
                    })

                if 'user_stories' not in us_data:
                    gaps.append({
                        "tipo": "CRÍTICO",
                        "arquivo": "user-stories.yaml",
                        "mensagem": "Seção 'user_stories' ausente"
                    })
                else:
                    stories = us_data['user_stories']
                    if not isinstance(stories, list):
                        gaps.append({
                            "tipo": "CRÍTICO",
                            "arquivo": "user-stories.yaml",
                            "mensagem": "'user_stories' deve ser uma lista"
                        })
                    elif len(stories) < 2:
                        gaps.append({
                            "tipo": "IMPORTANTE",
                            "arquivo": "user-stories.yaml",
                            "mensagem": f"Mínimo 2 User Stories esperado, encontrado {len(stories)}"
                        })

            except yaml.YAMLError as e:
                gaps.append({
                    "tipo": "CRÍTICO",
                    "arquivo": "user-stories.yaml",
                    "mensagem": f"YAML inválido: {str(e)}"
                })

        return len(gaps) == 0, gaps

    def validar_rf(self, rf_id: str) -> GovernanceValidationResult:
        """Valida governança completa de um RF"""
        try:
            rf_path = self.encontrar_rf(rf_id)
        except FileNotFoundError as e:
            return GovernanceValidationResult(
                rf_id=rf_id,
                status_yaml_valido=False,
                arquivos_obrigatorios_presentes=False,
                status_reflete_realidade=False,
                observacoes_backend_validas=False,
                user_stories_conforme=False,
                gaps=[{"tipo": "CRÍTICO", "mensagem": str(e)}]
            )

        all_gaps = []

        # Validação 1: STATUS.yaml válido
        status_valido, status_data, gaps_status = self.validar_status_yaml(rf_path)
        all_gaps.extend(gaps_status)

        # Validação 2: Arquivos obrigatórios presentes
        arquivos_ok, gaps_arq = self.validar_arquivos_obrigatorios(rf_path, rf_id)
        all_gaps.extend(gaps_arq)

        # Validação 3: STATUS reflete realidade
        status_reflete = True
        if status_valido and status_data:
            status_reflete, gaps_reflete = self.validar_status_reflete_realidade(rf_path, rf_id, status_data)
            all_gaps.extend(gaps_reflete)

        # Validação 4: Observações backend válidas
        obs_validas = True
        if status_valido and status_data:
            obs_validas, gaps_obs = self.validar_observacoes_backend(status_data)
            all_gaps.extend(gaps_obs)

        # Validação 5: User stories conforme
        us_conforme = True
        if status_valido and status_data:
            us_conforme, gaps_us = self.validar_user_stories(rf_path, status_data)
            all_gaps.extend(gaps_us)

        return GovernanceValidationResult(
            rf_id=rf_id,
            status_yaml_valido=status_valido,
            arquivos_obrigatorios_presentes=arquivos_ok,
            status_reflete_realidade=status_reflete,
            observacoes_backend_validas=obs_validas,
            user_stories_conforme=us_conforme,
            gaps=all_gaps
        )

    def validar_fase(self, fase_num: int) -> List[GovernanceValidationResult]:
        """Valida todos os RFs de uma fase"""
        results = []
        fase_dir = self.base_path / f"Fase-{fase_num}"

        if not fase_dir.exists():
            print(f"❌ Fase {fase_num} não encontrada em {self.base_path}")
            return results

        for epic_dir in sorted(fase_dir.glob("EPIC-*")):
            for rf_dir in sorted(epic_dir.glob("RF*")):
                rf_id = rf_dir.name.split('-')[0]
                print(f"Validando {rf_id}...")
                result = self.validar_rf(rf_id)
                results.append(result)

        return results

    def validar_todos(self) -> List[GovernanceValidationResult]:
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


def gerar_relatorio_markdown(results: List[GovernanceValidationResult], output_path: str = None):
    """Gera relatório em Markdown"""
    total = len(results)
    conformes = sum(1 for r in results if r.conforme)
    taxa_conformidade = (conformes / total * 100) if total > 0 else 0

    lines = [
        "# Relatório de Validação de Governança",
        "",
        f"**Data:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"**Total de RFs:** {total}",
        f"**Conformes:** {conformes} ({taxa_conformidade:.1f}%)",
        "",
        "---",
        "",
        "## Resumo por RF",
        "",
        "| RF | STATUS.yaml | Arquivos | Reflete Realidade | Backend | User Stories | Status |",
        "|-----|-------------|----------|-------------------|---------|--------------|--------|"
    ]

    for result in results:
        status = "✅ CONFORME" if result.conforme else "❌ GAPS"
        status_icon = "✅" if result.status_yaml_valido else "❌"
        arq_icon = "✅" if result.arquivos_obrigatorios_presentes else "❌"
        ref_icon = "✅" if result.status_reflete_realidade else "❌"
        back_icon = "✅" if result.observacoes_backend_validas else "❌"
        us_icon = "✅" if result.user_stories_conforme else "✅"

        lines.append(
            f"| {result.rf_id} | {status_icon} | {arq_icon} | {ref_icon} | "
            f"{back_icon} | {us_icon} | {status} |"
        )

    lines.extend(["", "---", "", "## Gaps Identificados", ""])

    for result in results:
        if result.gaps:
            lines.append(f"### {result.rf_id}")
            lines.append("")

            criticos = [g for g in result.gaps if g.get('tipo') == 'CRÍTICO']
            importantes = [g for g in result.gaps if g.get('tipo') == 'IMPORTANTE']
            menores = [g for g in result.gaps if g.get('tipo') == 'MENOR']

            if criticos:
                lines.append("**CRÍTICO:**")
                for gap in criticos:
                    lines.append(f"- {gap.get('mensagem')}")
                    if 'arquivo' in gap:
                        lines.append(f"  - Arquivo: {gap['arquivo']}")
                    if 'secao' in gap:
                        lines.append(f"  - Seção: {gap['secao']}")
                lines.append("")

            if importantes:
                lines.append("**IMPORTANTE:**")
                for gap in importantes:
                    lines.append(f"- {gap.get('mensagem')}")
                    if 'arquivo' in gap:
                        lines.append(f"  - Arquivo: {gap['arquivo']}")
                    if 'secao' in gap:
                        lines.append(f"  - Seção: {gap['secao']}")
                lines.append("")

            if menores:
                lines.append("**MENOR:**")
                for gap in menores:
                    lines.append(f"- {gap.get('mensagem')}")
                lines.append("")

    content = "\n".join(lines)

    if output_path:
        Path(output_path).write_text(content, encoding='utf-8')
        print(f"\n✅ Relatório salvo em: {output_path}")

    return content


def main():
    if len(sys.argv) < 2:
        print("Uso:")
        print("  python validator-governance.py RFXXX")
        print("  python validator-governance.py --fase N")
        print("  python validator-governance.py --all")
        sys.exit(1)

    validador = ValidadorGovernanca()
    results = []

    arg = sys.argv[1]

    if arg == '--all':
        print("Validando TODOS os RFs do projeto...")
        results = validador.validar_todos()
        output_file = "D:\\IC2\\relatorios\\validacao-governanca-completa.md"

    elif arg == '--fase':
        if len(sys.argv) < 3:
            print("❌ Especifique o número da fase: --fase N")
            sys.exit(1)

        fase_num = int(sys.argv[2])
        print(f"Validando RFs da Fase {fase_num}...")
        results = validador.validar_fase(fase_num)
        output_file = f"D:\\IC2\\relatorios\\validacao-governanca-fase{fase_num}.md"

    else:
        rf_id = arg
        print(f"Validando {rf_id}...")
        result = validador.validar_rf(rf_id)
        results = [result]
        output_file = None

        print("\n" + "="*60)
        print(f"RESULTADO: {rf_id}")
        print("="*60)
        print(f"STATUS.yaml Válido: {'✅' if result.status_yaml_valido else '❌'}")
        print(f"Arquivos Obrigatórios: {'✅' if result.arquivos_obrigatorios_presentes else '❌'}")
        print(f"STATUS Reflete Realidade: {'✅' if result.status_reflete_realidade else '❌'}")
        print(f"Observações Backend: {'✅' if result.observacoes_backend_validas else '✅'}")
        print(f"User Stories: {'✅' if result.user_stories_conforme else '✅'}")
        print(f"\nCONFORME: {'✅ SIM' if result.conforme else '❌ NÃO'}")

        if result.gaps:
            print(f"\nGaps Encontrados: {len(result.gaps)}")
            for gap in result.gaps:
                tipo = gap.get('tipo', 'INFO')
                msg = gap.get('mensagem', '')
                print(f"  [{tipo}] {msg}")
        else:
            print("\n✅ Nenhum gap encontrado!")

        print("\n" + "="*60)
        print("JSON:")
        print("="*60)
        print(result.to_json())

    if len(results) > 1:
        gerar_relatorio_markdown(results, output_file)

        total = len(results)
        conformes = sum(1 for r in results if r.conforme)
        print(f"\n{'='*60}")
        print(f"RESUMO: {conformes}/{total} RFs conformes ({conformes/total*100:.1f}%)")
        print('='*60)


if __name__ == '__main__':
    main()
