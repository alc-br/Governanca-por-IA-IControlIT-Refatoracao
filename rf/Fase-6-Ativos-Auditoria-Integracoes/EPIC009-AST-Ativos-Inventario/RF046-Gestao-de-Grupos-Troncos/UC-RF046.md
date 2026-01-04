# UC-RF046 — Casos de Uso Canônicos

**RF:** RF046 — Gestão de Grupos de Troncos
**Epic:** EPIC009-AST - Ativos e Inventário
**Fase:** Fase 6 - Ativos, Auditoria e Integrações
**Versão:** 2.0
**Data:** 2025-12-31
**Autor:** Agência ALC - alc.dev.br

---

## 1. OBJETIVO DO DOCUMENTO

Este documento descreve **todos os Casos de Uso (UC)** derivados do **RF046**, cobrindo integralmente o comportamento funcional esperado do sistema de gestão de grupos de troncos telefônicos.

Os UCs aqui definidos servem como **contrato comportamental**, sendo a **fonte primária** para geração de:
- Casos de Teste (TC-RF046.yaml)
- Massas de Teste (MT-RF046.yaml)
- Evidências de auditoria e validação funcional
- Execução por agentes de IA (tester, QA, E2E)

---

## 2. SUMÁRIO DE CASOS DE USO

| ID | Nome | Ator Principal |
|----|------|----------------|
| UC00 | Listar Grupos de Troncos | Usuário Autenticado |
| UC01 | Criar Grupo de Troncos | Usuário Autenticado |
| UC02 | Visualizar Grupo de Troncos | Usuário Autenticado |
| UC03 | Editar Grupo de Troncos | Usuário Autenticado |
| UC04 | Inativar Grupo de Troncos | Usuário Autenticado |

---

## 3. PADRÕES GERAIS APLICÁVEIS A TODOS OS UCs

- Todos os acessos respeitam **isolamento por tenant (FornecedorId)**
- Todas as ações exigem **permissão explícita** (RBAC com AST.GRUPOS_TRONCOS.*)
- Erros não devem vazar informações sensíveis
- Auditoria deve registrar **quem**, **quando** e **qual ação** (campos obrigatórios: CreatedBy, CreatedAt, LastModifiedBy, LastModifiedAt)
- Mensagens devem ser claras, previsíveis e rastreáveis
- **Soft delete obrigatório** (FlExcluido = TRUE, nunca DELETE físico)
- Health checks automáticos a cada 30 segundos (configurável, mínimo 10s)
- Failover automático em menos de 5 segundos após detecção de falha
- Notificações imediatas em caso de failover (e-mail + SMS)
- Histórico de 7 anos para auditoria de logs de failover e uso

---

## UC00 — Listar Grupos de Troncos

### Objetivo
Permitir que o usuário visualize todos os grupos de troncos do seu tenant com informações de status, capacidade e uso em tempo real.

### Pré-condições
- Usuário autenticado
- Permissão `AST.GRUPOS_TRONCOS.LIST`

### Pós-condições
- Lista exibida conforme filtros, paginação e isolamento por FornecedorId

### Fluxo Principal
- **FP-UC00-001:** Usuário acessa a funcionalidade de grupos de troncos
- **FP-UC00-002:** Sistema valida permissão AST.GRUPOS_TRONCOS.LIST
- **FP-UC00-003:** Sistema carrega registros do tenant (filtro FornecedorId)
- **FP-UC00-004:** Sistema aplica paginação (padrão 20 registros) e ordenação
- **FP-UC00-005:** Sistema exibe lista com colunas: Nome, Tipo, Algoritmo Balanceamento, Qtd Troncos Ativos, Concurrent Calls Atual, Capacidade Total, Status, Ações

### Fluxos Alternativos
- **FA-UC00-001:** Buscar por nome ou tipo de grupo
- **FA-UC00-002:** Ordenar por coluna (nome, tipo, capacidade, uso atual)
- **FA-UC00-003:** Filtrar por status (ATIVO, INATIVO, MANUTENCAO)
- **FA-UC00-004:** Filtrar por algoritmo de balanceamento (ROUND_ROBIN, LEAST_USED, WEIGHTED, PRIORITY, LCR)
- **FA-UC00-005:** Visualizar dashboard em tempo real via SignalR (atualização automática de concurrent calls e status)

