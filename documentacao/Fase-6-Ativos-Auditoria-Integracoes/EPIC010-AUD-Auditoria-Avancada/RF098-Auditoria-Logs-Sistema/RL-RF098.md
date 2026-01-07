# RL-RF098 — Referência ao Legado (Auditoria de Logs do Sistema)

**Versão:** 1.0
**Data:** 2025-12-31
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF-098
**Sistema Legado:** IControlIT v1 (ASP.NET Web Forms + VB.NET)
**Objetivo:** Documentar o sistema legado de logging e auditoria, que utilizava EventViewer + arquivos de texto + tabelas SQL Server sem estruturação adequada, sem correlação de eventos, sem alertas automáticos e sem integração com ferramentas de monitoramento modernas.

---

## 1. CONTEXTO DO SISTEMA LEGADO

### 1.1 Stack Tecnológica do Legado

- **Arquitetura:** Monolítica (ASP.NET Web Forms)
- **Linguagem:** VB.NET (code-behind .aspx.vb)
- **Frontend:** ASP.NET Web Forms (ViewState, PostBack)
- **Backend:** VB.NET + ADO.NET
- **Banco de Dados:** SQL Server (múltiplas instâncias por cliente)
- **Logging:** EventViewer (Windows Events) + Arquivos de texto (.log) + Tabelas SQL Server (LogRegistro, LogAuditoria, LogErro)
- **Multi-tenant:** Parcial (bancos separados por cliente)
- **Auditoria:** Parcial (logs em tabelas SQL Server sem padrão consistente)

### 1.2 Problemas Arquiteturais Identificados

1. **Logging Descentralizado e Não Estruturado**
   - Logs espalhados em múltiplos servidores (arquivos .log locais)
   - EventViewer usado apenas para erros críticos (não acessível remotamente)
   - Tabelas SQL Server com estrutura inconsistente (LogRegistro, LogAuditoria, LogErro)
   - Sem correlação entre eventos de diferentes camadas
   - Busca manual em arquivos de texto (impossível em grande volume)

2. **Ausência de Correlação de Requisições**
   - Impossível rastrear uma requisição HTTP completa do frontend ao backend
   - Logs sem TraceId/CorrelationId (não havia como correlacionar eventos relacionados)
   - Dificulta diagnóstico de problemas em fluxos multi-camadas

3. **Contexto Mínimo de Logs**
   - Logs contêm apenas: timestamp, mensagem, nível (Error/Info)
   - Sem informações de usuário, IP, sessão, requisição HTTP, latência
   - Impossibilita análise de segurança (quem fez o quê, de onde)

4. **Sem Alertas Automáticos**
   - Erros críticos não geravam notificações automáticas
   - Equipe de suporte descobria problemas apenas quando usuários reportavam
   - Sem monitoramento proativo de taxa de erro, latência, disponibilidade

5. **Retenção de Dados Sem Política Clara**
   - Logs mantidos indefinidamente (consumo excessivo de disco)
   - Ou deletados manualmente sem critério (perda de evidências)
   - Sem conformidade com LGPD (direito ao esquecimento não implementado)

6. **Performance Impactada por Logging Síncrono**
   - Gravação de logs no banco SQL Server em cada requisição (síncrono)
   - Latência adicional de 50-200ms por requisição
   - Em picos de carga, banco de logs travava a aplicação

7. **Sem Integração SIEM**
   - Logs não exportados para ferramentas de análise de segurança
   - Sem detecção automática de padrões de ataque (SQL Injection, força bruta)

---

## 2. TELAS ASPX DO LEGADO

### 2.1 VisualizarLogs.aspx

**Caminho:** `ic1_legado/IControlIT/Admin/VisualizarLogs.aspx`

**Responsabilidade:** Exibir últimos 100 registros da tabela LogRegistro em GridView

