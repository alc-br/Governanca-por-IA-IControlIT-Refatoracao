# CONTRATO DE EXECUÇÃO — ADITIVO (Evolução Incremental de RF)

**Versão:** 1.0
**Data:** 2026-01-03
**Status:** Ativo

---

## 📋 SUMÁRIO EXECUTIVO

### ⚡ O que este contrato faz

Este contrato **adiciona novas funcionalidades a um RF existente** de forma incremental e rastreável, garantindo:

- ✅ **Backup Automático**: Versões `_old` de todos os documentos (RF, UC, WF, MD, MT, TC)
- ✅ **Evolução Incremental**: Adiciona funcionalidades ao RF → UC → WF → MD → MT → TC
- ✅ **Rastreabilidade Total**: Delta entre versão original e `_old` documentado
- ✅ **Cobertura 100%**: Nova funcionalidade coberta em TODOS os níveis
- ✅ **Validação Rigorosa**: Zero tolerância a gaps (aprovação SEM ressalvas)

### 📁 Arquivos Gerados/Modificados

**Backups (sobrescritos a cada aditivo):**
1. `RFXXX_old.md` - Versão anterior do RF
2. `RFXXX_old.yaml` - Versão anterior do RF (YAML)
3. `UC-RFXXX_old.md` - Versão anterior dos UCs
4. `UC-RFXXX_old.yaml` - Versão anterior dos UCs (YAML)
5. `WF-RFXXX_old.md` - Versão anterior dos WFs
6. `WF-RFXXX_old.yaml` - Versão anterior dos WFs (YAML)
7. `MD-RFXXX_old.md` - Versão anterior do Modelo de Dados
8. `MD-RFXXX_old.yaml` - Versão anterior do MD (YAML)
9. `MT-RFXXX_old.yaml` - Versão anterior das Massas de Teste
10. `TC-RFXXX_old.yaml` - Versão anterior dos Casos de Teste

**Documentos atualizados (versões originais):**
1. `RFXXX.md` - RF com nova funcionalidade
2. `RFXXX.yaml` - RF YAML com nova funcionalidade
3. `UC-RFXXX.md` - UCs cobrindo nova funcionalidade
4. `UC-RFXXX.yaml` - UCs YAML cobrindo nova funcionalidade
5. `WF-RFXXX.md` - WFs cobrindo nova funcionalidade
6. `WF-RFXXX.yaml` - WFs YAML cobrindo nova funcionalidade
7. `MD-RFXXX.md` - MD cobrindo nova funcionalidade
8. `MD-RFXXX.yaml` - MD YAML cobrindo nova funcionalidade
9. `MT-RFXXX.yaml` - Massas de teste cobrindo nova funcionalidade
10. `TC-RFXXX.yaml` - Casos de teste cobrindo nova funcionalidade

**Relatórios de delta:**
11. `.temp_ia/aditivo-RFXXX-delta-report.md` - Relatório de mudanças aplicadas

### 🎯 Princípios Fundamentais

1. **Backup Antes de Modificar**: SEMPRE criar `_old` antes de tocar nos originais
2. **Evolução em Cascata**: RF → UC → WF → MD → MT → TC (nessa ordem)
3. **Cobertura Total**: Nova funcionalidade DEVE aparecer em TODOS os níveis
4. **Delta Rastreável**: Relatório mostrando exatamente o que foi adicionado
5. **Validação Rigorosa**: Aprovação SOMENTE SEM ressalvas (100%)

### ⚠️ REGRA CRÍTICA — VERSÕES _OLD SÃO SOBRESCRITAS

**As versões `_old` NÃO são históricas, são SNAPSHOTS do estado anterior.**

- A cada novo aditivo, os arquivos `_old` são **sobrescritos** com o conteúdo **atual**
- Os originais são então modificados com o novo aditivo
- Isso permite comparação antes/depois a cada iteração
- **Histórico real está no Git** (commits), não nos arquivos `_old`

---

## 1. Identificação do Agente

| Campo | Valor |
|-------|-------|
| **Papel** | Agente de Evolução Incremental de Documentação |
| **Escopo** | Adicionar novas funcionalidades a RF existente (RF → UC → WF → MD → MT → TC) |
| **Modo** | Documentação (sem alteração de código) |

---

## 2. Ativação do Contrato

Este contrato é ativado quando a solicitação mencionar explicitamente:

> **"Conforme docs/contracts/documentacao/execucao/aditivo.md para RFXXX"**

Exemplo:
```
Conforme docs/contracts/documentacao/execucao/aditivo.md para RF028.
Adicionar funcionalidade de "Exportação em PDF".
Seguir CLAUDE.md.
```

---

## 3. Objetivo do Contrato

Adicionar **novas funcionalidades** a um RF existente, propagando a mudança em cascata através de todos os documentos:

1. **RF** - Adicionar funcionalidade, regras de negócio, endpoints, permissões
2. **UC** - Criar casos de uso cobrindo 100% da nova funcionalidade
3. **WF** - Adicionar wireframes para nova interface
4. **MD** - Estender modelo de dados (se necessário)
5. **MT** - Criar massas de teste para nova funcionalidade
6. **TC** - Criar casos de teste cobrindo nova funcionalidade

---

## 4. Pré-Requisitos Bloqueantes

