Executar validacao de Massa de Teste (MT) e Casos de Teste (TC) do RFXXX conforme D:\IC2_Governanca\contracts\documentacao\validacao\mt-tc.md.

Modo governanca rigida. Nao negociar escopo. Nao extrapolar.
Seguir D:\IC2\CLAUDE.md.

Preste MUITA atencao ao checklist obrigatorio, pois e essencial que voce o siga.

ESTRUTURA DE ARQUIVOS (OBRIGATORIA):
```
docs\rf\[FASE]\[EPIC]\[RFXXX]\
├── RF[XXX].yaml
├── UC-RF[XXX].md
├── UC-RF[XXX].yaml
├── MT-RF[XXX].yaml               ⚠️ VALIDAR AQUI (com hífen)
├── TC-RF[XXX].yaml               ⚠️ VALIDAR AQUI (com hífen)
├── RL-RF[XXX].yaml
└── STATUS.yaml
```

NOMENCLATURA OBRIGATORIA:
- Arquivos MT: MT-RF[XXX].yaml (nao MT-RFXXX.yaml)
- Arquivos TC: TC-RF[XXX].yaml (nao TC-RFXXX.yaml)
- IDs de massa: MT-RF[XXX]-[NNN] (exemplo: MT-RF006-001)
- IDs de casos: TC-RF[XXX]-[CAT]-[NNN] (exemplo: TC-RF006-HP-001)

PRE-REQUISITOS OBRIGATORIOS (BLOQUEANTES):
- MT-RF[XXX].yaml DEVE existir
- TC-RF[XXX].yaml DEVE existir
- UC-RF[XXX].md DEVE existir (para validar cobertura)
- UC-RF[XXX].yaml DEVE existir (para validar rastreabilidade)
- STATUS.yaml DEVE ter documentacao.mt = true E documentacao.tc = true
- Backend DEVE estar aprovado 100% (desenvolvimento.backend.conformidade = "100%")
- Frontend DEVE estar aprovado 100% (desenvolvimento.frontend.conformidade = "100%")

ORDEM DE VALIDACAO (BLOQUEANTE):
1. PRIMEIRO: Validar MT-RFXXX.yaml
   - Executar checklist-documentacao-mt.yaml
   - Validar cobertura 100% dos cenarios de UC
   - Validar IDs canonicos (MT-RFXXX-NNN)
   - Validar rastreabilidade UC → MT
   - SOMENTE prosseguir se aprovado 100%

2. SEGUNDO: Validar TC-RFXXX.yaml
   - Executar checklist-documentacao-tc.yaml
   - Validar cobertura 100% dos UCs e uc_items
   - Validar IDs canonicos (TC-RFXXX-[CAT]-NNN)
   - Validar rastreabilidade UC → MT → TC
   - SOMENTE prosseguir se aprovado 100%

COBERTURA 100% ABSOLUTA - VALIDACAO CRITICA (MT):

Principio fundamental: Cobertura TOTAL significa ZERO cenarios sem MT.

1. VALIDAR TODOS os Fluxos do UC (100%):
   - ✅ Verificar CADA FP-UCXX-NNN (Fluxo Principal) tem MT
   - ✅ Verificar CADA FA-UCXX-NNN (Fluxo Alternativo) tem MT
   - ✅ Verificar CADA FE-UCXX-NNN (Fluxo de Excecao) tem MT
   - ❌ Se QUALQUER fluxo sem MT: REPROVAR

2. VALIDAR TODOS os Criterios de Aceite (100%):
   - ✅ Verificar CADA CA-UCXX-NNN tem MT vinculado (ca_ref)
   - ❌ Se QUALQUER CA sem MT: REPROVAR

3. VALIDAR TODAS as Validacoes (100%):
   - ✅ Campos obrigatorios: TODOS devem ter MT de ausencia
   - ✅ Formatos: TODOS devem ter MT de formato invalido
   - ✅ Ranges: TODOS devem ter MT de valores fora do range
   - ✅ Regras de negocio: TODAS devem ter MT de violacao
   - ❌ Se QUALQUER validacao sem MT: REPROVAR

