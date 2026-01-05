# 💻 GUIA DO AGENTE DEVELOPER (DESENVOLVEDOR)

**Versão:** 1.0
**Data:** 2025-01-12
**Público:** Agente Developer (Desenvolvedor)

---

## 🎯 Seu Papel

Como **agente developer**, você é responsável por:

1. **Implementar funcionalidades** baseadas em RFs e UCs
2. **Seguir padrões de codificação** backend (.NET) e frontend (Angular)
3. **Criar APIs REST** seguindo princípios Clean Architecture
4. **Desenvolver componentes UI** usando Angular 18+ standalone
5. **Garantir qualidade** do código e testes unitários
6. **Integrar sistemas** (i18n, auditoria, permissões)

---

## 📚 Documentos Obrigatórios para Você

### LEIA PRIMEIRO (ordem de prioridade):

1. **[REGRAS-CRITICAS.md](./REGRAS-CRITICAS.md)** ⚠️ OBRIGATÓRIO
   - Regras que se aplicam a TODOS os agentes

2. **[ERROS-COMUNS-ANGULAR.md](./ERROS-COMUNS-ANGULAR.md)** ⚠️ CRÍTICO
   - **LEIA ANTES DE QUALQUER DESENVOLVIMENTO EM ANGULAR**
   - 8 erros reais documentados com soluções
   - Evita horas de debugging
   - Checklist completo para novos components

3. **[MANUAL-DE-CODIFICACAO.md](./MANUAL-DE-CODIFICACAO.md)** ⭐ PRINCIPAL
   - Padrões arquiteturais (.NET + Angular)
   - Convenções de código
   - Boas práticas
   - Logs obrigatórios

4. **[GUIA-BD.md](./GUIA-BD.md)** 🗄️ BANCO DE DADOS
   - **LEIA ANTES DE TRABALHAR COM MIGRATIONS**
   - Comandos essenciais (criar, listar, aplicar migrations)
   - Padrões de nomenclatura (tabelas, colunas)
   - O que commitar e o que NÃO commitar
   - Troubleshooting comum
   - Fluxo de trabalho entre desenvolvedores

5. **[PADROES-CODIFICACAO-BACKEND.md](./PADROES-CODIFICACAO-BACKEND.md)** 🔧 BACKEND
   - Clean Architecture
   - CQRS + MediatR
   - FluentValidation
   - Entity Framework Core

6. **[PADROES-CODIFICACAO-FRONTEND.md](./PADROES-CODIFICACAO-FRONTEND.md)** 🎨 FRONTEND
   - Angular 18+ Standalone Components
   - Fuse Template
   - Transloco (i18n)
   - Reactive Forms

6. **RF e UC da funcionalidade** 📋 REQUISITOS
   - Ler RF completo antes de implementar
   - Seguir regras de negócio documentadas
   - Consultar casos de uso para fluxos

---

## 🛠️ Suas Principais Tarefas

### 1. Implementar Funcionalidade (Backend + Frontend)

**Quando:** Usuário solicita "Implemente o UC01" ou "Codifique o RF-XXX-NNN"

**Processo completo:**

