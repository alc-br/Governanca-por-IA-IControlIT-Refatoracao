# UC-RF049 — Casos de Uso Canônicos

**RF:** RF049 — Gestão de Políticas de Consumidores
**Epic:** EPIC008-SD - Service Desk
**Fase:** Fase 5 - Service Desk
**Versão:** 2.0
**Data:** 2025-12-31
**Autor:** Agência ALC - alc.dev.br

---

## 1. OBJETIVO DO DOCUMENTO

Este documento descreve **todos os Casos de Uso (UC)** derivados do **RF049**, cobrindo integralmente o comportamento funcional esperado.

Os UCs aqui definidos servem como **contrato comportamental**, sendo a **fonte primária** para geração de:
- Casos de Teste (TC-RF049.yaml)
- Massas de Teste (MT-RF049.yaml)
- Evidências de auditoria e validação funcional
- Execução por agentes de IA (tester, QA, E2E)

---

## 2. SUMÁRIO DE CASOS DE USO

| ID | Nome | Ator Principal |
|----|------|----------------|
| UC00 | Listar Políticas de Consumidores | Usuário Autenticado |
| UC01 | Criar Política de Consumidor | Gestor de Políticas |
| UC02 | Visualizar Política de Consumidor | Usuário Autenticado |
| UC03 | Editar Política de Consumidor | Gestor de Políticas |
| UC04 | Excluir Política de Consumidor | Gestor de Políticas |
| UC05 | Aplicar Política a Consumidores | Gestor de Políticas |
| UC06 | Remover Política de Consumidores | Gestor de Políticas |
| UC07 | Processamento em Lote de Aplicação | Gestor de Políticas |
| UC08 | Avaliar Violação em Tempo Real | Sistema |
| UC09 | Simular Impacto de Política | Gestor de Políticas |
| UC10 | Gerenciar Alertas Proativos | Sistema |
| UC11 | Executar Bloqueios Automáticos | Sistema |
| UC12 | Visualizar Histórico de Aplicações | Usuário Autenticado |
| UC13 | Visualizar Dashboard de Conformidade | Gestor de Políticas |
| UC14 | Importar/Exportar Políticas | Administrador de Políticas |
| UC15 | Gerenciar Templates de Políticas | Administrador de Políticas |

---

## 3. PADRÕES GERAIS APLICÁVEIS A TODOS OS UCs

- Todos os acessos respeitam **isolamento por tenant** (Id_Fornecedor)
- Todas as ações exigem **permissão explícita** (RBAC)
- Erros não devem vazar informações sensíveis
- Auditoria deve registrar **quem**, **quando** e **qual ação**
- Mensagens devem ser claras, previsíveis e rastreáveis
- Histórico de aplicações/violações retido por 7 anos (LGPD)
- Motor de políticas avalia regras em tempo real (≤100ms P95)
- Políticas aplicadas por perfil/status são automáticas via Domain Events

---

## UC00 — Listar Políticas de Consumidores

### Objetivo
Permitir que o usuário visualize todas as políticas de consumidores disponíveis no seu tenant, com filtros e paginação.

### Pré-condições
- Usuário autenticado
- Permissão `GESTAO.POLITICAS.VIEW`

### Pós-condições
- Lista exibida conforme filtros e paginação
- Dados isolados por tenant

### Fluxo Principal
- **FP-UC00-001:** Usuário acessa Gestão → Políticas de Consumidores
- **FP-UC00-002:** Sistema valida permissão GESTAO.POLITICAS.VIEW
- **FP-UC00-003:** Sistema carrega políticas do tenant (Id_Fornecedor)
- **FP-UC00-004:** Sistema aplica paginação padrão (20 registros)
- **FP-UC00-005:** Sistema exibe lista com colunas: Nome, Tipo, Status, Consumidores Vinculados, Violações Ativas, Data Criação
- **FP-UC00-006:** Sistema permite ordenação por qualquer coluna

### Fluxos Alternativos
- **FA-UC00-001:** Usuário aplica filtro por Tipo de Política
  - Sistema recarrega lista filtrando por tipo selecionado (Limite Monetário, Franquia Dados, Franquia Voz, etc.)
- **FA-UC00-002:** Usuário aplica filtro por Status
  - Sistema recarrega lista filtrando por status (Rascunho, Ativa, Suspensa, Inativa, Cancelada)
- **FA-UC00-003:** Usuário busca por nome da política
  - Sistema aplica busca textual no campo Nome
- **FA-UC00-004:** Usuário ordena por coluna
  - Sistema reordena lista conforme coluna e direção (ASC/DESC)

### Fluxos de Exceção
- **FE-UC00-001:** Usuário sem permissão GESTAO.POLITICAS.VIEW
  - Sistema retorna HTTP 403 Forbidden
  - Exibe mensagem: "Acesso negado. Você não tem permissão para visualizar políticas."
- **FE-UC00-002:** Nenhuma política encontrada
  - Sistema exibe estado vazio: "Nenhuma política cadastrada. Clique em 'Nova Política' para criar."
- **FE-UC00-003:** Erro ao carregar dados
  - Sistema exibe mensagem: "Erro ao carregar políticas. Tente novamente."
  - Registra erro no log estruturado

### Regras de Negócio
- **RN-UC00-001:** Somente políticas do tenant do usuário autenticado devem ser exibidas
- **RN-UC00-002:** Políticas excluídas (Fl_Excluido=true) NÃO devem aparecer na listagem
- **RN-UC00-003:** Paginação padrão de 20 registros por página
- **RN-UC00-004:** Ordenação padrão: Data de Criação DESC (mais recentes primeiro)

### Critérios de Aceite
- **CA-UC00-001:** A lista DEVE exibir apenas políticas do tenant do usuário autenticado
- **CA-UC00-002:** Políticas excluídas (soft delete) NÃO devem aparecer na listagem
- **CA-UC00-003:** Paginação DEVE ser aplicada com limite padrão de 20 registros
- **CA-UC00-004:** Sistema DEVE permitir ordenação por qualquer coluna visível
- **CA-UC00-005:** Filtros DEVEM ser acumuláveis e refletir na URL para compartilhamento
- **CA-UC00-006:** Performance: Lista DEVE carregar em ≤2 segundos (P95)

---

## UC01 — Criar Política de Consumidor

### Objetivo
Permitir a criação de uma nova política de consumidor com múltiplos tipos de restrições configuráveis.

### Pré-condições
- Usuário autenticado
- Permissão `GESTAO.POLITICAS.CREATE`
- Conhecimento dos tipos de políticas suportados

### Pós-condições
- Política criada com status "Rascunho"
- Auditoria registrada (CREATE)
- Registro disponível para aplicação

### Fluxo Principal
- **FP-UC01-001:** Usuário clica em "Nova Política"
- **FP-UC01-002:** Sistema valida permissão GESTAO.POLITICAS.CREATE
- **FP-UC01-003:** Sistema exibe wizard de criação de política (3 etapas)
- **FP-UC01-004:** **Etapa 1 - Dados Básicos:** Usuário informa Nome*, Descrição, Tipo* (Limite Monetário, Franquia Dados, Franquia Voz, Franquia SMS, Restrição Horário, Restrição Destinos, Limite Roaming, Limite por Tipo Serviço)
- **FP-UC01-005:** Sistema valida unicidade do Nome no tenant
- **FP-UC01-006:** **Etapa 2 - Configurações:** Usuário configura limites/restrições conforme tipo selecionado (ex: Valor Máximo R$, Quantidade MB/Minutos/SMS, Horários Permitidos, Destinos Bloqueados)
- **FP-UC01-007:** Sistema valida formato e valores dos limites (valores positivos, horários válidos, etc.)
- **FP-UC01-008:** **Etapa 3 - Ações e Alertas:** Usuário configura: Limiares de Alerta (50%, 80%, 100%), Ação ao Violar (Alertar/Bloquear Parcial/Bloquear Total), Flag AlertOnly (se true, apenas alerta sem bloquear), Canais de Notificação (E-mail, SMS, In-app)
- **FP-UC01-009:** Usuário clica em "Salvar"
- **FP-UC01-010:** Sistema valida todos os dados (campos obrigatórios, formatos, consistência)
- **FP-UC01-011:** Sistema cria registro PoliticaConsumidor com status "Rascunho"
- **FP-UC01-012:** Sistema preenche campos de auditoria (Id_Usuario_Criacao, Dt_Criacao)
- **FP-UC01-013:** Sistema preenche Id_Fornecedor automaticamente
- **FP-UC01-014:** Sistema registra evento de auditoria (POLITICA_CREATED)
- **FP-UC01-015:** Sistema exibe mensagem de sucesso: "Política criada com sucesso. Status: Rascunho."
- **FP-UC01-016:** Sistema redireciona para UC02 (Visualizar Política)

### Fluxos Alternativos
- **FA-UC01-001:** Usuário seleciona "Salvar e Criar Outra"
  - Sistema salva política atual
  - Sistema limpa formulário
  - Sistema mantém usuário no wizard para criar nova política
- **FA-UC01-002:** Usuário clica em "Cancelar" durante preenchimento
  - Sistema solicita confirmação: "Descartar alterações?"
  - Se confirmado: volta para UC00 sem salvar
  - Se cancelado: mantém no wizard
- **FA-UC01-003:** Usuário seleciona "Aplicar Template"
  - Sistema abre modal de seleção de templates
  - Usuário seleciona template (Executivo, Gerente, Colaborador, Estagiário)
  - Sistema preenche formulário com dados do template
  - Usuário pode customizar valores antes de salvar
