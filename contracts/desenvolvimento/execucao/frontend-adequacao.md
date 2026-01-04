# CONTRATO DE ADEQUACAO DE FRONTEND

Este contrato regula a adequacao de frontends existentes
para o modelo de governanca atual.

---

## OBJETIVO

- Adequar frontend existente aos RFs/UCs/WFs atualizados
- Completar funcionalidades faltantes
- Ajustar integracao com backend regularizado
- Preservar layouts aprovados e componentizacao Fuse
- Preparar para validacao frontend completa

---

## O QUE ESTE CONTRATO PERMITE

- Adicionar funcionalidades faltantes do UC
- Ajustar DTOs para alinhar com backend regularizado
- Implementar i18n completo (pt-BR, en-US, es-ES)
- Adicionar testes E2E Playwright
- Corrigir bugs de frontend ja identificados
- Ajustar estados obrigatorios (Loading, Vazio, Erro)
- Refatorar para Standalone Components (se ainda nao for)
- Adicionar integracao de diagnosticos e auditoria

---

## O QUE ESTE CONTRATO PROIBE

- Quebrar layout aprovado
- Remover funcionalidades existentes
- Refatorar arquitetura sem necessidade
- Criar novos componentes genéricos (usar Fuse)
- Alterar backend
- Criar novas regras de negocio
- Modificar rotas globais sem autorizacao

---

## DEPENDENCIA OBRIGATORIA

Este contrato **DEPENDE** do contrato:

- **CONTRATO-PADRAO-DESENVOLVIMENTO.md**

Antes de executar este contrato, o agente **DEVE**:

1. Ler `CONTRATO-PADRAO-DESENVOLVIMENTO.md` **COMPLETAMENTE**
2. Seguir **TODOS** os checklists e regras definidos
3. Consultar as fontes externas obrigatorias:
   - `D:\DocumentosIC2\arquitetura.md`
   - `D:\DocumentosIC2\inteligencia-artificial\prompts\desenvolvimento.md`
   - `D:\DocumentosIC2\inteligencia-artificial\prompts\traducao.md`

**VIOLACAO:** Executar este contrato sem ler o CONTRATO-PADRAO-DESENVOLVIMENTO.md
e considerado **execucao invalida**.

---

## IDENTIFICACAO DO AGENTE

**PAPEL:** Agente Executor de Adequacao de Frontend
**ESCOPO:** Adequacao de frontend existente com preservacao de layout aprovado

---

## ATIVACAO DO CONTRATO

Este contrato e ativado quando a solicitacao contiver explicitamente
a expressao:

> **"Conforme CONTRATO DE ADEQUACAO DE FRONTEND"**

O Requisito Funcional, contexto e escopo especifico
DEVEM ser informados **exclusivamente na solicitacao**.

Este contrato **NUNCA** deve ser alterado para um RF especifico.

---

## VALIDACAO INICIAL OBRIGATORIA (ANTES DE QUALQUER ACAO)

Antes de QUALQUER acao de adequacao, o agente DEVE validar que o sistema nao esta quebrado.

### 1. Validacao Git (ANTES de criar branch)

**SEMPRE** validar o estado do Git ANTES de criar feature branch:

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
  - Continuar com validacao de builds

**Justificativa:**

**Nao adianta criar feature branch a partir de um branch com merge conflicts.**

Se criar branch de `dev` quando `dev` tem conflitos:
- Feature branch **herda os conflitos**
- Build **falha imediatamente**
- Erros aparecem como se fossem do RF
- Depuracao fica confusa
- Retrabalho garantido

**A validacao Git ANTES de criar branch evita trabalho desperdicado.**

### 2. Validacao de Builds (ANTES de qualquer adequacao)

```bash
# 1. Build do backend
cd backend/IControlIT.API
dotnet build

# 2. Build do frontend
cd ../../frontend/icontrolit-app
npm run build

# 3. Se QUALQUER build quebrar: PARAR
```

### Regras de Validacao de Builds

