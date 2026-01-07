# UC-RF060 — Casos de Uso Canônicos

**RF:** RF060 — Gestão de Tipos de Chamado
**Epic:** EPIC003-CAD - Cadastros Base
**Fase:** Fase 2 - Cadastros e Serviços Transversais
**Versão:** 2.0
**Data:** 2025-12-31
**Autor:** Agência ALC - alc.dev.br

---

## 1. OBJETIVO DO DOCUMENTO

Este documento descreve **todos os Casos de Uso (UC)** derivados do **RF060**, cobrindo integralmente o comportamento funcional esperado do sistema de gestão de tipos de chamados de Service Desk com classificação ITIL v4.

Os UCs aqui definidos servem como **contrato comportamental**, sendo a **fonte primária** para geração de:
- Casos de Teste (TC-RF060.yaml)
- Massas de Teste (MT-RF060.yaml)
- Evidências de auditoria e validação funcional
- Execução por agentes de IA (tester, QA, E2E)

---

## 2. SUMÁRIO DE CASOS DE USO

| ID | Nome | Ator Principal |
|----|------|----------------|
| UC00 | Listar Tipos de Chamado | Usuário Autenticado |
| UC01 | Criar Tipo de Chamado | Usuário Autenticado |
| UC02 | Visualizar Tipo de Chamado | Usuário Autenticado |
| UC03 | Editar Tipo de Chamado | Usuário Autenticado |
| UC04 | Inativar Tipo de Chamado | Usuário Autenticado |

---

## 3. PADRÕES GERAIS APLICÁVEIS A TODOS OS UCs

- Todos os acessos respeitam **isolamento por tenant (EmpresaId)**
- Todas as ações exigem **permissão explícita** (RBAC com GES.TIPOS_CHAMADO.*)
- Erros não devem vazar informações sensíveis
- Auditoria deve registrar **quem**, **quando** e **qual ação**
- Mensagens devem ser claras, previsíveis e rastreáveis
- **Classificação ITIL v4 obrigatória** (Incidente, Requisição, Mudança, Problema)
- **SLA configurável** por tipo e prioridade
- **Formulários dinâmicos** com validação
- **Templates de resolução** (knowledge base)
- **Escalonamento automático** configurável
- **Métricas ITIL** (MTTR, MTBF, FCR)

---

## UC00 — Listar Tipos de Chamado

### Objetivo
Permitir que o usuário visualize todos os tipos de chamado do seu tenant com métricas ITIL e estatísticas de uso.

### Pré-condições
- Usuário autenticado
- Permissão `GES.TIPOS_CHAMADO.VIEW`

### Pós-condições
- Lista exibida conforme filtros, paginação e isolamento por EmpresaId

### Fluxo Principal
- **FP-UC00-001:** Usuário acessa a funcionalidade de tipos de chamado
- **FP-UC00-002:** Sistema valida permissão GES.TIPOS_CHAMADO.VIEW
- **FP-UC00-003:** Sistema carrega registros do tenant (filtro EmpresaId)
- **FP-UC00-004:** Sistema aplica paginação (padrão 20 registros) e ordenação
- **FP-UC00-005:** Sistema exibe lista com colunas: Código, Nome, Categoria ITIL, SLA Padrão, Qtd Chamados, Status, Ações

### Fluxos Alternativos
- **FA-UC00-001:** Buscar por nome ou código
- **FA-UC00-002:** Ordenar por coluna (código, nome, categoria, quantidade chamados)
- **FA-UC00-003:** Filtrar por categoria ITIL (Incidente, Requisição, Mudança, Problema)
- **FA-UC00-004:** Filtrar por status (ativo, inativo)
- **FA-UC00-005:** Exportar lista para Excel

### Fluxos de Exceção
- **FE-UC00-001:** Usuário sem permissão → HTTP 403 Forbidden
- **FE-UC00-002:** Nenhum registro encontrado → estado vazio exibido

### Regras de Negócio
- **RN-UC00-001:** Somente registros do tenant (EmpresaId) do usuário autenticado
- **RN-UC00-002:** Registros soft-deleted não aparecem na listagem
- **RN-UC00-003:** Paginação padrão de 20 registros por página

### Critérios de Aceite
- **CA-UC00-001:** A lista DEVE exibir apenas registros do tenant do usuário autenticado (EmpresaId)
- **CA-UC00-002:** Registros excluídos NÃO devem aparecer na listagem
- **CA-UC00-003:** Paginação DEVE ser aplicada com limite padrão de 20 registros
- **CA-UC00-004:** Sistema DEVE permitir ordenação por qualquer coluna visível
- **CA-UC00-005:** Filtros DEVEM ser acumuláveis e refletir na URL

---

## UC01 — Criar Tipo de Chamado

