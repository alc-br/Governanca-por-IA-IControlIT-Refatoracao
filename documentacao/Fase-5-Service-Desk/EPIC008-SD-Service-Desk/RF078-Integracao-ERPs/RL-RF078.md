# RL-RF078 — Referência ao Legado (Integração com ERPs)

**Versão:** 1.0
**Data:** 2025-12-30
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF078 - Integração com ERPs
**Sistema Legado:** VB.NET + ASP.NET Web Forms
**Objetivo:** Documentar o comportamento do sistema legado de integrações com ERPs que serve de base para a refatoração, garantindo rastreabilidade, entendimento histórico e mitigação de riscos.

---

## 1. CONTEXTO DO LEGADO

### 1.1 Stack Tecnológica

- **Arquitetura:** Monolítica WebForms com batch jobs diários
- **Linguagem:** VB.NET (Framework .NET 4.5)
- **Frontend:** ASP.NET Web Forms com ViewState
- **Integração SAP:** RFC ABAP manual sem criptografia
- **Integração TOTVS:** SOAP WebServices com autenticação básica
- **Banco de Dados:** SQL Server 2012 com múltiplos bancos por cliente
- **Multi-tenant:** Não implementado (bancos separados por cliente)
- **Auditoria:** Logs em arquivo de texto plano
- **Configurações:** Hardcoded em web.config

### 1.2 Problemas Arquiteturais Identificados

1. **Credenciais Hardcoded**: Senhas e tokens de API armazenados em web.config sem criptografia
2. **Falta de Retry Automático**: Falhas de integração não eram retentadas automaticamente
3. **Logs Não Estruturados**: Logs em arquivos de texto sem possibilidade de consulta SQL
4. **Sincronização Batch**: Polling a cada 24h gerava latência de até 1 dia para refletir mudanças
5. **Falta de Deduplicação**: Mensagens duplicadas eram processadas 2x causando divergências
6. **Sem Validação de Schema**: Dados malformados causavam crashes silenciosos
7. **Falta de Dashboard**: Status de integrações verificado manualmente via SQL
8. **Sem Webhook**: Polling periódico desperdiçava recursos e aumentava latência

---

## 2. TELAS DO LEGADO

### Tela 1: frmIntegracaoERP.aspx

- **Caminho:** `D:\IC2\ic1_legado\IControlIT\Admin\Integracao\frmIntegracaoERP.aspx`
- **Responsabilidade:** Dashboard manual de integrações com SAP e TOTVS

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|------|------|-------------|-------------|
| `ddlTipoERP` | DropDownList | Sim | SAP, TOTVS, ORACLE |
| `ddlTipoOperacao` | DropDownList | Sim | IMPORT_NF, EXPORT_CUSTO, SYNC_RH |
| `txtDataInicio` | TextBox (Date) | Sim | Data inicial para filtro de logs |
| `txtDataFim` | TextBox (Date) | Sim | Data final para filtro de logs |
| `gridLogs` | GridView | Não | Exibe logs de integrações |

#### Comportamentos Implícitos

- Paginação manual do GridView com ViewState (performance ruim)
- Filtros aplicados via postback (reload completo da página)
- Sem refresh automático (usuário precisava clicar F5)
- Logs limitados a 1000 registros (registros antigos inacessíveis)

**DESTINO:** SUBSTITUÍDO

---

### Tela 2: frmConfiguracaoERP.aspx

- **Caminho:** `D:\IC2\ic1_legado\IControlIT\Admin\Integracao\frmConfiguracaoERP.aspx`
- **Responsabilidade:** Configuração de credenciais e endpoints do ERP

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|------|------|-------------|-------------|
| `txtNomeERP` | TextBox | Sim | Nome do ERP (SAP, TOTVS, ORACLE) |
| `txtUsuario` | TextBox | Sim | Usuário de integração |
| `txtSenha` | TextBox (Password) | Sim | Senha em texto plano no banco |
| `txtHostRFC` | TextBox | Não | Host RFC para SAP |
| `txtPortaRFC` | TextBox | Não | Porta RFC para SAP |
| `chkAtiva` | CheckBox | Não | Habilitar/desabilitar integração |

