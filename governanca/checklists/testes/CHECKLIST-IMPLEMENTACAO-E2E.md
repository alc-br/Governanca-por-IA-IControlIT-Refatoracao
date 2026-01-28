# CHECKLIST DE IMPLEMENTAÇÃO E2E

**Versão:** 1.0
**Data:** 2026-01-09
**Objetivo:** Garantir que implementação de RF está 100% pronta para testes E2E
**Contexto:** Criado após análise do RF006 para prevenir falhas sistemáticas em E2E

---

## CRITÉRIO DE SUCESSO

**Taxa de aprovação inicial E2E: ≥ 80%**

Se primeira execução E2E < 80%:
- ❌ Alinhamento com testes FALHOU
- ❌ RETORNAR à documentação (UC/TC/MT) e/ou implementação (Backend/Frontend)
- ❌ Corrigir gaps e re-executar

---

## FASE 1: PRÉ-IMPLEMENTAÇÃO (4 checklists)

### 1.1. Validação de Documentação (RF, UC, TC, MT)

**Checklist:**

- [ ] RF-RFXXX.md existe e está aprovado
- [ ] RF-RFXXX.yaml existe e está sincronizado com MD
- [ ] UC-RFXXX.md existe e está aprovado
- [ ] UC-RFXXX.yaml existe e possui **TODAS** as seções de teste:
  - [ ] `navegacao` (url_completa + referencia_routing)
  - [ ] `credenciais` (referencia_seeds + perfil_necessario)
  - [ ] `passos` com `elemento.data_test` para TODOS os passos interativos
  - [ ] `estados_ui` (loading, vazio, erro)
  - [ ] `tabela` (se aplicável: data_test_container, data_test_row, colunas)
  - [ ] `formulario` (se aplicável: data_test_form, campos, validacoes)
  - [ ] `performance` (tempo_carregamento_maximo, tempo_operacao_crud)
  - [ ] `timeouts_e2e` (navegacao, loading_spinner, dialog, operacao_crud)
- [ ] TC-RFXXX.yaml existe e possui **TODOS** os seletores E2E:
  - [ ] `passos[].seletor` para TODOS os passos
  - [ ] `passos[].acao_e2e` (código Playwright) para TODOS os passos
  - [ ] `validacoes[].seletor` para TODAS as validações
  - [ ] `validacoes[].acao_e2e` para TODAS as validações
- [ ] MT-RFXXX.yaml existe e está aprovado
- [ ] MT-RFXXX.data.ts existe e possui:
  - [ ] `CREDENCIAIS_TESTE` (email, password, perfil)
  - [ ] `FRONTEND_URLS` (todas as URLs necessárias)
  - [ ] `DATA_TEST_SELECTORS` (todos os seletores do UC)
  - [ ] `TIMEOUTS` (sincronizados com UC)

**Critério de Aprovação:**
- ✅ TODAS as checagens acima passaram

**Se FALHAR:**
- ❌ RETORNAR ao contrato de criação/adequação correspondente (RF, UC, TC, MT)
- ❌ Completar documentação antes de prosseguir

---

### 1.2. Sincronização de Credenciais (Backend Seeds)

**Objetivo:** Garantir que credenciais de teste batem com seeds do backend

**Checklist:**

- [ ] Backend seeds existe: `backend/Infrastructure/Persistence/ApplicationDbContextInitialiser.cs`
- [ ] MT-RFXXX.data.ts possui `CREDENCIAIS_TESTE` completo:
  - [ ] Email sincronizado com seed
  - [ ] Password sincronizado com seed
  - [ ] Perfil sincronizado com seed
- [ ] Comentário de sincronização presente:
  ```typescript
  /**
   * FONTE: ApplicationDbContextInitialiser.cs (linhas XX-YY)
   * ÚLTIMA SINCRONIZAÇÃO: [DATA]
   */
  ```
- [ ] Executar validação automática:
  ```bash
  npm run validate-credentials RFXXX
  ```
- [ ] Exit code 0 (PASS) retornado

**Critério de Aprovação:**
- ✅ `npm run validate-credentials RFXXX` retorna exit code 0

**Se FALHAR:**
- ❌ Atualizar `CREDENCIAIS_TESTE` em MT-RFXXX.data.ts
- ❌ Documentar sincronização (comentário com linha do seed)
- ❌ Re-executar validação até PASS

**Impacto RF006:**
- Resolve Problema 1/6: 100% de falhas E2E por credenciais erradas

---

### 1.3. Sincronização de URLs (Frontend Routing)

