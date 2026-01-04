# CONTRATO DE GERAÇÃO MT + TC (MASSA DE TESTE + CASOS DE TESTE)

**Versão:** 3.0
**Data:** 2026-01-02
**Status:** Ativo
**Changelog v3.0:** Consolidação MT e TC em único contrato, validação backend+frontend 100%, ordem sequencial bloqueante, rastreabilidade completa RF→UC→MT→TC

---

## 📋 SUMÁRIO EXECUTIVO

### ⚡ O que este contrato faz

Este contrato gera **Massa de Teste (MT) e Casos de Teste (TC)** de forma INTEGRADA e SEQUENCIAL, garantindo:

- ✅ **Backend + Frontend Prontos**: Só executa se ambos 100% aprovados
- ✅ **Dados Reais**: MT usa payloads reais do backend e estados reais do frontend
- ✅ **Cobertura Total (100%)**: MT e TC cobrem 100% dos UCs
- ✅ **Rastreabilidade Completa**: RF → UC → MT → TC
- ✅ **E2E Ready**: TC-E2E preparados para geração de specs Playwright
- ✅ **Segurança Completa**: Cobertura obrigatória de autenticação, autorização, multi-tenancy
- ✅ **Validação Automática**: Checklists executados após criação

### 📁 Arquivos Gerados

1. **MT-RF[XXX].yaml** - Massa de Teste (dados reais para testes)
2. **TC-RF[XXX].yaml** - Casos de Teste (cenários completos)
3. **STATUS.yaml** - Atualização de governança (documentacao.mt = true, documentacao.tc = true)

### 🎯 Por que MT e TC DEPOIS de Backend + Frontend?

**JUSTIFICATIVA TÉCNICA OBRIGATÓRIA:**

1. **MT precisa de DADOS REAIS:**
   - MT define payloads enviados ao backend → precisa conhecer contratos de API (DTOs, validações)
   - MT define respostas esperadas → precisa conhecer estrutura de resposta real
   - MT define estados renderizados → precisa conhecer estados do frontend (Loading, Vazio, Erro)
   - ❌ Criar MT antes = inventar dados = retrabalho garantido quando backend/frontend mudarem

2. **TC precisa de FLUXOS COMPLETOS:**
   - TC-E2E simula usuário real (clicar botão, preencher form, ver resposta na tela)
   - TC valida 4 estados obrigatórios: Padrão, Loading, Vazio, Erro (só existem no frontend)
   - TC precisa conhecer: endpoints disponíveis, componentes Angular renderizados, estados possíveis
   - ❌ Criar TC antes = fluxos imaginários = retrabalho garantido

3. **RASTREABILIDADE COMPLETA:**
   - MT e TC testam integração backend + frontend
   - Se backend mudar depois, MT/TC desalinham (quebra testes)
   - Se frontend mudar depois, MT/TC desalinham (quebra testes)
   - ✅ SOMENTE com ambos prontos, MT/TC refletem sistema REAL

### ⚠️ REGRA CRÍTICA

**Pré-requisitos BLOQUEANTES (se falhar, PARAR imediatamente):**
- Backend DEVE estar 100% aprovado (desenvolvimento.backend.conformidade = "100%")
- Frontend DEVE estar 100% aprovado (desenvolvimento.frontend.conformidade = "100%")
- UC-RFXXX.md DEVE existir e estar validado
- UC-RFXXX.yaml DEVE existir e estar sincronizado

**Se QUALQUER pré-requisito falhar, a execução é BLOQUEADA.**

---

## 1. Identificação do Agente

| Campo | Valor |
|-------|-------|
| **Papel** | Agente Gerador de Massa de Teste e Casos de Teste |
| **Escopo** | Criação completa de MT-RF[XXX].yaml e TC-RF[XXX].yaml |
| **Modo** | Documentação (sem alteração de código backend/frontend) |

---

## 2. Ativação do Contrato

Este contrato é ativado quando a solicitação mencionar explicitamente:

> **"Conforme CONTRATO-GERACAO-DOCS-MT-TC para RFXXX"**

Exemplo:
```
Conforme CONTRATO-GERACAO-DOCS-MT-TC para RF006.
Seguir CLAUDE.md.
```

---

