# UC-RF025 — Casos de Uso de Gestão de Ativos

**RF:** RF025 — Gestão Completa de Ativos de TI e Telecom
**Epic:** EPIC007-FIN - Financeiro Processos
**Fase:** Fase 4 - Financeiro II Processos
**Versão:** 1.0
**Data:** 2025-12-31
**Autor:** Agência ALC - alc.dev.br

---

## 1. OBJETIVO DO DOCUMENTO

Este documento descreve **todos os Casos de Uso (UC)** derivados do **RF025**, cobrindo integralmente o comportamento funcional esperado do sistema de gestão de ativos de TI e Telecom.

Os UCs aqui definidos servem como **contrato comportamental**, sendo a **fonte primária** para geração de:
- Casos de Teste (TC-RF025.yaml)
- Massas de Teste (MT-RF025.yaml)
- Evidências de auditoria e validação funcional
- Execução por agentes de IA (tester, QA, E2E)

---

## 2. SUMÁRIO DE CASOS DE USO

| ID | Nome | Ator Principal |
|----|------|----------------|
| UC00 | Listar Ativos | Usuário Autenticado |
| UC01 | Criar Ativo | Usuário Autenticado |
| UC02 | Visualizar Ativo | Usuário Autenticado |
| UC03 | Editar Ativo | Usuário Autenticado |
| UC04 | Excluir Ativo | Usuário Autenticado |
| UC05 | Alocar Ativo | Gestor TI |
| UC06 | Transferir Ativo | Gestor TI |
| UC07 | Devolver Ativo | Usuário Autenticado |
| UC08 | Enviar para Manutenção | Gestor TI |
| UC09 | Baixar Ativo | Controller/Financeiro |
| UC10 | Inventariar Ativo | Inventariante |
| UC11 | Consultar Histórico de Movimentações | Usuário Autenticado |
| UC12 | Gerar QR Code em Lote | Gestor TI |
| UC13 | Visualizar Dashboard Executivo | Gestor TI/Diretoria |
| UC14 | Calcular Depreciação Mensal (Job) | Sistema |
| UC15 | Enviar Alertas de Garantia (Job) | Sistema |

---

## 3. PADRÕES GERAIS APLICÁVEIS A TODOS OS UCs

- Todos os acessos respeitam **isolamento por tenant** (Id_Fornecedor)
- Todas as ações exigem **permissão explícita** (RBAC)
- Erros não devem vazar informações sensíveis
- Auditoria deve registrar **quem**, **quando** e **qual ação**
- Mensagens devem ser claras, previsíveis e rastreáveis
- **Soft delete obrigatório** para preservação de histórico
- **Chain of custody** imutável para movimentações
- **QR Code gerado automaticamente** ao criar ativo

---

## UC00 — Listar Ativos

### Objetivo
Permitir que o usuário visualize ativos disponíveis do seu próprio tenant com filtros avançados e paginação.

### Pré-condições
- Usuário autenticado
- Permissão `FIN.ATIVOS.VIEW_ANY`

### Pós-condições
- Lista exibida conforme filtros e paginação aplicados

### Fluxo Principal
- **FP-UC00-001:** Usuário acessa a funcionalidade via menu
- **FP-UC00-002:** Sistema valida permissão `FIN.ATIVOS.VIEW_ANY`
- **FP-UC00-003:** Sistema carrega ativos do tenant do usuário logado
- **FP-UC00-004:** Sistema aplica paginação (padrão 20 registros)
- **FP-UC00-005:** Sistema exibe lista com colunas: Número Patrimônio, Tipo, Status, Responsável, Localização, Valor

### Fluxos Alternativos
- **FA-UC00-001:** Filtrar por Tipo de Ativo (Notebook, Desktop, Smartphone, etc.)
- **FA-UC00-002:** Filtrar por Status (Disponivel, Alocado, Manutencao, Baixado, Perdido, Reservado)
- **FA-UC00-003:** Filtrar por Localização (hierarquia: Edifício → Andar → Sala)
- **FA-UC00-004:** Filtrar por Responsável
- **FA-UC00-005:** Filtrar por faixa de Valor (Min/Max)
- **FA-UC00-006:** Ordenar por qualquer coluna visível
- **FA-UC00-007:** Buscar por Número de Patrimônio ou Número de Série

### Fluxos de Exceção
- **FE-UC00-001:** Usuário sem permissão → HTTP 403 Forbidden
- **FE-UC00-002:** Nenhum registro → estado vazio exibido ("Nenhum ativo cadastrado")
- **FE-UC00-003:** Erro ao carregar dados → exibe mensagem e permite retry

### Regras de Negócio
- **RN-UC00-001:** Somente ativos do tenant do usuário logado (Id_Fornecedor)
- **RN-UC00-002:** Ativos soft-deleted (Fl_Ativo=FALSE) não aparecem
- **RN-UC00-003:** Paginação padrão 20 registros
- **RN-UC00-004:** Filtros são acumuláveis e refletem na URL

### Critérios de Aceite
- **CA-UC00-001:** A lista DEVE exibir apenas ativos do tenant do usuário autenticado
- **CA-UC00-002:** Ativos excluídos (soft delete) NÃO devem aparecer na listagem
- **CA-UC00-003:** Paginação DEVE ser aplicada com limite padrão de 20 registros
- **CA-UC00-004:** Sistema DEVE permitir ordenação por qualquer coluna visível
- **CA-UC00-005:** Filtros DEVEM ser acumuláveis e refletir na URL

---

## UC01 — Criar Ativo

### Objetivo
Permitir criação de novo ativo com geração automática de QR Code e número de patrimônio.

### Pré-condições
- Usuário autenticado
- Permissão `FIN.ATIVOS.CREATE`

