#!/usr/bin/env python3
"""
Script de Auditoria e Correção Automática de UCs
Usado pelo CONTRATO-ADEQUACAO-COMPLETA-UC

Capacidades:
1. Auditar nomenclatura (RN-CTR-XX → RN-RFXXX-XX)
2. Auditar cobertura (gaps de RNs)
3. Auditar catálogo híbrido (RF-CRUD-XX)
4. CORRIGIR automaticamente problemas identificados
5. Validar exit code 0
"""

import re
import yaml
from pathlib import Path
from typing import Dict, List, Set, Tuple
from dataclasses import dataclass
import sys

@dataclass
class AuditResult:
    """Resultado da auditoria de um RF"""
    documentacao_id: str
    documentacao_nome: str
    rns_total: int
    rns_cobertas: int
    cobertura_pct: float
    gaps: List[str]
    problemas_nomenclatura: List[str]
    catalogo_hibrido: List[str]
    jobs_nao_documentados: List[str]
    workflows_nao_documentados: List[str]
    integracoes_nao_documentadas: List[str]
    severidade: str  # "CRITICO", "ALTO", "MEDIO", "BAIXO", "CONFORME"


class UCAdequacaoEngine:
    """Motor de adequação automática de UCs"""

    def __init__(self, documentacao_path: Path, uc_path: Path):
        self.rf_path = documentacao_path
        self.uc_path = uc_path
        self.rf_data = None
        self.uc_data = None
        self.audit_result = None

    def run(self) -> AuditResult:
        """Executa auditoria → correção → validação"""
        print(f"🔍 Auditando {self.rf_path.stem}...")

        # 1. Carregar arquivos
        self._load_files()

        # 2. Auditar
        self.audit_result = self._audit()

        # 3. Exibir diagnóstico
        self._print_diagnosis()

        # 4. Corrigir automaticamente
        if self.audit_result.severidade != "CONFORME":
            print(f"\n🔧 Iniciando correção automática...")
            self._auto_correct()

        # 5. Validar
        validation_ok = self._validate()

        if validation_ok:
            print(f"✅ {self.rf_path.stem} adequado com sucesso!")
        else:
            print(f"❌ {self.rf_path.stem} falhou na validação final")
            sys.exit(1)

        return self.audit_result

    def _load_files(self):
        """Carrega RF.yaml e UC.yaml"""
        with open(self.rf_path, 'r', encoding='utf-8') as f:
            self.rf_data = yaml.safe_load(f)

        with open(self.uc_path, 'r', encoding='utf-8') as f:
            self.uc_data = yaml.safe_load(f)

    def _audit(self) -> AuditResult:
        """Executa auditoria completa"""
        documentacao_id = self.rf_data['rf']['id']
        documentacao_nome = self.rf_data['rf']['nome']

        # Extrair RNs do RF
        rns_rf = self._extract_rns_from_rf()
        rns_total = len(rns_rf)

        # Extrair RNs do UC
        rns_uc = self._extract_rns_from_uc()

        # Calcular gaps
        gaps = list(rns_rf - rns_uc)
        rns_cobertas = rns_total - len(gaps)
        cobertura_pct = (rns_cobertas / rns_total * 100) if rns_total > 0 else 0

        # Problemas de nomenclatura
        problemas_nomenclatura = self._check_nomenclatura(rns_uc)

        # Catálogo híbrido
        catalogo_hibrido = self._check_catalogo_hibrido()

        # Jobs, workflows, integrações não documentados
        jobs_nao_doc = self._check_jobs_nao_documentados(rns_rf, rns_uc)
        workflows_nao_doc = self._check_workflows_nao_documentados(rns_rf, rns_uc)
        integracoes_nao_doc = self._check_integracoes_nao_documentadas(rns_rf, rns_uc)

        # Calcular severidade
        severidade = self._calculate_severity(cobertura_pct)

        return AuditResult(
            documentacao_id=rf_id,
            documentacao_nome=rf_nome,
            rns_total=rns_total,
            rns_cobertas=rns_cobertas,
            cobertura_pct=cobertura_pct,
            gaps=gaps,
            problemas_nomenclatura=problemas_nomenclatura,
            catalogo_hibrido=catalogo_hibrido,
            jobs_nao_documentados=jobs_nao_doc,
            workflows_nao_documentados=workflows_nao_doc,
            integracoes_nao_documentadas=integracoes_nao_doc,
            severidade=severidade
        )

    def _extract_rns_from_rf(self) -> Set[str]:
        """Extrai IDs de RNs do RF.yaml"""
        rns = set()
        for regra in self.rf_data.get('regras_negocio', []):
            rn_id = regra.get('id')
            if rn_id:
                rns.add(rn_id)
        return rns

    def _extract_rns_from_uc(self) -> Set[str]:
        """Extrai RNs referenciadas nos UCs"""
        rns = set()
        for uc in self.uc_data.get('casos_uso', []):
            # regras_aplicadas
            for rn in uc.get('regras_aplicadas', []):
                rns.add(rn)
            # covers.rf_items
            for item in uc.get('covers', {}).get('rf_items', []):
                if item.startswith('RN-'):
                    rns.add(item)
        return rns

    def _check_nomenclatura(self, rns_uc: Set[str]) -> List[str]:
        """Verifica nomenclatura não-padrão (RN-CTR-, RN-DEP-, etc.)"""
        non_standard = []
        standard_pattern = re.compile(r'^RN-RF\d{3}-\d{2}$')

        for rn in rns_uc:
            if not standard_pattern.match(rn):
                non_standard.append(rn)

        return non_standard

    def _check_catalogo_hibrido(self) -> List[str]:
        """Verifica códigos de catálogo (RF023-CRUD-XX)"""
        catalog_codes = []
        catalog_pattern = re.compile(r'RF\d{3}-(CRUD|VAL|SEC)-\d{2}')

        for uc in self.uc_data.get('casos_uso', []):
            for item in uc.get('covers', {}).get('rf_items', []):
                if catalog_pattern.match(item):
                    catalog_codes.append(item)

        return catalog_codes

    def _check_jobs_nao_documentados(self, rns_rf: Set[str], rns_uc: Set[str]) -> List[str]:
        """Identifica jobs background sem UCs"""
        jobs = []
        for regra in self.rf_data.get('regras_negocio', []):
            rn_id = regra.get('id')
            tipo = regra.get('tipo', '')
            descricao = regra.get('descricao', '').lower()

            # Heurística: detectar jobs background
            if 'job' in tipo.lower() or 'job' in descricao or 'hangfire' in descricao or 'background' in descricao:
                if rn_id not in rns_uc:
                    jobs.append(rn_id)

        return jobs

    def _check_workflows_nao_documentados(self, rns_rf: Set[str], rns_uc: Set[str]) -> List[str]:
        """Identifica workflows complexos sem UCs"""
        workflows = []
        for regra in self.rf_data.get('regras_negocio', []):
            rn_id = regra.get('id')
            tipo = regra.get('tipo', '')
            descricao = regra.get('descricao', '').lower()

            # Heurística: detectar workflows
            if 'workflow' in tipo.lower() or 'workflow' in descricao or 'aprovação' in descricao or 'state-machine' in descricao:
                if rn_id not in rns_uc:
                    workflows.append(rn_id)

        return workflows

    def _check_integracoes_nao_documentadas(self, rns_rf: Set[str], rns_uc: Set[str]) -> List[str]:
        """Identifica integrações externas sem UCs"""
        integracoes = []
        for regra in self.rf_data.get('regras_negocio', []):
            rn_id = regra.get('id')
            tipo = regra.get('tipo', '')
            descricao = regra.get('descricao', '').lower()

            # Heurística: detectar integrações
            if 'integracao' in tipo.lower() or 'api' in descricao or 'azure' in descricao or 'graph' in descricao or 'externo' in descricao:
                if rn_id not in rns_uc:
                    integracoes.append(rn_id)

        return integracoes

    def _calculate_severity(self, cobertura_pct: float) -> str:
        """Calcula severidade baseado em cobertura"""
        if cobertura_pct == 100:
            return "CONFORME"
        elif cobertura_pct >= 81:
            return "BAIXO"
        elif cobertura_pct >= 51:
            return "MEDIO"
        elif cobertura_pct >= 21:
            return "ALTO"
        else:
            return "CRITICO"

    def _print_diagnosis(self):
        """Exibe diagnóstico detalhado"""
        r = self.audit_result

        print(f"\n📊 DIAGNÓSTICO: {r.rf_id} - {r.rf_nome}")
        print(f"   Cobertura: {r.rns_cobertas}/{r.rns_total} ({r.cobertura_pct:.1f}%)")
        print(f"   Severidade: {r.severidade}")

        if r.gaps:
            print(f"\n❌ Gaps de cobertura ({len(r.gaps)}):")
            for gap in r.gaps[:5]:  # Mostrar só os 5 primeiros
                print(f"   - {gap}")
            if len(r.gaps) > 5:
                print(f"   - ... e mais {len(r.gaps) - 5}")

        if r.problemas_nomenclatura:
            print(f"\n⚠️ Nomenclatura não-padrão ({len(r.problemas_nomenclatura)}):")
            for prob in r.problemas_nomenclatura[:3]:
                print(f"   - {prob}")

        if r.catalogo_hibrido:
            print(f"\n⚠️ Catálogo híbrido ({len(r.catalogo_hibrido)}):")
            for cat in r.catalogo_hibrido[:3]:
                print(f"   - {cat}")

        if r.jobs_nao_documentados:
            print(f"\n⚠️ Jobs background sem UC ({len(r.jobs_nao_documentados)}):")
            for job in r.jobs_nao_documentados:
                print(f"   - {job}")

        if r.workflows_nao_documentados:
            print(f"\n⚠️ Workflows sem UC ({len(r.workflows_nao_documentados)}):")
            for wf in r.workflows_nao_documentados:
                print(f"   - {wf}")

        if r.integracoes_nao_documentadas:
            print(f"\n⚠️ Integrações sem UC ({len(r.integracoes_nao_documentadas)}):")
            for integ in r.integracoes_nao_documentadas:
                print(f"   - {integ}")

    def _auto_correct(self):
        """CORREÇÃO AUTOMÁTICA de todos os problemas"""

        # 1. Migrar nomenclatura
        if self.audit_result.problemas_nomenclatura:
            print(f"   [1/5] Migrando nomenclatura...")
            self._fix_nomenclatura()

        # 2. Limpar catálogo híbrido
        if self.audit_result.catalogo_hibrido:
            print(f"   [2/5] Limpando catálogo híbrido...")
            self._fix_catalogo_hibrido()

        # 3. Criar UCs para gaps
        if self.audit_result.gaps:
            print(f"   [3/5] Criando {len(self.audit_result.gaps)} UCs faltantes...")
            self._create_missing_ucs()

        # 4. Documentar jobs/workflows/integrações
        print(f"   [4/5] Documentando funcionalidades especiais...")
        self._document_special_features()

        # 5. Salvar UC.yaml corrigido
        print(f"   [5/5] Salvando UC.yaml corrigido...")
        self._save_uc()

    def _fix_nomenclatura(self):
        """Migra nomenclatura para padrão oficial"""
        documentacao_num = self.rf_data['rf']['id']  # ex: RF023

        # Padrões não-padrão conhecidos
        migrations = {
            r'RN-CTR-(\d{3})-(\d{2})': f'RN-{rf_num}-\\2',
            r'RN-DEP-(\d{3})-(\d{2})': f'RN-{rf_num}-\\2',
            r'RN-FIN-(\d{3})-(\d{2})': f'RN-{rf_num}-\\2',
        }

        for uc in self.uc_data.get('casos_uso', []):
            # Migrar regras_aplicadas
            if 'regras_aplicadas' in uc:
                uc['regras_aplicadas'] = [
                    self._migrate_rn_id(rn, migrations) for rn in uc['regras_aplicadas']
                ]

            # Migrar covers.rf_items
            if 'covers' in uc and 'rf_items' in uc['covers']:
                uc['covers']['rf_items'] = [
                    self._migrate_rn_id(item, migrations) for item in uc['covers']['rf_items']
                ]

    def _migrate_rn_id(self, rn_id: str, migrations: Dict[str, str]) -> str:
        """Aplica migração de nomenclatura"""
        for pattern, replacement in migrations.items():
            rn_id = re.sub(pattern, replacement, rn_id)
        return rn_id

    def _fix_catalogo_hibrido(self):
        """Remove códigos de catálogo (RF-CRUD-XX) de covers.rf_items"""
        catalog_pattern = re.compile(r'RF\d{3}-(CRUD|VAL|SEC)-\d{2}')

        for uc in self.uc_data.get('casos_uso', []):
            if 'covers' in uc and 'rf_items' in uc['covers']:
                uc['covers']['rf_items'] = [
                    item for item in uc['covers']['rf_items']
                    if not catalog_pattern.match(item)
                ]

    def _create_missing_ucs(self):
        """Cria UCs para RNs não cobertas"""
        for gap_rn_id in self.audit_result.gaps:
            # Encontrar dados da RN no RF
            rn_data = self._find_rn_in_rf(gap_rn_id)
            if not rn_data:
                continue

            # Gerar UC baseado em template
            new_uc = self._generate_uc_from_rn(gap_rn_id, rn_data)

            # Adicionar aos casos_uso
            if 'casos_uso' not in self.uc_data:
                self.uc_data['casos_uso'] = []

            self.uc_data['casos_uso'].append(new_uc)

    def _find_rn_in_rf(self, rn_id: str) -> dict:
        """Encontra dados da RN no RF.yaml"""
        for regra in self.rf_data.get('regras_negocio', []):
            if regra.get('id') == rn_id:
                return regra
        return None

    def _generate_uc_from_rn(self, rn_id: str, rn_data: dict) -> dict:
        """Gera UC baseado em template a partir de RN"""
        # Extrair número do UC
        uc_num = len(self.uc_data.get('casos_uso', [])) + 1
        uc_id = f"UC{uc_num:02d}-{self.rf_data['rf']['id']}"

        # Template básico
        uc = {
            'id': uc_id,
            'titulo': rn_data.get('titulo', rn_data.get('descricao', 'Caso de Uso'))[:100],
            'ator_principal': self._infer_ator(rn_data),
            'objetivo': rn_data.get('descricao', ''),
            'preconditions': [
                'Usuário autenticado',
                f"Permissão: {self._infer_permission(rn_id)}"
            ],
            'fluxo_principal': {
                'FP': [
                    {
                        'passo': 'FP-01',
                        'acao': 'Usuário executa ação',
                        'sistema': rn_data.get('descricao', '')
                    }
                ]
            },
            'fluxos_excecao': {},
            'regras_aplicadas': [rn_id],
            'covers': {
                'rf_items': [rn_id]
            },
            'pos_conditions': ['Operação concluída com sucesso'],
            'criterios_aceite': rn_data.get('criterios_aceite', [])
        }

        # Se é validação, adicionar fluxo de exceção
        if rn_data.get('tipo') == 'validacao' or rn_data.get('validacao'):
            http_code = rn_data.get('validacao', {}).get('http_code', 400)
            msg_erro = rn_data.get('validacao', {}).get('mensagem_erro', 'Erro de validação')

            uc['fluxos_excecao']['FE-01'] = {
                'condicao': 'Payload inválido',
                'passos': [
                    {
                        'passo': 'FE-01-01',
                        'acao': 'Usuário envia dados inválidos',
                        'sistema': f'HTTP {http_code} - {msg_erro}'
                    }
                ]
            }

        return uc

    def _infer_ator(self, rn_data: dict) -> str:
        """Infere ator principal baseado na RN"""
        tipo = rn_data.get('tipo', '').lower()

        if 'job' in tipo or 'background' in tipo:
            return 'Sistema (Hangfire Scheduler)'
        elif 'integracao' in tipo:
            return 'Sistema (API Integration)'
        else:
            return self.rf_data.get('descricao', {}).get('publico_afetado', 'Usuário').split(',')[0].strip()

    def _infer_permission(self, rn_id: str) -> str:
        """Infere código de permissão baseado no RF"""
        documentacao_id_lower = self.rf_data['rf']['id'].lower()
        return f"{rf_id_lower}:read"

    def _document_special_features(self):
        """Documenta jobs, workflows, integrações com UCs especializados"""
        # Jobs
        for job_rn in self.audit_result.jobs_nao_documentados:
            rn_data = self._find_rn_in_rf(job_rn)
            if rn_data:
                uc_job = self._generate_job_uc(job_rn, rn_data)
                self.uc_data.get('casos_uso', []).append(uc_job)

        # Workflows
        for wf_rn in self.audit_result.workflows_nao_documentados:
            rn_data = self._find_rn_in_rf(wf_rn)
            if rn_data:
                uc_wf = self._generate_workflow_uc(wf_rn, rn_data)
                self.uc_data.get('casos_uso', []).append(uc_wf)

        # Integrações
        for integ_rn in self.audit_result.integracoes_nao_documentadas:
            rn_data = self._find_rn_in_rf(integ_rn)
            if rn_data:
                uc_integ = self._generate_integration_uc(integ_rn, rn_data)
                self.uc_data.get('casos_uso', []).append(uc_integ)

    def _generate_job_uc(self, rn_id: str, rn_data: dict) -> dict:
        """Gera UC especializado para job background"""
        uc_num = len(self.uc_data.get('casos_uso', [])) + 1
        uc_id = f"UC{uc_num:02d}-{self.rf_data['rf']['id']}"

        return {
            'id': uc_id,
            'titulo': f"Job Background - {rn_data.get('titulo', 'Job')}",
            'ator_principal': 'Sistema (Hangfire Scheduler)',
            'objetivo': rn_data.get('descricao', ''),
            'tipo': 'background_job',
            'fluxo_principal': {
                'FP': [
                    {
                        'passo': 'FP-01',
                        'acao': 'Job dispara conforme CRON',
                        'sistema': 'BackgroundJob.Enqueue()'
                    },
                    {
                        'passo': 'FP-02',
                        'sistema': rn_data.get('descricao', '')
                    }
                ]
            },
            'regras_aplicadas': [rn_id],
            'covers': {'rf_items': [rn_id]},
            'configuracao_job': {
                'expressao_cron': '0 0 * * *',
                'timezone': 'UTC'
            }
        }

    def _generate_workflow_uc(self, rn_id: str, rn_data: dict) -> dict:
        """Gera UC especializado para workflow"""
        uc_num = len(self.uc_data.get('casos_uso', [])) + 1
        uc_id = f"UC{uc_num:02d}-{self.rf_data['rf']['id']}"

        return {
            'id': uc_id,
            'titulo': f"Workflow - {rn_data.get('titulo', 'Workflow')}",
            'ator_principal': 'Usuário',
            'objetivo': rn_data.get('descricao', ''),
            'tipo': 'workflow',
            'state_machine': {
                'estados': [],
                'transicoes_permitidas': []
            },
            'fluxo_principal': {
                'FP': [
                    {
                        'passo': 'FP-01',
                        'acao': 'Usuário inicia workflow',
                        'sistema': rn_data.get('descricao', '')
                    }
                ]
            },
            'regras_aplicadas': [rn_id],
            'covers': {'rf_items': [rn_id]}
        }

    def _generate_integration_uc(self, rn_id: str, rn_data: dict) -> dict:
        """Gera UC especializado para integração externa"""
        uc_num = len(self.uc_data.get('casos_uso', [])) + 1
        uc_id = f"UC{uc_num:02d}-{self.rf_data['rf']['id']}"

        return {
            'id': uc_id,
            'titulo': f"Integração - {rn_data.get('titulo', 'Sistema Externo')}",
            'ator_principal': 'Sistema (API)',
            'objetivo': rn_data.get('descricao', ''),
            'tipo': 'integracao_externa',
            'sistema_externo': {
                'nome': 'Sistema Externo',
                'tipo': 'REST API'
            },
            'fluxo_principal': {
                'FP': [
                    {
                        'passo': 'FP-01',
                        'acao': 'Sistema autentica',
                        'sistema': 'OAuth2 ou API Key'
                    },
                    {
                        'passo': 'FP-02',
                        'sistema': rn_data.get('descricao', '')
                    }
                ]
            },
            'regras_aplicadas': [rn_id],
            'covers': {'rf_items': [rn_id]}
        }

    def _save_uc(self):
        """Salva UC.yaml corrigido"""
        with open(self.uc_path, 'w', encoding='utf-8') as f:
            yaml.dump(self.uc_data, f, allow_unicode=True, sort_keys=False, default_flow_style=False)

    def _validate(self) -> bool:
        """Valida UC corrigido (simula validator-rf-uc.py)"""
        # Re-auditar após correções
        self.audit_result = self._audit()

        # Critérios de aprovação
        ok = (
            self.audit_result.cobertura_pct == 100 and
            len(self.audit_result.problemas_nomenclatura) == 0 and
            len(self.audit_result.catalogo_hibrido) == 0
        )

        return ok


def main():
    """Execução em lote ou individual"""
    import argparse

    parser = argparse.ArgumentParser(description='Auditoria e Correção Automática de UCs')
    parser.add_argument('--rf', required=True, help='Path para RF.yaml')
    parser.add_argument('--uc', required=True, help='Path para UC.yaml')
    parser.add_argument('--auto-correct', action='store_true', help='Corrigir automaticamente')

    args = parser.parse_args()

    documentacao_path = Path(args.rf)
    uc_path = Path(args.uc)

    if not documentacao_path.exists():
        print(f"❌ RF não encontrado: {rf_path}")
        sys.exit(1)

    if not uc_path.exists():
        print(f"❌ UC não encontrado: {uc_path}")
        sys.exit(1)

    engine = UCAdequacaoEngine(rf_path, uc_path)
    result = engine.run()

    # Exit code baseado em severidade
    if result.severidade == "CONFORME":
        sys.exit(0)
    elif result.severidade in ["BAIXO", "MEDIO"]:
        sys.exit(1)
    else:  # ALTO, CRITICO
        sys.exit(2)


if __name__ == '__main__':
    main()
