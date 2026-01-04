# CONTRATO DE REGULARIZACAO DE BACKEND (Adequacao)

Este contrato regula a adaptacao de backends legados
para o modelo de governanca atual.

**IMPORTANTE:** Este contrato exige cobertura 100% dos UCs.

---

## OBJETIVO

- Alinhar backend existente aos RFs
- Corrigir lacunas de implementacao
- **IMPLEMENTAR 100% DOS UCs** (adequar existente + completar faltante)
- Preparar o backend para validacao (CONTRATO-VALIDACAO-BACKEND)
- Preservar compatibilidade com frontends existentes

---

## O QUE ESTE CONTRATO PERMITE

- Completar validacoes faltantes
- Implementar regras documentadas no RF
- **Implementar UCs faltantes** (completar ate 100%)
- Corrigir inconsistencias com MD
- Ajustar seeds e permissoes
- Ajustar testes basicos

---

## O QUE ESTE CONTRATO PROIBE

- Criar novas funcionalidades FORA do UC-RFXXX
- Alterar payloads publicos sem justificativa
- Quebrar frontends existentes
- Refatorar arquitetura
- Executar testes de violacao

---

## METODO DE TRABALHO

1. Ler UC-RFXXX.yaml completo (TODOS os UCs)
2. Auditar backend atual vs UC
3. Identificar gaps (o que falta implementar)
4. **Adequar o que ja existe** (corrigir divergencias)
5. **Implementar o que falta** (completar ate 100%)
6. Garantir funcionamento atual preservado
7. Preparar para validacao

**NAO CRIAR AUDITORIAS LONGAS. Criar TODO list e executar.**

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

## TODO LIST OBRIGATORIA (COPIAR EXATAMENTE)

> **ATENCAO:** O agente DEVE criar esta todo list IMEDIATAMENTE apos ativar o contrato.
> **NENHUMA ACAO** pode ser executada antes da todo list existir.
> **COPIAR EXATAMENTE** o template abaixo, substituindo RFXXX pelo RF real.

### Template para RF Unico (RFXXX)

```
TODO LIST - Backend Adequacao RFXXX
===================================

[pending] Ler anti-esquecimento PRIMEIRO
  +-- [pending] Ler D:\IC2\docs\anti-esquecimento-backend.md

[pending] Validacao Git Inicial (ANTES de criar branch)
  |-- [pending] git status (verificar estado limpo)
  |-- [pending] Verificar ausencia de merge conflicts no branch atual
  |-- [pending] Se merge conflicts existirem: PARAR, REPORTAR, AGUARDAR resolucao
  +-- [pending] Somente criar branch se Git estado limpo

[pending] Ler documentacao completa
  |-- [pending] Ler RFXXX.yaml
  |-- [pending] Ler UC-RFXXX.yaml (TODOS os UCs)
  |-- [pending] Ler MD-RFXXX.yaml
  +-- [pending] Identificar TODOS os UCs que devem existir

[pending] Auditar backend atual
  |-- [pending] Listar Commands/Queries existentes
  |-- [pending] Listar Endpoints existentes
  |-- [pending] Mapear UCs cobertos
  +-- [pending] Identificar UCs FALTANTES

[pending] Adequar backend existente
  |-- [pending] Corrigir validacoes faltantes
  |-- [pending] Corrigir inconsistencias com MD
  |-- [pending] Ajustar DTOs se necessario
  +-- [pending] Ajustar Seeds e Permissoes

[pending] Implementar UCs faltantes
  |-- [pending] Para cada UC faltante:
  |     |-- [pending] Criar Commands/Queries
  |     |-- [pending] Criar Handlers
  |     |-- [pending] Criar Validators
  |     |-- [pending] Criar Endpoints
  |     +-- [pending] Criar testes basicos
  +-- [pending] Garantir 100% dos UCs implementados

[pending] Executar smoke tests
  |-- [pending] dotnet build
  |-- [pending] dotnet ef database update
  +-- [pending] Testar caminho feliz de cada UC

[pending] Validar criterio de pronto
  |-- [pending] 100% dos UCs implementados
  |-- [pending] Backend builda sem erros
  |-- [pending] Seeds aplicados corretamente
  |-- [pending] Frontend existente funcional
  +-- [pending] Pronto para CONTRATO-VALIDACAO-BACKEND

[pending] Atualizar STATUS.yaml
  |-- [pending] execucao.backend = done
  +-- [pending] Verificar consistencia dos campos
```

