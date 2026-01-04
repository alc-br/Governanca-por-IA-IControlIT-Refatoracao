# RL-RF033 — Referência ao Legado (Gestão de Chamados)

**Versão:** 1.0
**Data:** 2025-12-30
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF033 - Gestão de Chamados (Service Desk)
**Sistema Legado:** ASP.NET Web Forms + VB.NET
**Objetivo:** Documentar o comportamento do sistema legado de chamados (Help Desk / Service Desk) que serve de base para a refatoração, garantindo rastreabilidade, entendimento histórico e mitigação de riscos.

---

## 1. CONTEXTO DO SISTEMA LEGADO

### 1.1 Arquitetura Geral

- **Arquitetura:** Monolítica Web Forms
- **Linguagem / Stack:** ASP.NET Web Forms + VB.NET
- **Banco de Dados:** SQL Server
- **Multi-tenant:** ❌ Não implementado (sem campo `Id_Conglomerado`)
- **Auditoria:** ❌ Inexistente (sem campos de criação/alteração)
- **Configurações:** Web.config
- **Controle de SLA:** Manual via campo texto `Excedente_SLA` (varchar(8000))
- **Notificações:** Sistema básico via campos `Id_Mail_Caixa_Saida_Usuario`, `Id_Mail_Caixa_Saida_Operadora`

### 1.2 Problemas Arquiteturais Identificados

1. **Ausência de Multi-Tenancy** - Todos os dados compartilhados sem isolamento
2. **Sem Auditoria** - Não há rastreamento de quem criou/alterou chamados
3. **Sem Soft Delete** - Exclusões físicas causam perda de dados
4. **SLA Manual** - Campo texto livre sem cálculo automático
5. **Notificações Manuais** - Controle via IDs de caixa de saída (não automatizado)
6. **Enum de Status Não Documentado** - Campo `Fl_Status` (int) sem documentação clara
7. **Sem Validações de Transição** - Não há controle de workflow
8. **Performance** - Sem índices otimizados, queries lentas

---

## 2. TELAS DO LEGADO

### 2.1 Tela Principal de Chamados

**Identificação no Código Legado:**
- **Componente:** Tabela `Solicitacao`
- **Local:** `ic1_legado/IControlIT/BancoDados/Interno/K2A.sql:8358`

**Campos Principais:**

| Campo Legado | Tipo | Obrigatório | Observações |
|--------------|------|-------------|-------------|
| `Id_Solicitacao` | `int IDENTITY(1,1)` | ✅ Sim (PK) | Migrar para `Guid` no moderno |
| `Nm_Solicitacao` | `varchar(300)` | ✅ Sim | Título do chamado |
| `Dt_Solicitacao` | `datetime` | ✅ Sim | Data de abertura |
| `Id_Usuario` | `int` | ✅ Sim | Usuário solicitante (FK) |
| `Id_Ativo_Tipo` | `int` | ✅ Sim | Tipo de ativo relacionado (FK) |
| `Id_Solicitacao_Tipo` | `int` | ✅ Sim | Tipo de solicitação (FK) |
| `Id_Consumidor_Unidade` | `int` | ❌ Não | Unidade de consumidor (FK opcional) |
| `Excedente_SLA` | `varchar(8000)` | ❌ Não | **Controle manual de SLA** (texto livre!) |
| `Dt_Encerramento` | `datetime` | ❌ Não | Data de encerramento |
| `Id_Solicitacao_Solucao` | `int` | ❌ Não | Solução aplicada (FK opcional) |
| `Id_Mail_Caixa_Saida_Usuario` | `int` | ❌ Não | Controle de e-mail enviado ao usuário |
| `Id_Mail_Caixa_Saida_Operadora` | `int` | ❌ Não | Controle de e-mail enviado à operadora |
| `Dt_Vencimento` | `datetime` | ✅ Sim | Data de vencimento do SLA |
| `Fl_Status` | `int` | ✅ Sim | Status do chamado (enum não documentado) |

**DDL Original:**

