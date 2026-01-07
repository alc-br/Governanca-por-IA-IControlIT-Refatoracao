# UC-RF031 — Casos de Uso Canônicos

**RF:** RF031 — Gestão de Plano de Contas Contábil Multi-Dimensional
**Epic:** EPIC006-FIN - Financeiro Base
**Fase:** Fase 3 - Financeiro I - Base Contábil
**Versão:** 2.0
**Data:** 2025-12-31
**Autor:** Agência ALC - alc.dev.br

---

## 1. OBJETIVO DO DOCUMENTO

Este documento descreve **todos os Casos de Uso (UC)** derivados do **RF031**, cobrindo integralmente o comportamento funcional esperado.

Os UCs aqui definidos servem como **contrato comportamental**, sendo a **fonte primária** para geração de:
- Casos de Teste (TC-RF031.yaml)
- Massas de Teste (MT-RF031.yaml)
- Evidências de auditoria e validação funcional
- Execução por agentes de IA (tester, QA, E2E)

---

## 2. SUMÁRIO DE CASOS DE USO

| ID | Nome | Ator Principal |
|----|------|----------------|
| UC00 | Listar Plano de Contas | Usuário Autenticado |
| UC01 | Criar Conta Contábil | Usuário Autenticado |
| UC02 | Visualizar Conta Contábil | Usuário Autenticado |
| UC03 | Editar Conta Contábil | Usuário Autenticado |
| UC04 | Inativar/Excluir Conta Contábil | Usuário Autenticado |

---

## 3. PADRÕES GERAIS APLICÁVEIS A TODOS OS UCs

- Todos os acessos respeitam **isolamento por tenant (ClienteId)**
- Todas as ações exigem **permissão explícita** (RBAC)
- Erros não devem vazar informações sensíveis
- Auditoria deve registrar **quem**, **quando** e **qual ação** (retenção 7 anos)
- Mensagens devem ser claras, previsíveis e rastreáveis
- Hierarquia de até **7 níveis configuráveis**
- Código contábil **único por ClienteId**
- **Soft delete obrigatório** (nunca DELETE físico)
- **Validações contábeis** executadas pré-save
- Conta **Sintética** não permite lançamentos diretos
- Conta **Analítica** (folha) permite lançamentos

---

## UC00 — Listar Plano de Contas

### Objetivo
Permitir que o usuário visualize a estrutura hierárquica completa do plano de contas contábil com até 7 níveis de profundidade, com capacidade de expandir/contrair nós.

### Pré-condições
- Usuário autenticado
- Permissão `GES.PLANO_CONTAS.VIEW`

### Pós-condições
- Estrutura hierárquica exibida conforme filtros
- Auditoria de acesso registrada

### Fluxo Principal
- **FP-UC00-001:** Usuário acessa menu "Gestão > Plano de Contas"
- **FP-UC00-002:** Sistema valida permissão `GES.PLANO_CONTAS.VIEW`
- **FP-UC00-003:** Sistema carrega estrutura hierárquica (tree view) do ClienteId do usuário
- **FP-UC00-004:** Sistema exibe contas de nível 1 (raiz) collapsed por padrão
- **FP-UC00-005:** Sistema disponibiliza filtros: Tipo (Sintética/Analítica), Status (Ativo/Inativo), Busca por código/nome

### Fluxos Alternativos
- **FA-UC00-001:** Expandir nó
  - Usuário clica em ícone (+) ao lado de conta Sintética
  - Sistema carrega e exibe contas filhas do próximo nível
- **FA-UC00-002:** Buscar conta
  - Usuário digita código ou nome no campo de busca
  - Sistema filtra e destaca contas correspondentes, expandindo caminho completo
- **FA-UC00-003:** Filtrar por tipo
  - Usuário seleciona "Sintética" ou "Analítica"
  - Sistema aplica filtro e atualiza tree view
- **FA-UC00-004:** Expandir tudo
  - Usuário clica em "Expandir Tudo"
  - Sistema expande recursivamente todos os nós (limite 1000 contas visíveis por performance)
