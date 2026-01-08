# PROMPT DE ATIVAÇÃO: DEBUG COM PLAYWRIGHT

**Versão:** 1.0
**Data:** 2026-01-08
**Contrato Relacionado:** `governanca/contracts/debug/debug-playwright.md`

---

## COMO USAR ESTE PROMPT

Este prompt ativa o **Contrato de Debug com Playwright**, que investiga e diagnostica problemas no frontend usando Playwright.

**IMPORTANTE:** Este prompt **NÃO corrige problemas**. Apenas investiga, diagnostica e gera um prompt estruturado para correção posterior.

---

## PROMPT DE ATIVAÇÃO

```
Seguindo o contrato D:\IC2_Governanca\governanca\contracts\debug\debug-playwright.md.
Modo governanca rigida. Nao negociar escopo. Nao extrapolar.
Seguir D:\IC2\CLAUDE.md.

Para investigar e diagnosticar o seguinte problema:

---
## DESCRIÇÃO DO PROBLEMA

{DESCREVA_O_PROBLEMA_AQUI}

Exemplo:
- "Merge conflict aparecendo no HTML da tela de login"
- "Erro no console: Error while trying to load 'pt'"
- "Botão de salvar não funciona na tela de cadastro"
- "Tela de relatórios carrega em branco"

---
## CONTEXTO ADICIONAL (se disponível)

**RF Afetado:** {RF_ID ou "Não identificado"}

**Rota/Tela Afetada:** {URL da rota, ex: /sign-in, /dashboard, /relatorios}

**Comportamento Esperado:** {O que deveria acontecer}

**Comportamento Atual:** {O que está acontecendo}

**Evidências Iniciais (se houver):**
- Console logs observados
- Erros visuais observados
- Screenshots disponíveis

---
## RESULTADO ESPERADO

Ao final do debug, espero receber:

1. ✅ **Diagnóstico completo** do problema
2. ✅ **Evidências coletadas** (logs, screenshots, network requests)
3. ✅ **Causa raiz identificada** com arquivo(s) e linha(s) afetadas
4. ✅ **Prompt estruturado** para correção do problema
5. ✅ **Recomendação de contrato** para execução da correção
```

---

## TEMPLATE SIMPLIFICADO (COPIAR E COLAR)

```
Seguindo o contrato D:\IC2_Governanca\governanca\contracts\debug\debug-playwright.md.
Modo governanca rigida. Nao negociar escopo. Nao extrapolar.
Seguir D:\IC2\CLAUDE.md.

Para investigar e diagnosticar o seguinte problema:

**DESCRIÇÃO:**
{DESCREVA_AQUI}

**ROTA/TELA:**
{ROTA_AFETADA}

**COMPORTAMENTO ESPERADO:**
{O_QUE_DEVERIA_ACONTECER}

**COMPORTAMENTO ATUAL:**
{O_QUE_ESTA_ACONTECENDO}
```

---

## EXEMPLOS DE USO

### Exemplo 1: Merge Conflict Visível

```
Seguindo o contrato D:\IC2_Governanca\governanca\contracts\debug\debug-playwright.md.
Modo governanca rigida. Nao negociar escopo. Nao extrapolar.
Seguir D:\IC2\CLAUDE.md.

Para investigar e diagnosticar o seguinte problema:

**DESCRIÇÃO:**
Merge conflict aparecendo no HTML da tela de login. Os markers <<<<<<< HEAD e >>>>>>> estão visíveis para o usuário.

**ROTA/TELA:**
/sign-in

**COMPORTAMENTO ESPERADO:**
Tela de login renderizada corretamente com logo e formulário

**COMPORTAMENTO ATUAL:**
Texto literal dos merge markers aparece na página
```

---

### Exemplo 2: Erro de i18n

```
Seguindo o contrato D:\IC2_Governanca\governanca\contracts\debug\debug-playwright.md.
Modo governanca rigida. Nao negociar escopo. Nao extrapolar.
Seguir D:\IC2\CLAUDE.md.

Para investigar e diagnosticar o seguinte problema:

**DESCRIÇÃO:**
Console mostra erro "Error while trying to load 'pt'" ao acessar qualquer tela

**ROTA/TELA:**
Todas as rotas (começa em /sign-in)

**COMPORTAMENTO ESPERADO:**
Textos em português carregados corretamente via Transloco

**COMPORTAMENTO ATUAL:**
Erro no console, textos aparecem como chaves (ex: "auth.signIn.form.title")
```

