# UC-RF100 - Casos de Uso - Dashboards e KPIs com Análise Preditiva

**RF Relacionado**: RF-100 - Dashboards e KPIs com Análise Preditiva (ML)
**Versão**: 1.0
**Última Atualização**: 2025-12-28
**Responsável**: Equipe de Desenvolvimento IControlIT

---

## UC01: Visualizar Forecast (Previsão) de KPI

### 1. Descrição

Este caso de uso permite que gestores visualizem previsões de KPIs (custos, receita, tickets) para 3, 6 ou 12 meses futuros, usando modelos de Machine Learning (Prophet, ARIMA) com intervalo de confiança de 95%.

### 2. Atores

- **Ator Principal**: Diretor / Gerente / Analista
- **Ator Secundário**: Sistema, Azure ML Studio

### 3. Pré-condições

- Usuário autenticado no sistema
- Usuário possui permissão: `dashboard:ml:forecast`
- Multi-tenancy ativo (ClienteId válido)
- Métrica possui mínimo 12 meses de dados históricos
- Modelo de forecast treinado e validado

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa menu Dashboards → Análise Preditiva → Forecast | - |
| 2 | Seleciona métrica desejada (ex: Custos Totais, Tickets Abertos) | - |
| 3 | Seleciona período de forecast (3, 6 ou 12 meses) | - |
| 4 | Clica em [Gerar Previsão] | - |
| 5 | - | Valida permissão `dashboard:ml:forecast` |
| 6 | - | Verifica cache Redis para forecast dessa métrica (TTL 24h) |
| 7 | - | Se não cacheado: valida mínimo 12 meses de dados históricos |
| 8 | - | Busca dados históricos (últimos 12-24 meses) com filtro multi-tenancy |
| 9 | - | Executa `POST /api/ml/forecast` enviando série temporal para Azure ML |
| 10 | - | Azure ML executa modelo Prophet com componente sazonal |
| 11 | - | Retorna previsão com intervalo de confiança 95% (banda superior/inferior) |
| 12 | - | Valida que confidence level >= 95%, senão retorna erro |
| 13 | - | Cacheia resultado no Redis (TTL 24h) |
| 14 | - | Registra operação em auditoria (FORECAST_GENERATED) |
| 15 | - | Renderiza gráfico interativo com: série histórica, série prevista, confidence bands |
| 16 | Visualiza previsão com intervalo de confiança (ex: Jan 2026: R$150k ± 8k) | - |

### 5. Fluxos Alternativos

**FA01: Comparar Múltiplos Cenários de Forecast**
- 4a. Usuário marca opção "Comparar Cenários"
- 4b. Sistema permite selecionar 2-3 métricas diferentes
- 4c. Gera forecast para todas simultaneamente
- 4d. Exibe gráficos lado-a-lado com escala normalizada
- 4e. Retorna ao passo 16

**FA02: Download de Forecast**
- 16a. Usuário clica em [📥 Exportar Previsão]
- 16b. Sistema gera Excel com abas: Dados Históricos, Previsão, Confiança, Métricas do Modelo (RMSE, MAE)
- 16c. Envia arquivo para download
- 16d. Retorna ao passo 16

**FA03: Usar Forecast Cacheado**
- 6a. Forecast para essa métrica existe em cache (< 24h)
- 6b. Sistema retorna resultado cacheado imediatamente
- 6c. Exibe timestamp de geração: "Previsão gerada há 3 horas"
- 6d. Pula para passo 15

### 6. Exceções

**EX01: Usuário sem Permissão**
- 5a. Sistema detecta falta de permissão `dashboard:ml:forecast`
- 5b. Sistema retorna HTTP 403 Forbidden
- 5c. Exibe mensagem: "Você não tem permissão para visualizar previsões"
- 5d. UC encerrado

**EX02: Dados Históricos Insuficientes**
- 7a. Métrica possui menos de 12 meses de dados
- 7b. Sistema retorna HTTP 400 Bad Request
- 7c. Exibe mensagem: "Requer mínimo 12 meses de dados históricos para forecasting. Atual: X meses."
- 7d. Sugere métricas alternativas com dados suficientes
- 7e. UC encerrado

**EX03: Confiança do Modelo Baixa**
- 12a. Modelo retorna confidence level < 95%
- 12b. Sistema rejeita previsão
- 12c. Exibe mensagem: "Previsão rejeitada: confiança abaixo de 95% (atual: X%). Dados podem estar inconsistentes."
- 12d. Sugere revisar qualidade dos dados históricos
- 12e. UC encerrado

