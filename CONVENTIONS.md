# CONVENTIONS.md

# 📐 Convenções Técnicas do Projeto IControlIT

> **Versão:** 1.1  
> **Data:** 2025-12-20  
> **Status:** Vigente  
> **Aplicação:** Obrigatória para todo código novo; progressiva para código legado

---

## Legenda de Obrigatoriedade

| Marcador | Significado |
|----------|-------------|
| 🔴 **OBRIGATÓRIO** | Deve ser seguido sem exceções. Violações bloqueiam merge. |
| 🟡 **RECOMENDADO** | Deve ser seguido salvo justificativa documentada. |
| 🟢 **OPCIONAL** | Boa prática sugerida, não exigida. |

---

## Sumário

1. [Estrutura de Pastas e Organização](#1-estrutura-de-pastas-e-organização)
2. [Convenções de Nomenclatura](#2-convenções-de-nomenclatura)
3. [Convenções de Camadas](#3-convenções-de-camadas)
4. [Padrões de Código](#4-padrões-de-código)
5. [Convenções de Testes](#5-convenções-de-testes)
6. [Convenções de Commits e Versionamento](#6-convenções-de-commits-e-versionamento)
7. [Convenções de Documentação](#7-convenções-de-documentação)
8. [Checklist de Conformidade](#8-checklist-de-conformidade)

---

## 1. Estrutura de Pastas e Organização

### 1.1 Backend (.NET)

#### 🔴 OBRIGATÓRIO: Estrutura de Solução

```
D:\IC2\backend\IControlIT.API/
├── src/
│   ├── Domain/
│   ├── Application/
│   ├── Infrastructure/
│   └── Web/
├── tests/
│   ├── Domain.Tests/
│   ├── Application.Tests/
│   ├── Infrastructure.Tests/
│   └── Web.Tests/
└── IControlIT.sln
```

#### 🔴 OBRIGATÓRIO: Estrutura da Camada Domain

```
Domain/
├── Entities/
├── Enums/
├── Constants/
├── Events/
├── Exceptions/
└── Common/
    ├── Interfaces/
    └── BaseClasses/
```

#### 🔴 OBRIGATÓRIO: Estrutura da Camada Application

```
Application/
├── Commands/
│   └── {Entidade}/
│       ├── Create{Entidade}Command.cs
│       ├── Create{Entidade}CommandHandler.cs
│       └── Create{Entidade}CommandValidator.cs
├── Queries/
│   └── {Entidade}/
│       ├── Get{Entidade}sQuery.cs
│       ├── Get{Entidade}sQueryHandler.cs
│       └── Get{Entidade}ByIdQuery.cs
├── DTOs/
│   └── {Entidade}/
├── Mappings/
├── Behaviours/
└── Common/
    ├── Interfaces/
    └── Models/
```

#### 🔴 OBRIGATÓRIO: Estrutura da Camada Infrastructure

```
Infrastructure/
├── Persistence/
│   ├── ApplicationDbContext.cs
│   ├── Configurations/
│   │   └── {Entidade}Configuration.cs
│   └── Interceptors/
├── Migrations/
├── Services/
├── Identity/
└── External/
    └── {SistemaExterno}/
```

#### 🔴 OBRIGATÓRIO: Estrutura da Camada Web

```
Web/
├── Endpoints/
│   └── {Entidade}Endpoints.cs
├── Middleware/
├── Filters/
└── Program.cs
```

---

### 1.2 Frontend (Angular)

#### 🔴 OBRIGATÓRIO: Estrutura do Projeto

```
D:\IC2\frontend\icontrolit-app/src/app/
├── core/
├── shared/
├── modules/
└── layout/
```

#### 🔴 OBRIGATÓRIO: Estrutura de Core

```
core/
├── auth/
│   ├── auth.service.ts
│   ├── auth.guard.ts
│   └── auth.interceptor.ts
├── api/
│   └── base-api.service.ts
├── guards/
├── interceptors/
├── services/
└── models/
```

#### 🔴 OBRIGATÓRIO: Estrutura de Shared

```
shared/
├── components/
│   └── {componente}/
│       ├── {componente}.component.ts
│       ├── {componente}.component.html
│       └── {componente}.component.scss
├── directives/
├── pipes/
└── models/
```

#### 🔴 OBRIGATÓRIO: Estrutura de Feature Module

```
modules/{feature}/
├── components/
│   └── {componente}/
├── services/
│   └── {feature}.service.ts
├── models/
│   └── {feature}.types.ts
└── {feature}.routes.ts
```

#### 🟡 RECOMENDADO: Estrutura de Componente CRUD

```
modules/{feature}/components/
├── list/
│   ├── list.component.ts
│   ├── list.component.html
│   └── list.component.scss
├── form/
│   ├── form.component.ts
│   ├── form.component.html
│   └── form.component.scss
└── detail/
    ├── detail.component.ts
    ├── detail.component.html
    └── detail.component.scss
```

---

### 1.3 Organização de Módulos

#### 🔴 OBRIGATÓRIO: Um Módulo por Domínio de Negócio

| Domínio | Backend (Commands/Queries) | Frontend (modules/) |
|---------|---------------------------|---------------------|
| Usuários | `Commands/Usuarios/` | `modules/admin/usuarios/` |
| Ativos | `Commands/Ativos/` | `modules/ativos/` |
| Linhas | `Commands/Linhas/` | `modules/linhas/` |
| Chamados | `Commands/Chamados/` | `modules/chamados/` |

#### 🔴 OBRIGATÓRIO: Não Criar Dependências Circulares Entre Módulos

- Módulo A não pode importar de Módulo B se B importa de A
- Dependências compartilhadas devem estar em `shared/` ou `core/`

---

## 2. Convenções de Nomenclatura

### 2.1 Nomenclatura Geral

#### 🔴 OBRIGATÓRIO: Idioma

| Elemento | Idioma | Exemplo |
|----------|--------|---------|
| Código (classes, métodos, variáveis) | Português | `Usuario`, `CriarAtivo`, `valorTotal` |
| Comentários técnicos | Português | `// Valida CPF do consumidor` |
| Commits | Português | `feat: adiciona validação de CNPJ` |
| Documentação técnica | Português | README, CONVENTIONS |
| Logs de sistema | Inglês | `User created successfully` |
| Mensagens de UI | Internacionalizado | Arquivos i18n |

#### 🔴 OBRIGATÓRIO: Sem Abreviações Obscuras

| ❌ Proibido | ✅ Correto |
|-------------|-----------|
| `usr` | `usuario` |
| `clt` | `cliente` |
| `dt` | `data` |
| `qtd` | `quantidade` |
| `vlr` | `valor` |

#### 🟡 RECOMENDADO: Abreviações Permitidas

| Abreviação | Significado | Uso |
|------------|-------------|-----|
| `Id` | Identificador | `UsuarioId`, `ClienteId` |
| `Dto` | Data Transfer Object | `UsuarioDto` |
| `Vm` | View Model | `UsuarioVm` |
| `Db` | Database | `DbContext` |
| `Api` | Application Programming Interface | `ApiService` |

---

### 2.2 Backend (.NET)

#### 🔴 OBRIGATÓRIO: Nomenclatura de Classes

| Tipo | Padrão | Exemplo |
|------|--------|---------|
| Entidade | `PascalCase` singular | `Usuario`, `Ativo`, `LinhaMovel` |
| Command | `{Verbo}{Entidade}Command` | `CreateUsuarioCommand` |
| Query | `Get{Entidade}(s)Query` | `GetUsuariosQuery`, `GetUsuarioByIdQuery` |
| Handler | `{Command/Query}Handler` | `CreateUsuarioCommandHandler` |
| Validator | `{Command}Validator` | `CreateUsuarioCommandValidator` |
| DTO | `{Entidade}Dto` | `UsuarioDto`, `AtivoDto` |
| Service | `{Dominio}Service` | `EmailService`, `TokenService` |
| Interface | `I{Nome}` | `IUsuarioRepository`, `IEmailService` |
| Endpoint | `{Entidade}Endpoints` | `UsuariosEndpoints` |
| Configuration (EF) | `{Entidade}Configuration` | `UsuarioConfiguration` |
| Interceptor | `{Funcao}Interceptor` | `AuditInterceptor` |
| Middleware | `{Funcao}Middleware` | `ExceptionHandlingMiddleware` |
| Exception | `{Descricao}Exception` | `NotFoundException`, `ForbiddenAccessException` |
| Domain Event | `{Entidade}{Acao}Event` | `AtivoAlocadoEvent` |

#### 🔴 OBRIGATÓRIO: Nomenclatura de Métodos

| Tipo | Padrão | Exemplo |
|------|--------|---------|
| Método assíncrono | `{Nome}Async` | `GetUsuarioByIdAsync` |
| Método de busca | `Get{O que}` | `GetAtivos`, `GetById` |
| Método de criação | `Create{Entidade}` | `CreateUsuario` |
| Método de atualização | `Update{Entidade}` | `UpdateUsuario` |
| Método de exclusão | `Delete{Entidade}` | `DeleteUsuario` |
| Método de validação | `Validate{O que}` ou `Is{Condicao}` | `ValidateCpf`, `IsActive` |
| Handler | `Handle` | `Handle(Command, CancellationToken)` |

#### 🔴 OBRIGATÓRIO: Nomenclatura de Variáveis e Parâmetros

| Tipo | Padrão | Exemplo |
|------|--------|---------|
| Variáveis locais | `camelCase` | `usuario`, `listaAtivos` |
| Parâmetros | `camelCase` | `usuarioId`, `cancellationToken` |
| Campos privados | `_camelCase` | `_context`, `_currentUser` |
| Constantes | `PascalCase` | `MaxRetries`, `DefaultPageSize` |
| Propriedades | `PascalCase` | `Nome`, `Email`, `ClienteId` |

#### 🔴 OBRIGATÓRIO: Nomenclatura de Arquivos

| Tipo | Padrão | Exemplo |
|------|--------|---------|
| Classe | `{NomeClasse}.cs` | `Usuario.cs` |
| Interface | `I{Nome}.cs` | `IUsuarioRepository.cs` |
| Command completo | Um arquivo por classe | `CreateUsuarioCommand.cs` |

---

### 2.3 Frontend (Angular)

#### 🔴 OBRIGATÓRIO: Nomenclatura de Arquivos

| Tipo | Padrão | Exemplo |
|------|--------|---------|
| Component | `{nome}.component.ts` | `usuarios-list.component.ts` |
| Service | `{nome}.service.ts` | `usuarios.service.ts` |
| Guard | `{nome}.guard.ts` | `permission.guard.ts` |
| Interceptor | `{nome}.interceptor.ts` | `auth.interceptor.ts` |
| Directive | `{nome}.directive.ts` | `permission.directive.ts` |
| Pipe | `{nome}.pipe.ts` | `format-date.pipe.ts` |
| Model/Interface | `{nome}.types.ts` ou `{nome}.model.ts` | `usuario.types.ts` |
| Routes | `{feature}.routes.ts` | `admin.routes.ts` |

#### 🔴 OBRIGATÓRIO: Nomenclatura de Classes Angular

| Tipo | Padrão | Exemplo |
|------|--------|---------|
| Component | `{Nome}Component` | `UsuariosListComponent` |
| Service | `{Nome}Service` | `UsuariosService` |
| Guard | `{Nome}Guard` | `PermissionGuard` |
| Interceptor | `{Nome}Interceptor` | `AuthInterceptor` |
| Directive | `{Nome}Directive` | `PermissionDirective` |
| Pipe | `{Nome}Pipe` | `FormatDatePipe` |

#### 🔴 OBRIGATÓRIO: Nomenclatura de Seletores

| Tipo | Padrão | Exemplo |
|------|--------|---------|
| Component | `app-{kebab-case}` | `app-usuarios-list` |
| Directive | `app{PascalCase}` | `appPermission` |
| Pipe | `camelCase` | `formatDate` |

#### 🔴 OBRIGATÓRIO: Nomenclatura de Variáveis TypeScript

| Tipo | Padrão | Exemplo |
|------|--------|---------|
| Propriedades públicas | `camelCase` | `usuarios`, `isLoading` |
| Propriedades privadas | `_camelCase` | `_usuariosService` |
| Signals | `camelCase` | `usuarios = signal([])` |
| Observables | `camelCase$` | `usuarios$` |
| Constantes | `UPPER_SNAKE_CASE` | `MAX_PAGE_SIZE` |

---

### 2.4 Banco de Dados

#### 🔴 OBRIGATÓRIO: Nomenclatura de Tabelas e Colunas

| Elemento | Padrão | Exemplo |
|----------|--------|---------|
| Tabela | `PascalCase` singular | `Usuario`, `Ativo`, `LinhaMovel` |
| Coluna | `PascalCase` | `Id`, `Nome`, `ClienteId` |
| Chave primária | `Id` | `Id` |
| Chave estrangeira | `{EntidadeRelacionada}Id` | `ClienteId`, `UsuarioId` |
| Índice | `IX_{Tabela}_{Coluna(s)}` | `IX_Usuario_Email` |
| Unique constraint | `UQ_{Tabela}_{Coluna(s)}` | `UQ_Usuario_Email_ClienteId` |
| Check constraint | `CK_{Tabela}_{Descricao}` | `CK_Ativo_ValorPositivo` |

#### 🔴 OBRIGATÓRIO: Colunas Padrão de Auditoria

Toda tabela de negócio deve ter:

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `Id` | `UNIQUEIDENTIFIER` | Chave primária |
| `ClienteId` | `UNIQUEIDENTIFIER NOT NULL` | Multi-tenancy (isolamento obrigatório) |
| `EmpresaId` | `UNIQUEIDENTIFIER NULL` | Organização fiscal (opcional) |
| `Created` | `DATETIME2` | Data de criação (UTC) |
| `CreatedBy` | `NVARCHAR(100)` | Usuário que criou |
| `LastModified` | `DATETIME2` | Última modificação (UTC) |
| `LastModifiedBy` | `NVARCHAR(100)` | Usuário que modificou |
| `FlExcluido` | `BIT` | Soft delete (false=ativo, true=excluído) |

**Nota:** Campo `Ativo` (BIT) é OPCIONAL e usado para flag funcional quando necessário (habilitado/desabilitado).

---

## 3. Convenções de Camadas

### 3.1 Responsabilidades por Camada

#### 🔴 OBRIGATÓRIO: Domain

| Permitido | Proibido |
|-----------|----------|
| Entidades de negócio | Referências a EF Core |
| Enums | Referências a bibliotecas externas |
| Value Objects | Lógica de infraestrutura |
| Domain Events | DTOs |
| Interfaces de repositório | Implementações concretas |
| Exceções de domínio | Dependência de Application/Infrastructure |
| Regras de negócio puras | Acesso a banco de dados |

#### 🔴 OBRIGATÓRIO: Application

| Permitido | Proibido |
|-----------|----------|
| Commands e Queries | Acesso direto ao banco (usar interfaces) |
| Handlers | Lógica de UI |
| DTOs | Entidades de domínio em respostas públicas |
| Validators | Implementações de infraestrutura |
| Mappings (AutoMapper) | Controllers/Endpoints |
| Interfaces de serviços | Dependência de Web |
| Orchestração de casos de uso | Regras de negócio (vai no Domain) |

#### 🔴 OBRIGATÓRIO: Infrastructure

| Permitido | Proibido |
|-----------|----------|
| DbContext e Configurations | Lógica de negócio |
| Implementações de repositórios | Commands/Queries |
| Serviços externos (email, storage) | DTOs de Application |
| Interceptors do EF Core | Endpoints/Controllers |
| Migrations | Dependência de Web |
| Identity (JWT, Auth) | |

#### 🔴 OBRIGATÓRIO: Web

| Permitido | Proibido |
|-----------|----------|
| Endpoints (Minimal APIs) | Lógica de negócio |
| Middlewares | Acesso direto ao DbContext |
| Filters | Implementações de serviços |
| Program.cs (composição) | Entidades de domínio |
| Configuração de DI | Regras de validação |

---

### 3.2 Direção das Dependências

#### 🔴 OBRIGATÓRIO: Fluxo de Dependência

```
Web ──────────────────────────────────┐
  │                                   │
  ▼                                   │
Application ◀─────────────────────────┤
  │                                   │
  ▼                                   │
Domain ◀──────────────────────────────┘
  ▲
  │
Infrastructure ───────────────────────┘
```

**Regra:** Camadas internas não conhecem camadas externas.

- Domain não referencia nenhuma outra camada
- Application referencia apenas Domain
- Infrastructure referencia Domain e Application
- Web referencia todas as camadas

---

### 3.3 Frontend - Responsabilidades

#### 🔴 OBRIGATÓRIO: Core

| Permitido | Proibido |
|-----------|----------|
| Serviços singleton | Componentes visuais |
| Guards globais | Lógica específica de feature |
| Interceptors HTTP | Models específicos de módulo |
| Auth service | Importar de modules/ |

#### 🔴 OBRIGATÓRIO: Shared

| Permitido | Proibido |
|-----------|----------|
| Componentes reutilizáveis | Serviços com estado |
| Directives genéricas | Lógica de negócio |
| Pipes genéricos | Dependência de módulos específicos |
| Models compartilhados | Guards específicos |

#### 🔴 OBRIGATÓRIO: Modules

| Permitido | Proibido |
|-----------|----------|
| Componentes da feature | Importar de outros modules |
| Services da feature | Serviços globais (vão no core) |
| Routes da feature | Componentes genéricos (vão no shared) |
| Models específicos | |

---

## 4. Padrões de Código

### 4.1 Princípios Gerais

#### 🔴 OBRIGATÓRIO: Single Responsibility

- Uma classe = uma responsabilidade
- Um método = uma ação
- Um arquivo = uma classe principal (exceto types/models)

#### 🔴 OBRIGATÓRIO: Tamanho Máximo

| Elemento | Limite | Ação se Exceder |
|----------|--------|-----------------|
| Método | 30 linhas | Extrair métodos privados |
| Classe | 300 linhas | Dividir responsabilidades |
| Arquivo | 400 linhas | Dividir em múltiplos arquivos |
| Parâmetros de método | 5 parâmetros | Criar objeto de parâmetros |

#### 🟡 RECOMENDADO: Complexidade Ciclomática

- Máximo de 10 por método
- Se exceder, refatorar com early returns ou extração de métodos

---

### 4.2 Backend - Padrões Específicos

#### 🔴 OBRIGATÓRIO: Commands e Queries

```
✅ CORRETO:
- Um Command/Query por caso de uso
- Handler correspondente no mesmo namespace
- Validator para Commands que modificam dados

❌ PROIBIDO:
- Command genérico para múltiplas operações
- Lógica de negócio no Endpoint
- Handler sem validação de multi-tenancy
```

#### 🔴 OBRIGATÓRIO: Validação de Multi-Tenancy no Handler

Todo Handler que acessa dados deve validar ClienteId:

```
1. Verificar request.ClienteId == _currentUser.ClienteId
2. Lançar ForbiddenAccessException se diferente
3. Query Filter do EF Core é segunda linha de defesa, não única
```

#### 🔴 OBRIGATÓRIO: Injeção de Dependência

| Padrão | Uso |
|--------|-----|
| Constructor injection | Sempre preferido |
| Property injection | Nunca usar |
| Method injection | Apenas para dependências opcionais |

#### 🔴 OBRIGATÓRIO: Async/Await

- Todo método de I/O deve ser async
- Sempre usar `CancellationToken`
- Nunca usar `.Result` ou `.Wait()` (causa deadlock)
- Sufixo `Async` em métodos assíncronos

#### 🟡 RECOMENDADO: Guard Clauses

Validações no início do método com retorno antecipado:

```
✅ CORRETO:
if (request == null) throw new ArgumentNullException();
if (string.IsNullOrEmpty(request.Nome)) throw new ValidationException();
// lógica principal

❌ EVITAR:
if (request != null)
{
    if (!string.IsNullOrEmpty(request.Nome))
    {
        // lógica aninhada
    }
}
```

---

### 4.3 Frontend - Padrões Específicos

#### 🔴 OBRIGATÓRIO: Standalone Components

- Todos os novos componentes devem ser `standalone: true`
- Não criar NgModules tradicionais
- Imports explícitos no decorator do componente

#### 🔴 OBRIGATÓRIO: Signals para Estado

- Usar `signal()` para estado do componente
- Usar `computed()` para valores derivados
- Usar `effect()` para side effects
- Evitar BehaviorSubject para estado local

#### 🔴 OBRIGATÓRIO: Reactive Forms

- Usar Reactive Forms para formulários
- Não usar Template-Driven Forms
- Validações no FormGroup, não no template

#### 🔴 OBRIGATÓRIO: Change Detection

- Usar `ChangeDetectionStrategy.OnPush` em todos os componentes
- Evitar mutação direta de objetos/arrays

#### 🔴 OBRIGATÓRIO: Unsubscribe

- Usar `takeUntilDestroyed()` para Observables
- Ou gerenciar subscription manualmente com `ngOnDestroy`
- Signals não precisam de unsubscribe

#### 🟡 RECOMENDADO: Smart vs Dumb Components

| Smart (Container) | Dumb (Presentational) |
|-------------------|----------------------|
| Injeta services | Recebe dados via @Input |
| Gerencia estado | Emite eventos via @Output |
| Chama APIs | Sem lógica de negócio |
| Localizado em `pages/` ou raiz do módulo | Localizado em `components/` |

---

### 4.4 Tratamento de Erros

#### 🔴 OBRIGATÓRIO: Backend

| Tipo de Erro | Exception | HTTP Status |
|--------------|-----------|-------------|
| Recurso não encontrado | `NotFoundException` | 404 |
| Validação de dados | `ValidationException` | 400 |
| Acesso negado | `ForbiddenAccessException` | 403 |
| Não autenticado | `UnauthorizedException` | 401 |
| Conflito de dados | `ConflictException` | 409 |
| Erro interno | `Exception` (genérica) | 500 |

#### 🔴 OBRIGATÓRIO: Frontend

- Interceptor global para tratamento de erros HTTP
- Notificação visual para o usuário (toast/snackbar)
- Log de erros para debugging
- Nunca exibir stack trace para o usuário

---

### 4.5 Comentários e Documentação de Código

#### 🔴 OBRIGATÓRIO: Quando Comentar

| Situação | Ação |
|----------|------|
| Código autoexplicativo | Não comentar |
| Regra de negócio complexa | Comentar o "porquê" |
| Workaround/hack temporário | Comentar com TODO e motivo |
| API pública | XML docs (backend) / JSDoc (frontend) |

#### 🔴 OBRIGATÓRIO: Formato de TODO

```
// TODO: [TICKET-123] Descrição do que fazer
// FIXME: [TICKET-456] Descrição do bug a corrigir
// HACK: [TICKET-789] Workaround temporário - remover após X
```

#### 🟡 RECOMENDADO: XML Documentation (Backend)

Classes e métodos públicos devem ter:

```xml
/// <summary>
/// Descrição breve da classe/método.
/// </summary>
/// <param name="nome">Descrição do parâmetro.</param>
/// <returns>Descrição do retorno.</returns>
/// <exception cref="NotFoundException">Quando não encontrado.</exception>
```

---

## 5. Convenções de Testes

### 5.1 Estrutura de Testes

#### 🔴 OBRIGATÓRIO: Espelhamento da Estrutura de Produção

```
tests/
├── Domain.Tests/
│   └── Entities/
│       └── UsuarioTests.cs
├── Application.Tests/
│   └── Commands/
│       └── Usuarios/
│           └── CreateUsuarioCommandHandlerTests.cs
├── Infrastructure.Tests/
│   └── Persistence/
│       └── UsuarioRepositoryTests.cs
└── Web.Tests/
    └── Endpoints/
        └── UsuariosEndpointsTests.cs
```

### 5.2 Nomenclatura de Testes

#### 🔴 OBRIGATÓRIO: Nome de Classe de Teste

```
{ClasseSobTeste}Tests

Exemplo: UsuarioTests, CreateUsuarioCommandHandlerTests
```

#### 🔴 OBRIGATÓRIO: Nome de Método de Teste

```
{Metodo}_{Cenario}_{ResultadoEsperado}

Exemplos:
- Handle_ValidCommand_ReturnsUsuarioId
- Handle_DuplicateEmail_ThrowsValidationException
- Validate_EmptyName_ReturnsError
- GetById_NonExistentId_ReturnsNull
```

### 5.3 Padrão AAA (Arrange-Act-Assert)

#### 🔴 OBRIGATÓRIO: Estrutura do Teste

```
// Arrange
// - Setup de dados e mocks
// - Criação do SUT (System Under Test)

// Act
// - Execução do método sendo testado
// - Apenas UMA ação por teste

// Assert
// - Verificação do resultado
// - Verificação de interações com mocks
```

### 5.4 Cobertura de Testes

#### 🔴 OBRIGATÓRIO: Mínimo de Cobertura

| Camada | Cobertura Mínima |
|--------|------------------|
| Domain | 90% |
| Application (Handlers) | 80% |
| Application (Validators) | 100% |
| Infrastructure | 70% |
| Web (Endpoints) | 60% |

#### 🔴 OBRIGATÓRIO: O Que Testar

| Camada | Foco dos Testes |
|--------|-----------------|
| Domain | Regras de negócio, validações de entidade |
| Application | Fluxo do handler, validações, mappings |
| Infrastructure | Queries complexas, integrações |
| Web | Autenticação, autorização, serialização |

### 5.5 Mocking

#### 🟡 RECOMENDADO: Bibliotecas

- Backend: NSubstitute ou Moq
- Frontend: Jest mocks

#### 🔴 OBRIGATÓRIO: O Que Mockar

| Mockar | Não Mockar |
|--------|------------|
| Serviços externos (email, APIs) | Lógica de domínio |
| Banco de dados (usar in-memory) | Classes simples sem dependências |
| Tempo atual (IDateTimeProvider) | Entidades |
| Usuário atual (ICurrentUserService) | Value Objects |

### 5.6 Data-test Attributes (Infraestrutura de Testes E2E)

#### 🔴 OBRIGATÓRIO: Atributos data-test em Componentes Angular

**TODOS os componentes Angular DEVEM incluir data-test attributes em elementos interativos.**

Data-test attributes são **INFRAESTRUTURA DE TESTES**, não funcionalidade opcional. São necessários para:
- Testes E2E Playwright
- Testes de integração
- Automação de QA

#### 🔴 OBRIGATÓRIO: Formato do Atributo

```
data-test="<contexto>-<elemento>-<acao>"
```

**Estrutura:**
- `<contexto>`: Módulo ou tela (ex: `client`, `contract`, `invoice`)
- `<elemento>`: Tipo do elemento (ex: `btn`, `input`, `select`, `grid`, `link`)
- `<acao>`: Ação ou identificador (ex: `save`, `cancel`, `name`, `email`)

#### 🔴 OBRIGATÓRIO: Elementos que DEVEM ter data-test

| Tipo de Elemento | Obrigatoriedade | Exemplo |
|------------------|-----------------|---------|
| Botões (ações) | **SIM** | `data-test="btn-save"` |
| Campos de formulário | **SIM** | `data-test="input-name"` |
| Selects/Dropdowns | **SIM** | `data-test="select-status"` |
| Links de navegação | **SIM** | `data-test="link-dashboard"` |
| Grids/Tabelas | **SIM** | `data-test="grid-clients"` |
| Modals/Dialogs | **SIM** | `data-test="modal-confirm-delete"` |
| Checkboxes/Radios | **SIM** | `data-test="checkbox-active"` |
| Textos estáticos | **NÃO** | - |
| Ícones decorativos | **NÃO** | - |
| Divs/spans estruturais | **NÃO** | - |

#### 🔴 OBRIGATÓRIO: Exemplos por Categoria

**Botões:**
```html
<button data-test="btn-save">Salvar</button>
<button data-test="btn-cancel">Cancelar</button>
<button data-test="btn-delete">Excluir</button>
<button data-test="btn-add-item">Adicionar Item</button>
<button data-test="btn-export">Exportar</button>
```

**Campos de Formulário:**
```html
<!-- Inputs de texto -->
<input data-test="input-name" type="text" />
<input data-test="input-email" type="email" />
<input data-test="input-phone" type="tel" />

<!-- Selects -->
<select data-test="select-status">
  <option>Ativo</option>
  <option>Inativo</option>
</select>

<!-- Textareas -->
<textarea data-test="textarea-notes"></textarea>

<!-- Checkboxes -->
<input data-test="checkbox-active" type="checkbox" />

<!-- Radios -->
<input data-test="radio-tipo-fisica" type="radio" name="tipo" />
<input data-test="radio-tipo-juridica" type="radio" name="tipo" />
```

**Links de Navegação:**
```html
<a data-test="link-dashboard" routerLink="/dashboard">Dashboard</a>
<a data-test="link-clients" routerLink="/clients">Clientes</a>
<a data-test="link-contracts" routerLink="/contracts">Contratos</a>
```

**Grids/Tabelas:**
```html
<table data-test="grid-clients">
  <thead>
    <tr>
      <th data-test="header-name">Nome</th>
      <th data-test="header-email">Email</th>
      <th data-test="header-status">Status</th>
      <th data-test="header-actions">Ações</th>
    </tr>
  </thead>
  <tbody>
    <tr data-test="row-client-1">
      <td data-test="cell-name">João Silva</td>
      <td data-test="cell-email">joao@example.com</td>
      <td data-test="cell-status">Ativo</td>
      <td>
        <button data-test="btn-edit-1">Editar</button>
        <button data-test="btn-delete-1">Excluir</button>
      </td>
    </tr>
  </tbody>
</table>
```

**Modals/Dialogs:**
```html
<div data-test="modal-confirm-delete">
  <h3>Confirmar Exclusão</h3>
  <p>Tem certeza que deseja excluir este item?</p>
  <button data-test="btn-confirm-delete">Confirmar</button>
  <button data-test="btn-cancel-delete">Cancelar</button>
</div>
```

#### 🔴 OBRIGATÓRIO: Validação de Data-test

Antes de considerar frontend concluído, validar:
- [ ] Todos elementos especificados no **WF-RFXXX.md** têm data-test attributes
- [ ] Nomenclatura segue padrão `<contexto>-<elemento>-<acao>`
- [ ] Data-test está documentado no **WF-RFXXX.md** (seção "Elementos de Interface")
- [ ] Seletores Playwright usam data-test (não classes CSS ou IDs)

#### 🟡 RECOMENDADO: Prefixos por Contexto

Para evitar colisões, usar prefixo de contexto:

```html
<!-- Módulo de Clientes -->
<button data-test="client-btn-save">Salvar</button>
<input data-test="client-input-name" />

<!-- Módulo de Contratos -->
<button data-test="contract-btn-save">Salvar</button>
<input data-test="contract-input-number" />
```

#### ❌ INCORRETO: O que NÃO fazer

```html
<!-- ❌ NÃO usar classes CSS como seletores -->
<button class="btn-primary">Salvar</button>

<!-- ❌ NÃO usar IDs como seletores -->
<button id="saveButton">Salvar</button>

<!-- ❌ NÃO usar texto como seletor (pode ser traduzido) -->
<button>Salvar</button>

<!-- ❌ NÃO usar hierarquia de elementos -->
<div class="actions">
  <button>Salvar</button>
</div>
```

#### ✅ CORRETO: Usar data-test

```html
<!-- ✅ SEMPRE usar data-test -->
<button data-test="btn-save">Salvar</button>
<input data-test="input-name" type="text" />
<select data-test="select-status"></select>
```

#### 🔴 OBRIGATÓRIO: Integração com Testes E2E

**Seletores Playwright DEVEM usar data-test:**

```typescript
// ✅ CORRETO
await page.click('[data-test="btn-save"]');
await page.fill('[data-test="input-name"]', 'João');
await page.selectOption('[data-test="select-status"]', 'Ativo');

// ❌ INCORRETO (NÃO usar)
await page.click('.btn-primary'); // classe CSS pode mudar
await page.click('#saveButton');  // ID pode mudar
await page.click('button:has-text("Salvar")'); // texto pode ser traduzido
```

**Razão:** Data-test attributes são estáveis e não mudam com refatorações de CSS ou i18n.

---

## 6. Convenções de Commits e Versionamento

### 6.1 Conventional Commits

#### 🔴 OBRIGATÓRIO: Formato do Commit

```
<tipo>(<escopo>): <descrição>

[corpo opcional]

[rodapé opcional]
```

#### 🔴 OBRIGATÓRIO: Tipos de Commit

| Tipo | Uso | Exemplo |
|------|-----|---------|
| `feat` | Nova funcionalidade | `feat(usuarios): adiciona filtro por empresa` |
| `fix` | Correção de bug | `fix(ativos): corrige cálculo de depreciação` |
| `docs` | Documentação | `docs: atualiza README com instruções de setup` |
| `style` | Formatação (sem mudança de lógica) | `style: aplica formatação do editorconfig` |
| `refactor` | Refatoração (sem mudança de comportamento) | `refactor(auth): extrai validação de token` |
| `test` | Adição/correção de testes | `test(usuarios): adiciona testes do handler` |
| `chore` | Tarefas de manutenção | `chore: atualiza dependências` |
| `perf` | Melhoria de performance | `perf(queries): adiciona índice em Usuario` |
| `ci` | Configuração de CI/CD | `ci: adiciona stage de testes no pipeline` |

#### 🔴 OBRIGATÓRIO: Regras da Mensagem

| Regra | Exemplo Correto | Exemplo Incorreto |
|-------|-----------------|-------------------|
| Inicial minúscula | `adiciona validação` | `Adiciona validação` |
| Sem ponto final | `corrige bug no login` | `corrige bug no login.` |
| Imperativo | `adiciona`, `corrige`, `remove` | `adicionado`, `corrigido` |
| Máximo 72 caracteres | - | - |
| Em português | `adiciona filtro` | `add filter` |

#### 🟡 RECOMENDADO: Escopo

```
feat(usuarios): ...
feat(ativos): ...
feat(linhas): ...
feat(auth): ...
feat(api): ...
```

### 6.2 Branching Strategy

#### 🔴 OBRIGATÓRIO: Branches Protegidas

| Branch | Propósito | Merge Permitido |
|--------|-----------|-----------------|
| `main` | Produção | Apenas via PR de `release/*` ou `hotfix/*` |
| `develop` | Desenvolvimento | Apenas via PR de `feature/*` ou `fix/*` |

#### 🔴 OBRIGATÓRIO: Nomenclatura de Branches

| Tipo | Padrão | Exemplo |
|------|--------|---------|
| Feature | `feature/{ticket}-{descricao}` | `feature/IC-123-filtro-usuarios` |
| Bugfix | `fix/{ticket}-{descricao}` | `fix/IC-456-corrige-login` |
| Hotfix | `hotfix/{ticket}-{descricao}` | `hotfix/IC-789-erro-critico` |
| Release | `release/{versao}` | `release/1.2.0` |

### 6.3 Versionamento Semântico

#### 🔴 OBRIGATÓRIO: Formato de Versão

```
MAJOR.MINOR.PATCH

Exemplo: 1.2.3
```

| Componente | Quando Incrementar |
|------------|-------------------|
| MAJOR | Breaking changes na API |
| MINOR | Nova funcionalidade retrocompatível |
| PATCH | Correção de bugs retrocompatível |

### 6.4 Pull Requests

#### 🔴 OBRIGATÓRIO: Checklist de PR

- [ ] Código segue as convenções deste documento
- [ ] Testes foram adicionados/atualizados
- [ ] Documentação foi atualizada (se aplicável)
- [ ] Não há conflitos com a branch de destino
- [ ] Build passa sem erros
- [ ] Code review aprovado por pelo menos 1 revisor

#### 🔴 OBRIGATÓRIO: Título do PR

```
[TICKET-123] Descrição breve da mudança
```

---

## 7. Convenções de Documentação

### 7.1 Documentação de Código

#### 🔴 OBRIGATÓRIO: README por Módulo

Todo módulo/feature deve ter um README.md com:

```markdown
# Nome do Módulo

## Descrição
Breve descrição do propósito do módulo.

## Estrutura
Descrição da organização de pastas.

## Dependências
Lista de dependências externas.

## Configuração
Variáveis de ambiente ou configurações necessárias.

## Uso
Exemplos de uso básico.
```

### 7.2 Documentação de APIs

#### 🔴 OBRIGATÓRIO: Swagger/OpenAPI

- Todos os endpoints documentados com Swagger
- Descrições em português
- Exemplos de request/response
- Códigos de status documentados

#### 🟡 RECOMENDADO: Atributos de Documentação

```
[EndpointSummary("Descrição breve")]
[EndpointDescription("Descrição detalhada")]
[ProducesResponseType<UsuarioDto>(StatusCodes.Status200OK)]
[ProducesResponseType(StatusCodes.Status404NotFound)]
```

### 7.3 Arquivos de Documentação do Projeto

#### 🔴 OBRIGATÓRIO: Arquivos na Raiz

| Arquivo | Conteúdo |
|---------|----------|
| `README.md` | Visão geral, setup, como contribuir |
| `ARCHITECTURE.md` | Decisões arquiteturais, diagramas |
| `CONVENTIONS.md` | Este documento |
| `CHANGELOG.md` | Histórico de mudanças por versão |
| `.editorconfig` | Configurações de formatação |

#### 🔴 OBRIGATÓRIO: Documentação Externa ao Repositório

| Local | Conteúdo |
|-------|----------|
| `D:\DocumentosIC2\fases\` | Requisitos funcionais, modelos de dados, casos de uso, workflows, testes |
| `D:\DocumentosIC2\modelo-fisico-bd.sql` | DDL completo do banco de dados |

### 7.4 Changelog

#### 🔴 OBRIGATÓRIO: Formato do CHANGELOG

```markdown
# Changelog

## [1.2.0] - 2025-12-20

### Adicionado
- Nova funcionalidade X

### Alterado
- Comportamento de Y foi modificado

### Corrigido
- Bug Z foi corrigido

### Removido
- Funcionalidade W foi removida

### Segurança
- Vulnerabilidade V foi corrigida
```

### 7.5 Documentação de Requisitos Funcionais

#### 🔴 OBRIGATÓRIO: Localização

Toda documentação de requisitos fica em:

```
D:\DocumentosIC2\fases\
```

#### 🔴 OBRIGATÓRIO: Estrutura de Pastas

```
fases/
├── Fase-1-Fundacao/
├── Fase-2-Servicos-Essenciais/
│   ├── EPIC001-ADM-Administracao/
│   ├── EPIC002-CAD-Cadastros/
│   ├── EPIC003-GES-Gestao/
│   │   ├── RF016-Gestao-Categorias-Ativos/
│   │   │   ├── RF016.md
│   │   │   ├── MD-RF016.md
│   │   │   ├── UC-RF016.md
│   │   │   ├── WF-RF016.md
│   │   │   ├── TC-RF016-SISTEMA.md
│   │   │   └── TC-RF016-OUTROS.md
│   │   ├── RF017-Gestao-Marcas/
│   │   └── ...
│   └── ...
├── Fase-3-Telecom/
├── Fase-4-Service-Desk/
├── Fase-5-Financeiro/
└── Fase-6-Analytics/
```

#### 🔴 OBRIGATÓRIO: Nomenclatura de Pastas

| Nível | Padrão | Exemplo |
|-------|--------|---------|
| Fase | `Fase-{N}-{Nome}` | `Fase-2-Servicos-Essenciais` |
| Epic | `EPIC{NNN}-{Sigla}-{Nome}` | `EPIC003-GES-Gestao` |
| RF | `RF{NNN}-{Nome}` | `RF016-Gestao-Categorias-Ativos` |

#### 🔴 OBRIGATÓRIO: Arquivos por Requisito Funcional

Cada RF deve conter os seguintes arquivos:

| Arquivo | Descrição | Conteúdo |
|---------|-----------|----------|
| `RF{NNN}.md` | Requisito Funcional | Especificação completa do requisito, regras de negócio, critérios de aceite |
| `MD-RF{NNN}.md` | Modelo de Dados | Entidades, atributos, relacionamentos, constraints |
| `UC-RF{NNN}.md` | Casos de Uso | Atores, fluxos principal/alternativo/exceção |
| `WF-RF{NNN}.md` | Workflows | Diagramas de fluxo, transições de estado, aprovações |
| `TC-RF{NNN}-SISTEMA.md` | Testes de Sistema | Casos de teste funcionais automatizados |
| `TC-RF{NNN}-OUTROS.md` | Outros Testes | Testes manuais, exploratórios, de integração |

#### 🟡 RECOMENDADO: Arquivos Opcionais

| Arquivo | Quando Usar |
|---------|-------------|
| `API-RF{NNN}.md` | Quando houver endpoints específicos a documentar |
| `INT-RF{NNN}.md` | Quando houver integrações externas |
| `MIG-RF{NNN}.md` | Quando houver migração de dados do legado |
| `SEC-RF{NNN}.md` | Quando houver requisitos de segurança específicos |

#### 🔴 OBRIGATÓRIO: Rastreabilidade Código ↔ Documentação

Todo código deve referenciar o RF correspondente:

**Backend (Handler):**
```csharp
/// <summary>
/// Cria uma nova categoria de ativo.
/// </summary>
/// <remarks>
/// Documentação: RF016 - Gestão de Categorias de Ativos
/// Caminho: D:\DocumentosIC2\fases\Fase-2-Servicos-Essenciais\EPIC003-GES-Gestao\RF016-Gestao-Categorias-Ativos\
/// </remarks>
public class CreateCategoriaAtivoCommandHandler : IRequestHandler<CreateCategoriaAtivoCommand, Guid>
```

**Frontend (Component):**
```typescript
/**
 * Lista de categorias de ativos.
 * 
 * @see RF016 - Gestão de Categorias de Ativos
 * @see D:\DocumentosIC2\fases\Fase-2-Servicos-Essenciais\EPIC003-GES-Gestao\RF016-Gestao-Categorias-Ativos\
 */
@Component({...})
export class CategoriasListComponent { }
```

#### 🔴 OBRIGATÓRIO: Registro no Central de Módulos

Todo RF implementado deve ser registrado no Central de Módulos com:

| Campo | Descrição | Exemplo |
|-------|-----------|---------|
| Código | Código do RF | `RF016` |
| Nome | Nome do requisito | `Gestão de Categorias de Ativos` |
| Epic | Epic relacionada | `EPIC003-GES` |
| Fase | Fase do projeto | `Fase 2` |
| Ações | Operações disponíveis | `CREATE`, `READ`, `UPDATE`, `DELETE` |
| Permissões | Códigos de permissão | `GES.CATEGORIAS.CREATE`, `GES.CATEGORIAS.READ`, etc. |
| Status | Estado atual | `Implementado`, `Em Desenvolvimento`, `Planejado` |

#### 🔴 OBRIGATÓRIO: Vínculo Ação → Permissão → RBAC

Cada ação registrada gera uma permissão no sistema:

```
RF016 - Gestão de Categorias de Ativos
│
├── Ação: CREATE → Permissão: GES.CATEGORIAS.CREATE
├── Ação: READ   → Permissão: GES.CATEGORIAS.READ
├── Ação: UPDATE → Permissão: GES.CATEGORIAS.UPDATE
└── Ação: DELETE → Permissão: GES.CATEGORIAS.DELETE
```

Essas permissões são então vinculadas aos Perfis (Roles) na matriz de RBAC.

### 7.6 Relacionamento Entre Documentos

#### 🔴 OBRIGATÓRIO: Hierarquia de Documentação

```
ARCHITECTURE.md          → Decisões macro, padrões globais
    │
    └── CONVENTIONS.md   → Regras de implementação
            │
            └── fases/   → Especificações detalhadas por RF
                 │
                 └── RF → Código-fonte (rastreável)
```

#### 🟡 RECOMENDADO: Navegação Entre Documentos

Cada documento deve ter links para:
- Documento pai (contexto)
- Documentos relacionados (dependências)
- Código implementado (quando aplicável)

---

## 8. Checklist de Conformidade

### 8.1 Checklist para Novo Código

#### Backend

- [ ] Classe no namespace correto conforme estrutura de pastas
- [ ] Nomenclatura segue padrões definidos
- [ ] Handler valida ClienteId do usuário atual
- [ ] Validator criado para Commands que modificam dados
- [ ] DTO criado (nunca expor entidades diretamente)
- [ ] Testes unitários com cobertura mínima
- [ ] Documentação XML em classes/métodos públicos
- [ ] Referência ao RF correspondente no XML docs
- [ ] Funcionalidade registrada no Central de Módulos

#### Frontend

- [ ] Componente é standalone
- [ ] Seletor usa prefixo `app-`
- [ ] ChangeDetectionStrategy.OnPush configurado
- [ ] Signals usados para estado local
- [ ] Observables têm unsubscribe apropriado
- [ ] Formulários usam Reactive Forms
- [ ] Strings de UI estão nos arquivos i18n
- [ ] Referência ao RF correspondente no JSDoc do componente

#### Geral

- [ ] Código formatado conforme .editorconfig
- [ ] Sem warnings de compilação/lint
- [ ] Commit message segue Conventional Commits
- [ ] Branch nomeada corretamente
- [ ] PR com título no formato correto

### 8.2 Checklist para Code Review

- [ ] Código segue as convenções deste documento
- [ ] Não há código duplicado
- [ ] Não há dependências circulares
- [ ] Tratamento de erros adequado
- [ ] Logs apropriados (sem dados sensíveis)
- [ ] Validação de multi-tenancy presente
- [ ] Testes cobrem cenários principais e de erro
- [ ] Performance aceitável (sem N+1, queries otimizadas)
- [ ] Referência ao RF está presente no código
- [ ] Funcionalidade registrada no Central de Módulos
- [ ] Permissões (ações) registradas e vinculadas aos perfis

---

## 9. Convenções de Multi-Tenancy e Soft Delete

### 9.1 Multi-Tenancy - Hierarquia de 4 Níveis

#### 🔴 OBRIGATÓRIO: Campo ClienteId em Todas as Entidades Multi-Tenant

```csharp
public class MinhaEntidade : BaseAuditableGuidEntity
{
    /// <summary>
    /// ID do Cliente (TENANT RAIZ) - OBRIGATÓRIO
    /// Query Filter automático aplicado pelo EF Core
    /// </summary>
    public Guid ClienteId { get; set; }

    /// <summary>
    /// ID da Empresa (Unidade Fiscal) - OPCIONAL
    /// Usado quando a entidade pertence a uma empresa específica
    /// </summary>
    public Guid? EmpresaId { get; set; }

    // Outros campos...
}
```

#### 🔴 OBRIGATÓRIO: Hierarquia Completa

| Nível | Campo | Tipo | Obrigatório | Propósito | Query Filter |
|-------|-------|------|-------------|-----------|--------------|
| 1. Cliente | `ClienteId` | `Guid` | ✅ SIM | **Isolamento multi-tenant** | ✅ SIM |
| 2. Conglomerado | `ConglomeradoId` | `Guid?` | ❌ NÃO | Agrupamento lógico | ❌ NÃO |
| 3. Empresa | `EmpresaId` | `Guid?` | ❌ NÃO | Organização fiscal (CNPJ) | ❌ NÃO |
| 4. Filial | `FilialId` | `Guid?` | ❌ NÃO | Localização física | ❌ NÃO |

#### 🔴 OBRIGATÓRIO: Validação de Multi-Tenancy em Handlers

Todo Handler que acessa dados deve validar `ClienteId`:

```csharp
public class MinhaCommandHandler : IRequestHandler<MinhaCommand, Guid>
{
    private readonly ICurrentUserService _currentUser;
    private readonly IApplicationDbContext _context;

    public async Task<Guid> Handle(MinhaCommand request, CancellationToken cancellationToken)
    {
        // ✅ OBRIGATÓRIO: Validar ClienteId
        if (request.ClienteId != _currentUser.ClienteId)
        {
            throw new ForbiddenAccessException("Acesso negado a dados de outro cliente");
        }

        // Lógica do handler...
    }
}
```

#### 🔴 OBRIGATÓRIO: Query Filter no DbContext

```csharp
// ApplicationDbContext.cs
protected override void OnModelCreating(ModelBuilder modelBuilder)
{
    // Aplicar Query Filter a TODAS as entidades que implementam IMultiTenantEntity
    foreach (var entityType in modelBuilder.Model.GetEntityTypes())
    {
        if (typeof(IMultiTenantEntity).IsAssignableFrom(entityType.ClrType))
        {
            var parameter = Expression.Parameter(entityType.ClrType, "e");
            var body = Expression.Equal(
                Expression.Property(parameter, nameof(IMultiTenantEntity.ClienteId)),
                Expression.Property(
                    Expression.Constant(_currentUserService),
                    nameof(ICurrentUserService.ClienteId)
                )
            );
            modelBuilder.Entity(entityType.ClrType).HasQueryFilter(Expression.Lambda(body, parameter));
        }
    }
}
```

#### 🟡 RECOMENDADO: Escopo de Entidade

| Escopo | ClienteId | EmpresaId | Uso |
|--------|-----------|-----------|-----|
| **Global** | Obrigatório | NULL | Configurações/dados compartilhados por todo o cliente |
| **Por Empresa** | Obrigatório | Obrigatório | Dados específicos de uma empresa (ex: Ativos, Linhas) |

#### 🔴 OBRIGATÓRIO: Tabelas SEM Multi-Tenancy

Apenas tabelas de sistema compartilhado podem omitir `ClienteId`:

```
- SistemaConfiguracao
- SistemaParametro
- SistemaIdioma
- SistemaFeatureFlag (quando global)
- Permission
- Role (perfis de sistema)
```

---

### 9.2 Soft Delete - Padronização com FlExcluido

#### 🔴 OBRIGATÓRIO: Campo FlExcluido para Soft Delete

```csharp
public class MinhaEntidade : BaseAuditableGuidEntity
{
    /// <summary>
    /// Soft delete: false=ativo (não deletado), true=excluído (deletado)
    /// </summary>
    public bool FlExcluido { get; set; } = false;

    /// <summary>
    /// Flag funcional (opcional): true=habilitado, false=desabilitado
    /// Semântica independente de FlExcluido
    /// </summary>
    public bool Ativo { get; set; } = true;
}
```

#### 🔴 OBRIGATÓRIO: Semântica FlExcluido vs Ativo

| Campo | Propósito | Valores | Uso |
|-------|-----------|---------|-----|
| `FlExcluido` | **Soft delete** | `false` = NÃO deletado<br>`true` = Deletado | **OBRIGATÓRIO** em todas as entidades |
| `Ativo` | **Flag funcional** | `true` = Habilitado<br>`false` = Desabilitado | **OPCIONAL** - quando entidade tem estado funcional |

#### 🔴 OBRIGATÓRIO: Queries Respeitando Soft Delete

**Backend:**
```csharp
// ✅ CORRETO: Filtrar registros não excluídos
var ativos = await _context.Ativos
    .Where(a => !a.FlExcluido)
    .ToListAsync();

// ✅ CORRETO: Incluir apenas ativos (funcional) E não excluídos (soft delete)
var ativosHabilitados = await _context.Ativos
    .Where(a => a.Ativo && !a.FlExcluido)
    .ToListAsync();

// ❌ INCORRETO: Usar Ativo para soft delete quando há FlExcluido
var ativos = await _context.Ativos
    .Where(a => a.Ativo)  // ERRADO se Ativo for flag funcional
    .ToListAsync();
```

**Frontend:**
```typescript
// ✅ CORRETO: Service com filtros claros
getEmpresas(incluirInativos = false, incluirExcluidos = false): Observable<Empresa[]> {
  return this.http.get<Empresa[]>(`${this.apiUrl}/empresas`)
    .pipe(
      map(empresas => {
        let resultado = empresas;

        // Sempre filtrar excluídos por padrão
        if (!incluirExcluidos) {
          resultado = resultado.filter(e => !e.flExcluido);
        }

        // Filtrar inativos se necessário
        if (!incluirInativos) {
          resultado = resultado.filter(e => e.ativo);
        }

        return resultado;
      })
    );
}
```

#### 🔴 OBRIGATÓRIO: Operações de Soft Delete

**Exclusão (soft delete):**
```csharp
// ✅ CORRETO: Setar FlExcluido
entidade.FlExcluido = true;
entidade.DeletedAt = DateTime.UtcNow;
entidade.DeletedBy = _currentUser.UserId;
await _context.SaveChangesAsync();

// ❌ INCORRETO: Deletar fisicamente (proibido)
_context.Ativos.Remove(entidade);
```

**Restauração:**
```csharp
// ✅ CORRETO: Restaurar registro deletado
entidade.FlExcluido = false;
entidade.DeletedAt = null;
entidade.DeletedBy = null;
await _context.SaveChangesAsync();
```

**Inativação (funcional):**
```csharp
// ✅ CORRETO: Desabilitar funcionalidade (independente de soft delete)
entidade.Ativo = false;
// FlExcluido permanece false (não deletado)
await _context.SaveChangesAsync();
```

#### 🔴 OBRIGATÓRIO: Migration para Adicionar FlExcluido

```sql
-- ✅ CORRETO: Adicionar coluna com default correto
ALTER TABLE MinhaTabela ADD FlExcluido BIT NOT NULL DEFAULT 0;

-- Se havia Ativo sendo usado para soft delete:
-- Migrar dados: Ativo false → FlExcluido true
UPDATE MinhaTabela SET FlExcluido = 1 WHERE Ativo = 0;

-- Redefinir Ativo para flag funcional (todos habilitados por padrão)
UPDATE MinhaTabela SET Ativo = 1;
```

#### 🔴 OBRIGATÓRIO: Query Filter para Soft Delete

```csharp
// ApplicationDbContext.cs
protected override void OnModelCreating(ModelBuilder modelBuilder)
{
    // Aplicar Query Filter global para soft delete
    foreach (var entityType in modelBuilder.Model.GetEntityTypes())
    {
        var hasFlExcluido = entityType.ClrType.GetProperty("FlExcluido");

        if (hasFlExcluido != null)
        {
            var parameter = Expression.Parameter(entityType.ClrType, "e");
            var body = Expression.Equal(
                Expression.Property(parameter, "FlExcluido"),
                Expression.Constant(false)
            );
            modelBuilder.Entity(entityType.ClrType).HasQueryFilter(Expression.Lambda(body, parameter));
        }
    }
}

// Para incluir deletados em queries específicas:
var todosIncluindoExcluidos = await _context.Ativos
    .IgnoreQueryFilters()
    .Where(a => a.ClienteId == _currentUser.ClienteId)  // Ainda respeitar multi-tenancy!
    .ToListAsync();
```

#### 🟡 RECOMENDADO: Estados Combinados

| FlExcluido | Ativo | Significado | Comportamento |
|------------|-------|-------------|---------------|
| `false` | `true` | Ativo e habilitado | ✅ Aparece em listagens normais |
| `false` | `false` | Ativo mas desabilitado | ⚠️ Não aparece em listagens (inativo) |
| `true` | `true` | Deletado | ❌ Não aparece (soft delete) |
| `true` | `false` | Deletado | ❌ Não aparece (soft delete) |

#### 🔴 OBRIGATÓRIO: Frontend - Interface TypeScript

```typescript
// ✅ CORRETO: Modelo com ambos campos quando aplicável
export interface Empresa {
  id: string;
  nome: string;
  cnpj: string;

  // Flag funcional (opcional, quando presente)
  ativo: boolean;

  // Soft delete (obrigatório)
  flExcluido: boolean;

  // Auditoria
  created: Date;
  createdBy?: string;
  lastModified?: Date;
  lastModifiedBy?: string;
  deletedAt?: Date;
  deletedBy?: string;
}
```

#### 🔴 OBRIGATÓRIO: Frontend - Ações de UI

```html
<!-- Template do componente -->
<tr *ngFor="let empresa of empresas()">
  <td>{{ empresa.nome }}</td>
  <td>
    <!-- Badge de status -->
    <span class="badge badge-success" *ngIf="empresa.ativo && !empresa.flExcluido">
      Ativo
    </span>
    <span class="badge badge-warning" *ngIf="!empresa.ativo && !empresa.flExcluido">
      Inativo
    </span>
    <span class="badge badge-danger" *ngIf="empresa.flExcluido">
      Excluído
    </span>
  </td>
  <td>
    <!-- Botões condicionais -->
    <button *ngIf="!empresa.flExcluido && empresa.ativo"
            (click)="inativar(empresa.id)">
      Inativar
    </button>
    <button *ngIf="!empresa.flExcluido && !empresa.ativo"
            (click)="ativar(empresa.id)">
      Ativar
    </button>
    <button *ngIf="!empresa.flExcluido"
            (click)="excluir(empresa.id)">
      Excluir
    </button>
    <button *ngIf="empresa.flExcluido"
            (click)="restaurar(empresa.id)">
      Restaurar
    </button>
  </td>
</tr>
```

---

## 10. Glossário

| Termo | Definição |
|-------|-----------|
| **Command** | Operação que modifica estado (write) |
| **Query** | Operação que apenas lê dados (read) |
| **Handler** | Classe que processa um Command ou Query |
| **DTO** | Data Transfer Object - objeto para transporte de dados |
| **Multi-tenancy** | Isolamento de dados por ClienteId (Query Filter automático do EF Core) |
| **Soft Delete** | Exclusão lógica usando `FlExcluido = true` (não deletar fisicamente) |
| **FlExcluido** | Campo booleano para soft delete (false=ativo, true=excluído) |
| **Ativo** | Campo booleano OPCIONAL para flag funcional (habilitado/desabilitado) |
| **SUT** | System Under Test - classe sendo testada |
| **Smart Component** | Componente que gerencia estado e serviços |
| **Dumb Component** | Componente apenas de apresentação |
| **RF** | Requisito Funcional - especificação de uma funcionalidade |
| **Epic** | Agrupamento de RFs relacionados por domínio |
| **Fase** | Etapa do projeto contendo múltiplas Epics |
| **Central de Módulos** | Registro de todas as funcionalidades e ações do sistema |
| **MD** | Modelo de Dados - documento de entidades e relacionamentos |
| **UC** | Use Case - documento de casos de uso |
| **WF** | Workflow - documento de fluxos e transições |
| **TC** | Test Case - documento de casos de teste |

---

## Histórico de Revisões

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 1.1 | 2025-12-20 | Arquitetura | Adicionada seção 7.5 (Documentação de RFs) e 7.6 (Relacionamento) |
| 1.0 | 2025-12-20 | Arquitetura | Versão inicial |

---

**Mantido por:** Time de Arquitetura IControlIT  
**Última Revisão:** 2025-12-20  
**Próxima Revisão:** 2026-03-20