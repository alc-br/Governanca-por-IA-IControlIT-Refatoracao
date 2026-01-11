# CONTRATO DE VALIDAÇÃO MT + TC (MASSA DE TESTE + CASOS DE TESTE)

**Versão:** 1.2
**Data:** 2026-01-11
**Status:** Ativo
**Changelog v1.2:** Adicionada validação 11 "Validar TC Stateful" na FASE 2 (TC) - Valida TCs stateful possuem: metadata.tipo_teste = "STATEFUL", contrato_teste_stateful ref, requisitos_playwright (workers: 1, fullyParallel: false, retries: 0), fixtures_necessarias, TCs E2E com usa_fixture, fixture_dependencia, sequencia ordenada. Resolve gap arquitetural: validação verifica stateful ANTES de execução
**Changelog v1.1:** Adicionada validação 10 "Validar Seletores E2E Especificados" na FASE 2 (TC) - Valida que TODOS os passos possuem seletor, seguem padrão [data-test='...'], possuem acao_e2e, e data-test batem com UC. Baseado em análise RF006. Referência: CLAUDE.md seção 18.2.2
**Changelog v1.0:** Criação do contrato de validação integrada de MT e TC com critério binário (0% ou 100%)

---

## 📋 SUMÁRIO EXECUTIVO

### ⚡ O que este contrato faz

Este contrato **VALIDA** MT-RF[XXX].yaml e TC-RF[XXX].yaml criados, garantindo:

- ✅ **Validação Sequencial**: MT validado 100% ANTES de TC
- ✅ **Cobertura Total (100%)**: MT cobre 100% dos cenários UC, TC cobre 100% dos UCs
- ✅ **Rastreabilidade Completa**: RF → UC → MT → TC sem gaps
- ✅ **IDs Canônicos**: Todos IDs válidos e sem duplicados
- ✅ **Categorias Obrigatórias**: Todas categorias preenchidas
- ✅ **Aprovação Binária**: 0% ou 100%, sem ressalvas

### 🎯 Critério de Aprovação

**MT-RF[XXX].yaml:**
- ✅ APROVADO: Cobertura 100%, IDs válidos, rastreabilidade completa, categorias OK, ca_ref OK
- ❌ REPROVADO: QUALQUER item acima falhar

**TC-RF[XXX].yaml:**
- ✅ APROVADO: Cobertura 100%, IDs válidos, rastreabilidade completa, categorias OK, vinculo CA OK, MT refs OK
- ❌ REPROVADO: QUALQUER item acima falhar

**NÃO EXISTE APROVAÇÃO COM RESSALVAS.**

---

## 1. Identificação do Agente

| Campo | Valor |
|-------|-------|
| **Papel** | Agente Validador de Massa de Teste e Casos de Teste |
| **Escopo** | Validação completa de MT-RF[XXX].yaml e TC-RF[XXX].yaml |
| **Modo** | Validação (não modifica arquivos, só APROVA ou REPROVA) |

---

## 2. Ativação do Contrato

Este contrato é ativado quando a solicitação mencionar explicitamente:

> **"Conforme CONTRATO-VALIDACAO-MT-TC para RFXXX"**

Exemplo:
```
Conforme CONTRATO-VALIDACAO-MT-TC para RF006.
Seguir D:\IC2\CLAUDE.md.
```

---

## 3. PRÉ-REQUISITOS OBRIGATÓRIOS (BLOQUEANTES)

Antes de QUALQUER ação, o agente DEVE validar:

| Pré-requisito | Validação | Bloqueante |
|---------------|-----------|------------|
| MT-RF[XXX].yaml | Deve existir | Sim |
| TC-RF[XXX].yaml | Deve existir | Sim |
| UC-RFXXX.md | Deve existir (para validar cobertura) | Sim |
| UC-RFXXX.yaml | Deve existir (para validar rastreabilidade) | Sim |
| STATUS.yaml | documentacao.uc = true | Sim |
| checklist-documentacao-mt.yaml | Deve existir em D:\IC2\docs\checklists\documentacao\ | Sim |
| checklist-documentacao-tc.yaml | Deve existir em D:\IC2\docs\checklists\documentacao\ | Sim |

**REGRA DE BLOQUEIO:**
- Se MT-RF[XXX].yaml ausente: PARAR, REPROVAR
- Se TC-RF[XXX].yaml ausente: PARAR, REPROVAR
- Se UC não validado: PARAR, REPROVAR

---

## 4. ORDEM DE VALIDAÇÃO (BLOQUEANTE)

**REGRA CRÍTICA:** MT ANTES de TC. Validação sequencial obrigatória.

### FASE 1: Validar MT-RF[XXX].yaml

1. **Ler documentação:**
   - Ler UC-RFXXX.md completamente
   - Ler UC-RFXXX.yaml completamente
   - Ler MT-RF[XXX].yaml completamente

