# UC-RF094 - Casos de Uso - Auditoria de Custos e Compliance

## UC01: Analisar Custos Multidimensionalmente com Drill-Down Interativo

### 1. Descrição

Este caso de uso permite que Gestores e Auditores analisem despesas agrupadas por múltiplas dimensões (fornecedor, categoria, departamento, período, filial) com drill-down interativo, filtros dinâmicos e visualizações gráficas para identificar oportunidades de economia.

### 2. Atores

- Gestor Financeiro
- Auditor
- Controller
- Sistema

### 3. Pré-condições

- Usuário autenticado
- Permissão: `auditoria:custos:read` ou `auditoria:admin:full`
- Dados de custos disponíveis (faturas, contratos, ativos)
- Multi-tenancy ativo (ClienteId válido)

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa menu Auditoria → Análise de Custos | - |
| 2 | - | Valida permissão `auditoria:custos:read` |
| 3 | - | Aplica filtro multi-tenancy (ClienteId) |
| 4 | - | Exibe dashboard com 3 seções: Filtros, Dimensões, Visualizações |
| 5 | - | **Seção Filtros**: Período (date range picker, padrão últimos 12 meses), Fornecedor (multi-select autocomplete), Categoria (multi-select), Centro de Custo (multi-select), Filial (multi-select) |
| 6 | Seleciona filtros: Período = Jan/2025 a Dez/2025, Categoria = "Telecom" | - |
| 7 | - | **Seção Dimensões**: Radio buttons: Agrupar por Fornecedor, Categoria, Departamento, Filial, Período (Mês) |
| 8 | Seleciona: Agrupar por Fornecedor | - |
| 9 | - | Executa `GET /api/auditoria/custos/analisar?periodo=2025-01-01:2025-12-31&categoria=Telecom&agruparPor=Fornecedor&clienteId={clienteId}` |
| 10 | - | Consulta banco com agregação: `SELECT FornecedorId, SUM(ValorTotal) AS TotalGasto, COUNT(*) AS QtdFaturas FROM Faturas WHERE ClienteId = {id} AND DataEmissao BETWEEN '2025-01-01' AND '2025-12-31' AND Categoria = 'Telecom' GROUP BY FornecedorId ORDER BY TotalGasto DESC` |
| 11 | - | Retorna: `[{ fornecedorId, fornecedorNome, totalGasto, qtdFaturas, percentualTotal }]` |
| 12 | - | **Seção Visualizações**: Exibe 3 gráficos: (1) Bar Chart Horizontal - Top 10 Fornecedores por Gasto, (2) Pie Chart - Distribuição Percentual, (3) Tabela Detalhada - Fornecedor, Total Gasto, Qtd Faturas, % do Total, Ações (Drill-Down) |
| 13 | - | Renderiza gráficos com Chart.js ou Highcharts |
| 14 | Identifica fornecedor com maior gasto: "Vivo Telecom" - R$ 500.000 (45% do total) | - |
| 15 | Clica em barra do gráfico "Vivo Telecom" para drill-down | - |
| 16 | - | Executa drill-down: Aplica filtro adicional Fornecedor = Vivo, re-agrupa por Categoria |
| 17 | - | Novo gráfico exibido: Categorias de gasto da Vivo (Voz R$ 200k, Dados R$ 250k, SMS R$ 50k) |
| 18 | Clica em categoria "Dados" para drill-down nível 2 | - |
| 19 | - | Re-agrupa por Filial: Filial SP R$ 150k, Filial RJ R$ 100k |
| 20 | - | Breadcrumb exibido: "Todos > Vivo Telecom > Dados > Filial SP" com botões de voltar |
| 21 | Clica em botão "Exportar Análise" | - |
| 22 | - | Executa `GET /api/auditoria/custos/exportar?formato=excel` |
| 23 | - | Gera arquivo Excel com 3 abas: (1) Resumo Executivo, (2) Detalhamento por Fornecedor, (3) Drill-Down Filial |
| 24 | - | Auditoria registrada (AUDITORIA_CUSTOS_EXPORTADA) com ClienteId, Usuario, Periodo, Formato |
| 25 | - | Download iniciado automaticamente |

### 5. Fluxos Alternativos

**FA01: Comparar Períodos (Análise Temporal)**
- Usuário seleciona "Comparar Períodos" no filtro
- Define Período 1: Jan-Jun/2025, Período 2: Jul-Dez/2025
- Sistema exibe gráfico de linha comparativa: Custo por Mês em ambos períodos
- Calcula crescimento percentual: Jul-Dez 15% maior que Jan-Jun
- Badge exibido: "Crescimento: +15% no segundo semestre"

