# UC-RF083 — Casos de Uso Canônicos

**RF:** RF083 — Central de Módulos
**Versão:** 2.0
**Data:** 2026-01-30
**Autor:** Agência ALC - alc.dev.br

---

## 1. OBJETIVO DO DOCUMENTO

Este documento descreve **todos os Casos de Uso (UC)** derivados do **RF083 - Central de Módulos**, cobrindo integralmente o comportamento funcional esperado.

Os UCs aqui definidos servem como **contrato comportamental**, sendo a **fonte primária** para geração de:
- Casos de Teste (TC-RF083.yaml)
- Massas de Teste (MT-RF083.yaml)
- Evidências de auditoria e validação funcional
- Execução por agentes de IA (tester, QA, E2E)

**Nota Especial:** A Central de Módulos é um módulo de **SISTEMA** com características especiais:
- Funcionalidades são **GLOBAIS** (não isoladas por tenant tradicional)
- Acesso filtrado por **perfil de usuário** (Developer, System, Tenant)
- **Pré-requisito** para todos os demais RFs do sistema
- Integração com RF117 (Gestão de Assinaturas) para controle baseado em planos comerciais

---

## 2. SUMÁRIO DE CASOS DE USO

| ID | Nome | Ator Principal | Tipo |
|----|------|----------------|------|
| UC00 | Listar Funcionalidades | Usuário Autenticado | Leitura |
| UC01 | Visualizar Funcionalidade | Usuário Autenticado | Leitura |
| UC02 | Listar Funcionalidades por Categoria | Usuário Autenticado | Leitura |
| UC03 | Obter Estatísticas | Usuário Autenticado | Leitura |
| UC04 | Gerenciar Empresas Exclusivas | Developer | Atualização |
| UC05 | Resetar Funcionalidades | Developer/Super Admin | Administração |
| UC06 | Expandir/Contrair Categorias | Usuário Autenticado | Interface |
| UC07 | Filtrar Funcionalidades | Usuário Autenticado | Leitura |

---

## 3. PADRÕES GERAIS APLICÁVEIS A TODOS OS UCs

- **Isolamento por perfil** (não por tenant): Developer (todas), System (Corporativo+Sistema), Tenant (apenas Corporativo)
- Todas as ações exigem **autenticação**
- Erros não devem vazar informações sensíveis
- Auditoria deve registrar **quem**, **quando** e **qual ação**
- Mensagens devem ser claras, previsíveis e rastreáveis
- Registros com `fl_excluido = true` não aparecem em listagens
- Validação de acesso considera ambiente atual (RN-RF083-21)
- Integração com RF117 para módulos que requerem assinatura (RN-RF083-22)

---

## UC00 — Listar Funcionalidades

### Objetivo
Permitir que o usuário visualize todas as funcionalidades do sistema conforme seu perfil de acesso.

### Pré-condições
- Usuário autenticado
- Permissão `central_modulos.view_any`

### Pós-condições
- Lista de funcionalidades exibida conforme perfil e filtros

### Fluxo Principal
- **FP-UC00-001:** Usuário acessa Central de Módulos pelo menu
- **FP-UC00-002:** Sistema valida autenticação
- **FP-UC00-003:** Sistema identifica perfil do usuário (Developer/System/Tenant)
- **FP-UC00-004:** Sistema aplica filtro por perfil (RN-RF083-02)
- **FP-UC00-005:** Sistema carrega funcionalidades ativas não excluídas
- **FP-UC00-006:** Sistema inclui ações associadas (se `incluirAcoes = true`)
- **FP-UC00-007:** Sistema inclui funcionalidades filhas (se `incluirFilhas = true`)
- **FP-UC00-008:** Sistema aplica ordenação (por `ordem`, depois por `nome`)
- **FP-UC00-009:** Sistema exibe a lista agrupada por categoria

### Fluxos Alternativos
- **FA-UC00-001:** Filtrar por categoria específica
- **FA-UC00-002:** Filtrar apenas funcionalidades ativas/inativas
- **FA-UC00-003:** Buscar por nome ou código

