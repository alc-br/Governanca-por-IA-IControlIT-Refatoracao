#!/usr/bin/env python3
"""
migrate-rf-to-rl.py - Script de Migração Batch Completa

Migra RFs para nova estrutura com separação RF/RL e criação de arquivos .yaml.

Funcionalidades:
1. Detecta conteúdo legado em RFXXX.md
2. Separa RFXXX.md limpo + RL-RFXXX.md/yaml
3. Gera RFXXX.yaml estruturado
4. Gera UC-RFXXX.yaml (se UC.md existir)
5. Converte MD.md  MD.yaml (se existir)
6. Backup automático antes de modificar
7. Validação pós-migração

Uso:
    python migrate-rf-to-rl.py RFXXX
    python migrate-rf-to-rl.py --fase N
    python migrate-rf-to-rl.py --all
    python migrate-rf-to-rl.py --dry-run RFXXX

Autor: Agência ALC - alc.dev.br
Versão: 1.0
Data: 2025-12-29
"""

import sys
import os
import re
import yaml
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

# Importar extratores criados na FASE 2
sys.path.append(str(Path(__file__).parent))

# Workaround: carregar módulos com hífen no nome
import importlib.util

def load_module_from_file(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

base_dir = Path(__file__).parent

extract_rf = load_module_from_file("extract_rf_yaml", base_dir / "extract-rf-yaml.py")
extract_uc = load_module_from_file("extract_uc_yaml", base_dir / "extract-uc-yaml.py")
convert_md = load_module_from_file("convert_md_yaml", base_dir / "convert-md-yaml.py")
validator_rl = load_module_from_file("validator_rl", base_dir / "validator-rl.py")

ExtractorRFYaml = extract_rf.ExtractorRFYaml
ExtractorUCYaml = extract_uc.ExtractorUCYaml
ConverterMDYaml = convert_md.ConverterMDYaml
ValidadorRL = validator_rl.ValidadorRL


class MigradorRF:
    """Migrador completo de RF para nova estrutura"""

    # Palavras-chave de legado para detectar conteúdo
    KEYWORDS_LEGADO = [
        'VB.NET', 'VB .NET', 'Visual Basic',
        'ASP.NET Web Forms', 'Web Forms', 'WebForms',
        '.aspx', 'ASPX', '.asmx',
        'GridView', 'DataGrid', 'ViewState',
        'ic1_legado', 'IControlIT legado',
        'código legado', 'sistema legado',
        'tela legado', 'webservice legado',
        'stored procedure', 'procedure SQL'
    ]

    def __init__(self, base_path: str = "D:\\IC2\\docs\\rf", dry_run: bool = False):
        self.base_path = Path(base_path)
        self.dry_run = dry_run
        self.extractor_rf = ExtractorRFYaml(base_path)
        self.extractor_uc = ExtractorUCYaml(base_path)
        self.converter_md = ConverterMDYaml(base_path)
        self.validador_rl = ValidadorRL(base_path)

    def encontrar_rf(self, documentacao_id: str) -> Path:
        """Encontra a pasta do RF"""
        for fase_dir in self.base_path.glob("Fase-*"):
            for epic_dir in fase_dir.glob("EPIC*"):
                for documentacao_dir in epic_dir.glob(f"{rf_id}-*"):
                    return documentacao_dir
        raise FileNotFoundError(f"RF {rf_id} nao encontrado")

    def criar_backup(self, arquivo: Path) -> Path:
        """Cria backup de arquivo antes de modificar"""
        if not arquivo.exists():
            return None

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        backup_path = arquivo.with_suffix(f"{arquivo.suffix}.backup-{timestamp}")

        if not self.dry_run:
            shutil.copy2(arquivo, backup_path)
            print(f"   Backup criado: {backup_path.name}")

        return backup_path

    def detectar_secoes_legado(self, content: str) -> List[Dict]:
        """Detecta seções com conteúdo legado no RF.md"""
        secoes_legado = []

        # Padrão 1: Seção explícita "Referências ao Legado"
        ref_match = re.search(
            r'##\s+(?:\d+\.\s+)?Referências ao Legado(.*?)(?=\n##|\Z)',
            content, re.DOTALL | re.IGNORECASE
        )
        if ref_match:
            secoes_legado.append({
                "tipo": "secao_explicita",
                "titulo": "Referências ao Legado",
                "conteudo": ref_match.group(0),
                "inicio": ref_match.start(),
                "fim": ref_match.end()
            })

        # Padrão 2: Parágrafos com palavras-chave de legado
        for keyword in self.KEYWORDS_LEGADO:
            pattern = re.compile(re.escape(keyword), re.IGNORECASE)
            for match in pattern.finditer(content):
                # Encontrar contexto (parágrafo completo)
                inicio = content.rfind('\n\n', 0, match.start())
                fim = content.find('\n\n', match.end())
                if inicio == -1:
                    inicio = 0
                if fim == -1:
                    fim = len(content)

                paragrafo = content[inicio:fim].strip()

                secoes_legado.append({
                    "tipo": "paragrafo_legado",
                    "keyword": keyword,
                    "conteudo": paragrafo,
                    "inicio": inicio,
                    "fim": fim
                })

        # Remover duplicatas por posição
        secoes_unicas = []
        posicoes_vistas = set()

        for secao in secoes_legado:
            pos = (secao["inicio"], secao["fim"])
            if pos not in posicoes_vistas:
                secoes_unicas.append(secao)
                posicoes_vistas.add(pos)

        return sorted(secoes_unicas, key=lambda x: x["inicio"])

    def separar_rf_limpo(self, documentacao_path: Path, documentacao_id: str) -> Tuple[str, str]:
        """Separa RF.md em conteúdo limpo + conteúdo legado"""
        documentacao_md = documentacao_path / f"{rf_id}.md"

        if not documentacao_md.exists():
            raise FileNotFoundError(f"{rf_md} não encontrado")

        content_original = documentacao_md.read_text(encoding='utf-8')
        secoes_legado = self.detectar_secoes_legado(content_original)

        if not secoes_legado:
            print(f"    Nenhum conteúdo legado detectado em {rf_id}.md")
            return content_original, ""

        # Remover seções legado do conteúdo original
        content_limpo = content_original

        # Ordenar por posição decrescente para remover de trás para frente
        for secao in sorted(secoes_legado, key=lambda x: x["inicio"], reverse=True):
            content_limpo = (
                content_limpo[:secao["inicio"]] +
                content_limpo[secao["fim"]:]
            )

        # Extrair conteúdo legado
        conteudo_legado_partes = []
        for secao in secoes_legado:
            if secao["tipo"] == "secao_explicita":
                conteudo_legado_partes.append(secao["conteudo"])
            else:
                conteudo_legado_partes.append(f"**[Extraído]** {secao['conteudo']}")

        conteudo_legado = "\n\n".join(conteudo_legado_partes)

        return content_limpo.strip(), conteudo_legado.strip()

    def gerar_rl_md(self, documentacao_id: str, conteudo_legado: str, documentacao_path: Path) -> str:
        """Gera RL-RFXXX.md estruturado"""
        template = f"""# RL-{rf_id}  Referência ao Legado

**Versão:** 1.0
**Data:** {datetime.now().strftime('%Y-%m-%d')}
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** {rf_id}
**Sistema Legado:** VB.NET + ASP.NET Web Forms
**Objetivo:** Documentar o comportamento do legado que serve de base para a refatoração.

---

## 1. CONTEXTO DO LEGADO

**Arquitetura:** Monolítica WebForms
**Linguagem / Stack:** VB.NET, ASP.NET Web Forms
**Banco de Dados:** SQL Server
**Multi-tenant:** Não
**Auditoria:** Parcial

---

## 2. CONTEÚDO EXTRAÍDO DO RF ORIGINAL

{conteudo_legado}

---

## 3. TELAS DO LEGADO

(A ser preenchido manualmente ou em migração futura)

---

## 4. WEBSERVICES / MÉTODOS LEGADOS

(A ser preenchido manualmente ou em migração futura)

---

## 5. TABELAS LEGADAS

(A ser preenchido manualmente ou em migração futura)

---

## 6. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

(A ser preenchido manualmente ou em migração futura)

---

## 7. GAP ANALYSIS (LEGADO x RF MODERNO)

(A ser preenchido manualmente ou em migração futura)

---

## 8. DECISÕES DE MODERNIZAÇÃO

(A ser preenchido manualmente ou em migração futura)

---

## 9. RISCOS DE MIGRAÇÃO

(A ser preenchido manualmente ou em migração futura)

---

## 10. RASTREABILIDADE

| Elemento Legado | Referência RF |
|----------------|---------------|
| (A preencher) | (A preencher) |

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|--------|------|-----------|-------|
| 1.0 | {datetime.now().strftime('%Y-%m-%d')} | Migração automática - conteúdo extraído de {rf_id}.md | Agência ALC - alc.dev.br |
"""
        return template

    def gerar_rl_yaml(self, documentacao_id: str, conteudo_legado: str) -> Dict:
        """Gera RL-RFXXX.yaml estruturado"""
        # Analisar conteúdo legado para gerar items
        items = []

        # Se há seção explícita, criar items básicos
        if conteudo_legado:
            items.append({
                "id": f"LEG-{rf_id}-001",
                "tipo": "regra_negocio",
                "nome": "Conteúdo legado extraído do RF original",
                "caminho": f"ic1_legado/IControlIT/ (a mapear)",
                "descricao": "Conteúdo legado identificado automaticamente no RF.md original. Requer análise manual para detalhamento.",
                "destino": "a_revisar",
                "justificativa": "Item criado automaticamente durante migração. Requer revisão manual para classificação correta e mapeamento de destino.",
                "rf_item_relacionado": None,
                "uc_relacionado": None,
                "complexidade": "alta",
                "risco_migracao": "medio",
                "prioridade": 1
            })

        return {
            "rf_id": documentacao_id,
            "titulo": f"Referência ao Legado - {rf_id}",
            "legado": {
                "sistema": "VB.NET + ASP.NET Web Forms",
                "versao": "N/A",
                "arquitetura": "Monolítica WebForms",
                "banco_dados": "SQL Server",
                "multi_tenant": False,
                "auditoria": "partial"
            },
            "referencias": items,
            "telas": [],
            "servicos": [],
            "tabelas": [],
            "regras_implicitas": [],
            "gap_analysis": [],
            "decisoes_modernizacao": [],
            "riscos_migracao": [],
            "rastreabilidade": [],
            "changelog": [
                {
                    "versao": "1.0",
                    "data": datetime.now().strftime('%Y-%m-%d'),
                    "descricao": f"Migração automática - conteúdo extraído de {rf_id}.md",
                    "autor": "Agência ALC - alc.dev.br"
                }
            ]
        }

    def migrar_rf(self, documentacao_id: str) -> Dict:
        """Migra um RF completo"""
        resultado = {
            "rf_id": documentacao_id,
            "sucesso": False,
            "arquivos_criados": [],
            "arquivos_modificados": [],
            "backups": [],
            "erros": [],
            "validacao": None
        }

        try:
            documentacao_path = self.encontrar_rf(rf_id)
            print(f"\n{'='*60}")
            print(f"Migrando {rf_id}...")
            print('='*60)

            # 1. Backup do RF.md original
            documentacao_md = documentacao_path / f"{rf_id}.md"
            backup = self.criar_backup(rf_md)
            if backup:
                resultado["backups"].append(str(backup))

            # 2. Separar RF limpo + conteúdo legado
            print(f"1. Separando conteúdo RF/RL...")
            documentacao_limpo, conteudo_legado = self.separar_rf_limpo(rf_path, documentacao_id)

            # 3. Criar RL-RFXXX.md
            print(f"2. Criando RL-{rf_id}.md...")
            rl_md_content = self.gerar_rl_md(rf_id, conteudo_legado, documentacao_path)
            rl_md_path = documentacao_path / f"RL-{rf_id}.md"

            if not self.dry_run:
                rl_md_path.write_text(rl_md_content, encoding='utf-8')
                resultado["arquivos_criados"].append(str(rl_md_path))
                print(f"    RL-{rf_id}.md criado")

            # 4. Criar RL-RFXXX.yaml
            print(f"3. Criando RL-{rf_id}.yaml...")
            rl_yaml_data = self.gerar_rl_yaml(rf_id, conteudo_legado)
            rl_yaml_path = documentacao_path / f"RL-{rf_id}.yaml"

            if not self.dry_run:
                rl_yaml_content = yaml.dump(rl_yaml_data, allow_unicode=True, default_flow_style=False, sort_keys=False, indent=2)
                header = f"""# =============================================
# RL-{rf_id} - Referência ao Legado
# Gerado automaticamente durante migração
# Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# =============================================

"""
                rl_yaml_path.write_text(header + rl_yaml_content, encoding='utf-8')
                resultado["arquivos_criados"].append(str(rl_yaml_path))
                print(f"    RL-{rf_id}.yaml criado")

            # 5. Atualizar RF.md limpo
            print(f"4. Atualizando {rf_id}.md (sem legado)...")
            if not self.dry_run:
                documentacao_md.write_text(rf_limpo, encoding='utf-8')
                resultado["arquivos_modificados"].append(str(rf_md))
                print(f"    {rf_id}.md atualizado")

            # 6. Gerar RFXXX.yaml
            print(f"5. Gerando {rf_id}.yaml...")
            try:
                if not self.dry_run:
                    self.extractor_rf.extrair_rf(rf_id)
                    resultado["arquivos_criados"].append(str(rf_path / f"{rf_id}.yaml"))
                else:
                    print(f"   [DRY-RUN] {rf_id}.yaml seria criado")
            except Exception as e:
                print(f"    Erro ao gerar {rf_id}.yaml: {e}")
                resultado["erros"].append(f"RF.yaml: {e}")

            # 7. Gerar UC-RFXXX.yaml (se UC.md existir)
            uc_md = documentacao_path / f"UC-{rf_id}.md"
            uc_md_alt = documentacao_path / "Casos de Uso" / f"UC-{rf_id}.md"

            if uc_md.exists() or uc_md_alt.exists():
                print(f"6. Gerando UC-{rf_id}.yaml...")
                try:
                    if not self.dry_run:
                        self.extractor_uc.processar_rf(rf_id)
                        resultado["arquivos_criados"].append(str(rf_path / f"UC-{rf_id}.yaml"))
                    else:
                        print(f"   [DRY-RUN] UC-{rf_id}.yaml seria criado")
                except Exception as e:
                    print(f"    Erro ao gerar UC-{rf_id}.yaml: {e}")
                    resultado["erros"].append(f"UC.yaml: {e}")
            else:
                print(f"6. UC-{rf_id}.md não encontrado - pulando UC.yaml")

            # 8. Converter MD.md  MD.yaml (se existir)
            md_md = documentacao_path / f"MD-{rf_id}.md"

            if md_md.exists():
                print(f"7. Convertendo MD-{rf_id}.md  MD-{rf_id}.yaml...")
                try:
                    if not self.dry_run:
                        self.converter_md.processar_rf(rf_id)
                        resultado["arquivos_criados"].append(str(rf_path / f"MD-{rf_id}.yaml"))
                        resultado["arquivos_modificados"].append(f"MD-{rf_id}.md (removido)")
                    else:
                        print(f"   [DRY-RUN] MD-{rf_id}.yaml seria criado, MD-{rf_id}.md seria removido")
                except Exception as e:
                    print(f"    Erro ao converter MD: {e}")
                    resultado["erros"].append(f"MD.yaml: {e}")
            else:
                print(f"7. MD-{rf_id}.md não encontrado - pulando conversão")

            # 9. Validar com validator-rl.py
            print(f"8. Validando separação RF/RL...")
            if not self.dry_run:
                validacao = self.validador_rl.validar_rf(rf_id)
                resultado["validacao"] = validacao.to_dict()

                if validacao.separacao_valida and validacao.rl_estruturado:
                    print(f"    Validação passou")
                else:
                    print(f"    Validação identificou {len(validacao.gaps)} gaps")
                    for gap in validacao.gaps[:3]:  # Mostrar primeiros 3
                        print(f"      [{gap.get('tipo')}] {gap.get('mensagem')}")
            else:
                print(f"   [DRY-RUN] validator-rl.py seria executado")

            resultado["sucesso"] = True
            print(f"\n Migração de {rf_id} concluída!")

        except Exception as e:
            print(f"\n Erro durante migração: {e}")
            resultado["erros"].append(str(e))
            resultado["sucesso"] = False

        return resultado

    def migrar_fase(self, fase_num: int) -> Dict:
        """Migra todos os RFs de uma fase"""
        fase_dir = self.base_path / f"Fase-{fase_num}"

        if not fase_dir.exists():
            print(f" Fase {fase_num} não encontrada")
            return {"sucesso": 0, "falhas": 0, "total": 0}

        resultados = {"sucesso": 0, "falhas": 0, "total": 0, "detalhes": []}

        for epic_dir in sorted(fase_dir.glob("EPIC-*")):
            for documentacao_dir in sorted(epic_dir.glob("RF*")):
                documentacao_id = documentacao_dir.name.split('-')[0]
                resultado = self.migrar_rf(rf_id)
                resultados["detalhes"].append(resultado)
                resultados["total"] += 1

                if resultado["sucesso"]:
                    resultados["sucesso"] += 1
                else:
                    resultados["falhas"] += 1

        return resultados

    def migrar_todos(self) -> Dict:
        """Migra todos os RFs do projeto"""
        resultados = {"sucesso": 0, "falhas": 0, "total": 0, "por_fase": {}}

        for fase_dir in sorted(self.base_path.glob("Fase-*")):
            fase_match = re.match(r'Fase-(\d+)', fase_dir.name)
            if fase_match:
                fase_num = int(fase_match.group(1))
                print(f"\n{'#'*60}")
                print(f"# FASE {fase_num}: {fase_dir.name}")
                print('#'*60)

                res_fase = self.migrar_fase(fase_num)
                resultados["por_fase"][fase_num] = res_fase
                resultados["sucesso"] += res_fase["sucesso"]
                resultados["falhas"] += res_fase["falhas"]
                resultados["total"] += res_fase["total"]

        return resultados


def gerar_relatorio_final(resultados: Dict, output_path: str = None):
    """Gera relatório final da migração"""
    lines = [
        "# Relatório de Migração RF/RL",
        "",
        f"**Data:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"**Total de RFs:** {resultados['total']}",
        f"**Sucesso:** {resultados['sucesso']}",
        f"**Falhas:** {resultados['falhas']}",
        f"**Taxa de Sucesso:** {(resultados['sucesso']/resultados['total']*100):.1f}%" if resultados['total'] > 0 else "0%",
        "",
        "---",
        ""
    ]

    if "por_fase" in resultados:
        lines.append("## Resumo por Fase")
        lines.append("")
        lines.append("| Fase | Total | Sucesso | Falhas | Taxa |")
        lines.append("|------|-------|---------|--------|------|")

        for fase, dados in sorted(resultados["por_fase"].items()):
            taxa = (dados["sucesso"]/dados["total"]*100) if dados["total"] > 0 else 0
            lines.append(f"| Fase {fase} | {dados['total']} | {dados['sucesso']} | {dados['falhas']} | {taxa:.1f}% |")

        lines.extend(["", "---", ""])

    content = "\n".join(lines)

    if output_path:
        Path(output_path).write_text(content, encoding='utf-8')
        print(f"\n Relatório salvo em: {output_path}")

    return content


def main():
    if len(sys.argv) < 2:
        print("Uso:")
        print("  python migrate-rf-to-rl.py RFXXX")
        print("  python migrate-rf-to-rl.py --fase N")
        print("  python migrate-rf-to-rl.py --all")
        print("  python migrate-rf-to-rl.py --dry-run RFXXX")
        sys.exit(1)

    dry_run = '--dry-run' in sys.argv
    if dry_run:
        sys.argv.remove('--dry-run')
        print("[DRY-RUN] Nenhum arquivo sera modificado\n")

    migrador = MigradorRF(dry_run=dry_run)
    arg = sys.argv[1]

    if arg == '--all':
        print("Migrando TODOS os RFs do projeto...")
        resultados = migrador.migrar_todos()
        output_file = "D:\\IC2\\relatorios\\migracao-rf-rl-completa.md"
        gerar_relatorio_final(resultados, output_file)

        print(f"\n{'='*60}")
        print(f"RESUMO FINAL: {resultados['sucesso']}/{resultados['total']} RFs migrados")
        print('='*60)

    elif arg == '--fase':
        if len(sys.argv) < 3:
            print(" Especifique o número da fase: --fase N")
            sys.exit(1)

        fase_num = int(sys.argv[2])
        print(f"Migrando RFs da Fase {fase_num}...")
        resultados = migrador.migrar_fase(fase_num)
        output_file = f"D:\\IC2\\relatorios\\migracao-rf-rl-fase{fase_num}.md"

        if resultados["total"] > 0:
            gerar_relatorio_final({"total": resultados["total"], "sucesso": resultados["sucesso"], "falhas": resultados["falhas"]}, output_file)

        print(f"\n{'='*60}")
        print(f"RESUMO: {resultados['sucesso']}/{resultados['total']} RFs migrados")
        print('='*60)

    else:
        documentacao_id = arg
        resultado = migrador.migrar_rf(rf_id)

        if resultado["sucesso"]:
            print("\n Migração concluída com sucesso!")
            print(f"Arquivos criados: {len(resultado['arquivos_criados'])}")
            print(f"Arquivos modificados: {len(resultado['arquivos_modificados'])}")
            print(f"Backups: {len(resultado['backups'])}")
        else:
            print(f"\n Migração falhou:")
            for erro in resultado["erros"]:
                print(f"  - {erro}")
            sys.exit(1)


if __name__ == '__main__':
    main()
