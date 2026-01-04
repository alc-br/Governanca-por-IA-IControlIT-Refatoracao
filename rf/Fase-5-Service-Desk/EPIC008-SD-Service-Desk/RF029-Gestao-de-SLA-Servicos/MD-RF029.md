# MD-RF029 - Modelo de Dados: Gestão de SLA Serviços

**Versão:** 1.0
**Data:** 2025-12-18
**Responsável:** Agente Architect
**RF Relacionado:** [RF029 - Gestão de SLA Serviços](./RF029.md)
**UC Relacionado:** [UC-RF029 - Casos de Uso](./UC-RF029.md)

---

## 1. VISÃO GERAL

Este modelo de dados suporta o gerenciamento completo de SLAs de Serviços (KPIs de negócio), incluindo:

- **KPIs de Negócio:** CSAT, NPS, FCR, Quality Score, Compliance, Balanced Scorecard
- **Balanced Scorecard (BSC)** com 4 perspectivas: Financeira, Clientes, Processos, Aprendizado
- **Gestão de Metas** com acompanhamento mensal e trimestral
- **Integração com Pesquisas** (SurveyMonkey, Typeform, Google Forms)
- **Biblioteca de KPIs** com 100+ KPIs pré-configurados
- **Dashboards Executivos** com visualizações estratégicas
- **Multi-tenancy** com isolamento por Conglomerado/Empresa/Cliente
- **Auditoria Completa** de todas as operações

**Complexidade:** MUITO ALTA
**Número de Tabelas:** 14
**Relacionamentos:** 28 Foreign Keys
**Índices Otimizados:** 45+

---

## 2. DIAGRAMA ER (Entidade-Relacionamento)

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                    MODELO DE DADOS - GESTÃO DE SLA SERVIÇOS                          │
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
        ┌───────────────────────┼───────────────────────┬─────────────────┐
        │*                      │*                      │*                │*
┌───────▼──────────┐   ┌────────▼─────────┐   ┌────────▼─────────┐   ┌──▼─────────────┐
│  Contrato        │   │ SLA_Servico      │   │ Usuario          │   │ BSC_Perspectiva│
│──────────────────│   │──────────────────│   │──────────────────│   │────────────────│
│ Id (PK)          │1 *│ Id (PK)          │   │ Id (PK)          │   │ Id (PK)        │
│ ClienteId (FK)   │◄──│ ContratoId (FK)  │   │ ClienteId (FK)   │   │ CongloId (FK)  │
│ Numero           │   │ ClienteId (FK)   │   │ Nome             │   │ Nome           │
│ VigenciaInicio   │   │ Nome             │   │ Email            │   │ Descricao      │
│ VigenciaFim      │   │ Descricao        │   └──────────────────┘   │ Ordem          │
└──────────────────┘   │ TipoSLA          │                          │ Ativo          │
                       │ Periodicidade    │                          └──────┬─────────┘
                       │ VigenciaInicio   │                                 │1
                       │ VigenciaFim      │                                 │
                       │ Status           │                                 │*
                       │ Ativo            │                     ┌───────────▼──────────┐
                       └────┬─┬───────────┘                     │ BSC_Objetivo         │
                            │ │1                                │──────────────────────│
                            │ │                                 │ Id (PK)              │
                            │ │*                                │ PerspectivaId (FK)   │
                    ┌───────┘ └───────────┐                     │ Nome                 │
                    │*                    │*                    │ Descricao            │
        ┌───────────▼─────────┐   ┌───────▼─────────────┐      │ Peso                 │
        │ SLA_Servico_KPI     │   │ SLA_Servico_Meta    │      │ Ativo                │
        │─────────────────────│   │─────────────────────│      └──────┬───────────────┘
        │ Id (PK)             │   │ Id (PK)             │             │1
        │ SLAServicoId (FK)   │   │ SLAServicoId (FK)   │             │
        │ TipoKPI             │   │ Competencia         │             │*
        │ NomeKPI             │   │ TipoMeta            │   ┌─────────▼────────────┐
        │ UnidadeMedida       │   │ ValorMeta           │   │ BSC_Indicador        │
        │ MetaMinima          │   │ ValorRealizado      │   │──────────────────────│
        │ MetaMaxima          │   │ PercentualAlcance   │   │ Id (PK)              │
        │ PesoCalculo         │   │ StatusMeta          │   │ ObjetivoId (FK)      │
        │ FormulaCalculo      │   │ Justificativa       │   │ Nome                 │
        │ FonteDados          │   │ PlanoAcao           │   │ Descricao            │
        │ Ativo               │   │ ResponsavelId (FK)  │   │ Formula              │
        └───────┬─────────────┘   │ Ativo               │   │ Meta                 │
                │1                └─────────────────────┘   │ UnidadeMedida        │
                │                                           │ Frequencia           │
                │*                                          │ Ativo                │
        ┌───────▼──────────────┐                            └──────┬───────────────┘
        │ SLA_Medicao_Negocio  │                                   │1
        │──────────────────────│                                   │
        │ Id (PK)              │                                   │*
        │ KPIId (FK)           │                         ┌─────────▼──────────────┐
        │ Competencia          │                         │ BSC_Medicao            │
        │ DataMedicao          │                         │────────────────────────│
        │ ValorMedido          │                         │ Id (PK)                │
        │ StatusKPI            │                         │ IndicadorId (FK)       │
        │ FonteDados           │                         │ Competencia            │
        │ ResponsavelColeta    │                         │ ValorMedido            │
        │ Observacoes          │                         │ ValorMeta              │
        └──────────────────────┘                         │ PercentualAlcance      │
                                                         │ TendenciaTrimestre     │
        ┌──────────────────────┐                         │ Ativo                  │
        │ KPI_Biblioteca       │                         └────────────────────────┘
        │──────────────────────│
        │ Id (PK)              │
        │ ConglomeradoId (FK)  │
        │ Categoria            │
        │ CodigoKPI            │
        │ NomeKPI              │
        │ DescricaoKPI         │
        │ FormulaCalculo       │
        │ UnidadeMedida        │
        │ FonteDados           │
        │ FrequenciaColeta     │
        │ MetaSugerida         │
        │ BenchmarkIndustria   │
        │ Ativo                │
        └──────────────────────┘

        ┌──────────────────────┐
        │ SLA_Pesquisa_Config  │
        │──────────────────────│
        │ Id (PK)              │
        │ ConglomeradoId (FK)  │
        │ SLAServicoId (FK)    │
        │ TipoPesquisa         │
        │ Plataforma           │
        │ URLPesquisa          │
        │ APIKey (Encriptado)  │
        │ MapeamentoCampos     │
        │ IntervaloImportacao  │
        │ UltimaImportacao     │
        │ Ativo                │
        └──────────────────────┘

        ┌──────────────────────┐
        │ SLA_Dashboard_Exec   │
        │──────────────────────│
        │ Id (PK)              │
        │ ConglomeradoId (FK)  │
        │ UsuarioId (FK)       │
        │ NomeDashboard        │
        │ TipoDashboard        │
        │ ConfigBSC (JSON)     │
        │ ConfigKPIs (JSON)    │
        │ LayoutWidgets (JSON) │
        │ Filtros (JSON)       │
        │ Publico              │
        │ Ativo                │
        └──────────────────────┘

        ┌──────────────────────┐
        │ SLA_Relatorio_Quality│
        │──────────────────────│
        │ Id (PK)              │
        │ SLAServicoId (FK)    │
        │ Competencia          │
        │ TipoRelatorio        │
        │ ScoreGeral           │
        │ ScoreCSAT            │
        │ ScoreNPS             │
        │ ScoreFCR             │
        │ ScoreCompliance      │
        │ TotalRespostas       │
        │ DataGeracao          │
        │ ArquivoPDF           │
        └──────────────────────┘

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

