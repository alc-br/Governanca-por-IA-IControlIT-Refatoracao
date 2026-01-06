# UC-RF024 — Casos de Uso Canônicos

**RF:** RF024 — Gestão de Departamentos e Estrutura Organizacional
**Versão:** 2.0
**Data:** 2025-12-31
**Autor:** Agência ALC - alc.dev.br
**Epic:** EPIC006-FIN - Financeiro Base
**Fase:** Fase 3 - Financeiro I - Base Contábil

---

## 1. OBJETIVO DO DOCUMENTO

Este documento descreve **todos os Casos de Uso (UC)** derivados do **RF024**, cobrindo integralmente o comportamento funcional esperado para gestão de departamentos organizacionais com hierarquia recursiva ilimitada, organograma visual interativo, lotação matricial de colaboradores, workflow de movimentações e sincronização com Azure AD.

Os UCs aqui definidos servem como **contrato comportamental**, sendo a **fonte primária** para geração de:
- Casos de Teste (TC-RF024.yaml)
- Massas de Teste (MT-RF024.yaml)
- Evidências de auditoria e validação funcional
- Execução por agentes de IA (tester, QA, E2E)

---

## 2. SUMÁRIO DE CASOS DE USO

| ID | Nome | Ator Principal |
|----|------|----------------|
| UC00 | Listar Departamentos | Usuário Autenticado |
| UC01 | Criar Departamento | Admin / Super Admin |
| UC02 | Visualizar Departamento | Usuário Autenticado |
| UC03 | Editar Departamento | Admin / Super Admin / Gestor |
| UC04 | Excluir Departamento | Super Admin |
| UC05 | Visualizar Organograma | Usuário Autenticado |
| UC06 | Alocar Colaborador em Departamento | Admin / RH |
| UC07 | Criar Movimentação Interdepartamental | Gestor / RH |
| UC08 | Aprovar Movimentação | Líder Origem / Líder Destino / RH |
| UC09 | Sincronizar com Azure AD | Super Admin |
| UC10 | Visualizar Dashboard Headcount | Gestor / RH |

---

## 3. PADRÕES GERAIS APLICÁVEIS A TODOS OS UCs

- Todos os acessos respeitam **isolamento por tenant** (Id_Fornecedor)
- Todas as ações exigem **permissão explícita** (RBAC)
- Erros não devem vazar informações sensíveis
- Auditoria deve registrar **quem**, **quando** e **qual ação**
- Mensagens devem ser claras, previsíveis e rastreáveis
- Hierarquia recursiva deve ser validada para evitar loops infinitos
- Multi-tenancy obrigatório em todas as operações

---

## UC00 — Listar Departamentos

### Objetivo
Permitir que o usuário visualize departamentos disponíveis do seu próprio tenant com opções de filtro, ordenação e paginação.

### Pré-condições
- Usuário autenticado
- Permissão `CAD.DEPARTAMENTOS.VIEW_ANY` (implícita para autenticados)

### Pós-condições
- Lista exibida conforme filtros e paginação
- Apenas departamentos do tenant do usuário são exibidos

### Fluxo Principal
- **FP-UC00-001:** Usuário acessa a funcionalidade "Departamentos" pelo menu
- **FP-UC00-002:** Sistema valida permissão do usuário
- **FP-UC00-003:** Sistema carrega departamentos do tenant (query filter global)
- **FP-UC00-004:** Sistema aplica paginação padrão (20 registros por página)
- **FP-UC00-005:** Sistema aplica ordenação padrão (Nome_Departamento ASC)
- **FP-UC00-006:** Sistema exibe lista com colunas: Código, Nome, Tipo, Líder, Qtd Colaboradores, Nível Hierárquico

### Fluxos Alternativos
- **FA-UC00-001:** Buscar por termo - Usuário digita termo, sistema filtra por Codigo_Departamento ou Nome_Departamento (LIKE)
- **FA-UC00-002:** Ordenar por coluna - Usuário clica em cabeçalho, sistema aplica ordenação crescente/decrescente
- **FA-UC00-003:** Filtrar por Tipo - Usuário seleciona tipo (Diretoria/Gerencia/Coordenacao/Equipe), sistema filtra
- **FA-UC00-004:** Filtrar por Líder - Usuário seleciona líder, sistema filtra por Id_Usuario_Lider
- **FA-UC00-005:** Filtrar por Nível Hierárquico - Usuário seleciona nível (1, 2, 3, 4+), sistema filtra

### Fluxos de Exceção
- **FE-UC00-001:** Usuário sem permissão → HTTP 403 Forbidden, mensagem "Acesso negado"
- **FE-UC00-002:** Nenhum registro encontrado → Exibe estado vazio "Nenhum departamento cadastrado"
- **FE-UC00-003:** Erro de conexão com banco → HTTP 500, mensagem "Erro ao carregar departamentos, tente novamente"

### Regras de Negócio
- **RN-UC-00-001**: Somente departamentos do tenant do usuário autenticado (Id_Fornecedor)
- **RN-UC-00-002**: Registros soft-deleted NÃO aparecem na listagem (Deleted_At IS NULL)
- **RN-UC-00-003**: Paginação padrão de 20 registros (configurável até 100)
- **RN-UC-00-004**: Ordenação padrão por Nome_Departamento ASC

### Critérios de Aceite
- **CA-UC00-001:** A lista DEVE exibir apenas departamentos do tenant do usuário autenticado
- **CA-UC00-002:** Departamentos excluídos (soft delete) NÃO devem aparecer na listagem
- **CA-UC00-003:** Paginação DEVE ser aplicada com limite padrão de 20 registros
- **CA-UC00-004:** Sistema DEVE permitir ordenação por qualquer coluna visível
- **CA-UC00-005:** Filtros DEVEM ser acumuláveis e refletir na URL (query params)
- **CA-UC00-006:** Qtd_Colaboradores DEVE exibir total de lotações principais ativas

---

## UC01 — Criar Departamento

### Objetivo
Permitir a criação de um novo departamento com hierarquia recursiva, líder designado e validação de código único.

### Pré-condições
- Usuário autenticado
- Permissão `CAD.DEPARTAMENTOS.CREATE`
- Roles autorizadas: Super Admin, Admin

### Pós-condições
- Departamento persistido no banco com auditoria
- Líder notificado via email, push e inbox
- Azure AD group criado (se sincronização ativa)
- Auditoria registrada em Departamento_Historico

### Fluxo Principal
- **FP-UC01-001:** Usuário clica em "Novo Departamento"
- **FP-UC01-002:** Sistema valida permissão CAD.DEPARTAMENTOS.CREATE
- **FP-UC01-003:** Sistema exibe formulário com campos obrigatórios
- **FP-UC01-004:** Usuário informa:
  - Código Departamento (ex: DIR-TI)
  - Nome Departamento (ex: Diretoria de Tecnologia)
  - Tipo Departamento (enum: Diretoria/Gerencia/Coordenacao/Equipe)
  - Departamento Pai (nullable, self-referencing FK)
  - Líder (FK Usuario - obrigatório exceto tipo Equipe)
- **FP-UC01-005:** Usuário clica em "Salvar"
- **FP-UC01-006:** Sistema valida dados (FluentValidation):
  - Código único por Fornecedor
  - Código formato alfanumérico regex: `^[A-Z]{3,5}-[A-Z0-9]{2,20}$`
  - Nome obrigatório (3-200 caracteres)
  - Líder existe e está ativo
  - Departamento Pai válido (se informado)
