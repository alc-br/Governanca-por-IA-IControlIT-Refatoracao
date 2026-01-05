# UC-RF061 — Casos de Uso Canônicos

**RF:** RF061 — Gestão de Ordens de Serviço (OS)
**Versão:** 2.1
**Data:** 2025-12-31
**Autor:** Agência ALC - alc.dev.br
**Epic:** EPIC008-SD-Service-Desk
**Fase:** Fase-5-Service-Desk

---

## 1. OBJETIVO DO DOCUMENTO

Este documento descreve **todos os Casos de Uso (UC)** derivados do **RF061**, cobrindo integralmente o comportamento funcional esperado para gestão completa de Ordens de Serviço (OS) para atendimentos técnicos presenciais (field service).

Os UCs aqui definidos servem como **contrato comportamental**, sendo a **fonte primária** para geração de:
- Casos de Teste (TC-RF061.yaml)
- Massas de Teste (MT-RF061.yaml)
- Evidências de auditoria e validação funcional
- Execução por agentes de IA (tester, QA, E2E)

---

## 2. SUMÁRIO DE CASOS DE USO

| ID | Nome | Ator Principal |
|----|------|----------------|
| UC00 | Listar Ordens de Serviço | Usuário Autenticado |
| UC01 | Criar Ordem de Serviço | Usuário Autenticado |
| UC02 | Visualizar Ordem de Serviço | Usuário Autenticado |
| UC03 | Executar Ordem de Serviço (Check-in/Check-out) | Técnico |
| UC04 | Cancelar Ordem de Serviço | Gestor/Atendente |
| UC05 | Agendar Ordem de Serviço | Atendente/Gestor |
| UC06 | Reagendar Ordem de Serviço | Atendente/Gestor/Técnico |
| UC07 | Monitorar SLA de Ordens de Serviço | Gestor |
| UC08 | Visualizar Dashboard e Mapa de OSs | Gestor |

---

## 3. PADRÕES GERAIS APLICÁVEIS A TODOS OS UCs

- Todos os acessos respeitam **isolamento por tenant (EmpresaId)**
- Todas as ações exigem **permissão explícita (RBAC)**
- Erros não devem vazar informações sensíveis
- Auditoria deve registrar **quem**, **quando** e **qual ação**
- Mensagens devem ser claras, previsíveis e rastreáveis
- OSs finalizadas **não podem** mudar de status
- Checklist obrigatório por tipo de OS (RN-RF061-003)
- Assinatura digital obrigatória para finalização (RN-RF061-004)
- Geolocalização de check-in/check-out obrigatória (RN-RF061-007)

---

## UC00 — Listar Ordens de Serviço

### Objetivo
Permitir que o usuário visualize todas as OS do seu tenant com filtros avançados.

### Pré-condições
- Usuário autenticado
- Permissão `GES.OS.VIEW_ANY`

### Pós-condições
- Lista exibida conforme filtros e paginação

### Fluxo Principal
- **FP-UC00-001:** Usuário acessa funcionalidade Ordens de Serviço
- **FP-UC00-002:** Sistema valida permissão
- **FP-UC00-003:** Sistema carrega OSs do tenant (EmpresaId)
- **FP-UC00-004:** Sistema aplica paginação (50 registros/página)
- **FP-UC00-005:** Sistema exibe lista com colunas (número, tipo, técnico, localização, data agendada, status, SLA)

### Fluxos Alternativos
- **FA-UC00-001:** Filtrar por status (AGUARDANDO_AGENDAMENTO, AGENDADA, EM_ATENDIMENTO, FINALIZADA, CANCELADA)
- **FA-UC00-002:** Filtrar por técnico
- **FA-UC00-003:** Filtrar por período (data agendada)
- **FA-UC00-004:** Filtrar por SLA (dentro do prazo, atrasada, vencida)
- **FA-UC00-005:** Ordenar por coluna (número, data, SLA)
- **FA-UC00-006:** Exportar para Excel/CSV
- **FA-UC00-007:** Visualizar mapa com OSs abertas (geolocalização)

### Fluxos de Exceção
- **FE-UC00-001:** Usuário sem permissão → HTTP 403
- **FE-UC00-002:** Nenhuma OS cadastrada → estado vazio

### Regras de Negócio
- RN-RF061-016: Isolamento Multi-Tenant

