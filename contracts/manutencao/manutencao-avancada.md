# CONTRATO DE MANUTENÇÃO AVANÇADA

**Versão:** 1.0
**Data:** 2026-01-06
**Status:** Ativo

---

## 📋 SUMÁRIO EXECUTIVO

### ⚡ O que este contrato faz

Este contrato permite **MANUTENÇÕES ARQUITETURAIS** que exigem refatoração de infraestrutura, consolidação de migrations, mudanças sistêmicas.

**Diferença em relação aos outros contratos:**

| Aspecto | Manutenção Controlada | Manutenção Completa | Manutenção Avançada |
|---------|----------------------|---------------------|---------------------|
| **Escopo** | ❌ 1-3 arquivos | ✅ 10+ arquivos | ✅ Ilimitado |
| **Camadas** | ❌ 1 camada | ✅ Cross-layer | ✅ Cross-layer + Infraestrutura |
| **Refatoração** | ❌ Proibida | ✅ Permitida | ✅ **Arquitetural permitida** |
| **Migrations** | ❌ Edição proibida | ❌ Edição proibida | ✅ **Consolidação permitida** |
| **Infraestrutura** | ❌ Bloqueada | ❌ Bloqueada | ✅ **Mudanças permitidas** |
| **Autorização** | Automática | Automática | **⚠️ REQUER APROVAÇÃO EXPLÍCITA** |
| **Exemplos** | Corrigir typo | Renomeação cross-layer | Consolidar migrations, refatorar banco |

---

## 1. Identificação do Agente

| Campo | Valor |
|-------|-------|
| **Papel** | Agente de Manutenção Avançada (Arquitetural) |
| **Escopo** | Refatorações arquiteturais, consolidação de migrations, mudanças sistêmicas |
| **Modo** | **Autonomia técnica com aprovação obrigatória** |

---

## 2. Ativação do Contrato

Este contrato é ativado quando a solicitação mencionar explicitamente:

> **"Conforme contracts/desenvolvimento/manutencao/manutencao-avancada.md"**

**OU quando o usuário solicitar via prompt:**

> **"Execute D:\IC2_Governanca\prompts\desenvolvimento\manutencao\manutencao-avancada.md"**

### ⚠️ REGRA CRÍTICA: Aprovação Obrigatória

**ANTES de iniciar, o agente DEVE:**

1. ✅ **Validar autorização explícita** do usuário
2. ✅ **Apresentar resumo de mudanças arquiteturais**
3. ✅ **Aguardar confirmação do usuário**
4. ❌ **NUNCA iniciar sem aprovação** (bloqueio total)

### Quando Usar Este Contrato

✅ **USE quando:**
- **Manutenção Controlada BLOQUEOU** por escopo excedido
- **Manutenção Completa BLOQUEOU** por refatoração arquitetural necessária
- Problema exige **consolidação de migrations**
- Problema exige **refatoração de infraestrutura** (EF Core, banco, testes)
- Problema exige **mudanças arquiteturais** (value converters, model snapshot)
- **Usuário aprovou explicitamente** manutenção avançada

❌ **NÃO USE quando:**
- Problema pode ser resolvido com **Manutenção Controlada** (1-3 arquivos, 1 camada)
- Problema pode ser resolvido com **Manutenção Completa** (cross-layer sem refatoração)
- **Usuário não autorizou** mudanças arquiteturais

---

## 3. ESCOPO PERMITIDO

### 3.1. Alterações Permitidas (COM APROVAÇÃO)

✅ **PERMITIDO:**
- **Consolidar migrations** (combinar múltiplas migrations antigas)
- **Refatorar infraestrutura** (EF Core configuration, value converters)
- **Recriar banco de dados** (migrations from scratch)
- **Alterar ApplicationDbContextModelSnapshot** (corrigir tipos incompatíveis)
- **Alterar AuditDbContextModelSnapshot**
- **Refatorar estratégia de migrations** (SQLite → SQL Server)
- **Modificar 40+ migrations** antigas (se necessário)
- **Alterar arquitetura de testes** (TestContainers configuration)
- **Decisões arquiteturais justificadas** (com aprovação)

❌ **PROIBIDO:**
- Adicionar **novas funcionalidades** (features)
- Alterar **lógica de negócio** além do necessário
- Modificar **contratos de API** públicos (breaking changes)
- Refatorar código **não relacionado** ao problema
- **Iniciar sem aprovação** do usuário

