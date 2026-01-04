# RL-RF100 — Referência ao Legado

**Versão:** 1.0
**Data:** 2025-12-31
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF-100 - Dashboards e KPIs com Análise Preditiva
**Sistema Legado:** IControlIT v1 (ASP.NET Web Forms + VB.NET)
**Objetivo:** Documentar funcionalidades de análise preditiva inexistentes no legado. RF-100 é uma evolução completamente nova, sem equivalente direto no sistema antigo.

---

## 1. CONTEXTO DO LEGADO

O sistema legado IControlIT v1 **NÃO possuía funcionalidades de Machine Learning ou análise preditiva**. Dashboards existentes eram puramente históricos e descritivos:

- **Arquitetura:** Monolítica ASP.NET Web Forms (VB.NET)
- **Linguagem / Stack:** VB.NET 4.5, ASP.NET Web Forms, SQL Server 2014
- **Banco de Dados:** SQL Server 2014, multi-database (um banco por cliente)
- **Multi-tenant:** Não (cada cliente tinha banco separado)
- **Auditoria:** Parcial (apenas operações CREATE/UPDATE/DELETE em tabelas principais)
- **Configurações:** Web.config + tabelas KPI_Config
- **Análise Preditiva:** **INEXISTENTE** (apenas relatórios históricos)
- **Machine Learning:** **INEXISTENTE** (nenhum modelo ML)

### Problemas Arquiteturais Identificados

1. **Ausência Total de Forecasting**: Sistema não previvia custos futuros, apenas exibia histórico
2. **Detecção Manual de Anomalias**: Regras fixas hard-coded (ex: "se > 10000 então alerta"), sem aprendizado
3. **Sem Clustering**: Ativos/usuários não eram segmentados automaticamente
4. **Sem Churn Prediction**: Clientes em risco de cancelamento não eram identificados
5. **Análise What-If Inexistente**: Gestores não podiam simular cenários hipotéticos
6. **Relatórios Estáticos**: Crystal Reports gerados manualmente, sem interatividade

---

## 2. TELAS DO LEGADO

### Tela: RelatorioExecutivo.aspx

- **Caminho:** `D:\IC2\ic1_legado\IControlIT\RelatoriosBI\RelatorioExecutivo.aspx`
- **Responsabilidade:** Exibir relatórios estáticos de KPIs (custos mensais, SLA, contratos) em formato tabular ou gráfico simples (Crystal Reports)

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| `ddlCliente` | DropDownList | Sim | Seleção de cliente (ID_Cliente) |
| `dtInicio` | Calendar | Sim | Data início do período de análise |
| `dtFim` | Calendar | Sim | Data fim do período de análise |
| `ddlTipoRelatorio` | DropDownList | Sim | "Custos", "SLA", "Contratos", "Ativos" |
| `btnGerar` | Button | - | Trigger geração relatório |

#### Comportamentos Implícitos

- **Sem Forecasting**: Apenas dados passados eram exibidos (histórico até data atual)
- **Sem Anomaly Detection**: Usuário precisava identificar anomalias visualmente
- **Geração Síncrona**: Relatórios grandes (>10k linhas) travavam navegador (timeout 30s)
- **Exportação Manual**: PDF/Excel gerado por Crystal Reports, lento e não interativo

**DESTINO:** **SUBSTITUÍDO** - Tela substituída por dashboard Angular interativo em `/admin/dashboards-preditivos` com forecasting, anomaly detection e visualizações D3.js/Power BI Embedded

---

### Tela: DashboardKPI.aspx

- **Caminho:** `D:\IC2\ic1_legado\IControlIT\DashboardsBI\DashboardKPI.aspx`
- **Responsabilidade:** Dashboard com gráficos de KPIs (custos, SLA, ativos) usando controles Crystal Reports e Telerik Charts

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| `pnlGraficos` | Panel | - | Container de gráficos Telerik |
| `lblCustoTotal` | Label | - | Custo total (período selecionado) |
| `lblSLAMedio` | Label | - | SLA médio (%) |
| `lblAtivosTotal` | Label | - | Total de ativos cadastrados |

