# CONTRATO DE ROLLBACK

**Versão:** 1.0
**Data de criação:** 2025-12-26
**Tipo de execução:** DECISÓRIA (Crítica)
**Autoridade:** DevOps / Release Manager

---

## NATUREZA DESTE CONTRATO

Este é um contrato de **EXECUÇÃO DECISÓRIA CRÍTICA**.

Rollback é uma operação de emergência que:
- Reverte ambiente produtivo para estado anterior seguro
- É acionado por falha de deploy ou incidente crítico
- Requer rastreabilidade completa
- Tem prioridade sobre qualquer outro contrato

---

## FONTE DA VERDADE

A **ÚNICA fonte da verdade** é o arquivo:

```
contracts/EXECUTION-MANIFEST.md
```

Rollback DEVE ter:
- Manifesto do deploy original
- Motivo formal do rollback
- Decisão registrada

---

## GATILHOS AUTOMÁTICOS (OBRIGATÓRIOS)

Rollback DEVE ser executado AUTOMATICAMENTE quando:

### 1. Falha de Smoke Test

Se qualquer smoke test pós-deploy falhar:
- ❌ Backend health check falhou
- ❌ Frontend não acessível
- ❌ Autenticação não funciona
- ❌ Banco de dados não acessível

➡️ **ROLLBACK AUTOMÁTICO**

### 2. Erro Crítico em Produção

Se após deploy for detectado:
- ❌ Taxa de erro > 5%
- ❌ Downtime > 30 segundos
- ❌ Perda de dados
- ❌ Falha de segurança

➡️ **ROLLBACK AUTOMÁTICO**

### 3. Violação de Contrato

Se foi detectado que:
- ❌ Deploy ocorreu sem contrato
- ❌ Deploy alterou código durante execução
- ❌ Deploy pulou validações

➡️ **ROLLBACK OBRIGATÓRIO**

---

## GATILHOS MANUAIS (AUTORIZADOS)

Rollback PODE ser executado MANUALMENTE quando:

### 1. Decisão de Negócio

- Funcionalidade causa impacto negativo não previsto
- Requisição formal de Product Owner
- Descoberta de bug não crítico mas bloqueante

### 2. Planejado

- Teste de procedimento de rollback
- Validação de processo de emergência
- Treinamento de equipe

---

## PRÉ-REQUISITOS OBRIGATÓRIOS

Para executar rollback, DEVEM existir:

### 1. Manifesto do Deploy Original

No EXECUTION-MANIFEST, DEVE existir:

- ID do deploy original
- Hash do commit deployado
- Versão deployada
- Ambiente de destino
- Timestamp do deploy

### 2. Motivo Formal

Rollback DEVE ter motivo documentado:

- Tipo de gatilho (automático / manual)
- Descrição do problema
- Impacto observado
- Autoridade que solicitou (se manual)

### 3. Versão Anterior Conhecida

DEVE ser possível identificar:

- Hash do commit anterior
- Versão anterior
- Estado do banco de dados anterior (se aplicável)

---

## PROCESSO DE ROLLBACK

### Passo 1: Validação de Gatilho

- Identificar gatilho (automático/manual)
- Validar manifesto do deploy original
- Validar motivo formal
- **SE MANUAL:** Validar autorização

### Passo 2: Identificação de Versão Anterior

- Ler EXECUTION-MANIFEST
- Encontrar último deploy APROVADO anterior
- Extrair hash do commit
- Extrair versão

### Passo 3: Rollback de Código

- Reverter App Service (backend) para versão anterior
- Reverter Static Web App (frontend) para versão anterior
- **NÃO alterar código** (apenas reverter deploy)

### Passo 4: Rollback de Banco de Dados (SE NECESSÁRIO)

⚠️ **ATENÇÃO:** Rollback de banco é complexo e arriscado

- **SE migrations foram executadas:**
  - Avaliar se migration é reversível
  - Executar migration down (se disponível)
  - **SE NÃO reversível:** Registrar limitação

- **SE dados foram alterados:**
  - **NÃO tentar reverter dados automaticamente**
  - Registrar que dados não foram revertidos
  - Escalar para DBA

### Passo 5: Smoke Tests Pós-Rollback

- Validar que aplicação iniciou
- Validar endpoints críticos
- Validar autenticação
- **SE FALHAR:** Escalar para equipe de infra

### Passo 6: Registro no Manifesto

- Registrar execução de rollback
- Registrar versão revertida
- Registrar motivo
- Registrar decisão (APROVADO)

### Passo 7: Atualização de STATUS.yaml

- Atualizar `devops.last_rollback`
- Atualizar `devops.rollback_reason`
- Atualizar `devops.current_version` (versão anterior)
- Atualizar `devops.board_column` para "Rollback Executado"

---

## ESCOPO PERMITIDO

Durante rollback, o agente PODE:

- ✅ Reverter versão de App Service
- ✅ Reverter versão de Static Web App
- ✅ Executar migrations down (se disponível)
- ✅ Executar smoke tests
- ✅ Registrar no EXECUTION-MANIFEST
- ✅ Atualizar STATUS.yaml

---

## PROIBIÇÕES ABSOLUTAS

Durante rollback, é **PROIBIDO**:

- ❌ Alterar código fonte
- ❌ Executar hotfix
- ❌ Corrigir bugs durante rollback
- ❌ Tentar "consertar" o deploy falhado
- ❌ Pular validações
- ❌ Rollback sem registro no manifesto
- ❌ Alterar dados manualmente no banco