**FA02: Identificar Top 5 Maiores Gastos**
- Sistema calcula automaticamente Top 5 Fornecedores com maior custo total
- Exibe cards destacados: Fornecedor 1 (R$ 500k), Fornecedor 2 (R$ 300k), etc.
- Botão "Ver Detalhes" em cada card abre drill-down específico

**FA03: Aplicar Filtro por Valor Mínimo**
- Usuário define: "Mostrar apenas gastos > R$ 10.000"
- Sistema aplica filtro: `WHERE ValorTotal > 10000`
- Tabela atualizada exibindo apenas faturas acima do threshold

### 6. Exceções

**EX01: Permissão Negada**
- Se usuário sem permissão `auditoria:custos:read` → HTTP 403 Forbidden
- Mensagem: "Você não tem permissão para acessar análise de custos"

**EX02: Nenhum Dado Encontrado**
- Se filtros não retornam resultados → HTTP 200 OK com array vazio
- Mensagem exibida: "Nenhum custo encontrado com os filtros selecionados. Tente ajustar período ou categorias."

**EX03: Timeout em Query Complexa**
- Se query com múltiplas dimensões excede 30 segundos → HTTP 504 Gateway Timeout
- Sistema sugere: "Reduza o período de análise ou agrupe por menos dimensões"

**EX04: Exportação Muito Grande**
- Se exportação Excel excede 1 milhão de linhas → HTTP 413 Payload Too Large
- Sistema oferece: "Exportar em múltiplos arquivos" ou "Aplicar filtros adicionais"

### 7. Pós-condições

- Dashboard exibindo custos agregados por dimensão selecionada
- Gráficos interativos renderizados com drill-down funcional
- Exportação disponível em Excel, PDF ou CSV
- Auditoria registrada (AUDITORIA_CUSTOS_ACESSADA)

### 8. Regras de Negócio Aplicáveis

- **RN-AUD-094-05**: Análise Multidimensional (Fornecedor, Categoria, Departamento, Filial, Período)
- **RN-AUD-094-06**: Drill-Down em até 3 níveis (ex: Fornecedor → Categoria → Filial)
- **RN-AUD-094-08**: Auditoria de Acesso com LGPD (rastreamento de exportações)

---

## UC02: Detectar Anomalias em Transações Usando Z-Score e Machine Learning

### 1. Descrição

Este caso de uso permite que o Sistema identifique automaticamente transações atípicas (outliers) usando Z-Score (desvio padrão > 2.5) e algoritmos de Machine Learning (Isolation Forest), gerando alertas para revisão de auditores.

### 2. Atores

- Sistema
- Auditor (revisão de anomalias)

### 3. Pré-condições

