# UC-RF013 — Casos de Uso: Gestão de Perfis de Acesso (RBAC)

**RF:** RF013 — Gestão de Perfis de Acesso (RBAC)
**Versão:** 2.0
**Data:** 2025-12-31
**Autor:** Agência ALC - alc.dev.br
**Epic:** EPIC002-CAD - Cadastros do Sistema
**Fase:** Fase 1 - Sistema Base

---

## 1. OBJETIVO DO DOCUMENTO

Este documento descreve **todos os Casos de Uso (UC)** derivados do **RF013 — Gestão de Perfis de Acesso (RBAC)**, cobrindo integralmente o comportamento funcional esperado.

Os UCs aqui definidos servem como **contrato comportamental**, sendo a **fonte primária** para geração de:
- Casos de Teste (TC-RF013.yaml)
- Massas de Teste (MT-RF013.yaml)
- Evidências de auditoria e validação funcional
- Execução por agentes de IA (tester, QA, E2E)

---

## 2. SUMÁRIO DE CASOS DE USO

| ID | Nome | Ator Principal | Regras Cobertas |
|----|------|----------------|-----------------|
| UC00 | Listar Perfis de Acesso | Administrador | RN-RF013-01, RN-RF013-10 |
| UC01 | Criar Perfil de Acesso | Super Admin, Administrador | RN-RF013-01, RN-RF013-02, RN-RF013-04, RN-RF013-09 |
| UC02 | Visualizar Perfil de Acesso | Administrador | RN-RF013-03, RN-RF013-10 |
| UC03 | Editar Perfil de Acesso | Super Admin, Administrador | RN-RF013-01, RN-RF013-02, RN-RF013-05, RN-RF013-07, RN-RF013-09 |
| UC04 | Excluir Perfil de Acesso | Super Admin, Administrador | RN-RF013-08, RN-RF013-09 |
| UC05 | Gerenciar Permissões do Perfil | Super Admin, Administrador | RN-RF013-04, RN-RF013-05, RN-RF013-06, RN-RF013-07 |
| UC06 | Duplicar Perfil de Acesso | Administrador | RN-RF013-01, RN-RF013-09 |

**Cobertura**: 10/10 Regras de Negócio (100%)

---

## 3. PADRÕES GERAIS APLICÁVEIS A TODOS OS UCs

- Todos os acessos respeitam **isolamento por tenant** (EmpresaId)
- Todas as ações exigem **permissão explícita** (RBAC)
- Erros não devem vazar informações sensíveis
- Auditoria deve registrar quem, quando e o que mudou
- Mensagens devem ser claras, previsíveis e rastreáveis
- Nomes de perfis únicos por tenant (RN-RF013-01)
- Super Admin bypassa todas as validações de permissão (RN-RF013-03)

---

## UC00 — Listar Perfis de Acesso

### Objetivo
Permitir que o usuário visualize a lista de perfis de acesso disponíveis no seu tenant.

### Pré-condições
- Usuário autenticado
- Permissão `perfis:perfil:view_any`
- Tenant_Id válido no contexto

### Pós-condições
- Lista exibida conforme filtros e paginação
- Registros isolados por tenant

### Fluxo Principal
1. Usuário acessa a funcionalidade "Perfis de Acesso"
2. Sistema valida permissão `perfis:perfil:view_any`
3. Sistema carrega perfis do tenant (WHERE EmpresaId = @EmpresaId OR EmpresaId IS NULL)
4. Sistema aplica paginação padrão (20 registros por página)
5. Sistema ordena por Nome ASC
6. Sistema exibe a lista com colunas: Nome, Descrição, Tipo (Sistema/Personalizado), Status (Ativo/Inativo), Usuários Vinculados

### Fluxos Alternativos
- **FA-00-01: Buscar por nome** - Filtro LIKE em Nome
- **FA-00-02: Filtrar por tipo** - Sistema ou Personalizado
- **FA-00-03: Filtrar por status** - Ativo ou Inativo
- **FA-00-04: Ordenar por coluna** - Alternar ASC/DESC

### Fluxos de Exceção
- **FE-00-01: Usuário sem permissão** - HTTP 403
- **FE-00-02: Nenhum perfil encontrado** - Estado vazio
- **FE-00-03: Erro de conexão** - Mensagem genérica + log técnico