### 3.1. SLA_Servico

**Propósito:** Entidade principal que define os SLAs de serviços (negócio).

**Campos Principais:**
- `Id` (Guid, PK)
- `ContratoId` (Guid, FK) - Referência ao contrato (opcional)
- `ClienteId` (Guid, FK) - Cliente proprietário (multi-tenancy)
- `EmpresaId` (Guid, FK) - Empresa proprietária (multi-tenancy)
- `ConglomeradoId` (Guid, FK) - Conglomerado proprietário (multi-tenancy)
- `Nome` (NVARCHAR(200)) - Nome do SLA (ex: "Satisfação do Cliente 2025")
- `Descricao` (NVARCHAR(1000))
- `TipoSLA` (INT) - Tipo (1=CSAT, 2=NPS, 3=FCR, 4=Quality Score, 5=Compliance, 6=BSC, 7=Customizado)
- `Periodicidade` (INT) - Periodicidade (1=Mensal, 2=Trimestral, 3=Semestral, 4=Anual)
- `VigenciaInicio` (DATETIME2)
- `VigenciaFim` (DATETIME2)
- `Status` (INT) - Status (1=Ativo, 2=Suspenso, 3=Cancelado, 4=Concluído)

**Regras de Negócio:**
- SLA pode ter múltiplos KPIs
- Periodicidade define consolidação de metas
- Integração com pesquisas externas

### 3.2. SLA_Servico_KPI

**Propósito:** KPIs específicos de cada SLA de serviço.

**Campos Principais:**
- `Id` (Guid, PK)
- `SLAServicoId` (Guid, FK)
- `TipoKPI` (INT) - Tipo (1=CSAT, 2=NPS, 3=FCR, 4=Quality Score, 5=Compliance, 6=Time to Resolution, 7=Churn Rate, 8=Customizado)
- `NomeKPI` (NVARCHAR(100))
- `DescricaoKPI` (NVARCHAR(500))
- `UnidadeMedida` (NVARCHAR(20)) - Unidade (%, pontos, score, etc.)
- `MetaMinima` (DECIMAL(18,4))
- `MetaMaxima` (DECIMAL(18,4))
- `PesoCalculo` (DECIMAL(5,2)) - Peso na média ponderada (0.00 a 1.00)
- `FormulaCalculo` (NVARCHAR(500)) - Fórmula NCalc
- `FonteDados` (NVARCHAR(200)) - Fonte (Pesquisa, CRM, Helpdesk, Manual)
- `FrequenciaColeta` (INT) - Frequência (1=Diária, 2=Semanal, 3=Mensal, 4=Sob Demanda)

**Regras de Negócio:**
- **CSAT:** Escala 1-5, meta típica ≥ 4.0
- **NPS:** Escala -100 a 100, meta típica ≥ 50
- **FCR:** First Call Resolution, meta típica ≥ 80%
- Soma dos pesos deve ser 1.00 por SLA

### 3.3. SLA_Servico_Meta

**Propósito:** Metas mensais/trimestrais com acompanhamento de realização.

**Campos Principais:**
- `Id` (Guid, PK)
- `SLAServicoId` (Guid, FK)
- `Competencia` (NVARCHAR(7)) - Competência (YYYY-MM)
- `TipoMeta` (INT) - Tipo (1=Mensal, 2=Trimestral, 3=Anual)
- `ValorMeta` (DECIMAL(18,4))
- `ValorRealizado` (DECIMAL(18,4))
- `PercentualAlcance` (DECIMAL(5,2)) - Calculated: (Realizado / Meta) * 100
- `StatusMeta` (INT) - Status (1=Em Andamento, 2=Alcançada, 3=Não Alcançada, 4=Superada)
- `Justificativa` (NVARCHAR(1000)) - Justificativa se não alcançada
- `PlanoAcao` (NVARCHAR(2000)) - Plano de ação corretiva
- `ResponsavelId` (Guid, FK)

**Regras de Negócio:**
- Meta criada automaticamente no início da competência
- Atualização manual ou via integração
- Alerta se percentual < 80% ao final da competência

### 3.4. SLA_Medicao_Negocio

**Propósito:** Medições periódicas dos KPIs de negócio.

**Campos Principais:**
- `Id` (Guid, PK)
- `KPIId` (Guid, FK)
- `Competencia` (NVARCHAR(7))
- `DataMedicao` (DATETIME2)
- `ValorMedido` (DECIMAL(18,4))
- `StatusKPI` (INT) - Status (1=Acima da Meta, 2=Na Meta, 3=Abaixo da Meta, 4=Crítico)
- `FonteDados` (NVARCHAR(200))
- `ResponsavelColeta` (UNIQUEIDENTIFIER)
- `Observacoes` (NVARCHAR(1000))
- `ArquivoEvidencia` (NVARCHAR(500))

**Regras de Negócio:**
- Medições consolidadas por competência
- Possibilidade de múltiplas medições por período
- Evidências anexadas (CSV, Excel, relatórios)

### 3.5. BSC_Perspectiva

**Propósito:** 4 perspectivas do Balanced Scorecard.

**Campos Principais:**
- `Id` (Guid, PK)
- `ConglomeradoId` (Guid, FK)
- `Nome` (NVARCHAR(100)) - Ex: "Financeira", "Clientes", "Processos", "Aprendizado"
- `Descricao` (NVARCHAR(500))
- `Icone` (NVARCHAR(50))
- `Cor` (NVARCHAR(20)) - Cor para visualização
- `Ordem` (INT) - Ordem de exibição (1-4)

**Regras de Negócio:**
- 4 perspectivas padrão (configurável)
- Cada perspectiva tem múltiplos objetivos

### 3.6. BSC_Objetivo

**Propósito:** Objetivos estratégicos dentro de cada perspectiva.

**Campos Principais:**
- `Id` (Guid, PK)
- `PerspectivaId` (Guid, FK)
- `Nome` (NVARCHAR(200)) - Ex: "Aumentar margem de lucro"
- `Descricao` (NVARCHAR(1000))
- `Peso` (DECIMAL(5,2)) - Peso no BSC (soma = 1.00 por perspectiva)
- `ResponsavelId` (Guid, FK)
- `DataInicio` (DATETIME2)
- `DataConclusao` (DATETIME2)

**Regras de Negócio:**
- Múltiplos objetivos por perspectiva
- Soma dos pesos = 1.00 por perspectiva
- Cada objetivo tem múltiplos indicadores

### 3.7. BSC_Indicador

**Propósito:** Indicadores (KPIs) que medem os objetivos.

