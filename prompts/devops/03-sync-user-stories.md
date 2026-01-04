# Sincronizar User Stories com Azure DevOps

Sincronizar user-stories.yaml do **RF-XXX** com Azure DevOps conforme docs/contracts/devops/CONTRATO-DEVOPS-GOVERNANCA.md.

**RF:** [Especificar RF, ex: RF-027]

---

**Contrato ativado:** CONTRATO-DEVOPS-GOVERNANCA

**Checklist:** docs/checklists/checklist-devops.yaml

**Script:** `python docs/tools/devops-sync/core/sync-user-stories.py RF-XXX`

**Objetivo:**
- Ler user-stories.yaml do RF
- Criar Feature (se não existir)
- Criar User Stories como Work Items
- Linkar User Stories à Feature
- Linkar Feature ao Epic
- Atualizar IDs no user-stories.yaml

**Resultado:**
- user-stories.yaml → Work Items criados
- Feature criada e linkada ao Epic
- User Stories criadas e linkadas à Feature
- IDs preenchidos no YAML
- Sprint Backlog populado (Features não aparecem em Sprint Backlogs por padrão)