### Regras de Negócio
- **RN-RF013-01**: Perfis únicos por tenant (validação visual)
- **RN-RF013-10**: Exibir apenas perfis com Fl_Ativo = 1 (padrão)
- **RN-UC00-001**: Perfis de sistema (IsSystemRole = true) exibidos separadamente
- **RN-UC00-002**: Paginação padrão 20 registros
- **RN-UC00-003**: Ordenação padrão por Nome ASC

### Critérios de Aceite
- **CA-UC00-001**: Lista DEVE exibir apenas perfis do tenant do usuário ou perfis de sistema (EmpresaId IS NULL)
- **CA-UC00-002**: Perfis inativos (Fl_Ativo = 0) NÃO devem aparecer na listagem padrão
- **CA-UC00-003**: Coluna "Usuários Vinculados" DEVE mostrar contagem de usuários ativos com o perfil
- **CA-UC00-004**: Perfis de sistema DEVEM ter indicador visual (badge "Sistema")
- **CA-UC00-005**: Filtros DEVEM ser acumuláveis e refletir na URL

---

## UC01 — Criar Perfil de Acesso

### Objetivo
Permitir a criação de um novo perfil de acesso com permissões granulares.

### Pré-condições
- Usuário autenticado
- Permissão `perfis:perfil:create`
- Tenant_Id válido no contexto

### Pós-condições
- Perfil criado e persistido
- Permissões associadas (se fornecidas)
- Auditoria registrada
- Cache invalidado (se aplicável)

### Fluxo Principal
1. Usuário clica "Novo Perfil"
2. Sistema valida permissão `perfis:perfil:create`
3. Sistema exibe formulário com campos: Nome (obrigatório), Descrição, IsSystemRole (checkbox desabilitado), Permissões (lista de checkboxes)
4. Usuário preenche dados e seleciona permissões
5. Usuário clica "Salvar"
6. Sistema valida dados (RN-RF013-01, RN-RF013-04)
7. Sistema cria perfil (INSERT INTO Role)
8. Sistema associa permissões (INSERT INTO RolePermission)
9. Sistema registra auditoria (Created, CreatedBy)
10. Sistema exibe mensagem de sucesso
11. Sistema redireciona para listagem

### Fluxos Alternativos
- **FA-01-01: Salvar e criar outro** - Mantém formulário aberto após salvar
- **FA-01-02: Cancelar criação** - Descarta dados e retorna à listagem

### Fluxos de Exceção
- **FE-01-01: Nome duplicado no tenant** - HTTP 400 com mensagem "Já existe um perfil com este nome nesta empresa"
- **FE-01-02: Permissão com formato inválido** - HTTP 400 com mensagem "Formato de permissão inválido: deve ser modulo:recurso:acao"
- **FE-01-03: Nome vazio ou maior que 100 caracteres** - HTTP 400
- **FE-01-04: Descrição maior que 500 caracteres** - HTTP 400

### Regras de Negócio
- **RN-RF013-01**: Nome único por tenant (validação case-insensitive)
- **RN-RF013-02**: Campo IsSystemRole = false (sempre) para perfis criados por usuário
- **RN-RF013-04**: Permissões seguem formato `modulo:recurso:acao`
- **RN-RF013-09**: Campos Created, CreatedBy preenchidos automaticamente
- **RN-UC01-001**: EmpresaId preenchido automaticamente com tenant do usuário
- **RN-UC01-002**: Fl_Ativo = 1 (ativo) por padrão
- **RN-UC01-003**: Fl_Super_Admin = 0 (sempre) para perfis criados por usuário

### Critérios de Aceite
- **CA-UC01-001**: Nome DEVE ser único dentro do tenant (validação no backend)
- **CA-UC01-002**: EmpresaId DEVE ser preenchido automaticamente com tenant do usuário autenticado
- **CA-UC01-003**: Created e CreatedBy DEVEM ser preenchidos automaticamente
- **CA-UC01-004**: Sistema DEVE retornar erro claro se validação falhar
- **CA-UC01-005**: Permissões selecionadas DEVEM ser persistidas na tabela RolePermission
- **CA-UC01-006**: Auditoria DEVE ser registrada APÓS sucesso da criação

---

## UC02 — Visualizar Perfil de Acesso

### Objetivo
Permitir visualização detalhada de um perfil de acesso específico.

### Pré-condições
- Usuário autenticado
- Permissão `perfis:perfil:view`
- Tenant_Id válido no contexto
- Perfil existe e pertence ao tenant ou é perfil de sistema

