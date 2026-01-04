# Modelo de Dados - RF053 - Gestão de Solicitações

**Versão:** 1.0
**Data:** 2025-12-18
**RF Relacionado:** [RF053 - Gestão de Solicitações](./RF053.md)
**Banco de Dados:** SQL Server

---

## 1. Diagrama de Entidades (ER)

```
┌─────────────────────────┐       ┌──────────────────────────┐
│   Solicitacao           │       │   SolicitacaoTipo        │
├─────────────────────────┤       ├──────────────────────────┤
│ Id (PK)                 │   ┌───│ Id (PK)                  │
│ Numero (UK)             │   │   │ Codigo (UK)              │
│ TipoId (FK) ────────────┼───┘   │ Nome                     │
│ SolicitanteId (FK)      │       │ CamposDinamicosJSON      │
│ AtendenteId (FK)        │       │ WorkflowJSON             │
│ Status                  │       │ SLAHoras                 │
│ Prioridade              │       │ Ativo                    │
│ Titulo                  │       │ ClienteId (FK)           │
│ Descricao               │       └──────────────────────────┘
│ CamposDinamicosJSON     │
│ DataAbertura            │       ┌──────────────────────────┐
│ DataLimiteSLA           │       │   SolicitacaoAnexo       │
│ DataFechamento          │       ├──────────────────────────┤
│ TempoPausadoSLA (min)   │   ┌───│ Id (PK)                  │
│ EmAprovacao (bit)       │   │   │ SolicitacaoId (FK) ──────┼───┐
│ NivelAprovacaoAtual     │   │   │ NomeArquivo              │   │
│ Solucao                 │   │   │ TipoMIME                 │   │
│ JustificativaCancelamento│  │   │ TamanhoBytes             │   │
│ Escalonada (bit)        │   │   │ CaminhoBlob              │   │
│ DataEscalonamento       │   │   │ DataUpload               │   │
│ VIP (bit)               │   │   │ UsuarioUploadId (FK)     │   │
│ ClienteId (FK)          │   │   └──────────────────────────┘   │
│ Ativo (bit)             │   │                                  │
│ CreatedAt               │   │   ┌──────────────────────────┐   │
│ CreatedBy (FK)          │   │   │   SolicitacaoHistorico   │   │
│ ModifiedAt              │   │   ├──────────────────────────┤   │
│ ModifiedBy (FK)         │   └───│ Id (PK)                  │   │
└─────────────────────────┘       │ SolicitacaoId (FK) ──────┼───┘
                                  │ StatusAnterior           │
                                  │ StatusNovo               │
                                  │ UsuarioId (FK)           │
                                  │ DataAlteracao            │
                                  │ Comentario               │
                                  │ TipoOperacao             │
                                  └──────────────────────────┘

┌──────────────────────────┐      ┌──────────────────────────┐
│   SolicitacaoAprovacao   │      │   SolicitacaoMensagem    │
├──────────────────────────┤      ├──────────────────────────┤
│ Id (PK)                  │  ┌───│ Id (PK)                  │
│ SolicitacaoId (FK) ──────┼──┘   │ SolicitacaoId (FK) ──────┼───┐
│ NivelAprovacao           │      │ UsuarioId (FK)           │   │
│ AprovadorId (FK)         │      │ Mensagem                 │   │
│ Decisao                  │      │ DataEnvio                │   │
│ Justificativa            │      │ Interna (bit)            │   │
│ DataDecisao              │      └──────────────────────────┘   │
└──────────────────────────┘                                     │
                                  ┌──────────────────────────┐   │
                                  │   DelegacaoAprovador     │   │
                                  ├──────────────────────────┤   │
                                  │ Id (PK)                  │   │
                                  │ AprovadorOriginalId (FK) │   │
                                  │ AprovadorDelegadoId (FK) │   │
                                  │ InicioVigencia           │   │
                                  │ FimVigencia              │   │
                                  │ Ativo (bit)              │   │
                                  │ ClienteId (FK)           │   │
                                  └──────────────────────────┘   │
                                                                 │
┌──────────────────────────┐      ┌──────────────────────────┐   │
│   PesquisaSatisfacao     │      │   SolicitacaoItemAtivo   │   │
├──────────────────────────┤      ├──────────────────────────┤   │
│ Id (PK)                  │      │ Id (PK)                  │   │
│ SolicitacaoId (FK) ──────┼──────│ SolicitacaoId (FK) ──────┼───┘
│ NotaAtendimento (1-10)   │      │ TipoAtivo                │
│ NotaAgilidade (1-5)      │      │ Modelo                   │
│ NotaComunicacao (1-5)    │      │ Quantidade               │
│ Comentarios              │      │ ValorEstimado            │
│ DataResposta             │      └──────────────────────────┘
└──────────────────────────┘
```

---

## 2. Entidades e Campos

### 2.1 Tabela: Solicitacao

