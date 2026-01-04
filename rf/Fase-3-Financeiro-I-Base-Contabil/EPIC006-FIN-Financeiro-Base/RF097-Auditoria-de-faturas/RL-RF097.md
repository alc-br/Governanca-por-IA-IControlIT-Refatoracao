# RL-RF097 — Referência ao Legado (Auditoria de Faturas)

**Versão:** 1.0
**Data:** 2025-12-31
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF-097 (Auditoria de Faturas - NF-e e Documentos Fiscais)
**Sistema Legado:** IControlIT v1.0 (VB.NET + ASP.NET Web Forms + SQL Server 2012)
**Objetivo:** Documentar o comportamento do sistema legado de auditoria fiscal (NF-e, SEFAZ, SPED Fiscal) para garantir rastreabilidade, entendimento histórico e mitigação de riscos durante a modernização para .NET 10 + Angular 19.

---

## 1. CONTEXTO DO LEGADO

Descreve o cenário geral do sistema legado de Auditoria de Faturas.

- **Arquitetura:** Monolítica, Cliente-Servidor (WebForms + SQL Server)
- **Linguagem / Stack:** VB.NET (ASP.NET Web Forms 4.8), SOAP WebServices (.asmx), JavaScript/jQuery (frontend)
- **Banco de Dados:** SQL Server 2012 (stored procedures pesadas, views complexas, triggers)
- **Multi-tenant:** Sim (campo `ClienteId` em todas as tabelas, sem Row-Level Security automático)
- **Auditoria:** Parcial (campos `DataCriacao`, `UsuarioCriacao`, mas sem log de auditoria automático)
- **Configurações:** Web.config (connectionStrings, certificado digital A1, chaves SEFAZ), parâmetros em tabela `Parametro`
- **Integrações:** SEFAZ via SOAP (sem retry exponencial), sem Machine Learning, importação manual de XML

**Problemas Identificados no Legado:**
1. ❌ **Timeout SEFAZ sem retry**: Consulta ao SEFAZ travava a aplicação se o WebService ficasse indisponível (> 2 minutos de timeout)
2. ❌ **Validação manual de assinatura digital**: Validação de certificado A1/A3 era opcional, permitindo NF-e inválidas
3. ❌ **Sem detecção automática de fraudes**: Duplicatas e operações anômalas eram detectadas apenas em auditoria manual
4. ❌ **SQL Injection em queries dinâmicas**: Stored procedures concatenavam strings diretamente (ex: `sp_BuscarNFe`)
5. ❌ **Sem isolamento tenant**: Queries não validavam `ClienteId`, permitindo data leakage entre clientes
6. ❌ **Sem i18n**: Mensagens hardcoded em português no código VB.NET
7. ❌ **Relatórios gerados em servidor (RDLC)**: Processamento síncrono, travava interface durante geração
8. ❌ **Sem alertas em tempo real**: Alertas eram gerados em batch (1x por dia via SQL Server Job)

---

## 2. TELAS DO LEGADO

### Tela 1: AuditoriaFatura.aspx

- **Caminho:** `D:\IC2\ic1_legado\IControlIT\Financeiro\AuditoriaFatura.aspx`
- **Responsabilidade:** Consulta auditorias de NF-e realizadas, exibe resultado de validações (SEFAZ, impostos, assinatura digital)

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|------|------|-------------|-------------|
| `txtChaveAcesso` | TextBox | Sim | Chave de acesso NF-e (44 dígitos). Validação manual no code-behind |
| `ddlClienteId` | DropDownList | Sim | Lista de clientes (multi-tenancy). Populado via `sp_ListarClientes` |
| `ddlStatusAuditoria` | DropDownList | Não | Filtro por status ("Pendente", "Auditado", "Erro") |
| `gvAuditorias` | GridView | - | Exibe auditorias. Botões: "Detalhar", "Consultar SEFAZ", "Gerar Relatório" |

#### Comportamentos Implícitos

- **Validação ClienteId:** Não valida se usuário logado tem acesso ao cliente selecionado (data leakage!)
- **Timeout SEFAZ:** Se consulta ao SEFAZ demorar > 2min, trava a página (sem async)
- **Sem paginação:** GridView carrega todas as auditorias do cliente (problema de performance para > 10k registros)
- **Hardcoded messages:** Mensagens de erro em português direto no código (`MsgBox "NF-e inválida!"`)
- **Download relatório síncrono:** Gerar relatório fiscal trava a tela por até 5 minutos

**Destino:** ❌ **SUBSTITUÍDO** — Tela será substituída por componente Angular 19 com API REST assíncrona