---

## 4. WORKFLOW OBRIGATÓRIO

### FASE 0: APROVAÇÃO OBRIGATÓRIA (BLOQUEANTE)

#### PASSO 0.1: Apresentar Resumo de Mudanças Arquiteturais

**O agente DEVE gerar e exibir:**

```markdown
🚨 MANUTENÇÃO AVANÇADA - APROVAÇÃO NECESSÁRIA

PROBLEMA IDENTIFICADO:
[Descrição do problema que exige manutenção avançada]

POR QUE MANUTENÇÃO CONTROLADA/COMPLETA NÃO RESOLVE:
- [Razão 1: ex: requer consolidação de 40+ migrations]
- [Razão 2: ex: requer refatoração de model snapshot]
- [Razão 3: ex: requer mudança em estratégia de migrations]

MUDANÇAS ARQUITETURAIS PROPOSTAS:
1. [Mudança 1: ex: Consolidar migrations 2025-11-05 até 2026-01-06 (40 migrations)]
2. [Mudança 2: ex: Corrigir ApplicationDbContextModelSnapshot (tipos TEXT→SQL Server)]
3. [Mudança 3: ex: Corrigir AuditDbContextModelSnapshot]
4. [Mudança 4: ex: Aplicar value converters para compatibilidade SQL Server]

IMPACTO ESTIMADO:
- Arquivos afetados: [N]
- Migrations consolidadas: [N]
- Risco: [ALTO/MÉDIO/BAIXO]
- Reversível: [SIM/NÃO]
- Tempo estimado: [NÃO INFORMAR - conforme regra de planejamento]

CRITÉRIO DE SUCESSO:
- ✅ [Critério 1: ex: Testes funcionais passam (23/23)]
- ✅ [Critério 2: ex: Build passa sem warnings]
- ✅ [Critério 3: ex: Migrations aplicam sem erro]

VOCÊ AUTORIZA ESTAS MUDANÇAS ARQUITETURAIS?
[ ] SIM - Prosseguir com manutenção avançada
[ ] NÃO - Cancelar e manter bloqueio atual
[ ] MODIFICAR - Ajustar escopo proposto
```

#### PASSO 0.2: Aguardar Confirmação do Usuário

**SE usuário responder "SIM":**
- ✅ Prosseguir para FASE 1

**SE usuário responder "NÃO":**
- ❌ **BLOQUEIO TOTAL**
- Exibir mensagem: "Manutenção avançada CANCELADA pelo usuário. Problema permanece sem resolução."
- Registrar em DECISIONS.md: "Usuário recusou manutenção avançada [DATA]"

**SE usuário responder "MODIFICAR":**
- ✅ Ajustar escopo conforme solicitação
- ✅ Reapresentar resumo ajustado
- ✅ Aguardar nova confirmação

---

### FASE 1: ANÁLISE DE CAUSA RAIZ (OBRIGATÓRIA)

#### PASSO 1.1: Identificar Causa Raiz Arquitetural

**O agente DEVE investigar:**

```bash
# 1. Analisar histórico de migrations
ls -la backend/IControlIT.API/src/Infrastructure/Data/Migrations/

# 2. Verificar model snapshot
cat backend/IControlIT.API/src/Infrastructure/Data/ApplicationDbContextModelSnapshot.cs

# 3. Verificar audit snapshot (se aplicável)
cat backend/IControlIT.API/src/Infrastructure/Data/AuditDbContextModelSnapshot.cs

# 4. Verificar configurations
grep -r "HasColumnType" backend/IControlIT.API/src/Infrastructure/

# 5. Verificar value converters
grep -r "HasConversion" backend/IControlIT.API/src/Infrastructure/
```

#### PASSO 1.2: Documentar Causa Raiz

Criar arquivo: `.temp_ia/ANALISE-CAUSA-RAIZ-[PROBLEMA].md`

```markdown
# ANÁLISE DE CAUSA RAIZ - [PROBLEMA]

## SINTOMA OBSERVADO
[Descrição do erro/sintoma visível]

## CAUSA RAIZ IDENTIFICADA
[Descrição técnica da causa raiz arquitetural]

Exemplo:
```
CAUSA RAIZ: Migrations criadas com tipos SQLite incompatíveis com SQL Server

EVIDÊNCIAS:
- 40+ migrations usando TEXT (SQLite) em vez de NVARCHAR(MAX) (SQL Server)
- ApplicationDbContextModelSnapshot com tipos TEXT
- Nenhum value converter aplicado
- Migrations anteriores a 2025-11-05 não validadas

