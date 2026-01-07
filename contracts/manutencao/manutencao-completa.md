# CONTRATO DE MANUTENÇÃO COMPLETA

**Versão:** 1.0
**Data:** 2026-01-06
**Status:** Ativo

---

## 📋 SUMÁRIO EXECUTIVO

### ⚡ O que este contrato faz

Este contrato permite **MANUTENÇÕES AMPLAS E CROSS-LAYER** que exigem alterações em múltiplos arquivos e camadas.

**Diferença em relação ao Contrato de Manutenção Controlada:**

| Aspecto | Manutenção Controlada | Manutenção Completa |
|---------|----------------------|---------------------|
| **Escopo** | ❌ Cirúrgico (1-3 arquivos) | ✅ Amplo (múltiplos arquivos/camadas) |
| **Camadas** | ❌ Limitado a 1 camada | ✅ Cross-layer (Domain + Application + Infrastructure + Web) |
| **Refatoração** | ❌ Proibida | ✅ Permitida (se necessária para correção) |
| **Decisões** | ❌ Bloqueadas (parar e alertar) | ✅ Permitidas (com justificativa técnica) |
| **Exemplos** | Corrigir typo, adicionar validação | Refatorar renomeação cross-layer, corrigir duplicações complexas |

---

## 1. Identificação do Agente

| Campo | Valor |
|-------|-------|
| **Papel** | Agente de Manutenção Completa |
| **Escopo** | Correções amplas, cross-layer, refatorações necessárias |
| **Modo** | Autonomia técnica com justificativas obrigatórias |

---

## 2. Ativação do Contrato

Este contrato é ativado quando a solicitação mencionar explicitamente:

> **"Conforme contracts/desenvolvimento/manutencao/manutencao-completa.md"**

**OU quando o usuário solicitar via prompt:**

> **"Execute D:\IC2_Governanca\prompts\desenvolvimento\manutencao\manutencao-completa.md"**

### Quando Usar Este Contrato

✅ **USE quando:**
- Correção exige alterações em **múltiplos arquivos** (10+ arquivos)
- Correção exige alterações em **múltiplas camadas** (Domain + Application + Infrastructure)
- Refatoração é **necessária** para corrigir o problema (ex: renomeação cross-layer)
- Decisões técnicas são **inevitáveis** (escolha entre múltiplas soluções)
- **Contrato de Manutenção Controlada BLOQUEOU** por ultrapassar escopo

❌ **NÃO USE quando:**
- Correção é **cirúrgica** (1-3 arquivos) → Use `manutencao-controlada.md`
- Correção é **limitada a 1 camada** → Use `manutencao-controlada.md`
- Refatoração é **opcional** → Use `manutencao-controlada.md`

---

## 3. ESCOPO PERMITIDO

### 3.1. Alterações Permitidas

✅ **PERMITIDO:**
- Alterar **10+ arquivos** em múltiplas camadas
- Refatorar código **se necessário** para correção
- Renomear propriedades/campos cross-layer
- Corrigir duplicações complexas
- Atualizar mapeamentos (AutoMapper, EF Core Configuration)
- Corrigir handlers, validators, DTOs, commands, queries
- Atualizar testes afetados
- Tomar **decisões técnicas justificadas**

❌ **PROIBIDO:**
- Adicionar **novas funcionalidades** (features)
- Alterar **arquitetura** do sistema
- Modificar **contratos de API** públicos (breaking changes)
- Refatorar código **não relacionado** ao problema
- Alterar **lógica de negócio** além do necessário

---

## 4. WORKFLOW OBRIGATÓRIO

### FASE 1: ANÁLISE DE IMPACTO (OBRIGATÓRIA)

#### PASSO 1.1: Identificar Arquivos Afetados

```bash
# 1. Identificar todos os arquivos que referenciam o código problemático
grep -r "NomeDaPropriedade" D:\IC2\backend\
grep -r "NomeDaClasse" D:\IC2\backend\

# 2. Listar arquivos por camada
# Domain: Entidades, Enums, Constants
# Application: Commands, Queries, Handlers, Validators, DTOs
# Infrastructure: Configurations, Repositories
# Web: Endpoints
```

#### PASSO 1.2: Mapear Dependências

Criar arquivo de análise em `.temp_ia/ANALISE-IMPACTO-[PROBLEMA].md`:

```markdown
# ANÁLISE DE IMPACTO - [PROBLEMA]

## ARQUIVOS AFETADOS

### Domain Layer
- [ ] Fornecedor.cs (duplicação de Id_Fornecedor)
- [ ] Ativo.cs (referência a Id_Fornecedor)

### Application Layer
- [ ] CreateAtivoCommand.cs
- [ ] UpdateAtivoCommand.cs
- [ ] GetFornecedoresQuery.cs
- [ ] (lista completa...)

### Infrastructure Layer
- [ ] FornecedorConfiguration.cs
- [ ] IApplicationDbContext.cs

### Web Layer
- [ ] FornecedoresEndpoints.cs

## IMPACTO ESTIMADO

- **Arquivos afetados:** 15
- **Camadas afetadas:** 4 (Domain, Application, Infrastructure, Web)
- **Tipo de alteração:** Renomeação cross-layer + remoção de duplicações
- **Risco:** Médio (quebra de compilação, mas não de lógica)

## DECISÕES NECESSÁRIAS

1. **Renomear `Id_Fornecedor` → `ClienteId` (obsoleto)**
   - Justificativa: Id_Fornecedor está marcado como obsoleto
   - Impacto: 13 arquivos em Application layer

2. **Remover duplicação de `IdFornecedor` em Ativo.cs**
   - Justificativa: Propriedade duplicada (linhas 23 e 103)
   - Impacto: Commands que usam IdFornecedor

3. **Resolver conflito `Conglomerado` vs `Fornecedor`**
   - Justificativa: Refatoração parcial mal resolvida
   - Impacto: DbContext, queries, seeds
```

#### PASSO 1.3: Validar Escopo

**SE impacto > 3 arquivos OU > 1 camada:**
- ✅ Continuar com **Manutenção Completa**

**SE impacto <= 3 arquivos E 1 camada:**
- ⚠️ Considerar usar **Manutenção Controlada** (`manutencao-controlada.md`)

---

### FASE 2: PLANEJAMENTO DE CORREÇÃO

#### PASSO 2.1: Definir Ordem de Correção

**REGRA OBRIGATÓRIA:** Corrigir de **dentro para fora** (Domain → Application → Infrastructure → Web)

```
1. Domain Layer (base)
   └─> 2. Application Layer (depende de Domain)
       └─> 3. Infrastructure Layer (depende de Domain + Application)
           └─> 4. Web Layer (depende de todos)
```

#### PASSO 2.2: Criar Checklist de Correção

Adicionar em `.temp_ia/ANALISE-IMPACTO-[PROBLEMA].md`:

```markdown
## CHECKLIST DE CORREÇÃO

### FASE 1 - Domain Layer
- [ ] Fornecedor.cs: Remover duplicação de Id_Fornecedor (linha 17)
- [ ] Fornecedor.cs: Renomear Fornecedor→FornecedorPai (linha 30)
- [ ] Ativo.cs: Remover duplicação de IdFornecedor (linha 103)
- [ ] Conglomerado.cs: REMOVER arquivo (duplicado)

### FASE 2 - Application Layer
- [ ] CreateAtivoCommand.cs: Renomear IdFornecedor→IdFornecedorAquisicao
- [ ] UpdateAtivoCommand.cs: Ajustar referência a IdFornecedor
- [ ] GetFornecedoresQuery.cs: Substituir Id_Fornecedor→ClienteId
- [ ] (continuar para todos os 15 arquivos...)

### FASE 3 - Infrastructure Layer
- [ ] IApplicationDbContext.cs: Remover DbSet<Fornecedor> duplicado
- [ ] FornecedorConfiguration.cs: Validar mapeamentos

### FASE 4 - Web Layer
- [ ] FornecedoresEndpoints.cs: Validar endpoints
```

---

### FASE 3: EXECUÇÃO DA CORREÇÃO

#### PASSO 3.1: Executar Correções por Fase

**Para CADA fase:**

1. ✅ Aplicar correções nos arquivos da fase
2. ✅ Compilar projeto: `dotnet build`
3. ✅ Validar que **ZERO erros** foram introduzidos nesta fase
4. ✅ **SE novos erros:** Corrigir antes de prosseguir para próxima fase
5. ✅ Marcar checklist da fase como concluída

**REGRA CRÍTICA:** NÃO prosseguir para próxima fase se compilação falhar.

#### PASSO 3.2: Validação Contínua

**Após CADA alteração:**

