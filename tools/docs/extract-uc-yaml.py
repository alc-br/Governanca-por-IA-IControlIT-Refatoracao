#!/usr/bin/env python3
"""
extract-uc-yaml.py - Extrator UC.md  UC.yaml

Lê UC-RFXXX.md e gera UC-RFXXX.yaml estruturado conforme template UC.yaml.

Extrai:
- Metadados (RF, versão, data)
- Casos de uso (UC00-UC04)
- Coberturas (rf_items, uc_items)
- Fluxos (principal, alternativo, exceção)
- Regras aplicadas

Uso:
    python extract-uc-yaml.py RFXXX
    python extract-uc-yaml.py --all

Autor: Agência ALC - alc.dev.br
Versão: 1.0
Data: 2025-12-29
"""

import sys
import re
import yaml
from pathlib import Path
from datetime import datetime


class ExtractorUCYaml:
    def __init__(self, base_path: str = "D:\\IC2\\docs\\rf"):
        self.base_path = Path(base_path)

    def encontrar_rf(self, documentacao_id: str) -> Path:
        """Encontra a pasta do RF (tolerante a diferentes padrões de estrutura)"""
        # Tentar múltiplos padrões de EPIC
        epic_patterns = ["EPIC*", "EPIC-*", "EPIC[0-9]*"]

        for fase_dir in self.base_path.glob("Fase-*"):
            for epic_pattern in epic_patterns:
                for epic_dir in fase_dir.glob(epic_pattern):
                    # Procurar RF com diferentes padrões
                    documentacao_patterns = [f"{rf_id}-*", f"{rf_id}"]
                    for documentacao_pattern in documentacao_patterns:
                        for documentacao_dir in epic_dir.glob(rf_pattern):
                            # Verificar se é realmente a pasta do RF
                            if documentacao_dir.is_dir() and documentacao_dir.name.startswith(rf_id):
                                return documentacao_dir

        raise FileNotFoundError(f"RF {rf_id} não encontrado em {self.base_path}")

    def extrair_uc(self, documentacao_id: str) -> dict:
        documentacao_path = self.encontrar_rf(rf_id)
        uc_md = documentacao_path / f"Casos de Uso" / f"UC-{rf_id}.md"

        if not uc_md.exists():
            uc_md = documentacao_path / f"UC-{rf_id}.md"  # Fallback raiz

        if not uc_md.exists():
            raise FileNotFoundError(f"UC-{rf_id}.md não encontrado")

        content = uc_md.read_text(encoding='utf-8')
        casos = []

        # Extrair cada UC## - Título
        uc_blocos = re.split(r'^##\s+(UC\d{2})\s+[-]\s+(.+?)$', content, flags=re.MULTILINE)

        for i in range(1, len(uc_blocos), 3):
            if i+1 >= len(uc_blocos):
                break

            uc_id = uc_blocos[i]
            nome = uc_blocos[i+1].strip()
            corpo = uc_blocos[i+2] if i+2 < len(uc_blocos) else ""

            caso = {
                "id": uc_id,
                "nome": nome,
                "ator_principal": "usuario_autenticado",
                "covers": {"rf_items": [], "uc_items": []},
                "precondicoes": [],
                "gatilho": "",
                "fluxo_principal": [],
                "fluxos_alternativos": [],
                "fluxos_excecao": [],
                "regras_aplicadas": [],
                "resultado_final": {"estado": ""}
            }

            # Extrair gatilho
            gat_match = re.search(r'\*\*Gatilho:\*\*\s+(.+)', corpo)
            if gat_match:
                caso["gatilho"] = gat_match.group(1).strip()

            # Extrair regras aplicadas
            regras = re.findall(r'(RN-[A-Z]+-\d+-\d+)', corpo)
            caso["regras_aplicadas"] = list(set(regras))

            casos.append(caso)

        return {
            "uc": {
                "rf": documentacao_id,
                "versao": "1.0",
                "data": datetime.now().strftime("%Y-%m-%d")
            },
            "casos_de_uso": casos,
            "exclusions": {"uc_items": []},
            "historico": [{
                "versao": "1.0",
                "data": datetime.now().strftime("%Y-%m-%d"),
                "autor": "Agência ALC - alc.dev.br",
                "descricao": "Versao inicial"
            }]
        }

    def salvar_yaml(self, documentacao_id: str, data: dict):
        documentacao_path = self.encontrar_rf(rf_id)
        output = documentacao_path / f"UC-{rf_id}.yaml"

        header = f"""# =============================================
# UC-{rf_id} - Casos de Uso (Contrato Comportamental)
# Gerado automaticamente de UC-{rf_id}.md
# Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# =============================================

"""
        yaml_content = yaml.dump(data, allow_unicode=True, default_flow_style=False, sort_keys=False, indent=2)
        output.write_text(header + yaml_content, encoding='utf-8')
        print(f" UC-{rf_id}.yaml criado")

    def processar_rf(self, documentacao_id: str) -> bool:
        try:
            data = self.extrair_uc(rf_id)
            self.salvar_yaml(rf_id, data)
            return True
        except Exception as e:
            print(f" Erro em {rf_id}: {e}")
            return False


def main():
    if len(sys.argv) < 2:
        print("Uso: python extract-uc-yaml.py RFXXX")
        sys.exit(1)

    extractor = ExtractorUCYaml()

    if sys.argv[1] == '--all':
        total = 0
        for fase in sorted(Path("D:\\IC2\\docs\\rf").glob("Fase-*")):
            for epic in sorted(fase.glob("EPIC-*")):
                for documentacao_dir in sorted(epic.glob("RF*")):
                    documentacao_id = documentacao_dir.name.split('-')[0]
                    if extractor.processar_rf(rf_id):
                        total += 1
        print(f"\n {total} arquivos UC.yaml gerados")
    else:
        extractor.processar_rf(sys.argv[1])


if __name__ == '__main__':
    main()