2. **Executar checklist:**
   - Executar D:\IC2\docs\checklists\documentacao\checklist-documentacao-mt.yaml
   - Validar cada item do checklist

3. **Validar cobertura 100% ABSOLUTA:**

   **3.1 TODOS os Fluxos (FP, FA, FE):**
   - ✅ Verificar CADA FP-UCXX-NNN do UC tem MT
   - ✅ Verificar CADA FA-UCXX-NNN do UC tem MT
   - ✅ Verificar CADA FE-UCXX-NNN do UC tem MT
   - ❌ Se QUALQUER fluxo sem MT: REPROVAR

   **3.2 TODOS os Critérios de Aceite:**
   - ✅ Verificar CADA CA-UCXX-NNN tem MT vinculado (ca_ref)
   - ❌ Se QUALQUER CA sem MT: REPROVAR

   **3.3 TODAS as Validações:**
   - ✅ Campos obrigatórios: TODOS devem ter MT de ausência
   - ✅ Formatos: TODOS devem ter MT de formato inválido
   - ✅ Ranges: TODOS devem ter MT de valores fora do range
   - ✅ Regras de negócio: TODAS devem ter MT de violação
   - ❌ Se QUALQUER validação sem MT: REPROVAR

   **3.4 TODOS os Cenários de Segurança:**
   - ✅ MT para não autenticado (401) existe?
   - ✅ MT para sem permissão (403) existe?
   - ✅ MT para multi-tenancy (isolamento) existe?
   - ✅ MT para tentativa acesso outro tenant existe?
   - ❌ Se QUALQUER cenário de segurança sem MT: REPROVAR

   **3.5 TODOS os Cenários de Auditoria (CRUD):**
   - ✅ MT para created_by preenchido existe?
   - ✅ MT para updated_by preenchido existe?
   - ✅ MT para created_at preenchido existe?
   - ✅ MT para updated_at preenchido existe?
   - ❌ Se QUALQUER cenário de auditoria sem MT: REPROVAR

   **3.6 TODOS os Edge Cases:**
   - ✅ CADA campo tem MT para tamanho máximo?
   - ✅ CADA campo numérico tem MT para valores limite (0, -1, MAX)?
   - ✅ CADA campo texto tem MT para caracteres especiais?
   - ✅ CADA campo texto tem MT para unicode/emojis?
   - ✅ CADA campo tem MT para string vazia vs null?
   - ❌ Se QUALQUER edge case sem MT: REPROVAR

   **3.7 TODAS as Integrações:**
   - ✅ CADA FK tem MT para FK inválida?
   - ✅ CADA constraint tem MT para violação?
   - ❌ Se QUALQUER integração sem MT: REPROVAR

4. **Validar IDs canônicos:**
   - Formato: MT-RF[XXX]-[NNN]
   - Sem duplicados
   - Sem IDs inválidos

5. **Validar rastreabilidade:**
   - Seção rastreabilidade presente?
   - Matriz RF → UC → MT completa?
   - Todos MT possuem ca_ref (quando CA existir)?

6. **Validar categorias obrigatórias:**
   - SUCESSO (pelo menos 1)
   - VALIDACAO (pelo menos 1)
   - SEGURANCA (pelo menos 1)
   - AUDITORIA (pelo menos 1 - OBRIGATÓRIA para CRUD)
   - MULTI_TENANCY (pelo menos 1 - OBRIGATÓRIA para CRUD)

7. **Validar campos obrigatórios:**
   - contexto (autenticacao, estado_inicial)
   - entrada (dados enviados)
   - resultado_esperado (sucesso, http_status, resposta, banco)

8. **Validar negação de inferência:**
   - Nenhuma MT com cenário não explicitado no UC
   - Nenhuma validação inventada
   - Nenhuma regra de negócio não documentada

9. **Resultado FASE 1:**
   - ✅ APROVADO 100%: Prosseguir para FASE 2 (TC)
   - ❌ REPROVADO: PARAR, Gerar relatório de gaps, NÃO prosseguir

**SOMENTE prosseguir para FASE 2 se MT APROVADO 100%.**

### FASE 2: Validar TC-RF[XXX].yaml

1. **Ler documentação:**
   - Ler UC-RFXXX.md completamente
   - Ler UC-RFXXX.yaml completamente
   - Ler MT-RF[XXX].yaml completamente (já validado)
   - Ler TC-RF[XXX].yaml completamente

2. **Executar checklist:**
   - Executar D:\IC2\docs\checklists\documentacao\checklist-documentacao-tc.yaml
   - Validar cada item do checklist

