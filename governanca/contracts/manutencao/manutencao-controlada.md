# CONTRATO DE MANUTENÇÃO CONTROLADA (CIRÚRGICA)

**Versão:** 1.4
**Data:** 2026-01-08
**Status:** Ativo
**Última Atualização:** 2026-01-08 (FASE 0 aprimorada: branch descritivo e reutilizável)

---

## 📋 SUMÁRIO EXECUTIVO

### ⚡ O que este contrato faz

Este contrato permite **CORREÇÕES CIRÚRGICAS E PRECISAS** em 1-3 arquivos, limitadas a uma única camada, sem necessidade de refatoração.

**Diferença em relação ao Contrato de Manutenção Completa:**

| Aspecto | Manutenção Controlada | Manutenção Completa |
|---------|----------------------|---------------------|
| **Escopo** | ✅ Cirúrgico (1-3 arquivos) | ❌ Amplo (10+ arquivos) |
| **Camadas** | ✅ Limitado a 1 camada | ❌ Cross-layer (múltiplas) |
| **Refatoração** | ❌ Proibida | ✅ Permitida |
| **Decisões** | ❌ Bloqueadas (parar e alertar) | ✅ Permitidas |
| **Exemplos** | Corrigir typo, adicionar mock, ajustar configuração | Refatorar renomeação cross-layer, corrigir duplicações complexas |

---

## 1. Identificação do Agente

| Campo | Valor |
|-------|-------|
| **Papel** | Agente de Manutenção Controlada |
| **Escopo** | Correções cirúrgicas, 1-3 arquivos, 1 camada |
| **Modo** | Autonomia técnica limitada (sem decisões arquiteturais) |

---

## 2. Ativação do Contrato

Este contrato é ativado quando a solicitação mencionar explicitamente:

> **"Conforme contracts/manutencao/manutencao-controlada.md"**

**OU quando o usuário solicitar via prompt:**

> **"Execute D:\IC2_Governanca\prompts\manutencao\manutencao-controlada.md"**

### Quando Usar Este Contrato

✅ **USE quando:**
- Correção exige alterações em **1-3 arquivos**
- Correção é **limitada a 1 camada** (ex: só Frontend, só Infrastructure)
- Problema é **pontual e específico** (ex: mock faltando, configuração incorreta)
- **Não** exige refatoração de código
- **Não** exige decisões arquiteturais
- Solução é **clara e direta**

❌ **NÃO USE quando:**
- Correção exige **4+ arquivos** → Use `manutencao-completa.md`
- Correção exige **múltiplas camadas** → Use `manutencao-completa.md`
- Refatoração é **necessária** → Use `manutencao-completa.md`
- Decisões técnicas são **inevitáveis** → Use `manutencao-completa.md`

### Exemplos de Uso Correto

**✅ CENÁRIOS IDEAIS:**
1. Adicionar traduções mockadas em 2 arquivos `.spec.ts` (Frontend)
2. Corrigir configuração EF Core em 1 arquivo (Infrastructure)
3. Adicionar provider HttpClient em 1 teste unitário (Frontend)
4. Ajustar mock de Router em 1 arquivo `.spec.ts` (Frontend)
5. Corrigir typo em 2 handlers (Application)

**❌ CENÁRIOS INADEQUADOS:**
1. Renomear propriedade usada em 10 arquivos → Use `manutencao-completa.md`
2. Corrigir duplicação cross-layer → Use `manutencao-completa.md`
3. Refatorar padrão em múltiplos handlers → Use `manutencao-completa.md`

---

## 3. ESCOPO PERMITIDO

### 3.1. Alterações Permitidas

✅ **PERMITIDO:**
- Alterar **1-3 arquivos** em uma única camada
- Adicionar mocks de dependências em testes
- Corrigir configurações pontuais (EF Core, Angular, etc)
- Ajustar valores/strings hardcoded
- Adicionar providers faltantes
- Corrigir imports/exports
- Atualizar testes afetados pela correção

❌ **PROIBIDO:**
- Alterar **4+ arquivos** (ultrapassar escopo cirúrgico)
- Alterar **múltiplas camadas** (cross-layer)
- Refatorar código (renomear, reestruturar)
- Tomar **decisões arquiteturais** (escolher entre padrões)
- Adicionar **novas funcionalidades**
- Modificar **lógica de negócio** além do necessário

---

## 4. COMANDOS PRÉ-VALIDADOS

### 4.1. Windows (Git Bash)

