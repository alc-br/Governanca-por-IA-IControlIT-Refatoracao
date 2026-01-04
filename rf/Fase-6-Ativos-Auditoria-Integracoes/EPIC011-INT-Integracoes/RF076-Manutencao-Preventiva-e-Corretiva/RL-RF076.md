# RL-RF076 — Referência ao Legado: Manutenção Preventiva e Corretiva

**Versão:** 2.0
**Data:** 2025-12-30
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF076 - Manutenção Preventiva e Corretiva
**Sistema Legado:** VB.NET + ASP.NET Web Forms
**Objetivo:** Documentar o comportamento do legado relacionado a manutenção de ativos, garantindo rastreabilidade e compreensão histórica para a refatoração.

---

## 1. CONTEXTO DO LEGADO

### Arquitetura
- **Tipo:** Monolítica Web Forms
- **Linguagem:** VB.NET / ASP.NET
- **Banco de Dados:** SQL Server (`IControlIT_Legado`)
- **Multi-tenant:** Não implementado (dados misturados por cliente sem isolamento efetivo)
- **Auditoria:** Parcial (apenas campos `Id_Usuario_Criacao`, `Dt_Criacao` sem histórico)
- **Configurações:** Web.config + tabelas de sistema

### Características Técnicas
- Formulários ASPX estáticos com ViewState pesado
- WebServices ASMX para operações CRUD
- Stored Procedures para lógica de negócio
- Sem agendamento automático (manutenções criadas manualmente)
- Sem workflow estruturado (aprovação informal por email)
- Cálculos de MTBF/MTTR manuais em Excel

---

## 2. TELAS DO LEGADO

### 2.1 Gestão de Ordens de Manutenção

**TELA NÃO ENCONTRADA** - Sistema legado não possui tela específica de ordens de manutenção como módulo isolado.

**Evidência:** Busca por `ordem*.aspx`, `manutencao*.aspx`, `servico*.aspx` retornou 0 resultados.

**Destino:** `descartado`

**Justificativa:** A funcionalidade de manutenção preventiva/corretiva será criada do zero no sistema modernizado, baseada em requisitos de negócio atuais e boas práticas de engenharia de manutenção (ISO 55000).

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

Não foram encontrados WebServices específicos para manutenção no sistema legado.

**Destino:** `descartado`

**Justificativa:** Implementação será baseada em Clean Architecture + CQRS, sem dependência de métodos legados.

---

## 4. TABELAS LEGADAS

### 4.1 Tabela `OrdemManutencao`

**Estrutura:**
```sql
CREATE TABLE [dbo].[OrdemManutencao](
    [Id_Ordem] [int] IDENTITY(1,1) NOT NULL,
    [Id_Ativo] [int] NOT NULL,
    [Nu_Ordem] [varchar](30) NOT NULL,
    [Ds_Tipo] [varchar](50), -- 'Preventiva', 'Corretiva'
    [Ds_Status] [varchar](50),
    [Dt_Solicitacao] [datetime] NOT NULL,
    [Dt_Prevista] [datetime],
    [Dt_Execucao] [datetime],
    [Dt_Fechamento] [datetime],
    [Nu_Horas] [numeric](10,2),
    [Vl_Total] [numeric](15,2),
    [Id_Usuario_Criacao] [int],
    [Dt_Criacao] [datetime],
    CONSTRAINT [PK_OrdemManutencao] PRIMARY KEY ([Id_Ordem])
);
```

**Problemas Identificados:**
- Sem campo `Id_Conglomerado` (não multi-tenant)
- Sem soft delete (`Fl_Excluido`)
- Sem campos de auditoria completos (falta `Id_Usuario_Alteracao`, `Dt_Alteracao`)
- Status textual sem enum (permite valores inconsistentes)
- Sem FK para responsável/técnico
- Sem FK para aprovador
- Sem campo de descrição/observações

**Destino:** `substituido`

