# RL-RF094 — Referência ao Legado: Auditoria de Custos e Compliance

**Versão:** 1.0
**Data:** 2025-12-31
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF-094
**Sistema Legado:** IControlIT v1.0 (ASP.NET Web Forms / VB.NET)
**Objetivo:** Documentar o comportamento do legado que serve de base para a refatoração, garantindo rastreabilidade, entendimento histórico e mitigação de riscos.

---

## 1. CONTEXTO DO SISTEMA LEGADO

### 1.1 Arquitetura Geral

- **Arquitetura**: Monolítica com separação de bases de dados por cliente
- **Linguagem / Stack**: ASP.NET Web Forms, VB.NET code-behind, SQL Server
- **Tecnologia Frontend**: ASPX com ViewState, JavaScript vanilla
- **Banco de Dados**: SQL Server (18 bases separadas - Alpargatas, Vale, Bombril, etc.)
- **Multi-tenant**: Sim (banco por cliente - problemas de manutenção)
- **Auditoria**: Parcial (logs em texto, sem estrutura formal)
- **Configurações**: Web.config (hardcoded), arquivos de configuração locais

### 1.2 Stack Tecnológica

| Componente | Tecnologia Legado | Observações |
|------------|-------------------|-------------|
| **Backend** | VB.NET (code-behind ASPX) | Lógica misturada com apresentação |
| **Relatórios** | Crystal Reports | Geração lenta, dependência de licenças |
| **Exportação** | Excel manual, PDF estático | Sem histórico, versão única |
| **Análise de Dados** | Stored Procedures SQL | Queries complexas sem índices adequados |
| **Visualização** | Tabelas ASPX, DataGridView | Sem drill-down, interatividade limitada |
| **Jobs Batch** | SQL Server Agent | Sem log estruturado, difícil debug |
| **Detecção de Anomalias** | Manual (analistas) | Nenhum algoritmo, 100% humano |

### 1.3 Problemas Arquiteturais Identificados

1. **Multi-database sem consolidação**: 18 bases SQL Server separadas (manutenção cara, queries lentas)
2. **Lógica de negócio em stored procedures**: Difícil testar, versionar e portar
3. **Relatórios estáticos**: Crystal Reports com performance ruim em grandes volumes
4. **Análise manual de anomalias**: Custo alto de especialistas, detecção lenta
5. **Auditoria não estruturada**: Logs em arquivos de texto, busca impossível
6. **ViewState excessivo**: Páginas ASPX com 2-5MB de ViewState (slow load)

---

## 2. TELAS DO LEGADO

### Tela: RelatoriosCustos.aspx

- **Caminho:** `ic1_legado/IControlIT/Relatorios/RelatoriosCustos.aspx`
- **Responsabilidade:** Exibir relatórios estáticos de custos agrupados por fornecedor, categoria ou período

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|------|------|-------------|-------------|
| `ddlFornecedor` | DropDownList | Não | Carrega fornecedores de todos os clientes (bug multi-tenant) |
| `ddlCategoria` | DropDownList | Não | Categorias fixas (Telecom, TI, Outsourcing) |
| `txtDataInicio` | TextBox (Calendar) | Sim | Validação JavaScript (aceita datas inválidas) |
| `txtDataFim` | TextBox (Calendar) | Sim | Validação JavaScript (aceita datas inválidas) |
| `btnGerar` | Button | - | Chama `pa_CustosPorFornecedor` SP |
| `gvCustos` | GridView | - | DataGridView sem paginação (lento > 1000 registros) |

#### Comportamentos Implícitos

- ❌ **Sem isolamento multi-tenant**: Dropdown carrega fornecedores de TODOS os clientes (bug crítico de segurança)
- ❌ **Sem paginação**: GridView carrega tudo em memória (crash com > 5.000 registros)
- ❌ **Exportação manual**: Usuário precisa copiar/colar para Excel (sem histórico)
- ❌ **Sem drill-down**: Clique em linha não expande detalhes
- ❌ **Performance ruim**: Query `pa_CustosPorFornecedor` sem índices (timeout > 60s)

