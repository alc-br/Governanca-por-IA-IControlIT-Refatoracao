# Modelo de Dados - RF061 - Gestão de Ordens de Serviço

**Versão:** 1.0
**Data:** 2025-12-18
**RF Relacionado:** [RF061 - Gestão de Ordens de Serviço](./RF061.md)
**Banco de Dados:** SQL Server / PostgreSQL

---

## 1. Diagrama de Entidades (ER)

```
┌─────────────────────────────────────────────────────┐
│                  GestaoCliente                       │
│                  (multi-tenancy)                     │
└──────────┬──────────────────────────────────────────┘
           │ 1:N
           │
┌──────────▼──────────────────────────────────────────────────┐
│                    OrdemServico                              │
├──────────────────────────────────────────────────────────────┤
│ Id (PK)                     UUID                             │
│ ClienteId (FK)              UUID                             │
│ Numero                      VARCHAR(50)                      │
│ SolicitacaoOrigemId (FK)    UUID (nullable)                  │
│ ChamadoOrigemId (FK)        UUID (nullable)                  │
│ ClienteId_Solicitante (FK)  UUID                             │
│ TecnicoId (FK)              UUID                             │
│ TipoOS                      VARCHAR(50)                      │
│ Status                      VARCHAR(50)                      │
│ Prioridade                  VARCHAR(20)                      │
│ LocalAtendimentoId (FK)     UUID                             │
│ DataAgendada                DATETIME2                        │
│ DataInicio                  DATETIME2                        │
│ DataFim                     DATETIME2                        │
│ DataPrevistaFinalizacao     DATETIME2                        │
│ TempoTotal (computed)       INT                              │
│ Descricao                   TEXT                             │
│ SolucaoAplicada             TEXT                             │
│ AvaliacaoNPS                INT (1-10)                       │
│ ComentarioAvaliacao         TEXT                             │
│ Ativo                       BIT                              │
│ CreatedAt, CreatedBy, ModifiedAt, ModifiedBy                 │
└──────────┬───────────────────────────────────────────────────┘
           │ 1:N
           ├──────────────────────────────────────────┐
           │                                          │
┌──────────▼──────────────┐   ┌──────────────────────▼──────────────────┐
│   ChecklistItemOS       │   │      AssinaturaOS                       │
├─────────────────────────┤   ├─────────────────────────────────────────┤
│ Id (PK)         UUID    │   │ Id (PK)              UUID               │
│ OSId (FK)       UUID    │   │ OSId (FK)            UUID               │
│ ClienteId (FK)  UUID    │   │ ClienteId (FK)       UUID               │
│ Descricao       VARCHAR │   │ TipoAssinatura       VARCHAR(20)        │
│ Concluido       BIT     │   │ NomeAssinante        VARCHAR(200)       │
│ Observacao      TEXT    │   │ CPF                  VARCHAR(11)         │
│ Ordem           INT     │   │ AssinaturaBase64     TEXT               │
│ DataConclusao   DATETIME│   │ IPDispositivo        VARCHAR(50)        │
│ CreatedAt, ...          │   │ Latitude             DECIMAL(10,7)      │
└─────────────────────────┘   │ Longitude            DECIMAL(10,7)      │
                               │ DataHoraAssinatura   DATETIME2          │
┌──────────────────────────┐   │ HashValidacao        VARCHAR(255)       │
│    PecaUtilizada         │   │ CreatedAt, CreatedBy                    │
├──────────────────────────┤   └─────────────────────────────────────────┘
│ Id (PK)          UUID    │
│ OSId (FK)        UUID    │   ┌─────────────────────────────────────────┐
│ ClienteId (FK)   UUID    │   │      FotoOS                             │
│ PecaId (FK)      UUID    │   ├─────────────────────────────────────────┤
│ Quantidade       INT     │   │ Id (PK)              UUID               │
│ ValorUnitario    DECIMAL │   │ OSId (FK)            UUID               │
│ ValorTotal (comp)DECIMAL │   │ ClienteId (FK)       UUID               │
│ EstoqueBaixado   BIT     │   │ TipoFoto             VARCHAR(20)        │
│ CreatedAt, ...           │   │ CaminhoArquivo       VARCHAR(500)       │
└──────────────────────────┘   │ DescricaoFoto        TEXT               │
                               │ DataUpload           DATETIME2          │
┌──────────────────────────┐   │ Latitude             DECIMAL(10,7)      │
│   CheckpointOS           │   │ Longitude            DECIMAL(10,7)      │
├──────────────────────────┤   │ TamanhoArquivoKB     INT                │
│ Id (PK)          UUID    │   │ CreatedAt, CreatedBy                    │
│ OSId (FK)        UUID    │   └─────────────────────────────────────────┘
│ ClienteId (FK)   UUID    │
│ TipoCheckpoint   VARCHAR │   ┌─────────────────────────────────────────┐
│ DataHora         DATETIME│   │   TemplateChecklistOS                   │
│ Latitude         DECIMAL │   ├─────────────────────────────────────────┤
│ Longitude        DECIMAL │   │ Id (PK)              UUID               │
│ Precisao         DECIMAL │   │ TipoOS               VARCHAR(50)        │
│ ObservacaoTecnico TEXT   │   │ ClienteId (FK)       UUID               │
│ CreatedAt, ...           │   │ Titulo               VARCHAR(200)       │
└──────────────────────────┘   │ Descricao            TEXT               │
                               │ Ativo                BIT                │
┌──────────────────────────┐   │ CreatedAt, CreatedBy, ...               │
│  AgendaTecnico           │   └─────────┬───────────────────────────────┘
├──────────────────────────┤             │ 1:N
│ Id (PK)          UUID    │   ┌─────────▼───────────────────────────────┐
│ TecnicoId (FK)   UUID    │   │   TemplateChecklistItemOS               │
│ ClienteId (FK)   UUID    │   ├─────────────────────────────────────────┤
│ Data             DATE    │   │ Id (PK)              UUID               │
│ HoraInicio       TIME    │   │ TemplateId (FK)      UUID               │
│ HoraFim          TIME    │   │ Descricao            VARCHAR(500)       │
│ Disponivel       BIT     │   │ TipoResposta         VARCHAR(20)        │
│ Motivo           TEXT    │   │ Obrigatorio          BIT                │
│ CreatedAt, ...           │   │ Ordem                INT                │
└──────────────────────────┘   │ Ativo                BIT                │
                               │ CreatedAt, CreatedBy                    │
                               └─────────────────────────────────────────┘
```

---

## 2. Entidades

### 2.1 Tabela: OrdemServico