## 3. PRÉ-REQUISITOS OBRIGATÓRIOS (BLOQUEANTES)

Antes de QUALQUER ação, o agente DEVE validar:

### 3.1 Documentação Base

| Pré-requisito | Validação | Bloqueante |
|---------------|-----------|------------|
| UC-RFXXX.md | Deve existir e estar validado | Sim |
| UC-RFXXX.yaml | Deve existir e estar sincronizado com .md | Sim |
| STATUS.yaml | documentacao.uc = true | Sim |
| Templates MT.yaml e TC.yaml | Devem existir em D:\IC2\docs\templates\ | Sim |

### 3.2 Backend e Frontend APROVADOS 100%

| Pré-requisito | Validação | Bloqueante |
|---------------|-----------|------------|
| Backend aprovado | desenvolvimento.backend.conformidade = "100%" | Sim |
| Frontend aprovado | desenvolvimento.frontend.conformidade = "100%" | Sim |

**REGRA DE BLOQUEIO:**
- Se backend < 100%: PARAR, REPROVAR, AVISAR usuário
- Se frontend < 100%: PARAR, REPROVAR, AVISAR usuário
- Motivo: MT e TC precisam de dados REAIS, não inventados

### 3.3 Validação de Pré-requisitos (Algoritmo)

```
1. Ler STATUS.yaml do RFXXX
2. Verificar desenvolvimento.backend.conformidade
   - Se != "100%": BLOQUEAR execução
   - Mensagem: "Backend não aprovado 100%. MT e TC precisam de backend pronto."
3. Verificar desenvolvimento.frontend.conformidade
   - Se != "100%": BLOQUEAR execução
   - Mensagem: "Frontend não aprovado 100%. MT e TC precisam de frontend pronto."
4. Verificar documentacao.uc
   - Se != true: BLOQUEAR execução
   - Mensagem: "UC não validado. MT e TC precisam de UC completo."
5. Se TODOS passarem: Prosseguir para geração de MT
```

---

## 4. WORKFLOW OBRIGATÓRIO (ORDEM SEQUENCIAL)

**REGRA DE EXECUÇÃO:** MT ANTES de TC. TC depende de MT.

### FASE 1: Geração de MT-RF[XXX].yaml

1. **Ler documentação base:**
   - Ler UC-RFXXX.md completamente
   - Ler UC-RFXXX.yaml completamente
   - Identificar TODOS os cenários (FP, FA, FE)
   - Mapear Critérios de Aceite (CA)

2. **Analisar backend implementado:**
   - Ler DTOs (Commands, Queries, Responses)
   - Ler validações (FluentValidation)
   - Ler regras de negócio (Domain)
   - Identificar payloads REAIS

3. **Analisar frontend implementado:**
   - Ler componentes Angular
   - Ler estados renderizados (Loading, Empty, Error)
   - Ler validações de formulário
   - Identificar fluxos de UI REAIS

4. **Criar MT-RF[XXX].yaml:**
   - Usar template D:\IC2\docs\templates\MT.yaml
   - Criar massas para TODAS as categorias obrigatórias:
     - SUCESSO (MT-RF[XXX]-001 a 099)
     - VALIDACAO (MT-RF[XXX]-100 a 199)
     - SEGURANCA (MT-RF[XXX]-400 a 499)
     - MULTI_TENANCY (MT-RF[XXX]-700 a 799)
     - AUDITORIA (MT-RF[XXX]-800 a 899)
     - INTEGRACAO (MT-RF[XXX]-900 a 999)
   - Garantir rastreabilidade UC → MT
   - Incluir ca_ref para cada CA

5. **Validar MT via checklist:**
   - Executar D:\IC2\docs\checklists\documentacao\checklist-documentacao-mt.yaml
   - Se REPROVAR: CORRIGIR e re-validar
   - Se APROVAR: Prosseguir para TC

6. **Atualizar STATUS.yaml:**
   ```yaml
   documentacao:
     mt: true
     mt_observacoes: "MT criado com cobertura 100% de cenários UC"
   ```

### FASE 2: Geração de TC-RF[XXX].yaml

1. **Ler MT-RF[XXX].yaml criado:**
   - Mapear TODAS as massas criadas
   - Identificar categorias
   - Preparar referências MT

