# UC-RF038 — Casos de Uso Canônicos

**RF:** RF038 — Gestão de SLA Solicitações
**Versão:** 2.0
**Data:** 2025-12-31
**Autor:** Agência ALC - alc.dev.br
**Epic:** EPIC008-SD - Service Desk
**Fase:** Fase 5 - Service Desk

---

## 1. OBJETIVO DO DOCUMENTO

Este documento descreve **todos os Casos de Uso (UC)** derivados do **RF038**, cobrindo integralmente o comportamento funcional esperado para gestão completa de Service Level Agreement (SLA) em solicitações de TI, com cálculo automático de prazos, monitoramento em tempo real, alertas escalonados, escalação automática, gestão de exceções, dashboard de compliance e análise de performance.

Os UCs aqui definidos servem como **contrato comportamental**, sendo a **fonte primária** para geração de:
- Casos de Teste (TC-RF038.yaml)
- Massas de Teste (MT-RF038.yaml)
- Evidências de auditoria e validação funcional
- Execução por agentes de IA (tester, QA, E2E)

---

## 2. SUMÁRIO DE CASOS DE USO

| ID | Nome | Ator Principal |
|----|------|----------------|
| UC00 | Listar Configurações de SLA | Usuário Autenticado |
| UC01 | Criar Configuração de SLA | Supervisor/Gerente |
| UC02 | Editar Configuração de SLA | Supervisor/Gerente |
| UC03 | Inativar Configuração de SLA | Gerente/Administrador |
| UC04 | Pausar SLA de Solicitação | Supervisor/Gerente |
| UC05 | Retomar SLA de Solicitação | Supervisor/Gerente |
| UC06 | Solicitar Extensão de Prazo | Supervisor/Gerente |
| UC07 | Aprovar/Rejeitar Extensão de Prazo | Gerente/Diretor |
| UC08 | Visualizar Dashboard de Monitoramento SLA | Supervisor/Gerente |
| UC09 | Gerar Relatório de Compliance SLA | Supervisor/Gerente/Diretor |
| UC10 | Visualizar Não-Conformidades de SLA | Supervisor/Gerente/Diretor |
| UC11 | Tratar Não-Conformidade (Análise de Causa Raiz) | Supervisor/Gerente |

---

## 3. PADRÕES GERAIS APLICÁVEIS A TODOS OS UCs

- Todos os acessos respeitam **isolamento por tenant (fornecedor)**
- Todas as ações exigem **permissão explícita RBAC**
- Erros não devem vazar informações sensíveis
- Auditoria deve registrar **quem**, **quando** e **qual ação**
- Mensagens devem ser claras, previsíveis e rastreáveis
- Cálculo de SLA DEVE considerar apenas horário de atendimento configurado
- Feriados cadastrados DEVEM ser excluídos do cálculo
- Alertas DEVEM ser enviados nos percentuais exatos (50%, 80%, 100%)
- Escalação automática DEVE ocorrer ao atingir 100% sem resolução

---

## UC00 — Listar Configurações de SLA

### Objetivo
Permitir que o usuário visualize configurações de SLA do seu tenant com opções de filtro, ordenação e paginação.

### Pré-condições
- Usuário autenticado
- Permissão `sla.config.view_any`

### Pós-condições
- Lista exibida conforme filtros e paginação

### Fluxo Principal
- **FP-UC00-001:** Usuário acessa a funcionalidade "Configuração de SLA" pelo menu
- **FP-UC00-002:** Sistema valida permissão do usuário
- **FP-UC00-003:** Sistema carrega configurações de SLA do tenant (query filter global)
- **FP-UC00-004:** Sistema aplica paginação padrão (20 registros por página)
- **FP-UC00-005:** Sistema aplica ordenação padrão (Tipo Solicitação ASC, Prioridade ASC)
- **FP-UC00-006:** Sistema exibe lista com colunas: Tipo Solicitação, Prioridade, Prazo (horas), Horário Atendimento, Status, Ações

### Fluxos Alternativos
- **FA-UC00-001:** Filtrar por tipo de solicitação
- **FA-UC00-002:** Filtrar por prioridade
- **FA-UC00-003:** Filtrar por status (ativo/inativo)
- **FA-UC00-004:** Ordenar por qualquer coluna

### Fluxos de Exceção
- **FE-UC00-001:** Usuário sem permissão → HTTP 403 com mensagem "Acesso negado"
- **FE-UC00-002:** Nenhuma configuração cadastrada → estado vazio exibido com botão "Criar Primeira Configuração"

### Regras de Negócio
- **RN-UC-00-001:** Somente configurações do tenant do usuário autenticado (Id_Fornecedor)
- **RN-UC-00-002:** Configurações soft-deleted NÃO aparecem na listagem (Deleted_At IS NULL)
- **RN-UC-00-003:** Paginação padrão: 20 registros por página
- **RN-UC-00-004:** Status "Ativo" exibe badge verde, "Inativo" exibe badge cinza

