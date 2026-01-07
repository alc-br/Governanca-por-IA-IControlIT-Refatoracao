# UC-RF023 — Casos de Uso Canônicos

**RF:** RF023 — Gestão de Contratos
**Fase:** Fase 3 - Financeiro I - Base Contábil
**Epic:** EPIC006-FIN-Financeiro-Base
**Versão:** 2.0
**Data:** 2025-12-31
**Autor:** Agência ALC - alc.dev.br

---

## 1. OBJETIVO DO DOCUMENTO

Este documento descreve **todos os Casos de Uso (UC)** derivados do **RF023 - Gestão de Contratos**, cobrindo integralmente o comportamento funcional esperado.

Os UCs aqui definidos servem como **contrato comportamental**, sendo a **fonte primária** para geração de:
- Casos de Teste (TC-RF023.yaml)
- Massas de Teste (MT-RF023.yaml)
- Evidências de auditoria e validação funcional
- Execução por agentes de IA (tester, QA, E2E)

---

## 2. SUMÁRIO DE CASOS DE USO

| ID | Nome | Ator Principal |
|----|------|----------------|
| UC00 | Listar Contratos | Usuário Autenticado |
| UC01 | Criar Contrato | Gestor/Gerente Contrato |
| UC02 | Visualizar Contrato | Usuário Autenticado |
| UC03 | Editar Contrato | Gerente Contrato |
| UC04 | Excluir Contrato | Admin |
| UC05 | Submeter Contrato para Aprovação | Gerente Contrato |
| UC06 | Aprovar/Rejeitar Contrato | Jurista/Diretor |
| UC07 | Gerenciar Anexos Contratuais | Gerente Contrato |
| UC08 | Renovar Contrato Manualmente | Gerente Contrato |
| UC09 | Simular Reajuste por Índice Econômico | Gestor/Gerente Contrato |

---

## 3. PADRÕES GERAIS APLICÁVEIS A TODOS OS UCs

- Todos os acessos respeitam **isolamento por tenant (ClienteId)**
- Todas as ações exigem **permissão explícita RBAC**
- Erros não devem vazar informações sensíveis
- Auditoria deve registrar **quem**, **quando** e **qual ação**
- Mensagens devem ser claras, previsíveis e rastreáveis
- Soft delete obrigatório: IsDeleted = true (nunca DELETE físico)
- Multi-tenancy: Todas as queries filtram WHERE ClienteId = [usuário autenticado]

---

## UC00 — Listar Contratos

### Objetivo
Permitir que o usuário visualize contratos disponíveis do seu próprio tenant com filtros dinâmicos, paginação e ordenação.

### Pré-condições
- Usuário autenticado
- Permissão `contratos:contratos:read`

### Pós-condições
- Lista exibida conforme filtros e paginação
- Apenas contratos do ClienteId do usuário autenticado

### Fluxo Principal
- **FP-UC00-001:** Usuário acessa "Contratos > Listagem"
- **FP-UC00-002:** Sistema valida permissão `contratos:contratos:read`
- **FP-UC00-003:** Sistema carrega contratos do tenant (WHERE ClienteId = [usuário] AND IsDeleted = false)
- **FP-UC00-004:** Sistema aplica paginação padrão (20 registros/página) e ordenação (DataInicio DESC)
- **FP-UC00-005:** Sistema exibe lista com: Número, Fornecedor, Tipo, Vigência, Valor, Status
- **FP-UC00-006:** Sistema exibe indicadores visuais: Vencimento próximo (⚠️), Ativo (✓), Vencido (❌)

### Fluxos Alternativos
- **FA-UC00-001:** Filtrar por Status (Rascunho, Ativo, Vencido, etc.)
  - Sistema aplica WHERE Status = [filtro selecionado]
- **FA-UC00-002:** Filtrar por Fornecedor
  - Sistema aplica WHERE FornecedorId = [filtro selecionado]
- **FA-UC00-003:** Filtrar por Tipo de Contrato (Compra, Locação, Manutenção, Telecom, Serviço)
  - Sistema aplica WHERE TipoContrato = [filtro selecionado]
- **FA-UC00-004:** Buscar por Número do Contrato
  - Sistema aplica WHERE Numero LIKE '%[termo]%'
- **FA-UC00-005:** Ordenar por Valor Total, Data Início, Data Fim
  - Sistema reordena conforme coluna clicada (ASC/DESC)
- **FA-UC00-006:** Exportar relatório (Excel/PDF)
  - Sistema gera arquivo com contratos filtrados
  - Download automático: `contratos-{timestamp}.xlsx`

### Fluxos de Exceção
- **FE-UC00-001:** Usuário sem permissão `contratos:contratos:read`
  - Sistema retorna HTTP 403 Forbidden
  - Mensagem: "Você não tem permissão para visualizar contratos"
- **FE-UC00-002:** Nenhum contrato encontrado
  - Sistema exibe estado vazio com ícone e mensagem
  - Mensagem: "Nenhum contrato encontrado. Crie o primeiro contrato."
- **FE-UC00-003:** Erro ao carregar dados
  - Sistema exibe mensagem de erro genérica
  - Mensagem: "Erro ao carregar contratos. Tente novamente."

