# UC-RF002 — Casos de Uso Canônicos

**RF:** RF-002 — Sistema de Configurações e Parametrização Avançada
**Epic:** EPIC001-SYS - Sistema e Infraestrutura
**Fase:** Fase 1 - Fundação e Cadastros Base
**Versão:** 2.0
**Data:** 2025-12-29
**Autor:** Agência ALC - alc.dev.br

---

## 1. OBJETIVO DO DOCUMENTO

Este documento descreve **todos os Casos de Uso (UC)** derivados do **RF-002**, cobrindo integralmente o comportamento funcional esperado do Sistema de Configurações e Parametrização Avançada.

Os UCs aqui definidos servem como **contrato comportamental**, sendo a **fonte primária** para geração de:
- Casos de Teste (TC-RF002.yaml)
- Massas de Teste (MT-RF002.yaml)
- Evidências de auditoria e validação funcional
- Execução por agentes de IA (tester, QA, E2E)

**Cobertura**: Este documento cobre **100% das funcionalidades** descritas no RF-002, incluindo:
- CRUD completo de configurações
- Hierarquia multi-tenant
- Criptografia automática com Azure Key Vault
- Cache Redis hot-reload
- Versionamento e rollback
- Feature flags com rollout progressivo
- Export/Import de configurações
- Auditoria SOX completa
- Validação de tipos e valores
- Dry-run e simulação de impacto

---

## 2. SUMÁRIO DE CASOS DE USO

| ID | Nome | Ator Principal | Cobertura RF-002 |
|----|------|----------------|------------------|
| UC00 | Listar Configurações | Usuário Autenticado | RF-CRUD-02, RN-RF002-01 (hierarquia multi-tenant), RN-RF002-09 (mascaramento senhas) |
| UC01 | Criar Configuração | Usuário Autenticado | RF-CRUD-01, RN-RF002-02 (criptografia), RN-RF002-03 (validação tipo), RN-RF002-04 (validação customizada), RN-RF002-05 (invalidação cache), RN-RF002-06 (versionamento), RN-RF002-11 (auditoria SOX) |
| UC02 | Visualizar Configuração | Usuário Autenticado | RF-CRUD-03, RN-RF002-09 (mascaramento senhas), RN-RF002-06 (histórico versionamento) |
| UC03 | Editar Configuração | Usuário Autenticado | RF-CRUD-04, RN-RF002-03 (validação tipo), RN-RF002-04 (validação customizada), RN-RF002-05 (invalidação cache), RN-RF002-06 (versionamento automático), RN-RF002-07 (rollback), RN-RF002-11 (auditoria SOX), RN-RF002-12 (notificações críticas), RN-RF002-14 (dry-run) |
| UC04 | Excluir Configuração | Usuário Autenticado | RF-CRUD-05, RN-RF002-05 (invalidação cache), RN-RF002-11 (auditoria), RN-RF002-13 (proteção somente leitura) |

**Casos de Uso Adicionais Específicos do RF-002:**

| ID | Nome | Ator Principal | Cobertura RF-002 |
|----|------|----------------|------------------|
| UC05 | Executar Rollback de Configuração | Super Admin / Admin DevOps | RN-RF002-07 (rollback 1-click), RN-RF002-06 (versionamento), RN-RF002-11 (auditoria), RN-RF002-12 (notificações) |
| UC06 | Gerenciar Feature Flags | Super Admin / Admin DevOps | RN-RF002-08 (rollout progressivo), RN-RF002-15 (expiração automática), RN-RF002-12 (notificações) |
| UC07 | Exportar Configurações | Admin DevOps / Gerente Operações / Auditor | RN-RF002-10 (export YAML), RN-RF002-11 (auditoria) |
| UC08 | Importar Configurações | Super Admin / Admin DevOps | RN-RF002-10 (import YAML, validação schema, dry-run), RN-RF002-11 (auditoria), RN-RF002-14 (dry-run) |
| UC09 | Descriptografar Valor Sensível | Super Admin | RN-RF002-02 (Azure Key Vault), RN-RF002-09 (permissão DECRYPT), RN-RF002-11 (auditoria acesso) |

---

## 3. PADRÕES GERAIS APLICÁVEIS A TODOS OS UCs

- Todos os acessos respeitam **isolamento por tenant** (RN-RF002-01)
- Todas as ações exigem **permissão explícita** (8 permissões RBAC)
- Erros não devem vazar informações sensíveis (valores criptografados retornam `********`)
- Auditoria deve registrar **quem**, **quando**, **IP**, **motivo** e **diff JSON** (RN-RF002-11)
- Mensagens devem ser claras, previsíveis e rastreáveis
- Cache Redis deve ser invalidado automaticamente após mudanças (RN-RF002-05)
- Valores sensíveis devem ser criptografados automaticamente com Azure Key Vault (RN-RF002-02)

