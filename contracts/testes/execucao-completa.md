# CONTRATO DE EXECUÇÃO COMPLETA DE TESTES

**Versão:** 1.0
**Data:** 2026-01-03
**Status:** Ativo
**Changelog v1.0:** Criação do contrato com auto-geração de specs E2E

---

## 📋 SUMÁRIO EXECUTIVO

### ⚡ O que este contrato faz

Este contrato **EXECUTA TODOS OS TESTES** de um RF automaticamente, incluindo:

- ✅ **Testes Backend**: Unitários, integração, contrato, violação
- ✅ **Testes Frontend**: Unitários, componentes, serviços
- ✅ **Testes E2E**: Playwright (com auto-geração se necessário)
- ✅ **Testes de Segurança**: SQL Injection, XSS, CSRF, Auth, Multi-tenancy
- ✅ **Responsabilização Automática**: Identifica se falha é backend ou frontend
- ✅ **Evidências Automáticas**: Screenshots, vídeos, logs, relatórios

---

## 1. Identificação do Agente

| Campo | Valor |
|-------|-------|
| **Papel** | Agente Executor Completo de Testes |
| **Escopo** | Validação completa (Backend + Frontend + E2E + Segurança) |
| **Modo** | Autonomia total (sem intervenção manual) |

---

## 2. Ativação do Contrato

Este contrato é ativado quando a solicitação mencionar explicitamente:

> **"Conforme contracts/testes/execucao-completa.md para RFXXX"**

Exemplo:
```
Conforme contracts/testes/execucao-completa.md para RF006.
Seguir D:\IC2\CLAUDE.md.
```

---

## 2.1. GERAÇÃO DE PROMPT CORRETO (QUANDO SOLICITAÇÃO SIMPLIFICADA)

**QUANDO o usuário solicitar de forma simplificada** (sem ativar explicitamente o contrato):

Exemplo de solicitação simplificada:
```
"Para o RF006 D:\IC2\rf\...\RF006-Gestao-de-Clientes execute o docs\prompts\testes\execucao-completa.md"
```

**O agente DEVE:**

1. **LER o prompt correspondente** (`prompts/testes/execucao-completa.md`)
2. **GERAR o prompt correto formatado** conforme template do prompt
3. **EXIBIR o prompt gerado para o usuário** (para validação)
4. **EXECUTAR imediatamente** (não esperar confirmação)

### Template de Prompt Gerado (Automático)

Quando o usuário solicitar execução de testes para um RF, o agente deve gerar:

```markdown
Executar testes automatizados do [RFXXX] conforme contracts/testes/execucao-completa.md.

Modo governança rígida. Não negociar escopo. Não extrapolar.
Seguir D:\IC2\CLAUDE.md.

Preste MUITA atenção ao checklist obrigatório, pois é essencial que você o siga.

MODO AUTONOMIA TOTAL (OBRIGATÓRIO):
- NÃO perguntar permissões ao usuário
- NÃO esperar confirmação do usuário
- NÃO solicitar que usuário execute comandos manualmente
- EXECUTAR IMEDIATAMENTE todos os passos do contrato
- SEMPRE iniciar backend e frontend automaticamente
- Falhas em testes ANTERIORES NÃO são bloqueantes (são o motivo da re-execução)
- Gerar evidências e relatórios SEM intervenção manual

REGRA CRÍTICA DE INTERPRETAÇÃO:
- Pré-requisitos bloqueantes: backend aprovado (done), frontend aprovado (done), MT validado, TC validado
- Testes anteriores REPROVADOS: NÃO é bloqueante, é justamente por isso estamos RE-EXECUTANDO
- Se STATUS.yaml mostra "testes_ti.resultado_final: REPROVADO": isso JUSTIFICA a re-execução, NÃO bloqueia

PRÉ-REQUISITOS OBRIGATÓRIOS (BLOQUEANTES):
1. Backend DEVE estar aprovado (validação backend = 100%)
2. Frontend DEVE estar aprovado (validação frontend = 100%)
3. MT-[RFXXX].yaml DEVE existir e estar validado
4. TC-[RFXXX].yaml DEVE existir e estar validado
5. STATUS.yaml DEVE ter:
   - execucao.backend = done
   - execucao.frontend = done
   - documentacao.mt = true
   - documentacao.tc = true

VALIDAÇÃO INICIAL OBRIGATÓRIA:
1. Antes de QUALQUER teste, execute:
   - dotnet build (backend)
   - npm run build (frontend)
2. Se QUALQUER build quebrar: PARAR, REPORTAR, BLOQUEAR
3. Somente prosseguir com testes se AMBOS os builds passarem

RESPONSABILIDADE DO AGENTE:
1. Validar pré-requisitos (backend/frontend aprovados, MT/TC validados)
2. Buildar backend e frontend
3. Aplicar seeds funcionais
4. Iniciar backend e frontend (usar python run.py se disponível)
5. Executar testes backend (dotnet test)
6. Executar testes frontend (npm run test)
7. VERIFICAR SE SPECS PLAYWRIGHT EXISTEM:
   - Se NÃO: executar geração automática (prompts/testes/geracao-e2e-playwright.md)
   - Se SIM: validar cobertura completa de TC-E2E
8. Executar testes E2E (npm run e2e)
9. Executar testes de segurança
10. Consolidar resultados
11. Atribuir responsabilidade em falhas
12. Gerar relatório consolidado
13. Gerar evidências (screenshots, logs)
14. Atualizar azure-test-cases-[RFXXX].csv (State conforme resultado)
15. Atualizar STATUS.yaml (incluindo testes.azure_devops)
16. Registrar decisão (APROVADO/REPROVADO)

CRITÉRIO DE APROVAÇÃO (0% OU 100%):
- ✅ APROVADO: Taxa de aprovação = 100% (TODOS os testes passaram)
- ❌ REPROVADO: Taxa de aprovação < 100% (QUALQUER teste falhou)

NÃO EXISTE APROVAÇÃO COM RESSALVAS.
```

