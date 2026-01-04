# ORDEM DE EXECUÇÃO DE CONTRATOS

**Versão:** 1.0
**Data de criação:** 2025-12-26
**Propósito:** Guia sequencial numerado para execução de contratos no IControlIT

---

## VISÃO GERAL

Este documento define a **ordem correta de execução** de todos os contratos de governança do IControlIT. Cada prompt/contrato está numerado e inclui pré-requisitos, gatilhos e próximos passos.

---

## FASE 1: DOCUMENTAÇÃO

### 1. CONTRATO-DOCUMENTACAO-ESSENCIAL

**Arquivo:** `/docs/contracts/CONTRATO-DOCUMENTACAO-ESSENCIAL.md`

**Quando executar:**
- Quando existe apenas ideia ou descrição do RF
- Código legado existe mas sem documentação formal
- RF novo que precisa ser especificado

**Pré-requisitos:**
- Acesso ao código legado (se aplicável)
- Acesso ao modelo físico do banco de dados
- Pasta do RF criada

**Prompt de ativação:**
```
Conforme CONTRATO DE DOCUMENTACAO-ESSENCIAL para RFXXX
```

**Saídas esperadas:**
- RF-XXX.md (5 seções obrigatórias)
- UC-RF-XXX.md (5 casos de uso)
- MD-RF-XXX.md (modelo de dados com DDL)
- WF-RF-XXX.md (wireframes e componentes)

**Próximo passo:** #2 (CONTRATO-DOCUMENTACAO-GOVERNADA-TESTES)

---

### 2. CONTRATO-DOCUMENTACAO-GOVERNADA-TESTES

**Arquivo:** `/docs/contracts/CONTRATO-DOCUMENTACAO-GOVERNADA-TESTES.md`

**Quando executar:**
- Após RF, UC, MD e WF estarem completos e aprovados
- STATUS.yaml com `documentacao: all True`

**Pré-requisitos (BLOQUEANTES):**
- RF-XXX.md aprovado
- UC-RF-XXX.md aprovado
- MD-RF-XXX.md aprovado
- WF-RF-XXX.md aprovado

**Prompt de ativação:**
```
Conforme CONTRATO DE DOCUMENTACAO-GOVERNADA-TESTES para RFXXX
```

**Saídas esperadas:**
- TC-RFXXX-BACKEND.md
- TC-RFXXX-FRONTEND.md
- TC-RFXXX-SEGURANCA.md
- TC-RFXXX-E2E.md

**Próximo passo:** #3 (CONTRATO-EXECUCAO-BACKEND) ou #4 (CONTRATO-REGULARIZACAO-BACKEND se legado)

---

## FASE 2: DESENVOLVIMENTO BACKEND

### 3. CONTRATO-EXECUCAO-BACKEND

**Arquivo:** `/docs/contracts/CONTRATO-EXECUCAO-BACKEND.md`

**Quando executar:**
- Backend não existe ainda
- Backend será criado do zero
- Documentação (RF, UC, MD) está completa

**Pré-requisitos (BLOQUEANTES):**
- RF-XXX.md completo
- UC-RF-XXX.md completo
- MD-RF-XXX.md completo
- TC-RFXXX-BACKEND.md completo

**Prompt de ativação:**
```
Conforme CONTRATO DE EXECUCAO – BACKEND para RFXXX
```

**Saídas esperadas:**
- Código backend (.NET)
- Migrations de banco de dados
- Seeds de dados
- Permissões configuradas
- Testes unitários mínimos
- EXECUTION-MANIFEST atualizado (tipo: OPERACIONAL)

**Próximo passo:** #5 (CONTRATO-EXECUCAO-TESTER-BACKEND)

---

### 4. CONTRATO-REGULARIZACAO-BACKEND

**Arquivo:** `/docs/contracts/CONTRATO-REGULARIZACAO-BACKEND.md`

**Quando executar:**
- Backend existe mas foi criado antes da governança
- Backend não está 100% aderente ao RF
- Frontend já depende do backend existente

**Pré-requisitos (BLOQUEANTES):**
- Backend legado existe
- RF-XXX.md completo
- UC-RF-XXX.md completo
- MD-RF-XXX.md completo