---

## UC00 — Listar Configurações

### Objetivo
Permitir que o usuário visualize configurações disponíveis respeitando hierarquia multi-tenant e mascaramento de valores sensíveis.

### Pré-condições
- Usuário autenticado
- Permissão `SYS.CONFIGURACOES.READ`

### Pós-condições
- Lista exibida conforme filtros, paginação e hierarquia multi-tenant
- Valores sensíveis mascarados como `********` (exceto se usuário tiver permissão `SYS.CONFIGURACOES.DECRYPT`)

### Fluxo Principal
1. Usuário acessa funcionalidade "Configurações do Sistema"
2. Sistema valida permissão `SYS.CONFIGURACOES.READ`
3. Sistema carrega configurações respeitando hierarquia multi-tenant:
   - Se configuração existe em nível Usuário → exibe valor do Usuário
   - Senão, busca em Departamento → Empresa → Conglomerado → Global
4. Sistema mascara valores sensíveis (`Fl_Criptografado = 1`) como `********`
5. Sistema aplica paginação padrão (50 registros)
6. Sistema aplica ordenação padrão (por categoria e nome)
7. Sistema exibe lista hierárquica com categorização:
   - Sistema, Email, Integração, Segurança, Notificação, Cache, Storage, Auditoria, Performance, Features

### Fluxos Alternativos
- **FA-UC00-001: Buscar por termo**
  - Usuário digita termo no campo de busca
  - Sistema filtra configurações por código, nome ou descrição (case-insensitive)
  - Sistema exibe resultados filtrados

- **FA-UC00-002: Ordenar por coluna**
  - Usuário clica no header de coluna (Código, Nome, Categoria, Tipo Dado, Valor)
  - Sistema reordena lista (ascendente/descendente)
  - Sistema exibe lista reordenada

- **FA-UC00-003: Filtrar por categoria**
  - Usuário seleciona categoria no dropdown
  - Sistema exibe apenas configurações da categoria selecionada

- **FA-UC00-004: Filtrar por nível hierárquico**
  - Usuário seleciona nível (Global, Conglomerado, Empresa, Departamento, Usuário)
  - Sistema exibe apenas configurações do nível selecionado

- **FA-UC00-005: Visualizar apenas configurações sensíveis**
  - Usuário marca checkbox "Exibir apenas sensíveis"
  - Sistema filtra configurações com `Fl_Criptografado = 1`

### Fluxos de Exceção
- **FE-UC00-001: Usuário sem permissão**
  - Sistema retorna HTTP 403 Forbidden
  - Mensagem: "Você não possui permissão para visualizar configurações do sistema"

- **FE-UC00-002: Nenhuma configuração disponível**
  - Sistema exibe estado vazio com botão "Criar Nova Configuração" (se usuário tiver permissão CREATE)

- **FE-UC00-003: Erro ao carregar cache Redis**
  - Sistema faz fallback para leitura direta do banco de dados
  - Exibe aviso: "Cache indisponível, performance degradada"
  - Registra erro no log

### Regras de Negócio
- **RN-UC00-001**: Somente configurações do tenant do usuário (isolamento por `Id_Conglomerado` e `Id_Empresa`)
- **RN-UC00-002**: Configurações soft-deleted (`Fl_Excluido = 1`) não aparecem
- **RN-UC00-003**: Paginação padrão 50 registros (configurável)
- **RN-UC00-004**: Valores sensíveis mascarados como `********` (exceto com permissão `DECRYPT`)
- **RN-UC00-005**: Hierarquia multi-tenant: Usuário → Departamento → Empresa → Conglomerado → Global

---

## UC01 — Criar Configuração

### Objetivo
Permitir a criação de uma nova configuração válida com criptografia automática de valores sensíveis, validação de tipo, invalidação de cache e auditoria completa.

### Pré-condições
- Usuário autenticado
- Permissão `SYS.CONFIGURACOES.CREATE`

### Pós-condições
- Configuração persistida no banco de dados
- Valor sensível criptografado com Azure Key Vault (se `Fl_Criptografado = 1`)
- Cache Redis invalidado via pub/sub
- Versionamento inicial criado
- Auditoria SOX registrada (quem, quando, IP, motivo)

