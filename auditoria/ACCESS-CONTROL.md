# ACCESS CONTROL – CONTROLE DE ACESSO

**Versão:** 1.0
**Data de criação:** 2025-12-26
**Propósito:** Documentação de controle de acesso e segregação de funções para auditoria ISO / Compliance

---

## VISÃO GERAL

Este documento define o modelo de controle de acesso do sistema de governança por contratos, demonstrando segregação de funções (Segregation of Duties - SoD) e princípio do menor privilégio.

---

## PRINCÍPIO FUNDAMENTAL

**Nenhum agente pode aprovar seu próprio trabalho.**

Segregação de Funções:
- Developer NÃO pode validar backend
- Tester-Backend NÃO pode desenvolver
- QA NÃO pode alterar código
- DevOps Agent NÃO pode pular validações

---

## MODELO DE CONTROLE DE ACESSO

### Tipo de Controle

**RBAC (Role-Based Access Control)**

- Cada agente tem um papel (role)
- Cada papel tem permissões específicas
- Permissões são baseadas em contratos
- Nenhum papel pode executar fora de seu contrato

---

## PAPÉIS (ROLES)

### 1. DEVELOPER AGENT

**Responsabilidades:**
- Executar CONTRATO-EXECUCAO-BACKEND
- Executar CONTRATO-EXECUCAO-FRONTEND
- Implementar código
- Executar testes unitários

**Permissões:**
- ✅ Ler documentação (RF, UC, MD, WF)
- ✅ Criar código backend (.NET)
- ✅ Criar código frontend (Angular)
- ✅ Executar testes unitários
- ✅ Criar seeds de dados
- ✅ Configurar permissões
- ✅ Criar commits
- ✅ Atualizar STATUS.yaml (desenvolvimento)
- ✅ Registrar execução no EXECUTION-MANIFEST

**Proibições:**
- ❌ Aprovar próprio backend
- ❌ Executar CONTRATO-TESTER-BACKEND
- ❌ Executar deploy
- ❌ Alterar contrato backend
- ❌ Pular validações
- ❌ Marcar testes como APROVADO
- ❌ Executar em produção

**Acesso a Ambientes:**
- ✅ DEV (desenvolvimento local)
- ❌ HOM (homologação)
- ❌ PRD (produção)

---

### 2. TESTER-BACKEND AGENT

**Responsabilidades:**
- Executar CONTRATO-EXECUCAO-TESTER-BACKEND
- Validar que backend respeita contrato
- Testar violações de contrato
- Decidir: APROVADO / REPROVADO

**Permissões:**
- ✅ Ler documentação (RF, UC, MD)
- ✅ Ler código backend
- ✅ Criar testes de contrato
- ✅ Criar testes de violação
- ✅ Executar testes contra backend
- ✅ Gerar matriz de violação
- ✅ Registrar decisão no EXECUTION-MANIFEST
- ✅ Bloquear merge se REPROVADO

**Proibições:**
- ❌ Alterar código backend
- ❌ Corrigir bugs
- ❌ Alterar contrato backend
- ❌ Executar deploy
- ❌ Pular validações
- ❌ Aprovar sem testar violações

**Acesso a Ambientes:**
- ✅ DEV (para testes)
- ❌ HOM
- ❌ PRD

**Autoridade:**
- ✅ Bloquear merge para `dev` se backend violar contrato
- ✅ Exigir correções antes de aprovação

---

### 3. QA AGENT / TESTER

**Responsabilidades:**
- Executar CONTRATO-EXECUCAO-TESTES
- Executar testes completos (backend, frontend, E2E, segurança)
- Gerar evidências
- Decidir: APROVADO / REPROVADO

**Permissões:**
- ✅ Ler documentação (RF, UC, MD, WF)
- ✅ Ler código (backend e frontend)
- ✅ Executar testes unitários
- ✅ Executar testes de integração
- ✅ Executar testes E2E (Playwright)
- ✅ Executar testes de segurança
- ✅ Capturar screenshots
- ✅ Gerar relatórios
- ✅ Registrar decisão no EXECUTION-MANIFEST
- ✅ Atualizar STATUS.yaml (testes)

**Proibições:**
- ❌ Alterar código (backend ou frontend)
- ❌ Corrigir bugs
- ❌ Pular testes que falharam
- ❌ Aprovar com taxa < 100%
- ❌ Modificar testes para fazer passar
- ❌ Executar deploy

**Acesso a Ambientes:**
- ✅ DEV (para testes E2E)
- ❌ HOM
- ❌ PRD