- **FA-UC01-004:** Usuário cria política customizada (Super Admin)
  - Usuário informa configuração JSON customizada
  - Sistema valida schema JSON
  - Sistema permite combinação de múltiplos tipos de restrições

### Fluxos de Exceção
- **FE-UC01-001:** Nome da política já existe no tenant
  - Sistema exibe erro no campo: "Já existe uma política com este nome."
  - Sistema não permite avançar no wizard
- **FE-UC01-002:** Valores inválidos (ex: limite negativo, horário fora do formato)
  - Sistema exibe erro no campo específico
  - Sistema não permite salvar até correção
- **FE-UC01-003:** Configuração JSON inválida (políticas customizadas)
  - Sistema exibe erro: "Schema JSON inválido. Consulte a documentação."
  - Sistema não permite salvar
- **FE-UC01-004:** Erro ao salvar no banco de dados
  - Sistema exibe mensagem: "Erro ao criar política. Tente novamente."
  - Sistema registra erro no log estruturado
  - Transação é revertida (rollback)

### Regras de Negócio
- **RN-UC01-001 (RN-RF049-01):** Tipos suportados: Limite Monetário (R$), Franquia de Dados (MB/GB), Franquia de Voz (minutos), Franquia de SMS (quantidade), Restrição de Horário, Restrição de Destinos, Limite de Roaming, Limite por Tipo de Serviço
- **RN-UC01-002 (RN-RF049-01):** Cada política pode combinar múltiplos tipos de restrições
- **RN-UC01-003:** Campo Nome é único por tenant (Id_Fornecedor)
- **RN-UC01-004:** Id_Fornecedor preenchido automaticamente com tenant do usuário autenticado
- **RN-UC01-005:** Id_Usuario_Criacao preenchido automaticamente
- **RN-UC01-006:** Dt_Criacao preenchido automaticamente com timestamp atual
- **RN-UC01-007:** Status inicial sempre "Rascunho"
- **RN-UC01-008 (RN-RF049-11):** Templates disponíveis: Executivo (sem limites), Gerente (R$ 500), Colaborador (R$ 200), Estagiário (R$ 50)
- **RN-UC01-009:** Valores monetários devem ser positivos
- **RN-UC01-010:** Franquias (dados/voz/SMS) devem ser positivas
- **RN-UC01-011:** Limiares de alerta devem estar entre 1% e 100%

### Critérios de Aceite
- **CA-UC01-001:** Todos os campos obrigatórios DEVEM ser validados antes de persistir
- **CA-UC01-002:** Id_Fornecedor DEVE ser preenchido automaticamente com tenant do usuário autenticado
- **CA-UC01-003:** Id_Usuario_Criacao DEVE ser preenchido automaticamente
- **CA-UC01-004:** Dt_Criacao DEVE ser preenchido automaticamente com timestamp UTC
- **CA-UC01-005:** Sistema DEVE validar unicidade do Nome dentro do tenant
- **CA-UC01-006:** Sistema DEVE retornar erro claro se validação falhar
- **CA-UC01-007:** Auditoria DEVE ser registrada APÓS sucesso da criação
- **CA-UC01-008:** Wizard DEVE ter 3 etapas bem definidas
- **CA-UC01-009:** Templates DEVEM preencher formulário para customização

---

## UC02 — Visualizar Política de Consumidor

### Objetivo
Permitir visualização detalhada de uma política específica, incluindo consumidores vinculados e histórico de violações.

### Pré-condições
- Usuário autenticado
- Permissão `GESTAO.POLITICAS.VIEW`
- Política existe no tenant do usuário

### Pós-condições
- Dados exibidos corretamente
- Informações de auditoria visíveis

### Fluxo Principal
- **FP-UC02-001:** Usuário seleciona política na lista (UC00) ou acessa por URL
- **FP-UC02-002:** Sistema valida permissão GESTAO.POLITICAS.VIEW
- **FP-UC02-003:** Sistema valida que política pertence ao tenant do usuário
- **FP-UC02-004:** Sistema carrega dados da política
- **FP-UC02-005:** Sistema exibe tela com 4 abas: Dados Gerais, Consumidores Vinculados, Histórico de Aplicações, Violações
- **FP-UC02-006:** **Aba Dados Gerais:** Exibe Nome, Tipo, Descrição, Status, Limites/Restrições Configuradas, Ações ao Violar, Limiares de Alerta, Data Criação, Criado Por, Última Alteração, Alterado Por
- **FP-UC02-007:** **Aba Consumidores Vinculados:** Lista consumidores com a política aplicada (Nome, Departamento, Data Aplicação, Status Conformidade, % Consumo do Limite)
- **FP-UC02-008:** **Aba Histórico de Aplicações:** Lista histórico de aplicações/remoções (Data, Usuário, Consumidor, Ação, Motivo)
- **FP-UC02-009:** **Aba Violações:** Lista violações registradas (Data, Consumidor, Valor Limite, Valor Consumido, Ação Tomada, Responsável Liberação)

### Fluxos Alternativos
- **FA-UC02-001:** Usuário clica em "Editar" na tela de visualização
  - Sistema redireciona para UC03 (Editar Política)
- **FA-UC02-002:** Usuário clica em "Aplicar Política"
  - Sistema abre modal de aplicação (UC05)
- **FA-UC02-003:** Usuário exporta dados da política
  - Sistema gera JSON com configuração completa
  - Sistema oferece download do arquivo

### Fluxos de Exceção
- **FE-UC02-001:** Política não encontrada
  - Sistema retorna HTTP 404 Not Found
  - Exibe mensagem: "Política não encontrada."
- **FE-UC02-002:** Política pertence a outro tenant
  - Sistema retorna HTTP 404 Not Found (não vaza existência)
  - Exibe mensagem: "Política não encontrada."
- **FE-UC02-003:** Usuário sem permissão GESTAO.POLITICAS.VIEW
  - Sistema retorna HTTP 403 Forbidden
  - Exibe mensagem: "Acesso negado."

### Regras de Negócio
- **RN-UC02-001:** Usuário SÓ pode visualizar políticas do próprio tenant
- **RN-UC02-002:** Informações de auditoria DEVEM ser exibidas (criado por, criado em, alterado por, alterado em)
- **RN-UC02-003:** Consumidores vinculados exibem status em tempo real (Conforme, Aviso, Crítico, Violação)
- **RN-UC02-004:** Histórico de aplicações é imutável e retido por 7 anos

### Critérios de Aceite
- **CA-UC02-001:** Usuário SÓ pode visualizar políticas do próprio tenant
- **CA-UC02-002:** Informações de auditoria DEVEM ser exibidas
- **CA-UC02-003:** Tentativa de acessar política de outro tenant DEVE retornar 404
- **CA-UC02-004:** Tentativa de acessar política inexistente DEVE retornar 404
- **CA-UC02-005:** Dados exibidos DEVEM corresponder exatamente ao estado atual no banco
- **CA-UC02-006:** Abas DEVEM carregar dados sob demanda (lazy loading) para performance

---

## UC03 — Editar Política de Consumidor

### Objetivo
Permitir alteração controlada de uma política existente, sem afetar aplicações históricas.

### Pré-condições
- Usuário autenticado
- Permissão `GESTAO.POLITICAS.UPDATE`
- Política existe e pertence ao tenant do usuário
- Política não está em status "Inativa" ou "Cancelada"

### Pós-condições
- Política atualizada
- Auditoria registrada (UPDATE)
- Alterações NÃO retroativas (aplicações existentes mantêm configuração original)

### Fluxo Principal
- **FP-UC03-001:** Usuário acessa UC02 e clica em "Editar"
- **FP-UC03-002:** Sistema valida permissão GESTAO.POLITICAS.UPDATE
- **FP-UC03-003:** Sistema valida que política NÃO está em estado final (Inativa/Cancelada)
- **FP-UC03-004:** Sistema carrega dados atuais da política
- **FP-UC03-005:** Sistema exibe wizard de edição (mesma estrutura do UC01)
- **FP-UC03-006:** Usuário altera campos desejados (Nome, Descrição, Limites, Ações, Alertas)
- **FP-UC03-007:** Sistema valida alterações (campos obrigatórios, formatos, unicidade do Nome)
- **FP-UC03-008:** Usuário clica em "Salvar"
- **FP-UC03-009:** Sistema persiste alterações
- **FP-UC03-010:** Sistema preenche Id_Usuario_Alteracao e Dt_Alteracao automaticamente
- **FP-UC03-011:** Sistema registra evento de auditoria (POLITICA_UPDATED) com diff de alterações
- **FP-UC03-012:** Sistema exibe mensagem: "Política atualizada com sucesso. Alterações NÃO afetam aplicações já existentes."
- **FP-UC03-013:** Sistema redireciona para UC02 (Visualizar)

### Fluxos Alternativos
- **FA-UC03-001:** Usuário clica em "Cancelar" durante edição
  - Sistema solicita confirmação: "Descartar alterações?"
  - Se confirmado: volta para UC02 sem salvar
  - Se cancelado: mantém no wizard
- **FA-UC03-002:** Usuário altera status da política
  - Sistema valida transição de estado permitida (conforme tabela de transições do RF049)
  - Se transição permitida: aplica mudança de estado
  - Se transição proibida: exibe erro "Transição de estado não permitida."

### Fluxos de Exceção
- **FE-UC03-001:** Erro de validação (ex: nome duplicado, valores inválidos)
  - Sistema exibe erro no campo específico
  - Sistema não permite salvar até correção
- **FE-UC03-002:** Tentativa de editar política em estado final (Inativa/Cancelada)
  - Sistema exibe mensagem: "Políticas inativas ou canceladas não podem ser editadas."
  - Sistema desabilita botão "Salvar"
