# COMPLIANCE.md
# Regras de Conformidade e Validação - Projeto IControlIT

**Versão:** 2.0.0
**Data:** 2026-01-01

Este documento define todas as regras de conformidade, validação e governança que DEVEM ser seguidas durante execução de contratos. Violações destas regras bloqueiam a execução.

---

## 1. SEPARAÇÃO RF / RL (OBRIGATÓRIA)

### Princípio Fundamental

Todo RF DEVE ter separação estrita entre:
- **RFXXX.md / RFXXX.yaml** - Contrato funcional moderno (o que o sistema DEVE fazer)
- **RL-RFXXX.md / RL-RFXXX.yaml** - Referência ao Legado (memória técnica histórica do VB.NET/ASPX)

### Proibições Absolutas

❌ **NUNCA:**
- Misturar conteúdo legado em RFXXX.md
- Criar requisitos funcionais a partir de RL
- Inferir obrigações de comportamento legado

✅ **SEMPRE:**
- RL documenta o passado (consulta histórica)
- RL NÃO cria futuro (não é contrato)
- Cada item de RL DEVE ter destino explícito (assumido/substituído/descartado)

### Workflow Obrigatório de Separação

1. Ler RFXXX.md atual (pode conter legado misturado)
2. Identificar seções que são **contrato moderno**
3. Identificar seções que são **referência ao legado**
4. Criar RFXXX.md limpo (apenas contrato)
5. Criar RL-RFXXX.md com memória legado
6. Estruturar RFXXX.yaml + RL-RFXXX.yaml
7. Executar validador: `python tools/docs/validator-rl.py RFXXX`
8. Corrigir gaps até 100%
9. Atualizar STATUS.yaml

### Validação Obrigatória

Antes de marcar RF como completo, DEVE executar:
```bash
# Validar separação RF/RL
python D:\IC2_Governanca\tools\docs\validator-rl.py RFXXX

# Validar cobertura RF → UC
python D:\IC2_Governanca\tools\docs\validator-rf-uc.py RFXXX

# Validar governança completa
python D:\IC2_Governanca\tools\docs\validator-governance.py RFXXX
```

### Critério de Aceite

RF NÃO pode avançar se:
- ❌ RF e RL não estiverem separados
- ❌ RL tiver itens sem destino explícito
- ❌ UC não cobrir 100% do RF
- ❌ TC não cobrir 100% dos UCs
- ❌ STATUS.yaml não refletir realidade

**VIOLAÇÃO:** Misturar legado em RF ou criar requisitos a partir de RL é considerado **execução inválida**.

---

## 2. GESTÃO DE USER STORIES (OBRIGATÓRIA)

### Quando Criar/Atualizar user-stories.yaml

Este arquivo **OBRIGATÓRIO** deve ser criado/atualizado quando:

1. **Novo RF é documentado** - Durante execução do CONTRATO-DOCUMENTACAO-ESSENCIAL
2. **RF é alterado** - Quando regras de negócio ou funcionalidades mudam
3. **Escopo é expandido** - Quando novas features são adicionadas ao RF
4. **Dependencies mudam** - Quando dependências entre RFs são alteradas

### Estrutura Obrigatória

```yaml
rf_id: RFXXX
rf_title: "[Título do RF]"
feature_work_item_id: null  # Preenchido após criação no Azure DevOps
epic_code: EPICXXX-YYY-ZZZ

user_stories:
  - id: null
    code: "US-RFXXX-001"
    title: "[Título da User Story]"
    module: "[Nome do Módulo]"
    description: |
      Como [Persona],
      Quero [Objetivo],
      Para [Benefício].
    acceptance_criteria:
      - [Critério 1 - testável e específico]
      - [Critério 2]
      - [Mínimo 5 critérios por story]
    technical_notes: |
      - Backend: Entity, Commands, Queries, API
      - Frontend: Telas, Componentes, Rotas
      - Integrações: i18n, auditoria, permissões
    dependencies:
      - RF-XXX: [Descrição]
    status: "To Do"
    story_points: 5  # Fibonacci: 1, 2, 3, 5, 8, 13
    priority: "Alta"  # Alta, Média, Baixa
    sprint: "[Nome da Fase]"
```