```bash
# Navegação (sintaxe correta para Windows)
cd /d/IC2/frontend/icontrolit-app
cd /d/IC2/backend/IControlIT.API

# Build backend
cd /d/IC2/backend/IControlIT.API && dotnet build --no-incremental 2>&1 | tail -30

# Build frontend
cd /d/IC2/frontend/icontrolit-app && npm run build 2>&1 | tail -50

# Testes backend
cd /d/IC2/backend/IControlIT.API && dotnet test --no-build 2>&1 | tail -50

# Testes frontend
cd /d/IC2/frontend/icontrolit-app && npm run test -- --watch=false 2>&1 | tail -50

# Verificar processos rodando
ps aux | grep -E "dotnet|node" | grep -v grep
```

### 4.2. PowerShell

```powershell
# Matar processos travados (se necessário)
Get-Process -Name "*IControlIT*","node" -ErrorAction SilentlyContinue | Stop-Process -Force

# Alternativa usando taskkill
taskkill /F /IM "IControlIT.API.exe" 2>$null
taskkill /F /IM "node.exe" 2>$null
```

### 4.3. Validação de Caminhos

**REGRA CRÍTICA:** Sempre usar sintaxe Unix-style em Git Bash Windows:

```bash
# ❌ INCORRETO (Git Bash Windows)
cd /d D:\IC2\frontend

# ✅ CORRETO (Git Bash Windows)
cd /d/IC2/frontend
```

---

## 5. TIMEOUTS OBRIGATÓRIOS

| Comando | Timeout | Ação se Exceder |
|---------|---------|-----------------|
| `dotnet build` | 3 minutos | ABORTAR (build travado) |
| `npm run build` | 5 minutos | ABORTAR (build travado) |
| `dotnet test` | 10 minutos | ABORTAR (testes travados) |
| `npm run test` | 5 minutos | ABORTAR (testes travados) |

**OBRIGATÓRIO:** Todos os comandos de build/testes devem ter timeout explícito.

**SE timeout excedido:**
1. ❌ ABORTAR comando
2. Reportar em `.temp_ia/ERRO-TIMEOUT-[COMANDO]-[DATA].md`
3. Informar usuário com contexto completo:
   - Comando executado
   - Tempo decorrido
   - Saída capturada (últimas 50 linhas)
   - Processo travado (se identificado)

---

## 6. WORKFLOW OBRIGATÓRIO

### FASE 0: PREPARAÇÃO DO BRANCH (OBRIGATÓRIA)

**🚨 REGRA CRÍTICA: Branch de Correção Dedicado**

Toda manutenção/correção **DEVE** ser executada em um branch dedicado criado automaticamente.

#### PASSO 0.1: Extrair RF do Prompt

**Analisar o prompt e extrair RF afetado:**

```bash
# Padrão no prompt: "**RF Afetado:** RF006" ou "RF006 - Gestão de Clientes"
# Extrair apenas o número (ex: RF006 → 006 ou RF006)
```

**SE RF não identificado no prompt:**
- Usar `correcao/GENERIC-{timestamp}` como nome do branch
- Exemplo: `correcao/GENERIC-20260108173045`

#### PASSO 0.2: Criar e Fazer Checkout do Branch

**Executar OBRIGATORIAMENTE:**

```bash
# 1. Ir para raiz do projeto de código (D:\IC2)
cd /d/IC2

# 2. Verificar branch atual
CURRENT_BRANCH=$(git branch --show-current)
echo "Branch atual: $CURRENT_BRANCH"

# 3. Extrair RF e descrição do prompt
RF_NUMBER="RF006"  # Extrair do prompt (ex: "RF Afetado: RF006")
DESCRICAO_BREVE="corrigindo-hierarquia-tenant"  # Extrair do "Descrição:" do prompt

# 4. Normalizar RF para lowercase (RF006 → rf006)
RF_LOWER=$(echo "$RF_NUMBER" | tr '[:upper:]' '[:lower:]')

# 5. Normalizar descrição (remover acentos, espaços → hífens, max 50 chars)
DESC_NORMALIZED=$(echo "$DESCRICAO_BREVE" | tr '[:upper:]' '[:lower:]' | sed 's/ /-/g' | sed 's/[^a-z0-9-]//g' | cut -c1-50)

# 6. Definir nome do branch (convenção: fix/rfXXX-descricao-curta)
BRANCH_NAME="fix/${RF_LOWER}-${DESC_NORMALIZED}"
echo "Branch de correção: $BRANCH_NAME"

# 7. Verificar se branch já existe
if git show-ref --verify --quiet refs/heads/"$BRANCH_NAME"; then
  echo "✅ Branch $BRANCH_NAME já existe, fazendo checkout..."
  git checkout "$BRANCH_NAME"
  BRANCH_ACTION="selecionado"
else
  echo "Branch $BRANCH_NAME não existe, criando..."
  git checkout -b "$BRANCH_NAME"
  BRANCH_ACTION="criado"
fi

# 8. Validar que estamos no branch correto
NEW_BRANCH=$(git branch --show-current)
if [ "$NEW_BRANCH" != "$BRANCH_NAME" ]; then
  echo "❌ ERRO: Branch não está ativo"
  echo "Esperado: $BRANCH_NAME"
  echo "Atual: $NEW_BRANCH"
  exit 1
fi

echo "✅ Branch $BRANCH_NAME ativo ($BRANCH_ACTION)"
if [ "$BRANCH_ACTION" = "criado" ]; then
  echo "✅ Base: $CURRENT_BRANCH"
fi
```

