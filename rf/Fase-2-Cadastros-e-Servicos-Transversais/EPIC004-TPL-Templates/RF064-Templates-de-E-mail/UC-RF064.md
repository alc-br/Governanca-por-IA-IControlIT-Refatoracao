# UC-RF064 — Casos de Uso Canônicos

**RF:** RF064 — Templates de E-mail
**Fase:** Fase 2 - Cadastros e Serviços Transversais
**Epic:** EPIC004-TPL-Templates
**Versão:** 2.0
**Data:** 2025-12-31
**Autor:** Agência ALC - alc.dev.br

---

## 1. OBJETIVO DO DOCUMENTO

Este documento descreve todos os Casos de Uso (UC) derivados do **RF064 - Templates de E-mail**.

O objetivo é permitir que o sistema gerencie templates de e-mail responsivos, personalizáveis e rastreáveis, com teste A/B automático, compatibilidade multi-cliente, métricas de engajamento e conformidade legal (LGPD/CAN-SPAM).

Este documento é a **especificação comportamental canônica** do RF064 e deve ser sincronizado com o arquivo **UC-RF064.yaml** (estrutura de dados).

---

## 2. SUMÁRIO DE CASOS DE USO

| ID   | Nome                                | Ator Principal        | Tipo       |
|------|-------------------------------------|-----------------------|------------|
| UC00 | Listar Templates de E-mail          | Usuário Autenticado   | Leitura    |
| UC01 | Criar Template de E-mail            | Admin, Marketing      | Escrita    |
| UC02 | Visualizar Template de E-mail       | Usuário Autenticado   | Leitura    |
| UC03 | Editar Template de E-mail           | Admin, Marketing      | Escrita    |
| UC04 | Inativar Template de E-mail         | Admin                 | Escrita    |

---

## 3. PADRÕES GERAIS APLICÁVEIS A TODOS OS UCs

### 3.1 Autenticação e Autorização

- **Autenticação**: Todos os UCs exigem Bearer Token JWT válido
- **Autorização**: Permissões RBAC (`TPL.EMAIL.*`) verificadas antes de cada operação
- **Multi-tenancy**: Isolamento por `EmpresaId` (usuário só acessa templates da sua empresa)
- **Templates globais**: Templates com `TemplateBase = true` são visíveis por todas as empresas

### 3.2 Validações de Entrada

- **Sanitização XSS**: HTML gerado de MJML é sanitizado para prevenir XSS
- **Tamanho máximo**: MJML limitado a 100KB
- **Validação de formato**: JSON Schema validado conforme JSON Schema Draft 7
- **Compilação MJML**: Template deve compilar sem erros antes de salvar

### 3.3 Tratamento de Erros

| Código HTTP | Descrição | Quando Ocorre |
|-------------|-----------|---------------|
| 400 Bad Request | Validação falhou | MJML inválido, JSON Schema incorreto, campos obrigatórios vazios |
| 401 Unauthorized | Token ausente/inválido | Bearer Token expirado ou ausente |
| 403 Forbidden | Sem permissão | Usuário sem permissão `TPL.EMAIL.*` correspondente |
| 404 Not Found | Recurso não encontrado | Template ID inexistente |
| 409 Conflict | Conflito de dados | Nome duplicado no conglomerado |
| 500 Internal Server Error | Erro inesperado | Falha na compilação MJML, erro de banco |

### 3.4 Auditoria

Todos os UCs que modificam dados registram:
- `Created` / `CreatedBy` (criação)
- `LastModified` / `LastModifiedBy` (modificação)
- Timestamp com precisão de milissegundos
- IP do usuário e User-Agent (header HTTP)

### 3.5 Paginação e Filtros (UC00)

- **Paginação**: `pageIndex` (base 0), `pageSize` (default 20, max 100)
- **Ordenação**: `sortBy` (campo), `sortDirection` (asc/desc)
- **Filtros**: Por empresa, categoria, status (ativo/inativo)
- **Pesquisa**: Busca por nome (case-insensitive, partial match)

### 3.6 Soft Delete

- Templates nunca são deletados fisicamente (preservar histórico)
- Flag `IsDeleted` marca remoção lógica
- Queries padrão filtram `IsDeleted = false` automaticamente

---

## UC00 — Listar Templates de E-mail

### Objetivo

Exibir lista paginada e filtrável de templates de e-mail, permitindo busca por nome, filtro por categoria, status e ordenação customizada.

### Pré-condições

- Usuário autenticado no sistema
- Usuário possui permissão `TPL.EMAIL.VIEW_ANY`

### Pós-condições

