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

O agente **DEVE** interagir com `docs/DECISIONS.md` durante a execução:

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

Se usuário solicitar registro, o agente **DEVE** adicionar ao final de `docs/DECISIONS.md`:

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

[pending] Implementar Componentes UI
  |-- [pending] Tela de Listagem (seguir padrao /management/users)
  |-- [pending] Tela de Criar/Editar
  |-- [pending] Tela de Visualizar
  |-- [pending] Modais (Confirmacao, Sucesso, Erro)
  +-- [pending] Estados (Loading, Vazio, Erro)

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

- `frontend/icontrolit-app/src/app/modules/**`
- `frontend/icontrolit-app/src/app/core/services/**` (somente se necessário)
- `frontend/icontrolit-app/src/app/core/models/**` (somente se necessário)

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

## CRITERIO DE PRONTO OBRIGATORIO

Para considerar o frontend COMPLETO, DEVE atender:

- [ ] **100% dos UCs do UC-RFXXX implementados**
- [ ] **100% dos fluxos testados** (Fluxo Principal, Alternativos, Excecoes)
- [ ] Frontend funcionalmente completo (nao parcial)
- [ ] Build frontend OK
- [ ] Seeds funcionais aplicados com sucesso
- [ ] Backend funciona **sem reset manual de banco**
- [ ] Funcionalidade navegavel e funcional
- [ ] i18n completo (todos os idiomas especificados no projeto)
- [ ] Nenhuma alteracao fora do escopo
- [ ] Testes E2E **EXECUTADOS e aprovados (100%)**
- [ ] Usuario com perfil adequado consegue:
  - Logar
  - Acessar via menu
  - Consumir endpoints sem erros de autorizacao
- [ ] Nenhum erro de permissao no console
- [ ] Nenhuma chave i18n faltante
- [ ] Pronto para passar pelo contrato de validacao de frontend

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

➡️ **CONTRATO-VALIDACAO-FRONTEND** (docs/contracts/desenvolvimento/validacao/frontend.md)

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