**Saída esperada (branch novo):**
```
Branch atual: dev
Branch de correção: fix/rf006-corrigindo-hierarquia-tenant
Branch fix/rf006-corrigindo-hierarquia-tenant não existe, criando...
Switched to a new branch 'fix/rf006-corrigindo-hierarquia-tenant'
✅ Branch fix/rf006-corrigindo-hierarquia-tenant ativo (criado)
✅ Base: dev
```

**Saída esperada (branch existente - múltiplas correções do mesmo RF):**
```
Branch atual: dev
Branch de correção: fix/rf006-corrigindo-hierarquia-tenant
✅ Branch fix/rf006-corrigindo-hierarquia-tenant já existe, fazendo checkout...
Switched to branch 'fix/rf006-corrigindo-hierarquia-tenant'
✅ Branch fix/rf006-corrigindo-hierarquia-tenant ativo (selecionado)
```

**Exemplos de nomes de branch:**
- `fix/rf006-corrigindo-hierarquia-tenant`
- `fix/rf010-preview-imagem-upload`
- `fix/rf008-alinhamento-botao-cnpj`
- `fix/generic-incompatibilidade-int64-int32` (quando RF não identificado)

#### PASSO 0.3: Documentar Branch em .temp_ia

**Criar arquivo de rastreamento:**

```bash
cat > /d/IC2/.temp_ia/BRANCH-CORRECAO-${RF_NUMBER}.md <<EOF
# BRANCH DE CORREÇÃO: ${BRANCH_NAME}

**Data:** $(date +"%Y-%m-%d %H:%M:%S")
**RF Afetado:** ${RF_NUMBER}
**Branch Base:** ${CURRENT_BRANCH}
**Branch Correção:** ${BRANCH_NAME}

## Prompt Original
${PROMPT_COMPLETO}

## Status
- [ ] Correção em andamento
- [ ] Testes executados
- [ ] Validação completa
- [ ] Pronto para merge

## Commits Realizados
(Serão adicionados durante execução)
EOF
```

**IMPORTANTE:**
- Branch permanece ativo para TODAS as correções do RF
- Não fazer checkout de volta para `main` ou `dev`
- Apenas ao final (após validação completa) fazer merge

#### PASSO 0.4: Validação de Sucesso

**Critérios de aprovação FASE 0:**
- [x] RF extraído do prompt (ou GENERIC usado)
- [x] Branch `correcao/RF{ID}` criado
- [x] Checkout realizado para o novo branch
- [x] Branch ativo confirmado com `git branch --show-current`
- [x] Arquivo de rastreamento criado em `.temp_ia/`

**SE qualquer validação falhar:**
- ❌ PARAR execução imediatamente
- ❌ NÃO prosseguir para FASE 1
- ✅ Reportar erro ao usuário
- ✅ Aguardar correção manual

---

### FASE 1: VALIDAÇÃO DE PRÉ-REQUISITOS (OBRIGATÓRIA)

#### PASSO 1.1: Validar Escopo Cirúrgico

**ANTES de iniciar qualquer correção, validar:**

```bash
# 1. Quantos arquivos serão afetados?
#    - Se <= 3 arquivos: ✅ CONTINUAR
#    - Se > 3 arquivos: ❌ ESCALAR → usar manutencao-completa.md

# 2. Quantas camadas serão afetadas?
#    - Se 1 camada: ✅ CONTINUAR
#    - Se 2+ camadas: ❌ ESCALAR → usar manutencao-completa.md

# 3. Refatoração necessária?
#    - Se NÃO: ✅ CONTINUAR
#    - Se SIM: ❌ ESCALAR → usar manutencao-completa.md

# 4. Todos os arquivos mencionados no prompt podem ser corrigidos?
#    - Ler prompt e listar TODOS os arquivos mencionados
#    - Validar que TODOS estão dentro do escopo (1-3 arquivos, 1 camada)
```

**🚨 REGRA CRÍTICA: ESCALAÇÃO AUTOMÁTICA DE CONTRATO**