3. **Validar cobertura 100% ABSOLUTA:**

   **3.1 TODOS os UCs:**
   - ✅ Verificar CADA UC tem pelo menos um TC
   - ❌ Se QUALQUER UC sem TC: REPROVAR

   **3.2 TODOS os uc_items (passos granulares):**
   - ✅ Listar TODOS os uc_items do UC-RFXXX.yaml
   - ✅ Verificar CADA uc_item está em covers.uc_items de algum TC
   - ❌ Se QUALQUER uc_item sem cobertura: REPROVAR

   **Exemplo de validação:**
   ```
   UC-RF006.yaml tem:
   - UC01-FP-01, UC01-FP-02, UC01-FP-03, UC01-FP-04, UC01-FP-05
   - UC01-FA-01, UC01-FA-02
   - UC01-FE-01, UC01-FE-02, UC01-FE-03

   TC-RF006.yaml DEVE ter:
   - TODOS esses uc_items listados em covers.uc_items de TCs
   ```

   **3.3 TODOS os Critérios de Aceite:**
   - ✅ Verificar CADA CA tem pelo menos um TC correspondente
   - ✅ Verificar TC lista CA em origem.criterios_aceite
   - ❌ Se QUALQUER CA sem TC: REPROVAR

   **3.4 TODOS os Fluxos:**
   - ✅ Fluxo Principal (FP): Tem TC-HP?
   - ✅ Fluxos Alternativos (FA): Tem TC-VAL ou TC-EDGE?
   - ✅ Fluxos de Exceção (FE): Tem TC-VAL, TC-SEC ou TC-EDGE?
   - ❌ Se QUALQUER fluxo sem TC: REPROVAR

   **3.5 TODAS as Categorias Obrigatórias:**
   - ✅ HAPPY_PATH: Pelo menos 1 TC-HP?
   - ✅ VALIDACAO: Pelo menos 1 TC-VAL?
   - ✅ SEGURANCA: Pelo menos 2 TC-SEC (401 + 403)?
   - ✅ EDGE_CASE: Pelo menos 1 TC-EDGE por campo?
   - ✅ AUDITORIA: Pelo menos 1 TC-AUD (CRUD)?
   - ✅ INTEGRACAO: Pelo menos 1 TC-INT por FK?
   - ✅ E2E: Pelo menos 1 TC-E2E completo (CRUD)?
   - ❌ Se QUALQUER categoria ausente: REPROVAR

   **3.6 TODAS as Referências MT:**
   - ✅ Verificar CADA TC tem massa_teste.referencias
   - ✅ Verificar TODAS as referências MT existem em MT-RF[XXX].yaml
   - ❌ Se QUALQUER TC sem referência MT: REPROVAR
   - ❌ Se QUALQUER referência MT inválida: REPROVAR

4. **Validar IDs canônicos:**
   - Formato: TC-RF[XXX]-[CAT]-[NNN]
   - Sem duplicados
   - Sem IDs inválidos

5. **Validar rastreabilidade:**
   - Matriz TC → UC → MT completa?
   - Todos TC possuem origem.criterios_aceite?
   - Todos TC possuem massa_teste.referencias?

6. **Validar categorias obrigatórias:**
   - HAPPY_PATH (pelo menos 1)
   - VALIDACAO (pelo menos 1)
   - SEGURANCA (pelo menos 1)
   - EDGE_CASE (se aplicável)
   - AUDITORIA (pelo menos 1 - OBRIGATÓRIA para CRUD)
   - INTEGRACAO (se aplicável)
   - E2E (pelo menos 1 - OBRIGATÓRIA para CRUD)

7. **Validar priorização correta:**
   - HAPPY_PATH = CRITICA
   - SEGURANCA >= ALTA (nunca BAIXA)
   - VALIDACAO (campo obrigatório) = CRITICA
   - E2E = CRITICA

8. **Validar vínculo CA obrigatório:**
   - Toda CA DEVE ter pelo menos um TC correspondente
   - CA sem TC = BLOQUEIO CRÍTICO

9. **Validar referências MT:**
   - Todos TC referenciam MT existentes (massa_teste.referencias)?
   - Nenhuma referência MT inválida?

