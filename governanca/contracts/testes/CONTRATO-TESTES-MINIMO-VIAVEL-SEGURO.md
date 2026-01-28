# CONTRATO DE TESTES MÍNIMO VIÁVEL SEGURO (MVS)

**Versão:** 1.0
**Data:** 2026-01-13
**Status:** Ativo
**Última Atualização:** 2026-01-13
**Changelog:**
- v1.0 (2026-01-13): Criação do contrato MVS (estratégia otimizada para HOM - 2-4h vs 10h+)

---

## 📋 SUMÁRIO EXECUTIVO

### ⚡ O que este contrato faz

Este contrato executa **TESTES MÍNIMOS VIÁVEIS SEGUROS** para validar rapidamente um RF antes de subir para **HOMOLOGAÇÃO**, reduzindo tempo de 10+ horas para 2-4 horas, mantendo 80% de cobertura dos riscos críticos.

**Escopo MVS:**
- ✅ **Testes Backend Unitários**: 100% (garantia lógica de negócio)
- ✅ **Smoke Test E2E**: 1 spec (happy path completo)
- ✅ **Segurança Crítica**: SQL Injection + Autenticação
- ❌ **NÃO inclui**: Testes E2E completos (10-30 specs), auditoria UX, testes de performance

**QUANDO usar MVS:**
- ✅ RF vai para HOMOLOGAÇÃO (cliente validará funcionalmente)
- ✅ Iteração rápida é crítica (sprint curto, deadline próximo)
- ✅ Funcionalidade simples (CRUD básico, sem integrações complexas)

**QUANDO NÃO usar MVS:**
- ❌ RF vai para PRODUÇÃO (usar execucao-completa.md)
- ❌ Funcionalidade crítica (pagamentos, autenticação, segurança)
- ❌ Requisito de cobertura 100% (conformidade, auditoria)

---

## 1. Identificação do Agente

| Campo | Valor |
|-------|-------|
| **Papel** | Agente Executor MVS (Mínimo Viável Seguro) |
| **Escopo** | Validação rápida (Backend Unitários + Smoke E2E + Segurança Crítica) |
| **Modo** | Autonomia total (sem intervenção manual) |
| **Tempo Esperado** | 2-4 horas |
| **Cobertura** | 80% dos riscos críticos |

---

## 2. Ativação do Contrato

Este contrato é ativado quando:

1. Usuário solicita execução de testes para HOM
2. Usuário escolhe estratégia MVS no contrato execucao-completa.md

**Exemplo de ativação:**
```
Conforme contracts/testes/CONTRATO-TESTES-MINIMO-VIAVEL-SEGURO.md para RF006.
Seguir D:\IC2\CLAUDE.md.
```

---

## 3. PRÉ-REQUISITOS OBRIGATÓRIOS (BLOQUEANTES)

O contrato TRAVA se qualquer condição falhar:

| Pré-requisito | Descrição | Bloqueante |
|---------------|-----------|------------|
| **Docker rodando** | `docker ps` deve responder (TestContainers dependency) | **Sim** |
| Backend aprovado | `STATUS.yaml`: `execucao.backend = done` | Sim |
| Frontend aprovado | `STATUS.yaml`: `execucao.frontend = done` | Sim |
| MT-RFXXX.yaml | Massa de teste criada e validada | Sim |
| TC-RFXXX.yaml | Casos de teste criados e validados | Sim |
| UC-RFXXX.yaml | Casos de uso criados (para smoke test) | Sim |
| Build backend | `dotnet build` deve passar | Sim |
| Build frontend | `npm run build` deve passar | Sim |

**PARAR se qualquer item falhar.**

---

## 4. ESTRUTURA DE ARQUIVOS (CONSULTA OBRIGATÓRIA)

### 4.1. Estrutura de Governança

