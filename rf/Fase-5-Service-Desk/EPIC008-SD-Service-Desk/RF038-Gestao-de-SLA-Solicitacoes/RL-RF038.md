# RL-RF038 — Referência ao Legado (Gestão de SLA Solicitações)

**Versão:** 1.0
**Data:** 2025-12-30
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF038 - Gestão de SLA Solicitações
**Sistema Legado:** IControlIT v1.0 (VB.NET + ASP.NET Web Forms + SQL Server)
**Objetivo:** Documentar o comportamento do legado que serve de base para a refatoração, garantindo rastreabilidade, entendimento histórico e mitigação de riscos.

---

## 1. CONTEXTO DO LEGADO

### Arquitetura Geral

- **Arquitetura:** Monolítica WebForms com lógica de negócio distribuída entre ASPX.VB, WebServices ASMX e Stored Procedures SQL
- **Linguagem / Stack:** VB.NET Framework 4.7, ASP.NET Web Forms, IIS 8.5
- **Banco de Dados:** SQL Server 2014, múltiplos databases isolados por cliente (multi-database, NÃO multi-tenant)
- **Multi-tenant:** NÃO (cada cliente tem database separado: K2A, Vale, Prudential, Odontoprev, etc.)
- **Auditoria:** Parcial (apenas tabelas de log específicas, sem padronização)
- **Configurações:** Web.config + registros em tabela `Configuracao_Sistema`

### Problemas Arquiteturais Identificados

1. **Ausência de Multi-Tenancy Real**: Cada cliente requer database separado, impossibilitando escalabilidade horizontal
2. **Lógica de Negócio em Stored Procedures**: Regras de cálculo de SLA estão em SQL, dificultando manutenção e testes unitários
3. **Alertas Manuais**: Não há job automático para envio de alertas, dependendo de execução manual via interface
4. **Falta de Rastreabilidade**: Pausas e extensões de SLA sem histórico estruturado
5. **Cálculo de Prazo Limitado**: Não considera horário de atendimento customizado nem feriados regionais (apenas feriados nacionais fixos)
6. **Escalação Manual**: Supervisores devem reassignar solicitações manualmente ao detectar breach

---

## 2. TELAS DO LEGADO

### Tela: Configuracao_SLA.aspx

- **Caminho:** `ic1_legado/IControlIT/ServiceDesk/Configuracao_SLA.aspx`
- **Responsabilidade:** Configurar SLA por tipo de solicitação

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| `ddlTipoSolicitacao` | DropDownList | Sim | Tipos cadastrados em `Solicitacao_Tipo` |
| `txtHoras` | TextBox (int) | Sim | Prazo em horas (sem distinção dias úteis) |
| `txtEmail2Nivel` | TextBox (email) | Sim | Email de supervisor para alertas |
| `chkDesativado` | CheckBox | Não | Fl_Desativado = 0 (ativo) ou 1 (desativado) |

#### Comportamentos Implícitos

- Validação de email apenas no formato (`@` presente), sem validação SMTP
- NÃO há campo de prioridade: SLA é fixo por tipo de solicitação (não considera alta/média/baixa)
- NÃO há configuração de percentuais de alerta (fixo em código VB: 50%, 80%, 100%)
- Prazo em **horas corridas** (não considera apenas horário comercial)
- NÃO permite configurar múltiplos níveis de escalação

**Destino:** SUBSTITUÍDO

**Justificativa:** Modelo simplificado demais. Sistema moderno permite SLA por **tipo + prioridade**, cálculo em **horas úteis**, múltiplos níveis de escalação, e horário de atendimento customizado.

**Rastreabilidade:**
- RF Moderno: RF038 - Seção 2 (Funcionalidades) → "Configuração de SLA por tipo de solicitação e prioridade"
- UC Relacionado: UC01-criar-sla (com campos expandidos: tipo, prioridade, prazo_horas, prazo_dias, horario_atendimento)

---

### Tela: Dashboard_SLA.aspx

