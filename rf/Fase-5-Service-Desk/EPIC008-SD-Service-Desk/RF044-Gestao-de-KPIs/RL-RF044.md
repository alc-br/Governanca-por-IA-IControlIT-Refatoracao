# RL-RF044 — Referência ao Legado (Gestão de KPIs)

**Versão:** 1.0
**Data:** 2025-12-30
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF044 - Gestão de KPIs
**Sistema Legado:** ASP.NET Web Forms + VB.NET
**Objetivo:** Documentar o comportamento do legado relacionado a relatórios gerenciais e KPIs, servindo de base para refatoração com rastreabilidade completa.

---

## 1. CONTEXTO DO LEGADO

- **Arquitetura:** Monolítica ASP.NET Web Forms
- **Linguagem / Stack:** VB.NET (code-behind), JavaScript (Chart.js), SQL Server
- **Banco de Dados:** SQL Server (tabelas simples sem auditoria)
- **Multi-tenant:** Não (dados misturados por fornecedor)
- **Auditoria:** Inexistente (sem log de quem criou/alterou)
- **Configurações:** Web.config + tabelas de configuração

**Limitações Críticas:**
- KPIs fixos hardcoded sem possibilidade de customização
- Relatórios estáticos gerados sob demanda (não real-time)
- Sem sistema de alertas automáticos
- Gráficos simples sem interatividade
- Dados históricos limitados (90 dias)
- Cálculos manuais de metas e desvios
- Sem análise preditiva ou tendências
- Exportação limitada a Excel simples
- Performance degradada com muitos indicadores

---

## 2. TELAS DO LEGADO

### Tela: DashboardGerencial.aspx

- **Caminho:** `ic1_legado/IControlIT/Relatorios/DashboardGerencial.aspx`
- **Responsabilidade:** Exibir cards com valores fixos de KPIs + gráficos estáticos

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|------|------|-------------|-------------|
| ddlFornecedor | DropDownList | Sim | Filtro por fornecedor |
| txtDataInicio | TextBox (Date) | Sim | Data inicial do período |
| txtDataFim | TextBox (Date) | Sim | Data final do período |
| pnlKPIs | Panel | - | Container de cards de KPIs |
| chartCustos | Chart | - | Gráfico de pizza de custos |

#### Comportamentos Implícitos

- Gráficos gerados com Chart.js versão antiga (sem interatividade)
- Cards de KPIs com valores hardcoded (Receita, Custo, SLA)
- Sem drill-down ou filtros avançados
- Refresh manual da página obrigatório
- Timeout em consultas > 2min

**DESTINO:** SUBSTITUÍDO por dashboards Angular 19 + ApexCharts

---

### Tela: RelatorioKPIs.aspx

- **Caminho:** `ic1_legado/IControlIT/Relatorios/RelatorioKPIs.aspx`
- **Responsabilidade:** Lista de KPIs pré-definidos + exportação Excel básica

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|------|------|-------------|-------------|
| gvKPIs | GridView | - | Lista de KPIs fixos |
| btnExportar | Button | - | Exporta para Excel |
| ddlCategoria | DropDownList | Não | Filtro por categoria |

#### Comportamentos Implícitos

- KPIs fixos definidos em code-behind
- Exportação Excel sem formatação
- Cálculos manuais a cada request (sem cache)
- Sem versionamento de fórmulas
- Performance ruim com muitos registros

**DESTINO:** SUBSTITUÍDO por sistema de KPIs customizáveis com exportação avançada

---

### Tela: GraficosCustos.aspx

- **Caminho:** `ic1_legado/IControlIT/Relatorios/GraficosCustos.aspx`
- **Responsabilidade:** Gráficos de evolução de custos + comparação YoY

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|------|------|-------------|-------------|
| chartEvolucao | Chart | - | Gráfico de linha (evolução) |
| chartComparativo | Chart | - | Gráfico de barra (YoY) |

#### Comportamentos Implícitos

- Biblioteca Chart.js antiga (versão 2.x)
- Sem zoom ou interatividade
- Dados limitados a 12 meses
- Sem análise de tendências
- Performance degradada ao carregar muitos pontos

**DESTINO:** SUBSTITUÍDO por gráficos ApexCharts com zoom, drill-down, filtering

---

### Tela: ConfiguracaoMetas.aspx

- **Caminho:** `ic1_legado/IControlIT/Relatorios/ConfiguracaoMetas.aspx`
- **Responsabilidade:** CRUD básico de metas mensais

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|------|------|-------------|-------------|
| ddlKPI | DropDownList | Sim | KPI fixo |
| ddlMes | DropDownList | Sim | Mês (1-12) |
| txtAno | TextBox | Sim | Ano |
| txtValorMeta | TextBox | Sim | Valor numérico |

#### Comportamentos Implícitos

