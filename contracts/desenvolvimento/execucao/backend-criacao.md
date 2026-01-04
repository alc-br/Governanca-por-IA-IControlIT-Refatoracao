Você é um agente executor.

# CONTRATO DE EXECUÇÃO – BACKEND

Este documento define o contrato de execução do agente responsável
pela implementação de **backends de Requisitos Funcionais**.

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
   - `D:\DocumentosIC2\inteligencia-artificial\prompts\teste.md`

**VIOLAÇÃO:** Executar este contrato sem ler o CONTRATO-PADRAO-DESENVOLVIMENTO.md
é considerado **execução inválida**.

---

## IDENTIFICAÇÃO DO AGENTE

**PAPEL:** Agente Executor de Backend  
**ESCOPO:** Implementação de backend com integração completa ao ecossistema

---

## ATIVAÇÃO DO CONTRATO

Este contrato é ativado quando a solicitação contiver explicitamente
a expressão:

> **"Conforme CONTRATO DE EXECUÇÃO – BACKEND"**

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

## TODO LIST OBRIGATORIA (LER PRIMEIRO)

> **ATENCAO:** O agente DEVE criar esta todo list IMEDIATAMENTE apos ativar o contrato.
> **NENHUMA ACAO** pode ser executada antes da todo list existir.
> **COPIAR EXATAMENTE** o template abaixo, substituindo RFXXX pelo RF real.

### Template para RF Unico (RFXXX)

```
TODO LIST - Backend RFXXX
=========================

[pending] Ler anti-esquecimento PRIMEIRO
  +-- [pending] Ler D:\IC2\docs\anti-esquecimento-backend.md

[pending] Validacao Git Inicial (ANTES de criar branch)
  |-- [pending] git status (verificar estado limpo)
  |-- [pending] Verificar ausencia de merge conflicts no branch atual
  |-- [pending] Se merge conflicts existirem: PARAR, REPORTAR, AGUARDAR resolucao
  +-- [pending] Somente criar branch se Git estado limpo

[pending] Ler documentacao do RF
  |-- [pending] Ler RFXXX.md
  |-- [pending] Ler UC-RFXXX.md
  |-- [pending] Ler MD-RFXXX.md
  +-- [pending] Identificar entidades e regras de negocio

[pending] Validar pre-requisitos
  |-- [pending] Verificar ARCHITECTURE.md
  |-- [pending] Verificar CONVENTIONS.md
  +-- [pending] Identificar dependencias de dominio

[pending] Implementar Domain (se autorizado)
  |-- [pending] Criar entidade principal
  |-- [pending] Criar Value Objects (se necessario)
  +-- [pending] Definir regras de dominio

[pending] Implementar Application Layer
  |-- [pending] Criar Commands (Create, Update, Delete)
  |-- [pending] Criar Queries (GetById, GetList)
  |-- [pending] Criar Handlers
  |-- [pending] Criar Validators
  +-- [pending] Criar DTOs

[pending] Implementar Infrastructure
  |-- [pending] Criar Configuration (EF Core)
  |-- [pending] Criar Repository (se necessario)
  +-- [pending] Registrar no DI Container

[pending] Implementar Web Layer
  |-- [pending] Criar Controller/Endpoints
  |-- [pending] Configurar rotas
  +-- [pending] Documentar Swagger

[pending] Seeds Funcionais (OBRIGATORIO)
  |-- [pending] Garantir entidades dependentes
  |-- [pending] Criar permissoes da funcionalidade
  |-- [pending] Associar permissoes ao perfil developer
  |-- [pending] Registrar na Central de Modulos
  +-- [pending] Verificar seeds sao idempotentes

[pending] Mapear Dependencias Funcionais
  |-- [pending] Ler MD-RFXXX.md e identificar FKs
  |-- [pending] Identificar entidades pai
  |-- [pending] Listar endpoints das dependencias
  +-- [pending] Definir ordem de setup para testes

[pending] Validar Dependencias (Pre-Testes)
  |-- [pending] Para cada dependencia na ordem:
  |     |-- [pending] Verificar se endpoint existe
  |     |-- [pending] Testar CRUD basico
  |     +-- [pending] Se FALHAR: criar RELATORIO-ERROS-RFXXX.md
  +-- [pending] Se todas OK: prosseguir para testes do RF atual

[pending] Testes Automatizados (OBRIGATORIO)
  |-- [pending] Teste do Command principal (caminho feliz)
  |-- [pending] Teste da Query principal
  |-- [pending] Teste de validacao basica
  |-- [pending] Teste dos endpoints HTTP
  +-- [pending] Verificar 401/403/500 falham os testes

[pending] Validar Criterio de Pronto
  |-- [pending] Build backend OK (dotnet build)
  |-- [pending] Seeds aplicados com sucesso
  |-- [pending] Testes executados em ambiente limpo
  |-- [pending] Nenhuma dependencia manual
  +-- [pending] Nenhuma alteracao fora do escopo

[pending] Atualizar STATUS.yaml
  |-- [pending] execucao.backend = done
  +-- [pending] Verificar consistencia dos campos
```

