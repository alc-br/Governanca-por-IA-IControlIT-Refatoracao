# Casos de Uso - RF101: Dashboards Executivos Operacionais

**Versão:** 1.0
**Data:** 2025-12-28
**RF Relacionado:** [RF101 - Dashboards Executivos Operacionais](./RF101.md)

---

## Índice de Casos de Uso

| UC | Nome | Descrição |
|----|------|-----------|
| UC01 | Visualizar Dashboard C-Level | Visão estratégica com 4 KPIs principais (Receita, Custos, Compliance, SLA) |
| UC02 | Visualizar Dashboard de Custos | Consolidação de custos por filial, centro de custo e contrato com trending |
| UC03 | Visualizar Heatmap de Consumo | Matriz bidimensional filial x centro de custo com escala de cores |
| UC04 | Visualizar Forecast com Machine Learning | Previsão de custos futuros com intervalo de confiança (ARIMA/Regressão) |
| UC05 | Exportar Dashboard em PowerPoint | Geração de relatório executivo em formato PPTX com gráficos embutidos |

---

## UC01 - Visualizar Dashboard C-Level

### Descrição

Permite executivos (CEO, CFO, CIO, Diretoria) visualizarem dashboard estratégico consolidado com 4 KPIs principais: Receita Total, Custos Totais, Margem Operacional e Conformidade SLA. Dashboard apresenta dados em tempo real (com atualização SignalR), trending comparativo com mês anterior, e alertas visuais quando indicadores saem de faixas aceitáveis.

### Atores

- Executivo C-Level (CEO, CFO, CIO)
- Diretoria
- Gerência Sênior
- Sistema de consolidação (Hangfire Job)
- Azure ML (para forecast)

### Pré-condições

- Usuário autenticado no sistema
- Usuário possui permissão: `dashboard:executivo:view`
- Usuário possui perfil: CEO, CFO, CIO, Diretoria ou Gerência Sênior
- Multi-tenancy ativo (ClienteId válido)
- Dados consolidados disponíveis (job Hangfire executado às 06:00 AM UTC)
- Mínimo 12 meses de histórico para exibição de trending

### Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa menu Dashboards → Executivo → C-Level | - |
| 2 | - | Valida autenticação via JWT Token |
| 3 | - | Valida autorização: verifica permissão `dashboard:executivo:view` |
| 4 | - | Valida perfil: CEO, CFO, CIO, Diretoria ou Gerência |
| 5 | - | Registra acesso em AuditLog (código: DSH_DASHBOARD_ACESSO) |
| 6 | - | Aplica filtro multi-tenancy (ClienteId do usuário logado) |
| 7 | - | Executa query `GET /api/dashboards/executivo/clevel` |
| 8 | - | Busca dados consolidados em FatoDashboard_Custos (últimos 12 meses) |
| 9 | - | Calcula KPIs: Receita Total, Custos Totais, Margem Operacional, Conformidade SLA |
| 10 | - | Calcula variação percentual vs mês anterior para cada KPI |
| 11 | - | Aplica alertas visuais: verde (conforme), amarelo (aviso), vermelho (crítico) |
| 12 | - | Renderiza interface com 4 widgets de KPI (D3.js/Highcharts) |
| 13 | - | Conecta SignalR para atualizações em tempo real |
| 14 | Visualiza dashboard com KPIs consolidados, trending e alertas | - |

### Fluxos Alternativos

**FA01 - Dados Ainda Não Consolidados Hoje**
- **Condição:** Job Hangfire ainda não executou (antes das 06:00 AM UTC)
- **Ação:** Sistema exibe dados do dia anterior com aviso "Dados atualizados em [data/hora]"

**FA02 - Drill-Down em KPI**
- **Condição:** Usuário clica em um KPI específico (ex: Custos Totais)
- **Ação:** Sistema redireciona para UC02 (Dashboard de Custos) com filtro pré-aplicado

**FA03 - Alteração de Período**
- **Condição:** Usuário seleciona período customizado (últimos 3, 6, 12 meses)
- **Ação:** Sistema recarrega dashboard com dados do período selecionado

**FA04 - Exportar Dashboard**
- **Condição:** Usuário clica em "Exportar em PowerPoint"
- **Ação:** Sistema aciona UC05 (Exportar Dashboard em PowerPoint)

