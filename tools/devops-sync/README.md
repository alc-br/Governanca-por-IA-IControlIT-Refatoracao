# Scripts de Sincronização com Azure DevOps

Este diretório contém scripts Python para sincronizar artefatos locais (STATUS.yaml, user-stories.yaml) com o Azure DevOps Board.

## Estrutura de Pastas

```
tools/devops-sync/
├── README.md                    # Esta documentação
│
├── core/                        # Scripts essenciais (uso regular)
│   ├── sync-rf.py               # Sincroniza 1 RF
│   ├── sync-all-rfs.py          # Sincroniza todos RFs
│   └── sync-user-stories.py     # Sincroniza user stories
│
├── validation/                  # Scripts troubleshooting
│   ├── check-env.py
│   ├── find-kanban-field.py
│   ├── check-team-sprints.py
│   ├── check-iteration-dates.py
│   ├── check-work-item.py
│   ├── validate-sprint-backlogs.py
│   ├── diagnose-sprint-backlog-empty.py
│   ├── check-backlog-levels.py
│   ├── check-classification-nodes.py
│   ├── check-team-iterations-detailed.py
│   ├── list-all-iterations.py
│   └── verify-sprint-dates.py
│
├── setup/                       # Scripts configuração inicial (1x)
│   ├── create-work-items.py
│   ├── create-iterations.py
│   ├── create-area-paths.py
│   ├── create-board-column.py
│   ├── create-missing-status.py
│   ├── create-delivery-plan.py
│   ├── configure-team-sprints.py
│   ├── assign-items-to-sprints.py
│   ├── refresh-team-iterations.py
│   └── update-sprint-dates.py   # Consolidado (3 modos: direct, hierarchy, by-id)
│
├── governance/                  # Scripts transição
│   ├── apply_rollback.py
│   └── apply_tests_to_deploy_transition.py
│
└── deprecated/                  # Scripts obsoletos
    ├── update-rf-status.py      # Substituído por sync-all-rfs.py
    ├── recreate-work-items-hierarchical.py
    ├── delete-all-work-items.py # RISCO ALTO
    ├── update-sprint-dates-hierarchy.py # Consolidado em setup/update-sprint-dates.py
    ├── update-sprint-dates-by-id.py # Consolidado em setup/update-sprint-dates.py
    ├── update-sprint-dates-direct.py # Consolidado em setup/update-sprint-dates.py
    ├── sync-board.py.bak
    └── sync-rf.py.bak
```

## Pré-requisitos

Todas as operações requerem variável de ambiente configurada:

```bash
export AZURE_DEVOPS_PAT="seu_personal_access_token"
```

**Windows PowerShell:**
```powershell
$env:AZURE_DEVOPS_PAT="seu_personal_access_token"
```

## Quando Usar Cada Pasta

