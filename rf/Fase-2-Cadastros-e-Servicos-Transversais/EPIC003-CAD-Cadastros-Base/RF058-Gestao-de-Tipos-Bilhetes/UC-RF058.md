# UC-RF058 — Casos de Uso Canônicos

**RF:** RF058 — Gestão de Tipos de Bilhetes
**Versão:** 2.0
**Data:** 2025-12-31
**Autor:** Agência ALC - alc.dev.br
**Epic:** EPIC003-CAD-Cadastros-Base
**Fase:** Fase-2-Cadastros-e-Servicos-Transversais

---

## 1. OBJETIVO DO DOCUMENTO

Este documento descreve **todos os Casos de Uso (UC)** derivados do **RF058**, cobrindo integralmente o comportamento funcional esperado para a funcionalidade de Gestão de Tipos de Bilhetes.

Os UCs aqui definidos servem como **contrato comportamental**, sendo a **fonte primária** para geração de:
- Casos de Teste (TC-RF058.yaml)
- Massas de Teste (MT-RF058.yaml)
- Evidências de auditoria e validação funcional
- Execução por agentes de IA (tester, QA, E2E)

---

## 2. SUMÁRIO DE CASOS DE USO

| ID | Nome | Ator Principal |
|----|------|----------------|
| UC00 | Listar Tipos de Bilhetes | Usuário Autenticado |
| UC01 | Criar Tipo de Bilhete | Usuário Autenticado |
| UC02 | Visualizar Tipo de Bilhete | Usuário Autenticado |
| UC03 | Editar Tipo de Bilhete | Usuário Autenticado |
| UC04 | Inativar Tipo de Bilhete | Usuário Autenticado |

---

## 3. PADRÕES GERAIS APLICÁVEIS A TODOS OS UCs

- Todos os acessos respeitam **isolamento por tenant** (EmpresaId)
- Todas as ações exigem **permissão explícita**
- Erros não devem vazar informações sensíveis
- Auditoria deve registrar **quem**, **quando** e **qual ação**
- Mensagens devem ser claras, previsíveis e rastreáveis
- Validações seguem regras de negócio documentadas (RN-RF058-001 a RN-RF058-012)

---

## UC00 — Listar Tipos de Bilhetes

### Objetivo
Permitir que o usuário visualize todos os tipos de bilhetes cadastrados no sistema do seu próprio tenant.

### Pré-condições
- Usuário autenticado
- Permissão `CAD.TIPOS_BILHETES.VIEW`

### Pós-condições
- Lista exibida conforme filtros e paginação aplicados

### Fluxo Principal
- **FP-UC00-001:** Usuário acessa a funcionalidade pelo menu "Cadastros > Tipos de Bilhetes"
- **FP-UC00-002:** Sistema valida permissão `CAD.TIPOS_BILHETES.VIEW`
- **FP-UC00-003:** Sistema carrega tipos de bilhetes do tenant (WHERE EmpresaId = {usuário.EmpresaId} AND Excluido = false)
- **FP-UC00-004:** Sistema aplica paginação padrão (10 itens/página) e ordenação por Nome (A-Z)
- **FP-UC00-005:** Sistema exibe grid com colunas: Nome, Descrição, Status, Ações

### Fluxos Alternativos
- **FA-UC00-001:** Buscar por Nome ou Descrição
  - Usuário digita termo na caixa de busca
  - Sistema filtra registros contendo o termo (case-insensitive)
  - Sistema exibe resultados filtrados

- **FA-UC00-002:** Ordenar por coluna
  - Usuário clica no cabeçalho de coluna (Nome, Status)
  - Sistema alterna ordenação (ASC ↔ DESC)
  - Sistema recarrega lista com nova ordenação

- **FA-UC00-003:** Filtrar por Status
  - Usuário seleciona filtro: Ativo / Inativo / Todos
  - Sistema aplica filtro (WHERE Ativo = {filtro})
  - Sistema exibe apenas registros correspondentes

