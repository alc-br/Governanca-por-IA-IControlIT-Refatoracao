# PARTICULARIDADES DO SISTEMA ICONTROLIT

**Versão:** 1.0
**Data:** 2026-01-01
**Objetivo:** Documentar requisitos e particularidades específicas do sistema IControlIT que devem ser seguidas em TODAS as implementações.

---

## 🎯 Visão Geral

Este documento lista **particularidades específicas do sistema IControlIT** que DEVEM ser implementadas em toda funcionalidade criada.

**Diferença entre este documento e os contratos:**
- **Contratos:** Governança genérica e portável (aplicável a qualquer projeto)
- **Este documento:** Particularidades específicas do IControlIT (não aplicáveis a outros sistemas)

**Uso obrigatório:**
- ✅ Consultar ANTES de implementar qualquer funcionalidade
- ✅ Validar APÓS implementação (checklist)
- ✅ Atualizar quando novas particularidades forem identificadas

---

## 📋 CHECKLIST DE PARTICULARIDADES OBRIGATÓRIAS

Toda funcionalidade implementada no IControlIT DEVE atender:

- [ ] **1. Central de Funcionalidades** - Cadastrada e registrada
- [ ] **2. i18n (Transloco)** - Traduzido em pt-BR, en, es
- [ ] **3. RBAC (Permissões)** - Permissões criadas e associadas ao perfil Developer
- [ ] **4. Auditoria Automática** - Logs estruturados em todas as operações
- [ ] **5. Multi-tenancy** - EmpresaId em todas as tabelas
- [ ] **6. Fuse Template** - Padrões visuais consistentes
- [ ] **7. Build e Validação** - Backend + Frontend rodando sem erros
- [ ] **8. Clean Architecture** - CQRS + MediatR no backend
- [ ] **9. Standalone Components** - Angular 19 sem NgModules
- [ ] **10. Banco de Dados** - Migrations no Git, *.db local apenas

---

## 1️⃣ CENTRAL DE FUNCIONALIDADES

### Descrição
Todo funcionalidade implementada DEVE ser cadastrada na **Central de Funcionalidades** do sistema.

### Quando aplicar
- ✅ Após implementar CRUD completo (backend + frontend)
- ✅ Antes de marcar RF como concluído
- ✅ Em TODAS as funcionalidades (sem exceção)

### Como implementar

**Backend:** Inserir registro na tabela `SistemaFuncionalidadeRegistro`

```sql
INSERT INTO SistemaFuncionalidadeRegistro (
    Codigo,
    Nome,
    Descricao,
    Tipo,
    Modulo,
    FlAtivo
) VALUES (
    'FUNC-CAD-USUARIOS',
    'Gestão de Usuários',
    'Cadastro, edição e consulta de usuários do sistema',
    'CRUD',
    'Cadastros',
    1
);
```

**Campos obrigatórios:**
- `Codigo` - Código único (padrão: FUNC-{MODULO}-{NOME})
- `Nome` - Nome da funcionalidade (exibido na Central)
- `Descricao` - Descrição breve do que a funcionalidade faz
- `Tipo` - Tipo (CRUD, Relatório, Dashboard, etc.)
- `Modulo` - Módulo ao qual pertence (Cadastros, Financeiro, etc.)
- `FlAtivo` - 1 = Ativo, 0 = Inativo

### Validação
```sql
-- Verificar se funcionalidade foi cadastrada
SELECT * FROM SistemaFuncionalidadeRegistro
WHERE Codigo = 'FUNC-CAD-USUARIOS';
```

**Referências:**
- [GUIA-DEVELOPER.md](./GUIA-DEVELOPER.md) - Seção "6.4. Central de Funcionalidades"

---

## 2️⃣ i18n (INTERNACIONALIZAÇÃO COM TRANSLOCO)

### Descrição
TODAS as funcionalidades DEVEM ser traduzidas para **3 idiomas obrigatórios:**
- pt-BR (Português do Brasil) - **IDIOMA PRINCIPAL**
- en (Inglês)
- es (Espanhol)

### Quando aplicar
- ✅ Em TODOS os textos visíveis no frontend
- ✅ Em TODAS as mensagens TypeScript (confirmações, toasts, erros)
- ✅ Em TODOS os componentes Angular Material (MatPaginator, etc.)

### Como implementar

