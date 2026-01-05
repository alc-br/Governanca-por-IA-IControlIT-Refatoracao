# UC-RF033 — Casos de Uso Canônicos

**RF:** RF033 — Gestão de Chamados (Service Desk)
**Versão:** 2.0
**Data:** 2025-12-31
**Autor:** Agência ALC - alc.dev.br
**Epic:** EPIC008-SD-Service-Desk
**Fase:** Fase 5 - Service Desk

---

## 1. OBJETIVO

Este documento especifica os **5 Casos de Uso Canônicos** do **RF033 — Gestão de Chamados (Service Desk)**, cobrindo as operações CRUD essenciais e funcionalidades avançadas de SLA, workflow e notificações.

**Escopo:**
- Abertura de chamados com cálculo automático de SLA
- Listagem com filtros avançados e dashboard em tempo real
- Visualização detalhada com histórico de interações
- Atualização de status, atribuição e adição de interações
- Encerramento com avaliação de satisfação e reabertura controlada

**Padrões Aplicados:**
- Multi-tenancy obrigatório (isolamento por `ConglomeradoId`)
- RBAC granular (permissões diferenciadas por perfil)
- Soft delete (nunca exclusão física)
- Auditoria completa (7 anos de retenção - LGPD)
- i18n em todas as mensagens (pt-BR, en-US, es-ES)

---

## 2. SUMÁRIO DOS CASOS DE USO

| UC | Nome | Ator Principal | Tipo | Impacta Dados |
|----|------|----------------|------|---------------|
| **UC00** | Listar Chamados | `usuario_autenticado` | Leitura | Não |
| **UC01** | Criar Chamado | `usuario_autenticado` | Escrita | Sim |
| **UC02** | Visualizar Chamado | `usuario_autenticado` | Leitura | Não |
| **UC03** | Editar Chamado | `suporte_atendente` | Escrita | Sim |
| **UC04** | Encerrar Chamado | `suporte_supervisor` | Escrita | Sim |

---

## 3. PADRÕES GERAIS APLICÁVEIS A TODOS OS UCs

### 3.1 Multi-Tenancy (Isolamento de Conglomerado)

**Regra:** Todos os UCs DEVEM filtrar dados por `ConglomeradoId` do usuário autenticado.

**Implementação:**
- Queries: `WHERE ConglomeradoId = @UsuarioConglomeradoId AND Fl_Ativo = 1`
- Tentativa de acesso a chamado de outro conglomerado → HTTP 403

### 3.2 Controle de Acesso (RBAC)

**Matriz de Permissões:**

| UC | Permissão Requerida | Perfis Autorizados |
|----|---------------------|---------------------|
| UC00 | `GES.CHAMADOS.VIEW` | Todos os usuários |
| UC01 | `GES.CHAMADOS.CREATE` | Todos os usuários |
| UC02 | `GES.CHAMADOS.VIEW` | Todos os usuários |
| UC03 | `GES.CHAMADOS.UPDATE` | Suporte Nível 1+, Admin |
| UC04 | `GES.CHAMADOS.CLOSE` | Suporte Nível 2+, Admin |

**Usuário sem permissão → HTTP 403**

### 3.3 Auditoria Automática

**Operações auditadas:**
- **CREATE**: Abertura de chamado
- **UPDATE**: Alteração de status, atribuição, adição de interação
- **CLOSE**: Encerramento
- **REOPEN**: Reabertura
- **EVALUATE**: Avaliação de satisfação
- **ESCALATE**: Escalação automática
- **ATTACH**: Upload de anexo

**Retenção:** 7 anos (LGPD)
**Campos registrados:** `UsuarioId`, `DataOperacao`, `IP`, `Operacao`, `DadosAntes`, `DadosDepois`

### 3.4 Internacionalização (i18n)

**Chaves principais:**
- `chamados.titulo` - "Gestão de Chamados"
- `chamados.campos.numero` - "Número"
- `chamados.status.aberto` - "Aberto"
- `chamados.acoes.criar` - "Abrir Chamado"
- `chamados.mensagens.sucesso.criado` - "Chamado criado com sucesso"
- `chamados.validacoes.titulo_obrigatorio` - "Título é obrigatório"

**Idiomas:** pt-BR (padrão), en-US, es-ES

### 3.5 Validações Comuns

**Todos os UCs de escrita (UC01, UC03, UC04):**
- Validação de entrada obrigatória (FluentValidation)
- Proteção contra injeção SQL (EF Core ORM)
- Soft delete (nunca exclusão física)
- Validação de unicidade
- Validação de integridade referencial

---

## 4. CASOS DE USO

---

### UC00 — Listar Chamados

**Objetivo:** Listar chamados com filtros avançados, paginação, ordenação e dashboard em tempo real.