### Pós-condições
- Ativo criado e persistido
- QR Code gerado automaticamente
- Número de patrimônio gerado automaticamente
- Auditoria registrada

### Fluxo Principal
- **FP-UC01-001:** Usuário clica em "Novo Ativo"
- **FP-UC01-002:** Sistema valida permissão `FIN.ATIVOS.CREATE`
- **FP-UC01-003:** Sistema exibe formulário com campos obrigatórios por tipo
- **FP-UC01-004:** Usuário seleciona Tipo de Ativo (Notebook, Smartphone, Linha Móvel, etc.)
- **FP-UC01-005:** Sistema ajusta campos obrigatórios conforme tipo (RN-RF025-008)
- **FP-UC01-006:** Usuário preenche dados obrigatórios
- **FP-UC01-007:** Sistema valida dados (FluentValidation)
- **FP-UC01-008:** Sistema gera Número de Patrimônio automaticamente (PAT-{TipoAbrev}-{Ano}-{Sequencial})
- **FP-UC01-009:** Sistema gera QR Code 300x300px apontando para URL do ativo
- **FP-UC01-010:** Sistema armazena QR_Code_Base64 e QR_Code_URL
- **FP-UC01-011:** Sistema cria registro com Id_Fornecedor do usuário logado
- **FP-UC01-012:** Sistema registra auditoria (Created, CreatedBy)
- **FP-UC01-013:** Sistema exibe mensagem de sucesso com Número de Patrimônio gerado

### Fluxos Alternativos
- **FA-UC01-001:** Salvar e criar outro ativo (botão "Salvar e Novo")
- **FA-UC01-002:** Cancelar criação (botão "Cancelar")
- **FA-UC01-003:** Upload de foto do ativo (opcional)
- **FA-UC01-004:** Upload de NF de compra (opcional)

### Fluxos de Exceção
- **FE-UC01-001:** Erro de validação → exibe erros por campo
- **FE-UC01-002:** Número de patrimônio duplicado → HTTP 409 Conflict
- **FE-UC01-003:** IMEI inválido (smartphone) → HTTP 400 Bad Request
- **FE-UC01-004:** Campos obrigatórios ausentes → HTTP 400 Bad Request
- **FE-UC01-005:** Erro inesperado → exibe mensagem genérica e loga erro

### Regras de Negócio
- **RN-UC01-001:** Número de patrimônio único global (RN-RF025-001)
- **RN-UC01-002:** QR Code gerado automaticamente (RN-RF025-002)
- **RN-UC01-003:** Campos obrigatórios variam por tipo (RN-RF025-008)
- **RN-UC01-004:** IMEI validado para smartphones (RN-RF025-011)
- **RN-UC01-005:** Id_Fornecedor preenchido automaticamente
- **RN-UC01-006:** Status inicial sempre "Disponivel"
- **RN-UC01-007:** Created/CreatedBy preenchidos automaticamente

### Critérios de Aceite
- **CA-UC01-001:** Número de patrimônio DEVE ser gerado automaticamente no formato PAT-{TipoAbrev}-{Ano}-{Sequencial}
- **CA-UC01-002:** QR Code DEVE ser gerado automaticamente ao criar ativo
- **CA-UC01-003:** Campos obrigatórios DEVEM variar por tipo de ativo
- **CA-UC01-004:** IMEI DEVE ser validado (formato, Luhn, Anatel) se tipo = Smartphone
- **CA-UC01-005:** Id_Fornecedor DEVE ser preenchido automaticamente
- **CA-UC01-006:** Auditoria DEVE registrar Created e CreatedBy

---

## UC02 — Visualizar Ativo

### Objetivo
Permitir visualização detalhada de um ativo com histórico completo de movimentações.

### Pré-condições
- Usuário autenticado
- Permissão `FIN.ATIVOS.VIEW`

### Pós-condições
- Dados do ativo exibidos corretamente
- Histórico de movimentações exibido

### Fluxo Principal
- **FP-UC02-001:** Usuário seleciona ativo na listagem
- **FP-UC02-002:** Sistema valida permissão `FIN.ATIVOS.VIEW`
- **FP-UC02-003:** Sistema valida que ativo pertence ao tenant do usuário
- **FP-UC02-004:** Sistema carrega dados completos do ativo
- **FP-UC02-005:** Sistema carrega histórico de movimentações (chain of custody)
- **FP-UC02-006:** Sistema carrega anexos (fotos, NFs, laudos)
- **FP-UC02-007:** Sistema exibe QR Code do ativo
- **FP-UC02-008:** Sistema exibe dados de auditoria (Created, LastModified)

### Fluxos Alternativos
- **FA-UC02-001:** Imprimir QR Code individual (botão "Imprimir QR")
- **FA-UC02-002:** Visualizar ativo via scan QR Code (mobile app)
- **FA-UC02-003:** Editar ativo (redireciona para UC03)
- **FA-UC02-004:** Alocar ativo (redireciona para UC05)

### Fluxos de Exceção
- **FE-UC02-001:** Ativo não encontrado → HTTP 404 Not Found
- **FE-UC02-002:** Ativo de outro tenant → HTTP 403 Forbidden
- **FE-UC02-003:** Erro ao carregar dados → exibe mensagem e permite retry

### Regras de Negócio
- **RN-UC02-001:** Isolamento por tenant obrigatório (RN-RF025-012)
- **RN-UC02-002:** Histórico de movimentações imutável (RN-RF025-005)
- **RN-UC02-003:** Auditoria completa visível

