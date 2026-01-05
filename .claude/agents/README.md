# Agentes Claude - Projeto IControlIT

Agentes especializados para execução de contratos de governança no projeto IControlIT.

## Quando Usar Cada Agente

| Agente | subagent_type | Quando Usar | Contrato Principal |
|--------|---------------|-------------|-------------------|
| **Architect** | `icontrolit-architect` | Criar RF, UC, MD, documentação técnica | CONTRATO-DOCUMENTACAO-ESSENCIAL |
| **Developer** | `full-stack-implementer` | Implementar backend + frontend | CONTRATO-EXECUCAO-BACKEND, CONTRATO-EXECUCAO-FRONTEND |
| **Tester** | `qa-tester` | Executar testes (Backend, E2E, Outros) | CONTRATO-EXECUCAO-TESTES, CONTRATO-EXECUCAO-TESTER-BACKEND |
| **Debugger** | `debug-investigator` | Investigar e corrigir bugs | CONTRATO-DEBUG-CONTROLADO |
| **Orchestrator** | `orchestrator` | Coordenar agentes, decisões estratégicas | CONTRATO-ORQUESTRACAO |
| **Backend Regularizer** | `backend-regularizer` | Adequar backend legado | CONTRATO-DE-REGULARIZACAO-DE-BACKEND |
| **Auditor** | `conformance-auditor` | Auditar conformidade RF ↔ Código | CONTRATO-AUDITORIA-CONFORMIDADE |

## Descrição Detalhada

### Architect (icontrolit-architect)

**Arquivo:** [architect.md](architect.md)

**Propósito:**
- Criar documentação completa de RFs (RF, UC, MD, WF, user-stories.yaml)
- Mapear sistema legado para documentação moderna
- Validar conformidade arquitetural

**Quando usar:**
- Criar novo RF do zero
- Documentar funcionalidade existente
- Analisar sistema legado antes de modernização

**Ferramentas permitidas:**
- Read, Glob, Grep (análise de código)
- Write (criar documentação)
- Bash (consultas read-only)

**Proibições:**
- NÃO implementar código
- NÃO executar testes
- NÃO fazer deploy

---

### Developer (full-stack-implementer)

**Arquivo:** [developer.md](developer.md)

**Propósito:**
- Implementar backend (.NET 10 + CQRS + Clean Architecture)
- Implementar frontend (Angular 19 + Standalone Components)
- Garantir integrações obrigatórias (i18n, auditoria, permissões)

**Quando usar:**
- Implementar RF completo (backend + frontend)
- Evoluir funcionalidade existente
- Corrigir bugs de implementação

**Ferramentas permitidas:**
- Read, Glob, Grep (análise de código)
- Write, Edit (criar/modificar código)
- Bash (build, testes, git)

**Proibições:**
- NÃO criar documentação (responsabilidade do Architect)
- NÃO executar testes de conformidade (responsabilidade do Tester)

---

### Tester (qa-tester)

**Arquivo:** [tester.md](tester.md)

**Propósito:**
- Executar testes automatizados (3 baterias: Backend, E2E, Outros)
- Validar contratos backend (Tester-Backend)
- Garantir 100% PASS antes de deploy

**Quando usar:**
- Após implementação de backend (validar contrato)
- Após implementação de frontend (testes E2E)
- Antes de deploy (validação completa)

**Ferramentas permitidas:**
- Read, Grep (análise de testes)
- Bash (executar testes)
- Write (criar relatórios de testes)

**Proibições:**
- NÃO corrigir código sob CONTRATO-EXECUCAO-TESTES (apenas reportar falhas)
- Pode corrigir sob CONTRATO-EXECUCAO-TESTER-BACKEND (criar testes de violação)

---

### Debugger (debug-investigator)

**Arquivo:** [debugger.md](debugger.md)

**Propósito:**
- Investigar erros e bugs (modo READ-ONLY)
- Identificar causa raiz
- Propor plano de correção (sem executar)

**Quando usar:**
- Erro 500 em produção
- Comportamento inesperado
- Performance degradada

**Ferramentas permitidas:**
- Read, Grep (análise de código)
- Bash (consultas read-only, logs)

**Proibições:**
- NÃO alterar código (apenas investigar)
- NÃO executar correções (propor plano apenas)
- NÃO criar commits

---

### Orchestrator (orquestrador)

**Arquivo:** [orchestrator.md](orchestrator.md)