```
┌─────────────────────────────────────┐
│ PREPARAÇÃO                          │
├─────────────────────────────────────┤
│ 1. Ler RF completo                  │
│ 2. Ler UC específico                │
│ 3. Ler MD (modelo de dados)         │
│ 4. Ler ERROS-COMUNS-ANGULAR.md      │ ← CRÍTICO!
│ 5. Consultar código legado          │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│ BACKEND (.NET 10)                    │
├─────────────────────────────────────┤
│ 1. Criar entidade (Domain/Entities) │
│ 2. Criar Command/Query (Application)│
│ 3. Criar Validator (FluentValidation)│
│ 4. Criar Handler (MediatR)          │
│ 5. Criar Endpoint (Web/Endpoints)   │
│ 6. Atualizar DbContext              │
│ 7. Criar migration (EF Core) ⚠️     │ ← VER GUIA-BD.md
│ 8. Testar API (Postman/Swagger)     │
└─────────────────────────────────────┘
  ⚠️ ATENÇÃO: Ao trabalhar com migrations (passo 7),
     consulte GUIA-BD.md para comandos e padrões!
         ↓
┌─────────────────────────────────────┐
│ FRONTEND (Angular 18)               │
├─────────────────────────────────────┤
│ 1. Criar service (API calls)        │
│ 2. Criar types/interfaces           │
│ 3. Criar component (standalone)     │
│ 4. Criar template (.html)           │
│ 5. Criar estilos (.scss)            │
│ 6. Adicionar i18n (transloco)       │
│ 7. Adicionar validações (forms)     │
│ 8. Testar no navegador              │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│ INTEGRAÇÕES OBRIGATÓRIAS            │
├─────────────────────────────────────┤
│ 1. Central de Funcionalidades       │
│ 2. Sistema de i18n (Transloco)      │
│ 3. Auditoria (logs automáticos)     │
│ 4. Permissões (hasPermission)       │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│ BUILD E VALIDAÇÃO DO AMBIENTE       │
├─────────────────────────────────────┤
│ 1. Build backend (dotnet build)     │
│ 2. Build frontend (npm run build)   │
│ 3. Corrigir erros se houver         │
│ 4. Rodar backend (dotnet run)       │
│ 5. Rodar frontend (npm start)       │
│ 6. Testar integração (API calls)    │
│ 7. Validar ambiente funcionando     │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│ TESTES                              │
├─────────────────────────────────────┤
│ 1. Testes unitários (backend)       │
│ 2. Testes de componente (Angular)   │
│ 3. Validar lint/format              │
└─────────────────────────────────────┘
```

**⚠️ CRÍTICO:** Após TODA implementação, você DEVE executar build e garantir que tanto Backend quanto Frontend estão rodando sem erros!

---

### 2. Padrões de Backend (.NET 10)

**Arquitetura:** Clean Architecture + CQRS + MediatR

#### 2.1. Estrutura de Pastas

```
backend/IControlIT.API/src/
├── Domain/                    ← Entidades, Enums, Exceptions
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

#### 2.2. Criar Command (exemplo: CreateUsuarioCommand)

**Localização:** `src/Application/Usuarios/Commands/CreateUsuario/`

**CreateUsuarioCommand.cs:**
```csharp
using MediatR;

namespace IControlIT.Application.Usuarios.Commands.CreateUsuario;

public record CreateUsuarioCommand : IRequest<Guid>
{
    public string Nome { get; init; } = string.Empty;
    public string Email { get; init; } = string.Empty;
    public string Login { get; init; } = string.Empty;
    public string Senha { get; init; } = string.Empty;
    public Guid IdIdioma { get; init; }
    public Guid IdPerfil { get; init; }
}
```

**CreateUsuarioCommandValidator.cs:**
```csharp
using FluentValidation;

namespace IControlIT.Application.Usuarios.Commands.CreateUsuario;

public class CreateUsuarioCommandValidator : AbstractValidator<CreateUsuarioCommand>
{
    public CreateUsuarioCommandValidator()
    {
        RuleFor(x => x.Nome)
            .NotEmpty().WithMessage("Nome é obrigatório")
            .MaximumLength(120);

        RuleFor(x => x.Email)
            .NotEmpty().WithMessage("Email é obrigatório")
            .EmailAddress().WithMessage("Email inválido");

        RuleFor(x => x.Login)
            .NotEmpty().WithMessage("Login é obrigatório")
            .MaximumLength(50);

        RuleFor(x => x.Senha)
            .NotEmpty().WithMessage("Senha é obrigatória")
            .MinimumLength(8).WithMessage("Senha deve ter no mínimo 8 caracteres");
    }
}
```

**CreateUsuarioCommandHandler.cs:**
```csharp
using MediatR;
using IControlIT.Application.Common.Interfaces;
using IControlIT.Domain.Entities;

namespace IControlIT.Application.Usuarios.Commands.CreateUsuario;

