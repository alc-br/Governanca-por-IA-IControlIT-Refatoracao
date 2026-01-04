# RL-RF028 — Referência ao Legado: Gestão de SLA - Operações

**Versão:** 2.0
**Data:** 2025-12-30
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF-028
**Sistema Legado:** IC1_Sistema_Producao - ASP.NET Web Forms + VB.NET
**Objetivo:** Documentar o comportamento do legado que serve de base para a refatoração de Gestão de SLA para Operações, garantindo rastreabilidade, entendimento histórico e mitigação de riscos.

---

## 1. CONTEXTO DO LEGADO

### 1.1 Stack Tecnológica

- **Arquitetura:** Monolítica WebForms com ASMX WebServices
- **Linguagem / Stack:** VB.NET, ASP.NET Web Forms (.NET Framework 4.5)
- **Banco de Dados:** SQL Server 2012
- **Multi-tenant:** Sim, mas por banco de dados separado (um DB por empresa)
- **Auditoria:** Parcial (logs textuais em arquivo text.log sem estrutura)
- **Configurações:** Web.config + tabela SistemaConfiguracao

### 1.2 Problemas Arquiteturais Identificados

- **Cálculo de SLA em VB.NET:** Stored Procedure `paCalculaSLA` com lógica complexa, difícil de manter
- **Não excluía feriados:** Contava todos os dias, inclusive feriados nacionais
- **Escalação manual:** Técnico precisava escalar manualmente, sem automação
- **Alertas apenas por email:** Sem notificação em tempo real (SignalR)
- **ViewState gigante:** Listagem de SLAs carregava ViewState >500KB
- **Sem versionamento:** Sobrescrevia SLA anterior ao editar, perdendo histórico

### 1.3 Multi-tenancy Legado

- **Modelo:** Um banco SQL Server por empresa (ex: `IControlIT_Cliente001`, `IControlIT_Cliente002`)
- **Isolamento:** Por connection string (risco de erro de conexão cruzada)
- **Migração moderna:** ClienteId em cada tabela com isolamento em row-level

---

## 2. TELAS DO LEGADO

### 2.1 Tela: SLAOperacao.aspx

- **Caminho:** `ic1_legado/IControlIT/ServiceDesk/SLA/SLAOperacao.aspx`
- **Responsabilidade:** Formulário de criação/edição de SLA (Server-Side Rendering)

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|------|------|-------------|-------------|
| txtNome | TextBox | Sim | Nome do SLA |
| txtDescricao | TextArea | Não | Descrição do SLA |
| ddlCalendario | DropDownList | Sim | Calendário 24x7, Comercial, Dias Úteis |
| txtMetaRespostaP1 | TextBox (int) | Sim | Minutos de meta resposta P1 |
| txtMetaResolucaoP1 | TextBox (int) | Sim | Minutos de meta resolução P1 |
| txtMetaAtendimentoP1 | TextBox (int) | Sim | Minutos de meta atendimento P1 |

#### Comportamentos Implícitos

- **Não validava hierarquia:** Permitia criar SLA com resposta >= resolução
- **Cálculo manual de horas:** Usuário digitava minutos, sistema não convertia automaticamente
- **Sem validação de duplicatas:** Permitia criar 2 SLAs com mesmo nome
- **Auditoria:** Gravava log textual em `D:\Logs\text.log` (sem estrutura JSON)

**DESTINO:** SUBSTITUÍDO (Componente Angular com validações robustas)

---

### 2.2 Tela: SLAOperacaoLista.aspx

- **Caminho:** `ic1_legado/IControlIT/ServiceDesk/SLA/SLAOperacaoLista.aspx`
- **Responsabilidade:** Listagem e busca de SLAs com GridView (paginação server-side no ViewState)

#### Problemas Identificados

- **ViewState gigante:** >500KB, paginação ineficiente (carregava TODOS os registros)
- **Filtros limitados:** Apenas nome e calendário
- **Sem exportação inline:** Exportava para Excel via Crystal Reports (lento)

**DESTINO:** SUBSTITUÍDO (SPA Angular com DataTable/Grid moderno)

---

### 2.3 Tela: SLAOperacaoConsulta.aspx

- **Caminho:** `ic1_legado/IControlIT/ServiceDesk/SLA/SLAOperacaoConsulta.aspx`
- **Responsabilidade:** Consulta de SLA de uma OS específica