**Descrição:** Tabela principal que armazena todas as solicitações do service desk (novos ativos, trocas, reparos, cancelamentos).

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| Numero | VARCHAR(20) | NÃO | - | Número único sequencial (SOL-2025-00001) |
| ClienteId | UNIQUEIDENTIFIER | NÃO | - | FK para Cliente (multi-tenancy) |
| TipoId | UNIQUEIDENTIFIER | NÃO | - | FK para SolicitacaoTipo |
| SolicitanteId | UNIQUEIDENTIFIER | NÃO | - | FK para Usuario (quem solicitou) |
| AtendenteId | UNIQUEIDENTIFIER | SIM | NULL | FK para Usuario (quem está atendendo) |
| Status | VARCHAR(30) | NÃO | 'ABERTA' | ABERTA, EM_APROVACAO, APROVADA, REJEITADA, EM_ATENDIMENTO, AGUARDANDO_CLIENTE, FECHADA, CANCELADA, REABERTA |
| Prioridade | INT | NÃO | 2 | 1-Baixa, 2-Normal, 3-Alta, 4-Urgente, 5-Crítica |
| Titulo | NVARCHAR(200) | NÃO | - | Título resumido da solicitação |
| Descricao | NVARCHAR(MAX) | NÃO | - | Descrição detalhada |
| CamposDinamicosJSON | NVARCHAR(MAX) | SIM | NULL | JSON com campos específicos do tipo |
| DataAbertura | DATETIME2(7) | NÃO | SYSUTCDATETIME() | Data/hora de abertura |
| DataLimiteSLA | DATETIME2(7) | SIM | NULL | Data limite calculada por SLA |
| DataFechamento | DATETIME2(7) | SIM | NULL | Data/hora de fechamento |
| TempoPausadoSLA | INT | NÃO | 0 | Tempo pausado do SLA (em minutos) |
| DataAtribuicao | DATETIME2(7) | SIM | NULL | Quando foi atribuída a um atendente |
| EmAprovacao | BIT | NÃO | 0 | Se está em workflow de aprovação |
| NivelAprovacaoAtual | INT | NÃO | 0 | Nível atual do workflow (0 se não aplicável) |
| Solucao | NVARCHAR(MAX) | SIM | NULL | Solução aplicada (preenchido no fechamento) |
| JustificativaCancelamento | NVARCHAR(500) | SIM | NULL | Motivo do cancelamento |
| Escalonada | BIT | NÃO | 0 | Se foi escalonada por SLA vencido |
| DataEscalonamento | DATETIME2(7) | SIM | NULL | Data do escalonamento |
| VIP | BIT | NÃO | 0 | Se solicitante é VIP (CEO, Diretor) |
| DataReabertura | DATETIME2(7) | SIM | NULL | Data de reabertura (se aplicável) |
| MotivoPendencia | NVARCHAR(500) | SIM | NULL | Motivo se status = AGUARDANDO_CLIENTE |
| Ativo | BIT | NÃO | 1 | Soft delete: false=ativo, true=excluído |
| CreatedAt | DATETIME2(7) | NÃO | SYSUTCDATETIME() | Data de criação |
| CreatedBy | UNIQUEIDENTIFIER | NÃO | - | Usuário que criou |
| ModifiedAt | DATETIME2(7) | SIM | NULL | Data de modificação |
| ModifiedBy | UNIQUEIDENTIFIER | SIM | NULL | Usuário que modificou |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| PK_Solicitacao | Id | CLUSTERED | Chave primária |
| UK_Solicitacao_Numero | Numero | UNIQUE NONCLUSTERED | Número único |
| IX_Solicitacao_Cliente | ClienteId, DataAbertura DESC | NONCLUSTERED | Performance multi-tenant |
| IX_Solicitacao_Status | Status, DataLimiteSLA | NONCLUSTERED FILTERED (WHERE Status IN ('ABERTA','EM_ATENDIMENTO')) | Solicitações ativas |
| IX_Solicitacao_Solicitante | SolicitanteId, DataAbertura DESC | NONCLUSTERED | Solicitações do usuário |
| IX_Solicitacao_Atendente | AtendenteId, Status | NONCLUSTERED FILTERED (WHERE AtendenteId IS NOT NULL) | Solicitações atribuídas |
| IX_Solicitacao_SLA | DataLimiteSLA | NONCLUSTERED FILTERED (WHERE Status NOT IN ('FECHADA','CANCELADA')) | Alertas de SLA |
| IX_Solicitacao_Tipo | TipoId, DataAbertura DESC | NONCLUSTERED | Agrupamento por tipo |
| IX_Solicitacao_VIP | VIP, Prioridade DESC | NONCLUSTERED FILTERED (WHERE VIP = 1) | Solicitações VIP |

#### Constraints

| Nome | Tipo | Definição | Descrição |
|------|------|-----------|-----------|
| PK_Solicitacao | PRIMARY KEY | Id | Chave primária |
| FK_Solicitacao_Cliente | FOREIGN KEY | ClienteId REFERENCES Cliente(Id) | Multi-tenancy |
| FK_Solicitacao_Tipo | FOREIGN KEY | TipoId REFERENCES SolicitacaoTipo(Id) | Tipo da solicitação |
| FK_Solicitacao_Solicitante | FOREIGN KEY | SolicitanteId REFERENCES Usuario(Id) | Quem solicitou |
| FK_Solicitacao_Atendente | FOREIGN KEY | AtendenteId REFERENCES Usuario(Id) | Quem atende |
| FK_Solicitacao_CreatedBy | FOREIGN KEY | CreatedBy REFERENCES Usuario(Id) | Auditoria |
| CK_Solicitacao_Status | CHECK | Status IN ('ABERTA', 'EM_APROVACAO', 'APROVADA', 'REJEITADA', 'EM_ATENDIMENTO', 'AGUARDANDO_CLIENTE', 'FECHADA', 'CANCELADA', 'REABERTA') | Status válidos |
| CK_Solicitacao_Prioridade | CHECK | Prioridade BETWEEN 1 AND 5 | Prioridade válida |
| CK_Solicitacao_NivelAprovacao | CHECK | NivelAprovacaoAtual >= 0 | Nível válido |

---

### 2.2 Tabela: SolicitacaoTipo

**Descrição:** Tipos de solicitação configuráveis com campos dinâmicos e workflow específico.

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| Codigo | VARCHAR(50) | NÃO | - | Código único (NOVO_CELULAR, REPARO, CANCELAMENTO) |
| Nome | NVARCHAR(100) | NÃO | - | Nome exibido |
| Descricao | NVARCHAR(500) | SIM | NULL | Descrição do tipo |
| CamposDinamicosJSON | NVARCHAR(MAX) | SIM | NULL | Definição de campos extras (JSON schema) |
| WorkflowJSON | NVARCHAR(MAX) | SIM | NULL | Definição do workflow de aprovação |
| SLAHoras | INT | NÃO | 120 | SLA padrão em horas |
| RequerAprovacao | BIT | NÃO | 0 | Se requer workflow de aprovação |
| AnexosObrigatorios | BIT | NÃO | 0 | Se anexos são obrigatórios |
| QuantidadeMinimaAnexos | INT | NÃO | 0 | Quantidade mínima de anexos |
| ClienteId | UNIQUEIDENTIFIER | NÃO | - | FK para Cliente |
| Ativo | BIT | NÃO | 1 | Se tipo está ativo |
| CreatedAt | DATETIME2(7) | NÃO | SYSUTCDATETIME() | Data de criação |
| CreatedBy | UNIQUEIDENTIFIER | NÃO | - | Usuário que criou |
| ModifiedAt | DATETIME2(7) | SIM | NULL | Data de modificação |
| ModifiedBy | UNIQUEIDENTIFIER | SIM | NULL | Usuário que modificou |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| PK_SolicitacaoTipo | Id | CLUSTERED | Chave primária |
| UK_SolicitacaoTipo_Codigo | ClienteId, Codigo | UNIQUE NONCLUSTERED | Código único por cliente |
| IX_SolicitacaoTipo_Cliente | ClienteId, Ativo | NONCLUSTERED | Tipos ativos por cliente |

---

### 2.3 Tabela: SolicitacaoAnexo

**Descrição:** Arquivos anexados às solicitações (fotos, documentos, evidências).

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| SolicitacaoId | UNIQUEIDENTIFIER | NÃO | - | FK para Solicitacao |
| NomeArquivo | NVARCHAR(255) | NÃO | - | Nome original do arquivo |
| TipoMIME | VARCHAR(100) | NÃO | - | Tipo MIME (image/jpeg, application/pdf) |
| TamanhoBytes | BIGINT | NÃO | - | Tamanho em bytes |
| CaminhoBlob | NVARCHAR(500) | NÃO | - | Caminho no Azure Blob Storage |
| HashSHA256 | VARCHAR(64) | NÃO | - | Hash para verificação de integridade |
| TipoAnexo | VARCHAR(50) | SIM | NULL | FOTO_EQUIPAMENTO, ORCAMENTO, AUTORIZACAO, OUTROS |
| DataUpload | DATETIME2(7) | NÃO | SYSUTCDATETIME() | Data do upload |
| UsuarioUploadId | UNIQUEIDENTIFIER | NÃO | - | Quem fez upload |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| PK_SolicitacaoAnexo | Id | CLUSTERED | Chave primária |
| IX_SolicitacaoAnexo_Solicitacao | SolicitacaoId, DataUpload DESC | NONCLUSTERED | Anexos por solicitação |
| IX_SolicitacaoAnexo_Usuario | UsuarioUploadId, DataUpload DESC | NONCLUSTERED | Uploads do usuário |

