# RL-RF102 — Referência ao Legado (Relatórios e Análises)

**Versão:** 1.0
**Data:** 2025-12-31
**Autor:** Claude Code

**RF Moderno Relacionado:** RF102 - Relatórios e Análises
**Sistema Legado:** IControlIT VB.NET / ASP.NET Web Forms
**Objetivo:** Documentar o comportamento do legado que serve de base para a refatoração, garantindo rastreabilidade, entendimento histórico e mitigação de riscos.

---

## 1. CONTEXTO DO LEGADO

### 1.1 Arquitetura Geral

- **Arquitetura:** Monolítica, ASP.NET Web Forms com code-behind VB.NET
- **Linguagem / Stack:** VB.NET, ASP.NET 4.x, Crystal Reports
- **Banco de Dados:** SQL Server (multi-database por cliente)
- **Multi-tenant:** Sim, via bancos separados por cliente (ex: `IC1_Cliente01`, `IC1_Cliente02`)
- **Auditoria:** Parcial (logs manuais em algumas operações)
- **Configurações:** Web.config (connection strings, app settings)

### 1.2 Problemas Arquiteturais Identificados

1. **Multi-database por cliente:** Cada cliente tem banco separado, dificultando consolidação e análise cross-tenant
2. **SQL inline em código:** Queries SQL escritas diretamente em VB.NET (risco de SQL Injection)
3. **Crystal Reports:** Complexo, requer conhecimento técnico, licenças caras
4. **Processamento síncrono:** Relatórios grandes bloqueiam tela durante minutos
5. **Sem conformidade LGPD:** Nenhuma justificativa de acesso a dados sensíveis
6. **Auditoria manual:** Logs não estruturados, difíceis de rastrear
7. **Agendamento via SQL Agent:** Difícil de configurar, requer acesso DBA

---

## 2. TELAS DO LEGADO

### 2.1 Tela: RelatóriosListar.aspx

- **Caminho:** `ic1_legado/IControlIT/Relatorios/RelatóriosListar.aspx`
- **Responsabilidade:** Lista todos os relatórios disponíveis (predefinidos + personalizados do usuário)

#### Campos Principais

| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| `GridRelatorios` | GridView | Sim | Lista relatórios com colunas: Nome, Módulo, Última Execução, Total Execuções |
| `btnNovo` | Button | Sim | Redireciona para designer |
| `btnExecutar` | Button | Sim | Redireciona para tela de execução |
| `btnEditar` | Button | Não | Apenas para relatórios personalizados |
| `btnExcluir` | Button | Não | Soft delete |

#### Comportamentos Implícitos

- **Filtro automático por usuário:** Code-behind VB.NET filtra relatórios por `Cd_Usuario` (não por ClienteId - problema de isolamento)
- **Nenhuma validação de permissões:** Todos os usuários autenticados veem todos os relatórios (falha de segurança)
- **Ordenação fixa:** Ordenado por `Dt_Criacao DESC` (sem opção de customização)
- **Sem paginação:** Lista completa carrega de uma vez (performance ruim se muitos relatórios)

**DESTINO:** SUBSTITUÍDO (tela Angular `/relatorios` com paginação, filtros e RBAC)

---

### 2.2 Tela: RelatóriosDesigner.aspx

- **Caminho:** `ic1_legado/IControlIT/Relatorios/RelatóriosDesigner.aspx`
- **Responsabilidade:** Interface para criar/editar relatórios personalizados usando Crystal Reports

#### Campos Principais

| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| `txtNome` | TextBox | Sim | Nome do relatório |
| `ddlModulo` | DropDownList | Sim | EST, CON, FAT, CHM, SLA |
| `CrystalReportViewer1` | Crystal Reports Viewer | Sim | Designer visual pesado |
| `btnSalvar` | Button | Sim | Salva definição do relatório |

#### Comportamentos Implícitos

- **Crystal Reports obrigatório:** Requer instalação de runtime Crystal Reports (licença cara)
- **Sem limite de campos:** Usuários podem selecionar 100+ campos (relatórios ilegíveis)
- **Query SQL gerada automaticamente:** Crystal gera SQL complexo (difícil de otimizar)
- **Sem validação de campos sensíveis:** Usuários podem acessar CPF, Salário sem permissão (problema LGPD)
- **Nenhum preview:** Só vê resultado após salvar e executar (UX ruim)