public class CreateUsuarioCommandHandler : IRequestHandler<CreateUsuarioCommand, Guid>
{
    private readonly IApplicationDbContext _context;

    public CreateUsuarioCommandHandler(IApplicationDbContext context)
    {
        _context = context;
    }

    public async Task<Guid> Handle(CreateUsuarioCommand request, CancellationToken cancellationToken)
    {
        var usuario = new Usuario
        {
            Nome = request.Nome,
            Email = request.Email,
            Login = request.Login,
            PasswordHash = BCrypt.Net.BCrypt.HashPassword(request.Senha),
            IdIdioma = request.IdIdioma,
            IdPerfil = request.IdPerfil,
            FlAtivo = 1
        };

        _context.Usuarios.Add(usuario);
        await _context.SaveChangesAsync(cancellationToken);

        return usuario.Id;
    }
}
```

#### 2.3. Criar Endpoint (Minimal API)

**Localização:** `src/Web/Endpoints/Usuarios.cs`

```csharp
using IControlIT.Application.Usuarios.Commands.CreateUsuario;
using IControlIT.Application.Usuarios.Queries.GetUsuarios;
using MediatR;
using Microsoft.AspNetCore.Mvc;

namespace IControlIT.Web.Endpoints;

public class Usuarios : EndpointGroupBase
{
    public override void Map(WebApplication app)
    {
        app.MapGroup(this)
            .RequireAuthorization()
            .MapPost(CreateUsuario)
            .MapGet(GetUsuarios, "");
    }

    public async Task<Guid> CreateUsuario(
        [FromBody] CreateUsuarioCommand command,
        ISender sender)
    {
        return await sender.Send(command);
    }

    public async Task<IEnumerable<UsuarioDto>> GetUsuarios(
        ISender sender,
        [AsParameters] GetUsuariosQuery query)
    {
        return await sender.Send(query);
    }
}
```

**Documentação:**
- [PADROES-CODIFICACAO-BACKEND.md](./PADROES-CODIFICACAO-BACKEND.md)

---

### 3. Padrões de Frontend (Angular 18)

**Framework:** Angular 18+ Standalone Components + Fuse Template

#### 3.1. Estrutura de Pastas

```
frontend/icontrolit-app/src/app/
├── core/                          ← Services, Auth, Guards
│   ├── auth/
│   ├── i18n/
│   └── services/
├── modules/                       ← Módulos funcionais
│   └── admin/
│       └── management/
│           └── users/             ← Módulo de usuários
│               ├── list/
│               │   ├── list.component.ts
│               │   ├── list.component.html
│               │   └── list.component.scss
│               ├── details/
│               ├── users.service.ts
│               ├── users.types.ts
│               └── users.routes.ts
└── layout/                        ← Layout e componentes comuns
```

#### 3.2. Criar Service

**users.service.ts:**
```typescript
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Usuario, CreateUsuarioRequest } from './users.types';
import { environment } from 'environments/environment';

@Injectable({ providedIn: 'root' })
export class UsersService {
    private apiUrl = `${environment.apiUrl}/usuarios`;

    constructor(private http: HttpClient) {}

    getUsuarios(): Observable<Usuario[]> {
        return this.http.get<Usuario[]>(this.apiUrl);
    }

    getUsuario(id: string): Observable<Usuario> {
        return this.http.get<Usuario>(`${this.apiUrl}/${id}`);
    }

    createUsuario(data: CreateUsuarioRequest): Observable<string> {
        return this.http.post<string>(this.apiUrl, data);
    }

    updateUsuario(id: string, data: Partial<Usuario>): Observable<void> {
        return this.http.put<void>(`${this.apiUrl}/${id}`, data);
    }

    deleteUsuario(id: string): Observable<void> {
        return this.http.delete<void>(`${this.apiUrl}/${id}`);
    }
}
```

**users.types.ts:**
```typescript
export interface Usuario {
    id: string;
    nome: string;
    email: string;
    login: string;
    idIdioma: string;
    idiomaNome: string;
    idPerfil: string;
    perfilNome: string;
    flAtivo: number;
    dtCadastro: string;
}

