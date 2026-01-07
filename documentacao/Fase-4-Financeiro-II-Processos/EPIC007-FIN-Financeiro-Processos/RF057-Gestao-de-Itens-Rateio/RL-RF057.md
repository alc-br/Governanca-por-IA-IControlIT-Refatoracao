# RL-RF057 — Referência ao Legado

**Versão:** 1.0
**Data:** 2025-01-14
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF-057 — Gestão de Itens de Rateio
**Sistema Legado:** ASP.NET Web Forms + VB.NET
**Objetivo:** Documentar ausência de funcionalidade equivalente no legado e justificar criação direta no formato moderno.

---

## 1. CONTEXTO DO LEGADO

### Arquitetura
- **Tipo:** Monolítica Cliente-Servidor
- **Frontend:** ASP.NET Web Forms (ASPX + Code-Behind VB.NET)
- **Backend:** VB.NET + Stored Procedures SQL Server
- **Banco de Dados:** SQL Server (schema `Branco.sql`)
- **Sessão:** ViewState + Session State

### Stack Tecnológica
- ASP.NET Framework 4.7.2
- VB.NET
- SQL Server 2012+
- IIS 7.5+
- JavaScript Vanilla + jQuery + Bootstrap 4.5

### Multi-tenancy
- **Parcial** - Segregação por base de dados cliente (padrão `SC_<OPERADORA>_<CLIENTE>`)
- Não há isolamento por `TenantId` nas tabelas
- Cada cliente possui banco SQL Server separado

### Auditoria
- **Parcial** - Existe tabela `Auditoria_Resumo` e webservice `WS_Cadastro.Envia_Log`
- Auditoria não é automática (requer chamada explícita no code-behind)
- Sem campos `Created`, `CreatedBy`, `LastModified`, `LastModifiedBy` nas tabelas

---

## 2. ANÁLISE DE FUNCIONALIDADE NO LEGADO

### Pesquisa Realizada