```sql
CREATE TABLE [dbo].[Solicitacao](
    [Id_Solicitacao] [int] IDENTITY(1,1) NOT NULL,
    [Nm_Solicitacao] [varchar](300) NOT NULL,
    [Dt_Solicitacao] [datetime] NOT NULL,
    [Id_Usuario] [int] NOT NULL,
    [Id_Ativo_Tipo] [int] NOT NULL,
    [Id_Solicitacao_Tipo] [int] NOT NULL,
    [Id_Consumidor_Unidade] [int] NULL,
    [Excedente_SLA] [varchar](8000) NULL,
    [Dt_Encerramento] [datetime] NULL,
    [Id_Solicitacao_Solucao] [int] NULL,
    [Id_Mail_Caixa_Saida_Usuario] [int] NULL,
    [Id_Mail_Caixa_Saida_Operadora] [int] NULL,
    [Dt_Vencimento] [datetime] NOT NULL,
    [Fl_Status] [int] NOT NULL,
 CONSTRAINT [PK_Solicitacao] PRIMARY KEY CLUSTERED
(
    [Id_Solicitacao] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, FILLFACTOR = 90) ON [PRIMARY]
) ON [PRIMARY]
GO
```

**Comportamentos Implícitos Identificados:**
1. SLA calculado manualmente e armazenado em campo texto `Excedente_SLA`
2. Notificações disparadas via atualização de campos `Id_Mail_Caixa_Saida_*`
3. Status controlado via campo `Fl_Status` (int) sem validação de transições
4. Sem controle de escalação automática
5. Sem pausas de SLA em status "Aguardando"

---

### 2.2 Tela de Interações (Itens do Chamado)

**Identificação no Código Legado:**
- **Componente:** Tabela `Solicitacao_Item`
- **Local:** `ic1_legado/IControlIT/BancoDados/Interno/K2A.sql:8429`

**Campos Principais:**

| Campo Legado | Tipo | Obrigatório | Observações |
|--------------|------|-------------|-------------|
| `Id_Solicitacao_Item` | `int IDENTITY(1,1)` | ✅ Sim (PK) | Migrar para `Guid` |
| `Id_Solicitacao` | `int` | ✅ Sim | FK para `Solicitacao` |
| `Nm_Solicitacao_Item` | `varchar(8000)` | ✅ Sim | Descrição da interação |
| `Id_Usuario` | `int` | ✅ Sim | Usuário que criou a interação |
| `Dt_Hr_Solicitacao_Item` | `datetime` | ✅ Sim | Data/hora da interação |
| `Fl_Publicado` | `int` | ✅ Sim | 0 = privado, 1 = público |

**DDL Original:**

```sql
CREATE TABLE [dbo].[Solicitacao_Item](
    [Id_Solicitacao_Item] [int] IDENTITY(1,1) NOT NULL,
    [Id_Solicitacao] [int] NOT NULL,
    [Nm_Solicitacao_Item] [varchar](8000) NOT NULL,
    [Id_Usuario] [int] NOT NULL,
    [Dt_Hr_Solicitacao_Item] [datetime] NOT NULL,
    [Fl_Publicado] [int] NOT NULL,
 CONSTRAINT [PK_Solicitacao_Item] PRIMARY KEY CLUSTERED
(
    [Id_Solicitacao_Item] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, FILLFACTOR = 90) ON [PRIMARY]
) ON [PRIMARY]
GO
```

**Comportamentos Implícitos:**
- `Fl_Publicado = 1` → interação visível ao solicitante
- `Fl_Publicado = 0` → interação apenas para equipe de suporte
- Sem validação de permissões para criar interações privadas

---

### 2.3 Tela de Avaliação de Satisfação

**Identificação no Código Legado:**
- **Componente:** Tabela `Solicitacao_Avaliacao`
- **Local:** `ic1_legado/IControlIT/BancoDados/Interno/K2A.sql:8384`

**Campos Principais:**

| Campo Legado | Tipo | Obrigatório | Observações |
|--------------|------|-------------|-------------|
| `Id_Solicitacao_Avaliacao` | `int IDENTITY(1,1)` | ✅ Sim (PK) | Migrar para `Guid` |
| `Id_Solicitacao` | `int` | ✅ Sim | FK para `Solicitacao` |
| `Dt_Avaliacao` | `datetime` | ✅ Sim | Data da avaliação |
| `Avaliacao` | `int` | ✅ Sim | Nota de satisfação |
| `Descricao` | `varchar(100)` | ❌ Não | Comentário opcional |