### Regras de Geração

1. **Substituir `[RFXXX]` pelo RF correto** (ex: RF006)
2. **Copiar o template do prompt** (`prompts/testes/execucao-completa.md`)
3. **Exibir prompt completo** antes de executar
4. **Não esperar confirmação** (executar imediatamente)

### Exemplo Prático

**Solicitação do usuário:**
```
Para o RF006 execute o docs\prompts\testes\execucao-completa.md
```

**O que o agente FAZ:**

1. ✅ Lê `prompts/testes/execucao-completa.md`
2. ✅ Gera prompt substituindo `RFXXX` → `RF006`
3. ✅ Exibe: "Prompt gerado para RF006 (executando imediatamente):"
4. ✅ Exibe prompt completo formatado
5. ✅ Executa imediatamente FASE 1 → PASSO 1.1

**O que o agente NÃO FAZ:**

- ❌ Executar sem gerar/exibir prompt
- ❌ Pedir confirmação ao usuário
- ❌ Tentar executar sem ler o prompt primeiro

---

## 3. PRÉ-REQUISITOS OBRIGATÓRIOS (BLOQUEANTES)

O contrato TRAVA se qualquer condição falhar:

| Pré-requisito | Descrição | Bloqueante |
|---------------|-----------|------------|
| **Docker rodando** | `docker ps` deve responder (TestContainers dependency) | **Sim** |
| Backend aprovado | `STATUS.yaml`: `execucao.backend = done` | Sim |
| Frontend aprovado | `STATUS.yaml`: `execucao.frontend = done` | Sim |
| MT-RFXXX.yaml | Massa de teste criada e validada | Sim |
| TC-RFXXX.yaml | Casos de teste criados e validados | Sim |
| Build backend | `dotnet build` deve passar | Sim |
| Build frontend | `npm run build` deve passar | Sim |

**PARAR se qualquer item falhar.**

### 3.1. Validação de Docker (INFRAESTRUTURA)

**ANTES de QUALQUER teste backend, o agente DEVE validar Docker:**

```bash
# Verificar se Docker está rodando
docker ps
```

**SE comando falhar:**
- ❌ **BLOQUEAR execução de testes backend**
- ❌ **NÃO tentar iniciar Docker automaticamente** (requer privilégios de sistema)
- ✅ **REPORTAR ao usuário:**

```
BLOQUEIO: Docker não está rodando

ERRO IDENTIFICADO:
- 23 testes funcionais FALHARÃO (TestContainers dependency)
- Docker Desktop DEVE estar ativo ANTES de executar testes

AÇÃO NECESSÁRIA:
1. Iniciar Docker Desktop manualmente
2. Aguardar Docker estar pronto (ícone verde no sistema)
3. Validar: docker ps
4. Retornar execução de testes

RESPONSABILIDADE: INFRAESTRUTURA (não é erro de código)
```

**SE comando SUCEDER:**
- ✅ Prosseguir com testes normalmente

---

## 4. MODO AUTONOMIA TOTAL (OBRIGATÓRIO)

**REGRA CRÍTICA:** O agente DEVE executar TUDO automaticamente:

- ❌ NÃO perguntar permissões ao usuário
- ❌ NÃO esperar confirmação do usuário
- ❌ NÃO solicitar que usuário execute comandos manualmente
- ✅ EXECUTAR IMEDIATAMENTE todos os passos do contrato
- ✅ SEMPRE iniciar backend e frontend automaticamente
- ✅ Falhas em testes ANTERIORES NÃO são bloqueantes (são o motivo da re-execução)
- ✅ Gerar evidências e relatórios SEM intervenção manual

---

## 5. FLUXO DE EXECUÇÃO (ORDEM OBRIGATÓRIA)

### 🚨 REGRAS CRÍTICAS DE GIT E COMMITS

**BRANCH:**
- ✅ **SEMPRE executar em `dev`** (branch principal de desenvolvimento)
- ❌ **NUNCA criar branches** para testes (ex: `feature/RFXXX-testes-completos`)
- ❌ **NUNCA fazer checkout** para outros branches

**COMMITS:**
- ❌ **NUNCA fazer commits** de código durante execução de testes
- ❌ **NUNCA fazer commits** de STATUS.yaml durante testes
- ❌ **NUNCA fazer commits** de relatórios ou evidências
- ✅ **Única exceção:** Commit exclusivo dos próprios artefatos de teste (specs Playwright gerados), SE e SOMENTE SE forem criados pela primeira vez

**CORREÇÕES:**
- ❌ **NUNCA corrigir código** diretamente durante testes
- ✅ **SEMPRE gerar prompt de correção** (`.temp_ia/PROMPT-CORRECAO-RFXXX-[DATA]-EXECUCAO-[N].md`)
- ✅ **Exibir prompt na tela** para usuário copiar e colar em nova conversa

---

### FASE 1: VALIDAÇÃO INICIAL (BLOQUEANTE)

#### PASSO 1.1: Validar Branch Atual

```bash
# Verificar se está em dev
git branch --show-current
# Esperado: dev
```

