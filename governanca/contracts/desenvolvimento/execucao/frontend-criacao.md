Você é um agente executor.

# CONTRATO DE EXECUÇÃO – FRONTEND

Este documento define o contrato de execução do agente responsável
pela implementação de **frontends de Requisitos Funcionais**.

Este contrato é **obrigatório**, **executável** e **inviolável**.

Ele NÃO é um prompt.
Ele NÃO deve ser editado por RF.
Ele define **como** o trabalho deve ser executado.

---

## DEPENDÊNCIA OBRIGATÓRIA

Este contrato **DEPENDE** do contrato:

- **CONTRATO-PADRAO-DESENVOLVIMENTO.md**

Antes de executar este contrato, o agente **DEVE**:

1. Ler `CONTRATO-PADRAO-DESENVOLVIMENTO.md` **COMPLETAMENTE**
2. Seguir **TODOS** os checklists e regras definidos
3. Consultar as fontes externas obrigatórias:
   - `D:\DocumentosIC2\arquitetura.md`
   - `D:\DocumentosIC2\inteligencia-artificial\prompts\desenvolvimento.md`
   - `D:\DocumentosIC2\inteligencia-artificial\prompts\traducao.md`

**VIOLAÇÃO:** Executar este contrato sem ler o CONTRATO-PADRAO-DESENVOLVIMENTO.md
é considerado **execução inválida**.

---

## IDENTIFICAÇÃO DO AGENTE

**PAPEL:** Agente Executor de Frontend  
**ESCOPO:** Implementação de frontend com integração completa ao ecossistema

---

## ATIVAÇÃO DO CONTRATO

Este contrato é ativado quando a solicitação contiver explicitamente
a expressão:

> **"Conforme CONTRATO DE EXECUÇÃO – FRONTEND"**

O Requisito Funcional, contexto e escopo específico
DEVEM ser informados **exclusivamente na solicitação**.

Este contrato **NUNCA** deve ser alterado para um RF específico.

---

## HISTÓRICO DE ATUALIZAÇÕES

### v3.0 (2026-01-11)
- **FASE 6.7 adicionada**: Validators Angular Obrigatórios (BLOQUEANTE)
  - Origem: Análise de falhas RF006 (execução #9) - GAP 1
  - Impacto: Resolve 21% das falhas E2E (3/14 falhas)
  - Bloqueio: Frontend sem validators completos = REPROVADO
  - Validações: Validators, mat-error messages, botões disabled em form.invalid

### v2.0 (2026-01-10)
- **FASE 6.6 adicionada**: Material Dialog Backdrop Cleanup (BLOQUEANTE)
  - Origem: Análise de falhas RF006 (execução #7-#9) - GAP 3
  - Impacto: Resolve 17% das falhas E2E (3/18 testes)
  - Padrão: firstValueFrom(dialogRef.afterClosed()) obrigatório
  - Helper: dialog-helpers.ts criado

---

## VALIDACAO GIT OBRIGATORIA (ANTES DE CRIAR BRANCH)

Antes de criar o feature branch, o agente DEVE validar que o branch base esta limpo.

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
  - **NAO** criar feature branch
  - **AGUARDAR** resolucao manual dos conflitos

- Se branch atual estiver **limpo** (sem conflicts):
  - **PROSSEGUIR** para criar feature branch
  - Continuar com implementacao

**Justificativa:**

**Nao adianta criar feature branch a partir de um branch com merge conflicts.**

Se criar branch de `dev` quando `dev` tem conflitos:
- Feature branch **herda os conflitos**
- Build **falha imediatamente**
- Erros aparecem como se fossem do RF
- Depuracao fica confusa
- Retrabalho garantido

**A validacao Git ANTES de criar branch evita trabalho desperdicado.**

---

## REGRA OBRIGATÓRIA - Data-test Attributes (Infraestrutura de Testes E2E)

**TODOS os componentes Angular criados neste contrato DEVEM incluir data-test attributes em elementos interativos.**

### Obrigatoriedade

Data-test attributes são **INFRAESTRUTURA DE TESTES**, não funcionalidade opcional.

**Propósito:**
- Testes E2E Playwright (seletores estáveis)
- Testes de integração
- Automação de QA
- Garantir que 100% dos testes E2E executem

### Elementos que DEVEM ter data-test

- ✅ **Botões** (salvar, cancelar, excluir, adicionar, etc.)
- ✅ **Campos de formulário** (input, select, textarea, checkbox, radio)
- ✅ **Links de navegação** (routerLink, href)
- ✅ **Grids/tabelas** (cabeçalhos, linhas, células clicáveis)
- ✅ **Modals/dialogs** (container e botões)
- ✅ **Menus/dropdowns** (p-menu, p-dropdown, etc.)

### Elementos que NÃO precisam de data-test

- ❌ **Textos estáticos** (labels, parágrafos de ajuda)
- ❌ **Ícones decorativos** (sem ação)
- ❌ **Divs/spans estruturais** (layout)

### Padrão de Nomenclatura

**Formato:** `data-test="<contexto>-<elemento>-<acao>"`

**Exemplos:**
```html
<!-- Botões -->
<button data-test="btn-save">Salvar</button>
<button data-test="btn-cancel">Cancelar</button>

<!-- Campos -->
<input data-test="input-name" type="text" />
<select data-test="select-status"></select>

<!-- Links -->
<a data-test="link-dashboard" routerLink="/dashboard">Dashboard</a>

<!-- Grid -->
<p-table data-test="grid-clients">
  <ng-template pTemplate="header">
    <tr>
      <th data-test="header-name">Nome</th>
    </tr>
  </ng-template>
</p-table>
```

### Validação Obrigatória (BLOQUEANTE)

Antes de considerar frontend CONCLUÍDO, o agente DEVE validar:

1. **Todos elementos especificados no WF-RFXXX.md têm data-test**
   ```bash
   # Verificar presença de data-test no módulo
   grep -r "data-test=" frontend/src/app/modules/RFXXX/
   ```

2. **Nomenclatura segue padrão CONVENTIONS.md**
   - Formato: `<contexto>-<elemento>-<acao>`
   - Sem espaços, hífens como separadores

3. **Data-test está documentado no WF-RFXXX.md**
   - Seção "Elementos de Interface" deve listar data-test attributes

4. **Elementos NÃO especificados no WF foram PULADOS**
   - Correto: Se WF não menciona botão "Exportar", NÃO adicionar data-test nele
   - Incorreto: Adicionar data-test em elementos não documentados

### BLOQUEIO: Frontend sem data-test

Se componente NÃO tiver data-test attributes:
1. **PARAR** execução
2. **REPORTAR** elementos faltantes
3. **NÃO** marcar frontend como concluído
4. **AGUARDAR** correção

**Razão:** Testes E2E dependem de data-test. Sem eles, 100% dos testes FALHAM.

### Exemplo Completo - RF006 (Gestão de Clientes)

**WF-RF006.md especifica:**
- Botão "Salvar Cliente"
- Botão "Cancelar"
- Campo "Nome do Cliente"
- Campo "CNPJ"
- Grid de Clientes

**Implementação CORRETA:**
```html
<!-- Formulário -->
<form>
  <input data-test="input-name" formControlName="nome" />
  <input data-test="input-cnpj" formControlName="cnpj" />

  <button data-test="btn-save">Salvar Cliente</button>
  <button data-test="btn-cancel">Cancelar</button>
</form>

<!-- Grid -->
<p-table data-test="grid-clients">
  <!-- ... -->
</p-table>
```

**Implementação INCORRETA:**
```html
<!-- ❌ SEM data-test attributes -->
<form>
  <input formControlName="nome" />
  <input formControlName="cnpj" />

  <button>Salvar Cliente</button>
  <button>Cancelar</button>
</form>
```

### Integração com STATUS.yaml

Após adicionar data-test attributes, atualizar STATUS.yaml:

```yaml
execucao:
  frontend:
    data_test_attributes:
      aplicado: true
      elementos_cobertos: 15
      elementos_especificados_wf: 15
      cobertura_percentual: 100
      validacao: aprovada
```

**Ver padrões completos em:** `CONVENTIONS.md` (seção 5.6 - Data-test Attributes)

### Auditoria de Data-Test (FASE OBRIGATÓRIA)

**Momento de execução:** ANTES dos Testes E2E

Durante o desenvolvimento, data-test attributes devem ser adicionados em TODOS os elementos interativos conforme são criados. Porém, é comum esquecer elementos ou usar nomenclatura incorreta.

**Antes de executar testes E2E, o agente DEVE:**

1. **Executar auditoria automatizada:**
   ```
   Conforme D:\IC2_Governanca\governanca\prompts\auditoria\data-test.md
   ```

2. **Analisar relatório gerado:**
   - Relatório: `D:\IC2\.temp_ia\RELATORIO-AUDITORIA-DATA-TEST-RFXXX-*.md`
   - Verificar problemas BLOQUEANTES (elementos sem data-test)
   - Verificar problemas ALTA (nomenclatura incorreta)

3. **Corrigir TODOS os problemas identificados:**
   - Usar prompt de correção: `D:\IC2\.temp_ia\PROMPT-CORRECAO-DATA-TEST-RFXXX-*.md`
   - Corrigir via `manutencao-controlada.md`
   - Re-auditar após correções

4. **Validar aprovação:**
   - 0 problemas BLOQUEANTES
   - 0 problemas ALTA
   - 100% dos elementos interativos com data-test

**BLOQUEIO:** Se auditoria reprovar (problemas BLOQUEANTES/ALTA):
- **NÃO** executar testes E2E
- **NÃO** considerar frontend concluído
- **CORRIGIR** todos os problemas
- **RE-AUDITAR** até aprovação

**Justificativa:**
- Testes E2E dependem de data-test attributes
- Sem data-test corretos, 100% dos testes FALHAM
- Auditoria preventiva economiza tempo de debug
- Garante qualidade e manutenibilidade dos testes

---

## CONSULTA OBRIGATÓRIA À BASE DE CONHECIMENTO

Antes de criar a TODO LIST e iniciar qualquer implementação, o agente **DEVE**:

### 1. LER Base de Conhecimento Frontend

```bash
# Ler arquivo completo
cat docs/base-conhecimento/frontend.yaml
```

### 2. PROCURAR Problemas Similares

Verificar se há problemas conhecidos relacionados a:
- Tecnologias que serão usadas (Angular, PrimeNG, HttpClient, etc.)
- Padrões que serão aplicados (standalone components, lazy loading, etc.)
- Funcionalidades UI similares já implementadas

### 3. CONSULTAR Erros Comuns

Revisar seção `erros_comuns:` para antecipar problemas frequentes

### 4. VALIDAR Padrões Obrigatórios

Confirmar conhecimento dos padrões em `padroes:` antes de implementar

### 5. REVISAR Layout Padrão

Consultar `layout_padrao:` para estrutura de página, botões e cores

### 6. EXECUTAR Checklist Pré-Execução

Validar todos os itens em `checklist_pre_execucao:` do YAML

**IMPORTANTE:**
- Esta consulta é **OBRIGATÓRIA** e **BLOQUEANTE**
- Se encontrar problema similar, aplicar solução conhecida
- Se encontrar padrão obrigatório, seguir exatamente como documentado
- Declarar: "Base de conhecimento consultada: [N] problemas conhecidos revisados"

---

## ATUALIZAÇÃO OBRIGATÓRIA DA BASE DE CONHECIMENTO (AO FINAL)

Ao encontrar dificuldade **RELEVANTE** durante implementação, o agente **DEVE**:

### Critério de Relevância

Documentar SE E SOMENTE SE:
- ✅ Problema levou > 30min para resolver
- ✅ Erro não estava documentado em `erros_comuns:`
- ✅ Solução não é óbvia (não está na documentação oficial)
- ✅ Problema pode se repetir em outros RFs

NÃO documentar:
- ❌ Erros triviais (typo, import faltando)
- ❌ Problemas específicos de um RF único
- ❌ Soluções óbvias

### Template de Documentação

```yaml
problemas:
  - problema: "Descrição clara e concisa"
    contexto: "RFXXX ou cenário genérico"
    sintoma: "Erro no console, UI ou comportamento"
    causa_raiz: "Análise técnica do por quê"
    solucao: |
      Passo a passo da solução:
      1. Primeiro passo
      2. Segundo passo
      3. Código exemplo (se aplicável)
    arquivos_afetados:
      - "frontend/src/app/caminho/arquivo.ts"
    data_registro: "YYYY-MM-DD"
    tags: [categoria, tecnologia, ui]
```

**AÇÃO OBRIGATÓRIA:**
- Adicionar novo problema ao final de `problemas:` em `docs/base-conhecimento/frontend.yaml`
- Declarar: "Base de conhecimento atualizada: novo problema documentado"

---

## CONSULTA E REGISTRO DE DECISÕES TÉCNICAS (DECISIONS.md)

O agente **DEVE** interagir com `DECISIONS.md` durante a execução:

### 1. CONSULTA OBRIGATÓRIA (Antes de Implementar)

Antes de iniciar implementação, o agente **DEVE**:

```bash
# Ler decisões técnicas registradas
cat docs/DECISIONS.md
```

**Verificar decisões relacionadas a:**
- Padrões de UI/UX (layout padrão, componentes PrimeNG)
- Escolhas de tecnologia (Angular standalone, lazy loading, state management)
- Regras de navegação e roteamento
- Decisões anteriores que impactam o RF atual

**Declaração obrigatória:**
> "DECISIONS.md consultado: [N] decisões técnicas revisadas"

### 2. IDENTIFICAÇÃO DE DECISÕES IMPLÍCITAS (Durante Implementação)

Durante implementação, o agente **DEVE PARAR e ALERTAR** quando identificar:

#### Situações que exigem registro em DECISIONS.md:

**a) Escolha entre abordagens técnicas equivalentes**
- Exemplo: "Usar Signals vs Observables para state management"
- Exemplo: "Criar service compartilhado vs service por feature"

**b) Desvio de padrão de UI existente**
- Exemplo: "Usar modal ao invés de página separada (diferente do padrão)"
- Exemplo: "Layout customizado diferente do card padrão"