### Objetivo
Permitir a criação de um novo tipo de chamado com classificação ITIL v4, SLA, formulários dinâmicos e templates.

### Pré-condições
- Usuário autenticado
- Permissão `GES.TIPOS_CHAMADO.CREATE`

### Pós-condições
- Tipo de chamado criado no banco de dados
- Auditoria registrada
- EmpresaId preenchido automaticamente

### Fluxo Principal
- **FP-UC01-001:** Usuário clica em "Novo Tipo de Chamado"
- **FP-UC01-002:** Sistema valida permissão GES.TIPOS_CHAMADO.CREATE
- **FP-UC01-003:** Sistema exibe formulário com campos obrigatórios e opcionais
- **FP-UC01-004:** Usuário informa dados (código, nome, categoria ITIL, SLA, formulários, templates)
- **FP-UC01-005:** Sistema valida dados conforme RN-RF060-001 a RN-RF060-015
- **FP-UC01-006:** Sistema cria registro com EmpresaId = tenant do usuário
- **FP-UC01-007:** Sistema registra auditoria
- **FP-UC01-008:** Sistema confirma sucesso

### Fluxos Alternativos
- **FA-UC01-001:** Salvar e configurar SLA imediatamente
- **FA-UC01-002:** Cancelar criação

### Fluxos de Exceção
- **FE-UC01-001:** Campo obrigatório ausente → HTTP 400
- **FE-UC01-002:** Código duplicado no mesmo tenant → HTTP 409 Conflict
- **FE-UC01-003:** Categoria ITIL inválida → HTTP 400 "Categoria ITIL inválida" (RN-RF060-001)
- **FE-UC01-004:** Formulário dinâmico com campos duplicados → HTTP 400 (RN-RF060-003)
- **FE-UC01-005:** Erro inesperado → HTTP 500

### Regras de Negócio
- **RN-UC01-001:** Campos obrigatórios: Código, Nome, Categoria ITIL
- **RN-UC01-002:** Categoria ITIL DEVE ser uma das 4 opções: Incidente, Requisição, Mudança, Problema (RN-RF060-001)
- **RN-UC01-003:** EmpresaId preenchido automaticamente com tenant do usuário autenticado
- **RN-UC01-004:** CreatedBy preenchido automaticamente com ID do usuário autenticado
- **RN-UC01-005:** CreatedAt preenchido automaticamente com timestamp UTC atual
- **RN-UC01-006:** SLA DEVE ser configurado para cada prioridade (RN-RF060-002)

### Critérios de Aceite
- **CA-UC01-001:** Todos os campos obrigatórios DEVEM ser validados antes de persistir
- **CA-UC01-002:** Categoria ITIL DEVE ser validada contra enum (Incidente, Requisição, Mudança, Problema)
- **CA-UC01-003:** EmpresaId DEVE ser preenchido automaticamente
- **CA-UC01-004:** CreatedBy e CreatedAt DEVEM ser preenchidos automaticamente
- **CA-UC01-005:** Sistema DEVE retornar erro claro se validação falhar
- **CA-UC01-006:** Auditoria DEVE ser registrada APÓS sucesso da criação

---

## UC02 — Visualizar Tipo de Chamado

### Objetivo
Permitir visualização detalhada de um tipo de chamado com configurações de SLA, formulários, templates e métricas ITIL.

### Pré-condições
- Usuário autenticado
- Permissão `GES.TIPOS_CHAMADO.VIEW`

### Pós-condições
- Dados do tipo de chamado exibidos corretamente
- Métricas ITIL exibidas (MTTR, MTBF, FCR)

### Fluxo Principal
- **FP-UC02-001:** Usuário seleciona tipo de chamado na listagem
- **FP-UC02-002:** Sistema valida permissão GES.TIPOS_CHAMADO.VIEW
- **FP-UC02-003:** Sistema valida que registro pertence ao tenant do usuário (EmpresaId)
- **FP-UC02-004:** Sistema carrega dados do tipo e configurações associadas
- **FP-UC02-005:** Sistema exibe dados estruturados em seções:
  - Informações Básicas (Código, Nome, Categoria ITIL, Status)
  - Configuração de SLA por Prioridade
  - Formulários Dinâmicos
  - Templates de Resolução
  - Regras de Escalonamento
  - Métricas ITIL (MTTR, MTBF, FCR)
  - Histórico de Chamados (últimos 30 dias)

### Fluxos Alternativos
- **FA-UC02-001:** Visualizar histórico completo de chamados do tipo
- **FA-UC02-002:** Exportar métricas ITIL em PDF

### Fluxos de Exceção
- **FE-UC02-001:** Registro inexistente → HTTP 404
- **FE-UC02-002:** Registro de outro tenant → HTTP 404
- **FE-UC02-003:** Registro soft-deleted → HTTP 404

