# CONTROL MATRIX – MATRIZ DE CONTROLE

**Versão:** 1.0
**Data de criação:** 2025-12-26
**Propósito:** Mapeamento de rastreabilidade RF → Contrato → Manifesto → Status → Deploy

---

## VISÃO GERAL

Este documento define a matriz de controle que mapeia cada Requisito Funcional (RF) através de todo o pipeline de desenvolvimento e deploy, demonstrando rastreabilidade completa para fins de auditoria.

---

## ESTRUTURA DA MATRIZ

Para cada RF em produção, a matriz demonstra:

```
RF → Documentação → Backend → Frontend → Testes → Deploy → Evidências
```

---

## MAPEAMENTO POR RF

### Template de Entrada na Matriz

```yaml
RF: RFXXX
titulo: <titulo do RF>

documentacao:
  rf_documento: docs/rf/RFXXX/RFXXX.md
  uc_documento: docs/rf/RFXXX/UC-RFXXX.md
  md_documento: docs/rf/RFXXX/MD-RFXXX.md
  wf_documento: docs/rf/RFXXX/WF-RFXXX.md
  status: aprovado | pendente

desenvolvimento:
  backend:
    contrato: CONTRATO-EXECUCAO-BACKEND
    manifesto_id: <ID_MANIFESTO_BACKEND>
    decisao: APROVADO | REPROVADO
    commit_hash: <hash>
    branch: feature/RFXXX-backend
    contrato_validado: true | false
    tester_manifesto_id: <ID_MANIFESTO_TESTER>

  frontend:
    contrato: CONTRATO-EXECUCAO-FRONTEND
    manifesto_id: <ID_MANIFESTO_FRONTEND>
    decisao: APROVADO | REPROVADO
    commit_hash: <hash>
    branch: feature/RFXXX-frontend

testes:
  contrato: CONTRATO-EXECUCAO-TESTES
  manifesto_id: <ID_MANIFESTO_TESTES>
  decisao: APROVADO | REPROVADO
  taxa_aprovacao: 100% | <XX%>
  evidencias:
    - docs/rf/RFXXX/evidencias/testes-backend.log
    - docs/rf/RFXXX/evidencias/testes-e2e-screenshots/
    - docs/rf/RFXXX/evidencias/testes-seguranca.log

transicao_deploy:
  contrato: CONTRATO-TRANSICAO-TESTES-PARA-DEPLOY
  manifesto_id: <ID_MANIFESTO_TRANSICAO>
  decisao: APROVADO
  timestamp: YYYY-MM-DD HH:MM:SS

deploy:
  contrato: CONTRATO-EXECUCAO-DEPLOY
  manifesto_id: <ID_MANIFESTO_DEPLOY>
  decisao: APROVADO | REPROVADO
  commit_hash: <hash>
  versao: <versao>
  ambiente: HOM | PRD
  timestamp: YYYY-MM-DD HH:MM:SS
  smoke_tests: PASS | FAIL

rollback:
  executado: true | false
  contrato: CONTRATO-ROLLBACK
  manifesto_id: <ID_MANIFESTO_ROLLBACK>
  motivo: <motivo>
  versao_revertida: <versao>
  timestamp: YYYY-MM-DD HH:MM:SS

auditoria:
  rastreavel: true | false
  conformidade_iso: true | false
  evidencias_completas: true | false
```

---

## EXEMPLOS DE CONTROLE

### Exemplo 1: RF001 (Completo)