---

## ROLLBACK AUTOMÁTICO (IMPLEMENTAÇÃO)

Quando smoke test falha, o script de deploy DEVE:

```python
def execute_deploy():
    # ... deploy code ...

    # Smoke tests
    if not run_smoke_tests():
        print("[CRÍTICO] Smoke tests falharam")
        print("[AUTOMÁTICO] Executando rollback...")

        # Chamar script de rollback
        subprocess.run([
            "python",
            "tools/devops-sync/apply_rollback.py",
            rf,
            "--automatic",
            "--reason", "Smoke tests failed"
        ])

        abort("Deploy abortado - Rollback executado")
```

---

## SAÍDAS OBRIGATÓRIAS

Ao final do rollback, DEVEM existir:

### 1. Registro no EXECUTION-MANIFEST

```markdown
# EXECUCAO: <ID_UNICO>

## TIPO DE EXECUCAO

- Tipo: DECISORIA (CRÍTICA)

## CONTRATO ATIVO

- Contrato: CONTRATO-ROLLBACK
- RF: RFXXX
- Data: YYYY-MM-DD HH:MM:SS
- Executor: DevOps Agent

## ROLLBACK EXECUTADO

- Gatilho: AUTOMÁTICO | MANUAL
- Motivo: <motivo>
- Deploy Original: <id_deploy>
- Versão Revertida: <versao>
- Commit Revertido: <hash>
- Ambiente: HOM | PRD

## SMOKE TESTS PÓS-ROLLBACK

- [x] Backend health: PASS
- [x] Frontend acessível: PASS
- [x] Autenticação: PASS

## DECISAO FORMAL

decision:
  resultado: APROVADO
  autoridade: DevOps-Agent
  contrato: CONTRATO-ROLLBACK
  motivo: <motivo>
```

### 2. STATUS.yaml Atualizado

```yaml
devops:
  last_rollback: "2025-12-26 15:00:00"
  rollback_reason: "Smoke tests failed"
  current_version: "1.2.2" # versão anterior
  deployed_commit: "xyz789abc123" # commit anterior
  board_column: "Rollback Executado"
```

### 3. Evidências

- Logs de rollback
- Resultado de smoke tests pós-rollback
- Screenshot de ambiente restaurado
- Timeline do incidente

---

## LIMITAÇÕES DO ROLLBACK

### Banco de Dados

⚠️ **Rollback de banco é limitado:**

- Migrations podem não ser reversíveis
- Dados criados após deploy NÃO serão removidos
- Estrutura pode estar incompatível com código anterior

**Recomendação:**
- Sempre criar migrations reversíveis
- Testar migration down em HOM antes de PRD
- Ter backup do banco antes de deploy

### Dados de Usuário

⚠️ **Dados de usuário NÃO são revertidos:**

- Registros criados após deploy permanecem
- Uploads de arquivos permanecem
- Histórico de auditoria permanece

**Recomendação:**
- Rollback é para CÓDIGO, não para DADOS
- Se dados precisam ser revertidos, envolver DBA

---

## REGRA DE AUDITORIA

Rollback é auditável e DEVE ser rastreável:

- Por que foi necessário? → Motivo no manifesto
- Quando ocorreu? → Timestamp no manifesto
- Qual versão foi revertida? → Hash do commit
- Qual ambiente? → HOM / PRD
- Foi bem-sucedido? → Smoke tests pós-rollback
- O que não foi revertido? → Limitações registradas

---

## AUTOMAÇÃO

Este contrato DEVE ser executado pelo script:

```bash
# Rollback automático (chamado pelo script de deploy)
python tools/devops-sync/apply_rollback.py RFXXX --automatic --reason "Smoke tests failed"

# Rollback manual
python tools/devops-sync/apply_rollback.py RFXXX --manual --reason "Business decision" --authorized-by "Release Manager"
```

O script DEVE:
- Validar gatilho
- Validar autorização (se manual)
- Identificar versão anterior
- Executar rollback
- Executar smoke tests pós-rollback
- Registrar no EXECUTION-MANIFEST
- Atualizar STATUS.yaml

---

## PROIBIÇÃO DE HOTFIX DURANTE ROLLBACK

❌ **É ABSOLUTAMENTE PROIBIDO:**

- Executar hotfix ao invés de rollback
- "Consertar rapidamente" o problema
- Fazer "apenas um ajuste" no código

✅ **REGRA ABSOLUTA:**

1. Rollback PRIMEIRO
2. Ambiente estável DEPOIS
3. Correção em DEV DEPOIS
4. Novo deploy (com contrato) DEPOIS

---

## COMUNICAÇÃO OBRIGATÓRIA

Se rollback for executado em PRD:

- Comunicar imediatamente ao Product Owner
- Comunicar à equipe de suporte
- Comunicar aos usuários (se necessário)
- Registrar incident report

---

## REGRA FINAL

**Rollback não é falha.**
**Rollback é proteção.**
**Rollback é governança.**

Nenhuma exceção manual é permitida.
Nenhum hotfix substitui rollback.
Todo rollback DEVE ser auditável.

---

## VIOLAÇÃO DESTE CONTRATO

Se qualquer regra for violada:

➡️ O rollback é considerado **INVÁLIDO**
➡️ Ambiente DEVE ser considerado **INSTÁVEL**
➡️ Acesso ao ambiente DEVE ser revisado
➡️ Investigação formal DEVE ser iniciada
➡️ Processo de rollback DEVE ser reavaliado

---

**FIM DO CONTRATO**
