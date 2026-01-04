# RL-RF103 — Referência ao Legado (Relatórios e Volumetria)

**Versão:** 1.0
**Data:** 2025-12-31
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF-103 - Relatórios e Volumetria
**Sistema Legado:** IControl Legado (VB.NET + ASP.NET Web Forms)
**Objetivo:** Documentar o comportamento do módulo de volumetria legado, garantindo rastreabilidade e memória técnica para decisões de modernização.

---

## 1. CONTEXTO DO SISTEMA LEGADO

### 1.1 Informações Gerais

- **Arquitetura**: Monolítica Cliente-Servidor com Web Forms
- **Linguagem / Stack**: VB.NET + ASP.NET Web Forms + Crystal Reports
- **Banco de Dados**: SQL Server (um banco por cliente - multi-database)
- **Multi-tenant**: Sim, porém com banco de dados isolado por cliente (1 cliente = 1 banco)
- **Auditoria**: Inexistente para acessos a relatórios
- **Configurações**: Web.config + configurações em banco de dados

### 1.2 Problemas Arquiteturais Identificados

1. **Performance Crítica**: Crystal Reports travava com > 500k registros, gerando relatórios de 30+ segundos
2. **Multi-database Complexo**: Cada cliente tinha banco próprio, dificultando consultas agregadas e manutenção
3. **Falta de Cache**: Nenhuma estratégia de cache, recalculava volumetrias a cada acesso
4. **Processamento Síncrono**: Relatórios grandes travavam browser do usuário, causando timeouts HTTP
5. **Sem Consolidação**: Volumetrias sempre calculadas on-demand, sobrecarregando banco em horário comercial
6. **Auditoria Ausente**: Impossível rastrear quem acessou relatórios de volumetria (falha de conformidade)
7. **Export Limitado**: Excel XLS com limite de 65.536 linhas (não suportava grandes volumes)
8. **Sem Comparativos Temporais**: Não havia funcionalidade de comparar períodos (mês vs mês, ano vs ano)
9. **Permissões Coarse-grained**: Usuário tinha acesso total ou bloqueio total (sem granularidade)

---

## 2. TELAS ASPX DO LEGADO

### 2.1 Tela: RelatorioVolumetria.aspx

**Caminho:** `D:\IC2\ic1_legado\IControlIT\Relatorios\RelatorioVolumetria.aspx`

**Responsabilidade:** Tela principal de consulta de volumetria com filtros de período e geração de relatório em Crystal Reports.

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| `txtDataInicio` | TextBox (Data) | Sim | Data início do período sem validação de formato |
| `txtDataFim` | TextBox (Data) | Sim | Data fim sem validação se > data início |
| `ddlTipoRelatorio` | DropDownList | Sim | Valores: Chamados, Ativos, Usuários, Contratos |
| `btnGerar` | Button | - | Dispara geração síncrona do relatório |

#### Comportamentos Implícitos

- Botão "Gerar" bloqueava interface por 30-90 segundos enquanto Crystal Reports processava
- Sem loading spinner ou feedback visual de progresso
- Timeout HTTP após 90 segundos causava perda do relatório gerado
- Não validava se período estava finalizado antes de comparar
- Crystal Reports carregava TODOS os registros em memória antes de agregar (problema crítico)

**Destino:** **SUBSTITUÍDO** - Substituído por componente Angular com processamento assíncrono e feedback visual

**Rastreabilidade:**
- RF Moderno: RF-103 - Seção 4 (Funcionalidades)
- UC Moderno: UC01-RF103 (Consultar Volumetria)
- Componente Angular: `volumetria-relatorio.component.ts`
- Rota Frontend: `/relatorios/volumetria`

---

### 2.2 Tela: ComparativoTemporal.aspx

**Caminho:** `D:\IC2\ic1_legado\IControlIT\Relatorios\ComparativoTemporal.aspx`

