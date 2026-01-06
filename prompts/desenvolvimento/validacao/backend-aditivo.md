# Validação Backend Aditivo RFXXX

Ele fica nesse endereço D:\IC2\rf\Fase*\EPIC*\RF*

**Instruções:** Altere RFXXX acima para o RF desejado (ex: RF001, RF025, RF028).

---

Executar **VALIDADOR BACKEND ADITIVO** para o RF informado acima conforme D:/IC2_Governanca/contracts/desenvolvimento/validacao/backend-aditivo.md.
Seguir D:\IC2\CLAUDE.md.

## ⚠️ MODO READ-ONLY

Você NÃO corrige problemas, apenas IDENTIFICA e REPORTA.

## ✅ 10 VALIDAÇÕES (executar todas)

### PARTE 1: DELTA IMPLEMENTADO (5 validações)

1. **VAL-1: Entities criadas/atualizadas (se MD mudou)**
   - Comparar MD-RFXXX.yaml vs MD-RFXXX_old.yaml
   - Verificar se novas entidades foram criadas em `src/Domain/Entities/`

2. **VAL-2: Migrations criadas/aplicadas (se MD mudou)**
   - Verificar migrations em `src/Infrastructure/Data/Migrations/`
   - Executar: `dotnet ef migrations list`

3. **VAL-3: Commands/Queries criados (para cada novo endpoint)**
   - Comparar RF.md vs RF_old.md (identificar novos endpoints)
   - Verificar Commands/Queries em `src/Application/`

4. **VAL-4: Handlers criados (com validação de RNs novas)**
   - Verificar Handlers em `src/Application/`
   - Confirmar que TODAS as RNs novas estão validadas

5. **VAL-5: Endpoints adicionados (Controllers atualizados)**
   - Verificar endpoints em `src/Web/Endpoints/`
   - Confirmar que novos endpoints existem

### PARTE 2: QUALIDADE E TESTES (5 validações)

6. **VAL-6: RNs validadas nos Handlers (todas as RNs novas do delta)**
   - Comparar RF.md vs RF_old.md (identificar RNs novas)
   - Verificar código dos Handlers (buscar por RN-XXX-XXX-XX)

7. **VAL-7: Permissões aplicadas (Authorization nos endpoints)**
   - Verificar `[Authorize(Policy = ...)]` nos endpoints novos

8. **VAL-8: Testes criados (para novos Commands/Queries/Handlers)**
   - Verificar testes em `tests/Application.Tests/`

9. **VAL-9: Build PASS**
   ```bash
   cd backend/IControlIT.API
   dotnet build
   ```
   Exit code 0 = PASS

10. **VAL-10: Tests PASS**
    ```bash
    dotnet test
    ```
    Exit code 0 = PASS

## 📂 ARQUIVOS QUE VOCÊ DEVE LER

**Documentos delta:**
- RFXXX.md vs RFXXX_old.md
- UC-RFXXX.yaml vs UC-RFXXX_old.yaml
- MD-RFXXX.yaml vs MD-RFXXX_old.yaml

**Relatórios:**
- `.temp_ia/aditivo-RFXXX-delta-report.md`
- `.temp_ia/backend-aditivo-RFXXX-relatorio.md`

**Código backend:**
- `src/Domain/Entities/` (Entities)
- `src/Infrastructure/Data/Migrations/` (Migrations)
- `src/Application/` (Commands/Queries/Handlers)
- `src/Web/Endpoints/` (Controllers)
- `tests/Application.Tests/` (Testes)

**Relatório de validação (você vai gerar):**
- `.temp_ia/validacao-backend-aditivo-RFXXX-relatorio.md`

## 🎯 CRITÉRIOS DE APROVAÇÃO

- ✅ **APROVADO:** 10/10 validações PASS
- ❌ **REPROVADO:** Qualquer validação FAIL

## 📄 RELATÓRIO QUE VOCÊ DEVE GERAR

Gere tabela com 10 validações mostrando:
- **Status:** ✅ PASS / ❌ FAIL
- **Severidade:** CRÍTICO / IMPORTANTE / MENOR
- **Resultado:** (detalhes específicos)

Depois, mostre:
- **DELTA VALIDADO:** O que foi implementado vs o que era esperado
- **GAPS IDENTIFICADOS:** (se houver)
- **PONTUAÇÃO FINAL:** X/10 PASS (Z%)
- **VEREDICTO:** ✅ APROVADO / ❌ REPROVADO

**Salvar em:** `.temp_ia/validacao-backend-aditivo-RFXXX-relatorio.md`

## 🔍 VALIDAÇÕES DETALHADAS

### VAL-1: Entities

```python
# Identificar novas tabelas no delta
tabelas_delta = identificar_novas_tabelas(MD_yaml, MD_old_yaml)

# Verificar se entities existem
for tabela in tabelas_delta:
    entity_path = f"src/Domain/Entities/{tabela}.cs"
    if not file_exists(entity_path):
        FAIL(f"Entity {tabela} não criada")

PASS(f"{len(tabelas_delta)}/{len(tabelas_delta)} entities criadas")
```

### VAL-3: Commands/Queries