---

### Tela 2: ConsultaSEFAZ.aspx

- **Caminho:** `D:\IC2\ic1_legado\IControlIT\Financeiro\ConsultaSEFAZ.aspx`
- **Responsabilidade:** Consulta status de NF-e no WebService SEFAZ (autorizada, cancelada, denegada)

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|------|------|-------------|-------------|
| `txtChaveAcesso` | TextBox | Sim | Chave de acesso NF-e |
| `txtCNPJEmitente` | TextBox | Sim | CNPJ do emitente (validação via máscara JavaScript) |
| `btnConsultar` | Button | - | Dispara consulta SEFAZ via SOAP |
| `lblStatusSEFAZ` | Label | - | Exibe status retornado: "100" (Autorizado), "101" (Cancelado), "102" (Denegado) |

#### Comportamentos Implícitos

- **Timeout sem retry:** Se SEFAZ não responder em 120s, retorna erro genérico "Timeout" (sem retry exponencial)
- **Certificado digital hardcoded:** Certificado A1 está no Web.config (não usa Azure Key Vault)
- **Sem cache:** Consulta SEFAZ mesmo se já consultou recentemente (duplica chamadas)
- **Log manual:** Histórico de consultas é salvo manualmente via `INSERT INTO ConsultaSEFAZ`

**Destino:** ❌ **SUBSTITUÍDO** — Será migrado para `SefazService` (.NET 10) com retry exponencial (Polly) + cache Redis

---

### Tela 3: RelatorioFiscal.aspx

- **Caminho:** `D:\IC2\ic1_legado\IControlIT\Financeiro\RelatorioFiscal.aspx`
- **Responsabilidade:** Gera relatórios fiscais (Livro Fiscal, Apuração ICMS, SPED Fiscal)

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|------|------|-------------|-------------|
| `ddlTipoRelatorio` | DropDownList | Sim | "Livro Fiscal", "Apuração ICMS", "SPED Fiscal" |
| `txtDataInicio` | TextBox | Sim | Data início do período (validação manual) |
| `txtDataFim` | TextBox | Sim | Data fim do período |
| `btnGerar` | Button | - | Gera relatório RDLC (síncrono) |

#### Comportamentos Implícitos

- **Processamento síncrono:** Geração de relatório trava a interface (sem background job)
- **Sem validação de período:** Aceita períodos > 1 ano (pode travar banco de dados)
- **Hardcoded RDLC:** Relatórios em formato RDLC não permitem customização por cliente
- **Sem exportação CSV/Excel:** Apenas PDF e impressão direta

**Destino:** ❌ **SUBSTITUÍDO** — Relatórios serão gerados via API REST + Hangfire (background job) + Angular (download assíncrono)

---

### Tela 4: AlertasFatura.aspx

- **Caminho:** `D:\IC2\ic1_legado\IControlIT\Financeiro\AlertasFatura.aspx`
- **Responsabilidade:** Exibe alertas críticos de auditoria (NF-e cancelada, duplicatas, impostos divergentes)

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|------|------|-------------|-------------|
| `gvAlertas` | GridView | - | Lista alertas. Colunas: Tipo, Severidade, Descrição, Data |
| `ddlSeveridade` | DropDownList | Não | Filtro por severidade ("Crítico", "Aviso", "Informação") |
| `btnResolver` | Button | - | Marca alerta como resolvido (sem auditoria de quem resolveu) |

#### Comportamentos Implícitos

- **Alertas gerados em batch:** SQL Server Job roda 1x por dia às 23h (não é tempo real)
- **Sem notificação push:** Usuário precisa abrir tela manualmente para ver alertas
- **Resolução sem auditoria:** Marca alerta como resolvido mas não registra usuário nem justificativa

**Destino:** ❌ **SUBSTITUÍDO** — Alertas serão gerados em tempo real (SignalR) com notificação push + auditoria completa (quem resolveu, quando, justificativa)

---

### Tela 5: DashboardFiscal.aspx

- **Caminho:** `D:\IC2\ic1_legado\IControlIT\Financeiro\DashboardFiscal.aspx`
- **Responsabilidade:** Dashboard com KPIs fiscais (taxa de conformidade, tempo médio de auditoria)

#### Campos

| Campo | Tipo | Observações |
|------|------|-------------|
| `lblTaxaConformidade` | Label | % de NF-e sem alertas críticos (calculado via stored procedure) |
| `lblTempoMedioAuditoria` | Label | Tempo médio em segundos (calculado via query agregada) |
| `chartAlertas` | Chart | Gráfico de barras com alertas por tipo (usando MS Chart Controls) |