**Responsabilidade:** Comparativo básico mês vs mês (funcionalidade parcial).

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| `ddlMes` | DropDownList | Sim | Mês de referência |
| `ddlAno` | DropDownList | Sim | Ano de referência |
| `btnComparar` | Button | - | Gera comparativo |

#### Comportamentos Implícitos

- Comparava apenas meses finalizados (regra correta)
- Mas não verificava se dados do mês anterior existiam (falha)
- Não calculava variação percentual automaticamente
- Exibia apenas valores absolutos (usuário tinha que calcular manualmente)

**Destino:** **ASSUMIDO** - Regra de períodos finalizados mantida em RN-RF103-003

**Rastreabilidade:**
- RF Moderno: RF-103 - RN-RF103-003
- UC Moderno: UC03-RF103 (Comparativo Temporal)
- Componente Angular: `volumetria-comparativo.component.ts`
- Rota Frontend: `/relatorios/volumetria/comparativo`

---

### 2.3 Tela: Top10.aspx

**Caminho:** `D:\IC2\ic1_legado\IControlIT\Relatorios\Top10.aspx`

**Responsabilidade:** Ranking top 10 por filiais (hardcoded apenas para filiais).

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| `txtPeriodo` | TextBox | Sim | Período fixo (não permitia customização) |
| `btnGerar` | Button | - | Gerava top 10 filiais |

#### Comportamentos Implícitos

- Hardcoded para filiais apenas (não permitia top 10 por departamento, centro de custo, etc.)
- Ordenação descendente (correto)
- Não calculava percentual do total
- Exibia apenas volume absoluto

**Destino:** **SUBSTITUÍDO** - Modernizado para permitir top 10 por qualquer dimensão (filial, depto, CC, responsável)

**Rastreabilidade:**
- RF Moderno: RF-103 - RN-RF103-004
- UC Moderno: UC04-RF103 (Top 10)
- API Moderna: GET `/api/volumetria/top10/{tipo}`

---

### 2.4 Tela: ExportExcel.aspx

**Caminho:** `D:\IC2\ic1_legado\IControlIT\Relatorios\ExportExcel.aspx`

**Responsabilidade:** Export de volumetria para Excel XLS (formato antigo).

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| `btnExportar` | Button | - | Dispara export |

#### Comportamentos Implícitos

- Usava formato XLS (limite 65.536 linhas)
- Falhava silenciosamente se volume > 65k (truncava dados sem avisar)
- Não tinha aba de resumo executivo
- Gerava apenas uma aba única com todos dados misturados

**Destino:** **SUBSTITUÍDO** - Modernizado para XLSX ilimitado com abas de resumo + detalhes

**Rastreabilidade:**
- RF Moderno: RF-103 - RN-RF103-008
- API Moderna: POST `/api/volumetria/export/excel`

---

## 3. WEBSERVICES (.asmx) DO LEGADO

### 3.1 Webservice: WSVolumetria.asmx

**Caminho:** `D:\IC2\ic1_legado\IControlIT\WebService\WSVolumetria.asmx.vb`

**Métodos Públicos:**

| Método | Parâmetros | Retorno | Observações |
|--------|-----------|---------|-------------|
| `ObterVolumetriaChamados()` | `idCliente As Integer, dataInicio As Date, dataFim As Date` | `DataTable` | Retornava DataTable sem tipagem |
| `ObterTop10Filiais()` | `idCliente As Integer, periodo As String` | `DataTable` | Hardcoded para filiais |
| `ObterComparativoMesVsMes()` | `idCliente As Integer, mes As Integer, ano As Integer` | `DataTable` | Sem validação de período finalizado |
| `ExportarExcel()` | `idCliente As Integer, dados As DataTable` | `String (caminho arquivo)` | Salvava arquivo em servidor (problema de concorrência) |

**Comportamentos Implícitos:**