### Critérios de Aceite
- **CA-UC02-001:** Usuário SÓ pode visualizar ativos do próprio tenant
- **CA-UC02-002:** Histórico de movimentações DEVE ser exibido em ordem cronológica inversa
- **CA-UC02-003:** QR Code DEVE ser exibido e permitir impressão
- **CA-UC02-004:** Dados de auditoria DEVEM estar visíveis
- **CA-UC02-005:** Tentativa de acessar ativo de outro tenant DEVE retornar 403

---

## UC03 — Editar Ativo

### Objetivo
Permitir alteração controlada de dados de um ativo existente.

### Pré-condições
- Usuário autenticado
- Permissão `FIN.ATIVOS.UPDATE`

### Pós-condições
- Ativo atualizado
- Auditoria registrada (LastModified, LastModifiedBy)

### Fluxo Principal
- **FP-UC03-001:** Usuário solicita edição de ativo
- **FP-UC03-002:** Sistema valida permissão `FIN.ATIVOS.UPDATE`
- **FP-UC03-003:** Sistema valida que ativo pertence ao tenant
- **FP-UC03-004:** Sistema carrega dados atuais do ativo
- **FP-UC03-005:** Usuário altera dados (exceto Número Patrimônio e QR Code)
- **FP-UC03-006:** Sistema valida alterações (FluentValidation)
- **FP-UC03-007:** Sistema persiste alterações
- **FP-UC03-008:** Sistema atualiza LastModified e LastModifiedBy
- **FP-UC03-009:** Sistema registra auditoria
- **FP-UC03-010:** Sistema exibe mensagem de sucesso

### Fluxos Alternativos
- **FA-UC03-001:** Cancelar edição (botão "Cancelar")
- **FA-UC03-002:** Upload de novo anexo

### Fluxos de Exceção
- **FE-UC03-001:** Erro de validação → exibe erros por campo
- **FE-UC03-002:** Conflito de edição concorrente → exibe alerta
- **FE-UC03-003:** Tentativa de editar Número Patrimônio → bloqueado (campo readonly)
- **FE-UC03-004:** Tentativa de editar ativo de outro tenant → HTTP 403

### Regras de Negócio
- **RN-UC03-001:** LastModified e LastModifiedBy automáticos
- **RN-UC03-002:** Número de Patrimônio e QR Code são imutáveis
- **RN-UC03-003:** Validação de campos obrigatórios por tipo
- **RN-UC03-004:** Isolamento por tenant obrigatório

### Critérios de Aceite
- **CA-UC03-001:** LastModified e LastModifiedBy DEVEM ser atualizados automaticamente
- **CA-UC03-002:** Número de Patrimônio NÃO pode ser editado
- **CA-UC03-003:** QR Code NÃO pode ser editado
- **CA-UC03-004:** Validação DEVE respeitar campos obrigatórios por tipo
- **CA-UC03-005:** Tentativa de editar ativo de outro tenant DEVE retornar 403

---

## UC04 — Excluir Ativo

### Objetivo
Permitir exclusão lógica (soft delete) de ativos.

### Pré-condições
- Usuário autenticado
- Permissão `FIN.ATIVOS.DELETE`

### Pós-condições
- Ativo marcado como excluído (Fl_Ativo=FALSE)
- Auditoria registrada

### Fluxo Principal
- **FP-UC04-001:** Usuário solicita exclusão de ativo
- **FP-UC04-002:** Sistema exige confirmação explícita
- **FP-UC04-003:** Sistema valida permissão `FIN.ATIVOS.DELETE`
- **FP-UC04-004:** Sistema verifica dependências ativas
- **FP-UC04-005:** Sistema executa soft delete (Fl_Ativo=FALSE)
- **FP-UC04-006:** Sistema registra auditoria
- **FP-UC04-007:** Sistema exibe mensagem de sucesso

### Fluxos Alternativos
- **FA-UC04-001:** Cancelar exclusão (botão "Cancelar" no modal)
- **FA-UC04-002:** Reativar ativo soft-deleted (apenas Admin)

### Fluxos de Exceção
- **FE-UC04-001:** Ativo possui dependências ativas → HTTP 400 Bad Request
- **FE-UC04-002:** Ativo já excluído → HTTP 410 Gone
- **FE-UC04-003:** Tentativa de DELETE físico → bloqueado pelo sistema

### Regras de Negócio
- **RN-UC04-001:** Exclusão sempre lógica (RN-RF025-013)
- **RN-UC04-002:** Verificação de dependências obrigatória
- **RN-UC04-003:** Confirmação explícita obrigatória
- **RN-UC04-004:** DELETE físico proibido

### Critérios de Aceite
- **CA-UC04-001:** Exclusão DEVE ser sempre lógica (soft delete)
- **CA-UC04-002:** Sistema DEVE verificar dependências ANTES de permitir exclusão
- **CA-UC04-003:** Sistema DEVE exigir confirmação explícita
- **CA-UC04-004:** DELETE físico NUNCA deve ser executado
- **CA-UC04-005:** Ativo excluído NÃO deve aparecer em listagens padrão

---

## UC05 — Alocar Ativo

### Objetivo
Alocar ativo a um usuário responsável com geração de termo de responsabilidade digital.

### Pré-condições
- Usuário autenticado
- Permissão `FIN.ATIVOS.ALOCAR`
- Ativo com status "Disponivel" ou "Reservado"

### Pós-condições
- Ativo com status "Alocado"
- Id_Usuario_Responsavel preenchido
- Termo de responsabilidade gerado e enviado
- Movimentação registrada em histórico