```yaml
RF: RF001
titulo: Parametros e Configuracoes do Sistema

documentacao:
  rf_documento: docs/rf/Fase-1-Fundacao-e-Cadastros-Base/EPIC001-SYS-Sistema-Infraestrutura/RF001-Parametros-e-Configuracoes-do-Sistema/RF001.md
  uc_documento: docs/rf/Fase-1-Fundacao-e-Cadastros-Base/EPIC001-SYS-Sistema-Infraestrutura/RF001-Parametros-e-Configuracoes-do-Sistema/UC-RF001.md
  md_documento: docs/rf/Fase-1-Fundacao-e-Cadastros-Base/EPIC001-SYS-Sistema-Infraestrutura/RF001-Parametros-e-Configuracoes-do-Sistema/MD-RF001.md
  wf_documento: docs/rf/Fase-1-Fundacao-e-Cadastros-Base/EPIC001-SYS-Sistema-Infraestrutura/RF001-Parametros-e-Configuracoes-do-Sistema/WF-RF001.md
  status: aprovado

desenvolvimento:
  backend:
    contrato: CONTRATO-EXECUCAO-BACKEND
    manifesto_id: RF001-BACKEND-20251201-143000
    decisao: APROVADO
    commit_hash: abc123def456
    branch: feature/RF001-backend
    contrato_validado: true
    tester_manifesto_id: RF001-TESTER-BACKEND-20251202-100000

  frontend:
    contrato: CONTRATO-EXECUCAO-FRONTEND
    manifesto_id: RF001-FRONTEND-20251203-150000
    decisao: APROVADO
    commit_hash: def456ghi789
    branch: feature/RF001-frontend

testes:
  contrato: CONTRATO-EXECUCAO-TESTES
  manifesto_id: RF001-TESTES-20251204-140000
  decisao: APROVADO
  taxa_aprovacao: 100%
  evidencias:
    - docs/rf/Fase-1-Fundacao-e-Cadastros-Base/EPIC001-SYS-Sistema-Infraestrutura/RF001-Parametros-e-Configuracoes-do-Sistema/evidencias/testes-backend.log
    - docs/rf/Fase-1-Fundacao-e-Cadastros-Base/EPIC001-SYS-Sistema-Infraestrutura/RF001-Parametros-e-Configuracoes-do-Sistema/evidencias/testes-e2e-screenshots/

transicao_deploy:
  contrato: CONTRATO-TRANSICAO-TESTES-PARA-DEPLOY
  manifesto_id: RF001-TRANSITION-TESTS-TO-DEPLOY-20251205-100000
  decisao: APROVADO
  timestamp: 2025-12-05 10:00:00

deploy:
  contrato: CONTRATO-EXECUCAO-DEPLOY
  manifesto_id: RF001-DEPLOY-20251205-110000
  decisao: APROVADO
  commit_hash: def456ghi789
  versao: 1.0.0
  ambiente: PRD
  timestamp: 2025-12-05 11:00:00
  smoke_tests: PASS

rollback:
  executado: false

auditoria:
  rastreavel: true
  conformidade_iso: true
  evidencias_completas: true
```

---

### Exemplo 2: RF015 (Com Rollback)

```yaml
RF: RF015
titulo: Gestao Locais Enderecos

documentacao:
  rf_documento: docs/rf/Fase-2-Servicos-Essenciais/EPIC003-GES-Gestao/RF015-Gestao-Locais-Enderecos/RF015.md
  uc_documento: docs/rf/Fase-2-Servicos-Essenciais/EPIC003-GES-Gestao/RF015-Gestao-Locais-Enderecos/UC-RF015.md
  md_documento: docs/rf/Fase-2-Servicos-Essenciais/EPIC003-GES-Gestao/RF015-Gestao-Locais-Enderecos/MD-RF015.md
  wf_documento: docs/rf/Fase-2-Servicos-Essenciais/EPIC003-GES-Gestao/RF015-Gestao-Locais-Enderecos/WF-RF015.md
  status: aprovado

desenvolvimento:
  backend:
    contrato: CONTRATO-EXECUCAO-BACKEND
    manifesto_id: RF015-BACKEND-20251210-100000
    decisao: APROVADO
    commit_hash: xyz789abc123
    branch: feature/RF015-backend
    contrato_validado: true
    tester_manifesto_id: RF015-TESTER-BACKEND-20251211-143000

  frontend:
    contrato: CONTRATO-EXECUCAO-FRONTEND
    manifesto_id: RF015-FRONTEND-20251212-110000
    decisao: APROVADO
    commit_hash: jkl012mno345
    branch: feature/RF015-frontend

testes:
  contrato: CONTRATO-EXECUCAO-TESTES
  manifesto_id: RF015-TESTES-20251213-140000
  decisao: APROVADO
  taxa_aprovacao: 100%
  evidencias:
    - docs/rf/Fase-2-Servicos-Essenciais/EPIC003-GES-Gestao/RF015-Gestao-Locais-Enderecos/evidencias/

transicao_deploy:
  contrato: CONTRATO-TRANSICAO-TESTES-PARA-DEPLOY
  manifesto_id: RF015-TRANSITION-TESTS-TO-DEPLOY-20251214-100000
  decisao: APROVADO
  timestamp: 2025-12-14 10:00:00

deploy:
  contrato: CONTRATO-EXECUCAO-DEPLOY
  manifesto_id: RF015-DEPLOY-20251214-110000
  decisao: REPROVADO
  commit_hash: jkl012mno345
  versao: 1.1.0
  ambiente: HOM
  timestamp: 2025-12-14 11:00:00
  smoke_tests: FAIL

rollback:
  executado: true
  contrato: CONTRATO-ROLLBACK
  manifesto_id: RF015-ROLLBACK-20251214-110530
  motivo: Smoke tests failed
  versao_revertida: 1.0.5
  timestamp: 2025-12-14 11:05:30

auditoria:
  rastreavel: true
  conformidade_iso: true
  evidencias_completas: true
```

---

## QUERY DE RASTREABILIDADE

Para auditoria, é possível consultar a matriz para responder:

### 1. Quais RFs estão em produção?

**Filtro:**
```yaml
deploy.ambiente: PRD
deploy.decisao: APROVADO
rollback.executado: false
```

---

### 2. Qual versão de um RF específico está em produção?

**Query:**
```yaml
RF: RFXXX
deploy.versao: ?
deploy.commit_hash: ?
```

---

### 3. Todos os RFs em produção foram testados com taxa 100%?

**Validação:**
```yaml
testes.taxa_aprovacao: 100%
testes.decisao: APROVADO
```

---

### 4. Todos os RFs em produção têm backend validado por contrato?

**Validação:**
```yaml
desenvolvimento.backend.contrato_validado: true
desenvolvimento.backend.tester_manifesto_id: exists
```

---

### 5. Houve rollbacks recentemente?

**Filtro:**
```yaml
rollback.executado: true
rollback.timestamp: > YYYY-MM-DD
```

---

## VALIDAÇÕES AUTOMÁTICAS

### Script de Validação da Matriz

```python
# tools/audit/validate_control_matrix.py

def validate_rf_in_production(rf):
    """
    Valida que RF em produção tem rastreabilidade completa
    """
    checks = {
        'documentacao_completa': False,
        'backend_validado': False,
        'testes_aprovados': False,
        'deploy_aprovado': False,
        'evidencias_completas': False
    }

    # Validar documentação
    if all([
        exists(f"docs/rf/{rf}/RF{rf}.md"),
        exists(f"docs/rf/{rf}/UC-RF{rf}.md"),
        exists(f"docs/rf/{rf}/MD-RF{rf}.md"),
        exists(f"docs/rf/{rf}/WF-RF{rf}.md")
    ]):
        checks['documentacao_completa'] = True

    # Validar backend
    status = load_status_yaml(rf)
    if status['desenvolvimento']['backend']['contrato_validado'] == True:
        checks['backend_validado'] = True

    # Validar testes
    manifest = load_manifest()
    test_execution = find_test_execution(manifest, rf)
    if test_execution and test_execution['decisao'] == 'APROVADO':
        checks['testes_aprovados'] = True

    # Validar deploy
    deploy_execution = find_deploy_execution(manifest, rf)
    if deploy_execution and deploy_execution['decisao'] == 'APROVADO':
        checks['deploy_aprovado'] = True

    # Validar evidências
    if exists(f"docs/rf/{rf}/evidencias/"):
        checks['evidencias_completas'] = True

    return all(checks.values()), checks
```

---

## RELATÓRIO DE CONFORMIDADE

Para auditoria externa, gerar relatório:

### Cabeçalho

```
RELATÓRIO DE CONFORMIDADE - CONTROL MATRIX
Data: YYYY-MM-DD
RFs em Produção: X
RFs com Rastreabilidade Completa: Y
Taxa de Conformidade: Y/X = XX%
```

### Detalhamento por RF

```
RF001 - Parametros e Configuracoes do Sistema
  ✅ Documentação completa
  ✅ Backend validado por contrato
  ✅ Testes aprovados (taxa 100%)
  ✅ Deploy aprovado
  ✅ Evidências completas
  ✅ CONFORME

RF015 - Gestao Locais Enderecos
  ✅ Documentação completa
  ✅ Backend validado por contrato
  ✅ Testes aprovados (taxa 100%)
  ⚠️  Deploy com rollback (smoke tests failed)
  ✅ Evidências completas
  ⚠️  CONFORME (com ressalvas)
```

---

## PONTOS DE CONTROLE

### 1. Controle de Qualidade

**Ponto de verificação:**
- Tester-Backend valida contrato backend
- Taxa de aprovação de testes = 100%

**Evidência:**
- EXECUTION-MANIFEST com decisão APROVADO

---

### 2. Controle de Mudança

**Ponto de verificação:**
- Todo deploy tem transição aprovada
- Transição só ocorre com testes aprovados

**Evidência:**
- CONTRATO-TRANSICAO-TESTES-PARA-DEPLOY no manifesto

---

### 3. Controle de Acesso

**Ponto de verificação:**
- Nenhum agente aprova próprio trabalho
- Deploy só ocorre via contrato

**Evidência:**
- Segregação de autoridades no manifesto

---

### 4. Controle de Reversibilidade

**Ponto de verificação:**
- Rollback automático se smoke test falha
- Versão anterior identificável

**Evidência:**
- CONTRATO-ROLLBACK no manifesto (se executado)

---

## CONCLUSÃO

A matriz de controle demonstra:

✅ **Rastreabilidade RF → Deploy**
✅ **Validação em cada etapa**
✅ **Decisões formais registradas**
✅ **Evidências preservadas**
✅ **Conformidade auditável**

---

**FIM DO DOCUMENTO**
