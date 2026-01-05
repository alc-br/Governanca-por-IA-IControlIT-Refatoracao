# PROMPT: Correção Sistêmica Cross-RF

**Versão:** 1.0
**Data:** 2026-01-05
**Contrato Ativado:** `docs/contracts/manutencao/correcao-sistemica-cross-rf.md`

---

## 🎯 OBJETIVO

Executar correção técnica/infraestrutural que afeta múltiplos RFs simultaneamente, mantendo validação individual de escopo por RF.

---

## 📋 PRÉ-REQUISITOS OBRIGATÓRIOS

Antes de usar este prompt, você DEVE:

1. ✅ Confirmar que correção é TÉCNICA/INFRAESTRUTURAL (não funcional)
2. ✅ Confirmar que correção está na LISTA FECHADA de correções autorizadas
3. ✅ Confirmar que tem acesso aos WF/UC-RFXXX.md de TODOS os RFs afetados

---

## 🚫 BLOQUEIOS CONHECIDOS

Este prompt **NÃO PODE** ser usado se:

- ❌ Correção for de natureza FUNCIONAL (regra de negócio, validação de domínio)
- ❌ Correção NÃO estiver na LISTA FECHADA do contrato
- ❌ Você quiser "aproveitar" para outras melhorias
- ❌ Documentação (WF/UC) dos RFs afetados não existir

---

## ✅ QUANDO USAR ESTE PROMPT

Use este prompt quando:

1. **Data-test Attributes Ausentes:**
   - Testes E2E não executam por falta de data-test attributes
   - Attributes DEVEM estar especificados nos WF-RFXXX.md

2. **Erros de Compilação Idênticos:**
   - Mesmo erro TypeScript/C# em múltiplos RFs
   - Correção é técnica, não altera comportamento funcional

3. **Atualização de Dependência Crítica:**
   - Vulnerabilidade de segurança em biblioteca
   - Somente patch/minor version

4. **Conformidade com Linter:**
   - Aplicar regra de linter em múltiplos arquivos
   - Somente formatação, não altera lógica

---

## 📝 TEMPLATE DO PROMPT

```
Conforme CONTRATO DE CORREÇÃO SISTÊMICA CROSS-RF, execute correção:

NATUREZA DA CORREÇÃO: [data-test attributes | compilação | dependência | linter]

ERRO/GAP IDENTIFICADO:
[Descrição clara do erro ou gap técnico]

RFS AFETADOS:
[Lista de RFs que precisam de correção]

VALIDAÇÃO PRÉVIA OBRIGATÓRIA:
1. Ler WF-RFXXX.md (ou UC-RFXXX.yaml) de CADA RF afetado
2. Identificar elementos/ações especificados no WF/UC
3. Somente aplicar correção em elementos ESPECIFICADOS na documentação
4. PULAR elementos NÃO especificados (não aplicar correção)

ABORDAGEM:
1. Auditoria: Listar TODOS os RFs que precisam de correção
2. Priorização: [RFs críticos primeiro - ex: RF007 (Login), RF001 (Sistema)]
3. Aplicação: Corrigir RF por RF, validando contra WF/UC de cada um
4. Validação: Executar testes de cada RF após correção

LIMITAÇÃO DE ESCOPO OBRIGATÓRIA:
- NÃO corrigir elementos não especificados nos WF/UC
- NÃO "aproveitar" para outras melhorias
- SOMENTE correção técnica/infraestrutural
- Validar CADA RF individualmente contra sua documentação

RESULTADO ESPERADO:
[Descrição clara do resultado esperado após correção]

ATUALIZAÇÃO DE STATUS.yaml:
- Atualizar STATUS.yaml de CADA RF corrigido
- Incluir: correcao_sistemica.total_rfs_afetados
- Incluir: validacao_wf_uc.alinhado = true
```

---

## 📚 EXEMPLO COMPLETO: Data-test Attributes

### Cenário Real (RF006 - Falha Sistêmica E2E)

**Problema:**
- 712/712 testes E2E falharam (0% aprovação)
- Data-test attributes ausentes em TODOS os componentes (exceto RF006)

**Prompt Correto:**