**Ator Principal:** `usuario_autenticado`

**Pré-condições:**
- Usuário autenticado
- Possui permissão `GES.CHAMADOS.VIEW`

**Pós-condições:**
- Lista de chamados retornada (próprios ou de toda a equipe, conforme perfil)
- Dashboard atualizado em tempo real (SignalR)

---

#### FP-UC00-001 — Acessar Tela de Chamados

**Ação:** Usuário acessa `/gestao/chamados`

**Sistema:**
1. Verifica autenticação e permissão `GES.CHAMADOS.VIEW`
2. Renderiza tela com:
   - Grid de chamados
   - Filtros (status, prioridade, fila, período, solicitante, atendente)
   - Dashboard de SLA (cards com totais, gráficos)
   - Botão "Abrir Chamado"
3. Carrega chamados com paginação padrão (25 registros, página 1)

**Cobertura:**
- RF033-CRUD-02 (Listar chamados)
- RF033-SEC-01 (Isolamento multi-tenant)
- RF033-SEC-02 (Permissões RBAC)

---

#### FP-UC00-002 — Aplicar Filtros

**Ação:** Usuário preenche filtros e clica "Buscar"

**Sistema:**
1. Valida filtros
2. Monta query com cláusulas WHERE:
   - `ConglomeradoId = @UsuarioConglomeradoId`
   - `Fl_Ativo = 1`
   - Filtros adicionais (status, prioridade, fila, período, solicitante, atendente)
3. Se perfil = "Usuário" → adiciona `SolicitanteId = @UsuarioId`
4. Se perfil = "Suporte Nível 1+" → retorna todos do conglomerado
5. Retorna lista paginada

**Cobertura:**
- RF033-CRUD-02 (Listar chamados)
- RF033-SEC-01 (Isolamento multi-tenant)
- RN-RF033-16 (Isolamento multi-tenant)

---

#### FP-UC00-003 — Ordenar e Paginar

**Ação:** Usuário clica em coluna para ordenar ou muda página

**Sistema:**
1. Aplica ordenação solicitada (ASC/DESC)
2. Aplica paginação (25, 50 ou 100 registros por página)
3. Retorna nova página de dados

**Cobertura:**
- RF033-CRUD-02 (Listar chamados)

---

#### FP-UC00-004 — Visualizar Dashboard SLA

**Ação:** Sistema atualiza dashboard automaticamente (SignalR)

**Sistema:**
1. Job executa a cada 15 minutos:
   - Total de chamados abertos
   - Chamados vencendo SLA (80%)
   - Chamados vencidos (100%)
   - Chamados encerrados (últimos 30 dias)
   - Tempo médio de resolução
   - Avaliação média de satisfação
2. Envia atualização via SignalR para clientes conectados
3. Dashboard re-renderiza cards e gráficos

**Cobertura:**
- RF033-FUNC-02 (Alertas SLA)
- RF033-FUNC-06 (Dashboard em tempo real)

---

**Fluxos Alternativos:** Nenhum

**Fluxos de Exceção:**

#### FE-UC00-001 — Usuário sem Permissão

**Condição:** Usuário não possui `GES.CHAMADOS.VIEW`

**Sistema:**
1. Retorna HTTP 403
2. Exibe mensagem i18n: `chamados.mensagens.erro.sem_permissao`

**Cobertura:**
- RF033-SEC-02 (Permissões RBAC)

---

**Regras de Negócio:**
- RN-RF033-01 (Atribuição automática a fila)
- RN-RF033-05 (Alertas SLA)
- RN-RF033-10 (Notificações automáticas)
- RN-RF033-16 (Isolamento multi-tenant)

---

### UC01 — Criar Chamado

**Objetivo:** Abrir novo chamado com cálculo automático de SLA e notificações.

**Ator Principal:** `usuario_autenticado`

**Pré-condições:**
- Usuário autenticado
- Possui permissão `GES.CHAMADOS.CREATE`

**Pós-condições:**
- Chamado criado com status `Aberto`
- SLA calculado automaticamente
- Notificações enviadas (solicitante + fila)
- Evento `ChamadoCriado` emitido

---

#### FP-UC01-001 — Acessar Formulário de Criação

**Ação:** Usuário clica em "Abrir Chamado"

**Sistema:**
1. Verifica permissão `GES.CHAMADOS.CREATE`
2. Renderiza formulário com campos:
   - Título* (máx 200 caracteres)
   - Descrição* (máx 2000 caracteres)
   - Tipo de Solicitação* (dropdown - carrega ativos do conglomerado)
   - Prioridade* (Alta, Média, Baixa)
   - Fila de Atendimento* (dropdown - carrega filas ativas do conglomerado)
   - Ativo (opcional - autocomplete)
   - Unidade Consumidor (opcional - autocomplete)
   - Anexos (opcional - múltiplos arquivos)

