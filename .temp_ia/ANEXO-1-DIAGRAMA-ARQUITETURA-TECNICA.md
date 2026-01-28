# ANEXO 1 - Diagrama de Arquitetura Técnica

**Projeto:** IControlIT - Refatoração
**Data:** 2026-01-14
**Versão:** 1.0

---

## 1. Arquitetura Clean Architecture + CQRS

```mermaid
graph TB
    subgraph "Camada de Apresentação"
        A[Angular 19 SPA]
        A1[Fuse Admin Template]
        A2[Material Design]
        A3[Transloco i18n]
    end

    subgraph "Camada de API"
        B[ASP.NET Core Web API]
        B1[JWT Authentication]
        B2[Authorization Policies]
        B3[Middleware Pipeline]
    end

    subgraph "Camada de Aplicação"
        C[Application Layer]
        C1[Commands CQRS]
        C2[Queries CQRS]
        C3[MediatR Handler]
        C4[FluentValidation]
        C5[AutoMapper DTOs]
    end

    subgraph "Camada de Domínio"
        D[Domain Layer]
        D1[Entities]
        D2[Value Objects]
        D3[Domain Events]
        D4[Business Rules]
        D5[Aggregate Roots]
    end

    subgraph "Camada de Infraestrutura"
        E[Infrastructure Layer]
        E1[EF Core + SQL Server]
        E2[Azure Blob Storage]
        E3[ReceitaWS API]
        E4[Email Service]
        E5[Repository Pattern]
        E6[Query Filters Multi-Tenancy]
    end

    subgraph "Serviços Externos"
        F1[ReceitaWS API]
        F2[Azure Blob]
        F3[SMTP Server]
        F4[ERP Integrações]
    end

    A --> B
    A1 --> A
    A2 --> A
    A3 --> A

    B --> C
    B1 --> B
    B2 --> B
    B3 --> B

    C --> D
    C1 --> C3
    C2 --> C3
    C4 --> C
    C5 --> C

    D --> E
    D1 --> D5
    D2 --> D5
    D3 --> D
    D4 --> D

    E --> F1
    E --> F2
    E --> F3
    E --> F4
    E1 --> E5
    E6 --> E1

    style A fill:#4CAF50
    style B fill:#2196F3
    style C fill:#FF9800
    style D fill:#F44336
    style E fill:#9C27B0
```

---

## 2. Fluxo CQRS (Commands e Queries)

```mermaid
sequenceDiagram
    participant U as Usuário Frontend
    participant API as Web API
    participant M as MediatR
    participant CH as Command Handler
    participant QH as Query Handler
    participant D as Domain
    participant DB as Database

    Note over U,DB: Fluxo de Comando (Write)
    U->>API: POST /api/clientes (CreateClienteCommand)
    API->>M: Send(CreateClienteCommand)
    M->>CH: Handle(CreateClienteCommand)
    CH->>D: Create Cliente Entity
    D->>D: Validate Business Rules
    D->>D: Raise Domain Events
    CH->>DB: SaveChangesAsync()
    DB-->>CH: Success
    CH-->>M: ClienteDto
    M-->>API: ClienteDto
    API-->>U: 201 Created + ClienteDto

    Note over U,DB: Fluxo de Query (Read)
    U->>API: GET /api/clientes (GetClientesQuery)
    API->>M: Send(GetClientesQuery)
    M->>QH: Handle(GetClientesQuery)
    QH->>DB: AsNoTracking().Where(...).ToListAsync()
    DB-->>QH: List<Cliente>
    QH->>QH: AutoMapper → DTOs
    QH-->>M: List<ClienteDto>
    M-->>API: List<ClienteDto>
    API-->>U: 200 OK + List<ClienteDto>
```

---

## 3. Multi-Tenancy - Row-Level Security