**Propósito:**
- Coordenar agentes especializados
- Tomar decisões estratégicas
- Validar qualidade final
- Garantir conformidade com governança

**Quando usar:**
- Tarefa complexa que requer coordenação de múltiplos agentes
- Decisões arquiteturais críticas
- Validação de completude de RF

**Ferramentas permitidas:**
- Task (chamar outros agentes)
- Read (validar contexto)
- TodoWrite (gerenciar tarefas)

**Proibições:**
- NÃO implementar código diretamente (delegar para Developer)
- NÃO criar documentação diretamente (delegar para Architect)

---

### Backend Regularizer (backend-regularizer)

**Arquivo:** [backend-regularizer.md](backend-regularizer.md)

**Propósito:**
- Adaptar backend legado aos padrões modernos
- Preservar compatibilidade com frontend existente
- Preparar backend para CONTRATO-TESTER-BACKEND

**Quando usar:**
- Backend foi desenvolvido antes da governança
- Backend não está 100% aderente ao RF/UC/MD
- Frontend já implementado depende do backend

**Ferramentas permitidas:**
- Read, Grep (análise de backend legado)
- Write, Edit (correções mínimas)
- Bash (migrations, testes)

**Proibições:**
- NÃO criar novas funcionalidades
- NÃO alterar payloads públicos
- NÃO quebrar contratos com frontend
- NÃO refatorar arquitetura completa

---

### Auditor (conformance-auditor)

**Arquivo:** [auditor.md](auditor.md)

**Propósito:**
- Validar conformidade entre especificação (RF, UC, MD, WF) e implementação (código)
- Gerar relatório de gaps com classificação (CRÍTICO, IMPORTANTE, MENOR)
- Recomendar contratos para correção

**Quando usar:**
- Antes de marcar RF como concluído
- Após implementação de backend (auditar antes de frontend)
- Após implementação de frontend (auditar antes de testes E2E)
- Durante code review

**Ferramentas permitidas:**
- Read, Grep (análise de código)
- Write (gerar relatório em `D:\IC2\relatorios\AAAA-MM-DD-RFXXX-[BACKEND|FRONTEND|COMPLETO]-Gaps.md`)

**Proibições:**
- NÃO corrigir código (apenas reportar gaps)
- NÃO implementar funcionalidades faltantes
- NÃO executar testes

---

## Como Usar os Agentes

### Exemplo 1: Criar RF do Zero

```python
# 1. Criar documentação
Task(
    subagent_type="icontrolit-architect",
    prompt="Criar documentação completa do RF-028 conforme CONTRATO-DOCUMENTACAO-ESSENCIAL",
    description="Criar docs RF-028"
)

# 2. Implementar backend
Task(
    subagent_type="full-stack-implementer",
    prompt="Implementar backend do RF-028 conforme CONTRATO-EXECUCAO-BACKEND",
    description="Implementar backend RF-028"
)

# 3. Validar contrato backend
Task(
    subagent_type="qa-tester",
    prompt="Validar backend do RF-028 conforme CONTRATO-EXECUCAO-TESTER-BACKEND",
    description="Validar contrato RF-028"
)

# 4. Implementar frontend
Task(
    subagent_type="full-stack-implementer",
    prompt="Implementar frontend do RF-028 conforme CONTRATO-EXECUCAO-FRONTEND",
    description="Implementar frontend RF-028"
)

# 5. Executar testes completos
Task(
    subagent_type="qa-tester",
    prompt="Executar testes do RF-028 conforme CONTRATO-EXECUCAO-TESTES",
    description="Testar RF-028"
)
```

### Exemplo 2: Adequar Backend Legado

```python
# 1. Regularizar backend
Task(
    subagent_type="backend-regularizer",
    prompt="Regularizar backend do RF-015 conforme CONTRATO-DE-REGULARIZACAO-DE-BACKEND",
    description="Regularizar backend RF-015"
)

# 2. Validar contrato backend
Task(
    subagent_type="qa-tester",
    prompt="Validar backend do RF-015 conforme CONTRATO-EXECUCAO-TESTER-BACKEND",
    description="Validar contrato RF-015"
)
```

### Exemplo 3: Auditar Conformidade