### Fluxo Principal
- **FP-UC05-001:** Usuário seleciona ativo e clica em "Alocar"
- **FP-UC05-002:** Sistema valida permissão `FIN.ATIVOS.ALOCAR`
- **FP-UC05-003:** Sistema valida status atual (Disponivel ou Reservado)
- **FP-UC05-004:** Sistema exibe formulário solicitando Id_Usuario_Responsavel
- **FP-UC05-005:** Usuário seleciona responsável
- **FP-UC05-006:** Sistema valida transição Disponivel → Alocado (RN-RF025-003)
- **FP-UC05-007:** Sistema atualiza status para "Alocado"
- **FP-UC05-008:** Sistema preenche Id_Usuario_Responsavel
- **FP-UC05-009:** Sistema registra movimentação em Ativo_Movimentacao
- **FP-UC05-010:** Sistema gera Termo de Responsabilidade digital (DocuSign/Clicksign)
- **FP-UC05-011:** Sistema envia email/push para usuário responsável com termo
- **FP-UC05-012:** Sistema exibe mensagem de sucesso

### Fluxos Alternativos
- **FA-UC05-001:** Cancelar alocação
- **FA-UC05-002:** Capturar GPS da localização atual (se mobile app)

### Fluxos de Exceção
- **FE-UC05-001:** Ativo não está disponível → HTTP 400 Bad Request
- **FE-UC05-002:** Transição de status inválida → HTTP 400 Bad Request
- **FE-UC05-003:** Usuário responsável não informado → HTTP 400 Bad Request
- **FE-UC05-004:** Falha ao gerar termo → loga erro mas permite alocação

### Regras de Negócio
- **RN-UC05-001:** Alocação requer usuário responsável obrigatório (RN-RF025-004)
- **RN-UC05-002:** Transições de status válidas (RN-RF025-003)
- **RN-UC05-003:** Histórico de movimentação imutável (RN-RF025-005)
- **RN-UC05-004:** Termo de responsabilidade obrigatório

### Critérios de Aceite
- **CA-UC05-001:** Id_Usuario_Responsavel DEVE ser obrigatório
- **CA-UC05-002:** Status DEVE ser alterado para "Alocado"
- **CA-UC05-003:** Movimentação DEVE ser registrada em Ativo_Movimentacao
- **CA-UC05-004:** Termo de responsabilidade DEVE ser enviado ao responsável
- **CA-UC05-005:** Transição de status DEVE ser validada

---

## UC06 — Transferir Ativo

### Objetivo
Transferir ativo entre localizações com captura de geolocalização GPS.

### Pré-condições
- Usuário autenticado
- Permissão `FIN.ATIVOS.TRANSFERIR`

### Pós-condições
- Ativo movido para nova localização
- GPS capturado (se mobile app)
- Movimentação registrada

### Fluxo Principal
- **FP-UC06-001:** Usuário seleciona ativo e clica em "Transferir"
- **FP-UC06-002:** Sistema valida permissão `FIN.ATIVOS.TRANSFERIR`
- **FP-UC06-003:** Sistema exibe formulário com Localização Destino
- **FP-UC06-004:** Usuário seleciona nova localização (hierarquia: Edifício → Andar → Sala)
- **FP-UC06-005:** Sistema captura GPS (latitude/longitude) se mobile app
- **FP-UC06-006:** Sistema valida precisão GPS (<= 20 metros) se mobile
- **FP-UC06-007:** Sistema registra movimentação em Ativo_Movimentacao
- **FP-UC06-008:** Sistema atualiza Id_Localizacao
- **FP-UC06-009:** Sistema exibe mensagem de sucesso

### Fluxos Alternativos
- **FA-UC06-001:** Cancelar transferência
- **FA-UC06-002:** Informar localização manual (web desktop) → marca InventarioRemoto=TRUE

### Fluxos de Exceção
- **FE-UC06-001:** GPS desabilitado (mobile) → exibe erro e bloqueia
- **FE-UC06-002:** Precisão GPS > 20m → exige aguardar sinal melhor
- **FE-UC06-003:** Localização destino não informada → HTTP 400 Bad Request

### Regras de Negócio
- **RN-UC06-001:** Histórico de movimentação imutável (RN-RF025-005)
- **RN-UC06-002:** GPS obrigatório para mobile app (RN-RF025-009)
- **RN-UC06-003:** Flag InventarioRemoto para transferências web

### Critérios de Aceite
- **CA-UC06-001:** Movimentação DEVE ser registrada em Ativo_Movimentacao
- **CA-UC06-002:** GPS DEVE ser capturado se mobile app
- **CA-UC06-003:** Precisão GPS DEVE ser <= 20 metros
- **CA-UC06-004:** Flag InventarioRemoto DEVE ser TRUE se web desktop

---

## UC07 — Devolver Ativo

### Objetivo
Devolver ativo alocado, liberando-o para reuso.

### Pré-condições
- Usuário autenticado
- Permissão `FIN.ATIVOS.DEVOLVER`
- Ativo com status "Alocado"

### Pós-condições
- Ativo com status "Disponivel"
- Id_Usuario_Responsavel limpo (NULL)
- Movimentação registrada

### Fluxo Principal
- **FP-UC07-001:** Usuário seleciona ativo alocado e clica em "Devolver"
- **FP-UC07-002:** Sistema valida permissão `FIN.ATIVOS.DEVOLVER`
- **FP-UC07-003:** Sistema valida status atual "Alocado"
- **FP-UC07-004:** Sistema exibe checklist de devolução (estado físico, acessórios)
- **FP-UC07-005:** Usuário preenche checklist
- **FP-UC07-006:** Sistema valida transição Alocado → Disponivel
- **FP-UC07-007:** Sistema atualiza status para "Disponivel"
- **FP-UC07-008:** Sistema limpa Id_Usuario_Responsavel (NULL)
- **FP-UC07-009:** Sistema registra movimentação em Ativo_Movimentacao
- **FP-UC07-010:** Sistema exibe mensagem de sucesso

