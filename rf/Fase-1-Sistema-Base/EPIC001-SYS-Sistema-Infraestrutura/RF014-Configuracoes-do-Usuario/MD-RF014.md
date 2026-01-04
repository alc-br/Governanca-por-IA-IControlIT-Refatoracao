# MD-RF014: Modelo de Dados - Configuracoes do Usuario

**RF Relacionado**: RF014 - Configuracoes do Usuario
**Versao**: 1.1 | **Data**: 2025-12-27
**Banco de Dados**: SQL Server

**CHANGELOG**:
- v1.1 (2025-12-27): Atualizacao conforme CONTRATO DE DOCUMENTACAO ESSENCIAL - Inclusao de campos de auditoria completos (Id_Usuario_Criacao, Id_Usuario_Alteracao, Dt_Criacao, Dt_Alteracao), uso de Fl_Ativo BIT, padronizacao SQL Server
- v1.0 (2025-11-19): Versao inicial

---

## Resumo

Este documento descreve o modelo de dados utilizado pela funcionalidade de Configuracoes do Usuario. A funcionalidade utiliza principalmente a tabela `Usuario` existente, com campos especificos para preferencias do usuario.

---

## Diagrama ER

```
                +----------------------+
                |   Conglomerado       |
                +----------------------+
                | PK Id                |
                |    Nm_Conglomerado   |
                +----------------------+
                          ^
                          | N:1
                          |
+------------------+      |          +------------------+
|     Usuario      |------+          |  Usuario (Audit) |
+------------------+                 +------------------+
| PK Id            |<----------------|    (self-ref)    |
|    Nome          |       1:N       +------------------+
|    Email         |
|    PasswordHash  |
|    CPF           |
|    Telefone      |
|    DataNascimento|
|    Avatar        |
|    Idioma        |   <- Preferencias
|    Timezone      |   <- Preferencias
|    Tema          |   <- Preferencias
|    MustChangePassword
|    DataUltimoAcesso
|    DataExpiracaoSenha
|    Bloqueado     |
|    MFAHabilitado |
|    Fl_Ativo      |   <- Status (BIT)
| FK Id_Conglomerado
| FK Id_Usuario_Criacao    <- Auditoria
|    Dt_Criacao            <- Auditoria
| FK Id_Usuario_Alteracao  <- Auditoria
|    Dt_Alteracao          <- Auditoria
+------------------+
```

---

## DDL Completo - Tabela Usuario

