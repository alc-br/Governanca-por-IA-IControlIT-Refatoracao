# CONTRATO DE AUDITORIA DE DATA-TEST ATTRIBUTES

**Versão:** 1.0
**Data:** 2026-01-08
**Status:** Ativo

---

## 📋 SUMÁRIO EXECUTIVO

### ⚡ O que este contrato faz

Este contrato **AUDITA DATA-TEST ATTRIBUTES** em componentes Angular de um RF específico, identificando:

- ❌ **Elementos faltantes**: Botões, inputs, selects, checkboxes sem `data-test`
- ❌ **Nomenclatura incorreta**: Padrão não seguido (`data-test="RFXXX-action-target"`)
- ❌ **Duplicações**: Mesmo `data-test` usado em múltiplos elementos
- ❌ **Cobertura incompleta**: Elementos interativos sem atributo
- ✅ **Gera relatório completo**: Lista todos os problemas encontrados
- ✅ **Gera prompt de correção**: Para uso com `manutencao-controlada.md`

**Importante:** Este contrato **NÃO corrige código**, apenas **identifica problemas** e **gera prompt de correção**.

---

## 1. Identificação do Agente

| Campo | Valor |
|-------|-------|
| **Papel** | Agente de Auditoria de Data-Test |
| **Escopo** | Análise read-only de componentes Angular |
| **Modo** | Auditoria (sem correções) |

---

## 2. Ativação do Contrato

Este contrato é ativado quando a solicitação mencionar explicitamente:

> **"Conforme contracts/auditoria/data-test.md"**

**OU quando o usuário solicitar via prompt:**

> **"Execute D:\IC2_Governanca\governanca\prompts\auditoria\data-test.md"**

### Parâmetros Obrigatórios

- **RF**: Requisito funcional a auditar (ex: `RF006`)

### Exemplo de Ativação

```
Auditar data-test do RF006 conforme contracts/auditoria/data-test.md
```

---

## 3. OBJETIVO

Identificar **TODOS os problemas relacionados a data-test attributes** em componentes Angular de um RF específico:

1. **Elementos sem data-test** (botões, inputs, selects, checkboxes, radio buttons)
2. **Nomenclatura incorreta** (não segue padrão `RFXXX-action-target`)
3. **Duplicações** (mesmo valor de `data-test` em múltiplos elementos)
4. **Cobertura incompleta** (elementos interativos sem atributo)

**SEM alterar código.**

---

## 4. ESCOPO DE AUDITORIA

### 4.1. Elementos que DEVEM ter data-test

**OBRIGATÓRIO:**
- ✅ `<button>` (todos)
- ✅ `<input>` (todos os tipos)
- ✅ `<select>`
- ✅ `<textarea>`
- ✅ `<mat-select>` (Material)
- ✅ `<mat-checkbox>` (Material)
- ✅ `<mat-radio-button>` (Material)
- ✅ `<mat-slide-toggle>` (Material)
- ✅ `<mat-datepicker>` (Material)
- ✅ Links clicáveis: `<a>` com `(click)` ou `[routerLink]`

**OPCIONAL (não bloqueia testes):**
- `<div>` com `(click)`
- `<span>` com `(click)`
- `<mat-icon>` com `(click)`

### 4.2. Padrão de Nomenclatura

**Formato esperado:**

```
data-test="RFXXX-<acao>-<alvo>"
```

**Exemplos válidos:**
- `data-test="RF006-salvar-cliente"`
- `data-test="RF006-filtrar-nome"`
- `data-test="RF006-ativar-cliente"`
- `data-test="RF006-cancelar-edicao"`
- `data-test="RF006-input-razaosocial"`
- `data-test="RF006-select-tipo"`

**Exemplos inválidos:**
- `data-test="salvar"` ❌ (falta RFXXX)
- `data-test="btn-salvar"` ❌ (falta RFXXX)
- `data-test="RF006_salvar"` ❌ (underscore ao invés de hífen)
- `data-test="RF006-SalvarCliente"` ❌ (CamelCase ao invés de kebab-case)

### 4.3. Componentes a Auditar

**Escopo:**
- Todos os componentes `.component.html` do RF especificado
- Localização típica: `D:\IC2\frontend\icontrolit-app\src\app\**\*RFXXX*.component.html`

**Excluir da auditoria:**
- Componentes compartilhados (ex: `shared/`, `core/`)
- Componentes de layout (ex: `layout/`, `header/`, `sidebar/`)
- Componentes de terceiros (ex: `node_modules/`)

---

## 5. TODO LIST OBRIGATÓRIA (CRIAR PRIMEIRO)

