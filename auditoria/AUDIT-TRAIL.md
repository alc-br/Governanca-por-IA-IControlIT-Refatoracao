# AUDIT TRAIL – TRILHA DE AUDITORIA

**Versão:** 1.0
**Data de criação:** 2025-12-26
**Propósito:** Documentação para auditoria ISO / Compliance

---

## VISÃO GERAL

Este documento descreve a trilha de auditoria completa do sistema IControlIT, demonstrando rastreabilidade total de decisões e execuções através de governança por contratos.

---

## CADEIA DE DECISÃO

### Princípio Fundamental

**Toda execução deve ser rastreável do requisito até a produção.**

```
Requisito (RF)
  → Contrato de Execução
    → Manifesto de Execução
      → Decisão Formal
        → Mudança de Estado
          → Deploy
            → Evidências
```

---

## FLUXO COMPLETO DE CONTRATOS

### 1. FASE: DOCUMENTAÇÃO

**Entrada:**
- Requisito funcional (RF)
- Caso de uso (UC)
- Modelo de dados (MD)
- Wireframe (WF)

**Contratos Aplicáveis:**
- CONTRATO-DOCUMENTACAO-ESSENCIAL
- CONTRATO-DOCUMENTACAO-GOVERNADA
- CONTRATO-DOCUMENTACAO-GOVERNADA-TESTES

**Saídas Auditáveis:**
- RF completo (5 seções obrigatórias)
- 5 casos de uso (UC00-UC04)
- Modelo de dados com DDL
- 4 arquivos de casos de teste

**Evidências:**
- Arquivos em `rf/RFXXX/`
- STATUS.yaml com `documentacao: all True`

---

### 2. FASE: DESENVOLVIMENTO BACKEND

**Entrada:**
- Documentação aprovada
- RF, UC, MD validados

**Contratos Aplicáveis:**
- CONTRATO-EXECUCAO-BACKEND
- CONTRATO-REGULARIZACAO-BACKEND (se legado)
- CONTRATO-EXECUCAO-TESTER-BACKEND

**Saídas Auditáveis:**
- Código backend (.NET)
- Seeds de dados
- Permissões configuradas
- Testes unitários

**Evidências:**
- Commits em branch `feature/RFXXX-backend`
- EXECUTION-MANIFEST com decisão APROVADO
- STATUS.yaml com `desenvolvimento.backend.status: done`
- STATUS.yaml com `desenvolvimento.backend.contrato_validado: true`

---

### 3. FASE: DESENVOLVIMENTO FRONTEND

**Entrada:**
- Backend aprovado e mergeado em `dev`

**Contratos Aplicáveis:**
- CONTRATO-EXECUCAO-FRONTEND

**Saídas Auditáveis:**
- Código frontend (Angular)
- Componentes, serviços, rotas
- Testes unitários

**Evidências:**
- Commits em branch `feature/RFXXX-frontend`
- EXECUTION-MANIFEST com decisão APROVADO
- STATUS.yaml com `desenvolvimento.frontend.status: done`

---

### 4. FASE: TRANSIÇÃO PARA TESTES

**Entrada:**
- Backend validado (Tester-Backend)
- Frontend concluído (se aplicável)

**Contratos Aplicáveis:**
- CONTRATO-TRANSICAO-BACKEND-PARA-TESTES

**Saídas Auditáveis:**
- STATUS.yaml com `contrato_ativo: CONTRATO-EXECUCAO-TESTES`
- Board column: "Testes Pendentes"

**Evidências:**
- EXECUTION-MANIFEST com decisão APROVADO
- Timestamp de transição

---

### 5. FASE: EXECUÇÃO DE TESTES

**Entrada:**
- Código aprovado e pronto para testes
- Documentação de testes disponível

**Contratos Aplicáveis:**
- CONTRATO-EXECUCAO-TESTES

**Saídas Auditáveis:**
- Resultados de testes backend
- Resultados de testes frontend
- Resultados de testes E2E
- Resultados de testes segurança
- Taxa de aprovação: 100%

**Evidências:**
- EXECUTION-MANIFEST com taxa de aprovação
- Screenshots de testes E2E
- Logs de execução
- STATUS.yaml com `testes: all pass`

---