**Descrição:** Ordem de Serviço (OS) para atendimentos técnicos presenciais (field service). Contém informações de agendamento, execução, avaliação e vinculação com solicitações/chamados origem.

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| ClienteId | UNIQUEIDENTIFIER | NÃO | - | FK para GestaoCliente |
| Numero | VARCHAR(50) | NÃO | - | Número sequencial (OS-2025-00001) |
| SolicitacaoOrigemId | UNIQUEIDENTIFIER | SIM | NULL | FK para Solicitacao (se criada automaticamente) |
| ChamadoOrigemId | UNIQUEIDENTIFIER | SIM | NULL | FK para Chamado (alternativa) |
| ClienteId_Solicitante | UNIQUEIDENTIFIER | NÃO | - | FK para Cliente (solicitante) |
| TecnicoId | UNIQUEIDENTIFIER | SIM | NULL | FK para Usuario (técnico responsável) |
| TipoOS | VARCHAR(50) | NÃO | - | INSTALACAO, MANUTENCAO, DESINSTALACAO, REPARO |
| Status | VARCHAR(50) | NÃO | - | AGUARDANDO_AGENDAMENTO, AGENDADA, EM_ATENDIMENTO, PAUSADA, FINALIZADA, CANCELADA |
| Prioridade | VARCHAR(20) | NÃO | 'MEDIA' | CRITICA, ALTA, MEDIA, BAIXA |
| LocalAtendimentoId | UNIQUEIDENTIFIER | NÃO | - | FK para Local (endereço) |
| DataAgendada | DATETIME2 | SIM | NULL | Data/hora agendada com cliente |
| DataInicio | DATETIME2 | SIM | NULL | Data/hora início real (check-in) |
| DataFim | DATETIME2 | SIM | NULL | Data/hora fim real (check-out) |
| DataPrevistaFinalizacao | DATETIME2 | SIM | NULL | Data prevista SLA |
| TempoTotalMinutos | AS (CASE WHEN DataFim IS NOT NULL AND DataInicio IS NOT NULL THEN DATEDIFF(MINUTE, DataInicio, DataFim) ELSE NULL END) PERSISTED | - | - | Tempo total atendimento |
| Descricao | TEXT | NÃO | - | Descrição do serviço a ser executado |
| SolucaoAplicada | TEXT | SIM | NULL | Descrição da solução aplicada |
| AvaliacaoNPS | INT | SIM | NULL | Nota NPS 1-10 (cliente avalia serviço) |
| ComentarioAvaliacao | TEXT | SIM | NULL | Comentário da avaliação |
| Ativo | BIT | NÃO | 1 | Status ativo/inativo |
| CreatedAt | DATETIME2 | NÃO | GETUTCDATE() | Data de criação |
| CreatedBy | UNIQUEIDENTIFIER | NÃO | - | Usuário criador |
| ModifiedAt | DATETIME2 | SIM | NULL | Data de atualização |
| ModifiedBy | UNIQUEIDENTIFIER | SIM | NULL | Usuário atualizador |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| PK_OrdemServico | Id | CLUSTERED | Chave primária |
| IX_OrdemServico_ClienteId | ClienteId | NONCLUSTERED | Multi-tenancy |
| IX_OrdemServico_Numero | Numero, ClienteId | NONCLUSTERED UNIQUE | Número único |
| IX_OrdemServico_TecnicoId | TecnicoId, Status | NONCLUSTERED | OSs por técnico |
| IX_OrdemServico_Status | Status, ClienteId | NONCLUSTERED | Filtro por status |
| IX_OrdemServico_DataAgendada | DataAgendada, TecnicoId | NONCLUSTERED | Agenda técnico |
| IX_OrdemServico_Solicitacao | SolicitacaoOrigemId | NONCLUSTERED | Rastreabilidade |
| IX_OrdemServico_Chamado | ChamadoOrigemId | NONCLUSTERED | Rastreabilidade |
| IX_OrdemServico_LocalAtendimento | LocalAtendimentoId | NONCLUSTERED | OSs por local |

#### Constraints

| Nome | Tipo | Definição | Descrição |
|------|------|-----------|-----------|
| PK_OrdemServico | PRIMARY KEY | Id | Chave primária |
| FK_OrdemServico_Cliente | FOREIGN KEY | ClienteId REFERENCES GestaoCliente(Id) | Multi-tenancy |
| FK_OrdemServico_Solicitacao | FOREIGN KEY | SolicitacaoOrigemId REFERENCES Solicitacao(Id) | Solicitação origem |
| FK_OrdemServico_Chamado | FOREIGN KEY | ChamadoOrigemId REFERENCES Chamado(Id) | Chamado origem |
| FK_OrdemServico_Solicitante | FOREIGN KEY | ClienteId_Solicitante REFERENCES Cliente(Id) | Solicitante |
| FK_OrdemServico_Tecnico | FOREIGN KEY | TecnicoId REFERENCES Usuario(Id) | Técnico responsável |
| FK_OrdemServico_Local | FOREIGN KEY | LocalAtendimentoId REFERENCES Local(Id) | Local atendimento |
| FK_OrdemServico_CreatedBy | FOREIGN KEY | CreatedBy REFERENCES Usuario(Id) | Auditoria |
| FK_OrdemServico_ModifiedBy | FOREIGN KEY | ModifiedBy REFERENCES Usuario(Id) | Auditoria |
| UQ_OrdemServico_Numero | UNIQUE | (Numero, ClienteId) | Número único |
| CHK_OrdemServico_TipoOS | CHECK | TipoOS IN ('INSTALACAO', 'MANUTENCAO', 'DESINSTALACAO', 'REPARO') | Tipos válidos |
| CHK_OrdemServico_Status | CHECK | Status IN ('AGUARDANDO_AGENDAMENTO', 'AGENDADA', 'EM_ATENDIMENTO', 'PAUSADA', 'FINALIZADA', 'CANCELADA') | Status válidos |
| CHK_OrdemServico_Prioridade | CHECK | Prioridade IN ('CRITICA', 'ALTA', 'MEDIA', 'BAIXA') | Prioridades válidas |
| CHK_OrdemServico_DataFimMaiorInicio | CHECK | DataFim IS NULL OR DataInicio IS NULL OR DataFim >= DataInicio | Fim >= Início |
| CHK_OrdemServico_AvaliacaoNPS | CHECK | AvaliacaoNPS IS NULL OR AvaliacaoNPS BETWEEN 1 AND 10 | NPS 1-10 |

---

### 2.2 Tabela: ChecklistItemOS

**Descrição:** Itens do checklist de execução da OS. Técnico marca cada item como concluído durante o atendimento. Baseado em template ou criado manualmente.

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| OSId | UNIQUEIDENTIFIER | NÃO | - | FK para OrdemServico |
| ClienteId | UNIQUEIDENTIFIER | NÃO | - | FK para GestaoCliente |
| Descricao | VARCHAR(500) | NÃO | - | Descrição do item checklist |
| Concluido | BIT | NÃO | 0 | Se foi concluído |
| Observacao | TEXT | SIM | NULL | Observações sobre execução |
| Ordem | INT | NÃO | 0 | Ordem de exibição |
| DataConclusao | DATETIME2 | SIM | NULL | Data/hora da conclusão |
| CreatedAt | DATETIME2 | NÃO | GETUTCDATE() | Data de criação |
| CreatedBy | UNIQUEIDENTIFIER | NÃO | - | Usuário criador |
| ModifiedAt | DATETIME2 | SIM | NULL | Data de atualização |
| ModifiedBy | UNIQUEIDENTIFIER | SIM | NULL | Usuário atualizador |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| PK_ChecklistItemOS | Id | CLUSTERED | Chave primária |
| IX_ChecklistItemOS_OSId | OSId, Ordem | NONCLUSTERED | Listar itens da OS |
| IX_ChecklistItemOS_ClienteId | ClienteId | NONCLUSTERED | Multi-tenancy |
| IX_ChecklistItemOS_Concluido | OSId, Concluido | NONCLUSTERED | Filtro concluídos |

