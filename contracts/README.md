# Contratos do Projeto IControlIT

Este diretório contém os **contratos formais e vinculantes** que regem a atuação de agentes automatizados (Claude Code) neste repositório.

## O que são Contratos?

Os contratos **NÃO são prompts**. Eles definem:
- **Limites de atuação** do agente
- **Escopo permitido** de ações
- **Regras invioláveis** de execução
- **Critérios de bloqueio** (quando parar)

## Hierarquia de Governança

O comportamento do agente é governado por:
1. **`CLAUDE.md`** - Camada superior (regras gerais do projeto)
2. **Contratos específicos** - Este diretório (regras por tipo de tarefa)
3. **Checklists** - Validação estruturada (`checklists/`)
4. **Prompts** - Ativadores simplificados (`prompts/`)

---

## Princípios Fundamentais

- ✅ Um contrato **só é aplicado se for explicitamente citado no prompt**
- ✅ Contratos **não se misturam** (um de cada vez)
- ✅ Em caso de conflito, o contrato **mais restritivo prevalece**
- ✅ Qualquer violação exige: **PARAR → ALERTAR → AGUARDAR decisão**

---

## Estrutura Organizada

Este diretório está organizado por categoria:

```
contracts/
├── desenvolvimento/      ← Criação e manutenção de código
│   ├── execucao/
│   ├── validacao/
│   └── manutencao/
│
├── documentacao/         ← Geração e validação de documentação
│   ├── geracao/
│   ├── execucao/
│   └── validacao/
│
├── devops/               ← Operações DevOps e manifestos
│
├── deploy/               ← Deploy, hotfix e rollback
│
├── auditoria/            ← Auditoria e debug
│
├── orquestracao/         ← Orquestração e transições
│
├── fluxos/               ← Documentação de fluxos
│
├── deprecated/           ← Contratos obsoletos (não usar)
│
└── README.md             ← Este arquivo
```

---

## Como Usar os Contratos

**Formato obrigatório do prompt:**

```
Conforme <CAMINHO_COMPLETO_DO_CONTRATO> para <RF/TAREFA>.
Seguir D:\IC2\CLAUDE.md.
```

**Exemplos corretos:**

```
# Adequar frontend
Conforme contracts/desenvolvimento/execucao/frontend-adequacao.md para RF046.
Seguir D:\IC2\CLAUDE.md.

# Validar frontend
Conforme contracts/desenvolvimento/validacao/frontend.md para RF046.
Seguir D:\IC2\CLAUDE.md.

# Gerar documentação UC
Conforme contracts/documentacao/geracao/uc.md para RF046.
Seguir D:\IC2\CLAUDE.md.

# Auditar conformidade
Conforme contracts/auditoria/conformidade.md para RF046.
Seguir D:\IC2\CLAUDE.md.
```

**Se nenhum contrato for citado:**
- O agente NÃO deve implementar código
- A solicitação será tratada como análise técnica
- O agente DEVE solicitar esclarecimento

---

## Lista de Contratos

### 1. Contrato de Manutenção / Correção Controlada

Arquivo:
```
CONTRATO-MANUTENCAO-CORRECAO-CONTROLADA.md
```

Finalidade:
- Correção pontual de erros
- Hotfix governado
- Atuação cirúrgica

Proíbe:
- Evolução funcional
- Refatoração
- Alterações arquiteturais
- Melhorias técnicas

Este é o **contrato mais restritivo**.
Quando ativado, ele **sobrepõe qualquer outro**.

---

### 2. Contrato de Execução – Frontend

Arquivo:
```
CONTRATO-EXECUCAO-FRONTEND.md
```

Finalidade:
- Implementação de frontend
- Integração completa com o ecossistema
- i18n, permissões, seeds e testes E2E

Regras-chave:
- Backend é a fonte da verdade
- RF/UC/MD externos são apenas referência conceitual
- Qualquer 401/403 invalida a entrega
- Warnings de i18n invalidam o RF

---

### 3. Contrato de Execução – Backend

Arquivo:
```
CONTRATO-EXECUCAO-BACKEND.md
```

Finalidade:
- Implementação de backend
- Commands, Queries, Endpoints e Validators
- Seeds funcionais e permissões obrigatórias

Regras-chave:
- Nenhuma mudança arquitetural
- Seeds idempotentes obrigatórios
- Testes mínimos obrigatórios
- 401/403/404/500 DEVEM falhar testes

---

### 4. Contrato de Execução – Testes