Antes de iniciar, **OS PRÉ-REQUISITOS MÍNIMOS** devem ser satisfeitos:

| # | Pré-Requisito | Obrigatório | Verificação |
|---|---------------|-------------|-------------|
| 1 | RF existe (`RFXXX.md`, `RFXXX.yaml`) | ✅ **SIM** | ✅ Arquivo existe |
| 2 | UC existe (`UC-RFXXX.md`, `UC-RFXXX.yaml`) | ✅ **SIM** | ✅ Arquivo existe |
| 3 | WF existe (`WF-RFXXX.md`, `WF-RFXXX.yaml`) | ⚠️ Opcional | ✅ Arquivo existe ou N/A |
| 4 | MD existe (`MD-RFXXX.md`, `MD-RFXXX.yaml`) | ⚠️ Opcional | ✅ Arquivo existe ou N/A |
| 5 | MT existe (`MT-RFXXX.yaml`) | ⚠️ Opcional | ✅ Arquivo existe ou N/A |
| 6 | TC existe (`TC-RFXXX.yaml`) | ⚠️ Opcional | ✅ Arquivo existe ou N/A |
| 7 | STATUS.yaml existe | ✅ **SIM** | ✅ Arquivo existe |
| 8 | Branch correto (`feature/RFXXX-aditivo-*`) | ✅ **SIM** | ✅ Branch ativo |
| 9 | Descrição clara da nova funcionalidade | ✅ **SIM** | ✅ Fornecida pelo usuário |

**Pré-Requisitos OBRIGATÓRIOS (Bloqueantes):**
- ✅ RF.md e RF.yaml **DEVEM** existir
- ✅ UC.md e UC.yaml **DEVEM** existir
- ✅ STATUS.yaml **DEVE** existir
- ✅ Branch correto ativo
- ✅ Descrição da nova funcionalidade fornecida

**Pré-Requisitos OPCIONAIS (Não Bloqueantes):**
- ⚠️ WF, MD, MT, TC **PODEM** não existir
- ⚠️ Se não existirem, aditivo **PULA** esses passos
- ⚠️ Backup `_old` **SÓ É CRIADO** para documentos que existem

**Se pré-requisito OBRIGATÓRIO falhar:**
➡️ **BLOQUEIO TOTAL**. Não prosseguir até resolução.

**Se pré-requisito OPCIONAL não existir:**
➡️ **PULAR** passos relacionados. ADITIVO continua normalmente.

---

## ⚠️ ADENDO CRÍTICO — PRINCÍPIO FUNDAMENTAL DO ADITIVO

### ADITIVO ATUALIZA, NÃO CRIA

**Regra Absoluta:**
- ✅ **SE** documento **EXISTE** → ADITIVO **ATUALIZA** (cria backup _old, depois modifica)
- ❌ **SE** documento **NÃO EXISTE** → ADITIVO **PULA** (não cria, não toca)

**Aplicação por Documento:**

| Documento | Existe? | Ação ADITIVO |
|-----------|---------|--------------|
| **RF.md, RF.yaml** | ✅ SEMPRE (obrigatório) | ✅ Criar backup → Atualizar |
| **UC.md, UC.yaml** | ✅ SEMPRE (obrigatório) | ✅ Criar backup → Atualizar |
| **WF.md, WF.yaml** | ⚠️ PODE NÃO EXISTIR | SE existe → backup + update; SE NÃO → PULAR |
| **MD.md, MD.yaml** | ⚠️ PODE NÃO EXISTIR | SE existe → backup + update; SE NÃO → PULAR |
| **MT.yaml** | ⚠️ PODE NÃO EXISTIR | SE existe → backup + update; SE NÃO → PULAR |
| **TC.yaml** | ⚠️ PODE NÃO EXISTIR | SE existe → backup + update; SE NÃO → PULAR |

**Consequências:**
1. **JAMAIS criar** MD.yaml se MD não existia antes
2. **JAMAIS criar** WF.yaml se WF não existia antes
3. **JAMAIS criar** MT/TC.yaml se não existiam antes
4. **SEMPRE pular passos** de documentos ausentes

**Validação:**
- Validador marca como **N/A** quando baseline (_old) não existe
- **N/A não reprova** o aditivo
- Apenas validações **aplicáveis** (documentos que existem) contam para 100%

**Razão:**
- ADITIVO serve para **evoluir RF existente**
- Criar documentos novos é responsabilidade de **contratos de criação** (RF, WF, MD, MT, TC)
- Misturar criação com evolução gera **inconsistências** e **violações de contrato**

---

## 5. Workflow de Execução (12 Passos Obrigatórios)

### PASSO 0: PLANEJAR E DOCUMENTAR EXECUÇÃO (OBRIGATÓRIO - CRÍTICO)

**ANTES DE CRIAR QUALQUER BACKUP OU MODIFICAR QUALQUER ARQUIVO**, o agente **DEVE**:

#### 0.1. Ler e Interpretar Solicitação do Usuário

**Objetivo:** Entender EXATAMENTE o que deve ser adicionado ao RF.

```markdown
**Solicitação do usuário:**
> [Transcrição literal da solicitação completa]

**Interpretação:**
- Funcionalidade a adicionar: [descrição clara]
- Escopo: [o que está incluído]
- Limitações: [o que NÃO está incluído]
```