### Regras de Qualidade

1. **Mínimo 2 User Stories por RF** (exceto RFs extremamente simples)
2. **Cada story deve ter 1-13 pontos** (Fibonacci) - stories > 13 devem ser quebradas
3. **Total de pontos por RF não deve exceder 100**
4. **Acceptance Criteria**: mínimo 5 critérios testáveis por story
5. **Technical Notes**: incluir backend, frontend e integrações obrigatórias
6. **Dependencies**: mapear todas as dependências entre stories e RFs
7. **Código único**: US-RFXXX-NNN (onde NNN = 001, 002, 003...)
8. **Description**: formato "Como... Quero... Para..." obrigatório

### Violação

Se o agente criar ou alterar documentação de RF SEM criar/atualizar user-stories.yaml:
➡️ A execução é considerada **INCOMPLETA**
➡️ STATUS.yaml NÃO deve marcar documentacao.user_stories = True
➡️ RF NÃO pode avançar para próximo contrato

---

## 3. AUTO-VALIDAÇÃO OBRIGATÓRIA DO AGENTE

### Quando Validar

Sempre que o agente criar ou modificar qualquer um dos arquivos abaixo:

- RFXXX.yaml
- UC-RFXXX.yaml
- TC-RFXXX.yaml
- STATUS.yaml

### Passos Obrigatórios

O agente DEVE, OBRIGATORIAMENTE:

1. Executar o validador de cobertura RF → UC → TC:
```bash
python tools/docs/validator-rf-uc.py \
  --rf rf/[FASE]/[EPIC]/RFXXX/RFXXX.yaml \
  --uc rf/[FASE]/[EPIC]/RFXXX/UC-RFXXX.yaml \
  --tc rf/[FASE]/[EPIC]/RFXXX/TC-RFXXX.yaml
```

2. Interpretar o EXIT CODE retornado:
   - Exit code ≠ 0 → execução BLOQUEADA
   - Exit code = 0 → validação APROVADA

3. Atualizar STATUS.yaml SOMENTE se:
   - UC cobre 100% do RF
   - TC cobre 100% dos UCs
   - Nenhum UC cria comportamento fora do RF
   - Todos os UCs obrigatórios (UC00–UC04) existem

4. Registrar no STATUS.yaml:
```yaml
validacoes:
  rf_uc_cobertura_total: true
  uc_md_consistente: true
  uc_wf_consistente: true
  rf_yaml_sincronizado: true
  uc_yaml_sincronizado: true
```

### Proibições

É PROIBIDO:
- Atualizar STATUS.yaml antes da validação
- Fazer commit com validação falhando
- Ignorar exit codes do validador

---

## 4. TODO LIST OBRIGATÓRIA DE CONTRATOS

### Regra Fundamental

Ao ativar QUALQUER contrato de execução (BACKEND, FRONTEND, DOCUMENTACAO, TESTES):

1. **LER** a seção "TODO LIST OBRIGATÓRIA" do contrato **ANTES** de qualquer ação
2. **COPIAR EXATAMENTE** o template de todo list do contrato
3. **SUBSTITUIR** apenas o RFXXX pelo RF real (ex: RF046)
4. **NÃO SIMPLIFICAR** ou omitir itens do template
5. **NÃO INICIAR** nenhuma ação antes da todo list existir

### Itens OBRIGATÓRIOS em Toda Execução

- [ ] Preparar ambiente Git
- [ ] Ler documentação do RF
- [ ] Validar pré-requisitos
- [ ] [Implementação específica do contrato]
- [ ] Validar Critério de Pronto
- [ ] **Atualizar STATUS.yaml**
- [ ] Finalizar Git (commit, merge, push, delete branch)
- [ ] **Sincronizar DevOps** (ver `D:\IC2\sincronizar-devops.txt`)
- [ ] **Verificar resultado final** (Board atualizado)

### Violação

Se o agente criar uma todo list que **NÃO INCLUA** todos os itens do template:
➡️ A execução é considerada **INVALIDA**
➡️ O agente deve **PARAR** e corrigir a todo list

---

## 5. VALIDAÇÃO DE DEPENDÊNCIAS E2E