Antes de iniciar a auditoria, criar todo list:

```
TODO LIST - Auditoria Data-Test RFXXX
=======================================

FASE 1: Preparação
  [ ] 1.1. Ler checklist (checklists/auditoria/data-test.yaml)
  [ ] 1.2. Identificar componentes do RFXXX
  [ ] 1.3. Validar que componentes existem

FASE 2: Auditoria de Componentes
  [ ] 2.1. Auditar componente 1 (nome do componente)
  [ ] 2.2. Auditar componente 2 (nome do componente)
  [ ] 2.N. Auditar componente N (nome do componente)

FASE 3: Consolidação
  [ ] 3.1. Consolidar problemas encontrados
  [ ] 3.2. Classificar severidade (BLOQUEANTE, ALTA, MÉDIA, BAIXA)
  [ ] 3.3. Gerar relatório de auditoria

FASE 4: Geração de Prompt
  [ ] 4.1. Gerar prompt de correção estruturado
  [ ] 4.2. Salvar prompt em .temp_ia/
  [ ] 4.3. Apresentar prompt ao usuário
```

---

## 6. FLUXO DE EXECUÇÃO

### FASE 1: Preparação

#### PASSO 1.1: Ler Checklist
```
Read D:\IC2_Governanca\governanca\checklists\auditoria\data-test.yaml
```

#### PASSO 1.2: Identificar Componentes
```bash
# Buscar componentes do RF especificado
Glob "D:\IC2\frontend\icontrolit-app\src\app\**\*RFXXX*.component.html"
```

**Se nenhum componente encontrado:**
- ❌ BLOQUEAR auditoria
- Reportar: "Nenhum componente encontrado para RFXXX"
- PARAR execução

#### PASSO 1.3: Validar Existência
- Confirmar que arquivos `.component.html` existem
- Listar todos os componentes a serem auditados

---

### FASE 2: Auditoria de Componentes

**Para cada componente:**

#### PASSO 2.X: Auditar Componente

1. **Ler arquivo `.component.html`**
   ```
   Read D:\IC2\frontend\icontrolit-app\src\app\...\componente.component.html
   ```

2. **Identificar elementos interativos**
   - Buscar: `<button`, `<input`, `<select`, `<textarea`, `<mat-select`, etc.
   - Contar total de elementos interativos

3. **Verificar data-test**
   - Para cada elemento, verificar presença de `data-test="..."`
   - Validar nomenclatura (padrão `RFXXX-action-target`)
   - Verificar duplicações

4. **Registrar problemas encontrados**
   - **BLOQUEANTE**: Elemento sem `data-test`
   - **ALTA**: Nomenclatura incorreta
   - **MÉDIA**: Duplicação de `data-test`
   - **BAIXA**: Nomenclatura não segue convenção exata (mas funcional)

---

### FASE 3: Consolidação

#### PASSO 3.1: Consolidar Problemas

Agregar todos os problemas encontrados:

```
Componente: clientes-lista.component.html
-----------------------------------------------
- BLOQUEANTE (3):
  * Linha 12: <button> sem data-test (ação: salvar)
  * Linha 45: <input type="text"> sem data-test (campo: razaoSocial)
  * Linha 67: <mat-select> sem data-test (campo: tipo)

- ALTA (2):
  * Linha 23: data-test="salvar" → Deveria ser "RF006-salvar-cliente"
  * Linha 34: data-test="btn-cancelar" → Deveria ser "RF006-cancelar-edicao"

- MÉDIA (1):
  * Linha 89: data-test="RF006-salvar-cliente" duplicado com linha 102
```

#### PASSO 3.2: Classificar Severidade

**Regras de bloqueio:**
- ✅ **0 problemas BLOQUEANTES** → Aprovar (apenas alertar sobre ALTA/MÉDIA/BAIXA)
- ❌ **1+ problemas BLOQUEANTES** → Reprovar (gerar prompt de correção)

#### PASSO 3.3: Gerar Relatório

**Formato do relatório:**

