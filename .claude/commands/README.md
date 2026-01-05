# Comandos Claude - Projeto IControlIT

Comandos de atalho para workflows comuns no projeto IControlIT.

## Comandos Disponíveis

| Comando | Descrição | Quando Usar |
|---------|-----------|-------------|
| **/start-rf** | Iniciar trabalho em um RF | Ao começar desenvolvimento de um RF |
| **/validate-rf** | Validar build, testes e docs | Antes de marcar RF como concluído |
| **/deploy-rf** | Deploy para HOM ou PRD | Após validação completa |
| **/audit-rf** | Auditar conformidade | Antes de marcar RF como concluído |
| **/fix-build** | Corrigir erros de compilação | Quando build falha |
| **/sync-devops** | Sincronizar com Azure DevOps | Após atualizar STATUS.yaml |
| **/sync-todos** | Sincronizar lista de tarefas | (já existente) |

## Como Usar

### 1. /start-rf

Prepara ambiente para trabalhar em um RF.

**Uso:**
```
/start-rf
```

**O que faz:**
- Pergunta qual RF deseja iniciar
- Valida que documentação existe
- Cria branch apropriado
- Verifica ambiente (portas livres)
- Cria checklist de próximos passos

**Exemplo:**
```
Usuário: /start-rf
Agente: Qual RF deseja iniciar?
Usuário: RF-028
Agente: [Prepara ambiente e informa status]
```

---

### 2. /validate-rf

Valida que RF está completo e pronto para produção.

**Uso:**
```
/validate-rf
```

**O que faz:**
- Pergunta qual RF deseja validar
- Valida documentação (5/5)
- Valida STATUS.yaml (100% True)
- Executa build backend
- Executa build frontend
- Executa testes backend
- Executa testes E2E
- Verifica auditoria de conformidade
- Gera relatório de validação

**Exemplo:**
```
Usuário: /validate-rf
Agente: Qual RF deseja validar?
Usuário: RF-028
Agente: [Executa todas as validações e informa resultado]
```

---

### 3. /deploy-rf

Executa deploy de RF para HOM ou PRD.

**Uso:**
```
/deploy-rf
```

**O que faz:**
- Pergunta qual RF e ambiente (HOM/PRD)
- Valida pré-requisitos
- Executa deploy via prompt apropriado
- Atualiza STATUS.yaml
- Sincroniza DevOps

**Exemplo:**
```
Usuário: /deploy-rf
Agente: Qual RF? Qual ambiente (HOM/PRD)?
Usuário: RF-028, HOM
Agente: [Executa deploy e informa resultado]
```

---

### 4. /audit-rf

Executa auditoria de conformidade entre especificação e código.

**Uso:**
```
/audit-rf
```

**O que faz:**
- Pergunta qual RF e escopo (Backend/Frontend/Completo)
- Chama agente `conformance-auditor`
- Aguarda relatório de gaps
- Analisa taxa de conformidade
- Informa se RF está conforme ou não

**Exemplo:**
```
Usuário: /audit-rf
Agente: Qual RF? Qual escopo (Backend/Frontend/Completo)?
Usuário: RF-028, Completo
Agente: [Executa auditoria e gera relatório]
```

---

### 5. /fix-build

Corrige erros de compilação automaticamente.

**Uso:**
```
/fix-build
```

**O que faz:**
- Detecta erros de build (backend/frontend)
- Analisa erros
- Aplica correções automáticas:
  - Adiciona imports faltantes
  - Instala dependências ausentes
  - Resolve conflitos de versão
- Re-executa build

**Exemplo:**
```
Usuário: /fix-build
Agente: [Detecta erros, corrige e re-builda]
```

---

### 6. /sync-devops

Sincroniza STATUS.yaml e user-stories.yaml com Azure DevOps.

**Uso:**
```
/sync-devops
```

**O que faz:**
- Pergunta: 1 RF ou todos?
- Executa `sync-rf.py` ou `sync-all-rfs.py`
- Executa `sync-user-stories.py` se aplicável
- Verifica que Work Items foram atualizados

**Exemplo:**
```
Usuário: /sync-devops
Agente: Sincronizar 1 RF ou todos?
Usuário: RF-028
Agente: [Sincroniza RF-028 com Azure DevOps]
```

---

### 7. /sync-todos

Sincroniza lista de tarefas (já existente).

**Uso:**
```
/sync-todos
```

---

## Workflows Comuns

### Workflow 1: Iniciar Novo RF

```
1. /start-rf → RF-028
2. [Implementar conforme prompts D:\IC2_Governanca\prompts\novo/]
3. /validate-rf → RF-028
4. /audit-rf → RF-028, Completo
5. /sync-devops → RF-028
6. /deploy-rf → RF-028, HOM
```

### Workflow 2: Corrigir Build

```
1. dotnet build (falha)
2. /fix-build
3. dotnet build (sucesso)
```

### Workflow 3: Validar antes de Deploy

```
1. /validate-rf → RF-015
2. [Se falhar, corrigir]
3. /validate-rf → RF-015 (novamente)
4. /audit-rf → RF-015, Completo
5. /deploy-rf → RF-015, HOM
```

## Diferença entre Comandos e Prompts

### Comandos (/comando)
- Atalhos interativos
- Perguntam informações ao usuário
- Executam ações automáticas
- Exemplo: `/start-rf` pergunta qual RF

### Prompts (D:\IC2_Governanca\prompts\)
- Instruções completas de execução
- Usados por agentes especializados
- Seguem contratos formais
- Exemplo: `D:\IC2_Governanca\prompts\novo/02-backend.md`

**Regra:** Comandos são para **uso humano**, prompts são para **uso de agentes**.

## Criando Novos Comandos

Para criar novo comando:

1. Criar arquivo `.claude/commands/novo-comando.md`
2. Adicionar frontmatter YAML:
   ```yaml
   ---
   description: Descrição do comando
   allowed-tools: Read, Bash, TodoWrite
   ---
   ```
3. Documentar instruções detalhadas
4. Adicionar exemplos de uso
5. Atualizar este README.md

## Versionamento

- **Criado em:** 2025-12-23 (sync-todos)
- **Última atualização:** 2025-12-28 (6 novos comandos)
- **Versão:** 2.0.0 (Reorganização completa)

---

**Para mais detalhes sobre agentes, consulte:** `.claude/agents/README.md`

**Para mais detalhes sobre prompts, consulte:** `D:\IC2_Governanca\prompts\README.md`

**Para mais detalhes sobre contratos, consulte:** `D:\IC2_Governanca\contracts\README.md`