**Campos Principais:**
- `Id` (Guid, PK)
- `ObjetivoId` (Guid, FK)
- `Nome` (NVARCHAR(200))
- `Descricao` (NVARCHAR(1000))
- `Formula` (NVARCHAR(500)) - Fórmula de cálculo
- `Meta` (DECIMAL(18,4))
- `UnidadeMedida` (NVARCHAR(20))
- `Frequencia` (INT) - Frequência de medição
- `TipoIndicador` (INT) - Tipo (1=Lagging, 2=Leading)
- `Polaridade` (INT) - Polaridade (1=Maior Melhor, 2=Menor Melhor)

**Regras de Negócio:**
- **Lagging indicators:** Resultados (ex: lucro líquido)
- **Leading indicators:** Preditivos (ex: pipeline de vendas)
- Polaridade define direção desejada

### 3.8. BSC_Medicao

**Propósito:** Medições mensais dos indicadores BSC.

**Campos Principais:**
- `Id` (Guid, PK)
- `IndicadorId` (Guid, FK)
- `Competencia` (NVARCHAR(7))
- `ValorMedido` (DECIMAL(18,4))
- `ValorMeta` (DECIMAL(18,4))
- `PercentualAlcance` (DECIMAL(5,2))
- `TendenciaTrimestre` (INT) - Tendência (1=Crescente, 2=Estável, 3=Decrescente)
- `StatusSemaforo` (INT) - Semáforo (1=Verde, 2=Amarelo, 3=Vermelho)
- `Observacoes` (NVARCHAR(1000))

**Regras de Negócio:**
- Semáforo automático: Verde (≥100%), Amarelo (80-99%), Vermelho (<80%)
- Tendência calculada com base em 3 últimos meses
- Dashboard BSC consolidado

### 3.9. KPI_Biblioteca

**Propósito:** Biblioteca de KPIs pré-configurados (100+ KPIs).

**Campos Principais:**
- `Id` (Guid, PK)
- `ConglomeradoId` (Guid, FK)
- `Categoria` (INT) - Categoria (1=Financeiro, 2=Cliente, 3=Operacional, 4=RH, 5=TI)
- `CodigoKPI` (NVARCHAR(20)) - Código único (ex: "FIN-001")
- `NomeKPI` (NVARCHAR(100))
- `DescricaoKPI` (NVARCHAR(1000))
- `FormulaCalculo` (NVARCHAR(500))
- `UnidadeMedida` (NVARCHAR(20))
- `FonteDados` (NVARCHAR(200))
- `FrequenciaColeta` (INT)
- `MetaSugerida` (NVARCHAR(50))
- `BenchmarkIndustria` (NVARCHAR(200)) - Benchmarks típicos
- `Tags` (NVARCHAR(MAX)) - JSON com tags

**Regras de Negócio:**
- Biblioteca global compartilhada
- Usuários podem criar KPIs customizados
- Importar KPI da biblioteca para SLA

### 3.10. SLA_Pesquisa_Config

**Propósito:** Configuração de integrações com plataformas de pesquisa.

**Campos Principais:**
- `Id` (Guid, PK)
- `ConglomeradoId` (Guid, FK)
- `SLAServicoId` (Guid, FK)
- `TipoPesquisa` (INT) - Tipo (1=CSAT, 2=NPS, 3=FCR, 4=Custom)
- `Plataforma` (INT) - Plataforma (1=SurveyMonkey, 2=Typeform, 3=Google Forms, 4=Qualtrics)
- `URLPesquisa` (NVARCHAR(500))
- `APIKeyEncriptada` (NVARCHAR(MAX)) - API Key (AES-256)
- `MapeamentoCampos` (NVARCHAR(MAX)) - JSON com mapeamento
- `IntervaloImportacao` (INT) - Intervalo em horas
- `UltimaImportacao` (DATETIME2)
- `ProximaImportacao` (DATETIME2)
- `StatusIntegracao` (INT)

**Regras de Negócio:**
- Importação automática via Hangfire
- Validação de API Key ao salvar
- Mapeamento flexível de campos

### 3.11. SLA_Dashboard_Exec

**Propósito:** Dashboards executivos personalizados.

**Campos Principais:**
- `Id` (Guid, PK)
- `ConglomeradoId` (Guid, FK)
- `UsuarioId` (Guid, FK)
- `NomeDashboard` (NVARCHAR(100))
- `TipoDashboard` (INT) - Tipo (1=BSC, 2=KPIs, 3=Quality, 4=Customizado)
- `ConfigBSC` (NVARCHAR(MAX)) - JSON com config BSC
- `ConfigKPIs` (NVARCHAR(MAX)) - JSON com KPIs selecionados
- `LayoutWidgets` (NVARCHAR(MAX)) - JSON com layout
- `Filtros` (NVARCHAR(MAX)) - JSON com filtros
- `Publico` (BIT)
- `RefreshInterval` (INT)

**Regras de Negócio:**
- Dashboards públicos compartilhados
- Export para PDF/PowerPoint
- Drill-down em KPIs

### 3.12. SLA_Relatorio_Quality

**Propósito:** Relatórios consolidados de qualidade.

**Campos Principais:**
- `Id` (Guid, PK)
- `SLAServicoId` (Guid, FK)
- `Competencia` (NVARCHAR(7))
- `TipoRelatorio` (INT) - Tipo (1=Mensal, 2=Trimestral, 3=Anual)
- `ScoreGeral` (DECIMAL(5,2))
- `ScoreCSAT` (DECIMAL(5,2))
- `ScoreNPS` (DECIMAL(5,2))
- `ScoreFCR` (DECIMAL(5,2))
- `ScoreCompliance` (DECIMAL(5,2))
- `TotalRespostas` (INT)
- `DataGeracao` (DATETIME2)
- `ArquivoPDF` (NVARCHAR(500))

**Regras de Negócio:**
- Geração automática ao final da competência
- Relatório em PDF com gráficos
- Distribuição automática por email

---

## 4. SCRIPT DDL COMPLETO (SQL SERVER)