### Critérios de Aceite
- **CA-UC00-001:** A lista DEVE exibir apenas configurações do tenant do usuário autenticado
- **CA-UC00-002:** Configurações excluídas (soft delete) NÃO devem aparecer
- **CA-UC00-003:** Paginação DEVE ser aplicada com limite padrão de 20 registros
- **CA-UC00-004:** Sistema DEVE permitir ordenação por qualquer coluna visível
- **CA-UC00-005:** Filtros DEVEM ser acumuláveis e refletir na URL

---

## UC01 — Criar Configuração de SLA

### Objetivo
Permitir a criação de uma nova configuração de SLA por tipo de solicitação e prioridade.

### Pré-condições
- Usuário autenticado
- Permissão `sla.config.create`

### Pós-condições
- Configuração criada no banco
- Auditoria registrada
- Cálculo automático de prazos ativado para novas solicitações

### Fluxo Principal
- **FP-UC01-001:** Usuário clica em "Nova Configuração SLA"
- **FP-UC01-002:** Sistema valida permissão
- **FP-UC01-003:** Sistema exibe formulário com campos:
  - Tipo de Solicitação* (dropdown)
  - Prioridade* (dropdown: Baixa/Média/Alta/Urgente)
  - Prazo em Horas* (number, min: 1, max: 720)
  - Horário de Atendimento* (dropdown: 8x5, 12x5, 24x7, Customizado)
  - Considerar Feriados (checkbox, default: true)
  - Escalação Automática (checkbox, default: false)
  - Nível de Escalação (dropdown, obrigatório se Escalação = true)
- **FP-UC01-004:** Usuário preenche os campos
- **FP-UC01-005:** Usuário clica em "Salvar"
- **FP-UC01-006:** Sistema valida dados (RN-RF038-001, RN-RF038-002, RN-RF038-005)
- **FP-UC01-007:** Sistema verifica duplicação (tipo + prioridade)
- **FP-UC01-008:** Sistema cria registro no banco
- **FP-UC01-009:** Sistema registra auditoria
- **FP-UC01-010:** Sistema exibe mensagem de sucesso
- **FP-UC01-011:** Sistema redireciona para lista de configurações

### Fluxos Alternativos
- **FA-UC01-001:** Cancelar criação → volta para lista sem salvar
- **FA-UC01-002:** Salvar e criar outra → salva e reexibe formulário limpo

### Fluxos de Exceção
- **FE-UC01-001:** Campos obrigatórios vazios → erro inline por campo
- **FE-UC01-002:** Prazo fora dos limites (RN-RF038-002) → erro "Prioridade Urgente max 4h, Alta max 24h, Média max 72h, Baixa max 168h"
- **FE-UC01-003:** Duplicação (tipo + prioridade já existe) → erro "Já existe configuração para este tipo de solicitação e prioridade"
- **FE-UC01-004:** Erro inesperado → mensagem genérica + log interno

### Regras de Negócio
- **RN-UC-01-001:** Campos obrigatórios: Tipo Solicitação, Prioridade, Prazo, Horário Atendimento
- **RN-UC-01-002:** Id_Fornecedor preenchido automaticamente com tenant do usuário
- **RN-UC-01-003:** Created_By preenchido automaticamente com ID do usuário autenticado
- **RN-UC-01-004:** Prazo máximo por prioridade (RN-RF038-002):
  - Urgente: max 4h
  - Alta: max 24h
  - Média: max 72h (3 dias)
  - Baixa: max 168h (7 dias)
- **RN-UC-01-005:** Combinação tipo + prioridade DEVE ser única por tenant

### Critérios de Aceite
- **CA-UC01-001:** Todos os campos obrigatórios DEVEM ser validados antes de persistir
- **CA-UC01-002:** Id_Fornecedor DEVE ser preenchido automaticamente
- **CA-UC01-003:** Created_By DEVE ser preenchido automaticamente
- **CA-UC01-004:** Sistema DEVE retornar erro claro se validação falhar
- **CA-UC01-005:** Auditoria DEVE ser registrada APÓS sucesso da criação
- **CA-UC01-006:** Duplicação de tipo + prioridade DEVE ser impedida

---

## UC02 — Editar Configuração de SLA

### Objetivo
Permitir alteração de configuração existente de SLA.

### Pré-condições
- Usuário autenticado
- Permissão `sla.config.update`
- Configuração pertence ao tenant do usuário

### Pós-condições
- Configuração atualizada
- Auditoria registrada com estado anterior e novo
- Alteração afeta apenas novas solicitações (RN-RF038-004)

### Fluxo Principal
- **FP-UC02-001:** Usuário clica em "Editar" em uma configuração
- **FP-UC02-002:** Sistema valida permissão
- **FP-UC02-003:** Sistema valida que registro pertence ao tenant
- **FP-UC02-004:** Sistema carrega dados atuais no formulário
- **FP-UC02-005:** Usuário altera campos permitidos (Prazo, Horário Atendimento, Escalação)
- **FP-UC02-006:** Usuário clica em "Salvar"
- **FP-UC02-007:** Sistema valida alterações
- **FP-UC02-008:** Sistema persiste alterações
- **FP-UC02-009:** Sistema registra auditoria com snapshot anterior e novo
- **FP-UC02-010:** Sistema exibe mensagem "Configuração atualizada com sucesso. Alteração aplicada a partir de agora."

