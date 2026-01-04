Executar validacao completa de MT-RF[XXX].yaml e TC-RF[XXX].yaml conforme contrato.

Modo governanca rigida. Nao negociar escopo. Nao extrapolar.
Seguir CLAUDE.md.

PRE-REQUISITOS OBRIGATORIOS (BLOQUEANTES):
1. MT-RF[XXX].yaml DEVE existir
2. TC-RF[XXX].yaml DEVE existir
3. UC-RF[XXX].md DEVE existir
4. UC-RF[XXX].yaml DEVE existir
5. STATUS.yaml DEVE ter documentacao.mt = true E documentacao.tc = true

VALIDACAO MT-RF[XXX].yaml:

1. NOMENCLATURA:
   - IDs no formato MT-RF[XXX]-[NNN] (exemplo: MT-RF006-001)
   - Arquivo chamado MT-RF[XXX].yaml (nao MT-RFXXX.yaml)

2. CATEGORIAS OBRIGATORIAS (9 categorias):
   - SUCESSO (001-099): Minimo 1
   - VALIDACAO_OBRIGATORIO (100-199): 1 por campo obrigatorio
   - VALIDACAO_FORMATO (200-299): 1 por campo formatado
   - REGRA_NEGOCIO (300-399): 1 por regra
   - AUTORIZACAO (400-499): 2 (401 + 403)
   - EDGE_CASE (500-599): 1 por campo
   - MULTI_TENANCY (700-799): 1 (CRUD)
   - AUDITORIA (800-899): 1 (CRUD)
   - INTEGRACAO (900-999): 1 por FK

3. COBERTURA 100% ABSOLUTA:
   - TODOS os UCs (UC00-UC08 para RF006)
   - TODOS os CAs vinculados (ca_ref)
   - TODOS os fluxos (FP, FA, FE)
   - ZERO cenarios sem MT

4. RASTREABILIDADE:
   - Campo uc_ref presente em TODAS as MTs
   - Campo ca_ref presente em TODAS as MTs
   - Campo fluxo_ref presente em TODAS as MTs
   - Matriz rastreabilidade.mapeamento_uc_mt completa

5. DADOS REAIS:
   - Campo entrada com payloads reais do backend
   - Campo resultado_esperado com DTOs reais
   - Campo contexto.autenticacao completo
   - Campo contexto.estado_inicial definido

VALIDACAO TC-RF[XXX].yaml:

1. NOMENCLATURA:
   - IDs no formato TC-RF[XXX]-[CAT]-[NNN] (exemplo: TC-RF006-HP-001)
   - Arquivo chamado TC-RF[XXX].yaml (nao TC-RFXXX.yaml)

2. CATEGORIAS OBRIGATORIAS (7 categorias):
   - HAPPY_PATH: 1 por UC (CRITICA)
   - VALIDACAO: 1 por validacao (CRITICA)
   - SEGURANCA: 2 (401 + 403) (CRITICA)
   - EDGE_CASE: 1 por campo (ALTA)
   - AUDITORIA: 1 (CRUD) (ALTA)
   - INTEGRACAO: 1 por FK (ALTA)
   - E2E: 1 completo (CRUD) (CRITICA)

3. COBERTURA 100% ABSOLUTA:
   - TODOS os UCs (1 TC-HP por UC no minimo)
   - TODOS os uc_items cobertos (campo covers.uc_items)
   - TODOS os CAs vinculados (campo origem.criterios_aceite)
   - TODAS as MTs referenciadas (campo massa_teste.referencias)
   - ZERO TCs sem referencia MT
   - ZERO MTs orfas (sem TC correspondente)

4. RASTREABILIDADE:
   - Campo uc_ref presente em TODOS os TCs
   - Campo covers.uc_items presente em TODOS os TCs
   - Campo origem.criterios_aceite presente em TODOS os TCs
   - Campo massa_teste.referencias presente em TODOS os TCs
   - Matriz rastreabilidade.mapeamento_tc_mt_uc completa
   - rastreabilidade.ucs_sem_tc = [] (vazio)
   - rastreabilidade.massas_sem_tc = [] (vazio)

