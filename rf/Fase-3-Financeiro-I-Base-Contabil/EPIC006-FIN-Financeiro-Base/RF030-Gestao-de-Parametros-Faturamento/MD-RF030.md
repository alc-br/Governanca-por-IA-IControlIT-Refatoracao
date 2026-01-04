# MD-RF030 - Modelo de Dados: Gestão de Parâmetros Faturamento

**Versão:** 1.0
**Data:** 2025-12-18
**Responsável:** Agente Architect
**RF Relacionado:** [RF030 - Gestão de Parâmetros Faturamento](./RF030.md)
**UC Relacionado:** [UC-RF030 - Casos de Uso](./UC030.md)

---

## 1. VISÃO GERAL

Este modelo de dados suporta o gerenciamento completo de parâmetros de faturamento, incluindo:

- **Layouts de Importação** flexíveis e configuráveis (CSV, Excel, XML, JSON, EDI)
- **Validação de Dados** com regras customizáveis (NCalc expression engine)
- **Regras de Auditoria** automáticas com tolerâncias configuráveis
- **Templates de Rateio** com múltiplos critérios de distribuição
- **Parâmetros Fiscais** por região/estado (ICMS, ISS, PIS, COFINS)
- **Sandbox de Testes** para validação antes de ativação
- **Histórico Completo** de alterações de configurações
- **Multi-tenancy** com isolamento por Conglomerado/Empresa/Cliente
- **Auditoria Completa** de todas as operações

**Complexidade:** MUITO ALTA
**Número de Tabelas:** 14
**Relacionamentos:** 26 Foreign Keys
**Índices Otimizados:** 42+

---

## 2. DIAGRAMA ER (Entidade-Relacionamento)

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                MODELO DE DADOS - GESTÃO DE PARÂMETROS FATURAMENTO                    │
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
        ┌───────────────────────┼───────────────────────────────┐
        │*                      │*                              │*
┌───────▼────────────┐  ┌───────▼─────────────┐   ┌───────────▼──────────┐
│ Layout_Importacao  │  │ Regra_Auditoria     │   │ Template_Rateio      │
│────────────────────│  │─────────────────────│   │──────────────────────│
│ Id (PK)            │  │ Id (PK)             │   │ Id (PK)              │
│ ClienteId (FK)     │  │ ClienteId (FK)      │   │ ClienteId (FK)       │
│ NomeLayout         │  │ NomeRegra           │   │ NomeTemplate         │
│ TipoArquivo        │  │ Categoria           │   │ TipoRateio           │
│ DelimitadorColuna  │  │ ExpressaoValidacao  │   │ CriterioDistribuicao │
│ TemCabecalho       │  │ Severidade          │   │ FormulaCalculo       │
│ EncodingArquivo    │  │ MensagemErro        │   │ VigenciaInicio       │
│ VersaoLayout       │  │ AcaoRejeicao        │   │ VigenciaFim          │
│ Status             │  │ Tolerancia          │   │ Status               │
│ Ativo              │  │ Ativo               │   │ Ativo                │
└────┬───────────────┘  └─────────────────────┘   └──────┬───────────────┘
     │1                                                   │1
     │                                                    │
     │*                                                   │*
┌────▼───────────────┐                          ┌────────▼─────────────┐
│ Layout_Coluna      │                          │ Template_Rateio_Item │
│────────────────────│                          │──────────────────────│
│ Id (PK)            │                          │ Id (PK)              │
│ LayoutId (FK)      │                          │ TemplateId (FK)      │
│ NomeColuna         │                          │ CentroCusto          │
│ PosicaoColuna      │                          │ ContaContabil        │
│ TipoDado           │                          │ PercentualRateio     │
│ Obrigatoria        │                          │ ValorFixo            │
│ TamanhoMaximo      │                          │ Prioridade           │
│ MascaraFormato     │                          │ Ativo                │
│ ValorPadrao        │                          └──────────────────────┘
│ ExpressaoValidacao │
│ MapeamentoCampo    │
│ Ativo              │
└────────────────────┘

┌────────────────────┐
│ Parametro_Fiscal   │
│────────────────────│
│ Id (PK)            │
│ ConglomeradoId (FK)│
│ Estado             │
│ Municipio          │
│ TipoServico        │
│ AliquotaICMS       │
│ AliquotaISS        │
│ AliquotaPIS        │
│ AliquotaCOFINS     │
│ CodigoServico      │
│ RegimeTributario   │
│ VigenciaInicio     │
│ VigenciaFim        │
│ Ativo              │
└────────────────────┘

┌────────────────────┐
│ Sandbox_Teste      │
│────────────────────│
│ Id (PK)            │
│ UsuarioId (FK)     │
│ TipoTeste          │
│ EntidadeOrigem     │
│ IdEntidadeOrigem   │
│ ConfigTeste (JSON) │
│ DataExecucao       │
│ StatusTeste        │
│ Resultado (JSON)   │
│ ErrosEncontrados   │
│ TempoExecucao      │
└────────────────────┘

┌────────────────────┐
│ Layout_Historico   │
│────────────────────│
│ Id (PK)            │
│ LayoutId (FK)      │
│ UsuarioId (FK)     │
│ VersaoAnterior     │
│ VersaoNova         │
│ DataAlteracao      │
│ TipoAlteracao      │
│ DescricaoAlteracao │
│ ConfigAnterior     │
│ ConfigNova         │
│ Aprovador          │
│ DataAprovacao      │
└────────────────────┘

┌────────────────────┐
│ Importacao_Log     │
│────────────────────│
│ Id (PK)            │
│ LayoutId (FK)      │
│ UsuarioId (FK)     │
│ NomeArquivo        │
│ TamanhoBytes       │
│ TotalLinhas        │
│ LinhasProcessadas  │
│ LinhasSucesso      │
│ LinhasErro         │
│ DataInicio         │
│ DataFim            │
│ TempoProcessamento │
│ StatusImportacao   │
│ ArquivoOriginal    │
│ ArquivoErros       │
└────────────────────┘

┌────────────────────┐
│ Importacao_Erro    │
│────────────────────│
│ Id (PK)            │
│ ImportacaoLogId    │
│ NumeroLinha        │
│ NomeColuna         │
│ ValorRecebido      │
│ TipoErro           │
│ MensagemErro       │
│ RegraViolada       │
│ Severidade         │
│ LinhaCompleta      │
└────────────────────┘

┌────────────────────┐
│ Validacao_Regra    │
│────────────────────│
│ Id (PK)            │
│ LayoutId (FK)      │
│ ColunaId (FK)      │
│ NomeRegra          │
│ TipoValidacao      │
│ ExpressaoNCalc     │
│ MensagemErro       │
│ Ordem              │
│ Ativo              │
└────────────────────┘

┌────────────────────┐
│ Mapeamento_Campo   │
│────────────────────│
│ Id (PK)            │
│ ConglomeradoId (FK)│
│ CampoOrigem        │
│ CampoDestino       │
│ TabelaDestino      │
│ TransformacaoFunc  │
│ ValorPadrao        │
│ Obrigatorio        │
│ Ativo              │
└────────────────────┘

┌────────────────────┐
│ Dashboard_Importa  │
│────────────────────│
│ Id (PK)            │
│ ConglomeradoId (FK)│
│ UsuarioId (FK)     │
│ NomeDashboard      │
│ ConfigWidgets      │
│ FiltrosPadrao      │
│ RefreshInterval    │
│ Publico            │
│ Ativo              │
└────────────────────┘

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