**EX04: Erro no Azure ML**
- 10a. Falha ao executar modelo no Azure ML (timeout, quota excedida)
- 10b. Sistema retorna HTTP 500
- 10c. Exibe mensagem: "Erro ao gerar previsão. Tente novamente em alguns minutos."
- 10d. Registra erro em log para investigação
- 10e. UC encerrado

### 7. Pós-condições

- Previsão gerada e exibida com gráfico interativo
- Gráfico mostra: série histórica (últimos 12 meses), série prevista (próximos 3-12 meses), confidence bands (95%)
- Cores: linha azul (histórico), linha verde (forecast), área sombreada verde (intervalo confiança)
- Resultado cacheado no Redis (TTL 24h)
- Operação registrada em auditoria (FORECAST_GENERATED) com: métrica, período, modelo usado (Prophet/ARIMA), RMSE, MAE, usuário, timestamp

### 8. Regras de Negócio Aplicáveis

- **RN-DSH-100-01**: Forecast requer mínimo 12 meses de histórico
- **RN-DSH-100-05**: Forecast cacheado por 24h no Redis

---

## UC02: Detectar Anomalias em Tempo Real

### 1. Descrição

Este caso de uso permite que o sistema detecte automaticamente valores anômalos em KPIs usando Z-score (threshold padrão: |Z| > 3), dispare alertas em tempo real e registre anomalias para investigação.

### 2. Atores

- **Ator Principal**: Sistema (Job Automático)
- **Ator Secundário**: Usuários que recebem alertas

### 3. Pré-condições

- KPIs configurados com detecção de anomalias ativa
- Job de monitoramento ativo (execução contínua a cada 1 minuto)
- Threshold de Z-score configurado (padrão: 3.0)
- Mínimo 30 dias de dados históricos para cálculo de média/desvio

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | - | Job Hangfire executa a cada 1 minuto |
| 2 | - | Busca todos os KPIs com anomaly detection ativo |
| 3 | - | Para cada KPI: obtém valor atual em tempo real |
| 4 | - | Calcula estatísticas históricas (últimos 30 dias): média, desvio padrão |
| 5 | - | Calcula Z-score = |(valor atual - média) / desvio padrão| |
| 6 | - | Compara Z-score com threshold configurado (padrão: 3.0) |
| 7 | - | Se |Z-score| > threshold: detecta anomalia |
| 8 | - | Determina severidade: Z > 4 = Critical, Z > 3 = High, Z > 2.5 = Medium |
| 9 | - | Verifica se anomalia já foi alertada recentemente (debounce: 1 hora) |
| 10 | - | Se anomalia nova: cria registro de anomalia no banco |
| 11 | - | Envia alerta via canais configurados: email, SMS, push notification, dashboard |
| 12 | - | Atualiza dashboard em tempo real via SignalR com badge de anomalia (🔴) |
| 13 | - | Registra operação em auditoria (ANOMALY_DETECTED) |

### 5. Fluxos Alternativos

**FA01: Anomalia Resolvida Automaticamente**
- 7a. Valor do KPI volta ao intervalo normal (|Z-score| <= threshold)
- 7b. Sistema marca anomalia anterior como resolvida
- 7c. Envia notificação de resolução para usuários
- 7d. Remove badge de anomalia do dashboard
- 7e. Registra resolução em auditoria (ANOMALY_RESOLVED)
- 7f. Retorna ao passo 13

**FA02: Usar Isolation Forest para Anomalias Complexas**
- 6a. Z-score não é suficiente (dados não normalmente distribuídos)
- 6b. Sistema executa Isolation Forest (Azure ML)
- 6c. Modelo retorna score de anomalia (0-1, >0.7 = anomalia)
- 6d. Se anomalia detectada: continua no passo 7
- 6e. Senão: pula para próximo KPI (passo 2)

**FA03: Anomalia com Debounce (Já Alertada Recentemente)**
- 9a. Anomalia foi alertada há menos de 1 hora
- 9b. Sistema NÃO reenvia notificação (evita spam)
- 9c. Atualiza apenas registro existente com novo valor e Z-score
- 9d. Continua no passo 13

### 6. Exceções

**EX01: Dados Históricos Insuficientes**
- 4a. KPI possui menos de 30 dias de dados
- 4b. Sistema não consegue calcular média/desvio confiável
- 4c. Registra warning em log: "Anomaly detection desabilitado temporariamente - dados insuficientes"
- 4d. Pula para próximo KPI

