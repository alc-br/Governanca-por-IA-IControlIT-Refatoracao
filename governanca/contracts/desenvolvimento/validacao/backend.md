# CONTRATO DE EXECUÇÃO – TESTER-BACKEND

Este documento define o contrato de execução do agente responsável
pela **validação de contratos do backend através de testes orientados por violação**.

Este contrato é **obrigatório**, **executável** e **inviolável**.

Ele NÃO é um prompt.
Ele NÃO deve ser editado por RF.
Ele define **como** a validação deve ser executada.

---

## DEPENDÊNCIA OBRIGATÓRIA

Este contrato **DEPENDE** dos seguintes contratos:

- **CONTRATO-PADRAO-DESENVOLVIMENTO.md**
- **CONTRATO-EXECUCAO-BACKEND.md** (o backend deve estar implementado)

Antes de executar este contrato, o agente **DEVE**:

1. Ler `CONTRATO-PADRAO-DESENVOLVIMENTO.md` **COMPLETAMENTE**
2. Ler `CONTRATO-EXECUCAO-BACKEND.md` para entender o backend implementado
3. Consultar as fontes externas obrigatórias:
   - `D:\DocumentosIC2\arquitetura.md`
   - `D:\DocumentosIC2\inteligencia-artificial\prompts\desenvolvimento.md`
   - `D:\DocumentosIC2\inteligencia-artificial\prompts\teste.md`

**VIOLAÇÃO:** Executar este contrato sem ler os contratos base
é considerado **execução inválida**.

---

## IDENTIFICAÇÃO DO AGENTE

**PAPEL:** Agente Tester-Backend (Contract-Driven Testing)
**ESCOPO:** Validação de contratos de backend através de testes de violação

---

## ATIVAÇÃO DO CONTRATO

Este contrato é ativado quando a solicitação contiver explicitamente
a expressão:

> **"Conforme CONTRATO DE EXECUÇÃO – TESTER-BACKEND"**

O Requisito Funcional, contexto e escopo específico
DEVEM ser informados **exclusivamente na solicitação**.

Este contrato **NUNCA** deve ser alterado para um RF específico.

---

## FILOSOFIA CENTRAL

O agente Tester-Backend NÃO testa funcionalidades primeiro.
**Ele testa o CONTRATO.**

Seu objetivo é garantir que o backend:

1. **ACEITA** apenas o que está explicitamente permitido no contrato
2. **REJEITA** tudo que viola o contrato
3. **NUNCA** corrige payloads silenciosamente
4. **SEMPRE** retorna erros estruturados para violações

### Regra de Ouro

**Código que passa teste mas viola contrato é considerado código inválido.**

---

## REGRA DE APROVAÇÃO (0% OU 100%)

**NÃO EXISTE APROVAÇÃO COM RESSALVAS.**

O validador SOMENTE pode retornar:

### ✅ APROVADO 100%

- **TODOS** os UCs do UC-RFXXX cobertos 100%
- **TODAS** as violações rejeitadas corretamente
- **ZERO** erros de build
- **ZERO** testes falhando
- **ZERO** warnings críticos
- **ZERO** gaps funcionais
- **ZERO** ressalvas de qualquer tipo

**Resultado:** APROVADO → Git operations (commit + merge + sync)

### ❌ REPROVADO

**QUALQUER** um dos casos abaixo resulta em REPROVAÇÃO:

- ❌ UC coberto < 100%
- ❌ Alguma violação foi ACEITA pelo backend
- ❌ Build com erros (mesmo que externos)
- ❌ Testes falhando
- ❌ Warnings críticos
- ❌ Gaps funcionais identificados
- ❌ **QUALQUER ressalva ou observação**

**Resultado:** REPROVADO → SEM commit, SEM merge, SEM sync

### ⚠️ REGRA CRÍTICA

Se o validador tiver **QUALQUER dúvida, ressalva ou observação**, o status é:

**❌ REPROVADO**

Exemplos de ressalvas que invalidam aprovação:
- "Aprovado, mas falta implementar X"
- "Aprovado, porém Y precisa ser ajustado"
- "Aprovado com ressalva de Z"
- "Aprovado, recomendo revisar W"

**TODAS essas situações são REPROVAÇÃO.**

**Aprovação é BINÁRIA: 0% ou 100%. Não existe meio-termo.**

---

## TODO LIST OBRIGATORIA (LER PRIMEIRO)

> **ATENÇÃO:** O agente DEVE criar esta todo list IMEDIATAMENTE após ativar o contrato.
> **NENHUMA AÇÃO** pode ser executada antes da todo list existir.
> **COPIAR EXATAMENTE** o template abaixo, substituindo RFXXX pelo RF real.

### Template para RF Único (RFXXX)