```bash
# Compilar
dotnet build

# Interpretar resultado
# - Exit code 0 → SUCESSO (prosseguir)
# - Exit code != 0 → FALHA (corrigir antes de prosseguir)
```

---

### FASE 4: VALIDAÇÃO FINAL

#### PASSO 4.1: Executar Testes

```bash
# Testes unitários
dotnet test

# Testes de integração (se aplicável)
dotnet test --filter "Category=Integration"
```

**SE qualquer teste FALHAR:**
- ❌ **BLOQUEIO TOTAL**
- Corrigir teste quebrado ANTES de prosseguir

#### PASSO 4.2: Validação de Build Completo

```bash
# Backend
dotnet build --no-incremental

# Frontend (se afetado)
npm run build
```

**Critério de Aprovação:**
- ✅ Build backend: **SUCESSO**
- ✅ Build frontend: **SUCESSO** (se aplicável)
- ✅ Testes: **100% passando**

---

### FASE 5: COMMIT E DOCUMENTAÇÃO

#### PASSO 5.1: Criar Branch Dedicado

```bash
# Criar branch de manutenção
git checkout dev
git pull origin dev
git checkout -b manutencao/correcao-[PROBLEMA]-[DATA]

# Exemplo:
# git checkout -b manutencao/correcao-duplicacao-fornecedor-2026-01-06
```

#### PASSO 5.2: Commit Estruturado

```bash
git add .
git commit -m "$(cat <<'EOF'
fix(domain/application): corrige duplicação e renomeação Fornecedor cross-layer

PROBLEMA IDENTIFICADO:
- Duplicação de Id_Fornecedor em Domain layer
- 13 erros CS0618 (uso de propriedade obsoleta Id_Fornecedor)
- Refatoração parcial "Conglomerado → Fornecedor" mal resolvida

CORREÇÕES APLICADAS:

Domain Layer:
- Fornecedor.cs: Removida duplicação Id_Fornecedor (linha 17)
- Fornecedor.cs: Renomeada Fornecedor→FornecedorPai (linha 30)
- Ativo.cs: Removida duplicação IdFornecedor (linha 103)
- Conglomerado.cs: REMOVIDO (arquivo duplicado)

Application Layer (15 arquivos):
- Substituído Id_Fornecedor (obsoleto) → ClienteId
- Renomeado IdFornecedor → IdFornecedorAquisicao (contexto aquisição)
- Corrigidos mapeamentos e inicializadores

Infrastructure Layer:
- IApplicationDbContext.cs: Removida duplicação DbSet<Fornecedor>
- FornecedorConfiguration.cs: Validados mapeamentos

IMPACTO:
- Arquivos alterados: 20
- Camadas afetadas: 3 (Domain, Application, Infrastructure)
- Builds: SUCESSO
- Testes: SUCESSO (100%)

TIPO DE MANUTENÇÃO: Completa (cross-layer)
CONTRATO: contracts/desenvolvimento/manutencao/manutencao-completa.md

🤖 Generated with Claude Code
Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"
```

#### PASSO 5.3: Atualizar DECISIONS.md

**SE decisões técnicas foram tomadas:**

Adicionar em `D:\IC2\DECISIONS.md`:

```markdown
### [2026-01-06] Correção de Duplicação Fornecedor (Cross-Layer)

**Contexto:**
- Refatoração parcial "Conglomerado → Fornecedor" causou duplicações e propriedades obsoletas
- 15 erros de compilação em Application layer

**Decisões Tomadas:**

1. **Renomear `Id_Fornecedor` → `ClienteId`**
   - Razão: Id_Fornecedor marcado como obsoleto, causa 13 warnings CS0618
   - Alternativas: Manter Id_Fornecedor (não recomendado - deprecado)
   - Escolha: Migrar para ClienteId (padrão multi-tenancy)

2. **Renomear `IdFornecedor` → `IdFornecedorAquisicao` em Ativo.cs**
   - Razão: Esclarecer contexto (fornecedor de aquisição vs fornecedor de manutenção)
   - Alternativas: Manter IdFornecedor genérico
   - Escolha: Renomear para clareza

3. **Remover Conglomerado.cs**
   - Razão: Arquivo duplicado, refatoração incompleta
   - Alternativas: Manter e resolver conflitos
   - Escolha: Remover (mais limpo)

**Impacto:**
- Arquivos: 20
- Camadas: 3 (Domain, Application, Infrastructure)
- Risco: Baixo (breaking changes apenas internos)

**Tipo de Manutenção:** Completa (cross-layer)
**Contrato:** `manutencao-completa.md`
```