**DESTINO:** SUBSTITUÍDO (designer Angular drag-and-drop, máximo 20 campos, preview em tempo real)

---

### 2.3 Tela: RelatóriosExecutar.aspx

- **Caminho:** `ic1_legado/IControlIT/Relatorios/RelatóriosExecutar.aspx`
- **Responsabilidade:** Executar relatório e exibir resultados

#### Campos Principais

| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| `ddlFiltros` | DropDownList (dinâmico) | Não | Filtros parametrizados |
| `btnExecutar` | Button | Sim | Dispara execução |
| `GridResultado` | GridView | Sim | Exibe dados do relatório |
| `btnExportarPDF` | Button | Sim | Export PDF via Crystal |
| `btnExportarExcel` | Button | Sim | Export Excel via Crystal |

#### Comportamentos Implícitos

- **Processamento síncrono:** Bloqueia tela durante execução (pode levar minutos)
- **Timeout HTTP:** Relatórios > 100k registros frequentemente dão timeout
- **Nenhuma justificativa LGPD:** Dados sensíveis acessados sem documentação
- **Auditoria manual:** Log escrito manualmente em `tblHistoricoRelatorios` (inconsistente)
- **Sem notificação de conclusão:** Usuário fica esperando sem feedback

**DESTINO:** SUBSTITUÍDO (execução assíncrona Hangfire para > 10k registros, notificação ao usuário, justificativa LGPD obrigatória)

---

### 2.4 Tela: AgendamentosListar.aspx

- **Caminho:** `ic1_legado/IControlIT/Relatorios/AgendamentosListar.aspx`
- **Responsabilidade:** Lista agendamentos de relatórios do usuário

#### Campos Principais

| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| `GridAgendamentos` | GridView | Sim | Lista agendamentos ativos |
| `btnNovo` | Button | Sim | Cria novo agendamento |
| `btnCancelar` | Button | Sim | Cancela agendamento (soft delete) |

#### Comportamentos Implícitos

- **Agendamento via SQL Agent:** Code-behind cria job no SQL Server Agent (requer permissões DBA)
- **Sem limite de agendamentos:** Usuários podem criar 100+ agendamentos (abuso de recursos)
- **Email hard-coded:** Código VB.NET envia email via SMTP configurado em Web.config (inflexível)
- **Frequência limitada:** Apenas diário às 08:00 (sem horário customizável)

**DESTINO:** SUBSTITUÍDO (agendamento Hangfire, máximo 10 por usuário, horário customizável, múltiplos emails)

---

### 2.5 Tela: HistoricoRelatorios.aspx

- **Caminho:** `ic1_legado/IControlIT/Relatorios/HistoricoRelatorios.aspx`
- **Responsabilidade:** Visualizar execuções anteriores de um relatório

#### Campos Principais

| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| `GridHistorico` | GridView | Sim | Lista execuções anteriores |
| `btnDownload` | Button | Sim | Download do arquivo gerado |

#### Comportamentos Implícitos

- **Histórico ilimitado:** Arquivos mantidos indefinidamente (consumo excessivo de storage)
- **Sem política de retenção:** Nenhuma limpeza automática
- **Arquivos em servidor local:** Salvos em pasta física do servidor (não escalável)
- **Auditoria incompleta:** Não registra IP do usuário ou justificativa LGPD

**DESTINO:** SUBSTITUÍDO (histórico 90 dias, job Hangfire limpeza automática, arquivos em Azure Blob Storage, auditoria completa)

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

### 3.1 Webservice: WSRelatorios.asmx

- **Caminho:** `ic1_legado/WebService/WSRelatorios.asmx.vb`
- **Responsabilidade:** API SOAP para operações de relatórios