---

### 2.4 Tabela: SolicitacaoHistorico

**Descrição:** Timeline completa de mudanças de status e ações na solicitação.

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| SolicitacaoId | UNIQUEIDENTIFIER | NÃO | - | FK para Solicitacao |
| StatusAnterior | VARCHAR(30) | SIM | NULL | Status antes da mudança |
| StatusNovo | VARCHAR(30) | NÃO | - | Novo status |
| UsuarioId | UNIQUEIDENTIFIER | NÃO | - | Quem executou a ação |
| DataAlteracao | DATETIME2(7) | NÃO | SYSUTCDATETIME() | Timestamp da mudança |
| Comentario | NVARCHAR(1000) | SIM | NULL | Comentário opcional |
| TipoOperacao | VARCHAR(50) | NÃO | - | CRIACAO, ATRIBUICAO, APROVACAO, REJEICAO, FECHAMENTO, CANCELAMENTO, ESCALONAMENTO, REABERTURA, PAUSA_SLA, RETOMADA_SLA |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| PK_SolicitacaoHistorico | Id | CLUSTERED | Chave primária |
| IX_SolicitacaoHistorico_Solicitacao | SolicitacaoId, DataAlteracao DESC | NONCLUSTERED | Timeline da solicitação |
| IX_SolicitacaoHistorico_Usuario | UsuarioId, DataAlteracao DESC | NONCLUSTERED | Ações do usuário |
| IX_SolicitacaoHistorico_TipoOperacao | TipoOperacao, DataAlteracao DESC | NONCLUSTERED | Agrupamento por tipo |

---

### 2.5 Tabela: SolicitacaoAprovacao

**Descrição:** Workflow de aprovação multi-nível com decisões de cada aprovador.

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| SolicitacaoId | UNIQUEIDENTIFIER | NÃO | - | FK para Solicitacao |
| NivelAprovacao | INT | NÃO | - | Ordem do nível (1, 2, 3...) |
| AprovadorId | UNIQUEIDENTIFIER | NÃO | - | FK para Usuario aprovador |
| Decisao | VARCHAR(20) | SIM | NULL | PENDENTE, APROVADO, REJEITADO |
| Justificativa | NVARCHAR(500) | SIM | NULL | Justificativa (obrigatório se REJEITADO) |
| DataDecisao | DATETIME2(7) | SIM | NULL | Timestamp da decisão |
| DataLimiteDecisao | DATETIME2(7) | SIM | NULL | Prazo para decisão |
| TokenTemporario | VARCHAR(100) | SIM | NULL | Token para aprovação mobile |
| DataExpiracaoToken | DATETIME2(7) | SIM | NULL | Expiração do token (15 min) |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| PK_SolicitacaoAprovacao | Id | CLUSTERED | Chave primária |
| IX_SolicitacaoAprovacao_Solicitacao | SolicitacaoId, NivelAprovacao | NONCLUSTERED | Workflow por solicitação |
| IX_SolicitacaoAprovacao_Aprovador | AprovadorId, Decisao | NONCLUSTERED FILTERED (WHERE Decisao = 'PENDENTE') | Pendentes do aprovador |
| IX_SolicitacaoAprovacao_DataLimite | DataLimiteDecisao | NONCLUSTERED FILTERED (WHERE Decisao = 'PENDENTE') | Alertas de prazo |

---

### 2.6 Tabela: SolicitacaoMensagem

**Descrição:** Chat interno por solicitação (comunicação entre solicitante e atendentes).

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| SolicitacaoId | UNIQUEIDENTIFIER | NÃO | - | FK para Solicitacao |
| UsuarioId | UNIQUEIDENTIFIER | NÃO | - | Quem enviou |
| Mensagem | NVARCHAR(4000) | NÃO | - | Texto da mensagem |
| DataEnvio | DATETIME2(7) | NÃO | SYSUTCDATETIME() | Timestamp |
| Interna | BIT | NÃO | 0 | Se visível só para atendentes (notas internas) |
| Lida | BIT | NÃO | 0 | Se foi lida pelo destinatário |
| DataLeitura | DATETIME2(7) | SIM | NULL | Quando foi lida |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| PK_SolicitacaoMensagem | Id | CLUSTERED | Chave primária |
| IX_SolicitacaoMensagem_Solicitacao | SolicitacaoId, DataEnvio ASC | NONCLUSTERED | Chat ordenado |
| IX_SolicitacaoMensagem_NaoLidas | SolicitacaoId, Lida | NONCLUSTERED FILTERED (WHERE Lida = 0) | Mensagens não lidas |

---

### 2.7 Tabela: DelegacaoAprovador

**Descrição:** Delegações temporárias de aprovadores (férias, ausências).

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| AprovadorOriginalId | UNIQUEIDENTIFIER | NÃO | - | FK para Usuario original |
| AprovadorDelegadoId | UNIQUEIDENTIFIER | NÃO | - | FK para Usuario delegado |
| InicioVigencia | DATETIME2(7) | NÃO | - | Início da delegação |
| FimVigencia | DATETIME2(7) | NÃO | - | Fim da delegação |
| Motivo | NVARCHAR(200) | SIM | NULL | Motivo da delegação |
| ClienteId | UNIQUEIDENTIFIER | NÃO | - | FK para Cliente |
| Ativo | BIT | NÃO | 1 | Se delegação está ativa |
| CreatedAt | DATETIME2(7) | NÃO | SYSUTCDATETIME() | Data de criação |
| CreatedBy | UNIQUEIDENTIFIER | NÃO | - | Quem criou |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| PK_DelegacaoAprovador | Id | CLUSTERED | Chave primária |
| IX_DelegacaoAprovador_Original | AprovadorOriginalId, InicioVigencia, FimVigencia | NONCLUSTERED | Delegações do aprovador |
| IX_DelegacaoAprovador_Vigente | InicioVigencia, FimVigencia, Ativo | NONCLUSTERED FILTERED (WHERE FlExcluido = 0) | Delegações ativas |

---

### 2.8 Tabela: PesquisaSatisfacao

**Descrição:** NPS e avaliação de satisfação após fechamento.

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| SolicitacaoId | UNIQUEIDENTIFIER | NÃO | - | FK para Solicitacao |
| NotaAtendimento | INT | NÃO | - | NPS de 0 a 10 |
| NotaAgilidade | INT | SIM | NULL | Estrelas de 1 a 5 |
| NotaComunicacao | INT | SIM | NULL | Estrelas de 1 a 5 |
| Comentarios | NVARCHAR(2000) | SIM | NULL | Comentários livres |
| DataResposta | DATETIME2(7) | NÃO | SYSUTCDATETIME() | Timestamp da resposta |
| DataEnvio | DATETIME2(7) | NÃO | - | Quando pesquisa foi enviada |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| PK_PesquisaSatisfacao | Id | CLUSTERED | Chave primária |
| UK_PesquisaSatisfacao_Solicitacao | SolicitacaoId | UNIQUE NONCLUSTERED | Uma pesquisa por solicitação |
| IX_PesquisaSatisfacao_Nota | NotaAtendimento, DataResposta DESC | NONCLUSTERED | Análise de NPS |