- **FE-UC03-003:** Conflito de edição concorrente (outro usuário editou simultaneamente)
  - Sistema detecta via timestamp (Dt_Alteracao)
  - Sistema exibe mensagem: "Esta política foi alterada por outro usuário. Recarregue a página."
  - Sistema não permite salvar (evita perda de dados)
- **FE-UC03-004:** Erro ao salvar no banco de dados
  - Sistema exibe mensagem: "Erro ao atualizar política. Tente novamente."
  - Sistema registra erro no log
  - Transação é revertida (rollback)

### Regras de Negócio
- **RN-UC03-001:** Id_Usuario_Alteracao preenchido automaticamente com ID do usuário autenticado
- **RN-UC03-002:** Dt_Alteracao preenchido automaticamente com timestamp UTC
- **RN-UC03-003:** Alterações NÃO são retroativas (aplicações existentes mantêm configuração original)
- **RN-UC03-004:** Políticas em estado "Inativa" ou "Cancelada" NÃO podem ser editadas
- **RN-UC03-005:** Transições de estado devem respeitar tabela de transições do RF049
- **RN-UC03-006:** Apenas campos alterados devem ser validados
- **RN-UC03-007:** Auditoria DEVE registrar diff (estado anterior vs novo estado)

### Critérios de Aceite
- **CA-UC03-001:** Id_Usuario_Alteracao DEVE ser preenchido automaticamente
- **CA-UC03-002:** Dt_Alteracao DEVE ser preenchido automaticamente
- **CA-UC03-003:** Sistema DEVE detectar conflitos de edição concorrente
- **CA-UC03-004:** Tentativa de editar política de outro tenant DEVE retornar 404
- **CA-UC03-005:** Auditoria DEVE registrar estado anterior e novo estado (diff JSON)
- **CA-UC03-006:** Alterações NÃO devem afetar aplicações já existentes
- **CA-UC03-007:** Sistema DEVE validar transições de estado

---

## UC04 — Excluir Política de Consumidor

### Objetivo
Permitir exclusão lógica de uma política, mantendo histórico para conformidade.

### Pré-condições
- Usuário autenticado
- Permissão `GESTAO.POLITICAS.DELETE`
- Política existe e pertence ao tenant do usuário
- Política NÃO está aplicada a nenhum consumidor ativo

### Pós-condições
- Política marcada como excluída (Fl_Excluido=true)
- Auditoria registrada (DELETE)
- Política NÃO aparece mais em listagens padrão
- Histórico mantido para conformidade

### Fluxo Principal
- **FP-UC04-001:** Usuário seleciona política na lista (UC00) e clica em "Excluir"
- **FP-UC04-002:** Sistema valida permissão GESTAO.POLITICAS.DELETE
- **FP-UC04-003:** Sistema verifica se política está aplicada a consumidores ativos
- **FP-UC04-004:** Sistema exibe modal de confirmação: "Tem certeza que deseja excluir a política [Nome]? Esta ação não pode ser desfeita."
- **FP-UC04-005:** Usuário confirma exclusão
- **FP-UC04-006:** Sistema executa soft delete (Fl_Excluido=true)
- **FP-UC04-007:** Sistema preenche Dt_Exclusao e Id_Usuario_Exclusao
- **FP-UC04-008:** Sistema registra evento de auditoria (POLITICA_DELETED)
- **FP-UC04-009:** Sistema exibe mensagem: "Política excluída com sucesso."
- **FP-UC04-010:** Sistema atualiza lista (UC00) removendo o item excluído

### Fluxos Alternativos
- **FA-UC04-001:** Usuário cancela exclusão no modal de confirmação
  - Sistema fecha modal sem executar exclusão
  - Sistema mantém usuário na tela atual

### Fluxos de Exceção
- **FE-UC04-001:** Política está aplicada a consumidores ativos
  - Sistema exibe mensagem: "Não é possível excluir esta política pois está aplicada a [N] consumidores. Remova as aplicações primeiro."
  - Sistema não permite exclusão
  - Sistema oferece botão "Visualizar Consumidores" que redireciona para aba Consumidores Vinculados (UC02)
- **FE-UC04-002:** Política já foi excluída anteriormente
  - Sistema exibe mensagem: "Esta política já foi excluída."
  - Sistema atualiza lista (UC00)
- **FE-UC04-003:** Erro ao executar soft delete
  - Sistema exibe mensagem: "Erro ao excluir política. Tente novamente."
  - Sistema registra erro no log
  - Transação é revertida (rollback)

### Regras de Negócio
- **RN-UC04-001:** Exclusão SEMPRE é lógica (soft delete) via Fl_Excluido=true
- **RN-UC04-002:** Políticas com consumidores ativos vinculados NÃO podem ser excluídas
- **RN-UC04-003:** Sistema DEVE exigir confirmação explícita do usuário
- **RN-UC04-004:** Dt_Exclusao e Id_Usuario_Exclusao devem ser preenchidos
- **RN-UC04-005:** Histórico de aplicações e violações deve ser mantido (7 anos LGPD)
- **RN-UC04-006:** Política excluída NÃO aparece em listagens padrão (UC00)
- **RN-UC04-007:** Política excluída ainda é visível em histórico de aplicações (UC12)

### Critérios de Aceite
- **CA-UC04-001:** Exclusão DEVE ser sempre lógica (soft delete)
- **CA-UC04-002:** Sistema DEVE verificar dependências ANTES de permitir exclusão
- **CA-UC04-003:** Sistema DEVE exigir confirmação explícita do usuário
- **CA-UC04-004:** Fl_Excluido, Dt_Exclusao e Id_Usuario_Exclusao DEVEM ser preenchidos
- **CA-UC04-005:** Tentativa de excluir política com dependências DEVE retornar erro claro
- **CA-UC04-006:** Política excluída NÃO deve aparecer em listagens padrão
- **CA-UC04-007:** Histórico de aplicações DEVE ser mantido mesmo após exclusão

---

## UC05 — Aplicar Política a Consumidores

### Objetivo
Vincular uma política a um ou mais consumidores, com vigência definida e aplicação automática por perfil/status.

### Pré-condições
- Usuário autenticado
- Permissão `GESTAO.POLITICAS.APPLY`
- Política existe, está ativa e pertence ao tenant
- Consumidor(es) existem e pertencem ao tenant

### Pós-condições
- Política aplicada ao(s) consumidor(es)
- Registro criado em PoliticaConsumidorAplicacao
- Histórico imutável criado em PoliticaConsumidorHistorico
- Auditoria registrada (POLITICA_APPLIED)

### Fluxo Principal
- **FP-UC05-001:** Usuário acessa UC02 e clica em "Aplicar Política"
- **FP-UC05-002:** Sistema valida permissão GESTAO.POLITICAS.APPLY
- **FP-UC05-003:** Sistema valida que política está no status "Ativa"
- **FP-UC05-004:** Sistema exibe modal de aplicação com formulário
- **FP-UC05-005:** Usuário seleciona consumidor(es) via dropdown ou busca
- **FP-UC05-006:** Usuário informa Data Início* (padrão: data atual)
- **FP-UC05-007:** Usuário informa Data Fim (opcional)
- **FP-UC05-008:** Usuário informa Motivo (opcional, recomendado para auditoria)
- **FP-UC05-009:** Sistema valida que Dt_Fim >= Dt_Inicio (se preenchida)
- **FP-UC05-010:** Usuário clica em "Aplicar"
- **FP-UC05-011:** Sistema cria registro(s) em PoliticaConsumidorAplicacao
- **FP-UC05-012:** Sistema cria registro(s) IMUTÁVEL em PoliticaConsumidorHistorico (tipo: APLICACAO)
- **FP-UC05-013:** Sistema registra evento de auditoria (POLITICA_APPLIED)
- **FP-UC05-014:** Sistema exibe mensagem: "Política aplicada com sucesso a [N] consumidor(es)."
- **FP-UC05-015:** Sistema atualiza aba Consumidores Vinculados (UC02)

### Fluxos Alternativos
- **FA-UC05-001 (RN-RF049-02):** Sistema aplica política automaticamente por perfil
  - Evento: ConsumidorCreated ou ConsumidorProfileChanged
  - Sistema identifica perfil do consumidor (Executivo, Gerente, Colaborador, Estagiário, Externo)
  - Sistema busca políticas configuradas para o perfil
  - Sistema aplica políticas automaticamente via Domain Event Handler
  - Sistema cria histórico com Motivo: "Aplicação automática por perfil [nome_perfil]"
- **FA-UC05-002 (RN-RF049-03):** Sistema aplica política automaticamente por status
  - Evento: ConsumidorStatusChanged
  - Sistema identifica novo status (Ativo, Suspenso, Bloqueado, Inativo, Pendente)
  - Sistema busca políticas configuradas para o status
  - Sistema aplica políticas de status (sobrescrevem políticas de perfil)
  - Sistema cria histórico com Motivo: "Aplicação automática por mudança de status para [status]"
- **FA-UC05-003:** Usuário cancela aplicação
  - Sistema fecha modal sem aplicar política
  - Sistema mantém usuário em UC02

### Fluxos de Exceção
- **FE-UC05-001:** Política não está no status "Ativa"
  - Sistema exibe mensagem: "Apenas políticas ativas podem ser aplicadas."
  - Sistema não permite aplicação
- **FE-UC05-002:** Consumidor já possui a política aplicada (aplicação duplicada)
  - Sistema exibe aviso: "Consumidor [Nome] já possui esta política aplicada. Deseja substituir a vigência?"
  - Se usuário confirmar: remove aplicação antiga e cria nova
  - Se usuário cancelar: não aplica ao consumidor duplicado, continua com os demais