- Se `dotnet build` FALHAR:
  - **PARAR** imediatamente
  - **CORRIGIR** erros de build do backend
  - **RE-VALIDAR** ate que build passe
  - **NAO** prosseguir para adequacao

- Se `npm run build` FALHAR:
  - **PARAR** imediatamente
  - **CORRIGIR** erros de build do frontend
  - **RE-VALIDAR** ate que build passe
  - **NAO** prosseguir para adequacao

- Se AMBOS os builds PASSAREM:
  - **PROSSEGUIR** para adequacao do frontend
  - Garantir que sistema continua buildando ao final

### Justificativa

**Nao adianta pegar um sistema quebrado para desenvolver.**

Se o sistema ja esta quebrado ANTES da adequacao:
- Erros podem ser mascarados
- Depuracao fica impossivel
- Retrabalho e garantido

**A validacao inicial economiza tempo e garante qualidade.**

---

## AUTONOMIA TOTAL DO AGENTE (EXECUCAO IMEDIATA E COMPLETA)

O agente POSSUI AUTONOMIA TOTAL e DEVE EXECUTAR IMEDIATAMENTE:

**PROIBIDO PERGUNTAR:**
- ❌ "Você quer que eu continue?"
- ❌ "Devo corrigir todos os gaps agora?"
- ❌ "Prefere fazer em fases?"
- ❌ "Qual opção você escolhe?"
- ❌ QUALQUER pergunta sobre escopo ou priorização

**EXECUCAO OBRIGATORIA:**
- ✅ Corrigir **TODOS** os gaps identificados
- ✅ Implementar **TODOS** os UCs faltantes (100%)
- ✅ Adicionar i18n completo (pt-BR, en-US, es-ES)
- ✅ Criar **TODOS** os testes E2E
- ✅ Deixar frontend **100% PRONTO**
- ✅ Build passando
- ✅ Testes E2E passando
- ✅ UC coberto 100%

**REGRA ABSOLUTA:**

Adequacao = **100% de execucao IMEDIATA**

Nao existe "fazer parte agora e parte depois".
Nao existe "corrigir apenas os gaps criticos".
Nao existe "aguardar decisao do usuario".

**O agente EXECUTA TUDO ate 100% sem perguntar.**

Se o agente perguntar algo relacionado a escopo, priorização ou continuação:
➡️ **VIOLACAO DO CONTRATO**

**Autonomia significa:**
- Buildar backend (`dotnet build`)
- Buildar frontend (`npm run build`)
- Rodar backend (`dotnet run`)
- Rodar frontend (`npm start`)
- Executar testes (`npm run e2e`)
- Corrigir **TODOS** os erros de build
- Implementar **TODOS** os gaps funcionais
- Deixar sistema **100% FUNCIONAL** ao final

### Regras de Autonomia

**E PROIBIDO:**
- Perguntar ao usuario se pode buildar
- Perguntar ao usuario se pode rodar
- Esperar que usuario execute comandos manualmente
- Entregar sistema quebrado ou nao buildando
- **Criar "relatórios de gaps" com opções/perguntas**
- **Oferecer "Opção A, B ou C" ao usuário**
- **Parar no meio da execução para "aguardar decisão"**
- **Criar commits intermediários e perguntar "continuo?"**

**E OBRIGATORIO:**
- Executar todos os comandos necessarios autonomamente
- Deixar sistema buildando ANTES de iniciar adequacao
- Deixar sistema buildando e rodando AO FINAL da adequacao
- Garantir funcionamento sem intervencao manual
- **Executar TUDO até 100% sem pausas**
- **Criar um UNICO commit ao final com TUDO pronto**
- **NÃO criar relatórios com "próximos passos" - FAZER os próximos passos**

**Filosofia:**

> O usuario deixa o sistema funcionando.
> O agente DEVE deixar o sistema funcionando.
> Ninguem intervem manualmente em builds ou execucoes.
> **Ninguém escolhe "opções" - o agente EXECUTA até 100%.**

---

## TODO LIST OBRIGATORIA (LER PRIMEIRO)

