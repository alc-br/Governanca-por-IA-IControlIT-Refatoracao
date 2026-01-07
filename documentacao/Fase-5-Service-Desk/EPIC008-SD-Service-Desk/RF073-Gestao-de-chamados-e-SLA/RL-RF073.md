# RL-RF073 — Referência ao Legado (Gestão de Chamados e SLA)

**Versão:** 1.0
**Data:** 2025-12-30
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF-073
**Sistema Legado:** VB.NET + ASP.NET Web Forms
**Objetivo:** Documentar o comportamento do legado que serve de base para a refatoração, garantindo rastreabilidade, entendimento histórico e mitigação de riscos.

---

## 1. CONTEXTO DO LEGADO

### 1.1 Arquitetura Geral

- **Arquitetura**: Monolítica ASP.NET Web Forms com VB.NET code-behind
- **Linguagem / Stack**: VB.NET, ASP.NET Web Forms 4.x, SQL Server 2012+
- **Banco de Dados**: SQL Server multi-database (banco específico por cliente: `SC_CLIENTE_NOME`)
- **Multi-tenant**: Não nativo (requer múltiplas databases físicas)
- **Auditoria**: Parcial via triggers SQL (não estruturada)
- **Configurações**: Web.config + tabelas de configuração
- **WebServices**: SOAP (.asmx) com XML serialization manual
- **Sessão**: ASP.NET Session State (In-Proc)
- **Autenticação**: Forms Authentication + cookies

### 1.2 Problemas Arquiteturais Identificados

1. **Multi-database sem multi-tenancy**: Cada cliente tem banco separado, dificultando manutenção e consolidação
2. **Stored Procedures pesadas**: Lógica de negócio em SQL dificulta testes e manutenção
3. **Código VB.NET spaghetti**: Code-behind mistura UI, lógica de negócio e acesso a dados
4. **Sem auditoria estruturada**: Triggers SQL não registram IP, usuário executante ou ação detalhada
5. **Performance**: Queries N+1, sem paginação adequada, carregamento ansioso de relacionamentos
6. **Segurança**: Sem proteção contra SQL Injection em alguns pontos, XSS não tratado
7. **WebServices SOAP ineficientes**: XML verboso, sem versionamento, autenticação Basic Auth
8. **Sem testes automatizados**: Zero cobertura de testes unitários ou integração

---

## 2. TELAS DO LEGADO

### 2.1 Tela: Chamado.aspx (Listagem de Chamados)

**Caminho:** `D:\IC2\ic1_legado\IControlIT\Chamado\Chamado.aspx`

**Responsabilidade:** Listagem de chamados com filtros por status, prioridade, categoria e técnico. Exibe grid paginado (50 registros por página).

#### Campos da Grid

| Campo | Tipo | Observações |
|-------|------|-------------|
| Número | Label | Número sequencial gerado (ex: CHD-2025-001) |
| Descrição | Label (truncado 100 chars) | Hover mostra texto completo |
| Status | DropDownList (read-only) | Valores: Novo, Atribuído, Resolvido, Fechado |
| Prioridade | Label colorizado | P1=Vermelho, P2=Laranja, P3=Amarelo, P4=Verde |
| SLA | Label (% concluído) | Verde (<80%), Amarelo (80-95%), Vermelho (>95%) |
| Atribuído a | Label | Nome do técnico ou "Não atribuído" |
| Criado em | Label (DateTime) | Formato: dd/MM/yyyy HH:mm |

#### Comportamentos Implícitos

- **Paginação manual**: ViewState armazena página atual, clicar "Próximo" chama stored procedure com OFFSET/FETCH
- **Filtro não persistente**: Filtros perdidos ao navegar para outra página
- **Sem ordenação customizada**: Sempre ordena por DataCriacao DESC (hard-coded)
- **Refresh automático**: Timer de 30 segundos recarrega grid (causa flicker visual)
- **Sem validação de permissão**: Qualquer usuário autenticado vê todos chamados (vulnerabilidade)

**DESTINO**: **SUBSTITUÍDO** - Tela moderna Angular com paginação otimizada, filtros persistentes e RBAC.

---

### 2.2 Tela: Chamado_Consulta.aspx (Detalhes do Chamado)

**Caminho:** `D:\IC2\ic1_legado\IControlIT\Chamado\Chamado_Consulta.aspx`

