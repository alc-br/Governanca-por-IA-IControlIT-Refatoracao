# RL-RF090 — Referência ao Legado

**Versão:** 1.0
**Data:** 2025-12-31
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF-090
**Sistema Legado:** VB.NET + ASP.NET Web Forms (IControlIT v1)
**Objetivo:** Documentar o comportamento do legado que serve de base para a refatoração, garantindo rastreabilidade, entendimento histórico e mitigação de riscos.

---

## 1. CONTEXTO DO LEGADO

Descreve o cenário geral do sistema legado.

- **Arquitetura:** Monolítica WebForms (Server-Side Rendering)
- **Linguagem / Stack:** VB.NET + ASP.NET Web Forms 4.7
- **Banco de Dados:** SQL Server 2012+
- **Multi-tenant:** Não (sem isolamento por ClienteId, controle manual)
- **Auditoria:** Parcial (logs em arquivos texto, sem estrutura JSON, sem hash)
- **Configurações:** Web.config (connection strings, appSettings)

**Características do Sistema Legado:**

- Cálculos de medição e fatura realizados manualmente ou via stored procedures executadas ad-hoc
- Reajustes aplicados manualmente por DBA com UPDATE direto em tabelas
- Rateio registrado em tabela separada sem validação de soma = 100%
- Workflow de aprovação inexistente (qualquer usuário podia alterar medições)
- Glosas registradas em tabela simples sem auditoria de análise/decisão
- Integração com geração de fatura manual (link feito via planilha)

---

## 2. TELAS DO LEGADO

### Tela: MedicaoLista.aspx

- **Caminho:** `ic1_legado/IControlIT/Financeiro/Medicao/MedicaoLista.aspx`
- **Responsabilidade:** Listar medições existentes com filtros por período e contrato

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|------|------|-------------|-------------|
| `ddlContrato` | DropDownList | Sim | Combo de contratos ativos |
| `txtDataInicio` | TextBox (Date) | Não | Filtro por data início |
| `txtDataFim` | TextBox (Date) | Não | Filtro por data fim |
| `gvMedicoes` | GridView | - | Lista de medições com paginação server-side |

#### Comportamentos Implícitos

- Sem validação de permissão (qualquer usuário logado podia listar todas medições)
- Sem isolamento por ClienteId (misturava dados de clientes diferentes)
- Paginação server-side (postback completo a cada navegação)
- Sem ordenação dinâmica por colunas
- Sem exportação para Excel/PDF

---

### Tela: MedicaoDetalhe.aspx

- **Caminho:** `ic1_legado/IControlIT/Financeiro/Medicao/MedicaoDetalhe.aspx`
- **Responsabilidade:** Criar ou editar medição com cálculo manual de valor

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|------|------|-------------|-------------|
| `ddlContrato` | DropDownList | Sim | FK para Contrato |
| `txtDataInicio` | TextBox (Date) | Sim | Data início período |
| `txtDataFim` | TextBox (Date) | Sim | Data fim período |
| `txtValor` | TextBox (Decimal) | Sim | Valor total (calculado manualmente pelo usuário) |
| `txtObservacoes` | TextBox (MultiLine) | Não | Observações livres |
| `btnSalvar` | Button | - | Persiste medição sem validações |

#### Comportamentos Implícitos

- **Sem validação de sobreposição:** Permitia criar medições com períodos duplicados
- **Sem validação de vigência:** Permitia criar medição fora da vigência do contrato
- **Cálculo manual:** Usuário calculava valor manualmente (alto risco de erro)
- **Sem tipo de medição:** Não diferenciava Fixa/Variável/Híbrida
- **Sem rateio automático:** Rateio feito em tela separada (TabelaRateio.aspx) manualmente
- **Sem reajuste automático:** Reajuste aplicado via UPDATE SQL manual por DBA

---

### Tela: RelatorioFaturamento.aspx

- **Caminho:** `ic1_legado/IControlIT/Financeiro/Medicao/RelatorioFaturamento.aspx`
- **Responsabilidade:** Relatório de faturamento por período com exportação

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|------|------|-------------|-------------|
| `txtPeriodoInicio` | TextBox (Date) | Sim | Período início |
| `txtPeriodoFim` | TextBox (Date) | Sim | Período fim |
| `ddlFornecedor` | DropDownList | Não | Filtro opcional por fornecedor |
| `btnGerar` | Button | - | Gera relatório em GridView |
| `btnExportar` | Button | - | Exporta para Excel (Response.Write com ContentType) |

