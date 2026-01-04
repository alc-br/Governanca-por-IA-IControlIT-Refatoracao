# CONTRATO DE MANUTENÇÃO / CORREÇÃO CONTROLADA

Este documento regula **exclusivamente atividades de manutenção e correção** em funcionalidades **já existentes** no sistema.

Este contrato é **executável**, **vinculante** e **inviolável**.

Ele NÃO autoriza evolução funcional, refatoração ampla, alterações arquiteturais ou mudanças de escopo.

---

## DEPENDÊNCIA OBRIGATÓRIA

Este contrato **DEPENDE** do contrato:

- **CONTRATO-PADRAO-DESENVOLVIMENTO.md**

Antes de executar este contrato, o agente **DEVE**:

1. Ler `CONTRATO-PADRAO-DESENVOLVIMENTO.md` **COMPLETAMENTE**
2. Seguir os padrões técnicos definidos (autorização, multi-tenancy, etc.)
3. Consultar as fontes externas obrigatórias:
   - `D:\DocumentosIC2\arquitetura.md`
   - `D:\DocumentosIC2\inteligencia-artificial\prompts\desenvolvimento.md`

**VIOLAÇÃO:** Executar este contrato sem ler o CONTRATO-PADRAO-DESENVOLVIMENTO.md
é considerado **execução inválida**.

---

## IDENTIFICAÇÃO DO AGENTE

**PAPEL:** Agente Executor de Manutenção  
**TIPO DE ATIVIDADE:** Correção Controlada (Hotfix Governado)

---

## NATUREZA DA SOLICITAÇÃO

- [x] Manutenção
- [x] Correção de erro
- [ ] Novo requisito
- [ ] Evolução funcional
- [ ] Refatoração

Qualquer atividade fora de **manutenção corretiva** é automaticamente **PROIBIDA** por este contrato.

---

## ATIVAÇÃO DO CONTRATO

Este contrato é ativado quando a solicitação contiver
explicitamente a expressão:

"Conforme CONTRATO DE MANUTENÇÃO / CORREÇÃO CONTROLADA"

A descrição do erro, sintomas e contexto
DEVE estar **exclusivamente na mensagem da solicitação**.

O contrato **NÃO deve ser editado** para cada correção.


---

## VALIDACAO GIT OBRIGATORIA (ANTES DE CRIAR BRANCH)

Antes de criar o hotfix branch, o agente DEVE validar que o branch base esta limpo.

### Workflow de Validacao Git

```bash
# Verificar estado do Git
git status

# Verificar se ha merge conflicts no branch atual
# Se houver markers como <<<<<<< HEAD, ======= ou >>>>>>>
# PARAR imediatamente
```

**Regras de Validacao Git:**

- Se `git status` mostrar **merge conflicts** (arquivos com markers):
  - **PARAR** imediatamente
  - **REPORTAR** conflitos ao usuario
  - **NAO** criar hotfix branch
  - **AGUARDAR** resolucao manual dos conflitos

- Se branch atual estiver **limpo** (sem conflicts):
  - **PROSSEGUIR** para criar hotfix branch
  - Continuar com correcao

**Justificativa:**

**Nao adianta criar hotfix branch a partir de um branch com merge conflicts.**

Se criar branch de `dev` quando `dev` tem conflitos:
- Hotfix branch **herda os conflitos**
- Build **falha imediatamente**
- Erros aparecem como se fossem da correcao
- Depuracao fica confusa
- Retrabalho garantido

**A validacao Git ANTES de criar branch evita trabalho desperdicado.**

---

## CONSULTA OBRIGATÓRIA À BASE DE CONHECIMENTO

Antes de criar a TODO LIST e iniciar análise do erro, o agente **DEVE**:

### 1. IDENTIFICAR Camada do Erro

Determinar se o erro está em:
- Backend (.NET, EF Core, handlers, etc.) → Consultar `backend.yaml`
- Frontend (Angular, componentes, rotas, etc.) → Consultar `frontend.yaml`
- Ambos → Consultar ambos os arquivos

### 2. LER Base de Conhecimento Apropriada

```bash
# Se erro no backend
cat docs/base-conhecimento/backend.yaml

# Se erro no frontend
cat docs/base-conhecimento/frontend.yaml

# Se erro em ambos (ler os dois)
cat docs/base-conhecimento/backend.yaml
cat docs/base-conhecimento/frontend.yaml
```