- **Caminho:** `ic1_legado/IControlIT/ServiceDesk/Dashboard_SLA.aspx`
- **Responsabilidade:** Exibir solicitações em andamento com status de SLA

#### Campos (GridView)

| Campo | Fonte | Observações |
|-------|-------|-------------|
| `Nr_Solicitacao` | Tabela `Solicitacao` | Número da solicitação |
| `Tipo` | Join com `Solicitacao_Tipo` | Tipo da solicitação |
| `Data_Abertura` | `Dt_Abertura` | Data de criação |
| `Prazo_Limite` | Calculado (Data_Abertura + Horas) | Sem considerar feriados |
| `Tempo_Restante` | Diferença (NOW - Prazo_Limite) | Em horas |
| `Percentual` | (Tempo_Decorrido / Prazo_Total) * 100 | Cálculo via SQL |
| `Status_Visual` | Barra de progresso (verde/amarelo/vermelho) | Renderizada via JavaScript |

#### Comportamentos Implícitos

- Grid atualiza APENAS ao recarregar página (não há SignalR ou polling)
- Cores fixas: verde (0-50%), amarelo (50-80%), vermelho (80-100%), sem indicação visual de breach (>100%)
- NÃO há filtro por prioridade, tipo ou atendente
- NÃO há ordenação automática (prazo mais próximo primeiro)
- Solicitações finalizadas NÃO são removidas automaticamente do grid
- NÃO há busca por número de solicitação

**Destino:** SUBSTITUÍDO

**Justificativa:** Dashboard estático sem atualização em tempo real. Sistema moderno usa SignalR para push automático, filtros avançados, ordenação inteligente e indicador de breach (preto).

**Rastreabilidade:**
- RF Moderno: RN-RF038-008 (Dashboard em tempo real com cores)
- UC Relacionado: UC07-monitorar-dashboard

---

### Tela: Pausa_SLA.aspx

- **Caminho:** `ic1_legado/IControlIT/ServiceDesk/Pausa_SLA.aspx`
- **Responsabilidade:** Pausar e retomar SLA de solicitação

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| `txtNrSolicitacao` | TextBox (int) | Sim | Número da solicitação |
| `txtMotivo` | TextArea | Sim | Motivo da pausa (mínimo 10 caracteres no code-behind) |
| `btnPausar` | Button | - | Ação de pausa |
| `btnRetomar` | Button | - | Ação de retomada |

#### Comportamentos Implícitos

- Pausa NÃO registra timestamp exato no banco (apenas flag `Fl_SLA_Pausado = 1`)
- Ao retomar, NÃO recalcula prazo corretamente (não subtrai tempo pausado)
- NÃO há histórico de pausas/retomadas (apenas último estado)
- Permitia múltiplas pausas simultâneas (bug de concorrência)
- NÃO valida se usuário tem permissão de pausar (apenas verifica login)

**Destino:** SUBSTITUÍDO

**Justificativa:** Lógica de pausa/retomada com bugs graves (não recalcula prazo). Sistema moderno registra histórico completo com timestamps, recalcula prazo automaticamente e valida permissões RBAC.

**Rastreabilidade:**
- RF Moderno: RN-RF038-004 (Pausa e retomada com recálculo)
- UC Relacionado: UC08-pausar-retomar-sla

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

### WebService: SlaService.asmx

- **Caminho:** `ic1_legado/IControlIT/WebServices/SlaService.asmx`
- **Responsabilidade:** Cálculo de prazo de SLA e envio de alertas

#### Métodos

| Método | Parâmetros | Retorno | Observações |
|--------|------------|---------|-------------|
| `CalcularPrazoSLA(idSolicitacao)` | `int` | `DateTime` | Calcula prazo limite (Data_Abertura + Horas) |
| `EnviarAlerta50Porcento()` | - | `bool` | Envia emails para solicitações em 50% do prazo |
| `EnviarAlerta80Porcento()` | - | `bool` | Envia emails para solicitações em 80% do prazo |
| `EnviarAlerta100Porcento()` | - | `bool` | Envia emails para solicitações em 100% (breach) |

#### Comportamentos Implícitos

