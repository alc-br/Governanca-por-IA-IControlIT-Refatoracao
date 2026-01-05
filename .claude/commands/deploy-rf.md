---
description: Deploy de RF para HOM ou PRD
allowed-tools: Read, Bash, TodoWrite
---

# Deploy RF

Executa deploy de um Requisito Funcional para HOM ou PRD.

## Instruções

1. **Pergunte ao usuário:**
   - Qual RF? (ex: RF-028)
   - Ambiente? (HOM ou PRD)

2. **Validar Pré-requisitos**

   **Para HOM:**
   - [ ] Build backend OK
   - [ ] Build frontend OK
   - [ ] Testes >= 80% PASS

   **Para PRD:**
   - [ ] Testes 100% PASS (OBRIGATÓRIO)
   - [ ] Tester-Backend aprovado (OBRIGATÓRIO)
   - [ ] Deploy HOM bem-sucedido (OBRIGATÓRIO)
   - [ ] Validação HOM OK

3. **Executar Deploy**

   **HOM com validação:**
   ```bash
   # Ver: D:\IC2_Governanca\prompts\deploy/01-deploy-hom.md
   ```

   **HOM sem validação (EXCEPCIONAL):**
   ```bash
   # Ver: D:\IC2_Governanca\prompts\deploy/02-deploy-hom-sem-validacao.md
   ```

   **PRD:**
   ```bash
   # Ver: D:\IC2_Governanca\prompts\deploy/03-deploy-prd.md
   # Requer: az login + AZURE_DEVOPS_PAT configurado
   ```

4. **Atualizar STATUS.yaml**
   ```yaml
   deploy:
     homologacao: true  # Se HOM
     producao: true     # Se PRD
   ```

5. **Sincronizar DevOps**
   ```bash
   python D:\IC2_Governanca\tools\devops-sync/core/sync-rf.py RFXXX
   ```

6. **Informar Resultado**
   ```
   ✅ Deploy RF-XXX para [HOM|PRD] concluído

   🌐 URL: [URL do ambiente]
   📦 Build: [número do build]
   ⏰ Hora: 2025-12-28 15:45:00

   ✅ Validações:
   - Backend: deployed
   - Frontend: deployed
   - Database: migrations applied
   - STATUS.yaml: atualizado
   - DevOps: sincronizado

   🎯 Próximos Passos:
   [Se HOM] Validar HOM e depois fazer deploy PRD
   [Se PRD] RF concluído ✅
   ```

## Rollback

Se deploy falhar:

```bash
# Executar rollback
python D:\IC2_Governanca\tools\devops-sync/governance/apply_rollback.py RFXXX

# Verificar logs
# Corrigir problema
# Re-executar deploy
```

## Notas

- Deploy PRD **REQUER** 100% aprovação Tester-Backend
- Deploy PRD **REQUER** validação HOM bem-sucedida
- Rollback é **OBRIGATÓRIO** em caso de falha