**16 PONTOS OBRIGATÓRIOS DE TRADUÇÃO:**

1. ✅ Templates HTML - Títulos, subtítulos, labels
2. ✅ Mensagens TypeScript - Confirmações, diálogos, tooltips
3. ✅ Validações Frontend - Mensagens de erro de formulário
4. ✅ Validações Backend - Mensagens de erro da API (.NET)
5. ✅ Toasts e Notificações - Mensagens de sucesso/erro
6. ✅ Tooltips e Hints - Ajudas contextuais
7. ✅ Badges e Status - Labels de status, badges visuais
8. ✅ Breadcrumbs e Navegação - Títulos de navegação
9. ✅ Tabelas e Grid - Cabeçalhos de colunas, mensagens "sem dados"
10. ✅ Paginação - Labels do MatPaginator
11. ✅ Filtros - Labels e opções de filtros
12. ✅ Diálogos de Confirmação - Títulos, mensagens, botões
13. ✅ Mensagens de Erro HTTP - Tratamento de erros da API
14. ✅ Pluralização - Textos que mudam com quantidade
15. ✅ Interpolação - Textos com variáveis dinâmicas
16. ✅ Componentes do Angular Material - MatPaginator, MatDatepicker

**Estrutura de arquivos:**
```
frontend/icontrolit-app/public/i18n/
├── pt.json     ← Português (Brasil)
├── en.json     ← Inglês
└── es.json     ← Espanhol
```

**Exemplo de uso:**

**Template (HTML):**
```html
<h2>{{ 'users.title' | transloco }}</h2>
<button mat-flat-button>{{ 'users.new-user' | transloco }}</button>
```

**TypeScript:**
```typescript
import { TranslocoService } from '@jsverse/transloco';

private _translocoService = inject(TranslocoService);

deleteUsuario(usuario: Usuario): void {
  const confirmation = this._fuseConfirmationService.open({
    title: this._translocoService.translate('users.dialog-delete-title'),
    message: this._translocoService.translate('users.dialog-delete-message', {
      nome: usuario.nome
    })
  });
}
```

**Arquivo i18n (pt.json):**
```json
{
  "users": {
    "title": "Usuários",
    "new-user": "Novo Usuário",
    "dialog-delete-title": "Excluir usuário",
    "dialog-delete-message": "Tem certeza que deseja excluir {{nome}}?"
  }
}
```

### Validação
```bash
# Verificar chaves faltantes
npm run i18n:validate

# Corrigir automaticamente
npm run i18n:fix
```

**Checklist de validação:**
- [ ] Todas as chaves existem em pt.json, en.json, es.json
- [ ] Nenhum texto hardcoded em templates HTML
- [ ] Nenhuma mensagem hardcoded em TypeScript
- [ ] MatPaginator configurado com CustomMatPaginatorIntl
- [ ] Testado troca de idioma em tempo real

**Referências:**
- [GUIA-TRANSLATE.md](./GUIA-TRANSLATE.md) - Guia completo de i18n (16 pontos)
- [GUIA-DEVELOPER.md](./GUIA-DEVELOPER.md) - Seção "6.1. Sistema de i18n"

---

## 3️⃣ RBAC (PERMISSÕES E AUTORIZAÇÃO)

### Descrição
TODAS as funcionalidades DEVEM ter permissões RBAC (Role-Based Access Control) criadas e associadas ao perfil Developer.

### Quando aplicar
- ✅ Ao criar endpoints de API (backend)
- ✅ Ao criar botões/ações no frontend
- ✅ ANTES de marcar funcionalidade como concluída

### Como implementar

**1. Criar permissões no banco de dados:**

```sql
-- Exemplo: RF-008 Empresas
INSERT INTO Permissions (Id, Code, Description, Module, IsActive) VALUES
  (newid(), 'cadastros:empresa:read', 'Visualizar empresas', 'Cadastros', 1),
  (newid(), 'cadastros:empresa:create', 'Criar empresas', 'Cadastros', 1),
  (newid(), 'cadastros:empresa:update', 'Editar empresas', 'Cadastros', 1),
  (newid(), 'cadastros:empresa:delete', 'Excluir empresas', 'Cadastros', 1);
```

**2. Associar permissões ao perfil Developer:**