- Nenhuma validação de permissões (qualquer usuário autenticado acessava)
- Sem filtro multi-tenancy explícito (confiava no `idCliente` passado pelo frontend)
- Retornava DataTable não tipado (problema de manutenção)
- Processamento síncrono bloqueava thread IIS

**Destino:** **SUBSTITUÍDO** - Substituído por REST API com tipagem forte, RBAC e processamento assíncrono

**Rastreabilidade:**
- RF Moderno: RF-103 - Seção 10 (API Endpoints)
- Endpoints Modernos:
  - `ObterVolumetriaChamados()` → GET `/api/volumetria/chamados`
  - `ObterTop10Filiais()` → GET `/api/volumetria/top10/filial`
  - `ObterComparativoMesVsMes()` → GET `/api/volumetria/comparativo?tipo=mes`
  - `ExportarExcel()` → POST `/api/volumetria/export/excel`

---

## 4. STORED PROCEDURES DO LEGADO

### 4.1 Procedure: pa_sp_volumetria_chamados

**Caminho:** `D:\IC2\ic1_legado\Database\Procedures\pa_sp_volumetria_chamados.sql`

**Parâmetros de Entrada:**
```sql
@id_cliente INT,
@dt_inicio DATETIME,
@dt_fim DATETIME
```

**Parâmetros de Saída:**
```sql
-- Retorna ResultSet (SELECT)
```

**Lógica Principal (em linguagem natural):**

1. Filtrava chamados por `id_cliente`, `dt_criacao` entre `@dt_inicio` e `@dt_fim`
2. Agregava por tipo, prioridade e status usando COUNT(*)
3. Retornava resultado como SELECT múltiplas linhas
4. NÃO utilizava índices otimizados (tabela completa scanned)
5. NÃO tratava timezone (assumia sempre GMT-3)

**Problemas Identificados:**

- Table scan completo (> 1M registros = 30+ segundos)
- Sem índice em `dt_criacao` + `id_cliente`
- Sem paginação (retornava TODOS registros)

**Destino:** **SUBSTITUÍDO** - Substituído por Query LINQ nativa com índices otimizados

**Rastreabilidade:**
- RF Moderno: RF-103 - RN-RF103-001
- Query Moderna: `VolumetriaQueryHandler.GetVolumetriaChamados()` (LINQ to SQL)

---

### 4.2 Procedure: pa_sp_top10_filiais

**Caminho:** `D:\IC2\ic1_legado\Database\Procedures\pa_sp_top10_filiais.sql`

**Parâmetros de Entrada:**
```sql
@id_cliente INT,
@periodo VARCHAR(20)
```

**Lógica Principal:**

1. Parseava `@periodo` manualmente (formato "2025-12")
2. Agregava chamados por filial usando GROUP BY
3. Ordenava descendente por COUNT(*)
4. Limitava a 10 resultados com TOP 10

**Problemas Identificados:**

- Parse manual de string para data (error-prone)
- Hardcoded apenas para filiais (não reutilizável)
- Sem cálculo de percentual do total

**Destino:** **SUBSTITUÍDO** - Substituído por agregação SQL genérica com parâmetro de dimensão

**Rastreabilidade:**
- RF Moderno: RF-103 - RN-RF103-004
- Query Moderna: `VolumetriaQueryHandler.GetTop10(tipo, dimensao)` (dinâmico)

---

### 4.3 Procedure: pa_sp_comparativo_temporal

**Caminho:** `D:\IC2\ic1_legado\Database\Procedures\pa_sp_comparativo_temporal.sql`

**Parâmetros de Entrada:**
```sql
@id_cliente INT,
@mes INT,
@ano INT
```

**Lógica Principal:**

1. Calculava início/fim do mês atual
2. Calculava início/fim do mês anterior
3. Executava duas queries separadas (COUNT para cada mês)
4. Retornava dois valores (mês atual, mês anterior)
5. Frontend calculava variação percentual

