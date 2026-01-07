# Modelo de Dados - RF012

**Versao:** 1.0
**Data:** 2025-12-27
**RF Relacionado:** [RF012 - Gestao de Usuarios](./RF012.md)
**Banco de Dados:** SQL Server (Compativel com PostgreSQL)

---

## 1. Diagrama de Entidades

```
┌─────────────────────────┐       ┌─────────────────────────┐
│      Cliente            │       │       Empresa           │
├─────────────────────────┤       ├─────────────────────────┤
│ Id (PK)                 │──┐    │ Id (PK)                 │──┐
│ Nome                    │  │    │ ClienteId (FK)          │  │
│ CNPJ                    │  │    │ Nome                    │  │
│ Ativo                   │  │    │ Ativo                   │  │
│ ...                     │  │    │ ...                     │  │
└─────────────────────────┘  │    └─────────────────────────┘  │
                             │                                 │
                             │                                 │
              ┌──────────────┴──────────────┬──────────────────┘
              │                             │
              v                             v
┌─────────────────────────┐       ┌─────────────────────────┐
│       Usuario           │       │     UsuarioRole         │
├─────────────────────────┤       ├─────────────────────────┤
│ Id (PK)                 │<──┐   │ Id (PK)                 │
│ ClienteId (FK)          │   │   │ UsuarioId (FK)          │───┐
│ EmpresaId (FK)          │   │   │ RoleId (FK)             │   │
│ Nome                    │   │   │ ...                     │   │
│ Email                   │   │   └─────────────────────────┘   │
│ PasswordHash            │   │                                 │
│ MFAHabilitado           │   │   ┌─────────────────────────┐   │
│ Ativo                   │   │   │    Role                 │   │
│ Bloqueado               │   │   ├─────────────────────────┤   │
│ TentativasFalhas        │   │   │ Id (PK)                 │<──┘
│ DataExpiracaoSenha      │   │   │ Name                    │
│ ADObjectGUID            │   │   │ NormalizedName          │
│ ...                     │   │   │ ...                     │
│ Created (Auditoria)     │   │   └─────────────────────────┘
│ CreatedBy (FK Usuario)  │───┘
│ LastModified            │       ┌─────────────────────────┐
│ LastModifiedBy (FK)     │───────│ HistoricoSenhaUsuario   │
│ FlExcluido (Soft Delete)│       ├─────────────────────────┤
└─────────────────────────┘       │ Id (PK)                 │
                                  │ UsuarioId (FK)          │───┐
                                  │ PasswordHash            │   │
                                  │ DataCriacao             │   │
                                  └─────────────────────────┘   │
                                                                │
                                                                │
                                  ┌─────────────────────────┐   │
                                  │ SolicitacaoFilaAtend.   │   │
                                  ├─────────────────────────┤   │
                                  │ Id (PK)                 │   │
                                  │ UsuarioId (FK)          │───┘
                                  │ FilaId (FK)             │
                                  │ ...                     │
                                  └─────────────────────────┘
```

---

## 2. Entidades

### 2.1 Tabela: Usuario

**Descricao:** Armazena informacoes de usuarios do sistema IControlIT. Gerencia autenticacao, autorizacao, multi-tenancy, MFA e integracao com Active Directory. Implementa auditoria completa com BaseAuditableGuidEntity e soft delete para conformidade LGPD.

#### Campos