```sql
-- Tabela Usuario (campos relevantes para Configuracoes do Usuario)
CREATE TABLE Usuario (
    -- Chave Primaria
    Id UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),

    -- Informacoes Pessoais
    Nome NVARCHAR(200) NOT NULL,
    Email NVARCHAR(200) NOT NULL,
    PasswordHash NVARCHAR(500) NOT NULL,
    CPF NVARCHAR(14) NULL,
    Telefone NVARCHAR(20) NULL,
    DataNascimento DATE NULL,
    Avatar NVARCHAR(500) NULL,

    -- Preferencias de Interface
    Idioma NVARCHAR(10) NOT NULL DEFAULT 'pt-BR',
    Timezone NVARCHAR(50) NOT NULL DEFAULT 'America/Sao_Paulo',
    Tema NVARCHAR(20) NOT NULL DEFAULT 'light',

    -- Seguranca de Senha
    MustChangePassword BIT NOT NULL DEFAULT 0,
    DataUltimoAcesso DATETIME2 NULL,
    DataExpiracaoSenha DATETIME2 NULL,
    TentativasFalhasLogin INT NOT NULL DEFAULT 0,
    DataUltimaTentativaFalha DATETIME2 NULL,

    -- Bloqueio de Conta
    Bloqueado BIT NOT NULL DEFAULT 0,
    DataBloqueio DATETIME2 NULL,
    MotivoBloqueio NVARCHAR(500) NULL,

    -- Autenticacao Multi-Fator
    MFAHabilitado BIT NOT NULL DEFAULT 0,
    MFASecret NVARCHAR(100) NULL,

    -- Active Directory
    UsuarioAD BIT NOT NULL DEFAULT 0,
    ADSamAccountName NVARCHAR(100) NULL,

    -- Status da Conta
    Fl_Ativo BIT NOT NULL DEFAULT 1,
    Dt_Desativacao DATETIME2 NULL,
    Ds_Motivo_Desativacao NVARCHAR(500) NULL,
    Fl_Anonimizado BIT NOT NULL DEFAULT 0,

    -- Multi-Tenancy
    Id_Conglomerado UNIQUEIDENTIFIER NOT NULL,

    -- Auditoria (Campos Obrigatorios conforme Padrao IControlIT)
    Id_Usuario_Criacao UNIQUEIDENTIFIER NOT NULL,
    Dt_Criacao DATETIME2 NOT NULL DEFAULT GETDATE(),
    Id_Usuario_Alteracao UNIQUEIDENTIFIER NULL,
    Dt_Alteracao DATETIME2 NULL,

    -- Constraints
    CONSTRAINT PK_Usuario PRIMARY KEY (Id),
    CONSTRAINT UQ_Usuario_Email UNIQUE (Email),
    CONSTRAINT FK_Usuario_Conglomerado FOREIGN KEY (Id_Conglomerado)
        REFERENCES Conglomerado(Id) ON DELETE NO ACTION,
    CONSTRAINT FK_Usuario_UsuarioCriacao FOREIGN KEY (Id_Usuario_Criacao)
        REFERENCES Usuario(Id) ON DELETE NO ACTION,
    CONSTRAINT FK_Usuario_UsuarioAlteracao FOREIGN KEY (Id_Usuario_Alteracao)
        REFERENCES Usuario(Id) ON DELETE NO ACTION,
    CONSTRAINT CK_Usuario_Idioma CHECK (Idioma IN ('pt-BR', 'en-US', 'es-ES')),
    CONSTRAINT CK_Usuario_Tema CHECK (Tema IN ('light', 'dark', 'auto'))
);

-- Indices
CREATE INDEX IX_Usuario_Email ON Usuario(Email);
CREATE INDEX IX_Usuario_Id_Conglomerado ON Usuario(Id_Conglomerado);
CREATE INDEX IX_Usuario_Fl_Ativo ON Usuario(Fl_Ativo);
CREATE INDEX IX_Usuario_CPF ON Usuario(CPF) WHERE CPF IS NOT NULL;
CREATE INDEX IX_Usuario_Dt_Criacao ON Usuario(Dt_Criacao);
CREATE INDEX IX_Usuario_Id_Usuario_Criacao ON Usuario(Id_Usuario_Criacao);

-- Comentarios
EXEC sp_addextendedproperty
    @name = N'MS_Description',
    @value = N'Tabela de usuarios do sistema com informacoes pessoais, preferencias e seguranca',
    @level0type = N'SCHEMA', @level0name = 'dbo',
    @level1type = N'TABLE', @level1name = 'Usuario';

EXEC sp_addextendedproperty
    @name = N'MS_Description',
    @value = N'Idioma preferido do usuario (pt-BR, en-US, es-ES)',
    @level0type = N'SCHEMA', @level0name = 'dbo',
    @level1type = N'TABLE', @level1name = 'Usuario',
    @level2type = N'COLUMN', @level2name = 'Idioma';

EXEC sp_addextendedproperty
    @name = N'MS_Description',
    @value = N'Timezone IANA preferido (America/Sao_Paulo, etc)',
    @level0type = N'SCHEMA', @level0name = 'dbo',
    @level1type = N'TABLE', @level1name = 'Usuario',
    @level2type = N'COLUMN', @level2name = 'Timezone';

EXEC sp_addextendedproperty
    @name = N'MS_Description',
    @value = N'Tema visual preferido (light, dark, auto)',
    @level0type = N'SCHEMA', @level0name = 'dbo',
    @level1type = N'TABLE', @level1name = 'Usuario',
    @level2type = N'COLUMN', @level2name = 'Tema';
```

---

## Dicionario de Dados - Campos de Preferencias

### Campos Utilizados na Funcionalidade