- **FE-UC05-003:** Data Fim anterior a Data Início
  - Sistema exibe erro no campo: "Data Fim deve ser maior ou igual a Data Início."
  - Sistema não permite salvar
- **FE-UC05-004:** Erro ao criar aplicação
  - Sistema exibe mensagem: "Erro ao aplicar política. Tente novamente."
  - Sistema registra erro no log
  - Transação é revertida (rollback)

### Regras de Negócio
- **RN-UC05-001:** Apenas políticas no status "Ativa" podem ser aplicadas
- **RN-UC05-002:** Dt_Fim deve ser >= Dt_Inicio (se preenchida)
- **RN-UC05-003 (RN-RF049-02):** Políticas aplicadas por perfil são automáticas via Domain Events
- **RN-UC05-004 (RN-RF049-03):** Políticas de status sobrescrevem políticas de perfil em caso de conflito
- **RN-UC05-005 (RN-RF049-07):** Registro IMUTÁVEL em PoliticaConsumidorHistorico é obrigatório
- **RN-UC05-006:** Histórico retido por 7 anos (LGPD)
- **RN-UC05-007:** Consumidor pode ter políticas customizadas que sobrescrevem políticas de perfil
- **RN-UC05-008:** Id_Fornecedor da política e do consumidor devem coincidir (isolamento multi-tenant)

### Critérios de Aceite
- **CA-UC05-001:** Sistema DEVE validar que política está ativa antes de aplicar
- **CA-UC05-002:** Sistema DEVE validar Dt_Fim >= Dt_Inicio
- **CA-UC05-003:** Sistema DEVE criar registro IMUTÁVEL em PoliticaConsumidorHistorico
- **CA-UC05-004:** Sistema DEVE aplicar políticas automaticamente por perfil via Domain Events
- **CA-UC05-005:** Sistema DEVE aplicar políticas automaticamente por status via Domain Events
- **CA-UC05-006:** Histórico DEVE ser retido por 7 anos
- **CA-UC05-007:** Sistema DEVE validar isolamento multi-tenant (política e consumidor do mesmo tenant)

---

## UC06 — Remover Política de Consumidores

### Objetivo
Remover vínculo de política de um ou mais consumidores, mantendo histórico para auditoria.

### Pré-condições
- Usuário autenticado
- Permissão `GESTAO.POLITICAS.APPLY`
- Política aplicada ao(s) consumidor(es)

### Pós-condições
- Registro removido de PoliticaConsumidorAplicacao (ou marcado com Dt_Fim)
- Histórico imutável criado em PoliticaConsumidorHistorico (tipo: REMOCAO)
- Auditoria registrada (POLITICA_REMOVED)

### Fluxo Principal
- **FP-UC06-001:** Usuário acessa UC02, aba Consumidores Vinculados
- **FP-UC06-002:** Usuário seleciona consumidor(es) e clica em "Remover Política"
- **FP-UC06-003:** Sistema valida permissão GESTAO.POLITICAS.APPLY
- **FP-UC06-004:** Sistema exibe modal de confirmação: "Deseja remover a política [Nome] de [N] consumidor(es)?"
- **FP-UC06-005:** Sistema solicita informar Motivo (opcional, recomendado)
- **FP-UC06-006:** Usuário confirma remoção
- **FP-UC06-007:** Sistema marca aplicação como removida (Dt_Fim = data atual) OU remove registro fisicamente
- **FP-UC06-008:** Sistema cria registro IMUTÁVEL em PoliticaConsumidorHistorico (tipo: REMOCAO)
- **FP-UC06-009:** Sistema registra evento de auditoria (POLITICA_REMOVED)
- **FP-UC06-010:** Sistema exibe mensagem: "Política removida com sucesso de [N] consumidor(es)."
- **FP-UC06-011:** Sistema atualiza aba Consumidores Vinculados

### Fluxos Alternativos
- **FA-UC06-001:** Usuário cancela remoção no modal de confirmação
  - Sistema fecha modal sem remover política
  - Sistema mantém usuário em UC02

### Fluxos de Exceção
- **FE-UC06-001:** Política não está aplicada ao consumidor selecionado
  - Sistema exibe mensagem: "Política não está aplicada ao consumidor [Nome]."
  - Sistema não permite remoção
- **FE-UC06-002:** Erro ao remover aplicação
  - Sistema exibe mensagem: "Erro ao remover política. Tente novamente."
  - Sistema registra erro no log
  - Transação é revertida (rollback)

### Regras de Negócio
- **RN-UC06-001 (RN-RF049-07):** Registro IMUTÁVEL em PoliticaConsumidorHistorico é obrigatório
- **RN-UC06-002:** Histórico retido por 7 anos (LGPD)
- **RN-UC06-003:** Remoção pode ser física (DELETE) ou lógica (Dt_Fim = data atual)
- **RN-UC06-004:** Motivo da remoção é opcional mas recomendado para auditoria

### Critérios de Aceite
- **CA-UC06-001:** Sistema DEVE criar registro IMUTÁVEL em PoliticaConsumidorHistorico (tipo: REMOCAO)
- **CA-UC06-002:** Sistema DEVE registrar auditoria POLITICA_REMOVED
- **CA-UC06-003:** Histórico DEVE ser retido por 7 anos
- **CA-UC06-004:** Sistema DEVE solicitar confirmação explícita

---

## UC07 — Processamento em Lote de Aplicação

### Objetivo
Aplicar ou remover políticas de múltiplos consumidores simultaneamente de forma assíncrona.

### Pré-condições
- Usuário autenticado
- Permissão `GESTAO.POLITICAS.APPLY`
- Política existe e está ativa
- Lista de consumidores (máximo 1000 por lote)

### Pós-condições
- Job assíncrono criado no Hangfire
- Políticas aplicadas/removidas para todos os consumidores
- Relatório consolidado de sucesso/falha gerado
- Auditoria registrada (BATCH_APPLY ou BATCH_REMOVE)

### Fluxo Principal
- **FP-UC07-001:** Usuário acessa UC00 e seleciona política
- **FP-UC07-002:** Usuário clica em "Aplicar em Lote"
- **FP-UC07-003:** Sistema valida permissão GESTAO.POLITICAS.APPLY
- **FP-UC07-004:** Sistema exibe modal de aplicação em lote
- **FP-UC07-005:** Usuário seleciona critérios de filtro (Departamento, Cargo, Filial, Perfil, Status)
- **FP-UC07-006:** Sistema exibe preview: "[N] consumidores serão afetados. Máximo: 1000."
- **FP-UC07-007:** Usuário informa Data Início, Data Fim (opcional), Motivo (opcional)
- **FP-UC07-008:** Usuário clica em "Confirmar Aplicação em Lote"
- **FP-UC07-009:** Sistema valida que N ≤ 1000 consumidores
- **FP-UC07-010:** Sistema cria job assíncrono no Hangfire
- **FP-UC07-011:** Sistema exibe mensagem: "Processamento iniciado. Você receberá notificação ao concluir. ID do Job: [GUID]."
- **FP-UC07-012:** **[Background]** Hangfire processa consumidores em lotes de 100
- **FP-UC07-013:** **[Background]** Para cada consumidor: valida se política é aplicável, aplica política, cria histórico, registra sucesso/falha
- **FP-UC07-014:** **[Background]** Ao finalizar: gera relatório consolidado (Sucesso: N, Falha: M, Detalhes de Erros)
- **FP-UC07-015:** **[Background]** Sistema envia notificação ao usuário (e-mail + in-app) com link para relatório
- **FP-UC07-016:** Usuário acessa relatório e visualiza resultado detalhado

### Fluxos Alternativos
- **FA-UC07-001 (RN-RF049-06):** Lote com mais de 1000 consumidores
  - Sistema divide automaticamente em múltiplos jobs
  - Sistema exibe mensagem: "Serão criados [K] jobs de até 1000 consumidores cada."
  - Usuário pode confirmar ou cancelar
- **FA-UC07-002:** Usuário cancela processamento em lote
  - Sistema fecha modal sem criar job
- **FA-UC07-003:** Rollback em caso de falha crítica
  - Se ≥ 50% dos consumidores falham: sistema reverte TODAS as aplicações do lote
  - Sistema envia notificação de falha crítica
  - Sistema registra erro detalhado no log

### Fluxos de Exceção
- **FE-UC07-001:** Filtro resulta em mais de 1000 consumidores e usuário não aceita divisão
  - Sistema exibe mensagem: "Refine os filtros para reduzir o número de consumidores."
  - Sistema não cria job
- **FE-UC07-002:** Erro ao criar job no Hangfire
  - Sistema exibe mensagem: "Erro ao iniciar processamento. Tente novamente."
  - Sistema registra erro no log
- **FE-UC07-003:** Falhas individuais durante processamento
  - Sistema continua processando demais consumidores
  - Sistema registra falhas no relatório
  - Sistema NÃO reverte se falhas < 50%

### Regras de Negócio
- **RN-UC07-001 (RN-RF049-06):** Limite máximo de 1000 consumidores por lote
- **RN-UC07-002 (RN-RF049-06):** Processamento assíncrono via Hangfire
- **RN-UC07-003 (RN-RF049-06):** Geração obrigatória de relatório consolidado de sucesso/falha
- **RN-UC07-004 (RN-RF049-06):** Rollback automático se ≥50% de falhas críticas
- **RN-UC07-005:** Lotes > 1000 consumidores são divididos automaticamente
- **RN-UC07-006:** Validação individual de cada consumidor (política aplicável, tenant, etc.)
- **RN-UC07-007:** Notificação ao usuário ao concluir (e-mail + in-app)