| Campo | Tipo | Nulo | Default | Descricao |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NAO | NEWID() | Chave primaria (GUID) |
| ClienteId | UNIQUEIDENTIFIER | NAO | - | FK para Cliente (TENANT RAIZ - multi-tenancy obrigatorio) |
| EmpresaId | UNIQUEIDENTIFIER | SIM | NULL | FK para Empresa (tenant especifico - opcional para SuperAdmin) |
| Nome | NVARCHAR(200) | NAO | - | Nome completo do usuario |
| Email | NVARCHAR(200) | NAO | - | Email do usuario (usado para login e recuperacao de senha) |
| Telefone | NVARCHAR(20) | SIM | NULL | Telefone do usuario |
| CPF | VARCHAR(14) | SIM | NULL | CPF do usuario (formato: XXX.XXX.XXX-XX) |
| DataNascimento | DATE | SIM | NULL | Data de nascimento |
| Avatar | NVARCHAR(500) | SIM | NULL | URL ou caminho do avatar do usuario |
| PasswordHash | NVARCHAR(MAX) | NAO | - | Hash da senha (bcrypt) |
| DataUltimoAcesso | DATETIME2 | SIM | NULL | Data/hora do ultimo acesso ao sistema |
| DataExpiracaoSenha | DATETIME2 | SIM | NULL | Data de expiracao da senha (90 dias apos criacao/alteracao) |
| TentativasFalhas | INT | NAO | 0 | Contador de tentativas falhas de login consecutivas |
| Bloqueado | BIT | NAO | 0 | Indica se usuario esta bloqueado (1=bloqueado, 0=ativo) |
| DataBloqueio | DATETIME2 | SIM | NULL | Data/hora do bloqueio |
| MFAHabilitado | BIT | NAO | 0 | Indica se MFA (autenticacao de dois fatores) esta habilitado |
| MFASecret | NVARCHAR(500) | SIM | NULL | Secret do MFA (TOTP) criptografado |
| TelefoneMFA | NVARCHAR(20) | SIM | NULL | Telefone para MFA via SMS |
| UsuarioAD | BIT | NAO | 0 | Indica se usuario e sincronizado com Active Directory |
| ADObjectGUID | UNIQUEIDENTIFIER | SIM | NULL | GUID do objeto no Active Directory |
| ADSamAccountName | NVARCHAR(256) | SIM | NULL | SamAccountName do AD |
| ADDistinguishedName | NVARCHAR(500) | SIM | NULL | Distinguished Name do AD |
| DataUltimaSincronizacaoAD | DATETIME2 | SIM | NULL | Data/hora da ultima sincronizacao com AD |
| Idioma | VARCHAR(10) | NAO | 'pt-BR' | Idioma preferido (pt-BR, en-US, es-ES) |
| Timezone | VARCHAR(100) | NAO | 'America/Sao_Paulo' | Timezone do usuario (TZ database name) |
| Tema | VARCHAR(20) | NAO | 'light' | Tema da interface (light, dark) |
| Ativo | BIT | NAO | 1 | Status ativo/inativo do usuario (1=ativo, 0=inativo) |
| FlExcluido | BIT | NAO | 0 | Soft delete (0=nao deletado, 1=deletado) |
| MustChangePassword | BIT | NAO | 0 | Indica se usuario deve alterar senha no proximo login |
| DataDesativacao | DATETIME2 | SIM | NULL | Data de desativacao do usuario |
| DesativadoPorId | UNIQUEIDENTIFIER | SIM | NULL | FK Usuario que desativou |
| MotivoDesativacao | NVARCHAR(500) | SIM | NULL | Motivo da desativacao |
| Anonimizado | BIT | NAO | 0 | Indica se usuario foi anonimizado (LGPD) |
| DataAnonimizacao | DATETIME2 | SIM | NULL | Data de anonimizacao (LGPD) |
| AnonimizadoPorId | UNIQUEIDENTIFIER | SIM | NULL | FK Usuario que anonimizou |
| Created | DATETIME2 | NAO | GETDATE() | Data de criacao (BaseAuditableGuidEntity) |
| CreatedBy | UNIQUEIDENTIFIER | SIM | NULL | FK Usuario que criou (auditoria) |
| LastModified | DATETIME2 | SIM | NULL | Data da ultima modificacao (BaseAuditableGuidEntity) |
| LastModifiedBy | UNIQUEIDENTIFIER | SIM | NULL | FK Usuario que modificou (auditoria) |

#### Indices