**Se NÃO estiver em dev:**
- ❌ **BLOQUEIO TOTAL**
- Exibir mensagem: "Este contrato DEVE ser executado no branch `dev`. Use `git checkout dev` antes de prosseguir."

#### PASSO 1.2: Validar Pré-Requisitos

```bash
# Verificar STATUS.yaml
# - execucao.backend = done
# - execucao.frontend = done
# - documentacao.mt = true
# - documentacao.tc = true

# Verificar arquivos
# - D:\IC2\backend\IControlIT.API/IControlIT.API.sln existe
# - D:\IC2\frontend\icontrolit-app/package.json existe
# - rf/.../MT-RFXXX.yaml existe
# - rf/.../TC-RFXXX.yaml existe
```

**Se qualquer validação FALHAR:** BLOQUEIO TOTAL

#### PASSO 1.3: Matar Processos Travados (AUTOMÁTICO)

**ANTES de validar builds, o agente DEVE AUTOMATICAMENTE matar processos travados:**

```bash
# Usar run.py para matar processos (RECOMENDADO)
python run.py --kill-only
```

**OU (se --kill-only não disponível, usar PowerShell/Bash):**

```powershell
# Windows
powershell.exe -ExecutionPolicy Bypass -Command "Get-Process | Where-Object { $_.ProcessName -like '*IControlIT*' -or $_.ProcessName -like '*node*' } | Stop-Process -Force"
```

**IMPORTANTE:**
- Esta etapa é **OBRIGATÓRIA** antes de builds
- Processos travados (PID bloqueando DLLs) são **NORMAIS** em desenvolvimento
- **NÃO gerar prompt de correção** para processos travados
- Apenas matar automaticamente e prosseguir

#### PASSO 1.4: Validar Builds

```bash
# Backend
cd backend/IControlIT.API
dotnet build --no-incremental

# Frontend
cd frontend/icontrolit-app
npm run build
```

**Se QUALQUER build FALHAR (APÓS matar processos):** BLOQUEIO TOTAL (PARAR, REPORTAR, BLOQUEAR)

---

### FASE 2: SETUP DE AMBIENTE (AUTOMÁTICO)

#### PASSO 2.1: Inicialização Automática (RECOMENDADO)

**A forma MAIS SIMPLES e RECOMENDADA de iniciar o sistema completo:**

```bash
python run.py
```

O script `run.py` executa automaticamente:
- ✅ Mata TODOS os processos travados (backend e frontend)
- ✅ Inicia backend em BACKGROUND (porta 5000)
- ✅ Inicia frontend em BACKGROUND (porta 4200)
- ✅ Aguarda ambos estarem prontos
- ✅ Valida health checks automaticamente

**IMPORTANTE:** Sempre use `python run.py` para garantir ambiente limpo e funcional.

#### PASSO 2.2: Credenciais de Teste (OBRIGATÓRIO)

Para executar testes E2E, use as seguintes credenciais:

```
Email: anderson.chipak@k2apartners.com.br
Senha: Vi696206@
```

Este usuário tem:
- ✅ Perfil: Developer (escopo = 3)
- ✅ Permissões completas para TODOS os RFs
- ✅ Acesso a TODAS as funcionalidades do sistema
- ✅ Dados de teste pré-populados

#### PASSO 2.3: Preparação Manual (FALLBACK)

Se `run.py` falhar ou não estiver disponível, executar MANUALMENTE:

```powershell
# 1. Matar processos travados (se houver)
Get-Process | Where-Object { $_.ProcessName -like "*IControlIT*" } | Stop-Process -Force

# 2. Aplicar seeds
cd backend/IControlIT.API
dotnet ef database update

# 3. Iniciar backend (BACKGROUND)
cd backend/IControlIT.API
Start-Process -NoNewWindow -FilePath "dotnet" -ArgumentList "run"

# 4. Iniciar frontend (BACKGROUND)
cd frontend/icontrolit-app
Start-Process -NoNewWindow -FilePath "npm" -ArgumentList "start"
```

**IMPORTANTE:** Backend pode travar durante inicialização de seeds.

**Se /health não responder em 20s, backend está travado. Solução:**

1. Verificar se Program.cs tem Task.Run() em InitialiseDatabaseAsync
2. Se NÃO tiver, backend vai travar. Corrigir conforme:
   - Linha 216-232 de D:\IC2\backend\IControlIT.API/src/Web/Program.cs
   - DEVE usar Task.Run() para executar seeds em BACKGROUND
   - Nunca usar await direto (bloqueia startup)

3. Se backend continuar travado após 30s:
   - Matar processo: `Stop-Process -Name "IControlIT.API.Web" -Force`
   - Limpar artifacts: `Remove-Item D:\IC2\backend\IControlIT.API/artifacts -Recurse -Force`
   - Rebuild: `dotnet build --no-incremental`
   - Reiniciar: `dotnet run`

#### PASSO 2.4: Validação de Health

Após iniciar backend (via run.py OU manual), SEMPRE validar:

```bash
# Tentar 3 vezes com intervalo de 5s
curl http://localhost:5000/health
# Esperado: Status 200 OK (Healthy)
```

**Se timeout após 15s total:** Backend TRAVADO (erro CRÍTICO)

---

### FASE 3: TESTES BACKEND (Prioridade 1)

#### PASSO 3.1: Executar Testes Backend

```bash
cd backend/IControlIT.API
dotnet test --verbosity normal
```

#### PASSO 3.2: Registrar Resultados

- ✅ Testes unitários passaram
- ✅ Testes de integração passaram
- ✅ Testes de contrato passaram
- ✅ Testes de violação passaram
- ✅ Backend rejeita payloads inválidos