### Regras de Negócio
- **RN-UC02-001:** Isolamento por tenant (EmpresaId) obrigatório
- **RN-UC02-002:** Informações de auditoria DEVEM ser visíveis
- **RN-UC02-003:** Métricas ITIL calculadas automaticamente (RN-RF060-011)
- **RN-UC02-004:** Integração com CMDB exibida (RN-RF060-012)

### Critérios de Aceite
- **CA-UC02-001:** Usuário SÓ pode visualizar tipos do próprio tenant
- **CA-UC02-002:** Informações de auditoria DEVEM ser exibidas
- **CA-UC02-003:** Tentativa de acessar registro de outro tenant DEVE retornar HTTP 404
- **CA-UC02-004:** Métricas ITIL (MTTR, MTBF, FCR) DEVEM ser calculadas e exibidas
- **CA-UC02-005:** Templates de resolução DEVEM exibir taxa de sucesso

---

## UC03 — Editar Tipo de Chamado

### Objetivo
Permitir alteração controlada de configurações do tipo de chamado (nome, SLA, formulários, templates).

### Pré-condições
- Usuário autenticado
- Permissão `GES.TIPOS_CHAMADO.EDIT`
- Tipo pertence ao tenant do usuário (EmpresaId)

### Pós-condições
- Registro atualizado no banco de dados
- Auditoria registrada
- Se houver mudança de SLA, recalcular deadlines de chamados abertos

### Fluxo Principal
- **FP-UC03-001:** Usuário clica em "Editar" no tipo de chamado
- **FP-UC03-002:** Sistema valida permissão GES.TIPOS_CHAMADO.EDIT
- **FP-UC03-003:** Sistema valida que registro pertence ao tenant (EmpresaId)
- **FP-UC03-004:** Sistema carrega dados atuais do tipo
- **FP-UC03-005:** Usuário altera dados (nome, categoria ITIL, SLA, formulários, templates)
- **FP-UC03-006:** Sistema valida alterações conforme RN-RF060-001 a RN-RF060-015
- **FP-UC03-007:** Sistema persiste alterações
- **FP-UC03-008:** Sistema atualiza auditoria
- **FP-UC03-009:** Se mudança de SLA → Sistema recalcula deadlines de chamados abertos
- **FP-UC03-010:** Sistema confirma sucesso

### Fluxos Alternativos
- **FA-UC03-001:** Cancelar edição

### Fluxos de Exceção
- **FE-UC03-001:** Campo obrigatório ausente → HTTP 400
- **FE-UC03-002:** Código duplicado no mesmo tenant → HTTP 409 Conflict
- **FE-UC03-003:** Categoria ITIL inválida → HTTP 400 (RN-RF060-001)
- **FE-UC03-004:** Tipo "Mudança" sem aprovação CAB configurada → HTTP 400 (RN-RF060-007)
- **FE-UC03-005:** Registro de outro tenant → HTTP 404

### Regras de Negócio
- **RN-UC03-001:** LastModifiedBy preenchido automaticamente
- **RN-UC03-002:** LastModifiedAt preenchido automaticamente
- **RN-UC03-003:** Alteração de SLA recalcula deadlines de chamados abertos
- **RN-UC03-004:** Tipos "Mudança" DEVEM ter aprovação CAB configurada (RN-RF060-007)
- **RN-UC03-005:** Alteração de categoria ITIL requer justificativa

### Critérios de Aceite
- **CA-UC03-001:** LastModifiedBy e LastModifiedAt DEVEM ser preenchidos automaticamente
- **CA-UC03-002:** Mudança de SLA DEVE recalcular deadlines de chamados abertos
- **CA-UC03-003:** Tipos "Mudança" DEVEM ter aprovação CAB obrigatória
- **CA-UC03-004:** Auditoria DEVE ser registrada APÓS sucesso da atualização

---

## UC04 — Inativar Tipo de Chamado

### Objetivo
Permitir inativação (soft delete) de um tipo de chamado que não está mais em uso.

### Pré-condições
- Usuário autenticado
- Permissão `GES.TIPOS_CHAMADO.DELETE`
- Tipo pertence ao tenant do usuário (EmpresaId)
- Tipo NÃO possui chamados abertos

### Pós-condições
- Registro marcado como excluído (soft delete)
- Auditoria registrada
- Chamados futuros não podem mais usar este tipo

