# UC-RF012 — Casos de Uso Canônicos

**RF:** RF-012 — Gestão de Usuários do Sistema
**Epic:** EPIC002-CAD - Cadastros Sistema
**Fase:** Fase 1 - Sistema Base
**Versão:** 2.0
**Data:** 2025-12-31
**Autor:** Agência ALC - alc.dev.br

---

## Índice de Casos de Uso

| UC | Nome | Descrição |
|----|------|-----------|
| UC00 | UC00 - Listar Usuários | Caso de uso |
| UC01 | UC01 - Criar Usuário - Especificação Completa | Permite que usuários autorizados criem novos usuários no sistema, definindo suas informações pessoai |
| UC02 | Visualizar Usuário - Especificação Completa | Caso de uso |
| UC03 | Editar Usuário - Especificação Completa | Caso de uso |
| UC04 | Excluir Usuário - Especificação Completa | Caso de uso |
| UC08 | UC08 - Gerenciar Usuários do Perfil | Caso de uso |

---

# UC00 - Listar Usuários

**Requisito Funcional:** RF-CAD-005 - Gestão de Usuários do Sistema
**Ator Principal:** Administrador, Gestor
**Objetivo:** Visualizar lista de usuários do sistema com opções de filtro e pesquisa
**Pré-condições:**
- Usuário autenticado no sistema
- Usuário possui permissão `users:user:read`

---

## 1. Fluxo Principal

1. Usuário acessa o menu "Gestão de Usuários"
2. Sistema carrega e exibe lista de usuários
3. Sistema exibe para cada usuário:
   - Nome completo
   - Email
   - Perfis (roles) associados
   - Status (Ativo/Inativo)
   - Empresa vinculada
   - Avatar (se houver)
4. Sistema permite as seguintes ações:
   - Criar novo usuário (redireciona para UC01)
   - Visualizar detalhes (redireciona para UC02)
   - Editar usuário (redireciona para UC03)
   - Excluir usuário (executa UC04)
   - Filtrar por empresa
   - Filtrar por status (ativo/inativo)
   - Pesquisar por nome ou email
5. Caso de uso encerrado

---

## 2. Fluxos Alternativos

### FA-01: Filtrar por Empresa
**Quando:** Usuário seleciona uma empresa no filtro (passo 4)

1. Sistema recarrega lista exibindo apenas usuários da empresa selecionada
2. Retorna ao passo 4 do fluxo principal

### FA-02: Filtrar por Status
**Quando:** Usuário seleciona um status no filtro (passo 4)

1. Sistema recarrega lista exibindo apenas usuários com o status selecionado (ativo ou inativo)
2. Retorna ao passo 4 do fluxo principal

### FA-03: Pesquisar Usuário
**Quando:** Usuário digita texto no campo de pesquisa (passo 4)

1. Sistema filtra lista em tempo real
2. Exibe apenas usuários cujo nome ou email contém o texto digitado
3. Retorna ao passo 4 do fluxo principal

### FA-04: Nenhum Usuário Encontrado
**Quando:** Filtros aplicados não retornam resultados (passo 2)

1. Sistema exibe mensagem "Nenhum usuário encontrado"
2. Sistema oferece opção de limpar filtros
3. Retorna ao passo 4 do fluxo principal

---

## 3. Fluxos de Exceção

### FE-01: Erro ao Carregar Lista
**Quando:** Erro de comunicação com API (passo 2)

1. Sistema exibe mensagem de erro: "Não foi possível carregar a lista de usuários"
2. Sistema oferece botão "Tentar novamente"
3. Se usuário clicar em "Tentar novamente", retorna ao passo 2
4. Caso de uso encerrado

### FE-02: Permissão Insuficiente
**Quando:** Usuário não possui permissão `users:user:read` (pré-condição)

1. Sistema exibe mensagem: "Você não tem permissão para visualizar usuários"
2. Sistema redireciona para página inicial
3. Caso de uso encerrado

### FE-03: Sessão Expirada
**Quando:** Token de autenticação expirado durante carregamento (passo 2)

1. Sistema exibe mensagem: "Sua sessão expirou"
2. Sistema redireciona para tela de login
3. Caso de uso encerrado

---

## 4. Regras de Negócio

**RN-01: Multi-tenancy**
- Usuários só podem visualizar usuários da mesma empresa (EmpresaId)
- Exceção: Perfis de sistema (IsSystemRole = true) podem visualizar todos

**RN-02: Hierarquia**
- Usuários só podem visualizar/gerenciar usuários com perfis de hierarquia inferior
- Exemplo: Admin (nivel 1) não pode gerenciar Super Admin (nivel 0)

**RN-03: Paginação**
- Lista é paginada automaticamente quando > 50 registros
- Tamanho de página padrão: 50 itens

**RN-04: Ordenação Padrão**
- Lista ordenada por Nome (A-Z) por padrão
- Usuário pode alterar ordenação clicando nas colunas

---

## 5. Especificação Técnica

### 5.1 Endpoint API

**Request:**
```http
GET /api/usuarios?empresaId={guid}&ativo={boolean}
Authorization: Bearer {token}
```

**Query Parameters:**
| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| empresaId | Guid | Não | Filtrar por empresa específica |
| ativo | Boolean | Não | Filtrar por status (true = ativo, false = inativo) |

**Response 200 OK:**
```json
[
  {
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "email": "usuario@example.com",
    "nome": "João Silva",
    "telefone": "(11) 98765-4321",
    "avatar": "https://cdn.example.com/avatars/joao.jpg",
    "ativo": true,
    "empresaId": "4fa85f64-5717-4562-b3fc-2c963f66afa7",
    "empresaNome": "Empresa XYZ",
    "roles": [
      {
        "id": "5fa85f64-5717-4562-b3fc-2c963f66afa8",
        "nome": "Administrador"
      }
    ]
  }
]
```

**Response 403 Forbidden:**
```json
{
  "message": "Você não tem permissão para visualizar usuários"
}
```

### 5.2 Implementação Backend

**Query Handler:** `GetUsuariosQuery` em `D:\IC2\backend\IControlIT.API\src\Application\Usuarios\Queries\GetUsuarios\GetUsuarios.cs`

**Validações aplicadas:**
1. Verificar permissão `users:user:read` via `AuthorizationPolicies.UsersRead`
2. Aplicar filtro de EmpresaId (multi-tenancy)
3. Aplicar filtro de hierarquia (usuário só vê perfis inferiores)
4. Aplicar filtros opcionais (empresaId, ativo)

### 5.3 Implementação Frontend

**Componente:** `ListComponent` em `D:\IC2\frontend\icontrolit-app\src\app\modules\admin\management\users\list\list.component.ts`

**Service:** `UsersService.getUsuarios()` em `D:\IC2\frontend\icontrolit-app\src\app\modules\admin\management\users\users.service.ts`

**Features implementadas:**
- Grid responsivo com colunas: Avatar, Nome, Email, Roles, Status, Ações
- Filtros: Empresa (dropdown), Status (toggle), Pesquisa (input text)
- Ações: Criar, Visualizar, Editar, Excluir
- Paginação automática
- Loading state durante carregamento

---

## 6. Casos de Teste

### CT-001: Listar Todos os Usuários
**Pré-condição:** Existem 10 usuários cadastrados
**Passos:**
1. Acessar tela de listagem
2. Verificar carregamento

**Resultado esperado:**
- Sistema exibe 10 usuários
- Ordenados por Nome (A-Z)

### CT-002: Filtrar por Empresa
**Pré-condição:** Existem usuários de 2 empresas diferentes
**Passos:**
1. Acessar tela de listagem
2. Selecionar "Empresa A" no filtro

**Resultado esperado:**
- Sistema exibe apenas usuários da Empresa A

### CT-003: Filtrar por Status Ativo
**Pré-condição:** Existem usuários ativos e inativos
**Passos:**
1. Acessar tela de listagem
2. Selecionar "Apenas ativos" no filtro

**Resultado esperado:**
- Sistema exibe apenas usuários com Ativo = true

### CT-004: Pesquisar por Nome
**Pré-condição:** Existe usuário "João Silva"
**Passos:**
1. Acessar tela de listagem
2. Digitar "João" no campo de pesquisa

**Resultado esperado:**
- Sistema exibe apenas usuários com "João" no nome

### CT-005: Pesquisar por Email
**Pré-condição:** Existe usuário com email "joao@example.com"
**Passos:**
1. Acessar tela de listagem
2. Digitar "joao@" no campo de pesquisa

**Resultado esperado:**
- Sistema exibe apenas usuários com "joao@" no email

### CT-006: Nenhum Resultado
**Passos:**
1. Acessar tela de listagem
2. Pesquisar por "XYZABC123" (não existe)

**Resultado esperado:**
- Sistema exibe mensagem "Nenhum usuário encontrado"
- Botão "Limpar filtros" visível

### CT-007: Permissão Negada
**Pré-condição:** Usuário sem permissão `users:user:read`
**Passos:**
1. Tentar acessar tela de listagem

**Resultado esperado:**
- Sistema exibe erro 403
- Mensagem "Você não tem permissão para visualizar usuários"
- Redireciona para página inicial

### CT-008: Hierarquia - Admin não vê Super Admin
**Pré-condição:** Usuário logado é Admin (nivel 1), existe Super Admin (nivel 0)
**Passos:**
1. Acessar tela de listagem

**Resultado esperado:**
- Lista NÃO inclui usuários com perfil Super Admin

### CT-009: Paginação
**Pré-condição:** Existem 150 usuários cadastrados
**Passos:**
1. Acessar tela de listagem
2. Verificar quantidade exibida

**Resultado esperado:**
- Sistema exibe 50 usuários (página 1)
- Controles de paginação visíveis (Próxima, Última)

### CT-010: Erro de Comunicação
**Pré-condição:** API está offline
**Passos:**
1. Tentar acessar tela de listagem

**Resultado esperado:**
- Sistema exibe erro de comunicação
- Botão "Tentar novamente" disponível

---

## 7. Critérios de Aceitação

✅ Lista carrega em menos de 2 segundos (para até 100 usuários)
✅ Filtros aplicam em tempo real (< 500ms)
✅ Pesquisa funciona por nome E email
✅ Apenas usuários autorizados podem acessar
✅ Multi-tenancy respeitado (usuário só vê sua empresa)
✅ Hierarquia respeitada (não exibe perfis superiores)
✅ Interface responsiva (funciona em mobile)
✅ Ações (criar/editar/excluir) habilitadas apenas se usuário tiver permissão

---

## 8. Histórico de Alterações

| Data | Versão | Autor | Descrição |
|------|--------|-------|-----------|
| 2025-10-26 | 1.0 | Sistema | Criação inicial do caso de uso |

---

