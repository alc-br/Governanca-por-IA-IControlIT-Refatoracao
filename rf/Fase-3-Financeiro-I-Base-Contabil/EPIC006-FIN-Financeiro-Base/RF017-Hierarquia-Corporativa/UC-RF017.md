# UC-RF017 — Casos de Uso Canônicos

**RF:** RF017 — Gestão de Hierarquia Corporativa
**Epic:** EPIC006-FIN - Financeiro Base
**Fase:** Fase 3 - Financeiro I - Base Contábil
**Versão:** 2.0
**Data:** 2025-12-31
**Autor:** Agência ALC - alc.dev.br

---

## 1. OBJETIVO DO DOCUMENTO

Este documento descreve **todos os Casos de Uso (UC)** derivados do **RF017**, cobrindo integralmente o comportamento funcional esperado.

Os UCs aqui definidos servem como **contrato comportamental**, sendo a **fonte primária** para geração de:
- Casos de Teste (TC-RF017.yaml)
- Massas de Teste (MT-RF017.yaml)
- Evidências de auditoria e validação funcional
- Execução por agentes de IA (tester, QA, E2E)

---

## 2. SUMÁRIO DE CASOS DE USO

| ID | Nome | Ator Principal |
|----|------|----------------|
| UC00 | Listar Hierarquia Corporativa | Usuário Autenticado |
| UC01 | Criar Nível Hierárquico | Usuário Autenticado |
| UC02 | Visualizar Nível Hierárquico | Usuário Autenticado |
| UC03 | Editar Nível Hierárquico | Usuário Autenticado |
| UC04 | Inativar Nível Hierárquico | Usuário Autenticado |

---

## 3. PADRÕES GERAIS APLICÁVEIS A TODOS OS UCs

- Todos os acessos respeitam **isolamento por tenant (conglomerado)**
- Todas as ações exigem **permissão explícita**
- Erros não devem vazar informações sensíveis
- Auditoria deve registrar **quem**, **quando** e **qual ação**
- Mensagens devem ser claras, previsíveis e rastreáveis
- A hierarquia obrigatória é: **Filial → Centro de Custo → Departamento → Setor → Seção**
- Todos os códigos devem seguir **UPPER_SNAKE_CASE**
- Budget mensal, se informado, deve ser **positivo (> 0)**
- Gestores devem ser **consumidores ativos**

---

## UC00 — Listar Hierarquia Corporativa

### Objetivo
Permitir que o usuário visualize todos os níveis hierárquicos (Centro de Custo, Departamento, Setor, Seção) disponíveis do seu próprio conglomerado.

### Pré-condições
- Usuário autenticado
- Permissão `hierarquia.view_any`

### Pós-condições
- Lista exibida conforme filtros e paginação
- Auditoria de acesso registrada

### Fluxo Principal
- **FP-UC00-001:** Usuário acessa a funcionalidade de hierarquia corporativa
- **FP-UC00-002:** Sistema valida permissão `hierarquia.view_any`
- **FP-UC00-003:** Sistema carrega registros do conglomerado do usuário autenticado
- **FP-UC00-004:** Sistema aplica paginação (padrão: 20 registros) e ordenação (padrão: por código)
- **FP-UC00-005:** Sistema exibe a lista com colunas: Código, Nome, Tipo (CC/Depto/Setor/Seção), Nível Pai, Gestor, Budget Mensal, Status

### Fluxos Alternativos
- **FA-UC00-001:** Filtrar por tipo de nível
  - Usuário seleciona tipo (Centro de Custo, Departamento, Setor ou Seção)
  - Sistema filtra lista exibindo apenas registros do tipo selecionado
- **FA-UC00-002:** Filtrar por filial
  - Usuário seleciona filial no filtro
  - Sistema exibe apenas níveis hierárquicos vinculados àquela filial
- **FA-UC00-003:** Filtrar por status
  - Usuário seleciona "Ativos" ou "Inativos"
  - Sistema filtra lista conforme status
