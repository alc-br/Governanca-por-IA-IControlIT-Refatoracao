# Validador de Conformidade RF/RL com Templates

## Objetivo

O `validator-rf-rl.py` valida se os documentos gerados de Requisitos Funcionais (RF) e Referências ao Legado (RL) estão conformes aos templates oficiais em `D:\IC2\docs\templates\`.

## Validações Realizadas

### 1. RFXXX.md conforme RF.md

**Seções obrigatórias:**
- 1. OBJETIVO DO REQUISITO
- 2. ESCOPO
- 3. CONCEITOS E DEFINIÇÕES
- 4. FUNCIONALIDADES COBERTAS
- 5. REGRAS DE NEGÓCIO
- 6. ESTADOS DA ENTIDADE
- 7. EVENTOS DE DOMÍNIO
- 8. CRITÉRIOS GLOBAIS DE ACEITE
- 9. SEGURANÇA
- 10. ARTEFATOS DERIVADOS
- 11. RASTREABILIDADE

**Cabeçalho obrigatório:**
- Versão
- Data
- Autor
- EPIC
- Fase

### 2. RFXXX.yaml conforme RF.yaml

**Campos obrigatórios:**
- `rf.id`
- `rf.nome`
- `rf.versao`
- `rf.data`
- `rf.fase`
- `rf.epic`
- `rf.status`
- `descricao.objetivo`
- `escopo.incluso`
- `entidades`
- `regras_negocio`
- `permissoes`

### 3. RL-RFXXX.md conforme RL.md (opcional)

**Seções obrigatórias:**
- 1. CONTEXTO DO LEGADO
- 2. TELAS DO LEGADO
- 3. WEBSERVICES / MÉTODOS LEGADOS
- 4. TABELAS LEGADAS
- 5. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO
- 6. GAP ANALYSIS (LEGADO x RF MODERNO)
- 7. DECISÕES DE MODERNIZAÇÃO
- 8. RISCOS DE MIGRAÇÃO
- 9. RASTREABILIDADE

**Cabeçalho obrigatório:**
- Versão
- Data
- Autor

### 4. RL-RFXXX.yaml conforme RL.yaml (opcional)

**Campos obrigatórios:**
- `rf_id`
- `titulo`
- `legado.sistema`
- `referencias`

**Validação adicional:**
- Cada item em `referencias` DEVE ter campo `destino` preenchido
- Valores válidos para `destino`: `assumido`, `substituido`, `descartado`, `a_revisar`

## Uso

### Validar um RF específico

```bash
python tools/docs/validator-rf-rl.py RFXXX
```

**Exemplo:**
```bash
python tools/docs/validator-rf-rl.py RF001
```

**Saída:**
```
Validando RF001...

============================================================
RESULTADO: RF001
============================================================
RF.md Conforme: [OK]
RF.yaml Conforme: [X]
RL.md Conforme: [X]
RL.yaml Conforme: [OK]

Gaps Encontrados: 10
  [X] [CRITICO] YAML invalido: mapping values are not allowed here
      Arquivo: RF001.yaml
  [X] [CRITICO] Secao obrigatoria ausente: '1. CONTEXTO DO LEGADO'
      Arquivo: RL-RF001.md
  ...

============================================================
STATUS FINAL:
============================================================
[X] NAO CONFORME - RF possui gaps em relacao aos templates
```

### Validar todos os RFs de uma fase

```bash
python tools/docs/validator-rf-rl.py --fase N
```

**Exemplo:**
```bash
python tools/docs/validator-rf-rl.py --fase 1
```

**Saída:**
- Relatório em Markdown: `D:\IC2\relatorios\validacao-conformidade-rf-rl-fase1.md`
- Resumo no console

### Validar todos os RFs do projeto

```bash
python tools/docs/validator-rf-rl.py --all
```

**Saída:**
- Relatório em Markdown: `D:\IC2\relatorios\validacao-conformidade-rf-rl-completa.md`
- Resumo no console

## Exit Codes

O validador retorna códigos de saída específicos para automação:

| Exit Code | Significado |
|-----------|-------------|
| 0 | PASS - RF 100% conforme aos templates |
| 10 | RF.md NÃO conforme ao template |
| 11 | RF.yaml NÃO conforme ao template |
| 20 | RL.md NÃO conforme ao template |
| 21 | RL.yaml NÃO conforme ao template |
| 30 | Arquivo(s) obrigatório(s) ausente(s) |
| 1 | Erro genérico ou múltiplos RFs com gaps |

## Relatório Markdown

O relatório gerado contém:

### Resumo Geral

```markdown
# Relatório de Conformidade RF/RL com Templates