#### Constraints

| Nome | Tipo | Definição | Descrição |
|------|------|-----------|-----------|
| PK_ChecklistItemOS | PRIMARY KEY | Id | Chave primária |
| FK_ChecklistItemOS_OS | FOREIGN KEY | OSId REFERENCES OrdemServico(Id) ON DELETE CASCADE | OS pai |
| FK_ChecklistItemOS_Cliente | FOREIGN KEY | ClienteId REFERENCES GestaoCliente(Id) | Multi-tenancy |
| FK_ChecklistItemOS_CreatedBy | FOREIGN KEY | CreatedBy REFERENCES Usuario(Id) | Auditoria |
| FK_ChecklistItemOS_ModifiedBy | FOREIGN KEY | ModifiedBy REFERENCES Usuario(Id) | Auditoria |

---

### 2.3 Tabela: AssinaturaOS

**Descrição:** Armazena assinatura digital do cliente coletada em tablet/mobile ao finalizar OS. Inclui dados do assinante, geolocalização e hash para validade jurídica.

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| OSId | UNIQUEIDENTIFIER | NÃO | - | FK para OrdemServico |
| ClienteId | UNIQUEIDENTIFIER | NÃO | - | FK para GestaoCliente |
| TipoAssinatura | VARCHAR(20) | NÃO | - | CLIENTE, TECNICO, TESTEMUNHA |
| NomeAssinante | VARCHAR(200) | NÃO | - | Nome completo do assinante |
| CPF | VARCHAR(11) | SIM | NULL | CPF do assinante |
| AssinaturaBase64 | TEXT | NÃO | - | Imagem da assinatura em Base64 |
| IPDispositivo | VARCHAR(50) | NÃO | - | IP do dispositivo usado |
| Latitude | DECIMAL(10,7) | SIM | NULL | Latitude geolocalização |
| Longitude | DECIMAL(10,7) | SIM | NULL | Longitude geolocalização |
| DataHoraAssinatura | DATETIME2 | NÃO | GETUTCDATE() | Timestamp da assinatura |
| HashValidacao | VARCHAR(255) | NÃO | - | SHA-256 para validade |
| CreatedAt | DATETIME2 | NÃO | GETUTCDATE() | Data de criação |
| CreatedBy | UNIQUEIDENTIFIER | NÃO | - | Usuário criador (técnico) |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| PK_AssinaturaOS | Id | CLUSTERED | Chave primária |
| IX_AssinaturaOS_OSId | OSId, TipoAssinatura | NONCLUSTERED | Assinaturas da OS |
| IX_AssinaturaOS_ClienteId | ClienteId | NONCLUSTERED | Multi-tenancy |
| IX_AssinaturaOS_CPF | CPF, ClienteId | NONCLUSTERED | Busca por CPF |
| IX_AssinaturaOS_DataHora | DataHoraAssinatura DESC | NONCLUSTERED | Ordenação temporal |

#### Constraints

| Nome | Tipo | Definição | Descrição |
|------|------|-----------|-----------|
| PK_AssinaturaOS | PRIMARY KEY | Id | Chave primária |
| FK_AssinaturaOS_OS | FOREIGN KEY | OSId REFERENCES OrdemServico(Id) ON DELETE CASCADE | OS pai |
| FK_AssinaturaOS_Cliente | FOREIGN KEY | ClienteId REFERENCES GestaoCliente(Id) | Multi-tenancy |
| FK_AssinaturaOS_CreatedBy | FOREIGN KEY | CreatedBy REFERENCES Usuario(Id) | Técnico |
| CHK_AssinaturaOS_TipoAssinatura | CHECK | TipoAssinatura IN ('CLIENTE', 'TECNICO', 'TESTEMUNHA') | Tipos válidos |
| CHK_AssinaturaOS_CPF | CHECK | CPF IS NULL OR LEN(CPF) = 11 | CPF 11 dígitos |

---

### 2.4 Tabela: PecaUtilizada

**Descrição:** Peças/materiais utilizados na execução da OS. Registra quantidade, valor e realiza baixa automática no estoque.

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| OSId | UNIQUEIDENTIFIER | NÃO | - | FK para OrdemServico |
| ClienteId | UNIQUEIDENTIFIER | NÃO | - | FK para GestaoCliente |
| PecaId | UNIQUEIDENTIFIER | NÃO | - | FK para Peca/Material |
| Quantidade | INT | NÃO | - | Quantidade utilizada |
| ValorUnitario | DECIMAL(18,2) | NÃO | - | Valor unitário na data |
| ValorTotal | AS (Quantidade * ValorUnitario) PERSISTED | - | - | Valor total calculado |
| EstoqueBaixado | BIT | NÃO | 0 | Se baixa no estoque foi realizada |
| DataBaixaEstoque | DATETIME2 | SIM | NULL | Data da baixa no estoque |
| CreatedAt | DATETIME2 | NÃO | GETUTCDATE() | Data de criação |
| CreatedBy | UNIQUEIDENTIFIER | NÃO | - | Usuário criador |
| ModifiedAt | DATETIME2 | SIM | NULL | Data de atualização |
| ModifiedBy | UNIQUEIDENTIFIER | SIM | NULL | Usuário atualizador |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| PK_PecaUtilizada | Id | CLUSTERED | Chave primária |
| IX_PecaUtilizada_OSId | OSId | NONCLUSTERED | Peças da OS |
| IX_PecaUtilizada_ClienteId | ClienteId | NONCLUSTERED | Multi-tenancy |
| IX_PecaUtilizada_PecaId | PecaId, OSId | NONCLUSTERED | Busca por peça |
| IX_PecaUtilizada_EstoqueBaixado | EstoqueBaixado, OSId | NONCLUSTERED | Controle baixas pendentes |

#### Constraints

| Nome | Tipo | Definição | Descrição |
|------|------|-----------|-----------|
| PK_PecaUtilizada | PRIMARY KEY | Id | Chave primária |
| FK_PecaUtilizada_OS | FOREIGN KEY | OSId REFERENCES OrdemServico(Id) ON DELETE CASCADE | OS pai |
| FK_PecaUtilizada_Cliente | FOREIGN KEY | ClienteId REFERENCES GestaoCliente(Id) | Multi-tenancy |
| FK_PecaUtilizada_Peca | FOREIGN KEY | PecaId REFERENCES Peca(Id) | Peça/material |
| FK_PecaUtilizada_CreatedBy | FOREIGN KEY | CreatedBy REFERENCES Usuario(Id) | Auditoria |
| FK_PecaUtilizada_ModifiedBy | FOREIGN KEY | ModifiedBy REFERENCES Usuario(Id) | Auditoria |
| CHK_PecaUtilizada_Quantidade | CHECK | Quantidade > 0 | Quantidade positiva |
| CHK_PecaUtilizada_ValorUnitario | CHECK | ValorUnitario >= 0 | Valor não negativo |

---

### 2.5 Tabela: FotoOS