```sql
-- ID do perfil Developer: 1dd7b3e2-3735-4854-adaa-6a4c9cada803
INSERT INTO RolePermissions (Id, RoleId, PermissionId, Created, CreatedBy) VALUES
  (newid(), '1dd7b3e2-3735-4854-adaa-6a4c9cada803', '<ID_PERMISSAO_READ>', datetime('now'), 'system'),
  (newid(), '1dd7b3e2-3735-4854-adaa-6a4c9cada803', '<ID_PERMISSAO_CREATE>', datetime('now'), 'system'),
  (newid(), '1dd7b3e2-3735-4854-adaa-6a4c9cada803', '<ID_PERMISSAO_UPDATE>', datetime('now'), 'system'),
  (newid(), '1dd7b3e2-3735-4854-adaa-6a4c9cada803', '<ID_PERMISSAO_DELETE>', datetime('now'), 'system');
```

**3. Backend - Endpoint usa Policy:**

```csharp
// ✅ CORRETO
groupBuilder.MapDelete(DeleteEmpresa, "{id}/permanent")
    .RequireAuthorization(AuthorizationPolicies.CompaniesPermanentDelete);
```

**4. Backend - Command usa Roles:**

```csharp
// ✅ CORRETO
[Authorize(Roles = "Developer,Super Admin")]
public record DeleteEmpresaCommand(Guid Id) : IRequest;

// ❌ ERRADO - NÃO use Policy em Command (causa erro 403!)
[Authorize(Policy = EmpresasPermissions.PermanentDelete)]
public record DeleteEmpresaCommand(Guid Id) : IRequest;
```

**5. Frontend - Diretiva hasPermission:**

```html
<button
    mat-raised-button
    *hasPermission="'Users.Create'">
    Criar Usuário
</button>
```

### Regra CRÍTICA: Policy vs Roles

⚠️ **ERRO COMUM QUE CAUSA 403:**

| Camada | Usar | Exemplo |
|--------|------|---------|
| **Endpoint (Minimal API)** | Policy-based | `.RequireAuthorization(AuthorizationPolicies.X)` |
| **Command/Query** | Role-based | `[Authorize(Roles = "Developer")]` |

**NÃO use `[Authorize(Policy = ...)]` em Commands!** Isso causa erro 403.

### Validação

**Teste de autorização:**
```python
import requests

# 1. Login
response = requests.post("http://localhost:5000/api/auth/login", ...)
token = response.json()['accessToken']

# 2. Testar endpoint com permissão
response = requests.get(
    "http://localhost:5000/api/usuarios",
    headers={"Authorization": f"Bearer {token}"}
)

# 3. Verificar resultado
assert response.status_code == 200  # Não deve retornar 403!
```

**Checklist:**
- [ ] Permissões criadas no banco
- [ ] Permissões associadas ao perfil Developer
- [ ] Endpoint usa `.RequireAuthorization(Policy)`
- [ ] Command usa `[Authorize(Roles = "...")]`
- [ ] Frontend usa `*hasPermission`
- [ ] Testado com usuário Developer (não retorna 403)

**Referências:**
- [GUIA-DEVELOPER.md](./GUIA-DEVELOPER.md) - Seção "6.3. Sistema de Autorização e Permissões"
- [ERROS-A-EVITAR.md](../ERROS-A-EVITAR.md) - Erro #3 (Policy vs Roles)

---

## 4️⃣ AUDITORIA E LOGGING AUTOMÁTICO

### Descrição
TODAS as operações DEVEM ser auditadas automaticamente via **StructuredLoggingBehaviour**.

### Quando aplicar
- ✅ Já está implementado automaticamente via MediatR
- ✅ NÃO precisa criar try/catch para logging
- ✅ Apenas deixar exceções propagarem

### Como funciona

**StructuredLoggingBehaviour** já loga automaticamente:
- ✅ Toda requisição MediatR (Commands e Queries)
- ✅ Usuário que executou a ação
- ✅ Data/hora da operação
- ✅ IP de origem
- ✅ Duração da operação
- ✅ Erros com stack trace completo

**Backend - NÃO precisa fazer:**
```csharp
// ❌ ERRADO (logging manual desnecessário)
try {
    await _context.SaveChangesAsync();
} catch (Exception ex) {
    _logger.LogError(ex, "Erro ao salvar");
    throw;
}

// ✅ CORRETO (deixar exceção propagar, StructuredLoggingBehaviour loga)
await _context.SaveChangesAsync(cancellationToken);
```

