#!/usr/bin/env python3
"""
validator-docs.py - Validador Universal de Documentação

Valida TODOS os arquivos de documentação contra templates oficiais:
- RF*.md, RF*.yaml
- RL-RF*.md, RL-RF*.yaml
- UC-RF*.md, UC-RF*.yaml
- MD-RF*.yaml
- WF-RF*.md
- MT-RF*.yaml
- TC-RF*.yaml
- STATUS.yaml

Características:
1. Descobre estrutura dos templates automaticamente
2. Adapta-se a mudanças nos templates (novas seções, campos)
3. Identifica arquivos duplicados (.backup, etc)
4. Valida estrutura YAML e Markdown
5. Gera JSON detalhado para análise

Uso:
    python validator-docs.py --all                    # Todos os RFs
    python validator-docs.py --fase 1                 # RFs da Fase 1
    python validator-docs.py RF001                    # RF específico
    python validator-docs.py --output report.json     # JSON customizado

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
from typing import Dict, List, Tuple, Any, Set
from dataclasses import dataclass, asdict, field
from datetime import datetime
from collections import defaultdict

# CRITICAL FIX: Force UTF-8 encoding on Windows (Git Bash issue)
# Without this, Windows reads UTF-8 files as cp1252, causing "Versão" → "Vers�o"
os.environ['PYTHONIOENCODING'] = 'utf-8'
if sys.platform == 'win32':
    # Force UTF-8 for stdin, stdout, stderr
    sys.stdin.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')


# =====================================================
# ESTRUTURAS DE DADOS
# =====================================================

@dataclass
class TemplateStructure:
    """Estrutura descoberta de um template"""
    tipo: str  # md ou yaml
    secoes_md: List[str] = field(default_factory=list)  # ["## 1. OBJETIVO", "## 2. ESCOPO"]
    campos_yaml: Dict[str, Any] = field(default_factory=dict)  # {"rf": {"id": str, ...}}
    campos_obrigatorios: List[str] = field(default_factory=list)

    def to_dict(self):
        return asdict(self)


@dataclass
class FileValidation:
    """Resultado da validação de um arquivo"""
    arquivo: str
    existe: bool
    tipo: str  # md, yaml
    valido: bool
    estrutura_conforme: bool
    gaps: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self):
        return asdict(self)


@dataclass
class RFValidationResult:
    """Resultado completo da validação de um RF"""
    documentacao_id: str
    pasta: str
    arquivos_esperados: Dict[str, FileValidation] = field(default_factory=dict)
    arquivos_duplicados: List[str] = field(default_factory=list)
    arquivos_extra: List[str] = field(default_factory=list)
    conforme: bool = False
    total_gaps: int = 0

    def to_dict(self):
        return {
            "rf_id": self.documentacao_id,
            "pasta": self.pasta,
            "arquivos_esperados": {k: v.to_dict() for k, v in self.arquivos_esperados.items()},
            "arquivos_duplicados": self.arquivos_duplicados,
            "arquivos_extra": self.arquivos_extra,
            "conforme": self.conforme,
            "total_gaps": self.total_gaps
        }


# =====================================================
# ANALISADOR DE TEMPLATES
# =====================================================

class TemplateAnalyzer:
    """Analisa templates e descobre estrutura automaticamente"""

    def __init__(self, templates_path: str = "D:\\IC2\\docs\\templates"):
        self.templates_path = Path(templates_path)
        self.templates: Dict[str, TemplateStructure] = {}
        self._descobrir_templates()

    def _descobrir_templates(self):
        """Descobre todos os templates disponíveis"""
        # Templates Markdown
        for md_file in self.templates_path.glob("*.md"):
            nome = md_file.stem  # RF, RL, UC, WF
            self.templates[nome] = self._analisar_template_md(md_file)

        # Templates YAML
        for yaml_file in self.templates_path.glob("*.yaml"):
            nome = yaml_file.stem  # RF, RL, UC, MD, TC, MT, STATUS
            self.templates[nome] = self._analisar_template_yaml(yaml_file)

    def _analisar_template_md(self, filepath: Path) -> TemplateStructure:
        """Analisa estrutura de um template Markdown"""
        content = filepath.read_text(encoding='utf-8')

        # Descobrir seções (## Título)
        secoes = re.findall(r'^##\s+(.+)$', content, re.MULTILINE)

        # Descobrir campos obrigatórios (marcados com ✅, obrigatório, required, etc)
        campos_obrigatorios = []
        for line in content.split('\n'):
            if any(marker in line.lower() for marker in ['obrigatório', 'required', '✅']):
                # Extrair nome do campo/seção
                match = re.search(r'[*_`]?([A-Za-z0-9_]+)[*_`]?', line)
                if match:
                    campos_obrigatorios.append(match.group(1))

        return TemplateStructure(
            tipo='md',
            secoes_md=secoes,
            campos_obrigatorios=list(set(campos_obrigatorios))
        )

    def _analisar_template_yaml(self, filepath: Path) -> TemplateStructure:
        """Analisa estrutura de um template YAML"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f) or {}
        except Exception as e:
            return TemplateStructure(tipo='yaml')

        # Descobrir campos de primeiro nível
        campos_obrigatorios = self._extrair_campos_obrigatorios(data)

        return TemplateStructure(
            tipo='yaml',
            campos_yaml=data,
            campos_obrigatorios=campos_obrigatorios
        )

    def _extrair_campos_obrigatorios(self, data: Dict, prefix: str = "") -> List[str]:
        """Extrai campos obrigatórios recursivamente"""
        campos = []

        if isinstance(data, dict):
            for key, value in data.items():
                campo_path = f"{prefix}.{key}" if prefix else key

                # Considerar campos de primeiro e segundo nível como obrigatórios
                if not prefix or prefix.count('.') < 1:
                    campos.append(campo_path)

                # Recursão
                if isinstance(value, dict):
                    campos.extend(self._extrair_campos_obrigatorios(value, campo_path))

        return campos

    def get_template(self, nome: str) -> TemplateStructure:
        """Retorna estrutura de um template"""
        return self.templates.get(nome)


# =====================================================
# VALIDADOR DE ARQUIVOS
# =====================================================