### Fluxos de Exceção
- **FE-UC00-001:** Usuário não autenticado → redirect para login
- **FE-UC00-002:** Nenhuma funcionalidade encontrada → estado vazio exibido

### Regras de Negócio
- RN-RF083-02: Isolamento por perfil de usuário
- RN-RF083-05: Soft delete (apenas `fl_excluido = false`)
- RN-RF083-11: Ordem de exibição

### Critérios de Aceite
- **CA-UC00-001:** Developer DEVE visualizar TODAS as funcionalidades
- **CA-UC00-002:** System DEVE visualizar apenas funcionalidades Corporativo + Sistema
- **CA-UC00-003:** Tenant DEVE visualizar apenas funcionalidades Corporativo
- **CA-UC00-004:** Funcionalidades excluídas (soft delete) NÃO devem aparecer
- **CA-UC00-005:** Ordenação DEVE ser por `ordem` ASC, depois `nome` ASC
- **CA-UC00-006:** Ações e filhas DEVEM ser incluídas quando solicitado

---

## UC01 — Visualizar Funcionalidade

### Objetivo
Permitir visualização detalhada de uma funcionalidade específica.

### Pré-condições
- Usuário autenticado
- Permissão `central_modulos.view`

### Pós-condições
- Detalhes da funcionalidade exibidos

### Fluxo Principal
- **FP-UC01-001:** Usuário seleciona funcionalidade na lista
- **FP-UC01-002:** Sistema valida autenticação
- **FP-UC01-003:** Sistema carrega funcionalidade por ID
- **FP-UC01-004:** Sistema verifica se funcionalidade existe e não está excluída
- **FP-UC01-005:** Sistema carrega ações associadas
- **FP-UC01-006:** Sistema carrega funcionalidades filhas
- **FP-UC01-007:** Sistema carrega empresas exclusivas
- **FP-UC01-008:** Sistema calcula estatísticas (total ações, ações ativas, usuários com acesso)
- **FP-UC01-009:** Sistema verifica estado da Feature Flag vinculada (se houver)
- **FP-UC01-010:** Sistema exibe detalhes completos

### Fluxos de Exceção
- **FE-UC01-001:** Funcionalidade não encontrada → 404 Not Found
- **FE-UC01-002:** Funcionalidade excluída → 404 Not Found

### Regras de Negócio
- RN-RF083-05: Soft delete (funcionalidade excluída retorna 404)
- RN-RF083-07: Vinculação com Feature Flag

### Critérios de Aceite
- **CA-UC01-001:** Sistema DEVE exibir código, nome, descrição, ícone, rota
- **CA-UC01-002:** Sistema DEVE exibir lista de ações com seus tipos
- **CA-UC01-003:** Sistema DEVE exibir lista de funcionalidades filhas
- **CA-UC01-004:** Sistema DEVE exibir empresas exclusivas (ou "Todas" se vazio)
- **CA-UC01-005:** Sistema DEVE exibir estado da Feature Flag vinculada
- **CA-UC01-006:** Sistema DEVE calcular total de ações e ações ativas
- **CA-UC01-007:** Funcionalidade inexistente DEVE retornar 404

---

## UC02 — Listar Funcionalidades por Categoria

### Objetivo
Permitir visualização de funcionalidades filtradas por categoria específica.

### Pré-condições
- Usuário autenticado
- Permissão `central_modulos.view_any`

### Pós-condições
- Lista filtrada por categoria exibida

### Fluxo Principal
- **FP-UC02-001:** Usuário seleciona categoria no filtro
- **FP-UC02-002:** Sistema valida autenticação
- **FP-UC02-003:** Sistema aplica filtro por perfil (RN-RF083-02)
- **FP-UC02-004:** Sistema carrega funcionalidades da categoria selecionada
- **FP-UC02-005:** Sistema aplica filtro de ativos/não excluídos
- **FP-UC02-006:** Sistema aplica ordenação
- **FP-UC02-007:** Sistema exibe lista filtrada

### Fluxos Alternativos
- **FA-UC02-001:** Limpar filtro de categoria (voltar para todas)