### Campos de auditoria obrigatórios em entidades

Todas as entidades DEVEM ter:
```csharp
public DateTime Created { get; set; }
public string? CreatedBy { get; set; }
public DateTime? LastModified { get; set; }
public string? LastModifiedBy { get; set; }
public string? DeletedBy { get; set; }
```

**AuditInterceptor** preenche automaticamente via EF Core.

### Validação

**Consultar logs:**
```sql
-- Logs de auditoria
SELECT * FROM AuditLog
WHERE EntityType = 'Usuario'
ORDER BY Created DESC;
```

**Checklist:**
- [ ] Entidade tem campos de auditoria (Created, CreatedBy, etc.)
- [ ] NÃO há try/catch desnecessário para logging
- [ ] Logs estruturados aparecem no console
- [ ] Tabela AuditLog registra operações

**Referências:**
- [GUIA-DEVELOPER.md](./GUIA-DEVELOPER.md) - Seção "6.2. Sistema de Auditoria"

---

## 5️⃣ MULTI-TENANCY (EMPRESAID EM TODAS AS TABELAS)

### Descrição
TODAS as tabelas (exceto tabelas de sistema) DEVEM ter coluna `EmpresaId` para isolamento multi-tenant.

### Quando aplicar
- ✅ Ao criar novas tabelas (migrations)
- ✅ Em TODAS as entidades de domínio
- ✅ Exceto: tabelas de sistema (Permissions, Roles, etc.)

### Como implementar

**Migration:**
```csharp
migrationBuilder.CreateTable(
    name: "Usuarios",
    columns: table => new
    {
        Id = table.Column<Guid>(nullable: false),
        EmpresaId = table.Column<Guid>(nullable: false),  // ← OBRIGATÓRIO
        Nome = table.Column<string>(maxLength: 200, nullable: false),
        // ... outros campos ...
        // Campos de auditoria obrigatórios
        Created = table.Column<DateTime>(nullable: false),
        CreatedBy = table.Column<string>(nullable: true),
        LastModified = table.Column<DateTime>(nullable: true),
        LastModifiedBy = table.Column<string>(nullable: true),
        DeletedBy = table.Column<string>(nullable: true)
    });
```

**Entidade:**
```csharp
public class Usuario
{
    public Guid Id { get; set; }
    public Guid EmpresaId { get; set; }  // ← OBRIGATÓRIO
    public string Nome { get; set; } = string.Empty;

    // Relacionamento com Empresa
    public virtual Empresa? Empresa { get; set; }
}
```

**Query automática:**
O sistema filtra automaticamente por `EmpresaId` do usuário logado.

### Validação

```sql
-- Verificar se tabela tem EmpresaId
PRAGMA table_info(Usuarios);
-- Deve aparecer coluna "EmpresaId" do tipo Guid
```

**Checklist:**
- [ ] Migration cria coluna `EmpresaId`
- [ ] Entidade tem propriedade `EmpresaId`
- [ ] Foreign key para tabela `Empresa` configurada
- [ ] Índice em `EmpresaId` criado (performance)

**Referências:**
- [PADROES-CODIFICACAO-BACKEND.md](./PADROES-CODIFICACAO-BACKEND.md) - Multi-tenancy

---

## 6️⃣ FUSE TEMPLATE (PADRÕES VISUAIS)

### Descrição
TODAS as telas DEVEM seguir os padrões visuais do **Fuse Admin Template**.

### Quando aplicar
- ✅ Ao criar novos componentes Angular
- ✅ Ao criar listagens, formulários, dashboards
- ✅ SEMPRE usar componentes do Fuse (não criar do zero)

### Leitura obrigatória

**ANTES de desenvolver qualquer tela:**

| Recurso | URL | Descrição |
|---------|-----|-----------|
| **Guia de Introdução** | http://localhost:4200/docs/guides/getting-started/introduction | Conceitos fundamentais |
| **Material Components** | http://localhost:4200/ui/material-components | Todos os componentes Material |
| **Other Components** | http://localhost:4200/ui/other-components/common/overview | Componentes adicionais |
| **Fuse Components** | http://localhost:4200/ui/fuse-components/libraries/mock-api | Componentes Fuse |

### Padrões obrigatórios

**1. Estrutura base de página:**
```html
<div class="flex w-full flex-auto flex-col">
    <div class="mx-auto flex w-full flex-wrap p-6 md:p-8">
        <!-- Conteúdo da página -->
    </div>
</div>
```