- **FP-UC01-007:** Sistema valida referências circulares na hierarquia (algoritmo HashSet)
- **FP-UC01-008:** Sistema calcula Nivel_Hierarquia e Caminho_Hierarquico (trigger ou aplicação)
- **FP-UC01-009:** Sistema cria registro com campos automáticos:
  - Id_Fornecedor (tenant do usuário autenticado)
  - Created_By (Id do usuário autenticado)
  - Created_At (timestamp atual)
  - Qtd_Colaboradores = 0
- **FP-UC01-010:** Sistema registra auditoria em Departamento_Historico (tipo: Criacao)
- **FP-UC01-011:** Sistema envia notificação multicanal ao líder designado (email + push + inbox)
- **FP-UC01-012:** Sistema retorna HTTP 201 Created com ID do departamento
- **FP-UC01-013:** Frontend exibe mensagem "Departamento criado com sucesso"

### Fluxos Alternativos
- **FA-UC01-001:** Salvar e criar outro - Usuário marca checkbox "Criar outro", sistema limpa formulário após salvar
- **FA-UC01-002:** Cancelar criação - Usuário clica em "Cancelar", sistema descarta alterações e retorna à listagem

### Fluxos de Exceção
- **FE-UC01-001:** Código duplicado → HTTP 409 Conflict, mensagem "Código departamento já existe"
- **FE-UC01-002:** Código formato inválido → HTTP 422, mensagem "Código deve seguir formato [TIPO]-[NOME] (ex: DIR-TI)"
- **FE-UC01-003:** Líder inválido ou inativo → HTTP 422, mensagem "Líder inválido ou inativo"
- **FE-UC01-004:** Referência circular detectada → HTTP 422, mensagem "Referência circular detectada na hierarquia"
- **FE-UC01-005:** Departamento Pai não existe → HTTP 404, mensagem "Departamento pai não encontrado"
- **FE-UC01-006:** Departamento Pai de outro tenant → HTTP 403, mensagem "Departamento pai não pertence ao seu tenant"

### Regras de Negócio
- **RN-UC-01-001**: Código departamento único por Fornecedor (**RN-RF024-001**)
- **RN-UC-01-002**: Código formato alfanumérico regex: `^[A-Z]{3,5}-[A-Z0-9]{2,20}$` (**RN-RF024-001**)
- **RN-UC-01-003**: Hierarquia recursiva ilimitada via self-referencing FK (**RN-RF024-002**)
- **RN-UC-01-004**: Validação de referências circulares obrigatória (**RN-RF024-003**)
- **RN-UC-01-005**: Líder obrigatório para tipos Diretoria/Gerencia/Coordenacao (**RN-RF024-004**)
- **RN-UC-01-006**: Id_Fornecedor automático (tenant do usuário autenticado)
- **RN-UC-01-007**: Created_By automático (ID do usuário autenticado)
- **RN-UC-01-008**: Created_At automático (timestamp atual)
- **RN-UC-01-009**: Nivel_Hierarquia calculado automaticamente (1 = raiz, 2 = filho, etc.)
- **RN-UC-01-010**: Caminho_Hierarquico calculado (ex: "/DIR-TI/GER-DEV/COORD-BACKEND")
- **RN-UC-01-011**: Notificação multicanal ao líder (email + push + inbox) (**RN-RF024-010**)
- **RN-UC-01-012**: Auditoria completa em Departamento_Historico (**RN-RF024-015**)

### Critérios de Aceite
- **CA-UC01-001:** Todos os campos obrigatórios DEVEM ser validados antes de persistir
- **CA-UC01-002:** Id_Fornecedor DEVE ser preenchido automaticamente com o tenant do usuário autenticado
- **CA-UC01-003:** Created_By DEVE ser preenchido automaticamente com o ID do usuário autenticado
- **CA-UC01-004:** Created_At DEVE ser preenchido automaticamente com timestamp atual
- **CA-UC01-005:** Sistema DEVE retornar erro claro se validação falhar
- **CA-UC01-006:** Auditoria DEVE ser registrada APÓS sucesso da criação
- **CA-UC01-007:** Validação de referências circulares DEVE executar em O(n) onde n = profundidade hierarquia
- **CA-UC01-008:** Líder DEVE receber notificação multicanal (email + push + inbox) (**RN-RF024-010**)

---

## UC02 — Visualizar Departamento

### Objetivo
Permitir visualização detalhada de um departamento com informações de hierarquia, líder, colaboradores alocados e histórico de auditoria.

### Pré-condições
- Usuário autenticado
- Permissão implícita (todos autenticados podem visualizar)

### Pós-condições
- Dados completos do departamento exibidos
- Hierarquia visual (breadcrumb) exibida
- Lista de colaboradores alocados exibida

### Fluxo Principal
- **FP-UC02-001:** Usuário clica em "Visualizar" na listagem ou acessa por ID
- **FP-UC02-002:** Sistema valida autenticação do usuário
- **FP-UC02-003:** Sistema carrega departamento por ID
- **FP-UC02-004:** Sistema valida que departamento pertence ao tenant do usuário (query filter global)
- **FP-UC02-005:** Sistema carrega dados relacionados:
  - Departamento Pai (se houver)
  - Líder (Usuario)
  - Colaboradores alocados (Usuario_Departamento WHERE Fl_Ativo=1)
  - Filhos diretos (Departamentos WHERE Id_Departamento_Pai = ID)
- **FP-UC02-006:** Sistema exibe informações:
  - Código, Nome, Tipo
  - Nível Hierárquico e Caminho Hierárquico (breadcrumb)
  - Líder (nome, email, foto)
  - Qtd Colaboradores (lotações principais ativas)
  - Azure AD Object ID (se sincronizado)
  - Dados de auditoria (Created_By, Created_At, LastModified_By, LastModified_At)
- **FP-UC02-007:** Sistema exibe lista de colaboradores alocados:
  - Nome, Email, Tipo Lotação (Principal/DottedLine/Temporaria), Percentual Alocação, Dt_Inicio, Dt_Fim

### Fluxos Alternativos
- **FA-UC02-001:** Visualizar organograma a partir deste departamento - Usuário clica em "Ver Organograma", sistema redireciona para UC05 com departamento como raiz
- **FA-UC02-002:** Editar departamento - Usuário clica em "Editar", sistema redireciona para UC03 (se tiver permissão)

### Fluxos de Exceção
- **FE-UC02-001:** Departamento não existe → HTTP 404, mensagem "Departamento não encontrado"
- **FE-UC02-002:** Departamento de outro tenant → HTTP 404, mensagem "Departamento não encontrado" (sem vazar informação)
- **FE-UC02-003:** Departamento soft-deleted → HTTP 404, mensagem "Departamento não encontrado"

### Regras de Negócio
- **RN-UC-02-001**: Isolamento por tenant obrigatório (Id_Fornecedor)
- **RN-UC-02-002**: Informações de auditoria devem ser exibidas (Created_By, Created_At, LastModified_By, LastModified_At)
- **RN-UC-02-003**: Caminho hierárquico exibido como breadcrumb clicável (ex: Diretoria TI > Gerência Dev > Coordenação Backend)
- **RN-UC-02-004**: Colaboradores soft-deleted não aparecem na lista (Deleted_At IS NULL)

