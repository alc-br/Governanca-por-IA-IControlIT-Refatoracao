# CONTRATO PADRÃO DE DESENVOLVIMENTO

Este documento define o **padrão obrigatório** para todo desenvolvimento no projeto IControlIT.

Este contrato é **obrigatório**, **executável** e **inviolável**.

Ele é **referenciado por todos os outros contratos** de execução.

---

## IDENTIFICAÇÃO DO CONTRATO

**NOME:** Contrato Padrão de Desenvolvimento
**VERSÃO:** 1.0
**DATA:** 2025-12-24
**PROPÓSITO:** Definir padrões técnicos que DEVEM ser seguidos em TODA implementação

---

## ATIVAÇÃO DO CONTRATO

Este contrato é ativado **AUTOMATICAMENTE** quando qualquer um dos seguintes contratos for ativado:

- CONTRATO DE EXECUÇÃO – BACKEND
- CONTRATO DE EXECUÇÃO – FRONTEND
- CONTRATO DE MANUTENÇÃO / CORREÇÃO CONTROLADA
- CONTRATO DE DOCUMENTAÇÃO
- CONTRATO DE TESTES

O agente DEVE ler este contrato **ANTES** de executar qualquer ação técnica.

---

## FONTES DE VERDADE

Este contrato consolida informações das seguintes fontes:

| Fonte | Caminho | Conteúdo |
|-------|---------|----------|
| Arquitetura Master | `D:\DocumentosIC2\arquitetura.md` | Multi-tenancy, padrões de domínio, integrações |
| Desenvolvimento | `D:\DocumentosIC2\inteligencia-artificial\prompts\desenvolvimento.md` | Checklists Backend/Frontend |
| Testes | `D:\DocumentosIC2\inteligencia-artificial\prompts\teste.md` | 3 baterias de teste |
| Traduções | `D:\DocumentosIC2\inteligencia-artificial\prompts\traducao.md` | 16 pontos i18n |

---

## CHECKLIST BACKEND (.NET 10)

### 1. Domain Layer

- [ ] `Domain/Entities/[Entidade].cs` - Herdar de `AuditableEntity`
- [ ] Incluir `ClienteId` (OBRIGATÓRIO - multi-tenancy)
- [ ] Incluir `EmpresaId` (OPCIONAL - organizacional/fiscal)
- [ ] Incluir `Enums` se necessário

```csharp
public class Entidade : BaseAuditableGuidEntity
{
    // Multi-tenancy (OBRIGATÓRIO)
    public Guid ClienteId { get; set; }    // TENANT (isolamento)

    // Organização/Fiscal (OPCIONAL)
    public Guid? EmpresaId { get; set; }   // Unidade organizacional

    // Campos de negócio
    // ...
}
```

### 2. Application Layer

- [ ] `Application/[Feature]/Commands/` - Commands com Handlers e Validators
- [ ] `Application/[Feature]/Queries/` - Queries com Handlers
- [ ] Usar `IRequest<TResponse>` do MediatR

```csharp
// Command
public record CreateEntidadeCommand : IRequest<Guid>
{
    public string Nome { get; init; }
    public Guid ClienteId { get; init; }   // OBRIGATÓRIO
    public Guid? EmpresaId { get; init; }  // OPCIONAL
}

// Handler
[Authorize(Roles = "Developer,Super Admin")]  // Role-based!
public class CreateEntidadeCommandHandler : IRequestHandler<CreateEntidadeCommand, Guid>
{
    public async Task<Guid> Handle(CreateEntidadeCommand request, CancellationToken ct)
    {
        // Validação multi-tenancy
        if (request.ClienteId != _currentUser.ClienteId)
            throw new ForbiddenAccessException();

        // Implementação...
    }
}

// Validator
public class CreateEntidadeCommandValidator : AbstractValidator<CreateEntidadeCommand>
{
    public CreateEntidadeCommandValidator()
    {
        RuleFor(x => x.Nome).NotEmpty().MaximumLength(100);
        RuleFor(x => x.ClienteId).NotEmpty();
    }
}
```

### 3. Infrastructure Layer

- [ ] `Infrastructure/Data/ApplicationDbContext.cs` - Adicionar DbSet
- [ ] `Infrastructure/Data/Configurations/` - EF Configuration

```csharp
// ApplicationDbContext.cs
public DbSet<Entidade> Entidades => Set<Entidade>();

// Query Filter automático (multi-tenancy + soft delete)
modelBuilder.Entity<Entidade>().HasQueryFilter(
    e => e.ClienteId == _currentUser.ClienteId && e.FlAtivo == true
);
```