**Problemas Identificados:**

- Não validava se mês estava finalizado
- Não verificava se mês anterior tinha dados
- Cálculo de variação % no frontend (inconsistente)

**Destino:** **ASSUMIDO** parcialmente - Validação de período finalizado mantida, cálculo % movido para backend

**Rastreabilidade:**
- RF Moderno: RF-103 - RN-RF103-003
- Query Moderna: `VolumetriaQueryHandler.GetComparativoTemporal(ano, mes)`

---

### 4.4 Procedure: pa_sp_tendencia_30dias

**Caminho:** `D:\IC2\ic1_legado\Database\Procedures\pa_sp_tendencia_30dias.sql`

**Parâmetros de Entrada:**
```sql
@id_cliente INT
```

**Lógica Principal:**

1. Retornava volumetria diária dos últimos 30 dias
2. NÃO calculava média móvel (frontend exibia valores brutos)
3. Ordenação por data

**Problemas Identificados:**

- Valores brutos sem suavização (difícil identificar tendência)
- Frontend exibia linha com muita oscilação (ruído)

**Destino:** **SUBSTITUÍDO** - Substituído por cálculo de média móvel 7 dias no backend

**Rastreabilidade:**
- RF Moderno: RF-103 - RN-RF103-005
- Query Moderna: `VolumetriaQueryHandler.GetTendencia()` com média móvel 7d

---

### 4.5 Procedure: pa_sp_export_volumetria_excel

**Caminho:** `D:\IC2\ic1_legado\Database\Procedures\pa_sp_export_volumetria_excel.sql`

**Lógica Principal:**

1. Selecionava TODOS registros sem paginação
2. Retornava para aplicação VB.NET
3. VB.NET usava `Microsoft.Office.Interop.Excel` para gerar XLS
4. Salvava arquivo temporário em `C:\Temp\{GUID}.xls`
5. Retornava caminho do arquivo ao frontend

**Problemas Identificados:**

- Microsoft.Office.Interop.Excel exigia Office instalado no servidor (licenciamento)
- Limite de 65.536 linhas (XLS antigo)
- Salvava arquivo em disco (problema de concorrência e limpeza)
- Sem limpeza automática de arquivos temporários (disco ficava cheio)

**Destino:** **SUBSTITUÍDO** - Substituído por EPPlus (XLSX ilimitado) com stream direto ao cliente

**Rastreabilidade:**
- RF Moderno: RF-103 - RN-RF103-008
- Implementação Moderna: `ExportVolumetriaService.GerarExcel()` (EPPlus)

---

## 5. TABELAS LEGADAS

### 5.1 Tabela: tb_chamados

**Schema:**
```sql
CREATE TABLE [dbo].[tb_chamados](
    [id_chamado] [int] IDENTITY(1,1) NOT NULL,
    [id_cliente] [int] NOT NULL,
    [ds_tipo] [varchar](50) NOT NULL,
    [ds_prioridade] [varchar](50) NOT NULL,
    [ds_status] [varchar](50) NOT NULL,
    [dt_criacao] [datetime] NOT NULL,
    [dt_atualizacao] [datetime] NULL,
    [id_filial] [int] NULL,
    CONSTRAINT [PK_tb_chamados] PRIMARY KEY CLUSTERED ([id_chamado] ASC)
);
```

**Problemas Identificados:**

1. Sem índice em `dt_criacao` (volumetria filtrava por essa coluna)
2. Sem índice composto (`id_cliente`, `dt_criacao`) para multi-tenancy + período
3. Campos texto sem normalização (`ds_tipo`, `ds_prioridade` - valores duplicados)
4. Sem auditoria (Created, CreatedBy, Modified, ModifiedBy)
5. Sem Foreign Key para `id_filial` (integridade não garantida)

**Destino:** **SUBSTITUÍDO** - Redesenhada como `Chamado` com auditoria, FKs, índices otimizados