- Dados históricos de transações disponíveis (mínimo 90 dias)
- Hangfire job DeteccaoAnomaliaJob agendado
- Multi-tenancy ativo (ClienteId válido)
- Modelo ML treinado (Isolation Forest ou Prophet)

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | - | Hangfire job DeteccaoAnomaliaJob executa diariamente às 4h AM |
| 2 | - | Consulta transações dos últimos 30 dias: `SELECT * FROM Faturas WHERE ClienteId = {id} AND DataEmissao >= DATEADD(DAY, -30, GETDATE())` |
| 3 | - | Calcula estatísticas: Média (μ), Desvio Padrão (σ) para cada categoria de custo |
| 4 | - | Exemplo: Categoria "Telecom" → μ = R$ 10.000, σ = R$ 2.000 |
| 5 | - | Para cada transação, calcula Z-Score: `z = (valor - μ) / σ` |
| 6 | - | Transação R$ 18.000 → z = (18.000 - 10.000) / 2.000 = 4.0 |
| 7 | - | Se `|z| > 2.5` → Marca como anomalia potencial |
| 8 | - | Cria registro AnomaliaDetectada com: TransacaoId, TipoDeteccao = "Z-Score", ValorZ, Severidade (Alta se z > 3.0, Média se 2.5 < z < 3.0) |
| 9 | - | **Machine Learning - Isolation Forest**: Serializa transações para formato JSON: `[{ valor, categoria, fornecedorId, filialId, dia_semana }]` |
| 10 | - | Envia para API Python/Scikit-learn ou Azure ML: `POST /ml/detect-anomalies` |
| 11 | - | Modelo retorna score de anomalia (0-1): Valores próximos de 1 = alta probabilidade de anomalia |
| 12 | - | Se score > 0.8 → Marca como anomalia com TipoDeteccao = "IsolationForest" |
| 13 | - | Cria alerta AnomaliaAlerta com: AnomaliaId, Severidade, Mensagem = "Transação atípica detectada - Valor 4x acima da média", AcaoRecomendada = "Revisar fatura e contrato" |
| 14 | - | Auditoria registrada (ANOMALIA_DETECTADA) com ClienteId, AnomaliaId, TipoDeteccao, ValorZ, ScoreML |
| 15 | - | Notificação enviada para auditor via SignalR: "3 anomalias detectadas. Revisar pendências." |
| 16 | - | Dashboard atualizado com badge vermelho: "3 Anomalias Pendentes" |
| 17 | Auditor acessa Auditoria → Anomalias Detectadas | - |
| 18 | - | Valida permissão `auditoria:anomalias:read` |
| 19 | - | Exibe grid paginado: Transação, Fornecedor, Valor, Z-Score, Score ML, Severidade, Data Detecção, Status (Pendente/Revisada/Falso Positivo), Ações |
| 20 | Seleciona anomalia para revisar | - |
| 21 | Clica em "Ver Detalhes" | - |
| 22 | - | Executa `GET /api/auditoria/anomalias/{id}` |
| 23 | - | Exibe modal com: Dados da Transação, Histórico do Fornecedor (média últimos 6 meses), Gráfico de Distribuição (mostrando outlier), Classificação Z-Score, Score ML, Comentários |
| 24 | Analisa gráfico e identifica que valor realmente é atípico | - |
| 25 | Clica em "Marcar como Anomalia Verdadeira" | - |
| 26 | Preenche Comentário: "Valor diverge significativamente do contrato. Solicitar revisão ao fornecedor." | - |
| 27 | - | Executa `POST /api/auditoria/anomalias/{id}/confirmar` com { comentario, acaoTomada } |
| 28 | - | Atualiza anomalia: Status = Confirmada, Revisor = usuarioId, DataRevisao = DateTime.UtcNow |
| 29 | - | Cria tarefa no sistema: "Revisar fatura #{numero} com fornecedor - Valor atípico R$ 18.000" |
| 30 | - | Auditoria registrada (ANOMALIA_CONFIRMADA) |
| 31 | - | HTTP 200 OK retornado |

### 5. Fluxos Alternativos

**FA01: Marcar como Falso Positivo**
- Auditor identifica que valor alto é justificado (ex: compra extraordinária aprovada)
- Clica em "Marcar como Falso Positivo"
- Preenche Justificativa: "Compra extraordinária de equipamentos conforme aprovação DIR-2025-001"
- Sistema atualiza Status = FalsoPositivo
- Modelo ML retreinado para reduzir falsos positivos futuros

**FA02: Detectar Padrão Sazonal (Prophet)**
- Sistema usa algoritmo Prophet (Facebook) para séries temporais
- Identifica sazonalidade: Gastos sempre aumentam 20% em dezembro (férias)
- Ajusta threshold dinâmico: Em dezembro, z > 3.5 para anomalia (ao invés de 2.5)
- Reduz falsos positivos em períodos sazonais

**FA03: Alertar Anomalia em Tempo Real (Transação Sendo Criada)**
- Durante criação de fatura via API
- Sistema valida valor contra média histórica
- Se valor > 3σ → Exibe warning modal: "Atenção: Valor 3x acima da média. Confirmar?"
- Usuário pode prosseguir ou revisar

### 6. Exceções

**EX01: Modelo ML Indisponível**
- Se API Python/Azure ML falha (timeout ou HTTP 503) → Loga erro
- Continua detecção apenas com Z-Score
- Marca registros com flag MLNotAnalyzed = true
- Notificação para TI: "Modelo ML indisponível. Detecção degradada."

**EX02: Dados Históricos Insuficientes**
- Se menos de 90 dias de histórico → Não calcula Z-Score (desvio padrão não confiável)
- Mensagem: "Aguardando dados históricos suficientes para detecção de anomalias"

**EX03: Desvio Padrão Zero (Todos Valores Iguais)**
- Se σ = 0 (todos valores idênticos) → Divisão por zero
- Sistema trata: Se valor atual != μ → Anomalia automática
- Se valor atual == μ → Normal