**Justificativa:** Será criada nova tabela `OrdemServico` com:
- Multi-tenancy (`Id_Conglomerado`)
- Auditoria completa
- Soft delete
- Status enum estruturado
- FKs para responsável, técnico, aprovador
- Campo texto para descrição

**Mapeamento de Campos:**

| Campo Legado | Campo Moderno | Observação |
|--------------|---------------|------------|
| `Id_Ordem` | `Id` | GUID em vez de INT |
| `Id_Ativo` | `IdAtivo` | FK mantida |
| `Nu_Ordem` | `NumeroOrdem` | Mantido |
| `Ds_Tipo` | `Tipo` (enum) | Preventiva/Corretiva |
| `Ds_Status` | `Status` (enum) | Agendada/Aprovada/EmExecucao/Concluida/Fechada |
| `Dt_Solicitacao` | `DataCriacao` | Auditoria |
| `Dt_Prevista` | `DataPrevista` | Mantido |
| `Dt_Execucao` | `DataInicio` | Renomeado para clareza |
| `Dt_Fechamento` | `DataFechamento` | Mantido |
| `Nu_Horas` | `HorasExecutadas` | Renomeado |
| `Vl_Total` | `CustoTotal` | Calculado (não armazenado) |
| - | `Id_Conglomerado` | NOVO (multi-tenancy) |
| - | `Fl_Excluido` | NOVO (soft delete) |
| - | `IdResponsavel` | NOVO (FK Usuario) |
| - | `IdTecnico` | NOVO (FK Usuario) |
| - | `IdAprovador` | NOVO (FK Usuario) |
| - | `Descricao` | NOVO |

---

### 4.2 Tabela `OrdemManutencaoItem`

**Estrutura:**
```sql
CREATE TABLE [dbo].[OrdemManutencaoItem](
    [Id_Item] [int] IDENTITY(1,1) NOT NULL,
    [Id_Ordem] [int] NOT NULL,
    [Id_Peca] [int],
    [Ds_Item] [varchar](200),
    [Qt_Quantidade] [int],
    [Vl_Unitario] [numeric](15,2),
    [Vl_Total] [numeric](15,2),
    CONSTRAINT [PK_OrdemManutencaoItem] PRIMARY KEY ([Id_Item]),
    CONSTRAINT [FK_Item_Ordem] FOREIGN KEY ([Id_Ordem]) REFERENCES [OrdemManutencao]([Id_Ordem])
);
```

**Problemas Identificados:**
- Sem auditoria
- `Vl_Total` redundante (deveria ser calculado)
- Sem campo para unidade de medida

**Destino:** `substituido`

**Justificativa:** Será criada nova tabela `OrdemServicoItem` com auditoria e campos adicionais.

**Mapeamento de Campos:**

| Campo Legado | Campo Moderno | Observação |
|--------------|---------------|------------|
| `Id_Item` | `Id` | GUID |
| `Id_Ordem` | `IdOrdem` | FK mantida |
| `Id_Peca` | `IdPeca` | FK opcional |
| `Ds_Item` | `Descricao` | Mantido |
| `Qt_Quantidade` | `Quantidade` | Mantido |
| `Vl_Unitario` | `CustoUnitario` | Mantido |
| `Vl_Total` | - | REMOVIDO (calculado) |
| - | `UnidadeMedida` | NOVO |
| - | `Id_Usuario_Criacao` | NOVO (auditoria) |
| - | `Dt_Criacao` | NOVO (auditoria) |

---

### 4.3 Tabela `PlanoManutencao`

**Estrutura:**
```sql
CREATE TABLE [dbo].[PlanoManutencao](
    [Id_Plano] [int] IDENTITY(1,1) NOT NULL,
    [Id_Ativo] [int] NOT NULL,
    [Ds_Plano] [varchar](100),
    [Nu_Intervalo_Dias] [int],
    [Fl_Ativo] [bit],
    [Dt_Proxima] [datetime],
    CONSTRAINT [PK_PlanoManutencao] PRIMARY KEY ([Id_Plano]),
    CONSTRAINT [FK_Plano_Ativo] FOREIGN KEY ([Id_Ativo]) REFERENCES [Ativo]([Id_Ativo])
);
```

