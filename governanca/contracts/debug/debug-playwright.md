# CONTRATO DE DEBUG COM PLAYWRIGHT

**Versão:** 1.0
**Data:** 2026-01-08
**Status:** Ativo
**Última Atualização:** 2026-01-08 (Criação inicial)

---

## 📋 SUMÁRIO EXECUTIVO

### ⚡ O que este contrato faz

Este contrato permite **INVESTIGAÇÃO E DIAGNÓSTICO** de problemas no frontend usando Playwright para:

- ✅ **Acessar a aplicação**: Navegar pelas telas afetadas
- ✅ **Capturar evidências**: Screenshots, console logs, network requests
- ✅ **Reproduzir problemas**: Executar cenários que causam o erro
- ✅ **Diagnosticar causa raiz**: Identificar origem exata do problema
- ✅ **Gerar prompt de correção**: Criar descrição detalhada para manutenção

**IMPORTANTE:** Este contrato **NÃO corrige problemas**. Apenas investiga e diagnóstica. A correção será feita posteriormente com o contrato de manutenção apropriado.

---

## 1. Identificação do Agente

| Campo | Valor |
|-------|-------|
| **Papel** | Agente de Debug com Playwright |
| **Escopo** | Investigação, diagnóstico, evidências |
| **Modo** | Somente leitura + execução de testes |
| **Saída** | Diagnóstico em texto + prompt de correção |

---

## 2. Ativação do Contrato

Este contrato é ativado quando a solicitação mencionar explicitamente:

> **"Conforme contracts/debug/debug-playwright.md"**

**OU quando o usuário solicitar via prompt:**

> **"Execute D:\IC2_Governanca\governanca\prompts\debug\debug-playwright.md"**

### Quando Usar Este Contrato

✅ **USE quando:**
- Problema visual não identificado (layout quebrado, componente não aparece)
- Erro no console do browser (JavaScript, network, warnings)
- Comportamento inesperado na UI (botão não funciona, formulário não submete)
- Problema de integração frontend-backend (API retorna erro na UI)
- Necessidade de reproduzir cenário de usuário para entender o problema
- Merge conflicts ou erros que não foram pegos por testes automatizados

❌ **NÃO USE quando:**
- Problema já está claramente identificado → Use contrato de manutenção diretamente
- Erro é no backend apenas → Use debug de backend apropriado
- Problema é de build/compilação → Resolva com ferramentas de build

### Exemplos de Uso Correto

**✅ CENÁRIOS IDEAIS:**
1. "Merge conflict aparecendo no HTML da tela de login" → Acessar /sign-in, capturar screenshot, verificar console
2. "Erro de i18n: Error while trying to load 'pt'" → Navegar, capturar network requests, verificar console
3. "Botão de salvar não funciona em produção" → Reproduzir clique, capturar eventos, verificar chamadas API
4. "Tela de relatórios carrega em branco" → Acessar rota, capturar console errors, verificar loading states
5. "Validação de formulário não está funcionando" → Preencher formulário, capturar validations, verificar comportamento

**❌ CENÁRIOS INADEQUADOS:**
1. "API de autenticação retorna 500" → Debug de backend (não requer Playwright)
2. "Código não compila após merge" → Problema de build (resolver antes de debug)
3. "Renomear variável em 10 arquivos" → Não é debug, é manutenção

---

## 3. ESCOPO PERMITIDO

### 3.1. Ações Permitidas

✅ **PERMITIDO:**
- Executar testes Playwright existentes
- Criar scripts Playwright temporários para reproduzir o problema
- Navegar pela aplicação em modo headed (com browser visível)
- Capturar screenshots de telas afetadas
- Extrair logs do console do browser
- Verificar network requests (XHR, Fetch, WebSocket)
- Inspecionar elementos HTML/CSS
- Verificar estado da aplicação (localStorage, sessionStorage, cookies)
- Reproduzir interações de usuário (clique, preenchimento, navegação)
- Documentar fluxo que causa o problema