**❌ NÃO usar:** `max-w-screen-xl` (limita largura)
**✅ USAR:** largura total responsiva

**2. Cards de conteúdo:**
```html
<div class="bg-card flex flex-col overflow-hidden rounded-2xl shadow">
    <div class="flex items-center justify-between border-b border-surface-200/60 px-6 py-5">
        <div class="text-lg font-medium leading-6 tracking-tight">
            Título do Card
        </div>
    </div>
    <div class="p-6">
        <!-- Conteúdo -->
    </div>
</div>
```

**3. Tabelas:**
```html
<div class="overflow-x-auto mx-6">
    <table mat-table [dataSource]="dataSource" class="w-full min-w-[720px] bg-transparent">
        <!-- Colunas -->
    </table>
</div>
```

**4. Ícones:**
- **Padrão:** `heroicons_outline` (ícones linha)
- **Tamanhos:** `icon-size-4`, `icon-size-5`, `icon-size-6`, `icon-size-8`

### Validação

**Checklist visual:**
- [ ] Layout segue estrutura base (sem max-w-screen-xl)
- [ ] Cards com `bg-card` e `rounded-2xl`
- [ ] Tabelas com hover states
- [ ] Ícones Heroicons Outline
- [ ] Dark mode funcionando
- [ ] Responsividade testada (mobile/desktop)

**Referências:**
- [GUIA-LAYOUT.md](./GUIA-LAYOUT.md) - Padrões completos do Fuse Template

---

## 7️⃣ BUILD E VALIDAÇÃO DE AMBIENTE

### Descrição
Após TODA implementação ou modificação de código, DEVE executar build e garantir que Backend + Frontend estão rodando SEM ERROS.

### Quando aplicar
- ✅ Após criar nova funcionalidade
- ✅ Após corrigir bugs
- ✅ Antes de commitar código
- ✅ SEMPRE antes de marcar RF como concluído

### Como validar

**Backend (.NET 10):**
```bash
cd backend/IControlIT.API
dotnet build
# Deve retornar: Build succeeded. 0 Error(s)

cd src/Web
dotnet run
# Deve iniciar em http://localhost:5000
```

**Frontend (Angular 19):**
```bash
cd frontend/icontrolit-app
npm run build
# Deve retornar: ✔ Compiled successfully.

npm start
# Deve iniciar em http://localhost:4200
```

**Teste de integração:**
```bash
# Backend rodando em http://localhost:5000
curl http://localhost:5000/api/health
# Deve retornar: HTTP 200 OK

# Frontend rodando em http://localhost:4200
# Abrir navegador e verificar:
# - Página abre sem erros no console (F12)
# - Requests para API retornam 200 OK (Network tab)
```

### Checklist de ambiente funcionando

- [ ] Backend compilando sem erros (`dotnet build`)
- [ ] Backend rodando em http://localhost:5000
- [ ] Health check respondendo 200 OK
- [ ] Frontend compilando sem erros (`npm run build`)
- [ ] Frontend rodando em http://localhost:4200
- [ ] Página abrindo sem erros no console do navegador
- [ ] API calls retornando HTTP 200 (Network tab)
- [ ] Dados sendo exibidos corretamente na UI
- [ ] NENHUM erro no console do backend
- [ ] NENHUM erro no console do navegador (F12)

**SE QUALQUER ITEM FALHAR:**
1. **PARE**
2. **Identifique o erro**
3. **Corrija o erro**
4. **Rebuilde** (dotnet build / npm run build)
5. **Reinicie** (dotnet run / npm start)
6. **Re-valide** todos os itens

**Referências:**
- [GUIA-DEVELOPER.md](./GUIA-DEVELOPER.md) - Seção "4. Build e Validação do Ambiente"

---

## 8️⃣ CLEAN ARCHITECTURE + CQRS + MEDIATR (BACKEND)

### Descrição
TODO backend DEVE seguir padrões de **Clean Architecture + CQRS + MediatR**.

### Quando aplicar
- ✅ Ao criar novos Commands (Create, Update, Delete)
- ✅ Ao criar novas Queries (Get, GetAll, GetById)
- ✅ Em TODAS as operações de backend

### Estrutura obrigatória