### Fluxos de Exceção
- **FE-UC00-001:** Usuário sem permissão
  - Sistema retorna HTTP 403 Forbidden
  - Sistema exibe mensagem: "Você não possui permissão para acessar Tipos de Bilhetes"

- **FE-UC00-002:** Nenhum registro encontrado
  - Sistema exibe estado vazio com mensagem: "Nenhum tipo de bilhete encontrado"
  - Sistema exibe botão "Novo Tipo de Bilhete" (se permissão CREATE)

### Regras de Negócio
- **RN-RF058-007:** Apenas tipos de bilhetes do tenant do usuário são exibidos (multi-tenancy)
- **RN-RF058-008:** Tipos excluídos (Excluido = true) NÃO aparecem na listagem
- **RN-RF058-012:** Filtros aplicados (Status, Busca) devem ser respeitados
- **RN-RF058-011:** Permissão `CAD.TIPOS_BILHETES.VIEW` é obrigatória

### Critérios de Aceite
- **CA-UC00-001:** A lista DEVE exibir apenas tipos de bilhetes do tenant do usuário autenticado (WHERE EmpresaId = {usuário.EmpresaId})
- **CA-UC00-002:** Tipos excluídos (Excluido = true) NÃO devem aparecer na listagem padrão
- **CA-UC00-003:** Paginação DEVE ser aplicada com limite padrão de 10 registros por página
- **CA-UC00-004:** Sistema DEVE permitir ordenação por Nome (A-Z / Z-A)
- **CA-UC00-005:** Filtros DEVEM ser acumuláveis (Busca + Status) e refletir na URL
- **CA-UC00-006:** Grid DEVE exibir colunas: Nome, Descrição, Status (Ativo/Inativo), Ações
- **CA-UC00-007:** Busca DEVE funcionar com case-insensitive e buscar em Nome E Descrição

---

## UC01 — Criar Tipo de Bilhete

### Objetivo
Permitir a criação de um novo tipo de bilhete no sistema.

### Pré-condições
- Usuário autenticado
- Permissão `CAD.TIPOS_BILHETES.CREATE`

### Pós-condições
- Tipo de bilhete persistido no banco de dados
- Auditoria registrada (CREATE)
- EmpresaId preenchido automaticamente
- Status padrão Ativo (true)

### Fluxo Principal
- **FP-UC01-001:** Usuário clica em "Novo Tipo de Bilhete"
- **FP-UC01-002:** Sistema valida permissão `CAD.TIPOS_BILHETES.CREATE`
- **FP-UC01-003:** Sistema exibe formulário de criação
- **FP-UC01-004:** Usuário preenche campos obrigatórios: Nome, Descrição
- **FP-UC01-005:** Usuário clica em "Salvar"
- **FP-UC01-006:** Sistema valida dados conforme regras de negócio (RN-RF058-001 a RN-RF058-006)
- **FP-UC01-007:** Sistema valida que Nome é único no tenant (RN-RF058-001)
- **FP-UC01-008:** Sistema preenche automaticamente: EmpresaId (do usuário logado), DataCriacao (agora), UsuarioCriacaoId (usuário logado), Ativo (true), Excluido (false)
- **FP-UC01-009:** Sistema persiste registro no banco de dados
- **FP-UC01-010:** Sistema registra auditoria (operação: CREATE, código: TIPO_BILHETE_CREATED)
- **FP-UC01-011:** Sistema exibe mensagem de sucesso: "Tipo de bilhete criado com sucesso"
- **FP-UC01-012:** Sistema redireciona para listagem ou exibe formulário limpo (se "Salvar e criar outro")

### Fluxos Alternativos
- **FA-UC01-001:** Salvar e criar outro
  - Após salvar com sucesso, usuário escolhe "Salvar e criar outro"
  - Sistema cria registro e mantém usuário no formulário (campos limpos)

- **FA-UC01-002:** Cancelar criação
  - Usuário clica em "Cancelar" antes de salvar
  - Sistema descarta dados e redireciona para listagem