```sql
-- =============================================
-- MD-RF029 - GESTÃO DE SLA SERVIÇOS
-- Versão: 1.0
-- Data: 2025-12-18
-- =============================================

-- =============================================
-- 1. TABELA: SLA_Servico
-- =============================================
CREATE TABLE [dbo].[SLA_Servico] (
    [Id] UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    [ConglomeradoId] UNIQUEIDENTIFIER NOT NULL,
    [EmpresaId] UNIQUEIDENTIFIER NOT NULL,
    [ClienteId] UNIQUEIDENTIFIER NOT NULL,
    [ContratoId] UNIQUEIDENTIFIER NULL,
    [Nome] NVARCHAR(200) NOT NULL,
    [Descricao] NVARCHAR(1000) NULL,
    [TipoSLA] INT NOT NULL, -- 1=CSAT, 2=NPS, 3=FCR, 4=Quality Score, 5=Compliance, 6=BSC, 7=Customizado
    [Periodicidade] INT NOT NULL DEFAULT 1, -- 1=Mensal, 2=Trimestral, 3=Semestral, 4=Anual
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

    CONSTRAINT [PK_SLA_Servico] PRIMARY KEY CLUSTERED ([Id] ASC),
    CONSTRAINT [FK_SLA_Servico_Conglomerado] FOREIGN KEY ([ConglomeradoId])
        REFERENCES [dbo].[Conglomerado] ([Id]),
    CONSTRAINT [FK_SLA_Servico_Empresa] FOREIGN KEY ([EmpresaId])
        REFERENCES [dbo].[Empresa] ([Id]),
    CONSTRAINT [FK_SLA_Servico_Cliente] FOREIGN KEY ([ClienteId])
        REFERENCES [dbo].[Cliente] ([Id]),
    CONSTRAINT [FK_SLA_Servico_Contrato] FOREIGN KEY ([ContratoId])
        REFERENCES [dbo].[Contrato] ([Id]),
    CONSTRAINT [CK_SLA_Servico_TipoSLA] CHECK ([TipoSLA] BETWEEN 1 AND 7),
    CONSTRAINT [CK_SLA_Servico_Periodicidade] CHECK ([Periodicidade] IN (1, 2, 3, 4)),
    CONSTRAINT [CK_SLA_Servico_Status] CHECK ([Status] IN (1, 2, 3, 4)),
    CONSTRAINT [CK_SLA_Servico_Vigencia] CHECK ([VigenciaFim] IS NULL OR [VigenciaFim] >= [VigenciaInicio])
);

CREATE NONCLUSTERED INDEX [IX_SLA_Servico_ConglomeradoId] ON [dbo].[SLA_Servico] ([ConglomeradoId]);
CREATE NONCLUSTERED INDEX [IX_SLA_Servico_ClienteId] ON [dbo].[SLA_Servico] ([ClienteId]);
CREATE NONCLUSTERED INDEX [IX_SLA_Servico_TipoSLA] ON [dbo].[SLA_Servico] ([TipoSLA]);
CREATE NONCLUSTERED INDEX [IX_SLA_Servico_Status] ON [dbo].[SLA_Servico] ([Status]) WHERE [Fl_Excluido] = 0;

-- =============================================
-- 2. TABELA: SLA_Servico_KPI
-- =============================================
CREATE TABLE [dbo].[SLA_Servico_KPI] (
    [Id] UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    [SLAServicoId] UNIQUEIDENTIFIER NOT NULL,
    [TipoKPI] INT NOT NULL, -- 1=CSAT, 2=NPS, 3=FCR, 4=Quality Score, 5=Compliance, 6=Time to Resolution, 7=Churn Rate, 8=Customizado
    [NomeKPI] NVARCHAR(100) NOT NULL,
    [DescricaoKPI] NVARCHAR(500) NULL,
    [UnidadeMedida] NVARCHAR(20) NOT NULL,
    [MetaMinima] DECIMAL(18,4) NOT NULL,
    [MetaMaxima] DECIMAL(18,4) NULL,
    [PesoCalculo] DECIMAL(5,2) NOT NULL DEFAULT 1.00,
    [FormulaCalculo] NVARCHAR(500) NULL,
    [FonteDados] NVARCHAR(200) NULL,
    [FrequenciaColeta] INT NOT NULL DEFAULT 3, -- 1=Diária, 2=Semanal, 3=Mensal, 4=Sob Demanda
    [Ordem] INT NOT NULL DEFAULT 1,
    [Ativo] BIT NOT NULL DEFAULT 1,
    [CreatedAt] DATETIME2(7) NOT NULL DEFAULT GETUTCDATE(),
    [CreatedBy] UNIQUEIDENTIFIER NOT NULL,
    [ModifiedAt] DATETIME2(7) NULL,
    [ModifiedBy] UNIQUEIDENTIFIER NULL,
    [Fl_Excluido] BIT NOT NULL DEFAULT 0,
    [Data_Exclusao] DATETIME2(7) NULL,

    CONSTRAINT [PK_SLA_Servico_KPI] PRIMARY KEY CLUSTERED ([Id] ASC),
    CONSTRAINT [FK_SLA_Servico_KPI_SLA] FOREIGN KEY ([SLAServicoId])
        REFERENCES [dbo].[SLA_Servico] ([Id]) ON DELETE CASCADE,
    CONSTRAINT [CK_SLA_Servico_KPI_TipoKPI] CHECK ([TipoKPI] BETWEEN 1 AND 8),
    CONSTRAINT [CK_SLA_Servico_KPI_PesoCalculo] CHECK ([PesoCalculo] >= 0 AND [PesoCalculo] <= 1),
    CONSTRAINT [CK_SLA_Servico_KPI_FrequenciaColeta] CHECK ([FrequenciaColeta] IN (1, 2, 3, 4))
);

CREATE NONCLUSTERED INDEX [IX_SLA_Servico_KPI_SLAServicoId] ON [dbo].[SLA_Servico_KPI] ([SLAServicoId]);
CREATE NONCLUSTERED INDEX [IX_SLA_Servico_KPI_TipoKPI] ON [dbo].[SLA_Servico_KPI] ([TipoKPI]);

-- =============================================
-- 3. TABELA: SLA_Servico_Meta
-- =============================================
CREATE TABLE [dbo].[SLA_Servico_Meta] (
    [Id] UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    [SLAServicoId] UNIQUEIDENTIFIER NOT NULL,
    [Competencia] NVARCHAR(7) NOT NULL, -- YYYY-MM
    [TipoMeta] INT NOT NULL, -- 1=Mensal, 2=Trimestral, 3=Anual
    [ValorMeta] DECIMAL(18,4) NOT NULL,
    [ValorRealizado] DECIMAL(18,4) NULL,
    [PercentualAlcance] AS (CASE WHEN [ValorMeta] = 0 THEN 0 ELSE ([ValorRealizado] / [ValorMeta]) * 100 END) PERSISTED,
    [StatusMeta] INT NOT NULL DEFAULT 1, -- 1=Em Andamento, 2=Alcançada, 3=Não Alcançada, 4=Superada
    [Justificativa] NVARCHAR(1000) NULL,
    [PlanoAcao] NVARCHAR(2000) NULL,
    [ResponsavelId] UNIQUEIDENTIFIER NULL,
    [Ativo] BIT NOT NULL DEFAULT 1,
    [CreatedAt] DATETIME2(7) NOT NULL DEFAULT GETUTCDATE(),
    [CreatedBy] UNIQUEIDENTIFIER NOT NULL,
    [ModifiedAt] DATETIME2(7) NULL,
    [ModifiedBy] UNIQUEIDENTIFIER NULL,

    CONSTRAINT [PK_SLA_Servico_Meta] PRIMARY KEY CLUSTERED ([Id] ASC),
    CONSTRAINT [FK_SLA_Servico_Meta_SLA] FOREIGN KEY ([SLAServicoId])
        REFERENCES [dbo].[SLA_Servico] ([Id]) ON DELETE CASCADE,
    CONSTRAINT [FK_SLA_Servico_Meta_Responsavel] FOREIGN KEY ([ResponsavelId])
        REFERENCES [dbo].[Usuario] ([Id]),
    CONSTRAINT [UQ_SLA_Servico_Meta_Competencia] UNIQUE ([SLAServicoId], [Competencia]),
    CONSTRAINT [CK_SLA_Servico_Meta_TipoMeta] CHECK ([TipoMeta] IN (1, 2, 3)),
    CONSTRAINT [CK_SLA_Servico_Meta_StatusMeta] CHECK ([StatusMeta] IN (1, 2, 3, 4)),
    CONSTRAINT [CK_SLA_Servico_Meta_Competencia] CHECK ([Competencia] LIKE '[0-9][0-9][0-9][0-9]-[0-1][0-9]')
);

CREATE NONCLUSTERED INDEX [IX_SLA_Servico_Meta_SLAServicoId] ON [dbo].[SLA_Servico_Meta] ([SLAServicoId]);
CREATE NONCLUSTERED INDEX [IX_SLA_Servico_Meta_Competencia] ON [dbo].[SLA_Servico_Meta] ([Competencia]);
CREATE NONCLUSTERED INDEX [IX_SLA_Servico_Meta_StatusMeta] ON [dbo].[SLA_Servico_Meta] ([StatusMeta]);

-- =============================================
-- 4. TABELA: SLA_Medicao_Negocio
-- =============================================
CREATE TABLE [dbo].[SLA_Medicao_Negocio] (
    [Id] UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    [KPIId] UNIQUEIDENTIFIER NOT NULL,
    [Competencia] NVARCHAR(7) NOT NULL,
    [DataMedicao] DATETIME2(7) NOT NULL DEFAULT GETUTCDATE(),
    [ValorMedido] DECIMAL(18,4) NOT NULL,
    [StatusKPI] INT NOT NULL, -- 1=Acima da Meta, 2=Na Meta, 3=Abaixo da Meta, 4=Crítico
    [FonteDados] NVARCHAR(200) NULL,
    [ResponsavelColeta] UNIQUEIDENTIFIER NULL,
    [Observacoes] NVARCHAR(1000) NULL,
    [ArquivoEvidencia] NVARCHAR(500) NULL,

    CONSTRAINT [PK_SLA_Medicao_Negocio] PRIMARY KEY CLUSTERED ([Id] ASC),
    CONSTRAINT [FK_SLA_Medicao_Negocio_KPI] FOREIGN KEY ([KPIId])
        REFERENCES [dbo].[SLA_Servico_KPI] ([Id]),
    CONSTRAINT [FK_SLA_Medicao_Negocio_Responsavel] FOREIGN KEY ([ResponsavelColeta])
        REFERENCES [dbo].[Usuario] ([Id]),
    CONSTRAINT [CK_SLA_Medicao_Negocio_StatusKPI] CHECK ([StatusKPI] IN (1, 2, 3, 4))
);

CREATE NONCLUSTERED INDEX [IX_SLA_Medicao_Negocio_KPIId] ON [dbo].[SLA_Medicao_Negocio] ([KPIId]);
CREATE NONCLUSTERED INDEX [IX_SLA_Medicao_Negocio_Competencia] ON [dbo].[SLA_Medicao_Negocio] ([Competencia]);
CREATE NONCLUSTERED INDEX [IX_SLA_Medicao_Negocio_DataMedicao] ON [dbo].[SLA_Medicao_Negocio] ([DataMedicao] DESC);

-- =============================================
-- 5. TABELA: BSC_Perspectiva
-- =============================================
CREATE TABLE [dbo].[BSC_Perspectiva] (
    [Id] UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    [ConglomeradoId] UNIQUEIDENTIFIER NOT NULL,
    [Nome] NVARCHAR(100) NOT NULL,
    [Descricao] NVARCHAR(500) NULL,
    [Icone] NVARCHAR(50) NULL,
    [Cor] NVARCHAR(20) NULL,
    [Ordem] INT NOT NULL,
    [Ativo] BIT NOT NULL DEFAULT 1,
    [CreatedAt] DATETIME2(7) NOT NULL DEFAULT GETUTCDATE(),
    [CreatedBy] UNIQUEIDENTIFIER NOT NULL,
    [ModifiedAt] DATETIME2(7) NULL,
    [ModifiedBy] UNIQUEIDENTIFIER NULL,

    CONSTRAINT [PK_BSC_Perspectiva] PRIMARY KEY CLUSTERED ([Id] ASC),
    CONSTRAINT [FK_BSC_Perspectiva_Conglomerado] FOREIGN KEY ([ConglomeradoId])
        REFERENCES [dbo].[Conglomerado] ([Id]),
    CONSTRAINT [UQ_BSC_Perspectiva_Nome] UNIQUE ([ConglomeradoId], [Nome]),
    CONSTRAINT [CK_BSC_Perspectiva_Ordem] CHECK ([Ordem] >= 1 AND [Ordem] <= 10)
);

CREATE NONCLUSTERED INDEX [IX_BSC_Perspectiva_ConglomeradoId] ON [dbo].[BSC_Perspectiva] ([ConglomeradoId]);
CREATE NONCLUSTERED INDEX [IX_BSC_Perspectiva_Ordem] ON [dbo].[BSC_Perspectiva] ([Ordem]);

-- =============================================
-- 6. TABELA: BSC_Objetivo
-- =============================================
CREATE TABLE [dbo].[BSC_Objetivo] (
    [Id] UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    [PerspectivaId] UNIQUEIDENTIFIER NOT NULL,
    [Nome] NVARCHAR(200) NOT NULL,
    [Descricao] NVARCHAR(1000) NULL,
    [Peso] DECIMAL(5,2) NOT NULL DEFAULT 0.25,
    [ResponsavelId] UNIQUEIDENTIFIER NULL,
    [DataInicio] DATETIME2(7) NOT NULL,
    [DataConclusao] DATETIME2(7) NULL,
    [StatusObjetivo] INT NOT NULL DEFAULT 1, -- 1=Em Andamento, 2=Concluído, 3=Cancelado
    [Ativo] BIT NOT NULL DEFAULT 1,
    [CreatedAt] DATETIME2(7) NOT NULL DEFAULT GETUTCDATE(),
    [CreatedBy] UNIQUEIDENTIFIER NOT NULL,
    [ModifiedAt] DATETIME2(7) NULL,
    [ModifiedBy] UNIQUEIDENTIFIER NULL,

    CONSTRAINT [PK_BSC_Objetivo] PRIMARY KEY CLUSTERED ([Id] ASC),
    CONSTRAINT [FK_BSC_Objetivo_Perspectiva] FOREIGN KEY ([PerspectivaId])
        REFERENCES [dbo].[BSC_Perspectiva] ([Id]) ON DELETE CASCADE,
    CONSTRAINT [FK_BSC_Objetivo_Responsavel] FOREIGN KEY ([ResponsavelId])
        REFERENCES [dbo].[Usuario] ([Id]),
    CONSTRAINT [CK_BSC_Objetivo_Peso] CHECK ([Peso] >= 0 AND [Peso] <= 1),
    CONSTRAINT [CK_BSC_Objetivo_StatusObjetivo] CHECK ([StatusObjetivo] IN (1, 2, 3))
);

CREATE NONCLUSTERED INDEX [IX_BSC_Objetivo_PerspectivaId] ON [dbo].[BSC_Objetivo] ([PerspectivaId]);
CREATE NONCLUSTERED INDEX [IX_BSC_Objetivo_ResponsavelId] ON [dbo].[BSC_Objetivo] ([ResponsavelId]);

-- =============================================
-- 7. TABELA: BSC_Indicador
-- =============================================
CREATE TABLE [dbo].[BSC_Indicador] (
    [Id] UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    [ObjetivoId] UNIQUEIDENTIFIER NOT NULL,
    [Nome] NVARCHAR(200) NOT NULL,
    [Descricao] NVARCHAR(1000) NULL,
    [Formula] NVARCHAR(500) NULL,
    [Meta] DECIMAL(18,4) NOT NULL,
    [UnidadeMedida] NVARCHAR(20) NOT NULL,
    [Frequencia] INT NOT NULL DEFAULT 3, -- 1=Diária, 2=Semanal, 3=Mensal, 4=Trimestral
    [TipoIndicador] INT NOT NULL DEFAULT 1, -- 1=Lagging, 2=Leading
    [Polaridade] INT NOT NULL DEFAULT 1, -- 1=Maior Melhor, 2=Menor Melhor
    [Ativo] BIT NOT NULL DEFAULT 1,
    [CreatedAt] DATETIME2(7) NOT NULL DEFAULT GETUTCDATE(),
    [CreatedBy] UNIQUEIDENTIFIER NOT NULL,
    [ModifiedAt] DATETIME2(7) NULL,
    [ModifiedBy] UNIQUEIDENTIFIER NULL,

    CONSTRAINT [PK_BSC_Indicador] PRIMARY KEY CLUSTERED ([Id] ASC),
    CONSTRAINT [FK_BSC_Indicador_Objetivo] FOREIGN KEY ([ObjetivoId])
        REFERENCES [dbo].[BSC_Objetivo] ([Id]) ON DELETE CASCADE,
    CONSTRAINT [CK_BSC_Indicador_Frequencia] CHECK ([Frequencia] IN (1, 2, 3, 4)),
    CONSTRAINT [CK_BSC_Indicador_TipoIndicador] CHECK ([TipoIndicador] IN (1, 2)),
    CONSTRAINT [CK_BSC_Indicador_Polaridade] CHECK ([Polaridade] IN (1, 2))
);

CREATE NONCLUSTERED INDEX [IX_BSC_Indicador_ObjetivoId] ON [dbo].[BSC_Indicador] ([ObjetivoId]);

-- =============================================
-- 8. TABELA: BSC_Medicao
-- =============================================
CREATE TABLE [dbo].[BSC_Medicao] (
    [Id] UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    [IndicadorId] UNIQUEIDENTIFIER NOT NULL,
    [Competencia] NVARCHAR(7) NOT NULL,
    [ValorMedido] DECIMAL(18,4) NOT NULL,
    [ValorMeta] DECIMAL(18,4) NOT NULL,
    [PercentualAlcance] AS (CASE WHEN [ValorMeta] = 0 THEN 0 ELSE ([ValorMedido] / [ValorMeta]) * 100 END) PERSISTED,
    [TendenciaTrimestre] INT NULL, -- 1=Crescente, 2=Estável, 3=Decrescente
    [StatusSemaforo] INT NOT NULL, -- 1=Verde (≥100%), 2=Amarelo (80-99%), 3=Vermelho (<80%)
    [Observacoes] NVARCHAR(1000) NULL,
    [Ativo] BIT NOT NULL DEFAULT 1,
    [CreatedAt] DATETIME2(7) NOT NULL DEFAULT GETUTCDATE(),
    [CreatedBy] UNIQUEIDENTIFIER NOT NULL,

    CONSTRAINT [PK_BSC_Medicao] PRIMARY KEY CLUSTERED ([Id] ASC),
    CONSTRAINT [FK_BSC_Medicao_Indicador] FOREIGN KEY ([IndicadorId])
        REFERENCES [dbo].[BSC_Indicador] ([Id]) ON DELETE CASCADE,
    CONSTRAINT [UQ_BSC_Medicao_Competencia] UNIQUE ([IndicadorId], [Competencia]),
    CONSTRAINT [CK_BSC_Medicao_TendenciaTrimestre] CHECK ([TendenciaTrimestre] IS NULL OR [TendenciaTrimestre] IN (1, 2, 3)),
    CONSTRAINT [CK_BSC_Medicao_StatusSemaforo] CHECK ([StatusSemaforo] IN (1, 2, 3))
);

CREATE NONCLUSTERED INDEX [IX_BSC_Medicao_IndicadorId] ON [dbo].[BSC_Medicao] ([IndicadorId]);
CREATE NONCLUSTERED INDEX [IX_BSC_Medicao_Competencia] ON [dbo].[BSC_Medicao] ([Competencia]);

-- =============================================
-- 9. TABELA: KPI_Biblioteca
-- =============================================
CREATE TABLE [dbo].[KPI_Biblioteca] (
    [Id] UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    [ConglomeradoId] UNIQUEIDENTIFIER NOT NULL,
    [Categoria] INT NOT NULL, -- 1=Financeiro, 2=Cliente, 3=Operacional, 4=RH, 5=TI
    [CodigoKPI] NVARCHAR(20) NOT NULL,
    [NomeKPI] NVARCHAR(100) NOT NULL,
    [DescricaoKPI] NVARCHAR(1000) NULL,
    [FormulaCalculo] NVARCHAR(500) NULL,
    [UnidadeMedida] NVARCHAR(20) NOT NULL,
    [FonteDados] NVARCHAR(200) NULL,
    [FrequenciaColeta] INT NOT NULL DEFAULT 3,
    [MetaSugerida] NVARCHAR(50) NULL,
    [BenchmarkIndustria] NVARCHAR(200) NULL,
    [Tags] NVARCHAR(MAX) NULL, -- JSON
    [Ativo] BIT NOT NULL DEFAULT 1,
    [CreatedAt] DATETIME2(7) NOT NULL DEFAULT GETUTCDATE(),
    [CreatedBy] UNIQUEIDENTIFIER NOT NULL,
    [ModifiedAt] DATETIME2(7) NULL,
    [ModifiedBy] UNIQUEIDENTIFIER NULL,

    CONSTRAINT [PK_KPI_Biblioteca] PRIMARY KEY CLUSTERED ([Id] ASC),
    CONSTRAINT [FK_KPI_Biblioteca_Conglomerado] FOREIGN KEY ([ConglomeradoId])
        REFERENCES [dbo].[Conglomerado] ([Id]),
    CONSTRAINT [UQ_KPI_Biblioteca_Codigo] UNIQUE ([ConglomeradoId], [CodigoKPI]),
    CONSTRAINT [CK_KPI_Biblioteca_Categoria] CHECK ([Categoria] BETWEEN 1 AND 5),
    CONSTRAINT [CK_KPI_Biblioteca_Tags_JSON] CHECK ([Tags] IS NULL OR ISJSON([Tags]) = 1)
);

CREATE NONCLUSTERED INDEX [IX_KPI_Biblioteca_ConglomeradoId] ON [dbo].[KPI_Biblioteca] ([ConglomeradoId]);
CREATE NONCLUSTERED INDEX [IX_KPI_Biblioteca_Categoria] ON [dbo].[KPI_Biblioteca] ([Categoria]);
CREATE NONCLUSTERED INDEX [IX_KPI_Biblioteca_CodigoKPI] ON [dbo].[KPI_Biblioteca] ([CodigoKPI]);

-- =============================================
-- 10. TABELA: SLA_Pesquisa_Config
-- =============================================
CREATE TABLE [dbo].[SLA_Pesquisa_Config] (
    [Id] UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    [ConglomeradoId] UNIQUEIDENTIFIER NOT NULL,
    [SLAServicoId] UNIQUEIDENTIFIER NULL,
    [TipoPesquisa] INT NOT NULL, -- 1=CSAT, 2=NPS, 3=FCR, 4=Custom
    [Plataforma] INT NOT NULL, -- 1=SurveyMonkey, 2=Typeform, 3=Google Forms, 4=Qualtrics
    [URLPesquisa] NVARCHAR(500) NOT NULL,
    [APIKeyEncriptada] NVARCHAR(MAX) NOT NULL, -- AES-256
    [MapeamentoCampos] NVARCHAR(MAX) NULL, -- JSON
    [IntervaloImportacao] INT NOT NULL DEFAULT 24, -- Horas
    [UltimaImportacao] DATETIME2(7) NULL,
    [ProximaImportacao] DATETIME2(7) NULL,
    [StatusIntegracao] INT NOT NULL DEFAULT 1, -- 1=Ativo, 2=Erro, 3=Desabilitado
    [MensagemErro] NVARCHAR(500) NULL,
    [Ativo] BIT NOT NULL DEFAULT 1,
    [CreatedAt] DATETIME2(7) NOT NULL DEFAULT GETUTCDATE(),
    [CreatedBy] UNIQUEIDENTIFIER NOT NULL,
    [ModifiedAt] DATETIME2(7) NULL,
    [ModifiedBy] UNIQUEIDENTIFIER NULL,

    CONSTRAINT [PK_SLA_Pesquisa_Config] PRIMARY KEY CLUSTERED ([Id] ASC),
    CONSTRAINT [FK_SLA_Pesquisa_Config_Conglomerado] FOREIGN KEY ([ConglomeradoId])
        REFERENCES [dbo].[Conglomerado] ([Id]),
    CONSTRAINT [FK_SLA_Pesquisa_Config_SLA] FOREIGN KEY ([SLAServicoId])
        REFERENCES [dbo].[SLA_Servico] ([Id]),
    CONSTRAINT [CK_SLA_Pesquisa_Config_TipoPesquisa] CHECK ([TipoPesquisa] IN (1, 2, 3, 4)),
    CONSTRAINT [CK_SLA_Pesquisa_Config_Plataforma] CHECK ([Plataforma] IN (1, 2, 3, 4)),
    CONSTRAINT [CK_SLA_Pesquisa_Config_IntervaloImportacao] CHECK ([IntervaloImportacao] >= 1 AND [IntervaloImportacao] <= 168),
    CONSTRAINT [CK_SLA_Pesquisa_Config_StatusIntegracao] CHECK ([StatusIntegracao] IN (1, 2, 3)),
    CONSTRAINT [CK_SLA_Pesquisa_Config_APIKey_JSON] CHECK (ISJSON([APIKeyEncriptada]) = 1),
    CONSTRAINT [CK_SLA_Pesquisa_Config_MapeamentoCampos_JSON] CHECK ([MapeamentoCampos] IS NULL OR ISJSON([MapeamentoCampos]) = 1)
);

CREATE NONCLUSTERED INDEX [IX_SLA_Pesquisa_Config_ConglomeradoId] ON [dbo].[SLA_Pesquisa_Config] ([ConglomeradoId]);
CREATE NONCLUSTERED INDEX [IX_SLA_Pesquisa_Config_SLAServicoId] ON [dbo].[SLA_Pesquisa_Config] ([SLAServicoId]);
CREATE NONCLUSTERED INDEX [IX_SLA_Pesquisa_Config_ProximaImportacao] ON [dbo].[SLA_Pesquisa_Config] ([ProximaImportacao]) WHERE [Ativo] = 1;

-- =============================================
-- 11. TABELA: SLA_Dashboard_Exec
-- =============================================
CREATE TABLE [dbo].[SLA_Dashboard_Exec] (
    [Id] UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    [ConglomeradoId] UNIQUEIDENTIFIER NOT NULL,
    [UsuarioId] UNIQUEIDENTIFIER NULL,
    [NomeDashboard] NVARCHAR(100) NOT NULL,
    [TipoDashboard] INT NOT NULL, -- 1=BSC, 2=KPIs, 3=Quality, 4=Customizado
    [ConfigBSC] NVARCHAR(MAX) NULL, -- JSON
    [ConfigKPIs] NVARCHAR(MAX) NULL, -- JSON
    [LayoutWidgets] NVARCHAR(MAX) NOT NULL, -- JSON
    [Filtros] NVARCHAR(MAX) NULL, -- JSON
    [Publico] BIT NOT NULL DEFAULT 0,
    [RefreshInterval] INT NOT NULL DEFAULT 60, -- Segundos
    [Ativo] BIT NOT NULL DEFAULT 1,
    [CreatedAt] DATETIME2(7) NOT NULL DEFAULT GETUTCDATE(),
    [CreatedBy] UNIQUEIDENTIFIER NOT NULL,
    [ModifiedAt] DATETIME2(7) NULL,
    [ModifiedBy] UNIQUEIDENTIFIER NULL,

    CONSTRAINT [PK_SLA_Dashboard_Exec] PRIMARY KEY CLUSTERED ([Id] ASC),
    CONSTRAINT [FK_SLA_Dashboard_Exec_Conglomerado] FOREIGN KEY ([ConglomeradoId])
        REFERENCES [dbo].[Conglomerado] ([Id]),
    CONSTRAINT [FK_SLA_Dashboard_Exec_Usuario] FOREIGN KEY ([UsuarioId])
        REFERENCES [dbo].[Usuario] ([Id]),
    CONSTRAINT [CK_SLA_Dashboard_Exec_TipoDashboard] CHECK ([TipoDashboard] IN (1, 2, 3, 4)),
    CONSTRAINT [CK_SLA_Dashboard_Exec_RefreshInterval] CHECK ([RefreshInterval] >= 30 AND [RefreshInterval] <= 600),
    CONSTRAINT [CK_SLA_Dashboard_Exec_ConfigBSC_JSON] CHECK ([ConfigBSC] IS NULL OR ISJSON([ConfigBSC]) = 1),
    CONSTRAINT [CK_SLA_Dashboard_Exec_ConfigKPIs_JSON] CHECK ([ConfigKPIs] IS NULL OR ISJSON([ConfigKPIs]) = 1),
    CONSTRAINT [CK_SLA_Dashboard_Exec_LayoutWidgets_JSON] CHECK (ISJSON([LayoutWidgets]) = 1),
    CONSTRAINT [CK_SLA_Dashboard_Exec_Filtros_JSON] CHECK ([Filtros] IS NULL OR ISJSON([Filtros]) = 1)
);

CREATE NONCLUSTERED INDEX [IX_SLA_Dashboard_Exec_ConglomeradoId] ON [dbo].[SLA_Dashboard_Exec] ([ConglomeradoId]);
CREATE NONCLUSTERED INDEX [IX_SLA_Dashboard_Exec_UsuarioId] ON [dbo].[SLA_Dashboard_Exec] ([UsuarioId]);
CREATE NONCLUSTERED INDEX [IX_SLA_Dashboard_Exec_Publico] ON [dbo].[SLA_Dashboard_Exec] ([Publico]) WHERE [Publico] = 1;

-- =============================================
-- 12. TABELA: SLA_Relatorio_Quality
-- =============================================
CREATE TABLE [dbo].[SLA_Relatorio_Quality] (
    [Id] UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    [SLAServicoId] UNIQUEIDENTIFIER NOT NULL,
    [Competencia] NVARCHAR(7) NOT NULL,
    [TipoRelatorio] INT NOT NULL, -- 1=Mensal, 2=Trimestral, 3=Anual
    [ScoreGeral] DECIMAL(5,2) NOT NULL,
    [ScoreCSAT] DECIMAL(5,2) NULL,
    [ScoreNPS] DECIMAL(5,2) NULL,
    [ScoreFCR] DECIMAL(5,2) NULL,
    [ScoreCompliance] DECIMAL(5,2) NULL,
    [TotalRespostas] INT NULL,
    [DataGeracao] DATETIME2(7) NOT NULL DEFAULT GETUTCDATE(),
    [ArquivoPDF] NVARCHAR(500) NULL,
    [Observacoes] NVARCHAR(1000) NULL,

    CONSTRAINT [PK_SLA_Relatorio_Quality] PRIMARY KEY CLUSTERED ([Id] ASC),
    CONSTRAINT [FK_SLA_Relatorio_Quality_SLA] FOREIGN KEY ([SLAServicoId])
        REFERENCES [dbo].[SLA_Servico] ([Id]),
    CONSTRAINT [UQ_SLA_Relatorio_Quality_Competencia] UNIQUE ([SLAServicoId], [Competencia], [TipoRelatorio]),
    CONSTRAINT [CK_SLA_Relatorio_Quality_TipoRelatorio] CHECK ([TipoRelatorio] IN (1, 2, 3)),
    CONSTRAINT [CK_SLA_Relatorio_Quality_ScoreGeral] CHECK ([ScoreGeral] >= 0 AND [ScoreGeral] <= 100)
);

CREATE NONCLUSTERED INDEX [IX_SLA_Relatorio_Quality_SLAServicoId] ON [dbo].[SLA_Relatorio_Quality] ([SLAServicoId]);
CREATE NONCLUSTERED INDEX [IX_SLA_Relatorio_Quality_Competencia] ON [dbo].[SLA_Relatorio_Quality] ([Competencia]);
CREATE NONCLUSTERED INDEX [IX_SLA_Relatorio_Quality_DataGeracao] ON [dbo].[SLA_Relatorio_Quality] ([DataGeracao] DESC);

-- =============================================
-- FIM DO SCRIPT DDL
-- =============================================
```