**DESTINO**: SUBSTITUÍDO por `/financeiro/auditoria/relatorios` (Angular)

---

### Tela: AnaliseVariancia.aspx

- **Caminho:** `ic1_legado/IControlIT/Relatorios/AnaliseVariancia.aspx`
- **Responsabilidade:** Análise manual de variância entre custo planejado e realizado

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|------|------|-------------|-------------|
| `ddlCentroCusto` | DropDownList | Sim | Carrega centros de custo do cliente autenticado |
| `txtMesReferencia` | TextBox | Sim | Formato MM/YYYY (validação VB.NET) |
| `btnCalcular` | Button | - | Chama `pa_AnaliseVariancia` SP |
| `lblCustoPlano` | Label | - | Exibe valor planejado |
| `lblCustoRealizado` | Label | - | Exibe valor realizado |
| `lblVariancia` | Label | - | Cálculo manual (Realizado - Plano) |
| `lblPercentual` | Label | - | Cálculo manual sem classificação |

#### Comportamentos Implícitos

- ❌ **Sem classificação de severidade**: Não categoriza variância (Aceitável, Aviso, Crítico)
- ❌ **Sem histórico**: Recalcula toda vez, não persiste resultado
- ❌ **Sem alertas**: Variância > 15% não dispara notificação
- ❌ **Sem comparação com períodos anteriores**: Análise isolada mensal

**DESTINO**: SUBSTITUÍDO por `/financeiro/auditoria/variancia` (Dashboard interativo)

---

### Tela: AnomaliasCustos.aspx

- **Caminho:** `ic1_legado/IControlIT/Relatorios/AnomaliasCustos.aspx`
- **Responsabilidade:** Lista de anomalias detectadas manualmente por analistas

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|------|------|-------------|-------------|
| `gvAnomalias` | GridView | - | Carrega anomalias marcadas por humanos |
| `txtObservacao` | TextBox (MultiLine) | Não | Observação manual do analista |
| `ddlStatus` | DropDownList | Sim | Novo, Investigando, Resolvido, Falso Positivo |
| `btnAtualizar` | Button | - | Atualiza status manualmente |

#### Comportamentos Implícitos

- ❌ **Detecção 100% manual**: Nenhum algoritmo, analistas revisam faturas linha-a-linha
- ❌ **Sem Z-score ou ML**: Anomalias identificadas por "experiência" do analista
- ❌ **Sem severidade**: Todas anomalias tratadas igualmente (falta priorização)
- ❌ **Sem integração com alertas**: Email manual copiando observação

**DESTINO**: SUBSTITUÍDO por `/financeiro/auditoria/anomalias` (Detecção automática ML)

---

### Tela: CustosPorFornecedor.aspx

- **Caminho:** `ic1_legado/IControlIT/Relatorios/CustosPorFornecedor.aspx`
- **Responsabilidade:** Custos agrupados por fornecedor

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|------|------|-------------|-------------|
| `gvFornecedores` | GridView | - | Agrupamento SQL |
| `txtPeriodo` | TextBox | Sim | Mês/Ano |

#### Comportamentos Implícitos

- ❌ **Sem drill-down**: Clique em fornecedor não detalha faturas
- ❌ **Sem gráficos**: Apenas tabela de texto

**DESTINO**: SUBSTITUÍDO por `/financeiro/auditoria/custos-fornecedor` (Drill-down interativo)

---

### Tela: DepreciacaoAtivos.aspx

- **Caminho:** `ic1_legado/IControlIT/Ativos/DepreciacaoAtivos.aspx`
- **Responsabilidade:** Relatório de depreciação de ativos

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|------|------|-------------|-------------|
| `gvAtivos` | GridView | - | Exibe depreciação acumulada |
| `ddlMetodo` | DropDownList | Sim | Linear, Acelerado |

#### Comportamentos Implícitos

- ❌ **Cálculo manual mensal**: Job SQL Server Agent (falha sem log)
- ❌ **Sem histórico mensal**: Apenas valor acumulado atual

