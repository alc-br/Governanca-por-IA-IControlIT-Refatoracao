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

## TODO LIST OBRIGATORIA (LER PRIMEIRO)

> **ATENCAO:** O agente DEVE criar esta todo list IMEDIATAMENTE apos ativar o contrato.
> **NENHUMA ACAO** pode ser executada antes da todo list existir.
> **COPIAR EXATAMENTE** o template abaixo.

### Template para Correcao de Erro

```
TODO LIST - Manutencao/Correcao
================================

[pending] Salvar contexto Git inicial
  |-- [pending] BRANCH_ORIGINAL=$(git branch --show-current)
  |-- [pending] git status (verificar estado limpo)
  +-- [pending] Anotar branch original para retorno

[pending] Analisar o erro reportado
  |-- [pending] Ler relatorio de erros (se fornecido)
  |-- [pending] Reproduzir o erro localmente
  |-- [pending] Identificar causa raiz
  +-- [pending] Validar que o erro existe

[pending] Criar branch de correcao (se necessario)
  |-- [pending] git checkout -b hotfix/correcao-<modulo>
  +-- [pending] OU continuar no branch atual (se apropriado)

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

[pending] Fazer commit da correcao
  |-- [pending] git add . (somente arquivos corrigidos)
  |-- [pending] git commit -m "fix: <descricao do erro corrigido>"
  +-- [pending] Commit com mensagem clara

[pending] RETORNAR ao branch original (OBRIGATORIO)
  |-- [pending] git checkout $BRANCH_ORIGINAL
  +-- [pending] Confirmar retorno ao branch original

[pending] Declaracao final
  |-- [pending] Causa raiz do erro
  |-- [pending] Onde a correcao foi aplicada
  |-- [pending] Por que nao impacta outras partes
  +-- [pending] Como validar que erro nao ocorre mais
```

### Regras de Execucao da Todo List

1. **COPIAR** o template acima ANTES de qualquer acao
2. **SALVAR** o branch original ANTES de criar branch de hotfix
3. Atualizar status em tempo real ([pending] → [in_progress] → [completed])
4. **NUNCA** pular etapas
5. **PARAR** em caso de falha (build error/test failure)
6. **RETORNAR** ao branch original SEMPRE ao final
7. Seguir ordem sequencial
8. Somente declarar CONCLUIDO apos **TODOS** os itens completed

---

## WORKFLOW DE BRANCHES (OBRIGATORIO)

### 1. Salvar Branch Original

```bash
# SEMPRE salvar o branch atual ANTES de qualquer acao
BRANCH_ORIGINAL=$(git branch --show-current)
echo "Branch original: $BRANCH_ORIGINAL"
```

### 2. Criar Branch de Hotfix (se necessario)

```bash
# Criar branch especifico para a correcao
git checkout -b hotfix/correcao-<modulo>
```

### 3. Fazer Commit da Correcao

```bash
# Commit da correcao
git add .
git commit -m "fix: <descricao clara do erro corrigido>"
```

### 4. RETORNAR ao Branch Original (OBRIGATORIO)

```bash
# SEMPRE retornar ao branch original
git checkout $BRANCH_ORIGINAL
```

**IMPORTANTE:**
- O agente de manutencao **NAO** faz merge
- O agente de manutencao **NAO** faz push
- O agente de manutencao **RETORNA** ao branch original
- O usuario decide quando/como integrar a correcao

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

## PROVA DE CORREÇÃO (OBRIGATÓRIA)

A correção **SÓ é considerada válida** quando:

- O erro descrito **não ocorre mais**
- O sistema funciona após restart
- Nenhum novo warning ou erro é introduzido
- Testes existentes continuam passando
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