CONSEQUÊNCIA:
- Testes funcionais falham: "Operand type clash: text is incompatible with tinyint"
- TestContainers (SQL Server) rejeita migrations
- Incompatibilidade cross-database SQLite vs SQL Server
```

## TENTATIVAS ANTERIORES

[Listar tentativas de Manutenção Controlada/Completa que falharam]

Exemplo:
```
TENTATIVA 1: Manutenção Controlada
- Corrigidas 20 migrations recentes (últimos 7 dias)
- Build passou
- ❌ Testes ainda falharam (migrations antigas não corrigidas)

TENTATIVA 2: Manutenção Completa
- Corrigido CargoConfiguration.cs
- Corrigido ApplicationDbContextModelSnapshot parcialmente
- ❌ Testes ainda falharam (AuditDbContextModelSnapshot não corrigido)
```

## POR QUE MANUTENÇÃO AVANÇADA É NECESSÁRIA

[Justificativa técnica para refatoração arquitetural]

Exemplo:
```
RAZÃO 1: Escopo excede Manutenção Completa
- 40+ migrations precisam correção (não apenas 20)
- Migrations antigas (pré-2025-11-05) fora do escopo anterior

RAZÃO 2: Refatoração arquitetural necessária
- ApplicationDbContextModelSnapshot precisa regeneração
- AuditDbContextModelSnapshot precisa correção
- Value converters precisam ser aplicados

RAZÃO 3: Consolidação de migrations
- Migrations antigas com tipos incompatíveis
- Melhor estratégia: consolidar migrations antigas
```

## SOLUÇÃO PROPOSTA

[Estratégia técnica detalhada]
```

---

### FASE 2: PLANEJAMENTO DE REFATORAÇÃO

#### PASSO 2.1: Definir Estratégia

**Escolher uma estratégia:**

**ESTRATÉGIA A: Correção Incremental** (Preferencial)
- Corrigir migrations uma por uma (script automatizado)
- Corrigir model snapshots
- Aplicar value converters
- Validar após cada correção

**ESTRATÉGIA B: Consolidação de Migrations**
- Backup migrations antigas
- Criar migration consolidada
- Regenerar model snapshot
- Aplicar migrations do zero

**ESTRATÉGIA C: Recriação Completa**
- Deletar todas as migrations
- Recriar migrations from scratch
- Regenerar model snapshots
- Aplicar migrations limpo

#### PASSO 2.2: Criar Plano de Execução

Adicionar em `.temp_ia/ANALISE-CAUSA-RAIZ-[PROBLEMA].md`:

```markdown
## PLANO DE EXECUÇÃO

### ESTRATÉGIA ESCOLHIDA: [A/B/C]

### FASE 1 - Backup (OBRIGATÓRIO)
- [ ] Backup de todas as migrations (`.temp_ia/backup-migrations/`)
- [ ] Backup de ApplicationDbContextModelSnapshot.cs
- [ ] Backup de AuditDbContextModelSnapshot.cs
- [ ] Backup de configurations (`*Configuration.cs`)

### FASE 2 - Correção
- [ ] [Passo 1 específico]
- [ ] [Passo 2 específico]
- [ ] [Passo 3 específico]

### FASE 3 - Validação
- [ ] Build backend: `dotnet build`
- [ ] Aplicar migrations: `dotnet ef database update`
- [ ] Testes unitários: `dotnet test` (Domain + Application)
- [ ] Testes funcionais: `dotnet test` (Application.FunctionalTests)

### FASE 4 - Rollback (SE FALHAR)
- [ ] Restaurar migrations de backup
- [ ] Restaurar model snapshots
- [ ] Reportar falha ao usuário
```

---

### FASE 3: EXECUÇÃO DA REFATORAÇÃO

#### PASSO 3.1: Backup Obrigatório

```bash
# Criar pasta de backup
mkdir -p .temp_ia/backup-migrations-[DATA]/

# Backup migrations
cp -r backend/IControlIT.API/src/Infrastructure/Data/Migrations/ .temp_ia/backup-migrations-[DATA]/

# Backup snapshots
cp backend/IControlIT.API/src/Infrastructure/Data/ApplicationDbContextModelSnapshot.cs .temp_ia/backup-migrations-[DATA]/
cp backend/IControlIT.API/src/Infrastructure/Data/AuditDbContextModelSnapshot.cs .temp_ia/backup-migrations-[DATA]/

# Backup configurations (se aplicável)
cp backend/IControlIT.API/src/Infrastructure/Data/Configurations/*.cs .temp_ia/backup-migrations-[DATA]/configurations/
```

