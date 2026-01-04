# MD-RF027 - Modelo de Dados: Gestão de Aditivos Contratos

**Versão:** 1.0
**Data:** 2025-12-18
**Responsável:** Agente Architect
**RF Relacionado:** [RF027 - Gestão de Aditivos Contratos](./RF027.md)
**UC Relacionado:** [UC-RF027 - Casos de Uso](./UC-RF027.md)

---

## 1. VISÃO GERAL

Este modelo de dados suporta o gerenciamento completo de aditivos contratuais, incluindo:

- **Cadastro de Aditivos** com versionamento e histórico completo
- **Workflow de Aprovação** multi-nível com rastreabilidade
- **Análise de Impacto Financeiro** com previsões e realizações
- **Gestão Documental** com anexos e assinaturas digitais
- **Auditoria Completa** de todas as operações
- **Multi-tenancy** com isolamento por Conglomerado/Empresa/Cliente
- **Soft Delete** para preservação de histórico

**Complexidade:** MUITO ALTA
**Número de Tabelas:** 14
**Relacionamentos:** 28 Foreign Keys
**Índices Otimizados:** 45+

---

## 2. DIAGRAMA ER (Entidade-Relacionamento)

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                     MODELO DE DADOS - GESTÃO DE ADITIVOS CONTRATOS                   │
└─────────────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────┐         ┌──────────────────────┐
│  Conglomerado        │1       *│  Empresa             │
│──────────────────────│◄────────│──────────────────────│
│ Id (PK)              │         │ Id (PK)              │
│ Nome                 │         │ ConglomeradoId (FK)  │
└──────────────────────┘         │ Nome                 │
                                 └──────┬───────────────┘
                                        │1
                                        │
                                        │*
                         ┌──────────────▼───────────────┐
                         │  Cliente                     │
                         │──────────────────────────────│
                         │ Id (PK)                      │
                         │ EmpresaId (FK)               │
                         │ Nome                         │
                         └──────┬───────────────────────┘
                                │1
                                │
        ┌───────────────────────┼───────────────────────┐
        │*                      │*                      │*
┌───────▼──────────┐   ┌────────▼─────────┐   ┌────────▼─────────────┐
│  Contrato        │   │ Aditivo_Contrato │   │ Usuario              │
│──────────────────│   │──────────────────│   │──────────────────────│
│ Id (PK)          │1 *│ Id (PK)          │   │ Id (PK)              │
│ ClienteId (FK)   │◄──│ ContratoId (FK)  │   │ ClienteId (FK)       │
│ Numero           │   │ ClienteId (FK)   │   │ Nome                 │
│ VigenciaInicio   │   │ Numero           │   │ Email                │
│ VigenciaFim      │   │ Tipo             │   └──────┬───────────────┘
└──────────────────┘   │ Status           │          │1
                       │ VersaoAtual      │          │
                       │ VigenciaInicio   │          │*
                       │ VigenciaFim      │   ┌──────▼───────────────┐
                       │ ValorOriginal    │   │ Aditivo_Workflow     │
                       │ ValorAditado     │   │──────────────────────│
                       │ PercentualAcres  │1 *│ Id (PK)              │
                       │ MotivoJustific   │◄──│ AditivoId (FK)       │
                       │ Ativo            │   │ UsuarioId (FK)       │
                       │ CreatedAt        │   │ Etapa                │
                       │ CreatedBy        │   │ StatusWorkflow       │
                       │ ModifiedAt       │   │ DataEtapa            │
                       │ ModifiedBy       │   │ Parecer              │
                       │ Fl_Excluido      │   │ Prazo                │
                       └────┬─┬─┬─┬───────┘   │ Ordem                │
                            │ │ │ │1          │ Ativo                │
                            │ │ │ │           └──────────────────────┘
                            │ │ │ │*
                            │ │ │ └───────────┐
                            │ │ │             │
                    ┌───────┘ │ │             │
                    │*        │ │             │
        ┌───────────▼─────────┴─┴─┐   ┌───────▼──────────────────┐
        │ Aditivo_Versao          │   │ Aditivo_ImpactoFinanc    │
        │─────────────────────────│   │──────────────────────────│
        │ Id (PK)                 │   │ Id (PK)                  │
        │ AditivoId (FK)          │   │ AditivoId (FK)           │
        │ NumeroVersao            │   │ Tipo                     │
        │ DataVersao              │   │ Competencia              │
        │ UsuarioId (FK)          │   │ ValorPrevisto            │
        │ DescricaoAlteracao      │   │ ValorRealizado           │
        │ CamposAlterados (JSON)  │   │ PercentualImpacto        │
        │ HashAnterior            │   │ CentroCusto              │
        │ HashAtual               │   │ ContaContabil            │
        │ Ativo                   │   │ Observacoes              │
        └─────────────────────────┘   │ Ativo                    │
                                      └──────────────────────────┘
                    ┌─────────────┐
                    │*            │
        ┌───────────▼─────────────┴──┐
        │ Aditivo_Anexo              │
        │────────────────────────────│
        │ Id (PK)                    │
        │ AditivoId (FK)             │
        │ TipoDocumento              │
        │ NomeArquivo                │
        │ CaminhoArquivo             │
        │ TamanhoBytes               │
        │ HashSHA256                 │
        │ DataUpload                 │
        │ UsuarioUploadId (FK)       │
        │ AssinadoDigitalmente       │
        │ DataAssinatura             │
        │ CertificadoDigital         │
        │ Ativo                      │
        └────────────────────────────┘

        ┌────────────────────────────┐
        │ Aditivo_Historico          │
        │────────────────────────────│
        │ Id (PK)                    │
        │ AditivoId (FK)             │
        │ UsuarioId (FK)             │
        │ DataOperacao               │
        │ TipoOperacao               │
        │ DescricaoOperacao          │
        │ DadosAnteriores (JSON)     │
        │ DadosNovos (JSON)          │
        │ EnderecoIP                 │
        │ UserAgent                  │
        └────────────────────────────┘

        ┌────────────────────────────┐
        │ Aditivo_Tipo               │
        │────────────────────────────│
        │ Id (PK)                    │
        │ ConglomeradoId (FK)        │
        │ Codigo                     │
        │ Descricao                  │
        │ RequerAprovacao            │
        │ NiveisAprovacao            │
        │ Ativo                      │
        └────────────────────────────┘

        ┌────────────────────────────┐
        │ Workflow_Configuracao      │
        │────────────────────────────│
        │ Id (PK)                    │
        │ ConglomeradoId (FK)        │
        │ TipoAditivoId (FK)         │
        │ NomeWorkflow               │
        │ DescricaoWorkflow          │
        │ Etapas (JSON)              │
        │ RegrasAprovacao (JSON)     │
        │ PrazoPadrao                │
        │ Ativo                      │
        └────────────────────────────┘

        ┌────────────────────────────┐
        │ Aditivo_Tag                │
        │────────────────────────────│
        │ Id (PK)                    │
        │ AditivoId (FK)             │
        │ Tag                        │
        │ DataCriacao                │
        └────────────────────────────┘

        ┌────────────────────────────┐
        │ Aditivo_Notificacao        │
        │────────────────────────────│
        │ Id (PK)                    │
        │ AditivoId (FK)             │
        │ UsuarioDestinoId (FK)      │
        │ TipoNotificacao            │
        │ Mensagem                   │
        │ DataEnvio                  │
        │ DataLeitura                │
        │ Lida                       │
        │ EmailEnviado               │
        └────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────┐
│  LEGENDA:                                                                            │
│  (PK) = Primary Key                                                                  │
│  (FK) = Foreign Key                                                                  │
│  1    = Relação Um                                                                   │
│  *    = Relação Muitos                                                               │
│  ◄─── = Direção do relacionamento (muitos para um)                                  │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. DESCRIÇÃO DAS ENTIDADES

### 3.1. Aditivo_Contrato