**Problemas Identificados:**
- Apenas periodicidade por dias (sem suporte para horas ou km)
- Sem checklist de atividades
- Sem campos de auditoria
- Sem multi-tenancy
- Sem campo para tipo de periodicidade

**Destino:** `substituido`

**Justificativa:** Será criada nova tabela `PlanoManutencao` com periodicidade flexível e checklist.

**Mapeamento de Campos:**

| Campo Legado | Campo Moderno | Observação |
|--------------|---------------|------------|
| `Id_Plano` | `Id` | GUID |
| `Id_Ativo` | `IdAtivo` | FK mantida |
| `Ds_Plano` | `NomePlano` | Renomeado |
| `Nu_Intervalo_Dias` | `IntervaloDias` | Mantido |
| - | `IntervaloHoras` | NOVO |
| - | `IntervaloKm` | NOVO |
| - | `TipoPeriodicidade` (enum) | NOVO |
| `Fl_Ativo` | `Ativo` | Mantido |
| `Dt_Proxima` | `DataProximaManutencao` | Mantido |
| - | `Checklist` (JSON ou tabela separada) | NOVO |
| - | `Id_Conglomerado` | NOVO (multi-tenancy) |
| - | `Id_Usuario_Criacao` | NOVO (auditoria) |
| - | `Dt_Criacao` | NOVO (auditoria) |
| - | `Fl_Excluido` | NOVO (soft delete) |

---

## 5. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

### RL-RN-001: Status textual sem validação

**Descrição:** O campo `Ds_Status` aceita qualquer texto, permitindo valores inconsistentes como "Agendado", "agendada", "AGENDADA".

**Fonte:** Tabela `OrdemManutencao`, campo `Ds_Status VARCHAR(50)`

**Destino:** `substituido`

**Justificativa:** No sistema modernizado, será usado enum `StatusOrdem` com valores fixos (Agendada, Aprovada, Rejeitada, EmExecucao, Concluida, Fechada).

---

### RL-RN-002: Cálculo manual de custo total

**Descrição:** O campo `Vl_Total` em `OrdemManutencao` é preenchido manualmente, não sincronizado com soma de itens.

**Fonte:** Tabela `OrdemManutencao`, campo `Vl_Total`

**Destino:** `substituido`

**Justificativa:** No sistema modernizado, `CustoTotal` será propriedade calculada automaticamente a partir de `OrdemServicoItem`.

---

### RL-RN-003: Sem workflow de aprovação

**Descrição:** Não há registro de quem aprovou a ordem, quando foi aprovada ou se foi rejeitada. Aprovação era informal (email).

**Fonte:** Ausência de campos `Id_Aprovador`, `Dt_Aprovacao`, `Status_Aprovacao`

**Destino:** `substituido`

**Justificativa:** No sistema modernizado, workflow estruturado com transições de estado auditadas (Agendada → Aprovada/Rejeitada).

---

### RL-RN-004: Sem integração com status de ativo

**Descrição:** Quando ordem entra em execução, status do ativo não é atualizado automaticamente.

**Fonte:** Código VB.NET (ausência de trigger ou lógica de integração)

**Destino:** `substituido`

**Justificativa:** No sistema modernizado, eventos de domínio atualizam status do ativo (RN-RF076-08).

---

### RL-RN-005: MTBF/MTTR calculados manualmente em Excel

**Descrição:** Não há cálculo automático de indicadores. Dados são exportados para Excel e calculados manualmente.

**Fonte:** Relatórios VB.NET (exportação de dados brutos)

**Destino:** `substituido`

**Justificativa:** No sistema modernizado, cálculo automático (RN-RF076-05, RN-RF076-06).

---

## 6. GAP ANALYSIS (LEGADO x RF MODERNO)

