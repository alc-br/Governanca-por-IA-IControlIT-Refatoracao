# UC-RF022 — Casos de Uso Canônicos

**RF:** RF022 — Gestão de Fornecedores
**Versão:** 2.0
**Data:** 2025-12-31
**Autor:** Agência ALC - alc.dev.br
**Epic:** EPIC003-CAD - Cadastros Base
**Fase:** Fase 2 - Cadastros e Serviços Transversais

---

## 1. OBJETIVO DO DOCUMENTO

Este documento descreve **todos os Casos de Uso (UC)** derivados do **RF022**, cobrindo integralmente o comportamento funcional esperado para a gestão de fornecedores e empresas contratadas.

Os UCs aqui definidos servem como **contrato comportamental**, sendo a **fonte primária** para geração de:
- Casos de Teste (TC-RF022.yaml)
- Massas de Teste (MT-RF022.yaml)
- Evidências de auditoria e validação funcional
- Execução por agentes de IA (tester, QA, E2E)

---

## 2. SUMÁRIO DE CASOS DE USO

| ID | Nome | Ator Principal |
|----|------|----------------|
| UC00 | Listar Fornecedores | Usuário Autenticado |
| UC01 | Criar Fornecedor | Usuário Autenticado |
| UC02 | Visualizar Fornecedor | Usuário Autenticado |
| UC03 | Editar Fornecedor | Usuário Autenticado |
| UC04 | Inativar Fornecedor | Usuário Autenticado |
| UC05 | Validar CNPJ/CPF | Sistema |
| UC06 | Gerenciar Contatos | Usuário Autenticado |
| UC07 | Avaliar Fornecedor | Usuário Autenticado |
| UC08 | Gerenciar Documentos | Usuário Autenticado |
| UC09 | Alertar Vencimentos | Sistema |

---

## 3. PADRÕES GERAIS APLICÁVEIS A TODOS OS UCs

- Todos os acessos respeitam **isolamento por tenant (multi-tenancy)**
- Todas as ações exigem **permissão explícita** (RBAC)
- Erros não devem vazar informações sensíveis
- Auditoria deve registrar **quem**, **quando** e **qual ação**
- Mensagens devem ser claras, previsíveis e rastreáveis
- CNPJ/CPF devem ser validados (dígitos verificadores)
- Validações devem executar no backend (não confiar apenas no frontend)

---

## UC00 — Listar Fornecedores

### Objetivo
Permitir que o usuário visualize e pesquise fornecedores cadastrados do seu tenant com paginação, filtros e ordenação.

### Pré-condições
- Usuário autenticado
- Permissão `fornecedor.read`

### Pós-condições
- Lista exibida conforme filtros e paginação
- Apenas fornecedores do tenant do usuário são exibidos

### Fluxo Principal
- **FP-UC00-001:** Usuário acessa a funcionalidade "Cadastros → Fornecedores"
- **FP-UC00-002:** Sistema valida permissão `fornecedor.read`
- **FP-UC00-003:** Sistema carrega registros do tenant do usuário autenticado
- **FP-UC00-004:** Sistema aplica paginação (padrão 20 itens) e ordenação (padrão: Nome ASC)
- **FP-UC00-005:** Sistema exibe a lista com colunas: Nome, CNPJ/CPF, Tipo, Status, Avaliação, Ações

### Fluxos Alternativos
- **FA-UC00-001:** Buscar por nome parcial (mínimo 3 caracteres, case-insensitive)
- **FA-UC00-002:** Ordenar por coluna clicável (Nome, Tipo, Status, Avaliação)
- **FA-UC00-003:** Filtrar por tipo (dropdown com tipos: OPERADORA_TELECOM, FORNECEDOR_TI, PRESTADOR_SERVICOS, DISTRIBUIDOR, FABRICANTE, OUTROS)
- **FA-UC00-004:** Filtrar por status (dropdown: ATIVO, INATIVO, EM_HOMOLOGACAO, BLOQUEADO)
- **FA-UC00-005:** Buscar por CNPJ/CPF completo ou parcial
- **FA-UC00-006:** Navegar entre páginas (anterior, próxima, específica)
- **FA-UC00-007:** Alterar quantidade de itens por página (10, 20, 50, 100)

### Fluxos de Exceção
- **FE-UC00-001:** Usuário sem permissão → HTTP 403 + mensagem "Você não possui permissão para visualizar fornecedores"
- **FE-UC00-002:** Nenhum registro encontrado → exibir estado vazio "Nenhum fornecedor encontrado. Tente ajustar os filtros ou criar um novo fornecedor"
- **FE-UC00-003:** Erro no backend → HTTP 500 + mensagem "Erro ao carregar fornecedores. Tente novamente"

### Regras de Negócio
- **RN-RF022-014:** Isolamento por tenant - apenas fornecedores do tenant do usuário
- **RN-RF022-020:** Busca por nome parcial (LIKE, case-insensitive, mínimo 3 caracteres)
- RN-UC-00-001: Paginação padrão 20 itens (permitido 10, 20, 50, 100)
- RN-UC-00-002: Registros soft-deleted (fl_excluido = true) não aparecem
- RN-UC-00-003: Ordenação padrão: Nome ASC

### Critérios de Aceite
- **CA-UC00-001:** A lista DEVE exibir apenas fornecedores do tenant do usuário autenticado (RN-RF022-014)
- **CA-UC00-002:** Registros excluídos (soft delete) NÃO devem aparecer na listagem
- **CA-UC00-003:** Paginação DEVE ser aplicada com limite padrão de 20 registros
- **CA-UC00-004:** Sistema DEVE permitir ordenação por qualquer coluna visível
- **CA-UC00-005:** Filtros DEVEM ser acumuláveis e refletir na URL (para compartilhamento)
- **CA-UC00-006:** Busca por nome DEVE aceitar mínimo 3 caracteres e ser case-insensitive (RN-RF022-020)
- **CA-UC00-007:** Badge de status DEVE ter cores distintas (ATIVO: verde, INATIVO: cinza, EM_HOMOLOGACAO: amarelo, BLOQUEADO: vermelho)
- **CA-UC00-008:** Avaliação DEVE ser exibida em estrelas (0-5) com nota decimal (ex: 4.2 ⭐)

---

## UC01 — Criar Fornecedor

### Objetivo
Permitir a criação de um novo fornecedor com validações completas de dados obrigatórios e regras de negócio.