**SE qualquer validação falhar:**

1. ❌ **NÃO PARAR** a execução
2. ✅ **ESCALAR automaticamente** para contrato adequado:
   - 4-10 arquivos OU múltiplas camadas → `manutencao-completa.md`
   - > 10 arquivos OU refatoração complexa → `manutencao-avancada.md`
3. ✅ Documentar escalação em `.temp_ia/ESCALACAO-CONTRATO-[DATA].md`
4. ✅ Continuar execução com novo contrato
5. ✅ Informar no commit final qual contrato foi utilizado

**PROIBIDO:**
- ❌ Parar execução e pedir permissão ao usuário
- ❌ Tentar forçar escopo cirúrgico quando inadequado
- ❌ Fazer commit sem informar escalação

**🚨 REGRA CRÍTICA: LISTA DE ARQUIVOS DO PROMPT**

O agente DEVE criar lista explícita de TODOS os arquivos que o prompt solicita corrigir:

```markdown
**ARQUIVOS DO PROMPT (TODOS devem ser corrigidos):**
1. [ ] Arquivo 1: [caminho completo]
2. [ ] Arquivo 2: [caminho completo]
...

**CRITÉRIO DE CONCLUSÃO:**
- ✅ TODOS os arquivos da lista acima devem estar marcados como [x]
- ✅ TODOS os testes relacionados ao problema do escopo devem passar (100%)
- ❌ NÃO fazer commit se algum arquivo não foi corrigido completamente
- ❌ NÃO considerar "escopo parcialmente concluído"
```

**Exemplo de escalação:**

```markdown
# ESCALAÇÃO DE CONTRATO DETECTADA

**Contrato inicial:** manutencao-controlada.md (1-3 arquivos, 1 camada)

**Motivo da escalação:**
- Prompt solicita correção em 5 arquivos
- Limite cirúrgico: 3 arquivos
- Decisão: ESCALAR para manutencao-completa.md

**Novo contrato:** manutencao-completa.md
**Execução:** Prosseguindo automaticamente
```

#### PASSO 1.2: Criar Análise de Impacto Mínima

Criar arquivo em `.temp_ia/ANALISE-IMPACTO-[PROBLEMA].md`:

```markdown
# ANÁLISE DE IMPACTO - [PROBLEMA]

## VALIDAÇÃO DE ESCOPO CIRÚRGICO

- ✅ Arquivos afetados: 2 (limite: 3)
- ✅ Camadas afetadas: 1 (Frontend - Unit Tests)
- ✅ Refatoração necessária: NÃO
- ✅ Decisões arquiteturais: NÃO

**ESCOPO APROVADO PARA MANUTENÇÃO CONTROLADA**

## ARQUIVOS AFETADOS

1. [ ] `frontend/icontrolit-app/src/app/modules/auth/sign-in/sign-in.component.spec.ts`
   - Tipo: Unit Test
   - Alteração: Adicionar traduções mockadas
   - Risco: Nenhum (apenas testes)

2. [ ] `frontend/icontrolit-app/src/app/modules/admin/management/users/list/list.component.spec.ts`
   - Tipo: Unit Test
   - Alteração: Adicionar traduções mockadas
   - Risco: Nenhum (apenas testes)

## SOLUÇÃO

- **Tipo:** Correção pontual
- **Complexidade:** Baixa
- **Tempo estimado:** 15-30 minutos
- **Risco:** Nenhum (não afeta produção)
```

---

### FASE 2: EXECUÇÃO DA CORREÇÃO

**LEMBRETE:** Usar comandos pré-validados da Seção 4 e respeitar timeouts da Seção 5.

#### PASSO 2.1: Aplicar Correção nos Arquivos

**Para CADA arquivo:**

1. ✅ Ler arquivo completo
2. ✅ Aplicar correção pontual
3. ✅ Validar sintaxe (lint/build)
4. ✅ **OBRIGATÓRIO:** Executar testes APENAS deste arquivo
5. ✅ **OBRIGATÓRIO:** Validar que correção RESOLVEU o problema
6. ✅ Marcar como concluído no checklist SOMENTE se validação passou

**🚨 REGRA CRÍTICA: VALIDAÇÃO INCREMENTAL OBRIGATÓRIA**

Após corrigir CADA arquivo, executar testes específicos:

```bash
# Frontend (exemplo)
cd /d/IC2/frontend/icontrolit-app && timeout 300 npm run test -- --watch=false --include='**/*[nome-do-arquivo].spec.ts' 2>&1 | tail -80

# Backend (exemplo)
cd /d/IC2/backend/IControlIT.API && timeout 600 dotnet test --filter "FullyQualifiedName~[NomeDoArquivo]" 2>&1 | tail-50
```