```markdown
# RELATÓRIO DE AUDITORIA - DATA-TEST ATTRIBUTES

**RF:** RFXXX
**Data:** AAAA-MM-DD
**Componentes Auditados:** N

---

## RESUMO EXECUTIVO

- Total de elementos interativos: X
- Elementos com data-test: Y
- Elementos sem data-test: Z
- Problemas BLOQUEANTES: A
- Problemas ALTA: B
- Problemas MÉDIA: C
- Problemas BAIXA: D

**Status:** ❌ REPROVADO (A problemas bloqueantes)

---

## PROBLEMAS POR COMPONENTE

### componente1.component.html

**BLOQUEANTE (N):**
- Linha X: <elemento> sem data-test (descrição)

**ALTA (N):**
- Linha X: data-test="valor-incorreto" → Deveria ser "RFXXX-acao-alvo"

### componente2.component.html

...

---

## RECOMENDAÇÕES

1. Corrigir todos os problemas BLOQUEANTES (obrigatório)
2. Corrigir problemas ALTA (recomendado)
3. Corrigir problemas MÉDIA (opcional)
4. Corrigir problemas BAIXA (opcional)

---

## PRÓXIMOS PASSOS

Executar correção via:
```
Conforme contracts/manutencao/manutencao-controlada.md
```

Usar prompt gerado em: `D:\IC2\.temp_ia\PROMPT-CORRECAO-DATA-TEST-RFXXX.md`
```

**Salvar relatório em:**
```
D:\IC2\.temp_ia\RELATORIO-AUDITORIA-DATA-TEST-RFXXX-AAAA-MM-DD.md
```

---

### FASE 4: Geração de Prompt

#### PASSO 4.1: Gerar Prompt Estruturado

**Template do prompt:**

```markdown
# CORREÇÃO DE DATA-TEST ATTRIBUTES - RFXXX

Conforme D:\IC2_Governanca\governanca\contracts\manutencao\manutencao-controlada.md

---

## CONTEXTO

Durante auditoria de data-test attributes do RFXXX, foram identificados N problemas bloqueantes que impedem execução de testes E2E Playwright.

**Relatório completo:** D:\IC2\.temp_ia\RELATORIO-AUDITORIA-DATA-TEST-RFXXX-AAAA-MM-DD.md

---

## CORREÇÕES NECESSÁRIAS

### Arquivo: src/app/.../componente1.component.html

**Linha X:**
```html
<!-- ANTES -->
<button (click)="salvar()">Salvar</button>

<!-- DEPOIS -->
<button data-test="RFXXX-salvar-entidade" (click)="salvar()">Salvar</button>
```

**Linha Y:**
```html
<!-- ANTES -->
<input type="text" formControlName="campo">

<!-- DEPOIS -->
<input data-test="RFXXX-input-campo" type="text" formControlName="campo">
```

---

### Arquivo: src/app/.../componente2.component.html

...

---

## VALIDAÇÃO

Após correção:
1. Executar: `npm run build` (validar compilação)
2. Re-auditar: Executar auditoria data-test novamente
3. Executar testes E2E: `npm run e2e`

---

## ESCOPO

- ✅ Alterações: N arquivos (Frontend)
- ✅ Camada: Frontend (1 camada)
- ✅ Tipo: Adição de atributos data-test
- ✅ Refatoração: Não
- ✅ Decisões: Não

**Contrato aplicável:** manutencao-controlada.md ✅
```

#### PASSO 4.2: Salvar Prompt

```
Write D:\IC2\.temp_ia\PROMPT-CORRECAO-DATA-TEST-RFXXX-AAAA-MM-DD.md
```

#### PASSO 4.3: Apresentar ao Usuário

**Mensagem final:**

```
✅ Auditoria concluída

Relatório: D:\IC2\.temp_ia\RELATORIO-AUDITORIA-DATA-TEST-RFXXX-AAAA-MM-DD.md
Prompt de correção: D:\IC2\.temp_ia\PROMPT-CORRECAO-DATA-TEST-RFXXX-AAAA-MM-DD.md

---

Para executar correção, copie e cole o prompt:

D:\IC2\.temp_ia\PROMPT-CORRECAO-DATA-TEST-RFXXX-AAAA-MM-DD.md
```

---

## 7. REGRAS DE AUDITORIA

### 7.1. Elementos Obrigatórios

**DEVE ter data-test:**
- Todos os `<button>` (exceto se `disabled` e não-interativo)
- Todos os `<input>` (text, number, email, password, etc.)
- Todos os `<select>` e `<mat-select>`
- Todos os `<textarea>`
- Todos os `<mat-checkbox>`, `<mat-radio-button>`, `<mat-slide-toggle>`
- Todos os `<a>` com `(click)` ou `[routerLink]`

**OPCIONAL (não bloqueia):**
- `<div>`, `<span>`, `<mat-icon>` com `(click)` (auditado, mas não bloqueante)

### 7.2. Validação de Nomenclatura

**Padrão esperado:**
```regex
^RFXXX-[a-z0-9]+(-[a-z0-9]+)*$
```