#### Comportamentos Implícitos

- **Queries lentas:** KPIs calculados via stored procedures que fazem full table scan
- **Sem cache:** Dashboard recalcula KPIs a cada refresh (mesmo que dados não tenham mudado)
- **Gráficos desatualizados:** Chart Controls não atualizam em tempo real

**Destino:** ❌ **SUBSTITUÍDO** — Dashboard moderno com Angular + ApexCharts + API REST com cache Redis (atualização em tempo real via SignalR)

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

| Método | Local | Responsabilidade | Observações |
|------|-------|------------------|-------------|
| `ConsultarStatusSEFAZ(chaveAcesso, cnpj)` | `WSAuditoriaFatura.asmx.vb` | Consulta status NF-e no WebService SEFAZ | ❌ **SUBSTITUÍDO** — Migrar para `SefazService` com retry exponencial |
| `ValidarNFe(xmlContent, clienteId)` | `WSAuditoriaFatura.asmx.vb` | Valida XML NF-e (assinatura digital, chave, impostos) | ❌ **SUBSTITUÍDO** — Migrar para `ValidarNFeHandler` (CQRS) |
| `GerarRelatorioFiscal(dataInicio, dataFim)` | `WSAuditoriaFatura.asmx.vb` | Gera relatório fiscal (Livro Fiscal, SPED) | ❌ **SUBSTITUÍDO** — Migrar para `GerarRelatorioHandler` + Hangfire |
| `ListarAlertas(clienteId)` | `WSAuditoriaFatura.asmx.vb` | Lista alertas críticos | ❌ **SUBSTITUÍDO** — Migrar para `GET /api/auditoria-faturas/alertas` |

**Problemas Identificados:**
- **SOAP** (verboso, lento) → Migrar para **REST JSON**
- **Sem versionamento** → Implementar versionamento de API (`/v1/`, `/v2/`)
- **Sem autenticação OAuth** → Migrar para JWT Bearer Token
- **Sem rate limiting** → Implementar rate limiting (100 req/min)

---

## 4. TABELAS LEGADAS

| Tabela | Finalidade | Problemas Identificados |
|-------|------------|-------------------------|
| `NotaFiscal` | Armazena dados de NF-e importadas | ❌ Sem auditoria automática, ❌ `ClienteId` sem índice, ❌ `XmlContent` em `ntext` (obsoleto) |
| `NotaFiscalItem` | Itens de NF-e (produtos, serviços) | ❌ Sem validação de NCM, ❌ Alíquotas sem validação por CFOP |
| `AuditoriaFatura` | Histórico de auditorias realizadas | ❌ `ResultadoJSON` em `ntext` (problema de performance), ❌ Sem soft delete |
| `AlertaFatura` | Alertas críticos gerados | ❌ Sem auditoria de resolução, ❌ `NivelSeveridade` sem ENUM |
| `ConsultaSEFAZ` | Histórico de consultas ao SEFAZ | ❌ Sem TTL (tabela cresce indefinidamente), ❌ Sem índice em `ChaveAcesso` |

**Destino de Tabelas:**
- `NotaFiscal` → ✅ **ASSUMIDO** — Migrar para `NotaFiscal` moderna (EF Core, auditoria automática, índices otimizados)
- `NotaFiscalItem` → ✅ **ASSUMIDO** — Migrar para `NotaFiscalItem` (validação de NCM + alíquotas)
- `AuditoriaFatura` → ✅ **SUBSTITUÍDO** — Nova tabela `AuditoriaFatura` com estados (pending, in_progress, completed)
- `AlertaFatura` → ✅ **SUBSTITUÍDO** — Nova tabela `AlertaFiscal` com ENUM de severidade + auditoria de resolução
- `ConsultaSEFAZ` → ✅ **ASSUMIDO** — Nova tabela `ConsultaSEFAZ` com TTL automático (30 dias) + cache Redis

---

## 5. STORED PROCEDURES LEGADOS