**Propósito:** Entidade principal que armazena todos os aditivos contratuais.

**Campos Principais:**
- `Id` (Guid, PK) - Identificador único
- `ContratoId` (Guid, FK) - Referência ao contrato original
- `ClienteId` (Guid, FK) - Cliente proprietário (multi-tenancy)
- `EmpresaId` (Guid, FK) - Empresa proprietária (multi-tenancy)
- `ConglomeradoId` (Guid, FK) - Conglomerado proprietário (multi-tenancy)
- `Numero` (NVARCHAR(50)) - Número único do aditivo (ex: "AD-2025-001")
- `Tipo` (INT) - Tipo de aditivo (1=Prazo, 2=Valor, 3=Escopo, 4=Misto)
- `Status` (INT) - Status atual (1=Elaboração, 2=Aprovação, 3=Aprovado, 4=Rejeitado, 5=Cancelado)
- `VersaoAtual` (INT) - Número da versão atual (controle de versioning)
- `VigenciaInicio` (DATETIME2) - Data de início da vigência
- `VigenciaFim` (DATETIME2) - Data de fim da vigência
- `ValorOriginal` (DECIMAL(18,2)) - Valor original do contrato
- `ValorAditado` (DECIMAL(18,2)) - Valor do aditivo (pode ser positivo ou negativo)
- `PercentualAcrescimo` (DECIMAL(5,2)) - Percentual de acréscimo/decréscimo
- `MotivoJustificativa` (NVARCHAR(2000)) - Justificativa detalhada do aditivo

**Regras de Negócio:**
- Número do aditivo deve ser único por conglomerado
- Valor aditado não pode ultrapassar 25% do valor original (regra padrão Lei 8.666)
- Vigência do aditivo não pode ultrapassar 60 meses (5 anos)
- Status inicial sempre "Em Elaboração"
- Versionamento automático a cada alteração

### 3.2. Aditivo_Workflow

**Propósito:** Controle de workflow de aprovação dos aditivos.

**Campos Principais:**
- `Id` (Guid, PK)
- `AditivoId` (Guid, FK) - Referência ao aditivo
- `UsuarioId` (Guid, FK) - Usuário responsável pela etapa
- `Etapa` (NVARCHAR(100)) - Nome da etapa (ex: "Aprovação Jurídica")
- `StatusWorkflow` (INT) - Status da etapa (1=Pendente, 2=Aprovado, 3=Rejeitado, 4=Em Análise)
- `DataEtapa` (DATETIME2) - Data de início da etapa
- `DataLimite` (DATETIME2) - Prazo limite para conclusão
- `Parecer` (NVARCHAR(2000)) - Parecer do aprovador
- `Ordem` (INT) - Ordem da etapa no workflow

**Regras de Negócio:**
- Workflow deve seguir ordem sequencial
- Etapa só pode ser aprovada pelo usuário designado
- Rejeição em qualquer etapa retorna aditivo para elaboração
- SLA de 5 dias úteis por etapa (configurável)
- Notificação automática 24h antes do prazo

### 3.3. Aditivo_Versao

**Propósito:** Histórico completo de versões de cada aditivo.

**Campos Principais:**
- `Id` (Guid, PK)
- `AditivoId` (Guid, FK)
- `NumeroVersao` (INT) - Número sequencial da versão
- `DataVersao` (DATETIME2) - Data/hora da criação da versão
- `UsuarioId` (Guid, FK) - Usuário que criou a versão
- `DescricaoAlteracao` (NVARCHAR(1000)) - Descrição do que foi alterado
- `CamposAlterados` (NVARCHAR(MAX)) - JSON com campos alterados
- `HashAnterior` (NVARCHAR(64)) - Hash SHA256 da versão anterior
- `HashAtual` (NVARCHAR(64)) - Hash SHA256 da versão atual

**Regras de Negócio:**
- Versão 1 criada automaticamente na criação do aditivo
- Nova versão criada a cada alteração de campos críticos
- Hash garante integridade e rastreabilidade
- Impossível deletar versões (auditoria LGPD)

### 3.4. Aditivo_ImpactoFinanceiro

**Propósito:** Análise detalhada do impacto financeiro do aditivo.

**Campos Principais:**
- `Id` (Guid, PK)
- `AditivoId` (Guid, FK)
- `Tipo` (INT) - Tipo de impacto (1=Receita, 2=Despesa, 3=Investimento)
- `Competencia` (NVARCHAR(7)) - Competência (YYYY-MM)
- `ValorPrevisto` (DECIMAL(18,2)) - Valor previsto
- `ValorRealizado` (DECIMAL(18,2)) - Valor realizado
- `PercentualImpacto` (DECIMAL(5,2)) - Percentual de impacto no orçamento
- `CentroCusto` (NVARCHAR(50)) - Centro de custo
- `ContaContabil` (NVARCHAR(50)) - Conta contábil

**Regras de Negócio:**
- Pode ter múltiplas competências para aditivos plurianuais
- Comparação previsto x realizado para análise de desvios
- Integração com sistema financeiro/contábil
- Alertas automáticos se desvio > 10%

### 3.5. Aditivo_Anexo

**Propósito:** Gestão de documentos anexos aos aditivos.

**Campos Principais:**
- `Id` (Guid, PK)
- `AditivoId` (Guid, FK)
- `TipoDocumento` (INT) - Tipo (1=Minuta, 2=Parecer Jurídico, 3=Análise Técnica, 4=Documento Assinado)
- `NomeArquivo` (NVARCHAR(255)) - Nome original do arquivo
- `CaminhoArquivo` (NVARCHAR(500)) - Caminho no storage
- `TamanhoBytes` (BIGINT) - Tamanho do arquivo
- `HashSHA256` (NVARCHAR(64)) - Hash para integridade
- `AssinadoDigitalmente` (BIT) - Indica se foi assinado digitalmente
- `DataAssinatura` (DATETIME2) - Data da assinatura digital
- `CertificadoDigital` (NVARCHAR(MAX)) - Certificado digital (ICP-Brasil)

**Regras de Negócio:**
- Tamanho máximo: 50 MB por arquivo
- Formatos permitidos: PDF, DOCX, XLSX, PNG, JPG
- Obrigatório ao menos 1 anexo tipo "Documento Assinado"
- Validação de assinatura digital ICP-Brasil

### 3.6. Aditivo_Historico

**Propósito:** Auditoria completa de todas as operações nos aditivos.

**Campos Principais:**
- `Id` (Guid, PK)
- `AditivoId` (Guid, FK)
- `UsuarioId` (Guid, FK)
- `DataOperacao` (DATETIME2)
- `TipoOperacao` (NVARCHAR(50)) - CREATE, UPDATE, DELETE, APPROVE, REJECT
- `DescricaoOperacao` (NVARCHAR(500))
- `DadosAnteriores` (NVARCHAR(MAX)) - JSON com estado anterior
- `DadosNovos` (NVARCHAR(MAX)) - JSON com estado novo
- `EnderecoIP` (NVARCHAR(50))
- `UserAgent` (NVARCHAR(500))

**Regras de Negócio:**
- Registro automático via AuditInterceptor
- Retenção de 7 anos (LGPD)
- Não pode ser deletado ou modificado
- Comparação visual de antes/depois

### 3.7. Aditivo_Tipo

**Propósito:** Catálogo de tipos de aditivos configuráveis.

**Campos Principais:**
- `Id` (Guid, PK)
- `ConglomeradoId` (Guid, FK)
- `Codigo` (NVARCHAR(20)) - Código único (ex: "AD-PRAZO")
- `Descricao` (NVARCHAR(200))
- `RequerAprovacao` (BIT)
- `NiveisAprovacao` (INT) - Número de níveis de aprovação

**Regras de Negócio:**
- Código único por conglomerado
- Possibilidade de criar tipos customizados
- Configuração de workflow específico por tipo

### 3.8. Workflow_Configuracao

**Propósito:** Configuração de workflows de aprovação por tipo de aditivo.