### Fluxos de Exceção
- **FE-UC02-001:** Categoria sem funcionalidades → estado vazio

### Regras de Negócio
- RN-RF083-02: Isolamento por perfil
- RN-RF083-05: Soft delete
- RN-RF083-12: Categoria via `categoria_id` (prioridade) ou `categoria` (legado)

### Critérios de Aceite
- **CA-UC02-001:** Filtro DEVE usar `categoria_id` quando disponível
- **CA-UC02-002:** Filtro DEVE fallback para campo `categoria` (legado)
- **CA-UC02-003:** Resultado DEVE respeitar isolamento por perfil
- **CA-UC02-004:** Estado vazio DEVE ser exibido quando categoria sem funcionalidades

---

## UC03 — Obter Estatísticas

### Objetivo
Permitir visualização de estatísticas agregadas das funcionalidades.

### Pré-condições
- Usuário autenticado
- Permissão `central_modulos.view_any`

### Pós-condições
- Estatísticas calculadas e exibidas

### Fluxo Principal
- **FP-UC03-001:** Usuário acessa área de estatísticas
- **FP-UC03-002:** Sistema valida autenticação
- **FP-UC03-003:** Sistema calcula total de funcionalidades (ativas, não excluídas)
- **FP-UC03-004:** Sistema calcula total de ações
- **FP-UC03-005:** Sistema agrupa funcionalidades por categoria
- **FP-UC03-006:** Sistema exibe dashboard com estatísticas

### Regras de Negócio
- RN-RF083-14: Estatísticas consideram apenas registros ativos e não excluídos

### Critérios de Aceite
- **CA-UC03-001:** Total geral DEVE considerar apenas `ativo = true` e `fl_excluido = false`
- **CA-UC03-002:** Contagem por categoria DEVE ser precisa
- **CA-UC03-003:** Total de ações DEVE ser exibido
- **CA-UC03-004:** Dashboard DEVE ser responsivo

---

## UC04 — Gerenciar Empresas Exclusivas

### Objetivo
Permitir que Developer defina quais empresas têm acesso exclusivo a uma funcionalidade.

### Pré-condições
- Usuário autenticado
- Perfil: Developer
- Permissão `central_modulos.manage_exclusives`

### Pós-condições
- Lista de empresas exclusivas atualizada
- Auditoria registrada

### Fluxo Principal
- **FP-UC04-001:** Developer acessa detalhes da funcionalidade
- **FP-UC04-002:** Sistema valida se usuário é Developer
- **FP-UC04-003:** Developer clica em "Gerenciar Empresas Exclusivas"
- **FP-UC04-004:** Sistema exibe modal com lista de empresas
- **FP-UC04-005:** Developer seleciona empresas com acesso exclusivo
- **FP-UC04-006:** Developer confirma alteração
- **FP-UC04-007:** Sistema valida IDs das empresas selecionadas
- **FP-UC04-008:** Sistema persiste alteração em `empresas_exclusivas_json`
- **FP-UC04-009:** Sistema registra auditoria
- **FP-UC04-010:** Sistema exibe confirmação de sucesso

### Fluxos Alternativos
- **FA-UC04-001:** Limpar exclusividade (disponibilizar para todas)
- **FA-UC04-002:** Cancelar operação

### Fluxos de Exceção
- **FE-UC04-001:** Usuário não é Developer → 403 Forbidden
- **FE-UC04-002:** Empresa inexistente → erro de validação
- **FE-UC04-003:** Funcionalidade não encontrada → 404 Not Found

### Regras de Negócio
- RN-RF083-03: Empresas exclusivas vazias = acesso total
- RN-RF083-04: Apenas Developer pode gerenciar empresas exclusivas
- RN-RF083-13: Auditoria obrigatória

### Critérios de Aceite
- **CA-UC04-001:** APENAS Developer DEVE poder acessar esta funcionalidade
- **CA-UC04-002:** Usuário não Developer DEVE receber 403 Forbidden
- **CA-UC04-003:** Array vazio DEVE disponibilizar para todas as empresas
- **CA-UC04-004:** IDs de empresas DEVEM ser validados antes de persistir
- **CA-UC04-005:** Auditoria DEVE registrar quem e quando alterou
- **CA-UC04-006:** Mensagem de sucesso DEVE ser exibida após alteração