**Rastreabilidade:**
- RF Moderno: RF-103 - Seção 12 (Modelo de Dados)
- MD Moderno: MD-RF103 - Tabela `Chamado`
- Migration EF Core: `20251231_CreateChamadoTable.cs`

---

### 5.2 Tabela: tb_ativos

**Schema:**
```sql
CREATE TABLE [dbo].[tb_ativos](
    [id_ativo] [int] IDENTITY(1,1) NOT NULL,
    [id_cliente] [int] NOT NULL,
    [ds_tipo] [varchar](50) NOT NULL,
    [ds_categoria] [varchar](50) NOT NULL,
    [ds_status] [varchar](50) NOT NULL,
    [id_localizacao] [int] NULL,
    [dt_criacao] [datetime] NOT NULL,
    CONSTRAINT [PK_tb_ativos] PRIMARY KEY CLUSTERED ([id_ativo] ASC)
);
```

**Problemas Identificados:**

1. Mesmos problemas de `tb_chamados` (índices, normalização, auditoria)
2. Sem FK para `id_localizacao`
3. Categoria como texto livre (valores inconsistentes)

**Destino:** **SUBSTITUÍDO** - Redesenhada como `Ativo` com normalização

**Rastreabilidade:**
- RF Moderno: RF-103 - Seção 12
- MD Moderno: MD-RF103 - Tabela `Ativo`

---

### 5.3 Tabela: tb_usuarios

**Schema:**
```sql
CREATE TABLE [dbo].[tb_usuarios](
    [id_usuario] [int] IDENTITY(1,1) NOT NULL,
    [id_cliente] [int] NOT NULL,
    [ds_nome] [varchar](100) NOT NULL,
    [ds_email] [varchar](100) NOT NULL,
    [ds_status] [varchar](50) NOT NULL,
    [dt_criacao] [datetime] NOT NULL,
    CONSTRAINT [PK_tb_usuarios] PRIMARY KEY CLUSTERED ([id_usuario] ASC)
);
```

**Problemas Identificados:**

1. Email sem UNIQUE constraint (permitia duplicados)
2. Status como texto livre (valores inconsistentes: "ativo", "Ativo", "ATIVO")
3. Sem auditoria

**Destino:** **SUBSTITUÍDO** - Redesenhada como `Usuario` com constraints

**Rastreabilidade:**
- RF Moderno: RF-103 - Seção 12
- MD Moderno: MD-RF103 - Tabela `Usuario`

---

### 5.4 Tabela: tb_contratos

**Schema:**
```sql
CREATE TABLE [dbo].[tb_contratos](
    [id_contrato] [int] IDENTITY(1,1) NOT NULL,
    [id_cliente] [int] NOT NULL,
    [ds_numero] [varchar](50) NOT NULL,
    [ds_status] [varchar](50) NOT NULL,
    [dt_vigencia_inicio] [datetime] NOT NULL,
    [dt_vigencia_fim] [datetime] NOT NULL,
    [dt_criacao] [datetime] NOT NULL,
    CONSTRAINT [PK_tb_contratos] PRIMARY KEY CLUSTERED ([id_contrato] ASC)
);
```

**Problemas Identificados:**

1. Status como texto livre
2. Sem validação `dt_vigencia_fim > dt_vigencia_inicio`
3. Sem auditoria

**Destino:** **SUBSTITUÍDO** - Redesenhada como `Contrato` com validações

**Rastreabilidade:**
- RF Moderno: RF-103 - Seção 12
- MD Moderno: MD-RF103 - Tabela `Contrato`

---

## 6. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

### RL-RN-001: Volumetria sempre calculada on-demand

**Descrição:** Todo acesso a relatório recalculava volumetria do zero, sem cache ou pré-processamento.

**Localização:** `RelatorioVolumetria.aspx.vb` - Botão `btnGerar_Click`

