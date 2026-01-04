# MD-RF028 - Modelo de Dados: Gestão de SLA Operações

**Versão:** 1.0
**Data:** 2025-12-18
**Responsável:** Agente Architect
**RF Relacionado:** [RF028 - Gestão de SLA Operações](./RF028.md)
**UC Relacionado:** [UC-RF028 - Casos de Uso](./UC-RF028.md)

---

## 1. VISÃO GERAL

Este modelo de dados suporta o gerenciamento completo de SLAs Operacionais (KPIs técnicos), incluindo:

- **KPIs Técnicos:** Response Time, Resolution Time, Uptime, MTTR, MTBF, Availability
- **Monitoramento em Tempo Real** com SignalR e dashboards dinâmicos
- **Gestão de Violações** com alertas automáticos e planos de ação
- **Análise de Tendências** com histórico de métricas
- **Integração com Ferramentas** de monitoramento (Zabbix, Nagios, Prometheus, Grafana)
- **Multi-tenancy** com isolamento por Conglomerado/Empresa/Cliente
- **Auditoria Completa** de todas as operações

**Complexidade:** ALTA
**Número de Tabelas:** 12
**Relacionamentos:** 24 Foreign Keys
**Índices Otimizados:** 40+

---

## 2. DIAGRAMA ER (Entidade-Relacionamento)

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                   MODELO DE DADOS - GESTÃO DE SLA OPERAÇÕES                          │
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
│  Contrato        │   │ SLA_Operacao     │   │ Usuario              │
│──────────────────│   │──────────────────│   │──────────────────────│
│ Id (PK)          │1 *│ Id (PK)          │   │ Id (PK)              │
│ ClienteId (FK)   │◄──│ ContratoId (FK)  │   │ ClienteId (FK)       │
│ Numero           │   │ ClienteId (FK)   │   │ Nome                 │
│ VigenciaInicio   │   │ Nome             │   │ Email                │
│ VigenciaFim      │   │ Descricao        │   └──────────────────────┘
└──────────────────┘   │ Periodicidade    │
                       │ MetodoCalculo    │
                       │ TipoAgregacao    │
                       │ VigenciaInicio   │
                       │ VigenciaFim      │
                       │ Status           │
                       │ Ativo            │
                       └────┬─┬─┬─────────┘
                            │ │ │1
                            │ │ │
                            │ │ │*
                    ┌───────┘ │ └───────────┐
                    │*        │*            │*
        ┌───────────▼─────────┴─┐   ┌───────▼──────────────────┐
        │ SLA_Operacao_Metrica  │   │ SLA_Operacao_Threshold   │
        │───────────────────────│   │──────────────────────────│
        │ Id (PK)               │   │ Id (PK)                  │
        │ SLAOperacaoId (FK)    │   │ SLAOperacaoId (FK)       │
        │ TipoMetrica           │   │ TipoThreshold            │
        │ UnidadeMedida         │   │ OperadorComparacao       │
        │ MetaMinima            │   │ ValorMinimo              │
        │ MetaMaxima            │   │ ValorMaximo              │
        │ ValorAlerta           │   │ Severidade               │
        │ ValorCritico          │   │ AcaoAutomatica           │
        │ PesoCalculo           │   │ NotificarUsuarios        │
        │ Ativo                 │   │ Ativo                    │
        └───────────────────────┘   └──────────────────────────┘
                    │1
                    │
                    │*
        ┌───────────▼───────────────┐
        │ SLA_Medicao_RealTime      │
        │───────────────────────────│
        │ Id (PK)                   │
        │ MetricaId (FK)            │
        │ DataHoraMedicao           │
        │ ValorMedido               │
        │ StatusSLA                 │
        │ FonteDados                │
        │ ServidorOrigem            │
        │ AplicacaoOrigem           │
        └───────────────────────────┘

        ┌───────────────────────────┐
        │ SLA_Violacao              │1 *
        │───────────────────────────│◄───┐
        │ Id (PK)                   │    │
        │ SLAOperacaoId (FK)        │    │
        │ MetricaId (FK)            │    │
        │ DataHoraDeteccao          │    │
        │ DataHoraResolucao         │    │
        │ Severidade                │    │
        │ StatusViolacao            │    │
        │ ValorMedido               │    │
        │ ValorEsperado             │    │
        │ PercentualDesvio          │    │
        │ ImpactoCliente            │    │
        │ CausaRaiz                 │    │
        │ PlanoAcao                 │    │
        │ ResponsavelId (FK)        │    │
        └───────┬───────────────────┘    │
                │1                       │
                │                        │
                │*                       │
        ┌───────▼───────────────────┐    │
        │ SLA_Violacao_Comentario   │    │
        │───────────────────────────│    │
        │ Id (PK)                   │    │
        │ ViolacaoId (FK)           │────┘
        │ UsuarioId (FK)            │
        │ DataComentario            │
        │ Comentario                │
        │ TipoComentario            │
        └───────────────────────────┘

        ┌───────────────────────────┐
        │ SLA_Alerta                │
        │───────────────────────────│
        │ Id (PK)                   │
        │ SLAOperacaoId (FK)        │
        │ MetricaId (FK)            │
        │ ViolacaoId (FK)           │
        │ TipoAlerta                │
        │ Severidade                │
        │ Mensagem                  │
        │ DataHoraAlerta            │
        │ DataHoraResolucao         │
        │ StatusAlerta              │
        │ UsuarioNotificadoId (FK)  │
        │ CanalNotificacao          │
        └───────────────────────────┘

        ┌───────────────────────────┐
        │ SLA_Historico_Agregado    │
        │───────────────────────────│
        │ Id (PK)                   │
        │ SLAOperacaoId (FK)        │
        │ MetricaId (FK)            │
        │ Competencia               │
        │ TipoAgregacao             │
        │ ValorMedio                │
        │ ValorMinimo               │
        │ ValorMaximo               │
        │ Desvio Padrao             │
        │ Percentil95               │
        │ Percentil99               │
        │ TotalMedicoes             │
        │ TotalViolacoes            │
        │ PercentualDisponibilidade │
        └───────────────────────────┘

        ┌───────────────────────────┐
        │ SLA_Integracao_Config     │
        │───────────────────────────│
        │ Id (PK)                   │
        │ ConglomeradoId (FK)       │
        │ SLAOperacaoId (FK)        │
        │ TipoIntegracao            │
        │ NomeIntegracao            │
        │ URLEndpoint               │
        │ AutenticacaoTipo          │
        │ CredenciaisEncript (JSON) │
        │ IntervaloColeta           │
        │ MapeamentoCampos (JSON)   │
        │ Ativo                     │
        └───────────────────────────┘

        ┌───────────────────────────┐
        │ SLA_Dashboard_Config      │
        │───────────────────────────│
        │ Id (PK)                   │
        │ ConglomeradoId (FK)       │
        │ UsuarioId (FK)            │
        │ NomeDashboard             │
        │ Descricao                 │
        │ LayoutConfig (JSON)       │
        │ Widgets (JSON)            │
        │ Filtros (JSON)            │
        │ RefreshInterval           │
        │ Publico                   │
        │ Ativo                     │
        └───────────────────────────┘

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

