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

[pending] Adequar Componentes Existentes (ADICIONAR DATA-TEST DURANTE ADEQUACAO)
  |-- [pending] Ajustar DTOs conforme backend regularizado
  |-- [pending] Adicionar funcionalidades faltantes do UC
  |     +-- [pending] Adicionar data-test em NOVOS elementos interativos
  |-- [pending] Implementar estados faltantes (Loading/Vazio/Erro)
  |     +-- [pending] Adicionar data-test em botoes de acao
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

[pending] Auditoria de Data-Test Attributes (OBRIGATORIO - PRE-TESTE E2E)
  |-- [pending] Executar auditoria: Conforme D:\IC2_Governanca\governanca\prompts\auditoria\data-test.md
  |-- [pending] Analisar relatorio de auditoria gerado
  |-- [pending] Se problemas BLOQUEANTES: corrigir TODOS antes de prosseguir
  |-- [pending] Se problemas ALTA: corrigir TODOS (nomenclatura incorreta)
  |-- [pending] Re-auditar apos correcoes
  +-- [pending] Validar 0 problemas BLOQUEANTES e 0 problemas ALTA

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

- `D:\IC2\frontend\icontrolit-app/src/app/modules/**` (componentes do RF)
- `D:\IC2\frontend\icontrolit-app/src/app/core/services/**` (se necessario)
- `D:\IC2\frontend\icontrolit-app/src/app/core/models/**` (se necessario)
- `D:\IC2\frontend\icontrolit-app/src/assets/i18n/**` (traducoes)

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

## VALIDAÇÃO DE FORMULÁRIOS (OBRIGATÓRIO)

**Versão:** 1.0
**Data:** 2026-01-10
**Contexto:** Adicionado após análise do RF006 onde validações de formulário não foram implementadas, resultando em 3 falhas E2E (6%).

**Momento de execução:** Durante adequação de componentes com formulários

### Por que validar formulários?

Durante a análise do RF006, identificamos 3 problemas críticos:
1. **FormControls sem validators:** Campos obrigatórios aceitavam valores vazios
2. **mat-error ausentes:** Erros de validação não apareciam no template
3. **Botão submit não desabilitado:** Form inválido permitia submit

### Fluxo de Validação (OBRIGATÓRIO)

**Para CADA formulário no componente, o agente DEVE:**

#### 1. Identificar Campos Obrigatórios no UC

Ler `UC-RFXXX.yaml` e identificar:
```yaml
formulario:
  campos:
    - nome: "Razão Social"
      data_test: "RF006-input-razaosocial"
      tipo: text
      obrigatorio: true  # ← Campo obrigatório
      validacoes:
        - tipo: "required"
          mensagem_erro: "Razão social é obrigatória"
        - tipo: "maxlength"
          valor: 200
          mensagem_erro: "Razão social deve ter no máximo 200 caracteres"
```

#### 2. Implementar Validators no FormControl

**Para campos obrigatórios:**
```typescript
// ✅ CORRETO
this.clienteForm = this.formBuilder.group({
  razaoSocial: ['', [Validators.required, Validators.maxLength(200)]],
  cnpj: ['', [Validators.required, CnpjValidator]],
  email: ['', [Validators.email]]
});
```

**❌ INCORRETO (sem validators):**
```typescript
this.clienteForm = this.formBuilder.group({
  razaoSocial: [''],  // ❌ Campo obrigatório sem Validators.required
  cnpj: ['']
});
```

#### 3. Implementar mat-error no Template

**Para CADA campo com validação:**
```html
<!-- ✅ CORRETO -->
<mat-form-field>
  <input
    matInput
    data-test="RF006-input-razaosocial"
    formControlName="razaoSocial"
    placeholder="Razão Social"
  />
  <mat-error data-test="RF006-input-razaosocial-error">
    {{ getErrorMessage('razaoSocial') }}
  </mat-error>
</mat-form-field>
```