#### Comportamento

- **Cálculo on-demand:** Chamava `paCalculaSLA` ao abrir tela (lento para >100 OSs)
- **Sem cache:** Recalculava sempre, mesmo sem mudança nos dados
- **Dashboard estático:** Não atualizava em tempo real

**DESTINO:** SUBSTITUÍDO (Dashboard SignalR em tempo real)

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

| Método | Local | Responsabilidade | Observações | Destino |
|------|-------|------------------|-------------|---------|
| `ListarSLAOperacao(idEmpresa)` | `WSSLA.asmx.vb` | Retorna lista de SLAs | Sem paginação, sem multi-tenancy | SUBSTITUÍDO (GET /api/sla-operacoes) |
| `ObterSLAOperacao(id)` | `WSSLA.asmx.vb` | Retorna SLA por ID | Sem validação de ClienteId | SUBSTITUÍDO (GET /api/sla-operacoes/{id}) |
| `CriarSLAOperacao(nome, metas)` | `WSSLA.asmx.vb` | Cria novo SLA | Validações mínimas (confia no frontend) | SUBSTITUÍDO (POST /api/sla-operacoes) |
| `AtualizarSLAOperacao(id, dados)` | `WSSLA.asmx.vb` | Atualiza SLA | Sobrescreve dados (sem versionamento) | SUBSTITUÍDO (PUT /api/sla-operacoes/{id}) |
| `DeletarSLAOperacao(id)` | `WSSLA.asmx.vb` | Hard delete | DELETE FROM SLAOperacao (sem auditoria) | SUBSTITUÍDO (Soft delete) |
| `CalcularSLAOS(idOS)` | `WSSLA.asmx.vb` | Calcula SLA de uma OS | Chama paCalculaSLA (stored procedure) | SUBSTITUÍDO (GET /api/sla-operacoes/{id}/calcular) |

---

## 4. TABELAS LEGADAS

| Tabela | Finalidade | Problemas Identificados | Destino |
|-------|------------|-------------------------|---------|
| `SLAOperacao` | Configuração de SLA | Sem multi-tenancy (IdEmpresa apenas), metas em minutos (int), sem versioning | SUBSTITUÍDO (SLAOperacao com ClienteId, TimeSpan, versionamento) |
| `Calendario` | Calendário de atendimento | Hardcoded (24x7, Comercial, Dias Úteis), sem exceções | ASSUMIDO (melhorado com exceções) |
| `PausaSLA` | Pausas de SLA | Apenas manual (usuário criava), sem pausa automática | SUBSTITUÍDO (pausa automática fora de horário) |
| `LogSLA` | Log de cálculo | Auditoria textual sem estrutura | SUBSTITUÍDO (Event Sourcing estruturado) |

### 4.1 DDL Legado: SLAOperacao

```sql
CREATE TABLE [dbo].[SLAOperacao](
    [Id] [int] IDENTITY(1,1) NOT NULL,
    [Nome] [varchar](100) NOT NULL,
    [Descricao] [varchar](500) NULL,
    [MetaRespostaP1] [int] NOT NULL, -- minutos
    [MetaRespostaP2] [int] NOT NULL,
    [MetaRespostaP3] [int] NOT NULL,
    [MetaRespostaP4] [int] NOT NULL,
    [MetaResolucaoP1] [int] NOT NULL,
    [MetaResolucaoP2] [int] NOT NULL,
    [MetaResolucaoP3] [int] NOT NULL,
    [MetaResolucaoP4] [int] NOT NULL,
    [MetaAtendimentoP1] [int] NOT NULL,
    [MetaAtendimentoP2] [int] NOT NULL,
    [MetaAtendimentoP3] [int] NOT NULL,
    [MetaAtendimentoP4] [int] NOT NULL,
    [IdCalendario] [int] NOT NULL,
    [DataCriacao] [datetime] NOT NULL,
    [UsuarioCriacao] [varchar](50) NOT NULL,
    [DataAlteracao] [datetime] NULL,
    [UsuarioAlteracao] [varchar](50) NULL,
    [IdEmpresa] [int] NOT NULL,
    CONSTRAINT [PK_SLAOperacao] PRIMARY KEY CLUSTERED ([Id] ASC),
    CONSTRAINT [FK_SLAOperacao_Calendario] FOREIGN KEY ([IdCalendario]) REFERENCES [Calendario]([Id]),
    CONSTRAINT [FK_SLAOperacao_Empresa] FOREIGN KEY ([IdEmpresa]) REFERENCES [Empresa]([Id])
)
```

