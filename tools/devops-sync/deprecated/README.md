# Scripts Deprecated - DevOps Sync

Scripts **obsoletos** que foram substituídos por versões melhoradas ou consolidadas.

⚠️ **NÃO USE** scripts desta pasta. Eles são mantidos apenas para referência histórica.

## Scripts Obsoletos

| Script | Substituído Por | Motivo |
|--------|-----------------|--------|
| **update-rf-status.py** | `core/sync-all-rfs.py` | Lógica integrada ao sync principal |
| **recreate-work-items-hierarchical.py** | `setup/create-work-items.py` | Funcionalidade integrada ao setup |
| **delete-all-work-items.py** | *(nenhum)* | **RISCO ALTO** - Deletar todos os Work Items é operação perigosa |
| **update-sprint-dates-hierarchy.py** | `setup/update-sprint-dates.py hierarchy` | Consolidado em script único |
| **update-sprint-dates-by-id.py** | `setup/update-sprint-dates.py by-id` | Consolidado em script único |
| **update-sprint-dates-direct.py** | `setup/update-sprint-dates.py direct` | Consolidado em script único |
| **sync-board.py.bak** | `core/sync-rf.py` | Backup do script antigo |
| **sync-rf.py.bak** | `core/sync-rf.py` | Backup do script antigo |

## Por Que Foram Depreciados?

### update-rf-status.py
- **Problema:** Lógica duplicada com sync-all-rfs.py
- **Solução:** Funcionalidade integrada ao sync principal

### recreate-work-items-hierarchical.py
- **Problema:** Recriação de Work Items causava perda de histórico
- **Solução:** Setup inicial usa create-work-items.py apenas uma vez

### delete-all-work-items.py
- **Problema:** **RISCO CRÍTICO** - Pode deletar todo o trabalho do time
- **Solução:** **NENHUMA** - Operação não deve ser automatizada

### update-sprint-dates-*.py (3 scripts)
- **Problema:** Lógica duplicada em 3 scripts diferentes
- **Solução:** Consolidado em `setup/update-sprint-dates.py` com 3 modos

### *.bak
- **Problema:** Backups manuais sem controle de versão
- **Solução:** Git já gerencia histórico

## Migração

Se você ainda usa algum script deprecated:

### update-rf-status.py → sync-all-rfs.py
```bash
# ANTES (deprecated)
python tools/devops-sync/deprecated/update-rf-status.py

# DEPOIS (novo)
python tools/devops-sync/core/sync-all-rfs.py
```

### update-sprint-dates-hierarchy.py → update-sprint-dates.py hierarchy
```bash
# ANTES (deprecated)
python tools/devops-sync/deprecated/update-sprint-dates-hierarchy.py

# DEPOIS (novo)
python tools/devops-sync/setup/update-sprint-dates.py hierarchy
```

### update-sprint-dates-by-id.py → update-sprint-dates.py by-id
```bash
# ANTES (deprecated)
python tools/devops-sync/deprecated/update-sprint-dates-by-id.py <id>

# DEPOIS (novo)
python tools/devops-sync/setup/update-sprint-dates.py by-id <id>
```

### update-sprint-dates-direct.py → update-sprint-dates.py direct
```bash
# ANTES (deprecated)
python tools/devops-sync/deprecated/update-sprint-dates-direct.py

# DEPOIS (novo)
python tools/devops-sync/setup/update-sprint-dates.py direct
```

## Atenção

⚠️ **delete-all-work-items.py** é script de **RISCO CRÍTICO**.

Se precisar deletar Work Items:
1. Faça **MANUALMENTE** via interface do Azure DevOps
2. Confirme **DUAS VEZES** antes de executar
3. Considere mover para "Removed" ao invés de deletar

**NUNCA** execute `delete-all-work-items.py` em produção.

## Quando Esta Pasta Será Removida?

Esta pasta será removida quando:
- ✅ Todos os scripts novos estiverem testados e validados
- ✅ Nenhum script deprecated estiver sendo referenciado em documentação
- ✅ Migração completa para nova estrutura estiver concluída
- ✅ Aprovação formal de remoção for dada

**Estimativa:** Q1 2026