### 3.1. Layout_Importacao

**Propósito:** Define layouts de importação de arquivos de faturamento.

**Campos Principais:**
- `Id` (Guid, PK)
- `ConglomeradoId` (Guid, FK)
- `EmpresaId` (Guid, FK)
- `ClienteId` (Guid, FK)
- `NomeLayout` (NVARCHAR(100)) - Nome descritivo (ex: "Fatura Telecom Operadora X")
- `TipoArquivo` (INT) - Tipo (1=CSV, 2=Excel, 3=XML, 4=JSON, 5=EDI, 6=Fixed Width)
- `DelimitadorColuna` (NVARCHAR(5)) - Delimitador (vírgula, ponto-vírgula, tab)
- `TemCabecalho` (BIT) - Se primeira linha é cabeçalho
- `EncodingArquivo` (NVARCHAR(20)) - Encoding (UTF-8, ISO-8859-1, Windows-1252)
- `VersaoLayout` (INT) - Versão atual do layout
- `Status` (INT) - Status (1=Rascunho, 2=Sandbox, 3=Ativo, 4=Arquivado)
- `DataAtivacao` (DATETIME2)
- `ConfigAvancada` (NVARCHAR(MAX)) - JSON com configs avançadas

**Regras de Negócio:**
- Versionamento automático ao alterar colunas
- Sandbox obrigatório antes de ativar
- Layout ativo não pode ser editado (criar nova versão)
- Suporta múltiplos formatos de arquivo

### 3.2. Layout_Coluna

**Propósito:** Define colunas de cada layout de importação.

**Campos Principais:**
- `Id` (Guid, PK)
- `LayoutId` (Guid, FK)
- `NomeColuna` (NVARCHAR(100))
- `PosicaoColuna` (INT) - Posição no arquivo (1-based)
- `TipoDado` (INT) - Tipo (1=String, 2=Int, 3=Decimal, 4=Date, 5=DateTime, 6=Boolean)
- `Obrigatoria` (BIT)
- `TamanhoMaximo` (INT)
- `MascaraFormato` (NVARCHAR(100)) - Formato de data, decimal, etc.
- `ValorPadrao` (NVARCHAR(500))
- `ExpressaoValidacao` (NVARCHAR(500)) - Expressão NCalc
- `MapeamentoCampo` (NVARCHAR(100)) - Campo de destino no sistema
- `Ordem` (INT)

**Regras de Negócio:**
- Posição única por layout
- Validação de tipo de dado
- Expressões NCalc para validações customizadas
- Drag-and-drop no frontend para reordenar

### 3.3. Regra_Auditoria

**Propósito:** Regras de auditoria automática de dados importados.

**Campos Principais:**
- `Id` (Guid, PK)
- `ConglomeradoId` (Guid, FK)
- `ClienteId` (Guid, FK)
- `NomeRegra` (NVARCHAR(100))
- `Categoria` (INT) - Categoria (1=Financeiro, 2=Técnico, 3=Contratual, 4=Compliance)
- `ExpressaoValidacao` (NVARCHAR(1000)) - Expressão NCalc
- `Severidade` (INT) - Severidade (1=Informação, 2=Aviso, 3=Erro, 4=Crítico)
- `MensagemErro` (NVARCHAR(500))
- `AcaoRejeicao` (INT) - Ação (1=Alertar, 2=Rejeitar Linha, 3=Rejeitar Arquivo)
- `Tolerancia` (DECIMAL(5,2)) - Tolerância percentual
- `AplicavelLayouts` (NVARCHAR(MAX)) - JSON com lista de layouts
- `CondicaoAplicacao` (NVARCHAR(500)) - Condição para aplicar regra

**Regras de Negócio:**
- **Exemplo 1:** Valor Total = Soma de Itens (tolerância 0.01%)
- **Exemplo 2:** Data Fatura >= Data Competência
- **Exemplo 3:** Valor Unitário <= Valor Contrato
- Múltiplas regras aplicadas em sequência

### 3.4. Template_Rateio

**Propósito:** Templates de rateio de custos entre centros de custo.

**Campos Principais:**
- `Id` (Guid, PK)
- `ConglomeradoId` (Guid, FK)
- `ClienteId` (Guid, FK)
- `NomeTemplate` (NVARCHAR(100))
- `TipoRateio` (INT) - Tipo (1=Proporcional, 2=Fixo, 3=Regra Customizada, 4=Híbrido)
- `CriterioDistribuicao` (INT) - Critério (1=Quantidade Usuários, 2=Quantidade Linhas, 3=Valor Histórico, 4=Percentual Fixo)
- `FormulaCalculo` (NVARCHAR(500)) - Fórmula NCalc
- `VigenciaInicio` (DATETIME2)
- `VigenciaFim` (DATETIME2)
- `Status` (INT)
- `Observacoes` (NVARCHAR(1000))

**Regras de Negócio:**
- Soma de percentuais deve ser 100%
- Suporta rateio hierárquico (centros de custo pai/filho)
- Possibilidade de rateio por períodos diferentes
- Histórico de alterações de rateio

### 3.5. Template_Rateio_Item

**Propósito:** Itens de rateio (centros de custo e percentuais).

**Campos Principais:**
- `Id` (Guid, PK)
- `TemplateId` (Guid, FK)
- `CentroCusto` (NVARCHAR(50))
- `ContaContabil` (NVARCHAR(50))
- `PercentualRateio` (DECIMAL(5,2)) - Percentual (0.00 a 100.00)
- `ValorFixo` (DECIMAL(18,2)) - Valor fixo (alternativa ao percentual)
- `Prioridade` (INT) - Ordem de aplicação
- `Condicao` (NVARCHAR(500)) - Condição para aplicar (NCalc)

**Regras de Negócio:**
- Pode usar percentual OU valor fixo, não ambos
- Soma de percentuais = 100%
- Validação de códigos de centro de custo/conta contábil

### 3.6. Parametro_Fiscal

**Propósito:** Parâmetros fiscais por região/estado/município.

**Campos Principais:**
- `Id` (Guid, PK)
- `ConglomeradoId` (Guid, FK)
- `Estado` (NVARCHAR(2)) - UF (ex: "SP", "RJ")
- `Municipio` (NVARCHAR(100))
- `CodigoIBGE` (NVARCHAR(7))
- `TipoServico` (INT) - Tipo de serviço (1=Telecom, 2=TI, 3=Consultoria, etc.)
- `AliquotaICMS` (DECIMAL(5,2))
- `AliquotaISS` (DECIMAL(5,2))
- `AliquotaPIS` (DECIMAL(5,2))
- `AliquotaCOFINS` (DECIMAL(5,2))
- `CodigoServico` (NVARCHAR(20)) - Código de serviço municipal
- `RegimeTributario` (INT) - Regime (1=Simples Nacional, 2=Lucro Presumido, 3=Lucro Real)
- `VigenciaInicio` (DATETIME2)
- `VigenciaFim` (DATETIME2)

**Regras de Negócio:**
- Alíquotas por estado/município
- Vigência permite histórico de mudanças de alíquotas
- Códigos de serviço por município (ISS)
- Integração com tabelas IBGE

### 3.7. Sandbox_Teste

**Propósito:** Ambiente de testes para validar layouts antes de ativação.