### Critérios de Aceite
- **CA-UC07-001:** Sistema DEVE validar limite máximo de 1000 consumidores
- **CA-UC07-002:** Sistema DEVE processar de forma assíncrona via Hangfire
- **CA-UC07-003:** Sistema DEVE gerar relatório consolidado de sucesso/falha
- **CA-UC07-004:** Sistema DEVE permitir rollback em caso de falha crítica (≥50% falhas)
- **CA-UC07-005:** Sistema DEVE dividir automaticamente lotes >1000
- **CA-UC07-006:** Sistema DEVE validar se política é aplicável a cada consumidor
- **CA-UC07-007:** Sistema DEVE enviar notificação ao concluir

---

## UC08 — Avaliar Violação em Tempo Real

### Objetivo
Fornecer API para verificar se uma operação viola políticas aplicadas ao consumidor ANTES de executá-la.

### Pré-condições
- Sistema chamador autenticado (API key ou JWT)
- Consumidor existe e possui políticas aplicadas
- Motor de políticas disponível

### Pós-condições
- Resposta em ≤100ms (P95)
- Decisão: Permitido (true/false)
- Detalhes: Políticas aplicáveis, Limite, Consumo atual, Percentual usado

### Fluxo Principal
- **FP-UC08-001:** Sistema externo/interno faz `POST /api/gestao/politicas-consumidores/avaliar`
- **FP-UC08-002:** Request body contém: Id_Consumidor*, Tipo_Operacao* (Voz/Dados/SMS/Roaming), Valor* (R$ ou quantidade), Destino (opcional), Horario (opcional)
- **FP-UC08-003:** Sistema valida autenticação (JWT/API key)
- **FP-UC08-004:** Sistema carrega políticas ativas aplicadas ao consumidor (cache de 5 minutos)
- **FP-UC08-005:** Motor de políticas avalia regras em memória
- **FP-UC08-006:** Sistema calcula: Limite_Maximo, Consumo_Atual, Valor_Apos_Operacao, Percentual_Usado
- **FP-UC08-007:** Sistema verifica se Valor_Apos_Operacao > Limite_Maximo
- **FP-UC08-008:** Sistema retorna JSON: `{ "permitido": true/false, "politicas_aplicaveis": [...], "limite_maximo": 500.00, "consumo_atual": 320.00, "percentual_usado": 64.0, "margem_disponivel": 180.00 }`
- **FP-UC08-009:** Tempo de resposta ≤ 100ms (P95)

### Fluxos Alternativos
- **FA-UC08-001 (RN-RF049-04):** Consumo atinge limiar de alerta (50%, 80%, 100%)
  - Sistema dispara evento AlertThresholdReached
  - RF066/RF067 enviam notificações (e-mail, SMS, in-app)
  - Sistema registra alerta (evita duplicação)
- **FA-UC08-002:** Consumidor sem políticas aplicadas
  - Sistema retorna: `{ "permitido": true, "politicas_aplicaveis": [], "motivo": "Nenhuma política aplicada" }`
- **FA-UC08-003 (RN-RF049-09):** Fail-open em caso de falha do motor
  - Se motor de políticas indisponível: retorna `{ "permitido": true, "motivo": "Fail-open: motor indisponível" }`
  - Sistema registra alerta de falha do motor
  - Disponibilidade > segurança (evita bloqueio total do sistema)

### Fluxos de Exceção
- **FE-UC08-001:** Request inválido (campos obrigatórios faltando)
  - Sistema retorna HTTP 400 Bad Request
  - Body: `{ "erro": "Campo obrigatório faltando: [campo]" }`
- **FE-UC08-002:** Consumidor não encontrado
  - Sistema retorna HTTP 404 Not Found
  - Body: `{ "erro": "Consumidor não encontrado" }`
- **FE-UC08-003:** Tempo de resposta > 100ms (P95)
  - Sistema registra alerta de performance
  - Sistema analisa cache e otimiza queries

### Regras de Negócio
- **RN-UC08-001 (RN-RF049-09):** Tempo de resposta ≤ 100ms (P95) obrigatório
- **RN-UC08-002 (RN-RF049-09):** Motor de políticas avalia regras em memória (cache)
- **RN-UC08-003 (RN-RF049-09):** Fail-open: Em caso de falha do motor, permitir operação (log de alerta)
- **RN-UC08-004:** Cache de políticas ativas em memória por 5 minutos
- **RN-UC08-005:** Endpoint autenticado via JWT ou API key
- **RN-UC08-006:** Isolamento multi-tenant obrigatório

### Critérios de Aceite
- **CA-UC08-001:** Endpoint DEVE responder em ≤100ms (P95)
- **CA-UC08-002:** Sistema DEVE retornar: permitido (true/false), políticas aplicáveis, limite, consumo, percentual
- **CA-UC08-003:** Motor DEVE avaliar regras em memória (cache)
- **CA-UC08-004:** Em caso de falha, política padrão DEVE ser "permitir" (fail-open)
- **CA-UC08-005:** Sistema DEVE disparar alertas em limiares (50%, 80%, 100%)
- **CA-UC08-006:** Cache DEVE ser de 5 minutos para políticas ativas

---

## UC09 — Simular Impacto de Política

### Objetivo
Permitir simular o impacto de uma política antes de aplicá-la em produção, analisando histórico de consumo.

### Pré-condições
- Usuário autenticado
- Permissão `GESTAO.POLITICAS.VIEW`
- Política criada (pode estar em Rascunho)
- Histórico de consumo disponível (mínimo 1 mês)

### Pós-condições
- Relatório de simulação gerado
- Nenhuma mudança aplicada no banco de dados (simulação read-only)

### Fluxo Principal
- **FP-UC09-001:** Usuário acessa UC02 e clica em "Simular Impacto"
- **FP-UC09-002:** Sistema valida permissão GESTAO.POLITICAS.VIEW
- **FP-UC09-003:** Sistema exibe modal de simulação
- **FP-UC09-004:** Usuário seleciona critérios de filtro (Departamento, Cargo, Filial, Perfil)
- **FP-UC09-005:** Sistema exibe preview: "[N] consumidores serão analisados."
- **FP-UC09-006:** Usuário seleciona período de análise (padrão: últimos 3 meses)
- **FP-UC09-007:** Usuário clica em "Simular"
- **FP-UC09-008:** Sistema analisa consumo histórico dos consumidores afetados
- **FP-UC09-009:** Sistema calcula: Quantos seriam bloqueados?, Quando seriam bloqueados? (data estimada), Estimativa de economia (consumo médio antes vs limite da política)
- **FP-UC09-010:** Sistema gera relatório visual com gráficos (ApexCharts):
  - Gráfico de barras: Consumidores por status (Conforme, Aviso, Crítico, Violação)
  - Timeline: Quando cada consumidor violaria a política
  - Gráfico de economia: Estimativa de economia mensal (R$)
  - Top 10 consumidores mais impactados
- **FP-UC09-011:** Sistema exibe relatório em ≤5 segundos
- **FP-UC09-012:** Usuário pode exportar relatório (PDF)

### Fluxos Alternativos
- **FA-UC09-001:** Usuário ajusta parâmetros da simulação
  - Usuário altera período de análise, filtros ou limites da política
  - Sistema recalcula simulação com novos parâmetros
- **FA-UC09-002:** Usuário aplica política após analisar simulação
  - Usuário clica em "Aplicar Política" no modal de simulação
  - Sistema redireciona para UC05 com filtros pré-selecionados

### Fluxos de Exceção
- **FE-UC09-001:** Consumidores sem histórico de consumo
  - Sistema exibe aviso: "[M] consumidores não possuem histórico suficiente e foram excluídos da simulação."
  - Sistema continua simulação apenas com consumidores com histórico
- **FE-UC09-002:** Período de análise sem dados
  - Sistema exibe mensagem: "Não há dados de consumo no período selecionado."
  - Sistema não gera relatório
- **FE-UC09-003:** Erro ao gerar relatório
  - Sistema exibe mensagem: "Erro ao gerar simulação. Tente novamente."
  - Sistema registra erro no log

### Regras de Negócio
- **RN-UC09-001 (RN-RF049-10):** Simulador analisa consumo histórico real dos consumidores
- **RN-UC09-002 (RN-RF049-10):** Simulador NÃO aplica mudanças (read-only)
- **RN-UC09-003 (RN-RF049-10):** Simulador retorna: Quantos seriam bloqueados, Quando, Estimativa de economia
- **RN-UC09-004 (RN-RF049-10):** Simulador não funciona para consumidores novos sem histórico
- **RN-UC09-005:** Período mínimo de análise: 1 mês
- **RN-UC09-006:** Período recomendado de análise: 3 meses
- **RN-UC09-007:** Tempo de resposta ≤5 segundos

### Critérios de Aceite
- **CA-UC09-001:** Simulador DEVE analisar consumo histórico real
- **CA-UC09-002:** Simulador NÃO deve aplicar mudanças (read-only)
- **CA-UC09-003:** Relatório DEVE incluir: quantos bloqueados, quando, economia estimada
- **CA-UC09-004:** Sistema DEVE excluir consumidores sem histórico suficiente
- **CA-UC09-005:** Relatório DEVE ser gerado em ≤5 segundos
- **CA-UC09-006:** Usuário DEVE poder exportar relatório (PDF)

---

## UC10 — Gerenciar Alertas Proativos