**c) Trade-offs de UX**
- Exemplo: "Paginação server-side vs client-side"
- Exemplo: "Validação eager vs lazy em formulários"

**d) Decisões difíceis de reverter**
- Exemplo: "Estrutura de rotas (mudança afeta navegação global)"
- Exemplo: "Mudança em componente shared usado em vários lugares"

**e) Introdução de nova dependência ou componente**
- Exemplo: "Adicionar biblioteca de gráficos não utilizada antes"
- Exemplo: "Criar novo componente shared genérico"

### 3. PROCEDIMENTO DE ALERTA (OBRIGATÓRIO)

Quando identificar decisão implícita, o agente **DEVE**:

**PASSO 1: PARAR implementação**
- NÃO prosseguir silenciosamente
- NÃO assumir decisão por conta própria

**PASSO 2: ALERTAR usuário**
```
⚠️ DECISÃO TÉCNICA IDENTIFICADA

Contexto: [Descrever situação]
Decisão implícita: [O que está sendo decidido]
Alternativas:
  - Opção A: [Descrição] - Vantagens: [...] - Desvantagens: [...]
  - Opção B: [Descrição] - Vantagens: [...] - Desvantagens: [...]

Recomendação: [Qual opção o agente sugere e por quê]

Esta decisão deve ser registrada em docs/DECISIONS.md?
```

**PASSO 3: AGUARDAR confirmação do usuário**
- Usuário decide qual opção
- Usuário decide se registra em DECISIONS.md

### 4. REGISTRO DE DECISÃO (Se Solicitado)

Se usuário solicitar registro, o agente **DEVE** adicionar ao final de `DECISIONS.md`:

**Template ADR:**
```markdown
### ADR-XXX: [Título da Decisão]

**Data:** YYYY-MM-DD
**Status:** Aceita
**RF Relacionado:** RFXXX (se aplicável)

**Contexto:**
[Descrever problema ou situação que motivou a decisão]

**Decisão:**
[Descrever decisão tomada]

**Alternativas Consideradas:**
- [Alternativa 1]: [Motivo de rejeição]
- [Alternativa 2]: [Motivo de rejeição]

**Consequências:**
- Positivas: [Impactos positivos]
- Negativas: [Impactos negativos ou trade-offs]

**Responsável:** Agente Claude + [Nome do usuário]
```

**IMPORTANTE:**
- Numerar sequencialmente (verificar último ADR registrado)
- Incluir RF relacionado se aplicável
- Ser conciso mas completo
- Declarar: "Decisão técnica registrada: ADR-XXX em DECISIONS.md"

### 5. EXEMPLOS DE DECISÕES QUE DEVEM SER REGISTRADAS

**Exemplo 1: Escolha de Gerenciamento de Estado**
```
ADR-020: Usar Signals para state local de componentes

Contexto: RF035 precisa gerenciar estado complexo de formulário
Decisão: Usar Angular Signals ao invés de Observables
Alternativa rejeitada: RxJS Observables (mais verboso para casos simples)
Consequência: Melhor performance, sintaxe mais simples, menos código
```

**Exemplo 2: Exceção ao Layout Padrão**
```
ADR-021: Dashboard com layout grid customizado

Contexto: RF040 (Dashboard) requer layout diferente do card padrão
Decisão: Criar layout grid responsivo customizado
Alternativa rejeitada: Forçar card padrão (limitaria visualização)
Consequência: Quebra consistência visual, requer CSS específico
```

### 6. DECISÕES QUE NÃO PRECISAM SER REGISTRADAS

**NÃO registrar:**
- ❌ Aplicação de layout padrão já estabelecido
- ❌ Seguir padrão de componentes PrimeNG já usado
- ❌ Decisões triviais (cores, espaçamento)
- ❌ Decisões reversíveis sem impacto (refactoring local)

**Registrar:**
- ✅ Exceções a padrões de UI/UX estabelecidos
- ✅ Introdução de novos padrões de componentes
- ✅ Escolhas com trade-offs de UX significativos
- ✅ Decisões que afetam navegação ou estrutura global

---

## TODO LIST OBRIGATORIA (LER PRIMEIRO)

> **ATENCAO:** O agente DEVE criar esta todo list IMEDIATAMENTE apos ativar o contrato.
> **NENHUMA ACAO** pode ser executada antes da todo list existir.
> **COPIAR EXATAMENTE** o template abaixo, substituindo RFXXX pelo RF real.

### Template para RF Unico (RFXXX)

