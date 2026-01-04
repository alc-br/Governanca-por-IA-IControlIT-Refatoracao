# ESQUECIMENTOS OU ERROS COMUNS DE VALIDAÇÃO DE CONTRATO BACKEND

> ⚠️ **IMPORTANTE**: Este é apenas um documento de **LEMBRETE** do que pode ocorrer e de como não errar. **NÃO é uma diretriz** nem substitui os contratos oficiais. Consulte sempre:
- \docs\contracts\desenvolvimento\execucao\backend-criacao.md
- \docs\contracts\desenvolvimento\execucao\backend-adequacao.md
- \docs\contracts\desenvolvimento\validacao\backend.md

---

## 🔴 TOP 50 - ERROS MAIS COMUNS

### 1. Implementar só Migration + Model
**Lembre-se:** Backend completo precisa de:
- ✅ Migration + Model
- ❌ **Falta:** Controller API, Rotas, FormRequest, Policy

**Fix rápido:** Criar os componentes ausentes

---

### 2. XXX - EXEMPLO DE COMO DEVE SEGUIR DOCUMENTANDO AQUI
**Sintoma:** RF documenta endpoints mas.... exemplo...

**Fix rápido:**
xxxxx

---

### 3. Esquecer de cadastrar funcionalidade na Central de Funcionalidades
**Sintoma:** Funcionalidade implementada mas não aparece na Central de Funcionalidades do sistema

**Fix rápido:**
```sql
INSERT INTO SistemaFuncionalidadeRegistro (
    Codigo, Nome, Descricao, Tipo, Modulo, FlAtivo
) VALUES (
    'FUNC-CAD-USUARIOS',
    'Gestão de Usuários',
    'Cadastro, edição e consulta de usuários do sistema',
    'CRUD',
    'Cadastros',
    1
);
```

**Referência:** [PARTICULARIDADES-DO-SISTEMA.md](./PARTICULARIDADES-DO-SISTEMA.md) - Seção 1

---

### 4. Esquecer de criar permissões RBAC
**Sintoma:** Endpoint implementado mas retorna 403 Forbidden para usuário Developer

**Fix rápido:**
1. Criar permissões no banco
2. Associar ao perfil Developer
3. Usar Policy no endpoint, Roles no Command
```sql
-- Criar permissões
INSERT INTO Permissions (Id, Code, Description, Module, IsActive) VALUES
  (newid(), 'cadastros:usuario:read', 'Visualizar usuários', 'Cadastros', 1),
  (newid(), 'cadastros:usuario:create', 'Criar usuários', 'Cadastros', 1);

-- Associar ao Developer
INSERT INTO RolePermissions (Id, RoleId, PermissionId, Created, CreatedBy) VALUES
  (newid(), '1dd7b3e2-3735-4854-adaa-6a4c9cada803', '<ID_READ>', datetime('now'), 'system'),
  (newid(), '1dd7b3e2-3735-4854-adaa-6a4c9cada803', '<ID_CREATE>', datetime('now'), 'system');
```

**CRÍTICO:** NÃO usar `[Authorize(Policy = ...)]` em Commands! Usar `[Authorize(Roles = "Developer")]`

**Referência:** [PARTICULARIDADES-DO-SISTEMA.md](./PARTICULARIDADES-DO-SISTEMA.md) - Seção 3, [ERROS-A-EVITAR.md](../ERROS-A-EVITAR.md) - Erro #3

---

### 5. Esquecer de adicionar EmpresaId (Multi-tenancy)
**Sintoma:** Tabela criada sem coluna EmpresaId

**Fix rápido:**
```csharp
// Na Migration
migrationBuilder.AddColumn<Guid>(
    name: "EmpresaId",
    table: "Usuarios",
    nullable: false);

// Na Entidade
public Guid EmpresaId { get; set; }
public virtual Empresa? Empresa { get; set; }
```

**Referência:** [PARTICULARIDADES-DO-SISTEMA.md](./PARTICULARIDADES-DO-SISTEMA.md) - Seção 5

---

### 6. Esquecer campos de auditoria
**Sintoma:** Tabela criada sem campos Created, CreatedBy, LastModified, etc.