**Responsabilidade:** Exibir detalhes completos do chamado + histórico de comentários + anexos + SLA.

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| Número | TextBox (read-only) | Sim | Gerado automaticamente |
| Solicitante | Label | Sim | Nome do usuário |
| Descrição | TextArea (read-only) | Sim | Texto completo |
| Categoria | Label | Sim | Nível 1 → Nível 2 → Nível 3 |
| Prioridade | Label | Sim | P1-P4 |
| Status | DropDownList | Sim | Editável por Staff |
| Ativos Afetados | GridView | Não | Lista de ativos linkados |
| Data Criação | Label | Sim | dd/MM/yyyy HH:mm |
| Data Resposta | Label | Não | Quando técnico fez primeiro comentário |
| Data Resolução | Label | Não | Quando marcado como Resolvido |
| SLA Status | Label colorizado | Sim | No Prazo / Risco / Vencido |
| Comentários | Repeater | Não | Lista de comentários (sem distinção interno/externo) |
| Anexos | GridView | Não | Lista de arquivos com link download |

#### Comportamentos Implícitos

- **Comentários sem visibilidade**: Todos comentários visíveis a todos (sem flag interno/externo)
- **SLA calculado em tempo real**: Query SQL recalcula a cada page load (ineficiente)
- **Anexos sem antivírus**: Upload direto para filesystem sem scanning
- **Edição inline de status**: Mudança de status sem confirmação ou comentário obrigatório
- **Sem auditoria de visualização**: Não registra quem visualizou o chamado

**DESTINO**: **SUBSTITUÍDO** - Tela moderna com comentários internos/externos, SLA pré-calculado, antivírus obrigatório.

---

### 2.3 Tela: Chamado_Solicitacao.aspx (Abrir Novo Chamado)

**Caminho:** `D:\IC2\ic1_legado\IControlIT\Chamado\Chamado_Solicitacao.aspx`

**Responsabilidade:** Formulário para abertura de novo chamado.

#### Campos

| Campo | Tipo | Obrigatório | Validação |
|-------|------|-------------|-----------|
| Descrição | TextArea | Sim | Mínimo 10 caracteres (deveria ser 20) |
| Categoria | DropDownList (cascata) | Sim | 3 níveis hierárquicos |
| Prioridade | DropDownList | Não | Default: P3 |
| Ativos | CheckBoxList | Sim | Mínimo 1 selecionado |
| Contato | TextBox | Não | Email ou telefone |
| Anexo | FileUpload | Não | Sem validação de tamanho |

#### Comportamentos Implícitos

- **Prioridade fixa**: Usuário escolhe manualmente (não calcula via matriz Impacto x Urgência)
- **Sem validação de descrição adequada**: Aceita textos vagos como "Problema" (10 chars)
- **Cascata de categoria via PostBack**: A cada mudança de Nível 1, recarrega página (lento)
- **Upload sem limite**: Aceita arquivos de qualquer tamanho (risco de DoS)
- **Sem detecção automática de contrato**: Não usa ativo para inferir contrato/SLA
- **SLA fixo por prioridade**: Ignora contratos específicos de cliente

**DESTINO**: **SUBSTITUÍDO** - Validações rigorosas (20 chars mínimo), matriz Impacto x Urgência, upload limitado a 5MB.

---

### 2.4 Tela: Chamado_SLA_Consulta.aspx (Monitoramento de SLA)

**Caminho:** `D:\IC2\ic1_legado\IControlIT\Chamado\Chamado_SLA_Consulta.aspx`

**Responsabilidade:** Dashboard de SLA com KPIs (conformidade, vencidos, em risco).

#### Widgets

- **Taxa de Conformidade**: (Resolvidos no prazo / Total resolvidos) * 100
- **Chamados Vencidos**: Count(Status=Vencido)
- **Chamados em Risco**: Count(Status=Risco)
- **Tempo Médio de Resposta**: AVG(DataResposta - DataCriacao)
- **Tempo Médio de Resolução**: AVG(DataResolucao - DataCriacao)

#### Comportamentos Implícitos

- **Cálculo em tempo real sem cache**: Query pesada roda a cada acesso (timeout em clientes grandes)
- **Sem filtro por período**: Sempre calcula sobre TODOS os chamados históricos
- **Sem drill-down**: Não permite clicar em "Vencidos" para ver lista detalhada
- **Gráficos estáticos**: Imagens PNG geradas server-side com GDI+ (feias e lentas)

