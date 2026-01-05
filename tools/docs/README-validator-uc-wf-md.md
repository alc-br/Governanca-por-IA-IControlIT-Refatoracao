# Validador de Conformidade UC/WF/MD com Templates

## Objetivo

O `validator-uc-wf-md.py` valida se os documentos de Casos de Uso (UC), Wireframes (WF) e Modelos de Dados (MD) estão conformes aos templates oficiais em `D:\IC2\docs\templates\`.

## Validações Realizadas

### 1. UC-RFXXX.md conforme UC.md

**Seções obrigatórias:**
- 1. OBJETIVO DO DOCUMENTO
- 2. SUMÁRIO DE CASOS DE USO
- 3. PADRÕES GERAIS APLICÁVEIS A TODOS OS UCs
- UC00 (Listar)
- UC01 (Criar)
- UC02 (Visualizar)
- UC03 (Editar)
- UC04 (Excluir)
- 4. MATRIZ DE RASTREABILIDADE

**Cabeçalho obrigatório:**
- RF
- Versão
- Data
- Autor

### 2. UC-RFXXX.yaml conforme UC.yaml

**Campos obrigatórios:**
- `uc.rf`
- `uc.versao`
- `uc.data`
- `casos_de_uso`

**Validação adicional:**
- Todos os 5 UCs obrigatórios devem estar presentes: UC00, UC01, UC02, UC03, UC04

### 3. WF-RFXXX.md conforme WF.md

**Seções obrigatórias:**
- 1. OBJETIVO DO DOCUMENTO
- 2. PRINCÍPIOS DE DESIGN (OBRIGATÓRIOS)
- 3. MAPA DE TELAS (COBERTURA TOTAL DO RF)
- 4. WF-01 (Listagem)
- 5. WF-02 (Criação)
- 6. WF-03 (Edição)
- 7. WF-04 (Visualização)
- 8. WF-05 (Confirmação)
- 9. NOTIFICAÇÕES
- 10. RESPONSIVIDADE (OBRIGATÓRIO)
- 11. ACESSIBILIDADE (OBRIGATÓRIO)
- 12. RASTREABILIDADE
- 13. NÃO-OBJETIVOS (OUT OF SCOPE)
- 14. HISTÓRICO DE ALTERAÇÕES

**Cabeçalho obrigatório:**
- Versão
- Data
- Autor
- RF Relacionado

### 4. MD-RFXXX.yaml conforme MD.yaml

**Campos obrigatórios:**
- `metadata.versao`
- `metadata.data`
- `metadata.autor`
- `metadata.rf_relacionado.id`
- `metadata.rf_relacionado.nome`
- `entidades`
- `observacoes`
- `historico`

**Validação adicional:**
- Cada entidade deve ter campo `campos` definido

## Uso

### Validar um RF específico

```bash
python tools/docs/validator-uc-wf-md.py RFXXX
```

**Exemplo:**
```bash
python tools/docs/validator-uc-wf-md.py RF001
```

**Saída:**
```
Validando RF001...

============================================================
RESULTADO: RF001
============================================================
UC.md Conforme: [X]
UC.yaml Conforme: [X]
WF.md Conforme: [X]
MD.yaml Conforme: [X]

[X] Arquivos Ausentes: WF-RF001.md, MD-*.yaml

Gaps Encontrados: 15
  [X] [CRITICO] Secao obrigatoria ausente: '1. OBJETIVO DO DOCUMENTO'
      Arquivo: UC-RF001.md
  ...

============================================================
STATUS FINAL:
============================================================
[X] NAO CONFORME - UC/WF/MD possuem gaps em relacao aos templates
```

### Validar todos os RFs de uma fase

```bash
python tools/docs/validator-uc-wf-md.py --fase N
```

**Exemplo:**
```bash
python tools/docs/validator-uc-wf-md.py --fase 1
```

**Saída:**
- Relatório em Markdown: `D:\IC2\relatorios\validacao-conformidade-uc-wf-md-fase1.md`
- Resumo no console

### Validar todos os RFs do projeto

```bash
python tools/docs/validator-uc-wf-md.py --all
```

**Saída:**
- Relatório em Markdown: `D:\IC2\relatorios\validacao-conformidade-uc-wf-md-completa.md`
- Resumo no console

## Exit Codes

O validador retorna códigos de saída específicos para automação:

| Exit Code | Significado |
|-----------|-------------|
| 0 | PASS - UC/WF/MD 100% conformes aos templates |
| 10 | UC.md NÃO conforme ao template |
| 11 | UC.yaml NÃO conforme ao template |
| 20 | WF.md NÃO conforme ao template |
| 30 | MD.yaml NÃO conforme ao template |
| 40 | Arquivo(s) obrigatório(s) ausente(s) |
| 1 | Erro genérico ou múltiplos RFs com gaps |

## Relatório Markdown

O relatório gerado contém:

### Resumo Geral

```markdown
# Relatorio de Conformidade UC/WF/MD com Templates