---

## 5. RELACIONAMENTOS

### 5.1. Hierarquia Multi-Tenancy

```
Conglomerado (1) ──► (N) Empresa (1) ──► (N) Cliente ──► (N) SLA_Servico
```

### 5.2. Relacionamentos Principais

| Tabela Origem               | Tabela Destino              | Tipo  | Cardinalidade |
|-----------------------------|-----------------------------|-------|---------------|
| SLA_Servico                 | Contrato                    | FK    | N:1           |
| SLA_Servico_KPI             | SLA_Servico                 | FK    | N:1           |
| SLA_Servico_Meta            | SLA_Servico                 | FK    | N:1           |
| SLA_Medicao_Negocio         | SLA_Servico_KPI             | FK    | N:1           |
| BSC_Perspectiva             | Conglomerado                | FK    | N:1           |
| BSC_Objetivo                | BSC_Perspectiva             | FK    | N:1           |
| BSC_Indicador               | BSC_Objetivo                | FK    | N:1           |
| BSC_Medicao                 | BSC_Indicador               | FK    | N:1           |
| KPI_Biblioteca              | Conglomerado                | FK    | N:1           |
| SLA_Pesquisa_Config         | SLA_Servico                 | FK    | N:1           |
| SLA_Dashboard_Exec          | Usuario                     | FK    | N:1           |
| SLA_Relatorio_Quality       | SLA_Servico                 | FK    | N:1           |

