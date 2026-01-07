# RL-RF099 — Referência ao Legado: Dashboards e KPIs

**Versão:** 1.0
**Data:** 2025-12-31
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF-099 — Dashboards e KPIs
**Sistema Legado:** IControlIT VB.NET + ASP.NET WebForms + Crystal Reports
**Objetivo:** Documentar comportamento do legado de dashboards e KPIs que serve de base para refatoração, garantindo rastreabilidade e mitigação de riscos.

---

## 1. CONTEXTO DO LEGADO

### Arquitetura Legada
- **Tipo**: Monolítica Cliente-Servidor
- **Linguagem Frontend**: ASP.NET WebForms (ASPX) + VB.NET Code-Behind
- **Linguagem Backend**: VB.NET + WebServices (ASMX)
- **Banco de Dados**: SQL Server (múltiplos databases por cliente)
- **Relatórios**: Crystal Reports + SQL Server Views
- **Multi-tenant**: Multi-Database (1 database por cliente)
- **Auditoria**: Inexistente para dashboards
- **Configurações**: Web.config + SQL Server tables

### Stack Tecnológica
- **Framework**: .NET Framework 4.5
- **UI**: ASP.NET WebForms com ViewState
- **Charts**: Crystal Reports (binários compilados, não editáveis)
- **Data Access**: ADO.NET com SqlCommand direto (SQL Injection risk)
- **Refresh**: Manual (F5) ou agendado SQL Server Agent (1x/hora)

### Problemas Identificados
1. **Sem Real-Time**: Refresh manual ou batch 1x/hora, dados desatualizados
2. **Crystal Reports Fixos**: Relatórios compilados, não customizáveis pelo usuário
3. **Sem Alertas**: Nenhum sistema de alerta quando KPI sai de meta
4. **Sem Multi-Tenancy Seguro**: ClienteId em queries mas sem Row-Level Security
5. **SQL Injection**: Queries concatenadas sem parametrização
6. **Sem Auditoria**: Não registra quem acessou, exportou ou visualizou dashboards sensíveis

---

## 2. TELAS DO LEGADO

### Tela 1: DashboardExecutivo.aspx

**Caminho:** `D:\IC2\ic1_legado\IControlIT\Relatorios\DashboardExecutivo.aspx`

**Responsabilidade:** Exibe dashboard executivo com 3 KPIs fixos: SLA Geral, Custos Totais, Chamados Abertos. Usa Crystal Reports embarcado (CrystalReportViewer control).

**Campos/Controles:**
| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| `crvDashboard` | CrystalReportViewer | Sim | Control para renderizar Crystal Reports |
| `ddlCliente` | DropDownList | Não | Filtro por cliente (se usuário Admin) |
| `ddlPeriodo` | DropDownList | Sim | Período fixo (Hoje, Última Semana, Último Mês) |
| `btnAtualizar` | Button | Sim | Botão para refresh manual (F5 alternativo) |

**Comportamentos Implícitos:**
- **BI-DSH-001**: Relatório sempre carrega todos os dados do cliente sem paginação (performance ruim)
- **BI-DSH-002**: Período "Último Mês" hardcoded para 30 dias (ignora mês calendário)
- **BI-DSH-003**: KPIs calculados em tempo de execução (queries lentas no SQL Server)
- **BI-DSH-004**: Crystal Reports gera PDF temporário no servidor (nunca limpo, disk fill risk)
- **BI-DSH-005**: Sem permissão granular: qualquer usuário autenticado acessa (security risk)