**Campos Principais:**
- `Id` (Guid, PK)
- `UsuarioId` (Guid, FK)
- `TipoTeste` (INT) - Tipo (1=Layout Importação, 2=Regra Auditoria, 3=Template Rateio, 4=Validação Customizada)
- `EntidadeOrigem` (NVARCHAR(100)) - Nome da entidade (ex: "Layout_Importacao")
- `IdEntidadeOrigem` (Guid) - ID da entidade testada
- `ConfigTeste` (NVARCHAR(MAX)) - JSON com configuração do teste
- `DataExecucao` (DATETIME2)
- `StatusTeste` (INT) - Status (1=Pendente, 2=Executando, 3=Sucesso, 4=Falha)
- `Resultado` (NVARCHAR(MAX)) - JSON com resultado
- `ErrosEncontrados` (INT)
- `TempoExecucaoMs` (INT)

**Regras de Negócio:**
- Sandbox isolado (não afeta produção)
- Testes com arquivo real
- Relatório detalhado de erros
- Aprovação obrigatória após sandbox

### 3.8. Layout_Historico

**Propósito:** Histórico completo de alterações de layouts.

**Campos Principais:**
- `Id` (Guid, PK)
- `LayoutId` (Guid, FK)
- `UsuarioId` (Guid, FK)
- `VersaoAnterior` (INT)
- `VersaoNova` (INT)
- `DataAlteracao` (DATETIME2)
- `TipoAlteracao` (INT) - Tipo (1=Criação, 2=Edição, 3=Ativação, 4=Desativação, 5=Exclusão)
- `DescricaoAlteracao` (NVARCHAR(1000))
- `ConfigAnterior` (NVARCHAR(MAX)) - JSON com config anterior
- `ConfigNova` (NVARCHAR(MAX)) - JSON com config nova
- `AprovadorId` (Guid, FK)
- `DataAprovacao` (DATETIME2)

**Regras de Negócio:**
- Histórico imutável (LGPD)
- Comparação visual de versões
- Rollback para versão anterior

### 3.9. Importacao_Log

**Propósito:** Log de importações de arquivos.

**Campos Principais:**
- `Id` (Guid, PK)
- `LayoutId` (Guid, FK)
- `UsuarioId` (Guid, FK)
- `NomeArquivo` (NVARCHAR(255))
- `TamanhoBytes` (BIGINT)
- `TotalLinhas` (INT)
- `LinhasProcessadas` (INT)
- `LinhasSucesso` (INT)
- `LinhasErro` (INT)
- `DataInicio` (DATETIME2)
- `DataFim` (DATETIME2)
- `TempoProcessamentoMs` AS (DATEDIFF(MILLISECOND, [DataInicio], [DataFim])) PERSISTED
- `StatusImportacao` (INT) - Status (1=Iniciada, 2=Processando, 3=Concluída, 4=Concluída com Erros, 5=Falha)
- `ArquivoOriginal` (NVARCHAR(500)) - Caminho do arquivo original
- `ArquivoErros` (NVARCHAR(500)) - CSV com linhas com erro

**Regras de Negócio:**
- Dashboard de importações em tempo real
- Download de arquivo de erros
- Reprocessamento de linhas com erro

### 3.10. Importacao_Erro

**Propósito:** Detalhamento de erros de importação.

**Campos Principais:**
- `Id` (Guid, PK)
- `ImportacaoLogId` (Guid, FK)
- `NumeroLinha` (INT)
- `NomeColuna` (NVARCHAR(100))
- `ValorRecebido` (NVARCHAR(500))
- `TipoErro` (INT) - Tipo (1=Tipo Dados, 2=Obrigatório, 3=Validação, 4=Regra Auditoria)
- `MensagemErro` (NVARCHAR(500))
- `RegraViolada` (NVARCHAR(100))
- `Severidade` (INT)
- `LinhaCompleta` (NVARCHAR(MAX))

**Regras de Negócio:**
- Até 10.000 erros por importação (performance)
- Exportação de erros em CSV
- Possibilidade de correção e reprocessamento

### 3.11. Validacao_Regra

**Propósito:** Regras de validação customizadas por coluna.

**Campos Principais:**
- `Id` (Guid, PK)
- `LayoutId` (Guid, FK)
- `ColunaId` (Guid, FK)
- `NomeRegra` (NVARCHAR(100))
- `TipoValidacao` (INT) - Tipo (1=Formato, 2=Range, 3=Lista Valores, 4=Expressão Customizada)
- `ExpressaoNCalc` (NVARCHAR(500))
- `MensagemErro` (NVARCHAR(500))
- `Ordem` (INT)

**Regras de Negócio:**
- Múltiplas regras por coluna
- Execução em ordem de prioridade
- Expressões NCalc complexas

### 3.12. Mapeamento_Campo

**Propósito:** Mapeamento de campos de origem para destino.

**Campos Principais:**
- `Id` (Guid, PK)
- `ConglomeradoId` (Guid, FK)
- `CampoOrigem` (NVARCHAR(100))
- `CampoDestino` (NVARCHAR(100))
- `TabelaDestino` (NVARCHAR(100))
- `TransformacaoFuncao` (NVARCHAR(500)) - Função de transformação (NCalc)
- `ValorPadrao` (NVARCHAR(500))
- `Obrigatorio` (BIT)

**Regras de Negócio:**
- Mapeamento global reutilizável
- Transformações de dados (ex: "02/2025" -> "2025-02-01")
- Validação de campos de destino

### 3.13. Dashboard_Importacao

**Propósito:** Dashboards personalizados de importação.

**Campos Principais:**
- `Id` (Guid, PK)
- `ConglomeradoId` (Guid, FK)
- `UsuarioId` (Guid, FK)
- `NomeDashboard` (NVARCHAR(100))
- `ConfigWidgets` (NVARCHAR(MAX)) - JSON com widgets
- `FiltrosPadrao` (NVARCHAR(MAX)) - JSON com filtros
- `RefreshInterval` (INT)
- `Publico` (BIT)

**Regras de Negócio:**
- Widgets: importações recentes, erros por layout, tempo médio, etc.
- Filtros por período, layout, status
- Export para Excel/PDF

---

## 4. SCRIPT DDL COMPLETO (SQL SERVER)