### Fluxo Principal
1. Usuário solicita criação de nova configuração (botão "Nova Configuração")
2. Sistema valida permissão `SYS.CONFIGURACOES.CREATE`
3. Sistema exibe formulário hierarquizado por abas:
   - **Aba Geral**: Código, Nome, Descrição, Categoria, Grupo Visual
   - **Aba Valor**: Tipo Dado, Valor, Valor Padrão
   - **Aba Validação**: Validação Regex, Valores Permitidos, Min/Max
   - **Aba Segurança**: Criptografado (checkbox), Somente Leitura (checkbox), Crítica (checkbox)
   - **Aba Multi-Tenancy**: Nível (Global/Conglomerado/Empresa/Departamento/Usuário)
   - **Aba Feature Flag** (opcional): Habilitar Feature Flag, Estratégia Rollout, Data Expiração
4. Usuário preenche campos obrigatórios:
   - Código (ex: `SMTP_Host`)
   - Nome (ex: "Host do servidor SMTP")
   - Categoria (ex: Email)
   - Tipo Dado (ex: String)
   - Valor
5. Usuário marca checkbox "Criptografado" se valor sensível (senha, API key, token)
6. Usuário clica em "Salvar"
7. Sistema valida dados:
   - Código único por tenant (`WHERE Nm_Codigo = ? AND Id_Conglomerado = ? AND Fl_Excluido = 0`)
   - Tipo de dado válido (String, Integer, Decimal, Boolean, JSON, Enum, DateTime)
   - Valor compatível com tipo escolhido
   - Validação customizada (regex, ranges, valores permitidos)
8. Se `Fl_Criptografado = 1`:
   - Sistema invoca Azure Key Vault
   - Criptografa valor com AES-256-GCM
   - Armazena valor criptografado no banco
9. Sistema persiste configuração com campos automáticos:
   - `Id_Conglomerado` (do usuário logado)
   - `Id_Empresa` (se nível Empresa/Departamento/Usuário)
   - `Dt_Criacao` (timestamp atual)
   - `Id_Usuario_Criacao` (usuário logado)
   - `Fl_Excluido = 0`
10. Sistema cria versionamento inicial:
    - Tabela `SistemaConfiguracaoHistorico`
    - `Nm_Versao = "1.0"`
    - `Ds_DiffJson` = valor inicial serializado
11. Sistema invalida cache Redis:
    - Publica evento `config:invalidate:SMTP_Host` no canal pub/sub
    - Todas instâncias da API recebem evento e invalidam cache local
12. Sistema registra auditoria SOX:
    - Tabela `AuditLog`
    - Ação: `CREATE_CONFIGURACAO`
    - Usuário, IP, User-Agent, Timestamp
    - Motivo (campo texto livre obrigatório)
    - Diff JSON (valor criado)
13. Sistema confirma sucesso:
    - Mensagem: "Configuração criada com sucesso"
    - Redireciona para listagem

### Fluxos Alternativos
- **FA-UC01-001: Salvar e criar outra**
  - Usuário clica em "Salvar e Criar Outra"
  - Sistema salva configuração atual
  - Sistema limpa formulário
  - Sistema mantém usuário na tela de criação

- **FA-UC01-002: Cancelar criação**
  - Usuário clica em "Cancelar"
  - Sistema exibe confirmação: "Descartar alterações?"
  - Se confirmado, redireciona para listagem

- **FA-UC01-003: Criar configuração sensível**
  - Usuário marca checkbox "Criptografado"
  - Sistema exibe aviso: "Valor será criptografado com Azure Key Vault. Não será possível visualizar em texto claro após salvar (exceto com permissão DECRYPT)"
  - Sistema desabilita preview do valor

- **FA-UC01-004: Criar feature flag**
  - Usuário marca checkbox "Habilitar Feature Flag"
  - Sistema exibe aba "Feature Flag"
  - Sistema valida estratégia de rollout selecionada
  - Sistema valida data de expiração (futuro obrigatório)

### Fluxos de Exceção
- **FE-UC01-001: Erro de validação**
  - Sistema retorna HTTP 400 Bad Request
  - Mensagem específica por campo:
    - Código duplicado: "Configuração com código 'SMTP_Host' já existe para este tenant"
    - Tipo inválido: "Valor '999999' inválido para tipo Integer (max: 65535)"
    - Regex falhou: "E-mail inválido, formato esperado: exemplo@dominio.com"
    - Range violado: "Porta SMTP deve estar entre 1 e 65535"

- **FE-UC01-002: Configuração duplicada**
  - Sistema retorna HTTP 409 Conflict
  - Mensagem: "Configuração com código 'SMTP_Host' já existe para este tenant. Deseja editar a existente?"
  - Botão "Editar Existente" redireciona para UC03