| Método | Responsabilidade | Observações |
|--------|------------------|-------------|
| `ListarRelatorios()` | Lista todos os relatórios do usuário | Retorna DataTable (não tipado) |
| `GetRelatorio(id)` | Obter relatório por ID | Sem validação de ClienteId (falha segurança) |
| `ExecutarRelatorio(id, filtros)` | Executa relatório | Síncrono, bloqueia thread |
| `ExportarPDF(id, filtros)` | Exporta para PDF via Crystal | Licença Crystal obrigatória |
| `ExportarExcel(id, filtros)` | Exporta para Excel via Crystal | Licença Crystal obrigatória |
| `CriarAgendamento(relId, freq, email)` | Cria agendamento via SQL Agent | Requer sysadmin SQL Server |

**Problemas Identificados:**

1. **SOAP (deprecated):** Tecnologia legada, difícil de consumir de frontends modernos
2. **Sem autenticação JWT:** Usa autenticação Windows (não funciona em SaaS)
3. **Retorna DataTable:** Não tipado, difícil de deserializar em JSON
4. **Sem multi-tenancy:** Não filtra por ClienteId automaticamente
5. **Queries SQL inline:** Concatenação de strings (SQL Injection)

**DESTINO:** SUBSTITUÍDO (REST API com endpoints `/api/relatorios`, autenticação JWT, DTOs tipados, EF Core)

---

## 4. TABELAS LEGADAS

### 4.1 Tabela: tblRelatorios

- **Schema:** `[dbo].[tblRelatorios]`
- **Finalidade:** Armazena definições de relatórios predefinidos e personalizados

| Campo | Tipo | Observações |
|-------|------|-------------|
| `[Id_Relatorio]` | INT IDENTITY | PK |
| `[Nm_Relatorio]` | VARCHAR(255) | Nome do relatório |
| `[Ds_Relatorio]` | TEXT | Descrição |
| `[Cd_Modulo]` | VARCHAR(50) | Código do módulo (EST, CON, FAT, CHM) |
| `[Tx_SQL]` | TEXT | **PROBLEMA:** Query SQL inline (risco SQL Injection) |
| `[Dt_Criacao]` | DATETIME | Data de criação |
| `[Bl_Ativo]` | BIT | Ativo/Inativo |

**Problemas Identificados:**

1. **Falta FK para validar Cd_Modulo:** Nenhuma tabela de referência
2. **Campo Tx_SQL (TEXT):** Query SQL armazenada como texto (inseguro, difícil de manter)
3. **Sem auditoria:** Não tem campos Created, CreatedBy, LastModified, LastModifiedBy
4. **Sem multi-tenancy:** Não tem campo ClienteId (relatórios globais)
5. **Nomenclatura legada:** Prefixos húngaros ([Nm_], [Cd_], [Tx_])

**DESTINO:** SUBSTITUÍDO (tabela `Relatorio` com multi-tenancy, auditoria, sem SQL inline)

---

### 4.2 Tabela: tblAgendamentos

- **Schema:** `[dbo].[tblAgendamentos]`
- **Finalidade:** Armazena agendamentos de relatórios

| Campo | Tipo | Observações |
|-------|------|-------------|
| `[Id_Agendamento]` | INT IDENTITY | PK |
| `[Id_Relatorio]` | INT | FK para tblRelatorios |
| `[Cd_Usuario]` | INT | FK para tblUsuarios |
| `[Cd_Frequencia]` | INT | 1=Diário, 2=Semanal, 3=Mensal |
| `[Hr_Execucao]` | TIME | Horário de execução |
| `[Tx_Email]` | VARCHAR(MAX) | Emails separados por ponto-e-vírgula |
| `[Bl_Ativo]` | BIT | Ativo/Inativo |
| `[Dt_Criacao]` | DATETIME | Data de criação |

**Problemas Identificados:**

1. **Falta FK definida:** `[Id_Relatorio]` e `[Cd_Usuario]` sem CONSTRAINT
2. **Campo Tx_Email (VARCHAR(MAX)):** Emails como string delimitada (difícil de validar)
3. **Sem limite de agendamentos por usuário:** Nenhuma constraint CHECK
4. **Sem auditoria:** Não tem CreatedBy, LastModified
5. **Sem multi-tenancy:** Não tem ClienteId

**DESTINO:** SUBSTITUÍDO (tabela `AgendamentoRelatorio` com multi-tenancy, auditoria, EmailsDestinatarios como List<string>)

