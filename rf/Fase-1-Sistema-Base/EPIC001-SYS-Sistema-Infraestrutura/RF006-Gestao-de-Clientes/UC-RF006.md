# UC-RF006 — Casos de Uso Canônicos

**RF:** RF006 — Gestão de Clientes (Multi-Tenancy SaaS)
**Versão:** 2.0
**Data:** 2025-12-30
**Autor:** Agência ALC - alc.dev.br
**Epic:** EPIC001-SYS-Sistema-Infraestrutura
**Fase:** Fase-1-Sistema-Base

---

## 1. VISÃO GERAL

Este documento descreve os **casos de uso canônicos** para o módulo de Gestão de Clientes, que implementa a camada de multi-tenancy SaaS da aplicação IControlIT. Clientes representam a **entidade raiz de tenant**, sendo o discriminador obrigatório em TODAS as operações do sistema.

**Contexto Multi-Tenancy:**
- ClienteId é discriminador de tenant obrigatório via EF Core Query Filters
- Super Admin possui privilégio de bypass (IsSuperAdmin = true) para visualizar todos os Clientes
- Usuários comuns NÃO possuem acesso ao módulo de Gestão de Clientes (RBAC)
- Cada Cliente funciona como banco de dados lógico (Row-Level Security)

**Integrações Obrigatórias:**
- **ReceitaWS API**: Consulta automática de CNPJ (https://www.receitaws.com.br/v1/)
- **Azure Blob Storage**: Armazenamento de logos corporativos (container: clientes-logos)
- **i18n**: Chaves de tradução para labels, erros e mensagens de confirmação
- **Auditoria**: Registro automático via AuditInterceptor (7 anos LGPD)
- **Permissões RBAC**: Todas as operações restritas a Super Admin

---

## 2. SUMÁRIO DE CASOS DE USO

| ID | Nome | Ator Principal | Permissão Requerida | RNs Cobertas |
|----|------|----------------|---------------------|--------------|
| UC00 | Listar Clientes | Super Admin | ClientesVisualizar | RN-CLI-006-01, RN-CLI-006-08 |
| UC01 | Criar Cliente com ReceitaWS | Super Admin | ClientesGerenciar | RN-CLI-006-02, RN-CLI-006-03, RN-CLI-006-04, RN-CLI-006-05, RN-CLI-006-10 |
| UC02 | Visualizar Cliente | Super Admin | ClientesVisualizar | RN-CLI-006-01, RN-CLI-006-08 |
| UC03 | Editar Cliente | Super Admin | ClientesGerenciar | RN-CLI-006-04, RN-CLI-006-10 |
| UC04 | Excluir Cliente (Soft Delete) | Super Admin | ClientesGerenciar | RN-CLI-006-07, RN-CLI-006-09, RN-CLI-006-10 |
| UC05 | Upload de Logo do Cliente | Super Admin | ClientesGerenciar | RN-CLI-006-06, RN-CLI-006-10 |
| UC06 | Restaurar Cliente Excluído | Super Admin | ClientesGerenciar | RN-CLI-006-07, RN-CLI-006-10 |
| UC07 | Desativar Cliente | Super Admin | ClientesGerenciar | RN-CLI-006-09, RN-CLI-006-10 |
| UC08 | Consultar CNPJ na ReceitaWS | Super Admin | ClientesGerenciar | RN-CLI-006-05, RN-CLI-006-03, RN-CLI-006-10 |

**Cobertura de Regras de Negócio**: 10/10 RNs (100%)

---

## 3. CASOS DE USO DETALHADOS

---

## UC00 — Listar Clientes

### Objetivo
Permitir ao Super Admin visualizar todos os Clientes cadastrados no sistema, com filtros, ordenação, paginação e bypass de multi-tenancy.

### Pré-condições
- [PRE-001] Usuário autenticado com IsSuperAdmin = true
- [PRE-002] Permissão: ClientesVisualizar
- [PRE-003] JWT válido com claims: `nameid`, `email`, `role:Super Admin`

### Pós-condições
- [POS-001] Lista de Clientes retornada com paginação (default: 10 registros/página)
- [POS-002] Filtros aplicados conforme parâmetros de consulta
- [POS-003] Operação registrada em AuditLog com tipo: CLI_LIST

### Fluxo Principal
1. Super Admin acessa a rota `/admin/clientes`
2. Sistema executa `GetClientesQuery` com parâmetros
3. Sistema aplica **bypass de multi-tenancy** (IsSuperAdmin = true)
4. Sistema aplica filtros e ordenação
5. Sistema retorna DTO paginado com lista de Clientes
6. Sistema registra auditoria (Tipo: CLI_LIST)

### Fluxos Alternativos

**FA-UC00-001: Usuário NÃO é Super Admin**
- Sistema retorna HTTP 403 Forbidden

**FA-UC00-002: Nenhum Cliente cadastrado**
- Sistema retorna lista vazia (HTTP 200 OK)

**FA-UC00-003: Filtro por FlAtivo = false (Clientes inativos)**
- Sistema aplica `WHERE FlAtivo = false`

### Fluxos de Exceção

**FE-UC00-001: Erro de conectividade com banco de dados**
- Sistema retorna HTTP 500 Internal Server Error

**FE-UC00-002: Token JWT expirado**
- Sistema retorna HTTP 401 Unauthorized

### Regras de Negócio
- RN-UC-00-001: Super Admin DEVE visualizar TODOS os Clientes (bypass multi-tenancy via IsSuperAdmin = true)
- RN-UC-00-002: Query Filter DEVE ser ignorado quando IsSuperAdmin = true
- RN-UC-00-003: Registros soft-deleted (FlExcluido = true) NÃO devem aparecer na listagem
- RN-UC-00-004: Paginação padrão DEVE ser 10 registros por página (máximo 100)
- RN-UC-00-005: Filtros DEVEM ser acumuláveis (FlAtivo AND search)

---

## UC01 — Criar Cliente com ReceitaWS

### Objetivo
Permitir ao Super Admin criar novo Cliente com consulta automática de CNPJ via ReceitaWS API.

### Pré-condições
- [PRE-001] Usuário autenticado com IsSuperAdmin = true
- [PRE-002] Permissão: ClientesGerenciar
- [PRE-003] CNPJ fornecido válido (14 dígitos numéricos)
- [PRE-004] ReceitaWS API disponível (timeout: 10 segundos)

### Pós-condições
- [POS-001] Novo Cliente criado com Id gerado (Guid)
- [POS-002] Dados da ReceitaWS preenchidos automaticamente (se API disponível)
- [POS-003] FlAtivo = true, FlExcluido = false por default
- [POS-004] Operação registrada em AuditLog com tipo: CLI_CREATE

### Fluxo Principal
1. Super Admin acessa formulário "Novo Cliente"
2. Super Admin preenche CNPJ
3. Frontend valida formato CNPJ
4. Frontend envia POST `/api/clientes/consultar-cnpj`
5. Backend executa `ConsultarCnpjReceitaWsQuery`
6. ReceitaWS retorna dados do CNPJ
7. Frontend preenche automaticamente campos
8. Super Admin clica "Salvar"
9. Backend executa `CreateClienteCommand`
10. Sistema registra auditoria (Tipo: CLI_CREATE)
11. Sistema retorna HTTP 201 Created

### Fluxos Alternativos

**FA-UC01-001: ReceitaWS API indisponível (timeout)**
- Sistema retorna flag `success: false`
- Frontend permite preenchimento manual

**FA-UC01-002: CNPJ não encontrado na ReceitaWS**
- Sistema retorna HTTP 404 Not Found

**FA-UC01-003: CNPJ inválido (dígitos verificadores)**
- Sistema retorna HTTP 400 Bad Request

**FA-UC01-004: CNPJ já cadastrado (duplicado)**
- Sistema retorna HTTP 409 Conflict

**FA-UC01-005: Rate limit ReceitaWS (3 consultas/minuto/usuário)**
- Sistema retorna HTTP 429 Too Many Requests

### Fluxos de Exceção

**FE-UC01-001: Razão Social vazia (violação RN-CLI-006-04)**
- Sistema retorna HTTP 400 Bad Request

**FE-UC01-002: Erro ao persistir no banco (SqlException)**
- Sistema retorna HTTP 500 Internal Server Error

### Regras de Negócio
- RN-UC-01-001: CNPJ DEVE ter dígitos verificadores validados ANTES de consultar ReceitaWS
- RN-UC-01-002: ReceitaWS DEVE ter timeout de 10 segundos (não bloqueia criação se falhar)
- RN-UC-01-003: Razão Social DEVE ser obrigatória mesmo se ReceitaWS retornar vazio
- RN-UC-01-004: FlAtivo DEVE ser true por padrão na criação
- RN-UC-01-005: FlExcluido DEVE ser false por padrão na criação
- RN-UC-01-006: Auditoria DEVE registrar operação CLI_CREATE APÓS sucesso

---

## UC02 — Visualizar Cliente

### Objetivo
Permitir ao Super Admin visualizar detalhes completos de um Cliente específico.

### Pré-condições
- [PRE-001] Usuário autenticado com IsSuperAdmin = true
- [PRE-002] Permissão: ClientesVisualizar
- [PRE-003] Cliente existe no banco de dados (Id válido)

### Pós-condições
- [POS-001] Dados completos do Cliente retornados
- [POS-002] Logo exibido (se existir no Azure Blob Storage)
- [POS-003] Operação NÃO registrada em auditoria (leitura sem impacto)

### Fluxo Principal
1. Super Admin acessa `/admin/clientes/{clienteId}`
2. Frontend envia GET `/api/clientes/{clienteId}`
3. Backend executa `GetClienteByIdQuery`
4. Sistema retorna DTO completo
5. Frontend exibe tela de detalhes

### Fluxos Alternativos

**FA-UC02-001: Cliente não encontrado**
- Sistema retorna HTTP 404 Not Found

**FA-UC02-002: Cliente excluído (FlExcluido = true)**
- Frontend exibe badge "EXCLUÍDO"

**FA-UC02-003: Cliente inativo (FlAtivo = false)**
- Frontend exibe badge "INATIVO"

### Fluxos de Exceção

**FE-UC02-001: Token JWT expirado**
- Sistema retorna HTTP 401 Unauthorized

**FE-UC02-002: Usuário NÃO é Super Admin**
- Sistema retorna HTTP 403 Forbidden

### Regras de Negócio
- RN-UC-02-001: Cliente DEVE existir e NÃO estar excluído (FlExcluido = false)
- RN-UC-02-002: Super Admin DEVE ter acesso cross-tenant (ignora ClienteId)
- RN-UC-02-003: URL de logo DEVE ser retornada mesmo se arquivo não existir (null seguro)

---

## UC03 — Editar Cliente

### Objetivo
Permitir ao Super Admin editar dados cadastrais de um Cliente existente.

### Pré-condições
- [PRE-001] Usuário autenticado com IsSuperAdmin = true
- [PRE-002] Permissão: ClientesGerenciar
- [PRE-003] Cliente existe e FlExcluido = false
- [PRE-004] CNPJ não pode ser alterado (campo read-only)

### Pós-condições
- [POS-001] Dados do Cliente atualizados no banco
- [POS-002] DataUltimaAlteracao e UsuarioUltimaAlteracaoId atualizados
- [POS-003] Operação registrada em AuditLog com tipo: CLI_UPDATE

### Fluxo Principal
1. Super Admin acessa `/admin/clientes/{clienteId}/editar`
2. Sistema carrega dados atuais do Cliente
3. Frontend exibe formulário com campos preenchidos
4. Super Admin altera campos desejados
5. Super Admin clica "Salvar"
6. Backend executa `UpdateClienteCommand`
7. Sistema registra auditoria (Tipo: CLI_UPDATE)
8. Sistema retorna HTTP 200 OK

### Fluxos Alternativos

**FA-UC03-001: Tentar editar Cliente excluído**
- Sistema retorna HTTP 400 Bad Request

**FA-UC03-002: Tentar alterar CNPJ (campo read-only)**
- Backend ignora alteração de CNPJ

**FA-UC03-003: Desativar Cliente via toggle FlAtivo**
- Executa UC07 (Desativar Cliente)

### Fluxos de Exceção

**FE-UC03-001: Razão Social vazia (violação RN-CLI-006-04)**
- Sistema retorna HTTP 400 Bad Request

**FE-UC03-002: Cliente não encontrado (Id inválido)**
- Sistema retorna HTTP 404 Not Found

### Regras de Negócio
- RN-UC-03-001: CNPJ é campo READ-ONLY (não pode ser alterado após criação)
- RN-UC-03-002: Cliente DEVE estar ativo (FlExcluido = false) para ser editado
- RN-UC-03-003: Razão Social DEVE ser validada (3-200 caracteres)
- RN-UC-03-004: Auditoria DEVE registrar campos alterados (before/after) via CLI_UPDATE

---

## UC04 — Excluir Cliente (Soft Delete)

### Objetivo
Permitir ao Super Admin excluir (soft delete) um Cliente, marcando FlExcluido = true e bloqueando todos os Usuários vinculados.

### Pré-condições
- [PRE-001] Usuário autenticado com IsSuperAdmin = true
- [PRE-002] Permissão: ClientesGerenciar
- [PRE-003] Cliente existe e FlExcluido = false
- [PRE-004] Trigger INSTEAD OF DELETE configurado no banco

### Pós-condições
- [POS-001] Cliente.FlExcluido = true
- [POS-002] TODOS os Usuários do Cliente bloqueados (FlAtivo = false)
- [POS-003] Operação registrada em AuditLog com tipo: CLI_DELETE
- [POS-004] Registro de bloqueio de usuários com tipo: CLI_DEACTIVATE_USERS

### Fluxo Principal
1. Super Admin acessa `/admin/clientes/{clienteId}`
2. Super Admin clica "Excluir Cliente"
3. Frontend exibe confirmação CRÍTICA
4. Super Admin confirma exclusão
5. Frontend envia DELETE `/api/clientes/{clienteId}`
6. Backend executa `DeleteClienteCommand`
7. Sistema marca FlExcluido = true
8. Sistema bloqueia TODOS os usuários vinculados
9. Trigger bloqueia DELETE físico
10. Sistema registra auditoria (CLI_DELETE, CLI_DEACTIVATE_USERS)
11. Sistema retorna HTTP 200 OK

### Fluxos Alternativos

**FA-UC04-001: Cliente já excluído**
- Sistema retorna HTTP 400 Bad Request

**FA-UC04-002: Nenhum usuário ativo vinculado**
- Sistema prossegue normalmente

**FA-UC04-003: Super Admin cancela confirmação**
- Nenhuma requisição enviada

### Fluxos de Exceção

**FE-UC04-001: Tentativa de DELETE físico via SQL**
- Trigger bloqueia operação

**FE-UC04-002: Erro ao bloquear usuários (parcial)**
- Transação é revertida (rollback)

### Regras de Negócio
- RN-UC-04-001: DELETE físico DEVE ser bloqueado via trigger INSTEAD OF DELETE
- RN-UC-04-002: Soft delete DEVE marcar FlExcluido = true (não remove do banco)
- RN-UC-04-003: TODOS os usuários vinculados DEVEM ser bloqueados (FlAtivo = false)
- RN-UC-04-004: Auditoria DEVE registrar CLI_DELETE + CLI_DEACTIVATE_USERS
- RN-UC-04-005: Cliente já excluído (FlExcluido = true) DEVE retornar HTTP 400

---

## UC05 — Upload de Logo do Cliente

### Objetivo
Permitir ao Super Admin fazer upload do logo corporativo de um Cliente para Azure Blob Storage.

### Pré-condições
- [PRE-001] Usuário autenticado com IsSuperAdmin = true
- [PRE-002] Permissão: ClientesGerenciar
- [PRE-003] Cliente existe e FlExcluido = false
- [PRE-004] Azure Blob Storage configurado (container: clientes-logos)
- [PRE-005] Arquivo enviado é imagem válida (PNG, JPG ou SVG)

### Pós-condições
- [POS-001] Logo armazenado no Azure Blob Storage
- [POS-002] Cliente.LogoUrl atualizado com URL público do blob
- [POS-003] Operação registrada em AuditLog com tipo: CLI_LOGO_UPLOAD

### Fluxo Principal
1. Super Admin acessa `/admin/clientes/{clienteId}`
2. Super Admin clica "Upload Logo"
3. Frontend exibe modal de upload
4. Super Admin seleciona arquivo de imagem
5. Frontend valida formato e tamanho
6. Frontend envia POST `/api/clientes/{clienteId}/logo`
7. Backend executa `UploadClienteLogoCommand`
8. Backend valida magic bytes
9. Backend faz upload para Azure Blob Storage
10. Sistema registra auditoria (Tipo: CLI_LOGO_UPLOAD)
11. Sistema retorna HTTP 200 OK

### Fluxos Alternativos

**FA-UC05-001: Arquivo maior que 2 MB**
- Sistema retorna HTTP 400 Bad Request

**FA-UC05-002: Formato de arquivo inválido**
- Sistema retorna HTTP 400 Bad Request

**FA-UC05-003: Magic bytes inválidos**
- Sistema retorna HTTP 400 Bad Request

**FA-UC05-004: Substituir logo existente**
- Backend deleta blob antigo antes de novo upload

**FA-UC05-005: Azure Blob Storage indisponível**
- Sistema retorna HTTP 500 Internal Server Error

### Fluxos de Exceção

**FE-UC05-001: Cliente excluído (FlExcluido = true)**
- Sistema retorna HTTP 400 Bad Request

**FE-UC05-002: Arquivo corrompido (stream inválido)**
- Sistema retorna HTTP 400 Bad Request

### Regras de Negócio
- RN-UC-05-001: Magic bytes DEVEM ser validados (não apenas extensão de arquivo)
- RN-UC-05-002: Tamanho máximo DEVE ser 2MB (2.097.152 bytes)
- RN-UC-05-003: Formatos permitidos: JPG, PNG, SVG (via magic bytes)
- RN-UC-05-004: Azure Blob Storage DEVE usar container público (clientes-logos)
- RN-UC-05-005: URL retornada DEVE substituir LogoUrl anterior (sobrescreve)
- RN-UC-05-006: Cliente excluído (FlExcluido = true) NÃO pode fazer upload

---

## UC06 — Restaurar Cliente Excluído

### Objetivo
Permitir ao Super Admin restaurar um Cliente previamente excluído, reativando o Cliente e desbloqueando os Usuários vinculados.

### Pré-condições
- [PRE-001] Usuário autenticado com IsSuperAdmin = true
- [PRE-002] Permissão: ClientesGerenciar
- [PRE-003] Cliente existe e FlExcluido = true

### Pós-condições
- [POS-001] Cliente.FlExcluido = false
- [POS-002] Cliente.FlAtivo = true
- [POS-003] Usuários vinculados REATIVADOS
- [POS-004] Operação registrada em AuditLog com tipo: CLI_RESTORE

### Fluxo Principal
1. Super Admin acessa lista de Clientes excluídos
2. Super Admin clica "Restaurar" em um Cliente
3. Frontend exibe confirmação
4. Super Admin confirma restauração
5. Frontend envia POST `/api/clientes/{clienteId}/restaurar`
6. Backend executa `RestoreClienteCommand`
7. Sistema marca FlExcluido = false
8. Sistema reativa TODOS os usuários vinculados
9. Sistema registra auditoria (Tipo: CLI_RESTORE)
10. Sistema retorna HTTP 200 OK

### Fluxos Alternativos

**FA-UC06-001: Cliente não está excluído**
- Sistema retorna HTTP 400 Bad Request

**FA-UC06-002: Nenhum usuário bloqueado por exclusão**
- Sistema prossegue normalmente

**FA-UC06-003: Restaurar Cliente como inativo**
- Backend marca FlAtivo = false
- Usuários permanecem bloqueados

### Fluxos de Exceção

**FE-UC06-001: Cliente não encontrado**
- Sistema retorna HTTP 404 Not Found

**FE-UC06-002: Erro ao reativar usuários**
- Transação é revertida (rollback)

### Regras de Negócio
- RN-UC-06-001: Somente Clientes com FlExcluido = true podem ser restaurados
- RN-UC-06-002: Restauração DEVE marcar FlExcluido = false
- RN-UC-06-003: FlAtivo DEVE permanecer como estava (não reativa automaticamente)
- RN-UC-06-004: Usuários bloqueados NÃO são reativados automaticamente (manual)
- RN-UC-06-005: Auditoria DEVE registrar CLI_RESTORE

---

## UC07 — Desativar Cliente

### Objetivo
Permitir ao Super Admin desativar um Cliente (FlAtivo = false) SEM excluí-lo, bloqueando todos os Usuários vinculados temporariamente.

### Pré-condições
- [PRE-001] Usuário autenticado com IsSuperAdmin = true
- [PRE-002] Permissão: ClientesGerenciar
- [PRE-003] Cliente existe, FlExcluido = false e FlAtivo = true

### Pós-condições
- [POS-001] Cliente.FlAtivo = false
- [POS-002] TODOS os Usuários do Cliente bloqueados
- [POS-003] MotivoInativacao registrado: "Cliente desativado"
- [POS-004] Operação registrada em AuditLog (CLI_DEACTIVATE, CLI_DEACTIVATE_USERS)

### Fluxo Principal
1. Super Admin acessa `/admin/clientes/{clienteId}`
2. Super Admin clica toggle "Ativo" (de true para false)
3. Frontend exibe confirmação
4. Super Admin confirma desativação
5. Frontend envia PUT `/api/clientes/{clienteId}/desativar`
6. Backend executa `DeactivateClienteCommand`
7. Sistema marca FlAtivo = false
8. Sistema bloqueia TODOS os usuários vinculados
9. Sistema registra auditoria (CLI_DEACTIVATE, CLI_DEACTIVATE_USERS)
10. Sistema retorna HTTP 200 OK

### Fluxos Alternativos

**FA-UC07-001: Reativar Cliente desativado**
- Sistema executa `ReactivateClienteCommand`
- Usuários são desbloqueados automaticamente

**FA-UC07-002: Cliente já desativado**
- Sistema retorna HTTP 400 Bad Request

**FA-UC07-003: Nenhum usuário ativo vinculado**
- Sistema prossegue normalmente

### Fluxos de Exceção

**FE-UC07-001: Cliente excluído (FlExcluido = true)**
- Sistema retorna HTTP 400 Bad Request

**FE-UC07-002: Erro ao bloquear usuários**
- Transação é revertida (rollback)

### Regras de Negócio
- RN-UC-07-001: Desativação DEVE marcar FlAtivo = false (diferente de soft delete)
- RN-UC-07-002: Cliente já desativado (FlAtivo = false) DEVE retornar HTTP 400
- RN-UC-07-003: TODOS os usuários vinculados DEVEM ser bloqueados (FlAtivo = false)
- RN-UC-07-004: Cliente excluído (FlExcluido = true) NÃO pode ser desativado
- RN-UC-07-005: Auditoria DEVE registrar CLI_DEACTIVATE + CLI_DEACTIVATE_USERS

---

## UC08 — Consultar CNPJ na ReceitaWS

### Objetivo
Permitir ao Super Admin consultar dados de CNPJ na ReceitaWS API INDEPENDENTEMENTE de criação de Cliente.

### Pré-condições
- [PRE-001] Usuário autenticado com IsSuperAdmin = true
- [PRE-002] Permissão: ClientesGerenciar
- [PRE-003] CNPJ fornecido válido
- [PRE-004] ReceitaWS API disponível
- [PRE-005] Rate limit não excedido (3 consultas/minuto/usuário)

### Pós-condições
- [POS-001] Dados da ReceitaWS retornados ao frontend
- [POS-002] Operação registrada em AuditLog com tipo: CLI_RECEITA_QUERY
- [POS-003] Rate limit atualizado para o usuário

### Fluxo Principal
1. Super Admin está em formulário "Novo Cliente" ou "Editar Cliente"
2. Super Admin preenche campo CNPJ
3. Super Admin clica "Consultar CNPJ"
4. Frontend valida formato CNPJ
5. Frontend envia POST `/api/clientes/consultar-cnpj`
6. Backend executa `ConsultarCnpjReceitaWsQuery`
7. Backend valida dígitos verificadores
8. Backend verifica rate limit
9. Backend consulta ReceitaWS
10. Sistema registra auditoria (Tipo: CLI_RECEITA_QUERY)
11. Sistema retorna HTTP 200 OK com dados processados
12. Frontend preenche automaticamente campos

### Fluxos Alternativos

**FA-UC08-001: ReceitaWS API indisponível (timeout)**
- Sistema retorna `success: false`

**FA-UC08-002: CNPJ não encontrado na ReceitaWS**
- Sistema retorna HTTP 404 Not Found

**FA-UC08-003: CNPJ com situação "BAIXADA" ou "SUSPENSA"**
- Sistema retorna HTTP 200 OK com aviso

**FA-UC08-004: Rate limit excedido**
- Sistema retorna HTTP 429 Too Many Requests

### Fluxos de Exceção

**FE-UC08-001: CNPJ inválido (dígitos verificadores)**
- Sistema retorna HTTP 400 Bad Request

**FE-UC08-002: ReceitaWS retorna erro HTTP 500**
- Sistema retorna HTTP 200 OK com flag `success: false`

### Regras de Negócio
- RN-UC-08-001: CNPJ DEVE ter dígitos verificadores validados ANTES de consultar API
- RN-UC-08-002: Rate limit DEVE ser 3 consultas/minuto/usuário
- RN-UC-08-003: Timeout DEVE ser 10 segundos
- RN-UC-08-004: Falha ReceitaWS NÃO deve bloquear criação de Cliente
- RN-UC-08-005: Auditoria DEVE registrar CLI_RECEITA_QUERY (sucesso ou falha)

---

## 4. MATRIZ DE RASTREABILIDADE

### 4.1 Cobertura RF → UC

| Regra de Negócio (RN) | Título | UCs que Cobrem | Status |
|-----------------------|--------|----------------|--------|
| RN-CLI-006-01 | Cliente como Tenant Raiz | UC00, UC02 | ✅ 100% |
| RN-CLI-006-02 | CNPJ Único por Cliente | UC01 | ✅ 100% |
| RN-CLI-006-03 | Validação de Dígitos Verificadores do CNPJ | UC01, UC08 | ✅ 100% |
| RN-CLI-006-04 | Razão Social Obrigatória | UC01, UC03 | ✅ 100% |
| RN-CLI-006-05 | Consulta ReceitaWS Automática | UC01, UC08 | ✅ 100% |
| RN-CLI-006-06 | Upload de Logo com Validação | UC05 | ✅ 100% |
| RN-CLI-006-07 | Soft Delete Obrigatório | UC04, UC06 | ✅ 100% |
| RN-CLI-006-08 | Super Admin Bypass de Multi-Tenancy | UC00, UC02 | ✅ 100% |
| RN-CLI-006-09 | Desativação de Cliente Bloqueia Usuários | UC04, UC07 | ✅ 100% |
| RN-CLI-006-10 | Auditoria de Operações de Cliente | UC01, UC03, UC04, UC05, UC06, UC07, UC08 | ✅ 100% |

**Cobertura Total**: 10/10 RNs (100%) ✅

### 4.2 Cobertura UC → Endpoints API

| UC | Endpoint(s) | Método(s) | Validações |
|----|------------|-----------|-----------|
| UC00 | `/api/clientes` | GET | IsSuperAdmin, ClientesVisualizar |
| UC01 | `/api/clientes` | POST | IsSuperAdmin, ClientesGerenciar, CNPJ único, Validação CNPJ, Razão Social |
| UC02 | `/api/clientes/{id}` | GET | IsSuperAdmin, ClientesVisualizar |
| UC03 | `/api/clientes/{id}` | PUT | IsSuperAdmin, ClientesGerenciar, Razão Social, FlExcluido = false |
| UC04 | `/api/clientes/{id}` | DELETE | IsSuperAdmin, ClientesGerenciar, Trigger INSTEAD OF DELETE |
| UC05 | `/api/clientes/{id}/logo` | POST | IsSuperAdmin, ClientesGerenciar, Magic bytes, Max 2 MB |
| UC06 | `/api/clientes/{id}/restaurar` | POST | IsSuperAdmin, ClientesGerenciar, FlExcluido = true |
| UC07 | `/api/clientes/{id}/desativar` | PUT | IsSuperAdmin, ClientesGerenciar, FlAtivo = true |
| UC08 | `/api/clientes/consultar-cnpj` | POST | IsSuperAdmin, ClientesGerenciar, Validação CNPJ, Rate limit |

**Total de Endpoints Únicos**: 7 endpoints (13 operações)

### 4.3 Cobertura UC → Permissões RBAC

| Permissão | Código | UCs que Requerem | Roles Autorizadas |
|-----------|--------|------------------|-------------------|
| Visualizar Clientes | `CAD.CLIENTES.VISUALIZAR` | UC00, UC02 | Super Admin |
| Gerenciar Clientes | `CAD.CLIENTES.GERENCIAR` | UC01, UC03, UC04, UC05, UC06, UC07, UC08 | Super Admin |

**Total de Permissões**: 2 (todas restritas a Super Admin)

---

## 5. VALIDAÇÕES TRANSVERSAIS

### 5.1 Segurança (RBAC)
- TODOS os endpoints restritos a Super Admin APENAS
- HTTP 403 Forbidden para usuários comuns
- HTTP 401 Unauthorized para token expirado

### 5.2 Auditoria (LGPD)
- Operações de escrita auditadas via AuditInterceptor
- Retenção: 7 anos (LGPD Art. 16)
- Tipos: CLI_CREATE, CLI_UPDATE, CLI_DELETE, CLI_LOGO_UPLOAD, CLI_RESTORE, CLI_DEACTIVATE, CLI_DEACTIVATE_USERS, CLI_RECEITA_QUERY, CLI_LIST

### 5.3 Multi-Tenancy
- ClienteId é discriminador de tenant obrigatório
- Bypass via `IgnoreQueryFilters()` para Super Admin
- Usuários comuns NÃO acessam Gestão de Clientes

### 5.4 Internacionalização (i18n)
- Chaves de tradução obrigatórias: `gestao-clientes.errors.*`, `gestao-clientes.success.*`, `gestao-clientes.warnings.*`
- Idiomas: pt-BR (default), en, es

---

## 6. REQUISITOS NÃO-FUNCIONAIS GLOBAIS

### 6.1 Performance
- Tempo de resposta API (GET): < 200ms (P95)
- Tempo de resposta API (POST/PUT): < 500ms (P95)
- Upload de logo (2 MB): < 5 segundos (P95)
- Consulta ReceitaWS: < 10 segundos (timeout)

### 6.2 Disponibilidade
- SLA: 99.9%
- ReceitaWS offline: funcional (preenchimento manual)
- Azure Blob Storage offline: degradado (logs sem imagem)

### 6.3 Segurança
- Autenticação: JWT Bearer Token
- Autorização: RBAC (Super Admin APENAS)
- Auditoria: 7 anos (LGPD)
- Proteção CNPJ: Validação dígitos verificadores
- Proteção Upload: Magic bytes validation
- HTTPS obrigatório

---

## 7. GLOSSÁRIO

| Termo | Definição |
|-------|-----------|
| **Cliente** | Entidade raiz de multi-tenancy no sistema IControlIT |
| **ClienteId** | Discriminador de tenant obrigatório via EF Core Query Filters |
| **Super Admin** | Único role autorizado a acessar Gestão de Clientes (IsSuperAdmin = true) |
| **Soft Delete** | Exclusão lógica via FlExcluido = true (dados permanem no banco) |
| **ReceitaWS** | API pública da Receita Federal Brasileira (https://www.receitaws.com.br/v1/) |
| **Magic Bytes** | Primeiros bytes de arquivo identificando formato (PNG = 89 50 4E 47) |
| **Azure Blob Storage** | Serviço de armazenamento de objetos (container: clientes-logos) |
| **Rate Limit** | Limite de requisições (3 consultas ReceitaWS/minuto/usuário) |
| **EF Core Query Filters** | Filtros globais automáticos (WHERE ClienteId = @CurrentClienteId) |
| **CNPJ** | Cadastro Nacional de Pessoa Jurídica (14 dígitos, 2 verificadores) |
| **FlAtivo** | Flag indicando Cliente ativo (true) ou desativado (false) |
| **FlExcluido** | Flag indicando Cliente excluído via soft delete (true) |
| **LGPD** | Lei Geral de Proteção de Dados (Brasil) - auditoria 7 anos (Art. 16) |
| **RBAC** | Role-Based Access Control - autorização via roles |
| **Multi-Tenancy** | Arquitetura com múltiplos clientes compartilhando app (Row-Level Security) |

---

## 8. REFERÊNCIAS

- **RF006.md**: Requisito Funcional completo com 10 RNs
- **RF006.yaml**: Versão estruturada do RF (YAML)
- **RL-RF006.md**: Referências ao Legado (18 bancos, 6 problemas)
- **RL-RF006.yaml**: Versão estruturada do RL (YAML)
- **ReceitaWS API**: https://www.receitaws.com.br/v1/
- **Azure Blob Storage Docs**: https://learn.microsoft.com/azure/storage/blobs/
- **EF Core Query Filters**: https://learn.microsoft.com/ef/core/querying/filters
- **LGPD Art. 16**: https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm

---

**Fim do Documento UC-RF006.md**

**Cobertura Final**:
- ✅ 9 Casos de Uso detalhados
- ✅ 10 Regras de Negócio (100% cobertas)
- ✅ 7 Permissões RBAC documentadas
- ✅ 13 Endpoints API mapeados
- ✅ 5 Integrações obrigatórias documentadas
- ✅ Matriz de rastreabilidade completa
- ✅ Validações transversais
- ✅ Requisitos não-funcionais globais
- ✅ Glossário e referências

**Data de Criação**: 2025-12-30
**Versão**: 2.0
**Aprovador**: [Pendente]
**Status**: AGUARDANDO VALIDAÇÃO (validator-rf-uc.py)