### Critérios de Aceite
- **CA-UC00-001:** A lista DEVE exibir apenas OSs do tenant do usuário
- **CA-UC00-002:** OSs soft-deleted NÃO aparecem
- **CA-UC00-003:** Paginação DEVE ser aplicada (50 registros/página)
- **CA-UC00-004:** Sistema DEVE permitir ordenação por número, data, SLA
- **CA-UC00-005:** Filtros DEVEM ser acumuláveis

---

## UC01 — Criar Ordem de Serviço

### Objetivo
Permitir criação de nova OS (manual ou automática a partir de solicitação aprovada).

### Pré-condições
- Usuário autenticado
- Permissão `GES.OS.CREATE`

### Pós-condições
- OS criada com número único (OS-YYYY-NNNNN)
- Status inicial: AGUARDANDO_AGENDAMENTO
- Auditoria registrada

### Fluxo Principal
- **FP-UC01-001:** Usuário acessa formulário de criação
- **FP-UC01-002:** Sistema valida permissão
- **FP-UC01-003:** Usuário preenche campos obrigatórios (tipo, descrição, localização, cliente, data prevista)
- **FP-UC01-004:** Sistema valida campos obrigatórios
- **FP-UC01-005:** Sistema gera número único (OS-YYYY-NNNNN)
- **FP-UC01-006:** Sistema cria OS com EmpresaId automático
- **FP-UC01-007:** Sistema define status inicial: AGUARDANDO_AGENDAMENTO
- **FP-UC01-008:** Sistema registra auditoria
- **FP-UC01-009:** Sistema confirma sucesso

### Fluxos Alternativos
- **FA-UC01-001:** Criação automática a partir de solicitação aprovada (RN-RF061-001)
- **FA-UC01-002:** Agendar imediatamente (técnico + data/hora) → status AGENDADA
- **FA-UC01-003:** Anexar ativo relacionado
- **FA-UC01-004:** Definir prioridade (BAIXA, MÉDIA, ALTA, CRÍTICA)
- **FA-UC01-005:** Carrega checklist template do tipo de OS

### Fluxos de Exceção
- **FE-UC01-001:** Campo obrigatório ausente → HTTP 400
- **FE-UC01-002:** Tipo de OS não encontrado → HTTP 400
- **FE-UC01-003:** Cliente de outro tenant → HTTP 403

### Regras de Negócio
- RN-RF061-001: Criação Automática de OS a partir de Solicitação
- RN-RF061-003: Checklist Obrigatório por Tipo de OS
- RN-RF061-016: Isolamento Multi-Tenant

### Critérios de Aceite
- **CA-UC01-001:** EmpresaId DEVE ser preenchido automaticamente
- **CA-UC01-002:** Número DEVE ser único e no formato OS-YYYY-NNNNN
- **CA-UC01-003:** Status inicial DEVE ser AGUARDANDO_AGENDAMENTO
- **CA-UC01-004:** Criação automática a partir de solicitação DEVE copiar dados relevantes
- **CA-UC01-005:** Auditoria DEVE ser registrada APÓS sucesso

---

## UC02 — Visualizar Ordem de Serviço

### Objetivo
Permitir visualização completa de uma OS com todos os detalhes, checklist, fotos, assinatura e histórico.

### Pré-condições
- Usuário autenticado
- Permissão `GES.OS.VIEW`

### Pós-condições
- Dados exibidos corretamente

### Fluxo Principal
- **FP-UC02-001:** Usuário seleciona OS na listagem
- **FP-UC02-002:** Sistema valida permissão
- **FP-UC02-003:** Sistema valida tenant (EmpresaId)
- **FP-UC02-004:** Sistema carrega dados completos (cabeçalho, técnico, agendamento, checklist, peças, fotos)
- **FP-UC02-005:** Sistema carrega histórico de mudanças de status
- **FP-UC02-006:** Sistema carrega assinatura digital (se houver)
- **FP-UC02-007:** Sistema calcula tempo de atendimento (se finalizada)
- **FP-UC02-008:** Sistema exibe dados formatados

