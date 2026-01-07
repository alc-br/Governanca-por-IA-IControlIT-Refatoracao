# Casos de Uso - RF103: Relatórios e Volumetria

**Versão:** 1.0
**Data:** 2025-12-28
**RF Relacionado:** [RF103 - Relatórios e Volumetria](./RF103.md)

---

## Índice de Casos de Uso

| UC | Nome | Descrição |
|----|------|-----------|
| UC01 | Visualizar Volumetria Agregada por Tipo | Volumetria de chamados, ativos, usuários, contratos e consumo com agregações pré-calculadas |
| UC02 | Visualizar Comparativo de Períodos (Mês vs Mês, Ano vs Ano) | Comparativo temporal com cálculo de variação percentual e tendência |
| UC03 | Visualizar Análise de Tendência com Média Móvel 7 Dias | Gráfico de tendência diária suavizado com média móvel para identificar padrões |
| UC04 | Visualizar Ranking Top 10 por Dimensão | Top 10 filiais, centros de custo, departamentos ou responsáveis ordenado por volume |
| UC05 | Exportar Volumetria em Múltiplos Formatos (Excel, PDF, CSV) | Export com aba de resumo executivo + abas detalhadas, processamento assíncrono se > 100k registros |

---

## UC01 - Visualizar Volumetria Agregada por Tipo

### Descrição

Permite usuários autorizados visualizarem volumetria consolidada de chamados, ativos, usuários, contratos e consumo, com agregações pré-calculadas (total, por tipo, prioridade, status, localização) em período selecionado. Dados são carregados de tabela `VolumetriaConsolidada` (pré-calculada via Hangfire às 4h diariamente) para performance otimizada.

### Atores

- Gestor
- Analista
- Administrador
- Diretoria
- Sistema de consolidação (Hangfire Job)
- Sistema de auditoria (RF004)

### Pré-condições

- Usuário autenticado no sistema
- Usuário possui permissão: `relatorio:volumetria:read`
- Multi-tenancy ativo (ClienteId válido)
- Feature flag `VOLUMETRIA_RELATORIOS` habilitada
- Volumetria consolidada disponível para o período selecionado

### Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa menu Relatórios → Volumetria | - |
| 2 | - | Valida autenticação e autorização (permissão `relatorio:volumetria:read`) |
| 3 | - | Renderiza interface com filtros: Tipo (Chamados, Ativos, Usuários, Contratos, Consumo), Período (De, Até) |
| 4 | Seleciona tipo "Chamados" e período "01/12/2025 a 31/12/2025" | - |
| 5 | Clica em "Gerar Relatório" | - |
| 6 | - | Valida filtros: data final >= data inicial |
| 7 | - | Aplica filtro multi-tenancy obrigatório (ClienteId do usuário autenticado) |
| 8 | - | Executa GET `/api/volumetria/chamados?de=2025-12-01&ate=2025-12-31` |
| 9 | - | Busca dados em `VolumetriaConsolidada WHERE ClienteId = X AND Tipo = 'Chamados' AND Data BETWEEN de AND ate` (RN-VOL-103-01) |
| 10 | - | Se dados não encontrados em VolumetriaConsolidada → executa agregação SQL nativa em tabela Chamados com COUNT/SUM/AVG |
| 11 | - | Registra acesso em auditoria (código: REL_VOLUMETRIA_READ) com usuário, período, resultado total |
| 12 | - | Retorna JSON com: total, porTipo, porPrioridade, porStatus |
| 13 | - | Renderiza interface com gráficos (Chart.js): pizza (proporção por tipo), barras (por prioridade), linha (evolução diária) |
| 14 | Visualiza volumetria consolidada com agregações | - |

### Fluxos Alternativos

**FA01 - Alterar Tipo de Volumetria**
- **Condição:** Usuário altera tipo de "Chamados" para "Ativos"
- **Ação:** Sistema recarrega endpoint GET `/api/volumetria/ativos`, atualiza gráficos com novos dados

**FA02 - Volumetria por Dimensão Customizada**
- **Condição:** Usuário clica em "Agrupar por Filial"
- **Ação:** Sistema executa GET `/api/volumetria/por-dimensao/filial`, exibe tabela com volume agregado por cada filial

