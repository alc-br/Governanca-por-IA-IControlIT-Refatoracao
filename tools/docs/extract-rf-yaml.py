#!/usr/bin/env python3
"""
extract-rf-yaml.py - Extrator RF.md  RF.yaml

Lê RFXXX.md e gera RFXXX.yaml estruturado conforme template RF.yaml.

Extrai:
- Metadados do RF (id, nome, fase, epic)
- Descrição (objetivo, problema, público)
- Escopo (incluso/fora)
- Entidades principais
- Regras de negócio (RN-XXX-NN)
- Estados e transições
- Permissões
- Integrações
- UCs esperados

Uso:
    python extract-rf-yaml.py RFXXX
    python extract-rf-yaml.py --fase 1
    python extract-rf-yaml.py --all

Autor: Agência ALC - alc.dev.br
Versão: 1.0
Data: 2025-12-29
"""

import sys
import os
import re
import yaml
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


class ExtractorRFYaml:
    """Extrator de RF.md para RF.yaml"""

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

    def extrair_metadados(self, content: str, rf_id: str, rf_path: Path) -> Dict:
        """Extrai metadados básicos do RF"""
        # Tentar extrair título da primeira linha (# RF-XXX  Título)
        title_match = re.search(r'^#\s+' + re.escape(rf_id) + r'\s+[-]\s+(.+)$', content, re.MULTILINE)
        nome = title_match.group(1).strip() if title_match else "Sem título"

        # Extrair fase e epic do caminho
        fase = rf_path.parent.parent.name  # Fase-X-Nome
        epic = rf_path.parent.name  # EPIC-XXX-YYY

        # Extrair versão e data se existir seção "Histórico de Versões"
        versao = "1.0"
        data = datetime.now().strftime("%Y-%m-%d")

        hist_match = re.search(r'##\s+(?:Histórico de Versões|Changelog|CHANGELOG)(.*?)(?=\n##|\Z)', content, re.DOTALL | re.IGNORECASE)
        if hist_match:
            hist_content = hist_match.group(1)
            # Procurar primeira linha da tabela
            primeira_linha = re.search(r'\|\s*(\d+\.\d+)\s*\|\s*(\d{4}-\d{2}-\d{2})', hist_content)
            if primeira_linha:
                versao = primeira_linha.group(1)
                data = primeira_linha.group(2)

        return {
            "id": rf_id,
            "nome": nome,
            "versao": versao,
            "data": data,
            "fase": fase,
            "epic": epic,
            "status": "draft"  # Status padrão
        }

    def extrair_descricao(self, content: str) -> Dict:
        """Extrai seção de descrição/objetivo"""
        descricao = {
            "objetivo": "",
            "problema_resolvido": "",
            "publico_afetado": ""
        }

        # Procurar seção "Visão Geral" ou "Objetivo"
        visao_match = re.search(r'##\s+(?:1\.\s+)?Visão Geral(.*?)(?=\n##|\Z)', content, re.DOTALL | re.IGNORECASE)
        if visao_match:
            visao_content = visao_match.group(1).strip()

            # Extrair objetivo
            obj_match = re.search(r'\*\*Objetivo:\*\*\s+(.+?)(?=\n\n|\*\*|\Z)', visao_content, re.DOTALL)
            if obj_match:
                descricao["objetivo"] = obj_match.group(1).strip()

            # Extrair problema
            prob_match = re.search(r'\*\*Problema:\*\*\s+(.+?)(?=\n\n|\*\*|\Z)', visao_content, re.DOTALL)
            if prob_match:
                descricao["problema_resolvido"] = prob_match.group(1).strip()

            # Extrair público
            pub_match = re.search(r'\*\*Público:\*\*\s+(.+?)(?=\n\n|\*\*|\Z)', visao_content, re.DOTALL)
            if pub_match:
                descricao["publico_afetado"] = pub_match.group(1).strip()

        return descricao

    def extrair_escopo(self, content: str) -> Dict:
        """Extrai escopo (incluso/fora)"""
        escopo = {
            "incluso": [],
            "fora": []
        }

        # Procurar seção "Escopo"
        escopo_match = re.search(r'###\s+Escopo(.*?)(?=\n###|\n##|\Z)', content, re.DOTALL | re.IGNORECASE)
        if escopo_match:
            escopo_content = escopo_match.group(1)

            # Extrair incluso
            inc_match = re.search(r'\*\*Incluso:\*\*(.*?)(?=\*\*|###|\Z)', escopo_content, re.DOTALL)
            if inc_match:
                itens = re.findall(r'[-]\s+(.+)', inc_match.group(1))
                escopo["incluso"] = [item.strip() for item in itens]

            # Extrair fora
            fora_match = re.search(r'\*\*Fora do Escopo:\*\*(.*?)(?=\*\*|###|\Z)', escopo_content, re.DOTALL)
            if fora_match:
                itens = re.findall(r'[-]\s+(.+)', fora_match.group(1))
                escopo["fora"] = [item.strip() for item in itens]

        return escopo

    def extrair_regras_negocio(self, content: str) -> List[Dict]:
        """Extrai regras de negócio (RN-XXX-NN)"""
        regras = []

        # Procurar seção "Regras de Negócio" ou "Funcionalidades"
        rn_match = re.search(r'##\s+(?:\d+\.\s+)?(?:Regras de Negócio|Funcionalidades)(.*?)(?=\n##|\Z)', content, re.DOTALL | re.IGNORECASE)
        if not rn_match:
            return regras

        rn_content = rn_match.group(1)

        # Padrão: ### RN-XXX-01: Título
        regras_encontradas = re.finditer(r'###\s+(RN-[A-Z]+-\d+-\d+):\s+(.+?)$(.*?)(?=\n###|\n##|\Z)', rn_content, re.MULTILINE | re.DOTALL)

        for match in regras_encontradas:
            rn_id = match.group(1)
            titulo = match.group(2).strip()
            corpo = match.group(3).strip()

            # Extrair descrição (primeiro parágrafo ou lista)
            desc_match = re.search(r'^(.+?)(?=\n\n|\*\*|\Z)', corpo, re.DOTALL)
            descricao = desc_match.group(1).strip() if desc_match else titulo

            # Tentar identificar tipo
            tipo = "regra_negocio"
            if any(keyword in descricao.lower() for keyword in ['validar', 'validação', 'obrigatório']):
                tipo = "validacao"
            elif any(keyword in descricao.lower() for keyword in ['único', 'unicidade', 'duplicado']):
                tipo = "unicidade"
            elif any(keyword in descricao.lower() for keyword in ['permissão', 'autorização', 'acesso']):
                tipo = "seguranca"

            regras.append({
                "id": rn_id,
                "descricao": descricao,
                "tipo": tipo,
                "campos_afetados": [],  # Difícil extrair automaticamente
                "obrigatorio": True
            })

        return regras

    def extrair_entidades(self, content: str, rf_id: str) -> List[Dict]:
        """Extrai entidades principais (da seção MD ou nome do RF)"""
        entidades = []

        # Tentar extrair nome da entidade do título do RF
        # Ex: "RF-008  Gestão de Empresas"  entidade = "empresa"
        title_match = re.search(r'^#\s+' + re.escape(rf_id) + r'\s+[-]\s+(?:Gestão de|Gerenciamento de)?\s*(.+?)(?:s)?$', content, re.MULTILINE | re.IGNORECASE)
        if title_match:
            nome_singular = title_match.group(1).strip().lower()
            # Remover plural
            if nome_singular.endswith('s'):
                nome_singular = nome_singular[:-1]

            entidades.append({
                "nome": nome_singular,
                "descricao": f"Entidade principal do {rf_id}",
                "multi_tenant": True,
                "soft_delete": True,
                "auditoria": True
            })

        return entidades

    def extrair_permissoes(self, content: str, entidade_nome: str = "entidade") -> List[Dict]:
        """Extrai ou gera permissões padrão CRUD"""
        permissoes_padrao = [
            {"codigo": f"{entidade_nome}.view_any", "descricao": "Listar registros"},
            {"codigo": f"{entidade_nome}.view", "descricao": "Visualizar registro"},
            {"codigo": f"{entidade_nome}.create", "descricao": "Criar registro"},
            {"codigo": f"{entidade_nome}.update", "descricao": "Atualizar registro"},
            {"codigo": f"{entidade_nome}.delete", "descricao": "Excluir registro"},
        ]

        # Procurar seção "Permissões" ou "Central de Funcionalidades"
        perm_match = re.search(r'##\s+(?:\d+\.\s+)?(?:Permissões|Central de Funcionalidades)(.*?)(?=\n##|\Z)', content, re.DOTALL | re.IGNORECASE)
        if perm_match:
            perm_content = perm_match.group(1)

            # Se encontrar tabela de permissões, usar ela
            # Formato: | CAD.EMPRESAS.VIEW | Visualizar empresa |
            perm_encontradas = re.findall(r'\|\s*([A-Z_\.]+)\s*\|\s*(.+?)\s*\|', perm_content)
            if perm_encontradas:
                return [{"codigo": codigo.strip(), "descricao": desc.strip()} for codigo, desc in perm_encontradas]

        return permissoes_padrao

    def extrair_ucs_esperados(self, content: str) -> List[str]:
        """Extrai UCs esperados ou gera lista padrão UC00-UC04"""
        ucs = []

        # Procurar seção "Casos de Uso"
        uc_match = re.search(r'##\s+(?:\d+\.\s+)?Casos de Uso(.*?)(?=\n##|\Z)', content, re.DOTALL | re.IGNORECASE)
        if uc_match:
            uc_content = uc_match.group(1)

            # Padrão: ### UC00 - Título
            uc_encontrados = re.findall(r'###\s+(UC\d{2})', uc_content)
            if uc_encontrados:
                return sorted(set(uc_encontrados))

        # Lista padrão
        return ["UC00", "UC01", "UC02", "UC03", "UC04"]

    def gerar_rf_yaml(self, rf_id: str) -> Dict:
        """Gera estrutura YAML completa do RF"""
        rf_path = self.encontrar_rf(rf_id)
        rf_md = rf_path / f"{rf_id}.md"

        if not rf_md.exists():
            raise FileNotFoundError(f"Arquivo {rf_md} não encontrado")

        content = rf_md.read_text(encoding='utf-8')

        # Extrair todas as seções
        metadados = self.extrair_metadados(content, rf_id, rf_path)
        descricao = self.extrair_descricao(content)
        escopo = self.extrair_escopo(content)
        entidades = self.extrair_entidades(content, rf_id)
        regras = self.extrair_regras_negocio(content)
        ucs = self.extrair_ucs_esperados(content)

        # Nome da entidade para permissões
        entidade_nome = entidades[0]["nome"] if entidades else "entidade"
        permissoes = self.extrair_permissoes(content, entidade_nome)

        # Montar estrutura YAML
        rf_yaml = {
            "rf": metadados,
            "descricao": descricao,
            "escopo": escopo,
            "entidades": entidades,
            "regras_negocio": regras,
            "estados": [
                {"id": "pending", "descricao": "Criado, aguardando processamento"},
                {"id": "active", "descricao": "Ativo"},
                {"id": "inactive", "descricao": "Inativo"},
                {"id": "cancelled", "descricao": "Cancelado"}
            ],
            "transicoes": {
                "permitidas": [
                    {"de": "pending", "para": "active"},
                    {"de": "active", "para": "inactive"}
                ],
                "proibidas": [
                    {"de": "cancelled", "para": "active"}
                ]
            },
            "permissoes": permissoes,
            "integracoes": {
                "internas": ["Autenticacao", "Multi-Tenancy", "Auditoria"],
                "externas": []
            },
            "seguranca": {
                "isolamento_tenant": True,
                "auditoria_obrigatoria": True,
                "soft_delete": True
            },
            "rastreabilidade": {
                "ucs_esperados": ucs
            },
            "catalog": {
                "crud": [
                    {"id": "RF-CRUD-01", "title": "Criar registro", "required": True},
                    {"id": "RF-CRUD-02", "title": "Listar registros", "required": True},
                    {"id": "RF-CRUD-03", "title": "Visualizar registro", "required": True},
                    {"id": "RF-CRUD-04", "title": "Atualizar registro", "required": True},
                    {"id": "RF-CRUD-05", "title": "Excluir registro", "required": True}
                ],
                "validacoes": [
                    {"id": "RF-VAL-01", "title": "Validar campos obrigatórios", "required": True},
                    {"id": "RF-VAL-02", "title": "Validar unicidade", "required": False}
                ],
                "seguranca": [
                    {"id": "RF-SEC-01", "title": "Isolamento de tenant", "required": True},
                    {"id": "RF-SEC-02", "title": "Permissões RBAC", "required": True}
                ]
            },
            "exclusions": {
                "rf_items": []
            },
            "historico": [
                {
                    "versao": metadados["versao"],
                    "data": metadados["data"],
                    "autor": "Agência ALC - alc.dev.br",
                    "descricao": "Versão inicial"
                }
            ]
        }

        return rf_yaml

    def salvar_yaml(self, rf_id: str, data: Dict, output_path: Path = None):
        """Salva YAML em arquivo"""
        if output_path is None:
            rf_path = self.encontrar_rf(rf_id)
            output_path = rf_path / f"{rf_id}.yaml"

        # Criar comentário de cabeçalho
        header = f"""# =============================================
# {rf_id} - Requisito Funcional (Contrato Canônico)
# Gerado automaticamente de {rf_id}.md
# Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# Autor padrão: Agência ALC - alc.dev.br
# =============================================

"""

        # Gerar YAML
        yaml_content = yaml.dump(data, allow_unicode=True, default_flow_style=False, sort_keys=False, indent=2)

        # Salvar
        output_path.write_text(header + yaml_content, encoding='utf-8')
        print(f" {output_path.name} criado com sucesso")

    def extrair_rf(self, rf_id: str) -> bool:
        """Extrai um RF completo"""
        try:
            print(f"Extraindo {rf_id}.md  {rf_id}.yaml...")
            data = self.gerar_rf_yaml(rf_id)
            self.salvar_yaml(rf_id, data)
            return True
        except Exception as e:
            print(f" Erro ao extrair {rf_id}: {str(e)}")
            return False

    def extrair_fase(self, fase_num: int) -> int:
        """Extrai todos os RFs de uma fase"""
        fase_dir = self.base_path / f"Fase-{fase_num}"

        if not fase_dir.exists():
            print(f" Fase {fase_num} não encontrada")
            return 0

        sucesso = 0

        for epic_dir in sorted(fase_dir.glob("EPIC-*")):
            for rf_dir in sorted(epic_dir.glob("RF*")):
                rf_id = rf_dir.name.split('-')[0]
                if self.extrair_rf(rf_id):
                    sucesso += 1

        return sucesso

    def extrair_todos(self) -> int:
        """Extrai todos os RFs do projeto"""
        sucesso = 0

        for fase_dir in sorted(self.base_path.glob("Fase-*")):
            fase_match = re.match(r'Fase-(\d+)', fase_dir.name)
            if fase_match:
                fase_num = int(fase_match.group(1))
                print(f"\n{'='*60}")
                print(f"FASE {fase_num}: {fase_dir.name}")
                print('='*60)
                sucesso += self.extrair_fase(fase_num)

        return sucesso


def main():
    if len(sys.argv) < 2:
        print("Uso:")
        print("  python extract-rf-yaml.py RFXXX")
        print("  python extract-rf-yaml.py --fase N")
        print("  python extract-rf-yaml.py --all")
        sys.exit(1)

    extractor = ExtractorRFYaml()
    arg = sys.argv[1]

    if arg == '--all':
        print("Extraindo TODOS os RFs do projeto...")
        total = extractor.extrair_todos()
        print(f"\n {total} arquivos RF.yaml gerados com sucesso")

    elif arg == '--fase':
        if len(sys.argv) < 3:
            print(" Especifique o número da fase: --fase N")
            sys.exit(1)

        fase_num = int(sys.argv[2])
        print(f"Extraindo RFs da Fase {fase_num}...")
        total = extractor.extrair_fase(fase_num)
        print(f"\n {total} arquivos RF.yaml gerados com sucesso")

    else:
        rf_id = arg
        if extractor.extrair_rf(rf_id):
            print("\n Extração concluída!")
        else:
            sys.exit(1)


if __name__ == '__main__':
    main()