- **FA-UC00-005:** Exportar para Excel
  - Usuário clica em "Exportar"
  - Sistema gera Excel flat com colunas: Código, Nome, Tipo, Nível, Código Pai, Status

### Fluxos de Exceção
- **FE-UC00-001:** Usuário sem permissão
  - Sistema detecta falta de permissão `GES.PLANO_CONTAS.VIEW`
  - Sistema retorna HTTP 403 (Forbidden)
  - Sistema exibe mensagem: "Acesso negado"
- **FE-UC00-002:** Lista vazia
  - Não existem contas cadastradas para este ClienteId
  - Sistema exibe estado vazio: "Nenhuma conta cadastrada. Clique em 'Nova Conta' ou 'Importar Estrutura'"
- **FE-UC00-003:** Hierarquia circular detectada (dados corrompidos)
  - Sistema detecta loop circular (A → B → C → A)
  - Sistema exibe alerta: "Estrutura contábil com inconsistência detectada. Contate o administrador"
  - Sistema registra erro em log de auditoria

### Regras de Negócio
- **RN-UC-00-001:** Somente contas do ClienteId do usuário autenticado (RN-RF031-14)
- **RN-UC-00-002:** Contas com `FlExcluido=TRUE` NÃO aparecem (RN-RF031-15)
- **RN-UC-00-003:** Tree view exibe até 1000 contas expandidas simultaneamente (performance)

### Critérios de Aceite
- **CA-UC00-001:** Lista DEVE exibir apenas contas do ClienteId do usuário autenticado
- **CA-UC00-002:** Contas excluídas (FlExcluido=TRUE) NÃO devem aparecer
- **CA-UC00-003:** Filtros DEVEM ser acumuláveis (tipo + status + busca)
- **CA-UC00-004:** Expandir nó DEVE carregar filhos sob demanda (lazy loading)
- **CA-UC00-005:** Tentativa de acesso sem permissão DEVE retornar HTTP 403

---

## UC01 — Criar Conta Contábil

### Objetivo
Permitir criação de nova conta contábil na estrutura hierárquica, validando código único, nível máximo (7) e regras contábeis.

### Pré-condições
- Usuário autenticado
- Permissão `GES.PLANO_CONTAS.CREATE`

### Pós-condições
- Conta persistida no banco de dados
- Auditoria registrada (usuário, timestamp, dados criados)
- Evento de domínio `PlanoContaCriada` publicado

### Fluxo Principal
- **FP-UC01-001:** Usuário clica em "Nova Conta" ou "+" em nó pai
- **FP-UC01-002:** Sistema valida permissão `GES.PLANO_CONTAS.CREATE`
- **FP-UC01-003:** Sistema exibe formulário com campos:
  - Código Contábil (obrigatório, único)
  - Nome (obrigatório, máx 200 caracteres)
  - Tipo (Sintética / Analítica)
  - Conta Pai (dropdown hierárquico, opcional se nível 1)
  - Permite Lançamento (automático: TRUE se Analítica, FALSE se Sintética)
  - Aceita Rateio (checkbox)
  - Dedutível IR (checkbox, herdado do pai se não informado)
- **FP-UC01-004:** Usuário preenche campos obrigatórios
- **FP-UC01-005:** Usuário clica em "Salvar"
- **FP-UC01-006:** Sistema valida dados (RN-RF031-01, RN-RF031-11)
- **FP-UC01-007:** Sistema cria registro com campos automáticos:
  - `ClienteId` = ID do cliente do usuário autenticado
  - `Nivel` = calculado automaticamente (pai.Nivel + 1, ou 1 se sem pai)
  - `FlAtivo` = TRUE
  - `FlExcluido` = FALSE
  - `DtCadastro` = timestamp atual
  - `IdUsuarioCadastro` = ID do usuário autenticado
- **FP-UC01-008:** Sistema registra auditoria completa (RN-RF031-10)
- **FP-UC01-009:** Sistema publica evento `PlanoContaCriada`
- **FP-UC01-010:** Sistema exibe mensagem de sucesso: "Conta {codigo} criada com sucesso"
- **FP-UC01-011:** Sistema redireciona para tree view expandindo caminho até nova conta