**FA03 - Drill-Down em Agregação**
- **Condição:** Usuário clica em fatia do gráfico de pizza "Incidente" (750 chamados)
- **Ação:** Sistema redireciona para `/chamados` com filtro pré-aplicado: Tipo=Incidente, Período=01/12-31/12

**FA04 - Cache Hit (Dados Já Consolidados)**
- **Condição:** Dados foram consolidados via Hangfire às 4h
- **Ação:** Sistema busca em VolumetriaConsolidada em < 500ms, retorna imediatamente (sem calcular agregação on-demand)

### Exceções

**EX01 - Período Inválido**
- **Condição:** Data final < data inicial (ex: De=31/12/2025, Até=01/12/2025)
- **Ação:** Sistema retorna HTTP 400 Bad Request, exibe mensagem "Data final deve ser posterior à data inicial"

**EX02 - Usuário Sem Permissão**
- **Condição:** Usuário sem permissão `relatorio:volumetria:read` tenta acessar endpoint
- **Ação:** Sistema retorna HTTP 403 Forbidden, exibe mensagem "Você não tem permissão para acessar relatórios de volumetria", registra tentativa em auditoria

**EX03 - Sem Dados no Período**
- **Condição:** Query retorna 0 registros (período selecionado sem dados)
- **Ação:** Sistema retorna HTTP 200 OK com JSON `{total: 0}`, exibe mensagem "Nenhum dado encontrado para o período selecionado"

**EX04 - Erro ao Acessar VolumetriaConsolidada (Tabela Vazia)**
- **Condição:** Job Hangfire ainda não executou consolidação ou falhou
- **Ação:** Sistema fallback para agregação SQL nativa em tempo real (mais lento, 2-5 segundos), exibe aviso "Dados sendo calculados (consolidação pendente)"

### Pós-condições

- Volumetria exibida com gráficos interativos (Chart.js)
- Acesso registrado em auditoria (REL_VOLUMETRIA_READ)
- Dados em cache Redis por 1 hora (TTL)
- Usuário pode exportar ou visualizar comparativos

### Regras de Negócio Aplicáveis

- **RN-VOL-103-01**: Volumetria via Agregação SQL Nativa
- **RN-VOL-103-07**: Multi-tenancy Obrigatória - ClienteId em Todos os Filtros
- **RN-VOL-103-10**: Auditoria de Acesso a Relatórios de Volumetria

---

## UC02 - Visualizar Comparativo de Períodos (Mês vs Mês, Ano vs Ano)

### Descrição

Permite visualizar comparativo temporal entre período atual e período anterior equivalente (mês vs mês anterior, ano vs ano anterior) com cálculo automático de variação percentual e classificação de tendência (CRESCENTE, DECRESCENTE, ESTÁVEL). Exige que ambos os períodos estejam completamente finalizados para evitar comparativos parciais.

### Atores

- Analista
- Administrador
- Diretoria
- Sistema de consolidação (Hangfire Job)
- Sistema de auditoria (RF004)

### Pré-condições

- Usuário autenticado no sistema
- Usuário possui permissão: `relatorio:volumetria:comparativo`
- Multi-tenancy ativo (ClienteId válido)
- Volumetria consolidada disponível para ambos os períodos
- Ambos os períodos completamente finalizados (RN-VOL-103-03)

### Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa menu Relatórios → Volumetria → Comparativo de Períodos | - |
| 2 | - | Valida autenticação e autorização (permissão `relatorio:volumetria:comparativo`) |
| 3 | - | Renderiza interface com filtros: Tipo Comparativo (Mês vs Mês, Ano vs Ano), Ano, Mês (se aplicável) |
| 4 | Seleciona tipo "Mês vs Mês", Ano=2025, Mês=11 (Novembro) | - |
| 5 | Clica em "Gerar Comparativo" | - |
| 6 | - | Executa GET `/api/volumetria/comparativo?ano=2025&mes=11&tipo=mes` |
| 7 | - | Valida período atual (Novembro/2025) está finalizado: DataFim = 30/11/2025 <= DateTime.Now |
| 8 | - | Se período ainda aberto: retorna erro (vai para EX01) |
| 9 | - | Calcula período anterior: Outubro/2025 (mes-1) |
| 10 | - | Aplica filtro multi-tenancy (ClienteId) |
| 11 | - | Busca volumetria consolidada para Novembro/2025: `SELECT * FROM VolumetriaConsolidada WHERE ClienteId=X AND Data='2025-11-30'` |
| 12 | - | Busca volumetria consolidada para Outubro/2025: `SELECT * FROM VolumetriaConsolidada WHERE ClienteId=X AND Data='2025-10-31'` |
| 13 | - | Calcula variação: `((VolumeNov - VolumeOut) / VolumeOut) * 100` |
| 14 | - | Classifica tendência: variação > 0 = CRESCENTE, variação < 0 = DECRESCENTE, variação = 0 = ESTÁVEL |
| 15 | - | Registra auditoria (REL_VOLUMETRIA_COMPARATIVO) |
| 16 | - | Retorna JSON: `{periodoAtual: "11/2025", periodoAnterior: "10/2025", volumeAtual: 1250, volumeAnterior: 980, variacao: "+27.55%", tendencia: "CRESCENTE"}` |
| 17 | Visualiza comparativo com gráfico de barras lado-a-lado e indicador de tendência (seta verde/vermelha) | - |