**EX02: Erro ao Calcular Z-score**
- 5a. Desvio padrão = 0 (todos os valores históricos iguais)
- 5b. Z-score seria infinito (divisão por zero)
- 5c. Sistema usa método alternativo: Isolation Forest
- 5d. Continua no passo 6 (FA02)

**EX03: Falha ao Enviar Alerta**
- 11a. Tentativa de envio de email/SMS falha
- 11b. Sistema registra falha em log
- 11c. Tenta canais alternativos (push notification, dashboard)
- 11d. Registra anomalia mesmo sem notificação enviada
- 11e. Continua no passo 13

### 7. Pós-condições

- Anomalia registrada no banco com: KPI ID, valor atual, média histórica, Z-score, threshold, severidade, timestamp
- Alertas enviados via canais configurados (email, SMS, push, dashboard)
- Dashboard atualizado em tempo real com badge de anomalia (🔴 Critical, 🟡 High, 🟠 Medium)
- Operação registrada em auditoria (ANOMALY_DETECTED) com: KPI, valor, Z-score, severidade, usuários notificados
- Se anomalia resolvida: badge removido e notificação de resolução enviada

### 8. Regras de Negócio Aplicáveis

- **RN-DSH-100-02**: Anomaly detection com threshold configurável (padrão Z-score > 3)
- **RN-DSH-100-06**: Debounce de 1 hora para evitar spam de alertas

---

## UC03: Executar Clustering Inteligente de Ativos/Usuários

### 1. Descrição

Este caso de uso permite que gestores executem clustering automático (K-means, DBSCAN) para segmentar ativos ou usuários em grupos similares (3-10 clusters), recebendo recomendações customizadas por cluster.

### 2. Atores

- **Ator Principal**: Gerente / Analista de BI
- **Ator Secundário**: Sistema, Azure ML Studio

### 3. Pré-condições

- Usuário autenticado no sistema
- Usuário possui permissão: `dashboard:ml:clustering`
- Multi-tenancy ativo (ClienteId válido)
- Mínimo 50 registros para clustering (evita fragmentação excessiva)

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa menu Dashboards → Análise Preditiva → Clustering | - |
| 2 | Seleciona entidade para clusterizar (Ativos, Usuários, Clientes) | - |
| 3 | Seleciona features/variáveis (ex: Custo Mensal, Uso (GB), Tempo Ativo, Tickets Abertos) | - |
| 4 | Define número de clusters desejado (3-10, ou automático via Elbow Method) | - |
| 5 | Clica em [Executar Clustering] | - |
| 6 | - | Valida permissão `dashboard:ml:clustering` |
| 7 | - | Valida mínimo 50 registros disponíveis |
| 8 | - | Busca dados com filtro multi-tenancy (ClienteId) |
| 9 | - | Normaliza features (MinMax scaling: 0-1) |
| 10 | - | Se número de clusters = "automático": executa Elbow Method para determinar K ótimo |
| 11 | - | Executa `POST /api/ml/clustering` enviando dados para Azure ML |
| 12 | - | Azure ML executa K-means (ou DBSCAN se ruído esperado) |
| 13 | - | Retorna clusters com: ID cluster, centroid, membros, características principais |
| 14 | - | Calcula estatísticas por cluster: tamanho, % do total, média de cada feature |
| 15 | - | Gera recomendações automáticas por cluster (ex: Idle → descontinuar, High-Use → monitorar) |
| 16 | - | Registra operação em auditoria (CLUSTERING_EXECUTED) |
| 17 | - | Renderiza visualização: scatter plot (2D/3D), tabela com clusters, recomendações |
| 18 | Visualiza clusters (ex: 5 clusters: High-Use 50 ativos, Medium 150, Low 300, Idle 200, Over-Provisioned 20) | - |

### 5. Fluxos Alternativos

**FA01: Usar DBSCAN em Vez de K-means**
- 4a. Usuário marca opção "Detectar Outliers"
- 4b. Sistema usa DBSCAN em vez de K-means
- 4c. DBSCAN identifica clusters + ruído (outliers sem cluster)
- 4d. Cluster ID = -1 indica outliers
- 4e. Recomendação para outliers: investigar manualmente
- 4f. Continua no passo 12