### Exceções

**EX01 - Usuário Sem Permissão**
- **Condição:** Usuário não possui perfil executivo ou permissão `dashboard:executivo:view`
- **Ação:** Sistema retorna HTTP 403 Forbidden, exibe mensagem "Acesso negado. Usuário sem permissão.", registra tentativa em AuditLog com flag "Unauthorized"

**EX02 - Dados Insuficientes (< 12 meses)**
- **Condição:** Contrato possui menos de 12 meses de histórico
- **Ação:** Sistema exibe dashboard com KPIs disponíveis e aviso "Histórico insuficiente para trending (< 12 meses)"

**EX03 - Erro de Consolidação**
- **Condição:** Job Hangfire falhou na consolidação (status=Falha)
- **Ação:** Sistema exibe mensagem "Erro ao carregar dados. Contate o suporte.", registra erro em log estruturado

**EX04 - Erro de Conexão com SignalR**
- **Condição:** Falha ao conectar WebSocket para atualizações em tempo real
- **Ação:** Sistema funciona em modo polling (atualização manual), exibe aviso "Atualizações automáticas indisponíveis"

### Pós-condições

- Dashboard C-Level exibido com dados atualizados
- Acesso registrado em AuditLog com: UserId, ClienteId, DashboardTipo="C-Level", DataAcesso, IpOrigem, UserAgent
- Conexão SignalR ativa para atualizações em tempo real
- Dados em cache Redis por 12 horas (expiração às 18:00 UTC)

### Regras de Negócio Aplicáveis

- **RN-DSH-101-01**: Controle de Acesso Restrito a Executivos
- **RN-DSH-101-02**: Consolidação Diária de Dados via Hangfire
- **RN-DSH-101-10**: Auditoria Obrigatória de Acesso a Dashboards Executivos

---

## UC02 - Visualizar Dashboard de Custos

### Descrição

Permite executivos e gerentes visualizarem consolidação de custos por contrato, filial, centro de custo com trending histórico (diário, semanal, mensal), forecast com ML (6-12 meses), e comparativo Budget vs Real com alertas automáticos.

### Atores

- Executivo C-Level (CEO, CFO, CIO)
- Diretoria
- Gerência Sênior
- Gerente de Filial (acesso restrito à sua filial)
- Sistema de consolidação (Hangfire Job)
- Azure ML / ML.NET (forecast)

### Pré-condições

- Usuário autenticado no sistema
- Usuário possui permissão: `dashboard:executivo:view`
- Multi-tenancy ativo (ClienteId válido)
- Dados consolidados em FatoDashboard_Custos disponíveis
- Para trending: mínimo 3 meses de histórico
- Para forecast: mínimo 12 meses de histórico

### Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa menu Dashboards → Executivo → Custos | - |
| 2 | - | Valida autenticação e autorização (permissão `dashboard:executivo:view`) |
| 3 | - | Registra acesso em AuditLog (código: DSH_DASHBOARD_ACESSO) |
| 4 | - | Aplica filtro multi-tenancy (ClienteId) |
| 5 | - | Se Gerente de Filial: aplica filtro adicional por FilialId |
| 6 | - | Executa query `GET /api/dashboards/executivo/custos` |
| 7 | - | Busca dados de FatoDashboard_Custos agregados por FilialId, CentroCustoId, ContratoId |
| 8 | - | Calcula custos totais por dimensão (Filial, Centro de Custo, Contrato) |
| 9 | - | Busca Budget definido (RF094) para comparativo |
| 10 | - | Calcula variação percentual: ((Real - Budget) / Budget) * 100 |
| 11 | - | Aplica alertas: > 10% variação = amarelo, > 20% variação = vermelho |
| 12 | - | Busca trending: últimos 12 meses de FatoDashboard_Custos |
| 13 | - | Calcula regressão linear para linha de tendência |
| 14 | - | Renderiza interface com: gráficos de custos, trending, Budget vs Real, alertas |
| 15 | Visualiza dashboard de custos consolidado com trending e comparativos | - |

### Fluxos Alternativos

**FA01 - Alterar Granularidade de Trending**
- **Condição:** Usuário seleciona granularidade: diária (30 dias), semanal (13 semanas), mensal (12 meses)
- **Ação:** Sistema recarrega trending com granularidade selecionada, recalcula regressão linear