**DESTINO**: **SUBSTITUÍDO** - Dashboard Angular com gráficos ApexCharts, filtros de período, drill-down, cache de KPIs.

---

### 2.5 Tela: Chamado_Fila_Atendimento.aspx (Gestão de Filas)

**Caminho:** `D:\IC2\ic1_legado\IControlIT\Chamado\Chamado_Fila_Atendimento.aspx`

**Responsabilidade:** Criar/editar filas de atendimento e associar técnicos.

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| Nome da Fila | TextBox | Sim | Ex: Fila_Telecom |
| Descrição | TextArea | Não | Texto livre |
| Técnicos | CheckBoxList | Sim | Lista de usuários com perfil "Técnico" |

#### Comportamentos Implícitos

- **Sem skill-based routing**: Apenas agrupa técnicos, mas não roteia automaticamente
- **Atribuição manual**: Manager escolhe técnico na mão (não considera carga)
- **Sem validação de disponibilidade**: Permite atribuir técnico com 50 chamados abertos
- **Filas não mapeadas a categorias**: Relação manual (não automática)

**DESTINO**: **ASSUMIDO COM MELHORIAS** - Manter conceito de filas mas adicionar skill-based routing automático e load balancing.

---

### 2.6 Tela: Chamado_Data_Parada.aspx (Registrar Parada)

**Caminho:** `D:\IC2\ic1_legado\IControlIT\Chamado\Chamado_Data_Parada.aspx`

**Responsabilidade:** Registrar período de downtime que suspende SLA.

#### Campos

| Campo | Tipo | Obrigatório | Validação |
|-------|------|-------------|-----------|
| Data Início | DateTimePicker | Sim | Deve ser >= DataCriacao do chamado |
| Data Fim | DateTimePicker | Sim | Deve ser > Data Início |
| Motivo | TextArea | Não | Texto livre |

#### Comportamentos Implícitos

- **Recálculo manual de SLA**: Após registrar parada, SLA não é recalculado automaticamente
- **Sem validação de sobreposição**: Permite registrar múltiplas paradas com datas sobrepostas
- **Paradas sem auditoria**: Não registra quem criou ou alterou a parada
- **Sem limite de paradas**: Permite criar paradas infinitas (risco de abuso)

**DESTINO**: **ASSUMIDO COM MELHORIAS** - Manter funcionalidade mas adicionar recálculo automático de SLA e validação de sobreposição.

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

### 3.1 WebService: WSChamado.asmx

**Caminho:** `D:\IC2\ic1_legado\WS_IControlIT\WSChamado.asmx.vb`

**Responsabilidade:** API SOAP para integração externa (ServiceNow, aplicativos mobile legados).

| Método | Responsabilidade | Observações |
|--------|------------------|-------------|
| `Solicitacao_Incluir(xmlDados As String) As String` | Cria chamado via XML | Retorna XML com ID ou erro |
| `Solicitacao_Atualizar(xmlDados As String) As String` | Atualiza status/prioridade | Sem validação de transição de estado |
| `Solicitacao_Detalhes(idSolicitacao As Integer) As String` | Retorna DataSet em XML | Performance ruim (lazy loading N+1) |
| `Solicitacao_Lista(filtros As String) As String` | Lista paginada | Filtros em querystring encoded (inseguro) |
| `Solicitacao_SLA_Recalcular(idSolicitacao As Integer) As Boolean` | Recalcula SLA manualmente | Usado apenas em batch noturno |
| `Solicitacao_Atribuir_Fila(idSolicitacao As Integer, idFila As Integer) As Boolean` | Atribui à fila | Sem load balancing |

#### Comportamentos Implícitos

- **Autenticação Basic Auth**: Username/password em cada request (não usa token)
- **Sem rate limiting**: Possível abuse via flood de requests
- **XML parsing manual**: Vulnerável a XXE (XML External Entity) injection
- **Sem versionamento**: Qualquer mudança quebra clientes antigos
- **Erros genéricos**: Retorna "Erro" sem detalhes (dificulta debug)

**DESTINO**: **SUBSTITUÍDO** - REST API com JWT, OpenAPI/Swagger, versionamento semântico, erros estruturados.