### Critérios de Aceite
- **CA-UC02-001:** Usuário SÓ pode visualizar departamentos do próprio tenant
- **CA-UC02-002:** Informações de auditoria DEVEM ser exibidas (Created_By, Created_At, LastModified_By, LastModified_At)
- **CA-UC02-003:** Tentativa de acessar departamento de outro tenant DEVE retornar 404
- **CA-UC02-004:** Tentativa de acessar departamento inexistente DEVE retornar 404
- **CA-UC02-005:** Dados exibidos DEVEM corresponder exatamente ao estado atual no banco
- **CA-UC02-006:** Breadcrumb hierárquico DEVE ser clicável e navegar para departamento pai

---

## UC03 — Editar Departamento

### Objetivo
Permitir alteração controlada de um departamento, incluindo mudança de hierarquia (reparenting), alteração de líder e atualização de dados.

### Pré-condições
- Usuário autenticado
- Permissão `CAD.DEPARTAMENTOS.UPDATE`
- Roles autorizadas: Super Admin, Admin, Gestor (próprio departamento)

### Pós-condições
- Departamento atualizado no banco
- Auditoria registrada em Departamento_Historico
- Níveis hierárquicos recalculados (se mudou pai)
- Líder notificado (se alterado)

### Fluxo Principal
- **FP-UC03-001:** Usuário clica em "Editar" na visualização ou listagem
- **FP-UC03-002:** Sistema valida permissão CAD.DEPARTAMENTOS.UPDATE
- **FP-UC03-003:** Sistema carrega dados atuais do departamento
- **FP-UC03-004:** Sistema valida que departamento pertence ao tenant do usuário
- **FP-UC03-005:** Sistema exibe formulário pré-preenchido com dados atuais
- **FP-UC03-006:** Usuário altera campos:
  - Nome Departamento
  - Tipo Departamento
  - Departamento Pai (permitindo "reparenting" - mudança de hierarquia)
  - Líder
- **FP-UC03-007:** Usuário clica em "Salvar"
- **FP-UC03-008:** Sistema valida dados (FluentValidation):
  - Nome obrigatório (3-200 caracteres)
  - Líder existe e está ativo
  - Departamento Pai válido (se informado)
  - Código NÃO pode ser alterado (campo readonly)
- **FP-UC03-009:** Sistema valida referências circulares na hierarquia (algoritmo HashSet) - **CRÍTICO para reparenting**
- **FP-UC03-010:** Sistema detecta mudanças:
  - Se mudou Departamento Pai → recalcula Nivel_Hierarquia e Caminho_Hierarquico de toda subárvore
  - Se mudou Líder → envia notificação ao novo líder
- **FP-UC03-011:** Sistema atualiza campos automáticos:
  - LastModified_By (ID do usuário autenticado)
  - LastModified_At (timestamp atual)
- **FP-UC03-012:** Sistema registra auditoria em Departamento_Historico (tipo: Alteracao ou Movimentacao_Hierarquia)
- **FP-UC03-013:** Sistema retorna HTTP 200 OK
- **FP-UC03-014:** Frontend exibe mensagem "Departamento atualizado com sucesso"

### Fluxos Alternativos
- **FA-UC03-001:** Cancelar edição - Usuário clica em "Cancelar", sistema descarta alterações e retorna à visualização
- **FA-UC03-002:** Alterar hierarquia (reparenting) - Usuário altera Departamento Pai, sistema valida loops e recalcula hierarquia de toda subárvore

### Fluxos de Exceção
- **FE-UC03-001:** Líder inválido ou inativo → HTTP 422, mensagem "Líder inválido ou inativo"
- **FE-UC03-002:** Referência circular detectada → HTTP 422, mensagem "Referência circular detectada na hierarquia" (**CRÍTICO para reparenting**)
- **FE-UC03-003:** Departamento Pai não existe → HTTP 404, mensagem "Departamento pai não encontrado"
- **FE-UC03-004:** Tentativa de alterar Código → HTTP 422, mensagem "Código do departamento não pode ser alterado"
- **FE-UC03-005:** Conflito de edição concorrente → HTTP 409 Conflict, mensagem "Departamento foi alterado por outro usuário, recarregue a página"

### Regras de Negócio
- **RN-UC-03-001**: LastModified_By automático (ID do usuário autenticado)
- **RN-UC-03-002**: LastModified_At automático (timestamp atual)
- **RN-UC-03-003**: Código departamento é IMUTÁVEL (não pode ser alterado)
- **RN-UC-03-004**: Validação de referências circulares obrigatória ao alterar Departamento Pai (**RN-RF024-003**)
- **RN-UC-03-005**: Recalcular Nivel_Hierarquia e Caminho_Hierarquico de toda subárvore se mudou Departamento Pai (**RN-RF024-002**)
- **RN-UC-03-006**: Notificar novo líder se alterado (**RN-RF024-010**)
- **RN-UC-03-007**: Auditoria completa em Departamento_Historico (**RN-RF024-015**)
- **RN-UC-03-008**: Detecção de edição concorrente (Optimistic Concurrency Control com RowVersion ou LastModified_At)

### Critérios de Aceite
- **CA-UC03-001:** LastModified_By DEVE ser preenchido automaticamente com ID do usuário autenticado
- **CA-UC03-002:** LastModified_At DEVE ser preenchido automaticamente com timestamp atual
- **CA-UC03-003:** Apenas campos alterados DEVEM ser validados
- **CA-UC03-004:** Sistema DEVE detectar conflitos de edição concorrente
- **CA-UC03-005:** Tentativa de editar departamento de outro tenant DEVE retornar 404
- **CA-UC03-006:** Auditoria DEVE registrar estado anterior e novo estado
- **CA-UC03-007:** Validação de referências circulares DEVE bloquear loops infinitos (**RN-RF024-003**)
- **CA-UC03-008:** Mudança de Departamento Pai DEVE recalcular hierarquia de toda subárvore
- **CA-UC03-009:** Novo líder DEVE receber notificação multicanal (**RN-RF024-010**)

---

## UC04 — Excluir Departamento

### Objetivo
Permitir exclusão lógica (soft delete) de departamentos sem colaboradores alocados ou departamentos filhos, preservando referências históricas.

### Pré-condições
- Usuário autenticado
- Permissão `CAD.DEPARTAMENTOS.DELETE`
- Role autorizada: Super Admin

### Pós-condições
- Departamento marcado como excluído (soft delete) via Deleted_At
- Auditoria registrada em Departamento_Historico
- Departamento não aparece em listagens padrão

### Fluxo Principal
- **FP-UC04-001:** Usuário clica em "Excluir" na visualização ou listagem
- **FP-UC04-002:** Sistema valida permissão CAD.DEPARTAMENTOS.DELETE
- **FP-UC04-003:** Sistema exibe modal de confirmação: "Tem certeza que deseja excluir o departamento [Nome]? Esta ação não pode ser desfeita."
- **FP-UC04-004:** Usuário clica em "Confirmar Exclusão"
- **FP-UC04-005:** Sistema verifica dependências:
  - Departamentos filhos (Departamentos WHERE Id_Departamento_Pai = ID)
  - Colaboradores alocados (Usuario_Departamento WHERE Fl_Ativo=1)