### Fluxos Alternativos

**FA01 - Comparativo Ano vs Ano**
- **Condição:** Usuário seleciona tipo "Ano vs Ano", Ano=2025
- **Ação:** Sistema compara 2025 vs 2024 completos, calcula variação anual, exibe gráfico de linhas mensais sobrepostas (2024 vs 2025)

**FA02 - Comparativo com Múltiplos Tipos**
- **Condição:** Usuário seleciona "Comparar Chamados + Ativos"
- **Ação:** Sistema exibe 2 gráficos lado-a-lado: comparativo de chamados e comparativo de ativos

**FA03 - Exportar Comparativo**
- **Condição:** Usuário clica em "Exportar Comparativo"
- **Ação:** Sistema gera PDF ou Excel com: tabela de comparativo, gráfico, variação destacada, análise textual

**FA04 - Visualizar Histórico de Comparativos**
- **Condição:** Usuário clica em "Ver Histórico"
- **Ação:** Sistema exibe lista de comparativos anteriores já gerados (últimos 12 meses)

### Exceções

**EX01 - Período Atual Ainda Aberto**
- **Condição:** Mês selecionado (Dezembro/2025) ainda está em andamento (hoje = 28/12/2025)
- **Ação:** Sistema retorna HTTP 422 Unprocessable Entity, exibe mensagem "Comparativo não disponível. Período atual (Dezembro/2025) ainda está em aberto. Aguarde o encerramento do mês."

**EX02 - Período Anterior Sem Dados**
- **Condição:** Período anterior não possui dados consolidados (ex: Janeiro/2024 no sistema legado vazio)
- **Ação:** Sistema retorna HTTP 422, exibe mensagem "Período anterior (Janeiro/2024) não possui dados de consolidação. Impossível gerar comparativo."

**EX03 - Variação Infinita (Divisão por Zero)**
- **Condição:** Período anterior com volume = 0, período atual com volume > 0
- **Ação:** Sistema retorna variação = "N/A (período anterior sem dados)", tendência = "CRESCENTE"

**EX04 - Erro ao Buscar Dados Consolidados**
- **Condição:** Tabela VolumetriaConsolidada vazia ou job Hangfire falhou
- **Ação:** Sistema retorna HTTP 500, exibe mensagem "Erro ao buscar dados consolidados. Contate o suporte.", registra erro em log estruturado

### Pós-condições

- Comparativo exibido com variação percentual e tendência classificada
- Acesso registrado em auditoria (REL_VOLUMETRIA_COMPARATIVO)
- Gráfico interativo permite drill-down em cada período
- Dados em cache Redis por 24 horas (comparativo raramente muda)

### Regras de Negócio Aplicáveis

- **RN-VOL-103-03**: Comparativos Temporais Exigem Mínimo 2 Períodos Completos
- **RN-VOL-103-07**: Multi-tenancy Obrigatória - ClienteId em Todos os Filtros
- **RN-VOL-103-10**: Auditoria de Acesso a Relatórios de Volumetria

---

## UC03 - Visualizar Análise de Tendência com Média Móvel 7 Dias

### Descrição

Permite visualizar análise de tendência temporal (crescimento ou redução ao longo do tempo) utilizando média móvel de 7 dias para suavizar flutuações diárias e identificar padrões reais. Gráfico exibe linha de volumetria diária (valores brutos) sobreposta com linha de média móvel (valores suavizados).

### Atores