- **FE-UC01-003: Azure Key Vault indisponível**
  - Sistema retorna HTTP 503 Service Unavailable
  - Mensagem: "Serviço de criptografia temporariamente indisponível. Tente novamente em alguns instantes."
  - Sistema registra erro no log
  - Sistema envia alerta para equipe DevOps

- **FE-UC01-004: Erro inesperado**
  - Sistema retorna HTTP 500 Internal Server Error
  - Mensagem genérica: "Erro ao criar configuração. Tente novamente ou contate o suporte."
  - Sistema registra stack trace completo no log
  - Sistema NÃO vaza detalhes técnicos ao usuário

### Regras de Negócio
- **RN-UC01-001**: Campos obrigatórios: Código, Nome, Categoria, Tipo Dado, Valor
- **RN-UC01-002**: `Id_Conglomerado` e `Id_Empresa` automáticos (multi-tenancy)
- **RN-UC01-003**: `Dt_Criacao`, `Id_Usuario_Criacao` automáticos
- **RN-UC01-004**: Código único por tenant (case-insensitive)
- **RN-UC01-005**: Validação de tipo antes de persistir (RN-RF002-03)
- **RN-UC01-006**: Criptografia automática se `Fl_Criptografado = 1` (RN-RF002-02)
- **RN-UC01-007**: Invalidação cache Redis via pub/sub (RN-RF002-05)
- **RN-UC01-008**: Versionamento inicial 1.0 (RN-RF002-06)
- **RN-UC01-009**: Auditoria SOX completa (RN-RF002-11)
- **RN-UC01-010**: Validação customizada (regex, ranges, valores permitidos) (RN-RF002-04)

---

## UC02 — Visualizar Configuração

### Objetivo
Permitir visualização detalhada de uma configuração incluindo histórico de versões, mascaramento de valores sensíveis e auditoria de acessos.

### Pré-condições
- Usuário autenticado
- Permissão `SYS.CONFIGURACOES.READ`

### Pós-condições
- Dados da configuração exibidos corretamente
- Valores sensíveis mascarados (exceto com permissão `DECRYPT`)
- Histórico de versões exibido com diff visual
- Acesso auditado (se configuração sensível)

### Fluxo Principal
1. Usuário seleciona configuração na listagem (UC00)
2. Sistema valida permissão `SYS.CONFIGURACOES.READ`
3. Sistema valida tenant (configuração pertence ao tenant do usuário)
4. Sistema carrega dados da configuração do cache Redis (ou banco se cache miss)
5. Sistema carrega histórico de versões (tabela `SistemaConfiguracaoHistorico`)
6. Se `Fl_Criptografado = 1`:
   - Sistema exibe valor como `********`
   - Sistema exibe aviso: "Valor sensível. Requer permissão DECRYPT para visualizar"
   - Se usuário tiver permissão `SYS.CONFIGURACOES.DECRYPT`:
     - Sistema exibe botão "Revelar Valor"
7. Sistema exibe dados em abas:
   - **Aba Geral**: Código, Nome, Descrição, Categoria, Grupo Visual, Status
   - **Aba Valor**: Tipo Dado, Valor (mascarado se sensível), Valor Padrão
   - **Aba Validação**: Validação Regex, Valores Permitidos, Min/Max
   - **Aba Segurança**: Criptografado, Somente Leitura, Crítica
   - **Aba Multi-Tenancy**: Nível, Conglomerado, Empresa, Departamento, Usuário
   - **Aba Feature Flag** (se aplicável): Estratégia Rollout, Data Expiração, Status
   - **Aba Histórico**: Lista de versões com diff visual (JSON comparado)
   - **Aba Auditoria**: Log completo de acessos e modificações
8. Sistema exibe dados

### Fluxos Alternativos
- **FA-UC02-001: Revelar valor sensível** → Ver UC09

- **FA-UC02-002: Comparar versões**
  - Usuário seleciona 2 versões na aba Histórico
  - Sistema exibe diff visual lado a lado:
    - Campos adicionados (verde)
    - Campos removidos (vermelho)
    - Campos alterados (amarelo com antes/depois)

- **FA-UC02-003: Ver auditoria completa**
  - Usuário clica em "Ver Auditoria Completa"
  - Sistema exibe timeline de eventos:
    - Criação, edições, rollbacks, acessos a valores sensíveis
    - Quem, quando, IP, user-agent, motivo, diff JSON

### Fluxos de Exceção
- **FE-UC02-001: Configuração inexistente**
  - Sistema retorna HTTP 404 Not Found
  - Mensagem: "Configuração não encontrada ou foi excluída"