### Fluxos Alternativos
- **FA-UC02-001:** Visualizar checklist preenchido pelo técnico
- **FA-UC02-002:** Visualizar fotos de evidência (antes/depois)
- **FA-UC02-003:** Visualizar assinatura digital do cliente
- **FA-UC02-004:** Visualizar peças utilizadas com valores
- **FA-UC02-005:** Visualizar checkpoints de geolocalização (check-in/check-out)
- **FA-UC02-006:** Visualizar avaliação NPS do cliente
- **FA-UC02-007:** Visualizar timeline completa da OS
- **FA-UC02-008:** Download PDF assinado

### Fluxos de Exceção
- **FE-UC02-001:** OS não encontrada → HTTP 404
- **FE-UC02-002:** OS de outro tenant → HTTP 404

### Regras de Negócio
- RN-RF061-008: Cálculo Automático de Tempo de Atendimento
- RN-RF061-016: Isolamento Multi-Tenant

### Critérios de Aceite
- **CA-UC02-001:** Usuário SÓ pode visualizar OSs do próprio tenant
- **CA-UC02-002:** Informações de auditoria DEVEM ser exibidas
- **CA-UC02-003:** Tentativa de acessar OS de outro tenant → HTTP 404
- **CA-UC02-004:** Sistema DEVE exibir tempo de atendimento calculado (check-out - check-in)
- **CA-UC02-005:** Fotos DEVEM ser carregadas de Azure Blob Storage

---

## UC03 — Executar Ordem de Serviço (Check-in/Check-out)

### Objetivo
Permitir que técnico execute a OS completa (check-in, preenchimento checklist, peças, fotos, check-out, assinatura).

### Pré-condições
- Técnico autenticado
- Permissão `GES.OS.EXECUTE`
- OS em status AGENDADA ou CONFIRMADA

### Pós-condições
- OS finalizada com assinatura
- Status: FINALIZADA
- Baixa automática de peças no estoque
- Pré-nota gerada para faturamento
- Auditoria registrada

### Fluxo Principal (Check-in)
- **FP-UC03-001:** Técnico acessa OS agendada
- **FP-UC03-002:** Sistema valida permissão
- **FP-UC03-003:** Técnico clica "Iniciar Atendimento"
- **FP-UC03-004:** Sistema captura geolocalização (lat, lon, data/hora) (RN-RF061-007)
- **FP-UC03-005:** Sistema registra check-in
- **FP-UC03-006:** Sistema muda status para EM_ATENDIMENTO
- **FP-UC03-007:** Sistema inicia cálculo de SLA

### Fluxo Principal (Execução)
- **FP-UC03-008:** Técnico preenche checklist obrigatório (RN-RF061-003)
- **FP-UC03-009:** Técnico adiciona peças utilizadas (se houver) (RN-RF061-005)
- **FP-UC03-010:** Técnico upload fotos de evidência (antes/depois) (RN-RF061-006)

### Fluxo Principal (Check-out)
- **FP-UC03-011:** Técnico clica "Concluir Atendimento"
- **FP-UC03-012:** Sistema valida checklist completo (itens obrigatórios preenchidos)
- **FP-UC03-013:** Sistema captura geolocalização de check-out (RN-RF061-007)
- **FP-UC03-014:** Sistema calcula tempo de atendimento (check-out - check-in) (RN-RF061-008)
- **FP-UC03-015:** Sistema muda status para AGUARDANDO_ASSINATURA

### Fluxo Principal (Assinatura)
- **FP-UC03-016:** Técnico solicita assinatura do cliente
- **FP-UC03-017:** Cliente assina digitalmente (canvas touchscreen) (RN-RF061-004)
- **FP-UC03-018:** Sistema captura nome, CPF, data/hora, IP, hash SHA-256
- **FP-UC03-019:** Sistema armazena assinatura
- **FP-UC03-020:** Sistema finaliza OS (status: FINALIZADA)
- **FP-UC03-021:** Sistema dá baixa automática em peças no estoque (RN-RF061-005)
- **FP-UC03-022:** Sistema gera pré-nota para faturamento (RN-RF061-012)
- **FP-UC03-023:** Sistema atualiza histórico de performance do técnico (RN-RF061-013)
- **FP-UC03-024:** Sistema registra auditoria
- **FP-UC03-025:** Sistema envia notificação ao cliente

### Fluxos Alternativos
- **FA-UC03-001:** Pausar execução temporariamente (aguardando peça) → requer justificativa
- **FA-UC03-002:** Reagendar (cliente ausente, emergência) → requer justificativa (RN-RF061-009)
- **FA-UC03-003:** Solicitar avaliação NPS ao cliente (RN-RF061-011)
- **FA-UC03-004:** Adicionar observações técnicas