**Campos:**
| Campo | Tipo | Obrigatório | Observações |
|------|------|-------------|-------------|
| txtDataInicio | TextBox (date) | Não | Filtro de data inicial (sem máscara, validação manual) |
| txtDataFim | TextBox (date) | Não | Filtro de data final |
| ddlNivel | DropDownList | Não | Valores: ERROR, WARNING, INFO (sem Trace, Debug, Critical) |
| GridViewLogs | GridView | - | Exibe: DataLog, TipoLog, Mensagem, Usuario (sem paginação real) |

**Comportamentos Implícitos:**
- Sem paginação real (carrega todos os registros em memória, depois aplica PageSize=100)
- Filtros não combinados (ou filtra por data, ou por nível, nunca ambos)
- Sem busca por texto livre na mensagem
- Sem correlação de eventos (impossível rastrear requisição completa)

**DESTINO:** SUBSTITUÍDO por `/auditoria/logs` (Angular com filtros dinâmicos, paginação server-side, Application Insights KQL)

---

### 2.2 RelatorioErros.aspx

**Caminho:** `ic1_legado/IControlIT/Admin/RelatorioErros.aspx`

**Responsabilidade:** Relatório de erros agrupados por tipo (COUNT(*) GROUP BY Mensagem)

**Campos:**
| Campo | Tipo | Obrigatório | Observações |
|------|------|-------------|-------------|
| txtPeriodo | TextBox (number) | Sim | Quantidade de dias (ex: 7 para últimos 7 dias) |
| GridViewErros | GridView | - | Exibe: Mensagem, Ocorrencias, PrimeiraOcorrencia, UltimaOcorrencia |

**Comportamentos Implícitos:**
- Agrupa apenas por mensagem (não agrupa por stack trace ou módulo)
- Sem drill-down para ver detalhes de uma ocorrência específica
- Timeout frequente ao consultar períodos > 30 dias (query sem índices otimizados)

**DESTINO:** SUBSTITUÍDO por `/auditoria/logs/dashboard` (dashboard com top erros, gráficos temporais, drill-down)

---

### 2.3 AuditoriaOperacoes.aspx

**Caminho:** `ic1_legado/IControlIT/Admin/AuditoriaOperacoes.aspx`

**Responsabilidade:** Exibir logs da tabela LogAuditoria (mudanças em dados de negócio)

**Campos:**
| Campo | Tipo | Obrigatório | Observações |
|------|------|-------------|-------------|
| ddlTabela | DropDownList | Sim | Lista de tabelas auditadas (hardcoded em VB.NET) |
| txtUsuario | TextBox | Não | Filtro por nome de usuário (LIKE %texto%) |
| GridViewAuditoria | GridView | - | Exibe: DataOperacao, Tabela, Operacao (INSERT/UPDATE/DELETE), Usuario, DadosAnteriores, DadosNovos |

**Comportamentos Implícitos:**
- Auditoria implementada manualmente (trigger em cada tabela)
- DadosAnteriores e DadosNovos armazenados como XML (difícil comparação)
- Sem versionamento (apenas last known state)
- Sem informação de IP, sessão, requisição HTTP (apenas usuário)

**DESTINO:** SUBSTITUÍDO por AuditInterceptor (EF Core) + `/auditoria/logs` (auditoria automática, JSON estruturado, contexto completo)

---

## 3. WEBSERVICES E MÉTODOS LEGADOS

### 3.1 WSAuditoria.asmx.vb

**Localização:** `ic1_legado/IControlIT/WebServices/WSAuditoria.asmx.vb`

| Método | Responsabilidade | DESTINO |
|--------|------------------|---------|
| `ObterLogs()` | Retorna últimos 100 logs da tabela LogRegistro | SUBSTITUÍDO por `GET /api/logs?pageSize=100` |
| `BuscarErros(dataInicio, dataFim)` | Retorna logs com TipoLog = 'ERROR' em período | SUBSTITUÍDO por `GET /api/logs?severidade=Error&dataInicio=X&dataFim=Y` |
| `ExportarAuditoria(tabela)` | Exporta auditoria em CSV (sem criptografia, sem autenticação) | SUBSTITUÍDO por `POST /api/logs/export` (com RBAC, limite de 10k registros) |