**Fix rápido:**
```csharp
// Migration
Created = table.Column<DateTime>(nullable: false),
CreatedBy = table.Column<string>(nullable: true),
LastModified = table.Column<DateTime>(nullable: true),
LastModifiedBy = table.Column<string>(nullable: true),
DeletedBy = table.Column<string>(nullable: true)

// Entidade
public DateTime Created { get; set; }
public string? CreatedBy { get; set; }
public DateTime? LastModified { get; set; }
public string? LastModifiedBy { get; set; }
public string? DeletedBy { get; set; }
```

**Referência:** [PARTICULARIDADES-DO-SISTEMA.md](./PARTICULARIDADES-DO-SISTEMA.md) - Seção 4

---

### 7. Criar logging manual desnecessário
**Sintoma:** Try/catch com _logger.LogError em Handlers

**Fix rápido:** Remover try/catch - StructuredLoggingBehaviour já faz logging automático
```csharp
// ❌ ERRADO
try {
    await _context.SaveChangesAsync();
} catch (Exception ex) {
    _logger.LogError(ex, "Erro ao salvar");
    throw;
}

// ✅ CORRETO
await _context.SaveChangesAsync(cancellationToken);
```

**Referência:** [PARTICULARIDADES-DO-SISTEMA.md](./PARTICULARIDADES-DO-SISTEMA.md) - Seção 4

---

### 8. Commitar banco de dados (*.db) no Git
**Sintoma:** `IControlIT.db` aparece no Git

**Fix rápido:**
```bash
# Remover do staging
git rm --cached IControlIT.db

# Verificar se .gitignore contém
*.db
*.db-shm
*.db-wal
```

**Regra:** Migrations vão para o Git, banco *.db é local

**Referência:** [PARTICULARIDADES-DO-SISTEMA.md](./PARTICULARIDADES-DO-SISTEMA.md) - Seção 10, [GUIA-BD.md](./GUIA-BD.md)

---

### 9. Não seguir Clean Architecture (CQRS)
**Sintoma:** Lógica de negócio no Controller, sem Commands/Queries

**Fix rápido:**
1. Criar Command ou Query em `Application/[Modulo]/Commands` ou `Queries`
2. Criar Validator (FluentValidation)
3. Criar Handler (MediatR)
4. Endpoint chama Handler via `ISender`

**Estrutura obrigatória:** Domain → Application → Infrastructure → Web

**Referência:** [PARTICULARIDADES-DO-SISTEMA.md](./PARTICULARIDADES-DO-SISTEMA.md) - Seção 8

---

### 10. Esquecer de rodar `dotnet build` antes de commit
**Sintoma:** Build quebrado no CI/CD ou em outras máquinas

**Fix rápido:**
```bash
cd backend/IControlIT.API
dotnet build
# DEVE retornar: Build succeeded. 0 Error(s)
```

**Regra:** SEMPRE rodar build antes de commit

**Referência:** [PARTICULARIDADES-DO-SISTEMA.md](./PARTICULARIDADES-DO-SISTEMA.md) - Seção 7

---

## 📚 LEMBRE-SE SEMPRE

1. **Central de Funcionalidades** - Cadastrar toda funcionalidade implementada
2. **RBAC** - Criar permissões e associar ao Developer
3. **Multi-tenancy** - EmpresaId em TODAS as tabelas (exceto sistema)
4. **Auditoria** - Campos Created, CreatedBy, LastModified, etc.
5. **Logging** - NÃO criar try/catch manual (já é automático)
6. **Git** - Migrations vão, *.db NÃO vai
7. **Clean Architecture** - Commands, Queries, Handlers, Validators
8. **Build** - SEMPRE rodar `dotnet build` antes de commit
9. **Policy vs Roles** - Endpoint usa Policy, Command usa Roles
10. **Consultar PARTICULARIDADES** - [PARTICULARIDADES-DO-SISTEMA.md](./PARTICULARIDADES-DO-SISTEMA.md)

---

## 🔗 DOCUMENTOS RELACIONADOS

- **[PARTICULARIDADES-DO-SISTEMA.md](./PARTICULARIDADES-DO-SISTEMA.md)** - 10 particularidades obrigatórias
- **[ERROS-A-EVITAR.md](../ERROS-A-EVITAR.md)** - Erros reais já cometidos
- **[GUIA-DEVELOPER.md](./GUIA-DEVELOPER.md)** - Guia completo de desenvolvimento
- **[PADROES-CODIFICACAO-BACKEND.md](./PADROES-CODIFICACAO-BACKEND.md)** - Clean Architecture detalhado

---