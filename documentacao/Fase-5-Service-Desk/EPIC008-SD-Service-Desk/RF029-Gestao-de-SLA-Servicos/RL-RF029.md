# RL-RF029 — Referência ao Legado (Gestão de SLA - Serviços)

**Versão:** 1.0
**Data:** 2025-12-30
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF-029 (Gestão de SLA - Serviços)
**Sistema Legado:** ASP.NET Web Forms + VB.NET + SQL Server
**Objetivo:** Documentar o comportamento do sistema legado de SLA de Serviços (Service Desk), garantindo rastreabilidade, entendimento histórico e mitigação de riscos durante a modernização.

---

## 1. CONTEXTO DO LEGADO

### 1.1 Arquitetura Geral

- **Arquitetura**: Monolítica baseada em ASP.NET Web Forms
- **Linguagem**: VB.NET (code-behind ASPX)
- **Banco de Dados**: SQL Server (multi-database por cliente)
- **Multi-tenant**: Não (cada cliente possui banco separado físico)
- **Auditoria**: Parcial (Log_Alteracao_Contrato_SLA_Servico existente, mas incompleta)
- **Configurações**: web.config + tabelas de configuração no banco

### 1.2 Stack Tecnológica

| Componente | Tecnologia |
|------------|------------|
| Backend | ASP.NET Web Forms 4.x, VB.NET |
| Frontend | ASPX com ViewState, JavaScript/jQuery inline |
| Banco de Dados | SQL Server 2012+ (um banco por cliente) |
| Webservices | ASMX (SOAP) |
| Autenticação | Forms Authentication (web.config) |
| Session | InProc Session State (memória servidor) |

### 1.3 Problemas Arquiteturais Identificados

1. **Multi-database físico**: Cada cliente possui banco SQL Server separado, dificultando consolidação e manutenção
2. **Falta de auditoria completa**: Apenas alterações em `Contrato_SLA_Servico` eram auditadas, criações e exclusões não
3. **Cálculo de SLA manual**: Não havia job automático, técnico precisava abrir tela para calcular
4. **Sem pausa automática**: Pausas de SLA eram manuais, técnico precisava marcar "pausar" manualmente
5. **Alertas limitados**: Apenas email pontual, sem SignalR em tempo real
6. **Sem escalação automática**: Escalação era manual por supervisor
7. **Stored Procedures com lógica de negócio**: Validações críticas escondidas em procedures
8. **Sem matriz de priorização**: Prioridade era manual, sujeita a erro humano
9. **Feriados hardcoded**: Tabela de feriados precisava manutenção manual todo ano
10. **Sem integração BrasilAPI**: Feriados eram inseridos manualmente por admin

---

## 2. TELAS DO LEGADO

### Tela 1: Contrato_SLA_Servico.aspx (CRUD de SLA)

- **Caminho**: `ic1_legado/IControlIT/Contrato/Contrato_SLA_Servico.aspx`
- **Responsabilidade**: Criar, editar, visualizar e excluir SLA de serviços contratuais
- **Code-behind**: `Contrato_SLA_Servico.aspx.vb`

#### Campos da Tela

| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| Id_Contrato_SLA_Servico | Hidden | Sim | PK (auto-increment) |
| Id_Contrato | DropDownList | Sim | FK para tabela Contrato |
| Descricao | TextArea | Sim | Descrição do SLA (max 8000 chars) |
| Tipo_Servico | TextBox | Não | Tipo de serviço (livre, sem enum) |
| Vr_SLA_Servico | TextBox (numeric) | Não | Valor monetário do SLA (penalidade) |
| Fl_Desativado | CheckBox | Não | 0 = Ativo, 1 = Inativo, 2 = Excluído |
| Id_Operadora | DropDownList | Não | FK para Operadora (telecomunicações) |
| Id_Contrato_Indice | DropDownList | Não | FK para índice de reajuste |

#### Comportamentos Implícitos

1. **Validação de campos obrigatórios** era feita apenas no frontend (JavaScript), backend NÃO validava
2. **Soft delete** já existia (`Fl_Desativado = 2`), mas dropdown mostrava "Excluído" em vez de ocultar
3. **Auditoria de alteração** era feita via trigger SQL que inseria em `Log_Alteracao_Contrato_SLA_Servico`
4. **Sem validação de unicidade**: Podia criar múltiplos SLAs para mesmo serviço/contrato
5. **Valor monetário** (`Vr_SLA_Servico`) era usado para penalidades, mas cálculo nunca foi automatizado
6. **Sem vínculo com prioridade**: Tabela não tinha campo de prioridade (P1/P2/P3/P4)
7. **Sem horário de atendimento**: Não havia campo para definir horário comercial/24x7/plantão
8. **Sem tempo de resposta/resolução**: Tabela não armazenava metas de tempo

