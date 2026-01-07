# RL-RF003 — Referência ao Legado: Sistema de Logs

**Versão:** 1.0
**Data:** 2025-12-29
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF-003 - Sistema de Logs, Monitoramento e Observabilidade
**Sistema Legado:** Arquivo de Log Texto Plano (VB.NET + ASP.NET Web Forms)
**Objetivo:** Documentar o comportamento do sistema de logging legado que serve de base para a modernização com Serilog, Seq e Elasticsearch, garantindo rastreabilidade, entendimento histórico e mitigação de riscos.

---

## 1. CONTEXTO DO LEGADO

O sistema legado **NÃO possuía sistema estruturado de logs, monitoramento ou observabilidade**.

- **Arquitetura:** Monolítica Web Forms (ASP.NET + VB.NET)
- **Linguagem / Stack:** VB.NET, ASP.NET Web Forms 4.x
- **Banco de Dados:** SQL Server (logs NÃO eram persistidos em banco)
- **Multi-tenant:** Não aplicável (logs globais sem segregação)
- **Auditoria:** Inexistente (logs não tinham rastreabilidade de usuário ou ação)
- **Configurações:** Não configurável (nível de log fixo, sem controle)

**Método de Logging:**
- Arquivo texto plano (`app.log`) no diretório `D:\IC2\ic1_legado\IControlIT\IControlIT\logs\`
- Escrita direta via `StreamWriter` no code-behind VB.NET
- Sem biblioteca estruturada (escrita manual linha por linha)
- Cada servidor web tinha seu próprio arquivo `app.log` isolado

---

## 2. TELAS DO LEGADO

### Tela: ❌ NENHUMA INTERFACE DE VISUALIZAÇÃO

O sistema legado **não possuía interface web para visualizar logs**.

**Método de Acesso:**
- Administradores acessavam servidor via **RDP** (Remote Desktop Protocol)
- Abriam arquivos `.log` manualmente com **Notepad** ou **Notepad++**
- Buscas realizadas via `Ctrl+F` (find) ou `grep` em linha de comando

**Problemas:**
1. ❌ Sem interface web (necessário acesso RDP ao servidor)
2. ❌ Sem autenticação/autorização (qualquer admin RDP podia ler)
3. ❌ Sem histórico de quem acessou logs (auditoria zero)
4. ❌ Sem filtros (data, usuário, nível de erro)
5. ❌ Sem busca full-text estruturada
6. ❌ Sem paginação (arquivos grandes travavam Notepad)

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

| Método | Local | Responsabilidade | Observações |
|--------|-------|------------------|-------------|
| `LogError(mensagem As String)` | Code-behind (*.aspx.vb) | Escrever linha de erro no app.log | ❌ Vazava dados sensíveis (CPF, senhas) |
| `LogInfo(mensagem As String)` | Code-behind (*.aspx.vb) | Escrever linha informativa | ❌ Sem timestamp estruturado |
| ❌ Nenhum endpoint API | - | - | Logs não eram acessíveis via API |

**Código VB.NET Legado:**

```vb.net
' Exemplo real de logging no sistema legado
Public Sub LogError(mensagem As String)
    Dim logFile As String = Server.MapPath("~/logs/app.log")
    Dim writer As New StreamWriter(logFile, True) ' append mode
    writer.WriteLine($"{DateTime.Now} - {mensagem}")
    writer.Close()
End Sub

' Uso típico (COM VAZAMENTO DE DADOS SENSÍVEIS!)
Try
    ' ... código de processamento
Catch ex As Exception
    LogError($"Erro ao processar CPF {cpf}: {ex.Message}")
    LogError($"Senha do usuário: {senha}") ' ❌ GRAVÍSSIMO: senha em texto claro!