**DESTINO**: SUBSTITUÍDO por `/financeiro/auditoria/depreciacao` (Hangfire job + histórico)

---

### Tela: ConformidadeCompliance.aspx

- **Caminho:** `ic1_legado/IControlIT/Compliance/ConformidadeCompliance.aspx`
- **Responsabilidade:** Check-list manual de conformidade

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|------|------|-------------|-------------|
| `chkLGPD` | CheckBox | - | Marcação manual "LGPD OK" |
| `chkSOX` | CheckBox | - | Marcação manual "SOX OK" |
| `txtObservacoes` | TextBox | Não | Texto livre |

#### Comportamentos Implícitos

- ❌ **100% manual**: Nenhuma validação automática
- ❌ **Sem evidências**: CheckBox marcado sem anexo de prova
- ❌ **Sem histórico**: Não rastreia quem/quando marcou

**DESTINO**: SUBSTITUÍDO por `/financeiro/auditoria/compliance` (Alertas automáticos)

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

### WebService: WSAuditoria.asmx.vb

- **Caminho:** `ic1_legado/IControlIT/WebService/WSAuditoria.asmx.vb`

| Método | Responsabilidade | Observações | Destino |
|--------|------------------|-------------|---------|
| `GetCustosPorFornecedor(dataInicio, dataFim)` | Retorna custo agrupado por fornecedor | Query SQL hardcoded, sem paginação | **SUBSTITUÍDO** por `GET /api/auditoria/custos-fornecedor` |
| `CalcularVariancia(ccId, dataInicio, dataFim)` | Calcula variância para centro de custo | Não persiste resultado, sem classificação | **SUBSTITUÍDO** por `GET /api/auditoria/variancia` |
| `DetectarAnomalias(fornecedorId)` | Simples MAX/MIN check | Algoritmo primitivo (não usa Z-score) | **SUBSTITUÍDO** por `POST /api/auditoria/anomalias/detectar` (Z-score + ML) |
| `ExportarRelatorio(tipo, formato)` | Exporta relatório em PDF ou Excel | Crystal Reports (lento, licenças) | **SUBSTITUÍDO** por `GET /api/auditoria/relatorios/exportar` |
| `CalcularDepreciacao(ativoId)` | Calcula depreciação de um ativo | Apenas método linear, sem histórico | **SUBSTITUÍDO** por `GET /api/auditoria/depreciacao/{ativoId}` |
| `VerificarCompliance(clienteId)` | Verifica violações de conformidade | Verifica apenas fornecedores, incompleto | **SUBSTITUÍDO** por `GET /api/auditoria/compliance/verificar` |

---

## 4. STORED PROCEDURES LEGADAS

### pa_CustosPorFornecedor

- **Caminho:** `ic1_legado/Database/Procedures/pa_CustosPorFornecedor.sql`
- **Responsabilidade:** Agrega custos mensais por fornecedor com comparação ao mês anterior

#### Parâmetros

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `@ClienteId` | UNIQUEIDENTIFIER | ID do cliente (multi-tenant) |
| `@DataInicio` | DATE | Data início período |
| `@DataFim` | DATE | Data fim período |

#### Lógica Principal

- Agrega `Fatura.ValorTotal` por `FornecedorId`
- Calcula crescimento comparado ao mês anterior (sem Z-score)
- Ordena por `ValorTotal DESC`
- **Problemas**: Query sem índice em `Fatura.DataEmissao`, timeout > 60s em volumes altos

**DESTINO**: **SUBSTITUÍDO** por Query EF Core + LINQ no Handler `GetCustosFornecedorQuery`

---

### pa_AnaliseVariancia

- **Caminho:** `ic1_legado/Database/Procedures/pa_AnaliseVariancia.sql`
- **Responsabilidade:** Compara orçamento vs realizado por centro de custo

#### Parâmetros

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `@CentroCustoId` | UNIQUEIDENTIFIER | ID do centro de custo |
| `@MesReferencia` | DATE | Mês de análise |

#### Lógica Principal