**DDL Original:**

```sql
CREATE TABLE [dbo].[Solicitacao_Avaliacao](
    [Id_Solicitacao_Avaliacao] [int] IDENTITY(1,1) NOT NULL,
    [Id_Solicitacao] [int] NOT NULL,
    [Dt_Avaliacao] [datetime] NOT NULL,
    [Avaliacao] [int] NOT NULL,
    [Descricao] [varchar](100) NULL,
 CONSTRAINT [PK_Solicitacao_Avaliacao] PRIMARY KEY CLUSTERED
(
    [Id_Solicitacao_Avaliacao] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, FILLFACTOR = 90) ON [PRIMARY]
) ON [PRIMARY]
GO
```

**Comportamentos Implícitos:**
- Sem validação de range de nota (permite valores fora de 1-5)
- Sem validação de unicidade (permite múltiplas avaliações)
- Descrição limitada a 100 caracteres (insuficiente para feedback detalhado)

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

**Análise realizada:** Não foram identificados WebServices específicos (.asmx) dedicados à gestão de chamados no código legado.

**Observação:** A lógica de negócio provavelmente está embutida nos code-behind (.aspx.vb) das páginas Web Forms.

---

## 4. STORED PROCEDURES LEGADAS

**Análise realizada:** Não foram identificadas stored procedures específicas para gestão de chamados.

**Observação:** O sistema legado provavelmente utiliza queries SQL diretas no código VB.NET (anti-pattern).

---

## 5. TABELAS LEGADAS

### 5.1 Tabelas Principais

| Tabela Legada | Finalidade | Problemas Identificados |
|---------------|------------|-------------------------|
| `Solicitacao` | Tabela principal de chamados | ❌ Sem multi-tenancy, sem auditoria, sem soft delete, SLA em campo texto |
| `Solicitacao_Item` | Interações/itens do chamado | ❌ Sem multi-tenancy, sem auditoria, sem soft delete |
| `Solicitacao_Avaliacao` | Avaliações de satisfação | ❌ Sem validação de unicidade, sem multi-tenancy |
| `Solicitacao_Tipo` | Tipos de solicitação | ❌ Sem multi-tenancy, sem auditoria |
| `Solicitacao_SLA` | Definições de SLA | ❌ Sem multi-tenancy, sem auditoria |
| `Solicitacao_Fila_Atendimento` | Filas de atendimento | ❌ Sem multi-tenancy, sem auditoria |
| `Solicitacao_Solucao` | Soluções aplicadas | ❌ Sem multi-tenancy, sem auditoria |
| `Solicitacao_Data_Parada` | Feriados e datas de parada | ❌ Sem multi-tenancy, sem auditoria |
| `Rl_Solicitacao_Ativo` | Relacionamento com ativos | ❌ Sem multi-tenancy, tabela de relacionamento N:N não documentada |
| `Solicitacao_Permissao` | Controle de permissões customizado | ❌ Não segue padrão RBAC, difícil manutenção |

### 5.2 Relacionamentos

```
Solicitacao (Chamado Principal)
├── FK: Id_Usuario → Usuario.Id_Usuario (Solicitante)
├── FK: Id_Ativo_Tipo → Ativo_Tipo.Id_Ativo_Tipo (Tipo de Ativo)
├── FK: Id_Solicitacao_Tipo → Solicitacao_Tipo.Id_Solicitacao_Tipo (Tipo)
├── FK: Id_Consumidor_Unidade → Consumidor_Unidade.Id_Consumidor_Unidade (Unidade)
└── FK: Id_Solicitacao_Solucao → Solicitacao_Solucao.Id_Solicitacao_Solucao (Solução)

Solicitacao_Item (Interações)
└── FK: Id_Solicitacao → Solicitacao.Id_Solicitacao

Solicitacao_Avaliacao (Avaliações)
└── FK: Id_Solicitacao → Solicitacao.Id_Solicitacao

Rl_Solicitacao_Ativo (Vinculação N:N com Ativos)
├── FK: Id_Solicitacao → Solicitacao.Id_Solicitacao
└── FK: Id_Ativo → Ativo.Id_Ativo
```

---

## 6. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

### RL-RN-001: Campos Obrigatórios

