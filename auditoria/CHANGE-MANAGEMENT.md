# CHANGE MANAGEMENT – GESTÃO DE MUDANÇAS

**Versão:** 1.0
**Data de criação:** 2025-12-26
**Propósito:** Documentação do processo de gestão de mudanças para auditoria ISO / Compliance

---

## VISÃO GERAL

Este documento define o processo formal de gestão de mudanças do sistema IControlIT, demonstrando controle total sobre alterações em código, configuração e infraestrutura.

---

## PRINCÍPIO FUNDAMENTAL

**Toda mudança DEVE ser:**
- Planejada
- Autorizada
- Testada
- Documentada
- Reversível

**Nenhuma mudança pode ocorrer fora do processo formal.**

---

## TIPOS DE MUDANÇA

### 1. MUDANÇA PLANEJADA (Normal)

**Definição:**
- Nova funcionalidade (RF novo)
- Evolução de funcionalidade existente
- Refatoração planejada

**Processo:**
```
Documentação
  → Desenvolvimento Backend
    → Validação Tester-Backend
      → Desenvolvimento Frontend
        → Testes Completos
          → Deploy HOM
            → Deploy PRD
```

**Tempo estimado:** Semanas / Meses

**Autorização:** Product Owner + Tester-Backend + QA

---

### 2. MUDANÇA DE EMERGÊNCIA (Hotfix)

**Definição:**
- Falha crítica em produção
- Vulnerabilidade de segurança
- Perda de dados

**Processo:**
```
Identificação do Problema
  → Rollback (se possível)
    → Correção em DEV
      → Testes de Regressão
        → Deploy Emergencial
```

**Tempo estimado:** Horas

**Autorização:** Release Manager

**IMPORTANTE:** Mesmo hotfix DEVE seguir contratos
- CONTRATO-HOTFIX-PRODUCAO
- Registro obrigatório no EXECUTION-MANIFEST
- Testes mínimos obrigatórios

---

### 3. MUDANÇA PADRÃO (Repetitiva)

**Definição:**
- Atualização de dependências
- Renovação de certificados
- Atualização de configurações documentadas

**Processo:**
```
Checklist Padrão
  → Validação Automática
    → Deploy
```

**Tempo estimado:** Minutos / Horas

**Autorização:** DevOps Agent (seguindo checklist aprovado)

---

## PROCESSO DE MUDANÇA PLANEJADA

### Etapa 1: REQUISIÇÃO DE MUDANÇA

**Responsável:** Product Owner / Stakeholder

**Artefato:** Requisito Funcional (RF)

**Validação:**
- RF possui 5 seções obrigatórias
- UC possui 5 casos de uso
- MD possui DDL completo
- WF possui wireframes

**Aprovação:** Arquiteto / Tech Lead

---

### Etapa 2: ANÁLISE DE IMPACTO

**Responsável:** Arquiteto / Tech Lead

**Análise:**
- Impacto em outros RFs
- Dependências de dados
- Impacto em performance
- Riscos de segurança

**Saída:** Documento de análise de impacto

**Decisão:** Aprovar / Rejeitar / Ajustar

---

### Etapa 3: DESENVOLVIMENTO BACKEND

**Responsável:** Developer Agent

**Contrato:** CONTRATO-EXECUCAO-BACKEND

**Atividades:**
- Implementar código backend
- Criar seeds de dados
- Configurar permissões
- Executar testes unitários

**Critério de Pronto:**
- Build sem erros
- Testes unitários passando
- Seeds configurados
- Permissões mapeadas

**Registro:** EXECUTION-MANIFEST

---

### Etapa 4: VALIDAÇÃO DE CONTRATO BACKEND

**Responsável:** Tester-Backend Agent

**Contrato:** CONTRATO-EXECUCAO-TESTER-BACKEND

**Atividades:**
- Validar que backend respeita contrato
- Testar violações de contrato
- Validar rejeição de payloads inválidos
- Gerar matriz de violação

**Critério de Aprovação:**
- Backend rejeita TODAS as violações
- Erros são estruturados
- Contrato é respeitado 100%

**Decisão:** APROVADO / REPROVADO

**Registro:** EXECUTION-MANIFEST com decisão formal

---

### Etapa 5: DESENVOLVIMENTO FRONTEND

**Responsável:** Developer Agent

**Contrato:** CONTRATO-EXECUCAO-FRONTEND

**Pré-requisito:** Backend aprovado e mergeado em `dev`

