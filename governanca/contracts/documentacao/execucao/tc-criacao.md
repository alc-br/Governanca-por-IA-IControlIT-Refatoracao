# CONTRATO DE GERAÇÃO TC (CASOS DE TESTE)

**Versão:** 2.2
**Data:** 2026-01-11
**Status:** Ativo
**Changelog v2.2:** Adicionada Fase 1.4 (Identificar Tipo de Teste E2E) e Fase 2.2 (Documentar TC Stateful) - Identifica se RF requer STATEFUL ou ISOLATED durante criação. TCs stateful documentam: tipo_teste, requisitos_playwright, fixtures_necessarias, usa_fixture, fixture_dependencia, sequencia. Resolve gap arquitetural: stateful conhecido DURANTE criação do TC (não apenas execução)
**Changelog v2.1:** Adicionada seção 6 (Validação de UC com Especificações de Teste - BLOQUEANTE) para garantir UC completo antes de criar TC. Renumeradas seções 6→7, 7→8, 8→9, 9→10, 10→11, 11→12, 12→13, 13→14
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

## 6. Validação de UC com Especificações de Teste (NOVO - BLOQUEANTE)

**Versão:** 1.0
**Data:** 2026-01-09
**Contexto:** Adicionado após análise do RF006 para garantir que UC possui TODAS as especificações necessárias para testes E2E ANTES de criar TC.

**Objetivo:** Garantir que UC-RFXXX.yaml está 100% completo com especificações de teste, evitando criação de TC incompleto ou desatualizado.

### PASSO 6.1: Validar UC Completo com Especificações de Teste

O agente DEVE verificar que `UC-RFXXX.yaml` possui:

```python
# 1. Ler UC-RFXXX.yaml
uc_yaml = ler_yaml(f"D:\\IC2\\documentacao\\{fase}\\{epic}\\RF{rf}\\UC-RF{rf}.yaml")

# 2. Verificar seções obrigatórias para testes
validacoes = {
    "navegacao": False,
    "credenciais": False,
    "data_test_em_passos": False,
    "estados_ui": False,
    "tabela_se_aplicavel": False,
    "formulario_se_aplicavel": False,
    "performance": False,
    "timeouts_e2e": False
}

# 3. Validar seção navegacao
if "navegacao" in uc_yaml and \
   "url_completa" in uc_yaml["navegacao"] and \
   "referencia_routing" in uc_yaml["navegacao"]:
    validacoes["navegacao"] = True
else:
    ERRO("UC sem seção 'navegacao' completa (url_completa, referencia_routing)")

# 4. Validar seção credenciais
if "credenciais" in uc_yaml and \
   "referencia_seeds" in uc_yaml["credenciais"] and \
   "perfil_necessario" in uc_yaml["credenciais"]:
    validacoes["credenciais"] = True
else:
    ERRO("UC sem seção 'credenciais' completa (referencia_seeds, perfil_necessario)")

# 5. Validar data-test em TODOS os passos
passos = uc_yaml.get("passos", [])
if not passos:
    ERRO("UC sem passos definidos")

passos_com_data_test = 0
for passo in passos:
    if "elemento" in passo and "data_test" in passo["elemento"]:
        passos_com_data_test += 1

if passos_com_data_test == len(passos):
    validacoes["data_test_em_passos"] = True
else:
    ERRO(f"UC com passos sem data-test: {len(passos) - passos_com_data_test}/{len(passos)} faltando")

# 6. Validar seção estados_ui
if "estados_ui" in uc_yaml:
    estados_obrigatorios = ["loading", "vazio", "erro"]
    estados_presentes = list(uc_yaml["estados_ui"].keys())

    if all(estado in estados_presentes for estado in estados_obrigatorios):
        # Validar que cada estado tem data_test
        todos_com_data_test = True
        for estado in estados_obrigatorios:
            if "data_test" not in uc_yaml["estados_ui"][estado]:
                ERRO(f"Estado '{estado}' sem data_test")
                todos_com_data_test = False

        if todos_com_data_test:
            validacoes["estados_ui"] = True
    else:
        ERRO(f"UC sem estados UI obrigatórios: {estados_obrigatorios}")
else:
    ERRO("UC sem seção 'estados_ui'")

# 7. Validar seção tabela (se aplicável)
# Se UC menciona lista/tabela, seção é obrigatória
if "tabela" in uc_yaml:
    if "data_test_container" in uc_yaml["tabela"] and \
       "data_test_row" in uc_yaml["tabela"] and \
       "colunas" in uc_yaml["tabela"]:
        validacoes["tabela_se_aplicavel"] = True
    else:
        ERRO("UC com seção 'tabela' incompleta")
else:
    # Se não possui tabela, considerar como N/A (passou)
    validacoes["tabela_se_aplicavel"] = True

# 8. Validar seção formulario (se aplicável)
# Se UC menciona formulário, seção é obrigatória
if "formulario" in uc_yaml:
    if "data_test_form" in uc_yaml["formulario"] and \
       "campos" in uc_yaml["formulario"]:
        # Validar que TODOS os campos têm data_test
        campos = uc_yaml["formulario"]["campos"]
        campos_com_data_test = sum(1 for campo in campos if "data_test" in campo)

        if campos_com_data_test == len(campos):
            validacoes["formulario_se_aplicavel"] = True
        else:
            ERRO(f"Formulário com campos sem data_test: {len(campos) - campos_com_data_test}/{len(campos)}")
    else:
        ERRO("UC com seção 'formulario' incompleta")
else:
    # Se não possui formulário, considerar como N/A (passou)
    validacoes["formulario_se_aplicavel"] = True

# 9. Validar seção performance
if "performance" in uc_yaml and \
   "tempo_carregamento_maximo" in uc_yaml["performance"] and \
   "tempo_operacao_crud" in uc_yaml["performance"]:
    validacoes["performance"] = True
else:
    ERRO("UC sem seção 'performance' completa")

# 10. Validar seção timeouts_e2e
if "timeouts_e2e" in uc_yaml:
    timeouts_obrigatorios = ["navegacao", "loading_spinner", "dialog", "operacao_crud"]
    timeouts_presentes = list(uc_yaml["timeouts_e2e"].keys())

    if all(timeout in timeouts_presentes for timeout in timeouts_obrigatorios):
        validacoes["timeouts_e2e"] = True
    else:
        ERRO(f"UC sem timeouts E2E obrigatórios: {timeouts_obrigatorios}")
else:
    ERRO("UC sem seção 'timeouts_e2e'")

# 11. Verificar aprovação
if all(validacoes.values()):
    print("✅ UC completo com especificações de teste - TC pode ser criado")
else:
    falhas = [k for k, v in validacoes.items() if not v]
    print(f"❌ UC INCOMPLETO para testes - Faltam: {falhas}")
    print("❌ BLOQUEIO: TC NÃO pode ser criado")
    print("❌ RETORNAR ao contrato de UC (uc-criacao.md) para completar")
    PARAR()
```

**Critério de Aprovação:**
- ✅ UC possui seção `navegacao` completa (URL + referência routing)
- ✅ UC possui seção `credenciais` completa (referência seeds + perfil)
- ✅ UC possui seção `passos` com `data_test` para TODOS os elementos
- ✅ UC possui seção `estados_ui` completa (loading, vazio, erro com data_test)
- ✅ UC possui seção `tabela` completa (se aplicável)
- ✅ UC possui seção `formulario` completa (se aplicável)
- ✅ UC possui seção `performance` completa (timeouts)
- ✅ UC possui seção `timeouts_e2e` completa

**SE UC NÃO possui todas as seções:**
- ❌ BLOQUEIO: TC NÃO pode ser criado
- ❌ RETORNAR ao contrato de UC para completar FASE 3.6 (Especificações de Teste)

**IMPORTANTE:** Esta validação garante que TC será criado com seletores E2E corretos, URLs corretas, credenciais corretas e timeouts corretos, evitando falhas sistemáticas em testes E2E.

**Referência:** `CLAUDE.md` seção 18.2.2 "Bloqueios Obrigatórios"

---

## 7. Workflow Obrigatório de Geração

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

#### 1.4 Identificar Tipo de Teste E2E (NOVO - CRÍTICO)

**Versão:** 1.0
**Data:** 2026-01-11
**Contexto:** Adicionado após análise do RF006 para garantir que TCs stateful sejam documentados corretamente ANTES de implementação.

**Objetivo:** Identificar se RF requer testes **stateful** (compartilhamento de dados entre testes sequenciais) ou **isolated** (cada teste independente).