#### Comportamentos Implícitos

- Relatório gerado via stored procedure `pa_RelatorioFaturamento`
- Exportação para Excel usando HTML table (não XLS real)
- Sem agrupamento dinâmico (sempre agrupado por contrato)
- Sem dashboard visual (somente tabela)

---

### Tela: GlosaAnaliseLista.aspx

- **Caminho:** `ic1_legado/IControlIT/Financeiro/Medicao/GlosaAnaliseLista.aspx`
- **Responsabilidade:** Listar glosas registradas para análise

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|------|------|-------------|-------------|
| `gvGlosas` | GridView | - | Lista de glosas com status Pendente/Aprovada/Rejeitada |
| `btnAprovar` | Button | - | Aprova glosa (UPDATE direto) |
| `btnRejeitar` | Button | - | Rejeita glosa (UPDATE direto) |

#### Comportamentos Implícitos

- Sem workflow formal (botões executam UPDATE direto)
- Sem auditoria de quem aprovou/rejeitou
- Sem geração automática de nota fiscal de crédito (feito manualmente no RF032)
- Sem integração com medição (link manual via MedicaoId)

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

| Método | Local | Responsabilidade | Observações |
|------|-------|------------------|-------------|
| `ObterMedicoes()` | `WSMedicao.asmx.vb` | Retorna lista de medições por contrato | Sem paginação, retorna todas (risco de timeout) |
| `CriarMedicao()` | `WSMedicao.asmx.vb` | Cria nova medição | Sem validações de período/vigência |
| `AtualizarMedicao()` | `WSMedicao.asmx.vb` | Atualiza medição existente | Permite atualizar qualquer campo sem controle de estado |
| `CalcularFatura()` | `WSMedicao.asmx.vb` | Calcula valor de fatura (chama stored procedure) | Execução síncrona, pode travar em volumes altos |
| `AplicarReajuste()` | `WSMedicao.asmx.vb` | Aplica reajuste manualmente (admin) | UPDATE direto sem histórico |

---

## 4. TABELAS LEGADAS

| Tabela | Finalidade | Problemas Identificados |
|-------|------------|-------------------------|
| `Medicao` | Registro principal de medições | Sem multi-tenancy (Id_Cliente sem filtro automático), sem soft delete, sem tipo de medição |
| `Rateio_Medicao` | Rateio entre centros de custo | Sem validação soma=100%, permite percentuais negativos, sem auditoria |
| `Glosa` | Contestações de fatura | Flag simples Aprovada (bit), sem workflow, sem auditoria de decisão |
| `HistoricoReajuste` | Não existia | Reajustes aplicados via UPDATE direto, sem histórico rastreável |

**DDL Legado Simplificado:**

```sql
-- Tabela Medicao (legado)
CREATE TABLE [dbo].[Medicao](
    [Id_Medicao] [int] IDENTITY(1,1) NOT NULL,
    [Id_Contrato] [int] NOT NULL,
    [Id_Cliente] [int] NOT NULL,
    [Dt_Inicio_Medicao] [datetime] NOT NULL,
    [Dt_Fim_Medicao] [datetime] NOT NULL,
    [Vl_Medicao] [numeric](13, 2) NOT NULL,
    [Vl_Reajuste] [numeric](13, 2) NULL,
    [Fl_Rateado] [bit] NOT NULL DEFAULT 0,
    [Id_Usuario_Criacao] [int] NOT NULL,
    [Dt_Criacao] [datetime] NOT NULL,
    [Id_Usuario_Atualizacao] [int] NULL,
    [Dt_Atualizacao] [datetime] NULL,
    CONSTRAINT [PK_Medicao] PRIMARY KEY CLUSTERED ([Id_Medicao] ASC)
)

-- Tabela Rateio_Medicao (legado)
CREATE TABLE [dbo].[Rateio_Medicao](
    [Id_Rateio] [int] IDENTITY(1,1) NOT NULL,
    [Id_Medicao] [int] NOT NULL,
    [Id_Centro_Custo] [int] NOT NULL,
    [Percentual_Rateio] [numeric](5, 2) NOT NULL,
    [Vl_Rateado] [numeric](13, 2) NOT NULL,
    CONSTRAINT [PK_Rateio_Medicao] PRIMARY KEY CLUSTERED ([Id_Rateio] ASC)
)

-- Tabela Glosa (legado)
CREATE TABLE [dbo].[Glosa](
    [Id_Glosa] [int] IDENTITY(1,1) NOT NULL,
    [Id_Medicao] [int] NOT NULL,
    [Percentual_Glosa] [numeric](5, 2) NOT NULL,
    [Vl_Glosa] [numeric](13, 2) NOT NULL,
    [Ds_Justificativa] [varchar](500) NOT NULL,
    [Fl_Aprovada] [bit] NOT NULL DEFAULT 0,
    [Dt_Aprovacao] [datetime] NULL,
    CONSTRAINT [PK_Glosa] PRIMARY KEY CLUSTERED ([Id_Glosa] ASC)
)
```

