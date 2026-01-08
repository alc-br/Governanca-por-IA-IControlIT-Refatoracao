# Sincronizar Todos RFs com Azure DevOps

Sincronizar STATUS.yaml de **TODOS os RFs** com Azure DevOps conforme contracts/devops/CONTRATO-DEVOPS-GOVERNANCA.md.

---

**Contrato ativado:** CONTRATO-DEVOPS-GOVERNANCA

**Checklist:** checklists/checklist-devops.yaml

**Script:** `python tools/devops-sync/core/sync-all-rfs.py`

**Objetivo:**
- Varrer todos os RFs em `rf/`
- Ler STATUS.yaml de cada RF
- Determinar coluna correta do board para cada
- Mover Work Items para colunas corretas
- Atualizar campos dos Work Items

**Resultado:**
- Todos STATUS.yaml → Board columns atualizados
- Todos Work Items sincronizados
- Board reflete estado real de todos RFs

**Uso:** Executar periodicamente para manter board sincronizado