2. **Criar TC-RF[XXX].yaml:**
   - Usar template D:\IC2\docs\templates\TC.yaml
   - Criar casos para TODAS as categorias obrigatórias:
     - HAPPY_PATH (TC-RF[XXX]-HP-NNN)
     - VALIDACAO (TC-RF[XXX]-VAL-NNN)
     - SEGURANCA (TC-RF[XXX]-SEC-NNN)
     - EDGE_CASE (TC-RF[XXX]-EDGE-NNN)
     - AUDITORIA (TC-RF[XXX]-AUD-NNN)
     - INTEGRACAO (TC-RF[XXX]-INT-NNN)
     - E2E (TC-RF[XXX]-E2E-NNN) ⚠️ OBRIGATÓRIO para CRUD
   - Garantir rastreabilidade UC → MT → TC
   - Vincular TODOS os TCs a CAs (origem.criterios_aceite)
   - Referenciar MTs correspondentes (massa_teste.referencias)

3. **Validar TC via checklist:**
   - Executar D:\IC2\docs\checklists\documentacao\checklist-documentacao-tc.yaml
   - Se REPROVAR: CORRIGIR e re-validar
   - Se APROVAR: Concluir

4. **Atualizar STATUS.yaml:**
   ```yaml
   documentacao:
     tc: true
     tc_observacoes: "TC criado com cobertura 100% de UCs e rastreabilidade completa"
   ```

---

## 5. ESTRUTURA DE ARQUIVOS (OBRIGATÓRIA)

```
D:\IC2\docs\rf\[FASE]\[EPIC]\[RFXXX]\
├── RF[XXX].yaml
├── UC-RF[XXX].md
├── UC-RF[XXX].yaml
├── MT-RF[XXX].yaml               ⚠️ CRIAR AQUI (FASE 1)
├── TC-RF[XXX].yaml               ⚠️ CRIAR AQUI (FASE 2)
├── RL-RF[XXX].yaml
└── STATUS.yaml                   ⚠️ ATUALIZAR (mt: true, tc: true)
```

**Exemplo para RF006:**
```
D:\IC2\docs\rf\Fase-1-Sistema-Base\EPIC001-SYS-Sistema-Infraestrutura\RF006-Gestao-de-Clientes\
├── MT-RF006.yaml                 ⚠️ CRIAR AQUI
├── TC-RF006.yaml                 ⚠️ CRIAR AQUI
└── STATUS.yaml                   ⚠️ ATUALIZAR
```

---

## 6. NOMENCLATURA OBRIGATÓRIA

### 6.1 Arquivos

- **MT:** MT-RF[XXX].yaml (não MT-RFXXX.yaml)
- **TC:** TC-RF[XXX].yaml (não TC-RFXXX.yaml)

### 6.2 IDs Canônicos

**MT (Massa de Teste):**
```
MT-RF[XXX]-[NNN]

Exemplos:
- MT-RF006-001 (sucesso - criação completa)
- MT-RF006-100 (validação - campo obrigatório ausente)
- MT-RF006-400 (segurança - usuário não autenticado)
- MT-RF006-700 (multi-tenancy - isolamento entre tenants)
- MT-RF006-800 (auditoria - created_by preenchido)
```

**TC (Casos de Teste):**
```
TC-RF[XXX]-[CAT]-[NNN]

Exemplos:
- TC-RF006-HP-001 (happy path - criação bem-sucedida)
- TC-RF006-VAL-001 (validação - campo obrigatório)
- TC-RF006-SEC-001 (segurança - não autenticado)
- TC-RF006-E2E-001 (e2e - fluxo completo CRUD)
```

---

## 7. CATEGORIAS OBRIGATÓRIAS

### 7.1 MT (Massa de Teste)

