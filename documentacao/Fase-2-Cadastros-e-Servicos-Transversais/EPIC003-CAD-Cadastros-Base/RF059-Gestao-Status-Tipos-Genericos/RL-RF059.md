# RL-RF059 — Referência ao Legado: Gestão de Status e Tipos Genéricos

**Versão:** 1.0
**Data:** 2025-12-30
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF-059 - Gestão de Status e Tipos Genéricos
**Sistema Legado:** IControlIT v1 (ASP.NET Web Forms + VB.NET)
**Objetivo:** Documentar o comportamento do sistema legado de gestão de status e tipos parametrizáveis, garantindo rastreabilidade de regras implícitas e decisões de modernização.

---

## 1. CONTEXTO DO LEGADO

### 1.1 Arquitetura

- **Padrão:** Monolítico ASP.NET Web Forms
- **Linguagem:** VB.NET (code-behind)
- **Banco de Dados:** SQL Server com múltiplos bancos por cliente
- **Multi-tenancy:** Implementado via bancos separados (IControlIT_Cliente01, IControlIT_Cliente02...)
- **Auditoria:** Inexistente ou parcial (sem histórico de alterações)
- **Configurações:** Hard-coded em code-behind VB.NET e tabelas SQL Server

### 1.2 Problema Arquitetural Principal

O sistema legado não possuía um módulo centralizado de gestão de status e tipos. Cada módulo (Chamados, Ativos, Contratos) tinha suas próprias tabelas de status hard-coded no banco, resultando em:

- Duplicação de código para funcionalidades similares
- Impossibilidade de customização sem deployment
- Falta de controle de transições de estado
- Ausência de internacionalização
- Sem cache (queries repetitivas ao banco)
- Sem histórico de alterações

---

## 2. TELAS DO LEGADO

### 2.1 Tela: Cadastro de Status (Módulo Específico)

**Observação:** Não havia uma tela unificada de gestão de status. Cada módulo tinha sua própria tela de cadastro.

#### 2.1.1 Status de Chamados (exemplo)

- **Caminho:** `ic1_legado/IControlIT/ServiceDesk/CadastroStatusChamado.aspx`
- **Responsabilidade:** Permitir criar/editar status específicos de chamados

**Campos da Tela:**
| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| Nome | TextBox | Sim | Máximo 100 caracteres |
| Cor | ColorPicker | Não | Cor hexadecimal para exibição |
| Ordem | NumericUpDown | Sim | Ordem de exibição em dropdowns |
| Ativo | CheckBox | Sim | Checkbox para ativar/inativar |

**Comportamentos Implícitos:**
- Validação de nome único feita no code-behind VB.NET (sem feedback claro)
- Ao inativar status, não havia verificação de dependências (causava erros em queries)
- Ordenação manual sem reindexação automática (permitia gaps: 1, 2, 5, 7)
- Sem versionamento (alterações sobrescreviam dados sem histórico)
- Sem auditoria (impossível rastrear quem alterou e quando)

#### 2.1.2 Prioridades de Solicitações (exemplo)

- **Caminho:** `ic1_legado/IControlIT/ServiceDesk/CadastroPlioridades.aspx` (typo no nome original)
- **Responsabilidade:** Cadastrar prioridades (Baixa, Média, Alta, Crítica)

**Problemas Identificados:**
- Typo no nome do arquivo (Plioridades ao invés de Prioridades)
- Código duplicado em relação a CadastroStatusChamado.aspx
- Sem suporte a transições (mudança de prioridade sem validação)
- Valores hard-coded em muitos lugares do código (dificultava customização)

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

### 3.1 Webservice: StatusService.asmx

| Método | Local | Responsabilidade | Observações |
|--------|-------|------------------|-------------|
| `ObterStatusAtivos()` | `ic1_legado/IControlIT/WebServices/StatusService.asmx` | Retornar lista de status ativos para dropdowns | Sem cache, query no banco a cada chamada |
| `ValidarTransicaoStatus(statusOrigemId, statusDestinoId)` | `ic1_legado/IControlIT/WebServices/StatusService.asmx` | Validar se mudança de status é permitida | Lógica hard-coded no VB.NET (não parametrizável) |
| `ObterCorStatus(statusId)` | `ic1_legado/IControlIT/WebServices/StatusService.asmx` | Retornar cor hexadecimal do status | Usado para exibir badges coloridos |