**FA02: Elbow Method para K Ótimo**
- 10a. Usuário selecionou número de clusters = "automático"
- 10b. Sistema executa K-means para K=2 até K=10
- 10c. Calcula inércia (within-cluster sum of squares) para cada K
- 10d. Identifica "cotovelo" no gráfico (ponto de diminuição marginal)
- 10e. Sugere K ótimo (ex: K=5)
- 10f. Usuário confirma K sugerido ou ajusta manualmente
- 10g. Continua no passo 11

**FA03: Drill-Down em Cluster Específico**
- 18a. Usuário clica em cluster (ex: "Idle - 200 ativos")
- 18b. Sistema exibe lista detalhada de membros do cluster
- 18c. Para cada membro: exibe features, distância ao centroid, recomendação individual
- 18d. Permite exportar lista de membros para Excel
- 18e. Retorna ao passo 18

### 6. Exceções

**EX01: Usuário sem Permissão**
- 6a. Sistema detecta falta de permissão `dashboard:ml:clustering`
- 6b. Sistema retorna HTTP 403 Forbidden
- 6c. Exibe mensagem: "Você não tem permissão para executar clustering"
- 6d. UC encerrado

**EX02: Dados Insuficientes**
- 7a. Menos de 50 registros disponíveis
- 7b. Sistema retorna HTTP 400 Bad Request
- 7c. Exibe mensagem: "Requer mínimo 50 registros para clustering. Atual: X."
- 7d. UC encerrado

**EX03: Número de Clusters Inválido**
- 4a. Usuário define K < 3 ou K > 10
- 4b. Sistema exibe mensagem: "Número de clusters deve estar entre 3 e 10"
- 4c. Retorna ao passo 4

**EX04: Erro no Azure ML**
- 12a. Falha ao executar clustering (timeout, convergência não atingida)
- 12b. Sistema retorna HTTP 500
- 12c. Exibe mensagem: "Erro ao executar clustering. Tente reduzir número de clusters ou revisar dados."
- 12d. UC encerrado

### 7. Pós-condições

- Clustering executado e resultados armazenados
- Visualização gerada com: scatter plot (PCA redução 2D/3D), tabela de clusters, recomendações
- Para cada cluster: ID, nome sugerido (High-Use, Idle, etc.), tamanho, % do total, centroid, features médias, recomendações
- Operação registrada em auditoria (CLUSTERING_EXECUTED) com: entidade, features usadas, K, algoritmo (K-means/DBSCAN), usuário, timestamp

### 8. Regras de Negócio Aplicáveis

- **RN-DSH-100-03**: Clustering requer 3-10 clusters (evita fragmentação)
- **RN-DSH-100-04**: Mínimo 50 registros para clustering

---

## UC04: Executar What-If Analysis (Análise de Cenários)

### 1. Descrição

Este caso de uso permite que gestores criem cenários hipotéticos (aumento de tickets, redução de equipe, mudança de SLA) e visualizem impacto previsto em KPIs (custos, SLA, receita) usando modelos treinados.

### 2. Atores

- **Ator Principal**: Diretor / Gerente
- **Ator Secundário**: Sistema, Azure ML Studio

### 3. Pré-condições

- Usuário autenticado no sistema
- Usuário possui permissão: `dashboard:ml:what-if`
- Multi-tenancy ativo (ClienteId válido)
- Modelo de What-If treinado com correlações entre variáveis

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa menu Dashboards → Análise Preditiva → What-If Analysis | - |
| 2 | - | Exibe baseline atual (valores atuais de KPIs: custos, SLA, receita, tickets) |
| 3 | Define cenário hipotético: "Aumentar tickets em 20%" | - |
| 4 | Define variáveis controláveis: "Manter equipe atual" OU "Reduzir equipe em 1 pessoa" | - |
| 5 | Clica em [Simular Cenário] | - |
| 6 | - | Valida permissão `dashboard:ml:what-if` |
| 7 | - | Valida máximo 5 cenários simultâneos (evita sobrecarga) |
| 8 | - | Executa `POST /api/ml/what-if` enviando cenário para Azure ML |
| 9 | - | Azure ML aplica modelo treinado (regressão linear multivariada) |
| 10 | - | Calcula impacto em 3 dimensões: Custos (R$), SLA (%), Receita (R$) |
| 11 | - | Retorna predição com intervalo de confiança 90% |
| 12 | - | Cacheia resultado por 1 hora (Redis) |
| 13 | - | Registra operação em auditoria (WHAT_IF_EXECUTED) |
| 14 | - | Renderiza comparativo: Baseline vs Cenário (gráficos lado-a-lado, variação %) |
| 15 | Visualiza impacto: "SLA degradará de 94% para 87%, custos economizados R$2k/mês, risco churn +12%" | - |

