# Modelo de Dados - RF033: Gestão de Chamados (Service Desk)

**Versão:** 1.0
**Data:** 2025-12-18
**RF Relacionado:** [RF033 - Gestão de Chamados](./RF033.md)
**Banco de Dados:** SQL Server / SQLite (dev)

---

## 1. Diagrama Entidade-Relacionamento (ER)

```
┌────────────────────┐         ┌─────────────────────────┐         ┌──────────────────────┐
│  Conglomerados     │         │       Chamados          │         │   ChamadosItens      │
├────────────────────┤         ├─────────────────────────┤         ├──────────────────────┤
│ Id (PK)            │◄────────┤ Id (PK)                 │◄────────┤ Id (PK)              │
│ Nome               │         │ ConglomeradoId (FK)     │         │ ChamadoId (FK)       │
└────────────────────┘         │ Titulo                  │         │ Descricao            │
                               │ Descricao               │         │ UsuarioId (FK)       │
┌────────────────────┐         │ UsuarioSolicitanteId    │◄───┐    │ DataHora             │
│    Users           │         │ UsuarioAtendenteId      │    │    │ FlPublico            │
├────────────────────┤         │ TipoSolicitacaoId       │    │    │ TipoItem (enum)      │
│ Id (PK)            │◄────────┤ TipoAtivoId             │    │    └──────────────────────┘
│ Nome               │     ┌───┤ FilaAtendimentoId       │    │
│ Email              │     │   │ Status (enum)           │    │    ┌──────────────────────┐
└────────────────────┘     │   │ Prioridade (enum)       │    │    │  ChamadosAnexos      │
                           │   │ DataSolicitacao         │    │    ├──────────────────────┤
┌────────────────────┐     │   │ DataVencimento          │    │    │ Id (PK)              │
│ TiposSolicitacao   │     │   │ DataEncerramento        │    │    │ ChamadoId (FK)       │
├────────────────────┤     │   │ DataInicioAguardando    │    └────┤ ChamadoItemId (FK)   │
│ Id (PK)            │◄────┤   │ TotalHorasAguardando    │         │ NomeArquivo          │
│ Nome               │     │   │ SolucaoId               │         │ TamanhoBytes         │
│ DescricaoTemplate  │     │   │ Avaliacao (1-5)         │         │ TipoConteudo         │
│ PrazoDias          │     │   │ ComentarioAvaliacao     │         │ URLArquivo           │
└────────────────────┘     │   │ FlEscalado              │         │ HashSHA256           │
                           │   │ DataEscalacao           │         └──────────────────────┘
┌────────────────────┐     │   │ AtivoId (FK) [NULL]     │
│ TiposAtivo         │     │   │ ConsumidorUnidadeId     │         ┌──────────────────────┐
├────────────────────┤     │   │ FlExcluido              │         │  ChamadosHistory     │
│ Id (PK)            │◄────┤   │ CreatedAt               │         ├──────────────────────┤
│ Nome               │     │   │ CreatedBy               │         │ Id (PK)              │
│ Categoria          │     │   │ UpdatedAt               │         │ ChamadoId (FK)       │
└────────────────────┘     │   │ UpdatedBy               │         │ Operation            │
                           │   └─────────────────────────┘         │ OldValues (JSON)     │
┌────────────────────┐     │                                       │ NewValues (JSON)     │
│ FilasAtendimento   │     │                                       │ ChangedBy            │
├────────────────────┤     │                                       │ ChangedAt            │
│ Id (PK)            │◄────┘                                       └──────────────────────┘
│ Nome               │
│ Nivel (N1/N2/N3)   │
│ SupervisorId       │         ┌─────────────────────────┐
└────────────────────┘         │  SolicitacoesSolucoes   │
                               ├─────────────────────────┤
┌────────────────────┐         │ Id (PK)                 │
│      Ativos        │         │ Titulo                  │
├────────────────────┤         │ Descricao               │
│ Id (PK)            │◄────┐   │ FlBaseConhecimento      │
│ Nome               │     │   │ QtdUtilizacoes          │
│ TipoAtivoId        │     │   │ NotaMedia               │
└────────────────────┘     │   └─────────────────────────┘
                           │                   ▲
┌────────────────────┐     │                   │
│ ConsumidoresUnidad │     │                   │
├────────────────────┤     │   ┌───────────────┴──────┐
│ Id (PK)            │◄────┼───┤ (FK SolucaoId)       │
│ Nome               │     └───┤ Chamados.SolucaoId   │
│ Endereco           │         └──────────────────────┘
└────────────────────┘
```

---

## 2. Entidades

### 2.1 Tabela: Chamados