- `CalcularPrazoSLA`: soma horas direto (não considera fins de semana ou feriados)
- Alertas NÃO são enviados automaticamente (requer chamada manual via task agendada no Windows Server)
- Alertas duplicados NÃO são prevenidos (pode enviar mesmo alerta múltiplas vezes)
- NÃO usa templates de email (mensagens hard-coded no código VB)
- NÃO registra envio de alerta no banco (impossível auditar)

**Destino:** SUBSTITUÍDO

**Justificativa:** Cálculo de prazo simplificado demais (não considera calendário comercial). Sistema moderno usa Hangfire para jobs recorrentes, templates de email via RF064, e registra todos os alertas no banco.

**Rastreabilidade:**
- RF Moderno: RN-RF038-001 (Cálculo automático de prazo), RN-RF038-002 (Alertas escalonados)
- UC Relacionado: UC01-criar-sla (cálculo automático), Alertas via Hangfire Job

---

## 4. STORED PROCEDURES

### Procedure: sp_Solicitacao_SLA_Calcula_Prazo

- **Caminho:** `ic1_legado/Database/Procedures/sp_Solicitacao_SLA_Calcula_Prazo.sql`
- **Parâmetros de Entrada:**
  - `@Id_Solicitacao INT`
  - `@Id_Tipo_Solicitacao INT`
- **Parâmetros de Saída:**
  - `@Data_Limite DATETIME OUTPUT`

#### Lógica

Busca prazo em horas da tabela `Solicitacao_SLA` com base em `Id_Tipo_Solicitacao`, soma diretamente à data de abertura da solicitação, sem considerar horário comercial ou feriados. Retorna `Data_Abertura + Horas`.

**Destino:** SUBSTITUÍDO

**Justificativa:** Lógica movida para Application Layer (CQRS Handler `CreateSolicitacaoCommandHandler`). Cálculo moderno considera calendário corporativo, feriados e horário de atendimento configurável.

**Rastreabilidade:**
- RF Moderno: RN-RF038-001 (Cálculo automático de prazo)
- Implementação Moderna: `CreateSolicitacaoCommandHandler.cs` + `SlaCalculationService.cs`

---

### Procedure: sp_Solicitacao_SLA_Lista_Alertas

- **Caminho:** `ic1_legado/Database/Procedures/sp_Solicitacao_SLA_Lista_Alertas.sql`
- **Parâmetros de Entrada:**
  - `@Percentual INT` (50, 80 ou 100)
- **Parâmetros de Saída:**
  - ResultSet: Lista de solicitações que atingiram o percentual

#### Lógica

Calcula percentual decorrido como `(DATEDIFF(HOUR, Data_Abertura, GETDATE()) * 100.0) / Horas_SLA`. Retorna solicitações onde percentual >= @Percentual AND percentual < (@Percentual + 10).

**Problemas:**
- NÃO marca alertas enviados (pode retornar mesma solicitação múltiplas vezes)
- NÃO considera pausas de SLA no cálculo
- Cálculo em HOURS direto (não considera apenas horário comercial)

**Destino:** SUBSTITUÍDO

**Justificativa:** Lógica movida para Hangfire Job `SlaMonitoringJob.cs` que executa a cada 15 minutos. Alertas são registrados na tabela `SlaAlert` evitando duplicação e considerando pausas.

**Rastreabilidade:**
- RF Moderno: RN-RF038-002 (Alertas escalonados)
- Implementação Moderna: `SlaMonitoringJob.cs` + `SlaAlertService.cs`

---

## 5. TABELAS LEGADAS

### Tabela: Solicitacao_SLA

- **Schema:** `[dbo].[Solicitacao_SLA]`
- **Finalidade:** Armazenar configurações de SLA por tipo de solicitação

#### Estrutura

```sql
CREATE TABLE [dbo].[Solicitacao_SLA](
    [Id_Solicitacao_SLA] [int] IDENTITY(1,1) NOT NULL,
    [Nm_Solicitacao_SLA] [varchar](50) NOT NULL,
    [Horas] [int] NOT NULL,
    [Email_2_Nivel] [varchar](50) NOT NULL,
    [Fl_Desativado] [int] NOT NULL,
    CONSTRAINT [PK_Solicitacao_SLA] PRIMARY KEY CLUSTERED ([Id_Solicitacao_SLA] ASC)
)
```