**Resultado:** PASS/FAIL

---

### FASE 4: TESTES FRONTEND (Prioridade 2)

#### PASSO 4.1: Executar Testes Frontend

```bash
cd frontend/icontrolit-app
npm run test
```

#### PASSO 4.2: Registrar Resultados

- ✅ Testes unitários passaram
- ✅ Testes de componentes passaram
- ✅ Testes de serviços passaram
- ✅ Validações de formulário funcionando

**Resultado:** PASS/FAIL

---

### FASE 5: TESTES E2E (Prioridade 3) — AUTO-GERAÇÃO INTELIGENTE

#### 🚨 PASSO 5.1: VERIFICAR SE SPECS PLAYWRIGHT EXISTEM (OBRIGATÓRIO)

**ANTES de executar testes E2E, o agente DEVE verificar:**

```bash
# 1. Verificar pasta de specs do RF
ls D:\IC2\frontend\icontrolit-app/e2e/specs/RFXXX/

# 2. Verificar arquivo de dados MT
ls D:\IC2\frontend\icontrolit-app/e2e/data/MT-RFXXX.data.ts

# 3. Ler TC-RFXXX.yaml e contar TC-E2E
# Exemplo: TC-RF006-E2E-001, TC-RF006-E2E-002, etc.
```

**Regra de Cobertura:**
- Para CADA `TC-RFXXX-E2E-NNN` em TC-RFXXX.yaml
- DEVE existir `TC-RFXXX-E2E-NNN.spec.ts` em `e2e/specs/RFXXX/`

**Exemplo:**
```yaml
# TC-RF006.yaml
test_cases:
  - tc_id: TC-RF006-E2E-001
    # ...
  - tc_id: TC-RF006-E2E-002
    # ...
  - tc-id: TC-RF006-E2E-003
    # ...
```

**Deve existir:**
```
D:\IC2\frontend\icontrolit-app/e2e/specs/RF006/
├── TC-RF006-E2E-001.spec.ts
├── TC-RF006-E2E-002.spec.ts
└── TC-RF006-E2E-003.spec.ts
```

#### 🚨 PASSO 5.2: SE SPECS NÃO EXISTEM OU INCOMPLETOS → AUTO-GERAÇÃO (BLOQUEANTE)

**SE specs não existem ou cobertura < 100%:**

**O agente DEVE AUTOMATICAMENTE:**

1. **Ativar contrato de geração de specs:**
   ```
   Conforme contracts/testes/geracao-testes-e2e-playwright.md para RFXXX.
   Seguir D:\IC2\CLAUDE.md.
   ```

2. **O contrato de geração irá:**
   - Ler TC-RFXXX.yaml e MT-RFXXX.yaml
   - Gerar `D:\IC2\frontend\e2e/data/MT-RFXXX.data.ts`
   - Gerar `D:\IC2\frontend\e2e/helpers/rf-helpers.ts`
   - Gerar `D:\IC2\frontend\e2e/specs/RFXXX/*.spec.ts` (1 spec por TC-E2E)
   - Validar cobertura 100% de TC-E2E

3. **SOMENTE prosseguir** se geração aprovada 100%

**REGRA CRÍTICA:**
- ❌ NÃO executar testes E2E sem specs completos
- ❌ NÃO pular auto-geração
- ✅ SEMPRE validar cobertura 100% antes de executar
- ✅ SEMPRE chamar contrato de geração se specs faltando

#### PASSO 5.3: Executar Testes E2E

```bash
cd frontend/icontrolit-app
npm run e2e
```

#### PASSO 5.4: Validar Fluxos Completos

- ✅ Login como developer (anderson.chipak@k2apartners.com.br / Vi696206@)
- ✅ Navegar via menu
- ✅ Acessar tela do RFXXX
- ✅ Executar CRUD completo (criar, editar, excluir, consultar)

#### PASSO 5.5: Validar 4 Estados Renderizados

- ✅ Estado Padrão (dados carregados)
- ✅ Estado Loading (spinner/skeleton visível)
- ✅ Estado Vazio (mensagem quando lista vazia)
- ✅ Estado Erro (mensagem quando HTTP falha)

#### PASSO 5.6: Validar i18n

- ✅ pt-BR (Português Brasil)
- ✅ en-US (Inglês EUA)
- ✅ es-ES (Espanhol)

#### PASSO 5.7: Capturar Evidências

- Screenshots de cada estado
- Vídeos de execução (se disponível)
- Logs completos
- Traces do Playwright

**Resultado:** PASS/FAIL

---

### FASE 6: TESTES DE SEGURANÇA (Prioridade 4)

#### PASSO 6.1: Validar Proteções

- ✅ SQL Injection (backend rejeita)
- ✅ XSS (backend sanitiza, frontend escapa)
- ✅ CSRF (tokens validados)
- ✅ Autenticação (401 quando não logado)
- ✅ Autorização (403 quando sem permissão)
- ✅ Multi-tenancy (isolamento entre tenants)

**Resultado:** PASS/FAIL

---

### FASE 7: CONSOLIDAÇÃO DE RESULTADOS

#### PASSO 7.1: Calcular Taxa de Aprovação

```
Taxa = (Testes PASS / Total Testes) * 100%
```

#### PASSO 7.2: Identificar Falhas Críticas

Para cada teste FALHADO:
- Identificar categoria (BACKEND/FRONTEND/INTEGRAÇÃO)
- Capturar evidências (screenshot, log, trace)
- Gerar relatório de falha
- **Criar prompt de correção automático (OBRIGATÓRIO)**