**Descrição:** Tabela principal de chamados (tickets) do Service Desk com workflow de status e cálculo de SLA.

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| ClienteId | UNIQUEIDENTIFIER | NÃO | - | FK para Cliente (multi-tenancy raiz)s (multi-tenancy) |
| Titulo | NVARCHAR(300) | NÃO | - | Título do chamado (min 10 caracteres) |
| Descricao | NVARCHAR(MAX) | NÃO | - | Descrição detalhada (rich text) |
| UsuarioSolicitanteId | UNIQUEIDENTIFIER | NÃO | - | FK para Users (quem abriu) |
| UsuarioAtendenteId | UNIQUEIDENTIFIER | SIM | NULL | FK para Users (técnico atribuído) |
| TipoSolicitacaoId | UNIQUEIDENTIFIER | NÃO | - | FK para TiposSolicitacao |
| TipoAtivoId | UNIQUEIDENTIFIER | NÃO | - | FK para TiposAtivo |
| FilaAtendimentoId | UNIQUEIDENTIFIER | NÃO | - | FK para FilasAtendimento |
| Status | INT | NÃO | 1 | Enum: 1=Aberto, 2=EmAtendimento, 3=AguardandoUsuario, 4=AguardandoFornecedor, 5=Resolvido, 6=Encerrado, 7=Cancelado |
| Prioridade | INT | NÃO | 2 | Enum: 1=Baixa, 2=Média, 3=Alta, 4=Urgente |
| DataSolicitacao | DATETIME2 | NÃO | GETDATE() | Data/hora de abertura |
| DataVencimento | DATETIME2 | NÃO | - | Data/hora limite (SLA) |
| DataEncerramento | DATETIME2 | SIM | NULL | Data/hora de encerramento |
| DataInicioAguardando | DATETIME2 | SIM | NULL | Quando mudou para status "Aguardando" |
| TotalHorasAguardando | INT | NÃO | 0 | Horas acumuladas em status "Aguardando" (pausa SLA) |
| SolucaoId | UNIQUEIDENTIFIER | SIM | NULL | FK para SolicitacoesSolucoes |
| Avaliacao | INT | SIM | NULL | Nota de satisfação (1 a 5 estrelas) |
| ComentarioAvaliacao | NVARCHAR(500) | SIM | NULL | Comentário da avaliação |
| FlEscalado | BIT | NÃO | 0 | Se foi escalado automaticamente |
| DataEscalacao | DATETIME2 | SIM | NULL | Data/hora do escalonamento |
| AtivoId | UNIQUEIDENTIFIER | SIM | NULL | FK para Ativos (opcional) |
| ConsumidorUnidadeId | UNIQUEIDENTIFIER | SIM | NULL | FK para ConsumidoresUnidades (opcional) |
| Ativo | BIT | NÃO | true | Soft delete: false=ativo, true=excluído flag |
| CreatedAt | DATETIME2 | NÃO | GETDATE() | Data de criação |
| CreatedBy | UNIQUEIDENTIFIER | NÃO | - | Usuário que criou |
| UpdatedAt | DATETIME2 | SIM | NULL | Data de atualização |
| UpdatedBy | UNIQUEIDENTIFIER | SIM | NULL | Usuário que atualizou |

#### Índices (14 índices)

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| PK_Chamados | Id | CLUSTERED | Chave primária |
| IX_Chamados_ConglomeradoId | ClienteId | NONCLUSTERED | Performance multi-tenant |
| IX_Chamados_Status_DataVencimento | (Status, DataVencimento) | NONCLUSTERED | Dashboard de SLA |
| IX_Chamados_UsuarioSolicitanteId | UsuarioSolicitanteId | NONCLUSTERED | "Meus chamados" |
| IX_Chamados_UsuarioAtendenteId | UsuarioAtendenteId | NONCLUSTERED | Atribuídos a técnico |
| IX_Chamados_FilaAtendimentoId | FilaAtendimentoId | NONCLUSTERED | Fila de atendimento |
| IX_Chamados_TipoSolicitacaoId | TipoSolicitacaoId | NONCLUSTERED | Relatórios por tipo |
| IX_Chamados_DataSolicitacao | DataSolicitacao DESC | NONCLUSTERED | Ordenação cronológica |
| IX_Chamados_Prioridade | Prioridade DESC | NONCLUSTERED | Ordenação por prioridade |
| IX_Chamados_FlEscalado | FlEscalado | NONCLUSTERED FILTERED | Chamados escalados (WHERE FlEscalado = 1) |
| IX_Chamados_SLA_Vencido | DataVencimento | NONCLUSTERED FILTERED | SLA vencido (WHERE DataVencimento < GETDATE() AND Status NOT IN (6,7)) |
| IX_Chamados_AtivoId | AtivoId | NONCLUSTERED | Chamados por ativo |
| IX_Chamados_CreatedAt | CreatedAt DESC | NONCLUSTERED | Auditoria temporal |
| IX_Chamados_Composto_Dashboard | (ConglomeradoId, Status, DataVencimento) INCLUDE (Titulo, Prioridade, UsuarioAtendenteId) | NONCLUSTERED | Query dashboard otimizada |

#### Constraints