**Fonte:** Análise do DDL da tabela `Solicitacao`

**Descrição:** Os campos obrigatórios na criação do chamado são: `Nm_Solicitacao`, `Dt_Solicitacao`, `Id_Usuario`, `Id_Ativo_Tipo`, `Id_Solicitacao_Tipo`, `Dt_Vencimento`, `Fl_Status`.

**Destino no RF Moderno:** ✅ **ASSUMIDO** como RN-RF033-01

**Observações:** Mesma regra mantida, porém com validações mais rigorosas no moderno.

---

### RL-RN-002: SLA Manual em Campo Texto

**Fonte:** Campo `Excedente_SLA varchar(8000)`

**Descrição:** O controle de excedente de SLA era feito manualmente, armazenado em um campo texto livre sem estrutura.

**Destino no RF Moderno:** ✅ **SUBSTITUÍDO** por cálculo automático (RN-RF033-02)

**Justificativa:** Campo texto é propenso a erros humanos. Sistema moderno calcula SLA automaticamente considerando dias úteis e datas de parada.

**Impacto:** **ALTO** - Requer implementação de serviço de cálculo de SLA (`CalcularSLAService`).

---

### RL-RN-003: Status Sem Validação de Transições

**Fonte:** Campo `Fl_Status int` sem documentação ou validações

**Descrição:** O status do chamado era um campo int sem validação de transições válidas. Qualquer mudança era permitida.

**Destino no RF Moderno:** ✅ **SUBSTITUÍDO** por workflow controlado (RN-RF033-03)

**Justificativa:** Falta de controle causava inconsistências. Sistema moderno valida transições de estado.

**Impacto:** **MÉDIO** - Requer enum `ChamadoStatus` e validação de transições no validator.

---

### RL-RN-004: Notificações Manuais

**Fonte:** Campos `Id_Mail_Caixa_Saida_Usuario`, `Id_Mail_Caixa_Saida_Operadora`

**Descrição:** Notificações eram disparadas manualmente via atualização de campos que referenciam caixas de saída de e-mail.

**Destino no RF Moderno:** ✅ **SUBSTITUÍDO** por sistema de eventos de domínio (RN-RF033-10)

**Justificativa:** Sistema manual não escalável. Moderno utiliza Domain Events (`ChamadoCriadoDomainEvent`, etc) para disparo automático.

**Impacto:** **ALTO** - Requer implementação de MediatR Notifications e serviço de notificações.

---

### RL-RN-005: Interações Públicas vs Privadas

**Fonte:** Campo `Fl_Publicado int` na tabela `Solicitacao_Item`

**Descrição:** Interações marcadas como `Fl_Publicado = 1` são visíveis ao solicitante. `Fl_Publicado = 0` são privadas (apenas equipe).

**Destino no RF Moderno:** ✅ **ASSUMIDO** como RN-RF033-07

**Observações:** Mesma lógica mantida, porém com campo renomeado para `FlPublico` (bool).

---

### RL-RN-006: Avaliação Sem Validações

**Fonte:** Tabela `Solicitacao_Avaliacao` sem constraints

**Descrição:** Não havia validação de range de nota, unicidade ou permissão. Qualquer usuário poderia criar múltiplas avaliações com valores arbitrários.

**Destino no RF Moderno:** ✅ **SUBSTITUÍDO** por validações rigorosas (RN-RF033-06, RN-RF033-17)

**Justificativa:** Falta de validações causava métricas incorretas. Moderno valida range (1-5) e unicidade.

**Impacto:** **MÉDIO** - Requer validadores FluentValidation.

---

### RL-RN-007: Vinculação a Ativo e Consumidor Opcional

**Fonte:** Campos `Id_Consumidor_Unidade int NULL` e tabela `Rl_Solicitacao_Ativo`

**Descrição:** Chamados podiam ser vinculados a unidades de consumidor e ativos de forma opcional, sem validação de existência.

**Destino no RF Moderno:** ✅ **ASSUMIDO** com melhorias (RN-RF033-09)

**Observações:** Mesma lógica mantida, porém com validação de existência e pertencimento ao conglomerado.

---

### RL-RN-008: Fila de Atendimento Obrigatória

**Fonte:** Análise de dados históricos (não explícito no DDL)