- Analista
- Administrador
- Diretoria
- Sistema de consolidação (Hangfire Job)
- Sistema de auditoria (RF004)

### Pré-condições

- Usuário autenticado no sistema
- Usuário possui permissão: `relatorio:volumetria:tendencia`
- Multi-tenancy ativo (ClienteId válido)
- Mínimo 7 dias de dados consolidados disponíveis
- Feature flag `VOLUMETRIA_RELATORIOS` habilitada

### Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa menu Relatórios → Volumetria → Análise de Tendência | - |
| 2 | - | Valida autenticação e autorização (permissão `relatorio:volumetria:tendencia`) |
| 3 | - | Renderiza interface com filtros: Tipo (Chamados, Ativos, Usuários), Período (últimos 30 dias, 60 dias, 90 dias ou customizado) |
| 4 | Seleciona tipo "Chamados", período "Últimos 30 dias" | - |
| 5 | Clica em "Gerar Análise de Tendência" | - |
| 6 | - | Executa GET `/api/volumetria/tendencia?de=2025-11-28&ate=2025-12-28&tipo=chamados` |
| 7 | - | Aplica filtro multi-tenancy (ClienteId) |
| 8 | - | Busca volumetria diária em `VolumetriaConsolidada WHERE ClienteId=X AND Tipo='Chamados' AND Data BETWEEN de AND ate ORDER BY Data ASC` |
| 9 | - | Para cada dia, calcula média móvel de 7 dias: `MM(i) = AVG(volumetria[i-6], ..., volumetria[i])` (RN-VOL-103-05) |
| 10 | - | Se < 7 dias: média móvel usa dias disponíveis (ex: dia 2 usa média de 2 dias) |
| 11 | - | Classifica tendência: se MM(último) > MM(primeiro) → CRESCENTE, senão → DECRESCENTE |
| 12 | - | Registra auditoria (REL_VOLUMETRIA_TENDENCIA) com dias analisados, média móvel calculada |
| 13 | - | Retorna JSON array: `[{data: "2025-11-28", volumeReal: 100, mediaMovel7Dias: 105, tendencia: "CRESCENTE"}, ...]` |
| 14 | - | Renderiza gráfico de linha (Chart.js): linha azul (volumetria diária), linha vermelha (média móvel 7d), área sombreada entre linhas |
| 15 | Visualiza tendência com padrão suavizado, identifica crescimento/redução | - |

### Fluxos Alternativos

**FA01 - Alterar Período de Análise**
- **Condição:** Usuário altera período de 30 dias para 90 dias
- **Ação:** Sistema recarrega endpoint com novos parâmetros, recalcula média móvel para 90 dias de dados

**FA02 - Comparar Tendência de Múltiplos Tipos**
- **Condição:** Usuário marca checkbox "Comparar Chamados + Ativos"
- **Ação:** Sistema exibe 2 linhas no mesmo gráfico: tendência chamados (azul) e tendência ativos (verde)

**FA03 - Exportar Gráfico de Tendência**
- **Condição:** Usuário clica em "Exportar Gráfico"
- **Ação:** Sistema gera imagem PNG do gráfico Chart.js e permite download

**FA04 - Drill-Down em Ponto Específico**
- **Condição:** Usuário clica em ponto do gráfico (ex: dia 15/12 com 150 chamados)
- **Ação:** Sistema exibe tooltip detalhado: "15/12/2025: 150 chamados (real), 145 (média móvel 7d), variação +3.4% vs dia anterior"

### Exceções

**EX01 - Dados Insuficientes (< 7 dias)**
- **Condição:** Período selecionado possui < 7 dias de dados consolidados
- **Ação:** Sistema calcula média móvel com dias disponíveis (ex: 3 dias = média de 3), exibe aviso "Dados insuficientes para média móvel completa. Usando média parcial."

**EX02 - Tendência Indefinida (Dados Constantes)**
- **Condição:** Todos os dias têm exatamente o mesmo volume (ex: 100, 100, 100, ...)
- **Ação:** Sistema retorna tendência = "ESTÁVEL", linha de média móvel sobrepõe linha real perfeitamente

**EX03 - Pico Anômalo Detectado**
- **Condição:** Um dia com volume 10x acima da média (ex: pico de 1.000 em série de ~100)
- **Ação:** Sistema destaca ponto no gráfico com marcador especial, exibe tooltip "Anomalia detectada: volume atípico"