### Fluxos Alternativos
- **FA-UC07-001:** Cancelar devolução
- **FA-UC07-002:** Ativo retorna com defeito → envia para manutenção (UC08)

### Fluxos de Exceção
- **FE-UC07-001:** Ativo não está alocado → HTTP 400 Bad Request
- **FE-UC07-002:** Transição de status inválida → HTTP 400 Bad Request

### Regras de Negócio
- **RN-UC07-001:** Devolução limpa Id_Usuario_Responsavel automaticamente
- **RN-UC07-002:** Transições de status válidas (RN-RF025-003)
- **RN-UC07-003:** Histórico de movimentação imutável

### Critérios de Aceite
- **CA-UC07-001:** Id_Usuario_Responsavel DEVE ser limpo (NULL) automaticamente
- **CA-UC07-002:** Status DEVE ser alterado para "Disponivel"
- **CA-UC07-003:** Movimentação DEVE ser registrada
- **CA-UC07-004:** Checklist de devolução DEVE ser preenchido

---

## UC08 — Enviar para Manutenção

### Objetivo
Alterar status do ativo para "Manutencao" e registrar motivo.

### Pré-condições
- Usuário autenticado
- Permissão `FIN.ATIVOS.MANUTENCAO`

### Pós-condições
- Ativo com status "Manutencao"
- Motivo registrado
- Movimentação registrada

### Fluxo Principal
- **FP-UC08-001:** Usuário seleciona ativo e clica em "Enviar para Manutenção"
- **FP-UC08-002:** Sistema valida permissão `FIN.ATIVOS.MANUTENCAO`
- **FP-UC08-003:** Sistema valida status atual (Disponivel ou Alocado)
- **FP-UC08-004:** Sistema exibe formulário solicitando motivo
- **FP-UC08-005:** Usuário informa motivo (preventiva, corretiva, sinistro)
- **FP-UC08-006:** Sistema valida transição para "Manutencao"
- **FP-UC08-007:** Sistema atualiza status para "Manutencao"
- **FP-UC08-008:** Sistema registra movimentação com motivo
- **FP-UC08-009:** Sistema exibe mensagem de sucesso

### Fluxos Alternativos
- **FA-UC08-001:** Cancelar envio para manutenção
- **FA-UC08-002:** Upload de laudo técnico

### Fluxos de Exceção
- **FE-UC08-001:** Motivo não informado → HTTP 400 Bad Request
- **FE-UC08-002:** Transição de status inválida → HTTP 400 Bad Request

### Regras de Negócio
- **RN-UC08-001:** Transições de status válidas (RN-RF025-003)
- **RN-UC08-002:** Motivo obrigatório
- **RN-UC08-003:** Histórico de movimentação imutável

### Critérios de Aceite
- **CA-UC08-001:** Status DEVE ser alterado para "Manutencao"
- **CA-UC08-002:** Motivo DEVE ser obrigatório
- **CA-UC08-003:** Movimentação DEVE ser registrada

---

## UC09 — Baixar Ativo

### Objetivo
Realizar baixa patrimonial com workflow de aprovação de 2 níveis.

### Pré-condições
- Usuário autenticado
- Permissão `FIN.ATIVOS.BAIXAR`

### Pós-condições
- Ativo com status "Baixado" (após aprovações)
- Justificativa registrada
- Anexos obrigatórios armazenados
- Workflow de aprovação iniciado

### Fluxo Principal
- **FP-UC09-001:** Usuário seleciona ativo e clica em "Baixar Ativo"
- **FP-UC09-002:** Sistema valida permissão `FIN.ATIVOS.BAIXAR`
- **FP-UC09-003:** Sistema exibe formulário de baixa patrimonial
- **FP-UC09-004:** Usuário informa Justificativa (mínimo 50 caracteres)
- **FP-UC09-005:** Usuário seleciona Motivo (roubo, dano irreparável, alienação)
- **FP-UC09-006:** Usuário anexa documentos obrigatórios (BO, laudo técnico, NF venda)
- **FP-UC09-007:** Sistema valida justificativa (>= 50 chars)
- **FP-UC09-008:** Sistema valida anexos obrigatórios conforme motivo
- **FP-UC09-009:** Sistema inicia workflow de aprovação Nível 1 (Gestor imediato)
- **FP-UC09-010:** Sistema aguarda aprovação Nível 1
- **FP-UC09-011:** Após aprovação Nível 1, sistema inicia Nível 2 (Controller/Financeiro)
- **FP-UC09-012:** Após aprovação Nível 2, sistema atualiza status para "Baixado"
- **FP-UC09-013:** Sistema registra movimentação
- **FP-UC09-014:** Sistema envia evento para ERP (integração)
- **FP-UC09-015:** Sistema exibe mensagem de sucesso

### Fluxos Alternativos
- **FA-UC09-001:** Cancelar baixa (antes de aprovações)
- **FA-UC09-002:** Reprovar no Nível 1 → baixa cancelada
- **FA-UC09-003:** Reprovar no Nível 2 → baixa cancelada

### Fluxos de Exceção
- **FE-UC09-001:** Justificativa com < 50 caracteres → HTTP 400 Bad Request
- **FE-UC09-002:** Anexos obrigatórios ausentes → HTTP 400 Bad Request
- **FE-UC09-003:** Aprovação pendente → status permanece inalterado
- **FE-UC09-004:** Integração ERP falha → retry 3x, se falhar vai para DLQ

### Regras de Negócio
- **RN-UC09-001:** Baixa requer aprovação de 2 níveis (RN-RF025-010)
- **RN-UC09-002:** Justificativa mínima 50 caracteres
- **RN-UC09-003:** Anexos obrigatórios conforme motivo
- **RN-UC09-004:** Estado "Baixado" é irreversível (exceto admin)
- **RN-UC09-005:** Integração com ERP obrigatória

