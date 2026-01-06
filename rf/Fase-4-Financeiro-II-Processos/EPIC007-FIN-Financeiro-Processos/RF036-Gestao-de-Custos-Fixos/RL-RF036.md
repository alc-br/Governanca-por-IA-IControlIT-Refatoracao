# RL-RF036 — Referência ao Legado - Gestão de Custos Fixos

**Versão:** 1.0
**Data:** 2025-12-30
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF036 - Gestão de Custos Fixos
**Sistema Legado:** ASP.NET Web Forms + VB.NET
**Objetivo:** Documentar o comportamento do legado que serve de base para a refatoração, garantindo rastreabilidade, entendimento histórico e mitigação de riscos.

---

## 1. CONTEXTO DO SISTEMA LEGADO

### Arquitetura Geral

- **Arquitetura:** Monolítica WebForms
- **Linguagem / Stack:** VB.NET, ASP.NET Web Forms 4.x
- **Banco de Dados:** SQL Server 2014+
- **Multi-tenant:** Não (filtros manuais por empresa)
- **Auditoria:** Inexistente (sem rastreamento de alterações)
- **Configurações:** Web.config, constantes hardcoded no código

### Observações Gerais

O sistema legado **NÃO possui módulo específico dedicado à Gestão de Custos Fixos**. Funcionalidades relacionadas a custos fixos, se existentes, estão:

1. **Integradas ao módulo financeiro genérico** (contas a pagar/receber)
2. **Gerenciadas manualmente em planilhas externas** (Excel)
3. **Controladas por lançamentos manuais mensais** (sem provisionamento automático)
4. **Sem alertas de variação orçamentária**
5. **Sem detecção de anomalias**
6. **Sem análise de tendências ou YoY**

### Principais Lacunas Identificadas

- ❌ Sem provisionamento automático de lançamentos recorrentes
- ❌ Sem sistema de alertas de variação orçamentária
- ❌ Sem detecção estatística de anomalias
- ❌ Sem dashboard gerencial de custos fixos
- ❌ Sem projeção de custos futuros
- ❌ Sem rateio automático por centro de custo
- ❌ Sem histórico de alterações de valores orçados
- ❌ Sem aprovação gerencial para variações significativas

---

## 2. TELAS DO LEGADO

### Constatação

**Nenhuma tela específica de Gestão de Custos Fixos foi identificada no sistema legado.**

Possíveis telas genéricas que podem ter sido usadas:

| Tela Hipotética | Caminho Provável | Responsabilidade |
|----------------|------------------|------------------|
| Contas a Pagar | `Financeiro/ContasPagar.aspx` | Lançamento manual de despesas recorrentes |
| Categorias de Despesa | `Cadastros/CategoriasDespesa.aspx` | Classificação de tipos de custo |
| Relatórios Financeiros | `Relatorios/Financeiro.aspx` | Visualização de despesas por categoria |

### Comportamentos Implícitos (Hipotéticos)

Baseado em padrões do sistema legado:

- **Lançamento manual mensal:** Usuário precisava lembrar de lançar custos fixos todo mês
- **Sem validação de variação:** Sistema aceitava qualquer valor sem alertas
- **Sem controle de duplicatas:** Possível lançar mesmo custo múltiplas vezes no mesmo mês
- **Sem rastreamento de origem:** Não havia flag indicando se lançamento foi manual ou automático

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

### Constatação

**Nenhum WebService (.asmx) ou API específica para Custos Fixos foi identificada.**

Possíveis métodos genéricos que podem ter sido usados:

| Método Hipotético | Local Provável | Responsabilidade |
|------------------|----------------|------------------|
| `InserirContaPagar()` | `Services/Financeiro.asmx` | Inserir despesa manualmente |
| `ListarDespesasPorCategoria()` | `Services/Relatorios.asmx` | Listar despesas por tipo |
| `ConsultarOrcamento()` | `Services/Orcamento.asmx` | Comparar realizado vs orçado |

---

## 4. TABELAS LEGADAS

### Estrutura Provável (Não Confirmada)

O sistema legado pode ter usado uma ou mais das seguintes tabelas genéricas:

#### Tabela Hipotética: `ContasPagar`

```sql
CREATE TABLE [dbo].[ContasPagar](
    [Id_Conta] [int] IDENTITY(1,1) NOT NULL,
    [Nm_Descricao] [varchar](500) NULL,
    [Id_Categoria] [int] NULL,
    [Vl_Conta] [decimal](18, 2) NULL,
    [Dt_Vencimento] [datetime] NULL,
    [Dt_Pagamento] [datetime] NULL,
    [Fl_Pago] [bit] NULL,
    CONSTRAINT [PK_ContasPagar] PRIMARY KEY ([Id_Conta])
);
```

**Problemas Identificados:**