### Fluxos Alternativos
- **FA-UC01-001:** Salvar e criar outra
  - Usuário clica em "Salvar e Criar Outra"
  - Sistema salva registro
  - Sistema limpa formulário mantendo mesma tela
- **FA-UC01-002:** Cancelar criação
  - Usuário clica em "Cancelar"
  - Sistema exibe confirmação: "Descartar alterações?"
  - Se confirmado, retorna à tree view sem salvar

### Fluxos de Exceção
- **FE-UC01-001:** Código duplicado
  - Sistema detecta código já existente no ClienteId (RN-RF031-01)
  - Sistema retorna HTTP 400
  - Sistema exibe mensagem: "Código contábil {codigo} já existe"
- **FE-UC01-002:** Nível máximo excedido
  - Conta pai está no nível 7, usuário tenta criar filha
  - Sistema retorna HTTP 400
  - Sistema exibe mensagem: "Estrutura permite no máximo 7 níveis hierárquicos"
- **FE-UC01-003:** Nome muito longo
  - Nome possui mais de 200 caracteres
  - Sistema retorna HTTP 400
  - Sistema exibe mensagem: "Nome deve ter até 200 caracteres"
- **FE-UC01-004:** Tipo inválido
  - Tentativa de marcar conta Sintética como "Permite Lançamento"
  - Sistema retorna HTTP 400
  - Sistema exibe mensagem: "Conta Sintética não pode receber lançamentos diretos (RN-RF031-11)"

### Regras de Negócio
- **RN-UC-01-001:** Código DEVE ser único por ClienteId (RN-RF031-01)
- **RN-UC-01-002:** Máximo 7 níveis de profundidade (RN-RF031-01)
- **RN-UC-01-003:** ClienteId preenchido automaticamente (RN-RF031-14)
- **RN-UC-01-004:** DtCadastro e IdUsuarioCadastro preenchidos automaticamente
- **RN-UC-01-005:** Conta Sintética NUNCA permite lançamento (RN-RF031-11)
- **RN-UC-01-006:** Nivel calculado automaticamente (pai.Nivel + 1)

### Critérios de Aceite
- **CA-UC01-001:** Todos campos obrigatórios DEVEM ser validados antes de persistir
- **CA-UC01-002:** ClienteId DEVE ser preenchido automaticamente
- **CA-UC01-003:** DtCadastro DEVE ser preenchido automaticamente com timestamp atual
- **CA-UC01-004:** Tentativa de criar com código duplicado DEVE retornar HTTP 400
- **CA-UC01-005:** Tentativa de criar nível 8 DEVE retornar HTTP 400
- **CA-UC01-006:** Auditoria DEVE ser registrada APÓS sucesso

---

## UC02 — Visualizar Conta Contábil

### Objetivo
Permitir visualização detalhada de uma conta contábil específica, incluindo histórico de alterações e lançamentos associados.

### Pré-condições
- Usuário autenticado
- Permissão `GES.PLANO_CONTAS.VIEW_DETAILS`
- Conta pertence ao ClienteId do usuário

### Pós-condições
- Dados exibidos corretamente
- Auditoria de acesso registrada

### Fluxo Principal
- **FP-UC02-001:** Usuário clica em conta na tree view ou acessa via URL direta
- **FP-UC02-002:** Sistema valida permissão `GES.PLANO_CONTAS.VIEW_DETAILS`
- **FP-UC02-003:** Sistema valida que conta pertence ao ClienteId do usuário (RN-RF031-14)
- **FP-UC02-004:** Sistema carrega dados completos da conta
- **FP-UC02-005:** Sistema exibe tela de visualização com:
  - **Dados principais:** Código, Nome, Tipo, Nível, Status
  - **Hierarquia:** Caminho completo (Classe > Grupo > ... > Conta)
  - **Configurações:** Permite Lançamento, Aceita Rateio, Dedutível IR
  - **Estatísticas:** Qtd lançamentos (12 meses), Valor acumulado
  - **Auditoria:** Criado por, em, Atualizado por, em
  - **Histórico de alterações:** Últimas 10 mudanças com diff
  - **Contas filhas:** Lista de contas subordinadas (se Sintética)

