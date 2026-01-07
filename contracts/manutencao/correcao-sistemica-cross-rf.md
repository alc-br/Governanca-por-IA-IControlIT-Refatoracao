# CONTRATO DE CORREÇÃO SISTÊMICA CROSS-RF

**Versão:** 1.0
**Data:** 2026-01-05
**Status:** Vigente

Este contrato regula **exclusivamente correções sistêmicas** que afetam **múltiplos RFs simultaneamente**, quando a correção é de **natureza técnica/infraestrutural**, não funcional.

Este contrato é **executável**, **vinculante** e **inviolável**.

---

## IDENTIFICAÇÃO DO AGENTE

**PAPEL:** Agente Executor de Correção Sistêmica Cross-RF
**TIPO DE ATIVIDADE:** Correção Técnica/Infraestrutural em Múltiplos RFs

---

## NATUREZA DA SOLICITAÇÃO

- [x] Correção técnica/infraestrutural
- [x] Afeta múltiplos RFs
- [x] Correção idêntica em todos os RFs
- [ ] Funcionalidade de negócio
- [ ] Evolução funcional
- [ ] Refatoração

**Qualquer atividade de natureza funcional é automaticamente PROIBIDA por este contrato.**

---

## ⚠️ PROIBIÇÕES ABSOLUTAS - GIT E BRANCHES

**ANTES de qualquer ação, o agente DEVE estar ciente:**

### NUNCA TOCAR NO MAIN/MASTER

- ❌ **NUNCA** criar branch a partir de `main` ou `master`
- ❌ **NUNCA** fazer checkout de `main` ou `master`
- ❌ **NUNCA** trabalhar diretamente em `main` ou `master`
- ❌ **NUNCA** fazer commit em `main` ou `master`
- ❌ **NUNCA** fazer merge para `main` ou `master`
- ❌ **NUNCA** fazer push para `main` ou `master`
- ❌ **NUNCA** referenciar `main` ou `master` em comandos git

### TUDO PROVÉM DO DEV

- ✅ **SEMPRE** partir de `dev` local
- ✅ **SEMPRE** criar branch a partir de `dev`
- ✅ **SEMPRE** fazer merge de volta para `dev`
- ✅ **SEMPRE** retornar para `dev` como estado final
- ✅ **SEMPRE** validar que está em `dev` antes de começar

**O branch `main` NÃO EXISTE para o agente.**
**O branch `master` NÃO EXISTE para o agente.**
**SOMENTE `dev` existe.**

**VIOLAÇÃO desta regra invalida TODA a execução.**

---

## ATIVAÇÃO DO CONTRATO

Este contrato é ativado quando a solicitação contiver explicitamente:

```
"Conforme CONTRATO DE CORREÇÃO SISTÊMICA CROSS-RF"
```

**E** a correção for de uma das seguintes naturezas:

### Correções Autorizadas (LISTA FECHADA)

1. **Data-test Attributes (Infraestrutura de Testes)**
   - Adicionar/corrigir data-test attributes em componentes Angular
   - Objetivo: Habilitar testes E2E automatizados
   - Validação: Attributes DEVEM estar especificados nos WF-RFXXX.md correspondentes

2. **Correções de Build/Compilação**
   - Corrigir erros de compilação TypeScript/C# idênticos em múltiplos RFs
   - Objetivo: Restaurar capacidade de build
   - Validação: Correção DEVE ser técnica, não alterar comportamento funcional

3. **Atualizações de Dependências Críticas**
   - Atualizar versão de biblioteca com bug de segurança
   - Objetivo: Resolver vulnerabilidade
   - Validação: SOMENTE versão patch/minor, não major

4. **Correções de Linter/Formatação**
   - Aplicar regras de linter/prettier em múltiplos arquivos
   - Objetivo: Conformidade com CONVENTIONS.md
   - Validação: SOMENTE formatação, não alterar lógica

**QUALQUER OUTRA correção NÃO está autorizada por este contrato.**

---

## ESCOPO PERMITIDO (LIMITADO)

### Princípio Fundamental

**Correção sistêmica cross-RF é TÉCNICA/INFRAESTRUTURAL, não FUNCIONAL.**