**EX04 - Erro ao Buscar Dados Diários**
- **Condição:** Tabela VolumetriaConsolidada sem dados para alguns dias (gaps)
- **Ação:** Sistema preenche gaps com valor 0, exibe aviso "Dados ausentes em [datas]. Consolidação pode ter falh

ado.", continua cálculo de média móvel

### Pós-condições

- Gráfico de tendência exibido com média móvel de 7 dias
- Acesso registrado em auditoria (REL_VOLUMETRIA_TENDENCIA)
- Tendência classificada (CRESCENTE, DECRESCENTE, ESTÁVEL)
- Dados em cache Redis por 6 horas

### Regras de Negócio Aplicáveis

- **RN-VOL-103-05**: Tendências Usam Média Móvel de 7 Dias
- **RN-VOL-103-07**: Multi-tenancy Obrigatória - ClienteId em Todos os Filtros
- **RN-VOL-103-10**: Auditoria de Acesso a Relatórios de Volumetria

---

## UC04 - Visualizar Ranking Top 10 por Dimensão

### Descrição

Permite visualizar ranking top 10 de maior volume por dimensão selecionada (filial, centro de custo, departamento, responsável), ordenado descendente (maior volume primeiro) com totalização acumulada e percentual do total. Utilizado para identificar áreas críticas que concentram maior volume de operações.

### Atores

- Gestor
- Analista
- Administrador
- Diretoria
- Sistema de auditoria (RF004)

### Pré-condições

- Usuário autenticado no sistema
- Usuário possui permissão: `relatorio:volumetria:top10`
- Multi-tenancy ativo (ClienteId válido)
- Volumetria consolidada disponível
- Feature flag `VOLUMETRIA_RELATORIOS` habilitada

### Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa menu Relatórios → Volumetria → Top 10 | - |
| 2 | - | Valida autenticação e autorização (permissão `relatorio:volumetria:top10`) |
| 3 | - | Renderiza interface com filtros: Tipo (Chamados, Ativos, Usuários), Dimensão (Filial, Departamento, Responsável), Período (De, Até) |
| 4 | Seleciona tipo "Chamados", dimensão "Filial", período "01/12/2025 a 31/12/2025" | - |
| 5 | Clica em "Gerar Top 10" | - |
| 6 | - | Executa GET `/api/volumetria/top10/filial?de=2025-12-01&ate=2025-12-31` |
| 7 | - | Aplica filtro multi-tenancy (ClienteId) |
| 8 | - | Executa agregação SQL com GROUP BY + ORDER BY DESC + LIMIT 10 (RN-VOL-103-04) |
| 9 | - | Query: `SELECT Filial.Nome, COUNT(*) as Total FROM Chamados WHERE ClienteId=X AND DataCriacao BETWEEN de AND ate GROUP BY Filial.Nome ORDER BY Total DESC LIMIT 10` |
| 10 | - | Calcula total geral: `SUM(Total) de todos os resultados` |
| 11 | - | Para cada item do top 10: calcula percentual = `(itemTotal / totalGeral) * 100` |
| 12 | - | Registra auditoria (REL_VOLUMETRIA_TOP10) |
| 13 | - | Retorna JSON array: `[{posicao: 1, dimensao: "Filial São Paulo", volume: 500, percentualTotal: "40.00%"}, ...]` |
| 14 | - | Renderiza tabela ranking + gráfico de barras horizontais (Chart.js) |
| 15 | Visualiza top 10 com destaque para áreas críticas de maior volume | - |

### Fluxos Alternativos

**FA01 - Alterar Dimensão**
- **Condição:** Usuário altera dimensão de "Filial" para "Departamento"
- **Ação:** Sistema recarrega endpoint GET `/api/volumetria/top10/departamento`, atualiza gráfico com novo ranking

**FA02 - Drill-Down em Item do Top 10**
- **Condição:** Usuário clica em "Filial São Paulo" (1º lugar, 500 chamados)
- **Ação:** Sistema redireciona para `/chamados` com filtro pré-aplicado: Filial=São Paulo, Período=01/12-31/12, exibe lista detalhada de 500 chamados

**FA03 - Visualizar Top 20 ou Top 50**
- **Condição:** Usuário clica em "Expandir para Top 20"
- **Ação:** Sistema recarrega endpoint com `?limit=20`, exibe ranking completo com 20 itens

