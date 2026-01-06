# CHECKLIST: Manutenção Avançada

**Contrato:** D:\IC2_Governanca\contracts\desenvolvimento\manutencao\manutencao-avancada.md
**Prompt:** D:\IC2_Governanca\prompts\desenvolvimento\manutencao\manutencao-avancada.md

---

## FASE 0: APROVAÇÃO OBRIGATÓRIA (BLOQUEANTE)

### Validação de Necessidade

- [ ] Problema NÃO pode ser resolvido com Manutenção Controlada (escopo > 3 arquivos ou cross-layer)
- [ ] Problema NÃO pode ser resolvido com Manutenção Completa (requer mudanças arquiteturais)
- [ ] Justificativa documentada explicando por que outras manutenções não resolvem

### Identificação de Mudanças Arquiteturais

- [ ] Todas as mudanças arquiteturais propostas foram listadas
- [ ] Cada mudança tem descrição clara
- [ ] Cada mudança tem impacto identificado
- [ ] Cada mudança tem nível de risco atribuído (Baixo/Médio/Alto)

### Apresentação ao Usuário

- [ ] Resumo das mudanças exibido em formato claro
- [ ] Riscos explicitados
- [ ] Autorização explícita solicitada (SIM/NÃO)

### Decisão de Aprovação

- [ ] Usuário autorizou explicitamente (SIM) ✅ **PROSSEGUIR**
- [ ] Usuário negou (NÃO) ❌ **PARAR E NÃO EXECUTAR**

⚠️ **SE NEGADO:** Parar execução imediatamente. Não prosseguir.

---

## FASE 1: ANÁLISE DE CAUSA RAIZ

### Investigação Inicial

- [ ] Problema reproduzido localmente
- [ ] Logs de erro coletados
- [ ] Screenshots de evidência capturados (se aplicável)
- [ ] Testes falhando identificados (TCs específicos)

### Identificação de Arquivos Afetados

- [ ] Migrations afetadas listadas (quantidade e período)
- [ ] Model snapshot analisado (ApplicationDbContextModelSnapshot.cs)
- [ ] Arquivos de infraestrutura identificados
- [ ] Arquivos de configuração de testes identificados

### Mapeamento de Causa Raiz

- [ ] Causa raiz identificada claramente
- [ ] Histórico de mudanças analisado (git log)
- [ ] Dependências entre migrations mapeadas
- [ ] Incompatibilidades de tipos identificadas (se aplicável)

### Documentação de Análise

- [ ] Arquivo `.temp_ia/ANALISE-CAUSA-RAIZ-[PROBLEMA].md` criado
- [ ] Análise contém: problema, causa raiz, arquivos afetados, evidências
- [ ] Análise contém recomendação de estratégia de refatoração

---

## FASE 2: PLANEJAMENTO DE REFATORAÇÃO

### Escolha de Estratégia

Estratégia selecionada:
- [ ] **A: Incremental** (corrigir migrations uma a uma, manter histórico)
- [ ] **B: Consolidação** (consolidar migrations, simplificar histórico)
- [ ] **C: Recriação** (drop database, criar do zero, perda de histórico)

### Validação de Estratégia

Se **Estratégia A (Incremental)**:
- [ ] Quantidade de migrations é viável (< 20)
- [ ] Cada migration pode ser corrigida isoladamente
- [ ] Histórico pode ser preservado

Se **Estratégia B (Consolidação)**:
- [ ] Migrations a consolidar identificadas (ex: 2025-11-05 até 2026-01-06)
- [ ] Migration consolidada terá nome claro (ex: `20260106_ConsolidatedMigrations.cs`)
- [ ] Snapshot será regenerado após consolidação

Se **Estratégia C (Recriação)**:
- [ ] Database está em ambiente dev (NUNCA produção)
- [ ] Perda de histórico é aceitável
- [ ] Seeds funcionais estão atualizados para repovoar dados

### Plano de Execução

- [ ] Ordem de execução definida (por fase)
- [ ] Comandos específicos documentados
- [ ] Pontos de validação identificados (build, test)
- [ ] Plano de rollback definido (backup + restore)

### Documentação de Plano

- [ ] Arquivo `.temp_ia/PLANO-REFATORACAO-[PROBLEMA].md` criado
- [ ] Plano contém: estratégia escolhida, ordem de execução, comandos, pontos de validação

---

## FASE 3: EXECUÇÃO DA REFATORAÇÃO

### Backup Obrigatório (Antes de Qualquer Mudança)

- [ ] Backup de migrations criado (`backup-migrations-[DATA].zip`)
- [ ] Backup de model snapshot criado (`backup-snapshot-[DATA].cs`)
- [ ] Backup de arquivos de configuração (se aplicável)
- [ ] Backup salvo em `.temp_ia/BACKUP-MIGRATIONS-[DATA].zip`

### Execução por Fase

**FASE 3.1: Preparação**
- [ ] Branch `dev` confirmado (git branch)
- [ ] Working directory limpo (git status)
- [ ] Docker rodando (docker ps) - se necessário

**FASE 3.2: Refatoração de Migrations**