### Fluxos de Exceção
- **FE-UC00-001:** Usuário sem permissão → HTTP 403 Forbidden
- **FE-UC00-002:** Nenhum registro encontrado → estado vazio exibido com mensagem "Nenhum grupo de troncos cadastrado"

### Regras de Negócio
- **RN-UC00-001:** Somente registros do tenant (FornecedorId) do usuário autenticado
- **RN-UC00-002:** Registros com FlExcluido=TRUE (soft-deleted) não aparecem na listagem
- **RN-UC00-003:** Paginação padrão de 20 registros por página
- **RN-UC00-004:** Informações de uso (concurrent calls) são atualizadas em tempo real via SignalR

### Critérios de Aceite
- **CA-UC00-001:** A lista DEVE exibir apenas registros do tenant do usuário autenticado (FornecedorId)
- **CA-UC00-002:** Registros excluídos (FlExcluido=TRUE) NÃO devem aparecer na listagem
- **CA-UC00-003:** Paginação DEVE ser aplicada com limite padrão de 20 registros
- **CA-UC00-004:** Sistema DEVE permitir ordenação por qualquer coluna visível
- **CA-UC00-005:** Filtros DEVEM ser acumuláveis e refletir na URL
- **CA-UC00-006:** Concurrent calls atual DEVE ser atualizado em tempo real (SignalR)
- **CA-UC00-007:** Status de saúde de troncos DEVE ser visível (indicador visual ATIVO/FALHA)

---

## UC01 — Criar Grupo de Troncos

### Objetivo
Permitir a criação de um novo grupo de troncos com configurações de balanceamento, failover e monitoramento.

### Pré-condições
- Usuário autenticado
- Permissão `AST.GRUPOS_TRONCOS.CREATE`

### Pós-condições
- Grupo de troncos criado no banco de dados
- Auditoria registrada (CreatedBy, CreatedAt)
- FornecedorId preenchido automaticamente com tenant do usuário
- Evento de domínio publicado: `GrupoTronco.Criado`

### Fluxo Principal
- **FP-UC01-001:** Usuário clica em "Novo Grupo de Troncos"
- **FP-UC01-002:** Sistema valida permissão AST.GRUPOS_TRONCOS.CREATE
- **FP-UC01-003:** Sistema exibe formulário com campos obrigatórios e opcionais
- **FP-UC01-004:** Usuário informa dados do grupo (nome, tipo, algoritmo, capacidade, intervalo health check)
- **FP-UC01-005:** Sistema valida dados conforme RN-RF046-001 a RN-RF046-015
- **FP-UC01-006:** Sistema cria registro com FornecedorId = tenant do usuário
- **FP-UC01-007:** Sistema registra auditoria (CreatedBy, CreatedAt)
- **FP-UC01-008:** Sistema publica evento `GrupoTronco.Criado`
- **FP-UC01-009:** Sistema confirma sucesso e redireciona para visualização do grupo

### Fluxos Alternativos
- **FA-UC01-001:** Salvar e adicionar troncos imediatamente (modal "Adicionar Troncos")
- **FA-UC01-002:** Cancelar criação (descarta formulário sem persistir)

### Fluxos de Exceção
- **FE-UC01-001:** Campo obrigatório ausente → HTTP 400 com mensagem específica
- **FE-UC01-002:** Nome duplicado no mesmo tenant → HTTP 409 Conflict "Já existe grupo com este nome"
- **FE-UC01-003:** Intervalo de health check < 10s → HTTP 400 "Intervalo mínimo: 10 segundos" (RN-RF046-004)
- **FE-UC01-004:** Algoritmo LCR sem custo configurado → HTTP 400 "LCR requer custo por minuto em todos os troncos" (RN-RF046-006)
- **FE-UC01-005:** Erro inesperado → HTTP 500 com mensagem genérica (não vazar detalhes internos)