### Pré-condições
- Usuário autenticado
- Permissão `fornecedor.create`

### Pós-condições
- Registro persistido no banco com tenant_id do usuário
- Auditoria registrada em Fornecedor_Historico
- Evento `fornecedor.criado` publicado

### Fluxo Principal
- **FP-UC01-001:** Usuário clica em "Novo Fornecedor"
- **FP-UC01-002:** Sistema valida permissão `fornecedor.create`
- **FP-UC01-003:** Sistema exibe formulário vazio com abas: Dados Principais (ativa), Contatos (desabilitada), Documentos (desabilitada), Avaliações (desabilitada)
- **FP-UC01-004:** Usuário preenche campos obrigatórios: Tipo de Fornecedor, CNPJ ou CPF, Nome (Razão Social)
- **FP-UC01-005:** Usuário preenche campos opcionais: Nome Fantasia, E-mail, Telefone, Website, Observações, Limite de Crédito
- **FP-UC01-006:** Usuário clica em "Salvar"
- **FP-UC01-007:** Sistema valida campos obrigatórios (RN-RF022-004, RN-RF022-005)
- **FP-UC01-008:** Sistema valida formato de CNPJ/CPF (dígitos verificadores) (RN-RF022-002, RN-RF022-003)
- **FP-UC01-009:** Sistema valida unicidade de CNPJ/CPF no tenant (RN-RF022-001)
- **FP-UC01-010:** Sistema valida e-mail (formato RFC 5322) se informado (RN-RF022-008)
- **FP-UC01-011:** Sistema valida limite de crédito (>= 0) se informado (RN-RF022-016)
- **FP-UC01-012:** Sistema cria registro com status padrão "EM_HOMOLOGACAO" (RN-RF022-006)
- **FP-UC01-013:** Sistema preenche automaticamente tenant_id, usuario_criacao_id, data_criacao
- **FP-UC01-014:** Sistema registra auditoria (CREATE) em Fornecedor_Historico (RN-RF022-015)
- **FP-UC01-015:** Sistema publica evento `fornecedor.criado`
- **FP-UC01-016:** Sistema exibe mensagem de sucesso "Fornecedor criado com sucesso"
- **FP-UC01-017:** Sistema redireciona para UC02 (visualização do fornecedor criado)

### Fluxos Alternativos
- **FA-UC01-001:** Salvar e continuar editando → mantém no formulário, habilita abas Contatos/Documentos/Avaliações
- **FA-UC01-002:** Cancelar criação → exibir confirmação "Deseja realmente cancelar? Os dados serão perdidos" → redirecionar para UC00

### Fluxos de Exceção
- **FE-UC01-001:** Campo obrigatório ausente → HTTP 400 + mensagem específica (ex: "Nome do fornecedor é obrigatório") (RN-RF022-005)
- **FE-UC01-002:** CNPJ inválido (dígitos verificadores) → HTTP 400 + "CNPJ inválido" (RN-RF022-002)
- **FE-UC01-003:** CPF inválido (dígitos verificadores) → HTTP 400 + "CPF inválido" (RN-RF022-003)
- **FE-UC01-004:** CNPJ duplicado no tenant → HTTP 409 + "CNPJ já cadastrado neste conglomerado" (RN-RF022-001)
- **FE-UC01-005:** E-mail inválido → HTTP 400 + "E-mail inválido" (RN-RF022-008)
- **FE-UC01-006:** Tipo de fornecedor fora da lista → HTTP 400 + "Tipo de fornecedor inválido" (RN-RF022-004)
- **FE-UC01-007:** Limite de crédito negativo → HTTP 400 + "Limite de crédito deve ser maior ou igual a zero" (RN-RF022-016)
- **FE-UC01-008:** Usuário sem permissão → HTTP 403 + "Você não possui permissão para criar fornecedores"

### Regras de Negócio
- **RN-RF022-001:** CNPJ único por tenant
- **RN-RF022-002:** Validação de CNPJ (dígitos verificadores)
- **RN-RF022-003:** Validação de CPF (dígitos verificadores)
- **RN-RF022-004:** Tipo de fornecedor obrigatório
- **RN-RF022-005:** Nome obrigatório (3-200 caracteres)
- **RN-RF022-006:** Status padrão "EM_HOMOLOGACAO"
- **RN-RF022-008:** Validação de e-mail (RFC 5322)
- **RN-RF022-014:** Isolamento por tenant
- **RN-RF022-015:** Auditoria completa
- **RN-RF022-016:** Limite de crédito >= 0

### Critérios de Aceite
- **CA-UC01-001:** Todos os campos obrigatórios DEVEM ser validados antes de persistir (RN-RF022-004, RN-RF022-005)
- **CA-UC01-002:** tenant_id DEVE ser preenchido automaticamente com o tenant do usuário autenticado (RN-RF022-014)
- **CA-UC01-003:** usuario_criacao_id DEVE ser preenchido automaticamente com ID do usuário autenticado
- **CA-UC01-004:** data_criacao DEVE ser preenchido automaticamente com timestamp atual (UTC)
- **CA-UC01-005:** Status DEVE ser preenchido como "EM_HOMOLOGACAO" se não informado (RN-RF022-006)
- **CA-UC01-006:** CNPJ DEVE ser validado com dígitos verificadores (RN-RF022-002)
- **CA-UC01-007:** Sistema DEVE rejeitar CNPJ duplicado no mesmo tenant (RN-RF022-001)
- **CA-UC01-008:** Auditoria DEVE ser registrada APÓS sucesso da criação (RN-RF022-015)
- **CA-UC01-009:** E-mail DEVE ser validado se informado (RN-RF022-008)
- **CA-UC01-010:** Limite de crédito DEVE aceitar zero ou valores positivos (RN-RF022-016)

---

## UC02 — Visualizar Fornecedor

### Objetivo
Permitir visualização detalhada de um fornecedor, incluindo dados principais, contatos, documentos e avaliações.

### Pré-condições
- Usuário autenticado
- Permissão `fornecedor.read`
- Fornecedor existe e pertence ao tenant do usuário

### Pós-condições
- Dados exibidos corretamente
- Usuário pode navegar entre abas (Dados Principais, Contatos, Documentos, Avaliações, Histórico)