**Descrição:** Todos os chamados eram atribuídos a uma fila de atendimento, embora não houvesse constraint no banco.

**Destino no RF Moderno:** ✅ **ASSUMIDO** com validação obrigatória (RN-RF033-08)

**Observações:** Moderno torna obrigatório via validador.

---

### RL-RN-009: Sem Controle de Reabertura

**Fonte:** Ausência de lógica no legado

**Descrição:** Não havia controle de reabertura de chamados encerrados. Usuários tinham que criar novo chamado.

**Destino no RF Moderno:** ✅ **NOVA FUNCIONALIDADE** (RN-RF033-11)

**Justificativa:** Melhorar experiência do usuário permitindo reabertura controlada (até 7 dias).

**Impacto:** **MÉDIO** - Requer comando `ReabrirChamadoCommand` com validação de prazo.

---

### RL-RN-010: SLA Não Pausava em Status "Aguardando"

**Fonte:** Análise de comportamento observado

**Descrição:** O SLA continuava contando mesmo quando chamado estava aguardando resposta de terceiros.

**Destino no RF Moderno:** ✅ **NOVA FUNCIONALIDADE** (RN-RF033-12)

**Justificativa:** Evitar penalização da equipe por atrasos de terceiros.

**Impacto:** **ALTO** - Requer campos `DataInicioAguardando`, `TotalHorasAguardando` e lógica de pausa/retomada.

---

### RL-RN-011: Sem Escalação Automática

**Fonte:** Ausência de lógica no legado

**Descrição:** Chamados vencidos não eram escalados automaticamente. Dependia de supervisão manual.

**Destino no RF Moderno:** ✅ **NOVA FUNCIONALIDADE** (RN-RF033-14)

**Justificativa:** Garantir atenção gerencial a chamados críticos.

**Impacto:** **ALTO** - Requer job recorrente `EscalarChamadosVencidosJob` e campos `FlEscalado`, `DataEscalacao`.

---

### RL-RN-012: Anexos Sem Controle de Tamanho

**Fonte:** Ausência de tabela específica (provavelmente armazenados em filesystem)

**Descrição:** Não havia controle de tamanho de anexos ou limite por chamado.

**Destino no RF Moderno:** ✅ **NOVA FUNCIONALIDADE** (RN-RF033-13)

**Justificativa:** Controlar espaço de armazenamento e prevenir uploads abusivos.

**Impacto:** **MÉDIO** - Requer entidade `ChamadoAnexo` e validação de tamanho.

---

### RL-RN-013: Base de Conhecimento Rudimentar

**Fonte:** Tabela `Solicitacao_Solucao` sem flag de reutilização

**Descrição:** Soluções eram cadastradas, mas não havia marcação para base de conhecimento ou sugestão de soluções similares.

**Destino no RF Moderno:** ✅ **MELHORADO** (RN-RF033-15)

**Justificativa:** Construir repositório de soluções para problemas recorrentes.

**Impacto:** **MÉDIO** - Requer campo `FlBaseConhecimento` e query de sugestão.

---

### RL-RN-014: Controle de Permissões Customizado

**Fonte:** Tabela `Solicitacao_Permissao`

**Descrição:** Sistema customizado de permissões não seguindo padrão RBAC.

**Destino no RF Moderno:** ✅ **SUBSTITUÍDO** por RBAC padrão (RN-RF033-16 + Seção 10.4)

**Justificativa:** Sistema customizado dificulta manutenção e integração.

**Impacto:** **ALTO** - Requer migração de permissões para sistema RBAC centralizado.

---

### RL-RN-015: Sem Isolamento Multi-Tenant

**Fonte:** Ausência de campo `Id_Conglomerado`

**Descrição:** Todos os dados eram compartilhados sem isolamento por conglomerado.

**Destino no RF Moderno:** ✅ **NOVA FUNCIONALIDADE CRÍTICA** (RN-RF033-16)

**Justificativa:** **OBRIGATÓRIO** para conformidade LGPD e segurança.

**Impacto:** **CRÍTICO** - Requer adição de `ConglomeradoId` em TODAS as entidades e Row-Level Security.

---

## 7. GAP ANALYSIS (LEGADO × RF MODERNO)