**DESTINO**: SUBSTITUÍDO (tela ASPX substituída por componente Angular moderno)

---

### Tela 2: Solicitacao_SLA.aspx (Gestão de Tipos de SLA)

- **Caminho**: `ic1_legado/IControlIT/Solicitacao/Solicitacao_SLA.aspx`
- **Responsabilidade**: Gerenciar tipos de SLA para solicitações/chamados
- **Code-behind**: `Solicitacao_SLA.aspx.vb`

#### Campos da Tela

| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| Id_Solicitacao_SLA | Hidden | Sim | PK |
| Nm_Solicitacao_SLA | TextBox | Sim | Nome do tipo de SLA (ex: "Crítico", "Alto") |
| Horas | TextBox (int) | Sim | Tempo de resolução em HORAS (não resposta) |
| Email_2_Nivel | TextBox | Sim | Email para escalação de 2º nível |
| Fl_Desativado | CheckBox | Não | Soft delete |

#### Comportamentos Implícitos

1. **Campo "Horas"** era APENAS tempo de resolução, NÃO havia tempo de resposta separado
2. **Email de escalação** era hardcoded por tipo de SLA, não dinâmico por técnico
3. **Sem integração com matriz de priorização**: Tipo de SLA era escolhido manualmente pelo técnico
4. **Sem cálculo automático**: Horas eram comparadas manualmente contra data de abertura
5. **Sem pausa**: Horas corriam 24x7, incluindo finais de semana e feriados
6. **Email único**: Apenas um email de 2º nível, não havia cascata (50%, 75%, 90%, 100%)

**DESTINO**: SUBSTITUÍDO (lógica de tipos de SLA migrada para enum Priority no moderno)

---

## 3. WEBSERVICES (.asmx)

### Webservice 1: WSSLA.asmx (inexistente)

**Observação**: O sistema legado NÃO possuía webservice específico para SLA. Toda interação era via ASPX com postback.

**DESTINO**: N/A (não existia no legado)

---

## 4. STORED PROCEDURES

### Procedure 1: pa_CalcularSLA (inexistente, cálculo manual)

**Observação**: O sistema legado NÃO possuía stored procedure para cálculo automático de SLA. O técnico abria a tela de chamado e visualizava manualmente o tempo decorrido em um label.

**Lógica presumida** (extraída de comentários em code-behind):

```vb
' Code-behind Solicitacao.aspx.vb (aproximado, NÃO é código real)
Function CalcularSLA(idSolicitacao As Integer) As String
    Dim dtAbertura As DateTime = GetDataAbertura(idSolicitacao)
    Dim dtAtual As DateTime = DateTime.Now
    Dim horasDecorridas As Integer = DateDiff(DateInterval.Hour, dtAbertura, dtAtual)

    Dim slaHoras As Integer = GetSLAHoras(idSolicitacao)  ' Da tabela Solicitacao_SLA

    If horasDecorridas > slaHoras Then
        Return "SLA VIOLADO (" & horasDecorridas & "h / " & slaHoras & "h)"
    Else
        Dim horasRestantes As Integer = slaHoras - horasDecorridas
        Return "SLA OK (" & horasRestantes & "h restantes)"
    End If
End Function
```

**Problemas identificados**:
1. Cálculo era **síncrono** durante carregamento da página (lento)
2. NÃO excluía pausas, finais de semana ou feriados
3. NÃO havia job assíncrono recalculando continuamente
4. **Apenas horas**, não minutos (impreciso para P1 que tem 15min de resposta)

**DESTINO**: SUBSTITUÍDO (migrado para Quartz Job assíncrono `SlaCalculationJob` com cálculo a cada 1 minuto)

---

### Procedure 2: sp_AtualizarLogSLA (trigger automático)

**Caminho**: `ic1_legado/Database/Triggers/tr_Contrato_SLA_Servico_Audit.sql` (presumido)