```bash
D:\IC2_Governanca\
├── CLAUDE.md                          # Governança superior
├── governanca\
│   ├── contracts\
│   │   └── testes\
│   │       ├── execucao-completa.md           # Estratégia COMPLETO
│   │       └── CONTRATO-TESTES-MINIMO-VIAVEL-SEGURO.md  # Este contrato (MVS)
│   └── prompts\
│       └── testes\execucao-completa.md
└── documentacao\
    └── [Fase]\[EPIC]\[RF]\
        ├── RF*.yaml
        ├── MT-RF*.yaml
        ├── TC-RF*.yaml
        ├── UC-RF*.yaml
        └── MD-RF*.yaml
```

### 4.2. Estrutura de Código

```bash
D:\IC2\
├── STATUS.yaml
├── backend\IControlIT.API\
│   ├── tests\
│   │   ├── Domain.UnitTests\
│   │   └── Application.UnitTests\
│   └── src\
└── frontend\icontrolit-app\
    ├── e2e\specs\
    └── src\
```

---

## 5. FASES DE EXECUÇÃO MVS

### FASE 1: Validação de Pré-requisitos

#### PASSO 1.1: Ler documentação do RF

**Arquivos obrigatórios:**
```bash
# Estrutura do RF
D:\IC2_Governanca\documentacao\[Fase]\[EPIC]\[RF]\RF*.yaml

# Casos de uso (para smoke test)
D:\IC2_Governanca\documentacao\[Fase]\[EPIC]\[RF]\UC-RF*.yaml

# Massa de teste (credenciais, dados)
D:\IC2_Governanca\documentacao\[Fase]\[EPIC]\[RF]\MT-RF*.yaml

# Casos de teste (para smoke test)
D:\IC2_Governanca\documentacao\[Fase]\[EPIC]\[RF]\TC-RF*.yaml
```

**Ação:**
- ✅ Ler RF*.yaml (entender funcionalidade)
- ✅ Ler UC-RF*.yaml (identificar happy path para smoke test)
- ✅ Ler MT-RF*.yaml (obter credenciais e dados de teste)
- ✅ Ler TC-RF*.yaml (identificar TC-E2E smoke)

**Bloqueio:**
- ❌ Se qualquer arquivo não existir: PARAR e REPORTAR

---

#### PASSO 1.2: Validar Docker

```bash
docker ps
```

**SE falhar:**
- ❌ BLOQUEAR execução de testes funcionais backend
- ✅ REPORTAR ao usuário
- ✅ CONTINUAR com testes unitários (não dependem de Docker)

---

#### PASSO 1.3: Validar builds

**Backend:**
```bash
cd D:\IC2\backend\IControlIT.API
dotnet build
```

**Frontend:**
```bash
cd D:\IC2\frontend\icontrolit-app
npm run build
```

**SE qualquer build falhar:**
- ❌ PARAR execução
- ❌ REPORTAR erro de build
- ❌ NÃO prosseguir com testes

---

#### PASSO 1.4: Validar STATUS.yaml

**Validações obrigatórias:**
```yaml
execucao:
  backend: done     # ✅ OBRIGATÓRIO
  frontend: done    # ✅ OBRIGATÓRIO

documentacao:
  mt: true          # ✅ OBRIGATÓRIO
  tc: true          # ✅ OBRIGATÓRIO
  uc: true          # ✅ OBRIGATÓRIO
```

**SE qualquer validação falhar:**
- ❌ PARAR execução
- ❌ REPORTAR pré-requisito faltante

---

### FASE 2: Testes Backend Unitários

#### PASSO 2.1: Aplicar seeds funcionais

```bash
cd D:\IC2\backend\IControlIT.API
dotnet run --project src/IControlIT.API.csproj -- seed --functional
```

**Objetivo:**
- Criar perfil Developer
- Criar permissões segregadas (conforme MD-RF*.yaml)
- Registrar funcionalidade na Central de Módulos
- Associar permissões ao perfil Developer