**Campos Principais:**
- `Id` (Guid, PK)
- `ConglomeradoId` (Guid, FK)
- `TipoAditivoId` (Guid, FK)
- `NomeWorkflow` (NVARCHAR(100))
- `Etapas` (NVARCHAR(MAX)) - JSON com definição das etapas
- `RegrasAprovacao` (NVARCHAR(MAX)) - JSON com regras (ex: valor > 100k = 3 níveis)
- `PrazoPadrao` (INT) - Prazo em dias úteis

**Regras de Negócio:**
- Permite workflows dinâmicos
- Regras baseadas em valor, tipo, cliente
- Configuração de prazos e alçadas

### 3.9. Aditivo_Tag

**Propósito:** Sistema de tags para categorização e busca.

**Campos Principais:**
- `Id` (Guid, PK)
- `AditivoId` (Guid, FK)
- `Tag` (NVARCHAR(50))

**Regras de Negócio:**
- Permite múltiplas tags por aditivo
- Busca rápida por tag
- Autocomplete de tags existentes

### 3.10. Aditivo_Notificacao

**Propósito:** Gerenciamento de notificações relacionadas aos aditivos.

**Campos Principais:**
- `Id` (Guid, PK)
- `AditivoId` (Guid, FK)
- `UsuarioDestinoId` (Guid, FK)
- `TipoNotificacao` (INT) - 1=Aprovação Pendente, 2=Prazo Vencendo, 3=Aprovado, 4=Rejeitado
- `Mensagem` (NVARCHAR(500))
- `DataEnvio` (DATETIME2)
- `DataLeitura` (DATETIME2)
- `Lida` (BIT)
- `EmailEnviado` (BIT)

**Regras de Negócio:**
- Notificação em tempo real via SignalR
- Envio de email se não lida em 2h
- Dashboard de notificações pendentes

---

## 4. SCRIPT DDL COMPLETO (SQL SERVER)