### Pós-condições
- Dados do perfil exibidos corretamente
- Permissões associadas listadas
- Usuários vinculados exibidos

### Fluxo Principal
1. Usuário seleciona perfil na listagem (UC00)
2. Usuário clica "Visualizar"
3. Sistema valida permissão `perfis:perfil:view`
4. Sistema valida isolamento de tenant (WHERE (EmpresaId = @EmpresaId OR EmpresaId IS NULL) AND Id = @Id)
5. Sistema carrega dados do perfil
6. Sistema carrega permissões associadas (JOIN RolePermission, Permission)
7. Sistema carrega usuários vinculados (COUNT UsuarioRoles WHERE RoleId = @Id)
8. Sistema exibe 3 painéis:
   - **Painel 1: Informações Gerais** (Nome, Descrição, Tipo, Status, Criado em, Atualizado em)
   - **Painel 2: Permissões** (Lista de permissões com módulo, recurso, ação)
   - **Painel 3: Usuários Vinculados** (Contagem + link para lista)

### Fluxos Alternativos
- **FA-02-01: Editar perfil** - Redireciona para UC03 se usuário tiver permissão
- **FA-02-02: Ver histórico de auditoria** - Redireciona para RF-004 (Sistema de Auditoria)

### Fluxos de Exceção
- **FE-02-01: Perfil não encontrado** - HTTP 404
- **FE-02-02: Perfil de outro tenant** - HTTP 404 (não revelar existência)
- **FE-02-03: Erro ao carregar permissões** - Mensagem genérica + log técnico

### Regras de Negócio
- **RN-RF013-03**: Super Admin pode visualizar qualquer perfil
- **RN-RF013-10**: Perfis inativos também são visualizáveis (mas com indicador)
- **RN-UC02-001**: Isolamento por tenant obrigatório (exceto Super Admin)
- **RN-UC02-002**: Perfis de sistema têm badge "Sistema" destacado

### Critérios de Aceite
- **CA-UC02-001**: Usuário SÓ pode visualizar perfis do próprio tenant ou perfis de sistema
- **CA-UC02-002**: Informações de auditoria DEVEM ser exibidas (Created, CreatedBy, LastModified, LastModifiedBy)
- **CA-UC02-003**: Tentativa de acessar perfil de outro tenant DEVE retornar 404
- **CA-UC02-004**: Permissões DEVEM ser agrupadas por módulo
- **CA-UC02-005**: Contagem de usuários DEVE incluir apenas usuários ativos

---

## UC03 — Editar Perfil de Acesso

### Objetivo
Permitir alteração controlada de um perfil de acesso existente.

### Pré-condições
- Usuário autenticado
- Permissão `perfis:perfil:update`
- Tenant_Id válido no contexto
- Perfil existe e pertence ao tenant ou é perfil de sistema

### Pós-condições
- Perfil atualizado
- Permissões atualizadas (adicionadas/removidas)
- Auditoria registrada
- Cache de permissões invalidado

### Fluxo Principal
1. Usuário seleciona perfil na listagem (UC00)
2. Usuário clica "Editar"
3. Sistema valida permissão `perfis:perfil:update`
4. Sistema valida se perfil é editável (RN-RF013-02)
5. Sistema carrega dados do perfil
6. Sistema exibe formulário pré-preenchido
7. Usuário altera dados (Nome, Descrição) e/ou permissões
8. Usuário clica "Salvar"
9. Sistema valida dados (RN-RF013-01, RN-RF013-04, RN-RF013-05)
10. Sistema atualiza perfil (UPDATE Role)
11. Sistema atualiza permissões (DELETE + INSERT RolePermission)
12. Sistema registra auditoria (LastModified, LastModifiedBy)
13. Sistema invalida cache de permissões (RN-RF013-07)
14. Sistema exibe mensagem de sucesso

### Fluxos Alternativos
- **FA-03-01: Cancelar edição** - Descarta alterações
- **FA-03-02: Adicionar justificativa** - Obrigatório ao atribuir permissão crítica (RN-RF013-05)

### Fluxos de Exceção
- **FE-03-01: Nome duplicado** - HTTP 400
- **FE-03-02: Tentativa de editar nome/descrição de perfil de sistema** - HTTP 400 "Perfis de sistema não podem ter nome ou descrição alterados"
- **FE-03-03: Permissão crítica sem justificativa** - HTTP 400 "Justificativa obrigatória para permissões críticas"
- **FE-03-04: Perfil de outro tenant** - HTTP 404