### Fluxos de Exceção
- **FE-UC01-001:** Nome vazio ou com menos de 3 caracteres
  - Sistema valida campo Nome (RN-RF058-002)
  - Sistema exibe erro: "O nome deve ter no mínimo 3 caracteres"
  - Formulário permanece aberto para correção

- **FE-UC01-002:** Nome excede 100 caracteres
  - Sistema valida campo Nome (RN-RF058-003)
  - Sistema exibe erro: "O nome não pode exceder 100 caracteres"

- **FE-UC01-003:** Nome contém caracteres especiais inválidos
  - Sistema valida formato (RN-RF058-004, regex: `^[a-zA-Z0-9À-ÿ\s\-]+$`)
  - Sistema exibe erro: "O nome pode conter apenas letras, números, espaços e hífen"

- **FE-UC01-004:** Nome duplicado (case-insensitive)
  - Sistema valida unicidade no tenant (RN-RF058-001)
  - Sistema exibe erro: "Já existe um tipo de bilhete com este nome"

- **FE-UC01-005:** Descrição vazia ou com menos de 10 caracteres
  - Sistema valida campo Descrição (RN-RF058-005)
  - Sistema exibe erro: "A descrição é obrigatória e deve ter no mínimo 10 caracteres"

- **FE-UC01-006:** Descrição excede 500 caracteres
  - Sistema valida campo Descrição (RN-RF058-006)
  - Sistema exibe erro: "A descrição não pode exceder 500 caracteres"

- **FE-UC01-007:** Erro inesperado ao salvar
  - Sistema retorna HTTP 500
  - Sistema exibe erro genérico: "Erro ao criar tipo de bilhete. Tente novamente"
  - Sistema registra erro no log para troubleshooting

### Regras de Negócio
- **RN-RF058-001:** Nome único no tenant (case-insensitive)
- **RN-RF058-002:** Nome mínimo 3 caracteres
- **RN-RF058-003:** Nome máximo 100 caracteres
- **RN-RF058-004:** Formato de Nome válido (regex)
- **RN-RF058-005:** Descrição obrigatória com mínimo 10 caracteres
- **RN-RF058-006:** Descrição máximo 500 caracteres
- **RN-RF058-007:** EmpresaId preenchido automaticamente (multi-tenancy)
- **RN-RF058-009:** Auditoria obrigatória (CREATE)
- **RN-RF058-010:** Status padrão Ativo (true)
- **RN-RF058-011:** Permissão `CAD.TIPOS_BILHETES.CREATE` obrigatória

### Critérios de Aceite
- **CA-UC01-001:** Todos os campos obrigatórios (Nome, Descrição) DEVEM ser validados antes de persistir
- **CA-UC01-002:** EmpresaId DEVE ser preenchido automaticamente com o tenant do usuário autenticado
- **CA-UC01-003:** UsuarioCriacaoId DEVE ser preenchido automaticamente com o ID do usuário autenticado
- **CA-UC01-004:** DataCriacao DEVE ser preenchido automaticamente com timestamp atual (UTC)
- **CA-UC01-005:** Ativo DEVE ser preenchido automaticamente com valor padrão true
- **CA-UC01-006:** Excluido DEVE ser preenchido automaticamente com valor padrão false
- **CA-UC01-007:** Sistema DEVE retornar erro claro se validação de Nome falhar (duplicidade, formato, tamanho)
- **CA-UC01-008:** Sistema DEVE retornar erro claro se validação de Descrição falhar
- **CA-UC01-009:** Auditoria DEVE ser registrada APÓS sucesso da criação (operação: CREATE)
- **CA-UC01-010:** Validação de unicidade DEVE ser case-insensitive (LOWER(Nome))

---

## UC02 — Visualizar Tipo de Bilhete

### Objetivo
Permitir visualização detalhada de um tipo de bilhete específico.

### Pré-condições
- Usuário autenticado
- Permissão `CAD.TIPOS_BILHETES.VIEW`
- Tipo de bilhete existe e pertence ao tenant do usuário