### Fluxo Principal
- **FP-UC02-001:** Usuário seleciona fornecedor (via UC00 ou URL direta /fornecedores/{id})
- **FP-UC02-002:** Sistema valida permissão `fornecedor.read`
- **FP-UC02-003:** Sistema valida que fornecedor pertence ao tenant do usuário (RN-RF022-014)
- **FP-UC02-004:** Sistema carrega dados do fornecedor
- **FP-UC02-005:** Sistema exibe dados em modo leitura com abas:
  - **Dados Principais:** Nome, CNPJ/CPF, Tipo, Status, E-mail, Telefone, Website, Limite de Crédito, Observações
  - **Contatos:** Lista de contatos (nome, tipo, principal, telefone, e-mail)
  - **Documentos:** Lista de documentos anexados (tipo, data vencimento, status)
  - **Avaliações:** Histórico de avaliações (data, avaliador, notas, comentários)
  - **Histórico:** Auditoria de alterações (operação, usuário, data, diff)
- **FP-UC02-006:** Sistema exibe botões de ação conforme permissões: Editar (fornecedor.update), Inativar (fornecedor.delete), Avaliar (fornecedor.rate)

### Fluxos Alternativos
- **FA-UC02-001:** Clicar em "Editar" → redirecionar para UC03
- **FA-UC02-002:** Clicar em "Inativar" → acionar UC04
- **FA-UC02-003:** Clicar em "Avaliar" → abrir modal de avaliação
- **FA-UC02-004:** Navegar entre abas → carregar dados da aba selecionada

### Fluxos de Exceção
- **FE-UC02-001:** Fornecedor não encontrado → HTTP 404 + "Fornecedor não encontrado"
- **FE-UC02-002:** Fornecedor de outro tenant → HTTP 404 (não HTTP 403 para não vazar existência) (RN-RF022-014)
- **FE-UC02-003:** Usuário sem permissão → HTTP 403 + "Você não possui permissão para visualizar fornecedores"

### Regras de Negócio
- **RN-RF022-014:** Isolamento por tenant - tentar acessar fornecedor de outro tenant retorna 404
- RN-UC-02-001: Informações de auditoria DEVEM ser exibidas (usuario_criacao, data_criacao, usuario_atualizacao, data_atualizacao)
- RN-UC-02-002: Badge de documentos vencidos ou próximos do vencimento (30 dias) (RN-RF022-013)

### Critérios de Aceite
- **CA-UC02-001:** Usuário SÓ pode visualizar fornecedores do próprio tenant (RN-RF022-014)
- **CA-UC02-002:** Informações de auditoria DEVEM ser exibidas (usuario_criacao, data_criacao, usuario_atualizacao, data_atualizacao)
- **CA-UC02-003:** Tentativa de acessar fornecedor de outro tenant DEVE retornar 404 (não 403)
- **CA-UC02-004:** Tentativa de acessar fornecedor inexistente DEVE retornar 404
- **CA-UC02-005:** Dados exibidos DEVEM corresponder exatamente ao estado atual no banco
- **CA-UC02-006:** Badge de alerta DEVE ser exibido se documentos vencendo em 30 dias (RN-RF022-013)
- **CA-UC02-007:** Avaliação DEVE exibir nota geral calculada com média ponderada (RN-RF022-011)
- **CA-UC02-008:** Botões de ação DEVEM ser exibidos apenas se usuário tiver permissão correspondente

---

## UC03 — Editar Fornecedor

### Objetivo
Permitir alteração controlada de dados de um fornecedor existente com validações e auditoria.

### Pré-condições
- Usuário autenticado
- Permissão `fornecedor.update`
- Fornecedor existe e pertence ao tenant do usuário

### Pós-condições
- Registro atualizado no banco
- Auditoria registrada com diff (antes/depois)
- Evento `fornecedor.atualizado` publicado

### Fluxo Principal
- **FP-UC03-001:** Usuário acessa fornecedor via UC02 e clica em "Editar"
- **FP-UC03-002:** Sistema valida permissão `fornecedor.update`
- **FP-UC03-003:** Sistema valida que fornecedor pertence ao tenant do usuário (RN-RF022-014)
- **FP-UC03-004:** Sistema carrega dados atuais no formulário
- **FP-UC03-005:** Usuário altera campos desejados
- **FP-UC03-006:** Usuário clica em "Salvar"
- **FP-UC03-007:** Sistema valida campos obrigatórios (se alterados)
- **FP-UC03-008:** Sistema valida formato de CNPJ/CPF (se alterado) (RN-RF022-002, RN-RF022-003)
- **FP-UC03-009:** Sistema valida unicidade de CNPJ/CPF (se alterado) (RN-RF022-001)
- **FP-UC03-010:** Sistema valida transição de status (se alterado) conforme matriz de transições
- **FP-UC03-011:** Sistema valida e-mail (se alterado) (RN-RF022-008)
- **FP-UC03-012:** Sistema atualiza registro
- **FP-UC03-013:** Sistema preenche automaticamente usuario_atualizacao_id, data_atualizacao
- **FP-UC03-014:** Sistema registra auditoria (UPDATE) com diff em Fornecedor_Historico (RN-RF022-015)
- **FP-UC03-015:** Sistema publica evento `fornecedor.atualizado` com campos alterados
- **FP-UC03-016:** Sistema exibe mensagem de sucesso "Fornecedor atualizado com sucesso"
- **FP-UC03-017:** Sistema redireciona para UC02 (visualização)

### Fluxos Alternativos
- **FA-UC03-001:** Cancelar edição → exibir confirmação "Deseja realmente cancelar? Alterações não salvas serão perdidas" → redirecionar para UC02

### Fluxos de Exceção
- **FE-UC03-001:** Campo obrigatório removido → HTTP 400 + mensagem específica
- **FE-UC03-002:** CNPJ duplicado (se alterado) → HTTP 409 + "CNPJ já cadastrado neste conglomerado" (RN-RF022-001)
- **FE-UC03-003:** E-mail inválido (se alterado) → HTTP 400 + "E-mail inválido" (RN-RF022-008)
- **FE-UC03-004:** Transição de status inválida → HTTP 400 + "Transição de status inválida" (ex: INATIVO → EM_HOMOLOGACAO não permitido)
- **FE-UC03-005:** Fornecedor de outro tenant → HTTP 404 (RN-RF022-014)
- **FE-UC03-006:** Usuário sem permissão → HTTP 403 + "Você não possui permissão para editar fornecedores"