```
TODO LIST - Frontend RFXXX
==========================

[pending] Ler anti-esquecimento PRIMEIRO
  +-- [pending] Ler D:\IC2\docs\anti-esquecimento-frontend.md

[pending] Validacao Git Inicial (ANTES de criar branch)
  |-- [pending] git status (verificar estado limpo)
  |-- [pending] Verificar ausencia de merge conflicts no branch atual
  |-- [pending] Se merge conflicts existirem: PARAR, REPORTAR, AGUARDAR resolucao
  +-- [pending] Somente criar branch se Git estado limpo

[pending] Ler documentacao do RF
  |-- [pending] Ler RFXXX.md
  |-- [pending] Ler UC-RFXXX.md
  |-- [pending] Ler WF-RFXXX.md
  +-- [pending] Identificar endpoints do backend

[pending] Validar pre-requisitos
  |-- [pending] Verificar backend implementado e mergeado em dev
  |-- [pending] Identificar permissoes necessarias
  +-- [pending] Declarar perfil de acesso (minimo: developer)

[pending] Prova de Acesso (OBRIGATORIA)
  |-- [pending] Autenticar como developer
  |-- [pending] Executar chamada real ao backend
  |-- [pending] Confirmar retorno HTTP 200
  +-- [pending] Se 401/403/404: PARAR e corrigir

[pending] Seeds Funcionais (se necessario)
  |-- [pending] Garantir entidades dependentes
  |-- [pending] Garantir permissoes existem
  |-- [pending] Associar permissoes ao perfil developer
  +-- [pending] Registrar na Central de Modulos

[pending] Mapear Dependencias Funcionais
  |-- [pending] Ler MD-RFXXX.md e identificar FKs
  |-- [pending] Identificar entidades pai (dropdowns)
  |-- [pending] Listar rotas das dependencias
  +-- [pending] Definir ordem de setup E2E

[pending] Validar Dependencias (Pre-E2E)
  |-- [pending] Para cada dependencia na ordem:
  |     |-- [pending] Navegar para rota da dependencia
  |     |-- [pending] Verificar se tela carrega (HTTP 200)
  |     |-- [pending] Verificar se CRUD basico funciona
  |     +-- [pending] Se FALHAR: analisar causa (frontend atual vs outro RF)
  |-- [pending] Se erro no frontend atual: CORRIGIR e re-testar
  +-- [pending] Se erro em outro RF: criar RELATORIO-ERROS-RFXXX.md

[pending] Implementar Componentes UI (ADICIONAR DATA-TEST DURANTE DESENVOLVIMENTO)
  |-- [pending] Tela de Listagem (seguir padrao /management/users)
  |     +-- [pending] Adicionar data-test em TODOS os elementos interativos
  |-- [pending] Tela de Criar/Editar
  |     +-- [pending] Adicionar data-test em TODOS os elementos interativos
  |-- [pending] Tela de Visualizar
  |     +-- [pending] Adicionar data-test em TODOS os elementos interativos
  |-- [pending] Modais (Confirmacao, Sucesso, Erro)
  |     +-- [pending] Adicionar data-test em TODOS os botoes
  +-- [pending] Estados (Loading, Vazio, Erro)
        +-- [pending] Adicionar data-test em botoes de acao

[pending] Implementar Services
  |-- [pending] Criar service de API
  |-- [pending] Criar models/interfaces
  +-- [pending] Integrar com endpoints do backend

[pending] Configurar Rotas e Menu
  |-- [pending] Configurar rotas do modulo
  |-- [pending] Adicionar item no menu (se aplicavel)
  +-- [pending] Configurar guards de permissao

[pending] Implementar i18n (OBRIGATORIO)
  |-- [pending] Criar chaves pt-BR
  |-- [pending] Criar chaves en-US
  |-- [pending] Criar chaves es-ES
  +-- [pending] Validar ZERO warnings no console

[pending] Auditoria de Data-Test Attributes (OBRIGATORIO - PRE-TESTE E2E)
  |-- [pending] Executar auditoria: Conforme D:\IC2_Governanca\governanca\prompts\auditoria\data-test.md
  |-- [pending] Analisar relatorio de auditoria gerado
  |-- [pending] Se problemas BLOQUEANTES: corrigir TODOS antes de prosseguir
  |-- [pending] Se problemas ALTA: corrigir TODOS antes de prosseguir
  |-- [pending] Re-auditar apos correcoes
  +-- [pending] Validar 0 problemas BLOQUEANTES e 0 problemas ALTA

[pending] Testes E2E (Playwright - OBRIGATORIO)
  |-- [pending] TC-E2E: Login como developer
  |-- [pending] TC-E2E: Acesso via menu
  |-- [pending] TC-E2E: Carregamento da listagem
  |-- [pending] TC-E2E: Criar registro (caminho feliz)
  |-- [pending] TC-E2E: Editar registro
  |-- [pending] TC-E2E: Excluir registro
  |-- [pending] Validar responsividade (desktop/mobile)
  +-- [pending] TC-E2E: Criar registro FINAL como evidencia (NAO excluir)

[pending] Validar Criterio de Pronto
  |-- [pending] Build frontend OK (ng build)
  |-- [pending] Nenhum warning i18n no console
  |-- [pending] Nenhum erro 401/403 no console
  |-- [pending] Seeds aplicados sem reset manual
  |-- [pending] Testes E2E APROVADOS
  +-- [pending] Funcionalidade navegavel e funcional

[pending] Atualizar STATUS.yaml
  |-- [pending] execucao.frontend = done
  +-- [pending] Verificar consistencia dos campos
```

### Regras de Execucao da Todo List

1. **COPIAR** o template acima ANTES de qualquer acao
2. Atualizar status em tempo real ([pending] → [in_progress] → [completed])
3. **NUNCA** pular etapas
4. **PARAR** em caso de falha (401/403/build error)
5. Seguir ordem sequencial
6. Somente declarar CONCLUIDO apos **TODOS** os itens completed

---

## WORKFLOW DE BRANCHES (OBRIGATORIO)

Antes de iniciar qualquer implementacao:

```bash
# 1. Atualizar dev
git checkout dev
git pull origin dev

# 2. Criar branch a partir de dev
git checkout -b feature/RFXXX-frontend
```

Ao concluir a implementacao:

```bash
# 3. Commit e merge em dev
git add .
git commit -m "feat(RFXXX): implementacao frontend"
git checkout dev
git pull origin dev
git merge feature/RFXXX-frontend
git push origin dev
```

> Referencia completa: `docs/devops/BRANCH-WORKFLOW.md`

---

## OBJETIVO

Implementar o frontend da **funcionalidade alvo**
conforme o **backend já implementado**.

Documentos externos (RF/UC/MD) são utilizados
**apenas como referência conceitual**.

A **fonte da verdade técnica** é:
- O backend existente
- Os documentos em `/docs`

---

## ESCOPO FUNCIONAL

Inclui exclusivamente:

- Componentes de UI da funcionalidade alvo
- Services de acesso à API correspondente
- Rotas e bindings necessários
- Integração obrigatória com i18n (Transloco)

É **EXPRESSAMENTE PROIBIDO**:

- Usar chaves i18n não registradas
- Depender de fallback silencioso do Transloco
- Considerar a funcionalidade pronta com warnings no console

Qualquer warning de tradução ausente:
- **INVALIDA a entrega**
- Deve ser tratado como **erro funcional**

---

## ZONAS PERMITIDAS

- `D:\IC2\frontend\icontrolit-app/src/app/modules/**`
- `D:\IC2\frontend\icontrolit-app/src/app/core/services/**` (somente se necessário)
- `D:\IC2\frontend\icontrolit-app/src/app/core/models/**` (somente se necessário)

---

## ZONAS PROIBIDAS

- `/docs/**`
- Layout base e shell principal
- Core compartilhado existente (salvo autorização explícita)
- Configurações globais do Angular
- Arquitetura base do frontend

---

## REGRAS GERAIS (INVIOLÁVEIS)

- Seguir estritamente:
  - `ARCHITECTURE.md`
  - `CONVENTIONS.md`
  - `CLAUDE.md`
- NÃO inferir requisitos
- Usar **Standalone Components**
- Usar **Transloco obrigatoriamente**
- NÃO criar serviços genéricos reutilizáveis
- NÃO alterar estrutura global de rotas
- Se precisar sair do escopo: **PARAR e AVISAR**
- O layout deve seguir **EXATAMENTE** os padrões já existentes em:
  - `/management/users`
  - `/management/roles`
  - `/hierarquia/centros-custo`
- O frontend **não é apenas UI**, é integração com todo o ecossistema

---

## GOVERNANÇA DE ACESSO (OBRIGATÓRIA)

Antes de iniciar qualquer implementação, o agente DEVE declarar explicitamente:

- Quais permissões a funcionalidade exige
- Qual perfil deve ter acesso (mínimo: `developer`)

Essas permissões são **pré-condições de funcionamento**
e NÃO simples configurações opcionais.

---

## PROVA DE ACESSO (OBRIGATÓRIA)

Antes de iniciar QUALQUER implementação de frontend,
o agente DEVE comprovar que o backend está acessível
para o perfil esperado.

O agente DEVE:

- Autenticar como usuário `developer`
- Executar manualmente (ou via teste automatizado)
  ao menos UMA chamada real da funcionalidade
- Confirmar retorno HTTP **200**

Se o retorno for:
- 401
- 403
- 404 inesperado

O agente DEVE:
- **PARAR imediatamente**
- Corrigir seeds, permissões ou registros necessários
- Reexecutar a verificação
- Somente prosseguir após confirmação de acesso real

É **PROIBIDO**:
- Assumir acesso com base apenas em código ou registry
- Prosseguir sem validação runtime

---

## DEPENDENCIAS FUNCIONAIS (OBRIGATORIO)

Antes de executar os testes E2E, o agente DEVE validar
todas as dependencias funcionais da entidade.

### Identificar Dependencias

Analisar MD-RFXXX.md e identificar:
- Foreign Keys (FKs) que apontam para outras entidades
- Dropdowns que carregam dados de outras tabelas
- Rotas relacionadas

### Validar Dependencias

Para CADA dependencia identificada:
1. Navegar para a rota da dependencia
2. Verificar carregamento (HTTP 200)
3. Tentar criar um registro basico
4. Se FALHAR: registrar erro

### Comportamento em Caso de Falha

Se QUALQUER dependencia falhar, o agente DEVE analisar a causa:

**Erro no FRONTEND do RF atual:**
- O agente DEVE corrigir o problema
- Re-executar os testes Playwright
- Repetir ate que todos os testes passem
- NAO parar para aguardar usuario

**Erro em OUTRO RF ou no BACKEND:**
- **PARAR** a execucao do RF atual
- Criar arquivo `RELATORIO-ERROS-RFXXX.md` na pasta do RF
- Listar todas as dependencias com erro
- Sugerir contratos de manutencao para os RFs afetados
- **NAO** marcar RF como concluido
- **AGUARDAR** usuario resolver dependencias externas

### Criterio de Continuacao

O agente pode prosseguir quando:
- TODAS as dependencias foram validadas com sucesso
- OU todos os erros de frontend do RF atual foram corrigidos