### 5. Fluxos Alternativos

**FA01: Comparar Múltiplos Cenários**
- 5a. Usuário clica em [+ Adicionar Cenário]
- 5b. Sistema permite criar até 5 cenários simultâneos
- 5c. Calcula impacto para todos os cenários
- 5d. Exibe tabela comparativa com todos os cenários lado-a-lado
- 5e. Destaca cenário com melhor custo-benefício
- 5f. Retorna ao passo 15

**FA02: Usar Cenário Cacheado**
- 8a. Cenário idêntico foi simulado há menos de 1 hora
- 8b. Sistema retorna resultado cacheado imediatamente
- 8c. Exibe timestamp: "Simulação gerada há 25 minutos"
- 8d. Pula para passo 14

**FA03: Salvar Cenário para Referência Futura**
- 15a. Usuário clica em [💾 Salvar Cenário]
- 15b. Sistema salva cenário com nome customizado
- 15c. Permite carregar cenário salvo posteriormente
- 15d. Retorna ao passo 15

### 6. Exceções

**EX01: Usuário sem Permissão**
- 6a. Sistema detecta falta de permissão `dashboard:ml:what-if`
- 6b. Sistema retorna HTTP 403 Forbidden
- 6c. Exibe mensagem: "Você não tem permissão para executar análise de cenários"
- 6d. UC encerrado

**EX02: Limite de Cenários Excedido**
- 7a. Usuário tenta criar mais de 5 cenários simultâneos
- 7b. Sistema retorna HTTP 400 Bad Request
- 7c. Exibe mensagem: "Máximo 5 cenários simultâneos permitidos. Remova um cenário para adicionar novo."
- 7d. Retorna ao passo 3

**EX03: Cenário Inválido (Variáveis Fora do Range)**
- 8a. Variável definida está fora do range treinado (ex: aumentar tickets em 500%)
- 8b. Sistema retorna HTTP 400 Bad Request
- 8c. Exibe mensagem: "Cenário fora do range treinado. Ajuste variáveis para intervalo válido (0-200%)."
- 8d. Retorna ao passo 3

**EX04: Erro no Azure ML**
- 9a. Falha ao executar modelo (timeout, modelo não disponível)
- 9b. Sistema retorna HTTP 500
- 9c. Exibe mensagem: "Erro ao simular cenário. Tente novamente."
- 9d. UC encerrado

### 7. Pós-condições

- Cenário simulado e impacto calculado
- Comparativo exibido com: Baseline (valores atuais), Cenário (valores previstos), Variação (delta em % e absoluto)
- Para cada dimensão (Custos, SLA, Receita): exibe valor previsto com intervalo de confiança 90%
- Resultado cacheado no Redis (TTL 1h)
- Operação registrada em auditoria (WHAT_IF_EXECUTED) com: cenário definido, variáveis, resultados, usuário, timestamp

### 8. Regras de Negócio Aplicáveis

- **RN-DSH-100-07**: Máximo 5 cenários simultâneos
- **RN-DSH-100-08**: Cenários cacheados por 1 hora

---

## UC05: Visualizar Churn Prediction (Predição de Cancelamento)

### 1. Descrição

Este caso de uso permite que gestores visualizem clientes/contratos com alto risco de cancelamento (score >= 70%), baseado em modelo treinado com features (recência, frequência, NPS, tickets), recebendo recomendações automáticas de retenção.

### 2. Atores

- **Ator Principal**: Gerente Comercial / Customer Success
- **Ator Secundário**: Sistema, Azure ML Studio

### 3. Pré-condições

- Usuário autenticado no sistema
- Usuário possui permissão: `dashboard:ml:churn`
- Multi-tenancy ativo (ClienteId válido)
- Modelo de churn prediction treinado com precisão >= 70%

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa menu Dashboards → Análise Preditiva → Churn Prediction | - |
| 2 | - | Valida permissão `dashboard:ml:churn` |
| 3 | - | Executa `GET /api/ml/churn?riskLevel=high` |
| 4 | - | Busca clientes/contratos com filtro multi-tenancy |
| 5 | - | Para cada cliente: calcula features (Recência último acesso, Frequência transações, Valor gasto, NPS, Tickets suporte) |
| 6 | - | Envia features para modelo Azure ML (Random Forest treinado) |
| 7 | - | Modelo retorna churn score (0-100, >= 70 = risco alto) |
| 8 | - | Filtra apenas clientes com score >= 70 |
| 9 | - | Para cada cliente: gera recomendações automáticas (desconto, upgrade, call suporte) |
| 10 | - | Ordena por score (maior risco primeiro) |
| 11 | - | Registra operação em auditoria (CHURN_PREDICTION_VIEW) |
| 12 | - | Renderiza tabela com: Cliente, Score Churn, Features Críticas, Recomendações, Ações |
| 13 | Visualiza lista de clientes em risco (ex: Cliente ABC, Score 82%, Recomendação: Oferecer desconto 10%) | - |