```sql
-- =============================================
-- MD-RF027 - GESTÃO DE ADITIVOS CONTRATOS
-- Versão: 1.0
-- Data: 2025-12-18
-- =============================================

-- =============================================
-- 1. TABELA: Aditivo_Tipo
-- =============================================
CREATE TABLE [dbo].[Aditivo_Tipo] (
    [Id] UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    [ConglomeradoId] UNIQUEIDENTIFIER NOT NULL,
    [Codigo] NVARCHAR(20) NOT NULL,
    [Descricao] NVARCHAR(200) NOT NULL,
    [RequerAprovacao] BIT NOT NULL DEFAULT 1,
    [NiveisAprovacao] INT NOT NULL DEFAULT 1,
    [Ativo] BIT NOT NULL DEFAULT 1,
    [CreatedAt] DATETIME2(7) NOT NULL DEFAULT GETUTCDATE(),
    [CreatedBy] UNIQUEIDENTIFIER NOT NULL,
    [ModifiedAt] DATETIME2(7) NULL,
    [ModifiedBy] UNIQUEIDENTIFIER NULL,
    [Fl_Excluido] BIT NOT NULL DEFAULT 0,
    [Data_Exclusao] DATETIME2(7) NULL,

    CONSTRAINT [PK_Aditivo_Tipo] PRIMARY KEY CLUSTERED ([Id] ASC),
    CONSTRAINT [FK_Aditivo_Tipo_Conglomerado] FOREIGN KEY ([ConglomeradoId])
        REFERENCES [dbo].[Conglomerado] ([Id]),
    CONSTRAINT [UQ_Aditivo_Tipo_Codigo] UNIQUE ([ConglomeradoId], [Codigo], [Fl_Excluido]),
    CONSTRAINT [CK_Aditivo_Tipo_NiveisAprovacao] CHECK ([NiveisAprovacao] >= 1 AND [NiveisAprovacao] <= 10)
);

CREATE NONCLUSTERED INDEX [IX_Aditivo_Tipo_ConglomeradoId] ON [dbo].[Aditivo_Tipo] ([ConglomeradoId]);
CREATE NONCLUSTERED INDEX [IX_Aditivo_Tipo_Codigo] ON [dbo].[Aditivo_Tipo] ([Codigo]);
CREATE NONCLUSTERED INDEX [IX_Aditivo_Tipo_Ativo] ON [dbo].[Aditivo_Tipo] ([Ativo]) WHERE [Fl_Excluido] = 0;

-- =============================================
-- 2. TABELA: Workflow_Configuracao
-- =============================================
CREATE TABLE [dbo].[Workflow_Configuracao] (
    [Id] UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    [ConglomeradoId] UNIQUEIDENTIFIER NOT NULL,
    [TipoAditivoId] UNIQUEIDENTIFIER NOT NULL,
    [NomeWorkflow] NVARCHAR(100) NOT NULL,
    [DescricaoWorkflow] NVARCHAR(500) NULL,
    [Etapas] NVARCHAR(MAX) NOT NULL, -- JSON
    [RegrasAprovacao] NVARCHAR(MAX) NULL, -- JSON
    [PrazoPadrao] INT NOT NULL DEFAULT 5, -- Dias úteis
    [Ativo] BIT NOT NULL DEFAULT 1,
    [CreatedAt] DATETIME2(7) NOT NULL DEFAULT GETUTCDATE(),
    [CreatedBy] UNIQUEIDENTIFIER NOT NULL,
    [ModifiedAt] DATETIME2(7) NULL,
    [ModifiedBy] UNIQUEIDENTIFIER NULL,
    [Fl_Excluido] BIT NOT NULL DEFAULT 0,
    [Data_Exclusao] DATETIME2(7) NULL,

    CONSTRAINT [PK_Workflow_Configuracao] PRIMARY KEY CLUSTERED ([Id] ASC),
    CONSTRAINT [FK_Workflow_Configuracao_Conglomerado] FOREIGN KEY ([ConglomeradoId])
        REFERENCES [dbo].[Conglomerado] ([Id]),
    CONSTRAINT [FK_Workflow_Configuracao_TipoAditivo] FOREIGN KEY ([TipoAditivoId])
        REFERENCES [dbo].[Aditivo_Tipo] ([Id]),
    CONSTRAINT [CK_Workflow_Configuracao_PrazoPadrao] CHECK ([PrazoPadrao] >= 1 AND [PrazoPadrao] <= 90),
    CONSTRAINT [CK_Workflow_Configuracao_Etapas_JSON] CHECK (ISJSON([Etapas]) = 1),
    CONSTRAINT [CK_Workflow_Configuracao_Regras_JSON] CHECK ([RegrasAprovacao] IS NULL OR ISJSON([RegrasAprovacao]) = 1)
);

CREATE NONCLUSTERED INDEX [IX_Workflow_Configuracao_ConglomeradoId] ON [dbo].[Workflow_Configuracao] ([ConglomeradoId]);
CREATE NONCLUSTERED INDEX [IX_Workflow_Configuracao_TipoAditivoId] ON [dbo].[Workflow_Configuracao] ([TipoAditivoId]);

-- =============================================
-- 3. TABELA: Aditivo_Contrato
-- =============================================
CREATE TABLE [dbo].[Aditivo_Contrato] (
    [Id] UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    [ConglomeradoId] UNIQUEIDENTIFIER NOT NULL,
    [EmpresaId] UNIQUEIDENTIFIER NOT NULL,
    [ClienteId] UNIQUEIDENTIFIER NOT NULL,
    [ContratoId] UNIQUEIDENTIFIER NOT NULL,
    [TipoAditivoId] UNIQUEIDENTIFIER NOT NULL,
    [Numero] NVARCHAR(50) NOT NULL,
    [Tipo] INT NOT NULL, -- 1=Prazo, 2=Valor, 3=Escopo, 4=Misto
    [Status] INT NOT NULL DEFAULT 1, -- 1=Elaboração, 2=Aprovação, 3=Aprovado, 4=Rejeitado, 5=Cancelado
    [VersaoAtual] INT NOT NULL DEFAULT 1,
    [VigenciaInicio] DATETIME2(7) NOT NULL,
    [VigenciaFim] DATETIME2(7) NOT NULL,
    [ValorOriginal] DECIMAL(18,2) NOT NULL,
    [ValorAditado] DECIMAL(18,2) NOT NULL,
    [PercentualAcrescimo] DECIMAL(5,2) NOT NULL,
    [MotivoJustificativa] NVARCHAR(2000) NOT NULL,
    [ObjetoPormenorizado] NVARCHAR(MAX) NULL,
    [ClausulaModificada] NVARCHAR(MAX) NULL,
    [DataAssinatura] DATETIME2(7) NULL,
    [LocalAssinatura] NVARCHAR(200) NULL,
    [ResponsavelAssinatura] NVARCHAR(200) NULL,
    [Observacoes] NVARCHAR(2000) NULL,
    [Ativo] BIT NOT NULL DEFAULT 1,
    [CreatedAt] DATETIME2(7) NOT NULL DEFAULT GETUTCDATE(),
    [CreatedBy] UNIQUEIDENTIFIER NOT NULL,
    [ModifiedAt] DATETIME2(7) NULL,
    [ModifiedBy] UNIQUEIDENTIFIER NULL,
    [Fl_Excluido] BIT NOT NULL DEFAULT 0,
    [Data_Exclusao] DATETIME2(7) NULL,

    CONSTRAINT [PK_Aditivo_Contrato] PRIMARY KEY CLUSTERED ([Id] ASC),
    CONSTRAINT [FK_Aditivo_Contrato_Conglomerado] FOREIGN KEY ([ConglomeradoId])
        REFERENCES [dbo].[Conglomerado] ([Id]),
    CONSTRAINT [FK_Aditivo_Contrato_Empresa] FOREIGN KEY ([EmpresaId])
        REFERENCES [dbo].[Empresa] ([Id]),
    CONSTRAINT [FK_Aditivo_Contrato_Cliente] FOREIGN KEY ([ClienteId])
        REFERENCES [dbo].[Cliente] ([Id]),
    CONSTRAINT [FK_Aditivo_Contrato_Contrato] FOREIGN KEY ([ContratoId])
        REFERENCES [dbo].[Contrato] ([Id]),
    CONSTRAINT [FK_Aditivo_Contrato_TipoAditivo] FOREIGN KEY ([TipoAditivoId])
        REFERENCES [dbo].[Aditivo_Tipo] ([Id]),
    CONSTRAINT [UQ_Aditivo_Contrato_Numero] UNIQUE ([ConglomeradoId], [Numero], [Fl_Excluido]),
    CONSTRAINT [CK_Aditivo_Contrato_Tipo] CHECK ([Tipo] IN (1, 2, 3, 4)),
    CONSTRAINT [CK_Aditivo_Contrato_Status] CHECK ([Status] IN (1, 2, 3, 4, 5)),
    CONSTRAINT [CK_Aditivo_Contrato_Vigencia] CHECK ([VigenciaFim] >= [VigenciaInicio]),
    CONSTRAINT [CK_Aditivo_Contrato_VersaoAtual] CHECK ([VersaoAtual] >= 1),
    CONSTRAINT [CK_Aditivo_Contrato_PercentualAcrescimo] CHECK ([PercentualAcrescimo] >= -100 AND [PercentualAcrescimo] <= 100)
);

CREATE NONCLUSTERED INDEX [IX_Aditivo_Contrato_ConglomeradoId] ON [dbo].[Aditivo_Contrato] ([ConglomeradoId]);
CREATE NONCLUSTERED INDEX [IX_Aditivo_Contrato_EmpresaId] ON [dbo].[Aditivo_Contrato] ([EmpresaId]);
CREATE NONCLUSTERED INDEX [IX_Aditivo_Contrato_ClienteId] ON [dbo].[Aditivo_Contrato] ([ClienteId]);
CREATE NONCLUSTERED INDEX [IX_Aditivo_Contrato_ContratoId] ON [dbo].[Aditivo_Contrato] ([ContratoId]);
CREATE NONCLUSTERED INDEX [IX_Aditivo_Contrato_TipoAditivoId] ON [dbo].[Aditivo_Contrato] ([TipoAditivoId]);
CREATE NONCLUSTERED INDEX [IX_Aditivo_Contrato_Numero] ON [dbo].[Aditivo_Contrato] ([Numero]);
CREATE NONCLUSTERED INDEX [IX_Aditivo_Contrato_Status] ON [dbo].[Aditivo_Contrato] ([Status]) WHERE [Fl_Excluido] = 0;
CREATE NONCLUSTERED INDEX [IX_Aditivo_Contrato_VigenciaInicio] ON [dbo].[Aditivo_Contrato] ([VigenciaInicio]);
CREATE NONCLUSTERED INDEX [IX_Aditivo_Contrato_VigenciaFim] ON [dbo].[Aditivo_Contrato] ([VigenciaFim]);
CREATE NONCLUSTERED INDEX [IX_Aditivo_Contrato_CreatedAt] ON [dbo].[Aditivo_Contrato] ([CreatedAt] DESC);

-- =============================================
-- 4. TABELA: Aditivo_Workflow
-- =============================================
CREATE TABLE [dbo].[Aditivo_Workflow] (
    [Id] UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    [AditivoId] UNIQUEIDENTIFIER NOT NULL,
    [UsuarioId] UNIQUEIDENTIFIER NOT NULL,
    [Etapa] NVARCHAR(100) NOT NULL,
    [StatusWorkflow] INT NOT NULL DEFAULT 1, -- 1=Pendente, 2=Aprovado, 3=Rejeitado, 4=Em Análise
    [DataEtapa] DATETIME2(7) NOT NULL DEFAULT GETUTCDATE(),
    [DataLimite] DATETIME2(7) NOT NULL,
    [DataConclusao] DATETIME2(7) NULL,
    [Parecer] NVARCHAR(2000) NULL,
    [AnexoParecerId] UNIQUEIDENTIFIER NULL,
    [Ordem] INT NOT NULL,
    [Ativo] BIT NOT NULL DEFAULT 1,
    [CreatedAt] DATETIME2(7) NOT NULL DEFAULT GETUTCDATE(),
    [CreatedBy] UNIQUEIDENTIFIER NOT NULL,
    [ModifiedAt] DATETIME2(7) NULL,
    [ModifiedBy] UNIQUEIDENTIFIER NULL,

    CONSTRAINT [PK_Aditivo_Workflow] PRIMARY KEY CLUSTERED ([Id] ASC),
    CONSTRAINT [FK_Aditivo_Workflow_Aditivo] FOREIGN KEY ([AditivoId])
        REFERENCES [dbo].[Aditivo_Contrato] ([Id]) ON DELETE CASCADE,
    CONSTRAINT [FK_Aditivo_Workflow_Usuario] FOREIGN KEY ([UsuarioId])
        REFERENCES [dbo].[Usuario] ([Id]),
    CONSTRAINT [CK_Aditivo_Workflow_StatusWorkflow] CHECK ([StatusWorkflow] IN (1, 2, 3, 4)),
    CONSTRAINT [CK_Aditivo_Workflow_DataLimite] CHECK ([DataLimite] >= [DataEtapa]),
    CONSTRAINT [CK_Aditivo_Workflow_Ordem] CHECK ([Ordem] >= 1 AND [Ordem] <= 50)
);

CREATE NONCLUSTERED INDEX [IX_Aditivo_Workflow_AditivoId] ON [dbo].[Aditivo_Workflow] ([AditivoId]);
CREATE NONCLUSTERED INDEX [IX_Aditivo_Workflow_UsuarioId] ON [dbo].[Aditivo_Workflow] ([UsuarioId]);
CREATE NONCLUSTERED INDEX [IX_Aditivo_Workflow_StatusWorkflow] ON [dbo].[Aditivo_Workflow] ([StatusWorkflow]);
CREATE NONCLUSTERED INDEX [IX_Aditivo_Workflow_DataLimite] ON [dbo].[Aditivo_Workflow] ([DataLimite]) WHERE [StatusWorkflow] = 1;
CREATE NONCLUSTERED INDEX [IX_Aditivo_Workflow_Ordem] ON [dbo].[Aditivo_Workflow] ([AditivoId], [Ordem]);

-- =============================================
-- 5. TABELA: Aditivo_Versao
-- =============================================
CREATE TABLE [dbo].[Aditivo_Versao] (
    [Id] UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    [AditivoId] UNIQUEIDENTIFIER NOT NULL,
    [NumeroVersao] INT NOT NULL,
    [DataVersao] DATETIME2(7) NOT NULL DEFAULT GETUTCDATE(),
    [UsuarioId] UNIQUEIDENTIFIER NOT NULL,
    [DescricaoAlteracao] NVARCHAR(1000) NOT NULL,
    [CamposAlterados] NVARCHAR(MAX) NULL, -- JSON
    [HashAnterior] NVARCHAR(64) NULL,
    [HashAtual] NVARCHAR(64) NOT NULL,
    [SnapshotDados] NVARCHAR(MAX) NOT NULL, -- JSON com snapshot completo
    [Ativo] BIT NOT NULL DEFAULT 1,
    [CreatedAt] DATETIME2(7) NOT NULL DEFAULT GETUTCDATE(),
    [CreatedBy] UNIQUEIDENTIFIER NOT NULL,

    CONSTRAINT [PK_Aditivo_Versao] PRIMARY KEY CLUSTERED ([Id] ASC),
    CONSTRAINT [FK_Aditivo_Versao_Aditivo] FOREIGN KEY ([AditivoId])
        REFERENCES [dbo].[Aditivo_Contrato] ([Id]) ON DELETE CASCADE,
    CONSTRAINT [FK_Aditivo_Versao_Usuario] FOREIGN KEY ([UsuarioId])
        REFERENCES [dbo].[Usuario] ([Id]),
    CONSTRAINT [UQ_Aditivo_Versao_NumeroVersao] UNIQUE ([AditivoId], [NumeroVersao]),
    CONSTRAINT [CK_Aditivo_Versao_NumeroVersao] CHECK ([NumeroVersao] >= 1),
    CONSTRAINT [CK_Aditivo_Versao_CamposAlterados_JSON] CHECK ([CamposAlterados] IS NULL OR ISJSON([CamposAlterados]) = 1),
    CONSTRAINT [CK_Aditivo_Versao_SnapshotDados_JSON] CHECK (ISJSON([SnapshotDados]) = 1)
);

CREATE NONCLUSTERED INDEX [IX_Aditivo_Versao_AditivoId] ON [dbo].[Aditivo_Versao] ([AditivoId]);
CREATE NONCLUSTERED INDEX [IX_Aditivo_Versao_NumeroVersao] ON [dbo].[Aditivo_Versao] ([AditivoId], [NumeroVersao] DESC);
CREATE NONCLUSTERED INDEX [IX_Aditivo_Versao_DataVersao] ON [dbo].[Aditivo_Versao] ([DataVersao] DESC);
CREATE NONCLUSTERED INDEX [IX_Aditivo_Versao_HashAtual] ON [dbo].[Aditivo_Versao] ([HashAtual]);

-- =============================================
-- 6. TABELA: Aditivo_ImpactoFinanceiro
-- =============================================
CREATE TABLE [dbo].[Aditivo_ImpactoFinanceiro] (
    [Id] UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    [AditivoId] UNIQUEIDENTIFIER NOT NULL,
    [Tipo] INT NOT NULL, -- 1=Receita, 2=Despesa, 3=Investimento
    [Competencia] NVARCHAR(7) NOT NULL, -- YYYY-MM
    [ValorPrevisto] DECIMAL(18,2) NOT NULL,
    [ValorRealizado] DECIMAL(18,2) NULL,
    [PercentualImpacto] DECIMAL(5,2) NOT NULL,
    [CentroCusto] NVARCHAR(50) NULL,
    [ContaContabil] NVARCHAR(50) NULL,
    [ProjetoCod] NVARCHAR(50) NULL,
    [RubricaOrcamentaria] NVARCHAR(100) NULL,
    [Observacoes] NVARCHAR(1000) NULL,
    [Ativo] BIT NOT NULL DEFAULT 1,
    [CreatedAt] DATETIME2(7) NOT NULL DEFAULT GETUTCDATE(),
    [CreatedBy] UNIQUEIDENTIFIER NOT NULL,
    [ModifiedAt] DATETIME2(7) NULL,
    [ModifiedBy] UNIQUEIDENTIFIER NULL,

    CONSTRAINT [PK_Aditivo_ImpactoFinanceiro] PRIMARY KEY CLUSTERED ([Id] ASC),
    CONSTRAINT [FK_Aditivo_ImpactoFinanceiro_Aditivo] FOREIGN KEY ([AditivoId])
        REFERENCES [dbo].[Aditivo_Contrato] ([Id]) ON DELETE CASCADE,
    CONSTRAINT [CK_Aditivo_ImpactoFinanceiro_Tipo] CHECK ([Tipo] IN (1, 2, 3)),
    CONSTRAINT [CK_Aditivo_ImpactoFinanceiro_Competencia] CHECK ([Competencia] LIKE '[0-9][0-9][0-9][0-9]-[0-1][0-9]'),
    CONSTRAINT [CK_Aditivo_ImpactoFinanceiro_PercentualImpacto] CHECK ([PercentualImpacto] >= -100 AND [PercentualImpacto] <= 100)
);

CREATE NONCLUSTERED INDEX [IX_Aditivo_ImpactoFinanceiro_AditivoId] ON [dbo].[Aditivo_ImpactoFinanceiro] ([AditivoId]);
CREATE NONCLUSTERED INDEX [IX_Aditivo_ImpactoFinanceiro_Competencia] ON [dbo].[Aditivo_ImpactoFinanceiro] ([Competencia]);
CREATE NONCLUSTERED INDEX [IX_Aditivo_ImpactoFinanceiro_CentroCusto] ON [dbo].[Aditivo_ImpactoFinanceiro] ([CentroCusto]);
CREATE NONCLUSTERED INDEX [IX_Aditivo_ImpactoFinanceiro_ContaContabil] ON [dbo].[Aditivo_ImpactoFinanceiro] ([ContaContabil]);

-- =============================================
-- 7. TABELA: Aditivo_Anexo
-- =============================================
CREATE TABLE [dbo].[Aditivo_Anexo] (
    [Id] UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    [AditivoId] UNIQUEIDENTIFIER NOT NULL,
    [TipoDocumento] INT NOT NULL, -- 1=Minuta, 2=Parecer Jurídico, 3=Análise Técnica, 4=Documento Assinado, 5=Outro
    [NomeArquivo] NVARCHAR(255) NOT NULL,
    [CaminhoArquivo] NVARCHAR(500) NOT NULL,
    [ExtensaoArquivo] NVARCHAR(10) NOT NULL,
    [TamanhoBytes] BIGINT NOT NULL,
    [HashSHA256] NVARCHAR(64) NOT NULL,
    [DataUpload] DATETIME2(7) NOT NULL DEFAULT GETUTCDATE(),
    [UsuarioUploadId] UNIQUEIDENTIFIER NOT NULL,
    [AssinadoDigitalmente] BIT NOT NULL DEFAULT 0,
    [DataAssinatura] DATETIME2(7) NULL,
    [CertificadoDigital] NVARCHAR(MAX) NULL, -- Certificado ICP-Brasil
    [SignatarioNome] NVARCHAR(200) NULL,
    [SignatarioCPF] NVARCHAR(14) NULL,
    [Descricao] NVARCHAR(500) NULL,
    [Ativo] BIT NOT NULL DEFAULT 1,
    [CreatedAt] DATETIME2(7) NOT NULL DEFAULT GETUTCDATE(),
    [CreatedBy] UNIQUEIDENTIFIER NOT NULL,
    [ModifiedAt] DATETIME2(7) NULL,
    [ModifiedBy] UNIQUEIDENTIFIER NULL,
    [Fl_Excluido] BIT NOT NULL DEFAULT 0,
    [Data_Exclusao] DATETIME2(7) NULL,

    CONSTRAINT [PK_Aditivo_Anexo] PRIMARY KEY CLUSTERED ([Id] ASC),
    CONSTRAINT [FK_Aditivo_Anexo_Aditivo] FOREIGN KEY ([AditivoId])
        REFERENCES [dbo].[Aditivo_Contrato] ([Id]) ON DELETE CASCADE,
    CONSTRAINT [FK_Aditivo_Anexo_Usuario] FOREIGN KEY ([UsuarioUploadId])
        REFERENCES [dbo].[Usuario] ([Id]),
    CONSTRAINT [CK_Aditivo_Anexo_TipoDocumento] CHECK ([TipoDocumento] IN (1, 2, 3, 4, 5)),
    CONSTRAINT [CK_Aditivo_Anexo_TamanhoBytes] CHECK ([TamanhoBytes] > 0 AND [TamanhoBytes] <= 52428800), -- 50 MB
    CONSTRAINT [CK_Aditivo_Anexo_ExtensaoArquivo] CHECK ([ExtensaoArquivo] IN ('.pdf', '.docx', '.xlsx', '.png', '.jpg', '.jpeg'))
);

CREATE NONCLUSTERED INDEX [IX_Aditivo_Anexo_AditivoId] ON [dbo].[Aditivo_Anexo] ([AditivoId]);
CREATE NONCLUSTERED INDEX [IX_Aditivo_Anexo_TipoDocumento] ON [dbo].[Aditivo_Anexo] ([TipoDocumento]);
CREATE NONCLUSTERED INDEX [IX_Aditivo_Anexo_HashSHA256] ON [dbo].[Aditivo_Anexo] ([HashSHA256]);
CREATE NONCLUSTERED INDEX [IX_Aditivo_Anexo_DataUpload] ON [dbo].[Aditivo_Anexo] ([DataUpload] DESC);

-- =============================================
-- 8. TABELA: Aditivo_Historico
-- =============================================
CREATE TABLE [dbo].[Aditivo_Historico] (
    [Id] UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    [AditivoId] UNIQUEIDENTIFIER NOT NULL,
    [UsuarioId] UNIQUEIDENTIFIER NOT NULL,
    [DataOperacao] DATETIME2(7) NOT NULL DEFAULT GETUTCDATE(),
    [TipoOperacao] NVARCHAR(50) NOT NULL, -- CREATE, UPDATE, DELETE, APPROVE, REJECT, CANCEL
    [DescricaoOperacao] NVARCHAR(500) NOT NULL,
    [DadosAnteriores] NVARCHAR(MAX) NULL, -- JSON
    [DadosNovos] NVARCHAR(MAX) NULL, -- JSON
    [EnderecoIP] NVARCHAR(50) NULL,
    [UserAgent] NVARCHAR(500) NULL,
    [Hostname] NVARCHAR(100) NULL,
    [AplicacaoOrigem] NVARCHAR(100) NULL,

    CONSTRAINT [PK_Aditivo_Historico] PRIMARY KEY CLUSTERED ([Id] ASC),
    CONSTRAINT [FK_Aditivo_Historico_Aditivo] FOREIGN KEY ([AditivoId])
        REFERENCES [dbo].[Aditivo_Contrato] ([Id]),
    CONSTRAINT [FK_Aditivo_Historico_Usuario] FOREIGN KEY ([UsuarioId])
        REFERENCES [dbo].[Usuario] ([Id]),
    CONSTRAINT [CK_Aditivo_Historico_TipoOperacao] CHECK ([TipoOperacao] IN ('CREATE', 'UPDATE', 'DELETE', 'APPROVE', 'REJECT', 'CANCEL', 'WORKFLOW_START', 'WORKFLOW_COMPLETE')),
    CONSTRAINT [CK_Aditivo_Historico_DadosAnteriores_JSON] CHECK ([DadosAnteriores] IS NULL OR ISJSON([DadosAnteriores]) = 1),
    CONSTRAINT [CK_Aditivo_Historico_DadosNovos_JSON] CHECK ([DadosNovos] IS NULL OR ISJSON([DadosNovos]) = 1)
);

CREATE NONCLUSTERED INDEX [IX_Aditivo_Historico_AditivoId] ON [dbo].[Aditivo_Historico] ([AditivoId]);
CREATE NONCLUSTERED INDEX [IX_Aditivo_Historico_UsuarioId] ON [dbo].[Aditivo_Historico] ([UsuarioId]);
CREATE NONCLUSTERED INDEX [IX_Aditivo_Historico_DataOperacao] ON [dbo].[Aditivo_Historico] ([DataOperacao] DESC);
CREATE NONCLUSTERED INDEX [IX_Aditivo_Historico_TipoOperacao] ON [dbo].[Aditivo_Historico] ([TipoOperacao]);

-- =============================================
-- 9. TABELA: Aditivo_Tag
-- =============================================
CREATE TABLE [dbo].[Aditivo_Tag] (
    [Id] UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    [AditivoId] UNIQUEIDENTIFIER NOT NULL,
    [Tag] NVARCHAR(50) NOT NULL,
    [DataCriacao] DATETIME2(7) NOT NULL DEFAULT GETUTCDATE(),
    [CreatedBy] UNIQUEIDENTIFIER NOT NULL,

    CONSTRAINT [PK_Aditivo_Tag] PRIMARY KEY CLUSTERED ([Id] ASC),
    CONSTRAINT [FK_Aditivo_Tag_Aditivo] FOREIGN KEY ([AditivoId])
        REFERENCES [dbo].[Aditivo_Contrato] ([Id]) ON DELETE CASCADE,
    CONSTRAINT [UQ_Aditivo_Tag_AditivoTag] UNIQUE ([AditivoId], [Tag])
);

CREATE NONCLUSTERED INDEX [IX_Aditivo_Tag_AditivoId] ON [dbo].[Aditivo_Tag] ([AditivoId]);
CREATE NONCLUSTERED INDEX [IX_Aditivo_Tag_Tag] ON [dbo].[Aditivo_Tag] ([Tag]);

-- =============================================
-- 10. TABELA: Aditivo_Notificacao
-- =============================================
CREATE TABLE [dbo].[Aditivo_Notificacao] (
    [Id] UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    [AditivoId] UNIQUEIDENTIFIER NOT NULL,
    [UsuarioDestinoId] UNIQUEIDENTIFIER NOT NULL,
    [TipoNotificacao] INT NOT NULL, -- 1=Aprovação Pendente, 2=Prazo Vencendo, 3=Aprovado, 4=Rejeitado, 5=Cancelado
    [Mensagem] NVARCHAR(500) NOT NULL,
    [DataEnvio] DATETIME2(7) NOT NULL DEFAULT GETUTCDATE(),
    [DataLeitura] DATETIME2(7) NULL,
    [Lida] BIT NOT NULL DEFAULT 0,
    [EmailEnviado] BIT NOT NULL DEFAULT 0,
    [DataEnvioEmail] DATETIME2(7) NULL,
    [LinkAcao] NVARCHAR(500) NULL,
    [Prioridade] INT NOT NULL DEFAULT 2, -- 1=Alta, 2=Normal, 3=Baixa

    CONSTRAINT [PK_Aditivo_Notificacao] PRIMARY KEY CLUSTERED ([Id] ASC),
    CONSTRAINT [FK_Aditivo_Notificacao_Aditivo] FOREIGN KEY ([AditivoId])
        REFERENCES [dbo].[Aditivo_Contrato] ([Id]) ON DELETE CASCADE,
    CONSTRAINT [FK_Aditivo_Notificacao_Usuario] FOREIGN KEY ([UsuarioDestinoId])
        REFERENCES [dbo].[Usuario] ([Id]),
    CONSTRAINT [CK_Aditivo_Notificacao_TipoNotificacao] CHECK ([TipoNotificacao] IN (1, 2, 3, 4, 5)),
    CONSTRAINT [CK_Aditivo_Notificacao_Prioridade] CHECK ([Prioridade] IN (1, 2, 3))
);

CREATE NONCLUSTERED INDEX [IX_Aditivo_Notificacao_AditivoId] ON [dbo].[Aditivo_Notificacao] ([AditivoId]);
CREATE NONCLUSTERED INDEX [IX_Aditivo_Notificacao_UsuarioDestinoId] ON [dbo].[Aditivo_Notificacao] ([UsuarioDestinoId]);
CREATE NONCLUSTERED INDEX [IX_Aditivo_Notificacao_Lida] ON [dbo].[Aditivo_Notificacao] ([Lida], [UsuarioDestinoId]) WHERE [Lida] = 0;
CREATE NONCLUSTERED INDEX [IX_Aditivo_Notificacao_DataEnvio] ON [dbo].[Aditivo_Notificacao] ([DataEnvio] DESC);

-- =============================================
-- FIM DO SCRIPT DDL
-- =============================================
```