class FileValidator:
    """Valida arquivos individuais contra templates"""

    def __init__(self, template_analyzer: TemplateAnalyzer):
        self.analyzer = template_analyzer

    def validar_md(self, filepath: Path, template_name: str) -> FileValidation:
        """Valida arquivo Markdown contra template"""
        if not filepath.exists():
            return FileValidation(
                arquivo=filepath.name,
                existe=False,
                tipo='md',
                valido=False,
                estrutura_conforme=False,
                gaps=[{
                    "tipo": "CRÍTICO",
                    "mensagem": f"Arquivo {filepath.name} não encontrado",
                    "template_original": f"Arquivo {filepath.name} deve existir",
                    "documento_analisado": "Arquivo não existe",
                    "acao_necessaria": f"Criar arquivo {filepath.name} seguindo template em docs/templates/{template_name}.md"
                }]
            )

        template = self.analyzer.get_template(template_name)
        if not template:
            return FileValidation(
                arquivo=filepath.name,
                existe=True,
                tipo='md',
                valido=False,
                estrutura_conforme=False,
                gaps=[{
                    "tipo": "ERRO",
                    "mensagem": f"Template '{template_name}' não encontrado",
                    "template_original": "N/A",
                    "documento_analisado": "N/A",
                    "acao_necessaria": f"Verificar se template docs/templates/{template_name}.md existe"
                }]
            )

        content = filepath.read_text(encoding='utf-8')
        gaps = []

        # Validar seções obrigatórias
        secoes_encontradas = re.findall(r'^##\s+(.+)$', content, re.MULTILINE)
        secoes_encontradas_str = "\n".join([f"  - {s}" for s in secoes_encontradas]) if secoes_encontradas else "  (nenhuma seção ## encontrada)"

        for secao_esperada in template.secoes_md:
            # Normalizar para comparação (remover números, pontos)
            secao_norm = re.sub(r'^\d+\.\s*', '', secao_esperada).strip()
            encontrada = any(
                secao_norm.lower() in secao.lower()
                for secao in secoes_encontradas
            )

            if not encontrada:
                gaps.append({
                    "tipo": "IMPORTANTE",
                    "categoria": "estrutura_md",
                    "mensagem": f"Seção esperada não encontrada: '{secao_esperada}'",
                    "template_original": f"No template original está assim:\n{secao_esperada}\n(deve estar presente no documento)",
                    "documento_analisado": f"No documento analisado está assim:\nSeções encontradas:\n{secoes_encontradas_str}\n(falta esta seção)",
                    "acao_necessaria": f"Adicionar seção '{secao_esperada}' ao arquivo {filepath.name}, conforme template em docs/templates/{template_name}.md"
                })

        # Validar cabeçalho (versão, data, autor)
        # CRITICAL FIX: Markdown bold format is **Text:sao** (asterisks AFTER colon)
        # NOT **Text**:
        headers_patterns = [
            (r'\*\*Vers.o:\*\*', 'versão'),  # **Versão:**** (ão or �o or ao)
            (r'\*\*Data:\*\*', 'data'),      # **Data:****
            (r'\*\*Autor:\*\*', 'autor'),    # **Autor:****
            (r'\*\*Epic:\*\*', 'epic'),      # **Epic:****
            (r'\*\*Fase:\*\*', 'fase')       # **Fase:****
        ]

        for pattern_str, header_name in headers_patterns:
            pattern = re.compile(pattern_str, re.IGNORECASE)
            if not pattern.search(content):
                # CRITICAL FIX: Extrair cabeçalho ANTES da primeira marca --- (não entre marcas)
                # Template oficial tem metadados antes de ---, não entre ---...---
                cabecalho_match = re.search(r'^# .*?\n\n(.*?)^---', content, re.MULTILINE | re.DOTALL)
                cabecalho_atual = cabecalho_match.group(1).strip() if cabecalho_match else "(cabeçalho não encontrado ou mal formatado)"

                gaps.append({
                    "tipo": "MENOR",
                    "categoria": "metadados",
                    "mensagem": f"Metadado '{header_name}' não encontrado no cabeçalho",
                    "template_original": f"No template original está assim:\n**{header_name.title()}**: [valor]\n...\n---",
                    "documento_analisado": f"No documento analisado está assim:\n{cabecalho_atual}\n---\n(falta metadado '{header_name}')",
                    "acao_necessaria": f"Adicionar linha '**{header_name.title()}**: [valor adequado]' no cabeçalho do arquivo {filepath.name}, antes da primeira marca ---"
                })

        return FileValidation(
            arquivo=filepath.name,
            existe=True,
            tipo='md',
            valido=len(gaps) == 0,
            estrutura_conforme=all(g['tipo'] != 'CRÍTICO' for g in gaps),
            gaps=gaps
        )

    def validar_yaml(self, filepath: Path, template_name: str) -> FileValidation:
        """Valida arquivo YAML contra template"""
        if not filepath.exists():
            return FileValidation(
                arquivo=filepath.name,
                existe=False,
                tipo='yaml',
                valido=False,
                estrutura_conforme=False,
                gaps=[{
                    "tipo": "CRÍTICO",
                    "mensagem": f"Arquivo {filepath.name} não encontrado",
                    "template_original": f"Arquivo {filepath.name} deve existir",
                    "documento_analisado": "Arquivo não existe",
                    "acao_necessaria": f"Criar arquivo {filepath.name} seguindo template em docs/templates/{template_name}.yaml"
                }]
            )

        template = self.analyzer.get_template(template_name)
        if not template:
            return FileValidation(
                arquivo=filepath.name,
                existe=True,
                tipo='yaml',
                valido=False,
                estrutura_conforme=False,
                gaps=[{
                    "tipo": "ERRO",
                    "mensagem": f"Template '{template_name}' não encontrado",
                    "template_original": "N/A",
                    "documento_analisado": "N/A",
                    "acao_necessaria": f"Verificar se template docs/templates/{template_name}.yaml existe"
                }]
            )

        gaps = []

        # Validar YAML válido
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                raw_content = f.read()
                data = yaml.safe_load(raw_content)
        except yaml.YAMLError as e:
            # Extrair linha do erro se possível
            error_line = "desconhecida"
            if hasattr(e, 'problem_mark'):
                error_line = f"linha {e.problem_mark.line + 1}, coluna {e.problem_mark.column + 1}"

            return FileValidation(
                arquivo=filepath.name,
                existe=True,
                tipo='yaml',
                valido=False,
                estrutura_conforme=False,
                gaps=[{
                    "tipo": "CRÍTICO",
                    "categoria": "sintaxe_yaml",
                    "mensagem": f"YAML inválido: {str(e)}",
                    "template_original": "No template original está assim:\n(YAML válido, sem erros de sintaxe)",
                    "documento_analisado": f"No documento analisado está assim:\nErro de sintaxe YAML em {error_line}:\n{str(e)}",
                    "acao_necessaria": f"Corrigir sintaxe YAML no arquivo {filepath.name} em {error_line}. Verificar indentação, dois-pontos, aspas e estrutura YAML válida."
                }]
            )
        except Exception as e:
            return FileValidation(
                arquivo=filepath.name,
                existe=True,
                tipo='yaml',
                valido=False,
                estrutura_conforme=False,
                gaps=[{
                    "tipo": "CRÍTICO",
                    "categoria": "leitura_arquivo",
                    "mensagem": f"Erro ao ler arquivo: {str(e)}",
                    "template_original": "Arquivo deve ser legível com encoding UTF-8",
                    "documento_analisado": f"Erro ao ler arquivo: {str(e)}",
                    "acao_necessaria": f"Verificar encoding do arquivo {filepath.name} (deve ser UTF-8) e permissões de leitura"
                }]
            )

        # Validar campos obrigatórios
        for campo_path in template.campos_obrigatorios:
            if not self._campo_existe(data, campo_path):
                # Obter valor do template para este campo
                valor_template = self._obter_valor_campo(template.campos_yaml, campo_path)
                tipo_template = type(valor_template).__name__ if valor_template else "string"

                # Mostrar estrutura atual do documento
                partes = campo_path.split('.')
                contexto_atual = self._obter_contexto_campo(data, partes[:-1]) if len(partes) > 1 else data
                campos_atuais = list(contexto_atual.keys()) if isinstance(contexto_atual, dict) else []

                gaps.append({
                    "tipo": "IMPORTANTE",
                    "categoria": "campos_obrigatorios",
                    "mensagem": f"Campo obrigatório ausente: '{campo_path}'",
                    "template_original": f"No template original está assim:\n{campo_path}: {valor_template}\n(tipo esperado: {tipo_template})",
                    "documento_analisado": f"No documento analisado está assim:\nCampos presentes em '{'.'.join(partes[:-1]) if len(partes) > 1 else 'raiz'}': {campos_atuais}\n(campo '{partes[-1]}' não encontrado)",
                    "acao_necessaria": f"Adicionar campo '{campo_path}' ao arquivo {filepath.name} com valor apropriado (tipo: {tipo_template})"
                })

        # Validar estrutura similar ao template
        campos_template = set(self._listar_campos(template.campos_yaml))
        campos_arquivo = set(self._listar_campos(data))

        # Campos faltando
        faltando = campos_template - campos_arquivo
        for campo in faltando:
            # Ignorar campos de exemplo ou placeholders
            if not any(placeholder in campo.lower() for placeholder in ['xxx', 'example', 'placeholder']):
                valor_template = self._obter_valor_campo(template.campos_yaml, campo)

                gaps.append({
                    "tipo": "MENOR",
                    "categoria": "estrutura_yaml",
                    "mensagem": f"Campo do template não encontrado: '{campo}'",
                    "template_original": f"No template original está assim:\n{campo}: {valor_template}",
                    "documento_analisado": f"No documento analisado está assim:\n(campo '{campo}' não existe)",
                    "acao_necessaria": f"Adicionar campo '{campo}' ao arquivo {filepath.name} seguindo estrutura do template em docs/templates/{template_name}.yaml"
                })

        return FileValidation(
            arquivo=filepath.name,
            existe=True,
            tipo='yaml',
            valido=len([g for g in gaps if g['tipo'] == 'CRÍTICO']) == 0,
            estrutura_conforme=len(gaps) == 0,
            gaps=gaps
        )

    def _campo_existe(self, data: Dict, campo_path: str) -> bool:
        """Verifica se campo existe no YAML (suporta path como 'rf.id')"""
        parts = campo_path.split('.')
        current = data

        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return False

        return True

    def _listar_campos(self, data: Any, prefix: str = "") -> List[str]:
        """Lista todos os campos de um dicionário recursivamente"""
        campos = []

        if isinstance(data, dict):
            for key, value in data.items():
                campo_path = f"{prefix}.{key}" if prefix else key
                campos.append(campo_path)

                if isinstance(value, dict):
                    campos.extend(self._listar_campos(value, campo_path))

        return campos

    def _obter_valor_campo(self, data: Dict, campo_path: str) -> Any:
        """Obtém valor de um campo do template (suporta path como 'rf.id')"""
        parts = campo_path.split('.')
        current = data

        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return None

        return current

    def _obter_contexto_campo(self, data: Dict, path_parts: List[str]) -> Any:
        """Obtém contexto (dicionário pai) de um campo"""
        current = data

        for part in path_parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return {}

        return current


# =====================================================
# VALIDADOR COMPLETO DE RF
# =====================================================