### Pós-condições
- Dados do tipo de bilhete exibidos corretamente
- Auditoria registrada (ACCESS)

### Fluxo Principal
- **FP-UC02-001:** Usuário seleciona tipo de bilhete na listagem (clica em "Visualizar" ou no nome)
- **FP-UC02-002:** Sistema valida permissão `CAD.TIPOS_BILHETES.VIEW`
- **FP-UC02-003:** Sistema valida que tipo de bilhete pertence ao tenant do usuário (WHERE Id = {id} AND EmpresaId = {usuário.EmpresaId})
- **FP-UC02-004:** Sistema carrega dados do tipo de bilhete
- **FP-UC02-005:** Sistema exibe tela de visualização (modo somente leitura) com:
  - Nome
  - Descrição
  - Status (Ativo/Inativo)
  - Data de Criação
  - Usuário que Criou
  - Data da Última Alteração
  - Usuário que Alterou
- **FP-UC02-006:** Sistema registra auditoria (operação: ACCESS, código: TIPO_BILHETE_ACCESSED)
- **FP-UC02-007:** Sistema exibe botões: "Editar" (se permissão EDIT), "Voltar"

### Fluxos de Exceção
- **FE-UC02-001:** Tipo de bilhete não existe
  - Sistema retorna HTTP 404 Not Found
  - Sistema exibe mensagem: "Tipo de bilhete não encontrado"

- **FE-UC02-002:** Tipo de bilhete pertence a outro tenant
  - Sistema retorna HTTP 404 Not Found (não vaza informação de existência)
  - Sistema exibe mensagem: "Tipo de bilhete não encontrado"

- **FE-UC02-003:** Usuário sem permissão
  - Sistema retorna HTTP 403 Forbidden
  - Sistema exibe mensagem: "Você não possui permissão para visualizar tipos de bilhetes"

### Regras de Negócio
- **RN-RF058-007:** Usuário SÓ pode visualizar tipos de bilhetes do próprio tenant (isolamento)
- **RN-RF058-009:** Visualização DEVE ser auditada (ACCESS)
- **RN-RF058-011:** Permissão `CAD.TIPOS_BILHETES.VIEW` obrigatória

### Critérios de Aceite
- **CA-UC02-001:** Usuário SÓ pode visualizar tipos de bilhetes do próprio tenant (WHERE EmpresaId = {usuário.EmpresaId})
- **CA-UC02-002:** Informações de auditoria DEVEM ser exibidas: DataCriacao, UsuarioCriacaoId (nome), DataAlteracao, UsuarioAlteracaoId (nome)
- **CA-UC02-003:** Tentativa de acessar tipo de outro tenant DEVE retornar HTTP 404 (NÃO vazar informação)
- **CA-UC02-004:** Tentativa de acessar tipo inexistente DEVE retornar HTTP 404
- **CA-UC02-005:** Dados exibidos DEVEM corresponder exatamente ao estado atual no banco
- **CA-UC02-006:** Sistema DEVE registrar auditoria de acesso (operação: ACCESS)
- **CA-UC02-007:** Botão "Editar" SÓ aparece se usuário tiver permissão `CAD.TIPOS_BILHETES.EDIT`

---

## UC03 — Editar Tipo de Bilhete

### Objetivo
Permitir alteração controlada dos dados de um tipo de bilhete existente.

### Pré-condições
- Usuário autenticado
- Permissão `CAD.TIPOS_BILHETES.EDIT`
- Tipo de bilhete existe e pertence ao tenant do usuário

### Pós-condições
- Registro atualizado no banco de dados
- Auditoria registrada (UPDATE) com dados antes/depois
- DataAlteracao e UsuarioAlteracaoId atualizados