| Categoria | Faixa IDs | Obrigatória | Mínimo | Exemplos |
|-----------|-----------|-------------|--------|----------|
| SUCESSO | 001-099 | Sim | 1 | Criação válida, edição válida, consulta válida |
| VALIDACAO_OBRIGATORIO | 100-199 | Sim | 1 por campo obrigatório | Campo ausente, null quando obrigatório |
| VALIDACAO_FORMATO | 200-299 | Sim | 1 por campo formatado | Email inválido, CPF inválido, data inválida |
| REGRA_NEGOCIO | 300-399 | Sim | 1 por regra | Duplicação, violação de unicidade, limites de negócio |
| AUTORIZACAO | 400-499 | Sim | 2 (401 + 403) | Não autenticado (401), sem permissão (403) |
| EDGE_CASE | 500-599 | Sim | 1 por campo | Tamanho máximo, valores limite, caracteres especiais |
| MULTI_TENANCY | 700-799 | Sim (CRUD) | 1 | Isolamento entre tenants, tentativa acesso outro tenant |
| AUDITORIA | 800-899 | Sim (CRUD) | 1 | created_by, updated_by, created_at, updated_at |
| INTEGRACAO | 900-999 | Sim | 1 por FK | FK inválida, integridade referencial, constraint violada |

**REGRA CRÍTICA:** TODAS as categorias são obrigatórias. "Mínimo" indica quantidade mínima de MTs por categoria.

### 7.2 TC (Casos de Teste)

| Categoria | Código | Obrigatória | Mínimo | Prioridade Padrão | Exemplos |
|-----------|--------|-------------|--------|-------------------|----------|
| HAPPY_PATH | HP | Sim | 1 por UC | CRITICA | Fluxo principal de sucesso FP-UCXX completo |
| VALIDACAO | VAL | Sim | 1 por validação | CRITICA (campos obrigatórios) | Campo obrigatório, formato inválido |
| SEGURANCA | SEC | Sim | 2 (401 + 403) | CRITICA | Não autenticado (401), sem permissão (403) |
| EDGE_CASE | EDGE | Sim | 1 por campo | ALTA | Tamanho máximo, valores limite, casos extremos |
| AUDITORIA | AUD | Sim (CRUD) | 1 | ALTA | Auditoria de criação, atualização, exclusão |
| INTEGRACAO | INT | Sim | 1 por FK | ALTA | FK inválida, integridade referencial |
| E2E | E2E | Sim (CRUD) | 1 completo | CRITICA | Fluxo CRUD completo (criar → consultar → editar → excluir) |

**REGRA CRÍTICA:** TODAS as categorias são obrigatórias. "Mínimo" indica quantidade mínima de TCs por categoria.

---

## 8. VALIDAÇÕES OBRIGATÓRIAS

### 8.1 Cobertura 100% ABSOLUTA (REGRA CRÍTICA)

**PRINCÍPIO FUNDAMENTAL:** Cobertura TOTAL significa ZERO cenários sem MT/TC.

**MT (Massa de Teste) - Cobertura OBRIGATÓRIA:**

1. **TODOS os Fluxos do UC (100%):**
   - ✅ Fluxo Principal (FP): TODOS os passos FP-UCXX-NNN devem ter MT
   - ✅ Fluxos Alternativos (FA): TODOS os passos FA-UCXX-NNN devem ter MT
   - ✅ Fluxos de Exceção (FE): TODOS os passos FE-UCXX-NNN devem ter MT
   - ❌ NENHUM fluxo pode ficar sem MT

2. **TODOS os Critérios de Aceite (100%):**
   - ✅ TODOS os CA-UCXX-NNN devem ter MT vinculado (ca_ref)
   - ❌ NENHUM CA pode ficar sem MT

3. **TODAS as Validações (100%):**
   - ✅ Campos obrigatórios (TODOS)
   - ✅ Formatos (email, CPF, data, etc - TODOS)
   - ✅ Ranges (min, max - TODOS)
   - ✅ Regras de negócio (duplicação, unicidade - TODAS)

4. **TODOS os Cenários de Segurança (100%):**
   - ✅ Não autenticado
   - ✅ Sem permissão
   - ✅ Multi-tenancy (isolamento entre tenants)
   - ✅ Tentativa de acesso a dados de outro tenant

5. **TODOS os Cenários de Auditoria (100% - CRUD):**
   - ✅ created_by preenchido
   - ✅ updated_by preenchido
   - ✅ created_at preenchido
   - ✅ updated_at preenchido

6. **TODOS os Edge Cases (100%):**
   - ✅ Tamanho máximo de campos
   - ✅ Valores limite (0, -1, MAX_INT)
   - ✅ Caracteres especiais
   - ✅ Unicode / emojis
   - ✅ Strings vazias vs null