### Regras de Negócio
- **RN-UC01-001:** Campos obrigatórios: Nome, Tipo (GEOGRAFICO, OPERADORA, TECNOLOGIA, CUSTO, QUALIDADE), Algoritmo Balanceamento (ROUND_ROBIN, LEAST_USED, WEIGHTED, PRIORITY, LCR)
- **RN-UC01-002:** FornecedorId preenchido automaticamente com tenant do usuário autenticado
- **RN-UC01-003:** CreatedBy preenchido automaticamente com ID do usuário autenticado
- **RN-UC01-004:** CreatedAt preenchido automaticamente com timestamp UTC atual
- **RN-UC01-005:** FlExcluido inicializado como FALSE
- **RN-UC01-006:** Intervalo de health check deve ser ≥ 10 segundos (padrão: 30s) — RN-RF046-004

### Critérios de Aceite
- **CA-UC01-001:** Todos os campos obrigatórios DEVEM ser validados antes de persistir
- **CA-UC01-002:** FornecedorId DEVE ser preenchido automaticamente com o tenant do usuário autenticado
- **CA-UC01-003:** CreatedBy DEVE ser preenchido automaticamente com o ID do usuário autenticado
- **CA-UC01-004:** CreatedAt DEVE ser preenchido automaticamente com timestamp UTC atual
- **CA-UC01-005:** Sistema DEVE retornar erro claro se validação falhar (HTTP 400 com mensagens específicas)
- **CA-UC01-006:** Auditoria DEVE ser registrada APÓS sucesso da criação
- **CA-UC01-007:** Evento de domínio `GrupoTronco.Criado` DEVE ser publicado após persistência
- **CA-UC01-008:** Tentativa de criar grupo com nome duplicado no mesmo tenant DEVE retornar HTTP 409

---

## UC02 — Visualizar Grupo de Troncos

### Objetivo
Permitir visualização detalhada de um grupo de troncos com métricas de uso, saúde dos troncos e histórico de failover.

### Pré-condições
- Usuário autenticado
- Permissão `AST.GRUPOS_TRONCOS.LIST`

### Pós-condições
- Dados do grupo exibidos corretamente
- Métricas de saúde e uso atualizadas em tempo real (SignalR)

### Fluxo Principal
- **FP-UC02-001:** Usuário seleciona grupo na listagem ou acessa via URL direta
- **FP-UC02-002:** Sistema valida permissão AST.GRUPOS_TRONCOS.LIST
- **FP-UC02-003:** Sistema valida que registro pertence ao tenant do usuário (FornecedorId)
- **FP-UC02-004:** Sistema carrega dados do grupo e troncos vinculados
- **FP-UC02-005:** Sistema exibe dados estruturados em seções:
  - Informações Básicas (Nome, Tipo, Algoritmo, Capacidade, Status)
  - Lista de Troncos (Nome, Tipo, Prioridade, Peso, Custo/Min, Status Saúde, Concurrent Calls, Ações)
  - Métricas em Tempo Real (Concurrent Calls Total, Bandwidth, MOS médio)
  - Histórico de Failovers (últimos 30 dias)
  - Logs de Health Checks (últimas 24 horas)

### Fluxos Alternativos
- **FA-UC02-001:** Atualizar métricas em tempo real via SignalR (sem reload da página)
- **FA-UC02-002:** Exportar relatório de uso em PDF/Excel

### Fluxos de Exceção
- **FE-UC02-001:** Registro inexistente → HTTP 404 "Grupo de troncos não encontrado"
- **FE-UC02-002:** Registro de outro tenant (FornecedorId diferente) → HTTP 404 (não 403, por segurança)
- **FE-UC02-003:** Registro com FlExcluido=TRUE → HTTP 404 "Grupo de troncos não encontrado"

### Regras de Negócio
- **RN-UC02-001:** Isolamento por tenant (FornecedorId) obrigatório
- **RN-UC02-002:** Informações de auditoria DEVEM ser visíveis (CreatedBy, CreatedAt, LastModifiedBy, LastModifiedAt)
- **RN-UC02-003:** Métricas de saúde atualizadas via SignalR a cada health check (padrão 30s)
- **RN-UC02-004:** Histórico de failovers limitado aos últimos 7 anos (conforme RN-RF046-014)