4. VALIDAR TODOS os Cenarios de Seguranca (100%):
   - ✅ Usuario nao autenticado (401): OBRIGATORIO
   - ✅ Usuario sem permissao (403): OBRIGATORIO
   - ✅ Multi-tenancy (isolamento entre tenants): OBRIGATORIO
   - ✅ Tentativa de acesso a dados de outro tenant: OBRIGATORIO
   - ❌ Se QUALQUER cenario de seguranca ausente: REPROVAR

5. VALIDAR TODOS os Cenarios de Auditoria (100% - CRUD):
   - ✅ created_by preenchido: OBRIGATORIO
   - ✅ updated_by preenchido: OBRIGATORIO
   - ✅ created_at preenchido: OBRIGATORIO
   - ✅ updated_at preenchido: OBRIGATORIO
   - ❌ Se QUALQUER campo de auditoria nao testado: REPROVAR

6. VALIDAR TODOS os Edge Cases (100%):
   - ✅ Tamanho maximo de CADA campo
   - ✅ Valores limite de CADA campo numerico (0, -1, MAX_INT)
   - ✅ Caracteres especiais em CADA campo texto
   - ✅ Unicode / emojis em CADA campo texto
   - ✅ Strings vazias vs null em CADA campo
   - ❌ Se QUALQUER campo sem edge case: REPROVAR

7. VALIDAR TODAS as Integracoes (100%):
   - ✅ CADA FK deve ter MT de FK invalida
   - ✅ CADA constraint deve ter MT de violacao
   - ❌ Se QUALQUER FK ou constraint nao testada: REPROVAR

VALIDACOES OBRIGATORIAS (MT):

1. IDS CANONICOS:
   - Formato: MT-RF[XXX]-[NNN] (exemplo: MT-RF006-001)
   - Sem duplicados
   - Sem IDs invalidos

2. RASTREABILIDADE COMPLETA:
   - Secao rastreabilidade presente
   - Matriz RF → UC → MT completa
   - Todos MT possuem ca_ref (quando CA existir)

3. CATEGORIAS OBRIGATORIAS (TODAS - SEM EXCECAO):

| Categoria | Minimo | Exemplos |
|-----------|--------|----------|
| SUCESSO | 1 | Criacao valida, edicao valida, consulta valida |
| VALIDACAO_OBRIGATORIO | 1 por campo obrigatorio | Campo ausente, null quando obrigatorio |
| VALIDACAO_FORMATO | 1 por campo formatado | Email invalido, CPF invalido, data invalida |
| REGRA_NEGOCIO | 1 por regra | Duplicacao, violacao de unicidade |
| AUTORIZACAO | 2 (401 + 403) | Nao autenticado (401), sem permissao (403) |
| EDGE_CASE | 1 por campo | Tamanho maximo, valores limite, caracteres especiais |
| MULTI_TENANCY | 1 (CRUD) | Isolamento entre tenants |
| AUDITORIA | 1 (CRUD) | created_by, updated_by, created_at, updated_at |
| INTEGRACAO | 1 por FK | FK invalida, integridade referencial |

**REGRA CRITICA:** TODAS as categorias sao obrigatorias. "Minimo" indica quantidade minima de MTs por categoria.

4. CAMPOS OBRIGATORIOS:
   - contexto (autenticacao, estado_inicial)
   - entrada (dados enviados)
   - resultado_esperado (sucesso, http_status, resposta, banco)

5. NEGACAO DE INFERENCIA:
   - Nenhuma MT com cenario nao explicitado no UC
   - Nenhuma validacao inventada
   - Nenhuma regra de negocio nao documentada

COBERTURA 100% ABSOLUTA - VALIDACAO CRITICA (TC):

Principio fundamental: Cobertura TOTAL significa ZERO UCs sem TC.

1. VALIDAR TODOS os UCs (100%):
   - ✅ Verificar CADA UC tem pelo menos um TC
   - ❌ Se QUALQUER UC sem TC: REPROVAR