- **FA-UC00-004:** Buscar por código ou nome
  - Usuário digita termo de busca
  - Sistema filtra registros que contenham o termo no código ou nome (case-insensitive)
- **FA-UC00-005:** Ordenar por coluna
  - Usuário clica em cabeçalho de coluna
  - Sistema reordena lista (ascendente/descendente)

### Fluxos de Exceção
- **FE-UC00-001:** Usuário sem permissão
  - Sistema detecta falta de permissão `hierarquia.view_any`
  - Sistema retorna HTTP 403 (Forbidden)
  - Sistema exibe mensagem: "Acesso negado. Você não possui permissão para visualizar a hierarquia corporativa."
- **FE-UC00-002:** Nenhum registro encontrado
  - Não existem níveis hierárquicos cadastrados no conglomerado
  - Sistema exibe estado vazio com mensagem: "Nenhum nível hierárquico cadastrado"
  - Sistema exibe botão "Criar Primeiro Nível" (se usuário tiver permissão `hierarquia.create`)
- **FE-UC00-003:** Erro de conexão
  - Erro ao conectar com banco de dados
  - Sistema exibe mensagem: "Erro ao carregar dados. Tente novamente."
  - Sistema disponibiliza botão "Tentar novamente"

### Regras de Negócio
- **RN-UC-00-001:** Somente registros do conglomerado do usuário autenticado devem ser exibidos (RN-RF017-09)
- **RN-UC-00-002:** Registros com soft delete (deleted_at não nulo) NÃO devem aparecer por padrão
- **RN-UC-00-003:** Paginação padrão: 20 registros por página
- **RN-UC-00-004:** Ordenação padrão: por código (ascendente)

### Critérios de Aceite
- **CA-UC00-001:** A lista DEVE exibir apenas registros do conglomerado do usuário autenticado
- **CA-UC00-002:** Registros excluídos (soft delete) NÃO devem aparecer na listagem padrão
- **CA-UC00-003:** Paginação DEVE ser aplicada com limite padrão de 20 registros
- **CA-UC00-004:** Sistema DEVE permitir ordenação por qualquer coluna visível
- **CA-UC00-005:** Filtros DEVEM ser acumuláveis e refletir na URL (query parameters)
- **CA-UC00-006:** Tentativa de acesso sem permissão DEVE retornar HTTP 403

---

## UC01 — Criar Nível Hierárquico

### Objetivo
Permitir a criação de um novo nível hierárquico (Centro de Custo, Departamento, Setor ou Seção) válido, respeitando a hierarquia obrigatória.

### Pré-condições
- Usuário autenticado
- Permissão `hierarquia.create`
- Nível pai existe e está ativo (exceto para Centro de Custo que depende de Filial)

### Pós-condições
- Registro persistido no banco de dados
- Auditoria registrada (usuário, timestamp, dados criados)
- Evento de domínio publicado (ex: `centro_custo.criado`)

### Fluxo Principal
- **FP-UC01-001:** Usuário solicita criação de novo nível hierárquico
- **FP-UC01-002:** Sistema valida permissão `hierarquia.create`
- **FP-UC01-003:** Sistema exibe formulário com campos:
  - Tipo (Centro de Custo, Departamento, Setor, Seção)
  - Código (obrigatório, UPPER_SNAKE_CASE)
  - Nome (obrigatório, máx 120 caracteres)
  - Nível Pai (dropdown filtrado por tipo anterior na hierarquia)
  - Gestor/Gerente/Supervisor/Coordenador (opcional, autocomplete de consumidores ativos)
  - Budget Mensal (opcional, numérico positivo)
- **FP-UC01-004:** Usuário preenche campos obrigatórios
- **FP-UC01-005:** Usuário clica em "Salvar"
- **FP-UC01-006:** Sistema valida dados (RN-RF017-01 a RN-RF017-07)
- **FP-UC01-007:** Sistema cria registro com campos automáticos:
  - `conglomerado_id` = ID do conglomerado do usuário autenticado
  - `created_by` = ID do usuário autenticado
  - `created_at` = timestamp atual
  - `status` = "active"