#### 0.2. Criar Plano de Execução Detalhado

**Objetivo:** Documentar TODAS as entregas esperadas em CADA documento.

O agente DEVE criar o arquivo `.temp_ia/aditivo-RFXXX-PLANO.md` com o seguinte conteúdo:

```markdown
# PLANO DE EXECUÇÃO — ADITIVO RFXXX

**Data:** YYYY-MM-DD
**Solicitação do usuário:**
> [Transcrição literal]

---

## 1. META GERAL

**Funcionalidade a adicionar:**
[Descrição em 1-2 parágrafos]

**Objetivo:**
[O que o usuário quer alcançar]

---

## 2. ENTREGAS PLANEJADAS POR DOCUMENTO

### 2.1. RF (RFXXX.md, RFXXX.yaml) — OBRIGATÓRIO

**RNs a adicionar:**
1. **RN-XXX-YYY-001**: [Título] — [Descrição breve]
2. **RN-XXX-YYY-002**: [Título] — [Descrição breve]
...
N. **RN-XXX-YYY-NNN**: [Título] — [Descrição breve]

**Total:** N RNs planejadas

**Funcionalidades (catalog.rf_items) a adicionar:**
1. **RF-XXX-01**: [Nome] — Mapeia RN-XXX-YYY-001, RN-XXX-YYY-002
2. **RF-XXX-02**: [Nome] — Mapeia RN-XXX-YYY-003
...

**Endpoints a adicionar (se aplicável):**
1. **POST /api/xxx**: [Descrição]
2. **GET /api/xxx/{id}**: [Descrição]

**Permissões a adicionar (se aplicável):**
1. **XXX.Create**: Criar XXX
2. **XXX.Read**: Visualizar XXX

---

### 2.2. UC (UC-RFXXX.md, UC-RFXXX.yaml) — OBRIGATÓRIO

**UCs a criar:**
1. **UC-NN**: [Título] — Cobre RN-XXX-YYY-001, RN-XXX-YYY-002, RN-XXX-YYY-003
2. **UC-MM**: [Título] — Cobre RN-XXX-YYY-004, RN-XXX-YYY-005
...

**Total:** M UCs planejados

**Matriz de Cobertura UC → RN:**
| UC | RNs Cobertas |
|----|--------------|
| UC-NN | RN-XXX-YYY-001, RN-XXX-YYY-002, RN-XXX-YYY-003 |
| UC-MM | RN-XXX-YYY-004, RN-XXX-YYY-005 |

**Garantia:** TODAS as N RNs planejadas DEVEM ser cobertas por pelo menos 1 UC.

---

### 2.3. WF (WF-RFXXX.md, WF-RFXXX.yaml) — SE EXISTIR

**Condição:** ⚠️ PULAR se WF-RFXXX_old.md NÃO for criado no Passo 3

**WFs a criar (SE WF EXISTIR):**
1. **WF-NN**: [Título] — Telas para UC-NN
2. **WF-MM**: [Título] — Telas para UC-MM
...

**Total:** P WFs planejados (SE WF EXISTIR)

**Matriz de Cobertura WF → UC:**
| WF | UCs Cobertos |
|----|--------------|
| WF-NN | UC-NN |
| WF-MM | UC-MM |

---

### 2.4. MD (MD-RFXXX.md, MD-RFXXX.yaml) — SE EXISTIR

**Condição:** ⚠️ PULAR se MD-RFXXX_old.md NÃO for criado no Passo 4

**Mudanças MD planejadas (SE MD EXISTIR):**

**DTOs a criar:**
1. **CreateXxxDto**: [Campos]
2. **UpdateXxxDto**: [Campos]
3. **XxxResponseDto**: [Campos]

**Entidades a criar/modificar:**
1. **Xxx**: [Descrição] — Campos: [lista]

**Índices a criar:**
1. **IX_Xxx_Campo**: [Justificativa]

**Total (SE MD EXISTIR):**
- N DTOs
- M Entidades
- P Índices

---

### 2.5. MT (MT-RFXXX.yaml) — SE EXISTIR

**Condição:** ⚠️ PULAR se MT-RFXXX_old.yaml NÃO for criado no Passo 5

**Massas de teste planejadas (SE MT EXISTIR):**

| UC | Registros Planejados |
|----|----------------------|
| UC-NN | ≥5 registros |
| UC-MM | ≥5 registros |

**Total (SE MT EXISTIR):** ≥M registros

---

### 2.6. TC (TC-RFXXX.yaml) — SE EXISTIR

**Condição:** ⚠️ PULAR se TC-RFXXX_old.yaml NÃO for criado no Passo 6

**Casos de teste planejados (SE TC EXISTIR):**

| UC | TCs Planejados |
|----|----------------|
| UC-NN | ≥30 TCs |
| UC-MM | ≥30 TCs |

**Total (SE TC EXISTIR):** ≥N TCs

---

## 3. CHECKLIST DE VALIDAÇÃO (VAL-0)

Ao final da execução, o validador VAL-0 verificará:

### RF:
- [ ] N RNs criadas (conforme planejado)
- [ ] Todas as RNs planejadas existem em RFXXX.md
- [ ] Todas as RNs planejadas existem em RFXXX.yaml

### UC:
- [ ] M UCs criados (conforme planejado)
- [ ] Todos os UCs planejados existem em UC-RFXXX.md
- [ ] Todos os UCs planejados existem em UC-RFXXX.yaml
- [ ] **100% das N RNs planejadas cobertas por UCs**

### WF (SE EXISTIR):
- [ ] P WFs criados (conforme planejado)
- [ ] Todos os WFs planejados existem em WF-RFXXX.md
- [ ] Todos os WFs planejados existem em WF-RFXXX.yaml

### MD (SE EXISTIR):
- [ ] DTOs criados (conforme planejado)
- [ ] Entidades criadas/modificadas (conforme planejado)
- [ ] Índices criados (conforme planejado)

### MT (SE EXISTIR):
- [ ] Massas de teste criadas para todos os UCs planejados

### TC (SE EXISTIR):
- [ ] ≥30 TCs criados para cada UC planejado

---

## 4. CRITÉRIO DE APROVAÇÃO VAL-0

**✅ PASS:** 100% do plano cumprido (todas as entregas criadas)
**❌ FAIL:** Plano parcialmente cumprido (faltam entregas)

---

**Mantido por:** Agente de Execução ADITIVO
**Governado por:** CLAUDE.md
```

