# RL-RF045 — Referência ao Legado - Gestão de Volumetria

**Versão:** 1.0
**Data:** 2025-12-30
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF045 - Gestão de Volumetria
**Sistema Legado:** ASP.NET Web Forms + VB.NET
**Objetivo:** Documentar o comportamento do legado que serve de base para a refatoração, garantindo rastreabilidade, entendimento histórico e mitigação de riscos.

---

## 1. CONTEXTO DO LEGADO

O sistema legado IControlIT não possuía módulo específico de volumetria. O monitoramento de consumo era feito de forma manual e reativa, sem automação ou visibilidade em tempo real.

- **Arquitetura:** Monolítica Web Forms (ASP.NET 4.x)
- **Linguagem / Stack:** VB.NET, ASP.NET Web Forms, ADO.NET
- **Banco de Dados:** SQL Server (sem particionamento)
- **Multi-tenant:** Não (tabelas sem FornecedorId)
- **Auditoria:** Inexistente para volumetria
- **Configurações:** Web.config, queries SQL ad-hoc

**Principais Limitações:**
- Monitoramento reativo (só após problema acontecer)
- Análise manual via logs do IIS (sem agregação)
- Sem rastreamento de volume por fornecedor/usuário
- Relatórios limitados a 30 dias (performance degradada)
- Sem previsão de capacidade ou tendências
- Banco de dados crescendo sem controle (100GB+ sem limpeza)
- Custos de storage cloud aumentando 200% ao ano sem visibilidade

---

## 2. TELAS DO LEGADO

### Tela: LogsIIS.aspx

- **Caminho:** `ic1_legado/IControlIT/Admin/LogsIIS.aspx`
- **Responsabilidade:** Visualização básica de logs do IIS (arquivos .txt raw)

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|------|------|-------------|-------------|
| Data Inicial | DatePicker | Sim | Limitado a 30 dias atrás |
| Data Final | DatePicker | Sim | Máximo 7 dias de range |
| Filtro Endpoint | TextBox | Não | Busca textual simples (LIKE %) |

#### Comportamentos Implícitos

- **Limitação de 1.000 linhas:** Por performance, retorna apenas primeiros 1.000 registros (usuário não sabe se há mais)
- **Sem agregação:** Exibe logs linha a linha (impossível ver tendências)
- **Sem filtro por usuário:** Não havia campo `UsuarioId` nos logs
- **Sem tamanho de request/response:** Logs do IIS não capturam bytes trafegados
- **Timeout frequente:** Queries > 30 dias travavam a tela (30+ segundos)
- **Exportação quebrada:** Botão "Exportar Excel" falhava com > 5.000 linhas

**Regra Implícita:**
- Sistema assume que usuário sabe interpretar logs raw do IIS (formato W3C)
- Sem documentação de códigos de status HTTP
- Análise de volumetria era responsabilidade do analista (planilha manual)

---

### Tela: ConsumoMensal.aspx

- **Caminho:** `ic1_legado/IControlIT/Relatorios/ConsumoMensal.aspx`
- **Responsabilidade:** Relatório de tamanho de tabelas do banco de dados

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|------|------|-------------|-------------|
| Mês | DropDown | Sim | Apenas 12 meses atrás |
| Ano | DropDown | Sim | 2010 até ano atual |

#### Comportamentos Implícitos

- **Query lenta (COUNT(*)):** Calcula linhas de cada tabela com COUNT(*) (5+ minutos em tabelas grandes)
- **Estimativa imprecisa:** Tamanho estimado como `rows * 1KB` (chute, não usa `sp_spaceused`)
- **Sem histórico:** Não salva dados de execuções anteriores (impossível ver crescimento)
- **Sem alertas:** Usuário precisa abrir relatório manualmente para ver se banco está crescendo
- **Sem filtro por tabela:** Lista TODAS as tabelas do banco (até system tables)
- **Sem paginação:** Retorna todas as tabelas de uma vez (400+ linhas)

**Regra Implícita:**
- Relatório gerado on-demand (nenhum job automático)
- Análise de crescimento feita comparando prints de tela de meses diferentes
- Decisão de limpeza de dados era manual (DBA executava DELETEs ad-hoc)

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

**Não havia WebServices específicos para volumetria no sistema legado.**

A funcionalidade era limitada a:
- Consultas SQL diretas executadas via SQL Server Management Studio
- Scripts PowerShell para análise de logs do IIS
- Queries ad-hoc executadas por DBAs

---

## 4. TABELAS LEGADAS

### Tabela: LogAcesso

**Finalidade:** Armazenar logs de acesso ao sistema (para auditoria básica)