### Critérios de Aceite
- **CA-UC09-001:** Workflow de aprovação DEVE ter 2 níveis
- **CA-UC09-002:** Justificativa DEVE ter mínimo 50 caracteres
- **CA-UC09-003:** Anexos DEVEM ser obrigatórios conforme motivo
- **CA-UC09-004:** Status "Baixado" DEVE ser irreversível
- **CA-UC09-005:** Integração ERP DEVE ser executada após aprovações

---

## UC10 — Inventariar Ativo

### Objetivo
Registrar inventário físico com foto e geolocalização GPS (app mobile).

### Pré-condições
- Usuário autenticado
- Permissão `FIN.ATIVOS.INVENTARIAR`
- App mobile instalado (ou web desktop)

### Pós-condições
- Inventário registrado
- Dt_Ultimo_Inventario atualizada
- Foto armazenada (se capturada)
- GPS armazenado (se mobile)

### Fluxo Principal
- **FP-UC10-001:** Usuário abre app mobile e clica em "Inventariar"
- **FP-UC10-002:** Sistema valida permissão `FIN.ATIVOS.INVENTARIAR`
- **FP-UC10-003:** Usuário escaneia QR Code do ativo
- **FP-UC10-004:** Sistema carrega dados do ativo
- **FP-UC10-005:** Sistema captura GPS (latitude/longitude) obrigatoriamente
- **FP-UC10-006:** Sistema valida precisão GPS (<= 20 metros)
- **FP-UC10-007:** Usuário tira foto do ativo
- **FP-UC10-008:** Usuário confirma estado físico (Bom, Avaria Leve, Avaria Grave)
- **FP-UC10-009:** Sistema registra inventário em Ativo_Inventario
- **FP-UC10-010:** Sistema atualiza Dt_Ultimo_Inventario
- **FP-UC10-011:** Sistema exibe mensagem de sucesso

### Fluxos Alternativos
- **FA-UC10-001:** Inventário via web desktop → permite localização manual (marca InventarioRemoto=TRUE)
- **FA-UC10-002:** Pular foto (opcional)
- **FA-UC10-003:** Registrar observação adicional

### Fluxos de Exceção
- **FE-UC10-001:** GPS desabilitado ou sem sinal → exibe erro e bloqueia
- **FE-UC10-002:** Precisão GPS > 20m → exige aguardar sinal melhor
- **FE-UC10-003:** QR Code inválido → exibe erro
- **FE-UC10-004:** Ativo não encontrado → HTTP 404 Not Found

### Regras de Negócio
- **RN-UC10-001:** GPS obrigatório para mobile app (RN-RF025-009)
- **RN-UC10-002:** Precisão GPS <= 20 metros
- **RN-UC10-003:** Inventário periódico obrigatório conforme valor (RN-RF025-015)
- **RN-UC10-004:** Flag InventarioRemoto para inventários web

### Critérios de Aceite
- **CA-UC10-001:** GPS DEVE ser capturado obrigatoriamente em mobile app
- **CA-UC10-002:** Precisão GPS DEVE ser <= 20 metros
- **CA-UC10-003:** Dt_Ultimo_Inventario DEVE ser atualizada
- **CA-UC10-004:** Foto DEVE ser armazenada se capturada
- **CA-UC10-005:** Flag InventarioRemoto=TRUE se inventário web

---

## UC11 — Consultar Histórico de Movimentações

### Objetivo
Visualizar timeline completa de movimentações de um ativo (chain of custody).

### Pré-condições
- Usuário autenticado
- Permissão `FIN.ATIVOS.HISTORICO`

### Pós-condições
- Histórico exibido em ordem cronológica inversa

### Fluxo Principal
- **FP-UC11-001:** Usuário seleciona ativo e clica em "Histórico"
- **FP-UC11-002:** Sistema valida permissão `FIN.ATIVOS.HISTORICO`
- **FP-UC11-003:** Sistema carrega todas as movimentações da tabela Ativo_Movimentacao
- **FP-UC11-004:** Sistema ordena por Data_Movimentacao DESC
- **FP-UC11-005:** Sistema exibe timeline com: Tipo, Status Origem → Destino, Responsável, Localização, Justificativa, GPS
- **FP-UC11-006:** Sistema exibe quem executou cada movimentação

### Fluxos Alternativos
- **FA-UC11-001:** Filtrar por Tipo de Movimentação
- **FA-UC11-002:** Filtrar por período (Data Início/Fim)
- **FA-UC11-003:** Exportar histórico em PDF/Excel

### Fluxos de Exceção
- **FE-UC11-001:** Ativo sem movimentações → exibe mensagem "Nenhuma movimentação registrada"
- **FE-UC11-002:** Erro ao carregar → exibe mensagem e permite retry

### Regras de Negócio
- **RN-UC11-001:** Histórico imutável (RN-RF025-005)
- **RN-UC11-002:** Registros NUNCA podem ser editados/deletados
- **RN-UC11-003:** Timeline completa (chain of custody)

### Critérios de Aceite
- **CA-UC11-001:** Histórico DEVE ser imutável
- **CA-UC11-002:** Movimentações DEVEM ser ordenadas cronologicamente
- **CA-UC11-003:** Registros NUNCA devem ser editados/deletados
- **CA-UC11-004:** GPS DEVE ser exibido se capturado

---

## UC12 — Gerar QR Code em Lote

### Objetivo
Gerar PDF com múltiplos QR Codes para impressão em lote de etiquetas.

