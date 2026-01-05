Executar criacao de Massa de Teste (MT) e Casos de Teste (TC) do RFXXX conforme docs\contracts\documentacao\execucao\mt-tc-criacao.md.

Modo governanca rigida. Nao negociar escopo. Nao extrapolar.
Seguir D:\IC2\CLAUDE.md.

Preste MUITA atencao ao checklist obrigatorio, pois e essencial que voce o siga.

ORDEM DE EXECUCAO (BLOQUEANTE):
1. PRIMEIRO: Executar CONTRATO-GERACAO-DOCS-MT
   - Criar docs\rf\[FASE]\[EPIC]\[RFXXX]\MT-RF[XXX].yaml (Massa de Teste)
   - Validar via checklist-documentacao-mt.yaml
   - Atualizar STATUS.yaml
   - SOMENTE prosseguir se aprovado 100%

2. SEGUNDO: Executar CONTRATO-GERACAO-DOCS-TC
   - Criar docs\rf\[FASE]\[EPIC]\[RFXXX]\TC-RF[XXX].yaml (Casos de Teste)
   - Validar via checklist-documentacao-tc.yaml
   - Atualizar STATUS.yaml
   - SOMENTE prosseguir se aprovado 100%

ESTRUTURA DE ARQUIVOS (OBRIGATORIA):
```
docs\rf\[FASE]\[EPIC]\[RFXXX]\
├── RF[XXX].yaml                  (Requisito Funcional)
├── UC-RF[XXX].md                 (Casos de Uso)
├── UC-RF[XXX].yaml               (Casos de Uso estruturado)
├── MD-RF[XXX].md                 (Modelo de Dados - se aplicavel)
├── WF-RF[XXX].md                 (Workflow - se aplicavel)
├── MT-RF[XXX].yaml               (Massa de Teste) ⚠️ CRIAR AQUI
├── TC-RF[XXX].yaml               (Casos de Teste) ⚠️ CRIAR AQUI
├── RL-RF[XXX].yaml               (Regras de Negocio)
└── STATUS.yaml                   (Status do RF)
```

Exemplo para RF006:
```
docs\rf\Fase-1-Sistema-Base\EPIC001-SYS-Sistema-Infraestrutura\RF006-Gestao-de-Clientes\
├── RF006.yaml
├── UC-RF006.md
├── UC-RF006.yaml
├── MT-RF006.yaml                 ⚠️ CRIAR AQUI (na mesma pasta do RF)
├── TC-RF006.yaml                 ⚠️ CRIAR AQUI (na mesma pasta do RF)
├── RL-RF006.yaml
└── STATUS.yaml
```

NOMENCLATURA OBRIGATORIA:
- Arquivos MT: MT-RF[XXX].yaml (nao MT-RFXXX.yaml)
- Arquivos TC: TC-RF[XXX].yaml (nao TC-RFXXX.yaml)
- IDs de massa: MT-RF[XXX]-[NNN] (exemplo: MT-RF006-001)
- IDs de casos: TC-RF[XXX]-[CAT]-[NNN] (exemplo: TC-RF006-HP-001)

PRE-REQUISITOS OBRIGATORIOS (BLOQUEANTES):
Antes de QUALQUER acao, validar:

1. UC-RFXXX.md DEVE existir e estar validado
2. UC-RFXXX.yaml DEVE existir e estar sincronizado
3. STATUS.yaml DEVE ter documentacao.uc = true
4. Backend DEVE estar aprovado 100% (desenvolvimento.backend.conformidade = "100%")
5. Frontend DEVE estar aprovado 100% (desenvolvimento.frontend.conformidade = "100%")
6. Templates MT.yaml e TC.yaml DEVEM existir

JUSTIFICATIVA - Por que MT e TC precisam de backend E frontend prontos:

1. MT (Massa de Teste) precisa de DADOS REAIS:
   - MT define payloads que serao enviados ao backend (precisa conhecer contratos de API)
   - MT define respostas esperadas do backend (precisa conhecer DTOs reais)
   - MT define estados que frontend vai renderizar (precisa conhecer estados implementados)
   - NAO da para criar MT eficaz sem saber como backend E frontend funcionam juntos

2. TC (Casos de Teste) testa FLUXOS COMPLETOS:
   - TC-E2E simula usuario real (clicar botao, preencher form, ver resposta na tela)
   - TC valida 4 estados renderizados: Padrao, Loading, Vazio, Erro (so existem no frontend)
   - TC precisa conhecer: endpoints disponiveis, componentes Angular, estados possiveis
   - Impossivel escrever TC-E2E sem backend E frontend prontos