```
backend/IControlIT.API/src/
├── Domain/                    ← Entidades, Enums, Constants
│   ├── Entities/
│   ├── Enums/
│   └── Constants/
├── Application/               ← Lógica de negócio, Commands/Queries
│   ├── Common/
│   │   ├── Interfaces/
│   │   ├── Behaviours/       ← StructuredLoggingBehaviour
│   │   └── Validators/
│   ├── [Modulo]/
│   │   ├── Commands/
│   │   └── Queries/
├── Infrastructure/            ← Implementações, DbContext, Services
│   ├── Data/
│   │   ├── ApplicationDbContext.cs
│   │   ├── Configurations/
│   │   └── Migrations/
│   └── Services/
└── Web/                       ← API, Endpoints, Controllers
    ├── Endpoints/
    └── Controllers/
```

### Exemplo completo

**1. Entidade (Domain):**
```csharp
public class Usuario
{
    public Guid Id { get; set; }
    public Guid EmpresaId { get; set; }
    public string Nome { get; set; } = string.Empty;
    public string Email { get; set; } = string.Empty;
}
```

**2. Command (Application):**
```csharp
public record CreateUsuarioCommand : IRequest<Guid>
{
    public string Nome { get; init; } = string.Empty;
    public string Email { get; init; } = string.Empty;
}
```

**3. Validator (Application):**
```csharp
public class CreateUsuarioCommandValidator : AbstractValidator<CreateUsuarioCommand>
{
    public CreateUsuarioCommandValidator()
    {
        RuleFor(x => x.Nome).NotEmpty().MaximumLength(200);
        RuleFor(x => x.Email).NotEmpty().EmailAddress();
    }
}
```

**4. Handler (Application):**
```csharp
public class CreateUsuarioCommandHandler : IRequestHandler<CreateUsuarioCommand, Guid>
{
    private readonly IApplicationDbContext _context;

    public async Task<Guid> Handle(CreateUsuarioCommand request, CancellationToken cancellationToken)
    {
        var usuario = new Usuario
        {
            Nome = request.Nome,
            Email = request.Email
        };

        _context.Usuarios.Add(usuario);
        await _context.SaveChangesAsync(cancellationToken);

        return usuario.Id;
    }
}
```

**5. Endpoint (Web):**
```csharp
public class Usuarios : EndpointGroupBase
{
    public override void Map(WebApplication app)
    {
        app.MapGroup(this)
            .RequireAuthorization()
            .MapPost(CreateUsuario);
    }

    public async Task<Guid> CreateUsuario(
        [FromBody] CreateUsuarioCommand command,
        ISender sender)
    {
        return await sender.Send(command);
    }
}
```

### Validação

**Checklist de estrutura:**
- [ ] Entidade em `Domain/Entities/`
- [ ] Command/Query em `Application/[Modulo]/Commands|Queries/`
- [ ] Validator criado (FluentValidation)
- [ ] Handler implementado (MediatR)
- [ ] Endpoint em `Web/Endpoints/`
- [ ] DbContext atualizado
- [ ] Migration criada

**Referências:**
- [PADROES-CODIFICACAO-BACKEND.md](./PADROES-CODIFICACAO-BACKEND.md) - Clean Architecture completo

---

## 9️⃣ STANDALONE COMPONENTS (ANGULAR 19)

### Descrição
TODO frontend DEVE usar **Angular 19 Standalone Components** (sem NgModules).

### Quando aplicar
- ✅ Ao criar novos componentes
- ✅ Em TODOS os componentes (sem exceção)
- ✅ NÃO criar NgModules (deprecated)

### Como implementar

**❌ ERRADO (NgModules - deprecated):**
```typescript
@NgModule({
    declarations: [ListComponent],
    imports: [CommonModule]
})
export class UsersModule {}
```

**✅ CORRETO (Standalone Components):**
```typescript
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { MatTableModule } from '@angular/material/table';
import { TranslocoModule } from '@jsverse/transloco';
import { FuseCardComponent } from '@fuse/components/card';

@Component({
    selector: 'app-users-list',
    standalone: true,  // ← SEMPRE standalone!
    imports: [
        CommonModule,
        RouterModule,
        MatTableModule,
        TranslocoModule,
        FuseCardComponent
    ],
    templateUrl: './list.component.html'
})
export class ListComponent {}
```

### Imports obrigatórios