### Regras de Negócio
- **RN-UC00-001:** Somente contratos do tenant do usuário autenticado (RN-CTR-023-09)
- **RN-UC00-002:** Contratos soft-deleted (IsDeleted = true) não aparecem (RN-CTR-023-10)
- **RN-UC00-003:** Paginação padrão: 20 registros por página
- **RN-UC00-004:** Ordenação padrão: DataInicio DESC (mais recentes primeiro)

### Critérios de Aceite
- **CA-UC00-001:** A lista DEVE exibir apenas contratos do tenant do usuário autenticado
- **CA-UC00-002:** Contratos excluídos (soft delete) NÃO devem aparecer na listagem
- **CA-UC00-003:** Paginação DEVE ser aplicada com limite padrão de 20 registros
- **CA-UC00-004:** Sistema DEVE permitir ordenação por qualquer coluna visível
- **CA-UC00-005:** Filtros DEVEM ser acumuláveis (Status + Fornecedor simultaneamente)
- **CA-UC00-006:** Indicadores visuais DEVEM alertar contratos próximos de vencer (30 dias)
- **CA-UC00-007:** Exportação DEVE incluir TODOS os contratos filtrados, não apenas página atual

---

## UC01 — Criar Contrato

### Objetivo
Permitir criação de novo contrato com validações completas de dados, vigência, fornecedor e valores.

### Pré-condições
- Usuário autenticado
- Permissão `contratos:contratos:create`
- Fornecedor cadastrado e ativo (FK para RF022)

### Pós-condições
- Contrato persistido com Status = "Rascunho"
- Auditoria registrada (CTR_CONTRATO_CREATE)
- ClienteId preenchido automaticamente

### Fluxo Principal
- **FP-UC01-001:** Usuário clica em "Novo Contrato"
- **FP-UC01-002:** Sistema valida permissão `contratos:contratos:create`
- **FP-UC01-003:** Sistema exibe formulário vazio
- **FP-UC01-004:** Usuário preenche dados obrigatórios:
  - Número do Contrato (único por ClienteId)
  - Fornecedor (dropdown com fornecedores ativos)
  - Tipo de Contrato (Compra, Locação, Manutenção, Telecom, Serviço)
  - Descrição
  - Data Início
  - Data Fim
  - Valor Total OU Valor Mensal
  - Moeda (BRL, USD, EUR)
- **FP-UC01-005:** Sistema valida dados conforme RN-CTR-023-01 (DataFim > DataInicio)
- **FP-UC01-006:** Sistema valida fornecedor conforme RN-CTR-023-08 (CNPJ válido, fornecedor ativo)
- **FP-UC01-007:** Sistema calcula ValorMensal automaticamente conforme RN-CTR-023-02
- **FP-UC01-008:** Sistema cria contrato com Status = "Rascunho", ClienteId automático
- **FP-UC01-009:** Sistema registra auditoria (CTR_CONTRATO_CREATE)
- **FP-UC01-010:** Sistema exibe mensagem de sucesso e redireciona para visualização

### Fluxos Alternativos
- **FA-UC01-001:** Informar Valor Mensal ao invés de Valor Total
  - Sistema recalcula ValorTotal = ValorMensal * meses de vigência
- **FA-UC01-002:** Marcar "Renovação Automática"
  - Campo RenovacaoAutomatica = true
  - Sistema exibe aviso: "Contrato será renovado automaticamente ao vencimento"
- **FA-UC01-003:** Definir Índice de Reajuste (IGPM, IPCA, INPC)
  - Campo IndiceReajuste preenchido
  - Sistema exibe aviso: "Reajuste será aplicado anualmente na data de aniversário"
- **FA-UC01-004:** Salvar e Submeter para Aprovação
  - Sistema executa UC05 automaticamente após salvar
- **FA-UC01-005:** Cancelar criação
  - Sistema descarta dados e retorna para listagem

### Fluxos de Exceção
- **FE-UC01-001:** Número de Contrato duplicado
  - Sistema retorna HTTP 400 Bad Request
  - Mensagem: "Já existe um contrato com o número '{Numero}'"
- **FE-UC01-002:** DataFim <= DataInicio
  - Sistema retorna HTTP 400 Bad Request
  - Mensagem: "Data de término deve ser maior que data de início"
- **FE-UC01-003:** Vigência > 10 anos
  - Sistema retorna HTTP 400 Bad Request
  - Mensagem: "Vigência não pode exceder 10 anos"
- **FE-UC01-004:** Fornecedor inexistente ou inativo
  - Sistema retorna HTTP 400 Bad Request
  - Mensagem: "Fornecedor '{Nome}' está inativo ou não existe"
- **FE-UC01-005:** CNPJ do fornecedor inválido
  - Sistema retorna HTTP 400 Bad Request
  - Mensagem: "CNPJ do fornecedor é inválido"
- **FE-UC01-006:** Valores negativos
  - Sistema retorna HTTP 400 Bad Request
  - Mensagem: "Valor Total e Valor Mensal devem ser maiores que zero"

### Regras de Negócio
- **RN-UC01-001:** DataFim > DataInicio obrigatório (RN-CTR-023-01)
- **RN-UC01-002:** ValorMensal calculado automaticamente se não informado (RN-CTR-023-02)
- **RN-UC01-003:** Fornecedor válido e ativo obrigatório (RN-CTR-023-08)
- **RN-UC01-004:** ClienteId preenchido automaticamente com tenant do usuário (RN-CTR-023-09)
- **RN-UC01-005:** Status inicial sempre "Rascunho"
- **RN-UC01-006:** Número de contrato único por ClienteId