#### PASSO 7.3: Atribuir Responsabilidade

**BACKEND é responsável quando:**
- HTTP 500 (erro interno do servidor)
- HTTP 400 com mensagem incorreta
- Validação aceita payload inválido
- Violação não rejeitada
- Multi-tenancy quebrado (retorna dados de outro tenant)
- Auditoria não gravada
- Endpoint /health não responde (TIMEOUT/ERROR/BACKEND_DOWN)
- Backend não confirma "Application started" nos logs
- Seeds travando inicialização (InitialiseDatabaseAsync bloqueante)
- **AutoMapper configuration inválida:**
  - Teste `ShouldHaveValidConfiguration` falhando
  - Unmapped members detectados
  - Arquivo responsável: `*MappingProfile.cs`
  - **Correção via CONTRATO DE MANUTENÇÃO CONTROLADA**
  - **NÃO criar data-test para isto** (não é UI)

**FRONTEND é responsável quando:**
- Elemento não renderizado (data-test ausente)
- Estado Loading não visível
- Estado Vazio não visível
- Estado Erro não visível
- i18n quebrado (chave não traduzida)
- Validação de formulário ausente

**INTEGRAÇÃO é responsável quando:**
- Contrato de API quebrado (campo ausente)
- DTO incompatível
- Mapeamento incorreto

**INFRAESTRUTURA é responsável quando:**
- Docker não está rodando (TestContainers dependency)
- Processo travado bloqueando DLLs (PID bloqueante)
- Variáveis de ambiente ausentes
- Banco de dados não acessível
- **NÃO gerar prompt de correção para infraestrutura**
- **Reportar ao usuário para ação manual**

#### 🚨 REGRA ESPECIAL: Erros de Infraestrutura

**Quando erro for de INFRAESTRUTURA, o agente DEVE:**

1. ❌ **NÃO gerar prompt de correção** (agente não pode corrigir infraestrutura)
2. ✅ **Reportar claramente ao usuário:**
   ```
   BLOQUEIO: Infraestrutura (não é erro de código)

   ERRO IDENTIFICADO:
   - [Descrição do erro de infraestrutura]

   AÇÃO NECESSÁRIA (USUÁRIO):
   1. [Passo 1 manual]
   2. [Passo 2 manual]
   3. Retornar execução de testes

   RESPONSABILIDADE: INFRAESTRUTURA
   ```
3. ✅ **Atualizar STATUS.yaml com bloqueio:**
   ```yaml
   testes_ti:
     resultado_final: "BLOQUEADO"
     motivo_bloqueio: "Infraestrutura - Docker não está rodando"
     requer_acao_manual: true
   ```

---

### FASE 7.4: GERAR PROMPT DE CORREÇÃO AUTOMÁTICO (SE REPROVADO)

**SE taxa de aprovação < 100%, o agente DEVE OBRIGATORIAMENTE:**

1. ✅ **Gerar prompt de correção completo e descritivo**
2. ✅ **Salvar em `.temp_ia/PROMPT-CORRECAO-RFXXX-[DATA]-EXECUCAO-[N].md`**
3. ✅ **Exibir prompt completo na tela**
4. ✅ **Informar ao usuário:**
   ```
   📋 PROMPT DE CORREÇÃO GERADO

   Arquivo: .temp_ia/PROMPT-CORRECAO-RFXXX-2026-01-05-EXECUCAO-1.md

   Para corrigir os erros identificados, COPIE o conteúdo do arquivo acima
   e COLE em uma NOVA CONVERSA com o Claude Code.

   O prompt já está pronto para uso e contém:
   - Contexto completo da execução
   - Erros identificados com responsabilidade atribuída
   - Evidências técnicas completas
   - Solução esperada detalhada
   ```
5. ❌ **NUNCA tentar corrigir código** durante execução de testes
6. ❌ **NUNCA fazer commits** de correções

#### ⚠️ REGRA OBRIGATÓRIA: Prompt Completo e Descritivo

O prompt de correção **DEVE** conter:

1. ✅ **Contexto da execução** (RF, data, execução N, taxa de aprovação)
2. ✅ **Descrição específica do erro** (mensagem exata, código de erro)
3. ✅ **Evidências completas** (logs, processos travados, arquivos bloqueados)
4. ✅ **Comandos já tentados** (e seus resultados - SUCESSO/FALHOU + motivo)
5. ✅ **Fase e passo onde erro ocorreu** (ex: FASE 2 → PASSO 2.1)
6. ✅ **Responsabilidade atribuída** (BACKEND/FRONTEND/INTEGRAÇÃO + justificativa técnica)
7. ✅ **Arquivos prováveis** (onde erro provavelmente está)
8. ✅ **Solução esperada** (passos claros e específicos, não genéricos)

**PROIBIDO:**
- ❌ Prompt vago ("Corrija isso usando...")
- ❌ Placeholders não substituídos ([YYYY-MM-DD], [N], [Lista...])
- ❌ Falta de evidências técnicas
- ❌ Soluções genéricas ("corrigir o erro")
- ❌ Omitir comandos tentados

#### Template de Prompt de Correção