- **FP-UC04-006:** Se SEM dependências, sistema executa soft delete:
  - Define Deleted_At = timestamp atual
  - Define Deleted_By = ID do usuário autenticado
- **FP-UC04-007:** Sistema registra auditoria em Departamento_Historico (tipo: Exclusao)
- **FP-UC04-008:** Sistema retorna HTTP 200 OK
- **FP-UC04-009:** Frontend exibe mensagem "Departamento excluído com sucesso"
- **FP-UC04-010:** Frontend redireciona para listagem

### Fluxos Alternativos
- **FA-UC04-001:** Cancelar exclusão - Usuário clica em "Cancelar" no modal de confirmação, sistema cancela operação

### Fluxos de Exceção
- **FE-UC04-001:** Departamento tem filhos → HTTP 422, mensagem "Não é possível excluir departamento com departamentos filhos. Exclua ou mova os filhos primeiro."
- **FE-UC04-002:** Departamento tem colaboradores alocados → HTTP 422, mensagem "Não é possível excluir departamento com colaboradores alocados. Realoque os colaboradores primeiro."
- **FE-UC04-003:** Departamento já excluído → HTTP 404, mensagem "Departamento não encontrado"
- **FE-UC04-004:** Departamento de outro tenant → HTTP 404, mensagem "Departamento não encontrado"

### Regras de Negócio
- **RN-UC-04-001**: Exclusão sempre lógica (soft delete) via Deleted_At
- **RN-UC-04-002**: Departamentos com filhos BLOQUEIAM exclusão (**RN-RF024-002**)
- **RN-UC-04-003**: Departamentos com colaboradores alocados BLOQUEIAM exclusão (**RN-RF024-008**)
- **RN-UC-04-004**: Deleted_By automático (ID do usuário autenticado)
- **RN-UC-04-005**: Deleted_At automático (timestamp atual)
- **RN-UC-04-006**: Auditoria completa em Departamento_Historico (**RN-RF024-015**)

### Critérios de Aceite
- **CA-UC04-001:** Exclusão DEVE ser sempre lógica (soft delete) via Deleted_At
- **CA-UC04-002:** Sistema DEVE verificar dependências (filhos e colaboradores) ANTES de permitir exclusão
- **CA-UC04-003:** Sistema DEVE exigir confirmação explícita do usuário
- **CA-UC04-004:** Deleted_At DEVE ser preenchido com timestamp atual
- **CA-UC04-005:** Tentativa de excluir departamento com dependências DEVE retornar erro claro
- **CA-UC04-006:** Departamento excluído NÃO deve aparecer em listagens padrão
- **CA-UC04-007:** Auditoria DEVE registrar exclusão com tipo "Exclusao"

---

## UC05 — Visualizar Organograma

### Objetivo
Permitir visualização interativa do organograma completo da empresa em formato de árvore hierárquica usando D3.js, com funcionalidades de zoom, pan, collapse/expand, busca e exportação.

### Pré-condições
- Usuário autenticado
- Permissão implícita (todos autenticados podem visualizar organograma)

### Pós-condições
- Organograma visual renderizado no navegador
- Hierarquia completa carregada (com cache Redis)

### Fluxo Principal
- **FP-UC05-001:** Usuário acessa "Organograma" pelo menu
- **FP-UC05-002:** Sistema valida autenticação
- **FP-UC05-003:** Sistema consulta cache Redis (chave: `organograma:{tenant_id}`, TTL: 1h)
- **FP-UC05-004:** Se cache HIT, retorna DTO recursivo do cache
- **FP-UC05-005:** Se cache MISS, sistema executa query recursiva (CTE ou View):
  ```sql
  WITH RECURSIVE OrgTree AS (
    SELECT * FROM Departamento WHERE Id_Departamento_Pai IS NULL AND Deleted_At IS NULL
    UNION ALL
    SELECT d.* FROM Departamento d
    INNER JOIN OrgTree ot ON d.Id_Departamento_Pai = ot.Id
    WHERE d.Deleted_At IS NULL
  )
  SELECT * FROM OrgTree;
  ```
- **FP-UC05-006:** Sistema monta DTO recursivo (NodeDto):
  - Id, Nome, Tipo, Codigo, Lider (nome, foto), Qtd_Colaboradores
  - Children (array de NodeDto)
- **FP-UC05-007:** Sistema armazena em cache Redis (TTL: 1h)
- **FP-UC05-008:** Sistema retorna JSON para frontend
- **FP-UC05-009:** Frontend renderiza organograma D3.js v7:
  - Zoom: Mouse wheel / pinch mobile (scale 0.1x - 10x)
  - Pan: Drag & drop canvas
  - Collapse/Expand: Click em nó colapsa/expande subárvore
  - Tooltip: Hover mostra detalhes (líder, qtd colaboradores)

### Fluxos Alternativos
- **FA-UC05-001:** Buscar departamento - Usuário digita termo, sistema destaca caminho hierárquico completo até departamento encontrado
- **FA-UC05-002:** Filtrar por tipo - Usuário seleciona tipo (Diretoria/Gerencia/Coordenacao/Equipe), sistema filtra visualmente
- **FA-UC05-003:** Exportar organograma - Usuário clica em "Exportar", sistema gera:
  - PNG: `canvas.toDataURL()`
  - PDF: jsPDF com renderização canvas
  - SVG: `d3.serialize()`
- **FA-UC05-004:** Visualizar subárvore - Usuário clica com botão direito em nó, sistema renderiza organograma com aquele nó como raiz
- **FA-UC05-005:** Ver colaboradores - Usuário clica em departamento, sistema exibe sidebar com lista de colaboradores alocados

### Fluxos de Exceção
- **FE-UC05-001:** Nenhum departamento cadastrado → Exibe estado vazio "Nenhum departamento cadastrado"
- **FE-UC05-002:** Organograma muito grande (>500 nós) → HTTP 413 Payload Too Large, mensagem "Organograma muito grande, use filtros"
- **FE-UC05-003:** Erro ao renderizar D3.js → Frontend exibe mensagem "Erro ao carregar organograma, tente novamente"

### Regras de Negócio
- **RN-UC-05-001**: Organograma visual D3.js v7 interativo (**RN-RF024-009**)
- **RN-UC-05-002**: Cache Redis TTL 1h, invalidar ao criar/editar departamento (**RN-RF024-009**)
- **RN-UC-05-003**: Zoom mouse wheel / pinch mobile (scale 0.1x - 10x)
- **RN-UC-05-004**: Pan drag & drop canvas
- **RN-UC-05-005**: Collapse/Expand click nó
- **RN-UC-05-006**: Busca destaca caminho hierárquico completo
- **RN-UC-05-007**: Filtro por tipo departamento (Diretoria, Gerencia, Coordenacao, Equipe)
- **RN-UC-05-008**: Export PNG, PDF, SVG
- **RN-UC-05-009**: Limite absoluto de 500 nós para renderização (performance)

### Critérios de Aceite
- **CA-UC05-001:** Organograma DEVE renderizar hierarquia completa em <2 segundos para até 500 nós (**KPI Performance**)
- **CA-UC05-002:** Cache Redis DEVE ser invalidado ao criar/editar departamento
- **CA-UC05-003:** Zoom DEVE funcionar via mouse wheel e pinch mobile
- **CA-UC05-004:** Pan DEVE funcionar via drag & drop
- **CA-UC05-005:** Collapse/Expand DEVE colapsar/expandir subárvore ao clicar em nó
- **CA-UC05-006:** Busca DEVE destacar caminho hierárquico completo até departamento
- **CA-UC05-007:** Exportação DEVE gerar arquivos PNG, PDF e SVG válidos
- **CA-UC05-008:** Organogramas com >500 nós DEVEM retornar HTTP 413 com mensagem clara