**❌ INCORRETO (sem mat-error):**
```html
<mat-form-field>
  <input matInput formControlName="razaoSocial" />
  <!-- ❌ Falta mat-error -->
</mat-form-field>
```

#### 4. Implementar getErrorMessage()

**Método obrigatório no component.ts:**
```typescript
getErrorMessage(fieldName: string): string {
  const control = this.clienteForm.get(fieldName);

  if (control?.hasError('required')) {
    return this.translateService.translate(`errors.${fieldName}.required`);
  }

  if (control?.hasError('maxlength')) {
    const maxLength = control.getError('maxlength').requiredLength;
    return this.translateService.translate(`errors.${fieldName}.maxlength`, { maxLength });
  }

  if (control?.hasError('email')) {
    return this.translateService.translate(`errors.${fieldName}.email`);
  }

  return '';
}
```

#### 5. Desabilitar Botão Submit quando Form Inválido

**Sempre usar [disabled]:**
```html
<!-- ✅ CORRETO -->
<button
  mat-raised-button
  color="primary"
  data-test="RF006-salvar-cliente"
  [disabled]="!clienteForm.valid"
  (click)="salvar()"
>
  Salvar
</button>
```

**❌ INCORRETO (sem [disabled]):**
```html
<button
  mat-raised-button
  data-test="RF006-salvar-cliente"
  (click)="salvar()"
>
  Salvar
</button>
```

#### 6. Criar Testes Unitários para Validators

**Para CADA validator implementado:**
```typescript
describe('ClienteFormComponent - Validators', () => {
  it('deve invalidar formulário quando razão social vazia', () => {
    component.clienteForm.patchValue({ razaoSocial: '' });
    expect(component.clienteForm.get('razaoSocial')?.hasError('required')).toBe(true);
  });

  it('deve invalidar quando razão social excede 200 caracteres', () => {
    const longText = 'a'.repeat(201);
    component.clienteForm.patchValue({ razaoSocial: longText });
    expect(component.clienteForm.get('razaoSocial')?.hasError('maxlength')).toBe(true);
  });

  it('deve desabilitar botão salvar quando formulário inválido', () => {
    component.clienteForm.patchValue({ razaoSocial: '' });
    expect(component.clienteForm.valid).toBe(false);
  });
});
```

### Validações Obrigatórias

**Checklist de validação de formulários:**

- [ ] TODOS os campos obrigatórios do UC possuem `Validators.required`
- [ ] TODOS os campos com validação possuem `mat-error` no template
- [ ] TODOS os `mat-error` possuem `data-test="RFXXX-input-[campo]-error"`
- [ ] Método `getErrorMessage()` implementado no component.ts
- [ ] Botão submit possui `[disabled]="!form.valid"`
- [ ] Testes unitários criados para TODOS os validators
- [ ] Testes unitários executados: `npm test` → 100% aprovação

### Bloqueio de Execução

**Se validação de formulários FALHAR:**
- ❌ **NÃO** executar testes E2E
- ❌ **NÃO** considerar frontend concluído
- ✅ **CORRIGIR** todos os validators ausentes
- ✅ **ADICIONAR** mat-error em todos os campos
- ✅ **CRIAR** testes unitários para validators
- ✅ **RE-VALIDAR** até aprovação (100% cobertura)

### Justificativa

- Validações de formulário evitam submits inválidos
- mat-error fornece feedback visual ao usuário
- Botão desabilitado previne cliques em form inválido
- Testes unitários garantem que validators funcionam corretamente
- 3 testes E2E do RF006 falharam por falta dessas validações

### Referência Cruzada

- UC-TEMPLATE.yaml → seção `formulario.campos[].validacoes`
- CONVENTIONS.md → seção 3.3 "Mensagens de Erro de Validação"
- frontend.yaml (validação) → seção `validacoes_formulario`

---

## AUDITORIA DE DATA-TEST ATTRIBUTES (OBRIGATORIO)

**Momento de execução:** ANTES dos Testes E2E