#### 0.3. Checkpoint PASSO 0

**Antes de prosseguir para FASE 1, verificar:**
- ✅ Arquivo `.temp_ia/aditivo-RFXXX-PLANO.md` criado
- ✅ Seção "ENTREGAS PLANEJADAS POR DOCUMENTO" completa
- ✅ Matriz de cobertura UC → RN documentada
- ✅ Checklist de validação (VAL-0) documentado

**Se PASSO 0 não for concluído:**
➡️ **BLOQUEIO TOTAL**. Não prosseguir para FASE 1.

---

### FASE 1: BACKUP (Passos 1-6)

**REGRA CRÍTICA:** Backup `_old` **SÓ É CRIADO** para documentos que **JÁ EXISTEM**.

#### Passo 1: Criar Backup do RF (OBRIGATÓRIO)

```bash
# RF é OBRIGATÓRIO - DEVE existir
cp RFXXX.md RFXXX_old.md
cp RFXXX.yaml RFXXX_old.yaml
```

**Checkpoint:**
- ✅ Arquivos `RFXXX_old.md` e `RFXXX_old.yaml` criados
- ✅ Conteúdo IDÊNTICO aos originais

#### Passo 2: Criar Backup do UC (OBRIGATÓRIO)

```bash
# UC é OBRIGATÓRIO - DEVE existir
cp UC-RFXXX.md UC-RFXXX_old.md
cp UC-RFXXX.yaml UC-RFXXX_old.yaml
```

**Checkpoint:**
- ✅ Arquivos `UC-RFXXX_old.md` e `UC-RFXXX_old.yaml` criados

#### Passo 3: Criar Backup do WF (SE EXISTIR)

```bash
# Verificar se WF existe antes de criar backup
if [ -f "WF-RFXXX.md" ]; then
  cp WF-RFXXX.md WF-RFXXX_old.md
  cp WF-RFXXX.yaml WF-RFXXX_old.yaml
fi
```

**Checkpoint:**
- ✅ SE WF existir: Arquivos `WF-RFXXX_old.md` e `WF-RFXXX_old.yaml` criados
- ⚠️ SE WF NÃO existir: Pular este passo (N/A)

#### Passo 4: Criar Backup do MD (SE EXISTIR)

```bash
# Verificar se MD existe antes de criar backup
if [ -f "MD-RFXXX.md" ]; then
  cp MD-RFXXX.md MD-RFXXX_old.md
  cp MD-RFXXX.yaml MD-RFXXX_old.yaml
fi
```

**Checkpoint:**
- ✅ SE MD existir: Arquivos `MD-RFXXX_old.md` e `MD-RFXXX_old.yaml` criados
- ⚠️ SE MD NÃO existir: Pular este passo (N/A)

#### Passo 5: Criar Backup do MT (SE EXISTIR)

```bash
# Verificar se MT existe antes de criar backup
if [ -f "MT-RFXXX.yaml" ]; then
  cp MT-RFXXX.yaml MT-RFXXX_old.yaml
fi
```

**Checkpoint:**
- ✅ SE MT existir: Arquivo `MT-RFXXX_old.yaml` criado
- ⚠️ SE MT NÃO existir: Pular este passo (N/A)

#### Passo 6: Criar Backup do TC (SE EXISTIR)

```bash
# Verificar se TC existe antes de criar backup
if [ -f "TC-RFXXX.yaml" ]; then
  cp TC-RFXXX.yaml TC-RFXXX_old.yaml
fi
```

**Checkpoint:**
- ✅ SE TC existir: Arquivo `TC-RFXXX_old.yaml` criado
- ⚠️ SE TC NÃO existir: Pular este passo (N/A)
- ✅ **FASE 1 COMPLETA** - Backups criados para documentos existentes

---

### FASE 2: EVOLUÇÃO INCREMENTAL (Passos 7-10)

#### Passo 7: Adicionar Funcionalidade ao RF

**Ações:**