**Code-Behind Crítico (VB.NET):**
```vb
Protected Sub Page_Load(sender As Object, e As EventArgs)
    If Not IsPostBack Then
        Dim clienteId As String = Session("ClienteId").ToString()
        Dim periodo As String = ddlPeriodo.SelectedValue ' "30" para último mês

        ' SQL INJECTION RISK: concatenação direta
        Dim sql As String = "SELECT * FROM vw_DashboardExecutivo WHERE ClienteId = " & clienteId & " AND DataCriacao >= DATEADD(day, -" & periodo & ", GETDATE())"

        Dim rpt As New ReportDocument()
        rpt.Load(Server.MapPath("~/Relatorios/DashboardExecutivo.rpt"))
        rpt.SetDataSource(ExecuteQuery(sql)) ' Executa query sem parametrização

        crvDashboard.ReportSource = rpt
        crvDashboard.DataBind()
    End If
End Sub
```

---

### Tela 2: RelatoriosChamados.aspx

**Caminho:** `D:\IC2\ic1_legado\IControlIT\Relatorios\RelatoriosChamados.aspx`

**Responsabilidade:** Lista chamados do cliente com filtros básicos (Status, Prioridade, Data). Exporta para Crystal Reports ou Excel.

**Campos/Controles:**
| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| `gvChamados` | GridView | Sim | Grid com paginação manual (ViewState pesado) |
| `ddlStatus` | DropDownList | Não | Filtro por status (Aberto, Resolvido, Fechado) |
| `ddlPrioridade` | DropDownList | Não | Filtro por prioridade (P1, P2, P3) |
| `txtDataInicio` | TextBox | Não | Data início (sem validação, aceita texto livre) |
| `txtDataFim` | TextBox | Não | Data fim (sem validação) |
| `btnExportar` | Button | Sim | Exporta para Excel (formato XLS legado) |

**Comportamentos Implícitos:**
- **BI-REL-001**: GridView carrega todos os dados em memória (OutOfMemoryException com > 10k registros)
- **BI-REL-002**: Exportação Excel gera arquivo temporário sem cleanup (disk fill)
- **BI-REL-003**: Sem paginação server-side, apenas client-side (performance ruim)
- **BI-REL-004**: Datas aceitas em formato livre (dd/MM/yyyy, MM-dd-yyyy, etc.) sem validação

---

### Tela 3: RelatoriosFaturas.aspx

**Caminho:** `D:\IC2\ic1_legado\IControlIT\Relatorios\RelatoriosFaturas.aspx`

**Responsabilidade:** Exibe relatório de faturas por cliente com totalizadores. Usa Crystal Reports para PDF.

**Campos/Controles:**
| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| `crvFaturas` | CrystalReportViewer | Sim | Crystal Reports embarcado |
| `ddlClienteFiltro` | DropDownList | Não | Filtro por cliente (Admin only) |
| `ddlStatusFatura` | DropDownList | Não | Filtro por status (Pendente, Pago, Atrasado) |

**Comportamentos Implícitos:**
- **BI-FAT-001**: Totalizadores calculados no Crystal Reports (logic duplicada em 3 lugares)
- **BI-FAT-002**: Sem cache, recalcula dados a cada F5 (queries lentas)
- **BI-FAT-003**: PDF gerado sincronamente (trava browser por 5-10 segundos)

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

### WebService: WSDashboard.asmx.vb

**Caminho:** `D:\IC2\ic1_legado\WebService\WSDashboard.asmx.vb`

**Métodos:**

| Método | Responsabilidade | Observações |
|--------|------------------|-------------|
| `GetDashboardExecutivo(clienteId As Integer)` | Retorna dados do dashboard executivo | SQL Injection risk, sem cache |
| `GetRelatoriosChamados(clienteId As Integer, status As String, dataInicio As String, dataFim As String)` | Retorna lista de chamados filtrados | Datas como string (parsing manual), SQL Injection |
| `ExportarPDF(relatorioNome As String, clienteId As Integer)` | Gera PDF do relatório e retorna byte array | Síncrono, pode travar por 10+ segundos |

