# CONTRATO DE EXECUÇÃO – DEPLOY

**Versão:** 1.0
**Data de criação:** 2025-12-26
**Tipo de execução:** DECISÓRIA
**Autoridade:** DevOps / Release Manager

---

## NATUREZA DESTE CONTRATO

Este é um contrato de **EXECUÇÃO DECISÓRIA**.

Ele define as regras para executar deploy governado por contrato.

Deploy é uma operação crítica que:
- Altera ambiente produtivo
- Impacta usuários finais
- Requer rastreabilidade completa
- Requer aprovação formal

---

## FONTE DA VERDADE

A **ÚNICA fonte da verdade** é o arquivo:

```
contracts/EXECUTION-MANIFEST.md
```

Este contrato NÃO pode ser executado sem:
- Aprovação registrada no manifesto (transição TESTES → DEPLOY)
- STATUS.yaml com `contrato_ativo: CONTRATO-EXECUCAO-DEPLOY`

---

## PRÉ-REQUISITOS OBRIGATÓRIOS (BLOQUEANTES)

Para que este contrato seja ativado, DEVEM existir:

### 1. Transição Aprovada

No EXECUTION-MANIFEST, DEVE existir uma execução de transição com:

- RF identificado
- Contrato: `CONTRATO-TRANSICAO-TESTES-PARA-DEPLOY`
- Bloco `DECISAO FORMAL` com:
  ```yaml
  decision:
    resultado: APROVADO
    autoridade: DevOps-Agent
    contrato: CONTRATO-TRANSICAO-TESTES-PARA-DEPLOY
  ```

### 2. STATUS.yaml Atual

O STATUS.yaml do RF DEVE ter:

```yaml
governanca:
  contrato_ativo: CONTRATO-EXECUCAO-DEPLOY

devops:
  board_column: "Pronto para Deploy"
```

### 3. Testes Aprovados

O histórico de execuções DEVE mostrar:

- Testes backend: PASS
- Testes frontend: PASS (se aplicável)
- Testes E2E: PASS
- Testes segurança: PASS

### 4. Ambiente de Destino Validado

- Azure válido e acessível
- Credenciais configuradas (`az login`)
- Pipeline configurado
- Rollback plan disponível

---

## REGRA DE NEGAÇÃO AUTOMÁTICA

Se QUALQUER pré-requisito falhar:

➡️ O deploy DEVE ser **NEGADO**
➡️ O agente DEVE **PARAR**
➡️ O agente DEVE **DOCUMENTAR** o motivo da negação
➡️ Nenhuma ação parcial pode ser executada
➡️ Rollback NÃO deve ser necessário (porque deploy não iniciou)

---

## ESCOPO PERMITIDO

Durante a execução deste contrato, o agente PODE:

### 1. Build

- Executar build do backend (.NET)
- Executar build do frontend (Angular)
- Validar que builds passaram sem erros
- Gerar artefatos (binários, dist/)

### 2. Deploy

- Executar deploy conforme pipeline Azure
- Atualizar App Service (backend)
- Atualizar Static Web App (frontend)
- Executar migrations (se aplicável)
- Registrar versão deployada

### 3. Smoke Tests Pós-Deploy

- Validar que aplicação iniciou
- Validar que endpoints respondem (HTTP 200)
- Validar que autenticação funciona
- Validar que banco de dados está acessível

### 4. Geração de Evidências

- Hash do commit deployado
- Timestamp do deploy
- Versão do artefato
- Ambiente de destino (HOM / PRD)
- Resultado dos smoke tests

---

## PROIBIÇÕES ABSOLUTAS

Durante a execução deste contrato, é **PROIBIDO**:

- ❌ Alterar código durante o deploy
- ❌ Corrigir bugs "on the fly"
- ❌ Modificar configurações não documentadas
- ❌ Pular validações
- ❌ Deploy sem registro no manifesto
- ❌ Deploy manual "para testar rapidamente"
- ❌ Alterar contratos anteriores
- ❌ Executar ações sem rastreabilidade

---

## PROCESSO DE DEPLOY

### Passo 1: Validação de Pré-Requisitos

- Ler EXECUTION-MANIFEST
- Validar transição aprovada
- Validar STATUS.yaml
- Validar ambiente de destino

### Passo 2: Build

- Executar `dotnet build` (backend)
- Executar `npm run build` (frontend)
- Validar que não há erros

### Passo 3: Deploy

- Executar pipeline Azure
- Registrar hash do commit
- Registrar timestamp
- Registrar versão

### Passo 4: Smoke Tests

- Validar inicialização
- Validar endpoints críticos
- Validar autenticação
- **SE FALHAR:** Executar ROLLBACK AUTOMÁTICO