### Fluxos Alternativos
- **FA-UC02-001:** Cancelar edição → volta para lista sem salvar

### Fluxos de Exceção
- **FE-UC02-001:** Erro de validação → exibe erros inline
- **FE-UC02-002:** Tentativa de editar configuração de outro tenant → HTTP 404
- **FE-UC02-003:** Configuração já excluída → HTTP 404

### Regras de Negócio
- **RN-UC-02-001:** Updated_By preenchido automaticamente
- **RN-UC-02-002:** Updated_At preenchido automaticamente
- **RN-UC-02-003:** Alteração NÃO afeta solicitações já criadas (RN-RF038-004)
- **RN-UC-02-004:** Tipo de Solicitação e Prioridade NÃO podem ser alterados (campos desabilitados)

### Critérios de Aceite
- **CA-UC02-001:** Updated_By DEVE ser preenchido automaticamente
- **CA-UC02-002:** Updated_At DEVE ser preenchido automaticamente
- **CA-UC02-003:** Auditoria DEVE registrar estado anterior e novo
- **CA-UC02-004:** Tentativa de editar configuração de outro tenant DEVE retornar 404
- **CA-UC02-005:** Tipo e Prioridade DEVEM ser somente leitura (não editáveis)

---

## UC03 — Inativar Configuração de SLA

### Objetivo
Permitir desativação de configuração de SLA obsoleta.

### Pré-condições
- Usuário autenticado
- Permissão `sla.config.delete`
- Configuração pertence ao tenant

### Pós-condições
- Configuração marcada como inativa
- Não será aplicada a novas solicitações

### Fluxo Principal
- **FP-UC03-001:** Usuário clica em "Inativar" em uma configuração ativa
- **FP-UC03-002:** Sistema valida permissão
- **FP-UC03-003:** Sistema verifica se há solicitações ativas vinculadas (RN-RF038-005)
- **FP-UC03-004:** Sistema exibe modal de confirmação "Tem certeza que deseja inativar esta configuração?"
- **FP-UC03-005:** Usuário confirma
- **FP-UC03-006:** Sistema marca Status = "Inativo"
- **FP-UC03-007:** Sistema registra auditoria
- **FP-UC03-008:** Sistema exibe mensagem de sucesso

### Fluxos Alternativos
- **FA-UC03-001:** Cancelar inativação → fecha modal sem alterar

### Fluxos de Exceção
- **FE-UC03-001:** Configuração com solicitações ativas vinculadas → erro "Não é possível inativar. Existem X solicitações ativas usando esta configuração"
- **FE-UC03-002:** Tentativa de inativar configuração de outro tenant → HTTP 404

### Regras de Negócio
- **RN-UC-03-001:** Inativação é lógica (Status = Inativo), não física
- **RN-UC-03-002:** Configuração com solicitações ativas NÃO pode ser inativada (RN-RF038-005)
- **RN-UC-03-003:** Configuração inativa pode ser reativada posteriormente

### Critérios de Aceite
- **CA-UC03-001:** Inativação DEVE ser lógica via campo Status
- **CA-UC03-002:** Sistema DEVE impedir inativação se há solicitações ativas vinculadas
- **CA-UC03-003:** Sistema DEVE exigir confirmação explícita
- **CA-UC03-004:** Auditoria DEVE registrar inativação

---

## UC04 — Pausar SLA de Solicitação

### Objetivo
Permitir pausa temporária do cálculo de SLA em situações específicas.

### Pré-condições
- Usuário autenticado
- Permissão `sla.pausar`
- Solicitação em aberto (não finalizada)
- SLA não está já pausado

### Pós-condições
- SLA pausado temporariamente
- Tempo não contabilizado durante pausa
- Histórico de pausa registrado

### Fluxo Principal
- **FP-UC04-001:** Usuário acessa solicitação em aberto
- **FP-UC04-002:** Usuário clica em "Pausar SLA"
- **FP-UC04-003:** Sistema valida permissão
- **FP-UC04-004:** Sistema verifica que solicitação não está finalizada
- **FP-UC04-005:** Sistema verifica que SLA não está já pausado
- **FP-UC04-006:** Sistema exibe modal com campo "Motivo da Pausa*" (mín. 10 caracteres)
- **FP-UC04-007:** Usuário informa motivo
- **FP-UC04-008:** Usuário confirma
- **FP-UC04-009:** Sistema valida motivo (RN-RF038-004)
- **FP-UC04-010:** Sistema marca Status_SLA = "Pausado"
- **FP-UC04-011:** Sistema registra Data_Pausa, Usuario_Pausa, Motivo_Pausa
- **FP-UC04-012:** Sistema para contabilização de tempo
- **FP-UC04-013:** Sistema registra auditoria
- **FP-UC04-014:** Sistema exibe mensagem "SLA pausado com sucesso"

### Fluxos Alternativos
- **FA-UC04-001:** Cancelar pausa → fecha modal sem pausar

