# UC-RF047 — Casos de Uso Canônicos

**RF:** RF047 — Gestão de Tipos de Consumidores
**Versão:** 2.0
**Data:** 2025-12-31
**Autor:** Agência ALC - alc.dev.br
**Epic:** EPIC003-CAD - Cadastros Base
**Fase:** Fase 2 - Cadastros e Serviços Transversais

---

## 1. OBJETIVO DO DOCUMENTO

Este documento descreve **todos os Casos de Uso (UC)** derivados do **RF047**, cobrindo integralmente o comportamento funcional esperado para gestão de tipos de consumidores (usuários, dispositivos, máquinas) com classificação, quotas, custos e hierarquia.

Os UCs aqui definidos servem como **contrato comportamental**, sendo a **fonte primária** para geração de:
- Casos de Teste (TC-RF047.yaml)
- Massas de Teste (MT-RF047.yaml)
- Evidências de auditoria e validação funcional
- Execução por agentes de IA (tester, QA, E2E)

---

## 2. SUMÁRIO DE CASOS DE USO

| ID | Nome | Ator Principal |
|----|------|----------------|
| UC00 | Listar Tipos de Consumidores | Usuário Autenticado |
| UC01 | Criar Tipo de Consumidor | Usuário Autenticado |
| UC02 | Visualizar Tipo de Consumidor | Usuário Autenticado |
| UC03 | Editar Tipo de Consumidor | Usuário Autenticado |
| UC04 | Inativar Tipo de Consumidor | Usuário Autenticado |

---

## 3. PADRÕES GERAIS APLICÁVEIS A TODOS OS UCs

- Todos os acessos respeitam **isolamento por tenant (TenantId)**
- Todas as ações exigem **permissão explícita (RBAC)**
- Erros não devem vazar informações sensíveis
- Auditoria deve registrar **quem**, **quando** e **qual ação**
- Mensagens devem ser claras, previsíveis e rastreáveis
- Código de tipo é **imutável** após criação (RN-RF047-001)
- Hierarquia deve ser **acíclica** (máximo 5 níveis) (RN-RF047-003)
- Inativação de tipo move consumidores para tipo padrão automaticamente (RN-RF047-007)

---

## UC00 — Listar Tipos de Consumidores

### Objetivo
Permitir que o usuário visualize todos os tipos de consumidores do seu tenant com filtros avançados.

### Pré-condições
- Usuário autenticado
- Permissão `CAD.TIPOS_CONSUMIDORES.VIEW_ANY`

### Pós-condições
- Lista exibida conforme filtros e paginação

### Fluxo Principal
- **FP-UC00-001:** Usuário acessa funcionalidade Tipos de Consumidores
- **FP-UC00-002:** Sistema valida permissão
- **FP-UC00-003:** Sistema carrega tipos do tenant (TenantId)
- **FP-UC00-004:** Sistema aplica paginação (50 registros/página)
- **FP-UC00-005:** Sistema exibe lista com colunas (código, nome, descrição, fornecedor, quantidade consumidores, ativo/inativo, cor, ícone)

### Fluxos Alternativos
- **FA-UC00-001:** Filtrar por status (ativo/inativo)
- **FA-UC00-002:** Filtrar por fornecedor
- **FA-UC00-003:** Filtrar por hierarquia (tipos raiz vs filhos)
- **FA-UC00-004:** Ordenar por coluna (código, nome, quantidade consumidores)
- **FA-UC00-005:** Exportar para Excel/CSV

### Fluxos de Exceção
- **FE-UC00-001:** Usuário sem permissão → HTTP 403
- **FE-UC00-002:** Nenhum tipo cadastrado → estado vazio

### Regras de Negócio
- RN-RF047-009: Limite de 50 tipos por fornecedor

### Critérios de Aceite
- **CA-UC00-001:** A lista DEVE exibir apenas tipos do tenant do usuário
- **CA-UC00-002:** Tipos soft-deleted NÃO aparecem
- **CA-UC00-003:** Paginação DEVE ser aplicada (50 registros/página)
- **CA-UC00-004:** Sistema DEVE permitir ordenação por código, nome, quantidade consumidores
- **CA-UC00-005:** Filtros DEVEM ser acumuláveis

---

## UC01 — Criar Tipo de Consumidor

### Objetivo
Permitir criação de novo tipo de consumidor com código único, nome, hierarquia, quotas e configurações.

