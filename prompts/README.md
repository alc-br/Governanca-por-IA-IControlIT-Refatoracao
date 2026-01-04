# Prompts - Governança IControlIT

Este diretório contém todos os prompts organizados por **fluxo de trabalho**.

## Estrutura de Pastas

| Pasta | Quando Usar | Contratos Ativados |
|-------|-------------|-------------------|
| **novo/** | Backend não existe, RF novo | DOCUMENTACAO-ESSENCIAL, EXECUCAO-BACKEND, TESTER-BACKEND, EXECUCAO-FRONTEND, EXECUCAO-TESTES |
| **adequacao/** | Backend legado → modernizado | REGULARIZACAO-BACKEND, TESTER-BACKEND, EXECUCAO-FRONTEND, EXECUCAO-TESTES |
| **manutencao/** | Correção, hotfix, debug | DEBUG-CONTROLADO, MANUTENCAO-CURTO, MANUTENCAO-BACKEND |
| **deploy/** | Deploy HOM/PRD | DEPLOY-AZURE, DEPLOY-HOM-SEM-VALIDACAO |
| **auditoria/** | Verificar conformidade | AUDITORIA-CONFORMIDADE |
| **devops/** | Sincronização Azure DevOps | DEVOPS-GOVERNANCA |

## Fluxo: NOVO RF (Backend não existe)

Use quando estiver criando um RF completamente novo.

### Ordem de Execução

1. [novo/01-documentacao-essencial.md](novo/01-documentacao-essencial.md) - Criar RF, UC, MD, WF, user-stories.yaml
2. [novo/02-backend.md](novo/02-backend.md) - Implementar backend (.NET 10 + CQRS)
3. [novo/03-validar-contrato.md](novo/03-validar-contrato.md) - Validar backend (testes de violação)
4. [novo/04-frontend.md](novo/04-frontend.md) - Implementar frontend (Angular 19)
5. [novo/05-testes.md](novo/05-testes.md) - Executar testes (Backend, E2E, Segurança)

## Fluxo: ADEQUAÇÃO (Backend legado → modernizado)

Use quando estiver adaptando backend legado aos padrões atuais.

### Ordem de Execução

1. [adequacao/01-regularizar-backend.md](adequacao/01-regularizar-backend.md) - Auditar e adequar backend legado
2. [adequacao/02-validar-contrato.md](adequacao/02-validar-contrato.md) - Validar backend adequado
3. [adequacao/03-frontend.md](adequacao/03-frontend.md) - Ajustar/criar frontend
4. [adequacao/04-testes.md](adequacao/04-testes.md) - Executar testes

## Fluxo: MANUTENÇÃO (Correção, hotfix, debug)

Use para correções, bugs e manutenções.

### Ordem de Execução

1. [manutencao/01-debug.md](manutencao/01-debug.md) - Investigar erro (modo READ-ONLY)
2. [manutencao/02-manutencao-curta.md](manutencao/02-manutencao-curta.md) - Correção rápida
3. [manutencao/03-manutencao-backend.md](manutencao/03-manutencao-backend.md) - Manutenção técnica

## Fluxo: DEPLOY (HOM/PRD)

Use para deploy em ambientes.

### Ordem de Execução

1. [deploy/01-deploy-hom.md](deploy/01-deploy-hom.md) - Deploy HOM com validação
2. [deploy/02-deploy-hom-sem-validacao.md](deploy/02-deploy-hom-sem-validacao.md) - Deploy HOM sem validação (EXCEPCIONAL)
3. [deploy/03-deploy-prd.md](deploy/03-deploy-prd.md) - Deploy PRD

## Fluxo: AUDITORIA (Conformidade)

Use para auditar conformidade entre especificação e implementação.

### Ordem de Execução

1. [auditoria/01-auditoria-backend.md](auditoria/01-auditoria-backend.md) - Auditar backend vs RF/UC/MD
2. [auditoria/02-auditoria-frontend.md](auditoria/02-auditoria-frontend.md) - Auditar frontend vs RF/UC/WF
3. [auditoria/03-auditoria-completa.md](auditoria/03-auditoria-completa.md) - Auditar backend + frontend

## Fluxo: DEVOPS (Sincronização)

Use para sincronizar com Azure DevOps.

### Ordem de Execução

1. [devops/01-sync-rf.md](devops/01-sync-rf.md) - Sincronizar 1 RF
2. [devops/02-sync-all-rfs.md](devops/02-sync-all-rfs.md) - Sincronizar todos RFs
3. [devops/03-sync-user-stories.md](devops/03-sync-user-stories.md) - Sincronizar User Stories

## Fluxo: ADITIVO (Evolução Incremental de RF)

Use para adicionar novas funcionalidades a um RF existente de forma incremental e rastreável.

### Ordem de Execução

1. [documentacao/execucao/aditivo.md](documentacao/execucao/aditivo.md) - Adicionar funcionalidade aos documentos (RF → UC → WF → MD → MT → TC)
2. [documentacao/validacao/aditivo.md](documentacao/validacao/aditivo.md) - Validar aditivo de documentação (15 validações)
3. Backend: Implementar delta no backend (Commands, Queries, Handlers, Endpoints)
4. Backend: Validar implementação backend (10 validações)
5. Frontend: Implementar delta no frontend (Services, Components, Routes, Forms, i18n)
6. Frontend: Validar implementação frontend (10 validações)

**Características do Fluxo ADITIVO:**
- ✅ Cria backups `_old` de todos os documentos (10 arquivos)
- ✅ Propaga mudanças em cascata (RF → UC → WF → MD → MT → TC)
- ✅ Delta rastreável (relatórios de mudanças)
- ✅ Validação rigorosa (100% ou REPROVADO)
- ✅ Versões `_old` são sobrescritas a cada novo aditivo

---

## Matriz de Rastreabilidade

| Prompt | Contrato | Checklist | Agente |
|--------|----------|-----------|--------|
| documentacao/execucao/rf-criacao.md | docs/contracts/documentacao/execucao/rf-criacao.md | docs/checklists/documentacao/geracao/rf.yaml | architect |
| documentacao/execucao/uc-criacao.md | docs/contracts/documentacao/execucao/uc-criacao.md | docs/checklists/documentacao/geracao/uc.yaml | architect |
| documentacao/execucao/wf-criacao.md | docs/contracts/documentacao/execucao/wf-criacao.md | docs/checklists/documentacao/geracao/wf.yaml | architect |
| documentacao/execucao/md-criacao.md | docs/contracts/documentacao/execucao/md-criacao.md | docs/checklists/documentacao/geracao/md.yaml | architect |
| documentacao/execucao/mt-tc-criacao.md | docs/contracts/documentacao/execucao/mt-tc-criacao.md | - | architect |
| **documentacao/execucao/aditivo.md** | **docs/contracts/documentacao/execucao/aditivo.md** | **docs/checklists/documentacao/geracao/aditivo.yaml** | **architect** |
| documentacao/validacao/rf.md | docs/contracts/documentacao/validacao/rf.md | - | validator |
| documentacao/validacao/uc.md | docs/contracts/documentacao/validacao/uc.md | - | validator |
| documentacao/validacao/wf-md.md | docs/contracts/documentacao/validacao/wf-md.md | - | validator |
| **documentacao/validacao/aditivo.md** | **docs/contracts/documentacao/validacao/aditivo.md** | - | **validator** |
| **desenvolvimento/execucao/backend-aditivo.md** | **docs/contracts/desenvolvimento/execucao/backend-aditivo.md** | - | **developer** |
| **desenvolvimento/execucao/frontend-aditivo.md** | **docs/contracts/desenvolvimento/execucao/frontend-aditivo.md** | - | **developer** |
| **desenvolvimento/validacao/backend-aditivo.md** | **docs/contracts/desenvolvimento/validacao/backend-aditivo.md** | - | **validator** |
| **desenvolvimento/validacao/frontend-aditivo.md** | **docs/contracts/desenvolvimento/validacao/frontend-aditivo.md** | - | **validator** |
| novo/01-documentacao-essencial.md | CONTRATO-DOCUMENTACAO-ESSENCIAL | checklist-documentacao-essencial.yaml | architect |
| novo/02-backend.md | CONTRATO-EXECUCAO-BACKEND | checklist-backend.yaml | developer |
| novo/03-validar-contrato.md | CONTRATO-EXECUCAO-TESTER-BACKEND | checklist-tester-backend.yaml | tester |
| novo/04-frontend.md | CONTRATO-EXECUCAO-FRONTEND | checklist-frontend.yaml | developer |
| novo/05-testes.md | CONTRATO-EXECUCAO-TESTES | checklist-testes.yaml | tester |
| adequacao/01-regularizar-backend.md | CONTRATO-DE-REGULARIZACAO-DE-BACKEND | checklist-regularizacao-backend.yaml | backend-regularizer |
| adequacao/02-validar-contrato.md | CONTRATO-EXECUCAO-TESTER-BACKEND | checklist-tester-backend.yaml | tester |
| adequacao/03-frontend.md | CONTRATO-EXECUCAO-FRONTEND | checklist-frontend.yaml | developer |
| adequacao/04-testes.md | CONTRATO-EXECUCAO-TESTES | checklist-testes.yaml | tester |
| manutencao/01-debug.md | CONTRATO-DEBUG-CONTROLADO | checklist-debug.yaml | debugger |
| manutencao/02-manutencao-curta.md | CONTRATO-MANUTENCAO-CURTO | checklist-manutencao-curto.yaml | developer |
| manutencao/03-manutencao-backend.md | CONTRATO-DE-MANUTENCAO-BACKEND | checklist-manutencao-backend.yaml | developer |
| deploy/01-deploy-hom.md | CONTRATO-DEPLOY-AZURE | checklist-deploy-prd.yaml | - |
| deploy/02-deploy-hom-sem-validacao.md | CONTRATO-DEPLOY-HOM-SEM-VALIDACAO | checklist-deploy-hom-sem-validacao.yaml | - |
| deploy/03-deploy-prd.md | CONTRATO-DEPLOY-AZURE | checklist-deploy-prd.yaml | - |
| auditoria/01-auditoria-backend.md | CONTRATO-AUDITORIA-CONFORMIDADE | checklist-auditoria-conformidade.yaml | auditor |
| auditoria/02-auditoria-frontend.md | CONTRATO-AUDITORIA-CONFORMIDADE | checklist-auditoria-conformidade.yaml | auditor |
| auditoria/03-auditoria-completa.md | CONTRATO-AUDITORIA-CONFORMIDADE | checklist-auditoria-conformidade.yaml | auditor |
| devops/01-sync-rf.md | CONTRATO-DEVOPS-GOVERNANCA | checklist-devops.yaml | - |
| devops/02-sync-all-rfs.md | CONTRATO-DEVOPS-GOVERNANCA | checklist-devops.yaml | - |
| devops/03-sync-user-stories.md | CONTRATO-DEVOPS-GOVERNANCA | checklist-devops.yaml | - |

---

## Como Usar os Prompts

1. **Identifique o fluxo:** Novo RF vs Adequação vs Manutenção vs Deploy vs Auditoria vs DevOps
2. **Abra a pasta correspondente**
3. **Execute os prompts na ordem numérica** (01 → 02 → 03...)
4. **Cada prompt ativa 1 contrato específico**
5. **Siga o checklist vinculado** para garantir conformidade
6. **Atualize STATUS.yaml** ao concluir cada etapa
7. **Sincronize com DevOps** usando prompts da pasta `devops/`

---

## Princípios dos Prompts

- **Prompts são mínimos:** Apenas o essencial (5-10 linhas)
- **Contratos têm toda a lógica:** Prompts ativam contratos
- **1 Prompt = 1 Contrato = 1 Checklist = 1 Agente** (quando aplicável)
- **Ordem importa:** Siga a sequência numérica
- **Fluxos não se misturam:** Não use prompts de fluxos diferentes simultaneamente

---

## Versionamento

- **Criado em:** 2025-12-28
- **Última atualização:** 2026-01-03
- **Versão:** 1.2.0 (Adicionado sistema completo ADITIVO - evolução incremental de RFs)

---

**Para mais detalhes sobre contratos, consulte:** `docs/contracts/README.md`

**Para mais detalhes sobre checklists, consulte:** `docs/checklists/README.md`

**Para mais detalhes sobre agentes, consulte:** `.claude/agents/README.md`
