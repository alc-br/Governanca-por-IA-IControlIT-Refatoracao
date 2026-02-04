# CONTRATO DE EXECUÇÃO COMPLETA DE TESTES

**Versão:** 2.3
**Data:** 2026-02-04
**Status:** Ativo
**Última Atualização:** 2026-02-04 (REGRA DE NÃO PARADA: Nunca pare em estado parcial)
**Changelog:**
- v2.3 (2026-02-04): **REGRA CRÍTICA DE NÃO PARADA**: Agente NUNCA pode parar em estado parcial (66%, 80%) sem esgotar TODAS as tentativas de resolução - Resposta ao caso RF007 onde agente parou aos 66% sem tentar resolver problema de autenticação
- v2.2 (2026-01-11): NOVA SEÇÃO 2.5: Seleção de Estratégia de Testes (MVS para HOM, COMPLETO para PRD) - Reduz tempo de 10h → 2-4h para homologação mantendo 80% cobertura de riscos críticos
- v2.1 (2026-01-11): NOVO PASSO 5.10 BLOQUEANTE: Validar isolamento de testes E2E (isolated vs stateful, beforeEach/afterEach, closeAllOverlays) - Detecta padrão test.describe.serial PROIBIDO em testes isolated
- v2.0 (2026-01-11): NOVO PASSO 5.9 BLOQUEANTE: Validar cobertura 100% de TCs (resolve GAP 2 do RF006 - 75% não testado)
- v1.9 (2026-01-08): OTIMIZAÇÃO CRÍTICA: run.py v2.0 valida health automaticamente (removidos health checks manuais do contrato)
- v1.8 (2026-01-08): NOVA FEATURE: Merge automático em dev quando testes atingem 100% em branch fix/*
- v1.7 (2026-01-08): MUDANÇA CRÍTICA: Executa no branch ativo (não valida, não faz checkout)
- v1.6 (2026-01-08): NOVA FASE 6.5: Auditoria de Conformidade Funcional e UX (incongruências, funcionalidades duplicadas, UX)
- v1.5 (2026-01-08): CORREÇÃO CRÍTICA: validação de frontend com retry (120s) - Angular demora mais
- v1.4 (2026-01-08): CORREÇÃO CRÍTICA: removido PASSO 1.4 (matar processos) - run.py já cuida disso
- v1.3 (2026-01-08): CORREÇÃO CRÍTICA: health checks movidos para PASSO 1.3 (ANTES de matar processos)
- v1.2 (2026-01-08): Adicionada verificação inteligente de ambiente (health checks antes de iniciar)
- v1.1.1 (2026-01-08): Correção de estrutura de caminhos (MT-RF*.yaml e TC-RF*.yaml estão na raiz do RF)
- v1.1 (2026-01-08): Adicionadas 5 otimizações de eficiência (⬇️ 66% tempo de inicialização)
- v1.0 (2026-01-03): Criação do contrato com auto-geração de specs E2E

---

## 📋 SUMÁRIO EXECUTIVO

### ⚡ O que este contrato faz

Este contrato **EXECUTA TODOS OS TESTES** de um RF automaticamente, incluindo:

- ✅ **Testes Backend**: Unitários, integração, contrato, violação
- ✅ **Testes Frontend**: Unitários, componentes, serviços
- ✅ **Testes E2E**: Playwright (com auto-geração se necessário)
- ✅ **Testes de Segurança**: SQL Injection, XSS, CSRF, Auth, Multi-tenancy
- ✅ **Auditoria de Conformidade**: Incongruências funcionais, UX, funcionalidades duplicadas
- ✅ **Responsabilização Automática**: Identifica se falha é backend ou frontend
- ✅ **Evidências Automáticas**: Screenshots, vídeos, logs, relatórios

---

## 0. MAPA DE CAMINHOS RÁPIDOS (CONSULTA OBRIGATÓRIA)

**IMPORTANTE:** Estrutura reorganizada em 2026-01-08. Use caminhos atualizados abaixo.

### 0.1. Estrutura de Governança

```bash
D:\IC2_Governanca\
├── CLAUDE.md                          # Governança superior (leitura obrigatória)
├── governanca\
│   ├── contracts\
│   │   ├── testes\execucao-completa.md        # Este contrato
│   │   └── manutencao\*.md
│   ├── prompts\
│   │   └── testes\execucao-completa.md        # Prompt de ativação
│   └── checklists\
│       └── testes\pre-execucao.yaml           # Checklist pré-execução
└── documentacao\
    └── [Fase]\[EPIC]\[RF]\
        ├── RF*.yaml                            # Estrutura do RF
        ├── MT-RF*.yaml                         # Massa de teste (raiz do RF)
        ├── TC-RF*.yaml                         # Casos de teste (raiz do RF)
        ├── UC-RF*.yaml                         # Casos de uso (raiz do RF)
        ├── MD-RF*.yaml                         # Modelo de dados (raiz do RF)
        ├── Testes\                             # Casos de teste detalhados
        │   ├── Backend\TC-*.md                 # Casos de teste backend
        │   ├── Sistema\TC-*.md                 # Casos de teste frontend
        │   └── Outros\TC-*.md                  # Casos de teste outros
        └── schema.sql                          # Schema (se aplicável)
```

### 0.2. Estrutura de Código

```bash
D:\IC2\
├── STATUS.yaml                        # Status consolidado (LER APENAS NA FASE 8)
├── backend\IControlIT.API\
│   ├── IControlIT.API.sln
│   ├── src\                           # Código de produção
│   └── tests\                         # Testes backend
│       ├── Domain.UnitTests\
│       ├── Application.UnitTests\
│       └── Application.FunctionalTests\
└── frontend\icontrolit-app\
    ├── package.json
    ├── src\                           # Código de produção
    └── e2e\specs\                     # Specs Playwright (auto-gerados)
```

### 0.3. Regras de Leitura Eficiente

**REGRA #1: Usar caminhos diretos sempre que possível**
- ✅ `Read D:\IC2_Governanca\governanca\contracts\testes\execucao-completa.md`
- ❌ `Glob "**/execucao-completa.md"` (apenas se caminho desconhecido)

**REGRA #2: Não ler STATUS.yaml na FASE 1**
- STATUS.yaml será lido APENAS na FASE 8 (Atualização de STATUS)
- Na FASE 1, ler apenas: RF*.yaml, MT-RF*.yaml, TC-RF*.yaml

**REGRA #3: Leitura única de arquivos pequenos (<2000 linhas)**
- RF*.yaml, MT-RF*.yaml, TC-RF*.yaml: Ler UMA ÚNICA VEZ
- Se necessário consultar novamente: usar informações já lidas (não re-ler)
- Exceção: Arquivos grandes (>2000 linhas) podem ser lidos em partes

**REGRA #4: Ordem de leitura obrigatória**
```markdown
1. FASE 1 (Validação de Pré-requisitos):
   - RF*.yaml (estrutura do RF)
   - MT-RF*.yaml (massa de teste)
   - TC-RF*.yaml (casos de teste)
   - schema.sql (se necessário)

2. FASE 2-7 (Execução de Testes):
   - Nenhuma leitura adicional (usar informações já carregadas)

3. FASE 8 (Atualização de STATUS):
   - STATUS.yaml (primeira e única leitura)
```

**IMPACTO:**
- ⬇️ 66% no tempo de inicialização (de 30-45s para 10-15s)
- ⬇️ 83% em operações Glob (de 6 para 0-1)
- ⬇️ 100% em leituras redundantes

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
"Para o RF006 D:\IC2\documentacao\...\RF006-Gestao-de-Clientes execute o docs\prompts\testes\execucao-completa.md"
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

⚠️ CATEGORIAS INVENTADAS SÃO PROIBIDAS (v1.4 - 2026-01-31):

As seguintes categorias NÃO EXISTEM e são VIOLAÇÕES GRAVES:
- ❌ "APROVADO CONDICIONALMENTE" → NÃO EXISTE
- ❌ "APROVADO COM RESSALVAS" → NÃO EXISTE
- ❌ "APROVADO PARCIALMENTE" → NÃO EXISTE
- ❌ "APROVADO PARA HOM, PENDENTE PRD" → NÃO EXISTE
- ❌ "PROBLEMA DE INFRAESTRUTURA, NÃO DO CÓDIGO" → NÃO É DESCULPA

SE agente usar qualquer categoria acima:
- Execução é INVÁLIDA
- Aprovação é NULA
- Agente VIOLOU o contrato

REGRA PARA PROBLEMAS DE AUTENTICAÇÃO/INTEGRAÇÃO (v1.4):

SE testes falharem por problemas de autenticação (401, token expirado, interceptor):
1. NÃO aprovar condicionalmente
2. NÃO atribuir a "infraestrutura" e aprovar
3. RESOLVER o problema (debugar, ajustar config, corrigir código)
4. SE não conseguir resolver: REPROVAR com responsabilidade atribuída

Exemplos de atribuição CORRETA:
- Token expirado muito rápido → BACKEND (configuração JWT)
- Interceptor não adiciona header → FRONTEND (auth.interceptor.ts)
- LocalStorage não persiste → FRONTEND (auth.service.ts)
- E2E não mantém sessão → TESTES (storageState do Playwright)

A ÚNICA saída é: APROVADO (100%) ou REPROVADO (< 100%).
Não existe meio termo.
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

## 2.5. SELEÇÃO DE ESTRATÉGIA DE TESTES (NOVO - v2.2)

**ANTES de iniciar execução, o agente DEVE perguntar ao usuário qual estratégia usar:**

### Estratégias Disponíveis

#### OPÇÃO A: MVS - Mínimo Viável Seguro (PADRÃO PARA HOM)
- ⏱️ **Tempo:** 2-4 horas/RF
- 📊 **Cobertura:** 80% dos riscos críticos
- 🎯 **Uso:** Subir para **HOMOLOGAÇÃO**
- ✅ **Testes:**
  - Unitários backend: 100%
  - Smoke E2E: 1 spec (happy path)
  - Segurança: SQL Injection + Autenticação
- 📄 **Contrato:** `CONTRATO-TESTES-MINIMO-VIAVEL-SEGURO.md`

#### OPÇÃO B: COMPLETO (PADRÃO PARA PRD)
- ⏱️ **Tempo:** 10+ horas/RF
- 📊 **Cobertura:** 95-100% dos riscos
- 🎯 **Uso:** Subir para **PRODUÇÃO**
- ✅ **Testes:**
  - Unitários backend: 100%
  - E2E completo: Todos os specs (10-30 specs)
  - Segurança: Completo (5 tipos)
  - Auditoria UX
- 📄 **Contrato:** Este arquivo (execucao-completa.md)

### Decisão Automática (Se usuário não especificar)

**SE usuário mencionar "HOM" ou "homologação":**
- ✅ Usar estratégia **MVS** automaticamente
- ℹ️ Informar: "Usando estratégia MVS para HOM (2-4h)"

**SE usuário mencionar "PRD" ou "produção":**
- ✅ Usar estratégia **COMPLETO** automaticamente
- ℹ️ Informar: "Usando estratégia COMPLETO para PRD (10+h)"

**SE usuário NÃO especificar destino:**
- ❓ **PERGUNTAR**: "Este RF vai para HOM ou PRD?"
- ⏳ Aguardar resposta do usuário
- ✅ Aplicar estratégia correspondente

### Prompt de Confirmação

```
Este RF vai para:
A) HOMOLOGAÇÃO (usar MVS: 2-4h, 80% cobertura)
B) PRODUÇÃO (usar COMPLETO: 10+h, 95-100% cobertura)

Responda A ou B (ou especifique se incerto).
```

### Executando Estratégia MVS

**QUANDO usuário escolher MVS (OPÇÃO A):**

1. ✅ Ativar contrato: `CONTRATO-TESTES-MINIMO-VIAVEL-SEGURO.md`
2. ✅ Executar:
   - FASE 1: Pré-requisitos (validar backend/frontend aprovados)
   - FASE 2: Testes Unitários (100%)
   - FASE 3: Smoke Test E2E (1 spec)
   - FASE 4: Segurança Crítica (SQL Injection + Autenticação)
   - FASE 5: Aprovação Final
3. ✅ Gerar relatório: `RELATORIO-MVS-RFXXX-[DATA].yaml`
4. ✅ Atualizar STATUS.yaml: `estrategia: MVS, resultado_final: APROVADO_HOM`
5. ✅ Documentar gaps conhecidos: `GAPS-CONHECIDOS-RFXXX.md`

**Critério MVS:**
- ✅ Unitários: 100%
- ✅ Smoke E2E: 100% (1 spec)
- ✅ Segurança: 100%

**Tempo total:** 2-4 horas

---

### Executando Estratégia COMPLETO

**QUANDO usuário escolher COMPLETO (OPÇÃO B):**

1. ✅ Continuar execução normal deste contrato
2. ✅ Executar TODAS as fases (1-8)
3. ✅ Gerar relatório completo
4. ✅ Atualizar STATUS.yaml: `estrategia: COMPLETO, resultado_final: APROVADO_PRD`

**Critério COMPLETO:**
- ✅ Todos os testes: 100%

**Tempo total:** 10+ horas

---

### Regras de Estratégia

1. **MVS é SUFICIENTE para HOM** (cliente validará funcionalmente)
2. **COMPLETO é OBRIGATÓRIO para PRD** (zero tolerância a bugs)
3. **Estratégia é IRREVERSÍVEL** durante execução (não mudar no meio)
4. **Gaps conhecidos do MVS DEVEM ser documentados**

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

### 3.1. Validação de Docker (INFRAESTRUTURA) - BLOQUEANTE

**ANTES de QUALQUER teste backend, o agente DEVE validar Docker:**

```bash
# Verificar se Docker está rodando
docker ps
```

#### ℹ️ CONTEXTO: Testcontainers

**Por que Docker é necessário:**
- Testes funcionais backend usam **Testcontainers** (biblioteca .NET)
- Testcontainers cria containers SQL Server efêmeros para testes
- Containers são criados/destruídos automaticamente durante execução
- Arquivo responsável: `tests/Application.FunctionalTests/SqlTestcontainersTestDatabase.cs`

**Alternativa (SE Docker não disponível):**
- Existe `SqlTestDatabase.cs` que usa SQL Server local
- Requer alterar `TestDatabaseFactory.cs` (linha 9)
- **NÃO é responsabilidade do agente** (decisão arquitetural)
- **NÃO sugerir esta alternativa** ao usuário

---

**SE comando `docker ps` falhar:**
- ❌ **BLOQUEAR execução de testes funcionais backend**
- ❌ **NÃO tentar iniciar Docker automaticamente** (requer privilégios de sistema)
- ❌ **NÃO gerar prompt de correção** (não é erro de código)
- ❌ **NÃO sugerir usar SQL Server local** (decisão arquitetural)
- ✅ **REPORTAR ao usuário E CONTINUAR com testes unitários:**

```
⚠️ BLOQUEIO PARCIAL: Docker não está rodando

IMPACTO:
- ❌ Testes funcionais backend BLOQUEADOS (23 testes - Testcontainers dependency)
- ✅ Testes unitários backend PROSSEGUIRÃO normalmente (5 testes Domain.UnitTests)
- ✅ Testes unitários backend PROSSEGUIRÃO normalmente (26 testes Application.UnitTests)
- ✅ Testes frontend PROSSEGUIRÃO normalmente

CONTEXTO TÉCNICO:
- Testcontainers cria containers SQL Server efêmeros
- Biblioteca: Testcontainers.MsSql (via NuGet)
- Container: mcr.microsoft.com/mssql/server:2022-latest (baixado automaticamente)
- Arquivo: tests/Application.FunctionalTests/SqlTestcontainersTestDatabase.cs

AÇÃO NECESSÁRIA (USUÁRIO - ANTES DE RE-EXECUTAR):
1. Iniciar Docker Desktop manualmente
2. Aguardar Docker estar pronto (ícone verde na bandeja do sistema)
3. Validar: docker ps (deve retornar cabeçalhos sem erro)
4. Re-executar testes: prompts/testes/execucao-completa.md

OBSERVAÇÃO: Primeira execução pode ser lenta (download da imagem SQL Server ~1.5GB)

RESPONSABILIDADE: INFRAESTRUTURA (não é erro de código)
TIPO: BLOQUEIO DE AMBIENTE (não gera prompt de correção)
```

**SE comando `docker ps` SUCEDER:**
- ✅ Prosseguir com TODOS os testes normalmente
- ✅ Testcontainers criará containers SQL Server automaticamente
- ✅ Containers serão destruídos ao final dos testes

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