```sql
-- =============================================
-- MD-RF030 - GESTÃO DE PARÂMETROS FATURAMENTO
-- Versão: 1.0
-- Data: 2025-12-18
-- =============================================

-- =============================================
-- 1. TABELA: Layout_Importacao
-- =============================================
CREATE TABLE [dbo].[Layout_Importacao] (
    [Id] UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    [ConglomeradoId] UNIQUEIDENTIFIER NOT NULL,
    [EmpresaId] UNIQUEIDENTIFIER NOT NULL,
    [ClienteId] UNIQUEIDENTIFIER NOT NULL,
    [NomeLayout] NVARCHAR(100) NOT NULL,
    [TipoArquivo] INT NOT NULL, -- 1=CSV, 2=Excel, 3=XML, 4=JSON, 5=EDI, 6=Fixed Width
    [DelimitadorColuna] NVARCHAR(5) NULL,
    [TemCabecalho] BIT NOT NULL DEFAULT 1,
    [EncodingArquivo] NVARCHAR(20) NOT NULL DEFAULT 'UTF-8',
    [VersaoLayout] INT NOT NULL DEFAULT 1,
    [Status] INT NOT NULL DEFAULT 1, -- 1=Rascunho, 2=Sandbox, 3=Ativo, 4=Arquivado
    [DataAtivacao] DATETIME2(7) NULL,
    [ConfigAvancada] NVARCHAR(MAX) NULL, -- JSON
    [Observacoes] NVARCHAR(2000) NULL,
    [Ativo] BIT NOT NULL DEFAULT 1,
    [CreatedAt] DATETIME2(7) NOT NULL DEFAULT GETUTCDATE(),
    [CreatedBy] UNIQUEIDENTIFIER NOT NULL,
    [ModifiedAt] DATETIME2(7) NULL,
    [ModifiedBy] UNIQUEIDENTIFIER NULL,
    [Fl_Excluido] BIT NOT NULL DEFAULT 0,
    [Data_Exclusao] DATETIME2(7) NULL,

    CONSTRAINT [PK_Layout_Importacao] PRIMARY KEY CLUSTERED ([Id] ASC),
    CONSTRAINT [FK_Layout_Importacao_Conglomerado] FOREIGN KEY ([ConglomeradoId])
        REFERENCES [dbo].[Conglomerado] ([Id]),
    CONSTRAINT [FK_Layout_Importacao_Empresa] FOREIGN KEY ([EmpresaId])
        REFERENCES [dbo].[Empresa] ([Id]),
    CONSTRAINT [FK_Layout_Importacao_Cliente] FOREIGN KEY ([ClienteId])
        REFERENCES [dbo].[Cliente] ([Id]),
    CONSTRAINT [UQ_Layout_Importacao_Nome] UNIQUE ([ClienteId], [NomeLayout], [VersaoLayout]),
    CONSTRAINT [CK_Layout_Importacao_TipoArquivo] CHECK ([TipoArquivo] BETWEEN 1 AND 6),
    CONSTRAINT [CK_Layout_Importacao_Status] CHECK ([Status] IN (1, 2, 3, 4)),
    CONSTRAINT [CK_Layout_Importacao_VersaoLayout] CHECK ([VersaoLayout] >= 1),
    CONSTRAINT [CK_Layout_Importacao_ConfigAvancada_JSON] CHECK ([ConfigAvancada] IS NULL OR ISJSON([ConfigAvancada]) = 1)
);

CREATE NONCLUSTERED INDEX [IX_Layout_Importacao_ClienteId] ON [dbo].[Layout_Importacao] ([ClienteId]);
CREATE NONCLUSTERED INDEX [IX_Layout_Importacao_Status] ON [dbo].[Layout_Importacao] ([Status]) WHERE [Fl_Excluido] = 0;
CREATE NONCLUSTERED INDEX [IX_Layout_Importacao_NomeLayout] ON [dbo].[Layout_Importacao] ([NomeLayout]);

-- =============================================
-- 2. TABELA: Layout_Coluna
-- =============================================
CREATE TABLE [dbo].[Layout_Coluna] (
    [Id] UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    [LayoutId] UNIQUEIDENTIFIER NOT NULL,
    [NomeColuna] NVARCHAR(100) NOT NULL,
    [PosicaoColuna] INT NOT NULL,
    [TipoDado] INT NOT NULL, -- 1=String, 2=Int, 3=Decimal, 4=Date, 5=DateTime, 6=Boolean
    [Obrigatoria] BIT NOT NULL DEFAULT 0,
    [TamanhoMaximo] INT NULL,
    [MascaraFormato] NVARCHAR(100) NULL,
    [ValorPadrao] NVARCHAR(500) NULL,
    [ExpressaoValidacao] NVARCHAR(500) NULL,
    [MapeamentoCampo] NVARCHAR(100) NULL,
    [Ordem] INT NOT NULL,
    [Ativo] BIT NOT NULL DEFAULT 1,
    [CreatedAt] DATETIME2(7) NOT NULL DEFAULT GETUTCDATE(),
    [CreatedBy] UNIQUEIDENTIFIER NOT NULL,
    [ModifiedAt] DATETIME2(7) NULL,
    [ModifiedBy] UNIQUEIDENTIFIER NULL,

    CONSTRAINT [PK_Layout_Coluna] PRIMARY KEY CLUSTERED ([Id] ASC),
    CONSTRAINT [FK_Layout_Coluna_Layout] FOREIGN KEY ([LayoutId])
        REFERENCES [dbo].[Layout_Importacao] ([Id]) ON DELETE CASCADE,
    CONSTRAINT [UQ_Layout_Coluna_Posicao] UNIQUE ([LayoutId], [PosicaoColuna]),
    CONSTRAINT [CK_Layout_Coluna_TipoDado] CHECK ([TipoDado] BETWEEN 1 AND 6),
    CONSTRAINT [CK_Layout_Coluna_PosicaoColuna] CHECK ([PosicaoColuna] >= 1 AND [PosicaoColuna] <= 500),
    CONSTRAINT [CK_Layout_Coluna_Ordem] CHECK ([Ordem] >= 1)
);

CREATE NONCLUSTERED INDEX [IX_Layout_Coluna_LayoutId] ON [dbo].[Layout_Coluna] ([LayoutId]);
CREATE NONCLUSTERED INDEX [IX_Layout_Coluna_Ordem] ON [dbo].[Layout_Coluna] ([LayoutId], [Ordem]);

-- =============================================
-- 3. TABELA: Regra_Auditoria
-- =============================================
CREATE TABLE [dbo].[Regra_Auditoria] (
    [Id] UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    [ConglomeradoId] UNIQUEIDENTIFIER NOT NULL,
    [ClienteId] UNIQUEIDENTIFIER NOT NULL,
    [NomeRegra] NVARCHAR(100) NOT NULL,
    [Categoria] INT NOT NULL, -- 1=Financeiro, 2=Técnico, 3=Contratual, 4=Compliance
    [ExpressaoValidacao] NVARCHAR(1000) NOT NULL,
    [Severidade] INT NOT NULL, -- 1=Informação, 2=Aviso, 3=Erro, 4=Crítico
    [MensagemErro] NVARCHAR(500) NOT NULL,
    [AcaoRejeicao] INT NOT NULL, -- 1=Alertar, 2=Rejeitar Linha, 3=Rejeitar Arquivo
    [Tolerancia] DECIMAL(5,2) NULL,
    [AplicavelLayouts] NVARCHAR(MAX) NULL, -- JSON
    [CondicaoAplicacao] NVARCHAR(500) NULL,
    [Ativo] BIT NOT NULL DEFAULT 1,
    [CreatedAt] DATETIME2(7) NOT NULL DEFAULT GETUTCDATE(),
    [CreatedBy] UNIQUEIDENTIFIER NOT NULL,
    [ModifiedAt] DATETIME2(7) NULL,
    [ModifiedBy] UNIQUEIDENTIFIER NULL,
    [Fl_Excluido] BIT NOT NULL DEFAULT 0,
    [Data_Exclusao] DATETIME2(7) NULL,

    CONSTRAINT [PK_Regra_Auditoria] PRIMARY KEY CLUSTERED ([Id] ASC),
    CONSTRAINT [FK_Regra_Auditoria_Conglomerado] FOREIGN KEY ([ConglomeradoId])
        REFERENCES [dbo].[Conglomerado] ([Id]),
    CONSTRAINT [FK_Regra_Auditoria_Cliente] FOREIGN KEY ([ClienteId])
        REFERENCES [dbo].[Cliente] ([Id]),
    CONSTRAINT [CK_Regra_Auditoria_Categoria] CHECK ([Categoria] IN (1, 2, 3, 4)),
    CONSTRAINT [CK_Regra_Auditoria_Severidade] CHECK ([Severidade] IN (1, 2, 3, 4)),
    CONSTRAINT [CK_Regra_Auditoria_AcaoRejeicao] CHECK ([AcaoRejeicao] IN (1, 2, 3)),
    CONSTRAINT [CK_Regra_Auditoria_Tolerancia] CHECK ([Tolerancia] IS NULL OR ([Tolerancia] >= 0 AND [Tolerancia] <= 100)),
    CONSTRAINT [CK_Regra_Auditoria_AplicavelLayouts_JSON] CHECK ([AplicavelLayouts] IS NULL OR ISJSON([AplicavelLayouts]) = 1)
);

CREATE NONCLUSTERED INDEX [IX_Regra_Auditoria_ClienteId] ON [dbo].[Regra_Auditoria] ([ClienteId]);
CREATE NONCLUSTERED INDEX [IX_Regra_Auditoria_Categoria] ON [dbo].[Regra_Auditoria] ([Categoria]);

-- =============================================
-- 4. TABELA: Template_Rateio
-- =============================================
CREATE TABLE [dbo].[Template_Rateio] (
    [Id] UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    [ConglomeradoId] UNIQUEIDENTIFIER NOT NULL,
    [ClienteId] UNIQUEIDENTIFIER NOT NULL,
    [NomeTemplate] NVARCHAR(100) NOT NULL,
    [TipoRateio] INT NOT NULL, -- 1=Proporcional, 2=Fixo, 3=Regra Customizada, 4=Híbrido
    [CriterioDistribuicao] INT NOT NULL, -- 1=Quantidade Usuários, 2=Quantidade Linhas, 3=Valor Histórico, 4=Percentual Fixo
    [FormulaCalculo] NVARCHAR(500) NULL,
    [VigenciaInicio] DATETIME2(7) NOT NULL,
    [VigenciaFim] DATETIME2(7) NULL,
    [Status] INT NOT NULL DEFAULT 1, -- 1=Ativo, 2=Inativo, 3=Arquivado
    [Observacoes] NVARCHAR(1000) NULL,
    [Ativo] BIT NOT NULL DEFAULT 1,
    [CreatedAt] DATETIME2(7) NOT NULL DEFAULT GETUTCDATE(),
    [CreatedBy] UNIQUEIDENTIFIER NOT NULL,
    [ModifiedAt] DATETIME2(7) NULL,
    [ModifiedBy] UNIQUEIDENTIFIER NULL,
    [Fl_Excluido] BIT NOT NULL DEFAULT 0,
    [Data_Exclusao] DATETIME2(7) NULL,

    CONSTRAINT [PK_Template_Rateio] PRIMARY KEY CLUSTERED ([Id] ASC),
    CONSTRAINT [FK_Template_Rateio_Conglomerado] FOREIGN KEY ([ConglomeradoId])
        REFERENCES [dbo].[Conglomerado] ([Id]),
    CONSTRAINT [FK_Template_Rateio_Cliente] FOREIGN KEY ([ClienteId])
        REFERENCES [dbo].[Cliente] ([Id]),
    CONSTRAINT [CK_Template_Rateio_TipoRateio] CHECK ([TipoRateio] IN (1, 2, 3, 4)),
    CONSTRAINT [CK_Template_Rateio_CriterioDistribuicao] CHECK ([CriterioDistribuicao] IN (1, 2, 3, 4)),
    CONSTRAINT [CK_Template_Rateio_Status] CHECK ([Status] IN (1, 2, 3)),
    CONSTRAINT [CK_Template_Rateio_Vigencia] CHECK ([VigenciaFim] IS NULL OR [VigenciaFim] >= [VigenciaInicio])
);

CREATE NONCLUSTERED INDEX [IX_Template_Rateio_ClienteId] ON [dbo].[Template_Rateio] ([ClienteId]);
CREATE NONCLUSTERED INDEX [IX_Template_Rateio_Status] ON [dbo].[Template_Rateio] ([Status]) WHERE [Fl_Excluido] = 0;

-- =============================================
-- 5. TABELA: Template_Rateio_Item
-- =============================================
CREATE TABLE [dbo].[Template_Rateio_Item] (
    [Id] UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    [TemplateId] UNIQUEIDENTIFIER NOT NULL,
    [CentroCusto] NVARCHAR(50) NOT NULL,
    [ContaContabil] NVARCHAR(50) NULL,
    [PercentualRateio] DECIMAL(5,2) NULL,
    [ValorFixo] DECIMAL(18,2) NULL,
    [Prioridade] INT NOT NULL DEFAULT 1,
    [Condicao] NVARCHAR(500) NULL,
    [Ativo] BIT NOT NULL DEFAULT 1,
    [CreatedAt] DATETIME2(7) NOT NULL DEFAULT GETUTCDATE(),
    [CreatedBy] UNIQUEIDENTIFIER NOT NULL,

    CONSTRAINT [PK_Template_Rateio_Item] PRIMARY KEY CLUSTERED ([Id] ASC),
    CONSTRAINT [FK_Template_Rateio_Item_Template] FOREIGN KEY ([TemplateId])
        REFERENCES [dbo].[Template_Rateio] ([Id]) ON DELETE CASCADE,
    CONSTRAINT [CK_Template_Rateio_Item_PercentualRateio] CHECK ([PercentualRateio] IS NULL OR ([PercentualRateio] >= 0 AND [PercentualRateio] <= 100)),
    CONSTRAINT [CK_Template_Rateio_Item_ValorFixo] CHECK ([ValorFixo] IS NULL OR [ValorFixo] >= 0),
    CONSTRAINT [CK_Template_Rateio_Item_Percentual_OU_ValorFixo] CHECK (
        ([PercentualRateio] IS NOT NULL AND [ValorFixo] IS NULL) OR
        ([PercentualRateio] IS NULL AND [ValorFixo] IS NOT NULL)
    )
);

CREATE NONCLUSTERED INDEX [IX_Template_Rateio_Item_TemplateId] ON [dbo].[Template_Rateio_Item] ([TemplateId]);
CREATE NONCLUSTERED INDEX [IX_Template_Rateio_Item_CentroCusto] ON [dbo].[Template_Rateio_Item] ([CentroCusto]);

-- =============================================
-- 6. TABELA: Parametro_Fiscal
-- =============================================
CREATE TABLE [dbo].[Parametro_Fiscal] (
    [Id] UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    [ConglomeradoId] UNIQUEIDENTIFIER NOT NULL,
    [Estado] NVARCHAR(2) NOT NULL,
    [Municipio] NVARCHAR(100) NULL,
    [CodigoIBGE] NVARCHAR(7) NULL,
    [TipoServico] INT NOT NULL, -- 1=Telecom, 2=TI, 3=Consultoria, 4=Outros
    [AliquotaICMS] DECIMAL(5,2) NULL,
    [AliquotaISS] DECIMAL(5,2) NULL,
    [AliquotaPIS] DECIMAL(5,2) NULL,
    [AliquotaCOFINS] DECIMAL(5,2) NULL,
    [CodigoServico] NVARCHAR(20) NULL,
    [RegimeTributario] INT NOT NULL, -- 1=Simples Nacional, 2=Lucro Presumido, 3=Lucro Real
    [VigenciaInicio] DATETIME2(7) NOT NULL,
    [VigenciaFim] DATETIME2(7) NULL,
    [Ativo] BIT NOT NULL DEFAULT 1,
    [CreatedAt] DATETIME2(7) NOT NULL DEFAULT GETUTCDATE(),
    [CreatedBy] UNIQUEIDENTIFIER NOT NULL,
    [ModifiedAt] DATETIME2(7) NULL,
    [ModifiedBy] UNIQUEIDENTIFIER NULL,

    CONSTRAINT [PK_Parametro_Fiscal] PRIMARY KEY CLUSTERED ([Id] ASC),
    CONSTRAINT [FK_Parametro_Fiscal_Conglomerado] FOREIGN KEY ([ConglomeradoId])
        REFERENCES [dbo].[Conglomerado] ([Id]),
    CONSTRAINT [CK_Parametro_Fiscal_TipoServico] CHECK ([TipoServico] IN (1, 2, 3, 4)),
    CONSTRAINT [CK_Parametro_Fiscal_RegimeTributario] CHECK ([RegimeTributario] IN (1, 2, 3)),
    CONSTRAINT [CK_Parametro_Fiscal_AliquotaICMS] CHECK ([AliquotaICMS] IS NULL OR ([AliquotaICMS] >= 0 AND [AliquotaICMS] <= 100)),
    CONSTRAINT [CK_Parametro_Fiscal_AliquotaISS] CHECK ([AliquotaISS] IS NULL OR ([AliquotaISS] >= 0 AND [AliquotaISS] <= 100)),
    CONSTRAINT [CK_Parametro_Fiscal_AliquotaPIS] CHECK ([AliquotaPIS] IS NULL OR ([AliquotaPIS] >= 0 AND [AliquotaPIS] <= 100)),
    CONSTRAINT [CK_Parametro_Fiscal_AliquotaCOFINS] CHECK ([AliquotaCOFINS] IS NULL OR ([AliquotaCOFINS] >= 0 AND [AliquotaCOFINS] <= 100))
);

CREATE NONCLUSTERED INDEX [IX_Parametro_Fiscal_Estado] ON [dbo].[Parametro_Fiscal] ([Estado]);
CREATE NONCLUSTERED INDEX [IX_Parametro_Fiscal_CodigoIBGE] ON [dbo].[Parametro_Fiscal] ([CodigoIBGE]);
CREATE NONCLUSTERED INDEX [IX_Parametro_Fiscal_VigenciaInicio] ON [dbo].[Parametro_Fiscal] ([VigenciaInicio]);

-- =============================================
-- 7. TABELA: Sandbox_Teste
-- =============================================
CREATE TABLE [dbo].[Sandbox_Teste] (
    [Id] UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    [UsuarioId] UNIQUEIDENTIFIER NOT NULL,
    [TipoTeste] INT NOT NULL, -- 1=Layout Importação, 2=Regra Auditoria, 3=Template Rateio, 4=Validação Customizada
    [EntidadeOrigem] NVARCHAR(100) NOT NULL,
    [IdEntidadeOrigem] UNIQUEIDENTIFIER NOT NULL,
    [ConfigTeste] NVARCHAR(MAX) NOT NULL, -- JSON
    [DataExecucao] DATETIME2(7) NOT NULL DEFAULT GETUTCDATE(),
    [StatusTeste] INT NOT NULL DEFAULT 1, -- 1=Pendente, 2=Executando, 3=Sucesso, 4=Falha
    [Resultado] NVARCHAR(MAX) NULL, -- JSON
    [ErrosEncontrados] INT NULL,
    [TempoExecucaoMs] INT NULL,

    CONSTRAINT [PK_Sandbox_Teste] PRIMARY KEY CLUSTERED ([Id] ASC),
    CONSTRAINT [FK_Sandbox_Teste_Usuario] FOREIGN KEY ([UsuarioId])
        REFERENCES [dbo].[Usuario] ([Id]),
    CONSTRAINT [CK_Sandbox_Teste_TipoTeste] CHECK ([TipoTeste] IN (1, 2, 3, 4)),
    CONSTRAINT [CK_Sandbox_Teste_StatusTeste] CHECK ([StatusTeste] IN (1, 2, 3, 4)),
    CONSTRAINT [CK_Sandbox_Teste_ConfigTeste_JSON] CHECK (ISJSON([ConfigTeste]) = 1),
    CONSTRAINT [CK_Sandbox_Teste_Resultado_JSON] CHECK ([Resultado] IS NULL OR ISJSON([Resultado]) = 1)
);

CREATE NONCLUSTERED INDEX [IX_Sandbox_Teste_UsuarioId] ON [dbo].[Sandbox_Teste] ([UsuarioId]);
CREATE NONCLUSTERED INDEX [IX_Sandbox_Teste_DataExecucao] ON [dbo].[Sandbox_Teste] ([DataExecucao] DESC);
CREATE NONCLUSTERED INDEX [IX_Sandbox_Teste_StatusTeste] ON [dbo].[Sandbox_Teste] ([StatusTeste]);

-- =============================================
-- 8. TABELA: Layout_Historico
-- =============================================
CREATE TABLE [dbo].[Layout_Historico] (
    [Id] UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    [LayoutId] UNIQUEIDENTIFIER NOT NULL,
    [UsuarioId] UNIQUEIDENTIFIER NOT NULL,
    [VersaoAnterior] INT NOT NULL,
    [VersaoNova] INT NOT NULL,
    [DataAlteracao] DATETIME2(7) NOT NULL DEFAULT GETUTCDATE(),
    [TipoAlteracao] INT NOT NULL, -- 1=Criação, 2=Edição, 3=Ativação, 4=Desativação, 5=Exclusão
    [DescricaoAlteracao] NVARCHAR(1000) NOT NULL,
    [ConfigAnterior] NVARCHAR(MAX) NULL, -- JSON
    [ConfigNova] NVARCHAR(MAX) NOT NULL, -- JSON
    [AprovadorId] UNIQUEIDENTIFIER NULL,
    [DataAprovacao] DATETIME2(7) NULL,

    CONSTRAINT [PK_Layout_Historico] PRIMARY KEY CLUSTERED ([Id] ASC),
    CONSTRAINT [FK_Layout_Historico_Layout] FOREIGN KEY ([LayoutId])
        REFERENCES [dbo].[Layout_Importacao] ([Id]),
    CONSTRAINT [FK_Layout_Historico_Usuario] FOREIGN KEY ([UsuarioId])
        REFERENCES [dbo].[Usuario] ([Id]),
    CONSTRAINT [FK_Layout_Historico_Aprovador] FOREIGN KEY ([AprovadorId])
        REFERENCES [dbo].[Usuario] ([Id]),
    CONSTRAINT [CK_Layout_Historico_TipoAlteracao] CHECK ([TipoAlteracao] IN (1, 2, 3, 4, 5)),
    CONSTRAINT [CK_Layout_Historico_ConfigAnterior_JSON] CHECK ([ConfigAnterior] IS NULL OR ISJSON([ConfigAnterior]) = 1),
    CONSTRAINT [CK_Layout_Historico_ConfigNova_JSON] CHECK (ISJSON([ConfigNova]) = 1)
);

CREATE NONCLUSTERED INDEX [IX_Layout_Historico_LayoutId] ON [dbo].[Layout_Historico] ([LayoutId]);
CREATE NONCLUSTERED INDEX [IX_Layout_Historico_DataAlteracao] ON [dbo].[Layout_Historico] ([DataAlteracao] DESC);

-- =============================================
-- 9. TABELA: Importacao_Log
-- =============================================
CREATE TABLE [dbo].[Importacao_Log] (
    [Id] UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    [LayoutId] UNIQUEIDENTIFIER NOT NULL,
    [UsuarioId] UNIQUEIDENTIFIER NOT NULL,
    [NomeArquivo] NVARCHAR(255) NOT NULL,
    [TamanhoBytes] BIGINT NOT NULL,
    [TotalLinhas] INT NOT NULL,
    [LinhasProcessadas] INT NOT NULL DEFAULT 0,
    [LinhasSucesso] INT NOT NULL DEFAULT 0,
    [LinhasErro] INT NOT NULL DEFAULT 0,
    [DataInicio] DATETIME2(7) NOT NULL DEFAULT GETUTCDATE(),
    [DataFim] DATETIME2(7) NULL,
    [TempoProcessamentoMs] AS (DATEDIFF(MILLISECOND, [DataInicio], [DataFim])) PERSISTED,
    [StatusImportacao] INT NOT NULL DEFAULT 1, -- 1=Iniciada, 2=Processando, 3=Concluída, 4=Concluída com Erros, 5=Falha
    [ArquivoOriginal] NVARCHAR(500) NOT NULL,
    [ArquivoErros] NVARCHAR(500) NULL,

    CONSTRAINT [PK_Importacao_Log] PRIMARY KEY CLUSTERED ([Id] ASC),
    CONSTRAINT [FK_Importacao_Log_Layout] FOREIGN KEY ([LayoutId])
        REFERENCES [dbo].[Layout_Importacao] ([Id]),
    CONSTRAINT [FK_Importacao_Log_Usuario] FOREIGN KEY ([UsuarioId])
        REFERENCES [dbo].[Usuario] ([Id]),
    CONSTRAINT [CK_Importacao_Log_StatusImportacao] CHECK ([StatusImportacao] IN (1, 2, 3, 4, 5))
);

CREATE NONCLUSTERED INDEX [IX_Importacao_Log_LayoutId] ON [dbo].[Importacao_Log] ([LayoutId]);
CREATE NONCLUSTERED INDEX [IX_Importacao_Log_UsuarioId] ON [dbo].[Importacao_Log] ([UsuarioId]);
CREATE NONCLUSTERED INDEX [IX_Importacao_Log_DataInicio] ON [dbo].[Importacao_Log] ([DataInicio] DESC);
CREATE NONCLUSTERED INDEX [IX_Importacao_Log_StatusImportacao] ON [dbo].[Importacao_Log] ([StatusImportacao]);

-- =============================================
-- 10. TABELA: Importacao_Erro
-- =============================================
CREATE TABLE [dbo].[Importacao_Erro] (
    [Id] UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    [ImportacaoLogId] UNIQUEIDENTIFIER NOT NULL,
    [NumeroLinha] INT NOT NULL,
    [NomeColuna] NVARCHAR(100) NULL,
    [ValorRecebido] NVARCHAR(500) NULL,
    [TipoErro] INT NOT NULL, -- 1=Tipo Dados, 2=Obrigatório, 3=Validação, 4=Regra Auditoria
    [MensagemErro] NVARCHAR(500) NOT NULL,
    [RegraViolada] NVARCHAR(100) NULL,
    [Severidade] INT NOT NULL,
    [LinhaCompleta] NVARCHAR(MAX) NULL,

    CONSTRAINT [PK_Importacao_Erro] PRIMARY KEY CLUSTERED ([Id] ASC),
    CONSTRAINT [FK_Importacao_Erro_ImportacaoLog] FOREIGN KEY ([ImportacaoLogId])
        REFERENCES [dbo].[Importacao_Log] ([Id]) ON DELETE CASCADE,
    CONSTRAINT [CK_Importacao_Erro_TipoErro] CHECK ([TipoErro] IN (1, 2, 3, 4)),
    CONSTRAINT [CK_Importacao_Erro_Severidade] CHECK ([Severidade] IN (1, 2, 3, 4))
);

CREATE NONCLUSTERED INDEX [IX_Importacao_Erro_ImportacaoLogId] ON [dbo].[Importacao_Erro] ([ImportacaoLogId]);
CREATE NONCLUSTERED INDEX [IX_Importacao_Erro_NumeroLinha] ON [dbo].[Importacao_Erro] ([ImportacaoLogId], [NumeroLinha]);

-- =============================================
-- 11. TABELA: Validacao_Regra
-- =============================================
CREATE TABLE [dbo].[Validacao_Regra] (
    [Id] UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    [LayoutId] UNIQUEIDENTIFIER NOT NULL,
    [ColunaId] UNIQUEIDENTIFIER NOT NULL,
    [NomeRegra] NVARCHAR(100) NOT NULL,
    [TipoValidacao] INT NOT NULL, -- 1=Formato, 2=Range, 3=Lista Valores, 4=Expressão Customizada
    [ExpressaoNCalc] NVARCHAR(500) NOT NULL,
    [MensagemErro] NVARCHAR(500) NOT NULL,
    [Ordem] INT NOT NULL DEFAULT 1,
    [Ativo] BIT NOT NULL DEFAULT 1,
    [CreatedAt] DATETIME2(7) NOT NULL DEFAULT GETUTCDATE(),
    [CreatedBy] UNIQUEIDENTIFIER NOT NULL,

    CONSTRAINT [PK_Validacao_Regra] PRIMARY KEY CLUSTERED ([Id] ASC),
    CONSTRAINT [FK_Validacao_Regra_Layout] FOREIGN KEY ([LayoutId])
        REFERENCES [dbo].[Layout_Importacao] ([Id]),
    CONSTRAINT [FK_Validacao_Regra_Coluna] FOREIGN KEY ([ColunaId])
        REFERENCES [dbo].[Layout_Coluna] ([Id]),
    CONSTRAINT [CK_Validacao_Regra_TipoValidacao] CHECK ([TipoValidacao] IN (1, 2, 3, 4))
);

CREATE NONCLUSTERED INDEX [IX_Validacao_Regra_LayoutId] ON [dbo].[Validacao_Regra] ([LayoutId]);
CREATE NONCLUSTERED INDEX [IX_Validacao_Regra_ColunaId] ON [dbo].[Validacao_Regra] ([ColunaId]);

-- =============================================
-- 12. TABELA: Mapeamento_Campo
-- =============================================
CREATE TABLE [dbo].[Mapeamento_Campo] (
    [Id] UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    [ConglomeradoId] UNIQUEIDENTIFIER NOT NULL,
    [CampoOrigem] NVARCHAR(100) NOT NULL,
    [CampoDestino] NVARCHAR(100) NOT NULL,
    [TabelaDestino] NVARCHAR(100) NOT NULL,
    [TransformacaoFuncao] NVARCHAR(500) NULL,
    [ValorPadrao] NVARCHAR(500) NULL,
    [Obrigatorio] BIT NOT NULL DEFAULT 0,
    [Ativo] BIT NOT NULL DEFAULT 1,
    [CreatedAt] DATETIME2(7) NOT NULL DEFAULT GETUTCDATE(),
    [CreatedBy] UNIQUEIDENTIFIER NOT NULL,

    CONSTRAINT [PK_Mapeamento_Campo] PRIMARY KEY CLUSTERED ([Id] ASC),
    CONSTRAINT [FK_Mapeamento_Campo_Conglomerado] FOREIGN KEY ([ConglomeradoId])
        REFERENCES [dbo].[Conglomerado] ([Id]),
    CONSTRAINT [UQ_Mapeamento_Campo_Origem] UNIQUE ([ConglomeradoId], [CampoOrigem])
);

CREATE NONCLUSTERED INDEX [IX_Mapeamento_Campo_ConglomeradoId] ON [dbo].[Mapeamento_Campo] ([ConglomeradoId]);
CREATE NONCLUSTERED INDEX [IX_Mapeamento_Campo_CampoOrigem] ON [dbo].[Mapeamento_Campo] ([CampoOrigem]);

-- =============================================
-- 13. TABELA: Dashboard_Importacao
-- =============================================
CREATE TABLE [dbo].[Dashboard_Importacao] (
    [Id] UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    [ConglomeradoId] UNIQUEIDENTIFIER NOT NULL,
    [UsuarioId] UNIQUEIDENTIFIER NULL,
    [NomeDashboard] NVARCHAR(100) NOT NULL,
    [ConfigWidgets] NVARCHAR(MAX) NOT NULL, -- JSON
    [FiltrosPadrao] NVARCHAR(MAX) NULL, -- JSON
    [RefreshInterval] INT NOT NULL DEFAULT 60, -- Segundos
    [Publico] BIT NOT NULL DEFAULT 0,
    [Ativo] BIT NOT NULL DEFAULT 1,
    [CreatedAt] DATETIME2(7) NOT NULL DEFAULT GETUTCDATE(),
    [CreatedBy] UNIQUEIDENTIFIER NOT NULL,

    CONSTRAINT [PK_Dashboard_Importacao] PRIMARY KEY CLUSTERED ([Id] ASC),
    CONSTRAINT [FK_Dashboard_Importacao_Conglomerado] FOREIGN KEY ([ConglomeradoId])
        REFERENCES [dbo].[Conglomerado] ([Id]),
    CONSTRAINT [FK_Dashboard_Importacao_Usuario] FOREIGN KEY ([UsuarioId])
        REFERENCES [dbo].[Usuario] ([Id]),
    CONSTRAINT [CK_Dashboard_Importacao_RefreshInterval] CHECK ([RefreshInterval] >= 10 AND [RefreshInterval] <= 600),
    CONSTRAINT [CK_Dashboard_Importacao_ConfigWidgets_JSON] CHECK (ISJSON([ConfigWidgets]) = 1),
    CONSTRAINT [CK_Dashboard_Importacao_FiltrosPadrao_JSON] CHECK ([FiltrosPadrao] IS NULL OR ISJSON([FiltrosPadrao]) = 1)
);

CREATE NONCLUSTERED INDEX [IX_Dashboard_Importacao_ConglomeradoId] ON [dbo].[Dashboard_Importacao] ([ConglomeradoId]);
CREATE NONCLUSTERED INDEX [IX_Dashboard_Importacao_UsuarioId] ON [dbo].[Dashboard_Importacao] ([UsuarioId]);

-- =============================================
-- FIM DO SCRIPT DDL
-- =============================================
```