### Critérios de Aceite
- **CA-UC01-001:** Todos os campos obrigatórios DEVEM ser validados antes de persistir
- **CA-UC01-002:** ClienteId DEVE ser preenchido automaticamente com tenant do usuário autenticado
- **CA-UC01-003:** ValorMensal DEVE ser calculado automaticamente se apenas ValorTotal informado
- **CA-UC01-004:** ValorTotal DEVE ser recalculado se ValorMensal informado
- **CA-UC01-005:** Sistema DEVE retornar erro claro se validação falhar
- **CA-UC01-006:** Auditoria DEVE ser registrada APÓS sucesso da criação
- **CA-UC01-007:** Fornecedor DEVE estar ativo (IsAtivo = true) para ser selecionável
- **CA-UC01-008:** CNPJ do fornecedor DEVE ser validado (dígitos verificadores corretos)

---

## UC02 — Visualizar Contrato

### Objetivo
Permitir visualização detalhada de um contrato com todos os dados, histórico de alterações e anexos.

### Pré-condições
- Usuário autenticado
- Permissão `contratos:contratos:read`
- Contrato existe e pertence ao ClienteId do usuário

### Pós-condições
- Dados exibidos corretamente
- Histórico de alterações visível
- Anexos listados

### Fluxo Principal
- **FP-UC02-001:** Usuário seleciona contrato na listagem
- **FP-UC02-002:** Sistema valida permissão `contratos:contratos:read`
- **FP-UC02-003:** Sistema valida que contrato pertence ao ClienteId do usuário (RN-CTR-023-09)
- **FP-UC02-004:** Sistema carrega dados do contrato:
  - Informações gerais (Número, Fornecedor, Tipo, Descrição)
  - Vigência (DataInicio, DataFim, dias restantes)
  - Valores (ValorTotal, ValorMensal, Moeda)
  - Status atual
  - Renovação automática (Sim/Não)
  - Índice de reajuste (se configurado)
- **FP-UC02-005:** Sistema carrega histórico de alterações (ContratoHistorico)
- **FP-UC02-006:** Sistema lista anexos contratuais (ContratoAnexo)
- **FP-UC02-007:** Sistema exibe campos de auditoria: CriadoPor, CriadoEm, AtualizadoPor, AtualizadoEm
- **FP-UC02-008:** Sistema exibe ações disponíveis conforme permissões: Editar, Excluir, Submeter, Renovar

### Fluxos Alternativos
- **FA-UC02-001:** Visualizar Histórico de Alterações
  - Sistema exibe timeline com: Data, Usuário, Campos alterados (before/after)
- **FA-UC02-002:** Download de Anexo
  - Usuário clica em anexo listado
  - Sistema executa UC07 (Download de Anexo)
- **FA-UC02-003:** Editar Contrato
  - Usuário clica em "Editar"
  - Sistema executa UC03
- **FA-UC02-004:** Excluir Contrato
  - Usuário clica em "Excluir"
  - Sistema executa UC04

### Fluxos de Exceção
- **FE-UC02-001:** Contrato inexistente
  - Sistema retorna HTTP 404 Not Found
  - Mensagem: "Contrato não encontrado"
- **FE-UC02-002:** Contrato de outro tenant
  - Sistema retorna HTTP 403 Forbidden
  - Mensagem: "Você não tem permissão para visualizar este contrato"
- **FE-UC02-003:** Contrato soft-deleted
  - Sistema retorna HTTP 404 Not Found
  - Mensagem: "Contrato não encontrado" (não vazar que foi deletado)

### Regras de Negócio
- **RN-UC02-001:** Isolamento por tenant (RN-CTR-023-09)
- **RN-UC02-002:** Auditoria visível (CriadoPor, CriadoEm, AtualizadoPor, AtualizadoEm)
- **RN-UC02-003:** Histórico de alterações exibido em ordem cronológica reversa

### Critérios de Aceite
- **CA-UC02-001:** Usuário SÓ pode visualizar contratos do próprio tenant
- **CA-UC02-002:** Informações de auditoria DEVEM ser exibidas
- **CA-UC02-003:** Tentativa de acessar contrato de outro tenant DEVE retornar HTTP 403
- **CA-UC02-004:** Tentativa de acessar contrato inexistente DEVE retornar HTTP 404
- **CA-UC02-005:** Dados exibidos DEVEM corresponder exatamente ao estado atual no banco
- **CA-UC02-006:** Histórico DEVE mostrar before/after de campos alterados
- **CA-UC02-007:** Anexos DEVEM ser listados com: Nome, Tamanho, Data Upload, Usuário

---

## UC03 — Editar Contrato

### Objetivo
Permitir alteração controlada de contrato existente com validações e auditoria completa.

### Pré-condições
- Usuário autenticado
- Permissão `contratos:contratos:update`
- Contrato existe e pertence ao ClienteId do usuário
- Contrato em status permitido para edição (Rascunho, Rejeitado)

### Pós-condições
- Contrato atualizado
- Histórico de alterações registrado (ContratoHistorico)
- Auditoria registrada (CTR_CONTRATO_UPDATE)