**O agente DEVE identificar:**

```python
# 1. Analisar UCs do RF
ucs = ler_todos_ucs(f"UC-RF{rf}.yaml")

# 2. Identificar padrão CRUD completo
crud_completo = False
operacoes = set()

for uc in ucs:
    if "criar" in uc.lower() or "create" in uc.lower():
        operacoes.add("CREATE")
    if "listar" in uc.lower() or "read" in uc.lower() or "visualizar" in uc.lower():
        operacoes.add("READ")
    if "editar" in uc.lower() or "update" in uc.lower():
        operacoes.add("UPDATE")
    if "excluir" in uc.lower() or "delete" in uc.lower():
        operacoes.add("DELETE")

# Se RF possui operações CRUD completas → stateful obrigatório
if len(operacoes) >= 3:  # Pelo menos 3 operações CRUD
    crud_completo = True

# 3. Identificar fluxos sequenciais
fluxos_sequenciais = False
for uc in ucs:
    if "depende" in uc.lower() or "após" in uc.lower() or "sequencial" in uc.lower():
        fluxos_sequenciais = True
        break

# 4. Determinar tipo de teste
if crud_completo or fluxos_sequenciais:
    tipo_teste_e2e = "STATEFUL"
    print("✅ RF requer testes E2E STATEFUL (compartilhamento de dados)")
    print("   Referência obrigatória: CONTRATO-TESTES-E2E-STATEFUL.md")
else:
    tipo_teste_e2e = "ISOLATED"
    print("✅ RF requer testes E2E ISOLATED (cada teste independente)")
```

**Critérios para STATEFUL:**
- ✅ RF possui CRUD completo (≥ 3 operações)
- ✅ RF possui fluxos sequenciais explícitos
- ✅ UC menciona dependências entre passos
- ✅ UC menciona compartilhamento de dados (ex: "usar ID criado")

**Critérios para ISOLATED:**
- ✅ RF possui apenas 1-2 operações isoladas
- ✅ UC não menciona dependências
- ✅ Cada UC é independente

**SE STATEFUL identificado:**
O agente DEVE:
1. Documentar em TC metadata: `tipo_teste: "STATEFUL"`
2. Referenciar contrato: `D:\IC2_Governanca\governanca\contracts\testes\CONTRATO-TESTES-E2E-STATEFUL.md`
3. Documentar requisitos:
   - playwright.config.ts: workers: 1, fullyParallel: false
   - Fixtures necessárias (ex: clienteId)
   - test.describe.serial para sequência garantida

**Referência:** `CONTRATO-TESTES-E2E-STATEFUL.md` seção 2 (Configuração Obrigatória - Playwright)

---

### Fase 2: Criação TC-RFXXX.yaml (Casos de Teste)

#### 2.1 Criar TC-RFXXX.yaml

**Baseado em:** `D:\IC2\docs\templates\TC.yaml`

**Estrutura obrigatória derivada do template:**

- **metadata**: versao, data, autor, documentacao_relacionada, arquivo_uc_referencia, arquivo_massa_teste, tipo_teste, executor_padrao
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

#### 2.2 Documentar TC Stateful (SE APLICÁVEL)

**Versão:** 1.0
**Data:** 2026-01-11
**Contexto:** Adicionado após análise do RF006 para garantir que TCs stateful sejam documentados corretamente durante criação.

**Aplicabilidade:** SE tipo_teste = "STATEFUL" (identificado em Fase 1.4), o agente DEVE adicionar seção específica em TC-RFXXX.yaml.

**Estrutura obrigatória para TC stateful:**

