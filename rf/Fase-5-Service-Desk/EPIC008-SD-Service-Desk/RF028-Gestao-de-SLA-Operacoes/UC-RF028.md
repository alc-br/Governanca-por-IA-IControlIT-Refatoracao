# UC-RF028 — Casos de Uso Canônicos

**RF:** RF028 — Gestão de SLA - Operações
**Versão:** 2.0
**Data:** 2025-12-31
**Autor:** Agência ALC - alc.dev.br
**Epic:** EPIC008-SD-Service-Desk
**Fase:** Fase-5-Service-Desk

---

## 1. OBJETIVO DO DOCUMENTO

Este documento descreve **todos os Casos de Uso (UC)** derivados do **RF028**, cobrindo integralmente o comportamento funcional esperado para Gestão de SLA - Operações.

Os UCs aqui definidos servem como **contrato comportamental**, sendo a **fonte primária** para geração de:
- Casos de Teste (TC-RF028.yaml)
- Massas de Teste (MT-RF028.yaml)
- Evidências de auditoria e validação funcional
- Execução por agentes de IA (tester, QA, E2E)

**Cobertura**: Este documento cobre 100% das 12 regras de negócio do RF028 (RN-SLA-028-01 até RN-SLA-028-12).

---

## 2. SUMÁRIO DE CASOS DE USO

| ID | Nome | Ator Principal | RNs Cobertas |
|----|------|----------------|--------------|
| UC00 | Listar SLAs Operações | Usuário Autenticado | RN-SLA-028-10, RN-SLA-028-11 |
| UC01 | Criar SLA Operação | Usuário Autenticado | RN-SLA-028-01, RN-SLA-028-06, RN-SLA-028-07, RN-SLA-028-08, RN-SLA-028-09, RN-SLA-028-10 |
| UC02 | Visualizar SLA Operação | Usuário Autenticado | RN-SLA-028-10 |
| UC03 | Editar SLA Operação | Usuário Autenticado | RN-SLA-028-01, RN-SLA-028-10 |
| UC04 | Excluir SLA Operação | Usuário Autenticado | RN-SLA-028-10, RN-SLA-028-11 |
| UC05 | Calcular SLA de Operação | Sistema + Usuário | RN-SLA-028-02, RN-SLA-028-12 |
| UC06 | Pausar SLA Manualmente | Usuário Autenticado | RN-SLA-028-03 |
| UC07 | Retomar SLA Pausado | Usuário Autenticado | RN-SLA-028-03 |
| UC08 | Visualizar Dashboard Compliance | Usuário Autenticado | RN-SLA-028-04, RN-SLA-028-05 |

---

## 3. PADRÕES GERAIS APLICÁVEIS A TODOS OS UCs

- Todos os acessos respeitam **isolamento por tenant (ClienteId)**
- Todas as ações exigem **permissão explícita**
- Erros não devem vazar informações sensíveis
- Auditoria deve registrar **quem**, **quando** e **qual ação**
- Mensagens devem ser claras, previsíveis e rastreáveis
- Soft delete obrigatório (IsDeleted flag)
- Integração com BrasilAPI para feriados nacionais

---

## UC00 — Listar SLAs Operações

### Objetivo
Permitir que o usuário visualize registros de SLAs para operações disponíveis do seu próprio tenant, com filtros avançados e paginação.

### Pré-condições
- Usuário autenticado
- Permissão `sla:operacoes:read`
- Multi-tenancy: Usuário vinculado a ClienteId válido

### Pós-condições
- Lista exibida conforme filtros e paginação
- SLAs deletados (IsDeleted = true) não aparecem na listagem padrão

### Fluxo Principal
- **FP-UC00-001:** Usuário acessa menu "SLA" → "SLA Operações"
- **FP-UC00-002:** Sistema valida permissão `sla:operacoes:read`
- **FP-UC00-003:** Sistema carrega registros do tenant (WHERE ClienteId = [usuário])
- **FP-UC00-004:** Sistema filtra SLAs ativos (WHERE IsDeleted = false)
- **FP-UC00-005:** Sistema aplica paginação (padrão: 20 registros/página) e ordenação
- **FP-UC00-006:** Sistema exibe colunas: Nome SLA, Tipo Operação, Calendário, Prioridade, Status, Compliance %, Ações