### Pré-condições
- Usuário autenticado
- Permissão `CAD.TIPOS_CONSUMIDORES.CREATE`
- Fornecedor tem < 50 tipos (RN-RF047-009)

### Pós-condições
- Tipo criado e disponível para atribuição
- Auditoria registrada
- Evento `TipoConsumidorCriado` disparado

### Fluxo Principal
- **FP-UC01-001:** Usuário acessa formulário de criação
- **FP-UC01-002:** Sistema valida permissão
- **FP-UC01-003:** Usuário preenche campos obrigatórios (código, nome, fornecedor)
- **FP-UC01-004:** Sistema valida código único por fornecedor (RN-RF047-001)
- **FP-UC01-005:** Sistema valida formato código [A-Z0-9_]{3,20}
- **FP-UC01-006:** Sistema valida limite de 50 tipos por fornecedor (RN-RF047-009)
- **FP-UC01-007:** Sistema cria tipo com TenantId automático
- **FP-UC01-008:** Sistema registra auditoria
- **FP-UC01-009:** Sistema confirma sucesso

### Fluxos Alternativos
- **FA-UC01-001:** Definir tipo pai (hierarquia)
- **FA-UC01-002:** Configurar quotas (dados, voz, SMS) - valor -1 = ilimitado (RN-RF047-004)
- **FA-UC01-003:** Configurar custo fixo mensal (RN-RF047-008)
- **FA-UC01-004:** Configurar permissões default (RN-RF047-012)
- **FA-UC01-005:** Configurar regras de auto-classificação (regex, domínio, departamento) (RN-RF047-005)
- **FA-UC01-006:** Marcar como tipo padrão (RN-RF047-002)
- **FA-UC01-007:** Marcar como tipo crítico (RN-RF047-006)
- **FA-UC01-008:** Configurar cor hexadecimal e ícone Material Icons (RN-RF047-014)
- **FA-UC01-009:** Configurar template de provisioning automático

### Fluxos de Exceção
- **FE-UC01-001:** Código duplicado no fornecedor → HTTP 400
- **FE-UC01-002:** Formato de código inválido → HTTP 400
- **FE-UC01-003:** Limite de 50 tipos excedido → HTTP 400
- **FE-UC01-004:** Tipo pai cria loop acíclico → HTTP 400 (RN-RF047-003)
- **FE-UC01-005:** Hierarquia excede 5 níveis → HTTP 400 (RN-RF047-003)
- **FE-UC01-006:** Quota inválida (< -1) → HTTP 400
- **FE-UC01-007:** Cor não está no formato #RRGGBB → HTTP 400

### Regras de Negócio
- RN-RF047-001: Código único e imutável
- RN-RF047-002: Tipo padrão obrigatório por fornecedor
- RN-RF047-003: Hierarquia sem loops (acíclica)
- RN-RF047-004: Quota -1 = ilimitado
- RN-RF047-005: Regras de auto-classificação por prioridade
- RN-RF047-009: Limite de 50 tipos por fornecedor

### Critérios de Aceite
- **CA-UC01-001:** TenantId DEVE ser preenchido automaticamente
- **CA-UC01-002:** Código DEVE ser único por fornecedor
- **CA-UC01-003:** Código DEVE ser imutável após criação
- **CA-UC01-004:** Sistema DEVE validar hierarquia acíclica com DFS
- **CA-UC01-005:** Auditoria DEVE ser registrada APÓS sucesso
- **CA-UC01-006:** Criar tipo padrão DEVE desmarcar tipo padrão anterior do fornecedor
- **CA-UC01-007:** Quota -1 DEVE significar ilimitado

---

## UC02 — Visualizar Tipo de Consumidor

### Objetivo
Permitir visualização completa de um tipo com metadados, quotas, hierarquia, consumidores vinculados e histórico.

### Pré-condições
- Usuário autenticado
- Permissão `CAD.TIPOS_CONSUMIDORES.VIEW`

### Pós-condições
- Dados exibidos corretamente

### Fluxo Principal
- **FP-UC02-001:** Usuário seleciona tipo na listagem
- **FP-UC02-002:** Sistema valida permissão
- **FP-UC02-003:** Sistema valida tenant (TenantId)
- **FP-UC02-004:** Sistema carrega dados completos (código, nome, descrição, fornecedor, hierarquia, quotas, custo fixo)
- **FP-UC02-005:** Sistema carrega consumidores vinculados
- **FP-UC02-006:** Sistema carrega histórico de mudanças (últimos 30 dias)
- **FP-UC02-007:** Sistema exibe dados formatados