class RFDocumentationValidator:
    """Valida documentação completa de um RF"""

    # Padrões de arquivos esperados por RF
    ARQUIVOS_ESPERADOS = {
        'RF.md': ('RF', 'md'),
        'RF.yaml': ('RF', 'yaml'),
        'RL-RF.md': ('RL', 'md'),
        'RL-RF.yaml': ('RL', 'yaml'),
        'UC-RF.md': ('UC', 'md'),
        'UC-RF.yaml': ('UC', 'yaml'),
        'MD-RF.yaml': ('MD', 'yaml'),
        'WF-RF.md': ('WF', 'md'),
        'TC-RF.yaml': ('TC', 'yaml'),
        'MT-RF.yaml': ('MT', 'yaml'),
        'STATUS.yaml': ('STATUS', 'yaml'),
    }

    # Padrões de arquivos duplicados/backup
    PADROES_DUPLICADOS = [
        r'\.backup',
        r'\.bak',
        r'-\d{8}',  # -20251231
        r'\.old',
        r'\.tmp',
        r'_copy',
        r' \(\d+\)',  # (1), (2)
    ]

    def __init__(self, base_path: str = "D:\\IC2\\docs\\rf"):
        self.base_path = Path(base_path)
        self.analyzer = TemplateAnalyzer()
        self.file_validator = FileValidator(self.analyzer)

    def encontrar_rf(self, documentacao_id: str) -> Path:
        """Encontra pasta de um RF"""
        for fase_dir in self.base_path.glob("Fase-*"):
            for epic_dir in fase_dir.glob("EPIC*"):
                for documentacao_dir in epic_dir.glob(f"{documentacao_id}*"):
                    if documentacao_dir.is_dir():
                        return documentacao_dir

        raise FileNotFoundError(f"RF {documentacao_id} não encontrado em {self.base_path}")

    def validar_rf(self, documentacao_id: str) -> RFValidationResult:
        """Valida documentação completa de um RF"""
        try:
            documentacao_path = self.encontrar_rf(documentacao_id)
        except FileNotFoundError as e:
            return RFValidationResult(
                documentacao_id=documentacao_id,
                pasta="NÃO ENCONTRADA",
                conforme=False,
                total_gaps=1
            )

        result = RFValidationResult(
            documentacao_id=documentacao_id,
            pasta=str(documentacao_path)
        )

        # Validar cada arquivo esperado
        for pattern, (template_name, tipo) in self.ARQUIVOS_ESPERADOS.items():
            # Substituir RF pelo RF real
            filename = pattern.replace('RF', documentacao_id)
            filepath = documentacao_path / filename

            if tipo == 'md':
                validation = self.file_validator.validar_md(filepath, template_name)
            else:
                validation = self.file_validator.validar_yaml(filepath, template_name)

            result.arquivos_esperados[filename] = validation
            result.total_gaps += len(validation.gaps)

        # Detectar arquivos duplicados
        result.arquivos_duplicados = self._detectar_duplicados(documentacao_path, documentacao_id)

        # Detectar arquivos extra (não esperados)
        result.arquivos_extra = self._detectar_arquivos_extra(documentacao_path, documentacao_id)

        # Determinar se está conforme
        result.conforme = (
            all(v.existe and v.valido for v in result.arquivos_esperados.values()) and
            len(result.arquivos_duplicados) == 0 and
            result.total_gaps == 0
        )

        return result

    def _detectar_duplicados(self, documentacao_path: Path, documentacao_id: str) -> List[str]:
        """Detecta arquivos duplicados/backup"""
        duplicados = []

        for arquivo in documentacao_path.glob("*"):
            if arquivo.is_file():
                nome = arquivo.name

                # Verificar padrões de duplicados
                for pattern in self.PADROES_DUPLICADOS:
                    if re.search(pattern, nome):
                        duplicados.append(nome)
                        break

        return duplicados

    def _detectar_arquivos_extra(self, documentacao_path: Path, documentacao_id: str) -> List[str]:
        """Detecta arquivos na raiz do RF que não são esperados"""
        esperados = {
            pattern.replace('RF', documentacao_id)
            for pattern in self.ARQUIVOS_ESPERADOS.keys()
        }
        esperados.add("README.md")  # README é permitido
        esperados.add("user-stories.yaml")  # User stories é permitido

        extras = []

        for arquivo in documentacao_path.glob("*"):
            if arquivo.is_file() and arquivo.name not in esperados:
                # Ignorar duplicados (já contabilizados)
                if not any(re.search(p, arquivo.name) for p in self.PADROES_DUPLICADOS):
                    extras.append(arquivo.name)

        return extras

    def validar_fase(self, fase_num: int) -> List[RFValidationResult]:
        """Valida todos os RFs de uma fase"""
        results = []

        # Buscar fase com diferentes padrões de nome
        fase_patterns = [
            f"Fase-{fase_num}-*",
            f"Fase-{fase_num}*",
            f"Fase{fase_num}-*"
        ]

        fase_dir = None
        for pattern in fase_patterns:
            matches = list(self.base_path.glob(pattern))
            if matches:
                fase_dir = matches[0]
                break

        if not fase_dir or not fase_dir.exists():
            return results

        for epic_dir in sorted(fase_dir.glob("EPIC*")):
            if not epic_dir.is_dir():
                continue

            for documentacao_dir in sorted(epic_dir.glob("RF*")):
                if documentacao_dir.is_dir():
                    # Extrair RF ID do nome da pasta
                    match = re.match(r'(RF\d+)', documentacao_dir.name)
                    if match:
                        documentacao_id = match.group(1)
                        print(f"Validando {documentacao_id}...")
                        result = self.validar_rf(documentacao_id)
                        results.append(result)

        return results

    def validar_todos(self) -> List[RFValidationResult]:
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


# =====================================================
# GERAÇÃO DE RELATÓRIOS
# =====================================================

def gerar_relatorio_json(results: List[RFValidationResult], output_path: str):
    """Gera relatório JSON completo"""
    total = len(results)
    conformes = sum(1 for r in results if r.conforme)

    report = {
        "metadata": {
            "data_validacao": datetime.now().isoformat(),
            "total_rfs": total,
            "rfs_conformes": conformes,
            "taxa_conformidade": f"{(conformes/total*100):.1f}%" if total > 0 else "0%"
        },
        "rfs": [r.to_dict() for r in results],
        "resumo_por_tipo_gap": _resumir_gaps_por_tipo(results),
        "arquivos_duplicados_global": _listar_duplicados_global(results),
        "rfs_criticos": [
            r.documentacao_id for r in results
            if any(
                g['tipo'] == 'CRÍTICO'
                for v in r.arquivos_esperados.values()
                for g in v.gaps
            )
        ]
    }

    Path(output_path).write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding='utf-8'
    )
    print(f"\nRelatorio JSON salvo em: {output_path}")


def _resumir_gaps_por_tipo(results: List[RFValidationResult]) -> Dict[str, int]:
    """Resume gaps por tipo"""
    resumo = defaultdict(int)

    for result in results:
        for validation in result.arquivos_esperados.values():
            for gap in validation.gaps:
                tipo = gap.get('tipo', 'DESCONHECIDO')
                resumo[tipo] += 1

    return dict(resumo)


def _listar_duplicados_global(results: List[RFValidationResult]) -> List[Dict[str, str]]:
    """Lista todos os duplicados encontrados"""
    duplicados = []

    for result in results:
        for dup in result.arquivos_duplicados:
            duplicados.append({
                "rf_id": result.documentacao_id,
                "arquivo": dup,
                "caminho": result.pasta
            })

    return duplicados