### Fluxo Principal
- **FP-UC03-001:** Usuário clica em "Editar" na visualização do contrato
- **FP-UC03-002:** Sistema valida permissão `contratos:contratos:update`
- **FP-UC03-003:** Sistema valida que Status permite edição (Rascunho OU Rejeitado)
- **FP-UC03-004:** Sistema carrega formulário preenchido com dados atuais
- **FP-UC03-005:** Usuário altera campos desejados
- **FP-UC03-006:** Sistema valida alterações (RN-CTR-023-01, RN-CTR-023-02, RN-CTR-023-08)
- **FP-UC03-007:** Sistema recalcula ValorMensal/ValorTotal se necessário
- **FP-UC03-008:** Sistema persiste alterações
- **FP-UC03-009:** Sistema registra histórico de alterações (before/after JSON)
- **FP-UC03-010:** Sistema registra auditoria (CTR_CONTRATO_UPDATE)
- **FP-UC03-011:** Sistema exibe mensagem de sucesso

### Fluxos Alternativos
- **FA-UC03-001:** Alterar Valor Total
  - Sistema recalcula ValorMensal automaticamente
- **FA-UC03-002:** Alterar Vigência
  - Sistema recalcula ValorMensal se ValorTotal informado
- **FA-UC03-003:** Alterar Fornecedor
  - Sistema valida novo fornecedor (ativo, CNPJ válido)
- **FA-UC03-004:** Cancelar edição
  - Sistema descarta alterações e retorna para visualização

### Fluxos de Exceção
- **FE-UC03-001:** Contrato em status bloqueado para edição (Aprovado, Ativo, Vencido)
  - Sistema retorna HTTP 400 Bad Request
  - Mensagem: "Contratos em status '{Status}' não podem ser editados"
- **FE-UC03-002:** Erro de validação (DataFim <= DataInicio)
  - Sistema retorna HTTP 400 Bad Request
  - Mensagem conforme erro específico
- **FE-UC03-003:** Fornecedor alterado para inativo
  - Sistema retorna HTTP 400 Bad Request
  - Mensagem: "Fornecedor '{Nome}' está inativo"
- **FE-UC03-004:** Conflito de edição concorrente
  - Sistema retorna HTTP 409 Conflict
  - Mensagem: "Contrato foi alterado por outro usuário. Recarregue a página."

### Regras de Negócio
- **RN-UC03-001:** Apenas contratos em Rascunho ou Rejeitado podem ser editados
- **RN-UC03-002:** Validações de criação aplicam-se também na edição
- **RN-UC03-003:** AtualizadoPor e AtualizadoEm preenchidos automaticamente
- **RN-UC03-004:** Histórico de alterações registra before/after

### Critérios de Aceite
- **CA-UC03-001:** AtualizadoPor DEVE ser preenchido automaticamente com ID do usuário autenticado
- **CA-UC03-002:** AtualizadoEm DEVE ser preenchido automaticamente com timestamp UTC atual
- **CA-UC03-003:** Apenas campos alterados DEVEM ser validados
- **CA-UC03-004:** Sistema DEVE detectar conflitos de edição concorrente
- **CA-UC03-005:** Tentativa de editar contrato de outro tenant DEVE retornar HTTP 403
- **CA-UC03-006:** Histórico DEVE registrar before/after de TODOS os campos alterados
- **CA-UC03-007:** Contratos Aprovados/Ativos NÃO devem ser editáveis

---

## UC04 — Excluir Contrato

### Objetivo
Permitir exclusão lógica (soft delete) de contrato com validação de dependências.

### Pré-condições
- Usuário autenticado
- Permissão `contratos:contratos:delete`
- Contrato existe e pertence ao ClienteId do usuário
- Contrato NÃO possui medições associadas (RF090)

### Pós-condições
- Contrato marcado como excluído (IsDeleted = true)
- Auditoria registrada (CTR_CONTRATO_DELETE)
- Contrato não aparece em listagens padrão

### Fluxo Principal
- **FP-UC04-001:** Usuário clica em "Excluir" na visualização do contrato
- **FP-UC04-002:** Sistema valida permissão `contratos:contratos:delete`
- **FP-UC04-003:** Sistema verifica dependências (medições em RF090)
- **FP-UC04-004:** Sistema exibe modal de confirmação: "Tem certeza que deseja excluir o contrato '{Numero}'?"
- **FP-UC04-005:** Usuário confirma exclusão
- **FP-UC04-006:** Sistema executa soft delete:
  - IsDeleted = true
  - DataDelecao = timestamp UTC atual
  - DeletadoPor = ID do usuário autenticado
- **FP-UC04-007:** Sistema registra auditoria (CTR_CONTRATO_DELETE) com snapshot completo
- **FP-UC04-008:** Sistema exibe mensagem de sucesso e redireciona para listagem

### Fluxos Alternativos
- **FA-UC04-001:** Cancelar exclusão
  - Usuário clica em "Cancelar" no modal
  - Sistema fecha modal e permanece na visualização

### Fluxos de Exceção
- **FE-UC04-001:** Contrato possui medições associadas (RN-CTR-023-06)
  - Sistema retorna HTTP 409 Conflict
  - Mensagem: "Não é possível excluir contrato com {N} medição(ões) associada(s). Valor total: R$ {Valor}"
  - Sugestão: "Exclua as medições primeiro ou contate o suporte"