**TC (Casos de Teste) - Cobertura OBRIGATÓRIA:**

1. **TODOS os UCs (100%):**
   - ✅ CADA UC deve ter pelo menos um TC
   - ❌ NENHUM UC pode ficar sem TC

2. **TODOS os uc_items (100%):**
   - ✅ CADA uc_item (passo granular) deve estar coberto
   - ✅ Exemplo: Se UC01 tem uc_items UC01-FP-01 a UC01-FP-10, TODOS devem estar em covers.uc_items
   - ❌ NENHUM uc_item pode ficar sem cobertura

3. **TODOS os Critérios de Aceite (100%):**
   - ✅ CADA CA deve ter pelo menos um TC correspondente
   - ✅ TC deve listar CA em origem.criterios_aceite
   - ❌ NENHUM CA pode ficar sem TC

4. **TODOS os Fluxos (100%):**
   - ✅ Fluxo Principal (FP): Pelo menos um TC-HP (Happy Path)
   - ✅ Fluxos Alternativos (FA): TC-VAL ou TC-EDGE
   - ✅ Fluxos de Exceção (FE): TC-VAL, TC-SEC, TC-EDGE

5. **TODAS as Categorias Obrigatórias (100%):**
   - ✅ HAPPY_PATH: Pelo menos 1 (caminho feliz completo)
   - ✅ VALIDACAO: Pelo menos 1 (campo obrigatório, formato, etc)
   - ✅ SEGURANCA: Pelo menos 1 (não autenticado, sem permissão)
   - ✅ EDGE_CASE: Pelo menos 1 (limites, casos extremos)
   - ✅ AUDITORIA: Pelo menos 1 (CRUD obrigatório)
   - ✅ E2E: Pelo menos 1 (CRUD obrigatório - fluxo completo)

6. **TODAS as Referências MT (100%):**
   - ✅ CADA TC deve referenciar MT correspondente (massa_teste.referencias)
   - ❌ NENHUM TC sem referência MT
   - ❌ NENHUMA referência MT inválida (MT inexistente)

### 8.2 IDs Canônicos

**MT:**
- ✅ Formato: MT-RF[XXX]-[NNN]
- ❌ Sem duplicados
- ❌ Sem IDs inválidos (MT-001, MT-RFXXX-1, etc)

**TC:**
- ✅ Formato: TC-RF[XXX]-[CAT]-[NNN]
- ❌ Sem duplicados
- ❌ Sem IDs inválidos (TC-HP-001, TC-RFXXX-HP-1, etc)

### 8.3 Rastreabilidade Completa

**MT:**
```yaml
data_sets:
  MT-RF006-001:
    categoria: "SUCESSO"
    descricao: "Criação com dados válidos completos"

    # ⚠️ OBRIGATÓRIO: Rastreabilidade ao UC
    ca_ref: "CA-UC01-001"  # Se CA existe

    contexto:
      autenticacao:
        usuario_id: 1
        tenant_id: 1
        permissoes: ["cliente.create"]
```

**TC:**
```yaml
test_cases:
  TC-RF006-HP-001:
    categoria: "HAPPY_PATH"
    prioridade: "CRITICA"

    uc_ref: "UC01"

    # ⚠️ OBRIGATÓRIO: Cobertura de uc_items
    covers:
      uc_items:
        - "UC01-FP-01"
        - "UC01-FP-05"

    # ⚠️ OBRIGATÓRIO: Vínculo com CA
    origem:
      criterios_aceite: ["CA-UC01-001", "CA-UC01-002"]
      ucs: ["UC01"]
      fluxos_uc: ["FP-UC01-001", "FP-UC01-005"]

    # ⚠️ OBRIGATÓRIO: Referência a MT
    massa_teste:
      referencias: ["MT-RF006-001"]
```

### 8.4 Matriz de Rastreabilidade

**OBRIGATÓRIO ao final de TC-RF[XXX].yaml:**

```yaml
rastreabilidade:
  - tc: "TC-RF006-HP-001"
    ucs: ["UC01"]
    massas: ["MT-RF006-001"]
  - tc: "TC-RF006-VAL-001"
    ucs: ["UC01"]
    massas: ["MT-RF006-100"]
  # ... (TODOS os TCs devem estar listados)
```