### Fluxos de Exceção
- **FE-UC03-001:** Check-in em horário diferente do agendado → alerta + registro
- **FE-UC03-002:** GPS desabilitado → bloquear check-in até ativar
- **FE-UC03-003:** Checklist incompleto → bloquear finalização
- **FE-UC03-004:** Assinatura ausente → bloquear finalização
- **FE-UC03-005:** Estoque insuficiente → alertar mas permitir finalização
- **FE-UC03-006:** Falha na geração de pré-nota → registrar erro e notificar gestor

### Regras de Negócio
- RN-RF061-003: Checklist Obrigatório por Tipo de OS
- RN-RF061-004: Assinatura Digital Obrigatória
- RN-RF061-005: Controle de Peças Utilizadas
- RN-RF061-006: Fotos de Evidência (Antes/Depois)
- RN-RF061-007: Geolocalização de Check-in/Check-out
- RN-RF061-008: Cálculo Automático de Tempo de Atendimento
- RN-RF061-009: Reagendamento com Justificativa Obrigatória
- RN-RF061-011: Avaliação NPS do Serviço
- RN-RF061-012: Integração com Faturamento
- RN-RF061-013: Histórico de Performance do Técnico

### Critérios de Aceite
- **CA-UC03-001:** Check-in DEVE capturar geolocalização com 6 casas decimais
- **CA-UC03-002:** Checklist DEVE bloquear finalização se item obrigatório não preenchido
- **CA-UC03-003:** Assinatura DEVE ser armazenada com hash SHA-256
- **CA-UC03-004:** Tempo de atendimento DEVE ser calculado em minutos (check-out - check-in)
- **CA-UC03-005:** Baixa de peças DEVE ocorrer APÓS finalização com sucesso
- **CA-UC03-006:** OS finalizada NÃO pode mais mudar de status
- **CA-UC03-007:** Pré-nota DEVE conter valor peças + mão de obra

---

## UC04 — Cancelar Ordem de Serviço

### Objetivo
Permitir cancelamento de OS com justificativa obrigatória.

### Pré-condições
- Usuário autenticado
- Permissão `GES.OS.CANCEL`
- OS NÃO está em status FINALIZADA

### Pós-condições
- OS cancelada
- Justificativa registrada
- Cliente notificado
- Auditoria registrada

### Fluxo Principal
- **FP-UC04-001:** Gestor seleciona OS e acessa cancelamento
- **FP-UC04-002:** Sistema valida permissão
- **FP-UC04-003:** Sistema valida que OS NÃO está finalizada
- **FP-UC04-004:** Sistema exibe formulário de justificativa
- **FP-UC04-005:** Usuário preenche justificativa (mínimo 20 caracteres)
- **FP-UC04-006:** Sistema valida justificativa
- **FP-UC04-007:** Sistema muda status para CANCELADA
- **FP-UC04-008:** Sistema registra justificativa, data/hora, usuário
- **FP-UC04-009:** Sistema registra auditoria
- **FP-UC04-010:** Sistema envia notificação ao cliente
- **FP-UC04-011:** Sistema confirma sucesso

### Fluxos Alternativos
- **FA-UC04-001:** Liberar técnico alocado para outras OSs
- **FA-UC04-002:** Devolver peças reservadas ao estoque

### Fluxos de Exceção
- **FE-UC04-001:** OS já finalizada → HTTP 400 ("OS finalizada não pode ser cancelada")
- **FE-UC04-002:** Justificativa < 20 caracteres → HTTP 400
- **FE-UC04-003:** OS de outro tenant → HTTP 403

### Regras de Negócio
- RN-RF061-016: Isolamento Multi-Tenant

### Critérios de Aceite
- **CA-UC04-001:** OS finalizada NÃO pode ser cancelada
- **CA-UC04-002:** Justificativa DEVE ter mínimo 20 caracteres
- **CA-UC04-003:** Cliente DEVE ser notificado automaticamente
- **CA-UC04-004:** Auditoria DEVE registrar quem cancelou e quando
- **CA-UC04-005:** Técnico alocado DEVE ser liberado para outras OSs

---

## UC05 — Agendar Ordem de Serviço

