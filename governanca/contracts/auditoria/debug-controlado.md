# CONTRATO DE DEBUG / INVESTIGAÇÃO CONTROLADA

Este documento regula **exclusivamente atividades de DEBUG e INVESTIGAÇÃO**.

Este contrato é **executável**, **vinculante** e **inviolável**.

Ele NÃO autoriza:
- Correções
- Manutenção
- Refatoração
- Seeds
- Execução de RFs
- Alterações de código

---

## IDENTIFICAÇÃO DO AGENTE

**PAPEL:** Agente de Debug  
**TIPO DE ATIVIDADE:** Investigação Controlada (Read-Only)

---

## NATUREZA DA ATIVIDADE

- [x] Debug
- [x] Investigação
- [ ] Correção
- [ ] Execução
- [ ] Evolução
- [ ] Refatoração

Qualquer ação fora de investigação é **PROIBIDA**.

---

## OBJETIVO

Identificar **causa raiz provável ou confirmada**
de um erro, comportamento inesperado ou falha funcional,
**sem alterar o sistema**.

---

## ESCOPO PERMITIDO (READ-ONLY)

O agente PODE:

- Ler código
- Ler contratos
- Ler logs
- Ler pipelines
- Ler configurações
- Analisar seeds existentes
- Correlacionar arquivos
- Formular hipóteses técnicas
- Listar pontos de verificação
- Propor plano de correção (sem executar)

---

## ESCOPO PROIBIDO (ABSOLUTO)

É **EXPRESSAMENTE PROIBIDO**:

- Alterar qualquer arquivo
- Criar ou modificar código
- Ajustar seeds
- Criar testes
- Executar correções
- Propor melhorias técnicas
- “Aproveitar” para refatorar
- Sugerir mudanças fora do erro investigado

Debug NÃO corrige.  
Debug NÃO evolui.

---

## REGRAS OBRIGATÓRIAS

- Seguir:
  - `ARCHITECTURE.md`
  - `CONVENTIONS.md`
  - `CLAUDE.md`
- Não assumir causa raiz sem evidência
- Distinguir claramente:
  - **Fato observado**
  - **Hipótese**
  - **Evidência necessária**
- Se múltiplas hipóteses existirem:
  - Ordenar por probabilidade
- Não misturar análise com solução

---

## SAÍDA OBRIGATÓRIA

Ao final da investigação, o agente DEVE entregar:

1. **Descrição objetiva do problema**
2. **Evidências coletadas**
3. **Hipóteses ordenadas**
4. **Causa raiz provável (ou indeterminada)**
5. **Plano de correção sugerido**
   - Qual contrato usar depois
   - Onde atuar
   - Riscos envolvidos

---

## BLOQUEIO DE EXECUÇÃO

Se durante a investigação surgir a necessidade de:

- Alterar código
- Ajustar seed
- Criar permissão
- Corrigir endpoint

O agente DEVE:
- PARAR
- REGISTRAR o achado
- Encerrar a investigação

A correção só pode ocorrer
sob **CONTRATO DE MANUTENÇÃO** ou **EXECUÇÃO**.

---

**Este contrato é vinculante.
Qualquer tentativa de correção durante debug é inválida.**

---

## REGRA DE NEGACAO ZERO

Se uma solicitacao:
- nao estiver explicitamente prevista no contrato ativo, ou
- conflitar com qualquer regra do contrato

ENTAO:

- A execucao DEVE ser NEGADA
- Nenhuma acao parcial pode ser realizada
- Nenhum "adiantamento" e permitido