---

### Exemplo 3: Botão Não Funciona

```
Seguindo o contrato D:\IC2_Governanca\governanca\contracts\debug\debug-playwright.md.
Modo governanca rigida. Nao negociar escopo. Nao extrapolar.
Seguir D:\IC2\CLAUDE.md.

Para investigar e diagnosticar o seguinte problema:

**DESCRIÇÃO:**
Botão "Salvar" não responde ao clique na tela de cadastro de cliente

**RF AFETADO:**
RF006 - Gestão de Clientes

**ROTA/TELA:**
/clientes/novo

**COMPORTAMENTO ESPERADO:**
Ao clicar em "Salvar", formulário deve ser enviado e cliente criado

**COMPORTAMENTO ATUAL:**
Nada acontece ao clicar no botão. Nenhum erro no console visível inicialmente.
```

---

### Exemplo 4: Tela em Branco

```
Seguindo o contrato D:\IC2_Governanca\governanca\contracts\debug\debug-playwright.md.
Modo governanca rigida. Nao negociar escopo. Nao extrapolar.
Seguir D:\IC2\CLAUDE.md.

Para investigar e diagnosticar o seguinte problema:

**DESCRIÇÃO:**
Tela de relatórios carrega completamente em branco após navegação

**ROTA/TELA:**
/relatorios/vendas

**COMPORTAMENTO ESPERADO:**
Grid com dados de vendas, filtros e botão de exportar

**COMPORTAMENTO ATUAL:**
Tela branca. Header e sidebar aparecem, mas área de conteúdo está vazia.
```

---

## PRÉ-REQUISITOS ANTES DE USAR

Antes de ativar este prompt, **VALIDE**:

- [ ] Backend está rodando (`curl http://localhost:5000/health` → 200)
- [ ] Frontend está rodando (`curl http://localhost:4200` → 200)
- [ ] Playwright está instalado (`npx playwright --version`)
- [ ] Você tem descrição clara do problema
- [ ] Você identificou qual rota/tela está afetada (se aplicável)

**Se algum pré-requisito falhar:**
- Corrija antes de ativar o prompt
- O contrato irá validar novamente e bloquear execução se necessário

---

## O QUE ACONTECE APÓS ATIVAR

1. **Validação de Pré-Requisitos:**
   - Checklist `pre-debug-playwright.yaml` será executado
   - Se falhar alguma validação bloqueante, debug será interrompido

2. **Criação de Script de Debug:**
   - Script temporário será criado em `D:\IC2\.temp_ia\debug-playwright-{timestamp}.spec.ts`
   - Script será configurado para reproduzir o problema

3. **Execução do Debug:**
   - Playwright abrirá browser (headed mode)
   - Navegará até a rota afetada
   - Capturará logs, network requests, screenshots

4. **Diagnóstico:**
   - Evidências serão analisadas
   - Causa raiz será identificada
   - Arquivos e linhas afetadas serão localizados

5. **Geração de Prompt de Correção:**
   - Prompt estruturado será exibido na tela
   - Contrato de manutenção apropriado será recomendado
   - Você poderá copiar o prompt e iniciar correção

---

## O QUE NÃO ACONTECE

❌ **Este debug NÃO irá:**
- Corrigir o código automaticamente
- Modificar arquivos de produção
- Criar arquivos de relatório (diagnóstico é exibido em texto)
- Tomar decisões sobre qual correção aplicar
- Executar operações destrutivas

**Para correção:** Use o prompt gerado ao final do debug com o contrato de manutenção recomendado.

---

## FLUXO COMPLETO (DEBUG → CORREÇÃO)

### Passo 1: Debug (este prompt)
```
Seguindo o contrato D:\IC2_Governanca\governanca\contracts\debug\debug-playwright.md.
...
Para investigar e diagnosticar o seguinte problema:
{DESCRIÇÃO_DO_PROBLEMA}
```

**Saída:** Prompt de correção estruturado

---