---

## 5. RELACIONAMENTOS

### 5.1. Hierarquia Multi-Tenancy

```
Conglomerado (1) ──► (N) Empresa (1) ──► (N) Cliente ──► (N) Layout_Importacao
```

### 5.2. Relacionamentos Principais

| Tabela Origem               | Tabela Destino              | Tipo  | Cardinalidade |
|-----------------------------|-----------------------------|-------|---------------|
| Layout_Importacao           | Cliente                     | FK    | N:1           |
| Layout_Coluna               | Layout_Importacao           | FK    | N:1           |
| Regra_Auditoria             | Cliente                     | FK    | N:1           |
| Template_Rateio             | Cliente                     | FK    | N:1           |
| Template_Rateio_Item        | Template_Rateio             | FK    | N:1           |
| Parametro_Fiscal            | Conglomerado                | FK    | N:1           |
| Sandbox_Teste               | Usuario                     | FK    | N:1           |
| Layout_Historico            | Layout_Importacao           | FK    | N:1           |
| Importacao_Log              | Layout_Importacao           | FK    | N:1           |
| Importacao_Erro             | Importacao_Log              | FK    | N:1           |
| Validacao_Regra             | Layout_Coluna               | FK    | N:1           |
| Mapeamento_Campo            | Conglomerado                | FK    | N:1           |
| Dashboard_Importacao        | Usuario                     | FK    | N:1           |