### Setup E2E Obrigatorio

Os testes E2E DEVEM criar dados na ordem correta:
1. Primeiro: entidades mais basicas (Empresa)
2. Depois: entidades intermediarias (Filial, Centro de Custo)
3. Por fim: entidade do RF atual (Departamento)

Exemplo para RF024 (Departamentos):
```
ordem_setup:
  1. Empresa
  2. Filial
  3. Centro de Custo
  4. Departamento (testar CRUD completo)
  5. Departamento FINAL (evidencia - NAO excluir)
```

### Fluxo de Teste Correto

```
1. Setup: Criar dependencias (Empresa, Filial, CC)
2. Teste: Criar registro → Validar
3. Teste: Editar registro → Validar
4. Teste: Excluir registro → Validar
5. FINAL: Criar registro de evidencia
   - Nome: "[EVIDENCIA E2E] RF024 - 2024-12-24 14:30"
   - NAO excluir este registro
6. Fim dos testes
```

---

## ALTERAÇÕES PERMITIDAS NO BACKEND (LIMITADAS)

Permitidas **somente** para viabilizar acesso e testes:

- Registro da funcionalidade na **Central de Módulos**
- Associação de permissões existentes a perfis existentes
- Ajustes mínimos e estritamente necessários para habilitar acesso

Caso o registro na Central de Módulos:
- Não exista
- Ou exija alteração não permitida

O agente DEVE:
- **PARAR**
- **REPORTAR explicitamente**
- **AGUARDAR decisão**

Essas alterações **NÃO** são consideradas:
- Mudança de arquitetura
- Criação de escopo novo
- Evolução funcional

---

## SEEDS FUNCIONAIS (OBRIGATÓRIO)

Para que a funcionalidade seja considerada testável e concluída,
o agente DEVE garantir a existência dos dados mínimos necessários.

Inclui, quando aplicável:

- Entidades dependentes (Cliente, Empresa, Perfis)
- Permissões necessárias
- Associação das permissões ao perfil `developer`
- Usuário de teste funcional

### REGRAS DE SEED

- Criar SOMENTE se não existirem
- Seeds idempotentes
- NÃO alterar dados produtivos
- Seeds existem apenas para habilitar execução e testes

### LOCAL DE SEED

- `DataInitializer`
- Seeders existentes
- Mecanismo de inicialização já adotado pelo projeto

### É PROIBIDO

- Criar seeds em handlers
- Criar seeds escondidos em testes
- Criar seeds temporários sem controle

---

## VERIFICAÇÃO DE CONSISTÊNCIA NO STARTUP (CRÍTICO)

Em ambientes **DEV/TEST**, o sistema DEVE validar no startup:

- Existência das permissões da funcionalidade
- Associação ao perfil `developer`
- Existência do registro na Central de Módulos

Se qualquer item estiver ausente:

- Logar erro claro
- NÃO permitir funcionamento silencioso
- Alertar explicitamente

---

## TESTES E2E (PLAYWRIGHT)

Os testes E2E são **obrigatórios**.

### Regras

- Qualquer **401 ou 403** deve falhar o teste
- Respostas **404, 500 ou vazias inesperadas** devem falhar
- Testes devem validar:
  - Login como `developer`
  - Acesso via menu
  - Carregamento da listagem com dados reais
  - Execução do fluxo principal (caminho feliz)

### Responsividade (Validação Funcional)

- Validar acesso funcional em diferentes viewports
- NÃO exigir identidade visual absoluta entre desktop e mobile

### Registro de Evidencia (OBRIGATORIO)

Ao final dos testes E2E, o agente DEVE:

1. Executar todos os testes de CRUD (criar, editar, excluir)
2. Validar que todos passaram
3. **Criar UM registro final** que permanece no sistema
4. **NAO excluir** este registro final

Este registro serve como **evidencia** de que:
- O fluxo completo foi executado
- A funcionalidade esta operacional
- O teste foi realizado com sucesso

Nomenclatura sugerida para o registro de evidencia:
- Nome: `[EVIDENCIA E2E] RFXXX - YYYY-MM-DD HH:MM`
- Ou campo identificador claro que indique ser um registro de teste

---

## FASE 6.5: DATA-TEST ATTRIBUTES OBRIGATÓRIOS (NOVO - BLOQUEANTE)

**Este passo é OBRIGATÓRIO para alinhamento completo com testes E2E. Sem ele, frontend está INCOMPLETO.**

Esta fase complementa e reforça as regras de data-test já estabelecidas, garantindo **sincronização completa** com UC-RFXXX.yaml.

---

### 6.5.1: Implementar Data-test em TODOS os Elementos

**O agente DEVE adicionar `data-test` em:**

#### 1. Botões de Ação

**Padrão obrigatório:** `RFXXX-[acao]-[entidade]`

```html
<!-- Botões de CRUD -->
<button data-test="RF006-criar-cliente">Novo Cliente</button>
<button data-test="RF006-editar-cliente">Editar</button>
<button data-test="RF006-excluir-cliente">Excluir</button>
<button data-test="RF006-salvar-cliente">Salvar</button>
<button data-test="RF006-cancelar-cliente">Cancelar</button>
```

**Critério de aceite:**
- ✅ TODOS os botões de ação (Criar, Editar, Excluir, Salvar, Cancelar) possuem data-test
- ✅ Nomenclatura segue padrão `RFXXX-[acao]-[entidade]`

---

#### 2. Campos de Formulário

**Padrão obrigatório:** `RFXXX-input-[nomecampo]`

```html
<!-- Inputs de texto -->
<input data-test="RF006-input-razaosocial"
       formControlName="razaoSocial"
       type="text" />

<input data-test="RF006-input-cnpj"
       formControlName="cnpj"
       type="text" />

<!-- Selects/Dropdowns -->
<p-dropdown data-test="RF006-input-status"
            formControlName="status"></p-dropdown>

<!-- Textareas -->
<textarea data-test="RF006-input-observacoes"
          formControlName="observacoes"></textarea>

<!-- Checkboxes -->
<p-checkbox data-test="RF006-input-ativo"
            formControlName="ativo"></p-checkbox>

<!-- Radio buttons -->
<p-radioButton data-test="RF006-input-tipo-pf"
               value="PF"></p-radioButton>
```

**Critério de aceite:**
- ✅ TODOS os campos de formulário (input, select, textarea, checkbox, radio) possuem data-test
- ✅ Nomenclatura segue padrão `RFXXX-input-[nomecampo]`

---

#### 3. Mensagens de Erro de Validação

**Padrão obrigatório:** `RFXXX-input-[nomecampo]-error`

```html
<!-- Mensagens de erro do Angular Material -->
<mat-error data-test="RF006-input-razaosocial-error">
  Razão Social é obrigatória
</mat-error>

<mat-error data-test="RF006-input-cnpj-error">
  CNPJ inválido
</mat-error>

<!-- Mensagens de erro do PrimeNG -->
<small class="p-error" data-test="RF006-input-email-error">
  E-mail inválido
</small>
```

**Critério de aceite:**
- ✅ TODAS as mensagens de erro de validação possuem data-test
- ✅ Nomenclatura segue padrão `RFXXX-input-[nomecampo]-error`

---

#### 4. Tabelas/Listas

**Padrão obrigatório:**
- Container: `[entidade]-list`
- Linhas: `[entidade]-row`
- Ações de linha: `RFXXX-[acao]-[entidade]`

```html
<!-- Tabela/Grid -->
<p-table data-test="clientes-list" [value]="clientes">
  <!-- Cabeçalho -->
  <ng-template pTemplate="header">
    <tr>
      <th data-test="cliente-col-razaosocial">Razão Social</th>
      <th data-test="cliente-col-cnpj">CNPJ</th>
      <th data-test="cliente-col-acoes">Ações</th>
    </tr>
  </ng-template>

  <!-- Corpo -->
  <ng-template pTemplate="body" let-cliente>
    <tr data-test="cliente-row">
      <td>{{ cliente.razaoSocial }}</td>
      <td>{{ cliente.cnpj }}</td>
      <td>
        <button data-test="RF006-editar-cliente"
                (click)="editar(cliente)">Editar</button>
        <button data-test="RF006-excluir-cliente"
                (click)="excluir(cliente)">Excluir</button>
      </td>
    </tr>
  </ng-template>
</p-table>
```

**Critério de aceite:**
- ✅ Container da tabela possui data-test `[entidade]-list`
- ✅ Linhas da tabela possuem data-test `[entidade]-row`
- ✅ Colunas possuem data-test `[entidade]-col-[nome]`
- ✅ Ações de linha seguem padrão `RFXXX-[acao]-[entidade]`

---

#### 5. Estados de UI

**Padrão fixo (sem prefixo RF):**
- Loading: `loading-spinner`
- Vazio: `empty-state`
- Erro: `error-message`

```html
<!-- Estado de Loading -->
<p-progressSpinner data-test="loading-spinner"
                   *ngIf="loading"></p-progressSpinner>

<!-- Estado Vazio -->
<div data-test="empty-state" *ngIf="!loading && clientes.length === 0">
  <p>Nenhum cliente encontrado</p>
  <button data-test="RF006-criar-cliente">Adicionar Primeiro Cliente</button>
</div>

<!-- Estado de Erro -->
<div data-test="error-message" *ngIf="error">
  <p>Erro ao carregar clientes: {{ error }}</p>
  <button data-test="btn-retry">Tentar Novamente</button>
</div>
```

**Critério de aceite:**
- ✅ Estado loading possui data-test `loading-spinner`
- ✅ Estado vazio possui data-test `empty-state`
- ✅ Estado erro possui data-test `error-message`

---

#### 6. Diálogos/Modais

**Padrão obrigatório:**
- Container: `dialog-[tipo]`
- Botões: `btn-[acao]-dialog`