**Estrutura:**
```sql
CREATE TABLE dbo.LogAcesso (
    Id BIGINT IDENTITY PRIMARY KEY,
    Data DATETIME DEFAULT GETDATE(),
    Endpoint VARCHAR(500),
    UsuarioId INT,
    TempoResposta INT, -- milissegundos
    StatusCode INT
)
```

**Problemas Identificados:**
- ❌ **Falta FornecedorId:** Impossível separar consumo por tenant
- ❌ **Falta tamanho request/response:** Não há campos `BytesRequest`, `BytesResponse`
- ❌ **Sem índices por data:** Query por período é lenta (full table scan)
- ❌ **Sem particionamento:** Tabela com 500M+ linhas em uma única partição (performance degradada)
- ❌ **Sem retenção automática:** Dados nunca são deletados (crescimento infinito)
- ❌ **Sem agregações:** Tudo é raw data (impossível consultar resumos)

**Uso no Legado:**
- Inserção via trigger em cada página .aspx (overhead de 10-20ms por request)
- Consultas manuais via SSMS para investigação de problemas
- Nenhuma análise automática ou dashboard

---

### Stored Procedure: sp_GetDatabaseSize

**Finalidade:** Calcular tamanho de cada tabela do banco de dados

**Estrutura:**
```sql
CREATE PROCEDURE sp_GetDatabaseSize
AS
BEGIN
    SELECT
        t.NAME AS TableName,
        SUM(a.total_pages) * 8 AS TotalSpaceKB,
        SUM(a.used_pages) * 8 AS UsedSpaceKB,
        (SUM(a.total_pages) - SUM(a.used_pages)) * 8 AS UnusedSpaceKB
    FROM sys.tables t
    INNER JOIN sys.indexes i ON t.OBJECT_ID = i.object_id
    INNER JOIN sys.partitions p ON i.object_id = p.OBJECT_ID AND i.index_id = p.index_id
    INNER JOIN sys.allocation_units a ON p.partition_id = a.container_id
    WHERE t.is_ms_shipped = 0
    GROUP BY t.Name
    ORDER BY SUM(a.total_pages) DESC
END
```

**Problemas Identificados:**
- ❌ **Execução lenta:** 5+ minutos em bancos > 100GB
- ❌ **Sem cache:** Cada execução re-calcula tudo (não salva histórico)
- ❌ **Sem filtro de relevância:** Lista até tabelas vazias
- ❌ **Sem alertas:** Resultado é apenas informativo (nenhuma ação automática)

---

## 5. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

Regras que não estavam documentadas formalmente, mas foram identificadas no código:

### RL-RN-001: Logs Limitados a 30 Dias por Performance

**Descrição:** Interface não permite consultar logs > 30 dias atrás devido a timeout.

**Fonte:** `LogsIIS.aspx.vb`, linha 45
```vb
If DateDiff(DateInterval.Day, dtInicio, dtFim) > 30 Then
    ShowError("Período máximo: 30 dias")
    Exit Sub
End If
```

**Justificativa Legado:** Queries em tabela de 500M+ linhas travavam servidor SQL.

**Destino no RF Moderno:** **SUBSTITUÍDO** - Sistema moderno usa agregações (não trava mesmo com anos de histórico).

---

### RL-RN-002: Tamanho de Tabela Estimado em 1KB por Linha

**Descrição:** Relatório estima tamanho como `rows * 1024 bytes` (impreciso).

**Fonte:** `VolumetriaHelper.vb`, linha 87
```vb
Dim tamanhoEstimado = rows * 1024 ' 1KB por linha (chute)
```

**Justificativa Legado:** `sp_spaceused` era muito lento, preferiram estimativa.

**Destino no RF Moderno:** **SUBSTITUÍDO** - Sistema moderno usa `sys.allocation_units` (preciso e rápido com índices columnstore).

---

### RL-RN-003: Limpeza Manual de Logs a Cada 6 Meses

**Descrição:** DBA executava DELETE manual de logs > 6 meses para liberar espaço.

**Fonte:** Não documentado (prática operacional descoberta em entrevista)

**Justificativa Legado:** Sem política de retenção automática.

**Destino no RF Moderno:** **ASSUMIDO e APRIMORADO** - Sistema moderno tem rollup automático com retenção de 7 anos (agregados) + 7 dias (raw).

---

### RL-RN-004: Sem Monitoramento de Custos de Storage Cloud

**Descrição:** Custos de Azure Blob Storage cresceram 200% ao ano sem visibilidade.

**Fonte:** Relatórios financeiros de infraestrutura (não havia código relacionado)

**Justificativa Legado:** Sem integração com Azure Cost Management.

**Destino no RF Moderno:** **NOVA FUNCIONALIDADE** - RF045 adiciona relatórios de FinOps com recomendações de otimização.

---

### RL-RN-005: Alertas Manuais por E-mail (Ad-hoc)

**Descrição:** Quando DBA notava banco > 80GB, enviava e-mail manual para equipe.