2. VALIDAR TODOS os uc_items (100%):
   - ✅ Verificar CADA uc_item (passo granular) esta em covers.uc_items
   - Exemplo: Se UC01 tem UC01-FP-01 a UC01-FP-10, TODOS devem estar cobertos
   - ❌ Se QUALQUER uc_item sem cobertura: REPROVAR

3. VALIDAR TODOS os Criterios de Aceite (100%):
   - ✅ Verificar CADA CA tem pelo menos um TC correspondente
   - ✅ Verificar TC lista CA em origem.criterios_aceite
   - ❌ Se QUALQUER CA sem TC: REPROVAR

4. VALIDAR TODOS os Fluxos (100%):
   - ✅ Fluxo Principal (FP): Pelo menos um TC-HP (Happy Path)
   - ✅ Fluxos Alternativos (FA): TC-VAL ou TC-EDGE
   - ✅ Fluxos de Excecao (FE): TC-VAL, TC-SEC, TC-EDGE
   - ❌ Se QUALQUER fluxo sem TC: REPROVAR

5. VALIDAR TODAS as Referencias MT (100%):
   - ✅ Verificar CADA TC referencia MT correspondente (massa_teste.referencias)
   - ❌ Se QUALQUER TC sem referencia MT: REPROVAR
   - ❌ Se QUALQUER referencia MT invalida (MT inexistente): REPROVAR

VALIDACOES OBRIGATORIAS (TC):

1. IDS CANONICOS:
   - Formato: TC-RF[XXX]-[CAT]-[NNN] (exemplo: TC-RF006-HP-001)
   - Sem duplicados
   - Sem IDs invalidos

2. RASTREABILIDADE COMPLETA:
   - Matriz TC → UC → MT completa
   - Todos TC possuem origem.criterios_aceite
   - Todos TC possuem massa_teste.referencias

3. CATEGORIAS OBRIGATORIAS (TODAS - SEM EXCECAO):

| Categoria | Minimo | Prioridade | Exemplos |
|-----------|--------|------------|----------|
| HAPPY_PATH | 1 por UC | CRITICA | Fluxo principal FP-UCXX completo |
| VALIDACAO | 1 por validacao | CRITICA | Campo obrigatorio, formato invalido |
| SEGURANCA | 2 (401 + 403) | CRITICA | Nao autenticado (401), sem permissao (403) |
| EDGE_CASE | 1 por campo | ALTA | Tamanho maximo, valores limite |
| AUDITORIA | 1 (CRUD) | ALTA | Auditoria de criacao, atualizacao, exclusao |
| INTEGRACAO | 1 por FK | ALTA | FK invalida, integridade referencial |
| E2E | 1 completo (CRUD) | CRITICA | Fluxo CRUD completo (criar → consultar → editar → excluir) |

**REGRA CRITICA:** TODAS as categorias sao obrigatorias. "Minimo" indica quantidade minima de TCs por categoria.

4. PRIORIZACAO CORRETA:
   - HAPPY_PATH = CRITICA
   - SEGURANCA >= CRITICA (nunca BAIXA)
   - VALIDACAO (campo obrigatorio) = CRITICA
   - E2E = CRITICA

5. VINCULO CA OBRIGATORIO:
   - Toda CA DEVE ter pelo menos um TC correspondente
   - CA sem TC = BLOQUEIO CRITICO

CRITERIO DE APROVACAO (0% OU 100%):

MT-RF[XXX].yaml:
- ✅ APROVADO: Cobertura 100% ABSOLUTA, TODOS fluxos (FP, FA, FE), TODOS CAs, TODAS validacoes, TODOS edge cases, TODAS categorias obrigatorias, IDs validos, rastreabilidade completa, campos OK, sem inferencia
- ❌ REPROVADO: QUALQUER item acima falhar

TC-RF[XXX].yaml:
- ✅ APROVADO: Cobertura 100% ABSOLUTA, TODOS UCs, TODOS uc_items, TODOS CAs, TODOS fluxos, TODAS referencias MT validas, TODAS categorias obrigatorias, IDs validos, rastreabilidade completa, priorizacao OK
- ❌ REPROVADO: QUALQUER item acima falhar