---

### 3.2 WebService Handler: ServiceNow/Handler.asmx

**Caminho:** `D:\IC2\ic1_legado\WS_IControlIT\Connect\ServiceNow\Handler.asmx`

**Responsabilidade:** Recebe webhooks de ServiceNow e cria/atualiza chamados em IControlIT.

| Método | Responsabilidade |
|--------|------------------|
| `ProcessIncidentUpdate(xmlIncident As String) As String` | Mapeia incident ServiceNow → Solicitacao IControlIT |

#### Comportamentos Implícitos

- **Sincronização unidirecional**: ServiceNow → IControlIT (não o contrário)
- **Sem retry**: Se falhar, perde o webhook (não reprocessa)
- **Mapeamento manual**: Código VB.NET hardcoded para mapear campos
- **Sem validação de signature**: Aceita qualquer POST (risco de spoofing)

**DESTINO**: **SUBSTITUÍDO** - Integração bidirecional com mapeamento automático de tipos, retry com Polly, validação de signature HMAC.

---

## 4. STORED PROCEDURES

### 4.1 pa_Solicitacao_Incluir

**Caminho:** `D:\IC2\ic1_legado\Database\Procedures\pa_Solicitacao_Incluir.sql`

**Parâmetros:**
- `@Cd_Fornecedor INT`
- `@Cd_Usuario INT`
- `@Cd_Prioridade INT`
- `@Ds_Solicitacao VARCHAR(MAX)`
- `@Cd_Categoria INT`

**Lógica (em linguagem natural):**
1. Valida se `@Cd_Usuario` existe na tabela Usuario
2. Valida se `@Cd_Categoria` existe na tabela Solicitacao_Tipo
3. Calcula próximo número sequencial (SELECT MAX(Id_Solicitacao) + 1)
4. Insere registro em tabela `Solicitacao` com Status='Novo'
5. Calcula SLA baseado em `@Cd_Prioridade` (tabela Configuracao_SLA)
6. Insere registro em tabela `Solicitacao_SLA`
7. Retorna `Id_Solicitacao` gerado

**Problemas:**
- **Race condition**: MAX(Id) + 1 não é thread-safe (pode gerar duplicatas)
- **Sem transaction**: Se inserção de SLA falhar, chamado fica órfão
- **Validações espalhadas**: Parte em VB.NET, parte em SQL (inconsistente)

**DESTINO**: **SUBSTITUÍDO** - Lógica movida para `CreateTicketCommandHandler` (CQRS) com `IDbContextTransaction`, GUID em vez de INT sequencial.

---

### 4.2 pa_Solicitacao_SLA_Recalcular

**Caminho:** `D:\IC2\ic1_legado\Database\Procedures\pa_Solicitacao_SLA_Recalcular.sql`

**Parâmetros:**
- `@Id_Solicitacao INT` (NULL = recalcular todos)

**Lógica:**
1. Para cada chamado em aberto (Status != 'Fechado')
2. Calcula tempo decorrido (GETDATE() - Dt_Criacao)
3. Subtrai períodos de parada (tabela Solicitacao_Data_Parada)
4. Compara com Data esperada (tabela Solicitacao_SLA)
5. Atualiza Status SLA (NoPrazo/Risco/Vencido)

**Problemas:**
- **Performance**: Cursor SQL (RBAR - Row By Agonizing Row) em vez de set-based
- **Lock escalation**: Atualiza tabela inteira sem índices adequados (deadlocks)
- **Não considera horário comercial**: Calcula 24/7 (deveria respeitar expediente)

**DESTINO**: **SUBSTITUÍDO** - Job Hangfire com batch processing, índices otimizados, consideração de horário comercial.

---

### 4.3 pa_Solicitacao_Lista

**Caminho:** `D:\IC2\ic1_legado\Database\Procedures\pa_Solicitacao_Lista.sql`

**Parâmetros:**
- `@Cd_Fornecedor INT`
- `@Filtro_Status VARCHAR(20)` (NULL = todos)
- `@Filtro_Prioridade INT` (NULL = todos)
- `@PageNumber INT`
- `@PageSize INT`