### Fluxo Principal
- **FP-UC03-001:** Usuário seleciona tipo de bilhete e clica em "Editar"
- **FP-UC03-002:** Sistema valida permissão `CAD.TIPOS_BILHETES.EDIT`
- **FP-UC03-003:** Sistema valida que tipo pertence ao tenant do usuário
- **FP-UC03-004:** Sistema carrega dados atuais do tipo de bilhete
- **FP-UC03-005:** Sistema exibe formulário preenchido com dados atuais (campos editáveis: Nome, Descrição, Status)
- **FP-UC03-006:** Usuário altera campos desejados
- **FP-UC03-007:** Usuário clica em "Salvar"
- **FP-UC03-008:** Sistema valida alterações conforme regras de negócio (RN-RF058-001 a RN-RF058-006)
- **FP-UC03-009:** Sistema valida que Nome continua único no tenant (se foi alterado)
- **FP-UC03-010:** Sistema atualiza campos: Nome, Descrição, Ativo, DataAlteracao (agora), UsuarioAlteracaoId (usuário logado)
- **FP-UC03-011:** Sistema persiste alterações no banco de dados
- **FP-UC03-012:** Sistema registra auditoria (operação: UPDATE, código: TIPO_BILHETE_UPDATED) com dados antes/depois (JSON)
- **FP-UC03-013:** Sistema exibe mensagem de sucesso: "Tipo de bilhete atualizado com sucesso"
- **FP-UC03-014:** Sistema redireciona para visualização ou listagem

### Fluxos Alternativos
- **FA-UC03-001:** Cancelar edição
  - Usuário clica em "Cancelar" antes de salvar
  - Sistema descarta alterações e redireciona para visualização

### Fluxos de Exceção
- **FE-UC03-001:** Nome vazio ou com menos de 3 caracteres
  - Sistema valida campo Nome (RN-RF058-002)
  - Sistema exibe erro: "O nome deve ter no mínimo 3 caracteres"
  - Formulário permanece aberto para correção

- **FE-UC03-002:** Nome excede 100 caracteres
  - Sistema valida campo Nome (RN-RF058-003)
  - Sistema exibe erro: "O nome não pode exceder 100 caracteres"

- **FE-UC03-003:** Nome contém caracteres especiais inválidos
  - Sistema valida formato (RN-RF058-004)
  - Sistema exibe erro: "O nome pode conter apenas letras, números, espaços e hífen"

- **FE-UC03-004:** Nome duplicado com outro tipo (case-insensitive)
  - Sistema valida unicidade (RN-RF058-001, excluindo próprio registro)
  - Sistema exibe erro: "Já existe outro tipo de bilhete com este nome"

- **FE-UC03-005:** Descrição vazia ou com menos de 10 caracteres
  - Sistema valida campo Descrição (RN-RF058-005)
  - Sistema exibe erro: "A descrição é obrigatória e deve ter no mínimo 10 caracteres"

- **FE-UC03-006:** Descrição excede 500 caracteres
  - Sistema valida campo Descrição (RN-RF058-006)
  - Sistema exibe erro: "A descrição não pode exceder 500 caracteres"

- **FE-UC03-007:** Conflito de edição concorrente
  - Outro usuário editou o registro enquanto atual estava editando
  - Sistema detecta versão desatualizada
  - Sistema exibe erro: "Este registro foi alterado por outro usuário. Recarregue a página e tente novamente"

- **FE-UC03-008:** Tipo de bilhete pertence a outro tenant
  - Sistema retorna HTTP 404 Not Found
  - Sistema exibe mensagem: "Tipo de bilhete não encontrado"

### Regras de Negócio
- **RN-RF058-001:** Nome único no tenant (excluindo próprio registro)
- **RN-RF058-002:** Nome mínimo 3 caracteres
- **RN-RF058-003:** Nome máximo 100 caracteres
- **RN-RF058-004:** Formato de Nome válido
- **RN-RF058-005:** Descrição obrigatória com mínimo 10 caracteres
- **RN-RF058-006:** Descrição máximo 500 caracteres
- **RN-RF058-007:** Usuário SÓ pode editar tipos do próprio tenant
- **RN-RF058-009:** Auditoria obrigatória (UPDATE) com dados antes/depois
- **RN-RF058-011:** Permissão `CAD.TIPOS_BILHETES.EDIT` obrigatória