**Atividades:**
- Implementar componentes Angular
- Implementar serviços e rotas
- Integrar com backend
- Executar testes unitários

**Critério de Pronto:**
- Build sem erros
- Testes unitários passando
- Integração com backend funcionando

**Registro:** EXECUTION-MANIFEST

---

### Etapa 6: TESTES COMPLETOS

**Responsável:** QA Agent / Tester

**Contrato:** CONTRATO-EXECUCAO-TESTES

**Atividades:**
- Testes backend (unitários, integração, contrato)
- Testes frontend (unitários, componentes)
- Testes E2E (Playwright)
- Testes segurança (SQL Injection, XSS, CSRF)

**Critério de Aprovação:**
- Taxa de aprovação = **100%**
- Nenhum teste crítico falhou
- Evidências geradas

**Decisão:** APROVADO / REPROVADO

**Registro:** EXECUTION-MANIFEST com taxa de aprovação

---

### Etapa 7: TRANSIÇÃO PARA DEPLOY

**Responsável:** DevOps Agent

**Contrato:** CONTRATO-TRANSICAO-TESTES-PARA-DEPLOY

**Validação:**
- Testes aprovados (taxa 100%)
- EXECUTION-MANIFEST com decisão APROVADO
- STATUS.yaml atualizado

**Ação:**
- Atualizar `contrato_ativo` para CONTRATO-EXECUCAO-DEPLOY
- Atualizar `board_column` para "Pronto para Deploy"

**Registro:** EXECUTION-MANIFEST

---

### Etapa 8: DEPLOY HOMOLOGAÇÃO

**Responsável:** DevOps Agent

**Contrato:** CONTRATO-EXECUCAO-DEPLOY

**Ambiente:** HOM

**Atividades:**
- Build de produção
- Deploy em App Service (backend)
- Deploy em Static Web App (frontend)
- Smoke tests pós-deploy

**Critério de Sucesso:**
- Build sem erros
- Deploy sem erros
- Smoke tests PASS

**Falha:** Rollback automático

**Registro:** EXECUTION-MANIFEST com hash, versão, timestamp

---

### Etapa 9: VALIDAÇÃO EM HOMOLOGAÇÃO

**Responsável:** Product Owner / Stakeholder

**Atividades:**
- Validar funcionalidade em HOM
- Validar regras de negócio
- Validar UX

**Critério de Aprovação:**
- Funcionalidade conforme RF
- Nenhum bug crítico
- UX aceitável

**Decisão:** Aprovar para PRD / Rejeitar

---

### Etapa 10: DEPLOY PRODUÇÃO

**Responsável:** DevOps Agent

**Contrato:** CONTRATO-EXECUCAO-DEPLOY

**Ambiente:** PRD

**Autorização:** Release Manager

**Pré-requisitos:**
- Aprovação em HOM
- Janela de deploy definida
- Rollback plan validado
- Comunicação enviada

**Atividades:**
- Build de produção
- Deploy em App Service PRD
- Deploy em Static Web App PRD
- Smoke tests pós-deploy

**Critério de Sucesso:**
- Build sem erros
- Deploy sem erros
- Smoke tests PASS

**Falha:** Rollback automático

**Registro:** EXECUTION-MANIFEST com hash, versão, timestamp

---

### Etapa 11: VALIDAÇÃO PÓS-DEPLOY

**Responsável:** DevOps Agent

**Atividades:**
- Monitorar logs (primeiras 24h)
- Monitorar taxa de erro
- Monitorar performance

**Critério de Sucesso:**
- Taxa de erro < 1%
- Performance aceitável
- Nenhum incidente crítico

**Falha:** Considerar rollback

---

## APROVAÇÕES NECESSÁRIAS

### Mudança Planejada

| Etapa | Aprovador | Artefato |
|-------|-----------|----------|
| Documentação | Arquiteto | RF, UC, MD, WF |
| Backend | Tester-Backend | EXECUTION-MANIFEST (decisão APROVADO) |
| Testes | QA / Tester | EXECUTION-MANIFEST (taxa 100%) |
| Deploy HOM | DevOps Agent | EXECUTION-MANIFEST (smoke tests PASS) |
| Deploy PRD | Release Manager | Aprovação formal |

---

### Mudança de Emergência (Hotfix)

| Etapa | Aprovador | Artefato |
|-------|-----------|----------|
| Identificação | On-call Engineer | Incident Report |
| Correção | Senior Developer | Pull Request |
| Testes Mínimos | QA (on-call) | Resultados de testes |
| Deploy PRD | Release Manager | Aprovação verbal + registro |