---

### 4.3 Tabela: tblHistoricoRelatorios

- **Schema:** `[dbo].[tblHistoricoRelatorios]`
- **Finalidade:** Armazena histórico de execuções

| Campo | Tipo | Observações |
|-------|------|-------------|
| `[Id_Historico]` | INT IDENTITY | PK |
| `[Id_Relatorio]` | INT | FK para tblRelatorios |
| `[Cd_Usuario]` | INT | FK para tblUsuarios |
| `[Dt_Execucao]` | DATETIME | Data/hora de execução |
| `[Tx_Filtros]` | TEXT | Filtros aplicados (texto livre) |
| `[Nm_Arquivo]` | VARCHAR(500) | Nome do arquivo gerado |
| `[Tm_Arquivo]` | BIGINT | Tamanho do arquivo em bytes |

**Problemas Identificados:**

1. **Sem política de retenção:** Dados mantidos indefinidamente
2. **Sem campo DataExpiracao:** Nenhuma limpeza automática
3. **Campo Tx_Filtros (TEXT):** Filtros como texto livre (difícil de queryar)
4. **Sem auditoria de acesso LGPD:** Não registra IP, UserAgent, JustificativaLGPD
5. **Sem multi-tenancy:** Não tem ClienteId
6. **Arquivos em servidor local:** `[Nm_Arquivo]` aponta para path físico (não cloud)

**DESTINO:** SUBSTITUÍDO (tabela `HistoricoRelatorio` com DataExpiracao, job Hangfire limpeza 90 dias, arquivos em Azure Blob)

---

## 5. STORED PROCEDURES LEGADAS

### 5.1 Procedure: pa_GerarRelatorioAtivos

- **Caminho:** `ic1_legado/Database/Procedures/pa_GerarRelatorioAtivos.sql`
- **Parâmetros:**
  - `@Cd_Usuario INT` (entrada)
  - `@Dt_Inicio DATETIME` (entrada)
  - `@Dt_Fim DATETIME` (entrada)
  - `@Result INT OUTPUT` (saída - total de registros)

**Lógica Principal (em linguagem natural):**

1. Valida se usuário existe
2. Monta query dinâmica com filtros (concatenação de strings - **SQL Injection**)
3. Executa query e insere resultados em tabela temporária
4. Retorna total de registros

**Problemas Identificados:**

1. **SQL Injection:** Query montada via concatenação de strings
2. **Nenhuma validação de ClienteId:** Usuário pode acessar dados de outros clientes
3. **Tabela temporária global:** `##Temp_Relatorio` (conflitos se múltiplos usuários)
4. **Sem auditoria:** Não registra execução

**DESTINO:** SUBSTITUÍDO (handler CQRS `ExecutarRelatorioHandler` com EF Core, LINQ, multi-tenancy automático)

---

### 5.2 Procedure: pa_ExportarRelatorioExcel

- **Caminho:** `ic1_legado/Database/Procedures/pa_ExportarRelatorioExcel.sql`
- **Parâmetros:**
  - `@Id_Relatorio INT` (entrada)
  - `@Tx_Filtros TEXT` (entrada)

**Lógica Principal:**

