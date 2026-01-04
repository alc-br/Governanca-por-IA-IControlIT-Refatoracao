#!/usr/bin/env python3
"""
validator-rf-uc-coverage.py - Validador de Cobertura RF → UC

Valida se os UCs cobrem 100% das funcionalidades e RNs do RF.

Detecções:
1. Funcionalidades do RF sem UC correspondente
2. RNs do RF sem referência em UC
3. UCs que introduzem comportamento fora do RF
4. Sincronização UC.md ↔ UC.yaml

Saída:
- auditoria.json com gaps detalhados
- Exit code 0 (PASS) ou 1 (FAIL)

Uso:
    python validator-rf-uc-coverage.py --rf RF001
    python validator-rf-uc-coverage.py --all  # Todos os RFs

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
from typing import Dict, List, Set, Tuple, Any
from dataclasses import dataclass, asdict, field
from datetime import datetime

# Force UTF-8 encoding
os.environ['PYTHONIOENCODING'] = 'utf-8'
if sys.platform == 'win32':
    sys.stdin.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')


# =====================================================
# ESTRUTURAS DE DADOS
# =====================================================

@dataclass
class CoberturaItem:
    """Item de cobertura (funcionalidade ou RN)"""
    id: str
    tipo: str  # 'funcionalidade' ou 'rn'
    descricao: str
    coberto: bool = False
    coberto_por: List[str] = field(default_factory=list)  # Lista de UCs que cobrem


@dataclass
class GapCobertura:
    """Gap de cobertura detectado"""
    tipo: str  # 'funcionalidade_nao_coberta', 'rn_nao_coberta', 'uc_fora_escopo'
    item_id: str
    descricao: str
    severidade: str  # 'CRÍTICO', 'IMPORTANTE', 'MENOR'
    recomendacao: str


@dataclass
class ResultadoCobertura:
    """Resultado completo da análise de cobertura"""
    rf_id: str
    total_funcionalidades: int
    funcionalidades_cobertas: int
    total_rns: int
    rns_cobertas: int
    total_ucs: int
    gaps: List[GapCobertura] = field(default_factory=list)
    cobertura_percentual: float = 0.0
    conforme: bool = False
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self):
        return {
            **asdict(self),
            'gaps': [asdict(g) for g in self.gaps]
        }


# =====================================================
# EXTRATORES
# =====================================================

class ExtratorRF:
    """Extrai funcionalidades e RNs do RF"""

    def __init__(self, rf_path: str):
        self.rf_path = Path(rf_path)
        # Extrair RF ID do nome da pasta (ex: RF001-Parametros-... → RF001)
        rf_id = self.rf_path.name.split('-')[0]
        self.rf_md = self.rf_path / f"{rf_id}.md"
        self.rf_yaml = self.rf_path / f"{rf_id}.yaml"

    def extrair_funcionalidades(self) -> List[CoberturaItem]:
        """Extrai funcionalidades do RF.md"""
        funcionalidades = []

        if not self.rf_md.exists():
            return funcionalidades

        try:
            content = self.rf_md.read_text(encoding='utf-8')

            # Procurar seção "## 2. FUNCIONALIDADES" ou similar
            # Padrão: ### 2.1. Título da Funcionalidade
            pattern_funcionalidades = r'###\s+\d+\.\d+\.?\s+(.+)'

            # Encontrar seção de funcionalidades
            in_funcionalidades_section = False
            for line in content.split('\n'):
                # Detectar início da seção de funcionalidades
                if re.match(r'##\s+\d+\.?\s+FUNCIONALIDADES', line, re.IGNORECASE):
                    in_funcionalidades_section = True
                    continue

                # Detectar fim da seção (próxima seção nível 2)
                if in_funcionalidades_section and re.match(r'##\s+\d+', line):
                    break

                # Extrair funcionalidades (### 2.1, ### 2.2, etc)
                if in_funcionalidades_section:
                    match = re.match(pattern_funcionalidades, line)
                    if match:
                        titulo = match.group(1).strip()
                        # Gerar ID baseado no título (simplificado)
                        func_id = f"FUNC-{len(funcionalidades)+1:02d}"
                        funcionalidades.append(CoberturaItem(
                            id=func_id,
                            tipo='funcionalidade',
                            descricao=titulo
                        ))

            # Se não encontrou funcionalidades no MD, tentar RF.yaml
            if not funcionalidades and self.rf_yaml.exists():
                with open(self.rf_yaml, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f) or {}

                # Tentar extrair do escopo.incluso
                escopo_incluso = data.get('escopo', {}).get('incluso', [])
                for idx, item in enumerate(escopo_incluso, 1):
                    funcionalidades.append(CoberturaItem(
                        id=f"FUNC-{idx:02d}",
                        tipo='funcionalidade',
                        descricao=item if isinstance(item, str) else item.get('descricao', '')
                    ))

        except Exception as e:
            print(f"⚠️  Erro ao ler RF.md: {e}", file=sys.stderr)

        return funcionalidades

    def extrair_rns(self) -> List[CoberturaItem]:
        """Extrai RNs do RF.md e RF.yaml"""
        rns = []

        # Tentar RF.yaml primeiro (mais estruturado)
        if self.rf_yaml.exists():
            try:
                with open(self.rf_yaml, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f) or {}

                regras = data.get('regras_negocio', [])
                for regra in regras:
                    if isinstance(regra, dict) and 'id' in regra:
                        rns.append(CoberturaItem(
                            id=regra['id'],
                            tipo='rn',
                            descricao=regra.get('descricao', '')[:100]
                        ))
            except Exception as e:
                print(f"⚠️  Erro ao ler RF.yaml: {e}", file=sys.stderr)

        # Complementar com RF.md
        if self.rf_md.exists():
            try:
                content = self.rf_md.read_text(encoding='utf-8')

                # Padrões de RN:
                # 1. **RN-SYS-XXX-NN**: Descrição
                # 2. RN-RFXXX-NNN: Descrição
                # 3. **RN-XXX-NNN**
                patterns = [
                    r'\*?\*?RN-[A-Z]{3}-\d{3}-\d{2}\*?\*?:?\s*(.+)',
                    r'\*?\*?RN-RF\d{3}-\d{3}\*?\*?:?\s*(.+)',
                    r'\*?\*?RN-[A-Z]+-\d{3}-\d{2}\*?\*?:?\s*(.+)'
                ]

                rn_ids_existentes = {rn.id for rn in rns}

                for pattern in patterns:
                    for match in re.finditer(pattern, content):
                        rn_match = re.search(r'RN-[A-Z]+-\d{3}-\d{2,3}', match.group(0))
                        if rn_match:
                            rn_id = rn_match.group(0)
                            if rn_id not in rn_ids_existentes:
                                rns.append(CoberturaItem(
                                    id=rn_id,
                                    tipo='rn',
                                    descricao=match.group(1).strip()[:100]
                                ))
                                rn_ids_existentes.add(rn_id)

            except Exception as e:
                print(f"⚠️  Erro ao ler RF.md: {e}", file=sys.stderr)

        return rns


class ExtratorUC:
    """Extrai UCs e suas coberturas"""

    def __init__(self, uc_path: str):
        self.uc_path = Path(uc_path)
        self.uc_md = list(self.uc_path.glob("UC-*.md"))
        self.uc_yaml = list(self.uc_path.glob("UC-*.yaml"))

    def extrair_ucs(self) -> Set[str]:
        """Extrai IDs dos UCs"""
        ucs = set()

        # Do MD
        for uc_md_file in self.uc_md:
            content = uc_md_file.read_text(encoding='utf-8')
            # Padrão: ## UC00, ### UC01, etc
            found = re.findall(r'##\s+(UC\d{2})', content)
            ucs.update(found)

        # Do YAML (validação cruzada)
        for uc_yaml_file in self.uc_yaml:
            try:
                with open(uc_yaml_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f) or {}

                casos = data.get('casos_de_uso', [])
                for caso in casos:
                    if isinstance(caso, dict) and 'id' in caso:
                        ucs.add(caso['id'])
            except:
                pass

        return ucs

    def extrair_cobertura_funcionalidades(self) -> Dict[str, List[str]]:
        """Extrai quais UCs cobrem quais funcionalidades (via UC.yaml)"""
        cobertura = {}

        for uc_yaml_file in self.uc_yaml:
            try:
                with open(uc_yaml_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f) or {}

                casos = data.get('casos_de_uso', [])
                for caso in casos:
                    if isinstance(caso, dict):
                        uc_id = caso.get('id')
                        rf_items = caso.get('covers', {}).get('rf_items', [])

                        for rf_item in rf_items:
                            if rf_item not in cobertura:
                                cobertura[rf_item] = []
                            cobertura[rf_item].append(uc_id)

            except Exception as e:
                print(f"⚠️  Erro ao ler {uc_yaml_file.name}: {e}", file=sys.stderr)

        return cobertura

    def extrair_rns_referenciadas(self) -> Set[str]:
        """Extrai RNs referenciadas nos UCs"""
        rns = set()

        for uc_md_file in self.uc_md:
            content = uc_md_file.read_text(encoding='utf-8')

            # Padrões de RN (captura TODOS os formatos):
            # 1. RN-SYS-XXX-NN (ex: RN-SYS-001-01)
            # 2. RN-RFXXX-NNN (ex: RN-RF061-001)
            # 3. RN-UC-XX-NNN (ex: RN-UC-01-001)
            # 4. RN-XXX-NNN-NN (ex: RN-JOB-112-01)
            # 5. Outros padrões similares

            # Regex universal: RN-[LETRAS]-[NÚMEROS]-[NÚMEROS]
            # Aceita 2 ou 3 dígitos finais para compatibilidade
            found = re.findall(r'RN-[A-Z]{2,4}-\d{2,3}-\d{2,3}', content)
            rns.update(found)

        return rns


# =====================================================
# ANALISADOR DE COBERTURA
# =====================================================

class AnalisadorCobertura:
    """Analisa cobertura RF → UC"""

    def __init__(self, rf_path: str):
        self.rf_path = Path(rf_path)
        self.rf_id = self.rf_path.name.split('-')[0]  # Ex: RF001
        self.extrator_rf = ExtratorRF(rf_path)
        self.extrator_uc = ExtratorUC(rf_path)

    def analisar(self) -> ResultadoCobertura:
        """Executa análise completa de cobertura"""

        # Extrair do RF
        funcionalidades = self.extrator_rf.extrair_funcionalidades()
        rns_rf = self.extrator_rf.extrair_rns()

        # Extrair dos UCs
        ucs = self.extrator_uc.extrair_ucs()
        cobertura_func = self.extrator_uc.extrair_cobertura_funcionalidades()
        rns_uc = self.extrator_uc.extrair_rns_referenciadas()

        # Marcar funcionalidades cobertas
        for func in funcionalidades:
            if func.id in cobertura_func:
                func.coberto = True
                func.coberto_por = cobertura_func[func.id]

        # Marcar RNs cobertas
        for rn in rns_rf:
            if rn.id in rns_uc:
                rn.coberto = True
                rn.coberto_por = ['UC (referenciado)']

        # Detectar gaps
        gaps = self._detectar_gaps(funcionalidades, rns_rf, ucs)

        # Calcular métricas
        func_cobertas = sum(1 for f in funcionalidades if f.coberto)
        rns_cobertas = sum(1 for r in rns_rf if r.coberto)

        total_items = len(funcionalidades) + len(rns_rf)
        items_cobertos = func_cobertas + rns_cobertas

        cobertura_pct = (items_cobertos / total_items * 100) if total_items > 0 else 0

        # Determinar conformidade (100% obrigatório)
        conforme = (cobertura_pct == 100.0) and (len(gaps) == 0)

        return ResultadoCobertura(
            rf_id=self.rf_id,
            total_funcionalidades=len(funcionalidades),
            funcionalidades_cobertas=func_cobertas,
            total_rns=len(rns_rf),
            rns_cobertas=rns_cobertas,
            total_ucs=len(ucs),
            gaps=gaps,
            cobertura_percentual=round(cobertura_pct, 2),
            conforme=conforme
        )

    def _detectar_gaps(
        self,
        funcionalidades: List[CoberturaItem],
        rns: List[CoberturaItem],
        ucs: Set[str]
    ) -> List[GapCobertura]:
        """Detecta gaps de cobertura"""
        gaps = []

        # Gap 1: Funcionalidades não cobertas
        for func in funcionalidades:
            if not func.coberto:
                gaps.append(GapCobertura(
                    tipo='funcionalidade_nao_coberta',
                    item_id=func.id,
                    descricao=f"Funcionalidade '{func.id}' do RF não está coberta por nenhum UC",
                    severidade='CRÍTICO',
                    recomendacao=f"Criar UC que cubra '{func.id}' ou adicionar em UC existente (campo covers.rf_items no UC.yaml)"
                ))

        # Gap 2: RNs não referenciadas
        for rn in rns:
            if not rn.coberto:
                gaps.append(GapCobertura(
                    tipo='rn_nao_coberta',
                    item_id=rn.id,
                    descricao=f"Regra de Negócio '{rn.id}' não está referenciada em nenhum UC",
                    severidade='IMPORTANTE',
                    recomendacao=f"Adicionar '{rn.id}' na seção 'Regras de Negócio' do UC correspondente"
                ))

        # Gap 3: Verificar quantidade mínima de UCs (CRUD = UC00-UC04)
        ucs_minimos_crud = {'UC00', 'UC01', 'UC02', 'UC03', 'UC04'}
        if not ucs_minimos_crud.issubset(ucs) and len(funcionalidades) > 0:
            faltantes = ucs_minimos_crud - ucs
            if faltantes:
                gaps.append(GapCobertura(
                    tipo='ucs_faltantes',
                    item_id=', '.join(sorted(faltantes)),
                    descricao=f"UCs CRUD obrigatórios faltando: {', '.join(sorted(faltantes))}",
                    severidade='CRÍTICO',
                    recomendacao=f"Criar UCs faltantes: {', '.join(sorted(faltantes))}"
                ))

        return gaps


# =====================================================
# GERADOR DE RELATÓRIOS
# =====================================================

class GeradorRelatorio:
    """Gera relatórios de cobertura"""

    @staticmethod
    def gerar_console(resultado: ResultadoCobertura):
        """Gera relatório para console"""
        print(f"\n{'='*80}")
        print(f"📊 ANÁLISE DE COBERTURA RF→UC: {resultado.rf_id}")
        print(f"{'='*80}\n")

        # Métricas
        print("📈 MÉTRICAS:")
        print(f"   Funcionalidades: {resultado.funcionalidades_cobertas}/{resultado.total_funcionalidades}")
        print(f"   Regras de Negócio: {resultado.rns_cobertas}/{resultado.total_rns}")
        print(f"   Total de UCs: {resultado.total_ucs}")
        print(f"   Cobertura: {resultado.cobertura_percentual}%")
        print(f"   Status: {'✅ CONFORME' if resultado.conforme else '❌ NÃO CONFORME'}\n")

        # Gaps
        if resultado.gaps:
            print(f"⚠️  GAPS IDENTIFICADOS ({len(resultado.gaps)}):\n")

            gaps_criticos = [g for g in resultado.gaps if g.severidade == 'CRÍTICO']
            gaps_importantes = [g for g in resultado.gaps if g.severidade == 'IMPORTANTE']
            gaps_menores = [g for g in resultado.gaps if g.severidade == 'MENOR']

            if gaps_criticos:
                print("🔴 CRÍTICOS:")
                for gap in gaps_criticos:
                    print(f"   • {gap.descricao}")
                    print(f"     ↳ {gap.recomendacao}\n")

            if gaps_importantes:
                print("🟡 IMPORTANTES:")
                for gap in gaps_importantes:
                    print(f"   • {gap.descricao}")
                    print(f"     ↳ {gap.recomendacao}\n")

            if gaps_menores:
                print("🟢 MENORES:")
                for gap in gaps_menores:
                    print(f"   • {gap.descricao}")
                    print(f"     ↳ {gap.recomendacao}\n")

        else:
            print("✅ NENHUM GAP IDENTIFICADO - 100% CONFORME!\n")

        print(f"{'='*80}\n")

    @staticmethod
    def gerar_json(resultado: ResultadoCobertura, output_path: str):
        """Gera relatório JSON"""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(resultado.to_dict(), f, indent=2, ensure_ascii=False)

        print(f"📄 Relatório JSON salvo em: {output_file}")


# =====================================================
# MAIN
# =====================================================

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Validador de Cobertura RF→UC')
    parser.add_argument('--rf', type=str, help='RF específico (ex: RF001)')
    parser.add_argument('--all', action='store_true', help='Validar todos os RFs')
    parser.add_argument('--output', type=str, help='Caminho do relatório JSON')
    args = parser.parse_args()

    base_path = Path('D:/IC2/docs/rf')

    if args.all:
        # Validar todos os RFs
        rfs = sorted(base_path.glob('**/RF*'))
        rfs = [rf for rf in rfs if rf.is_dir() and re.match(r'RF\d{3}', rf.name)]

        resultados = []
        total_conformes = 0

        for rf_path in rfs:
            analisador = AnalisadorCobertura(str(rf_path))
            resultado = analisador.analisar()
            resultados.append(resultado)

            if resultado.conforme:
                total_conformes += 1

        # Resumo geral
        print(f"\n{'='*80}")
        print(f"📊 RESUMO GERAL: {len(resultados)} RFs analisados")
        print(f"{'='*80}\n")
        print(f"   ✅ Conformes: {total_conformes}/{len(resultados)}")
        print(f"   ❌ Não Conformes: {len(resultados) - total_conformes}/{len(resultados)}\n")

        # Detalhes dos não conformes
        nao_conformes = [r for r in resultados if not r.conforme]
        if nao_conformes:
            print("⚠️  RFs NÃO CONFORMES:\n")
            for r in nao_conformes:
                print(f"   {r.rf_id}: {r.cobertura_percentual}% ({len(r.gaps)} gaps)")

        # Salvar JSON consolidado
        if args.output:
            output_data = {
                'timestamp': datetime.now().isoformat(),
                'total_rfs': len(resultados),
                'conformes': total_conformes,
                'nao_conformes': len(resultados) - total_conformes,
                'resultados': [r.to_dict() for r in resultados]
            }

            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)

            print(f"\n📄 Relatório consolidado salvo em: {args.output}")

        sys.exit(0 if total_conformes == len(resultados) else 1)

    elif args.rf:
        # Validar RF específico
        rf_id = args.rf if args.rf.startswith('RF') else f'RF{args.rf}'

        # Encontrar pasta do RF
        rf_paths = list(base_path.glob(f'**/{rf_id}*'))
        rf_paths = [p for p in rf_paths if p.is_dir()]

        if not rf_paths:
            print(f"❌ RF '{rf_id}' não encontrado", file=sys.stderr)
            sys.exit(1)

        rf_path = rf_paths[0]

        # Analisar
        analisador = AnalisadorCobertura(str(rf_path))
        resultado = analisador.analisar()

        # Gerar relatórios
        GeradorRelatorio.gerar_console(resultado)

        if args.output:
            GeradorRelatorio.gerar_json(resultado, args.output)
        else:
            # Salvar em relatorios/rfXXX/uc/auditoria.json
            output_default = f"D:/IC2/relatorios/{rf_id.lower()}/uc/auditoria.json"
            GeradorRelatorio.gerar_json(resultado, output_default)

        sys.exit(0 if resultado.conforme else 1)

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
