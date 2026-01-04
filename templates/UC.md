# UC-RFXXX — Casos de Uso Canônicos

**RF:** RFXXX — [Nome do Requisito Funcional]  
**Versão:** 2.0  
**Data:** YYYY-MM-DD  
**Autor:** Agência ALC - alc.dev.br  

---

## 1. OBJETIVO DO DOCUMENTO

Este documento descreve **todos os Casos de Uso (UC)** derivados do **RFXXX**, cobrindo integralmente o comportamento funcional esperado.

Os UCs aqui definidos servem como **contrato comportamental**, sendo a **fonte primária** para geração de:
- Casos de Teste (TC-RFXXX.yaml)
- Massas de Teste (MT-RFXXX.yaml)
- Evidências de auditoria e validação funcional
- Execução por agentes de IA (tester, QA, E2E)

---

## 2. SUMÁRIO DE CASOS DE USO

| ID | Nome | Ator Principal |
|----|------|----------------|
| UC00 | Listar [Entidade] | Usuário Autenticado |
| UC01 | Criar [Entidade] | Usuário Autenticado |
| UC02 | Visualizar [Entidade] | Usuário Autenticado |
| UC03 | Editar [Entidade] | Usuário Autenticado |
| UC04 | Excluir [Entidade] | Usuário Autenticado |

---

## 3. PADRÕES GERAIS APLICÁVEIS A TODOS OS UCs

- Todos os acessos respeitam **isolamento por tenant**
- Todas as ações exigem **permissão explícita**
- Erros não devem vazar informações sensíveis
- Auditoria deve registrar **quem**, **quando** e **qual ação**
- Mensagens devem ser claras, previsíveis e rastreáveis

---

## UC00 — Listar [Entidade]

### Objetivo
Permitir que o usuário visualize registros disponíveis do seu próprio tenant.

### Pré-condições
- Usuário autenticado
- Permissão `entidade.view_any`

### Pós-condições
- Lista exibida conforme filtros e paginação

### Fluxo Principal
- **FP-UC00-001:** Usuário acessa a funcionalidade
- **FP-UC00-002:** Sistema valida permissão
- **FP-UC00-003:** Sistema carrega registros do tenant
- **FP-UC00-004:** Sistema aplica paginação e ordenação
- **FP-UC00-005:** Sistema exibe a lista

### Fluxos Alternativos
- **FA-UC00-001:** Buscar por termo
- **FA-UC00-002:** Ordenar por coluna
- **FA-UC00-003:** Filtrar por status

### Fluxos de Exceção
- **FE-UC00-001:** Usuário sem permissão → acesso negado
- **FE-UC00-002:** Nenhum registro → estado vazio exibido

### Regras de Negócio
- RN-UC-00-001: Somente registros do tenant
- RN-UC-00-002: Registros soft-deleted não aparecem
- RN-UC-00-003: Paginação padrão definida

### Critérios de Aceite
- **CA-UC00-001:** A lista DEVE exibir apenas registros do tenant do usuário autenticado
- **CA-UC00-002:** Registros excluídos (soft delete) NÃO devem aparecer na listagem
- **CA-UC00-003:** Paginação DEVE ser aplicada com limite padrão de 20 registros
- **CA-UC00-004:** Sistema DEVE permitir ordenação por qualquer coluna visível
- **CA-UC00-005:** Filtros DEVEM ser acumuláveis e refletir na URL

---

## UC01 — Criar [Entidade]

### Objetivo
Permitir a criação de um novo registro válido.

### Pré-condições
- Usuário autenticado
- Permissão `entidade.create`

### Pós-condições
- Registro persistido
- Auditoria registrada

### Fluxo Principal
- **FP-UC01-001:** Usuário solicita criação
- **FP-UC01-002:** Sistema valida permissão
- **FP-UC01-003:** Sistema exibe formulário
- **FP-UC01-004:** Usuário informa dados
- **FP-UC01-005:** Sistema valida dados
- **FP-UC01-006:** Sistema cria registro
- **FP-UC01-007:** Sistema registra auditoria
- **FP-UC01-008:** Sistema confirma sucesso

### Fluxos Alternativos
- **FA-UC01-001:** Salvar e criar outro
- **FA-UC01-002:** Cancelar criação

### Fluxos de Exceção
- **FE-UC01-001:** Erro de validação
- **FE-UC01-002:** Registro duplicado
- **FE-UC01-003:** Erro inesperado

### Regras de Negócio
- RN-UC-01-001: Campos obrigatórios
- RN-UC-01-002: tenant_id automático
- RN-UC-01-003: created_by automático

### Critérios de Aceite
- **CA-UC01-001:** Todos os campos obrigatórios DEVEM ser validados antes de persistir
- **CA-UC01-002:** tenant_id DEVE ser preenchido automaticamente com o tenant do usuário autenticado
- **CA-UC01-003:** created_by DEVE ser preenchido automaticamente com o ID do usuário autenticado
- **CA-UC01-004:** created_at DEVE ser preenchido automaticamente com timestamp atual
- **CA-UC01-005:** Sistema DEVE retornar erro claro se validação falhar
- **CA-UC01-006:** Auditoria DEVE ser registrada APÓS sucesso da criação

---