```mermaid
graph LR
    subgraph "Usuário Cliente A"
        U1[Login Cliente A]
        U1 --> T1[ClienteId = A]
    end

    subgraph "Usuário Cliente B"
        U2[Login Cliente B]
        U2 --> T2[ClienteId = B]
    end

    subgraph "Super Admin K2A"
        U3[Login K2A]
        U3 --> T3[IsSuperAdmin = true]
    end

    subgraph "EF Core Query Filters"
        QF[Query Filter Global]
        QF --> QF1{IsSuperAdmin?}
        QF1 -->|Sim| QF2[Bypass Filter]
        QF1 -->|Não| QF3[WHERE ClienteId = CurrentUser.ClienteId]
    end

    subgraph "Database - SQL Server"
        DB[(Database Único)]
        DB --> TB1[Tabela Clientes]
        DB --> TB2[Tabela Usuários]
        DB --> TB3[Tabela Contratos]
        DB --> TB4[Tabela Faturas]

        TB2 --> |ClienteId = A| ROWS_A[Registros Cliente A]
        TB2 --> |ClienteId = B| ROWS_B[Registros Cliente B]
        TB3 --> |ClienteId = A| ROWS_A
        TB3 --> |ClienteId = B| ROWS_B
        TB4 --> |ClienteId = A| ROWS_A
        TB4 --> |ClienteId = B| ROWS_B
    end

    T1 --> QF
    T2 --> QF
    T3 --> QF

    QF2 --> DB
    QF3 --> DB

    style U1 fill:#4CAF50
    style U2 fill:#2196F3
    style U3 fill:#FF9800
    style QF fill:#F44336
    style DB fill:#9C27B0
```

**Explicação:**
- **1 banco de dados** substituiu **18 bancos físicos** do legado
- **Isolamento lógico** via `ClienteId` em todas as tabelas
- **EF Core Query Filters** aplicam `WHERE ClienteId = X` automaticamente
- **Super Admin K2A** tem bypass (`IsSuperAdmin = true`)
- **Cliente A NÃO vê dados do Cliente B** (isolamento 100%)

---

## 4. RBAC - Sistema de Permissões

```mermaid
graph TD
    subgraph "Usuário"
        U[Usuário: joao@clienteA.com]
        U --> UP[PerfilId: GERENTE]
    end

    subgraph "Perfil de Acesso"
        P[Perfil: GERENTE]
        P --> PP1[Permissão: CAD.CLIENTES.VISUALIZAR]
        P --> PP2[Permissão: FIN.CONTRATOS.GERENCIAR]
        P --> PP3[Permissão: FIN.FATURAS.VISUALIZAR]
    end

    subgraph "Central de Funcionalidades"
        CF[Central de Funcionalidades]
        CF --> CF1[Módulo: Cadastros - ATIVO]
        CF --> CF2[Módulo: Financeiro - ATIVO]
        CF --> CF3[Módulo: Service Desk - INATIVO]
    end

    subgraph "Autorização em Runtime"
        AUTH{Autorizar Ação?}
        AUTH --> AUTH1{Usuário tem Permissão?}
        AUTH1 -->|Sim| AUTH2{Módulo está ATIVO?}
        AUTH1 -->|Não| DENY[403 Forbidden]
        AUTH2 -->|Sim| ALLOW[200 OK]
        AUTH2 -->|Não| DENY
    end

    U --> AUTH
    P --> AUTH1
    CF --> AUTH2

    style U fill:#4CAF50
    style P fill:#2196F3
    style CF fill:#FF9800
    style AUTH fill:#F44336
    style ALLOW fill:#4CAF50
    style DENY fill:#F44336
```

**Fluxo de Autorização:**
1. Usuário tenta acessar `/api/contratos` (GET)
2. Sistema verifica se usuário tem permissão `FIN.CONTRATOS.VISUALIZAR`
3. Sistema verifica se módulo "Financeiro" está ATIVO para o cliente
4. Se ambos OK → 200 OK, senão → 403 Forbidden

---

## 5. Stack Tecnológica Completa