End Try
```

**Problemas Identificados:**

1. ❌ **Formato texto não estruturado** (impossível parsear campos)
2. ❌ **CPF e senhas em texto claro** (violação LGPD)
3. ❌ **Sem correlation ID** (impossível rastrear request completo)
4. ❌ **Sem níveis de log** (tudo era "informação")
5. ❌ **Sem agregação** (cada servidor tinha arquivo separado)
6. ❌ **Sem busca** (apenas `grep` manual ou Ctrl+F)
7. ❌ **Sem métricas** (não sabia response time, error rate, throughput)
8. ❌ **Sem alertas** (problemas descobertos apenas quando usuário reportava)

---

## 4. TABELAS LEGADAS

| Tabela | Finalidade | Problemas Identificados |
|--------|------------|-------------------------|
| ❌ Nenhuma | Logs não eram persistidos em banco de dados | Não havia tabelas específicas de log |

**Observação:** Logs eram armazenados apenas em arquivos `.log` no sistema de arquivos do servidor web, sem backup, sem retenção controlada, sem replicação.

---

## 5. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

Regras que **não estavam documentadas**, apenas inferidas do código:

- **RL-RN-001:** Logs eram escritos apenas em caso de erro (exceções) - sucesso não era logado
- **RL-RN-002:** Formato de log era fixo: `{DateTime.Now} - {mensagem}`
- **RL-RN-003:** Não havia rotação de arquivos (app.log crescia indefinidamente até travar disco)
- **RL-RN-004:** Não havia mascaramento de dados sensíveis (CPF, senhas, cartões logados em texto claro)
- **RL-RN-005:** Não havia níveis de log (Info, Warning, Error) - tudo era texto livre
- **RL-RN-006:** Cada servidor web tinha arquivo isolado (sem agregação centralizada)
- **RL-RN-007:** Não havia retenção automática (arquivos nunca eram deletados)
- **RL-RN-008:** Logs de segurança (login, logout, acesso negado) NÃO eram registrados

---

## 6. GAP ANALYSIS (LEGADO x RF MODERNO)

| Item | Legado | RF Moderno | Observação |
|------|--------|------------|------------|
| **Formato** | Texto plano não estruturado | JSON estruturado (Serilog) | Permite queries por campos específicos |
| **Agregação** | Arquivo local por servidor | Centralizado (Seq/Elasticsearch) | Busca unificada em todos os servidores |
| **Correlation ID** | ❌ Inexistente | ✅ GUID em todos os logs | Rastrear request end-to-end |
| **Níveis de Log** | ❌ Inexistente | ✅ Verbose/Debug/Info/Warning/Error/Fatal | Filtrar por severidade |
| **Dados Sensíveis** | ❌ Texto claro (CPF, senhas) | ✅ Mascaramento automático | Compliance LGPD |
| **Busca** | ❌ Ctrl+F / grep manual | ✅ Full-text queries (SQL-like) | Queries complexas em segundos |
| **Interface** | ❌ Notepad via RDP | ✅ Seq UI / Grafana | Interface web com filtros |
| **Métricas** | ❌ Inexistente | ✅ Prometheus/Grafana (RED) | Response time, error rate, throughput |
| **Alertas** | ❌ Inexistente | ✅ PagerDuty/Opsgenie | Alertas proativos (error rate > 5%) |
| **Health Checks** | ❌ Inexistente | ✅ `/health` endpoint | Kubernetes liveness/readiness |
| **Tracing** | ❌ Inexistente | ✅ OpenTelemetry | Rastrear chamadas entre microservices |
| **Retenção** | ❌ Indefinida (nunca deletado) | ✅ Automática (90d/1y/7y) | Compliance LGPD/SOX |
| **Sampling** | ❌ Inexistente | ✅ 10% sucesso, 100% erros | Reduz custos sem perder diagnóstico |
| **Circuit Breaker** | ❌ Inexistente | ✅ Fallback para arquivo local | Logging não derruba aplicação |
| **Export** | ❌ Copy/paste manual | ✅ CSV/JSON via API | Auditoria externa |
| **Auditoria de Acesso** | ❌ Inexistente | ✅ Logs de quem acessou logs | Compliance ISO 27001 |

---

## 7. DECISÕES DE MODERNIZAÇÃO

### Decisão 1: Serilog + Seq (DEV/HOM) + Elasticsearch (PRD)

**Justificativa:**
- **Serilog:** Biblioteca .NET mais madura para structured logging (JSON)
- **Seq:** Interface web simples para DEV/HOM (self-hosted, grátis)
- **Elasticsearch:** Escala para milhões de logs/dia em PRD (búsca full-text)

**Impacto:** Alto (mudança completa de paradigma de logging)

### Decisão 2: Mascaramento Automático de Dados Sensíveis

**Justificativa:**
- Compliance LGPD (não logar CPF em texto claro)
- Compliance PCI-DSS (não logar cartões)
- Evitar multas (até 2% faturamento)

**Impacto:** Alto (requer regex e sanitização em todos os pontos de log)

### Decisão 3: Correlation IDs Obrigatórios

**Justificativa:**
- Rastrear request completo (frontend → API → banco → fila → job)
- Diagnosticar problemas em sistemas distribuídos (microservices)

**Impacto:** Médio (requer propagação de GUID em headers HTTP)

### Decisão 4: Sampling 10% em Produção

**Justificativa:**
- Reduzir custos de armazenamento (Elasticsearch caro para 1M logs/dia)
- Manter 100% de erros (troubleshooting não prejudicado)

**Impacto:** Baixo (apenas logs Info/Debug reduzidos, erros sempre 100%)

### Decisão 5: Retenção Automática (90d / 1y / 7y)

**Justificativa:**
- LGPD: não reter dados pessoais além do necessário (90 dias)
- SOX: reter logs de auditoria por 7 anos (compliance financeiro)

**Impacto:** Médio (job diário para deletar logs expirados)

### Decisão 6: Health Checks `/health` Endpoint

**Justificativa:**
- Kubernetes liveness/readiness probes (detectar pod unhealthy)
- Load balancer (remover servidor com problema do pool)

**Impacto:** Baixo (endpoint simples retornando JSON)

### Decisão 7: Alertas Proativos (PagerDuty)

**Justificativa:**
- Detectar problemas antes de usuário reportar (proativo, não reativo)
- SLA 99.9% exige resposta em minutos (não horas/dias)

**Impacto:** Médio (integração com PagerDuty/Opsgenie)

### Decisão 8: OpenTelemetry para Tracing Distribuído

**Justificativa:**
- Padrão W3C (vendor-neutral, não lock-in)
- Suporte nativo em Azure Application Insights

**Impacto:** Alto (instrumentação de todo código assíncrono)

---

## 8. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Mitigação |
|-------|---------|-----------|
| **Perda de logs durante transição** | Alto | Circuit breaker: se Seq/Elasticsearch falhar, escrever em arquivo local temporário |
| **Custo elevado Elasticsearch** | Médio | Sampling 10% sucesso + retenção automática 90 dias |
| **Overhead performance (logging síncrono)** | Médio | Logging assíncrono (queue interna Serilog) |
| **Mascaramento quebrar troubleshooting** | Médio | Mascarar apenas últimos 4 dígitos CPF (manter sufixo) |
| **Alertas falsos positivos (ruído)** | Baixo | Calibrar thresholds: error rate > 5% (não 1%) |
| **Tracing aumentar latência** | Baixo | Sampling 10% também em tracing (não 100%) |
| **Retenção 7 anos custar caro** | Médio | Apenas logs de segurança/auditoria 7 anos (não todos) |
| **Equipe não saber usar Seq/Grafana** | Baixo | Treinamento + documentação (guias de busca) |

---

## 9. RASTREABILIDADE

| Elemento Legado | Referência RF |
|-----------------|---------------|
| `LogError(mensagem As String)` em code-behind | RF-003 → RN-LOG-001 (logs estruturados JSON) |
| Arquivo `app.log` texto plano | RF-003 → Seção 2 (escopo incluso: agregação centralizada) |
| ❌ Sem correlation ID | RF-003 → RN-LOG-003 (correlation IDs obrigatórios) |
| ❌ CPF em texto claro | RF-003 → RN-LOG-004 (mascaramento automático) |
| ❌ Sem níveis de log | RF-003 → RN-LOG-002 (níveis configuráveis por ambiente) |
| ❌ Sem métricas | RF-003 → RN-LOG-009 (métricas RED) |
| ❌ Sem alertas | RF-003 → RN-LOG-011 (alertas automáticos) |
| ❌ Sem health checks | RF-003 → RN-LOG-010 (endpoint /health) |
| ❌ Sem tracing | RF-003 → RN-LOG-012 (tracing distribuído OpenTelemetry) |
| ❌ Sem retenção controlada | RF-003 → RN-LOG-008 (retenção automática 90d/1y/7y) |
| ❌ Sem interface web | RF-003 → Seção 4 (funcionalidades: busca full-text, dashboards) |
| Acesso via RDP + Notepad | RF-003 → Integração com Seq UI / Grafana (interface web) |

---

## EXEMPLO REAL DE LOG LEGADO

**Arquivo:** `D:\IC2\ic1_legado\IControlIT\IControlIT\logs\app.log`

**Conteúdo Típico:**

```
2023-10-15 14:23:45 - Usuário admin@test.com fez login
2023-10-15 14:24:12 - Erro ao salvar usuário: Object reference not set to an instance of an object
2023-10-15 14:25:33 - CPF 123.456.789-00 consultado
2023-10-15 14:26:01 - Senha do usuário: Admin@123
2023-10-15 14:27:15 - Erro ao conectar ao banco de dados: Timeout expired
```

**Problemas Identificados:**

1. ❌ **Formato texto não estruturado** - Impossível buscar "todos os erros de banco de dados do usuário X"
2. ❌ **CPF em texto claro** - Violação LGPD (dados pessoais não mascarados)
3. ❌ **Senha em texto claro** - Violação gravíssima de segurança
4. ❌ **Sem correlation ID** - Impossível rastrear request completo (login → consulta CPF)
5. ❌ **Sem nível de log** - "Erro" e "Info" misturados, impossível filtrar
6. ❌ **Sem contexto** - Qual IP? Qual navegador? Qual tenant?
7. ❌ **Timestamp sem timezone** - Problemas com servidores em timezones diferentes
8. ❌ **Sem stack trace** - "Object reference not set" é inútil sem linha de código

**Modernização (RF-003):**

```json
{
  "Timestamp": "2025-12-29T14:23:45.123Z",
  "Level": "Error",
  "Message": "Erro ao salvar usuário: FK constraint violation",
  "CorrelationId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "UserId": "admin@test.com",
  "TenantId": "tenant-123",
  "IP": "192.168.1.100",
  "UserAgent": "Mozilla/5.0",
  "Exception": {
    "Type": "DbUpdateException",
    "Message": "FK constraint violation",
    "StackTrace": "at IControlIT.Infrastructure.Persistence.ApplicationDbContext.SaveChangesAsync() in /src/Infrastructure/Persistence/ApplicationDbContext.cs:line 127"
  }
}
```

**Melhorias:**
- ✅ JSON estruturado (pesquisável por campos)
- ✅ Correlation ID (rastrear request completo)
- ✅ Timestamp ISO 8601 com timezone
- ✅ Nível de log (Error)
- ✅ Contexto completo (User, Tenant, IP, UserAgent)
- ✅ Stack trace completo (linha de código)
- ✅ Sem dados sensíveis vazados (CPF/senha mascarados se presentes)

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|--------|------|-----------|-------|
| 1.0 | 2025-12-29 | Versão inicial - Referência ao Legado do RF-003 (Sistema de Logs) | Agência ALC - alc.dev.br |