| Procedure | Responsabilidade | Problemas | Destino |
|-----------|------------------|-----------|---------|
| `sp_ConsultarStatusSEFAZ` | Consulta status NF-e no SEFAZ via SOAP | ❌ SQL Injection (concatena strings), ❌ Timeout sem retry | ❌ **SUBSTITUÍDO** — `SefazService` (.NET 10) |
| `sp_ValidarAliquotaICMS` | Valida alíquota ICMS conforme CFOP | ❌ Regras hardcoded (sem tabela de parâmetros) | ❌ **SUBSTITUÍDO** — `ValidarAliquotaICMSHandler` |
| `sp_VerificarDuplicatas` | Busca NF-e com mesma chave de acesso | ❌ Full table scan (sem índice em `ChaveAcesso`) | ❌ **SUBSTITUÍDO** — `ValidarDuplicataHandler` |
| `sp_GerarRelatorioFiscal` | Gera relatório Livro Fiscal / SPED | ❌ Processamento síncrono (trava banco por minutos) | ❌ **SUBSTITUÍDO** — `GerarRelatorioHandler` + Hangfire |
| `sp_AlertarInconsistencias` | Dispara alertas por email (batch 1x/dia) | ❌ Sem tempo real, ❌ Email hardcoded | ❌ **SUBSTITUÍDO** — `AlertaService` + SignalR (tempo real) |

**Exemplo de SQL Injection (sp_BuscarNFe - LEGADO):**
```sql
-- ❌ LEGADO (SQL Injection)
DECLARE @SQL NVARCHAR(MAX)
SET @SQL = 'SELECT * FROM NotaFiscal WHERE ChaveAcesso = ''' + @ChaveAcesso + ''''
EXEC sp_executesql @SQL

-- ✅ MODERNO (EF Core parameterizado)
context.NotaFiscal.Where(nf => nf.ChaveAcesso == chaveAcesso).ToListAsync()
```

---

## 6. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

Liste regras que não estavam documentadas formalmente (extraídas do código VB.NET e stored procedures).

### RL-RN-001: Validação Manual de Chave de Acesso NF-e
**Legado:** Validação de chave de acesso (44 dígitos, módulo 11) era feita manualmente em JavaScript no frontend. Backend não validava.
**Problema:** NF-e com chave inválida era salva no banco de dados.
**Destino:** ❌ **SUBSTITUÍDO** — Backend moderno valida chave (RN-AUF-097-001) via FluentValidation + rejeição HTTP 400

---

### RL-RN-002: Consulta SEFAZ Opcional (Apenas se Usuário Clicar)
**Legado:** Consulta ao SEFAZ não era automática. Usuário precisava clicar em "Consultar SEFAZ" manualmente.
**Problema:** NF-e canceladas no SEFAZ permaneciam como "Autorizadas" no sistema.
**Destino:** ✅ **SUBSTITUÍDO** — Consulta SEFAZ automática (RN-AUF-097-002) via Hangfire (job diário + sob demanda)

---

### RL-RN-003: Alíquota ICMS Hardcoded no Código
**Legado:** Alíquotas de ICMS por CFOP estavam hardcoded no código VB.NET (ex: `If CFOP = "5.102" Then AliquotaICMS = 18`).
**Problema:** Mudanças de legislação exigiam deploy de código.
**Destino:** ✅ **SUBSTITUÍDO** — Alíquotas parametrizadas em RF001 (tabela `ParametroFiscal`) + RN-AUF-097-003

---

### RL-RN-004: Detecção Manual de Duplicatas (Sem Alertas Automáticos)
**Legado:** Duplicatas eram detectadas apenas se usuário rodasse relatório específico ("Relatório de Duplicatas").
**Problema:** Duplicatas passavam despercebidas por meses.
**Destino:** ✅ **SUBSTITUÍDO** — Detecção automática (RN-AUF-097-007) com alerta crítico em tempo real (SignalR)

---

### RL-RN-005: Assinatura Digital Opcional
**Legado:** Validação de assinatura digital XML era opcional (checkbox "Validar Assinatura?").
**Problema:** NF-e com assinatura inválida eram aceitas.
**Destino:** ✅ **SUBSTITUÍDO** — Validação OBRIGATÓRIA (RN-AUF-097-005) + rejeição HTTP 400

---

### RL-RN-006: Base de Cálculo Não Validada
**Legado:** Sistema não recalculava base de cálculo de ICMS/IPI. Apenas salvava o valor da NF-e.
**Problema:** Valores divergentes passavam sem alerta.
**Destino:** ✅ **SUBSTITUÍDO** — Recálculo automático (RN-AUF-097-006) + alerta se divergência > R$ 0,10

---

### RL-RN-007: Sem Conformidade SPED Fiscal
**Legado:** Sistema não validava se NF-e estava escriturada no SPED Fiscal (EFD-ICMS/IPI).
**Problema:** NF-e não escrituradas resultavam em autuações.
**Destino:** ✅ **SUBSTITUÍDO** — Validação SPED automática (RN-AUF-097-008)

---