### 4. Web Layer

- [ ] `Web/Endpoints/[Feature].cs` - Minimal APIs
- [ ] Usar `RequireAuthorization(AuthorizationPolicies.XXX)` (Policy-based!)

```csharp
public class EntidadesEndpoints : EndpointGroupBase
{
    public override void Map(WebApplication app)
    {
        app.MapGroup(this)
            .RequireAuthorization()
            .MapGet(GetEntidades)
            .MapPost(CreateEntidade)
                .RequireAuthorization(AuthorizationPolicies.EntidadesCreate);
    }
}
```

### 5. Migration

```bash
# Criar migration
dotnet ef migrations add [Nome] \
  --project src/Infrastructure \
  --startup-project src/Web \
  --context ApplicationDbContext

# Aplicar migration
dotnet ef database update \
  --project src/Infrastructure \
  --startup-project src/Web \
  --context ApplicationDbContext
```

---

## MIGRATIONS - REGRAS CRÍTICAS

### O que VAI para o Git

- `src/Infrastructure/Data/Migrations/*.cs`
- `ApplicationDbContextModelSnapshot.cs`

### O que NÃO VAI para o Git

- `IControlIT.db` (banco SQLite)
- `IControlIT.db-shm` (arquivo temporário)
- `IControlIT.db-wal` (Write-Ahead Log)

---

## CHECKLIST FRONTEND (Angular 19)

### 1. Estrutura de Pastas

```
modules/admin/management/[feature]/
├── [feature].routes.ts           # Rotas do módulo
├── list/
│   └── list.component.ts         # Listar registros
├── create/
│   └── create.component.ts       # Criar registro
├── edit/
│   └── edit.component.ts         # Editar registro
├── view/
│   └── view.component.ts         # Visualizar registro
└── [feature].service.ts          # Integração com API
```

### 2. Componentes (Standalone)

```typescript
@Component({
  selector: 'app-[feature]-list',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    ReactiveFormsModule,
    MatTableModule,
    MatButtonModule,
    MatIconModule,
    MatPaginatorModule,
    TranslocoModule,
    FuseCardComponent,
    PermissionDirective
  ],
  templateUrl: './list.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class ListComponent implements OnInit {
  // Signals (Angular 19)
  items = signal<Entidade[]>([]);
  isLoading = signal<boolean>(false);

  // ...
}
```

### 3. Service

```typescript
@Injectable({ providedIn: 'root' })
export class FeatureService extends BaseApiService<Entidade> {
  protected override resourcePath = '[feature]';

  constructor(http: HttpClient) {
    super(http);
  }

  // Métodos: getAll(), getById(), create(), update(), delete()
}
```

### 4. Traduções (i18n)

- [ ] `assets/i18n/pt-BR/[feature].json`
- [ ] `assets/i18n/en/[feature].json`
- [ ] `assets/i18n/es/[feature].json`

---

## REGRA DE AUTORIZAÇÃO (CRÍTICO)

### Onde Usar Cada Tipo

| Local | Tipo | Exemplo |
|-------|------|---------|
| **Endpoint (Minimal API)** | Policy-based | `RequireAuthorization(AuthorizationPolicies.XXX)` |
| **Command/Query (Application)** | Role-based | `[Authorize(Roles = "Developer,Super Admin")]` |

### Os 3 Conceitos de Autorização

| Conceito | O que é | Onde usar | Exemplo |
|----------|---------|-----------|---------|
| **Permission Code** | Valor no banco de dados | Constants, banco | `"CAD.EMPRESAS.PERMANENT_DELETE"` |
| **Policy Name** | Registrado no ASP.NET Core | Endpoints | `AuthorizationPolicies.CompaniesPermanentDelete` |
| **Role Name** | Claim no JWT token | Commands/Queries | `"Developer"`, `"Super Admin"` |

### ERRO COMUM - CAUSA 403

```csharp
// ✅ CORRETO: No Endpoint (Minimal API)
groupBuilder.MapDelete(DeleteEmpresa, "{id}/permanent")
    .RequireAuthorization(AuthorizationPolicies.CompaniesPermanentDelete);

// ✅ CORRETO: No Command (Application Layer)
[Authorize(Roles = "Developer,Super Admin")]
public record DeleteEmpresaCommand(Guid Id) : IRequest;

// ❌ ERRADO: NÃO use policy-based em Commands! (causa erro 403)
[Authorize(Policy = EmpresasPermissions.PermanentDelete)]  // NUNCA FAZER ISSO!
```