**Data:** 2025-12-31 14:30:00
**Total de RFs:** 15
**Conformes:** 12 (80.0%)
```

### Tabela de Resumo

| RF | UC.md | UC.yaml | WF.md | MD.yaml | Arquivos Ausentes | Status |
|-----|-------|---------|-------|---------|-------------------|--------|
| RF001 | [X] | [X] | [X] | [X] | WF-RF001.md, MD-*.yaml | [GAPS] |
| RF002 | [OK] | [OK] | [OK] | [OK] | - | [OK] CONFORME |

### Gaps Detalhados

```markdown
### RF001

**[CRITICO]:**
- Secao obrigatoria ausente: '1. OBJETIVO DO DOCUMENTO'
  - Arquivo: UC-RF001.md
- UCs obrigatorios ausentes: UC00, UC01, UC02, UC03, UC04
  - Arquivo: UC-RF001.yaml

**[IMPORTANTE]:**
- Campo de cabecalho ausente ou incorreto: 'Versao'
  - Arquivo: UC-RF001.md
```

## JSON Output

Para RF único, além do relatório legível, também é gerado JSON estruturado:

```json
{
  "rf_id": "RF001",
  "uc_md_conforme": false,
  "uc_yaml_conforme": false,
  "wf_md_conforme": false,
  "md_yaml_conforme": false,
  "arquivos_ausentes": ["WF-RF001.md", "MD-*.yaml"],
  "gaps": [
    {
      "tipo": "CRITICO",
      "arquivo": "UC-RF001.md",
      "mensagem": "Secao obrigatoria ausente: '1. OBJETIVO DO DOCUMENTO'"
    }
  ]
}
```

## Integração com CI/CD

### GitHub Actions

```yaml
- name: Validar conformidade UC/WF/MD
  run: python tools/docs/validator-uc-wf-md.py RF001
  continue-on-error: false
```

### Azure DevOps

```yaml
- script: python tools/docs/validator-uc-wf-md.py --fase 1
  displayName: 'Validar UC/WF/MD Fase 1'
  failOnStderr: true
```

## Tipos de Gaps

### CRÍTICO

Bloqueiam aprovação do RF. Exemplos:
- Arquivo obrigatório ausente
- YAML malformado
- Seção obrigatória ausente
- Campo obrigatório ausente
- UCs obrigatórios ausentes (UC00-UC04)
- Entidade sem campo `campos`

### IMPORTANTE

Não bloqueiam, mas devem ser corrigidos. Exemplos:
- Campo de cabeçalho ausente
- Padrão de nomenclatura incorreto

### MENOR

Sugestões de melhoria. Exemplos:
- Seções recomendadas ausentes
- Documentação complementar

## Relação com Outros Validadores

| Validador | Objetivo |
|-----------|----------|
| validator-rf-rl.py | Conformidade RF/RL com templates |
| **validator-uc-wf-md.py** | Conformidade UC/WF/MD com templates |
| validator-rf-uc.py | Cobertura RF → UC → TC |
| validator-governance.py | Governança completa (todos os validadores) |

## Fluxo de Validação Completo

```
1. validator-rf-rl.py      → RF/RL conformes aos templates?
   ↓ PASS
2. validator-uc-wf-md.py   → UC/WF/MD conformes aos templates?
   ↓ PASS
3. validator-rf-uc.py      → Cobertura RF → UC → TC completa?
   ↓ PASS
4. validator-governance.py → Todos os aspectos validados?
   ↓ PASS
5. STATUS.yaml atualizado
```

## Exemplos de Correção

### Gap: Seção obrigatória ausente em UC

**Problema:**
```
[X] [CRITICO] Secao obrigatoria ausente: '1. OBJETIVO DO DOCUMENTO'
    Arquivo: UC-RF001.md
```

**Correção:**
Adicionar seção no UC-RF001.md:

```markdown
## 1. OBJETIVO DO DOCUMENTO

Este documento descreve **todos os Casos de Uso (UC)** derivados do **RF001**,
cobrindo integralmente o comportamento funcional esperado.
```

### Gap: UCs obrigatórios ausentes

**Problema:**
```
[X] [CRITICO] UCs obrigatorios ausentes: UC00, UC01, UC02, UC03, UC04
    Arquivo: UC-RF001.yaml
```

**Correção:**
Adicionar UCs no UC-RF001.yaml:

```yaml
casos_de_uso:
  - id: "UC00"
    nome: "Listar Parametros"
    ator_principal: "usuario_autenticado"
    # ...

  - id: "UC01"
    nome: "Criar Parametro"
    ator_principal: "usuario_autenticado"
    # ...

  - id: "UC02"
    nome: "Visualizar Parametro"
    ator_principal: "usuario_autenticado"
    # ...

  - id: "UC03"
    nome: "Editar Parametro"
    ator_principal: "usuario_autenticado"
    # ...

  - id: "UC04"
    nome: "Excluir Parametro"
    ator_principal: "usuario_autenticado"
    # ...