❌ **PROIBIDO:**
- **CORRIGIR** código (use contrato de manutenção após diagnóstico)
- Modificar arquivos de código fonte
- Alterar testes existentes (apenas criar temporários em `.temp_ia/`)
- Fazer deploy ou restart de serviços
- Executar operações destrutivas (deletar dados, limpar banco)
- Tomar decisões sobre qual correção aplicar

---

## 4. PRÉ-REQUISITOS OBRIGATÓRIOS

### 4.1. Checklist Pré-Debug (Consultar ANTES)

**OBRIGATÓRIO:** Ler e validar checklist antes de iniciar:

```
D:\IC2_Governanca\governanca\checklists\debug\pre-debug-playwright.yaml
```

### 4.2. Validações Pré-Debug

Antes de iniciar debug, **VALIDAR**:

- [ ] Ambiente de desenvolvimento está rodando (backend + frontend)
- [ ] Backend responde em `http://localhost:5000/health` com status 200
- [ ] Frontend responde em `http://localhost:4200` com status 200
- [ ] Playwright está instalado (`npx playwright --version`)
- [ ] Browsers do Playwright estão instalados (`npx playwright install`)
- [ ] Descrição do problema foi fornecida pelo usuário
- [ ] RF afetado foi identificado (se aplicável)

**Se qualquer validação falhar:**
- ❌ **PARAR** execução
- ❌ **INFORMAR** o que está faltando
- ❌ **AGUARDAR** correção do pré-requisito

---

## 5. FLUXO DE EXECUÇÃO (PASSO A PASSO)

### FASE 1: Preparação (OBRIGATÓRIA)

#### PASSO 1.1: Validar Pré-Requisitos

**Executar validações do checklist:**

```bash
# 1. Validar backend
curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/health

# 2. Validar frontend
curl -s -o /dev/null -w "%{http_code}" http://localhost:4200

# 3. Validar Playwright
npx playwright --version
```

**Critério de Sucesso:**
- Backend: Status 200
- Frontend: Status 200
- Playwright: Versão exibida (ex: `Version 1.40.0`)

**Se falhar:** PARAR e informar o que está faltando.

---

#### PASSO 1.2: Criar Script de Debug Temporário

**Local:** `D:\IC2\.temp_ia\debug-playwright-{timestamp}.spec.ts`

**Estrutura mínima:**

```typescript
import { test, expect } from '@playwright/test';

test.describe('Debug: {DESCRIÇÃO_DO_PROBLEMA}', () => {
  test.beforeEach(async ({ page }) => {
    // Navegar para a rota afetada
    await page.goto('http://localhost:4200/{ROTA}');
  });

  test('Reproduzir problema e capturar evidências', async ({ page, context }) => {
    // PASSO 1: Capturar console logs
    const logs: string[] = [];
    page.on('console', msg => logs.push(`[${msg.type()}] ${msg.text()}`));

    // PASSO 2: Capturar network requests
    const requests: string[] = [];
    page.on('request', req => requests.push(`${req.method()} ${req.url()}`));

    // PASSO 3: Capturar erros
    const errors: string[] = [];
    page.on('pageerror', err => errors.push(err.message));

    // PASSO 4: Reproduzir cenário do problema
    // (Adicionar interações específicas aqui)

    // PASSO 5: Capturar screenshot
    await page.screenshot({
      path: 'D:\\IC2\\.temp_ia\\debug-screenshot-{timestamp}.png',
      fullPage: true
    });

    // PASSO 6: Exibir evidências
    console.log('=== CONSOLE LOGS ===');
    logs.forEach(log => console.log(log));

    console.log('\n=== NETWORK REQUESTS ===');
    requests.forEach(req => console.log(req));

    console.log('\n=== ERRORS ===');
    errors.forEach(err => console.log(err));
  });
});
```

**IMPORTANTE:** Este script é temporário e será criado em `.temp_ia/`. Não modificar testes oficiais.

---

### FASE 2: Execução do Debug (OBRIGATÓRIA)