export interface CreateUsuarioRequest {
    nome: string;
    email: string;
    login: string;
    senha: string;
    idIdioma: string;
    idPerfil: string;
}
```

#### 3.3. Criar Component (Standalone)

**⚠️ LEIA [ERROS-COMUNS-ANGULAR.md](./ERROS-COMUNS-ANGULAR.md) ANTES!**

**list.component.ts:**
```typescript
import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { MatTableModule } from '@angular/material/table';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { TranslocoModule } from '@jsverse/transloco';
import { FuseCardComponent } from '@fuse/components/card';
import { UsersService } from '../users.service';
import { Usuario } from '../users.types';

@Component({
    selector: 'app-users-list',
    standalone: true,
    imports: [
        CommonModule,
        RouterModule,
        MatTableModule,
        MatButtonModule,
        MatIconModule,
        TranslocoModule,
        FuseCardComponent
    ],
    templateUrl: './list.component.html'
})
export class ListComponent implements OnInit {
    usuarios: Usuario[] = [];
    displayedColumns = ['nome', 'email', 'login', 'perfil', 'status', 'actions'];

    constructor(private usersService: UsersService) {}

    ngOnInit(): void {
        this.loadUsuarios();
    }

    loadUsuarios(): void {
        this.usersService.getUsuarios().subscribe({
            next: (usuarios) => this.usuarios = usuarios,
            error: (err) => console.error('Erro ao carregar usuários', err)
        });
    }
}
```

**list.component.html:**
```html
<fuse-card class="flex flex-col w-full p-8">
    <!-- Header -->
    <div class="flex items-center justify-between mb-6">
        <h2 class="text-3xl font-bold">{{ 'users.title' | transloco }}</h2>
        <button
            mat-raised-button
            color="primary"
            [routerLink]="['new']">
            <mat-icon>add</mat-icon>
            {{ 'users.new' | transloco }}
        </button>
    </div>

    <!-- Table -->
    <table mat-table [dataSource]="usuarios" class="w-full">
        <ng-container matColumnDef="nome">
            <th mat-header-cell *matHeaderCellDef>{{ 'users.name' | transloco }}</th>
            <td mat-cell *matCellDef="let user">{{ user.nome }}</td>
        </ng-container>

        <ng-container matColumnDef="email">
            <th mat-header-cell *matHeaderCellDef>{{ 'users.email' | transloco }}</th>
            <td mat-cell *matCellDef="let user">{{ user.email }}</td>
        </ng-container>

        <!-- Actions -->
        <ng-container matColumnDef="actions">
            <th mat-header-cell *matHeaderCellDef></th>
            <td mat-cell *matCellDef="let user">
                <button mat-icon-button [routerLink]="[user.id]">
                    <mat-icon>edit</mat-icon>
                </button>
            </td>
        </ng-container>

        <tr mat-header-row *matHeaderRowDef="displayedColumns"></tr>
        <tr mat-row *matRowDef="let row; columns: displayedColumns;"></tr>
    </table>
</fuse-card>
```

**Documentação:**
- [ERROS-COMUNS-ANGULAR.md](./ERROS-COMUNS-ANGULAR.md) ⚠️ CRÍTICO
- [PADROES-CODIFICACAO-FRONTEND.md](./PADROES-CODIFICACAO-FRONTEND.md)

---

### 4. Build e Validação do Ambiente (OBRIGATÓRIO)

**⚠️ CRÍTICO:** Após TODA implementação (ou modificação de código), você DEVE executar build e garantir que o ambiente completo está funcionando.

#### 4.1. Build do Backend

**1. Navegar para pasta do backend:**
```bash
cd backend/IControlIT.API
```

**2. Executar build:**
```bash
dotnet build
```

**3. Analisar resultado:**
- ✅ **0 errors = SUCCESS** → Prosseguir
- ❌ **Errors found** → Corrigir IMEDIATAMENTE antes de continuar

**Erros comuns e soluções:**
```
❌ "The name 'X' does not exist in the current context"
   → Falta using ou namespace errado