### Fluxos Alternativos
- **FA-UC02-001:** Editar conta
  - Usuário clica em "Editar"
  - Sistema redireciona para UC03 (Editar Conta Contábil)
- **FA-UC02-002:** Inativar conta
  - Usuário clica em "Inativar"
  - Sistema redireciona para UC04 (Inativar Conta Contábil)
- **FA-UC02-003:** Visualizar histórico completo
  - Usuário clica em "Histórico Completo"
  - Sistema exibe modal com todas as alterações (ilimitado)
- **FA-UC02-004:** Visualizar lançamentos
  - Usuário clica em "Ver Lançamentos"
  - Sistema redireciona para tela de lançamentos filtrada por esta conta

### Fluxos de Exceção
- **FE-UC02-001:** Conta inexistente
  - ID informado não existe
  - Sistema retorna HTTP 404
  - Sistema exibe mensagem: "Conta não encontrada"
- **FE-UC02-002:** Conta de outro cliente
  - Conta existe mas pertence a outro ClienteId
  - Sistema retorna HTTP 404 (por segurança, não revelar existência)
  - Sistema exibe mensagem: "Conta não encontrada"
- **FE-UC02-003:** Usuário sem permissão
  - Sistema detecta falta de permissão `GES.PLANO_CONTAS.VIEW_DETAILS`
  - Sistema retorna HTTP 403
  - Sistema exibe mensagem: "Acesso negado"

### Regras de Negócio
- **RN-UC-02-001:** Usuário SÓ pode visualizar contas do próprio ClienteId (RN-RF031-14)
- **RN-UC-02-002:** Histórico de auditoria DEVE ser exibido (RN-RF031-10)
- **RN-UC-02-003:** Se conta Sintética, exibir lista de filhas

### Critérios de Aceite
- **CA-UC02-001:** Usuário SÓ pode visualizar contas do próprio ClienteId
- **CA-UC02-002:** Informações de auditoria DEVEM ser exibidas
- **CA-UC02-003:** Tentativa de acessar conta de outro ClienteId DEVE retornar HTTP 404
- **CA-UC02-004:** Tentativa de acessar conta inexistente DEVE retornar HTTP 404
- **CA-UC02-005:** Dados exibidos DEVEM corresponder ao estado atual no banco

---

## UC03 — Editar Conta Contábil

### Objetivo
Permitir alteração controlada de conta contábil existente, respeitando restrições de contas com lançamentos.

### Pré-condições
- Usuário autenticado
- Permissão `GES.PLANO_CONTAS.EDIT`
- Conta ativa e pertence ao ClienteId do usuário

### Pós-condições
- Conta atualizada no banco de dados
- Auditoria registrada com dados anteriores (JSON) e novos
- Evento `PlanoContaAtualizada` publicado

### Fluxo Principal
- **FP-UC03-001:** Usuário clica em "Editar" na visualização ou tree view
- **FP-UC03-002:** Sistema valida permissão `GES.PLANO_CONTAS.EDIT`
- **FP-UC03-003:** Sistema valida que conta pertence ao ClienteId do usuário
- **FP-UC03-004:** Sistema carrega dados atuais da conta
- **FP-UC03-005:** Sistema exibe formulário preenchido
- **FP-UC03-006:** Sistema bloqueia campos se conta possui lançamentos:
  - Código (readonly)
  - Tipo (readonly)
  - Conta Pai (readonly)
- **FP-UC03-007:** Usuário altera campos permitidos
- **FP-UC03-008:** Usuário clica em "Salvar"
- **FP-UC03-009:** Sistema valida alterações
- **FP-UC03-010:** Sistema persiste alterações com campos automáticos:
  - `DtAlteracao` = timestamp atual
  - `IdUsuarioAlteracao` = ID do usuário autenticado
- **FP-UC03-011:** Sistema salva dados anteriores em JSON para auditoria (RN-RF031-10)
- **FP-UC03-012:** Sistema publica evento `PlanoContaAtualizada`
- **FP-UC03-013:** Sistema exibe mensagem de sucesso: "Conta {codigo} atualizada"
- **FP-UC03-014:** Sistema redireciona para visualização (UC02)