### Critérios de Aceite
- **CA-UC03-001:** UsuarioAlteracaoId DEVE ser preenchido automaticamente com ID do usuário autenticado
- **CA-UC03-002:** DataAlteracao DEVE ser preenchido automaticamente com timestamp atual (UTC)
- **CA-UC03-003:** Apenas campos alterados DEVEM ser validados (validação incremental)
- **CA-UC03-004:** Sistema DEVE detectar conflitos de edição concorrente (optimistic locking)
- **CA-UC03-005:** Tentativa de editar tipo de outro tenant DEVE retornar HTTP 404
- **CA-UC03-006:** Auditoria DEVE registrar estado anterior E novo estado (JSON antes/depois)
- **CA-UC03-007:** Validação de unicidade de Nome DEVE excluir próprio registro (WHERE Nome = {valor} AND Id != {id})
- **CA-UC03-008:** Campos NÃO editáveis (EmpresaId, DataCriacao, UsuarioCriacaoId) NÃO devem ser alterados

---

## UC04 — Inativar Tipo de Bilhete

### Objetivo
Permitir exclusão lógica de tipos de bilhetes (soft delete), alterando status para Inativo.

### Pré-condições
- Usuário autenticado
- Permissão `CAD.TIPOS_BILHETES.DELETE`
- Tipo de bilhete existe e pertence ao tenant do usuário

### Pós-condições
- Campo Excluido marcado como true (soft delete)
- Tipo não aparece mais em listagens padrão
- Auditoria registrada (DELETE)
- Histórico preservado (registro permanece no banco)

### Fluxo Principal
- **FP-UC04-001:** Usuário seleciona tipo de bilhete e clica em "Inativar"
- **FP-UC04-002:** Sistema exibe confirmação: "Deseja realmente inativar este tipo de bilhete?"
- **FP-UC04-003:** Usuário confirma ação
- **FP-UC04-004:** Sistema valida permissão `CAD.TIPOS_BILHETES.DELETE`
- **FP-UC04-005:** Sistema valida que tipo pertence ao tenant do usuário
- **FP-UC04-006:** Sistema verifica se tipo está em uso (bilhetes associados) - apenas para ALERTA, NÃO bloqueia
- **FP-UC04-007:** Se tipo está em uso, sistema exibe alerta: "Este tipo possui bilhetes associados. Tem certeza que deseja inativá-lo?"
- **FP-UC04-008:** Usuário confirma novamente (se alerta exibido)
- **FP-UC04-009:** Sistema atualiza campos: Excluido = true, DataAlteracao = agora, UsuarioAlteracaoId = usuário logado
- **FP-UC04-010:** Sistema persiste alteração (UPDATE)
- **FP-UC04-011:** Sistema registra auditoria (operação: DELETE, código: TIPO_BILHETE_DELETED)
- **FP-UC04-012:** Sistema exibe mensagem de sucesso: "Tipo de bilhete inativado com sucesso"
- **FP-UC04-013:** Sistema remove tipo da listagem (refresh)

### Fluxos Alternativos
- **FA-UC04-001:** Cancelar exclusão
  - Usuário clica em "Cancelar" na confirmação
  - Sistema descarta ação e retorna para listagem

- **FA-UC04-002:** Exclusão em lote (futuro)
  - Usuário seleciona múltiplos tipos (checkboxes)
  - Usuário clica em "Inativar Selecionados"
  - Sistema executa soft delete para todos (validações individuais)

### Fluxos de Exceção
- **FE-UC04-001:** Tipo de bilhete já está inativado (Excluido = true)
  - Sistema retorna HTTP 404 Not Found (tipo não aparece na listagem)
  - OU sistema exibe mensagem: "Este tipo já foi inativado"

- **FE-UC04-002:** Tipo de bilhete pertence a outro tenant
  - Sistema retorna HTTP 404 Not Found
  - Sistema exibe mensagem: "Tipo de bilhete não encontrado"