### Regras de Execucao da Todo List

1. **COPIAR** o template acima ANTES de qualquer acao
2. Atualizar status em tempo real ([pending] → [in_progress] → [completed])
3. **NUNCA** pular etapas
4. **PARAR** em caso de falha (build error/test failure)
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
git checkout -b feature/RFXXX-backend
```

Ao concluir a implementacao:

```bash
# 3. Commit e merge em dev
git add .
git commit -m "feat(RFXXX): implementacao backend"
git checkout dev
git pull origin dev
git merge feature/RFXXX-backend
git push origin dev
```

> Referencia completa: `docs/devops/BRANCH-WORKFLOW.md`

---

## OBJETIVO

Implementar o backend da **funcionalidade alvo**
sem redefinir arquitetura, padrões ou regras existentes.

A implementação DEVE respeitar estritamente:

- `ARCHITECTURE.md`
- `CONVENTIONS.md`
- `CLAUDE.md`

Documentos externos (RF/UC/MD) são utilizados
**apenas como referência conceitual**.

A **fonte da verdade técnica** é:
- O código backend existente
- Os documentos em `/docs`

---

## ESCOPO FUNCIONAL

Inclui exclusivamente, quando aplicável:

- Commands, Queries, Handlers e Validators
- Endpoints HTTP correspondentes
- Ajustes pontuais de infraestrutura **somente se indispensáveis**

É **PROIBIDO**:
- Redefinir regras de negócio
- Introduzir abstrações reutilizáveis
- Alterar padrões arquiteturais
- Evoluir escopo funcional

---

## ZONAS PERMITIDAS

- `backend/IControlIT.API/src/Application/**`
- `backend/IControlIT.API/src/Web/**`
- `backend/IControlIT.API/src/Infrastructure/**` (somente se necessário)

---

## ZONAS PROIBIDAS

- `/docs/**`
- `Domain/**` (exceto se explicitamente autorizado)
- Código compartilhado existente
- Arquitetura base
- Refatorações não relacionadas ao escopo

---

## REGRAS GERAIS (INVIOLÁVEIS)

- Seguir estritamente:
  - `ARCHITECTURE.md`
  - `CONVENTIONS.md`
  - `CLAUDE.md`
- NÃO criar abstrações reutilizáveis
- NÃO alterar padrões existentes
- NÃO inferir requisitos
- Se precisar sair do escopo: **PARAR e AVISAR**
- Testes de backend têm objetivo de:
  - Validação funcional básica
  - Smoke tests
  - Caminho feliz
- Cobertura completa **NÃO** é exigida por este contrato

---

## ALTERAÇÕES PERMITIDAS NO BACKEND (LIMITADAS)

Permitidas **somente** para viabilizar acesso, execução e testes:

- Registro da funcionalidade na **Central de Módulos**
- Associação de permissões existentes a perfis existentes
- Criação ou ajuste de **seeds funcionais**
- Ajustes estritamente necessários para habilitar acesso
  a funcionalidades já implementadas

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
- Associação de permissões a perfis
- Usuário de teste funcional (ex: `developer`)

### REGRAS DE SEED

- Criar **SOMENTE** se não existirem
- Seeds **idempotentes**
- NÃO alterar dados produtivos
- Seeds existem apenas para habilitar execução e testes

### LOCAL DE SEED

- `DataInitializer`
- Seeders existentes
- Mecanismo de inicialização já adotado pelo projeto

### É PROIBIDO

- Criar seeds ad-hoc em handlers
- Criar seeds escondidos em testes
- Criar seeds temporários sem controle

---

## REEXECUÇÃO DE SEEDS (OBRIGATÓRIO)

O sistema DEVE permitir que seeds funcionais
sejam reaplicados de forma segura em ambientes
de desenvolvimento e teste, **sem exclusão manual do banco**.

Se o mecanismo atual **NÃO** permitir isso,
o agente DEVE:

- **PARAR**
- **ALERTAR**
- Explicar por que a reexecução não é possível
- Propor ajuste mínimo no mecanismo de seed
  (sem alterar arquitetura ou domínio)
- **AGUARDAR decisão**

---

## DEPENDENCIAS FUNCIONAIS (OBRIGATORIO)

Antes de executar os testes automatizados, o agente DEVE validar
todas as dependencias funcionais da entidade.

### Identificar Dependencias

Analisar MD-RFXXX.md e identificar:
- Foreign Keys (FKs) que apontam para outras entidades
- Entidades pai necessarias para criar a entidade principal
- Endpoints relacionados

### Validar Dependencias

Para CADA dependencia identificada:
1. Verificar se o endpoint existe
2. Testar CRUD basico
3. Se FALHAR: registrar erro

### Gerar Relatorio de Erros (se necessario)

Se QUALQUER dependencia falhar:
1. **PARAR** a execucao do RF atual
2. Criar arquivo `RELATORIO-ERROS-RFXXX.md` na pasta do RF
3. Listar todas as dependencias com erro
4. Sugerir contratos de manutencao
5. **NAO** marcar RF como concluido

### Criterio de Continuacao

O agente SO pode prosseguir para os testes do RF atual quando:
- TODAS as dependencias foram validadas com sucesso
- OU o usuario autorizou explicitamente continuar com dependencias quebradas

### Setup de Testes Obrigatorio

Os testes automatizados DEVEM criar dados na ordem correta:
1. Primeiro: entidades mais basicas (Empresa)
2. Depois: entidades intermediarias (Filial, Centro de Custo)
3. Por fim: entidade do RF atual (Departamento)

---

## VERIFICAÇÃO DE CONSISTÊNCIA EM RUNTIME (OBRIGATÓRIO)

Ao iniciar a aplicação em ambientes **DEV/TEST**,
o sistema DEVE validar:

- Existência das permissões exigidas pela funcionalidade
- Associação das permissões ao perfil esperado
- Existência do registro na Central de Módulos

Se qualquer item estiver ausente:

- A aplicação DEVE:
  - Logar erro explícito
  - Indicar exatamente o item faltante
  - Opcionalmente falhar o startup (fail-fast)
- O agente DEVE:
  - **PARAR**
  - **ALERTAR** que o ambiente está inconsistente

---

## CRITERIO DE PRONTO OBRIGATORIO

Para considerar o backend COMPLETO, DEVE atender:

- [ ] **100% dos UCs do UC-RFXXX implementados**
- [ ] **100% das RNs validadas**
- [ ] Backend funcionalmente completo (nao parcial)
- [ ] Build backend OK
- [ ] Seeds funcionais aplicados com sucesso
- [ ] Testes executados em ambiente limpo
- [ ] Nenhuma dependencia manual para execucao dos testes
- [ ] Testes automatizados executados com sucesso,
  cobrindo no minimo:
  - Execucao do Command principal (caminho feliz)
  - Execucao da Query principal
  - Validacao basica de regras (quando aplicavel)
  - Resposta correta dos endpoints HTTP
- [ ] Respostas HTTP **401, 403, 404 ou 500**
  DEVEM falhar os testes automaticamente
- [ ] Nenhuma alteracao fora do escopo ocorreu
- [ ] Pronto para passar pelo CONTRATO-VALIDACAO-BACKEND

⚠️ **ATENCAO CRITICA:** Este contrato NAO permite implementacao parcial.

**TODOS os UCs do UC-RFXXX devem estar implementados.**

**Cobertura parcial = REPROVADO**

**Qualquer ressalva = REPROVACAO**

---

## ANTI-ESQUECIMENTO (OBRIGATORIO)

⚠️ **LEITURA OBRIGATÓRIA NO INÍCIO:**

Antes de iniciar qualquer implementação, você DEVE ler:
- **D:\IC2\docs\anti-esquecimento-backend.md**

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

➡️ **CONTRATO-VALIDACAO-BACKEND** (docs/contracts/desenvolvimento/validacao/backend.md)

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