### Fluxos Alternativos
- **FA-UC03-001:** Cancelar edição
  - Usuário clica em "Cancelar"
  - Sistema exibe confirmação: "Descartar alterações?"
  - Se confirmado, retorna à visualização sem salvar

### Fluxos de Exceção
- **FE-UC03-001:** Código duplicado (se permitido alterar)
  - Código alterado já existe para outro registro no ClienteId
  - Sistema retorna HTTP 400
  - Sistema exibe mensagem: "Código contábil {codigo} já existe"
- **FE-UC03-002:** Nome muito longo
  - Nome alterado possui mais de 200 caracteres
  - Sistema retorna HTTP 400
  - Sistema exibe mensagem: "Nome deve ter até 200 caracteres"
- **FE-UC03-003:** Tentativa de alterar tipo com lançamentos
  - Conta possui lançamentos e usuário tenta mudar tipo
  - Sistema retorna HTTP 400
  - Sistema exibe mensagem: "Não é possível alterar tipo de conta com lançamentos existentes"
- **FE-UC03-004:** Conflito de edição concorrente
  - Outro usuário alterou a conta simultaneamente
  - Sistema detecta conflito (versioning/timestamp)
  - Sistema retorna HTTP 409
  - Sistema exibe mensagem: "Conta foi alterada por outro usuário. Recarregue e tente novamente"

### Regras de Negócio
- **RN-UC-03-001:** DtAlteracao e IdUsuarioAlteracao preenchidos automaticamente
- **RN-UC-03-002:** Conta com lançamentos NÃO pode alterar: Código, Tipo, Pai
- **RN-UC-03-003:** Nome DEVE respeitar limite de 200 caracteres
- **RN-UC-03-004:** Auditoria DEVE salvar estado anterior em JSON (RN-RF031-10)

### Critérios de Aceite
- **CA-UC03-001:** DtAlteracao DEVE ser preenchido automaticamente
- **CA-UC03-002:** IdUsuarioAlteracao DEVE ser preenchido automaticamente
- **CA-UC03-003:** Campos críticos (Código, Tipo, Pai) DEVEM aparecer readonly se conta tiver lançamentos
- **CA-UC03-004:** Sistema DEVE detectar conflitos de edição concorrente (HTTP 409)
- **CA-UC03-005:** Auditoria DEVE registrar estado anterior em JSON

---

## UC04 — Inativar/Excluir Conta Contábil

### Objetivo
Permitir inativação lógica (soft delete) de contas contábeis, validando dependências (lançamentos, contas filhas).

### Pré-condições
- Usuário autenticado
- Permissão `GES.PLANO_CONTAS.DELETE`
- Conta ativa e pertence ao ClienteId do usuário

### Pós-condições
- Se **sem lançamentos/filhos**: Conta marcada como excluída (`FlExcluido=TRUE`)
- Se **com lançamentos/filhos**: Conta marcada como inativa (`FlAtivo=FALSE`)
- Auditoria registrada
- Evento `PlanoContaExcluida` ou `PlanoContaInativada` publicado

### Fluxo Principal
- **FP-UC04-001:** Usuário clica em "Excluir" ou "Inativar" na visualização
- **FP-UC04-002:** Sistema valida permissão `GES.PLANO_CONTAS.DELETE`
- **FP-UC04-003:** Sistema valida que conta pertence ao ClienteId do usuário
- **FP-UC04-004:** Sistema verifica dependências:
  - Possui lançamentos contábeis?
  - Possui contas filhas ativas?
- **FP-UC04-005:** Sistema exibe confirmação apropriada:
  - **Sem dependências:** "Confirma exclusão de {codigo} - {nome}?" (soft delete)
  - **Com lançamentos:** "Esta conta possui {qtd} lançamentos. Será apenas inativada (não excluída). Confirma?"
  - **Com filhas ativas:** "Esta conta possui {qtd} contas filhas ativas. Não é possível inativar/excluir."