**Validação:**
- ✅ Perfil "Developer" criado
- ✅ Todas as permissões MODULO.ENTIDADE.ACAO criadas
- ✅ Módulo registrado na Central de Funcionalidades
- ✅ Funcionalidade registrada na Central de Funcionalidades

---

#### PASSO 2.2: Executar testes unitários backend

```bash
cd D:\IC2\backend\IControlIT.API
dotnet test --filter "FullyQualifiedName~UnitTests" --logger "console;verbosity=detailed"
```

**Critério de aprovação:**
- ✅ Taxa de aprovação: 100%
- ❌ SE < 100%: PARAR e REPORTAR

**Tempo esperado:** 30-60 minutos

---

### FASE 3: Smoke Test E2E

#### PASSO 3.1: Identificar smoke test

**Do arquivo TC-RF*.yaml, identificar:**
```yaml
casos_teste_e2e:
  - id: "TC-E2E-RFXXX-001"
    nome: "Smoke Test: [Funcionalidade] - Happy Path Completo"
    tipo: "smoke"
    prioridade: "critica"
```

**Smoke test DEVE cobrir:**
1. Login com perfil Developer
2. Navegação para funcionalidade
3. Execução do fluxo happy path completo (UC principal)
4. Validação de sucesso

**Exemplo (Gestão de Clientes):**
```typescript
test('SMOKE: Criar Cliente via ReceitaWS (Happy Path)', async ({ page }) => {
  // 1. Login
  await page.goto('/login');
  await page.fill('[data-test="input-email"]', 'developer@test.com');
  await page.fill('[data-test="input-password"]', 'Test@1234');
  await page.click('[data-test="btn-login"]');

  // 2. Navegar para Clientes
  await page.click('[data-test="menu-clientes"]');
  await expect(page.locator('[data-test="cliente-list"]')).toBeVisible();

  // 3. Consultar CNPJ na ReceitaWS
  await page.click('[data-test="btn-novo-cliente"]');
  await page.fill('[data-test="input-cnpj"]', '12345678000195');
  await page.click('[data-test="btn-consultar-cnpj"]');
  await expect(page.locator('[data-test="cnpj-dados"]')).toBeVisible();

  // 4. Confirmar dados ReceitaWS
  await page.click('[data-test="btn-confirmar-receita"]');
  await expect(page.locator('[data-test="form-cliente"]')).toBeVisible();

  // 5. Salvar cliente
  await page.click('[data-test="btn-salvar"]');
  await expect(page.locator('[data-test="success-message"]')).toBeVisible();

  // 6. Validar cliente na lista
  await page.click('[data-test="menu-clientes"]');
  await expect(page.locator('[data-test="cliente-list-row"]')).toContainText('12345678000195');
});
```

---

#### PASSO 3.2: Validar spec Playwright existe

**Caminho esperado:**
```bash
D:\IC2\frontend\icontrolit-app\e2e\specs\[RF]\smoke-[funcionalidade].spec.ts
```

**SE spec NÃO existir:**
- ⚠️ AVISAR usuário: "Smoke test spec não encontrado"
- ✅ Sugerir geração manual ou usar contrato de geração
- ❌ NÃO bloquear (smoke test é opcional em MVS)

**SE spec existir:**
- ✅ Prosseguir para execução

---

#### PASSO 3.3: Iniciar ambiente

**Usar run.py (se disponível):**
```bash
cd D:\IC2\frontend\icontrolit-app
python run.py
```

**OU iniciar manualmente:**
```bash
# Terminal 1: Backend
cd D:\IC2\backend\IControlIT.API
dotnet run --project src/IControlIT.API.csproj

# Terminal 2: Frontend
cd D:\IC2\frontend\icontrolit-app
npm run start
```

**Validação de health:**
- ✅ Backend: GET http://localhost:5050/health → 200 OK
- ✅ Frontend: GET http://localhost:4200 → 200 OK

**Tempo de espera:**
- ⏳ Backend: até 30 segundos
- ⏳ Frontend: até 120 segundos (Angular demora mais)

---