- **FE-UC04-003:** Usuário sem permissão
  - Sistema retorna HTTP 403 Forbidden
  - Sistema exibe mensagem: "Você não possui permissão para inativar tipos de bilhetes"

### Regras de Negócio
- **RN-RF058-007:** Usuário SÓ pode inativar tipos do próprio tenant
- **RN-RF058-008:** Exclusão SEMPRE lógica (soft delete), NUNCA física
- **RN-RF058-009:** Auditoria obrigatória (DELETE)
- **RN-RF058-011:** Permissão `CAD.TIPOS_BILHETES.DELETE` obrigatória

### Critérios de Aceite
- **CA-UC04-001:** Exclusão DEVE ser sempre lógica (soft delete) via campo Excluido = true
- **CA-UC04-002:** Sistema DEVE verificar dependências (bilhetes associados) ANTES de inativar, MAS permitir inativação mesmo com dependências (apenas alerta)
- **CA-UC04-003:** Sistema DEVE exigir confirmação explícita do usuário antes de inativar
- **CA-UC04-004:** Excluido DEVE ser atualizado para true
- **CA-UC04-005:** DataAlteracao DEVE ser preenchido com timestamp atual
- **CA-UC04-006:** UsuarioAlteracaoId DEVE ser preenchido com ID do usuário autenticado
- **CA-UC04-007:** Tipo inativado NÃO deve aparecer em listagens padrão (WHERE Excluido = false)
- **CA-UC04-008:** Registro inativado DEVE permanecer no banco de dados (preservação de histórico)
- **CA-UC04-009:** Auditoria DEVE registrar operação DELETE com dados do tipo inativado

---

## 4. MATRIZ DE RASTREABILIDADE

| UC | Regras de Negócio Cobertas |
|----|---------------------------|
| UC00 | RN-RF058-007, RN-RF058-008, RN-RF058-011, RN-RF058-012 |
| UC01 | RN-RF058-001, RN-RF058-002, RN-RF058-003, RN-RF058-004, RN-RF058-005, RN-RF058-006, RN-RF058-007, RN-RF058-009, RN-RF058-010, RN-RF058-011 |
| UC02 | RN-RF058-007, RN-RF058-009, RN-RF058-011 |
| UC03 | RN-RF058-001, RN-RF058-002, RN-RF058-003, RN-RF058-004, RN-RF058-005, RN-RF058-006, RN-RF058-007, RN-RF058-009, RN-RF058-011 |
| UC04 | RN-RF058-007, RN-RF058-008, RN-RF058-009, RN-RF058-011 |

**Cobertura Total:** 100% das 12 regras de negócio do RF058 (RN-RF058-001 a RN-RF058-012)

---

## 5. EXCLUSÕES

Funcionalidades explicitamente FORA do escopo deste RF:

- Gestão de bilhetes propriamente dita (RF separado)
- Workflow de atendimento de bilhetes
- Tarifação de bilhetes (mencionado incorretamente em versão anterior - NÃO faz parte deste RF)
- Sistema de tarifas por horário/destino/volume
- SLA e métricas de tempo
- Integração com sistemas externos de ticketing
- Dashboard e relatórios analíticos

**Nota Importante:** O UC-RF058.md versão 1.0 mencionava "tarifação" e "bilhetes telefônicos", mas o escopo oficial do RF058 (conforme RF058.md e RF058.yaml) é exclusivamente sobre **cadastro de tipos de bilhetes** (categorias para classificar bilhetes de suporte), NÃO sobre tarifação ou telecomunicações.

---

## CHANGELOG

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 2.0 | 2025-12-31 | Agência ALC - alc.dev.br | Recriação completa conforme template v2.0 - Separação RF/RL, cobertura 100% de 12 RNs, remoção de conteúdo incorreto sobre tarifação |
| 1.0 | 2025-12-18 | - | Versão inicial (continha escopo incorreto sobre tarifação) |