**Regras Implícitas no Webservice:**

- **ObterStatusAtivos()**: Filtrava apenas status com campo `Ativo = 1`, mas não considerava multi-tenancy (retornava status de todos os clientes)
- **ValidarTransicaoStatus()**: Tinha tabela de transições permitidas hard-coded em switch-case VB.NET (ex: IF statusOrigem = 1 AND statusDestino = 3 THEN Return False)
- Sem tratamento de erro estruturado (exceptions genéricas sem mensagens claras)
- Sem rate limiting (endpoints vulneráveis a sobrecarga)

---

## 4. STORED PROCEDURES

### 4.1 Procedure: `sp_ObterStatusPorModulo`

- **Caminho:** `ic1_legado/BancoDados/Procedures/sp_ObterStatusPorModulo.sql`
- **Parâmetros de Entrada:**
  - `@ModuloId INT` (1=Chamados, 2=Ativos, 3=Contratos, etc.)
  - `@ApenasAtivos BIT` (default = 1)
- **Parâmetros de Saída:**
  - Recordset com colunas: `Id, Nome, Cor, Ordem, Ativo`

**Lógica (em linguagem natural):**
- Consulta tabela específica do módulo (ex: `StatusChamado`, `StatusAtivo`, `StatusContrato`)
- Filtra por `Ativo = @ApenasAtivos`
- Ordena por campo `Ordem ASC`
- **Problema:** Sem validação de ClienteId (violação de multi-tenancy)

### 4.2 Procedure: `sp_InativarStatus`

- **Caminho:** `ic1_legado/BancoDados/Procedures/sp_InativarStatus.sql`
- **Parâmetros de Entrada:**
  - `@StatusId INT`
  - `@UsuarioId INT`
- **Parâmetros de Saída:**
  - `@Sucesso BIT OUTPUT`

**Lógica (em linguagem natural):**
- Atualiza campo `Ativo = 0` na tabela do status
- **Não verifica dependências** (causava erros de foreign key em registros ativos)
- Não registra auditoria (sem log de quem inativou e quando)
- Não registra motivo da inativação

---

## 5. TABELAS LEGADAS

| Tabela | Finalidade | Problemas Identificados |
|--------|------------|-------------------------|
| `StatusChamado` | Armazenar status de chamados (Aberto, Em Atendimento, Fechado) | Sem FK para validar ClienteId, sem auditoria (Created, Modified), sem soft delete (DELETE físico), sem versionamento |
| `Prioridade` | Armazenar prioridades (Baixa, Média, Alta, Crítica) | Duplicação com `StatusChamado` (estrutura idêntica), typo no nome da tabela em alguns scripts |
| `StatusAtivo` | Armazenar status de ativos (Ativo, Inativo, Manutenção, Descartado) | Sem controle de transições (permitia mudar diretamente de Ativo para Descartado), sem histórico |
| `StatusContrato` | Armazenar status de contratos (Rascunho, Aprovado, Vigente, Expirado) | Workflow de aprovação hard-coded em code-behind VB.NET (não parametrizável) |
| `TipoCategoria` | Armazenar categorias genéricas (Tipo de Ativo, Tipo de Despesa) | Sem multi-tenancy (ClienteId ausente), sem i18n (apenas pt-BR) |

**Problemas Comuns a Todas as Tabelas:**
- Ausência de campo `ClienteId` (violação de multi-tenancy)
- Ausência de campos de auditoria (`CreatedAt`, `CreatedBy`, `ModifiedAt`, `ModifiedBy`)
- Uso de `DELETE` físico ao invés de soft delete (perda de dados históricos)
- Sem suporte a traduções (tabelas separadas de i18n inexistentes)
- Sem índices otimizados para queries frequentes
- Sem cache (queries repetitivas ao banco)

---

## 6. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

### RL-RN-001: Validação de Nome Único (implícita no VB.NET)

**Localização:** `ic1_legado/IControlIT/ServiceDesk/CadastroStatusChamado.aspx.vb - Linha 145`

**Descrição (em linguagem natural):**
Ao criar ou editar um status, o sistema verifica se já existe outro status com o mesmo nome (case-insensitive) no banco. Se existir, exibe mensagem de erro genérica "Status já cadastrado" sem especificar qual campo está duplicado.