### Regra de Validação

Ao executar testes E2E para QUALQUER RF:

1. **IDENTIFICAR** todas as dependências funcionais:
   - Analisar MD-RFXXX.md para encontrar FKs
   - Mapear dropdowns que carregam dados externos
   - Listar entidades pai necessárias

2. **VALIDAR** cada dependência ANTES dos testes E2E:
   - Navegar para a rota da dependência
   - Verificar se a tela carrega (HTTP 200)
   - Tentar criar um registro básico

3. **SE FALHAR** qualquer dependência, analisar a causa:

   **Erro no FRONTEND do RF atual:**
   - CORRIGIR o problema
   - Re-executar testes Playwright
   - Repetir até passar

   **Erro em OUTRO RF ou BACKEND:**
   - PARAR a execução
   - Criar arquivo `RELATORIO-ERROS-RFXXX.md` na pasta do RF
   - Listar dependências com erro
   - NÃO marcar o RF como concluído

4. **SETUP E2E** deve criar dados na ordem correta:
   - Primeiro: entidades mais básicas (Empresa)
   - Depois: entidades intermediárias (Filial, Centro de Custo)
   - Por fim: entidade do RF atual (Departamento)

5. **REGISTRO DE EVIDÊNCIA** ao final dos testes:
   - Executar todos os testes CRUD (criar, editar, excluir)
   - Após todos passarem, criar UM registro final
   - NÃO excluir este registro - ele fica como evidência
   - Nomenclatura: `[EVIDENCIA E2E] RFXXX - YYYY-MM-DD HH:MM`

### Violação

Se o agente executar testes E2E SEM validar dependências:
➡️ A execução é considerada **INVALIDA**

Se o agente PARAR por erro de frontend do RF atual (em vez de corrigir):
➡️ A execução é considerada **INCOMPLETA**
➡️ O agente DEVE corrigir e re-testar automaticamente

---

## 6. GOVERNANÇA DE CONTRATO BACKEND

### Princípio Fundamental

**Nenhum teste backend pode ser criado sem contrato explícito.**

O backend DEVE ter um contrato que define:
- Endpoints
- Payloads válidos (tipos, ranges, obrigatoriedade)
- Payloads inválidos (violações)
- Estados possíveis
- Transições de estado permitidas
- Erros esperados (códigos HTTP + mensagens)
- Regras de permissão

### Priorização de Testes

**Testes devem priorizar violação, não fluxo feliz.**

Para cada endpoint, DEVE existir testes que validam:
1. Campo obrigatório ausente → HTTP 400
2. Tipo de dado incorreto → HTTP 400
3. Valor fora do range → HTTP 400
4. Enum inválido → HTTP 400
5. Estado proibido → HTTP 400
6. Acesso sem permissão → HTTP 403
7. Payload com campo extra → HTTP 400
8. Headers inválidos → HTTP 415

### Proibições Absolutas do Backend

**Backend é proibido de aceitar payload fora do contrato.**

O backend NUNCA pode:
- Aceitar payload inválido silenciosamente
- Corrigir dados automaticamente (sanitização não documentada)
- Retornar sucesso (HTTP 2xx) para violação
- Aceitar defaults não documentados
- Ignorar campos extras sem validar

### Gravidade de Violações

**Correções silenciosas são consideradas bugs graves.**

Se o backend aceita uma violação ou corrige dados silenciosamente:
➡️ É considerado um **BUG CRÍTICO**
➡️ Deve ser corrigido sob **CONTRATO DE MANUTENÇÃO**
➡️ NÃO pode avançar para produção

### Bloqueio por Ambiguidade

**Qualquer ambiguidade no contrato bloqueia desenvolvimento.**

Se o contrato backend não definir claramente:
- Tipos de campos
- Obrigatoriedade
- Validações
- Erros esperados

➡️ O agente DEVE PARAR
➡️ Documentar a ambiguidade
➡️ Propor ajuste no contrato
➡️ NÃO inventar regra

### Autoridade do Agente Tester-Backend

**O agente Tester-Backend tem autoridade para bloquear merges.**