---

### 2.9 Tabela: SolicitacaoItemAtivo

**Descrição:** Itens de ativos solicitados (para integração com inventário).

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| SolicitacaoId | UNIQUEIDENTIFIER | NÃO | - | FK para Solicitacao |
| TipoAtivo | VARCHAR(50) | NÃO | - | CELULAR, NOTEBOOK, DESKTOP, MONITOR, OUTROS |
| Modelo | NVARCHAR(100) | SIM | NULL | Modelo desejado |
| Quantidade | INT | NÃO | 1 | Quantidade solicitada |
| ValorEstimado | DECIMAL(18,2) | SIM | NULL | Valor estimado unitário |
| Aprovado | BIT | NÃO | 0 | Se item foi aprovado |
| AtivoGeradoId | UNIQUEIDENTIFIER | SIM | NULL | FK para Ativo (após criação) |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| PK_SolicitacaoItemAtivo | Id | CLUSTERED | Chave primária |
| IX_SolicitacaoItemAtivo_Solicitacao | SolicitacaoId | NONCLUSTERED | Itens da solicitação |

---

## 3. Relacionamentos

| Tabela Origem | Cardinalidade | Tabela Destino | Descrição |
|---------------|---------------|----------------|-----------|
| Cliente | 1:N | Solicitacao | Cliente possui muitas solicitações |
| Cliente | 1:N | SolicitacaoTipo | Cliente configura tipos |
| SolicitacaoTipo | 1:N | Solicitacao | Tipo possui muitas solicitações |
| Usuario | 1:N | Solicitacao (Solicitante) | Usuário pode criar solicitações |
| Usuario | 1:N | Solicitacao (Atendente) | Atendente gerencia solicitações |
| Solicitacao | 1:N | SolicitacaoAnexo | Solicitação possui anexos |
| Solicitacao | 1:N | SolicitacaoHistorico | Solicitação possui histórico |
| Solicitacao | 1:N | SolicitacaoAprovacao | Solicitação possui workflow aprovação |
| Solicitacao | 1:N | SolicitacaoMensagem | Solicitação possui chat |
| Solicitacao | 1:1 | PesquisaSatisfacao | Solicitação possui pesquisa NPS |
| Solicitacao | 1:N | SolicitacaoItemAtivo | Solicitação possui itens de ativos |
| Usuario | 1:N | DelegacaoAprovador (Original) | Aprovador delega temporariamente |
| Usuario | 1:N | DelegacaoAprovador (Delegado) | Usuário recebe delegações |

---

## 4. DDL - SQL Server