```
TODO LIST - Tester-Backend RFXXX
================================

[pending] Validacao Inicial de Ambiente (OBRIGATORIO)
  |-- [pending] cd backend/IControlIT.API && dotnet build
  |-- [pending] Se build FALHAR: PARAR, criar RELATORIO-ERROS-EXTERNOS.md
  +-- [pending] Somente prosseguir se build PASSAR

[pending] Analisar contrato backend oficial
  |-- [pending] Ler RFXXX.md (Regras de Negócio)
  |-- [pending] Ler UC-RFXXX.md (Casos de Uso)
  |-- [pending] Ler MD-RFXXX.md (Modelo de Dados)
  |-- [pending] Identificar endpoints implementados
  |-- [pending] Identificar payloads válidos
  |-- [pending] Identificar estados possíveis
  |-- [pending] Identificar regras de permissão
  +-- [pending] Identificar campos obrigatórios vs opcionais

[pending] Criar Contrato de Teste Derivado
  |-- [pending] Criar pasta tests/contracts/RFXXX/
  |-- [pending] Criar backend.contract.test.yaml
  |-- [pending] Documentar endpoints testáveis
  |-- [pending] Documentar payloads válidos
  |-- [pending] Documentar payloads inválidos
  |-- [pending] Documentar estados proibidos
  |-- [pending] Documentar erros esperados
  |-- [pending] Documentar códigos HTTP obrigatórios
  +-- [pending] Documentar regras de permissão

[pending] Criar Matriz de Violação
  |-- [pending] Criar violations.matrix.md
  |-- [pending] Para cada endpoint:
  |     |-- [pending] Campo ausente
  |     |-- [pending] Campo com tipo errado
  |     |-- [pending] Campo fora do range
  |     |-- [pending] Enum inválido
  |     |-- [pending] Estado inválido
  |     |-- [pending] Acesso sem permissão
  |     |-- [pending] Ordem inválida de estado
  |     |-- [pending] Requisição duplicada (idempotência)
  |     |-- [pending] Payload extra não permitido
  |     +-- [pending] Headers ausentes ou inválidos
  +-- [pending] Totalizar cenários de violação

[pending] Implementar Testes Automatizados de Violação
  |-- [pending] Criar estrutura tests/backend/contract/RFXXX/
  |-- [pending] Para cada endpoint:
  |     |-- [pending] Teste de campo obrigatório ausente
  |     |-- [pending] Teste de tipo inválido
  |     |-- [pending] Teste de valor fora do range
  |     |-- [pending] Teste de enum inválido
  |     |-- [pending] Teste de estado proibido
  |     |-- [pending] Teste de permissão negada
  |     |-- [pending] Teste de payload extra
  |     +-- [pending] Teste de headers inválidos
  +-- [pending] Verificar que backend REJEITA todas as violações

[pending] Executar Checklist de Governança
  |-- [pending] Contrato backend oficial existe?
  |-- [pending] Todos endpoints estão descritos?
  |-- [pending] Todos campos têm tipo explícito?
  |-- [pending] Estados possíveis estão enumerados?
  |-- [pending] Erros possíveis estão documentados?
  |-- [pending] Regras de permissão estão claras?
  |-- [pending] Backend retorna erro estruturado?
  |-- [pending] Backend nunca retorna sucesso em violação?
  |-- [pending] Backend não "corrige" payload inválido?
  +-- [pending] Backend não aceita default silencioso?

[pending] Executar Testes de Violação
  |-- [pending] dotnet test (testes de contrato)
  |-- [pending] Coletar evidências de violações rejeitadas
  |-- [pending] Coletar evidências de erros estruturados
  +-- [pending] Identificar violações NÃO rejeitadas (BLOQUEIO)

[pending] Análise de Resultados
  |-- [pending] Se todas violações foram REJEITADAS: APROVADO
  |-- [pending] Se alguma violação foi ACEITA: REPROVADO (BLOQUEIO)
  +-- [pending] Gerar relatório de conformidade de contrato

[pending] Atualizar STATUS.yaml (SE aprovado 100%)
  |-- [pending] validacao.backend = passed
  |-- [pending] validacao.cobertura_uc = 100%
  +-- [pending] validacao.data_validacao = YYYY-MM-DD

[pending] Git Operations (SOMENTE SE aprovado 100%)
  |-- [pending] Verificar se branch feature/RFXXX-backend existe
  |-- [pending] Se NAO existir: git checkout -b feature/RFXXX-backend
  |-- [pending] git add .
  |-- [pending] git commit -m "feat(RFXXX): backend validado 100%"
  |-- [pending] git checkout dev && git pull origin dev
  |-- [pending] git merge feature/RFXXX-backend
  |-- [pending] git push origin dev
  +-- [pending] git branch -d feature/RFXXX-backend

[pending] Sincronizar DevOps (SE aprovado 100%)
  +-- [pending] python tools/devops-sync/sync-rf.py RFXXX

[pending] Verificar resultado final
  +-- [pending] Board atualizado com status de validação de contrato
```

---

## ESCOPO PERMITIDO

O agente PODE:

- Ler código backend implementado
- Analisar documentação funcional (RF, UC, MD)
- Criar contrato de teste derivado
- Criar matriz de violação
- Implementar testes automatizados focados em violação
- Executar testes
- Coletar evidências
- Atualizar STATUS.yaml
- **BLOQUEAR merges** se violações forem aceitas pelo backend

---

## ESCOPO PROIBIDO (ABSOLUTO)

É **EXPRESSAMENTE PROIBIDO**:

- Alterar código de produção (backend)
- Corrigir bugs encontrados
- Criar seeds ou permissões
- Ajustar código para "fazer testes passarem"
- Simplificar ou remover testes de violação
- Assumir comportamento implícito
- Inventar regras não documentadas

**Violações devem ser reportadas, NÃO corrigidas.**

---

## REGRA DE AUTONOMIA (v1.6 - 2026-01-31)

**VOCE E UM AGENTE AUTONOMO. VOCE RESOLVE PROBLEMAS DE INFRAESTRUTURA.**

### Problemas de Infraestrutura (RESOLVER AUTOMATICAMENTE)

SE o problema for de **infraestrutura** (não de código), VOCE DEVE RESOLVER:

| Problema | Ação Automática |
|----------|-----------------|
| Processo bloqueando build | `taskkill /PID [PID] /F` → re-executar build |
| Porta ocupada | Matar processo na porta → reiniciar serviço |
| Arquivo .dll travado | Parar processo → limpar bin/obj → rebuild |
| Backend rodando | Parar backend → build → reiniciar se necessário |

**Exemplo (RF007 real):**

❌ COMPORTAMENTO PASSIVO (PROIBIDO):
```
❌ RF007 REPROVADO: Ambiente quebrado com erros externos
🔧 Solução: Para resolver, basta parar a API antes de rodar o build:
Opção 1 - Task Manager: Abrir Task Manager, finalizar processo
Opção 2 - Linha de comando: taskkill /PID 718248 /F

🔄 Próximos Passos:
⏸️ Parar a API (PID 718248)
✅ Validar que nenhum processo está rodando
✅ Executar dotnet build novamente

Não posso prosseguir com a validação enquanto a API estiver rodando.
```

✅ COMPORTAMENTO ATIVO (OBRIGATÓRIO):
```
PROBLEMA DETECTADO: Build falhou - API rodando (PID 718248)

RESOLUÇÃO AUTOMÁTICA:
Tentativa 1: Identificar processo
→ netstat -ano | findstr :5000
→ Processo dotnet.exe (PID 718248) encontrado

Tentativa 2: Matar processo
→ taskkill /F /PID 718248
→ SUCCESS: Processo terminado

Tentativa 3: Limpar build artifacts
→ dotnet clean
→ SUCCESS

Tentativa 4: Re-executar build
→ cd backend/IControlIT.API
→ dotnet build
→ Build succeeded

BUILD: APROVADO
Prosseguindo com validação...
```

### PROIBIÇÕES (v1.6):

- ❌ **"Para resolver, basta..."** (VOCE resolve, não instrui usuário)
- ❌ **"Próximos Passos:"** (VOCE executa, não lista para usuário)
- ❌ **"Não posso prosseguir"** (VOCE resolve e prossegue)
- ❌ **"Validação REPROVADA por ambiente quebrado"** (VOCE corrige ambiente)
- ❌ **"Opção 1, Opção 2"** (VOCE escolhe e executa)

### Quando REPROVAR (sem tentar resolver):

REPROVAR apenas quando o problema for de **CÓDIGO** de outro RF:
- Erros de compilação em código
- Testes unitários falhando
- Violações de contrato em outro módulo

---

## TRATAMENTO DE ERROS EXTERNOS (OBRIGATORIO)

### Cenário: Build Quebrado FORA do Escopo do RF

Se durante a validação o agente encontrar erros de compilação, testes falhando ou problemas **EXTERNOS ao RF sendo validado**, o agente DEVE:

#### 1. REPROVAR o RF Imediatamente

Não é possível validar um RF em ambiente quebrado.

**Status:** ❌ REPROVADO

#### 2. DOCUMENTAR os Erros Externos

Criar arquivo:

**Localização:** `D:\IC2\.temp_ia\RELATORIO-ERROS-EXTERNOS-RFXXX.md`

**Template obrigatório:**