**Código Crítico (VB.NET):**
```vb
<WebMethod()>
Public Function GetDashboardExecutivo(clienteId As Integer) As DataSet
    ' SQL INJECTION RISK
    Dim sql As String = "EXEC pa_DashboardExecutivo @ClienteId = " & clienteId.ToString()

    Dim ds As New DataSet()
    Using conn As New SqlConnection(ConfigurationManager.ConnectionStrings("IControlIT_Cliente" & clienteId).ConnectionString)
        Dim cmd As New SqlCommand(sql, conn)
        Dim adapter As New SqlDataAdapter(cmd)
        adapter.Fill(ds)
    End Using

    Return ds
End Function
```

**Problemas:**
- **PROB-WS-001**: SQL concatenado (SQL Injection)
- **PROB-WS-002**: Connection string hardcoded por cliente (multi-database inseguro)
- **PROB-WS-003**: Sem tratamento de exceções (expõe stack trace completo)
- **PROB-WS-004**: Sem auditoria (não registra quem chamou o método)

---

## 4. TABELAS LEGADAS

### Tabela 1: Chamados

**Finalidade:** Armazena chamados do Service Desk (fonte de dados para KPIs).

**Schema:**
```sql
CREATE TABLE [dbo].[Chamados](
    [IdChamado] [int] IDENTITY(1,1) NOT NULL,
    [IdCliente] [int] NOT NULL,
    [IdFilial] [int] NULL,
    [Descricao] [varchar](500) NOT NULL,
    [DataAbertura] [datetime] NOT NULL,
    [DataFechamento] [datetime] NULL,
    [TempoResolucao] [int] NULL, -- Minutos
    [Prioridade] [varchar](10) NOT NULL, -- P1, P2, P3
    [Status] [varchar](20) NOT NULL, -- Aberto, Resolvido, Fechado
    CONSTRAINT [PK_Chamados] PRIMARY KEY CLUSTERED ([IdChamado] ASC)
);
```

**Problemas Identificados:**
- **PROB-TAB-001**: IdCliente sem FK (dados órfãos possíveis)
- **PROB-TAB-002**: varchar(500) para Descricao (limite baixo)
- **PROB-TAB-003**: Prioridade como varchar livre (deveria ser ENUM)
- **PROB-TAB-004**: Sem campos de auditoria (DataCriacao, CriadoPor, DataAlteracao, AlteradoPor)
- **PROB-TAB-005**: Sem índices em DataAbertura, Status (queries lentas)

---

### Tabela 2: Faturas

**Finalidade:** Armazena faturas de clientes (usado para KPI "Custo por Cliente").

**Schema:**
```sql
CREATE TABLE [dbo].[Faturas](
    [IdFatura] [int] IDENTITY(1,1) NOT NULL,
    [IdCliente] [int] NOT NULL,
    [IdFilial] [int] NULL,
    [Valor] [decimal](18,2) NOT NULL,
    [DataFatura] [datetime] NOT NULL,
    [Status] [varchar](20) NOT NULL, -- Pendente, Pago, Atrasado
    CONSTRAINT [PK_Faturas] PRIMARY KEY CLUSTERED ([IdFatura] ASC)
);
```

**Problemas Identificados:**
- **PROB-TAB-006**: Status como varchar livre (deveria ser ENUM)
- **PROB-TAB-007**: Sem campos de auditoria
- **PROB-TAB-008**: Sem índices em DataFatura, Status

---

### Tabela 3: Ativos

**Finalidade:** Armazena ativos de clientes (usado em dashboards de inventário).

**Schema:**
```sql
CREATE TABLE [dbo].[Ativos](
    [IdAtivo] [int] IDENTITY(1,1) NOT NULL,
    [IdCliente] [int] NOT NULL,
    [IdFilial] [int] NULL,
    [Descricao] [varchar](100) NOT NULL,
    [DataAquisicao] [datetime] NOT NULL,
    [ValorAquisicao] [decimal](18,2) NOT NULL,
    CONSTRAINT [PK_Ativos] PRIMARY KEY CLUSTERED ([IdAtivo] ASC)
);
```