> **ATENCAO:** O agente DEVE criar esta todo list IMEDIATAMENTE apos ativar o contrato.
> **NENHUMA ACAO** pode ser executada antes da todo list existir.
> **COPIAR EXATAMENTE** o template abaixo, substituindo RFXXX pelo RF real.

### Template para RF Unico (RFXXX)

```
TODO LIST - Adequacao Frontend RFXXX
====================================

[pending] Ler anti-esquecimento PRIMEIRO
  +-- [pending] Ler D:\IC2\docs\anti-esquecimento-frontend.md

[pending] Validacao Git Inicial (ANTES de criar branch)
  |-- [pending] git status (verificar estado limpo)
  |-- [pending] Verificar ausencia de merge conflicts no branch atual
  |-- [pending] Se merge conflicts existirem: PARAR, REPORTAR, AGUARDAR resolucao
  +-- [pending] Somente criar branch se Git estado limpo

[pending] Validacao Inicial (ANTES de qualquer adequacao)
  |-- [pending] cd backend/IControlIT.API && dotnet build
  |-- [pending] cd frontend/icontrolit-app && npm run build
  |-- [pending] Se QUALQUER build falhar: PARAR e CORRIGIR
  +-- [pending] Somente prosseguir se AMBOS builds passarem

[pending] Ler documentacao do RF
  |-- [pending] Ler RFXXX.md
  |-- [pending] Ler UC-RFXXX.md
  |-- [pending] Ler WF-RFXXX.md (layouts e estados)
  +-- [pending] Identificar endpoints do backend regularizado

[pending] Auditar frontend atual
  |-- [pending] Identificar componentes existentes
  |-- [pending] Listar funcionalidades ja implementadas
  |-- [pending] Identificar gaps funcionais (UC vs codigo)
  |-- [pending] Validar layout aprovado (80%+ completo)
  |-- [pending] Validar i18n existente
  +-- [pending] Gerar relatorio de gaps

[pending] Validar pre-requisitos
  |-- [pending] Verificar backend regularizado e mergeado em dev
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
  |     +-- [pending] Se FALHAR: analisar causa
  |-- [pending] Se erro no frontend atual: CORRIGIR e re-testar
  +-- [pending] Se erro em outro RF: criar RELATORIO-ERROS-RFXXX.md

[pending] Adequar Componentes Existentes
  |-- [pending] Ajustar DTOs conforme backend regularizado
  |-- [pending] Adicionar funcionalidades faltantes do UC
  |-- [pending] Implementar estados faltantes (Loading/Vazio/Erro)
  |-- [pending] Refatorar para Standalone Components (se necessario)
  |-- [pending] Preservar layout aprovado (componentes Fuse)
  +-- [pending] Validar responsividade (desktop/tablet/mobile)

[pending] Adequar Services
  |-- [pending] Ajustar interfaces para alinhar com backend
  |-- [pending] Adicionar metodos faltantes do UC
  |-- [pending] Integrar diagnosticos (DiagnosticsLoggerService)
  +-- [pending] Validar tratamento de erros estruturados

[pending] Implementar i18n Completo (OBRIGATORIO)
  |-- [pending] Completar chaves pt-BR faltantes
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
  |-- [pending] TC-E2E: Estados (Loading/Vazio/Erro)
  |-- [pending] Validar responsividade (desktop/mobile)
  +-- [pending] TC-E2E: Criar registro FINAL como evidencia (NAO excluir)

[pending] Validar Criterio de Pronto
  |-- [pending] Build frontend OK (ng build)
  |-- [pending] Nenhum warning i18n no console
  |-- [pending] Nenhum erro 401/403 no console
  |-- [pending] Seeds aplicados sem reset manual
  |-- [pending] Testes E2E APROVADOS (100%)
  |-- [pending] UC coberto 100%
  |-- [pending] Layout aprovado preservado
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
git checkout -b feature/RFXXX-frontend-adequacao
```

Ao concluir a implementacao:

```bash
# 3. Commit e merge em dev
git add .
git commit -m "feat(RFXXX): adequacao frontend"
git checkout dev
git pull origin dev
git merge feature/RFXXX-frontend-adequacao
git push origin dev
git branch -d feature/RFXXX-frontend-adequacao
```