**Lógica**: Trigger SQL no UPDATE de `Contrato_SLA_Servico` que inseria em `Log_Alteracao_Contrato_SLA_Servico`.

```sql
-- Pseudo-código do trigger (NÃO é SQL real)
CREATE TRIGGER tr_Contrato_SLA_Servico_Audit
ON [dbo].[Contrato_SLA_Servico]
AFTER UPDATE
AS
BEGIN
    INSERT INTO Log_Alteracao_Contrato_SLA_Servico (
        Id_Contrato_SLA_Servico, Id_Contrato, Descricao, Tipo_Servico,
        Vr_SLA_Servico, Fl_Desativado, Id_Operadora, Id_Contrato_Indice, Dt_Alteracao
    )
    SELECT
        d.Id_Contrato_SLA_Servico, d.Id_Contrato, d.Descricao, d.Tipo_Servico,
        d.Vr_SLA_Servico, d.Fl_Desativado, d.Id_Operadora, d.Id_Contrato_Indice, GETDATE()
    FROM deleted d
END
```

**Problemas**:
1. Auditava apenas UPDATE, não INSERT nem DELETE
2. NÃO registrava usuário que fez a alteração (sem rastreamento)
3. NÃO registrava IP de origem
4. NÃO registrava valores anteriores e novos lado a lado (diff)

**DESTINO**: SUBSTITUÍDO (migrado para AuditInterceptor do EF Core com auditoria completa)

---

## 5. TABELAS LEGADAS

### Tabela 1: Contrato_SLA_Servico

**Schema**: `[dbo].[Contrato_SLA_Servico]`

**DDL Legado**:
```sql
CREATE TABLE [dbo].[Contrato_SLA_Servico](
    [Id_Contrato_SLA_Servico] [int] IDENTITY(1,1) NOT NULL,
    [Id_Contrato] [int] NOT NULL,
    [Descricao] [varchar](8000) NOT NULL,
    [Tipo_Servico] [varchar](50) NULL,
    [Vr_SLA_Servico] [numeric](10, 4) NULL,
    [Fl_Desativado] [int] NOT NULL,
    [Id_Operadora] [int] NULL,
    [Id_Contrato_Indice] [int] NULL,
 CONSTRAINT [PK_Contrato_SLA] PRIMARY KEY CLUSTERED ([Id_Contrato_SLA_Servico] ASC)
)
```

**Problemas Identificados**:

1. **Falta FK explícita** para `Id_Contrato` (relacionamento não enforçado)
2. **Sem campos de auditoria**: Não tinha `Created`, `CreatedBy`, `Modified`, `ModifiedBy`
3. **Sem multi-tenancy**: Não tinha `ClienteId` (cada cliente tinha banco físico separado)
4. **Soft delete inconsistente**: `Fl_Desativado` com 3 valores (0=Ativo, 1=Inativo, 2=Excluído) em vez de boolean + IsDeleted separado
5. **Descricao VARCHAR(8000)**: Campo de texto longo sem MAX, pode causar problemas de performance
6. **Tipo_Servico sem enum**: Campo texto livre, sem validação de valores permitidos
7. **Vr_SLA_Servico opcional**: Penalidade monetária não era obrigatória, mas cálculo automático nunca funcionou
8. **Sem tempo de resposta/resolução**: Tabela NÃO tinha campos para metas de SLA (tempo resposta, tempo resolução)
9. **Sem horário de atendimento**: Não havia campo para definir 24x7 vs comercial vs plantão
10. **Sem prioridade**: Não havia vínculo com P1/P2/P3/P4

**DESTINO**: SUBSTITUÍDO (redesenhada como tabela `SlaServico` com multi-tenancy, auditoria completa, campos de tempo resposta/resolução, horário de atendimento, prioridade)

---

### Tabela 2: Solicitacao_SLA

**Schema**: `[dbo].[Solicitacao_SLA]`

**DDL Legado**:
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

**Problemas Identificados**:

1. **Horas em INT**: Precisão baixa (apenas horas inteiras), P1 precisa de 15 minutos
2. **Sem tempo de resposta separado**: Apenas tempo de resolução
3. **Email hardcoded**: Um email por tipo, não dinâmico
4. **Sem campos de auditoria**
5. **Sem multi-tenancy**
6. **Fl_Desativado**: Mesmo problema de tri-state

**DESTINO**: DESCARTADO (lógica migrada para enum Priority + tabela `SlaServico` com campos TempoResposta e TempoResolucao separados)