**FA04 - Exportar Ranking**
- **Condição:** Usuário clica em "Exportar Top 10"
- **Ação:** Sistema gera Excel ou PDF com tabela de ranking, gráfico, percentuais

### Exceções

**EX01 - Menos de 10 Itens Disponíveis**
- **Condição:** Query retorna apenas 7 filiais (total disponível < 10)
- **Ação:** Sistema exibe ranking com 7 itens, não preenche posições 8-10, mensagem "Apenas 7 filiais com dados no período"

**EX02 - Empate em Volume**
- **Condição:** Duas filiais com mesmo volume (ex: Filial A = 300, Filial B = 300)
- **Ação:** Sistema ordena alfabeticamente em caso de empate (Filial A antes de Filial B), exibe nota "* Ordenação alfabética em caso de empate"

**EX03 - Dimensão Sem Dados**
- **Condição:** Usuário seleciona dimensão "Responsável" mas campo Responsável está NULL em 100% dos registros
- **Ação:** Sistema retorna HTTP 200 com array vazio `[]`, exibe mensagem "Nenhum dado disponível para a dimensão selecionada (Responsável não preenchido)"

**EX04 - Percentual Total > 100% (Erro de Cálculo)**
- **Condição:** Soma de percentuais dos top 10 não bate com 100% (bug de arredondamento)
- **Ação:** Sistema ajusta último item para totalizar exatamente 100%, exibe nota "* Percentuais ajustados para totalização"

### Pós-condições

- Ranking top 10 exibido em ordem descendente
- Acesso registrado em auditoria (REL_VOLUMETRIA_TOP10)
- Percentuais calculados e validados
- Dados em cache Redis por 2 horas

### Regras de Negócio Aplicáveis

- **RN-VOL-103-04**: Top 10 Ordenado Descendente por Volume
- **RN-VOL-103-07**: Multi-tenancy Obrigatória - ClienteId em Todos os Filtros
- **RN-VOL-103-10**: Auditoria de Acesso a Relatórios de Volumetria

---

## UC05 - Exportar Volumetria em Múltiplos Formatos (Excel, PDF, CSV)

### Descrição

Permite exportar relatório de volumetria em múltiplos formatos (Excel XLSX, PDF, CSV) com estrutura otimizada: primeira aba de resumo executivo (KPIs principais, comparativos, tendências) + abas detalhadas por tipo. Relatórios com mais de 100.000 registros são processados assincronamente via Hangfire com notificação por email quando concluído.

### Atores

- Gestor
- Administrador
- Diretoria
- Hangfire (processamento assíncrono)
- Sistema de email (SMTP)
- Azure Blob Storage
- Sistema de auditoria (RF004)

### Pré-condições

- Usuário autenticado no sistema
- Usuário possui permissão: `relatorio:volumetria:export`
- Multi-tenancy ativo (ClienteId válido)
- Volumetria consolidada disponível
- Feature flags `VOLUMETRIA_EXPORT_EXCEL`, `VOLUMETRIA_EXPORT_PDF`, `VOLUMETRIA_EXPORT_CSV` habilitadas

### Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Visualiza volumetria gerada (UC01, UC02, UC03 ou UC04) | - |
| 2 | Clica em "Exportar" e seleciona formato "Excel" | - |
| 3 | - | Valida autenticação e autorização (permissão `relatorio:volumetria:export`) |
| 4 | - | Executa POST `/api/volumetria/export/excel` com body: `{de: "2025-12-01", ate: "2025-12-31", tipos: ["Chamados", "Ativos"]}` |
| 5 | - | Estima número de registros: executa COUNT em VolumetriaConsolidada e tabelas base |
| 6 | - | Se COUNT > 100.000: vai para FA01 (processamento assíncrono) |
| 7 | - | Se COUNT <= 100.000: processa sincronamente |
| 8 | - | Aplica filtro multi-tenancy (ClienteId) |
| 9 | - | Gera Excel XLSX usando EPPlus com estrutura de múltiplas abas (RN-VOL-103-08): Aba 1="Resumo Executivo", Aba 2="Chamados", Aba 3="Ativos" |
| 10 | - | Aba Resumo contém: logo cliente, título, período, KPIs principais, comparativo vs mês anterior, tendência |
| 11 | - | Abas detalhadas contêm: tabelas com agregações (por tipo, prioridade, status), totalizadores, formatação condicional |
| 12 | - | Registra auditoria (REL_VOLUMETRIA_EXPORT_EXCEL) com tamanho arquivo, tipos exportados |
| 13 | - | Retorna arquivo com headers: `Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`, `Content-Disposition: attachment; filename="volumetria_2025-12-01_2025-12-31.xlsx"` |
| 14 | Faz download do arquivo Excel (3.5 MB) | - |