- ❌ Sem campo de "Recorrência" ou "Tipo" (fixo vs variável)
- ❌ Sem campo de "Valor Orçado" vs "Valor Realizado"
- ❌ Sem campo de "Mês de Referência" para provisionamento
- ❌ Sem multi-tenancy (campo `Id_Fornecedor`)
- ❌ Sem auditoria (campos `Dt_Criacao`, `Id_Usuario_Criacao`, etc)
- ❌ Sem exclusão lógica (`Fl_Excluido`)
- ❌ Sem flag de "Provisionamento Automático"
- ❌ Sem campo de "Justificativa de Variação"
- ❌ Sem campo de "Aprovação Gerencial"

---

## 5. STORED PROCEDURES LEGADAS

### Constatação

**Nenhuma stored procedure específica para Custos Fixos foi identificada.**

Procedimentos genéricos que podem ter sido usados:

| Procedimento Hipotético | Finalidade | Observações |
|------------------------|------------|-------------|
| `sp_InserirContaPagar` | Inserir despesa manualmente | Sem validação de recorrência |
| `sp_ListarDespesasPorMes` | Listar despesas de um mês | Sem separação fixo/variável |
| `sp_ConsultarOrcadoRealizado` | Comparar orçado vs realizado | Sem alertas automáticos |

---

## 6. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

Baseado em análise de padrões do sistema legado:

### RL-RN-001: Lançamento Manual Mensal

**Descrição:** Custos fixos eram lançados manualmente todo mês pelo usuário responsável.

**Fonte:** Comportamento padrão observado em outros módulos financeiros.

**Destino:** **SUBSTITUÍDO** por provisionamento automático (RN-RF036-02).

**Impacto:** Reduz risco de esquecimento e garante consistência.

---

### RL-RN-002: Sem Validação de Variação Orçamentária

**Descrição:** Sistema aceitava qualquer valor de despesa sem comparar com orçado ou alertar variações.

**Fonte:** Ausência de validação em módulos financeiros legados.

**Destino:** **SUBSTITUÍDO** por alertas automáticos de variação (RN-RF036-03).

**Impacto:** Gestores terão visibilidade proativa de desvios.

---

### RL-RN-003: Sem Detecção de Anomalias

**Descrição:** Não havia análise estatística de valores fora do padrão histórico.

**Fonte:** Funcionalidade inexistente no legado.

**Destino:** **NOVO** - implementado via detecção estatística (RN-RF036-07).

**Impacto:** Identifica erros de digitação ou aumentos anormais automaticamente.

---

### RL-RN-004: Sem Rateio Automático

**Descrição:** Custos compartilhados eram lançados integralmente em um centro de custo.

**Fonte:** Limitação observada em outros módulos.

**Destino:** **SUBSTITUÍDO** por rateio multi-dimensional (RN-RF036-06).

**Impacto:** Alocação precisa de custos entre áreas/filiais.

---

### RL-RN-005: Sem Aprovação Gerencial

**Descrição:** Não havia workflow de aprovação para lançamentos com valores muito divergentes.

**Fonte:** Ausência de workflow de aprovação no legado.

**Destino:** **NOVO** - aprovação obrigatória para variações >30% (RN-RF036-05).

**Impacto:** Governança sobre custos com desvios significativos.

---

### RL-RN-006: Sem Histórico de Alterações

**Descrição:** Alterações em valores de despesas não eram rastreadas (quem, quando, por quê).

**Fonte:** Ausência de auditoria no legado.

**Destino:** **SUBSTITUÍDO** por auditoria automática (campos de auditoria obrigatórios).

**Impacto:** Rastreabilidade completa para compliance e auditorias.

---

### RL-RN-007: Sem Alertas de Vencimento

**Descrição:** Sistema não enviava notificações antes do vencimento de despesas.

**Fonte:** Funcionalidade inexistente no legado.

**Destino:** **NOVO** - alertas automáticos 7, 3 e 1 dia antes (RN-RF036-11).

**Impacto:** Reduz atrasos e multas por pagamento em atraso.

---

## 7. GAP ANALYSIS (LEGADO × RF MODERNO)