- Lista de templates retornada com paginação
- Apenas templates do conglomerado do usuário + templates globais
- Templates inativos (`Ativo = false`) não exibidos por padrão

### Gatilho

Usuário acessa menu "Templates > E-mail" ou endpoint `/api/templates-email`.

### Fluxo Principal

| Passo | Ator    | Ação                                  | Sistema                                      |
|-------|---------|---------------------------------------|----------------------------------------------|
| 1     | Usuário | Acessa menu "Templates de E-mail"     | Carrega listagem paginada (20 por página)   |
| 2     | Sistema | Consulta banco de dados               | Filtra por `EmpresaId` + templates globais  |
| 3     | Sistema | Retorna lista de templates            | Exibe: Nome, Tipo, Status, Versão, Última modificação |
| 4     | Usuário | (Opcional) Aplica filtros/busca       | Recarrega lista com filtros aplicados       |
| 5     | Usuário | (Opcional) Ordena por coluna          | Reordena lista conforme critério            |

**Resultado**: Usuário visualiza templates disponíveis.

### Fluxos Alternativos

#### FA-UC00-001: Pesquisar por Nome
- **Quando**: Usuário digita no campo de busca
- **Sistema**: Filtra templates cujo nome contém texto digitado (case-insensitive)
- **Retorna ao passo 4**

#### FA-UC00-002: Filtrar por Categoria
- **Quando**: Usuário seleciona categoria (Transacional/Marketing/Notificação)
- **Sistema**: Exibe apenas templates da categoria selecionada
- **Retorna ao passo 4**

#### FA-UC00-003: Filtrar por Status
- **Quando**: Usuário filtra por "Ativo" ou "Inativo"
- **Sistema**: Exibe apenas templates com status selecionado
- **Retorna ao passo 4**

#### FA-UC00-004: Ordenar Resultados
- **Quando**: Usuário clica em cabeçalho de coluna (Nome/Tipo/Data)
- **Sistema**: Reordena lista (asc/desc alternado)
- **Retorna ao passo 4**

### Fluxos de Exceção

#### FE-UC00-001: Sem Permissão
- **Quando**: Usuário sem `TPL.EMAIL.VIEW_ANY`
- **Resposta**: HTTP 403 Forbidden
- **Mensagem**: "Você não tem permissão para listar templates de e-mail"

#### FE-UC00-002: Erro de Comunicação
- **Quando**: Falha na consulta ao banco
- **Resposta**: HTTP 500 Internal Server Error
- **Mensagem**: "Erro ao carregar lista de templates. Tente novamente."

#### FE-UC00-003: Nenhum Resultado Encontrado
- **Quando**: Filtros não retornam resultados
- **Resposta**: HTTP 200 OK com lista vazia
- **Mensagem UI**: "Nenhum template encontrado. Ajuste os filtros ou crie um novo template."

### Regras de Negócio Aplicadas

- **RN-RF064-005**: Branding customizado por empresa (exibir logo/cor na listagem)
- **RN-RF064-016**: Unicidade de nome por empresa (verificar duplicatas)

### Critérios de Aceite

- ✅ Lista carrega em menos de 2 segundos (até 1000 templates)
- ✅ Filtros aplicam em tempo real (< 500ms)
- ✅ Paginação funciona corretamente (20 itens por página)
- ✅ Busca por nome encontra matches parciais
- ✅ Multi-tenancy respeitado (não exibir templates de outras empresas)
- ✅ Templates globais visíveis para todas as empresas

---

## UC01 — Criar Template de E-mail

### Objetivo

Permitir criação de novo template de e-mail com MJML responsivo, JSON Schema de variáveis, configurações de tracking e branding customizado.

### Pré-condições

- Usuário autenticado no sistema
- Usuário possui permissão `TPL.EMAIL.CREATE`
- Biblioteca MJML configurada no backend
- Monaco Editor configurado no frontend

### Pós-condições

- Template criado com status `Rascunho`
- Primeira versão (`v1.0.0`) registrada
- HTML compilado de MJML armazenado
- Auditoria registrada

### Gatilho

Usuário clica em "Novo Template" na listagem.

### Fluxo Principal