**EX04: Threshold Configurável por Cliente**
- Alguns clientes preferem threshold mais conservador (z > 2.0) ou liberal (z > 3.5)
- Administrador acessa Configurações → Detecção de Anomalias → Altera threshold
- Sistema respeita configuração por ClienteId

### 7. Pós-condições

- Anomalias detectadas e registradas em AnomaliaDetectada
- Alertas criados para auditores
- Auditoria registrada (ANOMALIA_DETECTADA)
- Notificações enviadas via SignalR e email
- Dashboard atualizado com badge de pendências

### 8. Regras de Negócio Aplicáveis

- **RN-AUD-094-02**: Detecção de Anomalias por Z-Score (threshold > 2.5)
- **RN-AUD-094-03**: Machine Learning com Isolation Forest (score > 0.8)
- **RN-AUD-094-04**: Classificação de Severidade (Alta se z > 3.0, Média se 2.5 < z < 3.0)

---

## UC03: Calcular e Analisar Variância entre Custo Planejado e Realizado

### 1. Descrição

Este caso de uso permite que Gestores Financeiros comparem custo orçado (planejado) com custo efetivo (realizado), calculem variância absoluta e percentual, classifiquem desvios (Aceitável, Aviso, Crítico) e identifiquem áreas que requerem ação.

### 2. Atores

- Gestor Financeiro
- Controller
- Sistema

### 3. Pré-condições

- Usuário autenticado
- Permissão: `auditoria:variancia:read` ou `auditoria:admin:full`
- Orçamento cadastrado por período e centro de custo
- Dados de custos realizados disponíveis
- Multi-tenancy ativo (ClienteId válido)

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa menu Auditoria → Análise de Variância | - |
| 2 | - | Valida permissão `auditoria:variancia:read` |
| 3 | - | Aplica filtro multi-tenancy (ClienteId) |
| 4 | - | Exibe formulário com: Período (date picker, padrão mês corrente), Centro de Custo (multi-select), Categoria (multi-select) |
| 5 | Seleciona: Período = Jan/2025, Centro de Custo = TI | - |
| 6 | Clica em "Analisar Variância" | - |
| 7 | - | Executa `GET /api/auditoria/variancia?periodo=2025-01&centroCusto=TI&clienteId={clienteId}` |
| 8 | - | Consulta orçamento: `SELECT * FROM Orcamento WHERE ClienteId = {id} AND Periodo = '2025-01' AND CentroCustoId = {tiId}` |
| 9 | - | Retorna: CustoPlano = R$ 10.000 |
| 10 | - | Consulta custo realizado: `SELECT SUM(ValorTotal) FROM Faturas WHERE ClienteId = {id} AND DataEmissao BETWEEN '2025-01-01' AND '2025-01-31' AND CentroCustoId = {tiId}` |
| 11 | - | Retorna: CustoRealizado = R$ 10.500 |
| 12 | - | Calcula variância absoluta: `varianc = custoRealizado - custoPlano = 10.500 - 10.000 = R$ 500` |
| 13 | - | Calcula variância percentual: `variancPerc = (variancia / custoPlano) × 100 = (500 / 10.000) × 100 = 5%` |
| 14 | - | Classifica variância: `|5%| <= 5% → "Aceitável"` |
| 15 | - | Exibe dashboard com 3 seções: (1) KPIs - Cards: Custo Plano (R$ 10k), Custo Realizado (R$ 10,5k), Variância (R$ 500), Variância % (5%), Classificação (badge verde "Aceitável"), (2) Gráfico Comparativo - Bar chart lado a lado: Plano vs Realizado, (3) Tabela Detalhada - Por subcategoria com drill-down |
| 16 | - | Tabela exibe linhas: Subcategoria Telecom → Plano R$ 3k, Realizado R$ 3,5k, Variância R$ 500 (16,7%) - Aviso (badge amarelo) |
| 17 | Identifica subcategoria Telecom com variância 16,7% (Aviso) | - |
| 18 | Clica em linha "Telecom" para drill-down | - |
| 19 | - | Detalha por fornecedor: Vivo → Plano R$ 2k, Realizado R$ 2,8k, Variância R$ 800 (40%) - Crítico (badge vermelho) |
| 20 | - | Exibe alerta: "Variância crítica detectada (40%). Ação recomendada: Revisar contrato com Vivo e negociar valores." |
| 21 | Clica em botão "Gerar Relatório de Variância" | - |
| 22 | - | Executa `GET /api/auditoria/variancia/relatorio?periodo=2025-01&centroCusto=TI&formato=pdf` |
| 23 | - | Gera PDF com: (1) Sumário Executivo (Total Plano, Realizado, Variância), (2) Análise por Categoria, (3) Drill-Down Subcategorias com Variância > 10%, (4) Recomendações de Ação |
| 24 | - | Auditoria registrada (VARIANCIA_RELATORIO_GERADO) com Periodo, CentroCustoId, Formato |
| 25 | - | Download iniciado |