---

## UC05 — Resetar Funcionalidades

### Objetivo
Permitir reset completo das funcionalidades com dados padrão (operação destrutiva).

### Pré-condições
- Usuário autenticado
- Perfil: Developer OU Super Admin
- Permissão `central_modulos.reset`

### Pós-condições
- Funcionalidades deletadas e recriadas com dados padrão
- Auditoria registrada

### Fluxo Principal
- **FP-UC05-001:** Usuário acessa área administrativa
- **FP-UC05-002:** Sistema valida se usuário é Developer ou Super Admin
- **FP-UC05-003:** Usuário clica em "Resetar Funcionalidades"
- **FP-UC05-004:** Sistema exibe alerta de operação destrutiva
- **FP-UC05-005:** Sistema solicita confirmação explícita (digitar "CONFIRMAR")
- **FP-UC05-006:** Usuário confirma operação
- **FP-UC05-007:** Sistema deleta todas as funcionalidades existentes
- **FP-UC05-008:** Sistema recria funcionalidades com dados padrão
- **FP-UC05-009:** Sistema registra auditoria
- **FP-UC05-010:** Sistema exibe resultado (quantidade de funcionalidades criadas)

### Fluxos Alternativos
- **FA-UC05-001:** Cancelar operação

### Fluxos de Exceção
- **FE-UC05-001:** Usuário não autorizado → 403 Forbidden
- **FE-UC05-002:** Erro durante reset → rollback e erro exibido

### Regras de Negócio
- RN-RF083-15: Reset é operação destrutiva, apenas Developer ou Super Admin

### Critérios de Aceite
- **CA-UC05-001:** APENAS Developer ou Super Admin DEVE poder executar
- **CA-UC05-002:** Sistema DEVE exigir confirmação explícita
- **CA-UC05-003:** Operação DEVE ser atômica (tudo ou nada)
- **CA-UC05-004:** Resultado DEVE informar quantidade de funcionalidades criadas
- **CA-UC05-005:** Auditoria DEVE registrar operação completa
- **CA-UC05-006:** 403 DEVE ser retornado para usuários não autorizados

---

## UC06 — Expandir/Contrair Categorias

### Objetivo
Permitir controle visual da expansão/contração de categorias na listagem.

### Pré-condições
- Usuário autenticado
- Lista de funcionalidades exibida

### Pós-condições
- Estado visual da categoria alterado

### Fluxo Principal
- **FP-UC06-001:** Usuário visualiza lista de funcionalidades por categoria
- **FP-UC06-002:** Usuário clica no ícone de expandir/contrair categoria
- **FP-UC06-003:** Sistema alterna estado visual (expandido ↔ contraído)
- **FP-UC06-004:** Sistema persiste preferência (opcional, localStorage)

### Fluxos Alternativos
- **FA-UC06-001:** Expandir todas as categorias
- **FA-UC06-002:** Contrair todas as categorias

### Critérios de Aceite
- **CA-UC06-001:** Click DEVE alternar estado expandido/contraído
- **CA-UC06-002:** Ícone DEVE refletir estado atual
- **CA-UC06-003:** Animação DEVE ser suave
- **CA-UC06-004:** Preferência PODE ser persistida em localStorage

---

## UC07 — Filtrar Funcionalidades

### Objetivo
Permitir filtragem avançada de funcionalidades por múltiplos critérios.

### Pré-condições
- Usuário autenticado
- Permissão `central_modulos.view_any`

### Pós-condições
- Lista filtrada conforme critérios

### Fluxo Principal
- **FP-UC07-001:** Usuário acessa Central de Módulos
- **FP-UC07-002:** Usuário aplica filtro por nome/código
- **FP-UC07-003:** Sistema filtra em tempo real (debounce)
- **FP-UC07-004:** Sistema exibe resultados filtrados
- **FP-UC07-005:** Sistema atualiza URL com parâmetros de filtro