**FA02 - Drill-Down em Filial/Centro de Custo**
- **Condição:** Usuário clica em barra de gráfico de uma filial/centro de custo específico
- **Ação:** Sistema exibe detalhamento: contratos, faturas, itens de custo, histórico mensal

**FA03 - Visualizar Forecast**
- **Condição:** Usuário clica em "Ver Forecast (ML)"
- **Ação:** Sistema aciona UC04 (Visualizar Forecast com Machine Learning)

**FA04 - Exportar Dashboard de Custos**
- **Condição:** Usuário clica em "Exportar"
- **Ação:** Sistema gera PDF ou Excel com dados de custos, trending e comparativos

### Exceções

**EX01 - Budget Não Definido**
- **Condição:** Não existe orçamento (budget) cadastrado para o período
- **Ação:** Sistema exibe custos reais sem comparativo, mensagem "Budget não definido. Configure em RF094."

**EX02 - Dados Insuficientes para Trending**
- **Condição:** Menos de 3 meses de histórico disponível
- **Ação:** Sistema exibe custos mas sem trending, aviso "Histórico insuficiente para trending (< 3 meses)"

**EX03 - Variação Crítica (> 20%)**
- **Condição:** Variação Budget vs Real > 20%
- **Ação:** Sistema exibe alerta vermelho com mensagem "CRÍTICO: Desvio de [X]% - Ação necessária", envia notificação para CFO

**EX04 - Erro ao Calcular Regressão**
- **Condição:** Falha ao calcular regressão linear (dados inconsistentes)
- **Ação:** Sistema exibe trending sem linha de tendência, log de erro registrado

### Pós-condições

- Dashboard de Custos exibido com dados consolidados, trending e alertas
- Acesso registrado em AuditLog
- Se variação > 20%: Notificação enviada para CFO
- Dados em cache Redis por 12 horas

### Regras de Negócio Aplicáveis

- **RN-DSH-101-02**: Consolidação Diária de Dados via Hangfire
- **RN-DSH-101-04**: Budget vs Real com Alertas quando Variação > 10%
- **RN-DSH-101-06**: Trending com Suporte a Múltiplas Granularidades
- **RN-DSH-101-10**: Auditoria Obrigatória de Acesso a Dashboards Executivos

---

## UC03 - Visualizar Heatmap de Consumo

### Descrição

Permite executivos visualizarem matriz bidimensional (filiais x centros de custo) com escala de cores representando intensidade de consumo: verde (< 80% da meta), amarelo (80-100% da meta), vermelho (> 100% da meta). Heatmap permite identificação rápida de "hot spots" de despesa e suporta drill-down para detalhes.

### Atores

- Executivo C-Level (CEO, CFO, CIO)
- Diretoria
- Gerência Sênior
- Sistema de consolidação (Hangfire Job)

### Pré-condições

- Usuário autenticado no sistema
- Usuário possui permissão: `dashboard:executivo:view`
- Multi-tenancy ativo (ClienteId válido)
- Dados consolidados em FatoDashboard_Custos disponíveis
- Metas mensais definidas por FilialId e CentroCustoId

### Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa menu Dashboards → Executivo → Heatmap de Consumo | - |
| 2 | - | Valida autenticação e autorização (permissão `dashboard:executivo:view`) |
| 3 | - | Registra acesso em AuditLog (código: DSH_DASHBOARD_ACESSO) |
| 4 | - | Aplica filtro multi-tenancy (ClienteId) |
| 5 | Seleciona período: mês e ano (padrão: mês atual) | - |
| 6 | - | Executa query `GET /api/dashboards/executivo/heatmap?mes={MM}&ano={YYYY}` |
| 7 | - | Busca todas FilialId ativas (ClienteId filtrado) |
| 8 | - | Busca todos CentroCustoId ativos (ClienteId filtrado) |
| 9 | - | Para cada célula (Filial x CCusto): busca consumo realizado em FatoDashboard_Custos |
| 10 | - | Para cada célula: busca meta mensal definida |
| 11 | - | Calcula percentual: (ConsumoReal / MetaMensal) * 100 |
| 12 | - | Aplica escala de cores: < 80% = verde (#4CAF50), 80-100% = amarelo (#FFC107), > 100% = vermelho (#F44336) |
| 13 | - | Calcula trending: variação % últimos 3 meses |
| 14 | - | Renderiza matriz bidimensional com cores e tooltips (valor absoluto, % meta, trending) |
| 15 | Visualiza heatmap com "hot spots" destacados em vermelho | - |

### Fluxos Alternativos

**FA01 - Drill-Down em Célula**
- **Condição:** Usuário clica em célula específica do heatmap
- **Ação:** Sistema exibe detalhamento: contratos da filial/ccusto, faturas, histórico mensal, trending

**FA02 - Filtrar por Filial/Centro de Custo**
- **Condição:** Usuário aplica filtro para visualizar apenas filiais ou centros de custo específicos
- **Ação:** Sistema recarrega heatmap com filtro aplicado

**FA03 - Alterar Período**
- **Condição:** Usuário altera mês/ano de referência
- **Ação:** Sistema recarrega heatmap com dados do período selecionado

**FA04 - Exportar Heatmap**
- **Condição:** Usuário clica em "Exportar"
- **Ação:** Sistema gera imagem PNG ou PDF do heatmap para compartilhamento

### Exceções

**EX01 - Meta Não Definida**
- **Condição:** Célula sem meta mensal cadastrada
- **Ação:** Sistema exibe célula em cinza (#999999) com tooltip "Meta não definida"

**EX02 - Sem Dados de Consumo**
- **Condição:** Filial/CCusto sem consumo no período (valor = 0)
- **Ação:** Sistema exibe célula em branco com tooltip "Sem consumo registrado"

**EX03 - Erro ao Calcular Trending**
- **Condição:** Menos de 3 meses de histórico disponível
- **Ação:** Sistema exibe heatmap sem trending, tooltip sem variação %

**EX04 - Acessibilidade (Daltonismo)**
- **Condição:** Usuário ativa modo acessível
- **Ação:** Sistema aplica escala de cores compatível com WCAG AA (padrões alternativos para verde/vermelho)

### Pós-condições

- Heatmap exibido com escala de cores representando intensidade de consumo
- "Hot spots" (vermelho) identificados visualmente
- Acesso registrado em AuditLog
- Dados em cache Redis por 12 horas

### Regras de Negócio Aplicáveis

- **RN-DSH-101-05**: Heatmap com Escala de Cores (Verde < 80%, Amarelo 80-100%, Vermelho > 100%)
- **RN-DSH-101-10**: Auditoria Obrigatória de Acesso a Dashboards Executivos

---

## UC04 - Visualizar Forecast com Machine Learning

### Descrição

Permite executivos visualizarem previsão de custos futuros (3, 6, 12 meses) usando modelos de Machine Learning (ARIMA ou Regressão Linear) treinados com Azure ML SDK ou ML.NET. Forecast apresenta intervalo de confiança de 95%, indicador de qualidade (R²) e data de próxima atualização do modelo.

### Atores

- Executivo C-Level (CEO, CFO, CIO)
- Diretoria
- Gerência Sênior
- Azure ML Studio / ML.NET (treinamento e inferência)
- Sistema de consolidação (Hangfire Job)

### Pré-condições

- Usuário autenticado no sistema
- Usuário possui permissão: `dashboard:executivo:view`
- Multi-tenancy ativo (ClienteId válido)
- Contrato possui mínimo 12 meses de histórico em FatoDashboard_Custos
- Modelo de forecast treinado e validado (R² >= 0.85)

### Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa menu Dashboards → Executivo → Forecast (ML) | - |
| 2 | - | Valida autenticação e autorização (permissão `dashboard:executivo:view`) |
| 3 | - | Registra acesso em AuditLog (código: DSH_DASHBOARD_ACESSO) |
| 4 | - | Aplica filtro multi-tenancy (ClienteId) |
| 5 | Seleciona contrato e período de forecast (3, 6, 12 meses) | - |
| 6 | - | Executa query `GET /api/dashboards/executivo/forecast?contratoId={id}&meses=6` |
| 7 | - | Busca série histórica: últimos 12+ meses de FatoDashboard_Custos |
| 8 | - | Valida se histórico >= 12 meses (RN-DSH-101-03) |
| 9 | - | Prepara dados para ML: normaliza série temporal |
| 10 | - | Treina modelo ARIMA ou Regressão Linear via ML.NET ou Azure ML |
| 11 | - | Calcula R² (coeficiente de determinação) para validar modelo |
| 12 | - | Se R² >= 0.85: modelo válido; senão: retorna aviso "Confiança baixa" |
| 13 | - | Gera previsões para próximos N meses com intervalo de confiança 95% |
| 14 | - | Renderiza gráfico: linha histórica + linha forecast + faixa de confiança sombreada |
| 15 | Visualiza forecast com previsões, intervalo de confiança e indicador R² | - |

### Fluxos Alternativos

**FA01 - Alterar Período de Forecast**
- **Condição:** Usuário altera período (3, 6, 12 meses)
- **Ação:** Sistema recalcula forecast para novo período

**FA02 - Comparar Forecast vs Real**
- **Condição:** Usuário seleciona "Comparar com Real" (para meses já passados)
- **Ação:** Sistema sobrepõe dados reais ao forecast para avaliar acurácia

**FA03 - Exportar Forecast**
- **Condição:** Usuário clica em "Exportar Forecast"
- **Ação:** Sistema gera Excel com: mês, valor forecast, intervalo min, intervalo max, R²

**FA04 - Atualizar Modelo**
- **Condição:** Usuário clica em "Atualizar Modelo" (força re-treinamento)
- **Ação:** Sistema executa job assíncrono para re-treinar modelo com dados atualizados

### Exceções

**EX01 - Histórico Insuficiente (< 12 meses)**
- **Condição:** Contrato possui menos de 12 meses de histórico
- **Ação:** Sistema retorna `{IsValido: false, MotivoInvalido: "Histórico insuficiente (< 12 meses)", ConfiancaPercentual: 0}`, exibe mensagem "Forecast indisponível. Aguarde 12 meses de histórico."

**EX02 - Modelo com Baixa Confiança (R² < 0.85)**
- **Condição:** R² calculado é menor que 0.85
- **Ação:** Sistema exibe forecast com aviso "Confiança baixa (R² = [valor]). Previsões podem ser imprecisas.", exibe em amarelo

**EX03 - Erro ao Treinar Modelo**
- **Condição:** Falha no treinamento do modelo ML (Azure ML indisponível, dados inconsistentes)
- **Ação:** Sistema exibe mensagem "Erro ao gerar forecast. Contate o suporte.", registra erro em log estruturado

**EX04 - Modelo Desatualizado**
- **Condição:** Última atualização do modelo > 30 dias
- **Ação:** Sistema exibe aviso "Modelo desatualizado. Recomendado re-treinar.", oferece botão "Atualizar Modelo"

### Pós-condições

- Forecast exibido com previsões mensais, intervalo de confiança e indicador R²
- Acesso registrado em AuditLog
- Modelo em cache por 30 dias (próxima atualização automática)
- Se R² < 0.85: Aviso exibido ao usuário

### Regras de Negócio Aplicáveis

- **RN-DSH-101-03**: Forecast Baseado em Série Histórica de 12+ Meses
- **RN-DSH-101-10**: Auditoria Obrigatória de Acesso a Dashboards Executivos

---

## UC05 - Exportar Dashboard em PowerPoint

### Descrição

Permite executivos exportarem dashboard consolidado em formato PowerPoint (.pptx) contendo: capa, sumário executivo, Dashboard C-Level com gráficos, Dashboard de Custos, SLA e Compliance, e análises/recomendações. Gráficos são renderizados como imagens PNG embutidas via Puppeteer/Headless Chrome. Arquivo gerado fica disponível em Azure Blob Storage por 7 dias.

### Atores

- Executivo C-Level (CEO, CFO, CIO)
- Diretoria
- Gerência Sênior
- Sistema de renderização de gráficos (Puppeteer/Headless Chrome)
- Azure Blob Storage

### Pré-condições

- Usuário autenticado no sistema
- Usuário possui permissão: `dashboard:executivo:export`
- Multi-tenancy ativo (ClienteId válido)
- Dados consolidados em FatoDashboard_Custos disponíveis
- Navegador headless (Puppeteer) configurado para renderização de gráficos

### Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa dashboard executivo (C-Level, Custos, Compliance, etc.) | - |
| 2 | Clica em botão "Exportar em PowerPoint" | - |
| 3 | - | Valida autenticação e autorização (permissão `dashboard:executivo:export`) |
| 4 | - | Registra operação em AuditLog (código: DSH_EXPORT_POWERPOINT) |
| 5 | - | Aplica filtro multi-tenancy (ClienteId) |
| 6 | - | Executa POST `/api/dashboards/executivo/export/pptx` |
| 7 | - | Coleta dados: Dashboard C-Level, Custos, SLA, Compliance |
| 8 | - | Renderiza gráficos D3.js/Highcharts como imagens PNG via Puppeteer |
| 9 | - | Gera documento PPTX usando Open XML SDK com 6 slides: Capa, Sumário, C-Level, Custos, SLA/Compliance, Recomendações |
| 10 | - | Embute imagens PNG dos gráficos nos slides |
| 11 | - | Salva arquivo em Azure Blob Storage com nome: `relatorio_executivo_{ClienteId}_{timestamp}.pptx` |
| 12 | - | Define expiração do blob: 7 dias |
| 13 | - | Gera URL de download assinada (SAS Token) válida por 7 dias |
| 14 | - | Retorna JSON: `{UrlDownload, NomeArquivo, DataGeracao, ExpiracaoEm, Tamanho}` |
| 15 | Clica em link de download e obtém arquivo PPTX | - |

### Fluxos Alternativos

**FA01 - Agendar Envio Recorrente**
- **Condição:** Usuário clica em "Agendar envio por email"
- **Ação:** Sistema exibe formulário: frequência (semanal, mensal), destinatários, horário. Cria job Hangfire para envio recorrente

**FA02 - Exportar em PDF**
- **Condição:** Usuário seleciona "Exportar em PDF" ao invés de PowerPoint
- **Ação:** Sistema executa endpoint similar: POST `/api/dashboards/executivo/export/pdf-executivo`, gera PDF via iText

**FA03 - Customizar Slides**
- **Condição:** Usuário seleciona quais dashboards incluir (C-Level, Custos, SLA, Compliance)
- **Ação:** Sistema gera PPTX apenas com slides selecionados

**FA04 - Download de Arquivo Expirado**
- **Condição:** Usuário tenta baixar após 7 dias de expiração
- **Ação:** Sistema retorna HTTP 404 Not Found, mensagem "Arquivo expirado. Gere novamente."

### Exceções

**EX01 - Erro ao Renderizar Gráficos**
- **Condição:** Puppeteer/Headless Chrome falha ao renderizar gráfico (timeout, memória)
- **Ação:** Sistema registra erro, exibe mensagem "Erro ao gerar relatório. Tente novamente.", não gera arquivo

**EX02 - Azure Blob Storage Indisponível**
- **Condição:** Falha ao salvar arquivo em Azure Blob (storage indisponível, quota excedida)
- **Ação:** Sistema registra erro, exibe mensagem "Erro ao salvar relatório. Contate o suporte."

**EX03 - Usuário Sem Permissão de Export**
- **Condição:** Usuário possui permissão `dashboard:executivo:view` mas não `dashboard:executivo:export`
- **Ação:** Sistema retorna HTTP 403 Forbidden, mensagem "Acesso negado. Permissão de exportação necessária."

**EX04 - Arquivo Muito Grande (> 50 MB)**
- **Condição:** PPTX gerado excede 50 MB (muitos gráficos de alta resolução)
- **Ação:** Sistema reduz resolução de imagens PNG (de 300 DPI para 150 DPI), regenera arquivo

### Pós-condições

- Arquivo PPTX gerado e salvo em Azure Blob Storage
- URL de download retornada ao usuário
- Expiração configurada para 7 dias
- Operação registrada em AuditLog com: UserId, ClienteId, NomeArquivo, DataExportacao
- Arquivo disponível para download imediato

### Regras de Negócio Aplicáveis

- **RN-DSH-101-09**: Export Executivo em PowerPoint com Gráficos
- **RN-DSH-101-10**: Auditoria Obrigatória de Acesso a Dashboards Executivos

---

## Histórico de Alterações

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 1.0 | 2025-12-28 | Claude Code | Versão inicial - 5 casos de uso cobrindo visualização de dashboards executivos, heatmap, forecast ML e export PowerPoint |