```html
<!-- Modal de Confirmação -->
<p-dialog data-test="dialog-confirmacao"
          [(visible)]="showConfirmDialog">
  <p>Tem certeza que deseja excluir este cliente?</p>
  <p-footer>
    <button data-test="btn-confirmar-dialog"
            (click)="confirmar()">Confirmar</button>
    <button data-test="btn-cancelar-dialog"
            (click)="cancelar()">Cancelar</button>
  </p-footer>
</p-dialog>

<!-- Modal de Sucesso -->
<p-dialog data-test="dialog-sucesso"
          [(visible)]="showSuccessDialog">
  <p>Cliente salvo com sucesso!</p>
  <p-footer>
    <button data-test="btn-fechar-dialog"
            (click)="fechar()">Fechar</button>
  </p-footer>
</p-dialog>
```

**Critério de aceite:**
- ✅ Diálogos possuem data-test `dialog-[tipo]`
- ✅ Botões de diálogo seguem padrão `btn-[acao]-dialog`

---

### 6.5.2: Validar Nomenclatura com UC-RFXXX.yaml

**O agente DEVE verificar sincronização com UC:**

1. **Comparar data-test do frontend com UC-RFXXX.yaml:**
   - Ler `UC-RFXXX.yaml` → seções `passos[]`, `tabela`, `formulario`, `estados_ui`
   - Extrair TODOS os `data_test` especificados
   - Comparar com data-test implementados no HTML

2. **Verificar consistência:**
   ```yaml
   # UC-RFXXX.yaml especifica:
   passos:
     - numero: 1
       elemento:
         data_test: "RF006-criar-cliente"

   formulario:
     campos:
       - data_test: "RF006-input-razaosocial"
   ```

   ```html
   <!-- Frontend DEVE ter EXATAMENTE: -->
   <button data-test="RF006-criar-cliente">Novo Cliente</button>
   <input data-test="RF006-input-razaosocial" />
   ```

**SE nomenclatura NÃO bate:**
- ❌ BLOQUEIO: Corrigir nomenclatura para corresponder ao UC
- ❌ Não prosseguir para testes E2E

**Critério de aceite:**
- ✅ 100% dos data-test do UC estão implementados no frontend
- ✅ Nomenclatura é IDÊNTICA entre UC e frontend

---

### 6.5.3: Executar Auditoria de Data-test

**O agente DEVE executar auditoria automatizada:**

```bash
# Executar script de auditoria
npm run audit-data-test RFXXX

# OU
ts-node tools/audit-data-test.ts RFXXX
```

**Validar resultado da auditoria:**
- ✅ TODOS os data-test de UC-RFXXX.yaml estão presentes no HTML
- ✅ Nenhum data-test está ausente
- ✅ Nomenclatura é consistente

**SE auditoria FALHAR:**
- ❌ BLOQUEIO: Adicionar data-test ausentes
- ❌ BLOQUEIO: Corrigir nomenclatura inconsistente
- ❌ Re-executar auditoria até aprovação

**Relatório esperado:**

```
============================================================
AUDITORIA DE DATA-TEST ATTRIBUTES - RF006
============================================================

Data-test esperados (UC): 18
Data-test encontrados (HTML): 18
Taxa de cobertura: 100.0%

✅ Data-test ENCONTRADOS (18):
  ✓ RF006-criar-cliente
  ✓ RF006-input-razaosocial
  ✓ RF006-input-cnpj
  ✓ RF006-salvar-cliente
  ✓ loading-spinner
  ✓ empty-state
  ✓ error-message
  [...]

❌ Data-test AUSENTES (0):
  (nenhum)

============================================================
✅ AUDITORIA PASSOU
Todos os data-test esperados estão presentes no HTML
============================================================
```

**Critério de aceite:**
- ✅ Exit code 0 (auditoria passou)
- ✅ 0 data-test ausentes
- ✅ Cobertura: 100%

---

### 6.5.4: Documentar Data-test Implementados

**O agente DEVE atualizar STATUS.yaml:**

```yaml
desenvolvimento:
  frontend:
    status: done

    data_test_attributes:
      implementados: 18
      esperados_uc: 18
      cobertura: 100
      auditoria: "✅ PASS (npm run audit-data-test RF006)"
      data_auditoria: "2026-01-09"
      nomenclatura_consistente: true
      sincronizado_uc: true
```

**Critério de aceite:**
- ✅ STATUS.yaml atualizado com métricas de data-test
- ✅ Auditoria documentada como PASS
- ✅ Cobertura: 100%

---

### 6.5.5: Validação Final de Bloqueio

**Antes de prosseguir para testes E2E, o agente DEVE confirmar:**

- ✅ TODOS os elementos interativos possuem data-test
- ✅ Nomenclatura é 100% consistente com UC-RFXXX.yaml
- ✅ Auditoria passou (exit code 0)
- ✅ Cobertura: 100% dos data-test de UC estão no HTML
- ✅ Estados de UI (loading, vazio, erro) possuem data-test
- ✅ Tabelas/listas possuem data-test
- ✅ Formulários possuem data-test em campos e erros
- ✅ Diálogos possuem data-test

**SE qualquer verificação FALHAR:**
- ❌ Frontend NÃO está pronto para testes E2E
- ❌ BLOQUEIO: Não executar testes E2E
- ❌ BLOQUEIO: Não marcar frontend como done
- ❌ Corrigir TODOS os problemas identificados
- ❌ Re-auditar até aprovação

---

**RESUMO DA FASE 6.5:**

Esta fase é **CRÍTICA** para alinhamento com testes E2E. Sem ela:
- ❌ Testes E2E falharão 100% por seletores não encontrados
- ❌ MT (Massa de Teste) não conseguirá executar ações
- ❌ TC (Casos de Teste) falhará por elementos ausentes
- ❌ Taxa de aprovação inicial será 0%

**Com esta fase:**
- ✅ Frontend tem data-test 100% sincronizados com UC
- ✅ Testes E2E encontram TODOS os elementos
- ✅ Taxa de aprovação inicial será 80-90%
- ✅ Zero retrabalho por seletores ausentes

**Resultado esperado:**
- ✅ Frontend pronto para testes E2E
- ✅ Rastreabilidade: UC → Frontend → Testes
- ✅ Zero gaps de alinhamento

---

## FASE 6.6: MATERIAL DIALOG BACKDROP CLEANUP (NOVO - BLOQUEANTE)

**🆕 ADICIONADO:** 2026-01-11 (Resolve 17% dos problemas identificados no RF006)

**Este passo é OBRIGATÓRIO para operações assíncronas com dialogs. Sem ele, testes E2E falharão por backdrop persistente.**

**Contexto do Problema:**

Durante testes do RF006, identificou-se que após operações assíncronas (consulta ReceitaWS, chamadas de API), o backdrop do Material Dialog **permanece visível** mesmo após o dialog ser fechado. Isso resulta em:
- ❌ Backdrop intercepta cliques subsequentes
- ❌ Testes E2E falham com timeout (elementos não clicáveis)
- ❌ Usuário não consegue interagir com a UI
- ❌ 17% de falhas nos testes E2E do RF006

**Causa Raiz:**

O Material Dialog usa `cdk-overlay-backdrop` para escurecer a tela. Quando operações assíncronas ocorrem:
1. Dialog abre → backdrop aparece
2. Operação assíncrona executa (ex: HTTP request)
3. Dialog fecha **antes** da animação de saída completar
4. Backdrop **permanece no DOM** interceptando cliques

---

### 6.6.1: Identificar Operações Assíncronas com Dialog

**O agente DEVE identificar situações onde backdrop pode persistir:**

#### Cenários Críticos (OBRIGATÓRIO limpar backdrop):

**a) Consultas a APIs Externas com Dialog de Loading**
```typescript
// Cenário: Consultar ReceitaWS com loading dialog
const dialogRef = this.dialog.open(LoadingDialogComponent, {
  disableClose: true,
  data: { message: 'Consultando CNPJ...' }
});

try {
  const dados = await this.receitaWsService.consultar(cnpj);
  // ⚠️ PROBLEMA: Dialog fecha mas backdrop pode persistir
  dialogRef.close();
  // ✅ SOLUÇÃO: Aguardar fechamento completo
} catch (error) {
  dialogRef.close();
}
```

**b) Operações CRUD Assíncronas com Dialog de Confirmação**
```typescript
// Cenário: Confirmar exclusão com loading
const confirmRef = this.dialog.open(ConfirmDialogComponent, {
  data: { message: 'Confirmar exclusão?' }
});

confirmRef.afterClosed().subscribe(async (confirmed) => {
  if (confirmed) {
    const loadingRef = this.dialog.open(LoadingDialogComponent);
    await this.service.delete(id);
    // ⚠️ PROBLEMA: Loading dialog fecha mas backdrop persiste
    loadingRef.close();
    // ✅ SOLUÇÃO: Aguardar fechamento completo
  }
});
```

**c) Dialogs Aninhados (Dialog dentro de Dialog)**
```typescript
// Cenário: Dialog de edição abre dialog de confirmação
const editRef = this.dialog.open(EditDialogComponent);

editRef.componentInstance.onConfirm.subscribe(() => {
  const confirmRef = this.dialog.open(ConfirmDialogComponent);
  // ⚠️ PROBLEMA: Múltiplos backdrops podem persistir
});
```

**d) Formulários em Dialog com Validação Assíncrona**
```typescript
// Cenário: Validar CPF/CNPJ com API externa antes de salvar
const dialogRef = this.dialog.open(FormDialogComponent);

dialogRef.componentInstance.form.valueChanges
  .pipe(debounceTime(500))
  .subscribe(async (value) => {
    const valid = await this.validationService.validate(value.cpf);
    // ⚠️ PROBLEMA: Validação assíncrona pode deixar backdrop
  });
```

**Critério de aceite:**
- ✅ TODAS as operações assíncronas com dialog identificadas
- ✅ Cenários de backdrop persistente mapeados

---

### 6.6.2: Implementar Cleanup de Backdrop (PADRÃO OBRIGATÓRIO)