---

## 6. ÍNDICES E OTIMIZAÇÕES

- **45+ índices não-clusterizados** para otimizar queries
- **Computed columns:** PercentualAlcance em Meta e Medicao
- **Unique constraints:** Evitar duplicatas em Competência
- **Índices filtrados:** Filtrar registros ativos

---

## 7. REGRAS DE NEGÓCIO MAPEADAS

| Regra de Negócio                         | Implementação no Banco                                |
|------------------------------------------|-------------------------------------------------------|
| RN001: KPIs de negócio (CSAT, NPS, FCR) | Enum TipoKPI (1-8)                                    |
| RN002: Balanced Scorecard 4 perspectivas | Tabelas BSC_Perspectiva, BSC_Objetivo, BSC_Indicador  |
| RN003: Metas mensais/trimestrais         | Tabela SLA_Servico_Meta                               |
| RN004: Biblioteca de KPIs (100+)         | Tabela KPI_Biblioteca                                 |
| RN005: Integração com pesquisas          | Tabela SLA_Pesquisa_Config                            |
| RN006: Dashboards executivos             | Tabela SLA_Dashboard_Exec                             |
| RN007: Relatórios de qualidade           | Tabela SLA_Relatorio_Quality                          |

---

## 8. INTEGRAÇÕES OBRIGATÓRIAS

