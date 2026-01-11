# CONVENTIONS.md

# 📐 Convenções Técnicas do Projeto IControlIT

> **Versão:** 1.2
> **Data:** 2026-01-10
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
3. [Nomenclatura de Data-test Attributes (Test-First)](#3-nomenclatura-de-data-test-attributes-test-first) **✨ NOVO**
4. [Convenções de Camadas](#4-convenções-de-camadas)
5. [Padrões de Código](#5-padrões-de-código)
6. [Convenções de Testes](#6-convenções-de-testes)
7. [Convenções de Commits e Versionamento](#7-convenções-de-commits-e-versionamento)
8. [Convenções de Documentação](#8-convenções-de-documentação)
9. [Checklist de Conformidade](#9-checklist-de-conformidade)

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

## 3. Nomenclatura de Data-test Attributes (Test-First) **✨ NOVO**

**Versão:** 1.0
**Data:** 2026-01-09
**Contexto:** Criado após análise do RF006 onde falta de padronização resultou em 32 falhas E2E por seletores não encontrados.

### 3.1. Princípio Fundamental

**Data-test attributes são OBRIGATÓRIOS para TODOS os elementos interativos.**

Este não é um princípio aspiracional. É uma **regra obrigatória** com **bloqueios automáticos**.

**Referência:** `CLAUDE.md` seção 18 "ALINHAMENTO OBRIGATÓRIO COM TESTES"

---

### 3.2. Formato Padrão (OBRIGATÓRIO)

#### 🔴 REGRA: Nomenclatura de Data-test

**Formato:** `RFXXX-[acao]-[alvo]`

**Componentes:**
- `RFXXX`: Identificador do Requisito Funcional (ex: RF006, RF012)
- `[acao]`: Verbo que descreve a ação (criar, editar, excluir, salvar, cancelar, listar, filtrar)
- `[alvo]`: Substantivo que identifica o elemento de negócio (cliente, usuario, ativo, contrato)

**Características obrigatórias:**
- Tudo em **minúsculas**
- Separação por **hífen** (`-`)
- **Sem acentos** ou caracteres especiais
- **Sem espaços**
- **Prefixo RF obrigatório** para elementos de ação
- **Sem prefixo RF** para estados de UI reutilizáveis (loading, empty, error)

---

### 3.3. Elementos que DEVEM ter Data-test

#### 🔴 OBRIGATÓRIO: Botões de Ação

**Padrão:** `RFXXX-[acao]-[alvo]`

| Tipo de Botão | Padrão | Exemplo |
|---------------|--------|---------|
| Criar novo registro | `RFXXX-criar-[entidade]` | `RF006-criar-cliente` |
| Editar registro existente | `RFXXX-editar-[entidade]` | `RF006-editar-cliente` |
| Excluir registro | `RFXXX-excluir-[entidade]` | `RF006-excluir-cliente` |
| Salvar formulário | `RFXXX-salvar-[entidade]` | `RF006-salvar-cliente` |
| Cancelar operação | `RFXXX-cancelar-[contexto]` | `RF006-cancelar-edicao` |
| Buscar/Filtrar | `RFXXX-filtrar-[entidade]` | `RF006-filtrar-cliente` |
| Limpar filtros | `RFXXX-limpar-filtros` | `RF006-limpar-filtros` |

**Exemplo HTML:**
```html
<!-- ✅ CORRETO -->
<button mat-raised-button data-test="RF006-criar-cliente" (click)="criarCliente()">
  Novo Cliente
</button>

<button mat-icon-button data-test="RF006-editar-cliente" (click)="editarCliente(cliente.id)">
  <mat-icon>edit</mat-icon>
</button>

<!-- ❌ INCORRETO (sem data-test) -->
<button mat-raised-button (click)="criarCliente()">
  Novo Cliente
</button>

<!-- ❌ INCORRETO (nomenclatura inconsistente) -->
<button mat-raised-button data-test="btn-novo-cliente" (click)="criarCliente()">
  Novo Cliente
</button>
```

---

#### 🔴 OBRIGATÓRIO: Campos de Formulário

**Padrão:** `RFXXX-input-[nome-campo]`

| Tipo de Campo | Padrão | Exemplo |
|---------------|--------|---------|
| Input text | `RFXXX-input-[campo]` | `RF006-input-razaosocial` |
| Input number | `RFXXX-input-[campo]` | `RF006-input-valor` |
| Input email | `RFXXX-input-[campo]` | `RF006-input-email` |
| Select/Dropdown | `RFXXX-select-[campo]` | `RF006-select-tipopessoa` |
| Textarea | `RFXXX-textarea-[campo]` | `RF006-textarea-observacoes` |
| Checkbox | `RFXXX-checkbox-[campo]` | `RF006-checkbox-ativo` |
| Radio button | `RFXXX-radio-[campo]` | `RF006-radio-tipopagamento` |
| Date picker | `RFXXX-datepicker-[campo]` | `RF006-datepicker-datainicio` |

**Exemplo HTML (Angular + PrimeNG):**
```html
<!-- ✅ CORRETO -->
<input
  pInputText
  data-test="RF006-input-razaosocial"
  formControlName="razaoSocial"
  placeholder="Razão Social"
/>

<p-dropdown
  data-test="RF006-select-tipopessoa"
  formControlName="tipoPessoa"
  [options]="tiposPessoa"
></p-dropdown>

<!-- ❌ INCORRETO (sem data-test) -->
<input pInputText formControlName="razaoSocial" />

<!-- ❌ INCORRETO (nomenclatura inconsistente) -->
<input pInputText data-test="input-razao" formControlName="razaoSocial" />
```

---

#### 🔴 OBRIGATÓRIO: Mensagens de Erro de Validação

**Padrão:** `RFXXX-input-[campo]-error`

| Tipo | Padrão | Exemplo |
|------|--------|---------|
| Erro de campo obrigatório | `RFXXX-input-[campo]-error` | `RF006-input-razaosocial-error` |
| Erro de formato (email, CPF) | `RFXXX-input-[campo]-error` | `RF006-input-email-error` |
| Erro de tamanho (maxlength) | `RFXXX-input-[campo]-error` | `RF006-input-cnpj-error` |

**Exemplo HTML (Angular Material):**
```html
<!-- ✅ CORRETO -->
<mat-form-field>
  <input matInput data-test="RF006-input-email" formControlName="email" />
  <mat-error data-test="RF006-input-email-error">
    {{ getErrorMessage('email') }}
  </mat-error>
</mat-form-field>

<!-- ❌ INCORRETO (sem data-test no mat-error) -->
<mat-form-field>
  <input matInput data-test="RF006-input-email" formControlName="email" />
  <mat-error>{{ getErrorMessage('email') }}</mat-error>
</mat-form-field>
```

---

#### 🔴 OBRIGATÓRIO: Tabelas e Listas

**Padrão:**
- Container: `[entidade]-list` (sem prefixo RF)
- Linha/Item: `[entidade]-row` (sem prefixo RF)
- Ações da linha: `RFXXX-[acao]-[entidade]` (com prefixo RF)

| Elemento | Padrão | Exemplo |
|----------|--------|---------|
| Container da lista | `[entidade]-list` | `clientes-list` |
| Linha/Item da lista | `[entidade]-row` | `cliente-row` |
| Botão editar (linha) | `RFXXX-editar-[entidade]` | `RF006-editar-cliente` |
| Botão excluir (linha) | `RFXXX-excluir-[entidade]` | `RF006-excluir-cliente` |

**Exemplo HTML (PrimeNG Table):**
```html
<!-- ✅ CORRETO -->
<p-table data-test="clientes-list" [value]="clientes">
  <ng-template pTemplate="body" let-cliente>
    <tr data-test="cliente-row">
      <td>{{ cliente.razaoSocial }}</td>
      <td>
        <button
          mat-icon-button
          data-test="RF006-editar-cliente"
          (click)="editar(cliente)"
        >
          <mat-icon>edit</mat-icon>
        </button>
        <button
          mat-icon-button
          data-test="RF006-excluir-cliente"
          (click)="excluir(cliente)"
        >
          <mat-icon>delete</mat-icon>
        </button>
      </td>
    </tr>
  </ng-template>
</p-table>

<!-- ❌ INCORRETO (sem data-test) -->
<p-table [value]="clientes">
  <ng-template pTemplate="body" let-cliente>
    <tr>
      <td>{{ cliente.razaoSocial }}</td>
    </tr>
  </ng-template>
</p-table>
```

---

#### 🔴 OBRIGATÓRIO: Estados de UI (Reutilizáveis)

**Padrão:** `[estado]` (SEM prefixo RF, pois são reutilizáveis)

| Estado | Data-test | Descrição |
|--------|-----------|-----------|
| Loading/Spinner | `loading-spinner` | Spinner exibido durante carregamento |
| Lista vazia | `empty-state` | Mensagem quando lista está vazia |
| Erro ao carregar | `error-message` | Mensagem de erro ao carregar dados |
| Sem resultados (filtro) | `no-results` | Mensagem quando filtro não retorna resultados |

**Exemplo HTML:**
```html
<!-- ✅ CORRETO -->
<div *ngIf="isLoading" data-test="loading-spinner">
  <mat-spinner></mat-spinner>
</div>

<div *ngIf="clientes.length === 0 && !isLoading" data-test="empty-state">
  <p>Nenhum cliente encontrado.</p>
</div>

<div *ngIf="hasError" data-test="error-message">
  <p>Erro ao carregar clientes.</p>
</div>

<!-- ❌ INCORRETO (sem data-test) -->
<div *ngIf="isLoading">
  <mat-spinner></mat-spinner>
</div>
```

---

#### 🔴 OBRIGATÓRIO: Dialogs/Modais

**Padrão:**
- Container: `RFXXX-dialog-[contexto]`
- Botões: `RFXXX-dialog-[acao]`

| Elemento | Padrão | Exemplo |
|----------|--------|---------|
| Container do dialog | `RFXXX-dialog-[contexto]` | `RF006-dialog-confirmar-exclusao` |
| Botão confirmar | `RFXXX-dialog-confirmar` | `RF006-dialog-confirmar` |
| Botão cancelar | `RFXXX-dialog-cancelar` | `RF006-dialog-cancelar` |

**Exemplo HTML (Angular Material Dialog):**
```html
<!-- ✅ CORRETO -->
<div mat-dialog-content data-test="RF006-dialog-confirmar-exclusao">
  <p>Tem certeza que deseja excluir este cliente?</p>
</div>
<div mat-dialog-actions>
  <button
    mat-button
    data-test="RF006-dialog-cancelar"
    (click)="onCancel()"
  >
    Cancelar
  </button>
  <button
    mat-raised-button
    color="warn"
    data-test="RF006-dialog-confirmar"
    (click)="onConfirm()"
  >
    Confirmar
  </button>
</div>

<!-- ❌ INCORRETO (sem data-test) -->
<div mat-dialog-content>
  <p>Tem certeza?</p>
</div>
```

---

### 3.4. Casos Especiais

#### Aliases (Compatibilidade Retroativa)

**Permitido:** Adicionar aliases para compatibilidade com implementações existentes.

**Como documentar no UC:**
```yaml
passos:
  - numero: 3
    acao: "Clicar em 'Novo Cliente'"
    elemento:
      tipo: button
      data_test: "RF006-criar-cliente"
      aliases: ["btn-novo-cliente", "criar-cliente"]  # ✅ Aliases permitidos
      localizacao: "clientes.component.html linha 42"
```

**Exemplo HTML:**
```html
<!-- ✅ CORRETO (data-test principal + alias) -->
<button
  mat-raised-button
  data-test="RF006-criar-cliente"
  id="btn-novo-cliente"
  (click)="criarCliente()"
>
  Novo Cliente
</button>
```

---

#### Elementos Dinâmicos (Loop)

**Padrão:** Data-test base + índice/id

| Tipo | Padrão | Exemplo |
|------|--------|---------|
| Linha de tabela (por índice) | `[entidade]-row` | `cliente-row` (Playwright usa nth-child) |
| Botão editar (por linha) | `RFXXX-editar-[entidade]` | `RF006-editar-cliente` (Playwright filtra por row) |

**Exemplo HTML:**
```html
<!-- ✅ CORRETO -->
<tr *ngFor="let cliente of clientes; let i = index" data-test="cliente-row">
  <td>{{ cliente.razaoSocial }}</td>
  <td>
    <button
      mat-icon-button
      data-test="RF006-editar-cliente"
      (click)="editar(cliente)"
    >
      <mat-icon>edit</mat-icon>
    </button>
  </td>
</tr>
```

**Uso no Playwright:**
```typescript
// Editar o primeiro cliente
await page.locator('[data-test="cliente-row"]').first()
  .locator('[data-test="RF006-editar-cliente"]').click();

// Editar o terceiro cliente
await page.locator('[data-test="cliente-row"]').nth(2)
  .locator('[data-test="RF006-editar-cliente"]').click();
```

---

### 3.5. Validação de Nomenclatura

#### 🔴 OBRIGATÓRIO: Script de Auditoria

**Comando:**
```bash
npm run audit-data-test RFXXX
```

**O que valida:**
1. TODOS os data-test de `UC-RFXXX.yaml` estão presentes no HTML
2. Nomenclatura segue padrão `RFXXX-[acao]-[alvo]`
3. Estados de UI (loading, empty, error) estão presentes
4. Campos de formulário possuem data-test
5. Mensagens de erro possuem data-test

**Exit codes:**
- `0`: Auditoria PASSOU (100% de cobertura)
- `1`: Auditoria FALHOU (data-test ausentes ou inconsistentes)

**Bloqueio:**
- Se exit code = 1 → ❌ Frontend REPROVADO (não pode prosseguir para testes E2E)

**Referência:** `CLAUDE.md` seção 18.2.2 "Bloqueios Obrigatórios"

---

### 3.6. Integração com Testes E2E (Playwright)

#### Como UC → TC → MT → E2E se conectam

**Fluxo de rastreabilidade:**

1. **UC-RFXXX.yaml** especifica data-test:
```yaml
passos:
  - numero: 3
    acao: "Clicar em 'Novo Cliente'"
    elemento:
      tipo: button
      data_test: "RF006-criar-cliente"
```

2. **TC-RFXXX.yaml** especifica seletor E2E:
```yaml
passos:
  - numero: 3
    descricao: "Clicar em 'Novo Cliente'"
    seletor: "[data-test='RF006-criar-cliente']"
    acao_e2e: "page.click('[data-test=\"RF006-criar-cliente\"]')"
```

3. **MT-RFXXX.data.ts** centraliza seletores:
```typescript
export const DATA_TEST_SELECTORS = {
  btnNovoCliente: 'RF006-criar-cliente',
  inputRazaoSocial: 'RF006-input-razaosocial',
  loadingSpinner: 'loading-spinner'
};
```

4. **Teste E2E (Playwright)** usa seletores de MT:
```typescript
import { DATA_TEST_SELECTORS } from './MT-RF006.data';

test('deve criar cliente com sucesso', async ({ page }) => {
  await page.click(`[data-test="${DATA_TEST_SELECTORS.btnNovoCliente}"]`);
  await page.fill(`[data-test="${DATA_TEST_SELECTORS.inputRazaoSocial}"]`, 'Empresa Teste');
  // ...
});
```

---

### 3.7. Exemplos Completos por Cenário

#### Cenário 1: Listagem com CRUD

```html
<!-- Container da lista -->
<div>
  <!-- Botão criar (topo) -->
  <button
    mat-raised-button
    data-test="RF006-criar-cliente"
    (click)="criarCliente()"
  >
    Novo Cliente
  </button>

  <!-- Estados de UI -->
  <div *ngIf="isLoading" data-test="loading-spinner">
    <mat-spinner></mat-spinner>
  </div>

  <div *ngIf="clientes.length === 0 && !isLoading" data-test="empty-state">
    <p>Nenhum cliente encontrado.</p>
  </div>

  <div *ngIf="hasError" data-test="error-message">
    <p>Erro ao carregar clientes.</p>
  </div>

  <!-- Tabela -->
  <p-table data-test="clientes-list" [value]="clientes">
    <ng-template pTemplate="body" let-cliente>
      <tr data-test="cliente-row">
        <td>{{ cliente.razaoSocial }}</td>
        <td>
          <button
            mat-icon-button
            data-test="RF006-editar-cliente"
            (click)="editar(cliente)"
          >
            <mat-icon>edit</mat-icon>
          </button>
          <button
            mat-icon-button
            data-test="RF006-excluir-cliente"
            (click)="excluir(cliente)"
          >
            <mat-icon>delete</mat-icon>
          </button>
        </td>
      </tr>
    </ng-template>
  </p-table>
</div>
```

---

#### Cenário 2: Formulário Completo

```html
<form [formGroup]="clienteForm" data-test="RF006-form-cliente">
  <!-- Campo 1: Razão Social -->
  <mat-form-field>
    <input
      matInput
      data-test="RF006-input-razaosocial"
      formControlName="razaoSocial"
      placeholder="Razão Social"
    />
    <mat-error data-test="RF006-input-razaosocial-error">
      {{ getErrorMessage('razaoSocial') }}
    </mat-error>
  </mat-form-field>

  <!-- Campo 2: CNPJ -->
  <mat-form-field>
    <input
      matInput
      data-test="RF006-input-cnpj"
      formControlName="cnpj"
      placeholder="CNPJ"
    />
    <mat-error data-test="RF006-input-cnpj-error">
      {{ getErrorMessage('cnpj') }}
    </mat-error>
  </mat-form-field>

  <!-- Campo 3: Tipo Pessoa (Select) -->
  <mat-form-field>
    <mat-select
      data-test="RF006-select-tipopessoa"
      formControlName="tipoPessoa"
      placeholder="Tipo Pessoa"
    >
      <mat-option value="F">Física</mat-option>
      <mat-option value="J">Jurídica</mat-option>
    </mat-select>
    <mat-error data-test="RF006-select-tipopessoa-error">
      {{ getErrorMessage('tipoPessoa') }}
    </mat-error>
  </mat-form-field>

  <!-- Ações do formulário -->
  <div>
    <button
      mat-button
      data-test="RF006-cancelar-edicao"
      (click)="cancelar()"
    >
      Cancelar
    </button>
    <button
      mat-raised-button
      color="primary"
      data-test="RF006-salvar-cliente"
      (click)="salvar()"
      [disabled]="!clienteForm.valid"
    >
      Salvar
    </button>
  </div>
</form>
```

---

### 3.8. Checklist de Conformidade

Antes de marcar frontend como concluído, verificar:

- [ ] TODOS os botões de ação possuem data-test no formato `RFXXX-[acao]-[alvo]`
- [ ] TODOS os campos de formulário possuem data-test no formato `RFXXX-input-[campo]`
- [ ] TODAS as mensagens de erro possuem data-test no formato `RFXXX-input-[campo]-error`
- [ ] Container de tabela possui data-test `[entidade]-list`
- [ ] Linhas de tabela possuem data-test `[entidade]-row`
- [ ] Estados de UI (loading, empty, error) possuem data-test sem prefixo RF
- [ ] Dialogs possuem data-test `RFXXX-dialog-[contexto]`
- [ ] Script de auditoria executado: `npm run audit-data-test RFXXX`
- [ ] Exit code da auditoria = 0 (100% cobertura)
- [ ] Nomenclatura é consistente com `UC-RFXXX.yaml`

**SE qualquer item FALHAR:**
- ❌ Frontend REPROVADO
- ❌ Adicionar data-test ausentes
- ❌ Corrigir nomenclatura inconsistente
- ❌ Re-executar auditoria até exit code = 0

---

### 3.9. Referências Relacionadas

| Documento | Seção | Descrição |
|-----------|-------|-----------|
| `CLAUDE.md` | 18 | Alinhamento Obrigatório com Testes |
| `CHECKLIST-IMPLEMENTACAO-E2E.md` | 2.1 | Checklist de Data-test Attributes |
| `frontend.yaml` (validação) | data_test_attributes | Validação de data-test (28 itens) |
| `pre-execucao.yaml` | sincronizacao_mt | Auditoria de data-test obrigatória |
| `UC-TEMPLATE.yaml` | passos.elemento.data_test | Especificação de data-test em UC |
| `MT-TEMPLATE.data.ts` | DATA_TEST_SELECTORS | Centralização de seletores E2E |

---

### 3.10. Padrões de Seletores Angular Material **✨ NOVO**

**Versão:** 1.0
**Data:** 2026-01-10
**Contexto:** Criado após análise do RF006 onde 4 problemas (8%) foram causados por seletores incorretos para componentes Angular Material.

#### Problema Identificado (RF006)

Durante testes E2E, identificamos falhas por uso de seletores CSS genéricos que não funcionam corretamente com Angular Material:

**❌ INCORRETO:**
```typescript
// Tenta clicar no mat-select mas clica no wrapper
await page.click('mat-select');  // FALHA

// Tenta preencher input Material mas pega elemento interno
await page.fill('input', 'valor');  // FALHA intermitente
```

**✅ CORRETO:**
```typescript
// Usa data-test que aponta para o elemento clicável correto
await page.click('[data-test="RF006-select-tipopessoa"]');

// Usa data-test que aponta para o input correto
await page.fill('[data-test="RF006-input-razaosocial"]', 'valor');
```

---

#### 🔴 OBRIGATÓRIO: Seletores para Componentes Material

| Componente Material | Elemento que recebe data-test | Exemplo HTML | Seletor Playwright |
|---------------------|-------------------------------|--------------|-------------------|
| `<mat-form-field>` + `<input>` | `<input matInput>` | `<input matInput data-test="RF006-input-email">` | `[data-test="RF006-input-email"]` |
| `<mat-select>` | `<mat-select>` | `<mat-select data-test="RF006-select-tipo">` | `[data-test="RF006-select-tipo"]` |
| `<mat-option>` (dentro de select) | `<mat-option>` | `<mat-option value="F" data-test="RF006-option-fisica">` | `[data-test="RF006-option-fisica"]` |
| `<mat-checkbox>` | `<mat-checkbox>` | `<mat-checkbox data-test="RF006-checkbox-ativo">` | `[data-test="RF006-checkbox-ativo"]` |
| `<mat-radio-button>` | `<mat-radio-button>` | `<mat-radio-button data-test="RF006-radio-sim">` | `[data-test="RF006-radio-sim"]` |
| `<mat-datepicker>` | `<input matInput>` (trigger) | `<input matInput data-test="RF006-datepicker-inicio">` | `[data-test="RF006-datepicker-inicio"]` |
| `<mat-error>` | `<mat-error>` | `<mat-error data-test="RF006-input-email-error">` | `[data-test="RF006-input-email-error"]` |
| `<button mat-button>` | `<button>` | `<button mat-button data-test="RF006-cancelar">` | `[data-test="RF006-cancelar"]` |
| `<button mat-raised-button>` | `<button>` | `<button mat-raised-button data-test="RF006-salvar">` | `[data-test="RF006-salvar"]` |
| `<button mat-icon-button>` | `<button>` | `<button mat-icon-button data-test="RF006-editar">` | `[data-test="RF006-editar"]` |
| `<mat-dialog-content>` | `<div mat-dialog-content>` | `<div mat-dialog-content data-test="RF006-dialog-confirmar">` | `[data-test="RF006-dialog-confirmar"]` |
| `<mat-spinner>` | Wrapper do spinner | `<div *ngIf="isLoading" data-test="loading-spinner">` | `[data-test="loading-spinner"]` |
| `<mat-progress-bar>` | `<mat-progress-bar>` | `<mat-progress-bar data-test="progress-upload">` | `[data-test="progress-upload"]` |
| `<mat-slide-toggle>` | `<mat-slide-toggle>` | `<mat-slide-toggle data-test="RF006-toggle-notificacoes">` | `[data-test="RF006-toggle-notificacoes"]` |

---

#### Exemplos Corretos por Componente

##### mat-select (Dropdown)

```html
<!-- ✅ CORRETO -->
<mat-form-field>
  <mat-label>Tipo de Pessoa</mat-label>
  <mat-select
    data-test="RF006-select-tipopessoa"
    formControlName="tipoPessoa"
  >
    <mat-option value="F" data-test="RF006-option-fisica">Física</mat-option>
    <mat-option value="J" data-test="RF006-option-juridica">Jurídica</mat-option>
  </mat-select>
  <mat-error data-test="RF006-select-tipopessoa-error">
    {{ getErrorMessage('tipoPessoa') }}
  </mat-error>
</mat-form-field>
```

**Uso no Playwright:**
```typescript
// Abrir o dropdown
await page.click('[data-test="RF006-select-tipopessoa"]');

// Selecionar opção
await page.click('[data-test="RF006-option-juridica"]');

// Verificar erro
await expect(page.locator('[data-test="RF006-select-tipopessoa-error"]'))
  .toBeVisible();
```

---

##### mat-datepicker (Data)

```html
<!-- ✅ CORRETO -->
<mat-form-field>
  <mat-label>Data de Início</mat-label>
  <input
    matInput
    [matDatepicker]="picker"
    data-test="RF006-datepicker-datainicio"
    formControlName="dataInicio"
  />
  <mat-datepicker-toggle matIconSuffix [for]="picker"></mat-datepicker-toggle>
  <mat-datepicker #picker></mat-datepicker>
  <mat-error data-test="RF006-datepicker-datainicio-error">
    {{ getErrorMessage('dataInicio') }}
  </mat-error>
</mat-form-field>
```

**Uso no Playwright:**
```typescript
// Preencher data diretamente
await page.fill('[data-test="RF006-datepicker-datainicio"]', '01/01/2024');

// OU: Clicar no toggle e selecionar data no calendário
await page.click('[data-test="RF006-datepicker-datainicio"]');
// (Material abre o calendário automaticamente)
await page.click('.mat-calendar-body-cell[aria-label="1 janeiro 2024"]');
```

---

##### mat-checkbox (Checkbox)

```html
<!-- ✅ CORRETO -->
<mat-checkbox
  data-test="RF006-checkbox-ativo"
  formControlName="ativo"
>
  Ativo
</mat-checkbox>
```

**Uso no Playwright:**
```typescript
// Marcar checkbox
await page.click('[data-test="RF006-checkbox-ativo"]');

// Verificar estado
const isChecked = await page.locator('[data-test="RF006-checkbox-ativo"]')
  .locator('input[type="checkbox"]').isChecked();
```

---

##### mat-radio-button (Radio)

```html
<!-- ✅ CORRETO -->
<mat-radio-group formControlName="tipoPagamento">
  <mat-radio-button value="PIX" data-test="RF006-radio-pix">
    PIX
  </mat-radio-button>
  <mat-radio-button value="BOLETO" data-test="RF006-radio-boleto">
    Boleto
  </mat-radio-button>
  <mat-radio-button value="CARTAO" data-test="RF006-radio-cartao">
    Cartão
  </mat-radio-button>
</mat-radio-group>
```

**Uso no Playwright:**
```typescript
// Selecionar opção
await page.click('[data-test="RF006-radio-boleto"]');

// Verificar seleção
const isSelected = await page.locator('[data-test="RF006-radio-boleto"]')
  .locator('input[type="radio"]').isChecked();
```

---

##### mat-dialog (Dialog/Modal)

```html
<!-- ✅ CORRETO -->
<h2 mat-dialog-title>Confirmar Exclusão</h2>
<div mat-dialog-content data-test="RF006-dialog-confirmar-exclusao">
  <p>Tem certeza que deseja excluir este cliente?</p>
  <p><strong>{{ cliente.razaoSocial }}</strong></p>
</div>
<div mat-dialog-actions>
  <button
    mat-button
    data-test="RF006-dialog-cancelar"
    (click)="onCancel()"
  >
    Cancelar
  </button>
  <button
    mat-raised-button
    color="warn"
    data-test="RF006-dialog-confirmar"
    (click)="onConfirm()"
  >
    Confirmar
  </button>
</div>
```

**Uso no Playwright:**
```typescript
import { waitForDialogToOpen, dialogFlow } from '../helpers';

// Fluxo completo de dialog
await dialogFlow(
  page,
  'RF006-excluir-cliente',      // botão que abre
  'RF006-dialog-confirmar-exclusao',  // container do dialog
  async (page) => {
    // Ações dentro do dialog
    await page.click('[data-test="RF006-dialog-confirmar"]');
  }
);
```

---

##### mat-spinner (Loading)

```html
<!-- ✅ CORRETO -->
<div *ngIf="isLoading" data-test="loading-spinner" class="loading-container">
  <mat-spinner diameter="50"></mat-spinner>
  <p>Carregando...</p>
</div>
```

**Uso no Playwright:**
```typescript
import { waitForNoBackdrop } from '../helpers';

// Aguardar spinner desaparecer
await page.waitForSelector('[data-test="loading-spinner"]', {
  state: 'detached',
  timeout: 30000
});

// OU: Usar helper específico
await waitForNoBackdrop(page, 30000);
```

---

#### 🔴 PROIBIDO: Seletores CSS Genéricos para Material

**Não use:**
```typescript
// ❌ INCORRETO - seletor CSS genérico não funciona com Material
await page.click('mat-select');           // Clica no wrapper, não no trigger
await page.fill('input', 'valor');        // Pode pegar input interno do Material
await page.click('button');               // Ambíguo, pode clicar no botão errado
await page.click('.mat-raised-button');   // Classe interna do Material, instável
await page.click('mat-option');           // Sem contexto, pode clicar na opção errada
```

**Use data-test:**
```typescript
// ✅ CORRETO - seletor por data-test é estável
await page.click('[data-test="RF006-select-tipopessoa"]');
await page.fill('[data-test="RF006-input-razaosocial"]', 'valor');
await page.click('[data-test="RF006-salvar-cliente"]');
await page.click('[data-test="RF006-option-juridica"]');
```

---

#### Razões para Evitar Seletores CSS Genéricos

1. **Estrutura DOM complexa:** Material envolve elementos em múltiplos wrappers (`mat-form-field`, `mat-select-trigger`, etc.)
2. **Classes CSS dinâmicas:** Classes internas do Material podem mudar entre versões
3. **Shadow DOM (futuro):** Material pode migrar para Shadow DOM, quebrando seletores CSS
4. **Ambiguidade:** Múltiplos `<input>` ou `<button>` na mesma página
5. **Manutenibilidade:** data-test é explícito e rastreável até UC/TC

---

#### Checklist de Conformidade (Material)

Antes de marcar frontend Material como concluído:

- [ ] TODOS os `<mat-select>` possuem data-test
- [ ] TODAS as `<mat-option>` dentro de selects críticos possuem data-test
- [ ] TODOS os `<input matInput>` possuem data-test
- [ ] TODOS os `<mat-checkbox>` possuem data-test
- [ ] TODOS os `<mat-radio-button>` possuem data-test
- [ ] TODOS os `<mat-datepicker>` (input trigger) possuem data-test
- [ ] TODOS os `<mat-error>` possuem data-test
- [ ] TODOS os `<mat-dialog-content>` possuem data-test
- [ ] TODOS os `<mat-spinner>` possuem wrapper com data-test
- [ ] Nenhum teste E2E usa seletores CSS genéricos (`mat-select`, `input`, `button`)
- [ ] Testes E2E usam helpers de dialog (`waitForDialogToOpen`, `dialogFlow`)

**SE qualquer item FALHAR:**
- ❌ Frontend REPROVADO
- ❌ Adicionar data-test ausentes em componentes Material
- ❌ Refatorar testes E2E que usam seletores CSS genéricos

---

#### Referências Relacionadas

| Documento | Seção | Descrição |
|-----------|-------|-----------|
| `D:\IC2\frontend\icontrolit-app\e2e\helpers\dialog-helpers.ts` | `waitForDialogToOpen`, `dialogFlow` | Helpers para dialogs Material |
| `ANALISE-GAPS-GOVERNANCA-RF006-COMPLETA.md` | GAP 4 | Problema de seletores Material (4 problemas, 8%) |
| `frontend-adequacao.md` | FASE 6.5 | Data-test attributes obrigatórios |

---

### 3.11. Changelog

#### v1.1 (2026-01-10)
- Adicionada subseção 3.10 "Padrões de Seletores Angular Material"
- Tabela de referência rápida para 13 componentes Material
- Exemplos corretos e incorretos para cada componente
- Checklist de conformidade específico para Material
- Contexto do RF006: GAP 4 resolvido (4 problemas, 8%)

#### v1.0 (2026-01-09)
- Criação da seção dedicada a nomenclatura de data-test attributes
- Definição de formato padrão obrigatório: `RFXXX-[acao]-[alvo]`
- Exemplos completos para todos os tipos de elementos (botões, campos, tabelas, estados UI)
- Integração com auditoria automática (`npm run audit-data-test`)
- Referências cruzadas com CLAUDE.md seção 18
- Alinhamento com governança de testes (Sprint 5)

---

## 4. Convenções de Camadas

### 4.1 Responsabilidades por Camada

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
| 2. Fornecedor | `FornecedorId` | `Guid?` | ❌ NÃO | Agrupamento lógico | ❌ NÃO |
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
| 1.2 | 2026-01-09 | Arquitetura | Adicionada seção 3 (Nomenclatura de Data-test Attributes - Test-First) - 591 linhas com padrões obrigatórios RFXXX-[acao]-[alvo], exemplos completos para botões/campos/tabelas/estados UI, integração Playwright, checklist conformidade, auditoria automática npm run audit-data-test |
| 1.1 | 2025-12-20 | Arquitetura | Adicionada seção 7.5 (Documentação de RFs) e 7.6 (Relacionamento) |
| 1.0 | 2025-12-20 | Arquitetura | Versão inicial |

---

**Mantido por:** Time de Arquitetura IControlIT  
**Última Revisão:** 2025-12-20  
**Próxima Revisão:** 2026-03-20