**O agente DEVE aplicar o padrão de cleanup em TODOS os cenários identificados:**

#### Padrão #1: Aguardar afterClosed() Completo

**Para operações simples (1 dialog):**

```typescript
// ❌ INCORRETO: Fechar sem aguardar
const dialogRef = this.dialog.open(LoadingDialogComponent);
await this.api.consultar();
dialogRef.close();
// Backdrop pode persistir aqui ⚠️

// ✅ CORRETO: Aguardar fechamento completo
const dialogRef = this.dialog.open(LoadingDialogComponent);
await this.api.consultar();
dialogRef.close();
await firstValueFrom(dialogRef.afterClosed());  // ✅ Garantia de fechamento
```

#### Padrão #2: Usar Helper waitForDialogToClosed (E2E)

**Para testes E2E (Playwright):**

```typescript
// ❌ INCORRETO: Clicar imediatamente após fechar dialog
await page.click('[data-test="RF006-dialog-cancelar"]');
await page.click('[data-test="RF006-criar-cliente"]');  // ⚠️ Falha: backdrop intercepta

// ✅ CORRETO: Aguardar backdrop ser removido
import { waitForDialogToClosed } from '../helpers';

await page.click('[data-test="RF006-dialog-cancelar"]');
await waitForDialogToClosed(page);  // ✅ Aguarda backdrop desaparecer
await page.click('[data-test="RF006-criar-cliente"]');  // ✅ Clique funciona
```

**Implementação do helper** (já existe em `e2e/helpers/dialog-helpers.ts`):

```typescript
export async function waitForDialogToClosed(
  page: Page,
  timeout: number = 15000
): Promise<void> {
  try {
    // Aguarda que backdrop seja REMOVIDO do DOM
    await page.waitForSelector('.cdk-overlay-backdrop', {
      state: 'detached',  // ✅ Garante que foi removido
      timeout
    });

    // Aguarda adicional para animação CSS finalizar
    await page.waitForTimeout(500);
  } catch (error) {
    throw new Error(
      `Dialog backdrop não foi removido dentro de ${timeout}ms. ` +
      `Verifique se dialog foi fechado corretamente.`
    );
  }
}
```

#### Padrão #3: Múltiplos Dialogs (Aninhados)

**Para dialogs aninhados:**

```typescript
// ✅ CORRETO: Aguardar fechamento de CADA dialog
const editRef = this.dialog.open(EditDialogComponent);

editRef.componentInstance.onConfirm.subscribe(async () => {
  const confirmRef = this.dialog.open(ConfirmDialogComponent);
  const confirmed = await firstValueFrom(confirmRef.afterClosed());

  if (confirmed) {
    const loadingRef = this.dialog.open(LoadingDialogComponent);
    await this.api.save();
    loadingRef.close();
    await firstValueFrom(loadingRef.afterClosed());  // ✅ Aguarda loading fechar
  }

  editRef.close();
  await firstValueFrom(editRef.afterClosed());  // ✅ Aguarda edit fechar
});
```

#### Padrão #4: Operações Assíncronas Longas

**Para operações que demoram (>5s):**

```typescript
// ✅ CORRETO: Dialog persiste durante operação
const dialogRef = this.dialog.open(LoadingDialogComponent, {
  disableClose: true,  // ✅ Impede fechamento acidental
  data: { message: 'Processando...' }
});

try {
  const result = await this.longRunningService.process();

  dialogRef.close();
  await firstValueFrom(dialogRef.afterClosed());  // ✅ Aguarda fechamento

  // Agora é seguro mostrar resultado
  this.showSuccess(result);
} catch (error) {
  dialogRef.close();
  await firstValueFrom(dialogRef.afterClosed());  // ✅ Aguarda mesmo em erro

  this.showError(error);
}
```

**Critério de aceite:**
- ✅ TODOS os cenários aplicam padrão de cleanup
- ✅ Código usa `firstValueFrom(dialogRef.afterClosed())`
- ✅ Testes E2E usam `waitForDialogToClosed(page)`

---

### 6.6.3: Atualizar Testes E2E com Helpers

**O agente DEVE atualizar TODOS os testes E2E que interagem com dialogs:**

#### Atualização de Imports

```typescript
// ✅ CORRETO: Importar helpers no início do arquivo
import { test, expect } from '@playwright/test';
import {
  waitForDialogToClosed,
  waitForDialogToOpen,
  waitForNoBackdrop
} from '../helpers';
```

#### Atualização de Testes de Criação

```typescript
test('TC-E2E: Criar Cliente com Consulta CNPJ', async ({ page }) => {
  // 1. Clicar em "Novo Cliente"
  await page.click('[data-test="RF006-criar-cliente"]');
  await waitForDialogToOpen(page, 'dialog-criar-cliente');  // ✅ Aguarda abertura

  // 2. Preencher CNPJ e consultar ReceitaWS
  await page.fill('[data-test="RF006-input-cnpj"]', '00.000.000/0001-91');
  await page.click('[data-test="RF006-btn-consultar-cnpj"]');

  // ⚠️ CRÍTICO: Aguardar loading dialog fechar ANTES de continuar
  await waitForDialogToClosed(page);  // ✅ Aguarda backdrop desaparecer

  // 3. Validar dados carregados
  await expect(page.locator('[data-test="RF006-input-razaosocial"]'))
    .not.toHaveValue('');

  // 4. Salvar cliente
  await page.click('[data-test="RF006-salvar-cliente"]');
  await waitForDialogToClosed(page);  // ✅ Aguarda dialog de sucesso fechar

  // 5. Validar redirecionamento
  await page.waitForURL('**/management/clientes', { timeout: 10000 });
});
```

#### Atualização de Testes de Exclusão

```typescript
test('TC-E2E: Excluir Cliente com Confirmação', async ({ page }) => {
  // 1. Clicar em "Excluir"
  await page.click('[data-test="RF006-excluir-cliente"]');
  await waitForDialogToOpen(page, 'dialog-confirmacao');  // ✅ Aguarda dialog abrir

  // 2. Confirmar exclusão
  await page.click('[data-test="btn-confirmar-dialog"]');
  await waitForDialogToClosed(page);  // ✅ Aguarda dialog fechar

  // 3. Validar que registro foi excluído
  await expect(page.locator('[data-test="cliente-row"]')).not.toBeVisible();
});
```

#### Atualização de Testes com Múltiplos Dialogs

```typescript
test('TC-E2E: Editar e Cancelar com Confirmação', async ({ page }) => {
  // 1. Abrir dialog de edição
  await page.click('[data-test="RF006-editar-cliente"]');
  await waitForDialogToOpen(page, 'dialog-editar-cliente');

  // 2. Modificar campo
  await page.fill('[data-test="RF006-input-nomeFantasia"]', 'NOME EDITADO');

  // 3. Clicar em cancelar (abre dialog de confirmação)
  await page.click('[data-test="btn-cancelar-dialog"]');
  await waitForDialogToOpen(page, 'dialog-confirmacao-cancelar');

  // 4. Confirmar cancelamento
  await page.click('[data-test="btn-confirmar-dialog"]');

  // ⚠️ CRÍTICO: Aguardar AMBOS os dialogs fecharem
  await waitForNoBackdrop(page);  // ✅ Garante ZERO backdrops

  // 5. Validar retorno à listagem
  await page.waitForURL('**/management/clientes');
});
```

**Critério de aceite:**
- ✅ TODOS os testes E2E usam helpers de dialog
- ✅ Nenhum teste clica em elemento logo após fechar dialog sem aguardar
- ✅ Testes com múltiplos dialogs usam `waitForNoBackdrop()`

---

### 6.6.4: Validar Comportamento em Produção

**O agente DEVE validar que cleanup não quebra comportamento em produção:**

#### Checklist de Validação:

**a) Dialog Fecha Corretamente**
- [ ] Dialog desaparece visualmente
- [ ] Backdrop é removido do DOM
- [ ] Animação de saída completa
- [ ] Nenhum overlay residual visível

**b) Usuário Pode Interagir Após Dialog**
- [ ] Cliques funcionam imediatamente
- [ ] Campos são editáveis
- [ ] Navegação funciona
- [ ] Nenhum delay perceptível

**c) Múltiplos Dialogs Funcionam**
- [ ] Dialog aninhado abre corretamente
- [ ] Backdrop correto para cada dialog
- [ ] Fechar aninhado não fecha pai
- [ ] Fechar pai remove TODOS os backdrops

**d) Operações Assíncronas Não Quebram**
- [ ] Loading dialog fecha após operação
- [ ] Erro não deixa backdrop preso
- [ ] Timeout não deixa backdrop preso
- [ ] Cancelamento limpa backdrop

**Validação Manual (Developer Console):**

```javascript
// Durante teste manual, verificar no console:
document.querySelectorAll('.cdk-overlay-backdrop').length
// Esperado: 0 (nenhum backdrop após fechar dialog)
// Se > 0: backdrop preso (problema!)
```

**Critério de aceite:**
- ✅ Dialog fecha visualmente
- ✅ Zero backdrops após fechamento (validado no console)
- ✅ Usuário pode interagir imediatamente
- ✅ Múltiplos dialogs funcionam corretamente

---

### 6.6.5: Documentar Padrão no Código

**O agente DEVE adicionar comentários nos componentes:**

```typescript
/**
 * PADRÃO OBRIGATÓRIO: Cleanup de Dialog Backdrop
 *
 * Ao usar MatDialog com operações assíncronas, SEMPRE:
 * 1. Fechar dialog: dialogRef.close()
 * 2. Aguardar fechamento: await firstValueFrom(dialogRef.afterClosed())
 *
 * Referência: D:\IC2_Governanca\governanca\contracts\desenvolvimento\execucao\frontend-criacao.md
 * Seção: FASE 6.6 - Material Dialog Backdrop Cleanup
 *
 * @see CONTRATO-TESTES-E2E-STATEFUL.md (seção 3 - Dialog Helpers)
 */
async consultarCNPJ(cnpj: string): Promise<void> {
  const dialogRef = this.dialog.open(LoadingDialogComponent, {
    disableClose: true,
    data: { message: 'Consultando CNPJ...' }
  });

  try {
    const dados = await this.receitaWsService.consultar(cnpj);
    this.form.patchValue(dados);

    dialogRef.close();
    await firstValueFrom(dialogRef.afterClosed());  // ✅ Cleanup obrigatório
  } catch (error) {
    dialogRef.close();
    await firstValueFrom(dialogRef.afterClosed());  // ✅ Cleanup mesmo em erro

    this.showError(error);
  }
}
```