- **FP-UC01-008:** Sistema registra auditoria completa (RN-RF017-10)
- **FP-UC01-009:** Sistema publica evento de domínio
- **FP-UC01-010:** Sistema exibe mensagem de sucesso: "Nível hierárquico {codigo} criado com sucesso"
- **FP-UC01-011:** Sistema redireciona para tela de listagem

### Fluxos Alternativos
- **FA-UC01-001:** Salvar e criar outro
  - Após salvar, usuário clica em "Salvar e Criar Outro"
  - Sistema salva registro
  - Sistema limpa formulário mantendo mesma tela
- **FA-UC01-002:** Cancelar criação
  - Usuário clica em "Cancelar"
  - Sistema exibe confirmação: "Descartar alterações?"
  - Se confirmado, sistema retorna à listagem sem salvar

### Fluxos de Exceção
- **FE-UC01-001:** Código duplicado
  - Sistema detecta código já existente no conglomerado (RN-RF017-01)
  - Sistema retorna HTTP 400 (Bad Request)
  - Sistema exibe mensagem: "Código {codigo} já existe para este conglomerado"
- **FE-UC01-002:** Código inválido (não UPPER_SNAKE_CASE)
  - Sistema detecta código fora do padrão (RN-RF017-07)
  - Sistema retorna HTTP 400
  - Sistema exibe mensagem: "Código deve seguir padrão UPPER_SNAKE_CASE (ex: DEPTO_TI, CC_ADM)"
- **FE-UC01-003:** Hierarquia quebrada
  - Usuário tenta criar nível sem nível pai ativo (RN-RF017-02)
  - Sistema retorna HTTP 400
  - Sistema exibe mensagem: "Não é possível criar {nivel} sem {nivel_pai} ativo"
- **FE-UC01-004:** Nome muito longo
  - Nome possui mais de 120 caracteres (RN-RF017-11)
  - Sistema retorna HTTP 400
  - Sistema exibe mensagem: "Nome deve ter até 120 caracteres"
- **FE-UC01-005:** Budget negativo
  - Budget mensal informado é ≤ 0 (RN-RF017-05)
  - Sistema retorna HTTP 400
  - Sistema exibe mensagem: "Budget mensal deve ser maior que zero"
- **FE-UC01-006:** Gestor inativo
  - Gestor selecionado está inativo (RN-RF017-04)
  - Sistema retorna HTTP 400
  - Sistema exibe mensagem: "Consumidor {id} não está ativo"
- **FE-UC01-007:** Filial inativa (para Centro de Custo)
  - Filial selecionada está inativa (RN-RF017-06)
  - Sistema retorna HTTP 400
  - Sistema exibe mensagem: "Filial {id} não existe ou está inativa"

### Regras de Negócio
- **RN-UC-01-001:** Código DEVE ser único por conglomerado (case-insensitive) (RN-RF017-01)
- **RN-UC-01-002:** Código DEVE seguir padrão UPPER_SNAKE_CASE (RN-RF017-07)
- **RN-UC-01-003:** Nome é obrigatório e DEVE ter até 120 caracteres (RN-RF017-11)
- **RN-UC-01-004:** Hierarquia DEVE ser respeitada: Filial → CC → Depto → Setor → Seção (RN-RF017-02)
- **RN-UC-01-005:** `conglomerado_id` preenchido automaticamente (RN-RF017-09)
- **RN-UC-01-006:** `created_by` e `created_at` preenchidos automaticamente
- **RN-UC-01-007:** Budget mensal, se informado, DEVE ser > 0 (RN-RF017-05)
- **RN-UC-01-008:** Gestor, se informado, DEVE ser consumidor ativo (RN-RF017-04)