## 5. COMANDOS PRÉ-VALIDADOS

### Windows (Git Bash)

```bash
# Verificar branch
git -C /d/IC2 branch --show-current

# Build backend
cd /d/IC2/backend/IControlIT.API && dotnet build --no-incremental 2>&1 | tail -30

# Build frontend
cd /d/IC2/frontend/icontrolit-app && npm run build 2>&1 | tail -50

# Testes backend
cd /d/IC2/backend/IControlIT.API && dotnet test --verbosity normal
```

### PowerShell

```powershell
# Matar processos
Get-Process -Name "*IControlIT*","node" -ErrorAction SilentlyContinue | Stop-Process -Force
```

---

## 6. TIMEOUTS OBRIGATÓRIOS

| Fase | Timeout | Ação se Exceder |
|------|---------|-----------------|
| dotnet build | 3 minutos | ABORTAR (build travado) |
| npm run build | 5 minutos | ABORTAR (build travado) |
| dotnet test | 10 minutos | ABORTAR (testes travados) |
| npm run test | 5 minutos | ABORTAR (testes travados) |
| npm run e2e | 15 minutos | ABORTAR (E2E travado) |

---

## 7. FLUXO DE EXECUÇÃO (ORDEM OBRIGATÓRIA)

### 🚨 REGRAS CRÍTICAS DE GIT E COMMITS

**BRANCH:**
- ✅ **Executar no branch ativo** (qualquer branch: `main`, `dev`, `correcao/RF006`, etc.)
- ✅ **NÃO validar branch** (testes executam onde estiver)
- ✅ **NÃO fazer checkout** (manter branch atual)
- ❌ **NUNCA criar branches** para testes (ex: `feature/RFXXX-testes-completos`)

**JUSTIFICATIVA:**
- Testes devem validar o código NO ESTADO ATUAL do branch ativo
- Se em `main`: testa produção
- Se em `dev`: testa desenvolvimento
- Se em `correcao/RF006`: testa correção antes de merge
- Usuário é responsável por estar no branch correto

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

#### PASSO 1.1: Identificar Branch Ativo (Informativo)

```bash
# Apenas identificar branch atual (não validar)
CURRENT_BRANCH=$(git branch --show-current)
echo "ℹ️ Executando testes no branch: $CURRENT_BRANCH"
```

**IMPORTANTE:**
- ✅ Exibir branch ativo no início da execução
- ✅ Incluir branch no relatório final
- ❌ NÃO bloquear execução por causa do branch
- ❌ NÃO fazer checkout para outro branch

**Exemplos válidos:**
- `main` → Testa código em produção
- `dev` → Testa código em desenvolvimento
- `correcao/RF006` → Testa correção antes de merge
- `feature/RF010` → Testa nova funcionalidade

#### PASSO 1.2: Validar Pré-Requisitos (Documentação Obrigatória)

**⚠️ NÃO LER STATUS.yaml NESTA FASE** (será lido apenas na FASE 8)

**Ler e validar APENAS os seguintes arquivos de documentação:**

```bash
# 1. Estrutura do RF (leitura obrigatória)
Read D:\IC2_Governanca\documentacao\[Fase]\[EPIC]\[RF]\RF*.yaml

# 2. Massa de teste (leitura obrigatória - RAIZ DO RF)
Read D:\IC2_Governanca\documentacao\[Fase]\[EPIC]\[RF]\MT-RF*.yaml

# 3. Casos de teste (leitura obrigatória - RAIZ DO RF)
Read D:\IC2_Governanca\documentacao\[Fase]\[EPIC]\[RF]\TC-RF*.yaml

# 4. Schema SQL (validação de existência - NÃO ler conteúdo)
# Verificar existência: D:\IC2\backend\IControlIT.API\tests\schema.sql
# Validar tamanho > 10KB

# 5. Verificar arquivos de código (validação de existência)
# - D:\IC2\backend\IControlIT.API\IControlIT.API.sln
# - D:\IC2\frontend\icontrolit-app\package.json
```

**REGRA CRÍTICA: Leitura única**
- Arquivos RF*.yaml, MT-RF*.yaml, TC-RF*.yaml: Ler UMA ÚNICA VEZ
- Armazenar informações em memória para consultas posteriores
- NÃO re-ler arquivos já lidos

**Se schema.sql NÃO existir:**
```
⚠️ BLOQUEIO PARCIAL: schema.sql não encontrado

IMPACTO:
- ❌ Testes funcionais backend BLOQUEADOS (23 testes - Testcontainers dependency)
- ✅ Testes unitários backend PROSSEGUIRÃO normalmente (31 testes)
- ✅ Testes frontend PROSSEGUIRÃO normalmente
- ✅ Testes E2E PROSSEGUIRÃO normalmente

CONTEXTO TÉCNICO:
- Schema-First Testing: Testcontainers usa schema.sql em vez de EnsureCreatedAsync()
- Arquivo: tests/Application.FunctionalTests/SqlTestcontainersTestDatabase.cs
- Decisão arquitetural: ADR-005 (DECISIONS.md)

AÇÃO NECESSÁRIA (USUÁRIO - ANTES DE RE-EXECUTAR):
1. Exportar schema do Azure SQL DEV:
   sqlpackage /Action:Extract /SourceConnectionString:"..." /TargetFile:tests/schema.sql
2. Validar: arquivo > 10KB
3. Re-executar testes: prompts/testes/execucao-completa.md

RESPONSABILIDADE: INFRAESTRUTURA (não é erro de código)
TIPO: BLOQUEIO DE AMBIENTE (não gera prompt de correção)
```

**Se qualquer validação FALHAR:** BLOQUEIO TOTAL

#### PASSO 1.3: Verificar Ambiente (HEALTH CHECKS)

**🚨 REGRA CRÍTICA: VERIFICAR ANTES DE MATAR PROCESSOS**

**SEMPRE verificar se ambiente já está rodando ANTES de matar processos:**

```bash
# 1. Verificar backend
curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/health

# 2. Verificar frontend
curl -s -o /dev/null -w "%{http_code}" http://localhost:4200
```

**Cenário A: Ambos saudáveis (200 OK)**
- ✅ Backend: Status 200
- ✅ Frontend: Status 200
- ✅ **PULAR** PASSO 2.1 (não inicializar ambiente)
- ✅ Seguir direto para PASSO 1.4 (validar builds)

**Cenário B: Qualquer um falhou (não-200, timeout, connection refused)**
- ❌ Backend: Status != 200 OU timeout OU connection refused
- ❌ Frontend: Status != 200 OU timeout OU connection refused
- ✅ **MARCAR** para execução do PASSO 2.1 (inicializar ambiente com run.py)
- ✅ **NÃO matar processos manualmente** (run.py cuida disso automaticamente)

**Justificativa:**
- Economiza ~60 segundos quando ambiente já está rodando
- Evita duplicação (run.py já mata processos antes de iniciar)
- Evita matar backend saudável desnecessariamente

---

#### PASSO 1.4: Validar Builds

```bash
# Backend
cd backend/IControlIT.API
dotnet build --no-incremental

# Frontend
cd frontend/icontrolit-app
npm run build
```

**Se QUALQUER build FALHAR:** BLOQUEIO TOTAL (PARAR, REPORTAR, BLOQUEAR)

---

#### PASSO 1.5: Criar TODO List (APÓS Validação Completa)

**✅ SOMENTE APÓS TODOS OS PRÉ-REQUISITOS VALIDADOS:**

Criar TODO list com as seguintes tarefas:

```markdown
1. [ ] Validar pré-requisitos obrigatórios (backend, frontend, MT, TC)
2. [ ] Executar build do backend (dotnet build)
3. [ ] Executar build do frontend (npm run build)
4. [ ] Iniciar ambiente completo (backend + frontend) via run.py
5. [ ] Validar health checks (backend /health e frontend localhost:4200)
6. [ ] Executar testes backend (dotnet test)
7. [ ] Executar testes frontend (npm run test)
8. [ ] Verificar existência de specs Playwright para RF
9. [ ] Executar testes E2E Playwright (npm run e2e)
10. [ ] Executar testes de segurança (SQL Injection, XSS, CSRF)
11. [ ] Consolidar resultados e gerar relatório final
12. [ ] Gerar evidências (screenshots, logs, traces)
13. [ ] Atualizar STATUS.yaml com resultado final
```

**🚨 SE ALGUM PRÉ-REQUISITO FALHAR:**
- ❌ **NÃO** criar TODO list
- ❌ **PARAR** execução imediatamente
- ❌ **REPORTAR** gap em `.temp_ia/BLOQUEIO-EXECUCAO-RF*-[DATA].md`
- ✅ Informar ao usuário qual pré-requisito falhou e ação necessária

**Justificativa:** TODO list criada prematuramente fica obsoleta se pré-requisitos falharem.

---

### FASE 2: SETUP DE AMBIENTE (AUTOMÁTICO)

#### PASSO 2.1: Inicializar Ambiente (CONDICIONAL)

**REGRA:** Verificação de ambiente já foi feita no PASSO 1.3 (FASE 1)

**Executar inicialização SOMENTE se:**
- PASSO 1.3 Cenário B foi detectado (health checks falharam), OU
- Testes subsequentes (FASE 3/4/5) falharem com erros de ambiente

**SE durante FASE 3/4/5 ocorrerem erros que CLARAMENTE indicam problema de ambiente:**
- ❌ Conexão recusada (backend/frontend)
- ❌ Timeout em requisições HTTP
- ❌ "Cannot connect to database"
- ❌ "Port already in use" seguido de falhas
- ❌ Erros de autenticação que não existiam antes

**ENTÃO:**
- ✅ **REINICIAR** ambiente completo (executar PASSO 2.1)
- ✅ **RE-EXECUTAR** bateria de testes que falhou
- ✅ Documentar reinicialização no relatório final

**Inicialização:**

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

---

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

---

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

---

#### PASSO 2.4: Validação de Health (AUTOMÁTICO via run.py v2.0)

**✅ MUDANÇA CRÍTICA: run.py v2.0 valida health automaticamente**

O script `python D:\IC2\run.py` agora valida automaticamente que backend e frontend estão 100% prontos antes de retornar:

**Comportamento do run.py v2.0:**
- ✅ Mata processos anteriores (dotnet, node)
- ✅ Inicia backend em background (porta 5000)
- ✅ Inicia frontend em background (porta 4200)
- ✅ **Valida health do backend com retry (timeout: 60s, intervalo: 5s)**
- ✅ **Valida health do frontend com retry (timeout: 120s, intervalo: 5s)**
- ✅ **Retorna exit code 0 SOMENTE quando AMBOS estão 200 OK**
- ❌ **Retorna exit code 1 se timeout ou falha**

**Exemplo de saída:**
```
============================================================
  IControlIT - Gerenciador de Desenvolvimento v2.0
============================================================

[1/4] Matando processos existentes...
  ✓ Processos finalizados
  ✓ Portas liberadas

[2/4] Iniciando backend...
  ✓ Backend iniciado em background (porta 5000)

[3/4] Iniciando frontend...
  ✓ Frontend iniciado em background (porta 4200)

[4/4] Validando ambiente...

  Backend (http://localhost:5000/health):
    ⏳ Aguardando... (tentativa 1, 0s/60s)
    ⏳ Aguardando... (tentativa 2, 5s/60s)
    ✓ Backend PRONTO (tentativa 3, 10s)

  Frontend (http://localhost:4200):
    ⏳ Aguardando compilação Angular... (tentativa 1, 0s/120s)
    ⏳ Aguardando compilação Angular... (tentativa 5, 20s/120s)
    ✓ Frontend PRONTO (tentativa 11, 50s)

============================================================
  ✓ AMBIENTE PRONTO

  Backend:  http://localhost:5000/health (200 OK)
  Frontend: http://localhost:4200 (200 OK)
============================================================
```

**Regra de execução:**
```bash
# Executar run.py (já valida health automaticamente)
python D:\IC2\run.py

# Verificar exit code
if [ $? -eq 0 ]; then
  echo "✅ Ambiente pronto, prosseguir para testes"
else
  echo "❌ Ambiente com falhas, BLOQUEAR execução de testes"
  exit 1
fi
```

**PROIBIDO:**
- ❌ Adicionar validações manuais de health após run.py
- ❌ Adicionar sleep manual após run.py
- ❌ Assumir que ambiente está pronto sem verificar exit code

**REGRA FINAL:**
- ✅ Executar `python D:\IC2\run.py`
- ✅ Validar exit code (0 = sucesso, 1 = falha)
- ✅ Prosseguir para testes SOMENTE se exit code = 0

---

### FASE 3: TESTES BACKEND (Prioridade 1)

#### 🚨 REGRA CRÍTICA: NÃO PARAR NA PRIMEIRA FALHA

**OBRIGATÓRIO:** Executar TODOS os testes backend, mesmo se alguns falharem.
**PROIBIDO:** Abortar após primeira falha.
**OBJETIVO:** Identificar TODOS os erros de uma vez para correção única.

#### PASSO 3.1: Executar Testes Backend

```bash
cd backend/IControlIT.API
dotnet test --verbosity normal
```

**Comportamento esperado:**
- ✅ Executar TODOS os projetos de teste (Domain.UnitTests, Application.UnitTests, Application.FunctionalTests)
- ✅ Registrar TODOS os testes que falharam
- ✅ NÃO abortar se alguns testes falharem
- ✅ Continuar para FASE 4 (frontend) independentemente do resultado

#### ℹ️ CONTEXTO: Comportamento Esperado dos Testes Funcionais

**COM Docker rodando:**
```
✅ Domain.UnitTests: 5/5 testes passam (fast)
✅ Application.UnitTests: 26/26 testes passam (fast)
✅ Application.FunctionalTests: 23/23 testes passam (slow - Testcontainers)
   - Testcontainers baixa imagem SQL Server (primeira vez: ~1.5GB)
   - Testcontainers cria container efêmero
   - Testes executam contra SQL Server real
   - Container é destruído automaticamente
   - Tempo estimado: 30-60s (primeira execução), 10-20s (subsequentes)

Total: 54/54 testes
```

**SEM Docker rodando:**
```
✅ Domain.UnitTests: 5/5 testes passam (fast)
✅ Application.UnitTests: 26/26 testes passam (fast)
❌ Application.FunctionalTests: 0/23 testes executados (SKIP - Docker não disponível)
   - Testcontainers tenta conectar ao Docker
   - Falha: "Docker not found" ou similar
   - 23 testes PULADOS (não é falha de código)

Total: 31/54 testes (23 bloqueados por infraestrutura)
```

**IMPORTANTE:**
- Testes funcionais pulados NÃO são erro de código
- Docker ausente = BLOQUEIO DE INFRAESTRUTURA
- Taxa de aprovação será < 100%, mas NÃO gera prompt de correção
- Resultado: `BLOQUEADO_INFRAESTRUTURA` (não `REPROVADO`)

#### PASSO 3.2: Registrar Resultados

- ✅ Testes unitários passaram (Domain: 5, Application: 26)
- ✅ Testes funcionais passaram (Application.FunctionalTests: 23) **OU** ⚠️ Bloqueados (Docker ausente)
- ✅ Backend rejeita payloads inválidos (se funcionais executaram)

**Resultado:** PASS/FAIL/BLOCKED

#### PASSO 3.3: PRINTS OBRIGATÓRIOS (v2.3 - 2026-01-31)

**REGRA:** Durante execução dos testes backend, o agente DEVE exibir PRINTs estruturados confirmando execução e resultados.

### Formato de PRINT de Início de Fase

```
═══════════════════════════════════════════════════════════════
📋 FASE 3: TESTES BACKEND
═══════════════════════════════════════════════════════════════
RF: RFXXX
Data/Hora: 2026-01-31 15:23:45
Comando: cd backend/IControlIT.API && dotnet test --verbosity normal
Log: D:\IC2\.temp_ia\EVIDENCIAS-BACKEND-RFXXX.log
───────────────────────────────────────────────────────────────
```

### Formato de PRINT Durante Execução

O agente DEVE exibir os resultados do `dotnet test` em tempo real, incluindo:

```
🧪 EXECUTANDO: Domain.UnitTests
  ✅ ValidarCNPJ_ComDigitosCorretos_DeveRetornarTrue (0.1s)
  ✅ ValidarCNPJ_ComDigitosIncorretos_DeveRetornarFalse (0.1s)
  ✅ ValidarCPF_ComDigitosCorretos_DeveRetornarTrue (0.1s)
  ✅ ValidarCPF_ComDigitosIncorretos_DeveRetornarFalse (0.1s)
  ✅ ValidarEmail_ComFormatoValido_DeveRetornarTrue (0.05s)
───────────────────────────────────────────────────────────────
📊 Domain.UnitTests: 5/5 PASS (0.35s)

🧪 EXECUTANDO: Application.UnitTests
  ✅ CreateEmpresaCommand_ComDadosValidos_DeveRetornarSucesso (0.2s)
  ✅ CreateEmpresaCommand_SemCNPJ_DeveRetornarErro (0.15s)
  ✅ UpdateEmpresaCommand_ComDadosValidos_DeveRetornarSucesso (0.18s)
  ...
───────────────────────────────────────────────────────────────
📊 Application.UnitTests: 26/26 PASS (4.5s)

🧪 EXECUTANDO: Application.FunctionalTests
  ⏳ Inicializando Testcontainers... (SQL Server)
  ✅ CreateEmpresa_Integration_DeveInserirNoBanco (2.1s)
  ✅ UpdateEmpresa_Integration_DeveAtualizarNoBanco (1.8s)
  ...
───────────────────────────────────────────────────────────────
📊 Application.FunctionalTests: 23/23 PASS (35.2s)
```

### Formato de PRINT de Resumo de Fase

```
═══════════════════════════════════════════════════════════════
📊 RESUMO: FASE 3 - TESTES BACKEND
═══════════════════════════════════════════════════════════════
Total de testes: 54
✅ Aprovados: 54 (100%)
❌ Reprovados: 0 (0%)
⏭️ Pulados: 0 (0%)
⚠️ Bloqueados: 0 (0%)
Tempo total: 40.05s
Evidências: D:\IC2\.temp_ia\EVIDENCIAS-BACKEND-RFXXX.log
Status da fase: ✅ APROVADO
═══════════════════════════════════════════════════════════════
```

### Comando de Execução Atualizado

```bash
# Criar diretório de evidências se não existir
mkdir -p D:/IC2/.temp_ia/

# Definir nome do arquivo de log
LOG_FILE="D:/IC2/.temp_ia/EVIDENCIAS-BACKEND-RFXXX.log"

# PRINT de início
echo "═══════════════════════════════════════════════════════════════"
echo "📋 FASE 3: TESTES BACKEND"
echo "═══════════════════════════════════════════════════════════════"
echo "RF: RFXXX"
echo "Data/Hora: $(date +"%Y-%m-%d %H:%M:%S")"
echo "Log: $LOG_FILE"
echo "───────────────────────────────────────────────────────────────"

# Executar testes e salvar log
cd backend/IControlIT.API
dotnet test --verbosity normal 2>&1 | tee "$LOG_FILE"

# Calcular resumo
TOTAL=$(grep -c "Passed\|Failed\|Skipped" "$LOG_FILE" || echo "0")
PASSED=$(grep -c "Passed" "$LOG_FILE" || echo "0")
FAILED=$(grep -c "Failed" "$LOG_FILE" || echo "0")
SKIPPED=$(grep -c "Skipped" "$LOG_FILE" || echo "0")

# PRINT de resumo
echo "═══════════════════════════════════════════════════════════════"
echo "📊 RESUMO: FASE 3 - TESTES BACKEND"
echo "═══════════════════════════════════════════════════════════════"
echo "Total de testes: $TOTAL"
echo "✅ Aprovados: $PASSED"
echo "❌ Reprovados: $FAILED"
echo "⏭️ Pulados: $SKIPPED"
echo "Evidências: $LOG_FILE"
if [ "$FAILED" -eq 0 ]; then
  echo "Status da fase: ✅ APROVADO"
else
  echo "Status da fase: ❌ REPROVADO"
fi
echo "═══════════════════════════════════════════════════════════════"
```

### Validação de Evidências

```bash
# Validar que arquivo de log foi gerado
if [ ! -f "$LOG_FILE" ]; then
  echo "❌ ERRO: Arquivo de evidências backend não foi gerado"
  exit 1
fi

# Validar que arquivo não está vazio
if [ ! -s "$LOG_FILE" ]; then
  echo "❌ ERRO: Arquivo de evidências backend está vazio"
  exit 1
fi

echo "✅ Evidências backend registradas: $LOG_FILE"
```

---

### FASE 4: TESTES FRONTEND (Prioridade 2)

#### 🚨 REGRA CRÍTICA: NÃO PARAR NA PRIMEIRA FALHA

**OBRIGATÓRIO:** Executar TODOS os testes frontend, mesmo se alguns falharem.
**PROIBIDO:** Abortar após primeira falha.
**OBJETIVO:** Identificar TODOS os erros de uma vez para correção única.

#### PASSO 4.1: Executar Testes Frontend

```bash
cd frontend/icontrolit-app
npm run test
```

**Comportamento esperado:**
- ✅ Executar TODOS os specs (.spec.ts)
- ✅ Registrar TODOS os testes que falharam
- ✅ NÃO abortar se alguns testes falharem
- ✅ Continuar para FASE 5 (E2E) independentemente do resultado

#### PASSO 4.2: Registrar Resultados

- ✅ Testes unitários passaram
- ✅ Testes de componentes passaram
- ✅ Testes de serviços passaram
- ✅ Validações de formulário funcionando

**Resultado:** PASS/FAIL

#### PASSO 4.3: PRINTS OBRIGATÓRIOS (v2.3 - 2026-01-31)

**REGRA:** Durante execução dos testes frontend, o agente DEVE exibir PRINTs estruturados confirmando execução e resultados.

### Formato de PRINT de Início de Fase

```
═══════════════════════════════════════════════════════════════
📋 FASE 4: TESTES FRONTEND
═══════════════════════════════════════════════════════════════
RF: RFXXX
Data/Hora: 2026-01-31 15:24:30
Comando: cd frontend/icontrolit-app && npm run test
Log: D:\IC2\.temp_ia\EVIDENCIAS-FRONTEND-RFXXX.log
───────────────────────────────────────────────────────────────
```

### Formato de PRINT Durante Execução

O agente DEVE exibir os resultados do `npm run test` em tempo real, incluindo:

```
🧪 EXECUTANDO: app.component.spec.ts
  ✅ should create the app (0.05s)
  ✅ should have title 'IControlIT' (0.03s)
───────────────────────────────────────────────────────────────
📊 app.component.spec.ts: 2/2 PASS (0.08s)

🧪 EXECUTANDO: login/login.component.spec.ts
  ✅ should create (0.12s)
  ✅ should validate email format (0.08s)
  ✅ should validate required fields (0.06s)
  ✅ should emit loginSuccess on valid submit (0.15s)
───────────────────────────────────────────────────────────────
📊 login.component.spec.ts: 4/4 PASS (0.41s)

🧪 EXECUTANDO: services/auth.service.spec.ts
  ✅ should be created (0.05s)
  ✅ should store token on successful login (0.12s)
  ✅ should clear token on logout (0.08s)
  ✅ should return user from token (0.10s)
───────────────────────────────────────────────────────────────
📊 auth.service.spec.ts: 4/4 PASS (0.35s)
```

### Formato de PRINT de Resumo de Fase

```
═══════════════════════════════════════════════════════════════
📊 RESUMO: FASE 4 - TESTES FRONTEND
═══════════════════════════════════════════════════════════════
Total de testes: 30
✅ Aprovados: 30 (100%)
❌ Reprovados: 0 (0%)
⏭️ Pulados: 0 (0%)
Tempo total: 5.2s
Evidências: D:\IC2\.temp_ia\EVIDENCIAS-FRONTEND-RFXXX.log
Status da fase: ✅ APROVADO
═══════════════════════════════════════════════════════════════
```

### Comando de Execução Atualizado

```bash
# Criar diretório de evidências se não existir
mkdir -p D:/IC2/.temp_ia/

# Definir nome do arquivo de log
LOG_FILE="D:/IC2/.temp_ia/EVIDENCIAS-FRONTEND-RFXXX.log"

# PRINT de início
echo "═══════════════════════════════════════════════════════════════"
echo "📋 FASE 4: TESTES FRONTEND"
echo "═══════════════════════════════════════════════════════════════"
echo "RF: RFXXX"
echo "Data/Hora: $(date +"%Y-%m-%d %H:%M:%S")"
echo "Log: $LOG_FILE"
echo "───────────────────────────────────────────────────────────────"

# Executar testes e salvar log
cd frontend/icontrolit-app
npm run test 2>&1 | tee "$LOG_FILE"

# Calcular resumo
TOTAL=$(grep -c "PASS\|FAIL" "$LOG_FILE" || echo "0")
PASSED=$(grep -c "PASS" "$LOG_FILE" || echo "0")
FAILED=$(grep -c "FAIL" "$LOG_FILE" || echo "0")

# PRINT de resumo
echo "═══════════════════════════════════════════════════════════════"
echo "📊 RESUMO: FASE 4 - TESTES FRONTEND"
echo "═══════════════════════════════════════════════════════════════"
echo "Total de testes: $TOTAL"
echo "✅ Aprovados: $PASSED"
echo "❌ Reprovados: $FAILED"
echo "Evidências: $LOG_FILE"
if [ "$FAILED" -eq 0 ]; then
  echo "Status da fase: ✅ APROVADO"
else
  echo "Status da fase: ❌ REPROVADO"
fi
echo "═══════════════════════════════════════════════════════════════"
```

### Validação de Evidências

```bash
# Validar que arquivo de log foi gerado
if [ ! -f "$LOG_FILE" ]; then
  echo "❌ ERRO: Arquivo de evidências frontend não foi gerado"
  exit 1
fi

# Validar que arquivo não está vazio
if [ ! -s "$LOG_FILE" ]; then
  echo "❌ ERRO: Arquivo de evidências frontend está vazio"
  exit 1
fi

echo "✅ Evidências frontend registradas: $LOG_FILE"
```

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

#### 🚨 PASSO 5.2: SE SPECS NÃO EXISTEM OU INCOMPLETOS → BLOQUEIO TOTAL E REPROVAÇÃO IMEDIATA

**⚠️ REGRA INVIOLÁVEL (v1.3 - 2026-01-28):**

**SE specs não existem ou cobertura < 100%:**

**O agente DEVE OBRIGATORIAMENTE:**

1. **REPROVAR IMEDIATAMENTE** - NÃO prosseguir para testes E2E
2. **ATRIBUIR RESPONSABILIDADE** ao agente de geração E2E
3. **GERAR PROMPT DE CORREÇÃO** para o usuário executar

**MENSAGEM DE REPROVAÇÃO OBRIGATÓRIA:**
```
❌ REPROVADO - SPECS PLAYWRIGHT NÃO EXISTEM

BLOQUEIO TOTAL: Testes E2E não podem ser executados.

DIAGNÓSTICO:
- Pasta e2e/specs/RFXXX/ não existe ou está incompleta
- Cobertura de specs: 0% (esperado: 100%)
- TC-E2E definidos em TC-RFXXX.yaml: [N] casos
- Specs Playwright encontrados: 0

RESPONSABILIDADE: AGENTE DE GERAÇÃO E2E

O agente de criação de TC/MT (mt-tc-criacao.md) criou os casos de teste
(TC-RFXXX.yaml), mas os specs Playwright (.spec.ts) não foram gerados.

AÇÃO NECESSÁRIA:
Execute o prompt de geração de specs E2E:

═══════════════════════════════════════════════════════════════════════
Para o RF[XXX] [CAMINHO_COMPLETO_RF] execute o
D:\IC2_Governanca\governanca\prompts\testes\geracao-e2e-playwright.md
═══════════════════════════════════════════════════════════════════════

APÓS gerar specs, re-execute este contrato de testes.

RESULTADO: REPROVADO
STATUS.yaml: testes_ti.resultado_final = "REPROVADO"
STATUS.yaml: testes_ti.motivo_reprovacao = "SPECS_E2E_AUSENTES"
```

**PROIBIÇÕES ABSOLUTAS:**
- ❌ **NUNCA** aprovar sem specs E2E (VIOLAÇÃO GRAVE)
- ❌ **NUNCA** pular validação de specs (VIOLAÇÃO GRAVE)
- ❌ **NUNCA** assumir que "smoke test é opcional" (FALSO)
- ❌ **NUNCA** continuar para FASE 6 sem specs 100%
- ❌ **NUNCA** marcar testes_ti.resultado_final como "APROVADO" sem specs

**SE agente tentar aprovar sem specs:**
- Execução é **INVÁLIDA**
- Aprovação é **NULA**
- Usuário DEVE re-executar após gerar specs

**AUTO-GERAÇÃO (OPCIONAL - APÓS REPROVAÇÃO):**

SE o agente tiver capacidade de gerar specs (mesma sessão):

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
4. **SE geração falhar:** REPROVAR (não continuar)

**REGRA CRÍTICA FINAL:**
- ❌ NÃO executar testes E2E sem specs completos
- ❌ NÃO pular validação de specs
- ❌ NÃO aprovar com 0% de specs
- ✅ SEMPRE reprovar se specs ausentes
- ✅ SEMPRE atribuir responsabilidade clara
- ✅ SEMPRE gerar prompt de correção para usuário

#### PASSO 5.3: Executar Testes E2E

#### 🚨 REGRA CRÍTICA: NÃO PARAR NA PRIMEIRA FALHA

**OBRIGATÓRIO:** Executar TODOS os testes E2E, mesmo se alguns falharem.
**PROIBIDO:** Abortar após primeira falha.
**OBJETIVO:** Identificar TODOS os erros de uma vez para correção única.

```bash
cd frontend/icontrolit-app
npm run e2e
```

**Comportamento esperado:**
- ✅ Executar TODAS as specs Playwright
- ✅ Registrar TODOS os testes que falharam
- ✅ NÃO abortar se alguns testes falharem
- ✅ Continuar para FASE 6 (Segurança) independentemente do resultado

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

#### PASSO 5.7.1: PRINTS OBRIGATÓRIOS (v2.3 - 2026-01-31)

**REGRA:** Durante execução dos testes E2E, o agente DEVE exibir PRINTs estruturados confirmando execução e resultados.

### Formato de PRINT de Início de Fase

```
═══════════════════════════════════════════════════════════════
📋 FASE 5: TESTES E2E (PLAYWRIGHT)
═══════════════════════════════════════════════════════════════
RF: RFXXX
Data/Hora: 2026-01-31 15:25:15
Comando: cd frontend/icontrolit-app && npm run e2e
Log: D:\IC2\.temp_ia\EVIDENCIAS-E2E-RFXXX.log
Specs: e2e/specs/RFXXX/
───────────────────────────────────────────────────────────────
```

### Formato de PRINT Durante Execução

O agente DEVE exibir os resultados do Playwright em tempo real, incluindo:

```
🧪 EXECUTANDO: TC-RF007-E2E-001.spec.ts - Login com credenciais válidas
───────────────────────────────────────────────────────────────
[Chromium] Login com credenciais válidas
  ✅ Deve exibir formulário de login (0.5s)
  ✅ Deve aceitar credenciais válidas (1.2s)
  ✅ Deve redirecionar para dashboard (0.8s)
  ✅ Deve exibir nome do usuário logado (0.3s)
───────────────────────────────────────────────────────────────
📊 TC-RF007-E2E-001.spec.ts: 4/4 PASS (2.8s)
📸 Screenshots: e2e/screenshots/TC-RF007-E2E-001/
🎬 Video: e2e/videos/TC-RF007-E2E-001.webm
📝 Trace: e2e/traces/TC-RF007-E2E-001.zip

🧪 EXECUTANDO: TC-RF007-E2E-002.spec.ts - Login com credenciais inválidas
───────────────────────────────────────────────────────────────
[Chromium] Login com credenciais inválidas
  ✅ Deve exibir erro de credenciais incorretas (1.0s)
  ✅ Deve manter usuário na tela de login (0.4s)
  ✅ Deve limpar campo de senha (0.2s)
───────────────────────────────────────────────────────────────
📊 TC-RF007-E2E-002.spec.ts: 3/3 PASS (1.6s)
📸 Screenshots: e2e/screenshots/TC-RF007-E2E-002/
🎬 Video: e2e/videos/TC-RF007-E2E-002.webm
📝 Trace: e2e/traces/TC-RF007-E2E-002.zip

🧪 EXECUTANDO: TC-RF007-E2E-003.spec.ts - Logout
───────────────────────────────────────────────────────────────
[Chromium] Logout
  ✅ Deve fazer login primeiro (1.1s)
  ✅ Deve clicar em menu de usuário (0.3s)
  ✅ Deve clicar em logout (0.4s)
  ✅ Deve redirecionar para tela de login (0.6s)
  ❌ Deve limpar token do localStorage (0.2s)
     Error: expected '' but got 'eyJhbGc...'
     at logout.spec.ts:45:11
───────────────────────────────────────────────────────────────
📊 TC-RF007-E2E-003.spec.ts: 4/5 FAIL (2.6s)
📸 Screenshots: e2e/screenshots/TC-RF007-E2E-003/
🎬 Video: e2e/videos/TC-RF007-E2E-003.webm
📝 Trace: e2e/traces/TC-RF007-E2E-003.zip
❌ RESPONSABILIDADE: FRONTEND (auth.service.ts - método logout)
```