### Objetivo
Monitorar consumo em tempo real e disparar alertas proativos em múltiplos limiares (50%, 80%, 100%).

### Pré-condições
- Consumidor com política aplicada
- Política configurada com limiares de alerta
- Motor de políticas monitorando consumo em tempo real

### Pós-condições
- Alertas disparados nos limiares configurados
- Notificações enviadas aos destinatários (Consumidor, Gestor, Financeiro)
- Histórico de alertas registrado
- Alertas não duplicados (apenas 1 alerta por limiar por período)

### Fluxo Principal
- **FP-UC10-001:** **[Background]** Motor de políticas monitora consumo em tempo real (via eventos de faturamento)
- **FP-UC10-002:** **[Background]** Sistema calcula percentual de consumo do limite para cada consumidor com política ativa
- **FP-UC10-003:** **[Background]** Sistema detecta que consumidor atingiu limiar (50%, 80% ou 100%)
- **FP-UC10-004:** **[Background]** Sistema verifica se já foi enviado alerta para este limiar no período atual
- **FP-UC10-005:** **[Background]** Se alerta NÃO foi enviado: Sistema dispara evento AlertThresholdReached
- **FP-UC10-006:** **[Background]** RF066/RF067 enviam notificações:
  - 50%: E-mail informativo + notificação in-app
  - 80%: E-mail crítico + notificação in-app + SMS (se configurado)
  - 100%: E-mail urgente + notificação in-app + SMS (obrigatório)
- **FP-UC10-007:** **[Background]** Sistema registra alerta enviado (evita duplicação)
- **FP-UC10-008:** **[Background]** Sistema atualiza status do consumidor no dashboard (Verde → Amarelo → Laranja → Vermelho)
- **FP-UC10-009:** Gestor visualiza alertas pendentes no dashboard (UC13)
- **FP-UC10-010:** Consumidor recebe notificação e pode visualizar consumo atual

### Fluxos Alternativos
- **FA-UC10-001 (RN-RF049-04):** Política com alertas desabilitados (ex: ambiente de teste)
  - Sistema NÃO dispara alertas
  - Sistema apenas registra violação no histórico
- **FA-UC10-002:** Gestor configura destinatários personalizados de alertas
  - Gestor acessa configurações da política
  - Gestor adiciona/remove destinatários de notificações
  - Sistema salva configuração

### Fluxos de Exceção
- **FE-UC10-001:** Falha ao enviar e-mail/SMS
  - Sistema tenta reenvio (máximo 3 tentativas)
  - Se falhar: registra erro no log
  - Sistema garante que notificação in-app seja enviada (fallback)
- **FE-UC10-002:** Destinatário sem e-mail/telefone cadastrado
  - Sistema exibe alerta: "Consumidor [Nome] sem e-mail cadastrado. Notificação in-app enviada."
  - Sistema registra inconsistência

### Regras de Negócio
- **RN-UC10-001 (RN-RF049-04):** Alertas em: 50% (informativo), 80% (crítico), 100% (bloqueio iminente)
- **RN-UC10-002 (RN-RF049-04):** Canais: E-mail, SMS (crítico), Notificação in-app
- **RN-UC10-003 (RN-RF049-04):** Destinatários: Consumidor, Gestor responsável, Financeiro
- **RN-UC10-004 (RN-RF049-04):** Alertas NÃO devem duplicar (apenas 1 por limiar por período)
- **RN-UC10-005 (RN-RF049-04):** Sistema monitora consumo em tempo real e dispara alertas via RF066/RF067
- **RN-UC10-006 (RN-RF049-04):** Alertas podem ser desabilitados por política (flag AlertOnly=false)
- **RN-UC10-007:** Período de não duplicação: 24 horas por limiar

### Critérios de Aceite
- **CA-UC10-001:** Sistema DEVE alertar ANTES de atingir limite (50%, 80%, 100%)
- **CA-UC10-002:** Alertas DEVEM ser enviados por múltiplos canais (e-mail, SMS, in-app)
- **CA-UC10-003:** Alertas NÃO devem duplicar (máximo 1 por limiar por 24h)
- **CA-UC10-004:** Sistema DEVE monitorar consumo em tempo real (eventos de faturamento)
- **CA-UC10-005:** Políticas com AlertOnly DEVEM ser respeitadas (não bloquear)

---

## UC11 — Executar Bloqueios Automáticos

### Objetivo
Bloquear automaticamente consumidores que atingem 100% do limite definido em política, garantindo conformidade.

### Pré-condições
- Consumidor com política aplicada
- Consumo atingiu 100% do limite
- Política configurada para bloquear (AlertOnly=false)

### Pós-condições
- Consumidor bloqueado (integração com RF048)
- Violação registrada em ViolacaoPolitica
- Notificações enviadas aos stakeholders
- Solicitação de análise criada para Gestor

### Fluxo Principal
- **FP-UC11-001:** **[Background]** Sistema detecta que consumidor atingiu 100% do limite (via UC08)
- **FP-UC11-002:** **[Background]** Sistema verifica se política está configurada para bloquear (AlertOnly=false)
- **FP-UC11-003:** **[Background]** Sistema identifica tipo de bloqueio (Total ou Parcial)
- **FP-UC11-004:** **[Background]** Sistema dispara evento PolicyViolated
- **FP-UC11-005:** **[Background]** RF048 executa bloqueio:
  - Bloqueio Total: Bloqueia todos os serviços do consumidor
  - Bloqueio Parcial: Bloqueia apenas serviço que violou (mantém outros ativos)
- **FP-UC11-006:** **[Background]** Sistema registra violação em ViolacaoPolitica (Data, Consumidor, Política, Valor Limite, Valor Consumido, Ação Tomada)
- **FP-UC11-007:** **[Background]** Sistema envia notificações:
  - Consumidor: E-mail + SMS + In-app (urgente)
  - Gestor: E-mail + In-app com solicitação de análise
  - Financeiro: E-mail informativo
- **FP-UC11-008:** **[Background]** Sistema cria solicitação de análise para Gestor (ticket/workflow)
- **FP-UC11-009:** **[Background]** Sistema atualiza dashboard (status: Violação)
- **FP-UC11-010:** Gestor visualiza solicitação de análise no dashboard (UC13)
- **FP-UC11-011:** Gestor analisa violação e decide: Liberar (com justificativa), Manter bloqueio, Ajustar limite da política
- **FP-UC11-012:** Se liberado: Sistema desbloqueia consumidor (RF048), Registra liberação em ViolacaoPolitica (Id_Usuario_Liberacao, Dt_Liberacao, Justificativa)

### Fluxos Alternativos
- **FA-UC11-001 (RN-RF049-05):** Política com flag AlertOnly=true
  - Sistema NÃO executa bloqueio
  - Sistema apenas registra violação e envia alertas
- **FA-UC11-002:** Bloqueio Parcial (apenas serviço violado)
  - Exemplo: Política de Franquia de Dados violada
  - Sistema bloqueia apenas DADOS
  - Sistema mantém VOZ e SMS funcionando
- **FA-UC11-003:** Gestor libera consumidor temporariamente
  - Gestor informa Data/Hora limite para liberação
  - Sistema agenda reativação automática do bloqueio
  - Sistema envia lembrete 1 hora antes da reativação

### Fluxos de Exceção
- **FE-UC11-001:** Erro ao executar bloqueio no RF048
  - Sistema tenta reenvio (máximo 3 tentativas)
  - Se falhar: registra erro crítico no log
  - Sistema envia alerta para equipe técnica
  - Sistema NÃO registra violação até bloqueio ser confirmado
- **FE-UC11-002:** Conflito de políticas (múltiplas políticas aplicadas)
  - Sistema aplica política mais restritiva
  - Sistema registra conflito no log

### Regras de Negócio
- **RN-UC11-001 (RN-RF049-05):** Ao atingir 100%: Bloqueia novas operações, Notifica stakeholders, Registra violação, Cria solicitação de análise
- **RN-UC11-002 (RN-RF049-05):** Bloqueio Total (todos os serviços) ou Parcial (apenas serviço violado)
- **RN-UC11-003 (RN-RF049-05):** Motor de políticas avalia violação e dispara bloqueio via RF048
- **RN-UC11-004 (RN-RF049-05):** Políticas com flag AlertOnly apenas alertam sem bloquear
- **RN-UC11-005 (RN-RF049-05):** Bloqueio seletivo: mantém outros serviços funcionando
- **RN-UC11-006:** Violação registrada com: Data/Hora, Consumidor, Política, Valor Limite, Valor Consumido, Ação Tomada
- **RN-UC11-007:** Gestor pode liberar com justificativa obrigatória
- **RN-UC11-008:** Liberação registra: Id_Usuario_Liberacao, Dt_Liberacao, Justificativa

### Critérios de Aceite
- **CA-UC11-001:** Sistema DEVE bloquear automaticamente ao atingir 100%
- **CA-UC11-002:** Sistema DEVE registrar violação em ViolacaoPolitica
- **CA-UC11-003:** Sistema DEVE notificar Consumidor, Gestor e Financeiro
- **CA-UC11-004:** Sistema DEVE criar solicitação de análise para Gestor
- **CA-UC11-005:** Bloqueio DEVE ser Total ou Parcial conforme configuração
- **CA-UC11-006:** Políticas AlertOnly DEVEM apenas alertar sem bloquear
- **CA-UC11-007:** Gestor DEVE poder liberar com justificativa obrigatória

---

## UC12 — Visualizar Histórico de Aplicações

### Objetivo
Permitir consulta ao histórico imutável de aplicações/remoções de políticas, com retenção de 7 anos (LGPD).