### Regras de Negócio
- **RN-RF022-001:** CNPJ único por tenant (se alterado)
- **RN-RF022-002:** Validação de CNPJ (se alterado)
- **RN-RF022-003:** Validação de CPF (se alterado)
- **RN-RF022-008:** Validação de e-mail (se alterado)
- **RN-RF022-014:** Isolamento por tenant
- **RN-RF022-015:** Auditoria completa com diff
- RN-UC-03-001: usuario_atualizacao_id preenchido automaticamente
- RN-UC-03-002: data_atualizacao preenchida automaticamente (UTC)
- RN-UC-03-003: Transições de status devem seguir matriz permitida (EM_HOMOLOGACAO → ATIVO, ATIVO → INATIVO/BLOQUEADO, INATIVO → ATIVO, BLOQUEADO → ATIVO)

### Critérios de Aceite
- **CA-UC03-001:** usuario_atualizacao_id DEVE ser preenchido automaticamente com ID do usuário autenticado
- **CA-UC03-002:** data_atualizacao DEVE ser preenchida automaticamente com timestamp atual (UTC)
- **CA-UC03-003:** Apenas campos alterados DEVEM ser validados
- **CA-UC03-004:** Tentativa de editar fornecedor de outro tenant DEVE retornar 404 (RN-RF022-014)
- **CA-UC03-005:** Auditoria DEVE registrar estado anterior e novo estado (diff) (RN-RF022-015)
- **CA-UC03-006:** Sistema DEVE validar transições de status permitidas
- **CA-UC03-007:** CNPJ DEVE ser validado se alterado (RN-RF022-002)
- **CA-UC03-008:** Unicidade de CNPJ DEVE ser validada se alterado (RN-RF022-001)

---

## UC04 — Inativar Fornecedor

### Objetivo
Permitir exclusão lógica (soft delete) de fornecedor com validação de vínculos.

### Pré-condições
- Usuário autenticado
- Permissão `fornecedor.delete`
- Fornecedor existe, pertence ao tenant do usuário e está ativo
- Fornecedor NÃO possui contratos ativos (RN-RF022-007)

### Pós-condições
- Registro marcado como excluído (soft delete)
- Status alterado para "INATIVO"
- Auditoria registrada
- Evento `fornecedor.inativado` publicado

### Fluxo Principal
- **FP-UC04-001:** Usuário acessa fornecedor via UC02 e clica em "Inativar"
- **FP-UC04-002:** Sistema valida permissão `fornecedor.delete`
- **FP-UC04-003:** Sistema valida que fornecedor pertence ao tenant do usuário (RN-RF022-014)
- **FP-UC04-004:** Sistema verifica se fornecedor possui contratos ativos (RN-RF022-007)
- **FP-UC04-005:** Sistema exibe diálogo de confirmação "Deseja realmente inativar este fornecedor? Esta ação pode ser revertida posteriormente"
- **FP-UC04-006:** Usuário confirma inativação
- **FP-UC04-007:** Sistema atualiza status para "INATIVO"
- **FP-UC04-008:** Sistema preenche fl_excluido = true
- **FP-UC04-009:** Sistema preenche usuario_exclusao_id e data_exclusao
- **FP-UC04-010:** Sistema registra auditoria (DELETE) em Fornecedor_Historico (RN-RF022-015)
- **FP-UC04-011:** Sistema publica evento `fornecedor.inativado`
- **FP-UC04-012:** Sistema exibe mensagem de sucesso "Fornecedor inativado com sucesso"
- **FP-UC04-013:** Sistema redireciona para UC00 (listagem)

### Fluxos Alternativos
- **FA-UC04-001:** Cancelar inativação → fechar diálogo e retornar para UC02

### Fluxos de Exceção
- **FE-UC04-001:** Fornecedor possui contratos ativos → HTTP 409 + "Não é possível inativar fornecedor com contratos ativos" + lista de contratos (RN-RF022-007)
- **FE-UC04-002:** Fornecedor já está inativo → HTTP 400 + "Fornecedor já está inativo"
- **FE-UC04-003:** Fornecedor de outro tenant → HTTP 404 (RN-RF022-014)
- **FE-UC04-004:** Usuário sem permissão → HTTP 403 + "Você não possui permissão para inativar fornecedores"

### Regras de Negócio
- **RN-RF022-007:** Não inativar fornecedor com contratos ativos
- **RN-RF022-014:** Isolamento por tenant
- **RN-RF022-015:** Auditoria completa
- RN-UC-04-001: Exclusão sempre lógica (soft delete) via fl_excluido e data_exclusao
- RN-UC-04-002: Status alterado para "INATIVO" ao inativar
- RN-UC-04-003: usuario_exclusao_id e data_exclusao preenchidos automaticamente

### Critérios de Aceite
- **CA-UC04-001:** Exclusão DEVE ser sempre lógica (soft delete) via fl_excluido e data_exclusao
- **CA-UC04-002:** Sistema DEVE verificar contratos ativos ANTES de permitir inativação (RN-RF022-007)
- **CA-UC04-003:** Sistema DEVE exigir confirmação explícita do usuário
- **CA-UC04-004:** data_exclusao DEVE ser preenchida com timestamp atual (UTC)
- **CA-UC04-005:** usuario_exclusao_id DEVE ser preenchido com ID do usuário autenticado
- **CA-UC04-006:** Tentativa de inativar fornecedor com contratos ativos DEVE retornar HTTP 409 (RN-RF022-007)
- **CA-UC04-007:** Fornecedor inativado NÃO deve aparecer em listagens padrão (UC00)
- **CA-UC04-008:** Status DEVE ser alterado para "INATIVO"
- **CA-UC04-009:** Auditoria DEVE ser registrada (RN-RF022-015)

---


## UC05 - Validar CNPJ/CPF

### Objetivo
Validar dígitos verificadores de CNPJ ou CPF conforme algoritmos oficiais.

### Pré-condições
- Usuário autenticado
- Permissão `fornecedor.create` ou `fornecedor.update`
- CNPJ ou CPF informado

### Pós-condições
- CNPJ/CPF validado e aceito (HTTP 200) OU rejeitado (HTTP 400)

### Fluxo Principal
- **FP-UC05-001:** Sistema recebe CNPJ ou CPF durante criação/edição de fornecedor (UC01 ou UC03)
- **FP-UC05-002:** Sistema identifica tipo de documento (14 dígitos = CNPJ, 11 dígitos = CPF)
- **FP-UC05-003:** Sistema remove caracteres especiais (pontos, traços, barras)
- **FP-UC05-004:** Sistema valida se todos os caracteres são numéricos
- **FP-UC05-005:** Sistema calcula dígitos verificadores conforme algoritmo oficial
- **FP-UC05-006:** Sistema compara dígitos calculados com informados
- **FP-UC05-007:** Se válido: prossegue com criação/edição
- **FP-UC05-008:** Se inválido: retorna HTTP 400