### 3.1. SLA_Operacao

**Propósito:** Entidade principal que define os SLAs operacionais (técnicos).

**Campos Principais:**
- `Id` (Guid, PK) - Identificador único
- `ContratoId` (Guid, FK) - Referência ao contrato (opcional)
- `ClienteId` (Guid, FK) - Cliente proprietário (multi-tenancy)
- `EmpresaId` (Guid, FK) - Empresa proprietária (multi-tenancy)
- `ConglomeradoId` (Guid, FK) - Conglomerado proprietário (multi-tenancy)
- `Nome` (NVARCHAR(200)) - Nome do SLA (ex: "Uptime Servidores Web")
- `Descricao` (NVARCHAR(1000)) - Descrição detalhada
- `Periodicidade` (INT) - Periodicidade de avaliação (1=Horário, 2=Diário, 3=Semanal, 4=Mensal)
- `MetodoCalculo` (INT) - Método de cálculo (1=Média, 2=Máximo, 3=Mínimo, 4=Percentil, 5=Soma)
- `TipoAgregacao` (INT) - Tipo de agregação (1=Tempo, 2=Quantidade, 3=Percentual)
- `VigenciaInicio` (DATETIME2) - Data de início da vigência
- `VigenciaFim` (DATETIME2) - Data de fim da vigência
- `Status` (INT) - Status (1=Ativo, 2=Suspenso, 3=Cancelado, 4=Concluído)

**Regras de Negócio:**
- SLA pode ter múltiplas métricas associadas
- Periodicidade define frequência de consolidação
- Método de cálculo aplica-se a todas as métricas
- Vigência pode ser indefinida (VigenciaFim = NULL)

### 3.2. SLA_Operacao_Metrica

**Propósito:** Métricas específicas de cada SLA operacional.

**Campos Principais:**
- `Id` (Guid, PK)
- `SLAOperacaoId` (Guid, FK)
- `TipoMetrica` (INT) - Tipo (1=Response Time, 2=Resolution Time, 3=Uptime, 4=MTTR, 5=MTBF, 6=Throughput, 7=Error Rate, 8=CPU, 9=Memory, 10=Disk)
- `UnidadeMedida` (NVARCHAR(20)) - Unidade (ms, s, %, GB, etc.)
- `MetaMinima` (DECIMAL(18,4)) - Meta mínima aceitável
- `MetaMaxima` (DECIMAL(18,4)) - Meta máxima desejada
- `ValorAlerta` (DECIMAL(18,4)) - Valor que dispara alerta
- `ValorCritico` (DECIMAL(18,4)) - Valor crítico
- `PesoCalculo` (DECIMAL(5,2)) - Peso na média ponderada (0.00 a 1.00)
- `FormulaCalculo` (NVARCHAR(500)) - Fórmula customizada (NCalc)

**Regras de Negócio:**
- MetaMinima <= ValorAlerta <= ValorCritico <= MetaMaxima
- Soma dos pesos deve ser 1.00 por SLA
- Fórmula permite cálculos customizados (NCalc expression)
- Response Time: menor é melhor (< 200ms)
- Uptime: maior é melhor (> 99.9%)

### 3.3. SLA_Operacao_Threshold

**Propósito:** Thresholds de alertas e ações automáticas.

**Campos Principais:**
- `Id` (Guid, PK)
- `SLAOperacaoId` (Guid, FK)
- `TipoThreshold` (INT) - Tipo (1=Valor Absoluto, 2=Percentual Desvio, 3=Taxa de Crescimento)
- `OperadorComparacao` (INT) - Operador (1=Maior, 2=Menor, 3=Igual, 4=Entre)
- `ValorMinimo` (DECIMAL(18,4))
- `ValorMaximo` (DECIMAL(18,4))
- `Severidade` (INT) - Severidade (1=Informação, 2=Alerta, 3=Crítico, 4=Emergência)
- `AcaoAutomatica` (NVARCHAR(MAX)) - JSON com ações automáticas (webhook, restart, escala automática)
- `NotificarUsuarios` (NVARCHAR(MAX)) - JSON com lista de usuários a notificar

**Regras de Negócio:**
- Múltiplos thresholds por SLA
- Ações automáticas executadas via Hangfire
- Notificações via SignalR + Email + SMS
- Escala automática integrada com Kubernetes/Docker

### 3.4. SLA_Medicao_RealTime

**Propósito:** Medições em tempo real das métricas.

**Campos Principais:**
- `Id` (Guid, PK)
- `MetricaId` (Guid, FK)
- `DataHoraMedicao` (DATETIME2) - Data/hora da medição (UTC)
- `ValorMedido` (DECIMAL(18,4)) - Valor coletado
- `StatusSLA` (INT) - Status (1=OK, 2=Alerta, 3=Crítico, 4=Falha)
- `FonteDados` (NVARCHAR(100)) - Fonte (Zabbix, Nagios, Prometheus, APM)
- `ServidorOrigem` (NVARCHAR(100)) - Servidor que gerou a métrica
- `AplicacaoOrigem` (NVARCHAR(100)) - Aplicação monitorada
- `MetadadosAdicionais` (NVARCHAR(MAX)) - JSON com dados extras

**Regras de Negócio:**
- Retenção: 90 dias no banco principal, 7 anos em cold storage
- Inserção via bulk insert (performance)
- Particionamento por mês
- Agregação automática em SLA_Historico_Agregado

### 3.5. SLA_Violacao

**Propósito:** Registro de violações de SLA com plano de ação.

**Campos Principais:**
- `Id` (Guid, PK)
- `SLAOperacaoId` (Guid, FK)
- `MetricaId` (Guid, FK)
- `DataHoraDeteccao` (DATETIME2)
- `DataHoraResolucao` (DATETIME2)
- `Severidade` (INT) - Severidade (1=Baixa, 2=Média, 3=Alta, 4=Crítica)
- `StatusViolacao` (INT) - Status (1=Aberta, 2=Em Análise, 3=Resolvida, 4=Falsa Positiva)
- `ValorMedido` (DECIMAL(18,4))
- `ValorEsperado` (DECIMAL(18,4))
- `PercentualDesvio` (DECIMAL(5,2))
- `ImpactoCliente` (NVARCHAR(500)) - Descrição do impacto
- `CausaRaiz` (NVARCHAR(2000)) - Análise da causa raiz (Root Cause Analysis)
- `PlanoAcao` (NVARCHAR(2000)) - Plano de ação corretiva
- `ResponsavelId` (Guid, FK) - Usuário responsável pela resolução

**Regras de Negócio:**
- Violação criada automaticamente quando threshold excedido
- SLA de 4 horas para análise de violação crítica
- Workflow de aprovação para resolução
- Dashboard de violações abertas

### 3.6. SLA_Violacao_Comentario

**Propósito:** Comentários e atualizações nas violações (timeline).