| Nome | Colunas | Tipo | Descricao |
|------|---------|------|-----------|
| PK_Usuario | Id | CLUSTERED | Chave primaria (GUID) |
| IX_Usuario_ClienteId | ClienteId | NONCLUSTERED | Performance multi-tenant (filtro obrigatorio) |
| IX_Usuario_EmpresaId | EmpresaId | NONCLUSTERED | Performance filtro por empresa |
| IX_Usuario_Email_ClienteId | Email, ClienteId | UNIQUE NONCLUSTERED | Garantir email unico por cliente (tenant) |
| IX_Usuario_CPF_ClienteId | CPF, ClienteId | NONCLUSTERED | Busca por CPF dentro do tenant |
| IX_Usuario_ADObjectGUID | ADObjectGUID | NONCLUSTERED | Performance sincronizacao AD |
| IX_Usuario_Ativo | Ativo | NONCLUSTERED | Filtro usuarios ativos |
| IX_Usuario_FlExcluido | FlExcluido | NONCLUSTERED | Filtro soft delete |
| IX_Usuario_Created | Created | NONCLUSTERED | Performance ordenacao temporal |

#### Constraints

| Nome | Tipo | Definicao | Descricao |
|------|------|-----------|-----------|
| PK_Usuario | PRIMARY KEY | Id | Chave primaria |
| FK_Usuario_Cliente | FOREIGN KEY | ClienteId REFERENCES Cliente(Id) | Multi-tenancy obrigatorio |
| FK_Usuario_Empresa | FOREIGN KEY | EmpresaId REFERENCES Empresa(Id) | Empresa especifica (opcional) |
| FK_Usuario_CreatedBy | FOREIGN KEY | CreatedBy REFERENCES Usuario(Id) | Auditoria (usuario criador) |
| FK_Usuario_LastModifiedBy | FOREIGN KEY | LastModifiedBy REFERENCES Usuario(Id) | Auditoria (usuario modificador) |
| FK_Usuario_DesativadoPor | FOREIGN KEY | DesativadoPorId REFERENCES Usuario(Id) | Usuario que desativou |
| FK_Usuario_AnonimizadoPor | FOREIGN KEY | AnonimizadoPorId REFERENCES Usuario(Id) | Usuario que anonimizou (LGPD) |
| UQ_Usuario_Email_Cliente | UNIQUE | (Email, ClienteId) | Email unico por cliente (tenant) |
| UQ_Usuario_ADObjectGUID | UNIQUE | ADObjectGUID | ObjectGUID do AD unico (quando nao NULL) |
| CHK_Usuario_TentativasFalhas | CHECK | TentativasFalhas >= 0 | Tentativas nao pode ser negativo |
| CHK_Usuario_Email_Format | CHECK | Email LIKE '%@%' | Formato basico de email |
| CHK_Usuario_Idioma | CHECK | Idioma IN ('pt-BR', 'en-US', 'es-ES') | Idiomas permitidos |

---

### 2.2 Tabela: HistoricoSenhaUsuario

**Descricao:** Armazena historico de senhas dos ultimos 12 meses para impedir reutilizacao de senhas (politica de seguranca). Implementa retencao automatica de 12 meses.

#### Campos

| Campo | Tipo | Nulo | Default | Descricao |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NAO | NEWID() | Chave primaria |
| UsuarioId | UNIQUEIDENTIFIER | NAO | - | FK para Usuario |
| PasswordHash | NVARCHAR(MAX) | NAO | - | Hash da senha antiga (bcrypt) |
| DataCriacao | DATETIME2 | NAO | GETDATE() | Data/hora de criacao do registro |

#### Indices

| Nome | Colunas | Tipo | Descricao |
|------|---------|------|-----------|
| PK_HistoricoSenhaUsuario | Id | CLUSTERED | Chave primaria |
| IX_HistoricoSenha_UsuarioId | UsuarioId | NONCLUSTERED | Performance busca por usuario |
| IX_HistoricoSenha_DataCriacao | DataCriacao | NONCLUSTERED | Performance cleanup automatico |

#### Constraints