| Item | Existe no Legado | Existe no RF076 | Destino | Observação |
|------|------------------|-----------------|---------|------------|
| Criação de ordem manual | Sim | Sim | assumido | Funcionalidade mantida |
| Plano de manutenção | Sim (básico) | Sim (completo) | substituido | Expandido com checklist e periodicidade flexível |
| Agendamento automático | Não | Sim | substituido | Hangfire para recorrência |
| Workflow de aprovação | Não | Sim | substituido | Estados estruturados |
| Registro de peças | Sim | Sim | assumido | Mantido com melhorias (unidade, auditoria) |
| Cálculo MTBF/MTTR | Não (manual) | Sim (automático) | substituido | Cálculo em tempo real |
| Alertas de vencimento | Não | Sim | substituido | Verificação diária automática |
| Multi-tenancy | Não | Sim | substituido | Isolamento obrigatório |
| Auditoria completa | Não | Sim | substituido | Antes/depois de todas operações |
| Integração com RF028 | Não | Sim | substituido | Status de ativo sincronizado |
| Relatórios de custo | Sim (básico) | Sim (detalhado) | substituido | Quebra por período, ativo, tipo |
| Soft delete | Não | Sim | substituido | `Fl_Excluido` obrigatório |

---

## 7. DECISÕES DE MODERNIZAÇÃO

### Decisão 1: Não migrar dados históricos de ordens antigas

**Motivo:** Tabelas legadas sem multi-tenancy e auditoria completa tornam migração arriscada. Dados históricos serão mantidos no legado apenas para consulta.

**Impacto:** Alto

**Mitigação:** Criar view somente leitura no legado para consulta histórica se necessário.

---

### Decisão 2: Implementar agendamento com Hangfire

**Motivo:** Sistema legado não possui agendamento automático. Hangfire é padrão moderno para jobs recorrentes.

**Impacto:** Alto (nova funcionalidade crítica)

**Mitigação:** Testes extensivos de agendamento, monitoramento de jobs falhados.

---

### Decisão 3: Workflow estruturado com eventos de domínio

**Motivo:** Legado não possui workflow formal. Modernizado precisa rastreabilidade e compliance.

**Impacto:** Alto

**Mitigação:** Documentar transições permitidas, validar em testes.

---

### Decisão 4: Cálculos de MTBF/MTTR automáticos

**Motivo:** Processo manual do legado é propenso a erros e demorado.

**Impacto:** Médio

**Mitigação:** Validar fórmulas com equipe de manutenção, comparar com resultados Excel.

---

## 8. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| Perda de dados históricos se migração falhar | Alto | Baixa | Manter legado como backup, migração incremental |
| Jobs Hangfire não executarem após deploy | Alto | Média | Testes de agendamento em HOM, monitoramento |
| Usuários não compreenderem novo workflow | Médio | Alta | Treinamento, documentação, tour guiado |
| Fórmulas MTBF/MTTR incorretas | Médio | Média | Validação com equipe técnica, testes com dados reais |
| Performance de cálculos em tempo real | Médio | Baixa | Índices otimizados, cache de resultados |

---

## 9. RASTREABILIDADE

| Elemento Legado | Referência RF | Status |
|-----------------|---------------|--------|
| Tabela `OrdemManutencao` | RN-RF076-03, RN-RF076-08 | substituido |
| Tabela `OrdemManutencaoItem` | RN-RF076-04 | substituido |
| Tabela `PlanoManutencao` | RN-RF076-01, RN-RF076-02 | substituido |
| Cálculo manual MTBF/MTTR | RN-RF076-05, RN-RF076-06 | substituido |
| Sem workflow de aprovação | RN-RF076-03, RN-RF076-09 | substituido |
| Sem alertas automáticos | RN-RF076-07 | substituido |
| Sem integração com ativo | RN-RF076-08 | substituido |

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|--------|------|-----------|-------|
| 2.0 | 2025-12-30 | Adequação para governança v2.0: campo destino obrigatório, rastreabilidade completa | Agência ALC - alc.dev.br |
| 1.0 | 2025-12-28 | Documentação inicial do legado | Claude Architect |

---

**Última Atualização:** 2025-12-30
**Status:** Completo (100% itens com destino explícito)