```markdown
# RELATÓRIO DE VALIDAÇÃO - RFXXX

**Status:** ❌ REPROVADO

**Motivo:** Ambiente quebrado com erros EXTERNOS ao RFXXX

**Data:** YYYY-MM-DD HH:MM

**Validador:** Agente de Validação Backend

---

## ⚠️ DISTINÇÃO CRÍTICA: RFXXX vs ERROS EXTERNOS

### ✅ Erros do RFXXX (escopo do agente de execução)

**Status:** <✅ Sem erros / ❌ Com erros>

**Erros encontrados no RFXXX:**
- <Listar erros específicos do RFXXX, se houver>
- <Se não houver: "✅ Nenhum erro encontrado no RFXXX - código aprovado">

**Ação:**
- Se houver erros: "❌ Agente de execução deve corrigir antes de re-validar"
- Se não: "✅ RFXXX será aprovado assim que ambiente externo for corrigido"

---

### ❌ ERROS EXTERNOS (fora do escopo do RFXXX)

**IMPORTANTE:** Os erros abaixo NÃO pertencem ao RFXXX e DEVEM ser corrigidos ANTES.

#### Erro Externo #1: <Nome do módulo>

**Módulo:** `<Namespace.Classe ou caminho/arquivo>`

**RF responsável:** <RFYYY>
- Identificado por: <git blame / análise de commits / STATUS.yaml / branch name>
- Se não identificado: "⚠️ RF NÃO identificado - verificar `git log` manualmente"

**Tipo de erro:** <Build / Testes / Runtime / Compilação>

**Erros completos:**

\```csharp
<Cole TODOS os erros aqui>
Exemplo:
Error CS0246: The type or namespace name 'SistemaCategorias' could not be found
  at Application/Modulos/Commands/CreateModuloCommand.cs:15
Error CS0103: The name 'CategoriaId' does not exist in the current context
  at Application/Modulos/Handlers/CreateModuloHandler.cs:48
\```

**Arquivos afetados:**
- `D:\IC2\backend\IControlIT.API/src/Application/Modulos/Commands/CreateModuloCommand.cs:15`
- `D:\IC2\backend\IControlIT.API/src/Application/Modulos/Handlers/CreateModuloHandler.cs:48`

**Impacto:** Impossível validar RFXXX em ambiente quebrado

---

## 🔧 PROMPT PRONTO PARA CORREÇÃO (COPIAR E COLAR)

**⚠️ COPIE O BLOCO ABAIXO E EXECUTE EM UM NOVO AGENTE:**

\```
Conforme CONTRATO-MANUTENCAO-CORRECAO-CONTROLADA,
corrija os seguintes erros no módulo <Nome do módulo>:

ERROS IDENTIFICADOS:
<Cole os erros completos aqui com números de linha>

CONTEXTO:
- RF afetado: <RFYYY>
- Módulo: <Nome>
- Tipo de erro: <Build/Runtime/Testes>
- Relatório completo: D:\IC2\.temp_ia\RELATORIO-ERROS-EXTERNOS-RFXXX.md

ARQUIVOS COM ERRO:
- <arquivo1.cs:linha>
- <arquivo2.cs:linha>

CRITÉRIO DE PRONTO:
- `dotnet build` deve passar 100%
- Nenhum novo erro introduzido
- Funcionalidade original deve continuar funcionando
- RFXXX poderá ser validado após correção
\```

---

## 📊 RESUMO EXECUTIVO

| Item | Status |
|------|--------|
| **RFXXX (código próprio)** | <✅ Sem erros / ❌ Com erros> |
| **Ambiente externo** | ❌ QUEBRADO |
| **Erros externos identificados** | <Número> |
| **RFs externos afetados** | <RFYYY, RFZZZ> |
| **Validação do RFXXX** | ⏸️ BLOQUEADA até correção externa |

---

## 📋 PRÓXIMOS PASSOS (ORDEM OBRIGATÓRIA)

1. ✅ **PARAR** validação do RFXXX
2. ✅ **COPIAR** o prompt de correção acima
3. ✅ **COLAR** em novo agente (com contrato de manutenção)
4. ✅ **AGUARDAR** correção dos erros externos
5. ✅ **VALIDAR** que `dotnet build` passou
6. ✅ **RE-VALIDAR** RFXXX após ambiente corrigido
7. ❌ **NÃO** prosseguir enquanto ambiente quebrado

---

## 🔍 DETALHES DA IDENTIFICAÇÃO DO RF

**Método de identificação:**
- [ ] `git blame` nos arquivos com erro
- [ ] Análise de commits recentes (`git log`)
- [ ] Padrão de nomenclatura de branch (`feature/RFYYY-*`)
- [ ] STATUS.yaml do RF externo
- [ ] Comentários no código
- [ ] Namespace/pasta do módulo
- [ ] Não foi possível identificar

**Evidência:**
<Explicar como o RF responsável foi identificado>

Exemplo:
\```bash
$ git blame backend/.../CreateModuloCommand.cs
a1b2c3d4 (RF024-backend 2026-01-01) public Guid CategoriaId { get; set; }
\```

---

**IMPORTANTE:**
- Este relatório foi gerado automaticamente pelo validador
- Todos os erros foram confirmados por `dotnet build` real
- O validador NÃO corrige erros externos (fora do escopo)
```

#### 3. NÃO CORRIGIR os Erros

Erros externos estão **fora do escopo** deste contrato.