### Passo 2: Correção (prompt gerado)
```
Seguindo o contrato D:\IC2_Governanca\governanca\contracts\manutencao\manutencao-controlada.md.
Modo governanca rigida. Nao negociar escopo. Nao extrapolar.
Seguir D:\IC2\CLAUDE.md.

Para corrigir o seguinte problema:

## PROBLEMA IDENTIFICADO
{DIAGNÓSTICO_COMPLETO_DO_DEBUG}

## EVIDÊNCIAS COLETADAS
{LOGS_SCREENSHOTS_NETWORK}

## CAUSA RAIZ
{ARQUIVOS_E_LINHAS_AFETADAS}

## CORREÇÃO NECESSÁRIA
{PASSOS_PARA_CORRIGIR}
```

---

## QUANDO NÃO USAR ESTE PROMPT

❌ **NÃO use este prompt quando:**

1. **Problema já está claramente identificado:**
   - Você já sabe qual arquivo e linha precisa corrigir
   - **Use:** Prompt de manutenção diretamente

2. **Problema é de backend:**
   - Erro ocorre na API, não no frontend
   - **Use:** Debug de backend apropriado

3. **Problema é de build/compilação:**
   - Código não compila
   - **Use:** Correção de build antes de debug

4. **Ambiente não está rodando:**
   - Backend ou frontend não iniciaram
   - **Use:** `python run.py` primeiro

---

## TROUBLESHOOTING

### Debug não inicia

**Problema:** Checklist pré-debug reprova

**Solução:**
- Verificar saída do checklist
- Corrigir validações que falharam
- Reexecutar prompt após correção

---

### Browser não abre

**Problema:** Playwright instalado mas browsers faltando

**Solução:**
```bash
npx playwright install
```

---

### Problema não reproduzível

**Problema:** Debug executa mas não encontra o erro

**Solução:**
- Verificar se rota está correta
- Verificar se problema é intermitente
- Adicionar mais detalhes na descrição do problema
- Tentar reproduzir manualmente primeiro

---

### Timeout ao acessar frontend

**Problema:** Frontend demora mais de 120s para responder

**Solução:**
- Aguardar compilação Angular completar
- Verificar se frontend realmente iniciou
- Verificar logs do terminal onde frontend está rodando

---

## REFERÊNCIAS

### Documentos Relacionados

| Documento | Propósito |
|-----------|-----------|
| `D:\IC2\CLAUDE.md` | Governança superior |
| `governanca/contracts/debug/debug-playwright.md` | Contrato de debug completo |
| `governanca/checklists/debug/pre-debug-playwright.yaml` | Checklist de pré-requisitos |
| `governanca/contracts/manutencao/manutencao-controlada.md` | Correção cirúrgica (1-3 arquivos) |
| `governanca/contracts/manutencao/manutencao-completa.md` | Correção complexa (4+ arquivos) |

### Comandos Úteis

```bash
# Validar ambiente antes do debug
curl http://localhost:5000/health  # Backend
curl http://localhost:4200         # Frontend

# Verificar Playwright
npx playwright --version           # Versão instalada
npx playwright install             # Instalar browsers

# Iniciar ambiente (se necessário)
python D:\IC2\run.py               # Mata processos anteriores e inicia backend + frontend

# Após debug, ver arquivos temporários
ls D:\IC2\.temp_ia\debug-*
```

---

## DICAS DE USO

### 1. Seja Específico na Descrição

**❌ Ruim:** "Login não funciona"

**✅ Bom:** "Ao clicar em 'Entrar' na tela de login, nada acontece. Credenciais corretas foram inseridas mas botão não responde."

---

### 2. Identifique a Rota

**❌ Ruim:** "Problema na tela de cadastro"

**✅ Bom:** "Problema em /clientes/novo ao tentar salvar formulário"

---

### 3. Descreva o Comportamento Esperado

**❌ Ruim:** "Botão quebrado"

**✅ Bom:** "Esperado: Ao clicar em 'Salvar', modal de confirmação deve aparecer. Atual: Nada acontece."

---

### 4. Forneça Evidências Iniciais (se tiver)

**✅ Bom:**
```
Erro observado no console:
TypeError: Cannot read property 'name' of undefined
  at ClientFormComponent.save (client-form.component.ts:45)
```

---

## CHANGELOG

### v1.0 (2026-01-08)
- Criação do prompt de ativação de debug
- Template simplificado para copiar e colar
- 4 exemplos práticos de uso
- Guia de troubleshooting
- Fluxo completo debug → correção
- Dicas de uso para descrições eficazes

---

**Mantido por:** Time de Arquitetura IControlIT
**Última Atualização:** 2026-01-08
**Versão:** 1.0 - Prompt de Ativação