**Exemplos:**
- ✅ `RF006-salvar-cliente`
- ✅ `RF006-filtrar-razaosocial`
- ✅ `RF006-input-cnpj`
- ❌ `RF006_salvar` (underscore)
- ❌ `RF006-SalvarCliente` (CamelCase)
- ❌ `salvar-cliente` (falta RFXXX)

### 7.3. Detecção de Duplicações

**Regra:**
- Mesmo valor de `data-test` NÃO pode aparecer em múltiplos elementos
- Exceção: Elementos em `*ngFor` (permitido se diferenciados por índice)

**Exemplo de problema:**
```html
<!-- ❌ DUPLICAÇÃO -->
<button data-test="RF006-salvar">Salvar</button>
...
<button data-test="RF006-salvar">Confirmar</button>
```

**Solução:**
```html
<!-- ✅ CORRIGIDO -->
<button data-test="RF006-salvar-cliente">Salvar</button>
<button data-test="RF006-confirmar-edicao">Confirmar</button>
```

---

## 8. PROIBIÇÕES

❌ **PROIBIDO:**
- Modificar código durante auditoria
- Criar branches
- Executar correções
- Alterar arquivos
- Gerar arquivos fora de `.temp_ia/`
- Tomar decisões sobre nomenclatura (seguir padrão estrito)

✅ **PERMITIDO:**
- Ler arquivos `.component.html`
- Analisar código
- Gerar relatórios em `.temp_ia/`
- Gerar prompts de correção

---

## 9. SAÍDAS ESPERADAS

### 9.1. Relatório de Auditoria

**Arquivo:** `D:\IC2\.temp_ia\RELATORIO-AUDITORIA-DATA-TEST-RFXXX-AAAA-MM-DD.md`

**Conteúdo:**
- Resumo executivo
- Problemas por componente (BLOQUEANTE, ALTA, MÉDIA, BAIXA)
- Recomendações
- Próximos passos

### 9.2. Prompt de Correção

**Arquivo:** `D:\IC2\.temp_ia\PROMPT-CORRECAO-DATA-TEST-RFXXX-AAAA-MM-DD.md`

**Conteúdo:**
- Contexto da auditoria
- Correções necessárias (ANTES/DEPOIS)
- Validação pós-correção
- Escopo (confirmar aplicabilidade de `manutencao-controlada.md`)

---

## 10. CHECKLIST DE VALIDAÇÃO

Antes de finalizar auditoria, validar:

- [ ] Todo list criada e completa
- [ ] Todos os componentes auditados
- [ ] Todos os elementos interativos verificados
- [ ] Problemas classificados por severidade
- [ ] Relatório gerado em `.temp_ia/`
- [ ] Prompt de correção gerado em `.temp_ia/`
- [ ] Nenhum código foi modificado
- [ ] Usuário informado sobre próximos passos

---

## 11. EXEMPLO COMPLETO

### Cenário

**RF:** RF006 (Gestão de Clientes)
**Componentes:** `clientes-lista.component.html`, `clientes-form.component.html`

### Execução

1. **FASE 1: Preparação**
   - Checklist lido
   - 2 componentes identificados

2. **FASE 2: Auditoria**
   - `clientes-lista.component.html`: 5 problemas bloqueantes
   - `clientes-form.component.html`: 8 problemas bloqueantes

3. **FASE 3: Consolidação**
   - Total: 13 problemas bloqueantes
   - Status: ❌ REPROVADO
   - Relatório gerado

4. **FASE 4: Prompt**
   - Prompt estruturado gerado
   - 13 correções ANTES/DEPOIS
   - Apresentado ao usuário

### Saída

```
✅ Auditoria concluída

Relatório: D:\IC2\.temp_ia\RELATORIO-AUDITORIA-DATA-TEST-RF006-2026-01-08.md
Prompt: D:\IC2\.temp_ia\PROMPT-CORRECAO-DATA-TEST-RF006-2026-01-08.md

Próxima ação: Copiar e colar prompt para executar correção via manutencao-controlada.md
```

---

## 12. REGRAS FINAIS

1. **Auditoria é read-only**: NUNCA modificar código
2. **Gerar relatório completo**: Identificar TODOS os problemas
3. **Gerar prompt estruturado**: Facilitar correção posterior
4. **Classificar severidade**: Separar BLOQUEANTE de ALTA/MÉDIA/BAIXA
5. **Validar padrão estrito**: `RFXXX-acao-alvo` (kebab-case)
6. **Detectar duplicações**: Mesmo `data-test` não pode repetir
7. **Salvar em `.temp_ia/`**: Todos os artefatos gerados

---

**Mantido por:** Time de Arquitetura IControlIT
**Última Atualização:** 2026-01-08
**Versão:** 1.0