```

### Gap: Arquivo WF ausente

**Problema:**
```
[X] [CRITICO] Arquivo WF-RF001.md nao encontrado
```

**Correção:**
Criar arquivo `WF-RF001.md` na pasta do RF baseado no template `WF.md`:

```bash
cp D:\IC2\docs\templates\WF.md D:\IC2\docs\rf\...\RF001\WF-RF001.md
# Editar WF-RF001.md com conteúdo específico do RF001
```

### Gap: Campo obrigatório ausente em MD

**Problema:**
```
[X] [CRITICO] Campo obrigatorio ausente: 'metadata.rf_relacionado.id'
    Arquivo: MD-PARAMETROS.yaml
```

**Correção:**
Adicionar campo no MD-PARAMETROS.yaml:

```yaml
metadata:
  versao: "2.0"
  data: "2025-12-31"
  autor: "Agencia ALC - alc.dev.br"
  rf_relacionado:
    id: "RF001"  # ← Adicionar este campo
    nome: "Parametros e Configuracoes do Sistema"
```

### Gap: Entidade sem campo 'campos'

**Problema:**
```
[X] [CRITICO] Entidade 'parametros_gerais' sem campo 'campos'
    Arquivo: MD-PARAMETROS.yaml
```

**Correção:**
Adicionar seção `campos` na entidade:

```yaml
entidades:
  - nome: "parametros_gerais"
    descricao: "Tabela de parametros gerais do sistema"
    campos:  # ← Adicionar esta seção
      - nome: "id"
        tipo: "BIGSERIAL"
        nulo: false
        pk: true
      - nome: "nome"
        tipo: "VARCHAR(200)"
        nulo: false
      # ... outros campos
```

## Arquivos Relacionados

- Templates oficiais: `D:\IC2\docs\templates\`
  - UC.md
  - UC.yaml
  - WF.md
  - MD.yaml
- Documentos gerados: `D:\IC2\docs\rf\Fase-X\EPIC-XXX\RFXXX\`
  - UC-RFXXX.md
  - UC-RFXXX.yaml
  - WF-RFXXX.md
  - MD-*.yaml
- Relatórios: `D:\IC2\relatorios\`

## Casos de Uso Típicos

### 1. Validar após criar UC

Após criar documentação de Casos de Uso:

```bash
python tools/docs/validator-uc-wf-md.py RF027
```

### 2. Validar antes de implementação

Antes de iniciar implementação backend/frontend, garantir que UC/WF/MD estão completos:

```bash
python tools/docs/validator-uc-wf-md.py RF027
# Exit code 0 → pode iniciar implementação
# Exit code != 0 → corrigir documentação primeiro
```

### 3. Validar Fase completa

Ao finalizar documentação de uma fase:

```bash
python tools/docs/validator-uc-wf-md.py --fase 1
# Gera relatório em relatorios/validacao-conformidade-uc-wf-md-fase1.md
```

### 4. Auditoria de projeto

Validar todo o projeto:

```bash
python tools/docs/validator-uc-wf-md.py --all
# Gera relatório completo em relatorios/validacao-conformidade-uc-wf-md-completa.md
```

## Regras de Negócio do Validador

### UC.md

1. Deve conter **exatamente 5 UCs obrigatórios** (UC00-UC04)
2. Cada UC deve ter seção própria (## UC00, ## UC01, etc.)
3. Cabeçalho deve referenciar RF relacionado
4. Matriz de rastreabilidade é obrigatória

### UC.yaml

1. Deve conter **lista `casos_de_uso`** com todos os 5 UCs
2. Cada UC deve ter `id`, `nome` e `ator_principal`
3. Campo `uc.rf` deve referenciar RF correto

### WF.md

1. Deve cobrir **5 wireframes obrigatórios** (WF-01 a WF-05)
2. Cada wireframe mapeia para um UC (WF-01→UC00, WF-02→UC01, etc.)
3. Princípios de design e acessibilidade são obrigatórios

### MD.yaml

1. Metadados completos (versão, data, autor, RF relacionado)
2. Seção `entidades` obrigatória
3. Cada entidade deve ter `campos` definidos
4. Histórico de alterações obrigatório

## Troubleshooting

### Erro: "YAML inválido"

**Sintoma:**
```
[X] [CRITICO] YAML invalido: mapping values are not allowed here
```

**Causa:** Sintaxe YAML incorreta (indentação, dois pontos, aspas)

**Solução:**
- Validar YAML em https://www.yamllint.com/
- Verificar indentação (usar espaços, não tabs)
- Verificar dois pontos após chaves

### Erro: "Seção obrigatória ausente"

**Sintoma:**
```
[X] [CRITICO] Secao obrigatoria ausente: 'UC00'
```

**Causa:** Arquivo MD não contém seção com título exato

**Solução:**
- Adicionar seção com título exato (ex: `## UC00 — Listar Parametros`)
- Verificar formato Markdown (deve começar com `##`)

### Erro: "Campo obrigatório ausente"

**Sintoma:**
```
[X] [CRITICO] Campo obrigatorio ausente: 'uc.rf'
```

**Causa:** Campo YAML ausente ou com nome incorreto

**Solução:**
- Adicionar campo no YAML seguindo estrutura do template
- Verificar nested paths (ex: `uc.rf` = `uc: { rf: "RFXXX" }`)

## Autor

**Agência ALC - alc.dev.br**
Versão: 1.0
Data: 2025-12-31