### Fluxos Alternativos
- **FA-UC05-001:** CNPJ/CPF não informado (opcional) → prosseguir sem validação

### Fluxos de Exceção
- **FE-UC05-001:** CNPJ com dígitos verificadores incorretos → HTTP 400 + "CNPJ inválido" (RN-RF022-002)
- **FE-UC05-002:** CPF com dígitos verificadores incorretos → HTTP 400 + "CPF inválido" (RN-RF022-003)
- **FE-UC05-003:** Documento com caracteres não numéricos → HTTP 400 + "Formato inválido"
- **FE-UC05-004:** CNPJ/CPF com todos dígitos iguais (ex: 111.111.111-11) → HTTP 400 + "Documento inválido"

### Regras de Negócio
- **RN-RF022-002:** Validação de CNPJ (dígitos verificadores)
- **RN-RF022-003:** Validação de CPF (dígitos verificadores)

### Critérios de Aceite
- **CA-UC05-001:** Validação DEVE executar no backend (não confiar apenas no frontend)
- **CA-UC05-002:** CNPJ com formato 00.000.000/0000-00 DEVE ser aceito após remoção de pontuação
- **CA-UC05-003:** CPF com formato 000.000.000-00 DEVE ser aceito após remoção de pontuação
- **CA-UC05-004:** CNPJ/CPF com todos dígitos iguais (ex: 111.111.111-11, 00.000.000/0000-00) DEVE ser rejeitado
- **CA-UC05-005:** Algoritmo DEVE seguir especificação oficial da Receita Federal
- **CA-UC05-006:** Mensagem de erro DEVE indicar se problema é no CNPJ ou CPF especificamente

---

## UC06 - Gerenciar Contatos

### Objetivo
Adicionar, editar, excluir e marcar contatos principais do fornecedor por tipo (Comercial, Técnico, Financeiro, Jurídico).

### Pré-condições
- Usuário autenticado
- Permissão `fornecedor.update`
- Fornecedor existe e pertence ao tenant

### Pós-condições
- Contato criado/editado/excluído (HTTP 201/200/204)
- Auditoria registrada
- Apenas um contato principal por tipo (RN-RF022-009)

### Fluxo Principal - Criar Contato
- **FP-UC06-001:** Usuário acessa fornecedor via UC02 e clica em "Adicionar Contato"
- **FP-UC06-002:** Sistema exibe formulário: Nome (obrigatório), Cargo, Tipo (dropdown: Comercial/Técnico/Financeiro/Jurídico), Telefone (obrigatório - RN-RF022-017), E-mail, Principal (checkbox)
- **FP-UC06-003:** Usuário preenche campos e clica "Salvar"
- **FP-UC06-004:** Sistema valida telefone obrigatório (RN-RF022-017)
- **FP-UC06-005:** Sistema valida e-mail (se informado - RN-RF022-018)
- **FP-UC06-006:** Se marcado como principal: Sistema verifica se já existe contato principal do mesmo tipo (RN-RF022-009)
- **FP-UC06-007:** Se já existe: Sistema desmarca contato anterior automaticamente
- **FP-UC06-008:** Sistema cria registro com fornecedor_id, tenant_id, criado_por, criado_em
- **FP-UC06-009:** Sistema retorna HTTP 201 Created

### Fluxo Principal - Editar Contato
- **FP-UC06-010:** Usuário clica em "Editar" em contato existente
- **FP-UC06-011:** Sistema carrega dados do contato
- **FP-UC06-012:** Usuário altera campos e clica "Salvar"
- **FP-UC06-013:** Sistema valida campos (RN-RF022-017, RN-RF022-018)
- **FP-UC06-014:** Se alterado para principal: Sistema desmarca contato anterior do mesmo tipo (RN-RF022-009)
- **FP-UC06-015:** Sistema atualiza registro com alterado_por, alterado_em
- **FP-UC06-016:** Sistema retorna HTTP 200 OK

### Fluxo Principal - Excluir Contato
- **FP-UC06-017:** Usuário clica em "Excluir" em contato
- **FP-UC06-018:** Sistema exibe confirmação
- **FP-UC06-019:** Usuário confirma
- **FP-UC06-020:** Sistema marca como excluído (soft delete: fl_excluido = true, data_exclusao, usuario_exclusao_id)
- **FP-UC06-021:** Sistema retorna HTTP 204 No Content

### Fluxos Alternativos
- **FA-UC06-001:** Cancelar criação/edição → fechar formulário sem salvar
- **FA-UC06-002:** Adicionar múltiplos telefones ao mesmo contato → permitir telefone_1, telefone_2

### Fluxos de Exceção
- **FE-UC06-001:** Tentativa de marcar segundo contato como principal do mesmo tipo → Sistema desmarca anterior automaticamente (RN-RF022-009) - NÃO é erro
- **FE-UC06-002:** Nome ausente → HTTP 400 + "Nome do contato é obrigatório"
- **FE-UC06-003:** Telefone ausente → HTTP 400 + "Telefone é obrigatório" (RN-RF022-017)
- **FE-UC06-004:** E-mail inválido (se informado) → HTTP 400 + "E-mail inválido" (RN-RF022-018)
- **FE-UC06-005:** Tipo não informado → HTTP 400 + "Tipo de contato é obrigatório"
- **FE-UC06-006:** Contato não encontrado → HTTP 404
- **FE-UC06-007:** Contato de outro fornecedor/tenant → HTTP 404 (RN-RF022-014)
- **FE-UC06-008:** Usuário sem permissão → HTTP 403

### Regras de Negócio
- **RN-RF022-009:** Apenas um contato principal por tipo (desmarcação automática do anterior)
- **RN-RF022-014:** Isolamento por tenant
- **RN-RF022-015:** Auditoria completa
- **RN-RF022-017:** Telefone obrigatório para contato
- **RN-RF022-018:** Validação de e-mail (se informado)

