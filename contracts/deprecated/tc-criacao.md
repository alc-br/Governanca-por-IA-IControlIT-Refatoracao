# CONTRATO DE GERAÇÃO TC (CASOS DE TESTE)

**Versão:** 2.0
**Data:** 2025-12-31
**Status:** Ativo
**Changelog v2.0:** Ordem execução bloqueante, IDs canônicos, vínculo CA obrigatório, regras priorização, política E2E, validação ciclo completo RF→UC→MT→TC

---

## 📋 SUMÁRIO EXECUTIVO

### ⚡ O que este contrato faz

Este contrato gera **Casos de Teste (TC) completos** com base nos **Casos de Uso (UC) e Massa de Teste (MT)** já criados, garantindo:

- ✅ **Cobertura Total (100%)**: TC cobre 100% dos UCs
- ✅ **Rastreabilidade Completa**: UC → MT → TC
- ✅ **Organização por Categoria**: HAPPY_PATH, VALIDACAO, SEGURANCA, etc.
- ✅ **Independência de Plataforma**: Agnóstico de linguagem/framework
- ✅ **Sem Criação de Código**: APENAS documentação

### 📁 Arquivos Gerados

1. **TC-RFXXX.yaml** - Casos de Teste (derivados dos UCs e MTs)
2. **STATUS.yaml** - Atualização de governança

✅ **UC e MT devem estar criados** (pré-requisito)
⚠️ **Commit e push:** Responsabilidade do usuário (não automatizado)

### 🎯 Princípios Fundamentais

1. **Derivação UC + MT**: TC deriva dos UCs (cenários) e MTs (dados)
2. **Cobertura Total**: TC cobre 100% dos UCs
3. **Categorização Obrigatória**: HAPPY_PATH, VALIDACAO, SEGURANCA, EDGE_CASE, AUDITORIA, INTEGRACAO, E2E
4. **Rastreabilidade**: Cada TC DEVE referenciar UC e MT correspondentes
5. **Independência**: Agnóstico de plataforma e linguagem
6. **Sem Código**: Este contrato NÃO cria implementação

### ⚠️ REGRA CRÍTICA

**Se QUALQUER UC não estiver coberto por TC, a execução é considerada FALHADA.**

---

## 1. Identificação do Agente

| Campo | Valor |
|-------|-------|
| **Papel** | Agente Gerador de Casos de Teste |
| **Escopo** | Criação completa de TC-RFXXX.yaml |
| **Modo** | Documentação (sem alteração de código) |

---

## 2. Ativação do Contrato

Este contrato é ativado quando a solicitação mencionar explicitamente:

> **"Conforme CONTRATO-GERACAO-DOCS-TC para RFXXX"**

Exemplo:
```
Conforme CONTRATO-GERACAO-DOCS-TC para RF060.
Seguir D:\IC2\CLAUDE.md.
```

---

## 3. Objetivo do Contrato

Gerar **1 arquivo fundamental** que complementa UC e MT com **casos de teste**:

1. **TC-RFXXX.yaml** - Casos de Teste (contrato de cenários)

Além disso, atualizar:

2. **STATUS.yaml** - Controle de governança e progresso do RF

### 3.1 Princípio da Cobertura Total (100%)

**REGRA CRÍTICA:** Os Casos de Teste DEVEM cobrir **100% ABSOLUTO** dos UCs.

- ✅ TODO UC DEVE estar coberto por pelo menos um TC
- ✅ TODOS os fluxos (FP, FA, FE) DEVEM ter TC correspondente
- ✅ Nenhum TC pode existir sem rastreabilidade ao UC
- ✅ Cenários fora de escopo nos UCs NÃO geram TCs

**Se houver dúvida sobre algum cenário:**
- ❌ NÃO assumir que pode ser ignorado
- ❌ NÃO deixar de documentar
- ✅ Criar TC correspondente ao UC

### 3.2 Categorização Obrigatória

**REGRA CRÍTICA:** Cada TC DEVE ter categoria clara.

Categorias obrigatórias:
- **HAPPY_PATH**: Fluxos principais (sucesso)
- **VALIDACAO**: Validações de campos
- **SEGURANCA**: Autenticação, autorização, multi-tenancy
- **EDGE_CASE**: Limites, casos extremos
- **AUDITORIA**: Campos de auditoria
- **INTEGRACAO**: Integridade referencial
- **E2E**: Fluxos completos ponta a ponta

### 3.3 Ordem de Execução Bloqueante (NOVO v2.0)