### Critérios de Aceite
- **CA-UC02-001:** Usuário SÓ pode visualizar grupos do próprio tenant (FornecedorId)
- **CA-UC02-002:** Informações de auditoria DEVEM ser exibidas (CreatedBy, CreatedAt, LastModifiedBy, LastModifiedAt)
- **CA-UC02-003:** Tentativa de acessar registro de outro tenant DEVE retornar HTTP 404
- **CA-UC02-004:** Tentativa de acessar registro inexistente ou soft-deleted DEVE retornar HTTP 404
- **CA-UC02-005:** Dados exibidos DEVEM corresponder exatamente ao estado atual no banco
- **CA-UC02-006:** Métricas de saúde (concurrent calls, MOS, latência) DEVEM ser atualizadas em tempo real via SignalR

---

## UC03 — Editar Grupo de Troncos

### Objetivo
Permitir alteração controlada de configurações do grupo de troncos (nome, algoritmo, capacidade, prioridades).

### Pré-condições
- Usuário autenticado
- Permissão `AST.GRUPOS_TRONCOS.UPDATE`
- Grupo pertence ao tenant do usuário (FornecedorId)

### Pós-condições
- Registro atualizado no banco de dados
- Auditoria registrada (LastModifiedBy, LastModifiedAt)
- Evento de domínio publicado: `GrupoTronco.Atualizado`
- Se houver mudança de algoritmo, roteamento é reconfigurado automaticamente

### Fluxo Principal
- **FP-UC03-001:** Usuário clica em "Editar" no grupo
- **FP-UC03-002:** Sistema valida permissão AST.GRUPOS_TRONCOS.UPDATE
- **FP-UC03-003:** Sistema valida que registro pertence ao tenant (FornecedorId)
- **FP-UC03-004:** Sistema carrega dados atuais do grupo
- **FP-UC03-005:** Usuário altera dados (nome, tipo, algoritmo, capacidade, intervalo health check)
- **FP-UC03-006:** Sistema valida alterações conforme RN-RF046-001 a RN-RF046-015
- **FP-UC03-007:** Sistema persiste alterações
- **FP-UC03-008:** Sistema atualiza auditoria (LastModifiedBy, LastModifiedAt)
- **FP-UC03-009:** Sistema publica evento `GrupoTronco.Atualizado`
- **FP-UC03-010:** Se mudança de algoritmo → Sistema recalcula roteamento imediatamente
- **FP-UC03-011:** Sistema confirma sucesso

### Fluxos Alternativos
- **FA-UC03-001:** Cancelar edição (descarta alterações sem persistir)
- **FA-UC03-002:** Forçar atualização mesmo com chamadas ativas (forceUpdate=true) — RN-RF046-013

### Fluxos de Exceção
- **FE-UC03-001:** Campo obrigatório ausente → HTTP 400 com mensagem específica
- **FE-UC03-002:** Nome duplicado no mesmo tenant → HTTP 409 Conflict
- **FE-UC03-003:** Alteração de algoritmo ou remoção de tronco com chamadas ativas → HTTP 409 "Grupo possui chamadas ativas. Use forceUpdate=true para continuar" (RN-RF046-013)
- **FE-UC03-004:** Soma de pesos ≠ 100% (algoritmo WEIGHTED) → HTTP 400 "Soma de pesos deve ser exatamente 100%" (RN-RF046-003)
- **FE-UC03-005:** Registro de outro tenant → HTTP 404

### Regras de Negócio
- **RN-UC03-001:** LastModifiedBy preenchido automaticamente com ID do usuário autenticado
- **RN-UC03-002:** LastModifiedAt preenchido automaticamente com timestamp UTC atual
- **RN-UC03-003:** Mudança de algoritmo recalcula roteamento imediatamente (reconfigura PABX via API)
- **RN-UC03-004:** Alteração com chamadas ativas bloqueada, exceto se forceUpdate=true (RN-RF046-013)
- **RN-UC03-005:** Se algoritmo WEIGHTED, soma de pesos de troncos ativos DEVE ser exatamente 100% (RN-RF046-003)