### Regras de Negócio
- **RN-RF013-01**: Nome único por tenant (validação case-insensitive)
- **RN-RF013-02**: Perfis de sistema (IsSystemRole = true) não podem ter Nome/Descrição editados
- **RN-RF013-05**: Permissões críticas exigem justificativa
- **RN-RF013-07**: Cache invalidado após alteração
- **RN-RF013-09**: LastModified, LastModifiedBy atualizados automaticamente
- **RN-UC03-001**: Permissões podem ser alteradas mesmo em perfis de sistema
- **RN-UC03-002**: Notificação enviada ao gestor se permissão crítica for atribuída

### Critérios de Aceite
- **CA-UC03-001**: LastModified e LastModifiedBy DEVEM ser atualizados automaticamente
- **CA-UC03-002**: Apenas Nome e Descrição podem ser alterados em perfis personalizados
- **CA-UC03-003**: Perfis de sistema DEVEM permitir apenas alteração de permissões
- **CA-UC03-004**: Sistema DEVE invalidar cache de permissões após alteração
- **CA-UC03-005**: Tentativa de editar perfil de outro tenant DEVE retornar 404
- **CA-UC03-006**: Auditoria DEVE registrar estado anterior e novo estado

---

## UC04 — Excluir Perfil de Acesso

### Objetivo
Permitir exclusão lógica (soft delete) de perfis de acesso.

### Pré-condições
- Usuário autenticado
- Permissão `perfis:perfil:delete`
- Tenant_Id válido no contexto
- Perfil existe e pertence ao tenant ou é perfil de sistema
- Perfil NÃO possui usuários vinculados (RN-RF013-08)

### Pós-condições
- Perfil marcado como inativo (Fl_Ativo = 0)
- Auditoria registrada
- Cache invalidado

### Fluxo Principal
1. Usuário seleciona perfil na listagem (UC00)
2. Usuário clica "Excluir"
3. Sistema exibe confirmação: "Tem certeza que deseja excluir o perfil '{Nome}'?"
4. Usuário confirma
5. Sistema valida permissão `perfis:perfil:delete`
6. Sistema verifica se perfil possui usuários vinculados (RN-RF013-08)
7. Sistema valida isolamento de tenant
8. Sistema atualiza Fl_Ativo = 0 (UPDATE Role)
9. Sistema registra auditoria (LastModified, LastModifiedBy)
10. Sistema invalida cache
11. Sistema exibe mensagem de sucesso
12. Sistema remove perfil da listagem

### Fluxos Alternativos
- **FA-04-01: Cancelar exclusão** - Fecha modal sem alterar nada

### Fluxos de Exceção
- **FE-04-01: Perfil com usuários vinculados** - HTTP 400 "Não é possível excluir este perfil pois existem {N} usuário(s) vinculado(s). Remova os usuários deste perfil antes de excluí-lo."
- **FE-04-02: Perfil já excluído** - HTTP 404
- **FE-04-03: Perfil de outro tenant** - HTTP 404

### Regras de Negócio
- **RN-RF013-08**: Perfil com usuários vinculados não pode ser excluído
- **RN-RF013-09**: Auditoria registrada automaticamente
- **RN-RF013-10**: Exclusão é sempre lógica (Fl_Ativo = 0)
- **RN-UC04-001**: Perfis de sistema PODEM ser excluídos se não tiverem usuários
- **RN-UC04-002**: Contagem de usuários vinculados DEVE exibida na mensagem de erro

### Critérios de Aceite
- **CA-UC04-001**: Exclusão DEVE ser sempre lógica (soft delete) via Fl_Ativo = 0
- **CA-UC04-002**: Sistema DEVE verificar usuários vinculados ANTES de permitir exclusão
- **CA-UC04-003**: Sistema DEVE exigir confirmação explícita do usuário
- **CA-UC04-004**: LastModified e LastModifiedBy DEVEM ser atualizados
- **CA-UC04-005**: Tentativa de excluir perfil com usuários DEVE retornar erro claro com contagem
- **CA-UC04-006**: Perfil excluído NÃO deve aparecer em listagens padrão
- **CA-UC04-007**: Super Admin pode excluir qualquer perfil (respeitando RN-RF013-08)

---

## UC05 — Gerenciar Permissões do Perfil

### Objetivo
Permitir atribuição e remoção de permissões granulares em um perfil de acesso.