Se **Estratégia A (Incremental)**:
- [ ] Migrations corrigidas uma a uma
- [ ] Tipos SQLite convertidos para SQL Server (TEXT→nvarchar(max), INTEGER→int)
- [ ] Cada migration validada individualmente

Se **Estratégia B (Consolidação)**:
- [ ] Migrations antigas removidas (ex: 40 migrations)
- [ ] Migration consolidada criada
- [ ] Migration consolidada contém TODAS as mudanças de schema

Se **Estratégia C (Recriação)**:
- [ ] Database dropado (dotnet ef database drop --force)
- [ ] Migrations removidas (exceto inicial)
- [ ] Migration inicial recriada (dotnet ef migrations add InitialCreate)

**FASE 3.3: Regeneração de Model Snapshot**
- [ ] ApplicationDbContextModelSnapshot.cs analisado
- [ ] Tipos incompatíveis identificados (ex: TEXT, INTEGER)
- [ ] Snapshot regenerado (dotnet ef migrations remove + add)
- [ ] Snapshot validado (tipos SQL Server corretos)

**FASE 3.4: Validação de Compilação**
- [ ] Backend compila sem erros (dotnet build)
- [ ] Frontend compila sem erros (npm run build) - se aplicável
- [ ] Nenhum warning crítico de migrations

⚠️ **SE COMPILAÇÃO FALHAR:** Parar e reverter mudanças usando backup.

---

## FASE 4: VALIDAÇÃO COMPLETA

### Aplicação de Migrations

- [ ] Database atualizado (dotnet ef database update)
- [ ] Migrations aplicadas sem erros
- [ ] Schema do banco validado (verificar tabelas criadas)

### Execução de Testes Backend

- [ ] Domain.UnitTests: 5/5 passando
- [ ] Application.UnitTests: 26/26 passando
- [ ] Application.FunctionalTests: 23/23 passando (com Docker)
- [ ] **Total: 54/54 testes passando (100%)**

⚠️ **SE QUALQUER TESTE FALHAR:** Parar e reverter mudanças.

### Execução de Testes Frontend (se aplicável)

- [ ] Testes unitários passando (npm run test)
- [ ] Testes de componentes passando
- [ ] Testes E2E passando (npm run e2e) - se aplicável

### Validação de Funcionalidade

- [ ] Backend iniciado sem erros (dotnet run)
- [ ] Endpoint /health responde (200 OK)
- [ ] Seeds aplicados corretamente
- [ ] Frontend iniciado sem erros (npm start) - se aplicável
- [ ] Funcionalidade do RF validada manualmente (smoke test)

---

## FASE 5: COMMIT E DOCUMENTAÇÃO

### Preparação do Commit

- [ ] Working directory limpo (apenas mudanças intencionais)
- [ ] Arquivos temporários removidos (exceto `.temp_ia/`)
- [ ] Backup files removidos do commit

### Estrutura da Mensagem de Commit

- [ ] Mensagem segue padrão:
  ```
  feat(infra): [descrição da refatoração]

  MANUTENÇÃO AVANÇADA - [PROBLEMA]

  Mudanças arquiteturais:
  - [Mudança 1]
  - [Mudança 2]

  Validação:
  - Testes: 54/54 passando (100%)
  - Compilação: ✅ backend + ✅ frontend

  Refs: RFXXX, UCXX

  🤖 Generated with Claude Code
  Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
  ```

### Atualização de Decisões

- [ ] Arquivo `DECISIONS.md` atualizado
- [ ] Decisão arquitetural documentada
- [ ] Justificativa incluída (por que mudança foi necessária)
- [ ] Alternativas consideradas documentadas
- [ ] Impacto futuro analisado

### Commit Executado

- [ ] Commit realizado em `dev`
- [ ] Commit contém APENAS mudanças relacionadas
- [ ] Mensagem de commit clara e estruturada
- [ ] Co-autoria do Claude incluída

---

## FASE 6: RELATÓRIO FINAL

### Evidências Geradas

- [ ] `.temp_ia/ANALISE-CAUSA-RAIZ-[PROBLEMA].md` criado
- [ ] `.temp_ia/PLANO-REFATORACAO-[PROBLEMA].md` criado
- [ ] `.temp_ia/BACKUP-MIGRATIONS-[DATA].zip` criado (se aplicável)
- [ ] `.temp_ia/RELATORIO-MANUTENCAO-AVANCADA-[PROBLEMA].md` criado

### Conteúdo do Relatório Final

Relatório deve conter:

- [ ] **Resumo Executivo** (problema, estratégia, resultado)
- [ ] **Causa Raiz Identificada**
- [ ] **Mudanças Arquiteturais Realizadas**
- [ ] **Migrations Afetadas** (antes e depois)
- [ ] **Validação de Testes** (54/54 = 100%)
- [ ] **Decisões Tomadas** (e por quê)
- [ ] **Riscos Mitigados**
- [ ] **Impacto Futuro**

### Validação de Relatório

- [ ] Relatório está completo
- [ ] Relatório está objetivo e técnico
- [ ] Relatório documenta TODAS as mudanças arquiteturais
- [ ] Relatório pode ser usado como referência futura

---