| Passo | Ator    | Ação                                      | Sistema                                          |
|-------|---------|-------------------------------------------|--------------------------------------------------|
| 1     | Usuário | Clica em "Novo Template"                  | Abre formulário de criação                      |
| 2     | Usuário | Preenche nome do template                 | Valida unicidade do nome                        |
| 3     | Usuário | Seleciona categoria (Transacional/Marketing/Notificação) | Ajusta configurações padrão por tipo |
| 4     | Usuário | Preenche assunto (suporta variáveis Razor) | Valida sintaxe Razor |
| 5     | Usuário | Escreve código MJML no editor             | Monaco Editor com syntax highlighting           |
| 6     | Usuário | Define JSON Schema das variáveis          | Valida schema (JSON Schema Draft 7)            |
| 7     | Usuário | (Opcional) Preenche corpo texto plano     | Usado para clientes sem HTML                    |
| 8     | Usuário | Marca opções de tracking                  | Padrão: ambos para Marketing, só abertura para Transacional |
| 9     | Usuário | Clica em "Salvar"                         | Valida todos os campos                          |
| 10    | Sistema | Compila MJML para HTML                    | Retorna erro se MJML inválido                   |
| 11    | Sistema | Converte CSS para inline                  | Usa biblioteca de inlining CSS                  |
| 12    | Sistema | Salva template com status Rascunho        | Gera ID e timestamp                             |
| 13    | Sistema | Cria versão v1.0.0 em histórico           | Registra commit: "Versão inicial"               |
| 14    | Sistema | Exibe mensagem de sucesso                 | "Template criado com sucesso!"                  |

**Resultado**: Template de e-mail criado como rascunho.

### Fluxos Alternativos

#### FA-UC01-001: Usar Template Base
- **Quando**: Usuário clica em "Duplicar" em template existente
- **Sistema**: Carrega dados do original, adiciona sufixo " (Cópia)" ao nome
- **Resultado**: Novo template criado a partir de base existente

#### FA-UC01-002: Inserir Componente Reutilizável
- **Quando**: Usuário clica em "Inserir Componente"
- **Sistema**: Exibe galeria de componentes (header, footer, button)
- **Resultado**: Componente inserido no template

#### FA-UC01-003: Preview em Tempo Real
- **Quando**: Usuário digita no editor MJML
- **Sistema**: Aguarda 1s (debounce), compila MJML, atualiza preview lateral
- **Resultado**: Feedback visual imediato

### Fluxos de Exceção

#### FE-UC01-001: Nome Duplicado
- **Resposta**: HTTP 400 Bad Request
- **Mensagem**: "Já existe um template com este nome. Escolha outro."

#### FE-UC01-002: MJML Inválido
- **Resposta**: HTTP 400 Bad Request
- **Mensagem**: "Erro MJML na linha X: detalhes"

#### FE-UC01-003: JSON Schema Inválido
- **Resposta**: HTTP 400 Bad Request
- **Mensagem**: "JSON Schema inválido: detalhes"

#### FE-UC01-004: Template Muito Grande
- **Resposta**: HTTP 400 Bad Request
- **Mensagem**: "Template muito grande. Máximo: 100KB."

### Regras de Negócio Aplicadas

- **RN-RF064-001**: Design responsivo obrigatório (MJML compilável)
- **RN-RF064-008**: Pre-header text obrigatório (max 150 caracteres)
- **RN-RF064-009**: CSS inline automático (Outlook compatibility)
- **RN-RF064-012**: Versionamento automático (v1.0.0 na criação)
- **RN-RF064-016**: Unicidade de nome por empresa

### Critérios de Aceite

- ✅ Compilação MJML < 2s para templates até 50KB
- ✅ Preview atualiza em tempo real (debounce 1s)
- ✅ Salvamento < 1s (incluindo validações)
- ✅ Autocomplete de variáveis baseado em JSON Schema
- ✅ Mensagens de erro claras com linha/coluna

---

## UC02 — Visualizar Template de E-mail

### Objetivo

Exibir detalhes completos de um template: código MJML, HTML compilado, JSON Schema, histórico de versões, métricas de uso.

### Pré-condições

- Usuário autenticado
- Usuário possui permissão `TPL.EMAIL.VIEW`
- Template existe no banco
- Usuário tem acesso ao template (mesmo conglomerado ou global)

### Pós-condições

- Detalhes do template exibidos
- Histórico de versões carregado
- Métricas de engajamento calculadas

### Gatilho

Usuário clica em ícone "Visualizar" na listagem.

### Fluxo Principal

| Passo | Ator    | Ação                        | Sistema                                      |
|-------|---------|-----------------------------|----------------------------------------------|
| 1     | Usuário | Clica em "Visualizar"       | Abre tela de detalhes                       |
| 2     | Sistema | Carrega dados do template   | Exibe abas: Detalhes, MJML, Preview, Versões, Métricas |
| 3     | Usuário | Visualiza aba "Detalhes"    | Exibe: Nome, Tipo, Assunto, Status          |
| 4     | Usuário | Acessa aba "MJML"           | Exibe código MJML (read-only)              |
| 5     | Usuário | Acessa aba "Preview"        | Renderiza template com dados de exemplo     |