**Problemas Identificados:**
- Sem autenticação (qualquer um com URL podia acessar logs)
- Retorna todos os campos (inclusive dados sensíveis em texto claro: CPF, email)
- Timeout frequente ao exportar períodos grandes (> 10k registros)

**DESTINO:** SUBSTITUÍDO por API RESTful com autenticação JWT + RBAC + sanitização de dados sensíveis

---

## 4. STORED PROCEDURES DO LEGADO

### 4.1 pa_LogInserir

**Localização:** `ic1_legado/Database/StoredProcedures/pa_LogInserir.sql`

**Descrição:** Insere registro na tabela LogRegistro de forma síncrona

```sql
CREATE PROCEDURE [dbo].[pa_LogInserir]
    @DataLog DATETIME,
    @TipoLog VARCHAR(50),
    @Mensagem VARCHAR(1000),
    @Usuario VARCHAR(50),
    @Modulo VARCHAR(100)
AS
BEGIN
    INSERT INTO LogRegistro (DataLog, TipoLog, Mensagem, Usuario, Modulo)
    VALUES (@DataLog, @TipoLog, @Mensagem, @Usuario, @Modulo)
END
```

**Problemas Identificados:**
- Execução síncrona (bloqueia thread da aplicação até commit no banco)
- Sem batch insert (um INSERT por log = muitas transações)
- Sem índices em colunas de busca (DataLog, TipoLog) = queries lentas

**DESTINO:** SUBSTITUÍDO por Serilog Sink (assíncrono, batch, envio para Application Insights)

---

### 4.2 pa_LogBuscar

**Localização:** `ic1_legado/Database/StoredProcedures/pa_LogBuscar.sql`

**Descrição:** Busca logs por critério (data, tipo, usuário)

```sql
CREATE PROCEDURE [dbo].[pa_LogBuscar]
    @DataInicio DATETIME = NULL,
    @DataFim DATETIME = NULL,
    @TipoLog VARCHAR(50) = NULL,
    @Usuario VARCHAR(50) = NULL
AS
BEGIN
    SELECT * FROM LogRegistro
    WHERE (@DataInicio IS NULL OR DataLog >= @DataInicio)
    AND (@DataFim IS NULL OR DataLog <= @DataFim)
    AND (@TipoLog IS NULL OR TipoLog = @TipoLog)
    AND (@Usuario IS NULL OR Usuario LIKE '%' + @Usuario + '%')
    ORDER BY DataLog DESC
END
```

**Problemas Identificados:**
- SELECT * (retorna todos os campos, inclusive BLOB com stack trace completo = alto consumo de rede)
- Sem LIMIT (pode retornar milhões de registros = timeout)
- LIKE '%texto%' (não usa índices, scan completo da tabela)

**DESTINO:** SUBSTITUÍDO por Application Insights KQL (queries indexadas, paginação automática, projections otimizadas)

---

## 5. TABELAS LEGADAS

### 5.1 LogRegistro

**Tabela:** `[dbo].[LogRegistro]`

**Finalidade:** Armazenar logs gerais da aplicação

**Problemas Identificados:**
- Sem campo CorrelationId (impossível correlacionar eventos relacionados)
- Sem campo IpAddress, SessionId, RequestPath, StatusCode, ResponseTime (contexto mínimo)
- Mensagem VARCHAR(1000) (stack traces grandes eram truncados = perda de informação)
- Sem índice em DataLog, TipoLog (queries lentas)
- Sem particionamento (tabela com +10M registros = performance degradada)
- Sem multi-tenancy (logs de todos os clientes na mesma tabela = risco de vazamento)

**DESTINO:** SUBSTITUÍDO por Application Insights (estrutura otimizada, índices automáticos, particionamento temporal)

---

### 5.2 LogAuditoria

**Tabela:** `[dbo].[LogAuditoria]`