### Pré-condições
- Usuário autenticado
- Permissão `perfis:permissao:assign` ou `perfis:permissao:revoke`
- Tenant_Id válido no contexto
- Perfil existe e pertence ao tenant ou é perfil de sistema

### Pós-condições
- Permissões atribuídas/removidas
- Auditoria registrada com detalhes da operação
- Cache de permissões invalidado
- Notificação enviada (se permissão crítica)

### Fluxo Principal
1. Usuário acessa edição de perfil (UC03)
2. Usuário visualiza painel "Permissões Disponíveis" (catálogo completo)
3. Sistema exibe permissões agrupadas por módulo (CONTRATOS, FATURAS, USUARIOS, etc.)
4. Usuário seleciona/desmarca permissões (checkboxes)
5. Sistema valida formato de permissões (RN-RF013-04)
6. Sistema identifica permissões críticas (RN-RF013-05)
7. **SE** permissão crítica sendo atribuída:
   - Sistema exibe campo "Justificativa" (obrigatório)
   - Usuário preenche justificativa (mínimo 20 caracteres)
8. Usuário clica "Salvar Permissões"
9. Sistema valida permissões selecionadas
10. Sistema atualiza RolePermission (DELETE antigas + INSERT novas)
11. Sistema registra auditoria detalhada (permissão, ação, justificativa, IP)
12. Sistema invalida cache (RN-RF013-07)
13. **SE** permissão crítica foi atribuída: Sistema envia notificação para gestor
14. Sistema exibe mensagem de sucesso

### Fluxos Alternativos
- **FA-05-01: Selecionar todas do módulo** - Checkbox master por módulo
- **FA-05-02: Buscar permissão** - Filtro por nome/código de permissão
- **FA-05-03: Ver descrição da permissão** - Tooltip com descrição detalhada

### Fluxos de Exceção
- **FE-05-01: Permissão crítica sem justificativa** - HTTP 400 "Justificativa obrigatória para permissões críticas"
- **FE-05-02: Formato de permissão inválido** - HTTP 400 "Formato deve ser modulo:recurso:acao"
- **FE-05-03: Erro ao invalidar cache** - Log técnico + continua operação

### Regras de Negócio
- **RN-RF013-04**: Permissões seguem formato `modulo:recurso:acao`
- **RN-RF013-05**: Permissões críticas (Fl_Critica = true) exigem justificativa
- **RN-RF013-06**: Middleware valida permissões em runtime
- **RN-RF013-07**: Cache invalidado após alteração
- **RN-UC05-001**: Permissões críticas: usuarios:usuario:*, perfis:perfil:*, contratos:contrato:approve, faturas:fatura:import
- **RN-UC05-002**: Auditoria DEVE incluir: usuário, timestamp, permissão, ação (add/remove), justificativa (se aplicável), IP
- **RN-UC05-003**: Notificação enviada para gestor quando permissão crítica é atribuída

### Critérios de Aceite
- **CA-UC05-001**: Catálogo de permissões DEVE estar agrupado por módulo
- **CA-UC05-002**: Permissões críticas DEVEM ter indicador visual (ícone ou cor)
- **CA-UC05-003**: Justificativa DEVE ter mínimo 20 caracteres
- **CA-UC05-004**: Sistema DEVE validar formato antes de persistir
- **CA-UC05-005**: Cache DEVE ser invalidado imediatamente após alteração
- **CA-UC05-006**: Auditoria DEVE registrar estado anterior e novo estado
- **CA-UC05-007**: Notificação DEVE ser enviada assincronamente (não bloquear operação)

---

## UC06 — Duplicar Perfil de Acesso

### Objetivo
Permitir criação de novo perfil baseado em perfil existente (cópia completa).

### Pré-condições
- Usuário autenticado
- Permissão `perfis:perfil:duplicate`
- Tenant_Id válido no contexto
- Perfil origem existe e pertence ao tenant ou é perfil de sistema

### Pós-condições
- Novo perfil criado com cópia das permissões do perfil origem
- Auditoria registrada
- Cache não afetado (novo perfil ainda sem usuários)

### Fluxo Principal
1. Usuário seleciona perfil na listagem (UC00)
2. Usuário clica "Duplicar"
3. Sistema valida permissão `perfis:perfil:duplicate`
4. Sistema exibe modal com campo "Novo Nome" pré-preenchido: "{Nome original} - Cópia"
5. Usuário ajusta nome (se desejar) e clica "Duplicar"
6. Sistema valida nome único (RN-RF013-01)
7. Sistema cria novo perfil (INSERT INTO Role):
   - Nome = novo nome
   - Descrição = descrição original + " (cópia)"
   - EmpresaId = tenant do usuário
   - IsSystemRole = false
   - Fl_Ativo = 1