---

## UC06 — Alocar Colaborador em Departamento

### Objetivo
Permitir alocação de colaborador em departamento com suporte a lotação principal (100%), dotted-line (parcial) e temporária (com data fim), respeitando limite de soma de alocações ≤100%.

### Pré-condições
- Usuário autenticado
- Permissão implícita Admin / RH
- Colaborador (Usuario) existe e está ativo
- Departamento existe e está ativo

### Pós-condições
- Colaborador alocado em departamento
- Qtd_Colaboradores atualizado automaticamente (trigger)
- Líder do departamento notificado (email + push + inbox)
- Auditoria registrada

### Fluxo Principal
- **FP-UC06-001:** Usuário acessa "Alocar Colaborador" em departamento
- **FP-UC06-002:** Sistema valida permissão
- **FP-UC06-003:** Sistema exibe formulário com campos:
  - Colaborador (autocomplete por nome/email)
  - Tipo Lotação (enum: Principal/DottedLine/Temporaria)
  - Percentual Alocação (DECIMAL 0-100, padrão 100)
  - Data Início (DATE obrigatória)
  - Data Fim (DATE nullable, obrigatória se Tipo=Temporaria)
- **FP-UC06-004:** Usuário preenche dados e clica em "Alocar"
- **FP-UC06-005:** Sistema valida:
  - Colaborador existe e está ativo
  - Departamento existe e está ativo
  - Percentual Alocação >0 e ≤100
  - Se Tipo=Principal: verifica se colaborador já tem lotação principal ativa (UNIQUE constraint)
  - Soma de alocações ativas do colaborador ≤100% (**RN-RF024-007**)
- **FP-UC06-006:** Sistema cria registro em Usuario_Departamento:
  - Id_Usuario, Id_Departamento, Tipo_Lotacao, Percentual_Alocacao, Dt_Inicio, Dt_Fim
  - Fl_Ativo = true
  - Created_By, Created_At (automáticos)
- **FP-UC06-007:** Trigger `trg_Usuario_Departamento_AtualizarQtdColaboradores` atualiza Qtd_Colaboradores do departamento (**RN-RF024-008**)
- **FP-UC06-008:** Sistema envia notificação multicanal ao líder do departamento (**RN-RF024-010**):
  - "João Silva foi alocado em seu departamento (TI > Desenvolvimento > Backend) em 31/12/2025 com 100% alocação"
- **FP-UC06-009:** SignalR Hub `DepartamentoHub` broadcast evento `OnColaboradorAlocado`
- **FP-UC06-010:** Sistema retorna HTTP 201 Created
- **FP-UC06-011:** Frontend exibe mensagem "Colaborador alocado com sucesso"

### Fluxos Alternativos
- **FA-UC06-001:** Alocação temporária - Usuário seleciona Tipo=Temporaria, sistema exige Data Fim
- **FA-UC06-002:** Dotted-line (matricial) - Usuário seleciona Tipo=DottedLine e Percentual parcial (ex: 30%), sistema valida soma ≤100%

### Fluxos de Exceção
- **FE-UC06-001:** Colaborador já tem lotação principal ativa → HTTP 422, mensagem "Colaborador já possui lotação principal ativa em outro departamento"
- **FE-UC06-002:** Soma de alocações >100% → HTTP 422, mensagem "Soma de alocações do colaborador excede 100%" (**RN-RF024-007**)
- **FE-UC06-003:** Percentual inválido (≤0 ou >100) → HTTP 422, mensagem "Percentual deve estar entre 1 e 100"
- **FE-UC06-004:** Data Fim anterior a Data Início → HTTP 422, mensagem "Data fim deve ser posterior a data início"
- **FE-UC06-005:** Tipo Temporaria sem Data Fim → HTTP 422, mensagem "Lotação temporária exige data fim"

### Regras de Negócio
- **RN-UC-06-001**: Dotted-line múltiplos departamentos, soma ≤100% (**RN-RF024-007**)
- **RN-UC-06-002**: Validação trigger: SUM(Percentual_Alocacao) WHERE Fl_Ativo=1 ≤100 (**RN-RF024-007**)
- **RN-UC-06-003**: UNIQUE (Id_Usuario, Tipo_Lotacao='Principal', Fl_Ativo=1) (**RN-RF024-007**)
- **RN-UC-06-004**: Atualização automática Qtd_Colaboradores via trigger (**RN-RF024-008**)
- **RN-UC-06-005**: Notificação multicanal ao líder (**RN-RF024-010**)
- **RN-UC-06-006**: SignalR broadcast OnColaboradorAlocado (**RN-RF024-010**)

### Critérios de Aceite
- **CA-UC06-001:** Sistema DEVE validar que soma de alocações ativas do colaborador ≤100%
- **CA-UC06-002:** Colaborador DEVE ter apenas UMA lotação principal ativa por vez
- **CA-UC06-003:** Trigger DEVE atualizar Qtd_Colaboradores automaticamente
- **CA-UC06-004:** Líder DEVE receber notificação multicanal (email + push + inbox)
- **CA-UC06-005:** SignalR DEVE broadcast evento OnColaboradorAlocado
- **CA-UC06-006:** Percentual DEVE estar entre 1 e 100
- **CA-UC06-007:** Lotação temporária DEVE exigir Data Fim

---

## UC07 — Criar Movimentação Interdepartamental

### Objetivo
Permitir criação de solicitação de transferência de colaborador entre departamentos com workflow de aprovação multinível (Líder Origem → Líder Destino → RH).

### Pré-condições
- Usuário autenticado
- Permissão implícita Gestor / RH
- Colaborador existe e tem lotação principal ativa
- Departamento Origem e Destino existem e estão ativos

### Pós-condições
- Movimentação criada com status Pendente
- Notificação enviada ao Líder do Departamento Origem

### Fluxo Principal
- **FP-UC07-001:** Usuário acessa "Criar Movimentação" em departamento ou colaborador
- **FP-UC07-002:** Sistema valida permissão
- **FP-UC07-003:** Sistema exibe formulário com campos:
  - Colaborador (autocomplete)
  - Departamento Origem (preenchido automaticamente se acessado de colaborador)
  - Departamento Destino (autocomplete)
  - Tipo Movimentação (enum: Transferencia/Promocao/Realocacao/Temporaria/Retorno)
  - Motivo (NVARCHAR(1000) obrigatório)
  - Data Efetivação Prevista (DATE)
- **FP-UC07-004:** Usuário preenche dados e clica em "Criar Movimentação"
- **FP-UC07-005:** Sistema valida:
  - Colaborador tem lotação principal ativa no Departamento Origem
  - Departamento Origem ≠ Departamento Destino
  - Motivo preenchido (obrigatório)
- **FP-UC07-006:** Sistema cria registro em Departamento_Movimentacao:
  - Id_Usuario, Id_Departamento_Origem, Id_Departamento_Destino
  - Tipo_Movimentacao, Motivo, Dt_Efetivacao_Prevista
  - Status_Aprovacao = Pendente
  - Created_By, Created_At (automáticos)