---

## PERMISSÕES AO PERFIL DEVELOPER

### Regra Crítica

Toda nova funcionalidade **DEVE** ter suas permissões associadas ao perfil Developer.

**Por quê?**
- Desenvolvedores precisam testar imediatamente
- Evita frustração de não conseguir acessar o que implementou
- Mantém fluxo ágil

### Como Fazer

```sql
-- ID do perfil Developer: 1dd7b3e2-3735-4854-adaa-6a4c9cada803

INSERT INTO RolePermissions (
    Id, RoleId, PermissionId, Created, CreatedBy
) VALUES (
    lower(hex(randomblob(16))),
    '1dd7b3e2-3735-4854-adaa-6a4c9cada803',  -- Developer Role
    '<ID_DA_PERMISSAO>',                      -- Sua permissão
    datetime('now'),
    'system'
);
```

---

## MULTI-TENANCY

### Modelo de 1 Nível (Cliente)

O IControlIT implementa multi-tenancy em **1 nível único**:

```
Cliente (Tenant) ← Isolamento de dados acontece AQUI
 └── Empresa    ← NÃO é subtenant! Apenas organizacional/fiscal
```

### ClienteId vs EmpresaId

| Campo | Obrigatório | Propósito | Isolamento |
|-------|-------------|-----------|------------|
| **ClienteId** | SIM | Tenant (isolamento) | SIM - Query Filter automático |
| **EmpresaId** | NÃO | Organização/Fiscal | NÃO - apenas informativo |

### IMPORTANTE

```
❌ ERRADO: Pensar que Empresa isola dados (subtenant)
✅ CORRETO: Empresa é apenas para organização/fiscalização

Exemplo:
- Cliente: Alpargatas (Tenant)
  - Usuário Anderson (ClienteId = Alpargatas)
    - Pode ver TODOS os ativos da Alpargatas
    - EmpresaId é apenas informativo (qual unidade ele pertence)
```

### Query Filters Automáticos

```csharp
// ApplicationDbContext.cs
protected override void OnModelCreating(ModelBuilder modelBuilder)
{
    // Isolamento APENAS por ClienteId
    modelBuilder.Entity<Ativo>().HasQueryFilter(
        e => e.ClienteId == _currentUser.ClienteId &&
             e.FlAtivo == true  // Soft delete
    );

    // EmpresaId NÃO é usado para isolamento!
}
```

---

## PADRÕES DE DOMÍNIO (8 PADRÕES)

### 1. Multi-Tenancy

Todas as entidades de negócio DEVEM ter ClienteId.

### 2. Soft Delete

```csharp
public class BaseEntity
{
    public bool FlAtivo { get; set; } = true;
    public DateTime? DeletedAt { get; set; }
    public string? DeletedBy { get; set; }
}
```

### 3. Auditoria Automática

Campos preenchidos automaticamente via AuditInterceptor:
- `Created`, `CreatedBy`
- `LastModified`, `LastModifiedBy`
- `DeletedAt`, `DeletedBy`

### 4. CQRS

- Commands: Write operations
- Queries: Read operations
- Handlers: Implementam lógica
- Validators: FluentValidation

### 5. Domain Events

```csharp
public class AtivoAlocadoDomainEvent : INotification
{
    public Guid AtivoId { get; }
    public Guid ConsumidorId { get; }
}
```

### 6. Workflow/Status Transitions

Validação de transições permitidas via dicionário.

### 7. Approval Workflows

Aprovações multi-nível para contratos e documentos.

### 8. Depreciação de Ativos

Cálculo automático via Hangfire job.

---

## BUILD E VALIDAÇÃO DE AMBIENTE (OBRIGATÓRIO)

### Backend

```bash
cd backend/IControlIT.API
dotnet build
```

**Verificar:**
- 0 errors = SUCCESS
- Errors found = PARAR e corrigir

```bash
cd src/Web
dotnet run
```

**Verificar:**
- `Now listening on: http://localhost:5000`

```bash
curl http://localhost:5000/api/health
```

**Esperado:** HTTP 200 OK

### Frontend

```bash
cd frontend/icontrolit-app
npm run build
```

**Verificar:**
- 0 errors = SUCCESS

```bash
npm start
```