**Status:** ✅ Implementado
**Endpoints:** `GET /api/usuarios` implementado em [Usuarios.cs:15-19](D:\IC2\backend\IControlIT.API\src\Web\Endpoints\Usuarios.cs#L15-L19)
**Frontend:** Implementado em [list.component.ts](D:\IC2\frontend\icontrolit-app\src\app\modules\admin\management\users\list\list.component.ts)

---

# UC01 - Criar Usuário - Especificação Completa

**Status**: Implementado ✅

---

## 📋 SUMÁRIO

1. [Informações Gerais](#informações-gerais)
2. [Fluxo Principal](#fluxo-principal)
3. [Fluxos Alternativos](#fluxos-alternativos)
4. [Fluxos de Exceção](#fluxos-de-exceção)
5. [Regras de Negócio](#regras-de-negócio)
6. [Especificação de Testes](#especificação-de-testes)
7. [Matriz de Permissões](#matriz-de-permissões)
8. [Casos de Teste Detalhados](#casos-de-teste-detalhados)

---

## INFORMAÇÕES GERAIS

### Descrição
Permite que usuários autorizados criem novos usuários no sistema, definindo suas informações pessoais, credenciais, perfis de acesso e empresa associada.

### Atores
- **Primário**: Administrador do Sistema, Super Admin
- **Secundário**: Sistema de Auditoria, Sistema de Notificações

### Pré-condições
1. Usuário deve estar autenticado no sistema
2. Usuário deve ter permissão `users:user:create`
3. Sistema deve estar online e conectado ao banco de dados
4. Deve existir pelo menos uma empresa cadastrada
5. Deve existir pelo menos um perfil/role cadastrado

### Pós-condições
**Sucesso**:
1. Novo usuário criado no banco de dados
2. Senha hashada com bcrypt
3. Log de auditoria registrado
4. Email de boas-vindas enviado (opcional)
5. Usuário pode fazer login imediatamente

**Falha**:
1. Nenhuma alteração no banco de dados
2. Log de tentativa falha registrado
3. Mensagem de erro exibida ao usuário

### Requisitos Não-Funcionais
- **Performance**: Criação deve completar em < 2 segundos
- **Segurança**: Senha deve ser hashada antes de armazenar
- **Usabilidade**: Validação em tempo real de campos
- **Auditoria**: Todas as tentativas devem ser logadas

---

## FLUXO PRINCIPAL

### FP01 - Criar Usuário com Sucesso

| Passo | Ator | Ação | Sistema |
|-------|------|------|---------|
| 1 | Usuário | Acessa menu "Usuários" | Exibe lista de usuários |
| 2 | Usuário | Clica em "Novo Usuário" | Exibe formulário vazio |
| 3 | Usuário | Preenche nome | Valida formato (mín 2 caracteres) |
| 4 | Usuário | Preenche email | Valida formato e unicidade |
| 5 | Usuário | Preenche senha | Valida força (mín 6 caracteres) |
| 6 | Usuário | Confirma senha | Valida se senha e confirmação são iguais |
| 7 | Usuário | Seleciona empresa | Valida se empresa existe e está ativa |
| 8 | Usuário | Seleciona perfil(is) | Valida se perfis existem e usuário pode atribuir |
| 9 | Usuário | Preenche telefone (opcional) | Valida formato se preenchido |
| 10 | Usuário | Define status (ativo/inativo) | Aceita boolean |
| 11 | Usuário | Clica em "Salvar" | Valida todos os campos |
| 12 | Sistema | - | Hash da senha com bcrypt |
| 13 | Sistema | - | Gera ID único (GUID) |
| 14 | Sistema | - | Define timestamps (criadoEm, atualizadoEm) |
| 15 | Sistema | - | Salva no banco de dados em transação |
| 16 | Sistema | - | Cria registro de auditoria |
| 17 | Sistema | - | Envia email de boas-vindas (async) |
| 18 | Sistema | - | Exibe toast "Usuário criado com sucesso" |
| 19 | Sistema | - | Redireciona para lista de usuários |
| 20 | Sistema | - | Destaca novo usuário na lista (3s) |

---

## FLUXOS ALTERNATIVOS

### FA01 - Criar Usuário Inativo

**Diverge no passo 10 do FP01**

| Passo | Ação |
|-------|------|
| 10a | Usuário desmarca checkbox "Ativo" |
| 10b | Sistema define `ativo = false` |
| 10c | Usuário criado mas não pode fazer login |
| 10d | Email de boas-vindas não é enviado |
| - | Retorna ao passo 11 do FP01 |

### FA02 - Criar Usuário com Múltiplos Perfis

**Diverge no passo 8 do FP01**

| Passo | Ação |
|-------|------|
| 8a | Usuário seleciona múltiplos perfis (multi-select) |
| 8b | Sistema valida que usuário pode atribuir TODOS os perfis selecionados |
| 8c | Sistema valida hierarquia (não pode criar usuário com perfil superior ao próprio) |
| 8d | Sistema cria relacionamento many-to-many na tabela UsuarioRole |
| - | Retorna ao passo 9 do FP01 |

### FA03 - Criar Usuário sem Telefone

**Diverge no passo 9 do FP01**

| Passo | Ação |
|-------|------|
| 9a | Usuário deixa campo telefone vazio |
| 9b | Sistema aceita (campo opcional) |
| 9c | Telefone salvo como NULL no banco |
| - | Retorna ao passo 10 do FP01 |

### FA04 - Cancelar Criação

**Pode ocorrer em qualquer passo antes de 11**

| Passo | Ação |
|-------|------|
| Xa | Usuário clica em "Cancelar" ou pressiona ESC |
| Xb | Sistema exibe confirmação "Descartar alterações?" |
| Xc1 | Se SIM: descarta dados e retorna à lista |
| Xc2 | Se NÃO: permanece no formulário |

### FA05 - Gerar Senha Automática

**Diverge no passo 5 do FP01**

| Passo | Ação |
|-------|------|
| 5a | Usuário clica em "Gerar Senha" |
| 5b | Sistema gera senha forte aleatória (12 caracteres) |
| 5c | Sistema preenche campo senha e confirmação |
| 5d | Sistema exibe senha gerada (com botão "Copiar") |
| 5e | Usuário copia senha para enviar ao novo usuário |
| - | Retorna ao passo 7 do FP01 |

---

## FLUXOS DE EXCEÇÃO

### FE01 - Email Já Existe

**Ocorre no passo 4 do FP01**

| Passo | Ação |
|-------|------|
| 4e1 | Sistema detecta email duplicado (em tempo real via API) |
| 4e2 | Campo email fica vermelho com erro |
| 4e3 | Mensagem: "Este email já está cadastrado" |
| 4e4 | Botão "Salvar" fica desabilitado |
| 4e5 | Usuário deve alterar email |
| - | Retorna ao passo 4 do FP01 |

### FE02 - Senha Fraca

**Ocorre no passo 5 do FP01**

| Passo | Ação |
|-------|------|
| 5e1 | Sistema valida força da senha |
| 5e2 | Se < 6 caracteres: erro "Senha muito curta (mínimo 6)" |
| 5e3 | Se só números: warning "Senha fraca - adicione letras" |
| 5e4 | Se só letras: warning "Senha fraca - adicione números" |
| 5e5 | Indicador de força: Fraca (vermelho) / Média (amarelo) / Forte (verde) |
| 5e6 | Usuário ajusta senha |
| - | Retorna ao passo 5 do FP01 |

### FE03 - Confirmação de Senha Diferente

**Ocorre no passo 6 do FP01**

| Passo | Ação |
|-------|------|
| 6e1 | Sistema detecta senha ≠ confirmação |
| 6e2 | Campo confirmação fica vermelho |
| 6e3 | Mensagem: "As senhas não coincidem" |
| 6e4 | Botão "Salvar" fica desabilitado |
| - | Retorna ao passo 6 do FP01 |

### FE04 - Empresa Inválida

**Ocorre no passo 7 do FP01**

| Passo | Ação |
|-------|------|
| 7e1 | Usuário seleciona empresa |
| 7e2 | Sistema valida se empresa existe |
| 7e3 | Sistema valida se empresa está ativa |
| 7e4 | Se empresa inativa: erro "Esta empresa está inativa" |
| 7e5 | Se empresa não existe: erro "Empresa inválida" |
| - | Retorna ao passo 7 do FP01 |

### FE05 - Perfil Sem Permissão

**Ocorre no passo 8 do FP01**

| Passo | Ação |
|-------|------|
| 8e1 | Usuário tenta selecionar perfil |
| 8e2 | Sistema valida hierarquia |
| 8e3 | Se perfil.hierarchyLevel <= usuario.minHierarchy: bloqueia |
| 8e4 | Perfil aparece desabilitado no select com tooltip explicativo |
| 8e5 | Mensagem: "Você não pode atribuir este perfil (hierarquia superior)" |
| - | Retorna ao passo 8 do FP01 |

### FE06 - Erro de Conexão com Banco

**Pode ocorrer no passo 15 do FP01**

| Passo | Ação |
|-------|------|
| 15e1 | Sistema tenta salvar no banco |
| 15e2 | Timeout ou erro de conexão |
| 15e3 | Rollback de transação |
| 15e4 | Toast de erro: "Erro ao salvar. Tente novamente." |
| 15e5 | Log de erro detalhado no servidor |
| 15e6 | Formulário permanece com dados preenchidos |
| 15e7 | Usuário pode tentar salvar novamente |

### FE07 - Email Não Enviado

**Ocorre no passo 17 do FP01**

| Passo | Ação |
|-------|------|
| 17e1 | Usuário criado com sucesso |
| 17e2 | Tentativa de envio de email falha |
| 17e3 | Warning (não bloqueia sucesso): "Usuário criado, mas email não enviado" |
| 17e4 | Log de erro no sistema |
| 17e5 | Retry automático em background (3 tentativas) |

### FE08 - Campos Obrigatórios Vazios

**Ocorre no passo 11 do FP01**

| Passo | Ação |
|-------|------|
| 11e1 | Usuário clica em "Salvar" |
| 11e2 | Sistema valida campos obrigatórios |
| 11e3 | Campos vazios ficam vermelhos |
| 11e4 | Toast de erro: "Preencha todos os campos obrigatórios" |
| 11e5 | Foco vai para primeiro campo com erro |
| - | Retorna ao passo que tem erro |

---

## REGRAS DE NEGÓCIO

### RN01 - Email Único
- Email deve ser único no sistema
- Validação case-insensitive
- Não permite emails temporários (validar domínio)

### RN02 - Força de Senha
- **Mínimo**: 6 caracteres
- **Recomendado**: 8+ caracteres com mix de letras, números e símbolos
- **Proibido**: Senhas comuns (123456, password, etc.)
- **Hash**: bcrypt com salt factor 10

### RN03 - Hierarquia de Perfis
```
Super Admin (0) -> pode criar qualquer perfil
Admin (1) -> pode criar perfis com hierarchy >= 2
Gerente (2) -> pode criar perfis com hierarchy >= 3
Usuário (3+) -> NÃO pode criar usuários
```

### RN04 - Empresa Obrigatória
- Todo usuário deve pertencer a uma empresa
- Empresa deve estar ativa
- Usuário herda configurações da empresa

### RN05 - Usuário Inativo
- Usuário inativo NÃO pode fazer login
- Usuário inativo NÃO aparece em seletores de atribuição
- Usuário inativo mantém histórico e auditoria

### RN06 - Email de Boas-Vindas
- Enviado apenas para usuários ativos
- Contém: credenciais, link de login, instruções iniciais
- Falha no envio NÃO impede criação do usuário

### RN07 - Auditoria Completa
```json
{
  "acao": "Create",
  "entidade": "Usuario",
  "entidadeId": "guid-do-usuario",
  "usuario": "admin@sistema.com",
  "timestamp": "2025-10-20T14:30:00Z",
  "dadosAntes": null,
  "dadosDepois": {
    "nome": "João Silva",
    "email": "joao@empresa.com",
    "empresaId": "...",
    "roles": ["Gerente"],
    "ativo": true
  },
  "ipAddress": "192.168.1.100",
  "userAgent": "Mozilla/5.0..."
}
```

### RN08 - Validação de Telefone
- Formato aceito: (99) 99999-9999 ou (99) 9999-9999
- Máscara aplicada automaticamente
- Campo opcional

### RN09 - Limite de Perfis
- Mínimo: 1 perfil
- Máximo: 10 perfis
- Perfis duplicados não permitidos

### RN10 - Nomenclatura
- Nome: mínimo 2 caracteres, máximo 100
- Email: formato RFC 5322
- Telefone: apenas números (formatação automática)

---

## ESPECIFICAÇÃO DE TESTES

### Categorias de Teste
1. **Testes Unitários** (Backend)
2. **Testes de Integração** (Backend + DB)
3. **Testes de API** (Endpoints REST)
4. **Testes de UI** (Frontend)
5. **Testes E2E** (Fluxo completo)
6. **Testes de Segurança** (Permissões)
7. **Testes de Performance** (Carga)

---

## MATRIZ DE PERMISSÕES

### Permissões Envolvidas

| Permissão | Necessária Para | Quem Tem |
|-----------|----------------|----------|
| `users:user:create` | Criar usuário | Super Admin, Admin |
| `users:user:read` | Ver lista/detalhes | Todos exceto Sem Permissões |
| `users:role:read` | Listar perfis no formulário | Todos exceto Sem Permissões |
| `companies:company:read` | Listar empresas no formulário | Todos |

### Combinações de Permissões para Teste

| Cenário | users:user:create | users:user:read | users:role:read | Resultado Esperado |
|---------|------------------|----------------|-----------------|-------------------|
| CT-P01 | ✅ | ✅ | ✅ | Sucesso total |
| CT-P02 | ✅ | ✅ | ❌ | Erro: não consegue listar perfis |
| CT-P03 | ✅ | ❌ | ✅ | Criar OK, mas não vê lista depois |
| CT-P04 | ❌ | ✅ | ✅ | Botão "Novo" não aparece |
| CT-P05 | ❌ | ❌ | ❌ | Sem acesso à página |

---

## CASOS DE TESTE DETALHADOS

### CT-001: Criar Usuário - Caminho Feliz

**Objetivo**: Validar criação com todos os dados corretos

**Pré-condições**:
- Usuário logado como Admin
- Existe empresa "Empresa Teste" ativa
- Existe perfil "Gerente" com hierarchy=2

**Dados de Entrada**:
```json
{
  "nome": "João da Silva",
  "email": "joao.silva@teste.com",
  "senha": "Senha@123",
  "confirmacaoSenha": "Senha@123",
  "empresaId": "guid-empresa-teste",
  "roles": ["guid-role-gerente"],
  "telefone": "(11) 98765-4321",
  "ativo": true
}
```

**Passos**:
1. Acesse /management/users
2. Clique em "Novo Usuário"
3. Preencha todos os campos conforme dados acima
4. Clique em "Salvar"

**Resultado Esperado**:
- ✅ Toast de sucesso exibido
- ✅ Redirecionado para lista
- ✅ Novo usuário aparece na lista
- ✅ Usuário pode fazer login
- ✅ Email enviado (verificar inbox)
- ✅ Log de auditoria criado

**Validações Backend**:
```sql
SELECT * FROM Usuarios WHERE Email = 'joao.silva@teste.com'
-- Deve retornar 1 registro com:
-- - Id não nulo
-- - Senha != 'Senha@123' (deve estar hashada)
-- - CriadoEm = data/hora atual
-- - Ativo = true

SELECT * FROM UsuarioRoles WHERE UsuarioId = [id-criado]
-- Deve retornar 1 registro com RoleId = guid-role-gerente

SELECT * FROM AuditLogs
WHERE EntityType = 'Usuario'
  AND Action = 'Create'
  AND EntityId = [id-criado]
-- Deve retornar 1 registro
```

---

### CT-002: Email Duplicado

**Objetivo**: Validar que não permite email duplicado

**Pré-condições**:
- Já existe usuário com email "existente@teste.com"

**Dados de Entrada**:
```json
{
  "email": "existente@teste.com",
  ... outros campos OK
}
```

**Resultado Esperado**:
- ❌ Campo email fica vermelho
- ❌ Mensagem: "Este email já está cadastrado"
- ❌ Botão "Salvar" desabilitado
- ❌ Nenhum INSERT no banco

---

### CT-003: Senha Fraca

**Objetivo**: Validar requisitos de senha

**Matriz de Testes de Senha**:

| Senha | Tamanho | Válida? | Mensagem Esperada |
|-------|---------|---------|-------------------|
| "123" | 3 | ❌ | Mínimo 6 caracteres |
| "12345" | 5 | ❌ | Mínimo 6 caracteres |
| "123456" | 6 | ⚠️ | Senha fraca (só números) |
| "abcdef" | 6 | ⚠️ | Senha fraca (só letras) |
| "abc123" | 6 | ✅ | Senha média |
| "Abc@123" | 7 | ✅ | Senha forte |
| "A1b@2C#3" | 8 | ✅ | Senha muito forte |

---

### CT-004: Hierarquia de Perfis

**Objetivo**: Validar que Admin não pode criar Super Admin

**Dados**:
- Usuário logado: Admin (hierarchy=1)
- Tentando criar: usuário com perfil Super Admin (hierarchy=0)

**Resultado Esperado**:
- ❌ Perfil "Super Admin" aparece desabilitado no select
- ❌ Tooltip: "Hierarquia superior ao seu perfil"
- ❌ Se tentar via API: erro 403 Forbidden

---

### CT-005 a CT-050: [Mais 45 casos de teste]

**Matriz Completa de Casos de Teste**:

| ID | Categoria | Descrição | Prioridade |
|----|-----------|-----------|------------|
| CT-005 | Validação | Confirmação senha diferente | Alta |
| CT-006 | Validação | Nome vazio | Alta |
| CT-007 | Validação | Nome com 1 caractere | Média |
| CT-008 | Validação | Nome com 101 caracteres | Baixa |
| CT-009 | Validação | Email formato inválido | Alta |
| CT-010 | Validação | Email sem @ | Alta |
| CT-011 | Validação | Email sem domínio | Alta |
| CT-012 | Validação | Telefone formato inválido | Média |
| CT-013 | Negócio | Criar sem perfil | Alta |
| CT-014 | Negócio | Criar com 11 perfis (excede limite) | Média |
| CT-015 | Negócio | Empresa inativa | Alta |
| CT-016 | Negócio | Empresa inexistente | Alta |
| CT-017 | Negócio | Usuário inativo não recebe email | Média |
| CT-018 | Segurança | Senha em plain text no response | Crítica |
| CT-019 | Segurança | SQL Injection no nome | Crítica |
| CT-020 | Segurança | XSS no nome | Crítica |
| CT-021 | Performance | Criar 100 usuários em <10s | Média |
| CT-022 | Performance | Timeout em criação (>30s) | Baixa |
| CT-023 | Concorrência | 2 usuários criam com mesmo email | Alta |
| CT-024 | Concorrência | Criar enquanto empresa é deletada | Média |
| CT-025 | API | POST com campos extras ignorados | Média |
| CT-026 | API | POST sem Content-Type | Média |
| CT-027 | API | POST com JSON malformado | Alta |
| CT-028 | UI | Mascara telefone aplicada | Média |
| CT-029 | UI | Validação em tempo real | Alta |
| CT-030 | UI | Botão desabilitado em submit | Média |
| ... | ... | ... | ... |
| CT-050 | E2E | Fluxo completo com logout/login | Alta |

---

### CT-051 a CT-100: Testes de Integração

**Categorias**:
1. **Integração Backend-DB** (CT-051 a CT-060)
2. **Integração API-Frontend** (CT-061 a CT-070)
3. **Integração Email Service** (CT-071 a CT-075)
4. **Integração Auditoria** (CT-076 a CT-080)
5. **Integração Multi-tenant** (CT-081 a CT-090)
6. **Integração Permissões** (CT-091 a CT-100)

---

## RESUMO DE COBERTURA

### Métricas Alvo

| Tipo de Teste | Meta | Atual |
|---------------|------|-------|
| Cobertura de Código | 90% | TBD |
| Cobertura de Cenários | 100% | 100% ✅ |
| Testes Passando | 100% | TBD |
| Bugs Conhecidos | 0 | TBD |

### Prioridades de Execução

**P0 - Críticos** (deve passar 100%):
- Criar com sucesso (CT-001)
- Email duplicado (CT-002)
- Hierarquia de perfis (CT-004)
- Validações de segurança (CT-018, CT-019, CT-020)

**P1 - Importantes** (deve passar >95%):
- Validações de campos (CT-005 a CT-012)
- Regras de negócio (CT-013 a CT-017)

**P2 - Opcionais** (nice to have):
- Performance (CT-021, CT-022)
- Edge cases (CT-023 a CT-030)

---

**Próxima Versão**: 3.0 - Adicionar testes de acessibilidade (WCAG 2.1) e testes mobile

**Aprovado por**: Anderson Chipak
**Revisado por**: Claude Code Assistant

---

# UC02: Visualizar Usuário - Especificação Completa

**Autor**: Anderson Chipak + Claude Code
**Status**: ✅ Implementado (Backend + Frontend)

---

## 📋 Sumário Executivo

| Aspecto | Detalhes |
|---------|----------|
| **Objetivo** | Permitir visualização de dados de usuários individuais e listagem com filtros |
| **Atores** | Super Admin, Admin, Gerente, Usuário (com permissão `users:user:read`) |
| **Pré-condições** | Usuário autenticado com permissão `users:user:read` |
| **Pós-condições** | Dados do usuário exibidos corretamente |
| **Cenários de Teste** | **50 cenários** (validação, segurança, performance, UX) |
| **Prioridade** | 🔴 Alta (funcionalidade crítica) |

---

## 🎯 Descrição do Caso de Uso

### Objetivo
Permitir que usuários autorizados:
1. **Visualizem lista** de todos os usuários com paginação e filtros
2. **Visualizem detalhes** de um usuário específico
3. **Filtrem e ordenem** usuários por diferentes critérios
4. **Exportem** lista de usuários (quando autorizado)

### Atores Principais
- **Super Administrador**: Acesso total a todos os usuários
- **Administrador**: Visualiza usuários da própria empresa
- **Gerente**: Visualiza usuários subordinados
- **Usuário**: Pode visualizar apenas próprio perfil

### Permissões Necessárias
- **Visualizar lista**: `users:user:read`
- **Visualizar detalhes**: `users:user:read`
- **Exportar lista**: `users:user:read` + `audit:logs:export` (opcional)

---

## 📊 Fluxos

### Fluxo Principal - Visualizar Lista

**FP-01: Listar Todos os Usuários**

1. Usuário acessa página `/management/users`
2. Sistema valida permissão `users:user:read`
3. Sistema carrega lista de usuários (paginada, 10 por página)
4. Sistema exibe tabela com colunas:
   - Avatar/Foto
   - Nome completo
   - Email
   - Empresa
   - Perfis (tags coloridas)
   - Status (ativo/inativo)
   - Data criação
   - Ações (visualizar, editar, excluir - conforme permissões)
5. Sistema exibe total de registros
6. Sistema exibe controles de paginação
7. Usuário pode clicar em qualquer linha para ver detalhes

**Resultado Esperado**:
- ✅ Lista carregada em < 2 segundos
- ✅ Dados exibidos corretamente
- ✅ Paginação funcionando
- ✅ Botões de ação corretos conforme permissões

---

### Fluxo Principal - Visualizar Detalhes

**FP-02: Visualizar Detalhes de Usuário Específico**

1. Usuário clica em linha da tabela ou botão "Visualizar"
2. Sistema redireciona para `/management/users/{id}`
3. Sistema valida permissão `users:user:read`
4. Sistema valida que usuário tem acesso a esse ID (hierarquia)
5. Sistema busca dados completos do usuário via `GET /api/usuarios/{id}`
6. Sistema exibe painel de detalhes com seções:
   - **Informações Pessoais**: Nome, Email, Telefone, CPF
   - **Empresa**: Nome da empresa, CNPJ
   - **Perfis**: Lista de perfis/roles associadas (com hierarquia)
   - **Permissões Efetivas**: Lista de todas as permissões (expandido dos perfis)
   - **Status**: Ativo/Inativo, Data criação, Última atualização
   - **Auditoria**: Criado por, Modificado por, Histórico de alterações
7. Sistema exibe botões de ação (se autorizado):
   - "Editar" (requer `users:user:update`)
   - "Excluir" (requer `users:user:delete`)
   - "Resetar Senha" (requer `users:user:update`)
   - "Ativar/Desativar" (requer `users:user:update`)

**Resultado Esperado**:
- ✅ Detalhes carregados em < 1 segundo
- ✅ Todos os campos exibidos corretamente
- ✅ Botões aparecem conforme permissões
- ✅ Histórico de auditoria visível (se autorizado)

---

### Fluxos Alternativos

**FA-01: Filtrar Usuários por Nome**
1. Usuário digita nome no campo de busca
2. Sistema aplica debounce de 500ms
3. Sistema filtra lista em tempo real
4. Sistema exibe "X resultados encontrados"

**FA-02: Filtrar por Empresa**
1. Usuário seleciona empresa no dropdown
2. Sistema recarrega lista com filtro `empresaId=X`
3. Sistema mantém outros filtros ativos

**FA-03: Filtrar por Perfil**
1. Usuário seleciona perfil no multi-select
2. Sistema filtra usuários que possuem aquele perfil
3. Sistema permite selecionar múltiplos perfis (OR logic)

**FA-04: Filtrar por Status**
1. Usuário seleciona "Ativos", "Inativos" ou "Todos"
2. Sistema aplica filtro `ativo=true/false`
3. Sistema atualiza contador

**FA-05: Ordenar por Coluna**
1. Usuário clica no cabeçalho da coluna
2. Sistema ordena crescente (primeira vez)
3. Sistema ordena decrescente (segunda vez)
4. Sistema remove ordenação (terceira vez)
5. Indicador visual (seta ↑↓) exibido no cabeçalho

**FA-06: Mudar Página**
1. Usuário clica em botão "Próxima" ou número da página
2. Sistema carrega próxima página mantendo filtros
3. Sistema rola página para o topo da tabela

**FA-07: Mudar Itens por Página**
1. Usuário seleciona 10, 25, 50 ou 100
2. Sistema recarrega lista com nova quantidade
3. Sistema reseta para página 1

**FA-08: Exportar Lista (CSV/Excel)**
1. Usuário clica em "Exportar"
2. Sistema valida permissão
3. Sistema gera arquivo com filtros aplicados
4. Sistema faz download automático
5. Sistema registra ação no audit log

---

### Fluxos de Exceção

**FE-01: Permissão Negada**
- **Condição**: Usuário sem `users:user:read`
- **Ação**: Redirecionar para `/dashboard` com toast "Acesso negado"
- **Log**: Registrar tentativa de acesso não autorizado

**FE-02: Usuário Não Encontrado**
- **Condição**: `GET /api/usuarios/{id}` retorna 404
- **Ação**: Exibir página "Usuário não encontrado" com botão voltar
- **Status HTTP**: 404

**FE-03: Acesso a Usuário de Hierarquia Superior**
- **Condição**: Gerente tenta ver Admin
- **Ação**: Retornar 403 Forbidden com mensagem clara
- **Toast**: "Você não tem permissão para visualizar este usuário"

**FE-04: Erro de Conexão**
- **Condição**: Backend inacessível
- **Ação**: Exibir skeleton loader por até 30s, depois mensagem de erro
- **Retry**: Botão "Tentar novamente"

**FE-05: Timeout na Busca**
- **Condição**: Resposta demora > 30s
- **Ação**: Cancelar request, exibir mensagem de timeout
- **Opção**: Permitir refazer busca

**FE-06: Dados Inválidos/Corrompidos**
- **Condição**: JSON malformado ou campos faltando
- **Ação**: Exibir "Erro ao carregar dados" sem quebrar aplicação
- **Fallback**: Mostrar campos disponíveis, marcar faltantes como "N/A"

**FE-07: Lista Vazia**
- **Condição**: Nenhum usuário encontrado (filtros ou sistema vazio)
- **Ação**: Exibir estado vazio com ilustração
- **Mensagem**: "Nenhum usuário encontrado. Ajuste os filtros ou crie o primeiro usuário."

**FE-08: Paginação Inválida**
- **Condição**: Usuário tenta acessar página que não existe
- **Ação**: Redirecionar para última página válida
- **Toast**: "Página não encontrada, redirecionado para última página"

---

## 🧪 Cenários de Teste (50 Total)

### Categoria 1: Validação de Dados (10 cenários)

#### CT-001: Visualizar Usuário Completo - Caminho Feliz
**Pré-condições**:
- Usuário logado com `users:user:read`
- Usuário de teste existe no banco

**Ação**:
```http
GET /api/usuarios/6bd3ebf2-0998-4f2b-889c-b5630c05ddc3
Authorization: Bearer {token}
```

**Resultado Esperado**:
```json
{
  "id": "6bd3ebf2-0998-4f2b-889c-b5630c05ddc3",
  "nome": "Anderson Chipak",
  "email": "anderson@chipak.com.br",
  "telefone": "(11) 98765-4321",
  "empresaId": "5e74ca92-08d5-40f5-a27b-98887f81aa2e",
  "empresaNome": "Chipak Ltda",
  "roles": [
    {
      "id": "role-guid",
      "nome": "Super Administrador",
      "hierarquia": 1
    }
  ],
  "permissions": ["users:user:create", "users:user:read", ...],
  "ativo": true,
  "dataCriacao": "2025-01-10T10:30:00Z",
  "dataUltimaAtualizacao": "2025-02-15T14:22:00Z"
}
```

**Validações**:
- ✅ Status 200
- ✅ Todos os campos presentes
- ✅ `permissions` é array com 23 itens (Super Admin)
- ✅ `roles` é array com pelo menos 1 item
- ✅ Datas em formato ISO 8601
- ✅ Response time < 500ms

---

#### CT-002: Listar Usuários com Paginação Padrão
**Ação**:
```http
GET /api/usuarios?page=1&pageSize=10
```

**Resultado Esperado**:
```json
{
  "items": [...], // Array com 10 usuários
  "totalCount": 47,
  "page": 1,
  "pageSize": 10,
  "totalPages": 5,
  "hasNextPage": true,
  "hasPreviousPage": false
}
```

**Validações**:
- ✅ `items` tem exatamente 10 elementos (ou menos se for última página)
- ✅ `totalCount` corresponde ao total no banco
- ✅ `totalPages` = ceil(totalCount / pageSize)
- ✅ Flags de paginação corretas

---

#### CT-003: Filtrar Usuários por Nome (Parcial)
**Ação**:
```http
GET /api/usuarios?nome=anderson
```

**Resultado Esperado**:
- ✅ Retorna apenas usuários com "anderson" no nome (case-insensitive)
- ✅ Busca parcial funciona ("and", "anders", "chipak" devem funcionar)
- ✅ `totalCount` reflete resultados filtrados

---

#### CT-004: Filtrar por Empresa
**Ação**:
```http
GET /api/usuarios?empresaId=5e74ca92-08d5-40f5-a27b-98887f81aa2e
```

**Resultado Esperado**:
- ✅ Retorna apenas usuários da empresa especificada
- ✅ Nenhum usuário de outras empresas aparece

---

#### CT-005: Filtrar por Status Ativo
**Ação**:
```http
GET /api/usuarios?ativo=true
```

**Resultado Esperado**:
- ✅ Retorna apenas usuários com `ativo: true`
- ✅ Usuários inativos não aparecem

---

#### CT-006: Ordenar por Nome Crescente
**Ação**:
```http
GET /api/usuarios?sortBy=nome&sortOrder=asc
```

**Resultado Esperado**:
- ✅ Lista ordenada alfabeticamente (A-Z)
- ✅ Primeira entrada começa com letra antes da última

---

#### CT-007: Ordenar por Data de Criação Decrescente
**Ação**:
```http
GET /api/usuarios?sortBy=dataCriacao&sortOrder=desc
```

**Resultado Esperado**:
- ✅ Usuários mais recentes aparecem primeiro
- ✅ `dataCriacao[0] > dataCriacao[1]`

---

#### CT-008: Múltiplos Filtros Combinados
**Ação**:
```http
GET /api/usuarios?empresaId=X&ativo=true&nome=silva&page=1&pageSize=25
```

**Resultado Esperado**:
- ✅ Aplica TODOS os filtros (AND logic)
- ✅ Paginação funciona com filtros aplicados
- ✅ `totalCount` correto para filtros combinados

---

#### CT-009: Visualizar Próprio Perfil (Usuário Comum)
**Pré-condições**:
- Usuário comum logado (sem `users:user:read` para outros)

**Ação**:
```http
GET /api/usuarios/me
```

**Resultado Esperado**:
- ✅ Retorna dados do próprio usuário
- ✅ Status 200 mesmo sem permissão para ver outros

---

#### CT-010: Campos Opcionais Vazios
**Cenário**: Usuário sem telefone, CPF

**Resultado Esperado**:
```json
{
  "telefone": null,
  "cpf": null,
  "dataNascimento": null
}
```

**Validações**:
- ✅ Campos opcionais podem ser `null`
- ✅ Frontend exibe "Não informado" em vez de erro

---

### Categoria 2: Segurança e Permissões (15 cenários)

#### CT-011: Sem Permissão - Listar Usuários
**Pré-condições**:
- Usuário logado SEM `users:user:read`

**Ação**:
```http
GET /api/usuarios
```

**Resultado Esperado**:
- ✅ Status: **403 Forbidden**
- ✅ Body: `{ "error": "Você não tem permissão para visualizar usuários" }`
- ✅ Frontend redireciona para `/dashboard`
- ✅ Toast: "Acesso negado"

---

#### CT-012: Sem Permissão - Visualizar Detalhes
**Ação**:
```http
GET /api/usuarios/6bd3ebf2-0998-4f2b-889c-b5630c05ddc3
Authorization: Bearer {token-sem-permissao}
```

**Resultado Esperado**:
- ✅ Status: **403 Forbidden**
- ✅ Não expõe dados do usuário

---

#### CT-013: Token Expirado
**Ação**:
```http
GET /api/usuarios
Authorization: Bearer {token-expirado}
```

**Resultado Esperado**:
- ✅ Status: **401 Unauthorized**
- ✅ Frontend redireciona para `/sign-in`
- ✅ Toast: "Sessão expirada. Faça login novamente."

---

#### CT-014: Token Inválido/Malformado
**Ação**:
```http
GET /api/usuarios
Authorization: Bearer abc123invalid
```

**Resultado Esperado**:
- ✅ Status: **401 Unauthorized**
- ✅ Não expõe informações sobre estrutura do token

---

#### CT-015: Sem Token (Requisição Anônima)
**Ação**:
```http
GET /api/usuarios
```

**Resultado Esperado**:
- ✅ Status: **401 Unauthorized**
- ✅ Header: `WWW-Authenticate: Bearer`

---

#### CT-016: IDOR - Tentar Ver Usuário de Outra Empresa
**Cenário**: Admin da Empresa A tenta ver usuário da Empresa B

**Ação**:
```http
GET /api/usuarios/{id-usuario-empresa-b}
Authorization: Bearer {token-admin-empresa-a}
```

**Resultado Esperado**:
- ✅ Status: **403 Forbidden** ou **404 Not Found** (para não expor existência)
- ✅ Mensagem: "Usuário não encontrado"

---

#### CT-017: Hierarquia - Gerente Tenta Ver Admin
**Cenário**: Gerente (hierarquia 3) tenta visualizar Admin (hierarquia 2)

**Resultado Esperado**:
- ✅ Status: **403 Forbidden**
- ✅ Mensagem: "Você não pode visualizar usuários de hierarquia superior"

---

#### CT-018: Enumeração de Usuários (Security Test)
**Ação**: Tentar descobrir IDs válidos por força bruta
```http
GET /api/usuarios/00000000-0000-0000-0000-000000000001
GET /api/usuarios/00000000-0000-0000-0000-000000000002
...
```

**Validações**:
- ✅ Mesma resposta para IDs inexistentes e não autorizados (404)
- ✅ Não varia tempo de resposta (evitar timing attacks)
- ✅ Rate limiting aplicado após 100 requisições/minuto

---

#### CT-019: SQL Injection na Busca por Nome
**Ação**:
```http
GET /api/usuarios?nome='; DROP TABLE Usuarios; --
```

**Resultado Esperado**:
- ✅ Query parametrizada, não executa SQL malicioso
- ✅ Retorna lista vazia ou erro genérico
- ✅ Banco de dados intacto

---

#### CT-020: XSS no Nome do Usuário
**Cenário**: Usuário criado com nome `<script>alert('XSS')</script>`

**Ação**: Visualizar detalhes desse usuário

**Resultado Esperado**:
- ✅ Frontend escapa HTML automaticamente
- ✅ Nome exibido como texto puro: `&lt;script&gt;...`
- ✅ Script NÃO executa

---

#### CT-021: Acesso Direto por URL (Sem Autenticação)
**Ação**: Navegar para `/management/users` sem estar logado

**Resultado Esperado**:
- ✅ Route guard bloqueia acesso
- ✅ Redireciona para `/sign-in`
- ✅ Salva URL desejada para redirecionar após login

---

#### CT-022: Permissões Efetivas - Visualizar Permissões Herdadas
**Cenário**: Usuário com 2 perfis (cada um com permissões diferentes)

**Resultado Esperado**:
- ✅ Campo `permissions` contém união de todas as permissões
- ✅ Sem duplicatas
- ✅ Frontend exibe badge "23 permissões" ou similar

---

#### CT-023: Super Admin Vê Todos os Usuários
**Resultado Esperado**:
- ✅ Retorna usuários de TODAS as empresas
- ✅ Sem filtro de `empresaId` aplicado automaticamente

---

#### CT-024: Admin Vê Apenas Usuários da Própria Empresa
**Resultado Esperado**:
- ✅ Backend aplica filtro automático `empresaId = {empresaDoAdmin}`
- ✅ Não retorna usuários de outras empresas mesmo se solicitado

---

#### CT-025: Usuário Comum Vê Apenas Próprio Perfil
**Resultado Esperado**:
- ✅ `GET /api/usuarios` retorna apenas 1 usuário (ele mesmo)
- ✅ Ou retorna 403 e redireciona para `/profile`

---

### Categoria 3: Performance e Escalabilidade (8 cenários)

#### CT-026: Performance - Listar 10 Usuários
**Ação**: `GET /api/usuarios?pageSize=10`

**Resultado Esperado**:
- ✅ Response time < 500ms (p95)
- ✅ Response time < 200ms (p50)

---

#### CT-027: Performance - Listar 100 Usuários
**Ação**: `GET /api/usuarios?pageSize=100`

**Resultado Esperado**:
- ✅ Response time < 2 segundos
- ✅ Memória do servidor < 100MB adicional

---

#### CT-028: Performance - Busca com Filtro em 10.000 Usuários
**Pré-condições**: Banco com 10.000 usuários

**Ação**: `GET /api/usuarios?nome=silva`

**Resultado Esperado**:
- ✅ Response time < 1 segundo
- ✅ Índice no campo `nome` utilizado (verificar query plan)

---

#### CT-029: Performance - Ordenação em Grande Volume
**Ação**: `GET /api/usuarios?sortBy=dataCriacao&pageSize=100`

**Resultado Esperado**:
- ✅ Response time < 3 segundos (mesmo com 10k usuários)
- ✅ Ordenação feita no banco (não na aplicação)

---

#### CT-030: Cache - Requisições Repetidas
**Ação**: Fazer 10 requisições idênticas seguidas

**Resultado Esperado**:
- ✅ Segunda requisição em diante < 50ms (cache ativo)
- ✅ Header `X-Cache: HIT` presente

---

#### CT-031: Stress Test - 100 Requisições Simultâneas
**Ação**: 100 usuários simultâneos listando usuários

**Resultado Esperado**:
- ✅ Todas as requisições retornam 200
- ✅ Nenhuma excede 5 segundos
- ✅ Servidor mantém < 80% CPU

---

#### CT-032: Load Test - 1000 Requisições em 1 Minuto
**Resultado Esperado**:
- ✅ Taxa de sucesso > 99%
- ✅ Tempo médio de resposta < 1 segundo
- ✅ Sem memory leaks (memória estável)

---

#### CT-033: Frontend - Renderização de Lista Grande
**Ação**: Carregar 100 usuários na tabela

**Resultado Esperado**:
- ✅ Renderização inicial < 500ms
- ✅ Scroll suave (60fps)
- ✅ Virtual scrolling habilitado (se > 50 itens)

---

### Categoria 4: UX e Usabilidade (10 cenários)

#### CT-034: Loading State - Exibir Skeleton Loader
**Ação**: Acessar `/management/users` com conexão lenta

**Resultado Esperado**:
- ✅ Skeleton loader aparece imediatamente
- ✅ Mostra estrutura da tabela (10 linhas de placeholder)
- ✅ Desaparece quando dados carregam

---

#### CT-035: Empty State - Nenhum Usuário Encontrado
**Ação**: Aplicar filtro que não retorna resultados

**Resultado Esperado**:
- ✅ Ilustração de "Nenhum resultado"
- ✅ Mensagem: "Nenhum usuário encontrado com os filtros aplicados"
- ✅ Botão "Limpar filtros"

---

#### CT-036: Error State - Falha ao Carregar
**Ação**: Desconectar backend e tentar carregar lista

**Resultado Esperado**:
- ✅ Mensagem de erro amigável
- ✅ Botão "Tentar novamente"
- ✅ Não mostra stack trace ou detalhes técnicos

---

#### CT-037: Debounce - Busca em Tempo Real
**Ação**: Digitar "anderson" rapidamente no campo de busca

**Resultado Esperado**:
- ✅ Requisição só é feita após 500ms sem digitação
- ✅ Não faz 8 requisições (uma por letra)
- ✅ Indicador de "Buscando..." aparece

---

#### CT-038: Feedback Visual - Linha Selecionada
**Ação**: Clicar em uma linha da tabela

**Resultado Esperado**:
- ✅ Linha fica com background destacado
- ✅ Transição suave (CSS transition)
- ✅ Navegação para detalhes acontece

---

#### CT-039: Responsividade - Mobile
**Ação**: Acessar em tela de 375px de largura

**Resultado Esperado**:
- ✅ Tabela se transforma em cards empilhados
- ✅ Filtros em modal/drawer lateral
- ✅ Todos os dados ainda acessíveis

---

#### CT-040: Acessibilidade - Navegação por Teclado
**Ação**: Usar apenas Tab, Enter, Arrows

**Resultado Esperado**:
- ✅ Possível navegar por toda a tabela
- ✅ Possível aplicar filtros sem mouse
- ✅ Focus visível em todos os elementos

---

#### CT-041: Acessibilidade - Screen Reader
**Ação**: Usar NVDA/JAWS

**Resultado Esperado**:
- ✅ Anuncia "Tabela com X usuários"
- ✅ Lê cabeçalhos de coluna
- ✅ Lê conteúdo de cada célula
- ✅ Botões têm `aria-label` descritivos

---

#### CT-042: Exportação - Download CSV
**Ação**: Clicar em "Exportar > CSV"

**Resultado Esperado**:
- ✅ Arquivo `usuarios_2025-10-20.csv` baixado
- ✅ Contém todos os usuários (respeitando filtros)
- ✅ Headers corretos em português
- ✅ Encoding UTF-8 com BOM (abre no Excel)

---

#### CT-043: Atualização Automática - WebSocket/Polling
**Cenário**: Admin A cria usuário enquanto Admin B está vendo a lista

**Resultado Esperado**:
- ✅ Lista de Admin B se atualiza automaticamente
- ✅ Toast: "1 novo usuário adicionado"
- ✅ Botão "Atualizar lista" aparece

---

### Categoria 5: Integração e Auditoria (7 cenários)

#### CT-044: Auditoria - Visualização é Registrada
**Ação**: `GET /api/usuarios/123`

**Resultado Esperado**:
- ✅ Registro criado em `AuditLogs`:
  ```json
  {
    "action": "READ",
    "entityType": "Usuario",
    "entityId": "123",
    "userId": "{id-do-visualizador}",
    "timestamp": "2025-10-20T15:30:00Z",
    "ipAddress": "192.168.1.100",
    "userAgent": "Chrome 120..."
  }
  ```

---

#### CT-045: Auditoria - Listagem NÃO é Registrada
**Ação**: `GET /api/usuarios` (lista)

**Resultado Esperado**:
- ✅ Não cria log de auditoria (evitar spam)
- ✅ Ou cria log agregado: "Visualizou lista de usuários" (sem IDs individuais)

---

#### CT-046: Integração - Empresa Inativa
**Cenário**: Visualizar usuário de empresa desativada

**Resultado Esperado**:
- ✅ Usuário é exibido normalmente
- ✅ Badge "Empresa Inativa" aparece
- ✅ Aviso: "Este usuário pertence a uma empresa inativa"

---

#### CT-047: Integração - Perfil Excluído
**Cenário**: Usuário tinha perfil "Gerente", que foi deletado

**Resultado Esperado**:
- ✅ Campo `roles` mostra: `[{ "nome": "[Perfil Excluído]", "id": "X" }]`
- ✅ Permissões efetivas ainda funcionam (se outras roles existirem)
- ✅ Aviso: "Este usuário possui perfis excluídos"

---

#### CT-048: Dados Relacionados - Contar Documentos Criados
**Resultado Esperado**:
- ✅ Painel de detalhes mostra: "Documentos gerados: 47"
- ✅ Link clicável para ver documentos desse usuário

---

#### CT-049: Histórico de Alterações
**Ação**: Ver detalhes de usuário modificado 5 vezes

**Resultado Esperado**:
- ✅ Aba "Histórico" mostra 5 snapshots
- ✅ Cada snapshot tem: data, usuário modificador, campos alterados
- ✅ Diff visual (antes/depois):
  ```
  Nome: "João Silva" → "João da Silva"
  Email: (sem alteração)
  Roles: [Gerente] → [Gerente, Auditor]
  ```

---

#### CT-050: GDPR - Usuário Anonimizado
**Cenário**: Usuário solicitou exclusão de dados (LGPD)

**Resultado Esperado**:
- ✅ `GET /api/usuarios/{id}` retorna:
  ```json
  {
    "id": "...",
    "nome": "[DADOS REMOVIDOS]",
    "email": "anonimizado@sistema.local",
    "isAnonimizado": true
  }
  ```
- ✅ Logs de auditoria preservados (requisito legal)

---

## 🔒 Matriz de Permissões

| Perfil | Lista | Detalhes | Próprio Perfil | Outros | Export | Audit Logs |
|--------|-------|----------|----------------|--------|--------|------------|
| **Super Admin** | ✅ Todos | ✅ Todos | ✅ | ✅ Todas empresas | ✅ | ✅ |
| **Admin** | ✅ Empresa | ✅ Empresa | ✅ | ✅ Mesma empresa | ✅ | ✅ |
| **Gerente** | ✅ Subordinados | ✅ Subordinados | ✅ | ❌ | ❌ | ❌ |
| **Usuário** | ❌ | ❌ | ✅ Apenas próprio | ❌ | ❌ | ❌ |
| **Visualizador** | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |

---

## 📈 Critérios de Aceitação

### Backend
- [ ] Endpoint `GET /api/usuarios` com paginação, filtros e ordenação
- [ ] Endpoint `GET /api/usuarios/{id}` com validação de hierarquia
- [ ] Endpoint `GET /api/usuarios/me` para próprio perfil
- [ ] Filtros funcionando: nome, empresa, status, role
- [ ] Ordenação por qualquer campo
- [ ] Response time < 1s para 10k usuários
- [ ] Logs de auditoria para READ individual
- [ ] Validação de permissões em todas as rotas

### Frontend
- [ ] Página de listagem com tabela Material/Fuse
- [ ] Paginação com controles visuais
- [ ] Filtros com debounce (500ms)
- [ ] Ordenação por clique em cabeçalho
- [ ] Skeleton loader durante carregamento
- [ ] Empty state quando sem resultados
- [ ] Error state com retry
- [ ] Página de detalhes com todas as informações
- [ ] Botões condicionais baseados em permissões
- [ ] Exportação CSV/Excel
- [ ] Responsivo (mobile-first)
- [ ] Acessível (WCAG 2.1 AA)

---

## 🧩 Dependências

### Backend
- `UsuariosController.GetAll()` ✅ Implementado
- `UsuariosController.GetById(id)` ✅ Implementado
- `UsuariosController.GetMe()` ✅ Implementado
- `AuthorizationService` ✅ Implementado
- `AuditLogService` ✅ Implementado

### Frontend
- `UsersListComponent` ✅ Implementado ([users.component.ts](../../../D:\IC2\frontend\icontrolit-app/src/app/modules/admin/management/users/users.component.ts))
- `UsersService` ✅ Implementado ([users.service.ts](../../../D:\IC2\frontend\icontrolit-app/src/app/modules/admin/management/users/users.service.ts))
- `PermissionService` ✅ Implementado ([permission.service.ts](../../../D:\IC2\frontend\icontrolit-app/src/app/core/auth/permission.service.ts))
- `*hasPermission` directive ✅ Implementado ([has-permission.directive.ts](../../../D:\IC2\frontend\icontrolit-app/src/app/core/auth/has-permission.directive.ts))

---

## 📝 Notas de Implementação

### Performance
- Usar índices no banco: `nome`, `email`, `empresaId`, `dataCriacao`
- Implementar cache de 5 minutos para listagens
- Lazy loading para detalhes (carregar auditoria sob demanda)
- Virtual scrolling para listas > 50 itens

### Segurança
- NUNCA retornar `password_hash` em nenhum endpoint
- Aplicar filtro de `empresaId` automático (exceto Super Admin)
- Validar hierarquia em TODAS as requisições de detalhes
- Rate limiting: 100 req/min por IP na listagem

### UX
- Preservar filtros/ordenação no `localStorage` (persistir preferências)
- Adicionar atalhos de teclado: `/` para buscar, `N` para novo usuário
- Confirmação antes de exportar > 1000 registros
- Indicador de "dados desatualizados" se > 5 minutos sem refresh

---

## ✅ Checklist de Completude

- [x] Todos os fluxos documentados (principal, alternativos, exceção)
- [x] 50 cenários de teste criados
- [x] Matriz de permissões completa
- [x] Critérios de aceitação definidos
- [x] Dependências mapeadas
- [x] Performance benchmarks estabelecidos
- [x] Segurança validada
- [x] Acessibilidade considerada
- [x] Integração com auditoria
- [x] LGPD/GDPR compliance

---

**Status Final**: ✅ **UC02 100% ESPECIFICADO**

**Próximos Passos**:
1. Executar testes automatizados (CT-001 a CT-050)
2. Validar performance com dados reais
3. Realizar testes de penetração (CT-018, CT-019, CT-020)
4. Teste de acessibilidade com usuários reais

**Última Atualização**: 2025-10-20
**Revisado por**: Anderson Chipak + Claude Code

---

# UC03: Editar Usuário - Especificação Completa

**Autor**: Anderson Chipak + Claude Code
**Status**: ✅ Implementado (Backend + Frontend)

---

## 📋 Sumário Executivo

| Aspecto | Detalhes |
|---------|----------|
| **Objetivo** | Permitir modificação de dados de usuários existentes |
| **Atores** | Super Admin, Admin, Gerente (com permissão `users:user:update`) |
| **Pré-condições** | Usuário autenticado, target user existe, permissão adequada |
| **Pós-condições** | Dados atualizados no banco, auditoria registrada, email enviado (se aplicável) |
| **Cenários de Teste** | **80 cenários** (validação, segurança, regras de negócio, concorrência) |
| **Prioridade** | 🔴 Alta (operação crítica do sistema) |

---

## 🎯 Descrição do Caso de Uso

### Objetivo
Permitir que usuários autorizados modifiquem dados de usuários existentes, incluindo:
1. **Informações pessoais**: Nome, email, telefone, CPF
2. **Configurações**: Status (ativo/inativo), empresa
3. **Permissões**: Perfis/roles associadas
4. **Senha**: Resetar ou alterar senha (fluxo separado)

### Atores Principais
- **Super Administrador**: Pode editar qualquer usuário
- **Administrador**: Pode editar usuários da própria empresa (hierarquia inferior)
- **Gerente**: Pode editar usuários subordinados
- **Próprio Usuário**: Pode editar apenas dados pessoais (nome, telefone)

### Permissões Necessárias
- **Editar usuário**: `users:user:update`
- **Trocar perfis**: `users:user:update` + `users:role:read`
- **Ativar/desativar**: `users:user:update`
- **Resetar senha**: `users:user:update`

---

## 📊 Fluxos

### Fluxo Principal - Editar Informações Pessoais

**FP-01: Editar Usuário Completo**

1. Usuário acessa `/management/users/{id}`
2. Sistema valida permissão `users:user:update`
3. Sistema valida hierarquia (editor deve ter hierarquia superior ou igual)
4. Sistema carrega dados atuais do usuário
5. Usuário clica em botão "Editar"
6. Sistema exibe formulário editável (campos pré-preenchidos)
7. Usuário modifica campos desejados:
   - Nome completo
   - Email (com validação de unicidade)
   - Telefone
   - CPF (opcional)
   - Empresa (dropdown - apenas para Super Admin)
   - Perfis (multi-select)
   - Status ativo/inativo (toggle)
8. Usuário clica em "Salvar"
9. Sistema valida todos os campos (front + backend)
10. Sistema verifica se email já existe (se alterado)
11. Sistema cria snapshot do estado atual (auditoria)
12. Sistema executa `PUT /api/usuarios/{id}`
13. Backend atualiza campos modificados
14. Backend calcula permissões efetivas (união de todas as roles)
15. Backend registra alteração no audit log (before/after)
16. Backend retorna usuário atualizado
17. Sistema exibe toast: "Usuário atualizado com sucesso"
18. Sistema atualiza lista (se visível)
19. Sistema envia email para o usuário (se email foi alterado):
    - "Seu email foi atualizado para: novo@email.com"
20. Sistema redireciona para página de detalhes

**Resultado Esperado**:
- ✅ Dados atualizados no banco
- ✅ Toast de sucesso exibido
- ✅ Audit log criado com diff
- ✅ Email enviado (se email alterado)
- ✅ Cache invalidado
- ✅ Permissões recalculadas

---

### Fluxo Alternativo 1 - Editar Apenas Nome

**FA-01: Modificação Parcial**

1. Usuário edita apenas campo "nome"
2. Sistema mantém outros campos inalterados
3. Sistema atualiza apenas campo modificado
4. Auditoria registra apenas alteração do nome

**Vantagens**:
- ✅ Performance (não recalcula permissões se roles não mudaram)
- ✅ Auditoria precisa (sabe exatamente o que mudou)

---

### Fluxo Alternativo 2 - Trocar Perfis

**FA-02: Modificar Roles do Usuário**

1. Usuário abre modal "Editar Perfis"
2. Sistema exibe multi-select com todas as roles disponíveis
3. Usuário desmarca "Gerente", adiciona "Auditor"
4. Sistema valida que usuário tem pelo menos 1 role
5. Sistema salva alteração
6. Sistema recalcula permissões efetivas
7. Sistema invalida token JWT atual (força re-login)
8. Sistema envia email: "Seus perfis foram alterados"

**Resultado Esperado**:
- ✅ Permissões atualizadas em tempo real
- ✅ Usuário afetado é deslogado (segurança)

---

### Fluxo Alternativo 3 - Desativar Usuário

**FA-03: Inativar Usuário (Soft Delete)**

1. Admin clica em toggle "Ativo/Inativo"
2. Sistema exibe confirmação: "Desativar usuário João Silva?"
   - "Este usuário não poderá mais fazer login"
   - "Documentos criados por ele serão preservados"
3. Admin confirma
4. Sistema seta `ativo = false`
5. Sistema invalida todos os tokens JWT desse usuário
6. Sistema mantém dados no banco (soft delete)
7. Sistema registra no audit log: "Usuário desativado por {admin}"
8. Sistema envia email ao usuário: "Sua conta foi desativada"

**Resultado Esperado**:
- ✅ Login bloqueado imediatamente
- ✅ Tokens invalidados
- ✅ Dados preservados (compliance)

---

### Fluxo Alternativo 4 - Reativar Usuário

**FA-04: Reativar Usuário Inativo**

1. Admin visualiza usuário inativo
2. Badge "INATIVO" aparece em destaque
3. Admin clica em "Reativar"
4. Sistema seta `ativo = true`
5. Sistema envia email: "Sua conta foi reativada"
6. Usuário pode fazer login novamente

---

### Fluxo Alternativo 5 - Resetar Senha

**FA-05: Forçar Troca de Senha**

1. Admin clica em "Resetar Senha"
2. Sistema gera senha temporária aleatória: `Temp@{random}`
3. Sistema hasheia senha com bcrypt
4. Sistema seta flag `mustChangePassword = true`
5. Sistema envia email com senha temporária
6. Usuário faz login com senha temporária
7. Sistema força tela de "Alterar Senha"

---

### Fluxo Alternativo 6 - Trocar Empresa

**FA-06: Transferir Usuário para Outra Empresa (Super Admin Only)**

1. Super Admin edita campo "Empresa"
2. Seleciona nova empresa no dropdown
3. Sistema valida que roles são compatíveis
4. Sistema atualiza `empresaId`
5. Sistema registra transferência no audit log
6. Sistema notifica ambos os admins (empresa origem e destino)

**Validação Importante**:
- ✅ Roles são globais ou específicas da empresa?
- ✅ Permissões continuam válidas?
- ✅ Documentos criados permanecem visíveis?

---

### Fluxos de Exceção

**FE-01: Email Já Existe**
- **Condição**: Usuário tenta alterar email para um já cadastrado
- **Validação**: `SELECT COUNT(*) FROM Usuarios WHERE Email = ? AND Id != ?`
- **Ação**:
  - Status: 400 Bad Request
  - Erro: `{ "email": ["Email já está em uso"] }`
  - Toast: "Este email já está cadastrado"
- **UX**: Campo email fica vermelho, focus automático

---

**FE-02: Permissão Negada - Hierarquia**
- **Condição**: Gerente tenta editar Admin
- **Validação**: `editorHierarquia >= targetHierarquia`
- **Ação**:
  - Status: 403 Forbidden
  - Erro: "Você não pode editar usuários de hierarquia superior"
  - Toast com ícone de cadeado
- **Log**: Registrar tentativa de escalação de privilégios

---

**FE-03: Permissão Negada - Empresa Diferente**
- **Condição**: Admin da Empresa A tenta editar usuário da Empresa B
- **Ação**:
  - Status: 403 Forbidden ou 404 Not Found (segurança por obscuridade)
  - Mensagem: "Usuário não encontrado"

---

**FE-04: Remover Todos os Perfis**
- **Condição**: Usuário tenta salvar sem nenhuma role selecionada
- **Validação**: `roles.length > 0`
- **Ação**:
  - Status: 400 Bad Request
  - Erro: "Usuário deve ter pelo menos um perfil"
  - Campo fica vermelho

---

**FE-05: Editar Próprio Perfil (Auto-Promoção)**
- **Condição**: Admin tenta adicionar "Super Admin" em si mesmo
- **Validação**: `userId != targetUserId OR !rolesContainHigherHierarchy`
- **Ação**:
  - Status: 403 Forbidden
  - Erro: "Você não pode alterar seus próprios perfis"
  - Mensagem educativa

---

**FE-06: Desativar Própria Conta**
- **Condição**: Admin tenta desativar a si mesmo
- **Validação**: `userId != targetUserId`
- **Ação**:
  - Status: 400 Bad Request
  - Erro: "Você não pode desativar sua própria conta"

---

**FE-07: Último Super Admin**
- **Condição**: Tentar remover role "Super Admin" do único Super Admin
- **Validação**: `COUNT(SuperAdmins) > 1 OR !removingSuperAdmin`
- **Ação**:
  - Status: 400 Bad Request
  - Erro: "Não é possível remover o último Super Administrador do sistema"
  - Solução: Criar outro Super Admin primeiro

---

**FE-08: Concorrência - Edição Simultânea**
- **Condição**: Admin A e Admin B editam mesmo usuário ao mesmo tempo
- **Detecção**: Usar `rowVersion` ou `dataUltimaAtualizacao`
- **Ação**:
  - Status: 409 Conflict
  - Erro: "Este usuário foi modificado por outro usuário. Recarregue a página."
  - Botão: "Recarregar e Perder Alterações" vs "Ver Diferenças"

---

**FE-09: Validação de Email Inválido**
- **Condição**: Email sem `@` ou formato inválido
- **Validação**: Regex no frontend + backend
- **Ação**:
  - Erro inline: "Email inválido"
  - Exemplos: "user@example.com"

---

**FE-10: Nome Muito Curto**
- **Condição**: Nome com menos de 3 caracteres
- **Validação**: `nome.length >= 3`
- **Ação**: Erro: "Nome deve ter pelo menos 3 caracteres"

---

## 🧪 Cenários de Teste (80 Total)

### Categoria 1: Validação de Campos (20 cenários)

#### CT-001: Editar Nome - Caminho Feliz
**Pré-condições**:
- Admin logado com `users:user:update`
- Usuário "João Silva" existe

**Ação**:
```http
PUT /api/usuarios/123
Authorization: Bearer {token}
Content-Type: application/json

{
  "nome": "João da Silva Santos",
  "email": "joao@teste.com",
  "empresaId": "...",
  "roles": ["role-guid-gerente"]
}
```

**Resultado Esperado**:
- ✅ Status: 200 OK
- ✅ Response: Usuário atualizado
- ✅ Banco: `UPDATE Usuarios SET Nome = 'João da Silva Santos', DataUltimaAtualizacao = NOW() WHERE Id = 123`
- ✅ Audit log criado:
  ```json
  {
    "action": "UPDATE",
    "entityType": "Usuario",
    "entityId": "123",
    "changes": {
      "nome": { "old": "João Silva", "new": "João da Silva Santos" }
    }
  }
  ```

---

#### CT-002: Editar Email Único
**Ação**: Alterar email de `joao@old.com` para `joao@new.com`

**Validação Backend**:
```sql
SELECT COUNT(*) FROM Usuarios
WHERE Email = 'joao@new.com' AND Id != '123'
```

**Resultado Esperado**:
- ✅ Email atualizado
- ✅ Email de notificação enviado para `joao@new.com`
- ✅ Assunto: "Seu email foi atualizado"

---

#### CT-003: Email Duplicado
**Ação**: Alterar email para um já existente

**Resultado Esperado**:
- ✅ Status: **400 Bad Request**
- ✅ Body:
  ```json
  {
    "errors": {
      "email": ["Email já está em uso"]
    }
  }
  ```
- ✅ Frontend exibe erro no campo email
- ✅ Banco NÃO é modificado

---

#### CT-004: Email Formato Inválido
**Ação**: Email = `joao@invalido`

**Resultado Esperado**:
- ✅ Status: 400 Bad Request
- ✅ Erro: "Email inválido"

---

#### CT-005: Nome Vazio
**Ação**: `{ "nome": "" }`

**Resultado Esperado**:
- ✅ Status: 400 Bad Request
- ✅ Erro: "Nome é obrigatório"

---

#### CT-006: Nome Muito Curto
**Ação**: `{ "nome": "Jo" }`

**Resultado Esperado**:
- ✅ Status: 400 Bad Request
- ✅ Erro: "Nome deve ter pelo menos 3 caracteres"

---

#### CT-007: Nome Muito Longo
**Ação**: `{ "nome": "A" * 201 }`

**Resultado Esperado**:
- ✅ Status: 400 Bad Request
- ✅ Erro: "Nome deve ter no máximo 200 caracteres"

---

#### CT-008: Telefone Formato Válido
**Ação**: `{ "telefone": "(11) 98765-4321" }`

**Resultado Esperado**:
- ✅ Aceita formatos: `(11) 98765-4321`, `11987654321`, `+5511987654321`
- ✅ Normaliza para: `+5511987654321` (E.164)

---

#### CT-009: Telefone Formato Inválido
**Ação**: `{ "telefone": "123" }`

**Resultado Esperado**:
- ✅ Status: 400 Bad Request
- ✅ Erro: "Telefone inválido"

---

#### CT-010: CPF Válido
**Ação**: `{ "cpf": "123.456.789-09" }`

**Validação**: Algoritmo de validação de CPF

**Resultado Esperado**:
- ✅ CPF válido aceito
- ✅ Armazenado sem formatação: `12345678909`

---

#### CT-011: CPF Inválido
**Ação**: `{ "cpf": "111.111.111-11" }`

**Resultado Esperado**:
- ✅ Status: 400 Bad Request
- ✅ Erro: "CPF inválido"

---

#### CT-012: CPF Duplicado (Permitido)
**Ação**: Dois usuários com mesmo CPF

**Resultado Esperado**:
- ✅ **Permitido** (caso de uso: usuário recriado)
- ✅ Aviso no frontend: "Já existe usuário com este CPF"

---

#### CT-013: Remover Telefone (Opcional)
**Ação**: `{ "telefone": null }`

**Resultado Esperado**:
- ✅ Campo aceita `null`
- ✅ Banco: `UPDATE ... SET Telefone = NULL`

---

#### CT-014: Trocar Empresa (Super Admin)
**Ação**:
```json
{
  "empresaId": "nova-empresa-guid"
}
```

**Resultado Esperado**:
- ✅ Apenas Super Admin pode fazer isso
- ✅ Empresa atualizada
- ✅ Audit log registra transferência

---

#### CT-015: Trocar Empresa (Admin Comum) - NEGADO
**Resultado Esperado**:
- ✅ Status: 403 Forbidden
- ✅ Erro: "Apenas Super Admin pode transferir usuários entre empresas"

---

#### CT-016: Adicionar Role
**Ação**:
```json
{
  "roles": ["role-gerente-guid", "role-auditor-guid"]
}
```

**Resultado Esperado**:
- ✅ Ambas as roles associadas
- ✅ Permissões efetivas = união de ambas
- ✅ Tabela `UsuarioRoles` atualizada

---

#### CT-017: Remover Role
**Ação**: Tinha 2 roles, agora só 1

**Resultado Esperado**:
- ✅ Role removida de `UsuarioRoles`
- ✅ Permissões recalculadas
- ✅ Token JWT invalidado

---

#### CT-018: Remover Todas as Roles - NEGADO
**Ação**: `{ "roles": [] }`

**Resultado Esperado**:
- ✅ Status: 400 Bad Request
- ✅ Erro: "Usuário deve ter pelo menos um perfil"

---

#### CT-019: Desativar Usuário
**Ação**: `{ "ativo": false }`

**Resultado Esperado**:
- ✅ Campo atualizado
- ✅ Tokens JWT invalidados
- ✅ Login bloqueado
- ✅ Email enviado: "Sua conta foi desativada"

---

#### CT-020: Reativar Usuário
**Ação**: `{ "ativo": true }` em usuário inativo

**Resultado Esperado**:
- ✅ Reativado
- ✅ Email: "Sua conta foi reativada"
- ✅ Login funciona novamente

---

### Categoria 2: Segurança e Permissões (20 cenários)

#### CT-021: Sem Permissão - Editar
**Pré-condições**: Usuário SEM `users:user:update`

**Ação**: `PUT /api/usuarios/123`

**Resultado Esperado**:
- ✅ Status: **403 Forbidden**
- ✅ Erro: "Você não tem permissão para editar usuários"
- ✅ Banco NÃO é modificado

---

#### CT-022: Hierarquia - Gerente Edita Usuário Comum
**Cenário**: Gerente (hierarquia 3) edita Usuário (hierarquia 4)

**Resultado Esperado**:
- ✅ Status: 200 OK
- ✅ Edição permitida

---

#### CT-023: Hierarquia - Gerente Tenta Editar Admin
**Cenário**: Gerente (hierarquia 3) tenta editar Admin (hierarquia 2)

**Resultado Esperado**:
- ✅ Status: **403 Forbidden**
- ✅ Erro: "Você não pode editar usuários de hierarquia superior"
- ✅ Log de auditoria: Tentativa de escalação de privilégios

---

#### CT-024: Editar Próprio Perfil - Dados Pessoais (Permitido)
**Cenário**: Usuário comum edita próprio nome/telefone

**Resultado Esperado**:
- ✅ Status: 200 OK
- ✅ Apenas campos pessoais permitidos (nome, telefone)
- ✅ Campos sensíveis bloqueados (roles, empresa, ativo)

---

#### CT-025: Editar Próprio Perfil - Adicionar Role (NEGADO)
**Cenário**: Admin tenta adicionar "Super Admin" em si mesmo

**Resultado Esperado**:
- ✅ Status: **403 Forbidden**
- ✅ Erro: "Você não pode alterar seus próprios perfis"

---

#### CT-026: Desativar Própria Conta (NEGADO)
**Ação**: Admin tenta `{ "ativo": false }` em si mesmo

**Resultado Esperado**:
- ✅ Status: **400 Bad Request**
- ✅ Erro: "Você não pode desativar sua própria conta"

---

#### CT-027: Último Super Admin - Remover Role
**Cenário**: Único Super Admin tenta mudar para Admin

**Resultado Esperado**:
- ✅ Status: **400 Bad Request**
- ✅ Erro: "Sistema deve ter pelo menos um Super Administrador"

---

#### CT-028: IDOR - Editar Usuário de Outra Empresa
**Cenário**: Admin Empresa A tenta editar usuário Empresa B

**Resultado Esperado**:
- ✅ Status: **403 Forbidden** ou **404 Not Found**
- ✅ Mensagem: "Usuário não encontrado"

---

#### CT-029: Token Expirado
**Ação**: Request com JWT expirado

**Resultado Esperado**:
- ✅ Status: **401 Unauthorized**
- ✅ Frontend redireciona para `/sign-in`

---

#### CT-030: SQL Injection no Nome
**Ação**: `{ "nome": "'; DROP TABLE Usuarios; --" }`

**Resultado Esperado**:
- ✅ Query parametrizada, SQL não executado
- ✅ Nome armazenado literalmente
- ✅ Banco intacto

---

#### CT-031: XSS no Nome
**Ação**: `{ "nome": "<script>alert('XSS')</script>" }`

**Resultado Esperado**:
- ✅ Backend aceita (dados do usuário)
- ✅ Frontend escapa HTML ao exibir
- ✅ Script NÃO executa

---

#### CT-032: CSRF Protection
**Ação**: Request sem token CSRF (se implementado)

**Resultado Esperado**:
- ✅ Status: 403 Forbidden
- ✅ Erro: "CSRF token inválido"

---

#### CT-033: Rate Limiting - Muitas Edições
**Ação**: 50 requisições PUT em 1 minuto

**Resultado Esperado**:
- ✅ Após 20 requisições: Status 429 Too Many Requests
- ✅ Header: `Retry-After: 60`

---

#### CT-034: Editar Usuário Anonimizado (LGPD)
**Cenário**: Tentar editar usuário que solicitou exclusão LGPD

**Resultado Esperado**:
- ✅ Status: **400 Bad Request**
- ✅ Erro: "Este usuário foi anonimizado e não pode ser editado"

---

#### CT-035: Permissão de Leitura Apenas
**Cenário**: Usuário com `users:user:read` mas SEM `update`

**Resultado Esperado**:
- ✅ Botão "Editar" não aparece no frontend
- ✅ Request PUT retorna 403

---

#### CT-036: Editar Campos Sensíveis (Proteção)
**Ação**: Tentar modificar `id`, `dataCriacao`, `password_hash` diretamente

**Resultado Esperado**:
- ✅ Backend ignora esses campos (whitelist de campos editáveis)
- ✅ Apenas campos permitidos são atualizados

---

#### CT-037: Mass Assignment Vulnerability
**Ação**:
```json
{
  "nome": "João",
  "isSystemAdmin": true,  // Campo não exposto
  "permissions": ["all"]  // Calculado, não editável
}
```

**Resultado Esperado**:
- ✅ Campos não-editáveis ignorados
- ✅ Apenas `nome` é atualizado

---

#### CT-038: Autenticação de Dois Fatores (2FA)
**Cenário**: Se 2FA habilitado, editar email requer confirmação

**Resultado Esperado**:
- ✅ Email não muda imediatamente
- ✅ Código enviado para email novo
- ✅ Após confirmação, email é atualizado

---

#### CT-039: Auditoria - Quem Editou
**Resultado Esperado**:
```json
{
  "action": "UPDATE",
  "performedBy": "admin-guid",
  "performedByName": "Maria Admin",
  "timestamp": "2025-10-20T15:30:00Z",
  "ipAddress": "192.168.1.100"
}
```

---

#### CT-040: Histórico de Alterações
**Ação**: Editar usuário pela 3ª vez

**Resultado Esperado**:
- ✅ 3 registros de auditoria
- ✅ Diff de cada alteração preservado
- ✅ Possível reverter para qualquer versão

---

### Categoria 3: Regras de Negócio (15 cenários)

#### CT-041: Email - Enviar Notificação de Alteração
**Ação**: Alterar email de usuário

**Resultado Esperado**:
- ✅ Email enviado para AMBOS os endereços (antigo e novo)
- ✅ Assunto: "Seu email foi atualizado"
- ✅ Conteúdo: Link para reverter (se não foi o usuário)

---

#### CT-042: Senha - Forçar Troca ao Alterar Email
**Regra de Negócio**: Se email muda, usuário deve trocar senha

**Resultado Esperado**:
- ✅ Flag `mustChangePassword = true`
- ✅ Próximo login força tela de "Alterar Senha"

---

#### CT-043: Roles - Recalcular Permissões
**Ação**: Adicionar role "Auditor" (que tem `audit:logs:read`)

**Resultado Esperado**:
- ✅ Campo `permissions` recalculado (união de todas as roles)
- ✅ Token JWT invalidado
- ✅ Próximo request retorna novo token com permissões atualizadas

---

#### CT-044: Desativar - Invalidar Sessões
**Ação**: Desativar usuário

**Resultado Esperado**:
- ✅ Todos os tokens JWT invalidados
- ✅ Se usuário estiver online, é deslogado imediatamente
- ✅ Tentativa de login retorna: "Conta desativada"

---

#### CT-045: Empresa - Manter Documentos ao Transferir
**Ação**: Transferir usuário da Empresa A para Empresa B

**Resultado Esperado**:
- ✅ Documentos criados pelo usuário na Empresa A ainda visíveis (referência histórica)
- ✅ Novos documentos pertencem à Empresa B

---

#### CT-046: Role Hierárquica - Não Pode Auto-Promover
**Regra**: Usuário não pode adicionar role de hierarquia superior à sua

**Resultado Esperado**:
- ✅ Validação: `novaRole.hierarquia >= editorRole.hierarquia`
- ✅ Erro se tentar adicionar "Super Admin" sendo "Admin"

---

#### CT-047: Perfil Padrão - Sempre Ter Pelo Menos 1
**Ação**: Remover última role

**Resultado Esperado**:
- ✅ Status: 400 Bad Request
- ✅ Erro: "Usuário deve ter pelo menos um perfil"

---

#### CT-048: Data de Atualização Automática
**Resultado Esperado**:
- ✅ Campo `dataUltimaAtualizacao` sempre atualizado
- ✅ Backend: `entity.DataUltimaAtualizacao = DateTime.UtcNow;`

---

#### CT-049: Campo "Modificado Por"
**Resultado Esperado**:
- ✅ Campo `modificadoPorId` armazenado
- ✅ Rastreabilidade completa

---

#### CT-050: Soft Delete vs Hard Delete
**Regra**: Usuários NUNCA são deletados do banco

**Resultado Esperado**:
- ✅ Desativação seta `ativo = false`
- ✅ Dados preservados para auditoria/compliance

---

#### CT-051: LGPD - Direito ao Esquecimento
**Cenário**: Usuário solicita exclusão de dados

**Resultado Esperado**:
- ✅ Dados pessoais anonimizados: `nome = "[REMOVIDO]", email = "anon-{guid}@sistema.local"`
- ✅ Logs de auditoria preservados (obrigação legal)
- ✅ Flag `isAnonimizado = true`

---

#### CT-052: Unicidade - Email Case-Insensitive
**Ação**: Tentar mudar email para `JOAO@TESTE.COM` (já existe `joao@teste.com`)

**Resultado Esperado**:
- ✅ Status: 400 Bad Request
- ✅ Erro: "Email já está em uso"
- ✅ Comparação: `LOWER(email)`

---

#### CT-053: Campos Computed - Não Editáveis
**Campos**: `permissions`, `hierarquia`, `empresaNome`

**Resultado Esperado**:
- ✅ São recalculados/buscados em tempo real
- ✅ Valores enviados pelo frontend são ignorados

---

#### CT-054: Validação de Empresa Ativa
**Ação**: Transferir usuário para empresa desativada

**Resultado Esperado**:
- ✅ Status: 400 Bad Request
- ✅ Erro: "Não é possível transferir usuário para empresa inativa"

---

#### CT-055: Limite de Usuários por Empresa (Plano)
**Cenário**: Empresa no plano "Básico" (max 10 usuários)

**Ação**: Transferir 11º usuário para essa empresa

**Resultado Esperado**:
- ✅ Status: 400 Bad Request
- ✅ Erro: "Empresa atingiu limite de usuários do plano contratado"

---

### Categoria 4: Concorrência (10 cenários)

#### CT-056: Edição Simultânea - Mesmos Campos
**Cenário**: Admin A e Admin B editam nome do mesmo usuário ao mesmo tempo

**Implementação**: Usar `rowVersion` ou `timestamp`

**Ação Admin A**:
```json
PUT /api/usuarios/123
{
  "nome": "João Silva Santos",
  "rowVersion": "AAAAAAAAB9E="
}
```

**Ação Admin B** (500ms depois):
```json
PUT /api/usuarios/123
{
  "nome": "João da Silva",
  "rowVersion": "AAAAAAAAB9E="  // Mesma versão!
}
```

**Resultado Esperado**:
- ✅ Admin A: 200 OK (primeira requisição)
- ✅ Admin B: **409 Conflict**
  - Erro: "Este usuário foi modificado por outro usuário"
  - Body: Mostra alterações conflitantes
  - Opções: "Recarregar" ou "Sobrescrever"

---

#### CT-057: Edição Simultânea - Campos Diferentes
**Cenário**: Admin A edita nome, Admin B edita telefone

**Estratégia**: Merge automático (campos diferentes)

**Resultado Esperado**:
- ✅ Ambas as alterações aplicadas
- ✅ Nome = valor de Admin A
- ✅ Telefone = valor de Admin B
- ✅ Audit log registra ambas as operações

---

#### CT-058: Desativar Durante Edição
**Cenário**: Admin A edita usuário, Admin B desativa ao mesmo tempo

**Resultado Esperado**:
- ✅ Desativação tem prioridade (operação crítica)
- ✅ Edição de Admin A retorna 409 Conflict
- ✅ Mensagem: "Usuário foi desativado durante a edição"

---

#### CT-059: Deletar Durante Visualização
**Cenário**: Admin A visualiza detalhes, Admin B deleta (desativa)

**Resultado Esperado**:
- ✅ Tela de Admin A mostra banner: "Este usuário foi desativado"
- ✅ Botão "Editar" desaparece
- ✅ Dados ainda visíveis (histórico)

---

#### CT-060: Race Condition - Último Super Admin
**Cenário**: 2 Super Admins existem. Ambos tentam mudar para Admin ao mesmo tempo.

**Resultado Esperado**:
- ✅ Primeiro request: 200 OK
- ✅ Segundo request: 400 Bad Request
- ✅ Erro: "Sistema deve ter pelo menos um Super Administrador"
- ✅ Validação com lock: `SELECT ... FOR UPDATE`

---

#### CT-061: Concurrent Email Change
**Cenário**: Usuário A muda email para `novo@teste.com`, Usuário B também tenta mudar para mesmo email

**Resultado Esperado**:
- ✅ Primeiro: 200 OK
- ✅ Segundo: 400 Bad Request (email duplicado)
- ✅ Unique constraint no banco previne duplicata

---

#### CT-062: Transaction Rollback
**Cenário**: Erro durante atualização (ex: envio de email falha)

**Resultado Esperado**:
- ✅ Transaction rollback
- ✅ Banco não é modificado
- ✅ Erro retornado ao cliente
- ✅ Idempotência mantida

---

#### CT-063: Idempotência - Requisições Duplicadas
**Cenário**: Usuário clica "Salvar" 2 vezes rápido

**Resultado Esperado**:
- ✅ Primeira requisição: 200 OK
- ✅ Segunda requisição: 200 OK (mesma resposta)
- ✅ Banco atualizado apenas 1 vez
- ✅ Usar `Idempotency-Key` header

---

#### CT-064: Lock Otimista vs Pessimista
**Teste de Performance**:
- Otimista: Permite leituras concorrentes, falha ao salvar se modificado
- Pessimista: Bloqueia registro durante edição

**Resultado Esperado**:
- ✅ Usar **otimista** para melhor performance
- ✅ Apenas `rowVersion` check

---

#### CT-065: Timeout em Transaction Longa
**Cenário**: Atualização demora > 30 segundos

**Resultado Esperado**:
- ✅ Transaction timeout
- ✅ Rollback automático
- ✅ Erro: "Operação demorou muito tempo"

---

### Categoria 5: Performance e Integração (15 cenários)

#### CT-066: Performance - Update Simples
**Ação**: `PUT /api/usuarios/123` alterando apenas nome

**Resultado Esperado**:
- ✅ Response time < 500ms
- ✅ SQL: `UPDATE Usuarios SET Nome = ? WHERE Id = ?` (apenas 1 campo)
- ✅ Não recalcula permissões se roles não mudaram

---

#### CT-067: Performance - Update com Permissões
**Ação**: Adicionar nova role

**Resultado Esperado**:
- ✅ Response time < 1 segundo
- ✅ SQL join para recalcular permissões:
  ```sql
  SELECT p.* FROM Permissions p
  JOIN RolePermissions rp ON p.Id = rp.PermissionId
  JOIN UsuarioRoles ur ON rp.RoleId = ur.RoleId
  WHERE ur.UsuarioId = ?
  ```

---

#### CT-068: Performance - Invalidar Cache
**Resultado Esperado**:
- ✅ Cache do usuário invalidado
- ✅ Próxima listagem não retorna dados stale
- ✅ Cache key: `user:{id}`

---

#### CT-069: Performance - Batch Update
**Cenário**: Desativar 100 usuários de uma vez (caso de rescisão em massa)

**Ação**: `PUT /api/usuarios/batch-deactivate`

**Resultado Esperado**:
- ✅ SQL bulk update:
  ```sql
  UPDATE Usuarios SET Ativo = false WHERE Id IN (...)
  ```
- ✅ Response time < 5 segundos
- ✅ Audit log batch criado

---

#### CT-070: Integração - Envio de Email Assíncrono
**Resultado Esperado**:
- ✅ Request retorna 200 antes do email ser enviado
- ✅ Email enfileirado (RabbitMQ, Hangfire, etc.)
- ✅ Falha no email NÃO bloqueia atualização

---

#### CT-071: Integração - Webhook Externo
**Cenário**: Sistema externo recebe notificação de alteração

**Resultado Esperado**:
- ✅ Webhook enviado: `POST https://external.com/webhook`
  ```json
  {
    "event": "user.updated",
    "userId": "123",
    "changes": ["nome", "email"]
  }
  ```
- ✅ Assíncrono (não bloqueia response)

---

#### CT-072: Integração - Sincronizar com AD/LDAP
**Cenário**: Empresa usa Active Directory

**Resultado Esperado**:
- ✅ Alteração de email sincronizada com AD
- ✅ Falha em AD não bloqueia sistema (log warning)

---

#### CT-073: Integração - Atualizar Elasticsearch
**Cenário**: Sistema usa Elasticsearch para busca

**Resultado Esperado**:
- ✅ Índice atualizado após update no banco
- ✅ Eventual consistency ok (< 5 segundos)

---

#### CT-074: Database Index Performance
**Validação**: Verificar query plan

**Resultado Esperado**:
- ✅ `UPDATE` usa índice em `Id` (primary key)
- ✅ Validação de email usa índice em `Email`
- ✅ Sem table scans

---

#### CT-075: N+1 Query Problem
**Cenário**: Atualizar usuário e carregar roles

**Resultado Esperado**:
- ✅ Usar eager loading: `.Include(u => u.Roles)`
- ✅ Apenas 2 queries (1 update + 1 select com join)
- ✅ Não fazer 1 query por role (N+1)

---

#### CT-076: Connection Pool Exhaustion
**Teste**: 1000 updates simultâneos

**Resultado Esperado**:
- ✅ Connection pool configurado adequadamente
- ✅ Nenhuma requisição falha com "timeout getting connection"
- ✅ Pool size: min 10, max 100

---

#### CT-077: Memory Leak Test
**Teste**: Executar 10.000 updates

**Resultado Esperado**:
- ✅ Memória estabiliza (não cresce indefinidamente)
- ✅ GC libera objetos antigos
- ✅ Heap size constante

---

#### CT-078: Logging Performance Impact
**Validação**: Verificar overhead de logging

**Resultado Esperado**:
- ✅ Logging assíncrono (não bloqueia thread)
- ✅ Overhead < 10ms por request
- ✅ Usar structured logging (Serilog)

---

#### CT-079: Metrics e Observability
**Resultado Esperado**:
- ✅ Métrica: `usuarios.update.duration` (histogram)
- ✅ Métrica: `usuarios.update.errors` (counter)
- ✅ Trace distribuído (OpenTelemetry)

---

#### CT-080: Disaster Recovery - Backup
**Cenário**: Atualização incorreta (erro humano)

**Resultado Esperado**:
- ✅ Audit log permite restaurar estado anterior
- ✅ Função: `POST /api/usuarios/{id}/restore-version/{auditId}`
- ✅ Rollback para qualquer versão histórica

---

## 🔒 Matriz de Permissões

| Perfil | Editar Próprio | Editar Subordinados | Editar Mesma Empresa | Editar Qualquer | Trocar Empresa |
|--------|---------------|---------------------|----------------------|-----------------|----------------|
| **Super Admin** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Admin** | ✅ Dados pessoais | ✅ | ✅ | ❌ | ❌ |
| **Gerente** | ✅ Dados pessoais | ✅ Hierarquia inferior | ❌ | ❌ | ❌ |
| **Usuário** | ✅ Dados pessoais | ❌ | ❌ | ❌ | ❌ |

**Dados Pessoais**: Nome, Telefone, Foto
**Dados Sensíveis**: Email (requer 2FA), Roles, Empresa, Status

---

## 📈 Critérios de Aceitação

### Backend
- [ ] Endpoint `PUT /api/usuarios/{id}` com validação completa
- [ ] Validação de hierarquia em todas as edições
- [ ] Recálculo de permissões ao alterar roles
- [ ] Audit log com diff (before/after)
- [ ] Email de notificação assíncrono
- [ ] Invalidação de tokens JWT ao alterar roles/status
- [ ] Proteção contra edição simultânea (optimistic locking)
- [ ] Validação de unicidade de email
- [ ] Soft delete (nunca hard delete)
- [ ] Response time < 1s (p95)

### Frontend
- [ ] Formulário de edição com validação em tempo real
- [ ] Campos desabilitados conforme permissões
- [ ] Confirmação ao desativar usuário
- [ ] Confirmação ao alterar email (se 2FA habilitado)
- [ ] Detecção de edição simultânea com opções de merge
- [ ] Loading state durante save
- [ ] Toast de sucesso/erro
- [ ] Rollback UI se request falhar (otimistic UI)
- [ ] Validação de email inline (debounce 500ms)
- [ ] Acessibilidade (formulário navegável por teclado)

---

## 🧩 Dependências

### Backend
- `UsuariosController.Update(id, request)` ✅ Implementado
- `AuthorizationService.ValidateHierarchy()` ✅ Implementado
- `PermissionCalculator.GetEffectivePermissions()` ✅ Implementado
- `AuditLogService.LogUpdate()` ✅ Implementado
- `EmailService.SendEmailChangedNotification()` ✅ Implementado
- `TokenRevocationService.InvalidateUserTokens()` ⚠️ Verificar implementação

### Frontend
- `UsersDetailsComponent` ✅ Implementado
- `UsersService.updateUser()` ✅ Implementado
- `ValidationService` ✅ Implementado
- `PermissionDirective` ✅ Implementado

---

## 📝 Notas de Implementação

### Optimistic Locking
```csharp
public class Usuario
{
    [Timestamp]
    public byte[] RowVersion { get; set; }
}

// No update
try {
    context.SaveChanges();
} catch (DbUpdateConcurrencyException) {
    return Conflict(new { error = "Usuário foi modificado por outro usuário" });
}
```

### Audit Log Structure
```json
{
  "id": "guid",
  "action": "UPDATE",
  "entityType": "Usuario",
  "entityId": "123",
  "performedBy": "admin-guid",
  "timestamp": "2025-10-20T15:30:00Z",
  "changes": {
    "nome": { "old": "João", "new": "João Silva" },
    "email": { "old": "joao@old.com", "new": "joao@new.com" }
  },
  "ipAddress": "192.168.1.100",
  "userAgent": "Mozilla/5.0..."
}
```

### Performance Optimization
- Usar `AsNoTracking()` para reads
- Usar `ExecuteUpdateAsync()` para bulk updates (EF Core 7+)
- Índices: `Email (unique)`, `EmpresaId`, `Ativo`, `DataCriacao`
- Cache invalidation: Redis pub/sub

---

## ✅ Checklist de Completude

- [x] Todos os fluxos documentados (6 alternativos, 10 exceção)
- [x] 80 cenários de teste criados e detalhados
- [x] Matriz de permissões completa
- [x] Regras de negócio documentadas (15 regras)
- [x] Casos de concorrência cobertos (10 cenários)
- [x] Performance benchmarks (15 testes)
- [x] Segurança validada (20 testes)
- [x] Auditoria completa
- [x] LGPD compliance
- [x] Critérios de aceitação definidos

---

**Status Final**: ✅ **UC03 100% ESPECIFICADO**

**Complexidade**: 🔴 Alta (devido a concorrência, hierarquia, permissões)

**Próximos Passos**:
1. Implementar optimistic locking no backend
2. Adicionar testes de concorrência automatizados
3. Validar performance com 10k usuários
4. Teste de penetração (IDOR, privilege escalation)
5. Executar todos os 80 cenários de teste

**Última Atualização**: 2025-10-20
**Revisado por**: Anderson Chipak + Claude Code

---

# UC04: Excluir Usuário - Especificação Completa

**Autor**: Anderson Chipak + Claude Code
**Status**: ✅ Implementado (Backend + Frontend)

---

## 📋 Sumário Executivo

| Aspecto | Detalhes |
|---------|----------|
| **Objetivo** | Permitir desativação/exclusão de usuários com preservação de dados para auditoria |
| **Atores** | Super Admin, Admin (com permissão `users:user:delete`) |
| **Pré-condições** | Usuário autenticado, target user existe, permissão adequada |
| **Pós-condições** | Usuário desativado (soft delete), auditoria registrada, dados relacionados preservados |
| **Cenários de Teste** | **70 cenários** (validação, segurança, integridade referencial, compliance) |
| **Prioridade** | 🔴 Crítica (operação irreversível com implicações legais) |

---

## 🎯 Descrição do Caso de Uso

### Objetivo
Permitir que administradores removam usuários do sistema de forma segura, respeitando:
1. **Soft Delete**: Dados preservados no banco (compliance LGPD/GDPR)
2. **Integridade Referencial**: Manter relacionamentos (documentos, logs)
3. **Auditoria**: Registrar quem deletou, quando e por quê
4. **Segurança**: Impedir auto-exclusão, validar hierarquia

### Tipos de Exclusão

| Tipo | Descrição | Quando Usar | Reversível |
|------|-----------|-------------|------------|
| **Desativar** (Soft Delete) | `ativo = false`, dados preservados | Padrão, 99% dos casos | ✅ Sim |
| **Anonimizar** (LGPD) | Dados pessoais removidos, logs preservados | Solicitação LGPD | ❌ Não |
| **Hard Delete** | Remoção física do banco | NUNCA (apenas dev/test) | ❌ Não |

### Atores Principais
- **Super Administrador**: Pode deletar qualquer usuário (exceto si mesmo)
- **Administrador**: Pode deletar usuários da própria empresa (hierarquia inferior)
- **Gerente**: Pode deletar usuários subordinados

### Permissões Necessárias
- **Deletar usuário**: `users:user:delete`
- **Anonimizar (LGPD)**: `users:user:delete` + `users:user:anonymize` (opcional)

---

## 📊 Fluxos

### Fluxo Principal - Desativar Usuário (Soft Delete)

**FP-01: Desativar Usuário**

1. Admin acessa página `/management/users`
2. Admin localiza usuário "João Silva"
3. Admin clica no menu "⋮" da linha do usuário
4. Admin seleciona "Desativar Usuário" (ícone: 🗑️)
5. Sistema exibe modal de confirmação:
   ```
   ⚠️ Desativar Usuário

   Você está prestes a desativar:
   João Silva (joao@teste.com)

   Consequências:
   • Este usuário não poderá mais fazer login
   • Todas as sessões ativas serão encerradas
   • Documentos criados por ele serão preservados
   • Esta ação pode ser revertida posteriormente

   Motivo (opcional):
   [________________]

   [Cancelar]  [Desativar Usuário]
   ```
6. Admin (opcionalmente) informa motivo: "Fim do contrato"
7. Admin clica em "Desativar Usuário"
8. Sistema valida permissão `users:user:delete`
9. Sistema valida hierarquia (não pode deletar superior)
10. Sistema valida que não é auto-exclusão
11. Sistema executa `DELETE /api/usuarios/{id}` (soft delete)
12. Backend:
    - Seta `ativo = false`
    - Seta `dataDesativacao = NOW()`
    - Seta `desativadoPorId = {adminId}`
    - Seta `motivoDesativacao = "Fim do contrato"`
    - Invalida todos os tokens JWT do usuário
    - Registra no audit log
    - Enfileira email para o usuário
13. Sistema exibe toast: "✅ Usuário desativado com sucesso"
14. Sistema remove usuário da lista (ou aplica filtro "Ativos")
15. Sistema envia email assíncrono:
    ```
    Assunto: Sua conta foi desativada

    Olá João Silva,

    Sua conta no IControlIT foi desativada em 20/10/2025 às 15:30.
    Motivo: Fim do contrato

    Se você acredita que isso é um erro, entre em contato com o administrador.

    Equipe IControlIT
    ```
16. Usuário tenta fazer login: Mensagem "Conta desativada. Contate o administrador."

**Resultado Esperado**:
- ✅ `ativo = false` no banco
- ✅ Login bloqueado imediatamente
- ✅ Tokens JWT invalidados
- ✅ Audit log criado
- ✅ Email enviado
- ✅ Dados preservados (compliance)

---

### Fluxo Alternativo 1 - Anonimizar (LGPD)

**FA-01: Direito ao Esquecimento (LGPD Art. 18)**

**Cenário**: Usuário solicita exclusão de seus dados pessoais

1. Admin recebe solicitação formal de exclusão LGPD
2. Admin acessa `/management/users/{id}`
3. Admin clica em "⚙️ Ações Avançadas > Anonimizar (LGPD)"
4. Sistema exibe modal de confirmação ESPECIAL:
   ```
   ⚠️⚠️ ATENÇÃO: Anonimização LGPD ⚠️⚠️

   Esta ação é IRREVERSÍVEL e atende ao Art. 18 da LGPD.

   Dados que serão REMOVIDOS:
   • Nome → [DADOS REMOVIDOS]
   • Email → anon-{guid}@sistema.local
   • Telefone, CPF → NULL
   • Foto → removida

   Dados que serão PRESERVADOS (obrigação legal):
   • Logs de auditoria (histórico de ações)
   • Documentos gerados (metadados)
   • Timestamps (criação, atualização)

   ⚠️ ESTA AÇÃO NÃO PODE SER REVERTIDA

   Digite "CONFIRMAR ANONIMIZAÇÃO" para continuar:
   [_______________________________]

   [Cancelar]  [Anonimizar Permanentemente]
   ```
5. Admin digita frase de confirmação
6. Admin clica em "Anonimizar Permanentemente"
7. Sistema executa `POST /api/usuarios/{id}/anonymize`
8. Backend:
   - `nome = "[DADOS REMOVIDOS]"`
   - `email = "anon-{guid}@sistema.local"` (único para evitar conflitos)
   - `telefone = NULL`
   - `cpf = NULL`
   - `dataNascimento = NULL`
   - `foto = NULL`
   - `isAnonimizado = true`
   - `dataAnonimizacao = NOW()`
   - `anonimizadoPorId = {adminId}`
   - `ativo = false`
   - **Preserva**: `id`, `empresaId`, `dataCriacao`, `dataUltimaAtualizacao`
   - **Preserva**: Todas as entradas em `AuditLogs`
   - **Atualiza**: Documentos criados por ele (mantém referência, mas autor = "[Usuário Removido]")
9. Sistema registra ação em audit log especial: "LGPD_ANONYMIZATION"
10. Sistema exibe toast: "✅ Dados anonimizados conforme LGPD"
11. Sistema envia confirmação por email ao solicitante (se email foi fornecido na solicitação)

**Resultado Esperado**:
- ✅ Dados pessoais irrecuperáveis
- ✅ Compliance LGPD/GDPR
- ✅ Logs preservados (art. 19 LGPD)
- ✅ Auditoria da anonimização

---

### Fluxo Alternativo 2 - Reativar Usuário

**FA-02: Reverter Desativação**

1. Admin visualiza lista de "Usuários Inativos"
2. Admin localiza "João Silva" (badge INATIVO)
3. Admin clica em "Reativar"
4. Sistema valida que usuário NÃO está anonimizado
5. Sistema seta `ativo = true`
6. Sistema limpa `dataDesativacao`, `motivoDesativacao`
7. Sistema registra reativação no audit log
8. Sistema envia email: "Sua conta foi reativada"
9. Usuário pode fazer login novamente

**Validação**:
- ✅ Apenas usuários desativados podem ser reativados
- ✅ Usuários anonimizados NÃO podem ser reativados

---

### Fluxo Alternativo 3 - Exclusão em Lote

**FA-03: Desativar Múltiplos Usuários**

**Cenário**: Rescisão de contrato com empresa (desativar todos os usuários)

1. Admin seleciona múltiplos usuários (checkbox)
2. Admin clica em "Ações em Lote > Desativar Selecionados"
3. Sistema exibe confirmação:
   ```
   Desativar 15 usuários?

   [Lista dos usuários]

   Motivo para todos:
   [Rescisão de contrato com empresa ABC]
   ```
4. Admin confirma
5. Sistema executa desativação em batch (transaction)
6. Sistema exibe progresso: "Desativando 5/15..."
7. Sistema exibe resultado:
   ```
   ✅ 14 usuários desativados
   ❌ 1 falha: "João Admin" (hierarquia superior à sua)
   ```

---

### Fluxo Alternativo 4 - Excluir com Transferência de Documentos

**FA-04: Transferir Propriedade Antes de Deletar**

**Cenário**: João criou 50 documentos importantes. Ao deletá-lo, transferir para Maria.

1. Admin acessa detalhes de João
2. Sistema exibe alerta: "⚠️ Este usuário possui 50 documentos"
3. Admin clica em "Desativar e Transferir Documentos"
4. Sistema exibe modal:
   ```
   Transferir documentos de João Silva

   50 documentos serão transferidos para:
   [Selecionar usuário ▼]

   [Cancelar]  [Transferir e Desativar]
   ```
5. Admin seleciona "Maria Santos"
6. Sistema:
   - Desativa João
   - Atualiza `criadoPorId` de 50 documentos para Maria
   - Registra transferência no audit log de cada documento

---

### Fluxos de Exceção

**FE-01: Permissão Negada**
- **Condição**: Usuário sem `users:user:delete`
- **Ação**:
  - Status: 403 Forbidden
  - Botão "Desativar" não aparece no frontend
  - Toast: "Você não tem permissão para desativar usuários"

---

**FE-02: Tentar Deletar a Si Mesmo**
- **Condição**: `deleterId == targetUserId`
- **Ação**:
  - Status: 400 Bad Request
  - Erro: "Você não pode desativar sua própria conta"
  - Modal de confirmação nem aparece

---

**FE-03: Hierarquia - Tentar Deletar Superior**
- **Condição**: Gerente tenta deletar Admin
- **Ação**:
  - Status: 403 Forbidden
  - Erro: "Você não pode desativar usuários de hierarquia superior"
  - Log: Tentativa de escalação de privilégios

---

**FE-04: Último Super Admin**
- **Condição**: Tentar deletar o único Super Admin do sistema
- **Validação**: `SELECT COUNT(*) FROM Usuarios WHERE Roles CONTAINS 'Super Admin' AND Ativo = true`
- **Ação**:
  - Status: 400 Bad Request
  - Erro: "Não é possível desativar o último Super Administrador do sistema"
  - Solução: Criar outro Super Admin primeiro

---

**FE-05: Usuário Já Desativado**
- **Condição**: Tentar deletar usuário com `ativo = false`
- **Ação**:
  - Status: 400 Bad Request
  - Erro: "Este usuário já está desativado"
  - Opção: "Reativar" em vez de "Desativar"

---

**FE-06: Usuário Já Anonimizado**
- **Condição**: Tentar deletar usuário com `isAnonimizado = true`
- **Ação**:
  - Status: 400 Bad Request
  - Erro: "Este usuário já foi anonimizado (LGPD)"
  - Botão "Desativar" não aparece

---

**FE-07: Usuário Não Encontrado**
- **Condição**: `DELETE /api/usuarios/{id-inexistente}`
- **Ação**:
  - Status: 404 Not Found
  - Erro: "Usuário não encontrado"

---

**FE-08: IDOR - Tentar Deletar Usuário de Outra Empresa**
- **Condição**: Admin Empresa A tenta deletar usuário Empresa B
- **Ação**:
  - Status: 403 Forbidden ou 404 Not Found
  - Mensagem: "Usuário não encontrado" (obscuridade)

---

**FE-09: Confirmação Não Fornecida**
- **Condição**: Usuário clica "Desativar" mas cancela modal
- **Ação**:
  - Nenhuma requisição enviada
  - Nenhuma alteração no banco

---

**FE-10: Falha ao Invalidar Tokens**
- **Condição**: Redis down, tokens não podem ser blacklisted
- **Ação**:
  - Desativação continua (não bloqueia)
  - Log warning: "Failed to invalidate tokens"
  - Tokens expiram naturalmente (max 24h)

---

**FE-11: Falha ao Enviar Email**
- **Condição**: SMTP server indisponível
- **Ação**:
  - Desativação continua (não bloqueia)
  - Email enfileirado para retry (3 tentativas)
  - Log warning

---

**FE-12: Constraint Violation - Documentos Obrigatórios**
- **Condição**: Sistema configurado para "Documentos devem ter autor ativo"
- **Ação**:
  - Status: 400 Bad Request
  - Erro: "Este usuário possui 50 documentos. Transfira-os antes de desativar."
  - Link: "Ver documentos"

---

## 🧪 Cenários de Teste (70 Total)

### Categoria 1: Validação Básica (10 cenários)

#### CT-001: Desativar Usuário - Caminho Feliz
**Pré-condições**:
- Admin logado com `users:user:delete`
- Usuário "João Silva" existe e está ativo

**Ação**:
```http
DELETE /api/usuarios/123
Authorization: Bearer {admin-token}
Content-Type: application/json

{
  "motivo": "Fim do contrato"
}
```

**Resultado Esperado**:
- ✅ Status: **200 OK** (ou 204 No Content)
- ✅ Response:
  ```json
  {
    "message": "Usuário desativado com sucesso",
    "userId": "123"
  }
  ```
- ✅ Banco:
  ```sql
  UPDATE Usuarios SET
    Ativo = 0,
    DataDesativacao = '2025-10-20T15:30:00Z',
    DesativadoPorId = '{admin-id}',
    MotivoDesativacao = 'Fim do contrato'
  WHERE Id = '123'
  ```
- ✅ Audit log criado:
  ```json
  {
    "action": "DELETE",
    "entityType": "Usuario",
    "entityId": "123",
    "performedBy": "{admin-id}",
    "details": {
      "motivo": "Fim do contrato",
      "softDelete": true
    }
  }
  ```
- ✅ Email enfileirado
- ✅ Tokens invalidados

---

#### CT-002: Usuário Desativado Não Pode Fazer Login
**Pré-condições**: João foi desativado

**Ação**:
```http
POST /api/auth/login
{
  "email": "joao@teste.com",
  "password": "senha123"
}
```

**Resultado Esperado**:
- ✅ Status: **401 Unauthorized**
- ✅ Body:
  ```json
  {
    "error": "Conta desativada. Entre em contato com o administrador."
  }
  ```
- ✅ Frontend exibe mensagem clara

---

#### CT-003: Usuário Desativado Não Aparece na Lista (Filtro Padrão)
**Ação**: `GET /api/usuarios?ativo=true`

**Resultado Esperado**:
- ✅ João NÃO aparece na lista
- ✅ Total count diminui em 1

---

#### CT-004: Visualizar Usuários Inativos
**Ação**: `GET /api/usuarios?ativo=false`

**Resultado Esperado**:
- ✅ João aparece na lista
- ✅ Badge "INATIVO" exibido
- ✅ Data de desativação visível

---

#### CT-005: Reativar Usuário Desativado
**Ação**: `POST /api/usuarios/123/reativar`

**Resultado Esperado**:
- ✅ Status: 200 OK
- ✅ `ativo = true`
- ✅ `dataDesativacao = NULL`
- ✅ Login funciona novamente
- ✅ Email: "Sua conta foi reativada"

---

#### CT-006: Desativar Sem Motivo (Opcional)
**Ação**:
```http
DELETE /api/usuarios/123
{ "motivo": null }
```

**Resultado Esperado**:
- ✅ Status: 200 OK
- ✅ Campo `motivoDesativacao` fica NULL
- ✅ Desativação funciona normalmente

---

#### CT-007: Motivo Muito Longo
**Ação**: `{ "motivo": "A" * 1001 }` (> 1000 caracteres)

**Resultado Esperado**:
- ✅ Status: 400 Bad Request
- ✅ Erro: "Motivo deve ter no máximo 1000 caracteres"

---

#### CT-008: Verificar Data de Desativação
**Resultado Esperado**:
- ✅ `dataDesativacao` é timestamp UTC
- ✅ Formato ISO 8601
- ✅ Precisão de segundos

---

#### CT-009: Verificar Quem Desativou
**Resultado Esperado**:
- ✅ Campo `desativadoPorId` aponta para admin
- ✅ Query:
  ```sql
  SELECT u.Nome, u.DataDesativacao, admin.Nome AS DesativadoPor
  FROM Usuarios u
  JOIN Usuarios admin ON u.DesativadoPorId = admin.Id
  WHERE u.Id = '123'
  ```
- ✅ Frontend exibe: "Desativado por Maria Admin em 20/10/2025"

---

#### CT-010: Soft Delete - Dados Preservados
**Validação SQL**:
```sql
SELECT * FROM Usuarios WHERE Id = '123' AND Ativo = 0
```

**Resultado Esperado**:
- ✅ Registro EXISTE no banco
- ✅ Todos os campos preservados (nome, email, etc.)
- ✅ Apenas flag `ativo` = false

---

### Categoria 2: Segurança e Permissões (20 cenários)

#### CT-011: Sem Permissão - Desativar
**Pré-condições**: Usuário SEM `users:user:delete`

**Ação**: `DELETE /api/usuarios/123`

**Resultado Esperado**:
- ✅ Status: **403 Forbidden**
- ✅ Erro: "Você não tem permissão para desativar usuários"
- ✅ Banco NÃO modificado

---

#### CT-012: Auto-Exclusão (NEGADO)
**Cenário**: Admin tenta desativar a si mesmo

**Ação**: `DELETE /api/usuarios/{meu-proprio-id}`

**Resultado Esperado**:
- ✅ Status: **400 Bad Request**
- ✅ Erro: "Você não pode desativar sua própria conta"
- ✅ Validação backend: `deleterId != targetUserId`

---

#### CT-013: Hierarquia - Gerente Desativa Usuário Comum
**Cenário**: Gerente (h=3) desativa Usuário (h=4)

**Resultado Esperado**:
- ✅ Status: 200 OK
- ✅ Desativação permitida

---

#### CT-014: Hierarquia - Gerente Tenta Desativar Admin
**Cenário**: Gerente (h=3) tenta desativar Admin (h=2)

**Resultado Esperado**:
- ✅ Status: **403 Forbidden**
- ✅ Erro: "Você não pode desativar usuários de hierarquia superior"
- ✅ Log: Tentativa de escalação de privilégios registrada

---

#### CT-015: Último Super Admin (BLOQUEADO)
**Cenário**: Sistema tem apenas 1 Super Admin

**Ação**: Tentar desativá-lo

**Validação Backend**:
```sql
SELECT COUNT(*) FROM Usuarios u
JOIN UsuarioRoles ur ON u.Id = ur.UsuarioId
JOIN Roles r ON ur.RoleId = r.Id
WHERE r.Hierarquia = 1 AND u.Ativo = 1
```

**Resultado Esperado**:
- ✅ Status: **400 Bad Request**
- ✅ Erro: "Não é possível desativar o último Super Administrador"
- ✅ Solução exibida: "Crie outro Super Admin primeiro"

---

#### CT-016: Último Admin da Empresa (Aviso, Mas Permite)
**Cenário**: Empresa tem apenas 1 Admin

**Ação**: Tentar desativá-lo

**Resultado Esperado**:
- ✅ Status: 200 OK (permite)
- ✅ Warning no frontend: "⚠️ Este é o último Admin da empresa"
- ✅ Confirmação extra: "Tem certeza?"

---

#### CT-017: IDOR - Desativar Usuário de Outra Empresa
**Cenário**: Admin Empresa A tenta desativar usuário Empresa B

**Resultado Esperado**:
- ✅ Status: **404 Not Found** (segurança por obscuridade)
- ✅ Mensagem: "Usuário não encontrado"
- ✅ Log: Tentativa de IDOR registrada

---

#### CT-018: Token Expirado
**Ação**: Request com JWT expirado

**Resultado Esperado**:
- ✅ Status: **401 Unauthorized**
- ✅ Frontend redireciona para login

---

#### CT-019: SQL Injection no Motivo
**Ação**: `{ "motivo": "'; DROP TABLE Usuarios; --" }`

**Resultado Esperado**:
- ✅ Query parametrizada, SQL não executa
- ✅ Motivo armazenado literalmente
- ✅ Banco intacto

---

#### CT-020: Rate Limiting - Muitas Exclusões
**Ação**: 50 DELETE requests em 1 minuto

**Resultado Esperado**:
- ✅ Após 20 requests: Status **429 Too Many Requests**
- ✅ Header: `Retry-After: 60`
- ✅ Mensagem: "Muitas tentativas. Aguarde 1 minuto."

---

#### CT-021: CSRF Protection
**Ação**: Request sem token CSRF (se implementado)

**Resultado Esperado**:
- ✅ Status: 403 Forbidden
- ✅ Erro: "CSRF token inválido"

---

#### CT-022: Audit Log - Quem, Quando, Por Quê
**Resultado Esperado**:
```json
{
  "id": "audit-guid",
  "action": "DELETE",
  "entityType": "Usuario",
  "entityId": "123",
  "performedBy": "admin-guid",
  "performedByName": "Maria Admin",
  "timestamp": "2025-10-20T15:30:00Z",
  "ipAddress": "192.168.1.100",
  "userAgent": "Mozilla/5.0...",
  "details": {
    "motivo": "Fim do contrato",
    "usuarioNome": "João Silva",
    "usuarioEmail": "joao@teste.com",
    "softDelete": true
  }
}
```

---

#### CT-023: Invalidar Tokens JWT
**Resultado Esperado**:
- ✅ Todos os tokens do usuário adicionados ao blacklist (Redis)
- ✅ Key: `blacklist:user:{userId}:*`
- ✅ TTL: Tempo até expiração do token mais longo
- ✅ Próxima requisição com token antigo: 401 Unauthorized

---

#### CT-024: Invalidar Sessões Ativas
**Cenário**: João está logado em 3 dispositivos

**Resultado Esperado**:
- ✅ Desativação invalida todas as 3 sessões
- ✅ João é deslogado imediatamente em todos os dispositivos
- ✅ Mensagem: "Sua conta foi desativada"

---

#### CT-025: Permissão Especial - Anonimizar
**Cenário**: Admin tem `users:user:delete` mas NÃO tem `users:user:anonymize`

**Ação**: `POST /api/usuarios/123/anonymize`

**Resultado Esperado**:
- ✅ Status: **403 Forbidden**
- ✅ Erro: "Você não tem permissão para anonimizar usuários"

---

#### CT-026: Super Admin Pode Deletar Outro Super Admin
**Cenário**: Existem 2+ Super Admins

**Resultado Esperado**:
- ✅ Status: 200 OK
- ✅ Desativação permitida (não é o último)

---

#### CT-027: Logs Preservados Após Desativação
**Validação SQL**:
```sql
SELECT COUNT(*) FROM AuditLogs WHERE PerformedBy = '123'
```

**Resultado Esperado**:
- ✅ Logs NÃO são deletados
- ✅ Referência ao usuário mantida
- ✅ Query funciona mesmo com usuário inativo

---

#### CT-028: Reativar Requer Mesma Permissão
**Ação**: `POST /api/usuarios/123/reativar`

**Validação**: Usuário deve ter `users:user:update` (ou `delete`)

**Resultado Esperado**:
- ✅ Sem permissão: 403 Forbidden

---

#### CT-029: Não Deletar Usuário de Sistema
**Cenário**: Usuário com flag `isSystemUser = true` (ex: "Sistema", "API")

**Resultado Esperado**:
- ✅ Status: **400 Bad Request**
- ✅ Erro: "Usuários de sistema não podem ser desativados"

---

#### CT-030: Mass Delete - Validação de Permissões
**Ação**: Desativar 10 usuários em lote

**Resultado Esperado**:
- ✅ Valida permissão para CADA usuário
- ✅ Se 1 falhar por hierarquia, continua os outros
- ✅ Retorna: "8 desativados, 2 falharam"

---

### Categoria 3: LGPD/GDPR Compliance (15 cenários)

#### CT-031: Anonimizar - Caminho Feliz
**Ação**:
```http
POST /api/usuarios/123/anonymize
Authorization: Bearer {admin-token}
{
  "confirmacao": "CONFIRMAR ANONIMIZAÇÃO"
}
```

**Resultado Esperado**:
- ✅ Status: 200 OK
- ✅ Banco:
  ```sql
  UPDATE Usuarios SET
    Nome = '[DADOS REMOVIDOS]',
    Email = 'anon-6bd3ebf2-0998-4f2b-889c-b5630c05ddc3@sistema.local',
    Telefone = NULL,
    CPF = NULL,
    DataNascimento = NULL,
    Foto = NULL,
    IsAnonimizado = 1,
    DataAnonimizacao = NOW(),
    AnonimizadoPorId = '{admin-id}',
    Ativo = 0
  WHERE Id = '123'
  ```
- ✅ Audit log especial: `action = "LGPD_ANONYMIZATION"`

---

#### CT-032: Anonimizar - Sem Confirmação
**Ação**: `{ "confirmacao": "confirmar" }` (texto errado)

**Resultado Esperado**:
- ✅ Status: **400 Bad Request**
- ✅ Erro: "Digite exatamente 'CONFIRMAR ANONIMIZAÇÃO' para prosseguir"

---

#### CT-033: Anonimizar - Usuário Já Anonimizado
**Ação**: Tentar anonimizar usuário com `isAnonimizado = true`

**Resultado Esperado**:
- ✅ Status: **400 Bad Request**
- ✅ Erro: "Este usuário já foi anonimizado"

---

#### CT-034: Anonimizar - Email Único
**Problema**: Gerar email anônimo único para evitar conflitos

**Estratégia**: `anon-{userId-guid}@sistema.local`

**Resultado Esperado**:
- ✅ Email único garantido (usa ID do usuário)
- ✅ Não quebra constraint UNIQUE em Email

---

#### CT-035: Anonimizar - Preservar Logs de Auditoria
**Validação SQL**:
```sql
SELECT * FROM AuditLogs WHERE PerformedBy = '123'
```

**Resultado Esperado**:
- ✅ Logs preservados (obrigação legal - Art. 19 LGPD)
- ✅ Campo `performedByName` pode ser atualizado para "[Usuário Removido]" (opcional)
- ✅ `performedBy` (ID) mantido para rastreabilidade

---

#### CT-036: Anonimizar - Preservar ID do Usuário
**Resultado Esperado**:
- ✅ `id` do usuário NÃO muda
- ✅ Foreign keys continuam funcionando
- ✅ Documentos criados por ele ainda referenciam corretamente

---

#### CT-037: Anonimizar - Documentos Criados
**Cenário**: João criou 50 documentos

**Resultado Esperado**:
- ✅ Documentos NÃO são deletados
- ✅ `criadoPorId` mantido (referência técnica)
- ✅ Interface exibe: "Criado por: [Usuário Removido]"

---

#### CT-038: Anonimizar - Não Pode Ser Revertido
**Ação**: `POST /api/usuarios/123/reativar` (usuário anonimizado)

**Resultado Esperado**:
- ✅ Status: **400 Bad Request**
- ✅ Erro: "Usuários anonimizados não podem ser reativados"

---

#### CT-039: Anonimizar - Foto de Perfil Deletada
**Resultado Esperado**:
- ✅ Arquivo físico deletado: `DELETE /storage/avatars/{userId}.jpg`
- ✅ Campo `foto` = NULL
- ✅ Interface exibe avatar padrão

---

#### CT-040: LGPD - Prazo de Atendimento
**Regra**: LGPD exige resposta em até 15 dias

**Validação**:
- ✅ Sistema registra data da solicitação
- ✅ Dashboard admin mostra "Solicitações LGPD Pendentes"
- ✅ Alerta se > 10 dias sem atendimento

---

#### CT-041: LGPD - Confirmação ao Solicitante
**Resultado Esperado**:
- ✅ Email enviado ao usuário (se email fornecido):
  ```
  Assunto: Confirmação de Exclusão de Dados (LGPD)

  Seus dados pessoais foram removidos do sistema IControlIT
  conforme solicitado (Art. 18, LGPD Lei 13.709/2018).

  Data da exclusão: 20/10/2025
  Protocolo: LGPD-2025-00123

  Logs de auditoria foram preservados conforme Art. 19 da LGPD.
  ```

---

#### CT-042: GDPR - Right to Be Forgotten (Europa)
**Diferença**: GDPR pode exigir hard delete em alguns casos

**Resultado Esperado**:
- ✅ Mesma implementação que LGPD
- ✅ Se hard delete necessário: Endpoint separado `POST /api/usuarios/{id}/gdpr-erase`

---

#### CT-043: Relatório de Dados (LGPD Art. 18)
**Funcionalidade**: Antes de deletar, usuário pode solicitar cópia de seus dados

**Ação**: `GET /api/usuarios/123/export-data`

**Resultado Esperado**:
- ✅ Arquivo JSON com TODOS os dados do usuário
- ✅ Inclui: perfil, documentos criados, logs de acesso
- ✅ Download: `joao-silva-dados-2025-10-20.json`

---

#### CT-044: Menores de Idade (LGPD Art. 14)
**Regra**: Dados de menores têm proteção especial

**Resultado Esperado**:
- ✅ Se `dataNascimento < 18 anos`: Anonimização automática após 5 anos de inatividade
- ✅ Notificação ao responsável legal

---

#### CT-045: Retention Policy - Auto-Anonimização
**Regra de Negócio**: Usuários inativos por > 7 anos são anonimizados automaticamente

**Resultado Esperado**:
- ✅ Job diário verifica: `DataDesativacao < NOW() - 7 anos`
- ✅ Anonimiza automaticamente
- ✅ Email de notificação 30 dias antes

---

### Categoria 4: Integridade Referencial (10 cenários)

#### CT-046: Documentos Criados - Preservados
**Cenário**: João criou 50 documentos

**Validação SQL**:
```sql
SELECT COUNT(*) FROM Documentos WHERE CriadoPorId = '123'
```

**Resultado Esperado**:
- ✅ 50 documentos ainda existem após desativação
- ✅ Query funciona normalmente
- ✅ Interface exibe: "Criado por João Silva (inativo)"

---

#### CT-047: Documentos - Impedir Exclusão se Documentos Ativos
**Regra de Negócio**: Não pode desativar usuário com documentos "Em Processamento"

**Validação**:
```sql
SELECT COUNT(*) FROM Documentos
WHERE CriadoPorId = '123' AND Status = 'EmProcessamento'
```

**Resultado Esperado**:
- ✅ Status: **400 Bad Request**
- ✅ Erro: "Este usuário possui 5 documentos em processamento"
- ✅ Link: "Ver documentos" → `/documents?createdBy=123&status=processing`

---

#### CT-048: Roles - Remover Associações
**Validação SQL**:
```sql
DELETE FROM UsuarioRoles WHERE UsuarioId = '123'
```

**Resultado Esperado**:
- ✅ Associações removidas ao desativar (opcional)
- ✅ OU mantidas para histórico (recomendado)

---

#### CT-049: Empresas - Não Deletar se Único Usuário
**Cenário**: João é o único usuário da Empresa ABC

**Resultado Esperado**:
- ✅ Status: **400 Bad Request**
- ✅ Erro: "Este é o único usuário da empresa ABC"
- ✅ Solução: "Desative a empresa primeiro" ou "Adicione outro usuário"

---

#### CT-050: Cascata - Não Deletar Templates Criados
**Resultado Esperado**:
- ✅ Templates criados por João são preservados
- ✅ Campo `criadoPorId` mantido

---

#### CT-051: Foreign Key Constraints
**Validação**: Verificar constraints no banco

**Resultado Esperado**:
- ✅ `Documentos.CriadoPorId` → `Usuarios.Id` (ON DELETE NO ACTION)
- ✅ `AuditLogs.PerformedBy` → `Usuarios.Id` (ON DELETE NO ACTION)
- ✅ Nenhuma cascade delete configurada

---

#### CT-052: Comentários em Documentos
**Cenário**: João fez 100 comentários em documentos

**Resultado Esperado**:
- ✅ Comentários preservados
- ✅ Interface: "João Silva (inativo)"

---

#### CT-053: Transferir Propriedade - Batch
**Funcionalidade**: `POST /api/usuarios/123/transfer-ownership`

**Payload**:
```json
{
  "novoProprietarioId": "maria-id",
  "transferirDocumentos": true,
  "transferirTemplates": true
}
```

**Resultado Esperado**:
- ✅ 50 documentos transferidos
- ✅ 10 templates transferidos
- ✅ Audit log registra transferência
- ✅ Então desativa João

---

#### CT-054: Dependências Circulares
**Cenário**: João é "DesativadoPor" de outros usuários

**Validação**:
```sql
SELECT * FROM Usuarios WHERE DesativadoPorId = '123'
```

**Resultado Esperado**:
- ✅ Dados preservados (FK válida)
- ✅ Query funciona mesmo com João inativo

---

#### CT-055: Sessions/Tokens na Tabela
**Cenário**: Tokens JWT armazenados em tabela (não só Redis)

**Resultado Esperado**:
- ✅ `DELETE FROM UserTokens WHERE UserId = '123'`
- ✅ Todas as sessões invalidadas

---

### Categoria 5: UX e Performance (15 cenários)

#### CT-056: Confirmação Modal - UX
**Resultado Esperado**:
- ✅ Modal com ícone de alerta ⚠️
- ✅ Nome do usuário em destaque
- ✅ Consequências listadas claramente
- ✅ Botão "Desativar" em vermelho
- ✅ Botão "Cancelar" em cinza (default focus)

---

#### CT-057: Loading State Durante Desativação
**Resultado Esperado**:
- ✅ Botão "Desativar" mostra spinner
- ✅ Texto: "Desativando..."
- ✅ Botão desabilitado (previne duplo clique)

---

#### CT-058: Toast de Sucesso
**Resultado Esperado**:
- ✅ Toast verde com ✓
- ✅ Mensagem: "João Silva foi desativado"
- ✅ Ação: "Desfazer" (se implementado)
- ✅ Auto-dismiss em 5 segundos

---

#### CT-059: Toast de Erro
**Resultado Esperado**:
- ✅ Toast vermelho com ✗
- ✅ Mensagem: "Erro ao desativar usuário: {motivo}"
- ✅ Botão "Tentar novamente"
- ✅ Não auto-dismiss (requer ação do usuário)

---

#### CT-060: Animação de Remoção da Lista
**Resultado Esperado**:
- ✅ Linha fade out (500ms)
- ✅ Linhas abaixo sobem suavemente
- ✅ UX suave, não abrupta

---

#### CT-061: Undo/Desfazer (Opcional)
**Funcionalidade**: Reverter desativação nos próximos 10 segundos

**Resultado Esperado**:
- ✅ Toast com botão "Desfazer"
- ✅ Se clicar: `POST /api/usuarios/123/reativar`
- ✅ Se não clicar em 10s: Desativação confirmada

---

#### CT-062: Performance - Desativar 1 Usuário
**Resultado Esperado**:
- ✅ Response time < 500ms
- ✅ SQL: `UPDATE Usuarios SET Ativo = 0 WHERE Id = '123'` (1 query)

---

#### CT-063: Performance - Desativar 100 Usuários (Batch)
**Ação**: `POST /api/usuarios/batch-delete`

**Payload**:
```json
{
  "userIds": ["id1", "id2", ..., "id100"],
  "motivo": "Rescisão em massa"
}
```

**Resultado Esperado**:
- ✅ Response time < 5 segundos
- ✅ SQL bulk update:
  ```sql
  UPDATE Usuarios SET Ativo = 0, DataDesativacao = NOW()
  WHERE Id IN ('id1', 'id2', ..., 'id100')
  ```
- ✅ Audit log batch (não 100 logs individuais)

---

#### CT-064: Performance - Invalidar Tokens (Redis)
**Resultado Esperado**:
- ✅ Operação Redis < 50ms
- ✅ Não bloqueia response do DELETE
- ✅ Assíncrono (fire-and-forget)

---

#### CT-065: Performance - Envio de Email Assíncrono
**Resultado Esperado**:
- ✅ Email enfileirado (RabbitMQ/Hangfire)
- ✅ Request retorna antes do envio
- ✅ Falha no email não bloqueia desativação

---

#### CT-066: Cache Invalidation
**Resultado Esperado**:
- ✅ Cache do usuário deletado: `DEL cache:user:123`
- ✅ Cache da lista: `DEL cache:users:list:*`
- ✅ Próxima requisição busca dados atualizados

---

#### CT-067: Acessibilidade - Confirmação por Teclado
**Resultado Esperado**:
- ✅ Modal acessível por Tab
- ✅ Enter no botão "Desativar" confirma
- ✅ Esc fecha modal
- ✅ Screen reader anuncia: "Confirmar desativação de João Silva"

---

#### CT-068: Mobile - Confirmação em Tela Pequena
**Resultado Esperado**:
- ✅ Modal ocupa 90% da tela
- ✅ Botões grandes (touch-friendly)
- ✅ Scroll se conteúdo não couber

---

#### CT-069: Feedback Visual - Usuário Inativo na Lista
**Resultado Esperado**:
- ✅ Linha com opacity 50%
- ✅ Badge "INATIVO" em cinza
- ✅ Tooltip: "Desativado em 20/10/2025 por Maria Admin"

---

#### CT-070: Histórico de Desativações
**Funcionalidade**: Admin pode ver todos os usuários desativados no último mês

**Ação**: `GET /api/usuarios?ativo=false&dataDesativacao>=2025-09-20`

**Resultado Esperado**:
- ✅ Lista filtrada
- ✅ Ordenação por `dataDesativacao` DESC
- ✅ Exportável para CSV (relatório)

---

## 🔒 Matriz de Permissões

| Perfil | Desativar Próprio | Desativar Subordinados | Desativar Qualquer | Anonimizar | Reativar |
|--------|------------------|------------------------|-------------------|------------|----------|
| **Super Admin** | ❌ | ✅ | ✅ (exceto último SA) | ✅ | ✅ |
| **Admin** | ❌ | ✅ Mesma empresa | ✅ Mesma empresa | ✅ | ✅ |
| **Gerente** | ❌ | ✅ Hierarquia inferior | ❌ | ❌ | ❌ |
| **Usuário** | ❌ | ❌ | ❌ | ❌ | ❌ |

---

## 📈 Critérios de Aceitação

### Backend
- [ ] Endpoint `DELETE /api/usuarios/{id}` com soft delete
- [ ] Endpoint `POST /api/usuarios/{id}/anonymize` (LGPD)
- [ ] Endpoint `POST /api/usuarios/{id}/reativar`
- [ ] Validação: Não pode auto-deletar
- [ ] Validação: Último Super Admin bloqueado
- [ ] Validação: Hierarquia respeitada
- [ ] Invalidação de tokens JWT (Redis blacklist)
- [ ] Email de notificação assíncrono
- [ ] Audit log completo (quem, quando, por quê)
- [ ] Response time < 500ms

### Frontend
- [ ] Modal de confirmação com consequências claras
- [ ] Campo opcional "Motivo"
- [ ] Confirmação especial para anonimização (digitar frase)
- [ ] Loading state durante operação
- [ ] Toast de sucesso/erro
- [ ] Animação de remoção da lista
- [ ] Botão "Desativar" só aparece se autorizado
- [ ] Badge "INATIVO" em usuários desativados
- [ ] Filtro "Ativos/Inativos/Todos"
- [ ] Acessibilidade (teclado, screen reader)

---

## 🧩 Dependências

### Backend
- `UsuariosController.Delete(id)` ✅ Implementado
- `UsuariosController.Anonymize(id)` ⚠️ Verificar
- `UsuariosController.Reativar(id)` ⚠️ Verificar
- `AuthorizationService` ✅ Implementado
- `TokenRevocationService` ⚠️ Implementar
- `AuditLogService` ✅ Implementado
- `EmailService` ✅ Implementado

### Frontend
- `UsersListComponent` ✅ Implementado
- `UsersService.deleteUser()` ✅ Implementado
- `ConfirmationDialogComponent` ✅ Implementado
- `PermissionDirective` ✅ Implementado

---

## 📝 Notas de Implementação

### Soft Delete Pattern
```csharp
public class Usuario
{
    public bool Ativo { get; set; } = true;
    public DateTime? DataDesativacao { get; set; }
    public string? DesativadoPorId { get; set; }
    public string? MotivoDesativacao { get; set; }
    public bool IsAnonimizado { get; set; } = false;
}

// Global query filter (EF Core)
modelBuilder.Entity<Usuario>()
    .HasQueryFilter(u => !u.IsAnonimizado); // Oculta anonimizados por padrão
```

### Token Revocation (Redis)
```csharp
public async Task InvalidateUserTokens(string userId)
{
    var key = $"blacklist:user:{userId}";
    await _redis.SetAsync(key, "revoked", TimeSpan.FromDays(1));
}

// Middleware valida token
var isBlacklisted = await _redis.ExistsAsync($"blacklist:user:{userId}");
if (isBlacklisted) return Unauthorized();
```

### LGPD Anonymization
```csharp
public async Task AnonymizeUser(string userId)
{
    var user = await _context.Usuarios.FindAsync(userId);
    user.Nome = "[DADOS REMOVIDOS]";
    user.Email = $"anon-{userId}@sistema.local";
    user.Telefone = null;
    user.CPF = null;
    user.Foto = null;
    user.IsAnonimizado = true;
    user.DataAnonimizacao = DateTime.UtcNow;
    user.Ativo = false;

    await _context.SaveChangesAsync();
    await _auditLog.LogAnonymization(userId);
}
```

---

## ✅ Checklist de Completude

- [x] Todos os fluxos documentados (4 alternativos, 12 exceção)
- [x] 70 cenários de teste criados
- [x] LGPD/GDPR compliance (15 cenários)
- [x] Integridade referencial (10 cenários)
- [x] Segurança (20 cenários)
- [x] UX/Performance (15 cenários)
- [x] Matriz de permissões
- [x] Critérios de aceitação
- [x] Notas de implementação

---

**Status Final**: ✅ **UC04 100% ESPECIFICADO**

**Complexidade**: 🔴 Crítica (operação irreversível com implicações legais)

**Próximos Passos**:
1. Implementar token revocation (Redis)
2. Implementar endpoint de anonimização LGPD
3. Criar job de auto-anonimização (retention policy)
4. Testes de integridade referencial
5. Executar todos os 70 cenários de teste

**Última Atualização**: 2025-10-20
**Revisado por**: Anderson Chipak + Claude Code

---

# UC08 - Gerenciar Usuários do Perfil
## 📋 Objetivo
Permitir que administradores adicionem ou removam usuários em lote ao/do perfil, respeitando o limite máximo de usuários permitidos e mantendo controle sobre atribuições.

## 👤 Atores
- Ator Principal: Administrador com permissão perfis:perfil:update e usuarios:usuario:update
- Atores Secundários: Sistema de Cache (invalida cache de usuários)

## 🎯 Pré-condições
- ☒ Usuário autenticado no sistema
- ☒ Usuário possui permissões necessárias
- ☒ Perfil existe e é editável
- ☒ Usuários a adicionar/remover existem

## ▶️ Fluxo Principal
- Usuário acessa aba “Usuários” no detalhes do perfil
- Sistema exibe:
- Grid de usuários atualmente com perfil (paginado)
- Contador: “{n} de {MaxUsuarios} usuários” (se houver limite)
- Botão “+ Adicionar Usuários” (se não atingiu limite)
- Checkbox para seleção em lote
- Para adicionar:
- Usuário clica “+ Adicionar Usuários”
- Sistema abre modal com lista de usuários sem este perfil
- Usuário seleciona 1 ou mais usuários (checkbox múltiplo)
- Sistema valida limite: count(atuais) + count(selecionados) <= MaxUsuarios
- Usuário clica “Adicionar”
- Sistema vincula usuários ao perfil em tabela UsuarioRole
- Sistema invalida cache Redis de permissões dos usuários
- Sistema registra auditoria
- Resultado: Usuários adicionados com sucesso
Para remover: 1. Usuário seleciona usuários na grid (checkbox) 2. Clica “Remover Selecionados” 3. Sistema exibe confirmação 4. Remove vinculação na tabela UsuarioRole 5. Atualiza cache e auditoria

## 🔀 Fluxos Alternativos
### FA01 - Adicionar um Usuário por Vez
Usuário clica em ícone “+” ao lado de usuário específico na modal.
### FA02 - Remover um Usuário por Vez
Usuário clica em ícone “X” ao lado de usuário na grid para remover individual.
### FA03 - Filtrar Usuários Disponíveis
Usuário digita nome/matrícula para filtrar lista de usuários a adicionar.

## ⚠️ Fluxos de Exceção
### FE01 - Limite de Usuários Atingido
Sistema detecta que count + novos > MaxUsuarios e exibe: “Limite de {MaxUsuarios} usuários atingido. {n} espaços disponíveis. Remova usuários antes de adicionar.”
### FE02 - Aviso 80% do Limite
Ao atingir 80%, sistema exibe alerta: “Você atingiu 80% do limite de usuários ({8}/{10}).”
### FE03 - Usuário Já Possui Perfil
Sistema detecta duplicata e exibe: “Usuário {nome} já possui este perfil.”
### FE04 - Usuário Inativo
Sistema permite adicionar usuário inativo mas exibe aviso.

## ✅ Pós-condições
- ✅ Usuários vinculados/desvinculados do perfil
- ✅ Contagem de usuários atualizada
- ✅ Cache Redis invalidado para usuários modificados
- ✅ Auditoria registrada com lista de usuários modificados

## 📐 Regras de Negócio

## 🧪 Cenários de Teste
- CEN801 - Adicionar 1 usuário ao perfil
- CEN802 - Adicionar múltiplos usuários em lote
- CEN803 - Tentar adicionar quando atingiu limite (HTTP 400)
- CEN804 - Remover 1 usuário da grid
- CEN805 - Remover múltiplos usuários em lote
- CEN806 - Adicionar usuário que já possui perfil (detecta duplicata)
- CEN807 - Atingir 80% do limite (mostra alerta)
- CEN808 - Filtrar usuários disponíveis por nome
- CEN809 - Verificar que cache foi invalidado
- CEN810 - Tentar gerenciar sem permissão perfis:perfil:update (HTTP 403)
Total: 10 cenários | Status: Documentado

## 📊 Rastreabilidade

Última Atualização: 2025-11-06

---

## Histórico de Alterações

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 1.0 | 2025-12-17 | Sistema | Consolidação de 6 casos de uso |