**Data:** 2025-12-31 14:30:00
**Total de RFs:** 15
**Conformes:** 12 (80.0%)
```

### Tabela de Resumo

| RF | RF.md | RF.yaml | RL.md | RL.yaml | Arquivos Ausentes | Status |
|-----|-------|---------|-------|---------|-------------------|--------|
| RF001 | [OK] | [X] | [X] | [OK] | - | [GAPS] |
| RF002 | [OK] | [OK] | N/A | N/A | - | [OK] CONFORME |

### Gaps Detalhados

```markdown
### RF001

**[CRITICO]:**
- YAML invalido: mapping values are not allowed here
  - Arquivo: RF001.yaml
- Secao obrigatoria ausente: '1. CONTEXTO DO LEGADO'
  - Arquivo: RL-RF001.md

**[IMPORTANTE]:**
- Campo de cabeçalho ausente ou incorreto: 'Versão'
  - Arquivo: RL-RF001.md
```

## JSON Output

Para RF único, além do relatório legível, também é gerado JSON estruturado:

```json
{
  "rf_id": "RF001",
  "rf_md_conforme": true,
  "rf_yaml_conforme": false,
  "rl_md_conforme": false,
  "rl_yaml_conforme": true,
  "arquivos_ausentes": [],
  "gaps": [
    {
      "tipo": "CRÍTICO",
      "arquivo": "RF001.yaml",
      "mensagem": "YAML inválido: ..."
    }
  ]
}
```

## Integração com CI/CD

### GitHub Actions

```yaml
- name: Validar conformidade RF/RL
  run: python tools/docs/validator-rf-rl.py RF001
  continue-on-error: false
```

### Azure DevOps

```yaml
- script: python tools/docs/validator-rf-rl.py --fase 1
  displayName: 'Validar Fase 1'
  failOnStderr: true
```

## Tipos de Gaps

### CRÍTICO

Bloqueiam aprovação do RF. Exemplos:
- Arquivo obrigatório ausente
- YAML malformado
- Seção obrigatória ausente
- Campo obrigatório ausente

### IMPORTANTE

Não bloqueiam, mas devem ser corrigidos. Exemplos:
- Campo de cabeçalho ausente
- Item RL sem justificativa (quando descartado)

### MENOR

Sugestões de melhoria. Exemplos:
- Item assumido sem `rf_item_relacionado`
- Tipo não padrão em referência RL

## Relação com Outros Validadores

| Validador | Objetivo |
|-----------|----------|
| **validator-rf-rl.py** | Conformidade com templates oficiais |
| validator-rl.py | Separação RF/RL (legado não misturado) |
| validator-rf-uc.py | Cobertura RF → UC → TC |
| validator-governance.py | Governança completa (todos os validadores) |

## Fluxo de Validação Completo

```
1. validator-rf-rl.py     → Documentos conformes aos templates?
   ↓ PASS
2. validator-rl.py        → Legado separado corretamente?
   ↓ PASS
3. validator-rf-uc.py     → Cobertura RF → UC → TC completa?
   ↓ PASS
4. validator-governance.py → Todos os aspectos validados?
   ↓ PASS
5. STATUS.yaml atualizado
```

## Exemplos de Correção

### Gap: Seção obrigatória ausente

**Problema:**
```
[X] [CRITICO] Secao obrigatoria ausente: '5. REGRAS DE NEGÓCIO'
    Arquivo: RF001.md
```

**Correção:**
Adicionar seção no RF001.md:

```markdown
## 5. REGRAS DE NEGÓCIO

### RN-RF001-01 — Campos obrigatórios

**Descrição**: ...
**Critério de Aceite**: ...
```

### Gap: Campo obrigatório ausente

**Problema:**
```
[X] [CRITICO] Campo obrigatório ausente: 'regras_negocio'
    Arquivo: RF001.yaml
```

**Correção:**
Adicionar campo no RF001.yaml:

```yaml
regras_negocio:
  - id: "RN-RF001-01"
    descricao: "Descrição da regra"
    tipo: "validacao"
```

### Gap: Item RL sem destino

**Problema:**
```
[X] [CRITICO] Campo 'destino' obrigatório ausente em item de referência
    Item: LEG-RF001-001
```

**Correção:**
Adicionar campo `destino` no RL-RF001.yaml:

```yaml
referencias:
  - id: "LEG-RF001-001"
    tipo: "tela"
    nome: "frmParametrosGerais.aspx"
    caminho: "ic1_legado/IControlIT/Parametros/frmParametrosGerais.aspx"
    descricao: "Tela de parâmetros gerais do legado"
    destino: "assumido"  # ← Adicionar este campo
    justificativa: "Comportamento mantido no RF moderno"
```

## Arquivos Relacionados

- Templates oficiais: `D:\IC2\docs\templates\`
  - RF.md
  - RF.yaml
  - RL.md
  - RL.yaml
- Documentos gerados: ` D:\IC2\documentacao\Fase-X\EPIC-XXX\RFXXX\`
- Relatórios: `D:\IC2\relatorios\`

## Autor

**Agência ALC - alc.dev.br**
Versão: 1.0
Data: 2025-12-31