**Verificar:**
- `Angular Live Development Server is listening on localhost:4200`
- Abrir http://localhost:4200
- DevTools (F12) → Console → **NENHUM ERRO**
- Network tab → API calls → **HTTP 200**

### Checklist de Ambiente Funcionando

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

### SE QUALQUER ITEM ACIMA FALHAR

1. **PARE**
2. **Identifique o erro**
3. **Corrija o erro**
4. **Rebuilde** (dotnet build / npm run build)
5. **Reinicie** (dotnet run / npm start)
6. **Re-valide** todos os itens
7. **Só prossiga quando TODOS os itens estiverem OK**

---

## i18n - 16 PONTOS OBRIGATÓRIOS

### Checklist Completo de Tradução

- [ ] **1. Templates HTML** - Todos os textos visíveis (títulos, labels, botões, placeholders)
- [ ] **2. Mensagens TypeScript** - Confirmações, diálogos, tooltips
- [ ] **3. Validações Frontend** - Mensagens de erro de formulário (`<mat-error>`)
- [ ] **4. Validações Backend** - Mensagens de erro da API (.NET)
- [ ] **5. Toasts e Notificações** - Mensagens de sucesso/erro
- [ ] **6. Tooltips e Hints** - Ajudas contextuais (`matTooltip`, `mat-hint`)
- [ ] **7. Badges e Status** - Labels de status, badges visuais
- [ ] **8. Breadcrumbs e Navegação** - Títulos de navegação
- [ ] **9. Tabelas e Grid** - Cabeçalhos de colunas, mensagens "sem dados"
- [ ] **10. Paginação** - Labels do MatPaginator
- [ ] **11. Filtros** - Labels e opções de filtros
- [ ] **12. Diálogos de Confirmação** - Títulos, mensagens, botões
- [ ] **13. Mensagens de Erro HTTP** - Tratamento de erros da API
- [ ] **14. Pluralização** - Textos que mudam com quantidade
- [ ] **15. Interpolação** - Textos com variáveis dinâmicas (`{{variavel}}`)
- [ ] **16. Componentes do Angular Material** - MatPaginator, MatDatepicker, etc.

### Estrutura de Arquivos

```
frontend/icontrolit-app/public/i18n/
├── pt.json    (Português - PRIMARY)
├── en.json    (Inglês)
└── es.json    (Espanhol)
```

### Regra Crítica

- **ZERO warnings** de tradução no console é obrigatório
- Usar chaves i18n não registradas = **INVALIDA a entrega**
- Dependência em fallback silencioso = ERRO FUNCIONAL

---

## TESTES - 3 BATERIAS (100% PASS)

### Regra de Ouro

Cada bateria DEVE ter 100% PASS antes de executar a próxima.

```
Bateria 1 (Backend)  → Se < 100% PASS → PARAR e corrigir
                      → Se = 100% PASS → Prosseguir Bateria 2

Bateria 2 (E2E)      → Se < 100% PASS → PARAR e corrigir
                      → Se = 100% PASS → Prosseguir Bateria 3

Bateria 3 (Outros)   → Se < 100% PASS → PARAR e corrigir
                      → Se = 100% PASS → Concluído
```

### Bateria 1: Backend

- Testes de Commands
- Testes de Queries
- Testes de Validators
- Testes de Endpoints (HTTP 200, 401, 403)

### Bateria 2: E2E/Sistema

- Playwright tests
- Fluxo: Login → Navegar → Listar → Criar → Editar → Excluir
- Screenshots como evidência

### Bateria 3: Outros

- Segurança (SQL Injection, XSS, CSRF)
- Performance (100 usuários concorrentes, <500ms)
- RBAC (permissões corretas)

---

## BLOQUEIO DE EXECUÇÃO

Se qualquer dependência exigir:

- Nova entidade de domínio não autorizada
- Nova regra de negócio
- Alteração estrutural de arquitetura

O agente DEVE:

1. **PARAR**
2. **ALERTAR**
3. **DESCREVER a dependência**
4. **AGUARDAR decisão**

---

**Este contrato é vinculante.
Execuções fora dele são inválidas.**

---

## REGRA DE NEGACAO ZERO

Se uma solicitacao:
- nao estiver explicitamente prevista no contrato ativo, ou
- conflitar com qualquer regra do contrato

ENTAO:

- A execucao DEVE ser NEGADA
- Nenhuma acao parcial pode ser realizada
- Nenhum "adiantamento" e permitido