### 6. FASE: TRANSIÇÃO PARA DEPLOY

**Entrada:**
- Testes aprovados (taxa = 100%)

**Contratos Aplicáveis:**
- CONTRATO-TRANSICAO-TESTES-PARA-DEPLOY

**Saídas Auditáveis:**
- STATUS.yaml com `contrato_ativo: CONTRATO-EXECUCAO-DEPLOY`
- Board column: "Pronto para Deploy"

**Evidências:**
- EXECUTION-MANIFEST com decisão APROVADO
- Timestamp de transição
- Referência ao manifesto de testes aprovado

---

### 7. FASE: DEPLOY

**Entrada:**
- Aprovação formal para deploy

**Contratos Aplicáveis:**
- CONTRATO-EXECUCAO-DEPLOY

**Saídas Auditáveis:**
- Build executado
- Deploy em HOM ou PRD
- Smoke tests executados
- Versão deployada

**Evidências:**
- EXECUTION-MANIFEST com:
  - Hash do commit
  - Versão deployada
  - Ambiente (HOM/PRD)
  - Timestamp
  - Resultado de smoke tests
- STATUS.yaml com:
  - `devops.last_deploy`
  - `devops.deployed_version`
  - `devops.deployed_commit`

---

### 8. FASE: ROLLBACK (SE NECESSÁRIO)

**Entrada:**
- Falha de smoke test (automático)
- Decisão de negócio (manual)

**Contratos Aplicáveis:**
- CONTRATO-ROLLBACK

**Saídas Auditáveis:**
- Versão revertida
- Motivo do rollback
- Smoke tests pós-rollback

**Evidências:**
- EXECUTION-MANIFEST com:
  - Gatilho (automático/manual)
  - Motivo
  - Versão revertida
  - Autorização (se manual)
- STATUS.yaml com:
  - `devops.last_rollback`
  - `devops.rollback_reason`

---

## RASTREABILIDADE COMPLETA

Para QUALQUER mudança em produção, é possível rastrear:

### Pergunta 1: O QUE foi alterado?
**Resposta:**
- RF identificado no EXECUTION-MANIFEST
- Hash do commit no manifesto
- Versão no STATUS.yaml

### Pergunta 2: QUANDO foi alterado?
**Resposta:**
- Timestamp no EXECUTION-MANIFEST
- `last_deploy` no STATUS.yaml

### Pergunta 3: QUEM autorizou?
**Resposta:**
- Decisão formal no EXECUTION-MANIFEST
- Autoridade identificada (DevOps Agent, QA, Tester-Backend)

### Pergunta 4: POR QUE foi alterado?
**Resposta:**
- RF descreve o requisito
- Contrato ativo no EXECUTION-MANIFEST
- Decisão APROVADA rastreável

### Pergunta 5: COMO foi validado?
**Resposta:**
- Tester-Backend validou backend
- QA/Tester executou testes (taxa 100%)
- Smoke tests pós-deploy (PASS)

### Pergunta 6: COMO reverter?
**Resposta:**
- EXECUTION-MANIFEST identifica versão anterior
- CONTRATO-ROLLBACK define processo
- Script `apply_rollback.py` executa

---

## PAPÉIS E RESPONSABILIDADES

### 1. Developer Agent
**Responsabilidades:**
- Executar CONTRATO-EXECUCAO-BACKEND
- Executar CONTRATO-EXECUCAO-FRONTEND
- Registrar execução no EXECUTION-MANIFEST
- Atualizar STATUS.yaml

**NÃO pode:**
- Aprovar próprio código
- Pular validações
- Executar deploy

---

### 2. Tester-Backend Agent
**Responsabilidades:**
- Executar CONTRATO-EXECUCAO-TESTER-BACKEND
- Validar que backend respeita contrato
- Testar violações de contrato
- Decidir: APROVADO / REPROVADO

**NÃO pode:**
- Corrigir código
- Alterar contrato backend
- Executar deploy

---

### 3. QA Agent / Tester
**Responsabilidades:**
- Executar CONTRATO-EXECUCAO-TESTES
- Executar testes completos (backend, frontend, E2E, segurança)
- Decidir: APROVADO / REPROVADO
- Gerar evidências