O validador **NÃO DEVE**:
- Tentar corrigir o código de outros RFs
- Modificar código fora do escopo
- "Adiantar" correções

#### 4. NÃO FAZER COMMIT

RF reprovado **NÃO** deve ser commitado.

#### 5. INFORMAR o Usuário

Declarar explicitamente:

> "❌ RFXXX REPROVADO: Ambiente quebrado com erros externos.
>
> Verifique RELATORIO-ERROS-EXTERNOS-RFXXX.md para detalhes.
>
> Utilize CONTRATO-MANUTENCAO-CORRECAO-CONTROLADA para corrigir os erros do módulo <Nome> antes de validar RFXXX."

### Critério de Re-Validação

Somente após:
- ✅ Erros externos corrigidos
- ✅ Build passando 100%
- ✅ Testes do ambiente passando

O RFXXX pode ser **re-validado**.

---

## ARTEFATOS OBRIGATÓRIOS

O agente DEVE gerar/manter os seguintes artefatos:

### 1. Contrato de Teste Derivado

**Localização:** `tests/contracts/RFXXX/backend.contract.test.yaml`

**Conteúdo obrigatório:**
- Endpoints testáveis
- Payloads válidos (com tipos e ranges)
- Payloads inválidos (violações explícitas)
- Estados proibidos
- Erros esperados (código HTTP + mensagem)
- Campos obrigatórios vs opcionais
- Regras de permissão
- Versionamento esperado

**Regra:** Este contrato espelha e estressa o contrato oficial.

### 2. Matriz de Violação

**Localização:** `tests/contracts/RFXXX/violations.matrix.md`

**Conteúdo obrigatório:**

Para cada endpoint, documentar:

| Violação | Payload Enviado | Erro HTTP Esperado | Mensagem Esperada | Status |
|----------|----------------|-------------------|------------------|--------|
| Campo ausente | `{ "nome": null }` | 400 | "Campo obrigatório" | PASS/FAIL |
| Tipo errado | `{ "idade": "abc" }` | 400 | "Tipo inválido" | PASS/FAIL |
| Range inválido | `{ "idade": -5 }` | 400 | "Valor fora do range" | PASS/FAIL |
| Enum inválido | `{ "status": "INVALIDO" }` | 400 | "Enum inválido" | PASS/FAIL |
| Estado proibido | `DELETE /ativo/1` (ativo ativo) | 400 | "Estado proibido" | PASS/FAIL |
| Sem permissão | `POST /ativo` (sem claim) | 403 | "Acesso negado" | PASS/FAIL |
| Payload extra | `{ "id": 1, "hack": true }` | 400 | "Campo não permitido" | PASS/FAIL |
| Header ausente | `POST /ativo` (sem Content-Type) | 415 | "Media type inválido" | PASS/FAIL |

**Esta matriz se torna o mapa de ataque do sistema.**

### 3. Testes Automatizados de Violação

**Estrutura obrigatória:**
```
tests/backend/contract/RFXXX/
  ├── CreateEndpoint.Violations.Tests.cs
  ├── UpdateEndpoint.Violations.Tests.cs
  ├── DeleteEndpoint.Violations.Tests.cs
  └── GetEndpoint.Violations.Tests.cs
```

**Foco dos testes:**
- **NÃO** validar apenas "fluxo feliz"
- **VALIDAR** tudo que NÃO pode acontecer
- **GARANTIR** que backend REJEITA violações
- **VERIFICAR** que erros são estruturados

---

## CHECKLIST DE GOVERNANÇA (INEGOCIÁVEL)

Antes de executar qualquer teste, o agente DEVE validar:

### Contrato Oficial

- [ ] Existe contrato backend oficial documentado?
- [ ] Todos endpoints estão descritos?
- [ ] Todos campos têm tipo explícito?
- [ ] Estados possíveis estão enumerados?
- [ ] Erros possíveis estão documentados?
- [ ] Regras de permissão estão claras?

### Comportamento do Backend

- [ ] O que acontece se faltar campo obrigatório?
- [ ] O que acontece se enviar campo extra?
- [ ] O que acontece se enviar enum inválido?
- [ ] O que acontece se acessar fora do estado correto?
- [ ] O que acontece se usuário sem permissão acessar?
- [ ] O que acontece se repetir a mesma requisição?

### Validação do Backend

- [ ] Backend retorna erro estruturado?
- [ ] Backend nunca retorna sucesso em violação?
- [ ] Backend não "corrige" payload inválido?
- [ ] Backend não aceita default silencioso?

**Se qualquer item for NÃO:**
➡️ O agente PARA, documenta e abre violação de contrato.

---

## CHECKLIST DE CENTRAL DE MODULOS E RBAC (OBRIGATORIO - v1.0)

**EXCECAO:** Funcionalidades base (login, multi-tenant, RBAC, Central de Modulos) estao ISENTAS.

Para TODAS as outras funcionalidades, o validador DEVE verificar:

### Central de Modulos (RF083)