#### Comportamentos Implícitos

- **Gráficos Estáticos**: Telerik Charts sem drill-down ou interatividade avançada
- **Sem Confidence Bands**: Previsões futuras não existiam, apenas histórico
- **Refresh Manual**: Usuário precisava clicar "Atualizar" para ver novos dados
- **Sem Alertas Automáticos**: Anomalias não disparavam notificações

**DESTINO:** **SUBSTITUÍDO** - Dashboard substituído por componente Angular moderno com forecasting (confidence bands), anomaly detection em tempo real, clustering visualization e what-if analysis

---

### Tela: AnalisePreditiva.aspx

- **Caminho:** **NÃO EXISTE** (funcionalidade nova no RF-100)
- **Responsabilidade:** N/A (não havia análise preditiva no legado)

**DESTINO:** **NOVA FUNCIONALIDADE** - Criada do zero no RF-100. Componente Angular `/analytics/forecast-analysis` com modelos ML (Prophet, ARIMA, churn prediction, clustering)

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

| Método | Local | Responsabilidade | Observações |
|--------|-------|------------------|-------------|
| `GetRelatorioExecutivo(idCliente)` | `WSRelatorio.asmx.vb` | Retorna dados históricos de relatório | **SUBSTITUÍDO** por `GET /api/ml/dashboards/{id}` com forecasting |
| `CalculaKPI(idKPI, dtInicio, dtFim)` | `WSRelatorio.asmx.vb` | Calcula KPI baseado em fórmula fixa | **SUBSTITUÍDO** por `POST /api/ml/forecast` com modelos ML |
| `ExportarRelatorio(idRelatorio, tipo)` | `WSRelatorio.asmx.vb` | Exporta relatório para PDF/Excel | **ASSUMIDO** (migrado para `POST /api/ml/export`) |
| `DetectaAnomaliaManual(idMetrica, valor)` | **NÃO EXISTE** | N/A | **NOVA** - Substituído por `POST /api/ml/anomaly-detection` (Z-score + Isolation Forest) |

**DESTINO GERAL:** **SUBSTITUÍDOS** - Webservices VB.NET substituídos por REST API modernos (.NET 10 + Azure ML)

---

## 4. TABELAS LEGADAS

| Tabela | Finalidade | Problemas Identificados |
|--------|------------|-------------------------|
| `[dbo].[Metricas]` | Armazenar valores de métricas (custos, SLA, etc.) ao longo do tempo | ✅ **ASSUMIDA** - Migrada para `MetricDataPoint` com ClienteId (multi-tenancy) |
| `[dbo].[KPI_Config]` | Configuração de KPIs (nome, meta, fórmula) | **ASSUMIDA** - Migrada para `KpiConfiguration` com suporte a ML models |
| `[dbo].[Relatorio_Executivo]` | Histórico de relatórios gerados (PDF/Excel) | **DESCARTADA** - Não migrada (relatórios agora gerados em tempo real) |
| `[dbo].[Dashboard_Widgets]` | **NÃO EXISTE** | N/A - Widgets eram hard-coded em ASPX |

### Problemas Identificados nas Tabelas

#### `[dbo].[Metricas]`

- **Falta Foreign Key** para validar `Id_Cliente` → Migrado com FK para `Clientes` + ClienteId (GUID)
- **Sem Auditoria**: Campos `Created`, `Modified` ausentes → Adicionados na migração
- **Sem Multi-tenancy**: Clientes em bancos separados → Consolidado em banco único com ClienteId

**DESTINO:** **SUBSTITUÍDA** - Tabela redesenhada como `MetricDataPoint` com multi-tenancy, auditoria, índices para forecasting

#### `[dbo].[KPI_Config]`