**Problemas Identificados:**
- **PROB-TAB-009**: Sem campos de auditoria
- **PROB-TAB-010**: Sem índices em DataAquisicao

---

## 5. STORED PROCEDURES LEGADAS

### SP 1: pa_DashboardExecutivo

**Responsabilidade:** Retorna KPIs do dashboard executivo (SLA Geral, Custos, Chamados Abertos).

**Código:**
```sql
CREATE PROCEDURE [dbo].[pa_DashboardExecutivo]
    @ClienteId INT
AS
BEGIN
    SELECT
        -- SLA Geral
        CAST(COUNT(CASE WHEN TempoResolucao <= 240 THEN 1 END) AS DECIMAL) / COUNT(*) * 100 AS SLAGeral,

        -- Custos Totais
        (SELECT SUM(Valor) FROM Faturas WHERE IdCliente = @ClienteId AND Status = 'Pago') AS CustosTotais,

        -- Chamados Abertos
        (SELECT COUNT(*) FROM Chamados WHERE IdCliente = @ClienteId AND Status = 'Aberto') AS ChamadosAbertos

    FROM Chamados
    WHERE IdCliente = @ClienteId
END
```

**Problemas:**
- **PROB-SP-001**: SLA hardcoded para 240 minutos (4 horas), não configurável
- **PROB-SP-002**: Subquery em SELECT (performance ruim)
- **PROB-SP-003**: Sem filtro de período (calcula desde sempre)

---

### SP 2: pa_RelatoriosChamados

**Responsabilidade:** Retorna lista de chamados filtrados.

**Código:**
```sql
CREATE PROCEDURE [dbo].[pa_RelatoriosChamados]
    @ClienteId INT,
    @Status VARCHAR(20) = NULL,
    @DataInicio DATETIME = NULL,
    @DataFim DATETIME = NULL
AS
BEGIN
    SELECT
        IdChamado, Descricao, DataAbertura, DataFechamento, Prioridade, Status
    FROM Chamados
    WHERE IdCliente = @ClienteId
        AND (@Status IS NULL OR Status = @Status)
        AND (@DataInicio IS NULL OR DataAbertura >= @DataInicio)
        AND (@DataFim IS NULL OR DataAbertura <= @DataFim)
    ORDER BY DataAbertura DESC
END
```

**Problemas:**
- **PROB-SP-004**: Sem paginação (retorna todos os registros)
- **PROB-SP-005**: Sem índices apropriados (lento com > 10k registros)

---

### SP 3: pa_RelatorioFaturas

**Responsabilidade:** Retorna lista de faturas filtradas por status.

**Código:**
```sql
CREATE PROCEDURE [dbo].[pa_RelatorioFaturas]
    @ClienteId INT,
    @Status VARCHAR(20) = NULL
AS
BEGIN
    SELECT
        IdFatura, Valor, DataFatura, Status,
        SUM(Valor) OVER () AS TotalGeral
    FROM Faturas
    WHERE IdCliente = @ClienteId
        AND (@Status IS NULL OR Status = @Status)
    ORDER BY DataFatura DESC
END
```

**Problemas:**
- **PROB-SP-006**: Sem paginação
- **PROB-SP-007**: SUM OVER() calcula para todos os registros (performance ruim)

---

## 6. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

### RN-LEG-DSH-001: SLA sempre 4 horas (hardcoded)
**Descrição:** KPI "Tempo Médio Resolução" sempre usa meta de 4 horas (240 minutos) hardcoded em stored procedure `pa_DashboardExecutivo`. Não há configuração de meta por cliente ou filial.

**Destino:** SUBSTITUÍDO — RF-099 permite configuração de meta via `ConfigureKpiMetaCommand` com valores diferentes por cliente/filial.

---

### RN-LEG-DSH-002: Refresh manual ou batch 1x/hora
**Descrição:** Dashboards não atualizam automaticamente. Usuário deve clicar F5 ou aguardar job SQL Server Agent executar 1x/hora.