**SEMPRE incluir:**
- ✅ `CommonModule` - Diretivas básicas (*ngIf, *ngFor)
- ✅ `RouterModule` - Se usar routerLink
- ✅ `TranslocoModule` - Traduções (OBRIGATÓRIO)
- ✅ Módulos do Material - Conforme uso (MatButtonModule, MatTableModule, etc.)
- ✅ Componentes do Fuse - Importar component diretamente (não module)

### Erro comum a evitar

**❌ NÃO importar FuseModule:**
```typescript
import { FuseModule } from '@fuse';  // ❌ ERRADO
```

**✅ Importar componente direto:**
```typescript
import { FuseCardComponent } from '@fuse/components/card';  // ✅ CORRETO
```

### Validação

**Checklist:**
- [ ] `standalone: true` em @Component
- [ ] CommonModule importado
- [ ] RouterModule importado (se usar routerLink)
- [ ] TranslocoModule importado
- [ ] Material Modules importados conforme uso
- [ ] Componentes Fuse importados diretamente
- [ ] NÃO há NgModule criado

**Referências:**
- [GUIA-DEVELOPER.md](./GUIA-DEVELOPER.md) - Seção "3.3. Criar Component (Standalone)"
- [ERROS-COMUNS-ANGULAR.md](./ERROS-COMUNS-ANGULAR.md) - Erro #1

---

## 🔟 BANCO DE DADOS (MIGRATIONS NO GIT, *.DB LOCAL)

### Descrição
**Migrations vão para o Git, banco de dados (*.db) é local.**

### Quando aplicar
- ✅ Ao criar/modificar tabelas
- ✅ Ao commitar código

### Regras de ouro

**O QUE VAI PARA O GIT:**
- ✅ Migrations (`.cs` files) - Scripts que CRIAM o banco
- ✅ `ApplicationDbContextModelSnapshot.cs` - Estado atual do schema

**O QUE NÃO VAI PARA O GIT:**
- ❌ `IControlIT.db` - Banco de dados SQLite
- ❌ `*.db-shm`, `*.db-wal` - Arquivos temporários SQLite

**Por quê?**
- Migrations = "Receita" (commitada)
- Banco = "Bolo" (cada dev constrói localmente)

### Como trabalhar

**Criar migration:**
```bash
cd backend/IControlIT.API
dotnet ef migrations add NomeDaMigration \
  --project src/Infrastructure \
  --startup-project src/Web \
  --context ApplicationDbContext
```

**Aplicar migrations:**
```bash
dotnet ef database update \
  --project src/Infrastructure \
  --startup-project src/Web \
  --context ApplicationDbContext
```

**Criar banco em nova máquina:**
```bash
# 1. Restaurar ferramentas
dotnet tool restore

# 2. Aplicar todas as migrations
dotnet ef database update \
  --project src/Infrastructure \
  --startup-project src/Web \
  --context ApplicationDbContext
```

### Validação

**Checklist de commit:**
- [ ] Migration (`.cs`) foi commitada
- [ ] `ApplicationDbContextModelSnapshot.cs` atualizado
- [ ] `IControlIT.db` NÃO foi commitado
- [ ] `.gitignore` contém `*.db`, `*.db-shm`, `*.db-wal`

**Referências:**
- [GUIA-BD.md](./GUIA-BD.md) - Guia completo de banco de dados
- [IMPORTANTE-BANCO-DE-DADOS.md](../IMPORTANTE-BANCO-DE-DADOS.md) - Explicação detalhada

---

## 📊 MATRIZ DE APLICABILIDADE

| Particularidade | Backend | Frontend | Documentação | Quando Validar |
|-----------------|---------|----------|--------------|----------------|
| **1. Central de Funcionalidades** | ✅ | ❌ | ❌ | Após implementação completa |
| **2. i18n (Transloco)** | ❌ | ✅ | ❌ | Durante implementação frontend |
| **3. RBAC (Permissões)** | ✅ | ✅ | ❌ | Antes de marcar RF como pronto |
| **4. Auditoria Automática** | ✅ | ❌ | ❌ | Automático (já implementado) |
| **5. Multi-tenancy** | ✅ | ❌ | ❌ | Ao criar migrations |
| **6. Fuse Template** | ❌ | ✅ | ❌ | Durante implementação frontend |
| **7. Build e Validação** | ✅ | ✅ | ❌ | Antes de commit |
| **8. Clean Architecture** | ✅ | ❌ | ❌ | Durante implementação backend |
| **9. Standalone Components** | ❌ | ✅ | ❌ | Ao criar componentes Angular |
| **10. Migrations no Git** | ✅ | ❌ | ❌ | Antes de commit |

