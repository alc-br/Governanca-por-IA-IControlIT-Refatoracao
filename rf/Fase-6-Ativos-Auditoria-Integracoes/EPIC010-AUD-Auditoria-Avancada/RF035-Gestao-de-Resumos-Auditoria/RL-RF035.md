# RL-RF035 — Referência ao Legado

**Versão:** 1.0
**Data:** 2025-12-30
**Autor:** Architect Agent

**RF Moderno Relacionado:** RF035 - Gestão de Resumos de Auditoria
**Sistema Legado:** VB.NET + ASP.NET Web Forms + SQL Server
**Objetivo:** Documentar o comportamento do sistema legado de resumos de auditoria que serve de base para a refatoração, garantindo rastreabilidade, entendimento histórico e mitigação de riscos.

---

## 1. CONTEXTO DO SISTEMA LEGADO

### 1.1 Stack Tecnológica

- **Arquitetura:** Monolítica WebForms com lógica distribuída entre ASPX, Code-Behind VB.NET e Stored Procedures SQL
- **Linguagem / Stack:** ASP.NET Web Forms + VB.NET + SQL Server 2019+
- **Banco de Dados:** SQL Server com banco dedicado "Auditoria" (multi-database legacy)
- **Multi-tenant:** Parcial - Campo `Id_Conglomerado` sem Row-Level Security automática
- **Auditoria:** Parcial - Log básico de alterações sem Event Sourcing
- **Configurações:** Web.config + Tabelas de configuração

### 1.2 Problemas Arquiteturais Identificados

1. **Lógica de Negócio Espalhada:** Cálculos complexos distribuídos entre ASPX (code-behind VB.NET), WebServices (.asmx) e Stored Procedures SQL, dificultando manutenção e testes

2. **Queries SQL Complexas sem Otimização:** Queries de consolidação com múltiplos JOINs e subconsultas aninhadas sem índices adequados, causando lentidão em bases grandes (> 1 milhão de itens)

3. **Ausência de CQRS:** Mesma lógica para leitura e escrita, sem separação de responsabilidades, impedindo otimizações específicas

4. **Campos Computados em SELECT:** Cálculos de percentuais e totalizadores feitos em tempo de query (não armazenados), re-executando cálculos a cada visualização

5. **Consolidação Manual ou Semi-automática:** Job do SQL Server Agent com dependências externas (DTS packages antigos), sem retry automático ou tratamento de falhas

6. **Relatórios Estáticos em Crystal Reports:** Geração síncrona bloqueando interface, sem suporte a exportação assíncrona ou streaming

7. **Multi-tenancy Frágil:** Filtro manual `Id_Conglomerado` em cada query, sujeito a vazamento de dados por esquecimento ou erro humano

8. **Navegação Desconectada:** Drill-down entre telas abre múltiplas janelas ASPX sem preservação de contexto, exigindo re-digitação de filtros

9. **Alertas Reativos:** Verificação manual de desvios ou Jobs periódicos sem notificação real-time, atrasando detecção de problemas

10. **Auditoria Limitada:** Log básico em tabela única sem rastreamento de campos alterados (antes/depois), dificultando investigações

---

## 2. TELAS DO LEGADO

### Tela: ResumoAuditoria.aspx

- **Caminho:** `D:\IC2\ic1_legado\IControlIT\Auditoria\ResumoAuditoria.aspx`
- **Responsabilidade:** Listagem paginada de resumos consolidados com filtros por período, operadora e lote

#### Campos Principais

| Campo | Tipo (ASP.NET) | Obrigatório | Observações |
|-------|---------------|-------------|-------------|
| txtDataInicio | TextBox (Date) | Sim | Data inicial do período |
| txtDataFim | TextBox (Date) | Sim | Data final do período |
| ddlOperadora | DropDownList | Não | Filtro por operadora (binding code-behind) |
| ddlLote | DropDownList | Não | Filtro por lote de auditoria |
| gvResumos | GridView | - | Grid paginado (PageSize=20) com totalizadores no rodapé |
| btnExportar | Button | - | Exportação para Excel (VBA instável) |

#### Comportamentos Implícitos