#### Comportamentos Implícitos

- Senha armazenada em texto plano na tabela `tbCredencialERP`
- Sem rotação automática de credenciais
- Sem validação de conexão (teste apenas em produção)
- Alteração de credencial não auditada

**DESTINO:** SUBSTITUÍDO

---

### Tela 3: frmLogIntegracao.aspx

- **Caminho:** `D:\IC2\ic1_legado\IControlIT\Admin\Integracao\frmLogIntegracao.aspx`
- **Responsabilidade:** Visualização detalhada de logs de integração

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|------|------|-------------|-------------|
| `lblMessageId` | Label | Não | Não existia UUID, usado ID autoincrement |
| `lblTipoIntegracao` | Label | Não | Tipo de operação |
| `lblDataExecucao` | Label | Não | Data/hora da execução |
| `lblStatus` | Label | Não | SUCESSO ou ERRO |
| `txtMensagemErro` | TextBox (MultiLine) | Não | Mensagem de erro em texto livre |

#### Comportamentos Implícitos

- Não exibia payload de entrada/saída (impossível debug)
- Mensagem de erro truncada em 1000 caracteres
- Sem export para CSV ou JSON
- Sem paginação (limitado a 100 registros)

**DESTINO:** SUBSTITUÍDO

---

### Tela 4: frmReconciliacao.aspx

- **Caminho:** `D:\IC2\ic1_legado\IControlIT\Financeiro\frmReconciliacao.aspx`
- **Responsabilidade:** Reconciliação manual de faturas telecom com contas a pagar do ERP

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|------|------|-------------|-------------|
| `gridFaturasPendentes` | GridView | Não | Faturas sem reconciliação |
| `gridContasPagar` | GridView | Não | Contas a pagar do ERP |
| `btnReconciliar` | Button | Não | Matching manual |
| `txtDiferencaTolerada` | TextBox | Não | Percentual de tolerância (padrão 0,5%) |

#### Comportamentos Implícitos

- Reconciliação 100% manual (nenhum matching automático)
- Usuário precisava encontrar visualmente a correspondência
- Diferença de valor não calculada automaticamente
- Sem auditoria de quem reconciliou

**DESTINO:** SUBSTITUÍDO

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

### WebService 1: WSIntegracaoERP.asmx

| Método | Local | Responsabilidade | Observações |
|------|-------|------------------|-------------|
| `ImportarNotaFiscal(xmlNF As String)` | `D:\IC2\ic1_legado\IControlIT\WebService\WSIntegracaoERP.asmx.vb` | Importa NF-e do ERP (SAP RFC) | Parsing XML manual em VB.NET |
| `ExportarCustosTI(mes As Integer, ano As Integer)` | `D:\IC2\ic1_legado\IControlIT\WebService\WSIntegracaoERP.asmx.vb` | Exporta custos para contabilização | Sem validação de período aberto |
| `ValidarSincronizacao(tipo As String)` | `D:\IC2\ic1_legado\IControlIT\WebService\WSIntegracaoERP.asmx.vb` | Valida status de sincronização | Retorna apenas "OK" ou "ERRO" |
| `ObterLogIntegracao(idIntegracao As Integer)` | `D:\IC2\ic1_legado\IControlIT\WebService\WSIntegracaoERP.asmx.vb` | Retorna logs detalhados de uma execução | Sem filtro por data ou tipo |

**DESTINO:** SUBSTITUÍDO

---

## 4. TABELAS LEGADAS

### Tabela 1: tbCentroCusto