**Destino:** SUBSTITUÍDO — RF-099 implementa refresh real-time via SignalR a cada 30 segundos.

---

### RN-LEG-DSH-003: Período "Último Mês" = 30 dias fixos
**Descrição:** Filtro de período "Último Mês" sempre calcula `DATEADD(day, -30, GETDATE())` ignorando calendário (meses com 28, 29, 31 dias).

**Destino:** CORRIGIDO — RF-099 usa `DateTime.UtcNow.AddMonths(-1)` respeitando calendário.

---

### RN-LEG-DSH-004: Sem alertas proativos
**Descrição:** Sistema não notifica quando KPI sai de meta. Usuário deve abrir dashboard manualmente para verificar.

**Destino:** SUBSTITUÍDO — RF-099 implementa `MonitorKpiAlertsBackgroundService` que dispara alertas amarelos (80% meta) e vermelhos (60% meta) via email/SMS.

---

### RN-LEG-DSH-005: Sem auditoria de acessos
**Descrição:** Sistema não registra quem acessou dashboard executivo, quais dados visualizou ou exportou.

**Destino:** SUBSTITUÍDO — RF-099 implementa auditoria completa com `DashboardAccessAuditAttribute` registrando usuário, IP, timestamp, dados acessados. Retenção 7 anos (LGPD).

---

### RN-LEG-DSH-006: Multi-Database sem Row-Level Security
**Descrição:** Multi-tenancy implementado como 1 database por cliente (`IControlIT_Cliente01`, `IControlIT_Cliente02`). ClienteId em queries mas sem Row-Level Security. Risco de vazamento de dados se connection string errada.

**Destino:** SUBSTITUÍDO — RF-099 usa banco único com `ClienteId` em todas as tabelas + Row-Level Security via EF Core Global Query Filters.

---

## 7. GAP ANALYSIS (LEGADO x RF MODERNO)

| Item | Legado | RF Moderno (RF-099) | Observação |
|------|--------|---------------------|------------|
| **Atualização de Dados** | Manual (F5) ou batch 1x/hora | Real-time via SignalR (30s) + WebSocket | Gap crítico de UX |
| **Widgets** | Relatórios fixos Crystal Reports | Widgets drag-and-drop, reposicionáveis | Gap de customização |
| **Filtros** | Parâmetros fixos em relatório | Filtros dinâmicos, multi-select | Gap de flexibilidade |
| **Alertas** | Sem alertas em tempo real | Alertas com limites configuráveis, email + SMS | Gap de proatividade |
| **Export** | Excel XLS legado, sem branding | PDF com logo cliente, Excel XLSX, Power BI API | Gap de branding |
| **Tecnologia Frontend** | ASP.NET WebForms, ViewState pesado | Angular 19 Standalone Components | Gap arquitetural |
| **Tecnologia Backend** | VB.NET, SQL concatenado | .NET 10, EF Core, CQRS + MediatR | Gap de segurança |
| **Performance** | Queries lentas, sem cache | Redis cache, agregações ElasticSearch | Gap de performance |
| **Multi-tenancy** | Multi-Database (1 DB por cliente) | Row-Level Security (ClienteId em filtros) | Gap de escalabilidade |
| **Auditoria** | Logs básicos ou inexistentes | Auditoria completa (acesso, export, alertas) | Gap de compliance |

---

## 8. DECISÕES DE MODERNIZAÇÃO

### Decisão 1: Abandonar Crystal Reports
**Motivo:** Crystal Reports é legado, binários compilados, não editáveis dinamicamente, licenças caras. Substituir por Chart.js (open-source, JavaScript, customizável).

**Impacto:** ALTO — Requer reimplementação de todos os 12+ relatórios legados como componentes Angular.

---

