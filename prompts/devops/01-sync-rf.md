# Sincronizar RF com Azure DevOps

Sincronizar STATUS.yaml do **RF-XXX** com Azure DevOps conforme contracts/devops/CONTRATO-DEVOPS-GOVERNANCA.md.

**RF:** [Especificar RF, ex: RF-027]

---

**Contrato ativado:** CONTRATO-DEVOPS-GOVERNANCA

**Checklist:** checklists/checklist-devops.yaml

**Script:** `python tools/devops-sync/core/sync-rf.py RF-XXX`

**Objetivo:**
- Ler STATUS.yaml do RF
- Determinar coluna correta do board
- Mover Work Item para coluna correta
- Atualizar campos do Work Item

**Resultado:**
- STATUS.yaml → Board column atualizado
- Work Item sincronizado
- Board reflete estado real do RF