3. RASTREABILIDADE COMPLETA:
   - MT e TC testam integracao backend + frontend
   - Se backend mudar depois, MT/TC ficam desalinhados (retrabalho)
   - Se frontend mudar depois, MT/TC ficam desalinhados (retrabalho)
   - SOMENTE com ambos prontos, MT/TC refletem sistema REAL

VALIDACAO DE PRE-REQUISITOS:
1. Verificar se backend foi aprovado:
   - STATUS.yaml desenvolvimento.backend.conformidade DEVE ser "100%"
   - Se < 100%: BLOQUEAR criacao de MT e TC
   - Motivo: MT precisa de contratos de API reais, nao inventados

2. Verificar se frontend foi aprovado:
   - STATUS.yaml desenvolvimento.frontend.conformidade DEVE ser "100%"
   - Se < 100%: BLOQUEAR criacao de MT e TC
   - Motivo: TC precisa de estados renderizados reais, nao imaginarios

3. Se QUALQUER pre-requisito falhar:
   - PARAR imediatamente
   - REPROVAR com mensagem clara
   - NAO prosseguir com MT e TC

COBERTURA 100% ABSOLUTA (PRINCIPIO FUNDAMENTAL):
Cobertura TOTAL significa ZERO cenarios sem MT/TC.

MT (Massa de Teste) DEVE COBRIR:
1. TODOS os Fluxos do UC (100%):
   - Fluxo Principal (FP): TODOS os passos FP-UCXX-NNN
   - Fluxos Alternativos (FA): TODOS os passos FA-UCXX-NNN
   - Fluxos de Excecao (FE): TODOS os passos FE-UCXX-NNN
   - NENHUM fluxo pode ficar sem MT

2. TODOS os Criterios de Aceite (100%):
   - TODOS os CA-UCXX-NNN devem ter MT vinculado (ca_ref)
   - NENHUM CA pode ficar sem MT

3. TODAS as Validacoes (100%):
   - Campos obrigatorios (TODOS)
   - Formatos (email, CPF, data - TODOS)
   - Ranges (min, max - TODOS)
   - Regras de negocio (duplicacao, unicidade - TODAS)

4. TODOS os Cenarios de Seguranca (100%):
   - Nao autenticado (401)
   - Sem permissao (403)
   - Multi-tenancy (isolamento entre tenants)
   - Tentativa de acesso a dados de outro tenant

5. TODOS os Cenarios de Auditoria (100% - CRUD):
   - created_by, updated_by, created_at, updated_at

6. TODOS os Edge Cases (100%):
   - Tamanho maximo de campos
   - Valores limite (0, -1, MAX_INT)
   - Caracteres especiais
   - Unicode / emojis
   - Strings vazias vs null

7. TODAS as Integracoes (100%):
   - CADA FK deve ter MT de FK invalida
   - CADA constraint deve ter MT de violacao

TC (Casos de Teste) DEVE COBRIR:
1. TODOS os UCs (100%):
   - CADA UC deve ter pelo menos um TC
   - NENHUM UC pode ficar sem TC

2. TODOS os uc_items (100%):
   - CADA uc_item (passo granular) deve estar coberto
   - Exemplo: Se UC01 tem uc_items UC01-FP-01 a UC01-FP-10, TODOS devem estar em covers.uc_items
   - NENHUM uc_item pode ficar sem cobertura

3. TODOS os Criterios de Aceite (100%):
   - CADA CA deve ter pelo menos um TC correspondente
   - TC deve listar CA em origem.criterios_aceite
   - NENHUM CA pode ficar sem TC

4. TODOS os Fluxos (100%):
   - Fluxo Principal (FP): Pelo menos um TC-HP (Happy Path)
   - Fluxos Alternativos (FA): TC-VAL ou TC-EDGE
   - Fluxos de Excecao (FE): TC-VAL, TC-SEC, TC-EDGE

5. TODAS as Referencias MT (100%):
   - CADA TC deve referenciar MT correspondente (massa_teste.referencias)
   - NENHUM TC sem referencia MT
   - NENHUMA referencia MT invalida (MT inexistente)

CATEGORIAS OBRIGATORIAS (MT) - TODAS SEM EXCECAO:
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