**Campos Principais:**
- `Id` (Guid, PK)
- `ViolacaoId` (Guid, FK)
- `UsuarioId` (Guid, FK)
- `DataComentario` (DATETIME2)
- `Comentario` (NVARCHAR(2000))
- `TipoComentario` (INT) - Tipo (1=Análise, 2=Ação Tomada, 3=Atualização Status, 4=Pergunta)
- `VisibilidadeExterna` (BIT) - Se é visível para cliente externo

**Regras de Negócio:**
- Timeline de eventos da violação
- Comentários internos vs externos
- Notificação em tempo real (SignalR)

### 3.7. SLA_Alerta

**Propósito:** Alertas gerados quando thresholds são atingidos.

**Campos Principais:**
- `Id` (Guid, PK)
- `SLAOperacaoId` (Guid, FK)
- `MetricaId` (Guid, FK)
- `ViolacaoId` (Guid, FK) - Pode ser NULL se alerta preventivo
- `TipoAlerta` (INT) - Tipo (1=Preventivo, 2=Violação, 3=Recuperação)
- `Severidade` (INT)
- `Mensagem` (NVARCHAR(500))
- `DataHoraAlerta` (DATETIME2)
- `DataHoraResolucao` (DATETIME2)
- `StatusAlerta` (INT) - Status (1=Ativo, 2=Reconhecido, 3=Resolvido)
- `UsuarioNotificadoId` (Guid, FK)
- `CanalNotificacao` (INT) - Canal (1=SignalR, 2=Email, 3=SMS, 4=Webhook)
- `EmailEnviado` (BIT)
- `SMSEnviado` (BIT)

**Regras de Negócio:**
- Alertas preventivos antes da violação
- Alertas de recuperação quando volta ao normal
- Deduplicação de alertas (não enviar mesmo alerta em 5min)
- Dashboard de alertas ativos

### 3.8. SLA_Historico_Agregado

**Propósito:** Histórico consolidado de métricas (performance de queries).

**Campos Principais:**
- `Id` (Guid, PK)
- `SLAOperacaoId` (Guid, FK)
- `MetricaId` (Guid, FK)
- `Competencia` (NVARCHAR(20)) - Competência (YYYY-MM-DD para diário, YYYY-MM para mensal)
- `TipoAgregacao` (INT) - Tipo (1=Horário, 2=Diário, 3=Semanal, 4=Mensal)
- `ValorMedio` (DECIMAL(18,4))
- `ValorMinimo` (DECIMAL(18,4))
- `ValorMaximo` (DECIMAL(18,4))
- `DesvioPadrao` (DECIMAL(18,4))
- `Percentil95` (DECIMAL(18,4))
- `Percentil99` (DECIMAL(18,4))
- `TotalMedicoes` (INT)
- `TotalViolacoes` (INT)
- `PercentualDisponibilidade` (DECIMAL(5,2))

**Regras de Negócio:**
- Agregação automática via Hangfire (job noturno)
- Queries rápidas em relatórios (usar agregado, não raw data)
- Retenção permanente (7 anos)

### 3.9. SLA_Integracao_Config

**Propósito:** Configuração de integrações com ferramentas de monitoramento.

**Campos Principais:**
- `Id` (Guid, PK)
- `ConglomeradoId` (Guid, FK)
- `SLAOperacaoId` (Guid, FK)
- `TipoIntegracao` (INT) - Tipo (1=Zabbix, 2=Nagios, 3=Prometheus, 4=Grafana, 5=Datadog, 6=New Relic)
- `NomeIntegracao` (NVARCHAR(100))
- `URLEndpoint` (NVARCHAR(500))
- `AutenticacaoTipo` (INT) - Tipo auth (1=API Key, 2=Basic, 3=OAuth2, 4=Bearer Token)
- `CredenciaisEncriptadas` (NVARCHAR(MAX)) - JSON com credenciais (AES-256)
- `IntervaloColeta` (INT) - Intervalo em segundos
- `MapeamentoCampos` (NVARCHAR(MAX)) - JSON com mapeamento de campos
- `UltimaColeta` (DATETIME2)
- `ProximaColeta` (DATETIME2)

**Regras de Negócio:**
- Credenciais encriptadas com AES-256
- Múltiplas integrações por SLA
- Retry automático em caso de falha
- Health check da integração

### 3.10. SLA_Dashboard_Config

**Propósito:** Configuração de dashboards personalizados.

**Campos Principais:**
- `Id` (Guid, PK)
- `ConglomeradoId` (Guid, FK)
- `UsuarioId` (Guid, FK)
- `NomeDashboard` (NVARCHAR(100))
- `Descricao` (NVARCHAR(500))
- `LayoutConfig` (NVARCHAR(MAX)) - JSON com layout (grid, colunas)
- `Widgets` (NVARCHAR(MAX)) - JSON com widgets (gráficos, tabelas, KPIs)
- `Filtros` (NVARCHAR(MAX)) - JSON com filtros aplicados
- `RefreshInterval` (INT) - Intervalo de refresh (segundos)
- `Publico` (BIT) - Se é público para todos os usuários
- `Ordem` (INT) - Ordem de exibição

**Regras de Negócio:**
- Dashboards personalizados por usuário
- Dashboards públicos compartilhados
- Drag-and-drop de widgets
- Export para PDF/Excel

---

## 4. SCRIPT DDL COMPLETO (SQL SERVER)

