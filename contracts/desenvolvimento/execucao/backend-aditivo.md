# CONTRATO DE EXECUÇÃO — BACKEND ADITIVO

**Versão:** 1.0
**Data:** 2026-01-03
**Status:** Ativo

---

## 📋 SUMÁRIO EXECUTIVO

Este contrato **implementa incrementalmente no backend** as mudanças especificadas no ADITIVO de documentação (RF, UC, MD).

**Entrada:**
- Documentos originais: RFXXX.md, UC-RFXXX.yaml, MD-RFXXX.yaml
- Documentos `_old`: RFXXX_old.md, UC-RFXXX_old.yaml, MD-RFXXX_old.yaml
- Relatório de delta: `.temp_ia/aditivo-RFXXX-delta-report.md`

**Saída:**
- Código backend atualizado (Commands, Queries, Handlers, Endpoints)
- Migrations atualizadas (se aplicável)
- Testes atualizados
- Relatório de implementação: `.temp_ia/backend-aditivo-RFXXX-relatorio.md`

---

## 1. Ativação

```
Conforme docs/contracts/desenvolvimento/execucao/backend-aditivo.md para RFXXX.
Seguir CLAUDE.md.
```

---

## 2. Pré-Requisitos Bloqueantes

| # | Pré-Requisito | Verificação |
|---|---------------|-------------|
| 1 | ADITIVO de documentação executado | ✅ Arquivos `_old` existem |
| 2 | ADITIVO de documentação validado | ✅ Validação APROVADA |
| 3 | Relatório de delta existe | ✅ `.temp_ia/aditivo-RFXXX-delta-report.md` |
| 4 | Backend original existe | ✅ Commands, Queries, Handlers existem |
| 5 | Branch correto | ✅ `feature/RFXXX-aditivo-*` ativo |

---

## 3. Workflow de Execução

### FASE 1: ANÁLISE DE DELTA

**Passo 1:** Comparar documentos originais vs `_old`

```bash
# Identificar mudanças
diff RFXXX.md RFXXX_old.md
diff UC-RFXXX.yaml UC-RFXXX_old.yaml
diff MD-RFXXX.yaml MD-RFXXX_old.yaml
```

**Passo 2:** Ler relatório de delta

```bash
# Extrair o que foi adicionado
cat .temp_ia/aditivo-RFXXX-delta-report.md
```

**Passo 3:** Identificar o que deve ser implementado

- Novos endpoints (novos Commands/Queries)
- Novas RNs (validações em Handlers)
- Novas tabelas/campos (Migrations)
- Novas permissões (Authorization)

**Checkpoint:**
- ✅ Delta identificado
- ✅ Lista de implementações criada

---

### FASE 2: IMPLEMENTAÇÃO INCREMENTAL

**Passo 4:** Criar/Atualizar Entities (se aplicável)

- Se MD foi atualizado (novas tabelas/campos)
- Adicionar entidades em `src/Domain/Entities/`
- Garantir multi-tenancy (`ClienteId`)
- Garantir auditoria (5 campos)
- Garantir soft delete (`DeletedAt`)

**Passo 5:** Criar Migrations (se aplicável)

```bash
dotnet ef migrations add AdicionadoFuncionalidadeX_RFXXX
```

**Passo 6:** Criar/Atualizar Commands e Queries

- Para cada novo endpoint identificado no delta
- Seguir padrão CQRS
- Exemplo:
  - Novo endpoint: `POST /api/v1/clientes/export/pdf`
  - Criar: `ExportarClientesPdfQuery.cs`

**Passo 7:** Criar/Atualizar Handlers

- Implementar lógica de negócio
- Validar RNs novas (identificadas no delta)
- Aplicar permissões novas
- Exemplo:
  - `ExportarClientesPdfQueryHandler.cs`
  - Validar RN-CLI-028-15, RN-CLI-028-16, RN-CLI-028-17

**Passo 8:** Criar/Atualizar Endpoints (Controllers)

- Adicionar endpoints em `src/Web/Endpoints/`
- Aplicar Authorization
- Exemplo:
  ```csharp
  [HttpGet("export/pdf")]
  [Authorize(Policy = Permissions.Cliente.ExportPdf)]
  public async Task<IActionResult> ExportarPdf([FromQuery] ExportarClientesPdfQuery query)
  {
      var result = await Mediator.Send(query);
      return File(result.Pdf, "application/pdf", $"clientes-{DateTime.Now:yyyyMMdd}.pdf");
  }
  ```