Durante a adequação, data-test attributes devem ser adicionados em TODOS os elementos interativos novos ou modificados. Elementos existentes também devem ser auditados para garantir conformidade com o padrão RF006-acao-alvo.

### Por que auditar data-test?

- **Elementos esquecidos:** É comum esquecer de adicionar data-test em novos botões, inputs ou modais
- **Nomenclatura incorreta:** Elementos antigos podem ter nomenclatura sem prefixo RF (ex: `data-test="botao-salvar"` ao invés de `data-test="RF006-salvar-cliente"`)
- **Cobertura incompleta:** Testes E2E dependem de 100% de cobertura de data-test

### Fluxo de Auditoria (OBRIGATÓRIO)

**Antes de executar testes E2E, o agente DEVE:**

1. **Executar auditoria automatizada:**
   ```
   Conforme D:\IC2_Governanca\governanca\prompts\auditoria\data-test.md
   ```

2. **Analisar relatório gerado:**
   - Relatório: `D:\IC2\.temp_ia\RELATORIO-AUDITORIA-DATA-TEST-RFXXX-*.md`
   - Verificar problemas BLOQUEANTES (elementos sem data-test)
   - Verificar problemas ALTA (nomenclatura incorreta - falta prefixo RFXXX)

3. **Corrigir TODOS os problemas identificados:**
   - Usar prompt de correção: `D:\IC2\.temp_ia\PROMPT-CORRECAO-DATA-TEST-RFXXX-*.md`
   - Corrigir via `manutencao-controlada.md`
   - Re-auditar após correções

4. **Validar aprovação:**
   - 0 problemas BLOQUEANTES
   - 0 problemas ALTA
   - 100% dos elementos interativos com data-test no padrão correto

### Bloqueio de Execução

**Se auditoria reprovar (problemas BLOQUEANTES/ALTA):**
- ❌ **NÃO** executar testes E2E
- ❌ **NÃO** considerar frontend concluído
- ✅ **CORRIGIR** todos os problemas identificados
- ✅ **RE-AUDITAR** até aprovação (0 BLOQUEANTES, 0 ALTA)

### Padrão de Nomenclatura (RF-Específico)

**Formato obrigatório:**
```
data-test="RFXXX-<acao>-<alvo>"
```

**Exemplos corretos:**
- `data-test="RF006-salvar-cliente"`
- `data-test="RF006-input-razaosocial"`
- `data-test="RF006-editar-cliente"`
- `data-test="RF006-filtro-status"`

**Exemplos incorretos (problema ALTA):**
- `data-test="botao-salvar"` ❌ (falta RFXXX)
- `data-test="salvar-cliente"` ❌ (falta RFXXX)
- `data-test="RF006_salvar"` ❌ (underscore)
- `data-test="RF006-SalvarCliente"` ❌ (CamelCase)

### Justificativa

- Testes E2E dependem de data-test attributes estáveis
- Sem data-test corretos, 100% dos testes FALHAM
- Auditoria preventiva economiza tempo de debug
- Garante qualidade e manutenibilidade dos testes
- Evita retrabalho após implementação de testes E2E

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

## FASE 6.6: MATERIAL DIALOG BACKDROP CLEANUP (NOVO - BLOQUEANTE)

**🆕 ADICIONADO:** 2026-01-11 (Resolve 17% dos problemas identificados no RF006)

**Este passo é OBRIGATÓRIO para adequações que envolvem operações assíncronas com dialogs. Sem ele, testes E2E falharão por backdrop persistente.**

**Contexto do Problema:**

Durante testes do RF006, identificou-se que após operações assíncronas (consulta ReceitaWS, chamadas de API), o backdrop do Material Dialog **permanece visível** mesmo após o dialog ser fechado. Isso resulta em:
- ❌ Backdrop intercepta cliques subsequentes
- ❌ Testes E2E falham com timeout (elementos não clicáveis)
- ❌ Usuário não consegue interagir com a UI
- ❌ 17% de falhas nos testes E2E do RF006

