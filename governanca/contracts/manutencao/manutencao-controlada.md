# CONTRATO DE MANUTENÇÃO CONTROLADA (CIRÚRGICA)

**Versão:** 1.1
**Data:** 2026-01-08
**Status:** Ativo
**Última Atualização:** 2026-01-08 (Adicionadas seções 4, 5 e 10)

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

### FASE 1: VALIDAÇÃO DE PRÉ-REQUISITOS (OBRIGATÓRIA)

#### PASSO 1.1: Validar Escopo Cirúrgico

**ANTES de iniciar qualquer correção, validar:**

```bash
# 1. Quantos arquivos serão afetados?
#    - Se <= 3 arquivos: ✅ CONTINUAR
#    - Se > 3 arquivos: ❌ BLOQUEAR → usar manutencao-completa.md

# 2. Quantas camadas serão afetadas?
#    - Se 1 camada: ✅ CONTINUAR
#    - Se 2+ camadas: ❌ BLOQUEAR → usar manutencao-completa.md

# 3. Refatoração necessária?
#    - Se NÃO: ✅ CONTINUAR
#    - Se SIM: ❌ BLOQUEAR → usar manutencao-completa.md
```

**SE qualquer validação falhar:**
- ❌ **PARAR IMEDIATAMENTE**
- Informar ao usuário que o escopo ultrapassou o contrato
- Recomendar `manutencao-completa.md`

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
4. ✅ Marcar como concluído no checklist

**REGRA CRÍTICA:** NÃO prosseguir para próximo arquivo se compilação falhar.

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