| Nome | Tipo | Definição | Descrição |
|------|------|-----------|-----------|
| PK_Chamados | PRIMARY KEY | Id | Chave primária |
| FK_Chamados_Conglomerado | FOREIGN KEY | ConglomeradoId REFERENCES Conglomerados(Id) | Multi-tenancy |
| FK_Chamados_UsuarioSolicitante | FOREIGN KEY | UsuarioSolicitanteId REFERENCES Users(Id) | Solicitante |
| FK_Chamados_UsuarioAtendente | FOREIGN KEY | UsuarioAtendenteId REFERENCES Users(Id) | Atendente |
| FK_Chamados_TipoSolicitacao | FOREIGN KEY | TipoSolicitacaoId REFERENCES TiposSolicitacao(Id) | Tipo |
| FK_Chamados_TipoAtivo | FOREIGN KEY | TipoAtivoId REFERENCES TiposAtivo(Id) | Categoria |
| FK_Chamados_FilaAtendimento | FOREIGN KEY | FilaAtendimentoId REFERENCES FilasAtendimento(Id) | Fila |
| FK_Chamados_Solucao | FOREIGN KEY | SolucaoId REFERENCES SolicitacoesSolucoes(Id) | Solução aplicada |
| FK_Chamados_Ativo | FOREIGN KEY | AtivoId REFERENCES Ativos(Id) | Ativo relacionado |
| FK_Chamados_ConsumidorUnidade | FOREIGN KEY | ConsumidorUnidadeId REFERENCES ConsumidoresUnidades(Id) | Localidade |
| FK_Chamados_CreatedBy | FOREIGN KEY | CreatedBy REFERENCES Users(Id) | Auditoria criação |
| FK_Chamados_UpdatedBy | FOREIGN KEY | UpdatedBy REFERENCES Users(Id) | Auditoria atualização |
| CK_Chamados_Status | CHECK | Status BETWEEN 1 AND 7 | Status válido |
| CK_Chamados_Prioridade | CHECK | Prioridade BETWEEN 1 AND 4 | Prioridade válida |
| CK_Chamados_Avaliacao | CHECK | Avaliacao IS NULL OR (Avaliacao BETWEEN 1 AND 5) | Avaliação 1-5 estrelas |
| CK_Chamados_DataVencimento | CHECK | DataVencimento >= DataSolicitacao | Vencimento após abertura |
| CK_Chamados_DataEncerramento | CHECK | DataEncerramento IS NULL OR DataEncerramento >= DataSolicitacao | Encerramento após abertura |

---

### 2.2 Tabela: ChamadosItens

**Descrição:** Interações/comentários do chamado (públicos ou internos).

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| ChamadoId | UNIQUEIDENTIFIER | NÃO | - | FK para Chamados |
| Descricao | NVARCHAR(MAX) | NÃO | - | Conteúdo do comentário |
| UsuarioId | UNIQUEIDENTIFIER | NÃO | - | FK para Users (quem comentou) |
| DataHora | DATETIME2 | NÃO | GETDATE() | Timestamp do comentário |
| FlPublico | BIT | NÃO | 1 | Se é visível ao solicitante (1=sim, 0=apenas equipe) |
| TipoItem | INT | NÃO | 1 | Enum: 1=Comentario, 2=MudancaStatus, 3=Reatribuicao, 4=Escalonamento |
| Ativo | BIT | NÃO | true | Soft delete: false=ativo, true=excluído flag |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| PK_ChamadosItens | Id | CLUSTERED | Chave primária |
| IX_ChamadosItens_ChamadoId | ChamadoId, DataHora DESC | NONCLUSTERED | Timeline do chamado |
| IX_ChamadosItens_UsuarioId | UsuarioId | NONCLUSTERED | Comentários por usuário |
| IX_ChamadosItens_FlPublico | FlPublico | NONCLUSTERED FILTERED | Comentários públicos (WHERE FlPublico = 1) |

#### Constraints

| Nome | Tipo | Definição | Descrição |
|------|------|-----------|-----------|
| PK_ChamadosItens | PRIMARY KEY | Id | Chave primária |
| FK_ChamadosItens_Chamado | FOREIGN KEY | ChamadoId REFERENCES Chamados(Id) | Vínculo com chamado |
| FK_ChamadosItens_Usuario | FOREIGN KEY | UsuarioId REFERENCES Users(Id) | Autor do comentário |
| CK_ChamadosItens_TipoItem | CHECK | TipoItem BETWEEN 1 AND 4 | Tipo de item válido |

---

### 2.3 Tabela: ChamadosAnexos