- **FE-UC02-002: Configuração de outro tenant**
  - Sistema retorna HTTP 403 Forbidden
  - Mensagem: "Você não possui permissão para visualizar esta configuração"

- **FE-UC02-003: Azure Key Vault indisponível (ao descriptografar)**
  - Sistema retorna HTTP 503 Service Unavailable
  - Mensagem: "Serviço de descriptografia temporariamente indisponível"

### Regras de Negócio
- **RN-UC02-001**: Isolamento por tenant obrigatório
- **RN-UC02-002**: Auditoria de acesso a valores sensíveis (RN-RF002-11)
- **RN-UC02-003**: Mascaramento automático de valores sensíveis (RN-RF002-09)
- **RN-UC02-004**: Histórico de versões exibido com diff visual (RN-RF002-06)
- **RN-UC02-005**: Descriptografia apenas com permissão `DECRYPT` (RN-RF002-09)

---

## UC03 — Editar Configuração

### Objetivo
Permitir alteração controlada de uma configuração com validação, versionamento automático, rollback, dry-run, invalidação de cache e notificações para configurações críticas.

### Pré-condições
- Usuário autenticado
- Permissão `SYS.CONFIGURACOES.UPDATE`
- Configuração NÃO marcada como somente leitura (`Fl_SomenteLeitura = 0`)

### Pós-condições
- Configuração atualizada no banco de dados
- Nova versão criada no histórico com diff JSON completo
- Cache Redis invalidado via pub/sub
- Auditoria SOX registrada
- Notificação Slack/Teams enviada (se configuração crítica)

### Fluxo Principal
1. Usuário solicita edição de configuração (botão "Editar" em UC00 ou UC02)
2. Sistema valida permissão `SYS.CONFIGURACOES.UPDATE`
3. Sistema valida que configuração NÃO é somente leitura
4. Sistema carrega dados atuais no formulário (mesmas abas do UC01)
5. Usuário altera dados desejados (ex: mudar `SMTP_Port` de 587 para 465)
6. Usuário preenche campo **obrigatório** "Motivo da Alteração"
7. Se configuração crítica (`Fl_Critica = 1`):
   - Sistema exibe aviso: "Configuração crítica. Executar dry-run antes de salvar?"
   - Se confirmado, executa FA-03-04 (Dry-Run)
8. Usuário clica em "Salvar"
9. Sistema valida alterações:
   - Tipo de dado compatível
   - Validação customizada (regex, ranges, valores permitidos)
   - Motivo da alteração preenchido
10. Sistema cria nova versão no histórico:
    - `Nm_Versao` incrementada (ex: "1.0" → "1.1")
    - `Ds_DiffJson` com comparação antes/depois
    - `Ds_MotivoAlteracao` (obrigatório)
11. Sistema persiste alterações:
    - Atualiza registro em `SistemaConfiguracaoGeral`
    - `Dt_Atualizacao` = timestamp atual
    - `Id_Usuario_Atualizacao` = usuário logado
12. Sistema invalida cache Redis:
    - Publica evento `config:invalidate:SMTP_Port` no canal pub/sub
    - Todas instâncias recebem e invalidam cache
13. Sistema registra auditoria SOX:
    - Ação: `UPDATE_CONFIGURACAO`
    - Diff JSON completo (valor anterior vs novo)
    - Motivo da alteração
14. Se `Fl_Critica = 1`:
    - Sistema envia notificação Slack/Teams:
      - "⚠️ Configuração crítica alterada: SMTP_Port"
      - "Autor: João Silva"
      - "Motivo: Migração para TLS 1.3"
      - "Diff: 587 → 465"
15. Sistema confirma sucesso:
    - Mensagem: "Configuração atualizada com sucesso. Nova versão: 1.1"

### Fluxos Alternativos
- **FA-UC03-001: Cancelar edição**
  - Usuário clica em "Cancelar"
  - Sistema exibe confirmação: "Descartar alterações?"
  - Se confirmado, retorna para UC02

- **FA-UC03-002: Editar valor sensível**
  - Usuário tenta editar configuração com `Fl_Criptografado = 1`
  - Sistema exibe campo de entrada mascarado
  - Sistema exibe aviso: "Novo valor será criptografado automaticamente ao salvar"
  - Sistema NÃO exibe valor atual em texto claro (segurança)

- **FA-UC03-003: Executar rollback**
  - Usuário clica em "Rollback" na aba Histórico
  - Redireciona para UC05 (Executar Rollback)