### 5. Fluxos Alternativos

**FA01: Detectar Economia (Variância Negativa)**
- Sistema calcula: Plano R$ 10k, Realizado R$ 8,5k
- Variância = -R$ 1,5k (-15%)
- Badge verde exibido: "Economia de R$ 1.500"
- Mensagem: "Parabéns! Economia de 15% em relação ao orçado."

**FA02: Variância Crítica Acima de 15%**
- Sistema calcula: Plano R$ 10k, Realizado R$ 12k
- Variância = R$ 2k (20%) → Classificação "Crítico"
- Badge vermelho piscante: "Ação Urgente Requerida"
- Sistema cria automaticamente tarefa: "Investigar variância crítica em Centro de Custo TI - Jan/2025"
- Notificação enviada para Diretor Financeiro

**FA03: Comparar Variância Entre Períodos**
- Usuário seleciona "Comparar com Período Anterior"
- Sistema calcula variância de Jan/2025 vs Dez/2024
- Exibe gráfico de linha: Tendência de variância últimos 6 meses
- Identifica padrão: Variância aumentando progressivamente (requer ação preventiva)

### 6. Exceções

**EX01: Permissão Negada**
- Se usuário sem permissão `auditoria:variancia:read` → HTTP 403 Forbidden
- Mensagem: "Você não tem permissão para acessar análise de variância"

**EX02: Orçamento Não Cadastrado**
- Se não existe orçamento para período selecionado → HTTP 404 Not Found
- Mensagem: "Orçamento não cadastrado para período {mes/ano}. Configure orçamento antes de analisar variância."

**EX03: Custo Plano Zero (Divisão por Zero)**
- Se custoPlano = 0 → Variância percentual não pode ser calculada
- Sistema exibe: "Variância: R$ {valor} (percentual indisponível - orçamento zerado)"

**EX04: Múltiplos Centros de Custo com Variância Crítica**
- Se 5+ centros com variância > 15% → Dashboard exibe alerta global
- Mensagem: "Atenção: Variância crítica em múltiplas áreas. Revisar orçamento global."

### 7. Pós-condições

- Variância calculada e classificada (Aceitável, Aviso, Crítico)
- Dashboard exibindo KPIs, gráficos e tabela detalhada
- Relatório PDF gerado (se solicitado)
- Auditoria registrada (VARIANCIA_ANALISADA)
- Tarefas criadas para variâncias críticas

### 8. Regras de Negócio Aplicáveis

- **RN-AUD-094-01**: Cálculo de Variância (Absoluta e Percentual)
- **RN-AUD-094-02**: Classificação (|var%| <= 5% = Aceitável, <= 15% = Aviso, > 15% = Crítico)
- **RN-AUD-094-05**: Drill-Down por Categoria → Subcategoria → Fornecedor

---

## UC04: Verificar Conformidade com Políticas Corporativas e Gerar Alertas

### 1. Descrição

Este caso de uso permite que o Sistema verifique automaticamente conformidade de transações com políticas corporativas (limites de gasto, fornecedores aprovados, contratos vigentes), identifique violações e gere alertas com severidade classificada.

### 2. Atores

- Sistema
- Gestor de Compliance
- Auditor

### 3. Pré-condições