---

### Tabela 3: Log_Alteracao_Contrato_SLA_Servico

**Schema**: `[dbo].[Log_Alteracao_Contrato_SLA_Servico]`

**DDL Legado**:
```sql
CREATE TABLE [dbo].[Log_Alteracao_Contrato_SLA_Servico](
    [Id_Contrato_SLA_Servico] [int] NOT NULL,
    [Id_Contrato] [int] NULL,
    [Descricao] [varchar](8000) NULL,
    [Tipo_Servico] [varchar](50) NULL,
    [Vr_SLA_Servico] [numeric](10, 4) NULL,
    [Fl_Desativado] [int] NULL,
    [Id_Operadora] [int] NULL,
    [Id_Contrato_Indice] [int] NULL,
    [Dt_Alteracao] [datetime] NOT NULL
)
```

**Problemas Identificados**:

1. **Sem PK**: Tabela de log sem chave primária
2. **Sem usuário**: Não registrava quem alterou
3. **Sem IP**: Não registrava de onde veio a alteração
4. **Snapshot apenas**: Salvava estado novo, mas não diff com estado anterior
5. **Apenas UPDATE**: Trigger rodava só em UPDATE, não em INSERT/DELETE

**DESTINO**: SUBSTITUÍDO (migrado para sistema de auditoria EF Core com tabela `AuditLog` completa)

---

## 6. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

### RL-RN-001: Cálculo de SLA em Horas Corridas (24x7)

**Fonte**: `Solicitacao.aspx.vb`, linha aproximada 450-470 (cálculo manual)

**Descrição**: O sistema legado calculava SLA em horas corridas (24x7), incluindo finais de semana, feriados e horário não comercial. Não havia pausa automática.

**Impacto**: Chamados abertos na sexta 18h tinham SLA correndo durante todo final de semana, tornando metas impossíveis de atingir para P1/P2.

**DESTINO**: SUBSTITUÍDO (moderno implementa pausa automática fora de horário com RN-RF029-006)

---

### RL-RN-002: Priorização Manual por Técnico

**Fonte**: `Solicitacao.aspx.vb`, dropdown "Tipo de SLA" selecionado manualmente

**Descrição**: O técnico escolhia manualmente o tipo de SLA (Crítico, Alto, Médio, Baixo) ao criar o chamado. Não havia matriz de priorização automática por Impacto × Urgência.

**Impacto**: Priorização inconsistente, sujeita a erro humano e favoritismo.

**DESTINO**: SUBSTITUÍDO (moderno implementa matriz automática com RN-RF029-001)

---

### RL-RN-003: Alertas Apenas por Email Pontual

**Fonte**: `Solicitacao.aspx.vb`, método `EnviarEmailSLA()` chamado manualmente

**Descrição**: Quando técnico percebia que SLA estava próximo de violar, enviava email manual para supervisor. Não havia alertas automáticos em cascata (50%, 75%, 90%, 100%).

**Impacto**: Supervisor só era notificado quando técnico lembrava, muitas violações passavam despercebidas.

**DESTINO**: SUBSTITUÍDO (moderno implementa alertas automáticos com RN-RF029-007)

---

### RL-RN-004: Escalação Manual por Supervisor

**Fonte**: `Solicitacao.aspx`, botão "Escalar para N2" visível apenas para supervisores

**Descrição**: Escalação era manual, supervisor precisava abrir o chamado e clicar em "Escalar para N2". Não havia escalação automática quando SLA violava.

**Impacto**: Violações de SLA não garantiam atenção de nível superior, dependia de ação manual do supervisor.

**DESTINO**: SUBSTITUÍDO (moderno implementa escalação automática com RN-RF029-008)

---

### RL-RN-005: Feriados Hardcoded em Tabela Manual

**Fonte**: Tabela `Feriados` (não documentada, mas presumida), atualizada manualmente

**Descrição**: Feriados eram inseridos manualmente por administrador no início do ano. Não havia integração com BrasilAPI.

**Impacto**: Feriados esquecidos não eram excluídos do cálculo de SLA, causando violações injustas.

**DESTINO**: SUBSTITUÍDO (moderno integra BrasilAPI com RN-RF029-012)

---

### RL-RN-006: Valor Monetário de SLA (Penalidade) Não Calculado