**Critério de aceite:**
- ✅ Componentes com dialog possuem comentários de padrão
- ✅ Referência ao contrato documentada
- ✅ Exemplo de uso correto no código

---

### 6.6.6: Atualizar STATUS.yaml

**O agente DEVE documentar aplicação do padrão:**

```yaml
desenvolvimento:
  frontend:
    status: done

    dialog_backdrop_cleanup:
      aplicado: true
      cenarios_cobertos: 5
      helpers_usados:
        - waitForDialogToClosed
        - waitForDialogToOpen
        - waitForNoBackdrop
      testes_e2e_atualizados: true
      validacao_manual: aprovada
      data_implementacao: "2026-01-11"
      referencia_contrato: "FASE 6.6 - frontend-criacao.md"
```

**Critério de aceite:**
- ✅ STATUS.yaml documentado
- ✅ Cenários cobertos listados
- ✅ Helpers documentados

---

### 6.6.7: Validação Final de Bloqueio

**Antes de marcar frontend como done, o agente DEVE confirmar:**

- ✅ TODAS as operações assíncronas com dialog aplicam cleanup
- ✅ TODOS os testes E2E usam helpers de dialog
- ✅ Zero backdrops persistentes após operações (validado manualmente)
- ✅ Código possui comentários de padrão
- ✅ STATUS.yaml documentado
- ✅ Validação manual passou

**SE qualquer verificação FALHAR:**
- ❌ Frontend NÃO está pronto
- ❌ BLOQUEIO: Corrigir TODOS os problemas
- ❌ Re-validar até aprovação

---

**RESUMO DA FASE 6.6:**

Esta fase resolve **17% dos problemas do RF006** causados por backdrop persistente.

**Sem esta fase:**
- ❌ Backdrop intercepta cliques após operações assíncronas
- ❌ Testes E2E falham com timeout
- ❌ Usuário não consegue interagir
- ❌ 17% de taxa de falha (3/18 testes do RF006)

**Com esta fase:**
- ✅ Backdrop sempre limpo após operações
- ✅ Testes E2E passam sem timeouts
- ✅ Usuário interage normalmente
- ✅ Zero falhas por backdrop persistente

**Resultado esperado:**
- ✅ Taxa de falha reduzida de 26% → 9% (apenas formulários multi-aba restantes)
- ✅ Padrão documentado e reutilizável
- ✅ Código robusto e manutenível

**Referências:**
- Helper implementado: `D:\IC2\frontend\icontrolit-app\e2e\helpers\dialog-helpers.ts`
- Contrato stateful: `D:\IC2_Governanca\governanca\contracts\testes\CONTRATO-TESTES-E2E-STATEFUL.md`
- Problema identificado: RF006 execução #7-#9 (17% de falhas)

---

## FASE 6.7: VALIDATORS ANGULAR OBRIGATÓRIOS (NOVO - BLOQUEANTE)