**Aplicabilidade:**

Esta seção é obrigatória SE a adequação:
- Modifica ou cria operações assíncronas com Material Dialog
- Adiciona consultas a APIs externas (ReceitaWS, ViaCEP, etc.)
- Implementa dialogs de confirmação com operações CRUD
- Usa dialogs aninhados (dialog dentro de dialog)
- Adiciona validação assíncrona em formulários

SE a adequação NÃO envolve dialogs: **PULAR esta seção**.

---

### 6.6.1: Identificar Operações Assíncronas com Dialog (SE APLICÁVEL)

**O agente DEVE identificar no código existente e novo:**

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

**Critério de aceite:**
- ✅ TODAS as operações assíncronas com dialog identificadas (existentes + novas)
- ✅ Cenários de backdrop persistente mapeados

---

### 6.6.2: Aplicar Padrão de Cleanup (OBRIGATÓRIO)

**O agente DEVE aplicar o padrão de cleanup em TODAS as operações identificadas (existentes + novas):**

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
    await page.waitForSelector('.cdk-overlay-backdrop', {
      state: 'detached',  // ✅ Garante que foi removido
      timeout
    });
    await page.waitForTimeout(500);
  } catch (error) {
    throw new Error(
      `Dialog backdrop não foi removido dentro de ${timeout}ms.`
    );
  }
}
```

**Critério de aceite:**
- ✅ TODOS os cenários (existentes + novos) aplicam padrão de cleanup
- ✅ Código usa `firstValueFrom(dialogRef.afterClosed())`
- ✅ Testes E2E usam `waitForDialogToClosed(page)`

---

### 6.6.3: Atualizar Testes E2E Existentes

**O agente DEVE atualizar TODOS os testes E2E existentes que interagem com dialogs:**

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

#### Atualização de Testes

```typescript
// ❌ ANTES (INCORRETO):
test('TC-E2E: Criar registro', async ({ page }) => {
  await page.click('[data-test="RF006-criar-cliente"]');
  await page.fill('[data-test="RF006-input-cnpj"]', '00.000.000/0001-91');
  await page.click('[data-test="RF006-btn-consultar-cnpj"]');

  // ⚠️ PROBLEMA: Não aguarda backdrop desaparecer
  await page.fill('[data-test="RF006-input-razaosocial"]', 'EMPRESA TESTE');
  // ✗ FALHA: Backdrop intercepta preenchimento
});