### Objetivo
Permitir agendamento de OS com técnico, verificando disponibilidade e enviando notificações automáticas ao cliente.

### Pré-condições
- Usuário autenticado
- Permissão `GES.OS.SCHEDULE`
- OS em status AGUARDANDO_AGENDAMENTO

### Pós-condições
- OS agendada com técnico e data/hora definidos
- Cliente notificado 24h antes
- Auditoria registrada

### Fluxo Principal
- **FP-UC05-001:** Atendente seleciona OS em AGUARDANDO_AGENDAMENTO
- **FP-UC05-002:** Sistema valida permissão
- **FP-UC05-003:** Usuário acessa tela de agendamento
- **FP-UC05-004:** Sistema carrega tipos de OS e SLAs
- **FP-UC05-005:** Usuário seleciona técnico
- **FP-UC05-006:** Sistema consulta disponibilidade do técnico (RN-RF061-002)
- **FP-UC05-007:** Sistema verifica OSs já agendadas para o técnico
- **FP-UC05-008:** Sistema calcula janelas livres considerando duração estimada
- **FP-UC05-009:** Sistema exibe agenda com slots disponíveis (verde) e ocupados (vermelho)
- **FP-UC05-010:** Usuário seleciona data/hora disponível
- **FP-UC05-011:** Sistema valida que slot está livre
- **FP-UC05-012:** Sistema muda status para AGENDADA
- **FP-UC05-013:** Sistema envia notificação 24h antes (SMS/WhatsApp/Email) (RN-RF061-014)
- **FP-UC05-014:** Sistema inclui link para cliente confirmar presença
- **FP-UC05-015:** Sistema registra auditoria
- **FP-UC05-016:** Sistema confirma sucesso

### Fluxos Alternativos
- **FA-UC05-001:** Cliente confirmar presença via link → status CONFIRMADA
- **FA-UC05-002:** Visualizar histórico de agendamentos do técnico
- **FA-UC05-003:** Filtrar janelas por período (manhã, tarde)

### Fluxos de Exceção
- **FE-UC05-001:** Horário ocupado → HTTP 400 ("Técnico já possui OS agendada neste horário")
- **FE-UC05-002:** Técnico de outro tenant → HTTP 403
- **FE-UC05-003:** Técnico inativo → HTTP 400

### Regras de Negócio
- RN-RF061-002: Agendamento com Verificação de Disponibilidade
- RN-RF061-010: Controle de SLA de Atendimento
- RN-RF061-014: Notificações de Agendamento
- RN-RF061-016: Isolamento Multi-Tenant

### Critérios de Aceite
- **CA-UC05-001:** Sistema DEVE consultar agenda do técnico antes de permitir agendamento
- **CA-UC05-002:** Slots ocupados NÃO podem ser selecionados
- **CA-UC05-003:** Notificação DEVE ser enviada 24h antes via SMS/WhatsApp/Email
- **CA-UC05-004:** Link de confirmação DEVE atualizar status para CONFIRMADA ao ser clicado
- **CA-UC05-005:** Cálculo de janelas DEVE considerar duração estimada do tipo de OS

---

## UC06 — Reagendar Ordem de Serviço

### Objetivo
Permitir reagendamento de OS com justificativa obrigatória e notificação automática ao cliente.

### Pré-condições
- Usuário autenticado
- Permissão `GES.OS.RESCHEDULE`
- OS em status AGENDADA ou CONFIRMADA

### Pós-condições
- OS reagendada com nova data/hora
- Justificativa registrada
- Cliente notificado
- Auditoria registrada

### Fluxo Principal
- **FP-UC06-001:** Usuário seleciona OS agendada ou confirmada
- **FP-UC06-002:** Sistema valida permissão
- **FP-UC06-003:** Usuário acessa reagendamento
- **FP-UC06-004:** Sistema exibe formulário com justificativa obrigatória (RN-RF061-009)
- **FP-UC06-005:** Usuário preenche justificativa (mínimo 20 caracteres)
- **FP-UC06-006:** Sistema valida justificativa
- **FP-UC06-007:** Sistema exibe agenda do técnico (ou permite trocar técnico)
- **FP-UC06-008:** Sistema consulta disponibilidade (RN-RF061-002)
- **FP-UC06-009:** Usuário seleciona nova data/hora
- **FP-UC06-010:** Sistema valida slot disponível
- **FP-UC06-011:** Sistema atualiza data agendada
- **FP-UC06-012:** Sistema registra justificativa, data/hora, usuário responsável
- **FP-UC06-013:** Sistema envia notificação automática ao cliente (RN-RF061-009)
- **FP-UC06-014:** Sistema registra em auditoria
- **FP-UC06-015:** Sistema confirma sucesso

