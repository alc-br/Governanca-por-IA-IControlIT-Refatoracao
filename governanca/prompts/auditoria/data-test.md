# Auditar Data-Test Attributes de RF

Auditar presença, nomenclatura e unicidade de **data-test attributes** em componentes Angular do **RFXXX** conforme D:\IC2_Governanca\governanca\contracts\auditoria\data-test.md.

**RF:** [Especificar RF, ex: RF006]

---

## Contrato Ativado

**CONTRATO-AUDITORIA-DATA-TEST**

Caminho: `D:\IC2_Governanca\governanca\contracts\auditoria\data-test.md`

---

## Checklist

**Obrigatório:** `D:\IC2_Governanca\governanca\checklists\auditoria\data-test.yaml`

---

## Agente Responsável

**Agente:** Auditor de Data-Test Attributes

**Modo:** READ-ONLY (não corrige código)

---

## Objetivo

Identificar **TODOS os problemas** relacionados a data-test attributes em componentes Angular do RFXXX:

1. **Elementos sem data-test** (botões, inputs, selects, etc.)
2. **Nomenclatura incorreta** (não segue padrão `RFXXX-acao-alvo`)
3. **Duplicações** (mesmo `data-test` em múltiplos elementos)
4. **Cobertura incompleta** (elementos interativos sem atributo)

**SEM alterar código.**

---

## Escopo de Auditoria

### Elementos que DEVEM ter data-test

**OBRIGATÓRIO:**
- ✅ `<button>` (todos)
- ✅ `<input>` (todos os tipos)
- ✅ `<select>` e `<mat-select>`
- ✅ `<textarea>`
- ✅ `<mat-checkbox>`, `<mat-radio-button>`, `<mat-slide-toggle>`
- ✅ `<mat-datepicker>`
- ✅ `<a>` com `(click)` ou `[routerLink]`

**OPCIONAL (não bloqueia):**
- `<div>`, `<span>`, `<mat-icon>` com `(click)`

### Padrão de Nomenclatura Esperado

**Formato:**
```
data-test="RFXXX-<acao>-<alvo>"
```

**Exemplos válidos:**
- `data-test="RF006-salvar-cliente"`
- `data-test="RF006-filtrar-razaosocial"`
- `data-test="RF006-input-cnpj"`
- `data-test="RF006-select-tipo"`

**Exemplos inválidos:**
- `data-test="salvar"` ❌ (falta RFXXX)
- `data-test="btn-salvar"` ❌ (falta RFXXX)
- `data-test="RF006_salvar"` ❌ (underscore)
- `data-test="RF006-SalvarCliente"` ❌ (CamelCase)

### Componentes a Auditar

**Caminho:**
```
D:\IC2\frontend\icontrolit-app\src\app\**\*RFXXX*.component.html
```

**Excluir:**
- `shared/`, `core/`, `layout/` (componentes compartilhados)
- `node_modules/` (bibliotecas externas)

---

## Fluxo de Execução

### FASE 1: Preparação

1. Ler checklist: `D:\IC2_Governanca\governanca\checklists\auditoria\data-test.yaml`
2. Identificar componentes do RFXXX (Glob)
3. Validar que componentes existem (mínimo 1)

### FASE 2: Auditoria de Componentes

**Para cada componente `.component.html`:**

1. Ler arquivo
2. Identificar elementos interativos:
   - `<button>`, `<input>`, `<select>`, `<textarea>`
   - `<mat-select>`, `<mat-checkbox>`, `<mat-radio-button>`, `<mat-slide-toggle>`
   - `<a>` com `(click)` ou `[routerLink]`
3. Verificar presença de `data-test`
4. Validar nomenclatura (padrão `RFXXX-acao-alvo`)
5. Detectar duplicações

**Registrar problemas por severidade:**
- **BLOQUEANTE**: Elemento sem `data-test`
- **ALTA**: Nomenclatura incorreta
- **MÉDIA**: Duplicação de `data-test`
- **BAIXA**: Nomenclatura não segue convenção exata

### FASE 3: Consolidação

1. Consolidar todos os problemas encontrados
2. Classificar por severidade (BLOQUEANTE, ALTA, MÉDIA, BAIXA)
3. Agrupar por componente
4. Gerar relatório estruturado

### FASE 4: Geração de Prompt

1. Gerar prompt de correção estruturado
2. Incluir exemplos ANTES/DEPOIS para cada problema
3. Confirmar escopo de `manutencao-controlada.md`
4. Salvar prompt em `.temp_ia/`

---

## Outputs Esperados

### 1. Relatório de Auditoria

**Arquivo:** `D:\IC2\.temp_ia\RELATORIO-AUDITORIA-DATA-TEST-RFXXX-AAAA-MM-DD.md`

**Conteúdo:**
- Resumo executivo (totais, status)
- Problemas por componente (BLOQUEANTE, ALTA, MÉDIA, BAIXA)
- Recomendações
- Próximos passos

### 2. Prompt de Correção

**Arquivo:** `D:\IC2\.temp_ia\PROMPT-CORRECAO-DATA-TEST-RFXXX-AAAA-MM-DD.md`

**Conteúdo:**
- Contexto da auditoria
- Correções necessárias (ANTES/DEPOIS)
- Validação pós-correção
- Confirmação de escopo cirúrgico

---

## Validação

Antes de finalizar auditoria:

- [ ] Todos os componentes auditados
- [ ] Todos os elementos interativos verificados
- [ ] Problemas classificados por severidade
- [ ] Relatório gerado em `.temp_ia/`
- [ ] Prompt gerado em `.temp_ia/`
- [ ] Nenhum código modificado
- [ ] Usuário informado sobre próximos passos

---

## Importante

**Auditoria NÃO corrige código:**
- ✅ Apenas identifica problemas
- ✅ Gera relatório completo
- ✅ Gera prompt de correção
- ❌ NÃO modifica arquivos
- ❌ NÃO cria branches
- ❌ NÃO executa correções

**Após auditoria:**
- Copiar e colar prompt gerado
- Executar correção via `manutencao-controlada.md`

---

## Exemplo de Uso

```bash
# Ativar auditoria
Auditar data-test do RF006 conforme contracts/auditoria/data-test.md

# Aguardar auditoria completa
# ...

# Copiar prompt gerado
D:\IC2\.temp_ia\PROMPT-CORRECAO-DATA-TEST-RF006-2026-01-08.md

# Executar correção
[Colar prompt completo aqui]
```

---

## Critérios de Aprovação

**✅ APROVADO** (sem correções necessárias):
- 0 problemas BLOQUEANTES
- Apenas problemas ALTA/MÉDIA/BAIXA (opcionais)

**❌ REPROVADO** (correções obrigatórias):
- 1+ problemas BLOQUEANTES
- Gerar prompt de correção

---

## Próximos Passos (Após Auditoria)

1. **Se APROVADO:**
   - Relatório informativo gerado
   - Nenhuma correção obrigatória
   - Prosseguir com testes E2E

2. **Se REPROVADO:**
   - Relatório + prompt gerado
   - Copiar prompt de correção
   - Executar via `manutencao-controlada.md`
   - Re-auditar após correção

---

**Contrato completo:** `D:\IC2_Governanca\governanca\contracts\auditoria\data-test.md`

**Checklist completo:** `D:\IC2_Governanca\governanca\checklists\auditoria\data-test.yaml`