### Critérios de Aceite
- **CA-UC06-001:** Sistema DEVE permitir múltiplos contatos por fornecedor
- **CA-UC06-002:** Ao marcar novo contato como principal, sistema DEVE desmarcar anterior do mesmo tipo automaticamente (RN-RF022-009)
- **CA-UC06-003:** Telefone DEVE ser obrigatório (RN-RF022-017)
- **CA-UC06-004:** E-mail DEVE ser validado se informado (RN-RF022-018)
- **CA-UC06-005:** Exclusão DEVE ser lógica (soft delete)
- **CA-UC06-006:** Sistema DEVE suportar 4 tipos de contato: Comercial, Técnico, Financeiro, Jurídico
- **CA-UC06-007:** Badge "Principal" DEVE ser exibido no contato marcado como principal
- **CA-UC06-008:** Listagem de contatos DEVE agrupar por tipo e destacar principal

---

## UC07 - Avaliar Fornecedor

### Objetivo
Registrar avaliação de performance do fornecedor com notas de 1 a 5 para Qualidade, Prazo, Atendimento e Preço, calculando nota geral automaticamente.

### Pré-condições
- Usuário autenticado
- Permissão `fornecedor.avaliar`
- Fornecedor existe e pertence ao tenant
- Fornecedor possui ao menos 1 contrato concluído (opcional, mas recomendado)

### Pós-condições
- Avaliação criada (HTTP 201)
- Nota geral do fornecedor recalculada (RN-RF022-011, RN-RF022-012)
- Auditoria registrada

### Fluxo Principal
- **FP-UC07-001:** Usuário acessa fornecedor via UC02 e clica em "Avaliar Fornecedor"
- **FP-UC07-002:** Sistema exibe formulário de avaliação com 4 notas (Qualidade, Prazo, Atendimento, Preço) - campo obrigatório de 1 a 5 estrelas
- **FP-UC07-003:** Sistema exibe campo opcional "Comentários" (até 1000 caracteres)
- **FP-UC07-004:** Usuário preenche notas e clica "Salvar"
- **FP-UC07-005:** Sistema valida que todas as 4 notas estão entre 1 e 5 (RN-RF022-010)
- **FP-UC07-006:** Sistema calcula nota individual da avaliação: (qualidade * 0.4) + (prazo * 0.3) + (atendimento * 0.2) + (preço * 0.1) (RN-RF022-011)
- **FP-UC07-007:** Sistema arredonda nota individual para 2 casas decimais
- **FP-UC07-008:** Sistema cria registro em Fornecedor_Avaliacao com: fornecedor_id, tenant_id, avaliado_por (usuário autenticado), avaliado_em (timestamp), qualidade, prazo, atendimento, preço, nota_geral_avaliacao, comentarios
- **FP-UC07-009:** Sistema busca últimas 12 avaliações do fornecedor (ordenadas por avaliado_em DESC)
- **FP-UC07-010:** Sistema calcula média das notas_gerais das últimas 12 avaliações (RN-RF022-012)
- **FP-UC07-011:** Sistema atualiza campo nota_geral do Fornecedor com nova média
- **FP-UC07-012:** Sistema registra auditoria (RN-RF022-015)
- **FP-UC07-013:** Sistema exibe mensagem "Avaliação registrada com sucesso. Nota geral do fornecedor atualizada para X.XX"
- **FP-UC07-014:** Sistema retorna HTTP 201 Created

### Fluxos Alternativos
- **FA-UC07-001:** Cancelar avaliação → fechar formulário sem salvar
- **FA-UC07-002:** Fornecedor possui menos de 12 avaliações → calcular média com avaliações existentes (RN-RF022-012)

### Fluxos de Exceção
- **FE-UC07-001:** Nota < 1 ou > 5 → HTTP 400 + "Nota deve estar entre 1 e 5" (RN-RF022-010)
- **FE-UC07-002:** Nota ausente (null ou vazia) → HTTP 400 + "Todas as notas são obrigatórias" (RN-RF022-010)
- **FE-UC07-003:** Comentário com mais de 1000 caracteres → HTTP 400 + "Comentário excede limite de 1000 caracteres"
- **FE-UC07-004:** Fornecedor não encontrado → HTTP 404
- **FE-UC07-005:** Fornecedor de outro tenant → HTTP 404 (RN-RF022-014)
- **FE-UC07-006:** Usuário sem permissão → HTTP 403

### Regras de Negócio
- **RN-RF022-010:** Nota de avaliação válida (1-5, permite decimais)
- **RN-RF022-011:** Cálculo automático de nota geral da avaliação (fórmula ponderada)
- **RN-RF022-012:** Atualização automática de nota do fornecedor (média últimas 12 avaliações)
- **RN-RF022-014:** Isolamento por tenant
- **RN-RF022-015:** Auditoria completa
- **RN-RF022-019:** Histórico de avaliações (todas as avaliações são preservadas)

### Critérios de Aceite
- **CA-UC07-001:** Sistema DEVE validar que notas estão entre 1 e 5 (RN-RF022-010)
- **CA-UC07-002:** Sistema DEVE permitir notas decimais (ex: 4.5)
- **CA-UC07-003:** Nota geral da avaliação DEVE ser calculada com fórmula: (qualidade * 0.4) + (prazo * 0.3) + (atendimento * 0.2) + (preço * 0.1) (RN-RF022-011)
- **CA-UC07-004:** Nota geral do fornecedor DEVE ser atualizada automaticamente com média das últimas 12 avaliações (RN-RF022-012)
- **CA-UC07-005:** Se fornecedor possui < 12 avaliações, média DEVE ser calculada com avaliações existentes
- **CA-UC07-006:** Arredondamento DEVE ser para 2 casas decimais
- **CA-UC07-007:** Campo avaliado_por DEVE ser preenchido automaticamente com usuário autenticado
- **CA-UC07-008:** Campo avaliado_em DEVE ser preenchido automaticamente com timestamp UTC
- **CA-UC07-009:** Sistema DEVE preservar histórico completo de avaliações (RN-RF022-019)
- **CA-UC07-010:** Listagem de avaliações DEVE exibir: data, avaliador, nota geral, comentários
- **CA-UC07-011:** Badge com estrelas DEVE ser exibido na listagem de fornecedores (nota geral)

---

## UC08 - Gerenciar Documentos

### Objetivo
Fazer upload, download, visualizar e excluir documentos obrigatórios do fornecedor (contratos sociais, certidões, certificados) com controle de vencimento.

### Pré-condições
- Usuário autenticado
- Permissão `fornecedor.update`
- Fornecedor existe e pertence ao tenant