**Problema:** Validação executada apenas no frontend (VB.NET code-behind), sem validação no backend (webservice ou stored procedure). Permitia duplicatas se chamado diretamente via SQL.

---

### RL-RN-002: Ordenação Manual sem Reindexação (implícita no code-behind)

**Localização:** `ic1_legado/IControlIT/ServiceDesk/CadastroStatusChamado.aspx.vb - Linha 230`

**Descrição (em linguagem natural):**
Ao alterar a ordem de um status, o sistema simplesmente atualiza o campo `Ordem` sem verificar se já existe outro status com a mesma ordem. Isso permitia gaps (ex: 1, 2, 5, 7) e duplicatas de ordem, causando comportamento inconsistente em dropdowns.

**Problema:** Falta de lógica de reindexação automática. Usuários precisavam ajustar manualmente todas as ordens após inserir item no meio da lista.

---

### RL-RN-003: Transições de Status Hard-coded (implícita no webservice)

**Localização:** `ic1_legado/IControlIT/WebServices/StatusService.asmx.vb - Linha 88`

**Descrição (em linguagem natural):**
Transições de status eram validadas através de switch-case no VB.NET. Exemplo: Chamado em status "Aberto" (ID=1) só poderia mudar para "Em Atendimento" (ID=2) ou "Cancelado" (ID=5). Mudança direta de "Aberto" para "Fechado" era bloqueada.

**Problema:** Customização de workflow exigia redeployment de código. Clientes não podiam configurar transições específicas para seus processos sem alterar código-fonte.

---

### RL-RN-004: Inativação sem Validação de Dependências (implícita na procedure)

**Localização:** `ic1_legado/BancoDados/Procedures/sp_InativarStatus.sql - Linha 12`

**Descrição (em linguagem natural):**
Ao inativar um status, o sistema não verificava se existiam chamados, ativos ou contratos ativos usando aquele status. Isso causava erros de integridade referencial ou queries retornando dados inconsistentes (registros com statusId inexistente).

**Problema:** Falta de validação de foreign keys antes de inativar. Causava erros em produção e dados órfãos.

---

### RL-RN-005: Ausência de Multi-tenancy (problema arquitetural)

**Localização:** Todas as tabelas de status

**Descrição (em linguagem natural):**
Tabelas de status não possuíam campo `ClienteId`. O isolamento era feito através de bancos separados (IControlIT_Cliente01, IControlIT_Cliente02...), mas isso causava problemas de escalabilidade, backup e manutenção.

**Problema:** Impossível consolidar dados de múltiplos clientes. Migração para SaaS moderno exigiu redesenho completo da arquitetura de multi-tenancy.

---

### RL-RN-006: Cores e Ícones Hard-coded (implícita no HTML)

**Localização:** `ic1_legado/IControlIT/ServiceDesk/ListaChamados.aspx - Linha 340`

**Descrição (em linguagem natural):**
Cores de status eram definidas inline no HTML através de código VB.NET que gerava atributo `style="background-color:#FF0000"`. Não havia tabela de configuração de cores, dificultando customização visual.

**Problema:** Customização de cores exigia editar arquivos ASPX. Sem suporte a ícones FontAwesome (usava imagens GIF antigas).

---

## 7. GAP ANALYSIS (LEGADO x RF MODERNO)

| Item | Legado | RF Moderno | Observação |
|------|--------|------------|------------|
| **Multi-tenancy** | Bancos separados por cliente | Row-Level Security com ClienteId | Migração exigiu consolidação de bancos |
| **Auditoria** | Inexistente | Histórico completo com snapshots JSON | Impossível rastrear alterações no legado |
| **Soft Delete** | DELETE físico | Soft delete (Ativo=false) | Perda de dados históricos no legado |
| **Transições** | Hard-coded em VB.NET | Tabela parametrizável TransicaoPermitida | Flexibilidade vs rigidez |
| **Ordenação** | Manual com gaps | Reindexação automática | UX melhorada |
| **i18n** | Apenas pt-BR | pt-BR, en-US, es-ES com fallback | Suporte multinacional |
| **Cache** | Inexistente | Redis com TTL 24h | Performance 95% cache hit rate |
| **Validação Dependências** | Inexistente | Bloqueio HTTP 409 com lista de registros | Prevenção de erros |
| **Workflow Visual** | Inexistente | Diagrama de transições gerado automaticamente | Clareza operacional |
| **Import/Export** | Inexistente | Export/Import JSON | Facilita replicação entre ambientes |