CATEGORIAS OBRIGATORIAS (TC) - TODAS SEM EXCECAO:
| Categoria | Minimo | Prioridade | Exemplos |
|-----------|--------|------------|----------|
| HAPPY_PATH | 1 por UC | CRITICA | Fluxo principal FP-UCXX completo |
| VALIDACAO | 1 por validacao | CRITICA | Campo obrigatorio, formato invalido |
| SEGURANCA | 2 (401 + 403) | CRITICA | Nao autenticado (401), sem permissao (403) |
| EDGE_CASE | 1 por campo | ALTA | Tamanho maximo, valores limite |
| AUDITORIA | 1 (CRUD) | ALTA | Auditoria de criacao, atualizacao, exclusao |
| INTEGRACAO | 1 por FK | ALTA | FK invalida, integridade referencial |
| E2E | 1 completo (CRUD) | CRITICA | Fluxo CRUD completo (criar → consultar → editar → excluir) |

REGRA CRITICA:
- SE MT nao cobrir 100% dos cenarios: BLOQUEIO
- SE TC nao cobrir 100% dos UCs: BLOQUEIO
- SE MT sem rastreabilidade: BLOQUEIO
- SE TC sem rastreabilidade: BLOQUEIO
- SE checklist reprovar: BLOQUEIO

AUTONOMIA TOTAL:
- NAO perguntar se pode criar MT ou TC
- NAO esperar usuario validar
- O agente DEVE criar MT e TC COMPLETOS (100%)
- Garantir rastreabilidade total sem intervencao manual

RESPONSABILIDADE DO AGENTE:
1. Validar pre-requisitos (backend 100%, frontend 100%, UC validado)
2. Ler UC-RFXXX.md e UC-RFXXX.yaml completamente
3. Analisar backend implementado (DTOs, validacoes, regras)
4. Analisar frontend implementado (componentes, estados, validacoes)
5. Criar MT-RF[XXX].yaml com DADOS REAIS e cobertura 100% ABSOLUTA
6. Executar checklist-documentacao-mt.yaml
7. Corrigir se reprovado e re-validar
8. Criar TC-RF[XXX].yaml com rastreabilidade completa e cobertura 100% ABSOLUTA
9. Executar checklist-documentacao-tc.yaml
10. Corrigir se reprovado e re-validar
11. Gerar azure-test-cases-RF[XXX].csv (exportacao Azure Test Plans - 15 colunas)
12. Gerar azure-test-suites-RF[XXX].json (suites Azure DevOps - 7 categorias)
13. Validar arquivos Azure (CSV + JSON conforme contrato)
14. Atualizar STATUS.yaml (mt: true, tc: true, azure_devops.pronto_importacao: true)
15. Declarar conclusao (MT + TC + Azure Export prontos 100%)

PROIBIDO:
- Criar MT sem rastreabilidade ao UC
- Criar TC sem rastreabilidade ao MT
- Omitir categorias obrigatorias
- Inferir cenarios nao explicitados no UC
- Criar MT ou TC orfaos
- Marcar como pronto se cobertura < 100%

EXPORTACAO AZURE DEVOPS (OBRIGATORIO):

Apos validar MT e TC, o agente DEVE gerar:

1. azure-test-cases-RF[XXX].csv (CSV com 15 colunas):
   - ID, Title, Area, Iteration, State, Assigned To, Priority
   - Automation Status, Steps, Expected Result, Test Suite
   - Tags, Work Item Type, UC Reference, MT Reference
   - TODOS os TCs exportados (linha por TC)
   - Steps separados por "|" (pipe)

2. azure-test-suites-RF[XXX].json (JSON com suites):
   - 7 suites (HAPPY_PATH, VALIDACAO, SEGURANCA, EDGE_CASE, AUDITORIA, INTEGRACAO, E2E)
   - TODOS os TCs listados em alguma suite
   - total_test_cases e total_suites corretos

3. Validacao da exportacao:
   - CSV: 15 colunas, TODOS TCs, nenhuma linha vazia
   - JSON: 7 suites, total_test_cases correto, TODOS TCs listados
   - STATUS.yaml: azure_devops.pronto_importacao = true

CRITERIO DE PRONTO (0% ou 100%):
- MT-RF[XXX].yaml criado e aprovado no checklist
- TC-RF[XXX].yaml criado e aprovado no checklist
- azure-test-cases-RF[XXX].csv criado e validado (15 colunas)
- azure-test-suites-RF[XXX].json criado e validado (7 suites)
- Cobertura 100% ABSOLUTA: ZERO cenarios sem MT/TC
- TODOS os fluxos (FP, FA, FE) cobertos
- TODOS os uc_items cobertos
- TODOS os CAs vinculados
- TODAS as categorias obrigatorias presentes
- Rastreabilidade completa UC → MT → TC
- Exportacao Azure completa e pronta para importacao
- STATUS.yaml atualizado (mt, tc, azure_devops)
- Nenhuma violacao de contrato

NAO EXISTE APROVACAO COM RESSALVAS.