### Fluxos de Exceção
- **FE-UC04-001:** Motivo com menos de 10 caracteres → erro "Motivo deve ter no mínimo 10 caracteres"
- **FE-UC04-002:** Solicitação já finalizada → erro "Não é possível pausar SLA de solicitação finalizada"
- **FE-UC04-003:** SLA já pausado → erro "SLA já está pausado. Retome antes de pausar novamente"
- **FE-UC04-004:** Usuário sem permissão → HTTP 403

### Regras de Negócio
- **RN-UC-04-001:** Motivo da pausa é OBRIGATÓRIO (mín. 10 caracteres) (RN-RF038-004)
- **RN-UC-04-002:** Durante pausa, tempo NÃO é contabilizado
- **RN-UC-04-003:** Solicitação NÃO pode estar finalizada
- **RN-UC-04-004:** NÃO permitir múltiplas pausas simultâneas
- **RN-UC-04-005:** Histórico completo de pausas DEVE ser registrado

### Critérios de Aceite
- **CA-UC04-001:** Motivo DEVE ter no mínimo 10 caracteres
- **CA-UC04-002:** Sistema DEVE impedir pausa de solicitação finalizada
- **CA-UC04-003:** Sistema DEVE impedir múltiplas pausas simultâneas
- **CA-UC04-004:** Auditoria DEVE registrar quem pausou, quando e por quê
- **CA-UC04-005:** Durante pausa, tempo NÃO deve ser contabilizado no percentual decorrido

---

## UC05 — Retomar SLA de Solicitação

### Objetivo
Permitir retomada de SLA previamente pausado, com recálculo automático de prazo.

### Pré-condições
- Usuário autenticado
- Permissão `sla.retomar`
- SLA está pausado

### Pós-condições
- SLA retomado
- Nova data limite recalculada
- Histórico de retomada registrado

### Fluxo Principal
- **FP-UC05-001:** Usuário acessa solicitação com SLA pausado
- **FP-UC05-002:** Usuário clica em "Retomar SLA"
- **FP-UC05-003:** Sistema valida permissão
- **FP-UC05-004:** Sistema verifica que SLA está pausado
- **FP-UC05-005:** Sistema calcula tempo decorrido antes da pausa
- **FP-UC05-006:** Sistema calcula tempo restante
- **FP-UC05-007:** Sistema recalcula nova data limite = Data_Retomada + Tempo_Restante (considerando horário de atendimento e feriados)
- **FP-UC05-008:** Sistema marca Status_SLA = estado anterior à pausa
- **FP-UC05-009:** Sistema registra Data_Retomada, Usuario_Retomada
- **FP-UC05-010:** Sistema retoma contabilização de tempo
- **FP-UC05-011:** Sistema recalcula alertas pendentes
- **FP-UC05-012:** Sistema registra auditoria
- **FP-UC05-013:** Sistema exibe mensagem "SLA retomado. Nova data limite: DD/MM/YYYY HH:MM"

### Fluxos Alternativos
- **FA-UC05-001:** Cancelar retomada → fecha modal sem retomar

### Fluxos de Exceção
- **FE-UC05-001:** SLA não está pausado → erro "SLA não está pausado"
- **FE-UC05-002:** Usuário sem permissão → HTTP 403

### Regras de Negócio
- **RN-UC-05-001:** Ao retomar, recalcular data limite considerando tempo já decorrido (RN-RF038-004)
- **RN-UC-05-002:** Novo prazo = Momento atual + Tempo restante (antes da pausa)
- **RN-UC-05-003:** Cálculo DEVE considerar horário de atendimento e feriados
- **RN-UC-05-004:** Alertas pendentes DEVEM ser recalculados

### Critérios de Aceite
- **CA-UC05-001:** Sistema DEVE recalcular data limite corretamente
- **CA-UC05-002:** Cálculo DEVE considerar apenas horário de atendimento
- **CA-UC05-003:** Feriados DEVEM ser excluídos do novo cálculo
- **CA-UC05-004:** Auditoria DEVE registrar quem retomou e quando
- **CA-UC05-005:** Alertas pendentes DEVEM ser atualizados

**Exemplo de Cálculo:**
```
Criada: 14/01 10:00 | SLA: 16h úteis | Prazo Original: 15/01 18:00
Pausada: 14/01 14:00 (4h decorridas, 12h restantes)
Retomada: 16/01 09:00
Novo prazo: 16/01 09:00 + 12h úteis = 17/01 13:00
```

---

## UC06 — Solicitar Extensão de Prazo

### Objetivo
Permitir que supervisores/gerentes solicitem extensão de prazo de SLA com justificativa.

### Pré-condições
- Usuário autenticado
- Permissão `sla.extensao.solicitar`
- Solicitação em aberto
- Máximo de 1 extensão pendente
- Máximo de 2 extensões totais (RN-RF038-007)

### Pós-condições
- Extensão registrada como pendente
- Aprovador notificado

