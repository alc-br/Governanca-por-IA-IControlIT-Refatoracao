# CHECKLIST – CONTRATO DE EXECUÇÃO – TESTER-BACKEND

Checklist de validação do **Contrato de Execução – Tester-Backend**.

Este checklist garante que o backend seja **PERFEITO** em relação ao contrato.

---

## 1. Governança Inicial

- [ ] Contrato Tester-Backend citado explicitamente
- [ ] CONTRATO-PADRAO-DESENVOLVIMENTO.md lido
- [ ] CONTRATO-EXECUCAO-BACKEND.md lido
- [ ] ARCHITECTURE.md, CONVENTIONS.md e CLAUDE.md respeitados
- [ ] Backend já implementado e mergeado em `dev`

---

## 2. Análise do Contrato Oficial

- [ ] Contrato backend oficial existe e está completo
- [ ] Todos endpoints estão documentados
- [ ] Todos campos têm tipo explícito (string, int, enum, etc.)
- [ ] Todos campos têm obrigatoriedade definida (required/optional)
- [ ] Estados possíveis estão enumerados
- [ ] Transições de estado estão documentadas
- [ ] Erros possíveis estão documentados (códigos HTTP + mensagens)
- [ ] Regras de permissão estão claras (claims/policies)
- [ ] Regras de validação estão explícitas (ranges, regex, etc.)

---

## 3. Contrato de Teste Derivado

- [ ] Arquivo `backend.contract.test.yaml` criado
- [ ] Todos endpoints listados com exemplos
- [ ] Payloads válidos documentados com tipos
- [ ] Payloads inválidos documentados (violações explícitas)
- [ ] Estados proibidos listados
- [ ] Erros esperados documentados (HTTP + mensagem)
- [ ] Campos obrigatórios vs opcionais claramente marcados
- [ ] Regras de permissão documentadas
- [ ] Versionamento da API documentado

---

## 4. Matriz de Violação

- [ ] Arquivo `violations.matrix.md` criado
- [ ] Para CADA endpoint, testado:
  - [ ] Campo obrigatório ausente
  - [ ] Campo com tipo errado (string em vez de int, etc.)
  - [ ] Campo fora do range (negativos, muito grandes, etc.)
  - [ ] Enum inválido (valor não permitido)
  - [ ] Estado inválido (operação proibida no estado atual)
  - [ ] Acesso sem permissão (claim/policy ausente)
  - [ ] Ordem inválida de estado (transição proibida)
  - [ ] Requisição duplicada (teste de idempotência)
  - [ ] Payload com campo extra não permitido
  - [ ] Headers ausentes ou inválidos (Content-Type, etc.)

---

## 5. Testes Automatizados de Violação

- [ ] Estrutura `tests/backend/contract/RFXXX/` criada
- [ ] Testes implementados para cada tipo de violação
- [ ] Cada teste valida que backend REJEITA a violação
- [ ] Cada teste valida código HTTP correto (400, 403, 415, etc.)
- [ ] Cada teste valida mensagem de erro estruturada
- [ ] Testes executam sem dependências manuais
- [ ] Testes são idempotentes (podem ser re-executados)

---

## 6. Execução dos Testes de Violação

- [ ] `dotnet test` executado com sucesso
- [ ] Todas violações foram REJEITADAS pelo backend
- [ ] Backend retorna códigos HTTP corretos (4xx para violações)
- [ ] Backend retorna erros estruturados (não apenas strings)
- [ ] Backend NUNCA aceita payload inválido
- [ ] Backend NUNCA corrige dados silenciosamente
- [ ] Backend NUNCA retorna sucesso (2xx) para violação

---

## 7. Validação de Perfeição do Backend

### Backend REJEITA (obrigatório):

- [ ] Campos obrigatórios ausentes
- [ ] Tipos de dados incorretos
- [ ] Valores fora do range permitido
- [ ] Enums inválidos
- [ ] Estados proibidos
- [ ] Acessos sem permissão
- [ ] Transições de estado inválidas
- [ ] Payloads com campos extras não documentados
- [ ] Requisições com headers inválidos

### Backend RETORNA (obrigatório):

- [ ] Erros estruturados (objeto JSON com código e mensagem)
- [ ] Códigos HTTP corretos (400, 403, 404, 415, etc.)
- [ ] Mensagens de erro claras e consistentes
- [ ] Validação em TODOS os endpoints (sem exceção)

### Backend NUNCA (proibido):

- [ ] Aceita payload inválido silenciosamente
- [ ] Corrige dados automaticamente (sanitização não documentada)
- [ ] Retorna sucesso (2xx) para violação
- [ ] Aceita defaults não documentados
- [ ] Ignora campos extras sem validar

---

## 8. Análise de Conformidade

- [ ] Total de violações testadas documentado
- [ ] Total de violações rejeitadas corretamente documentado
- [ ] Total de violações aceitas (BLOQUEIOS) documentado
- [ ] Relatório de conformidade gerado
- [ ] STATUS.yaml atualizado com resultados

---

## 9. Critério de Bloqueio (CRÍTICO)

**SE QUALQUER ITEM ABAIXO FOR VERDADEIRO, MERGE DEVE SER BLOQUEADO:**

- [ ] Backend aceita qualquer payload que viola o contrato
- [ ] Backend retorna sucesso (2xx) para violação
- [ ] Backend corrige silenciosamente dados inválidos
- [ ] Backend aceita defaults não documentados
- [ ] Erros retornados NÃO são estruturados
- [ ] Algum endpoint ignora validação
- [ ] Algum endpoint aceita campos extras sem rejeitar

**SE BLOQUEIO FOR NECESSÁRIO:**
- [ ] Merge para `dev` foi IMPEDIDO
- [ ] Violações foram documentadas em relatório
- [ ] CONTRATO DE MANUTENÇÃO foi indicado para correção
- [ ] STATUS.yaml atualizado com status `failed`

---

## 10. Ambiguidades Identificadas

**SE CONTRATO FOR AMBÍGUO:**

- [ ] Ambiguidade foi IDENTIFICADA e DOCUMENTADA
- [ ] Proposta de ajuste no contrato foi criada
- [ ] Execução foi PAUSADA (não inventou regra)
- [ ] Solicitação de esclarecimento foi enviada

---

## 11. Status Final

Marque APENAS UMA opção:

- [ ] **APROVADO** - Todas violações rejeitadas, backend perfeito
- [ ] **REPROVADO** - Violações aceitas, bloqueio ativado
- [ ] **BLOQUEADO** - Contrato ambíguo, esclarecimento necessário

---

## Métricas de Qualidade (Referência)

**Backend Perfeito:**
- 100% das violações testadas
- 100% das violações rejeitadas
- 0% de violações aceitas
- 100% de erros estruturados
- 100% de códigos HTTP corretos

**Tolerância:**
- **ZERO** violações aceitas permitidas
- **ZERO** correções silenciosas permitidas
- **ZERO** defaults não documentados permitidos

---

**Regra Final:**

Código que passa teste mas viola contrato = **CÓDIGO INVÁLIDO**

Backend que aceita violação = **BACKEND IMPERFEITO**

Merge com violações aceitas = **BLOQUEADO**
