# CONTRATO DE EXECUÇÃO – TESTES

**Versão:** 1.0
**Data de criação:** 2025-12-26
**Tipo de execução:** OPERACIONAL
**Autoridade:** QA / Tester

---

## NATUREZA DESTE CONTRATO

Este é um contrato de **EXECUÇÃO OPERACIONAL**.

Ele define a execução formal de testes após backend validado e aprovado por contrato.

Testes NÃO aprovam código.
Testes aprovam **CONTRATOS EM EXECUÇÃO**.

---

## FONTE DA VERDADE

A **ÚNICA fonte da verdade** é o arquivo:

```
contracts/EXECUTION-MANIFEST.md
```

Este contrato NÃO pode ser executado sem:
- Backend aprovado pelo Tester-Backend
- Decisão APROVADA registrada no manifesto
- STATUS.yaml com `contrato_ativo: CONTRATO-EXECUCAO-TESTES`

---

## PRÉ-REQUISITOS OBRIGATÓRIOS (BLOQUEANTES)

Para que este contrato seja ativado, DEVEM existir:

### 1. Backend Aprovado pelo Tester-Backend

No EXECUTION-MANIFEST, DEVE existir uma execução com:

- RF identificado
- Contrato: `CONTRATO-EXECUCAO-TESTER-BACKEND` ou `CONTRATO-TRANSICAO-BACKEND-PARA-TESTES`
- Bloco `DECISAO FORMAL` com:
  ```yaml
  decision:
    resultado: APROVADO
    autoridade: Tester-Backend
    contrato: CONTRATO-EXECUCAO-TESTER-BACKEND
  ```

### 2. STATUS.yaml Atual

O STATUS.yaml do RF DEVE ter:

```yaml
governanca:
  contrato_ativo: CONTRATO-EXECUCAO-TESTES
```

### 3. Documentação de Testes Disponível

DEVEM existir os arquivos:

- `rf/[FASE]/[EPIC]/RFXXX/MT-RFXXX.yaml` (Massa de Teste)
- `rf/[FASE]/[EPIC]/RFXXX/TC-RFXXX.yaml` (Casos de Teste)
- STATUS.yaml com `documentacao.mt = true`
- STATUS.yaml com `documentacao.tc = true`

---

## REGRA DE NEGAÇÃO AUTOMÁTICA

Se QUALQUER pré-requisito falhar:

➡️ A execução DEVE ser **NEGADA**
➡️ O agente DEVE **PARAR**
➡️ O agente DEVE **DOCUMENTAR** o motivo da negação
➡️ Nenhuma ação parcial pode ser executada

---

## ESCOPO PERMITIDO

Durante a execução deste contrato, o agente PODE:

### 1. Testes de Backend

- Executar testes unitários (.NET)
- Executar testes de integração
- Executar testes de contrato
- Executar testes de violação
- Validar que backend rejeita payloads inválidos

### 2. Testes de Frontend (se aplicável)

- Executar testes unitários (Angular)
- Executar testes de componentes
- Executar testes de serviços
- Validar formulários e validações

### 3. Testes E2E

- Executar testes Playwright
- Validar fluxos completos de usuário
- Validar integrações frontend ↔ backend
- Validar CRUD completo

### 4. Testes de Segurança

- Validar proteção contra SQL Injection
- Validar proteção contra XSS
- Validar proteção contra CSRF
- Validar autenticação e autorização
- Validar multi-tenancy

### 5. Geração de Evidências

- Screenshots de testes E2E
- Logs de execução
- Relatório de cobertura
- Taxa de aprovação
- Casos de falha (se houver)

---

## PROIBIÇÕES ABSOLUTAS

Durante a execução deste contrato, é **PROIBIDO**:

- ❌ Alterar código de produção
- ❌ Corrigir backend
- ❌ Ajustar contrato backend
- ❌ Modificar testes para fazer passar
- ❌ Pular testes que falharam
- ❌ Executar apenas subset de testes
- ❌ Marcar como APROVADO se houver falhas
- ❌ **ASSUMIR que backend ou frontend estão rodando** (SEMPRE INICIE)

---

## INSTRUÇÕES PRÁTICAS PARA O AGENTE

**REGRA DE OURO:** NUNCA assuma que as aplicações estão rodando. SEMPRE inicie backend e frontend.

### PASSO 0: LIMPEZA DE AMBIENTE (OBRIGATÓRIO - EXECUTAR PRIMEIRO)

**ANTES DE QUALQUER COISA**, matar processos que podem estar rodando e bloqueando arquivos:

```bash
# Windows (PowerShell)
taskkill /F /IM IControlIT.API.Web.exe 2>$null
taskkill /F /IM ng.exe 2>$null
taskkill /F /IM node.exe 2>$null

# Aguardar liberação de locks do sistema operacional
Start-Sleep -Seconds 5
```

**Verificar limpeza:**
```bash
# Deve retornar vazio (nenhum processo)
tasklist | findstr "IControlIT.API.Web"
tasklist | findstr "ng.exe"
```

**Se processos ainda existirem:**
- ❌ BLOQUEIO TOTAL
- Reportar ao usuário que processos não puderam ser mortos
- NÃO prosseguir com testes

---

### Comandos de Inicialização (Copy-Paste Ready)

**1. Build Backend e Frontend:**
```bash
# Backend
cd backend/IControlIT.API && dotnet build --no-incremental

# Frontend
cd frontend && npm run build
```

**2. Aplicar Seeds:**
```bash
cd backend/IControlIT.API && dotnet ef database update
```

**3. Iniciar Backend (Background):**
```bash
cd backend/IControlIT.API && dotnet run &
```

**Salvar Task ID:** O comando acima retorna um task ID (exemplo: `b8db6a0`). Guarde para monitorar ou matar depois.

**4. Iniciar Frontend (Background):**
```bash
cd frontend && npm start &
```

**Salvar Task ID:** O comando acima retorna um task ID (exemplo: `b6abe9e`). Guarde para monitorar ou matar depois.

### Validação de Health (OBRIGATÓRIO)

**Aguardar Backend Pronto (Timeout 60s):**
```bash
# Verificar se http://localhost:5000/health responde 200
for i in {1..60}; do
  curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/health | grep -q "200" && echo "Backend pronto!" && break
  sleep 1
done
```

**Aguardar Frontend Pronto (Timeout 120s):**
```bash
# Verificar se http://localhost:4200 responde
for i in {1..120}; do
  curl -s -o /dev/null -w "%{http_code}" http://localhost:4200 | grep -q "200" && echo "Frontend pronto!" && break
  sleep 1
done
```

### Validação Final Antes de Testes

**Checklist pré-testes:**
```bash
# 1. Backend respondendo?
curl -f http://localhost:5000/health && echo "✅ Backend OK" || echo "❌ Backend FALHOU"

# 2. Frontend respondendo?
curl -f http://localhost:4200 && echo "✅ Frontend OK" || echo "❌ Frontend FALHOU"
```

**Se AMBOS retornarem "OK":** Prosseguir com testes
**Se QUALQUER falhar:** REPROVAR com "ENVIRONMENT_SETUP_FAILED"

### Credenciais de Teste (OBRIGATÓRIO)

**REGRA CRÍTICA:** NUNCA assuma credenciais. SEMPRE use as credenciais definidas nos seeds.

**Fonte de Verdade:** Os seeds do backend (`dotnet ef database update`) criam usuários de teste.

**Credenciais Padrão (Seeds):**

| Perfil | Email | Senha | Descrição |
|--------|-------|-------|-----------|
| **Super Admin** | `anderson@chipak.com.br` | `Vi696206@` | Super administrador (permissões completas) |
| **Admin Teste** | `admin@teste.com` | `Test@123` | Administrador de testes |
| **Gerente Teste** | `gerente@teste.com` | `Test@123` | Gerente com permissões intermediárias |
| **Usuário Teste** | `usuario@teste.com` | `Test@123` | Usuário comum para testes |
| **Visualizador** | `visualizador@teste.com` | `Test@123` | Usuário com permissões de visualização |
| **Sem Permissão** | `sempermissao@teste.com` | `Test@123` | Usuário sem permissões (para testes 403) |

**Como Obter Credenciais Corretas:**

1. **Ler arquivo de seeds:** `D:\IC2\backend\IControlIT.API/src/Infrastructure/Data/ApplicationDbContextSeed.cs`
2. **Verificar STATUS.yaml:** Campo `testes.credenciais_padrao` (se existir)
3. **Ler MT (Massa de Teste):** Campo `contexto.autenticacao` em cada MT

**Exemplo de uso em Playwright:**
```typescript
// CORRETO: Usar credenciais dos seeds (admin@teste.com)
await page.goto('http://localhost:4200/sign-in');
await page.fill('[data-test="email"]', 'admin@teste.com');
await page.fill('[data-test="password"]', 'Test@123');
await page.click('[data-test="sign-in-button"]');

// Para testes de autorização (403), usar sempermissao@teste.com
await page.fill('[data-test="email"]', 'sempermissao@teste.com');
await page.fill('[data-test="password"]', 'Test@123');
```