---

## 5. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

Liste regras que não estavam documentadas formalmente.

- **RL-RN-001:** Cálculo de valor de medição era manual, usuário digitava valor sem validação (alto risco de erro)
- **RL-RN-002:** Reajustes aplicados manualmente por DBA via UPDATE SQL (sem histórico, sem auditoria)
- **RL-RN-003:** Rateio permitia soma de percentuais ≠ 100% (validação ausente)
- **RL-RN-004:** Workflow de aprovação inexistente (qualquer usuário podia alterar medições já faturadas)
- **RL-RN-005:** Glosas aprovadas não geravam nota fiscal de crédito automaticamente (processo manual no RF032)
- **RL-RN-006:** Períodos de medição podiam sobrepor (sem validação de sobreposição)
- **RL-RN-007:** Medições fora da vigência do contrato eram aceitas (sem validação)
- **RL-RN-008:** Integração com geração de fatura era manual (planilha Excel intermediária)
- **RL-RN-009:** Multi-tenancy não garantido (Id_Cliente presente mas sem query filter automático)
- **RL-RN-010:** Auditoria limitada a logs textuais (sem JSON, sem hash, sem retenção garantida 7 anos)

---

## 6. GAP ANALYSIS (LEGADO x RF MODERNO)

| Item | Legado | RF Moderno | Observação |
|-----|--------|------------|------------|
| **Tipo de Medição** | Não existia (campo único Vl_Medicao) | Fixa/Variável/Híbrida com cálculo automático | Nova funcionalidade |
| **Validação de Período** | Ausente (permitia sobreposição) | RN-RF090-001 + RN-RF090-002 (sem sobreposição, sem gaps) | Melhoria crítica |
| **Workflow de Aprovação** | Inexistente | State machine Rascunho→Pendente→Aprovada→Faturada→Glosa | Nova funcionalidade |
| **Reajuste Automático** | Manual (DBA via UPDATE SQL) | Job automático com IGPM/IPCA/INPC, histórico completo | Automação |
| **Rateio Validado** | Permitia soma ≠ 100% | RN-RF090-005 (soma exatamente 100%, tolerância 0,01%) | Melhoria crítica |
| **Geração de Fatura** | Manual (planilha intermediária) | Automática via job Hangfire + integração RF032 | Automação |
| **Glosa com Workflow** | Flag simples (bit) | Workflow PendenteAnalise→Aprovada/Rejeitada com auditoria | Melhoria crítica |
| **Multi-tenancy** | Não garantido (Id_Cliente presente mas sem filtro) | Row-level isolation automático (ClienteId) | Melhoria crítica |
| **Auditoria** | Logs textuais (parcial) | Tabela estruturada JSON + hash SHA-256 + retenção 7 anos | Melhoria crítica |
| **Soft Delete** | DELETE físico | Fl_Excluido=true (preservação histórico) | Melhoria crítica |

---

## 7. DECISÕES DE MODERNIZAÇÃO

Explique decisões tomadas durante a refatoração.

### Decisão 1: Introduzir Tipos de Medição (Fixa, Variável, Híbrida)

- **Motivo:** Legado tinha campo único `Vl_Medicao` (calculado manualmente pelo usuário). Tipos permitem cálculos automáticos, eliminam erros manuais e facilitam auditoria.
- **Impacto:** Alto (mudança arquitetural significativa, mas necessária)

### Decisão 2: Implementar State Machine de Aprovação

- **Motivo:** Legado permitia qualquer usuário alterar medições já faturadas (risco de fraude). State machine garante segregação de funções (medidor ≠ aprovador ≠ financeiro).
- **Impacto:** Alto (introduz controle de qualidade e rastreabilidade completa)

