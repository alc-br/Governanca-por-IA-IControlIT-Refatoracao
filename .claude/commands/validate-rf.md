---
description: Validar build, testes e documentação completos de um RF
allowed-tools: Read, Bash, Grep, TodoWrite
---

# Validar RF

Valida que um Requisito Funcional está completo e pronto para produção.

## Instruções

1. **Pergunte ao usuário:** Qual RF deseja validar? (ex: RF-028)

2. **Validar Documentação (5/5)**
   ```bash
   # Verificar arquivos obrigatórios
   ls D:\IC2_Governanca\rf\Fase-*/EPIC-*/RF-XXX/RF-XXX.md
   ls D:\IC2_Governanca\rf\Fase-*/EPIC-*/RF-XXX/UC-RF-XXX.md
   ls D:\IC2_Governanca\rf\Fase-*/EPIC-*/RF-XXX/MD-RF-XXX.md
   ls D:\IC2_Governanca\rf\Fase-*/EPIC-*/RF-XXX/WF-RF-XXX.md
   ls D:\IC2_Governanca\rf\Fase-*/EPIC-*/RF-XXX/user-stories.yaml
   ```

3. **Validar STATUS.yaml**
   ```yaml
   # Verificar que tudo está True
   documentacao:
     rf: true
     uc: true
     md: true
     wf: true
     user_stories: true
     documentacao_testes: true

   implementacao:
     backend: true
     frontend: true
     testes_backend: true
     testes_frontend: true
     testes_outros: true

   validacao:
     tester_backend_aprovado: true
     auditoria_conformidade: true
   ```

4. **Validar Build Backend**
   ```bash
   cd backend/IControlIT.Api
   dotnet build --configuration Release
   # Deve retornar: Build succeeded. 0 Error(s)
   ```

5. **Validar Build Frontend**
   ```bash
   cd frontend/icontrolit-app
   npm run build
   # Deve retornar: Build at: YYYY-MM-DDTHH:MM:SS (sem erros)
   ```

6. **Validar Testes Backend**
   ```bash
   cd backend/IControlIT.Tests
   dotnet test --no-build
   # Deve retornar: Passed! - Failed: 0, Passed: X, Skipped: 0
   ```

7. **Validar Testes E2E**
   ```bash
   cd frontend/icontrolit-app
   npx playwright test e2e/rfXXX-e2e.spec.js
   # Deve retornar: X passed (100%)
   ```

8. **Validar Auditoria de Conformidade**
   - Verificar se existe relatório em:
     `D:\IC2\relatorios\AAAA-MM-DD-RFXXX-COMPLETO-Gaps.md`
   - Verificar taxa de conformidade >= 95%

9. **Gerar Relatório de Validação**

   Criar checklist com TodoWrite:
   - [ ] Documentação 100% completa
   - [ ] STATUS.yaml 100% True
   - [ ] Build backend OK
   - [ ] Build frontend OK
   - [ ] Testes backend 100% PASS
   - [ ] Testes E2E 100% PASS
   - [ ] Auditoria conformidade >= 95%

10. **Informar Resultado**

    **Se 100% OK:**
    ```
    ✅ RF-XXX VALIDADO - Pronto para Produção

    📋 Documentação: 5/5 ✅
    🔧 Implementação: 2/2 ✅
    ✅ Testes: 100% PASS
    📊 Conformidade: 98% ✅

    🚀 Próximos Passos:
    1. Deploy HOM: D:\IC2_Governanca\prompts\deploy/01-deploy-hom.md
    2. Deploy PRD: D:\IC2_Governanca\prompts\deploy/03-deploy-prd.md
    ```

    **Se houver problemas:**
    ```
    ❌ RF-XXX NÃO VALIDADO - Pendências Encontradas

    📋 Documentação: 4/5 ⚠️
    - Falta: WF-RF-XXX.md

    🔧 Implementação: 2/2 ✅

    ❌ Testes: 80% PASS (2 falhas)
    - Backend: 1 falha em CreateDepartamentoCommand
    - E2E: 1 falha em exclusão de departamento

    📊 Conformidade: 85% ⚠️
    - 3 gaps CRÍTICOS identificados

    🔧 Ações Necessárias:
    1. Criar WF-RF-XXX.md
    2. Corrigir 2 testes falhando
    3. Corrigir 3 gaps críticos (ver relatório)
    4. Re-executar validação após correções
    ```