- **FP-UC07-007:** Sistema envia notificação ao Líder do Departamento Origem (email + push):
  - "Nova movimentação pendente aprovação: João Silva (Backend → Frontend)"
- **FP-UC07-008:** Sistema retorna HTTP 201 Created com ID da movimentação
- **FP-UC07-009:** Frontend exibe mensagem "Movimentação criada com sucesso, aguardando aprovação"

### Fluxos Alternativos
- **FA-UC07-001:** Movimentação temporária - Usuário seleciona Tipo=Temporaria e define Data Fim
- **FA-UC07-002:** Promoção - Usuário seleciona Tipo=Promocao, sistema registra no motivo

### Fluxos de Exceção
- **FE-UC07-001:** Colaborador não tem lotação no Departamento Origem → HTTP 422, mensagem "Colaborador não está alocado no departamento origem"
- **FE-UC07-002:** Departamento Origem = Destino → HTTP 422, mensagem "Departamento origem e destino não podem ser iguais"
- **FE-UC07-003:** Motivo vazio → HTTP 422, mensagem "Motivo é obrigatório"

### Regras de Negócio
- **RN-UC-07-001**: Workflow aprovação multinível sequencial: Pendente → Aprovado_Origem → Aprovado_Destino → Aprovado_RH (**RN-RF024-006**)
- **RN-UC-07-002**: Campo Motivo obrigatório (NVARCHAR(1000)) (**RN-RF024-006**)
- **RN-UC-07-003**: Tipo_Movimentacao enum: Transferencia/Promocao/Realocacao/Temporaria/Retorno (**RN-RF024-006**)
- **RN-UC-07-004**: Status_Aprovacao inicial = Pendente
- **RN-UC-07-005**: Notificação ao Líder Origem ao criar movimentação

### Critérios de Aceite
- **CA-UC07-001:** Sistema DEVE validar que colaborador tem lotação no Departamento Origem
- **CA-UC07-002:** Motivo DEVE ser obrigatório (mínimo 10 caracteres)
- **CA-UC07-003:** Status inicial DEVE ser Pendente
- **CA-UC07-004:** Líder Origem DEVE receber notificação (email + push)
- **CA-UC07-005:** Departamento Origem e Destino DEVEM ser diferentes

---

## UC08 — Aprovar Movimentação

### Objetivo
Permitir aprovação sequencial de movimentação interdepartamental por Líder Origem, Líder Destino e RH, com efetuação automática após aprovação final.

### Pré-condições
- Usuário autenticado
- Permissão específica por etapa:
  - Líder Origem: `CAD.DEPARTAMENTOS.APPROVE_MOVE_ORIGIN`
  - Líder Destino: `CAD.DEPARTAMENTOS.APPROVE_MOVE_DEST`
  - RH: `CAD.DEPARTAMENTOS.APPROVE_MOVE_HR`
- Movimentação existe e status adequado para aprovação

### Pós-condições
- Status da movimentação atualizado
- Notificação enviada ao próximo aprovador (ou colaborador se aprovação final)
- Se aprovação final (RH): lotação do colaborador efetivada

### Fluxo Principal - Aprovação Líder Origem
- **FP-UC08-001:** Líder Origem acessa "Minhas Aprovações Pendentes"
- **FP-UC08-002:** Sistema lista movimentações WHERE Status=Pendente AND Líder do Departamento Origem = Usuário Autenticado
- **FP-UC08-003:** Líder clica em "Aprovar" na movimentação
- **FP-UC08-004:** Sistema valida permissão `CAD.DEPARTAMENTOS.APPROVE_MOVE_ORIGIN`
- **FP-UC08-005:** Sistema valida que usuário é Líder do Departamento Origem
- **FP-UC08-006:** Sistema atualiza Status_Aprovacao = Aprovado_Origem
- **FP-UC08-007:** Sistema registra Dt_Aprovacao_Origem e Id_Aprovador_Origem
- **FP-UC08-008:** Sistema envia notificação ao Líder do Departamento Destino (email + push):
  - "Movimentação aprovada pelo líder de origem, aguardando sua aprovação: João Silva (Backend → Frontend)"
- **FP-UC08-009:** Sistema retorna HTTP 200 OK
- **FP-UC08-010:** Frontend exibe mensagem "Movimentação aprovada, aguardando aprovação do líder destino"

### Fluxo Principal - Aprovação Líder Destino
- **FP-UC08-011:** Líder Destino acessa "Minhas Aprovações Pendentes"
- **FP-UC08-012:** Sistema lista movimentações WHERE Status=Aprovado_Origem AND Líder do Departamento Destino = Usuário Autenticado
- **FP-UC08-013:** Líder clica em "Aprovar" na movimentação
- **FP-UC08-014:** Sistema valida permissão `CAD.DEPARTAMENTOS.APPROVE_MOVE_DEST`
- **FP-UC08-015:** Sistema valida que usuário é Líder do Departamento Destino
- **FP-UC08-016:** Sistema atualiza Status_Aprovacao = Aprovado_Destino
- **FP-UC08-017:** Sistema registra Dt_Aprovacao_Destino e Id_Aprovador_Destino
- **FP-UC08-018:** Sistema envia notificação ao RH (email + push):
  - "Movimentação aprovada pelos líderes, aguardando aprovação final do RH: João Silva (Backend → Frontend)"
- **FP-UC08-019:** Sistema retorna HTTP 200 OK
- **FP-UC08-020:** Frontend exibe mensagem "Movimentação aprovada, aguardando aprovação do RH"

### Fluxo Principal - Aprovação RH (Final)
- **FP-UC08-021:** RH acessa "Aprovações Pendentes RH"
- **FP-UC08-022:** Sistema lista movimentações WHERE Status=Aprovado_Destino
- **FP-UC08-023:** RH clica em "Aprovar" na movimentação
- **FP-UC08-024:** Sistema valida permissão `CAD.DEPARTAMENTOS.APPROVE_MOVE_HR`
- **FP-UC08-025:** Sistema valida que usuário tem role RH
- **FP-UC08-026:** Sistema atualiza Status_Aprovacao = Aprovado_RH
- **FP-UC08-027:** Sistema registra Dt_Aprovacao_RH e Id_Aprovador_RH
- **FP-UC08-028:** Sistema EFETIVA a movimentação (**RN-RF024-006**):
  - Desativa lotação anterior: UPDATE Usuario_Departamento SET Fl_Ativo=0, Dt_Fim=GETDATE() WHERE Id_Usuario=X AND Id_Departamento=Origem
  - Cria lotação nova: INSERT Usuario_Departamento (Id_Usuario, Id_Departamento=Destino, Tipo_Lotacao=Principal, Percentual_Alocacao=100, Dt_Inicio=Dt_Efetivacao)
  - Triggers atualizam Qtd_Colaboradores dos dois departamentos
- **FP-UC08-029:** Sistema sincroniza Azure AD (adicionar usuário ao grupo do novo departamento, remover do anterior) (**RN-RF024-005**)
- **FP-UC08-030:** Sistema define Dt_Efetivacao = timestamp atual
- **FP-UC08-031:** Sistema envia notificação ao colaborador (email + push + inbox):
  - "Sua movimentação foi aprovada e efetivada: agora você faz parte de Frontend (a partir de 31/12/2025)"