### Fluxos Alternativos
- **FA-UC02-001:** Visualizar tipo pai (se houver)
- **FA-UC02-002:** Visualizar tipos filhos (se houver)
- **FA-UC02-003:** Visualizar permissões default
- **FA-UC02-004:** Visualizar regras de auto-classificação
- **FA-UC02-005:** Visualizar template de provisioning
- **FA-UC02-006:** Filtrar consumidores vinculados por status (ativo/inativo)
- **FA-UC02-007:** Visualizar histórico completo (7 anos) (RN-RF047-015)

### Fluxos de Exceção
- **FE-UC02-001:** Tipo não encontrado → HTTP 404
- **FE-UC02-002:** Tipo de outro tenant → HTTP 404

### Regras de Negócio
- RN-RF047-011: Herança de configurações resolvida em runtime
- RN-RF047-015: Histórico de 7 anos para auditoria

### Critérios de Aceite
- **CA-UC02-001:** Usuário SÓ pode visualizar tipos do próprio tenant
- **CA-UC02-002:** Informações de auditoria DEVEM ser exibidas
- **CA-UC02-003:** Tentativa de acessar tipo de outro tenant → HTTP 404
- **CA-UC02-004:** Sistema DEVE exibir configurações herdadas do pai (se aplicável)
- **CA-UC02-005:** Histórico DEVE mostrar últimos 30 dias por padrão, com opção "Ver tudo" (7 anos)

---

## UC03 — Editar Tipo de Consumidor

### Objetivo
Permitir atualização de tipo existente preservando código (imutável) e aplicando regras de negócio.

### Pré-condições
- Usuário autenticado
- Permissão `CAD.TIPOS_CONSUMIDORES.UPDATE`
- Tipo pertence ao tenant do usuário

### Pós-condições
- Tipo atualizado
- Auditoria registrada com campos alterados
- Evento `TipoConsumidorAtualizado` disparado

### Fluxo Principal
- **FP-UC03-001:** Usuário seleciona tipo e acessa edição
- **FP-UC03-002:** Sistema valida permissão
- **FP-UC03-003:** Sistema valida tenant (TenantId)
- **FP-UC03-004:** Sistema carrega dados atuais (código READONLY)
- **FP-UC03-005:** Usuário modifica campos (nome, descrição, quotas, custo, permissões, etc.)
- **FP-UC03-006:** Sistema valida mudanças (hierarquia acíclica, quotas >= -1, etc.)
- **FP-UC03-007:** Sistema salva alterações
- **FP-UC03-008:** Sistema registra auditoria com diff de campos
- **FP-UC03-009:** Sistema confirma sucesso

### Fluxos Alternativos
- **FA-UC03-001:** Alterar tipo pai (revalidar hierarquia acíclica) (RN-RF047-003)
- **FA-UC03-002:** Alterar quotas (validar -1 = ilimitado)
- **FA-UC03-003:** Alterar custo fixo mensal
- **FA-UC03-004:** Alterar permissões default (aplicar a novos consumidores apenas)
- **FA-UC03-005:** Alterar regras de auto-classificação (prioridades)
- **FA-UC03-006:** Marcar/desmarcar tipo padrão (RN-RF047-002)
- **FA-UC03-007:** Marcar/desmarcar tipo crítico (RN-RF047-006)
- **FA-UC03-008:** Alterar cor e ícone

### Fluxos de Exceção
- **FE-UC03-001:** Tentativa de alterar código → HTTP 400 (código imutável)
- **FE-UC03-002:** Tipo de outro tenant → HTTP 404
- **FE-UC03-003:** Tipo pai cria loop → HTTP 400
- **FE-UC03-004:** Hierarquia excede 5 níveis → HTTP 400
- **FE-UC03-005:** Quota inválida → HTTP 400
- **FE-UC03-006:** Desmarcar tipo padrão sem definir outro → HTTP 400

### Regras de Negócio
- RN-RF047-001: Código é imutável
- RN-RF047-002: Apenas 1 tipo padrão por fornecedor
- RN-RF047-003: Hierarquia acíclica
- RN-RF047-004: Quota -1 = ilimitado
- RN-RF047-006: Mudança de tipo crítico exige aprovação