**INTERPRETAÇÃO DO RESULTADO:**

**Cenário A: Testes melhoraram (problema resolvido)**
```
Antes: 20/27 testes falhando por [PROBLEMA DO ESCOPO]
Depois: 27/27 testes passando (100%)
```
✅ **AÇÃO:** Marcar arquivo como [x] concluído e prosseguir para próximo arquivo

---

**Cenário B: Testes melhoraram parcialmente**
```
Antes: 20/27 testes falhando por [PROBLEMA DO ESCOPO]
Depois: 10/27 testes ainda falhando por [PROBLEMA DO ESCOPO]
```
⚠️ **AÇÃO:**
1. Revisar correção aplicada
2. Identificar o que ainda falta
3. Aplicar correção adicional
4. Re-executar testes
5. Só marcar como concluído quando 100% do problema do escopo estiver resolvido

---

**Cenário C: Testes NÃO melhoraram (erro DIFERENTE está bloqueando)**
```
Antes: 20/27 testes falhando por [PROBLEMA DO ESCOPO]
Depois: 27/27 testes falhando por [ERRO DIFERENTE] (ex: FUSE_APP_CONFIG, NullInjectorError)
```
🔴 **AÇÃO OBRIGATÓRIA:**

1. ❌ **NÃO** marcar arquivo como concluído
2. ❌ **NÃO** prosseguir para próximo arquivo ainda
3. ✅ Identificar se [ERRO DIFERENTE] impede validação do problema do escopo
4. ✅ Avaliar se correção de [ERRO DIFERENTE] está dentro do escopo cirúrgico:

```bash
# Perguntas críticas:
# - Correção de [ERRO DIFERENTE] afeta quantos arquivos? (≤ 3?)
# - Correção de [ERRO DIFERENTE] afeta quantas camadas? (= 1?)
# - Correção de [ERRO DIFERENTE] exige refatoração? (NÃO?)
```

**SE correção de [ERRO DIFERENTE] está DENTRO do escopo cirúrgico:**
- ✅ Corrigir [ERRO DIFERENTE] no mesmo arquivo
- ✅ Re-executar testes
- ✅ Validar que problema do escopo original foi resolvido
- ✅ Marcar arquivo como concluído

**SE correção de [ERRO DIFERENTE] está FORA do escopo cirúrgico:**
- ❌ **ESCALAR automaticamente** para `manutencao-completa.md` ou `manutencao-avancada.md`
- ✅ Documentar escalação em `.temp_ia/ESCALACAO-CONTRATO-[DATA].md`
- ✅ Continuar execução com novo contrato
- ✅ Informar escalação no commit final

---

**Cenário D: Testes PIORARAM**
```
Antes: 20/27 testes falhando
Depois: 25/27 testes falhando
```
🔴 **AÇÃO:**
1. ❌ REVERTER correção aplicada
2. Revisar abordagem (pode estar corrigindo coisa errada)
3. Re-ler prompt original para confirmar escopo
4. Aplicar correção revisada
5. Re-executar testes

---

**PROIBIDO:**
- ❌ Marcar arquivo como "concluído" sem executar testes
- ❌ Prosseguir para próximo arquivo se correção não funcionou
- ❌ Ignorar erros bloqueantes sem tentar corrigir ou escalar
- ❌ Assumir que "adicionei o código" = "problema resolvido"

#### PASSO 2.2: Validação Contínua

**Após CADA alteração:**

```bash
# Frontend
npm run build  # Exit code 0 → SUCESSO

# Backend
dotnet build   # Exit code 0 → SUCESSO
```

---

### FASE 3: VALIDAÇÃO FINAL

**LEMBRETE:** Usar comandos pré-validados da Seção 4 e respeitar timeouts da Seção 5.

#### PASSO 3.1: Executar Testes Afetados

```bash
# Se alterou testes frontend
npm run test -- --watch=false

# Se alterou testes backend
dotnet test
```

**Critério de Aprovação:**
- ✅ **100% dos testes passando**
- ❌ Se qualquer teste FALHAR: BLOQUEAR commit

#### PASSO 3.2: Validação de Build Completo

```bash
# Backend
dotnet build --no-incremental

# Frontend
npm run build
```

**Critério de Aprovação:**
- ✅ Build backend: **SUCESSO**
- ✅ Build frontend: **SUCESSO**

---

### FASE 4: COMMIT E DOCUMENTAÇÃO

#### PASSO 4.1: Commit Estruturado