- **FA-UC03-004: Dry-Run (Simulação de Impacto)**
  - Sistema simula aplicação da mudança SEM persistir
  - Sistema retorna relatório de impacto:
    - Quantos usuários/empresas afetados
    - Quais serviços precisam invalidar cache
    - Riscos conhecidos (ex: "Mudança de porta SMTP pode quebrar envio de e-mails")
    - Recomendações (ex: "Testar em HOM primeiro")
  - Usuário decide se confirma ou cancela alteração

### Fluxos de Exceção
- **FE-UC03-001: Erro de validação**
  - Sistema retorna HTTP 400 Bad Request
  - Mensagem específica por campo violado

- **FE-UC03-002: Configuração somente leitura**
  - Sistema retorna HTTP 403 Forbidden
  - Mensagem: "Configuração protegida. Não pode ser editada. Contate Super Admin."

- **FE-UC03-003: Conflito de edição concorrente**
  - Usuário A e B editam mesma configuração simultaneamente
  - Usuário B salva primeiro
  - Quando A tenta salvar:
    - Sistema detecta conflito (versão mudou)
    - Sistema retorna HTTP 409 Conflict
    - Mensagem: "Configuração foi alterada por outro usuário. Recarregue e tente novamente."

- **FE-UC03-004: Falha ao enviar notificação Slack/Teams**
  - Sistema registra erro no log
  - Sistema NÃO bloqueia salvamento da configuração
  - Sistema envia alerta interno para equipe DevOps

### Regras de Negócio
- **RN-UC03-001**: `Dt_Atualizacao` e `Id_Usuario_Atualizacao` automáticos
- **RN-UC03-002**: Motivo da alteração obrigatório (RN-RF002-11)
- **RN-UC03-003**: Versionamento automático com incremento (RN-RF002-06)
- **RN-UC03-004**: Invalidação cache pub/sub (RN-RF002-05)
- **RN-UC03-005**: Notificação automática se crítica (RN-RF002-12)
- **RN-UC03-006**: Dry-run obrigatório se crítica (RN-RF002-14)
- **RN-UC03-007**: Configuração somente leitura bloqueada (RN-RF002-13)

---

## UC04 — Excluir Configuração

### Objetivo
Permitir exclusão lógica (soft delete) de configurações com invalidação de cache e auditoria.

### Pré-condições
- Usuário autenticado
- Permissão `SYS.CONFIGURACOES.DELETE`
- Configuração NÃO marcada como somente leitura (`Fl_SomenteLeitura = 0`)

### Pós-condições
- Configuração marcada como excluída (`Fl_Excluido = 1`)
- Cache Redis invalidado
- Auditoria registrada

### Fluxo Principal
1. Usuário solicita exclusão (botão "Excluir" em UC00 ou UC02)
2. Sistema exibe confirmação: "Confirma exclusão da configuração 'SMTP_Host'? Esta ação pode ser revertida."
3. Usuário confirma
4. Sistema valida permissão `SYS.CONFIGURACOES.DELETE`
5. Sistema valida que configuração NÃO é somente leitura
6. Sistema executa soft delete:
   - `Fl_Excluido = 1`
   - `Dt_Exclusao` = timestamp atual
   - `Id_Usuario_Exclusao` = usuário logado
7. Sistema invalida cache Redis (pub/sub)
8. Sistema registra auditoria:
   - Ação: `DELETE_CONFIGURACAO`
9. Sistema confirma sucesso:
   - Mensagem: "Configuração excluída com sucesso"

### Fluxos Alternativos
- **FA-UC04-001: Cancelar exclusão**
  - Usuário clica em "Cancelar" na confirmação
  - Sistema retorna para tela anterior

- **FA-UC04-002: Restaurar configuração excluída**
  - Usuário acessa listagem de "Configurações Excluídas"
  - Usuário clica em "Restaurar"
  - Sistema marca `Fl_Excluido = 0`
  - Sistema registra auditoria

### Fluxos de Exceção
- **FE-UC04-001: Configuração já excluída**
  - Sistema retorna HTTP 404 Not Found
  - Mensagem: "Configuração não encontrada ou já foi excluída"

- **FE-UC04-002: Configuração somente leitura**
  - Sistema retorna HTTP 403 Forbidden
  - Mensagem: "Configuração protegida. Não pode ser excluída."

### Regras de Negócio
- **RN-UC04-001**: Exclusão sempre lógica (soft delete) (RN-RF002-06)
- **RN-UC04-002**: Configuração somente leitura bloqueada (RN-RF002-13)
- **RN-UC04-003**: Invalidação cache automática (RN-RF002-05)

---

## UC05 — Executar Rollback de Configuração

### Objetivo
Restaurar configuração para versão anterior em 1-click com auditoria completa.

### Pré-condições
- Usuário autenticado
- Permissão `SYS.CONFIGURACOES.ROLLBACK`
- Existir histórico de versões (versão > 1.0)

