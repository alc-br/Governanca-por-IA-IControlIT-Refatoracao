# Validador Universal de Documentação (validator-docs.py)

**Versão:** 1.0
**Data:** 2025-12-31
**Autor:** Agência ALC - alc.dev.br

## Visão Geral

O `validator-docs.py` é um validador completo e inteligente que analisa TODOS os arquivos de documentação dos RFs contra os templates oficiais do projeto.

### Características Principais

1. **Descoberta Automática de Templates**
   - Lê templates de `D:\IC2\docs\templates\`
   - Descobre estrutura esperada automaticamente
   - Adapta-se a mudanças nos templates (novas seções, campos)

2. **Validação Abrangente**
   - Valida estrutura de arquivos Markdown (.md)
   - Valida sintaxe e campos de arquivos YAML (.yaml)
   - Detecta arquivos duplicados (.backup, .old, etc)
   - Identifica arquivos faltantes
   - Detecta arquivos extra (não esperados)

3. **Relatórios Detalhados**
   - JSON completo com todos os gaps
   - Markdown formatado para leitura humana
   - Estatísticas por tipo de gap (CRÍTICO, IMPORTANTE, MENOR)
   - Lista de arquivos duplicados
   - Top RFs com mais problemas

## Arquivos Validados

Para cada RF, o validador verifica:

- **RF{ID}.md** - Requisito Funcional (Markdown)
- **RF{ID}.yaml** - Requisito Funcional (YAML)
- **RL-RF{ID}.md** - Referência ao Legado (Markdown)
- **RL-RF{ID}.yaml** - Referência ao Legado (YAML)
- **UC-RF{ID}.md** - Casos de Uso (Markdown)
- **UC-RF{ID}.yaml** - Casos de Uso (YAML)
- **MD-RF{ID}.yaml** - Modelo de Dados (YAML)
- **WF-RF{ID}.md** - Wireframes (Markdown)
- **TC-RF{ID}.yaml** - Casos de Teste (YAML)
- **MT-RF{ID}.yaml** - Massa de Teste (YAML)
- **STATUS.yaml** - Status de Governança

## Instalação

### Requisitos

- Python 3.7+
- PyYAML 6.0+

### Opção 1: Configuração Automática (Recomendado)

```bash
# Windows
cd D:\IC2
docs\tools\docs\setup-venv.bat
```

Este script irá:
1. Criar ambiente virtual `.venv` (se não existir)
2. Instalar/atualizar pip
3. Instalar PyYAML

### Opção 2: Instalação Manual

```bash
# Criar ambiente virtual
cd D:\IC2
python -m venv .venv

# Ativar ambiente virtual (Windows)
.venv\Scripts\activate

# Instalar dependências
pip install -r tools/docs/requirements.txt
```

### Verificar Instalação

```bash
# Windows (com venv)
.venv\Scripts\python.exe docs\tools\docs\validator-docs.py --help

# Linux/Mac (com venv)
.venv/bin/python tools/docs/validator-docs.py --help
```

## Uso

### Uso Rápido (com script batch)

```bash
# Windows - após executar setup-venv.bat
cd D:\IC2

# Validar tudo
docs\tools\docs\run-validator.bat --all

# Validar um RF
docs\tools\docs\run-validator.bat RF001

# Validar uma fase
docs\tools\docs\run-validator.bat --fase 2
```

### Validar um RF específico

```bash
python tools/docs/validator-docs.py RF001
```

**Saída:**
- JSON: `.temp_ia/test-validator-rf001.json` (padrão)
- Resumo no console

### Validar uma Fase completa

```bash
python tools/docs/validator-docs.py --fase 2
```

**Saída:**
- JSON: `relatorios/validacao-docs-fase2.json`
- Markdown: `relatorios/validacao-docs-fase2.md`

### Validar TODOS os RFs

```bash
python tools/docs/validator-docs.py --all
```

**Saída:**
- JSON: `relatorios/validacao-docs.json` (padrão)
- Markdown: `relatorios/validacao-docs.md`

### Personalizar saída

```bash
python tools/docs/validator-docs.py --all \
  --output relatorios/2025-12-31-validacao-completa.json \
  --markdown relatorios/2025-12-31-validacao-completa.md