**Destino:** **SUBSTITUÍDO** - Substituído por consolidação diária automática (RN-RF103-002)

**Rastreabilidade:** RF-103 - RN-RF103-002

---

### RL-RN-002: Crystal Reports bloqueava interface por 30-90 segundos

**Descrição:** Geração de relatório Crystal Reports era síncrona e travava browser do usuário.

**Localização:** `RelatorioVolumetria.aspx.vb` - Linha 145

**Destino:** **SUBSTITUÍDO** - Substituído por processamento assíncrono (RN-RF103-009)

**Rastreabilidade:** RF-103 - RN-RF103-009

---

### RL-RN-003: Top 10 hardcoded para filiais

**Descrição:** Ranking top 10 era fixo apenas para filiais, não permitia customizar dimensão.

**Localização:** `Top10.aspx.vb` - Método `GerarTop10()`

**Destino:** **SUBSTITUÍDO** - Substituído por top 10 genérico com parâmetro de dimensão (RN-RF103-004)

**Rastreabilidade:** RF-103 - RN-RF103-004

---

### RL-RN-004: Export Excel limitado a 65.536 linhas

**Descrição:** Excel XLS tinha limite de linhas e truncava dados silenciosamente.

**Localização:** `ExportExcel.aspx.vb` - Método `ExportarParaExcel()`

**Destino:** **SUBSTITUÍDO** - Substituído por XLSX ilimitado (RN-RF103-008)

**Rastreabilidade:** RF-103 - RN-RF103-008

---

### RL-RN-005: Multi-database (1 cliente = 1 banco)

**Descrição:** Cada cliente tinha banco SQL Server isolado, dificultando consolidação global e manutenção.

**Localização:** Arquitetura geral do sistema legado

**Destino:** **SUBSTITUÍDO** - Substituído por multi-tenancy com Row-Level Security (RN-RF103-007)

**Rastreabilidade:** RF-103 - RN-RF103-007

---

### RL-RN-006: Sem auditoria de acesso a relatórios

**Descrição:** Nenhum acesso a relatório era registrado em log de auditoria.

**Localização:** Ausência de lógica de auditoria em todos arquivos ASPX

**Destino:** **ASSUMIDO** - Auditoria obrigatória implementada (RN-RF103-010)

**Rastreabilidade:** RF-103 - RN-RF103-010

---

## 7. GAP ANALYSIS (LEGADO × RF MODERNO)

| Item | Legado | RF Moderno | Decisão |
|------|--------|------------|---------|
| **Engine de Relatório** | Crystal Reports (lento) | Agregações SQL + ElasticSearch | SUBSTITUÍDO |
| **Consolidação** | Manual (botão "Gerar") | Automática Hangfire (4h diárias) | SUBSTITUÍDO |
| **Multi-tenancy** | Multi-database (1 cliente = 1 banco) | Row-Level Security (ClienteId) | SUBSTITUÍDO |
| **Export** | Excel XLS (65k linhas) | Excel XLSX ilimitado | SUBSTITUÍDO |
| **Cache** | Nenhum | Redis com TTL inteligente | ADICIONADO |
| **Comparativo Temporal** | Não disponível | Mês vs mês, ano vs ano | ADICIONADO |
| **Tendências** | Valores brutos sem suavização | Média móvel 7 dias | ADICIONADO |
| **Performance** | 30+ segundos (> 500k registros) | < 2 segundos (10M+ registros) | SUBSTITUÍDO |
| **Permissões** | Coarse-grained (tudo ou nada) | Fine-grained RBAC | SUBSTITUÍDO |
| **Auditoria** | Inexistente | Log completo com rastreabilidade | ADICIONADO |
| **Validação Período** | Não validava se finalizado | Valida períodos finalizados | ASSUMIDO (regra correta mantida) |
| **Top 10** | Hardcoded filiais | Genérico (filial, depto, CC, responsável) | SUBSTITUÍDO |
| **Processamento Assíncrono** | Não disponível | > 100k registros em background | ADICIONADO |