**PROIBIDO:**
- ❌ Assumir credenciais (`admin@admin.com`, `password123`, etc.)
- ❌ Usar credenciais hardcoded sem validar nos seeds
- ❌ Inventar credenciais sem verificar banco de dados
- ❌ Ignorar campo `contexto.autenticacao` da MT

**Se credenciais falharem (401 Unauthorized):**
1. Verificar se seeds foram aplicados: `dotnet ef database update`
2. Ler arquivo de seeds para confirmar credenciais corretas
3. Verificar MT correspondente (campo `contexto.autenticacao`)
4. Se ainda falhar, REPROVAR com "CREDENTIALS_MISMATCH"

### Troubleshooting

**Problema 1: CONNECTION_REFUSED no frontend (porta 4200)**
- **Causa:** Frontend não foi iniciado
- **Solução:** Execute `cd frontend && npm start &` e aguarde até porta 4200 responder

**Problema 2: CONNECTION_REFUSED no backend (porta 5000)**
- **Causa:** Backend não foi iniciado
- **Solução:** Execute `cd backend/IControlIT.API && dotnet run &` e aguarde `/health` responder

**Problema 3: Build Failed**
- **Causa:** Código com erro de compilação
- **Solução:** NÃO prosseguir, REPROVAR com log detalhado do erro de build

**Problema 4: Timeout ao aguardar backend/frontend**
- **Causa:** Aplicação travou na inicialização
- **Solução:**
  1. Verificar logs: `D:\IC2\backend\IControlIT.API/logs/` ou `D:\IC2\frontend\logs/`
  2. Matar processos background
  3. REPROVAR com "STARTUP_TIMEOUT"

**Problema 5: Seeds não aplicados**
- **Causa:** Migration pendente ou banco corrompido
- **Solução:**
  1. Executar `cd backend/IControlIT.API && dotnet ef database update`
  2. Verificar se comando retornou exit code 0
  3. Se falhar, REPROVAR com log detalhado

### Workflow Completo (Passo a Passo)

```bash
# PASSO 1: Build (OBRIGATÓRIO)
cd backend/IControlIT.API && dotnet build --no-incremental || exit 1
cd frontend && npm run build || exit 1

# PASSO 2: Seeds (OBRIGATÓRIO)
cd backend/IControlIT.API && dotnet ef database update || exit 1

# PASSO 3: Iniciar Backend (Background)
cd backend/IControlIT.API && dotnet run &
# Salvar task ID retornado

# PASSO 4: Aguardar Backend (Polling 60s)
for i in {1..60}; do
  curl -s http://localhost:5000/health > /dev/null && break
  sleep 1
done

# PASSO 5: Validar Backend
curl -f http://localhost:5000/health || { echo "Backend FALHOU"; exit 1; }

# PASSO 6: Iniciar Frontend (Background)
cd frontend && npm start &
# Salvar task ID retornado

# PASSO 7: Aguardar Frontend (Polling 120s)
for i in {1..120}; do
  curl -s http://localhost:4200 > /dev/null && break
  sleep 1
done

# PASSO 8: Validar Frontend
curl -f http://localhost:4200 || { echo "Frontend FALHOU"; exit 1; }

# PASSO 9: SOMENTE AGORA executar testes
# Backend e frontend estão garantidamente rodando
npm run e2e  # ou dotnet test, etc
```

### Checklist Antes de Executar QUALQUER Teste

- [ ] Build backend concluído com sucesso
- [ ] Build frontend concluído com sucesso
- [ ] Seeds aplicados (dotnet ef database update)
- [ ] Backend iniciado (dotnet run &)
- [ ] Backend respondendo em http://localhost:5000/health (HTTP 200)
- [ ] Frontend iniciado (npm start &)
- [ ] Frontend respondendo em http://localhost:4200 (HTTP 200)
- [ ] SOMENTE AGORA: Executar testes

**Se QUALQUER item falhar:** PARAR, REPROVAR, DOCUMENTAR erro detalhado.

---

## PROCESSO DE EXECUÇÃO DE TESTES

### Passo 1: Validação de Pré-Requisitos

- Ler EXECUTION-MANIFEST
- Validar backend aprovado
- Validar STATUS.yaml
- Validar documentação de testes

### Passo 2: Setup de Ambiente (OBRIGATÓRIO - AUTOMÁTICO)

**REGRA CRÍTICA:** O agente DEVE SEMPRE iniciar backend e frontend ANTES de executar testes.

**❌ NÃO assumir que aplicação está rodando**
**✅ SEMPRE iniciar backend e frontend**

