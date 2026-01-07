# RL-RF101: Referência ao Legado - Dashboards Executivos Operacionais

**Versão**: 1.0 | **Data**: 2025-12-31
**RF Moderno**: RF101 v2.0 | **Sistema Legado**: VB.NET + ASP.NET Web Forms + Crystal Reports

---

## 1. VISÃO GERAL DO LEGADO

### 1.1 Sistema Origem

**Nome**: Sistema IControlIT v1.0 (Legado)
**Tecnologia**: ASP.NET Web Forms + VB.NET + SQL Server 2008 R2 + Crystal Reports
**Arquitetura**: Monolítica WebForms com camada de apresentação e dados acopladas
**Período Operacional**: 2010 - 2025 (15 anos)
**Banco de Dados**: IC1_Producao (SQL Server, sem multi-tenancy explícito)

### 1.2 Contexto Funcional

No sistema legado, dashboards executivos eram gerados através de Crystal Reports estáticos acessados via páginas ASPX. Consolidação de dados ocorria via Stored Procedures SSIS executadas por SQL Agent jobs noturnos. Não havia forecast, heatmaps ou exportação PowerPoint. Visualizações eram limitadas a gráficos estáticos gerados pelo Crystal Reports em PDF.

### 1.3 Problemas Identificados

- **Performance**: Queries OLTP contra tabelas transacionais causavam lentidão extrema (>30s para carregar dashboard)
- **Escalabilidade**: Crystal Reports não escala para múltiplos usuários simultâneos (crash com >5 acessos concorrentes)
- **Multi-tenancy**: Sem isolamento, filtros manuais WHERE ClienteId permitiam vazamento de dados entre clientes
- **Auditoria**: Sem rastreamento de quem acessou quais dados executivos
- **Modernização**: Impossível integrar ML, forecast ou visualizações interativas D3.js/Highcharts
- **Exportação**: PDF gerado via Crystal Reports com gráficos de baixa qualidade, sem PowerPoint
- **Manutenção**: Stored Procedures complexas (>1000 linhas) impossíveis de manter, documentação inexistente

---

## 2. ARQUITETURA LEGADA

### 2.1 Camadas da Aplicação

```
[Navegador] → [IIS 7.5 + ASP.NET WebForms] → [VB.NET Code-Behind] → [SQL Server 2008 R2]
                           ↓
                  [Crystal Reports SDK]
                           ↓
                  [Stored Procedures SSIS]
                           ↓
                  [SQL Agent Jobs (noturno)]
```

### 2.2 Fluxo de Dados

1. **Consolidação Noturna**: SQL Agent dispara SSIS package às 02:00 AM
2. **SSIS Package**: Executa stored procedures complexas agregando dados em tabelas temporárias
3. **Acesso Usuário**: Executivo acessa Dashboard.aspx
4. **Crystal Reports**: Carrega dados de tabelas temporárias via ODBC
5. **Renderização**: Gráfico gerado server-side como imagem estática
6. **Exportação**: PDF gerado via Crystal Reports SDK (lento, 10-30 segundos)

### 2.3 Principais Componentes

| Componente | Tecnologia | Responsabilidade |
|------------|------------|------------------|
| Dashboard.aspx | ASP.NET WebForms | Tela principal de visualização |
| Dashboard.aspx.vb | VB.NET | Code-behind com lógica de negócio |
| RelatorioCustos.rpt | Crystal Reports | Template de relatório de custos |
| WSDashboard.asmx | Web Service VB.NET | API SOAP para integração externa |
| pa_DashboardCustos | Stored Procedure | Consolidação de custos por período |
| pa_DashboardSLA | Stored Procedure | Consolidação de SLA vs meta |
| pa_ConsolidacaoDiaria | Stored Procedure | Job noturno de agregação |

---

## 3. TELAS LEGADAS (ASPX)

### 3.1 Dashboard.aspx

**Localização**: `D:\IC2\ic1_legado\IControlIT\Relatorios\Dashboard.aspx`

**Responsabilidade**: Tela principal de visualização de dashboards executivos com filtros de período e tipo.

**Campos**:
- **ddlTipoDashboard** (DropDownList): Opções: "Custos", "SLA", "Compliance" (sem "C-Level" ou "Performance")
- **txtDataInicio** (TextBox): Data inicial do período
- **txtDataFim** (TextBox): Data final do período
- **btnGerar** (Button): Dispara geração do relatório Crystal Reports
- **btnExportar** (Button): Exporta para PDF via Crystal Reports