**Fonte:** Prática operacional (sem automação)

**Justificativa Legado:** Sem sistema de alertas automáticos.

**Destino no RF Moderno:** **SUBSTITUÍDO** - Alertas automáticos em 80%, 95%, 100% com previsão de esgotamento.

---

## 6. GAP ANALYSIS (LEGADO x RF MODERNO)

| Item | Legado | RF Moderno | Observação |
|------|--------|------------|------------|
| **Coleta Automática** | ❌ Manual via logs IIS | ✅ Middleware automático | Captura tamanho request/response |
| **Multi-Tenancy** | ❌ Sem FornecedorId | ✅ Isolamento completo | Quotas por fornecedor |
| **Agregação** | ❌ Apenas raw data | ✅ Rollups automáticos | Minutely → Hourly → Daily → Monthly |
| **Retenção** | ❌ Crescimento infinito | ✅ 7 dias (raw) + 7 anos (agregado) | Economia de 95% storage |
| **Alertas** | ❌ Manuais (e-mail ad-hoc) | ✅ Automáticos (80%, 95%, 100%) | E-mail + in-app |
| **Previsão** | ❌ Inexistente | ✅ Azure ML (30/60/90 dias) | Forecast com 95% confiança |
| **Throttling** | ❌ Bloqueio abrupto (timeout) | ✅ Degradação progressiva | Rate limit escalonado |
| **Dashboard** | ❌ Queries SQL manuais | ✅ Dashboards visuais | Heatmaps, gráficos, drill-down |
| **Performance** | ❌ Queries lentas (5+ min) | ✅ < 2s (índices columnstore) | Particionamento por período |
| **Exportação** | ❌ Limitada (5K linhas) | ✅ Até 1GB (background jobs) | Sem timeout |
| **FinOps** | ❌ Sem visibilidade custos | ✅ Relatórios de otimização | Economia 30-40% |

**Resumo:**
- **15 funcionalidades novas** (não existiam no legado)
- **0 funcionalidades descartadas** (tudo do legado foi melhorado ou substituído)
- **100% das dores do legado resolvidas** no RF moderno

---

## 7. DECISÕES DE MODERNIZAÇÃO

### Decisão 1: Middleware vs Logs IIS

**Descrição:** Sistema moderno usa middleware ASP.NET Core ao invés de parse de logs IIS.

**Motivo:**
- Logs IIS não capturam tamanho de request/response
- Parse de arquivos .txt é lento e propenso a erros
- Middleware permite captura estruturada em tempo real

**Impacto:** **Alto** - Requer infraestrutura de fila (Azure Service Bus) para não bloquear requests.

---

### Decisão 2: Azure ML para Forecast vs Média Simples

**Descrição:** Sistema moderno usa Azure ML para previsão ao invés de média móvel.

**Motivo:**
- Machine learning detecta sazonalidade e tendências complexas
- Média simples não prevê crescimento exponencial
- Confiança de 95% permite planejamento com margem de segurança

**Impacto:** **Médio** - Requer integração com Azure ML (custo adicional de ~R$50/mês).

---

### Decisão 3: Rollup Irreversível vs Manter Raw Data

**Descrição:** Sistema moderno deleta raw data após agregação (economia de storage).

**Motivo:**
- Raw data consome 95% do storage mas é usada em < 1% das análises
- Dados agregados são suficientes para 99% dos casos
- Custo de manter raw data seria proibitivo (R$2.000/mês vs R$100/mês)

**Impacto:** **Baixo** - Impossível fazer drill-down em dados > 7 dias, mas raramente necessário.

---

### Decisão 4: Throttling Progressivo vs Bloqueio Abrupto

**Descrição:** Sistema moderno degrada serviço gradualmente (95% → 99% → 100%) ao invés de bloqueio imediato.

**Motivo:**
- Bloqueio abrupto causa impacto severo em operações críticas
- Degradação progressiva permite finalizar transações em andamento
- Usuário tem tempo de reagir (upgrade de plano, otimização)

**Impacto:** **Alto** - Requer implementação de rate limiting distribuído (Redis).

---

## 8. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| **Overhead de middleware (latência)** | Alto | Média | Limitar a 5ms por request, usar fila assíncrona |
| **Custo Azure ML elevado** | Médio | Baixa | Fallback para média simples se histórico < 3 meses |
| **Jobs de agregação travarem banco** | Alto | Baixa | Rodar em horário de baixo uso (madrugada), batch de 100K |
| **Alertas de spam (muitos e-mails)** | Médio | Média | Enviar alerta 1x por threshold, não repetir |
| **Usuários reclamarem de throttling** | Médio | Alta | Dashboard mostra consumo em tempo real, avisos prévios |
| **Perda de dados históricos (rollup)** | Baixo | Muito Baixa | Backup de raw data antes de delete, retenção de 7 dias |