### Decisão 2: Migrar Multi-Database → Single Database
**Motivo:** Multi-Database não escala (limite físico de databases no SQL Server, complexidade de manutenção). Single Database com Row-Level Security é padrão SaaS moderno.

**Impacto:** ALTO — Requer migração de dados de N databases para 1 único database com `ClienteId` em todas as tabelas.

---

### Decisão 3: Substituir Refresh Manual → SignalR Real-Time
**Motivo:** UX moderna exige dados em tempo real sem F5. SignalR WebSocket permite push de servidor para cliente sem polling HTTP.

**Impacto:** MÉDIO — Requer infraestrutura de WebSocket (Azure SignalR Service ou self-hosted).

---

### Decisão 4: Implementar Sistema de Alertas
**Motivo:** Dashboards reativos (usuário abre e vê) são inferiores a proativos (sistema avisa quando problema). Alertas com limites (80% amarelo, 60% vermelho) são padrão em SLAs.

**Impacto:** MÉDIO — Requer BackgroundService monitorando KPIs a cada 30s + integração com Email/SMS.

---

### Decisão 5: Auditoria Obrigatória (LGPD)
**Motivo:** Dashboards executivos contêm dados financeiros sensíveis. LGPD exige auditoria de acessos com retenção de 7 anos.

**Impacto:** MÉDIO — Requer tabela `AuditLog` com particionamento por cliente + job de limpeza automática após 7 anos.

---

## 9. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Mitigação |
|-------|---------|-----------|
| **Perda de Dados na Migração Multi-DB → Single DB** | CRÍTICO | Backup completo antes de migração + script de validação de integridade referencial + rollback plan |
| **Incompatibilidade de Fórmulas de KPI** | ALTO | Mapear todas as 15+ fórmulas legadas (SUM, AVG, COUNT) e testar com dados reais side-by-side (legado vs moderno) |
| **Performance de Dashboards com > 100k Registros** | MÉDIO | Implementar paginação server-side + Redis cache + agregações ElasticSearch para grandes datasets |
| **Dependência de Crystal Reports em Processos de Negócio** | MÉDIO | Manter Crystal Reports legado em paralelo por 3-6 meses (sunset gradual) até usuários migrarem |
| **Resistência de Usuários a Nova Interface** | BAIXO | Treinamento + documentação + período de transição com acesso a ambos (legado e moderno) |

---

## 10. RASTREABILIDADE

### Elementos Legados → RF Moderno

| Elemento Legado | Referência RF-099 |
|-----------------|-------------------|
| `DashboardExecutivo.aspx` | Seção 4 (Funcionalidades - F1: Dashboard Executivo) |
| `RelatoriosChamados.aspx` | Seção 4 (Funcionalidades - F4: Filtros Dinâmicos) |
| `RelatoriosFaturas.aspx` | Seção 4 (Funcionalidades - F10: Export Multi-Formato) |
| `WSDashboard.GetDashboardExecutivo()` | Endpoint `GET /api/dashboards/executivo` |
| `WSDashboard.ExportarPDF()` | Endpoint `POST /api/dashboards/{id}/export/pdf` |
| `pa_DashboardExecutivo` | Query `CalculateKpiQuery` (CQRS) |
| `pa_RelatoriosChamados` | Query `GetDashboardDataQuery` + filtros dinâmicos |
| Tabela `Chamados` | Entity `ChamadoEntity` (fonte de dados para KPIs) |
| Tabela `Faturas` | Entity `FaturaEntity` (KPI "Custo por Cliente") |
| Crystal Reports | Chart.js (Angular component) |
| SQL Server Views | EF Core Queries + Redis Cache |
| Multi-Database | Single Database + Row-Level Security |

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|--------|------|-----------|-------|
| 1.0 | 2025-12-31 | Criação de RL-RF099 após migração v1.0 → v2.0 | Claude Code |

---

**Última Atualização**: 2025-12-31
**Autor**: Claude Code
**Revisão**: Pendente
**Status**: Documentação Completa
