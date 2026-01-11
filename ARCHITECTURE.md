# ARCHITECTURE.md

# 🏗️ Arquitetura do Sistema IControlIT

> **Versão:** 4.0  
> **Data:** 2025-12-20  
> **Status:** Em Modernização (ASP.NET Web Forms → .NET 10 + Angular 19)

---

## 📋 Sumário

1. [Visão Geral](#1-visão-geral)
2. [Decisões Arquiteturais](#2-decisões-arquiteturais)
3. [Stack Tecnológica](#3-stack-tecnológica)
4. [Arquitetura de Camadas](#4-arquitetura-de-camadas)
5. [Multi-Tenancy](#5-multi-tenancy)
6. [Modelo de Domínio](#6-modelo-de-domínio)
7. [Padrões de Projeto](#7-padrões-de-projeto)
8. [Segurança e Autorização](#8-segurança-e-autorização)
9. [Integrações](#9-integrações)
10. [Infraestrutura](#10-infraestrutura)
11. [Observabilidade](#11-observabilidade)
12. [Referências](#12-referências)

---

## 1. Visão Geral

### 1.1 Propósito do Sistema

O **IControlIT** é uma plataforma corporativa de gestão de ativos de TI e Telecom, projetada para:

- Gerenciamento completo do ciclo de vida de ativos (notebooks, servidores, impressoras, licenças)
- Gestão de linhas móveis corporativas (Vivo, Claro, TIM, Oi)
- Service Desk integrado com SLA e workflows de aprovação
- Gestão de contratos e faturas com fornecedores
- Rateio de despesas e integração contábil

### 1.2 Contexto de Modernização

| Aspecto | Sistema Legado | Sistema Modernizado |
|---------|----------------|---------------------|
| Backend | ASP.NET Web Forms | .NET 10 + Minimal APIs |
| Frontend | Web Forms + jQuery | Angular 19 Standalone |
| Arquitetura | Monolítica | Clean Architecture + CQRS |
| Banco de Dados | SQL Server (Stored Procedures) | EF Core 10 (Code-First) |
| Autenticação | Forms Authentication | JWT + OAuth 2.0 |

### 1.3 Princípios Arquiteturais

| Princípio | Descrição |
|-----------|-----------|
| **Separação de Responsabilidades** | Clean Architecture com camadas bem definidas |
| **Multi-Tenancy Rigoroso** | Isolamento completo de dados por ClienteId |
| **Auditoria Completa** | Todas as operações são rastreáveis (LGPD, ISO 27001) |
| **API-First** | Backend expõe APIs RESTful consumidas pelo frontend |
| **Internacionalização** | Suporte nativo a múltiplos idiomas (pt-BR, en, es) |

---

## 2. Decisões Arquiteturais

### ADR-001: Clean Architecture

**Contexto:** Necessidade de separar concerns e facilitar testes.

**Decisão:** Adotar Clean Architecture com 4 camadas (Domain, Application, Infrastructure, Web).

**Consequências:**
- (+) Independência de frameworks
- (+) Testabilidade isolada por camada
- (+) Flexibilidade para trocar implementações
- (-) Maior complexidade inicial
- (-) Mais boilerplate code

---

### ADR-002: CQRS com MediatR

**Contexto:** Operações de leitura e escrita têm requisitos distintos.

**Decisão:** Implementar CQRS (Command Query Responsibility Segregation) usando MediatR.

**Consequências:**
- (+) Separação clara entre Commands (write) e Queries (read)
- (+) Pipeline de behaviors reutilizável (validação, logging, autorização)
- (+) Facilita event-driven architecture futura
- (-) Overhead de classes para operações simples

---

### ADR-003: Multi-Tenancy por Row-Level Security

**Contexto:** Múltiplos clientes compartilham a mesma infraestrutura.

**Decisão:** Implementar multi-tenancy em nível único (ClienteId) com Query Filters do EF Core.

**Consequências:**
- (+) Isolamento transparente e automático
- (+) Menor custo operacional (banco único)
- (+) Simplifica migrations
- (-) Risco de vazamento se Query Filter for ignorado
- (-) Performance pode degradar com volume alto

---

### ADR-004: Soft Delete com FlExcluido (Separação Semântica)

**Contexto:** Dados não devem ser permanentemente excluídos por razões legais e de auditoria. Auditoria identificou inconsistência: algumas entidades usavam `Ativo` para soft delete, outras usavam `FlExcluido`, e algumas tinham ambos com semânticas diferentes.

**Decisão:** Padronizar soft delete usando campo `FlExcluido` com semântica negativa:
- `FlExcluido = false` → Registro NÃO deletado (ativo)
- `FlExcluido = true` → Registro deletado (soft delete)
- Campo `Ativo` é OPCIONAL e usado para flag funcional quando necessário (habilitado/desabilitado)

**Consequências:**
- (+) Semântica clara e separada: `Ativo` (funcional) vs `FlExcluido` (soft delete)
- (+) Zero conflitos de nome (entidade `Ativo.cs` pode ter propriedade `FlExcluido`)
- (+) Permite desabilitar temporariamente (`Ativo=false`) sem deletar (`FlExcluido=false`)
- (+) Recuperação de dados deletados
- (+) Conformidade com LGPD (retenção obrigatória de 7 anos)
- (+) Auditoria completa do ciclo de vida
- (-) Semântica negativa menos intuitiva: `WHERE FlExcluido = false` vs `WHERE Ativo = true`
- (-) Crescimento contínuo do banco de dados

---

### ADR-005: Angular Standalone Components

**Contexto:** Modernização do frontend com Angular 19.

**Decisão:** Usar exclusivamente Standalone Components (sem NgModules tradicionais).

**Consequências:**
- (+) Tree-shaking mais eficiente
- (+) Lazy loading granular
- (+) Código mais declarativo
- (-) Migração de código legado mais trabalhosa

---

### ADR-006: Fuse Admin Template

**Contexto:** Necessidade de UI profissional e consistente.

**Decisão:** Adotar Fuse Angular Admin Template como base do frontend.

**Consequências:**
- (+) Componentes prontos e testados
- (+) Design system consistente
- (+) Responsivo out-of-the-box
- (-) Dependência de terceiros
- (-) Customizações podem conflitar com atualizações

---

### ADR-007: SQLite para Desenvolvimento

**Contexto:** Ambiente de desenvolvimento precisa ser leve e portátil.

**Decisão:** SQLite em desenvolvimento, SQL Server em produção.

**Consequências:**
- (+) Setup instantâneo sem instalar SQL Server
- (+) Arquivo único facilita reset
- (-) Algumas features SQL Server não disponíveis
- (-) Necessário validar em SQL Server antes de produção

---

## 3. Stack Tecnológica

### 3.1 Backend

| Componente | Tecnologia | Versão | Justificativa |
|------------|------------|--------|---------------|
| Runtime | .NET | 10.0 | LTS, performance, suporte nativo AOT |
| ORM | Entity Framework Core | 10 | Code-First, migrations, Query Filters |
| CQRS | MediatR | Latest | Desacoplamento, pipeline behaviors |
| Validação | FluentValidation | Latest | Validações expressivas e testáveis |
| Mapeamento | AutoMapper | Latest | Conversão DTO ↔ Entity |
| Jobs | Hangfire | Latest | Background processing, dashboard |
| Cache | Redis | Latest | Cache distribuído, sessões |
| Logging | Serilog | Latest | Structured logging, sinks múltiplos |

### 3.2 Frontend

| Componente | Tecnologia | Versão | Justificativa |
|------------|------------|--------|---------------|
| Framework | Angular | 19 | Standalone Components, Signals |
| UI Kit | Angular Material | Latest | Componentes acessíveis, consistentes |
| Template | Fuse Admin | Latest | Admin dashboard profissional |
| State | Signals | Nativo | Reatividade simplificada (Angular 19+) |
| i18n | Transloco | Latest | Internacionalização flexível |
| HTTP | HttpClient | Nativo | Interceptors, typed responses |
| Forms | Reactive Forms | Nativo | Validação robusta, tipagem |

### 3.3 Banco de Dados

| Ambiente | Tecnologia | Justificativa |
|----------|------------|---------------|
| Desenvolvimento | SQLite | Portabilidade, zero-config |
| Homologação | Azure SQL | Paridade com produção |
| Produção | Azure SQL / SQL Server 2019+ | Performance, recursos enterprise |

### 3.4 Infraestrutura

| Componente | Tecnologia | Justificativa |
|------------|------------|---------------|
| API Gateway | Azure API Management | Rate limiting, subscription keys |
| Hosting Backend | Azure App Service | PaaS gerenciado, scaling |
| Hosting Frontend | Azure Static Web Apps | CDN global, CI/CD integrado |
| Storage | Azure Blob Storage | Documentos, backups, arquivos |
| Secrets | Azure Key Vault | Gerenciamento seguro de secrets |
| CI/CD | Azure DevOps / GitHub Actions | Pipeline automatizado |

---

## 4. Arquitetura de Camadas

### 4.1 Diagrama de Camadas

```
┌─────────────────────────────────────────────────────────────────┐
│                        PRESENTATION                             │
│  ┌─────────────────────┐    ┌─────────────────────────────────┐│
│  │   Angular 19 SPA    │    │      .NET 10 Minimal APIs      ││
│  │  (Fuse Template)    │───▶│      (Web/Endpoints/)          ││
│  └─────────────────────┘    └─────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                        APPLICATION                              │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │    Commands     │  │     Queries     │  │   Behaviours    │ │
│  │   (Write Ops)   │  │   (Read Ops)    │  │ (Pipeline)      │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   Validators    │  │      DTOs       │  │    Mappings     │ │
│  │ (FluentValid)   │  │ (Contracts)     │  │  (AutoMapper)   │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                          DOMAIN                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │    Entities     │  │     Enums       │  │   Constants     │ │
│  │ (Business Core) │  │ (Value Types)   │  │ (Permissions)   │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
│  ┌─────────────────┐  ┌─────────────────┐                      │
│  │  Domain Events  │  │  Interfaces     │                      │
│  │  (Notifications)│  │ (Contracts)     │                      │
│  └─────────────────┘  └─────────────────┘                      │
└─────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                      INFRASTRUCTURE                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   Persistence   │  │    Identity     │  │    External     │ │
│  │  (EF Core)      │  │  (JWT/Auth)     │  │  (Integrations) │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │  Interceptors   │  │    Services     │  │   Migrations    │ │
│  │ (Audit/Tenant)  │  │ (Email/SMS)     │  │  (EF Core)      │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2 Estrutura de Diretórios - Backend

```
D:\IC2\backend\IControlIT.API/src/
│
├── Domain/                          # Núcleo do domínio (zero dependências)
│   ├── Entities/                    # Entidades de negócio
│   ├── Enums/                       # Enumerações tipadas
│   ├── Constants/                   # Permissões, Roles, Policies
│   ├── Events/                      # Domain Events
│   └── Common/                      # Interfaces base, Value Objects
│
├── Application/                     # Casos de uso (depende de Domain)
│   ├── Commands/                    # Operações de escrita
│   │   └── {Entidade}/             # Agrupado por entidade
│   │       ├── Create{Entidade}Command.cs
│   │       ├── Create{Entidade}CommandHandler.cs
│   │       └── Create{Entidade}CommandValidator.cs
│   ├── Queries/                     # Operações de leitura
│   │   └── {Entidade}/
│   ├── DTOs/                        # Data Transfer Objects
│   ├── Mappings/                    # AutoMapper Profiles
│   ├── Behaviours/                  # MediatR Pipeline
│   └── Common/                      # Interfaces, Models compartilhados
│
├── Infrastructure/                  # Implementações (depende de Application)
│   ├── Persistence/
│   │   ├── ApplicationDbContext.cs
│   │   ├── Configurations/          # Fluent API (EF Core)
│   │   └── Interceptors/            # Audit, MultiTenancy, SoftDelete
│   ├── Migrations/
│   ├── Services/                    # Implementações de serviços
│   ├── Identity/                    # JWT, Authorization Handlers
│   └── External/                    # Integrações externas
│
└── Web/                             # Apresentação (depende de todos)
    ├── Endpoints/                   # Minimal APIs agrupados
    ├── Middleware/                  # Exception, Logging, Tenant
    ├── Filters/                     # Action Filters
    └── Program.cs                   # Composition Root
```

### 4.3 Estrutura de Diretórios - Frontend

```
D:\IC2\frontend\icontrolit-app/src/app/
│
├── core/                            # Serviços singleton (providedIn: 'root')
│   ├── auth/                        # AuthService, AuthGuard, AuthInterceptor
│   ├── api/                         # BaseApiService
│   ├── guards/                      # PermissionGuard, ClienteGuard
│   ├── interceptors/                # Error, Loading, SubscriptionKey
│   ├── services/                    # CurrentUser, Notification, Modal
│   └── models/                      # Types compartilhados
│
├── shared/                          # Componentes reutilizáveis
│   ├── components/                  # DataTable, FormField, Dialog
│   ├── directives/                  # PermissionDirective
│   ├── pipes/                       # FormatDate, Currency
│   └── models/                      # Interfaces de domínio
│
├── modules/                         # Feature modules (lazy-loaded)
│   ├── admin/
│   │   ├── management/              # CRUD de entidades
│   │   │   ├── usuarios/
│   │   │   ├── clientes/
│   │   │   ├── empresas/
│   │   │   └── central-modulos/
│   │   └── admin.routes.ts
│   ├── ativos/
│   ├── linhas/
│   ├── chamados/
│   └── financeiro/
│
└── layout/                          # Layouts Fuse
    ├── layouts/                     # Empty, Classic, Modern
    └── common/                      # Navigation, Header, Footer
```

---

## 5. Multi-Tenancy

### 5.1 Modelo de Isolamento - Cliente Único

O IControlIT implementa **multi-tenancy de nível único** com isolamento rigoroso no nível `ClienteId`:

```
┌─────────────────────────────────────────────────────────────────┐
│                   NÍVEL 1: CLIENTE (TENANT ÚNICO)               │
│                      Isolamento OBRIGATÓRIO                     │
│                     (Query Filter automático)                   │
├─────────────────────────────────────────────────────────────────┤
│  Exemplo: "Grupo Chipak Holding"                               │
│  ClienteId: obrigatório em TODAS as entidades                  │
│  Tipo: Guid NOT NULL                                           │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                ESTRUTURA ORGANIZACIONAL                   │  │
│  │              (SEM isolamento de tenant)                   │  │
│  ├──────────────────────────────────────────────────────────┤  │
│  │                                                           │  │
│  │  ┌────────────────────────────────────────────────────┐  │  │
│  │  │       EMPRESA (Unidade Fiscal)                    │  │  │
│  │  │         CNPJ único - Matriz ou Filial             │  │  │
│  │  │      Organização interna do Cliente               │  │  │
│  │  ├────────────────────────────────────────────────────┤  │  │
│  │  │  Exemplo: "Chipak Matriz" (CNPJ 12.345.678/0001)  │  │  │
│  │  │  EmpresaId: opcional (Guid?)                      │  │  │
│  │  │                                                    │  │  │
│  │  │  ┌──────────────────────────────────────────────┐ │  │  │
│  │  │  │   FILIAL (Unidade Operacional)              │ │  │  │
│  │  │  │        Endereço físico de operação          │ │  │  │
│  │  │  ├──────────────────────────────────────────────┤ │  │  │
│  │  │  │  Exemplo: "Filial Porto Alegre"             │ │  │  │
│  │  │  │  FilialId: opcional (Guid?)                 │ │  │  │
│  │  │  │                                              │ │  │  │
│  │  │  │  ┌─────────┐  ┌─────────┐  ┌─────────┐     │ │  │  │
│  │  │  │  │ Ativos  │  │ Linhas  │  │Chamados │     │ │  │  │
│  │  │  │  └─────────┘  └─────────┘  └─────────┘     │ │  │  │
│  │  │  │  ┌─────────┐  ┌─────────┐  ┌─────────┐     │ │  │  │
│  │  │  │  │Consumid.│  │Contrato │  │ Usuários│     │ │  │  │
│  │  │  │  └─────────┘  └─────────┘  └─────────┘     │ │  │  │
│  │  │  └──────────────────────────────────────────────┘ │  │  │
│  │  └────────────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

**Exemplo Real:**
```
Cliente: "Grupo Chipak Holding" (ClienteId: 123e4567-...)
  ├─ Empresa: "Chipak Matriz SP" (CNPJ 12.345.678/0001-90, EmpresaId: aaa11111-...)
  │   ├─ Filial: "Matriz São Paulo - Av. Paulista" (FilialId: bbb22222-...)
  │   └─ Filial: "Centro Distribuição SP - Guarulhos" (FilialId: ccc33333-...)
  └─ Empresa: "Chipak Filial RS" (CNPJ 12.345.678/0002-71, EmpresaId: ddd44444-...)
      └─ Filial: "Filial Porto Alegre - Centro" (FilialId: eee55555-...)
```

### 5.2 Regras de Multi-Tenancy

| Nível | Campo | Obrigatório | Propósito | Query Filter | Tipo |
|-------|-------|-------------|-----------|--------------|------|
| **1. Cliente** | `ClienteId` | ✅ SIM | **Isolamento multi-tenant** | ✅ SIM (automático) | `Guid` NOT NULL |
| **2. Empresa** | `EmpresaId` | ❌ NÃO | Organização fiscal (CNPJ) | ❌ NÃO | `Guid?` NULLABLE |
| **3. Filial** | `FilialId` | ❌ NÃO | Localização física | ❌ NÃO | `Guid?` NULLABLE |

**Regras Críticas:**
1. **ClienteId é OBRIGATÓRIO** em TODAS as entidades multi-tenant
2. **Apenas ClienteId tem Query Filter automático** (isolamento garantido pelo EF Core)
3. **Empresa e Filial são OPCIONAIS** (organização interna do Cliente)
4. **Entidades podem ter escopo específico**: uma entidade pode ser do Cliente (global) ou de uma Empresa específica
5. **UM ÚNICO NÍVEL DE TENANT**: O sistema possui apenas 1 tenant (Cliente), não há sub-tenancy

### 5.3 Implementação

**Interface de Entidade Multi-Tenant:**

```
IMultiTenantEntity
└── ClienteId (Guid)          # Isolamento obrigatório (ÚNICO tenant)
```

**Campos Organizacionais Opcionais (NÃO são tenant):**
- `EmpresaId (Guid?)` - Organização fiscal (CNPJ)
- `FilialId (Guid?)` - Localização física

**Camadas de Validação:**

1. **Middleware:** Extrai `ClienteId` do JWT e injeta no `ICurrentUserService`
2. **Handler:** Valida que `request.ClienteId == currentUser.ClienteId`
3. **Query Filter:** EF Core aplica filtro automático em todas as queries
4. **Interceptor:** Valida `ClienteId` antes de salvar

### 5.4 Tabelas Globais (Sem Multi-Tenancy)

Tabelas de sistema compartilhadas por todos os clientes:

- `SistemaConfiguracao`
- `SistemaParametro`
- `SistemaIdioma`
- `Permission`
- `Role`
- `FeatureFlag` (quando global)

---

## 6. Modelo de Domínio

### 6.1 Entidades Fundamentais

```
┌─────────────────────────────────────────────────────────────────┐
│                    ENTIDADES FUNDACIONAIS                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐    1:N    ┌──────────────┐                   │
│  │   CLIENTE    │──────────▶│   EMPRESA    │                   │
│  │   (Tenant)   │           │   (Fiscal)   │                   │
│  └──────────────┘           └──────────────┘                   │
│         │                                                       │
│         │ 1:N                                                   │
│         ▼                                                       │
│  ┌──────────────┐    N:1    ┌──────────────┐                   │
│  │   USUARIO    │──────────▶│    PERFIL    │                   │
│  │  (Sistema)   │           │    (Role)    │                   │
│  └──────────────┘           └──────────────┘                   │
│                                    │                            │
│                                    │ 1:N                        │
│                                    ▼                            │
│                             ┌──────────────┐                   │
│                             │  PERMISSAO   │                   │
│                             └──────────────┘                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 6.2 Entidades de Negócio

```
┌─────────────────────────────────────────────────────────────────┐
│                    ENTIDADES DE NEGÓCIO                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  PESSOAS                    ATIVOS                              │
│  ┌──────────────┐          ┌──────────────┐                    │
│  │  CONSUMIDOR  │◀────────▶│    ATIVO     │                    │
│  │ (Colaborador)│  aloca   │ (Equipamento)│                    │
│  └──────────────┘          └──────────────┘                    │
│         │                         │                             │
│         │                         │                             │
│         ▼                         ▼                             │
│  ┌──────────────┐          ┌──────────────┐                    │
│  │ DEPARTAMENTO │          │  TIPO_ATIVO  │                    │
│  │    CARGO     │          │    MARCA     │                    │
│  │  HIERARQUIA  │          │   MODELO     │                    │
│  └──────────────┘          └──────────────┘                    │
│                                                                 │
│  TELECOM                    SERVICE DESK                        │
│  ┌──────────────┐          ┌──────────────┐                    │
│  │ LINHA_MOVEL  │          │   CHAMADO    │                    │
│  │   CHIP_SIM   │          │     SLA      │                    │
│  │  OPERADORA   │          │    FILA      │                    │
│  └──────────────┘          └──────────────┘                    │
│                                                                 │
│  FINANCEIRO                 LOCALIZAÇÃO                         │
│  ┌──────────────┐          ┌──────────────┐                    │
│  │   CONTRATO   │          │   ENDERECO   │                    │
│  │    FATURA    │          │   EDIFICIO   │                    │
│  │ FORNECEDOR   │          │  ANDAR/SALA  │                    │
│  └──────────────┘          └──────────────┘                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 6.3 Entidade Base

Todas as entidades de negócio herdam de:

```
BaseAuditableGuidEntity
├── Id (Guid)                 # Identificador único
├── Created (DateTime)        # Data de criação (UTC)
├── CreatedBy (string?)       # Usuário que criou
├── LastModified (DateTime)   # Última modificação (UTC)
├── LastModifiedBy (string?)  # Usuário que modificou
├── DeletedAt (DateTime?)     # Data de exclusão lógica
├── DeletedBy (string?)       # Usuário que excluiu
├── FlExcluido (bool)         # Soft delete: false=ativo, true=excluído
├── IpAddress (string?)       # IP da requisição
└── UserAgent (string?)       # User-Agent do cliente
```

**Convenção de Soft Delete:**
- `FlExcluido = false` → Registro NÃO deletado (padrão)
- `FlExcluido = true` → Registro deletado (soft delete)
- Campo `Ativo` (quando presente) é independente e usado para flag funcional (habilitado/desabilitado)

---

## 7. Padrões de Projeto

### 7.1 CQRS - Fluxo de Request

```
┌──────────┐    HTTP     ┌──────────┐   MediatR   ┌──────────┐
│  Client  │────────────▶│ Endpoint │────────────▶│ Pipeline │
└──────────┘             └──────────┘             └──────────┘
                                                       │
                              ┌─────────────────────────┤
                              ▼                         ▼
                         ┌──────────┐            ┌──────────┐
                         │ Logging  │            │Validation│
                         │Behaviour │            │Behaviour │
                         └──────────┘            └──────────┘
                              │                         │
                              └─────────────┬───────────┘
                                            ▼
                                      ┌──────────┐
                                      │  Auth    │
                                      │Behaviour │
                                      └──────────┘
                                            │
                                            ▼
                                      ┌──────────┐
                                      │ Handler  │
                                      │(Command/ │
                                      │  Query)  │
                                      └──────────┘
                                            │
                                            ▼
                                      ┌──────────┐
                                      │ DbContext│
                                      │  + EF    │
                                      └──────────┘
```

### 7.2 Domain Events

Eventos de domínio para desacoplamento:

| Evento | Trigger | Handlers |
|--------|---------|----------|
| `AtivoAlocadoEvent` | Ativo alocado a consumidor | Email, Auditoria, Dashboard |
| `ChamadoStatusAlteradoEvent` | Status do chamado mudou | Notificação, SLA, Auditoria |
| `ContratoAprovadoEvent` | Contrato aprovado | Workflow, Email, Integração |
| `LinhaPortadaEvent` | Portabilidade concluída | Atualiza status, Notifica |

### 7.3 Workflow de Status

Transições de status são validadas:

```
CHAMADO:
  Aberto ──▶ EmAtendimento ──▶ Resolvido ──▶ Fechado
    │              │              │
    ▼              ▼              ▼
 Cancelado     Aguardando     Reaberto
                   │              │
                   └──────────────┘
```

### 7.4 Approval Workflow

Aprovações multi-nível baseadas em valor:

| Valor do Contrato | Níveis Necessários |
|-------------------|-------------------|
| < R$ 10.000 | 1 (Supervisor) |
| R$ 10.000 - R$ 100.000 | 2 (Supervisor + Gerente) |
| > R$ 100.000 | 3 (Supervisor + Gerente + Diretor) |

---

## 8. Segurança e Autorização

### 8.1 Autenticação

| Aspecto | Implementação |
|---------|---------------|
| Protocolo | JWT Bearer Token |
| Expiração | Access Token: 1 hora |
| Renovação | Refresh Token: 7 dias |
| MFA | Opcional (TOTP) |
| SSO | SAML 2.0, OAuth 2.0 (Azure AD) |

### 8.2 Autorização (RBAC)

**Hierarquia de Perfis:**

```
Super Admin
    │
    ├── Developer
    │
    └── Cliente Admin
            │
            ├── Empresa Admin
            │
            ├── Gestor
            │
            ├── Operador
            │
            └── Consulta
```

**Matriz de Permissões (Exemplo):**

| Permissão | Super Admin | Developer | Cliente Admin | Gestor | Operador | Consulta |
|-----------|:-----------:|:---------:|:-------------:|:------:|:--------:|:--------:|
| CAD.ATIVOS.VIEW | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| CAD.ATIVOS.CREATE | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ |
| CAD.ATIVOS.UPDATE | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ |
| CAD.ATIVOS.DELETE | ✓ | ✓ | ✓ | ✗ | ✗ | ✗ |
| ADM.USUARIOS.* | ✓ | ✓ | ✓ | ✗ | ✗ | ✗ |
| ADM.CLIENTES.* | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ |

### 8.3 Proteção de Dados

| Camada | Controle |
|--------|----------|
| Transporte | TLS 1.3 |
| Repouso | AES-256 (dados sensíveis) |
| Senhas | bcrypt (cost factor 12) |
| API Gateway | Subscription Key obrigatória |

### 8.4 Auditoria

| Aspecto | Implementação |
|---------|---------------|
| Captura | AuditInterceptor (EF Core) |
| Operações | CREATE, UPDATE, DELETE |
| Formato | JSON com before/after |
| Retenção | 7 anos (LGPD) |
| Imutabilidade | Append-only, sem exclusão |

---

## 9. Padrões de UI e Formulários (Angular Material)

**🆕 ADICIONADO:** 2026-01-11 (Resolve problema RF006 - formulários multi-aba)

### 9.1 Formulários Multi-Aba (Angular Material Tabs)

#### Problema Técnico

Angular Material Tabs (`<mat-tab-group>`) usa **lazy loading por padrão**:

- ✅ **Performance:** Abas inativas não são renderizadas no DOM
- ❌ **Testes E2E:** Campos em abas inativas não existem até aba ser clicada
- ❌ **Preenchimento:** `page.fill()` falha em campos não renderizados
- ❌ **Timing:** `page.click('text=Aba')` não garante renderização **imediata**

**Evidência no código:**

```html
<!-- ❌ COMPORTAMENTO PADRÃO (Problemático para testes) -->
<mat-tab-group>
  <mat-tab label="Dados Básicos">
    <input data-test="razaoSocial" />  <!-- ✅ Renderizado -->
  </mat-tab>
  <mat-tab label="Contato">
    <input data-test="email" />  <!-- ❌ NÃO renderizado até clicar -->
  </mat-tab>
</mat-tab-group>
```

#### Solução #1: Desabilitar Lazy Loading (RECOMENDADO)

```html
<!-- ✅ CORRETO: Renderizar todas as abas -->
<mat-tab-group [preserveContent]="true">
  <mat-tab label="Dados Básicos">...</mat-tab>
  <mat-tab label="Contato">...</mat-tab>
  <mat-tab label="Observações">...</mat-tab>
</mat-tab-group>
```

**Vantagens:**
- ✅ Testes E2E acessam todos os campos imediatamente
- ✅ Validação completa de formulário
- ✅ Sem workarounds em testes
- ✅ Código mais simples

**Desvantagens:**
- ⚠️ Performance: todas as abas carregam ao abrir formulário
- ℹ️ Mitigação: usar apenas em formulários pequenos (<10 campos por aba)

**Quando usar:**
- Formulários com até 30 campos totais
- Abas com validação cruzada entre campos
- Formulários testados em E2E

#### Solução #2: Campos Críticos na Primeira Aba

```html
<!-- ✅ CORRETO: Campos obrigatórios/críticos na primeira aba -->
<mat-tab-group>
  <mat-tab label="Dados Básicos">
    <input data-test="razaoSocial" required />
    <input data-test="cnpj" required />
    <input data-test="email" required />  <!-- ✅ Email AQUI -->
  </mat-tab>
  <mat-tab label="Dados Adicionais">
    <input data-test="observacoes" />  <!-- Opcional -->
  </mat-tab>
</mat-tab-group>
```

**Quando usar:**
- Formulários com >30 campos
- Performance é crítica
- Campos opcionais podem ficar em abas secundárias

#### Solução #3: Navegação Programática em Testes (ÚLTIMO RECURSO)

```typescript
// ⚠️ Usar apenas se Solução #1 e #2 não aplicáveis
test('Preencher formulário multi-aba', async ({ page }) => {
  // Aba 1: Dados Básicos (sempre renderizada)
  await page.fill('[data-test~="razaoSocial"]', 'Cliente Teste');

  // Ativar aba 2: Contato
  await page.click('.mat-mdc-tab').filter({ hasText: 'Contato' });
  await page.waitForSelector('[data-test~="email"]', {
    state: 'visible',
    timeout: 5000
  });

  // Preencher campos da aba 2
  await page.fill('[data-test~="email"]', 'teste@exemplo.com');

  // Voltar para aba 1 e salvar
  await page.click('.mat-mdc-tab').filter({ hasText: 'Dados Básicos' });
  await page.click('[data-test~="btn-salvar"]');
});
```

**Quando usar:**
- Formulário é wizard (navegação aba-por-aba obrigatória)
- Formulários muito grandes (>50 campos)
- Performance é crítica E campos não são obrigatórios

#### Regra de Decisão Arquitetural

```yaml
Se formulário tem abas E campos são validados em testes E2E:
  Então: Usar [preserveContent]="true"  # ✅ Solução #1

Se formulário tem >30 campos E performance é crítica:
  Então: Campos obrigatórios/críticos na primeira aba  # ✅ Solução #2

Se formulário é wizard (aba-por-aba obrigatório):
  Então: Navegação programática em testes  # ⚠️ Solução #3
```

#### Validação Obrigatória (Checklist)

- [ ] Todos os `mat-tab-group` com campos críticos usam `[preserveContent]="true"`
- [ ] **OU**: Campos obrigatórios estão na primeira aba
- [ ] Testes E2E validam **TODOS** os campos do formulário
- [ ] Sem TODOs sobre "aba não renderiza" em testes
- [ ] Performance validada (formulário abre em <1s mesmo com `[preserveContent]="true"`)

#### Exemplo Aplicado: RF006 (Cliente)

**Arquivo:** `D:\IC2\frontend\icontrolit-app\src\app\modules\admin\management\clientes\details\details.component.html`

**Alteração:**

```html
<!-- ANTES -->
<mat-tab-group>
  <mat-tab label="Dados Básicos">...</mat-tab>
  <mat-tab label="Contato">...</mat-tab>
</mat-tab-group>

<!-- DEPOIS -->
<mat-tab-group [preserveContent]="true">
  <mat-tab label="Dados Básicos">...</mat-tab>
  <mat-tab label="Contato">...</mat-tab>
</mat-tab-group>
```

**Justificativa:**
- Formulário Cliente tem apenas 7 campos
- Performance **NÃO** é impactada com 7 campos
- Resolve problema de testes E2E **imediatamente**

---

## 10. Integrações

### 10.1 Visão Geral

```
┌─────────────────────────────────────────────────────────────────┐
│                        ICONTROLIT                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │   REST   │  │   SOAP   │  │   FTP    │  │   LDAP   │       │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘       │
│       │             │             │             │              │
└───────┼─────────────┼─────────────┼─────────────┼──────────────┘
        │             │             │             │
        ▼             ▼             ▼             ▼
┌──────────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐
│  Operadoras  │ │   ERPs   │ │  Faturas │ │  Azure AD /  │
│ Vivo, Claro, │ │ SAP,     │ │  (PDF,   │ │  Active      │
│ TIM, Oi      │ │ TOTVS    │ │  XML)    │ │  Directory   │
└──────────────┘ └──────────┘ └──────────┘ └──────────────┘
```

### 10.2 Integrações Principais

| Sistema | Protocolo | Autenticação | Frequência |
|---------|-----------|--------------|------------|
| Vivo | REST API | OAuth 2.0 | Diário (consumo), Mensal (fatura) |
| Claro | REST + SOAP | API Key | Diário |
| TIM | REST API | Bearer JWT | Diário |
| SAP | RFC/BAPI | NTLM | Diário (colaboradores) |
| Azure AD | LDAP/OAuth | OAuth 2.0 | 4 horas |
| ViaCEP | REST API | Nenhuma | On-demand |
| SendGrid | REST API | API Key | On-demand |

### 10.3 Padrões de Resiliência

| Padrão | Configuração |
|--------|--------------|
| Circuit Breaker | 5 falhas → 2 min aberto |
| Retry | 3 tentativas (1s, 2s, 4s exponential) |
| Timeout | 30s request, 10s connection |
| Rate Limit | Conforme limite da API externa |

### 9.4 Jobs de Sincronização (Hangfire)

| Job | Schedule | Descrição |
|-----|----------|-----------|
| SincronizarConsumoOperadoras | 02:00 diário | Importa consumo de voz/dados |
| SincronizarColaboradoresERP | 06:00 diário | Sincroniza colaboradores do SAP |
| SincronizarUsuariosAD | */4h | Sincroniza usuários do AD |
| ProcessarFaturas | Dia 5 mensal | Importa e processa faturas |
| CalcularDepreciacao | Dia 1 mensal | Recalcula depreciação de ativos |

---

## 10. Infraestrutura

### 10.1 Ambientes

| Ambiente | Backend | Frontend | Banco |
|----------|---------|----------|-------|
| Local | localhost:5000 | localhost:4200 | SQLite |
| Desenvolvimento | dev-api.icontrolit.com | dev.icontrolit.com | Azure SQL (Dev) |
| Homologação | hml-api.icontrolit.com | hml.icontrolit.com | Azure SQL (Hml) |
| Produção | api.icontrolit.com | app.icontrolit.com | Azure SQL (Prod) |

### 10.2 Diagrama de Infraestrutura (Azure)

```
┌─────────────────────────────────────────────────────────────────┐
│                         INTERNET                                │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
                  ┌──────────────────┐
                  │  Azure Front     │
                  │  Door / CDN      │
                  └────────┬─────────┘
                           │
         ┌─────────────────┼─────────────────┐
         │                 │                 │
         ▼                 ▼                 ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ Static Web   │  │   API        │  │   API        │
│ App (SPA)    │  │  Management  │  │  Management  │
│   Angular    │  │   Gateway    │  │   Gateway    │
└──────────────┘  └──────┬───────┘  └──────┬───────┘
                         │                 │
                         ▼                 ▼
                  ┌──────────────┐  ┌──────────────┐
                  │  App Service │  │  App Service │
                  │  (Backend)   │  │  (Backend)   │
                  │   Primary    │  │   Secondary  │
                  └──────┬───────┘  └──────┬───────┘
                         │                 │
         ┌───────────────┼─────────────────┼───────────────┐
         │               │                 │               │
         ▼               ▼                 ▼               ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│  Azure SQL   │ │    Redis     │ │    Blob      │ │  Key Vault   │
│  (Primary)   │ │    Cache     │ │   Storage    │ │  (Secrets)   │
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘
```

### 10.3 Requisitos de Escalabilidade

| Métrica | Requisito | Estratégia |
|---------|-----------|------------|
| Usuários Concorrentes | 500+ | Auto-scale horizontal |
| Requests/segundo | 1000+ | Load balancing |
| Tempo de Resposta | < 500ms (P95) | Caching, índices |
| Disponibilidade | 99.9% | Multi-region, failover |

---

## 11. Observabilidade

### 11.1 Logging

| Componente | Ferramenta | Nível |
|------------|------------|-------|
| Structured Logs | Serilog | Info+ (Prod), Debug (Dev) |
| Sink Primário | Azure Application Insights | Todos |
| Sink Secundário | Elasticsearch (opcional) | Todos |
| Correlação | CorrelationId em headers | Trace completo |

### 11.2 Métricas

| Métrica | Fonte | Alerta |
|---------|-------|--------|
| Response Time | Application Insights | > 2s (P95) |
| Error Rate | Application Insights | > 1% |
| CPU/Memory | Azure Monitor | > 80% |
| Queue Length | Hangfire Dashboard | > 100 |

### 11.3 Health Checks

| Endpoint | Verifica |
|----------|----------|
| `/health` | API disponível |
| `/health/ready` | DB, Redis, dependências |
| `/health/live` | Aplicação respondendo |

---

## 12. Referências

### 12.1 Documentação Interna

| Documento | Localização |
|-----------|-------------|
| Modelo Físico BD | `D:\DocumentosIC2\modelo-fisico-bd.sql` |
| Prompts de IA | `inteligencia-artificial/prompts/` |
| Requisitos Funcionais | `documentacao/requisitos/` |

### 12.2 Documentação Externa

| Recurso | URL |
|---------|-----|
| .NET 10 | https://learn.microsoft.com/en-us/dotnet/ |
| Angular 19 | https://angular.dev/ |
| Fuse Template | https://angular-material.fusetheme.com/ |
| MediatR | https://github.com/jbogard/MediatR |
| FluentValidation | https://docs.fluentvalidation.net/ |
| Transloco | https://ngneat.github.io/transloco/ |

---

## Changelog

### v4.0 (2025-12-20)
- Reestruturação completa do documento para formato ARCHITECTURE.md
- Adição de ADRs (Architecture Decision Records)
- Detalhamento de stack tecnológica
- Diagramas de arquitetura atualizados
- Seção de observabilidade adicionada

### v3.0 (2025-12-18)
- Modelo de domínio completo
- Padrões de projeto detalhados
- Framework de integrações

### v2.0 (2025-12-18)
- Documentação inicial da modernização
- Multi-tenancy documentado

---

**Mantido por:** Time de Arquitetura IControlIT  
**Última Revisão:** 2025-12-20