| Funcionalidade | Existe no Legado? | Existe no RF036? | Observação |
|----------------|-------------------|------------------|------------|
| Cadastro de Custos Fixos | ❌ Não (genérico) | ✅ Sim | Entidade dedicada com campos específicos |
| Provisionamento Automático | ❌ Não | ✅ Sim | Job Hangfire mensal |
| Alertas de Variação Orçamentária | ❌ Não | ✅ Sim | 3 níveis (10%, 20%, 30%) |
| Detecção de Anomalias | ❌ Não | ✅ Sim | Análise estatística (média + 2σ) |
| Dashboard Gerencial | ❌ Não | ✅ Sim | Com projeções 3, 6, 12 meses |
| Análise Year-over-Year (YoY) | ❌ Não | ✅ Sim | Comparação mesmo mês ano anterior |
| Rateio Multi-Dimensional | ❌ Não | ✅ Sim | Por centro de custo e filial |
| Aprovação Gerencial | ❌ Não | ✅ Sim | Para variações >30% |
| Alertas de Vencimento | ❌ Não | ✅ Sim | 7, 3, 1 dia antes |
| Auditoria Completa | ❌ Não | ✅ Sim | Campos de auditoria obrigatórios |
| Multi-Tenancy | ❌ Não | ✅ Sim | FornecedorId obrigatório |
| Exclusão Lógica | ❌ Não | ✅ Sim | FlExcluido = true |
| Histórico de Alterações | ❌ Não | ✅ Sim | Tabela de histórico + auditoria |
| RBAC Granular | ❌ Não | ✅ Sim | 7 permissões específicas |

---

## 8. DECISÕES DE MODERNIZAÇÃO

### Decisão 1: Criar Entidade Dedicada

**Decisão:** Criar entidade `CustoFixo` separada de `ContasPagar` genérico.

**Motivo:**
- Custos fixos têm comportamento específico (recorrência, provisionamento automático)
- Necessidade de campos próprios (ValorOrcado, TipoCustoFixo, Periodicidade)
- Separação facilita análise e relatórios específicos

**Impacto:** **Alto** - Exige migração de dados legados (se houver).

---

### Decisão 2: Provisionamento Automático com Hangfire

**Decisão:** Implementar job mensal via Hangfire no 1º dia útil do mês.

**Motivo:**
- Elimina necessidade de lançamento manual recorrente
- Garante consistência e previsibilidade
- Reduz risco de esquecimento

**Impacto:** **Alto** - Mudança cultural (usuários não lançam mais manualmente).

---

### Decisão 3: Alertas Proativos com 3 Níveis

**Decisão:** Alertas automáticos de variação em 10%, 20% e 30%.

**Motivo:**
- Gestores identificam desvios em tempo real
- Ação corretiva pode ser tomada antes do fechamento contábil
- Evita surpresas no final do mês

**Impacto:** **Médio** - Exige sistema de notificações funcional.

---

### Decisão 4: Aprovação Gerencial para Variações >30%

**Decisão:** Workflow de aprovação obrigatório para grandes variações.

**Motivo:**
- Governança sobre custos críticos
- Evita erros não detectados
- Rastreabilidade de decisões gerenciais

**Impacto:** **Médio** - Exige permissões RBAC e interface de aprovação.

---

### Decisão 5: Rateio Multi-Dimensional

**Decisão:** Permitir rateio por centro de custo e filial com soma = 100%.

**Motivo:**
- Custos compartilhados (aluguel, energia) precisam ser alocados proporcionalmente
- Facilita análise de custos por área/unidade
- Melhora acuracidade de relatórios gerenciais

**Impacto:** **Médio** - Complexidade adicional na criação de custos fixos.

---

## 9. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Probabilidade | Mitigação |
|------|---------|---------------|-----------|
| **Dados legados sem histórico de custos fixos** | Alto | Alta | Iniciar sistema novo sem migração de histórico legado |
| **Resistência a provisionamento automático** | Médio | Média | Treinamento e período de transição com revisão manual |
| **Falha no job de provisionamento** | Alto | Baixa | Monitoramento + alertas de falha + execução manual backup |
| **Classificação incorreta de custos (fixo vs variável)** | Médio | Média | Validação durante cadastro + revisão gerencial inicial |
| **Alertas excessivos (fadiga de notificação)** | Baixo | Média | Configuração de threshold ajustável por usuário |

---

## 10. RASTREABILIDADE (LEGADO → MODERNO)

| Elemento Legado | Referência RF036 | Status |
|----------------|------------------|--------|
| Lançamento Manual Mensal | RN-RF036-02 (Provisionamento Automático) | SUBSTITUÍDO |
| Ausência de Alertas | RN-RF036-03 (Alertas de Variação) | SUBSTITUÍDO |
| Ausência de Anomalia Detection | RN-RF036-07 (Detecção de Anomalias) | NOVO |
| Ausência de Rateio | RN-RF036-06 (Rateio Multi-Dimensional) | NOVO |
| Ausência de Aprovação | RN-RF036-05 (Aprovação Gerencial) | NOVO |
| Ausência de Auditoria | Campos de auditoria obrigatórios | SUBSTITUÍDO |
| Tabela `ContasPagar` (genérica) | Entidade `CustoFixo` (específica) | SUBSTITUÍDO |

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|--------|------|-----------|-------|
| 1.0 | 2025-12-30 | Documentação inicial de referência ao legado - RF036 Gestão de Custos Fixos | Agência ALC - alc.dev.br |
