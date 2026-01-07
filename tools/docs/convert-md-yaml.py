#!/usr/bin/env python3
"""
convert-md-yaml.py - Conversor MD.md  MD.yaml

Converte MD-RFXXX.md para MD-RFXXX.yaml conforme template MD.yaml.

Extrai:
- DDL completo
- Estrutura de tabelas
- Relacionamentos
- Índices

Uso:
    python convert-md-yaml.py RFXXX
    python convert-md-yaml.py --all

Autor: Agência ALC - alc.dev.br
Versão: 1.0
Data: 2025-12-29
"""

import sys
import re
import yaml
from pathlib import Path
from datetime import datetime


class ConverterMDYaml:
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

    def extrair_ddl(self, content: str) -> dict:
        """Extrai DDL SQL do MD.md"""
        ddl_match = re.search(r'```sql(.*?)```', content, re.DOTALL)
        ddl_completo = ddl_match.group(1).strip() if ddl_match else ""

        return {
            "versao": "1.0",
            "contexto": "Modernização IControlIT",
            "core": {"ddl": ddl_completo},
            "application": {"ddl": ""},
            "seed": {"ddl": ""}
        }

    def converter(self, documentacao_id: str) -> dict:
        documentacao_path = self.encontrar_rf(rf_id)
        md_md = documentacao_path / f"MD-{rf_id}.md"

        if not md_md.exists():
            raise FileNotFoundError(f"MD-{rf_id}.md não encontrado")

        content = md_md.read_text(encoding='utf-8')

        return {
            "md": {
                "rf": documentacao_id,
                "versao": "1.0",
                "data": datetime.now().strftime("%Y-%m-%d")
            },
            "database": self.extrair_ddl(content),
            "historico": [{
                "versao": "1.0",
                "data": datetime.now().strftime("%Y-%m-%d"),
                "autor": "Agência ALC - alc.dev.br",
                "descricao": "Conversão MD.md  MD.yaml"
            }]
        }

    def salvar_yaml(self, documentacao_id: str, data: dict):
        documentacao_path = self.encontrar_rf(rf_id)
        output = documentacao_path / f"MD-{rf_id}.yaml"

        header = f"""# =============================================
# MD-{rf_id} - Modelo de Dados
# Convertido de MD-{rf_id}.md
# Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# =============================================

"""
        yaml_content = yaml.dump(data, allow_unicode=True, default_flow_style=False, sort_keys=False, indent=2)
        output.write_text(header + yaml_content, encoding='utf-8')
        print(f" MD-{rf_id}.yaml criado")

        # Remover MD.md após conversão
        md_md = documentacao_path / f"MD-{rf_id}.md"
        if md_md.exists():
            md_md.unlink()
            print(f"   MD-{rf_id}.md removido")

    def processar_rf(self, documentacao_id: str) -> bool:
        try:
            data = self.converter(rf_id)
            self.salvar_yaml(rf_id, data)
            return True
        except Exception as e:
            print(f" Erro em {rf_id}: {e}")
            return False


def main():
    if len(sys.argv) < 2:
        print("Uso: python convert-md-yaml.py RFXXX")
        sys.exit(1)

    converter = ConverterMDYaml()

    if sys.argv[1] == '--all':
        total = 0
        for fase in sorted(Path("D:\\IC2\\docs\\rf").glob("Fase-*")):
            for epic in sorted(fase.glob("EPIC-*")):
                for documentacao_dir in sorted(epic.glob("RF*")):
                    documentacao_id = documentacao_dir.name.split('-')[0]
                    if converter.processar_rf(rf_id):
                        total += 1
        print(f"\n {total} arquivos MD.yaml criados")
    else:
        converter.processar_rf(sys.argv[1])


if __name__ == '__main__':
    main()