| Nome | Tipo | Definicao | Descricao |
|------|------|-----------|-----------|
| PK_HistoricoSenhaUsuario | PRIMARY KEY | Id | Chave primaria |
| FK_HistoricoSenha_Usuario | FOREIGN KEY | UsuarioId REFERENCES Usuario(Id) ON DELETE CASCADE | Relacionamento com Usuario |

---

### 2.3 Tabela: UsuarioRole (Associativa N:N)

**Descricao:** Relacionamento muitos-para-muitos entre Usuario e Role (perfis de acesso). Implementa RBAC (Role-Based Access Control).

#### Campos

| Campo | Tipo | Nulo | Default | Descricao |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NAO | NEWID() | Chave primaria |
| UsuarioId | UNIQUEIDENTIFIER | NAO | - | FK para Usuario |
| RoleId | UNIQUEIDENTIFIER | NAO | - | FK para Role |
| Created | DATETIME2 | NAO | GETDATE() | Data de criacao |
| CreatedBy | UNIQUEIDENTIFIER | SIM | NULL | FK Usuario que criou |

#### Indices

| Nome | Colunas | Tipo | Descricao |
|------|---------|------|-----------|
| PK_UsuarioRole | Id | CLUSTERED | Chave primaria |
| IX_UsuarioRole_UsuarioId | UsuarioId | NONCLUSTERED | Performance busca por usuario |
| IX_UsuarioRole_RoleId | RoleId | NONCLUSTERED | Performance busca por role |
| UQ_UsuarioRole_Usuario_Role | UsuarioId, RoleId | UNIQUE NONCLUSTERED | Impedir duplicacao |

#### Constraints

| Nome | Tipo | Definicao | Descricao |
|------|------|-----------|-----------|
| PK_UsuarioRole | PRIMARY KEY | Id | Chave primaria |
| FK_UsuarioRole_Usuario | FOREIGN KEY | UsuarioId REFERENCES Usuario(Id) ON DELETE CASCADE | Relacionamento Usuario |
| FK_UsuarioRole_Role | FOREIGN KEY | RoleId REFERENCES Role(Id) ON DELETE CASCADE | Relacionamento Role |
| UQ_UsuarioRole_Usuario_Role | UNIQUE | (UsuarioId, RoleId) | Usuario nao pode ter mesmo role duplicado |

---

## 3. Relacionamentos

| Tabela Origem | Cardinalidade | Tabela Destino | Descricao |
|---------------|---------------|----------------|-----------|
| Cliente | 1:N | Usuario | Cliente (tenant raiz) possui muitos usuarios |
| Empresa | 1:N | Usuario | Empresa (tenant especifico) possui muitos usuarios (opcional) |
| Usuario | 1:N | HistoricoSenhaUsuario | Usuario possui historico de senhas |
| Usuario | N:M | Role | Usuarios possuem multiplos perfis (via UsuarioRole) |
| Usuario | 1:N | Usuario | Usuario cria/modifica outros usuarios (auditoria) |
| Usuario | 1:N | Usuario | Usuario desativa outros usuarios |
| Usuario | 1:N | Usuario | Usuario anonimiza outros usuarios (LGPD) |

---

## 4. DDL - SQL Server