**Prompt de ativação:**
```
Conforme CONTRATO DE REGULARIZACAO DE BACKEND para RFXXX
```

**Saídas esperadas:**
- Backend normalizado (mínimas alterações)
- Compatibilidade com frontend mantida
- Aderência ao RF aumentada
- EXECUTION-MANIFEST atualizado

**Próximo passo:** #5 (CONTRATO-EXECUCAO-TESTER-BACKEND)

---

### 5. CONTRATO-EXECUCAO-TESTER-BACKEND

**Arquivo:** `/docs/contracts/CONTRATO-EXECUCAO-TESTER-BACKEND.md`

**Quando executar:**
- Backend implementado (#3) ou regularizado (#4)
- Código backend está em branch pronto para merge

**Pré-requisitos (BLOQUEANTES):**
- Backend implementado/regularizado
- EXECUTION-MANIFEST com execução de backend (tipo: OPERACIONAL)
- STATUS.yaml com `desenvolvimento.backend.status: done`

**Prompt de ativação:**
```
Conforme CONTRATO DE EXECUCAO – TESTER-BACKEND para RFXXX
```

**Saídas esperadas:**
- Contrato backend testado
- Matriz de violação criada
- Testes de violação implementados
- EXECUTION-MANIFEST atualizado (tipo: DECISORIA)
- decision.resultado: APROVADO ou REPROVADO
- STATUS.yaml com `contrato_validado: true` (se aprovado)

**Próximo passo:**
- Se APROVADO → #6 (CONTRATO-TRANSICAO-BACKEND-PARA-TESTES)
- Se REPROVADO → #3 ou #4 (retrabalho backend)

---

### 6. CONTRATO-TRANSICAO-BACKEND-PARA-TESTES

**Arquivo:** `/docs/contracts/CONTRATO-TRANSICAO-BACKEND-PARA-TESTES.md`

**Quando executar:**
- Backend foi APROVADO pelo Tester-Backend
- EXECUTION-MANIFEST tem decisão APROVADA
- Frontend pode ou não estar implementado

**Pré-requisitos (BLOQUEANTES):**
- EXECUTION-MANIFEST com decisão APROVADA do Tester-Backend
- STATUS.yaml com `contrato_validado: true`

**Prompt de ativação:**
```
Conforme CONTRATO DE TRANSICAO-BACKEND-PARA-TESTES para RFXXX
```

**Saídas esperadas:**
- STATUS.yaml atualizado:
  - `contrato_ativo: CONTRATO-EXECUCAO-TESTES`
  - `board_column: "Pronto para Testes"`
- EXECUTION-MANIFEST com registro de transição

**IMPORTANTE:** Este contrato NÃO executa testes. Apenas autoriza a transição.

**Próximo passo:**
- Se frontend necessário → #7 (CONTRATO-EXECUCAO-FRONTEND)
- Se frontend não necessário → #8 (CONTRATO-EXECUCAO-TESTES)

---

## FASE 3: DESENVOLVIMENTO FRONTEND

### 7. CONTRATO-EXECUCAO-FRONTEND

**Arquivo:** `/docs/contracts/CONTRATO-EXECUCAO-FRONTEND.md`

**Quando executar:**
- Backend foi aprovado e mergeado em `dev`
- WF-RF-XXX.md está completo
- Frontend será implementado

**Pré-requisitos (BLOQUEANTES):**
- Backend aprovado e em `dev`
- WF-RF-XXX.md completo
- TC-RFXXX-FRONTEND.md completo
- STATUS.yaml com `desenvolvimento.backend.contrato_validado: true`

**Prompt de ativação:**
```
Conforme CONTRATO DE EXECUCAO – FRONTEND para RFXXX
```

**Saídas esperadas:**
- Código frontend (Angular)
- Componentes, serviços, rotas
- Formulários com validação
- Testes unitários
- EXECUTION-MANIFEST atualizado (tipo: OPERACIONAL)

**Próximo passo:** #8 (CONTRATO-EXECUCAO-TESTES)

---

## FASE 4: EXECUÇÃO DE TESTES

### 8. CONTRATO-EXECUCAO-TESTES

**Arquivo:** `/docs/contracts/CONTRATO-EXECUCAO-TESTES.md`

**Quando executar:**
- Backend aprovado
- Frontend implementado (se aplicável)
- STATUS.yaml com `contrato_ativo: CONTRATO-EXECUCAO-TESTES`

**Pré-requisitos (BLOQUEANTES):**
- Backend aprovado pelo Tester-Backend
- EXECUTION-MANIFEST com decisão APROVADA
- TC-RFXXX-*.md completos (backend, frontend, e2e, segurança)

**Prompt de ativação:**
```
Conforme CONTRATO DE EXECUCAO DE TESTES para RFXXX
```

**Saídas esperadas:**
- Testes backend executados (taxa de aprovação)
- Testes frontend executados (taxa de aprovação)
- Testes E2E executados (taxa de aprovação)
- Testes segurança executados (taxa de aprovação)
- Taxa geral de aprovação: 100%
- Evidências (screenshots, logs)
- EXECUTION-MANIFEST atualizado (tipo: DECISORIA)
- decision.resultado: APROVADO ou REPROVADO

**Próximo passo:**
- Se taxa = 100% → #9 (CONTRATO-TRANSICAO-TESTES-PARA-DEPLOY)
- Se taxa < 100% → Correções + re-executar #8

---

## FASE 5: TRANSIÇÃO PARA DEPLOY

### 9. CONTRATO-TRANSICAO-TESTES-PARA-DEPLOY

**Arquivo:** `/docs/contracts/CONTRATO-TRANSICAO-TESTES-PARA-DEPLOY.md`

**Quando executar:**
- Testes foram APROVADOS (taxa = 100%)
- EXECUTION-MANIFEST tem decisão APROVADA

**Pré-requisitos (BLOQUEANTES):**
- EXECUTION-MANIFEST com decisão APROVADA de testes
- Taxa de aprovação = 100%

**Prompt de ativação:**
```
Conforme CONTRATO DE TRANSICAO-TESTES-PARA-DEPLOY para RFXXX
```

**Saídas esperadas:**
- STATUS.yaml atualizado:
  - `contrato_ativo: CONTRATO-EXECUCAO-DEPLOY`
  - `board_column: "Pronto para Deploy"`
- EXECUTION-MANIFEST com registro de transição

**IMPORTANTE:** Este contrato NÃO executa deploy. Apenas autoriza a transição.

**Próximo passo:** #10 (CONTRATO-EXECUCAO-DEPLOY)

---

## FASE 6: DEPLOY

### 10. CONTRATO-EXECUCAO-DEPLOY

**Arquivo:** `/docs/contracts/CONTRATO-EXECUCAO-DEPLOY.md`

**Quando executar:**
- Aprovação formal para deploy recebida
- STATUS.yaml com `contrato_ativo: CONTRATO-EXECUCAO-DEPLOY`

**Pré-requisitos (BLOQUEANTES):**
- EXECUTION-MANIFEST com transição aprovada (#9)
- Aprovação formal de Release Manager (PRD) ou DevOps (HOM)

**Prompt de ativação:**
```
Conforme CONTRATO DE EXECUCAO-DEPLOY para RFXXX em [HOM|PRD]
```

**Saídas esperadas:**
- Build executado
- Deploy realizado
- Smoke tests executados
- Versão registrada
- EXECUTION-MANIFEST atualizado (tipo: DECISORIA)
- decision.resultado: APROVADO ou REPROVADO

**Próximo passo:**
- Se smoke tests PASS → FIM (sucesso)
- Se smoke tests FAIL → #11 (CONTRATO-ROLLBACK - automático)

---

## FASE 7: ROLLBACK (SE NECESSÁRIO)

### 11. CONTRATO-ROLLBACK

**Arquivo:** `/docs/contracts/CONTRATO-ROLLBACK.md`

**Quando executar:**
- Smoke tests falharam (automático)
- Decisão de negócio (manual)
- Erro crítico detectado em produção

**Pré-requisitos (BLOQUEANTES):**
- Deploy executado (#10)
- Motivo documentado

**Prompt de ativação (automático):**
```
Rollback automático ativado por falha de smoke test
```

**Prompt de ativação (manual):**
```
Conforme CONTRATO-ROLLBACK para RFXXX
Motivo: [descrição]
Autorizado por: [nome]
```

**Saídas esperadas:**
- Versão anterior identificada
- Rollback de código executado
- Smoke tests pós-rollback executados
- EXECUTION-MANIFEST atualizado (tipo: DECISORIA CRÍTICA)
- STATUS.yaml atualizado com rollback

**Próximo passo:**
- Investigar causa → #12 (CONTRATO-DEBUG-CONTROLADO)
- Corrigir problema → Reiniciar do passo apropriado

---

## CONTRATOS DE SUPORTE (PARALELOS)

### 12. CONTRATO-DEBUG-CONTROLADO

**Arquivo:** `/docs/contracts/CONTRATO-DEBUG-CONTROLADO.md`

**Quando executar:**
- Bug identificado mas causa desconhecida
- Investigação necessária antes de corrigir
- Rollback executado

**Pré-requisitos:**
- Erro ou bug documentado

**Prompt de ativação:**
```
Conforme CONTRATO DE DEBUG para investigar [descrição do erro] em RFXXX
```

**Saídas esperadas:**
- Análise técnica
- Hipóteses ordenadas
- Causa raiz identificada (ou indeterminada)
- Plano de correção (sem executar)

**Próximo passo:** #13 ou #14 (CONTRATO-MANUTENCAO)

---

### 13. CONTRATO-MANUTENCAO-CORRECAO-CONTROLADA

**Arquivo:** `/docs/contracts/CONTRATO-MANUTENCAO-CORRECAO-CONTROLADA.md`

**Quando executar:**
- Causa raiz identificada (#12)
- Correção necessária
- Escopo delimitado

**Pré-requisitos:**
- Debug concluído
- Causa raiz conhecida

**Prompt de ativação:**
```
Conforme CONTRATO DE MANUTENCAO para corrigir [descrição] em RFXXX
```

**Saídas esperadas:**
- Código corrigido
- Testes validados
- EXECUTION-MANIFEST atualizado

**Próximo passo:** #8 (CONTRATO-EXECUCAO-TESTES)

---

### 14. CONTRATO-MANUTENCAO-BACKEND

**Arquivo:** `/docs/contracts/CONTRATO-DE-MANUTENCAO-BACKEND.md`

**Quando executar:**
- Manutenção específica de backend necessária
- Otimização, logging, refatoração

**Pré-requisitos:**
- Backend validado anteriormente

**Prompt de ativação:**
```
Conforme CONTRATO DE MANUTENCAO DE BACKEND para RFXXX
```

**Saídas esperadas:**
- Backend otimizado/corrigido
- EXECUTION-MANIFEST atualizado

**Próximo passo:** #5 (CONTRATO-EXECUCAO-TESTER-BACKEND) - revalidar contrato

---

### 15. CONTRATO-AUDITORIA-CONFORMIDADE

**Arquivo:** `/docs/contracts/CONTRATO-AUDITORIA-CONFORMIDADE.md`

**Quando executar:**
- Antes de marcar RF como concluído
- Code review
- Validação de conformidade

**Pré-requisitos:**
- Implementação concluída

**Prompt de ativação:**
```
Conforme CONTRATO DE AUDITORIA para auditar RFXXX
```

**Saídas esperadas:**
- Relatório de gaps
- Classificação de divergências
- Evidências
- Recomendações

**Próximo passo:** Corrigir gaps ou declarar CONFORME

---

### 16. CONTRATO-DEVOPS-GOVERNANCA

**Arquivo:** `/docs/contracts/CONTRATO-DEVOPS-GOVERNANCA.md`

**Quando executar:**
- Sincronização com Azure DevOps necessária
- Atualização de board
- Auditoria de estado

**Pré-requisitos:**
- STATUS.yaml atualizado

**Prompt de ativação:**
```
Conforme CONTRATO DE DEVOPS GOVERNANCA para sincronizar RFXXX
```

**Saídas esperadas:**
- Azure DevOps sincronizado
- Board atualizado
- EXECUTION-MANIFEST atualizado

**Próximo passo:** Nenhum (operacional)

---

## FLUXO RÁPIDO POR TIPO DE RF

### RF Novo (sem código legado)

1. CONTRATO-DOCUMENTACAO-ESSENCIAL (#1)
2. CONTRATO-DOCUMENTACAO-GOVERNADA-TESTES (#2)
3. CONTRATO-EXECUCAO-BACKEND (#3)
4. CONTRATO-EXECUCAO-TESTER-BACKEND (#5)
5. CONTRATO-TRANSICAO-BACKEND-PARA-TESTES (#6)
6. CONTRATO-EXECUCAO-FRONTEND (#7) - se necessário
7. CONTRATO-EXECUCAO-TESTES (#8)
8. CONTRATO-TRANSICAO-TESTES-PARA-DEPLOY (#9)
9. CONTRATO-EXECUCAO-DEPLOY (#10)

### RF com Backend Legado

1. CONTRATO-DOCUMENTACAO-ESSENCIAL (#1)
2. CONTRATO-DOCUMENTACAO-GOVERNADA-TESTES (#2)
3. CONTRATO-REGULARIZACAO-BACKEND (#4)
4. CONTRATO-EXECUCAO-TESTER-BACKEND (#5)
5. CONTRATO-TRANSICAO-BACKEND-PARA-TESTES (#6)
6. CONTRATO-EXECUCAO-FRONTEND (#7) - se necessário
7. CONTRATO-EXECUCAO-TESTES (#8)
8. CONTRATO-TRANSICAO-TESTES-PARA-DEPLOY (#9)
9. CONTRATO-EXECUCAO-DEPLOY (#10)

### Correção de Bug

1. CONTRATO-DEBUG-CONTROLADO (#12)
2. CONTRATO-MANUTENCAO-CORRECAO-CONTROLADA (#13)
3. CONTRATO-EXECUCAO-TESTES (#8)
4. CONTRATO-TRANSICAO-TESTES-PARA-DEPLOY (#9)
5. CONTRATO-EXECUCAO-DEPLOY (#10)

### Hotfix em Produção

1. CONTRATO-HOTFIX-EM-PRODUCAO
2. CONTRATO-EXECUCAO-DEPLOY (#10)
3. Se falhar → CONTRATO-ROLLBACK (#11)

---

## REGRAS CRÍTICAS

### Bloqueios Absolutos

1. **Backend SEM validação de contrato NÃO pode ir para testes**
   - OBRIGATÓRIO executar #5 (TESTER-BACKEND) antes de #8 (TESTES)

2. **Testes com taxa < 100% NÃO podem ir para deploy**
   - OBRIGATÓRIO re-executar #8 até taxa = 100%

3. **Deploy SEM transição aprovada é INVÁLIDO**
   - OBRIGATÓRIO executar #9 antes de #10

4. **Rollback SEM motivo documentado é BLOQUEADO**
   - OBRIGATÓRIO documentar motivo em #11

### Autoridades por Contrato

| Contrato | Autoridade | Pode Aprovar? |
|----------|-----------|---------------|
| #3 BACKEND | Developer | NÃO (só implementa) |
| #5 TESTER-BACKEND | Tester-Backend | SIM (aprova/reprova) |
| #8 TESTES | QA / Tester | SIM (aprova/reprova) |
| #10 DEPLOY | DevOps | SIM (executa) |
| #11 ROLLBACK | DevOps (auto) ou Release Manager (manual) | SIM |

### Segregação de Funções (SoD)

- Developer NÃO pode aprovar próprio código
- Tester-Backend NÃO pode corrigir código
- QA NÃO pode alterar código
- DevOps NÃO pode pular validações

---

## VALIDAÇÃO DE TRANSIÇÕES

Antes de executar qualquer contrato, validar transição:

```bash
python d:/IC2/docs/tools/contract-validator/validate-transitions.py RFXXX PROXIMO-CONTRATO
```

Exemplo:
```bash
python validate-transitions.py RF046 CONTRATO-EXECUCAO-TESTES
```

Se transição não for permitida, o script retorna erro explicativo.

---

## ORDEM DE PRIORIDADE

1. **BLOQUEANTES:** #5 (TESTER-BACKEND), #8 (TESTES com taxa 100%), #9 (TRANSICAO-DEPLOY)
2. **CRÍTICOS:** #10 (DEPLOY), #11 (ROLLBACK)
3. **IMPORTANTES:** #3 (BACKEND), #7 (FRONTEND)
4. **SUPORTE:** #12 (DEBUG), #13 (MANUTENCAO), #15 (AUDITORIA)

---

**FIM DO DOCUMENTO**