Se durante a validação de contrato for identificado que:
- Backend aceita violação
- Backend corrige silenciosamente
- Backend retorna sucesso para payload inválido
- Erros não são estruturados

➡️ O merge para `dev` DEVE ser bloqueado
➡️ O RF NÃO pode avançar
➡️ Correção sob CONTRATO DE MANUTENÇÃO é obrigatória

### Regra de Ouro

**Código que passa teste mas viola contrato é considerado código inválido.**

Não basta o teste passar.
O código DEVE:
- Respeitar o contrato 100%
- Rejeitar todas as violações
- Retornar erros estruturados
- Nunca aceitar o que não está documentado

---

## 7. EXECUTION MANIFEST (OBRIGATÓRIO)

### Quando Criar

Antes de executar QUALQUER ação que envolva:
- Alteração de código
- Execução de testes
- Manutenção
- Debug
- Evolução funcional

### Passos Obrigatórios

O agente DEVE obrigatoriamente:

1. Atualizar o arquivo:
   `contracts/EXECUTION-MANIFEST.md`

2. Declarar:
   - O contrato ativo
   - Tipo de execução
   - RF ou erro relacionado
   - Ambiente alvo

3. Somente APÓS essa atualização,
   qualquer ação técnica pode ser iniciada.

### Violação

Se o agente não puder atualizar o manifesto:
- Ele DEVE PARAR
- Solicitar autorização explícita
- Não executar nenhuma ação

### Manifesto de Deploy

Todo deploy (HOM, PRD ou HOTFIX) DEVE possuir:
- EXECUTION-MANIFEST específico de deploy

Deploy sem manifesto preenchido é considerado INVALIDO.

---

## 8. BRANCH POR RF (AUTOMÁTICA)

### Regra Fundamental

Toda execução sob contrato DEVE ocorrer em um branch dedicado.

Regras:

- 1 Requisito Funcional = 1 branch
- O nome do branch DEVE identificar o RF
- É PROIBIDO executar múltiplos RFs no mesmo branch
- É PROIBIDO executar código diretamente em `dev` ou `main`

### Formato Obrigatório

- `feature/RFXXX-frontend`
- `feature/RFXXX-backend`
- `feature/RFXXX-manutencao`
- `hotfix/RFXXX` (quando aplicável)

### Gerenciamento Automático de Branch (AUTORIZADO)

Antes de qualquer execução, o agente DEVE:

1. Verificar o branch atual
2. Verificar o RF informado no prompt
3. Se estiver em `dev`, `main` ou branch incompatível:
   - Criar automaticamente o branch correto
   - Trocar para esse branch
   - Somente então iniciar a execução

Exemplo de ação autorizada:

```bash
git checkout dev
git pull origin dev
git checkout -b feature/RF046-frontend
```

### Violação

Se o agente NÃO tiver permissão técnica para criar ou trocar branch:
➡️ Ele DEVE PARAR e solicitar autorização explícita.

É PROIBIDO executar código sem branch dedicado.

---

## 9. COMMIT E PR OBRIGATÓRIOS

### Regra Fundamental

Qualquer execução que resulte em:
- Alteração de código
- Atualização de STATUS.yaml
- Execução concluída de FRONTEND ou BACKEND
- Finalização de Testes TI

OBRIGA o agente a:

1. Criar commit no branch do RF
2. Incluir no commit:
   - Código alterado
   - STATUS.yaml atualizado
   - EXECUTION-MANIFEST.md atualizado
3. Garantir que o branch esteja pronto para PR
4. Declarar explicitamente:
   - "Commit realizado"
   - "Branch pronto para PR contra dev"

### Violação

Sem commit:
➡️ A execução é considerada **INCOMPLETA**
➡️ O status **NÃO deve ser atualizado**

Esta regra é **inviolável**.

---

## 10. ENCERRAMENTO DE EXECUÇÃO

### Critérios Obrigatórios

Antes de declarar qualquer execução como CONCLUÍDA, o agente DEVE:

- Executar TODOS os testes exigidos no contrato
- Apresentar evidência objetiva
- Atualizar STATUS.yaml
- Criar commit final
- Estar com branch pronto para PR

### Violação