### Pré-condições
- Usuário autenticado
- Permissão `GESTAO.POLITICAS.VIEW`
- Registros existem em PoliticaConsumidorHistorico

### Pós-condições
- Histórico exibido com filtros e paginação
- Dados retidos por 7 anos
- Registros imutáveis (não podem ser alterados)

### Fluxo Principal
- **FP-UC12-001:** Usuário acessa UC02, aba "Histórico de Aplicações"
- **FP-UC12-002:** Sistema valida permissão GESTAO.POLITICAS.VIEW
- **FP-UC12-003:** Sistema carrega histórico de PoliticaConsumidorHistorico filtrado por Id_Politica
- **FP-UC12-004:** Sistema exibe lista com colunas: Data/Hora, Tipo (Aplicação/Remoção), Consumidor, Usuário Responsável, Motivo, Vigência (Dt_Inicio - Dt_Fim)
- **FP-UC12-005:** Sistema aplica paginação (20 registros por página)
- **FP-UC12-006:** Sistema ordena por Data/Hora DESC (mais recentes primeiro)

### Fluxos Alternativos
- **FA-UC12-001:** Usuário filtra histórico por período
  - Sistema recarrega lista filtrada por intervalo de datas
- **FA-UC12-002:** Usuário filtra histórico por tipo (Aplicação/Remoção)
  - Sistema recarrega lista filtrada por tipo
- **FA-UC12-003:** Usuário filtra histórico por consumidor
  - Sistema recarrega lista filtrada por consumidor específico
- **FA-UC12-004:** Usuário exporta histórico (CSV/Excel)
  - Sistema gera arquivo com todos os registros filtrados
  - Sistema oferece download

### Fluxos de Exceção
- **FE-UC12-001:** Nenhum registro encontrado
  - Sistema exibe estado vazio: "Nenhum registro de histórico encontrado."
- **FE-UC12-002:** Erro ao carregar histórico
  - Sistema exibe mensagem: "Erro ao carregar histórico. Tente novamente."
  - Sistema registra erro no log

### Regras de Negócio
- **RN-UC12-001 (RN-RF049-07):** Registra: Data/Hora, Usuário Responsável, Consumidor Afetado, Política Aplicada/Removida, Motivo, Vigência (Dt_Inicio/Dt_Fim)
- **RN-UC12-002 (RN-RF049-07):** Retenção de 7 anos conforme LGPD
- **RN-UC12-003 (RN-RF049-07):** Dados NÃO podem ser alterados, apenas visualizados (tabela imutável)
- **RN-UC12-004:** Histórico isolado por tenant (Id_Fornecedor)
- **RN-UC12-005:** Paginação padrão de 20 registros
- **RN-UC12-006:** Ordenação padrão: Data/Hora DESC

### Critérios de Aceite
- **CA-UC12-001:** Sistema DEVE exibir registros de 7 anos atrás
- **CA-UC12-002:** Registros DEVEM ser imutáveis (sem edição/exclusão)
- **CA-UC12-003:** Filtros DEVEM funcionar: período, tipo, consumidor
- **CA-UC12-004:** Exportação DEVE incluir todos os campos obrigatórios
- **CA-UC12-005:** Isolamento multi-tenant DEVE ser respeitado

---

## UC13 — Visualizar Dashboard de Conformidade

### Objetivo
Exibir visualmente a conformidade de consumidores com políticas, com indicadores visuais e atualização em tempo real.

### Pré-condições
- Usuário autenticado
- Permissão `GESTAO.POLITICAS.VIEW`
- Políticas aplicadas a consumidores

### Pós-condições
- Dashboard carregado em ≤2 segundos
- Dados atualizados em tempo real via SignalR
- Indicadores visuais com cores (Verde, Amarelo, Laranja, Vermelho)

### Fluxo Principal
- **FP-UC13-001:** Usuário acessa Gestão → Políticas → Dashboard
- **FP-UC13-002:** Sistema valida permissão GESTAO.POLITICAS.VIEW
- **FP-UC13-003:** Sistema carrega dados do dashboard via `GET /api/gestao/politicas-consumidores/dashboard`
- **FP-UC13-004:** Sistema exibe **Seção 1 - Resumo Executivo** (cards superiores):
  - Total de Consumidores com Políticas
  - Consumidores Conformes (Verde)
  - Consumidores em Aviso (Amarelo, 50-79%)
  - Consumidores Críticos (Laranja, 80-99%)
  - Consumidores em Violação (Vermelho, ≥100%)
- **FP-UC13-005:** Sistema exibe **Seção 2 - Gráfico de Evolução Temporal**:
  - Gráfico de linhas (ApexCharts)
  - Eixo X: Últimos 30 dias
  - Eixo Y: Quantidade de violações por dia
  - Linhas por tipo de política
- **FP-UC13-006:** Sistema exibe **Seção 3 - Lista de Consumidores em Situação Crítica** (>80%):
  - Grid com: Nome, Departamento, Política Aplicada, % Consumo, Status, Ações
  - Ordenado por % Consumo DESC
  - Limite: Top 20
- **FP-UC13-007:** Sistema exibe **Seção 4 - Top 10 Violadores do Período**:
  - Grid com: Nome, Departamento, Quantidade de Violações, Valor Total Violado, Última Violação
  - Ordenado por Quantidade de Violações DESC
- **FP-UC13-008:** Sistema conecta via SignalR para atualizações em tempo real
- **FP-UC13-009:** Quando houver mudança: SignalR dispara evento, Dashboard atualiza seções afetadas

### Fluxos Alternativos
- **FA-UC13-001:** Usuário seleciona período de análise
  - Usuário escolhe: Últimos 7 dias, Últimos 30 dias, Últimos 3 meses, Personalizado
  - Sistema recarrega dashboard com dados do período selecionado
- **FA-UC13-002:** Usuário filtra por departamento/filial
  - Sistema recarrega dashboard filtrado
- **FA-UC13-003:** Usuário clica em consumidor crítico
  - Sistema abre modal com detalhes do consumidor e histórico de consumo
  - Sistema oferece ação: "Liberar Temporariamente", "Ajustar Política"

### Fluxos de Exceção
- **FE-UC13-001:** Erro ao carregar dashboard
  - Sistema exibe mensagem: "Erro ao carregar dashboard. Tente novamente."
  - Sistema registra erro no log
- **FE-UC13-002:** SignalR desconectado
  - Sistema exibe alerta: "Atualização em tempo real indisponível. Recarregue a página."
  - Sistema oferece botão "Reconectar"
- **FE-UC13-003:** Dashboard carrega em >2 segundos
  - Sistema registra alerta de performance
  - Sistema analisa queries e cache

### Regras de Negócio
- **RN-UC13-001 (RN-RF049-13):** Dashboard exibe: Total por status (Conforme, Aviso, Crítico, Violação), Gráfico temporal, Lista crítica (>80%), Top 10 violadores
- **RN-UC13-002 (RN-RF049-13):** Cores: Verde (Conforme), Amarelo (Aviso 50-79%), Laranja (Crítico 80-99%), Vermelho (Violação ≥100%)
- **RN-UC13-003 (RN-RF049-13):** Dashboard atualiza em tempo real via SignalR
- **RN-UC13-004 (RN-RF049-13):** Dados históricos (>3 meses) carregam sob demanda
- **RN-UC13-005:** Tempo de carregamento ≤2 segundos
- **RN-UC13-006:** Isolamento multi-tenant (apenas dados do tenant do usuário)

### Critérios de Aceite
- **CA-UC13-001:** Dashboard DEVE carregar em ≤2 segundos
- **CA-UC13-002:** Sistema DEVE usar cores conforme especificado (Verde/Amarelo/Laranja/Vermelho)
- **CA-UC13-003:** Dashboard DEVE atualizar em tempo real via SignalR
- **CA-UC13-004:** Dados históricos (>3 meses) DEVEM carregar sob demanda
- **CA-UC13-005:** Sistema DEVE exibir Top 10 violadores e Top 20 críticos
- **CA-UC13-006:** Isolamento multi-tenant DEVE ser respeitado

---

## UC14 — Importar/Exportar Políticas

### Objetivo
Permitir importação e exportação de políticas em formato JSON para replicação entre ambientes ou backup.

### Pré-condições
- Usuário autenticado
- Permissão `GESTAO.POLITICAS.ADMIN`

### Pós-condições (Exportação)
- Arquivo JSON gerado com todas as políticas e configurações
- Download disponível para o usuário

### Pós-condições (Importação)
- Políticas importadas do arquivo JSON
- Validação de schema executada
- Conflitos resolvidos
- Histórico de importação criado

### Fluxo Principal (Exportação)
- **FP-UC14-001:** Usuário acessa Gestão → Políticas → Exportar
- **FP-UC14-002:** Sistema valida permissão GESTAO.POLITICAS.ADMIN
- **FP-UC14-003:** Sistema exibe modal de exportação
- **FP-UC14-004:** Usuário seleciona políticas a exportar (opções: Todas, Apenas Ativas, Selecionadas)
- **FP-UC14-005:** Usuário clica em "Exportar"
- **FP-UC14-006:** Sistema gera JSON com estrutura:
  ```json
  {
    "versao": "1.0",
    "data_exportacao": "2025-12-31T10:00:00Z",
    "tenant": "Id_Fornecedor_Hash",
    "politicas": [...]
  }
  ```
- **FP-UC14-007:** Sistema oferece download do arquivo: `politicas_export_YYYYMMDD_HHmmss.json`
- **FP-UC14-008:** Sistema registra evento de auditoria (POLITICAS_EXPORTED)

