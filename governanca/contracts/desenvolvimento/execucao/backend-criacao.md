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

## CONSULTA OBRIGATÓRIA À BASE DE CONHECIMENTO

Antes de criar a TODO LIST e iniciar qualquer implementação, o agente **DEVE**:

### 1. LER Base de Conhecimento Backend

```bash
# Ler arquivo completo
cat docs/base-conhecimento/backend.yaml
```

### 2. PROCURAR Problemas Similares

Verificar se há problemas conhecidos relacionados a:
- Tecnologias que serão usadas (EF Core, AutoMapper, CQRS, etc.)
- Padrões que serão aplicados (multi-tenancy, auditoria, etc.)
- Funcionalidades similares já implementadas

### 3. CONSULTAR Erros Comuns

Revisar seção `erros_comuns:` para antecipar problemas frequentes

### 4. VALIDAR Padrões Obrigatórios

Confirmar conhecimento dos padrões em `padroes:` antes de implementar

### 5. EXECUTAR Checklist Pré-Execução

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
    sintoma: "Mensagem de erro ou comportamento observado"
    causa_raiz: "Análise técnica do por quê"
    solucao: |
      Passo a passo da solução:
      1. Primeiro passo
      2. Segundo passo
      3. Código exemplo (se aplicável)
    arquivos_afetados:
      - "backend/caminho/arquivo.cs"
    data_registro: "YYYY-MM-DD"
    tags: [categoria, tecnologia, padrao]
```

**AÇÃO OBRIGATÓRIA:**
- Adicionar novo problema ao final de `problemas:` em `docs/base-conhecimento/backend.yaml`
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
- Padrões arquiteturais (CQRS, Clean Architecture, DDD)
- Escolhas de tecnologia (EF Core, AutoMapper, MediatR)
- Regras de negócio globais (multi-tenancy, auditoria)
- Decisões anteriores que impactam o RF atual

**Declaração obrigatória:**
> "DECISIONS.md consultado: [N] decisões técnicas revisadas"

### 2. IDENTIFICAÇÃO DE DECISÕES IMPLÍCITAS (Durante Implementação)

Durante implementação, o agente **DEVE PARAR e ALERTAR** quando identificar:

#### Situações que exigem registro em DECISIONS.md:

**a) Escolha entre abordagens técnicas equivalentes**
- Exemplo: "Usar AutoMapper vs mapear manualmente"
- Exemplo: "Repository pattern vs acesso direto ao DbContext"

**b) Desvio de padrão existente**
- Exemplo: "Handler sem validação explícita (diferente do padrão)"
- Exemplo: "Quebrar regra de multi-tenancy para caso específico"

**c) Trade-offs relevantes**
- Exemplo: "Performance vs manutenibilidade"
- Exemplo: "Complexidade vs flexibilidade"

**d) Decisões difíceis de reverter**
- Exemplo: "Estrutura de migration (mudança de schema)"
- Exemplo: "Mudança em contrato de API pública"

**e) Introdução de nova dependência**
- Exemplo: "Adicionar pacote NuGet não utilizado antes"
- Exemplo: "Integração com serviço externo"

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

**Exemplo 1: Escolha de Padrão de Mapeamento**
```
ADR-015: Usar AutoMapper para todos os DTOs

Contexto: RF028 precisa mapear entre entidades e DTOs
Decisão: Usar AutoMapper com profiles configurados
Alternativa rejeitada: Mapear manualmente (mais verboso, menos DRY)
Consequência: +1 dependência, -código boilerplate
```

**Exemplo 2: Exceção à Regra de Multi-Tenancy**
```
ADR-016: Tabela de Configurações Globais sem ClienteId