### Fluxos Alternativos

**FA01 - Processamento Assíncrono (> 100.000 registros)**
- **Condição:** COUNT estimado > 100.000 registros
- **Ação:** Sistema enfileira job Hangfire `ProcessarExportVolumetriaJob`, retorna HTTP 202 Accepted com `{jobId: "abc-123", mensagem: "Relatório enfileirado. Você receberá um e-mail quando estiver pronto."}`. Job processa em background (60-90 segundos), gera arquivo, salva em Azure Blob Storage, envia email para usuário com link de download válido por 7 dias.

**FA02 - Exportar em PDF**
- **Condição:** Usuário seleciona formato "PDF"
- **Ação:** Sistema executa POST `/api/volumetria/export/pdf`, gera PDF usando iText com: logo cliente, resumo executivo (1 página), gráficos renderizados como imagens PNG, tabelas detalhadas, retorna arquivo PDF

**FA03 - Exportar em CSV**
- **Condição:** Usuário seleciona formato "CSV"
- **Ação:** Sistema executa POST `/api/volumetria/export/csv`, gera arquivo CSV com separador `;` (padrão Brasil), codificação UTF-8, header com nomes de colunas, dados agregados em linhas, retorna arquivo CSV

**FA04 - Exportar Apenas Resumo Executivo**
- **Condição:** Usuário marca checkbox "Apenas Resumo (sem detalhes)"
- **Ação:** Sistema gera Excel com 1 aba apenas (Resumo Executivo), arquivo menor (~500 KB), download instantâneo

### Exceções

**EX01 - Erro ao Gerar Excel (EPPlus Falha)**
- **Condição:** Biblioteca EPPlus lança exceção (dados corrompidos, OutOfMemoryException)
- **Ação:** Sistema retorna HTTP 500 Internal Server Error, exibe mensagem "Erro ao gerar arquivo Excel. Tente formato CSV ou contate o suporte.", registra stacktrace em log

**EX02 - Job Hangfire Falha 3x Consecutivas**
- **Condição:** Processamento assíncrono falha 3 vezes (timeout, erro SQL, blob storage indisponível)
- **Ação:** Sistema envia email ao usuário "Relatório falhou após 3 tentativas. Contate o suporte com JobId: abc-123.", registra erro crítico, alerta equipe DevOps

**EX03 - Arquivo Muito Grande (> 50 MB após Geração)**
- **Condição:** Excel gerado excede 50 MB (limite de download HTTP)
- **Ação:** Sistema divide em múltiplos arquivos (Part1.xlsx, Part2.xlsx, Part3.xlsx), zippa todos em volumetria.zip, retorna ZIP para download

**EX04 - Azure Blob Storage Indisponível**
- **Condição:** Falha ao fazer upload do arquivo gerado para Azure Blob Storage
- **Ação:** Sistema retorna HTTP 500, exibe mensagem "Erro ao salvar relatório. Tente novamente em alguns minutos.", registra erro em Application Insights

### Pós-condições

- Arquivo exportado em formato selecionado (Excel, PDF ou CSV)
- Auditoria registrada (REL_VOLUMETRIA_EXPORT_*) com tamanho arquivo, tipos exportados
- Se processamento assíncrono: email enviado com link de download
- Arquivo disponível em Azure Blob Storage por 7 dias
- Registro em histórico de exports

### Regras de Negócio Aplicáveis

- **RN-VOL-103-07**: Multi-tenancy Obrigatória - ClienteId em Todos os Filtros
- **RN-VOL-103-08**: Export Excel Deve Conter Aba de Resumo + Abas Detalhadas
- **RN-VOL-103-09**: Relatórios > 100.000 Registros Processados em Background
- **RN-VOL-103-10**: Auditoria de Acesso a Relatórios de Volumetria

---

## Histórico de Alterações

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 1.0 | 2025-12-28 | Claude Code | Versão inicial - 5 casos de uso cobrindo volumetria agregada, comparativos, tendências, top 10 e exports |