**Finalidade:** Armazenar auditoria de mudanças em dados de negócio

**Problemas Identificados:**
- DadosAnteriores e DadosNovos como XML (difícil comparação, sem schema validation)
- Trigger manual em cada tabela auditada (alto risco de inconsistência se alguém esquecer de criar trigger)
- Sem versionamento (apenas last known state, não histórico completo)
- Sem informação de IP, sessão, requisição HTTP (apenas usuário)

**DESTINO:** SUBSTITUÍDO por AuditInterceptor (EF Core) com JSON estruturado + Application Insights

---

### 5.3 LogErro

**Tabela:** `[dbo].[LogErro]`

**Finalidade:** Armazenar erros e exceções

**Problemas Identificados:**
- Separação artificial entre LogRegistro e LogErro (duplicação de lógica)
- StackTrace como TEXT (sem compressão = alto consumo de espaço)
- InnerException como VARCHAR(MAX) (pode estar truncado)

**DESTINO:** DESCARTADO (logs unificados em Application Insights com campo Exception estruturado)

---

## 6. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

### RL-RN-001: Logs Síncronos Bloqueiam Aplicação
**Localização:** `ic1_legado/IControlIT/Classes/Logger.vb:23`
**Descrição:** Toda operação de log executava INSERT síncrono no banco SQL Server, adicionando latência de 50-200ms por requisição.
**DESTINO:** SUBSTITUÍDO
**Rastreabilidade:** RN-RF098-007 (Serilog async sink para Application Insights, não bloqueia thread)

---

### RL-RN-002: Apenas 3 Níveis de Log (Error, Warning, Info)
**Localização:** `ic1_legado/Database/Tables/LogRegistro.sql:5`
**Descrição:** Tabela LogRegistro tinha apenas 3 valores possíveis para TipoLog: ERROR, WARNING, INFO (sem Trace, Debug, Critical).
**DESTINO:** ASSUMIDO com expansão
**Rastreabilidade:** RN-RF098-001 (6 níveis: Trace, Debug, Information, Warning, Error, Critical)

---

### RL-RN-003: Retenção Indefinida de Logs
**Localização:** Ausente (sem política de retenção)
**Descrição:** Logs eram mantidos indefinidamente no banco SQL Server até espaço em disco esgotar ou DBA deletar manualmente.
**DESTINO:** SUBSTITUÍDO
**Rastreabilidade:** RN-RF098-004 (Retenção diferenciada por severidade: Critical 365 dias, Error 180 dias, etc.)

---

### RL-RN-004: Mensagens Truncadas em 1000 Caracteres
**Localização:** `ic1_legado/Database/Tables/LogRegistro.sql:8`
**Descrição:** Campo Mensagem VARCHAR(1000) truncava stack traces grandes, causando perda de informação crítica para diagnóstico.
**DESTINO:** SUBSTITUÍDO
**Rastreabilidade:** RN-RF098-006 (Application Insights armazena stack trace completo + inner exceptions até 3 níveis)

---

### RL-RN-005: Busca Manual em Arquivos de Texto
**Localização:** Servidores de produção (`D:\Logs\IControlIT\*.log`)
**Descrição:** Logs também eram gravados em arquivos de texto (.log) sem estrutura, exigindo busca manual com Notepad++/grep.
**DESTINO:** DESCARTADO
**Rastreabilidade:** Logs estruturados em Application Insights com busca via KQL (Kusto Query Language)

---

### RL-RN-006: Sem Alertas Automáticos
**Localização:** Ausente
**Descrição:** Erros críticos não geravam notificações automáticas. Equipe descobria problemas apenas quando usuários reportavam.
**DESTINO:** SUBSTITUÍDO
**Rastreabilidade:** RN-RF098-009 (Alertas configuráveis com condições dinâmicas, email/webhook/in-app)

---