### Pós-condições
- Configuração restaurada para versão anterior
- Nova versão criada no histórico (rollback não altera versões antigas)
- Cache invalidado
- Notificação enviada
- Auditoria registrada

### Fluxo Principal
1. Usuário acessa aba "Histórico" (UC02)
2. Usuário seleciona versão desejada (ex: v1.0 - valor `SMTP_Port = 587`)
3. Usuário clica em "Rollback para esta versão"
4. Sistema exibe confirmação com diff:
   - "Reverter de: 465 (versão atual)"
   - "Para: 587 (versão 1.0)"
5. Usuário preenche motivo obrigatório (ex: "Rollback por falha após migração TLS")
6. Usuário confirma
7. Sistema valida permissão `ROLLBACK`
8. Sistema restaura valor da versão selecionada
9. Sistema cria nova versão no histórico:
   - `Nm_Versao` incrementada (ex: "1.2")
   - `Ds_DiffJson` com comparação (versão atual → versão restaurada)
   - `Ds_MotivoAlteracao` = "ROLLBACK: [motivo do usuário]"
   - `Id_Versao_Origem` = ID da versão restaurada
10. Sistema invalida cache Redis (pub/sub)
11. Sistema registra auditoria:
    - Ação: `ROLLBACK_CONFIGURACAO`
    - Versão origem e versão destino
12. Sistema envia notificação Slack/Teams:
    - "🔄 Rollback executado: SMTP_Port"
    - "Autor: João Silva"
    - "Motivo: Rollback por falha após migração TLS"
    - "Versão restaurada: 1.0 (valor: 587)"
13. Sistema confirma sucesso:
    - Mensagem: "Rollback executado com sucesso. Versão atual: 1.2 (restaurada da v1.0)"

### Fluxos de Exceção
- **FE-UC05-001: Versão origem não encontrada**
  - Sistema retorna HTTP 404
  - Mensagem: "Versão selecionada não existe no histórico"

### Regras de Negócio
- **RN-UC05-001**: Rollback cria nova versão (não altera histórico) (RN-RF002-07)
- **RN-UC05-002**: Motivo obrigatório (RN-RF002-11)
- **RN-UC05-003**: Notificação automática (RN-RF002-12)

---

## UC06 — Gerenciar Feature Flags

### Objetivo
Habilitar/desabilitar feature flags com rollout progressivo e expiração automática.

### Pré-condições
- Usuário autenticado
- Permissão `SYS.FEATURE_FLAGS.UPDATE`

### Pós-condições
- Feature flag habilitada/desabilitada
- Estratégia de rollout configurada
- Expiração automática agendada (se aplicável)

### Fluxo Principal
1. Usuário acessa configuração com `Fl_FeatureFlag = 1`
2. Usuário acessa aba "Feature Flag"
3. Usuário configura rollout:
   - **Estratégia Percentual**: "Habilitar para 25% dos usuários aleatoriamente"
   - **Estratégia Usuário**: "Habilitar apenas para IDs: 123, 456, 789"
   - **Estratégia Perfil**: "Habilitar apenas para perfis: Desenvolvedor, QA"
   - **Estratégia Empresa**: "Habilitar apenas para empresas: ID 10, 20"
4. Usuário define data de expiração (ex: 2025-01-31)
5. Usuário salva
6. Sistema valida configuração
7. Sistema persiste estratégia em JSON (`Ds_ConfiguracaoEstrategia`)
8. Sistema invalida cache de decisões de feature flags
9. Job diário verifica expiração:
   - Se `Dt_Expiracao <= HOJE`:
     - Desabilita flag automaticamente
     - Envia notificação Slack: "⏰ Feature flag 'NovoInterfaceRelatorios' expirada e desabilitada automaticamente"

### Regras de Negócio
- **RN-UC06-001**: 4 estratégias de rollout (RN-RF002-08)
- **RN-UC06-002**: Expiração automática por job (RN-RF002-15)
- **RN-UC06-003**: Notificação ao expirar (RN-RF002-12)

---

## UC07 — Exportar Configurações

### Objetivo
Exportar configurações em formato YAML para migração entre ambientes.

### Pré-condições
- Permissão `SYS.CONFIGURACOES.EXPORT`

### Pós-condições
- Arquivo YAML gerado com todas configurações
- Valores sensíveis mascarados no export
- Auditoria registrada

### Fluxo Principal
1. Usuário clica em "Exportar Configurações"
2. Sistema valida permissão `EXPORT`
3. Sistema gera YAML com todas configurações do tenant
4. Sistema mascara valores sensíveis como `********`
5. Sistema oferece download do arquivo `configuracoes-{tenant}-{data}.yaml`
6. Sistema registra auditoria

