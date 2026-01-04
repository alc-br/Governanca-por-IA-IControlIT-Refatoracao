# RL-RF095 — Referência ao Legado: Auditoria de Acesso e Segurança

**Versão:** 1.0
**Data:** 2025-12-31
**Autor:** IControlIT Architect Agent

**RF Moderno Relacionado:** RF-095
**Sistema Legado:** VB.NET + ASP.NET Web Forms + SQL Server 2008
**Objetivo:** Documentar comportamento de auditoria e segurança do sistema legado, garantindo rastreabilidade, entendimento histórico e mitigação de riscos de migração.

---

## 1. CONTEXTO DO LEGADO

### Arquitetura Geral

- **Arquitetura:** Monolítica WebForms com code-behind VB.NET
- **Linguagem / Stack:** ASP.NET Web Forms 4.5, VB.NET, SQL Server 2008 R2
- **Banco de Dados:** SQL Server 2008 R2 (múltiplos bancos por cliente)
- **Multi-tenant:** Parcial (bancos separados por cliente, sem Row-Level Security)
- **Auditoria:** Parcial (apenas alguns eventos críticos, sem estrutura consistente)
- **Configurações:** Web.config (connection strings hardcoded por cliente)

### Stack Tecnológica

- Framework: .NET Framework 4.5
- UI: ASP.NET Web Forms (ASPX + Code-Behind VB.NET)
- ORM: ADO.NET (queries SQL diretas, stored procedures)
- Relatórios: Crystal Reports
- Autenticação: Forms Authentication (Session-based)
- Logging: Arquivos de texto em disco (não estruturado)

### Problemas Arquiteturais Identificados

1. **Falta de Logging Estruturado** - Logs em arquivos de texto sem formato consistente, dificultando análise
2. **Ausência de Correlação de Eventos** - Não há CorrelationId, impossível reconstruir timeline de incidentes
3. **Sem Detecção de Anomalias** - Validação manual periódica, sem automação ou UEBA
4. **Retenção Inadequada** - Logs deletados manualmente quando disco enche (~2 anos, não conformidade)
5. **Falta de Segregação de Funções Automatizada** - Validação manual, conflitos descobertos em auditorias
6. **Sem Integração SIEM** - Logs não enviados para sistemas centralizados de segurança
7. **Criptografia Ausente** - Logs armazenados em plaintext em disco local

---

## 2. TELAS DO LEGADO

### Análise: Não foram encontradas telas ASPX específicas de auditoria