#### 2.1 Build Obrigatório (ANTES de tudo)

```bash
# Backend
cd backend/IControlIT.API
dotnet build --no-incremental

# Frontend
cd frontend
npm run build
```

**Se QUALQUER build falhar:**
- ❌ PARAR imediatamente
- ❌ REPROVAR com erro de build
- ❌ NÃO prosseguir com testes
- ✅ Gerar log detalhado do erro

#### 2.2 Aplicar Seeds Funcionais

```bash
cd backend/IControlIT.API
dotnet ef database update
```

**Validar seeds aplicados:**
- ✅ Banco tem empresas (Clientes)
- ✅ Banco tem perfis (Roles)
- ✅ Banco tem permissões (Permissions)
- ✅ Banco tem usuários de teste

#### 2.3 Iniciar Backend (Background - OBRIGATÓRIO)

```bash
cd backend/IControlIT.API
dotnet run &  # Background process
```

**Aguardar backend pronto (polling):**
```bash
# Verificar porta 5000 respondendo
max_attempts=60
for i in $(seq 1 $max_attempts); do
  curl -s http://localhost:5000/health > /dev/null && break
  sleep 1
done
```

**Se timeout (60 segundos):**
- ❌ REPROVAR (backend não inicializou)
- ❌ Verificar logs: `D:\IC2\backend\IControlIT.API/logs/`
- ❌ Gerar relatório de falha

#### 2.4 Iniciar Frontend (Background - OBRIGATÓRIO)

```bash
cd frontend
npm start &  # Background process
```

**Aguardar frontend pronto (polling):**
```bash
# Verificar porta 4200 respondendo
max_attempts=120  # Angular leva mais tempo
for i in $(seq 1 $max_attempts); do
  curl -s http://localhost:4200 > /dev/null && break
  sleep 1
done
```

**Se timeout (120 segundos):**
- ❌ REPROVAR (frontend não inicializou)
- ❌ Verificar logs: `D:\IC2\frontend\logs/`
- ❌ Gerar relatório de falha

#### 2.5 Validação de Ambiente (ANTES de testes)

```bash
# Validar backend
curl -f http://localhost:5000/health || exit 1

# Validar frontend
curl -f http://localhost:4200 || exit 1
```