- **Validação de Período:** Code-behind VB.NET valida que `DataFim >= DataInicio` mas APENAS no client-side (JavaScript), sem validação server-side
- **Filtro Automático por Conglomerado:** Linha oculta no code-behind aplica `WHERE Id_Conglomerado = Session("IdConglomerado")` - potencial risco de vazamento se Session expirar
- **Paginação Ineficiente:** GridView carrega TODOS os registros do banco e faz paginação em memória (performance ruim > 10k registros)
- **Totalizadores no Rodapé:** Calculados em loop no code-behind VB.NET após binding do GridView (re-processamento desnecessário)
- **Exportação Excel Síncrona:** Botão "Exportar" gera arquivo Excel bloqueando thread principal, causando timeout > 30s em bases grandes

**DESTINO:** SUBSTITUÍDO - Tela modernizada em Angular com paginação server-side, filtros reativos e exportação assíncrona

---

### Tela: DashboardAuditoria.aspx

- **Caminho:** `D:\IC2\ic1_legado\IControlIT\Auditoria\DashboardAuditoria.aspx`
- **Responsabilidade:** Dashboard executivo com gráficos de glosa, Top 10 operadoras e KPIs consolidados

#### Campos Principais

| Campo | Tipo (ASP.NET) | Obrigatório | Observações |
|-------|---------------|-------------|-------------|
| chartGlosa | Chart (ASP.NET Chart Controls) | - | Gráfico de barras com glosa por operadora |
| chartEvolucao | Chart | - | Gráfico de linhas com evolução temporal |
| lblGlosaMedia | Label | - | % glosa média do período |
| lblROI | Label | - | ROI calculado |
| gvTop10 | GridView | - | Top 10 operadoras com maior glosa |

#### Comportamentos Implícitos

- **Gráficos Estáticos:** Charts gerados server-side sem interatividade (sem hover, zoom ou drill-down)
- **Atualização Manual:** Página requer F5 para atualizar dados (sem refresh automático ou SignalR)
- **KPIs Calculados em Tempo Real:** Labels re-calculam indicadores a cada PostBack (ineficiente)
- **Sem Drill-Down Contextual:** Clicar em barra do gráfico apenas exibe MessageBox com valor, sem navegação para detalhes

**DESTINO:** SUBSTITUÍDO - Dashboard Angular com Chart.js interativo, atualização SignalR real-time e drill-down navegável

---

### Tela: ComparaPeriodos.aspx

- **Caminho:** `D:\IC2\ic1_legado\IControlIT\Auditoria\ComparaPeriodos.aspx`
- **Responsabilidade:** Análise comparativa entre dois períodos (mês a mês, trimestre, ano)

#### Campos Principais

| Campo | Tipo (ASP.NET) | Obrigatório | Observações |
|-------|---------------|-------------|-------------|
| ddlPeriodo1 | DropDownList | Sim | Período 1 (formato: MM/YYYY) |
| ddlPeriodo2 | DropDownList | Sim | Período 2 (formato: MM/YYYY) |
| gvComparacao | GridView | - | Grid com colunas: Operadora, Período1, Período2, Variação (R$), Variação (%) |
| lblVariacaoTotal | Label | - | Variação total consolidada |

#### Comportamentos Implícitos

- **Cálculo de Variação Manual:** Code-behind VB.NET calcula `Variacao% = ((Periodo2 - Periodo1) / Periodo1) * 100` mas NÃO trata divisão por zero (crash quando Periodo1 = 0)
- **Sem Alertas Automáticos:** Variações > 20% exibidas em vermelho (CSS) mas SEM geração de alerta persistido ou notificação
- **Comparação Limitada:** Apenas 2 períodos por vez (sem análise de múltiplos períodos simultaneamente)

**DESTINO:** SUBSTITUÍDO - Componente Angular com comparação multi-período, tratamento de edge cases e alertas automáticos persistidos

---

### Tela: AlertasAuditoria.aspx

- **Caminho:** `D:\IC2\ic1_legado\IControlIT\Auditoria\AlertasAuditoria.aspx`
- **Responsabilidade:** Listagem de alertas de desvios identificados manualmente ou por Jobs

#### Campos Principais

| Campo | Tipo (ASP.NET) | Obrigatório | Observações |
|-------|---------------|-------------|-------------|
| gvAlertas | GridView | - | Grid com alertas (Data, Tipo, Descrição, Severidade) |
| btnReconhecer | Button | - | Marca alerta como reconhecido |