- **FE-UC04-002:** Contrato já excluído
  - Sistema retorna HTTP 404 Not Found
  - Mensagem: "Contrato não encontrado"
- **FE-UC04-003:** Contrato de outro tenant
  - Sistema retorna HTTP 403 Forbidden
  - Mensagem: "Você não tem permissão para excluir este contrato"

### Regras de Negócio
- **RN-UC04-001:** Exclusão sempre lógica (soft delete) via IsDeleted (RN-CTR-023-10)
- **RN-UC04-002:** Dependências bloqueiam exclusão (RN-CTR-023-06)
- **RN-UC04-003:** Confirmação explícita do usuário obrigatória
- **RN-UC04-004:** Auditoria registra snapshot completo antes da exclusão

### Critérios de Aceite
- **CA-UC04-001:** Exclusão DEVE ser sempre lógica (soft delete) via IsDeleted = true
- **CA-UC04-002:** Sistema DEVE verificar dependências ANTES de permitir exclusão
- **CA-UC04-003:** Sistema DEVE exigir confirmação explícita do usuário
- **CA-UC04-004:** DataDelecao DEVE ser preenchido com timestamp UTC atual
- **CA-UC04-005:** DeletadoPor DEVE ser preenchido com ID do usuário autenticado
- **CA-UC04-006:** Tentativa de excluir contrato com medições DEVE retornar HTTP 409 com mensagem clara
- **CA-UC04-007:** Contrato excluído NÃO deve aparecer em listagens padrão (WHERE IsDeleted = false)
- **CA-UC04-008:** Auditoria DEVE registrar snapshot completo dos dados antes da exclusão

---

## UC05 — Submeter Contrato para Aprovação

### Objetivo
Permitir submissão de contrato para workflow de aprovação baseado em alçadas de valor.

### Pré-condições
- Usuário autenticado
- Permissão `contratos:contratos:update`
- Contrato em status "Rascunho"
- Todos os campos obrigatórios preenchidos

### Pós-condições
- Status alterado para "PendenteAprovacao"
- Próximo aprovador identificado conforme alçada
- Notificação enviada ao aprovador (e-mail + SignalR)
- Auditoria registrada

### Fluxo Principal
- **FP-UC05-001:** Usuário clica em "Submeter para Aprovação"
- **FP-UC05-002:** Sistema valida que Status = "Rascunho"
- **FP-UC05-003:** Sistema valida que todos os campos obrigatórios estão preenchidos
- **FP-UC05-004:** Sistema determina alçada conforme ValorTotal:
  - Até R$5.000 → Gestor
  - R$5.001 - R$50.000 → Jurista
  - Acima de R$50.000 → Diretor/CFO
- **FP-UC05-005:** Sistema identifica usuário aprovador automaticamente
- **FP-UC05-006:** Sistema altera Status para "PendenteAprovacao"
- **FP-UC05-007:** Sistema registra auditoria (CTR_CONTRATO_SUBMIT)
- **FP-UC05-008:** Sistema envia notificação ao aprovador:
  - E-mail: "Contrato '{Numero}' aguarda sua aprovação. Valor: R$ {ValorTotal}"
  - SignalR: Notificação em tempo real no dashboard
- **FP-UC05-009:** Sistema exibe mensagem de sucesso: "Contrato submetido para aprovação de {Aprovador}"

### Fluxos Alternativos
- **FA-UC05-001:** Múltiplos níveis de aprovação
  - Sistema identifica primeiro aprovador na cadeia
  - Após primeira aprovação, encaminha para próximo nível

### Fluxos de Exceção
- **FE-UC05-001:** Contrato não está em Rascunho
  - Sistema retorna HTTP 400 Bad Request
  - Mensagem: "Apenas contratos em Rascunho podem ser submetidos"
- **FE-UC05-002:** Campos obrigatórios faltando
  - Sistema retorna HTTP 400 Bad Request
  - Mensagem: "Preencha todos os campos obrigatórios antes de submeter"
- **FE-UC05-003:** Aprovador não encontrado
  - Sistema retorna HTTP 500 Internal Server Error
  - Mensagem: "Erro ao identificar aprovador. Contate o suporte."

### Regras de Negócio
- **RN-UC05-001:** Apenas contratos em Rascunho podem ser submetidos (RN-CTR-023-05)
- **RN-UC05-002:** Alçada determinada pelo ValorTotal
- **RN-UC05-003:** Notificação obrigatória ao aprovador

### Critérios de Aceite
- **CA-UC05-001:** Sistema DEVE validar Status = "Rascunho" antes de submeter
- **CA-UC05-002:** Sistema DEVE identificar aprovador automaticamente conforme alçada
- **CA-UC05-003:** Notificação DEVE ser enviada via e-mail E SignalR
- **CA-UC05-004:** Status DEVE ser alterado para "PendenteAprovacao"
- **CA-UC05-005:** Auditoria DEVE registrar: usuário que submeteu, aprovador identificado, timestamp

---

## UC06 — Aprovar/Rejeitar Contrato

### Objetivo
Permitir que aprovadores aprovem ou rejeitem contratos conforme alçada de valor.