---

## 9. NEGAÇÃO DE INFERÊNCIA

**PROIBIDO:**
- ❌ Criar MT com cenário NÃO explicitado no UC
- ❌ Criar TC com validação NÃO documentada
- ❌ Inventar regras de negócio
- ❌ Assumir comportamento implícito

**PERMITIDO:**
- ✅ Criar MT/TC para cenários explícitos no UC
- ✅ Criar MT/TC para validações documentadas no UC
- ✅ Criar MT/TC para regras de negócio do UC

**Se houver dúvida sobre algum cenário:**
- PARAR e QUESTIONAR ao usuário
- NÃO prosseguir com inferência

---

## 10. CRITÉRIO DE PRONTO (0% ou 100%)

**MT-RF[XXX].yaml:**
- ✅ APROVADO: Cobertura 100%, IDs válidos, rastreabilidade completa, categorias OK, ca_ref OK
- ❌ REPROVADO: QUALQUER item acima falhar

**TC-RF[XXX].yaml:**
- ✅ APROVADO: Cobertura 100%, IDs válidos, rastreabilidade completa, categorias OK, vinculo CA OK
- ❌ REPROVADO: QUALQUER item acima falhar

**NÃO EXISTE APROVAÇÃO COM RESSALVAS.**

---

## 11. AUTONOMIA TOTAL DO AGENTE

O agente DEVE:
- ✅ Validar pré-requisitos (backend 100%, frontend 100%) AUTOMATICAMENTE
- ✅ Criar MT-RF[XXX].yaml AUTOMATICAMENTE
- ✅ Executar checklist de validação de MT AUTOMATICAMENTE
- ✅ Criar TC-RF[XXX].yaml AUTOMATICAMENTE
- ✅ Executar checklist de validação de TC AUTOMATICAMENTE
- ✅ Atualizar STATUS.yaml AUTOMATICAMENTE
- ✅ Identificar gaps e REPROVAR se cobertura < 100%

O agente NÃO DEVE:
- ❌ Perguntar se pode criar MT ou TC
- ❌ Esperar usuário validar intermediariamente
- ❌ Aprovar com ressalvas
- ❌ Prosseguir se checklist reprovar

---

## 12. EXPORTAÇÃO PARA AZURE TEST PLANS (OBRIGATÓRIO)

### 12.1 Arquivos Azure DevOps Obrigatórios

Após criar e validar MT-RF[XXX].yaml e TC-RF[XXX].yaml, o agente DEVE gerar:

**Arquivo 1: `azure-test-cases-RF[XXX].csv`**
- Formato: CSV compatível com Azure Test Plans
- Localização: `docs/rf/[FASE]/[EPIC]/[RFXXX]/azure-test-cases-RF[XXX].csv`
- Propósito: Importação direta no Azure DevOps Test Plans

**Arquivo 2: `azure-test-suites-RF[XXX].json`**
- Formato: JSON compatível com Azure DevOps API
- Localização: `docs/rf/[FASE]/[EPIC]/[RFXXX]/azure-test-suites-RF[XXX].json`
- Propósito: Criação automática de Test Suites via API

### 12.2 Estrutura do CSV (azure-test-cases-RF[XXX].csv)

```csv
ID,Title,Area,Iteration,State,Assigned To,Priority,Automation Status,Steps,Expected Result,Test Suite,Tags,Work Item Type,UC Reference,MT Reference
TC-RF006-HP-001,UC01 - Criar Cliente com ReceitaWS e dados completos,IControlIT\Cadastros,Fase-1-Sistema-Base,Design,QA Team,1,Planned,"1. Acessar tela de Clientes|2. Clicar em 'Novo Cliente'|3. Preencher CNPJ e consultar ReceitaWS|4. Preencher dados adicionais|5. Clicar em 'Salvar'","Cliente criado com sucesso|HTTP 201|Auditoria registrada (CLI_CREATE)|Logo exibido se disponível",RF006-HAPPY_PATH,"e2e;happy-path;rf006;uc01",Test Case,UC01,MT-RF006-001
TC-RF006-VAL-001,UC01 - CNPJ ausente (campo obrigatório),IControlIT\Cadastros,Fase-1-Sistema-Base,Design,QA Team,1,Planned,"1. Acessar tela de Clientes|2. Clicar em 'Novo Cliente'|3. Deixar CNPJ vazio|4. Preencher Razão Social|5. Clicar em 'Salvar'","Erro de validação exibido|Mensagem: 'CNPJ é obrigatório'|HTTP 422|Nenhum registro criado",RF006-VALIDACAO,"validacao;campo-obrigatorio;rf006;uc01",Test Case,UC01,MT-RF006-100
```