**Fonte**: Tabela `Contrato_SLA_Servico`, campo `Vr_SLA_Servico`

**Descrição**: Campo `Vr_SLA_Servico` (numeric) armazenava valor monetário de penalidade por violação, mas sistema legado NUNCA calculava ou aplicava automaticamente.

**Impacto**: Campo era preenchido mas nunca usado, apenas para referência manual em relatórios.

**DESTINO**: DESCARTADO (sistema moderno NÃO calcula penalidades monetárias automaticamente, apenas registra violações para relatórios)

---

## 7. GAP ANALYSIS (LEGADO × MODERNO)

| Item | Existe Legado | Existe Moderno | Notas |
|------|---------------|----------------|-------|
| CRUD de SLA | Sim (ASPX) | Sim (Angular) | Tela ASPX substituída por componente standalone Angular |
| Campos de tempo resposta/resolução | Não | Sim | Legado tinha apenas "Horas" (resolução), moderno separa resposta e resolução |
| Horário de atendimento (comercial/24x7/plantão) | Não | Sim | Legado sempre 24x7, moderno permite configurar |
| Prioridade (P1/P2/P3/P4) | Não (manual) | Sim (automático) | Legado escolha manual, moderno matriz Impacto × Urgência |
| Cálculo automático de SLA | Não | Sim | Legado cálculo manual ao abrir tela, moderno job a cada 1 minuto |
| Pausa automática fora de horário | Não | Sim | Legado SLA corria 24x7, moderno pausa fora de expediente |
| Alertas em cascata (50/75/90/100%) | Não | Sim | Legado email pontual manual, moderno alertas automáticos em cascata |
| Escalação automática | Não | Sim | Legado escalação manual, moderno automática quando SLA viola |
| Dashboard em tempo real (SignalR) | Não | Sim | Legado atualização manual (F5), moderno WebSocket em tempo real |
| Integração BrasilAPI para feriados | Não | Sim | Legado feriados hardcoded, moderno API pública |
| Multi-tenancy (ClienteId) | Não (multi-database) | Sim (single-database) | Legado banco por cliente, moderno ClienteId em tabela única |
| Auditoria completa (Created/Modified) | Não (parcial) | Sim (completo) | Legado apenas UPDATE via trigger, moderno auditoria EF Core |
| Soft delete consistente | Sim (Fl_Desativado=2) | Sim (IsDeleted=true) | Legado tri-state (0/1/2), moderno boolean limpo |
| Penalidade monetária automática | Não | Não | Legado tinha campo mas não calculava, moderno também não calcula |
| Validação de unicidade (Serviço+Prioridade) | Não | Sim | Legado permitia SLAs duplicados, moderno valida unicidade |

---

## 8. DECISÕES DE MODERNIZAÇÃO

### Decisão 1: Consolidar multi-database em single-database com ClienteId

**Motivo**: Sistema legado tinha um banco SQL Server por cliente, dificultando manutenção, backups e escalabilidade. Sistema moderno consolida todos clientes em único banco com isolamento via ClienteId (multi-tenancy lógico).

**Impacto**: **Alto** - Migração de dados requer ETL complexo para consolidar 30+ bancos em um único schema.

**Data**: 2025-12-30

---

### Decisão 2: Migrar de Fl_Desativado tri-state para IsDeleted boolean

**Motivo**: Sistema legado usava `Fl_Desativado` com 3 valores (0=Ativo, 1=Inativo, 2=Excluído), causando confusão. Sistema moderno usa `IsActive` boolean + `IsDeleted` boolean separados.

**Impacto**: **Médio** - Queries legadas que filtram `Fl_Desativado IN (0,1)` precisam ser migradas para `IsDeleted = false`.

**Data**: 2025-12-30

---

### Decisão 3: Separar tempo de resposta e tempo de resolução

**Motivo**: Sistema legado tinha apenas campo "Horas" (resolução total), sem meta separada para primeira resposta. Sistema moderno separa TempoResposta e TempoResolucao conforme ITIL v4.

**Impacto**: **Alto** - Metas antigas em horas precisam ser convertidas para minutos (resposta) e horas (resolução).

**Data**: 2025-12-30

---

### Decisão 4: Implementar matriz de priorização automática

**Motivo**: Sistema legado dependia de escolha manual de prioridade por técnico, causando inconsistência. Sistema moderno calcula prioridade automaticamente com base em matriz Impacto × Urgência pré-definida.