- **FP-UC08-032:** Sistema retorna HTTP 200 OK
- **FP-UC08-033:** Frontend exibe mensagem "Movimentação aprovada e efetivada com sucesso"

### Fluxos Alternativos
- **FA-UC08-001:** Rejeitar movimentação - Aprovador clica em "Rejeitar", sistema define Status=Rejeitado, registra motivo e notifica solicitante

### Fluxos de Exceção
- **FE-UC08-001:** Usuário não é líder do departamento correto → HTTP 403, mensagem "Você não tem permissão para aprovar esta movimentação"
- **FE-UC08-002:** Status da movimentação inválido para aprovação → HTTP 422, mensagem "Movimentação não está no status adequado para aprovação"
- **FE-UC08-003:** Movimentação já aprovada ou rejeitada → HTTP 409, mensagem "Movimentação já foi processada"

### Regras de Negócio
- **RN-UC-08-001**: Workflow sequencial: Pendente → Aprovado_Origem → Aprovado_Destino → Aprovado_RH (**RN-RF024-006**)
- **RN-UC-08-002**: Notificações enviadas a cada etapa (email + push) (**RN-RF024-006**)
- **RN-UC-08-003**: Efetuação automática após aprovação RH: atualiza Usuario_Departamento, Qtd_Colaboradores, sincroniza Azure AD (**RN-RF024-006**)
- **RN-UC-08-004**: Validação de permissão específica por etapa (APPROVE_MOVE_ORIGIN, APPROVE_MOVE_DEST, APPROVE_MOVE_HR)

### Critérios de Aceite
- **CA-UC08-001:** Aprovação DEVE seguir sequência obrigatória (Origem → Destino → RH)
- **CA-UC08-002:** Apenas líder do departamento correspondente PODE aprovar cada etapa
- **CA-UC08-003:** Notificação DEVE ser enviada ao próximo aprovador após cada aprovação
- **CA-UC08-004:** Após aprovação RH, lotação DEVE ser efetivada automaticamente
- **CA-UC08-005:** Azure AD DEVE ser sincronizado após efetuação (usuário adicionado ao grupo novo, removido do anterior)
- **CA-UC08-006:** Qtd_Colaboradores DEVE ser atualizado automaticamente nos dois departamentos

---

## UC09 — Sincronizar com Azure AD

### Objetivo
Permitir sincronização sob demanda de departamento com Azure AD, criando grupo de segurança e adicionando colaboradores como membros via Microsoft Graph API.

### Pré-condições
- Usuário autenticado
- Permissão `CAD.DEPARTAMENTOS.SYNC_AZUREAD`
- Role autorizada: Super Admin
- Departamento existe e está ativo
- Credenciais Azure AD configuradas (Client ID, Client Secret, Tenant ID)

### Pós-condições
- Grupo Azure AD criado ou atualizado
- Membros sincronizados
- Azure_AD_Object_Id e Dt_Ultima_Sincronizacao_AD atualizados

### Fluxo Principal
- **FP-UC09-001:** Usuário clica em "Sincronizar com Azure AD" na visualização do departamento
- **FP-UC09-002:** Sistema valida permissão `CAD.DEPARTAMENTOS.SYNC_AZUREAD`
- **FP-UC09-003:** Sistema valida credenciais Azure AD (Client Credentials Flow)
- **FP-UC09-004:** Sistema obtém access token via Microsoft Identity Platform:
  ```
  POST https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token
  grant_type=client_credentials
  client_id={client_id}
  client_secret={client_secret}
  scope=https://graph.microsoft.com/.default
  ```
- **FP-UC09-005:** Sistema verifica se grupo já existe no Azure AD (via Azure_AD_Object_Id):
  - Se NÃO existe: cria grupo via Microsoft Graph API
  - Se existe: atualiza displayName e description
- **FP-UC09-006:** Sistema cria grupo Azure AD (se não existir):
  ```
  POST https://graph.microsoft.com/v1.0/groups
  {
    "displayName": "[Codigo_Departamento] Nome_Departamento",
    "mailNickname": "Codigo_Departamento",
    "mailEnabled": false,
    "securityEnabled": true,
    "description": "Tipo_Departamento - Lider: Nome_Lider",
    "groupTypes": []
  }
  ```
- **FP-UC09-007:** Sistema armazena Azure_AD_Object_Id retornado
- **FP-UC09-008:** Sistema busca colaboradores ativos do departamento (Tipo_Lotacao=Principal, Fl_Ativo=1)
- **FP-UC09-009:** Sistema adiciona colaboradores como membros do grupo Azure AD:
  ```
  POST https://graph.microsoft.com/v1.0/groups/{groupId}/members/$ref
  {
    "@odata.id": "https://graph.microsoft.com/v1.0/users/{userId}"
  }
  ```
- **FP-UC09-010:** Sistema atualiza Dt_Ultima_Sincronizacao_AD = timestamp atual
- **FP-UC09-011:** Sistema retorna HTTP 200 OK com resultado da sincronização:
  - Total de membros sincronizados
  - Erros (se houver)
- **FP-UC09-012:** Frontend exibe mensagem "Sincronização com Azure AD concluída: 15 membros sincronizados"

### Fluxos Alternativos
- **FA-UC09-001:** Sincronização automática via Hangfire - Job diário às 03:00 BRT (Cron "0 3 * * *") sincroniza todos os departamentos ativos (**RN-RF024-005**)

### Fluxos de Exceção
- **FE-UC09-001:** Falha autenticação Azure AD → HTTP 500, mensagem "Falha autenticação Azure AD, verifique credenciais"
- **FE-UC09-002:** Falha criação grupo → HTTP 500, mensagem "Falha ao criar grupo no Azure AD"
- **FE-UC09-003:** Falha adição membros → HTTP 500, mensagem "Falha ao adicionar membros ao grupo Azure AD"
- **FE-UC09-004:** 3+ falhas consecutivas → Alerta crítico enviado para TI e Super Admin (**Alertas**)

### Regras de Negócio
- **RN-UC-09-001**: Sincronização UNIDIRECIONAL IControlIT → Azure AD (**RN-RF024-005**)
- **RN-UC-09-002**: Job Hangfire diário às 03:00 BRT (Cron "0 3 * * *") (**RN-RF024-005**)
- **RN-UC-09-003**: Microsoft Graph SDK .NET, autenticação Client Credentials Flow
- **RN-UC-09-004**: Permissões Azure AD: `Group.ReadWrite.All`, `User.Read.All` (**RN-RF024-005**)
- **RN-UC-09-005**: Armazenar Azure_AD_Object_Id, AD_Distinguished_Name, Dt_Ultima_Sincronizacao_AD (**RN-RF024-005**)

### Critérios de Aceite
- **CA-UC09-001:** Grupo Azure AD DEVE ser criado com displayName formato "[CODIGO] Nome"
- **CA-UC09-002:** Colaboradores com lotação principal ativa DEVEM ser adicionados como membros
- **CA-UC09-003:** Azure_AD_Object_Id DEVE ser armazenado após criação
- **CA-UC09-004:** Dt_Ultima_Sincronizacao_AD DEVE ser atualizado após sucesso
- **CA-UC09-005:** Sincronização automática DEVE executar diariamente às 03:00 BRT
- **CA-UC09-006:** Taxa de sucesso DEVE ser ≥95% (**KPI**)
- **CA-UC09-007:** 3+ falhas consecutivas DEVEM gerar alerta crítico