1. **Ler `RFXXX.md` e `RFXXX.yaml`** (versões originais)
2. **Identificar seções relevantes** para adicionar a nova funcionalidade:
   - Seção 4: Funcionalidades → Adicionar nova funcionalidade ao catálogo
   - Seção 5: Regras de Negócio → Adicionar RNs específicas da nova funcionalidade
   - Seção 7: Permissões (RBAC) → Adicionar permissões necessárias
   - Seção 8: Endpoints da API → Adicionar novos endpoints (se aplicável)
   - Seção 9: Modelo de Dados → Documentar mudanças (se aplicável)
   - Seção 11: Integrações Obrigatórias → Atualizar chaves i18n, auditoria, etc.

3. **Adicionar conteúdo ao RF**:
   - Seguir template RF.md v2.0
   - Manter coerência com conteúdo existente
   - Adicionar mínimo 3 RNs para nova funcionalidade (RN-MOD-XXX-NN)

4. **Atualizar `RFXXX.yaml`**:
   - Sincronizar com `RFXXX.md`
   - Adicionar RNs, permissões, catálogo

**Checkpoint:**
- ✅ RF atualizado com nova funcionalidade
- ✅ Mínimo 3 RNs adicionadas
- ✅ Permissões adicionadas (se aplicável)
- ✅ Endpoints documentados (se aplicável)
- ✅ RFXXX.md ↔ RFXXX.yaml sincronizados

#### Passo 8: Adicionar Cobertura ao UC

**Ações:**

1. **Comparar `RFXXX.md` vs `RFXXX_old.md`**:
   - Identificar EXATAMENTE o que foi adicionado
   - Listar novas RNs, funcionalidades, endpoints

2. **Ler `UC-RFXXX.md` e `UC-RFXXX.yaml`** (versões originais)

3. **Criar novos UCs** para cobrir 100% da nova funcionalidade:
   - Seguir template UC.md v2.0
   - Garantir que TODAS as RNs novas estejam cobertas
   - Adicionar UCs em `UC-RFXXX.md` e `UC-RFXXX.yaml`

4. **Validar cobertura**:
   - Executar: `python docs/tools/docs/validator-rf-uc.py RFXXX`
   - Exit code DEVE ser 0 (100% de cobertura)

**Checkpoint:**
- ✅ Novos UCs criados cobrindo 100% do delta RF
- ✅ UC-RFXXX.md ↔ UC-RFXXX.yaml sincronizados
- ✅ Validador passou (exit code 0)

#### Passo 9: Adicionar Cobertura ao WF (SE WF EXISTIR)

**Condição:** PULAR se `WF-RFXXX_old.md` NÃO foi criado (documento não existia antes)

**Ações:**

1. **Comparar `UC-RFXXX.yaml` vs `UC-RFXXX_old.yaml`**:
   - Identificar novos UCs criados

2. **SE WF existe**, ler `WF-RFXXX.md` e `WF-RFXXX.yaml`** (versões originais)

3. **SE WF existe**, criar novos WFs para cobrir 100% dos novos UCs:
   - Seguir template WF.md
   - Documentar telas, componentes, eventos, estados
   - Garantir 4 estados obrigatórios (Loading, Vazio, Erro, Dados)
   - Documentar responsividade (Mobile, Tablet, Desktop)
   - Documentar acessibilidade WCAG AA

**Checkpoint:**
- ✅ SE WF existe: Novos WFs criados cobrindo 100% dos novos UCs
- ✅ SE WF existe: WF-RFXXX.md ↔ WF-RFXXX.yaml sincronizados
- ⚠️ SE WF NÃO existe: PULAR este passo (N/A)

#### Passo 10: Adicionar Cobertura ao MD (SE MD EXISTIR)

**Condição:** PULAR se `MD-RFXXX_old.md` NÃO foi criado (documento não existia antes)

**Ações:**

1. **Comparar `RFXXX.md` vs `RFXXX_old.md`**:
   - Identificar mudanças no modelo de dados (Seção 9)

2. **SE MD existe**, ler `MD-RFXXX.md` e `MD-RFXXX.yaml`** (versões originais)

3. **SE MD existe E RF documenta mudanças**, atualizar modelo de dados:
   - Adicionar novas tabelas (se necessário)
   - Adicionar novos campos a tabelas existentes
   - Garantir multi-tenancy (`cliente_id` ou `empresa_id`)
   - Garantir auditoria (5 campos obrigatórios)
   - Garantir soft delete (`deleted_at`)
   - Documentar novos relacionamentos

**Checkpoint:**
- ✅ SE MD existe E há mudanças: MD atualizado com suporte à nova funcionalidade
- ✅ SE MD existe E há mudanças: MD-RFXXX.md ↔ MD-RFXXX.yaml sincronizados
- ⚠️ SE MD NÃO existe: PULAR este passo (N/A)
- ⚠️ SE MD existe MAS RF não documenta mudanças: PULAR atualização (N/A)

---

### FASE 3: TESTES (Passos 11-12)

#### Passo 11: Adicionar Cobertura ao MT (SE MT EXISTIR)

**Condição:** PULAR se `MT-RFXXX_old.yaml` NÃO foi criado (documento não existia antes)

**Ações:**

1. **Comparar `UC-RFXXX.yaml` vs `UC-RFXXX_old.yaml`**:
   - Identificar novos UCs criados