### Fluxos Alternativos
- **FA-UC07-001:** Filtrar por status (ativo/inativo)
- **FA-UC07-002:** Filtrar por categoria
- **FA-UC07-003:** Limpar todos os filtros

### Regras de Negócio
- RN-RF083-02: Filtros respeitam isolamento por perfil

### Critérios de Aceite
- **CA-UC07-001:** Filtro por texto DEVE buscar em `codigo` e `nome`
- **CA-UC07-002:** Filtros DEVEM ser acumuláveis
- **CA-UC07-003:** URL DEVE refletir filtros aplicados
- **CA-UC07-004:** Limpar filtros DEVE restaurar lista completa

---

## 4. MATRIZ DE RASTREABILIDADE

| UC | Regras de Negócio | Endpoints | Funcionalidades CRUD |
|----|------------------|-----------|---------------------|
| UC00 | RN-RF083-02, RN-RF083-05, RN-RF083-11 | GET /api/funcionalidades | RF-CRUD-02 |
| UC01 | RN-RF083-05, RN-RF083-07 | GET /api/funcionalidades/{id} | RF-CRUD-03 |
| UC02 | RN-RF083-02, RN-RF083-05, RN-RF083-12 | GET /api/funcionalidades/categoria/{cat} | RF-CRUD-02.1 |
| UC03 | RN-RF083-14 | GET /api/funcionalidades/estatisticas | RF-CRUD-06 |
| UC04 | RN-RF083-03, RN-RF083-04, RN-RF083-13 | PUT /api/funcionalidades/{id}/empresas-exclusivas | RF-CRUD-04.1 |
| UC05 | RN-RF083-15 | POST /api/funcionalidades/reset | RF-ADMIN-01 |
| UC06 | - | - (UI apenas) | - |
| UC07 | RN-RF083-02 | GET /api/funcionalidades (com params) | RF-CRUD-02 |

---

## 5. COBERTURA DE REGRAS DE NEGÓCIO

| Regra | Descrição | UCs que cobrem |
|-------|-----------|----------------|
| RN-RF083-01 | Código único de funcionalidade | (Criação não exposta via UI) |
| RN-RF083-02 | Isolamento por perfil de usuário | UC00, UC02, UC07 |
| RN-RF083-03 | Empresas exclusivas vazias = acesso total | UC04 |
| RN-RF083-04 | Apenas Developer gerencia exclusivas | UC04 |
| RN-RF083-05 | Soft delete obrigatório | UC00, UC01, UC02 |
| RN-RF083-06 | Hierarquia de funcionalidades | UC00, UC01 |
| RN-RF083-07 | Vinculação com Feature Flag | UC01 |
| RN-RF083-08 | Ações pertencem a funcionalidade | UC01 |
| RN-RF083-09 | Código de ação padrão | UC01 |
| RN-RF083-10 | Tipos de ação padronizados | UC01 |
| RN-RF083-11 | Ordem de exibição | UC00 |
| RN-RF083-12 | Categoria textual legada | UC02 |
| RN-RF083-13 | Auditoria obrigatória | UC04, UC05 |
| RN-RF083-14 | Estatísticas (ativos, não excluídos) | UC03 |
| RN-RF083-15 | Reset é operação destrutiva | UC05 |
| RN-RF083-16 | Redirect para vendas | (Integração RF117) |
| RN-RF083-17 | Dependências circulares proibidas | (Validação interna) |
| RN-RF083-18 | Desativar módulo desativa dependentes | (Validação interna) |
| RN-RF083-19 | Ativar módulo ativa dependências | (Validação interna) |
| RN-RF083-20 | Planos incluem dependências | (Integração RF117) |
| RN-RF083-21 | Controle por ambiente | UC00, UC01 |
| RN-RF083-22 | Integração com Gestão de Assinaturas | UC00, UC01 |

---

## CHANGELOG

| Versão | Data | Autor | Descrição |
|------|------|-------|-----------|
| 2.0 | 2026-01-30 | Agência ALC - alc.dev.br | Versão inicial - 8 UCs cobrindo funcionalidades de leitura, administração e interface |