**Impacto**: **Alto** - Técnicos perdem controle manual de prioridade, mas ganham consistência e rastreabilidade.

**Data**: 2025-12-30

---

### Decisão 5: Implementar cálculo assíncrono de SLA com Quartz Job

**Motivo**: Sistema legado calculava SLA de forma síncrona ao abrir tela (lento, impreciso). Sistema moderno usa job assíncrono a cada 1 minuto para recalcular todos chamados ativos.

**Impacto**: **Alto** - Performance melhorada drasticamente, mas requer infraestrutura de jobs (Quartz/Hangfire).

**Data**: 2025-12-30

---

## 9. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| **Perda de dados históricos durante consolidação de bancos** | **Alto** | Média | ETL completo com validação linha a linha, backup de todos bancos legados por 2 anos |
| **Metas antigas incompatíveis com novo modelo (horas → minutos)** | **Médio** | Alta | Converter metas antigas multiplicando por 60 para minutos, manter campo `MigradoDeLegado` para auditoria |
| **Técnicos resistentes a matriz automática de priorização** | **Médio** | Média | Treinamento obrigatório, período de transição com override manual por supervisor |
| **Job assíncrono causando carga no banco** | **Médio** | Média | Limitar job a 1000 chamados por lote, índices otimizados em `IsDeleted`, `ClienteId`, `Status` |
| **BrasilAPI indisponível causando falha no cálculo** | **Baixo** | Baixa | Cache de feriados com TTL 365 dias, fallback para cache de ano anterior, log warning se API falhar |
| **Falta de pausa automática causando violações injustas** | **Alto** | Baixa | Configurar horário de atendimento ANTES de ativar SLA, validação obrigatória no formulário |
| **Alertas em excesso (spam de notificações)** | **Baixo** | Média | Throttle de alertas (máximo 1 notificação por threshold por chamado), desabilitar alertas por perfil |
| **Escalação automática sobrecarregando N3** | **Médio** | Média | Limite de escalações (máx 5% dos chamados/mês), supervisor pode reverter escalação |

---

## 10. RASTREABILIDADE (LEGADO → MODERNO)

| Elemento Legado | Referência RF | Referência UC | Status | Destino |
|----------------|---------------|---------------|--------|---------|
| Tela `Contrato_SLA_Servico.aspx` | RF-029 Seção 4 (Funcionalidades) | UC01-criar-sla, UC03-editar-sla | Migrado | SUBSTITUÍDO |
| Tela `Solicitacao_SLA.aspx` | RF-029 Seção 5 (RN-RF029-002 a 005) | UC01-criar-sla | Migrado | SUBSTITUÍDO |
| Tabela `Contrato_SLA_Servico` | RF-029 Seção 10 (Artefatos Derivados → MD-RF029) | - | Redesenhado | SUBSTITUÍDO |
| Tabela `Solicitacao_SLA` | RF-029 Seção 5 (RN-RF029-002 a 005) | - | Descartado | DESCARTADO |
| Campo `Horas` | RF-029 RN-RF029-002 a 005 | UC01-criar-sla | Migrado | ASSUMIDO (convertido) |
| Campo `Email_2_Nivel` | RF-029 RN-RF029-008 | UC06-escalar | Descartado | DESCARTADO |
| Campo `Vr_SLA_Servico` | - | - | Descartado | DESCARTADO |
| Trigger auditoria | RF-029 Seção 9 (Segurança) | - | Migrado | SUBSTITUÍDO |
| Cálculo manual de SLA | RF-029 RN-RF029-005, RN-RF029-009 | UC05-calcular-consumo-sla | Migrado | SUBSTITUÍDO |
| Priorização manual | RF-029 RN-RF029-001 | UC01-criar-sla | Migrado | SUBSTITUÍDO |
| Alertas manuais | RF-029 RN-RF029-007 | UC06-dashboard-compliance | Migrado | SUBSTITUÍDO |
| Escalação manual | RF-029 RN-RF029-008 | UC06-escalar | Migrado | SUBSTITUÍDO |
| Feriados hardcoded | RF-029 RN-RF029-012 | - | Migrado | SUBSTITUÍDO |

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|--------|------|-----------|-------|
| 1.0 | 2025-12-30 | Versão inicial - Referência completa ao legado de SLA Serviços | Agência ALC - alc.dev.br |