### RL-RN-008: Retenções Não Validadas
**Legado:** Sistema não validava retenções obrigatórias (IRRF, CSLL, ISS, INSS) para NF-e de serviços.
**Problema:** Retenções ausentes geravam multas.
**Destino:** ✅ **SUBSTITUÍDO** — Validação automática (RN-AUF-097-009) + alerta se retenção obrigatória ausente

---

### RL-RN-009: Sem Detecção de Fraudes (Machine Learning)
**Legado:** Sistema não detectava operações anômalas (valores fora do padrão, horários incomuns).
**Problema:** Fraudes eram detectadas apenas em auditoria manual (meses depois).
**Destino:** ✅ **SUBSTITUÍDO** — Azure ML (RN-AUF-097-010) para detecção de anomalias

---

### RL-RN-010: NF-e Cancelada com Movimentação Posterior Não Detectada
**Legado:** Sistema não verificava se NF-e cancelada tinha movimentações financeiras/estoque posteriores.
**Problema:** NF-e canceladas eram pagas/estocadas normalmente.
**Destino:** ✅ **SUBSTITUÍDO** — Detecção automática (RN-AUF-097-004) + bloqueio de movimentação

---

## 7. GAP ANALYSIS (LEGADO x RF MODERNO)

| Item | Legado | RF Moderno | Observação |
|-----|--------|------------|------------|
| **Validação Chave NF-e** | Frontend (JavaScript) | Backend (FluentValidation) | ✅ Validação server-side obrigatória (RN-AUF-097-001) |
| **Consulta SEFAZ** | Manual (clique do usuário) | Automática (Hangfire daily job) | ✅ Job diário + sob demanda (RN-AUF-097-002) |
| **Retry SEFAZ** | Sem retry (falha imediata) | Retry exponencial (Polly) | ✅ 3 tentativas com backoff (5s, 30s, 120s) |
| **Assinatura Digital** | Opcional (checkbox) | Obrigatória | ✅ Validação sempre executada (RN-AUF-097-005) |
| **Detecção Duplicatas** | Manual (relatório) | Automática (tempo real) | ✅ Alerta crítico imediato (RN-AUF-097-007) |
| **Alertas** | Batch (1x/dia) | Tempo real (SignalR) | ✅ Notificação push + email |
| **Relatórios** | Síncrono (RDLC) | Assíncrono (Hangfire) | ✅ Background job + download quando pronto |
| **Multi-tenancy** | Manual (`WHERE ClienteId = @ClienteId`) | Automático (Global Query Filter) | ✅ Row-Level Security |
| **i18n** | Sem suporte | Transloco (pt-BR, en, es) | ✅ 16 pontos de tradução |
| **Auditoria** | Parcial (DataCriacao) | Completa (AuditInterceptor) | ✅ Quem, quando, o quê, IP |
| **Machine Learning** | Inexistente | Azure ML (detecção fraude) | ✅ Score de anomalia (RN-AUF-097-010) |
| **SPED Fiscal** | Não validado | Validação automática | ✅ Conformidade EFD-ICMS/IPI (RN-AUF-097-008) |
| **Retenções** | Não validadas | Validação automática | ✅ IRRF, CSLL, ISS, INSS (RN-AUF-097-009) |

---

## 8. DECISÕES DE MODERNIZAÇÃO

### Decisão 1: Migrar de SOAP para REST

- **Motivo:** SOAP é verboso, lento, difícil de debugar. REST JSON é padrão moderno.
- **Impacto:** Alto (quebra integrações externas que consomem SOAP)
- **Mitigação:** Manter endpoint SOAP legado temporário (6 meses) + documentar migração para REST

---

### Decisão 2: Consulta SEFAZ Automática (Diária)

- **Motivo:** Legado exigia clique manual. Usuários esqueciam, resultando em NF-e canceladas não detectadas.
- **Impacto:** Médio (aumento de chamadas ao SEFAZ - precisa validar limite de requisições)
- **Mitigação:** Job Hangfire 1x/dia (madrugada) + cache Redis (evitar consultas duplicadas)

---

### Decisão 3: Validação de Assinatura Digital Obrigatória

- **Motivo:** Legado permitia desabilitar validação. Risco fiscal alto (NF-e inválidas aceitas).
- **Impacto:** Alto (pode rejeitar NF-e legítimas se certificado estiver expirado)
- **Mitigação:** Alert se certificado expira em < 30 dias + documentação clara sobre renovação

---

### Decisão 4: Machine Learning para Detecção de Fraudes