### Pós-condições
- Documento criado/excluído (HTTP 201/204)
- Arquivo armazenado em blob storage
- Data de vencimento registrada (se aplicável)
- Auditoria registrada

### Fluxo Principal - Upload de Documento
- **FP-UC08-001:** Usuário acessa fornecedor via UC02 e clica em "Adicionar Documento"
- **FP-UC08-002:** Sistema exibe formulário: Tipo (dropdown: Contrato Social, Certidão Negativa Débitos Federais, Certidão Negativa Débitos Estaduais, Certidão Negativa Débitos Municipais, Certificado ISO, Outros), Descrição, Arquivo (obrigatório), Data Vencimento (se aplicável)
- **FP-UC08-003:** Usuário seleciona arquivo (PDF, DOC, DOCX, JPG, PNG - max 10MB) e preenche campos
- **FP-UC08-004:** Usuário clica "Salvar"
- **FP-UC08-005:** Sistema valida tamanho do arquivo (<= 10MB)
- **FP-UC08-006:** Sistema valida extensão permitida (PDF, DOC, DOCX, JPG, PNG)
- **FP-UC08-007:** Sistema gera nome único do arquivo (GUID + extensão original)
- **FP-UC08-008:** Sistema faz upload do arquivo para blob storage (Azure Blob / AWS S3)
- **FP-UC08-009:** Sistema cria registro em Fornecedor_Documento com: fornecedor_id, tenant_id, tipo, descricao, nome_original, nome_armazenado, tamanho_bytes, data_vencimento, criado_por, criado_em
- **FP-UC08-010:** Sistema registra auditoria
- **FP-UC08-011:** Sistema retorna HTTP 201 Created

### Fluxo Principal - Download de Documento
- **FP-UC08-012:** Usuário clica em "Baixar" em documento da lista
- **FP-UC08-013:** Sistema valida permissão `fornecedor.view`
- **FP-UC08-014:** Sistema valida que documento pertence ao tenant (RN-RF022-014)
- **FP-UC08-015:** Sistema recupera arquivo do blob storage
- **FP-UC08-016:** Sistema retorna arquivo com nome original
- **FP-UC08-017:** Sistema registra auditoria (acesso ao documento)

### Fluxo Principal - Excluir Documento
- **FP-UC08-018:** Usuário clica em "Excluir" em documento
- **FP-UC08-019:** Sistema exibe confirmação
- **FP-UC08-020:** Usuário confirma
- **FP-UC08-021:** Sistema marca como excluído (soft delete: fl_excluido = true, data_exclusao, usuario_exclusao_id)
- **FP-UC08-022:** Sistema NÃO remove arquivo físico do blob (apenas marca como excluído para auditoria)
- **FP-UC08-023:** Sistema retorna HTTP 204 No Content

### Fluxos Alternativos
- **FA-UC08-001:** Visualizar documento (se PDF/imagem) → Sistema exibe preview inline antes de download
- **FA-UC08-002:** Cancelar upload → fechar formulário sem salvar

### Fluxos de Exceção
- **FE-UC08-001:** Arquivo com tamanho > 10MB → HTTP 400 + "Arquivo excede limite de 10MB"
- **FE-UC08-002:** Arquivo com extensão não permitida → HTTP 400 + "Formato de arquivo não permitido. Use PDF, DOC, DOCX, JPG ou PNG"
- **FE-UC08-003:** Tipo de documento não informado → HTTP 400 + "Tipo de documento é obrigatório"
- **FE-UC08-004:** Arquivo não selecionado → HTTP 400 + "Arquivo é obrigatório"
- **FE-UC08-005:** Erro ao fazer upload para blob storage → HTTP 500 + "Erro ao armazenar arquivo. Tente novamente"
- **FE-UC08-006:** Documento não encontrado → HTTP 404
- **FE-UC08-007:** Documento de outro fornecedor/tenant → HTTP 404 (RN-RF022-014)
- **FE-UC08-008:** Usuário sem permissão → HTTP 403

### Regras de Negócio
- **RN-RF022-013:** Validação de documentos vencidos (alerta se data_vencimento <= hoje + 30 dias)
- **RN-RF022-014:** Isolamento por tenant
- **RN-RF022-015:** Auditoria completa

### Critérios de Aceite
- **CA-UC08-001:** Sistema DEVE aceitar arquivos PDF, DOC, DOCX, JPG, PNG
- **CA-UC08-002:** Tamanho máximo DEVE ser 10MB por arquivo
- **CA-UC08-003:** Nome do arquivo armazenado DEVE ser GUID para evitar conflitos
- **CA-UC08-004:** Sistema DEVE preservar nome original do arquivo para download
- **CA-UC08-005:** Exclusão DEVE ser lógica (soft delete) - arquivo físico preservado para auditoria
- **CA-UC08-006:** Sistema DEVE exibir badge de alerta se documento vencido ou próximo do vencimento (RN-RF022-013)
- **CA-UC08-007:** Listagem DEVE exibir: tipo, descrição, data upload, data vencimento, status (vencido/válido/próximo vencimento)
- **CA-UC08-008:** Sistema DEVE permitir múltiplos documentos do mesmo tipo (ex: várias certidões)

---

## UC09 - Alertar Vencimentos

### Objetivo
Notificar automaticamente responsáveis sobre documentos próximos ao vencimento (30 dias) ou vencidos.

### Pré-condições
- Job noturno agendado (executado diariamente às 02:00 UTC)
- Fornecedores com documentos possuem data_vencimento preenchida

### Pós-condições
- Notificações enviadas (e-mail, push)
- Badge de alerta exibido na listagem de fornecedores
- Registro de envio em tabela de notificações

### Fluxo Principal
- **FP-UC09-001:** Job noturno inicia às 02:00 UTC
- **FP-UC09-002:** Sistema busca todos os documentos com data_vencimento ENTRE (hoje) E (hoje + 30 dias) E fl_excluido = false
- **FP-UC09-003:** Sistema agrupa documentos por fornecedor
- **FP-UC09-004:** Para cada fornecedor com documentos vencendo:
  - **FP-UC09-005:** Sistema identifica responsável pelo fornecedor (usuário que criou OU responsável definido)
  - **FP-UC09-006:** Sistema cria notificação: "O fornecedor {nome} possui {quantidade} documento(s) próximo(s) ao vencimento"
  - **FP-UC09-007:** Sistema envia e-mail ao responsável com lista de documentos e datas de vencimento
  - **FP-UC09-008:** Sistema cria registro em Notificacoes com: tipo='VENCIMENTO_DOCUMENTO', destinatario_id, enviado_em, lido=false