### Critérios de Aceite
- **CA-UC01-001:** Todos os campos obrigatórios DEVEM ser validados antes de persistir
- **CA-UC01-002:** `conglomerado_id` DEVE ser preenchido automaticamente com o conglomerado do usuário autenticado
- **CA-UC01-003:** `created_by` DEVE ser preenchido automaticamente com o ID do usuário autenticado
- **CA-UC01-004:** `created_at` DEVE ser preenchido automaticamente com timestamp atual
- **CA-UC01-005:** Sistema DEVE retornar erro claro se validação falhar (HTTP 400 + mensagem)
- **CA-UC01-006:** Auditoria DEVE ser registrada APÓS sucesso da criação
- **CA-UC01-007:** Tentativa de criar com código duplicado DEVE retornar HTTP 400
- **CA-UC01-008:** Tentativa de criar nível sem nível pai ativo DEVE retornar HTTP 400

---

## UC02 — Visualizar Nível Hierárquico

### Objetivo
Permitir visualização detalhada de um nível hierárquico específico (Centro de Custo, Departamento, Setor ou Seção).

### Pré-condições
- Usuário autenticado
- Permissão `hierarquia.view`
- Registro existe e pertence ao conglomerado do usuário

### Pós-condições
- Dados exibidos corretamente
- Auditoria de acesso registrada

### Fluxo Principal
- **FP-UC02-001:** Usuário seleciona registro na listagem ou acessa via URL direta
- **FP-UC02-002:** Sistema valida permissão `hierarquia.view`
- **FP-UC02-003:** Sistema valida que registro pertence ao conglomerado do usuário (RN-RF017-09)
- **FP-UC02-004:** Sistema carrega dados completos do registro
- **FP-UC02-005:** Sistema exibe tela de visualização com:
  - Dados principais (Código, Nome, Tipo, Status)
  - Nível Pai (se aplicável)
  - Gestor/Gerente/Supervisor/Coordenador (se informado)
  - Budget Mensal (se informado)
  - Consumo Atual vs Budget (se aplicável)
  - Dados de auditoria (Criado por, em, Atualizado por, em)
  - Lista de níveis filhos (se existirem)

### Fluxos Alternativos
- **FA-UC02-001:** Editar registro
  - Usuário clica em "Editar"
  - Sistema redireciona para UC03 (Editar Nível Hierárquico)
- **FA-UC02-002:** Inativar registro
  - Usuário clica em "Inativar"
  - Sistema redireciona para UC04 (Inativar Nível Hierárquico)
- **FA-UC02-003:** Visualizar histórico de alterações
  - Usuário clica em "Histórico"
  - Sistema exibe modal com log de auditoria (todas as alterações)

### Fluxos de Exceção
- **FE-UC02-001:** Registro inexistente
  - ID informado não existe
  - Sistema retorna HTTP 404 (Not Found)
  - Sistema exibe mensagem: "Registro não encontrado"
- **FE-UC02-002:** Registro de outro conglomerado
  - Registro existe mas pertence a outro conglomerado
  - Sistema retorna HTTP 404 (por segurança, não revelar existência)
  - Sistema exibe mensagem: "Registro não encontrado"
- **FE-UC02-003:** Usuário sem permissão
  - Sistema detecta falta de permissão `hierarquia.view`
  - Sistema retorna HTTP 403 (Forbidden)
  - Sistema exibe mensagem: "Acesso negado"

### Regras de Negócio
- **RN-UC-02-001:** Usuário SÓ pode visualizar registros do próprio conglomerado (RN-RF017-09)
- **RN-UC-02-002:** Informações de auditoria DEVEM ser exibidas (created_by, created_at, updated_by, updated_at)
- **RN-UC-02-003:** Se registro tiver níveis filhos, exibir lista resumida

### Critérios de Aceite
- **CA-UC02-001:** Usuário SÓ pode visualizar registros do próprio conglomerado
- **CA-UC02-002:** Informações de auditoria DEVEM ser exibidas (created_by, created_at, updated_by, updated_at)
- **CA-UC02-003:** Tentativa de acessar registro de outro conglomerado DEVE retornar HTTP 404
- **CA-UC02-004:** Tentativa de acessar registro inexistente DEVE retornar HTTP 404
- **CA-UC02-005:** Dados exibidos DEVEM corresponder exatamente ao estado atual no banco
- **CA-UC02-006:** Se budget configurado, exibir percentual de consumo atual