- **Motivo:** Legado não detectava anomalias. Azure ML oferece detecção automática.
- **Impacto:** Médio (custo Azure ML + falsos positivos)
- **Mitigação:** Modelo treinado com dados históricos + threshold ajustável (0.75 padrão) + Feature Flag para habilitar/desabilitar

---

### Decisão 5: Migrar Relatórios RDLC para Hangfire + Angular

- **Motivo:** RDLC trava interface. Hangfire permite geração assíncrona.
- **Impacto:** Alto (usuários acostumados com PDF instantâneo)
- **Mitigação:** Notificação push quando relatório estiver pronto + fallback para geração síncrona (relatórios pequenos < 1000 registros)

---

### Decisão 6: Soft Delete em Todas as Tabelas

- **Motivo:** Legado deletava fisicamente (sem rastreabilidade). SPED exige retenção de 5 anos.
- **Impacto:** Baixo (queries precisam incluir `WHERE DeletedAt IS NULL`)
- **Mitigação:** Global Query Filter do EF Core (automático)

---

### Decisão 7: Row-Level Security Automático (Multi-tenancy)

- **Motivo:** Legado exigia `WHERE ClienteId = @ClienteId` manual (risco de data leakage).
- **Impacto:** Médio (pode quebrar queries legacy)
- **Mitigação:** Global Query Filter + auditorias de segurança antes do deploy

---

## 9. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Mitigação |
|------|---------|-----------|
| **NF-e cancelada não detectada (consulta SEFAZ falha)** | ALTO | Retry exponencial (Polly) + alerta se SEFAZ indisponível > 1h |
| **Certificado A1/A3 expirado bloqueia todas as NF-e** | CRÍTICO | Alert 30 dias antes da expiração + validação não bloqueia importação (apenas alerta) |
| **Duplicatas não detectadas (bug na validação)** | ALTO | Testes automatizados (TC-UC00-listar-duplicatas) + validação dupla (banco + cache Redis) |
| **Data leakage (ClienteId não validado)** | CRÍTICO | Global Query Filter + testes de segurança (tentar acessar dados de outro tenant) |
| **Timeout SEFAZ trava aplicação** | MÉDIO | Timeout 120s + retry 3x + fallback para validação local |
| **Azure ML gera muitos falsos positivos** | MÉDIO | Threshold ajustável (0.75 padrão) + Feature Flag + re-treinar modelo com feedback |
| **Relatórios assíncronos confundem usuários** | BAIXO | Tutorial in-app + fallback para geração síncrona (relatórios pequenos) |
| **SPED Fiscal não validado corretamente** | ALTO | Validação com contador externo + testes com dados reais de produção |
| **Retenções calculadas incorretamente** | ALTO | Validação com tabela de parâmetros (RF001) + testes com cenários reais |
| **Alertas em tempo real sobrecarregam usuários** | BAIXO | Filtro por severidade (apenas críticos por padrão) + opção de desabilitar |

---

## 10. RASTREABILIDADE

| Elemento Legado | Referência RF Moderno |
|----------------|---------------|
| `AuditoriaFatura.aspx` | `GET /api/auditoria-faturas` + componente Angular `auditoria-faturas-list.component.ts` |
| `ConsultaSEFAZ.aspx` | `POST /api/auditoria-faturas/{id}/consultar-sefaz` + `SefazService` |
| `RelatorioFiscal.aspx` | `GET /api/auditoria-faturas/relatorios/livro-fiscal` + Hangfire job |
| `AlertasFatura.aspx` | `GET /api/auditoria-faturas/{id}/alertas` + SignalR hub |
| `DashboardFiscal.aspx` | `GET /api/auditoria-faturas/dashboard` + ApexCharts |
| `sp_ConsultarStatusSEFAZ` | `SefazService.ConsultarStatusAsync()` |
| `sp_ValidarAliquotaICMS` | `ValidarAliquotaICMSHandler` (CQRS Command) |
| `sp_VerificarDuplicatas` | `ValidarDuplicataHandler` (CQRS Query) |
| `sp_GerarRelatorioFiscal` | `GerarRelatorioHandler` + Hangfire |
| `sp_AlertarInconsistencias` | `AlertaService` + SignalR |
| Tabela `NotaFiscal` | Entidade `NotaFiscal` (EF Core) |
| Tabela `AuditoriaFatura` | Entidade `AuditoriaFatura` (EF Core) |
| Tabela `AlertaFatura` | Entidade `AlertaFiscal` (EF Core) |
| Tabela `ConsultaSEFAZ` | Entidade `ConsultaSEFAZ` (EF Core) |
| `WSAuditoriaFatura.asmx` | API REST `/api/auditoria-faturas` (Minimal APIs) |