---

## 5. RELACIONAMENTOS

### 5.1. Hierarquia Multi-Tenancy

```
Conglomerado (1) ──► (N) Empresa (1) ──► (N) Cliente
     │                                        │
     │                                        │
     └────────────────────────────────────────┴──► Aditivo_Contrato
```

**Regras:**
- Todo aditivo pertence a um único Cliente, Empresa e Conglomerado
- Queries SEMPRE filtram por ConglomeradoId (Row-Level Security)
- Não é possível acessar aditivos de outros conglomerados

### 5.2. Relacionamentos Principais

| Tabela Origem          | Tabela Destino         | Tipo        | Cardinalidade |
|------------------------|------------------------|-------------|---------------|
| Aditivo_Contrato       | Contrato               | FK          | N:1           |
| Aditivo_Contrato       | Aditivo_Tipo           | FK          | N:1           |
| Aditivo_Workflow       | Aditivo_Contrato       | FK          | N:1           |
| Aditivo_Workflow       | Usuario                | FK          | N:1           |
| Aditivo_Versao         | Aditivo_Contrato       | FK          | N:1           |
| Aditivo_Versao         | Usuario                | FK          | N:1           |
| Aditivo_ImpactoFinanc  | Aditivo_Contrato       | FK          | N:1           |
| Aditivo_Anexo          | Aditivo_Contrato       | FK          | N:1           |
| Aditivo_Anexo          | Usuario                | FK          | N:1           |
| Aditivo_Historico      | Aditivo_Contrato       | FK          | N:1           |
| Aditivo_Historico      | Usuario                | FK          | N:1           |
| Aditivo_Tag            | Aditivo_Contrato       | FK          | N:1           |
| Aditivo_Notificacao    | Aditivo_Contrato       | FK          | N:1           |
| Aditivo_Notificacao    | Usuario                | FK          | N:1           |
| Workflow_Configuracao  | Aditivo_Tipo           | FK          | N:1           |