**NÃO pode:**
- Alterar código
- Pular testes que falharam
- Aprovar com taxa < 100%

---

### 4. DevOps Agent
**Responsabilidades:**
- Executar CONTRATO-TRANSICAO-TESTES-PARA-DEPLOY
- Executar CONTRATO-EXECUCAO-DEPLOY
- Executar CONTRATO-ROLLBACK (automático)
- Atualizar STATUS.yaml
- Registrar no EXECUTION-MANIFEST

**NÃO pode:**
- Executar deploy sem aprovação
- Pular smoke tests
- Executar hotfix fora de contrato

---

### 5. Release Manager (Humano)
**Responsabilidades:**
- Autorizar deploy em PRD
- Autorizar rollback manual
- Validar janela de deploy
- Comunicar mudanças

**NÃO pode:**
- Executar deploy manual
- Alterar código em produção
- Pular validações

---

## FONTE DA VERDADE

### Único Ponto de Verdade

O arquivo `contracts/EXECUTION-MANIFEST.md` é a **ÚNICA fonte da verdade** para:

- Todas as execuções
- Todas as decisões
- Todas as transições

### STATUS.yaml É Reflexo

O arquivo `STATUS.yaml` de cada RF **REFLETE** o estado atual, mas:

- NÃO decide
- NÃO autoriza
- Apenas espelha decisões do EXECUTION-MANIFEST

---

## REGRAS DE AUDITORIA

### 1. Toda Execução Deve Ser Registrada

**Nenhuma execução** pode ocorrer sem registro no EXECUTION-MANIFEST.

**Violação:** Deploy sem manifesto = Deploy inválido

---

### 2. Toda Decisão Deve Ser Rastreável

Toda execução decisória DEVE ter bloco:

```yaml
decision:
  resultado: APROVADO | REPROVADO
  autoridade: <quem decidiu>
  contrato: <qual contrato>
```

---

### 3. Toda Mudança Deve Ser Reversível

- Deploy DEVE permitir rollback
- Rollback DEVE ser governado (CONTRATO-ROLLBACK)
- Versão anterior DEVE ser identificável

---

### 4. Toda Evidência Deve Ser Preservada

- Logs de execução
- Screenshots de testes
- Resultados de smoke tests
- Timestamps de deploy/rollback

---

## CONFORMIDADE ISO

Este sistema de governança por contratos atende aos seguintes requisitos ISO:

### ISO 27001 (Segurança da Informação)

- **A.12.1.2** – Gestão de mudanças
- **A.12.4.1** – Registro de eventos (logs)
- **A.12.4.3** – Logs de administrador
- **A.14.2.9** – Teste de aceite de sistemas

### ISO 9001 (Gestão de Qualidade)

- **7.1.5** – Recursos de monitoramento e medição
- **8.1** – Planejamento e controle operacional
- **8.5.6** – Controle de mudanças
- **9.1** – Monitoramento, medição, análise e avaliação

### SOC 2 (Service Organization Control)

- **CC6.1** – Segregação de funções
- **CC6.6** – Restrição lógica de acesso
- **CC7.2** – Detecção e correção de desvios
- **CC8.1** – Gestão de mudanças

---

## EVIDÊNCIAS PARA AUDITORIA EXTERNA

Para auditoria externa, fornecer:

1. **EXECUTION-MANIFEST.md completo**
   - Demonstra rastreabilidade total

2. **STATUS.yaml de todos os RFs em produção**
   - Demonstra estado atual validado

3. **Contratos ativos** (`contracts/`)
   - Demonstra governança formal

4. **Logs de deploy** (se disponíveis)
   - Demonstra execução conforme processo

5. **Este documento (AUDIT-TRAIL.md)**
   - Demonstra processo documentado

---

## CONCLUSÃO

Este sistema de governança por contratos garante:

✅ **Rastreabilidade total** – Do requisito à produção
✅ **Segregação de funções** – Nenhum agente aprova próprio trabalho
✅ **Decisões formais** – Toda mudança tem decisão registrada
✅ **Reversibilidade** – Rollback governado por contrato
✅ **Auditabilidade** – Evidências preservadas
✅ **Conformidade** – Atende ISO 27001, ISO 9001, SOC 2

---

**FIM DO DOCUMENTO**