### Regras de Negócio
- **RN-UC07-001**: Valores sensíveis sempre mascarados no export (RN-RF002-10)

---

## UC08 — Importar Configurações

### Objetivo
Importar configurações de arquivo YAML com validação de schema e dry-run obrigatório.

### Pré-condições
- Permissão `SYS.CONFIGURACOES.IMPORT`

### Pós-condições
- Configurações importadas e validadas
- Dry-run executado antes de aplicar
- Auditoria completa registrada

### Fluxo Principal
1. Usuário clica em "Importar Configurações"
2. Usuário faz upload de arquivo YAML
3. Sistema valida schema YAML
4. Sistema executa dry-run obrigatório:
   - Simula importação SEM persistir
   - Retorna relatório de impacto
5. Usuário confirma
6. Sistema importa configurações
7. Sistema invalida cache
8. Sistema registra auditoria

### Regras de Negócio
- **RN-UC08-001**: Validação schema obrigatória (RN-RF002-10)
- **RN-UC08-002**: Dry-run obrigatório antes de aplicar (RN-RF002-14)

---

## UC09 — Descriptografar Valor Sensível

### Objetivo
Permitir que Super Admin visualize valor sensível descriptografado.

### Pré-condições
- Permissão `SYS.CONFIGURACOES.DECRYPT`

### Pós-condições
- Valor exibido em texto claro temporariamente (30s)
- Auditoria de acesso registrada

### Fluxo Principal
1. Usuário clica em "Revelar Valor" (FA-02-01)
2. Sistema solicita motivo obrigatório
3. Sistema valida permissão `DECRYPT`
4. Sistema descriptografa via Azure Key Vault
5. Sistema exibe valor por 30 segundos
6. Sistema re-mascara automaticamente
7. Sistema registra auditoria detalhada

### Regras de Negócio
- **RN-UC09-001**: Apenas Super Admin (RN-RF002-09)
- **RN-UC09-002**: Auditoria obrigatória (RN-RF002-11)

---

## 4. MATRIZ DE RASTREABILIDADE

| UC | Regras de Negócio RF-002 | Funcionalidades RF-002 |
|----|--------------------------|------------------------|
| UC00 | RN-RF002-01, RN-RF002-09 | RF-CRUD-02, Hierarquia Multi-Tenant, Mascaramento Senhas |
| UC01 | RN-RF002-02, RN-RF002-03, RN-RF002-04, RN-RF002-05, RN-RF002-06, RN-RF002-11 | RF-CRUD-01, Criptografia, Validação, Cache Hot-Reload, Versionamento, Auditoria SOX |
| UC02 | RN-RF002-06, RN-RF002-09, RN-RF002-11 | RF-CRUD-03, Histórico Versões, Mascaramento, Auditoria Acesso |
| UC03 | RN-RF002-03, RN-RF002-04, RN-RF002-05, RN-RF002-06, RN-RF002-07, RN-RF002-11, RN-RF002-12, RN-RF002-13, RN-RF002-14 | RF-CRUD-04, Validação, Cache, Versionamento, Rollback, Auditoria, Notificações, Proteção Somente Leitura, Dry-Run |
| UC04 | RN-RF002-05, RN-RF002-11, RN-RF002-13 | RF-CRUD-05, Soft Delete, Auditoria, Proteção |
| UC05 | RN-RF002-06, RN-RF002-07, RN-RF002-11, RN-RF002-12 | Rollback 1-Click, Versionamento, Auditoria, Notificações |
| UC06 | RN-RF002-08, RN-RF002-12, RN-RF002-15 | Feature Flags, Rollout Progressivo, Expiração Automática, Notificações |
| UC07 | RN-RF002-10, RN-RF002-11 | Export YAML, Auditoria |
| UC08 | RN-RF002-10, RN-RF002-11, RN-RF002-14 | Import YAML, Validação Schema, Dry-Run, Auditoria |
| UC09 | RN-RF002-02, RN-RF002-09, RN-RF002-11 | Descriptografia Azure Key Vault, Permissão DECRYPT, Auditoria Acesso |

**Cobertura Total**: 100% das funcionalidades do RF-002 cobertas pelos 10 UCs (UC00-UC09).

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|--------|------|-----------|-------|
| 2.0 | 2025-12-29 | 10 UCs completos cobrindo 100% do RF-002 - CRUD + Rollback + Feature Flags + Export/Import + Descriptografia. Sem furos, sem falhas, sem faltas. | Agência ALC - alc.dev.br |