#### PASSO 2.1: Executar Script de Debug

**Comando:**

```bash
cd D:\IC2\frontend\icontrolit-app
npx playwright test D:\IC2\.temp_ia\debug-playwright-{timestamp}.spec.ts --headed --project=chromium
```

**Flags importantes:**
- `--headed`: Abre browser visível para observar o problema
- `--project=chromium`: Usa Chrome (ajustar se necessário)
- `--debug`: Adicionar se quiser pausar execução (opcional)

**Capturar:**
- Saída completa do console
- Screenshot gerado
- Comportamento visual do browser

---

#### PASSO 2.2: Análise Manual Complementar (se necessário)

Se o script automático não capturar tudo, **executar manualmente:**

```bash
# Abrir Playwright UI para navegação interativa
npx playwright test --ui D:\IC2\.temp_ia\debug-playwright-{timestamp}.spec.ts
```

**Ou usar Playwright Codegen para gravar interações:**

```bash
npx playwright codegen http://localhost:4200/{ROTA}
```

**Observar:**
- Erros no console do browser
- Network requests falhando (4xx, 5xx)
- Elementos faltando ou mal posicionados
- Warnings de frameworks (Angular, Transloco, etc)

---

### FASE 3: Diagnóstico (OBRIGATÓRIA)

#### PASSO 3.1: Consolidar Evidências

**Organizar todas as evidências coletadas:**

1. **Console Logs:**
   - Erros (vermelho)
   - Warnings (amarelo)
   - Info (azul)

2. **Network Requests:**
   - Requests que falharam (status 4xx, 5xx)
   - Requests que demoraram muito (>5s)
   - Requests cancelados

3. **Screenshots:**
   - Tela esperada vs tela atual
   - Elementos faltando
   - Layout quebrado

4. **Comportamento Observado:**
   - O que deveria acontecer
   - O que está acontecendo
   - Diferença entre esperado e real

---

#### PASSO 3.2: Identificar Causa Raiz

**Analisar evidências para determinar:**

1. **Tipo do Problema:**
   - [ ] Erro de JavaScript (exception não tratada)
   - [ ] Erro de carregamento (assets, scripts, styles)
   - [ ] Erro de API (backend retornando erro)
   - [ ] Erro de configuração (i18n, routing, etc)
   - [ ] Erro de estado (dados não carregados corretamente)
   - [ ] Erro visual (CSS, layout, responsividade)

2. **Localização do Problema:**
   - [ ] Componente específico: `{NOME_COMPONENTE}`
   - [ ] Serviço específico: `{NOME_SERVICO}`
   - [ ] Arquivo específico: `{CAMINHO_ARQUIVO}`
   - [ ] Linha aproximada: `{LINHA}`

3. **Impacto do Problema:**
   - [ ] Bloqueia funcionalidade crítica
   - [ ] Causa UX ruim mas não bloqueia
   - [ ] Visível apenas em console (usuário não percebe)

---

#### PASSO 3.3: Determinar Escopo da Correção

**Estimar complexidade da correção:**

| Tipo de Correção | Escopo | Contrato Recomendado |
|------------------|--------|----------------------|
| **Cirúrgica** | 1-3 arquivos, 1 camada | `manutencao-controlada.md` |
| **Moderada** | 4-10 arquivos, 1-2 camadas | `manutencao-completa.md` |
| **Complexa** | 10+ arquivos, múltiplas camadas | `manutencao-completa.md` + aprovação |

---

### FASE 4: Geração de Prompt de Correção (OBRIGATÓRIA)

#### PASSO 4.1: Gerar Prompt Estruturado

**Formato obrigatório do prompt de correção:**

