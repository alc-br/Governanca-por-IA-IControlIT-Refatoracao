# CONTRATO DE VALIDAÇÃO MT + TC (MASSA DE TESTE + CASOS DE TESTE)

**Versão:** 1.0
**Data:** 2026-01-02
**Status:** Ativo
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
Seguir CLAUDE.md.
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

10. **Resultado FASE 2:**
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

## 12. REGRA DE NEGAÇÃO ZERO

Se uma solicitação:
- não estiver explicitamente prevista no contrato ativo, ou
- conflitar com qualquer regra do contrato

ENTÃO:
- A execução DEVE ser NEGADA
- Nenhuma ação parcial pode ser realizada
- Nenhum "adiantamento" é permitido

---

**FIM DO CONTRATO**