10. **Validar Seletores E2E Especificados (NOVO - CRÍTICO):**

   **Versão:** 1.0
   **Data:** 2026-01-09
   **Contexto:** Adicionado após análise do RF006 para garantir que TC possui seletores E2E corretos ANTES de executar testes.

   **Objetivo:** Garantir que TC-RFXXX.yaml possui seletores E2E especificados para TODOS os passos, evitando falhas sistemáticas em testes E2E.

   ```python
   # 1. Ler TC-RFXXX.yaml
   tc_yaml = ler_yaml(f"TC-RF{rf}.yaml")

   # 2. Ler UC-RFXXX.yaml (para validar consistência)
   uc_yaml = ler_yaml(f"UC-RF{rf}.yaml")

   # 3. Validar TODOS os TCs possuem seletores E2E
   falhas_seletores = []

   for tc in tc_yaml["casos_teste"]:
       tc_id = tc["id"]
       passos = tc.get("passos", [])

       # 3.1 Validar que TC possui passos
       if not passos:
           falhas_seletores.append(f"{tc_id}: TC sem passos definidos")
           continue

       # 3.2 Validar que TODOS os passos possuem campo 'seletor'
       passos_sem_seletor = []
       for i, passo in enumerate(passos):
           if "seletor" not in passo:
               passos_sem_seletor.append(f"Passo {i+1}")

       if passos_sem_seletor:
           falhas_seletores.append(
               f"{tc_id}: Passos sem seletor: {', '.join(passos_sem_seletor)}"
           )

       # 3.3 Validar que TODOS os seletores seguem padrão [data-test='...']
       for i, passo in enumerate(passos):
           if "seletor" in passo:
               seletor = passo["seletor"]
               if not seletor.startswith("[data-test="):
                   falhas_seletores.append(
                       f"{tc_id}: Passo {i+1} com seletor fora do padrão: {seletor}"
                   )

       # 3.4 Validar que TODOS os passos possuem campo 'acao_e2e' (código Playwright)
       passos_sem_acao_e2e = []
       for i, passo in enumerate(passos):
           if "acao_e2e" not in passo:
               passos_sem_acao_e2e.append(f"Passo {i+1}")

       if passos_sem_acao_e2e:
           falhas_seletores.append(
               f"{tc_id}: Passos sem acao_e2e: {', '.join(passos_sem_acao_e2e)}"
           )

   # 4. Validar consistência com UC (data-test batem?)
   # Extrair TODOS data-test do UC
   data_tests_uc = set()
   passos_uc = uc_yaml.get("passos", [])
   for passo in passos_uc:
       if "elemento" in passo and "data_test" in passo["elemento"]:
           data_tests_uc.add(passo["elemento"]["data_test"])

   # Estados UI
   if "estados_ui" in uc_yaml:
       for estado, config in uc_yaml["estados_ui"].items():
           if "data_test" in config:
               data_tests_uc.add(config["data_test"])

   # Tabela
   if "tabela" in uc_yaml:
       if "data_test_container" in uc_yaml["tabela"]:
           data_tests_uc.add(uc_yaml["tabela"]["data_test_container"])
       if "data_test_row" in uc_yaml["tabela"]:
           data_tests_uc.add(uc_yaml["tabela"]["data_test_row"])

   # Formulário
   if "formulario" in uc_yaml:
       if "data_test_form" in uc_yaml["formulario"]:
           data_tests_uc.add(uc_yaml["formulario"]["data_test_form"])
       campos = uc_yaml["formulario"].get("campos", [])
       for campo in campos:
           if "data_test" in campo:
               data_tests_uc.add(campo["data_test"])

   # Extrair TODOS data-test do TC
   data_tests_tc = set()
   for tc in tc_yaml["casos_teste"]:
       passos = tc.get("passos", [])
       for passo in passos:
           if "seletor" in passo:
               seletor = passo["seletor"]
               # Extrair data-test de [data-test="RFXXX-xxx"]
               import re
               match = re.search(r'\[data-test=["\']([^"\']+)["\']\]', seletor)
               if match:
                   data_tests_tc.add(match.group(1))

   # 5. Validar que TC usa data-test do UC (não inventados)
   data_tests_invalidos = data_tests_tc - data_tests_uc
   if data_tests_invalidos:
       falhas_seletores.append(
           f"TC usando data-test NÃO documentados em UC: {data_tests_invalidos}"
       )

   # 6. Verificar aprovação
   if falhas_seletores:
       print("❌ TC REPROVADO - Seletores E2E ausentes/inconsistentes:")
       for falha in falhas_seletores:
           print(f"  - {falha}")
       REPROVAR()
   else:
       print("✅ TC com seletores E2E completos e consistentes com UC")
   ```

   **Critério de Aprovação:**
   - ✅ TODOS os TCs possuem passos
   - ✅ TODOS os passos possuem campo `seletor`
   - ✅ TODOS os seletores seguem padrão `[data-test='...']`
   - ✅ TODOS os passos possuem campo `acao_e2e` (código Playwright)
   - ✅ TODOS os data-test do TC estão documentados no UC
   - ✅ Nenhum data-test inventado (não presente em UC)

   **SE qualquer verificação FALHAR:**
   - ❌ TC REPROVADO (seletores ausentes/inconsistentes)
   - ❌ Reportar TCs e passos com problemas
   - ❌ BLOQUEIO: Não prosseguir para execução de testes

   **IMPORTANTE:** Esta validação garante que testes E2E terão seletores corretos, evitando falhas sistemáticas por seletores não encontrados (como ocorreu em 32 testes do RF006).

   **Referência:** `CLAUDE.md` seção 18.2.2 "Bloqueios Obrigatórios"