```sql
-- =============================================
-- RF012 - Gestao de Usuarios
-- Modelo de Dados
-- Data: 2025-12-27
-- Melhorias Aplicadas: MELHORIAS.md
--   - BaseAuditableGuidEntity (Created, CreatedBy, LastModified, LastModifiedBy)
--   - Fl_Ativo BIT (0,1) ao inves de Fl_Desativado INT (1,2)
--   - Politica de senha forte
--   - Historico de senhas (ultimas 12)
--   - Bloqueio por tentativas (5 falhas = bloqueio)
--   - Expiracao de senha (90 dias)
--   - MFA (Multi-Factor Authentication)
-- =============================================

-- ---------------------------------------------
-- Tabela: Usuario
-- ---------------------------------------------
CREATE TABLE Usuario (
    Id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),

    -- Multi-Tenancy (OBRIGATORIO)
    ClienteId UNIQUEIDENTIFIER NOT NULL,
    EmpresaId UNIQUEIDENTIFIER NULL,

    -- Informacoes Basicas
    Nome NVARCHAR(200) NOT NULL,
    Email NVARCHAR(200) NOT NULL,
    Telefone NVARCHAR(20) NULL,
    CPF VARCHAR(14) NULL,
    DataNascimento DATE NULL,
    Avatar NVARCHAR(500) NULL,

    -- Autenticacao e Seguranca
    PasswordHash NVARCHAR(MAX) NOT NULL,
    DataUltimoAcesso DATETIME2 NULL,
    DataExpiracaoSenha DATETIME2 NULL,
    TentativasFalhas INT NOT NULL DEFAULT 0,
    Bloqueado BIT NOT NULL DEFAULT 0,
    DataBloqueio DATETIME2 NULL,

    -- Multi-Factor Authentication (MFA)
    MFAHabilitado BIT NOT NULL DEFAULT 0,
    MFASecret NVARCHAR(500) NULL,
    TelefoneMFA NVARCHAR(20) NULL,

    -- Active Directory Integration
    UsuarioAD BIT NOT NULL DEFAULT 0,
    ADObjectGUID UNIQUEIDENTIFIER NULL,
    ADSamAccountName NVARCHAR(256) NULL,
    ADDistinguishedName NVARCHAR(500) NULL,
    DataUltimaSincronizacaoAD DATETIME2 NULL,

    -- Configuracoes e Personalizacao
    Idioma VARCHAR(10) NOT NULL DEFAULT 'pt-BR',
    Timezone VARCHAR(100) NOT NULL DEFAULT 'America/Sao_Paulo',
    Tema VARCHAR(20) NOT NULL DEFAULT 'light',

    -- Status e Controle
    Ativo BIT NOT NULL DEFAULT 1,
    FlExcluido BIT NOT NULL DEFAULT 0,
    MustChangePassword BIT NOT NULL DEFAULT 0,
    DataDesativacao DATETIME2 NULL,
    DesativadoPorId UNIQUEIDENTIFIER NULL,
    MotivoDesativacao NVARCHAR(500) NULL,

    -- Anonimizacao LGPD
    Anonimizado BIT NOT NULL DEFAULT 0,
    DataAnonimizacao DATETIME2 NULL,
    AnonimizadoPorId UNIQUEIDENTIFIER NULL,

    -- Auditoria (BaseAuditableGuidEntity)
    Created DATETIME2 NOT NULL DEFAULT GETDATE(),
    CreatedBy UNIQUEIDENTIFIER NULL,
    LastModified DATETIME2 NULL,
    LastModifiedBy UNIQUEIDENTIFIER NULL,

    -- Foreign Keys
    CONSTRAINT FK_Usuario_Cliente
        FOREIGN KEY (ClienteId) REFERENCES Cliente(Id),
    CONSTRAINT FK_Usuario_Empresa
        FOREIGN KEY (EmpresaId) REFERENCES Empresa(Id),
    CONSTRAINT FK_Usuario_CreatedBy
        FOREIGN KEY (CreatedBy) REFERENCES Usuario(Id),
    CONSTRAINT FK_Usuario_LastModifiedBy
        FOREIGN KEY (LastModifiedBy) REFERENCES Usuario(Id),
    CONSTRAINT FK_Usuario_DesativadoPor
        FOREIGN KEY (DesativadoPorId) REFERENCES Usuario(Id),
    CONSTRAINT FK_Usuario_AnonimizadoPor
        FOREIGN KEY (AnonimizadoPorId) REFERENCES Usuario(Id),

    -- Unique Constraints
    CONSTRAINT UQ_Usuario_Email_Cliente
        UNIQUE (Email, ClienteId),
    CONSTRAINT UQ_Usuario_ADObjectGUID
        UNIQUE (ADObjectGUID),

    -- Check Constraints
    CONSTRAINT CHK_Usuario_TentativasFalhas
        CHECK (TentativasFalhas >= 0),
    CONSTRAINT CHK_Usuario_Email_Format
        CHECK (Email LIKE '%@%'),
    CONSTRAINT CHK_Usuario_Idioma
        CHECK (Idioma IN ('pt-BR', 'en-US', 'es-ES'))
);

-- Indices
CREATE NONCLUSTERED INDEX IX_Usuario_ClienteId
    ON Usuario(ClienteId);
CREATE NONCLUSTERED INDEX IX_Usuario_EmpresaId
    ON Usuario(EmpresaId)
    WHERE EmpresaId IS NOT NULL;
CREATE NONCLUSTERED INDEX IX_Usuario_CPF_ClienteId
    ON Usuario(CPF, ClienteId)
    WHERE CPF IS NOT NULL;
CREATE NONCLUSTERED INDEX IX_Usuario_ADObjectGUID
    ON Usuario(ADObjectGUID)
    WHERE ADObjectGUID IS NOT NULL;
CREATE NONCLUSTERED INDEX IX_Usuario_Ativo
    ON Usuario(Ativo)
    WHERE Ativo = 1;
CREATE NONCLUSTERED INDEX IX_Usuario_FlExcluido
    ON Usuario(FlExcluido)
    WHERE FlExcluido = 0;
CREATE NONCLUSTERED INDEX IX_Usuario_Created
    ON Usuario(Created DESC);

-- Comentarios
EXEC sp_addextendedproperty
    @name = N'MS_Description', @value = N'Usuarios do sistema IControlIT com autenticacao, autorizacao, multi-tenancy, MFA e integracao AD',
    @level0type = N'SCHEMA', @level0name = N'dbo',
    @level1type = N'TABLE',  @level1name = N'Usuario';

EXEC sp_addextendedproperty
    @name = N'MS_Description', @value = N'Chave primaria (GUID)',
    @level0type = N'SCHEMA', @level0name = N'dbo',
    @level1type = N'TABLE',  @level1name = N'Usuario',
    @level2type = N'COLUMN', @level2name = N'Id';

EXEC sp_addextendedproperty
    @name = N'MS_Description', @value = N'FK para Cliente (TENANT RAIZ - multi-tenancy obrigatorio)',
    @level0type = N'SCHEMA', @level0name = N'dbo',
    @level1type = N'TABLE',  @level1name = N'Usuario',
    @level2type = N'COLUMN', @level2name = N'ClienteId';

EXEC sp_addextendedproperty
    @name = N'MS_Description', @value = N'Soft delete: 0=ativo (nao deletado), 1=excluido (deletado)',
    @level0type = N'SCHEMA', @level0name = N'dbo',
    @level1type = N'TABLE',  @level1name = N'Usuario',
    @level2type = N'COLUMN', @level2name = N'FlExcluido';

EXEC sp_addextendedproperty
    @name = N'MS_Description', @value = N'Data de criacao (BaseAuditableGuidEntity)',
    @level0type = N'SCHEMA', @level0name = N'dbo',
    @level1type = N'TABLE',  @level1name = N'Usuario',
    @level2type = N'COLUMN', @level2name = N'Created';


-- ---------------------------------------------
-- Tabela: HistoricoSenhaUsuario
-- ---------------------------------------------
CREATE TABLE HistoricoSenhaUsuario (
    Id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    UsuarioId UNIQUEIDENTIFIER NOT NULL,
    PasswordHash NVARCHAR(MAX) NOT NULL,
    DataCriacao DATETIME2 NOT NULL DEFAULT GETDATE(),

    -- Foreign Keys
    CONSTRAINT FK_HistoricoSenha_Usuario
        FOREIGN KEY (UsuarioId) REFERENCES Usuario(Id) ON DELETE CASCADE
);

-- Indices
CREATE NONCLUSTERED INDEX IX_HistoricoSenha_UsuarioId
    ON HistoricoSenhaUsuario(UsuarioId);
CREATE NONCLUSTERED INDEX IX_HistoricoSenha_DataCriacao
    ON HistoricoSenhaUsuario(DataCriacao);

-- Comentarios
EXEC sp_addextendedproperty
    @name = N'MS_Description', @value = N'Historico de senhas dos ultimos 12 meses para impedir reutilizacao',
    @level0type = N'SCHEMA', @level0name = N'dbo',
    @level1type = N'TABLE',  @level1name = N'HistoricoSenhaUsuario';


-- ---------------------------------------------
-- Tabela: UsuarioRole (Associativa N:N)
-- ---------------------------------------------
CREATE TABLE UsuarioRole (
    Id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    UsuarioId UNIQUEIDENTIFIER NOT NULL,
    RoleId UNIQUEIDENTIFIER NOT NULL,
    Created DATETIME2 NOT NULL DEFAULT GETDATE(),
    CreatedBy UNIQUEIDENTIFIER NULL,

    -- Foreign Keys
    CONSTRAINT FK_UsuarioRole_Usuario
        FOREIGN KEY (UsuarioId) REFERENCES Usuario(Id) ON DELETE CASCADE,
    CONSTRAINT FK_UsuarioRole_Role
        FOREIGN KEY (RoleId) REFERENCES Role(Id) ON DELETE CASCADE,
    CONSTRAINT FK_UsuarioRole_CreatedBy
        FOREIGN KEY (CreatedBy) REFERENCES Usuario(Id),

    -- Unique Constraints
    CONSTRAINT UQ_UsuarioRole_Usuario_Role
        UNIQUE (UsuarioId, RoleId)
);

-- Indices
CREATE NONCLUSTERED INDEX IX_UsuarioRole_UsuarioId
    ON UsuarioRole(UsuarioId);
CREATE NONCLUSTERED INDEX IX_UsuarioRole_RoleId
    ON UsuarioRole(RoleId);

-- Comentarios
EXEC sp_addextendedproperty
    @name = N'MS_Description', @value = N'Relacionamento muitos-para-muitos entre Usuario e Role (RBAC)',
    @level0type = N'SCHEMA', @level0name = N'dbo',
    @level1type = N'TABLE',  @level1name = N'UsuarioRole';
```