8. Sistema copia permissões (INSERT INTO RolePermission SELECT ... WHERE RoleId = @OrigemId)
9. Sistema registra auditoria
10. Sistema exibe mensagem de sucesso
11. Sistema redireciona para edição do novo perfil (UC03)

### Fluxos Alternativos
- **FA-06-01: Cancelar duplicação** - Fecha modal sem criar nada

### Fluxos de Exceção
- **FE-06-01: Nome duplicado** - HTTP 400 "Já existe um perfil com este nome"
- **FE-06-02: Perfil origem não encontrado** - HTTP 404
- **FE-06-03: Erro ao copiar permissões** - Rollback + mensagem genérica + log técnico

### Regras de Negócio
- **RN-RF013-01**: Nome único por tenant (validação obrigatória)
- **RN-RF013-09**: Created, CreatedBy preenchidos automaticamente
- **RN-UC06-001**: Perfil duplicado é sempre personalizado (IsSystemRole = false)
- **RN-UC06-002**: EmpresaId sempre do tenant do usuário (nunca NULL)
- **RN-UC06-003**: Duplicação é transacional (perfil + permissões ou nada)

### Critérios de Aceite
- **CA-UC06-001**: Novo perfil DEVE ter mesmo conjunto de permissões que o original
- **CA-UC06-002**: Novo perfil DEVE ter IsSystemRole = false (sempre)
- **CA-UC06-003**: Novo perfil DEVE ter EmpresaId do tenant do usuário
- **CA-UC06-004**: Nome DEVE ser validado como único antes de criar
- **CA-UC06-005**: Operação DEVE ser transacional (rollback em caso de erro)
- **CA-UC06-006**: Sistema DEVE redirecionar para edição após criar

---

## 4. MATRIZ DE RASTREABILIDADE (RF013 → UCs)

| Regra de Negócio | UCs Cobrindo | Status |
|------------------|--------------|--------|
| RN-RF013-01 — Nome único por tenant | UC00, UC01, UC03, UC06 | ✅ |
| RN-RF013-02 — Perfis de sistema não-editáveis | UC01, UC03 | ✅ |
| RN-RF013-03 — Super Admin acesso total | UC02 | ✅ |
| RN-RF013-04 — Formato de permissão padronizado | UC01, UC03, UC05 | ✅ |
| RN-RF013-05 — Permissões críticas exigem justificativa | UC03, UC05 | ✅ |
| RN-RF013-06 — Middleware valida permissões | UC05 | ✅ |
| RN-RF013-07 — Cache de permissões | UC03, UC05 | ✅ |
| RN-RF013-08 — Não deletar perfil com usuários | UC04 | ✅ |
| RN-RF013-09 — Auditoria automática | UC01, UC03, UC04, UC06 | ✅ |
| RN-RF013-10 — Uso de Fl_Ativo | UC00, UC02, UC04 | ✅ |

**Cobertura Total: 10/10 Regras de Negócio (100%)**

---

## 5. MATRIZ DE PERMISSÕES RBAC

| Permissão | UCs Permitidos | Perfis Padrão |
|-----------|----------------|---------------|
| `perfis:perfil:view_any` | UC00 | Super Admin, Administrador, Gestor |
| `perfis:perfil:view` | UC02 | Super Admin, Administrador, Gestor |
| `perfis:perfil:create` | UC01 | Super Admin, Administrador |
| `perfis:perfil:update` | UC03 | Super Admin, Administrador |
| `perfis:perfil:delete` | UC04 | Super Admin, Administrador |
| `perfis:perfil:duplicate` | UC06 | Super Admin, Administrador |
| `perfis:permissao:assign` | UC05 | Super Admin, Administrador |
| `perfis:permissao:revoke` | UC05 | Super Admin, Administrador |

---

## CHANGELOG

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 2.0 | 2025-12-31 | Agência ALC - alc.dev.br | Versão canônica com 7 UCs cobrindo 100% das 10 regras de negócio (v2.0 Governance) |
| 1.0 | 2025-12-17 | Agência ALC - alc.dev.br | Versão inicial detalhada (DEPRECIADA, >25000 tokens) |