**Checklist de validação:**
- ✅ Backend rodando (http://localhost:5000/health retorna 200)
- ✅ Frontend rodando (http://localhost:4200 retorna 200)
- ✅ Banco de dados acessível
- ✅ Seeds aplicados

**Se QUALQUER validação falhar:**
- ❌ PARAR testes
- ❌ REPROVAR com "ENVIRONMENT_SETUP_FAILED"
- ❌ Gerar log detalhado
- ❌ Matar processos backend e frontend

---

### Passo 3: Execução de Testes Backend

**SOMENTE executar se ambiente estiver PRONTO (Passo 2 aprovado)**

- Executar testes unitários (`dotnet test`)
- Executar testes de integração
- Executar testes de contrato
- Registrar resultado (PASS / FAIL)

### Passo 4: Execução de Testes Frontend (se aplicável)

**SOMENTE executar se ambiente estiver PRONTO (Passo 2 aprovado)**

- Executar testes unitários (`npm run test`)
- Executar testes de componentes
- Registrar resultado (PASS / FAIL)

### Passo 5: Execução de Testes E2E

**PRÉ-REQUISITO:** Backend E Frontend DEVEM estar rodando (Passo 2 validado)

- Executar testes Playwright (`npm run e2e`)
- Validar fluxos completos
- Registrar resultado (PASS / FAIL)
- Capturar screenshots

### Passo 5: Execução de Testes de Segurança

- Executar testes de SQL Injection
- Executar testes de XSS
- Executar testes de CSRF
- Validar autenticação
- Registrar resultado (PASS / FAIL)

### Passo 6: Consolidação de Resultados

- Calcular taxa de aprovação
- Identificar falhas críticas
- Gerar relatório consolidado

### Passo 7: Decisão

- **SE taxa de aprovação = 100%:**
  - Decisão: APROVADO
  - Próximo passo: CONTRATO-TRANSICAO-TESTES-PARA-DEPLOY

- **SE taxa de aprovação < 100%:**
  - Decisão: REPROVADO
  - Próximo passo: Corrigir falhas e re-executar

### Passo 8: Registro no Manifesto

- Registrar execução de testes
- Registrar taxa de aprovação
- Registrar decisão (APROVADO / REPROVADO)
- Registrar evidências

### Passo 9: Atualização de STATUS.yaml

- Atualizar `testes.backend`
- Atualizar `testes.frontend`
- Atualizar `testes.e2e`
- Atualizar `testes.seguranca`
- Atualizar `devops.board_column`

---

## CRITÉRIO DE APROVAÇÃO

Para que testes sejam considerados **APROVADOS**:

- ✅ Taxa de aprovação = **100%** (todos os testes passaram)
- ✅ Nenhum teste crítico falhou
- ✅ Evidências geradas
- ✅ Smoke tests passaram

Qualquer falha resulta em **REPROVADO**.

---

## SAÍDAS OBRIGATÓRIAS

Ao final da execução, DEVEM existir:

### 1. Registro no EXECUTION-MANIFEST

```markdown
# EXECUCAO: <ID_UNICO>

## TIPO DE EXECUCAO

- Tipo: OPERACIONAL

## CONTRATO ATIVO

- Contrato: CONTRATO-EXECUCAO-TESTES
- RF: RFXXX
- Data: YYYY-MM-DD HH:MM:SS
- Executor: QA Agent / Tester

## TESTES EXECUTADOS

### Backend
- Testes unitários: X PASS, Y FAIL
- Testes integração: X PASS, Y FAIL
- Testes contrato: X PASS, Y FAIL
- Taxa de aprovação: XX%

### Frontend
- Testes unitários: X PASS, Y FAIL
- Testes componentes: X PASS, Y FAIL
- Taxa de aprovação: XX%

### E2E
- Testes Playwright: X PASS, Y FAIL
- Taxa de aprovação: XX%

### Segurança
- SQL Injection: PASS | FAIL
- XSS: PASS | FAIL
- CSRF: PASS | FAIL
- Autenticação: PASS | FAIL
- Multi-tenancy: PASS | FAIL
- Taxa de aprovação: XX%

## RESULTADO CONSOLIDADO

- Taxa geral de aprovação: XX%
- Total de testes: X
- Testes aprovados: X
- Testes reprovados: X

## DECISAO FORMAL

decision:
  resultado: APROVADO | REPROVADO
  autoridade: QA | Tester
  contrato: CONTRATO-EXECUCAO-TESTES
  taxa_aprovacao: XX%
```

### 2. STATUS.yaml Atualizado

```yaml
testes:
  backend: pass | fail
  frontend: pass | fail
  e2e: pass | fail
  seguranca: pass | fail

devops:
  board_column: "Testes Aprovados" | "Testes Reprovados"
  last_sync: "2025-12-26 14:30:00"
```

### 3. Evidências Anexadas

- Screenshots de testes E2E
- Logs de execução
- Relatório HTML de testes
- Relatório de cobertura

### 4. Exportação Azure DevOps (OBRIGATÓRIO)

Após executar testes, o agente DEVE atualizar:

**`azure-test-cases-RF[XXX].csv`:**
- Coluna "State" atualizada conforme resultado
- Resultados de execução registrados

**STATUS.yaml:**
```yaml
testes:
  azure_devops:
    ultima_execucao_completa: "2026-01-02"
    taxa_aprovacao_geral: "100%"
    backend_pass: true
    frontend_pass: true
    e2e_pass: true
    seguranca_pass: true
```

---

## REGRA DE AUDITORIA

Execução de testes é auditável e DEVE ser rastreável:

- Quais testes foram executados? → Lista no manifesto
- Qual a taxa de aprovação? → Percentual no manifesto
- Quais testes falharam? → Lista de falhas
- Quem executou? → Autoridade no manifesto
- Quando executou? → Timestamp no manifesto
- Evidências disponíveis? → Links ou anexos

---

## AUTOMAÇÃO

Este contrato DEVE ser executado pelo agente de testes:

```bash
# Via agente Claude Code com subagent_type=qa-tester
Task(
  subagent_type="qa-tester",
  prompt="Executar testes conforme CONTRATO-EXECUCAO-TESTES para RF001"
)
```

Ou via script:

```bash
python tools/testing/execute_tests.py RFXXX
```

---

## REGRA FINAL

**Testes não aprovam código.**
**Testes aprovam CONTRATOS EM EXECUÇÃO**.

Nenhuma exceção manual é permitida.
Nenhum teste pode ser pulado.
Toda execução DEVE ser auditável.

Taxa de aprovação < 100% = REPROVADO.

---

## VIOLAÇÃO DESTE CONTRATO

Se qualquer regra for violada:

➡️ A execução é considerada **INVÁLIDA**
➡️ Resultado de testes NÃO pode ser usado
➡️ RF NÃO pode avançar para deploy
➡️ Investigação formal DEVE ser iniciada

---

**FIM DO CONTRATO**