### Formato de PRINT de Resumo de Fase

```
═══════════════════════════════════════════════════════════════
📊 RESUMO: FASE 5 - TESTES E2E
═══════════════════════════════════════════════════════════════
Total de specs: 15
Total de testes: 45
✅ Aprovados: 43 (95.6%)
❌ Reprovados: 2 (4.4%)
⏭️ Pulados: 0 (0%)
Tempo total: 2m 15s
Evidências: D:\IC2\.temp_ia\EVIDENCIAS-E2E-RFXXX.log
Screenshots: frontend/icontrolit-app/e2e/screenshots/
Videos: frontend/icontrolit-app/e2e/videos/
Traces: frontend/icontrolit-app/e2e/traces/
Status da fase: ❌ REPROVADO (2 falhas)
───────────────────────────────────────────────────────────────
Falhas identificadas:
  1. TC-RF007-E2E-003: Token não limpo no logout (FRONTEND)
  2. TC-RF007-E2E-012: Lista não atualiza após criar (FRONTEND)
═══════════════════════════════════════════════════════════════
```

### Comando de Execução Atualizado

```bash
# Criar diretório de evidências se não existir
mkdir -p D:/IC2/.temp_ia/

# Definir nome do arquivo de log
LOG_FILE="D:/IC2/.temp_ia/EVIDENCIAS-E2E-RFXXX.log"

# PRINT de início
echo "═══════════════════════════════════════════════════════════════"
echo "📋 FASE 5: TESTES E2E (PLAYWRIGHT)"
echo "═══════════════════════════════════════════════════════════════"
echo "RF: RFXXX"
echo "Data/Hora: $(date +"%Y-%m-%d %H:%M:%S")"
echo "Log: $LOG_FILE"
echo "Specs: e2e/specs/RFXXX/"
echo "───────────────────────────────────────────────────────────────"

# Executar testes E2E e salvar log
cd frontend/icontrolit-app
npx playwright test 2>&1 | tee "$LOG_FILE"

# Calcular resumo
TOTAL_SPECS=$(find e2e/specs/RFXXX/ -name "*.spec.ts" | wc -l)
PASSED=$(grep -c "✓" "$LOG_FILE" || echo "0")
FAILED=$(grep -c "✘" "$LOG_FILE" || echo "0")

# PRINT de resumo
echo "═══════════════════════════════════════════════════════════════"
echo "📊 RESUMO: FASE 5 - TESTES E2E"
echo "═══════════════════════════════════════════════════════════════"
echo "Total de specs: $TOTAL_SPECS"
echo "✅ Aprovados: $PASSED"
echo "❌ Reprovados: $FAILED"
echo "Evidências: $LOG_FILE"
echo "Screenshots: $(pwd)/e2e/screenshots/"
echo "Videos: $(pwd)/e2e/videos/"
echo "Traces: $(pwd)/e2e/traces/"
if [ "$FAILED" -eq 0 ]; then
  echo "Status da fase: ✅ APROVADO"
else
  echo "Status da fase: ❌ REPROVADO ($FAILED falhas)"
fi
echo "═══════════════════════════════════════════════════════════════"
```

### Validação de Evidências

```bash
# Validar que arquivo de log foi gerado
if [ ! -f "$LOG_FILE" ]; then
  echo "❌ ERRO: Arquivo de evidências E2E não foi gerado"
  exit 1
fi

# Validar que arquivo não está vazio
if [ ! -s "$LOG_FILE" ]; then
  echo "❌ ERRO: Arquivo de evidências E2E está vazio"
  exit 1
fi

# Validar que screenshots foram gerados
if [ ! -d "e2e/screenshots/" ]; then
  echo "⚠️ AVISO: Pasta de screenshots não foi criada"
fi

echo "✅ Evidências E2E registradas: $LOG_FILE"
```

---

#### PASSO 5.8: TESTES STATEFUL - VALIDAÇÃO DE PERSISTÊNCIA

**🆕 ADICIONADO:** 2026-01-11 (Resolve problema RF006 - banco resetado entre testes)

**Quando usar:**
- ✅ Testes que validam fluxo CRUD completo (Criar → Listar → Editar → Excluir)
- ✅ Testes que compartilham estado entre múltiplos passos
- ✅ Testes que validam persistência de dados

**Referência obrigatória:**
```
D:\IC2_Governanca\governanca\contracts\testes\CONTRATO-TESTES-E2E-STATEFUL.md
```

**Validação pré-execução:**

```bash
# 1. Verificar configuração Playwright
cat D:\IC2\frontend\icontrolit-app\playwright.config.ts | grep -E "workers|fullyParallel|retries"

# Esperado:
#   workers: 1
#   fullyParallel: false
#   retries: 0
```

**Checklist obrigatório:**
- [ ] `playwright.config.ts` com `workers: 1` e `fullyParallel: false`
- [ ] `test.describe.serial` usado para fluxos CRUD
- [ ] Backend **NÃO reseta** banco a cada request
- [ ] Dados criados no Passo 1 **visíveis** no Passo 2

**Se dados NÃO persistem entre testes:**

```yaml
Diagnóstico:
  1. Verificar D:\IC2\backend\IControlIT.API\src\Web\Program.cs
  2. Confirmar que InitialiseDatabaseAsync() executa apenas no startup
  3. Verificar ApplicationDbContextInitialiser.cs (NÃO deve ter EnsureDeletedAsync)
  4. Validar que backend não está reiniciando entre testes

Responsável: Backend + DevOps
Exit Code: 2 (falha de configuração, não de lógica)
```

**Referência completa:** Ver `CONTRATO-TESTES-E2E-STATEFUL.md` seções 2-7 para detalhes de implementação, fixtures do Playwright, e resolução de problemas.

---

#### PASSO 5.9: VALIDAR COBERTURA 100% DE TCs (NOVO - BLOQUEANTE)

**🆕 ADICIONADO:** 2026-01-11 (Resolve problema RF006 - apenas 25% dos TCs executados)

**Contexto:**
Durante execução #9 do RF006, identificou-se que apenas **8 de 32 TCs (25%)** foram executados, deixando **75% não testado**. Categorias inteiras (SEGURANCA, EDGE_CASE, AUDITORIA, INTEGRACAO) não foram testadas.

**Objetivo:**
Garantir que **100% dos TCs** especificados em TC-RFXXX.yaml sejam executados, sem exceção.

**Método de Validação:**

```python
#!/usr/bin/env python3
# validate-tc-coverage.py

import yaml
import glob
import sys

def validar_cobertura_tc(rf_numero):
    """
    Valida que 100% dos TCs de TC-RFXXX.yaml foram executados.

    Returns:
        0: Cobertura 100% (APROVADO)
        1: Cobertura < 100% (REPROVADO)
    """

    # 1. Ler TC-RFXXX.yaml
    tc_file = f"D:\\IC2_Governanca\\documentos\\testes\\TC-RF{rf_numero}.yaml"

    with open(tc_file, 'r', encoding='utf-8') as f:
        tc_yaml = yaml.safe_load(f)

    casos_teste_yaml = tc_yaml.get('casos_teste', [])
    total_tcs_yaml = len(casos_teste_yaml)

    # 2. Mapear TCs por categoria
    tcs_por_categoria = {}
    for tc in casos_teste_yaml:
        categoria = tc.get('categoria', 'UNKNOWN')
        if categoria not in tcs_por_categoria:
            tcs_por_categoria[categoria] = []
        tcs_por_categoria[categoria].append(tc['id'])

    # 3. Contar specs Playwright executados
    e2e_dir = f"D:\\IC2\\frontend\\icontrolit-app\\e2e\\specs"
    spec_pattern = f"TC-RF{rf_numero}-*.spec.ts"
    spec_files = glob.glob(f"{e2e_dir}\\{spec_pattern}")

    total_specs_executados = len(spec_files)

    # 4. Validar cobertura 100%
    if total_specs_executados < total_tcs_yaml:
        print(f"❌ COBERTURA INCOMPLETA")
        print(f"   TCs especificados (TC-RF{rf_numero}.yaml): {total_tcs_yaml}")
        print(f"   Specs Playwright executados: {total_specs_executados}")
        print(f"   Cobertura: {(total_specs_executados / total_tcs_yaml) * 100:.1f}%")
        print(f"   TCs NÃO TESTADOS: {total_tcs_yaml - total_specs_executados}")
        print()

        # Listar categorias não testadas
        print("Categorias por cobertura:")
        for categoria, tc_ids in tcs_por_categoria.items():
            total_cat = len(tc_ids)
            # Contar quantos specs dessa categoria existem
            specs_cat = glob.glob(f"{e2e_dir}\\TC-RF{rf_numero}-{categoria}-*.spec.ts")
            executados_cat = len(specs_cat)
            cobertura_cat = (executados_cat / total_cat) * 100 if total_cat > 0 else 0

            status = "✅" if cobertura_cat == 100 else "❌"
            print(f"  {status} {categoria}: {executados_cat}/{total_cat} ({cobertura_cat:.1f}%)")

            if cobertura_cat < 100:
                print(f"      TCs ausentes: {tc_ids[executados_cat:]}")

        print()
        print("Ação: Criar specs Playwright para TODOS os TCs ausentes")
        print("Referência: TC-RF{rf_numero}.yaml")
        return 1

    # Cobertura 100%
    print(f"✅ COBERTURA 100% DE TCs")
    print(f"   TCs especificados: {total_tcs_yaml}")
    print(f"   Specs executados: {total_specs_executados}")
    print(f"   Cobertura: 100%")
    print()
    print("Categorias testadas:")
    for categoria, tc_ids in tcs_por_categoria.items():
        print(f"  ✓ {categoria}: {len(tc_ids)}/{len(tc_ids)} (100%)")

    return 0

if __name__ == "__main__":
    rf = sys.argv[1] if len(sys.argv) > 1 else input("RF número: ")
    sys.exit(validar_cobertura_tc(rf))
```

**Execução obrigatória:**

```bash
cd D:\IC2_Governanca\tools
python validate-tc-coverage.py {RF_NUMERO}
```

**Critério de aprovação:**
- ✅ Cobertura: 100% (total_specs_executados == total_tcs_yaml)
- ✅ TODAS as categorias testadas (FUNCIONAL, EDGE_CASE, SEGURANCA, INTEGRACAO, AUDITORIA, etc.)
- ❌ Qualquer TC não testado = **REPROVADO** (bloqueante)

**Saída esperada (APROVADO):**
```
✅ COBERTURA 100% DE TCs
   TCs especificados: 32
   Specs executados: 32
   Cobertura: 100%

Categorias testadas:
  ✓ FUNCIONAL: 20/20 (100%)
  ✓ EDGE_CASE: 5/5 (100%)
  ✓ SEGURANCA: 3/3 (100%)
  ✓ INTEGRACAO: 2/2 (100%)
  ✓ AUDITORIA: 2/2 (100%)
```

**Saída esperada (REPROVADO):**
```
❌ COBERTURA INCOMPLETA
   TCs especificados (TC-RF006.yaml): 32
   Specs Playwright executados: 8
   Cobertura: 25.0%
   TCs NÃO TESTADOS: 24

Categorias por cobertura:
  ✅ FUNCIONAL: 8/20 (40%)
      TCs ausentes: ['TC-RF006-E2E-009', 'TC-RF006-E2E-010', ..., 'TC-RF006-E2E-020']
  ❌ EDGE_CASE: 0/5 (0%)
      TCs ausentes: ['TC-RF006-EDGE-001', 'TC-RF006-EDGE-002', ..., 'TC-RF006-EDGE-005']
  ❌ SEGURANCA: 0/3 (0%)
      TCs ausentes: ['TC-RF006-SEC-001', 'TC-RF006-SEC-002', 'TC-RF006-SEC-003']
  ❌ INTEGRACAO: 0/2 (0%)
      TCs ausentes: ['TC-RF006-INT-001', 'TC-RF006-INT-002']
  ❌ AUDITORIA: 0/2 (0%)
      TCs ausentes: ['TC-RF006-AUD-001', 'TC-RF006-AUD-002']

Ação: Criar specs Playwright para TODOS os TCs ausentes
Referência: TC-RF006.yaml
```

**Integração com EXECUTION-MANIFEST:**

```yaml
testes:
  e2e:
    cobertura_tc:
      total_tcs_yaml: 32
      total_specs_executados: 32
      cobertura: 100%
      categorias:
        FUNCIONAL: "20/20 (100%)"
        EDGE_CASE: "5/5 (100%)"
        SEGURANCA: "3/3 (100%)"
        INTEGRACAO: "2/2 (100%)"
        AUDITORIA: "2/2 (100%)"
      status: "✅ APROVADO"
```

**Ações se REPROVADO:**

1. **Identificar TCs ausentes:**
   - Comparar TC-RFXXX.yaml com specs em `e2e/specs/`
   - Listar categorias não testadas

2. **Criar specs ausentes:**
   - Para CADA TC ausente, criar spec Playwright correspondente
   - Seguir padrão: `TC-RFXXX-{CATEGORIA}-{NUMERO}.spec.ts`

3. **Re-executar validação:**
   - `python validate-tc-coverage.py {RF}`
   - Repetir até cobertura 100%

**Impacto esperado:**

Esta validação resolve **GAP 2 do RF006** (cobertura incompleta de TCs).

**Sem esta validação:**
- ❌ Apenas 25% dos TCs executados (RF006)
- ❌ Categorias inteiras não testadas (SEGURANCA, EDGE_CASE, AUDITORIA, INTEGRACAO)
- ❌ Falhas críticas não detectadas até produção
- ❌ Falsa sensação de segurança (8/32 testes OK ≠ produto OK)

**Com esta validação:**
- ✅ 100% dos TCs executados (obrigatório)
- ✅ TODAS as categorias testadas
- ✅ Falhas detectadas ANTES de produção
- ✅ Confiança real na qualidade do produto

**Referências:**
- Relatório de testes: `D:\IC2\.temp_ia\RELATORIO-TESTES-RF006-2026-01-11.md` (GAP 2)
- TC Template: `D:\IC2_Governanca\governanca\templates\TC-TEMPLATE.yaml`
- Problema identificado: RF006 execução #9 (apenas 25% de cobertura TC)

---

#### PASSO 5.10: Validar Isolamento de Testes E2E (BLOQUEANTE) ✨ NOVO

**Versão:** 1.0
**Data de Criação:** 2026-01-11
**Contexto:** Adicionado para validar que testes E2E seguem padrão correto (isolated vs stateful) e prevenir contaminação de estado.

**Objetivo:** Validar que testes E2E seguem padrão **isolated** (SE aplicável) ou **stateful** (SE aplicável), garantindo estrutura correta.

**EXECUTAR OBRIGATORIAMENTE:**

```bash
cd D:\IC2_Governanca\tools
python validate-isolated-tests.py {RF_NUMERO}
```

**O que este script valida:**

1. **SE tipo_teste = "ISOLATED":**
   - ✅ Nenhum uso de `test.describe.serial` (PROIBIDO em isolated)
   - ✅ TODOS os specs possuem `test.beforeEach`
   - ✅ TODOS os specs possuem `test.afterEach`
   - ✅ TODOS os specs chamam `closeAllOverlays()` (previne overlay persistente)
   - ✅ TODOS os specs usam Page Objects

2. **SE tipo_teste = "STATEFUL":**
   - ✅ Usa `test.describe.serial` (obrigatório em stateful)
   - ✅ Possui fixtures necessárias
   - ✅ TCs E2E possuem `usa_fixture: true` e `fixture_dependencia`
   - ✅ Sequência ordenada (1, 2, 3, 4)

**Implementação do script:**

