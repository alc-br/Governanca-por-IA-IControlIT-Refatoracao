# Scripts Core - DevOps Sync

Scripts essenciais para **uso regular** na sincronização entre STATUS.yaml/user-stories.yaml e Azure DevOps.

## Scripts Disponíveis

| Script | Descrição | Quando Usar |
|--------|-----------|-------------|
| **sync-rf.py** | Sincroniza 1 RF específico | Após atualizar STATUS.yaml de 1 RF |
| **sync-all-rfs.py** | Sincroniza todos os RFs | Periodicamente ou após múltiplas alterações |
| **sync-user-stories.py** | Sincroniza user stories | Após criar/atualizar user-stories.yaml |

## Uso

### Sincronizar 1 RF
```bash
python tools/devops-sync/core/sync-rf.py RF027
```

### Sincronizar todos os RFs
```bash
python tools/devops-sync/core/sync-all-rfs.py
```

### Sincronizar User Stories
```bash
python tools/devops-sync/core/sync-user-stories.py RF027
```

## Pré-requisitos

- Variável de ambiente `AZURE_DEVOPS_PAT` configurada
- STATUS.yaml atualizado (para sync-rf / sync-all-rfs)
- user-stories.yaml atualizado (para sync-user-stories)

## Fluxo de Trabalho

1. **Após implementação de RF:**
   - Atualizar STATUS.yaml
   - Executar `sync-rf.py RFXXX`
   - Verificar board do Azure DevOps

2. **Após criar User Stories:**
   - Criar/atualizar user-stories.yaml
   - Executar `sync-user-stories.py RFXXX`
   - Verificar que Work Items foram criados

3. **Sincronização periódica:**
   - Executar `sync-all-rfs.py` (ex: diariamente)
   - Garantir que board reflete estado real

## Resultado Esperado

- **sync-rf.py**: Work Item movido para coluna correta do board
- **sync-all-rfs.py**: Todos os Work Items sincronizados
- **sync-user-stories.py**: Feature + User Stories criadas e linkadas ao Epic