**Objetivo:** Garantir que URLs de teste batem com rotas do Angular

**Checklist:**

- [ ] Frontend routing existe: `src/app/*-routing.module.ts`
- [ ] MT-RFXXX.data.ts possui `FRONTEND_URLS` completo:
  - [ ] URL de navegação principal especificada
  - [ ] Todas as URLs de subnavegação especificadas (se aplicável)
- [ ] Comentário de sincronização presente:
  ```typescript
  /**
   * FONTE: src/app/[caminho]/[arquivo]-routing.module.ts
   * ÚLTIMA SINCRONIZAÇÃO: [DATA]
   */
  ```
- [ ] Executar validação automática:
  ```bash
  npm run validate-routes
  ```
- [ ] Exit code 0 (PASS) retornado

**Critério de Aprovação:**
- ✅ `npm run validate-routes` retorna exit code 0

**Se FALHAR:**
- ❌ Atualizar `FRONTEND_URLS` em MT-RFXXX.data.ts
- ❌ Documentar sincronização (comentário com arquivo routing)
- ❌ Re-executar validação até PASS

**Impacto RF006:**
- Resolve Problema 2/6: 32 falhas E2E por URLs 404

---

### 1.4. Sincronização de Timeouts (UC)

**Objetivo:** Garantir que timeouts de teste batem com especificações do UC

**Checklist:**

- [ ] UC-RFXXX.yaml possui seção `performance`:
  - [ ] `tempo_carregamento_maximo` especificado
  - [ ] `tempo_operacao_crud` especificado
  - [ ] `timeout_api_externa` especificado (se aplicável)
- [ ] UC-RFXXX.yaml possui seção `timeouts_e2e`:
  - [ ] `navegacao` especificado
  - [ ] `loading_spinner` especificado
  - [ ] `dialog` especificado
  - [ ] `operacao_crud` especificado
- [ ] MT-RFXXX.data.ts possui `TIMEOUTS` sincronizado com UC:
  ```typescript
  export const TIMEOUTS = {
    navegacao: 30000,        // Valor de UC
    loadingSpinner: 30000,   // Valor de UC
    dialog: 10000,           // Valor de UC
    operacaoCRUD: 15000      // Valor de UC
  };
  ```
- [ ] Executar validação automática (se script existir):
  ```bash
  python tools/validate-timeouts.py RFXXX
  ```

**Critério de Aprovação:**
- ✅ TIMEOUTS em MT batem exatamente com UC

**Se FALHAR:**
- ❌ Atualizar `TIMEOUTS` em MT-RFXXX.data.ts
- ❌ Documentar sincronização (comentário com referência UC)

**Impacto RF006:**
- Resolve Problema 5/6: 15 falhas E2E por timeout insuficiente

---

## FASE 2: DURANTE IMPLEMENTAÇÃO (4 checklists)

### 2.1. Data-test Attributes (TODOS os Elementos)

**Objetivo:** Garantir que TODOS os elementos interativos possuem data-test

**Checklist:**

#### Botões de Ação
- [ ] Botão "Criar" possui data-test: `RFXXX-criar-[entidade]`
- [ ] Botão "Editar" possui data-test: `RFXXX-editar-[entidade]`
- [ ] Botão "Excluir" possui data-test: `RFXXX-excluir-[entidade]`
- [ ] Botão "Salvar" possui data-test: `RFXXX-salvar-[entidade]`
- [ ] Botão "Cancelar" possui data-test: `RFXXX-cancelar-[entidade]`
- [ ] Todos os botões seguem nomenclatura: `RFXXX-[acao]-[alvo]`

#### Campos de Formulário
- [ ] TODOS os inputs possuem data-test: `RFXXX-input-[nome]`
- [ ] TODOS os selects possuem data-test: `RFXXX-input-[nome]`
- [ ] TODOS os textareas possuem data-test: `RFXXX-input-[nome]`
- [ ] Nomenclatura segue padrão: `RFXXX-input-[nome]`

#### Mensagens de Erro
- [ ] TODAS as validações possuem data-test-erro: `RFXXX-input-[nome]-error`
- [ ] Mensagens seguem nomenclatura consistente

#### Sincronização com UC
- [ ] Data-test batem com UC-RFXXX.yaml (`passos[].elemento.data_test`)
- [ ] Nenhum data-test divergente de UC
- [ ] Nenhum data-test ausente em relação a UC

**Critério de Aprovação:**
- ✅ TODOS os elementos interativos possuem data-test
- ✅ Nomenclatura 100% consistente