- Sem cascateamento hierárquico (corporativa → divisão → departamento)
- Alertas manuais via e-mail (não automáticos)
- Sem tipos de meta (mínima, ideal, desafiadora)
- Validação básica apenas no frontend (vulnerável)

**DESTINO:** SUBSTITUÍDO por sistema de metas hierárquicas com alertas automáticos

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

| Método | Local | Responsabilidade | Observações |
|------|-------|------------------|-------------|
| `GetDadosKPIs` | `WS_Relatorios.asmx` | Retorna DataTable com KPIs fixos | Sem paginação, timeout em consultas grandes |
| `GetGraficoCustos` | `WS_Relatorios.asmx` | Retorna JSON básico para Chart.js | Sem cache, recalcula toda vez |
| `CalcularSLAUptime` | `KPIHelper.vb` | Cálculo manual de SLA | Lógica fixa sem parametrização |
| `VerificarAtingimentoMeta` | `MetasHelper.vb` | Semáforo vermelho/amarelo/verde | Thresholds hardcoded (80%, 100%) |

**DESTINO:** TODOS SUBSTITUÍDOS por endpoints REST + CQRS + motor de cálculo customizável

---

## 4. TABELAS LEGADAS

| Tabela | Finalidade | Problemas Identificados |
|-------|------------|-------------------------|
| `KPI` | Armazena definição de KPIs | Sem multi-tenancy, sem auditoria, sem versionamento |
| `KPIValor` | Valores históricos | Sem particionamento (performance ruim), sem quem calculou |
| `KPIMeta` | Metas mensais | Sem hierarquia, sem tipos de meta (mínima/ideal/desafiadora) |

**DDL Legado (simplificado):**
```sql
CREATE TABLE dbo.KPI (
    Id INT IDENTITY PRIMARY KEY,
    Nome VARCHAR(200) NOT NULL,
    Formula VARCHAR(MAX), -- SQL hardcoded
    Ativo BIT DEFAULT 1,
    DataCriacao DATETIME DEFAULT GETDATE()
    -- ❌ Falta: multi-tenancy (Id_Fornecedor)
    -- ❌ Falta: auditoria (quem criou, alterou)
    -- ❌ Falta: soft delete (Fl_Excluido)
    -- ❌ Falta: versionamento de fórmulas
)

CREATE TABLE dbo.KPIValor (
    Id INT IDENTITY PRIMARY KEY,
    KPIId INT FOREIGN KEY REFERENCES KPI(Id),
    Data DATE NOT NULL,
    Valor DECIMAL(18,4)
    -- ❌ Falta: quem calculou, fonte, meta
)

CREATE TABLE dbo.KPIMeta (
    Id INT IDENTITY PRIMARY KEY,
    KPIId INT,
    Mes INT, -- 1-12
    Ano INT,
    ValorMeta DECIMAL(18,4)
    -- ❌ Falta: tipo de meta, cascateamento
)
```

**DESTINO:** SUBSTITUÍDO por schema moderno com multi-tenancy, auditoria, soft delete, versionamento

---

## 5. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

### RL-RN-001: Cálculo de Receita Mensal

**Descrição:** Receita mensal = SUM(ValorTotal) de faturas do mês atual
**Fonte:** `KPIHelper.vb:CalcularReceitaMensal()`
**Código original:**
```vb
Public Shared Function CalcularReceitaMensal() As Decimal
    Dim sql As String = "SELECT SUM(ValorTotal) FROM Faturas WHERE MONTH(Data) = MONTH(GETDATE())"
    Return ExecuteScalar(sql)
End Function
```

**DESTINO:** ASSUMIDO - Regra migrada para fórmula customizável no RF moderno

---

### RL-RN-002: Cálculo de SLA Uptime

**Descrição:** SLA = (totalMinutos - minutosIndisponivel) / totalMinutos * 100
**Fonte:** `KPIHelper.vb:CalcularSLAUptime()`
**Código original:**
```vb
Public Shared Function CalcularSLAUptime() As Decimal
    Dim totalMinutos As Integer = 30 * 24 * 60
    Dim minutosIndisponivel As Integer = GetMinutosIndisponiveis()
    Return (totalMinutos - minutosIndisponivel) / totalMinutos * 100
End Function
```

**DESTINO:** ASSUMIDO - Lógica preservada mas parametrizada (período configurável)

---

### RL-RN-003: Semáforo de Metas (Vermelho/Amarelo/Verde)

**Descrição:** < 80% = Vermelho, 80-99% = Amarelo, ≥ 100% = Verde
**Fonte:** `MetasHelper.vb:VerificarAtingimentoMeta()`
**Código original:**
```vb
If percentual < 80 Then Return "Vermelho"
If percentual < 100 Then Return "Amarelo"
Return "Verde"
```

