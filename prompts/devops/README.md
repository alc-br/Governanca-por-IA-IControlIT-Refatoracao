# Fluxo: DEVOPS (Sincronização Azure DevOps)

Use esta sequência de prompts para sincronizar STATUS.yaml e user-stories.yaml com Azure DevOps.

## Quando usar

- Sincronizar 1 RF com Azure DevOps
- Sincronizar todos RFs com Azure DevOps
- Criar/atualizar User Stories no board

## Ordem de Execução

1. **01-sync-rf.md** - Sincronizar STATUS.yaml de 1 RF específico
2. **02-sync-all-rfs.md** - Sincronizar STATUS.yaml de todos RFs
3. **03-sync-user-stories.md** - Sincronizar user-stories.yaml (criar Work Items)

## Contratos Ativados

- CONTRATO-DEVOPS-GOVERNANCA

## Resultado Esperado

- STATUS.yaml → Coluna correta do Board
- user-stories.yaml → Work Items criados
- Feature linkado ao Epic
- User Stories linkadas à Feature
- Board atualizado corretamente

## Importante

- Sincronização é automática via scripts Python
- Scripts leem `docs/tools/devops-sync/config.yaml`
- Suporta múltiplas ferramentas (Azure DevOps, Jira, GitHub, GitLab)
- Usa Adapter Pattern para abstração