Foram realizadas as seguintes verificações no sistema legado localizado em `D:\IC2\ic1_legado\`:

1. **Busca por arquivos `.aspx` e `.asmx` relacionados**:
   - Padrão buscado: `*Rateio*`, `*RateioItem*`, `*ItemRateio*`, `*AlocacaoItem*`
   - **Resultado:** Nenhum arquivo encontrado

2. **Busca em README do legado** (`ic1_legado/README.md`):
   - Webservice `WSRateio.asmx` mencionado na seção "Servicos SOAP principais"
   - Descrito como: "endpoints especificos para cada macro dominio"
   - **Observação:** WSRateio.asmx existe mas não trata de gestão granular de itens

3. **Busca no schema do banco** (`BancoDados/Base/Branco.sql`):
   - Padrão buscado: `CREATE TABLE.*Rateio`, `CREATE TABLE.*Item`, `Alocacao`
   - **Resultado:** Tabela `Rateio` encontrada (relacionada a Recepcao_Fatura)
   - **Observação:** Tabela `Rateio` do legado trata de rateio de custos de fatura, **NÃO de gestão granular de itens individuais**

4. **Busca por termos no código VB.NET**:
   - Padrão buscado: `rateio`, `alocacao`, `linha movel`, `licenca software`
   - **Resultado:** Referências a "rateio" encontradas apenas em contexto de fatura (módulo `Recepcao_Fatura`)

### Conclusão da Pesquisa

**NÃO EXISTE funcionalidade equivalente no sistema legado.**

O sistema legado possui apenas:
- **Rateio de Fatura** (módulo `Recepcao_Fatura`): divide custos de fatura entre centros de custo
- **Webservice WSRateio.asmx**: suporta rateio de valores de fatura, **NÃO itens individuais**

**NÃO POSSUI:**
- Gestão granular de itens (linhas móveis, licenças, links, equipamentos)
- Configuração individual de regras de rateio por item
- Categorização de itens rateáveis
- Exceções de rateio por item
- Histórico versionado de alocações de item
- Detecção automática de itens sem uso
- Dashboard de itens de rateio

---

## 3. FUNCIONALIDADE LEGADA RELACIONADA (RATEIO DE FATURA)

Embora NÃO seja equivalente ao RF-057, documentamos abaixo a funcionalidade de **Rateio de Fatura** do legado para referência histórica:

### Tela: Rateio.aspx

- **Caminho:** `ic1_legado/IControlIT/Recepcao_Fatura/Rateio.aspx`
- **Responsabilidade:** Configurar regras de rateio de fatura entre centros de custo
- **Escopo:** Rateia **VALOR TOTAL DA FATURA**, não itens individuais

#### Comportamento Legado

- ✅ Permite dividir custo de fatura entre múltiplos centros de custo com percentuais
- ✅ Valida que soma dos percentuais = 100%
- ❌ **NÃO permite** configurar rateio por item individual (linha, licença, link)
- ❌ **NÃO categoriza** itens em LinhaMobile, LicencaSoftware, LinkDados, Equipamento
- ❌ **NÃO suporta** rateio dedicado vs compartilhado por item
- ❌ **NÃO separa** custos fixos de custos variáveis por item
- ❌ **NÃO rastreia** histórico de mudanças de alocação por item
- ❌ **NÃO detecta** itens sem uso
- ❌ **NÃO permite** exceções de rateio por item específico

---

## 4. TABELAS LEGADAS RELACIONADAS

### Tabela: Rateio (legado)

| Campo | Tipo | Finalidade | Diferenças vs RF-057 |
|-------|------|------------|----------------------|
| `Id_Rateio` | INT IDENTITY | PK da regra de rateio | ❌ Rateio é de fatura, não de item |
| `Id_Fatura` | INT | FK para tabela Fatura | ❌ RF-057 não depende de fatura |
| `Id_Centro_Custo` | INT | Centro de custo destino | ✅ Conceito equivalente (AlocacaoItem.CentroCusto) |
| `Percentual` | DECIMAL(5,2) | Percentual de rateio | ✅ Conceito equivalente (AlocacaoItem.Percentual) |
| - | - | - | ❌ Não há ItemId, Categoria, TipoRateio |
| - | - | - | ❌ Não há separação CustoFixo/CustoVariavel |
| - | - | - | ❌ Não há campos de auditoria (Created, CreatedBy) |
| - | - | - | ❌ Não há multi-tenancy (EmpresaId) |

### Stored Procedures Relacionadas

- `pa_Rateio`: CRUD básico de regras de rateio de fatura
- `sp_ProcessarRateioFatura`: Aplica regras de rateio sobre fatura fechada
- **Observação:** Nenhuma procedure trata de itens individuais

---

## 5. GAP ANALYSIS (LEGADO x RF MODERNO)

| Item | Legado (Rateio de Fatura) | RF-057 (Rateio de Itens) | Gap |
|------|---------------------------|--------------------------|-----|
| **Granularidade** | Fatura completa | Item individual (linha, licença, link, equipamento) | **CRÍTICO** - Conceitos completamente diferentes |
| **Categorização** | Ausente | 4 categorias (LinhaMobile, LicencaSoftware, LinkDados, Equipamento) | **ALTO** - Funcionalidade nova |
| **Tipo de Rateio** | Apenas percentual | Dedicado (100% para um CC) vs Compartilhado (% entre múltiplos) | **MÉDIO** - Legado assume sempre compartilhado |
| **Custos Fixos vs Variáveis** | Ausente (rateia valor total) | Separação obrigatória (franquia vs excedente) | **ALTO** - Precisão contábil |
| **Exceções** | Ausente | Exceções temporárias/permanentes por item | **ALTO** - Flexibilidade para VIPs |
| **Histórico** | Ausente | Versionamento completo com vigência | **CRÍTICO** - Auditoria e rastreabilidade |
| **Rateio Proporcional ao Uso** | Ausente | Baseado em Consumos.Quantidade medido | **ALTO** - Justiça na distribuição de custos |
| **Detecção Itens Sem Uso** | Ausente | Job Hangfire mensal automático | **MÉDIO** - Economia de custos |
| **Grupos de Itens** | Ausente | Aplicar regra em lote para grupo | **MÉDIO** - Produtividade |
| **Ajustes por Item** | Ausente | Multas, créditos, descontos vinculados a item | **MÉDIO** - Flexibilidade contábil |
| **Dashboard** | Ausente | Top caros, sem uso, evolução de custos | **ALTO** - Gestão gerencial |
| **Transferência entre CCs** | Ausente | Transferência de item dedicado com rastreabilidade | **MÉDIO** - Mobilidade organizacional |
| **Import CSV** | Ausente | Import em massa com validação | **MÉDIO** - Onboarding rápido |
| **Comparativo Mensal** | Ausente | Alerta variação > 30% | **MÉDIO** - Controle de anomalias |
| **Relatório Detalhado** | Ausente | Histórico completo do item (12 meses) | **ALTO** - Transparência |

---

## 6. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

### RL-RN-001: Rateio Sempre de Fatura Inteira

- **Descrição:** Sistema legado rateia apenas o valor total da fatura, nunca itens individuais
- **Implementação:** Tabela `Rateio` com FK para `Id_Fatura`
- **Limitação:** Impossível ratear linha móvel X diferentemente de linha móvel Y na mesma fatura
- **Fonte:** `ic1_legado/IControlIT/Recepcao_Fatura/Rateio.aspx.vb`

### RL-RN-002: Percentuais Fixos por Centro de Custo

- **Descrição:** Percentual de rateio é definido uma vez e aplicado para toda a fatura
- **Implementação:** Regras de rateio estáticas em tabela `Rateio`
- **Limitação:** Impossível aplicar percentuais diferentes para tipos de item diferentes
- **Fonte:** Stored procedure `sp_ProcessarRateioFatura`

### RL-RN-003: Sem Separação Fixo/Variável

- **Descrição:** Custo total da fatura é rateado sem separar franquia de excedente
- **Implementação:** Rateio aplica percentual sobre campo `Fatura.ValorTotal`
- **Limitação:** Impossível ratear franquia igualmente e excedente proporcionalmente ao uso
- **Fonte:** `pa_Rateio`

### RL-RN-004: Mudanças de Rateio Sem Vigência

- **Descrição:** Alterar regra de rateio afeta todas as faturas retroativamente
- **Implementação:** UPDATE direto em `Rateio` sem controle de vigência
- **Limitação:** Impossível manter histórico "CC X recebia 40% até março, depois 30%"
- **Fonte:** `Rateio.aspx.vb` (botão Salvar)

### RL-RN-005: Sem Detecção de Anomalias

- **Descrição:** Não há alertas automáticos de variação de custo ou itens sem uso
- **Implementação:** Relatórios são estáticos, sem inteligência
- **Limitação:** Gestores não são notificados de linhas com custo 300% maior que mês anterior
- **Fonte:** Módulo `Consulta` (relatórios manuais)

---

## 7. DECISÕES DE MODERNIZAÇÃO

### Decisão 1: Criar Funcionalidade Totalmente Nova (Sem Migração)

- **Descrição:** RF-057 é uma funcionalidade nova sem equivalente no legado
- **Motivo:** Legado só rateia faturas, não itens individuais
- **Impacto:** **NENHUM** - Não há dados legados a migrar
- **Justificativa:** Funcionalidade solicitada por gestores financeiros para controle granular

### Decisão 2: Não Integrar com Rateio de Fatura Legado

- **Descrição:** RF-057 e Rateio de Fatura são funcionalidades independentes
- **Motivo:** Escopos diferentes (item vs fatura completa)
- **Impacto:** **BAIXO** - Ambos podem coexistir sem conflito
- **Justificativa:** RF-057 é nível tático (item a item), Rateio de Fatura é nível estratégico (fatura inteira)

### Decisão 3: Não Reaproveitar Tabela `Rateio` do Legado

- **Descrição:** Criar tabelas novas (`ItemRateio`, `AlocacaoItem`, etc)
- **Motivo:** Estrutura legada incompatível (FK para Fatura, não para Item)
- **Impacto:** **NENHUM** - Não há conflito de namespace
- **Justificativa:** Separação clara de responsabilidades

### Decisão 4: Implementar Hangfire para Automações

- **Descrição:** Usar Hangfire para detectar itens sem uso e comparar custos mensais
- **Motivo:** Legado não possui scheduler/jobs automáticos
- **Impacto:** **MÉDIO** - Requer configuração Hangfire no backend
- **Justificativa:** Proatividade na gestão de custos

### Decisão 5: Usar Clean Architecture + CQRS Desde o Início

- **Descrição:** Implementar RF-057 diretamente em .NET 10 + Angular 19
- **Motivo:** Não há código legado a refatorar
- **Impacto:** **POSITIVO** - Arquitetura moderna desde o início
- **Justificativa:** Aproveitar ausência de legado para seguir boas práticas

---

## 8. RISCOS DE MODERNIZAÇÃO

### Risco 1: Expectativas Incompatíveis com Legado

- **Risco:** Usuários podem esperar que RF-057 se comporte como Rateio de Fatura legado
- **Impacto:** MÉDIO
- **Probabilidade:** BAIXA (funcionalidades têm escopos claramente diferentes)
- **Mitigação:** Treinamento explicitando que RF-057 é funcionalidade nova, não substituição

### Risco 2: Dados de Consumo Podem Não Existir

- **Risco:** RN-RF057-006 (rateio proporcional ao uso) depende de tabela `Consumos` (de RF separado)
- **Impacto:** ALTO
- **Probabilidade:** BAIXA (tabela Consumos já existe no legado)
- **Mitigação:** Validar integração com tabela `Consumos` no legado antes de implementar RN-RF057-006

### Risco 3: Performance com 50.000 Itens

- **Risco:** Requisito não funcional exige processar 50.000 itens em < 10 min
- **Impacto:** ALTO
- **Probabilidade:** MÉDIA (algoritmo de rateio pode ser lento)
- **Mitigação:** Usar processamento em lote (Hangfire background jobs) e índices otimizados

---

## 9. RASTREABILIDADE (LEGADO → MODERNO)

| Elemento Legado | Referência RF-057 | Status |
|-----------------|-------------------|--------|
| ❌ **Nenhum** - Funcionalidade não existe no legado | RF-057 completo | **NOVO** |
| Conceito de percentual de alocação (tabela `Rateio`) | `AlocacaoItem.Percentual` | **INSPIRADO** |
| Validação soma percentuais = 100% (Rateio de Fatura) | `RN-RF057-011` | **ASSUMIDO** |
| Tabela `Consumos` (já existe no legado) | `RN-RF057-006` (rateio proporcional ao uso) | **INTEGRAÇÃO** |
| Conceito de Centro de Custo | `AlocacaoItem.CentroCusto` | **ASSUMIDO** |

**Nota:** Como não há funcionalidade legada equivalente, quase 100% do RF-057 é **NOVO**.

---

## 10. REFERÊNCIAS AO CÓDIGO LEGADO

### Arquivos Consultados Durante Pesquisa

1. `ic1_legado/README.md` - Visão geral do sistema legado
2. `ic1_legado/BancoDados/Base/Branco.sql` - Schema completo do banco
3. `ic1_legado/IControlIT/Recepcao_Fatura/Rateio.aspx` - Tela de rateio de fatura (funcionalidade relacionada)
4. `ic1_legado/IControlIT/Recepcao_Fatura/Rateio.aspx.vb` - Code-behind rateio de fatura
5. Busca global por `*.aspx`, `*.asmx`, `*.vb` contendo termos "rateio", "alocacao", "item"

### Webservices Relacionados (Indiretos)

- `WSRateio.asmx` - Rateio de fatura (NÃO de itens individuais)
- `WSConsulta.asmx` - Consultas/relatórios (pode ter consumo de dados)

### Tabelas Relacionadas (Indiretas)

- `Rateio` - Regras de rateio de fatura (conceito similar mas escopo diferente)
- `Consumos` - Consumo medido (necessário para RN-RF057-006)
- `Centro_Custo` - Centros de custo (usado em `AlocacaoItem`)

---

## 11. CONCLUSÃO

**RF-057 (Gestão de Itens de Rateio) é uma funcionalidade INTEIRAMENTE NOVA sem equivalente no sistema legado.**

O sistema legado possui apenas rateio de **FATURA COMPLETA** (módulo Recepcao_Fatura), que divide o valor total da fatura entre centros de custo. RF-057 vai além, permitindo:

- Gestão granular de **ITENS INDIVIDUAIS** (linha móvel, licença, link, equipamento)
- Regras **CUSTOMIZADAS POR ITEM** (dedicado vs compartilhado, exceções, histórico)
- Automações **PROATIVAS** (detecção de itens sem uso, alertas de variação)

**Recomendação:** Implementar RF-057 diretamente em arquitetura moderna (.NET 10 + Angular 19) aproveitando a ausência de legado para seguir Clean Architecture + CQRS desde o início.

**Próximo Passo:** Executar CONTRATO-EXECUCAO-BACKEND para implementar o backend completo do RF-057.

---

**Documento gerado em:** 2025-01-14
**Versão:** 1.0