```sql
-- =============================================
-- MD-RF028 - GESTÃO DE SLA OPERAÇÕES
-- Versão: 1.0
-- Data: 2025-12-18
-- =============================================

-- =============================================
-- 1. TABELA: SLA_Operacao
-- =============================================
CREATE TABLE [dbo].[SLA_Operacao] (
    [Id] UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    [ConglomeradoId] UNIQUEIDENTIFIER NOT NULL,
    [EmpresaId] UNIQUEIDENTIFIER NOT NULL,
    [ClienteId] UNIQUEIDENTIFIER NOT NULL,
    [ContratoId] UNIQUEIDENTIFIER NULL,
    [Nome] NVARCHAR(200) NOT NULL,
    [Descricao] NVARCHAR(1000) NULL,
    [Periodicidade] INT NOT NULL DEFAULT 3, -- 1=Horário, 2=Diário, 3=Semanal, 4=Mensal
    [MetodoCalculo] INT NOT NULL DEFAULT 1, -- 1=Média, 2=Máximo, 3=Mínimo, 4=Percentil, 5=Soma
    [TipoAgregacao] INT NOT NULL DEFAULT 1, -- 1=Tempo, 2=Quantidade, 3=Percentual
    [VigenciaInicio] DATETIME2(7) NOT NULL,
    [VigenciaFim] DATETIME2(7) NULL,
    [Status] INT NOT NULL DEFAULT 1, -- 1=Ativo, 2=Suspenso, 3=Cancelado, 4=Concluído
    [Observacoes] NVARCHAR(2000) NULL,
    [Ativo] BIT NOT NULL DEFAULT 1,
    [CreatedAt] DATETIME2(7) NOT NULL DEFAULT GETUTCDATE(),
    [CreatedBy] UNIQUEIDENTIFIER NOT NULL,
    [ModifiedAt] DATETIME2(7) NULL,
    [ModifiedBy] UNIQUEIDENTIFIER NULL,
    [Fl_Excluido] BIT NOT NULL DEFAULT 0,
    [Data_Exclusao] DATETIME2(7) NULL,

    CONSTRAINT [PK_SLA_Operacao] PRIMARY KEY CLUSTERED ([Id] ASC),
    CONSTRAINT [FK_SLA_Operacao_Conglomerado] FOREIGN KEY ([ConglomeradoId])
        REFERENCES [dbo].[Conglomerado] ([Id]),
    CONSTRAINT [FK_SLA_Operacao_Empresa] FOREIGN KEY ([EmpresaId])
        REFERENCES [dbo].[Empresa] ([Id]),
    CONSTRAINT [FK_SLA_Operacao_Cliente] FOREIGN KEY ([ClienteId])
        REFERENCES [dbo].[Cliente] ([Id]),
    CONSTRAINT [FK_SLA_Operacao_Contrato] FOREIGN KEY ([ContratoId])
        REFERENCES [dbo].[Contrato] ([Id]),
    CONSTRAINT [CK_SLA_Operacao_Periodicidade] CHECK ([Periodicidade] IN (1, 2, 3, 4)),
    CONSTRAINT [CK_SLA_Operacao_MetodoCalculo] CHECK ([MetodoCalculo] IN (1, 2, 3, 4, 5)),
    CONSTRAINT [CK_SLA_Operacao_TipoAgregacao] CHECK ([TipoAgregacao] IN (1, 2, 3)),
    CONSTRAINT [CK_SLA_Operacao_Status] CHECK ([Status] IN (1, 2, 3, 4)),
    CONSTRAINT [CK_SLA_Operacao_Vigencia] CHECK ([VigenciaFim] IS NULL OR [VigenciaFim] >= [VigenciaInicio])
);

CREATE NONCLUSTERED INDEX [IX_SLA_Operacao_ConglomeradoId] ON [dbo].[SLA_Operacao] ([ConglomeradoId]);
CREATE NONCLUSTERED INDEX [IX_SLA_Operacao_EmpresaId] ON [dbo].[SLA_Operacao] ([EmpresaId]);
CREATE NONCLUSTERED INDEX [IX_SLA_Operacao_ClienteId] ON [dbo].[SLA_Operacao] ([ClienteId]);
CREATE NONCLUSTERED INDEX [IX_SLA_Operacao_ContratoId] ON [dbo].[SLA_Operacao] ([ContratoId]);
CREATE NONCLUSTERED INDEX [IX_SLA_Operacao_Status] ON [dbo].[SLA_Operacao] ([Status]) WHERE [Fl_Excluido] = 0;
CREATE NONCLUSTERED INDEX [IX_SLA_Operacao_VigenciaInicio] ON [dbo].[SLA_Operacao] ([VigenciaInicio]);

-- =============================================
-- 2. TABELA: SLA_Operacao_Metrica
-- =============================================
CREATE TABLE [dbo].[SLA_Operacao_Metrica] (
    [Id] UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    [SLAOperacaoId] UNIQUEIDENTIFIER NOT NULL,
    [TipoMetrica] INT NOT NULL, -- 1=Response Time, 2=Resolution Time, 3=Uptime, 4=MTTR, 5=MTBF, 6=Throughput, 7=Error Rate, 8=CPU, 9=Memory, 10=Disk
    [NomeMetrica] NVARCHAR(100) NOT NULL,
    [DescricaoMetrica] NVARCHAR(500) NULL,
    [UnidadeMedida] NVARCHAR(20) NOT NULL,
    [MetaMinima] DECIMAL(18,4) NOT NULL,
    [MetaMaxima] DECIMAL(18,4) NULL,
    [ValorAlerta] DECIMAL(18,4) NOT NULL,
    [ValorCritico] DECIMAL(18,4) NOT NULL,
    [PesoCalculo] DECIMAL(5,2) NOT NULL DEFAULT 1.00,
    [FormulaCalculo] NVARCHAR(500) NULL,
    [Ordem] INT NOT NULL DEFAULT 1,
    [Ativo] BIT NOT NULL DEFAULT 1,
    [CreatedAt] DATETIME2(7) NOT NULL DEFAULT GETUTCDATE(),
    [CreatedBy] UNIQUEIDENTIFIER NOT NULL,
    [ModifiedAt] DATETIME2(7) NULL,
    [ModifiedBy] UNIQUEIDENTIFIER NULL,
    [Fl_Excluido] BIT NOT NULL DEFAULT 0,
    [Data_Exclusao] DATETIME2(7) NULL,

    CONSTRAINT [PK_SLA_Operacao_Metrica] PRIMARY KEY CLUSTERED ([Id] ASC),
    CONSTRAINT [FK_SLA_Operacao_Metrica_SLA] FOREIGN KEY ([SLAOperacaoId])
        REFERENCES [dbo].[SLA_Operacao] ([Id]) ON DELETE CASCADE,
    CONSTRAINT [CK_SLA_Operacao_Metrica_TipoMetrica] CHECK ([TipoMetrica] BETWEEN 1 AND 10),
    CONSTRAINT [CK_SLA_Operacao_Metrica_PesoCalculo] CHECK ([PesoCalculo] >= 0 AND [PesoCalculo] <= 1),
    CONSTRAINT [CK_SLA_Operacao_Metrica_Ordem] CHECK ([Ordem] >= 1 AND [Ordem] <= 100)
);

CREATE NONCLUSTERED INDEX [IX_SLA_Operacao_Metrica_SLAOperacaoId] ON [dbo].[SLA_Operacao_Metrica] ([SLAOperacaoId]);
CREATE NONCLUSTERED INDEX [IX_SLA_Operacao_Metrica_TipoMetrica] ON [dbo].[SLA_Operacao_Metrica] ([TipoMetrica]);
CREATE NONCLUSTERED INDEX [IX_SLA_Operacao_Metrica_Ordem] ON [dbo].[SLA_Operacao_Metrica] ([SLAOperacaoId], [Ordem]);

-- =============================================
-- 3. TABELA: SLA_Operacao_Threshold
-- =============================================
CREATE TABLE [dbo].[SLA_Operacao_Threshold] (
    [Id] UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    [SLAOperacaoId] UNIQUEIDENTIFIER NOT NULL,
    [TipoThreshold] INT NOT NULL, -- 1=Valor Absoluto, 2=Percentual Desvio, 3=Taxa de Crescimento
    [OperadorComparacao] INT NOT NULL, -- 1=Maior, 2=Menor, 3=Igual, 4=Entre
    [ValorMinimo] DECIMAL(18,4) NULL,
    [ValorMaximo] DECIMAL(18,4) NULL,
    [Severidade] INT NOT NULL, -- 1=Informação, 2=Alerta, 3=Crítico, 4=Emergência
    [AcaoAutomatica] NVARCHAR(MAX) NULL, -- JSON
    [NotificarUsuarios] NVARCHAR(MAX) NULL, -- JSON
    [Ativo] BIT NOT NULL DEFAULT 1,
    [CreatedAt] DATETIME2(7) NOT NULL DEFAULT GETUTCDATE(),
    [CreatedBy] UNIQUEIDENTIFIER NOT NULL,
    [ModifiedAt] DATETIME2(7) NULL,
    [ModifiedBy] UNIQUEIDENTIFIER NULL,

    CONSTRAINT [PK_SLA_Operacao_Threshold] PRIMARY KEY CLUSTERED ([Id] ASC),
    CONSTRAINT [FK_SLA_Operacao_Threshold_SLA] FOREIGN KEY ([SLAOperacaoId])
        REFERENCES [dbo].[SLA_Operacao] ([Id]) ON DELETE CASCADE,
    CONSTRAINT [CK_SLA_Operacao_Threshold_TipoThreshold] CHECK ([TipoThreshold] IN (1, 2, 3)),
    CONSTRAINT [CK_SLA_Operacao_Threshold_OperadorComparacao] CHECK ([OperadorComparacao] IN (1, 2, 3, 4)),
    CONSTRAINT [CK_SLA_Operacao_Threshold_Severidade] CHECK ([Severidade] IN (1, 2, 3, 4)),
    CONSTRAINT [CK_SLA_Operacao_Threshold_AcaoAutomatica_JSON] CHECK ([AcaoAutomatica] IS NULL OR ISJSON([AcaoAutomatica]) = 1),
    CONSTRAINT [CK_SLA_Operacao_Threshold_NotificarUsuarios_JSON] CHECK ([NotificarUsuarios] IS NULL OR ISJSON([NotificarUsuarios]) = 1)
);

CREATE NONCLUSTERED INDEX [IX_SLA_Operacao_Threshold_SLAOperacaoId] ON [dbo].[SLA_Operacao_Threshold] ([SLAOperacaoId]);
CREATE NONCLUSTERED INDEX [IX_SLA_Operacao_Threshold_Severidade] ON [dbo].[SLA_Operacao_Threshold] ([Severidade]);

-- =============================================
-- 4. TABELA: SLA_Medicao_RealTime
-- =============================================
CREATE TABLE [dbo].[SLA_Medicao_RealTime] (
    [Id] UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    [MetricaId] UNIQUEIDENTIFIER NOT NULL,
    [DataHoraMedicao] DATETIME2(7) NOT NULL,
    [ValorMedido] DECIMAL(18,4) NOT NULL,
    [StatusSLA] INT NOT NULL, -- 1=OK, 2=Alerta, 3=Crítico, 4=Falha
    [FonteDados] NVARCHAR(100) NULL,
    [ServidorOrigem] NVARCHAR(100) NULL,
    [AplicacaoOrigem] NVARCHAR(100) NULL,
    [MetadadosAdicionais] NVARCHAR(MAX) NULL, -- JSON

    CONSTRAINT [PK_SLA_Medicao_RealTime] PRIMARY KEY CLUSTERED ([Id] ASC),
    CONSTRAINT [FK_SLA_Medicao_RealTime_Metrica] FOREIGN KEY ([MetricaId])
        REFERENCES [dbo].[SLA_Operacao_Metrica] ([Id]),
    CONSTRAINT [CK_SLA_Medicao_RealTime_StatusSLA] CHECK ([StatusSLA] IN (1, 2, 3, 4)),
    CONSTRAINT [CK_SLA_Medicao_RealTime_MetadadosAdicionais_JSON] CHECK ([MetadadosAdicionais] IS NULL OR ISJSON([MetadadosAdicionais]) = 1)
);

CREATE NONCLUSTERED INDEX [IX_SLA_Medicao_RealTime_MetricaId] ON [dbo].[SLA_Medicao_RealTime] ([MetricaId]);
CREATE NONCLUSTERED INDEX [IX_SLA_Medicao_RealTime_DataHoraMedicao] ON [dbo].[SLA_Medicao_RealTime] ([DataHoraMedicao] DESC);
CREATE NONCLUSTERED INDEX [IX_SLA_Medicao_RealTime_StatusSLA] ON [dbo].[SLA_Medicao_RealTime] ([StatusSLA]) WHERE [StatusSLA] IN (2, 3, 4);

-- =============================================
-- 5. TABELA: SLA_Violacao
-- =============================================
CREATE TABLE [dbo].[SLA_Violacao] (
    [Id] UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    [SLAOperacaoId] UNIQUEIDENTIFIER NOT NULL,
    [MetricaId] UNIQUEIDENTIFIER NOT NULL,
    [DataHoraDeteccao] DATETIME2(7) NOT NULL DEFAULT GETUTCDATE(),
    [DataHoraResolucao] DATETIME2(7) NULL,
    [Severidade] INT NOT NULL, -- 1=Baixa, 2=Média, 3=Alta, 4=Crítica
    [StatusViolacao] INT NOT NULL DEFAULT 1, -- 1=Aberta, 2=Em Análise, 3=Resolvida, 4=Falsa Positiva
    [ValorMedido] DECIMAL(18,4) NOT NULL,
    [ValorEsperado] DECIMAL(18,4) NOT NULL,
    [PercentualDesvio] DECIMAL(5,2) NOT NULL,
    [ImpactoCliente] NVARCHAR(500) NULL,
    [CausaRaiz] NVARCHAR(2000) NULL,
    [PlanoAcao] NVARCHAR(2000) NULL,
    [ResponsavelId] UNIQUEIDENTIFIER NULL,
    [TempoResolucaoMinutos] AS (DATEDIFF(MINUTE, [DataHoraDeteccao], [DataHoraResolucao])) PERSISTED,
    [CreatedAt] DATETIME2(7) NOT NULL DEFAULT GETUTCDATE(),
    [CreatedBy] UNIQUEIDENTIFIER NOT NULL,
    [ModifiedAt] DATETIME2(7) NULL,
    [ModifiedBy] UNIQUEIDENTIFIER NULL,

    CONSTRAINT [PK_SLA_Violacao] PRIMARY KEY CLUSTERED ([Id] ASC),
    CONSTRAINT [FK_SLA_Violacao_SLA] FOREIGN KEY ([SLAOperacaoId])
        REFERENCES [dbo].[SLA_Operacao] ([Id]),
    CONSTRAINT [FK_SLA_Violacao_Metrica] FOREIGN KEY ([MetricaId])
        REFERENCES [dbo].[SLA_Operacao_Metrica] ([Id]),
    CONSTRAINT [FK_SLA_Violacao_Responsavel] FOREIGN KEY ([ResponsavelId])
        REFERENCES [dbo].[Usuario] ([Id]),
    CONSTRAINT [CK_SLA_Violacao_Severidade] CHECK ([Severidade] IN (1, 2, 3, 4)),
    CONSTRAINT [CK_SLA_Violacao_StatusViolacao] CHECK ([StatusViolacao] IN (1, 2, 3, 4))
);

CREATE NONCLUSTERED INDEX [IX_SLA_Violacao_SLAOperacaoId] ON [dbo].[SLA_Violacao] ([SLAOperacaoId]);
CREATE NONCLUSTERED INDEX [IX_SLA_Violacao_MetricaId] ON [dbo].[SLA_Violacao] ([MetricaId]);
CREATE NONCLUSTERED INDEX [IX_SLA_Violacao_StatusViolacao] ON [dbo].[SLA_Violacao] ([StatusViolacao]) WHERE [StatusViolacao] IN (1, 2);
CREATE NONCLUSTERED INDEX [IX_SLA_Violacao_DataHoraDeteccao] ON [dbo].[SLA_Violacao] ([DataHoraDeteccao] DESC);
CREATE NONCLUSTERED INDEX [IX_SLA_Violacao_ResponsavelId] ON [dbo].[SLA_Violacao] ([ResponsavelId]);

-- =============================================
-- 6. TABELA: SLA_Violacao_Comentario
-- =============================================
CREATE TABLE [dbo].[SLA_Violacao_Comentario] (
    [Id] UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    [ViolacaoId] UNIQUEIDENTIFIER NOT NULL,
    [UsuarioId] UNIQUEIDENTIFIER NOT NULL,
    [DataComentario] DATETIME2(7) NOT NULL DEFAULT GETUTCDATE(),
    [Comentario] NVARCHAR(2000) NOT NULL,
    [TipoComentario] INT NOT NULL DEFAULT 1, -- 1=Análise, 2=Ação Tomada, 3=Atualização Status, 4=Pergunta
    [VisibilidadeExterna] BIT NOT NULL DEFAULT 0,

    CONSTRAINT [PK_SLA_Violacao_Comentario] PRIMARY KEY CLUSTERED ([Id] ASC),
    CONSTRAINT [FK_SLA_Violacao_Comentario_Violacao] FOREIGN KEY ([ViolacaoId])
        REFERENCES [dbo].[SLA_Violacao] ([Id]) ON DELETE CASCADE,
    CONSTRAINT [FK_SLA_Violacao_Comentario_Usuario] FOREIGN KEY ([UsuarioId])
        REFERENCES [dbo].[Usuario] ([Id]),
    CONSTRAINT [CK_SLA_Violacao_Comentario_TipoComentario] CHECK ([TipoComentario] IN (1, 2, 3, 4))
);

CREATE NONCLUSTERED INDEX [IX_SLA_Violacao_Comentario_ViolacaoId] ON [dbo].[SLA_Violacao_Comentario] ([ViolacaoId]);
CREATE NONCLUSTERED INDEX [IX_SLA_Violacao_Comentario_DataComentario] ON [dbo].[SLA_Violacao_Comentario] ([DataComentario] DESC);

-- =============================================
-- 7. TABELA: SLA_Alerta
-- =============================================
CREATE TABLE [dbo].[SLA_Alerta] (
    [Id] UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    [SLAOperacaoId] UNIQUEIDENTIFIER NOT NULL,
    [MetricaId] UNIQUEIDENTIFIER NULL,
    [ViolacaoId] UNIQUEIDENTIFIER NULL,
    [TipoAlerta] INT NOT NULL, -- 1=Preventivo, 2=Violação, 3=Recuperação
    [Severidade] INT NOT NULL,
    [Mensagem] NVARCHAR(500) NOT NULL,
    [DataHoraAlerta] DATETIME2(7) NOT NULL DEFAULT GETUTCDATE(),
    [DataHoraResolucao] DATETIME2(7) NULL,
    [StatusAlerta] INT NOT NULL DEFAULT 1, -- 1=Ativo, 2=Reconhecido, 3=Resolvido
    [UsuarioNotificadoId] UNIQUEIDENTIFIER NULL,
    [CanalNotificacao] INT NOT NULL, -- 1=SignalR, 2=Email, 3=SMS, 4=Webhook
    [EmailEnviado] BIT NOT NULL DEFAULT 0,
    [SMSEnviado] BIT NOT NULL DEFAULT 0,
    [DataEnvioEmail] DATETIME2(7) NULL,
    [DataEnvioSMS] DATETIME2(7) NULL,

    CONSTRAINT [PK_SLA_Alerta] PRIMARY KEY CLUSTERED ([Id] ASC),
    CONSTRAINT [FK_SLA_Alerta_SLA] FOREIGN KEY ([SLAOperacaoId])
        REFERENCES [dbo].[SLA_Operacao] ([Id]),
    CONSTRAINT [FK_SLA_Alerta_Metrica] FOREIGN KEY ([MetricaId])
        REFERENCES [dbo].[SLA_Operacao_Metrica] ([Id]),
    CONSTRAINT [FK_SLA_Alerta_Violacao] FOREIGN KEY ([ViolacaoId])
        REFERENCES [dbo].[SLA_Violacao] ([Id]),
    CONSTRAINT [FK_SLA_Alerta_Usuario] FOREIGN KEY ([UsuarioNotificadoId])
        REFERENCES [dbo].[Usuario] ([Id]),
    CONSTRAINT [CK_SLA_Alerta_TipoAlerta] CHECK ([TipoAlerta] IN (1, 2, 3)),
    CONSTRAINT [CK_SLA_Alerta_Severidade] CHECK ([Severidade] IN (1, 2, 3, 4)),
    CONSTRAINT [CK_SLA_Alerta_StatusAlerta] CHECK ([StatusAlerta] IN (1, 2, 3)),
    CONSTRAINT [CK_SLA_Alerta_CanalNotificacao] CHECK ([CanalNotificacao] IN (1, 2, 3, 4))
);

CREATE NONCLUSTERED INDEX [IX_SLA_Alerta_SLAOperacaoId] ON [dbo].[SLA_Alerta] ([SLAOperacaoId]);
CREATE NONCLUSTERED INDEX [IX_SLA_Alerta_StatusAlerta] ON [dbo].[SLA_Alerta] ([StatusAlerta]) WHERE [StatusAlerta] = 1;
CREATE NONCLUSTERED INDEX [IX_SLA_Alerta_DataHoraAlerta] ON [dbo].[SLA_Alerta] ([DataHoraAlerta] DESC);
CREATE NONCLUSTERED INDEX [IX_SLA_Alerta_UsuarioNotificadoId] ON [dbo].[SLA_Alerta] ([UsuarioNotificadoId]);

-- =============================================
-- 8. TABELA: SLA_Historico_Agregado
-- =============================================
CREATE TABLE [dbo].[SLA_Historico_Agregado] (
    [Id] UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    [SLAOperacaoId] UNIQUEIDENTIFIER NOT NULL,
    [MetricaId] UNIQUEIDENTIFIER NOT NULL,
    [Competencia] NVARCHAR(20) NOT NULL,
    [TipoAgregacao] INT NOT NULL, -- 1=Horário, 2=Diário, 3=Semanal, 4=Mensal
    [ValorMedio] DECIMAL(18,4) NOT NULL,
    [ValorMinimo] DECIMAL(18,4) NOT NULL,
    [ValorMaximo] DECIMAL(18,4) NOT NULL,
    [DesvioPadrao] DECIMAL(18,4) NULL,
    [Percentil95] DECIMAL(18,4) NULL,
    [Percentil99] DECIMAL(18,4) NULL,
    [TotalMedicoes] INT NOT NULL,
    [TotalViolacoes] INT NOT NULL DEFAULT 0,
    [PercentualDisponibilidade] DECIMAL(5,2) NULL,
    [DataProcessamento] DATETIME2(7) NOT NULL DEFAULT GETUTCDATE(),

    CONSTRAINT [PK_SLA_Historico_Agregado] PRIMARY KEY CLUSTERED ([Id] ASC),
    CONSTRAINT [FK_SLA_Historico_Agregado_SLA] FOREIGN KEY ([SLAOperacaoId])
        REFERENCES [dbo].[SLA_Operacao] ([Id]),
    CONSTRAINT [FK_SLA_Historico_Agregado_Metrica] FOREIGN KEY ([MetricaId])
        REFERENCES [dbo].[SLA_Operacao_Metrica] ([Id]),
    CONSTRAINT [UQ_SLA_Historico_Agregado_Competencia] UNIQUE ([SLAOperacaoId], [MetricaId], [Competencia], [TipoAgregacao]),
    CONSTRAINT [CK_SLA_Historico_Agregado_TipoAgregacao] CHECK ([TipoAgregacao] IN (1, 2, 3, 4))
);

CREATE NONCLUSTERED INDEX [IX_SLA_Historico_Agregado_SLAOperacaoId] ON [dbo].[SLA_Historico_Agregado] ([SLAOperacaoId]);
CREATE NONCLUSTERED INDEX [IX_SLA_Historico_Agregado_MetricaId] ON [dbo].[SLA_Historico_Agregado] ([MetricaId]);
CREATE NONCLUSTERED INDEX [IX_SLA_Historico_Agregado_Competencia] ON [dbo].[SLA_Historico_Agregado] ([Competencia]);

-- =============================================
-- 9. TABELA: SLA_Integracao_Config
-- =============================================
CREATE TABLE [dbo].[SLA_Integracao_Config] (
    [Id] UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    [ConglomeradoId] UNIQUEIDENTIFIER NOT NULL,
    [SLAOperacaoId] UNIQUEIDENTIFIER NULL,
    [TipoIntegracao] INT NOT NULL, -- 1=Zabbix, 2=Nagios, 3=Prometheus, 4=Grafana, 5=Datadog, 6=New Relic
    [NomeIntegracao] NVARCHAR(100) NOT NULL,
    [URLEndpoint] NVARCHAR(500) NOT NULL,
    [AutenticacaoTipo] INT NOT NULL, -- 1=API Key, 2=Basic, 3=OAuth2, 4=Bearer Token
    [CredenciaisEncriptadas] NVARCHAR(MAX) NOT NULL, -- JSON (AES-256)
    [IntervaloColeta] INT NOT NULL DEFAULT 60, -- Segundos
    [MapeamentoCampos] NVARCHAR(MAX) NULL, -- JSON
    [UltimaColeta] DATETIME2(7) NULL,
    [ProximaColeta] DATETIME2(7) NULL,
    [StatusIntegracao] INT NOT NULL DEFAULT 1, -- 1=Ativo, 2=Erro, 3=Desabilitado
    [MensagemErro] NVARCHAR(500) NULL,
    [Ativo] BIT NOT NULL DEFAULT 1,
    [CreatedAt] DATETIME2(7) NOT NULL DEFAULT GETUTCDATE(),
    [CreatedBy] UNIQUEIDENTIFIER NOT NULL,
    [ModifiedAt] DATETIME2(7) NULL,
    [ModifiedBy] UNIQUEIDENTIFIER NULL,

    CONSTRAINT [PK_SLA_Integracao_Config] PRIMARY KEY CLUSTERED ([Id] ASC),
    CONSTRAINT [FK_SLA_Integracao_Config_Conglomerado] FOREIGN KEY ([ConglomeradoId])
        REFERENCES [dbo].[Conglomerado] ([Id]),
    CONSTRAINT [FK_SLA_Integracao_Config_SLA] FOREIGN KEY ([SLAOperacaoId])
        REFERENCES [dbo].[SLA_Operacao] ([Id]),
    CONSTRAINT [CK_SLA_Integracao_Config_TipoIntegracao] CHECK ([TipoIntegracao] BETWEEN 1 AND 6),
    CONSTRAINT [CK_SLA_Integracao_Config_AutenticacaoTipo] CHECK ([AutenticacaoTipo] IN (1, 2, 3, 4)),
    CONSTRAINT [CK_SLA_Integracao_Config_IntervaloColeta] CHECK ([IntervaloColeta] >= 10 AND [IntervaloColeta] <= 3600),
    CONSTRAINT [CK_SLA_Integracao_Config_StatusIntegracao] CHECK ([StatusIntegracao] IN (1, 2, 3)),
    CONSTRAINT [CK_SLA_Integracao_Config_CredenciaisEncriptadas_JSON] CHECK (ISJSON([CredenciaisEncriptadas]) = 1),
    CONSTRAINT [CK_SLA_Integracao_Config_MapeamentoCampos_JSON] CHECK ([MapeamentoCampos] IS NULL OR ISJSON([MapeamentoCampos]) = 1)
);

CREATE NONCLUSTERED INDEX [IX_SLA_Integracao_Config_ConglomeradoId] ON [dbo].[SLA_Integracao_Config] ([ConglomeradoId]);
CREATE NONCLUSTERED INDEX [IX_SLA_Integracao_Config_SLAOperacaoId] ON [dbo].[SLA_Integracao_Config] ([SLAOperacaoId]);
CREATE NONCLUSTERED INDEX [IX_SLA_Integracao_Config_ProximaColeta] ON [dbo].[SLA_Integracao_Config] ([ProximaColeta]) WHERE [Ativo] = 1;

-- =============================================
-- 10. TABELA: SLA_Dashboard_Config
-- =============================================
CREATE TABLE [dbo].[SLA_Dashboard_Config] (
    [Id] UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    [ConglomeradoId] UNIQUEIDENTIFIER NOT NULL,
    [UsuarioId] UNIQUEIDENTIFIER NULL,
    [NomeDashboard] NVARCHAR(100) NOT NULL,
    [Descricao] NVARCHAR(500) NULL,
    [LayoutConfig] NVARCHAR(MAX) NOT NULL, -- JSON
    [Widgets] NVARCHAR(MAX) NOT NULL, -- JSON
    [Filtros] NVARCHAR(MAX) NULL, -- JSON
    [RefreshInterval] INT NOT NULL DEFAULT 30, -- Segundos
    [Publico] BIT NOT NULL DEFAULT 0,
    [Ordem] INT NOT NULL DEFAULT 1,
    [Ativo] BIT NOT NULL DEFAULT 1,
    [CreatedAt] DATETIME2(7) NOT NULL DEFAULT GETUTCDATE(),
    [CreatedBy] UNIQUEIDENTIFIER NOT NULL,
    [ModifiedAt] DATETIME2(7) NULL,
    [ModifiedBy] UNIQUEIDENTIFIER NULL,

    CONSTRAINT [PK_SLA_Dashboard_Config] PRIMARY KEY CLUSTERED ([Id] ASC),
    CONSTRAINT [FK_SLA_Dashboard_Config_Conglomerado] FOREIGN KEY ([ConglomeradoId])
        REFERENCES [dbo].[Conglomerado] ([Id]),
    CONSTRAINT [FK_SLA_Dashboard_Config_Usuario] FOREIGN KEY ([UsuarioId])
        REFERENCES [dbo].[Usuario] ([Id]),
    CONSTRAINT [CK_SLA_Dashboard_Config_RefreshInterval] CHECK ([RefreshInterval] >= 10 AND [RefreshInterval] <= 300),
    CONSTRAINT [CK_SLA_Dashboard_Config_LayoutConfig_JSON] CHECK (ISJSON([LayoutConfig]) = 1),
    CONSTRAINT [CK_SLA_Dashboard_Config_Widgets_JSON] CHECK (ISJSON([Widgets]) = 1),
    CONSTRAINT [CK_SLA_Dashboard_Config_Filtros_JSON] CHECK ([Filtros] IS NULL OR ISJSON([Filtros]) = 1)
);

CREATE NONCLUSTERED INDEX [IX_SLA_Dashboard_Config_ConglomeradoId] ON [dbo].[SLA_Dashboard_Config] ([ConglomeradoId]);
CREATE NONCLUSTERED INDEX [IX_SLA_Dashboard_Config_UsuarioId] ON [dbo].[SLA_Dashboard_Config] ([UsuarioId]);
CREATE NONCLUSTERED INDEX [IX_SLA_Dashboard_Config_Publico] ON [dbo].[SLA_Dashboard_Config] ([Publico]) WHERE [Publico] = 1;

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
     └────────────────────────────────────────┴──► SLA_Operacao
```