| Tabela | Finalidade | Problemas Identificados |
|-------|------------|-------------------------|
| `tbCentroCusto` | Armazena centros de custo importados do ERP | - Falta de FK para validar relacionamento<br>- Campo `codigoErp` aceita NULL (centros sem mapeamento)<br>- Sem índice em `codigoErp` (performance ruim)<br>- Sem auditoria (Created, Modified) |

**DDL Original:**
```sql
CREATE TABLE [dbo].[tbCentroCusto](
    [id] [int] IDENTITY(1,1) PRIMARY KEY,
    [codigo] [varchar](20) NOT NULL UNIQUE,
    [descricao] [varchar](100) NOT NULL,
    [ativo] [bit] DEFAULT 1,
    [codigoErp] [varchar](20) NULL,
    [dataCriacao] [datetime] DEFAULT GETDATE()
);
```

**DESTINO:** SUBSTITUÍDO

---

### Tabela 2: tbIntegracaoERP

| Tabela | Finalidade | Problemas Identificados |
|-------|------------|-------------------------|
| `tbIntegracaoERP` | Registra execuções de integrações com ERP | - Sem campo MessageId (impossível deduplicação)<br>- Sem payload de entrada/saída (impossível debug)<br>- Sem retenção definida (cresce indefinidamente)<br>- Sem índice em `dataExecucao` (consultas lentas) |

**DDL Original:**
```sql
CREATE TABLE [dbo].[tbIntegracaoERP](
    [id] [int] IDENTITY(1,1) PRIMARY KEY,
    [tipoErp] [varchar](20), -- 'SAP', 'TOTVS', 'ORACLE'
    [tipoOperacao] [varchar](50), -- 'IMPORT_NF', 'EXPORT_CUSTO', 'SYNC_RH'
    [dataExecucao] [datetime],
    [status] [varchar](20), -- 'SUCESSO', 'ERRO'
    [mensagemErro] [nvarchar](max) NULL,
    [quantidadeRegistros] [int],
    [tempoExecucaoMs] [int]
);
```

**DESTINO:** SUBSTITUÍDO

---

### Tabela 3: tbCredencialERP

| Tabela | Finalidade | Problemas Identificados |
|-------|------------|-------------------------|
| `tbCredencialERP` | Armazena credenciais de acesso aos ERPs | - **CRÍTICO:** Senhas em texto plano<br>- Sem rotação automática<br>- Sem auditoria de leitura de credencial<br>- Sem criptografia de certificados RFC |

**DDL Original:**
```sql
CREATE TABLE [dbo].[tbCredencialERP](
    [id] [int] IDENTITY(1,1) PRIMARY KEY,
    [nomeErp] [varchar](20),
    [usuario] [varchar](100),
    [senha] [varchar](max), -- DEPRECATED: texto plano
    [hostRFC] [varchar](50),
    [portaRFC] [int],
    [ativa] [bit]
);
```

**DESTINO:** DESCARTADO (migrado para Azure Key Vault)

---

## 5. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

### RL-RN-001: Sincronização de Centro de Custo era unidirecional (apenas import)

- **Descrição:** Centros de custo eram importados do SAP para IControlIT, mas mudanças em IControlIT não eram exportadas de volta para SAP.
- **Localização:** `D:\IC2\ic1_legado\IControlIT\Jobs\SyncCentroCusto.vb` - Linha 45
- **Impacto:** Divergências entre sistemas causavam inconsistências contábeis.

**DESTINO:** SUBSTITUÍDO

---

### RL-RN-002: Exportação de custos não validava período contábil

- **Descrição:** Custos eram exportados para SAP sem validar se o período estava aberto, causando erros silenciosos no ERP.
- **Localização:** `D:\IC2\ic1_legado\IControlIT\WebService\WSIntegracaoERP.asmx.vb` - Linha 120
- **Impacto:** Erros de contabilização descobertos apenas no fechamento mensal.

**DESTINO:** ASSUMIDO (validação implementada no moderno)

---

### RL-RN-003: Reconciliação de faturas com tolerância fixa de 1% (não configurável)