### Fluxos Alternativos
- **FA-UC00-001:** Buscar por nome/descrição de SLA
- **FA-UC00-002:** Ordenar por coluna (nome, prioridade, compliance, data criação)
- **FA-UC00-003:** Filtrar por status (Ativo/Inativo)
- **FA-UC00-004:** Filtrar por prioridade (P1, P2, P3, P4)
- **FA-UC00-005:** Filtrar por tipo de operação (Instalação, Movimentação, Configuração, Manutenção)
- **FA-UC00-006:** Exportar lista para Excel (permissão `sla:operacoes:export`)

### Fluxos de Exceção
- **FE-UC00-001:** Usuário sem permissão → HTTP 403 Forbidden
- **FE-UC00-002:** Nenhum registro encontrado → estado vazio "Nenhum SLA cadastrado. Crie seu primeiro SLA."
- **FE-UC00-003:** Tentativa de acesso a SLA de outro tenant → HTTP 403 Forbidden

### Regras de Negócio
- **RN-SLA-028-10:** Todas as queries incluem WHERE ClienteId = [ClienteId do usuário autenticado]
- **RN-SLA-028-11:** Queries padrão filtram WHERE IsDeleted = false (soft delete)

### Critérios de Aceite
- **CA-UC00-001:** A lista DEVE exibir apenas registros do tenant do usuário autenticado
- **CA-UC00-002:** Registros excluídos (IsDeleted = true) NÃO devem aparecer na listagem padrão
- **CA-UC00-003:** Paginação DEVE ser aplicada com limite padrão de 20 registros
- **CA-UC00-004:** Sistema DEVE permitir ordenação por qualquer coluna visível
- **CA-UC00-005:** Filtros DEVEM ser acumuláveis e refletir na URL
- **CA-UC00-006:** Tentativa de acesso cruzado de tenant DEVE retornar HTTP 403

---

## UC01 — Criar SLA Operação

### Objetivo
Permitir a criação de um novo SLA para operações com validação completa de hierarquia de tempos e metas por prioridade.

### Pré-condições
- Usuário autenticado
- Permissão `sla:operacoes:create`
- Calendário de atendimento já cadastrado

### Pós-condições
- SLA persistido no banco com ClienteId automático
- Auditoria registrada (código: SLA_OP_CREATE)
- Motor de cálculo iniciado (Hangfire job)

### Fluxo Principal
- **FP-UC01-001:** Usuário clica em "Novo SLA Operação"
- **FP-UC01-002:** Sistema valida permissão `sla:operacoes:create`
- **FP-UC01-003:** Sistema exibe formulário com campos obrigatórios
- **FP-UC01-004:** Usuário informa dados básicos (nome, descrição, calendário)
- **FP-UC01-005:** Usuário define metas por prioridade (P1, P2, P3, P4)
- **FP-UC01-006:** Sistema valida hierarquia de tempos (RN-SLA-028-01)
- **FP-UC01-007:** Sistema valida metas específicas por prioridade (RN-SLA-028-06 a RN-SLA-028-09)
- **FP-UC01-008:** Sistema preenche ClienteId automaticamente
- **FP-UC01-009:** Sistema cria registro com IsDeleted = false
- **FP-UC01-010:** Sistema registra auditoria completa
- **FP-UC01-011:** Sistema inicia motor de cálculo (Hangfire)
- **FP-UC01-012:** Sistema confirma sucesso com mensagem

### Campos do Formulário

**Seção 1: Informações Básicas**

| Campo | Tipo | Obrigatório | Validação |
|-------|------|-------------|-----------|
| Nome SLA | Text | Sim | Max 200 caracteres, único por tenant |
| Descrição | Textarea | Sim | Min 50, max 1000 caracteres |
| Calendário Atendimento | Select | Sim | FK para Calendario (24x7, Comercial, Dias Úteis) |
| Data Início Vigência | Date | Sim | >= Hoje |
| Data Fim Vigência | Date | Não | Se preenchido, > Data Início |
| Status Inicial | Select | Sim | Ativo/Inativo (padrão: Ativo) |

**Seção 2: Metas por Prioridade**

Para cada prioridade (P1, P2, P3, P4), definir:

| Campo | Tipo | Validação |
|-------|------|-----------|
| Tempo Resposta | TimeSpan (horas) | > 0, resposta < resolução |
| Tempo Resolução | TimeSpan (horas) | > Tempo Resposta, resolução < atendimento |
| Tempo Atendimento | TimeSpan (horas) | > Tempo Resolução |

**Metas Padrão Sugeridas:**
- **P1 (Crítico):** Resposta=2h, Resolução=4h, Atendimento=8h (RN-SLA-028-06)
- **P2 (Alto):** Resposta=4h, Resolução=8h, Atendimento=24h (RN-SLA-028-07)
- **P3 (Médio):** Resposta=8h, Resolução=24h, Atendimento=48h (RN-SLA-028-08)
- **P4 (Baixo):** Resposta=24h, Resolução=72h, Atendimento=120h (5 dias) (RN-SLA-028-09)

### Fluxos Alternativos
- **FA-UC01-001:** Usar template pré-configurado (carrega metas padrão)
- **FA-UC01-002:** Salvar como rascunho (IsAtivo = false, sem iniciar motor cálculo)
- **FA-UC01-003:** Cancelar criação (retorna à listagem)

### Fluxos de Exceção
- **FE-UC01-001:** Erro de validação hierarquia tempos → HTTP 400 com mensagem "Tempo resposta deve ser menor que resolução, que deve ser menor que atendimento"
- **FE-UC01-002:** Meta P1 fora dos limites → HTTP 400 "Prioridade P1 deve ter resposta ≤ 2h, resolução ≤ 4h, atendimento ≤ 8h"
- **FE-UC01-003:** Meta P2 fora dos limites → HTTP 400 "Prioridade P2 deve ter resposta ≤ 4h, resolução ≤ 8h, atendimento ≤ 24h"
- **FE-UC01-004:** Meta P3 fora dos limites → HTTP 400 "Prioridade P3 deve ter resposta ≤ 8h, resolução ≤ 24h, atendimento ≤ 48h"
- **FE-UC01-005:** Meta P4 fora dos limites → HTTP 400 "Prioridade P4 deve ter resposta ≤ 24h, resolução ≤ 72h, atendimento ≤ 5 dias"
- **FE-UC01-006:** SLA duplicado (mesmo nome no tenant) → HTTP 400 "Já existe SLA com este nome"
- **FE-UC01-007:** Erro inesperado → HTTP 500 com log detalhado

### Regras de Negócio
- **RN-SLA-028-01:** Tempo resposta < resolução < atendimento (validação obrigatória)
- **RN-SLA-028-06:** P1 = 2h resposta, 4h resolução, 8h atendimento
- **RN-SLA-028-07:** P2 = 4h resposta, 8h resolução, 24h atendimento
- **RN-SLA-028-08:** P3 = 8h resposta, 24h resolução, 48h atendimento
- **RN-SLA-028-09:** P4 = 24h resposta, 72h resolução, 5 dias atendimento
- **RN-SLA-028-10:** ClienteId preenchido automaticamente com tenant do usuário

### Critérios de Aceite
- **CA-UC01-001:** Todos os campos obrigatórios DEVEM ser validados antes de persistir
- **CA-UC01-002:** Sistema DEVE validar hierarquia (resposta < resolução < atendimento) para TODAS as prioridades
- **CA-UC01-003:** Sistema DEVE rejeitar metas P1 que violem RN-SLA-028-06
- **CA-UC01-004:** Sistema DEVE rejeitar metas P2 que violem RN-SLA-028-07
- **CA-UC01-005:** Sistema DEVE rejeitar metas P3 que violem RN-SLA-028-08
- **CA-UC01-006:** Sistema DEVE rejeitar metas P4 que violem RN-SLA-028-09
- **CA-UC01-007:** ClienteId DEVE ser preenchido automaticamente
- **CA-UC01-008:** IsDeleted DEVE ser criado como false
- **CA-UC01-009:** Auditoria DEVE ser registrada APÓS sucesso da criação
- **CA-UC01-010:** Motor de cálculo DEVE ser iniciado imediatamente

---

## UC02 — Visualizar SLA Operação

### Objetivo
Permitir visualização detalhada de um SLA de operação incluindo configuração, métricas atuais e histórico.

### Pré-condições
- Usuário autenticado
- Permissão `sla:operacoes:read`
- SLA existe no tenant do usuário

### Pós-condições
- Dados exibidos corretamente com isolamento de tenant