| Item | Existe no Legado | Existe no Moderno | Decisão |
|------|------------------|-------------------|---------|
| CRUD de Chamados | ✅ Sim | ✅ Sim | **ASSUMIDO com melhorias** |
| Cálculo Manual de SLA | ✅ Sim (texto livre) | ❌ Não | **SUBSTITUÍDO** por cálculo automático |
| Workflow de Status | ✅ Sim (sem validação) | ✅ Sim (validado) | **MELHORADO** |
| Interações Públicas/Privadas | ✅ Sim | ✅ Sim | **ASSUMIDO** |
| Avaliação de Satisfação | ✅ Sim (sem validação) | ✅ Sim (validado) | **MELHORADO** |
| Notificações | ✅ Sim (manual) | ✅ Sim (automático) | **SUBSTITUÍDO** |
| Multi-Tenancy | ❌ Não | ✅ Sim | **NOVA FUNCIONALIDADE** |
| Auditoria | ❌ Não | ✅ Sim (7 anos LGPD) | **NOVA FUNCIONALIDADE** |
| Soft Delete | ❌ Não | ✅ Sim | **NOVA FUNCIONALIDADE** |
| Reabertura Controlada | ❌ Não | ✅ Sim (até 7 dias) | **NOVA FUNCIONALIDADE** |
| Pausa de SLA | ❌ Não | ✅ Sim (status Aguardando) | **NOVA FUNCIONALIDADE** |
| Escalação Automática | ❌ Não | ✅ Sim (SLA vencido) | **NOVA FUNCIONALIDADE** |
| Controle de Anexos | ⚠️ Parcial | ✅ Sim (limite tamanho) | **MELHORADO** |
| Base de Conhecimento | ⚠️ Básica | ✅ Sim (com sugestões) | **MELHORADO** |
| RBAC Granular | ⚠️ Customizado | ✅ Sim (padrão) | **SUBSTITUÍDO** |
| Dashboard Tempo Real | ❌ Não | ✅ Sim (SignalR) | **NOVA FUNCIONALIDADE** |
| i18n (pt-BR, en-US, es-ES) | ❌ Não | ✅ Sim | **NOVA FUNCIONALIDADE** |

---

## 8. DECISÕES DE MODERNIZAÇÃO

### Decisão 1: Substituir Campo Texto por Cálculo Automático de SLA

**Motivo:** Campo `Excedente_SLA varchar(8000)` é propenso a erros humanos e inconsistências.

**Solução Moderna:** Serviço `CalcularSLAService` com lógica de dias úteis + datas de parada.

**Impacto:** **ALTO** - Requer desenvolvimento de serviço complexo e testes extensivos.

---

### Decisão 2: Migrar de `int IDENTITY` para `Guid`

**Motivo:** PKs inteiras dificultam distribuição e merge de dados. Guids são globalmente únicos.

**Solução Moderna:** Todas as entidades usam `Guid Id` como PK.

**Impacto:** **MÉDIO** - Requer migração de dados históricos.

---

### Decisão 3: Implementar Multi-Tenancy Obrigatório

**Motivo:** Conformidade LGPD e isolamento de dados por conglomerado.

**Solução Moderna:** Campo `ConglomeradoId` em todas as entidades + Row-Level Security.

**Impacto:** **CRÍTICO** - Requer migração de TODOS os dados históricos associando a conglomerado padrão.

---

### Decisão 4: Substituir Sistema de Permissões Customizado por RBAC

**Motivo:** Tabela `Solicitacao_Permissao` dificulta manutenção e não é padrão.

**Solução Moderna:** RBAC centralizado com matriz de permissões (Seção 10.4 do RF033).

**Impacto:** **ALTO** - Requer migração de permissões e atualização de perfis.

---

### Decisão 5: Implementar Auditoria Completa

**Motivo:** Conformidade LGPD (retenção 7 anos) e rastreabilidade.

**Solução Moderna:** Campos de auditoria em todas as entidades (`UsuarioCriacaoId`, `DataCriacao`, etc).

**Impacto:** **MÉDIO** - Requer AuditInterceptor do EF Core.

---

### Decisão 6: Adicionar Soft Delete

**Motivo:** Evitar perda de dados e permitir recuperação.

**Solução Moderna:** Campo `FlExcluido` + query filter global.