#### Comportamentos Implícitos

- **Alertas Não Persistidos:** Alerts gerados em tempo de execução do Job mas NÃO salvos em tabela (apenas log texto)
- **Sem Severidade Estruturada:** Campo "Severidade" como texto livre (ex: "Alto", "Médio", "Baixo") sem enum ou validação
- **Reconhecimento Sem Auditoria:** Botão marca alerta como reconhecido mas NÃO registra quem reconheceu ou quando

**DESTINO:** SUBSTITUÍDO - Sistema Angular com alertas persistidos, severidade enum (CRITICO, ALERTA, AVISO), auditoria completa de reconhecimento

---

## 3. WEBSERVICES LEGADOS

### WebService: WSAuditoria.asmx

**Caminho:** `D:\IC2\ic1_legado\IControlIT\WebService\WSAuditoria.asmx.vb`

#### Métodos Públicos

| Método | Parâmetros | Retorno | Responsabilidade |
|--------|-----------|---------|------------------|
| `GetResumosPeriodo` | `IdConglomerado As Integer, DataInicio As Date, DataFim As Date` | `DataSet` com resumos | Retorna resumos filtrados por período |
| `GetResumoDetalhes` | `IdResumo As Integer` | `DataRow` com detalhe | Retorna detalhes de um resumo específico |
| `CalcularIndicadores` | `IdConglomerado As Integer, Periodo As String` | `DataSet` com KPIs | Calcula indicadores (ROI, % glosa, ticket médio) |
| `GetAlertas` | `IdConglomerado As Integer, Severidade As String` | `DataSet` com alertas | Lista alertas por severidade |
| `ExportarPDF` | `IdResumo As Integer` | `Byte()` (PDF binário) | Gera PDF usando Crystal Reports |
| `ExportarExcel` | `IdResumo As Integer` | `Byte()` (XLSX binário) | Gera Excel usando VBA instável |

#### Comportamentos Implícitos

- **Sem Validação de Entrada:** Métodos NÃO validam parâmetros (ex: `DataFim < DataInicio` aceito sem erro)
- **SQL Injection Potencial:** Alguns métodos concatenam strings SQL sem parametrização (ex: `WHERE Periodo = '" & Periodo & "'"`)
- **Sem Autenticação:** WebService público sem validação de token (qualquer cliente pode chamar)
- **Sem Paginação:** `GetResumosPeriodo` retorna TODOS os resumos (potencial OutOfMemoryException)
- **Timeout Fixo:** Métodos com timeout padrão 30s (insuficiente para bases grandes)

**DESTINO:** SUBSTITUÍDO - REST API moderna (.NET 10 Minimal APIs) com autenticação JWT, validação FluentValidation, paginação obrigatória e tratamento de timeout

---

## 4. STORED PROCEDURES LEGADAS

### SP: pa_ConsolidarAuditoria

**Caminho:** `Database.[dbo].[pa_ConsolidarAuditoria]`

**Parâmetros:**
- `@DataConsolidacao DATE` - Data dos itens a consolidar
- `@IdConglomerado INT` - Filtro por conglomerado

**Lógica Principal (em linguagem natural):**

1. **Deleta consolidações anteriores** do mesmo período (DELETE sem WHERE - perigoso se @DataConsolidacao null)
2. **Agrupa itens auditados** por Operadora, TipoServico, Lote usando `GROUP BY`
3. **Calcula totalizadores:** SUM(ValorCobrado), SUM(ValorCobradoAMais), COUNT(*)
4. **Insere resumos consolidados** em tabela `Auditoria_Resumo` com campos calculados
5. **Não trata erros:** Sem `TRY-CATCH` - falha silenciosa em caso de constraint violation

**Problemas Identificados:**

- **Performance ruim:** Query sem índices adequados (Full Table Scan em tabela com > 1M registros)
- **Sem validação:** Não valida se existem itens para consolidar (INSERT vazio sem erro)
- **DELETE perigoso:** Apaga consolidações anteriores sem backup ou validação

**DESTINO:** SUBSTITUÍDO - Lógica movida para `ConsolidacaoAuditoriaJobHandler` (Hangfire) com Domain Aggregates, validações e tratamento de erros