```python
# Identificar novos endpoints no delta
endpoints_delta = identificar_novos_endpoints(RF_md, RF_old_md)

# Verificar se Commands/Queries existem
for endpoint in endpoints_delta:
    if endpoint.method == "GET":
        # Deve existir Query
        query_name = inferir_query_name(endpoint)
        if not file_exists(f"src/Application/.../{query_name}.cs"):
            FAIL(f"Query {query_name} não criada")
    elif endpoint.method in ["POST", "PUT", "DELETE"]:
        # Deve existir Command
        command_name = inferir_command_name(endpoint)
        if not file_exists(f"src/Application/.../{command_name}.cs"):
            FAIL(f"Command {command_name} não criada")

PASS(f"{len(endpoints_delta)}/{len(endpoints_delta)} Commands/Queries criados")
```

### VAL-6: RNs validadas

```python
# Identificar RNs novas no delta
rns_delta = set(re.findall(r'RN-[A-Z]+-\d+-\d+', RF_md)) - set(re.findall(r'RN-[A-Z]+-\d+-\d+', RF_old_md))

# Verificar se RNs estão validadas nos Handlers
rns_validadas = set()
for handler_file in glob("src/Application/**/*Handler.cs"):
    handler_content = read_file(handler_file)
    for rn in rns_delta:
        if rn in handler_content:
            rns_validadas.add(rn)

rns_nao_validadas = rns_delta - rns_validadas

if rns_nao_validadas:
    FAIL(f"RNs não validadas nos Handlers: {rns_nao_validadas}")
else:
    PASS(f"{len(rns_delta)}/{len(rns_delta)} RNs validadas")
```

### VAL-9: Build PASS

```bash
cd backend/IControlIT.API
dotnet build

# Exit code 0 = APROVADO
# Exit code != 0 = REPROVADO
```

### VAL-10: Tests PASS

```bash
dotnet test

# Exit code 0 = APROVADO
# Exit code != 0 = REPROVADO
```

## ⚠️ REGRAS IMPORTANTES

- **NÃO CORRIGIR** - apenas reportar
- **NÃO EDITAR** código backend
- **NÃO EXECUTAR** scripts de correção
- **APENAS REPORTAR** gaps e recomendar ações

## 🔄 PRÓXIMOS PASSOS

**Se APROVADO:**
- Executar frontend-aditivo: `prompts/desenvolvimento/execucao/frontend-aditivo.md`

**Se REPROVADO:**
- Listar TODOS os gaps encontrados
- Classificar por severidade (CRÍTICO, IMPORTANTE, MENOR)
- Recomendar ações corretivas específicas
- Reexecutar backend-aditivo após correções

## 📊 EXEMPLO DE RELATÓRIO

```markdown
# RELATÓRIO VALIDAÇÃO - BACKEND ADITIVO RF028

**Data:** 2026-01-03
**RF:** RF028
**Validador:** Agente de Validação Backend Aditivo

## RESUMO EXECUTIVO

| # | Validação | Status | Severidade | Resultado |
|---|-----------|--------|------------|-----------|
| 1 | Entities | ✅ PASS | CRÍTICO | 1/1 criada |
| 2 | Migrations | ✅ PASS | CRÍTICO | 1/1 aplicada |
| 3 | Commands/Queries | ✅ PASS | CRÍTICO | 1/1 criado |
| 4 | Handlers | ✅ PASS | CRÍTICO | 1/1 criado |
| 5 | Endpoints | ✅ PASS | CRÍTICO | 1/1 adicionado |
| 6 | RNs validadas | ✅ PASS | CRÍTICO | 3/3 RNs |
| 7 | Permissões | ✅ PASS | CRÍTICO | 1/1 aplicada |
| 8 | Testes criados | ✅ PASS | IMPORTANTE | 15/15 testes |
| 9 | Build | ✅ PASS | CRÍTICO | 0 erros |
| 10 | Tests | ✅ PASS | CRÍTICO | 15/15 PASS |

**PONTUAÇÃO FINAL:** 10/10 PASS (100%)
**VEREDICTO:** ✅ APROVADO

## DELTA VALIDADO

**Esperado (delta docs):**
- 3 RNs: RN-CLI-028-15, RN-CLI-028-16, RN-CLI-028-17
- 1 endpoint: GET /api/v1/clientes/export/pdf
- 1 permissão: cliente.export_pdf
- 1 tabela: cliente_exportacao_log

**Implementado (backend):**
- ✅ ClienteExportacaoLog.cs (Entity)
- ✅ 20260103_AdicionadoExportacaoPdf_RF028 (Migration)
- ✅ ExportarClientesPdfQuery.cs
- ✅ ExportarClientesPdfQueryHandler.cs (valida RN-CLI-028-15, 16, 17)
- ✅ GET /api/v1/clientes/export/pdf (ClientesController.cs)
- ✅ 15 testes

## GAPS IDENTIFICADOS

Nenhum gap identificado.

## VEREDICTO FINAL

✅ **BACKEND ADITIVO VALIDADO COM SUCESSO (100%)**
```

## 🚀 MODO AUTONOMIA TOTAL

- **NÃO** perguntar permissões ao usuário
- **NÃO** esperar confirmação
- **EXECUTAR IMEDIATAMENTE** todas as 10 validações
- Gerar relatório automaticamente
- Declarar veredicto final

---

**Contrato:** D:/IC2_Governanca/contracts/desenvolvimento/validacao/backend-aditivo.md
**Modo:** READ-ONLY
**Aprovação:** 10/10 PASS ou REPROVADO