**REGRA CRÍTICA:** TC SÓ pode ser criado após MT validado.

**Pipeline obrigatório:**
```
RF → UC (validado) → MT (validado) → TC
```

**Bloqueios absolutos:**
- ❌ TC NÃO pode existir sem MT validada
- ❌ TC NÃO pode existir sem UC validado
- ❌ MT apenas "criada" (sem validação) NÃO libera TC

**Validação:**
- Checklist DEVE verificar `STATUS.yaml`:
  - `documentacao.uc = true`
  - `documentacao.mt = true`
  - `validacao_mt.checklist_aprovado = true`

**Sem estas 3 condições, TC é BLOQUEADO.**

### 3.4 Modelo Canônico de IDs Obrigatório (NOVO v2.0)

**REGRA CRÍTICA:** Todos os IDs de TC DEVEM seguir formato canônico.

**Formato obrigatório:**
```
TC-RFXXX-[CAT]-NNN
```

Onde:
- `TC-` = Prefixo fixo
- `RFXXX` = ID do RF (ex: RF060)
- `[CAT]` = Categoria (HP, VAL, SEC, EDGE, AUD, INT, E2E)
- `NNN` = Número sequencial de 3 dígitos (001, 002, etc.)

**Exemplos válidos:**
- ✅ `TC-RF060-HP-001` (primeiro happy path do RF060)
- ✅ `TC-RF060-SEC-015` (décima quinta segurança do RF060)

**Exemplos INVÁLIDOS:**
- ❌ `TC-HP-001` (falta RF)
- ❌ `TC-RF060-001` (falta categoria)
- ❌ `TC-RF060-HP-1` (falta zero à esquerda)

**Proibições absolutas:**
- ❌ IDs livres sem padrão
- ❌ IDs duplicados dentro do RF
- ❌ IDs fora do padrão canônico

### 3.5 Vínculo Obrigatório com Critérios de Aceite (NOVO v2.0)

**REGRA CRÍTICA:** CA sem TC = ERRO CRÍTICO.

**Princípio:**
> "Toda CA DEVE ter pelo menos um TC correspondente."

**Validação:**
- ✅ Checklist DEVE listar CA não cobertos
- ❌ CA sem TC = BLOQUEIO CRÍTICO

**Estrutura obrigatória:**

```yaml
TC-RF060-HP-001:
  origem:
    criterios_aceite: ["CA-UC01-001", "CA-UC01-002"]  # ← OBRIGATÓRIO
```

### 3.6 Regras de Priorização Obrigatória (NOVO v2.0)

**REGRA CRÍTICA:** Prioridade NÃO é livre.

**Regras por categoria:**

| Categoria | Prioridade Mínima | Razão |
|-----------|-------------------|-------|
| HAPPY_PATH (CRUD básico) | **CRITICA** | Fluxo principal obrigatório |
| SEGURANCA | **ALTA** (nunca BAIXA) | Segurança nunca é opcional |
| VALIDACAO (campo obrigatório) | **CRITICA** | Validação core |
| VALIDACAO (formato) | **ALTA** | Validação importante |
| AUDITORIA | **ALTA** | Rastreabilidade obrigatória |
| EDGE_CASE | **MEDIA** ou **ALTA** | Depende do impacto |
| INTEGRACAO | **ALTA** | Integridade crítica |
| E2E | **CRITICA** | Fluxo completo |

**Proibições:**
- ❌ HAPPY_PATH com prioridade MEDIA ou BAIXA
- ❌ SEGURANCA com prioridade BAIXA
- ❌ E2E com prioridade BAIXA

**Validação:**
- Checklist DEVE validar prioridade × categoria
- Prioridade inválida = BLOQUEIO CRÍTICO

### 3.7 Política de E2E Obrigatória (NOVO v2.0)

**REGRA CRÍTICA:** E2E não é opcional para certos RFs.

**E2E é OBRIGATÓRIO quando:**
- ✅ RF envolve múltiplos UCs (UC00-UC04 = CRUD completo)
- ✅ RF possui integração com outro RF
- ✅ RF possui fluxo crítico de negócio

**E2E é OPCIONAL quando:**
- ⚪ RF possui apenas 1 UC isolado
- ⚪ RF é puramente backend (sem UI)

**Critérios objetivos:**
- ✅ Se `uc_total >= 3` → E2E obrigatório
- ✅ Se RF possui dependências → E2E obrigatório
- ✅ Se RF é CRUD → E2E obrigatório