#### Problemas Identificados

- **Falta de chave estrangeira** para validar `Id_Tipo_Solicitacao` (referência implícita sem FK)
- **Falta de campo de prioridade**: SLA é único por tipo, não distingue alta/média/baixa prioridade
- **Sem auditoria**: não registra quem criou, quando criou, quem modificou
- **Sem multi-tenancy**: não tem `Id_Conglomerado` ou `Id_Fornecedor` (cada cliente tem database separado)
- **Prazo apenas em horas**: não permite configurar prazo misto (ex: 2 dias + 4 horas)
- **Email hard-coded**: apenas 1 email de supervisor, não suporta múltiplos destinatários ou níveis de escalação

**Destino:** SUBSTITUÍDO

**Justificativa:** Tabela redesenhada com multi-tenancy, auditoria completa, campo de prioridade, horário de atendimento configurável, e suporte a múltiplos níveis de escalação.

**Rastreabilidade:**
- RF Moderno: RF038 - Seção 7 (Modelo de Dados)
- MD Moderno: `MD-RF038.md` - Tabela `SlaConfiguration`
- Migration EF Core: `20251230_CreateSlaConfigurationTable.cs`

**Mapeamento:**

| Legado | Moderno |
|--------|---------|
| `Nm_Solicitacao_SLA` | `Name` (varchar(100)) |
| `Horas` | `DeadlineHours` (int) + `DeadlineDays` (int, novo) |
| `Email_2_Nivel` | **REMOVIDO** (alertas via tabela `SlaAlert` + notificações SignalR) |
| `Fl_Desativado` | `IsActive` (bool) + `DeletedAt` (DateTime?, soft delete) |
| - | `TenantId` (Guid, novo - multi-tenancy) |
| - | `PriorityId` (int, novo - alta/média/baixa) |
| - | `WorkingHoursType` (enum, novo - 8x5, 12x5, 24x7, custom) |
| - | `CreatedAt`, `CreatedBy`, `ModifiedAt`, `ModifiedBy` (auditoria) |

---

### Tabela: Solicitacao (relação com SLA)

- **Schema:** `[dbo].[Solicitacao]`
- **Finalidade:** Armazena solicitações de TI

#### Campos Relacionados a SLA

| Campo | Tipo | Observações |
|-------|------|-------------|
| `Id_Solicitacao_SLA` | `int` | FK para `Solicitacao_SLA` |
| `Dt_Abertura` | `datetime` | Data de criação da solicitação |
| `Fl_SLA_Pausado` | `bit` | Flag de pausa (sem timestamp) |
| `Dt_Encerramento` | `datetime` | Data de finalização |

#### Problemas

- **Falta de campo `Data_Limite_SLA`**: prazo é calculado on-the-fly (performance ruim)
- **Falta de campo `Percentual_Decorrido`**: recalcula em toda consulta
- **Flag de pausa sem histórico**: não registra quando foi pausado nem quando foi retomado
- **Sem rastreamento de alertas enviados**: não sabe se alerta de 50%, 80% ou 100% já foi enviado

**Destino:** SUBSTITUÍDO

**Justificativa:** Sistema moderno cria tabela `SlaTracking` específica para rastreamento de SLA por solicitação, com campos `DeadlineAt`, `PercentageElapsed`, `LastAlertSentAt`, e histórico de pausas em tabela separada `SlaHistory`.

**Rastreabilidade:**
- RF Moderno: RF038 - Seção 7 (Modelo de Dados)
- MD Moderno: `MD-RF038.md` - Tabelas `SlaTracking`, `SlaHistory`, `SlaAlert`

---

## 6. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

### RL-RN-001: Percentuais de Alerta Fixos

**Descrição:** Alertas são enviados em 3 níveis fixos: 50%, 80% e 100% do prazo. Não há configuração para ajustar esses percentuais.