❌ "Type 'X' already defines a member called 'Y'"
   → Propriedade/método duplicado

❌ "'X' does not contain a definition for 'Y'"
   → Propriedade não existe ou nome errado

SOLUÇÃO: Corrigir o erro → Rodar `dotnet build` novamente
```

**4. Rodar backend (se não estiver rodando):**
```bash
cd src/Web
dotnet run
```

**5. Verificar saída:**
```
✅ SUCESSO:
info: Microsoft.Hosting.Lifetime[14]
      Now listening on: http://localhost:5000

❌ ERRO:
Unable to bind to http://localhost:5000 on the IPv4 loopback interface:
'Address already in use'
```

**6. Se porta em uso:**
```powershell
# Encontrar processo
netstat -ano | findstr :5000

# Matar processo (substitua [PID])
taskkill /PID [PID] /F

# Rodar novamente
dotnet run
```

**7. Testar health check:**
```bash
curl http://localhost:5000/api/health
```
**Esperado:** HTTP 200 OK

---

#### 4.2. Build do Frontend

**1. Navegar para pasta do frontend:**
```bash
cd frontend/icontrolit-app
```

**2. Executar build (verifica compilação):**
```bash
npm run build
```

**3. Analisar resultado:**
- ✅ **0 errors = SUCCESS** → Prosseguir
- ❌ **Errors found** → Corrigir IMEDIATAMENTE

**Erros comuns e soluções:**
```
❌ "Module not found: Error: Can't resolve 'X'"
   → Falta import ou caminho errado

❌ "Property 'X' does not exist on type 'Y'"
   → Tipo incorreto ou propriedade não existe

❌ "Cannot find name 'X'"
   → Falta importação ou variável não declarada

SOLUÇÃO: Corrigir o erro → Rodar `npm run build` novamente
```

**4. Rodar frontend dev server:**
```bash
npm start
```

**5. Verificar saída:**
```
✅ SUCESSO:
✔ Compiled successfully.
✔ Browser application bundle generation complete.
** Angular Live Development Server is listening on localhost:4200

❌ ERRO:
✖ Failed to compile.
```

**6. Se porta em uso:**
```powershell
# Encontrar processo
netstat -ano | findstr :4200

# Matar processo
taskkill /PID [PID] /F

# Rodar novamente
npm start
```

**7. Testar no navegador:**
- Abrir: http://localhost:4200
- Navegar para funcionalidade implementada
- Abrir DevTools (F12) → Console
- **NÃO DEVE TER ERROS NO CONSOLE**

---

#### 4.3. Validação de Integração

**1. Verificar comunicação Backend ↔ Frontend:**

Abra DevTools (F12) → Aba Network:
- Navegue para funcionalidade implementada
- Execute uma operação (ex: listar items)
- Verifique requests HTTP:

```
✅ SUCESSO:
Status: 200 OK
Request URL: http://localhost:5000/api/usuarios
Response: [{"id": "...", "nome": "..."}]

❌ ERRO:
Status: 404 Not Found → Endpoint não existe/rota errada
Status: 500 Internal Server Error → Erro no backend (ver logs)
Status: 401 Unauthorized → Problema de autenticação
Status: 403 Forbidden → Sem permissão
```

**2. Se integração falhar:**
- Verificar CORS no backend (Program.cs)
- Verificar URL da API em environment.ts
- Verificar token JWT válido
- Verificar endpoint route no backend
- Verificar service no frontend chamando URL correta

---

#### 4.4. Checklist de Ambiente Funcionando

**Antes de considerar implementação completa:**

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

**⚠️ SE QUALQUER ITEM ACIMA FALHAR:**
1. **PARE**
2. **Identifique o erro**
3. **Corrija o erro**
4. **Rebuilde** (dotnet build / npm run build)
5. **Reinicie** (dotnet run / npm start)
6. **Re-valide** todos os itens
7. **Só prossiga quando TODOS os itens estiverem ✅**

---

### 5. Associação de Permissões ao Perfil Developer

**⚠️ REGRA CRÍTICA:** Toda nova funcionalidade criada DEVE ter suas permissões associadas ao perfil Developer.

**Por quê?**
- Desenvolvedores precisam testar novas funcionalidades imediatamente
- Evita frustração de implementar algo e não conseguir acessá-lo
- Mantém o fluxo de desenvolvimento ágil

**Como fazer:**

Após criar as permissões no banco de dados, execute:

```sql
-- ID do perfil Developer: 1dd7b3e2-3735-4854-adaa-6a4c9cada803
-- Substitua <ID_DA_PERMISSAO> pelo GUID da permissão criada