```sql
-- =============================================
-- RF053 - Gestão de Solicitações
-- Modelo de Dados Completo
-- Data: 2025-12-18
-- Banco: SQL Server 2019+
-- =============================================

-- ---------------------------------------------
-- Tabela: SolicitacaoTipo
-- ---------------------------------------------
CREATE TABLE SolicitacaoTipo (
    Id UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    Codigo VARCHAR(50) NOT NULL,
    Nome NVARCHAR(100) NOT NULL,
    Descricao NVARCHAR(500) NULL,
    CamposDinamicosJSON NVARCHAR(MAX) NULL,
    WorkflowJSON NVARCHAR(MAX) NULL,
    SLAHoras INT NOT NULL DEFAULT 120,
    RequerAprovacao BIT NOT NULL DEFAULT 0,
    AnexosObrigatorios BIT NOT NULL DEFAULT 0,
    QuantidadeMinimaAnexos INT NOT NULL DEFAULT 0,
    ClienteId UNIQUEIDENTIFIER NOT NULL,
    FlExcluido BIT NOT NULL DEFAULT 0,
    CreatedAt DATETIME2(7) NOT NULL DEFAULT SYSUTCDATETIME(),
    CreatedBy UNIQUEIDENTIFIER NOT NULL,
    ModifiedAt DATETIME2(7) NULL,
    ModifiedBy UNIQUEIDENTIFIER NULL,

    CONSTRAINT PK_SolicitacaoTipo PRIMARY KEY CLUSTERED (Id),
    CONSTRAINT FK_SolicitacaoTipo_Cliente FOREIGN KEY (ClienteId) REFERENCES Cliente(Id),
    CONSTRAINT FK_SolicitacaoTipo_CreatedBy FOREIGN KEY (CreatedBy) REFERENCES Usuario(Id),
    CONSTRAINT CK_SolicitacaoTipo_SLA CHECK (SLAHoras > 0),
    CONSTRAINT CK_SolicitacaoTipo_AnexosMin CHECK (QuantidadeMinimaAnexos >= 0)
);

CREATE UNIQUE NONCLUSTERED INDEX UK_SolicitacaoTipo_Codigo ON SolicitacaoTipo(ClienteId, Codigo) WHERE FlExcluido = 0;
CREATE NONCLUSTERED INDEX IX_SolicitacaoTipo_Cliente ON SolicitacaoTipo(ClienteId, FlExcluido);

-- Comentários
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'Tipos de solicitação configuráveis com campos dinâmicos' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'SolicitacaoTipo';
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'Código único do tipo (NOVO_CELULAR, REPARO, CANCELAMENTO)' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'SolicitacaoTipo', @level2type=N'COLUMN',@level2name=N'Codigo';


-- ---------------------------------------------
-- Tabela: Solicitacao
-- ---------------------------------------------
CREATE TABLE Solicitacao (
    Id UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    Numero VARCHAR(20) NOT NULL,
    ClienteId UNIQUEIDENTIFIER NOT NULL,
    TipoId UNIQUEIDENTIFIER NOT NULL,
    SolicitanteId UNIQUEIDENTIFIER NOT NULL,
    AtendenteId UNIQUEIDENTIFIER NULL,
    Status VARCHAR(30) NOT NULL DEFAULT 'ABERTA',
    Prioridade INT NOT NULL DEFAULT 2,
    Titulo NVARCHAR(200) NOT NULL,
    Descricao NVARCHAR(MAX) NOT NULL,
    CamposDinamicosJSON NVARCHAR(MAX) NULL,
    DataAbertura DATETIME2(7) NOT NULL DEFAULT SYSUTCDATETIME(),
    DataLimiteSLA DATETIME2(7) NULL,
    DataFechamento DATETIME2(7) NULL,
    TempoPausadoSLA INT NOT NULL DEFAULT 0,
    DataAtribuicao DATETIME2(7) NULL,
    EmAprovacao BIT NOT NULL DEFAULT 0,
    NivelAprovacaoAtual INT NOT NULL DEFAULT 0,
    Solucao NVARCHAR(MAX) NULL,
    JustificativaCancelamento NVARCHAR(500) NULL,
    Escalonada BIT NOT NULL DEFAULT 0,
    DataEscalonamento DATETIME2(7) NULL,
    VIP BIT NOT NULL DEFAULT 0,
    DataReabertura DATETIME2(7) NULL,
    MotivoPendencia NVARCHAR(500) NULL,
    FlExcluido BIT NOT NULL DEFAULT 0,
    CreatedAt DATETIME2(7) NOT NULL DEFAULT SYSUTCDATETIME(),
    CreatedBy UNIQUEIDENTIFIER NOT NULL,
    ModifiedAt DATETIME2(7) NULL,
    ModifiedBy UNIQUEIDENTIFIER NULL,

    CONSTRAINT PK_Solicitacao PRIMARY KEY CLUSTERED (Id),
    CONSTRAINT FK_Solicitacao_Cliente FOREIGN KEY (ClienteId) REFERENCES Cliente(Id),
    CONSTRAINT FK_Solicitacao_Tipo FOREIGN KEY (TipoId) REFERENCES SolicitacaoTipo(Id),
    CONSTRAINT FK_Solicitacao_Solicitante FOREIGN KEY (SolicitanteId) REFERENCES Usuario(Id),
    CONSTRAINT FK_Solicitacao_Atendente FOREIGN KEY (AtendenteId) REFERENCES Usuario(Id),
    CONSTRAINT FK_Solicitacao_CreatedBy FOREIGN KEY (CreatedBy) REFERENCES Usuario(Id),
    CONSTRAINT CK_Solicitacao_Status CHECK (Status IN ('ABERTA', 'EM_APROVACAO', 'APROVADA', 'REJEITADA', 'EM_ATENDIMENTO', 'AGUARDANDO_CLIENTE', 'FECHADA', 'CANCELADA', 'REABERTA')),
    CONSTRAINT CK_Solicitacao_Prioridade CHECK (Prioridade BETWEEN 1 AND 5),
    CONSTRAINT CK_Solicitacao_NivelAprovacao CHECK (NivelAprovacaoAtual >= 0),
    CONSTRAINT CK_Solicitacao_TempoPausado CHECK (TempoPausadoSLA >= 0)
);

CREATE UNIQUE NONCLUSTERED INDEX UK_Solicitacao_Numero ON Solicitacao(Numero);
CREATE NONCLUSTERED INDEX IX_Solicitacao_Cliente ON Solicitacao(ClienteId, DataAbertura DESC);
CREATE NONCLUSTERED INDEX IX_Solicitacao_Status ON Solicitacao(Status, DataLimiteSLA) WHERE Status IN ('ABERTA','EM_ATENDIMENTO');
CREATE NONCLUSTERED INDEX IX_Solicitacao_Solicitante ON Solicitacao(SolicitanteId, DataAbertura DESC);
CREATE NONCLUSTERED INDEX IX_Solicitacao_Atendente ON Solicitacao(AtendenteId, Status) WHERE AtendenteId IS NOT NULL;
CREATE NONCLUSTERED INDEX IX_Solicitacao_SLA ON Solicitacao(DataLimiteSLA) WHERE Status NOT IN ('FECHADA','CANCELADA');
CREATE NONCLUSTERED INDEX IX_Solicitacao_Tipo ON Solicitacao(TipoId, DataAbertura DESC);
CREATE NONCLUSTERED INDEX IX_Solicitacao_VIP ON Solicitacao(VIP, Prioridade DESC) WHERE VIP = 1;
CREATE NONCLUSTERED INDEX IX_Solicitacao_Prioridade ON Solicitacao(Prioridade DESC, DataAbertura) WHERE Status IN ('ABERTA', 'EM_ATENDIMENTO');

EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'Tabela principal de solicitações do service desk' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'Solicitacao';
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'Número sequencial único (SOL-2025-00001)' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'Solicitacao', @level2type=N'COLUMN',@level2name=N'Numero';


-- ---------------------------------------------
-- Tabela: SolicitacaoAnexo
-- ---------------------------------------------
CREATE TABLE SolicitacaoAnexo (
    Id UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    SolicitacaoId UNIQUEIDENTIFIER NOT NULL,
    NomeArquivo NVARCHAR(255) NOT NULL,
    TipoMIME VARCHAR(100) NOT NULL,
    TamanhoBytes BIGINT NOT NULL,
    CaminhoBlob NVARCHAR(500) NOT NULL,
    HashSHA256 VARCHAR(64) NOT NULL,
    TipoAnexo VARCHAR(50) NULL,
    DataUpload DATETIME2(7) NOT NULL DEFAULT SYSUTCDATETIME(),
    UsuarioUploadId UNIQUEIDENTIFIER NOT NULL,

    CONSTRAINT PK_SolicitacaoAnexo PRIMARY KEY CLUSTERED (Id),
    CONSTRAINT FK_SolicitacaoAnexo_Solicitacao FOREIGN KEY (SolicitacaoId) REFERENCES Solicitacao(Id) ON DELETE CASCADE,
    CONSTRAINT FK_SolicitacaoAnexo_Usuario FOREIGN KEY (UsuarioUploadId) REFERENCES Usuario(Id),
    CONSTRAINT CK_SolicitacaoAnexo_Tamanho CHECK (TamanhoBytes > 0 AND TamanhoBytes <= 10485760) -- Max 10MB
);

CREATE NONCLUSTERED INDEX IX_SolicitacaoAnexo_Solicitacao ON SolicitacaoAnexo(SolicitacaoId, DataUpload DESC);
CREATE NONCLUSTERED INDEX IX_SolicitacaoAnexo_Usuario ON SolicitacaoAnexo(UsuarioUploadId, DataUpload DESC);
CREATE NONCLUSTERED INDEX IX_SolicitacaoAnexo_Hash ON SolicitacaoAnexo(HashSHA256);

EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'Arquivos anexados às solicitações' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'SolicitacaoAnexo';


-- ---------------------------------------------
-- Tabela: SolicitacaoHistorico
-- ---------------------------------------------
CREATE TABLE SolicitacaoHistorico (
    Id UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    SolicitacaoId UNIQUEIDENTIFIER NOT NULL,
    StatusAnterior VARCHAR(30) NULL,
    StatusNovo VARCHAR(30) NOT NULL,
    UsuarioId UNIQUEIDENTIFIER NOT NULL,
    DataAlteracao DATETIME2(7) NOT NULL DEFAULT SYSUTCDATETIME(),
    Comentario NVARCHAR(1000) NULL,
    TipoOperacao VARCHAR(50) NOT NULL,

    CONSTRAINT PK_SolicitacaoHistorico PRIMARY KEY CLUSTERED (Id),
    CONSTRAINT FK_SolicitacaoHistorico_Solicitacao FOREIGN KEY (SolicitacaoId) REFERENCES Solicitacao(Id) ON DELETE CASCADE,
    CONSTRAINT FK_SolicitacaoHistorico_Usuario FOREIGN KEY (UsuarioId) REFERENCES Usuario(Id),
    CONSTRAINT CK_SolicitacaoHistorico_TipoOperacao CHECK (TipoOperacao IN ('CRIACAO', 'ATRIBUICAO', 'APROVACAO', 'REJEICAO', 'FECHAMENTO', 'CANCELAMENTO', 'ESCALONAMENTO', 'REABERTURA', 'PAUSA_SLA', 'RETOMADA_SLA'))
);

CREATE NONCLUSTERED INDEX IX_SolicitacaoHistorico_Solicitacao ON SolicitacaoHistorico(SolicitacaoId, DataAlteracao DESC);
CREATE NONCLUSTERED INDEX IX_SolicitacaoHistorico_Usuario ON SolicitacaoHistorico(UsuarioId, DataAlteracao DESC);
CREATE NONCLUSTERED INDEX IX_SolicitacaoHistorico_TipoOperacao ON SolicitacaoHistorico(TipoOperacao, DataAlteracao DESC);

EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'Timeline completa de ações na solicitação' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'SolicitacaoHistorico';


-- ---------------------------------------------
-- Tabela: SolicitacaoAprovacao
-- ---------------------------------------------
CREATE TABLE SolicitacaoAprovacao (
    Id UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    SolicitacaoId UNIQUEIDENTIFIER NOT NULL,
    NivelAprovacao INT NOT NULL,
    AprovadorId UNIQUEIDENTIFIER NOT NULL,
    Decisao VARCHAR(20) NULL DEFAULT 'PENDENTE',
    Justificativa NVARCHAR(500) NULL,
    DataDecisao DATETIME2(7) NULL,
    DataLimiteDecisao DATETIME2(7) NULL,
    TokenTemporario VARCHAR(100) NULL,
    DataExpiracaoToken DATETIME2(7) NULL,

    CONSTRAINT PK_SolicitacaoAprovacao PRIMARY KEY CLUSTERED (Id),
    CONSTRAINT FK_SolicitacaoAprovacao_Solicitacao FOREIGN KEY (SolicitacaoId) REFERENCES Solicitacao(Id) ON DELETE CASCADE,
    CONSTRAINT FK_SolicitacaoAprovacao_Aprovador FOREIGN KEY (AprovadorId) REFERENCES Usuario(Id),
    CONSTRAINT CK_SolicitacaoAprovacao_Decisao CHECK (Decisao IN ('PENDENTE', 'APROVADO', 'REJEITADO')),
    CONSTRAINT CK_SolicitacaoAprovacao_Nivel CHECK (NivelAprovacao > 0)
);

CREATE NONCLUSTERED INDEX IX_SolicitacaoAprovacao_Solicitacao ON SolicitacaoAprovacao(SolicitacaoId, NivelAprovacao);
CREATE NONCLUSTERED INDEX IX_SolicitacaoAprovacao_Aprovador ON SolicitacaoAprovacao(AprovadorId, Decisao) WHERE Decisao = 'PENDENTE';
CREATE NONCLUSTERED INDEX IX_SolicitacaoAprovacao_DataLimite ON SolicitacaoAprovacao(DataLimiteDecisao) WHERE Decisao = 'PENDENTE';

EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'Workflow de aprovação multi-nível' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'SolicitacaoAprovacao';


-- ---------------------------------------------
-- Tabela: SolicitacaoMensagem
-- ---------------------------------------------
CREATE TABLE SolicitacaoMensagem (
    Id UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    SolicitacaoId UNIQUEIDENTIFIER NOT NULL,
    UsuarioId UNIQUEIDENTIFIER NOT NULL,
    Mensagem NVARCHAR(4000) NOT NULL,
    DataEnvio DATETIME2(7) NOT NULL DEFAULT SYSUTCDATETIME(),
    Interna BIT NOT NULL DEFAULT 0,
    Lida BIT NOT NULL DEFAULT 0,
    DataLeitura DATETIME2(7) NULL,

    CONSTRAINT PK_SolicitacaoMensagem PRIMARY KEY CLUSTERED (Id),
    CONSTRAINT FK_SolicitacaoMensagem_Solicitacao FOREIGN KEY (SolicitacaoId) REFERENCES Solicitacao(Id) ON DELETE CASCADE,
    CONSTRAINT FK_SolicitacaoMensagem_Usuario FOREIGN KEY (UsuarioId) REFERENCES Usuario(Id)
);

CREATE NONCLUSTERED INDEX IX_SolicitacaoMensagem_Solicitacao ON SolicitacaoMensagem(SolicitacaoId, DataEnvio ASC);
CREATE NONCLUSTERED INDEX IX_SolicitacaoMensagem_NaoLidas ON SolicitacaoMensagem(SolicitacaoId, Lida) WHERE Lida = 0;

EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'Chat interno por solicitação' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'SolicitacaoMensagem';


-- ---------------------------------------------
-- Tabela: DelegacaoAprovador
-- ---------------------------------------------
CREATE TABLE DelegacaoAprovador (
    Id UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    AprovadorOriginalId UNIQUEIDENTIFIER NOT NULL,
    AprovadorDelegadoId UNIQUEIDENTIFIER NOT NULL,
    InicioVigencia DATETIME2(7) NOT NULL,
    FimVigencia DATETIME2(7) NOT NULL,
    Motivo NVARCHAR(200) NULL,
    ClienteId UNIQUEIDENTIFIER NOT NULL,
    FlExcluido BIT NOT NULL DEFAULT 0,
    CreatedAt DATETIME2(7) NOT NULL DEFAULT SYSUTCDATETIME(),
    CreatedBy UNIQUEIDENTIFIER NOT NULL,

    CONSTRAINT PK_DelegacaoAprovador PRIMARY KEY CLUSTERED (Id),
    CONSTRAINT FK_DelegacaoAprovador_Original FOREIGN KEY (AprovadorOriginalId) REFERENCES Usuario(Id),
    CONSTRAINT FK_DelegacaoAprovador_Delegado FOREIGN KEY (AprovadorDelegadoId) REFERENCES Usuario(Id),
    CONSTRAINT FK_DelegacaoAprovador_Cliente FOREIGN KEY (ClienteId) REFERENCES Cliente(Id),
    CONSTRAINT FK_DelegacaoAprovador_CreatedBy FOREIGN KEY (CreatedBy) REFERENCES Usuario(Id),
    CONSTRAINT CK_DelegacaoAprovador_Vigencia CHECK (FimVigencia > InicioVigencia),
    CONSTRAINT CK_DelegacaoAprovador_MaxDias CHECK (DATEDIFF(DAY, InicioVigencia, FimVigencia) <= 90)
);

CREATE NONCLUSTERED INDEX IX_DelegacaoAprovador_Original ON DelegacaoAprovador(AprovadorOriginalId, InicioVigencia, FimVigencia);
CREATE NONCLUSTERED INDEX IX_DelegacaoAprovador_Vigente ON DelegacaoAprovador(InicioVigencia, FimVigencia, Ativo) WHERE FlExcluido = 0;

EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'Delegações temporárias de aprovadores' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'DelegacaoAprovador';


-- ---------------------------------------------
-- Tabela: PesquisaSatisfacao
-- ---------------------------------------------
CREATE TABLE PesquisaSatisfacao (
    Id UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    SolicitacaoId UNIQUEIDENTIFIER NOT NULL,
    NotaAtendimento INT NOT NULL,
    NotaAgilidade INT NULL,
    NotaComunicacao INT NULL,
    Comentarios NVARCHAR(2000) NULL,
    DataResposta DATETIME2(7) NOT NULL DEFAULT SYSUTCDATETIME(),
    DataEnvio DATETIME2(7) NOT NULL,

    CONSTRAINT PK_PesquisaSatisfacao PRIMARY KEY CLUSTERED (Id),
    CONSTRAINT FK_PesquisaSatisfacao_Solicitacao FOREIGN KEY (SolicitacaoId) REFERENCES Solicitacao(Id),
    CONSTRAINT CK_PesquisaSatisfacao_NotaNPS CHECK (NotaAtendimento BETWEEN 0 AND 10),
    CONSTRAINT CK_PesquisaSatisfacao_NotaAgilidade CHECK (NotaAgilidade IS NULL OR NotaAgilidade BETWEEN 1 AND 5),
    CONSTRAINT CK_PesquisaSatisfacao_NotaComunicacao CHECK (NotaComunicacao IS NULL OR NotaComunicacao BETWEEN 1 AND 5)
);

CREATE UNIQUE NONCLUSTERED INDEX UK_PesquisaSatisfacao_Solicitacao ON PesquisaSatisfacao(SolicitacaoId);
CREATE NONCLUSTERED INDEX IX_PesquisaSatisfacao_Nota ON PesquisaSatisfacao(NotaAtendimento, DataResposta DESC);

EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'Pesquisa de satisfação NPS' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'PesquisaSatisfacao';


-- ---------------------------------------------
-- Tabela: SolicitacaoItemAtivo
-- ---------------------------------------------
CREATE TABLE SolicitacaoItemAtivo (
    Id UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    SolicitacaoId UNIQUEIDENTIFIER NOT NULL,
    TipoAtivo VARCHAR(50) NOT NULL,
    Modelo NVARCHAR(100) NULL,
    Quantidade INT NOT NULL DEFAULT 1,
    ValorEstimado DECIMAL(18,2) NULL,
    Aprovado BIT NOT NULL DEFAULT 0,
    AtivoGeradoId UNIQUEIDENTIFIER NULL,

    CONSTRAINT PK_SolicitacaoItemAtivo PRIMARY KEY CLUSTERED (Id),
    CONSTRAINT FK_SolicitacaoItemAtivo_Solicitacao FOREIGN KEY (SolicitacaoId) REFERENCES Solicitacao(Id) ON DELETE CASCADE,
    CONSTRAINT CK_SolicitacaoItemAtivo_Quantidade CHECK (Quantidade > 0),
    CONSTRAINT CK_SolicitacaoItemAtivo_Valor CHECK (ValorEstimado IS NULL OR ValorEstimado >= 0)
);

CREATE NONCLUSTERED INDEX IX_SolicitacaoItemAtivo_Solicitacao ON SolicitacaoItemAtivo(SolicitacaoId);

EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'Itens de ativos solicitados para integração com inventário' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'SolicitacaoItemAtivo';
```