2. **SE MT existe**, ler `MT-RFXXX.yaml` (versão original)

3. **SE MT existe**, criar novas massas de teste:
   - Adicionar dados de teste para cada novo UC
   - Garantir cenários: caminho feliz, triste, edge cases
   - Formato CSV conforme template

**Checkpoint:**
- ✅ SE MT existe: Massas de teste criadas para novos UCs
- ⚠️ SE MT NÃO existe: PULAR este passo (N/A)

#### Passo 12: Adicionar Cobertura ao TC (SE TC EXISTIR)

**Condição:** PULAR se `TC-RFXXX_old.yaml` NÃO foi criado (documento não existia antes)

**Ações:**

1. **Comparar `UC-RFXXX.yaml` vs `UC-RFXXX_old.yaml`**:
   - Identificar novos UCs criados

2. **SE TC existe**, ler `TC-RFXXX.yaml` (versão original)

3. **SE TC existe**, criar novos casos de teste:
   - Adicionar TCs para cada novo UC
   - Cobrir: Backend, Frontend, Segurança, Integração
   - Garantir mínimo 30-50 TCs por novo UC

**Checkpoint:**
- ✅ SE TC existe: Casos de teste criados para novos UCs
- ⚠️ SE TC NÃO existe: PULAR este passo (N/A)
- ✅ **FASE 3 COMPLETA** - Testes atualizados (se aplicável)

---

### FASE 4: RELATÓRIO E VALIDAÇÃO (Passo 13)

#### Passo 13: Gerar Relatório de Delta

**Ações:**

1. **Criar `.temp_ia/aditivo-RFXXX-delta-report.md`**

2. **Documentar mudanças aplicadas**:

```markdown
# RELATÓRIO DE ADITIVO - RFXXX

## FUNCIONALIDADE ADICIONADA

[Descrição da nova funcionalidade]

## DELTA APLICADO

### RF (RFXXX.md, RFXXX.yaml)
- ✅ Adicionado RN-MOD-XXX-NN: [descrição]
- ✅ Adicionado RN-MOD-XXX-NN+1: [descrição]
- ✅ Adicionado RN-MOD-XXX-NN+2: [descrição]
- ✅ Adicionado endpoint POST /api/nova-funcionalidade
- ✅ Adicionada permissão nova_funcionalidade.execute

### UC (UC-RFXXX.md, UC-RFXXX.yaml)
- ✅ Adicionado UC-NN: [nome do UC]
- ✅ Adicionado UC-NN+1: [nome do UC]

### WF (WF-RFXXX.md, WF-RFXXX.yaml)
- ✅ Adicionado WF-NN: [tela nova funcionalidade]

### MD (MD-RFXXX.md, MD-RFXXX.yaml)
- ✅ Adicionada tabela: nova_funcionalidade
- ✅ Adicionado campo: nova_coluna na tabela existente

### MT (MT-RFXXX.yaml)
- ✅ Adicionadas 10 massas de teste para UC-NN

### TC (TC-RFXXX.yaml)
- ✅ Adicionados 35 casos de teste para UC-NN

## VALIDAÇÕES EXECUTADAS

- ✅ validator-rf-uc.py: PASS (exit code 0)
- ✅ RF.md ↔ RF.yaml: 100% sincronizado
- ✅ UC.md ↔ UC.yaml: 100% sincronizado
- ✅ WF.md ↔ WF.yaml: 100% sincronizado
- ✅ MD.md ↔ MD.yaml: 100% sincronizado

## COBERTURA TOTAL

- ✅ Nova funcionalidade 100% coberta em RF
- ✅ Nova funcionalidade 100% coberta em UC
- ✅ Nova funcionalidade 100% coberta em WF
- ✅ Nova funcionalidade 100% coberta em MD
- ✅ Nova funcionalidade 100% coberta em MT
- ✅ Nova funcionalidade 100% coberta em TC

## VEREDICTO FINAL

✅ **ADITIVO APLICADO COM SUCESSO**

Todos os documentos foram atualizados com cobertura total da nova funcionalidade.
Versões `_old` criadas para rastreabilidade.
```

**Checkpoint:**
- ✅ Relatório de delta gerado
- ✅ **EXECUÇÃO COMPLETA**

---

## 6. Validações Obrigatórias (Durante Execução)

| # | Validação | Como Verificar | Ação se Falhar |
|---|-----------|----------------|----------------|
| 1 | Backups `_old` criados | Verificar existência dos 10 arquivos `_old` | BLOQUEAR execução |
| 2 | RF atualizado com mínimo 3 RNs | Contar RNs novas em RFXXX.md | Adicionar mais RNs |
| 3 | RF.md ↔ RF.yaml sincronizados | Comparar RNs, permissões, catálogo | Corrigir inconsistências |
| 4 | UC cobre 100% do delta RF | Executar validator-rf-uc.py | Criar UCs faltantes |
| 5 | UC.md ↔ UC.yaml sincronizados | Comparar UCs em ambos os formatos | Corrigir inconsistências |
| 6 | WF cobre 100% dos novos UCs | Comparar lista de UCs vs WFs | Criar WFs faltantes |
| 7 | WF.md ↔ WF.yaml sincronizados | Comparar WFs em ambos os formatos | Corrigir inconsistências |
| 8 | MD atualizado (se aplicável) | Verificar Seção 9 do RF | Adicionar tabelas/campos |
| 9 | MD.md ↔ MD.yaml sincronizados | Comparar tabelas em ambos os formatos | Corrigir inconsistências |
| 10 | MT cobre novos UCs | Contar massas de teste por UC | Adicionar massas faltantes |
| 11 | TC cobre novos UCs | Contar TCs por UC (mínimo 30) | Adicionar TCs faltantes |
| 12 | Relatório de delta gerado | Verificar `.temp_ia/aditivo-RFXXX-delta-report.md` | Gerar relatório |