**DESTINO:** EXPANDIDO - Sistema moderno adiciona Azul (meta ideal) e Roxo (meta desafiadora)

---

## 6. GAP ANALYSIS (LEGADO x RF MODERNO)

| Item | Legado | RF Moderno | Observação |
|-----|--------|------------|------------|
| KPIs Customizáveis | ❌ Fixos hardcoded | ✅ Fórmulas SQL/C# customizáveis | Nova funcionalidade |
| Dashboards Interativos | ❌ Estáticos | ✅ ApexCharts com zoom, drill-down | Melhoria significativa |
| Alertas Automáticos | ❌ E-mails manuais | ✅ Threshold, tendência, anomalia | Nova funcionalidade |
| Análise Preditiva | ❌ Inexistente | ✅ Azure ML forecasting | Nova funcionalidade |
| Histórico | ⚠️ 90 dias | ✅ 7 anos (LGPD) | Expansão |
| Metas Hierárquicas | ❌ Planas | ✅ Cascateamento corporativa → equipe | Nova funcionalidade |
| Exportação | ⚠️ Excel básico | ✅ Power BI, Tableau, PDF | Expansão |
| Versionamento de Fórmulas | ❌ Inexistente | ✅ Histórico de versões | Nova funcionalidade |
| Permissões por Categoria | ❌ Sem controle | ✅ RBAC granular | Nova funcionalidade |
| Dashboard Público | ❌ Inexistente | ✅ Token JWT temporário | Nova funcionalidade |

---

## 7. DECISÕES DE MODERNIZAÇÃO

### Decisão 1: Motor de Cálculo Customizável

**Descrição:** Substituir KPIs fixos por sistema de fórmulas customizáveis (SQL + C#)
**Motivo:** Flexibilidade para criar KPIs sem alterar código. Suporte a regras de negócio complexas.
**Impacto:** Alto - Arquitetura completamente nova (KPICalculationService)

---

### Decisão 2: Análise Preditiva com Azure ML

**Descrição:** Integrar Azure Machine Learning para forecasting e detecção de anomalias
**Motivo:** Permitir alertas proativos antes de problemas se agravarem
**Impacto:** Alto - Dependência externa, custos de API, complexidade técnica

---

### Decisão 3: Dashboards com ApexCharts

**Descrição:** Substituir Chart.js antigo por ApexCharts moderno
**Motivo:** Gráficos responsivos, interativos (zoom, drill-down), melhor UX
**Impacto:** Médio - Necessário reescrever lógica de geração de gráficos

---

### Decisão 4: Histórico de 7 Anos (LGPD)

**Descrição:** Estender retenção de dados históricos de 90 dias para 7 anos
**Motivo:** Conformidade LGPD + análises de longo prazo
**Impacto:** Alto - Particionamento de tabelas, estratégia de arquivamento

---

### Decisão 5: Alertas Automáticos Inteligentes

**Descrição:** Sistema de alertas com ML (threshold, tendência, anomalia, comparativo, SLA)
**Motivo:** Reduzir carga manual de monitoramento
**Impacto:** Alto - Lógica complexa de detecção + integração com canais de notificação

---

## 8. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Mitigação |
|------|---------|-----------|
| Migração de dados históricos incompleta | Alto | Script de migração testado + validação de integridade |
| Fórmulas legadas incompatíveis | Médio | Mapeamento manual + testes de regressão |
| Performance de cálculos complexos | Médio | Caching (Redis) + background jobs (Hangfire) |
| Custo de APIs externas (Azure ML) | Médio | Rate limiting + fallback para cálculos locais |
| Resistência de usuários a novo sistema | Baixo | Treinamento + período de convivência legado/moderno |

---

## 9. RASTREABILIDADE

| Elemento Legado | Referência RF |
|----------------|---------------|
| DashboardGerencial.aspx | RN-RF044-01 a RN-RF044-15 (todos) |
| RelatorioKPIs.aspx | UC01-criar-kpi, UC02-visualizar-kpi |
| GraficosCustos.aspx | UC07-visualizar-dashboard |
| ConfiguracaoMetas.aspx | UC05-definir-metas |
| KPIHelper.vb:CalcularReceitaMensal() | RN-RF044-02 (validação de fórmula) |
| KPIHelper.vb:CalcularSLAUptime() | RN-RF044-02 (validação de fórmula) |
| MetasHelper.vb:VerificarAtingimentoMeta() | RN-RF044-05 (semáforo automático) |
| Tabela KPI | Entidade KPI (RF moderno) |
| Tabela KPIValor | Entidade KPIHistorico (RF moderno) |
| Tabela KPIMeta | Entidade KPIMeta (RF moderno) |

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|------|------|----------|------|
| 1.0 | 2025-12-30 | Criação inicial - separação RF/RL após migração v2.0 | Agência ALC - alc.dev.br |