```python
#!/usr/bin/env python3
"""
Valida que testes E2E seguem padrão isolated (não stateful)

Referência: CONTRATO-TESTES-E2E-ISOLADOS.md seção 5
"""

import os
import re
import sys
import glob
import yaml

def validar_testes_isolados(rf_numero):
    """
    Valida que specs do RF seguem padrão isolated
    """
    # 1. Ler TC-RFXXX.yaml para identificar tipo de teste
    tc_file = f"D:\\IC2_Governanca\\documentos\\testes\\TC-RF{rf_numero}.yaml"

    if not os.path.exists(tc_file):
        print(f"❌ TC-RF{rf_numero}.yaml não encontrado")
        return 1

    with open(tc_file, 'r', encoding='utf-8') as f:
        tc_yaml = yaml.safe_load(f)

    tipo_teste = tc_yaml.get('metadata', {}).get('tipo_teste', 'ISOLATED')

    print(f"🔍 Validando testes E2E do RF{rf_numero}")
    print(f"   Tipo de teste: {tipo_teste}")
    print()

    # 2. Localizar specs Playwright
    e2e_dir = "D:\\IC2\\frontend\\icontrolit-app\\e2e\\specs"
    spec_pattern = f"TC-RF{rf_numero}-*.spec.ts"
    spec_files = glob.glob(f"{e2e_dir}\\{spec_pattern}")

    if not spec_files:
        print(f"⚠️  Nenhum spec encontrado para RF{rf_numero} (pode não ter testes E2E)")
        return 0  # Não é erro se não tem testes E2E

    falhas = []

    # 3. Validar ISOLATED
    if tipo_teste == "ISOLATED":
        for spec_file in spec_files:
            with open(spec_file, 'r', encoding='utf-8') as f:
                conteudo = f.read()

            # 3.1. Validar que NÃO usa test.describe.serial
            if 'test.describe.serial' in conteudo:
                falhas.append(f"{os.path.basename(spec_file)}: Usa test.describe.serial (PROIBIDO em isolated)")

            # 3.2. Validar que possui beforeEach
            if 'test.beforeEach' not in conteudo:
                falhas.append(f"{os.path.basename(spec_file)}: Ausente test.beforeEach (OBRIGATÓRIO)")

            # 3.3. Validar que beforeEach chama closeAllOverlays
            if 'closeAllOverlays()' not in conteudo:
                falhas.append(f"{os.path.basename(spec_file)}: Ausente closeAllOverlays() (OBRIGATÓRIO)")

            # 3.4. Validar que possui afterEach
            if 'test.afterEach' not in conteudo:
                falhas.append(f"{os.path.basename(spec_file)}: Ausente test.afterEach (OBRIGATÓRIO)")

            # 3.5. Validar que usa Page Objects
            if 'Page' not in conteudo or 'import' not in conteudo:
                falhas.append(f"{os.path.basename(spec_file)}: Não usa Page Objects (OBRIGATÓRIO)")

    # 4. Validar STATEFUL
    elif tipo_teste == "STATEFUL":
        for spec_file in spec_files:
            with open(spec_file, 'r', encoding='utf-8') as f:
                conteudo = f.read()

            # 4.1. Validar que USA test.describe.serial
            if 'test.describe.serial' not in conteudo:
                falhas.append(f"{os.path.basename(spec_file)}: Deve usar test.describe.serial (OBRIGATÓRIO em stateful)")

            # 4.2. Validar que usa fixtures
            if 'test.use' not in conteudo and 'fixture' not in conteudo.lower():
                falhas.append(f"{os.path.basename(spec_file)}: Deve usar fixtures (stateful)")

    # 5. Resultado
    if falhas:
        print(f"❌ RF{rf_numero} NÃO segue padrão {tipo_teste}:")
        for falha in falhas:
            print(f"  - {falha}")
        print()
        print("Ação: Corrigir specs para seguir padrão correto")
        if tipo_teste == "ISOLATED":
            print("Referência: CONTRATO-TESTES-E2E-ISOLADOS.md")
        else:
            print("Referência: CONTRATO-TESTES-E2E-STATEFUL.md")
        return 1
    else:
        print(f"✅ RF{rf_numero} segue padrão {tipo_teste} corretamente")
        print(f"  - {len(spec_files)} specs validados")
        if tipo_teste == "ISOLATED":
            print(f"  - beforeEach/afterEach presentes")
            print(f"  - closeAllOverlays() implementado")
            print(f"  - Page Objects utilizados")
            print(f"  - Nenhum test.describe.serial encontrado")
        else:
            print(f"  - test.describe.serial utilizado corretamente")
            print(f"  - Fixtures configuradas")
        return 0

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python validate-isolated-tests.py <RF_NUMERO>")
        sys.exit(1)

    rf_numero = sys.argv[1]
    sys.exit(validar_testes_isolados(rf_numero))
```

**Critério de Aprovação:**

- ✅ Script retorna exit code 0
- ✅ TODOS os specs seguem padrão correto (isolated ou stateful)
- ✅ Nenhuma violação de estrutura

**SE validação FALHAR:**

1. **Identificar tipo de teste:**
   - Ler `TC-RFXXX.yaml` → `metadata.tipo_teste`

2. **SE ISOLATED:**
   - Remover `test.describe.serial` (usar `test.describe`)
   - Adicionar `test.beforeEach` com login + navigate + closeAllOverlays
   - Adicionar `test.afterEach` com closeAllOverlays + logout
   - Usar Page Objects
   - Referência: [CONTRATO-TESTES-E2E-ISOLADOS.md](CONTRATO-TESTES-E2E-ISOLADOS.md)

3. **SE STATEFUL:**
   - Usar `test.describe.serial` (obrigatório)
   - Configurar fixtures
   - Configurar playwright.config.ts (workers: 1, fullyParallel: false)
   - Referência: [CONTRATO-TESTES-E2E-STATEFUL.md](CONTRATO-TESTES-E2E-STATEFUL.md)

4. **Re-executar validação:**
   - `python validate-isolated-tests.py {RF}`
   - Repetir até aprovação

**Impacto esperado:**

Esta validação **previne problemas sistemáticos** de contaminação de estado em testes E2E.

**Sem esta validação:**
- ❌ Testes isolated usam test.describe.serial (causa dependências)
- ❌ Testes sem closeAllOverlays() (67% dos problemas RF006)
- ❌ Overlay/backdrop persistente entre testes
- ❌ Taxa de aprovação E2E: 10-60% (vs 95-100% esperado)

**Com esta validação:**
- ✅ Testes seguem padrão correto (isolated ou stateful)
- ✅ closeAllOverlays() obrigatório (previne overlay persistente)
- ✅ beforeEach/afterEach garantem isolamento
- ✅ Taxa de aprovação E2E: 95-100%

**Referências:**
- Contrato Isolated: [CONTRATO-TESTES-E2E-ISOLADOS.md](CONTRATO-TESTES-E2E-ISOLADOS.md)
- Contrato Stateful: [CONTRATO-TESTES-E2E-STATEFUL.md](CONTRATO-TESTES-E2E-STATEFUL.md)
- Checklist Isolated: [CHECKLIST-TESTES-E2E-ISOLADOS.yaml](../../checklists/testes/CHECKLIST-TESTES-E2E-ISOLADOS.yaml)
- Análise RF006: `D:\IC2\.temp_ia\RELATORIO-TESTES-RF006-2026-01-11.md` (overlay/backdrop persistente)
- Proposta: `D:\IC2\.temp_ia\PROPOSTA-ARQUITETO-INTEGRACAO-E2E-ISOLADOS.md`

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

#### PASSO 6.2: PRINTS OBRIGATÓRIOS (v2.3 - 2026-01-31)

**REGRA:** Durante execução dos testes de segurança, o agente DEVE exibir PRINTs estruturados confirmando execução e resultados.

### Formato de PRINT de Início de Fase

```
═══════════════════════════════════════════════════════════════
📋 FASE 6: TESTES DE SEGURANÇA
═══════════════════════════════════════════════════════════════
RF: RFXXX
Data/Hora: 2026-01-31 15:27:00
Categorias: SQL Injection, XSS, CSRF, Autenticação, Autorização, Multi-tenancy
Log: D:\IC2\.temp_ia\EVIDENCIAS-SEGURANCA-RFXXX.log
───────────────────────────────────────────────────────────────
```

### Formato de PRINT de Cada Teste de Segurança

```
🛡️ TESTANDO: SQL Injection
───────────────────────────────────────────────────────────────
TC: SEC-001 - Injeção SQL via campo de busca
Payload: ' OR '1'='1
Expected: Backend deve rejeitar (400 Bad Request)
───────────────────────────────────────────────────────────────
✅ APROVADO: Backend rejeitou payload malicioso
   Response: 400 Bad Request
   Message: "Invalid input: special characters not allowed"
   Time: 0.3s
───────────────────────────────────────────────────────────────

🛡️ TESTANDO: XSS (Cross-Site Scripting)
───────────────────────────────────────────────────────────────
TC: SEC-002 - Script injection via campo de nome
Payload: <script>alert('XSS')</script>
Expected: Frontend deve escapar, backend deve sanitizar
───────────────────────────────────────────────────────────────
✅ APROVADO: Payload sanitizado corretamente
   Frontend: &lt;script&gt;alert('XSS')&lt;/script&gt;
   Backend: Script tags removidos
   Time: 0.5s
───────────────────────────────────────────────────────────────

🛡️ TESTANDO: Autenticação
───────────────────────────────────────────────────────────────
TC: SEC-003 - Acesso sem token
Expected: 401 Unauthorized
───────────────────────────────────────────────────────────────
✅ APROVADO: Endpoint protegido corretamente
   Response: 401 Unauthorized
   Time: 0.2s
───────────────────────────────────────────────────────────────

🛡️ TESTANDO: Autorização (RBAC)
───────────────────────────────────────────────────────────────
TC: SEC-004 - Usuário sem permissão tentando criar
Expected: 403 Forbidden
───────────────────────────────────────────────────────────────
✅ APROVADO: RBAC bloqueou acesso
   Response: 403 Forbidden
   Message: "Insufficient permissions"
   Time: 0.4s
───────────────────────────────────────────────────────────────

🛡️ TESTANDO: Multi-tenancy
───────────────────────────────────────────────────────────────
TC: SEC-005 - Acesso a dados de outro tenant
Expected: 404 Not Found ou 403 Forbidden
───────────────────────────────────────────────────────────────
✅ APROVADO: Isolamento de tenant funcional
   Response: 404 Not Found (dados não visíveis)
   Time: 0.6s
───────────────────────────────────────────────────────────────

🛡️ TESTANDO: CSRF (Cross-Site Request Forgery)
───────────────────────────────────────────────────────────────
TC: SEC-006 - Request sem CSRF token
Expected: 403 Forbidden
───────────────────────────────────────────────────────────────
❌ REPROVADO: CSRF token não validado
   Response: 200 OK (DEVERIA SER 403)
   VULNERABILIDADE CRÍTICA: Endpoint aceita requests sem CSRF token
   Time: 0.3s
   Responsabilidade: BACKEND (middleware CSRF ausente)
───────────────────────────────────────────────────────────────
```

### Formato de PRINT de Resumo de Fase

```
═══════════════════════════════════════════════════════════════
📊 RESUMO: FASE 6 - TESTES DE SEGURANÇA
═══════════════════════════════════════════════════════════════
Total de testes: 6
✅ Aprovados: 5 (83.3%)
❌ Reprovados: 1 (16.7%)
Tempo total: 2.3s
Evidências: D:\IC2\.temp_ia\EVIDENCIAS-SEGURANCA-RFXXX.log
Status da fase: ❌ REPROVADO (1 vulnerabilidade crítica)
───────────────────────────────────────────────────────────────
Vulnerabilidades identificadas:
  1. SEC-006: CSRF token não validado (BACKEND - middleware ausente)
───────────────────────────────────────────────────────────────
⚠️ AÇÃO NECESSÁRIA: Corrigir vulnerabilidade de segurança crítica antes de deploy
═══════════════════════════════════════════════════════════════
```

### Comando de Execução Atualizado

```bash
# Criar diretório de evidências se não existir
mkdir -p D:/IC2/.temp_ia/

# Definir nome do arquivo de log
LOG_FILE="D:/IC2/.temp_ia/EVIDENCIAS-SEGURANCA-RFXXX.log"

# PRINT de início
echo "═══════════════════════════════════════════════════════════════"
echo "📋 FASE 6: TESTES DE SEGURANÇA"
echo "═══════════════════════════════════════════════════════════════"
echo "RF: RFXXX"
echo "Data/Hora: $(date +"%Y-%m-%d %H:%M:%S")"
echo "Log: $LOG_FILE"
echo "───────────────────────────────────────────────────────────────"

# Executar cada teste de segurança e registrar
{
  echo "🛡️ TESTANDO: SQL Injection"
  # ... executar teste SQL injection
  echo "✅ APROVADO: Backend rejeitou payload malicioso"
  echo ""

  echo "🛡️ TESTANDO: XSS"
  # ... executar teste XSS
  echo "✅ APROVADO: Payload sanitizado corretamente"
  echo ""

  echo "🛡️ TESTANDO: Autenticação"
  # ... executar teste de autenticação
  echo "✅ APROVADO: Endpoint protegido corretamente"
  echo ""

  echo "🛡️ TESTANDO: Autorização (RBAC)"
  # ... executar teste de autorização
  echo "✅ APROVADO: RBAC bloqueou acesso"
  echo ""

  echo "🛡️ TESTANDO: Multi-tenancy"
  # ... executar teste de multi-tenancy
  echo "✅ APROVADO: Isolamento de tenant funcional"
  echo ""

  echo "🛡️ TESTANDO: CSRF"
  # ... executar teste CSRF
  echo "❌ REPROVADO: CSRF token não validado"
  echo ""
} | tee "$LOG_FILE"

# Calcular resumo
PASSED=$(grep -c "✅ APROVADO" "$LOG_FILE" || echo "0")
FAILED=$(grep -c "❌ REPROVADO" "$LOG_FILE" || echo "0")
TOTAL=$((PASSED + FAILED))

# PRINT de resumo
echo "═══════════════════════════════════════════════════════════════"
echo "📊 RESUMO: FASE 6 - TESTES DE SEGURANÇA"
echo "═══════════════════════════════════════════════════════════════"
echo "Total de testes: $TOTAL"
echo "✅ Aprovados: $PASSED"
echo "❌ Reprovados: $FAILED"
echo "Evidências: $LOG_FILE"
if [ "$FAILED" -eq 0 ]; then
  echo "Status da fase: ✅ APROVADO"
else
  echo "Status da fase: ❌ REPROVADO ($FAILED vulnerabilidades)"
  grep "❌ REPROVADO" "$LOG_FILE" | while read line; do
    echo "  - $line"
  done
fi
echo "═══════════════════════════════════════════════════════════════"
```

### Validação de Evidências

```bash
# Validar que arquivo de log foi gerado
if [ ! -f "$LOG_FILE" ]; then
  echo "❌ ERRO: Arquivo de evidências de segurança não foi gerado"
  exit 1
fi

# Validar que arquivo não está vazio
if [ ! -s "$LOG_FILE" ]; then
  echo "❌ ERRO: Arquivo de evidências de segurança está vazio"
  exit 1
fi

echo "✅ Evidências de segurança registradas: $LOG_FILE"
```

---

### FASE 6.5: AUDITORIA DE CONFORMIDADE FUNCIONAL E UX

**🎯 OBJETIVO:** Detectar incongruências funcionais e problemas de UX que testes automatizados não capturam.

#### PASSO 6.5.1: Validações de Conformidade Funcional

**EXECUTAR OBRIGATORIAMENTE:**

**1. Validação de Regras de Negócio vs Hierarquia**

```typescript
// Exemplo: Desativar cliente
test('Não deve permitir desativar cliente superior na hierarquia (tenancy)', async ({ page }) => {
  // 1. Logar como usuário de tenant filho
  await loginAs('usuario@tenantfilho.com');

  // 2. Tentar desativar tenant pai (superior na hierarquia)
  const result = await page.click('[data-test="btn-desativar-tenant-pai"]');

  // 3. DEVE SER BLOQUEADO
  expect(result).toContain('Não autorizado');
  expect(result).toContain('403'); // Forbidden
});
```

**Validações obrigatórias:**
- [ ] Usuário NÃO pode desativar/editar/deletar registros de tenants superiores
- [ ] Usuário NÃO pode acessar dados fora de seu tenant (multi-tenancy)
- [ ] Usuário NÃO pode executar ações sem permissão RBAC correspondente
- [ ] Soft delete vs Hard delete estão corretos (não há ações duplicadas)
- [ ] Estados mutuamente exclusivos não coexistem (ex: Ativo vs Desativado vs Restaurado)