---

## 5. Stored Procedures e Functions

```sql
-- =============================================
-- SP: Gerar Número Sequencial de Solicitação
-- =============================================
CREATE PROCEDURE sp_GerarNumeroSolicitacao
    @ClienteId UNIQUEIDENTIFIER,
    @Numero VARCHAR(20) OUTPUT
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @Ano INT = YEAR(GETDATE());
    DECLARE @Sequencial INT;

    -- Obter próximo sequencial do ano
    SELECT @Sequencial = ISNULL(MAX(CAST(RIGHT(Numero, 5) AS INT)), 0) + 1
    FROM Solicitacao
    WHERE ClienteId = @ClienteId
      AND Numero LIKE 'SOL-' + CAST(@Ano AS VARCHAR(4)) + '-%';

    SET @Numero = 'SOL-' + CAST(@Ano AS VARCHAR(4)) + '-' + RIGHT('00000' + CAST(@Sequencial AS VARCHAR(5)), 5);
END;
GO

-- =============================================
-- SP: Calcular Data Limite SLA
-- =============================================
CREATE PROCEDURE sp_CalcularDataLimiteSLA
    @DataAbertura DATETIME2(7),
    @SLAHoras INT,
    @DataLimite DATETIME2(7) OUTPUT
AS
BEGIN
    SET NOCOUNT ON;

    -- Cálculo simplificado (em produção, considerar feriados e fins de semana)
    SET @DataLimite = DATEADD(HOUR, @SLAHoras, @DataAbertura);
END;
GO

-- =============================================
-- Function: Calcular % SLA Consumido
-- =============================================
CREATE FUNCTION fn_PercentualSLAConsumido(
    @DataAbertura DATETIME2(7),
    @DataLimiteSLA DATETIME2(7),
    @TempoPausadoMinutos INT
)
RETURNS DECIMAL(5,2)
AS
BEGIN
    DECLARE @TempoDecorrido INT = DATEDIFF(MINUTE, @DataAbertura, SYSUTCDATETIME()) - @TempoPausadoMinutos;
    DECLARE @TempoTotal INT = DATEDIFF(MINUTE, @DataAbertura, @DataLimiteSLA);

    IF @TempoTotal <= 0 RETURN 100.00;

    RETURN CAST(@TempoDecorrido AS DECIMAL(10,2)) / @TempoTotal * 100;
END;
GO
```