---

## UC03 — Editar Nível Hierárquico

### Objetivo
Permitir alteração controlada de um nível hierárquico existente, respeitando restrições de histórico financeiro.

### Pré-condições
- Usuário autenticado
- Permissão `hierarquia.update`
- Registro existe, está ativo e pertence ao conglomerado do usuário

### Pós-condições
- Registro atualizado no banco de dados
- Auditoria registrada com dados anteriores e novos
- Evento de domínio publicado (ex: `centro_custo.atualizado`)

### Fluxo Principal
- **FP-UC03-001:** Usuário solicita edição de nível hierárquico
- **FP-UC03-002:** Sistema valida permissão `hierarquia.update`
- **FP-UC03-003:** Sistema valida que registro pertence ao conglomerado do usuário
- **FP-UC03-004:** Sistema carrega dados atuais do registro
- **FP-UC03-005:** Sistema exibe formulário preenchido com dados atuais
- **FP-UC03-006:** Usuário altera campos permitidos:
  - Nome (se não houver histórico financeiro para código)
  - Código (SOMENTE se não houver histórico financeiro) (RN-RF017-08)
  - Gestor/Gerente/Supervisor/Coordenador
  - Budget Mensal
- **FP-UC03-007:** Usuário clica em "Salvar"
- **FP-UC03-008:** Sistema valida alterações (RN-RF017-05, RN-RF017-07, RN-RF017-08, RN-RF017-11)
- **FP-UC03-009:** Sistema persiste alterações com campos automáticos:
  - `updated_by` = ID do usuário autenticado
  - `updated_at` = timestamp atual
- **FP-UC03-010:** Sistema registra auditoria completa (dados anteriores + novos) (RN-RF017-10)
- **FP-UC03-011:** Sistema publica evento de domínio
- **FP-UC03-012:** Sistema exibe mensagem de sucesso: "Nível hierárquico {codigo} atualizado com sucesso"
- **FP-UC03-013:** Sistema redireciona para tela de visualização (UC02)

### Fluxos Alternativos
- **FA-UC03-001:** Cancelar edição
  - Usuário clica em "Cancelar"
  - Sistema exibe confirmação: "Descartar alterações?"
  - Se confirmado, sistema retorna à tela de visualização sem salvar

### Fluxos de Exceção
- **FE-UC03-001:** Código duplicado
  - Código alterado já existe para outro registro no conglomerado
  - Sistema retorna HTTP 400
  - Sistema exibe mensagem: "Código {codigo} já existe para este conglomerado"
- **FE-UC03-002:** Tentativa de alterar código com histórico financeiro
  - Registro possui movimentações financeiras (RN-RF017-08)
  - Sistema retorna HTTP 400
  - Sistema exibe mensagem: "Não é possível alterar código com histórico de movimentações financeiras"
  - Sistema bloqueia campo Código (readonly)
- **FE-UC03-003:** Nome muito longo
  - Nome alterado possui mais de 120 caracteres
  - Sistema retorna HTTP 400
  - Sistema exibe mensagem: "Nome deve ter até 120 caracteres"
- **FE-UC03-004:** Budget negativo
  - Budget mensal alterado é ≤ 0
  - Sistema retorna HTTP 400
  - Sistema exibe mensagem: "Budget mensal deve ser maior que zero"
- **FE-UC03-005:** Gestor inativo
  - Gestor selecionado está inativo
  - Sistema retorna HTTP 400
  - Sistema exibe mensagem: "Consumidor {id} não está ativo"
- **FE-UC03-006:** Conflito de edição concorrente
  - Outro usuário alterou o registro simultaneamente
  - Sistema detecta conflito (versioning/timestamp)
  - Sistema retorna HTTP 409 (Conflict)
  - Sistema exibe mensagem: "Registro foi alterado por outro usuário. Recarregue e tente novamente."