INSERT INTO RolePermissions (
    Id, RoleId, PermissionId, Created, CreatedBy
) VALUES (
    lower(hex(randomblob(4))) || '-' || lower(hex(randomblob(2))) || '-' || lower(hex(randomblob(2))) || '-' || lower(hex(randomblob(2))) || '-' || lower(hex(randomblob(6))),
    '1dd7b3e2-3735-4854-adaa-6a4c9cada803',  -- Developer Role
    '<ID_DA_PERMISSAO>',                      -- Sua permissão
    datetime('now'),
    'system'
);
```

**Exemplo real (RF-008 Empresas):**

```sql
-- Permissões do RF-008: cadastros:empresa:read/create/update/delete
INSERT INTO RolePermissions (Id, RoleId, PermissionId, Created, CreatedBy) VALUES
  (lower(hex(randomblob(16))), '1dd7b3e2-3735-4854-adaa-6a4c9cada803', '32e61730-056b-4988-90ed-d66c8132dcc8', datetime('now'), 'system'),  -- read
  (lower(hex(randomblob(16))), '1dd7b3e2-3735-4854-adaa-6a4c9cada803', '2ad1d465-940a-4bcf-8b8a-f9d0558090d4', datetime('now'), 'system'),  -- create
  (lower(hex(randomblob(16))), '1dd7b3e2-3735-4854-adaa-6a4c9cada803', '92791c82-09ba-4082-8ae2-d0e2cfca8ba1', datetime('now'), 'system'),  -- update
  (lower(hex(randomblob(16))), '1dd7b3e2-3735-4854-adaa-6a4c9cada803', '3d2b96d0-1234-4bc4-8bca-8214f2c0872d', datetime('now'), 'system');  -- delete
```

---

### 6. Integrações Obrigatórias

**TODA funcionalidade DEVE integrar com:**

#### 6.1. Sistema de i18n (Transloco)

**Adicionar traduções:**

**frontend/icontrolit-app/public/i18n/pt.json:**
```json
{
  "users": {
    "title": "Gestão de Usuários",
    "new": "Novo Usuário",
    "name": "Nome",
    "email": "E-mail",
    "login": "Login",
    "profile": "Perfil",
    "status": "Status",
    "actions": "Ações"
  }
}
```

**public/i18n/en.json:**
```json
{
  "users": {
    "title": "User Management",
    "new": "New User",
    "name": "Name",
    "email": "Email",
    "login": "Login",
    "profile": "Profile",
    "status": "Status",
    "actions": "Actions"
  }
}
```

#### 6.2. Sistema de Auditoria (Automático)

**StructuredLoggingBehaviour** já loga automaticamente:
- ✅ Toda requisição MediatR
- ✅ Usuário que executou
- ✅ Data/hora
- ✅ IP de origem
- ✅ Duração
- ✅ Erros com stack trace

**Você NÃO precisa fazer nada!** O logging é automático.

#### 6.3. Sistema de Autorização e Permissões

⚠️ **CRÍTICO:** Erro comum que causa 403 Forbidden - confundir permission codes com policy names!

**Documentação completa:** Ver [ERROS-A-EVITAR.md](../ERROS-A-EVITAR.md) - Erro #3

##### 📋 REGRA DE OURO: Onde Usar Cada Tipo de Autorização

**NO ENDPOINT (Minimal API) - Use Policy:**
```csharp
// ✅ CORRETO - Policy-based authorization
groupBuilder.MapDelete(DeleteEmpresa, "{id}/permanent")
    .RequireAuthorization(AuthorizationPolicies.CompaniesPermanentDelete);