---

## 11. MAPEAMENTO DE CAMPOS (LEGADO → MODERNO)

| Campo Legado | Tabela Legado | Campo Moderno | Tabela Moderna | Observação |
|--------------|---------------|---------------|----------------|------------|
| `ChaveAcesso` | `NotaFiscal` | `ChaveAcesso` | `NotaFiscal` | ✅ ASSUMIDO (validação obrigatória adicionada) |
| `StatusSEFAZ` | `NotaFiscal` | `StatusSEFAZ` | `NotaFiscal` | ✅ ASSUMIDO (consulta automática adicionada) |
| `XmlContent` | `NotaFiscal` | `XmlContent` | `NotaFiscal` | ✅ SUBSTITUÍDO (`ntext` → `nvarchar(MAX)`) |
| `AliquotaICMS` | `NotaFiscalItem` | `AliquotaICMS` | `NotaFiscalItem` | ✅ ASSUMIDO (validação por CFOP adicionada) |
| `StatusAuditoria` | `AuditoriaFatura` | `Status` | `AuditoriaFatura` | ✅ SUBSTITUÍDO (varchar → ENUM de estados) |
| `ResultadoJSON` | `AuditoriaFatura` | `ResultadoJson` | `AuditoriaFatura` | ✅ SUBSTITUÍDO (`ntext` → `nvarchar(MAX)` + JSON Schema validado) |
| `TipoAlerta` | `AlertaFatura` | `TipoAlerta` | `AlertaFiscal` | ✅ ASSUMIDO (ENUM criado) |
| `NivelSeveridade` | `AlertaFatura` | `Severidade` | `AlertaFiscal` | ✅ SUBSTITUÍDO (varchar → ENUM: CRITICA, IMPORTANTE, INFORMACAO) |
| `ClienteId` | (todas as tabelas) | `EmpresaId` | (todas as tabelas) | ✅ SUBSTITUÍDO (renomeado para padrão multi-tenancy moderno) |

---

## 12. STORED PROCEDURES DETALHADAS (CÓDIGO LEGADO)

### sp_ConsultarStatusSEFAZ (LEGADO)

**Arquivo:** `D:\IC2\ic1_legado\Database\StoredProcedures\sp_ConsultarStatusSEFAZ.sql`

**Código (resumido):**
```sql
CREATE PROCEDURE [dbo].[sp_ConsultarStatusSEFAZ]
    @ChaveAcesso VARCHAR(44),
    @ClienteId INT
AS
BEGIN
    -- ❌ SQL Injection (concatenação direta)
    DECLARE @SQL NVARCHAR(MAX)
    SET @SQL = 'SELECT * FROM NotaFiscal WHERE ChaveAcesso = ''' + @ChaveAcesso + ''' AND ClienteId = ' + CAST(@ClienteId AS VARCHAR)

    -- ❌ Sem validação de ClienteId do usuário logado (data leakage!)
    EXEC sp_executesql @SQL

    -- ❌ Timeout SEFAZ sem retry (bloqueia até 120s)
    -- [Código VB.NET faz chamada SOAP síncrona]
END
```

**Problemas:**
1. SQL Injection via concatenação de `@ChaveAcesso`
2. Data leakage (não valida se usuário tem acesso ao `ClienteId`)
3. Timeout sem retry (120s fixo)

**Destino:** ❌ **SUBSTITUÍDO** — Migrar para `SefazService.ConsultarStatusAsync()` com:
- Parâmetros EF Core (sem SQL Injection)
- Row-Level Security (Global Query Filter)
- Retry exponencial (Polly: 5s, 30s, 120s)

---

### sp_ValidarAliquotaICMS (LEGADO)

**Código (resumido):**
```sql
CREATE PROCEDURE [dbo].[sp_ValidarAliquotaICMS]
    @CFOP VARCHAR(10),
    @AliquotaICMS DECIMAL(5,2)
AS
BEGIN
    -- ❌ Alíquotas hardcoded (sem tabela de parâmetros)
    DECLARE @AliquotaEsperada DECIMAL(5,2)

    IF @CFOP = '5.102'
        SET @AliquotaEsperada = 18.00
    ELSE IF @CFOP = '5.405'
        SET @AliquotaEsperada = 12.00
    ELSE IF @CFOP = '5.933'
        SET @AliquotaEsperada = 0.00 -- Serviço (sem ICMS)
    ELSE
        SET @AliquotaEsperada = 18.00 -- Default (pode estar errado!)

    -- ❌ Validação simples (sem range de tolerância)
    IF @AliquotaICMS <> @AliquotaEsperada
        RAISERROR('Alíquota ICMS divergente', 16, 1)
END
```