---

### 4. DEVOPS AGENT

**Responsabilidades:**
- Executar CONTRATO-TRANSICAO-TESTES-PARA-DEPLOY
- Executar CONTRATO-EXECUCAO-DEPLOY
- Executar CONTRATO-ROLLBACK (automático)
- Atualizar STATUS.yaml
- Registrar no EXECUTION-MANIFEST

**Permissões:**
- ✅ Ler EXECUTION-MANIFEST
- ✅ Validar pré-requisitos de transição
- ✅ Atualizar STATUS.yaml (governanca, devops)
- ✅ Executar build
- ✅ Executar deploy (HOM e PRD)
- ✅ Executar smoke tests
- ✅ Executar rollback automático
- ✅ Registrar execuções no EXECUTION-MANIFEST

**Proibições:**
- ❌ Alterar código
- ❌ Corrigir bugs
- ❌ Executar deploy sem aprovação no manifesto
- ❌ Pular smoke tests
- ❌ Executar hotfix fora de contrato
- ❌ Aprovar testes

**Acesso a Ambientes:**
- ✅ DEV (para build)
- ✅ HOM (para deploy)
- ✅ PRD (para deploy)

**Autoridade:**
- ✅ Executar rollback automático (se smoke test falha)
- ✅ Bloquear deploy se pré-requisitos não atendidos

---

### 5. RELEASE MANAGER (Humano)

**Responsabilidades:**
- Autorizar deploy em PRD
- Autorizar rollback manual
- Validar janela de deploy
- Comunicar mudanças

**Permissões:**
- ✅ Ler EXECUTION-MANIFEST
- ✅ Ler STATUS.yaml
- ✅ Autorizar deploy em PRD
- ✅ Autorizar rollback manual
- ✅ Definir janela de deploy
- ✅ Comunicar stakeholders

**Proibições:**
- ❌ Executar deploy manual
- ❌ Alterar código em produção
- ❌ Pular validações
- ❌ Executar hotfix sem contrato

**Acesso a Ambientes:**
- ✅ Read-only em todos os ambientes
- ❌ Write em nenhum ambiente (deve usar pipeline)

**Autoridade:**
- ✅ Aprovar deploy em PRD
- ✅ Autorizar rollback manual
- ✅ Bloquear deploy se risco alto

---

### 6. ARCHITECT / TECH LEAD (Humano)

**Responsabilidades:**
- Revisar arquitetura
- Validar padrões
- Aprovar documentação (RF, UC, MD, WF)
- Decidir sobre mudanças arquiteturais

**Permissões:**
- ✅ Ler toda documentação
- ✅ Ler todo código
- ✅ Revisar arquitetura
- ✅ Aprovar/Rejeitar RF
- ✅ Definir padrões
- ✅ Atualizar ARCHITECTURE.md
- ✅ Atualizar CONVENTIONS.md

**Proibições:**
- ❌ Implementar código diretamente (deve delegar)
- ❌ Executar deploy
- ❌ Pular validações

**Acesso a Ambientes:**
- ✅ Read-only em todos os ambientes
- ❌ Write em nenhum ambiente

---

## MATRIZ DE AUTORIZAÇÃO

| Ação | Developer | Tester-Backend | QA | DevOps | Release Mgr | Architect |
|------|-----------|----------------|----|---------|--------------|-----------||
| Implementar código | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Validar backend | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Executar testes | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| Aprovar testes | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| Deploy HOM | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| Deploy PRD | ❌ | ❌ | ❌ | ✅ | ✅ (autoriza) | ❌ |
| Rollback | ❌ | ❌ | ❌ | ✅ | ✅ (autoriza) | ❌ |
| Aprovar RF | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Atualizar contrato | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |

---

## SEGREGAÇÃO DE FUNÇÕES (SoD)

### Regra 1: Desenvolvimento vs Validação

**Incompatível:**
- Developer NÃO pode ser Tester-Backend para o mesmo RF
- Developer NÃO pode ser QA para o mesmo RF

**Motivo:**
- Conflito de interesse
- Reduz eficácia de validação

---

### Regra 2: Teste vs Deploy

**Incompatível:**
- QA NÃO pode executar deploy
- QA NÃO pode autorizar deploy

**Motivo:**
- QA não tem responsabilidade sobre infraestrutura
- Deploy deve ser separado de validação

---

### Regra 3: Desenvolvimento vs Deploy

**Incompatível:**
- Developer NÃO pode executar deploy em PRD
- Developer NÃO pode autorizar deploy