11. **Validar TC Stateful (SE APLICÁVEL):**

   **Versão:** 1.0
   **Data:** 2026-01-11
   **Contexto:** Adicionado após análise do RF006 para validar que TCs stateful estão documentados corretamente.

   **Objetivo:** Validar que TCs stateful possuem configuração e estrutura adequadas ANTES de execução de testes.

   ```python
   # 1. Ler TC-RFXXX.yaml
   tc_yaml = ler_yaml(f"TC-RF{rf}.yaml")

   # 2. Verificar se é stateful
   tipo_teste = tc_yaml.get("metadata", {}).get("tipo_teste", "ISOLATED")

   if tipo_teste == "STATEFUL":
       print("✅ TC identificado como STATEFUL - Validando configuração...")

       # 3. Validar metadata obrigatória
       falhas_stateful = []

       # 3.1 Validar referência ao contrato
       if "contrato_teste_stateful" not in tc_yaml["metadata"]:
           falhas_stateful.append("metadata.contrato_teste_stateful ausente")
       else:
           contrato_ref = tc_yaml["metadata"]["contrato_teste_stateful"]
           if "CONTRATO-TESTES-E2E-STATEFUL.md" not in contrato_ref:
               falhas_stateful.append(f"contrato_teste_stateful incorreto: {contrato_ref}")

       # 3.2 Validar requisitos_playwright
       if "requisitos_playwright" not in tc_yaml["metadata"]:
           falhas_stateful.append("metadata.requisitos_playwright ausente")
       else:
           req_pw = tc_yaml["metadata"]["requisitos_playwright"]

           if req_pw.get("workers") != 1:
               falhas_stateful.append(f"workers deve ser 1, encontrado: {req_pw.get('workers')}")

           if req_pw.get("fullyParallel") != False:
               falhas_stateful.append(f"fullyParallel deve ser false, encontrado: {req_pw.get('fullyParallel')}")

           if req_pw.get("retries") != 0:
               falhas_stateful.append(f"retries deve ser 0, encontrado: {req_pw.get('retries')}")

       # 3.3 Validar fixtures_necessarias
       if "fixtures_necessarias" not in tc_yaml["metadata"]:
           falhas_stateful.append("metadata.fixtures_necessarias ausente")
       else:
           fixtures = tc_yaml["metadata"]["fixtures_necessarias"]
           if not fixtures:
               falhas_stateful.append("fixtures_necessarias está vazia (deve ter pelo menos 1)")

           for fixture in fixtures:
               if "nome" not in fixture:
                   falhas_stateful.append(f"Fixture sem campo 'nome': {fixture}")
               if "tipo" not in fixture:
                   falhas_stateful.append(f"Fixture sem campo 'tipo': {fixture}")
               if "arquivo_fixture" not in fixture:
                   falhas_stateful.append(f"Fixture sem campo 'arquivo_fixture': {fixture}")

       # 4. Validar TCs E2E possuem campos stateful
       tcs_e2e = [tc for tc in tc_yaml["casos_teste"] if tc.get("categoria") == "E2E"]

       for tc in tcs_e2e:
           tc_id = tc["id"]

           # 4.1 Validar usa_fixture
           if "usa_fixture" not in tc or tc["usa_fixture"] != True:
               falhas_stateful.append(f"{tc_id}: Campo 'usa_fixture' ausente ou false")

           # 4.2 Validar fixture_dependencia
           if "fixture_dependencia" not in tc:
               falhas_stateful.append(f"{tc_id}: Campo 'fixture_dependencia' ausente")

           # 4.3 Validar sequencia
           if "sequencia" not in tc:
               falhas_stateful.append(f"{tc_id}: Campo 'sequencia' ausente (ordem de execução)")

           # 4.4 Validar pré-condições (opcional mas recomendado)
           if "pre_condicoes" not in tc:
               print(f"⚠️  {tc_id}: Campo 'pre_condicoes' ausente (recomendado)")

       # 5. Validar sequência está ordenada
       sequencias = [tc.get("sequencia", 0) for tc in tcs_e2e]
       if sequencias != sorted(sequencias):
           falhas_stateful.append(f"Sequências fora de ordem: {sequencias}")

       # 6. Verificar aprovação
       if falhas_stateful:
           print("❌ TC STATEFUL REPROVADO - Configuração incompleta/incorreta:")
           for falha in falhas_stateful:
               print(f"  - {falha}")
           REPROVAR()
       else:
           print("✅ TC STATEFUL com configuração completa e correta")
   else:
       print("✅ TC identificado como ISOLATED - Validação stateful N/A")
   ```

   **Critério de Aprovação (SE STATEFUL):**
   - ✅ `metadata.tipo_teste = "STATEFUL"`
   - ✅ `metadata.contrato_teste_stateful` referencia CONTRATO-TESTES-E2E-STATEFUL.md
   - ✅ `metadata.requisitos_playwright` com workers: 1, fullyParallel: false, retries: 0
   - ✅ `metadata.fixtures_necessarias` não está vazia
   - ✅ TODOS os TCs E2E possuem `usa_fixture: true`
   - ✅ TODOS os TCs E2E possuem `fixture_dependencia`
   - ✅ TODOS os TCs E2E possuem `sequencia`
   - ✅ Sequências estão ordenadas (1, 2, 3, 4)

   **SE qualquer verificação FALHAR:**
   - ❌ TC STATEFUL REPROVADO (configuração incompleta/incorreta)
   - ❌ Reportar gaps identificados
   - ❌ BLOQUEIO: Não prosseguir para execução de testes

   **IMPORTANTE:** Esta validação garante que testes stateful serão executados corretamente (workers: 1, serial, fixtures), evitando falhas sistemáticas por configuração incorreta (como 67% dos problemas do RF006).

   **Referência:** [CONTRATO-TESTES-E2E-STATEFUL.md](D:\IC2_Governanca\governanca\contracts\testes\CONTRATO-TESTES-E2E-STATEFUL.md) seção 2 (Configuração Obrigatória)