### Fluxo Principal
- **FP-UC04-001:** Usuário clica em "Inativar" no tipo de chamado
- **FP-UC04-002:** Sistema exibe confirmação: "Deseja realmente inativar este tipo de chamado?"
- **FP-UC04-003:** Usuário confirma ação
- **FP-UC04-004:** Sistema valida permissão GES.TIPOS_CHAMADO.DELETE
- **FP-UC04-005:** Sistema valida que registro pertence ao tenant (EmpresaId)
- **FP-UC04-006:** Sistema valida que NÃO há chamados abertos deste tipo
- **FP-UC04-007:** Sistema marca registro como excluído (soft delete)
- **FP-UC04-008:** Sistema registra auditoria
- **FP-UC04-009:** Sistema confirma sucesso

### Fluxos Alternativos
- **FA-UC04-001:** Cancelar inativação

### Fluxos de Exceção
- **FE-UC04-001:** Tipo possui chamados abertos → HTTP 409 "Não é possível inativar tipo com chamados abertos"
- **FE-UC04-002:** Registro de outro tenant → HTTP 404
- **FE-UC04-003:** Registro já inativado → HTTP 404

### Regras de Negócio
- **RN-UC04-001:** Soft delete obrigatório (nunca DELETE físico)
- **RN-UC04-002:** DeletedBy preenchido automaticamente
- **RN-UC04-003:** DeletedAt preenchido automaticamente
- **RN-UC04-004:** Inativação só permitida se não houver chamados abertos
- **RN-UC04-005:** Chamados históricos (fechados) permanecem vinculados ao tipo inativo

### Critérios de Aceite
- **CA-UC04-001:** Sistema DEVE usar soft delete, NUNCA DELETE físico
- **CA-UC04-002:** DeletedBy e DeletedAt DEVEM ser preenchidos automaticamente
- **CA-UC04-003:** Tentativa de inativar tipo com chamados abertos DEVE retornar HTTP 409
- **CA-UC04-004:** Auditoria DEVE ser registrada APÓS sucesso da inativação
- **CA-UC04-005:** Registros inativos NÃO devem aparecer nas listagens padrão (UC00)

---

## 6. MATRIZ DE RASTREABILIDADE

### Cobertura RN → UC

| Regra | UC00 | UC01 | UC02 | UC03 | UC04 |
|-------|------|------|------|------|------|
| RN-RF060-001 | | ✅ | ✅ | ✅ | |
| RN-RF060-002 | | ✅ | ✅ | ✅ | |
| RN-RF060-003 | | ✅ | ✅ | ✅ | |
| RN-RF060-004 | | | ✅ | ✅ | |
| RN-RF060-005 | | | ✅ | ✅ | |
| RN-RF060-006 | | ✅ | ✅ | | |
| RN-RF060-007 | | ✅ | ✅ | ✅ | |
| RN-RF060-008 | | | ✅ | | |
| RN-RF060-009 | | ✅ | ✅ | ✅ | |
| RN-RF060-010 | | ✅ | ✅ | ✅ | |
| RN-RF060-011 | | | ✅ | | |
| RN-RF060-012 | | | ✅ | | |
| RN-RF060-013 | | ✅ | ✅ | ✅ | |
| RN-RF060-014 | | | ✅ | | |
| RN-RF060-015 | ✅ | | ✅ | | |

### Cobertura de Permissões

| Permissão | UC00 | UC01 | UC02 | UC03 | UC04 |
|-----------|------|------|------|------|------|
| GES.TIPOS_CHAMADO.VIEW | ✅ | | ✅ | | |
| GES.TIPOS_CHAMADO.CREATE | | ✅ | | | |
| GES.TIPOS_CHAMADO.EDIT | | | | ✅ | |
| GES.TIPOS_CHAMADO.DELETE | | | | | ✅ |

---

## 7. INTEGRAÇÕES OBRIGATÓRIAS

- **Autenticação:** JWT Bearer Token
- **Multi-Tenancy:** EmpresaId em todas as tabelas
- **Auditoria:** CreatedBy, CreatedAt, LastModifiedBy, LastModifiedAt, DeletedBy, DeletedAt
- **Internacionalização:** Chaves i18n com prefixo `tipos_chamado.*` (pt-BR, en-US, es-ES)
- **Central de Funcionalidades:** Feature `GES.TIPOS_CHAMADO` registrada
- **ITIL v4:** Classificação obrigatória (Incidente, Requisição, Mudança, Problema)
- **SLA Engine:** Cálculo automático de deadlines
- **Knowledge Base:** Templates de resolução
- **CMDB:** Integração com Configuration Items
- **Hangfire:** Jobs de escalonamento automático

---

## 8. HISTÓRICO DE VERSÕES

| Versão | Data | Descrição | Autor |
|--------|------|-----------|-------|
| 2.0 | 2025-12-31 | Migração para template v2.0 com 5 UCs canônicos. Cobertura 100% do RF060. | Agência ALC - alc.dev.br |
| 1.0 | 2025-12-18 | Versão inicial com 7 UCs resumidos | - |