```yaml
metadata:
  tipo_teste: "STATEFUL"  # ← OBRIGATÓRIO

  # ← OBRIGATÓRIO: Referência ao contrato
  contrato_teste_stateful: "D:\\IC2_Governanca\\governanca\\contracts\\testes\\CONTRATO-TESTES-E2E-STATEFUL.md"

  # ← OBRIGATÓRIO: Requisitos de configuração
  requisitos_playwright:
    workers: 1                # Apenas 1 worker (obrigatório para stateful)
    fullyParallel: false      # Desabilitar paralelização (obrigatório)
    retries: 0                # Sem retries (obrigatório)

  # ← OBRIGATÓRIO: Fixtures necessárias
  fixtures_necessarias:
    - nome: "clienteId"         # Exemplo: ID da entidade criada
      tipo: "string"
      descricao: "ID do cliente criado no setup, compartilhado entre testes"
      arquivo_fixture: "e2e/fixtures/cliente-teste.ts"

# ← OBRIGATÓRIO: TCs E2E stateful devem especificar sequência
test_cases:
  TC-RF006-E2E-001:
    categoria: "E2E"
    prioridade: "CRITICA"

    # ← OBRIGATÓRIO: Indicar que teste usa fixture
    usa_fixture: true
    fixture_dependencia: "clienteId"  # Depende do fixture clienteId

    # ← OBRIGATÓRIO: Sequência de execução (test.describe.serial)
    sequencia: 1  # Ordem de execução

    descricao:
      resumo: "Passo 1: Criar Cliente (Setup via Fixture)"
      objetivo: "Fixture cria cliente UMA VEZ, compartilha ID com demais testes"

    covers:
      uc_items:
        - "UC01-FP-01"  # Criar cliente

    acao:
      tipo: "FIXTURE_SETUP"  # ← Especificar que é setup de fixture
      fixture: "clienteId"

    resultado_esperado:
      sucesso: true
      fixture_fornecido: "clienteId (string UUID)"

  TC-RF006-E2E-002:
    categoria: "E2E"
    prioridade: "CRITICA"

    # ← OBRIGATÓRIO: Indicar que teste usa fixture
    usa_fixture: true
    fixture_dependencia: "clienteId"

    sequencia: 2  # Executar APÓS TC-RF006-E2E-001

    descricao:
      resumo: "Passo 2: Listar Cliente Criado"
      objetivo: "Validar que cliente criado pela fixture está visível na listagem"

    covers:
      uc_items:
        - "UC02-FP-01"  # Listar clientes

    pre_condicoes:
      - "Cliente criado pela fixture clienteId existe"

    acao:
      tipo: "READ"
      endpoint_logico: "clientes.list"

    resultado_esperado:
      sucesso: true
      http_status: 200
      resposta:
        contem:
          - id: "${clienteId}"  # ← Referência ao fixture

  TC-RF006-E2E-003:
    categoria: "E2E"
    prioridade: "CRITICA"

    usa_fixture: true
    fixture_dependencia: "clienteId"

    sequencia: 3  # Executar APÓS TC-RF006-E2E-002

    descricao:
      resumo: "Passo 3: Editar Cliente Criado"
      objetivo: "Validar edição do cliente criado pela fixture"

    covers:
      uc_items:
        - "UC03-FP-01"  # Editar cliente

    pre_condicoes:
      - "Cliente criado pela fixture clienteId existe"

    acao:
      tipo: "UPDATE"
      endpoint_logico: "clientes.update"
      parametros:
        id: "${clienteId}"  # ← Referência ao fixture

    resultado_esperado:
      sucesso: true
      http_status: 200

  TC-RF006-E2E-004:
    categoria: "E2E"
    prioridade: "CRITICA"

    usa_fixture: true
    fixture_dependencia: "clienteId"

    sequencia: 4  # Executar APÓS TC-RF006-E2E-003

    descricao:
      resumo: "Passo 4: Excluir Cliente Criado"
      objetivo: "Validar exclusão do cliente criado pela fixture"

    covers:
      uc_items:
        - "UC04-FP-01"  # Excluir cliente

    pre_condicoes:
      - "Cliente criado pela fixture clienteId existe"

    acao:
      tipo: "DELETE"
      endpoint_logico: "clientes.delete"
      parametros:
        id: "${clienteId}"  # ← Referência ao fixture

    resultado_esperado:
      sucesso: true
      http_status: 204
      banco:
        clientes:
          nao_deve_existir:
            - id: "${clienteId}"
```

**Critério de Aprovação (SE STATEFUL):**
- ✅ `metadata.tipo_teste = "STATEFUL"`
- ✅ `metadata.contrato_teste_stateful` referencia CONTRATO-TESTES-E2E-STATEFUL.md
- ✅ `metadata.requisitos_playwright` especifica workers: 1, fullyParallel: false, retries: 0
- ✅ `metadata.fixtures_necessarias` lista TODAS as fixtures
- ✅ TCs E2E possuem `usa_fixture: true` e `fixture_dependencia`
- ✅ TCs E2E possuem `sequencia` (ordem de execução)
- ✅ TCs E2E referenciam fixture com `${nomeFixture}`

