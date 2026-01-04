# Sincronizar Todos RFs com Azure DevOps

Sincronizar STATUS.yaml de **TODOS os RFs** com Azure DevOps conforme docs/contracts/devops/CONTRATO-DEVOPS-GOVERNANCA.md.

---

**Contrato ativado:** CONTRATO-DEVOPS-GOVERNANCA

**Checklist:** docs/checklists/checklist-devops.yaml

**Script:** `python docs/tools/devops-sync/core/sync-all-rfs.py`

**Objetivo:**
- Varrer todos os RFs em `docs/rf/`
- Ler STATUS.yaml de cada RF
- Determinar coluna correta do board para cada
- Mover Work Items para colunas corretas
- Atualizar campos dos Work Items

**Resultado:**
- Todos STATUS.yaml → Board columns atualizados
- Todos Work Items sincronizados
- Board reflete estado real de todos RFs

**Uso:** Executar periodicamente para manter board sincronizado