```

**NO COMMAND/QUERY (Application Layer) - Use Roles:**
```csharp
// ✅ CORRETO - Role-based authorization
[Authorize(Roles = "Developer,Super Admin")]
public record DeleteEmpresaCommand(Guid Id) : IRequest;

// ❌ ERRADO - NÃO use policy-based em Commands!
[Authorize(Policy = EmpresasPermissions.PermanentDelete)]  // NUNCA FAZER ISSO!
public record DeleteEmpresaCommand(Guid Id) : IRequest;     // Causa erro 403!
```

##### 📊 Os 3 Conceitos de Autorização

| Conceito | O que é | Onde usar | Exemplo |
|----------|---------|-----------|---------|
| **Permission Code** | Valor no banco de dados | Constants, banco | `"CAD.EMPRESAS.PERMANENT_DELETE"` |
| **Policy Name** | Registrado no ASP.NET Core | Endpoints, policies | `AuthorizationPolicies.CompaniesPermanentDelete` |
| **Role Name** | Claim no JWT token | Commands/Queries | `"Developer"`, `"Super Admin"` |

##### ✅ Padrão Completo Correto

```csharp
// 1. DOMAIN - Permission Code (constants)
public static class EmpresasPermissions
{
    public const string PermanentDelete = "CAD.EMPRESAS.PERMANENT_DELETE";
}

// 2. WEB - Policy Name (para endpoints)
public static class AuthorizationPolicies
{
    public const string CompaniesPermanentDelete = "CAD.EMPRESAS.PERMANENT_DELETE";
}

// 3. WEB - Policy Mapping
public static class PolicyPermissionMap
{
    public static readonly Dictionary<string, string> Map = new()
    {
        { AuthorizationPolicies.CompaniesPermanentDelete,
          PermissionRegistry.Permissions.CompaniesCompanyPermanentDelete },
    };
}

// 4. APPLICATION - Command (role-based)
[Authorize(Roles = "Developer,Super Admin")]  // ✅ CORRETO
public record PermanentDeleteEmpresaCommand(Guid Id) : IRequest;

// 5. WEB - Endpoint (policy-based)
groupBuilder.MapDelete(PermanentDeleteEmpresa, "{id}/permanent")
    .RequireAuthorization(AuthorizationPolicies.CompaniesPermanentDelete);  // ✅ CORRETO
```

##### 🎯 Quando Usar Cada Abordagem

| Situação | Use | Exemplo |
|----------|-----|---------|
| Endpoint Minimal API | Policy-based | `.RequireAuthorization(AuthorizationPolicies.X)` |
| Command/Query/Handler | Role-based | `[Authorize(Roles = "Developer")]` |
| Verificação granular de permissão | Permission Check no código | `if (user.HasPermission("CAD.X.Y"))` |
| Múltiplas roles | Role-based | `[Authorize(Roles = "Admin,Manager")]` |

**Frontend (Directive):**
```html
<button
    mat-raised-button
    *hasPermission="'Users.Create'">
    Criar Usuário
