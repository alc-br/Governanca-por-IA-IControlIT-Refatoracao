# RL-RF093 - Referência ao Legado: Indicadores de Performance e Compliance

**RF ID:** RF093
**Versão:** 1.0
**Data de Criação:** 2025-12-30
**RF Relacionado:** RF093 v2.0
**Status:** Documentado

---

## Seção 1: Visão Geral do Legado

### 1.1 Contexto Histórico

O **sistema de KPIs (Key Performance Indicators)** descrito no RF093 é uma **funcionalidade completamente NOVA** do IControlIT modernizado. Não há equivalente no sistema legado VB.NET/ASPX.

### 1.2 Situação Encontrada no Legado

Durante a análise do código legado em `D:\IC2\ic1_legado\`, foi identificado:

**✅ Encontrado:**
- Tabela `Si_KPI` no banco de dados legado (Cliente_Modelo.sql, K2A.sql)
- Estrutura extremamente simples com apenas 9 campos de configuração básica

**❌ NÃO Encontrado:**
- Nenhuma tela ASPX de gestão de KPIs (Dashboard.aspx, GestaoKPI.aspx, MetasKPI.aspx, RelatorioKPI.aspx)
- Nenhum webservice VB.NET para KPIs (WSKPI.asmx.vb)
- Nenhuma stored procedure de cálculo (pa_CalcularKPI_*, pa_VerificarAlertas, pa_GerarRelatorioKPI)
- Nenhuma rotina de cálculo automático ou agendamento
- Nenhum sistema de metas, alertas ou dashboards
- Nenhuma integração com SLA, Contratos, Ativos ou Custos
- Nenhuma trilha de auditoria de cálculos

### 1.3 Conclusão da Análise

A tabela `Si_KPI` encontrada no legado **NÃO constitui um sistema de KPIs**. É apenas uma configuração auxiliar básica, provavelmente usada para armazenar alguns parâmetros de processamento (dias de carga, nomes de hierarquia corporativa).

O RF093 implementa um **sistema completo e moderno de KPIs** que **NÃO possui contrapartida no legado**.

---

## Seção 2: Tabelas Legadas

### 2.1 Tabela: Si_KPI

**Localização:** `D:\IC2\ic1_legado\BancoDados\Interno\Cliente_Modelo.sql` (linhas 8204-8215)

**DDL Original:**
```sql
CREATE TABLE [dbo].[Si_KPI](
    [Fl_Carga_Auditada] [int] NOT NULL,
    [Dia_Entrega_RH] [int] NOT NULL,
    [Dia_Entrega_Rateio] [int] NOT NULL,
    [Dia_Carga] [int] NOT NULL,
    [Nm_Filial] [varchar](50) NULL,
    [Nm_Centro_Custo] [varchar](50) NULL,
    [Nm_Departamento] [varchar](50) NULL,
    [Nm_Setor] [varchar](50) NULL,
    [Nm_Secao] [varchar](50) NULL
) ON [PRIMARY]
```

**Problemas Identificados:**
- ❌ Sem chave primária (PK)
- ❌ Sem campos de auditoria (CriadoEm, CriadoPorUsuarioId, etc.)
- ❌ Sem suporte a multi-tenancy (ClienteId)
- ❌ Sem relacionamentos com outras tabelas
- ❌ Campos genéricos sem tipagem forte (varchar sem constraints)
- ❌ Propósito pouco claro (mistura dias de entrega com nomes de hierarquia)
- ❌ Sem versionamento ou histórico

**Uso Presumido:**
Aparentemente armazena configurações básicas de processamento batch (dias de carga, nomes de departamentos). **Não é um sistema de KPIs**.

**Destino:** `DESCARTADO`

**Justificativa:** Esta tabela não tem relação com o sistema de KPIs descrito no RF093. O novo sistema implementa entidades específicas (KpiDefinition, KpiTarget, KpiCalculation, KpiAlert, KpiAuditLog) com propósitos bem definidos.

---

## Seção 3: Stored Procedures Legadas

### 3.1 Análise Realizada

**Busca Executada:**
```bash
Grep pattern: "pa_.*KPI|pa_CalcularKPI|pa_VerificarAlertas|pa_GerarRelatorioKPI"
Path: D:\IC2\ic1_legado
```

**Resultado:** Nenhuma stored procedure relacionada a KPIs foi encontrada.

**Destino:** `NÃO APLICÁVEL`

---

## Seção 4: Telas ASPX Legadas

### 4.1 Análise Realizada

**Busca Executada:**
```bash
Glob pattern: **/*Dashboard*.aspx, **/*KPI*.aspx
Path: D:\IC2\ic1_legado\IControlIT
```

**Resultado:** Nenhuma tela ASPX relacionada a KPIs foi encontrada.

**Telas Esperadas (mas NÃO encontradas):**
- `Dashboard.aspx` → Dashboard de KPIs
- `GestaoKPI.aspx` → Gestão de Indicadores
- `MetasKPI.aspx` → Configuração de Metas
- `RelatorioKPI.aspx` → Relatórios Analíticos

**Destino:** `NÃO APLICÁVEL`

---

## Seção 5: Webservices VB.NET Legados

### 5.1 Análise Realizada

**Busca Executada:**
```bash
Glob pattern: **/WSKPI.asmx*
Path: D:\IC2\ic1_legado
```

**Resultado:** Nenhum webservice relacionado a KPIs foi encontrado.

**Webservice Esperado (mas NÃO encontrado):**
- `WSKPI.asmx.vb` → Webservice de KPIs com métodos GetKPIs(), CalcularKPI(), GetAlertas()

**Destino:** `NÃO APLICÁVEL`

---

## Seção 6: Regras de Negócio Implícitas

### 6.1 Regras Extraídas do Código Legado

**Status:** `NÃO APLICÁVEL`

Como não há código legado relacionado a KPIs (nenhuma stored procedure, tela ASPX ou webservice), **não foi possível extrair regras de negócio implícitas**.

### 6.2 Regras Presumidas (Baseadas na Tabela Si_KPI)

**RB-LEG-093-01: Configuração de Dias de Processamento**

**Descrição Presumida:**
A tabela `Si_KPI` aparentemente armazena dias específicos para processamentos batch:
- `Dia_Entrega_RH`: Dia do mês em que RH entrega dados
- `Dia_Entrega_Rateio`: Dia do mês em que rateios são entregues
- `Dia_Carga`: Dia do mês em que carga de dados é executada

**Destino:** `DESCARTADO`

**Justificativa:** Esta regra não tem relação com o sistema de KPIs do RF093. O novo sistema utiliza agendamento via Hangfire com periodicidade configurável (horária, diária, semanal, mensal, anual), sem dependência de "dias fixos de processamento".

---

**RB-LEG-093-02: Nomes de Hierarquia Corporativa**

**Descrição Presumida:**
A tabela `Si_KPI` armazena nomes de níveis hierárquicos:
- `Nm_Filial`, `Nm_Centro_Custo`, `Nm_Departamento`, `Nm_Setor`, `Nm_Secao`

Possível uso: padronização de nomenclatura em relatórios.

**Destino:** `DESCARTADO`

**Justificativa:** O novo sistema obtém hierarquia corporativa diretamente do RF009 (Hierarquia Corporativa), eliminando duplicação de dados. Nomes são obtidos via foreign keys, garantindo consistência.

---

## Seção 7: Mapeamento de Destino

### 7.1 Resumo Executivo

| Artefato Legado | Tipo | Destino | Justificativa |
|-----------------|------|---------|---------------|
| Tabela `Si_KPI` | Tabela SQL | `DESCARTADO` | Não é sistema de KPIs, apenas config básica sem relação com RF093 |
| Stored Procedures de KPI | Procedure | `NÃO APLICÁVEL` | Não existem no legado |
| Telas ASPX de KPI | UI | `NÃO APLICÁVEL` | Não existem no legado |
| Webservice WSKPI.asmx.vb | Webservice | `NÃO APLICÁVEL` | Não existe no legado |
| Regra de dias de processamento | Regra | `DESCARTADO` | Substituída por Hangfire com periodicidade configurável |
| Regra de nomes de hierarquia | Regra | `DESCARTADO` | Substituída por integração com RF009 |

### 7.2 Estatísticas de Destino

- **ASSUMIDO:** 0 itens (0%)
- **SUBSTITUÍDO:** 0 itens (0%) - Não há funcionalidade legada equivalente
- **DESCARTADO:** 2 itens (100%) - Tabela Si_KPI e regras presumidas
- **A_REVISAR:** 0 itens (0%)

### 7.3 Análise de Cobertura

**Total de Itens Legados Analisados:** 2 (1 tabela + 1 conjunto de regras presumidas)
**Itens com Destino Definido:** 2 (100%)
**Itens Pendentes de Análise:** 0 (0%)

**Status:** ✅ **100% de cobertura alcançada**

---

## Seção 8: Funcionalidades Novas (Sem Legado)

As seguintes funcionalidades do RF093 são **completamente novas** e não possuem qualquer contrapartida no legado:

1. **Sistema completo de gestão de KPIs**
   - Cadastro de indicadores com fórmulas customizadas
   - Validação automática de fórmulas (sintaxe, referências, divisão por zero)
   - Versionamento e histórico de alterações

2. **Cálculo automático via Hangfire**
   - Agendamento periódico (horário, diário, semanal, mensal, anual)
   - Execução em background sem bloquear aplicação
   - Retry automático em caso de falha (3 tentativas)

3. **Sistema de metas e alertas**
   - Configuração de limites verde/amarelo/vermelho
   - Geração automática de alertas em desvios
   - Notificações multicanal (email, SMS, in-app via SignalR)

4. **Dashboards em tempo real**
   - Atualização automática via SignalR
   - Drill-down em gráficos
   - Exportação para PDF/Excel

5. **Indicadores específicos por categoria**
   - SLA: Percentual cumprimento, tempo médio resposta/resolução
   - Contratos: Custos, economia em renegociações
   - Ativos: TCO, taxa de utilização, disponibilidade
   - Custos: Variação orçamentária, ROI, tendências
   - Compliance: Aderência SOX/LGPD/ISO 27001

6. **Integração com ferramentas de BI**
   - Endpoint OData para Power BI
   - Web Data Connector para Tableau
   - Templates pré-configurados (.pbix, .twb)

7. **Auditoria completa**
   - Registro imutável de todos os cálculos
   - Snapshot de dados de entrada
   - Trilha de alterações com before/after

8. **Busca full-text com ElasticSearch**
   - Indexação automática de documentos
   - Busca facetada com filtros combinados
   - Fuzzy matching (tolerância a erros)

**Conclusão:** O RF093 é um **módulo inteiramente novo** que implementa capacidades analíticas modernas inexistentes no sistema legado.

---

## Seção 9: Recomendações Técnicas

### 9.1 Não Migrar Dados da Tabela Si_KPI

**Recomendação:** `NÃO migrar` dados da tabela `Si_KPI` para o novo sistema.

**Justificativa:**
- A tabela legada não armazena KPIs propriamente ditos
- Os campos (Dia_Entrega_RH, Nm_Filial, etc.) não têm correspondência nas novas entidades
- Dados parecem ser configurações específicas de processamento batch legado
- Migração causaria inconsistência semântica (forçar encaixe de dados incompatíveis)

### 9.2 Iniciar Sistema de KPIs com Dados Zerados

**Recomendação:** Implementar RF093 com banco de dados limpo (sem dados legados).

**Passos Sugeridos:**
1. Criar entidades modernas: `KpiDefinition`, `KpiTarget`, `KpiCalculation`, `KpiAlert`, `KpiAuditLog`
2. Permitir que usuários cadastrem KPIs manualmente via interface Angular
3. Sistema calculará histórico a partir da data de cadastro (não retroativo ao legado)
4. Dashboards exibirão dados a partir da data de ativação do módulo

### 9.3 Considerar Importação Manual de Indicadores Críticos

**Recomendação:** Se houver KPIs sendo acompanhados manualmente (ex: planilhas Excel), considerar importação via API.

**Cenário:**
- Empresa já acompanha "Taxa de Cumprimento de SLA" manualmente
- Possui histórico de 12 meses em Excel

**Solução:**
- Criar endpoint de importação: `POST /api/kpis/import`
- Validar formato CSV (colunas: Data, Valor, Meta)
- Criar registros em `KpiCalculation` com dados históricos
- Usuário visualiza tendência imediatamente no dashboard

---

## Seção 10: Referências

### 10.1 Documentos Relacionados

- **RF093 v2.0** - Indicadores de Performance e Compliance
- **RF028** - Gestão de SLA
- **RF029** - Monitoramento de SLA
- **RF023** - Gestão de Contratos
- **RF090** - Renovação de Contratos
- **RF028** - Gestão de Ativos
- **RF094** - Gestão de Custos
- **RF079** - Auditoria e Compliance
- **RF009** - Hierarquia Corporativa

### 10.2 Código Legado Consultado

- **Cliente_Modelo.sql** - `D:\IC2\ic1_legado\BancoDados\Interno\Cliente_Modelo.sql` (linhas 8204-8215)
- **K2A.sql** - `D:\IC2\ic1_legado\BancoDados\Interno\K2A.sql` (confirmação da tabela Si_KPI)

### 10.3 Buscas Executadas no Legado

| Tipo | Pattern | Caminho | Resultado |
|------|---------|---------|-----------|
| Tabelas SQL | `Si_KPI` | `D:\IC2\ic1_legado\BancoDados\` | ✅ ENCONTRADO |
| Stored Procedures | `pa_.*KPI\|pa_CalcularKPI\|pa_VerificarAlertas` | `D:\IC2\ic1_legado\` | ❌ NÃO ENCONTRADO |
| Telas ASPX | `**/*Dashboard*.aspx, **/*KPI*.aspx` | `D:\IC2\ic1_legado\IControlIT\` | ❌ NÃO ENCONTRADO |
| Webservices | `**/WSKPI.asmx*` | `D:\IC2\ic1_legado\` | ❌ NÃO ENCONTRADO |
| Code-behind VB.NET | `*KPI*.vb` | `D:\IC2\ic1_legado\IControlIT\` | ❌ NÃO ENCONTRADO |

### 10.4 Tecnologias de Referência

**Sistema Novo (RF093):**
- .NET 10 + Entity Framework Core 10
- Hangfire (agendamento de cálculos)
- SignalR (atualização em tempo real)
- ElasticSearch (busca full-text)
- Angular 19 (dashboards)
- ApexCharts (visualizações)

**Sistema Legado:**
- VB.NET + ASP.NET Web Forms
- SQL Server (stored procedures)
- JavaScript (client-side)

---

## Seção 11: Histórico de Revisões

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 1.0 | 2025-12-30 | Equipe IControlIT | Versão inicial - Análise completa do legado - Confirmação de que sistema de KPIs não existe no legado |

---

**Fim do Documento RL-RF093 v1.0**