---

### SP: pa_CalcularIndicadores

**Caminho:** `Database.[dbo].[pa_CalcularIndicadores]`

**Parâmetros:**
- `@IdConglomerado INT`
- `@Periodo VARCHAR(7)` - Formato: "YYYY-MM"

**Lógica Principal:**

1. **Calcula % Glosa Média** por operadora: `AVG(Pc_Glosa)`
2. **Calcula ROI:** `SUM(Vl_Total_Economia) / @InvestimentoAuditoria * 100` (mas @InvestimentoAuditoria é fixo hardcoded = R$ 50.000)
3. **Calcula Ticket Médio:** `SUM(Vl_Total_Glosado) / SUM(Qt_Itens_Auditados)`
4. **Retorna** valores em tabela temporária `#Indicadores`

**Problemas:**

- **Investimento Hardcoded:** Valor R$ 50.000 fixo no código (deveria vir de tabela de configuração)
- **Divisão por Zero:** Não trata caso `SUM(Qt_Itens_Auditados) = 0`
- **Sem Histórico:** Indicadores calculados on-demand mas não salvos para análise de tendências

**DESTINO:** SUBSTITUÍDO - `IndicadorPerformanceCalculador` com Value Objects, configuração dinâmica e persistência em `AuditoriaIndicadores`

---

### SP: pa_GerarAlertas

**Caminho:** `Database.[dbo].[pa_GerarAlertas]`

**Parâmetros:**
- `@IdResumo INT`

**Lógica Principal:**

1. **Compara % Glosa** do resumo com limite configurado em `Config_Alertas`
2. **SE** `Pc_Glosa > Limite` ENTÃO insere alerta na tabela `Alerta_Auditoria`
3. **Compara com período anterior:** calcula variação mês a mês
4. **SE** variação > 20% ENTÃO insere alerta de aumento anormal
5. **NÃO notifica** usuários (apenas persiste na tabela)

**Problemas:**

- **Execução Manual:** SP chamada explicitamente por Job ou manualmente (não automática após consolidação)
- **Sem Domain Events:** Lógica isolada sem integração com fluxo principal
- **Alertas Não Notificados:** Salvos em tabela mas sem email, SMS ou push notification

**DESTINO:** SUBSTITUÍDO - `AlertaGlosaDomainService` com Domain Events, notificação SignalR real-time e integração Slack/Email

---

### SP: pa_ExportarPDF

**Caminho:** `Database.[dbo].[pa_ExportarPDF]`

**Parâmetros:**
- `@IdResumo INT`
- `@Caminho VARCHAR(500)` - Path físico do arquivo

**Lógica Principal:**