12. **Resultado FASE 2:**
    - ✅ APROVADO 100%: Validação concluída com sucesso
    - ❌ REPROVADO: Gerar relatório de gaps

---

## 5. VALIDAÇÕES OBRIGATÓRIAS (DETALHAMENTO)

### 5.1 Cobertura 100%

**MT-RF[XXX].yaml:**
- ✅ TODOS os fluxos (FP, FA, FE) do UC cobertos
- ✅ TODOS os cenários de teste têm MT correspondente
- ✅ TODAS as validações de campos têm MT
- ❌ Nenhum cenário UC sem MT
- ❌ Nenhuma MT órfã (sem rastreabilidade)

**TC-RF[XXX].yaml:**
- ✅ TODOS os UCs cobertos
- ✅ TODOS os uc_items (granulares) cobertos
- ✅ TODAS as categorias preenchidas
- ❌ Nenhum UC sem TC
- ❌ Nenhum TC órfão (sem rastreabilidade)

### 5.2 IDs Canônicos

**MT:**
```
✅ VÁLIDO:
- MT-RF006-001
- MT-RF006-100
- MT-RF006-700

❌ INVÁLIDO:
- MT-001            (falta RF006)
- MT-RF006-1        (falta zero à esquerda)
- MT-RFXXX-001      (placeholder não substituído)
```

**TC:**
```
✅ VÁLIDO:
- TC-RF006-HP-001
- TC-RF006-VAL-001
- TC-RF006-E2E-001

❌ INVÁLIDO:
- TC-HP-001         (falta RF006)
- TC-RF006-HP-1     (falta zero à esquerda)
- TC-RFXXX-HP-001   (placeholder não substituído)
```

### 5.3 Rastreabilidade Completa

**MT-RF[XXX].yaml deve ter:**
```yaml
data_sets:
  MT-RF006-001:
    categoria: "SUCESSO"
    descricao: "..."

    # ⚠️ OBRIGATÓRIO: Se CA existe
    ca_ref: "CA-UC01-001"

    contexto:
      # ⚠️ OBRIGATÓRIO
      autenticacao:
        usuario_id: 1
        tenant_id: 1
        permissoes: ["cliente.create"]

      # ⚠️ OBRIGATÓRIO
      estado_inicial:
        banco:
          clientes: []

    # ⚠️ OBRIGATÓRIO
    entrada:
      nome: "Cliente Teste"

    # ⚠️ OBRIGATÓRIO
    resultado_esperado:
      sucesso: true
      http_status: 201
      resposta:
        contem:
          nome: "Cliente Teste"
      banco:
        clientes:
          deve_existir:
            - nome: "Cliente Teste"
```

**TC-RF[XXX].yaml deve ter:**
```yaml
test_cases:
  TC-RF006-HP-001:
    categoria: "HAPPY_PATH"
    prioridade: "CRITICA"

    # ⚠️ OBRIGATÓRIO
    uc_ref: "UC01"

    # ⚠️ OBRIGATÓRIO
    covers:
      uc_items:
        - "UC01-FP-01"
        - "UC01-FP-05"

    # ⚠️ OBRIGATÓRIO
    origem:
      criterios_aceite: ["CA-UC01-001", "CA-UC01-002"]
      ucs: ["UC01"]
      fluxos_uc: ["FP-UC01-001"]

    # ⚠️ OBRIGATÓRIO
    massa_teste:
      referencias: ["MT-RF006-001"]

# ⚠️ OBRIGATÓRIO ao final
rastreabilidade:
  - tc: "TC-RF006-HP-001"
    ucs: ["UC01"]
    massas: ["MT-RF006-001"]
```