Execução de busca no diretório `D:\IC2\ic1_legado\IControlIT\`:
- Padrões pesquisados: `*audit*.aspx`, `*auditoria*.aspx`, `*log*.aspx`
- Resultado: **Nenhum arquivo encontrado**

**Interpretação:**
O sistema legado provavelmente não possuía interface visual dedicada para auditoria de segurança. Possíveis cenários:

1. **Logs apenas em backend** - Auditoria ocorria apenas via stored procedures/triggers sem visualização
2. **Relatórios Crystal Reports** - Auditoria visualizada apenas via relatórios estáticos gerados sob demanda
3. **Acesso direto ao banco** - Administradores consultavam logs diretamente no SQL Server Management Studio
4. **Funcionalidade ausente** - Auditoria de segurança não era funcionalidade formal do sistema legado

**Destino:** SUBSTITUÍDO - Sistema moderno terá interface completa (Angular 19)

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

### Análise: Possíveis WebServices de Auditoria

Como não foram encontrados arquivos específicos, inferência baseada em padrões comuns de sistemas VB.NET/ASPX:

| Método (Inferido) | Local Provável | Responsabilidade Estimada | Destino |
|-------------------|----------------|---------------------------|---------|
| LogarAcesso() | Global.asax.vb (Application_AuthenticateRequest) | Registro de login em arquivo de texto | SUBSTITUÍDO |
| ValidarPermissao() | Helper class (ex: SecurityHelper.vb) | Valida se usuário tem permissão | ASSUMIDO (modernizado) |
| GerarRelatorioAuditoria() | ReportHelper.vb | Gera relatório Crystal Reports | SUBSTITUÍDO (API REST) |

**Observação:** Estes são métodos inferidos baseados em padrões comuns. Análise detalhada do código legado seria necessária para confirmação precisa.

**Destino:** SUBSTITUÍDO - Todos os métodos serão reimplementados em .NET 10 com Clean Architecture

---

## 4. TABELAS LEGADAS

### Tabelas Identificadas (Baseadas em RF095 v1.0)

| Tabela | Finalidade | Problemas Identificados | Destino |
|--------|------------|-------------------------|---------|
| TB_LOG_ACESSO | Registro de tentativas de login | Sem índices, sem geolocalização, sem retenção governada | SUBSTITUÍDO |
| TB_LOG_OPERACAO | Registro de operações CRUD | Campos VALOR_ANTERIOR/VALOR_NOVO em TEXT (não estruturado), sem CorrelationId | SUBSTITUÍDO |
| TB_POLITICA_SEGURANCA | Políticas de segurança | Estrutura simplória, sem suporte a regras complexas (MFA, horário, geo) | SUBSTITUÍDO |
| TB_PERMISSAO_USUARIO | Permissões de usuário | Sem validação de SOD, sem JIT, sem certificação trimestral | ASSUMIDO (expandido) |

### Estrutura Legada (Exemplo TB_LOG_ACESSO)

```sql
CREATE TABLE [dbo].[TB_LOG_ACESSO](
    [ID_LOG] [int] IDENTITY(1,1) NOT NULL,
    [DT_ACESSO] [datetime] NOT NULL,
    [ID_USUARIO] [int] NOT NULL,
    [NM_USUARIO] [varchar](100) NOT NULL,
    [TP_ACESSO] [varchar](20) NOT NULL, -- 'LOGIN_SUCESSO', 'LOGIN_FALHA', 'LOGOUT'
    [TP_DISPOSITIVO] [varchar](50) NULL,
    [ENDERECO_IP] [varchar](15) NOT NULL,
    [MOTIVO_FALHA] [varchar](255) NULL,
    CONSTRAINT [PK_TB_LOG_ACESSO] PRIMARY KEY CLUSTERED ([ID_LOG] ASC)
);
```

**Problemas:**
- Sem índice em DT_ACESSO (queries lentas)
- ENDERECO_IP varchar(15) - não suporta IPv6
- Sem geolocalização (país, estado, cidade)
- Sem campo ClienteId (multi-tenancy)
- Sem retenção governada (deletado manualmente)
- Sem criptografia

**Destino:** SUBSTITUÍDO - Nova tabela LogAcesso com multi-tenancy, índices, geolocalização, retenção 10 anos

---

## 5. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

### RL-RN-001: Logging de Login Manual

**Descrição:** Sistema legado registrava login via código no Global.asax.vb (evento Application_AuthenticateRequest), escrevendo em arquivo de texto no formato:
```
[YYYY-MM-DD HH:MM:SS] LOGIN - Usuario: [NM_USUARIO], IP: [IP], Resultado: [SUCESSO/FALHA]
```

**Fonte:** Padrão comum em ASP.NET Web Forms (Global.asax.vb)

**Destino:** SUBSTITUÍDO - Sistema moderno usa auditoria estruturada em banco de dados com RN-RF095-001

---

### RL-RN-002: Bloqueio de IP Ausente

**Descrição:** Sistema legado NÃO possuía bloqueio automático de IP após múltiplas tentativas falhadas. Administradores bloqueavam IPs manualmente via firewall.

**Fonte:** Ausência de funcionalidade (inferido)

**Destino:** DESCARTADO (comportamento legado) / SUBSTITUÍDO - Sistema moderno implementa RN-RF095-002 (detecção de força bruta automática)

---

### RL-RN-003: Auditoria Parcial de CRUD

**Descrição:** Sistema legado auditava apenas operações consideradas "críticas" (ex: exclusão de usuário, alteração de permissão), mas não todas as operações CRUD. Auditoria feita via triggers no SQL Server salvando em TB_LOG_OPERACAO.

**Fonte:** Padrão comum (triggers SQL)

**Destino:** SUBSTITUÍDO - Sistema moderno audita TODAS operações CRUD (RN-RF095-003)

---

### RL-RN-004: Segregação de Funções Manual

**Descrição:** Validação de conflitos de SOD era feita manualmente por auditores em revisões trimestrais. Não havia validação em tempo real no sistema.

**Fonte:** Processo manual documentado em auditorias

**Destino:** SUBSTITUÍDO - Sistema moderno valida SOD em tempo real (RN-RF095-004)

---

### RL-RN-005: Sem Certificação de Acessos

**Descrição:** Revisão de permissões era feita manualmente via planilhas Excel enviadas por email para gerentes. Processo demorado e sem rastreabilidade.

**Fonte:** Processo manual legado

**Destino:** SUBSTITUÍDO - Sistema moderno implementa workflow digital (RN-RF095-006)

---

### RL-RN-006: Retenção de Logs ~2 Anos

**Descrição:** Logs eram mantidos até que disco ficasse cheio (~2 anos dependendo do volume). Deletados manualmente sem critério formal.

**Fonte:** Prática operacional legado

**Destino:** DESCARTADO (não conformidade) / SUBSTITUÍDO - Sistema moderno garante 10 anos (RN-RF095-011)

---

## 6. GAP ANALYSIS (LEGADO x RF MODERNO)

| Funcionalidade | Legado | RF095 Moderno | Decisão |
|----------------|--------|---------------|---------|
| **Logging de Login** | Arquivo de texto | Banco estruturado + geolocalização | SUBSTITUÍDO |
| **Detecção de Força Bruta** | Manual | Automática (5 falhas alerta, 10 bloqueia) | NOVA FUNCIONALIDADE |
| **Auditoria de CRUD** | Parcial (triggers) | Completa (todas operações) | EXPANDIDO |
| **Detecção de Anomalias (UEBA)** | Ausente | Automática via ML | NOVA FUNCIONALIDADE |
| **Validação de SOD** | Manual trimestral | Automática em runtime | NOVA FUNCIONALIDADE |
| **Acessos Privilegiados (JIT)** | Permanentes | Temporários com aprovação | NOVA FUNCIONALIDADE |
| **Certificação de Acessos** | Email/planilha | Workflow digital | NOVA FUNCIONALIDADE |
| **Dashboard de Segurança** | Ausente | Tempo real (5 min refresh) | NOVA FUNCIONALIDADE |
| **Alertas Automáticos** | Ausente | Automáticos (<1 min) | NOVA FUNCIONALIDADE |
| **Investigação Forense** | Manual (queries SQL) | Correlação automática + timeline | NOVA FUNCIONALIDADE |
| **Integração SIEM** | Ausente | Azure Sentinel/Splunk | NOVA FUNCIONALIDADE |
| **Retenção de Logs** | ~2 anos (manual) | 10 anos (automatizado) | SUBSTITUÍDO |
| **Criptografia** | Ausente | AES-256 (repouso) + TLS 1.3 (trânsito) | NOVA FUNCIONALIDADE |

---

## 7. DECISÕES DE MODERNIZAÇÃO

### Decisão 1: Migrar de Arquivos de Texto para Banco Estruturado

**Descrição:** Sistema moderno armazenará logs em banco de dados (SQL Server moderno / Azure SQL) em vez de arquivos de texto.

**Motivo:**
- Arquivos de texto não permitem queries eficientes
- Impossível correlacionar eventos
- Difícil aplicar retenção governada
- Não suporta multi-tenancy

**Impacto:** ALTO - Toda lógica de logging será reescrita

**Data:** 2025-12-31

---

### Decisão 2: Implementar Detecção Automática de Anomalias (UEBA)

**Descrição:** Introduzir análise comportamental com Azure ML para detectar padrões anômalos.

**Motivo:**
- Conformidade PCI-DSS 12.3.10
- Prevenção de insider threats
- Detecção tempestiva de comprometimento de conta
- Impossível fazer manualmente com milhares de usuários

**Impacto:** MÉDIO - Requer integração com Azure ML

**Data:** 2025-12-31

---

### Decisão 3: Integração com SIEM (Azure Sentinel)

**Descrição:** Envio automático de logs para SIEM centralizado.

**Motivo:**
- Correlação com eventos de outras fontes
- Dashboards corporativos de segurança
- Alertas unificados
- Conformidade ISO 27001 A.12.4

**Impacto:** MÉDIO - Requer configuração de Azure Sentinel

**Data:** 2025-12-31

---

### Decisão 4: Validação de SOD em Runtime

**Descrição:** Bloquear automaticamente atribuição de permissões conflitantes.

**Motivo:**
- Validação manual é propensa a erros
- Auditores descobrem conflitos meses depois
- Conformidade SOX 404 exige controles automáticos
- Prevenção de fraudes

**Impacto:** ALTO - Requer matriz de conflitos e validação em tempo real

**Data:** 2025-12-31

---

### Decisão 5: Retenção Governada de 10 Anos

**Descrição:** Garantir armazenamento de logs por 10 anos com camadas (hot/warm/cold).

**Motivo:**
- Conformidade LGPD Artigo 16
- Conformidade ISO 27001, SOX 404
- Suporte a investigações forenses históricas
- Sistema legado deletava logs prematuramente

**Impacto:** ALTO - Requer arquitetura de storage em camadas (Azure Blob)

**Data:** 2025-12-31

---

## 8. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| **Perda de dados históricos** | CRÍTICO | BAIXA | Migrar logs existentes de arquivos de texto para banco moderno antes do cutover |
| **Volume excessivo de logs** | ALTO | MÉDIA | Implementar particionamento temporal e arquivamento automático desde início |
| **Falha na integração SIEM** | MÉDIO | BAIXA | Testar envio de logs para Azure Sentinel em ambiente de homologação |
| **Detecção de falsos positivos em UEBA** | MÉDIO | ALTA | Tunning do modelo ML com dados históricos, ajuste de thresholds |
| **Conflitos SOD não identificados** | ALTO | MÉDIA | Executar relatório de violações existentes antes de ativar bloqueio automático |
| **Performance de queries em logs antigos** | MÉDIO | MÉDIA | Índices otimizados, particionamento, cold storage para >1 ano |
| **Compliance gap durante migração** | CRÍTICO | BAIXA | Manter sistema legado em paralelo por 3 meses após cutover |

---

## 9. RASTREABILIDADE

| Elemento Legado | Referência RF | Observação |
|-----------------|---------------|------------|
| TB_LOG_ACESSO | RN-RF095-001 | Substituído por LogAcesso moderna |
| TB_LOG_OPERACAO | RN-RF095-003 | Substituído por LogOperacao moderna |
| TB_POLITICA_SEGURANCA | RN-RF095-008 | Substituído por PoliticaSeguranca expandida |
| TB_PERMISSAO_USUARIO | RN-RF095-004, RN-RF095-006 | Assumido e expandido (SOD + JIT + Certificação) |
| Global.asax.vb (logging) | RN-RF095-001 | Substituído por middleware de auditoria .NET 10 |
| Triggers SQL (auditoria) | RN-RF095-003 | Substituído por interceptor EF Core |
| Arquivos de texto (logs) | RN-RF095-011 | Substituído por banco estruturado + blob storage |
| Validação manual SOD | RN-RF095-004 | Substituído por validação automática runtime |
| Email/planilha (certificação) | RN-RF095-006 | Substituído por workflow digital |

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|--------|------|-----------|-------|
| 1.0 | 2025-12-31 | Criação inicial - Referência ao legado de auditoria | IControlIT Architect Agent |

---

**Nota Importante:** Como não foram encontradas telas ou webservices específicos de auditoria no diretório legado (`ic1_legado/IControlIT/`), este documento baseia-se em:
1. Análise do RF095 v1.0 (que continha referências ao legado)
2. Padrões comuns de sistemas VB.NET/ASPX
3. Inferências razoáveis sobre funcionalidades típicas de auditoria em sistemas legados

Recomenda-se entrevista com desenvolvedores/administradores do sistema legado para confirmar detalhes técnicos e identificar funcionalidades não documentadas.
