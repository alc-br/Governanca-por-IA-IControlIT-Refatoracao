---
description: Sincronizar STATUS.yaml com Azure DevOps
allowed-tools: Read, Bash, TodoWrite
---

# Sincronizar DevOps

Sincroniza STATUS.yaml e user-stories.yaml com Azure DevOps Board.

## Instruções

1. **Pergunte ao usuário:**
   - Sincronizar 1 RF ou todos?
   - Se 1 RF: Qual? (ex: RF-028)

2. **Sincronizar 1 RF**

   ```bash
   # Sincronizar STATUS.yaml → Board
   python D:\IC2_Governanca\tools\devops-sync/core/sync-rf.py RFXXX

   # Se user-stories.yaml foi criado/atualizado
   python D:\IC2_Governanca\tools\devops-sync/core/sync-user-stories.py RFXXX
   ```

3. **Sincronizar Todos os RFs**

   ```bash
   # Sincronizar todos STATUS.yaml → Board
   python D:\IC2_Governanca\tools\devops-sync/core/sync-all-rfs.py
   ```

4. **Verificar Resultado**

   ```bash
   # Verificar que Work Item foi movido para coluna correta
   # Abrir: https://dev.azure.com/icontrolit/IControlIT%202.0/_boards/board
   ```

5. **Criar Checklist**

   - [ ] Script executado sem erros
   - [ ] Work Item atualizado
   - [ ] Coluna do board correta
   - [ ] User Stories criadas (se aplicável)

6. **Informar Resultado**

   **1 RF:**
   ```
   ✅ RF-028 sincronizado com Azure DevOps

   📊 STATUS.yaml → Board
   - Work Item ID: 1234
   - Coluna: Em Desenvolvimento
   - Iteração: Fase 2

   📋 User Stories
   - 5 User Stories criadas
   - Linkadas à Feature RF-028
   - IDs atualizados em user-stories.yaml
   ```

   **Todos os RFs:**
   ```
   ✅ 42 RFs sincronizados com Azure DevOps

   📊 Resumo:
   - To Do: 8 RFs
   - Em Desenvolvimento: 12 RFs
   - Em Testes: 5 RFs
   - Em Homologação: 3 RFs
   - Concluído: 14 RFs

   ⏰ Tempo: 23 segundos
   ```

## Troubleshooting

### Erro 401 (Autenticação)

```bash
# Verificar PAT configurado
echo $env:AZURE_DEVOPS_PAT

# Se vazio, configurar
$env:AZURE_DEVOPS_PAT="seu_token_aqui"
```

### Work Item não moveu de coluna

Possíveis causas:
- STATUS.yaml não está atualizado corretamente
- Regras de transição do board não permitem movimento
- Work Item ID não está correto

Diagnóstico:
```bash
python D:\IC2_Governanca\tools\devops-sync/validation/check-work-item.py
```

### User Stories não aparecem no Sprint

Causa: Features não aparecem em Sprint Backlogs por padrão

Solução: User Stories SIM aparecem (sync-user-stories.py cria User Stories, não Features)

## Notas

- Executar após **QUALQUER** atualização de STATUS.yaml
- Executar após criar/atualizar user-stories.yaml
- Sincronização é **idempotente** (pode executar múltiplas vezes)
- Recomendado: executar `sync-all-rfs.py` diariamente