## Exemplos de Uso

### Exemplo 1: RF 100% Válido

```
Usuário: /validate-rf
Agente: Qual RF deseja validar?
Usuário: RF-028
Agente:
[Executa todos os passos de validação]

✅ RF-028 VALIDADO - Pronto para Produção

📋 Documentação: 5/5 ✅
- RF-028.md ✅
- UC-RF-028.md ✅
- MD-RF-028.md ✅
- WF-RF-028.md ✅
- user-stories.yaml ✅

🔧 Implementação: 2/2 ✅
- Backend: 15 arquivos ✅
- Frontend: 8 componentes ✅

✅ Build:
- Backend: Build succeeded (0 erros) ✅
- Frontend: Build at 2025-12-28T15:30:22 (0 erros) ✅

✅ Testes: 100% PASS
- Backend: 12 passed ✅
- E2E: 10 passed ✅
- Outros: 15 passed ✅

📊 Conformidade: 98% ✅
- Relatório: D:\IC2\relatorios\2025-12-28-RF028-COMPLETO-Gaps.md
- 1 gap MENOR (não bloqueante)

🚀 Próximos Passos:
1. Sincronizar DevOps: python D:\IC2_Governanca\tools\devops-sync/core/sync-rf.py RF028
2. Deploy HOM: D:\IC2_Governanca\prompts\deploy/01-deploy-hom.md
3. Validar HOM
4. Deploy PRD: D:\IC2_Governanca\prompts\deploy/03-deploy-prd.md
```

### Exemplo 2: RF com Pendências

```
Usuário: /validate-rf
Agente: Qual RF deseja validar?
Usuário: RF-015
Agente:
[Executa validação e encontra problemas]

❌ RF-015 NÃO VALIDADO - Pendências Encontradas

📋 Documentação: 5/5 ✅

🔧 Implementação: 2/2 ✅

❌ Build:
- Backend: Build succeeded ✅
- Frontend: Build FAILED ❌
  - Error: Cannot find module '@angular/common'
  - Solução: npm install

❌ Testes: 67% PASS (3 falhas)
- Backend: 10 passed, 2 failed ❌
  - CreateDepartamentoCommandTests.Should_Reject_Invalid_Nome (FAIL)
  - DeleteDepartamentoCommandTests.Should_Soft_Delete (FAIL)
- E2E: 8 passed, 1 failed ❌
  - should delete departamento (FAIL: botão excluir não encontrado)

📊 Conformidade: 72% ⚠️
- Relatório: D:\IC2\relatorios\2025-12-28-RF015-COMPLETO-Gaps.md
- 2 gaps CRÍTICOS
- 5 gaps IMPORTANTES

🔧 Ações Necessárias:

1. **Corrigir build frontend:**
   ```bash
   cd frontend/icontrolit-app
   npm install
   npm run build
   ```

2. **Corrigir testes backend:**
   - Verificar validação MinLength em CreateDepartamentoCommand
   - Verificar soft delete em DeleteDepartamentoCommand

3. **Corrigir teste E2E:**
   - Adicionar botão excluir na listagem (GAP-FRONTEND-001)

4. **Corrigir gaps críticos:**
   - Ver detalhes em: D:\IC2\relatorios\2025-12-28-RF015-COMPLETO-Gaps.md

5. **Re-executar validação:**
   /validate-rf → RF-015
```

## Troubleshooting

### Build falha

**Backend:**
```bash
# Limpar e rebuildar
dotnet clean
dotnet restore
dotnet build
```

**Frontend:**
```bash
# Limpar cache e reinstalar
rm -rf node_modules package-lock.json
npm install
npm run build
```

### Testes falham

**Identificar causa:**
```bash
# Backend: executar teste específico
dotnet test --filter FullyQualifiedName~CreateDepartamentoCommandTests

# Frontend: executar teste específico em headed mode
npx playwright test e2e/rf015-e2e.spec.js --headed
```

### Auditoria ausente

Se não houver relatório de auditoria:
```bash
# Executar auditoria
# Ver: D:\IC2_Governanca\prompts\auditoria/03-auditoria-completa.md
```

## Notas

- Validação deve ser executada **ANTES** de marcar RF como concluído
- Validação deve ser executada **ANTES** de deploy para HOM
- Se validação falhar, corrigir sob CONTRATO-MANUTENCAO
- Após correções, **RE-EXECUTAR** validação completa