---

### Mudança Padrão

| Etapa | Aprovador | Artefato |
|-------|-----------|----------|
| Execução | DevOps Agent | Checklist aprovado |

---

## PROIBIÇÕES ABSOLUTAS

### ❌ NUNCA É PERMITIDO:

1. **Deploy manual em PRD**
   - Todo deploy DEVE seguir contrato
   - Todo deploy DEVE ser registrado

2. **Alteração de código em produção**
   - Código DEVE ser alterado em DEV
   - Código DEVE passar por pipeline completo

3. **Hotfix sem registro**
   - Mesmo hotfix emergencial DEVE ser registrado
   - CONTRATO-HOTFIX-PRODUCAO DEVE ser seguido

4. **Pular testes**
   - Todos os testes DEVEM ser executados
   - Taxa de aprovação DEVE ser 100%

5. **Deploy sem rollback plan**
   - Versão anterior DEVE ser identificável
   - Rollback DEVE ser possível

6. **Mudança não documentada**
   - Todo deploy DEVE estar no EXECUTION-MANIFEST
   - Todo deploy DEVE atualizar STATUS.yaml

---

## ROLLBACK

### Gatilhos para Rollback

1. **Automático:**
   - Smoke tests falharam após deploy
   - Taxa de erro > 5%
   - Downtime > 30 segundos

2. **Manual:**
   - Decisão de negócio (Product Owner)
   - Bug crítico descoberto pós-deploy
   - Funcionalidade causa impacto negativo

---

### Processo de Rollback

```
Identificar Gatilho
  → Validar Manifesto do Deploy Original
    → Identificar Versão Anterior
      → Executar Rollback (via contrato)
        → Smoke Tests Pós-Rollback
          → Registrar no Manifesto
```

**Contrato:** CONTRATO-ROLLBACK

**Registro:** EXECUTION-MANIFEST com motivo e versão revertida

---

## COMUNICAÇÃO DE MUDANÇAS

### Deploy em HOM

**Comunicar:**
- Equipe de desenvolvimento
- QA

**Canal:** Slack / Teams

**Timing:** Após deploy

---

### Deploy em PRD

**Comunicar:**
- Equipe de desenvolvimento
- QA
- Product Owner
- Suporte
- Usuários (se mudança significativa)

**Canal:** E-mail + Slack / Teams

**Timing:** 24h antes (planejado) / Imediatamente (emergencial)

**Conteúdo:**
- O que foi alterado (RF)
- Quando foi deployado
- O que esperar (mudanças visíveis)
- Como reportar problemas

---

### Rollback em PRD

**Comunicar:**
- Todos os stakeholders
- Equipe técnica
- Suporte
- Usuários

**Canal:** E-mail + Slack / Teams + SMS (se crítico)

**Timing:** Imediatamente

**Conteúdo:**
- Motivo do rollback
- Versão revertida
- Impacto esperado
- Próximos passos

---

## AUDITORIA DE MUDANÇAS

### Relatório Mensal de Mudanças

**Conteúdo:**
- Total de deploys em HOM
- Total de deploys em PRD
- Total de rollbacks
- Taxa de sucesso
- Tempo médio de deploy
- RFs em produção

**Destinatários:**
- CTO
- Release Manager
- Auditoria (se aplicável)

---

### Evidências Preservadas

Para cada mudança, preservar:

1. **EXECUTION-MANIFEST**
   - Decisões formais
   - Timestamps
   - Autorizações

2. **STATUS.yaml**
   - Estado antes
   - Estado depois

3. **Logs de Deploy**
   - Build logs
   - Deploy logs
   - Smoke tests logs

4. **Evidências de Testes**
   - Resultados de testes
   - Screenshots E2E
   - Relatórios de cobertura

---

## CONFORMIDADE ISO

Este processo de gestão de mudanças atende:

### ISO 27001
- **A.12.1.2** – Gestão de mudanças

### ISO 9001
- **8.5.6** – Controle de mudanças

### SOC 2
- **CC8.1** – Gestão de mudanças

---

## CONCLUSÃO

Este processo de gestão de mudanças garante:

✅ **Toda mudança é planejada**
✅ **Toda mudança é autorizada**
✅ **Toda mudança é testada**
✅ **Toda mudança é documentada**
✅ **Toda mudança é reversível**

Nenhuma exceção é permitida.

---

**FIM DO DOCUMENTO**