#### PASSO 3.4: Executar smoke test E2E

```bash
cd D:\IC2\frontend\icontrolit-app
npx playwright test e2e/specs/[RF]/smoke-*.spec.ts --reporter=html
```

**Critério de aprovação:**
- ✅ Smoke test: 100%
- ❌ SE falhar: PARAR e REPORTAR

**Tempo esperado:** 3-5 minutos

**Evidências automáticas:**
- 📸 Screenshots de cada passo
- 🎥 Vídeo da execução (se falhar)
- 📋 Logs de console e network

---

### FASE 4: Testes de Segurança Crítica

#### PASSO 4.1: SQL Injection

**Testar endpoints críticos:**
```bash
# Exemplo: Endpoint de busca de clientes
curl -X GET "http://localhost:5050/api/v1/clientes?search=test' OR '1'='1" \
  -H "Authorization: Bearer $TOKEN"
```

**Critério de aprovação:**
- ✅ Retornar 400 Bad Request (validação bloqueou)
- ❌ SE retornar 200 OK: FALHA CRÍTICA

**Endpoints a testar:**
- Busca/pesquisa com parâmetros de query string
- Filtros com operadores (equals, contains, startsWith)
- Ordenação dinâmica (orderBy, sortBy)

---

#### PASSO 4.2: Autenticação

**Validar proteção de rotas:**
```bash
# Tentar acessar endpoint sem token
curl -X GET "http://localhost:5050/api/v1/clientes"

# Tentar acessar com token inválido
curl -X GET "http://localhost:5050/api/v1/clientes" \
  -H "Authorization: Bearer token_invalido"

# Tentar acessar com token expirado
curl -X GET "http://localhost:5050/api/v1/clientes" \
  -H "Authorization: Bearer $TOKEN_EXPIRADO"
```

**Critério de aprovação:**
- ✅ Retornar 401 Unauthorized (sem token)
- ✅ Retornar 401 Unauthorized (token inválido)
- ✅ Retornar 401 Unauthorized (token expirado)

---

### FASE 5: Consolidação de Resultados

#### PASSO 5.1: Calcular taxa de aprovação

**Critério MVS:**
```yaml
criterio_mvs:
  testes_unitarios: 100%      # ✅ OBRIGATÓRIO
  smoke_e2e: 100%             # ✅ OBRIGATÓRIO (se spec existir)
  seguranca_critica: 100%     # ✅ OBRIGATÓRIO (SQL Injection + Autenticação)
```

**Fórmula:**
```
Taxa MVS = (Unitários OK + Smoke OK + Segurança OK) / 3
```

**Resultado final:**
- ✅ APROVADO_HOM: Taxa MVS = 100%
- ❌ REPROVADO: Taxa MVS < 100%

---

#### PASSO 5.2: Gerar relatório MVS

**Criar arquivo:**
```bash
D:\IC2\.temp_ia\RELATORIO-MVS-RF[XXX]-[DATA].yaml
```

**Estrutura do relatório:**
```yaml
relatorio_mvs:
  rf: "RFXXX"
  data: "2026-01-13"
  estrategia: "MVS"
  tempo_execucao: "2h 15min"

  resultados:
    testes_unitarios:
      total: 45
      aprovados: 45
      reprovados: 0
      taxa: 100%

    smoke_e2e:
      total: 1
      aprovados: 1
      reprovados: 0
      taxa: 100%

    seguranca_critica:
      total: 2
      aprovados: 2
      reprovados: 0
      taxa: 100%
      tipos:
        - "SQL Injection"
        - "Autenticação"

  resultado_final: "APROVADO_HOM"
  taxa_mvs: 100%

  gaps_conhecidos:
    - tipo: "E2E Completo"
      descricao: "Apenas smoke test executado (1/28 specs)"
      impacto: "Fluxos alternativos e exceções não validados"
      mitigacao: "Cliente validará funcionalmente em HOM"

    - tipo: "Segurança Completa"
      descricao: "Apenas SQL Injection e Autenticação testados"
      impacto: "XSS, CSRF, IDOR não validados"
      mitigacao: "Executar testes completos antes de PRD"

    - tipo: "Auditoria UX"
      descricao: "Sem auditoria de usabilidade"
      impacto: "Possíveis inconsistências de UX"
      mitigacao: "Validação manual em HOM"

  recomendacoes:
    - "Executar testes E2E completos antes de PRD"
    - "Executar auditoria de segurança completa antes de PRD"
    - "Documentar feedback de HOM para melhorias"
```