**Validação:**
- Checklist DEVE verificar `e2e_obrigatorio_atendido`
- E2E obrigatório ausente = BLOQUEIO CRÍTICO

### 3.8 Granularidade Mínima de TCs (NOVO v2.0)

**REGRA CRÍTICA:** Nem sempre 1 uc_item = 1 TC.

**Critérios que exigem MÚLTIPLOS TCs por uc_item:**

1. **Validação + Autorização combinados:**
   ```
   uc_item: "UC01-FE-01" (campo obrigatório)
   → TC-VAL-001: Validação campo obrigatório
   → TC-SEC-001: Autorização para criar
   ```

2. **Multi-tenancy + Auditoria:**
   ```
   uc_item: "UC01-FP-01" (criar entidade)
   → TC-HP-001: Happy path
   → TC-SEC-010: Isolamento tenant
   → TC-AUD-001: Auditoria criação
   ```

**Regra geral:**
- Se uc_item envolve **segurança + validação**, criar 2 TCs
- Se uc_item envolve **CRUD**, criar TC de auditoria separado

**IMPORTANTE:** Este contrato NÃO inclui commit/push. O usuário é responsável por commitar os arquivos gerados.

---

## 4. Configuração de Ambiente

### 4.1 Paths do Projeto

| Variável | Caminho |
|----------|---------|
| **PROJECT_ROOT** | `D:\IC2\` |
| **RF_BASE_PATH** | ` D:\IC2\documentacao\Fase-*\EPIC*\RFXXX\` |
| **TEMPLATES_PATH** | `D:\IC2\docs\templates\` |

### 4.2 Permissões de Escrita

O agente PODE escrever **APENAS** em:
```
 D:\IC2\documentacao\Fase-*\EPIC*\RFXXX\TC-RFXXX.yaml
 D:\IC2\documentacao\Fase-*\EPIC*\RFXXX\STATUS.yaml