**Descrição:** Fotos de evidência (antes/depois/durante) da execução da OS. Armazenadas em storage externo com metadados no banco.

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| OSId | UNIQUEIDENTIFIER | NÃO | - | FK para OrdemServico |
| ClienteId | UNIQUEIDENTIFIER | NÃO | - | FK para GestaoCliente |
| TipoFoto | VARCHAR(20) | NÃO | - | ANTES, DEPOIS, DURANTE, DEFEITO |
| CaminhoArquivo | VARCHAR(500) | NÃO | - | Path no storage (Azure Blob, S3) |
| DescricaoFoto | TEXT | SIM | NULL | Descrição da foto |
| DataUpload | DATETIME2 | NÃO | GETUTCDATE() | Data do upload |
| Latitude | DECIMAL(10,7) | SIM | NULL | Latitude onde foto foi tirada |
| Longitude | DECIMAL(10,7) | SIM | NULL | Longitude onde foto foi tirada |
| TamanhoArquivoKB | INT | NÃO | - | Tamanho em KB |
| CreatedAt | DATETIME2 | NÃO | GETUTCDATE() | Data de criação |
| CreatedBy | UNIQUEIDENTIFIER | NÃO | - | Usuário criador (técnico) |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| PK_FotoOS | Id | CLUSTERED | Chave primária |
| IX_FotoOS_OSId | OSId, TipoFoto | NONCLUSTERED | Fotos da OS |
| IX_FotoOS_ClienteId | ClienteId | NONCLUSTERED | Multi-tenancy |
| IX_FotoOS_DataUpload | DataUpload DESC | NONCLUSTERED | Ordenação temporal |

#### Constraints

| Nome | Tipo | Definição | Descrição |
|------|------|-----------|-----------|
| PK_FotoOS | PRIMARY KEY | Id | Chave primária |
| FK_FotoOS_OS | FOREIGN KEY | OSId REFERENCES OrdemServico(Id) ON DELETE CASCADE | OS pai |
| FK_FotoOS_Cliente | FOREIGN KEY | ClienteId REFERENCES GestaoCliente(Id) | Multi-tenancy |
| FK_FotoOS_CreatedBy | FOREIGN KEY | CreatedBy REFERENCES Usuario(Id) | Técnico |
| CHK_FotoOS_TipoFoto | CHECK | TipoFoto IN ('ANTES', 'DEPOIS', 'DURANTE', 'DEFEITO') | Tipos válidos |
| CHK_FotoOS_TamanhoArquivo | CHECK | TamanhoArquivoKB > 0 | Tamanho positivo |

---

### 2.6 Tabela: CheckpointOS

**Descrição:** Registros de check-in/check-out do técnico com geolocalização GPS. Usado para calcular tempo de atendimento e validar presença física no local.

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| OSId | UNIQUEIDENTIFIER | NÃO | - | FK para OrdemServico |
| ClienteId | UNIQUEIDENTIFIER | NÃO | - | FK para GestaoCliente |
| TipoCheckpoint | VARCHAR(20) | NÃO | - | CHECK_IN, CHECK_OUT, PAUSA, RETORNO |
| DataHora | DATETIME2 | NÃO | GETUTCDATE() | Data/hora do checkpoint |
| Latitude | DECIMAL(10,7) | NÃO | - | Latitude GPS |
| Longitude | DECIMAL(10,7) | NÃO | - | Longitude GPS |
| Precisao | DECIMAL(10,2) | SIM | NULL | Precisão GPS em metros |
| ObservacaoTecnico | TEXT | SIM | NULL | Observação do técnico |
| CreatedAt | DATETIME2 | NÃO | GETUTCDATE() | Data de criação |
| CreatedBy | UNIQUEIDENTIFIER | NÃO | - | Usuário criador (técnico) |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| PK_CheckpointOS | Id | CLUSTERED | Chave primária |
| IX_CheckpointOS_OSId | OSId, DataHora | NONCLUSTERED | Checkpoints da OS |
| IX_CheckpointOS_ClienteId | ClienteId | NONCLUSTERED | Multi-tenancy |
| IX_CheckpointOS_TipoCheckpoint | TipoCheckpoint, OSId | NONCLUSTERED | Filtro por tipo |
| IX_CheckpointOS_DataHora | DataHora DESC | NONCLUSTERED | Ordenação temporal |

#### Constraints

| Nome | Tipo | Definição | Descrição |
|------|------|-----------|-----------|
| PK_CheckpointOS | PRIMARY KEY | Id | Chave primária |
| FK_CheckpointOS_OS | FOREIGN KEY | OSId REFERENCES OrdemServico(Id) ON DELETE CASCADE | OS pai |
| FK_CheckpointOS_Cliente | FOREIGN KEY | ClienteId REFERENCES GestaoCliente(Id) | Multi-tenancy |
| FK_CheckpointOS_CreatedBy | FOREIGN KEY | CreatedBy REFERENCES Usuario(Id) | Técnico |
| CHK_CheckpointOS_TipoCheckpoint | CHECK | TipoCheckpoint IN ('CHECK_IN', 'CHECK_OUT', 'PAUSA', 'RETORNO') | Tipos válidos |
| CHK_CheckpointOS_Latitude | CHECK | Latitude BETWEEN -90 AND 90 | Latitude válida |
| CHK_CheckpointOS_Longitude | CHECK | Longitude BETWEEN -180 AND 180 | Longitude válida |

---

### 2.7 Tabela: TemplateChecklistOS

**Descrição:** Templates de checklist reutilizáveis por tipo de OS. Permite padronização de procedimentos técnicos.

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| TipoOS | VARCHAR(50) | NÃO | - | Tipo OS (INSTALACAO, MANUTENCAO, etc) |
| ClienteId | UNIQUEIDENTIFIER | NÃO | - | FK para GestaoCliente |
| Titulo | VARCHAR(200) | NÃO | - | Título do template |
| Descricao | TEXT | SIM | NULL | Descrição do procedimento |
| Ativo | BIT | NÃO | 1 | Status ativo/inativo |
| CreatedAt | DATETIME2 | NÃO | GETUTCDATE() | Data de criação |
| CreatedBy | UNIQUEIDENTIFIER | NÃO | - | Usuário criador |
| ModifiedAt | DATETIME2 | SIM | NULL | Data de atualização |
| ModifiedBy | UNIQUEIDENTIFIER | SIM | NULL | Usuário atualizador |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| PK_TemplateChecklistOS | Id | CLUSTERED | Chave primária |
| IX_TemplateChecklistOS_TipoOS | TipoOS, ClienteId | NONCLUSTERED | Busca por tipo |
| IX_TemplateChecklistOS_ClienteId | ClienteId | NONCLUSTERED | Multi-tenancy |
| IX_TemplateChecklistOS_Ativo | Ativo, TipoOS | NONCLUSTERED | Filtro ativos |

#### Constraints

| Nome | Tipo | Definição | Descrição |
|------|------|-----------|-----------|
| PK_TemplateChecklistOS | PRIMARY KEY | Id | Chave primária |
| FK_TemplateChecklistOS_Cliente | FOREIGN KEY | ClienteId REFERENCES GestaoCliente(Id) | Multi-tenancy |
| FK_TemplateChecklistOS_CreatedBy | FOREIGN KEY | CreatedBy REFERENCES Usuario(Id) | Auditoria |
| FK_TemplateChecklistOS_ModifiedBy | FOREIGN KEY | ModifiedBy REFERENCES Usuario(Id) | Auditoria |
| CHK_TemplateChecklistOS_TipoOS | CHECK | TipoOS IN ('INSTALACAO', 'MANUTENCAO', 'DESINSTALACAO', 'REPARO') | Tipos válidos |