**Fonte:** `ic1_legado/IControlIT/ServiceDesk/Dashboard_SLA.aspx.vb` - Linha 127

**Destino:** ASSUMIDO

**Justificativa:** Percentuais mantidos no sistema moderno como padrão (50%, 80%, 100%), mas adicionado nível de breach (>100%) com cor preta e escalação automática.

**Rastreabilidade:**
- RF Moderno: RN-RF038-002 (Alertas escalonados)
- Implementação Moderna: `SlaMonitoringJob.cs` (classe com constantes `ALERT_THRESHOLD_50`, `ALERT_THRESHOLD_80`, `ALERT_THRESHOLD_100`)

---

### RL-RN-002: Cálculo de Prazo em Horas Corridas

**Descrição:** Prazo de SLA é calculado somando horas diretamente à data de abertura, sem considerar apenas horário comercial ou feriados. Exemplo: solicitação criada às 16h de sexta com SLA de 8h tem prazo limite às 00h de sábado.

**Fonte:** `ic1_legado/Database/Procedures/sp_Solicitacao_SLA_Calcula_Prazo.sql` - Linha 14

**Destino:** SUBSTITUÍDO

**Justificativa:** Regra INCORRETA que causava breaches indevidos. Sistema moderno calcula prazo considerando apenas horário de atendimento (8x5, 12x5, 24x7 ou customizado) e exclui feriados.

**Rastreabilidade:**
- RF Moderno: RN-RF038-001 (Cálculo automático de prazo), RN-RF038-005 (Horário de atendimento)
- Implementação Moderna: `SlaCalculationService.cs` (método `CalculateDeadlineConsideringBusinessHours`)

---

### RL-RN-003: Envio de Email para Supervisor Fixo

**Descrição:** Alertas de SLA são enviados apenas para 1 email de supervisor configurado na tabela `Solicitacao_SLA.Email_2_Nivel`. Não há suporte a múltiplos destinatários ou níveis hierárquicos.

**Fonte:** `ic1_legado/IControlIT/WebServices/SlaService.asmx.vb` - Linha 89

**Destino:** SUBSTITUÍDO

**Justificativa:** Limitação removida. Sistema moderno usa matriz de escalação (`SlaEscalation`) que define múltiplos níveis hierárquicos e envia notificações via SignalR push + email (template RF064).

**Rastreabilidade:**
- RF Moderno: RN-RF038-003 (Escalação automática), RN-RF038-010 (Notificações push)
- Implementação Moderna: `SlaEscalationService.cs` + `NotificationService.cs` (SignalR)

---

### RL-RN-004: Pausa de SLA Sem Recálculo de Prazo

**Descrição:** Ao pausar SLA, sistema apenas seta flag `Fl_SLA_Pausado = 1`. Ao retomar, NÃO recalcula prazo estendendo pelo tempo pausado. Resultado: solicitações pausadas sempre entravam em breach indevidamente.

**Fonte:** `ic1_legado/IControlIT/ServiceDesk/Pausa_SLA.aspx.vb` - Linha 63

**Destino:** SUBSTITUÍDO (BUG CRÍTICO CORRIGIDO)

**Justificativa:** Bug grave corrigido no sistema moderno. Ao retomar SLA, sistema calcula tempo pausado (`PausedAt - ResumedAt`) e estende prazo automaticamente.

**Rastreabilidade:**
- RF Moderno: RN-RF038-004 (Pausa e retomada com recálculo)
- Implementação Moderna: `ResumeSlaCommandHandler.cs` (recalcula `DeadlineAt += TimeSpan pausado`)

---

### RL-RN-005: Feriados Nacionais Hard-Coded

**Descrição:** Sistema considera apenas 12 feriados nacionais fixos (Ano Novo, Carnaval, Sexta-feira Santa, Tiradentes, Dia do Trabalho, Corpus Christi, Independência, Nossa Senhora Aparecida, Finados, Proclamação da República, Consciência Negra, Natal) diretamente no código VB.NET. Não permite cadastrar feriados estaduais, municipais ou corporativos.