---

## AUTONOMIA TOTAL DO AGENTE (EXECUCAO IMEDIATA E COMPLETA)

O agente POSSUI AUTONOMIA TOTAL e DEVE EXECUTAR IMEDIATAMENTE:

**PROIBIDO PERGUNTAR:**
- ❌ "Você quer que eu continue?"
- ❌ "Devo implementar todos os UCs agora?"
- ❌ "Prefere fazer em fases?"
- ❌ "Qual opção você escolhe?"
- ❌ QUALQUER pergunta sobre escopo ou priorização

**EXECUCAO OBRIGATORIA:**
- ✅ Implementar **TODOS** os UCs faltantes (100%)
- ✅ Corrigir **TODAS** as divergências com UC/MD
- ✅ Adicionar **TODAS** as validações faltantes
- ✅ Criar **TODOS** os testes necessários
- ✅ Deixar backend **100% PRONTO**
- ✅ Build passando
- ✅ Testes passando
- ✅ UC coberto 100%

**REGRA ABSOLUTA:**

Adequacao = **100% de execucao IMEDIATA**

Nao existe "fazer parte agora e parte depois".
Nao existe "implementar apenas os UCs criticos".
Nao existe "aguardar decisao do usuario".

**O agente EXECUTA TUDO ate 100% sem perguntar.**

Se o agente perguntar algo relacionado a escopo, priorização ou continuação:
➡️ **VIOLACAO DO CONTRATO**

### Regras de Execucao

**E PROIBIDO:**
- Perguntar ao usuario se pode buildar/testar
- Esperar que usuario execute comandos manualmente
- Entregar backend parcialmente implementado
- **Criar "relatórios de gaps" com opções/perguntas**
- **Oferecer "Opção A, B ou C" ao usuário**
- **Parar no meio da execução para "aguardar decisão"**
- **Criar commits intermediários e perguntar "continuo?"**

**E OBRIGATORIO:**
- Executar todos os comandos necessarios autonomamente
- Deixar backend buildando ANTES de iniciar adequacao
- Deixar backend buildando e testado AO FINAL da adequacao
- Garantir 100% dos UCs implementados
- **Executar TUDO até 100% sem pausas**
- **Criar um UNICO commit ao final com TUDO pronto**
- **NÃO criar relatórios com "próximos passos" - FAZER os próximos passos**

**Filosofia:**

> O usuario deixa o backend funcionando.
> O agente DEVE deixar o backend funcionando.
> **Ninguém escolhe "opções" - o agente EXECUTA até 100%.**

---

## ANTI-ESQUECIMENTO (OBRIGATORIO)

⚠️ **LEITURA OBRIGATÓRIA NO INÍCIO:**

Antes de iniciar qualquer implementação, você DEVE ler:
- **D:\IC2\docs\anti-esquecimento-backend.md**

Este documento contém os "esquecimentos" mais comuns que devem ser evitados.

A leitura está incluída como PRIMEIRO item do TODO list.

---

## CRITERIO DE PRONTO OBRIGATORIO

Para considerar a adequacao COMPLETA, o backend DEVE:

- [ ] **100% dos UCs do UC-RFXXX implementados**
- [ ] **100% das RNs validadas**
- [ ] Backend funcionalmente completo (nao parcial)
- [ ] Pronto para passar pelo contrato de validacao (CONTRATO-VALIDACAO-BACKEND)

⚠️ **ATENCAO:** Este contrato NÃO permite implementação parcial.

Se o backend atual cobre 70% dos UCs, este contrato DEVE implementar os 30% restantes.

**Cobertura parcial = REPROVADO**

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