---

## 5. Dados Iniciais (Seed)

```sql
-- =============================================
-- Seed de Usuarios do Sistema
-- =============================================

-- Nao ha seed padrao para usuarios.
-- Usuarios sao criados dinamicamente:
--   1. Primeiro usuario: criado via Setup inicial (SuperAdmin)
--   2. Usuarios subsequentes: criados via API/UI por usuarios com permissao
--   3. Usuarios AD: sincronizados via LDAP/AD connector

-- Exemplo de criacao de SuperAdmin inicial (executado apenas no Setup):
-- NOTA: Este exemplo e apenas ilustrativo. O hash real sera gerado no Setup.

/*
-- Exemplo conceitual (NAO executar diretamente):
DECLARE @ClienteId UNIQUEIDENTIFIER = (SELECT TOP 1 Id FROM Cliente);

INSERT INTO Usuario (
    ClienteId,
    EmpresaId,
    Nome,
    Email,
    PasswordHash, -- Hash gerado no Setup
    Ativo,
    MustChangePassword,
    Idioma,
    Timezone,
    Created
)
VALUES (
    @ClienteId,
    NULL, -- SuperAdmin nao esta vinculado a empresa especifica
    'Administrador do Sistema',
    'admin@icontrolit.com',
    '$2a$11$...hash...', -- Bcrypt hash gerado no Setup
    1, -- Ativo
    1, -- Deve alterar senha no primeiro login
    'pt-BR',
    'America/Sao_Paulo',
    GETDATE()
);

-- Atribuir role SuperAdmin ao usuario criado
DECLARE @UsuarioId UNIQUEIDENTIFIER = (SELECT Id FROM Usuario WHERE Email = 'admin@icontrolit.com');
DECLARE @SuperAdminRoleId UNIQUEIDENTIFIER = (SELECT Id FROM Role WHERE Name = 'SuperAdmin');

INSERT INTO UsuarioRole (UsuarioId, RoleId, Created, CreatedBy)
VALUES (@UsuarioId, @SuperAdminRoleId, GETDATE(), NULL);
*/
```