1. Busca definição do relatório (campo `[Tx_SQL]`)
2. Executa query SQL armazenada
3. Gera arquivo Excel via SSIS (SQL Server Integration Services)
4. Salva em pasta física `D:\IControlIT\Relatorios\`

**Problemas Identificados:**

1. **Dependência SSIS:** Requer instalação e configuração complexa
2. **Pasta física hard-coded:** Não escalável, requer servidor file server
3. **Sem validação de permissões:** Qualquer usuário pode exportar qualquer relatório
4. **Sem auditoria:** Não registra quem exportou

**DESTINO:** SUBSTITUÍDO (biblioteca EPPlus em .NET, arquivos salvos em Azure Blob Storage, auditoria completa)

---

### 5.3 Procedure: pa_LimparHistoricoRelatorios

- **Caminho:** `ic1_legado/Database/Procedures/pa_LimparHistoricoRelatorios.sql`
- **Parâmetros:** Nenhum

**Lógica Principal:**

1. Deleta registros de `tblHistoricoRelatorios` com > 365 dias
2. **Problema:** Não deleta arquivos físicos correspondentes

**DESTINO:** SUBSTITUÍDO (job Hangfire `LimparHistoricoExpiradoJob` com política 90 dias, deleta registros + arquivos Azure Blob)

---

## 6. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

### RL-RN-001: Relatórios ordenados por data de criação decrescente

**Descrição:** No code-behind VB.NET de `RelatóriosListar.aspx`, a query SQL sempre ordena por `Dt_Criacao DESC` (mais recentes primeiro).

**Localização:** `RelatóriosListar.aspx.vb`, linha 42-45

**DESTINO:** ASSUMIDO (ordem padrão mantida no sistema moderno, mas permitir customização)

---

### RL-RN-002: Agendamentos executam apenas às 08:00

**Descrição:** Todos os agendamentos criados via SQL Agent têm horário fixo 08:00. Não há opção de customização.

**Localização:** `WSRelatorios.asmx.vb`, método `CriarAgendamento`, linha 120

**DESTINO:** SUBSTITUÍDO (sistema moderno permite horário customizável)

---

### RL-RN-003: Exportação PDF sempre inclui logo do primeiro cliente

**Descrição:** Logo hard-coded em `Web.config` - `AppSettings["LogoClientePadrao"]`. Não é dinâmico por cliente.

**Localização:** `RelatóriosExecutar.aspx.vb`, linha 200

**DESTINO:** SUBSTITUÍDO (logo dinâmico obtido de `SistemaCliente` ou `SistemaConfiguracaoGeral`)

---

### RL-RN-004: Usuários sem permissão podem acessar qualquer relatório

**Descrição:** Code-behind apenas valida se usuário está autenticado (`User.Identity.IsAuthenticated`). Não valida permissões específicas.

**Localização:** Múltiplas telas ASPX

**DESTINO:** SUBSTITUÍDO (RBAC com permissões granulares `relatorio:relatorio:create`, `relatorio:relatorio:execute`, etc.)

---

### RL-RN-005: Histórico mantido indefinidamente

**Descrição:** Não há job de limpeza automática. Dados acumulam infinitamente.

**Localização:** Ausência de procedure de limpeza

**DESTINO:** SUBSTITUÍDO (job Hangfire limpeza automática 90 dias)

---

### RL-RN-006: Campos sensíveis acessíveis sem justificativa

**Descrição:** Usuários podem criar relatórios com CPF, Salário, RG sem fornecer justificativa LGPD.

**Localização:** `RelatóriosDesigner.aspx.vb`

**DESTINO:** SUBSTITUÍDO (validação obrigatória de justificativa LGPD + auditoria)

---

## 7. GAP ANALYSIS (LEGADO × RF MODERNO)

| Item | Legado | RF Moderno | Observação |
|------|--------|------------|------------|
| **Designer** | Crystal Reports (complexo) | Angular drag-and-drop (simples) | Usuários não técnicos conseguem criar relatórios |
| **Processamento** | Síncrono (bloqueia tela) | Assíncrono Hangfire (> 10k registros) | Melhora UX e evita timeout |
| **Formatos Export** | PDF e Excel (Crystal) | PDF, Excel, CSV, JSON, XML | Mais flexibilidade |
| **Agendamento** | SQL Agent (requer DBA) | Hangfire (UI integrada) | Usuários autônomos |
| **Multi-tenancy** | Multi-database (N bancos) | Single database com ClienteId | Consolidação e escalabilidade |
| **Auditoria** | Manual e inconsistente | Automática e imutável | Conformidade LGPD |
| **LGPD** | Nenhuma justificativa | Justificativa obrigatória | Conformidade legal |
| **Permissões** | Autenticação básica | RBAC granular | Segurança aprimorada |
| **Retenção Histórico** | Indefinido | 90 dias (automático) | Conformidade política retenção |
| **SQL Injection** | Vulnerável (SQL inline) | Protegido (EF Core + LINQ) | Segurança crítica |

---

## 8. DECISÕES DE MODERNIZAÇÃO

### Decisão 1: Abandonar Crystal Reports

- **Motivo:** Licenças caras, complexo para usuários não técnicos, não escalável
- **Impacto:** Alto - requer redesenho completo do designer
- **Solução:** Designer visual drag-and-drop em Angular

### Decisão 2: Single Database com Multi-tenancy

- **Motivo:** Multi-database por cliente não escala, dificulta análise consolidada
- **Impacto:** Alto - migração de dados de N bancos para 1 banco com ClienteId
- **Solução:** Migração gradual com Row-Level Security

### Decisão 3: Hangfire para Agendamento

- **Motivo:** SQL Agent requer permissões DBA, difícil de gerenciar
- **Impacto:** Médio - requer configuração de Hangfire
- **Solução:** Hangfire dashboard integrado ao sistema

### Decisão 4: Azure Blob Storage

- **Motivo:** Arquivos em servidor local não escalam, difícil backup
- **Impacto:** Médio - requer configuração Azure
- **Solução:** Storage account com política de lifecycle (90 dias)

### Decisão 5: REST API substituindo SOAP

- **Motivo:** SOAP é legado, difícil de consumir de frontends modernos
- **Impacto:** Alto - reescrever todos os webservices
- **Solução:** Minimal APIs .NET 10 com autenticação JWT

---

## 9. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Mitigação |
|-------|---------|-----------|
| **Perda de relatórios personalizados** | Alto | Exportar definições legado + script de conversão |
| **Usuários acostumados com Crystal** | Médio | Treinamento + documentação detalhada |
| **Migração multi-database** | Alto | Migração gradual + validação de integridade |
| **Quebra de agendamentos** | Alto | Manter SQL Agent até migração completa |
| **Arquivos históricos inacessíveis** | Médio | Copiar arquivos locais para Azure Blob antes de desativar legado |

---

## 10. RASTREABILIDADE

| Elemento Legado | Referência RF Moderno |
|-----------------|----------------------|
| `RelatóriosListar.aspx` | RF102 - Seção 4 (Funcionalidades), UC00-RF102 (Listar) |
| `RelatóriosDesigner.aspx` | RF102 - Seção 4, UC01-RF102 (Criar) |
| `RelatóriosExecutar.aspx` | RF102 - Seção 4, UC02-RF102 (Executar) |
| `AgendamentosListar.aspx` | RF102 - Seção 4, UC03-RF102 (Agendar) |
| `HistoricoRelatorios.aspx` | RF102 - Seção 4, UC04-RF102 (Histórico) |
| `WSRelatorios.asmx` | RF102 - Seção 11 (Endpoints API) |
| `tblRelatorios` | RF102 - Seção 7 (Modelo de Dados), MD-RF102 (Tabela Relatorio) |
| `tblAgendamentos` | MD-RF102 (Tabela AgendamentoRelatorio) |
| `tblHistoricoRelatorios` | MD-RF102 (Tabela HistoricoRelatorio) |
| `pa_GerarRelatorioAtivos` | RF102 - RN-RF102-001 a RN-RF102-010 |
| `pa_ExportarRelatorioExcel` | RF102 - Seção 11 (POST /api/relatorios/{id}/export/excel) |
| `pa_LimparHistoricoRelatorios` | RF102 - RN-RF102-007 (job Hangfire limpeza 90 dias) |

---

## 11. BANCOS LEGADOS MAPEADOS

### Banco: IC1_Producao (cliente genérico)

- **Servidor:** SQL-LEGADO-01
- **Tabelas Relacionadas:**
  - `tblRelatorios`
  - `tblAgendamentos`
  - `tblHistoricoRelatorios`
  - `tblUsuarios` (FK para `[Cd_Usuario]`)
- **DESTINO:** CONSOLIDADO (migrado para banco único com multi-tenancy via ClienteId)
- **Justificativa:** Multi-database por cliente não escala. Sistema moderno usa Single Database + Row-Level Security.
- **Banco Moderno:** `IControlIT.db` (SQLite dev) / SQL Server moderno (prod)

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|--------|------|-----------|-------|
| 1.0 | 2025-12-31 | Criação do RL-RF102 - Referência ao Legado completa | Claude Code |