---

## 7. Critérios de Aprovação

**✅ APROVADO (100%):**
- 12/12 validações PASS
- Todas as versões `_old` criadas
- Cobertura total (RF → UC → WF → MD → MT → TC)
- Zero gaps identificados
- Relatório de delta completo

**❌ REPROVADO (<100%):**
- Qualquer validação FAIL
- Qualquer gap de cobertura
- Inconsistências entre .md e .yaml
- Relatório de delta incompleto

**⚠️ NÃO EXISTE "APROVADO COM RESSALVAS"**
➡️ Aditivo deve ser 100% perfeito ou será REPROVADO.

---

## 8. Estrutura do Relatório de Delta

O relatório **DEVE** seguir este formato:

```markdown
# RELATÓRIO DE ADITIVO - RFXXX

**Data:** YYYY-MM-DD
**Funcionalidade:** [Nome da funcionalidade adicionada]
**Solicitante:** [Nome do usuário]

---

## 1. FUNCIONALIDADE ADICIONADA

[Descrição detalhada do que foi adicionado]

---

## 2. DELTA APLICADO POR DOCUMENTO

### 2.1 RF (RFXXX.md, RFXXX.yaml)

**Mudanças:**
- ✅ Seção 4 (Funcionalidades): Adicionado RF-NOVA-01
- ✅ Seção 5 (Regras de Negócio): Adicionado RN-MOD-XXX-10, RN-MOD-XXX-11, RN-MOD-XXX-12
- ✅ Seção 7 (Permissões): Adicionado nova_funcionalidade.execute
- ✅ Seção 8 (Endpoints): Adicionado POST /api/v1/nova-funcionalidade

**Total de mudanças:** 7 adições

### 2.2 UC (UC-RFXXX.md, UC-RFXXX.yaml)

**Mudanças:**
- ✅ Adicionado UC-10: Executar Nova Funcionalidade
- ✅ Adicionado UC-11: Validar Entrada da Nova Funcionalidade

**Total de mudanças:** 2 UCs novos

### 2.3 WF (WF-RFXXX.md, WF-RFXXX.yaml)

**Mudanças:**
- ✅ Adicionado WF-10: Tela de Nova Funcionalidade
- ✅ Adicionado componente: Botão "Executar Nova Funcionalidade"

**Total de mudanças:** 1 WF novo

### 2.4 MD (MD-RFXXX.md, MD-RFXXX.yaml)

**Mudanças:**
- ✅ Adicionada tabela: nova_funcionalidade (10 campos)
- ✅ Adicionado campo: nova_coluna_flag na tabela existente_x

**Total de mudanças:** 1 tabela, 1 campo

### 2.5 MT (MT-RFXXX.yaml)

**Mudanças:**
- ✅ Adicionadas 15 massas de teste para UC-10
- ✅ Adicionadas 10 massas de teste para UC-11

**Total de mudanças:** 25 massas de teste

### 2.6 TC (TC-RFXXX.yaml)

**Mudanças:**
- ✅ Adicionados 40 TCs para UC-10 (Backend: 15, Frontend: 15, Segurança: 10)
- ✅ Adicionados 35 TCs para UC-11 (Backend: 15, Frontend: 12, Segurança: 8)

**Total de mudanças:** 75 TCs novos

---

## 3. VALIDAÇÕES EXECUTADAS

| Validação | Resultado | Detalhes |
|-----------|-----------|----------|
| Backups `_old` criados | ✅ PASS | 10/10 arquivos |
| RF atualizado (mín. 3 RNs) | ✅ PASS | 3 RNs adicionadas |
| RF.md ↔ RF.yaml sincronizado | ✅ PASS | 100% |
| UC cobre 100% delta RF | ✅ PASS | validator-rf-uc.py: exit code 0 |
| UC.md ↔ UC.yaml sincronizado | ✅ PASS | 100% |
| WF cobre 100% novos UCs | ✅ PASS | 2/2 UCs cobertos |
| WF.md ↔ WF.yaml sincronizado | ✅ PASS | 100% |
| MD atualizado | ✅ PASS | 1 tabela, 1 campo |
| MD.md ↔ MD.yaml sincronizado | ✅ PASS | 100% |
| MT cobre novos UCs | ✅ PASS | 25 massas de teste |
| TC cobre novos UCs | ✅ PASS | 75 TCs (>30 por UC) |
| Relatório de delta gerado | ✅ PASS | Este documento |

**PONTUAÇÃO FINAL:** 12/12 PASS (100%)

---

## 4. COBERTURA TOTAL

- ✅ Nova funcionalidade 100% coberta em RF (3 RNs, 1 endpoint, 1 permissão)
- ✅ Nova funcionalidade 100% coberta em UC (2 UCs novos)
- ✅ Nova funcionalidade 100% coberta em WF (1 WF novo)
- ✅ Nova funcionalidade 100% coberta em MD (1 tabela, 1 campo)
- ✅ Nova funcionalidade 100% coberta em MT (25 massas de teste)
- ✅ Nova funcionalidade 100% coberta em TC (75 casos de teste)

---

## 5. ARQUIVOS MODIFICADOS

**Backups criados (_old):**
- RFXXX_old.md
- RFXXX_old.yaml
- UC-RFXXX_old.md
- UC-RFXXX_old.yaml
- WF-RFXXX_old.md
- WF-RFXXX_old.yaml
- MD-RFXXX_old.md
- MD-RFXXX_old.yaml
- MT-RFXXX_old.yaml
- TC-RFXXX_old.yaml

**Documentos atualizados:**
- RFXXX.md (7 adições)
- RFXXX.yaml (7 adições)
- UC-RFXXX.md (2 UCs novos)
- UC-RFXXX.yaml (2 UCs novos)
- WF-RFXXX.md (1 WF novo)
- WF-RFXXX.yaml (1 WF novo)
- MD-RFXXX.md (1 tabela, 1 campo)
- MD-RFXXX.yaml (1 tabela, 1 campo)
- MT-RFXXX.yaml (25 massas de teste)
- TC-RFXXX.yaml (75 casos de teste)

---

## 6. VEREDICTO FINAL

✅ **ADITIVO APLICADO COM SUCESSO (100%)**

Todos os documentos foram atualizados com cobertura total da nova funcionalidade.
Versões `_old` criadas para rastreabilidade.

---

**Próximos passos:**
1. Executar validação completa: `docs/prompts/documentacao/validacao/aditivo.md`
2. Se aprovado: Commit e merge
3. Executar backend-aditivo para implementar código
4. Executar frontend-aditivo para implementar UI
```