### Pré-condições
- Usuário autenticado
- Permissão `FIN.ATIVOS.GERAR_QR`

### Pós-condições
- PDF gerado com QR Codes 300x300px
- Etiquetas prontas para impressão

### Fluxo Principal
- **FP-UC12-001:** Usuário seleciona múltiplos ativos na listagem
- **FP-UC12-002:** Usuário clica em "Gerar QR Codes em Lote"
- **FP-UC12-003:** Sistema valida permissão `FIN.ATIVOS.GERAR_QR`
- **FP-UC12-004:** Sistema gera PDF com QR Codes 300x300px (correção erro High)
- **FP-UC12-005:** Sistema inclui Número de Patrimônio abaixo de cada QR Code
- **FP-UC12-006:** Sistema formata PDF para impressora Zebra ZD421 (etiquetas 30x30mm)
- **FP-UC12-007:** Sistema disponibiliza download do PDF
- **FP-UC12-008:** Sistema registra geração em log

### Fluxos Alternativos
- **FA-UC12-001:** Gerar QR Code individual (apenas 1 ativo)
- **FA-UC12-002:** Selecionar todos os ativos da listagem

### Fluxos de Exceção
- **FE-UC12-001:** Nenhum ativo selecionado → exibe alerta
- **FE-UC12-002:** Erro ao gerar PDF → exibe mensagem e permite retry

### Regras de Negócio
- **RN-UC12-001:** QR Code 300x300px (RN-RF025-002)
- **RN-UC12-002:** Correção de erro nível High (30% danificado funciona)
- **RN-UC12-003:** Formato para impressora Zebra ZD421

### Critérios de Aceite
- **CA-UC12-001:** PDF DEVE conter QR Codes 300x300px
- **CA-UC12-002:** Correção de erro DEVE ser nível High
- **CA-UC12-003:** Número de Patrimônio DEVE ser exibido
- **CA-UC12-004:** Formato DEVE ser compatível com Zebra ZD421

---

## UC13 — Visualizar Dashboard Executivo

### Objetivo
Exibir gráficos em tempo real sobre ativos (por status, tipo, taxa de utilização).

### Pré-condições
- Usuário autenticado
- Permissão `FIN.ATIVOS.DASHBOARD`

### Pós-condições
- Dashboard exibido com gráficos atualizados

### Fluxo Principal
- **FP-UC13-001:** Usuário acessa Dashboard via menu
- **FP-UC13-002:** Sistema valida permissão `FIN.ATIVOS.DASHBOARD`
- **FP-UC13-003:** Sistema carrega dados agregados (cache 5 min)
- **FP-UC13-004:** Sistema exibe gráfico "Ativos por Status" (Pizza Chart.js)
- **FP-UC13-005:** Sistema exibe gráfico "Ativos por Tipo" (Barra Chart.js)
- **FP-UC13-006:** Sistema exibe gráfico "Taxa de Utilização" (Linha Chart.js)
- **FP-UC13-007:** Sistema exibe "Top 10 Ativos Mais Caros" (Tabela)
- **FP-UC13-008:** Sistema exibe contador de "Ativos Atrasados para Inventário" (semáforo)
- **FP-UC13-009:** Sistema exibe alertas de garantia próximos (30/60/90 dias)

### Fluxos Alternativos
- **FA-UC13-001:** Filtrar por período (Mês, Trimestre, Ano)
- **FA-UC13-002:** Exportar gráficos em PNG
- **FA-UC13-003:** Atualizar dados manualmente (botão "Atualizar")

### Fluxos de Exceção
- **FE-UC13-001:** Erro ao carregar dados → exibe mensagem e permite retry
- **FE-UC13-002:** Nenhum dado disponível → exibe estado vazio

### Regras de Negócio
- **RN-UC13-001:** Cache de 5 minutos para otimização
- **RN-UC13-002:** Dados agregados por tenant
- **RN-UC13-003:** Gráficos Chart.js

### Critérios de Aceite
- **CA-UC13-001:** Dashboard DEVE exibir dados em tempo real (cache 5 min)
- **CA-UC13-002:** Gráficos DEVEM usar Chart.js
- **CA-UC13-003:** Isolamento por tenant obrigatório
- **CA-UC13-004:** Semáforo de inventário atrasado DEVE ser exibido

---

## UC14 — Calcular Depreciação Mensal (Job)

### Objetivo
Job Hangfire executado automaticamente TODO mês para calcular depreciação de ativos.

### Pré-condições
- Job configurado para executar dia 1 do mês às 02:00 UTC
- Ativos com Dt_Aquisicao preenchida

### Pós-condições
- Valor_Atual_Depreciado atualizado
- Dt_Ultima_Depreciacao atualizada
- Registro em Ativo_Depreciacao
- Integração ERP executada

### Fluxo Principal
- **FP-UC14-001:** Job Hangfire inicia execução no dia 1 do mês às 02:00 UTC
- **FP-UC14-002:** Sistema carrega ativos com Dt_Aquisicao preenchida
- **FP-UC14-003:** Para cada ativo, sistema identifica método de depreciação (Linear, Acelerada, Soma_Digitos)
- **FP-UC14-004:** Sistema calcula depreciação mensal conforme método
- **FP-UC14-005:** Sistema atualiza Valor_Atual_Depreciado
- **FP-UC14-006:** Sistema atualiza Dt_Ultima_Depreciacao
- **FP-UC14-007:** Sistema registra cálculo em Ativo_Depreciacao
- **FP-UC14-008:** Sistema envia lançamento contábil para ERP via API REST
- **FP-UC14-009:** Se falha na integração ERP, sistema executa retry 3x (backoff 2s, 4s, 8s)
- **FP-UC14-010:** Se falha após 3 tentativas, sistema envia para DLQ (RabbitMQ)
- **FP-UC14-011:** Sistema registra log de execução