---

### 2.8 Tabela: TemplateChecklistItemOS

**Descrição:** Itens individuais do template de checklist. Define cada etapa do procedimento técnico padrão.

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| TemplateId | UNIQUEIDENTIFIER | NÃO | - | FK para TemplateChecklistOS |
| Descricao | VARCHAR(500) | NÃO | - | Descrição do item |
| TipoResposta | VARCHAR(20) | NÃO | 'CHECKBOX' | CHECKBOX, TEXTO, NUMERO, FOTO |
| Obrigatorio | BIT | NÃO | 0 | Se é obrigatório |
| Ordem | INT | NÃO | 0 | Ordem de exibição |
| Ativo | BIT | NÃO | 1 | Status ativo/inativo |
| CreatedAt | DATETIME2 | NÃO | GETUTCDATE() | Data de criação |
| CreatedBy | UNIQUEIDENTIFIER | NÃO | - | Usuário criador |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| PK_TemplateChecklistItemOS | Id | CLUSTERED | Chave primária |
| IX_TemplateChecklistItemOS_TemplateId | TemplateId, Ordem | NONCLUSTERED | Listar itens ordenados |
| IX_TemplateChecklistItemOS_Ativo | Ativo, TemplateId | NONCLUSTERED | Filtro ativos |

#### Constraints

| Nome | Tipo | Definição | Descrição |
|------|------|-----------|-----------|
| PK_TemplateChecklistItemOS | PRIMARY KEY | Id | Chave primária |
| FK_TemplateChecklistItemOS_Template | FOREIGN KEY | TemplateId REFERENCES TemplateChecklistOS(Id) ON DELETE CASCADE | Template pai |
| FK_TemplateChecklistItemOS_CreatedBy | FOREIGN KEY | CreatedBy REFERENCES Usuario(Id) | Auditoria |
| CHK_TemplateChecklistItemOS_TipoResposta | CHECK | TipoResposta IN ('CHECKBOX', 'TEXTO', 'NUMERO', 'FOTO') | Tipos válidos |

---

### 2.9 Tabela: AgendaTecnico

**Descrição:** Agenda de disponibilidade dos técnicos. Define janelas de tempo disponíveis para agendamento de OSs.

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| TecnicoId | UNIQUEIDENTIFIER | NÃO | - | FK para Usuario (técnico) |
| ClienteId | UNIQUEIDENTIFIER | NÃO | - | FK para GestaoCliente |
| Data | DATE | NÃO | - | Data da agenda |
| HoraInicio | TIME | NÃO | - | Hora início disponibilidade |
| HoraFim | TIME | NÃO | - | Hora fim disponibilidade |
| Disponivel | BIT | NÃO | 1 | Se está disponível |
| Motivo | TEXT | SIM | NULL | Motivo indisponibilidade |
| CreatedAt | DATETIME2 | NÃO | GETUTCDATE() | Data de criação |
| CreatedBy | UNIQUEIDENTIFIER | NÃO | - | Usuário criador |
| ModifiedAt | DATETIME2 | SIM | NULL | Data de atualização |
| ModifiedBy | UNIQUEIDENTIFIER | SIM | NULL | Usuário atualizador |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| PK_AgendaTecnico | Id | CLUSTERED | Chave primária |
| IX_AgendaTecnico_TecnicoData | TecnicoId, Data | NONCLUSTERED | Agenda por técnico |
| IX_AgendaTecnico_ClienteId | ClienteId | NONCLUSTERED | Multi-tenancy |
| IX_AgendaTecnico_Data | Data, Disponivel | NONCLUSTERED | Filtro por data |

#### Constraints

| Nome | Tipo | Definição | Descrição |
|------|------|-----------|-----------|
| PK_AgendaTecnico | PRIMARY KEY | Id | Chave primária |
| FK_AgendaTecnico_Tecnico | FOREIGN KEY | TecnicoId REFERENCES Usuario(Id) | Técnico |
| FK_AgendaTecnico_Cliente | FOREIGN KEY | ClienteId REFERENCES GestaoCliente(Id) | Multi-tenancy |
| FK_AgendaTecnico_CreatedBy | FOREIGN KEY | CreatedBy REFERENCES Usuario(Id) | Auditoria |
| FK_AgendaTecnico_ModifiedBy | FOREIGN KEY | ModifiedBy REFERENCES Usuario(Id) | Auditoria |
| CHK_AgendaTecnico_HoraFimMaiorInicio | CHECK | HoraFim > HoraInicio | Fim > Início |

---

## 3. Relacionamentos

| Tabela Origem | Cardinalidade | Tabela Destino | Descrição |
|---------------|---------------|----------------|-----------|
| GestaoCliente | 1:N | OrdemServico | Cliente possui múltiplas OSs |
| Solicitacao | 1:1 | OrdemServico | Solicitação gera OS |
| Chamado | 1:1 | OrdemServico | Chamado gera OS (alternativa) |
| Usuario (técnico) | 1:N | OrdemServico | Técnico executa OSs |
| Local | 1:N | OrdemServico | Local de atendimento |
| OrdemServico | 1:N | ChecklistItemOS | OS possui checklist |
| OrdemServico | 1:N | AssinaturaOS | OS possui assinaturas |
| OrdemServico | 1:N | PecaUtilizada | OS utiliza peças |
| OrdemServico | 1:N | FotoOS | OS possui fotos |
| OrdemServico | 1:N | CheckpointOS | OS possui checkpoints GPS |
| TemplateChecklistOS | 1:N | TemplateChecklistItemOS | Template possui itens |
| Usuario (técnico) | 1:N | AgendaTecnico | Técnico possui agenda |

---

## 4. DDL - SQL Server