- **Fórmulas Hard-coded**: Stored procedure `pa_Calcula_KPI` com lógica SQL rígida → Migrado para ML models treinados
- **Sem Versionamento**: Mudanças em configuração não auditadas → Adicionado versionamento de modelos ML

**DESTINO:** **SUBSTITUÍDA** - Tabela redesenhada como `KpiConfiguration` + `ModelMetrics` (tracking de performance de modelos)

---

## 5. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

Lista de regras que não estavam documentadas formalmente, extraídas do código VB.NET:

- **RL-RN-001**: **Detecção de Anomalia Manual** - Regra fixa: "se custo > R$10.000 então alerta". Sem aprendizado ou adaptação.
  **DESTINO:** **SUBSTITUÍDA** - Z-score dinâmico (RN-100-002) com threshold configurável

- **RL-RN-002**: **Cálculo de SLA Manual** - Stored procedure `pa_Calcula_SLA` com fórmula SQL: `AVG(tempo_resolucao)`.
  **DESTINO:** **ASSUMIDA** - Mantida, mas complementada com forecasting de SLA (RN-100-001)

- **RL-RN-003**: **Exportação Síncrona** - Crystal Reports bloqueava navegador durante geração (30s timeout).
  **DESTINO:** **SUBSTITUÍDA** - Exportação assíncrona via `POST /api/ml/export` (timeout 10s, fallback para job Hangfire)

- **RL-RN-004**: **Refresh Manual de Dashboards** - Usuário clicava "Atualizar" para ver novos dados (sem auto-refresh).
  **DESTINO:** **SUBSTITUÍDA** - Dashboard atualizado em tempo real via SignalR + cache Redis (RN-100-008)

- **RL-RN-005**: **Sem Validação de Dados Históricos** - Sistema gerava "relatórios" com 1 mês de dados (não confiável).
  **DESTINO:** **SUBSTITUÍDA** - Forecast requer mínimo 12 meses (RN-100-001)

- **RL-RN-006**: **Sem Auditoria de Relatórios** - Ninguém sabia quem gerou relatório X ou quando.
  **DESTINO:** **SUBSTITUÍDA** - Auditoria append-only de TODAS operações ML (RN-100-010)

---

## 6. GAP ANALYSIS (LEGADO x RF MODERNO)

| Item | Legado | RF-100 Moderno | Observação |
|------|--------|----------------|------------|
| **Forecasting** | ❌ Não existe | ✅ Prophet/ARIMA com 95% confiança | **GAP CRÍTICO** - Nova funcionalidade |
| **Anomaly Detection** | ⚠️ Regras fixas (se > X) | ✅ Z-score + Isolation Forest | **GAP ALTO** - Aprendizado automático |
| **Clustering** | ❌ Não existe | ✅ K-means/DBSCAN (3-10 clusters) | **GAP CRÍTICO** - Segmentação automática |
| **Churn Prediction** | ❌ Não existe | ✅ Score 0-100 (70% precisão) | **GAP CRÍTICO** - Identificação de risco |
| **What-If Analysis** | ❌ Excel manual | ✅ Simulação em tempo real (max 5 cenários) | **GAP ALTO** - Análise de cenários |
| **Multi-tenancy** | ❌ Multi-database | ✅ Single-database com ClienteId | **GAP MÉDIO** - Isolamento Row-Level |
| **Cache** | ❌ Sem cache | ✅ Redis 24h TTL | **GAP MÉDIO** - Performance |
| **Auditoria ML** | ❌ Não existe | ✅ Append-only (2 anos) | **GAP CRÍTICO** - Compliance |
| **Retreinamento Automático** | ❌ Não aplicável | ✅ Hangfire mensal (domingo 02h) | **GAP CRÍTICO** - Model drift |

---

## 7. DECISÕES DE MODERNIZAÇÃO

### Decisão 1: Substituir Crystal Reports por Forecasting ML