---

## ✅ CHECKLIST FINAL DE CONFORMIDADE

Antes de considerar um RF concluído, verificar:

### Backend
- [ ] **Central de Funcionalidades** - Cadastrada no banco
- [ ] **RBAC** - Permissões criadas e associadas ao Developer
- [ ] **Auditoria** - Campos de auditoria em todas as entidades
- [ ] **Multi-tenancy** - EmpresaId em todas as tabelas
- [ ] **Clean Architecture** - Commands, Queries, Handlers, Validators
- [ ] **Migrations** - Criadas e commitadas (*.db NÃO commitado)
- [ ] **Build** - `dotnet build` sem erros
- [ ] **Health check** - http://localhost:5000/api/health retorna 200

### Frontend
- [ ] **i18n** - Traduzido em pt-BR, en, es (16 pontos)
- [ ] **RBAC** - Diretiva `*hasPermission` em botões
- [ ] **Fuse Template** - Padrões visuais consistentes
- [ ] **Standalone Components** - `standalone: true` em todos
- [ ] **Build** - `npm run build` sem erros
- [ ] **No errors** - Console do navegador sem erros (F12)
- [ ] **Integração** - API calls retornando 200 OK

### Geral
- [ ] **Build e Validação** - Backend + Frontend rodando sem erros
- [ ] **Teste manual** - Funcionalidade completa testada
- [ ] **3 idiomas** - Testado em pt-BR, en, es

---

## 🔗 DOCUMENTOS RELACIONADOS

### Guias Principais
- **[GUIA-DEVELOPER.md](./GUIA-DEVELOPER.md)** - Guia completo de desenvolvimento
- **[GUIA-TRANSLATE.md](./GUIA-TRANSLATE.md)** - Guia completo de i18n (16 pontos)
- **[GUIA-LAYOUT.md](./GUIA-LAYOUT.md)** - Padrões visuais do Fuse Template
- **[GUIA-BD.md](./GUIA-BD.md)** - Banco de dados e migrations

### Padrões Técnicos
- **[PADROES-CODIFICACAO-BACKEND.md](./PADROES-CODIFICACAO-BACKEND.md)** - Clean Architecture, CQRS
- **[PADROES-CODIFICACAO-FRONTEND.md](./PADROES-CODIFICACAO-FRONTEND.md)** - Angular 19, Standalone

### Erros Conhecidos
- **[ERROS-A-EVITAR.md](../ERROS-A-EVITAR.md)** - Erros reais e soluções
- **[ERROS-COMUNS-ANGULAR.md](./ERROS-COMUNS-ANGULAR.md)** - 8 erros de frontend

### Regras Gerais
- **[REGRAS-CRITICAS.md](./REGRAS-CRITICAS.md)** - 11 regras para todos os agentes

---

## 📝 OBSERVAÇÕES FINAIS

### Diferença entre PARTICULARIDADES e CONTRATOS

**PARTICULARIDADES-DO-SISTEMA.md (este documento):**
- ✅ Requisitos específicos do **IControlIT**
- ✅ **NÃO portável** para outros sistemas
- ✅ Referenciado em **prompts** e **anti-esquecimento**
- ✅ Consultado durante **implementação**

**CONTRATOS (docs/contracts/):**
- ✅ Governança **genérica e portável**
- ✅ Aplicável a **qualquer projeto**
- ✅ Define **processo** e **critérios de qualidade**
- ✅ Consultado durante **execução de contratos**

### Quando atualizar este documento

Este documento DEVE ser atualizado quando:
- ✅ Nova particularidade do sistema for identificada
- ✅ Integração obrigatória for adicionada
- ✅ Padrão específico do IControlIT mudar
- ✅ Erros recorrentes revelarem gaps nas particularidades

---

**ÚLTIMA ATUALIZAÇÃO:** 2026-01-01
**VERSÃO:** 1.0
**BASEADO EM:** GUIA-DEVELOPER.md, GUIA-TRANSLATE.md, GUIA-LAYOUT.md, GUIA-TESTER.md, REGRAS-CRITICAS.md