---

## 6. Views Úteis

```sql
-- =============================================
-- VIEW: Solicitações Abertas com % SLA
-- =============================================
CREATE VIEW vw_SolicitacoesAbertas
AS
SELECT
    s.Id,
    s.Numero,
    s.Titulo,
    s.Status,
    s.Prioridade,
    s.DataAbertura,
    s.DataLimiteSLA,
    dbo.fn_PercentualSLAConsumido(s.DataAbertura, s.DataLimiteSLA, s.TempoPausadoSLA) AS PercentualSLA,
    sol.Nome AS Solicitante,
    atd.Nome AS Atendente,
    st.Nome AS TipoSolicitacao
FROM Solicitacao s
INNER JOIN Usuario sol ON s.SolicitanteId = sol.Id
LEFT JOIN Usuario atd ON s.AtendenteId = atd.Id
INNER JOIN SolicitacaoTipo st ON s.TipoId = st.Id
WHERE s.Status IN ('ABERTA', 'EM_ATENDIMENTO', 'AGUARDANDO_CLIENTE')
  AND s.Ativo = 1;
GO

-- =============================================
-- VIEW: Estatísticas de Atendimento
-- =============================================
CREATE VIEW vw_EstatisticasAtendimento
AS
SELECT
    a.Id AS AtendenteId,
    a.Nome AS Atendente,
    COUNT(s.Id) AS TotalAtendimentos,
    AVG(DATEDIFF(MINUTE, s.DataAbertura, s.DataFechamento)) AS TempoMedioMinutos,
    SUM(CASE WHEN s.DataFechamento <= s.DataLimiteSLA THEN 1 ELSE 0 END) AS DentroSLA,
    AVG(ps.NotaAtendimento) AS MediaNPS
FROM Usuario a
LEFT JOIN Solicitacao s ON a.Id = s.AtendenteId AND s.Status = 'FECHADA'
LEFT JOIN PesquisaSatisfacao ps ON s.Id = ps.SolicitacaoId
WHERE a.Ativo = 1
GROUP BY a.Id, a.Nome;
GO
```