### Fluxo Principal (Importação)
- **FP-UC14-009:** Usuário acessa Gestão → Políticas → Importar
- **FP-UC14-010:** Sistema valida permissão GESTAO.POLITICAS.ADMIN
- **FP-UC14-011:** Sistema exibe modal de importação
- **FP-UC14-012:** Usuário faz upload do arquivo JSON
- **FP-UC14-013:** Sistema valida schema JSON (estrutura, campos obrigatórios, tipos)
- **FP-UC14-014:** Sistema verifica conflitos com políticas existentes (Nome duplicado)
- **FP-UC14-015:** Sistema exibe preview com:
  - Políticas a criar: [N]
  - Políticas com conflito: [M] (ação: Ignorar, Substituir, Renomear)
  - Políticas inválidas: [K]
- **FP-UC14-016:** Usuário resolve conflitos (seleciona ação para cada conflito)
- **FP-UC14-017:** Usuário clica em "Confirmar Importação"
- **FP-UC14-018:** Sistema importa políticas conforme ações selecionadas
- **FP-UC14-019:** Sistema cria registro de histórico de importação (data, usuário, arquivo, resultado)
- **FP-UC14-020:** Sistema exibe relatório: "Importadas com sucesso: [N]. Ignoradas: [M]. Erros: [K]."
- **FP-UC14-021:** Sistema registra evento de auditoria (POLITICAS_IMPORTED)

### Fluxos Alternativos
- **FA-UC14-001:** Exportação de políticas selecionadas
  - Usuário marca políticas específicas na lista (UC00)
  - Sistema exporta apenas políticas selecionadas
- **FA-UC14-002:** Importação com renomeação automática
  - Usuário seleciona opção "Renomear automaticamente em caso de conflito"
  - Sistema adiciona sufixo "_importado_YYYYMMDD" aos nomes duplicados

### Fluxos de Exceção
- **FE-UC14-001:** Arquivo JSON com schema inválido
  - Sistema exibe erro: "Schema JSON inválido. Consulte a documentação."
  - Sistema lista erros de validação (campos faltando, tipos incorretos)
  - Sistema NÃO permite importação
- **FE-UC14-002:** Importação de políticas inválidas
  - Sistema exibe erro: "[K] políticas possuem erros de validação."
  - Sistema lista políticas inválidas e motivos
  - Sistema permite importar apenas políticas válidas
- **FE-UC14-003:** Erro durante importação
  - Sistema exibe mensagem: "Erro ao importar políticas. Tente novamente."
  - Sistema registra erro no log
  - Transação é revertida (rollback)

### Regras de Negócio
- **RN-UC14-001 (RN-RF049-12):** Exportação gera JSON com todas as políticas e configurações
- **RN-UC14-002 (RN-RF049-12):** Importação valida estrutura do arquivo
- **RN-UC14-003 (RN-RF049-12):** Importação verifica conflitos com políticas existentes
- **RN-UC14-004 (RN-RF049-12):** Importação permite preview antes de confirmar
- **RN-UC14-005 (RN-RF049-12):** Importação cria histórico
- **RN-UC14-006 (RN-RF049-12):** Formato JSON deve seguir schema validado
- **RN-UC14-007 (RN-RF049-12):** Importação de políticas inválidas é rejeitada com mensagem de erro detalhada
- **RN-UC14-008:** Conflitos podem ser resolvidos: Ignorar, Substituir, Renomear

### Critérios de Aceite
- **CA-UC14-001:** Exportação DEVE gerar JSON válido
- **CA-UC14-002:** Importação DEVE validar schema JSON
- **CA-UC14-003:** Sistema DEVE verificar conflitos e permitir resolução
- **CA-UC14-004:** Sistema DEVE exibir preview antes de importar
- **CA-UC14-005:** Sistema DEVE criar histórico de importação
- **CA-UC14-006:** Importação inválida DEVE ser rejeitada com erro detalhado

---

## UC15 — Gerenciar Templates de Políticas

### Objetivo
Gerenciar templates pré-configurados de políticas para agilizar criação e padronização.

### Pré-condições
- Usuário autenticado
- Permissão `GESTAO.POLITICAS.ADMIN`

### Pós-condições
- Templates criados/editados/excluídos
- Templates disponíveis para uso no UC01

### Fluxo Principal
- **FP-UC15-001:** Usuário acessa Gestão → Políticas → Templates
- **FP-UC15-002:** Sistema valida permissão GESTAO.POLITICAS.ADMIN
- **FP-UC15-003:** Sistema exibe lista de templates com colunas: Nome, Descrição, Tipo, Políticas Criadas a Partir Deste Template, Ações
- **FP-UC15-004:** Sistema exibe templates padrão (Executivo, Gerente, Colaborador, Estagiário) com flag "Sistema" (não podem ser deletados)
- **FP-UC15-005:** Usuário clica em "Novo Template"
- **FP-UC15-006:** Sistema exibe modal de criação de template
- **FP-UC15-007:** Usuário informa: Nome*, Descrição*, Tipo*, Configuração JSON* (limites, restrições, alertas)
- **FP-UC15-008:** Sistema valida schema JSON da configuração
- **FP-UC15-009:** Usuário clica em "Salvar"
- **FP-UC15-010:** Sistema cria registro TemplatePolitica
- **FP-UC15-011:** Sistema exibe mensagem: "Template criado com sucesso."
- **FP-UC15-012:** Sistema atualiza lista de templates

### Fluxos Alternativos
- **FA-UC15-001:** Usuário edita template existente
  - Usuário clica em "Editar" na lista
  - Sistema carrega dados do template
  - Usuário altera campos
  - Sistema valida e salva alterações
  - Sistema exibe mensagem: "Template atualizado com sucesso."
- **FA-UC15-002:** Usuário exclui template customizado
  - Usuário seleciona template (não pode ser template de sistema)
  - Sistema verifica se template está em uso (políticas criadas a partir dele)
  - Se em uso: exibe erro "Não é possível excluir template em uso."
  - Se não em uso: solicita confirmação e executa soft delete
- **FA-UC15-003:** Usuário clona template existente
  - Usuário clica em "Clonar" na lista
  - Sistema cria novo template com sufixo "_copia"
  - Usuário pode customizar e salvar

### Fluxos de Exceção
- **FE-UC15-001:** Configuração JSON inválida
  - Sistema exibe erro: "Schema JSON inválido. Consulte a documentação."
  - Sistema não permite salvar
- **FE-UC15-002:** Tentativa de deletar template de sistema
  - Sistema exibe erro: "Templates de sistema não podem ser deletados."
  - Sistema desabilita botão "Excluir" para templates de sistema
- **FE-UC15-003:** Tentativa de deletar template em uso
  - Sistema exibe erro: "Não é possível excluir template em uso. [N] políticas foram criadas a partir dele."
  - Sistema não permite exclusão

### Regras de Negócio
- **RN-UC15-001 (RN-RF049-11):** Templates disponíveis: Executivo (sem limites), Gerente (R$ 500), Colaborador (R$ 200), Estagiário (R$ 50, apenas local)
- **RN-UC15-002 (RN-RF049-11):** Templates podem ser customizados ao aplicar
- **RN-UC15-003 (RN-RF049-11):** Templates podem ser criados por administradores
- **RN-UC15-004 (RN-RF049-11):** Templates não podem ser deletados se estiverem em uso
- **RN-UC15-005:** Templates de sistema (flag Fl_Sistema=true) não podem ser deletados
- **RN-UC15-006:** Configuração JSON deve seguir schema validado
- **RN-UC15-007:** Templates isolados por tenant (Id_Fornecedor)

### Critérios de Aceite
- **CA-UC15-001:** Sistema DEVE exibir templates padrão (Executivo, Gerente, Colaborador, Estagiário)
- **CA-UC15-002:** Templates DEVEM permitir customização ao aplicar
- **CA-UC15-003:** Administradores DEVEM poder criar templates customizados
- **CA-UC15-004:** Sistema DEVE validar schema JSON da configuração
- **CA-UC15-005:** Templates em uso NÃO devem poder ser deletados
- **CA-UC15-006:** Templates de sistema NÃO devem poder ser deletados

---

## 4. MATRIZ DE RASTREABILIDADE

| UC | Funcionalidades RF049 | Regras de Negócio RF049 |
|----|----------------------|------------------------|
| UC00 | F04 | RN-15 |
| UC01 | F01 | RN-01, RN-11, RN-15 |
| UC02 | F03 | RN-15 |
| UC03 | F02 | RN-15 |
| UC04 | F05 | RN-15 |
| UC05 | F06 | RN-02, RN-03, RN-07, RN-15 |
| UC06 | F07 | RN-07, RN-15 |
| UC07 | F06 | RN-06, RN-15 |
| UC08 | F08 | RN-04, RN-09, RN-15 |
| UC09 | F09 | RN-10, RN-15 |
| UC10 | F10 | RN-04, RN-15 |
| UC11 | F11, F13 | RN-05, RN-08, RN-15 |
| UC12 | F12 | RN-07, RN-15 |
| UC13 | F14 | RN-13, RN-15 |
| UC14 | F15, F16 | RN-12, RN-15 |
| UC15 | F17 | RN-11, RN-15 |

**Cobertura:** 17 funcionalidades → 16 UCs → 100% de cobertura

---

## CHANGELOG

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 2.0 | 2025-12-31 | Agência ALC - alc.dev.br | Versão canônica orientada a contrato - Cobertura total de 17 funcionalidades do RF049 com 16 UCs completos |
| 1.0 | 2025-12-18 | IControlIT Architect Agent | Versão inicial (formato antigo, incompleto) |