**Colunas obrigatórias:**
1. **ID**: TC-RF[XXX]-[CAT]-[NNN]
2. **Title**: Descrição resumida do TC (descricao.resumo do YAML)
3. **Area**: IControlIT\[Módulo] (extrair do RF)
4. **Iteration**: Fase do EPIC (ex: Fase-1-Sistema-Base)
5. **State**: Design (padrão inicial)
6. **Assigned To**: QA Team (padrão inicial)
7. **Priority**: 1 (CRITICA), 2 (ALTA), 3 (MEDIA)
8. **Automation Status**: Planned (todos TCs E2E), Not Planned (TCs manuais)
9. **Steps**: Passos do teste separados por "|" (pipe)
10. **Expected Result**: Resultado esperado do TC
11. **Test Suite**: Nome da suite (RF[XXX]-[CATEGORIA])
12. **Tags**: Tags separadas por ";" (categoria;rf;uc)
13. **Work Item Type**: Test Case (fixo)
14. **UC Reference**: UC relacionado (uc_ref do YAML)
15. **MT Reference**: MT relacionada (massa_teste.referencias[0] do YAML)

### 12.3 Estrutura do JSON (azure-test-suites-RF[XXX].json)

```json
{
  "rf": "RF006",
  "titulo": "Gestão de Clientes (Multi-Tenancy SaaS)",
  "area": "IControlIT\\Cadastros",
  "iteration": "Fase-1-Sistema-Base\\EPIC001-SYS-Sistema-Infraestrutura",
  "test_plan_name": "RF006 - Gestão de Clientes",
  "suites": [
    {
      "suite_name": "RF006-HAPPY_PATH",
      "suite_type": "StaticTestSuite",
      "parent_suite": "RF006 - Gestão de Clientes",
      "test_cases": ["TC-RF006-HP-001", "TC-RF006-HP-002", "TC-RF006-HP-003", "TC-RF006-HP-004", "TC-RF006-HP-005", "TC-RF006-HP-006", "TC-RF006-HP-007", "TC-RF006-HP-008", "TC-RF006-HP-009"]
    },
    {
      "suite_name": "RF006-VALIDACAO",
      "suite_type": "StaticTestSuite",
      "parent_suite": "RF006 - Gestão de Clientes",
      "test_cases": ["TC-RF006-VAL-001", "TC-RF006-VAL-002", "TC-RF006-VAL-003", "TC-RF006-VAL-004", "TC-RF006-VAL-005"]
    },
    {
      "suite_name": "RF006-SEGURANCA",
      "suite_type": "StaticTestSuite",
      "parent_suite": "RF006 - Gestão de Clientes",
      "test_cases": ["TC-RF006-SEC-001", "TC-RF006-SEC-002", "TC-RF006-SEC-003"]
    },
    {
      "suite_name": "RF006-EDGE_CASE",
      "suite_type": "StaticTestSuite",
      "parent_suite": "RF006 - Gestão de Clientes",
      "test_cases": ["TC-RF006-EDGE-001", "TC-RF006-EDGE-002", "TC-RF006-EDGE-003", "TC-RF006-EDGE-004", "TC-RF006-EDGE-005"]
    },
    {
      "suite_name": "RF006-AUDITORIA",
      "suite_type": "StaticTestSuite",
      "parent_suite": "RF006 - Gestão de Clientes",
      "test_cases": ["TC-RF006-AUD-001", "TC-RF006-AUD-002", "TC-RF006-AUD-003"]
    },
    {
      "suite_name": "RF006-INTEGRACAO",
      "suite_type": "StaticTestSuite",
      "parent_suite": "RF006 - Gestão de Clientes",
      "test_cases": ["TC-RF006-INT-001", "TC-RF006-INT-002", "TC-RF006-INT-003", "TC-RF006-INT-004"]
    },
    {
      "suite_name": "RF006-E2E",
      "suite_type": "StaticTestSuite",
      "parent_suite": "RF006 - Gestão de Clientes",
      "test_cases": ["TC-RF006-E2E-001", "TC-RF006-E2E-002", "TC-RF006-E2E-003"]
    }
  ],
  "total_test_cases": 45,
  "total_suites": 7
}
```