- Políticas corporativas configuradas (RF-079)
- Dados de transações, contratos e fornecedores disponíveis
- Hangfire job VerificacaoConformidadeJob agendado
- Multi-tenancy ativo (ClienteId válido)

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | - | Hangfire job VerificacaoConformidadeJob executa diariamente às 6h AM |
| 2 | - | Consulta políticas corporativas ativas: `SELECT * FROM PoliticasCorporativas WHERE ClienteId = {id} AND Ativa = TRUE` |
| 3 | - | Para cada política, executa verificação conforme tipo |
| 4 | - | **Tipo 1: Limite de Gasto por Filial** - Consulta gastos do mês corrente: `SELECT FilialId, SUM(ValorTotal) AS TotalGasto FROM Faturas WHERE ClienteId = {id} AND DataEmissao >= DATEADD(MONTH, -1, GETDATE()) GROUP BY FilialId` |
| 5 | - | Exemplo: Filial SP → Total Gasto R$ 250.000 |
| 6 | - | Compara com limite da política: Limite SP = R$ 200.000 |
| 7 | - | Se TotalGasto > Limite → Cria AlertaConformidade com Tipo = LimiteGastoExcedido, Severidade = Alta, Mensagem = "Filial SP excedeu limite mensal em R$ 50.000 (125%)", AcaoRecomendada = "Revisar faturas e aprovar exceção ou ajustar orçamento" |
| 8 | - | **Tipo 2: Fornecedor Não Aprovado** - Consulta faturas com fornecedores não cadastrados em lista aprovada: `SELECT * FROM Faturas f WHERE ClienteId = {id} AND NOT EXISTS (SELECT 1 FROM FornecedoresAprovados fa WHERE fa.FornecedorId = f.FornecedorId)` |
| 9 | - | Se encontrado → Cria AlertaConformidade com Tipo = FornecedorNaoAprovado, Severidade = Crítica, Mensagem = "Fatura emitida por fornecedor não aprovado: {razaoSocial}", AcaoRecomendada = "Solicitar aprovação ou cancelar contrato" |
| 10 | - | **Tipo 3: Contrato Próximo do Vencimento** - Consulta contratos com vencimento < 30 dias: `SELECT * FROM Contratos WHERE ClienteId = {id} AND DataVencimento >= GETDATE() AND DataVencimento < DATEADD(DAY, 30, GETDATE()) AND Status != 'Renovado'` |
| 11 | - | Se encontrado → Cria AlertaConformidade com Tipo = ContratoProximoVencimento, Severidade = Média, Mensagem = "Contrato {numero} vence em {dias} dias", AcaoRecomendada = "Renovar ou renegociar contrato" |
| 12 | - | Auditoria registrada (CONFORMIDADE_VERIFICADA) com TotalAlertas, AlertasCriticos, AlertasAltos |
| 13 | - | Notificação enviada para Gestor de Compliance: "Verificação de conformidade concluída. 5 alertas detectados (2 críticos)." |
| 14 | Gestor de Compliance acessa Auditoria → Alertas de Conformidade | - |
| 15 | - | Valida permissão `auditoria:conformidade:read` |
| 16 | - | Exibe grid paginado: Tipo, Severidade (badge colorido), Mensagem, Data Detecção, Ação Recomendada, Status (Pendente/Revisado/Resolvido), Ações |
| 17 | Seleciona alerta "Filial SP excedeu limite" | - |
| 18 | Clica em "Ver Detalhes" | - |
| 19 | - | Executa `GET /api/auditoria/alertas/{id}` |
| 20 | - | Exibe modal com: Detalhes do Alerta, Política Violada, Dados da Transação/Contrato, Histórico de Alertas Similares, Comentários |
| 21 | Analisa e decide: Aprovar exceção | - |
| 22 | Clica em "Aprovar Exceção" | - |
| 23 | Preenche Justificativa: "Compras extraordinárias aprovadas pela diretoria. Exceção válida para Jan/2025." | - |
| 24 | - | Executa `POST /api/auditoria/alertas/{id}/aprovar-excecao` com { justificativa } |
| 25 | - | Atualiza alerta: Status = Resolvido (Exceção Aprovada), Revisor = usuarioId, DataRevisao = DateTime.UtcNow |
| 26 | - | Auditoria registrada (ALERTA_EXCECAO_APROVADA) com AlertaId, Revisor, Justificativa |
| 27 | - | HTTP 200 OK retornado |

### 5. Fluxos Alternativos

**FA01: Escalar Alerta Crítico Não Resolvido**
- Sistema identifica alerta crítico pendente por > 48 horas
- Executa escalação automática: Envia notificação para Diretor Financeiro
- Cria tarefa urgente no sistema: "Revisar alerta crítico não resolvido - {mensagem}"
- Badge vermelho piscante no dashboard

**FA02: Configurar Nova Política Corporativa**
- Gestor acessa Configurações → Políticas Corporativas
- Clica em "Nova Política"
- Define: Tipo = Limite de Gasto, Entidade = Filial RJ, Limite = R$ 150.000, Período = Mensal
- Sistema valida e salva
- Próxima execução do job verifica nova política