**Lógica:**
1. Query principal com múltiplos JOINs (Usuario, Categoria, SLA)
2. Filtra por `@Cd_Fornecedor` (multi-tenancy)
3. Aplica filtros opcionais
4. Ordena por Dt_Criacao DESC
5. Aplica OFFSET/FETCH para paginação
6. Retorna recordset + total count (dois SELECTs)

**Problemas:**
- **N+1 queries**: Lista chamados depois faz loop em VB.NET para buscar anexos
- **Sem índices compostos**: OFFSET/FETCH lento em tabelas grandes (>100k registros)
- **Sem cache**: Query idêntica executada a cada 30 segundos (refresh automático)

**DESTINO**: **SUBSTITUÍDO** - Query LINQ com `Include()` para eager loading, índices compostos, cache Redis (5 minutos).

---

## 5. TABELAS LEGADAS

### 5.1 Tabela: Solicitacao

**Finalidade:** Armazenar dados principais do chamado.

**Problemas Identificados:**
- ❌ **Campo `Cd_Fornecedor` sem FK**: Permite inserir Fornecedor inexistente
- ❌ **Campo `St_Solicitacao` VARCHAR sem constraint**: Permite valores inválidos ("Pendente", "Aberto" não documentados)
- ❌ **Sem auditoria nativa**: Campos Created/Modified ausentes (apenas Dt_Criacao_SYS)
- ❌ **Soft delete manual**: `Fl_Excluido` sem índice (queries lentas com WHERE Fl_Excluido=0)
- ❌ **Sem campo ParentTicketId**: Reabertura não linkada ao chamado original
- ❌ **Índice faltando em Cd_Usuario_Atribuido**: Queries de "Meus Chamados" lentas

**Mapeamento para tabela moderna:**
```
Solicitacao (legado) → Ticket (moderno)
- Id_Solicitacao → Id (GUID)
- Cd_Fornecedor → ClienteId (FK com constraint)
- Cd_Usuario → SolicitanteId (FK)
- Cd_Usuario_Atribuido → TecnicoAtribuidoId (FK)
- Ds_Solicitacao → Descricao (nvarchar(max))
- St_Solicitacao → Status (Enum: Novo, Atribuído, etc)
- Fl_Excluido → IsDeleted (bit com índice)
- NOVO: ParentTicketId (FK para reabertura)
- NOVO: ExternalTicketId (ServiceNow sync)
- NOVO: Created, CreatedBy, LastModified, LastModifiedBy (auditoria)
```

**DESTINO**: **SUBSTITUÍDO** - Tabela redesenhada com multi-tenancy nativo, auditoria automática, soft delete indexado.

---

### 5.2 Tabela: Solicitacao_SLA

**Finalidade:** Armazenar datas de SLA esperadas e reais.

**Problemas:**
- ❌ **Sem FK cascade**: Deletar Solicitacao não deleta SLA (dados órfãos)
- ❌ **Campo `St_SLA` VARCHAR**: Permite valores inválidos
- ❌ **Sem histórico de mudanças**: Não registra quando SLA mudou de "NoPrazo" para "Vencido"
- ❌ **Não armazena pausas**: Paradas calculadas on-the-fly (ineficiente)

**Mapeamento:**
```
Solicitacao_SLA → TicketSLA
- Id_SLA → Id (GUID)
- Id_Solicitacao → TicketId (FK)
- Dt_Resposta_Esperada → DataRespostaEsperada
- Dt_Resolucao_Esperada → DataResolucaoEsperada
- St_SLA → Status (Enum: NoPrazo, Risco, Vencido)
- NOVO: TempoSuspenso (TimeSpan - total de pausas)
```

**DESTINO**: **SUBSTITUÍDO** - FK com cascade, enum constraint, campo TempoSuspenso pré-calculado.

---

### 5.3 Tabela: Solicitacao_Data_Parada

**Finalidade:** Registrar períodos de downtime que suspendem SLA.

**Problemas:**
- ❌ **Sem validação Dt_Fim > Dt_Inicio**: Permite datas inconsistentes
- ❌ **Sem auditoria**: Não registra quem criou/alterou a parada
- ❌ **Sem validação de sobreposição**: Permite múltiplas paradas com datas sobrepostas