**2. Validação de Funcionalidades Duplicadas ou Ambíguas**

```typescript
test('Ativar vs Restaurar: não deve haver ambiguidade', async ({ page }) => {
  // 1. Desativar um cliente
  await page.click('[data-test="btn-desativar"]');

  // 2. Verificar ações disponíveis
  const actions = await page.locator('[data-test^="btn-"]').allTextContents();

  // 3. Validar que há APENAS uma forma de reverter
  const revertActions = actions.filter(a =>
    a.includes('Ativar') || a.includes('Restaurar') || a.includes('Reativar')
  );

  // DEVE haver EXATAMENTE 1 ação de reversão
  expect(revertActions.length).toBe(1);

  // 4. Validar semântica correta
  if (actions.includes('Ativar')) {
    // "Ativar" reverte "Desativar" (soft delete)
    expect(actions).not.toContain('Restaurar'); // Restaurar é para hard delete (lixeira)
  }
});
```

**Validações obrigatórias:**
- [ ] Não há funcionalidades duplicadas com nomes diferentes (ex: Ativar + Restaurar fazendo a mesma coisa)
- [ ] Semântica clara: Ativar (soft delete) vs Restaurar (hard delete/lixeira)
- [ ] Ações contextuais corretas (botões aparecem apenas quando aplicáveis)
- [ ] Ações destrutivas têm confirmação obrigatória

**3. Validação de Feedback Visual e UX**

```typescript
test('Upload de imagem: preview e persistência', async ({ page }) => {
  // 1. Fazer upload de logo
  await page.setInputFiles('[data-test="input-logo"]', 'logo-test.png');

  // 2. DEVE mostrar preview IMEDIATAMENTE
  const preview = await page.locator('[data-test="img-preview-logo"]');
  await expect(preview).toBeVisible();
  await expect(preview).toHaveAttribute('src', /blob:|data:image/);

  // 3. Salvar formulário
  await page.click('[data-test="btn-salvar"]');

  // 4. DEVE persistir a imagem
  await page.reload();
  const persistedLogo = await page.locator('[data-test="img-logo"]');
  await expect(persistedLogo).toBeVisible();
  await expect(persistedLogo).toHaveAttribute('src', /^(http|\/)/); // URL persistida
});

test('Alinhamento de botões e campos', async ({ page }) => {
  // Validar que campos relacionados estão alinhados
  const btnConsultarCNPJ = await page.locator('[data-test="btn-consultar-cnpj"]').boundingBox();
  const inputCNPJ = await page.locator('[data-test="input-cnpj"]').boundingBox();

  // Botão deve estar alinhado com o campo (mesma linha ou próximo)
  const verticalDistance = Math.abs(btnConsultarCNPJ.y - inputCNPJ.y);
  expect(verticalDistance).toBeLessThan(50); // Menos de 50px de diferença
});
```

**Validações obrigatórias:**
- [ ] Upload de arquivo mostra preview ANTES de salvar
- [ ] Upload de arquivo persiste APÓS salvar (validar com reload)
- [ ] Botões relacionados a campos estão visualmente próximos/alinhados
- [ ] Loading states visíveis durante operações assíncronas
- [ ] Mensagens de sucesso/erro aparecem após ações
- [ ] Formulários com erros destacam campos problemáticos

**4. Validação de Congruência de Estado**

```typescript
test('Estado ativo/inativo refletido corretamente na UI', async ({ page }) => {
  // 1. Criar cliente ativo
  await createClient({ nome: 'Test', ativo: true });

  // 2. Navegar para lista
  await page.goto('/clientes');

  // 3. Badge/indicador deve mostrar "Ativo"
  const badge = await page.locator('[data-test="badge-status"]').first();
  await expect(badge).toHaveText('Ativo');
  await expect(badge).toHaveClass(/bg-green/); // Badge verde

  // 4. Desativar
  await page.click('[data-test="btn-desativar"]').first();
  await page.click('[data-test="btn-confirmar"]');

  // 5. Badge DEVE atualizar IMEDIATAMENTE
  await expect(badge).toHaveText('Inativo');
  await expect(badge).toHaveClass(/bg-red/); // Badge vermelho
});
```

**Validações obrigatórias:**
- [ ] Estado no backend === Estado na UI (não há dessincronização)
- [ ] Ações que alteram estado atualizam UI em tempo real
- [ ] Indicadores visuais (badges, ícones) correspondem ao estado real
- [ ] Filtros e buscas respeitam estado atual (ex: "Mostrar inativos" funciona)

---

#### PASSO 6.5.2: Relatório de Incongruências

**Estrutura obrigatória do relatório:**

```markdown
## INCONGRUÊNCIAS DETECTADAS

### 1. Violação de Hierarquia (CRÍTICO)
**Descrição:** Usuário de tenant filho consegue desativar tenant pai
**Arquivo:** {COMPONENTE}.component.ts
**Linha:** {LINHA}
**Impacto:** CRÍTICO - Quebra de segurança multi-tenancy
**Correção:** Adicionar validação de hierarquia antes de permitir ação

### 2. Funcionalidades Duplicadas (ALTO)
**Descrição:** "Ativar" e "Restaurar" fazem a mesma coisa
**Arquivos:**
- {COMPONENTE}-list.component.html (linha {X})
- {COMPONENTE}.service.ts (linha {Y})
**Impacto:** ALTO - Confusão do usuário, manutenção duplicada
**Correção:**
- Remover "Restaurar" se não houver hard delete
- OU: Diferenciar "Ativar" (soft delete) de "Restaurar" (lixeira)

### 3. Preview de Imagem Ausente (MÉDIO)
**Descrição:** Upload de logo não mostra preview antes de salvar
**Arquivo:** {COMPONENTE}-form.component.ts (linha {X})
**Impacto:** MÉDIO - UX ruim, usuário não vê o que está enviando
**Correção:** Adicionar FileReader para preview local antes de enviar ao backend

### 4. Desalinhamento Visual (BAIXO)
**Descrição:** Botão "Consultar CNPJ" desalinhado do campo CNPJ
**Arquivo:** {COMPONENTE}-form.component.html (linha {X})
**Impacto:** BAIXO - Problema estético, não funcional
**Correção:** Ajustar classes CSS para alinhar verticalmente com input
```

**Critérios de Severidade:**
- **CRÍTICO:** Quebra de segurança, violação de regras de negócio
- **ALTO:** Funcionalidade duplicada, estado inconsistente
- **MÉDIO:** UX ruim, falta de feedback
- **BAIXO:** Problemas estéticos, alinhamento

---

#### PASSO 6.5.3: Critérios de Aprovação

**FASE 6.5 é APROVADA quando:**
- [ ] Zero incongruências CRÍTICAS detectadas
- [ ] Incongruências ALTAS documentadas com prompt de correção
- [ ] Incongruências MÉDIAS documentadas (podem ser corrigidas depois)
- [ ] Incongruências BAIXAS documentadas (backlog de melhorias)

**FASE 6.5 REPROVA o RF quando:**
- [ ] Há pelo menos 1 incongruência CRÍTICA (segurança ou regra de negócio violada)
- [ ] Há 3+ incongruências ALTAS (funcionalidades duplicadas, estado inconsistente)

**Ação se REPROVADO:**
- Gerar prompt de correção para cada incongruência CRÍTICA ou ALTA
- Bloquear RF de ir para produção até correção

---

## ⚠️ REGRA DE NÃO PARADA - NUNCA PARE EM ESTADO PARCIAL (v2.3 - 2026-02-04)

**VOCÊ NÃO PODE PARAR EM 66%, 80%, OU QUALQUER % < 100%.**

### Princípio Fundamental

SE a taxa atual for < 100%:
1. **IDENTIFICAR** exatamente qual teste/fase falhou
2. **INVESTIGAR** a causa raiz do problema
3. **TENTAR TODAS** as opções de resolução (seeds, API, config, reiniciar)
4. **SE RESOLVER**: CONTINUAR até 100%
5. **SE NÃO RESOLVER**: TENTAR próxima opção
6. **SOMENTE REPROVAR** quando TODAS as tentativas falharem

### Comportamento Proibido (Caso Real RF007 - 66%)

❌ **ERRADO:**
```
RESULTADO FINAL: PARCIAL (66% aprovado)

⚠️ PROBLEMAS IDENTIFICADOS:
1. TESTES E2E - PARCIAL (11% aprovado)
   Motivo: Endpoint /auth/login não retorna token

PRÓXIMA AÇÃO RECOMENDADA:
Aguardar seeds completarem e re-executar testes E2E
```

**ISSO É VIOLAÇÃO GRAVE!** O agente parou sem tentar resolver.

### Comportamento Correto

✅ **CORRETO:**
```
FASE 5: TESTES E2E

PROBLEMA DETECTADO: 8/9 testes E2E falharam (endpoint /auth/login sem token)

INVESTIGAÇÃO:
Tentativa 1: Verificar logs do backend
→ Encontrado: "Seeds ainda executando em InitialiseDatabaseAsync"
→ Problema: Backend aceitou requisições antes de seeds terminarem

Tentativa 2: Aguardar seeds completarem
→ curl http://localhost:5000/health... 200 OK
→ Aguardando 30s para seeds terminarem...
→ Verificando tabela Users: SELECT COUNT(*) FROM Users WHERE Email='test@example.com'
→ Resultado: 0 registros (seed ainda não completou)

Tentativa 3: Executar seed manualmente
→ cd D:\IC2\backend\IControlIT.API
→ dotnet run -- seed --entity=User
→ Resultado: SUCESSO (usuário de teste criado)

Tentativa 4: Re-executar testes E2E
→ npx playwright test e2e/specs/RF007/*.spec.ts
→ Resultado: 9/9 PASSOU (100%)

FASE 5: APROVADO (100%)

RESULTADO FINAL: APROVADO (100%)
```

### Regra de Ouro

**NÃO EXISTE:**
- ❌ "Taxa 66% - continuarei depois"
- ❌ "Problemas identificados - próximos passos..."
- ❌ "Recomendação: aguardar X e tentar novamente"
- ❌ "PARCIAL (66%)" como resultado final
- ❌ Relatório final sem ter tentado TODAS as opções

**EXISTE APENAS:**
- ✅ **APROVADO (100%)** - após resolver TODOS os problemas
- ✅ **REPROVADO (XX%)** - após ESGOTAR TODAS as tentativas de resolução

**SE você criar relatório final com taxa < 100% SEM documentar TODAS as tentativas de resolução:**
- Execução é **INVÁLIDA**
- Aprovação é **NULA**
- Você **VIOLOU** o contrato

### Tentativas Exaustivas Obrigatórias

**Problema:** Testes E2E falharam (11% aprovado)

**TENTATIVAS OBRIGATÓRIAS (nesta ordem):**
1. Verificar logs backend (identificar problema)
2. Aguardar seeds (se seeds ainda executando)
3. Executar seeds manualmente (se não completaram)
4. Inserir dados via API (se seeds falharam)
5. Verificar configuração JWT (se problema de token)
6. Verificar CORS (se problema de cross-origin)
7. Verificar auth.interceptor.ts (se header ausente)
8. Reiniciar backend (se timeout/travamento)
9. Limpar localStorage (se token inválido/expirado)
10. Re-executar testes E2E (após cada resolução)

**SOMENTE REPROVAR quando:**
- Todas as 10 tentativas falharam
- Problema não é resolvível (código com bug)
- Responsabilidade atribuída (backend/frontend)
- Evidências de TODAS as tentativas documentadas

### Tempo Esperado

- Tentativas de resolução: 1-2h
- Não tenha pressa para reprovar
- Esgote TODAS as opções primeiro

### Exceção (quando pode parar sem 100%)

- **NENHUMA.** SEMPRE tente resolver até 100% ou esgotamento total.

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

#### PASSO 7.3: Atribuir Responsabilidade E CLASSIFICAR

**🚨 REGRA CRÍTICA: Classificar ANTES de atribuir responsabilidade**

```
1. Identificar erro
2. Classificar: CÓDIGO ou INFRAESTRUTURA?
3. SE CÓDIGO → Atribuir camada (BACKEND/FRONTEND/INTEGRAÇÃO)
4. SE INFRAESTRUTURA → Marcar como BLOQUEIO (não gerar prompt)
```

---

### CLASSIFICAÇÃO: BLOQUEIO DE INFRAESTRUTURA (Ação do Usuário)

**❌ NÃO gerar prompt de correção**
**✅ Reportar ao usuário e instruir ação manual**

| Erro | Responsável | Ação do Usuário |
|------|-------------|-----------------|
| Docker não rodando | USUÁRIO | Iniciar Docker Desktop → validar `docker ps` |
| Processo travado (PID) | USUÁRIO | Matar processo: `python run.py --kill-only` |
| Banco não acessível | USUÁRIO | Validar connection string, iniciar SQL Server |
| Variáveis ambiente ausentes | USUÁRIO | Configurar `.env` ou `appsettings.json` |
| Porta ocupada | USUÁRIO | Liberar porta ou alterar configuração |

**Marcação no relatório:**
```
RESPONSABILIDADE: INFRAESTRUTURA
TIPO: BLOQUEIO DE AMBIENTE
GERAR PROMPT: NÃO
AÇÃO: Usuário deve [ação específica]
```

---

### CLASSIFICAÇÃO: ERRO DE CÓDIGO (Correção via Prompt)

**✅ GERAR prompt de correção**
**✅ Atribuir camada responsável**

#### BACKEND é responsável quando:
- HTTP 500 (erro interno do servidor)
- HTTP 400 com mensagem incorreta
- Validação aceita payload inválido
- Violação não rejeitada
- Multi-tenancy quebrado (retorna dados de outro tenant)
- Auditoria não gravada
- **Testes unitários falhando** (Domain, Application)
- **AutoMapper configuration inválida:**
  - Teste `ShouldHaveValidConfiguration` falhando
  - Unmapped members detectados
  - Arquivo responsável: `*MappingProfile.cs`
  - **Correção via CONTRATO DE MANUTENÇÃO CONTROLADA/COMPLETA**

**Marcação no relatório:**
```
RESPONSABILIDADE: BACKEND ❌
TIPO: ERRO DE CÓDIGO
GERAR PROMPT: SIM
CONTRATO: manutencao-controlada.md (ou manutencao-completa.md se > 3 arquivos)
```

#### FRONTEND é responsável quando:
- **Compilação TypeScript falhou** (erros TS)
- **Testes unitários falhando** (Jest)
- Elemento não renderizado (data-test ausente)
- Estado Loading não visível
- Estado Vazio não visível
- Estado Erro não visível
- i18n quebrado (chave não traduzida)
- Validação de formulário ausente
- **Mock objects desatualizados**
- **Signals do Angular mal configurados**

**Marcação no relatório:**
```
RESPONSABILIDADE: FRONTEND ❌
TIPO: ERRO DE CÓDIGO
GERAR PROMPT: SIM
CONTRATO: manutencao-controlada.md (ou manutencao-completa.md se > 3 arquivos)
```

#### INTEGRAÇÃO é responsável quando:
- Contrato de API quebrado (campo ausente)
- DTO incompatível
- Mapeamento incorreto

**Marcação no relatório:**
```
RESPONSABILIDADE: INTEGRAÇÃO ❌
TIPO: ERRO DE CÓDIGO
GERAR PROMPT: SIM
CONTRATO: manutencao-completa.md (cross-layer)
```

#### 🚨 REGRA ESPECIAL: Erros de Infraestrutura vs Erros de Código

**Quando houver APENAS bloqueios de infraestrutura (0 erros de código):**

1. ❌ **NÃO gerar prompt de correção** (não há código para corrigir)
2. ✅ **Reportar claramente ao usuário:**
   ```
   ⚠️ BLOQUEIO DE INFRAESTRUTURA (não é erro de código)

   BLOQUEIOS IDENTIFICADOS:
   - Docker não está rodando (23 testes funcionais backend)
   - [outros bloqueios...]

   AÇÃO NECESSÁRIA (USUÁRIO):
   1. Iniciar Docker Desktop
   2. Validar: docker ps
   3. Re-executar: prompts/testes/execucao-completa.md

   RESPONSABILIDADE: USUÁRIO (infraestrutura)
   NÃO HÁ ERROS DE CÓDIGO PARA CORRIGIR.
   ```
3. ✅ **Atualizar STATUS.yaml:**
   ```yaml
   testes_ti:
     resultado_final: "BLOQUEADO_INFRAESTRUTURA"
     motivo_bloqueio: "Docker não disponível"
     requer_acao_manual: true
     erros_codigo: 0
     bloqueios_infraestrutura: 1
   ```