```
Seguindo o contrato D:\IC2_Governanca\governanca\contracts\{CONTRATO_APROPRIADO}.
Modo governanca rigida. Nao negociar escopo. Nao extrapolar.
Seguir D:\IC2\CLAUDE.md.

Para corrigir o seguinte problema:

---
## PROBLEMA IDENTIFICADO

**Descrição:** {DESCRIÇÃO_BREVE_DO_PROBLEMA}

**RF Afetado:** {RF_ID} (se aplicável)

**Rota/Tela Afetada:** {ROTA_URL}

**Componente Afetado:** {CAMINHO_COMPONENTE}

---
## EVIDÊNCIAS COLETADAS

### Console Logs
```
{LOGS_CAPTURADOS}
```

### Network Requests Falhando
```
{REQUESTS_COM_ERRO}
```

### Screenshot
Arquivo: D:\IC2\.temp_ia\debug-screenshot-{timestamp}.png

---
## CAUSA RAIZ

{EXPLICAÇÃO_DETALHADA_DA_CAUSA}

**Arquivo(s) Afetado(s):**
- {CAMINHO_ARQUIVO_1} (linhas aproximadas: {LINHAS})
- {CAMINHO_ARQUIVO_2} (linhas aproximadas: {LINHAS})

---
## CORREÇÃO NECESSÁRIA

**O que precisa ser feito:**
1. {AÇÃO_1}
2. {AÇÃO_2}
3. {AÇÃO_3}

**Escopo estimado:** {CIRÚRGICO | MODERADO | COMPLEXO}

**Contrato recomendado:** `{NOME_CONTRATO}.md`

---
## VALIDAÇÃO DA CORREÇÃO

**Após correção, validar:**
- [ ] {VALIDAÇÃO_1}
- [ ] {VALIDAÇÃO_2}
- [ ] {VALIDAÇÃO_3}
- [ ] Executar script de debug novamente (deve passar sem erros)
- [ ] Acessar rota {ROTA} e verificar comportamento correto
```

---

#### PASSO 4.2: Exibir Prompt ao Usuário

**OBRIGATÓRIO:** Exibir o prompt completo na saída do agente (não criar arquivo).

**Formato de saída:**

```
========================================
DIAGNÓSTICO COMPLETO
========================================

{PROMPT_GERADO_ACIMA}

========================================
PRÓXIMOS PASSOS
========================================

1. Copiar o prompt acima
2. Iniciar nova sessão com o contrato recomendado
3. Colar o prompt para executar a correção
```

---

## 6. PROIBIÇÕES CRÍTICAS

### 6.1. O Que NÃO Fazer

❌ **PROIBIDO:**
1. **Corrigir código** durante o debug (usar contrato de manutenção depois)
2. **Modificar testes oficiais** (apenas criar temporários em `.temp_ia/`)
3. **Criar arquivos de relatório** (diagnóstico deve ser exibido em texto)
4. **Tomar decisões sobre correção** (apenas diagnosticar e recomendar)
5. **Executar operações destrutivas** (não deletar, não limpar banco)
6. **Negociar escopo** (seguir CLAUDE.md rigorosamente)
7. **Extrapolar para correção** (foco exclusivo em diagnóstico)

### 6.2. Escalação Obrigatória

**Se durante o debug você identificar:**
- Problema exige refatoração cross-layer → Alertar usuário e recomendar `manutencao-completa.md`
- Problema é arquitetural → Alertar usuário e recomendar revisão de arquitetura
- Problema não é reproduzível → Alertar usuário e solicitar mais informações
- Pré-requisitos não atendidos → PARAR e informar o que falta

**Regra de Ouro:** SE ALGO ESTÁ FORA DO ESCOPO, PARE E ALERTE.

---

## 7. ESTRUTURA DE ARQUIVOS

### 7.1. Arquivos Temporários (Criados pelo Debug)

```
D:\IC2\.temp_ia\
├── debug-playwright-{timestamp}.spec.ts       # Script de debug temporário
├── debug-screenshot-{timestamp}.png           # Screenshot da tela com problema
└── debug-evidencias-{timestamp}.txt           # Logs consolidados (opcional)
```

**IMPORTANTE:** Todos os arquivos de debug são temporários e devem ser criados em `.temp_ia/`.

---

## 8. COMANDOS DE REFERÊNCIA