### Regras de Negócio
- **RN-UC-03-001:** `updated_by` preenchido automaticamente com ID do usuário autenticado
- **RN-UC-03-002:** `updated_at` preenchido automaticamente com timestamp atual
- **RN-UC-03-003:** Código NÃO pode ser alterado se houver histórico financeiro (RN-RF017-08)
- **RN-UC-03-004:** Nome DEVE respeitar limite de 120 caracteres (RN-RF017-11)
- **RN-UC-03-005:** Budget mensal, se alterado, DEVE ser > 0 (RN-RF017-05)
- **RN-UC-03-006:** Gestor, se alterado, DEVE ser consumidor ativo (RN-RF017-04)

### Critérios de Aceite
- **CA-UC03-001:** `updated_by` DEVE ser preenchido automaticamente com ID do usuário autenticado
- **CA-UC03-002:** `updated_at` DEVE ser preenchido automaticamente com timestamp atual
- **CA-UC03-003:** Apenas campos alterados DEVEM ser validados
- **CA-UC03-004:** Sistema DEVE detectar conflitos de edição concorrente (retornar HTTP 409)
- **CA-UC03-005:** Tentativa de editar registro de outro conglomerado DEVE retornar HTTP 404
- **CA-UC03-006:** Auditoria DEVE registrar estado anterior e novo estado (RN-RF017-10)
- **CA-UC03-007:** Tentativa de alterar código com histórico financeiro DEVE retornar HTTP 400
- **CA-UC03-008:** Campo Código DEVE aparecer readonly se houver histórico financeiro

---

## UC04 — Inativar Nível Hierárquico

### Objetivo
Permitir inativação lógica (soft delete) de níveis hierárquicos, com opção de inativação em cascata.

### Pré-condições
- Usuário autenticado
- Permissão `hierarquia.delete`
- Registro existe, está ativo e pertence ao conglomerado do usuário
- Se não usar cascata: nível NÃO pode ter filhos ativos (RN-RF017-03)

### Pós-condições
- Registro marcado como inativo (`deleted_at` preenchido)
- Se cascata: todos os filhos também inativados
- Auditoria registrada
- Evento de domínio publicado (ex: `centro_custo.inativado`)

### Fluxo Principal
- **FP-UC04-001:** Usuário solicita inativação de nível hierárquico
- **FP-UC04-002:** Sistema valida permissão `hierarquia.delete`
- **FP-UC04-003:** Sistema valida que registro pertence ao conglomerado do usuário
- **FP-UC04-004:** Sistema verifica se existem níveis filhos ativos
- **FP-UC04-005:** Se existem filhos ativos, sistema exibe confirmação:
  - "Este nível possui {quantidade} {tipo_filho}(s) ativo(s). Deseja inativar em cascata?"
  - Opções: "Inativar em Cascata" | "Cancelar"
- **FP-UC04-006:** Se não existem filhos ativos, sistema exibe confirmação simples:
  - "Confirma inativação de {codigo} - {nome}?"
  - Opções: "Inativar" | "Cancelar"
- **FP-UC04-007:** Usuário confirma inativação
- **FP-UC04-008:** Sistema executa soft delete:
  - `deleted_at` = timestamp atual
  - `deleted_by` = ID do usuário autenticado
- **FP-UC04-009:** Se cascata, sistema inativa todos os filhos recursivamente (RN-RF017-12)
- **FP-UC04-010:** Sistema registra auditoria para cada registro inativado (RN-RF017-10)
- **FP-UC04-011:** Sistema publica evento de domínio
- **FP-UC04-012:** Sistema exibe mensagem de sucesso:
  - Sem cascata: "Nível hierárquico {codigo} inativado com sucesso"
  - Com cascata: "Nível hierárquico {codigo} e {quantidade} filhos inativados com sucesso"
- **FP-UC04-013:** Sistema redireciona para listagem

### Fluxos Alternativos
- **FA-UC04-001:** Cancelar inativação
  - Usuário clica em "Cancelar" no modal de confirmação
  - Sistema fecha modal sem executar inativação