Se qualquer item falhar:
- A execução NÃO pode ser declarada concluída

---

## 11. ÂNCORA IMUTÁVEL DO PROJETO

### Diretórios e Arquivos Críticos

Os seguintes diretórios e arquivos são considerados **ÂNCORAS IMUTÁVEIS**
da governança do projeto:

- `CLAUDE.md`
- `contracts/*`
- `tools/*`

### Regras

1. Esses artefatos DEVEM existir em todos os branches
2. Eles DEVEM estar sincronizados com `origin/dev`
3. Eles NÃO podem ser removidos, sobrescritos ou ignorados

### Workflow Obrigatório

Antes de criar qualquer branch de execução, o agente DEVE:

1. Executar `git fetch`
2. Executar `git checkout dev`
3. Executar `git pull origin dev`
4. Verificar a presença das âncoras listadas acima
5. Somente então criar o branch do RF

### Violação

Se qualquer âncora estiver ausente:
➡️ O agente DEVE PARAR e declarar BLOQUEIO FORMAL.

É PROIBIDO executar contratos em branches
que não contenham as âncoras atualizadas.

---

## 12. DEPENDÊNCIA ENTRE CONTRATOS

### Ordem Obrigatória (Backend + Frontend)

Quando um RF envolver BACKEND e FRONTEND, a ordem obrigatória é:

1. CONTRATO DE EXECUÇÃO – BACKEND
2. Merge explícito do backend → `dev`
3. Somente então:
   - CONTRATO DE EXECUÇÃO – FRONTEND
   - CONTRATO DE EXECUÇÃO DE TESTES (E2E)

### Regras

- O FRONTEND NÃO PODE assumir código de backend
  que esteja apenas em branch paralelo
- O FRONTEND DEVE sempre usar como base:
  `origin/dev` atualizado

### Violação

Se o backend ainda não estiver mergeado em `dev`:
➡️ O agente DEVE PARAR e solicitar autorização.

Executar frontend sem backend integrado é
considerado violação grave de governança.

---

## 13. CERTIFICAÇÕES E COMPLIANCE REGULATÓRIO

### ISO 27001 (Segurança da Informação)

**Controles Implementados:**
- **A.9.1.1 - Política de Controle de Acesso:** RF-013 (Gestão de Perfis RBAC)
- **A.9.2.1 - Registro de Usuários:** RF-012 (Gestão de Usuários com auditoria)
- **A.12.4.1 - Registro de Eventos:** RF-004 (Auditoria com retenção 7 anos)
- **A.12.4.3 - Logs do Administrador:** RF-004 (Logs de auditoria)

**Artefatos:**
- `auditoria/ACCESS-CONTROL.md`
- `auditoria/AUDIT-TRAIL.md`
- RF-004 (Auditoria)

### SOC 2 (Service Organization Control)

**Princípios Atendidos:**
- **CC6.1 - Acesso Lógico:** RF-013 (RBAC com policies)
- **CC6.2 - Autenticação:** RF-007 (Login com JWT)
- **CC6.3 - Segregação de Funções:** RF-013 (Perfis separados)
- **CC8.1 - Trilha de Auditoria:** RF-004 (Auditoria 7 anos)

**Artefatos:**
- RF-004 (Auditoria) - Retenção 7 anos
- RF-007 (Login) - Autenticação segura

### LGPD (Lei Geral de Proteção de Dados)

**Requisitos Atendidos:**
- **Art. 6º - Princípios:** Soft delete com retenção 7 anos
- **Art. 7º - Consentimento:** RF-080 (Termos LGPD)
- **Art. 46 - Segurança:** Dados criptografados em trânsito (HTTPS)

**Implementação Obrigatória em TODO código:**

```csharp
public class MinhaEntidade
{
    public int Id { get; set; }
    public int ClienteId { get; set; } // Multi-tenancy (isolamento)

    // Soft Delete (retenção 7 anos)
    public bool FlExcluido { get; set; }

    // Auditoria
    public DateTime DataCriacao { get; set; }
    public int UsuarioCriacao { get; set; }
    public DateTime? DataAlteracao { get; set; }
    public int? UsuarioAlteracao { get; set; }
}
```