```markdown
Execute D:\IC2_Governanca\prompts\desenvolvimento\manutencao\manutencao-controlada.md para corrigir os seguintes erros CRÍTICOS identificados na Execução [N] de testes do RFXXX:

## CONTEXTO DA EXECUÇÃO

- **RF:** RFXXX - [Título do RF]
- **Data:** [YYYY-MM-DD]
- **Execução:** [N]ª tentativa
- **Taxa de Aprovação:** [XX%] ([Y]/[Z] testes)
- **Resultado:** REPROVADO (critério: 100%)
- **Relatório:** .temp_ia/RELATORIO-TESTES-RFXXX-[DATA]-EXECUCAO-[N].md
- **STATUS.yaml:** Atualizado com execução [N]

## ERROS IDENTIFICADOS

[PARA CADA CATEGORIA DE ERRO (FRONTEND, BACKEND, INTEGRAÇÃO), GERAR:]

### ERRO [N] - [CATEGORIA] (PRIORIDADE [1-4] - [BLOQUEANTE/ALTA/MÉDIA/BAIXA])

#### Descrição do Erro
- **TC falhados:** [Lista de TCs ou quantidade]
- **Erro:** [Mensagem de erro principal]
- **Status:** [Descrição do impacto]

#### Evidências
- Frontend build: [✅/❌] [detalhes]
- Backend build: [✅/❌] [detalhes]
- Frontend rodando: [✅/❌] [URL]
- Backend rodando: [✅/❌] [URL]
- Sistema base (FASE-1): [✅/❌] [X/Y testes passando]
- **RFXXX [Camada]:** [✅/❌] [X/Y testes passando]

#### Testes Falhados
[Lista detalhada de specs/testes que falharam]

#### Responsabilidade
- **Camada:** [BACKEND/FRONTEND/INTEGRAÇÃO] ❌
- **Razão:** [Por que atribuiu a essa camada]

#### Arquivos Prováveis
[Lista de arquivos que provavelmente contêm o erro]

#### Comandos Tentados
[Lista completa de comandos executados durante troubleshooting]
1. `[comando 1]` → [✅ SUCESSO / ❌ FALHOU] ([motivo])
2. `[comando 2]` → [✅ SUCESSO / ❌ FALHOU] ([motivo])

#### Contexto Técnico
- **Fase do erro:** [FASE X] → [PASSO X.X]
- **[Informação relevante 1]**
- **[Informação relevante 2]**
- **Problema:** [Descrição técnica do problema]

#### Solução Esperada
1. [Passo 1 da correção esperada - ESPECÍFICO, não genérico]
2. [Passo 2 da correção esperada - ESPECÍFICO, não genérico]
3. [...]

---

## ORDEM DE CORREÇÃO OBRIGATÓRIA

[SE HOUVER MÚLTIPLAS CATEGORIAS, DEFINIR ORDEM DE PRIORIDADE:]

### FASE 1 - [CATEGORIA BLOQUEANTE]
[Descrição do que deve ser corrigido primeiro]

### FASE 2 - [CATEGORIA ALTA]
[Descrição do que deve ser corrigido em seguida]

---

## CRITÉRIO DE SUCESSO

- ✅ [Critério específico 1]
- ✅ [Critério específico 2]
- ✅ Taxa de aprovação = 100% ([Z]/[Z] testes)

---

## OBSERVAÇÕES IMPORTANTES

1. **NÃO** altere código de testes (specs Playwright estão corretos)
2. **NÃO** altere configuração de porta (4200 está correto)
3. **FOCO:** [Áreas específicas a corrigir]

Modo governança rígida. Não negociar escopo. Não extrapolar.
Seguir D:\IC2\CLAUDE.md e contracts/desenvolvimento/execucao/manutencao/manutencao-controlada.md.
```

#### Regras para Geração do Prompt

1. **Priorização de Erros:**
   - **PRIORIDADE 1 (BLOQUEANTE):** Erros que impedem outros testes de executar
     - Frontend: Rota não acessível, componente não carrega
     - Backend: API não responde, autenticação quebrada

   - **PRIORIDADE 2 (ALTA):** Erros que afetam múltiplos testes
     - AutoMapper configuration
     - Seeds/Fixtures quebrados
     - Validações faltando

   - **PRIORIDADE 3 (MÉDIA):** Erros isolados em funcionalidades específicas
     - CRUD de entidade específica
     - Validação de campo específico

   - **PRIORIDADE 4 (BAIXA):** Erros de i18n, formatação, não-críticos

2. **Agrupamento de Erros:**
   - Agrupar erros da mesma categoria (FRONTEND vs BACKEND)
   - Agrupar erros da mesma causa raiz (ex: todos relacionados à mesma rota)
   - Ordenar por prioridade decrescente

3. **Evidências Obrigatórias:**
   - ✅ Status de build (frontend e backend)
   - ✅ Status de servidores (rodando ou não)
   - ✅ Taxa de aprovação do sistema base (FASE-1)
   - ✅ Taxa de aprovação do RF específico
   - ✅ Lista completa de testes falhados

4. **Atribuição de Responsabilidade:**
   - Usar regras da FASE 7.3 para atribuir camada
   - Justificar atribuição com evidências técnicas
   - Listar arquivos prováveis que contêm o erro

5. **Solução Esperada:**
   - Descrever passos claros de correção
   - Referenciar arquivos específicos
   - Evitar soluções genéricas ("corrigir o erro")
   - Preferir soluções técnicas ("verificar se rota está registrada em app.routes.ts")

6. **Salvar Prompt:**
   - Criar arquivo: `.temp_ia/PROMPT-CORRECAO-RFXXX-[DATA]-EXECUCAO-[N].md`
   - Formato Markdown completo
   - Pronto para copiar e colar em nova conversa