- [ ] Funcionalidade registrada na Central de Modulos?
- [ ] Seed de registro existe em `Seeds/Modules/`?
- [ ] Modulo aparece na listagem de modulos ativos?
- [ ] Metadados completos (nome, descricao, icone, rota)?

### RBAC

- [ ] Todas as acoes registradas no RBAC?
- [ ] Acoes padrao criadas (Listar, Criar, Editar, Excluir, Visualizar)?
- [ ] Acoes associadas ao perfil Developer?
- [ ] Seed de permissoes existe em `Seeds/Permissions/`?
- [ ] Endpoints protegidos por [Authorize] + politicas corretas?

**Se qualquer item for NAO:**
➡️ **REPROVACAO IMEDIATA** - Backend NAO pode ser aprovado sem Central de Modulos e RBAC.
➡️ O agente PARA, documenta o gap e retorna para correcao.

---

## CRITÉRIO DE BLOQUEIO

O agente **DEVE BLOQUEAR** o merge se:

1. Backend aceita qualquer payload que viola o contrato
2. Backend retorna sucesso (HTTP 2xx) para violação
3. Backend corrige silenciosamente dados inválidos
4. Backend aceita defaults não documentados
5. Erros retornados NÃO são estruturados

**Bloqueio é OBRIGATÓRIO. NÃO é negociável.**

---

## AUTORIDADE FORMAL

O Tester-Backend é um CONTRATO BLOQUEADOR da cadeia de execução.

Isso significa que:

- Nenhum contrato posterior pode prosseguir sem sua aprovação
- Nenhum merge é considerado válido sem sua validação
- Nenhum status COMPLETED pode ser registrado sem sua assinatura no EXECUTION-MANIFEST

A reprovação do Tester-Backend invalida automaticamente:
- A execução corrente
- O manifesto associado
- Qualquer tentativa de continuidade

---

## INTEGRACAO COM EXECUTION-MANIFEST

Toda execução do Tester-Backend DEVE:

1. Registrar resultado no EXECUTION-MANIFEST.md
2. Marcar explicitamente:
   - APROVADO ou REPROVADO
3. Incluir referência aos artefatos gerados:
   - violations.matrix.md
   - backend.test.contract.yaml
   - testes executados

Execuções sem registro no manifesto são consideradas INVALIDAS.

---

## PROIBICAO DE NEGOCIACAO DE ESCOPO

O Tester-Backend:

- NAO negocia escopo
- NAO executa tarefas fora do contrato
- NAO aceita solicitacoes implicitas
- NAO faz excecoes
- NAO continua execucao em caso de violacao

Qualquer solicitacao fora do escopo DEVE ser recusada imediatamente,
com orientacao para ajuste formal do contrato.

---

## CRITERIO DE COBERTURA 100% (OBRIGATORIO)

Este contrato DEVE validar que:

- [ ] **100% dos UCs do UC-RFXXX foram implementados**
- [ ] **100% das RNs foram validadas**
- [ ] Backend funcionalmente completo (nao parcial)
- [ ] TODAS as violacoes de contrato sao rejeitadas

⚠️ **ATENCAO CRITICA:**

**Cobertura UC < 100% = REPROVACAO AUTOMATICA**

**Qualquer ressalva = REPROVACAO**

---

## VALIDAÇÃO 18: COBERTURA DE TESTES UNITÁRIOS (NOVO - BLOQUEANTE)

**Versão:** 1.0
**Data:** 2026-01-09
**Contexto:** Adicionado após análise do RF006 para garantir que backend possui testes unitários OBRIGATÓRIOS para TODOS os Commands/Queries ANTES de marcar como concluído.

**Objetivo:** Garantir que backend possui testes unitários com 100% de cobertura de Commands/Queries, evitando implementações sem validação automatizada.

### PASSO 18.1: Validar Existência de Testes Unitários

O agente DEVE validar que:

```python
# 1. Listar TODOS os Commands implementados
commands_implementados = listar_arquivos(
    "backend/Application/Features/**/Commands/**/*.cs",
    excluir=["*Tests.cs", "*Validator.cs"]
)

# 2. Listar TODOS os Queries implementados
queries_implementados = listar_arquivos(
    "backend/Application/Features/**/Queries/**/*.cs",
    excluir=["*Tests.cs", "*Validator.cs"]
)

# 3. Listar TODOS os arquivos de teste
testes_existentes = listar_arquivos(
    "backend/Application.Tests/Features/**/*Tests.cs"
)

# 4. Validar que CADA Command tem teste correspondente
commands_sem_teste = []
for command in commands_implementados:
    nome_command = extrair_nome(command)  # Ex: CreateClienteCommand
    nome_teste = nome_command + "Tests.cs"  # Ex: CreateClienteCommandTests.cs

    teste_existe = any(nome_teste in teste for teste in testes_existentes)

    if not teste_existe:
        commands_sem_teste.append(nome_command)

# 5. Validar que CADA Query tem teste correspondente
queries_sem_teste = []
for query in queries_implementados:
    nome_query = extrair_nome(query)  # Ex: GetClienteByIdQuery
    nome_teste = nome_query + "Tests.cs"  # Ex: GetClienteByIdQueryTests.cs

    teste_existe = any(nome_teste in teste for teste in testes_existentes)

    if not teste_existe:
        queries_sem_teste.append(nome_query)

# 6. Calcular cobertura
total_commands_queries = len(commands_implementados) + len(queries_implementados)
total_sem_teste = len(commands_sem_teste) + len(queries_sem_teste)
total_com_teste = total_commands_queries - total_sem_teste

cobertura_percentual = (total_com_teste / total_commands_queries * 100) if total_commands_queries > 0 else 0

print(f"Cobertura de Testes Unitários: {total_com_teste}/{total_commands_queries} ({cobertura_percentual:.1f}%)")

# 7. Validar bloqueio
if cobertura_percentual < 100:
    print("❌ BACKEND REPROVADO - Cobertura de testes < 100%")
    print(f"Commands sem teste: {commands_sem_teste}")
    print(f"Queries sem teste: {queries_sem_teste}")
    print("❌ BLOQUEIO: Backend não pode ser marcado como concluído")
    print("❌ RETORNAR ao contrato de backend-criacao.md para criar testes")
    PARAR()
```

### PASSO 18.2: Executar Testes Unitários

O agente DEVE executar testes e validar aprovação:

```bash
# 1. Executar testes unitários
dotnet test backend/Application.Tests/Application.Tests.csproj --logger "console;verbosity=detailed"

# 2. Capturar exit code
exit_code=$?

# 3. Validar resultado
if [ $exit_code -ne 0 ]; then
    echo "❌ BACKEND REPROVADO - Testes unitários falharam"
    echo "❌ BLOQUEIO: Backend não pode ser marcado como concluído"
    echo "❌ Corrigir falhas e re-executar"
    PARAR()
fi

# 4. Capturar taxa de aprovação
# Exemplo de output: "Passed: 45, Failed: 0, Skipped: 0"
# Taxa de aprovação DEVE ser 100% (Failed = 0, Skipped = 0)
```

### PASSO 18.3: Validar Tipos de Testes Obrigatórios

Para CADA Command, o agente DEVE validar que existem pelo menos 3 tipos de teste:

1. **Teste de sucesso (happy path)**
   - Cenário: Dados válidos
   - Resultado esperado: `Success` com resultado correto

2. **Teste de validação (FluentValidation)**
   - Cenário: Dados inválidos (campo obrigatório ausente, formato inválido, etc.)
   - Resultado esperado: Validation errors

3. **Teste de regra de negócio**
   - Cenário: Violação de RN (ex: CNPJ duplicado, cliente inativo, etc.)
   - Resultado esperado: `Failure` com mensagem específica

```python
# Exemplo de validação
for command in commands_implementados:
    nome_teste = nome_command + "Tests.cs"
    arquivo_teste = ler_arquivo(nome_teste)

    # Validar presença de testes obrigatórios
    tem_teste_sucesso = "Success" in arquivo_teste or "ShouldReturnSuccess" in arquivo_teste
    tem_teste_validacao = "Validation" in arquivo_teste or "ShouldFailValidation" in arquivo_teste
    tem_teste_rn = "BusinessRule" in arquivo_teste or "ShouldFailBusinessRule" in arquivo_teste

    if not (tem_teste_sucesso and tem_teste_validacao and tem_teste_rn):
        print(f"❌ {nome_command}: Tipos de teste obrigatórios ausentes")
        print(f"   - Teste de sucesso: {'✅' if tem_teste_sucesso else '❌'}")
        print(f"   - Teste de validação: {'✅' if tem_teste_validacao else '❌'}")
        print(f"   - Teste de RN: {'✅' if tem_teste_rn else '❌'}")
        REPROVAR()
```

### PASSO 18.4: Atualizar STATUS.yaml

O agente DEVE atualizar `STATUS.yaml`:

```yaml
desenvolvimento:
  backend:
    testes_implementados:
      - "CreateClienteCommandTests.cs (3 testes)"
      - "UpdateClienteCommandTests.cs (3 testes)"
      - "DeleteClienteCommandTests.cs (2 testes)"
      - "GetClienteByIdQueryTests.cs (2 testes)"
    cobertura_testes: "4/4 commands com testes (100%)"
    taxa_aprovacao_testes: "10/10 testes aprovados (100%)"
    ultima_execucao_testes: "2026-01-09 14:30:00"
```

### Critério de Aprovação

- ✅ Cobertura: 100% dos Commands/Queries possuem testes
- ✅ Taxa de aprovação: 100% (nenhum teste falhando ou skipped)
- ✅ Tipos de teste: Cada Command possui pelo menos 3 tipos (sucesso, validação, RN)
- ✅ Exit code: `dotnet test` retorna 0