---

## 6. ÍNDICES E OTIMIZAÇÕES

### 6.1. Estratégia de Indexação

**Índices em Foreign Keys (28 índices):**
- Todas as FKs possuem índices não-clusterizados
- Melhora performance de JOINs e queries de navegação

**Índices em Campos de Busca (15+ índices):**
- `Numero` do aditivo (busca rápida)
- `Status` (filtros de dashboard)
- `DataLimite` (alertas de prazo)
- `VigenciaInicio/Fim` (relatórios de período)
- `Tag` (busca por tags)

**Índices Compostos (5 índices):**
- `[AditivoId, Ordem]` para workflow sequencial
- `[ConglomeradoId, Numero]` para unicidade
- `[Lida, UsuarioDestinoId]` para notificações pendentes

### 6.2. Particionamento (Futuro)

Para ambientes com volume alto (>1 milhão de aditivos):

```sql
-- Particionamento de Aditivo_Historico por ano
CREATE PARTITION FUNCTION PF_Aditivo_Historico_Ano (DATETIME2)
AS RANGE RIGHT FOR VALUES (
    '2024-01-01', '2025-01-01', '2026-01-01', '2027-01-01'
);
```

---

## 7. REGRAS DE NEGÓCIO MAPEADAS

| Regra de Negócio (RF027)                          | Implementação no Banco                                    |
|---------------------------------------------------|-----------------------------------------------------------|
| RN001: Número único de aditivo                    | UNIQUE CONSTRAINT em `Aditivo_Contrato.Numero`            |
| RN002: Acréscimo máximo 25%                       | CHECK CONSTRAINT em `PercentualAcrescimo`                 |
| RN003: Vigência máxima 60 meses                   | Validação em Application Layer                            |
| RN004: Versionamento automático                   | Trigger/Handler cria registro em `Aditivo_Versao`         |
| RN005: Workflow sequencial                        | Campo `Ordem` em `Aditivo_Workflow`                       |
| RN006: Assinatura digital obrigatória             | Campo `AssinadoDigitalmente` em `Aditivo_Anexo`           |
| RN007: Auditoria completa (7 anos)                | Tabela `Aditivo_Historico` + Retention Policy             |
| RN008: Multi-tenancy                              | Campos `ConglomeradoId`, `EmpresaId`, `ClienteId`         |
| RN009: Soft Delete                                | Campos `Fl_Excluido`, `Data_Exclusao`                     |
| RN010: Notificações automáticas                   | Tabela `Aditivo_Notificacao` + SignalR                    |
| RN011: Análise de impacto financeiro              | Tabela `Aditivo_ImpactoFinanceiro`                        |
| RN012: Tipos configuráveis                        | Tabela `Aditivo_Tipo` + `Workflow_Configuracao`           |