```bash
git add [arquivos alterados]

git commit -m "$(cat <<'EOF'
fix([camada]): [descrição concisa da correção]

PROBLEMA IDENTIFICADO:
- [Descrição do problema]
- [Testes falhando ou erro específico]

CORREÇÃO APLICADA:
- [Arquivo 1]: [O que foi alterado]
- [Arquivo 2]: [O que foi alterado]

RESULTADOS:
- Build: SUCESSO
- Testes: [X/Y] (100%)

IMPACTO:
- Arquivos alterados: [N]
- Camadas afetadas: 1 ([Nome da camada])
- Tipo: Correção cirúrgica
- Risco: [Nenhum/Baixo]

TIPO DE MANUTENÇÃO: Controlada (cirúrgica)
CONTRATO: contracts/manutencao/manutencao-controlada.md

🤖 Generated with Claude Code
Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"
```

#### PASSO 4.2: Documentação (OPCIONAL para correções menores)

Para correções triviais (ex: adicionar mock), documentação em DECISIONS.md é **OPCIONAL**.

Para correções que envolvem decisões (mesmo pequenas), documentar:

```markdown
### [DATA] Correção de [PROBLEMA]

**Contexto:** [Por que a correção foi necessária]

**Decisão:** [O que foi decidido]
- Razão: [Justificativa técnica]
- Alternativas: [O que NÃO foi feito]
- Impacto: [Arquivos afetados]

**Tipo de Manutenção:** Controlada (cirúrgica)
**Contrato:** `manutencao-controlada.md`
```

---

## 7. REGRAS DE DECISÕES TÉCNICAS

### 7.1. Quando Decisões SÃO BLOQUEADAS

❌ **PARAR e ALERTAR se precisar decidir:**
- Escolher entre múltiplos padrões arquiteturais
- Definir nova estrutura de código
- Escolher entre bibliotecas/frameworks
- Alterar arquitetura existente
- Criar novo padrão

**Nesses casos:**
- **NÃO** prossiga
- Informe ao usuário que decisão arquitetural é necessária
- Recomende `manutencao-completa.md` ou consulta ao time

### 7.2. Quando Decisões SÃO PERMITIDAS

✅ **PERMITIDO decidir (sem parar):**
- Nome de variável mock (ex: `mockRouter` vs `routerMock`)
- Ordem de providers em array
- Formatação de código (seguindo lint)
- Mensagem de erro específica
- Valores literais em mocks

**Nesses casos:** Decidir silenciosamente seguindo convenções existentes.

---

## 8. PROIBIÇÕES ABSOLUTAS

### 8.1. Proibições de Escopo

❌ **NUNCA:**
- Alterar 4+ arquivos (bloquear e recomendar `manutencao-completa.md`)
- Alterar múltiplas camadas (bloquear e recomendar `manutencao-completa.md`)
- Refatorar código além da correção pontual
- Adicionar features novas
- Modificar lógica de negócio além do necessário

### 8.2. Proibições de Git/Commits

❌ **NUNCA:**
- Fazer commits em `dev` sem branch dedicado (se RF específico)
- Fazer commits sem validar builds/testes
- Fazer commits com testes falhando

✅ **SEMPRE:**
- Validar builds ANTES de commit
- Validar testes ANTES de commit
- Commit message estruturado

---

## 9. CRITÉRIO DE PRONTO

O contrato só é considerado CONCLUÍDO quando:

### 9.1. Correção Aplicada

- [ ] Escopo validado (1-3 arquivos, 1 camada)
- [ ] Análise de impacto criada
- [ ] Correções aplicadas em todos os arquivos
- [ ] Compilação validada (exit code 0)

### 9.2. Validação Técnica

- [ ] Build: **SUCESSO**
- [ ] Testes afetados: **100% passando**
- [ ] Nenhum warning bloqueante

**🚨 DEFINIÇÃO RIGOROSA DE "100% PASSANDO":**

**"Testes afetados"** significa:
- ✅ **TODOS** os testes que falhavam pelo problema do escopo DEVEM estar passando
- ✅ **TODOS** os arquivos mencionados no prompt DEVEM ter seus testes passando
- ❌ **NÃO** significa "alguns testes passaram"
- ❌ **NÃO** significa "melhorou de 0/27 para 31/33"

**Exemplo Correto:**
```
PROMPT: Corrigir Transloco em AuthSignInComponent.spec.ts (31 testes) e UsersListComponent.spec.ts (27 testes)

ANTES: 0/58 testes passando (31+27 falhando por NullInjectorError: TranslocoService)
DEPOIS: 58/58 testes passando (31+27 resolvidos)

✅ CRITÉRIO ATENDIDO: 100% dos testes afetados pelo problema do escopo
```