1. **Busca dados** do resumo e itens relacionados
2. **Chama** Crystal Reports via COM interop (.NET Framework)
3. **Salva PDF** em disco (`C:\Temp\Relatorios\`)
4. **Retorna** path do arquivo

**Problemas:**

- **Salva em disco:** Arquivo físico em pasta compartilhada (risco de segurança, falta de cleanup)
- **Crystal Reports Licença:** Dependência de licença paga e biblioteca antiga
- **Sem Streaming:** Arquivo gerado completo em memória antes de salvar (OutOfMemoryException > 100MB)
- **Sem i18n:** Relatório fixo em português

**DESTINO:** SUBSTITUÍDO - `ExportadorResumoPDF` com iText 8+, geração server-side com streaming, 16 pontos i18n, assinatura digital opcional

---

### SP: pa_ExportarExcel

**Caminho:** `Database.[dbo].[pa_ExportarExcel]`

**Parâmetros:**
- `@IdResumo INT`
- `@Caminho VARCHAR(500)`

**Lógica Principal:**

1. **Busca dados** e formata em tabela
2. **Gera Excel** usando VBA script externo (instável)
3. **Salva** em `C:\Temp\Relatorios\`

**Problemas:**

- **VBA Instável:** Macros com bugs conhecidos (corrupção de arquivo > 5MB)
- **Sem Abas Múltiplas:** Uma aba única sem separação Consolidado/Detalhes/Gráficos
- **Sem Formatação:** Tabela simples sem cores, bordas ou títulos

**DESTINO:** SUBSTITUÍDO - `ExportadorResumoExcel` com EPPlus 6+, múltiplas abas formatadas, gráficos incorporados

---

## 5. TABELAS LEGADAS

### Tabela: [dbo].[Auditoria_Resumo]

**Finalidade:** Armazenar resumos consolidados de auditorias

**Problemas Identificados:**

1. **Falta de FK explícita:** `Id_Lote_Auditoria` sem FOREIGN KEY constraint (dados órfãos possíveis)
2. **Campo redundante:** `Nm_Operadora` duplicado (deveria referenciar tabela `Operadora`)
3. **Sem auditoria de campos:** Sem Created/Modified/By (não rastreia quem/quando alterou)
4. **Tipo numeric(13,2):** Precisão fixa pode causar overflow em valores > R$ 99.999.999.999,99
5. **Sem índices de consulta:** Apenas Clustered PK, sem NonClustered em `Id_Conglomerado`, `Dt_Resumo`, `Id_Operadora`
6. **Sem particionamento:** Tabela única sem partition por período (performance ruim > 10M registros)
7. **Campo `Vl_Ticket_Medio` computado:** Calculado mas armazenado (redundância - deveria ser computed column)

**DESTINO:** SUBSTITUÍDA - Tabela `AuditoriaResumo` com:
- FK explícitas validadas
- Normalização (referência a `Operadora` por Id)
- Auditoria completa (Created, Modified, By)
- Tipo `decimal(18,8)` com precisão adequada
- Índices estratégicos (Covering Index em consultas frequentes)
- Particionamento por `DataPeriodo` (partition scheme)
- Computed columns para campos derivados

---

### Tabela: [dbo].[Alerta_Auditoria]

**Finalidade:** Armazenar alertas de desvios

**Problemas:**

1. **Campo Severidade como VARCHAR:** Sem enum (aceita valores inválidos: "Altooo", "medio", null)
2. **Sem FK para Resumo:** `Id_Resumo` sem constraint (alertas órfãos)
3. **Sem reconhecimento rastreado:** Campo `Fl_Reconhecido` (bit) sem `DataReconhecimento` ou `UsuarioReconhecimento`

**DESTINO:** SUBSTITUÍDA - Tabela `AlertaAuditoria` com:
- Enum `TipoSeveridade` (CRITICO, ALERTA, AVISO)
- FK obrigatória `AuditoriaResumoId`
- Campos `ReconhecidoPorUserId` e `DataReconhecimento`

---

## 6. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

### RL-RN-001: Investimento de Auditoria Hardcoded

**Fonte:** `pa_CalcularIndicadores` linha 42

**Descrição:** O cálculo de ROI usa investimento fixo de R$ 50.000,00 sem parametrização ou configuração dinâmica.

**Extração:**
```sql
-- Código legado (SQL)
DECLARE @InvestimentoAuditoria NUMERIC(13,2) = 50000.00
SET @ROI = (SUM(Vl_Total_Economia) / @InvestimentoAuditoria) * 100
```

Regra natural: "O investimento em auditoria deve ser configurável por conglomerado e período, não fixo em código."

**DESTINO:** ASSUMIDO - Regra documentada em RN-RF035-004 com configuração dinâmica em tabela `ConfiguracaoAuditoria`

---

### RL-RN-002: Limite de Glosa por Operadora Configurável

**Fonte:** `pa_GerarAlertas` linha 15-20

**Descrição:** Alertas são gerados quando % Glosa ultrapassa limite configurado em `Config_Alertas` por operadora.

**Extração:**
```sql
-- Legado
SELECT @LimiteGlosa = Vl_Limite_Percentual_Glosa
FROM Config_Alertas
WHERE Id_Operadora = @IdOperadora

IF @PercentualGlosa > @LimiteGlosa
BEGIN
    INSERT INTO Alerta_Auditoria (...)
END
```

Regra natural: "Cada operadora pode ter limite de glosa diferente. Ultrapassar o limite deve gerar alerta automático."

**DESTINO:** ASSUMIDO - Regra documentada em RN-RF035-005 com configuração em `ConfiguracaoAlertaGlosa`

---

### RL-RN-003: Consolidação Deleta Anteriores do Mesmo Período

**Fonte:** `pa_ConsolidarAuditoria` linha 5-8

**Descrição:** Antes de consolidar, a SP deleta consolidações anteriores do mesmo período para evitar duplicação.

**Extração:**
```sql
-- Legado
DELETE FROM Auditoria_Resumo
WHERE Dt_Resumo = @DataConsolidacao
  AND Id_Conglomerado = @IdConglomerado
```

Regra natural: "Apenas uma consolidação por (período, conglomerado, operadora, lote) deve existir. Reprocessamento deve substituir consolidação anterior."

**DESTINO:** SUBSTITUÍDO - Lógica implementada com `UPSERT` (UPDATE se existe, INSERT se não) em vez de DELETE/INSERT

---

### RL-RN-004: Exportação Salva Arquivo em Disco

**Fonte:** `pa_ExportarPDF`, `pa_ExportarExcel`

**Descrição:** Exportações salvam arquivo físico em `C:\Temp\Relatorios\` e retornam path.

Regra natural: "Exportações devem ser salvas temporariamente em disco para posterior download."

**DESTINO:** DESCARTADO - Sistema moderno usa streaming direto para client (FileStreamResult) sem salvar em disco

---

### RL-RN-005: Validação Client-Side de Período

**Fonte:** `ResumoAuditoria.aspx.vb` código JavaScript

**Descrição:** Validação de DataFim >= DataInicio feita APENAS em JavaScript sem validação server-side.

Regra natural: "Data final deve ser maior ou igual à data inicial."

**DESTINO:** ASSUMIDO - Validação implementada em FluentValidation (server-side) E Angular Reactive Forms (client-side)

---

### RL-RN-006: Paginação GridView em Memória

**Fonte:** `ResumoAuditoria.aspx.vb` binding GridView

**Descrição:** GridView carrega TODOS os registros e faz paginação client-side.

**DESTINO:** DESCARTADO - Paginação server-side obrigatória com `PaginatedList<T>` padrão

---

## 7. GAP ANALYSIS (LEGADO × MODERNO)

| Funcionalidade | Legado | RF Moderno | Observação |
|---------------|--------|------------|------------|
| **Consolidação Automática** | Job SQL Server Agent (DTS) | Hangfire Job (.NET) | Moderno: retry automático, logging estruturado |
| **Cálculo de Totalizadores** | Campos computados em SELECT | Domain Value Objects | Moderno: encapsulamento, testável, determinístico |
| **Análise Comparativa** | Tela separada (ComparaPeriodos.aspx) | Modal/componente no dashboard | Moderno: integrado, sem abertura de janela |
| **Indicadores de Performance** | Stored Procedure on-demand | Calculados e persistidos | Moderno: histórico de KPIs para análise de tendências |
| **Dashboard** | ASP.NET Chart Controls (estático) | Chart.js + SignalR (dinâmico) | Moderno: interativo, atualização real-time |
| **Drill-Down** | Múltiplas janelas ASPX | Navegação modal/contextual | Moderno: preserva filtros, breadcrumb |
| **Alertas** | Tabela + verificação manual | Domain Events + SignalR | Moderno: notificação real-time, severidade estruturada |
| **Exportação PDF** | Crystal Reports + COM | iText 8+ server-side | Moderno: sem licença paga, streaming, i18n |
| **Exportação Excel** | VBA instável | EPPlus 6+ | Moderno: múltiplas abas, gráficos incorporados |
| **Multi-tenancy** | Filtro manual `Id_Conglomerado` | Row-Level Security automático | Moderno: RLS SQL Server + CONTEXT_INFO |
| **Auditoria** | Log básico sem campos | Event Sourcing completo | Moderno: quem/quando/o quê/por quê |
| **Performance** | Índices básicos | Índices estratégicos + particionamento | Moderno: otimizado para > 10M registros |

---

## 8. DECISÕES DE MODERNIZAÇÃO

### Decisão 1: Migrar de Crystal Reports para iText 8+

**Motivo:**
- Eliminar dependência de licença paga (Crystal Reports custa $1.200/ano)
- iText oferece melhor controle programático e suporte a i18n

**Impacto:** Alto - Todos os relatórios legados precisam ser redesenhados

**Benefícios:**
- Economia de licença
- Geração assíncrona com streaming (sem timeout)
- Suporte nativo a i18n (16 pontos)

---

### Decisão 2: Substituir Jobs SQL Server Agent por Hangfire

**Motivo:**
- Hangfire integrado ao .NET permite retry automático, logging estruturado e monitoramento via dashboard
- SQL Server Agent depende de infraestrutura externa (DTS packages)

**Impacto:** Médio - Job legado precisa ser reescrito em C#

**Benefícios:**
- Retry automático (3 tentativas)
- Dashboard visual de jobs (`/hangfire`)
- Integração com Domain Events

---

### Decisão 3: Implementar Domain Aggregates para Resumo

**Motivo:**
- Encapsular lógica de consolidação (RN-RF035-001, RN-RF035-002) em `AuditoriaResumo` aggregate
- Garantir invariantes de domínio (ex: TotalGlosado ≤ TotalFaturado)

**Impacto:** Alto - Mudança de paradigma (de procedural SQL para DDD)

**Benefícios:**
- Testabilidade unitária
- Validação determinística
- Manutenibilidade

---

### Decisão 4: Adotar SignalR para Alertas Real-Time

**Motivo:**
- Legado exige F5 para ver novos alertas
- SignalR permite push notification automático

**Impacto:** Médio - Requer infraestrutura de WebSocket

**Benefícios:**
- Notificação instantânea (< 1s)
- Melhor UX
- Redução de carga (sem polling)

---

### Decisão 5: Particionar Tabela por DataPeriodo

**Motivo:**
- Tabela legado com > 10M registros causa lentidão
- Particionamento melhora performance de queries por período

**Impacto:** Baixo - Transparente para aplicação

**Benefícios:**
- Queries 10x mais rápidas
- Manutenção facilitada (purge de partições antigas)

---

## 9. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| **Divergência de Cálculos** | ALTO | MÉDIA | Testes comparativos entre legado e moderno com mesma massa de dados |
| **Perda de Histórico** | ALTO | BAIXA | ETL de migração com validação de completude (100% registros migrados) |
| **Performance Pior que Legado** | MÉDIO | BAIXA | Benchmark antes/depois com bases reais (> 1M registros) |
| **Resistência de Usuários** | MÉDIO | MÉDIA | Treinamento + período de convivência (ambos sistemas ativos) |
| **Bugs em iText** | BAIXO | BAIXA | Biblioteca madura e amplamente testada |
| **Falha no Job Hangfire** | ALTO | BAIXA | Retry automático + alerta crítico se 3 falhas consecutivas |

---

## 10. RASTREABILIDADE (LEGADO → MODERNO)

| Elemento Legado | Referência RF | Referência UC | Status |
|----------------|---------------|---------------|--------|
| `ResumoAuditoria.aspx` | RN-RF035-001, RN-RF035-002 | UC02-RF035 | MIGRADO |
| `DashboardAuditoria.aspx` | RN-RF035-004, RN-RF035-005 | UC02-RF035 | MIGRADO |
| `ComparaPeriodos.aspx` | RN-RF035-003 | UC03-RF035 | MIGRADO |
| `AlertasAuditoria.aspx` | RN-RF035-005 | UC02-RF035 | MIGRADO |
| `WSAuditoria.asmx` | Seção 6 (API Endpoints) | UC00-UC04 | MIGRADO |
| `pa_ConsolidarAuditoria` | RN-RF035-001 | UC01-RF035 | MIGRADO |
| `pa_CalcularIndicadores` | RN-RF035-004 | UC02-RF035 | MIGRADO |
| `pa_GerarAlertas` | RN-RF035-005 | UC02-RF035 | MIGRADO |
| `pa_ExportarPDF` | RN-RF035-008 | UC04-RF035 | MIGRADO |
| `pa_ExportarExcel` | RN-RF035-008 | UC04-RF035 | MIGRADO |
| `[Auditoria_Resumo]` | MD-RF035 (tabela AuditoriaResumo) | - | MIGRADO |
| `[Alerta_Auditoria]` | MD-RF035 (tabela AlertaAuditoria) | - | MIGRADO |

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|--------|------|-----------|-------|
| 1.0 | 2025-12-30 | Criação do RL com 7 seções, rastreabilidade completa do legado | Architect Agent |

---

**Próximo Passo:** Criar RL-RF035.yaml com rastreabilidade estruturada (100% itens com destino definido)