**SE tipo_teste = "ISOLATED":**
- ⚪ Esta seção NÃO é aplicável
- ⚪ PULAR para Fase 3

**Referência obrigatória:** [CONTRATO-TESTES-E2E-STATEFUL.md](D:\IC2_Governanca\governanca\contracts\testes\CONTRATO-TESTES-E2E-STATEFUL.md)

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

## 8. Regras de Qualidade (OBRIGATÓRIAS)

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

## 9. Bloqueios de Execução

O agente DEVE PARAR se:

1. **UC-RFXXX.md não existe**: UCs não foram criados
2. **UC-RFXXX.yaml não existe**: UCs estruturados não disponíveis
3. **MT-RFXXX.yaml não existe**: Massas de teste não foram criadas
4. **Cobertura incompleta**: TC não cobre 100% dos UCs
5. **Categorização faltando**: Algum TC sem categoria definida
6. **MT órfã**: Alguma MT não é referenciada por nenhum TC

---

## 10. Critério de Pronto

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

## 11. Próximo Contrato

Após conclusão deste contrato, a documentação de testes está completa (MT + TC).

O próximo passo é:

> **CONTRATO-EXECUCAO-BACKEND** ou **CONTRATO-EXECUCAO-FRONTEND** (para implementação)
>
> ```
> Conforme CONTRATO-EXECUCAO-BACKEND para RFXXX.
> Seguir D:\IC2\CLAUDE.md.
> ```

---

## 12. Arquivos Relacionados

| Arquivo | Descrição |
|---------|-----------|
| `contracts/documentacao/CONTRATO-GERACAO-DOCS-TC.md` | Este contrato |
| `checklists/checklist-documentacao-tc.yaml` | Checklist YAML |
| `templates/TC.yaml` | Template do TC |
| `templates/STATUS.yaml` | Template STATUS estruturado |

---

## 13. Histórico de Versões

| Versão | Data | Descrição |
|--------|------|-----------|
| 2.2 | 2026-01-11 | Adicionada Fase 1.4 "Identificar Tipo de Teste E2E" e Fase 2.2 "Documentar TC Stateful" - Identifica se RF requer testes STATEFUL (CRUD completo, fluxos sequenciais) ou ISOLATED durante criação do TC. TCs stateful DEVEM documentar: tipo_teste, requisitos_playwright (workers: 1, fullyParallel: false, retries: 0), fixtures_necessarias, e TCs E2E com usa_fixture, fixture_dependencia, sequencia. Referência obrigatória: CONTRATO-TESTES-E2E-STATEFUL.md. Baseado em análise RF006 (67% dos problemas por configuração incorreta). Resolve gap arquitetural: TC agora conhece stateful DURANTE criação, não apenas execução. |
| 2.1 | 2026-01-09 | Adicionada seção 6 "Validação de UC com Especificações de Teste" (BLOQUEANTE) - Valida que UC possui navegacao, credenciais, data-test em TODOS passos, estados_ui, tabela/formulario (se aplicável), performance, timeouts_e2e ANTES de criar TC. Renumeradas seções 6→7, 7→8, 8→9, 9→10, 10→11, 11→12, 12→13, 13→14. Baseado em análise RF006. Referência: CLAUDE.md seção 18.2.2 |
| 2.0 | 2025-12-31 | **UPGRADE CRÍTICO:** Ordem execução bloqueante (MT validado obrigatório), IDs canônicos TC-RFXXX-[CAT]-NNN, vínculo CA obrigatório, regras priorização por categoria, política E2E obrigatória, granularidade mínima TCs, validação ciclo completo RF→UC→MT→TC |
| 1.0 | 2025-12-31 | Criação do contrato separado (TC depois de MT, TC depois de UC) |

---

## 14. REGRA DE NEGAÇÃO ZERO

Se uma solicitação:
- não estiver explicitamente prevista no contrato ativo, ou
- conflitar com qualquer regra do contrato

ENTÃO:

- A execução DEVE ser NEGADA
- Nenhuma ação parcial pode ser realizada
- Nenhum "adiantamento" é permitido

---

**FIM DO CONTRATO**