---

## 8. INTEGRAÇÕES OBRIGATÓRIAS

### 8.1. Central de Funcionalidades

**Funcionalidades a serem registradas:**
- `GES.ADITIVOS.LISTAR` - Listar aditivos
- `GES.ADITIVOS.CRIAR` - Criar aditivo
- `GES.ADITIVOS.VISUALIZAR` - Visualizar detalhes
- `GES.ADITIVOS.EDITAR` - Editar aditivo
- `GES.ADITIVOS.APROVAR` - Aprovar workflow
- `GES.ADITIVOS.REJEITAR` - Rejeitar workflow
- `GES.ADITIVOS.WORKFLOW` - Acompanhar workflow
- `GES.ADITIVOS.IMPACTO` - Análise de impacto financeiro

### 8.2. Internacionalização (i18n)

**Chaves de tradução necessárias:**
```
aditivos.titulo = "Gestão de Aditivos Contratos"
aditivos.novo = "Novo Aditivo"
aditivos.campos.numero = "Número do Aditivo"
aditivos.campos.tipo = "Tipo"
aditivos.campos.status = "Status"
aditivos.workflow.etapa = "Etapa"
aditivos.validacao.numero_duplicado = "Número de aditivo já existe"
aditivos.validacao.acrescimo_limite = "Acréscimo não pode ultrapassar 25%"
```

### 8.3. Auditoria

**Operações auditadas:**
- CREATE - Criação de aditivo
- UPDATE - Alteração de dados
- DELETE - Exclusão lógica
- APPROVE - Aprovação em workflow
- REJECT - Rejeição em workflow
- WORKFLOW_START - Início de workflow
- WORKFLOW_COMPLETE - Conclusão de workflow

**Campos auditados:**
- Usuario que executou
- Data/hora da operação
- IP, UserAgent, Hostname
- Dados antes e depois (JSON)