**Problemas:**
- Metas em `int` (minutos) → Difícil conversão para horas
- Sem `ClienteId` (Guid) → Multi-tenancy por banco separado
- Sem `IsDeleted` → Hard delete
- Sem versionamento → Sobrescreve dados

**DESTINO:** SUBSTITUÍDO (tabela moderna com ClienteId, TimeSpan, soft delete, versionamento)

---

## 5. STORED PROCEDURES

| Procedure | Descrição | Lógica Principal (Linguagem Natural) | Destino |
|-----------|-----------|--------------------------------------|---------|
| `pa_CalculaSLA` | Calcula SLA consumido para uma OS | 1. Obtém data abertura da OS<br>2. Obtém data atual ou resolução<br>3. Calcula diferença em minutos<br>4. Deduz pausas manuais<br>5. Não deduz feriados ou fins de semana<br>6. Retorna percentual consumido | SUBSTITUÍDO (SLACalculator em C# + EF Core) |
| `pa_ListarSLAOperacao` | Lista SLAs da empresa | SELECT * FROM SLAOperacao WHERE IdEmpresa = @id | SUBSTITUÍDO (Query CQRS com paginação) |
| `pa_InsertSLAOperacao` | Insere novo SLA | INSERT INTO SLAOperacao com validações mínimas | SUBSTITUÍDO (CriarSLAOperacaoCommand) |
| `pa_UpdateSLAOperacao` | Atualiza SLA existente | UPDATE SLAOperacao sem versionamento | SUBSTITUÍDO (AtualizarSLAOperacaoCommand com versionamento) |

### 5.1 Lógica de `pa_CalculaSLA` (Extraída)

**Regras implícitas encontradas:**
1. Tempo = DataAtual - DataAbertura
2. Se OS resolvida, Tempo = DataResolucao - DataAbertura
3. Deduz pausas manuais (PausaSLA.DataFim - PausaSLA.DataInicio)
4. NÃO deduz feriados (problema identificado)
5. NÃO deduz fins de semana se calendário != 24x7 (problema identificado)
6. Percentual = (Tempo - Pausas) / MetaSLA * 100

**DESTINO:** SUBSTITUÍDO (algoritmo em C# com BrasilAPI para feriados)

---

## 6. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

### RL-RN-001: Cálculo de SLA sem Feriados

**Descrição:** O cálculo de SLA no legado contava todos os dias, inclusive feriados nacionais (Natal, Ano Novo, etc).

**Comportamento Observado:** Stored Procedure `paCalculaSLA` não consultava tabela de feriados, resultando em SLA consumido maior que o real.

**DESTINO:** SUBSTITUÍDO (integração com BrasilAPI para obter feriados automaticamente)

---

### RL-RN-002: Escalação Manual

**Descrição:** Técnico precisava escalar manualmente via botão "Escalar" na tela de OS.

**Comportamento Observado:** Nenhum sistema automático de escalação quando SLA atingia 75%, 90% ou 100%.

**DESTINO:** SUBSTITUÍDO (escalação automática em cascata conforme RN-SLA-028-05)

---

### RL-RN-003: Alertas Apenas por Email

**Descrição:** Alertas de SLA eram enviados apenas por email, sem notificação em tempo real.

**Comportamento Observado:** Job background executava a cada hora e enviava emails. Técnico não via alerta em tempo real no dashboard.

**DESTINO:** SUBSTITUÍDO (SignalR para notificações em tempo real + email)

---

### RL-RN-004: Sem Validação de Hierarquia de Tempos

**Descrição:** Sistema permitia criar SLA com resposta >= resolução (ex: resposta=8h, resolução=4h).

**Comportamento Observado:** Validação apenas no frontend (Javascript), backend aceitava qualquer valor.

**DESTINO:** SUBSTITUÍDO (validação rigorosa em backend com FluentValidation)

---

### RL-RN-005: Pausa Apenas Manual

**Descrição:** Pausas de SLA eram criadas manualmente pelo usuário via botão "Pausar SLA".

**Comportamento Observado:** Nenhuma pausa automática fora do horário de atendimento. Sistema contava tempo à noite e fins de semana mesmo em calendário "Dias Úteis".

**DESTINO:** SUBSTITUÍDO (pausa automática fora de horário conforme RN-SLA-028-03)

---

## 7. GAP ANALYSIS (LEGADO x RF MODERNO)

| Item | Legado | RF Moderno | Impacto | Observação |
|-----|--------|------------|---------|------------|
| **Cálculo de SLA** | Stored Procedure VB.NET | Algoritmo C# otimizado | Alto | Modernização permite testes unitários |
| **Feriados** | Não considerava | BrasilAPI integrada | Crítico | SLA justo ao cliente |
| **Escalação** | Manual | Automática em cascata | Alto | Reduz tempo de resposta |
| **Alertas** | Email apenas | Email + SMS + SignalR | Médio | Notificação em tempo real |
| **Dashboard** | Estático | SignalR em tempo real | Alto | Visibilidade instantânea |
| **Versionamento** | Não existe | Histórico completo | Médio | Auditoria regulatória |
| **Multi-tenancy** | Por banco separado | Por ClienteId (row-level) | Crítico | Reduz custo de infraestrutura |
| **Pausa Automática** | Não existe | Automática fora de horário | Alto | SLA justo, não penaliza cliente |
| **Validação Hierarquia** | Frontend apenas | Backend rigoroso | Médio | Garante integridade |
| **Soft Delete** | Hard delete | Soft delete | Baixo | Auditoria e recovery |

---

## 8. DECISÕES DE MODERNIZAÇÃO

### Decisão 1: Integração com BrasilAPI

**Descrição:** Substituir tabela de feriados manual por consulta automática à BrasilAPI.

**Motivo:** Tabela manual exigia manutenção anual, sujeita a erro humano. BrasilAPI sempre atualizada.

**Impacto:** Médio (requer fallback se API indisponível)

**Implementação:** Cache local de feriados, renovado automaticamente a cada ano.

---

### Decisão 2: Escalação Automática

**Descrição:** Criar escalação automática quando SLA atinge 75%, 90%, 100%.

**Motivo:** Reduzir dependência de ação manual, garantir operações críticas recebem atenção.

**Impacto:** Alto (requer algoritmo de seleção de técnico disponível)

**Implementação:** Escalação em cascata L1 → L2 → L3 → Manager com notificação SMS + email.

---

### Decisão 3: SignalR para Notificações

**Descrição:** Substituir email por notificações em tempo real via SignalR.

**Motivo:** Técnico vê alerta instantaneamente, não precisa esperar abrir email.

**Impacto:** Médio (requer infraestrutura SignalR)

**Implementação:** Hub SignalR com grupo por ClienteId, push em tempo real para todos os técnicos online.

---

## 9. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Mitigação |
|------|---------|-----------|
| **BrasilAPI indisponível** | Alto | Cache local de feriados, fallback para último ano cacheado |
| **Algoritmo de cálculo divergente** | Crítico | Testes paralelos (legado vs moderno) para validar paridade |
| **Escalação sem técnico disponível** | Médio | Escalar para gerente se nenhum técnico no nível |
| **SignalR não conecta** | Baixo | Fallback para email se SignalR falhar |
| **Multi-tenancy por ClienteId** | Médio | Migration de dados com validação rigorosa de ClienteId |

---

## 10. RASTREABILIDADE

| Elemento Legado | Referência RF Moderno |
|----------------|----------------------|
| `SLAOperacao.aspx` | RF-028 - Seção 4 (Funcionalidades: Criação de SLA) |
| `paCalculaSLA` | RN-SLA-028-02 (Cálculo exclui pausas e feriados) |
| `WSSLA.asmx.vb` | RF-028 - Seção 8 (API Endpoints) |
| Tabela `SLAOperacao` | MD-RF028.md (Modelo de Dados) |
| Escalação manual | RN-SLA-028-05 (Escalação automática) |
| Alertas por email | RN-SLA-028-04 (Alertas em cascata) |

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|--------|------|-----------|-------|
| 1.0 | 2025-12-30 | Versão inicial de referência ao legado | Claude Code |
| 2.0 | 2025-12-30 | Migração v1.0 → v2.0 (separação RF/RL completa) | Claude Code |

---

**Última Atualização**: 2025-12-30
**Autor**: Claude Code - Agência ALC
**Revisão**: Pendente
