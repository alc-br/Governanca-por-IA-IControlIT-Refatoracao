# VALIDAÇÃO: RESULTADO vs PROCESSO

**Versão:** 1.0
**Data:** 2026-01-10
**Status:** Ativo
**Contexto:** Criado após problema de seed que existia mas falhou silenciosamente

---

## PRINCÍPIO FUNDAMENTAL

**SEMPRE validar RESULTADO, NÃO processo.**

Este é um princípio de **resiliência operacional** que evita travamentos desnecessários quando um processo falha mas o resultado esperado foi alcançado por outro meio.

---

## PROBLEMA IDENTIFICADO

### Situação RF006

**Validação antiga (PROCESSO):**
```yaml
- item: "Validar sincronização de credenciais (MT ↔ Backend Seeds)"
  bloqueante: true  # ❌ TRAVA se processo falhar
  acao_se_falhar: "ABORTAR execução"
```

**O que aconteceu:**
1. Seed **existia** no código (ApplicationDbContextInitialiser.cs)
2. Backend **executou** seed automaticamente ao iniciar
3. Seed **falhou silenciosamente** (ou teve erro desconhecido)
4. **RESULTADO foi alcançado**: Usuário foi criado via outro meio
5. **Sistema travou** porque validação focou no PROCESSO (seed executou?), não no RESULTADO (usuário existe?)

**Impacto:**
- ❌ Travamento desnecessário
- ❌ Perda de tempo investigando processo que já gerou resultado
- ❌ Dependência de processo específico (seed) ao invés de resultado (usuário criado)

---

## SOLUÇÃO: VALIDAR RESULTADO

### Validação nova (RESULTADO)

**Prioridade 1: RESULTADO (bloqueante)**
```yaml
- item: "Validar que usuário de teste EXISTE no banco (RESULTADO)"
  comando: "SELECT COUNT(*) FROM Usuarios WHERE Email = '[EMAIL_MT]'"
  resultado_esperado: "UserExists >= 1"
  bloqueante: true  # ✅ TRAVA se RESULTADO não foi alcançado
  acao_se_falhar: "CRIAR usuário via SQL direto"
  contexto: "VALIDA RESULTADO: usuário existe (independente de como foi criado)"
```

**Prioridade 2: PROCESSO (alertar)**
```yaml
- item: "Validar sincronização de credenciais (MT ↔ Backend Seeds)"
  bloqueante: false  # ✅ NÃO trava, apenas alerta
  acao_se_falhar: "ALERTAR (credenciais MT desatualizadas, mas usuário existe)"
```

**Vantagem:**
- ✅ Se seed funcionar: Ambas validações passam
- ✅ Se seed falhar mas usuário existe: Prossegue com alerta
- ✅ Se seed falhar E usuário não existe: TRAVA com alternativa (SQL direto)

---

## EXEMPLOS DE APLICAÇÃO

### 1. Seeds de Banco de Dados

**❌ ERRADO (validar processo):**
```yaml
- item: "Seed executou sem erros"
  bloqueante: true
```

**✅ CORRETO (validar resultado):**
```yaml
- item: "Dados esperados existem no banco"
  comando: "SELECT COUNT(*) FROM [Tabela] WHERE [Condicao]"
  bloqueante: true
  alternativa: "Se dados não existem, executar INSERT direto"
```

---

### 2. Build de Frontend

**❌ ERRADO (validar processo):**
```yaml
- item: "npm run build executou sem erros"
  bloqueante: true
```

**✅ CORRETO (validar resultado):**
```yaml
- item: "Artefatos de build existem (dist/)"
  comando: "test -d frontend/dist && echo EXISTS"
  bloqueante: true
  alternativa: "Se dist/ não existe, re-executar npm run build"
```

---

### 3. Migrações de Banco

**❌ ERRADO (validar processo):**
```yaml
- item: "Migrations aplicadas sem erro"
  bloqueante: true
```

**✅ CORRETO (validar resultado):**
```yaml
- item: "Schema do banco está atualizado"
  comando: "SELECT * FROM __EFMigrationsHistory WHERE MigrationId = '[ULTIMO_ID]'"
  bloqueante: true
  alternativa: "Se schema desatualizado, aplicar migration"
```