### Passo 5: Registro no Manifesto

- Registrar execução de deploy
- Registrar decisão (APROVADO / REPROVADO)
- Registrar evidências

### Passo 6: Atualização de STATUS.yaml

- Atualizar `devops.last_deploy`
- Atualizar `devops.deployed_version`
- Atualizar `devops.deployed_environment`
- Atualizar `devops.board_column` para "Deployed"

---

## SMOKE TESTS OBRIGATÓRIOS

Após deploy, DEVEM ser executados (mínimo):

### Backend
```bash
curl -X GET https://<backend-url>/health
# Esperado: HTTP 200
```

### Frontend
```bash
curl -X GET https://<frontend-url>/
# Esperado: HTTP 200
```

### Autenticação
```bash
curl -X POST https://<backend-url>/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"test"}'
# Esperado: HTTP 200 ou 401 (mas NÃO 500)
```

Se QUALQUER smoke test falhar:
➡️ Executar **ROLLBACK AUTOMÁTICO**

---

## ROLLBACK AUTOMÁTICO

Se smoke tests falharem, o agente DEVE:

1. Executar `CONTRATO-ROLLBACK`
2. Reverter para versão anterior
3. Registrar falha no EXECUTION-MANIFEST
4. Atualizar STATUS.yaml com `deploy_failed: true`
5. NÃO permitir novos deploys até correção

---

## SAÍDAS OBRIGATÓRIAS

Ao final da execução, DEVEM existir:

### 1. Registro no EXECUTION-MANIFEST

```markdown
# EXECUCAO: <ID_UNICO>

## TIPO DE EXECUCAO

- Tipo: DECISORIA

## CONTRATO ATIVO

- Contrato: CONTRATO-EXECUCAO-DEPLOY
- RF: RFXXX
- Data: YYYY-MM-DD HH:MM:SS
- Executor: DevOps Agent

## DEPLOY EXECUTADO

- Commit Hash: <hash>
- Versão: <versao>
- Ambiente: HOM | PRD
- Backend URL: <url>
- Frontend URL: <url>

## SMOKE TESTS

- [x] Backend health: PASS
- [x] Frontend acessível: PASS
- [x] Autenticação: PASS

## DECISAO FORMAL

decision:
  resultado: APROVADO | REPROVADO
  autoridade: DevOps-Agent
  contrato: CONTRATO-EXECUCAO-DEPLOY
```

### 2. STATUS.yaml Atualizado

```yaml
devops:
  last_deploy: "2025-12-26 14:30:00"
  deployed_version: "1.2.3"
  deployed_environment: "HOM" # ou "PRD"
  deployed_commit: "abc123def456"
  board_column: "Deployed"
```

### 3. Evidências Anexadas

- Screenshot de smoke tests
- Logs de deploy
- Hash do commit
- Timestamp do deploy

---

## REGRA DE AUDITORIA

Este deploy é auditável e DEVE ser rastreável:

- O quê foi deployado? → Hash do commit
- Quando foi deployado? → Timestamp no manifesto
- Onde foi deployado? → Ambiente (HOM/PRD)
- Quem autorizou? → Decisão de transição no manifesto
- Como validar? → Smoke tests registrados
- Como reverter? → CONTRATO-ROLLBACK

---

## AUTOMAÇÃO

Este contrato DEVE ser executado pelo script:

```bash
python tools/devops-sync/execute_deploy.py RFXXX HOM|PRD
```

O script DEVE:
- Validar todos os pré-requisitos
- NEGAR se qualquer regra falhar
- Executar deploy conforme processo definido
- Executar smoke tests
- Rollback automático se falhar
- Registrar no EXECUTION-MANIFEST

---

## AMBIENTES PERMITIDOS

Este contrato pode ser executado em:

- **HOM (Homologação)**: Ambiente de validação
- **PRD (Produção)**: Ambiente produtivo

Para PRD, regras adicionais:
- Aprovação de Release Manager obrigatória
- Deploy window definido
- Rollback plan validado
- Comunicação prévia enviada

---

## REGRA FINAL

**Manifesto decide.**
**Contrato autoriza.**
**Script executa.**
**Smoke tests validam.**
**Rollback protege.**

Nenhuma exceção manual é permitida.
Nenhum deploy fora de contrato é autorizado.
Todo deploy DEVE ser auditável.

---

## VIOLAÇÃO DESTE CONTRATO

Se qualquer regra for violada:

➡️ O deploy é considerado **INVÁLIDO**
➡️ Rollback DEVE ser executado
➡️ O manifesto DEVE registrar a violação
➡️ Investigação formal DEVE ser iniciada
➡️ Acesso ao ambiente DEVE ser revisado

---

**FIM DO CONTRATO**