### 3. PROCURAR Erro Similar

Verificar se erro já foi enfrentado e resolvido antes:
- Buscar em `problemas:` por sintomas similares
- Buscar em `erros_comuns:` por mensagem de erro
- Buscar em `troubleshooting:` por categoria

### 4. APLICAR Solução Conhecida (se encontrada)

Se encontrar problema similar:
- ✅ Aplicar solução documentada
- ✅ Validar que resolve o erro
- ✅ Declarar: "Solução aplicada da base de conhecimento: [descrição]"
- ✅ Pular para merge e commit

Se NÃO encontrar:
- ✅ Prosseguir com investigação normal
- ✅ Documentar solução ao final (ver próxima seção)

**IMPORTANTE:**
- Esta consulta é **OBRIGATÓRIA** antes de investigar
- Pode economizar horas de debugging
- Declarar: "Base de conhecimento consultada: [backend/frontend/ambos]"

---

## ATUALIZAÇÃO OBRIGATÓRIA DA BASE DE CONHECIMENTO (AO FINAL)

Ao resolver erro **RELEVANTE** que NÃO estava documentado, o agente **DEVE**:

### Critério de Relevância para Manutenção

Documentar SE E SOMENTE SE:
- ✅ Investigação levou > 30min
- ✅ Erro NÃO estava em `erros_comuns:` ou `problemas:`
- ✅ Causa raiz não era óbvia
- ✅ Erro pode ocorrer novamente em outros RFs ou cenários

NÃO documentar:
- ❌ Erros triviais (config local, dependência faltando)
- ❌ Bugs de código específico do RF (não se repete)
- ❌ Erros já documentados

### Qual Base Atualizar

- Erro em backend → Atualizar `docs/base-conhecimento/backend.yaml`
- Erro em frontend → Atualizar `docs/base-conhecimento/frontend.yaml`
- Erro em ambos → Atualizar ambos os arquivos

### Template de Documentação

```yaml
problemas:
  - problema: "Descrição clara do erro enfrentado"
    contexto: "Manutenção RFXXX ou cenário genérico"
    sintoma: "Mensagem de erro exata ou comportamento observado"
    causa_raiz: "Análise técnica: por que ocorreu"
    solucao: |
      Passo a passo da correção:
      1. Primeiro passo da investigação
      2. Identificação da causa
      3. Correção aplicada (com código se aplicável)
    arquivos_afetados:
      - "backend/ou/frontend/caminho/arquivo"
    data_registro: "YYYY-MM-DD"
    tags: [manutencao, categoria, tecnologia]
```

**AÇÃO OBRIGATÓRIA:**
- Adicionar novo problema ao final de `problemas:` no YAML apropriado
- Declarar: "Base de conhecimento atualizada: [backend/frontend] - novo problema documentado"
- Incluir essa atualização no commit da correção

---

## TODO LIST OBRIGATORIA (LER PRIMEIRO)

> **ATENCAO:** O agente DEVE criar esta todo list IMEDIATAMENTE apos ativar o contrato.
> **NENHUMA ACAO** pode ser executada antes da todo list existir.
> **COPIAR EXATAMENTE** o template abaixo.

### Template para Correcao de Erro