**Fonte:** `ic1_legado/IControlIT/Helpers/FeriadosHelper.vb` - Linha 8-32

**Destino:** SUBSTITUÍDO

**Justificativa:** Hard-coding removido. Sistema moderno permite cadastrar feriados de 4 tipos (Nacional, Estadual, Municipal, Corporativo) via tabela `SlaHoliday` e importação de calendários externos (Google Calendar, Outlook).

**Rastreabilidade:**
- RF Moderno: RN-RF038-006 (Calendário de feriados)
- Implementação Moderna: Tabela `SlaHoliday` + `HolidayService.cs` (importação de iCal)

---

### RL-RN-006: Extensão de Prazo Sem Aprovação

**Descrição:** Supervisor pode estender prazo de SLA sem aprovação de gerente ou diretor. Não há limite de extensões.

**Fonte:** `ic1_legado/IControlIT/ServiceDesk/Solicitacao_Detalhes.aspx.vb` - Linha 201

**Destino:** SUBSTITUÍDO

**Justificativa:** Risco de compliance. Sistema moderno exige aprovação de gerente/diretor para extensões e limita a 2 extensões por solicitação.

**Rastreabilidade:**
- RF Moderno: RN-RF038-007 (Extensão de prazo com aprovação)
- Implementação Moderna: Workflow de aprovação via `SlaExtensionApprovalService.cs`

---

## 7. GAP ANALYSIS (LEGADO × RF MODERNO)

| Funcionalidade | Existe Legado? | Existe Moderno? | Observação |
|----------------|----------------|-----------------|------------|
| **Configuração de SLA por tipo de solicitação** | Sim | Sim | Moderno adiciona campo de **prioridade** (alta/média/baixa) |
| **Cálculo automático de prazo** | Sim | Sim | Legado: horas corridas. Moderno: horário comercial + feriados |
| **Alertas escalonados (50%, 80%, 100%)** | Parcial | Sim | Legado: envio manual. Moderno: Hangfire job automático |
| **Escalação automática em breach** | Não | Sim | Nova funcionalidade no sistema moderno |
| **Pausa e retomada de SLA** | Sim | Sim | Legado: bug (não recalcula prazo). Moderno: corrigido |
| **Extensão de prazo** | Sim | Sim | Legado: sem aprovação. Moderno: workflow de aprovação obrigatória |
| **Dashboard em tempo real** | Não | Sim | Legado: grid estático. Moderno: SignalR push |
| **Relatórios de compliance** | Não | Sim | Nova funcionalidade no sistema moderno |
| **Registro de não-conformidades** | Não | Sim | Nova funcionalidade no sistema moderno |
| **SLA diferenciado por cliente** | Não | Sim | Nova funcionalidade no sistema moderno |
| **Notificações push (SignalR)** | Não | Sim | Legado: apenas email. Moderno: push + email |
| **Análise de tendências** | Não | Sim | Nova funcionalidade no sistema moderno |
| **Heatmap de horários críticos** | Não | Sim | Nova funcionalidade no sistema moderno |
| **Calendário de feriados customizado** | Não | Sim | Legado: 12 feriados hard-coded. Moderno: tabela configurável |
| **Horário de atendimento customizado** | Não | Sim | Legado: 24x7 sempre. Moderno: 8x5, 12x5, 24x7, custom |
| **Multi-tenancy (Row-Level Security)** | Não | Sim | Legado: multi-database. Moderno: RLS |
| **Auditoria completa** | Não | Sim | Legado: sem audit trail. Moderno: AuditInterceptor |

---

## 8. DECISÕES DE MODERNIZAÇÃO

### Decisão 1: Cálculo de Prazo em Application Layer (não SQL)

**Motivo:** Stored procedures dificultam testes unitários e manutenção. Lógica de negócio deve estar em C# para facilitar TDD e debugging.

**Impacto:** ALTO (requer refatoração completa do cálculo de prazo)

**Implementação:** `SlaCalculationService.cs` com método `CalculateDeadlineConsideringBusinessHours`