**Passo 9:** Atualizar Testes

- Criar testes para novos Commands/Queries/Handlers
- Garantir cobertura de RNs novas
- Executar: `dotnet test`

**Checkpoint:**
- ✅ Código implementado
- ✅ Migrations criadas (se aplicável)
- ✅ Testes passando

---

### FASE 3: VALIDAÇÃO E BUILD

**Passo 10:** Build do backend

```bash
cd backend/IControlIT.API
dotnet build
```

**Passo 11:** Executar testes

```bash
dotnet test
```

**Passo 12:** Aplicar migrations (dev)

```bash
dotnet ef database update
```

**Checkpoint:**
- ✅ Build PASS
- ✅ Testes PASS
- ✅ Migrations aplicadas

---

### FASE 4: RELATÓRIO

**Passo 13:** Gerar relatório de implementação

Criar `.temp_ia/backend-aditivo-RFXXX-relatorio.md` com:

```markdown
# RELATÓRIO DE IMPLEMENTAÇÃO - BACKEND ADITIVO RFXXX

## DELTA IMPLEMENTADO

### Entities
- ✅ ClienteExportacaoLog.cs (nova entidade)

### Migrations
- ✅ 20260103_AdicionadoExportacaoPdf_RF028

### Commands/Queries
- ✅ ExportarClientesPdfQuery.cs

### Handlers
- ✅ ExportarClientesPdfQueryHandler.cs
- ✅ Validações: RN-CLI-028-15, RN-CLI-028-16, RN-CLI-028-17

### Endpoints
- ✅ GET /api/v1/clientes/export/pdf

### Testes
- ✅ 15 testes criados (ExportarClientesPdfQueryTests.cs)

## VALIDAÇÕES

- ✅ Build: PASS
- ✅ Testes: 15/15 PASS (100%)
- ✅ Migrations: Aplicadas com sucesso

## VEREDICTO

✅ **BACKEND ADITIVO IMPLEMENTADO COM SUCESSO**
```

**Checkpoint:**
- ✅ Relatório gerado

---

## 4. Critérios de Aprovação

**✅ APROVADO:**
- Build PASS
- Testes PASS (100%)
- Migrations aplicadas (se aplicável)
- Relatório completo

**❌ REPROVADO:**
- Build FAIL
- Qualquer teste FAIL
- Migrations falharam
- Relatório incompleto

---

## 5. Exemplo Prático

**Entrada:**
- RF028: Adicionada funcionalidade "Exportação em PDF"
- Delta: 3 RNs, 1 endpoint, 1 permissão, 1 tabela

**Execução:**
1. Criar `ClienteExportacaoLog.cs` (Entity)
2. Criar migration `AdicionadoExportacaoPdf_RF028`
3. Criar `ExportarClientesPdfQuery.cs`
4. Criar `ExportarClientesPdfQueryHandler.cs` (validar RN-CLI-028-15, RN-CLI-028-16, RN-CLI-028-17)
5. Adicionar endpoint `GET /api/v1/clientes/export/pdf` em `ClientesController.cs`
6. Criar `ExportarClientesPdfQueryTests.cs` (15 testes)
7. Build + Test + Migrate
8. Gerar relatório

**Saída:**
✅ BACKEND ADITIVO IMPLEMENTADO COM SUCESSO

---

## 6. Regras Invioláveis

1. **SEMPRE** comparar documentos originais vs `_old` antes de implementar
2. **SEMPRE** ler relatório de delta (`.temp_ia/aditivo-RFXXX-delta-report.md`)
3. **SEMPRE** validar TODAS as RNs novas nos Handlers
4. **SEMPRE** criar testes para novos Commands/Queries/Handlers
5. **SEMPRE** garantir build e testes PASS antes de concluir
6. **SEMPRE** gerar relatório de implementação

---

## 7. Versionamento

- **Criado em:** 2026-01-03
- **Versão:** 1.0

---

**Mantido por:** Time de Arquitetura IControlIT
**Governado por:** CLAUDE.md