**Exemplo Incorreto:**
```
PROMPT: Corrigir Transloco em AuthSignInComponent.spec.ts (31 testes) e UsersListComponent.spec.ts (27 testes)

ANTES: 0/58 testes passando (31+27 falhando por NullInjectorError: TranslocoService)
DEPOIS: 31/58 testes passando (31 AuthSignIn OK, 27 UsersList falhando por FUSE_APP_CONFIG)

❌ CRITÉRIO NÃO ATENDIDO: Apenas 53% dos testes afetados passando
❌ UsersListComponent.spec.ts ainda está no escopo do prompt e deve ser corrigido
```

**REGRA FINAL:**

- **SE** todos os arquivos mencionados no prompt estão 100% passando: ✅ PRONTO
- **SE** algum arquivo do prompt ainda tem testes falhando:
  - **SE** erro bloqueante está dentro do escopo cirúrgico: ✅ Corrigir
  - **SE** erro bloqueante está fora do escopo cirúrgico: ✅ Escalar automaticamente para `manutencao-completa.md`
- **NUNCA** considerar "pronto" com arquivos do prompt falhando por qualquer motivo

### 9.3. Documentação

- [ ] Commit estruturado com contexto completo
- [ ] Análise de impacto salva em `.temp_ia/`
- [ ] (Opcional) DECISIONS.md atualizado se decisões foram tomadas

### 9.4. Entrega

- [ ] Branch pronto para merge (se aplicável)
- [ ] Nenhuma violação de contrato
- [ ] Escopo não ultrapassou limites (1-3 arquivos, 1 camada)

---

## 10. TROUBLESHOOTING

### Problema: "cd: too many arguments"

**Causa:** Sintaxe bash incorreta para Windows.

**Solução:** Usar `/d/IC2` em vez de `/d D:\IC2`.

```bash
# ❌ INCORRETO (Windows Git Bash)
cd /d D:\IC2\frontend

# ✅ CORRETO (Windows Git Bash)
cd /d/IC2/frontend
```

**Referência:** Seção 4.3 (Validação de Caminhos)

---

### Problema: "Get-Process: command not found"

**Causa:** Comando PowerShell executado em bash.

**Solução:** Executar em PowerShell ou usar alternativa bash:

```bash
# Alternativa bash (Git Bash)
taskkill //F //IM "IControlIT.API.exe" 2>/dev/null || true
taskkill //F //IM "node.exe" 2>/dev/null || true
```

**Referência:** Seção 4.2 (PowerShell)

---

### Problema: Build travado (sem saída por > 3 minutos)

**Causa:** Processo anterior não finalizado corretamente.

**Solução:**

```bash
# 1. Matar processos travados
taskkill //F //IM "dotnet.exe" 2>/dev/null || true
taskkill //F //IM "node.exe" 2>/dev/null || true

# 2. Limpar cache (se necessário)
cd /d/IC2/backend/IControlIT.API && dotnet clean
cd /d/IC2/frontend/icontrolit-app && rm -rf node_modules/.cache

# 3. Re-executar build
dotnet build --no-incremental
npm run build
```

**Referência:** Seção 5 (Timeouts Obrigatórios)

---

### Problema: "npm ERR! missing script: test"

**Causa:** package.json sem script `test` configurado.

**Solução:** Verificar `package.json`:

```bash
# Listar scripts disponíveis
npm run

# Se não houver script "test", usar alternativa
npm run test:unit
# OU
npm run test:ci
```

---

### Problema: Testes falhando após correção

**Causa:** Build incremental usando cache desatualizado.

**Solução:**

```bash
# Backend: build completo (sem cache)
dotnet build --no-incremental
dotnet test --no-build

# Frontend: limpar cache e rebuild
rm -rf node_modules/.cache
npm run build
npm run test -- --watch=false
```

---

### Problema: Correção aplicada mas testes ainda falhando por erro DIFERENTE

**Cenário Real (Execução 8 RF006):**
```
PROMPT: Corrigir Transloco em AuthSignInComponent.spec.ts e UsersListComponent.spec.ts

PASSO 1: Corrigir AuthSignInComponent
- ANTES: 0/31 testes (NullInjectorError: TranslocoService)
- DEPOIS: 31/31 testes (✅ RESOLVIDO)

PASSO 2: Corrigir UsersListComponent
- ANTES: 0/27 testes (NullInjectorError: TranslocoService)
- CORREÇÃO APLICADA: Adicionado getTranslocoModule()
- DEPOIS: 0/27 testes (NullInjectorError: FUSE_APP_CONFIG) ← ERRO DIFERENTE

❌ ERRO: Agente marcou como "pronto" porque "problema do Transloco foi resolvido"
✅ CORRETO: Agente deveria ter escalado para manutencao-completa.md
```