</button>
```

#### 6.4. Central de Funcionalidades

**Registrar funcionalidade:**
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

---

## 🚨 Erros Comuns a Evitar

### ❌ ERRO #1: Não ler ERROS-COMUNS-ANGULAR.md

**Consequência:** Perder horas com erros já documentados

**Solução:**
- ✅ **LER [ERROS-COMUNS-ANGULAR.md](./ERROS-COMUNS-ANGULAR.md) ANTES DE COMEÇAR**

---

### ❌ ERRO #2: Usar Modules ao invés de Standalone Components

**Código errado:**
```typescript
@NgModule({
    declarations: [ListComponent],
    imports: [CommonModule]
})
export class UsersModule {}
```

**Código correto:**
```typescript
@Component({
    selector: 'app-users-list',
    standalone: true,  // ← SEMPRE standalone!
    imports: [CommonModule, MatTableModule]
})
export class ListComponent {}
```

---

### ❌ ERRO #3: Usar @ngx-translate ao invés de @jsverse/transloco

**Código errado:**
```typescript
import { TranslateModule } from '@ngx-translate/core';  // ❌
```

**Código correto:**
```typescript
import { TranslocoModule } from '@jsverse/transloco';  // ✅
```

---

### ❌ ERRO #4: Esquecer de importar FuseCardComponent

**Erro:**
```
NG8001: 'fuse-card' is not a known element
```

**Solução:**
```typescript
import { FuseCardComponent } from '@fuse/components/card';  // ✅

@Component({
    imports: [FuseCardComponent]  // ✅
})
```

---

### ❌ ERRO #5: Não fazer logging estruturado

**Código errado:**
```csharp
try {
    await _context.SaveChangesAsync();
} catch (Exception ex) {
    // ❌ Engolir exceção silenciosamente
}
```

**Código correto:**
```csharp
// ✅ StructuredLoggingBehaviour já loga automaticamente!
// Você NÃO precisa fazer try/catch para logging
// Apenas deixe a exceção propagar

await _context.SaveChangesAsync(cancellationToken);
```

---

## ✅ Checklist de Implementação

Antes de considerar uma funcionalidade completa:

### Backend
- [ ] Entidade criada em Domain/Entities
- [ ] Command/Query criado em Application
- [ ] Validator criado (FluentValidation)
- [ ] **Permissões criadas e associadas ao perfil Developer** ⚠️ CRÍTICO
- [ ] Handler implementado (MediatR)
- [ ] Endpoint criado em Web/Endpoints
- [ ] DbContext atualizado
- [ ] Migration criada e aplicada
- [ ] API testada (Swagger/Postman)
- [ ] Logging automático funcionando
- [ ] Permissões configuradas

### Frontend
- [ ] Service criado (API calls)
- [ ] Types/Interfaces definidos
- [ ] Component criado (standalone)
- [ ] Template HTML implementado
- [ ] Estilos SCSS aplicados
- [ ] i18n adicionado (pt, en, es)
- [ ] Validações de formulário implementadas
- [ ] Permissões (hasPermission) aplicadas
- [ ] Component testado no navegador
- [ ] Build executado sem erros

### Integrações
- [ ] i18n (Transloco) configurado
- [ ] Auditoria automática funcionando
- [ ] Permissões (RBAC) implementadas
- [ ] Central de Funcionalidades registrada

### Testes
- [ ] Testes unitários (backend) criados
- [ ] Testes de componente (Angular) criados
- [ ] Build executado (`dotnet build`, `ng build`)
- [ ] Lint/format validado

---

## 📚 Documentos Relacionados

- **[REGRAS-CRITICAS.md](./REGRAS-CRITICAS.md)** - Regras para todos os agentes
- **[ERROS-COMUNS-ANGULAR.md](./ERROS-COMUNS-ANGULAR.md)** ⚠️ CRÍTICO
- **[MANUAL-DE-CODIFICACAO.md](./MANUAL-DE-CODIFICACAO.md)** - Padrões completos
- **[PADROES-CODIFICACAO-BACKEND.md](./PADROES-CODIFICACAO-BACKEND.md)** - Backend .NET
- **[PADROES-CODIFICACAO-FRONTEND.md](./PADROES-CODIFICACAO-FRONTEND.md)** - Frontend Angular
- **[GUIA-ARCHITECT.md](./GUIA-ARCHITECT.md)** - Para entender RFs e UCs
- **[GUIA-TESTER.md](./GUIA-TESTER.md)** - Para entender testes

---

**ÚLTIMA ATUALIZAÇÃO:** 2025-01-12
**VERSÃO:** 1.0