---

## 6. Observacoes

### 6.1 Decisoes de Modelagem

1. **Multi-Tenancy Obrigatorio:**
   - Todo usuario DEVE ter `ClienteId` (tenant raiz)
   - `EmpresaId` e opcional (permite usuarios globais do cliente, ex: SuperAdmin)
   - Garante isolamento completo de dados entre clientes

2. **Auditoria Completa (BaseAuditableGuidEntity):**
   - Campos `Created`, `CreatedBy`, `LastModified`, `LastModifiedBy` obrigatorios
   - Permite rastreabilidade completa de quem criou/modificou usuarios
   - Interceptor do EF Core preenche automaticamente

3. **Soft Delete (FlExcluido):**
   - Usuarios nunca sao deletados fisicamente (conformidade LGPD)
   - `FlExcluido = 1` marca usuario como deletado logicamente
   - Permite auditoria e recuperacao se necessario

4. **Anonimizacao LGPD:**
   - Campos `Anonimizado`, `DataAnonimizacao`, `AnonimizadoPorId`
   - Permite atender direito ao esquecimento (LGPD Art. 18)
   - Processo de anonimizacao substitui dados pessoais por valores genericos

5. **Politica de Senha Forte:**
   - Hash bcrypt armazenado em `PasswordHash`
   - Historico de senhas em `HistoricoSenhaUsuario` (ultimas 12)
   - Expiracao automatica em 90 dias (`DataExpiracaoSenha`)
   - Bloqueio automatico apos 5 tentativas falhas (`TentativasFalhas`, `Bloqueado`)