## CRITÉRIO DE APROVAÇÃO FINAL

### Aprovação (✅ MANUTENÇÃO AVANÇADA CONCLUÍDA)

Todos os itens abaixo DEVEM ser verdadeiros:

- [ ] Autorização do usuário foi obtida (FASE 0)
- [ ] Análise de causa raiz concluída (FASE 1)
- [ ] Plano de refatoração documentado (FASE 2)
- [ ] Backup criado antes de mudanças (FASE 3)
- [ ] Refatoração executada conforme plano (FASE 3)
- [ ] Backend compila sem erros (FASE 3.4)
- [ ] Frontend compila sem erros (FASE 3.4) - se aplicável
- [ ] Migrations aplicadas sem erros (FASE 4)
- [ ] **Testes backend: 54/54 passando (100%)** (FASE 4)
- [ ] Testes frontend passando (FASE 4) - se aplicável
- [ ] Funcionalidade validada (smoke test) (FASE 4)
- [ ] Commit estruturado realizado (FASE 5)
- [ ] DECISIONS.md atualizado (FASE 5)
- [ ] Relatório final gerado (FASE 6)
- [ ] Todas as evidências criadas (FASE 6)

### Reprovação (❌ MANUTENÇÃO AVANÇADA BLOQUEADA)

**PARAR IMEDIATAMENTE** se qualquer condição abaixo ocorrer:

- [ ] Usuário negou autorização (FASE 0) → **PARAR**
- [ ] Compilação falhou após refatoração (FASE 3.4) → **REVERTER + PARAR**
- [ ] Testes < 100% (ex: 53/54) (FASE 4) → **REVERTER + PARAR**
- [ ] Migrations falharam ao aplicar (FASE 4) → **REVERTER + PARAR**
- [ ] Funcionalidade quebrou (smoke test) (FASE 4) → **REVERTER + PARAR**

⚠️ **EM CASO DE REPROVAÇÃO:**
1. Reverter mudanças usando backup criado em FASE 3
2. Gerar relatório de falha em `.temp_ia/RELATORIO-FALHA-MANUTENCAO-AVANCADA-[PROBLEMA].md`
3. Documentar causa da falha
4. Sugerir alternativas ou investigação adicional

---

## PROIBIÇÕES CRÍTICAS

Durante TODA a execução, é **PROIBIDO**:

❌ Executar sem aprovação explícita do usuário (FASE 0)
❌ Pular backup antes de mudanças críticas (FASE 3)
❌ Consolidar migrations sem validar histórico
❌ Regenerar snapshot sem validar tipos de dados
❌ Commitar se testes não estiverem 100% passando
❌ Modificar migrations já aplicadas em produção
❌ Alterar contratos de infraestrutura sem documentar em DECISIONS.md
❌ Executar em branch diferente de `dev`
❌ Fazer múltiplos commits (deve ser commit único ao final)
❌ Omitir atualização de DECISIONS.md

---

## REGRAS DE ROLLBACK

Se qualquer fase falhar, executar rollback:

1. **Restaurar migrations do backup:**
   ```bash
   # Extrair backup
   Expand-Archive -Path .temp_ia/BACKUP-MIGRATIONS-[DATA].zip -DestinationPath backend/IControlIT.API/src/Infrastructure/Data/Migrations/

   # Reverter snapshot
   cp .temp_ia/backup-snapshot-[DATA].cs backend/IControlIT.API/src/Infrastructure/Data/ApplicationDbContextModelSnapshot.cs
   ```

2. **Reverter mudanças git (se houver):**
   ```bash
   git reset --hard HEAD
   git clean -fd
   ```

3. **Validar estado consistente:**
   ```bash
   dotnet build
   dotnet test
   ```

4. **Gerar relatório de falha:**
   - Documentar em `.temp_ia/RELATORIO-FALHA-MANUTENCAO-AVANCADA-[PROBLEMA].md`
   - Incluir: causa da falha, fase que falhou, estado atual, próximos passos

---

## RESUMO DE VALIDAÇÃO

| Fase | Critério de Aprovação | Ação se Falhar |
|------|----------------------|----------------|
| **FASE 0** | Autorização do usuário obtida | PARAR (não executar) |
| **FASE 1** | Análise de causa raiz completa | Solicitar mais investigação |
| **FASE 2** | Plano de refatoração aprovado | Revisar estratégia |
| **FASE 3** | Compilação 100% | REVERTER + PARAR |
| **FASE 4** | Testes 100% (54/54) | REVERTER + PARAR |
| **FASE 5** | Commit + DECISIONS.md | Corrigir e retentar |
| **FASE 6** | Relatório completo | Complementar documentação |

---

**LEMBRETE FINAL:**

Manutenção Avançada é a modalidade **MAIS PERMISSIVA** de manutenção, mas também a **MAIS ARRISCADA**.

Por isso:
- ✅ Autorização explícita é OBRIGATÓRIA
- ✅ Backup é OBRIGATÓRIO
- ✅ Validação 100% de testes é OBRIGATÓRIA
- ✅ Rollback imediato se qualquer fase falhar

**Qualquer desvio destas regras invalida a execução.**