**Mapeamento:**
```
Solicitacao_Data_Parada → TicketDowntime
- Id_Parada → Id (GUID)
- Id_Solicitacao → TicketId (FK)
- Dt_Inicio → DataInicio (DateTime UTC)
- Dt_Fim → DataFim (DateTime UTC, nullable durante parada ativa)
- Ds_Motivo → MotivoParada
- NOVO: Created, CreatedBy (auditoria)
```

**DESTINO**: **ASSUMIDO COM MELHORIAS** - Adicionar constraints CHECK (DataFim > DataInicio), auditoria, validação de sobreposição no handler.

---

### 5.4 Tabela: Solicitacao_Fila_Atendimento

**Finalidade:** Agrupar técnicos por especialidade (skill set).

**Problemas:**
- ❌ **Sem relação N:N com técnicos**: Lista de IDs em campo VARCHAR (ineficiente)
- ❌ **Sem skill set estruturado**: Apenas nome da fila (não mapeia categorias)

**Mapeamento:**
```
Solicitacao_Fila_Atendimento → QueueAtendimento + QueueTecnico (tabela junction N:N)
- Id_Fila → Id (GUID)
- Nm_Fila → Nome
- NOVO: SkillSet (JSON ou tabela normalizada)
- NOVO: Tabela junction QueueTecnico (QueueId, TecnicoId)
```

**DESTINO**: **ASSUMIDO COM MELHORIAS** - Normalizar relação N:N, adicionar mapeamento automático categoria → fila.

---

## 6. REGRAS DE NEGÓCIO IMPLÍCITAS

### RL-RN-001: Número de chamado sequencial por cliente

**Fonte:** `pa_Solicitacao_Incluir.sql` - Linha 45
**Descrição:** Número do chamado é gerado como `SELECT MAX(Id_Solicitacao) + 1 WHERE Cd_Fornecedor = @Cd_Fornecedor`. Formato exibido: `CHD-YYYY-NNN` (ex: CHD-2025-001).

**Destino:** **ASSUMIDO** - Manter numeração sequencial mas usar SEQUENCE do SQL Server (thread-safe) em vez de MAX+1.

---

### RL-RN-002: Prioridade fixa por cliente específico

**Fonte:** `Chamado.aspx.vb` - Linha 123 (hardcoded)
**Descrição:** Cliente "Empresa XYZ" (Cd_Fornecedor=5) sempre recebe prioridade P1, independente de impacto/urgência.

**Destino:** **DESCARTADO** - Regra de exceção não documentada, será substituída por matriz Impacto x Urgência universal.

---

### RL-RN-003: SLA pausa durante finais de semana

**Fonte:** `pa_Solicitacao_SLA_Recalcular.sql` - Linha 78
**Descrição:** Se chamado criado na sexta-feira após 18h, SLA só começa a contar na segunda-feira 08h.

**Destino:** **ASSUMIDO** - Regra válida, será configurável via `HorarioComercial` (tabela `Configuracao_SLA`).

---

### RL-RN-004: Comentários com palavra "urgente" escalam automaticamente

**Fonte:** `Chamado_Consulta.aspx.vb` - Linha 234
**Descrição:** Se comentário contém palavra-chave "urgente" ou "crítico", prioridade é automaticamente elevada para P1.

**Destino:** **DESCARTADO** - Regra não documentada e facilmente abusável. Substituir por escalação manual via Manager.

---

### RL-RN-005: Técnico não pode fechar próprio chamado

**Fonte:** `Chamado_Consulta.aspx.vb` - Linha 567
**Descrição:** Se usuário logado é o técnico atribuído, botão "Fechar" fica desabilitado. Apenas Manager pode fechar.

**Destino:** **DESCARTADO** - Regra restritiva sem justificativa. Moderno permitirá técnico fechar após resolver (status Resolvido → Fechado automático após 24h sem reabertura).

---

### RL-RN-006: Anexos maiores que 10MB enviados via FTP

**Fonte:** `Chamado_Solicitacao.aspx.vb` - Linha 345
**Descrição:** Upload > 10MB falha com mensagem "Enviar via FTP para servidor X". Não há interface FTP no sistema.

**Destino:** **DESCARTADO** - Workaround manual descontinuado. Moderno permitirá até 5MB via blob storage (Azure), acima disso usar link externo (OneDrive/SharePoint).

---

### RL-RN-007: Reabertura dentro de 48h não gera novo chamado