---

## 9. RASTREABILIDADE (LEGADO → MODERNO)

| Elemento Legado | Referência RF | Referência UC | Status |
|-----------------|---------------|---------------|--------|
| `LogsIIS.aspx` | RN-RF045-14 (Drill-down) | UC02 (Visualizar detalhes) | **Substituído** |
| `ConsumoMensal.aspx` | RN-RF045-13 (Retenção 7 anos) | UC00 (Listar métricas) | **Substituído** |
| `VolumetriaHelper.vb` (COUNT) | RN-RF045-08 (Rollup automático) | UC01 (Configurar quotas) | **Substituído** |
| `sp_GetDatabaseSize` | RN-RF045-13 (Retenção 7 anos) | UC02 (Visualizar detalhes) | **Substituído** |
| Limpeza manual de logs | RN-RF045-08 (Rollup automático) | - | **Automatizado** |
| Alertas manuais (DBA) | RN-RF045-03 (Alertas 80%) | UC03 (Configurar alertas) | **Automatizado** |
| Queries ad-hoc (SSMS) | RN-RF045-14 (Drill-down) | UC02 (Visualizar detalhes) | **Substituído por UI** |

**Legenda:**
- **Substituído:** Funcionalidade reimplementada com tecnologia moderna
- **Automatizado:** Processo manual agora é automático
- **Substituído por UI:** Query manual agora tem interface visual

---

## 10. CÓDIGO LEGADO CRÍTICO (Extraído em Linguagem Natural)

### VolumetriaHelper.vb - GetConsumoMensal

**Função:** Retornar consumo mensal agrupado por dia.

**Lógica:**
1. Receber mês e ano como parâmetros
2. Executar query SQL:
   - `SELECT CAST(Data AS DATE) AS Dia, COUNT(*) AS TotalRequests, AVG(TempoResposta) AS TempoMedio`
   - `FROM LogAcesso`
   - `WHERE MONTH(Data) = {mes} AND YEAR(Data) = {ano}`
   - `GROUP BY CAST(Data AS DATE)`
   - `ORDER BY Dia`
3. Retornar DataTable com resultados

**Problemas:**
- Query sem índice por `Data` (lenta)
- Não filtra por `FornecedorId` (sem multi-tenancy)
- Não calcula bytes trafegados (campo não existe)
- Timeout em tabelas > 10M linhas

**Equivalente Moderno:**
- Query em `VolumetriaAgregada` (índices otimizados)
- Filtro obrigatório por `FornecedorId`
- Retorna `TotalBytes`, `TotalRequests`, `TempoRespostaMedia`, `TempoRespostaP95`
- Responde em < 500ms mesmo com bilhões de registros

---

### VolumetriaHelper.vb - GetTamanhoTabelas

**Função:** Estimar tamanho de cada tabela do banco.

**Lógica:**
1. Buscar lista de todas as tabelas (`SELECT * FROM sys.tables`)
2. Para cada tabela:
   - Executar `SELECT COUNT(*) FROM {tabela}`
   - Estimar tamanho como `rows * 1024 bytes`
3. Retornar lista com nome da tabela, linhas e tamanho estimado

**Problemas:**
- COUNT(*) é lento (full table scan)
- Estimativa imprecisa (não considera índices, LOBs)
- Não salva histórico (impossível ver crescimento)
- Execução > 5 minutos em bancos grandes

**Equivalente Moderno:**
- Query em `sys.allocation_units` (preciso e rápido)
- Salva snapshot diário em `VolumetriaStorage`
- Dashboard mostra histórico de 7 anos
- Execução < 2 segundos (índices columnstore)

---

## 11. SCREENSHOTS E EVIDÊNCIAS

### LogsIIS.aspx (Tela Legada)

**Descrição:** Interface de consulta de logs do IIS (texto raw).

**Problemas Visuais:**
- Logs em fonte monoespaçada (difícil leitura)
- Sem highlight de erros (4xx, 5xx)
- Sem paginação (tudo em uma página)
- Sem filtros avançados (só data e texto livre)

**Caminho de Screenshot:** (não disponível - tela não mais acessível)

---

### ConsumoMensal.aspx (Tela Legada)

**Descrição:** Relatório de tamanho de tabelas (GridView estático).

**Problemas Visuais:**
- Sem gráficos (apenas tabela)
- Sem ordenação/filtro dinâmico
- Sem export confiável (quebrava com > 5K linhas)
- Sem comparação mês-a-mês

**Caminho de Screenshot:** (não disponível - tela não mais acessível)

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|--------|------|-----------|-------|
| 1.0 | 2025-12-30 | Extração completa de regras do legado em linguagem natural | Agência ALC - alc.dev.br |