**Problemas:**
1. Alíquotas hardcoded (mudança de legislação exige deploy)
2. Sem range de tolerância (±2%)
3. Default genérico (18%) pode estar errado

**Destino:** ❌ **SUBSTITUÍDO** — Migrar para `ValidarAliquotaICMSHandler` com:
- Tabela `ParametroFiscal` (RF001) para alíquotas
- Range de tolerância (±2%)
- Sem default genérico (rejeita se CFOP desconhecido)

---

### sp_VerificarDuplicatas (LEGADO)

**Código (resumido):**
```sql
CREATE PROCEDURE [dbo].[sp_VerificarDuplicatas]
    @ChaveAcesso VARCHAR(44),
    @ClienteId INT
AS
BEGIN
    -- ❌ Full table scan (sem índice em ChaveAcesso)
    SELECT COUNT(*) AS Duplicatas
    FROM NotaFiscal
    WHERE ChaveAcesso = @ChaveAcesso
      AND ClienteId = @ClienteId

    -- ❌ Não verifica CNPJ duplicado (mesma numeração no mês)
END
```

**Problemas:**
1. Full table scan (lento para > 100k registros)
2. Não detecta CNPJ duplicado (mesma numeração + série no mês)

**Destino:** ❌ **SUBSTITUÍDO** — Migrar para `ValidarDuplicataHandler` com:
- Índice composto: `(ChaveAcesso, ClienteId)`
- Validação adicional: `(CNPJ, Numero, Serie, MesEmissao)`
- Cache Redis (evitar queries repetidas)

---

## 13. WEBSERVICES LEGADOS DETALHADOS (VB.NET)

### WSAuditoriaFatura.asmx.vb

**Arquivo:** `D:\IC2\ic1_legado\IControlIT\WebService\WSAuditoriaFatura.asmx.vb`

**Código (resumido):**

```vb
' ❌ LEGADO (VB.NET + SOAP)
<WebMethod()> _
Public Function ConsultarStatusSEFAZ(ByVal chaveAcesso As String, ByVal cnpj As String) As String
    ' ❌ Sem validação de formato (aceita chave inválida)
    ' ❌ Sem retry (falha na primeira tentativa)
    ' ❌ Timeout 120s fixo (bloqueia thread)

    Dim soapClient As New SefazService.NFeStatusServicoSoapClient()
    Dim resultado As String = soapClient.ConsultarStatus(chaveAcesso, cnpj)

    ' ❌ Sem log de auditoria
    ' ❌ Sem cache (consulta SEFAZ mesmo se já consultou hoje)

    Return resultado
End Function
```

**Problemas:**
1. Sem validação de entrada (aceita chave inválida)
2. Sem retry (falha imediata se SEFAZ indisponível)
3. Timeout fixo 120s (bloqueia thread)
4. Sem log de auditoria
5. Sem cache (duplica consultas SEFAZ)

**Destino:** ❌ **SUBSTITUÍDO** — Migrar para:
```csharp
// ✅ MODERNO (.NET 10 + REST)
[HttpPost("api/auditoria-faturas/{id}/consultar-sefaz")]
[Authorize(Policy = AuthorizationPolicies.SefazConsulta)]
public async Task<IActionResult> ConsultarSefaz(Guid id)
{
    // ✅ Validação de entrada (FluentValidation)
    // ✅ Retry exponencial (Polly: 5s, 30s, 120s)
    // ✅ Timeout async (não bloqueia thread)
    // ✅ Log de auditoria automático (AuditInterceptor)
    // ✅ Cache Redis (30min TTL)

    var resultado = await _sefazService.ConsultarStatusAsync(id);
    return Ok(resultado);
}
```

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|------|------|----------|------|
| 1.0 | 2025-12-31 | Versão inicial de Referência ao Legado (RL-RF097) — Extração completa de Seção 3 do RF097.md v1.0. Documentação de telas ASPX, stored procedures, WebServices VB.NET, tabelas SQL Server, regras de negócio implícitas e gap analysis (LEGADO x MODERNO). Todos os itens possuem destino explícito: ASSUMIDO, SUBSTITUÍDO ou DESCARTADO. | Agência ALC - alc.dev.br |

---

**Última Atualização:** 2025-12-31
**Autor:** Agência ALC - alc.dev.br
**Revisão:** Pendente