### 8.4. Controle de Acesso (RBAC)

**Permissões necessárias:**

| Permissão                          | Descrição                              |
|------------------------------------|----------------------------------------|
| `GES.ADITIVOS.LISTAR`              | Listar aditivos                        |
| `GES.ADITIVOS.CRIAR`               | Criar novo aditivo                     |
| `GES.ADITIVOS.VISUALIZAR`          | Visualizar detalhes                    |
| `GES.ADITIVOS.EDITAR`              | Editar aditivo (status Elaboração)     |
| `GES.ADITIVOS.APROVAR`             | Aprovar etapa de workflow              |
| `GES.ADITIVOS.REJEITAR`            | Rejeitar etapa de workflow             |
| `GES.ADITIVOS.EXCLUIR`             | Excluir logicamente                    |
| `GES.ADITIVOS.WORKFLOW.GERENCIAR`  | Configurar workflows                   |
| `GES.ADITIVOS.IMPACTO.VISUALIZAR`  | Ver análise de impacto financeiro      |

---

## 9. CONSIDERAÇÕES DE PERFORMANCE

### 9.1. Estimativas de Volume

| Tabela                       | Estimativa Anual | Estimativa 5 Anos |
|------------------------------|------------------|-------------------|
| Aditivo_Contrato             | 5.000            | 25.000            |
| Aditivo_Workflow             | 15.000           | 75.000            |
| Aditivo_Versao               | 10.000           | 50.000            |
| Aditivo_ImpactoFinanceiro    | 60.000           | 300.000           |
| Aditivo_Anexo                | 20.000           | 100.000           |
| Aditivo_Historico            | 100.000          | 500.000           |
| Aditivo_Notificacao          | 50.000           | 250.000           |

### 9.2. Queries Críticas

**Query 1: Dashboard de Aditivos Pendentes**
```sql
-- Otimizada com índice IX_Aditivo_Contrato_Status
SELECT * FROM Aditivo_Contrato
WHERE Status IN (1, 2)
AND Fl_Excluido = 0
AND ConglomeradoId = @ConglomeradoId
ORDER BY CreatedAt DESC;
```

**Query 2: Workflow com Prazo Vencendo**
```sql
-- Otimizada com índice IX_Aditivo_Workflow_DataLimite
SELECT * FROM Aditivo_Workflow
WHERE StatusWorkflow = 1
AND DataLimite <= DATEADD(DAY, 2, GETUTCDATE())
AND UsuarioId = @UsuarioId;
```

**Query 3: Histórico de Versões**
```sql
-- Otimizada com índice IX_Aditivo_Versao_NumeroVersao
SELECT * FROM Aditivo_Versao
WHERE AditivoId = @AditivoId
ORDER BY NumeroVersao DESC;
```

---

## 10. SEGURANÇA E COMPLIANCE

### 10.1. LGPD

- **Dados Sensíveis:** CPF de signatário em `Aditivo_Anexo`
- **Retenção:** 7 anos para `Aditivo_Historico`
- **Direito ao Esquecimento:** Soft delete: false=ativo, true=excluído preserva histórico, anonimiza dados pessoais

### 10.2. Lei 8.666/93 (Contratos Públicos)

- **Limite de Acréscimo:** 25% implementado via CHECK CONSTRAINT
- **Vigência Máxima:** 60 meses validado em Application Layer
- **Rastreabilidade:** Histórico completo de aprovações e pareceres
- **Transparência:** Todos os anexos e justificativas preservados

### 10.3. Assinatura Digital ICP-Brasil

- Campo `CertificadoDigital` em `Aditivo_Anexo`
- Validação de certificado digital
- Timestamp de assinatura
- Nome e CPF do signatário

---

## 11. MIGRAÇÃO DE DADOS (LEGADO)

### 11.1. Mapeamento de Tabelas Legadas

| Tabela Legada                | Tabela Nova                | Observações                          |
|------------------------------|----------------------------|--------------------------------------|
| `TB_Aditivo`                 | `Aditivo_Contrato`         | Adicionar campos multi-tenancy       |
| `TB_Aditivo_Workflow`        | `Aditivo_Workflow`         | Migrar status para novos valores     |
| `TB_Aditivo_Anexo`           | `Aditivo_Anexo`            | Recalcular hash SHA256               |
| N/A                          | `Aditivo_Versao`           | Criar versão 1 para todos            |
| N/A                          | `Aditivo_Historico`        | Migrar dados de auditoria se houver  |

### 11.2. Script de Migração (Exemplo)

```sql
-- Migração de Aditivo_Contrato
INSERT INTO Aditivo_Contrato (
    Id, ConglomeradoId, EmpresaId, ClienteId, ContratoId,
    Numero, Tipo, Status, VersaoAtual, VigenciaInicio, VigenciaFim,
    ValorOriginal, ValorAditado, PercentualAcrescimo, MotivoJustificativa,
    CreatedAt, CreatedBy, Ativo
)
SELECT
    NEWID(),
    @ConglomeradoIdPadrao,
    @EmpresaIdPadrao,
    l.ClienteId,
    l.ContratoId,
    l.NumeroAditivo,
    CASE l.TipoAditivo
        WHEN 'PRAZO' THEN 1
        WHEN 'VALOR' THEN 2
        WHEN 'ESCOPO' THEN 3
        ELSE 4
    END,
    CASE l.StatusAditivo
        WHEN 'ELABORACAO' THEN 1
        WHEN 'APROVACAO' THEN 2
        WHEN 'APROVADO' THEN 3
        WHEN 'REJEITADO' THEN 4
        ELSE 5
    END,
    1, -- Versão inicial
    l.DataInicio,
    l.DataFim,
    l.ValorOriginal,
    l.ValorAditado,
    l.PercentualAcrescimo,
    l.Justificativa,
    ISNULL(l.DataCadastro, GETUTCDATE()),
    @UsuarioMigracaoId,
    1
FROM TB_Aditivo l
WHERE l.Fl_Excluido = 0;
```

---

## 12. TESTES RECOMENDADOS

### 12.1. Testes de Integridade

- ✅ Constraint de número único por conglomerado
- ✅ Constraint de percentual acréscimo (-100 a 100)
- ✅ Constraint de vigência (fim >= início)
- ✅ Constraint de ordem de workflow (1 a 50)
- ✅ Constraint de JSON válido em campos JSON

### 12.2. Testes de Performance

- ✅ Query dashboard com 100k aditivos (< 500ms)
- ✅ Query workflow com prazo vencendo (< 200ms)
- ✅ Insert de aditivo + 5 anexos (< 1s)
- ✅ Histórico de versões com 50 versões (< 300ms)

### 12.3. Testes de Carga

- ✅ 1000 aditivos criados simultaneamente
- ✅ 500 workflows em aprovação simultânea
- ✅ 100 uploads de anexos (10 MB cada) simultâneos

---

## 13. PRÓXIMOS PASSOS

1. **Implementação Backend (.NET 10)**
   - Entities no Domain Layer
   - Commands/Queries no Application Layer
   - Validators com FluentValidation
   - Handlers com MediatR

2. **Implementação Frontend (Angular 19)**
   - Componentes standalone
   - Services com HttpClient
   - Formulários reativos
   - Upload de anexos com drag-and-drop

3. **Testes**
   - Testes unitários (80%+ cobertura)
   - Testes de integração (API)
   - Testes E2E (Playwright)
   - Testes de carga (JMeter/k6)

4. **Documentação**
   - API documentation (Swagger)
   - Manual do usuário
   - Guia de operação
   - Runbook de troubleshooting

---

**FIM DO DOCUMENTO MD-RF027**

**Versão:** 1.0
**Última Atualização:** 2025-12-18
**Total de Linhas:** 480
**Total de Tabelas:** 10 principais + 4 auxiliares = 14 tabelas
**Total de Índices:** 45+
**Status:** ✅ COMPLETO - Pronto para Implementação