| Pasta | Quando Usar | Frequência |
|-------|-------------|------------|
| **core/** | Uso diário/regular | Sempre |
| **validation/** | Troubleshooting | Quando houver problemas |
| **setup/** | Configuração inicial | Uma vez (ou quando recriar) |
| **governance/** | Transições de estado | Quando necessário |
| **deprecated/** | **NUNCA** | Apenas referência |

## Workflow Completo para Novo RF

### 1. Setup Inicial (UMA VEZ no projeto)

```bash
# 1.1. Criar estrutura de iterações
python tools/devops-sync/setup/create-iterations.py

# 1.2. Criar áreas
python tools/devops-sync/setup/create-area-paths.py

# 1.3. Configurar sprints do time
python tools/devops-sync/setup/configure-team-sprints.py

# 1.4. Criar Work Items iniciais
python tools/devops-sync/setup/create-work-items.py

# 1.5. Atribuir Work Items a sprints
python tools/devops-sync/setup/assign-items-to-sprints.py

# 1.6. Criar Delivery Plan
python tools/devops-sync/setup/create-delivery-plan.py
```

### 2. Uso Regular (Para Cada RF)

```bash
# 2.1. Após criar documentação (CONTRATO-DOCUMENTACAO-ESSENCIAL)
python tools/devops-sync/core/sync-rf.py RF001

# 2.2. Após criar user-stories.yaml
python tools/devops-sync/core/sync-user-stories.py RF001

# 2.3. Após atualizar STATUS.yaml (qualquer mudança)
python tools/devops-sync/core/sync-rf.py RF001
```

### 3. Sincronização Periódica

```bash
# Sincronizar todos os RFs (recomendado: diariamente)
python tools/devops-sync/core/sync-all-rfs.py
```

### 4. Troubleshooting

```bash
# Validar ambiente
python tools/devops-sync/validation/check-env.py

# Diagnosticar backlog vazio
python tools/devops-sync/validation/diagnose-sprint-backlog-empty.py

# Verificar Work Item específico
python tools/devops-sync/validation/check-work-item.py
```

### 5. Transições de Estado

```bash
# Após testes 100% PASS → Deploy HOM
python tools/devops-sync/governance/apply_tests_to_deploy_transition.py RF001

# Rollback em caso de falha
python tools/devops-sync/governance/apply_rollback.py RF001
```

## Scripts Core (Uso Diário)

### sync-rf.py
**Propósito**: Sincroniza STATUS.yaml de um RF com Azure DevOps

**Uso**:
```bash
python tools/devops-sync/core/sync-rf.py RFXXX
```

**O que faz**:
- Lê STATUS.yaml do RF
- Determina coluna correta do board
- Move Work Item para coluna correta
- Atualiza campos do Work Item

**Resultado**:
- STATUS.yaml → Board column atualizado
- Work Item sincronizado
- Board reflete estado real do RF

---

### sync-all-rfs.py
**Propósito**: Sincroniza STATUS.yaml de **TODOS os RFs** com Azure DevOps

**Uso**:
```bash
python tools/devops-sync/core/sync-all-rfs.py
```

**O que faz**:
- Varre todos os RFs em `rf/`
- Lê STATUS.yaml de cada RF
- Determina coluna correta do board para cada
- Move Work Items para colunas corretas
- Atualiza campos dos Work Items

**Resultado**:
- Todos STATUS.yaml → Board columns atualizados
- Todos Work Items sincronizados
- Board reflete estado real de todos RFs

**Quando usar**: Executar periodicamente (diariamente) para manter board sincronizado

---

### sync-user-stories.py
**Propósito**: Cria User Stories no Azure DevOps a partir de user-stories.yaml

**Uso**:
```bash
python tools/devops-sync/core/sync-user-stories.py RFXXX
```

**O que faz**:
- Lê user-stories.yaml do RF
- Cria Feature (se não existir)
- Cria User Stories como Work Items
- Linka User Stories à Feature
- Linka Feature ao Epic
- Atualiza IDs no user-stories.yaml

**Resultado**:
- user-stories.yaml → Work Items criados
- Feature criada e linkada ao Epic
- User Stories criadas e linkadas à Feature
- IDs preenchidos no YAML
- Sprint Backlog populado (Features não aparecem em Sprint Backlogs por padrão)

**Campos sincronizados**:
- System.Title: `US-RFXXX-NNN: [Título]`
- System.Description: Description + Technical Notes
- Microsoft.VSTS.Common.AcceptanceCriteria: Lista de critérios
- Microsoft.VSTS.Scheduling.StoryPoints: Fibonacci (1-13)
- Microsoft.VSTS.Common.Priority: Alta=1, Média=2, Baixa=3
- System.Tags: RF code + Module
- System.LinkTypes.Hierarchy-Reverse: Link com Feature pai

---

## Troubleshooting Comum

### User Stories não aparecem no Sprint Backlog

**Causa**: Features não aparecem em Sprint Backlogs por padrão no Azure DevOps

**Solução**: Use `sync-user-stories.py` para criar User Stories que SIM aparecem nos Sprints

### Erro 400 ao criar Work Item

**Causa**: Campos obrigatórios faltando ou formato inválido

**Solução**:
1. Verifique user-stories.yaml:
   - Todos os campos obrigatórios estão preenchidos?
   - Story points são numéricos?
   - Description está no formato correto?
2. Execute validação:
   ```bash
   python tools/devops-sync/validation/check-env.py
   ```

### Work Item não move de coluna

**Causa**: Regras de transição do Board não permitem movimento

**Solução**:
1. Verifique STATUS.yaml
2. Consulte regras de transição em `core/sync-rf.py`
3. Execute diagnóstico:
   ```bash
   python tools/devops-sync/validation/find-kanban-field.py
   ```

### Sprint Backlog está vazio

**Causa**: Iteration Path não configurado ou Work Items não atribuídos

**Solução**:
```bash
# 1. Verificar configuração de iterações
python tools/devops-sync/validation/check-team-sprints.py

# 2. Diagnosticar problema específico
python tools/devops-sync/validation/diagnose-sprint-backlog-empty.py

# 3. Se necessário, atribuir items a sprints
python tools/devops-sync/setup/assign-items-to-sprints.py
```

### Datas de sprints estão erradas

**Solução**:
```bash
# Atualizar datas (modo direto)
python tools/devops-sync/setup/update-sprint-dates.py direct

# Atualizar datas (modo hierárquico)
python tools/devops-sync/setup/update-sprint-dates.py hierarchy

# Atualizar sprint específica
python tools/devops-sync/setup/update-sprint-dates.py by-id <iteration_id>
```

## Referências

- [Azure DevOps REST API](https://learn.microsoft.com/en-us/rest/api/azure/devops/)
- [Work Items API](https://learn.microsoft.com/en-us/rest/api/azure/devops/wit/)
- [CLAUDE.md - Gestão de User Stories](../../CLAUDE.md#regra-obrigatória--gestão-de-user-stories-user-storiesyaml)
- [CONTRATO-DEVOPS-GOVERNANCA](../..contracts/CONTRATO-DEVOPS-GOVERNANCA.md)

---

## Versionamento

- **Criado em:** 2025-12-23
- **Última atualização:** 2025-12-28
- **Versão:** 2.0.0 (Reorganização completa em subpastas)