## UC02 — Visualizar [Entidade]

### Objetivo
Permitir visualização detalhada de um registro.

### Pré-condições
- Usuário autenticado
- Permissão `entidade.view`

### Pós-condições
- Dados exibidos corretamente

### Fluxo Principal
- **FP-UC02-001:** Usuário seleciona registro
- **FP-UC02-002:** Sistema valida permissão
- **FP-UC02-003:** Sistema valida tenant
- **FP-UC02-004:** Sistema exibe dados

### Fluxos de Exceção
- **FE-UC02-001:** Registro inexistente
- **FE-UC02-002:** Registro de outro tenant

### Regras de Negócio
- RN-UC-02-001: Isolamento por tenant
- RN-UC-02-002: Auditoria visível

### Critérios de Aceite
- **CA-UC02-001:** Usuário SÓ pode visualizar registros do próprio tenant
- **CA-UC02-002:** Informações de auditoria DEVEM ser exibidas (created_by, created_at, updated_by, updated_at)
- **CA-UC02-003:** Tentativa de acessar registro de outro tenant DEVE retornar 404
- **CA-UC02-004:** Tentativa de acessar registro inexistente DEVE retornar 404
- **CA-UC02-005:** Dados exibidos DEVEM corresponder exatamente ao estado atual no banco

---

## UC03 — Editar [Entidade]

### Objetivo
Permitir alteração controlada de um registro.

### Pré-condições
- Usuário autenticado
- Permissão `entidade.update`

### Pós-condições
- Registro atualizado
- Auditoria registrada

### Fluxo Principal
- **FP-UC03-001:** Usuário solicita edição
- **FP-UC03-002:** Sistema valida permissão
- **FP-UC03-003:** Sistema carrega dados
- **FP-UC03-004:** Usuário altera dados
- **FP-UC03-005:** Sistema valida alterações
- **FP-UC03-006:** Sistema persiste alterações
- **FP-UC03-007:** Sistema registra auditoria

### Fluxos Alternativos
- **FA-UC03-001:** Cancelar edição

### Fluxos de Exceção
- **FE-UC03-001:** Erro de validação
- **FE-UC03-002:** Conflito de edição

### Regras de Negócio
- RN-UC-03-001: updated_by automático
- RN-UC-03-002: updated_at automático

### Critérios de Aceite
- **CA-UC03-001:** updated_by DEVE ser preenchido automaticamente com ID do usuário autenticado
- **CA-UC03-002:** updated_at DEVE ser preenchido automaticamente com timestamp atual
- **CA-UC03-003:** Apenas campos alterados DEVEM ser validados
- **CA-UC03-004:** Sistema DEVE detectar conflitos de edição concorrente
- **CA-UC03-005:** Tentativa de editar registro de outro tenant DEVE retornar 404
- **CA-UC03-006:** Auditoria DEVE registrar estado anterior e novo estado

---

## UC04 — Excluir [Entidade]

### Objetivo
Permitir exclusão lógica de registros.

### Pré-condições
- Usuário autenticado
- Permissão `entidade.delete`

### Pós-condições
- Registro marcado como excluído

### Fluxo Principal
- **FP-UC04-001:** Usuário solicita exclusão
- **FP-UC04-002:** Sistema confirma ação
- **FP-UC04-003:** Sistema valida permissão
- **FP-UC04-004:** Sistema verifica dependências
- **FP-UC04-005:** Sistema executa soft delete
- **FP-UC04-006:** Sistema registra auditoria

### Fluxos Alternativos
- **FA-UC04-001:** Cancelar exclusão
- **FA-UC04-002:** Exclusão em lote

### Fluxos de Exceção
- **FE-UC04-001:** Dependências existentes
- **FE-UC04-002:** Registro já excluído

### Regras de Negócio
- RN-UC-04-001: Exclusão sempre lógica
- RN-UC-04-002: Dependências bloqueiam exclusão

### Critérios de Aceite
- **CA-UC04-001:** Exclusão DEVE ser sempre lógica (soft delete) via deleted_at
- **CA-UC04-002:** Sistema DEVE verificar dependências ANTES de permitir exclusão
- **CA-UC04-003:** Sistema DEVE exigir confirmação explícita do usuário
- **CA-UC04-004:** deleted_at DEVE ser preenchido com timestamp atual
- **CA-UC04-005:** Tentativa de excluir registro com dependências DEVE retornar erro claro
- **CA-UC04-006:** Registro excluído NÃO deve aparecer em listagens padrão

---

## 4. MATRIZ DE RASTREABILIDADE

| UC | Regras de Negócio |
|----|------------------|
| UC00 | RN-UC-00-001, RN-UC-00-002, RN-UC-00-003 |
| UC01 | RN-UC-01-001, RN-UC-01-002, RN-UC-01-003 |
| UC02 | RN-UC-02-001, RN-UC-02-002 |
| UC03 | RN-UC-03-001, RN-UC-03-002 |
| UC04 | RN-UC-04-001, RN-UC-04-002 |

---

## CHANGELOG

| Versão | Data | Autor | Descrição |
|------|------|-------|-----------|
| 2.0 | YYYY-MM-DD | Agência ALC - alc.dev.br | Versão canônica orientada a contrato |