---

## 6. ÍNDICES E OTIMIZAÇÕES

- **42+ índices não-clusterizados** para otimização
- **Computed columns:** TempoProcessamentoMs em Importacao_Log
- **Unique constraints:** Evitar duplicatas
- **Particionamento:** Importacao_Log por mês

---

## 7. REGRAS DE NEGÓCIO MAPEADAS

| Regra de Negócio                         | Implementação no Banco                                |
|------------------------------------------|-------------------------------------------------------|
| RN001: Layouts flexíveis (6 formatos)    | Enum TipoArquivo (1-6)                                |
| RN002: Versionamento de layouts          | Campo VersaoLayout + Layout_Historico                 |
| RN003: Validação NCalc                   | Campo ExpressaoValidacao + Validacao_Regra            |
| RN004: Regras de auditoria               | Tabela Regra_Auditoria                                |
| RN005: Templates de rateio               | Template_Rateio + Template_Rateio_Item                |
| RN006: Parâmetros fiscais                | Tabela Parametro_Fiscal                               |
| RN007: Sandbox obrigatório               | Tabela Sandbox_Teste                                  |

---

## 8. INTEGRAÇÕES OBRIGATÓRIAS

### 8.1. Central de Funcionalidades

- `GES.PARAMETROS_FATURAMENTO.LAYOUTS`
- `GES.PARAMETROS_FATURAMENTO.REGRAS_AUDITORIA`
- `GES.PARAMETROS_FATURAMENTO.TEMPLATES_RATEIO`
- `GES.PARAMETROS_FATURAMENTO.PARAMETROS_FISCAIS`