### Fluxos Alternativos
- **FA-UC06-001:** Trocar técnico ao reagendar
- **FA-UC06-002:** Visualizar histórico de reagendamentos

### Fluxos de Exceção
- **FE-UC06-001:** Justificativa < 20 caracteres → HTTP 400
- **FE-UC06-002:** OS finalizada ou cancelada → HTTP 400 ("não pode reagendar")
- **FE-UC06-003:** Novo horário ocupado → HTTP 400

### Regras de Negócio
- RN-RF061-002: Agendamento com Verificação de Disponibilidade
- RN-RF061-009: Reagendamento com Justificativa Obrigatória
- RN-RF061-016: Isolamento Multi-Tenant

### Critérios de Aceite
- **CA-UC06-001:** Justificativa DEVE ter mínimo 20 caracteres
- **CA-UC06-002:** Cliente DEVE ser notificado automaticamente
- **CA-UC06-003:** Histórico DEVE registrar data/hora e usuário responsável
- **CA-UC06-004:** Sistema DEVE permitir troca de técnico ao reagendar

---

## UC07 — Monitorar SLA de Ordens de Serviço

### Objetivo
Permitir monitoramento de SLA de OSs com alertas automáticos quando prazo estiver próximo ou vencido.

### Pré-condições
- Usuário autenticado
- Permissão `GES.OS.DASHBOARD`

### Pós-condições
- Dashboard exibindo OSs com status de SLA
- Alertas emitidos quando necessário

### Fluxo Principal
- **FP-UC07-001:** Gestor acessa dashboard de SLA
- **FP-UC07-002:** Sistema valida permissão
- **FP-UC07-003:** Sistema carrega OSs do tenant com SLAs
- **FP-UC07-004:** Sistema calcula tempo restante em horário comercial (8h-18h, seg-sex) (RN-RF061-010)
- **FP-UC07-005:** Sistema classifica OSs (Dentro do Prazo, Alerta 20%, Vencida)
- **FP-UC07-006:** Sistema exibe relatório com colunas (número, tipo, técnico, SLA definido, tempo restante, status SLA)
- **FP-UC07-007:** Sistema destaca visualmente OSs com alerta (amarelo) e vencidas (vermelho)

### Fluxos Alternativos
- **FA-UC07-001:** Filtrar por status SLA (Dentro do Prazo, Alerta, Vencida)
- **FA-UC07-002:** Filtrar por técnico
- **FA-UC07-003:** Filtrar por período
- **FA-UC07-004:** Exportar relatório Excel/PDF
- **FA-UC07-005:** Receber alerta por email quando SLA atingir 20% (RN-RF061-010)
- **FA-UC07-006:** Receber alerta por SMS quando SLA vencer (RN-RF061-010)

### Fluxos de Exceção
- **FE-UC07-001:** Usuário sem permissão → HTTP 403
- **FE-UC07-002:** Nenhuma OS com SLA → estado vazio

### Regras de Negócio
- RN-RF061-010: Controle de SLA de Atendimento
- RN-RF061-016: Isolamento Multi-Tenant

### Critérios de Aceite
- **CA-UC07-001:** Cálculo de SLA DEVE considerar apenas horário comercial (8h-18h, seg-sex)
- **CA-UC07-002:** Alerta DEVE ser emitido quando faltar 20% do prazo
- **CA-UC07-003:** OSs vencidas DEVEM ser destacadas em vermelho
- **CA-UC07-004:** OSs em alerta DEVEM ser destacadas em amarelo
- **CA-UC07-005:** Sistema DEVE enviar email quando SLA atingir 20%
- **CA-UC07-006:** Sistema DEVE enviar SMS quando SLA vencer

---

## UC08 — Visualizar Dashboard e Mapa de OSs

### Objetivo
Permitir visualização de dashboard com mapa geográfico de OSs abertas e técnicos em campo em tempo real.

### Pré-condições
- Usuário autenticado
- Permissão `GES.OS.DASHBOARD`