### Fluxo Principal
- **FP-UC02-001:** Usuário clica em SLA na listagem
- **FP-UC02-002:** Sistema valida permissão `sla:operacoes:read`
- **FP-UC02-003:** Sistema valida tenant (WHERE ClienteId = [usuário])
- **FP-UC02-004:** Sistema carrega dados completos do SLA
- **FP-UC02-005:** Sistema exibe tela com abas: Resumo, Métricas, Violações, Histórico

### Informações Exibidas

**Aba Resumo:**
- Nome SLA, Descrição
- Calendário Atendimento (nome + horários)
- Status (Ativo/Inativo)
- Vigência (Data Início - Data Fim)
- Metas por Prioridade (P1 a P4)
- Dados Auditoria (criado por, criado em, modificado por, modificado em)

**Aba Métricas:**
- % Compliance Atual (últimos 30 dias)
- Gráfico de linha: Evolução compliance
- Estatísticas: Média, Mínimo, Máximo tempo resposta/resolução/atendimento

**Aba Violações:**
- Grid com violações ocorridas
- Colunas: Data/Hora, Operação, Prioridade, Tempo Meta, Tempo Real, Desvio, Status

**Aba Histórico:**
- Timeline de eventos: Criação, Modificações, Pausas, Violações
- Versionamento completo (se aplicável)

### Fluxos Alternativos
- **FA-UC02-001:** Editar SLA (se permissão `sla:operacoes:update`)
- **FA-UC02-002:** Excluir SLA (se permissão `sla:operacoes:delete`)
- **FA-UC02-003:** Exportar métricas para Excel

### Fluxos de Exceção
- **FE-UC02-001:** SLA não encontrado → HTTP 404
- **FE-UC02-002:** SLA de outro tenant → HTTP 403 Forbidden
- **FE-UC02-003:** SLA deletado (IsDeleted = true) → HTTP 404

### Regras de Negócio
- **RN-SLA-028-10:** Usuário SÓ pode visualizar SLAs do próprio tenant

### Critérios de Aceite
- **CA-UC02-001:** Usuário SÓ pode visualizar registros do próprio tenant
- **CA-UC02-002:** Informações de auditoria DEVEM ser exibidas
- **CA-UC02-003:** Tentativa de acessar SLA de outro tenant DEVE retornar 403
- **CA-UC02-004:** Tentativa de acessar SLA deletado DEVE retornar 404
- **CA-UC02-005:** Dados exibidos DEVEM corresponder exatamente ao estado atual no banco

---

## UC03 — Editar SLA Operação

### Objetivo
Permitir alteração controlada de um SLA de operação com validação de hierarquia de tempos.

### Pré-condições
- Usuário autenticado
- Permissão `sla:operacoes:update`
- SLA existe e pertence ao tenant do usuário

### Pós-condições
- SLA atualizado
- Auditoria registrada (código: SLA_OP_UPDATE)
- Nova versão criada (versionamento)

### Fluxo Principal
- **FP-UC03-001:** Usuário clica em "Editar" no SLA
- **FP-UC03-002:** Sistema valida permissão `sla:operacoes:update`
- **FP-UC03-003:** Sistema valida tenant
- **FP-UC03-004:** Sistema carrega formulário com dados preenchidos
- **FP-UC03-005:** Usuário altera campos desejados
- **FP-UC03-006:** Sistema valida hierarquia de tempos (RN-SLA-028-01)
- **FP-UC03-007:** Sistema persiste alterações
- **FP-UC03-008:** Sistema cria nova versão (versionamento)
- **FP-UC03-009:** Sistema registra auditoria completa (before/after)
- **FP-UC03-010:** Sistema confirma sucesso

### Fluxos Alternativos
- **FA-UC03-001:** Cancelar edição (descarta alterações)
- **FA-UC03-002:** Visualizar histórico de versões

### Fluxos de Exceção
- **FE-UC03-001:** Erro de validação hierarquia → HTTP 400
- **FE-UC03-002:** SLA de outro tenant → HTTP 403
- **FE-UC03-003:** SLA em uso por operações ativas → Alerta "SLA em uso. Alterações entram em vigor após término das operações ativas."
- **FE-UC03-004:** Conflito de edição concorrente → HTTP 409