5. PRIORIDADES:
   - HAPPY_PATH → CRITICA
   - VALIDACAO → CRITICA
   - SEGURANCA → CRITICA
   - EDGE_CASE → ALTA
   - AUDITORIA → ALTA
   - INTEGRACAO → ALTA
   - E2E → CRITICA

VALIDACAO EXPORTACAO AZURE DEVOPS (OBRIGATORIO):

1. ARQUIVO CSV (azure-test-cases-RF[XXX].csv):
   - Arquivo existe na pasta do RF
   - Header com 15 colunas:
     * ID, Title, Area, Iteration, State
     * Assigned To, Priority, Automation Status
     * Steps, Expected Result, Test Suite
     * Tags, Work Item Type, UC Reference, MT Reference
   - TODOS os TCs exportados (1 linha por TC)
   - Nenhuma linha vazia ou com dados faltando
   - Steps separados por "|" (pipe)
   - Priority: 1 (CRITICA), 2 (ALTA), 3 (MEDIA)
   - Automation Status: "Planned" (E2E) ou "Not Planned" (outros)

2. ARQUIVO JSON (azure-test-suites-RF[XXX].json):
   - Arquivo existe na pasta do RF
   - Campo rf correto (RF006)
   - Campo titulo correto
   - Campo test_plan_name correto
   - 7 suites presentes:
     * RF[XXX]-HAPPY_PATH
     * RF[XXX]-VALIDACAO
     * RF[XXX]-SEGURANCA
     * RF[XXX]-EDGE_CASE
     * RF[XXX]-AUDITORIA
     * RF[XXX]-INTEGRACAO
     * RF[XXX]-E2E
   - Campo total_test_cases = soma de TCs no TC-RF[XXX].yaml
   - Campo total_suites = 7
   - TODOS os TCs listados em alguma suite
   - Nenhum TC duplicado entre suites

3. STATUS.yaml atualizado:
   - testes.azure_devops.test_cases_exportados = true
   - testes.azure_devops.arquivo_csv correto
   - testes.azure_devops.arquivo_json correto
   - testes.azure_devops.total_test_cases correto
   - testes.azure_devops.total_suites = 7
   - testes.azure_devops.pronto_importacao = true

CRITERIO DE APROVACAO (0% OU 100%):

✅ APROVADO: TODAS as validacoes passaram
❌ REPROVADO: QUALQUER validacao falhou

NAO EXISTE APROVACAO COM RESSALVAS.

RESPONSABILIDADE DO AGENTE:
1. Ler MT-RF[XXX].yaml completamente
2. Ler TC-RF[XXX].yaml completamente
3. Ler azure-test-cases-RF[XXX].csv
4. Ler azure-test-suites-RF[XXX].json
5. Ler STATUS.yaml
6. Validar nomenclatura (MT e TC)
7. Validar categorias obrigatorias (9 MT + 7 TC)
8. Validar cobertura 100% absoluta
9. Validar rastreabilidade completa (UC → MT → TC)
10. Validar exportacao Azure DevOps (CSV + JSON)
11. Validar STATUS.yaml (azure_devops.pronto_importacao)
12. Calcular total de gaps identificados
13. Gerar relatorio de validacao consolidado
14. Declarar APROVADO 100% ou REPROVADO com gaps listados

PROIBIDO:
- Aprovar com cobertura < 100%
- Aprovar com categorias faltando
- Aprovar com rastreabilidade incompleta
- Aprovar sem exportacao Azure DevOps
- Aprovar com MTs ou TCs orfaos

CRITERIO DE PRONTO:
- Relatorio de validacao gerado
- Decisao final declarada (APROVADO 100% ou REPROVADO)
- Gaps identificados e listados (se reprovado)
- Nenhuma violacao de contrato
