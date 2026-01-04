# Backend Aditivo RFXXX - Implementar Delta no Backend

Ele fica nesse endereço \docs\rf\Fase*\EPIC*\RF*

**Instruções:** Altere RFXXX acima para o RF desejado (ex: RF001, RF025, RF028).

---

Executar **BACKEND ADITIVO** para o RF informado acima conforme docs/contracts/desenvolvimento/execucao/backend-aditivo.md.
Seguir CLAUDE.md.

## 📋 PRÉ-REQUISITOS OBRIGATÓRIOS

Antes de executar este prompt, você **DEVE** ter:

1. ✅ Executado aditivo de documentação: `docs/prompts/documentacao/execucao/aditivo.md`
2. ✅ Validado aditivo de documentação: `docs/prompts/documentacao/validacao/aditivo.md` (APROVADO)
3. ✅ Relatório de delta existe: `.temp_ia/aditivo-RFXXX-delta-report.md`
4. ✅ Arquivos `_old` existem (10 arquivos)
5. ✅ Branch correto: `feature/RFXXX-aditivo-*`

**Se qualquer pré-requisito falhar:**
➡️ **BLOQUEIO TOTAL**. Execute os passos anteriores primeiro.

---

## 🔄 WORKFLOW DE EXECUÇÃO

### FASE 1: ANÁLISE DE DELTA

1. **Comparar documentos originais vs `_old`**
   ```bash
   diff RFXXX.md RFXXX_old.md
   diff UC-RFXXX.yaml UC-RFXXX_old.yaml
   diff MD-RFXXX.yaml MD-RFXXX_old.yaml
   ```

2. **Ler relatório de delta**
   ```bash
   cat .temp_ia/aditivo-RFXXX-delta-report.md
   ```

3. **Identificar o que implementar**
   - Novos endpoints → novos Commands/Queries
   - Novas RNs → validações em Handlers
   - Novas tabelas/campos → Migrations
   - Novas permissões → Authorization

---

### FASE 2: IMPLEMENTAÇÃO INCREMENTAL

#### Passo 1: Criar/Atualizar Entities (se MD mudou)

**Verificar:**
```bash
diff MD-RFXXX.yaml MD-RFXXX_old.yaml
```

**Se houve mudanças:**
- Criar novas entidades em `src/Domain/Entities/`
- Garantir multi-tenancy (`ClienteId`)
- Garantir auditoria (5 campos)
- Garantir soft delete (`DeletedAt`)

**Exemplo:**
```csharp
public class ClienteExportacaoLog : BaseAuditableEntity
{
    public int Id { get; set; }
    public int ClienteId { get; set; }  // Multi-tenancy
    public DateTime DataExportacao { get; set; }
    public string FormatoExportacao { get; set; } = string.Empty;

    // Auditoria (herdado de BaseAuditableEntity):
    // CreatedAt, CreatedBy, UpdatedAt, UpdatedBy, DeletedAt
}
```

---

#### Passo 2: Criar Migrations (se MD mudou)

```bash
cd backend/IControlIT.API
dotnet ef migrations add AdicionadoFuncionalidadeX_RFXXX
```

---

#### Passo 3: Criar Commands/Queries

**Para cada novo endpoint identificado no delta:**

Exemplo (endpoint GET /api/v1/clientes/export/pdf):
```csharp
// src/Application/Clientes/Queries/ExportarClientesPdf/ExportarClientesPdfQuery.cs
public record ExportarClientesPdfQuery : IRequest<ExportarClientesPdfResult>
{
    public int? ClienteId { get; init; }
    public DateTime? DataInicio { get; init; }
    public DateTime? DataFim { get; init; }
}
```

---

#### Passo 4: Criar Handlers

**Implementar lógica de negócio:**
- Validar **TODAS** as RNs novas (identificadas no delta)
- Aplicar permissões

Exemplo:
```csharp
// ExportarClientesPdfQueryHandler.cs
public class ExportarClientesPdfQueryHandler : IRequestHandler<ExportarClientesPdfQuery, ExportarClientesPdfResult>
{
    public async Task<ExportarClientesPdfResult> Handle(...)
    {
        // RN-CLI-028-15: Sistema DEVE gerar PDF com logo da empresa
        if (!logoEmpresaExiste)
            throw new ValidationException("Logo da empresa não configurada");

        // RN-CLI-028-16: Sistema DEVE permitir exportação com filtros aplicados
        var clientesFiltrados = await AplicarFiltros(query);

        // RN-CLI-028-17: Sistema DEVE validar permissão antes de exportar
        if (!user.HasPermission(Permissions.Cliente.ExportPdf))
            throw new ForbiddenAccessException();

        // Gerar PDF...
    }
}
```

---

#### Passo 5: Criar/Atualizar Endpoints

Adicionar endpoints em `src/Web/Endpoints/`