### 5. Fluxos Alternativos

**FA01: Drill-Down em Cliente Específico**
- 13a. Usuário clica em cliente com score alto
- 13b. Sistema exibe detalhes: histórico de transações, NPS, tickets abertos, evolução do score (últimos 6 meses)
- 13c. Exibe gráfico de tendência do score de churn
- 13d. Lista ações recomendadas priorizadas (desconto > upgrade > call)
- 13e. Retorna ao passo 13

**FA02: Filtrar por Faixa de Risco**
- 1a. Usuário seleciona filtro de risco (Alto >= 70, Médio 40-69, Baixo < 40)
- 1b. Sistema aplica filtro na query
- 1c. Exibe apenas clientes naquela faixa
- 1d. Continua no passo 12

**FA03: Export de Lista de Risco**
- 13a. Usuário clica em [📥 Exportar]
- 13b. Sistema gera Excel com: Cliente, Score, Features, Recomendações, Contato
- 13c. Envia arquivo para download
- 13d. Retorna ao passo 13

### 6. Exceções

**EX01: Usuário sem Permissão**
- 2a. Sistema detecta falta de permissão `dashboard:ml:churn`
- 2b. Sistema retorna HTTP 403 Forbidden
- 2c. Exibe mensagem: "Você não tem permissão para visualizar churn prediction"
- 2d. UC encerrado

**EX02: Modelo de Churn Não Treinado**
- 6a. Modelo de churn não existe ou precisão < 70%
- 6b. Sistema retorna HTTP 503 Service Unavailable
- 6c. Exibe mensagem: "Modelo de churn indisponível. Aguarde retreinamento."
- 6d. UC encerrado

**EX03: Nenhum Cliente em Risco Alto**
- 8a. Nenhum cliente com score >= 70
- 8b. Sistema exibe mensagem: "Nenhum cliente com risco alto de churn. Parabéns!"
- 8c. Opção de visualizar todos os clientes (incluindo risco médio/baixo)
- 8d. UC encerrado

**EX04: Erro ao Calcular Features**
- 5a. Falha ao buscar dados do cliente (NPS, transações)
- 5b. Sistema pula esse cliente e continua com próximo
- 5c. Registra warning em log
- 5d. Continua no passo 5

### 7. Pós-condições

- Lista de clientes em risco exibida ordenada por score (maior risco primeiro)
- Para cada cliente: exibe score churn (0-100), features críticas (ex: "Sem transação há 90 dias"), recomendações priorizadas
- Operação registrada em auditoria (CHURN_PREDICTION_VIEW) com: quantidade de clientes em risco, usuário, timestamp

### 8. Regras de Negócio Aplicáveis

- **RN-DSH-100-09**: Churn prediction com precisão >= 70%
- **RN-DSH-100-10**: Threshold de risco alto = score >= 70

---

## Resumo dos Casos de Uso

| UC | Nome | Ator Principal | Complexidade | Integração |
|----|------|----------------|--------------|------------|
| UC01 | Visualizar Forecast (Previsão) de KPI | Diretor/Gerente | Muito Alta | Azure ML, Prophet/ARIMA, Redis Cache |
| UC02 | Detectar Anomalias em Tempo Real | Sistema (Job) | Alta | Z-score, Isolation Forest, SignalR |
| UC03 | Executar Clustering Inteligente | Gerente/Analista | Alta | K-means, DBSCAN, Azure ML |
| UC04 | Executar What-If Analysis | Diretor/Gerente | Muito Alta | Regressão Multivariada, Redis Cache |
| UC05 | Visualizar Churn Prediction | Gerente Comercial | Alta | Random Forest, Azure ML |

---

**Última Atualização**: 2025-12-28
**Versão do Documento**: 1.0
**Status**: ✅ Completo
