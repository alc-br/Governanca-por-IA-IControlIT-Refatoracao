# Matriz de Rastreabilidade - Governança IControlIT

Rastreabilidade completa entre Contratos, Checklists, Prompts, Agentes e Scripts.

## Regra de Ouro

**1 Contrato = 1 Checklist = 1 Prompt = 1 Agente (quando aplicável)**

---

## Fluxo: NOVO RF (Backend não existe)

| Passo | Contrato | Checklist | Prompt | Agente | Script |
|-------|----------|-----------|--------|--------|--------|
| 1. Documentação | CONTRATO-DOCUMENTACAO-ESSENCIAL | checklist-documentacao-essencial.yaml | novo/01-documentacao-essencial.md | architect | - |
| 2. Backend | CONTRATO-EXECUCAO-BACKEND | checklist-backend.yaml | novo/02-backend.md | developer | - |
| 3. Validar Contrato | CONTRATO-EXECUCAO-TESTER-BACKEND | checklist-tester-backend.yaml | novo/03-validar-contrato.md | tester | - |
| 4. Frontend | CONTRATO-EXECUCAO-FRONTEND | checklist-frontend.yaml | novo/04-frontend.md | developer | - |
| 5. Testes | CONTRATO-EXECUCAO-TESTES | checklist-testes.yaml | novo/05-testes.md | tester | - |
| 6. Sync DevOps | CONTRATO-DEVOPS-GOVERNANCA | checklist-devops.yaml | devops/01-sync-rf.md | - | sync-rf.py |

---

## Fluxo: ADEQUAÇÃO (Backend legado → modernizado)

| Passo | Contrato | Checklist | Prompt | Agente | Script |
|-------|----------|-----------|--------|--------|--------|
| 1. Regularizar | CONTRATO-DE-REGULARIZACAO-DE-BACKEND | checklist-regularizacao-backend.yaml | adequacao/01-regularizar-backend.md | backend-regularizer | - |
| 2. Validar Contrato | CONTRATO-EXECUCAO-TESTER-BACKEND | checklist-tester-backend.yaml | adequacao/02-validar-contrato.md | tester | - |
| 3. Frontend | CONTRATO-EXECUCAO-FRONTEND | checklist-frontend.yaml | adequacao/03-frontend.md | developer | - |
| 4. Testes | CONTRATO-EXECUCAO-TESTES | checklist-testes.yaml | adequacao/04-testes.md | tester | - |

---

## Fluxo: MANUTENÇÃO (Correção, hotfix, debug)

| Passo | Contrato | Checklist | Prompt | Agente | Script |
|-------|----------|-----------|--------|--------|--------|
| 1. Debug | CONTRATO-DEBUG-CONTROLADO | checklist-debug.yaml | manutencao/01-debug.md | debugger | - |
| 2. Correção Rápida | CONTRATO-MANUTENCAO-CURTO | checklist-manutencao-curto.yaml | manutencao/02-manutencao-curta.md | developer | - |
| 3. Manutenção Backend | CONTRATO-DE-MANUTENCAO-BACKEND | checklist-manutencao-backend.yaml | manutencao/03-manutencao-backend.md | developer | - |

---

## Fluxo: DEPLOY (HOM/PRD)

| Passo | Contrato | Checklist | Prompt | Agente | Script |
|-------|----------|-----------|--------|--------|--------|
| 1. Deploy HOM | CONTRATO-DEPLOY-AZURE | checklist-deploy-prd.yaml | deploy/01-deploy-hom.md | - | - |
| 2. Deploy HOM Sem Validação | CONTRATO-DEPLOY-HOM-SEM-VALIDACAO | checklist-deploy-hom-sem-validacao.yaml | deploy/02-deploy-hom-sem-validacao.md | - | - |
| 3. Deploy PRD | CONTRATO-DEPLOY-AZURE | checklist-deploy-prd.yaml | deploy/03-deploy-prd.md | - | - |

---

## Fluxo: AUDITORIA (Conformidade)

| Passo | Contrato | Checklist | Prompt | Agente | Script |
|-------|----------|-----------|--------|--------|--------|
| 1. Auditar Backend | CONTRATO-AUDITORIA-CONFORMIDADE | checklist-auditoria-conformidade.yaml | auditoria/01-auditoria-backend.md | auditor | - |
| 2. Auditar Frontend | CONTRATO-AUDITORIA-CONFORMIDADE | checklist-auditoria-conformidade.yaml | auditoria/02-auditoria-frontend.md | auditor | - |
| 3. Auditar Completo | CONTRATO-AUDITORIA-CONFORMIDADE | checklist-auditoria-conformidade.yaml | auditoria/03-auditoria-completa.md | auditor | - |

---

## Fluxo: DEVOPS (Sincronização)

| Passo | Contrato | Checklist | Prompt | Agente | Script |
|-------|----------|-----------|--------|--------|--------|
| 1. Sync 1 RF | CONTRATO-DEVOPS-GOVERNANCA | checklist-devops.yaml | devops/01-sync-rf.md | - | sync-rf.py |
| 2. Sync Todos RFs | CONTRATO-DEVOPS-GOVERNANCA | checklist-devops.yaml | devops/02-sync-all-rfs.md | - | sync-all-rfs.py |
| 3. Sync User Stories | CONTRATO-DEVOPS-GOVERNANCA | checklist-devops.yaml | devops/03-sync-user-stories.md | - | sync-user-stories.py |

---

## Comandos → Agentes

| Comando | Agente Chamado | Contrato Ativado |
|---------|----------------|------------------|
| /start-rf | - | - |
| /validate-rf | - | - |
| /deploy-rf | - | CONTRATO-DEPLOY-AZURE |
| /audit-rf | auditor | CONTRATO-AUDITORIA-CONFORMIDADE |
| /fix-build | - | - |
| /sync-devops | - | CONTRATO-DEVOPS-GOVERNANCA |

---

## Scripts DevOps → Contratos

| Script | Pasta | Quando Usar | Contrato |
|--------|-------|-------------|----------|
| sync-rf.py | core/ | Sincronizar 1 RF | CONTRATO-DEVOPS-GOVERNANCA |
| sync-all-rfs.py | core/ | Sincronizar todos RFs | CONTRATO-DEVOPS-GOVERNANCA |
| sync-user-stories.py | core/ | Sincronizar user stories | CONTRATO-DEVOPS-GOVERNANCA |
| check-env.py | validation/ | Troubleshooting | - |
| update-sprint-dates.py | setup/ | Setup inicial | - |
| apply_rollback.py | governance/ | Rollback deploy | CONTRATO-DEPLOY-AZURE |

---

## Versionamento

- **Criado em:** 2025-12-28
- **Última atualização:** 2025-12-28
- **Versão:** 1.0.0