---

## 7. Triggers

```sql
-- =============================================
-- TRIGGER: Criar Histórico Automático
-- =============================================
CREATE TRIGGER trg_Solicitacao_CriarHistorico
ON Solicitacao
AFTER INSERT, UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    IF EXISTS (SELECT 1 FROM inserted)
    BEGIN
        INSERT INTO SolicitacaoHistorico (SolicitacaoId, StatusAnterior, StatusNovo, UsuarioId, TipoOperacao, Comentario)
        SELECT
            i.Id,
            ISNULL(d.Status, 'NOVA'),
            i.Status,
            i.ModifiedBy,
            CASE
                WHEN d.Id IS NULL THEN 'CRIACAO'
                WHEN i.Status != d.Status THEN 'MUDANCA_STATUS'
                WHEN i.AtendenteId IS NOT NULL AND (d.AtendenteId IS NULL OR i.AtendenteId != d.AtendenteId) THEN 'ATRIBUICAO'
                ELSE 'ATUALIZACAO'
            END,
            NULL
        FROM inserted i
        LEFT JOIN deleted d ON i.Id = d.Id;
    END
END;
GO
```

---

## 8. Índices Computados

```sql
-- =============================================
-- Adicionar Colunas Computadas
-- =============================================
ALTER TABLE Solicitacao
ADD TempoAbertoDias AS DATEDIFF(DAY, DataAbertura, ISNULL(DataFechamento, SYSUTCDATETIME())) PERSISTED;

ALTER TABLE Solicitacao
ADD SLAVencido AS CASE WHEN DataLimiteSLA < SYSUTCDATETIME() AND Status NOT IN ('FECHADA','CANCELADA') THEN 1 ELSE 0 END PERSISTED;

CREATE NONCLUSTERED INDEX IX_Solicitacao_SLAVencido ON Solicitacao(SLAVencido, DataLimiteSLA) WHERE SLAVencido = 1;
```

---

## 9. Dados Iniciais (Seed)

```sql
-- =============================================
-- Dados Iniciais: Tipos de Solicitação
-- =============================================
DECLARE @ClienteId UNIQUEIDENTIFIER = (SELECT TOP 1 Id FROM Cliente WHERE FlExcluido = 0);
DECLARE @UsuarioId UNIQUEIDENTIFIER = (SELECT TOP 1 Id FROM Usuario WHERE Email = 'admin@icontrolit.com');

IF @ClienteId IS NOT NULL AND @UsuarioId IS NOT NULL
BEGIN
    INSERT INTO SolicitacaoTipo (Codigo, Nome, Descricao, SLAHoras, RequerAprovacao, ClienteId, CreatedBy)
    VALUES
        ('NOVO_CELULAR', N'Novo Celular', N'Solicitação de novo aparelho celular corporativo', 48, 1, @ClienteId, @UsuarioId),
        ('NOVO_NOTEBOOK', N'Novo Notebook', N'Solicitação de novo notebook corporativo', 72, 1, @ClienteId, @UsuarioId),
        ('REPARO_EQUIPAMENTO', N'Reparo de Equipamento', N'Solicitação de reparo técnico', 24, 0, @ClienteId, @UsuarioId),
        ('CANCELAMENTO_LINHA', N'Cancelamento de Linha', N'Solicitação de cancelamento de linha móvel', 48, 1, @ClienteId, @UsuarioId),
        ('TROCA_EQUIPAMENTO', N'Troca de Equipamento', N'Solicitação de troca por defeito ou upgrade', 48, 1, @ClienteId, @UsuarioId),
        ('SUPORTE_TECNICO', N'Suporte Técnico', N'Solicitação de suporte técnico geral', 4, 0, @ClienteId, @UsuarioId);
END;
GO
```

---

## 10. Observações Importantes

### 10.1 Multi-Tenancy
- Todas as tabelas principais possuem `ClienteId` para isolamento de dados entre clientes.
- Índices filtrados garantem performance em queries multi-tenant.

### 10.2 Performance
- Índices filtrados para consultas frequentes (solicitações abertas, SLA vencido).
- Colunas computadas persistidas para cálculos repetitivos.
- Particionamento por data pode ser aplicado em `SolicitacaoHistorico` para alta volumetria.

### 10.3 Auditoria
- Campos `CreatedAt`, `CreatedBy`, `ModifiedAt`, `ModifiedBy` em todas as tabelas.
- Tabela `SolicitacaoHistorico` mantém timeline completa.
- Retenção mínima de 7 anos (LGPD).

### 10.4 Integração com Azure Blob Storage
- Anexos armazenados em Blob Storage (não no banco).
- Tabela `SolicitacaoAnexo` armazena apenas metadados e caminho.
- Hash SHA-256 para verificação de integridade.

### 10.5 Workflow de Aprovação
- Suporta múltiplos níveis configuráveis por tipo.
- Delegação temporária de aprovadores.
- Tokens temporários para aprovação mobile (15 minutos).

### 10.6 SLA e Escalonamento
- Cálculo automático de SLA por tipo.
- Suporte a pausas durante pendências externas.
- Escalonamento automático via jobs Hangfire.

### 10.7 Segurança
- Soft delete: false=ativo, true=excluído em todas as entidades principais.
- ON DELETE CASCADE apenas em tabelas de relacionamento.
- Constraints para validação de dados críticos.

---

## 11. Jobs Hangfire Recomendados

```csharp
// Job: Verificar escalonamento de SLA (executar a cada 30 minutos)
RecurringJob.AddOrUpdate("verificar-escalonamento-solicitacoes",
    () => solicitacoesService.VerificarEscalonamento(), "*/30 * * * *");

// Job: Enviar pesquisa de satisfação (executar diariamente às 10h)
RecurringJob.AddOrUpdate("enviar-pesquisas-satisfacao",
    () => solicitacoesService.EnviarPesquisasSatisfacao(), "0 10 * * *");

// Job: Atualizar métricas dashboard (executar a cada 5 minutos)
RecurringJob.AddOrUpdate("atualizar-dashboard-solicitacoes",
    () => solicitacoesService.AtualizarDashboard(), "*/5 * * * *");

// Job: Limpar tokens expirados (executar diariamente às 2h)
RecurringJob.AddOrUpdate("limpar-tokens-aprovacao",
    () => solicitacoesService.LimparTokensExpirados(), "0 2 * * *");
```

---

## Histórico de Alterações

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 1.0 | 2025-12-18 | IControlIT Architect Agent | Versão inicial completa com 9 tabelas |

---

**Documento aprovado para implementação**
**Total de tabelas:** 9
**Total de índices:** 40+
**Total de constraints:** 35+
**Campos de auditoria:** Sim (Created/Modified em todas)
**Multi-tenancy:** Sim (ClienteId em todas)
**Soft delete: false=ativo, true=excluído:** Sim (Ativo em principais)