```
TODO LIST - Manutencao/Correcao
================================

[pending] Validar estado Git (BLOQUEANTE)
  |-- [pending] git status
  |-- [pending] Verificar se ha merge conflicts (markers <<<<<<< HEAD)
  |-- [pending] SE houver conflicts → PARAR e REPORTAR
  +-- [pending] SE limpo → PROSSEGUIR

[pending] Validar branch e trocar para DEV (BLOQUEANTE)
  |-- [pending] BRANCH_ATUAL=$(git branch --show-current)
  |-- [pending] SE em main/master → BLOQUEAR e trocar para dev
  |-- [pending] SE não em dev → trocar para dev
  |-- [pending] BRANCH_ORIGINAL="dev"
  +-- [pending] Confirmar que está em dev antes de prosseguir

[pending] Validar alinhamento RF ↔ Correção (BLOQUEANTE)
  |-- [pending] Ler RFXXX.md (requisitos funcionais)
  |-- [pending] Ler UC-RFXXX.md (casos de uso)
  |-- [pending] Ler TC-RFXXX.yaml (casos de teste, se aplicável)
  |-- [pending] Validar que erro é DESVIO da especificação (não funcionalidade nova)
  |-- [pending] SE RF NÃO especifica comportamento → PARAR e REPORTAR
  +-- [pending] Identificar gaps documentação ↔ código (reportar ao usuário)

[pending] Analisar o erro reportado
  |-- [pending] Ler relatorio de erros (se fornecido)
  |-- [pending] Reproduzir o erro localmente
  |-- [pending] Identificar causa raiz
  +-- [pending] Validar que o erro existe

[pending] Criar branch hotfix A PARTIR DE DEV
  |-- [pending] git checkout -b hotfix/correcao-<modulo>
  +-- [pending] Confirmar branch criado a partir de dev

[pending] Aplicar correcao minima
  |-- [pending] Corrigir SOMENTE o erro identificado
  |-- [pending] NAO refatorar codigo nao relacionado
  |-- [pending] NAO adicionar melhorias extras
  +-- [pending] Validar que correcao funciona

[pending] Executar validacoes obrigatorias
  |-- [pending] dotnet build (backend, se aplicavel)
  |-- [pending] npm run build (frontend, se aplicavel)
  |-- [pending] Executar testes existentes
  +-- [pending] Confirmar que nenhum novo erro foi introduzido

[pending] Prova de correcao
  |-- [pending] Demonstrar que erro original nao ocorre mais
  |-- [pending] Validar funcionamento esperado
  +-- [pending] Confirmar ausencia de efeitos colaterais

[pending] Atualizar STATUS.yaml (OBRIGATORIO)
  |-- [pending] Adicionar entrada em execucao.manutencao
  |-- [pending] Incluir: data, tipo, descricao, erro_original, causa_raiz
  |-- [pending] Incluir: arquivos_alterados, branch, commit
  |-- [pending] Incluir: validacao_rf.alinhado, gaps_identificados
  |-- [pending] Incluir: resultado, testes_apos_correcao
  +-- [pending] NAO alterar execucao.backend, execucao.frontend ou documentacao.*

[pending] Fazer commit da correcao no branch hotfix
  |-- [pending] git add . (arquivos corrigidos + STATUS.yaml)
  |-- [pending] git commit -m "fix: <descricao do erro corrigido>"
  +-- [pending] Commit DEVE incluir STATUS.yaml

[pending] Merge para DEV local (OBRIGATORIO)
  |-- [pending] git checkout dev
  |-- [pending] git merge hotfix/correcao-<modulo> --no-ff
  +-- [pending] Confirmar merge concluído

[pending] Permanecer em DEV (estado final)
  |-- [pending] Confirmar branch atual: dev
  +-- [pending] Confirmar correção integrada em dev local

[pending] Declaracao final
  |-- [pending] Causa raiz do erro
  |-- [pending] Onde a correcao foi aplicada
  |-- [pending] Por que nao impacta outras partes
  +-- [pending] Como validar que erro nao ocorre mais
```

### Regras de Execucao da Todo List

1. **COPIAR** o template acima ANTES de qualquer acao
2. **VALIDAR** branch atual e trocar para `dev` ANTES de criar hotfix
3. **BLOQUEAR** se estiver em `main` ou `master` (trocar para `dev`)
4. Atualizar status em tempo real ([pending] → [in_progress] → [completed])
5. **NUNCA** pular etapas
6. **PARAR** em caso de falha (build error/test failure)
7. **FAZER MERGE** do hotfix para `dev` ao final
8. **PERMANECER** em `dev` como estado final
9. Seguir ordem sequencial
10. Somente declarar CONCLUIDO apos **TODOS** os itens completed

---

## WORKFLOW DE BRANCHES (OBRIGATORIO)

### REGRA FUNDAMENTAL: NUNCA USAR MAIN

**BLOQUEIO ABSOLUTO:**
- ❌ **NUNCA** criar branch a partir de `main`
- ❌ **NUNCA** trabalhar diretamente em `main`
- ❌ **NUNCA** fazer commit em `main`
- ✅ **SEMPRE** partir de `dev` local
- ✅ **SEMPRE** retornar para `dev` local

### Fluxo Obrigatório

```
dev local → novo branch hotfix → mudanças → merge para dev local → volta para dev local
```

### 1. Validar Branch Atual e Trocar para DEV (BLOQUEANTE)