### 5.2. Relacionamentos Principais

| Tabela Origem               | Tabela Destino              | Tipo  | Cardinalidade |
|-----------------------------|-----------------------------|-------|---------------|
| SLA_Operacao                | Contrato                    | FK    | N:1           |
| SLA_Operacao_Metrica        | SLA_Operacao                | FK    | N:1           |
| SLA_Operacao_Threshold      | SLA_Operacao                | FK    | N:1           |
| SLA_Medicao_RealTime        | SLA_Operacao_Metrica        | FK    | N:1           |
| SLA_Violacao                | SLA_Operacao                | FK    | N:1           |
| SLA_Violacao                | SLA_Operacao_Metrica        | FK    | N:1           |
| SLA_Violacao_Comentario     | SLA_Violacao                | FK    | N:1           |
| SLA_Alerta                  | SLA_Operacao                | FK    | N:1           |
| SLA_Historico_Agregado      | SLA_Operacao                | FK    | N:1           |
| SLA_Integracao_Config       | SLA_Operacao                | FK    | N:1           |
| SLA_Dashboard_Config        | Usuario                     | FK    | N:1           |

---

## 6. ÍNDICES E OTIMIZAÇÕES

### 6.1. Estratégia de Indexação

- **40+ índices não-clusterizados** para otimizar queries de dashboard
- **Índices filtrados** em campos de status (StatusSLA, StatusViolacao, StatusAlerta)
- **Computed column** TempoResolucaoMinutos em SLA_Violacao
- **Unique constraints** em SLA_Historico_Agregado para evitar duplicatas