### Critérios de Aceite
- **CA-UC03-001:** LastModifiedBy DEVE ser preenchido automaticamente com ID do usuário
- **CA-UC03-002:** LastModifiedAt DEVE ser preenchido automaticamente com timestamp UTC
- **CA-UC03-003:** Mudança de algoritmo DEVE recalcular roteamento imediatamente
- **CA-UC03-004:** Tentativa de alterar grupo com chamadas ativas SEM forceUpdate DEVE retornar HTTP 409
- **CA-UC03-005:** Auditoria DEVE ser registrada APÓS sucesso da atualização
- **CA-UC03-006:** Evento de domínio `GrupoTronco.Atualizado` DEVE ser publicado após persistência

---

## UC04 — Inativar Grupo de Troncos

### Objetivo
Permitir inativação (soft delete) de um grupo de troncos que não está mais em uso.

### Pré-condições
- Usuário autenticado
- Permissão `AST.GRUPOS_TRONCOS.DELETE`
- Grupo pertence ao tenant do usuário (FornecedorId)
- Grupo NÃO possui chamadas ativas (concurrent calls = 0)

### Pós-condições
- Registro marcado como excluído (FlExcluido = TRUE)
- Auditoria registrada (DeletedBy, DeletedAt)
- Troncos vinculados são desvinculados automaticamente
- Evento de domínio publicado: `GrupoTronco.Inativado`

### Fluxo Principal
- **FP-UC04-001:** Usuário clica em "Inativar" no grupo
- **FP-UC04-002:** Sistema exibe confirmação: "Deseja realmente inativar este grupo? Todas as chamadas ativas serão encerradas."
- **FP-UC04-003:** Usuário confirma ação
- **FP-UC04-004:** Sistema valida permissão AST.GRUPOS_TRONCOS.DELETE
- **FP-UC04-005:** Sistema valida que registro pertence ao tenant (FornecedorId)
- **FP-UC04-006:** Sistema valida que NÃO há chamadas ativas (concurrent calls = 0)
- **FP-UC04-007:** Sistema marca FlExcluido = TRUE (soft delete, nunca DELETE físico)
- **FP-UC04-008:** Sistema desvincula todos os troncos do grupo
- **FP-UC04-009:** Sistema registra auditoria (DeletedBy, DeletedAt)
- **FP-UC04-010:** Sistema publica evento `GrupoTronco.Inativado`
- **FP-UC04-011:** Sistema confirma sucesso

### Fluxos Alternativos
- **FA-UC04-001:** Cancelar inativação (retorna sem alterar registro)

### Fluxos de Exceção
- **FE-UC04-001:** Grupo possui chamadas ativas → HTTP 409 "Não é possível inativar grupo com chamadas ativas"
- **FE-UC04-002:** Registro de outro tenant → HTTP 404
- **FE-UC04-003:** Registro já inativado (FlExcluido=TRUE) → HTTP 404

### Regras de Negócio
- **RN-UC04-001:** Soft delete obrigatório (FlExcluido = TRUE, nunca DELETE físico)
- **RN-UC04-002:** DeletedBy preenchido automaticamente com ID do usuário autenticado
- **RN-UC04-003:** DeletedAt preenchido automaticamente com timestamp UTC atual
- **RN-UC04-004:** Inativação só permitida se concurrent calls = 0
- **RN-UC04-005:** Troncos vinculados são desvinculados automaticamente
- **RN-UC04-006:** Histórico de logs mantido por 7 anos mesmo após inativação (RN-RF046-014)

### Critérios de Aceite
- **CA-UC04-001:** Sistema DEVE usar soft delete (FlExcluido=TRUE), NUNCA DELETE físico
- **CA-UC04-002:** DeletedBy DEVE ser preenchido automaticamente com ID do usuário
- **CA-UC04-003:** DeletedAt DEVE ser preenchido automaticamente com timestamp UTC
- **CA-UC04-004:** Tentativa de inativar grupo com chamadas ativas DEVE retornar HTTP 409
- **CA-UC04-005:** Auditoria DEVE ser registrada APÓS sucesso da inativação
- **CA-UC04-006:** Evento de domínio `GrupoTronco.Inativado` DEVE ser publicado após persistência
- **CA-UC04-007:** Registros inativos NÃO devem aparecer nas listagens padrão (UC00)

---

## 6. MATRIZ DE RASTREABILIDADE

### Cobertura RF → UC