```bash
# Verificar branch atual
BRANCH_ATUAL=$(git branch --show-current)
echo "Branch atual: $BRANCH_ATUAL"

# SE estiver em main → BLOQUEAR
if [ "$BRANCH_ATUAL" = "main" ] || [ "$BRANCH_ATUAL" = "master" ]; then
  echo "❌ BLOQUEIO: Não é permitido trabalhar a partir de main/master"
  echo "✅ Trocando para dev..."
  git checkout dev
fi

# SE não estiver em dev → trocar para dev
if [ "$BRANCH_ATUAL" != "dev" ]; then
  echo "✅ Trocando para dev..."
  git checkout dev
fi

# Salvar que estamos em dev
BRANCH_ORIGINAL="dev"
echo "Branch base: $BRANCH_ORIGINAL (dev local)"
```

**VALIDAÇÃO OBRIGATÓRIA:**
- Se `git branch --show-current` retornar `main` ou `master` → **BLOQUEAR** e trocar para `dev`
- Se retornar qualquer outro branch → trocar para `dev`
- Somente prosseguir quando estiver em `dev`

### 2. Criar Branch de Hotfix A PARTIR DO DEV

```bash
# SEMPRE criar a partir de dev (já estamos em dev)
git checkout -b hotfix/correcao-<modulo>
echo "Branch hotfix criado a partir de: dev"
```

### 3. Fazer Mudanças e Commit

```bash
# Aplicar correção no branch hotfix
# ...

# Commit da correção
git add .
git commit -m "fix: <descricao clara do erro corrigido>"
```

### 4. Merge para DEV Local

```bash
# Voltar para dev
git checkout dev

# Fazer merge do hotfix para dev
git merge hotfix/correcao-<modulo> --no-ff

# Confirmar merge
echo "✅ Merge do hotfix para dev concluído"
```

### 5. Permanecer em DEV (Estado Final)

```bash
# Já estamos em dev após o merge
echo "✅ Branch atual: $(git branch --show-current)"
echo "✅ Correção integrada em dev local"
```

**ESTADO FINAL OBRIGATÓRIO:**
- Branch atual: `dev`
- Branch hotfix: criado e mergeado
- Mudanças: integradas em `dev` local
- Branch `main`: **NUNCA tocado**

**IMPORTANTE:**
- O agente **SEMPRE** parte de `dev`
- O agente **SEMPRE** retorna para `dev`
- O agente **SEMPRE** faz merge do hotfix em `dev`
- O agente **NUNCA** faz push (usuário decide)
- O agente **NUNCA** toca em `main`

---

## OBJETIVO

Corrigir **exclusivamente** o erro descrito, restaurando o funcionamento esperado, **sem alterar comportamento não relacionado**.

---

## ESCOPO PERMITIDO (LIMITADO)

O agente PODE atuar **somente se for estritamente necessário** para corrigir o erro descrito, nos seguintes pontos:

- Frontend
- Backend
- Seeds funcionais
- Permissões
- i18n
- Inicialização / Startup
- Configuração de ambiente (somente se comprovadamente relacionada)

---

## ESCOPO PROIBIDO (ABSOLUTO)

É **EXPRESSAMENTE PROIBIDO**:

- Criar novas funcionalidades
- Alterar regras de negócio
- Refatorar código não relacionado ao erro
- “Aproveitar” para melhorias técnicas
- Introduzir novos padrões ou abstrações
- Alterar arquitetura
- Alterar contratos de RF
- Alterar arquivos em `/docs`
- Reorganizar pastas ou módulos
- Ajustar código “preventivamente”

Manutenção NÃO é evolução.

---

## REGRAS OBRIGATÓRIAS

- Seguir estritamente:
  - `ARCHITECTURE.md`
  - `CONVENTIONS.md`
  - `CLAUDE.md`
- Não assumir causa raiz sem evidência concreta
- Qualquer decisão técnica implícita DEVE ser reportada
- Se a correção exigir sair do escopo:
  - PARAR
  - ALERTAR
  - DESCREVER o impacto
  - AGUARDAR decisão

---

## SEEDS E DADOS (SE APLICÁVEL)

Caso o erro envolva ausência ou inconsistência de dados:

- Seeds PODEM ser ajustados
- Somente se:
  - Forem estritamente necessários para corrigir o erro
  - Forem idempotentes
  - Não alterarem dados produtivos

É PROIBIDO:
- Criar seeds temporários
- Criar seeds escondidos em testes
- Criar seeds fora do mecanismo oficial do projeto