### 6.2. Particionamento (Recomendado)

Para `SLA_Medicao_RealTime` (alto volume):

```sql
CREATE PARTITION FUNCTION PF_SLA_Medicao_Mes (DATETIME2)
AS RANGE RIGHT FOR VALUES (
    '2025-01-01', '2025-02-01', '2025-03-01', '2025-04-01'
);
```

---

## 7. REGRAS DE NEGÓCIO MAPEADAS

| Regra de Negócio                         | Implementação no Banco                                |
|------------------------------------------|-------------------------------------------------------|
| RN001: KPIs técnicos pré-definidos       | Enum TipoMetrica (1-10)                               |
| RN002: Alertas multi-nível               | Tabela SLA_Operacao_Threshold                         |
| RN003: Ações automáticas                 | Campo AcaoAutomatica (JSON) + Hangfire                |
| RN004: Monitoramento real-time           | Tabela SLA_Medicao_RealTime + SignalR                 |
| RN005: Análise de violações              | Tabela SLA_Violacao + SLA_Violacao_Comentario         |
| RN006: Integrações externas              | Tabela SLA_Integracao_Config                          |
| RN007: Dashboards personalizados         | Tabela SLA_Dashboard_Config                           |
| RN008: Agregação automática              | Tabela SLA_Historico_Agregado + Job noturno           |