---

## UC10 — Visualizar Dashboard Headcount

### Objetivo
Permitir visualização de dashboard KPIs de headcount por departamento atualizado em tempo real via SignalR, com métricas de ocupação, variação mensal e projeção.

### Pré-condições
- Usuário autenticado
- Permissão implícita Gestor / RH
- Departamento existe e está ativo

### Pós-condições
- Dashboard exibido com métricas atualizadas
- Conexão SignalR estabelecida para atualizações em tempo real

### Fluxo Principal
- **FP-UC10-001:** Usuário acessa "Dashboard Headcount" no departamento
- **FP-UC10-002:** Sistema valida permissão implícita
- **FP-UC10-003:** Sistema estabelece conexão SignalR Hub `DepartamentoHub`
- **FP-UC10-004:** Sistema calcula métricas (**RN-RF024-011**):
  - **Headcount Atual**: COUNT Usuario_Departamento WHERE Tipo_Lotacao='Principal' AND Fl_Ativo=1
  - **Headcount Orçado**: Campo `Headcount_Orcado` em `Departamento_Meta`
  - **Taxa Ocupação**: (Atual / Orçado) * 100
  - **Variação Mês Anterior**: Atual - Headcount do mês anterior (snapshot)
  - **Projeção Próximo Trimestre**: ML baseado em histórico (linear regression)
- **FP-UC10-005:** Sistema define cor do gauge (**RN-RF024-011**):
  - Verde: Taxa Ocupação ≥90%
  - Amarelo: Taxa Ocupação 75-89%
  - Vermelho: Taxa Ocupação <75%
- **FP-UC10-006:** Sistema retorna JSON com métricas para frontend
- **FP-UC10-007:** Frontend renderiza dashboard Chart.js:
  - Gauge chart: Taxa Ocupação (com cores)
  - Line chart: Evolução headcount últimos 12 meses
  - Cards: Headcount Atual, Orçado, Variação Mês, Projeção Trimestre
- **FP-UC10-008:** Sistema escuta eventos SignalR `OnHeadcountAtualizado`
- **FP-UC10-009:** Quando evento disparado (após alocação/movimentação), frontend atualiza métricas automaticamente

### Fluxos Alternativos
- **FA-UC10-001:** Visualizar subárvore - Usuário clica em departamento filho, dashboard mostra métricas agregadas (soma de todos os filhos recursivamente)
- **FA-UC10-002:** Exportar relatório - Usuário clica em "Exportar", sistema gera Excel com histórico 12 meses

### Fluxos de Exceção
- **FE-UC10-001:** Erro conexão SignalR → Frontend exibe mensagem "Erro conexão tempo real, dados podem estar desatualizados"
- **FE-UC10-002:** Departamento sem meta configurada → Headcount Orçado exibido como "Não configurado"

### Regras de Negócio
- **RN-UC-10-001**: Métricas calculadas em tempo real (**RN-RF024-011**)
- **RN-UC-10-002**: SignalR Hub `DepartamentoHub` broadcast evento `OnHeadcountAtualizado` após movimentações (**RN-RF024-011**)
- **RN-UC-10-003**: Frontend Chart.js line chart 12 meses, gauge chart taxa ocupação (**RN-RF024-011**)
- **RN-UC-10-004**: Cores: Verde ≥90%, Amarelo 75-89%, Vermelho <75% (**RN-RF024-011**)
- **RN-UC-10-005**: Latência SignalR <500ms para broadcast headcount (**KPI**)

### Critérios de Aceite
- **CA-UC10-001:** Dashboard DEVE exibir 5 métricas: Atual, Orçado, Taxa Ocupação, Variação Mês, Projeção Trimestre
- **CA-UC10-002:** Gauge chart DEVE usar cores verde/amarelo/vermelho conforme taxa ocupação
- **CA-UC10-003:** Line chart DEVE exibir evolução últimos 12 meses
- **CA-UC10-004:** SignalR DEVE atualizar dashboard em tempo real após alocações/movimentações
- **CA-UC10-005:** Latência SignalR DEVE ser <500ms (**KPI**)
- **CA-UC10-006:** Dashboard agregado (subárvore) DEVE somar headcount de todos os filhos recursivamente

---

## 4. MATRIZ DE RASTREABILIDADE

| UC | Regras de Negócio do RF | Funcionalidades do RF |
|----|------------------------|---------------------|
| UC00 | RN-RF024-001, RN-RF024-002 | RF-CRUD-02 (Listar) |
| UC01 | RN-RF024-001, RN-RF024-002, RN-RF024-003, RN-RF024-004, RN-RF024-010, RN-RF024-015 | RF-CRUD-01 (Criar), RF-VAL-01, RF-VAL-02, RF-VAL-03, RF-SEC-01, RF-SEC-03, RF-FUNC-01 |
| UC02 | - | RF-CRUD-03 (Visualizar), RF-SEC-01, RF-FUNC-01 |
| UC03 | RN-RF024-002, RN-RF024-003, RN-RF024-004, RN-RF024-010, RN-RF024-015 | RF-CRUD-04 (Atualizar), RF-VAL-02, RF-SEC-01, RF-SEC-03, RF-FUNC-01 |
| UC04 | RN-RF024-002, RN-RF024-008, RN-RF024-015 | RF-CRUD-05 (Excluir), RF-SEC-01, RF-SEC-03 |
| UC05 | RN-RF024-009 | RF-FUNC-02 (Organograma visual D3.js) |
| UC06 | RN-RF024-007, RN-RF024-008, RN-RF024-010 | RF-FUNC-03 (Dotted-line), RF-SEC-01, RF-SEC-03 |
| UC07 | RN-RF024-006 | RF-FUNC-05 (Workflow movimentações) |
| UC08 | RN-RF024-005, RN-RF024-006, RN-RF024-008 | RF-FUNC-05 (Workflow movimentações), RF-FUNC-04 (Sincronização Azure AD) |
| UC09 | RN-RF024-005 | RF-FUNC-04 (Sincronização Azure AD) |
| UC10 | RN-RF024-011 | RF-FUNC-06 (Dashboard headcount tempo real) |

---

## 5. CATÁLOGO DE PERMISSÕES

| Permissão | UCs Aplicáveis |
|-----------|---------------|
| CAD.DEPARTAMENTOS.CREATE | UC01 |
| CAD.DEPARTAMENTOS.UPDATE | UC03 |
| CAD.DEPARTAMENTOS.DELETE | UC04 |
| CAD.DEPARTAMENTOS.VIEW_ORGCHART | UC05 |
| CAD.DEPARTAMENTOS.APPROVE_MOVE_ORIGIN | UC08 |
| CAD.DEPARTAMENTOS.APPROVE_MOVE_DEST | UC08 |
| CAD.DEPARTAMENTOS.APPROVE_MOVE_HR | UC08 |
| CAD.DEPARTAMENTOS.SYNC_AZUREAD | UC09 |

---

## CHANGELOG

| Versão | Data | Autor | Descrição |
|------|------|-------|-----------|
| 2.0 | 2025-12-31 | Agência ALC - alc.dev.br | Versão canônica orientada a contrato - 11 UCs cobrindo 100% do RF024 |