### Fluxos Alternativos
- **FA-UC14-001:** Executar cálculo manual (apenas Admin)
- **FA-UC14-002:** Recalcular depreciação retroativa

### Fluxos de Exceção
- **FE-UC14-001:** Falha ao calcular → loga erro e continua próximo ativo
- **FE-UC14-002:** Integração ERP falha 3x → envia para DLQ
- **FE-UC14-003:** Job travou → alerta enviado para equipe técnica

### Regras de Negócio
- **RN-UC14-001:** Depreciação automática mensal (RN-RF025-006)
- **RN-UC14-002:** 3 métodos suportados (Linear, Acelerada, Soma_Digitos)
- **RN-UC14-003:** Integração ERP com retry 3x
- **RN-UC14-004:** DLQ para eventos não sincronizados

### Critérios de Aceite
- **CA-UC14-001:** Job DEVE executar dia 1 do mês às 02:00 UTC
- **CA-UC14-002:** Valor_Atual_Depreciado DEVE ser atualizado
- **CA-UC14-003:** Integração ERP DEVE ter retry 3x
- **CA-UC14-004:** Eventos falhos DEVEM ir para DLQ

---

## UC15 — Enviar Alertas de Garantia (Job)

### Objetivo
Job Hangfire executado DIARIAMENTE para verificar garantias vencendo e enviar notificações.

### Pré-condições
- Job configurado para executar diariamente às 08:00 UTC
- Ativos com Dt_Garantia_Fim preenchida

### Pós-condições
- Notificações enviadas (email/push/in-app)
- Registro em Ativo_Garantia_Alerta (prevenir duplicatas)
- Alerta exibido no dashboard

### Fluxo Principal
- **FP-UC15-001:** Job Hangfire inicia execução diariamente às 08:00 UTC
- **FP-UC15-002:** Sistema carrega ativos com Dt_Garantia_Fim nos próximos 90, 60 ou 30 dias
- **FP-UC15-003:** Sistema verifica em Ativo_Garantia_Alerta se notificação já foi enviada
- **FP-UC15-004:** Para garantias vencendo em 90 dias: envia Email para gestor de TI
- **FP-UC15-005:** Para garantias vencendo em 60 dias: envia Email + Push para responsável + gestor
- **FP-UC15-006:** Para garantias vencendo em 30 dias: envia Email + Push + In-App + alerta no dashboard
- **FP-UC15-007:** Sistema registra notificação em Ativo_Garantia_Alerta
- **FP-UC15-008:** Sistema registra log de execução

### Fluxos Alternativos
- **FA-UC15-001:** Executar envio manual (apenas Admin)
- **FA-UC15-002:** Reenviar alerta para um ativo específico

### Fluxos de Exceção
- **FE-UC15-001:** Falha ao enviar email → retry 2x
- **FE-UC15-002:** Falha ao enviar push → loga erro e continua
- **FE-UC15-003:** Job travou → alerta enviado para equipe técnica

### Regras de Negócio
- **RN-UC15-001:** Alertas automáticos 30/60/90 dias (RN-RF025-007)
- **RN-UC15-002:** Notificações registradas para evitar duplicatas
- **RN-UC15-003:** Canais de notificação variam por período
- **RN-UC15-004:** Alerta exibido no dashboard

### Critérios de Aceite
- **CA-UC15-001:** Job DEVE executar diariamente às 08:00 UTC
- **CA-UC15-002:** Notificações DEVEM ser enviadas apenas uma vez por período
- **CA-UC15-003:** Canais de notificação DEVEM variar: 90d (Email), 60d (Email+Push), 30d (Email+Push+In-App+Dashboard)
- **CA-UC15-004:** Alerta DEVE ser exibido no dashboard

---

## 4. MATRIZ DE RASTREABILIDADE

| UC | Regras de Negócio RF | Funcionalidades RF |
|----|----------------------|--------------------|
| UC00 | RN-RF025-012, RN-RF025-013 | RF-CRUD-02 |
| UC01 | RN-RF025-001, RN-RF025-002, RN-RF025-008, RN-RF025-011, RN-RF025-012 | RF-CRUD-01, RF-VAL-01, RF-VAL-03 |
| UC02 | RN-RF025-005, RN-RF025-012 | RF-CRUD-03 |
| UC03 | RN-RF025-008, RN-RF025-012, RN-RF025-013 | RF-CRUD-04 |
| UC04 | RN-RF025-013 | RF-CRUD-05, RF-SEC-03 |
| UC05 | RN-RF025-003, RN-RF025-004, RN-RF025-005 | RF-VAL-02 |
| UC06 | RN-RF025-005, RN-RF025-009 | RF-VAL-05 |
| UC07 | RN-RF025-003, RN-RF025-004, RN-RF025-005 | RF-VAL-02 |
| UC08 | RN-RF025-003, RN-RF025-005 | RF-VAL-02 |
| UC09 | RN-RF025-003, RN-RF025-005, RN-RF025-010, RN-RF025-014 | RF-VAL-02 |
| UC10 | RN-RF025-009, RN-RF025-015 | RF-VAL-05 |
| UC11 | RN-RF025-005 | - |
| UC12 | RN-RF025-002 | - |
| UC13 | RN-RF025-015 | - |
| UC14 | RN-RF025-006, RN-RF025-014 | RF-JOB-01 |
| UC15 | RN-RF025-007 | RF-JOB-02 |

---

## CHANGELOG

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 1.0 | 2025-12-31 | Agência ALC - alc.dev.br | Versão inicial canônica com 16 UCs cobrindo 100% do RF025 |