**Comportamentos Implícitos**:
- Período default: Mês atual (primeiro dia até dia atual)
- Filtro ClienteId aplicado manualmente no code-behind (inseguro)
- Crystal Report carregado dinamicamente baseado em ddlTipoDashboard
- Timeout de 60 segundos configurado (insuficiente para volumes grandes)
- Sem auditoria: nenhum log de quem acessou ou quando
- Sem validação de permissão: qualquer usuário logado podia acessar

### 3.2 RelatorioExec.aspx

**Localização**: `D:\IC2\ic1_legado\IControlIT\Relatorios\RelatorioExec.aspx`

**Responsabilidade**: Geração de relatório executivo consolidado mensal (PDF).

**Campos**:
- **ddlMes** (DropDownList): Mês (1-12)
- **ddlAno** (DropDownList): Ano (2010-2025)
- **chkIncluirGraficos** (CheckBox): Incluir gráficos no PDF
- **btnGerar** (Button): Dispara geração

**Comportamentos Implícitos**:
- Geração lenta (30-60 segundos para PDF de 20 páginas)
- Gráficos de baixa resolução (72 dpi, pixelizados quando impressos)
- Arquivo temporário salvo em `D:\Temp\Relatorios\` (vulnerabilidade: arquivos não deletados)
- Sem verificação de espaço em disco (falha se disco cheio)
- PDF não expirava: acumulava 100s de arquivos temporários

### 3.3 GraficosCustos.aspx

**Localização**: `D:\IC2\ic1_legado\IControlIT\Relatorios\GraficosCustos.aspx`

**Responsabilidade**: Visualização de gráficos de custos por filial/centro de custo.

**Campos**:
- **ddlFilial** (DropDownList): Seleção de filial (sem "Todas")
- **ddlCentroCusto** (DropDownList): Seleção de centro de custo
- **rblTipoGrafico** (RadioButtonList): "Barra", "Linha", "Pizza"
- **imgGrafico** (Image): Gráfico renderizado server-side como PNG

**Comportamentos Implícitos**:
- Gráfico gerado via System.Drawing.Graphics (baixa qualidade)
- Salvo como PNG temporário em `D:\Temp\Graficos\` (não deletado)
- Sem interatividade: usuário não pode fazer drill-down
- Cores hardcoded: verde/vermelho sem escala de intensidade
- Sem suporte a heatmap ou matriz bidimensional

### 3.4 SLAStatus.aspx

**Localização**: `D:\IC2\ic1_legado\IControlIT\SLA\SLAStatus.aspx`

**Responsabilidade**: Visualização de status de SLA contratual vs realizado.

**Campos**:
- **ddlContrato** (DropDownList): Seleção de contrato
- **gvSLA** (GridView): Grid com colunas: Mês, Meta, Realizado, Status
- **lblStatusGeral** (Label): Texto "CONFORME" ou "NÃO CONFORME"

**Comportamentos Implícitos**:
- Status calculado client-side via JavaScript (inseguro)
- Grid sem paginação: todas as linhas carregadas de uma vez (lento para contratos com 12+ meses)
- Cores de status aplicadas via RowDataBound (não WCAG AA compliant)
- Sem trending: apenas valores absolutos, sem gráfico de evolução
- Sem alertas automáticos: executivo precisa revisar manualmente

---

## 4. WEBSERVICES LEGADOS (ASMX)

### 4.1 WSDashboard.asmx

**Localização**: `D:\IC2\ic1_legado\IControlIT\WebServices\WSDashboard.asmx`
**Linguagem**: VB.NET
**Protocolo**: SOAP 1.1

**Métodos**:

#### GetDashboardCLevel()
**Descrição**: Retorna 4 KPIs principais (não existia no legado, descartado)
**Parâmetros**: Nenhum
**Retorno**: Não implementado

#### GetCustosConsolidados(DataInicio As Date, DataFim As Date, ClienteId As Integer)
**Descrição**: Retorna custos consolidados por período
**Parâmetros**:
- DataInicio: Data inicial
- DataFim: Data final
- ClienteId: ID do cliente (sem validação)

**Retorno**:
```vb
Public Class CustoConsolidado
    Public Property FilialId As Integer
    Public Property FilialNome As String
    Public Property ValorTotal As Decimal
    Public Property Quantidade As Integer