---

**Quando houver MIX (bloqueios de infraestrutura + erros de código):**

1. ✅ **GERAR prompt de correção APENAS para erros de código**
2. ✅ **Separar claramente bloqueios vs erros no prompt:**
   ```
   📋 PROMPT DE CORREÇÃO + BLOQUEIOS

   ERROS DE CÓDIGO (COPIAR PROMPT):
   - ERRO #1: Frontend Unit Tests (11 erros TypeScript)
   → Arquivo: .temp_ia/PROMPT-CORRECAO-RF006-2026-01-06.md

   BLOQUEIOS DE INFRAESTRUTURA (AÇÃO USUÁRIO):
   - Docker não disponível (23 testes funcionais backend)
   → Ação: Iniciar Docker Desktop

   ORDEM DE RESOLUÇÃO:
   1. Corrigir ERROS DE CÓDIGO (copiar prompt acima)
   2. Resolver BLOQUEIOS (ações manuais)
   3. Re-executar testes completos
   ```
3. ✅ **Atualizar STATUS.yaml:**
   ```yaml
   testes_ti:
     resultado_final: "REPROVADO_MISTO"
     erros_codigo: 11
     bloqueios_infraestrutura: 23
     requer_correcao_codigo: true
     requer_acao_usuario: true
   ```

---

### FASE 7.4: GERAR PROMPT DE CORREÇÃO AUTOMÁTICO (SE REPROVADO)

#### 🚨 REGRA CRÍTICA: Diferenciar Bloqueios de Infraestrutura vs Erros de Código

**ANTES de gerar prompt de correção, o agente DEVE classificar cada erro:**

| Tipo | Responsabilidade | Gerar Prompt? | Ação |
|------|------------------|---------------|------|
| **Erro de Código** | BACKEND/FRONTEND/INTEGRAÇÃO | ✅ **SIM** | Gerar prompt de correção |
| **Bloqueio de Infraestrutura** | USUÁRIO | ❌ **NÃO** | Reportar e instruir usuário |

**Exemplos de Bloqueio de Infraestrutura (NÃO gerar prompt):**
- Docker não está rodando
- Banco de dados não acessível
- Variáveis de ambiente ausentes
- Processos travados (PID bloqueando DLLs)

**Exemplos de Erro de Código (GERAR prompt):**
- Compilação TypeScript falhou (frontend)
- Testes unitários falhando (backend/frontend)
- AutoMapper configuration inválida (backend)
- Data-test attributes ausentes (frontend)

---

**SE taxa de aprovação < 100% E houver ERROS DE CÓDIGO:**

#### 🚨 REGRA CRÍTICA: IDENTIFICAR **TODOS** OS ERROS ANTES DE GERAR PROMPT

**OBRIGATÓRIO:** O agente DEVE executar **TODAS** as baterias de testes, mesmo se alguma falhar, para identificar o **MÁXIMO de erros possível** antes de gerar o prompt de correção.

**PROIBIDO:**
- ❌ Parar na primeira falha
- ❌ Gerar prompt após identificar apenas 1 erro
- ❌ "Descobrir erros aos poucos" (isso gera retrabalho para o usuário)
- ❌ Pular testes que ainda não foram executados

**OBRIGATÓRIO:**
- ✅ Executar TODOS os testes backend (mesmo se alguns falharem)
- ✅ Executar TODOS os testes frontend (mesmo se alguns falharem)
- ✅ Executar TODOS os testes E2E (mesmo se alguns falharem)
- ✅ Executar TODOS os testes de segurança (mesmo se alguns falharem)
- ✅ AGREGAR todos os erros identificados em um ÚNICO prompt de correção
- ✅ Listar TODOS os arquivos afetados de uma vez
- ✅ Priorizar erros (bloqueantes primeiro, depois alta, média, baixa)

**Exemplo Correto:**
```
ERROS IDENTIFICADOS (TODOS DE UMA VEZ):
- ERRO #1 (BLOQUEANTE): Backend compilation failed (5 arquivos)
- ERRO #2 (ALTA): Frontend unit tests failing (11 arquivos)
- ERRO #3 (ALTA): E2E tests failing (3 specs)
- ERRO #4 (MÉDIA): Security test SQL Injection (1 endpoint)

ARQUIVOS AFETADOS TOTAIS: 20 arquivos
CONTRATO: manutencao-completa.md (> 3 arquivos)
```

**Exemplo Incorreto (NÃO FAZER):**
```
❌ ERRO #1 identificado: Frontend unit tests failing (2 arquivos)
   → Gerar prompt agora...
   → [usuário corrige]
   → Re-executar testes...
   → ❌ ERRO #2 identificado: E2E tests failing (3 specs)
   → Gerar outro prompt...
   → [usuário corrige novamente]
   → Re-executar testes...
   → ❌ ERRO #3 identificado: Security test failing...
   → [RETRABALHO - PROIBIDO!]
```

---

#### 🚨 OBRIGAÇÃO CRÍTICA: O agente DEVE executar TODOS os passos abaixo

1. ✅ **Filtrar apenas erros de código** (excluir bloqueios de infraestrutura)
   - **IMPORTANTE:** Mas AGREGAR erros de TODAS as baterias executadas

2. ✅ **DECIDIR O CONTRATO DE MANUTENÇÃO CORRETO:**

   **REGRA AUTOMÁTICA:**
   ```
   SE (número de arquivos afetados <= 3):
       contrato = "D:\IC2_Governanca\governanca\contracts\manutencao\manutencao-controlada.md"
   SENÃO:
       contrato = "D:\IC2_Governanca\governanca\contracts\manutencao\manutencao-completa.md"
   ```

   **Contagem de arquivos:**
   - Listar TODOS os arquivos que precisam ser corrigidos
   - Se <= 3 arquivos: manutencao-controlada.md
   - Se > 3 arquivos: manutencao-completa.md

3. ✅ **Gerar prompt de correção completo e descritivo**
   - **OBRIGATÓRIO:** Usar o template da seção "Template de Prompt de Correção" abaixo
   - **OBRIGATÓRIO:** Substituir [TIPO] pelo contrato decidido no passo 2
   - **OBRIGATÓRIO:** Incluir caminho absoluto do contrato
   - **OBRIGATÓRIO:** Listar TODOS os arquivos que precisam correção

4. ✅ **Salvar em `.temp_ia/PROMPT-CORRECAO-RFXXX-[DATA]-EXECUCAO-[N].md`**
   - **OBRIGATÓRIO:** Nome de arquivo com data real (não placeholder)
   - **OBRIGATÓRIO:** Conteúdo completo (> 100 linhas)

5. ✅ **Exibir prompt completo na tela**
   - **OBRIGATÓRIO:** Mostrar TODO o conteúdo do arquivo gerado
   - **OBRIGATÓRIO:** Incluir linha inicial "Execute D:\IC2_Governanca\governanca\contracts\manutencao\[TIPO].md..."

6. ✅ **Informar ao usuário:**
   ```
   📋 PROMPT DE CORREÇÃO GERADO E PRONTO PARA USO

   Arquivo: .temp_ia/PROMPT-CORRECAO-RFXXX-2026-01-06-EXECUCAO-1.md
   Contrato: D:\IC2_Governanca\governanca\contracts\manutencao\[TIPO].md

   ERROS DE CÓDIGO IDENTIFICADOS:
   - ERRO #1: Frontend Unit Tests (11 erros TypeScript)
   - (lista apenas erros que exigem correção de código)

   ARQUIVOS AFETADOS: [N] arquivos
   CONTRATO ESCOLHIDO: [manutencao-controlada.md OU manutencao-completa.md]
   JUSTIFICATIVA: [N arquivos <= 3 OU N arquivos > 3]

   ══════════════════════════════════════════════════════════════
   📋 PROMPT COMPLETO PARA COPIAR (INÍCIO)
   ══════════════════════════════════════════════════════════════

   [EXIBIR CONTEÚDO COMPLETO DO ARQUIVO .temp_ia/PROMPT-CORRECAO-RFXXX...]

   ══════════════════════════════════════════════════════════════
   📋 PROMPT COMPLETO PARA COPIAR (FIM)
   ══════════════════════════════════════════════════════════════

   ➡️ COPIE o prompt acima (entre as linhas ═══) e COLE em uma NOVA CONVERSA.

   BLOQUEIOS DE INFRAESTRUTURA (SE HOUVER):
   - Docker não está rodando (iniciar Docker Desktop)

   Para resolver BLOQUEIOS DE INFRAESTRUTURA, execute as ações indicadas
   e RE-EXECUTE os testes.
   ```

7. ❌ **PROIBIDO:**
   - Apenas "recomendar" ação
   - Dizer "será necessário gerar prompt"
   - Omitir o conteúdo completo do prompt
   - Deixar o usuário "criar o prompt sozinho"

---

**SE taxa de aprovação < 100% APENAS por bloqueios de infraestrutura:**

1. ❌ **NÃO gerar prompt de correção** (não há código para corrigir)
2. ✅ **Reportar bloqueios ao usuário:**
   ```
   ⚠️ EXECUÇÃO BLOQUEADA POR INFRAESTRUTURA

   BLOQUEIOS IDENTIFICADOS:
   - Docker não está rodando (23 testes funcionais backend)

   AÇÃO NECESSÁRIA (USUÁRIO):
   1. Iniciar Docker Desktop
   2. Validar: docker ps
   3. Re-executar: prompts/testes/execucao-completa.md

   NÃO HÁ ERROS DE CÓDIGO PARA CORRIGIR.
   Após resolver bloqueios, testes devem passar.
   ```

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

**IMPORTANTE:** Este template é usado APENAS quando houver **ERROS DE CÓDIGO** (não bloqueios de infraestrutura).

**OBRIGATÓRIO:** O agente DEVE:
1. Decidir o contrato correto (passo 2 acima)
2. Substituir `[TIPO]` pelo contrato decidido
3. Gerar o prompt COMPLETO
4. Salvar em `.temp_ia/`
5. Exibir o prompt COMPLETO na tela

```markdown
Execute D:\IC2_Governanca\governanca\contracts\manutencao\[TIPO].md para corrigir os seguintes erros CRÍTICOS identificados na Execução [N] de testes do RFXXX:

**CONTRATO ESCOLHIDO AUTOMATICAMENTE:**
- [TIPO] = manutencao-controlada.md (arquivos afetados <= 3)
  OU
- [TIPO] = manutencao-completa.md (arquivos afetados > 3)

**ARQUIVOS AFETADOS:** [N] arquivos
**JUSTIFICATIVA:** [Explicar por que este contrato foi escolhido]

**REGRA CRÍTICA:** Sempre usar caminho absoluto (D:\IC2_Governanca\governanca\contracts\...) no prompt gerado

## CONTEXTO DA EXECUÇÃO

- **RF:** RFXXX - [Título do RF]
- **Data:** [YYYY-MM-DD]
- **Execução:** [N]ª tentativa
- **Taxa de Aprovação:** [XX%] ([Y]/[Z] testes CÓDIGO | [W] testes BLOQUEADOS por infraestrutura)
- **Resultado:** REPROVADO (critério: 100%)
- **Relatório:** .temp_ia/RELATORIO-TESTES-RFXXX-[DATA]-EXECUCAO-[N].md
- **STATUS.yaml:** Atualizado com execução [N]

## BLOQUEIOS DE INFRAESTRUTURA (AÇÃO DO USUÁRIO - NÃO CORRIGIR)

[SE houver bloqueios de infraestrutura, listar aqui:]

- ⚠️ **Docker não disponível:** 23 testes funcionais backend bloqueados
  - Ação: Iniciar Docker Desktop
  - Validar: `docker ps`
  - Re-executar testes após resolver

[SE não houver bloqueios, escrever:]
- ✅ Nenhum bloqueio de infraestrutura identificado

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
   - Buscar por `[YYYY-MM-DD]`, `[N]`, `[Lista...]`, `[RFXXX]`, `[TIPO]`
   - Se encontrar qualquer placeholder → **BLOQUEIO TOTAL**
4. ✅ Verificar que seções obrigatórias estão presentes:
   - "## CONTEXTO DA EXECUÇÃO"
   - "**CONTRATO ESCOLHIDO AUTOMATICAMENTE:**"
   - "**ARQUIVOS AFETADOS:**"
   - "**JUSTIFICATIVA:**"
   - "## ERROS IDENTIFICADOS"
   - "### ERRO [N] - [CATEGORIA]"
   - "#### Descrição do Erro"
   - "#### Evidências"
   - "#### Comandos Tentados"
   - "#### Contexto Técnico" (com "Fase do erro:")
   - "#### Responsabilidade"
   - "#### Solução Esperada"
5. ✅ **VALIDAÇÃO CRÍTICA:** Verificar linha inicial do prompt:
   - DEVE começar com: `Execute D:\IC2_Governanca\governanca\contracts\manutencao\[manutencao-controlada.md OU manutencao-completa.md]...`
   - **NÃO PODE** ter `[TIPO]` não substituído
   - **NÃO PODE** estar vago ("será necessário", "recomendado")
6. ✅ Exibir prompt completo na tela (entre linhas ═══)

**SE qualquer validação FALHAR:**
- ❌ **BLOQUEIO TOTAL**
- Exibir mensagem: "Prompt de correção incompleto ou vago. Refazer FASE 7.4 com captura completa de contexto."
- **NÃO prosseguir para FASE 8**

**PROIBIÇÕES ABSOLUTAS:**
- ❌ Dizer "será necessário gerar prompt"
- ❌ Dizer "próxima ação recomendada"
- ❌ Deixar `[TIPO]` não substituído
- ❌ Não exibir o prompt completo
- ❌ Não decidir o contrato automaticamente

---

### FASE 8: DECISÃO FINAL E MERGE AUTOMÁTICO

#### PASSO 8.1: Aplicar Critério 0% ou 100%

- ✅ **APROVADO**: Taxa de aprovação = 100% (TODOS os testes passaram)
- ❌ **REPROVADO**: Taxa de aprovação < 100% (QUALQUER teste falhou)

**NÃO EXISTE APROVAÇÃO COM RESSALVAS.**

**⚠️ PROIBIÇÕES ABSOLUTAS (v1.4 - 2026-01-31):**

- ❌ **NUNCA** usar "APROVADO CONDICIONALMENTE" (categoria não existe)
- ❌ **NUNCA** usar "APROVADO COM RESSALVAS" (categoria não existe)
- ❌ **NUNCA** atribuir a "infraestrutura" e aprovar (problema deve ser resolvido)
- ❌ **NUNCA** dizer "código está correto, problema é de integração" e aprovar
- ❌ **NUNCA** sugerir "aprovação condicional pendente correção de auth"

**SE testes de autenticação falharem:**
1. IDENTIFICAR: Qual componente está falhando (backend JWT, frontend interceptor, E2E storageState)
2. RESOLVER: Corrigir o problema OU documentar para correção
3. REPROVAR: Se não resolver, reprovar com responsabilidade atribuída
4. REPETIR: Após correção, re-executar testes

**Responsabilidade em falhas de autenticação:**
| Sintoma | Responsável |
|---------|-------------|
| Token expira muito rápido | BACKEND (config JWT) |
| Header Authorization ausente | FRONTEND (auth.interceptor.ts) |
| Token não persiste no localStorage | FRONTEND (auth.service.ts) |
| E2E perde sessão entre requests | TESTES (storageState Playwright) |
| 401 em endpoint protegido | BACKEND (policy) ou FRONTEND (interceptor) |

**Resultado: APROVADO (100%) ou REPROVADO (< 100%). Não existe outro.**

#### PASSO 8.2: Merge Automático em `dev` (SE APROVADO A 100%)

**🚨 REGRA CRÍTICA: Merge Automático ao Atingir 100%**

**SE taxa de aprovação = 100%:**

```bash
# 1. Identificar branch atual
CURRENT_BRANCH=$(git branch --show-current)
echo "Branch atual: $CURRENT_BRANCH"