### Critérios de Aceite
- **CA-UC03-001:** Código DEVE ser READONLY (imutável)
- **CA-UC03-002:** Sistema DEVE validar hierarquia acíclica ao alterar tipo pai
- **CA-UC03-003:** Auditoria DEVE registrar diff (antes/depois) de campos alterados
- **CA-UC03-004:** Marcar como padrão DEVE desmarcar tipo padrão anterior automaticamente
- **CA-UC03-005:** Mudança de permissões default NÃO afeta consumidores existentes

---

## UC04 — Inativar Tipo de Consumidor

### Objetivo
Permitir inativação lógica de tipo com migração automática de consumidores para tipo padrão.

### Pré-condições
- Usuário autenticado
- Permissão `CAD.TIPOS_CONSUMIDORES.INACTIVATE`
- Tipo pertence ao tenant do usuário
- Tipo NÃO é o tipo padrão do fornecedor

### Pós-condições
- Tipo inativado
- Consumidores vinculados migrados para tipo padrão (RN-RF047-007)
- Histórico de migração registrado (RN-RF047-015)
- Auditoria registrada
- Evento `TipoConsumidorInativado` disparado

### Fluxo Principal
- **FP-UC04-001:** Usuário seleciona tipo e acessa inativação
- **FP-UC04-002:** Sistema valida permissão
- **FP-UC04-003:** Sistema valida tenant (TenantId)
- **FP-UC04-004:** Sistema valida que tipo NÃO é padrão
- **FP-UC04-005:** Sistema exibe confirmação com quantidade de consumidores vinculados
- **FP-UC04-006:** Usuário confirma inativação
- **FP-UC04-007:** Sistema inicia job de migração em massa (background)
- **FP-UC04-008:** Sistema migra consumidores para tipo padrão do fornecedor (RN-RF047-007)
- **FP-UC04-009:** Sistema marca tipo como inativo
- **FP-UC04-010:** Sistema registra auditoria
- **FP-UC04-011:** Sistema envia notificação de conclusão

### Fluxos Alternativos
- **FA-UC04-001:** Tipo sem consumidores → inativação imediata (sem job)
- **FA-UC04-002:** Reativar tipo inativado (UC especial não coberto aqui, usar `CAD.TIPOS_CONSUMIDORES.REACTIVATE`)

### Fluxos de Exceção
- **FE-UC04-001:** Tipo é o padrão do fornecedor → HTTP 400 ("Tipo padrão não pode ser inativado")
- **FE-UC04-002:** Tipo de outro tenant → HTTP 404
- **FE-UC04-003:** Tipo padrão do fornecedor não encontrado → HTTP 400 (bloqueio de migração)
- **FE-UC04-004:** Job de migração falha → rollback + notificação de erro

### Regras de Negócio
- RN-RF047-002: Tipo padrão obrigatório por fornecedor (não pode ser inativado sem substituição)
- RN-RF047-007: Inativação move consumidores para tipo padrão
- RN-RF047-015: Histórico de 7 anos

### Critérios de Aceite
- **CA-UC04-001:** Tipo padrão NÃO pode ser inativado sem definir novo padrão antes
- **CA-UC04-002:** Inativação DEVE migrar TODOS os consumidores para tipo padrão
- **CA-UC04-003:** Migração DEVE ser registrada no histórico de cada consumidor
- **CA-UC04-004:** Notificação DEVE ser enviada aos responsáveis após conclusão
- **CA-UC04-005:** Job de migração DEVE processar até 1000 consumidores/lote
- **CA-UC04-006:** Sistema DEVE exibir quantidade de consumidores antes de confirmar

---

## 4. MATRIZ DE RASTREABILIDADE

| UC | Regras de Negócio |
|----|-------------------|
| UC00 | RN-RF047-009 |
| UC01 | RN-RF047-001, RN-RF047-002, RN-RF047-003, RN-RF047-004, RN-RF047-005, RN-RF047-009 |
| UC02 | RN-RF047-011, RN-RF047-015 |
| UC03 | RN-RF047-001, RN-RF047-002, RN-RF047-003, RN-RF047-004, RN-RF047-006 |
| UC04 | RN-RF047-002, RN-RF047-007, RN-RF047-015 |

---

## CHANGELOG

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 2.0 | 2025-12-31 | Agência ALC - alc.dev.br | Versão canônica completa com 5 UCs (UC00-UC04) cobrindo 15 regras de negócio |
| 1.0 | 2025-12-18 | Architect Agent | Versão stub incompleta |