| Campo | Tipo | Obrigatorio | Default | Descricao |
|-------|------|-------------|---------|-----------|
| **Id** | UNIQUEIDENTIFIER | Sim | NEWID() | Identificador unico do usuario |
| **Nome** | NVARCHAR(200) | Sim | - | Nome completo (somente leitura na tela) |
| **Email** | NVARCHAR(200) | Sim | - | Email do usuario (somente leitura) |
| **PasswordHash** | NVARCHAR(500) | Sim | - | Hash bcrypt da senha |
| **CPF** | NVARCHAR(14) | Nao | NULL | CPF formatado (somente leitura) |
| **Telefone** | NVARCHAR(20) | Nao | NULL | Telefone com DDD (editavel) |
| **DataNascimento** | DATE | Nao | NULL | Data de nascimento (editavel) |
| **Idioma** | NVARCHAR(10) | Sim | 'pt-BR' | Codigo do idioma preferido |
| **Timezone** | NVARCHAR(50) | Sim | 'America/Sao_Paulo' | Timezone IANA |
| **Tema** | NVARCHAR(20) | Sim | 'light' | Tema visual |
| **MustChangePassword** | BIT | Sim | 0 | Flag para forcar troca de senha |
| **Fl_Ativo** | BIT | Sim | 1 | Status ativo/inativo do usuario |
| **Id_Conglomerado** | UNIQUEIDENTIFIER | Sim | - | FK para conglomerado (multi-tenancy) |
| **Id_Usuario_Criacao** | UNIQUEIDENTIFIER | Sim | - | FK usuario que criou o registro |
| **Dt_Criacao** | DATETIME2 | Sim | GETDATE() | Data/hora de criacao do registro |
| **Id_Usuario_Alteracao** | UNIQUEIDENTIFIER | Nao | NULL | FK usuario que fez ultima alteracao |
| **Dt_Alteracao** | DATETIME2 | Nao | NULL | Data/hora da ultima alteracao |

---

## Valores Validos

### Idiomas
| Valor | Descricao |
|-------|-----------|
| pt-BR | Portugues do Brasil |
| en-US | Ingles (Estados Unidos) |
| es-ES | Espanhol (Espanha) |

### Temas
| Valor | Descricao |
|-------|-----------|
| light | Tema claro |
| dark | Tema escuro |
| auto | Automatico (segue SO) |

### Timezones (principais)
| Valor IANA | GMT | Descricao |
|------------|-----|-----------|
| America/Sao_Paulo | -3 | Brasilia |
| America/Manaus | -4 | Manaus |
| America/Rio_Branco | -5 | Rio Branco |
| America/Noronha | -2 | Fernando de Noronha |
| America/New_York | -5 | New York |
| America/Los_Angeles | -8 | Los Angeles |
| Europe/London | 0 | Londres |
| Europe/Paris | +1 | Paris |
| Asia/Tokyo | +9 | Toquio |

---

## DTOs Relacionados

### UsuarioDto (Query Response)

```csharp
public class UsuarioDto
{
    // Identificacao
    public Guid Id { get; set; }

    // Informacoes Basicas
    public string Nome { get; set; }
    public string Email { get; set; }
    public string? Telefone { get; set; }
    public string? CPF { get; set; }
    public DateTime? DataNascimento { get; set; }
    public string? Avatar { get; set; }

    // Preferencias
    public string Idioma { get; set; } = "pt-BR";
    public string Timezone { get; set; } = "America/Sao_Paulo";
    public string Tema { get; set; } = "light";

    // Seguranca
    public DateTime? DataUltimoAcesso { get; set; }
    public DateTime? DataExpiracaoSenha { get; set; }
    public bool Bloqueado { get; set; }
    public bool MFAHabilitado { get; set; }
    public bool MustChangePassword { get; set; }

    // Status
    public bool Ativo { get; set; }
    public bool Anonimizado { get; set; }

    // Multi-Tenancy
    public Guid IdConglomerado { get; set; }
    public string? ConglomeradoNome { get; set; }
    public List<RoleDto> Roles { get; set; } = new();

    // Auditoria
    public Guid IdUsuarioCriacao { get; set; }
    public DateTime DtCriacao { get; set; }
    public Guid? IdUsuarioAlteracao { get; set; }
    public DateTime? DtAlteracao { get; set; }
}
```

### ChangePasswordCommand (Command Request)

```csharp
public record ChangePasswordCommand : IRequest
{
    public string SenhaAtual { get; init; } = string.Empty;
    public string NovaSenha { get; init; } = string.Empty;
}
```

### UpdateUserPreferencesCommand (Futuro)