| Item RF | UC00 | UC01 | UC02 | UC03 | UC04 |
|---------|------|------|------|------|------|
| RF046-CRUD-01 | | ✅ | | | |
| RF046-CRUD-02 | ✅ | | | | |
| RF046-CRUD-03 | | | ✅ | | |
| RF046-CRUD-04 | | | | ✅ | |
| RF046-CRUD-05 | | | | | ✅ |
| RF046-VAL-01 | | ✅ | | ✅ | ✅ |
| RF046-VAL-02 | | ✅ | | ✅ | |
| RF046-VAL-03 | | ✅ | | ✅ | |
| RF046-VAL-04 | | ✅ | | ✅ | |
| RF046-VAL-05 | | ✅ | | ✅ | |
| RF046-SEC-01 | ✅ | ✅ | ✅ | ✅ | ✅ |
| RF046-SEC-02 | ✅ | ✅ | ✅ | ✅ | ✅ |
| RF046-SEC-03 | | | ✅ | | |
| RF046-SEC-04 | | | ✅ | ✅ | ✅ |
| RF046-RN-01 | | | ✅ | | |
| RF046-RN-02 | | | ✅ | | |
| RF046-RN-03 | ✅ | | ✅ | | |
| RF046-RN-04 | | | ✅ | | |
| RF046-RN-05 | | | ✅ | | |
| RN-RF046-001 | | ✅ | | ✅ | ✅ |
| RN-RF046-002 | | ✅ | | ✅ | |
| RN-RF046-003 | | ✅ | | ✅ | |
| RN-RF046-004 | | ✅ | | ✅ | |
| RN-RF046-005 | | ✅ | | ✅ | |
| RN-RF046-006 | | ✅ | | ✅ | |
| RN-RF046-007 | | | ✅ | | |
| RN-RF046-008 | | | ✅ | | |
| RN-RF046-009 | | | ✅ | | |
| RN-RF046-010 | | | ✅ | | |
| RN-RF046-011 | | ✅ | | ✅ | |
| RN-RF046-012 | | | ✅ | | |
| RN-RF046-013 | | | | ✅ | ✅ |
| RN-RF046-014 | | | ✅ | | ✅ |
| RN-RF046-015 | ✅ | ✅ | ✅ | ✅ | ✅ |

### Cobertura de Permissões

| Permissão | UC00 | UC01 | UC02 | UC03 | UC04 |
|-----------|------|------|------|------|------|
| AST.GRUPOS_TRONCOS.LIST | ✅ | | ✅ | | |
| AST.GRUPOS_TRONCOS.CREATE | | ✅ | | | |
| AST.GRUPOS_TRONCOS.UPDATE | | | | ✅ | |
| AST.GRUPOS_TRONCOS.DELETE | | | | | ✅ |
| AST.GRUPOS_TRONCOS.CONFIGURE_ROUTING | | | | ✅ | |
| AST.GRUPOS_TRONCOS.MONITOR | | | ✅ | | |

---

## 7. INTEGRAÇÕES OBRIGATÓRIAS

- **Autenticação:** JWT Bearer Token
- **Multi-Tenancy:** FornecedorId em todas as tabelas (GrupoTronco, Tronco, TroncoHealthCheck, TroncoFailoverLog, TroncoUso)
- **Auditoria:** CreatedBy, CreatedAt, LastModifiedBy, LastModifiedAt, DeletedBy, DeletedAt
- **Internacionalização:** Chaves i18n com prefixo `grupos_troncos.*` (pt-BR, en-US, es-ES)
- **Central de Funcionalidades:** Feature `AST.GRUPOS_TRONCOS` registrada
- **SignalR:** Atualização em tempo real de métricas (concurrent calls, status saúde, MOS)
- **PABX/SIP Providers:** Integração via API REST + Webhooks para reconfiguração de roteamento
- **Serviço de Notificação:** E-mail + SMS para alertas de failover e capacidade

---

## 8. HISTÓRICO DE VERSÕES

| Versão | Data | Descrição | Autor |
|--------|------|-----------|-------|
| 2.0 | 2025-12-31 | Migração para template v2.0 com 5 UCs canônicos. Cobertura 100% do RF046. | Agência ALC - alc.dev.br |
| 1.0 | 2025-12-18 | Versão inicial com 9 UCs | - |