```
Conforme CONTRATO DE CORREÇÃO SISTÊMICA CROSS-RF, execute correção:

NATUREZA DA CORREÇÃO: Data-test Attributes (Infraestrutura de Testes)

ERRO/GAP IDENTIFICADO:
Testes E2E não executam devido a data-test attributes ausentes em múltiplos componentes Angular. Todos os 712 testes E2E falharam (0% aprovação) pois seletores Playwright não encontram elementos sem data-test attributes.

RFS AFETADOS (Priorização):
CRÍTICOS (executar primeiro):
- RF007 (Login e Autenticação) - BLOQUEANTE para todos os testes
- RF001 (Parâmetros e Configurações) - Navegação e sistema base

ALTA PRIORIDADE:
- RF006 (Gestão de Clientes) - Validar (já corrigido parcialmente)
- RF008 (Gestão de Empresas) - CRUD principal
- RF012 (Gestão de Usuários) - Administração

MÉDIA PRIORIDADE:
- RF019 (Gestão de Tipos de Ativos)
- RF021 (Catálogo de Serviços)
- RF023 (Gestão de Contratos)
- RF024 (Gestão de Departamentos)
- RF026 (Gestão de Faturas)
- RF027 (Gestão de Aditivos)
- RF028 (Gestão de SLA Operações)
- RF029 (Gestão de SLA Serviços)
- RF031 (Gestão de Plano de Contas)
- [... demais 29 RFs conforme necessário]

VALIDAÇÃO PRÉVIA OBRIGATÓRIA:
1. Para CADA RF na lista:
   - Ler WF-RFXXX.md completo
   - Identificar elementos visuais mencionados (botões, grids, campos)
   - Identificar ações especificadas (clicar, preencher, navegar)
2. Somente adicionar data-test em elementos ESPECIFICADOS no WF
3. PULAR elementos NÃO mencionados no WF (não adicionar data-test)

ABORDAGEM:
1. Auditoria:
   cd frontend/icontrolit-app
   grep -r "data-test=" src/app/modules/ | wc -l
   # Se < 100 → confirma que faltam attributes

2. Priorização:
   - RF007 (Login) - EXECUTAR PRIMEIRO
   - RF001 (Sistema) - EXECUTAR SEGUNDO
   - RF006 (Clientes) - VALIDAR (já corrigido)
   - Demais RFs em ordem de prioridade

3. Aplicação (REPETIR PARA CADA RF):
   - Ler WF-RFXXX.md
   - Listar componentes do RFXXX
   - Adicionar data-test SOMENTE em elementos especificados no WF
   - PULAR elementos não especificados
   - Documentar elementos corrigidos vs. pulados

4. Validação (APÓS CADA RF):
   npm run e2e -- frontend/e2e/specs/RFXXX/
   # Validar que testes do RFXXX executam

LIMITAÇÃO DE ESCOPO OBRIGATÓRIA:
- NÃO adicionar data-test em elementos não especificados nos WFs
- NÃO "aproveitar" para adicionar IDs, classes ou outros attributes
- SOMENTE data-test conforme WF-RFXXX.md de cada RF
- Validar CADA RF individualmente contra seu WF

RESULTADO ESPERADO:
- Testes E2E executando em TODOS os RFs (não necessariamente 100% passando, mas executando)
- Data-test attributes presentes SOMENTE em elementos especificados nos WFs
- STATUS.yaml de CADA RF atualizado com entrada de correcao_sistemica
- Documentação de elementos corrigidos vs. pulados para cada RF
- Taxa de execução de testes E2E: 0% → 100%

ATUALIZAÇÃO DE STATUS.yaml:
- Atualizar STATUS.yaml de CADA RF corrigido
- Incluir: correcao_sistemica.total_rfs_afetados = 42 (ou número real)
- Incluir: correcao_sistemica.rf_atual = "RFXXX"
- Incluir: correcao_sistemica.elementos_corrigidos = N
- Incluir: correcao_sistemica.elementos_pulados = M (não especificados)
- Incluir: validacao_wf_uc.alinhado = true
- Incluir: validacao_wf_uc.wf_lido = "WF-RFXXX.md"
```

---

## 🎬 COMO EXECUTAR

### Passo 1: Copiar o Prompt

Copie o template acima e preencha:
- NATUREZA DA CORREÇÃO
- ERRO/GAP IDENTIFICADO
- RFS AFETADOS (com priorização)
- RESULTADO ESPERADO

### Passo 2: Ativar o Contrato

Cole o prompt completo em uma nova conversa com o Claude Code.

### Passo 3: Aguardar Validação

O agente irá:
1. Validar que correção está na LISTA FECHADA
2. Criar TODO LIST obrigatória
3. Validar estado Git e branch
4. Executar auditoria de RFs afetados

### Passo 4: Acompanhar Execução

O agente irá corrigir RF por RF:
- Ler WF-RFXXX.md
- Aplicar correção
- Validar contra WF
- Executar testes
- Atualizar STATUS.yaml