// ✅ DEPOIS (CORRETO):
test('TC-E2E: Criar registro', async ({ page }) => {
  await page.click('[data-test="RF006-criar-cliente"]');
  await page.fill('[data-test="RF006-input-cnpj"]', '00.000.000/0001-91');
  await page.click('[data-test="RF006-btn-consultar-cnpj"]');

  await waitForDialogToClosed(page);  // ✅ Aguarda backdrop desaparecer

  await page.fill('[data-test="RF006-input-razaosocial"]', 'EMPRESA TESTE');
  // ✓ SUCESSO: Campo preenchido normalmente
});
```

**Critério de aceite:**
- ✅ TODOS os testes E2E existentes usam helpers de dialog
- ✅ Nenhum teste clica em elemento logo após fechar dialog sem aguardar
- ✅ Imports atualizados

---

### 6.6.4: Documentar Padrão no Código Adequado

**O agente DEVE adicionar comentários em métodos modificados/criados:**

```typescript
/**
 * PADRÃO OBRIGATÓRIO: Cleanup de Dialog Backdrop
 *
 * Ao usar MatDialog com operações assíncronas, SEMPRE:
 * 1. Fechar dialog: dialogRef.close()
 * 2. Aguardar fechamento: await firstValueFrom(dialogRef.afterClosed())
 *
 * Referência: frontend-adequacao.md FASE 6.6
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
- ✅ Métodos modificados/criados possuem comentários de padrão
- ✅ Referência ao contrato documentada

---

### 6.6.5: Atualizar STATUS.yaml

**O agente DEVE documentar aplicação do padrão:**

```yaml
desenvolvimento:
  frontend:
    status: done

    dialog_backdrop_cleanup:
      aplicado: true
      cenarios_identificados: 3
      cenarios_corrigidos: 3
      helpers_usados:
        - waitForDialogToClosed
        - waitForDialogToOpen
      testes_e2e_atualizados: 5
      data_adequacao: "2026-01-11"
      referencia_contrato: "FASE 6.6 - frontend-adequacao.md"
```

**Critério de aceite:**
- ✅ STATUS.yaml documentado
- ✅ Cenários identificados e corrigidos listados

---

### 6.6.6: Validação Final de Bloqueio

**Antes de marcar adequação frontend como done, o agente DEVE confirmar:**

- ✅ TODAS as operações assíncronas com dialog (existentes + novas) aplicam cleanup
- ✅ TODOS os testes E2E (existentes + novos) usam helpers de dialog
- ✅ Código possui comentários de padrão (em métodos modificados/criados)
- ✅ STATUS.yaml documentado
- ✅ Validação manual: Zero backdrops após operações

**SE qualquer verificação FALHAR:**
- ❌ Adequação frontend NÃO está pronta
- ❌ BLOQUEIO: Corrigir TODOS os problemas
- ❌ Re-validar até aprovação

---

**RESUMO DA FASE 6.6:**

Esta fase resolve **17% dos problemas do RF006** causados por backdrop persistente.

**Quando aplicar:**
- ✅ SE adequação envolve dialogs com operações assíncronas
- ❌ SE adequação NÃO envolve dialogs: PULAR seção

**Resultado esperado (SE aplicável):**
- ✅ Backdrop sempre limpo após operações
- ✅ Testes E2E passam sem timeouts
- ✅ Usuário interage normalmente
- ✅ Zero falhas por backdrop persistente

**Referências:**
- Helper implementado: `D:\IC2\frontend\icontrolit-app\e2e\helpers\dialog-helpers.ts`
- Contrato stateful: `D:\IC2_Governanca\governanca\contracts\testes\CONTRATO-TESTES-E2E-STATEFUL.md`
- Contrato criação: `frontend-criacao.md` FASE 6.6

---

## FASE 6.7: VALIDATORS ANGULAR OBRIGATÓRIOS (NOVO - BLOQUEANTE)

**🆕 ADICIONADO:** 2026-01-11 (Resolve 21% dos problemas identificados no RF006)

**Este passo é OBRIGATÓRIO para adequações que envolvem formulários. Sem ele, testes E2E falharão por validators ausentes.**

**Contexto do Problema:**

Durante testes do RF006, identificou-se que formulários SEM validators Angular adequados resultam em:
- ❌ Formulários aceitam dados inválidos
- ❌ mat-error não aparece para usuário
- ❌ Botões não desabilitam quando formulário inválido
- ❌ Testes E2E falham validando mat-error
- ❌ 21% de falhas nos testes E2E do RF006

**Aplicabilidade:**

Esta seção é obrigatória SE a adequação:
- Modifica ou cria formulários reativos (ReactiveFormsModule)
- Adiciona campos com validação obrigatória
- Implementa campos com pattern validation (CNPJ, CPF, email, telefone)
- Usa Material Form Field (mat-form-field)
- Adiciona validações de negócio (maxLength, minLength, etc.)

SE a adequação NÃO envolve formulários: **PULAR esta seção**.

---

### 6.7.1: Identificar Campos com Validação

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

### 6.7.2: Implementar Validators Angular

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

### 6.7.3: Implementar mat-error Messages

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

### 6.7.4: Desabilitar Botões em Form Inválido

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

### 6.7.5: Validar Comportamento

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

### 6.7.6: Documentar Validators

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

### 6.7.7: Validação Final de Bloqueio

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
- Contrato criação: `frontend-criacao.md` FASE 6.7

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