**Se FALHAR:**
- ❌ Adicionar data-test ausentes
- ❌ Corrigir nomenclatura inconsistente
- ❌ Re-validar até PASS

**Impacto RF006:**
- Resolve Problema 3/6: 32 falhas E2E por seletores não encontrados

---

### 2.2. Estados UI (Loading, Vazio, Erro)

**Objetivo:** Garantir que TODOS os estados de UI estão implementados e com data-test

**Checklist:**

#### Estado Loading
- [ ] Spinner implementado
- [ ] Data-test: `loading-spinner`
- [ ] Exibido durante carregamento inicial
- [ ] Exibido durante operações CRUD

#### Estado Vazio
- [ ] Mensagem implementada
- [ ] Data-test: `empty-state`
- [ ] Texto exato: conforme UC-RFXXX.yaml (`estados_ui.vazio.texto_esperado`)
- [ ] Ilustração presente (se especificado no UC)

#### Estado Erro
- [ ] Mensagem implementada
- [ ] Data-test: `error-message`
- [ ] Texto exato: conforme UC-RFXXX.yaml (`estados_ui.erro.texto_esperado`)
- [ ] Botão "Tentar novamente" presente (se especificado no UC)

**Critério de Aprovação:**
- ✅ TODOS os 3 estados implementados
- ✅ Data-test presentes
- ✅ Textos exatos conforme UC

**Se FALHAR:**
- ❌ Implementar estados ausentes
- ❌ Adicionar data-test ausentes
- ❌ Corrigir textos divergentes

**Impacto RF006:**
- Resolve Problema 4/6: Estados UI não documentados

---

### 2.3. Tabelas/Listas (Container, Row, Buttons)

**Objetivo:** Garantir que tabelas/listas possuem data-test completos

**Checklist (se aplicável - UC possui listagem):**

#### Container
- [ ] Container da tabela possui data-test: `[entidade]-list`
- [ ] Exemplo: `clientes-list`, `usuarios-list`

#### Linhas
- [ ] Linhas da tabela possuem data-test: `[entidade]-row`
- [ ] Exemplo: `cliente-row`, `usuario-row`

#### Colunas
- [ ] TODAS as colunas possuem data-test conforme UC-RFXXX.yaml (`tabela.colunas[].data_test`)
- [ ] Nomenclatura consistente

#### Ações de Linha
- [ ] Botão "Editar" possui data-test: `RFXXX-editar-[entidade]`
- [ ] Botão "Excluir" possui data-test: `RFXXX-excluir-[entidade]`
- [ ] Outras ações possuem data-test conforme UC

**Critério de Aprovação:**
- ✅ Container, linhas, colunas, ações possuem data-test
- ✅ Data-test batem com UC-RFXXX.yaml (`tabela`)

**Se FALHAR:**
- ❌ Adicionar data-test ausentes
- ❌ Corrigir nomenclatura inconsistente

---

### 2.4. Formulários (Inputs, Errors, Buttons)

**Objetivo:** Garantir que formulários possuem data-test completos

**Checklist (se aplicável - UC possui formulário):**

#### Formulário
- [ ] Form possui data-test: `RFXXX-form`
- [ ] Exemplo: `RF006-form`

#### Campos
- [ ] TODOS os campos possuem data-test conforme UC-RFXXX.yaml (`formulario.campos[].data_test`)
- [ ] Nomenclatura: `RFXXX-input-[nome]`

#### Validações
- [ ] TODAS as validações possuem data-test-erro conforme UC-RFXXX.yaml (`formulario.campos[].validacoes[].data_test_erro`)
- [ ] Mensagens de erro exatas conforme UC

#### Botões
- [ ] Botão "Salvar" possui data-test: `RFXXX-salvar-[entidade]`
- [ ] Botão "Cancelar" possui data-test: `RFXXX-cancelar-[entidade]`

**Critério de Aprovação:**
- ✅ Form, campos, validações, botões possuem data-test
- ✅ Data-test batem com UC-RFXXX.yaml (`formulario`)

**Se FALHAR:**
- ❌ Adicionar data-test ausentes
- ❌ Corrigir nomenclatura inconsistente

---

### 2.5. Validação Visual (Layout e Alinhamento)

**Objetivo:** Garantir que elementos estão visualmente corretos (alinhamento, posição, layout)

**Checklist:**

#### Screenshots de Baseline
- [ ] Screenshots de baseline criados para TODAS as páginas principais
- [ ] Nomenclatura: `[RFXXX]-[pagina]-[estado].png`
- [ ] Armazenados em: `e2e/screenshots/baseline/RFXXX/`
- [ ] Baseline cobre estados: normal, loading, vazio, erro