7. **Comandos Tentados (NOVO - OBRIGATÓRIO):**
   - Listar TODOS os comandos executados durante troubleshooting
   - Incluir resultado de cada comando (✅ SUCESSO / ❌ FALHOU + motivo)
   - Exemplo:
     ```
     #### Comandos Tentados
     1. `taskkill /F /PID 20924` → ❌ FALHOU (argumento inválido /PID não reconhecido)
     2. `Get-Process | Where-Object...` → ❌ FALHOU (bash não reconhece PowerShell cmdlets)
     3. `python run.py &` → ✅ SUCESSO (backend reiniciou)
     ```

8. **Contexto de Fase/Passo (NOVO - OBRIGATÓRIO):**
   - Informar exatamente onde o erro ocorreu
   - Formato: "Fase do erro: FASE X (Nome) → PASSO X.X (Descrição)"
   - Exemplo: "Fase do erro: FASE 1 (PRÉ-REQUISITOS) → PASSO 1.2 (Validar Builds)"

---

#### 📋 Validação de Prompt Gerado (OBRIGATÓRIO)

**Após salvar `.temp_ia/PROMPT-CORRECAO-RFXXX-[DATA]-EXECUCAO-[N].md`, o agente DEVE:**

1. ✅ Verificar que arquivo foi criado
2. ✅ Verificar que arquivo tem > 100 linhas (prompt completo, não vago)
3. ✅ Verificar que NÃO contém placeholders não substituídos:
   - Buscar por `[YYYY-MM-DD]`, `[N]`, `[Lista...]`, `[RFXXX]`
   - Se encontrar qualquer placeholder → **BLOQUEIO TOTAL**
4. ✅ Verificar que seções obrigatórias estão presentes:
   - "## CONTEXTO DA EXECUÇÃO"
   - "## ERROS IDENTIFICADOS"
   - "### ERRO [N] - [CATEGORIA]"
   - "#### Descrição do Erro"
   - "#### Evidências"
   - "#### Comandos Tentados" (NOVO)
   - "#### Contexto Técnico" (com "Fase do erro:")
   - "#### Responsabilidade"
   - "#### Solução Esperada"
5. ✅ Exibir prompt completo na tela ANTES de salvar arquivo

**SE qualquer validação FALHAR:**
- ❌ **BLOQUEIO TOTAL**
- Exibir mensagem: "Prompt de correção incompleto ou vago. Refazer FASE 7.4 com captura completa de contexto."
- **NÃO prosseguir para FASE 8**

---

### FASE 8: DECISÃO FINAL

#### PASSO 8.1: Aplicar Critério 0% ou 100%

- ✅ **APROVADO**: Taxa de aprovação = 100% (TODOS os testes passaram)
- ❌ **REPROVADO**: Taxa de aprovação < 100% (QUALQUER teste falhou)

**NÃO EXISTE APROVAÇÃO COM RESSALVAS.**

#### PASSO 8.2: Atualizar STATUS.yaml (SEM COMMIT)

**IMPORTANTE:**
- ✅ Atualizar STATUS.yaml com resultados
- ❌ **NUNCA fazer commit** de STATUS.yaml durante testes
- ❌ **NUNCA fazer commit** de relatórios ou evidências
- ℹ️ Commit será feito APENAS quando correções forem aplicadas em nova conversa

```yaml
testes_ti:
  resultado_final: "APROVADO" # ou "REPROVADO"
  taxa_aprovacao: "100%" # ou "85%"
  data_execucao: "2026-01-03"
  backend:
    resultado: "PASS" # ou "FAIL"
    total: 50
    passaram: 50
  frontend:
    resultado: "PASS" # ou "FAIL"
    total: 30
    passaram: 30
  e2e:
    resultado: "PASS" # ou "FAIL"
    total: 15
    passaram: 15
    specs_gerados: true
  seguranca:
    resultado: "PASS" # ou "FAIL"
    total: 10
    passaram: 10
  azure_devops:
    ultima_execucao: "2026-01-03"
    taxa_aprovacao: "100%"
```

#### PASSO 8.3: Atualizar Azure DevOps

```bash
# Atualizar azure-test-cases-RF[XXX].csv
# - Coluna "State" atualizada (Design → Ready → Active → Closed)
# - Resultados de execução adicionados
# - Data de última execução registrada
```

---

### FASE 9: EVIDÊNCIAS OBRIGATÓRIAS

#### PASSO 9.1: Gerar Evidências

- Screenshots de testes E2E (sucesso e falhas)
- Vídeos de execução (se disponível)
- Logs de execução completos
- Relatório HTML de testes
- Relatório de cobertura
- Relatório de responsabilidade (backend vs frontend)

#### PASSO 9.2: Organizar Evidências

```
relatorios/RFXXX/testes/
├── backend/
│   └── test-results.xml
├── frontend/
│   └── test-results.json
├── e2e/
│   ├── screenshots/
│   ├── videos/
│   ├── traces/
│   └── playwright-report/
├── seguranca/
│   └── security-scan-results.txt
└── RELATORIO-CONSOLIDADO-TESTES-RFXXX.md
```

---

## 6. RELATÓRIO DE FALHAS (SE REPROVADO)

Para cada teste REPROVADO, criar:

```markdown
# RELATÓRIO DE FALHA - TC-RFXXX-[CAT]-NNN

## TESTE FALHADO
- TC: TC-RFXXX-[CAT]-NNN
- Descrição: [descrição do teste]
- Categoria: [HAPPY_PATH/VALIDACAO/SEGURANCA/E2E/etc]
- Prioridade: CRITICA/ALTA/MEDIA/BAIXA

## ERRO IDENTIFICADO
- Mensagem: [erro completo]
- Screenshot: evidencias/TC-RFXXX-[CAT]-NNN-falha.png
- Log: logs/TC-RFXXX-[CAT]-NNN.log

## RESPONSABILIDADE
- Camada: BACKEND ❌ | FRONTEND ❌ | INTEGRAÇÃO ❌
- Razão: [por que atribuiu a essa camada]
- Arquivo provável: [caminho do arquivo]
- Linha provável: [número da linha, se identificável]

## CONTEXTO
- MT usada: MT-RFXXX-NNN
- Dados enviados: { ... }
- Resposta recebida: { ... }
- Resposta esperada: { ... }

## PRÓXIMO PASSO
Corrigir via prompt de manutenção:

\```
Execute D:\IC2_Governanca\prompts\desenvolvimento\manutencao\manutencao-controlada.md para corrigir o seguinte erro no [backend/frontend] de RFXXX:

ERRO IDENTIFICADO:
- TC falhado: TC-RFXXX-[CAT]-NNN
- [Descrição completa do erro]

EVIDÊNCIAS:
- Screenshot: evidencias/TC-RFXXX-[CAT]-NNN-falha.png
- Log: logs/TC-RFXXX-[CAT]-NNN.log

CONTEXTO:
- RF: RFXXX
- UC: UCXX
- Handler/Component: [nome]
\```
```

---

## 7. PROIBIÇÕES

É **PROIBIDO**:

### 7.1. Proibições de Git/Commits

- ❌ **Criar branches** para testes (ex: `feature/RFXXX-testes-completos`)
- ❌ **Fazer checkout** para outros branches (sempre executar em `dev`)
- ❌ **Fazer commits** de código durante testes
- ❌ **Fazer commits** de STATUS.yaml durante testes
- ❌ **Fazer commits** de relatórios ou evidências
- ✅ **Única exceção:** Commit de specs Playwright SE gerados pela primeira vez

### 7.2. Proibições de Correção de Código

- ❌ **Alterar código de produção** durante testes
- ❌ **Corrigir erros** diretamente durante testes
- ❌ **Modificar testes** para fazer passar
- ✅ **SEMPRE gerar prompt de correção** quando encontrar problemas

### 7.3. Proibições de Execução

- ❌ Executar apenas subset de testes
- ❌ Pular testes que falharam
- ❌ Marcar como APROVADO se taxa < 100%
- ❌ Executar testes sem buildar antes
- ❌ Executar testes sem seeds aplicados
- ❌ **Executar testes E2E sem verificar se specs existem**
- ❌ **Pular auto-geração de specs quando faltando**
- ❌ **Executar com frontend em porta diferente de 4200**

---

## 8. CRITÉRIO DE PRONTO

O contrato só é considerado CONCLUÍDO quando:

### 8.1. Validações de Ambiente

- [ ] Branch atual é `dev` (validado no PASSO 1.1)
- [ ] Pré-requisitos validados (backend/frontend aprovados, MT/TC validados)
- [ ] Builds validados (backend e frontend buildando sem erros)
- [ ] Ambiente iniciado (backend porta 5000, frontend porta 4200)
- [ ] Health checks validados (backend e frontend respondendo)

### 8.2. Execução de Testes

- [ ] **Specs Playwright verificados (se não existem → gerados automaticamente)**
- [ ] Testes backend executados (dotnet test)
- [ ] Testes frontend executados (npm run test)
- [ ] Testes E2E executados (npm run e2e)
- [ ] Testes de segurança executados

### 8.3. Consolidação de Resultados

- [ ] Taxa de aprovação calculada
- [ ] Falhas identificadas com responsável atribuído
- [ ] Evidências geradas (screenshots, logs, traces)
- [ ] Relatório consolidado criado

### 8.4. Prompt de Correção (SE REPROVADO)

- [ ] **SE taxa < 100%: Prompt de correção gerado e validado:**
  - [ ] Arquivo `.temp_ia/PROMPT-CORRECAO-RFXXX-[DATA]-EXECUCAO-[N].md` criado
  - [ ] Prompt tem > 100 linhas (completo, não vago)
  - [ ] ZERO placeholders não substituídos ([YYYY-MM-DD], [N], etc.)
  - [ ] Todas as seções obrigatórias presentes (incluindo "Comandos Tentados")
  - [ ] **Prompt exibido na tela COMPLETO** para usuário copiar
  - [ ] **Mensagem clara:** "COPIE o prompt acima e COLE em nova conversa"

### 8.5. Atualização de Artefatos (SEM COMMITS)

- [ ] STATUS.yaml atualizado (incluindo testes.azure_devops)
- [ ] azure-test-cases-RF[XXX].csv atualizado (State conforme resultado)
- [ ] Decisão registrada (APROVADO/REPROVADO)
- [ ] **IMPORTANTE:** ZERO commits realizados (exceto specs Playwright se gerados pela primeira vez)

### 8.6. Validações Finais

- [ ] Nenhuma violação de contrato
- [ ] Nenhum branch criado
- [ ] Nenhum código de produção alterado
- [ ] **SE REPROVADO:** Prompt de correção pronto para uso

---

## 9. REGRA DE NEGAÇÃO ZERO

Se uma solicitação:
- não estiver explicitamente prevista no contrato ativo, ou
- conflitar com qualquer regra do contrato

ENTÃO:

- A execução DEVE ser NEGADA
- Nenhuma ação parcial pode ser realizada
- Nenhum "adiantamento" é permitido

---

**FIM DO CONTRATO**