**Cobertura:**
- RF033-CRUD-01 (Criar chamado)

---

#### FP-UC01-002 — Preencher e Validar Campos

**Ação:** Usuário preenche campos obrigatórios e opcionais

**Sistema:**
1. Validações frontend (real-time):
   - Título obrigatório (1-200 caracteres)
   - Descrição obrigatória (1-2000 caracteres)
   - Tipo de Solicitação obrigatório
   - Prioridade obrigatória
   - Fila de Atendimento obrigatória
2. Campos opcionais:
   - Ativo (se informado, valida existência e conglomerado)
   - Unidade Consumidor (se informado, valida existência e conglomerado)
   - Anexos (valida extensões e tamanho)

**Cobertura:**
- RF033-VAL-01 (Validar campos obrigatórios)
- RF033-VAL-05 (Validar limite anexos)

---

#### FP-UC01-003 — Submeter Criação

**Ação:** Usuário clica em "Abrir Chamado"

**Sistema:**
1. Valida backend (FluentValidation):
   - Campos obrigatórios preenchidos
   - Tipo de Solicitação existe e está ativo
   - Fila de Atendimento existe e está ativa
   - Anexos dentro dos limites (10 MB/arquivo, 50 MB/chamado)
2. Calcula SLA:
   - Busca `TipoSolicitacao.SLA.PrazoDias`
   - Calcula data de vencimento considerando:
     - Apenas dias úteis (seg-sex)
     - Exclusão de datas de parada cadastradas
     - Determina `DataVencimento`
3. Cria registro em `Chamado`:
   - `Numero` = auto-incremento por conglomerado
   - `Status` = `Aberto`
   - `SolicitanteId` = usuário logado
   - `DataAbertura` = `DateTime.Now`
   - `DataVencimento` = calculado
   - `ConglomeradoId` = conglomerado do usuário
   - `FilaAtendimentoId` = informado
   - `AtivoId` = opcional
   - `ConsumidorUnidadeId` = opcional
4. Upload de anexos (se houver)
5. Emite evento `ChamadoCriado`
6. Envia notificações:
   - Solicitante: confirmação de abertura
   - Fila de Atendimento: novo chamado para atendimento
7. Registra auditoria (`CREATE`)
8. Retorna HTTP 201 + ID do chamado

**Cobertura:**
- RF033-CRUD-01 (Criar chamado)
- RF033-CRUD-07 (Upload de anexo)
- RF033-VAL-01 (Validar campos obrigatórios)
- RF033-FUNC-01 (Cálculo automático de SLA)
- RF033-FUNC-05 (Notificações automáticas)
- RN-RF033-01 (Atribuição automática a fila)
- RN-RF033-02 (Cálculo automático de SLA)
- RN-RF033-08 (Atribuição a fila de atendimento)
- RN-RF033-09 (Vinculação a ativo ou consumidor)
- RN-RF033-10 (Notificações automáticas)
- RN-RF033-13 (Anexos e evidências)

---

**Fluxos Alternativos:** Nenhum

**Fluxos de Exceção:**

#### FE-UC01-001 — Campo Obrigatório Ausente

**Condição:** Título, Descrição, Tipo de Solicitação, Prioridade ou Fila ausentes

**Sistema:**
1. Retorna HTTP 400
2. Exibe mensagem i18n específica por campo:
   - `chamados.validacoes.titulo_obrigatorio`
   - `chamados.validacoes.descricao_obrigatoria`
   - `chamados.validacoes.tipo_solicitacao_obrigatorio`

**Cobertura:**
- RF033-VAL-01 (Validar campos obrigatórios)

---

#### FE-UC01-002 — Anexo Excede Limite

**Condição:** Arquivo > 10 MB OU total > 50 MB

**Sistema:**
1. Retorna HTTP 400
2. Exibe mensagem i18n: `chamados.validacoes.anexo_excede_limite`

**Cobertura:**
- RF033-VAL-05 (Validar limite anexos)
- RN-RF033-13 (Anexos e evidências)

---

#### FE-UC01-003 — Fila Inválida ou Inativa

**Condição:** Fila não existe, está inativa ou pertence a outro conglomerado

**Sistema:**
1. Retorna HTTP 400
2. Exibe mensagem i18n: `chamados.validacoes.fila_invalida`

**Cobertura:**
- RF033-VAL-01 (Validar campos obrigatórios)
- RN-RF033-08 (Atribuição a fila de atendimento)

---