### Passo 5: Validação Final

Após conclusão:
- Verificar STATUS.yaml de cada RF
- Executar testes E2E: `npm run e2e`
- Confirmar merge para dev

---

## ⚠️ AVISOS IMPORTANTES

### 1. Validação Individual é Obrigatória

Mesmo sendo correção cross-RF, **CADA RF deve ser validado individualmente**:
- ✅ Ler WF-RFXXX.md de CADA RF
- ✅ Aplicar correção SOMENTE em elementos especificados
- ✅ PULAR elementos não especificados

### 2. STATUS.yaml de CADA RF

**Todos os RFs corrigidos DEVEM ter STATUS.yaml atualizado:**
- ❌ NÃO basta 1 STATUS.yaml geral
- ✅ CADA RF tem seu próprio STATUS.yaml
- ✅ Cada STATUS.yaml registra a correção sistêmica

### 3. Elementos Pulados (Não Especificados)

**É NORMAL e CORRETO pular elementos:**
```
RF006 corrigido:
- ✅ 5 elementos corrigidos (especificados no WF)
- ❌ 2 elementos pulados (NÃO especificados no WF)
- ✅ Validação: alinhado = true
```

### 4. Tempo Estimado

**Correção sistêmica de data-test em 42 RFs:**
- Auditoria: 30 min
- Correção (42 RFs × 5 min/RF): 3.5 horas
- Validação: 1 hora
- **TOTAL: ~5 horas**

**Correção RF por RF (abordagem tradicional):**
- 42 RFs × 15 min/RF = 10.5 horas
- **Economia: 5.5 horas (52%)**

---

## 📊 CHECKLIST DE VALIDAÇÃO

Antes de considerar correção concluída, validar:

- [ ] Todos os RFs da lista foram corrigidos
- [ ] WF-RFXXX.md de CADA RF foi lido
- [ ] Correção aplicada SOMENTE em elementos especificados
- [ ] Elementos não especificados foram PULADOS
- [ ] STATUS.yaml de CADA RF foi atualizado
- [ ] Testes E2E executam (não necessariamente 100% passando)
- [ ] Nenhum novo erro foi introduzido
- [ ] Build backend/frontend SUCEDE
- [ ] Commit inclui STATUS.yaml de TODOS os RFs
- [ ] Merge para dev foi executado

---

## 🔄 PRÓXIMOS PASSOS APÓS EXECUÇÃO

1. **Validar Testes E2E:**
   ```bash
   npm run e2e
   # Esperado: 712/712 testes EXECUTANDO (não necessariamente passando)
   ```

2. **Corrigir Erros Funcionais (se houver):**
   - ERRO #2 (AutoMapper) - usar CONTRATO DE MANUTENÇÃO tradicional
   - ERRO #3 (TypeScript Signals) - usar CONTRATO DE MANUTENÇÃO tradicional

3. **Executar Testes Completos:**
   ```bash
   # Backend
   cd backend/IControlIT.API
   dotnet test

   # Frontend
   cd frontend/icontrolit-app
   npm run test

   # E2E
   npm run e2e
   ```

---

## 📝 EXEMPLO DE RESULTADO ESPERADO

```
Correção Sistêmica Cross-RF - Data-test Attributes
===================================================

NATUREZA: Infraestrutura de Testes
RFS AFETADOS: 42 RFs
ARQUIVOS ALTERADOS: 184 arquivos

RESUMO POR RF:
- RF007: 8 elementos corrigidos, 1 pulado
- RF001: 12 elementos corrigidos, 3 pulados
- RF006: 5 elementos corrigidos, 2 pulados (já corrigido parcialmente)
- RF008: 10 elementos corrigidos, 2 pulados
... (demais RFs)

TOTAL:
- Elementos corrigidos: 420
- Elementos pulados: 98 (não especificados nos WFs)
- Validação WF/UC: 42/42 RFs alinhados (100%)

RESULTADO:
- Taxa de execução testes E2E: 0% → 100% (712/712 executando)
- Build: SUCESSO
- Testes backend: 26/26 passando
- Testes frontend: COMPILAÇÃO OK (testes executando)
- STATUS.yaml: 42 RFs atualizados

BRANCH: hotfix/correcao-sistemica-data-test-attributes
COMMIT: <hash>
MERGE: dev ✅
```

---

**Mantido por:** Time de Arquitetura IControlIT
**Versão:** 1.0
**Data de Vigência:** 2026-01-05