---

## 8. DECISÕES DE MODERNIZAÇÃO

### Decisão 1: Substituir Crystal Reports por Agregações SQL Nativas

**Motivo:** Crystal Reports:
- Exigia licença cara
- Performance inaceitável (30+ segundos)
- Carregava tudo em memória
- Não escala para milhões de registros

**Impacto:** Alto - Mudança completa de engine de relatório

**Solução Moderna:** Agregações SQL via LINQ + ElasticSearch para volumes > 1M

---

### Decisão 2: Consolidação Automática Diária

**Motivo:** Volumetrias são lidas frequentemente mas mudam pouco (dados históricos).
Pré-calcular às 4h elimina carga em horário comercial.

**Impacto:** Médio - Requer job Hangfire e tabela dedicada

**Solução Moderna:** Job `ConsolidacaoVolumetriaJob` às 4h diárias

---

### Decisão 3: Multi-tenancy com Row-Level Security

**Motivo:** Multi-database é caro de manter, dificulta backups e consultas agregadas.

**Impacto:** Alto - Migração de dados de múltiplos bancos para banco único

**Solução Moderna:** Banco único com `ClienteId` em todas tabelas + filtro obrigatório

---

### Decisão 4: Processamento Assíncrono para Grandes Volumes

**Motivo:** HTTP timeout com relatórios grandes. Usuário perdia trabalho.

**Impacto:** Médio - Requer fila Hangfire + notificação por e-mail

**Solução Moderna:** Relatórios > 100k em background + notificação

---

## 9. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Mitigação |
|-------|---------|-----------|
| **Diferença de Valores entre Legado e Moderno** | Alto | Validar amostra de 1% comparando volumetrias antes da migração |
| **Performance Pior que Esperado** | Médio | Testar com 10M registros em ambiente de staging antes de produção |
| **Falta de Índices Adequados** | Médio | Criar índices (`ClienteId`, `DataCriacao`) antes de carregar dados |
| **Timezone Inconsistente** | Baixo | Padronizar UTC em todos registros migrados |
| **Usuários Estranharem Consolidação Diária** | Baixo | Comunicar que dados de "hoje" só aparecem após 4h do dia seguinte |

---

## 10. RASTREABILIDADE

| Elemento Legado | Referência RF Moderno |
|-----------------|----------------------|
| `RelatorioVolumetria.aspx` | RF-103 - UC01 (Consultar Volumetria) |
| `ComparativoTemporal.aspx` | RF-103 - UC03 (Comparativo Temporal) |
| `Top10.aspx` | RF-103 - UC04 (Top 10) |
| `ExportExcel.aspx` | RF-103 - RN-RF103-008 |
| `WSVolumetria.asmx` | RF-103 - Seção 10 (API Endpoints) |
| `pa_sp_volumetria_chamados` | RF-103 - RN-RF103-001 |
| `pa_sp_top10_filiais` | RF-103 - RN-RF103-004 |
| `pa_sp_comparativo_temporal` | RF-103 - RN-RF103-003 |
| `pa_sp_tendencia_30dias` | RF-103 - RN-RF103-005 |
| `pa_sp_export_volumetria_excel` | RF-103 - RN-RF103-008 |
| `tb_chamados` | MD-RF103 - Tabela `Chamado` |
| `tb_ativos` | MD-RF103 - Tabela `Ativo` |
| `tb_usuarios` | MD-RF103 - Tabela `Usuario` |
| `tb_contratos` | MD-RF103 - Tabela `Contrato` |

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|--------|------|-----------|-------|
| 1.0 | 2025-12-31 | Versão inicial - Documentação completa do legado RF-103 | Claude Code |

---

**Última Atualização**: 2025-12-31
**Autor**: Claude Code
**Status**: ATIVO
**Governança**: v2.0