---

## 9. Regras Invioláveis

1. **NUNCA** modificar originais antes de criar `_old`
2. **SEMPRE** sobrescrever `_old` (não acumular versões)
3. **SEMPRE** propagar mudanças em cascata (RF → UC → WF → MD → MT → TC)
4. **SEMPRE** validar cobertura 100% em cada nível
5. **NUNCA** aprovar com ressalvas (0% ou 100%)
6. **SEMPRE** gerar relatório de delta
7. **SEMPRE** manter sincronização .md ↔ .yaml

---

## 10. Atualização de STATUS.yaml

Após conclusão, atualizar:

```yaml
documentacao:
  aditivo:
    executado: true
    data: "YYYY-MM-DD"
    funcionalidade_adicionada: "Nome da funcionalidade"
    delta_report: ".temp_ia/aditivo-RFXXX-delta-report.md"
    aprovado: true
```

---

## 11. Proibições Absolutas

- ❌ Modificar código (backend/frontend) - este contrato é SOMENTE documentação
- ❌ Aprovar com gaps de cobertura
- ❌ Pular etapas do workflow (RF → UC → WF → MD → MT → TC)
- ❌ Manter versões `_old` históricas (sempre sobrescrever)
- ❌ Executar sem branch adequado (`feature/RFXXX-aditivo-*`)

---

## 12. Exemplo Prático

**Solicitação:**
```
Conforme docs/contracts/documentacao/execucao/aditivo.md para RF028.
Adicionar funcionalidade de "Exportação em PDF".
Seguir CLAUDE.md.
```

**Execução:**

1. **FASE 1 - BACKUP:**
   - Criar RF028_old.md, RF028_old.yaml
   - Criar UC-RF028_old.md, UC-RF028_old.yaml
   - Criar WF-RF028_old.md, WF-RF028_old.yaml
   - Criar MD-RF028_old.md, MD-RF028_old.yaml
   - Criar MT-RF028_old.yaml
   - Criar TC-RF028_old.yaml

2. **FASE 2 - EVOLUÇÃO:**
   - **RF028:** Adicionar RN-CLI-028-15, RN-CLI-028-16, RN-CLI-028-17 (exportação PDF)
   - **RF028:** Adicionar endpoint GET /api/v1/clientes/export/pdf
   - **RF028:** Adicionar permissão cliente.export_pdf
   - **UC-RF028:** Criar UC-12: Exportar Lista de Clientes em PDF
   - **WF-RF028:** Criar WF-12: Tela de Exportação PDF
   - **MD-RF028:** Sem mudanças no modelo (não requer novas tabelas)

3. **FASE 3 - TESTES:**
   - **MT-RF028:** Adicionar 12 massas de teste para UC-12
   - **TC-RF028:** Adicionar 40 TCs para UC-12

4. **FASE 4 - RELATÓRIO:**
   - Gerar `.temp_ia/aditivo-RF028-delta-report.md`
   - Documentar 3 RNs, 1 endpoint, 1 permissão, 1 UC, 1 WF, 12 MTs, 40 TCs

**Resultado:**
✅ ADITIVO APLICADO COM SUCESSO (100%)

---

## 13. Versionamento

- **Criado em:** 2026-01-03
- **Última atualização:** 2026-01-03
- **Versão:** 1.0

---

**Mantido por:** Time de Arquitetura IControlIT
**Governado por:** CLAUDE.md