---

### Decisão 2: Alertas via Hangfire Jobs Recorrentes

**Motivo:** Legado depende de task agendada no Windows Server, que falha frequentemente. Hangfire é mais robusto e permite monitoramento via dashboard.

**Impacto:** MÉDIO (requer instalação e configuração de Hangfire)

**Implementação:** `SlaMonitoringJob.cs` executado a cada 15 minutos

---

### Decisão 3: Notificações Push via SignalR

**Motivo:** Dashboard estático do legado exige refresh manual. SignalR permite atualização em tempo real sem polling.

**Impacto:** ALTO (requer configuração de SignalR Hub e client-side JavaScript)

**Implementação:** `SlaHub.cs` + `sla-dashboard.component.ts` (Angular com SignalR client)

---

### Decisão 4: Multi-Tenancy com Row-Level Security

**Motivo:** Arquitetura multi-database do legado é insustentável (cada cliente exige novo database). RLS permite escalar horizontalmente.

**Impacto:** CRÍTICO (maior mudança arquitetural)

**Implementação:** Todas as tabelas SLA têm campo `TenantId` (Guid) + EF Core Query Filters

---

### Decisão 5: Tabela de Histórico de SLA

**Motivo:** Legado não registra histórico de pausas, retomadas e extensões. Impossível auditar ou justificar breaches.

**Impacto:** MÉDIO (nova tabela `SlaHistory`)

**Implementação:** Trigger automático em Entity Framework que registra snapshot em `SlaHistory` a cada modificação

---

## 9. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| **Perda de dados históricos de SLA** | ALTO | BAIXA | Script de migração preserva registros de `Solicitacao_SLA` e mapeia para `SlaConfiguration` com valores default para campos novos |
| **Cálculo de prazo diferente causa breaches** | ALTO | MÉDIA | Validação em homologação com 100 solicitações reais comparando prazo legado vs moderno |
| **Alertas duplicados durante migração** | MÉDIO | MÉDIA | Desativar task agendada do Windows Server ANTES de ativar Hangfire job |
| **Supervisores não entendem novo workflow de aprovação** | MÉDIO | ALTA | Treinamento obrigatório + documentação de processo + vídeo tutorial |
| **Performance de cálculo de feriados** | BAIXO | BAIXA | Caching de feriados por 24h em memória (Redis) |

---

## 10. RASTREABILIDADE (LEGADO → MODERNO)

| Elemento Legado | Referência RF | Referência UC | Status |
|----------------|---------------|---------------|--------|
| `Configuracao_SLA.aspx` | RF038 - Seção 2 | UC01-criar-sla | Migrado |
| `Dashboard_SLA.aspx` | RN-RF038-008 | UC07-monitorar-dashboard | Migrado |
| `Pausa_SLA.aspx` | RN-RF038-004 | UC08-pausar-retomar-sla | Migrado |
| `SlaService.asmx` | RN-RF038-001, RN-RF038-002 | - | Descartado (substituído por CQRS Handlers) |
| `sp_Solicitacao_SLA_Calcula_Prazo` | RN-RF038-001 | - | Descartado (lógica em `SlaCalculationService.cs`) |
| `sp_Solicitacao_SLA_Lista_Alertas` | RN-RF038-002 | - | Descartado (lógica em `SlaMonitoringJob.cs`) |
| Tabela `Solicitacao_SLA` | MD-RF038 - `SlaConfiguration` | - | Migrado (com expansão de campos) |
| Tabela `Solicitacao` (campos SLA) | MD-RF038 - `SlaTracking` | - | Migrado (tabela separada) |
| Feriados hard-coded (VB) | RN-RF038-006 | UC06-gerenciar-feriados | Descartado (substituído por tabela `SlaHoliday`) |

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|--------|------|-----------|-------|
| 1.0 | 2025-12-30 | Criação do documento de referência ao legado com 6 telas/serviços, 2 stored procedures, 2 tabelas, 6 regras implícitas e gap analysis completo | Agência ALC - alc.dev.br |