**Versão:** 1.0
**Data de Criação:** 2026-01-11
**Origem:** Análise de falhas RF006 (execução #9) - GAP 1

### CONTEXTO

**Problema Identificado:**
Durante testes E2E do RF006, **3 falhas (21% das falhas E2E)** foram causadas por validators Angular ausentes:

| Teste | Falha | Causa Raiz |
|-------|-------|------------|
| FA-UC01-001 | mat-error não aparece para CNPJ inválido | Validators.pattern() ausente |
| FA-UC01-002 | Botão Salvar não desabilita | form.invalid não vinculado |
| FA-UC01-003 | Aba "Contato" não existe | Campo email sem Validators.email |

**Objetivo:**
Garantir que **TODOS** os formulários implementem validators Angular obrigatórios, mat-error messages, e comportamento de validação.

**Bloqueio:**
- ❌ Se validators obrigatórios estiverem ausentes → Frontend REPROVADO
- ❌ Se mat-error messages estiverem ausentes → Frontend REPROVADO
- ❌ Se botões não desabilitarem em form.invalid → Frontend REPROVADO

---

### PASSO 6.7.1: Identificar Campos com Validação

**O agente DEVE:**

1. **Ler UC-RFXXX.yaml:**
   - Localizar seção `formulario.campos`
   - Identificar todos os campos com `obrigatorio: true`
   - Identificar todos os campos com `validacoes` especificadas

2. **Mapear validações obrigatórias:**

**Exemplo UC-RF006.yaml:**
```yaml
formulario:
  campos:
    - nome: "cnpj"
      obrigatorio: true
      validacoes:
        - tipo: "required"
          mensagem_erro: "CNPJ é obrigatório"
        - tipo: "pattern"
          regex: "^\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}$"
          mensagem_erro: "CNPJ inválido"

    - nome: "razaoSocial"
      obrigatorio: true
      validacoes:
        - tipo: "required"
          mensagem_erro: "Razão Social é obrigatória"
        - tipo: "maxlength"
          valor: 200
          mensagem_erro: "Razão Social deve ter no máximo 200 caracteres"

    - nome: "email"
      obrigatorio: false
      validacoes:
        - tipo: "email"
          mensagem_erro: "E-mail inválido"
```

3. **Documentar mapeamento:**
   - Criar tabela: Campo → Validators Angular → mat-error messages

---

### PASSO 6.7.2: Implementar Validators Angular

**O agente DEVE implementar validators no FormGroup:**

**Localização:**
- `src/app/modules/[modulo]/[entidade]-form/[entidade]-form.component.ts`

**Implementação obrigatória:**

```typescript
import { Validators } from '@angular/forms';

// No construtor ou ngOnInit:
this.form = this.fb.group({
  // Campo obrigatório com pattern
  cnpj: ['', [
    Validators.required,
    Validators.pattern(/^\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}$/)
  ]],

  // Campo obrigatório com maxlength
  razaoSocial: ['', [
    Validators.required,
    Validators.maxLength(200)
  ]],

  // Campo opcional com email
  email: ['', [
    Validators.email
  ]],

  // Campo obrigatório simples
  nomeFantasia: ['', Validators.required]
});
```

**Validação:**
- ✅ TODOS os campos com `obrigatorio: true` possuem `Validators.required`
- ✅ TODOS os campos com `validacoes.tipo: pattern` possuem `Validators.pattern(regex)`
- ✅ TODOS os campos com `validacoes.tipo: email` possuem `Validators.email`
- ✅ TODOS os campos com `validacoes.tipo: maxlength` possuem `Validators.maxLength(valor)`
- ✅ TODOS os campos com `validacoes.tipo: minlength` possuem `Validators.minLength(valor)`

**SE qualquer campo NÃO tiver validator obrigatório:**
- ❌ BLOQUEIO: Implementar validator ausente

---

### PASSO 6.7.3: Implementar mat-error Messages

**O agente DEVE implementar mat-error para CADA validação:**

**Localização:**
- `src/app/modules/[modulo]/[entidade]-form/[entidade]-form.component.html`

**Implementação obrigatória:**

```html
<!-- Campo CNPJ -->
<mat-form-field>
  <mat-label>CNPJ</mat-label>
  <input matInput formControlName="cnpj" [data-test]="RF006-input-cnpj">

  <!-- mat-error para required -->
  <mat-error *ngIf="form.get('cnpj')?.hasError('required')" [data-test]="RF006-input-cnpj-error-required">
    CNPJ é obrigatório
  </mat-error>

  <!-- mat-error para pattern -->
  <mat-error *ngIf="form.get('cnpj')?.hasError('pattern')" [data-test]="RF006-input-cnpj-error-pattern">
    CNPJ inválido
  </mat-error>
</mat-form-field>

<!-- Campo Razão Social -->
<mat-form-field>
  <mat-label>Razão Social</mat-label>
  <input matInput formControlName="razaoSocial" [data-test]="RF006-input-razaosocial">

  <mat-error *ngIf="form.get('razaoSocial')?.hasError('required')" [data-test]="RF006-input-razaosocial-error-required">
    Razão Social é obrigatória
  </mat-error>

  <mat-error *ngIf="form.get('razaoSocial')?.hasError('maxlength')" [data-test]="RF006-input-razaosocial-error-maxlength">
    Razão Social deve ter no máximo 200 caracteres
  </mat-error>
</mat-form-field>

<!-- Campo E-mail (opcional) -->
<mat-form-field>
  <mat-label>E-mail</mat-label>
  <input matInput formControlName="email" [data-test]="RF006-input-email">

  <mat-error *ngIf="form.get('email')?.hasError('email')" [data-test]="RF006-input-email-error-email">
    E-mail inválido
  </mat-error>
</mat-form-field>
```

**Nomenclatura data-test para mat-error:**
- Padrão: `RFXXX-input-[campo]-error-[tipo]`
- Exemplos:
  - `RF006-input-cnpj-error-required`
  - `RF006-input-cnpj-error-pattern`
  - `RF006-input-razaosocial-error-maxlength`
  - `RF006-input-email-error-email`

**Validação:**
- ✅ TODOS os validators possuem mat-error correspondente
- ✅ TODAS as mensagens batem com UC-RFXXX.yaml → `formulario.campos[].validacoes[].mensagem_erro`
- ✅ TODOS os mat-error possuem data-test

**SE qualquer mat-error estiver ausente:**
- ❌ BLOQUEIO: Implementar mat-error ausente

---

### PASSO 6.7.4: Desabilitar Botões em Form Inválido

**O agente DEVE desabilitar botões de ação quando formulário estiver inválido:**

**Localização:**
- `src/app/modules/[modulo]/[entidade]-form/[entidade]-form.component.html`

**Implementação obrigatória:**

```html
<!-- Botão Salvar -->
<button mat-raised-button
        color="primary"
        [disabled]="form.invalid"
        [data-test]="RF006-salvar-cliente"
        (click)="salvar()">
  Salvar
</button>

<!-- Botão Confirmar (em dialogs) -->
<button mat-button
        [disabled]="form.invalid"
        [data-test]="RF006-confirmar"
        (click)="confirmar()">
  Confirmar
</button>
```

**Validação:**
- ✅ TODOS os botões de ação (Salvar, Confirmar, Criar, Atualizar) possuem `[disabled]="form.invalid"`
- ✅ Botões de cancelamento NÃO possuem disabled (permitir cancelar sempre)

**SE qualquer botão de ação NÃO estiver desabilitado:**
- ❌ BLOQUEIO: Adicionar `[disabled]="form.invalid"`

---

### PASSO 6.7.5: Validar Comportamento

**O agente DEVE validar comportamento de validação:**

**Teste manual:**

1. **Abrir formulário vazio:**
   - ✅ Botão Salvar deve estar DESABILITADO
   - ✅ Nenhum mat-error visível (touched = false)

2. **Clicar em campo obrigatório e sair (blur):**
   - ✅ mat-error "Campo é obrigatório" deve aparecer
   - ✅ Botão Salvar permanece DESABILITADO

3. **Preencher campo com valor INVÁLIDO:**
   - ✅ mat-error de validação específica deve aparecer (ex: "CNPJ inválido")
   - ✅ Botão Salvar permanece DESABILITADO

4. **Preencher campo com valor VÁLIDO:**
   - ✅ mat-error desaparece
   - ✅ Se TODOS os campos obrigatórios válidos → Botão Salvar HABILITA

5. **Clicar em Salvar com formulário VÁLIDO:**
   - ✅ Operação executa normalmente
   - ✅ Nenhum erro de validação

**SE qualquer comportamento falhar:**
- ❌ BLOQUEIO: Corrigir implementação de validators ou mat-error

---

### PASSO 6.7.6: Documentar Validators

**O agente DEVE atualizar STATUS.yaml:**

```yaml
desenvolvimento:
  frontend:
    validators_angular:
      implementados:
        - campo: "cnpj"
          validators: ["required", "pattern"]
          mat_errors: ["required", "pattern"]
        - campo: "razaoSocial"
          validators: ["required", "maxLength"]
          mat_errors: ["required", "maxlength"]
        - campo: "email"
          validators: ["email"]
          mat_errors: ["email"]

      cobertura: "100%"  # Todos os campos de UC-RFXXX.yaml implementados
      botoes_disabled: true  # Botões desabilitam em form.invalid
```

---

### PASSO 6.7.7: Validação Final de Bloqueio

**O agente DEVE executar validação final:**

**Verificar:**

1. **Cobertura de validators:**
   - ✅ TODOS os campos obrigatórios de UC-RFXXX.yaml possuem Validators.required
   - ✅ TODOS os campos com validacoes de UC-RFXXX.yaml possuem validators correspondentes

2. **Cobertura de mat-error:**
   - ✅ TODOS os validators possuem mat-error correspondente
   - ✅ TODAS as mensagens batem com UC-RFXXX.yaml

3. **Nomenclatura data-test:**
   - ✅ TODOS os mat-error possuem data-test no formato `RFXXX-input-[campo]-error-[tipo]`

4. **Botões disabled:**
   - ✅ TODOS os botões de ação possuem `[disabled]="form.invalid"`

**Critério de Aprovação:**
- ✅ Cobertura de validators: 100%
- ✅ Cobertura de mat-error: 100%
- ✅ Nomenclatura data-test: 100% conforme padrão
- ✅ Botões disabled: 100%

**SE qualquer verificação FALHAR:**
- ❌ Frontend está INCOMPLETO para validação
- ❌ BLOQUEIO: Não prosseguir para validação

---

### IMPACTO ESPERADO

Esta fase resolve **21% dos problemas do RF006** causados por validators ausentes.

**Sem esta fase:**
- ❌ Formulários aceitam dados inválidos
- ❌ mat-error não aparece para usuário
- ❌ Botões não desabilitam quando formulário inválido
- ❌ Testes E2E falham validando mat-error
- ❌ 21% de taxa de falha (3/14 falhas do RF006)

**Com esta fase:**
- ✅ Formulários validam corretamente
- ✅ mat-error aparecem para usuário
- ✅ Botões desabilitam em form.invalid
- ✅ Testes E2E passam validando mat-error
- ✅ Zero falhas por validators ausentes

**Resultado esperado:**
- ✅ Taxa de falha E2E reduzida em 21%
- ✅ UX consistente (usuário vê erros claramente)
- ✅ Código robusto e validado

**Referências:**
- Relatório de testes: `D:\IC2\.temp_ia\RELATORIO-TESTES-RF006-2026-01-11.md` (GAP 1)
- UC Template: `D:\IC2_Governanca\governanca\templates\UC-TEMPLATE.yaml` (seção formulario.campos)
- Testes falhados: FA-UC01-001, FA-UC01-002, FA-UC01-003

---

## CRITERIO DE PRONTO OBRIGATORIO

Para considerar o frontend COMPLETO, DEVE atender:

- [ ] **100% dos UCs do UC-RFXXX implementados**
- [ ] **100% dos fluxos testados** (Fluxo Principal, Alternativos, Excecoes)
- [ ] Frontend funcionalmente completo (nao parcial)
- [ ] Build frontend OK
- [ ] Seeds funcionais aplicados com sucesso
- [ ] Backend funciona **sem reset manual de banco**
- [ ] Funcionalidade navegavel e funcional
- [ ] Nenhuma alteracao fora do escopo
- [ ] Testes E2E **EXECUTADOS e aprovados (100%)**
- [ ] Usuario com perfil adequado consegue:
  - Logar
  - Acessar via menu
  - Consumir endpoints sem erros de autorizacao
- [ ] Nenhum erro de permissao no console
- [ ] Nenhuma chave i18n faltante
- [ ] Pronto para passar pelo contrato de validacao de frontend

### TRAVA OBRIGATORIA - i18n Completo (v1.0 - 2026-01-30)

**EXCECAO:** Funcionalidades base (login, multi-tenant, RBAC, Central de Modulos) estao ISENTAS desta trava.

Para TODAS as outras funcionalidades, o frontend so e considerado COMPLETO se:

- [ ] **PT-BR:** TODAS as chaves de traducao criadas/atualizadas em `pt-BR.json`
- [ ] **EN-US:** TODAS as chaves de traducao criadas/atualizadas em `en-US.json`
- [ ] **ES-ES:** TODAS as chaves de traducao criadas/atualizadas em `es-ES.json`
- [ ] **Console:** ZERO warnings de traducao no console (chaves faltantes)
- [ ] **Fallback:** Hierarquia pt-BR → en-US → es-ES funcional

**VALIDACAO OBRIGATORIA:**
O agente DEVE executar a funcionalidade nos 3 idiomas e verificar:
- Nenhum texto hardcoded aparecendo
- Nenhuma chave nao traduzida (ex: `management.clientes.titulo`)
- Nenhum warning no console

**SE QUALQUER ITEM ACIMA FOR NAO:**
- ❌ Frontend NAO e considerado COMPLETO
- ❌ NAO pode passar para CONTRATO-VALIDACAO-FRONTEND
- ❌ STATUS.yaml DEVE permanecer como `em_progresso`

**JUSTIFICATIVA:**
- Sistema e multi-idioma por design
- Usuarios em PT, EN e ES dependem de traducoes completas
- Chaves faltantes degradam experiencia do usuario

⚠️ **ATENCAO CRITICA:** Este contrato NAO permite implementacao parcial.

**TODOS os UCs devem estar implementados.**

**Cobertura parcial = REPROVADO**

**Qualquer ressalva = REPROVACAO**

Ao concluir, o agente DEVE informar explicitamente:
- Que os testes foram executados
- Quais cenarios foram cobertos
- Que a cobertura UC e 100%

---

## ANTI-ESQUECIMENTO (OBRIGATORIO)

⚠️ **LEITURA OBRIGATÓRIA NO INÍCIO:**

Antes de iniciar qualquer implementação, você DEVE ler:
- **D:\IC2\docs\anti-esquecimento-frontend.md**

Este documento contém os "esquecimentos" mais comuns que devem ser evitados.

A leitura está incluída como PRIMEIRO item do TODO list.

---

## BLOQUEIO DE EXECUÇÃO

Se qualquer dependência exigir:

- Nova entidade de domínio
- Nova regra de negócio
- Alteração estrutural de arquitetura

O agente DEVE:
- **PARAR**
- **ALERTAR**
- **DESCREVER a dependência**
- **AGUARDAR decisão**

---

**Este contrato é vinculante.
Execuções fora dele são inválidas.**

---

## PROXIMO CONTRATO

Apos conclusao deste contrato:

➡️ **CONTRATO-VALIDACAO-FRONTEND** (contracts/desenvolvimento/validacao/frontend.md)

O validador vai:
1. Verificar que TUDO no UC-RFXXX foi coberto 100%
2. **Criar branch** (se não existir)
3. **Fazer commit e sync** (SE aprovado 100% sem ressalvas)

⚠️ **IMPORTANTE:** O agente de EXECUÇÃO NÃO faz commit nem sync.
Essa responsabilidade é do VALIDADOR quando aprovar 100%.

---

## REGRA DE NEGACAO ZERO

Se uma solicitacao:
- nao estiver explicitamente prevista no contrato ativo, ou
- conflitar com qualquer regra do contrato

ENTAO:

- A execucao DEVE ser NEGADA
- Nenhuma acao parcial pode ser realizada
- Nenhum "adiantamento" e permitido