---

### 4. Deploy de Aplicação

**❌ ERRADO (validar processo):**
```yaml
- item: "Deploy command executou sem erros"
  bloqueante: true
```

**✅ CORRETO (validar resultado):**
```yaml
- item: "Aplicação está respondendo (health check)"
  comando: "curl https://app.exemplo.com/health"
  resultado_esperado: "HTTP 200"
  bloqueante: true
  alternativa: "Se health check falhar, re-executar deploy"
```

---

## CHECKLIST DE CONVERSÃO

Para converter validação de PROCESSO → RESULTADO:

1. **Identificar resultado esperado:**
   - O que DEVERIA existir/acontecer se o processo funcionar?

2. **Criar validação direta do resultado:**
   - SQL query, file check, HTTP request, etc.

3. **Tornar validação de resultado BLOQUEANTE:**
   - `bloqueante: true` → TRAVA se resultado não alcançado

4. **Tornar validação de processo NÃO-BLOQUEANTE:**
   - `bloqueante: false` → Apenas alerta

5. **Documentar alternativa:**
   - Se resultado não existe, como alcançá-lo manualmente?

---

## MATRIZ DE DECISÃO

| Validação Processo | Validação Resultado | Decisão |
|-------------------|---------------------|---------|
| ✅ PASS | ✅ PASS | ✅ PROSSEGUIR (ideal) |
| ❌ FAIL | ✅ PASS | ⚠️ ALERTAR + PROSSEGUIR (seed falhou mas resultado OK) |
| ✅ PASS | ❌ FAIL | ❌ TRAVAR (processo passou mas resultado não alcançado - BUG!) |
| ❌ FAIL | ❌ FAIL | ❌ TRAVAR + EXECUTAR ALTERNATIVA (ex: SQL direto) |

---

## IMPLEMENTAÇÃO EM CHECKLISTS

### Template de Validação

```yaml
validacoes:
  # PRIORIDADE 1: RESULTADO (bloqueante)
  - item: "[RESULTADO]: [Descrição do estado final esperado]"
    comando: "[Comando que verifica estado final]"
    resultado_esperado: "[Valor esperado]"
    bloqueante: true
    acao_se_falhar: "EXECUTAR ALTERNATIVA: [Como alcançar resultado manualmente]"
    contexto: "VALIDA RESULTADO: [explicação]"

  # PRIORIDADE 2: PROCESSO (não-bloqueante)
  - item: "[PROCESSO]: [Descrição do processo]"
    comando: "[Comando que verifica processo]"
    resultado_esperado: "[Valor esperado]"
    bloqueante: false
    acao_se_falhar: "ALERTAR: [mensagem]"
    contexto: "VALIDA PROCESSO: [explicação], mas resultado é prioritário"
    mudanca: "DOWNGRADE de bloqueante:true → bloqueante:false"
```

---

## EXCEÇÕES

**Quando PROCESSO deve ser bloqueante:**

1. **Segurança crítica:** Validação de certificados, assinaturas, hashes
2. **Compliance regulatório:** Auditorias obrigatórias por lei
3. **Processo É o resultado:** Logs de execução, timestamps, rastreabilidade

**Exemplo válido de processo bloqueante:**
```yaml
- item: "Commit possui assinatura GPG válida"
  bloqueante: true  # ✅ CORRETO: segurança crítica
```

---

## REFERÊNCIAS

| Documento | Seção |
|-----------|-------|
| `pre-execucao.yaml` | sincronizacao_mt (linhas 72-89) |
| `CLAUDE.md` | 18.2.3 Validação Automática |
| `CONTRATO-MANUTENCAO-CORRECAO-CONTROLADA.md` | FASE 1: Análise de seed |

---

## CHANGELOG

### v1.0 (2026-01-10)
- Criação do processo após problema de seed em RF006
- Definição do princípio: VALIDAR RESULTADO, NÃO PROCESSO
- Exemplos de aplicação (seeds, build, migrations, deploy)
- Checklist de conversão de validações
- Matriz de decisão
- Template para implementação em checklists

---

**Mantido por:** Time de Governança IControlIT
**Última Atualização:** 2026-01-10
**Versão:** 1.0