### Regras de Negócio
- **RN-SLA-028-01:** Validar hierarquia tempos em TODAS as alterações
- **RN-SLA-028-10:** Apenas SLAs do próprio tenant podem ser editados

### Critérios de Aceite
- **CA-UC03-001:** Sistema DEVE validar hierarquia de tempos antes de persistir
- **CA-UC03-002:** Sistema DEVE criar nova versão do SLA (versionamento)
- **CA-UC03-003:** Tentativa de editar SLA de outro tenant DEVE retornar 403
- **CA-UC03-004:** Auditoria DEVE registrar estado anterior e novo estado
- **CA-UC03-005:** Sistema DEVE detectar conflitos de edição concorrente

---

## UC04 — Excluir SLA Operação

### Objetivo
Permitir exclusão lógica de SLA de operação (soft delete).

### Pré-condições
- Usuário autenticado
- Permissão `sla:operacoes:delete`
- SLA existe e pertence ao tenant do usuário
- SLA não possui operações ativas

### Pós-condições
- SLA marcado como excluído (IsDeleted = true)
- Auditoria registrada (código: SLA_OP_DELETE)
- Motor de cálculo cancelado (Hangfire jobs)

### Fluxo Principal
- **FP-UC04-001:** Usuário clica em "Excluir" no SLA
- **FP-UC04-002:** Sistema confirma ação: "Deseja realmente excluir este SLA? Cálculos serão interrompidos."
- **FP-UC04-003:** Usuário confirma exclusão
- **FP-UC04-004:** Sistema valida permissão `sla:operacoes:delete`
- **FP-UC04-005:** Sistema valida tenant
- **FP-UC04-006:** Sistema verifica dependências (operações ativas)
- **FP-UC04-007:** Sistema marca IsDeleted = true, preenche DataDelecao, UsuarioDeletouId
- **FP-UC04-008:** Sistema cancela Hangfire jobs de cálculo
- **FP-UC04-009:** Sistema registra auditoria completa
- **FP-UC04-010:** Sistema confirma sucesso

### Fluxos Alternativos
- **FA-UC04-001:** Cancelar exclusão (fecha diálogo, mantém SLA ativo)

### Fluxos de Exceção
- **FE-UC04-001:** SLA com operações ativas → HTTP 400 "Não é possível excluir SLA com operações ativas. Aguarde conclusão das operações."
- **FE-UC04-002:** SLA já excluído → HTTP 400 "SLA já foi excluído"
- **FE-UC04-003:** SLA de outro tenant → HTTP 403

### Regras de Negócio
- **RN-SLA-028-10:** Apenas SLAs do próprio tenant podem ser excluídos
- **RN-SLA-028-11:** Exclusão sempre lógica (IsDeleted = true), nunca física

### Critérios de Aceite
- **CA-UC04-001:** Exclusão DEVE ser sempre lógica (soft delete) via IsDeleted
- **CA-UC04-002:** Sistema DEVE verificar dependências ANTES de permitir exclusão
- **CA-UC04-003:** Sistema DEVE exigir confirmação explícita do usuário
- **CA-UC04-004:** IsDeleted, DataDelecao, UsuarioDeletouId DEVEM ser preenchidos
- **CA-UC04-005:** Tentativa de excluir SLA com operações ativas DEVE retornar erro claro
- **CA-UC04-006:** SLA excluído NÃO deve aparecer em listagens padrão (UC00)
- **CA-UC04-007:** Histórico DEVE ser preservado por 7 anos (LGPD)

---

## UC05 — Calcular SLA de Operação

### Objetivo
Calcular automaticamente tempo consumido de SLA excluindo pausas, feriados e fins de semana conforme calendário.

### Pré-condições
- Operação (Ordem de Serviço) existente
- SLA configurado para a prioridade da operação
- Calendário de atendimento definido

### Pós-condições
- Percentual de SLA consumido calculado
- Alertas gerados se necessário (50%, 75%, 90%, 100%)