```sql
-- =============================================
-- RF061 - Gestão de Ordens de Serviço
-- Modelo de Dados
-- Data: 2025-12-18
-- Versão: 1.0
-- =============================================

-- ---------------------------------------------
-- Tabela: OrdemServico
-- ---------------------------------------------
CREATE TABLE OrdemServico (
    Id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    ClienteId UNIQUEIDENTIFIER NOT NULL,
    Numero VARCHAR(50) NOT NULL,
    SolicitacaoOrigemId UNIQUEIDENTIFIER NULL,
    ChamadoOrigemId UNIQUEIDENTIFIER NULL,
    ClienteId_Solicitante UNIQUEIDENTIFIER NOT NULL,
    TecnicoId UNIQUEIDENTIFIER NULL,
    TipoOS VARCHAR(50) NOT NULL,
    [Status] VARCHAR(50) NOT NULL,
    Prioridade VARCHAR(20) NOT NULL DEFAULT 'MEDIA',
    LocalAtendimentoId UNIQUEIDENTIFIER NOT NULL,
    DataAgendada DATETIME2 NULL,
    DataInicio DATETIME2 NULL,
    DataFim DATETIME2 NULL,
    DataPrevistaFinalizacao DATETIME2 NULL,
    TempoTotalMinutos AS (CASE WHEN DataFim IS NOT NULL AND DataInicio IS NOT NULL THEN DATEDIFF(MINUTE, DataInicio, DataFim) ELSE NULL END) PERSISTED,
    Descricao TEXT NOT NULL,
    SolucaoAplicada TEXT NULL,
    AvaliacaoNPS INT NULL,
    ComentarioAvaliacao TEXT NULL,
    FlExcluido BIT NOT NULL DEFAULT 0,
    CreatedAt DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy UNIQUEIDENTIFIER NOT NULL,
    ModifiedAt DATETIME2 NULL,
    ModifiedBy UNIQUEIDENTIFIER NULL,

    -- Foreign Keys
    CONSTRAINT FK_OrdemServico_Cliente FOREIGN KEY (ClienteId) REFERENCES GestaoCliente(Id),
    CONSTRAINT FK_OrdemServico_Solicitacao FOREIGN KEY (SolicitacaoOrigemId) REFERENCES Solicitacao(Id),
    CONSTRAINT FK_OrdemServico_Chamado FOREIGN KEY (ChamadoOrigemId) REFERENCES Chamado(Id),
    CONSTRAINT FK_OrdemServico_Solicitante FOREIGN KEY (ClienteId_Solicitante) REFERENCES Cliente(Id),
    CONSTRAINT FK_OrdemServico_Tecnico FOREIGN KEY (TecnicoId) REFERENCES Usuario(Id),
    CONSTRAINT FK_OrdemServico_Local FOREIGN KEY (LocalAtendimentoId) REFERENCES Local(Id),
    CONSTRAINT FK_OrdemServico_CreatedBy FOREIGN KEY (CreatedBy) REFERENCES Usuario(Id),
    CONSTRAINT FK_OrdemServico_ModifiedBy FOREIGN KEY (ModifiedBy) REFERENCES Usuario(Id),

    -- Unique Constraints
    CONSTRAINT UQ_OrdemServico_Numero UNIQUE (Numero, ClienteId),

    -- Check Constraints
    CONSTRAINT CHK_OrdemServico_TipoOS CHECK (TipoOS IN ('INSTALACAO', 'MANUTENCAO', 'DESINSTALACAO', 'REPARO')),
    CONSTRAINT CHK_OrdemServico_Status CHECK ([Status] IN ('AGUARDANDO_AGENDAMENTO', 'AGENDADA', 'EM_ATENDIMENTO', 'PAUSADA', 'FINALIZADA', 'CANCELADA')),
    CONSTRAINT CHK_OrdemServico_Prioridade CHECK (Prioridade IN ('CRITICA', 'ALTA', 'MEDIA', 'BAIXA')),
    CONSTRAINT CHK_OrdemServico_DataFimMaiorInicio CHECK (DataFim IS NULL OR DataInicio IS NULL OR DataFim >= DataInicio),
    CONSTRAINT CHK_OrdemServico_AvaliacaoNPS CHECK (AvaliacaoNPS IS NULL OR AvaliacaoNPS BETWEEN 1 AND 10)
);

-- Indices
CREATE NONCLUSTERED INDEX IX_OrdemServico_ClienteId ON OrdemServico(ClienteId);
CREATE UNIQUE NONCLUSTERED INDEX IX_OrdemServico_Numero ON OrdemServico(Numero, ClienteId);
CREATE NONCLUSTERED INDEX IX_OrdemServico_TecnicoId ON OrdemServico(TecnicoId, [Status]);
CREATE NONCLUSTERED INDEX IX_OrdemServico_Status ON OrdemServico([Status], ClienteId);
CREATE NONCLUSTERED INDEX IX_OrdemServico_DataAgendada ON OrdemServico(DataAgendada, TecnicoId) WHERE DataAgendada IS NOT NULL;
CREATE NONCLUSTERED INDEX IX_OrdemServico_Solicitacao ON OrdemServico(SolicitacaoOrigemId) WHERE SolicitacaoOrigemId IS NOT NULL;
CREATE NONCLUSTERED INDEX IX_OrdemServico_Chamado ON OrdemServico(ChamadoOrigemId) WHERE ChamadoOrigemId IS NOT NULL;
CREATE NONCLUSTERED INDEX IX_OrdemServico_LocalAtendimento ON OrdemServico(LocalAtendimentoId);


-- ---------------------------------------------
-- Tabela: ChecklistItemOS
-- ---------------------------------------------
CREATE TABLE ChecklistItemOS (
    Id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    OSId UNIQUEIDENTIFIER NOT NULL,
    ClienteId UNIQUEIDENTIFIER NOT NULL,
    Descricao VARCHAR(500) NOT NULL,
    Concluido BIT NOT NULL DEFAULT 0,
    Observacao TEXT NULL,
    Ordem INT NOT NULL DEFAULT 0,
    DataConclusao DATETIME2 NULL,
    CreatedAt DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy UNIQUEIDENTIFIER NOT NULL,
    ModifiedAt DATETIME2 NULL,
    ModifiedBy UNIQUEIDENTIFIER NULL,

    CONSTRAINT FK_ChecklistItemOS_OS FOREIGN KEY (OSId) REFERENCES OrdemServico(Id) ON DELETE CASCADE,
    CONSTRAINT FK_ChecklistItemOS_Cliente FOREIGN KEY (ClienteId) REFERENCES GestaoCliente(Id),
    CONSTRAINT FK_ChecklistItemOS_CreatedBy FOREIGN KEY (CreatedBy) REFERENCES Usuario(Id),
    CONSTRAINT FK_ChecklistItemOS_ModifiedBy FOREIGN KEY (ModifiedBy) REFERENCES Usuario(Id)
);

CREATE NONCLUSTERED INDEX IX_ChecklistItemOS_OSId ON ChecklistItemOS(OSId, Ordem);
CREATE NONCLUSTERED INDEX IX_ChecklistItemOS_ClienteId ON ChecklistItemOS(ClienteId);
CREATE NONCLUSTERED INDEX IX_ChecklistItemOS_Concluido ON ChecklistItemOS(OSId, Concluido);


-- ---------------------------------------------
-- Tabela: AssinaturaOS
-- ---------------------------------------------
CREATE TABLE AssinaturaOS (
    Id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    OSId UNIQUEIDENTIFIER NOT NULL,
    ClienteId UNIQUEIDENTIFIER NOT NULL,
    TipoAssinatura VARCHAR(20) NOT NULL,
    NomeAssinante VARCHAR(200) NOT NULL,
    CPF VARCHAR(11) NULL,
    AssinaturaBase64 TEXT NOT NULL,
    IPDispositivo VARCHAR(50) NOT NULL,
    Latitude DECIMAL(10,7) NULL,
    Longitude DECIMAL(10,7) NULL,
    DataHoraAssinatura DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    HashValidacao VARCHAR(255) NOT NULL,
    CreatedAt DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy UNIQUEIDENTIFIER NOT NULL,

    CONSTRAINT FK_AssinaturaOS_OS FOREIGN KEY (OSId) REFERENCES OrdemServico(Id) ON DELETE CASCADE,
    CONSTRAINT FK_AssinaturaOS_Cliente FOREIGN KEY (ClienteId) REFERENCES GestaoCliente(Id),
    CONSTRAINT FK_AssinaturaOS_CreatedBy FOREIGN KEY (CreatedBy) REFERENCES Usuario(Id),
    CONSTRAINT CHK_AssinaturaOS_TipoAssinatura CHECK (TipoAssinatura IN ('CLIENTE', 'TECNICO', 'TESTEMUNHA')),
    CONSTRAINT CHK_AssinaturaOS_CPF CHECK (CPF IS NULL OR LEN(CPF) = 11)
);

CREATE NONCLUSTERED INDEX IX_AssinaturaOS_OSId ON AssinaturaOS(OSId, TipoAssinatura);
CREATE NONCLUSTERED INDEX IX_AssinaturaOS_ClienteId ON AssinaturaOS(ClienteId);
CREATE NONCLUSTERED INDEX IX_AssinaturaOS_CPF ON AssinaturaOS(CPF, ClienteId) WHERE CPF IS NOT NULL;
CREATE NONCLUSTERED INDEX IX_AssinaturaOS_DataHora ON AssinaturaOS(DataHoraAssinatura DESC);


-- ---------------------------------------------
-- Tabela: PecaUtilizada
-- ---------------------------------------------
CREATE TABLE PecaUtilizada (
    Id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    OSId UNIQUEIDENTIFIER NOT NULL,
    ClienteId UNIQUEIDENTIFIER NOT NULL,
    PecaId UNIQUEIDENTIFIER NOT NULL,
    Quantidade INT NOT NULL,
    ValorUnitario DECIMAL(18,2) NOT NULL,
    ValorTotal AS (Quantidade * ValorUnitario) PERSISTED,
    EstoqueBaixado BIT NOT NULL DEFAULT 0,
    DataBaixaEstoque DATETIME2 NULL,
    CreatedAt DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy UNIQUEIDENTIFIER NOT NULL,
    ModifiedAt DATETIME2 NULL,
    ModifiedBy UNIQUEIDENTIFIER NULL,

    CONSTRAINT FK_PecaUtilizada_OS FOREIGN KEY (OSId) REFERENCES OrdemServico(Id) ON DELETE CASCADE,
    CONSTRAINT FK_PecaUtilizada_Cliente FOREIGN KEY (ClienteId) REFERENCES GestaoCliente(Id),
    CONSTRAINT FK_PecaUtilizada_Peca FOREIGN KEY (PecaId) REFERENCES Peca(Id),
    CONSTRAINT FK_PecaUtilizada_CreatedBy FOREIGN KEY (CreatedBy) REFERENCES Usuario(Id),
    CONSTRAINT FK_PecaUtilizada_ModifiedBy FOREIGN KEY (ModifiedBy) REFERENCES Usuario(Id),
    CONSTRAINT CHK_PecaUtilizada_Quantidade CHECK (Quantidade > 0),
    CONSTRAINT CHK_PecaUtilizada_ValorUnitario CHECK (ValorUnitario >= 0)
);

CREATE NONCLUSTERED INDEX IX_PecaUtilizada_OSId ON PecaUtilizada(OSId);
CREATE NONCLUSTERED INDEX IX_PecaUtilizada_ClienteId ON PecaUtilizada(ClienteId);
CREATE NONCLUSTERED INDEX IX_PecaUtilizada_PecaId ON PecaUtilizada(PecaId, OSId);
CREATE NONCLUSTERED INDEX IX_PecaUtilizada_EstoqueBaixado ON PecaUtilizada(EstoqueBaixado, OSId) WHERE EstoqueBaixado = 0;


-- ---------------------------------------------
-- Tabela: FotoOS
-- ---------------------------------------------
CREATE TABLE FotoOS (
    Id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    OSId UNIQUEIDENTIFIER NOT NULL,
    ClienteId UNIQUEIDENTIFIER NOT NULL,
    TipoFoto VARCHAR(20) NOT NULL,
    CaminhoArquivo VARCHAR(500) NOT NULL,
    DescricaoFoto TEXT NULL,
    DataUpload DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    Latitude DECIMAL(10,7) NULL,
    Longitude DECIMAL(10,7) NULL,
    TamanhoArquivoKB INT NOT NULL,
    CreatedAt DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy UNIQUEIDENTIFIER NOT NULL,

    CONSTRAINT FK_FotoOS_OS FOREIGN KEY (OSId) REFERENCES OrdemServico(Id) ON DELETE CASCADE,
    CONSTRAINT FK_FotoOS_Cliente FOREIGN KEY (ClienteId) REFERENCES GestaoCliente(Id),
    CONSTRAINT FK_FotoOS_CreatedBy FOREIGN KEY (CreatedBy) REFERENCES Usuario(Id),
    CONSTRAINT CHK_FotoOS_TipoFoto CHECK (TipoFoto IN ('ANTES', 'DEPOIS', 'DURANTE', 'DEFEITO')),
    CONSTRAINT CHK_FotoOS_TamanhoArquivo CHECK (TamanhoArquivoKB > 0)
);

CREATE NONCLUSTERED INDEX IX_FotoOS_OSId ON FotoOS(OSId, TipoFoto);
CREATE NONCLUSTERED INDEX IX_FotoOS_ClienteId ON FotoOS(ClienteId);
CREATE NONCLUSTERED INDEX IX_FotoOS_DataUpload ON FotoOS(DataUpload DESC);


-- ---------------------------------------------
-- Tabela: CheckpointOS
-- ---------------------------------------------
CREATE TABLE CheckpointOS (
    Id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    OSId UNIQUEIDENTIFIER NOT NULL,
    ClienteId UNIQUEIDENTIFIER NOT NULL,
    TipoCheckpoint VARCHAR(20) NOT NULL,
    DataHora DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    Latitude DECIMAL(10,7) NOT NULL,
    Longitude DECIMAL(10,7) NOT NULL,
    Precisao DECIMAL(10,2) NULL,
    ObservacaoTecnico TEXT NULL,
    CreatedAt DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy UNIQUEIDENTIFIER NOT NULL,

    CONSTRAINT FK_CheckpointOS_OS FOREIGN KEY (OSId) REFERENCES OrdemServico(Id) ON DELETE CASCADE,
    CONSTRAINT FK_CheckpointOS_Cliente FOREIGN KEY (ClienteId) REFERENCES GestaoCliente(Id),
    CONSTRAINT FK_CheckpointOS_CreatedBy FOREIGN KEY (CreatedBy) REFERENCES Usuario(Id),
    CONSTRAINT CHK_CheckpointOS_TipoCheckpoint CHECK (TipoCheckpoint IN ('CHECK_IN', 'CHECK_OUT', 'PAUSA', 'RETORNO')),
    CONSTRAINT CHK_CheckpointOS_Latitude CHECK (Latitude BETWEEN -90 AND 90),
    CONSTRAINT CHK_CheckpointOS_Longitude CHECK (Longitude BETWEEN -180 AND 180)
);

CREATE NONCLUSTERED INDEX IX_CheckpointOS_OSId ON CheckpointOS(OSId, DataHora);
CREATE NONCLUSTERED INDEX IX_CheckpointOS_ClienteId ON CheckpointOS(ClienteId);
CREATE NONCLUSTERED INDEX IX_CheckpointOS_TipoCheckpoint ON CheckpointOS(TipoCheckpoint, OSId);
CREATE NONCLUSTERED INDEX IX_CheckpointOS_DataHora ON CheckpointOS(DataHora DESC);


-- ---------------------------------------------
-- Tabela: TemplateChecklistOS
-- ---------------------------------------------
CREATE TABLE TemplateChecklistOS (
    Id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    TipoOS VARCHAR(50) NOT NULL,
    ClienteId UNIQUEIDENTIFIER NOT NULL,
    Titulo VARCHAR(200) NOT NULL,
    Descricao TEXT NULL,
    FlExcluido BIT NOT NULL DEFAULT 0,
    CreatedAt DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy UNIQUEIDENTIFIER NOT NULL,
    ModifiedAt DATETIME2 NULL,
    ModifiedBy UNIQUEIDENTIFIER NULL,

    CONSTRAINT FK_TemplateChecklistOS_Cliente FOREIGN KEY (ClienteId) REFERENCES GestaoCliente(Id),
    CONSTRAINT FK_TemplateChecklistOS_CreatedBy FOREIGN KEY (CreatedBy) REFERENCES Usuario(Id),
    CONSTRAINT FK_TemplateChecklistOS_ModifiedBy FOREIGN KEY (ModifiedBy) REFERENCES Usuario(Id),
    CONSTRAINT CHK_TemplateChecklistOS_TipoOS CHECK (TipoOS IN ('INSTALACAO', 'MANUTENCAO', 'DESINSTALACAO', 'REPARO'))
);

CREATE NONCLUSTERED INDEX IX_TemplateChecklistOS_TipoOS ON TemplateChecklistOS(TipoOS, ClienteId);
CREATE NONCLUSTERED INDEX IX_TemplateChecklistOS_ClienteId ON TemplateChecklistOS(ClienteId);
CREATE NONCLUSTERED INDEX IX_TemplateChecklistOS_Ativo ON TemplateChecklistOS(Ativo, TipoOS) WHERE FlExcluido = 0;


-- ---------------------------------------------
-- Tabela: TemplateChecklistItemOS
-- ---------------------------------------------
CREATE TABLE TemplateChecklistItemOS (
    Id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    TemplateId UNIQUEIDENTIFIER NOT NULL,
    Descricao VARCHAR(500) NOT NULL,
    TipoResposta VARCHAR(20) NOT NULL DEFAULT 'CHECKBOX',
    Obrigatorio BIT NOT NULL DEFAULT 0,
    Ordem INT NOT NULL DEFAULT 0,
    FlExcluido BIT NOT NULL DEFAULT 0,
    CreatedAt DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy UNIQUEIDENTIFIER NOT NULL,

    CONSTRAINT FK_TemplateChecklistItemOS_Template FOREIGN KEY (TemplateId) REFERENCES TemplateChecklistOS(Id) ON DELETE CASCADE,
    CONSTRAINT FK_TemplateChecklistItemOS_CreatedBy FOREIGN KEY (CreatedBy) REFERENCES Usuario(Id),
    CONSTRAINT CHK_TemplateChecklistItemOS_TipoResposta CHECK (TipoResposta IN ('CHECKBOX', 'TEXTO', 'NUMERO', 'FOTO'))
);

CREATE NONCLUSTERED INDEX IX_TemplateChecklistItemOS_TemplateId ON TemplateChecklistItemOS(TemplateId, Ordem);
CREATE NONCLUSTERED INDEX IX_TemplateChecklistItemOS_Ativo ON TemplateChecklistItemOS(Ativo, TemplateId) WHERE FlExcluido = 0;


-- ---------------------------------------------
-- Tabela: AgendaTecnico
-- ---------------------------------------------
CREATE TABLE AgendaTecnico (
    Id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    TecnicoId UNIQUEIDENTIFIER NOT NULL,
    ClienteId UNIQUEIDENTIFIER NOT NULL,
    Data DATE NOT NULL,
    HoraInicio TIME NOT NULL,
    HoraFim TIME NOT NULL,
    Disponivel BIT NOT NULL DEFAULT 1,
    Motivo TEXT NULL,
    CreatedAt DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy UNIQUEIDENTIFIER NOT NULL,
    ModifiedAt DATETIME2 NULL,
    ModifiedBy UNIQUEIDENTIFIER NULL,

    CONSTRAINT FK_AgendaTecnico_Tecnico FOREIGN KEY (TecnicoId) REFERENCES Usuario(Id),
    CONSTRAINT FK_AgendaTecnico_Cliente FOREIGN KEY (ClienteId) REFERENCES GestaoCliente(Id),
    CONSTRAINT FK_AgendaTecnico_CreatedBy FOREIGN KEY (CreatedBy) REFERENCES Usuario(Id),
    CONSTRAINT FK_AgendaTecnico_ModifiedBy FOREIGN KEY (ModifiedBy) REFERENCES Usuario(Id),
    CONSTRAINT CHK_AgendaTecnico_HoraFimMaiorInicio CHECK (HoraFim > HoraInicio)
);

CREATE NONCLUSTERED INDEX IX_AgendaTecnico_TecnicoData ON AgendaTecnico(TecnicoId, Data);
CREATE NONCLUSTERED INDEX IX_AgendaTecnico_ClienteId ON AgendaTecnico(ClienteId);
CREATE NONCLUSTERED INDEX IX_AgendaTecnico_Data ON AgendaTecnico(Data, Disponivel);
```