### 5.4 Categorias Obrigatórias

**MT-RF[XXX].yaml:**
| Categoria | Obrigatória | Mínimo |
|-----------|-------------|--------|
| SUCESSO | Sim | 1 |
| VALIDACAO | Sim | 1 |
| SEGURANCA | Sim | 1 |
| AUDITORIA | Sim (CRUD) | 1 |
| MULTI_TENANCY | Sim (CRUD) | 1 |

**TC-RF[XXX].yaml:**
| Categoria | Obrigatória | Prioridade Mínima |
|-----------|-------------|-------------------|
| HAPPY_PATH | Sim | CRITICA |
| VALIDACAO | Sim | CRITICA (campos obrigatórios) |
| SEGURANCA | Sim | ALTA |
| AUDITORIA | Sim (CRUD) | ALTA |
| E2E | Sim (CRUD) | CRITICA |

---

## 6. NEGAÇÃO DE INFERÊNCIA

**VALIDAÇÃO CRÍTICA:**
O validador DEVE REPROVAR se encontrar:

- ❌ MT com cenário NÃO explicitado no UC
- ❌ TC com validação NÃO documentada
- ❌ MT/TC com regra de negócio inventada
- ❌ MT/TC assumindo comportamento implícito

**Exemplo de REPROVAÇÃO:**
```yaml
# ❌ REPROVADO - validação não documentada no UC
MT-RF006-120:
  categoria: "VALIDACAO"
  descricao: "Email corporativo obrigatório"  # ❌ UC não menciona isso
```

---

## 7. CRITÉRIO DE APROVAÇÃO (0% OU 100%)

### 7.1 MT-RF[XXX].yaml

**✅ APROVADO (100%):**
- Cobertura 100% dos cenários UC
- IDs canônicos válidos
- Rastreabilidade completa
- Categorias obrigatórias presentes
- Campos obrigatórios preenchidos
- Sem inferência (todos cenários estão no UC)
- Checklist 100% aprovado

**❌ REPROVADO:**
- QUALQUER item acima falhar

### 7.2 TC-RF[XXX].yaml

**✅ APROVADO (100%):**
- Cobertura 100% dos UCs e uc_items
- IDs canônicos válidos
- Rastreabilidade completa (UC → MT → TC)
- Categorias obrigatórias presentes
- Priorização correta
- Vínculo CA obrigatório (origem.criterios_aceite)
- Referências MT válidas (massa_teste.referencias)
- Matriz de rastreabilidade completa
- Checklist 100% aprovado

**❌ REPROVADO:**
- QUALQUER item acima falhar

**NÃO EXISTE APROVAÇÃO COM RESSALVAS.**

---

## 8. AUTONOMIA TOTAL DO AGENTE

O agente DEVE:
- ✅ Ler UC-RFXXX.md e UC-RFXXX.yaml AUTOMATICAMENTE
- ✅ Ler MT-RF[XXX].yaml AUTOMATICAMENTE
- ✅ Executar checklist-documentacao-mt.yaml AUTOMATICAMENTE
- ✅ Validar cobertura, IDs, rastreabilidade, categorias MT AUTOMATICAMENTE
- ✅ Ler TC-RF[XXX].yaml AUTOMATICAMENTE
- ✅ Executar checklist-documentacao-tc.yaml AUTOMATICAMENTE
- ✅ Validar cobertura, IDs, rastreabilidade, categorias TC AUTOMATICAMENTE
- ✅ Gerar relatório de gaps (se reprovado) AUTOMATICAMENTE
- ✅ Atualizar STATUS.yaml com resultado AUTOMATICAMENTE

O agente NÃO DEVE:
- ❌ Perguntar se pode validar
- ❌ Esperar usuário confirmar intermediariamente
- ❌ Aprovar com ressalvas
- ❌ Corrigir gaps (responsabilidade de outro contrato)

---

## 9. RESPONSABILIDADE DO AGENTE

1. Validar pré-requisitos (MT e TC existem, UC validado)
2. Ler UC-RFXXX.md e UC-RFXXX.yaml completamente
3. Ler MT-RF[XXX].yaml completamente
4. Executar checklist-documentacao-mt.yaml
5. Validar cobertura, IDs, rastreabilidade, categorias MT
6. Se MT REPROVADO: gerar relatório de gaps, PARAR
7. Se MT APROVADO: prosseguir para TC
8. Ler TC-RF[XXX].yaml completamente
9. Executar checklist-documentacao-tc.yaml
10. Validar cobertura, IDs, rastreabilidade, categorias, priorização TC
11. Se TC REPROVADO: gerar relatório de gaps
12. Se TC APROVADO: declarar validação 100%
13. Atualizar STATUS.yaml com resultado