### Fluxo Principal
- **FP-UC05-001:** Sistema executa job de cálculo (Hangfire, a cada 15 minutos)
- **FP-UC05-002:** Sistema identifica operações ativas
- **FP-UC05-003:** Sistema obtém SLA correspondente (por prioridade)
- **FP-UC05-004:** Sistema calcula tempo total decorrido (DataAtual - DataAbertura)
- **FP-UC05-005:** Sistema identifica pausas ativas (PausaSLA)
- **FP-UC05-006:** Sistema deduz duração de pausas do tempo total
- **FP-UC05-007:** Sistema consulta BrasilAPI para obter feriados do ano
- **FP-UC05-008:** Sistema exclui feriados nacionais do cálculo
- **FP-UC05-009:** Sistema exclui fins de semana (se calendário não for 24x7)
- **FP-UC05-010:** Sistema calcula percentual consumido: (TempoConsumido / TempoMeta) * 100
- **FP-UC05-011:** Sistema registra cálculo em log (código: SLA_OP_CALC)
- **FP-UC05-012:** Sistema retorna resultado (TempoConsumido, TempoDisponível, PercentualConsumido)

### Fluxos Alternativos
- **FA-UC05-001:** Consulta manual via endpoint GET /api/sla-operacoes/{id}/calcular
- **FA-UC05-002:** Feriado estadual (consulta por UF na BrasilAPI)

### Fluxos de Exceção
- **FE-UC05-001:** BrasilAPI indisponível → Usar cache de feriados do ano anterior
- **FE-UC05-002:** Calendário não encontrado → Usar 24x7 como fallback
- **FE-UC05-003:** Pausas inconsistentes (DataFim < DataInicio) → Ignorar pausa e registrar erro

### Regras de Negócio
- **RN-SLA-028-02:** Cálculo deduz duração total de todas as pausas ativas
- **RN-SLA-028-02:** Feriados nacionais não contam no tempo produtivo
- **RN-SLA-028-02:** Fins de semana são excluídos se calendário não for 24x7
- **RN-SLA-028-12:** Consulta BrasilAPI anualmente e cacheia resultados
- **RN-SLA-028-12:** Fallback usa cache em caso de falha da API

### Critérios de Aceite
- **CA-UC05-001:** Cálculo DEVE excluir 100% das pausas ativas
- **CA-UC05-002:** Feriados nacionais NÃO devem contar no tempo produtivo
- **CA-UC05-003:** Fins de semana DEVEM ser excluídos se calendário for "Dias Úteis"
- **CA-UC05-004:** Sistema DEVE consultar BrasilAPI uma vez por ano
- **CA-UC05-005:** Em caso de falha BrasilAPI, sistema DEVE usar cache
- **CA-UC05-006:** Percentual consumido DEVE ser preciso (casa decimal)
- **CA-UC05-007:** Cálculo DEVE ser executado a cada 15 minutos automaticamente

---

## UC06 — Pausar SLA Manualmente

### Objetivo
Permitir pausa manual de SLA para operações que dependem de terceiros ou cliente.

### Pré-condições
- Usuário autenticado
- Permissão `sla:operacoes:pause`
- Operação ativa existe

### Pós-condições
- PausaSLA criada com DataInicio, TipoPausa, Motivo
- Contador de SLA pausado
- Auditoria registrada (código: SLA_OP_PAUSE)

### Fluxo Principal
- **FP-UC06-001:** Usuário clica em "Pausar SLA" na operação
- **FP-UC06-002:** Sistema valida permissão `sla:operacoes:pause`
- **FP-UC06-003:** Sistema exibe modal com campos: Tipo Pausa, Motivo
- **FP-UC06-004:** Usuário seleciona Tipo Pausa (Aguardando Cliente, Aguardando Terceiro, Fora Horário)
- **FP-UC06-005:** Usuário informa Motivo (textarea obrigatória, min 20 caracteres)
- **FP-UC06-006:** Sistema cria PausaSLA com DataInicio = Agora, DataFim = null
- **FP-UC06-007:** Sistema registra auditoria completa
- **FP-UC06-008:** Sistema notifica responsável (opcional)
- **FP-UC06-009:** Sistema confirma sucesso

### Fluxos Alternativos
- **FA-UC06-001:** Cancelar pausa (fecha modal)

### Fluxos de Exceção
- **FE-UC06-001:** SLA já pausado → HTTP 400 "SLA já está pausado. Retome antes de pausar novamente."
- **FE-UC06-002:** Motivo insuficiente → HTTP 400 "Motivo deve ter no mínimo 20 caracteres"

### Regras de Negócio
- **RN-SLA-028-03:** Pausa manual cria PausaSLA com TipoPausa informado
- **RN-SLA-028-03:** Contador de SLA para enquanto pausa estiver ativa

