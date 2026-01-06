# PROMPT: Manutenção Avançada

**Contrato:** D:\IC2_Governanca\contracts\desenvolvimento\manutencao\manutencao-avancada.md
**Checklist:** D:\IC2_Governanca\checklists\desenvolvimento\manutencao\manutencao-avancada.md

---

## CONTEXTO

Execute manutenção avançada conforme contrato de Manutenção Avançada para corrigir o seguinte problema no [backend/frontend] do **[RFXXX]**:

---

## PROBLEMA IDENTIFICADO

**Descrição:**
[Descreva o problema que requer manutenção avançada]

**Evidências:**
- Screenshot: [caminho para screenshot, se houver]
- Log: [caminho para log, se houver]
- Testes falhando: [lista de TCs falhando]

---

## POR QUE MANUTENÇÃO AVANÇADA?

**Bloqueios de Manutenção Controlada:**
- [ ] Escopo excede 3 arquivos
- [ ] Problema não isolado em 1 camada
- [ ] Requer refatoração estrutural

**Bloqueios de Manutenção Completa:**
- [ ] Requer consolidação de migrations
- [ ] Requer regeneração de model snapshot
- [ ] Requer mudanças arquiteturais na infraestrutura
- [ ] Requer refatoração de estratégia de testes

**Motivo específico:**
[Explique por que Manutenção Controlada e Completa não puderam resolver]

---

## MUDANÇAS ARQUITETURAIS PROPOSTAS

Liste as mudanças arquiteturais necessárias:

1. **[Mudança 1]:**
   - Descrição: [ex: Consolidar 40 migrations de 2025-11-05 até 2026-01-06]
   - Impacto: [ex: Remove migrations antigas, mantém histórico em snapshot]
   - Risco: [ex: Baixo - migrations já aplicadas em dev]

2. **[Mudança 2]:**
   - Descrição: [ex: Regenerar ApplicationDbContextModelSnapshot com tipos SQL Server]
   - Impacto: [ex: Corrige incompatibilidades SQLite→SQL Server]
   - Risco: [ex: Médio - requer validação completa de testes]

3. **[Mudança 3]:**
   - Descrição: [ex: Aplicar value converters para compatibilidade cross-database]
   - Impacto: [ex: Garante portabilidade SQLite/SQL Server]
   - Risco: [ex: Baixo - padrão estabelecido por EF Core]

[Adicione mais mudanças conforme necessário]

---

## AUTORIZAÇÃO (OBRIGATÓRIA)

🚨 **MANUTENÇÃO AVANÇADA - APROVAÇÃO NECESSÁRIA**

**MUDANÇAS ARQUITETURAIS PROPOSTAS:**
[Liste resumidamente as mudanças acima]

**VOCÊ AUTORIZA ESTAS MUDANÇAS ARQUITETURAIS?**
- [ ] **SIM** - Prosseguir com manutenção avançada
- [ ] **NÃO** - Cancelar e manter bloqueio atual

⚠️ **ATENÇÃO:** Manutenção Avançada permite:
- Consolidação de migrations
- Regeneração de model snapshot
- Refatoração de infraestrutura
- Mudanças em estratégia de testes

---

## CONTEXTO TÉCNICO

**RF:** [RFXXX]
**UC:** [UCXX]
**Handlers afetados:** [lista de handlers]
**Repositories afetados:** [lista de repositories]
**Migrations afetadas:** [quantidade e período]
**Testes falhando:** [quantidade/total]

---

## MODO DE EXECUÇÃO

Modo governança rígida. Não negociar escopo. Não extrapolar.
Seguir rigorosamente D:\IC2\CLAUDE.md e contrato ativado.

---

## WORKFLOW OBRIGATÓRIO

O agente DEVE seguir as fases do contrato:

### FASE 0: APROVAÇÃO OBRIGATÓRIA (BLOQUEANTE)
- Exibir resumo das mudanças arquiteturais
- Aguardar autorização explícita do usuário
- Se negado: PARAR e não prosseguir

### FASE 1: ANÁLISE DE CAUSA RAIZ
- Investigar causa raiz do problema
- Identificar arquivos/migrations afetados
- Gerar análise em `.temp_ia/ANALISE-CAUSA-RAIZ-[PROBLEMA].md`

### FASE 2: PLANEJAMENTO DE REFATORAÇÃO
- Escolher estratégia (A: Incremental, B: Consolidação, C: Recriação)
- Criar plano detalhado em `.temp_ia/PLANO-REFATORACAO-[PROBLEMA].md`
- Definir ordem de execução

### FASE 3: EXECUÇÃO DA REFATORAÇÃO
- Criar backup obrigatório antes de qualquer mudança
- Executar mudanças por fase
- Validar compilação após CADA fase
- Se compilação falhar: PARAR e reverter

### FASE 4: VALIDAÇÃO COMPLETA
- Executar suite completa de testes (54/54 testes)
- Se qualquer teste falhar: PARAR e reverter
- Critério de aprovação: 100% de testes passando

### FASE 5: COMMIT E DOCUMENTAÇÃO
- Commit estruturado com mensagem detalhada
- Atualizar DECISIONS.md com decisões arquiteturais
- Gerar relatório final em `.temp_ia/RELATORIO-MANUTENCAO-AVANCADA-[PROBLEMA].md`

---

## EVIDÊNCIAS OBRIGATÓRIAS

Ao final, gerar em `.temp_ia/`:

- `ANALISE-CAUSA-RAIZ-[PROBLEMA].md`
- `PLANO-REFATORACAO-[PROBLEMA].md`
- `RELATORIO-MANUTENCAO-AVANCADA-[PROBLEMA].md`
- `BACKUP-MIGRATIONS-[DATA].zip` (se aplicável)

---

## PROIBIÇÕES

❌ **NUNCA:**
- Executar sem aprovação explícita do usuário
- Pular backup antes de mudanças críticas
- Consolidar migrations sem validar histórico
- Regenerar snapshot sem validar tipos de dados
- Commitar se testes não estiverem 100% passando
- Modificar migrations já aplicadas em produção
- Alterar contratos de infraestrutura sem documentar

---

## REGRAS CRÍTICAS DE GIT

- **BRANCH:** Sempre executar em `dev`
- **COMMITS:** Commit único e estruturado ao final (se aprovado)
- **MENSAGEM:** Deve incluir:
  ```
  feat(infra): [descrição da refatoração]

  MANUTENÇÃO AVANÇADA - [PROBLEMA]

  Mudanças arquiteturais:
  - [Mudança 1]
  - [Mudança 2]
  - [Mudança 3]

  Validação:
  - Testes: 54/54 passando (100%)
  - Compilação: ✅ backend + ✅ frontend

  Refs: RFXXX, UCXX

  🤖 Generated with Claude Code
  Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
  ```

---

## CRITÉRIO DE PRONTO

✅ **APROVAÇÃO:**
- Autorização explícita do usuário obtida
- Análise de causa raiz concluída e documentada
- Plano de refatoração aprovado
- Backup criado (se aplicável)
- Mudanças executadas por fase
- Compilação aprovada (backend + frontend)
- Suite completa de testes aprovada (54/54 = 100%)
- Commit estruturado realizado
- DECISIONS.md atualizado
- Relatório final gerado

❌ **REPROVAÇÃO:**
- Qualquer fase falhar
- Testes < 100%
- Compilação quebrar
- Usuário negar autorização

---

**MODO AUTONOMIA TOTAL (APÓS APROVAÇÃO):**
- Executar todas as fases automaticamente
- Não perguntar permissões intermediárias
- Gerar evidências sem intervenção manual
- Parar imediatamente se qualquer validação falhar