**FA03: Marcar Alerta como Falso Positivo**
- Gestor identifica que alerta foi gerado incorretamente
- Clica em "Marcar como Falso Positivo"
- Preenche Motivo: "Política desatualizada. Limite foi ajustado em reunião de orçamento."
- Sistema atualiza Status = Resolvido (Falso Positivo)
- Sugestão exibida: "Atualizar política para evitar futuros falsos positivos?"

### 6. Exceções

**EX01: Permissão Negada**
- Se usuário sem permissão `auditoria:conformidade:read` → HTTP 403 Forbidden
- Mensagem: "Você não tem permissão para acessar alertas de conformidade"

**EX02: Nenhuma Política Configurada**
- Se não existem políticas ativas → Job executa sem criar alertas
- Loga warning: "Nenhuma política corporativa configurada para ClienteId {id}. Verificação de conformidade pulada."

**EX03: Justificativa de Exceção Muito Curta**
- Se justificativa tem menos de 30 caracteres → HTTP 400 Bad Request
- Mensagem: "Justificativa deve ter no mínimo 30 caracteres para aprovação de exceção"

**EX04: Múltiplos Alertas Críticos Simultâneos**
- Se 10+ alertas críticos criados simultaneamente → Dashboard exibe alerta global
- Notificação urgente para Compliance e Diretoria
- Email enviado com sumário executivo e lista de ações requeridas

### 7. Pós-condições

- Alertas de conformidade criados e classificados por severidade
- Notificações enviadas para gestores responsáveis
- Auditoria registrada (CONFORMIDADE_VERIFICADA)
- Dashboard atualizado com badges de alertas pendentes
- Exceções aprovadas ou alertas resolvidos

### 8. Regras de Negócio Aplicáveis

- **RN-AUD-094-07**: Alertas de Não-Conformidade (Limite Gasto, Fornecedor Não Aprovado, Contrato Vencendo)
- **RN-AUD-094-08**: Classificação de Severidade (Crítica, Alta, Média, Baixa)
- **RN-AUD-094-09**: Escalação automática de alertas críticos não resolvidos em 48 horas

---

## UC05: Auditar Acessos e Exportações com Retenção LGPD de 7 Anos

### 1. Descrição

Este caso de uso permite que o Sistema registre automaticamente todas as operações de leitura, modificação e exportação de dados de auditoria com usuário, timestamp, IP e dados acessados, garantindo rastreabilidade LGPD com retenção de 7 anos.

### 2. Atores

- Sistema (registro automático)
- Administrador (consulta de auditoria)
- DPO (Data Protection Officer)

### 3. Pré-condições

- Middleware de auditoria configurado
- Multi-tenancy ativo (ClienteId válido)
- Tabela AuditoriaLGPD criada

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Usuário executa qualquer operação de auditoria (ex: Exportar relatório de custos) | - |
| 2 | - | Middleware AuditoriaLGPDMiddleware intercepta requisição HTTP |
| 3 | - | Captura dados: Usuario (ClaimsPrincipal.Identity.Name), Operacao (EXPORT), Recurso ("Relatório Custos"), IpAddress (HttpContext.Connection.RemoteIpAddress), DadosAcessados (parâmetros da requisição) |
| 4 | - | Cria registro RegistroAuditoria com: Id (Guid), ClienteId, Usuario, Operacao, Recurso, IpAddress, Timestamp (DateTime.UtcNow), DadosAcessados (JSON), FlExcluido = false |
| 5 | - | Persiste em tabela AuditoriaLGPD: `INSERT INTO AuditoriaLGPD (...) VALUES (...)` |
| 6 | - | Agenda job de limpeza: `Hangfire.Schedule<LimpezaAuditoriaLGPDJob>(x => x.LimparRegistrosAntigos(clienteId, DateTime.UtcNow.AddYears(7)), TimeSpan.FromDays(7 * 365))` |
| 7 | - | Continua processamento normal da requisição |
| 8 | - | Retorna resposta para usuário (ex: arquivo exportado) |
| 9 | Administrador ou DPO acessa Auditoria → Logs LGPD | - |
| 10 | - | Valida permissão `auditoria:lgpd:read` (permissão restrita) |
| 11 | - | Aplica filtro multi-tenancy (ClienteId) |
| 12 | - | Exibe grid com filtros: Usuário (autocomplete), Operação (READ, MODIFY, EXPORT, DELETE), Recurso (text search), Período (date range) |
| 13 | Filtra: Operacao = EXPORT, Período = Últimos 30 dias | - |
| 14 | - | Executa `GET /api/auditoria/lgpd?operacao=EXPORT&periodo=2025-12-01:2025-12-29&clienteId={clienteId}` |
| 15 | - | Consulta: `SELECT * FROM AuditoriaLGPD WHERE ClienteId = {id} AND Operacao = 'EXPORT' AND Timestamp >= '2025-12-01' AND FlExcluido = FALSE ORDER BY Timestamp DESC` |
| 16 | - | Retorna lista paginada (pageSize = 50) |
| 17 | - | Tabela exibe: Usuário, Operação, Recurso, IP, Timestamp, Dados Acessados (resumo), Ações (Ver Detalhes) |
| 18 | Seleciona registro específico | - |
| 19 | Clica em "Ver Detalhes" | - |
| 20 | - | Executa `GET /api/auditoria/lgpd/{id}` |
| 21 | - | Exibe modal com: Usuario, Operacao, Recurso, IpAddress, Timestamp, DadosAcessados (JSON completo formatado), DadosAntigos (se MODIFY), DadosNovos (se MODIFY) |
| 22 | - | Auditoria de auditoria (meta-auditoria): Registra que Administrador acessou log LGPD |
| 23 | - | HTTP 200 OK retornado |