**Motivo:**
- Developer não deve ter acesso direto a produção
- Deploy deve passar por validações independentes

---

### Regra 4: Autorização vs Execução

**Incompatível:**
- Release Manager NÃO pode executar deploy manualmente
- Release Manager AUTORIZA, DevOps Agent EXECUTA

**Motivo:**
- Segregação entre decisão e execução
- Evita bypass de processo

---

## CONTROLE DE ACESSO AO EXECUTION-MANIFEST

### Leitura

**Permitido:**
- ✅ Todos os agentes (read-only)
- ✅ Release Manager
- ✅ Architect

**Motivo:**
- Manifesto é fonte da verdade
- Transparência total

---

### Escrita

**Permitido:**
- ✅ Developer Agent (registrar execução backend/frontend)
- ✅ Tester-Backend Agent (registrar decisão)
- ✅ QA Agent (registrar testes)
- ✅ DevOps Agent (registrar transição/deploy/rollback)

**Proibido:**
- ❌ Alterar execuções passadas
- ❌ Remover registros
- ❌ Alterar decisões de outros agentes

**Auditoria:**
- Git history rastreia TODAS as alterações no manifesto

---

## CONTROLE DE ACESSO AO STATUS.yaml

### Leitura

**Permitido:**
- ✅ Todos os agentes

---

### Escrita

**Permitido (por seção):**

| Seção | Developer | Tester-Backend | QA | DevOps |
|-------|-----------|----------------|----|---------||
| desenvolvimento.backend | ✅ | ❌ | ❌ | ❌ |
| desenvolvimento.frontend | ✅ | ❌ | ❌ | ❌ |
| testes | ❌ | ❌ | ✅ | ❌ |
| governanca | ❌ | ❌ | ❌ | ✅ |
| devops | ❌ | ❌ | ❌ | ✅ |

**Proibido:**
- ❌ Alterar seções de outro agente
- ❌ Alterar campos não autorizados

---

## CONTROLE DE ACESSO AOS AMBIENTES

### DEV (Desenvolvimento Local)

**Acesso:**
- ✅ Developer Agent (read/write)
- ✅ Tester-Backend Agent (read/execute)
- ✅ QA Agent (read/execute)

**Controle:**
- Nenhum (ambiente local)

---

### HOM (Homologação)

**Acesso:**
- ✅ DevOps Agent (deploy)
- ✅ Product Owner (validação)
- ✅ QA (validação manual)

**Controle:**
- Deploy via pipeline (CONTRATO-EXECUCAO-DEPLOY)
- Credenciais Azure

---

### PRD (Produção)

**Acesso:**
- ✅ DevOps Agent (deploy via pipeline)
- ✅ Release Manager (read-only)

**Controle:**
- Deploy via pipeline (CONTRATO-EXECUCAO-DEPLOY)
- Aprovação de Release Manager obrigatória
- Credenciais Azure (produção)
- Acesso SSH/RDP BLOQUEADO

---

## AUDITORIA DE ACESSO

### Logs de Acesso

**Registrar:**
- Quem executou cada contrato
- Quando executou
- Qual ambiente
- Qual ação

**Local:**
- EXECUTION-MANIFEST (decisões)
- Git history (alterações de código)
- Azure logs (deploys)

---

### Revisão de Acesso

**Frequência:** Trimestral

**Validar:**
- Todos os agentes têm apenas permissões necessárias
- Nenhum agente tem permissões excessivas
- Segregação de funções está sendo respeitada
- Nenhuma conta inativa tem acesso

---

## CONFORMIDADE ISO

Este modelo de controle de acesso atende:

### ISO 27001
- **A.9.1.1** – Política de controle de acesso
- **A.9.2.1** – Registro e cancelamento de usuário
- **A.9.2.3** – Gestão de direitos de acesso privilegiados
- **A.9.4.1** – Restrição de acesso à informação

### SOC 2
- **CC6.1** – Segregação de funções
- **CC6.2** – Provisão e desprovisionamento de acesso
- **CC6.3** – Gestão de acesso privilegiado

---

## CONCLUSÃO

Este modelo de controle de acesso garante:

✅ **Segregação de funções** – Nenhum agente aprova próprio trabalho
✅ **Menor privilégio** – Cada agente tem apenas permissões necessárias
✅ **Rastreabilidade** – Toda ação é auditável
✅ **Bloqueio de bypass** – Nenhuma exceção manual é permitida
✅ **Conformidade** – Atende ISO 27001 e SOC 2

---

**FIM DO DOCUMENTO**