### Decisão 3: Automatizar Reajustes com Job Hangfire

- **Motivo:** Legado aplicava reajustes manualmente via UPDATE SQL por DBA (sem histórico, sem auditoria, alto risco de erro). Job automático elimina erros, garante conformidade com índices oficiais.
- **Impacto:** Médio (introduz dependência de Hangfire, mas valor justifica)

### Decisão 4: Validar Rateio com Soma = 100%

- **Motivo:** Legado permitia rateios desequilibrados (ex: 60% + 30% = 90%). Validação garante distribuição correta de custos.
- **Impacto:** Baixo (validação simples, alto valor)

### Decisão 5: Geração Automática de Faturas via Job

- **Motivo:** Legado exigia processo manual com planilha Excel intermediária. Job automático elimina delay, garante consistência entre medição e fatura.
- **Impacto:** Médio (introduz integração com RF032 via job, mas automação justifica)

### Decisão 6: Workflow de Glosa com Análise e Decisão

- **Motivo:** Legado tinha flag simples `Fl_Aprovada` (bit) sem auditoria de quem/quando aprovou. Workflow garante transparência, rastreabilidade e compliance.
- **Impacto:** Médio (introduz complexidade, mas necessária para governança)

### Decisão 7: Multi-tenancy Row-Level Automático

- **Motivo:** Legado tinha `Id_Cliente` mas sem filtro automático (risco de vazamento de dados). Query filter automático garante isolamento 100%.
- **Impacto:** Alto (mudança arquitetural crítica para segurança)

### Decisão 8: Auditoria Imutável com Hash SHA-256

- **Motivo:** Legado tinha logs textuais sem estrutura (impossível auditar alterações pós-fato). Tabela estruturada com hash detecta alterações, garante conformidade LGPD.
- **Impacto:** Médio (introduz overhead de storage, mas conformidade regulatória exige)

---

## 8. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Mitigação |
|------|---------|-----------|
| **Dados legados sem tipo de medição** | Alto | Script de migração infere tipo baseado em campos preenchidos (se Vl_Medicao único → Fixa, se existir quantidade → Variável) |
| **Medições com períodos sobrepostos no legado** | Médio | Script de validação identifica sobreposições, marca para revisão manual |
| **Rateios com soma ≠ 100% no legado** | Médio | Script normaliza percentuais proporcionalmente ou marca para revisão |
| **Medições faturadas sem link para NotaFiscalId** | Alto | Script tenta vincular via período + contrato, casos não vinculados marcados para revisão manual |
| **Glosas com Fl_Aprovada mas sem Dt_Aprovacao** | Baixo | Script assume data de criação da glosa, adiciona observação na auditoria |
| **Auditoria legado em logs textuais** | Médio | Script extrai logs e importa para tabela estruturada (best-effort), gaps documentados |
| **Reajustes aplicados manualmente sem histórico** | Alto | Impossível reconstruir histórico completo; documentar valores atuais como baseline |

---

## 9. RASTREABILIDADE

| Elemento Legado | Referência RF |
|----------------|---------------|
| `Medicao.Vl_Medicao` | RN-RF090-003 (cálculo automático por tipo) |
| `Medicao.Dt_Inicio_Medicao` + `Dt_Fim_Medicao` | RN-RF090-001 + RN-RF090-002 (validação período) |
| `Rateio_Medicao.Percentual_Rateio` | RN-RF090-005 (soma = 100%) |
| `Glosa.Fl_Aprovada` | RN-RF090-009 (workflow com análise) |
| `pa_CalcularFatura_Contrato` | RN-RF090-008 (job automático Hangfire) |
| `pa_AplicarReajuste` | RN-RF090-004 (reajuste automático com índices) |
| `MedicaoLista.aspx` | UC00-Listar Medições (Angular SPA) |
| `MedicaoDetalhe.aspx` | UC01-Criar Medição + UC02-Visualizar (Angular SPA) |
| `GlosaAnaliseLista.aspx` | UC04-Gerenciar Glosa (Angular SPA) |
| `WSMedicao.asmx.vb` | API REST Minimal APIs (.NET 10) |

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|------|------|----------|------|
| 1.0 | 2025-12-31 | Criação da referência ao legado (separação RF/RL v2.0) | Agência ALC - alc.dev.br |