### 12.4 Mapeamento de Prioridade

| Prioridade TC (YAML) | Priority Azure DevOps | Automation Status |
|----------------------|----------------------|-------------------|
| CRITICA | 1 | Planned (se E2E), Not Planned (outros) |
| ALTA | 2 | Planned (se E2E), Not Planned (outros) |
| MEDIA | 3 | Not Planned |

### 12.5 Extração de Steps do TC

**Para TC-HP, TC-VAL, TC-SEC, TC-EDGE, TC-AUD, TC-INT:**
- Usar campo `acao.tipo` + `acao.endpoint`
- Gerar steps genéricos baseados na categoria

**Para TC-E2E:**
- Usar campo `passos` (array de objetos com passo, descricao, endpoint, esperado)
- Cada passo vira uma linha no CSV separada por "|"

Exemplo TC-RF006-E2E-001:
```
1. Criar Cliente com ReceitaWS (POST /api/clientes)|2. Listar Clientes (GET /api/clientes)|3. Visualizar detalhes (GET /api/clientes/{id})|4. Editar Nome Fantasia (PUT /api/clientes/{id})|5. Excluir Cliente (DELETE /api/clientes/{id})
```

### 12.6 Validação da Exportação

Após gerar os arquivos Azure, o agente DEVE validar:

1. **CSV:**
   - ✅ TODAS as 15 colunas presentes
   - ✅ TODOS os 45 TCs exportados
   - ✅ Nenhuma linha vazia ou com dados faltando
   - ✅ IDs válidos (TC-RF[XXX]-[CAT]-[NNN])
   - ✅ Steps formatados corretamente (separados por "|")

2. **JSON:**
   - ✅ TODAS as 7 suites presentes (HAPPY_PATH, VALIDACAO, SEGURANCA, EDGE_CASE, AUDITORIA, INTEGRACAO, E2E)
   - ✅ total_test_cases = soma de TCs em TC-RF[XXX].yaml
   - ✅ total_suites = 7
   - ✅ TODOS os TCs listados em alguma suite
   - ✅ Nenhum TC duplicado entre suites

3. **Atualizar STATUS.yaml:**
```yaml
testes:
  azure_devops:
    test_cases_exportados: true
    arquivo_csv: "azure-test-cases-RF006.csv"
    arquivo_json: "azure-test-suites-RF006.json"
    total_test_cases: 45
    total_suites: 7
    data_exportacao: "2026-01-02"
    pronto_importacao: true
```

---

## 13. RESPONSABILIDADE DO AGENTE

1. Validar pré-requisitos (backend 100%, frontend 100%, UC validado)
2. Ler UC-RFXXX.md e UC-RFXXX.yaml completamente
3. Analisar backend implementado (DTOs, validações, regras)
4. Analisar frontend implementado (componentes, estados, validações)
5. Criar MT-RF[XXX].yaml com dados REAIS
6. Executar checklist-documentacao-mt.yaml
7. Corrigir se reprovado e re-validar
8. Criar TC-RF[XXX].yaml com rastreabilidade completa
9. Executar checklist-documentacao-tc.yaml
10. Corrigir se reprovado e re-validar
11. **NOVO:** Gerar azure-test-cases-RF[XXX].csv (exportação CSV)
12. **NOVO:** Gerar azure-test-suites-RF[XXX].json (suites JSON)
13. **NOVO:** Validar arquivos Azure DevOps (CSV 15 colunas + JSON 7 suites)
14. **NOVO:** Atualizar STATUS.yaml (azure_devops.pronto_importacao = true)
11. Atualizar STATUS.yaml (mt: true, tc: true)
12. Declarar conclusão (MT + TC prontos 100%)

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