- **FP-UC09-009:** Sistema atualiza campo fl_alerta_vencimento = true no Fornecedor (exibir badge na listagem)
- **FP-UC09-010:** Sistema registra log de execução do job

### Fluxo Principal - Visualização de Alerta pelo Usuário
- **FP-UC09-011:** Usuário acessa listagem de fornecedores (UC00)
- **FP-UC09-012:** Sistema exibe badge de alerta (ícone de aviso amarelo/vermelho) ao lado do fornecedor com fl_alerta_vencimento = true
- **FP-UC09-013:** Usuário clica no fornecedor
- **FP-UC09-014:** Sistema exibe detalhes do fornecedor (UC02) com seção "Alertas" destacada
- **FP-UC09-015:** Sistema lista documentos vencidos/vencendo com datas

### Fluxos Alternativos
- **FA-UC09-001:** Nenhum documento vencendo → Job finaliza sem enviar notificações
- **FA-UC09-002:** Documento vencido (data_vencimento < hoje) → Badge vermelho + e-mail com urgência "VENCIDO"
- **FA-UC09-003:** Documento vence em 7 dias ou menos → Badge vermelho + prioridade alta

### Fluxos de Exceção
- **FE-UC09-001:** Erro ao enviar e-mail → Sistema registra falha em log, mas continua processando outros fornecedores
- **FE-UC09-002:** Responsável não possui e-mail cadastrado → Sistema pula envio de e-mail, mas cria notificação no sistema

### Regras de Negócio
- **RN-RF022-013:** Validação de documentos vencidos (alerta se data_vencimento <= hoje + 30 dias)
- **RN-RF022-014:** Isolamento por tenant
- **RN-RF022-015:** Auditoria completa (registro de envio de notificações)

### Critérios de Aceite
- **CA-UC09-001:** Job DEVE executar diariamente às 02:00 UTC
- **CA-UC09-002:** Sistema DEVE alertar sobre documentos vencendo nos próximos 30 dias (RN-RF022-013)
- **CA-UC09-003:** Sistema DEVE diferenciar documentos vencidos (badge vermelho) de vencendo (badge amarelo)
- **CA-UC09-004:** E-mail DEVE conter: nome do fornecedor, lista de documentos, datas de vencimento, link direto para o fornecedor
- **CA-UC09-005:** Badge DEVE ser exibido na listagem de fornecedores (UC00)
- **CA-UC09-006:** Sistema DEVE registrar tentativas de envio (sucesso/falha) em tabela de notificações
- **CA-UC09-007:** Notificação DEVE ser marcada como lida quando usuário acessa o fornecedor
- **CA-UC09-008:** Sistema DEVE permitir configurar dias de antecedência (default: 30 dias)

---
## 4. MATRIZ DE RASTREABILIDADE

| UC | Regras de Negócio RF022 Cobertas |
|----|----------------------------------|
| UC00 | RN-RF022-014, RN-RF022-020 |
| UC01 | RN-RF022-001, RN-RF022-002, RN-RF022-003, RN-RF022-004, RN-RF022-005, RN-RF022-006, RN-RF022-008, RN-RF022-014, RN-RF022-015, RN-RF022-016 |
| UC02 | RN-RF022-013, RN-RF022-014 |
| UC03 | RN-RF022-001, RN-RF022-002, RN-RF022-003, RN-RF022-008, RN-RF022-014, RN-RF022-015 |
| UC04 | RN-RF022-007, RN-RF022-014, RN-RF022-015 |
| UC05 | RN-RF022-002, RN-RF022-003 |
| UC06 | RN-RF022-009, RN-RF022-014, RN-RF022-015, RN-RF022-017, RN-RF022-018 |
| UC07 | RN-RF022-010, RN-RF022-011, RN-RF022-012, RN-RF022-014, RN-RF022-015, RN-RF022-019 |
| UC08 | RN-RF022-013, RN-RF022-014, RN-RF022-015 |
| UC09 | RN-RF022-013, RN-RF022-014, RN-RF022-015 |

**Cobertura Total:** 20 de 20 regras de negócio do RF022 (100%) ✅

**Detalhamento de Cobertura por Regra:**
- RN-RF022-001 (CNPJ único) → UC01, UC03
- RN-RF022-002 (Validação CNPJ) → UC01, UC03, UC05
- RN-RF022-003 (Validação CPF) → UC01, UC03, UC05
- RN-RF022-004 (Tipo obrigatório) → UC01
- RN-RF022-005 (Nome obrigatório) → UC01
- RN-RF022-006 (Status válido) → UC01
- RN-RF022-007 (Inativar com contratos ativos) → UC04
- RN-RF022-008 (Validação e-mail) → UC01, UC03
- RN-RF022-009 (Contato principal por tipo) → UC06
- RN-RF022-010 (Nota avaliação válida) → UC07
- RN-RF022-011 (Cálculo automático nota geral) → UC07
- RN-RF022-012 (Atualização automática nota fornecedor) → UC07
- RN-RF022-013 (Validação documentos vencidos) → UC02, UC08, UC09
- RN-RF022-014 (Isolamento multi-tenancy) → UC00, UC01, UC02, UC03, UC04, UC06, UC07, UC08, UC09
- RN-RF022-015 (Auditoria completa) → UC01, UC03, UC04, UC06, UC07, UC08, UC09
- RN-RF022-016 (Limite crédito válido) → UC01
- RN-RF022-017 (Telefone obrigatório para contato) → UC06
- RN-RF022-018 (Validação e-mail contato) → UC06
- RN-RF022-019 (Histórico avaliações) → UC07
- RN-RF022-020 (Busca parcial) → UC00

---

## CHANGELOG

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 1.0 | 2025-12-17 | Sistema Legado | Consolidação inicial de 5 casos de uso (UC00-UC04) |
| 2.0 | 2025-12-31 | Agência ALC - alc.dev.br | Adição de 5 UCs complementares (UC05-UC09) para cobertura 100% de RF022 - Total de 10 UCs cobrindo todas as 20 regras de negócio |

---

**Última Atualização:** 2025-12-31
**Versão de Governança:** 2.0
**Status:** ✅ Casos de Uso Canônicos Completos (Cobertura 100% das 20 regras RF022 em 10 UCs)