### Pós-condições
- Dashboard exibindo mapa com OSs abertas
- Mapa atualizado em tempo real

### Fluxo Principal
- **FP-UC08-001:** Gestor acessa dashboard de OSs
- **FP-UC08-002:** Sistema valida permissão
- **FP-UC08-003:** Sistema carrega OSs abertas do tenant (RN-RF061-015)
- **FP-UC08-004:** Sistema carrega checkpoints de geolocalização (check-in dos técnicos)
- **FP-UC08-005:** Sistema exibe mapa com pins coloridos por status
- **FP-UC08-006:** Sistema destaca técnicos em campo com ícone diferenciado (EM_ATENDIMENTO)
- **FP-UC08-007:** Sistema atualiza mapa automaticamente a cada 30 segundos (RN-RF061-015)
- **FP-UC08-008:** Sistema exibe painel com totalizadores (Total OSs, Agendadas, Em Atendimento, Finalizadas Hoje)

### Fluxos Alternativos
- **FA-UC08-001:** Filtrar por status (AGENDADA, EM_ATENDIMENTO, CONFIRMADA)
- **FA-UC08-002:** Filtrar por técnico
- **FA-UC08-003:** Filtrar por região geográfica (zoom no mapa)
- **FA-UC08-004:** Clicar em pin → exibir resumo da OS (número, cliente, técnico, horário)
- **FA-UC08-005:** Visualizar histórico de performance por técnico (RN-RF061-013)
- **FA-UC08-006:** Visualizar ranking de técnicos (NPS médio, OSs concluídas) (RN-RF061-013)

### Fluxos de Exceção
- **FE-UC08-001:** Usuário sem permissão → HTTP 403
- **FE-UC08-002:** Nenhuma OS aberta → mapa vazio + mensagem

### Regras de Negócio
- RN-RF061-013: Histórico de Performance do Técnico
- RN-RF061-015: Dashboard com Mapa de OSs Abertas
- RN-RF061-016: Isolamento Multi-Tenant

### Critérios de Aceite
- **CA-UC08-001:** Mapa DEVE exibir pins coloridos por status (AGENDADA=azul, EM_ATENDIMENTO=verde, CONFIRMADA=amarelo)
- **CA-UC08-002:** Técnicos em campo DEVEM ter ícone diferenciado
- **CA-UC08-003:** Mapa DEVE atualizar automaticamente a cada 30 segundos
- **CA-UC08-004:** Painel DEVE exibir totalizadores (Total OSs, Agendadas, Em Atendimento, Finalizadas Hoje)
- **CA-UC08-005:** Clicar em pin DEVE exibir resumo da OS
- **CA-UC08-006:** Dashboard DEVE permitir visualizar histórico de performance por técnico

---

## 4. MATRIZ DE RASTREABILIDADE

| UC | Regras de Negócio |
|----|-------------------|
| UC00 | RN-RF061-016 |
| UC01 | RN-RF061-001, RN-RF061-003, RN-RF061-016 |
| UC02 | RN-RF061-008, RN-RF061-016 |
| UC03 | RN-RF061-003, RN-RF061-004, RN-RF061-005, RN-RF061-006, RN-RF061-007, RN-RF061-008, RN-RF061-009, RN-RF061-011, RN-RF061-012, RN-RF061-013 |
| UC04 | RN-RF061-016 |
| UC05 | RN-RF061-002, RN-RF061-010, RN-RF061-014, RN-RF061-016 |
| UC06 | RN-RF061-002, RN-RF061-009, RN-RF061-016 |
| UC07 | RN-RF061-010, RN-RF061-016 |
| UC08 | RN-RF061-013, RN-RF061-015, RN-RF061-016 |

**Cobertura:** 100% das 16 regras de negócio (RN-RF061-001 a RN-RF061-016)

---

## CHANGELOG

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 2.1 | 2025-12-31 | Agência ALC - alc.dev.br | Versão canônica COMPLETA com 9 UCs (UC00-UC08) - 100% cobertura das 16 regras de negócio |
| 2.0 | 2025-12-31 | Agência ALC - alc.dev.br | Versão canônica INCOMPLETA com 5 UCs (UC00-UC04) - 68.75% cobertura |
| 1.0 | 2025-12-18 | Architect Agent | Versão stub incompleta com 11 UCs |