### Fluxo Principal
- **FP-UC06-001:** Usuário acessa solicitação em aberto
- **FP-UC06-002:** Usuário clica em "Solicitar Extensão de Prazo"
- **FP-UC06-003:** Sistema valida permissão
- **FP-UC06-004:** Sistema verifica que não há extensão pendente
- **FP-UC06-005:** Sistema verifica que não atingiu limite de 2 extensões
- **FP-UC06-006:** Sistema exibe modal com campos:
  - Prazo Atual (readonly)
  - Novo Prazo Solicitado* (datetime, deve ser > Prazo Atual)
  - Justificativa* (textarea, mín. 20 caracteres)
  - Aprovador* (dropdown de gerentes/diretores)
- **FP-UC06-007:** Usuário preenche campos
- **FP-UC06-008:** Usuário confirma
- **FP-UC06-009:** Sistema valida dados (RN-RF038-007)
- **FP-UC06-010:** Sistema cria registro de extensão com Status = "Pendente"
- **FP-UC06-011:** Sistema envia notificação para aprovador
- **FP-UC06-012:** Sistema registra auditoria
- **FP-UC06-013:** Sistema exibe mensagem "Extensão solicitada com sucesso. Aguardando aprovação de [Nome Aprovador]"

### Fluxos Alternativos
- **FA-UC06-001:** Cancelar solicitação → fecha modal sem salvar

### Fluxos de Exceção
- **FE-UC06-001:** Novo prazo menor ou igual ao atual → erro "Novo prazo deve ser maior que o prazo atual"
- **FE-UC06-002:** Justificativa com menos de 20 caracteres → erro "Justificativa deve ter no mínimo 20 caracteres"
- **FE-UC06-003:** Já existe extensão pendente → erro "Já existe uma solicitação de extensão pendente"
- **FE-UC06-004:** Limite de 2 extensões atingido → erro "Limite de 2 extensões por solicitação atingido"

### Regras de Negócio
- **RN-UC-06-001:** Novo prazo DEVE ser maior que prazo original (RN-RF038-007)
- **RN-UC-06-002:** Justificativa OBRIGATÓRIA (mín. 20 caracteres)
- **RN-UC-06-003:** Apenas 1 extensão pendente por solicitação
- **RN-UC-06-004:** Máximo 2 extensões por solicitação (total)
- **RN-UC-06-005:** Aprovador recebe notificação imediatamente

### Critérios de Aceite
- **CA-UC06-001:** Novo prazo DEVE ser validado como maior que atual
- **CA-UC06-002:** Justificativa DEVE ter mínimo 20 caracteres
- **CA-UC06-003:** Sistema DEVE impedir múltiplas extensões pendentes
- **CA-UC06-004:** Sistema DEVE impedir mais de 2 extensões totais
- **CA-UC06-005:** Aprovador DEVE receber notificação

---

## UC07 — Aprovar/Rejeitar Extensão de Prazo

### Objetivo
Permitir que aprovadores autorizados aprovem ou rejeitem extensões solicitadas.

### Pré-condições
- Usuário autenticado
- Permissão `sla.extensao.aprovar`
- Extensão com Status = "Pendente"
- Usuário é o aprovador designado

### Pós-condições (se aprovado)
- Novo prazo aplicado
- Alertas recalculados
- Solicitante notificado

### Pós-condições (se rejeitado)
- Extensão marcada como rejeitada
- Prazo original mantido
- Solicitante notificado

### Fluxo Principal
- **FP-UC07-001:** Aprovador acessa lista de extensões pendentes
- **FP-UC07-002:** Aprovador clica em "Visualizar" em uma extensão
- **FP-UC07-003:** Sistema valida que usuário é o aprovador designado
- **FP-UC07-004:** Sistema exibe detalhes da extensão:
  - Solicitação #
  - Prazo Atual
  - Novo Prazo Solicitado
  - Justificativa
  - Solicitante
  - Data Solicitação
- **FP-UC07-005:** Aprovador clica em "Aprovar" ou "Rejeitar"
- **FP-UC07-006:** Se "Aprovar":
  - Sistema aplica novo prazo
  - Sistema recalcula alertas pendentes
  - Sistema marca Status_Extensao = "Aprovada"
  - Sistema registra Aprovador_Id, Data_Aprovacao
  - Sistema envia notificação para solicitante
  - Sistema exibe mensagem "Extensão aprovada com sucesso"
- **FP-UC07-007:** Se "Rejeitar":
  - Sistema exibe campo "Motivo da Rejeição*" (mín. 10 caracteres)
  - Aprovador informa motivo
  - Sistema marca Status_Extensao = "Rejeitada"
  - Sistema registra Rejeitador_Id, Data_Rejeicao, Motivo_Rejeicao
  - Sistema envia notificação para solicitante
  - Sistema exibe mensagem "Extensão rejeitada"

### Fluxos Alternativos
- **FA-UC07-001:** Cancelar → volta para lista sem alterar

### Fluxos de Exceção
- **FE-UC07-001:** Usuário não é o aprovador designado → HTTP 403
- **FE-UC07-002:** Extensão já foi aprovada/rejeitada → erro "Extensão já foi processada"
- **FE-UC07-003:** Motivo de rejeição com menos de 10 caracteres → erro "Motivo deve ter no mínimo 10 caracteres"