---

## GOVERNANÇA DE DOCUMENTAÇÃO (OBRIGATÓRIA)

### Princípio Fundamental

**Manutenção corrige código, NÃO cria funcionalidade.**

Para garantir isso, o agente DEVE validar que a correção está **ALINHADA** com a documentação existente.

---

### PASSO 1: VALIDAR ALINHAMENTO RF ↔ CORREÇÃO (BLOQUEANTE)

**ANTES de aplicar correção, o agente DEVE:**

1. **Ler documentação do RF:**
   - RFXXX.md (requisitos funcionais)
   - UC-RFXXX.md (casos de uso)
   - TC-RFXXX.yaml (casos de teste, se aplicável)

2. **Validar que erro é DESVIO da especificação:**
   - ✅ SE RF especifica comportamento X E código faz Y → **CORRIGIR código para X**
   - ❌ SE RF NÃO especifica comportamento X E código faz Y → **BLOQUEIO** (pode ser funcionalidade nova)

3. **Exemplos:**

   **CORRETO:**
   ```
   RF006.md linha 45: "A tela de gestão de clientes deve ser acessível via menu Management > Clientes"
   UC-RF006.md UC00: "Usuário acessa /management/clientes e vê lista de clientes"

   ERRO: Rota /management/clientes timeout (não acessível)

   VALIDAÇÃO: ✅ RF especifica rota → Correção é RESTAURAR comportamento esperado
   ```

   **BLOQUEIO:**
   ```
   RF999.md: Não menciona relatórios em Excel
   UC-RF999.md: Não menciona exportação

   ERRO: "Botão exportar Excel não funciona"

   VALIDAÇÃO: ❌ RF NÃO especifica exportação → BLOQUEIO (pode ser funcionalidade nova)
   AÇÃO: Reportar ao usuário, solicitar atualização de RF primeiro
   ```

---

### PASSO 2: IDENTIFICAR GAPS DOCUMENTAÇÃO ↔ CÓDIGO (OBRIGATÓRIO)

Durante correção, o agente pode descobrir **gaps** entre código e documentação:

#### Cenário A: Código implementa MAIS que RF especifica

**Exemplo:**
```
RF006.md: Especifica 5 campos no formulário
Código: Implementa 8 campos

GAP: 3 campos extras não documentados
```

**AÇÃO OBRIGATÓRIA:**
- ❌ **NÃO** remover campos extras (pode quebrar produção)
- ✅ **REPORTAR** gap ao usuário
- ✅ **SUGERIR** atualização de RF (em atividade separada)
- ✅ **CONTINUAR** correção do erro original

---

#### Cenário B: RF especifica MAIS que código implementa

**Exemplo:**
```
RF006.md: Especifica validação CNPJ obrigatória
Código: Não valida CNPJ

GAP: Validação faltando
```

**AÇÃO OBRIGATÓRIA:**
- ❌ **NÃO** implementar validação durante manutenção (é funcionalidade nova)
- ✅ **REPORTAR** gap ao usuário
- ✅ **FOCAR** somente no erro original
- ✅ **SUGERIR** criação de correção/evolução separada

---

#### Cenário C: Documentação está ERRADA/DESATUALIZADA

**Exemplo:**
```
RF006.md linha 100: "Rota: /clientes"
Código (produção): Implementa /management/clientes
Menu (produção): Navega para /management/clientes

GAP: RF desatualizado (rota mudou)
```

**AÇÃO OBRIGATÓRIA:**
- ❌ **NÃO** alterar RF durante manutenção
- ✅ **REPORTAR** desatualização ao usuário
- ✅ **SEGUIR** comportamento de PRODUÇÃO (código existente)
- ✅ **SUGERIR** atualização de RF (em atividade separada)

---

### PASSO 3: ATUALIZAR STATUS.yaml (OBRIGATÓRIO)

**APÓS correção aprovada, o agente DEVE atualizar STATUS.yaml:**