**REGRA CRÍTICA:** NÃO prosseguir sem backup completo.

#### PASSO 3.2: Executar Refatoração

**Para CADA passo do plano:**

1. ✅ Executar alteração
2. ✅ Validar build: `dotnet build`
3. ✅ **SE build falhar:** Reverter para backup, reportar erro
4. ✅ Marcar passo como concluído

#### PASSO 3.3: Validação Contínua

**Após CADA alteração significativa:**

```bash
# Compilar
dotnet build --no-incremental

# Validar migrations (DRY RUN)
dotnet ef migrations script > .temp_ia/migration-preview.sql

# Inspecionar SQL gerado
cat .temp_ia/migration-preview.sql | grep -i "TEXT\|INTEGER\|REAL"
```

**SE encontrar tipos incompatíveis:**
- ❌ Corrigir ANTES de prosseguir

---

### FASE 4: VALIDAÇÃO FINAL

#### PASSO 4.1: Executar Testes Completos

```bash
# 1. Build backend
cd backend/IControlIT.API
dotnet build --no-incremental

# 2. Aplicar migrations (banco de teste)
dotnet ef database update --connection "Server=localhost;Database=IControlIT_Test;..."

# 3. Testes unitários
dotnet test tests/Domain.UnitTests/
dotnet test tests/Application.UnitTests/

# 4. Testes funcionais (TestContainers - SQL Server)
dotnet test tests/Application.FunctionalTests/
```

**Critério de Aprovação:**
- ✅ Build: **SUCESSO** (0 erros, 0 warnings)
- ✅ Migrations: **APLICADAS** sem erro
- ✅ Testes unitários: **100% passando**
- ✅ Testes funcionais: **100% passando** (23/23)

**SE qualquer critério FALHAR:**
- ❌ **Rollback obrigatório** (restaurar de backup)
- Reportar falha ao usuário
- Registrar em DECISIONS.md

#### PASSO 4.2: Validação de Compatibilidade

```bash
# Validar tipos SQL Server no snapshot
cat backend/IControlIT.API/src/Infrastructure/Data/ApplicationDbContextModelSnapshot.cs | grep -E "TEXT|INTEGER|REAL"

# Esperado: ZERO ocorrências de TEXT/INTEGER/REAL
```

**SE encontrar tipos incompatíveis:**
- ❌ **Rollback obrigatório**

---

### FASE 5: COMMIT E DOCUMENTAÇÃO

#### PASSO 5.1: Commit Estruturado

```bash
git add .
git commit -m "$(cat <<'EOF'
refactor(infra): [TÍTULO CURTO DA REFATORAÇÃO]

PROBLEMA IDENTIFICADO:
- [Descrição do problema que exigiu manutenção avançada]

TENTATIVAS ANTERIORES (FALHARAM):
- Manutenção Controlada: [motivo do bloqueio]
- Manutenção Completa: [motivo do bloqueio]

REFATORAÇÃO APLICADA (MANUTENÇÃO AVANÇADA):

Estratégia: [A/B/C]
Escopo: [N] migrations, [N] snapshots, [N] configurations

Alterações:
- [Lista detalhada de mudanças arquiteturais]

Backup:
- .temp_ia/backup-migrations-[DATA]/ (40+ migrations + snapshots)

IMPACTO:
- Arquivos alterados: [N]
- Migrations consolidadas: [N]
- Testes: SUCESSO (23/23 funcionais, 31/31 unitários)
- Builds: SUCESSO (0 erros, 0 warnings)

TIPO DE MANUTENÇÃO: Avançada (arquitetural)
CONTRATO: contracts/desenvolvimento/manutencao/manutencao-avancada.md
AUTORIZAÇÃO: Usuário aprovou em [DATA]

🤖 Generated with Claude Code
Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"
```

#### PASSO 5.2: Atualizar DECISIONS.md (OBRIGATÓRIO)

Adicionar em `D:\IC2\DECISIONS.md`:

```markdown
### [2026-01-06] Manutenção Avançada: Consolidação de Migrations SQL Server

**Contexto:**
- Testes funcionais falhavam: "Operand type clash: text is incompatible with tinyint"
- Manutenção Controlada BLOQUEOU (escopo excedido)
- Manutenção Completa BLOQUEOU (refatoração arquitetural necessária)

**Problema Raiz:**
- 40+ migrations criadas com tipos SQLite (TEXT, INTEGER)
- ApplicationDbContextModelSnapshot com tipos incompatíveis
- AuditDbContextModelSnapshot desatualizado
- Nenhum value converter aplicado

**Decisões Tomadas:**

1. **Estratégia de Refatoração: Correção Incremental (A)**
   - Razão: Preserva histórico de migrations
   - Alternativas: Consolidação (B), Recriação (C)
   - Escolha: Correção incremental + script PowerShell

2. **Tipos Corrigidos:**
   - Guid: TEXT → uniqueidentifier
   - DateTime: TEXT → datetime2
   - DateTimeOffset: TEXT → datetimeoffset
   - decimal: TEXT → decimal(18,2)
   - string sem maxLength: TEXT → NVARCHAR(MAX)

3. **Escopo da Correção:**
   - 40 migrations (2025-11-05 até 2026-01-06)
   - ApplicationDbContextModelSnapshot regenerado
   - AuditDbContextModelSnapshot corrigido
   - 15 configurations atualizadas

**Impacto:**
- Arquivos: 56 (40 migrations + 2 snapshots + 14 configurations)
- Testes: 54/54 passando (23 funcionais + 31 unitários)
- Risco: Médio (backup completo realizado)
- Reversível: Sim (.temp_ia/backup-migrations-2026-01-06/)

**Tipo de Manutenção:** Avançada (arquitetural)
**Autorização:** Usuário aprovou em 2026-01-06
**Contrato:** `manutencao-avancada.md`
```

---

## 5. PROIBIÇÕES

### 5.1. Proibições Absolutas

❌ **NUNCA:**
- Iniciar sem **aprovação explícita** do usuário
- Executar sem **backup completo** (migrations + snapshots)
- Adicionar **features novas** (fora do escopo)
- Criar **breaking changes** em APIs públicas
- Refatorar código **não relacionado** ao problema
- **Omitir validação** após cada alteração

### 5.2. Proibições de Rollback

❌ **NUNCA:**
- Prosseguir se **validação falhar**
- Ignorar **testes falhando**
- Commitar código que **não resolve o problema**
- Deletar **backup** antes de validação completa

---

## 6. CRITÉRIO DE PRONTO

O contrato só é considerado CONCLUÍDO quando:

### 6.1. Aprovação e Backup

- [ ] **Aprovação explícita** do usuário obtida (FASE 0)
- [ ] **Backup completo** realizado (migrations + snapshots + configurations)
- [ ] Backup salvo em `.temp_ia/backup-migrations-[DATA]/`

### 6.2. Análise e Planejamento

- [ ] Causa raiz identificada (`.temp_ia/ANALISE-CAUSA-RAIZ-[PROBLEMA].md`)
- [ ] Estratégia definida (A/B/C)
- [ ] Plano de execução criado

### 6.3. Execução

- [ ] Refatoração aplicada conforme plano
- [ ] Validação contínua após cada alteração
- [ ] ZERO tipos incompatíveis remanescentes

### 6.4. Validação Técnica

- [ ] Build backend: **SUCESSO** (0 erros, 0 warnings)
- [ ] Migrations aplicam sem erro
- [ ] Testes unitários: **100% passando**
- [ ] Testes funcionais: **100% passando**
- [ ] Model snapshots sem tipos incompatíveis

### 6.5. Documentação

- [ ] Commit estruturado com contexto completo
- [ ] DECISIONS.md atualizado (decisões arquiteturais)
- [ ] Análise de causa raiz salva em `.temp_ia/`
- [ ] Backup preservado para rollback

### 6.6. Entrega

- [ ] Problema original **RESOLVIDO**
- [ ] Nenhuma violação de contrato
- [ ] Nenhum breaking change não justificado
- [ ] Código compilando sem warnings

---

## 7. REGRA DE NEGAÇÃO ZERO

Se uma solicitação:
- não estiver explicitamente prevista no contrato ativo, ou
- conflitar com qualquer regra do contrato

ENTÃO:

- A execução DEVE ser NEGADA
- Nenhuma ação parcial pode ser realizada
- Nenhum "adiantamento" é permitido

---

**FIM DO CONTRATO**