- **Motivo:** Crystal Reports é lento, estático e não oferece análise preditiva. Azure ML + Prophet fornecem previsões estatisticamente confiáveis (95% confidence).
- **Impacto:** **ALTO** - Requer treinamento de modelos, infraestrutura Azure ML, mas aumenta valor estratégico do sistema.

### Decisão 2: Abandonar Multi-Database para Multi-tenancy Moderno

- **Motivo:** 50+ bancos SQL Server são complexos de gerenciar. Single-database com ClienteId + Row-Level Security é padrão SaaS moderno.
- **Impacto:** **ALTO** - Requer migração de dados de 50 bancos → 1 banco, mas simplifica operações DevOps e reduz custos de licenciamento SQL Server.

### Decisão 3: Introduzir Churn Prediction (Inexistente no Legado)

- **Motivo:** Clientes em risco de cancelamento não eram identificados no legado. Churn prediction com 70% precisão permite retenção proativa.
- **Impacto:** **MÉDIO** - Requer histórico de churns reais para treinar modelo, mas ROI esperado é alto (15% retenção).

### Decisão 4: Cache Redis 24h para Resultados ML

- **Motivo:** Recompilação de modelos a cada request é custosa (5-10s latência + billing Azure ML). Cache 24h reduz latência para < 100ms.
- **Impacto:** **MÉDIO** - Requer infraestrutura Redis, mas melhora UX significativamente.

### Decisão 5: Retreinamento Automático Mensal

- **Motivo:** Modelos ML degradam com o tempo ("model drift"). Retreinamento mensal garante modelos atualizados.
- **Impacto:** **MÉDIO** - Requer job Hangfire + validação automática (degradação > 5%), mas evita deployments manuais.

---

## 8. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Mitigação |
|-------|---------|-----------|
| **Falta de Dados Históricos** - Clientes novos sem 12 meses de dados | **ALTO** | Usar dados agregados de clientes similares (cluster) até completar 12 meses |
| **Azure ML Downtime** - SLA 99.9% ainda permite ~43min/mês de indisponibilidade | **MÉDIO** | Fallback para cálculos locais (sem ML) se Azure ML timeout > 30s |
| **Model Drift Não Detectado** - Modelo degrada mas validação falha | **ALTO** | Alerta manual se RMSE aumenta > 5% por 2 meses consecutivos |
| **Cache Redis Single Point of Failure** - Redis down = latência 10x | **MÉDIO** | Fallback para cálculo em tempo real (sem cache) + alerta DevOps |
| **Usuários Acostumados com Legado** - Resistência a forecasts vs relatórios estáticos | **BAIXO** | Treinamento + documentação clara (GU-100) + rollout gradual via Feature Flags |

---

## 9. RASTREABILIDADE

| Elemento Legado | Referência RF-100 |
|-----------------|-------------------|
| `RelatorioExecutivo.aspx` | **SUBSTITUÍDO** por `/admin/dashboards-preditivos` (Angular) |
| `DashboardKPI.aspx` | **SUBSTITUÍDO** por `/analytics/forecast-analysis` (Angular) |
| `WSRelatorio.GetRelatorioExecutivo()` | **SUBSTITUÍDO** por `GET /api/ml/dashboards/{id}` |
| `WSRelatorio.CalculaKPI()` | **SUBSTITUÍDO** por `POST /api/ml/forecast` |
| `[dbo].[Metricas]` | **ASSUMIDA** → `MetricDataPoint` (multi-tenancy) |
| `[dbo].[KPI_Config]` | **ASSUMIDA** → `KpiConfiguration` + `ModelMetrics` |
| `pa_Calcula_KPI` (Stored Procedure) | **SUBSTITUÍDO** por modelos ML (Prophet/ARIMA) |
| Detecção de anomalias manual | **SUBSTITUÍDA** por Z-score + Isolation Forest (RN-100-002) |

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|--------|------|-----------|-------|
| 1.0 | 2025-12-31 | Referência ao legado criada - Análise preditiva inexistente no sistema antigo | Agência ALC - alc.dev.br |