**Artefatos:**
- `ARCHITECTURE.md` ADR-004
- RF-080 (Termos LGPD)

### SOX (Sarbanes-Oxley)

**Requisitos Atendidos:**
- **Seção 404 - Controles Internos:** Auditoria financeira 7 anos
- **Trilha de Auditoria:** Todos os registros financeiros auditados

**Implementação:**
- RF-004 (Auditoria) - Retenção 7 anos
- Campos de auditoria obrigatórios em todas as entidades financeiras

**Artefatos:**
- RF-004 (Auditoria)

---

## 14. EVIDÊNCIAS DE COMPLIANCE

| Certificação | Evidência | Localização |
|--------------|-----------|-------------|
| ISO 27001 | Matriz de controles | `auditoria/ACCESS-CONTROL.md` |
| SOC 2 | Trilha de auditoria | RF-004 logs |
| LGPD | Soft delete implementado | `ADR-004` + código fonte |
| SOX | Retenção 7 anos | RF-004 configuração |

---

## 15. REGRAS DE NEGAÇÃO ZERO

### Princípio

Se uma solicitação:
- não estiver explicitamente prevista no contrato ativo, ou
- conflitar com qualquer regra do contrato

ENTÃO:

- A execução DEVE ser NEGADA
- Nenhuma ação parcial pode ser realizada
- Nenhum "adiantamento" é permitido

---

## 16. ARQUIVOS TEMPORÁRIOS DA IA

### Regra Fundamental

**PROIBIDO criar arquivos na raiz do projeto (`D:\IC2\`) sem solicitação explícita do usuário.**

### Regras

- Qualquer arquivo criado pela IA que NÃO seja código-fonte solicitado explicitamente DEVE ser criado em `D:\IC2\.temp_ia\`
- Arquivos temporários incluem: relatórios de debug, scripts auxiliares, logs, análises

### Exceções Permitidas (fora de `.temp_ia\`)

- Relatórios de auditoria em `D:\IC2\relatorios\`
- Documentação de governança em `D:\IC2\docs\`
- Código-fonte em `D:\IC2\backend\` ou `D:\IC2\frontend\`

### Exemplos

**✅ CORRETO:**
```
D:\IC2\.temp_ia\RELATORIO-DEBUG-RF028.md
D:\IC2\.temp_ia\analise-gap-backend.md
D:\IC2\.temp_ia\script-validacao-temporario.py
```

**❌ INCORRETO:**
```
D:\IC2\RELATORIO-DEBUG-RF028.md          # ❌ NA RAIZ (proibido)
D:\IC2\analise-gap-backend.md            # ❌ NA RAIZ (proibido)
D:\IC2\script-validacao.py               # ❌ NA RAIZ (proibido)
```

### Violação

Criar arquivos fora de `.temp_ia\` sem solicitação explícita é considerado **execução inválida**.

---

## 17. MODO DE EXECUÇÃO RÍGIDO

### Regras

- O agente NÃO pode negociar escopo
- O agente NÃO pode sugerir execuções fora do contrato ativo
- O agente NÃO pode executar tarefas não explicitamente solicitadas
- O agente NÃO pode "ajudar" fora do contrato
- O agente NÃO pode perguntar "se pode" fazer algo fora do contrato

### Se Solicitação Estiver Fora do Contrato

- O agente DEVE NEGAR
- O agente DEVE explicar o motivo
- O agente DEVE solicitar ajuste formal de contrato

### Violação

Qualquer tentativa de execução fora do contrato invalida a tarefa.

---

## Referências

- **CLAUDE.md** - Governança superior e hierarquia de contratos
- **ARCHITECTURE.md** - Stack tecnológico, padrões arquiteturais
- **CONVENTIONS.md** - Convenções de nomenclatura e código
- **COMMANDS.md** - Comandos de desenvolvimento, validação e deploy
- **DECISIONS.md** - Decisões arquiteturais tomadas
- **contracts/** - Contratos formais de execução
- **tools/README.md** - Ferramentas de validação e sincronização

---

**Última Atualização:** 2026-01-01
**Versão:** 2.0.0 - Redistribuição cirúrgica do D:\IC2\CLAUDE.md