```csharp
public record UpdateUserPreferencesCommand : IRequest
{
    public string? Telefone { get; init; }
    public DateTime? DataNascimento { get; init; }
    public string? Idioma { get; init; }
    public string? Timezone { get; init; }
    public string? Tema { get; init; }
}
```

---

## Relacionamentos

### Usuario -> Conglomerado (N:1)
- Um usuario pertence a um conglomerado (multi-tenancy)
- Um conglomerado pode ter muitos usuarios
- FK: `Usuario.Id_Conglomerado` -> `Conglomerado.Id`

### Usuario -> Usuario (Auditoria - 1:N)
- Um usuario pode criar muitos outros usuarios
- FK: `Usuario.Id_Usuario_Criacao` -> `Usuario.Id`
- FK: `Usuario.Id_Usuario_Alteracao` -> `Usuario.Id`

### Usuario -> UsuarioRole -> Role (N:N)
- Um usuario pode ter multiplos perfis
- Um perfil pode ter multiplos usuarios
- Tabela intermediaria: `UsuarioRole`

---

## Historico de Auditoria

A tabela `Usuario` utiliza o mecanismo de auditoria automatica do sistema (AuditInterceptor). Todas as alteracoes sao registradas na tabela `AuditLog`.

### Eventos Auditados
| Operacao | Evento | Dados |
|----------|--------|-------|
| UPDATE (senha) | USUARIO_SENHA_ALTERADA | UserId, Timestamp, IP |
| UPDATE (dados) | USUARIO_DADOS_ATUALIZADOS | UserId, CamposAlterados, ValoresAntigos, ValoresNovos |
| UPDATE (preferencias) | USUARIO_PREFERENCIAS_ATUALIZADAS | UserId, PreferenciasAntigas, PreferenciasNovas |

---

## Migracao/Script Inicial

Nao e necessaria nova migracao. A tabela `Usuario` ja existe e contem todos os campos necessarios. Os campos de preferencias (`Idioma`, `Timezone`, `Tema`) foram adicionados em migracao anterior.

### Verificar Campos de Preferencias

```sql
-- Verificar se campos de preferencias existem
SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_DEFAULT
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'Usuario'
  AND COLUMN_NAME IN ('Idioma', 'Timezone', 'Tema');
```

### Atualizar Valores Default (se necessario)

```sql
-- Definir valores default para usuarios existentes sem preferencias
UPDATE Usuario
SET Idioma = 'pt-BR'
WHERE Idioma IS NULL;

UPDATE Usuario
SET Timezone = 'America/Sao_Paulo'
WHERE Timezone IS NULL;

UPDATE Usuario
SET Tema = 'light'
WHERE Tema IS NULL;

-- Garantir que campo Fl_Ativo tenha valor (se migrado de campo Ativo)
UPDATE Usuario
SET Fl_Ativo = 1
WHERE Fl_Ativo IS NULL;
```

---

## Consideracoes de Performance

### Indices Recomendados
- `IX_Usuario_Email` - Busca por email (login)
- `IX_Usuario_Id_Conglomerado` - Filtro por conglomerado (multi-tenancy)
- `IX_Usuario_Fl_Ativo` - Filtro por status
- `IX_Usuario_Dt_Criacao` - Ordenacao por data de criacao
- `IX_Usuario_Id_Usuario_Criacao` - Rastreamento de auditoria (quem criou)

### Cache
- Dados do usuario atual podem ser cacheados no frontend
- Invalidar cache ao alterar dados/preferencias
- Idioma e salvo em localStorage para acesso rapido

---

## Seguranca

### Campos Sensiveis
- `PasswordHash` - Nunca exposto em DTOs
- `MFASecret` - Nunca exposto em DTOs
- `CPF` - Mascarado se necessario

### Validacoes de Integridade
- Email unico no sistema
- Idioma deve estar na lista permitida
- Tema deve estar na lista permitida
- Timezone deve ser valor IANA valido

---

## Relacionamento com LocalStorage

Algumas preferencias sao armazenadas no localStorage do navegador para acesso rapido:

| Key | Descricao | Sync com Backend |
|-----|-----------|------------------|
| `preferredLang` | Idioma selecionado | TODO |
| `theme` | Tema selecionado | TODO |

**Nota**: Futuramente, preferencias salvas no localStorage devem sincronizar com o backend para consistencia entre dispositivos.