---

## 10. RELATÓRIO DE GAPS (SE REPROVADO)

**OBRIGATÓRIO gerar se REPROVADO:**

```markdown
# RELATÓRIO DE GAPS - MT+TC RFXXX

**Data:** YYYY-MM-DD HH:mm:ss
**Validador:** Claude Sonnet 4.5
**Resultado:** ❌ REPROVADO

---

## RESUMO EXECUTIVO

Validação de MT-RF[XXX].yaml e TC-RF[XXX].yaml REPROVADA.

**Total de gaps identificados:** X

**Próximo passo:** Corrigir gaps identificados e re-executar validação.

---

## GAPS IDENTIFICADOS - MT-RF[XXX].yaml

### Cobertura
- [ ] Fluxo FP-UC01-003 não tem MT correspondente
- [ ] Validação campo "nome" não tem MT

### IDs Canônicos
- [ ] MT-001 inválido (falta RF006)
- [ ] MT-RF006-1 inválido (falta zero à esquerda)

### Rastreabilidade
- [ ] MT-RF006-015 sem ca_ref (CA-UC01-005 existe)

### Categorias
- [ ] Falta categoria AUDITORIA (obrigatória para CRUD)

### Campos Obrigatórios
- [ ] MT-RF006-010 sem resultado_esperado.banco

### Negação de Inferência
- [ ] MT-RF006-020 testa validação não documentada no UC

---

## GAPS IDENTIFICADOS - TC-RF[XXX].yaml

### Cobertura
- [ ] UC02 não tem TC correspondente
- [ ] uc_item UC01-FP-05 não coberto

### IDs Canônicos
- [ ] TC-HP-001 inválido (falta RF006)

### Rastreabilidade
- [ ] TC-RF006-HP-001 sem massa_teste.referencias

### Categorias
- [ ] Falta categoria E2E (obrigatória para CRUD)

### Priorização
- [ ] TC-RF006-HP-001 com prioridade MEDIA (deve ser CRITICA)
- [ ] TC-RF006-SEC-010 com prioridade BAIXA (deve ser >= ALTA)

### Vínculo CA
- [ ] CA-UC01-003 sem TC correspondente

---

## PRÓXIMO PASSO

Corrigir gaps identificados e re-executar validação.

**NAO prosseguir para testes E2E até 100% aprovado.**
```

---

## 11. ATUALIZAÇÃO STATUS.yaml

**Se APROVADO 100%:**
```yaml
documentacao:
  mt: true
  tc: true
  mt_tc_validacao:
    data_validacao: "2026-01-02 14:30:00"
    validador: "Claude Sonnet 4.5"
    resultado: "APROVADO"
    cobertura_mt: "100%"
    cobertura_tc: "100%"
```

**Se REPROVADO:**
```yaml
documentacao:
  mt: true
  tc: true
  mt_tc_validacao:
    data_validacao: "2026-01-02 14:30:00"
    validador: "Claude Sonnet 4.5"
    resultado: "REPROVADO"
    gaps_identificados: 15
    relatorio: "D:\IC2\.temp_ia\RELATORIO-GAPS-MT-TC-RF006.md"
```

---

## 12. Histórico de Versões

| Versão | Data | Descrição |
|--------|------|-----------|
| 1.2 | 2026-01-11 | Adicionada validação 11 "Validar TC Stateful" na FASE 2 (TC) - Valida que TCs stateful possuem configuração completa: metadata.tipo_teste = "STATEFUL", metadata.contrato_teste_stateful referenciando CONTRATO-TESTES-E2E-STATEFUL.md, metadata.requisitos_playwright (workers: 1, fullyParallel: false, retries: 0), metadata.fixtures_necessarias não vazia, TODOS os TCs E2E com usa_fixture, fixture_dependencia, sequencia ordenada. Garante que testes stateful serão executados corretamente, evitando 67% dos problemas do RF006. Resolve gap arquitetural: validação agora verifica stateful ANTES de execução. Referência: CONTRATO-TESTES-E2E-STATEFUL.md seção 2. |
| 1.1 | 2026-01-09 | Adicionada validação 10 "Validar Seletores E2E Especificados" na FASE 2 (TC) - Valida que TODOS os passos possuem seletor, seguem padrão [data-test='...'], possuem acao_e2e, e data-test batem com UC (não inventados). Garante que testes E2E terão seletores corretos, evitando falhas sistemáticas. Baseado em análise RF006 (32 testes falharam por seletores não encontrados). Referência: CLAUDE.md seção 18.2.2 |
| 1.0 | 2026-01-02 | Criação do contrato de validação integrada de MT e TC com critério binário (0% ou 100%) |

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