# 2. Verificar se está em branch de correção (fix/*)
if [[ "$CURRENT_BRANCH" == fix/* ]]; then
  echo "✅ Branch de correção detectado: $CURRENT_BRANCH"
  echo "✅ Testes 100% aprovados, fazendo merge em dev..."

  # 3. Fazer checkout para dev
  git checkout dev

  # 4. Fazer merge do branch de correção
  git merge --no-ff "$CURRENT_BRANCH" -m "merge: $CURRENT_BRANCH - testes 100% aprovados

Merge automático realizado após execução completa de testes.

Taxa de aprovação: 100%
Branch: $CURRENT_BRANCH
Data: $(date +"%Y-%m-%d %H:%M:%S")

Testes executados:
- Backend: PASS
- Frontend: PASS
- E2E: PASS
- Segurança: PASS
- Conformidade UX: PASS

🤖 Merge automático via contrato de testes

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"

  # 5. Validar merge bem-sucedido
  if [ $? -eq 0 ]; then
    echo "✅ Merge realizado com sucesso em dev"
    echo "ℹ️ Branch de correção mantido para referência: $CURRENT_BRANCH"
    echo "ℹ️ Para deletar: git branch -d $CURRENT_BRANCH"
  else
    echo "❌ ERRO: Merge falhou"
    echo "❌ Resolvendo manualmente..."
    exit 1
  fi
else
  echo "ℹ️ Branch atual não é de correção (fix/*), sem merge automático"
  echo "ℹ️ Branch: $CURRENT_BRANCH"
fi
```

**Saída esperada (branch de correção, 100% aprovado):**
```
Branch atual: fix/rf006-corrigindo-hierarquia-tenant
✅ Branch de correção detectado: fix/rf006-corrigindo-hierarquia-tenant
✅ Testes 100% aprovados, fazendo merge em dev...
Switched to branch 'dev'
Merge made by the 'ort' strategy.
 [arquivos alterados listados]
✅ Merge realizado com sucesso em dev
ℹ️ Branch de correção mantido para referência: fix/rf006-corrigindo-hierarquia-tenant
ℹ️ Para deletar: git branch -d fix/rf006-corrigindo-hierarquia-tenant
```

**Saída esperada (branch principal, 100% aprovado):**
```
Branch atual: dev
ℹ️ Branch atual não é de correção (fix/*), sem merge automático
ℹ️ Branch: dev
```

**SE taxa de aprovação < 100%:**
- ❌ **NÃO fazer merge**
- ✅ Permanecer no branch de correção (fix/*)
- ✅ Gerar prompts de correção
- ✅ Aguardar novas correções e re-execução de testes

---

#### PASSO 8.3: Atualizar STATUS.yaml (SEM COMMIT)

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

#### PASSO 9.3: Consolidar Logs de Evidências (v2.3 - 2026-01-31)

**REGRA:** Consolidar todos os logs de evidências gerados durante as fases em um único relatório.

### Logs Gerados por Fase

```
D:\IC2\.temp_ia\
├── EVIDENCIAS-BACKEND-RFXXX.log          # FASE 3
├── EVIDENCIAS-FRONTEND-RFXXX.log         # FASE 4
├── EVIDENCIAS-E2E-RFXXX.log              # FASE 5
└── EVIDENCIAS-SEGURANCA-RFXXX.log        # FASE 6
```

### Criar Relatório Consolidado

```bash
# Definir arquivo consolidado
CONSOLIDATED_LOG="D:/IC2/.temp_ia/EVIDENCIAS-CONSOLIDADAS-RFXXX-$(date +%Y%m%d-%H%M%S).log"

# Consolidar todos os logs
{
  echo "═══════════════════════════════════════════════════════════════"
  echo "📊 RELATÓRIO CONSOLIDADO DE EVIDÊNCIAS"
  echo "═══════════════════════════════════════════════════════════════"
  echo "RF: RFXXX"
  echo "Data: $(date +"%Y-%m-%d %H:%M:%S")"
  echo "═══════════════════════════════════════════════════════════════"
  echo ""

  if [ -f "D:/IC2/.temp_ia/EVIDENCIAS-BACKEND-RFXXX.log" ]; then
    echo "📋 FASE 3: TESTES BACKEND"
    echo "───────────────────────────────────────────────────────────────"
    cat "D:/IC2/.temp_ia/EVIDENCIAS-BACKEND-RFXXX.log"
    echo ""
  fi

  if [ -f "D:/IC2/.temp_ia/EVIDENCIAS-FRONTEND-RFXXX.log" ]; then
    echo "📋 FASE 4: TESTES FRONTEND"
    echo "───────────────────────────────────────────────────────────────"
    cat "D:/IC2/.temp_ia/EVIDENCIAS-FRONTEND-RFXXX.log"
    echo ""
  fi

  if [ -f "D:/IC2/.temp_ia/EVIDENCIAS-E2E-RFXXX.log" ]; then
    echo "📋 FASE 5: TESTES E2E"
    echo "───────────────────────────────────────────────────────────────"
    cat "D:/IC2/.temp_ia/EVIDENCIAS-E2E-RFXXX.log"
    echo ""
  fi

  if [ -f "D:/IC2/.temp_ia/EVIDENCIAS-SEGURANCA-RFXXX.log" ]; then
    echo "📋 FASE 6: TESTES DE SEGURANÇA"
    echo "───────────────────────────────────────────────────────────────"
    cat "D:/IC2/.temp_ia/EVIDENCIAS-SEGURANCA-RFXXX.log"
    echo ""
  fi

  echo "═══════════════════════════════════════════════════════════════"
  echo "📊 RESUMO FINAL DE TODAS AS FASES"
  echo "═══════════════════════════════════════════════════════════════"

  # Calcular totais
  BACKEND_PASSED=$(grep -c "✅" "D:/IC2/.temp_ia/EVIDENCIAS-BACKEND-RFXXX.log" 2>/dev/null || echo "0")
  BACKEND_FAILED=$(grep -c "❌" "D:/IC2/.temp_ia/EVIDENCIAS-BACKEND-RFXXX.log" 2>/dev/null || echo "0")

  FRONTEND_PASSED=$(grep -c "PASS" "D:/IC2/.temp_ia/EVIDENCIAS-FRONTEND-RFXXX.log" 2>/dev/null || echo "0")
  FRONTEND_FAILED=$(grep -c "FAIL" "D:/IC2/.temp_ia/EVIDENCIAS-FRONTEND-RFXXX.log" 2>/dev/null || echo "0")

  E2E_PASSED=$(grep -c "✓" "D:/IC2/.temp_ia/EVIDENCIAS-E2E-RFXXX.log" 2>/dev/null || echo "0")
  E2E_FAILED=$(grep -c "✘" "D:/IC2/.temp_ia/EVIDENCIAS-E2E-RFXXX.log" 2>/dev/null || echo "0")

  SECURITY_PASSED=$(grep -c "✅ APROVADO" "D:/IC2/.temp_ia/EVIDENCIAS-SEGURANCA-RFXXX.log" 2>/dev/null || echo "0")
  SECURITY_FAILED=$(grep -c "❌ REPROVADO" "D:/IC2/.temp_ia/EVIDENCIAS-SEGURANCA-RFXXX.log" 2>/dev/null || echo "0")

  TOTAL_PASSED=$((BACKEND_PASSED + FRONTEND_PASSED + E2E_PASSED + SECURITY_PASSED))
  TOTAL_FAILED=$((BACKEND_FAILED + FRONTEND_FAILED + E2E_FAILED + SECURITY_FAILED))
  TOTAL_TESTS=$((TOTAL_PASSED + TOTAL_FAILED))

  if [ "$TOTAL_TESTS" -gt 0 ]; then
    APPROVAL_RATE=$((TOTAL_PASSED * 100 / TOTAL_TESTS))
  else
    APPROVAL_RATE=0
  fi

  echo "FASE 3 (Backend):   $BACKEND_PASSED aprovados, $BACKEND_FAILED reprovados"
  echo "FASE 4 (Frontend):  $FRONTEND_PASSED aprovados, $FRONTEND_FAILED reprovados"
  echo "FASE 5 (E2E):       $E2E_PASSED aprovados, $E2E_FAILED reprovados"
  echo "FASE 6 (Segurança): $SECURITY_PASSED aprovados, $SECURITY_FAILED reprovados"
  echo "───────────────────────────────────────────────────────────────"
  echo "TOTAL:              $TOTAL_PASSED aprovados, $TOTAL_FAILED reprovados"
  echo "Taxa de aprovação:  $APPROVAL_RATE%"
  echo ""

  if [ "$TOTAL_FAILED" -eq 0 ]; then
    echo "RESULTADO FINAL: ✅ APROVADO 100%"
  else
    echo "RESULTADO FINAL: ❌ REPROVADO ($APPROVAL_RATE%)"
  fi

  echo "═══════════════════════════════════════════════════════════════"
} > "$CONSOLIDATED_LOG"

echo "✅ Relatório consolidado gerado: $CONSOLIDATED_LOG"
```

### Validação do Relatório Consolidado

```bash
# Validar que relatório foi gerado
if [ ! -f "$CONSOLIDATED_LOG" ]; then
  echo "❌ ERRO: Relatório consolidado não foi gerado"
  exit 1
fi

# Validar que contém dados
if [ ! -s "$CONSOLIDATED_LOG" ]; then
  echo "❌ ERRO: Relatório consolidado está vazio"
  exit 1
fi

# Exibir localização
echo "═══════════════════════════════════════════════════════════════"
echo "📄 EVIDÊNCIAS CONSOLIDADAS"
echo "═══════════════════════════════════════════════════════════════"
echo "Relatório: $CONSOLIDATED_LOG"
echo "Tamanho: $(wc -l < "$CONSOLIDATED_LOG") linhas"
echo "═══════════════════════════════════════════════════════════════"
```

### Estrutura Final de Evidências

```
D:\IC2\.temp_ia\
├── EVIDENCIAS-BACKEND-RFXXX.log                    # FASE 3 (individual)
├── EVIDENCIAS-FRONTEND-RFXXX.log                   # FASE 4 (individual)
├── EVIDENCIAS-E2E-RFXXX.log                        # FASE 5 (individual)
├── EVIDENCIAS-SEGURANCA-RFXXX.log                  # FASE 6 (individual)
└── EVIDENCIAS-CONSOLIDADAS-RFXXX-20260131-152800.log  # Consolidado (todas as fases)
```

**Observação:** Os logs individuais são mantidos para análise detalhada, e o consolidado fornece visão geral.

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

**OU (se > 3 arquivos afetados):**

Execute D:\IC2_Governanca\prompts\desenvolvimento\manutencao\manutencao-completa.md para corrigir o seguinte erro no [backend/frontend] de RFXXX:

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

### 7.4. Proibições de Categorias de Aprovação (v1.4 - 2026-01-31)

**O agente NÃO PODE criar ou usar categorias que não existem:**

- ❌ **"APROVADO CONDICIONALMENTE"** → Categoria não existe
- ❌ **"APROVADO COM RESSALVAS"** → Categoria não existe
- ❌ **"APROVADO PARCIALMENTE"** → Categoria não existe
- ❌ **"APROVADO PARA HOM"** → Categoria não existe (use MVS se quiser HOM)
- ❌ **"PASSOU, MAS COM PROBLEMA DE INTEGRAÇÃO"** → NÃO é aprovação

**Exemplos de relatórios INVÁLIDOS:**

```
❌ INVÁLIDO:
"O frontend RF083 deve ser considerado APROVADO CONDICIONALMENTE.
Próximos passos para resolver o GAP-INTEGRACAO-001..."

❌ INVÁLIDO:
"Recomendação: Este é um problema de infraestrutura de testes, não do código.
O código está correto, problema é de integração."

❌ INVÁLIDO:
"Conclusão: O problema NÃO é do código RF083. É um problema de INTEGRAÇÃO entre
o mecanismo de autenticação e o ambiente E2E."
```

**Exemplo de relatório VÁLIDO:**

```
✅ VÁLIDO:
"Resultado: REPROVADO

Testes falharam por problema de autenticação (401 Unauthorized).

RESPONSABILIDADE ATRIBUÍDA:
- Componente: FRONTEND (auth.interceptor.ts)
- Sintoma: Header Authorization não adicionado em requests
- Evidência: Network tab mostra request sem Bearer token

AÇÃO NECESSÁRIA:
Executar prompt de manutenção para corrigir auth.interceptor.ts

STATUS.yaml: testes_ti.resultado_final = REPROVADO
STATUS.yaml: testes_ti.motivo_reprovacao = AUTH_INTERCEPTOR_FALHA"
```

**REGRA CRÍTICA:**
- Se testes falham → REPROVAR e atribuir responsabilidade
- Não existe "problema de infraestrutura que não impede aprovação"
- Não existe "código correto mas testes falhando"
- Se testes falham, algo está errado e DEVE ser corrigido

### 7.5. Proibições de Comportamento Passivo (v1.5 - 2026-01-31)

**O agente NÃO PODE criar "Gaps" e pedir para usuário resolver:**

- ❌ **"Gap Crítico: GAP-MVS-001"** → VOCE resolve, não documenta gap e para
- ❌ **"Ação Requerida:"** → VOCE resolve, não pede para usuário
- ❌ **"Próximos Passos Recomendados:"** → VOCE executa, não sugere para usuário
- ❌ **"Iniciar backend manualmente"** → VOCE inicia, não pede para usuário
- ❌ **"Executar smoke test E2E"** → VOCE executa, não pede para usuário
- ❌ **"Implementar testes de segurança"** → VOCE atribui responsável, não pede
- ❌ **"Re-executar contrato MVS completo"** → VOCE re-executa, não pede
- ❌ **"Validar inicialização do backend manualmente"** → VOCE valida, não pede

**Exemplos de comportamento PASSIVO (PROIBIDO):**

```
❌ PASSIVO (RF083 real):
GAP-MVS-001: Backend não inicia programaticamente
Ação Requerida: Validar inicialização do backend manualmente

GAP-MVS-002: Testes de segurança não implementados
Ação Requerida: Implementar testes com Category=Security

Próximos Passos Recomendados:
1. Iniciar backend manualmente e executar smoke test E2E
2. Implementar testes de segurança crítica
3. Re-executar contrato MVS completo
```

**Exemplos de comportamento ATIVO (OBRIGATÓRIO):**

```
✅ ATIVO:
FASE 3: Backend não respondeu em http://localhost:5000

RESOLUÇÃO AUTÔNOMA:
Tentativa 1: Matar processo na porta 5000... SUCESSO
Tentativa 2: Reiniciar backend... SUCESSO
Tentativa 3: Executar smoke test... PASSOU (1/1)

FASE 3: APROVADO

FASE 4: Testes de segurança não encontrados

RESPONSABILIDADE ATRIBUÍDA:
- Componente: BACKEND (testes unitários)
- Responsável: Time de desenvolvimento backend
- Status: NÃO IMPLEMENTADO

FASE 4: REPROVADO
RESULTADO FINAL: REPROVADO (taxa 66%)
```

**REGRA CRÍTICA:**
- VOCE resolve problemas de infraestrutura (backend não inicia, portas ocupadas)
- VOCE atribui responsabilidade quando código falta (testes não implementados)
- VOCE NUNCA pede para usuário resolver
- VOCE NUNCA cria "Próximos Passos" para usuário

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

## 9. TROUBLESHOOTING

### Problema: "schema.sql NOT FOUND"
**Causa:** ADR-005 (Schema-First Testing) não implementado.

**Solução:**
1. Executar `/fix-schema-sql RF{NNN}` (se skill existir)
2. OU reportar gap em STATUS.yaml:
   ```yaml
   gaps:
     - tipo: "infrastructure"
       descricao: "schema.sql ausente (ADR-005 Schema-First Testing)"
       impacto: "23 testes funcionais backend bloqueados"
       acao: "Criar D:\\IC2\\backend\\IControlIT.API\\tests\\schema.sql"
   ```

### Problema: "cd: too many arguments"
**Causa:** Sintaxe bash incorreta para Windows.

**Solução:** Usar `cd /d/IC2` em vez de `cd /d D:\IC2`.

### Problema: "Get-Process: command not found"
**Causa:** PowerShell cmdlet executado em bash.

**Solução:** Executar diretamente no PowerShell (sem bash wrapper).

### Problema: "Docker not found" durante testes
**Causa:** Docker Desktop não está rodando.

**Solução:**
1. Iniciar Docker Desktop manualmente
2. Aguardar Docker estar pronto (ícone verde na bandeja)
3. Validar: `docker ps`
4. Re-executar testes

**Impacto:** 23 testes funcionais backend bloqueados (não é erro de código).

---

## 10. REGRA DE NEGAÇÃO ZERO

Se uma solicitação:
- não estiver explicitamente prevista no contrato ativo, ou
- conflitar com qualquer regra do contrato

ENTÃO:

- A execução DEVE ser NEGADA
- Nenhuma ação parcial pode ser realizada
- Nenhum "adiantamento" é permitido

---

**FIM DO CONTRATO**