#### Validações de Layout
- [ ] Botões principais estão visíveis e alinhados corretamente
- [ ] Campos de formulário estão alinhados verticalmente
- [ ] Tabelas possuem colunas alinhadas
- [ ] Estados UI (loading, vazio, erro) estão centralizados
- [ ] Elementos não estão sobrepostos ou cortados
- [ ] Nenhum elemento está fora da viewport

#### Configuração Playwright
- [ ] `screenshot: 'on'` configurado em playwright.config.ts
- [ ] Testes de snapshot criados para páginas principais
- [ ] Tolerância de diff configurada (`maxDiffPixels: 100`)
- [ ] Viewport configurado consistentemente (1920x1080 para desktop)

#### Validações Programáticas (Opcional)
- [ ] Validação de alinhamento de botões (boundingBox)
- [ ] Validação de posição de elementos críticos
- [ ] Validação de elementos dentro da viewport

**Critério de Aprovação:**
- ✅ TODAS as páginas principais possuem baseline visual
- ✅ Testes de snapshot executam sem falhas (ou diff < maxDiffPixels)
- ✅ Layout responsivo validado (desktop + mobile se aplicável)

**Se FALHAR:**
- ❌ Corrigir CSS/layout desalinhado
- ❌ Atualizar baseline (se mudança intencional)
- ❌ Re-executar testes visuais até PASS

**Impacto RF006:**
- Resolve GAP 4: Regressões visuais não detectadas (alinhamento, layout)

---

## FASE 3: PÓS-IMPLEMENTAÇÃO (4 checklists)

### 3.1. Validação Técnica (Build, Testes Unitários/Backend)

**Objetivo:** Garantir que código compila e testes unitários passam

**Checklist:**

#### Build Backend
- [ ] Executar build:
  ```bash
  cd backend/IControlIT.API && dotnet build --no-incremental
  ```
- [ ] Build retorna: `0 Erro(s)`

#### Testes Unitários Backend
- [ ] Executar testes:
  ```bash
  dotnet test backend/Application.Tests/Application.Tests.csproj
  ```
- [ ] Taxa de aprovação: 100%
- [ ] Cobertura: 100% dos Commands/Queries possuem testes

#### Build Frontend
- [ ] Executar build:
  ```bash
  cd frontend/icontrolit-app && npm run build
  ```
- [ ] Build retorna: `Output location: ...`

**Critério de Aprovação:**
- ✅ Backend builda sem erros
- ✅ Testes unitários backend 100% aprovados
- ✅ Frontend builda sem erros

**Se FALHAR:**
- ❌ Corrigir erros de compilação
- ❌ Corrigir testes falhando
- ❌ Re-executar até PASS

---

### 3.2. Validação Visual Primeira Execução

**Objetivo:** Garantir que baseline visual foi criado e testes visuais executam

**Checklist:**

#### Criação de Baseline
- [ ] Executar criação de baseline:
  ```bash
  cd frontend/icontrolit-app && npm run e2e:visual:baseline RFXXX
  ```
- [ ] Screenshots criados em: `e2e/screenshots/baseline/RFXXX/`
- [ ] Baseline cobre TODAS as páginas do RF

#### Primeira Execução de Testes Visuais
- [ ] Executar testes visuais:
  ```bash
  cd frontend/icontrolit-app && npm run e2e:visual RFXXX
  ```
- [ ] Testes visuais passam (ou diff < maxDiffPixels)
- [ ] Nenhum elemento fora da viewport detectado

#### Análise de Falhas Visuais (se houver)
- [ ] Identificar se falha é regressão (corrigir CSS) ou mudança intencional (atualizar baseline)
- [ ] Documentar decisão em comentário do commit
- [ ] Re-executar até PASS

**Critério de Aprovação:**
- ✅ Baseline criado para TODAS as páginas
- ✅ Testes visuais executam sem falhas críticas

**Se FALHAR:**
- ❌ Corrigir CSS/layout desalinhado
- ❌ Atualizar baseline (se mudança intencional)
- ❌ Re-executar testes visuais

---

### 3.3. Validação E2E Primeira Execução (≥ 80%)

**Objetivo:** Garantir que primeira execução E2E atinge taxa de aprovação ≥ 80%

**Checklist:**

#### Pré-Execução
- [ ] Executar checklist pré-execução de testes:
  - [ ] Credenciais sincronizadas (validate-credentials PASS)
  - [ ] URLs sincronizadas (validate-routes PASS)
  - [ ] Data-test sincronizados (audit-data-test PASS)
  - [ ] UC completo (validate-uc-test-specs PASS)
  - [ ] Frontend com data-test (audit HTML PASS)