**Fonte:** `Chamado.aspx.vb` - Linha 789
**Descrição:** Se cliente reabre chamado fechado dentro de 48h, apenas reverte status para "Em Andamento" (não cria novo). Após 48h, cria novo.

**Destino:** **A_REVISAR** - Regra de janela temporal pode ser válida, mas precisa decisão de negócio se 48h é adequado ou se sempre criar novo.

---

### RL-RN-008: Primeiro comentário técnico define data de resposta

**Fonte:** `pa_Solicitacao_Atualizar.sql` - Linha 123
**Descrição:** Campo `Dt_Resposta_Real` é preenchido no momento do primeiro comentário de um técnico (não no momento da atribuição).

**Destino:** **ASSUMIDO** - Regra válida. Atribuição automática não conta como resposta; apenas comentário explícito.

---

### RL-RN-009: Chamados P1 sem resposta em 30 min escalam para CEO

**Fonte:** Job SQL Agent "Escalacao_P1" (não documentado)
**Descrição:** Job SQL roda a cada 10 minutos, busca P1 sem resposta há mais de 30 min, envia email para CEO.

**Destino:** **ASSUMIDO COM MELHORIAS** - Regra válida mas email para CEO é excessivo. Moderno escalará para Supervisor da fila, depois Manager, depois CEO (3 níveis).

---

### RL-RN-010: Integração ServiceNow só para cliente "Banco ABC"

**Fonte:** Web.config `<appSettings key="ServiceNow_ClienteId" value="12"/>`
**Descrição:** Sincronização com ServiceNow habilitada apenas para cliente específico (Cd_Fornecedor=12).

**Destino:** **ASSUMIDO** - Integração será configurável via Feature Flag (`SERVICEDESK_SERVICENOW_SYNC`) ativada por cliente.

---

## 7. GAP ANALYSIS (LEGADO x RF MODERNO)

| Item | Legado | RF Moderno | Observação |
|------|--------|------------|------------|
| **Priorização** | Manual (usuário escolhe P1-P4) | Automática via matriz Impacto x Urgência | Modernização melhora padronização |
| **Atribuição** | Manual (Manager escolhe técnico) | Skill-based routing automático | Modernização reduz tempo de atribuição |
| **SLA Cálculo** | Recalculado a cada page load (lento) | Pré-calculado via job Hangfire (5 min) | Modernização melhora performance |
| **Comentários** | Sem distinção interno/externo | Interno (equipe) vs Externo (cliente) | Modernização melhora comunicação |
| **Anexos** | Upload direto filesystem (inseguro) | Azure Blob Storage + antivírus | Modernização melhora segurança |
| **Auditoria** | Triggers SQL (incompleta) | Middleware + tabela estruturada | Modernização melhora rastreabilidade |
| **Multi-tenancy** | Multi-database (ineficiente) | Single database com ClienteId (RLS) | Modernização simplifica manutenção |
| **API** | SOAP (.asmx) com XML | REST com JSON + OpenAPI | Modernização melhora integração |
| **Notificações** | Email + refresh manual (30s) | SignalR real-time + Email | Modernização melhora UX |
| **Reabertura** | Edita chamado original (perde histórico) | Cria novo linkado (preserva histórico) | Modernização melhora auditoria |
| **Paradas** | Recálculo manual de SLA | Recálculo automático via job | Modernização reduz erro humano |
| **ServiceNow Sync** | Unidirecional (Snow → IC) | Bidirecional (Snow ↔ IC) | Modernização melhora consistência |

---

## 8. DECISÕES DE MODERNIZAÇÃO

### Decisão 1: Substituir Priorização Manual por Matriz Automática

**Motivo:** Priorização manual sujeita a viés humano, inconsistência entre solicitantes. Matriz Impacto x Urgência (ITIL v4) padroniza e acelera.

**Impacto:** Alto - Usuários precisarão se adaptar ao cálculo automático (treinamento necessário).

---

### Decisão 2: Migrar de Multi-database para Single Database Multi-tenant

**Motivo:** Manutenção de 50+ bancos separados é insustentável. Single database com Row-Level Security (ClienteId) reduz custo operacional.

**Impacto:** Alto - Migração de dados complexa, risco de vazamento de dados entre tenants se RLS falhar.

---

### Decisão 3: Substituir SOAP por REST API