### Pré-condições
- Usuário autenticado
- Permissão `contratos:contratos:approve` OU `contratos:contratos:reject`
- Contrato em status "PendenteAprovacao"
- Usuário possui alçada para aprovar o valor do contrato

### Pós-condições
- Status alterado para "Aprovado" OU "Rejeitado"
- Justificativa registrada (obrigatória em rejeição)
- Auditoria completa registrada
- Notificação enviada ao criador do contrato

### Fluxo Principal (Aprovação)
- **FP-UC06-001:** Aprovador acessa "Contratos Pendentes"
- **FP-UC06-002:** Sistema lista contratos em "PendenteAprovacao" direcionados ao aprovador
- **FP-UC06-003:** Aprovador clica em "Aprovar"
- **FP-UC06-004:** Sistema valida permissão `contratos:contratos:approve`
- **FP-UC06-005:** Sistema valida alçada do aprovador (ValorTotal <= limite da alçada)
- **FP-UC06-006:** Sistema altera Status para "Aprovado"
- **FP-UC06-007:** Sistema registra: AprovadoPor, DataAprovacao
- **FP-UC06-008:** Sistema registra auditoria (CTR_CONTRATO_APPROVE)
- **FP-UC06-009:** Sistema envia notificação ao criador:
  - E-mail: "Contrato '{Numero}' foi aprovado por {Aprovador}"
  - SignalR: Notificação em tempo real
- **FP-UC06-010:** Sistema exibe mensagem de sucesso

### Fluxo Principal (Rejeição)
- **FP-UC06R-001:** Aprovador clica em "Rejeitar"
- **FP-UC06R-002:** Sistema exibe modal solicitando justificativa (obrigatória)
- **FP-UC06R-003:** Aprovador preenche justificativa
- **FP-UC06R-004:** Sistema valida permissão `contratos:contratos:reject`
- **FP-UC06R-005:** Sistema altera Status para "Rejeitado"
- **FP-UC06R-006:** Sistema registra: RejeitadoPor, DataRejeicao, Justificativa
- **FP-UC06R-007:** Sistema registra auditoria (CTR_CONTRATO_REJECT)
- **FP-UC06R-008:** Sistema envia notificação ao criador:
  - E-mail: "Contrato '{Numero}' foi rejeitado por {Aprovador}. Motivo: {Justificativa}"
  - SignalR: Notificação em tempo real
- **FP-UC06R-009:** Sistema exibe mensagem de sucesso

### Fluxos de Exceção
- **FE-UC06-001:** Aprovador sem alçada para o valor
  - Sistema retorna HTTP 403 Forbidden
  - Mensagem: "Você não possui alçada para aprovar contratos de R$ {ValorTotal}"
- **FE-UC06-002:** Contrato não está em PendenteAprovacao
  - Sistema retorna HTTP 400 Bad Request
  - Mensagem: "Contrato não está pendente de aprovação"
- **FE-UC06-003:** Rejeição sem justificativa
  - Sistema retorna HTTP 400 Bad Request
  - Mensagem: "Justificativa é obrigatória para rejeição"

### Regras de Negócio
- **RN-UC06-001:** Alçada validada conforme ValorTotal (RN-CTR-023-05)
- **RN-UC06-002:** Justificativa obrigatória em rejeição
- **RN-UC06-003:** Notificação obrigatória ao criador

### Critérios de Aceite
- **CA-UC06-001:** Sistema DEVE validar alçada do aprovador antes de permitir aprovação
- **CA-UC06-002:** Justificativa DEVE ser obrigatória em rejeições
- **CA-UC06-003:** Aprovação/Rejeição DEVE registrar: usuário, timestamp, justificativa (se rejeição)
- **CA-UC06-004:** Notificação DEVE ser enviada ao criador do contrato
- **CA-UC06-005:** Auditoria DEVE registrar transição de estado completa

---

## UC07 — Gerenciar Anexos Contratuais

### Objetivo
Permitir upload, download e exclusão de anexos contratuais com versionamento e validação de integridade.

### Pré-condições
- Usuário autenticado
- Permissão `contratos:anexos:upload` (para upload/exclusão)
- Permissão `contratos:anexos:read` (para download)
- Contrato existe e pertence ao ClienteId do usuário

### Pós-condições
- Anexo armazenado com metadata (nome, tamanho, hash CRC32, usuário, timestamp)
- Auditoria registrada (CTR_CONTRATO_ANEXO_UPLOAD)

### Fluxo Principal (Upload)
- **FP-UC07-001:** Usuário acessa visualização do contrato
- **FP-UC07-002:** Usuário clica em "Upload de Anexo"
- **FP-UC07-003:** Sistema exibe modal de upload
- **FP-UC07-004:** Usuário seleciona arquivo (PDF, DOCX, XML, JPG, PNG)
- **FP-UC07-005:** Sistema valida extensão permitida
- **FP-UC07-006:** Sistema valida tamanho máximo (10MB)
- **FP-UC07-007:** Sistema calcula hash CRC32 do arquivo
- **FP-UC07-008:** Sistema armazena arquivo com metadata:
  - Nome original
  - Tamanho em bytes
  - Extensão
  - Hash CRC32
  - UploadPor (usuário)
  - UploadEm (timestamp)
- **FP-UC07-009:** Sistema registra auditoria (CTR_CONTRATO_ANEXO_UPLOAD)
- **FP-UC07-010:** Sistema exibe mensagem de sucesso e atualiza lista de anexos