6. **Multi-Factor Authentication (MFA):**
   - `MFAHabilitado` habilita MFA
   - `MFASecret` armazena secret TOTP (criptografado)
   - `TelefoneMFA` permite MFA via SMS

7. **Integracao Active Directory:**
   - `UsuarioAD = 1` indica usuario sincronizado com AD
   - `ADObjectGUID` e UNIQUE para evitar duplicacao
   - Sincronizacao incremental via `DataUltimaSincronizacaoAD`

8. **Indices de Performance:**
   - Indice composto `(Email, ClienteId)` para login rapido dentro do tenant
   - Indices filtrados (`WHERE Ativo = 1`, `WHERE FlExcluido = 0`) para queries comuns
   - Indice em `Created DESC` para ordenacao temporal

### 6.2 Consideracoes de Performance

1. **Indices Filtrados:**
   - Usuarios ativos: `WHERE Ativo = 1` (reduz tamanho do indice)
   - Usuarios nao deletados: `WHERE FlExcluido = 0`

2. **Paginacao Obrigatoria:**
   - Listar usuarios SEMPRE com paginacao (100-200 registros por pagina)
   - Nunca carregar todos os usuarios de uma vez

3. **Cleanup Automatico:**
   - Job noturno para deletar registros de `HistoricoSenhaUsuario` com mais de 12 meses
   - Job mensal para anonimizar usuarios marcados para anonimizacao

### 6.3 Notas sobre Migracao de Dados

1. **Migracao do Sistema Legado:**
   - Campo `Fl_Desativado INT (1,2)` do legado → `Ativo BIT (0,1)` do novo sistema
   - Regra: `Fl_Desativado = 2` → `Ativo = 1`, `Fl_Desativado = 1` → `Ativo = 0`

2. **Migracao de Senhas:**
   - Senhas do legado estao em formato diferente (VB.NET hash)
   - Solucao: Marcar `MustChangePassword = 1` para todos os usuarios migrados
   - Usuarios devem redefinir senha no primeiro login

3. **Migracao de Perfis:**
   - Mapear perfis do legado para Roles do novo sistema
   - Criar registros em `UsuarioRole` para cada mapeamento

---

## Historico de Alteracoes

| Versao | Data | Autor | Descricao |
|--------|------|-------|-----------|
| 1.0 | 2025-12-27 | Claude Architect | Versao inicial com melhorias MELHORIAS.md aplicadas |