**Regras de Negócio:**
- RN-RF033-01 (Atribuição automática a fila)
- RN-RF033-02 (Cálculo automático de SLA)
- RN-RF033-08 (Atribuição a fila de atendimento)
- RN-RF033-09 (Vinculação a ativo ou consumidor)
- RN-RF033-10 (Notificações automáticas)
- RN-RF033-13 (Anexos e evidências)
- RN-RF033-16 (Isolamento multi-tenant)

---

### UC02 — Visualizar Chamado

**Objetivo:** Visualizar chamado específico com histórico completo de interações, anexos e SLA.

**Ator Principal:** `usuario_autenticado`

**Pré-condições:**
- Usuário autenticado
- Possui permissão `GES.CHAMADOS.VIEW`
- Chamado pertence ao conglomerado do usuário

**Pós-condições:**
- Detalhes completos do chamado exibidos
- Histórico de interações carregado

---

#### FP-UC02-001 — Acessar Chamado

**Ação:** Usuário clica em chamado na listagem ou acessa `/gestao/chamados/{id}`

**Sistema:**
1. Verifica permissão `GES.CHAMADOS.VIEW`
2. Carrega chamado:
   - `WHERE Id = @ChamadoId AND ConglomeradoId = @UsuarioConglomeradoId AND Fl_Ativo = 1`
3. Se perfil = "Usuário":
   - Verifica `SolicitanteId = @UsuarioId` OU `AtendenteResponsavelId = @UsuarioId`
   - Se não → HTTP 403
4. Carrega dados relacionados:
   - Tipo de Solicitação
   - Fila de Atendimento
   - Solicitante
   - Atendente Responsável (se atribuído)
   - Ativo (se vinculado)
   - Unidade Consumidor (se vinculado)
   - Solução (se encerrado)
   - Avaliação (se avaliado)
5. Renderiza tela com abas:
   - **Resumo**: Dados gerais, SLA, status
   - **Interações**: Histórico de interações (públicas/privadas conforme perfil)
   - **Anexos**: Lista de anexos
   - **Auditoria**: Histórico de alterações (apenas admin)

**Cobertura:**
- RF033-CRUD-03 (Visualizar chamado)
- RF033-SEC-01 (Isolamento multi-tenant)
- RF033-SEC-02 (Permissões RBAC)
- RN-RF033-16 (Isolamento multi-tenant)

---

#### FP-UC02-002 — Visualizar Interações

**Ação:** Usuário acessa aba "Interações"

**Sistema:**
1. Carrega interações do chamado:
   - Se perfil = "Usuário": apenas `FlPublico = true`
   - Se perfil = "Suporte Nível 1+": todas as interações
2. Exibe em ordem cronológica:
   - Autor da interação
   - Data/hora
   - Descrição
   - Indicador público/privado
   - Anexos (se houver)

**Cobertura:**
- RF033-CRUD-06 (Adicionar interação)
- RF033-FUNC-08 (Interações públicas e privadas)
- RN-RF033-07 (Interações públicas e privadas)

---

#### FP-UC02-003 — Visualizar SLA

**Ação:** Sistema exibe card de SLA em tempo real

**Sistema:**
1. Calcula indicadores:
   - Prazo total (dias)
   - Tempo decorrido (%)
   - Tempo restante (dias/horas)
   - Status SLA:
     - **Verde**: < 80%
     - **Amarelo**: 80-100%
     - **Vermelho**: > 100% (vencido)
2. Se status `AguardandoUsuario` ou `AguardandoFornecedor`:
   - Exibe badge "SLA Pausado"
   - Mostra tempo total pausado
3. Atualiza indicador via SignalR (real-time)

**Cobertura:**
- RF033-FUNC-01 (Cálculo automático de SLA)
- RF033-FUNC-02 (Alertas SLA)
- RF033-FUNC-04 (Pausa SLA em status 'Aguardando')
- RN-RF033-02 (Cálculo automático de SLA)
- RN-RF033-05 (Alertas de SLA)
- RN-RF033-12 (Prazo SLA pausado em status 'Aguardando')

---

**Fluxos Alternativos:** Nenhum

**Fluxos de Exceção:**

#### FE-UC02-001 — Chamado Não Encontrado

**Condição:** Chamado não existe ou pertence a outro conglomerado

**Sistema:**
1. Retorna HTTP 404
2. Exibe mensagem i18n: `chamados.mensagens.erro.nao_encontrado`

**Cobertura:**
- RF033-SEC-01 (Isolamento multi-tenant)

---

#### FE-UC02-002 — Usuário sem Acesso ao Chamado

**Condição:** Perfil "Usuário" tentando acessar chamado de outro solicitante

**Sistema:**
1. Retorna HTTP 403
2. Exibe mensagem i18n: `chamados.mensagens.erro.sem_permissao`