> Referencia completa: `docs/devops/BRANCH-WORKFLOW.md`

---

## ESCOPO FUNCIONAL

Inclui exclusivamente:

- Adicionar funcionalidades faltantes do UC
- Ajustar DTOs para backend regularizado
- Completar i18n (pt-BR, en-US, es-ES)
- Adicionar testes E2E faltantes
- Implementar estados obrigatorios (Loading/Vazio/Erro)
- Refatorar para Standalone Components
- Integrar diagnosticos e auditoria

E **EXPRESSAMENTE PROIBIDO**:

- Quebrar layout aprovado existente
- Remover funcionalidades ja implementadas
- Usar chaves i18n nao registradas
- Depender de fallback silencioso do Transloco
- Considerar funcionalidade pronta com warnings no console

Qualquer warning de traducao ausente:
- **INVALIDA a entrega**
- Deve ser tratado como **erro funcional**

---

## LAYOUTS APROVADOS (REFERENCIA OBRIGATORIA)

O projeto possui layouts JA APROVADOS que DEVEM ser preservados.

### Paginas Padrao (Referencias)

- `/management/users` - Listagem + Modal de detalhes
- `/management/roles` - Listagem + Drawer de edicao
- `/hierarquia/centros-custo` - Listagem com filtros avancados
- `/admin/management/sla-operacoes` - Listagem com status visuais

### Estrutura Visual Obrigatoria

Toda tela de listagem DEVE ter:
1. **Header** com titulo + botao de criar
2. **Filtros** (se aplicavel) em linha ou drawer
3. **Tabela** com Mat-Table + Sort + Pagination
4. **Acoes** por linha (editar, excluir, visualizar)
5. **Estados visuais:**
   - Loading (spinner centralizado)
   - Vazio (mensagem + ilustracao)
   - Erro (mensagem + acao de retry)
   - Dados (tabela populada)

### Componentes Fuse Disponiveis (Reutilizar)

O projeto usa **Fuse Admin Template** que fornece:

**Componentes visuais:**
- `FuseCardComponent` - Cards estilizados
- `FuseAlertComponent` - Alertas contextuais
- `FuseConfirmationService` - Dialogos de confirmacao
- `FuseNavigationService` - Menu lateral dinamico
- `FuseScrollbarDirective` - Scrollbars customizados
- `FuseLoadingBarComponent` - Loading bars

**Servicos utilitarios:**
- `FuseMediaWatcherService` - Deteccao de breakpoints
- `FuseConfigService` - Configuracoes globais
- `FusePlatformService` - Deteccao de plataforma

**E OBRIGATORIO reutilizar componentes Fuse antes de criar novos.**

---

## ZONAS PERMITIDAS

- `frontend/icontrolit-app/src/app/modules/**` (componentes do RF)
- `frontend/icontrolit-app/src/app/core/services/**` (se necessario)
- `frontend/icontrolit-app/src/app/core/models/**` (se necessario)
- `frontend/icontrolit-app/src/assets/i18n/**` (traducoes)

---

## ZONAS PROIBIDAS

- `/docs/**`
- Layout base e shell principal
- Core compartilhado existente (salvo autorizacao explicita)
- Configuracoes globais do Angular
- Arquitetura base do frontend
- Componentes ja aprovados em outros RFs

---

## REGRAS GERAIS (INVIOLAVEIS)

- Seguir estritamente:
  - `ARCHITECTURE.md`
  - `CONVENTIONS.md`
  - `CLAUDE.md`
- NÃO inferir requisitos
- Usar **Standalone Components**
- Usar **Transloco obrigatoriamente**
- NÃO criar servicos genericos reutilizaveis
- NÃO alterar estrutura global de rotas
- Se precisar sair do escopo: **PARAR e AVISAR**
- O layout deve seguir **EXATAMENTE** os padroes ja existentes
- O frontend **nao e apenas UI**, e integracao com todo o ecossistema
- **Preservar layout aprovado** (80%+ do frontend ja esta correto)