REGRA CRITICA:
- SE MT nao cobrir 100% ABSOLUTO dos cenarios: BLOQUEIO
- SE TC nao cobrir 100% ABSOLUTO dos UCs: BLOQUEIO
- SE MT sem rastreabilidade: BLOQUEIO
- SE TC sem rastreabilidade: BLOQUEIO
- SE checklist reprovar: BLOQUEIO
- ZERO cenarios sem MT/TC tolerado

NAO EXISTE APROVACAO COM RESSALVAS.

AUTONOMIA TOTAL:
- NAO perguntar se pode validar
- NAO esperar usuario confirmar
- O agente DEVE executar checklists AUTOMATICAMENTE
- Identificar gaps e REPROVAR se cobertura < 100%
- Gerar relatorio de gaps (se reprovado)

RESPONSABILIDADE DO AGENTE:
1. Ler UC-RFXXX.md e UC-RFXXX.yaml completamente
2. Ler MT-RFXXX.yaml completamente
3. Executar checklist-documentacao-mt.yaml
4. Validar cobertura, IDs, rastreabilidade, categorias
5. Se REPROVADO: gerar relatorio de gaps
6. Se APROVADO: prosseguir para TC
7. Ler TC-RFXXX.yaml completamente
8. Executar checklist-documentacao-tc.yaml
9. Validar cobertura, IDs, rastreabilidade, categorias, priorizacao
10. Se REPROVADO: gerar relatorio de gaps
11. Se APROVADO: declarar validacao 100%
12. Atualizar STATUS.yaml

RELATORIO DE GAPS (se reprovado):

```markdown
# RELATORIO DE GAPS - MT+TC RFXXX

## RESUMO EXECUTIVO

Validacao de MT-RFXXX.yaml e TC-RFXXX.yaml REPROVADA.

## GAPS IDENTIFICADOS - MT-RFXXX.yaml

### Cobertura
- [ ] Fluxo FP-UC01-003 nao tem MT correspondente
- [ ] Validacao campo "nome" nao tem MT

### IDs Canonicos
- [ ] MT-001 invalido (falta RFXXX)
- [ ] MT-RF060-1 invalido (falta zero a esquerda)

### Rastreabilidade
- [ ] MT-RF060-015 sem ca_ref (CA-UC01-005 existe)

### Categorias
- [ ] Falta categoria AUDITORIA (obrigatoria para CRUD)

### Campos Obrigatorios
- [ ] MT-RF060-010 sem resultado_esperado.banco

### Negacao de Inferencia
- [ ] MT-RF060-020 testa validacao nao documentada no UC

## GAPS IDENTIFICADOS - TC-RFXXX.yaml

### Cobertura
- [ ] UC02 nao tem TC correspondente
- [ ] uc_item UC01-FP-05 nao coberto

### IDs Canonicos
- [ ] TC-HP-001 invalido (falta RFXXX)

### Rastreabilidade
- [ ] TC-RF060-HP-001 sem massa_teste.referencias

### Categorias
- [ ] Falta categoria E2E (obrigatoria para CRUD)

### Priorizacao
- [ ] TC-RF060-HP-001 com prioridade MEDIA (deve ser CRITICA)
- [ ] TC-RF060-SEC-010 com prioridade BAIXA (deve ser >= ALTA)

### Vinculo CA
- [ ] CA-UC01-003 sem TC correspondente

## PROXIMO PASSO

Corrigir gaps identificados e re-executar validacao.

NAO prosseguir para testes E2E ate 100% aprovado.
```

PROIBIDO:
- Aprovar com ressalvas
- Ignorar gaps de cobertura
- Prosseguir se checklist reprovar
- Marcar STATUS.yaml como validado se reprovado

CRITERIO DE PRONTO:
- MT-RFXXX.yaml APROVADO 100%
- TC-RFXXX.yaml APROVADO 100%
- Relatorio de gaps gerado (se reprovado)
- STATUS.yaml atualizado com resultado validacao
- Nenhuma violacao de contrato