Contexto: RF030 precisa de configurações compartilhadas entre todos os clientes
Decisão: Criar tabela GlobalSettings SEM ClienteId
Alternativa rejeitada: Duplicar configurações por cliente (redundante)
Consequência: Quebra padrão multi-tenancy, requer controle de acesso especial
```

### 6. DECISÕES QUE NÃO PRECISAM SER REGISTRADAS

**NÃO registrar:**
- ❌ Aplicação de padrão já estabelecido em ARCHITECTURE.md
- ❌ Seguir convenção já definida em CONVENTIONS.md
- ❌ Decisões triviais (nome de variável, formatação)
- ❌ Decisões reversíveis sem impacto (refactoring local)

**Registrar:**
- ✅ Exceções a padrões estabelecidos
- ✅ Introdução de novos padrões
- ✅ Escolhas com trade-offs significativos
- ✅ Decisões que afetam múltiplos RFs

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
  |-- [pending] NOVO: Verificar schema.sql existe (para testes funcionais)
  |     |-- [pending] Caminho: D:\IC2\backend\IControlIT.API\tests\schema.sql
  |     +-- [pending] Se NAO existe: reportar bloqueio (testes funcionais pulados)
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

- `D:\IC2\backend\IControlIT.API/src/Application/**`
- `D:\IC2\backend\IControlIT.API/src/Web/**`
- `D:\IC2\backend\IControlIT.API/src/Infrastructure/**` (somente se necessário)

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

## FASE 7.5: TESTES UNITÁRIOS OBRIGATÓRIOS (NOVO - BLOQUEANTE)

**Este passo é OBRIGATÓRIO. Sem ele, backend está INCOMPLETO.**

### Contexto

Esta fase foi adicionada após análise de problemas identificados no RF006, onde a ausência de testes unitários desde o início resultou em:
- Backend aprovado SEM testes unitários
- Descoberta de bugs apenas em testes E2E (tardiamente)
- Retrabalho para adicionar testes após implementação completa
- Falta de validação de regras de negócio durante desenvolvimento

### Objetivo

Garantir que **TODOS os Commands e Queries** possuem testes unitários ANTES de marcar backend como concluído.

### PASSO 7.5.1: Criar Testes Unitários para Commands

**Para CADA Command criado** (Create, Update, Delete, etc.), o agente DEVE criar testes unitários cobrindo:

#### 1. Teste de Sucesso (Happy Path)

**Cenário:** Dados válidos fornecidos ao Command
**Resultado esperado:** Command retorna `Success` com resultado esperado

**Exemplo:**
```csharp
// backend/tests/Application.Tests/Features/Clientes/Commands/CreateClienteCommandTests.cs

public class CreateClienteCommandTests
{
    [Fact]
    public async Task CreateCliente_ComDadosValidos_DeveRetornarSucesso()
    {
        // Arrange
        var command = new CreateClienteCommand
        {
            RazaoSocial = "Cliente Teste Ltda",
            CNPJ = "12.345.678/0001-90",
            Email = "contato@clienteteste.com"
        };

        var handler = new CreateClienteCommandHandler(_context, _mapper);

        // Act
        var result = await handler.Handle(command, CancellationToken.None);

        // Assert
        Assert.True(result.Succeeded);
        Assert.NotNull(result.Data);
        Assert.Equal("Cliente Teste Ltda", result.Data.RazaoSocial);
    }
}
```

#### 2. Teste de Validação (FluentValidation)

**Cenário:** Dados inválidos fornecidos ao Command
**Resultado esperado:** Validator retorna erros de validação

**Exemplo:**
```csharp
[Fact]
public void CreateCliente_ComRazaoSocialVazia_DeveFalhar()
{
    // Arrange
    var command = new CreateClienteCommand
    {
        RazaoSocial = "",  // INVÁLIDO
        CNPJ = "12.345.678/0001-90",
        Email = "contato@clienteteste.com"
    };

    var validator = new CreateClienteCommandValidator();

    // Act
    var result = validator.Validate(command);

    // Assert
    Assert.False(result.IsValid);
    Assert.Contains(result.Errors, e => e.PropertyName == "RazaoSocial");
}
```

#### 3. Teste de Regra de Negócio

**Cenário:** Violação de RN (ex: CNPJ duplicado)
**Resultado esperado:** Command retorna `Failure` com mensagem específica

**Exemplo:**
```csharp
[Fact]
public async Task CreateCliente_ComCNPJDuplicado_DeveRetornarErro()
{
    // Arrange
    // Criar cliente com CNPJ X
    await _context.Clientes.AddAsync(new Cliente
    {
        RazaoSocial = "Cliente Existente",
        CNPJ = "12.345.678/0001-90"
    });
    await _context.SaveChangesAsync();

    // Tentar criar outro cliente com mesmo CNPJ
    var command = new CreateClienteCommand
    {
        RazaoSocial = "Cliente Novo",
        CNPJ = "12.345.678/0001-90"  // DUPLICADO
    };

    var handler = new CreateClienteCommandHandler(_context, _mapper);

    // Act
    var result = await handler.Handle(command, CancellationToken.None);

    // Assert
    Assert.False(result.Succeeded);
    Assert.Contains("CNPJ já cadastrado", result.Messages);
}
```

**Localização dos testes:**
```
D:\IC2\backend\tests\Application.Tests\Features\[Entidade]\Commands\[Command]Tests.cs
```

### PASSO 7.5.2: Criar Testes Unitários para Queries

**Para CADA Query criada** (GetAll, GetById, etc.), o agente DEVE criar testes unitários cobrindo:

#### 1. Teste de Sucesso (Retorno de Dados)

**Exemplo:**
```csharp
// backend/tests/Application.Tests/Features/Clientes/Queries/GetClientesQueryTests.cs

public class GetClientesQueryTests
{
    [Fact]
    public async Task GetClientes_ComDadosExistentes_DeveRetornarLista()
    {
        // Arrange
        await _context.Clientes.AddRangeAsync(
            new Cliente { RazaoSocial = "Cliente 1" },
            new Cliente { RazaoSocial = "Cliente 2" }
        );
        await _context.SaveChangesAsync();

        var query = new GetClientesQuery();
        var handler = new GetClientesQueryHandler(_context, _mapper);

        // Act
        var result = await handler.Handle(query, CancellationToken.None);

        // Assert
        Assert.True(result.Succeeded);
        Assert.Equal(2, result.Data.Count);
    }
}
```

#### 2. Teste de Retorno Vazio

**Exemplo:**
```csharp
[Fact]
public async Task GetClientes_SemDados_DeveRetornarListaVazia()
{
    // Arrange
    var query = new GetClientesQuery();
    var handler = new GetClientesQueryHandler(_context, _mapper);

    // Act
    var result = await handler.Handle(query, CancellationToken.None);

    // Assert
    Assert.True(result.Succeeded);
    Assert.Empty(result.Data);
}
```

### PASSO 7.5.3: Estrutura de Testes Obrigatória

**O agente DEVE criar:**

```
D:\IC2\backend\tests\Application.Tests\
├── Features\
│   └── [Entidade]\
│       ├── Commands\
│       │   ├── Create[Entidade]CommandTests.cs
│       │   ├── Update[Entidade]CommandTests.cs
│       │   └── Delete[Entidade]CommandTests.cs
│       └── Queries\
│           ├── Get[Entidade]sQueryTests.cs
│           └── Get[Entidade]ByIdQueryTests.cs
└── Common\
    └── TestBase.cs  (helper para setup de testes)
```

### PASSO 7.5.4: Executar Testes

**O agente DEVE:**

1. **Rodar testes unitários:**
   ```bash
   cd D:\IC2\backend
   dotnet test tests/Application.Tests/Application.Tests.csproj
   ```

2. **Validar resultado:**
   - Taxa de aprovação: **100%**
   - Nenhum teste falhando
   - Nenhum teste ignorado

**SE testes FALHAREM:**
- ❌ BLOQUEIO: Backend NÃO pode ser marcado como concluído
- ❌ Corrigir falhas e re-executar
- ❌ NÃO prosseguir até todos os testes passarem

### PASSO 7.5.5: Documentar Cobertura

**O agente DEVE atualizar STATUS.yaml:**

```yaml
desenvolvimento:
  backend:
    status: completed
    testes_implementados:
      - "CreateClienteCommandTests.cs (3 testes: sucesso, validação, RN)"
      - "UpdateClienteCommandTests.cs (3 testes)"
      - "DeleteClienteCommandTests.cs (2 testes)"
      - "GetClientesQueryTests.cs (2 testes: com dados, vazio)"
      - "GetClienteByIdQueryTests.cs (2 testes: encontrado, não encontrado)"
    cobertura_testes: "5/5 Commands/Queries com testes (100%)"
    taxa_aprovacao_testes: "12/12 testes passando (100%)"
```

### PASSO 7.5.6: Validar Cobertura Completa

**Verificar:**

- ✅ **TODOS** os Commands possuem testes (Create, Update, Delete, etc.)
- ✅ **TODOS** os Queries possuem testes (GetAll, GetById, etc.)
- ✅ **TODOS** os testes estão passando 100%
- ✅ Testes cobrem:
  - Happy path (sucesso)
  - Validação (FluentValidation)
  - Regras de negócio (RNs)
  - Casos de erro (não encontrado, duplicado, etc.)

**SE qualquer Command/Query NÃO possui testes:**
- ❌ Backend está INCOMPLETO
- ❌ BLOQUEIO: Não marcar como concluído

### CRITÉRIO DE APROVAÇÃO (Fase 7.5)

- ✅ Cobertura: **100%** dos Commands/Queries possuem testes
- ✅ Taxa de aprovação: **100%** dos testes passando
- ✅ Testes cobrem happy path + validação + RNs
- ✅ STATUS.yaml documentado com cobertura completa
- ✅ Comando executado: `dotnet test` retorna exit code 0

**Justificativa:**
- **Gap identificado:** Backend aprovado SEM testes → bugs descobertos tardiamente em E2E
- **Impacto:** Sem testes unitários, RNs não são validadas durante desenvolvimento
- **Solução:** Tornar testes unitários OBRIGATÓRIOS desde criação do backend
- **Resultado esperado:** Bugs detectados ANTES de testes E2E, reduzindo retrabalho

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

➡️ **CONTRATO-VALIDACAO-BACKEND** (contracts/desenvolvimento/validacao/backend.md)

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