End Class
```

**Problemas**:
- ClienteId não validado com token do usuário logado (vazamento de dados)
- Query sem índices: SELECT direto em tabelas transacionais (lento)
- Sem cache: toda requisição bate no banco
- Timeout hardcoded 30s (insuficiente para volumes grandes)

#### GetTrendingCustos(ContratoId As Integer, Meses As Integer)
**Descrição**: Retorna trending de custos para N meses
**Parâmetros**:
- ContratoId: ID do contrato
- Meses: Quantidade de meses (hardcoded max 12)

**Retorno**:
```vb
Public Class TrendingData
    Public Property Mes As String  ' Formato "YYYY-MM"
    Public Property Valor As Decimal
End Class
```

**Problemas**:
- Sem regressão linear: apenas dados brutos
- Sem variação percentual: cliente calcula manualmente
- Sem granularidade diária/semanal: apenas mensal
- Retorna array simples sem metadados (ValorMedio, ValorMax, etc.)

#### ExportarRelatorioPDF(TipoDashboard As String, Periodo As String)
**Descrição**: Gera PDF de dashboard executivo
**Parâmetros**:
- TipoDashboard: "Custos", "SLA", "Compliance"
- Periodo: "YYYY-MM"

**Retorno**: Byte() (array de bytes do PDF)

**Problemas**:
- Geração síncrona: request bloqueia até conclusão (30-60s)
- Arquivo temporário não deletado após download
- Sem URL de download: retorna array de bytes (payload grande)
- Sem auditoria: não registra quem exportou

---

## 5. STORED PROCEDURES LEGADAS

### 5.1 pa_DashboardCustos

**Localização**: `Database\dbo\pa_DashboardCustos.sql`
**Complexidade**: Alta (1200 linhas)

**Descrição**: Consolida custos por contrato, filial e centro de custo para período especificado.

**Parâmetros**:
- @ClienteId INT
- @DataInicio DATE
- @DataFim DATE

**Lógica**:
1. Criar tabela temporária #Custos
2. INSERT em #Custos agregando tblFatura + tblConsumo + tblChavado
3. JOIN com tblFilial, tblCentroCusto, tblContrato
4. GROUP BY FilialId, CentroCustoId, ContratoId
5. Calcular totais e médias
6. Retornar SELECT final

**Problemas**:
- Lógica duplicada: mesma agregação feita em 3 procedures diferentes
- Sem índices: queries sem NOLOCK causam bloqueios
- Tabela temporária sem índice: performance ruim para volumes grandes (>100k registros)
- Sem paginação: retorna TODOS os registros de uma vez
- Hardcoded ISNULL defaults: valores 0 quando deveria ser NULL

### 5.2 pa_DashboardSLA

**Localização**: `Database\dbo\pa_DashboardSLA.sql`
**Complexidade**: Média (600 linhas)

**Descrição**: Consolida SLA contratual vs performance realizada por contrato.

**Parâmetros**:
- @ContratoId INT
- @Mes INT
- @Ano INT

**Lógica**:
1. SELECT meta contratual de tblContratoSLA
2. COUNT chamados atendidos dentro SLA de tblAtendimento WHERE DentroSLA = 1
3. COUNT total esperado de tblExpectativaDemanda
4. Calcular percentual: (Atendido / Esperado) * 100
5. Classificar status: >= 95% "CONFORME", < 95% "NÃO CONFORME"

**Problemas**:
- Threshold hardcoded (95%): deveria vir de tblContratoSLA.MetaPercentual
- Sem trending: apenas mês atual, sem histórico comparativo
- Sem alertas: apenas retorna dados, lógica de alerta no client
- Campo DentroSLA calculado errado: não considera feriados e fins de semana

### 5.3 pa_ConsolidacaoDiaria

**Localização**: `Database\dbo\pa_ConsolidacaoDiaria.sql`
**Complexidade**: Muito Alta (2500 linhas)
**Execução**: SQL Agent Job diário às 02:00 AM

**Descrição**: Job master que executa consolidação diária de todos os dashboards.

**Lógica**:
1. EXEC pa_ConsolidaCustosDiarios (insere em tblConsolidadoCustos)
2. EXEC pa_ConsolidaSLADiarios (insere em tblConsolidadoSLA)
3. EXEC pa_ConsolidaComplianceDiarios (insere em tblConsolidadoCompliance)
4. EXEC pa_LimpaTemporariosDashboard (deleta arquivos >7 dias)
5. Registrar sucesso/falha em tblLogConsolidacao

**Problemas**:
- Execução sequencial: 2h30min de duração total (deveria ser paralelo)
- Falha de uma procedure cancela todo job (sem retry)
- Sem idempotência: re-executar duplica registros
- Limpeza de temporários falha silenciosamente (disco cheio não alertado)
- Log em tblLogConsolidacao sem retenção: cresce infinitamente

---

## 6. TABELAS LEGADAS

### 6.1 tblConsolidadoCustos

**Finalidade**: Armazenar custos agregados para consultas rápidas (equivalente a FatoDashboard_Custos no moderno).

**DDL Legado**:
```sql
CREATE TABLE [dbo].[tblConsolidadoCustos](
    [Id] [int] IDENTITY(1,1) PRIMARY KEY,
    [ClienteId] [int] NOT NULL,  -- SEM FK, apenas int
    [ContratoId] [int] NULL,
    [FilialId] [int] NULL,
    [DataConsolidacao] [date] NOT NULL,
    [ValorTotal] [decimal](18,2) NULL,
    -- SEM campos de auditoria (criado_por, criado_em)
    -- SEM soft delete
    -- SEM índices compostos
)
```

**Problemas**:
- Sem FK: integridade referencial não garantida
- Sem audit trail: não sabe quando/quem consolidou
- Sem índice em (ClienteId, DataConsolidacao): queries lentas
- Campo ContratoId nullable permite registros órfãos
- Sem campo Mes/Ano separados: queries com MONTH(DataConsolidacao) não usam índice

### 6.2 tblConsolidadoSLA

**Finalidade**: Armazenar SLA consolidado (equivalente a FatoDashboard_SLA no moderno).

**DDL Legado**:
```sql
CREATE TABLE [dbo].[tblConsolidadoSLA](
    [Id] [int] IDENTITY(1,1) PRIMARY KEY,
    [ContratoId] [int] NOT NULL,  -- SEM FK
    [Mes] [int] NOT NULL,
    [Ano] [int] NOT NULL,
    [MetaPercentual] [decimal](5,2) NULL,  -- DEVERIA ser NOT NULL
    [PercentualAtendimento] [decimal](5,2) NULL,
    [Status] [varchar](20) NULL  -- "CONFORME", "NAO CONFORME" (sem enum)
)
```

**Problemas**:
- Sem ClienteId: impossível isolar por cliente (multi-tenancy quebrado)
- Sem índice composto (ContratoId, Ano, Mes): queries lentas
- Status como string livre: permite valores inválidos ("conforme", "Confome", etc.)
- MetaPercentual nullable: registros órfãos sem meta definida

### 6.3 tblLogConsolidacao

**Finalidade**: Log de execuções do job de consolidação diária.

**DDL Legado**:
```sql
CREATE TABLE [dbo].[tblLogConsolidacao](
    [Id] [int] IDENTITY(1,1) PRIMARY KEY,
    [DataExecucao] [datetime] NOT NULL DEFAULT GETDATE(),
    [TipoDado] [varchar](50) NULL,  -- "CUSTOS", "SLA", "COMPLIANCE"
    [Sucesso] [bit] NULL,  -- DEVERIA ser NOT NULL
    [MensagemErro] [nvarchar](max) NULL
    -- SEM campo RegistrosProcessados
    -- SEM campo ClienteId (log compartilhado entre clientes)
    -- SEM retenção: cresce indefinidamente
)
```

**Problemas**:
- Sem retenção: tabela cresce infinitamente (>5M registros após 15 anos)
- Sem ClienteId: não sabe qual cliente teve falha
- Campo Sucesso nullable: permite NULL (deveria ser 0 ou 1)
- Sem RegistrosProcessados: não sabe se processamento foi completo
- Sem índice em DataExecucao: queries de auditoria lentas

---

## 7. DECISÕES DE MODERNIZAÇÃO

### 7.1 Crystal Reports → D3.js + Highcharts + Power BI Embedded

**Decisão**: Substituir Crystal Reports por bibliotecas JavaScript modernas.

**Motivo**:
- Crystal Reports não escala para múltiplos usuários simultâneos
- Impossível integrar interatividade (drill-down, zoom, filtros dinâmicos)
- Licenciamento caro (SAP Crystal Reports Server)
- Gráficos de baixa qualidade e não responsivos

**Impacto**: Alto
- Requer reescrita completa de visualizações
- Necessidade de treinamento em D3.js/Highcharts
- Migração de templates .rpt para componentes Angular

**Mitigação**:
- Power BI Embedded opcional para clientes que preferem Microsoft stack
- Componentes compartilhados com RF099 (Dashboards Genéricos) reduzem retrabalho

### 7.2 Stored Procedures SSIS → Hangfire Jobs + Entity Framework

**Decisão**: Migrar consolidação de Stored Procedures SSIS para Hangfire jobs com Entity Framework LINQ.

**Motivo**:
- Stored procedures de 1000+ linhas impossíveis de manter
- SSIS requer SQL Server Integration Services (licença separada)
- Lógica de negócio presa no banco (dificulta testes unitários)
- Jobs SQL Agent não têm retry automático ou monitoramento moderno

**Impacto**: Muito Alto
- Requer refatoração completa de lógica de consolidação
- Mudança de paradigma: de SQL procedural para C# LINQ
- Necessidade de validação extensiva (comparar resultados legado vs moderno)

**Mitigação**:
- Hangfire Dashboard fornece monitoramento visual em tempo real
- Testes automatizados comparam output legado vs moderno
- Rollback rápido: manter stored procedures por 6 meses em paralelo

### 7.3 Sem Forecast → Azure ML SDK + ML.NET

**Decisão**: Adicionar previsão de custos usando Machine Learning (não existia no legado).

**Motivo**:
- Executivos solicitam forecast para planejamento orçamentário
- Forecast manual via Excel propenso a erros
- Competidores oferecem forecast como diferencial

**Impacto**: Alto (nova funcionalidade)
- Requer expertise em Machine Learning (ARIMA, Regressão Linear)
- Necessidade de histórico mínimo de 12 meses
- Validação estatística (R² >= 0.85) para confiabilidade

**Mitigação**:
- ML.NET fornece APIs simplificadas para forecast
- Azure ML opcional para clientes com Azure subscription
- Forecast marcado como "beta" inicialmente

### 7.4 PDF via Crystal → PowerPoint via Open XML SDK

**Decisão**: Substituir exportação PDF (Crystal Reports) por PowerPoint (.pptx) via Open XML SDK.

**Motivo**:
- Executivos compartilham insights em reuniões (PowerPoint mais comum)
- Crystal Reports PDF de baixa qualidade (72 dpi, não editável)
- PowerPoint permite edição após geração (adicionar comentários, slides)

**Impacto**: Médio
- Requer aprendizado de Open XML SDK (complexo)
- Renderização de gráficos D3.js/Highcharts como PNG via Puppeteer

**Mitigação**:
- Templates PowerPoint pré-definidos reduzem complexidade
- PDF mantido como opção secundária (usando iText)
- Exportação assíncrona evita timeout

### 7.5 Multi-Tenancy Manual → ClienteId Obrigatório

**Decisão**: Enforçar multi-tenancy via ClienteId obrigatório em todas as queries.

**Motivo**:
- Legado filtrava ClienteId manualmente no code-behind (inseguro)
- Vulnerabilidade: trocar ClienteId na query string vazava dados de outros clientes
- Conformidade LGPD exige isolamento garantido

**Impacto**: Crítico
- Requer auditoria de TODAS as queries para garantir filtro ClienteId
- Entity Framework Global Query Filters automatizam isolamento
- Testes de segurança obrigatórios (penetration testing)

**Mitigação**:
- Global Query Filters em EF Core aplicam filtro automaticamente
- Validação automatizada: script verifica queries sem ClienteId
- Code review obrigatório para queries raw SQL

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|--------|------|-----------|-------|
| 1.0 | 2025-12-31 | Documento inicial de referência ao legado (7 seções obrigatórias) | Claude Code |

---

**FIM DO DOCUMENTO RL-RF101**