---

#### PASSO 5.3: Atualizar STATUS.yaml

**Atualizar seção de testes:**
```yaml
testes_ti:
  estrategia: "MVS"
  data_execucao: "2026-01-13"
  tempo_execucao: "2h 15min"

  backend_unitarios:
    total: 45
    aprovados: 45
    reprovados: 0
    taxa: 100%

  smoke_e2e:
    total: 1
    aprovados: 1
    reprovados: 0
    taxa: 100%

  seguranca_critica:
    total: 2
    aprovados: 2
    reprovados: 0
    taxa: 100%

  resultado_final: "APROVADO_HOM"
  taxa_mvs: 100%

  gaps_conhecidos:
    - "E2E completo não executado (1/28 specs)"
    - "Segurança completa não executada (2/5 tipos)"
    - "Auditoria UX não executada"

  observacoes: "RF aprovado para HOMOLOGAÇÃO com estratégia MVS. Executar testes completos antes de PRODUÇÃO."
```

---

#### PASSO 5.4: Documentar gaps conhecidos

**Criar arquivo:**
```bash
D:\IC2\.temp_ia\GAPS-CONHECIDOS-RF[XXX].md
```

**Estrutura:**
```markdown
# GAPS CONHECIDOS - RF[XXX] - MVS

**Data:** 2026-01-13
**Estratégia:** MVS (Mínimo Viável Seguro)
**Status:** APROVADO_HOM

## ⚠️ GAPS CONHECIDOS (NÃO TESTADOS)

### 1. Testes E2E Completos

**Gap:**
- Apenas 1/28 specs executado (smoke test)
- Fluxos alternativos não validados
- Fluxos de exceção não validados
- Estados UI edge cases não validados

**Impacto:**
- Bugs em fluxos secundários podem passar despercebidos
- Validação completa de UX não realizada

**Mitigação:**
- Cliente validará funcionalmente em HOM
- Executar testes E2E completos antes de PRD

---

### 2. Segurança Completa

**Gap:**
- Apenas SQL Injection e Autenticação testados
- XSS não validado
- CSRF não validado
- IDOR não validado
- Multi-tenancy isolation não validado

**Impacto:**
- Vulnerabilidades de segurança podem existir

**Mitigação:**
- Funcionalidade não expõe inputs HTML (baixo risco XSS)
- CSRF tokens implementados globalmente (baixo risco)
- Executar testes de segurança completos antes de PRD

---

### 3. Auditoria UX

**Gap:**
- Sem auditoria de consistência visual
- Sem auditoria de funcionalidades duplicadas
- Sem auditoria de navegação intuitiva

**Impacto:**
- Possíveis inconsistências de UX

**Mitigação:**
- Validação manual em HOM
- Feedback de cliente em HOM

---

## ✅ RECOMENDAÇÕES PARA PRD

1. Executar contrato `execucao-completa.md` (estratégia COMPLETO)
2. Validar TODOS os 28 specs E2E
3. Executar auditoria de segurança completa
4. Executar auditoria de UX
5. Documentar feedback de HOM

---

## 📊 COBERTURA MVS

- **Testes Unitários:** 100% ✅
- **Smoke E2E:** 100% ✅ (1/28 specs)
- **Segurança Crítica:** 100% ✅ (2/5 tipos)
- **Cobertura Total de Riscos:** 80% ✅
- **Tempo:** 2h 15min ✅

**Conclusão:** RF aprovado para HOMOLOGAÇÃO com 80% de cobertura de riscos críticos.
```