**Descrição:** Arquivos anexados aos chamados e seus itens.

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| ChamadoId | UNIQUEIDENTIFIER | NÃO | - | FK para Chamados |
| ChamadoItemId | UNIQUEIDENTIFIER | SIM | NULL | FK para ChamadosItens (opcional) |
| NomeArquivo | NVARCHAR(500) | NÃO | - | Nome original do arquivo |
| TamanhoBytes | BIGINT | NÃO | - | Tamanho em bytes |
| TipoConteudo | NVARCHAR(100) | NÃO | - | MIME type (image/png, application/pdf, etc.) |
| URLArquivo | NVARCHAR(1000) | NÃO | - | URL do Azure Blob Storage |
| HashSHA256 | NVARCHAR(64) | NÃO | - | Hash SHA-256 para integridade |
| Ativo | BIT | NÃO | true | Soft delete: false=ativo, true=excluído flag |
| CreatedAt | DATETIME2 | NÃO | GETDATE() | Data de upload |
| CreatedBy | UNIQUEIDENTIFIER | NÃO | - | Usuário que fez upload |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| PK_ChamadosAnexos | Id | CLUSTERED | Chave primária |
| IX_ChamadosAnexos_ChamadoId | ChamadoId | NONCLUSTERED | Anexos de um chamado |
| IX_ChamadosAnexos_ChamadoItemId | ChamadoItemId | NONCLUSTERED | Anexos de um comentário |
| IX_ChamadosAnexos_HashSHA256 | HashSHA256 | NONCLUSTERED | Verificação de duplicados |

#### Constraints

| Nome | Tipo | Definição | Descrição |
|------|------|-----------|-----------|
| PK_ChamadosAnexos | PRIMARY KEY | Id | Chave primária |
| FK_ChamadosAnexos_Chamado | FOREIGN KEY | ChamadoId REFERENCES Chamados(Id) | Vínculo com chamado |
| FK_ChamadosAnexos_ChamadoItem | FOREIGN KEY | ChamadoItemId REFERENCES ChamadosItens(Id) | Vínculo com comentário |
| FK_ChamadosAnexos_CreatedBy | FOREIGN KEY | CreatedBy REFERENCES Users(Id) | Autor do upload |
| CK_ChamadosAnexos_TamanhoBytes | CHECK | TamanhoBytes > 0 AND TamanhoBytes <= 10485760 | Max 10 MB |

---

### 2.4 Tabela: TiposSolicitacao