### Critérios de Aceite
- **CA-UC06-001:** PausaSLA DEVE ser criada com DataInicio = timestamp atual
- **CA-UC06-002:** DataFim DEVE ser null (pausa ativa)
- **CA-UC06-003:** TipoPausa DEVE ser obrigatório
- **CA-UC06-004:** Motivo DEVE ter mínimo 20 caracteres
- **CA-UC06-005:** Auditoria DEVE registrar quem pausou, quando e motivo
- **CA-UC06-006:** Sistema DEVE impedir pausar SLA já pausado

---

## UC07 — Retomar SLA Pausado

### Objetivo
Permitir retomada manual de SLA pausado.

### Pré-condições
- Usuário autenticado
- Permissão `sla:operacoes:resume`
- Operação com PausaSLA ativa (DataFim = null)

### Pós-condições
- PausaSLA fechada com DataFim preenchida
- Contador de SLA retomado
- Auditoria registrada (código: SLA_OP_RESUME)

### Fluxo Principal
- **FP-UC07-001:** Usuário clica em "Retomar SLA" na operação pausada
- **FP-UC07-002:** Sistema valida permissão `sla:operacoes:resume`
- **FP-UC07-003:** Sistema identifica PausaSLA ativa (DataFim = null)
- **FP-UC07-004:** Sistema preenche DataFim = Agora
- **FP-UC07-005:** Sistema calcula duração da pausa (DataFim - DataInicio)
- **FP-UC07-006:** Sistema registra auditoria completa
- **FP-UC07-007:** Sistema notifica responsável (opcional)
- **FP-UC07-008:** Sistema confirma sucesso

### Fluxos Alternativos
- Nenhum

### Fluxos de Exceção
- **FE-UC07-001:** SLA não pausado → HTTP 400 "SLA não está pausado"
- **FE-UC07-002:** Múltiplas pausas ativas → Fecha apenas a mais recente

### Regras de Negócio
- **RN-SLA-028-03:** Retomada fecha PausaSLA com DataFim
- **RN-SLA-028-03:** Contador de SLA retoma automaticamente

### Critérios de Aceite
- **CA-UC07-001:** PausaSLA DEVE ser fechada com DataFim = timestamp atual
- **CA-UC07-002:** Duração DEVE ser calculada (DataFim - DataInicio)
- **CA-UC07-003:** Auditoria DEVE registrar quem retomou e quando
- **CA-UC07-004:** Sistema DEVE impedir retomar SLA não pausado
- **CA-UC07-005:** Cálculo de SLA DEVE excluir duração da pausa após retomada

---

## UC08 — Visualizar Dashboard Compliance

### Objetivo
Exibir dashboard em tempo real com alertas de SLA (50%, 75%, 90%, 100%) e compliance geral.

### Pré-condições
- Usuário autenticado
- Permissão `sla:operacoes:metrics`
- SLAs ativos existem no sistema

### Pós-condições
- Dashboard carregado com dados em tempo real (SignalR)

### Fluxo Principal
- **FP-UC08-001:** Usuário acessa "Dashboard SLA Operações"
- **FP-UC08-002:** Sistema valida permissão `sla:operacoes:metrics`
- **FP-UC08-003:** Sistema carrega dados via SignalR (tempo real)
- **FP-UC08-004:** Sistema exibe cards principais:
  - Total SLAs Ativos
  - % Compliance Geral
  - Operações em Risco (75%+)
  - Violações Ativas (100%+)
- **FP-UC08-005:** Sistema exibe gráficos:
  - Linha: Evolução compliance últimos 30 dias
  - Pizza: Distribuição alertas (50%, 75%, 90%, 100%)
  - Barra: Top 5 operações em risco
- **FP-UC08-006:** Sistema exibe lista de alertas ativos com severidade
- **FP-UC08-007:** Sistema atualiza dashboard automaticamente a cada 30 segundos

### Alertas Exibidos (RN-SLA-028-04)

| Threshold | Severidade | Cor | Ação |
|-----------|-----------|-----|------|
| 50% | Informativo | Azul | Nenhuma |
| 75% | Aviso | Amarelo | Notificação + possível escalação |
| 90% | Crítico | Laranja | Escalação automática |
| 100% | Violação | Vermelho | Escalação obrigatória + penalidade |