Arquivo:
- CONTRATO-EXECUCAO-TESTES.md

Finalidade:
- Executar testes de backend e E2E
- Coletar evidências
- Detectar falhas sem correção

Proíbe:
- Alteração de código
- Ajuste de seeds
- Correções
- Workarounds

---

### 5. Contrato de Execução – Tester-Backend

Arquivo:
```
CONTRATO-EXECUCAO-TESTER-BACKEND.md
```

Checklist:
```
checklists/CHECKLIST-CONTRATO-TESTER-BACKEND.md
```

Prompt:
```
prompts/TESTER-BACKEND.md
```

Finalidade:
- Validação de contrato backend através de testes de violação
- Garantir que backend REJEITA payloads inválidos
- Criar matriz de violação
- Implementar testes automatizados focados em violação
- BLOQUEAR merges se violações forem aceitas

Filosofia:
- NÃO testa funcionalidades felizes primeiro
- TESTA o CONTRATO
- Prioriza violações sobre fluxo feliz
- Garante que backend seja PERFEITO

Regras-chave:
- Backend NUNCA pode aceitar payload inválido
- Backend NUNCA pode corrigir dados silenciosamente
- Backend DEVE rejeitar violações com erros estruturados
- Agente TEM AUTORIDADE para bloquear merges
- Código que passa teste mas viola contrato = CÓDIGO INVÁLIDO

Proíbe:
- Alterar código de produção (backend)
- Corrigir bugs encontrados
- Simplificar testes de violação
- Assumir comportamento implícito
- Inventar regras não documentadas

**Este agente é a última linha de defesa do contrato.**

---

## Boas Práticas de Prompt

Bom exemplo (frontend):

```
Executar frontend do RF046 conforme CONTRATO DE EXECUÇÃO – FRONTEND
```

Bom exemplo (backend):

```
Executar backend do RF046 conforme CONTRATO DE EXECUÇÃO – BACKEND
```

Bom exemplo (validação de contrato):

```
Validar contrato backend do RF046 conforme CONTRATO DE EXECUÇÃO – TESTER-BACKEND
```

Bom exemplo (manutenção):

```
Corrigir erro 403 ao acessar /api/TiposConsumidores
conforme CONTRATO DE MANUTENÇÃO
```

Exemplo inválido:

```
Executar frontend conforme CONTRATO DE EXECUÇÃO – BACKEND
```

Neste caso, o agente DEVE parar e solicitar correção.

---

## Checklists: Formato e Governança

Este projeto utiliza dois formatos de checklist por contrato:

- `.md` → Checklist **humano**, para leitura, revisão e auditoria
- `.yaml` → Checklist **executável**, utilizado pelo CI

### Regra Obrigatória

- O arquivo `.yaml` é a **ÚNICA fonte de validação automática**
- O arquivo `.md` existe apenas para referência humana
- Divergências entre `.md` e `.yaml` devem ser corrigidas
- O CI valida **EXCLUSIVAMENTE** os arquivos `.yaml`

---

## Importante

- Contratos NÃO devem ser editados a cada execução
- O RF, erro ou contexto **sempre** pertence ao prompt
- O contrato permanece estável e reutilizável

Contratos existem para **proteger o sistema**,
não para acelerar execução a qualquer custo.

---

## Regra Final

Se houver dúvida:
➡️ **Não execute. Pergunte.**

Este diretório é parte crítica da governança do projeto.

## Diagrama

            ┌────────────┐
            │   DEBUG    │
            │ Investig.  │
            │ Read-Only  │
            └─────┬──────┘
                  │
                  ▼
            ┌────────────┐
            │   TESTES   │
            │ Execução   │
            │ Observação │
            └─────┬──────┘
                  │
      ┌───────────┼───────────┐
      ▼           ▼           ▼
┌─────────┐ ┌─────────┐ ┌────────────┐
│ FRONTEND│ │ BACKEND │ │ MANUTENÇÃO │
│ Execução│ │ Execução│ │ Correção   │
└────┬────┘ └────┬────┘ └─────┬──────┘
     │           │            │
     │           ▼            │
     │    ┌──────────────┐   │
     │    │TESTER-BACKEND│   │
     │    │  Validação   │   │
     │    │   Contrato   │   │
     │    │(pode bloquear)│  │
     │    └──────┬───────┘   │
     │           │            │
     └───────────┴────────────┘
                  │
                  ▼
            ┌────────────┐
            │   TESTES   │
            │ Obrigatório│
            └────────────┘