**SE qualquer verificação FALHAR:**
- ❌ Backend REPROVADO
- ❌ BLOQUEIO: Backend não pode ser marcado como concluído
- ❌ Reportar Commands/Queries sem testes
- ❌ Reportar testes falhando
- ❌ RETORNAR ao contrato de backend-criacao.md

**IMPORTANTE:** Esta validação garante que backend possui validação automatizada COMPLETA antes de ser considerado concluído, evitando implementações sem garantias de qualidade.

**Referência:** `CLAUDE.md` seção 18.2.2 "Bloqueios Obrigatórios"

---

## SAÍDA OBRIGATÓRIA

Ao final da execução, o agente DEVE entregar:

1. **Contrato de Teste Derivado** (`backend.contract.test.yaml`)
2. **Matriz de Violação** (`violations.matrix.md`) com status PASS/FAIL
3. **Testes Automatizados** (executáveis via `dotnet test`)
4. **Relatório de Conformidade:**
   - Total de violações testadas: XX
   - Violações rejeitadas corretamente: XX
   - Violações aceitas (BLOQUEIO): XX
   - **Cobertura UC: XX%** (DEVE ser 100%)
   - Status final: APROVADO / REPROVADO
5. **STATUS.yaml atualizado**

---

## ATUALIZACAO DO ANTI-ESQUECIMENTO (QUANDO REPROVADO)

Caso o contrato seja **REPROVADO**, o agente DEVE:

1. **Identificar** os erros mais comuns encontrados
2. **Atualizar** o `D:\IC2\docs\anti-esquecimento-backend.md`
3. **Adicionar** observacoes genericas (nao muito especificas)
4. **Verificar** se a observacao ja existe antes de incluir
5. **Seguir** o padrao que ja esta no documento

### Regras de Atualizacao

- Observacoes devem ser genericas e reutilizaveis
- Nao duplicar observacoes existentes
- Seguir numeracao e formato do documento
- Focar em "esquecimentos" comuns, nao casos especificos

### Exemplo de Observacao

```markdown
## #XX: Validacao de Dígitos Verificadores

**Esquecimento comum:** Implementar validacao de CNPJ/CPF sem validar digitos verificadores.

**Como evitar:** Sempre criar validators matematicos para CNPJ/CPF usando algoritmo oficial da Receita Federal.
```

Desta forma, quando um contrato e reprovado, alimentamos a base de conhecimento para evitar repeticao de erros.

---

## CRITÉRIO DE AMBIGUIDADE

Se durante a análise, o agente identificar que o contrato é **ambíguo**:

1. **PARAR** imediatamente
2. **DOCUMENTAR** a ambiguidade encontrada
3. **PROPOR** ajuste no contrato oficial
4. **NÃO INVENTAR** regra ou comportamento

**Ambiguidade bloqueia execução.**

---

## AUTORIDADE DO AGENTE

Este agente tem **AUTORIDADE PARA BLOQUEAR MERGES**.

Se violações forem aceitas pelo backend:
➡️ O merge para `dev` **NÃO PODE** ser realizado.
➡️ O RF **NÃO PODE** avançar.
➡️ CONTRATO DE MANUTENÇÃO deve ser ativado para correção.

**Este contrato é a última linha de defesa da integridade do sistema.**

---

## REGRA FINAL

**Código que passa teste mas viola contrato é considerado código inválido.**

**Nenhum teste backend pode ser criado sem contrato explícito.**

**Testes devem priorizar violação, não fluxo feliz.**

**Backend é proibido de aceitar payload fora do contrato.**

**Correções silenciosas são consideradas bugs graves.**

**Qualquer ambiguidade no contrato bloqueia desenvolvimento.**

---

**Este contrato é vinculante.**
**Violações devem ser reportadas, NÃO corrigidas.**
**O agente Tester-Backend tem autoridade para bloquear merges.**

---

## HISTÓRICO DE VERSÕES

| Versão | Data | Descrição |
|--------|------|-----------|
| 1.1 | 2026-01-09 | Adicionada VALIDAÇÃO 18 "Cobertura de Testes Unitários" (BLOQUEANTE) - Valida que 100% dos Commands/Queries possuem testes unitários (sucesso, validação, RN), taxa de aprovação 100%, exit code 0. Garante que backend possui validação automatizada COMPLETA antes de ser marcado como concluído. Baseado em análise RF006. Referência: CLAUDE.md seção 18.2.2 |
| 1.0 | [DATA ANTERIOR] | Criação do contrato de validação de backend com testes orientados por violação |

---

## REGRA DE NEGACAO ZERO

Se uma solicitacao:
- nao estiver explicitamente prevista no contrato ativo, ou
- conflitar com qualquer regra do contrato

ENTAO:

- A execucao DEVE ser NEGADA
- Nenhuma acao parcial pode ser realizada
- Nenhum "adiantamento" e permitido