**Motivo:** SOAP está obsoleto, verboso, difícil de integrar. REST com JSON é padrão de mercado, compatível com mobile/SPA.

**Impacto:** Médio - Clientes com integrações SOAP precisarão migrar (deprecação gradual: 12 meses).

---

### Decisão 4: Adicionar Skill-Based Routing Automático

**Motivo:** Atribuição manual lenta, não considera carga de técnicos. Routing automático melhora SLA compliance.

**Impacto:** Médio - Requer mapeamento inicial categoria → skill set (trabalho manual de configuração).

---

### Decisão 5: Armazenar Anexos em Azure Blob Storage

**Motivo:** Filesystem local não escala, sem backup redundante, risco de perda. Blob Storage oferece CDN, versionamento, geo-replicação.

**Impacto:** Baixo - Custo adicional Azure (~$0.02/GB/mês), mas compensa em confiabilidade.

---

## 9. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Mitigação |
|-------|---------|-----------|
| **Perda de dados durante migração multi-database → single** | Crítico | Dry-run em ambiente de teste, validação de integridade pós-migração, backup completo |
| **Vazamento de dados entre tenants (RLS mal configurado)** | Crítico | Testes de segurança extensivos, auditoria de queries, policy enforcement no EF Core |
| **Quebra de integrações SOAP existentes** | Alto | Manter SOAP API como legacy endpoint (deprecated) por 12 meses durante transição |
| **SLA recalculado incorretamente (lógica diferente do legado)** | Alto | Comparação side-by-side legado vs moderno durante pilot (3 meses), ajuste de fórmulas |
| **Skill-based routing atribui técnico errado** | Médio | Fallback para fila geral + atribuição manual de Manager se routing falhar |
| **Anexos perdidos durante migração filesystem → blob** | Médio | Upload dual (filesystem + blob) durante período de transição (6 meses) |
| **Performance degradada em clientes grandes (>100k chamados)** | Médio | Índices compostos, particionamento de tabelas, cache Redis, CDN para estáticos |
| **Usuários não adaptados a nova UX (Angular vs WebForms)** | Baixo | Treinamento obrigatório, guia interativo (onboarding), suporte dedicado 1º mês |

---

## 10. RASTREABILIDADE

| Elemento Legado | Referência RF Moderno |
|-----------------|----------------------|
| Tela `Chamado.aspx` | RN-RF073-01 (Campos obrigatórios), UC00-RF073 (Listar chamados) |
| Tela `Chamado_Consulta.aspx` | RN-RF073-07 (Comentários internos/externos), UC02-RF073 (Visualizar detalhes) |
| Tela `Chamado_Solicitacao.aspx` | RN-RF073-02 (Priorização automática), UC01-RF073 (Criar chamado) |
| Procedure `pa_Solicitacao_Incluir` | RN-RF073-01, RN-RF073-03 (SLA baseado em prioridade) |
| Procedure `pa_Solicitacao_SLA_Recalcular` | RN-RF073-06 (Recálculo periódico), RN-RF073-04 (Pausas de SLA) |
| WebService `WSChamado.asmx` | API REST `/api/tickets` (endpoints modernos) |
| Handler `ServiceNow/Handler.asmx` | RN-RF073-10 (Integração ServiceNow bidirecional) |
| Tabela `Solicitacao` | Entidade `Ticket` (Modelo de Dados MD-RF073.md) |
| Tabela `Solicitacao_SLA` | Entidade `TicketSLA` |
| Tabela `Solicitacao_Data_Parada` | Entidade `TicketDowntime` |
| Regra implícita RL-RN-003 | RN-RF073-03 (SLA considerando horário comercial) |
| Regra implícita RL-RN-008 | RN-RF073-03 (Primeiro comentário técnico define resposta) |
| Regra implícita RL-RN-009 | RN-RF073-06 (Escalação automática de P1) |

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|--------|------|-----------|-------|
| 1.0 | 2025-12-30 | Documentação inicial de referência ao legado - 6 telas, 3 webservices, 6 stored procedures, 5 tabelas, 10 regras implícitas | Agência ALC - alc.dev.br |

---

**Última Atualização**: 2025-12-30
**Autor**: Agência ALC - alc.dev.br
**Objetivo**: Memória técnica completa do legado VB.NET/ASPX para garantir rastreabilidade e mitigação de riscos na modernização