### Regras de Negócio
- **RN-UC-07-001:** Se aprovado, novo prazo é aplicado e alertas recalculados (RN-RF038-007)
- **RN-UC-07-002:** Se rejeitado, prazo original é mantido
- **RN-UC-07-003:** Histórico completo de aprovações/rejeições registrado
- **RN-UC-07-004:** Solicitante DEVE ser notificado do resultado

### Critérios de Aceite
- **CA-UC07-001:** Se aprovado, novo prazo DEVE ser aplicado imediatamente
- **CA-UC07-002:** Alertas DEVEM ser recalculados após aprovação
- **CA-UC07-003:** Motivo de rejeição DEVE ser obrigatório
- **CA-UC07-004:** Solicitante DEVE receber notificação
- **CA-UC07-005:** Histórico DEVE ser registrado na auditoria

---

## UC08 — Visualizar Dashboard de Monitoramento SLA

### Objetivo
Exibir dashboard centralizado com status de solicitações ativas e indicadores visuais por proximidade do prazo.

### Pré-condições
- Usuário autenticado
- Permissão `sla.dashboard.view`

### Pós-condições
- Dashboard exibido com dados em tempo real
- Auto-refresh ativado

### Fluxo Principal
- **FP-UC08-001:** Usuário acessa "Dashboard SLA" pelo menu
- **FP-UC08-002:** Sistema valida permissão
- **FP-UC08-003:** Sistema carrega solicitações em aberto do tenant
- **FP-UC08-004:** Sistema calcula percentual decorrido de cada solicitação
- **FP-UC08-005:** Sistema aplica cor conforme proximidade (RN-RF038-008):
  - Verde: 0-50%
  - Amarelo: 50-80%
  - Vermelho: 80-100%
  - Preto: Breach (>100%)
- **FP-UC08-006:** Sistema exibe grid com colunas:
  - # Solicitação
  - Tipo
  - Prioridade
  - Atendente
  - Prazo Limite
  - Tempo Restante
  - % Decorrido
  - Status (badge colorido)
- **FP-UC08-007:** Sistema ordena por prazo mais próximo primeiro
- **FP-UC08-008:** Sistema ativa auto-refresh a cada 60 segundos (SignalR)

### Fluxos Alternativos
- **FA-UC08-001:** Filtrar por prioridade
- **FA-UC08-002:** Filtrar por tipo de solicitação
- **FA-UC08-003:** Filtrar por atendente
- **FA-UC08-004:** Filtrar por status (verde/amarelo/vermelho/preto)

### Fluxos de Exceção
- **FE-UC08-001:** Usuário sem permissão → HTTP 403
- **FE-UC08-002:** Nenhuma solicitação ativa → estado vazio "Nenhuma solicitação ativa no momento"

### Regras de Negócio
- **RN-UC-08-001:** Cores por proximidade do prazo (RN-RF038-008):
  - Verde: 0-50%
  - Amarelo: 50-80%
  - Vermelho: 80-100%
  - Preto: Breach
- **RN-UC-08-002:** Apenas solicitações em aberto exibidas
- **RN-UC-08-003:** Dashboard DEVE respeitar multi-tenancy
- **RN-UC-08-004:** Dados cacheados por 30s para performance
- **RN-UC-08-005:** Auto-refresh a cada 60 segundos (SignalR)

### Critérios de Aceite
- **CA-UC08-001:** Cores DEVEM refletir corretamente percentual decorrido
- **CA-UC08-002:** Apenas solicitações em aberto DEVEM ser exibidas
- **CA-UC08-003:** Ordenação padrão DEVE ser por prazo mais próximo
- **CA-UC08-004:** Auto-refresh DEVE ocorrer a cada 60s via SignalR
- **CA-UC08-005:** Dashboard DEVE exibir apenas dados do tenant do usuário

---

## UC09 — Gerar Relatório de Compliance SLA

### Objetivo
Gerar relatório gerencial exibindo taxa de cumprimento de SLA por período, tipo, prioridade e atendente.

### Pré-condições
- Usuário autenticado
- Permissão `sla.relatorios.gerar`

### Pós-condições
- Relatório gerado e exibido
- Opção de exportação disponível

### Fluxo Principal
- **FP-UC09-001:** Usuário acessa "Relatórios SLA" pelo menu
- **FP-UC09-002:** Usuário clica em "Relatório de Compliance"
- **FP-UC09-003:** Sistema valida permissão
- **FP-UC09-004:** Sistema exibe filtros:
  - Período* (data início, data fim, máx. 24 meses no passado)
  - Tipo de Solicitação (todos/específico)
  - Prioridade (todas/específica)
  - Atendente (todos/específico)
- **FP-UC09-005:** Usuário define filtros e clica em "Gerar"
- **FP-UC09-006:** Sistema valida período (RN-RF038-009)
- **FP-UC09-007:** Sistema calcula:
  - Total de solicitações finalizadas no período
  - Total dentro do prazo
  - Total fora do prazo (breach)
  - Taxa de cumprimento = (Dentro do prazo / Total finalizadas) × 100