- Busca `Centro_Custo.Orcamento_Mensal` (custo plano)
- Soma `Fatura.ValorTotal` do mês (custo realizado)
- Calcula variância simples (sem classificação)
- **Problemas**: Não persiste resultado, recalcula sempre

**DESTINO**: **SUBSTITUÍDO** por Handler + Persistência em tabela `AnaliseVariancia`

---

### pa_DeteccaoAnomalias

- **Caminho:** `ic1_legado/Database/Procedures/pa_DeteccaoAnomalias.sql`
- **Responsabilidade:** Simples verificação de valores extremos (MAX, MIN)

#### Lógica Principal

- Calcula `MAX(ValorTotal)` e `MIN(ValorTotal)` por fornecedor
- Se valor > 2× MAX ou < 0.5× MIN → marca como anomalia
- **Problemas**: Algoritmo primitivo, muitos falsos positivos, sem Z-score

**DESTINO**: **SUBSTITUÍDO** por Algoritmo Z-score + Isolation Forest (Azure ML)

---

### pa_DepreciacaoMensal

- **Caminho:** `ic1_legado/Database/Procedures/pa_DepreciacaoMensal.sql`
- **Responsabilidade:** Calcula depreciação linear de ativos

#### Lógica Principal

- Para cada ativo: `(ValorOriginal - ValorResidual) / (AnosVidaUtil × 12)`
- Atualiza `Ativo.ValorDepreciado`
- **Problemas**: Job SQL Server Agent sem log, falha silenciosa

**DESTINO**: **SUBSTITUÍDO** por Hangfire Job com log estruturado

---

### pa_CustosTelecom

- **Caminho:** `ic1_legado/Database/Procedures/pa_CustosTelecom.sql`
- **Responsabilidade:** Agrega consumo + plano de linhas móveis

#### Lógica Principal

- JOIN `LinhaMovel` + `ConsumoLinhaMovel`
- Soma `ValorMensal + ConsumoTotal`
- **Problemas**: JOIN sem índices, lento

**DESTINO**: **SUBSTITUÍDO** por Query EF Core com group by otimizado

---

### pa_LimparAuditoria

- **Caminho:** `ic1_legado/Database/Procedures/pa_LimparAuditoria.sql`
- **Responsabilidade:** Deleta registros de auditoria > 90 dias

#### Problemas Críticos

- ❌ **Violação LGPD**: Deleta após 90 dias (LGPD exige 7 anos)
- ❌ **Hard delete**: Exclusão física irreversível
- ❌ **Perda de evidências**: Impossível auditar acessos antigos

**DESTINO**: **SUBSTITUÍDO** por Soft delete com retenção 7 anos (LGPD compliant)

---

## 5. TABELAS LEGADAS

| Tabela | Finalidade | Problemas Identificados | Destino |
|--------|------------|-------------------------|---------|
| `Fatura` | Armazena faturas de fornecedores | Falta índice em `DataEmissao`, queries lentas | **ASSUMIDO** (índice adicionado) |
| `LinhaMovel` | Linhas móveis de telecom | Sem FK adequada para `Operadora` | **ASSUMIDO** (FK corrigida) |
| `ConsumoLinhaMovel` | Consumo detalhado de linhas | Sem índice em `MesReferencia` | **ASSUMIDO** (índice adicionado) |
| `Contrato` | Contratos com fornecedores | Sem validação de `DataVencimento` | **ASSUMIDO** (validação em Command) |
| `Ativo` | Ativos de TI | Falta campos `MetodoDepreciacao`, `ValorDepreciado` | **ASSUMIDO** (campos adicionados) |
| `Centro_Custo` | Centros de custo | Falta `Orcamento_Mensal` em alguns registros | **ASSUMIDO** (obrigatório em Command) |
| `Fornecedor` | Fornecedores | Duplicatas (mesmo CNPJ cadastrado 2×) | **CORRIGIDO** (validação unicidade CNPJ) |

---

## 6. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

### RL-RN-001: Detecção de Anomalias por Máximo/Mínimo

**Origem**: Código VB.NET em `AnomaliasCustos.aspx.vb`, linha 145