```

## Estrutura do Relatório JSON

```json
{
  "metadata": {
    "data_validacao": "2025-12-31T11:40:29",
    "total_rfs": 111,
    "rfs_conformes": 0,
    "taxa_conformidade": "0.0%"
  },
  "rfs": [
    {
      "rf_id": "RF001",
      "pasta": "D:\\IC2\\docs\\documentacao\\...",
      "arquivos_esperados": {
        "RF001.md": {
          "arquivo": "RF001.md",
          "existe": true,
          "tipo": "md",
          "valido": true,
          "estrutura_conforme": true,
          "gaps": []
        },
        "RF001.yaml": {
          "arquivo": "RF001.yaml",
          "existe": true,
          "tipo": "yaml",
          "valido": false,
          "estrutura_conforme": false,
          "gaps": [
            {
              "tipo": "CRÍTICO",
              "categoria": "sintaxe_yaml",
              "mensagem": "YAML inválido: ..."
            }
          ]
        }
      },
      "arquivos_duplicados": ["RF001.md.backup-20251230"],
      "arquivos_extra": [],
      "conforme": false,
      "total_gaps": 103
    }
  ],
  "resumo_por_tipo_gap": {
    "CRÍTICO": 536,
    "IMPORTANTE": 4817,
    "MENOR": 10953
  },
  "arquivos_duplicados_global": [
    {
      "rf_id": "RF015",
      "arquivo": "RF015.md.backup-20251230",
      "caminho": "D:\\IC2\\docs\\documentacao\\..."
    }
  ],
  "rfs_criticos": ["RF001", "RF002", "..."]
}
```

## Tipos de Gaps

### CRÍTICO
- Arquivo obrigatório não encontrado
- YAML com sintaxe inválida
- Erro ao ler arquivo

### IMPORTANTE
- Seção esperada do template não encontrada
- Campo obrigatório ausente no YAML
- Campo do template não encontrado no arquivo

### MENOR
- Metadado faltando no cabeçalho (versão, data, autor, epic, fase)
- Campo do template não encontrado (mas não obrigatório)

## Detecção de Duplicados

O validador identifica automaticamente arquivos duplicados usando padrões:

- `.backup`
- `.backup-YYYYMMDD`
- `.bak`
- `.old`
- `.tmp`
- `_copy`
- ` (1)`, ` (2)` (cópias do Windows)
- `-YYYYMMDD` (data no nome)

## Análise do Relatório JSON

### Ver resumo geral

```bash
python -c "
import json
data = json.load(open('relatorios/validacao-docs.json', encoding='utf-8'))
print(json.dumps(data['metadata'], indent=2))
print(json.dumps(data['resumo_por_tipo_gap'], indent=2))
"
```

### Top 10 RFs com mais gaps

```bash
python -c "
import json
data = json.load(open('relatorios/validacao-docs.json', encoding='utf-8'))
rfs_sorted = sorted(data['rfs'],
    key=lambda x: sum(len(v['gaps']) for v in x['arquivos_esperados'].values()),
    reverse=True)