### Fluxo Principal (Download)
- **FP-UC07D-001:** Usuário clica em anexo listado
- **FP-UC07D-002:** Sistema valida permissão `contratos:anexos:read`
- **FP-UC07D-003:** Sistema recupera arquivo do storage
- **FP-UC07D-004:** Sistema valida integridade (hash CRC32)
- **FP-UC07D-005:** Sistema inicia download com nome original

### Fluxo Principal (Exclusão)
- **FP-UC07E-001:** Usuário clica em "Excluir Anexo"
- **FP-UC07E-002:** Sistema valida permissão `contratos:anexos:upload`
- **FP-UC07E-003:** Sistema exibe modal de confirmação
- **FP-UC07E-004:** Usuário confirma exclusão
- **FP-UC07E-005:** Sistema executa soft delete do anexo
- **FP-UC07E-006:** Sistema registra auditoria
- **FP-UC07E-007:** Sistema exibe mensagem de sucesso

### Fluxos de Exceção
- **FE-UC07-001:** Extensão não permitida
  - Sistema retorna HTTP 400 Bad Request
  - Mensagem: "Extensão '{ext}' não permitida. Use: PDF, DOCX, XML, JPG, PNG"
- **FE-UC07-002:** Arquivo maior que 10MB
  - Sistema retorna HTTP 400 Bad Request
  - Mensagem: "Arquivo maior que 10MB. Tamanho: {tamanho}"
- **FE-UC07-003:** Hash corrompido no download
  - Sistema retorna HTTP 500 Internal Server Error
  - Mensagem: "Arquivo corrompido. Contate o suporte."
  - Notificação enviada ao admin

### Regras de Negócio
- **RN-UC07-001:** Extensões permitidas: PDF, DOCX, XML, JPG, PNG
- **RN-UC07-002:** Tamanho máximo: 10MB
- **RN-UC07-003:** Hash CRC32 calculado e validado

### Critérios de Aceite
- **CA-UC07-001:** Sistema DEVE validar extensão antes de aceitar upload
- **CA-UC07-002:** Sistema DEVE validar tamanho antes de aceitar upload
- **CA-UC07-003:** Hash CRC32 DEVE ser calculado e armazenado
- **CA-UC07-004:** Hash DEVE ser validado em todo download
- **CA-UC07-005:** Anexos DEVEM ter soft delete (IsDeleted)
- **CA-UC07-006:** Metadata DEVE incluir: nome, tamanho, hash, usuário, timestamp

---

## UC08 — Renovar Contrato Manualmente

### Objetivo
Permitir renovação manual de contrato criando novo contrato com vigência estendida.

### Pré-condições
- Usuário autenticado
- Permissão `contratos:renovacao:criar`
- Contrato existe e pertence ao ClienteId do usuário
- Contrato em status "Ativo" ou "Vencido"

### Pós-condições
- Novo contrato criado com DataInicio = DataFim do anterior + 1 dia
- Contrato original alterado para Status = "Renovado"
- Auditoria registrada (CTR_CONTRATO_RENOVACAO)

### Fluxo Principal
- **FP-UC08-001:** Usuário clica em "Renovar Contrato"
- **FP-UC08-002:** Sistema valida permissão `contratos:renovacao:criar`
- **FP-UC08-003:** Sistema valida Status (Ativo OU Vencido)
- **FP-UC08-004:** Sistema exibe modal de renovação com opções:
  - Período de renovação (meses)
  - Manter valores atuais OU Reajustar valores
  - Índice de reajuste (se aplicar)
- **FP-UC08-005:** Usuário preenche período e confirma
- **FP-UC08-006:** Sistema cria novo contrato:
  - DataInicio = DataFim do contrato original + 1 dia
  - DataFim = DataInicio + período informado
  - Número = "{NumeroOriginal}-R{sequencial}"
  - Valores: mantidos OU reajustados conforme índice
  - Status = "Aprovado" (herda aprovação anterior)
  - RenovadoDe = ID do contrato original
- **FP-UC08-007:** Sistema altera contrato original: Status = "Renovado"
- **FP-UC08-008:** Sistema registra auditoria (CTR_CONTRATO_RENOVACAO)
- **FP-UC08-009:** Sistema exibe mensagem de sucesso e redireciona para novo contrato

### Fluxos Alternativos
- **FA-UC08-001:** Reajustar valores na renovação
  - Usuário marca "Reajustar Valores"
  - Usuário informa índice e percentual
  - Sistema recalcula ValorTotal e ValorMensal

### Fluxos de Exceção
- **FE-UC08-001:** Contrato não permite renovação (Status = Rascunho, Cancelado)
  - Sistema retorna HTTP 400 Bad Request
  - Mensagem: "Contratos em status '{Status}' não podem ser renovados"
- **FE-UC08-002:** Período de renovação inválido (0 ou negativo)
  - Sistema retorna HTTP 400 Bad Request
  - Mensagem: "Período de renovação deve ser maior que zero"

### Regras de Negócio
- **RN-UC08-001:** Novo contrato herda aprovações do contrato original
- **RN-UC08-002:** Número do novo contrato segue padrão: {Original}-R{sequencial}
- **RN-UC08-003:** Contrato original marcado como "Renovado" (não pode ser renovado novamente)