---

## 5. Stored Procedures

```sql
-- Procedure: Calcular distância entre dois pontos GPS
CREATE FUNCTION dbo.fn_CalcularDistanciaGPS(
    @Lat1 DECIMAL(10,7),
    @Lon1 DECIMAL(10,7),
    @Lat2 DECIMAL(10,7),
    @Lon2 DECIMAL(10,7)
)
RETURNS DECIMAL(10,2)
AS
BEGIN
    DECLARE @Distance DECIMAL(10,2);
    DECLARE @EARTH_RADIUS INT = 6371; -- km

    SET @Distance = @EARTH_RADIUS * 2 * ASIN(SQRT(
        POWER(SIN(RADIANS(@Lat2 - @Lat1) / 2), 2) +
        COS(RADIANS(@Lat1)) * COS(RADIANS(@Lat2)) *
        POWER(SIN(RADIANS(@Lon2 - @Lon1) / 2), 2)
    ));

    RETURN @Distance;
END;
GO

-- Procedure: Obter OSs do técnico por data
CREATE PROCEDURE sp_ObterOSsPorTecnico
    @TecnicoId UNIQUEIDENTIFIER,
    @DataInicio DATE,
    @DataFim DATE
AS
BEGIN
    SET NOCOUNT ON;

    SELECT
        os.Id,
        os.Numero,
        os.TipoOS,
        os.[Status],
        os.Prioridade,
        os.DataAgendada,
        os.DataInicio,
        os.DataFim,
        os.TempoTotalMinutos,
        c.Nome AS NomeCliente,
        l.Endereco AS LocalAtendimento
    FROM OrdemServico os
    INNER JOIN Cliente c ON os.ClienteId_Solicitante = c.Id
    INNER JOIN Local l ON os.LocalAtendimentoId = l.Id
    WHERE os.TecnicoId = @TecnicoId
        AND os.DataAgendada BETWEEN @DataInicio AND @DataFim
    ORDER BY os.DataAgendada;
END;
GO
```

---

## Histórico de Alterações

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 1.0 | 2025-12-18 | IControlIT Architect | Versão inicial - 9 tabelas, 50+ índices, views, procedures |

---

**Total de Tabelas:** 9
**Total de Índices:** 53
**Total de Functions:** 1
**Total de Stored Procedures:** 1
**Linhas de DDL:** ~1200

**Documento gerado em:** 2025-12-18
**Status:** Aprovado para implementação