**Exemplos de correções AUTORIZADAS:**

✅ Adicionar `data-test="btn-save"` em botões de salvar de TODOS os RFs
✅ Corrigir `WritableSignal<T>` em mocks de TODOS os componentes
✅ Atualizar `@angular/core` de 18.0.1 para 18.0.2 (patch)
✅ Aplicar regra ESLint `no-console` em TODOS os componentes

**Exemplos de correções PROIBIDAS:**

❌ Adicionar validação de CNPJ em formulários de TODOS os RFs
❌ Alterar comportamento de autenticação em TODOS os RFs
❌ Adicionar campo "email" em entidades de TODOS os RFs
❌ Refatorar padrão de serviços em TODOS os RFs

---

## REGRA CRÍTICA: VALIDAÇÃO CONTRA WF/UC/MD-RFXXX

**MESMO sendo correção cross-RF, a correção DEVE respeitar o escopo de CADA RF individualmente.**

### Exemplo: Data-test Attributes

**CORRETO:**
```
WF-RF006.md linha 100: "Usuário clica no botão Salvar"
Código RF006: <button>Salvar</button>
Correção: <button data-test="btn-save">Salvar</button>
✅ APROVADO: WF-RF006.md ESPECIFICA ação "clicar no botão Salvar"
```

**INCORRETO:**
```
WF-RF006.md: NÃO menciona botão "Exportar Excel"
Código RF006: <button>Exportar Excel</button>
Correção proposta: <button data-test="btn-export-excel">Exportar Excel</button>
❌ BLOQUEIO: WF-RF006.md NÃO especifica ação "exportar Excel"
```

### Validação Obrigatória por RF

Para CADA RF afetado, o agente DEVE:

1. Ler WF-RFXXX.md (ou UC-RFXXX.yaml, conforme aplicável)
2. Identificar elementos/ações especificados
3. Aplicar correção SOMENTE em elementos especificados
4. NÃO aplicar correção em elementos não especificados

**Correção sistêmica NÃO isenta validação individual.**

---

## TODO LIST OBRIGATÓRIA

> **ATENÇÃO:** O agente DEVE criar esta todo list IMEDIATAMENTE após ativar o contrato.

### Template para Correção Sistêmica Cross-RF