**Cobertura:**
- RF033-SEC-02 (Permissões RBAC)
- RN-RF033-16 (Isolamento multi-tenant)

---

**Regras de Negócio:**
- RN-RF033-02 (Cálculo automático de SLA)
- RN-RF033-05 (Alertas de SLA)
- RN-RF033-07 (Interações públicas e privadas)
- RN-RF033-12 (Prazo SLA pausado em status 'Aguardando')
- RN-RF033-16 (Isolamento multi-tenant)

---

### UC03 — Editar Chamado

**Objetivo:** Atualizar chamado (status, atribuição, interações) com validação de workflow e notificações.

**Ator Principal:** `suporte_atendente`

**Pré-condições:**
- Usuário autenticado
- Possui permissão `GES.CHAMADOS.UPDATE`
- Chamado pertence ao conglomerado do usuário

**Pós-condições:**
- Chamado atualizado
- Evento `ChamadoStatusAlterado` ou `ChamadoAtribuido` emitido (se aplicável)
- Notificações enviadas (solicitante + atendente)
- SLA pausado/retomado (se aplicável)

---

#### FP-UC03-001 — Alterar Status

**Ação:** Atendente altera status do chamado

**Sistema:**
1. Verifica permissão `GES.CHAMADOS.UPDATE`
2. Valida transição de status (RN-RF033-03):
   - Carrega `StatusAtual` do chamado
   - Valida se transição `StatusAtual → NovoStatus` é permitida
   - Se não → HTTP 400 com mensagem i18n: `chamados.validacoes.transicao_invalida`
3. Se novo status = `AguardandoUsuario` ou `AguardandoFornecedor`:
   - Define `DataInicioAguardando = DateTime.Now`
4. Se status anterior era `Aguardando*` e novo status = `EmAtendimento`:
   - Calcula `TotalHorasAguardando += (Now - DataInicioAguardando)`
   - Limpa `DataInicioAguardando = null`
5. Atualiza `Status` + `DataUltimaAtualizacao`
6. Emite evento `ChamadoStatusAlterado`
7. Envia notificação ao solicitante
8. Registra auditoria (`UPDATE`)
9. Retorna HTTP 200

**Cobertura:**
- RF033-CRUD-08 (Alterar status)
- RF033-VAL-02 (Validar transições de status)
- RF033-FUNC-04 (Pausa SLA em status 'Aguardando')
- RF033-FUNC-05 (Notificações automáticas)
- RN-RF033-03 (Validação de transições de status)
- RN-RF033-10 (Notificações automáticas)
- RN-RF033-12 (Prazo SLA pausado em status 'Aguardando')

---

#### FP-UC03-002 — Atribuir a Técnico

**Ação:** Supervisor atribui chamado a técnico específico

**Sistema:**
1. Verifica permissão `GES.CHAMADOS.ASSIGN`
2. Valida técnico:
   - Existe e está ativo
   - Pertence ao mesmo conglomerado
   - Possui permissão `GES.CHAMADOS.UPDATE`
3. Atualiza `AtendenteResponsavelId`
4. Altera status para `EmAtendimento` (se estava `Aberto`)
5. Emite evento `ChamadoAtribuido`
6. Envia notificação ao técnico
7. Registra auditoria (`UPDATE`)
8. Retorna HTTP 200

**Cobertura:**
- RF033-CRUD-05 (Atribuir chamado)
- RF033-FUNC-05 (Notificações automáticas)
- RN-RF033-01 (Atribuição automática a fila)
- RN-RF033-10 (Notificações automáticas)

---

#### FP-UC03-003 — Adicionar Interação

**Ação:** Atendente adiciona interação (pública ou privada)

**Sistema:**
1. Verifica permissão `GES.CHAMADOS.UPDATE`
2. Valida campos:
   - Descrição obrigatória (1-2000 caracteres)
   - `FlPublico` obrigatório (true/false)
3. Cria registro em `ChamadoItem`:
   - `ChamadoId`
   - `AutorId` = usuário logado
   - `Descricao`
   - `FlPublico`
   - `DataCriacao = DateTime.Now`
4. Upload de anexos (se houver)
5. Se `FlPublico = true`:
   - Envia notificação ao solicitante
6. Registra auditoria (`ADD_ITEM`)
7. Retorna HTTP 201

**Cobertura:**
- RF033-CRUD-06 (Adicionar interação)
- RF033-CRUD-07 (Upload de anexo)
- RF033-FUNC-05 (Notificações automáticas)
- RF033-FUNC-08 (Interações públicas e privadas)
- RN-RF033-07 (Interações públicas e privadas)
- RN-RF033-10 (Notificações automáticas)
- RN-RF033-13 (Anexos e evidências)

---

