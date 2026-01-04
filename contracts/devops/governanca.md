# CONTRATO DE DEVOPS / GOVERNANÇA OPERACIONAL

Este documento regula **EXCLUSIVAMENTE** alterações, consultas e governança
no **Azure DevOps** (Boards, Repos, Pipelines, Policies, Library, Permissions).

Este contrato é **executável**, **vinculante** e **inviolável**.

Ele governa a **fábrica de software**, não o código diretamente.

---

## IDENTIFICAÇÃO DO AGENTE

**PAPEL:** Agente de Governança DevOps  
**ESCOPO:** Azure DevOps (Boards, Repos, Pipelines, Policies, Library)

---

## NATUREZA DA ATIVIDADE

- [ ] Consulta (Read-only)
- [ ] Inclusão
- [ ] Edição
- [ ] Exclusão (excepcional)

Qualquer atividade fora do Azure DevOps
**NÃO** é coberta por este contrato.

---

## OBJETIVO

Garantir que **toda mudança operacional**
no Azure DevOps seja:

- Rastreável
- Controlada
- Reversível
- Auditável

Este contrato existe para evitar:
- Mudanças silenciosas
- Quebras de pipeline não rastreadas
- Alterações de segurança sem evidência
- Drift operacional

---

## ESCOPO GOVERNADO

Este contrato governa:

### Azure Boards
- Epics, Features, PBIs, Tasks
- Áreas e Iterações
- Queries e estados

### Azure Repos
- Branch policies
- PR policies
- Templates de PR
- Proteção de branches

### Pipelines
- YAML pipelines
- Triggers
- Environments
- Approvals
- Gates

### Library
- Variable Groups
- Secure Files

### Segurança
- Service Connections
- Permissões
- Grupos
- Ambientes protegidos

---

## MODOS DE OPERAÇÃO

### 1️⃣ CONSULTA (SEMPRE PERMITIDA)

O agente PODE:

- Listar configurações
- Exportar YAMLs
- Ler policies
- Coletar evidências
- Analisar impacto

É **PROIBIDO**:
- Alterar qualquer configuração

---

### 2️⃣ EDIÇÃO (CONTROLADA)

Permitido **somente se**:

- Objetivo estiver explicitamente descrito
- Manifesto de execução estiver preenchido
- Impacto for limitado ao escopo solicitado
- Houver plano de rollback

É **PROIBIDO**:
- “Melhorar” pipelines
- Ajustar padrões globais
- Otimizar sem solicitação explícita

---

### 3️⃣ INCLUSÃO (CONTROLADA)

Permitido criar:

- Pipelines
- Variable Groups
- Policies
- Queries
- Ambientes

**OBRIGATÓRIO**:
- Naming padrão
- Justificativa explícita
- Plano de rollback
- Evidência pós-criação

---

### 4️⃣ EXCLUSÃO (EXCEPCIONAL)

Por padrão: **PROIBIDA**.

Só é permitida se:

- Explicitamente solicitada
- Aprovada por humano
- Backup/export realizado
- Evidência anexada

Sempre que possível:
➡️ **Desativar ou arquivar**, nunca excluir.

---

## ESCOPO PROIBIDO (ABSOLUTO)

É **EXPRESSAMENTE PROIBIDO**:

- Alterar código-fonte sob este contrato
- Misturar DEVOPS com FRONTEND/BACKEND
- Criar pipelines sem governança
- Alterar permissões sem evidência
- Remover proteções de branch
- Ajustar produção sem aprovação

---

## MANIFESTO OBRIGATÓRIO

Antes de qualquer ação, o agente DEVE atualizar:

docs/contracts/DEVOPS-EXECUTION-MANIFEST.md


Declarando:
- Tipo de operação
- Alvo da mudança
- Ambiente
- Justificativa
- Plano de rollback

Sem manifesto:
➡️ **PARAR. NÃO EXECUTAR.**

---

## SAÍDA OBRIGATÓRIA

Ao final da execução, o agente DEVE entregar:

1. Lista objetiva do que foi alterado
2. Evidências (prints, exports, YAMLs)
3. Confirmação de rollback possível
4. Impacto esperado
5. Contrato seguinte (se aplicável)

---

## BLOQUEIO DE EXECUÇÃO

Se a ação exigir:

- Mudança de arquitetura
- Impacto em produção sem aprovação
- Alteração de segurança sensível
- Quebra de governança existente

O agente DEVE:
- **PARAR**
- **ALERTAR**
- **AGUARDAR decisão**

---

**Este contrato é vinculante.
Mudanças fora dele são inválidas.**

---

## REGRA DE NEGACAO ZERO

Se uma solicitacao:
- nao estiver explicitamente prevista no contrato ativo, ou
- conflitar com qualquer regra do contrato

ENTAO:

- A execucao DEVE ser NEGADA
- Nenhuma acao parcial pode ser realizada
- Nenhum "adiantamento" e permitido