```yaml
execucao:
  manutencao:
    - data: "YYYY-MM-DD"
      tipo: "correcao_critica" | "correcao_normal" | "hotfix"
      descricao: "[Descrição clara do erro corrigido]"
      erro_original: "[Mensagem de erro original]"
      causa_raiz: "[Causa raiz identificada]"
      arquivos_alterados:
        - "[caminho/arquivo1.ts]"
        - "[caminho/arquivo2.cs]"
      branch: "hotfix/correcao-<modulo>"
      commit: "<hash do commit>"
      validacao_rf:
        alinhado: true | false
        gaps_identificados:
          - "[Gap 1 - se houver]"
          - "[Gap 2 - se houver]"
      resultado: "APROVADO" | "REPROVADO"
      testes_apos_correcao:
        backend: "[X/Y passando]"
        frontend: "[X/Y passando]"
        e2e: "[X/Y passando]"
```

**PROIBIÇÕES:**
- ❌ **NÃO** alterar `execucao.backend` ou `execucao.frontend`
- ❌ **NÃO** alterar `documentacao.*`
- ✅ **SOMENTE** adicionar entrada em `execucao.manutencao`

---

### PASSO 4: INCLUIR STATUS.yaml NO COMMIT (OBRIGATÓRIO)

**Conforme COMPLIANCE.md seção 9:**

> Qualquer execução que resulte em alteração de código OBRIGA:
> - Atualizar STATUS.yaml
> - Incluir STATUS.yaml no commit

**VIOLAÇÃO:** Commit sem STATUS.yaml = execução incompleta.

---

### PROIBIÇÕES ABSOLUTAS

É **EXPRESSAMENTE PROIBIDO** durante manutenção:

- ❌ Alterar RFXXX.md ou RFXXX.yaml
- ❌ Alterar UC-RFXXX.md ou UC-RFXXX.yaml
- ❌ Alterar TC-RFXXX.yaml ou MT-RFXXX.yaml
- ❌ Alterar user-stories.yaml
- ❌ Criar novos UCs ou TCs
- ❌ Alterar regras de negócio especificadas no RF
- ❌ "Aproveitar" para atualizar documentação desatualizada

**Manutenção corrige código para alinhar com RF.**
**Manutenção NÃO altera RF para alinhar com código.**

---

### BLOQUEIO DE EXECUÇÃO

Se durante validação de alinhamento RF ↔ Correção, o agente identificar:

- RF não especifica o comportamento que está sendo "corrigido"
- Correção exigiria alterar RF
- Correção exigiria criar novos UCs

O agente DEVE:
- **PARAR** imediatamente
- **REPORTAR** gap de documentação
- **DECLARAR** que correção não pode prosseguir sem atualização de RF
- **SUGERIR** atualização de RF primeiro (atividade separada)
- **AGUARDAR** decisão do usuário

---

## PROVA DE CORREÇÃO (OBRIGATÓRIA)

A correção **SÓ é considerada válida** quando:

- O erro descrito **não ocorre mais**
- O sistema funciona após restart
- Nenhum novo warning ou erro é introduzido
- Testes existentes continuam passando
- **STATUS.yaml foi atualizado com entrada de manutenção**
- **Validação RF ↔ Correção foi executada e aprovada**
- Se aplicável:
  - Um teste automatizado é ajustado ou criado para evitar regressão

---

## CRITÉRIO DE PRONTO

A atividade de manutenção é considerada concluída somente quando:

- O erro foi corrigido
- O comportamento esperado foi restaurado
- Nenhum efeito colateral foi introduzido
- Nenhuma alteração fora do escopo ocorreu
- Evidência objetiva da correção foi apresentada

---

## DECLARAÇÃO FINAL DO AGENTE (OBRIGATÓRIA)

Ao concluir, o agente DEVE declarar explicitamente:

- Qual era a causa raiz do erro
- Onde a correção foi aplicada
- Por que a correção não impacta outras partes do sistema
- Como validar que o erro não ocorre mais

---

## BLOQUEIO DE EXECUÇÃO

Se, em qualquer momento, a correção exigir:

- Criação de nova funcionalidade
- Alteração de regra de negócio
- Alteração arquitetural
- Mudança estrutural de domínio

O agente DEVE:
- PARAR
- ALERTAR
- DESCREVER a dependência
- AGUARDAR decisão

---

**Este contrato é vinculante.
Qualquer execução fora dele é inválida.**

---

## REGRA DE NEGACAO ZERO

Se uma solicitacao:
- nao estiver explicitamente prevista no contrato ativo, ou
- conflitar com qualquer regra do contrato

ENTAO:

- A execucao DEVE ser NEGADA
- Nenhuma acao parcial pode ser realizada
- Nenhum "adiantamento" e permitido