**Fluxos Alternativos:**

#### FA-UC03-001 — Escalação Automática por SLA Vencido

**Condição:** Job detecta chamado com SLA vencido e não escalado

**Sistema:**
1. Job executa a cada 15 minutos:
   - `WHERE Status != 'Encerrado' AND Status != 'Cancelado' AND DataVencimento < NOW() AND FlEscalado = false`
2. Para cada chamado:
   - Define `FlEscalado = true`
   - Define `DataEscalacao = DateTime.Now`
   - Cria interação privada: "Chamado escalado automaticamente por SLA vencido"
   - Envia notificação ao supervisor da fila
   - Emite evento `ChamadoEscalado`
   - Registra auditoria (`ESCALATE`)

**Cobertura:**
- RF033-FUNC-03 (Escalação automática)
- RN-RF033-14 (Escalação automática por SLA)

---

**Fluxos de Exceção:**

#### FE-UC03-001 — Transição de Status Inválida

**Condição:** Tentativa de transição não permitida

**Sistema:**
1. Retorna HTTP 400
2. Exibe mensagem i18n: `chamados.validacoes.transicao_invalida`
3. Exibe transições permitidas para status atual

**Cobertura:**
- RF033-VAL-02 (Validar transições de status)
- RN-RF033-03 (Validação de transições de status)

---

#### FE-UC03-002 — Técnico Inválido para Atribuição

**Condição:** Técnico não existe, está inativo ou pertence a outro conglomerado

**Sistema:**
1. Retorna HTTP 400
2. Exibe mensagem i18n: `chamados.validacoes.tecnico_invalido`

**Cobertura:**
- RF033-VAL-01 (Validar campos obrigatórios)

---

**Regras de Negócio:**
- RN-RF033-01 (Atribuição automática a fila)
- RN-RF033-03 (Validação de transições de status)
- RN-RF033-07 (Interações públicas e privadas)
- RN-RF033-10 (Notificações automáticas)
- RN-RF033-12 (Prazo SLA pausado em status 'Aguardando')
- RN-RF033-13 (Anexos e evidências)
- RN-RF033-14 (Escalação automática por SLA)
- RN-RF033-16 (Isolamento multi-tenant)

---

### UC04 — Encerrar Chamado

**Objetivo:** Encerrar chamado com solução obrigatória, avaliar satisfação e permitir reabertura controlada.

**Ator Principal:** `suporte_supervisor`

**Pré-condições:**
- Usuário autenticado
- Possui permissão `GES.CHAMADOS.CLOSE`
- Chamado pertence ao conglomerado do usuário
- Status atual = `Resolvido`

**Pós-condições:**
- Chamado encerrado (status = `Encerrado`)
- Solução obrigatória vinculada
- Evento `ChamadoEncerrado` emitido
- Notificação enviada ao solicitante

---

#### FP-UC04-001 — Encerrar com Solução

**Ação:** Supervisor encerra chamado após resolução

**Sistema:**
1. Verifica permissão `GES.CHAMADOS.CLOSE`
2. Valida status atual = `Resolvido`
3. Valida solução obrigatória:
   - `SolucaoId` deve ser informado
   - Solução deve existir e estar ativa
   - Se não → HTTP 400 com mensagem i18n: `chamados.validacoes.solucao_obrigatoria`
4. Valida se solução pertence ao mesmo conglomerado
5. Atualiza chamado:
   - `Status = Encerrado`
   - `DataEncerramento = DateTime.Now`
   - `SolucaoId` = informado
6. Emite evento `ChamadoEncerrado`
7. Envia notificação ao solicitante (com formulário de avaliação)
8. Registra auditoria (`CLOSE`)
9. Retorna HTTP 200

**Cobertura:**
- RF033-CRUD-09 (Encerrar chamado)
- RF033-VAL-03 (Validar solução obrigatória no encerramento)
- RF033-FUNC-05 (Notificações automáticas)
- RN-RF033-04 (Solução obrigatória no encerramento)
- RN-RF033-10 (Notificações automáticas)

---

#### FP-UC04-002 — Avaliar Satisfação

**Ação:** Solicitante avalia chamado (nota 1-5 + comentário opcional)

**Sistema:**
1. Verifica permissão `GES.CHAMADOS.EVALUATE`
2. Valida:
   - Solicitante do chamado = usuário logado
   - Status = `Encerrado`
   - Ainda não possui avaliação (RN-RF033-17)
   - Nota entre 1 e 5
   - Comentário máximo 500 caracteres
3. Cria registro em `ChamadoAvaliacao`:
   - `ChamadoId`
   - `Nota`
   - `Comentario` (opcional)
   - `DataAvaliacao = DateTime.Now`