**Causa:** Correção do problema original (Transloco) revelou erro bloqueante diferente (FUSE_APP_CONFIG) que impede validação.

**Diagnóstico:**

1. **Identificar se erro diferente está dentro do escopo cirúrgico:**
   - ✅ DENTRO: Erro pode ser resolvido no mesmo arquivo sem refatoração (ex: adicionar mais um provider)
   - ❌ FORA: Erro requer alterações em múltiplos arquivos ou camadas (ex: criar mock global de FUSE_APP_CONFIG)

2. **Aplicar regra de decisão:**

**SE erro diferente está DENTRO do escopo:**
```bash
# Corrigir no mesmo arquivo e re-executar testes
# Exemplo: FUSE_APP_CONFIG pode ser mockado localmente
```
✅ **AÇÃO:** Corrigir e validar que arquivo está 100% passando.

**SE erro diferente está FORA do escopo:**
```bash
# Exemplo: FUSE_APP_CONFIG requer mock global em test-setup.ts (múltiplos arquivos)
```
❌ **AÇÃO:** ESCALAR automaticamente para `manutencao-completa.md` ou `manutencao-avancada.md`.

**Solução Geral:**

1. ✅ **NUNCA** marcar arquivo como "pronto" se testes ainda falhando
2. ✅ Validar que correção EFETIVAMENTE resolveu o problema (testes 100% passando)
3. ✅ Se erro bloqueante diferente impede validação:
   - **SE** dentro do escopo cirúrgico: Corrigir
   - **SE** fora do escopo cirúrgico: Escalar automaticamente
4. ❌ **NUNCA** considerar "problema do escopo resolvido" se testes não passam

**Referência:** Seção 6 (PASSO 2.1 - Validação Incremental), Seção 9.2 (Definição de "100% Passando")

---

### Problema: "Error: Timeout of X ms exceeded"

**Causa:** Testes assíncronos sem timeout adequado.

**Solução:**

1. **NÃO** aumentar timeout globalmente (pode mascarar problemas)
2. Identificar teste específico que está travando
3. Reportar em `.temp_ia/ERRO-TIMEOUT-TESTE-[NOME].md`
4. Informar usuário para investigação manual

---

## 11. EXEMPLO PRÁTICO

### Cenário Real: Traduções Transloco Mockadas (RF006)

**Problema:**
- 31 testes frontend falhando
- Erro: `Expected 'auth.signIn.form.validating' to be 'Validando credenciais...'`
- Causa: TranslocoTestingModule com `langs: {}` vazios

**Análise de Escopo:**
- Arquivos afetados: 2 (`.spec.ts`)
- Camadas afetadas: 1 (Frontend - Unit Tests)
- Refatoração: NÃO
- Decisões arquiteturais: NÃO

**Decisão:**
- ✅ Usar **Manutenção Controlada** (escopo cirúrgico)
- ❌ Não usar Manutenção Completa (desnecessário)

**Execução:**
1. Criar análise de impacto
2. Identificar chaves de tradução
3. Adicionar traduções mockadas em 2 arquivos
4. Validar testes: 60/60 (100%)
5. Commit estruturado

**Resultado:**
- ✅ 2 arquivos corrigidos
- ✅ Builds: SUCESSO
- ✅ Testes: 60/60 (100%)
- ✅ Branch: `dev`

---

## 12. REGRA DE NEGAÇÃO ZERO

Se uma solicitação:
- **Ultrapassar 3 arquivos**, ou
- **Afetar múltiplas camadas**, ou
- **Exigir refatoração**

ENTÃO:

- A execução DEVE ser **NEGADA**
- Nenhuma ação parcial pode ser realizada
- Recomendar `manutencao-completa.md`

---

## 13. PROMPTS DE ATIVAÇÃO

### Prompt Direto (com arquivo específico)

```
Corrija [PROBLEMA] conforme o prompt D:\IC2\.temp_ia\PROMPT-CORRECAO-[...].md

Contrato: D:\IC2_Governanca\governanca\contracts\manutencao\manutencao-controlada.md

Modo autonomia total. Não perguntar confirmações. Executar todas as fases automaticamente.
```

### Prompt Genérico (sem arquivo)

```
Execute manutenção controlada para corrigir [PROBLEMA] em [ARQUIVOS]:

Contrato: D:\IC2_Governanca\governanca\contracts\manutencao\manutencao-controlada.md

PROBLEMA:
- [Descrição]

ARQUIVOS AFETADOS:
- [Lista de arquivos (máximo 3)]

CAMADA: [Nome da camada única]

SOLUÇÃO ESPERADA:
- [Descrição da correção]

Modo autonomia total.
```

---

**FIM DO CONTRATO**