- **Descrição:** Diferença de até 1% entre fatura telecom e conta a pagar era aceita automaticamente, mas percentual era hardcoded.
- **Localização:** `D:\IC2\ic1_legado\IControlIT\Financeiro\ReconciliacaoService.vb` - Linha 78
- **Impacto:** Mudanças na tolerância exigiam recompilação e deploy.

**DESTINO:** ASSUMIDO (tolerância configurável em 0,5% no moderno)

---

### RL-RN-004: Retry de integração era manual (sem backoff exponencial)

- **Descrição:** Falhas de integração eram registradas em log, mas retry exigia intervenção manual do administrador.
- **Localização:** `D:\IC2\ic1_legado\IControlIT\Jobs\IntegracaoJob.vb` - Linha 200
- **Impacto:** Integrações falhavam silenciosamente durante indisponibilidades temporárias.

**DESTINO:** SUBSTITUÍDO (retry automático com backoff exponencial)

---

### RL-RN-005: Webhooks não existiam (polling a cada 24h)

- **Descrição:** Sincronização era feita via job batch diário às 22h, sem notificações em tempo real.
- **Localização:** `D:\IC2\ic1_legado\IControlIT\Jobs\SyncDiarioERP.vb`
- **Impacto:** Latência de até 24h para refletir mudanças entre sistemas.

**DESTINO:** SUBSTITUÍDO (webhooks em tempo real no moderno)

---

### RL-RN-006: Validação de schema XML era inexistente

- **Descrição:** XML de nota fiscal recebido do SAP não era validado contra XSD, causando erros silenciosos em campos malformados.
- **Localização:** `D:\IC2\ic1_legado\IControlIT\WebService\WSIntegracaoERP.asmx.vb` - Linha 50
- **Impacto:** Notas fiscais com dados incorretos eram importadas, descobertas apenas em auditoria.

**DESTINO:** ASSUMIDO (validação obrigatória de schema no moderno)

---

## 6. GAP ANALYSIS (LEGADO x RF MODERNO)

| Item | Legado | RF Moderno | Observação |
|-----|--------|------------|------------|
| **Sincronização** | Batch diário (polling) | Webhooks em tempo real | Reduz latência de 24h para < 5 min |
| **Retry de Falhas** | Manual | Automático com backoff exponencial | Elimina intervenção manual |
| **Credenciais** | Hardcoded em web.config | Azure Key Vault com rotação automática | Conformidade SOX/LGPD |
| **Deduplicação** | Não existia | UUID (MessageId) obrigatório | Previne processamento duplicado |
| **Validação de Schema** | Não existia | JSON Schema v7 / XSD obrigatório | Garante qualidade dos dados |
| **Dashboard** | Manual via SQL | Real-time com Angular | Visibilidade operacional |
| **Auditoria** | Logs em arquivo de texto | Tabela estruturada com retenção 7 anos | Conformidade LGPD |
| **Reconciliação** | 100% manual | 95% automática (tolerância 0,5%) | Reduz trabalho financeiro |
| **Isolamento Multi-Tenant** | Bancos separados por cliente | Row-Level Security + EmpresaId | Reduz custo de infraestrutura |
| **Validação de Período** | Não existia | Validação obrigatória antes de exportar | Evita erros contábeis |

---

## 7. DECISÕES DE MODERNIZAÇÃO

### Decisão 1: Migrar credenciais para Azure Key Vault

- **Decisão:** Todas as credenciais de ERP (senhas, tokens, certificados RFC) devem ser migradas para Azure Key Vault.
- **Motivo:** Conformidade com SOX, LGPD e boas práticas de segurança. Tabela `tbCredencialERP` será descartada completamente.
- **Impacto:** ALTO - Requer configuração de infraestrutura Azure, mas elimina vulnerabilidade crítica.
- **Data:** 2025-12-30

---

### Decisão 2: Substituir batch diário por webhooks em tempo real