```python
# 1. Auditar backend
Task(
    subagent_type="conformance-auditor",
    prompt="Auditar backend do RF-027 conforme CONTRATO-AUDITORIA-CONFORMIDADE",
    description="Auditar backend RF-027"
)

# 2. Auditar frontend
Task(
    subagent_type="conformance-auditor",
    prompt="Auditar frontend do RF-027 conforme CONTRATO-AUDITORIA-CONFORMIDADE",
    description="Auditar frontend RF-027"
)

# 3. Auditar completo
Task(
    subagent_type="conformance-auditor",
    prompt="Auditar RF-027 completo conforme CONTRATO-AUDITORIA-CONFORMIDADE",
    description="Auditar RF-027 completo"
)
```

### Exemplo 4: Investigar Bug

```python
# 1. Investigar erro
Task(
    subagent_type="debug-investigator",
    prompt="Investigar erro 500 ao criar departamento conforme CONTRATO-DEBUG-CONTROLADO",
    description="Investigar erro 500"
)

# 2. Após identificar causa, corrigir
Task(
    subagent_type="full-stack-implementer",
    prompt="Corrigir erro 500 ao criar departamento conforme CONTRATO-MANUTENCAO",
    description="Corrigir erro 500"
)
```

---

## Matriz de Rastreabilidade

| Agente | Prompt | Contrato | Checklist |
|--------|--------|----------|-----------|
| Architect | novo/01-documentacao-essencial.md | CONTRATO-DOCUMENTACAO-ESSENCIAL | checklist-documentacao-essencial.yaml |
| Developer | novo/02-backend.md | CONTRATO-EXECUCAO-BACKEND | checklist-backend.yaml |
| Tester | novo/03-validar-contrato.md | CONTRATO-EXECUCAO-TESTER-BACKEND | checklist-tester-backend.yaml |
| Developer | novo/04-frontend.md | CONTRATO-EXECUCAO-FRONTEND | checklist-frontend.yaml |
| Tester | novo/05-testes.md | CONTRATO-EXECUCAO-TESTES | checklist-testes.yaml |
| Backend Regularizer | adequacao/01-regularizar-backend.md | CONTRATO-DE-REGULARIZACAO-DE-BACKEND | checklist-regularizacao-backend.yaml |
| Debugger | manutencao/01-debug.md | CONTRATO-DEBUG-CONTROLADO | checklist-debug.yaml |
| Developer | manutencao/02-manutencao-curta.md | CONTRATO-MANUTENCAO-CURTO | checklist-manutencao-curto.yaml |
| Developer | manutencao/03-manutencao-backend.md | CONTRATO-DE-MANUTENCAO-BACKEND | checklist-manutencao-backend.yaml |
| Auditor | auditoria/01-auditoria-backend.md | CONTRATO-AUDITORIA-CONFORMIDADE | checklist-auditoria-conformidade.yaml |
| Auditor | auditoria/02-auditoria-frontend.md | CONTRATO-AUDITORIA-CONFORMIDADE | checklist-auditoria-conformidade.yaml |
| Auditor | auditoria/03-auditoria-completa.md | CONTRATO-AUDITORIA-CONFORMIDADE | checklist-auditoria-conformidade.yaml |

---

## Regras de Uso

### 1. Agentes NÃO se sobrepõem

- Cada agente tem responsabilidade bem definida
- NÃO use Developer para criar documentação (use Architect)
- NÃO use Tester para corrigir código (use Developer)
- NÃO use Debugger para implementar correções (apenas investigar)

### 2. Agentes seguem contratos

- Cada agente segue um contrato específico
- Contrato define zonas permitidas (leitura/escrita)
- Violação de contrato invalida a execução

### 3. Ordem de execução importa

```
Documentação (Architect)
↓
Backend (Developer)
↓
Validação Contrato (Tester)
↓
Frontend (Developer)
↓
Testes Completos (Tester)
↓
Auditoria Final (Auditor)
↓
Deploy
```

### 4. Orquestrador coordena

- Para tarefas complexas, use Orchestrator primeiro
- Orchestrator define ordem de execução
- Orchestrator delega para agentes especializados

---

## Versionamento

- **Criado em:** 2025-12-23
- **Última atualização:** 2025-12-28
- **Versão:** 2.0.0 (Reorganização completa + novos agentes)

---

**Para mais detalhes sobre contratos, consulte:** `D:\IC2_Governanca\contracts\README.md`

**Para mais detalhes sobre prompts, consulte:** `D:\IC2_Governanca\prompts\README.md`

**Para mais detalhes sobre checklists, consulte:** `D:\IC2_Governanca\checklists\README.md`