### RL-RN-007: Dados Sensíveis em Texto Claro
**Localização:** `ic1_legado/IControlIT/Classes/Logger.vb:45`
**Descrição:** Logs continham dados sensíveis em texto claro: CPF completo, senhas (em mensagens de erro), tokens de API.
**DESTINO:** SUBSTITUÍDO
**Rastreabilidade:** RN-RF098-005 (Sanitização automática de dados sensíveis antes de logar)

---

## 7. GAP ANALYSIS (LEGADO × MODERNO)

| Item | Legado | RF-098 Moderno | Observação |
|------|--------|----------------|------------|
| **Framework de Logging** | EventViewer + Arquivos de texto + SQL Server manual | Serilog + Application Insights | Funcionalidade totalmente nova |
| **Níveis de Severidade** | 3 níveis (Error, Warning, Info) | 6 níveis (Trace, Debug, Information, Warning, Error, Critical) | Expansão de funcionalidade |
| **Correlação de Eventos** | Ausente | CorrelationId automático | Funcionalidade totalmente nova |
| **Contexto de Logs** | Mínimo (mensagem, timestamp) | Completo (usuário, IP, sessão, path, timing, stack trace) | Expansão significativa |
| **Centralização** | Logs espalhados (arquivos + EventViewer + SQL Server) | Application Insights centralizado | Funcionalidade totalmente nova |
| **Busca Avançada** | Busca manual em arquivos ou SELECT * sem índices | KQL (Kusto Query Language) com índices otimizados | Funcionalidade totalmente nova |
| **Alertas** | Ausente | Alertas configuráveis com múltiplos canais | Funcionalidade totalmente nova |
| **Retenção** | Indefinida (manual) | Governada por severidade (Critical 365d, Error 180d, etc.) | Melhoria |
| **Performance** | Síncrono (latência 50-200ms) | Assíncrono com batch (latência < 5ms) | Melhoria crítica |
| **Exportação** | CSV sem autenticação | CSV/JSON/Excel com RBAC + limite de 10k registros | Melhoria de segurança |
| **Sanitização de Dados Sensíveis** | Ausente | Automática (mascaramento de CPF, senha, token) | Funcionalidade totalmente nova |
| **Multi-Tenancy** | Ausente | Row-Level Security com EmpresaId | Funcionalidade totalmente nova |
| **SIEM** | Ausente | Integração com Azure Sentinel | Funcionalidade totalmente nova |
| **Dashboard** | Relatório estático em GridView | Dashboard em tempo real com gráficos interativos | Funcionalidade totalmente nova |
| **Conformidade LGPD** | Ausente | Direito ao esquecimento, retenção governada | Funcionalidade totalmente nova |

---

## 8. DECISÕES DE MODERNIZAÇÃO

### 8.1 Decisão: Substituir SQL Server + Arquivos por Application Insights
- **Motivo:** Application Insights oferece indexação automática, busca avançada (KQL), alertas integrados, dashboards nativos, escalabilidade automática e integração com Azure Sentinel.
- **Impacto:** ALTO (mudança completa de plataforma de logging)
- **Benefício:** Redução de latência (síncrono → assíncrono), busca performática (KQL vs SELECT *), alertas automáticos, conformidade LGPD.

---

### 8.2 Decisão: Usar Serilog como Framework de Logging
- **Motivo:** Serilog é padrão da indústria .NET, suporta structured logging, múltiplos sinks (Application Insights, File, Console), configuração via appsettings.json.
- **Impacto:** MÉDIO (nova dependência externa)
- **Benefício:** Logging estruturado (não apenas string), enrichers automáticos (usuário, IP, CorrelationId), assíncrono por padrão.

---

### 8.3 Decisão: Implementar CorrelationId Automático
- **Motivo:** Rastreamento de requisições completas (frontend → backend → database → APIs externas) é essencial para diagnóstico em arquiteturas distribuídas.
- **Impacto:** MÉDIO (middleware para injetar CorrelationId em HttpContext)
- **Benefício:** Facilita investigação de problemas, permite rastreamento end-to-end.

---