- **Decisão:** Eliminar job `SyncDiarioERP.vb` e implementar webhooks com assinatura HMAC-SHA256.
- **Motivo:** Reduzir latência de 24h para < 5 min, melhorar experiência do usuário.
- **Impacto:** ALTO - Requer configuração de webhooks nos ERPs (SAP, TOTVS), mas melhora drasticamente performance.
- **Data:** 2025-12-30

---

### Decisão 3: Implementar Dead Letter Queue para mensagens com falha

- **Decisão:** Mensagens que falharem após 5 tentativas de retry serão movidas para DLQ (Azure Service Bus).
- **Motivo:** Garantir que nenhuma integração seja perdida silenciosamente, permitindo investigação posterior.
- **Impacto:** MÉDIO - Requer configuração de Azure Service Bus, mas elimina perda de dados.
- **Data:** 2025-12-30

---

### Decisão 4: Unificar bancos de dados multi-cliente em banco único com Row-Level Security

- **Decisão:** Consolidar múltiplos bancos `IControlIT_Cliente01`, `IControlIT_Cliente02` em banco único com campo `EmpresaId`.
- **Motivo:** Reduzir custo de infraestrutura, simplificar backups, melhorar escalabilidade.
- **Impacto:** ALTO - Requer migração de dados, mas reduz custo operacional significativamente.
- **Data:** 2025-12-30 (em paralelo com outros RFs)

---

## 8. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Probabilidade | Mitigação |
|------|---------|---------------|-----------|
| **Perda de mensagens durante cutover** | ALTO | MÉDIA | Manter legado em paralelo por 30 dias, sincronizar DLQ com tabela legado |
| **ERPs não suportam webhooks** | ALTO | BAIXA | Manter polling como fallback para ERPs sem webhook |
| **Rotação de credencial quebra integração** | ALTO | BAIXA | Testar rotação em ambiente HOM, manter credencial antiga por 7 dias |
| **Tolerância de reconciliação muito restritiva** | MÉDIO | MÉDIA | Tornar tolerância configurável (0,5% padrão, ajustável por cliente) |
| **Latência de Key Vault causa timeout** | MÉDIO | BAIXA | Cache local de credenciais com TTL de 1h, refresh assíncrono |
| **Volume de mensagens sobrecarrega DLQ** | BAIXO | BAIXA | Alertar quando DLQ > 50 mensagens, escalar automaticamente Service Bus |

---

## 9. RASTREABILIDADE (LEGADO → MODERNO)

| Elemento Legado | Referência RF | Referência UC | Status |
|----------------|---------------|--------------|--------|
| `frmIntegracaoERP.aspx` | RN-RF078-007 | UC00-listar-integracoes | SUBSTITUÍDO |
| `frmConfiguracaoERP.aspx` | RN-RF078-002 | UC01-configurar-credenciais | SUBSTITUÍDO |
| `WSIntegracaoERP.asmx` | RN-RF078-001 a RN-RF078-010 | UC01 a UC04 | SUBSTITUÍDO |
| `tbIntegracaoERP` | RN-RF078-007 | IntegrationAudit (MD-RF078) | SUBSTITUÍDO |
| `tbCredencialERP` | RN-RF078-002 | Azure Key Vault | DESCARTADO |
| `tbCentroCusto` | RN-RF078-001 | CentroCusto (RF021) | SUBSTITUÍDO |
| `SyncDiarioERP.vb` (job batch) | RN-RF078-001 | UC04-processar-webhook | SUBSTITUÍDO |
| `ReconciliacaoService.vb` | RN-RF078-010 | UC03-reconciliar-faturas | ASSUMIDO |

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|------|------|----------|------|
| 1.0 | 2025-12-30 | Documentação completa do sistema legado de integrações com ERPs | Agência ALC - alc.dev.br |

---

**Última Atualização**: 2025-12-30
**Versão Governança**: 2.0
**Autor**: Agência ALC - alc.dev.br
**Status**: Completo