4. Emite evento `ChamadoAvaliado`
5. Envia notificação ao técnico responsável e supervisor
6. Registra auditoria (`EVALUATE`)
7. Retorna HTTP 201

**Cobertura:**
- RF033-CRUD-10 (Avaliar chamado)
- RF033-VAL-04 (Validar nota avaliação 1-5)
- RF033-VAL-07 (Validar unicidade de avaliação)
- RF033-FUNC-05 (Notificações automáticas)
- RN-RF033-06 (Avaliação de satisfação opcional)
- RN-RF033-10 (Notificações automáticas)
- RN-RF033-17 (Unicidade de avaliação)

---

#### FP-UC04-003 — Reabrir Chamado

**Ação:** Solicitante ou suporte reabre chamado em até 7 dias após encerramento

**Sistema:**
1. Verifica permissão `GES.CHAMADOS.REOPEN`
2. Valida:
   - Status = `Encerrado`
   - `DataEncerramento` < 7 dias atrás
   - Chamado ainda não foi reaberto (`FlReaberto = false`)
   - Justificativa obrigatória (máx 500 caracteres)
3. Se validações OK:
   - Atualiza `Status = EmAtendimento`
   - Define `FlReaberto = true`
   - Define `DataReabertura = DateTime.Now`
   - Cria interação privada com justificativa
   - Recalcula SLA (novo prazo)
4. Emite evento `ChamadoReaberto`
5. Envia notificações (solicitante + atendente responsável + supervisor)
6. Registra auditoria (`REOPEN`)
7. Retorna HTTP 200

**Cobertura:**
- RF033-CRUD-11 (Reabrir chamado)
- RF033-VAL-06 (Validar reabertura até 7 dias)
- RF033-FUNC-05 (Notificações automáticas)
- RN-RF033-10 (Notificações automáticas)
- RN-RF033-11 (Reabertura de chamado encerrado)

---

**Fluxos Alternativos:** Nenhum

**Fluxos de Exceção:**

#### FE-UC04-001 — Encerramento sem Solução

**Condição:** Tentativa de encerrar sem informar `SolucaoId`

**Sistema:**
1. Retorna HTTP 400
2. Exibe mensagem i18n: `chamados.validacoes.solucao_obrigatoria`

**Cobertura:**
- RF033-VAL-03 (Validar solução obrigatória no encerramento)
- RN-RF033-04 (Solução obrigatória no encerramento)

---

#### FE-UC04-002 — Avaliação Duplicada

**Condição:** Solicitante tenta avaliar chamado já avaliado

**Sistema:**
1. Retorna HTTP 400
2. Exibe mensagem i18n: `chamados.validacoes.avaliacao_duplicada`

**Cobertura:**
- RF033-VAL-07 (Validar unicidade de avaliação)
- RN-RF033-17 (Unicidade de avaliação)

---

#### FE-UC04-003 — Reabertura Após 7 Dias

**Condição:** Tentativa de reabertura após prazo de 7 dias

**Sistema:**
1. Retorna HTTP 400
2. Exibe mensagem i18n: `chamados.validacoes.reabertura_fora_prazo`
3. Sugere abertura de novo chamado

**Cobertura:**
- RF033-VAL-06 (Validar reabertura até 7 dias)
- RN-RF033-11 (Reabertura de chamado encerrado)

---

#### FE-UC04-004 — Nota de Avaliação Inválida

**Condição:** Nota fora do range 1-5

**Sistema:**
1. Retorna HTTP 400
2. Exibe mensagem i18n: `chamados.validacoes.nota_invalida`

**Cobertura:**
- RF033-VAL-04 (Validar nota avaliação 1-5)
- RN-RF033-06 (Avaliação de satisfação opcional)

---

**Regras de Negócio:**
- RN-RF033-04 (Solução obrigatória no encerramento)
- RN-RF033-06 (Avaliação de satisfação opcional)
- RN-RF033-10 (Notificações automáticas)
- RN-RF033-11 (Reabertura de chamado encerrado)
- RN-RF033-15 (Integração com base de conhecimento)
- RN-RF033-16 (Isolamento multi-tenant)
- RN-RF033-17 (Unicidade de avaliação)

---

## 5. MATRIZ DE RASTREABILIDADE

### 5.1 Cobertura RF → UC