- **FP-UC09-008:** Sistema exibe relatório com:
  - Taxa de cumprimento geral (%)
  - Gráfico de linha (tendência mês a mês)
  - Detalhamento por tipo de solicitação
  - Detalhamento por prioridade
  - Detalhamento por atendente
  - Comparação com períodos anteriores (MoM, YoY)
- **FP-UC09-009:** Sistema oferece botões de exportação (PDF, Excel, CSV)

### Fluxos Alternativos
- **FA-UC09-001:** Exportar para PDF → gera arquivo PDF com formatação
- **FA-UC09-002:** Exportar para Excel → gera arquivo .xlsx com tabelas dinâmicas
- **FA-UC09-003:** Exportar para CSV → gera arquivo .csv simples

### Fluxos de Exceção
- **FE-UC09-001:** Período inválido (data início > data fim) → erro "Data início deve ser anterior à data fim"
- **FE-UC09-002:** Período maior que 24 meses → erro "Período máximo permitido: 24 meses"
- **FE-UC09-003:** Nenhum dado no período selecionado → estado vazio "Nenhuma solicitação finalizada neste período"

### Regras de Negócio
- **RN-UC-09-001:** Cálculo: (Dentro do prazo / Total finalizadas) × 100 (RN-RF038-009)
- **RN-UC-09-002:** Detalhamento por: tipo, prioridade, atendente, período
- **RN-UC-09-003:** Comparação com períodos anteriores (MoM, YoY)
- **RN-UC-09-004:** Período DEVE ser válido (máx. 24 meses no passado)
- **RN-UC-09-005:** Dados consolidados e cacheados para performance

### Critérios de Aceite
- **CA-UC09-001:** Taxa de cumprimento DEVE ser calculada corretamente
- **CA-UC09-002:** Relatório DEVE permitir exportação em PDF, Excel e CSV
- **CA-UC09-003:** Período máximo de 24 meses DEVE ser respeitado
- **CA-UC09-004:** Dados DEVEM ser consolidados por tipo, prioridade e atendente
- **CA-UC09-005:** Comparação com períodos anteriores DEVE ser exibida

---

## UC10 — Visualizar Não-Conformidades de SLA

### Objetivo
Permitir visualização de todas as não-conformidades (breaches) registradas, com filtros e detalhamento.

### Pré-condições
- Usuário autenticado
- Permissão `sla.nao_conformidade.view`

### Pós-condições
- Lista de não-conformidades exibida
- Filtros aplicados

### Fluxo Principal
- **FP-UC10-001:** Usuário acessa "Não-Conformidades SLA" pelo menu
- **FP-UC10-002:** Sistema valida permissão
- **FP-UC10-003:** Sistema carrega não-conformidades do tenant
- **FP-UC10-004:** Sistema aplica filtros padrão (últimos 30 dias)
- **FP-UC10-005:** Sistema exibe grid com colunas:
  - # NC
  - # Solicitação
  - Data/Hora Breach
  - Tempo de Atraso
  - Atendente
  - Supervisor
  - Status Tratamento (Pendente/Em Análise/Concluída)
  - Impacto (Alto/Médio/Baixo)
  - Ações
- **FP-UC10-006:** Sistema ordena por data breach DESC (mais recente primeiro)

### Fluxos Alternativos
- **FA-UC10-001:** Filtrar por período
- **FA-UC10-002:** Filtrar por status tratamento
- **FA-UC10-003:** Filtrar por atendente
- **FA-UC10-004:** Filtrar por supervisor
- **FA-UC10-005:** Exportar lista para Excel

### Fluxos de Exceção
- **FE-UC10-001:** Usuário sem permissão → HTTP 403
- **FE-UC10-002:** Nenhuma não-conformidade no período → estado vazio "Nenhuma não-conformidade registrada"

### Regras de Negócio
- **RN-UC-10-001:** Apenas não-conformidades do tenant do usuário
- **RN-UC-10-002:** Breaches geram automaticamente registro de não-conformidade (RN-RF038-014)
- **RN-UC-10-003:** Status padrão ao criar: "Pendente"
- **RN-UC-10-004:** Não-conformidades não tratadas em 5 dias úteis → alerta gerência

### Critérios de Aceite
- **CA-UC10-001:** Lista DEVE exibir apenas não-conformidades do tenant
- **CA-UC10-002:** Ordenação padrão DEVE ser por data breach (mais recente primeiro)
- **CA-UC10-003:** Filtros DEVEM ser aplicáveis por período, status, atendente
- **CA-UC10-004:** Sistema DEVE permitir exportação para Excel
- **CA-UC10-005:** Não-conformidades pendentes > 5 dias DEVEM ser destacadas

---

## UC11 — Tratar Não-Conformidade (Análise de Causa Raiz)

### Objetivo
Permitir que supervisor/gerente preencha análise de causa raiz e plano de ação para não-conformidades.

### Pré-condições
- Usuário autenticado
- Permissão `sla.nao_conformidade.tratar`
- Não-conformidade com Status = "Pendente" ou "Em Análise"

