# CONTRATO DE EXECUÇÃO — FRONTEND ADITIVO

**Versão:** 1.0 | **Data:** 2026-01-03 | **Status:** Ativo

## Sumário

Implementa incrementalmente no frontend as mudanças especificadas no ADITIVO (RF, UC, WF).

**Entrada:** RFXXX.md, UC-RFXXX.yaml, WF-RFXXX.yaml + versões `_old` + relatório delta
**Saída:** Código Angular atualizado + relatório `.temp_ia/frontend-aditivo-RFXXX-relatorio.md`

## Ativação

```
Conforme contracts/desenvolvimento/execucao/frontend-aditivo.md para RFXXX.
```

## Pré-Requisitos

1. ✅ ADITIVO de documentação executado e validado
2. ✅ BACKEND ADITIVO executado (endpoints disponíveis)
3. ✅ Relatório de delta existe
4. ✅ Branch correto (`feature/RFXXX-aditivo-*`)

## Workflow

### FASE 1: ANÁLISE DE DELTA

1. Comparar WF-RFXXX.yaml vs WF-RFXXX_old.yaml (novos WFs)
2. Comparar UC-RFXXX.yaml vs UC-RFXXX_old.yaml (novos UCs)
3. Ler `.temp_ia/aditivo-RFXXX-delta-report.md`
4. Identificar: componentes, rotas, serviços, formulários, chaves i18n

### FASE 2: IMPLEMENTAÇÃO

1. **Services:** Criar/atualizar serviços para novos endpoints
2. **Components:** Criar novos componentes para novas telas (WFs novos)
3. **Routes:** Adicionar rotas em `app.routes.ts`
4. **Forms:** Criar formulários com validações (RNs)
5. **i18n:** Adicionar chaves de tradução (`pt.json`, `en.json`)
6. **Permissions:** Aplicar `*ixHasPermission` nos componentes
7. **Tests:** Criar testes unitários (Jasmine/Karma)

### FASE 3: VALIDAÇÃO

1. `npm run build` (DEVE PASSAR)
2. `npm run test` (DEVE PASSAR)
3. `npm start` (verificar funcionamento manual)

### FASE 4: RELATÓRIO

Gerar `.temp_ia/frontend-aditivo-RFXXX-relatorio.md`:

```markdown
# RELATÓRIO - FRONTEND ADITIVO RFXXX

## DELTA IMPLEMENTADO
- ✅ Service: ClienteExportacaoService (método exportarPdf)
- ✅ Component: ClienteExportacaoPdfComponent
- ✅ Route: `/clientes/exportar-pdf`
- ✅ i18n: 5 chaves adicionadas
- ✅ Tests: 12 testes criados

## VALIDAÇÕES
- ✅ Build: PASS
- ✅ Tests: 12/12 PASS

## VEREDICTO
✅ FRONTEND ADITIVO IMPLEMENTADO COM SUCESSO
```

## Critérios de Aprovação

✅ APROVADO: Build PASS + Tests PASS + Relatório completo
❌ REPROVADO: Build FAIL OU Tests FAIL OU Relatório incompleto

## Regras Invioláveis

1. SEMPRE comparar WF/UC originais vs `_old`
2. SEMPRE criar componentes para TODOS os WFs novos
3. SEMPRE adicionar chaves i18n
4. SEMPRE aplicar permissões (RBAC)
5. SEMPRE criar testes unitários

---

**Versão:** 1.0 | **Mantido por:** Time IControlIT | **Governado por:** D:\IC2\CLAUDE.md