| Item RF | Título | Coberto por UC |
|---------|--------|----------------|
| RF033-CRUD-01 | Criar chamado | UC01 |
| RF033-CRUD-02 | Listar chamados | UC00 |
| RF033-CRUD-03 | Visualizar chamado | UC02 |
| RF033-CRUD-04 | Atualizar chamado | UC03 |
| RF033-CRUD-05 | Atribuir chamado | UC03 |
| RF033-CRUD-06 | Adicionar interação | UC03 |
| RF033-CRUD-07 | Upload de anexo | UC01, UC03 |
| RF033-CRUD-08 | Alterar status | UC03 |
| RF033-CRUD-09 | Encerrar chamado | UC04 |
| RF033-CRUD-10 | Avaliar chamado | UC04 |
| RF033-CRUD-11 | Reabrir chamado | UC04 |
| RF033-VAL-01 | Validar campos obrigatórios | UC01, UC03 |
| RF033-VAL-02 | Validar transições de status | UC03 |
| RF033-VAL-03 | Validar solução obrigatória no encerramento | UC04 |
| RF033-VAL-04 | Validar nota avaliação (1-5) | UC04 |
| RF033-VAL-05 | Validar limite anexos | UC01 |
| RF033-VAL-06 | Validar reabertura (até 7 dias) | UC04 |
| RF033-VAL-07 | Validar unicidade de avaliação | UC04 |
| RF033-SEC-01 | Isolamento multi-tenant | UC00, UC01, UC02, UC03, UC04 |
| RF033-SEC-02 | Permissões RBAC | UC00, UC01, UC02, UC03, UC04 |
| RF033-SEC-03 | Auditoria completa (7 anos) | UC00, UC01, UC02, UC03, UC04 |
| RF033-SEC-04 | Soft delete | UC00, UC01, UC02, UC03, UC04 |
| RF033-SEC-05 | Validação de entrada | UC01, UC03, UC04 |
| RF033-FUNC-01 | Cálculo automático de SLA | UC01, UC02 |
| RF033-FUNC-02 | Alertas SLA (80% e 100%) | UC00, UC02 |
| RF033-FUNC-03 | Escalação automática (SLA vencido) | UC03-FA001 |
| RF033-FUNC-04 | Pausa SLA em status 'Aguardando' | UC02, UC03 |
| RF033-FUNC-05 | Notificações automáticas | UC01, UC03, UC04 |
| RF033-FUNC-06 | Dashboard em tempo real (SignalR) | UC00 |
| RF033-FUNC-07 | Base de conhecimento | UC04 |
| RF033-FUNC-08 | Interações públicas e privadas | UC02, UC03 |

**Cobertura RF → UC:** 100% (30/30 itens obrigatórios)

### 5.2 Cobertura RN → UC

| RN | Título | Coberto por UC |
|----|--------|----------------|
| RN-RF033-01 | Atribuição automática a fila | UC01, UC03 |
| RN-RF033-02 | Cálculo automático de SLA | UC01, UC02 |
| RN-RF033-03 | Validação de transições de status | UC03 |
| RN-RF033-04 | Solução obrigatória no encerramento | UC04 |
| RN-RF033-05 | Alertas de SLA | UC00, UC02 |
| RN-RF033-06 | Avaliação de satisfação opcional | UC04 |
| RN-RF033-07 | Interações públicas e privadas | UC02, UC03 |
| RN-RF033-08 | Atribuição a fila de atendimento | UC01 |
| RN-RF033-09 | Vinculação a ativo ou consumidor | UC01 |
| RN-RF033-10 | Notificações automáticas | UC01, UC03, UC04 |
| RN-RF033-11 | Reabertura de chamado encerrado | UC04 |
| RN-RF033-12 | Prazo SLA pausado em status 'Aguardando' | UC02, UC03 |
| RN-RF033-13 | Anexos e evidências | UC01, UC03 |
| RN-RF033-14 | Escalação automática por SLA | UC03-FA001 |
| RN-RF033-15 | Integração com base de conhecimento | UC04 |
| RN-RF033-16 | Isolamento multi-tenant | UC00, UC01, UC02, UC03, UC04 |
| RN-RF033-17 | Unicidade de avaliação | UC04 |

**Cobertura RN → UC:** 100% (17/17 regras de negócio)

---

## 6. CHANGELOG

### v2.0 — 2025-12-31
- **Migração v1.0 → v2.0**: Conformidade total com template canônico
- **Adicionado**: Metadatos Epic, Fase, Autor
- **Adicionado**: Seção "PADRÕES GERAIS APLICÁVEIS A TODOS OS UCs"
- **Reestruturação completa**: 5 UCs canônicos (UC00-UC04)
- **Adicionado**: Matriz de rastreabilidade completa (RF + RN → UC)
- **Adicionado**: 30 itens de cobertura RF (CRUD, VAL, SEC, FUNC)
- **Adicionado**: 17 regras de negócio detalhadas
- **Adicionado**: Seção `covers` em todos os fluxos principais
- **Validação**: Conformidade 100% com validator-docs.py

### v1.0 — 2025-01-14
- Versão inicial (10 UCs em formato v1.0)