```
TODO LIST - Correção Sistêmica Cross-RF
========================================

[pending] ⚠️ VALIDAR QUE NUNCA TOCA NO MAIN (BLOQUEANTE CRÍTICO)
  |-- [pending] Confirmar entendimento: main/master NÃO EXISTEM para o agente
  |-- [pending] Confirmar entendimento: TUDO provém do dev
  |-- [pending] Confirmar entendimento: Violação invalida TODA execução
  +-- [pending] SOMENTE prosseguir após confirmação explícita

[pending] Validar natureza da correção (BLOQUEANTE)
  |-- [pending] Verificar se correção está na LISTA FECHADA de correções autorizadas
  |-- [pending] SE NÃO estiver na lista → PARAR e REPORTAR
  +-- [pending] SE estiver na lista → PROSSEGUIR

[pending] Validar estado Git (BLOQUEANTE)
  |-- [pending] git status
  |-- [pending] Verificar se há merge conflicts
  |-- [pending] SE houver conflicts → PARAR e REPORTAR
  +-- [pending] SE limpo → PROSSEGUIR

[pending] Validar branch e trocar para DEV (BLOQUEANTE)
  |-- [pending] BRANCH_ATUAL=$(git branch --show-current)
  |-- [pending] SE em main/master → BLOQUEAR e trocar para dev
  |-- [pending] SE não em dev → trocar para dev
  +-- [pending] Confirmar que está em dev antes de prosseguir

[pending] Auditoria: Identificar RFs afetados
  |-- [pending] Listar TODOS os RFs que precisam de correção
  |-- [pending] Priorizar RFs críticos (login, navegação, CRUD principal)
  +-- [pending] Estimar escopo total (número de arquivos/componentes)

[pending] Validação individual por RF (BLOQUEANTE - REPETIR PARA CADA RF)
  |-- [pending] Ler WF-RFXXX.md (ou UC-RFXXX.yaml, conforme aplicável)
  |-- [pending] Identificar elementos/ações especificados no WF/UC
  |-- [pending] Validar que correção se aplica SOMENTE a elementos especificados
  |-- [pending] SE correção aplicar a elemento NÃO especificado → PULAR esse elemento
  +-- [pending] Marcar RF como validado

[pending] Criar branch hotfix cross-RF A PARTIR DE DEV
  |-- [pending] git checkout -b hotfix/correcao-sistemica-<nome-descritivo>
  +-- [pending] Confirmar branch criado a partir de dev

[pending] Aplicar correção por RF (REPETIR PARA CADA RF)
  |-- [pending] Aplicar correção no RFXXX
  |-- [pending] Validar que correção está conforme WF/UC-RFXXX
  |-- [pending] Executar testes do RFXXX (se aplicável)
  |-- [pending] Validar que nenhum novo erro foi introduzido
  +-- [pending] Marcar RFXXX como corrigido

[pending] Validação final (OBRIGATÓRIA)
  |-- [pending] dotnet build (backend, se aplicável)
  |-- [pending] npm run build (frontend, se aplicável)
  |-- [pending] Executar testes afetados
  +-- [pending] Confirmar que nenhum novo erro foi introduzido

[pending] Prova de correção (OBRIGATÓRIA)
  |-- [pending] Demonstrar que erro/gap original foi corrigido
  |-- [pending] Validar em pelo menos 3 RFs representativos
  +-- [pending] Confirmar ausência de efeitos colaterais

[pending] Atualizar STATUS.yaml de CADA RF (OBRIGATÓRIO)
  |-- [pending] Para CADA RF corrigido:
  |-- [pending]   Adicionar entrada em execucao.manutencao
  |-- [pending]   Incluir: data, tipo, descricao, natureza_correcao
  |-- [pending]   Incluir: rfs_afetados, total_rfs, arquivos_alterados
  |-- [pending]   Incluir: validacao_wf_uc.alinhado, resultado
  +-- [pending] NÃO alterar execucao.backend, execucao.frontend ou documentacao.*

[pending] Fazer commit da correção no branch hotfix
  |-- [pending] git add . (arquivos corrigidos + STATUS.yaml de cada RF)
  |-- [pending] git commit -m "fix(cross-rf): <descricao clara da correção sistêmica>"
  +-- [pending] Commit DEVE incluir STATUS.yaml de TODOS os RFs afetados

[pending] Merge para DEV local (OBRIGATÓRIO)
  |-- [pending] git checkout dev
  |-- [pending] git merge hotfix/correcao-sistemica-<nome> --no-ff
  +-- [pending] Confirmar merge concluído

[pending] Permanecer em DEV (estado final)
  |-- [pending] Confirmar branch atual: dev
  +-- [pending] Confirmar correção integrada em dev local

[pending] Declaração final
  |-- [pending] Natureza da correção (técnica/infraestrutural)
  |-- [pending] RFs afetados (lista completa)
  |-- [pending] Total de arquivos alterados
  |-- [pending] Validação de alinhamento WF/UC por RF
  +-- [pending] Como validar que correção funciona
```

---

## WORKFLOW DE BRANCHES (OBRIGATÓRIO)

### ⚠️ REGRA FUNDAMENTAL: NUNCA TOCAR NO MAIN

**BLOQUEIO ABSOLUTO E INVIOLÁVEL:**

- ❌ **NUNCA** criar branch a partir de `main`
- ❌ **NUNCA** fazer checkout de `main`
- ❌ **NUNCA** trabalhar diretamente em `main`
- ❌ **NUNCA** fazer commit em `main`
- ❌ **NUNCA** fazer merge para `main`
- ❌ **NUNCA** fazer push para `main`
- ❌ **NUNCA** referenciar `main` em comandos git

**TUDO PROVÉM DO DEV:**

- ✅ **SEMPRE** partir de `dev` local
- ✅ **SEMPRE** criar branch a partir de `dev`
- ✅ **SEMPRE** fazer merge de volta para `dev`
- ✅ **SEMPRE** retornar para `dev` como estado final
- ✅ **SEMPRE** validar que está em `dev` antes de começar