### Fluxos Alternativos
- **FA-UC08-001:** Drill-down em operação específica (redireciona para detalhes)
- **FA-UC08-002:** Filtrar por prioridade (P1, P2, P3, P4)
- **FA-UC08-003:** Filtrar por período (hoje, semana, mês)
- **FA-UC08-004:** Exportar dashboard para PDF

### Fluxos de Exceção
- **FE-UC08-001:** Nenhum SLA ativo → Exibe "Nenhum SLA ativo. Crie seu primeiro SLA."
- **FE-UC08-002:** SignalR desconectado → Exibe banner "Conexão perdida. Reconectando..." e tenta reconectar

### Regras de Negócio
- **RN-SLA-028-04:** Alertas gerados em 50%, 75%, 90%, 100% de consumo
- **RN-SLA-028-04:** Severidade: 50%=Informativo, 75%=Aviso, 90%=Crítico, 100%=Violação
- **RN-SLA-028-04:** Notificação por e-mail + SignalR em tempo real
- **RN-SLA-028-05:** Escalação automática disparada em 90%+
- **RN-SLA-028-05:** Escalação para Level 2 (90%), Level 3 (100%), Manager (violação confirmada)

### Critérios de Aceite
- **CA-UC08-001:** Dashboard DEVE atualizar em tempo real via SignalR
- **CA-UC08-002:** Alertas DEVEM ser exibidos conforme severidade (RN-SLA-028-04)
- **CA-UC08-003:** Sistema DEVE disparar escalação automática em 90%+ (RN-SLA-028-05)
- **CA-UC08-004:** Sistema DEVE exibir apenas dados do tenant do usuário
- **CA-UC08-005:** Gráficos DEVEM refletir dados atualizados automaticamente
- **CA-UC08-006:** Sistema DEVE exibir notificação toast quando nova violação ocorrer

---

## 4. MATRIZ DE RASTREABILIDADE

| UC | Regras de Negócio Cobertas |
|----|---------------------------|
| UC00 | RN-SLA-028-10, RN-SLA-028-11 |
| UC01 | RN-SLA-028-01, RN-SLA-028-06, RN-SLA-028-07, RN-SLA-028-08, RN-SLA-028-09, RN-SLA-028-10 |
| UC02 | RN-SLA-028-10 |
| UC03 | RN-SLA-028-01, RN-SLA-028-10 |
| UC04 | RN-SLA-028-10, RN-SLA-028-11 |
| UC05 | RN-SLA-028-02, RN-SLA-028-12 |
| UC06 | RN-SLA-028-03 |
| UC07 | RN-SLA-028-03 |
| UC08 | RN-SLA-028-04, RN-SLA-028-05 |

**Cobertura Total**: 12/12 regras (100%)

### Verificação de Cobertura por RN

- **RN-SLA-028-01** (Hierarquia tempos): UC01, UC03 ✅
- **RN-SLA-028-02** (Cálculo exclui pausas/feriados): UC05 ✅
- **RN-SLA-028-03** (Pausa/retomada automática): UC06, UC07 ✅
- **RN-SLA-028-04** (Alertas em cascata): UC08 ✅
- **RN-SLA-028-05** (Escalação automática): UC08 ✅
- **RN-SLA-028-06** (Metas P1): UC01 ✅
- **RN-SLA-028-07** (Metas P2): UC01 ✅
- **RN-SLA-028-08** (Metas P3): UC01 ✅
- **RN-SLA-028-09** (Metas P4): UC01 ✅
- **RN-SLA-028-10** (Multi-tenancy): UC00, UC01, UC02, UC03, UC04 ✅
- **RN-SLA-028-11** (Soft delete): UC00, UC04 ✅
- **RN-SLA-028-12** (BrasilAPI feriados): UC05 ✅

---

## CHANGELOG

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 1.0 | 2025-12-17 | Architect Agent | Versão inicial com 8 casos de uso |
| 2.0 | 2025-12-31 | Agência ALC - alc.dev.br | Recriação completa conforme template v2.0 com 9 UCs cobrindo 100% das 12 RNs |

---

**Última Atualização:** 2025-12-31
**Autor:** Agência ALC - alc.dev.br
**Cobertura:** 100% das regras de negócio RF028 (12/12 RNs)