- **FA-UC04-002:** Inativar múltiplos registros (lote)
  - Usuário seleciona múltiplos registros na listagem
  - Usuário clica em "Inativar Selecionados"
  - Sistema valida cada registro individualmente
  - Sistema executa inativação em lote

### Fluxos de Exceção
- **FE-UC04-001:** Nível possui filhos ativos e usuário não confirma cascata
  - Sistema detecta filhos ativos (RN-RF017-03)
  - Usuário cancela confirmação de cascata
  - Sistema retorna HTTP 400
  - Sistema exibe mensagem: "Não é possível inativar {nivel} com {quantidade} {nivel_filho}(s) ativo(s)"
  - Sistema lista os filhos ativos
- **FE-UC04-002:** Registro já inativo
  - Registro já possui `deleted_at` preenchido
  - Sistema retorna HTTP 400
  - Sistema exibe mensagem: "Registro já está inativo"
- **FE-UC04-003:** Registro não pertence ao conglomerado
  - Registro pertence a outro conglomerado
  - Sistema retorna HTTP 404
  - Sistema exibe mensagem: "Registro não encontrado"
- **FE-UC04-004:** Usuário sem permissão
  - Sistema detecta falta de permissão `hierarquia.delete`
  - Sistema retorna HTTP 403
  - Sistema exibe mensagem: "Acesso negado"

### Regras de Negócio
- **RN-UC-04-001:** Inativação DEVE ser sempre lógica (soft delete) via `deleted_at` (RN-RF017-03)
- **RN-UC-04-002:** Sistema DEVE verificar filhos ativos ANTES de permitir inativação (RN-RF017-03)
- **RN-UC-04-003:** Sistema DEVE exigir confirmação explícita do usuário
- **RN-UC-04-004:** `deleted_at` preenchido com timestamp atual
- **RN-UC-04-005:** `deleted_by` preenchido com ID do usuário autenticado
- **RN-UC-04-006:** Se cascata, auditoria DEVE registrar cada inativação individual (RN-RF017-12)
- **RN-UC-04-007:** Registro inativado NÃO deve aparecer em listagens padrão (UC00)

### Critérios de Aceite
- **CA-UC04-001:** Inativação DEVE ser sempre lógica (soft delete) via `deleted_at`
- **CA-UC04-002:** Sistema DEVE verificar filhos ativos ANTES de permitir inativação
- **CA-UC04-003:** Sistema DEVE exigir confirmação explícita do usuário
- **CA-UC04-004:** `deleted_at` DEVE ser preenchido com timestamp atual
- **CA-UC04-005:** Tentativa de inativar nível com filhos ativos (sem cascata) DEVE retornar HTTP 400
- **CA-UC04-006:** Registro inativado NÃO deve aparecer em listagens padrão
- **CA-UC04-007:** Se cascata, retornar lista de IDs inativados
- **CA-UC04-008:** Auditoria DEVE registrar cada inativação (mesmo em cascata)

---

## 4. MATRIZ DE RASTREABILIDADE

| UC | Regras de Negócio do RF |
|----|-------------------------|
| UC00 | RN-RF017-09 (Multi-tenancy), RN-RF017-10 (Auditoria) |
| UC01 | RN-RF017-01, RN-RF017-02, RN-RF017-04, RN-RF017-05, RN-RF017-06, RN-RF017-07, RN-RF017-09, RN-RF017-10, RN-RF017-11 |
| UC02 | RN-RF017-09, RN-RF017-10 |
| UC03 | RN-RF017-04, RN-RF017-05, RN-RF017-07, RN-RF017-08, RN-RF017-09, RN-RF017-10, RN-RF017-11 |
| UC04 | RN-RF017-03, RN-RF017-09, RN-RF017-10, RN-RF017-12 |

---

## CHANGELOG

| Versão | Data | Autor | Descrição |
|------|------|-------|-----------|
| 2.0 | 2025-12-31 | Agência ALC - alc.dev.br | Versão canônica orientada a contrato. Cobertura 100% do RF017. |
| 1.0 | 2025-12-17 | Agência ALC - alc.dev.br | Versão inicial (não seguia template) |