**Impacto:** **MÉDIO** - Requer configuração de Global Query Filter no EF Core.

---

### Decisão 7: Automatizar Notificações via Domain Events

**Motivo:** Sistema manual via `Id_Mail_Caixa_Saida_*` não escalável.

**Solução Moderna:** Domain Events (`ChamadoCriado`, `ChamadoAtribuido`, etc) com MediatR.

**Impacto:** **ALTO** - Requer implementação de todos os eventos e handlers.

---

### Decisão 8: Implementar Dashboard em Tempo Real

**Motivo:** Legado não possui métricas visuais.

**Solução Moderna:** Dashboard Angular com SignalR para atualização em tempo real.

**Impacto:** **ALTO** - Requer desenvolvimento frontend completo + integração SignalR.

---

## 9. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| **Perda de Dados Históricos** | 🔴 Alto | 🟡 Média | Backup completo antes da migração + script de validação pós-migração |
| **Incompatibilidade de Status Legados** | 🟡 Médio | 🟢 Baixa | Criar mapeamento `Fl_Status (int)` → `ChamadoStatus (enum)` |
| **Quebra de Integrações Externas** | 🟡 Médio | 🟢 Baixa | Manter endpoints legados em modo read-only durante transição |
| **Resistência dos Usuários** | 🟢 Baixo | 🟡 Média | Treinamento + período de convivência (legacy + moderno) |
| **Performance do Cálculo de SLA** | 🟡 Médio | 🟡 Média | Cache de datas de parada + índices otimizados |
| **Falhas em Jobs Recorrentes** | 🟡 Médio | 🟡 Média | Hangfire com retry policy + alertas de falha |
| **Migração de Permissões Incorreta** | 🔴 Alto | 🟡 Média | Matriz de validação + testes de acesso por perfil |
| **Inconsistência Multi-Tenancy** | 🔴 Alto | 🟢 Baixa | Validação em 100% das queries + testes de isolamento |

---

## 10. RASTREABILIDADE (LEGADO → MODERNO)

| Elemento Legado | Referência RF Moderno | Referência UC | Status |
|-----------------|------------------------|---------------|--------|
| Tabela `Solicitacao` | RN-RF033-01 a RN-RF033-17 | UC00-UC04 | ✅ Migrado |
| Tabela `Solicitacao_Item` | RN-RF033-07 | UC02, UC03 | ✅ Migrado |
| Tabela `Solicitacao_Avaliacao` | RN-RF033-06, RN-RF033-17 | UC04 | ✅ Migrado |
| Campo `Excedente_SLA` | RN-RF033-02 | UC01, UC02 | ✅ Substituído |
| Campo `Fl_Status` | RN-RF033-03 | UC00-UC04 | ✅ Substituído |
| Campos `Id_Mail_Caixa_Saida_*` | RN-RF033-10 | UC01, UC03, UC04 | ✅ Substituído |
| Campo `Fl_Publicado` | RN-RF033-07 | UC02, UC03 | ✅ Assumido |
| Tabela `Solicitacao_Permissao` | Seção 10.4 do RF033 | - | ✅ Substituído por RBAC |
| Tabela `Solicitacao_Tipo` | RN-RF033-02 | UC01 | ✅ Migrado |
| Tabela `Solicitacao_SLA` | RN-RF033-02 | UC01 | ✅ Migrado |
| Tabela `Solicitacao_Fila_Atendimento` | RN-RF033-08 | UC01, UC03 | ✅ Migrado |
| Tabela `Solicitacao_Solucao` | RN-RF033-04, RN-RF033-15 | UC04 | ✅ Melhorado |
| Tabela `Solicitacao_Data_Parada` | RN-RF033-02 | UC01 | ✅ Migrado |
| Tabela `Rl_Solicitacao_Ativo` | RN-RF033-09 | UC01, UC02 | ✅ Substituído (relacionamento direto) |

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|--------|------|-----------|-------|
| 1.0 | 2025-12-30 | Documentação completa de referência ao legado (Gestão de Chamados). Extração de 15 regras implícitas, análise de 9 tabelas legadas, gap analysis completo e mapeamento de decisões de modernização. Todas as referências ASPX, VB.NET e SQL Server migradas do RF033.md v1.0. | Agência ALC - alc.dev.br |