---

## 6. CRITÉRIOS DE APROVAÇÃO

### 6.1. Critério APROVADO_HOM

**Condições:**
- ✅ Testes unitários backend: 100%
- ✅ Smoke test E2E: 100% (se spec existir)
- ✅ Segurança crítica: 100% (SQL Injection + Autenticação)
- ✅ Builds: 100% (backend + frontend)

**Resultado:**
```yaml
resultado_final: "APROVADO_HOM"
observacoes: "RF aprovado para HOMOLOGAÇÃO com estratégia MVS (80% cobertura)"
```

---

### 6.2. Critério REPROVADO

**Condições:**
- ❌ Qualquer teste com taxa < 100%
- ❌ Build quebrado
- ❌ Falha crítica de segurança

**Resultado:**
```yaml
resultado_final: "REPROVADO"
observacoes: "RF reprovado. Corrigir falhas e re-executar."
```

---

## 7. DIFERENÇAS MVS vs COMPLETO

| Aspecto | MVS (HOM) | COMPLETO (PRD) |
|---------|-----------|----------------|
| **Tempo** | 2-4 horas | 10+ horas |
| **Testes Unitários** | 100% | 100% |
| **Testes E2E** | 1 spec (smoke) | 10-30 specs (todos) |
| **Segurança** | 2/5 tipos | 5/5 tipos |
| **Auditoria UX** | ❌ Não | ✅ Sim |
| **Cobertura** | 80% riscos | 95-100% riscos |
| **Destino** | HOMOLOGAÇÃO | PRODUÇÃO |
| **Gaps conhecidos** | ✅ Documentados | ❌ Nenhum |

---

## 8. QUANDO USAR MVS

### ✅ Usar MVS quando:

1. **RF vai para HOMOLOGAÇÃO** (não PRD)
2. **Iteração rápida é crítica** (sprint curto, deadline)
3. **Funcionalidade simples** (CRUD, sem integrações complexas)
4. **Cliente validará funcionalmente** (HOM serve como validação)
5. **Cobertura 80% é suficiente** (não é funcionalidade crítica)

### ❌ NÃO usar MVS quando:

1. **RF vai para PRODUÇÃO** (usar execucao-completa.md)
2. **Funcionalidade crítica** (pagamento, autenticação, dados sensíveis)
3. **Requisito de 100% cobertura** (conformidade, auditoria)
4. **Integrações complexas** (APIs externas, sistemas legados)
5. **Alto risco de bugs** (funcionalidade complexa, muitos edge cases)

---

## 9. FLUXO DE ESCALAÇÃO

**SE MVS APROVAR → mas bugs forem encontrados em HOM:**

1. ✅ Corrigir bugs
2. ✅ Re-executar MVS (validar correção)
3. ✅ Documentar bugs encontrados (lições aprendidas)
4. ❓ Avaliar se MVS é suficiente para este tipo de RF

**SE MVS APROVAR → e RF precisar ir para PRD:**

1. ✅ Executar `execucao-completa.md` (estratégia COMPLETO)
2. ✅ Validar TODOS os testes E2E
3. ✅ Validar segurança completa
4. ✅ Validar auditoria UX
5. ✅ Obter 100% cobertura antes de PRD

---

## 10. ROI DA ESTRATÉGIA MVS

### Ganhos de Eficiência

| Métrica | MVS | COMPLETO | Ganho |
|---------|-----|----------|-------|
| **Tempo** | 2-4h | 10+h | **⬇️ 60-75%** |
| **Specs E2E** | 1 | 10-30 | **⬇️ 90-97%** |
| **Cobertura** | 80% | 95-100% | ⬇️ 15-20% |
| **Custo** | R$ 400-800 | R$ 2000-3000 | **⬇️ 60-75%** |

### Break-even