#### Execução E2E
- [ ] Executar testes E2E:
  ```bash
  cd frontend/icontrolit-app && npm run e2e
  ```
- [ ] Calcular taxa de aprovação:
  ```
  Taxa = (Testes Passando / Total de Testes) * 100
  ```

#### Análise de Resultados
- [ ] Taxa de aprovação ≥ 80%: **APROVADO**
- [ ] Taxa de aprovação < 80%: **REPROVADO**

**Critério de Aprovação:**
- ✅ Taxa de aprovação primeira execução E2E ≥ 80%

**Se FALHAR (Taxa < 80%):**
- ❌ Analisar falhas detalhadamente
- ❌ Identificar gaps (credenciais, URLs, seletores, estados UI, timeouts)
- ❌ RETORNAR à documentação (UC/TC/MT) ou implementação (Backend/Frontend)
- ❌ Corrigir gaps
- ❌ Re-executar E2E até taxa ≥ 80%

**Impacto RF006:**
- RF006: 0% inicial → Meta: 80-90% inicial
- Economia: 12 execuções → 2-3 execuções
- Economia: ~10 horas → 2-4 horas

---

### 3.4. Documentação (STATUS.yaml, EXECUTION-MANIFEST)

**Objetivo:** Documentar resultado da implementação e primeira execução E2E

**Checklist:**

#### STATUS.yaml
- [ ] Atualizar seção `desenvolvimento`:
  ```yaml
  desenvolvimento:
    backend:
      implementado: true
      testes_unitarios_aprovados: true
      cobertura_testes: "100%"
    frontend:
      implementado: true
      data_test_attributes_completos: true
      auditoria_data_test: "PASS"
  ```
- [ ] Atualizar seção `validacao`:
  ```yaml
  validacao:
    backend: passed
    frontend: passed
    testes_visuais:
      baseline_criado: true
      testes_aprovados: true
      data: "[DATA]"
    testes_e2e_primeira_execucao:
      taxa_aprovacao: "[X]%"
      status: "[APROVADO|REPROVADO]"
      data: "[DATA]"
  ```

#### EXECUTION-MANIFEST.md (se aplicável)
- [ ] Documentar taxa de aprovação E2E
- [ ] Documentar número de execuções necessárias
- [ ] Documentar gaps identificados (se houver)
- [ ] Documentar tempo total de implementação

**Critério de Aprovação:**
- ✅ STATUS.yaml atualizado completamente
- ✅ EXECUTION-MANIFEST.md documentado (se aplicável)

---

## RESUMO DE BLOQUEIOS

**Bloqueios Obrigatórios (IMPEDEM prosseguir):**

1. **Documentação incompleta:**
   - UC sem seções de teste → RETORNAR a UC
   - TC sem seletores E2E → RETORNAR a TC
   - MT sem credenciais/URLs/seletores → RETORNAR a MT

2. **Sincronização FALHOU:**
   - Credenciais MT ≠ Backend seeds → Atualizar MT
   - URLs MT ≠ Frontend routing → Atualizar MT
   - Data-test MT ≠ UC → Atualizar MT

3. **Implementação incompleta:**
   - Backend sem testes unitários → Adicionar testes
   - Frontend sem data-test → Adicionar data-test
   - Estados UI ausentes → Implementar estados

4. **Primeira execução E2E < 80%:**
   - Analisar gaps
   - Corrigir documentação/implementação
   - Re-executar até ≥ 80%

---

## MÉTRICAS DE SUCESSO

| Métrica | RF006 (Baseline) | Meta (Com Checklist) |
|---------|------------------|----------------------|
| Taxa inicial E2E | 0% | ≥ 80% |
| Execuções necessárias | 12 | 2-3 |
| Tempo total | ~10 horas | 2-4 horas |
| Commits de correção | 7 | 0-1 |

---

## CHANGELOG

### v1.0 (2026-01-09)
- Criação do checklist de implementação E2E
- Fase 1: Pré-implementação (4 checklists)
- Fase 2: Durante implementação (4 checklists)
- Fase 3: Pós-implementação (3 checklists)
- Critério de sucesso: ≥ 80% taxa inicial E2E
- Bloqueios obrigatórios documentados
- Métricas de sucesso baseadas em RF006

---

**Mantido por:** Time de Arquitetura IControlIT
**Última Atualização:** 2026-01-09
**Versão:** 1.0