### Pós-condições
- Análise de causa raiz preenchida
- Plano de ação definido
- Status atualizado para "Concluída"
- Gerência notificada

### Fluxo Principal
- **FP-UC11-001:** Usuário acessa lista de não-conformidades
- **FP-UC11-002:** Usuário clica em "Tratar" em uma NC pendente
- **FP-UC11-003:** Sistema valida permissão
- **FP-UC11-004:** Sistema exibe formulário com:
  - Dados da NC (readonly): # NC, # Solicitação, Data Breach, Tempo Atraso
  - Análise de Causa Raiz* (textarea, mín. 50 caracteres)
  - Plano de Ação Corretiva* (textarea, mín. 30 caracteres)
  - Prazo de Implementação* (date, máx. 30 dias a partir de hoje)
  - Responsável pela Ação* (dropdown de usuários)
- **FP-UC11-005:** Usuário preenche campos
- **FP-UC11-006:** Usuário clica em "Salvar Tratamento"
- **FP-UC11-007:** Sistema valida dados (RN-RF038-014)
- **FP-UC11-008:** Sistema atualiza NC:
  - Status = "Concluída"
  - Analise_Causa_Raiz = texto informado
  - Plano_Acao = texto informado
  - Prazo_Implementacao = data informada
  - Responsavel_Id = usuário selecionado
  - Tratado_Por = usuário autenticado
  - Data_Tratamento = timestamp atual
- **FP-UC11-009:** Sistema envia notificação para gerência
- **FP-UC11-010:** Sistema registra auditoria
- **FP-UC11-011:** Sistema exibe mensagem "Não-conformidade tratada com sucesso"

### Fluxos Alternativos
- **FA-UC11-001:** Cancelar tratamento → volta para lista sem salvar

### Fluxos de Exceção
- **FE-UC11-001:** Análise de causa raiz com menos de 50 caracteres → erro "Análise de causa raiz deve ter no mínimo 50 caracteres"
- **FE-UC11-002:** Plano de ação com menos de 30 caracteres → erro "Plano de ação deve ter no mínimo 30 caracteres"
- **FE-UC11-003:** Prazo de implementação > 30 dias → erro "Prazo de implementação não pode ser maior que 30 dias"
- **FE-UC11-004:** NC já tratada → erro "Não-conformidade já foi tratada"

### Regras de Negócio
- **RN-UC-11-001:** Análise de causa raiz OBRIGATÓRIA (mín. 50 caracteres) (RN-RF038-014)
- **RN-UC-11-002:** Ação corretiva OBRIGATÓRIA (mín. 30 caracteres)
- **RN-UC-11-003:** Prazo de implementação NÃO pode ser maior que 30 dias
- **RN-UC-11-004:** Gerência recebe notificação após tratamento
- **RN-UC-11-005:** Histórico completo de tratamento registrado na auditoria

### Critérios de Aceite
- **CA-UC11-001:** Análise de causa raiz DEVE ter mínimo 50 caracteres
- **CA-UC11-002:** Plano de ação DEVE ter mínimo 30 caracteres
- **CA-UC11-003:** Prazo de implementação DEVE ser validado (máx. 30 dias)
- **CA-UC11-004:** Gerência DEVE receber notificação após tratamento
- **CA-UC11-005:** Auditoria DEVE registrar quem tratou, quando e quais ações definidas

---

## 4. MATRIZ DE RASTREABILIDADE

| UC | Regras de Negócio RF038 | Funcionalidades RF038 |
|----|------------------------|----------------------|
| UC00 | RN-RF038-001 | RF-CRUD-02 |
| UC01 | RN-RF038-001, RN-RF038-002, RN-RF038-005 | RF-CRUD-01, RF-VAL-01, RF-VAL-02, RF-FUNC-01 |
| UC02 | RN-RF038-004 | RF-CRUD-04, RF-FUNC-01 |
| UC03 | RN-RF038-005 | RF-CRUD-05 |
| UC04 | RN-RF038-004 | RF-FUNC-04, RF-VAL-03 |
| UC05 | RN-RF038-004 | RF-FUNC-04 |
| UC06 | RN-RF038-007 | RF-FUNC-05, RF-VAL-04, RF-VAL-05 |
| UC07 | RN-RF038-007 | RF-FUNC-05 |
| UC08 | RN-RF038-008, RN-RF038-010 | RF-FUNC-06, RF-FUNC-10 |
| UC09 | RN-RF038-009, RN-RF038-015 | RF-FUNC-07 |
| UC10 | RN-RF038-014 | RF-FUNC-08 |
| UC11 | RN-RF038-014 | RF-FUNC-08 |

---

## CHANGELOG

| Versão | Data | Autor | Descrição |
|------|------|-------|-----------|
| 2.0 | 2025-12-31 | Agência ALC - alc.dev.br | Versão canônica orientada a contrato: 12 UCs completos (UC00-UC11), estrutura conforme template UC.md, cobertura 100% do RF038, fluxos detalhados, regras de negócio e critérios de aceite estruturados |
| 1.0 | 2025-12-18 | Architect Agent | Versão inicial resumida com 9 UCs básicos |