### 8.1. Validação de Ambiente

```bash
# Iniciar ambiente (mata processos anteriores e inicia backend + frontend)
python D:\IC2\run.py

# Backend health
curl http://localhost:5000/health

# Frontend disponibilidade
curl http://localhost:4200

# Playwright versão
npx playwright --version

# Playwright browsers instalados
npx playwright install --dry-run
```

### 8.2. Execução de Debug

```bash
# Executar script de debug (headed)
npx playwright test {SCRIPT} --headed --project=chromium

# Executar com debug interativo
npx playwright test {SCRIPT} --debug

# Executar com UI
npx playwright test --ui {SCRIPT}

# Codegen para gravar interações
npx playwright codegen http://localhost:4200/{ROTA}
```

### 8.3. Captura de Evidências

```bash
# Screenshot de rota específica
npx playwright screenshot http://localhost:4200/{ROTA} screenshot.png

# Trace (gravação completa da execução)
npx playwright test {SCRIPT} --trace on
npx playwright show-trace trace.zip
```

---

## 9. EXEMPLOS DE USO

### Exemplo 1: Debug de Merge Conflict no HTML

**Descrição:** Usuário reporta que merge conflict aparece na tela de login.

**Execução:**

1. **Validar ambiente:**
   ```bash
   curl http://localhost:4200/sign-in
   ```

2. **Criar script de debug:**
   ```typescript
   test('Debug: Merge conflict visível no HTML', async ({ page }) => {
     await page.goto('http://localhost:4200/sign-in');

     // Capturar HTML da página
     const html = await page.content();

     // Procurar por merge markers
     const hasConflict = html.includes('<<<<<<<') || html.includes('>>>>>>>');

     // Capturar screenshot
     await page.screenshot({ path: 'D:\\IC2\\.temp_ia\\debug-merge-conflict.png' });

     // Exibir resultado
     console.log('Merge conflict encontrado:', hasConflict);
     if (hasConflict) {
       console.log('HTML com conflito:', html.substring(html.indexOf('<<<<<<<'), html.indexOf('>>>>>>>') + 50));
     }
   });
   ```

3. **Diagnosticar:**
   - Merge conflict encontrado em `sign-in.component.html` linhas 10-16
   - Conflito entre `HEAD` e commit `37fc47bf`
   - Impacto: Visível para o usuário, bloqueia login

4. **Gerar prompt de correção:**
   ```
   Seguindo o contrato D:\IC2_Governanca\governanca\contracts\manutencao\manutencao-controlada.md.
   Modo governanca rigida. Nao negociar escopo. Nao extrapolar.
   Seguir D:\IC2\CLAUDE.md.

   Para corrigir o seguinte problema:

   ## PROBLEMA IDENTIFICADO
   Merge conflict visível no HTML da tela de login

   ## CAUSA RAIZ
   Arquivo D:\IC2\frontend\icontrolit-app\src\app\modules\auth\sign-in\sign-in.component.html
   contém markers de merge (<<<<<<< HEAD, =======, >>>>>>>)

   ## CORREÇÃO NECESSÁRIA
   1. Abrir sign-in.component.html
   2. Remover merge markers (linhas 10-16)
   3. Manter versão correta do código
   4. Validar que página renderiza corretamente
   ```

---

### Exemplo 2: Debug de Erro i18n

**Descrição:** Console mostra "Error while trying to load 'pt'"

**Execução:**

1. **Criar script de debug:**
   ```typescript
   test('Debug: Erro i18n ao carregar pt', async ({ page }) => {
     const errors: string[] = [];
     page.on('pageerror', err => errors.push(err.message));

     const requests: { url: string, status: number }[] = [];
     page.on('response', res => {
       if (res.url().includes('i18n') || res.url().includes('.json')) {
         requests.push({ url: res.url(), status: res.status() });
       }
     });

     await page.goto('http://localhost:4200/sign-in');
     await page.waitForTimeout(3000);

     console.log('=== ERRORS ===');
     errors.forEach(e => console.log(e));

     console.log('\n=== i18n REQUESTS ===');
     requests.forEach(r => console.log(`${r.status} ${r.url}`));
   });
   ```