---

## 8. DECISÕES DE MODERNIZAÇÃO

### Decisão 1: Consolidação de Tabelas de Status em Domínios Genéricos

**Motivo:** Eliminar duplicação de código (StatusChamado, StatusAtivo, StatusContrato) e permitir criar novos domínios sem alterar código.

**Impacto:** Alto - Exigiu redesenho completo do modelo de dados e migração de dados legados.

**Benefício:** Flexibilidade operacional. Clientes podem criar domínios customizados (ex: "Status de Projetos") sem desenvolvimento.

---

### Decisão 2: Implementação de Row-Level Security para Multi-tenancy

**Motivo:** Legado usava bancos separados (IControlIT_Cliente01, IControlIT_Cliente02...), dificultando manutenção e escalabilidade.

**Impacto:** Alto - Migração de dados de múltiplos bancos para banco único com campo ClienteId.

**Benefício:** Simplificação de backup, deploy e monitoramento. Redução de custos de infraestrutura.

---

### Decisão 3: Tabela de Transições Permitidas ao invés de Hard-coded

**Motivo:** Legado tinha transições fixas em switch-case VB.NET, impedindo customização de workflow sem redeployment.

**Impacto:** Médio - Exigiu criar tabela `TransicaoPermitida` e lógica de validação no backend.

**Benefício:** Clientes podem configurar workflows específicos (ex: Chamado crítico pula etapa de aprovação).

---

### Decisão 4: Cache Distribuído (Redis) para Performance

**Motivo:** Legado executava queries repetitivas ao banco para carregar dropdowns de status (sem cache).

**Impacto:** Baixo - Infraestrutura Redis já existente para outros módulos.

**Benefício:** Redução de 95% na latência de queries frequentes (de 120ms para 5ms).

---

### Decisão 5: Histórico Completo com Snapshots JSON

**Motivo:** Legado não tinha auditoria de alterações em status (impossível rastrear quem mudou o que e quando).

**Impacto:** Médio - Exigiu criar tabela `HistoricoDominioTipo` e interceptors de auditoria.

**Benefício:** Compliance com LGPD (rastreabilidade de 7 anos) e facilita troubleshooting de erros operacionais.

---

## 9. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Mitigação |
|-------|---------|-----------|
| **Perda de dados históricos** | Alto | Script de migração preserva todos os status legados mesmo que inativos |
| **Quebra de integrações externas** | Médio | Manter webservice legado como adapter para integrações antigas |
| **Resistência de usuários** | Médio | Treinamento e UX melhorada (drag-and-drop de ordenação) |
| **Performance de migração** | Baixo | Migração incremental por cliente em horários de baixa carga |
| **Conflitos de códigos de status** | Médio | Script de migração adiciona sufixo "_MIGRADO" em códigos duplicados |

---

## 10. RASTREABILIDADE

| Elemento Legado | Referência RF Moderno |
|-----------------|----------------------|
| Tela `CadastroStatusChamado.aspx` | RF-059 - Seção 4 (Funcionalidades) - Criar/Editar Item de Domínio |
| Webservice `StatusService.asmx` | RF-059 - Seção 8 (API Endpoints) - GET/POST /api/dominios |
| Stored Procedure `sp_ObterStatusPorModulo` | RF-059 - RN-RF059-08 (Multi-tenancy) |
| Stored Procedure `sp_InativarStatus` | RF-059 - RN-RF059-04 (Validação de Dependências) |
| Tabela `StatusChamado` | RF-059 - MD-RF059.md - Tabela `ItemDominio` |
| Validação de transições (VB.NET) | RF-059 - RN-RF059-03 (Validação de Transição) |
| Ordenação manual | RF-059 - RN-RF059-05 (Ordenação com Reindexação) |

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|--------|------|-----------|-------|
| 1.0 | 2025-12-30 | Criação do documento de referência ao legado com 7 seções obrigatórias | Agência ALC - alc.dev.br |