**Resultado**: Usuário visualizou informações completas do template.

### Fluxos de Exceção

#### FE-UC02-001: Template Não Encontrado
- **Resposta**: HTTP 404 Not Found
- **Mensagem**: "Template não encontrado ou foi removido."

#### FE-UC02-002: Acesso Negado
- **Resposta**: HTTP 403 Forbidden
- **Mensagem**: "Você não tem acesso a este template."

### Critérios de Aceite

- ✅ Detalhes carregam em < 1s
- ✅ Preview renderiza corretamente em 3 viewports

---

## UC03 — Editar Template de E-mail

### Objetivo

Permitir edição de template existente, criando nova versão automaticamente com mensagem de commit e diff.

### Pré-condições

- Usuário autenticado
- Usuário possui permissão `TPL.EMAIL.UPDATE`
- Template existe e pertence ao conglomerado do usuário

### Pós-condições

- Template atualizado com novos dados
- Nova versão criada (ex: v1.0.0 → v1.1.0)
- Diff calculado e armazenado
- Auditoria registrada

### Gatilho

Usuário clica em "Editar" na listagem ou visualização.

### Fluxo Principal

| Passo | Ator    | Ação                                  | Sistema                                      |
|-------|---------|---------------------------------------|----------------------------------------------|
| 1     | Usuário | Clica em "Editar"                     | Abre formulário preenchido                  |
| 2     | Usuário | Modifica campos desejados             | Valida sintaxe MJML/JSON em tempo real     |
| 3     | Usuário | Clica em "Salvar"                     | Exibe modal de versionamento                |
| 4     | Usuário | Preenche mensagem de commit           | Obrigatório (mín. 10 caracteres)           |
| 5     | Sistema | Incrementa versão                     | Ex: v1.1.0 → v1.2.0                        |
| 6     | Sistema | Cria registro em histórico            | Armazena diff completo                      |

**Resultado**: Template editado, nova versão criada.

### Fluxos de Exceção

#### FE-UC03-001: Sem Permissão
- **Resposta**: HTTP 403 Forbidden
- **Mensagem**: "Você não tem permissão para editar templates."

#### FE-UC03-002: MJML Inválido
- **Resposta**: HTTP 400 Bad Request
- **Mensagem**: "Erro MJML: detalhes"

### Critérios de Aceite

- ✅ Salvamento (incluindo versionamento) < 2s
- ✅ Diff calculado em < 1s para templates até 50KB

---

## UC04 — Inativar Template de E-mail

### Objetivo

Desativar template que não está mais em uso (soft delete).

### Pré-condições

- Usuário autenticado
- Usuário possui permissão `TPL.EMAIL.DELETE`

### Gatilho

Usuário clica em "Inativar" na listagem.

### Fluxo Principal

| Passo | Ator    | Ação                        | Sistema                                      |
|-------|---------|-----------------------------|----------------------------------------------|
| 1     | Usuário | Clica em "Inativar"         | Exibe modal de confirmação                  |
| 2     | Usuário | Confirma inativação         | Marca `Ativo = false`                       |

**Resultado**: Template inativado.

### Critérios de Aceite

- ✅ Inativação < 500ms
- ✅ Histórico completo preservado

---

## 4. MATRIZ DE RASTREABILIDADE

| UC   | RF Items Cobertos | RNs Aplicadas | Endpoints |
|------|-------------------|---------------|-----------|
| UC00 | RF-CRUD-02        | RN-RF064-005, RN-RF064-016 | `GET /api/templates-email` |
| UC01 | RF-CRUD-01        | RN-RF064-001, RN-RF064-008, RN-RF064-009, RN-RF064-012, RN-RF064-016 | `POST /api/templates-email` |
| UC02 | RF-CRUD-03        | RN-RF064-013, RN-RF064-014 | `GET /api/templates-email/{id}` |
| UC03 | RF-CRUD-04        | RN-RF064-009, RN-RF064-012 | `PUT /api/templates-email/{id}` |
| UC04 | RF-CRUD-05        | Soft delete | `DELETE /api/templates-email/{id}` |

---

## CHANGELOG

| Versão | Data       | Autor                 | Descrição                                     |
|--------|------------|-----------------------|-----------------------------------------------|
| 2.0    | 2025-12-31 | Agência ALC - alc.dev.br | Versão canônica v2.0 conforme template oficial |
| 1.0    | 2025-12-17 | Sistema               | Versão inicial (não conforme, substituída)    |