### 5. Fluxos Alternativos

**FA01: Exportar Logs de Auditoria para Compliance**
- DPO clica em "Exportar Logs LGPD"
- Seleciona formato: CSV
- Define período: Últimos 12 meses
- Sistema executa `GET /api/auditoria/lgpd/exportar?formato=csv&periodo=2024-12-29:2025-12-29`
- Gera CSV com todas as colunas: Id, ClienteId, Usuario, Operacao, Recurso, IpAddress, Timestamp, DadosAcessados
- Download iniciado
- Meta-auditoria registrada: "DPO exportou logs LGPD para compliance"

**FA02: Limpeza Automática Após 7 Anos (LGPD)**
- Hangfire job LimpezaAuditoriaLGPDJob executa conforme agendamento (7 anos após criação)
- Consulta registros com Timestamp < (DateTime.UtcNow - 7 anos)
- Executa soft delete: `UPDATE AuditoriaLGPD SET FlExcluido = TRUE WHERE Timestamp < {7_anos_atras}`
- Loga: "Limpeza LGPD executada. {N} registros marcados como excluídos."
- Hard delete executado após 30 dias adicionais (retention buffer)

**FA03: Alertar Acesso Anômalo (Múltiplas Exportações em Curto Período)**
- Sistema detecta: Mesmo usuário exportou 10+ relatórios em 1 hora
- Cria alerta: "Possível acesso anômalo detectado - Usuário {nome}"
- Notificação enviada para DPO e Segurança
- Requer justificativa do usuário

### 6. Exceções

**EX01: Permissão Negada**
- Se usuário sem permissão `auditoria:lgpd:read` → HTTP 403 Forbidden
- Mensagem: "Você não tem permissão para acessar logs de auditoria LGPD"

**EX02: Tabela AuditoriaLGPD Corrompida**
- Se falha ao inserir registro (ex: database offline) → Loga erro em arquivo local
- Continua processamento normal (não bloqueia operação do usuário)
- Alerta enviado para TI: "Auditoria LGPD falhou. Verificar database."

**EX03: Exportação LGPD Excede Limite de Tamanho**
- Se exportação CSV excede 100 MB → HTTP 413 Payload Too Large
- Sistema oferece: "Exportar em múltiplos arquivos por ano" ou "Aplicar filtros adicionais"

**EX04: Tentativa de Deletar Log de Auditoria (Proibido)**
- Se usuário tenta executar DELETE manual → HTTP 403 Forbidden
- Mensagem: "Logs de auditoria LGPD são imutáveis. Apenas soft delete automático após 7 anos é permitido."

### 7. Pós-condições

- Todas as operações registradas automaticamente em AuditoriaLGPD
- Retenção de 7 anos garantida via soft delete programado
- Logs acessíveis para DPO e auditores autorizados
- Meta-auditoria registrada (acesso a logs)
- Compliance LGPD garantido

### 8. Regras de Negócio Aplicáveis

- **RN-AUD-094-08**: Auditoria de Acesso com LGPD (usuário, timestamp, IP, dados acessados)
- **RN-AUD-094-09**: Retenção mínima de 7 anos conforme LGPD artigo 7°
- **RN-AUD-094-10**: Soft delete após 7 anos, hard delete após 7 anos + 30 dias
- **RN-AUD-094-11**: Meta-auditoria (registrar acesso a logs de auditoria)