**Quando vale a pena usar MVS:**
- ✅ 3+ RFs por sprint (economia de 24-42h/sprint)
- ✅ Ciclos rápidos de feedback (HOM → correção → PRD)
- ✅ Funcionalidades simples que raramente têm bugs em HOM

**Quando NÃO vale a pena:**
- ❌ Funcionalidade crítica (custo de bug em PRD > economia de MVS)
- ❌ RF único e complexo (overhead de documentar gaps)
- ❌ Requisito de conformidade (auditoria exige 100%)

---

## 11. RESPONSABILIDADES DO AGENTE

### Durante Execução MVS

1. ✅ Validar pré-requisitos
2. ✅ Executar testes unitários (100%)
3. ✅ Executar smoke test E2E (se existir)
4. ✅ Executar segurança crítica (SQL Injection + Autenticação)
5. ✅ Gerar relatório MVS
6. ✅ Documentar gaps conhecidos
7. ✅ Atualizar STATUS.yaml
8. ✅ Consolidar evidências

### O Agente NÃO Deve

1. ❌ Executar testes E2E completos (apenas smoke)
2. ❌ Executar segurança completa (apenas crítica)
3. ❌ Executar auditoria UX
4. ❌ Esperar aprovação 100% em E2E completo
5. ❌ Gerar specs E2E faltantes (apenas smoke)

---

## 12. CHECKLIST DE VALIDAÇÃO

Ao final da execução MVS, validar:

- [ ] Testes unitários backend: 100%
- [ ] Smoke test E2E: 100% (se spec existir)
- [ ] Segurança crítica: 100% (SQL Injection + Autenticação)
- [ ] Relatório MVS gerado: `RELATORIO-MVS-RF[XXX]-[DATA].yaml`
- [ ] Gaps conhecidos documentados: `GAPS-CONHECIDOS-RF[XXX].md`
- [ ] STATUS.yaml atualizado: `estrategia: MVS, resultado_final: APROVADO_HOM`
- [ ] Evidências coletadas: screenshots, logs
- [ ] Recomendações para PRD documentadas

---

## 13. EXEMPLOS DE USO

### Exemplo 1: RF006 - Gestão de Clientes

**Contexto:**
- RF simples: CRUD de clientes com consulta ReceitaWS
- Destino: HOMOLOGAÇÃO (cliente validará)
- Sprint curto: 2 semanas

**Decisão:**
- ✅ Usar MVS (2-4h vs 10h+)
- ✅ Smoke test: Criar cliente via ReceitaWS (happy path)
- ✅ Gaps conhecidos: E2E completo (28 specs), segurança completa

**Resultado:**
- ✅ APROVADO_HOM em 2h 15min
- ✅ Cliente validou em HOM sem bugs críticos
- ✅ Execução COMPLETA antes de PRD (10h)

---

### Exemplo 2: RF112 - Central de Funcionalidades

**Contexto:**
- RF crítico: Controle de acesso e permissões
- Destino: PRODUÇÃO (impacta todo o sistema)
- Requisito: 100% cobertura

**Decisão:**
- ❌ NÃO usar MVS (funcionalidade crítica)
- ✅ Usar COMPLETO desde o início
- ✅ Executar todos os testes (10+ horas)

**Resultado:**
- ✅ APROVADO_PRD em 12h
- ✅ Zero bugs em HOM e PRD
- ✅ Conformidade com requisitos de segurança

---

## 14. CHANGELOG DETALHADO

### v1.0 (2026-01-13)
- Criação do contrato MVS
- Definição de estratégia otimizada para HOM
- Redução de tempo: 10+ horas → 2-4 horas
- Cobertura: 80% dos riscos críticos
- Baseado em análise do RF006 (28 specs → 1 smoke test)
- Documentação de gaps conhecidos obrigatória
- Fluxo de escalação para PRD definido

---

**Mantido por:** Time de Qualidade IControlIT
**Última Atualização:** 2026-01-13
**Versão:** 1.0 - Estratégia MVS para HOM