### Fluxo Obrigatório

```
dev local → branch hotfix/correcao-sistemica-<nome> → mudanças → merge para dev local → volta para dev local
```

**O branch `main` NÃO EXISTE para o agente.**
**O branch `master` NÃO EXISTE para o agente.**
**SOMENTE `dev` existe.**

### Validação de Branch (BLOQUEANTE - ANTES DE QUALQUER AÇÃO)

**ANTES de criar branch hotfix, o agente DEVE:**

```bash
# 1. Verificar branch atual
BRANCH_ATUAL=$(git branch --show-current)
echo "Branch atual: $BRANCH_ATUAL"

# 2. SE estiver em main/master → BLOQUEIO TOTAL
if [ "$BRANCH_ATUAL" = "main" ] || [ "$BRANCH_ATUAL" = "master" ]; then
  echo "❌ BLOQUEIO TOTAL: Não é permitido trabalhar a partir de main/master"
  echo "✅ Trocando para dev..."
  git checkout dev
fi

# 3. SE não estiver em dev → trocar para dev
if [ "$BRANCH_ATUAL" != "dev" ]; then
  echo "✅ Trocando para dev..."
  git checkout dev
fi

# 4. Confirmar que está em dev
BRANCH_FINAL=$(git branch --show-current)
if [ "$BRANCH_FINAL" != "dev" ]; then
  echo "❌ ERRO: Não conseguiu trocar para dev"
  exit 1
fi

echo "✅ Branch base confirmado: dev"
```

**SOMENTE APÓS validação aprovada, prosseguir com criação do branch hotfix.**

---

## VALIDAÇÃO INDIVIDUAL POR RF (OBRIGATÓRIA)

**MESMO sendo correção cross-RF, cada RF DEVE ser validado individualmente.**

### Processo de Validação por RF

Para CADA RF na lista de RFs afetados:

1. **Ler documentação do RF:**
   - WF-RFXXX.md (se correção afeta fluxos/elementos visuais)
   - UC-RFXXX.yaml (se correção afeta casos de uso)
   - MD-RFXXX.yaml (se correção afeta modelo de dados)

2. **Identificar elementos especificados:**
   - Listar elementos/ações/campos que ESTÃO especificados
   - Listar elementos/ações/campos que NÃO estão especificados

3. **Aplicar correção SOMENTE em elementos especificados:**
   - ✅ SE elemento está especificado → APLICAR correção
   - ❌ SE elemento NÃO está especificado → PULAR (não aplicar)

4. **Registrar validação:**
   - Documentar elementos corrigidos
   - Documentar elementos pulados (não especificados)

### Exemplo: Data-test Attributes no RF006

**Validação:**
```yaml
rf: RF006
documentacao_lida: WF-RF006.md
elementos_especificados:
  - botão Salvar (linha 100 do WF)
  - botão Cancelar (linha 105 do WF)
  - grid de Clientes (linha 80 do WF)
  - campo Nome (linha 90 do WF)
  - campo CNPJ (linha 92 do WF)

elementos_nao_especificados:
  - botão Exportar Excel (NÃO mencionado no WF)
  - botão Imprimir (NÃO mencionado no WF)

correcoes_aplicadas:
  - ✅ Adicionado data-test="btn-save" no botão Salvar
  - ✅ Adicionado data-test="btn-cancel" no botão Cancelar
  - ✅ Adicionado data-test="grid-clientes" no grid
  - ✅ Adicionado data-test="input-nome" no campo Nome
  - ✅ Adicionado data-test="input-cnpj" no campo CNPJ

correcoes_puladas:
  - ❌ NÃO adicionado data-test no botão Exportar Excel (não especificado)
  - ❌ NÃO adicionado data-test no botão Imprimir (não especificado)

alinhamento_wf: true
```

---

## ATUALIZAÇÃO DE STATUS.yaml (OBRIGATÓRIA)

**Para CADA RF afetado, atualizar seu STATUS.yaml:**