### Critérios de Aceite
- **CA-UC08-001:** Novo contrato DEVE ter DataInicio = DataFim do anterior + 1 dia
- **CA-UC08-002:** Número do novo contrato DEVE seguir padrão {Original}-R{sequencial}
- **CA-UC08-003:** Novo contrato DEVE ter Status = "Aprovado" (herda aprovação)
- **CA-UC08-004:** Contrato original DEVE ser marcado como "Renovado"
- **CA-UC08-005:** Auditoria DEVE linkar contrato original e contrato renovado

---

## UC09 — Simular Reajuste por Índice Econômico

### Objetivo
Permitir simulação de reajuste futuro baseado em índices econômicos (IGPM, IPCA, INPC) para planejamento financeiro.

### Pré-condições
- Usuário autenticado
- Permissão `contratos:contratos:read`
- Contrato existe e pertence ao ClienteId do usuário

### Pós-condições
- Projeção de valores futuros exibida
- Nenhuma alteração no contrato (apenas simulação)

### Fluxo Principal
- **FP-UC09-001:** Usuário clica em "Simular Reajuste"
- **FP-UC09-002:** Sistema exibe modal de simulação
- **FP-UC09-003:** Sistema carrega valores atuais (ValorMensal, ValorTotal)
- **FP-UC09-004:** Usuário seleciona índice econômico (IGPM, IPCA, INPC)
- **FP-UC09-005:** Usuário informa percentual de reajuste (ou sistema busca automaticamente do serviço de índices)
- **FP-UC09-006:** Sistema calcula projeção:
  - Novo ValorMensal = ValorMensal atual * (1 + percentual/100)
  - Novo ValorTotal = Novo ValorMensal * meses restantes de vigência
- **FP-UC09-007:** Sistema exibe comparação lado a lado:
  - Valores Atuais | Valores Projetados
  - Diferença em R$ e %
- **FP-UC09-008:** Usuário fecha modal (simulação NÃO altera contrato)

### Fluxos Alternativos
- **FA-UC09-001:** Buscar percentual do índice automaticamente
  - Sistema consome API de serviço de índices econômicos
  - Percentual preenchido automaticamente (ex: IGPM janeiro = 0,5%)

### Fluxos de Exceção
- **FE-UC09-001:** Serviço de índices indisponível
  - Sistema exibe mensagem informativa
  - Mensagem: "Não foi possível buscar índice automaticamente. Informe percentual manualmente."
- **FE-UC09-002:** Percentual inválido (negativo ou > 100%)
  - Sistema retorna erro de validação
  - Mensagem: "Percentual deve estar entre 0% e 100%"

### Regras de Negócio
- **RN-UC09-001:** Simulação NÃO altera contrato (apenas projeção)
- **RN-UC09-002:** Percentual pode ser informado manualmente ou obtido automaticamente

### Critérios de Aceite
- **CA-UC09-001:** Simulação NÃO deve alterar dados do contrato
- **CA-UC09-002:** Sistema DEVE exibir comparação clara: Atual vs Projetado
- **CA-UC09-003:** Percentual DEVE ser validado (0% a 100%)
- **CA-UC09-004:** Sistema DEVE calcular diferença em R$ e %
- **CA-UC09-005:** Busca automática de índice DEVE ser opcional (fallback manual)

---

## 4. MATRIZ DE RASTREABILIDADE

| UC | Regras de Negócio Cobertas |
|----|----------------------------|
| UC00 | RN-CTR-023-09, RN-CTR-023-10 |
| UC01 | RN-CTR-023-01, RN-CTR-023-02, RN-CTR-023-08, RN-CTR-023-09 |
| UC02 | RN-CTR-023-09 |
| UC03 | RN-CTR-023-01, RN-CTR-023-02, RN-CTR-023-08 |
| UC04 | RN-CTR-023-06, RN-CTR-023-09, RN-CTR-023-10 |
| UC05 | RN-CTR-023-05 |
| UC06 | RN-CTR-023-05 |
| UC07 | - |
| UC08 | RN-CTR-023-03 |
| UC09 | RN-CTR-023-07 |

| UC | Funcionalidades Cobertas (RF023) |
|----|----------------------------------|
| UC00 | RF023-CRUD-02 (Listar contratos) |
| UC01 | RF023-CRUD-01 (Criar contrato), RF023-VAL-01, RF023-VAL-02, RF023-VAL-04 |
| UC02 | RF023-CRUD-03 (Visualizar contrato) |
| UC03 | RF023-CRUD-04 (Atualizar contrato) |
| UC04 | RF023-CRUD-05 (Excluir contrato), RF023-VAL-03, RF023-SEC-03 |
| UC05 | RF023-WF-01 (Workflow de aprovação) |
| UC06 | RF023-WF-01 (Workflow de aprovação) |
| UC07 | RF023-CRUD-01 (Gestão de anexos) |
| UC08 | RF023-WF-02 (Renovação) |
| UC09 | RF023-WF-04 (Reajustes) |

---

## CHANGELOG

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 2.0 | 2025-12-31 | Agência ALC - alc.dev.br | Criação completa de UC-RF023 substituindo conteúdo incorreto (RF-090). Cobertura 100% do RF-023 com 10 UCs (UC00-UC09). |