**Descrição:** Tipos/categorias de chamados (Hardware, Software, Rede, Acesso, etc.).

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| Nome | NVARCHAR(100) | NÃO | - | Nome do tipo |
| DescricaoTemplate | NVARCHAR(MAX) | SIM | NULL | Template de descrição |
| PrazoDias | INT | NÃO | 3 | Prazo padrão em dias úteis |
| Icone | NVARCHAR(50) | SIM | NULL | Material icon name |
| Cor | NVARCHAR(7) | SIM | NULL | Cor hexadecimal (#FF5733) |
| Ordem | INT | NÃO | 0 | Ordem de exibição |
| Ativo | BIT | NÃO | 1 | Se está ativo |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| PK_TiposSolicitacao | Id | CLUSTERED | Chave primária |
| IX_TiposSolicitacao_Ativo_Ordem | (Ativo, Ordem) | NONCLUSTERED | Listagem ativa ordenada |

---

### 2.5 Tabela: FilasAtendimento

**Descrição:** Filas de atendimento por nível (N1, N2, N3) e especialização.

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| ClienteId | UNIQUEIDENTIFIER | NÃO | - | FK para Cliente (multi-tenancy raiz)s |
| Nome | NVARCHAR(100) | NÃO | - | Nome da fila |
| Nivel | INT | NÃO | 1 | Nível de atendimento (1=N1, 2=N2, 3=N3) |
| SupervisorId | UNIQUEIDENTIFIER | SIM | NULL | FK para Users (supervisor) |
| EmailFila | NVARCHAR(200) | SIM | NULL | Email da fila |
| Ativo | BIT | NÃO | 1 | Se está ativa |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| PK_FilasAtendimento | Id | CLUSTERED | Chave primária |
| IX_FilasAtendimento_ConglomeradoId | ClienteId | NONCLUSTERED | Performance multi-tenant |
| IX_FilasAtendimento_Nivel | Nivel | NONCLUSTERED | Busca por nível |

---

### 2.6 Tabela: SolicitacoesSolucoes

**Descrição:** Soluções aplicadas em chamados (base de conhecimento).

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| ClienteId | UNIQUEIDENTIFIER | NÃO | - | FK para Cliente (multi-tenancy raiz)s |
| Titulo | NVARCHAR(300) | NÃO | - | Título da solução |
| Descricao | NVARCHAR(MAX) | NÃO | - | Descrição detalhada |
| FlBaseConhecimento | BIT | NÃO | 0 | Se está disponível para consulta |
| QtdUtilizacoes | INT | NÃO | 0 | Quantas vezes foi reutilizada |
| NotaMedia | DECIMAL(3,2) | NÃO | 0.00 | Avaliação média (0 a 5) |
| CreatedAt | DATETIME2 | NÃO | GETDATE() | Data de criação |
| CreatedBy | UNIQUEIDENTIFIER | NÃO | - | Usuário que criou |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| PK_SolicitacoesSolucoes | Id | CLUSTERED | Chave primária |
| IX_SolicitacoesSolucoes_FlBaseConhecimento | FlBaseConhecimento | NONCLUSTERED FILTERED | Base de conhecimento (WHERE FlBaseConhecimento = 1) |
| IX_SolicitacoesSolucoes_QtdUtilizacoes | QtdUtilizacoes DESC | NONCLUSTERED | Ordenação por popularidade |

---

### 2.7 Tabela: ChamadosHistory

**Descrição:** Histórico de alterações em chamados (auditoria 7 anos LGPD).

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| ChamadoId | UNIQUEIDENTIFIER | NÃO | - | FK para Chamados |
| ClienteId | UNIQUEIDENTIFIER | NÃO | - | FK para Cliente (multi-tenancy raiz)s |
| Operation | NVARCHAR(20) | NÃO | - | INSERT, UPDATE, DELETE |
| OldValues | NVARCHAR(MAX) | SIM | NULL | JSON com valores anteriores |
| NewValues | NVARCHAR(MAX) | SIM | NULL | JSON com novos valores |
| ChangedBy | UNIQUEIDENTIFIER | NÃO | - | Usuário que fez alteração |
| ChangedAt | DATETIME2 | NÃO | GETDATE() | Timestamp da alteração |
| IPAddress | NVARCHAR(50) | SIM | NULL | IP de origem |
| UserAgent | NVARCHAR(500) | SIM | NULL | User Agent |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| PK_ChamadosHistory | Id | CLUSTERED | Chave primária |
| IX_ChamadosHistory_ChamadoId | ChamadoId, ChangedAt DESC | NONCLUSTERED | Histórico de um chamado |
| IX_ChamadosHistory_ConglomeradoId | ClienteId | NONCLUSTERED | Performance multi-tenant |
| IX_ChamadosHistory_ChangedAt | ChangedAt DESC | NONCLUSTERED | Auditoria temporal |

---

## 3. Relacionamentos

| Tabela Origem | Cardinalidade | Tabela Destino | Descrição |
|---------------|---------------|----------------|-----------|
| Conglomerados | 1:N | Chamados | Conglomerado possui muitos chamados |
| Users | 1:N | Chamados (Solicitante) | Usuário abre chamados |
| Users | 1:N | Chamados (Atendente) | Técnico atende chamados |
| TiposSolicitacao | 1:N | Chamados | Tipo possui muitos chamados |
| FilasAtendimento | 1:N | Chamados | Fila possui muitos chamados |
| Chamados | 1:N | ChamadosItens | Chamado possui múltiplas interações |
| Chamados | 1:N | ChamadosAnexos | Chamado possui múltiplos anexos |
| ChamadosItens | 1:N | ChamadosAnexos | Comentário pode ter anexos |
| SolicitacoesSolucoes | 1:N | Chamados | Solução aplicada em múltiplos chamados |
| Chamados | 1:N | ChamadosHistory | Chamado possui histórico de alterações |

---

## 4. DDL - SQL Server

```sql
-- =============================================
-- RF033 - Gestão de Chamados (Service Desk)
-- Modelo de Dados
-- Data: 2025-12-18
-- =============================================

-- ---------------------------------------------
-- Tabela: Chamados
-- ---------------------------------------------
CREATE TABLE [dbo].[Chamados] (
    [Id] UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    [ConglomeradoId] UNIQUEIDENTIFIER NOT NULL,
    [Titulo] NVARCHAR(300) NOT NULL,
    [Descricao] NVARCHAR(MAX) NOT NULL,
    [UsuarioSolicitanteId] UNIQUEIDENTIFIER NOT NULL,
    [UsuarioAtendenteId] UNIQUEIDENTIFIER NULL,
    [TipoSolicitacaoId] UNIQUEIDENTIFIER NOT NULL,
    [TipoAtivoId] UNIQUEIDENTIFIER NOT NULL,
    [FilaAtendimentoId] UNIQUEIDENTIFIER NOT NULL,
    [Status] INT NOT NULL DEFAULT 1,
    [Prioridade] INT NOT NULL DEFAULT 2,
    [DataSolicitacao] DATETIME2 NOT NULL DEFAULT GETDATE(),
    [DataVencimento] DATETIME2 NOT NULL,
    [DataEncerramento] DATETIME2 NULL,
    [DataInicioAguardando] DATETIME2 NULL,
    [TotalHorasAguardando] INT NOT NULL DEFAULT 0,
    [SolucaoId] UNIQUEIDENTIFIER NULL,
    [Avaliacao] INT NULL,
    [ComentarioAvaliacao] NVARCHAR(500) NULL,
    [FlEscalado] BIT NOT NULL DEFAULT 0,
    [DataEscalacao] DATETIME2 NULL,
    [AtivoId] UNIQUEIDENTIFIER NULL,
    [ConsumidorUnidadeId] UNIQUEIDENTIFIER NULL,
    [FlExcluido] BIT NOT NULL DEFAULT 0,
    [CreatedAt] DATETIME2 NOT NULL DEFAULT GETDATE(),
    [CreatedBy] UNIQUEIDENTIFIER NOT NULL,
    [UpdatedAt] DATETIME2 NULL,
    [UpdatedBy] UNIQUEIDENTIFIER NULL,

    -- Primary Key
    CONSTRAINT [PK_Chamados] PRIMARY KEY CLUSTERED ([Id] ASC),

    -- Foreign Keys
    CONSTRAINT [FK_Chamados_Conglomerado]
        FOREIGN KEY ([ConglomeradoId]) REFERENCES [dbo].[Conglomerados]([Id]),
    CONSTRAINT [FK_Chamados_UsuarioSolicitante]
        FOREIGN KEY ([UsuarioSolicitanteId]) REFERENCES [dbo].[Users]([Id]),
    CONSTRAINT [FK_Chamados_UsuarioAtendente]
        FOREIGN KEY ([UsuarioAtendenteId]) REFERENCES [dbo].[Users]([Id]),
    CONSTRAINT [FK_Chamados_TipoSolicitacao]
        FOREIGN KEY ([TipoSolicitacaoId]) REFERENCES [dbo].[TiposSolicitacao]([Id]),
    CONSTRAINT [FK_Chamados_TipoAtivo]
        FOREIGN KEY ([TipoAtivoId]) REFERENCES [dbo].[TiposAtivo]([Id]),
    CONSTRAINT [FK_Chamados_FilaAtendimento]
        FOREIGN KEY ([FilaAtendimentoId]) REFERENCES [dbo].[FilasAtendimento]([Id]),
    CONSTRAINT [FK_Chamados_Solucao]
        FOREIGN KEY ([SolucaoId]) REFERENCES [dbo].[SolicitacoesSolucoes]([Id]),
    CONSTRAINT [FK_Chamados_Ativo]
        FOREIGN KEY ([AtivoId]) REFERENCES [dbo].[Ativos]([Id]),
    CONSTRAINT [FK_Chamados_ConsumidorUnidade]
        FOREIGN KEY ([ConsumidorUnidadeId]) REFERENCES [dbo].[ConsumidoresUnidades]([Id]),
    CONSTRAINT [FK_Chamados_CreatedBy]
        FOREIGN KEY ([CreatedBy]) REFERENCES [dbo].[Users]([Id]),
    CONSTRAINT [FK_Chamados_UpdatedBy]
        FOREIGN KEY ([UpdatedBy]) REFERENCES [dbo].[Users]([Id]),

    -- Check Constraints
    CONSTRAINT [CK_Chamados_Status]
        CHECK ([Status] BETWEEN 1 AND 7),
    CONSTRAINT [CK_Chamados_Prioridade]
        CHECK ([Prioridade] BETWEEN 1 AND 4),
    CONSTRAINT [CK_Chamados_Avaliacao]
        CHECK ([Avaliacao] IS NULL OR ([Avaliacao] BETWEEN 1 AND 5)),
    CONSTRAINT [CK_Chamados_DataVencimento]
        CHECK ([DataVencimento] >= [DataSolicitacao]),
    CONSTRAINT [CK_Chamados_DataEncerramento]
        CHECK ([DataEncerramento] IS NULL OR [DataEncerramento] >= [DataSolicitacao])
);
GO

-- Índices (14 índices otimizados)
CREATE NONCLUSTERED INDEX [IX_Chamados_ConglomeradoId]
    ON [dbo].[Chamados]([ConglomeradoId])
    WHERE [FlExcluido] = 0;
GO

CREATE NONCLUSTERED INDEX [IX_Chamados_Status_DataVencimento]
    ON [dbo].[Chamados]([Status], [DataVencimento])
    INCLUDE ([Titulo], [Prioridade], [UsuarioAtendenteId])
    WHERE [FlExcluido] = 0;
GO

CREATE NONCLUSTERED INDEX [IX_Chamados_UsuarioSolicitanteId]
    ON [dbo].[Chamados]([UsuarioSolicitanteId])
    WHERE [FlExcluido] = 0;
GO

CREATE NONCLUSTERED INDEX [IX_Chamados_UsuarioAtendenteId]
    ON [dbo].[Chamados]([UsuarioAtendenteId])
    WHERE [FlExcluido] = 0 AND [UsuarioAtendenteId] IS NOT NULL;
GO

CREATE NONCLUSTERED INDEX [IX_Chamados_FilaAtendimentoId]
    ON [dbo].[Chamados]([FilaAtendimentoId])
    WHERE [FlExcluido] = 0;
GO

CREATE NONCLUSTERED INDEX [IX_Chamados_TipoSolicitacaoId]
    ON [dbo].[Chamados]([TipoSolicitacaoId])
    WHERE [FlExcluido] = 0;
GO

CREATE NONCLUSTERED INDEX [IX_Chamados_DataSolicitacao]
    ON [dbo].[Chamados]([DataSolicitacao] DESC)
    WHERE [FlExcluido] = 0;
GO

CREATE NONCLUSTERED INDEX [IX_Chamados_Prioridade]
    ON [dbo].[Chamados]([Prioridade] DESC)
    WHERE [FlExcluido] = 0;
GO

CREATE NONCLUSTERED INDEX [IX_Chamados_FlEscalado]
    ON [dbo].[Chamados]([FlEscalado])
    WHERE [FlEscalado] = 1 AND [FlExcluido] = 0;
GO

CREATE NONCLUSTERED INDEX [IX_Chamados_SLA_Vencido]
    ON [dbo].[Chamados]([DataVencimento])
    WHERE [DataVencimento] < GETDATE() AND [Status] NOT IN (6, 7) AND [FlExcluido] = 0;
GO

CREATE NONCLUSTERED INDEX [IX_Chamados_AtivoId]
    ON [dbo].[Chamados]([AtivoId])
    WHERE [FlExcluido] = 0 AND [AtivoId] IS NOT NULL;
GO

CREATE NONCLUSTERED INDEX [IX_Chamados_CreatedAt]
    ON [dbo].[Chamados]([CreatedAt] DESC)
    WHERE [FlExcluido] = 0;
GO

CREATE NONCLUSTERED INDEX [IX_Chamados_Composto_Dashboard]
    ON [dbo].[Chamados]([ConglomeradoId], [Status], [DataVencimento])
    INCLUDE ([Titulo], [Prioridade], [UsuarioAtendenteId])
    WHERE [FlExcluido] = 0;
GO

-- Comentários
EXEC sys.sp_addextendedproperty
    @name=N'MS_Description',
    @value=N'Tabela principal de chamados (tickets) do Service Desk',
    @level0type=N'SCHEMA', @level0name=N'dbo',
    @level1type=N'TABLE',  @level1name=N'Chamados';
GO


-- ---------------------------------------------
-- Tabelas auxiliares (simplificadas)
-- ---------------------------------------------
CREATE TABLE [dbo].[ChamadosItens] (
    [Id] UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    [ChamadoId] UNIQUEIDENTIFIER NOT NULL,
    [Descricao] NVARCHAR(MAX) NOT NULL,
    [UsuarioId] UNIQUEIDENTIFIER NOT NULL,
    [DataHora] DATETIME2 NOT NULL DEFAULT GETDATE(),
    [FlPublico] BIT NOT NULL DEFAULT 1,
    [TipoItem] INT NOT NULL DEFAULT 1,
    [FlExcluido] BIT NOT NULL DEFAULT 0,

    CONSTRAINT [PK_ChamadosItens] PRIMARY KEY CLUSTERED ([Id] ASC),
    CONSTRAINT [FK_ChamadosItens_Chamado] FOREIGN KEY ([ChamadoId]) REFERENCES [dbo].[Chamados]([Id]),
    CONSTRAINT [FK_ChamadosItens_Usuario] FOREIGN KEY ([UsuarioId]) REFERENCES [dbo].[Users]([Id]),
    CONSTRAINT [CK_ChamadosItens_TipoItem] CHECK ([TipoItem] BETWEEN 1 AND 4)
);
GO

CREATE NONCLUSTERED INDEX [IX_ChamadosItens_ChamadoId]
    ON [dbo].[ChamadosItens]([ChamadoId], [DataHora] DESC)
    WHERE [FlExcluido] = 0;
GO

CREATE TABLE [dbo].[ChamadosAnexos] (
    [Id] UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    [ChamadoId] UNIQUEIDENTIFIER NOT NULL,
    [ChamadoItemId] UNIQUEIDENTIFIER NULL,
    [NomeArquivo] NVARCHAR(500) NOT NULL,
    [TamanhoBytes] BIGINT NOT NULL,
    [TipoConteudo] NVARCHAR(100) NOT NULL,
    [URLArquivo] NVARCHAR(1000) NOT NULL,
    [HashSHA256] NVARCHAR(64) NOT NULL,
    [FlExcluido] BIT NOT NULL DEFAULT 0,
    [CreatedAt] DATETIME2 NOT NULL DEFAULT GETDATE(),
    [CreatedBy] UNIQUEIDENTIFIER NOT NULL,

    CONSTRAINT [PK_ChamadosAnexos] PRIMARY KEY CLUSTERED ([Id] ASC),
    CONSTRAINT [FK_ChamadosAnexos_Chamado] FOREIGN KEY ([ChamadoId]) REFERENCES [dbo].[Chamados]([Id]),
    CONSTRAINT [FK_ChamadosAnexos_ChamadoItem] FOREIGN KEY ([ChamadoItemId]) REFERENCES [dbo].[ChamadosItens]([Id]),
    CONSTRAINT [FK_ChamadosAnexos_CreatedBy] FOREIGN KEY ([CreatedBy]) REFERENCES [dbo].[Users]([Id]),
    CONSTRAINT [CK_ChamadosAnexos_TamanhoBytes] CHECK ([TamanhoBytes] > 0 AND [TamanhoBytes] <= 10485760)
);
GO

CREATE TABLE [dbo].[ChamadosHistory] (
    [Id] UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    [ChamadoId] UNIQUEIDENTIFIER NOT NULL,
    [ConglomeradoId] UNIQUEIDENTIFIER NOT NULL,
    [Operation] NVARCHAR(20) NOT NULL,
    [OldValues] NVARCHAR(MAX) NULL,
    [NewValues] NVARCHAR(MAX) NULL,
    [ChangedBy] UNIQUEIDENTIFIER NOT NULL,
    [ChangedAt] DATETIME2 NOT NULL DEFAULT GETDATE(),
    [IPAddress] NVARCHAR(50) NULL,
    [UserAgent] NVARCHAR(500) NULL,

    CONSTRAINT [PK_ChamadosHistory] PRIMARY KEY CLUSTERED ([Id] ASC),
    CONSTRAINT [FK_ChamadosHistory_Chamado] FOREIGN KEY ([ChamadoId]) REFERENCES [dbo].[Chamados]([Id]),
    CONSTRAINT [FK_ChamadosHistory_Conglomerado] FOREIGN KEY ([ConglomeradoId]) REFERENCES [dbo].[Conglomerados]([Id]),
    CONSTRAINT [FK_ChamadosHistory_ChangedBy] FOREIGN KEY ([ChangedBy]) REFERENCES [dbo].[Users]([Id])
);
GO

CREATE NONCLUSTERED INDEX [IX_ChamadosHistory_ChamadoId]
    ON [dbo].[ChamadosHistory]([ChamadoId], [ChangedAt] DESC);
GO
```

---

## 5. Views Úteis

```sql
-- =============================================
-- View: Chamados com SLA Calculado
-- =============================================
CREATE VIEW [dbo].[vw_Chamados_SLA]
AS
SELECT
    c.[Id],
    c.[Titulo],
    c.[Status],
    c.[Prioridade],
    c.[DataSolicitacao],
    c.[DataVencimento],
    DATEDIFF(HOUR, c.[DataSolicitacao], GETDATE()) - c.[TotalHorasAguardando] AS HorasDecorridas,
    DATEDIFF(HOUR, c.[DataSolicitacao], c.[DataVencimento]) AS TotalHorasSLA,
    CASE
        WHEN c.[Status] IN (6, 7) THEN 'ENCERRADO'
        WHEN GETDATE() > c.[DataVencimento] THEN 'VENCIDO'
        WHEN DATEDIFF(HOUR, GETDATE(), c.[DataVencimento]) <= 2 THEN 'CRÍTICO'
        WHEN DATEDIFF(HOUR, GETDATE(), c.[DataVencimento]) <= 8 THEN 'ALERTA'
        ELSE 'OK'
    END AS StatusSLA,
    CAST(
        (DATEDIFF(HOUR, c.[DataSolicitacao], GETDATE()) - c.[TotalHorasAguardando]) * 100.0 /
        NULLIF(DATEDIFF(HOUR, c.[DataSolicitacao], c.[DataVencimento]), 0)
    AS DECIMAL(5,2)) AS PercentualSLADecorrido
FROM [dbo].[Chamados] c
WHERE c.[FlExcluido] = 0;
GO
```

---

## 6. Stored Procedures

```sql
-- =============================================
-- SP: Escalar Chamados Vencidos
-- =============================================
CREATE PROCEDURE [dbo].[sp_EscalarChamadosVencidos]
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @ChamadosEscalados TABLE (Id UNIQUEIDENTIFIER);

    UPDATE c
    SET
        c.[FlEscalado] = 1,
        c.[DataEscalacao] = GETDATE(),
        c.[UpdatedAt] = GETDATE()
    OUTPUT INSERTED.[Id] INTO @ChamadosEscalados
    FROM [dbo].[Chamados] c
    WHERE c.[DataVencimento] < GETDATE()
      AND c.[Status] NOT IN (6, 7) -- Não encerrado/cancelado
      AND c.[FlEscalado] = 0
      AND c.[FlExcluido] = 0;

    SELECT COUNT(*) AS QtdEscalados FROM @ChamadosEscalados;
END;
GO
```

---

## 7. Observações

### Decisões de Modelagem

1. **Status como INT (enum)**: Facilita validações e evita erros de digitação. Enum no backend mapeia para INT.

2. **TotalHorasAguardando acumulado**: Permite cálculo preciso de SLA real (pausas em "Aguardando").

3. **ChamadosItens com TipoItem**: Diferencia comentários de ações automáticas (mudança de status, reatribuição).

4. **Índices filtrados**: Melhoram performance em queries específicas (SLA vencido, escalados).

5. **HashSHA256 em anexos**: Garante integridade e detecta duplicação de arquivos.

### Indicadores de Performance

- 14 índices na tabela Chamados (otimização para dashboard, "meus chamados", SLA).
- Índice composto (ConglomeradoId, Status, DataVencimento) com INCLUDE para query de dashboard sem table scan.
- Índices filtrados WHERE FlExcluido = 0 reduzem tamanho e melhoram performance.

### Migração do Legado

Mapear `Solicitacao` → `Chamados`, `Solicitacao_Item` → `ChamadosItens`, `Solicitacao_Avaliacao` → `Chamados.Avaliacao`.

---

## Histórico de Alterações

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 1.0 | 2025-12-18 | Architect Agent | Versão inicial - 7 tabelas, 47 índices |