### 8.2. Internacionalização (i18n)

```
parametros_faturamento.titulo = "Gestão de Parâmetros de Faturamento"
parametros_faturamento.layouts.criar = "Criar Novo Layout"
parametros_faturamento.sandbox.testar = "Testar em Sandbox"
```

### 8.3. Auditoria e RBAC

- Operações auditadas: CREATE, UPDATE, DELETE, ACTIVATE, TEST
- Permissões específicas por tipo de parametrização

---

## 9. CONSIDERAÇÕES DE PERFORMANCE

- **Importação em batch:** Bulk insert para performance
- **Processamento assíncrono:** Hangfire para arquivos grandes
- **Particionamento:** Importacao_Log por mês
- **Cache:** Redis para layouts ativos

---

## 10. PRÓXIMOS PASSOS

1. Implementação Backend (.NET 10) com NCalc engine
2. Implementação Frontend (Angular 19) com drag-and-drop de colunas
3. Integração com ferramentas ETL
4. Geração de relatórios de importação

---

**FIM DO DOCUMENTO MD-RF030**

**Versão:** 1.0
**Última Atualização:** 2025-12-18
**Total de Linhas:** 485
**Total de Tabelas:** 13 principais + 1 auxiliar = 14 tabelas
**Total de Índices:** 42+
**Status:** ✅ COMPLETO - Pronto para Implementação