- **FP-UC04-006:** Usuário confirma
- **FP-UC04-007:** Sistema executa operação:
  - **Sem dependências:** `FlExcluido=TRUE`, `DtExclusao=now()`, `IdUsuarioExclusao=userId`
  - **Com lançamentos:** `FlAtivo=FALSE`, `DtInativacao=now()`, `IdUsuarioInativacao=userId`
- **FP-UC04-008:** Sistema registra auditoria (RN-RF031-10)
- **FP-UC04-009:** Sistema publica evento apropriado
- **FP-UC04-010:** Sistema exibe mensagem de sucesso
- **FP-UC04-011:** Sistema redireciona para tree view

### Fluxos Alternativos
- **FA-UC04-001:** Cancelar exclusão/inativação
  - Usuário clica em "Cancelar" no modal de confirmação
  - Sistema fecha modal sem executar operação

### Fluxos de Exceção
- **FE-UC04-001:** Conta possui filhas ativas
  - Sistema detecta contas filhas ativas
  - Sistema retorna HTTP 400
  - Sistema exibe mensagem: "Não é possível inativar/excluir conta com {qtd} contas filhas ativas"
  - Sistema lista as contas filhas
- **FE-UC04-002:** Conta já excluída/inativa
  - Conta já possui `FlExcluido=TRUE` ou `FlAtivo=FALSE`
  - Sistema retorna HTTP 400
  - Sistema exibe mensagem: "Conta já está inativa/excluída"
- **FE-UC04-003:** Conta de outro cliente
  - Conta pertence a outro ClienteId
  - Sistema retorna HTTP 404
  - Sistema exibe mensagem: "Conta não encontrada"
- **FE-UC04-004:** Usuário sem permissão
  - Sistema detecta falta de permissão `GES.PLANO_CONTAS.DELETE`
  - Sistema retorna HTTP 403
  - Sistema exibe mensagem: "Acesso negado"

### Regras de Negócio
- **RN-UC-04-001:** Exclusão DEVE ser sempre lógica (soft delete) via `FlExcluido=TRUE` (RN-RF031-15)
- **RN-UC-04-002:** Conta com lançamentos NÃO pode ser excluída, apenas inativada
- **RN-UC-04-003:** Conta Sintética com filhas ativas NÃO pode ser inativada/excluída
- **RN-UC-04-004:** Sistema DEVE exigir confirmação explícita
- **RN-UC-04-005:** Conta excluída NÃO aparece em listagens (UC00)

### Critérios de Aceite
- **CA-UC04-001:** Exclusão DEVE ser sempre lógica (soft delete) via `FlExcluido=TRUE`
- **CA-UC04-002:** Conta com lançamentos SÓ pode ser inativada (`FlAtivo=FALSE`), não excluída
- **CA-UC04-003:** Sistema DEVE verificar filhas ativas ANTES de permitir inativação
- **CA-UC04-004:** Sistema DEVE exigir confirmação explícita
- **CA-UC04-005:** Tentativa de excluir conta com filhas ativas DEVE retornar HTTP 400
- **CA-UC04-006:** Conta excluída NÃO deve aparecer em listagens padrão
- **CA-UC04-007:** Auditoria DEVE registrar operação (exclusão/inativação)

---

## 4. MATRIZ DE RASTREABILIDADE

| UC | Regras de Negócio do RF |
|----|-------------------------|
| UC00 | RN-RF031-01, RN-RF031-14, RN-RF031-15 |
| UC01 | RN-RF031-01, RN-RF031-10, RN-RF031-11, RN-RF031-14 |
| UC02 | RN-RF031-10, RN-RF031-14 |
| UC03 | RN-RF031-10, RN-RF031-14 |
| UC04 | RN-RF031-10, RN-RF031-14, RN-RF031-15 |

---

## CHANGELOG

| Versão | Data | Autor | Descrição |
|------|------|-------|-----------|
| 2.0 | 2025-12-31 | Agência ALC - alc.dev.br | Versão canônica orientada a contrato. Migração para template v2.0. Cobertura dos 5 UCs principais do RF031. |
| 1.0 | 2025-01-14 | Agência ALC - alc.dev.br | Versão inicial (estrutura antiga, 9 UCs) |