Exemplo:
```csharp
// ClientesController.cs
[HttpGet("export/pdf")]
[Authorize(Policy = Permissions.Cliente.ExportPdf)]
public async Task<IActionResult> ExportarPdf([FromQuery] ExportarClientesPdfQuery query)
{
    var result = await Mediator.Send(query);
    return File(result.Pdf, "application/pdf", $"clientes-{DateTime.Now:yyyyMMdd}.pdf");
}
```

---

#### Passo 6: Criar Testes

**Para cada novo Command/Query/Handler:**

```csharp
// ExportarClientesPdfQueryTests.cs
[TestFixture]
public class ExportarClientesPdfQueryTests
{
    [Test]
    public async Task Handle_QuandoLogoNaoExiste_DeveLancarValidationException()
    {
        // Arrange
        // Act
        // Assert - RN-CLI-028-15
    }

    [Test]
    public async Task Handle_QuandoFiltrosAplicados_DeveRetornarClientesFiltrados()
    {
        // Arrange
        // Act
        // Assert - RN-CLI-028-16
    }

    [Test]
    public async Task Handle_QuandoUsuarioSemPermissao_DeveLancarForbiddenAccessException()
    {
        // Arrange
        // Act
        // Assert - RN-CLI-028-17
    }
}
```

---

### FASE 3: VALIDAÇÃO E BUILD

#### Passo 7: Build

```bash
cd backend/IControlIT.API
dotnet build
```

**Resultado esperado:** ✅ Build PASS (0 erros)

---

#### Passo 8: Executar Testes

```bash
dotnet test
```

**Resultado esperado:** ✅ Testes PASS (100%)

---

#### Passo 9: Aplicar Migrations (dev)

```bash
dotnet ef database update
```

**Resultado esperado:** ✅ Migrations aplicadas com sucesso

---

### FASE 4: RELATÓRIO

#### Passo 10: Gerar Relatório

Criar `.temp_ia/backend-aditivo-RFXXX-relatorio.md`:

```markdown
# RELATÓRIO DE IMPLEMENTAÇÃO - BACKEND ADITIVO RFXXX

**Data:** YYYY-MM-DD
**RF:** RFXXX
**Funcionalidade:** [Nome da funcionalidade adicionada]

---

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

---

## VALIDAÇÕES

- ✅ Build: PASS (0 erros)
- ✅ Testes: 15/15 PASS (100%)
- ✅ Migrations: Aplicadas com sucesso

---

## VEREDICTO FINAL

✅ **BACKEND ADITIVO IMPLEMENTADO COM SUCESSO**

Todos os itens do delta foram implementados com sucesso.
Build, testes e migrations passaram sem erros.
```

---

## ✅ CRITÉRIOS DE APROVAÇÃO

**APROVADO:**
- ✅ Build PASS (0 erros)
- ✅ Testes PASS (100%)
- ✅ Migrations aplicadas (se aplicável)
- ✅ Relatório completo

**REPROVADO:**
- ❌ Build FAIL
- ❌ Qualquer teste FAIL
- ❌ Migrations falharam
- ❌ Relatório incompleto

---

## 🚨 REGRAS IMPORTANTES

- **SEMPRE** comparar documentos originais vs `_old` antes de implementar
- **SEMPRE** ler relatório de delta (`.temp_ia/aditivo-RFXXX-delta-report.md`)
- **SEMPRE** validar TODAS as RNs novas nos Handlers
- **SEMPRE** criar testes para novos Commands/Queries/Handlers
- **SEMPRE** garantir build e testes PASS antes de concluir
- **SEMPRE** gerar relatório de implementação

---

## 🔄 PRÓXIMOS PASSOS

**Após aprovação deste prompt:**
1. Executar validação backend: `docs/contracts/desenvolvimento/validacao/backend-aditivo.md`
2. Se aprovado: Executar frontend-aditivo
3. Se aprovado: Commit e merge

---

## 💡 EXEMPLO PRÁTICO

**Delta identificado:**
- 3 RNs: RN-CLI-028-15, RN-CLI-028-16, RN-CLI-028-17
- 1 endpoint: GET /api/v1/clientes/export/pdf
- 1 permissão: cliente.export_pdf
- 1 tabela: cliente_exportacao_log

**Implementação:**
1. ✅ ClienteExportacaoLog.cs
2. ✅ Migration AdicionadoExportacaoPdf_RF028
3. ✅ ExportarClientesPdfQuery.cs
4. ✅ ExportarClientesPdfQueryHandler.cs (valida RN-CLI-028-15, 16, 17)
5. ✅ GET /api/v1/clientes/export/pdf em ClientesController.cs
6. ✅ ExportarClientesPdfQueryTests.cs (15 testes)
7. ✅ Build + Test + Migrate
8. ✅ Relatório gerado

---

**Contrato:** docs/contracts/desenvolvimento/execucao/backend-aditivo.md
**Modo:** Governança rígida
**Aprovação:** Build PASS + Testes PASS + Relatório completo