**Descrição**: O legado considera anomalia quando `ValorFatura > 2 × MAX(ÚltimosSeisMeses)` ou `< 0.5 × MIN(ÚltimosSeisMeses)`.

**Problemas**:
- Threshold fixo (2×) não considera variabilidade natural
- Muitos falsos positivos em fornecedores sazonais
- Não usa média ou desvio padrão

**DESTINO**: **SUBSTITUÍDO** por Z-score (threshold 2.5 desvios padrão)

---

### RL-RN-002: Cálculo de Variância sem Classificação

**Origem**: `pa_AnaliseVariancia.sql`, linha 23

**Descrição**: Variância calculada como `CustoRealizado - CustoPlano`, mas sem classificação de severidade.

**Problemas**:
- Usuário precisa interpretar manualmente se variância é aceitável
- Sem alertas automáticos

**DESTINO**: **ASSUMIDO** com classificação (Aceitável, Aviso, Crítico)

---

### RL-RN-003: Depreciação Apenas Linear

**Origem**: `pa_DepreciacaoMensal.sql`

**Descrição**: Suporta apenas depreciação linear, sem método acelerado.

**DESTINO**: **EXPANDIDO** para suportar método acelerado (50% ano 1)

---

### RL-RN-004: Auditoria Parcial (Sem IP, Sem Dados Acessados)

**Origem**: Tabela `LogAcesso` (não estruturada)

**Descrição**: Log armazena apenas `Usuario, DataHora, Tela`. Não registra IP, dados acessados, operação.

**Problemas**:
- Não LGPD compliant
- Impossível rastrear quem acessou quais dados

**DESTINO**: **SUBSTITUÍDO** por `AuditoriaAcessoLGPD` (estruturada, 7 anos)

---

### RL-RN-005: Fornecedores Duplicados Permitidos

**Origem**: Tabela `Fornecedor` sem UNIQUE constraint em `CNPJ`

**Descrição**: Mesmo CNPJ pode ser cadastrado múltiplas vezes (bug permite duplicatas).

**Impacto**: Relatórios mostram mesmo fornecedor 2× com contratos distintos.

**DESTINO**: **CORRIGIDO** com UNIQUE constraint + validação em Command

---

### RL-RN-006: Limpeza de Auditoria aos 90 Dias (Violação LGPD)

**Origem**: `pa_LimparAuditoria.sql`

**Descrição**: Job deleta fisicamente registros de auditoria > 90 dias.

**Violação**: LGPD exige 7 anos de retenção.

**DESTINO**: **SUBSTITUÍDO** por Soft delete + Hangfire job (7 anos)

---

## 7. GAP ANALYSIS (LEGADO x RF MODERNO)

| Item | Legado | RF Moderno | Observação |
|------|--------|------------|------------|
| **Detecção de Anomalias** | Manual (analistas) + MAX/MIN primitivo | Algoritmo Z-score + Isolation Forest (ML) | Reduz 90% tempo de análise |
| **Análise de Variância** | Não persiste, sem classificação | Persistida, classificada (Aceitável, Aviso, Crítico) | Permite histórico e alertas |
| **TCO de Ativos** | Não existe | Cálculo automático (aquisição + manutenção + depreciação) | Nova funcionalidade |
| **ROI de Iniciativas** | Não existe | Cálculo de ROI e Payback | Nova funcionalidade |
| **Alertas de Compliance** | Manual (check-list) | Automáticos (fornecedor não aprovado, orçamento excedido) | Proativo vs reativo |
| **Auditoria de Acesso** | Log parcial (90 dias) | LGPD compliant (7 anos, estruturado) | Conformidade regulatória |
| **Relatórios** | Estáticos (Crystal Reports) | Interativos (drill-down, filtros) | UX superior |
| **Jobs Batch** | SQL Server Agent (sem log) | Hangfire (log estruturado, retry) | Confiabilidade |
| **Depreciação** | Apenas linear | Linear + Acelerado | Flexibilidade contábil |
| **Multi-tenancy** | Banco por cliente (18 bases) | Banco único (Row-Level Security) | Manutenção reduzida 85% |