2. **Diagnosticar:**
   - Request para `/assets/i18n/pt.json` retorna 404
   - Arquivo não existe ou caminho incorreto
   - Impacto: Textos não traduzidos na tela

3. **Gerar prompt de correção** (similar ao exemplo 1)

---

## 10. CRITÉRIOS DE SUCESSO

**O debug é considerado BEM-SUCEDIDO quando:**

- [x] Ambiente foi validado (backend + frontend rodando)
- [x] Script de debug foi executado com sucesso
- [x] Evidências foram coletadas (logs, screenshots, network)
- [x] Causa raiz foi identificada com precisão
- [x] Arquivos afetados foram localizados
- [x] Prompt de correção foi gerado no formato correto
- [x] Escopo da correção foi estimado (cirúrgico/moderado/complexo)
- [x] Contrato de manutenção apropriado foi recomendado

**O debug FALHA quando:**

- [ ] Pré-requisitos não foram atendidos (ambiente não rodando)
- [ ] Problema não foi reproduzido
- [ ] Causa raiz não foi identificada
- [ ] Arquivos afetados não foram localizados
- [ ] Prompt de correção está incompleto

---

## 11. GOVERNANÇA E COMPLIANCE

### 11.1. Conformidade com CLAUDE.md

Este contrato segue **RIGOROSAMENTE** as regras de `D:\IC2\CLAUDE.md`:

- ✅ Modo de governança rígida ativado
- ✅ Escopo não negociável (diagnóstico apenas)
- ✅ Arquivos temporários criados em `.temp_ia/`
- ✅ Nenhuma correção de código durante debug
- ✅ Saída em texto (não criar arquivos de relatório)
- ✅ Escalação obrigatória quando fora do escopo

### 11.2. Regras de Negação Zero

**Se solicitação conflitar com este contrato:**
- ❌ Execução **DEVE** ser **NEGADA**
- ❌ Agente **DEVE** explicar o motivo
- ❌ Agente **DEVE** solicitar ajuste formal

**Exemplos de solicitações negadas:**
1. "Debug e já corrija o problema" → **NEGADO** (contrato só faz diagnóstico)
2. "Debug sem ambiente rodando" → **NEGADO** (pré-requisito não atendido)
3. "Debug e refatore o código" → **NEGADO** (refatoração fora do escopo)

---

## 12. REFERÊNCIAS

### 12.1. Documentos Relacionados

| Documento | Propósito |
|-----------|-----------|
| `D:\IC2\CLAUDE.md` | Governança superior (ler sempre) |
| `D:\IC2_Governanca\governanca\checklists\debug\pre-debug-playwright.yaml` | Checklist pré-debug |
| `D:\IC2_Governanca\governanca\prompts\debug\debug-playwright.md` | Prompt de ativação |
| `D:\IC2_Governanca\governanca\contracts\manutencao\manutencao-controlada.md` | Correções cirúrgicas |
| `D:\IC2_Governanca\governanca\contracts\manutencao\manutencao-completa.md` | Correções complexas |

### 12.2. Ferramentas Relacionadas

| Ferramenta | Uso |
|------------|-----|
| Playwright | Debug interativo e automático |
| Chrome DevTools | Inspeção manual complementar |
| cURL | Validação de endpoints |

---

## Changelog

### v1.0 (2026-01-08)
- Criação do contrato de debug com Playwright
- Definição de escopo (diagnóstico apenas, sem correção)
- Estrutura de 4 fases (Preparação, Execução, Diagnóstico, Prompt)
- Geração de prompt estruturado para correção posterior
- Exemplos práticos (merge conflict, erro i18n)
- Conformidade com CLAUDE.md e governança rígida

---

**Mantido por:** Time de Arquitetura IControlIT
**Última Atualização:** 2026-01-08
**Versão:** 1.0 - Debug com Playwright