---

## GOVERNANCA DE ACESSO (OBRIGATORIA)

Antes de iniciar qualquer implementacao, o agente DEVE declarar explicitamente:

- Quais permissoes a funcionalidade exige
- Qual perfil deve ter acesso (minimo: `developer`)

Essas permissoes sao **pre-condicoes de funcionamento**
e NAO simples configuracoes opcionais.

---

## PROVA DE ACESSO (OBRIGATORIA)

Antes de iniciar QUALQUER implementacao de frontend,
o agente DEVE comprovar que o backend esta acessivel
para o perfil esperado.

O agente DEVE:

- Autenticar como usuario `developer`
- Executar manualmente (ou via teste automatizado)
  ao menos UMA chamada real da funcionalidade
- Confirmar retorno HTTP **200**

Se o retorno for:
- 401
- 403
- 404 inesperado

O agente DEVE:
- **PARAR imediatamente**
- Corrigir seeds, permissoes ou registros necessarios
- Reexecutar a verificacao
- Somente prosseguir apos confirmacao de acesso real

E **PROIBIDO**:
- Assumir acesso com base apenas em codigo ou registry
- Prosseguir sem validacao runtime

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

## ALTERACOES PERMITIDAS NO BACKEND (LIMITADAS)

Permitidas **somente** para viabilizar acesso e testes:

- Registro da funcionalidade na **Central de Modulos**
- Associacao de permissoes existentes a perfis existentes
- Ajustes minimos e estritamente necessarios para habilitar acesso

Caso o registro na Central de Modulos:
- Nao exista
- Ou exija alteracao nao permitida

O agente DEVE:
- **PARAR**
- **REPORTAR explicitamente**
- **AGUARDAR decisao**

Essas alteracoes **NAO** sao consideradas:
- Mudanca de arquitetura
- Criacao de escopo novo
- Evolucao funcional

---

## SEEDS FUNCIONAIS (OBRIGATORIO)

Para que a funcionalidade seja considerada testavel e concluida,
o agente DEVE garantir a existencia dos dados minimos necessarios.

Inclui, quando aplicavel:

- Entidades dependentes (Cliente, Empresa, Perfis)
- Permissoes necessarias
- Associacao das permissoes ao perfil `developer`
- Usuario de teste funcional

### REGRAS DE SEED

- Criar SOMENTE se nao existirem
- Seeds idempotentes
- NAO alterar dados produtivos
- Seeds existem apenas para habilitar execucao e testes

### LOCAL DE SEED

- `DataInitializer`
- Seeders existentes
- Mecanismo de inicializacao ja adotado pelo projeto

### E PROIBIDO

- Criar seeds em handlers
- Criar seeds escondidos em testes
- Criar seeds temporarios sem controle

---

## VERIFICACAO DE CONSISTENCIA NO STARTUP (CRITICO)

Em ambientes **DEV/TEST**, o sistema DEVE validar no startup:

- Existencia das permissoes da funcionalidade
- Associacao ao perfil `developer`
- Existencia do registro na Central de Modulos

Se qualquer item estiver ausente:

- Logar erro claro
- NAO permitir funcionamento silencioso
- Alertar explicitamente

---

## TESTES E2E (PLAYWRIGHT)

Os testes E2E sao **obrigatorios**.

### Regras

- Qualquer **401 ou 403** deve falhar o teste
- Respostas **404, 500 ou vazias inesperadas** devem falhar
- Testes devem validar:
  - Login como `developer`
  - Acesso via menu
  - Carregamento da listagem com dados reais
  - Execucao do fluxo principal (caminho feliz)
  - Estados visuais (Loading, Vazio, Erro)

### Responsividade (Validacao Funcional)

- Validar acesso funcional em diferentes viewports
- NAO exigir identidade visual absoluta entre desktop e mobile
- Validar que componentes Fuse se adaptam corretamente

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

Para considerar a adequacao frontend COMPLETA, DEVE atender:

- [ ] **100% dos UCs do UC-RFXXX cobertos**
- [ ] **100% dos fluxos testados** (FP, FA-XX, FE-XX)
- [ ] Frontend funcionalmente completo (nao parcial)
- [ ] Build frontend OK
- [ ] Seeds funcionais aplicados com sucesso
- [ ] Backend funciona **sem reset manual de banco**
- [ ] Funcionalidade navegavel e funcional
- [ ] i18n completo (`pt-BR`, `en-US`, `es-ES`)
- [ ] Nenhuma alteracao fora do escopo
- [ ] Testes E2E **EXECUTADOS e aprovados (100%)**
- [ ] Layout aprovado preservado
- [ ] Usuario `developer` consegue:
  - Logar
  - Acessar via menu
  - Consumir endpoints sem 403
- [ ] Nenhum erro de permissao no console
- [ ] Nenhuma chave i18n faltante
- [ ] Estados obrigatorios implementados (Loading/Vazio/Erro)
- [ ] Pronto para passar pelo CONTRATO-VALIDACAO-FRONTEND

⚠️ **ATENCAO CRITICA:** Este contrato NAO permite implementacao parcial.

**TODOS os UCs do UC-RFXXX devem estar cobertos.**

**Cobertura parcial = REPROVADO**

**Qualquer ressalva = REPROVACAO**

Ao concluir, o agente DEVE informar explicitamente:
- Que os testes foram executados
- Quais cenarios foram cobertos
- Que o layout aprovado foi preservado
- Que a cobertura UC e 100%

---

## ANTI-ESQUECIMENTO (OBRIGATORIO)

⚠️ **LEITURA OBRIGATÓRIA NO INÍCIO:**

Antes de iniciar qualquer adequação, você DEVE ler:
- **D:\IC2\docs\anti-esquecimento-frontend.md**

Este documento contém os "esquecimentos" mais comuns que devem ser evitados.

A leitura está incluída como PRIMEIRO item do TODO list.

---

## BLOQUEIO DE EXECUCAO

Se qualquer dependencia exigir:

- Nova entidade de dominio
- Nova regra de negocio
- Alteracao estrutural de arquitetura

O agente DEVE:
- **PARAR**
- **ALERTAR**
- **DESCREVER a dependencia**
- **AGUARDAR decisao**

---

## METODO DE TRABALHO

1. Auditar frontend atual (identificar 80%+ ja completo)
2. Gerar relatorio de gaps funcionais
3. Adequar apenas o necessario para cobrir UC 100%
4. Preservar layout aprovado
5. Garantir funcionamento atual + novos recursos
6. Preparar para validacao frontend

---

## RELATORIO DE GAPS (OBRIGATORIO)

Antes de iniciar adequacao, o agente DEVE gerar:

**Arquivo:** `.temp_ia/GAPS-FRONTEND-RFXXX.md`

**Conteudo obrigatorio:**

```markdown
# Gaps Frontend RFXXX

## Frontend Atual (JA IMPLEMENTADO)

- [x] Listagem de registros
- [x] Filtros basicos (nome, status)
- [x] Criar registro (modal)
- [x] Editar registro (modal)
- [ ] Excluir registro (faltando confirmacao)
- [x] Paginacao
- [x] Ordenacao

## Gaps Identificados (UC vs Codigo)

### Gap #1: Estado de Loading
- **UC exige:** Spinner durante carregamento
- **Codigo atual:** Nao implementado
- **Severidade:** IMPORTANTE

### Gap #2: Traducao incompleta
- **UC exige:** pt-BR + en-US + es-ES
- **Codigo atual:** Apenas pt-BR
- **Severidade:** CRITICO

### Gap #3: Testes E2E ausentes
- **UC exige:** 100% cobertura de fluxos
- **Codigo atual:** Nenhum teste
- **Severidade:** CRITICO

## Plano de Adequacao

1. Implementar estado de Loading (1h)
2. Completar traducoes (30min)
3. Criar testes E2E (2h)
4. Validar responsividade (30min)
```

---

**Este contrato e vinculante.
Execucoes fora dele sao invalidas.**

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