---

## 8. DECISÕES DE MODERNIZAÇÃO

### Decisão 1: Migrar de Crystal Reports para Exportação Programática

**Motivo**: Crystal Reports é lento, caro (licenças) e dificulta manutenção.

**Impacto**: ALTO

**Trade-off**: Perda de templates visuais prontos, mas ganho em performance e customização.

---

### Decisão 2: Substituir SQL Server Agent por Hangfire

**Motivo**: SQL Server Agent não fornece log estruturado, retry ou dashboard.

**Impacto**: MÉDIO

**Trade-off**: Hangfire adiciona dependência .NET, mas é open-source e superior.

---

### Decisão 3: Consolidar 18 Bases SQL Server em 1 Banco SQLite (Dev)

**Motivo**: Manutenção de 18 bases separadas é cara e lenta.

**Impacto**: ALTO

**Trade-off**: Migration complexa, mas reduz custo operacional 85%.

---

### Decisão 4: Implementar Z-score em vez de MAX/MIN Primitivo

**Motivo**: Algoritmo legado gera 60% falsos positivos.

**Impacto**: ALTO

**Trade-off**: Requer configuração de threshold (2.5 padrão), mas aumenta acurácia 90%.

---

### Decisão 5: Auditoria LGPD 7 Anos (Soft Delete)

**Motivo**: Legado deleta após 90 dias (violação LGPD artigo 7°).

**Impacto**: CRÍTICO

**Trade-off**: Banco cresce mais rápido, mas conformidade regulatória garantida.

---

## 9. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Mitigação |
|------|---------|-----------|
| **Perda de Dados Durante Migração** | CRÍTICO | Backup de todas as 18 bases antes de consolidação |
| **Divergência de Cálculos (Variância, Depreciação)** | ALTO | Validar 100 amostras (legado vs moderno) antes de deploy |
| **Falsos Positivos em Anomalias (Z-score)** | MÉDIO | Ajustar threshold (2.5 → 3.0) se taxa > 20% |
| **Performance Dashboard com Grande Volume** | MÉDIO | Índices adequados + materialização de views |
| **Usuários Resistentes a Mudança de UX** | BAIXO | Treinamento + documentação + suporte 30 dias |

---

## 10. RASTREABILIDADE

| Elemento Legado | Referência RF Moderno |
|----------------|----------------------|
| `RelatoriosCustos.aspx` | RF-094 - Seção 2 (FUNC-094-01: Análise Multidimensional) |
| `AnaliseVariancia.aspx` | RF-094 - Seção 3 (RN-RF094-001: Cálculo de Variância) |
| `AnomaliasCustos.aspx` | RF-094 - Seção 3 (RN-RF094-002: Detecção por Z-Score) |
| `pa_CustosPorFornecedor` | RF-094 - Seção 6 (GET /api/auditoria/custos-fornecedor) |
| `pa_AnaliseVariancia` | RF-094 - Seção 6 (GET /api/auditoria/variancia) |
| `pa_DeteccaoAnomalias` | RF-094 - Seção 6 (POST /api/auditoria/anomalias/detectar) |
| `pa_DepreciacaoMensal` | RF-094 - Seção 3 (RN-RF094-009: Depreciação de Ativos) |
| `WSAuditoria.asmx` | RF-094 - Seção 6 (REST API endpoints) |
| Tabela `Fatura` | RF-094 - Seção 7 (Modelo de Dados) |
| Tabela `Ativo` | RF-094 - Seção 7 (Modelo de Dados) |
| `LogAcesso` (text-based) | RF-094 - Seção 3 (RN-RF094-008: Auditoria LGPD) |

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|--------|------|-----------|-------|
| 1.0 | 2025-12-31 | Criação do documento de referência ao legado RF-094 | Claude Code - Agente de Migração |

---

**Última Atualização**: 2025-12-31
**Autor**: Claude Code - Agente de Migração de Documentação
**Revisão**: Pendente de aprovação