```yaml
execucao:
  manutencao:
    - data: "2026-01-05"
      tipo: "correcao_sistemica_cross_rf"
      descricao: "Adicionados data-test attributes em componentes do RF006 conforme WF-RF006.md"
      natureza_correcao: "infraestrutural_testes"
      erro_original: "Testes E2E não executavam devido a data-test attributes ausentes"
      causa_raiz: "Data-test attributes não foram implementados durante criação inicial do RF"
      arquivos_alterados:
        - "D:\IC2\frontend\icontrolit-app/src/app/modules/clientes/clientes-list/clientes-list.component.html"
        - "D:\IC2\frontend\icontrolit-app/src/app/modules/clientes/clientes-form/clientes-form.component.html"
      branch: "hotfix/correcao-sistemica-data-test-attributes"
      commit: "<hash do commit>"
      correcao_sistemica:
        total_rfs_afetados: 42
        documentacao_atual: "RF006"
        elementos_corrigidos: 5
        elementos_pulados: 2 # Não especificados no WF
      validacao_wf_uc:
        alinhado: true
        wf_lido: "WF-RF006.md"
        elementos_especificados: ["botão Salvar", "botão Cancelar", "grid Clientes", "campo Nome", "campo CNPJ"]
        elementos_nao_especificados: ["botão Exportar Excel", "botão Imprimir"]
      resultado: "APROVADO"
      testes_apos_correcao:
        e2e_rf006: "3/3 passando"
```

---

## PROVA DE CORREÇÃO (OBRIGATÓRIA)

A correção sistêmica **SÓ é considerada válida** quando:

- O erro/gap descrito **não ocorre mais** em NENHUM RF afetado
- O sistema funciona após restart
- Nenhum novo warning ou erro é introduzido
- Testes existentes continuam passando
- **STATUS.yaml de CADA RF foi atualizado**
- **Validação WF/UC foi executada para CADA RF**
- **Correção NÃO foi aplicada em elementos não especificados nos WF/UC**
- **Correção permaneceu TÉCNICA/INFRAESTRUTURAL (não funcional)**
- Validação em pelo menos 3 RFs representativos (críticos)

---

## CRITÉRIO DE PRONTO

A correção sistêmica é considerada concluída somente quando:

- O erro/gap foi corrigido em TODOS os RFs afetados
- Cada RF foi validado individualmente contra seu WF/UC
- Nenhum efeito colateral foi introduzido
- Nenhuma alteração funcional ocorreu
- STATUS.yaml de CADA RF foi atualizado
- Evidência objetiva da correção foi apresentada

---

## DECLARAÇÃO FINAL DO AGENTE (OBRIGATÓRIA)

Ao concluir, o agente DEVE declarar explicitamente:

- Qual era a natureza técnica/infraestrutural da correção
- Quantos RFs foram afetados (lista completa)
- Total de arquivos alterados
- Validação de alinhamento WF/UC executada para CADA RF
- Elementos corrigidos vs. elementos pulados (não especificados)
- Como validar que correção funciona em TODOS os RFs

---

## BLOQUEIO DE EXECUÇÃO

Se, em qualquer momento, a correção exigir:

- Alteração de comportamento funcional
- Criação de nova funcionalidade
- Alteração de regra de negócio
- Mudança estrutural de domínio
- Aplicação de correção em elementos NÃO especificados nos WF/UC

O agente DEVE:
- **PARAR** imediatamente
- **ALERTAR** violação de escopo
- **DESCREVER** a dependência/violação
- **AGUARDAR** decisão do usuário

---

## REGRA DE NEGAÇÃO ZERO

Se uma solicitação:
- Não estiver explicitamente prevista na LISTA FECHADA de correções autorizadas, ou
- Conflitar com qualquer regra do contrato, ou
- Requerer alteração funcional (não técnica/infraestrutural)

ENTÃO:
- A execução DEVE ser NEGADA
- Nenhuma ação parcial pode ser realizada
- Nenhum "adiantamento" é permitido

---

**Este contrato é vinculante.
Qualquer execução fora dele é inválida.**

---

**Mantido por:** Time de Arquitetura IControlIT
**Versão:** 1.0
**Data de Vigência:** 2026-01-05