### 8.4 Decisão: Expandir Níveis de Severidade de 3 para 6
- **Motivo:** Legado tinha apenas Error, Warning, Info. Moderno adiciona Trace (verbose), Debug (diagnóstico), Critical (falha grave).
- **Impacto:** BAIXO (mudança de enum)
- **Benefício:** Melhor classificação de eventos, alertas mais inteligentes (apenas Critical gera PagerDuty).

---

### 8.5 Decisão: Implementar Sanitização Automática de Dados Sensíveis
- **Motivo:** Legado logava CPF, senhas, tokens em texto claro (violação LGPD).
- **Impacto:** MÉDIO (implementar sanitizer com regex para mascarar campos)
- **Benefício:** Conformidade LGPD, redução de risco de vazamento de dados.

---

### 8.6 Decisão: Retenção Diferenciada Por Severidade
- **Motivo:** Logs Critical precisam ser mantidos por 365 dias (evidências), mas logs Debug podem ser descartados após 7 dias (otimização de custo).
- **Impacto:** BAIXO (job Hangfire para limpeza de logs expirados)
- **Benefício:** Redução de custo de armazenamento, conformidade com políticas de retenção.

---

## 9. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Mitigação |
|------|---------|-----------|\n| **Perda de Histórico de Logs Antigos** | ALTO | Exportar logs históricos do SQL Server legado para Azure Blob Storage antes de desativar. Manter acesso read-only ao banco legado por 6 meses. |
| **Mudança de Interface de Busca** | MÉDIO | Treinar equipe de suporte em KQL (Kusto Query Language). Criar atalhos para queries mais comuns (últimos erros, logs por usuário). |
| **Latência de Envio para Application Insights** | BAIXO | Serilog envia logs de forma assíncrona (não bloqueia aplicação). Se Application Insights estiver indisponível, logs são bufferizados localmente. |
| **Custo de Application Insights** | MÉDIO | Configurar amostragem (sampling) para reduzir volume de logs em ambientes de desenvolvimento. Produção mantém 100% dos logs. |
| **Falta de Treinamento em KQL** | MÉDIO | Criar documentação interna com queries KQL mais usadas. Realizar treinamento de 2h para equipe de suporte e desenvolvimento. |

---

## 10. RASTREABILIDADE

| Elemento Legado | Destino | RF-098 Moderno |
|----------------|---------|----------------|
| `LogRegistro` (tabela SQL Server) | SUBSTITUÍDO | Application Insights (cloud-based, indexed, scalable) |
| `LogAuditoria` (tabela SQL Server) | SUBSTITUÍDO | AuditInterceptor (EF Core) + Application Insights |
| `LogErro` (tabela SQL Server) | DESCARTADO | Logs unificados em Application Insights com campo Exception |
| `pa_LogInserir` (stored procedure) | SUBSTITUÍDO | Serilog Sink (assíncrono, batch) |
| `pa_LogBuscar` (stored procedure) | SUBSTITUÍDO | Application Insights KQL queries |
| `VisualizarLogs.aspx` (tela legado) | SUBSTITUÍDO | `/auditoria/logs` (Angular + Material) |
| `RelatorioErros.aspx` (tela legado) | SUBSTITUÍDO | `/auditoria/logs/dashboard` |
| `AuditoriaOperacoes.aspx` (tela legado) | SUBSTITUÍDO | AuditInterceptor + `/auditoria/logs` |
| `WSAuditoria.asmx.vb` (WebService legado) | SUBSTITUÍDO | `GET /api/logs`, `POST /api/logs/export` (RESTful API) |
| Logs em arquivos de texto (`.log`) | DESCARTADO | Application Insights (structured logging) |
| EventViewer (Windows Events) | DESCARTADO | Application Insights (centralizado) |
| Logs síncronos (latência 50-200ms) | SUBSTITUÍDO | Serilog async sink (latência < 5ms) |
| 3 níveis de severidade (Error, Warning, Info) | ASSUMIDO com expansão | 6 níveis (Trace, Debug, Information, Warning, Error, Critical) |
| Retenção indefinida | SUBSTITUÍDO | Retenção governada (Critical 365d, Error 180d, etc.) |
| Dados sensíveis em texto claro | SUBSTITUÍDO | Sanitização automática (CPF, senha, token mascarados) |