```

**PROIBIDO** escrever em:
- `D:\IC2\backend\**`
- `D:\IC2\frontend\**`
- `contracts/**`
- `templates/**`
- Qualquer arquivo que não seja os 2 listados acima

---

## 5. Pré-requisitos (BLOQUEANTES)

O contrato TRAVA se qualquer condição falhar:

| Pré-requisito | Descrição | Bloqueante |
|---------------|-----------|------------|
| Pasta do RF | Pasta já criada em `rf/[Fase]/[EPIC]/RFXXX/` | Sim |
| UC-RFXXX.md | UC criado e completo | Sim |
| UC-RFXXX.yaml | UC estruturado e sincronizado | Sim |
| MT-RFXXX.yaml | Massa de Teste criada | Sim |
| Template TC.yaml | Template TC.yaml disponível em `templates/` | Sim |
| STATUS.yaml | Arquivo presente na pasta do RF | Sim |
| UC Validado | STATUS.yaml com `documentacao.uc = true` | Sim |
| MT Criado | STATUS.yaml com `documentacao.mt = true` | Sim |

**PARAR se qualquer item falhar.**

---

## 6. Workflow Obrigatório de Geração

### Fase 1: Leitura de UC e MT (OBRIGATÓRIA)

Antes de criar qualquer caso de teste, o agente DEVE:

#### 1.1 Ler UC-RFXXX.md Completamente
- Localização: ` D:\IC2\documentacao\[Fase]\[EPIC]\RFXXX\UC-RFXXX.md`
- Entender TODOS os casos de uso
- Identificar TODOS os fluxos (FP, FA, FE)
- Mapear regras de negócio testáveis

#### 1.2 Ler UC-RFXXX.yaml Completamente
- Localização: ` D:\IC2\documentacao\[Fase]\[EPIC]\RFXXX\UC-RFXXX.yaml`
- Extrair cenários de teste necessários
- Mapear uc_items (granulares)
- Identificar critérios de aceite

#### 1.3 Ler MT-RFXXX.yaml Completamente
- Localização: ` D:\IC2\documentacao\[Fase]\[EPIC]\RFXXX\MT-RFXXX.yaml`
- Identificar massas de teste disponíveis
- Mapear MT por categoria
- Entender dados reutilizáveis

**Critério de completude:**
- ✅ UC.md lido integralmente
- ✅ UC.yaml lido integralmente
- ✅ MT.yaml lido integralmente
- ✅ Cenários de teste mapeados
- ✅ Massas de teste identificadas

---

### Fase 2: Criação TC-RFXXX.yaml (Casos de Teste)

#### 2.1 Criar TC-RFXXX.yaml

**Baseado em:** `D:\IC2\docs\templates\TC.yaml`

**Estrutura obrigatória derivada do template:**

- **metadata**: versao, data, autor, documentacao_relacionado, arquivo_uc_referencia, arquivo_massa_teste, tipo_teste, executor_padrao
- **estrategia**: objetivo_geral, abordagem
- **conventions**: nomenclatura_tc, categorias, prioridades
- **test_cases**: TC-[CATEGORIA]-[NUMERO] organizados por categoria
- **rastreabilidade**: Matriz TC → UC → uc_items → MT
- **historico**: versões

**Categorias obrigatórias (conforme template):**
- HAPPY_PATH
- VALIDACAO
- SEGURANCA
- EDGE_CASE
- AUDITORIA
- INTEGRACAO
- E2E

**OBRIGATÓRIO em cada TC:**
- ✅ `categoria`: Categoria clara
- ✅ `prioridade`: CRITICA, ALTA, MEDIA, BAIXA
- ✅ `uc_ref`: Referência ao UC (ex: "UC01")
- ✅ `covers.uc_items`: Lista de uc_items cobertos (granular)
- ✅ `descricao`: resumo, objetivo
- ✅ `origem`: criterios_aceite, ucs, fluxos_uc, regras_negocio
- ✅ `massa_teste.referencias`: Lista de MTs utilizadas
- ✅ `acao`: tipo, endpoint_logico
- ✅ `resultado_esperado`: sucesso, http_status, resposta/erro, banco
- ✅ `criterio_aprovacao`: Lista de critérios

**Exemplo de TC derivado do template:**

```yaml
TC-HP-001:
  categoria: "HAPPY_PATH"
  prioridade: "CRITICA"
  uc_ref: "UC01"

  covers:
    uc_items:
      - "UC01-FP-01"
      - "UC01-FP-05"

  descricao:
    resumo: "Criar registro com dados completos"
    objetivo: "Validar criação bem-sucedida no fluxo principal"

  origem:
    criterios_aceite: ["CA-UC01-001"]
    ucs: ["UC01"]
    fluxos_uc: ["FP-UC01-001"]
    regras_negocio: ["RN-UC-01-001"]

  massa_teste:
    referencias: ["MT001"]

  acao:
    tipo: "CRIAR"
    endpoint_logico: "entidade.create"

  resultado_esperado:
    sucesso: true
    http_status: 201
    resposta:
      deve_conter:
        "campo1": "valor_valido"
      campos_gerados:
        - id
        - created_at

  criterio_aprovacao:
    - "Resposta indica sucesso"
    - "Registro persistido corretamente"
```

**PROIBIDO em TC-RFXXX.yaml:**
- ❌ Criar TC sem rastreabilidade ao UC
- ❌ Omitir categorização
- ❌ Criar TC sem MT correspondente
- ❌ Criar TC órfão (sem origem rastreável)

---

### Fase 3: Validação Estrutural

**⚠️ IMPORTANTE:** TC NÃO possui validador automático de código.

A validação de TC é **estrutural**, realizada via **checklist** ([checklist-documentacao-tc.yaml](../../checklists/checklist-documentacao-tc.yaml)):

- ✅ Cobertura de 100% dos UCs
- ✅ Cobertura de 100% dos uc_items (granulares)
- ✅ Categorização completa (todas as 7 categorias preenchidas)
- ✅ Rastreabilidade UC → MT → TC completa
- ✅ Campos obrigatórios preenchidos (origem, massa_teste, resultado_esperado)

A validação é **manual/estrutural**, não automatizada.

---

### Fase 4: Atualização STATUS.yaml

#### 4.1 Atualizar STATUS.yaml

**Baseado em:** `D:\IC2\docs\templates\STATUS.yaml`

**Campos a atualizar:**

```yaml
documentacao:
  tc: true           # TC-RFXXX.yaml criado
```

**REGRA CRÍTICA:** Só marcar como `true` após criação completa do TC e validação estrutural via checklist.

---

### Fase 5: Finalização

Após atualizar STATUS.yaml, a geração de TCs está concluída.

**Arquivos gerados:**
- TC-RFXXX.yaml
- STATUS.yaml (atualizado)

⚠️ **IMPORTANTE:** Commit e push são responsabilidade do usuário. O agente NÃO deve realizar essas operações.

---

## 7. Regras de Qualidade (OBRIGATÓRIAS)

### 7.1 TC deve cobrir 100% dos UCs

**OBRIGATÓRIO em TC-RFXXX.yaml:**
- ✅ Cobertura de 100% dos UCs
- ✅ Cobertura de 100% dos uc_items (granulares)
- ✅ Categorização completa (HAPPY_PATH, VALIDACAO, SEGURANCA, EDGE_CASE, AUDITORIA, INTEGRACAO, E2E)
- ✅ Rastreabilidade UC → MT → TC completa
- ✅ Campos obrigatórios preenchidos

**PROIBIDO em TC-RFXXX.yaml:**
- ❌ Criar TC sem rastreabilidade ao UC
- ❌ Omitir categorização
- ❌ Criar TC sem MT correspondente

### 7.2 Coerência Estrutural Obrigatória

**Coerência UC → MT → TC:**
- Todo UC deve ter TC correspondente
- Todo uc_item deve ser coberto por TC
- Toda MT deve ser referenciada por pelo menos um TC
- Todo TC deve derivar de UC e MT existentes

---

## 8. Bloqueios de Execução

O agente DEVE PARAR se:

1. **UC-RFXXX.md não existe**: UCs não foram criados
2. **UC-RFXXX.yaml não existe**: UCs estruturados não disponíveis
3. **MT-RFXXX.yaml não existe**: Massas de teste não foram criadas
4. **Cobertura incompleta**: TC não cobre 100% dos UCs
5. **Categorização faltando**: Algum TC sem categoria definida
6. **MT órfã**: Alguma MT não é referenciada por nenhum TC

---

## 9. Critério de Pronto

O contrato só é considerado CONCLUÍDO quando:

### 9.1 Checklist de Arquivos Gerados

- [ ] TC-RFXXX.yaml criado (casos de teste cobrindo 100% dos UCs)
- [ ] STATUS.yaml atualizado

### 9.2 Checklist de Qualidade Final

- [ ] **Cobertura:** TC cobre 100% dos UCs
- [ ] **Cobertura granular:** TC cobre 100% dos uc_items
- [ ] **Categorização:** Todas as 7 categorias preenchidas
- [ ] **Rastreabilidade:** UC → MT → TC completa
- [ ] **Campos obrigatórios:** origem, massa_teste, resultado_esperado
- [ ] **Derivação:** TC deriva dos UCs e MTs
- [ ] **Sem MTs órfãs:** Todas as MTs são referenciadas
- [ ] **Arquivos prontos** (2 arquivos gerados)

**REGRA DE BLOQUEIO:** Se QUALQUER item desta lista estiver incompleto, a execução DEVE ser considerada FALHADA.

---

## 10. Próximo Contrato

Após conclusão deste contrato, a documentação de testes está completa (MT + TC).

O próximo passo é:

> **CONTRATO-EXECUCAO-BACKEND** ou **CONTRATO-EXECUCAO-FRONTEND** (para implementação)
>
> ```
> Conforme CONTRATO-EXECUCAO-BACKEND para RFXXX.
> Seguir D:\IC2\CLAUDE.md.
> ```

---

## 11. Arquivos Relacionados

| Arquivo | Descrição |
|---------|-----------|
| `contracts/documentacao/CONTRATO-GERACAO-DOCS-TC.md` | Este contrato |
| `checklists/checklist-documentacao-tc.yaml` | Checklist YAML |
| `templates/TC.yaml` | Template do TC |
| `templates/STATUS.yaml` | Template STATUS estruturado |

---

## 12. Histórico de Versões

| Versão | Data | Descrição |
|--------|------|-----------|
| 2.0 | 2025-12-31 | **UPGRADE CRÍTICO:** Ordem execução bloqueante (MT validado obrigatório), IDs canônicos TC-RFXXX-[CAT]-NNN, vínculo CA obrigatório, regras priorização por categoria, política E2E obrigatória, granularidade mínima TCs, validação ciclo completo RF→UC→MT→TC |
| 1.0 | 2025-12-31 | Criação do contrato separado (TC depois de MT, TC depois de UC) |

---

## 13. REGRA DE NEGAÇÃO ZERO

Se uma solicitação:
- não estiver explicitamente prevista no contrato ativo, ou
- conflitar com qualquer regra do contrato

ENTÃO:

- A execução DEVE ser NEGADA
- Nenhuma ação parcial pode ser realizada
- Nenhum "adiantamento" é permitido

---

**FIM DO CONTRATO**