def gerar_relatorio_html(results: List[RFValidationResult], output_path: str):
    """Gera relatório HTML interativo com tabela detalhada"""
    from datetime import datetime

    total = len(results)
    conformes = sum(1 for r in results if r.conforme)
    taxa = (conformes/total*100) if total > 0 else 0

    # Calcular estatísticas
    total_gaps = sum(r.total_gaps for r in results)
    total_duplicados = sum(len(r.arquivos_duplicados) for r in results)

    gaps_por_tipo = defaultdict(int)
    for r in results:
        for v in r.arquivos_esperados.values():
            for gap in v.gaps:
                gaps_por_tipo[gap['tipo']] += 1

    html = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Validação de Documentação - IControlIT</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}

        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}

        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 300;
        }}

        .header .subtitle {{
            opacity: 0.9;
            font-size: 1.1em;
        }}

        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
            border-bottom: 1px solid #dee2e6;
        }}

        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            text-align: center;
        }}

        .stat-card .label {{
            color: #6c757d;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
        }}

        .stat-card .value {{
            font-size: 2em;
            font-weight: bold;
            color: #2d3748;
        }}

        .stat-card.success .value {{ color: #38a169; }}
        .stat-card.warning .value {{ color: #dd6b20; }}
        .stat-card.danger .value {{ color: #e53e3e; }}

        .table-container {{
            padding: 30px;
            overflow-x: auto;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.9em;
        }}

        thead {{
            background: #2d3748;
            color: white;
            position: sticky;
            top: 0;
            z-index: 10;
        }}

        th {{
            padding: 15px 10px;
            text-align: left;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.85em;
            letter-spacing: 0.5px;
        }}

        td {{
            padding: 12px 10px;
            border-bottom: 1px solid #e2e8f0;
        }}

        tbody tr:hover {{
            background: #f7fafc;
        }}

        .rf-id {{
            font-weight: 600;
            color: #2d3748;
            font-family: 'Courier New', monospace;
        }}

        .check {{
            color: #38a169;
            font-size: 1.2em;
            font-weight: bold;
        }}

        .cross {{
            color: #e53e3e;
            font-size: 1.2em;
            font-weight: bold;
            cursor: help;
            position: relative;
        }}

        .tooltip {{
            position: relative;
            display: inline-block;
        }}

        .tooltip .tooltiptext {{
            visibility: hidden;
            width: 300px;
            background-color: #2d3748;
            color: #fff;
            text-align: left;
            border-radius: 6px;
            padding: 12px;
            position: absolute;
            z-index: 1000;
            bottom: 125%;
            left: 50%;
            margin-left: -150px;
            opacity: 0;
            transition: opacity 0.3s;
            font-size: 0.85em;
            line-height: 1.4;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }}

        .tooltip .tooltiptext::after {{
            content: "";
            position: absolute;
            top: 100%;
            left: 50%;
            margin-left: -5px;
            border-width: 5px;
            border-style: solid;
            border-color: #2d3748 transparent transparent transparent;
        }}

        .tooltip:hover .tooltiptext {{
            visibility: visible;
            opacity: 1;
        }}

        .tooltip-title {{
            font-weight: bold;
            margin-bottom: 6px;
            color: #fbbf24;
        }}

        .tooltip-list {{
            list-style: none;
            padding-left: 0;
        }}

        .tooltip-list li {{
            margin-bottom: 4px;
            padding-left: 12px;
            position: relative;
        }}

        .tooltip-list li:before {{
            content: "•";
            position: absolute;
            left: 0;
            color: #fbbf24;
        }}

        .badge {{
            display: inline-block;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 0.8em;
            font-weight: 600;
        }}

        .badge.success {{
            background: #c6f6d5;
            color: #22543d;
        }}

        .badge.danger {{
            background: #fed7d7;
            color: #742a2a;
        }}

        .badge.warning {{
            background: #feebc8;
            color: #7c2d12;
        }}

        .footer {{
            padding: 20px;
            text-align: center;
            background: #f8f9fa;
            color: #6c757d;
            font-size: 0.9em;
        }}

        .filter-container {{
            padding: 20px 30px;
            background: #f8f9fa;
            border-bottom: 1px solid #dee2e6;
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            align-items: center;
        }}

        .filter-container input {{
            padding: 8px 12px;
            border: 1px solid #cbd5e0;
            border-radius: 6px;
            font-size: 0.9em;
            flex: 1;
            min-width: 250px;
        }}

        .filter-container select {{
            padding: 8px 12px;
            border: 1px solid #cbd5e0;
            border-radius: 6px;
            font-size: 0.9em;
            background: white;
        }}

        /* Modal Styles */
        .modal {{
            display: none;
            position: fixed;
            z-index: 10000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            overflow: auto;
            background-color: rgba(0,0,0,0.6);
            animation: fadeIn 0.3s;
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}

        .modal-content {{
            background-color: #fefefe;
            margin: 3% auto;
            padding: 0;
            border: 1px solid #888;
            width: 90%;
            max-width: 900px;
            border-radius: 8px;
            box-shadow: 0 4px 24px rgba(0,0,0,0.3);
            animation: slideDown 0.3s;
        }}

        @keyframes slideDown {{
            from {{
                transform: translateY(-50px);
                opacity: 0;
            }}
            to {{
                transform: translateY(0);
                opacity: 1;
            }}
        }}

        .modal-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px 30px;
            border-radius: 8px 8px 0 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .modal-header h2 {{
            margin: 0;
            font-size: 1.5em;
            font-weight: 400;
        }}

        .close {{
            color: white;
            font-size: 32px;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.2s;
        }}

        .close:hover {{
            transform: scale(1.2);
        }}

        .modal-body {{
            padding: 30px;
            max-height: 70vh;
            overflow-y: auto;
        }}

        .gap-item {{
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 4px;
        }}

        .gap-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }}

        .gap-tipo {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.75em;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .gap-tipo-crítico {{
            background: #fee;
            color: #c00;
            border: 1px solid #c00;
        }}

        .gap-tipo-importante {{
            background: #ffe;
            color: #d70;
            border: 1px solid #d70;
        }}

        .gap-tipo-menor {{
            background: #eef;
            color: #07d;
            border: 1px solid #07d;
        }}

        .copy-btn {{
            background: #667eea;
            color: white;
            border: none;
            padding: 6px 12px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.85em;
            transition: background 0.2s;
        }}

        .copy-btn:hover {{
            background: #764ba2;
        }}

        .copy-btn:active {{
            transform: scale(0.95);
        }}

        .gap-content p {{
            margin: 10px 0;
            color: #2d3748;
        }}

        details {{
            margin-top: 10px;
        }}

        summary {{
            cursor: pointer;
            color: #667eea;
            font-weight: 600;
            padding: 8px 0;
            user-select: none;
        }}

        summary:hover {{
            color: #764ba2;
        }}

        .gap-details {{
            margin-top: 15px;
            padding: 15px;
            background: white;
            border-radius: 4px;
        }}

        .compare-section {{
            margin-bottom: 20px;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 4px;
            border-left: 3px solid #cbd5e0;
        }}

        .compare-section.action {{
            background: #e6f7ff;
            border-left-color: #1890ff;
        }}

        .compare-section h4 {{
            margin-top: 0;
            margin-bottom: 10px;
            color: #2d3748;
            font-size: 0.95em;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .compare-section pre {{
            background: white;
            padding: 12px;
            border-radius: 4px;
            border: 1px solid #e2e8f0;
            overflow-x: auto;
            font-family: 'Courier New', monospace;
            font-size: 0.85em;
            line-height: 1.5;
            white-space: pre-wrap;
            word-wrap: break-word;
        }}

        .more-gaps {{
            text-align: center;
            color: #6c757d;
            font-style: italic;
            padding: 10px;
            background: #f8f9fa;
            border-radius: 4px;
        }}

        .tooltip-footer {{
            margin-top: 10px;
            text-align: center;
        }}

        .details-btn {{
            background: #667eea;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.85em;
            font-weight: 600;
            transition: background 0.2s;
            width: 100%;
        }}

        .details-btn:hover {{
            background: #764ba2;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Validação de Documentação</h1>
            <p class="subtitle">IControlIT - Modernização de Documentação</p>
            <p class="subtitle">Gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}</p>
        </div>

        <div class="stats">
            <div class="stat-card">
                <div class="label">Total de RFs</div>
                <div class="value">{total}</div>
            </div>
            <div class="stat-card success">
                <div class="label">Conformes</div>
                <div class="value">{conformes}</div>
            </div>
            <div class="stat-card danger">
                <div class="label">Não Conformes</div>
                <div class="value">{total - conformes}</div>
            </div>
            <div class="stat-card warning">
                <div class="label">Taxa Conformidade</div>
                <div class="value">{taxa:.1f}%</div>
            </div>
            <div class="stat-card danger">
                <div class="label">Total Gaps</div>
                <div class="value">{total_gaps:,}</div>
            </div>
            <div class="stat-card warning">
                <div class="label">Gaps Críticos</div>
                <div class="value">{gaps_por_tipo.get('CRÍTICO', 0):,}</div>
            </div>
            <div class="stat-card warning">
                <div class="label">Gaps Importantes</div>
                <div class="value">{gaps_por_tipo.get('IMPORTANTE', 0):,}</div>
            </div>
            <div class="stat-card">
                <div class="label">Duplicados</div>
                <div class="value">{total_duplicados}</div>
            </div>
        </div>

        <div class="filter-container">
            <input type="text" id="searchInput" placeholder="🔍 Buscar RF..." onkeyup="filterTable()">
            <select id="statusFilter" onchange="filterTable()">
                <option value="">Todos os Status</option>
                <option value="conforme">Apenas Conformes</option>
                <option value="nao-conforme">Apenas Não Conformes</option>
            </select>
        </div>

        <div class="table-container">
            <table id="validationTable">
                <thead>
                    <tr>
                        <th>RF</th>
                        <th>RF.md</th>
                        <th>RF.yaml</th>
                        <th>RL.md</th>
                        <th>RL.yaml</th>
                        <th>UC.md</th>
                        <th>UC.yaml</th>
                        <th>MD.yaml</th>
                        <th>WF.md</th>
                        <th>TC.yaml</th>
                        <th>MT.yaml</th>
                        <th>STATUS</th>
                        <th>Gaps</th>
                        <th>Duplicados</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
'''

    # Gerar linhas da tabela
    for result in sorted(results, key=lambda x: x.documentacao_id):
        documentacao_id = result.documentacao_id
        conforme = result.conforme

        # Função auxiliar para gerar célula com check/cross
        def cell_status(file_key):
            arq = result.arquivos_esperados.get(file_key)
            if not arq:
                return '<td class="tooltip"><span class="cross">✗</span></td>'

            if arq.existe and arq.valido and arq.estrutura_conforme:
                return '<td><span class="check">✓</span></td>'

            # Montar tooltip expandido com comparações
            tooltip_id = f"{documentacao_id}-{file_key.replace('.', '-')}"
            gaps_html = ""

            for idx, gap in enumerate(arq.gaps[:10]):  # Primeiros 10 gaps
                gap_id = f"{tooltip_id}-gap-{idx}"

                # Texto para copiar (formato para agente)
                texto_copiar = f"""Arquivo: {file_key}
Tipo: {gap.get('tipo', 'N/A')}
Problema: {gap.get('mensagem', 'N/A')}

No template original está assim:
{gap.get('template_original', 'N/A')}

No documento analisado está assim:
{gap.get('documento_analisado', 'N/A')}

A ação a ser tomada é:
{gap.get('acao_necessaria', 'N/A')}
"""

                gaps_html += f"""
                <div class="gap-item">
                    <div class="gap-header">
                        <span class="gap-tipo gap-tipo-{gap.get('tipo', 'ERRO').lower()}">{gap.get('tipo', 'ERRO')}</span>
                        <button class="copy-btn" onclick="copyGap('{gap_id}')" title="Copiar para colar ao agente">📋 Copiar</button>
                    </div>
                    <div class="gap-content">
                        <p><strong>Problema:</strong> {gap.get('mensagem', 'N/A')}</p>
                        <details>
                            <summary>Ver comparação detalhada</summary>
                            <div class="gap-details">
                                <div class="compare-section">
                                    <h4>Template Original:</h4>
                                    <pre>{gap.get('template_original', 'N/A')}</pre>
                                </div>
                                <div class="compare-section">
                                    <h4>Documento Analisado:</h4>
                                    <pre>{gap.get('documento_analisado', 'N/A')}</pre>
                                </div>
                                <div class="compare-section action">
                                    <h4>Ação Necessária:</h4>
                                    <pre>{gap.get('acao_necessaria', 'N/A')}</pre>
                                </div>
                            </div>
                        </details>
                    </div>
                    <textarea id="{gap_id}" style="display:none;">{texto_copiar}</textarea>
                </div>
                """

            if len(arq.gaps) > 10:
                gaps_html += f'<p class="more-gaps">... e mais {len(arq.gaps) - 10} gaps (ver JSON para completo)</p>'

            # Criar modal/dropdown grande em vez de tooltip simples
            problemas = []
            if not arq.existe:
                problemas.append("Arquivo não existe")
            elif not arq.valido:
                for gap in arq.gaps[:3]:  # Preview de 3 gaps no tooltip simples
                    problemas.append(f"[{gap['tipo']}] {gap['mensagem']}")
                if len(arq.gaps) > 3:
                    problemas.append(f"... e mais {len(arq.gaps) - 3} problemas")

            tooltip_html = f'''<div class="tooltip-title">{file_key}</div>
<ul class="tooltip-list">
{''.join(f'<li>{p}</li>' for p in problemas)}
</ul>
<div class="tooltip-footer">
    <button class="details-btn" onclick="showModal('{tooltip_id}')">📋 Ver Detalhes Completos</button>
</div>'''

            # Criar modal escondido com todos os gaps detalhados
            modal_html = f'''
            <div id="modal-{tooltip_id}" class="modal">
                <div class="modal-content">
                    <div class="modal-header">
                        <h2>Gaps Detalhados: {file_key}</h2>
                        <span class="close" onclick="closeModal('{tooltip_id}')">&times;</span>
                    </div>
                    <div class="modal-body">
                        <p><strong>RF:</strong> {documentacao_id}</p>
                        <p><strong>Total de Gaps:</strong> {len(arq.gaps)}</p>
                        <hr>
                        {gaps_html}
                    </div>
                </div>
            </div>
            '''

            return f'<td class="tooltip"><span class="cross">✗</span><span class="tooltiptext">{tooltip_html}</span>{modal_html}</td>'

        # Mapear arquivos
        file_map = {
            f'{documentacao_id}.md': 'RF.md',
            f'{documentacao_id}.yaml': 'RF.yaml',
            f'RL-{documentacao_id}.md': 'RL.md',
            f'RL-{documentacao_id}.yaml': 'RL.yaml',
            f'UC-{documentacao_id}.md': 'UC.md',
            f'UC-{documentacao_id}.yaml': 'UC.yaml',
            f'MD-{documentacao_id}.yaml': 'MD.yaml',
            f'WF-{documentacao_id}.md': 'WF.md',
            f'TC-{documentacao_id}.yaml': 'TC.yaml',
            f'MT-{documentacao_id}.yaml': 'MT.yaml',
            'STATUS.yaml': 'STATUS'
        }

        status_badge = '<span class="badge success">✓ OK</span>' if conforme else '<span class="badge danger">✗ GAPS</span>'

        html += f'''
                    <tr data-status="{'conforme' if conforme else 'nao-conforme'}">
                        <td class="rf-id">{documentacao_id}</td>
                        {cell_status(f'{documentacao_id}.md')}
                        {cell_status(f'{documentacao_id}.yaml')}
                        {cell_status(f'RL-{documentacao_id}.md')}
                        {cell_status(f'RL-{documentacao_id}.yaml')}
                        {cell_status(f'UC-{documentacao_id}.md')}
                        {cell_status(f'UC-{documentacao_id}.yaml')}
                        {cell_status(f'MD-{documentacao_id}.yaml')}
                        {cell_status(f'WF-{documentacao_id}.md')}
                        {cell_status(f'TC-{documentacao_id}.yaml')}
                        {cell_status(f'MT-{documentacao_id}.yaml')}
                        {cell_status('STATUS.yaml')}
                        <td><span class="badge {'success' if result.total_gaps == 0 else 'danger'}">{result.total_gaps}</span></td>
                        <td><span class="badge {'success' if len(result.arquivos_duplicados) == 0 else 'warning'}">{len(result.arquivos_duplicados)}</span></td>
                        <td>{status_badge}</td>
                    </tr>'''

    html += '''
                </tbody>
            </table>
        </div>

        <div class="footer">
            <p><strong>Validador de Documentação v1.0</strong> | Agência ALC - alc.dev.br</p>
            <p>Projeto IControlIT - Modernização de Documentação</p>
        </div>
    </div>

    <script>
        function filterTable() {
            const searchInput = document.getElementById('searchInput').value.toUpperCase();
            const statusFilter = document.getElementById('statusFilter').value;
            const table = document.getElementById('validationTable');
            const tr = table.getElementsByTagName('tr');

            for (let i = 1; i < tr.length; i++) {
                const tdRF = tr[i].getElementsByTagName('td')[0];
                const status = tr[i].getAttribute('data-status');

                if (tdRF) {
                    const rfText = tdRF.textContent || tdRF.innerText;
                    const matchSearch = rfText.toUpperCase().indexOf(searchInput) > -1;
                    const matchStatus = !statusFilter || status === statusFilter;

                    tr[i].style.display = (matchSearch && matchStatus) ? '' : 'none';
                }
            }
        }

        function showModal(modalId) {
            const modal = document.getElementById('modal-' + modalId);
            if (modal) {
                modal.style.display = 'block';
                document.body.style.overflow = 'hidden'; // Prevent body scroll
            }
        }

        function closeModal(modalId) {
            const modal = document.getElementById('modal-' + modalId);
            if (modal) {
                modal.style.display = 'none';
                document.body.style.overflow = 'auto'; // Restore body scroll
            }
        }

        function copyGap(gapId) {
            const textarea = document.getElementById(gapId);
            if (!textarea) {
                alert('Erro: Texto não encontrado');
                return;
            }

            // Copy text to clipboard
            textarea.style.display = 'block';
            textarea.select();
            textarea.setSelectionRange(0, 99999); // For mobile

            try {
                document.execCommand('copy');

                // Show feedback
                const btn = event.target;
                const originalText = btn.innerHTML;
                btn.innerHTML = '✓ Copiado!';
                btn.style.background = '#38a169';

                setTimeout(() => {
                    btn.innerHTML = originalText;
                    btn.style.background = '#667eea';
                }, 2000);
            } catch (err) {
                alert('Erro ao copiar: ' + err);
            }

            textarea.style.display = 'none';
        }

        // Close modal when clicking outside
        window.onclick = function(event) {
            if (event.target.classList.contains('modal')) {
                event.target.style.display = 'none';
                document.body.style.overflow = 'auto';
            }
        }

        // Close modal with Escape key
        document.addEventListener('keydown', function(event) {
            if (event.key === 'Escape') {
                const modals = document.getElementsByClassName('modal');
                for (let modal of modals) {
                    if (modal.style.display === 'block') {
                        modal.style.display = 'none';
                        document.body.style.overflow = 'auto';
                    }
                }
            }
        });
    </script>
</body>
</html>'''

    Path(output_path).write_text(html, encoding='utf-8')
    print(f"Relatorio HTML salvo em: {output_path}")


def gerar_relatorio_completo_html(results: List[RFValidationResult], output_path: str):
    """Gera relatório HTML completo organizado por fases, com botões de copiar para tudo"""

    # Organizar por fase
    fases = {}
    for result in results:
        # Extrair fase do caminho (ex: "docs/documentacao/Fase-1-Sistema-Base/...")
        fase_match = re.search(r'Fase-(\d+)', result.pasta)
        if fase_match:
            fase_num = int(fase_match.group(1))
            fase_nome = re.search(r'(Fase-\d+-[^/]+)', result.pasta)
            fase_key = fase_nome.group(1) if fase_nome else f"Fase-{fase_num}"

            if fase_key not in fases:
                fases[fase_key] = []
            fases[fase_key].append(result)

    # Ordenar fases
    fases_ordenadas = dict(sorted(fases.items(), key=lambda x: int(re.search(r'Fase-(\d+)', x[0]).group(1))))

    # Estatísticas gerais
    total = len(results)
    conformes = sum(1 for r in results if r.conforme)
    total_gaps = sum(r.total_gaps for r in results)
    total_duplicados = sum(len(r.arquivos_duplicados) for r in results)

    # Contar gaps por tipo
    gaps_por_tipo = {}
    for result in results:
        for arq in result.arquivos_esperados.values():
            for gap in arq.gaps:
                tipo = gap.get('tipo', 'DESCONHECIDO')
                gaps_por_tipo[tipo] = gaps_por_tipo.get(tipo, 0) + 1

    html = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório Completo de Validação - IControlIT</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: #f5f7fa;
            padding: 20px;
            line-height: 1.6;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            overflow: hidden;
        }}

        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}

        .header h1 {{
            font-size: 2em;
            margin-bottom: 10px;
        }}

        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            padding: 20px;
            background: #f8f9fa;
            border-bottom: 2px solid #dee2e6;
        }}

        .stat-card {{
            background: white;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }}

        .stat-card .label {{
            color: #6c757d;
            font-size: 0.85em;
            text-transform: uppercase;
            margin-bottom: 5px;
        }}

        .stat-card .value {{
            font-size: 1.8em;
            font-weight: bold;
            color: #2d3748;
        }}

        .stat-card.success .value {{ color: #38a169; }}
        .stat-card.danger .value {{ color: #e53e3e; }}
        .stat-card.warning .value {{ color: #dd6b20; }}

        .actions {{
            padding: 20px;
            background: white;
            border-bottom: 2px solid #dee2e6;
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            justify-content: center;
        }}

        .btn {{
            padding: 12px 24px;
            border: none;
            border-radius: 6px;
            font-size: 1em;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }}

        .btn-primary {{
            background: #667eea;
            color: white;
        }}

        .btn-primary:hover {{
            background: #764ba2;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }}

        .btn-success {{
            background: #38a169;
            color: white;
        }}

        .btn-success:hover {{
            background: #2f855a;
        }}

        .content {{
            padding: 30px;
        }}

        .fase {{
            margin-bottom: 40px;
            border: 2px solid #e2e8f0;
            border-radius: 8px;
            overflow: hidden;
        }}

        .fase-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .fase-header h2 {{
            font-size: 1.5em;
            font-weight: 400;
        }}

        .fase-stats {{
            display: flex;
            gap: 20px;
            font-size: 0.9em;
        }}

        .fase-stats span {{
            background: rgba(255,255,255,0.2);
            padding: 5px 12px;
            border-radius: 4px;
        }}

        .rf-item {{
            border-bottom: 1px solid #e2e8f0;
            padding: 20px;
            background: white;
        }}

        .rf-item:last-child {{
            border-bottom: none;
        }}

        .rf-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }}

        .rf-title {{
            font-size: 1.2em;
            font-weight: 600;
            color: #2d3748;
            font-family: 'Courier New', monospace;
        }}

        .rf-actions {{
            display: flex;
            gap: 10px;
        }}

        .btn-small {{
            padding: 6px 12px;
            font-size: 0.85em;
            border-radius: 4px;
            border: none;
            cursor: pointer;
            transition: all 0.2s;
            font-weight: 600;
        }}

        .btn-copy {{
            background: #667eea;
            color: white;
        }}

        .btn-copy:hover {{
            background: #764ba2;
        }}

        .btn-expand {{
            background: #e2e8f0;
            color: #2d3748;
        }}

        .btn-expand:hover {{
            background: #cbd5e0;
        }}

        .rf-summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 10px;
            margin-bottom: 15px;
        }}

        .summary-item {{
            background: #f8f9fa;
            padding: 10px;
            border-radius: 4px;
            border-left: 3px solid #cbd5e0;
        }}

        .summary-item.critical {{
            border-left-color: #e53e3e;
            background: #fff5f5;
        }}

        .summary-item.important {{
            border-left-color: #dd6b20;
            background: #fffaf0;
        }}

        .summary-label {{
            font-size: 0.8em;
            color: #6c757d;
            text-transform: uppercase;
            margin-bottom: 3px;
        }}

        .summary-value {{
            font-size: 1.2em;
            font-weight: bold;
            color: #2d3748;
        }}

        .gaps-container {{
            display: none;
            margin-top: 20px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
        }}

        .gaps-container.show {{
            display: block;
        }}

        .gap-item {{
            background: white;
            border-left: 4px solid #667eea;
            padding: 15px;
            margin-bottom: 15px;
            border-radius: 4px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }}

        .gap-item.critical {{
            border-left-color: #e53e3e;
        }}

        .gap-item.important {{
            border-left-color: #dd6b20;
        }}

        .gap-item.minor {{
            border-left-color: #3182ce;
        }}

        .gap-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 10px;
        }}

        .gap-tipo {{
            display: inline-block;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 0.75em;
            font-weight: bold;
            text-transform: uppercase;
        }}

        .gap-tipo.critical {{
            background: #fee;
            color: #c00;
        }}

        .gap-tipo.important {{
            background: #ffe;
            color: #d70;
        }}

        .gap-tipo.minor {{
            background: #eef;
            color: #07d;
        }}

        .gap-file {{
            font-family: 'Courier New', monospace;
            color: #667eea;
            font-weight: 600;
            margin-bottom: 5px;
        }}

        .gap-section {{
            margin: 15px 0;
            padding: 12px;
            background: #f8f9fa;
            border-radius: 4px;
        }}

        .gap-section h4 {{
            font-size: 0.9em;
            text-transform: uppercase;
            color: #6c757d;
            margin-bottom: 8px;
            letter-spacing: 0.5px;
        }}

        .gap-section pre {{
            background: white;
            padding: 12px;
            border-radius: 4px;
            border: 1px solid #e2e8f0;
            overflow-x: auto;
            font-family: 'Courier New', monospace;
            font-size: 0.85em;
            line-height: 1.5;
            white-space: pre-wrap;
            word-wrap: break-word;
        }}

        .gap-section.action {{
            background: #e6f7ff;
            border: 1px solid #91d5ff;
        }}

        .gap-section.action h4 {{
            color: #1890ff;
        }}

        .copy-feedback {{
            position: fixed;
            top: 20px;
            right: 20px;
            background: #38a169;
            color: white;
            padding: 15px 25px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            display: none;
            animation: slideIn 0.3s;
            z-index: 10000;
        }}

        .copy-feedback.show {{
            display: block;
        }}

        @keyframes slideIn {{
            from {{
                transform: translateX(400px);
                opacity: 0;
            }}
            to {{
                transform: translateX(0);
                opacity: 1;
            }}
        }}

        textarea.hidden-copy {{
            position: absolute;
            left: -9999px;
        }}

        .empty-state {{
            text-align: center;
            padding: 40px;
            color: #6c757d;
        }}

        .empty-state svg {{
            width: 100px;
            height: 100px;
            opacity: 0.3;
        }}
    </style>
</head>
<body>
    <div class="copy-feedback" id="copyFeedback">✓ Texto copiado para área de transferência!</div>

    <div class="container">
        <div class="header">
            <h1>📋 Relatório Completo de Validação</h1>
            <p>IControlIT - Modernização de Documentação</p>
            <p style="opacity: 0.9; font-size: 0.9em;">Gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}</p>
        </div>

        <div class="stats">
            <div class="stat-card">
                <div class="label">Total RFs</div>
                <div class="value">{total}</div>
            </div>
            <div class="stat-card success">
                <div class="label">Conformes</div>
                <div class="value">{conformes}</div>
            </div>
            <div class="stat-card danger">
                <div class="label">Não Conformes</div>
                <div class="value">{total - conformes}</div>
            </div>
            <div class="stat-card danger">
                <div class="label">Total Gaps</div>
                <div class="value">{total_gaps:,}</div>
            </div>
            <div class="stat-card warning">
                <div class="label">Críticos</div>
                <div class="value">{gaps_por_tipo.get('CRÍTICO', 0):,}</div>
            </div>
            <div class="stat-card warning">
                <div class="label">Importantes</div>
                <div class="value">{gaps_por_tipo.get('IMPORTANTE', 0):,}</div>
            </div>
        </div>

        <div class="actions">
            <button class="btn btn-primary" onclick="copyAll()">
                📋 Copiar TODOS os Gaps (Todas as Fases)
            </button>
            <button class="btn btn-success" onclick="expandAll()">
                ⬇️ Expandir Todos
            </button>
            <button class="btn btn-success" onclick="collapseAll()">
                ⬆️ Colapsar Todos
            </button>
        </div>

        <div class="content">
'''

    # Gerar conteúdo por fase
    for fase_nome, rfs in fases_ordenadas.items():
        fase_gaps = sum(rf.total_gaps for documentacao in rfs)
        fase_duplicados = sum(len(rf.arquivos_duplicados) for documentacao in rfs)

        html += f'''
            <div class="fase">
                <div class="fase-header">
                    <h2>{fase_nome}</h2>
                    <div class="fase-stats">
                        <span>{len(rfs)} RFs</span>
                        <span>{fase_gaps:,} Gaps</span>
                        <span>{fase_duplicados} Duplicados</span>
                    </div>
                </div>
                <div class="fase-actions" style="padding: 15px; background: #f8f9fa; border-bottom: 1px solid #e2e8f0;">
                    <button class="btn btn-small btn-copy" onclick="copyFase('{fase_nome}')">
                        📋 Copiar Toda Fase {fase_nome.split('-')[1]}
                    </button>
                </div>
'''

        # Gerar conteúdo por RF
        for documentacao in sorted(rfs, key=lambda x: x.documentacao_id):
            gaps_criticos = sum(1 for arq in rf.arquivos_esperados.values() for gap in arq.gaps if gap.get('tipo') == 'CRÍTICO')
            gaps_importantes = sum(1 for arq in rf.arquivos_esperados.values() for gap in arq.gaps if gap.get('tipo') == 'IMPORTANTE')

            html += f'''
                <div class="rf-item">
                    <div class="rf-header">
                        <div class="rf-title">{rf.rf_id}</div>
                        <div class="rf-actions">
                            <button class="btn-small btn-copy" onclick="copyRF('{rf.rf_id}')">
                                📋 Copiar RF
                            </button>
                            <button class="btn-small btn-expand" onclick="toggleRF('{rf.rf_id}')">
                                ⬇️ Expandir
                            </button>
                        </div>
                    </div>

                    <div class="rf-summary">
                        <div class="summary-item">
                            <div class="summary-label">Total Gaps</div>
                            <div class="summary-value">{rf.total_gaps}</div>
                        </div>
                        <div class="summary-item critical">
                            <div class="summary-label">Críticos</div>
                            <div class="summary-value">{gaps_criticos}</div>
                        </div>
                        <div class="summary-item important">
                            <div class="summary-label">Importantes</div>
                            <div class="summary-value">{gaps_importantes}</div>
                        </div>
                        <div class="summary-item">
                            <div class="summary-label">Duplicados</div>
                            <div class="summary-value">{len(rf.arquivos_duplicados)}</div>
                        </div>
                    </div>

                    <div class="gaps-container" id="gaps-{rf.rf_id}">
'''

            # Gerar gaps por arquivo
            for arquivo_nome, arq_val in rf.arquivos_esperados.items():
                if not arq_val.existe or len(arq_val.gaps) == 0:
                    continue

                for gap in arq_val.gaps:
                    tipo = gap.get('tipo', 'DESCONHECIDO')
                    tipo_class = tipo.lower().replace('í', 'i').replace('ã', 'a')

                    html += f'''
                        <div class="gap-item {tipo_class}">
                            <div class="gap-header">
                                <div>
                                    <span class="gap-tipo {tipo_class}">{tipo}</span>
                                    <div class="gap-file">{arquivo_nome}</div>
                                </div>
                            </div>

                            <div class="gap-section">
                                <h4>❌ Problema</h4>
                                <pre>{gap.get('mensagem', 'N/A')}</pre>
                            </div>

                            <div class="gap-section">
                                <h4>📄 No Template Original Está Assim:</h4>
                                <pre>{gap.get('template_original', 'N/A')}</pre>
                            </div>

                            <div class="gap-section">
                                <h4>📝 No Documento Analisado Está Assim:</h4>
                                <pre>{gap.get('documento_analisado', 'N/A')}</pre>
                            </div>

                            <div class="gap-section action">
                                <h4>✅ A Ação a Ser Tomada É:</h4>
                                <pre>{gap.get('acao_necessaria', 'N/A')}</pre>
                            </div>
                        </div>
'''

            html += '''
                    </div>
                </div>
'''

        html += '''
            </div>
'''

    html += '''
        </div>
    </div>

    <textarea class="hidden-copy" id="copyBuffer"></textarea>

    <script>
        function showCopyFeedback() {
            const feedback = document.getElementById('copyFeedback');
            feedback.classList.add('show');
            setTimeout(() => {
                feedback.classList.remove('show');
            }, 2000);
        }

        function copyToClipboard(text) {
            const buffer = document.getElementById('copyBuffer');
            buffer.value = text;
            buffer.select();
            buffer.setSelectionRange(0, 99999);
            document.execCommand('copy');
            showCopyFeedback();
        }

        function formatGapForCopy(gapElement) {
            const tipo = gapElement.querySelector('.gap-tipo').textContent;
            const arquivo = gapElement.querySelector('.gap-file').textContent;
            const sections = gapElement.querySelectorAll('.gap-section pre');

            let text = `========================================\\n`;
            text += `ARQUIVO: ${arquivo}\\n`;
            text += `TIPO: ${tipo}\\n`;
            text += `========================================\\n\\n`;

            const labels = ['PROBLEMA', 'NO TEMPLATE ORIGINAL ESTÁ ASSIM', 'NO DOCUMENTO ANALISADO ESTÁ ASSIM', 'A AÇÃO A SER TOMADA É'];
            sections.forEach((section, index) => {
                text += `${labels[index]}:\\n`;
                text += section.textContent.trim();
                text += `\\n\\n`;
            });

            return text;
        }

        function copyRF(rfId) {
            const gapsContainer = document.getElementById(`gaps-${rfId}`);
            const gaps = gapsContainer.querySelectorAll('.gap-item');

            let text = `\\n\\n`;
            text += `╔════════════════════════════════════════════════════════════╗\\n`;
            text += `║  RF: ${rfId.padEnd(55)} ║\\n`;
            text += `╚════════════════════════════════════════════════════════════╝\\n\\n`;

            gaps.forEach(gap => {
                text += formatGapForCopy(gap);
                text += `\\n`;
            });

            copyToClipboard(text);
        }

        function copyFase(faseNome) {
            const fase = Array.from(document.querySelectorAll('.fase')).find(f =>
                f.querySelector('.fase-header h2').textContent === faseNome
            );

            if (!fase) return;

            const rfs = fase.querySelectorAll('.rf-item');
            let text = `\\n\\n`;
            text += `╔════════════════════════════════════════════════════════════╗\\n`;
            text += `║  FASE: ${faseNome.padEnd(53)} ║\\n`;
            text += `╚════════════════════════════════════════════════════════════╝\\n\\n`;

            rfs.forEach(rf => {
                const rfId = rf.querySelector('.rf-title').textContent;
                const gapsContainer = rf.querySelector('.gaps-container');
                const gaps = gapsContainer.querySelectorAll('.gap-item');

                if (gaps.length > 0) {
                    text += `\\n--- RF: ${rfId} ---\\n\\n`;
                    gaps.forEach(gap => {
                        text += formatGapForCopy(gap);
                        text += `\\n`;
                    });
                }
            });

            copyToClipboard(text);
        }

        function copyAll() {
            const allGaps = document.querySelectorAll('.gap-item');
            let text = `\\n\\n`;
            text += `╔════════════════════════════════════════════════════════════╗\\n`;
            text += `║  RELATÓRIO COMPLETO - TODOS OS GAPS                        ║\\n`;
            text += `╚════════════════════════════════════════════════════════════╝\\n\\n`;

            const fases = document.querySelectorAll('.fase');
            fases.forEach(fase => {
                const faseNome = fase.querySelector('.fase-header h2').textContent;
                text += `\\n\\n═══ ${faseNome} ═══\\n\\n`;

                const rfs = fase.querySelectorAll('.rf-item');
                rfs.forEach(rf => {
                    const rfId = rf.querySelector('.rf-title').textContent;
                    const gapsContainer = rf.querySelector('.gaps-container');
                    const gaps = gapsContainer.querySelectorAll('.gap-item');

                    if (gaps.length > 0) {
                        text += `\\n--- RF: ${rfId} ---\\n\\n`;
                        gaps.forEach(gap => {
                            text += formatGapForCopy(gap);
                            text += `\\n`;
                        });
                    }
                });
            });

            copyToClipboard(text);
        }

        function toggleRF(rfId) {
            const container = document.getElementById(`gaps-${rfId}`);
            const btn = event.target;

            if (container.classList.contains('show')) {
                container.classList.remove('show');
                btn.textContent = '⬇️ Expandir';
            } else {
                container.classList.add('show');
                btn.textContent = '⬆️ Colapsar';
            }
        }

        function expandAll() {
            document.querySelectorAll('.gaps-container').forEach(container => {
                container.classList.add('show');
            });
            document.querySelectorAll('.btn-expand').forEach(btn => {
                btn.textContent = '⬆️ Colapsar';
            });
        }

        function collapseAll() {
            document.querySelectorAll('.gaps-container').forEach(container => {
                container.classList.remove('show');
            });
            document.querySelectorAll('.btn-expand').forEach(btn => {
                btn.textContent = '⬇️ Expandir';
            });
        }
    </script>
</body>
</html>'''

    Path(output_path).write_text(html, encoding='utf-8')
    print(f"Relatorio COMPLETO HTML salvo em: {output_path}")


def gerar_relatorio_markdown(results: List[RFValidationResult], output_path: str):
    """Gera relatório em Markdown"""
    total = len(results)
    conformes = sum(1 for r in results if r.conforme)
    taxa = (conformes/total*100) if total > 0 else 0

    lines = [
        "# Relatório de Validação de Documentação",
        "",
        f"**Data:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"**Total de RFs:** {total}",
        f"**Conformes:** {conformes} ({taxa:.1f}%)",
        f"**Não Conformes:** {total - conformes}",
        "",
        "---",
        "",
        "## Resumo por RF",
        "",
        "| RF | Pasta | Conforme | Gaps | Duplicados | Extras |",
        "|-----|-------|----------|------|------------|--------|"
    ]

    for result in results:
        status = "OK" if result.conforme else "GAPS"
        lines.append(
            f"| {result.documentacao_id} | {Path(result.pasta).name} | {status} | "
            f"{result.total_gaps} | {len(result.arquivos_duplicados)} | "
            f"{len(result.arquivos_extra)} |"
        )

    lines.extend(["", "---", "", "## Detalhes por RF", ""])

    for result in results:
        if not result.conforme:
            lines.append(f"### {result.documentacao_id}")
            lines.append("")

            # Arquivos com problemas
            for filename, validation in result.arquivos_esperados.items():
                if not validation.existe:
                    lines.append(f"- **{filename}**: Arquivo nao encontrado")
                elif not validation.valido:
                    lines.append(f"- **{filename}**: {len(validation.gaps)} gaps")
                    for gap in validation.gaps:
                        lines.append(f"  - [{gap['tipo']}] {gap['mensagem']}")

            # Duplicados
            if result.arquivos_duplicados:
                lines.append("")
                lines.append("**Arquivos Duplicados:**")
                for dup in result.arquivos_duplicados:
                    lines.append(f"- {dup}")

            # Extras
            if result.arquivos_extra:
                lines.append("")
                lines.append("**Arquivos Extra (não esperados):**")
                for extra in result.arquivos_extra:
                    lines.append(f"- {extra}")

            lines.append("")

    content = "\n".join(lines)
    Path(output_path).write_text(content, encoding='utf-8')
    print(f"Relatorio Markdown salvo em: {output_path}")


# =====================================================
# MAIN
# =====================================================

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Validador Universal de Documentação de RFs"
    )
    parser.add_argument(
        'rf_id',
        nargs='?',
        help="ID do RF (ex: RF001) ou --all, --fase N"
    )
    parser.add_argument(
        '--rf',
        type=str,
        help="Validar RF específico e gerar em relatorios/RFXXX/auditoria.json (ex: --rf RF001)"
    )
    parser.add_argument(
        '--doc',
        type=str,
        choices=['RF', 'RL', 'UC', 'WF', 'MD', 'TC', 'MT', 'STATUS'],
        help="Tipo de documento específico para validar (ex: --rf RF001 --doc UC)"
    )
    parser.add_argument(
        '--fase',
        type=int,
        help="Validar todos os RFs de uma fase"
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help="Validar todos os RFs do projeto"
    )
    parser.add_argument(
        '--output',
        default="D:\\IC2\\relatorios\\validacao-docs.json",
        help="Caminho do relatório JSON de saída"
    )

    args = parser.parse_args()

    validator = RFDocumentationValidator()
    results = []
    documentacao_mode = False  # Modo RF específico
    doc_filter = None  # Filtro de tipo de documento

    # Validar uso de --doc (só pode ser usado com --rf)
    if args.doc and not args.rf:
        print("ERRO: --doc só pode ser usado junto com --rf")
        print("Exemplo correto: python validator-docs.py --rf RF001 --doc UC")
        sys.exit(1)

    # Determinar modo de execução
    if args.rf:
        # Modo --rf: valida RF específico e gera em relatorios/RFXXX/
        documentacao_id = args.rf.upper()
        doc_filter = args.doc.upper() if args.doc else None

        if doc_filter:
            print(f"Validando {rf_id} - documento {doc_filter} (modo RF específico + filtro de documento)...")
        else:
            print(f"Validando {rf_id} (modo RF específico)...")

        result = validator.validar_rf(rf_id)

        # Aplicar filtro de documento se especificado
        if doc_filter:
            # Filtrar apenas arquivos do tipo especificado
            arquivos_filtrados = {}
            for nome_arquivo, validacao in result.arquivos_esperados.items():
                # Verificar se o arquivo corresponde ao tipo filtrado
                # RF.md, RF.yaml → RF
                # RL-RF*.md, RL-RF*.yaml → RL
                # UC-RF*.md, UC-RF*.yaml → UC
                # WF-RF*.md → WF
                # MD-RF*.yaml → MD
                # TC-RF*.yaml → TC
                # MT-RF*.yaml → MT
                # STATUS.yaml → STATUS

                if doc_filter == 'RF' and (nome_arquivo.startswith('RF') and not nome_arquivo.startswith('RL-RF')):
                    arquivos_filtrados[nome_arquivo] = validacao
                elif doc_filter == 'RL' and nome_arquivo.startswith('RL-RF'):
                    arquivos_filtrados[nome_arquivo] = validacao
                elif doc_filter == 'UC' and nome_arquivo.startswith('UC-RF'):
                    arquivos_filtrados[nome_arquivo] = validacao
                elif doc_filter == 'WF' and nome_arquivo.startswith('WF-RF'):
                    arquivos_filtrados[nome_arquivo] = validacao
                elif doc_filter == 'MD' and nome_arquivo.startswith('MD-RF'):
                    arquivos_filtrados[nome_arquivo] = validacao
                elif doc_filter == 'TC' and nome_arquivo.startswith('TC-RF'):
                    arquivos_filtrados[nome_arquivo] = validacao
                elif doc_filter == 'MT' and nome_arquivo.startswith('MT-RF'):
                    arquivos_filtrados[nome_arquivo] = validacao
                elif doc_filter == 'STATUS' and nome_arquivo == 'STATUS.yaml':
                    arquivos_filtrados[nome_arquivo] = validacao

            # Atualizar resultado com arquivos filtrados
            result.arquivos_esperados = arquivos_filtrados
            # Recalcular total de gaps
            result.total_gaps = sum(len(v.gaps) for v in arquivos_filtrados.values())
            # Recalcular conformidade
            result.conforme = result.total_gaps == 0

        results = [result]
        documentacao_mode = True

        # Definir caminho de saída específico
        if doc_filter:
            # Com filtro de documento: relatorios/rfXXX/uc/auditoria.json
            doc_dir = Path(f"D:\\IC2\\relatorios\\{rf_id.lower()}\\{doc_filter.lower()}")
            doc_dir.mkdir(parents=True, exist_ok=True)
            args.output = str(doc_dir / "auditoria.json")
        else:
            # Sem filtro: relatorios/rfXXX/auditoria.json (todos os documentos)
            documentacao_dir = Path(f"D:\\IC2\\relatorios\\{rf_id.lower()}")
            documentacao_dir.mkdir(parents=True, exist_ok=True)
            args.output = str(rf_dir / "auditoria.json")

    elif args.all:
        print("Validando TODOS os RFs do projeto...")
        results = validator.validar_todos()
    elif args.fase:
        print(f"Validando RFs da Fase {args.fase}...")
        results = validator.validar_fase(args.fase)
    elif args.rf_id:
        print(f"Validando {args.rf_id}...")
        result = validator.validar_rf(args.rf_id)
        results = [result]
    else:
        parser.print_help()
        sys.exit(1)

    # Gerar relatórios
    if results:
        gerar_relatorio_json(results, args.output)

        if documentacao_mode:
            # Modo RF: gerar JSON específico em relatorios/RFXXX/[doc]/auditoria.json
            print(f"\nRelatorio de auditoria salvo em: {args.output}")
            print(f"Pasta do RF: {Path(args.output).parent}")

            # CRITICAL FIX: Atualizar relatórios HTML consolidados com o RF atual
            # Carregar resultados existentes de validacao-docs.json (se existir)
            # e atualizar/adicionar o RF que acabou de ser validado
            print("\nAtualizando relatórios HTML consolidados...")
            relatorios_dir = Path.cwd() / "relatorios"
            relatorios_dir.mkdir(exist_ok=True)

            json_consolidado = relatorios_dir / "validacao-docs.json"
            all_results = []

            # Tentar carregar resultados existentes
            if json_consolidado.exists():
                try:
                    import json
                    with open(json_consolidado, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        # Reconstruir RFValidation objects dos dados existentes
                        for documentacao_data in data:
                            # Criar objeto RFValidation a partir do JSON
                            # (simplificado - assumindo que os campos principais existem)
                            documentacao_val = RFValidation(
                                documentacao_id=rf_data['rf_id'],
                                pasta=rf_data['pasta'],
                                arquivos_esperados={},
                                arquivos_duplicados=rf_data.get('arquivos_duplicados', []),
                                arquivos_extra=rf_data.get('arquivos_extra', []),
                                conforme=rf_data['conforme'],
                                total_gaps=rf_data['total_gaps']
                            )
                            all_results.append(rf_val)
                except:
                    # Se falhar ao carregar, começar do zero
                    pass

            # Remover o RF atual dos resultados antigos (se existir) e adicionar o novo
            all_results = [r for r in all_results if r.documentacao_id != results[0].rf_id]
            all_results.append(results[0])

            # Ordenar por RF ID
            all_results.sort(key=lambda r: r.documentacao_id)

            # Salvar JSON consolidado atualizado
            gerar_relatorio_json(all_results, str(json_consolidado))

            # Gerar HTMLs consolidados
            html_path = relatorios_dir / "validacao-docs.html"
            gerar_relatorio_html(all_results, str(html_path))

            html_completo_path = relatorios_dir / "validacao-docs-completo.html"
            gerar_relatorio_completo_html(all_results, str(html_completo_path))

            print(f"JSON consolidado atualizado: {json_consolidado}")
            print(f"HTML consolidado atualizado: {html_path}")
            print(f"HTML completo atualizado: {html_completo_path}")
        else:
            # Modo normal: gerar HTML interativo (tabela)
            html_path = args.output.replace('.json', '.html')
            gerar_relatorio_html(results, html_path)

            # Gerar HTML completo (relatório expandido)
            html_completo_path = args.output.replace('.json', '-completo.html')
            gerar_relatorio_completo_html(results, html_completo_path)

        # Resumo no console
        total = len(results)
        conformes = sum(1 for r in results if r.conforme)
        print(f"\n{'='*60}")
        print(f"RESUMO FINAL")
        print('='*60)
        print(f"Total de RFs validados: {total}")
        print(f"Conformes: {conformes} ({conformes/total*100:.1f}%)")
        print(f"Não Conformes: {total - conformes}")
        print(f"Total de Gaps: {sum(r.total_gaps for r in results)}")
        print(f"Arquivos Duplicados: {sum(len(r.arquivos_duplicados) for r in results)}")
        print('='*60)
    else:
        print("Nenhum RF encontrado para validacao.")
        sys.exit(1)


if __name__ == '__main__':
    main()