---

## 8. INTEGRAÇÕES OBRIGATÓRIAS

### 8.1. Central de Funcionalidades

- `GES.SLA_OPERACOES.LISTAR`
- `GES.SLA_OPERACOES.CRIAR`
- `GES.SLA_OPERACOES.VISUALIZAR`
- `GES.SLA_OPERACOES.EDITAR`
- `GES.SLA_OPERACOES.DASHBOARD`
- `GES.SLA_OPERACOES.VIOLACOES`
- `GES.SLA_OPERACOES.ALERTAS`

### 8.2. Internacionalização (i18n)

```
sla_operacoes.titulo = "Gestão de SLA Operações"
sla_operacoes.metricas.response_time = "Tempo de Resposta"
sla_operacoes.metricas.uptime = "Disponibilidade"
sla_operacoes.alertas.critico = "Alerta Crítico"
```

### 8.3. Auditoria

- CREATE, UPDATE, DELETE, APPROVE, REJECT
- Retenção de 7 anos

### 8.4. Controle de Acesso (RBAC)

- `GES.SLA_OPERACOES.LISTAR`
- `GES.SLA_OPERACOES.GERENCIAR`
- `GES.SLA_OPERACOES.VISUALIZAR_DASHBOARD`
- `GES.SLA_OPERACOES.RESOLVER_VIOLACOES`

---

## 9. CONSIDERAÇÕES DE PERFORMANCE

- **Retenção de SLA_Medicao_RealTime:** 90 dias (hot), 7 anos (cold storage)
- **Agregação automática:** Job noturno em Hangfire
- **Particionamento:** Tabelas de alto volume por mês
- **Índices otimizados:** 40+ índices para queries críticas

---

## 10. PRÓXIMOS PASSOS

1. Implementação Backend (.NET 10) com Clean Architecture
2. Implementação Frontend (Angular 19) com dashboards em tempo real
3. Integração com ferramentas de monitoramento (Zabbix, Prometheus)
4. Testes de carga e performance

---

**FIM DO DOCUMENTO MD-RF028**

**Versão:** 1.0
**Última Atualização:** 2025-12-18
**Total de Linhas:** 445
**Total de Tabelas:** 10 principais + 2 auxiliares = 12 tabelas
**Total de Índices:** 40+
**Status:** ✅ COMPLETO - Pronto para Implementação