---

## 11. PROBLEMAS LEGADO IDENTIFICADOS

### PROB-RF098-001: Logging Síncrono Degradando Performance
**Severidade:** CRÍTICA
**Descrição:** Toda operação de log executava INSERT síncrono no banco SQL Server, adicionando latência de 50-200ms por requisição. Em picos de carga, logging travava a aplicação.
**Impacto:** Degradação de performance, timeout de requisições, experiência ruim do usuário.
**Solução Moderna:** Serilog Sink assíncrono para Application Insights (latência < 5ms, não bloqueia thread).

---

### PROB-RF098-002: Ausência de Correlação de Eventos
**Severidade:** ALTA
**Descrição:** Impossível rastrear uma requisição HTTP completa do frontend ao backend. Logs sem TraceId/CorrelationId.
**Impacto:** Diagnóstico de problemas em fluxos multi-camadas é extremamente demorado (horas de investigação manual).
**Solução Moderna:** CorrelationId automático gerado no entry point e propagado para todas as camadas.

---

### PROB-RF098-003: Logs Não Estruturados
**Severidade:** ALTA
**Descrição:** Logs armazenados como texto plano em arquivos .log ou VARCHAR em SQL Server. Busca manual com grep/Notepad++.
**Impacto:** Busca ineficiente, impossível análises complexas (agregações, séries temporais, correlações).
**Solução Moderna:** Structured logging com Serilog + Application Insights KQL (queries indexadas, agregações automáticas).

---

### PROB-RF098-004: Dados Sensíveis em Texto Claro
**Severidade:** CRÍTICA
**Descrição:** Logs continham CPF completo, senhas (em mensagens de erro), tokens de API em texto claro.
**Impacto:** Violação LGPD, risco de vazamento de dados, multas regulatórias.
**Solução Moderna:** Sanitização automática de dados sensíveis antes de logar (CPF mascarado, senha redacted, token truncado).

---

### PROB-RF098-005: Sem Alertas Automáticos
**Severidade:** ALTA
**Descrição:** Erros críticos não geravam notificações automáticas. Equipe descobria problemas apenas quando usuários reportavam.
**Impacto:** Tempo de detecção de incidentes alto (MTTD > 30 minutos), tempo de resolução alto (MTTR > 2 horas).
**Solução Moderna:** Alertas configuráveis com Application Insights (taxa de erro > 5% → email para dev team, log Critical → PagerDuty).

---

### PROB-RF098-006: Retenção Sem Política Clara
**Severidade:** MÉDIA
**Descrição:** Logs mantidos indefinidamente até espaço em disco esgotar, ou deletados manualmente sem critério.
**Impacto:** Alto custo de armazenamento, perda de evidências para auditorias, não conformidade LGPD.
**Solução Moderna:** Retenção governada por severidade (Critical 365 dias, Error 180 dias, Warning 90 dias, Information 30 dias, Debug/Trace 7 dias).

---

## METADADOS

| Métrica | Valor |
|---------|-------|
| **Total de Itens Legado Rastreados** | 17 |
| **Itens ASSUMIDOS** | 1 |
| **Itens SUBSTITUÍDOS** | 14 |
| **Itens DESCARTADOS** | 2 |
| **Itens A_REVISAR** | 0 |
| **Cobertura de Destinos** | 100% |
| **Problemas Legado Identificados** | 6 |
| **Severidade Crítica** | 3 |
| **Severidade Alta** | 3 |
| **Severidade Média** | 0 |

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|--------|------|-----------|-------|
| 1.0 | 2025-12-31 | Documentação inicial de referência ao legado (logging descentralizado, não estruturado, sem correlação, sem alertas) | Agência ALC - alc.dev.br |