### 8.1. Central de Funcionalidades

- `GES.SLA_SERVICOS.LISTAR`
- `GES.SLA_SERVICOS.CRIAR`
- `GES.SLA_SERVICOS.BSC_DASHBOARD`
- `GES.SLA_SERVICOS.RELATORIOS`

### 8.2. Internacionalização (i18n)

```
sla_servicos.titulo = "Gestão de SLA Serviços"
sla_servicos.kpi.csat = "Customer Satisfaction (CSAT)"
sla_servicos.kpi.nps = "Net Promoter Score (NPS)"
sla_servicos.bsc.perspectivas.financeira = "Perspectiva Financeira"
```

### 8.3. Auditoria e RBAC

- Operações: CREATE, UPDATE, DELETE, APPROVE
- Permissões específicas por tipo de dashboard

---

## 9. CONSIDERAÇÕES DE PERFORMANCE

- **Agregação automática:** Job noturno para consolidar métricas
- **Particionamento:** Por competência (ano-mês)
- **Cache de dashboards:** Redis para dashboards executivos
- **Índices otimizados:** 45+ índices

---

## 10. PRÓXIMOS PASSOS

1. Implementação Backend (.NET 10) com Clean Architecture
2. Implementação Frontend (Angular 19) com dashboards BSC
3. Integração com plataformas de pesquisa (SurveyMonkey, Typeform)
4. Geração automática de relatórios PDF

---

**FIM DO DOCUMENTO MD-RF029**

**Versão:** 1.0
**Última Atualização:** 2025-12-18
**Total de Linhas:** 475
**Total de Tabelas:** 12 principais + 2 auxiliares = 14 tabelas
**Total de Índices:** 45+
**Status:** ✅ COMPLETO - Pronto para Implementação