---

## 5. REGRAS DE DECISÕES TÉCNICAS

### 5.1. Quando Decisões São Permitidas

✅ **PERMITIDO decidir:**
- Renomear propriedades para clareza
- Remover duplicações
- Escolher entre múltiplas soluções equivalentes
- Refatorar código necessário para correção
- Atualizar nomenclatura para seguir convenções

❌ **PROIBIDO decidir:**
- Adicionar novas funcionalidades
- Alterar lógica de negócio além do necessário
- Mudar arquitetura do sistema
- Criar breaking changes em APIs públicas

### 5.2. Documentação de Decisões (OBRIGATÓRIA)

**TODA decisão técnica DEVE:**

1. ✅ Ser **justificada tecnicamente** (por que foi necessária)
2. ✅ Listar **alternativas consideradas** (o que NÃO foi feito e por quê)
3. ✅ Documentar **impacto** (arquivos, camadas, risco)
4. ✅ Ser registrada em **DECISIONS.md** (rastreabilidade)
5. ✅ Ser incluída no **commit message** (contexto)

---

## 6. PROIBIÇÕES

### 6.1. Proibições Absolutas

❌ **NUNCA:**
- Adicionar features novas
- Alterar contratos de API públicos sem aprovação
- Modificar lógica de negócio além do necessário
- Refatorar código não relacionado ao problema
- Criar breaking changes sem justificativa

### 6.2. Proibições de Git/Commits

❌ **NUNCA:**
- Fazer commits em `dev` diretamente (sempre criar branch)
- Fazer commits sem mensagem estruturada
- Fazer commits sem validar builds/testes

✅ **SEMPRE:**
- Criar branch dedicado: `manutencao/correcao-[PROBLEMA]-[DATA]`
- Commit message estruturado (problema, correções, impacto)
- Validar builds e testes ANTES de commit

---

## 7. CRITÉRIO DE PRONTO

O contrato só é considerado CONCLUÍDO quando:

### 7.1. Correção Aplicada

- [ ] Análise de impacto criada (`.temp_ia/ANALISE-IMPACTO-[PROBLEMA].md`)
- [ ] Checklist de correção definido
- [ ] Correções aplicadas por fase (Domain → Application → Infrastructure → Web)
- [ ] Compilação validada após CADA fase

### 7.2. Validação Técnica

- [ ] Build backend: **SUCESSO**
- [ ] Build frontend: **SUCESSO** (se aplicável)
- [ ] Testes unitários: **100% passando**
- [ ] Testes de integração: **100% passando** (se aplicável)

### 7.3. Documentação

- [ ] Branch criado: `manutencao/correcao-[PROBLEMA]-[DATA]`
- [ ] Commit estruturado com contexto completo
- [ ] **SE decisões tomadas:** DECISIONS.md atualizado
- [ ] Análise de impacto salva em `.temp_ia/`

### 7.4. Entrega

- [ ] Branch pronto para PR contra `dev`
- [ ] Nenhuma violação de contrato
- [ ] Nenhum breaking change não justificado
- [ ] Código compilando sem warnings relacionados

---

## 8. EXEMPLO PRÁTICO

### Cenário Real: Duplicação Fornecedor

**Problema:**
- Duplicação de `Id_Fornecedor` em `Fornecedor.cs`
- 13 erros CS0618 (uso de propriedade obsoleta)
- Refatoração parcial "Conglomerado → Fornecedor" mal resolvida

**Análise de Impacto:**
- Arquivos afetados: 20
- Camadas afetadas: 3 (Domain, Application, Infrastructure)
- Tipo: Cross-layer

**Decisão:**
- ✅ Usar **Manutenção Completa** (cross-layer, múltiplos arquivos)
- ❌ Não usar Manutenção Controlada (ultrapassaria escopo)

**Execução:**
1. Criar análise de impacto
2. Corrigir Domain layer primeiro
3. Corrigir Application layer (15 arquivos)
4. Corrigir Infrastructure layer
5. Validar builds e testes
6. Commit estruturado
7. Atualizar DECISIONS.md

**Resultado:**
- ✅ 20 arquivos corrigidos
- ✅ Builds: SUCESSO
- ✅ Testes: 100%
- ✅ Branch: `manutencao/correcao-duplicacao-fornecedor-2026-01-06`

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