for documentacao in rfs_sorted[:10]:
    total_gaps = sum(len(v['gaps']) for v in rf['arquivos_esperados'].values())
    print(f\"{rf['rf_id']}: {total_gaps} gaps\")
"
```

### RFs com arquivos duplicados

```bash
python -c "
import json
data = json.load(open('relatorios/validacao-docs.json', encoding='utf-8'))
for dup in data['arquivos_duplicados_global']:
    print(f\"{dup['rf_id']}: {dup['arquivo']}\")
"
```

### RFs sem MD-*.yaml

```bash
python -c "
import json
data = json.load(open('relatorios/validacao-docs.json', encoding='utf-8'))
for documentacao in data['rfs']:
    md_files = [k for k in rf['arquivos_esperados'].keys() if k.startswith('MD-')]
    if md_files and not rf['arquivos_esperados'][md_files[0]]['existe']:
        print(rf['rf_id'])
"
```

## Adaptação a Mudanças nos Templates

O validador é **auto-adaptável**:

1. **Nova seção em RF.md**
   - Template atualizado: `## 7. NOVA SEÇÃO`
   - Validador detecta automaticamente
   - Passa a validar presença desta seção em todos os RFs

2. **Novo campo em STATUS.yaml**
   - Template atualizado: `novo_campo: value`
   - Validador descobre campo automaticamente
   - Adiciona à lista de campos obrigatórios

3. **Remoção de seção**
   - Seção removida do template
   - Validador para de cobrar esta seção
   - Não gera gaps para seções removidas

## Integração com Workflows

### CI/CD - Validar antes de merge

```yaml
# .github/workflows/validate-docs.yml
- name: Validar documentação
  run: |
    python tools/docs/validator-docs.py --all --output validation.json
    # Falha se houver gaps críticos
    python -c "
    import json, sys
    data = json.load(open('validation.json'))
    criticos = data['resumo_por_tipo_gap'].get('CRÍTICO', 0)
    if criticos > 0:
        print(f'ERRO: {criticos} gaps críticos encontrados')
        sys.exit(1)
    "
```

### Pre-commit hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Validar RF alterado
RF_CHANGED=$(git diff --cached --name-only | grep -oP 'RF\d+' | head -1)

if [ ! -z "$RF_CHANGED" ]; then
    echo "Validando $RF_CHANGED..."
    python tools/docs/validator-docs.py $RF_CHANGED
fi
```

## Exemplo de Execução Completa

```bash
# Validar todos os RFs
cd D:\IC2
python tools/docs/validator-docs.py --all \
  --output relatorios/2025-12-31-validacao-COMPLETA.json \
  --markdown relatorios/2025-12-31-validacao-COMPLETA.md

# Resultado:
# ============================================================
# RESUMO FINAL
# ============================================================
# Total de RFs validados: 111
# Conformes: 0 (0.0%)
# Não Conformes: 111
# Total de Gaps: 16306
# Arquivos Duplicados: 115
# ============================================================
```

## Troubleshooting

### "Nenhum RF encontrado para validação"

**Causa:** Estrutura de pastas diferente do esperado

**Solução:** Verificar se as pastas seguem o padrão:
```
rf/Fase-X-*/EPIC*/RF*-*/
```

### "UnicodeEncodeError" no Windows

**Causa:** Console Windows não suporta emojis UTF-8

**Solução:** Já corrigido na versão atual (removidos emojis do output)

### YAML inválido em múltiplos arquivos

**Causa:** Erro de sintaxe YAML (indentação, caracteres especiais)

**Solução:**
1. Ver mensagem de erro detalhada no JSON
2. Corrigir linha indicada
3. Re-executar validador

## Roadmap

Próximas versões planejadas:

- [ ] v1.1 - Validação de cross-references (RF → UC, UC → TC)
- [ ] v1.2 - Validação de cobertura (UC cobre 100% RF)
- [ ] v1.3 - Sugestão automática de correções
- [ ] v1.4 - Modo interativo (corrigir gaps durante validação)
- [ ] v1.5 - Integração com Azure DevOps (sincronizar gaps como work items)

## Suporte

Em caso de dúvidas ou problemas:

1. Ver exemplos de uso neste README
2. Analisar JSON de saída para detalhes
3. Verificar logs de execução
4. Consultar templates oficiais em `templates/`

---

**Última Atualização:** 2025-12-31
**Versão do Validador:** 1.0
**Projeto:** IControlIT - Modernização de Documentação