```mermaid
graph TB
    subgraph "Frontend"
        FE1[Angular 19 Standalone]
        FE2[TypeScript 5.0]
        FE3[RxJS 7.8]
        FE4[Fuse Admin Template]
        FE5[Material Design]
        FE6[Transloco i18n]
        FE7[ngx-image-cropper]
        FE8[Playwright E2E]
    end

    subgraph "Backend"
        BE1[.NET 10]
        BE2[ASP.NET Core Web API]
        BE3[EF Core 10]
        BE4[MediatR 12]
        BE5[FluentValidation 11]
        BE6[AutoMapper 13]
        BE7[Serilog]
        BE8[xUnit + NSubstitute]
    end

    subgraph "Database"
        DB1[SQL Server 2022]
        DB2[Azure Blob Storage]
        DB3[Redis Cache planejado]
    end

    subgraph "Integrações"
        INT1[ReceitaWS API]
        INT2[Azure Services]
        INT3[SMTP Email]
        INT4[ERP SAP/TOTVS planejado]
        INT5[PowerBI planejado]
    end

    subgraph "DevOps"
        DO1[Git + GitHub]
        DO2[Azure DevOps]
        DO3[Docker + Testcontainers]
        DO4[CI/CD Pipelines planejado]
    end

    FE1 --> BE2
    BE2 --> DB1
    BE3 --> DB1
    BE2 --> DB2
    BE2 --> INT1
    BE2 --> INT2
    BE2 --> INT3

    style FE1 fill:#4CAF50
    style BE1 fill:#2196F3
    style DB1 fill:#FF9800
    style INT1 fill:#9C27B0
    style DO1 fill:#F44336
```

---

## 6. Benefícios da Arquitetura

### **vs. Sistema Legado:**

| Aspecto | Legado | Novo Sistema |
|---------|--------|--------------|
| **Arquitetura** | Monolítica | Clean Architecture + CQRS |
| **Bancos de Dados** | 18 físicos | 1 lógico (Row-Level Security) |
| **Multi-Tenancy** | Separação física | Isolamento lógico (EF Core) |
| **RBAC** | Permissões hardcoded | RBAC granular + Central Funcionalidades |
| **i18n** | Não suportado | pt-BR, en-US, es-ES (Transloco) |
| **API Externa** | Nenhuma | ReceitaWS, Azure Blob |
| **Testes** | Manuais | Unitários + E2E (Playwright) |
| **Auditoria** | Logs simples | Domain Events + LGPD (7 anos) |
| **Onboarding Cliente** | 3-5 dias (manual DBA) | < 5 minutos (API) |

---

## 7. Segurança em Camadas

```mermaid
graph TD
    subgraph "Camadas de Segurança"
        S1[1. HTTPS TLS 1.3]
        S2[2. JWT Access Token 15min]
        S3[3. JWT Refresh Token 7 dias]
        S4[4. RBAC Permissões Granulares]
        S5[5. Multi-Tenancy Query Filters]
        S6[6. FluentValidation Input]
        S7[7. SQL Injection Protection EF Core]
        S8[8. CORS Policies]
        S9[9. Rate Limiting planejado]
        S10[10. Domain Events Auditoria]
    end

    S1 --> S2
    S2 --> S3
    S3 --> S4
    S4 --> S5
    S5 --> S6
    S6 --> S7
    S7 --> S8
    S8 --> S9
    S9 --> S10

    style S1 fill:#4CAF50
    style S5 fill:#F44336
    style S10 fill:#2196F3
```

---

## 8. Padrões de Projeto Implementados

- ✅ **Clean Architecture** (separação de responsabilidades)
- ✅ **CQRS** (Commands vs. Queries)
- ✅ **Domain-Driven Design** (Entities, Value Objects, Aggregates)
- ✅ **Repository Pattern** (abstração de acesso a dados)
- ✅ **Dependency Injection** (IoC Container)
- ✅ **Mediator Pattern** (MediatR)
- ✅ **Event Sourcing** (Domain Events)
- ✅ **Unit of Work** (DbContext SaveChanges)
- ✅ **Specification Pattern** (Query Filters)
- ✅ **DTO Pattern** (AutoMapper)

---

**Conclusão:**

A arquitetura implementada é **moderna, escalável, segura e testável**. Substitui um sistema monolítico legado por uma solução baseada em padrões de mercado (Clean Architecture, CQRS, DDD) com isolamento multi-tenancy robusto e RBAC granular.

**Tempo de implementação:** 3 meses (Fases 1-2)
**Status:** ✅ Fundação técnica completa e validada
