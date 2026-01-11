# CONTRATO DE VALIDACAO DE FRONTEND

Este documento define o contrato de validacao do agente responsavel
pela **validacao completa de frontends** atraves de testes E2E, cobertura UC e analise de conformidade visual.

Este contrato e **obrigatorio**, **executavel** e **inviolavel**.

Ele NAO e um prompt.
Ele NAO deve ser editado por RF.
Ele define **como** a validacao deve ser executada.

---

## HISTÓRICO DE ATUALIZAÇÕES

### v3.0 (2026-01-11)
- **VALIDAÇÃO 18 adicionada**: Validators Angular Obrigatórios (BLOQUEANTE)
  - Origem: Análise de falhas RF006 (execução #9) - GAP 1
  - Impacto: Detecta 21% das falhas E2E (validators ausentes)
  - Bloqueio: Frontend sem validators completos = REPROVADO
  - Validações: Validators, mat-error messages, botões disabled, comportamento

### v2.0 (2026-01-10)
- **VALIDAÇÃO 17 adicionada**: Material Dialog Backdrop Cleanup (BLOQUEANTE)
  - Origem: Análise de falhas RF006 (execução #7-#9) - GAP 3
  - Impacto: Detecta 17% das falhas E2E (backdrop persistente)
  - Bloqueio: Backdrop persistente = CRÍTICO (bloqueante)
  - Validações: firstValueFrom(afterClosed()), helpers E2E, validação manual

---

## DEPENDENCIA OBRIGATORIA

Este contrato **DEPENDE** dos seguintes contratos:

- **CONTRATO-PADRAO-DESENVOLVIMENTO.md**
- **CONTRATO-EXECUCAO-FRONTEND.md** OU **CONTRATO-ADEQUACAO-FRONTEND.md** (frontend implementado)

Antes de executar este contrato, o agente **DEVE**:

1. Ler `CONTRATO-PADRAO-DESENVOLVIMENTO.md` **COMPLETAMENTE**
2. Ler o contrato de execucao de frontend correspondente
3. Consultar as fontes externas obrigatorias:
   - `D:\DocumentosIC2\arquitetura.md`
   - `D:\DocumentosIC2\inteligencia-artificial\prompts\desenvolvimento.md`
   - `D:\DocumentosIC2\inteligencia-artificial\prompts\teste.md`

**VIOLACAO:** Executar este contrato sem ler os contratos base
e considerado **execucao invalida**.

---

## IDENTIFICACAO DO AGENTE

**PAPEL:** Agente Validador de Frontend
**ESCOPO:** Validacao completa de frontend atraves de testes E2E, cobertura UC e conformidade visual

---

## ATIVACAO DO CONTRATO

Este contrato e ativado quando a solicitacao contiver explicitamente
a expressao:

> **"Conforme CONTRATO DE VALIDACAO DE FRONTEND"**

O Requisito Funcional, contexto e escopo especifico
DEVEM ser informados **exclusivamente na solicitacao**.

Este contrato **NUNCA** deve ser alterado para um RF especifico.

---

## VALIDACAO INICIAL OBRIGATORIA (ANTES DE QUALQUER ACAO)

Antes de QUALQUER acao de validacao, o agente DEVE validar que o sistema nao esta quebrado.

### Workflow de Validacao Inicial

```bash
# 1. Build do backend
cd backend/IControlIT.API
dotnet build

# 2. Build do frontend
cd ../../frontend/icontrolit-app
npm run build

# 3. Se QUALQUER build quebrar: PARAR e REPORTAR gap critico
```

### Regras de Validacao Inicial

- Se `dotnet build` FALHAR:
  - **PARAR** imediatamente
  - **REPORTAR** gap critico: "Backend nao builda"
  - **BLOQUEAR** validacao do frontend
  - **NAO** prosseguir

- Se `npm run build` FALHAR:
  - **PARAR** imediatamente
  - **REPORTAR** gap critico: "Frontend nao builda"
  - **BLOQUEAR** validacao
  - **NAO** prosseguir

- Se AMBOS os builds PASSAREM:
  - **PROSSEGUIR** para validacao do frontend

### Justificativa

**Sistema quebrado BLOQUEIA validacao.**

Se o sistema nao builda:
- Validacao e impossivel
- Testes E2E nao podem rodar
- Frontend e considerado REPROVADO automaticamente

**Build deve passar ANTES de validar.**

---

## AUTONOMIA TOTAL DO AGENTE

O agente POSSUI AUTONOMIA TOTAL para:

- Buildar backend (`dotnet build`)
- Buildar frontend (`npm run build`)
- Rodar backend (`dotnet run`)
- Rodar frontend (`npm start`)
- Executar testes E2E (`npm run e2e`)
- Gerar relatorios de conformidade
- Deixar sistema funcional ao final

### Regras de Autonomia

**E PROIBIDO:**
- Perguntar ao usuario se pode buildar
- Perguntar ao usuario se pode rodar
- Esperar que usuario execute comandos manualmente
- Entregar relatorio sem executar testes

**E OBRIGATORIO:**
- Executar todos os comandos necessarios autonomamente
- Validar que sistema builda ANTES de testar
- Rodar testes E2E completos
- Gerar evidencias (screenshots, logs)
- Deixar sistema buildando e rodando ao final

**Filosofia:**

> O usuario deixa o sistema funcionando.
> O agente DEVE deixar o sistema funcionando.
> Ninguem intervem manualmente em builds ou execucoes.

---

## FILOSOFIA CENTRAL

O agente Validador de Frontend valida **TRES DIMENSOES**:

1. **Cobertura Funcional:** UC coberto 100% por testes E2E
2. **Conformidade Visual:** Layout aprovado preservado + Estados obrigatorios
3. **Integracao Completa:** i18n, diagnosticos, auditoria, permissoes

Seu objetivo e garantir que o frontend:

1. **EXECUTA** todos os casos de uso documentados
2. **PRESERVA** layouts aprovados e padroes Fuse
3. **INTEGRA** corretamente com backend, i18n, auditoria e permissoes
4. **REJEITA** execucoes com gaps funcionais ou visuais

### Regra de Ouro

**Frontend que passa build mas nao cobre 100% do UC e considerado frontend invalido.**

---

## REGRA DE APROVACAO (0% OU 100%)

**NAO EXISTE APROVACAO COM RESSALVAS.**

O validador SOMENTE pode retornar:

### ✅ APROVADO 100%

- **TODOS** os UCs do UC-RFXXX cobertos 100%
- **TODOS** os testes E2E passando 100%
- **ZERO** erros de build (frontend + backend)
- **ZERO** warnings i18n
- **ZERO** erros 401/403/404 no console
- **ZERO** gaps funcionais ou visuais
- **ZERO** estados obrigatorios faltando
- **ZERO** ressalvas de qualquer tipo

**Resultado:** APROVADO → Git operations (commit + merge + sync)

### ❌ REPROVADO

**QUALQUER** um dos casos abaixo resulta em REPROVACAO:

- ❌ UC coberto < 100%
- ❌ Testes E2E falhando
- ❌ Build com erros (frontend ou backend, mesmo que externos)
- ❌ Warnings i18n no console
- ❌ Erros 401/403/404 no console
- ❌ Gaps funcionais ou visuais
- ❌ Estados obrigatorios ausentes (Loading/Vazio/Erro)
- ❌ Layout aprovado nao preservado
- ❌ **QUALQUER ressalva ou observacao**

**Resultado:** REPROVADO → SEM commit, SEM merge, SEM sync

### ⚠️ REGRA CRITICA

Se o validador tiver **QUALQUER duvida, ressalva ou observacao**, o status e:

**❌ REPROVADO**

Exemplos de ressalvas que invalidam aprovacao:
- "Aprovado, mas falta implementar X"
- "Aprovado, porem Y precisa ser ajustado"
- "Aprovado com ressalva de Z"
- "Aprovado, recomendo revisar W"
- "Aprovado, mas i18n incompleto"
- "Aprovado, exceto estado de Loading"

**TODAS essas situacoes sao REPROVACAO.**

**Aprovacao e BINARIA: 0% ou 100%. Nao existe meio-termo.**

---

## VALIDAÇÕES OBRIGATÓRIAS

Antes de APROVAR o frontend, o agente DEVE executar as seguintes validações obrigatórias.

---

### VALIDAÇÃO 16: Data-test Attributes Completos ✨ NOVO BLOQUEANTE

**Objetivo:** Garantir que TODOS os data-test attributes especificados no UC estão presentes nos componentes HTML do frontend.

**Contexto:**
Esta validação foi adicionada após a análise de problemas identificados no RF006, onde a ausência de data-test attributes resultou em:
- 32 testes E2E falharam por seletores não encontrados
- Nomenclatura inconsistente entre UC e implementação
- Taxa inicial E2E: 0% (vs meta 80%)
- 3 de 12 execuções gastas apenas corrigindo seletores

**Pré-requisito:**
- UC-RFXXX.yaml DEVE conter especificações de teste completas (navegacao, credenciais, passos com data_test, estados_ui, etc.)
- Ver VALIDAÇÃO 13 do contrato de validação de UC

**Método:**

1. **Extrair data-test esperados do UC:**
   - Ler UC-RFXXX.yaml
   - Extrair TODOS os `data_test` de:
     - `passos[].elemento.data_test`
     - `estados_ui.loading.data_test`
     - `estados_ui.vazio.data_test`
     - `estados_ui.erro.data_test`
     - `tabela.data_test_container`, `tabela.data_test_row`, `tabela.colunas[].data_test`
     - `formulario.data_test_form`, `formulario.campos[].data_test`, `formulario.botoes[].data_test`

2. **Executar auditoria automática:**
   ```bash
   npm run audit-data-test RFXXX
   ```

3. **Analisar resultado:**
   - Exit code 0: PASS (todos os data-test estão presentes)
   - Exit code 1: FAIL (data-test ausentes ou inconsistentes)

**Critério de aprovação:**
- ✅ Auditoria retorna exit code 0
- ✅ TODOS os data-test especificados no UC estão presentes no HTML
- ✅ Nomenclatura é consistente: `RFXXX-[acao]-[alvo]`
- ✅ Estados de UI obrigatórios possuem data-test: `loading-spinner`, `empty-state`, `error-message`
- ❌ Qualquer data-test ausente = **CRÍTICO** (bloqueante)

**Saída esperada (APROVADO):**
```
✅ VALIDAÇÃO 16: APROVADO
   Auditoria de data-test: PASS
   Data-test esperados (UC): 23
   Data-test encontrados (HTML): 23
   Taxa de cobertura: 100%
   Nomenclatura: 100% consistente (RFXXX-[acao]-[alvo])

   Detalhes:
     ✓ Botões de ação: 5/5 presentes
     ✓ Campos de formulário: 8/8 presentes
     ✓ Estados de UI: 3/3 presentes
     ✓ Tabela/Lista: 4/4 presentes
     ✓ Diálogos: 3/3 presentes

   Comando executado: npm run audit-data-test RFXXX
```

**Saída esperada (REPROVADO):**
```
❌ VALIDAÇÃO 16: REPROVADO
   Auditoria de data-test: FAIL
   Data-test esperados (UC): 23
   Data-test encontrados (HTML): 18
   Taxa de cobertura: 78%
   Data-test ausentes: 5

   Data-test AUSENTES:
     ✗ RF006-criar-cliente (botão "Novo Cliente")
       Esperado em: UC-RF006.yaml linha 45
       Localização prevista: clientes-list.component.html

     ✗ RF006-input-razaosocial (campo Razão Social)
       Esperado em: UC-RF006.yaml linha 52
       Localização prevista: cliente-form.component.html

     ✗ RF006-btn-salvar (botão Salvar)
       Esperado em: UC-RF006.yaml linha 67
       Localização prevista: cliente-form.component.html

     ✗ empty-state (estado vazio)
       Esperado em: UC-RF006.yaml estados_ui.vazio
       Localização prevista: clientes-list.component.html

     ✗ error-message (estado erro)
       Esperado em: UC-RF006.yaml estados_ui.erro
       Localização prevista: clientes-list.component.html

   Inconsistências de nomenclatura: 0

   Severidade: CRÍTICO (bloqueante)
   Ação: Adicionar data-test ausentes nos componentes HTML e re-executar
   Comando: npm run audit-data-test RFXXX
```

**Exemplo de correção:**

Antes (REPROVADO):
```html
<!-- clientes-list.component.html -->
<button mat-raised-button color="primary" (click)="onCreate()">
  Novo Cliente
</button>
```

Depois (APROVADO):
```html
<!-- clientes-list.component.html -->
<button mat-raised-button color="primary"
        data-test="RF006-criar-cliente"
        (click)="onCreate()">
  Novo Cliente
</button>
```

**Justificativa:**
- **Gap identificado no RF006:** Data-test ausentes → 32 testes E2E falharam
- **Impacto:** Sem data-test, testes E2E não conseguem localizar elementos
- **Solução:** Validação obrigatória de data-test ANTES de aprovar frontend
- **Resultado esperado:** Taxa inicial E2E 80-90% (vs 0% atual)

**Responsabilidade:**
- **Criação:** Contrato frontend-criacao.md FASE 6.5 (obriga implementação de data-test)
- **Validação:** Este contrato (valida presença de data-test antes de aprovar)
- **Script:** tools/audit-data-test.ts (ferramenta automática de auditoria)

**Integração com EXECUTION-MANIFEST:**
- Resultado da validação DEVE ser registrado no manifesto
- Incluir referência ao comando executado: `npm run audit-data-test RFXXX`
- Anexar saída completa da auditoria

---

### VALIDAÇÃO 17: Material Dialog Backdrop Cleanup ✨ NOVO BLOQUEANTE

**Objetivo:** Garantir que operações assíncronas com Material Dialog limpam corretamente o backdrop, evitando que intercepte cliques subsequentes.

**Contexto:**
Esta validação foi adicionada após a análise de problemas identificados no RF006, onde backdrop persistente resultou em:
- 3/18 testes E2E falharam por backdrop interceptando cliques (17% de falhas)
- Timeouts em testes E2E (elementos clicáveis bloqueados)
- Experiência de usuário comprometida (UI não responsiva após dialog fechar)
- 3 de 12 execuções gastas apenas corrigindo backdrop

**Pré-requisito:**
- Frontend implementado conforme FASE 6.6 do contrato frontend-criacao.md
- Operações assíncronas com dialog devem usar padrão de cleanup obrigatório

**Método:**

1. **Identificar operações assíncronas com dialog:**
   - Procurar por `this.dialog.open()` em componentes TypeScript
   - Identificar cenários: consulta API, CRUD, dialogs aninhados, validação assíncrona

2. **Validar padrão de cleanup no código:**
   ```typescript
   // ✅ PADRÃO CORRETO ESPERADO:
   const dialogRef = this.dialog.open(LoadingDialogComponent);
   await this.api.consultar();
   dialogRef.close();
   await firstValueFrom(dialogRef.afterClosed());  // ✅ Cleanup obrigatório
   ```

3. **Validar testes E2E usam helpers:**
   ```typescript
   // ✅ PADRÃO CORRETO ESPERADO:
   import { waitForDialogToClosed } from '../helpers';

   await page.click('[data-test="RF006-dialog-cancelar"]');
   await waitForDialogToClosed(page);  // ✅ Aguarda backdrop desaparecer
   await page.click('[data-test="RF006-criar-cliente"]');
   ```

4. **Executar validação manual (Developer Console):**
   ```javascript
   // Durante teste manual, verificar:
   document.querySelectorAll('.cdk-overlay-backdrop').length
   // Esperado: 0 (nenhum backdrop após fechar dialog)
   // Se > 0: backdrop preso (REPROVADO)
   ```

**Critério de aprovação:**
- ✅ TODAS as operações assíncronas com dialog usam `await firstValueFrom(dialogRef.afterClosed())`
- ✅ TODOS os testes E2E com dialog usam `waitForDialogToClosed(page)`
- ✅ Validação manual: 0 backdrops após fechar dialogs
- ✅ Código possui comentários documentando padrão de cleanup
- ✅ STATUS.yaml documenta aplicação do padrão
- ❌ Qualquer backdrop persistente = **CRÍTICO** (bloqueante)

**Saída esperada (APROVADO):**
```
✅ VALIDAÇÃO 17: APROVADO
   Material Dialog Backdrop Cleanup: PASS
   Operações assíncronas com dialog: 5
   Operações com cleanup correto: 5
   Taxa de conformidade: 100%

   Detalhes:
     ✓ consultarCNPJ(): usa firstValueFrom(afterClosed())
     ✓ confirmarExclusao(): usa firstValueFrom(afterClosed())
     ✓ salvarCliente(): usa firstValueFrom(afterClosed())
     ✓ editarCliente(): usa firstValueFrom(afterClosed())
     ✓ cancelarEdicao(): usa firstValueFrom(afterClosed())

   Testes E2E com dialog: 8
   Testes usando waitForDialogToClosed(): 8
   Taxa de cobertura E2E: 100%

   Validação manual (Developer Console):
     ✓ Backdrop count após operações: 0
     ✓ Usuário pode interagir imediatamente
     ✓ Múltiplos dialogs funcionam corretamente

   STATUS.yaml documentado: ✓
   Comentários de padrão no código: ✓
```

**Saída esperada (REPROVADO):**
```
❌ VALIDAÇÃO 17: REPROVADO
   Material Dialog Backdrop Cleanup: FAIL
   Operações assíncronas com dialog: 5
   Operações com cleanup correto: 2
   Taxa de conformidade: 40%
   Operações SEM cleanup: 3

   Operações SEM cleanup obrigatório:
     ✗ consultarCNPJ() (linha 145 de cliente-form.component.ts)
       Código atual:
         dialogRef.close();
         // FALTA: await firstValueFrom(dialogRef.afterClosed())

       Código esperado:
         dialogRef.close();
         await firstValueFrom(dialogRef.afterClosed());  // ✅ Adicionar

     ✗ confirmarExclusao() (linha 203 de cliente-list.component.ts)
       Código atual:
         loadingRef.close();
         // FALTA: await firstValueFrom(loadingRef.afterClosed())

       Código esperado:
         loadingRef.close();
         await firstValueFrom(loadingRef.afterClosed());  // ✅ Adicionar

     ✗ editarCliente() (linha 178 de cliente-form.component.ts)
       Código atual:
         editRef.close();
         // FALTA: await firstValueFrom(editRef.afterClosed())

       Código esperado:
         editRef.close();
         await firstValueFrom(editRef.afterClosed());  // ✅ Adicionar

   Testes E2E sem helpers:
     ✗ TC-E2E-006: Criar registro (linha 78 de cliente.e2e-spec.ts)
       Código atual:
         await page.click('[data-test="RF006-dialog-cancelar"]');
         await page.click('[data-test="RF006-criar-cliente"]');  // ⚠️ Falha: backdrop intercepta

       Código esperado:
         await page.click('[data-test="RF006-dialog-cancelar"]');
         await waitForDialogToClosed(page);  // ✅ Adicionar
         await page.click('[data-test="RF006-criar-cliente"]');

   Validação manual (Developer Console):
     ✗ Backdrop count após operações: 2 (esperado: 0)
     ✗ Usuário NÃO pode interagir (backdrop intercepta cliques)

   Severidade: CRÍTICO (bloqueante)
   Ação: Aplicar padrão de cleanup em TODAS as operações e re-validar
   Referência: frontend-criacao.md FASE 6.6
```

**Exemplo de correção:**

Antes (REPROVADO):
```typescript
// cliente-form.component.ts
async consultarCNPJ(cnpj: string): Promise<void> {
  const dialogRef = this.dialog.open(LoadingDialogComponent, {
    disableClose: true,
    data: { message: 'Consultando CNPJ...' }
  });

  try {
    const dados = await this.receitaWsService.consultar(cnpj);
    this.form.patchValue(dados);
    dialogRef.close();  // ⚠️ PROBLEMA: Backdrop pode persistir
  } catch (error) {
    dialogRef.close();
    this.showError(error);
  }
}
```

Depois (APROVADO):
```typescript
// cliente-form.component.ts
/**
 * PADRÃO OBRIGATÓRIO: Cleanup de Dialog Backdrop
 * Referência: frontend-criacao.md FASE 6.6
 */
async consultarCNPJ(cnpj: string): Promise<void> {
  const dialogRef = this.dialog.open(LoadingDialogComponent, {
    disableClose: true,
    data: { message: 'Consultando CNPJ...' }
  });

  try {
    const dados = await this.receitaWsService.consultar(cnpj);
    this.form.patchValue(dados);

    dialogRef.close();
    await firstValueFrom(dialogRef.afterClosed());  // ✅ Cleanup obrigatório
  } catch (error) {
    dialogRef.close();
    await firstValueFrom(dialogRef.afterClosed());  // ✅ Cleanup mesmo em erro

    this.showError(error);
  }
}
```

Testes E2E - Antes (REPROVADO):
```typescript
test('TC-E2E: Criar Cliente com Consulta CNPJ', async ({ page }) => {
  await page.click('[data-test="RF006-criar-cliente"]');
  await page.fill('[data-test="RF006-input-cnpj"]', '00.000.000/0001-91');
  await page.click('[data-test="RF006-btn-consultar-cnpj"]');

  // ⚠️ PROBLEMA: Não aguarda backdrop desaparecer
  await page.fill('[data-test="RF006-input-razaosocial"]', 'EMPRESA TESTE');
  // ✗ FALHA: Backdrop intercepta preenchimento
});
```

Testes E2E - Depois (APROVADO):
```typescript
import { waitForDialogToClosed } from '../helpers';

test('TC-E2E: Criar Cliente com Consulta CNPJ', async ({ page }) => {
  await page.click('[data-test="RF006-criar-cliente"]');
  await page.fill('[data-test="RF006-input-cnpj"]', '00.000.000/0001-91');
  await page.click('[data-test="RF006-btn-consultar-cnpj"]');

  await waitForDialogToClosed(page);  // ✅ Aguarda backdrop desaparecer

  await page.fill('[data-test="RF006-input-razaosocial"]', 'EMPRESA TESTE');
  // ✓ SUCESSO: Campo preenchido normalmente
});
```

**Justificativa:**
- **Gap identificado no RF006:** Backdrop persistente → 3/18 testes E2E falharam (17%)
- **Impacto:** Usuário não consegue interagir com UI após dialog fechar
- **Solução:** Validação obrigatória de cleanup ANTES de aprovar frontend
- **Resultado esperado:** Zero falhas por backdrop persistente

**Responsabilidade:**
- **Criação:** Contrato frontend-criacao.md FASE 6.6 (obriga implementação de cleanup)
- **Validação:** Este contrato (valida cleanup antes de aprovar)
- **Helper:** `e2e/helpers/dialog-helpers.ts` (funções auxiliares para E2E)

**Integração com EXECUTION-MANIFEST:**
- Resultado da validação DEVE ser registrado no manifesto
- Incluir operações identificadas e taxa de conformidade
- Anexar validação manual (backdrop count)

**Referências:**
- Helper implementado: `D:\IC2\frontend\icontrolit-app\e2e\helpers\dialog-helpers.ts`
- Contrato stateful: `D:\IC2_Governanca\governanca\contracts\testes\CONTRATO-TESTES-E2E-STATEFUL.md`
- Problema identificado: RF006 execução #7-#9 (17% de falhas)

---

### VALIDAÇÃO 18: Validators Angular Obrigatórios ✨ NOVO BLOQUEANTE

**Objetivo:** Garantir que TODOS os formulários implementem validators Angular obrigatórios, mat-error messages, e comportamento de validação conforme UC.

**Contexto:**
Esta validação foi adicionada após a análise de problemas identificados no RF006, onde validators ausentes resultaram em:
- 3/14 testes E2E falharam por validators ausentes (21% de falhas)
- mat-error não aparecia para usuário (FA-UC01-001)
- Botões não desabilitavam em form.invalid (FA-UC01-002)
- Campos sem validação email (FA-UC01-003)

**Pré-requisito:**
- Frontend implementado conforme FASE 6.7 do contrato frontend-criacao.md
- UC-RFXXX.yaml possui seção `formulario.campos` completa

**Método:**

1. **Ler UC-RFXXX.yaml e mapear campos:**
   ```yaml
   # Exemplo UC-RF006.yaml
   formulario:
     campos:
       - nome: "cnpj"
         obrigatorio: true
         validacoes:
           - tipo: "required"
             mensagem_erro: "CNPJ é obrigatório"
           - tipo: "pattern"
             regex: "^\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}$"
             mensagem_erro: "CNPJ inválido"
   ```

2. **Validar implementação de Validators Angular:**
   ```typescript
   // ✅ PADRÃO CORRETO ESPERADO:
   this.form = this.fb.group({
     cnpj: ['', [
       Validators.required,              // ✅ UC: obrigatorio: true
       Validators.pattern(/^\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}$/)  // ✅ UC: pattern
     ]],
     razaoSocial: ['', [
       Validators.required,              // ✅ UC: obrigatorio: true
       Validators.maxLength(200)         // ✅ UC: maxlength: 200
     ]],
     email: ['', Validators.email]       // ✅ UC: tipo: email
   });
   ```

3. **Validar implementação de mat-error:**
   ```html
   <!-- ✅ PADRÃO CORRETO ESPERADO: -->
   <mat-form-field>
     <input matInput formControlName="cnpj" [data-test]="RF006-input-cnpj">

     <mat-error *ngIf="form.get('cnpj')?.hasError('required')"
                [data-test]="RF006-input-cnpj-error-required">
       CNPJ é obrigatório
     </mat-error>

     <mat-error *ngIf="form.get('cnpj')?.hasError('pattern')"
                [data-test]="RF006-input-cnpj-error-pattern">
       CNPJ inválido
     </mat-error>
   </mat-form-field>
   ```

4. **Validar botões disabled em form.invalid:**
   ```html
   <!-- ✅ PADRÃO CORRETO ESPERADO: -->
   <button mat-raised-button
           [disabled]="form.invalid"
           [data-test]="RF006-salvar-cliente"
           (click)="salvar()">
     Salvar
   </button>
   ```

5. **Executar validação manual (comportamento):**
   - Abrir formulário vazio → Botão Salvar DESABILITADO
   - Clicar em campo obrigatório e sair → mat-error APARECE
   - Preencher com valor inválido → mat-error específico APARECE
   - Preencher com valor válido → mat-error DESAPARECE, Botão HABILITA

**Critério de aprovação:**
- ✅ TODOS os campos com `obrigatorio: true` possuem `Validators.required`
- ✅ TODOS os campos com `validacoes` possuem validators correspondentes
- ✅ TODOS os validators possuem mat-error correspondente
- ✅ TODAS as mensagens mat-error batem com UC-RFXXX.yaml
- ✅ TODOS os mat-error possuem data-test no formato `RFXXX-input-[campo]-error-[tipo]`
- ✅ TODOS os botões de ação possuem `[disabled]="form.invalid"`
- ✅ Validação manual: comportamento correto
- ❌ Qualquer validator/mat-error ausente = **CRÍTICO** (bloqueante)

**Saída esperada (APROVADO):**
```
✅ VALIDAÇÃO 18: APROVADO
   Validators Angular Obrigatórios: PASS
   Campos do UC: 8
   Campos com validators completos: 8
   Taxa de cobertura validators: 100%

   Detalhes de validators:
     ✓ cnpj: required, pattern (2/2)
     ✓ razaoSocial: required, maxLength (2/2)
     ✓ nomeFantasia: required (1/1)
     ✓ email: email (1/1)
     ✓ telefone: pattern (1/1)
     ✓ cep: pattern (1/1)
     ✓ numero: required (1/1)
     ✓ complemento: - (0/0 - opcional sem validação)

   mat-error messages:
     ✓ TODOS os validators possuem mat-error
     ✓ TODAS as mensagens batem com UC-RFXXX.yaml
     ✓ TODOS os mat-error possuem data-test

   Botões disabled:
     ✓ btn-salvar: [disabled]="form.invalid"
     ✓ btn-confirmar: [disabled]="form.invalid"

   Validação manual (comportamento):
     ✓ Formulário vazio: botão desabilitado
     ✓ Campo obrigatório vazio: mat-error aparece
     ✓ Campo inválido: mat-error específico aparece
     ✓ Campo válido: mat-error desaparece, botão habilita

   STATUS.yaml documentado: ✓
```

**Saída esperada (REPROVADO):**
```
❌ VALIDAÇÃO 18: REPROVADO
   Validators Angular Obrigatórios: FAIL
   Campos do UC: 8
   Campos com validators completos: 5
   Taxa de cobertura validators: 62.5%
   Campos SEM validators: 3

   Campos SEM validators obrigatórios:
     ✗ email (linha 85 de cliente-form.component.ts)
       UC especifica: validacoes.tipo: "email"
       Código atual:
         email: ['']  // ⚠️ FALTA: Validators.email
       Código esperado:
         email: ['', Validators.email]  // ✅ Adicionar

     ✗ telefone (linha 86 de cliente-form.component.ts)
       UC especifica: validacoes.tipo: "pattern"
       Código atual:
         telefone: ['']  // ⚠️ FALTA: Validators.pattern
       Código esperado:
         telefone: ['', Validators.pattern(/^\(\d{2}\) \d{4,5}-\d{4}$/)]

     ✗ cep (linha 87 de cliente-form.component.ts)
       UC especifica: obrigatorio: true
       Código atual:
         cep: ['']  // ⚠️ FALTA: Validators.required
       Código esperado:
         cep: ['', Validators.required]

   mat-error messages ausentes:
     ✗ cnpj: FALTA mat-error para 'pattern' (cliente-form.component.html linha 45)
     ✗ razaoSocial: FALTA mat-error para 'maxlength' (cliente-form.component.html linha 52)
     ✗ email: FALTA mat-error para 'email' (cliente-form.component.html linha 59)

   Botões SEM disabled:
     ✗ btn-salvar: FALTA [disabled]="form.invalid" (cliente-form.component.html linha 120)

   Validação manual (comportamento):
     ✗ Formulário vazio: botão NÃO desabilita (esperado: desabilitado)
     ✗ Campo email inválido: mat-error NÃO aparece (esperado: "E-mail inválido")
     ✗ Campo CNPJ inválido: mat-error NÃO aparece (esperado: "CNPJ inválido")

   Severidade: CRÍTICO (bloqueante)
   Ação: Implementar validators/mat-error ausentes conforme FASE 6.7 e re-validar
   Referência: frontend-criacao.md FASE 6.7
```

**Exemplo de correção:**

1. **Adicionar validators ausentes:**
   ```typescript
   // ANTES (INCORRETO):
   this.form = this.fb.group({
     email: ['']  // ❌ Sem validação
   });

   // DEPOIS (CORRETO):
   this.form = this.fb.group({
     email: ['', Validators.email]  // ✅ Com validação
   });
   ```

2. **Adicionar mat-error ausentes:**
   ```html
   <!-- ANTES (INCORRETO): -->
   <mat-form-field>
     <input matInput formControlName="cnpj">
     <!-- ❌ Sem mat-error -->
   </mat-form-field>

   <!-- DEPOIS (CORRETO): -->
   <mat-form-field>
     <input matInput formControlName="cnpj" [data-test]="RF006-input-cnpj">

     <mat-error *ngIf="form.get('cnpj')?.hasError('required')"
                [data-test]="RF006-input-cnpj-error-required">
       CNPJ é obrigatório
     </mat-error>

     <mat-error *ngIf="form.get('cnpj')?.hasError('pattern')"
                [data-test]="RF006-input-cnpj-error-pattern">
       CNPJ inválido
     </mat-error>
   </mat-form-field>
   ```

3. **Adicionar disabled em botões:**
   ```html
   <!-- ANTES (INCORRETO): -->
   <button (click)="salvar()">Salvar</button>  <!-- ❌ Sem disabled -->

   <!-- DEPOIS (CORRETO): -->
   <button [disabled]="form.invalid"
           [data-test]="RF006-salvar-cliente"
           (click)="salvar()">
     Salvar
   </button>
   ```

**Documentação no manifesto:**
- Resultado da validação DEVE ser registrado no manifesto
- Incluir campos identificados, validators implementados, mat-error presentes
- Taxa de cobertura de validators (% campos com validators completos)

**Referências:**
- Relatório de testes: `D:\IC2\.temp_ia\RELATORIO-TESTES-RF006-2026-01-11.md` (GAP 1)
- UC Template: `D:\IC2_Governanca\governanca\templates\UC-TEMPLATE.yaml` (seção formulario.campos)
- Testes falhados: FA-UC01-001, FA-UC01-002, FA-UC01-003
- Contrato criação: `frontend-criacao.md` FASE 6.7

---

## TODO LIST OBRIGATORIA (LER PRIMEIRO)

> **ATENCAO:** O agente DEVE criar esta todo list IMEDIATAMENTE apos ativar o contrato.
> **NENHUMA ACAO** pode ser executada antes da todo list existir.
> **COPIAR EXATAMENTE** o template abaixo, substituindo RFXXX pelo RF real.

### Template para RF Unico (RFXXX)

```
TODO LIST - Validacao Frontend RFXXX
====================================

[pending] Validacao Inicial (ANTES de qualquer validacao)
  |-- [pending] cd backend/IControlIT.API && dotnet build
  |-- [pending] cd frontend/icontrolit-app && npm run build
  |-- [pending] Se QUALQUER build falhar: PARAR e REPORTAR gap critico
  +-- [pending] Somente prosseguir se AMBOS builds passarem


[pending] Analisar documentacao oficial
  |-- [pending] Ler RFXXX.md
  |-- [pending] Ler UC-RFXXX.md (todos os casos de uso)
  |-- [pending] Ler WF-RFXXX.md (wireframes e estados)
  |-- [pending] Identificar todos os fluxos (Principal, FA-XX, FE-XX)
  |-- [pending] Identificar estados obrigatorios (Loading/Vazio/Erro/Dados)
  +-- [pending] Identificar requisitos de responsividade

[pending] Auditar frontend implementado
  |-- [pending] Identificar componentes criados
  |-- [pending] Listar rotas configuradas
  |-- [pending] Validar menu (item existe e navegavel)
  |-- [pending] Verificar i18n (pt-BR, en-US, es-ES)
  |-- [pending] Verificar integracao de diagnosticos
  +-- [pending] Verificar guards de permissao

[pending] Criar Matriz de Cobertura UC
  |-- [pending] Criar coverage.matrix.md
  |-- [pending] Para cada UC (UC00-UC04):
  |     |-- [pending] Fluxo Principal (FP)
  |     |-- [pending] Fluxos Alternativos (FA-XX)
  |     |-- [pending] Fluxos de Excecao (FE-XX)
  |     |-- [pending] Regras de Negocio (RN-UC-XXX)
  |     +-- [pending] Mapear para testes E2E
  +-- [pending] Totalizar cenarios E2E necessarios

[pending] Implementar Testes E2E (Playwright)
  |-- [pending] Criar estrutura tests/e2e/RFXXX/
  |-- [pending] TC-E2E-001: Login + Acesso via menu
  |-- [pending] TC-E2E-002: Carregamento listagem (estado Dados)
  |-- [pending] TC-E2E-003: Estado Loading (spinner visivel)
  |-- [pending] TC-E2E-004: Estado Vazio (mensagem + ilustracao)
  |-- [pending] TC-E2E-005: Estado Erro (mensagem + retry)
  |-- [pending] TC-E2E-006: Criar registro (Fluxo Principal)
  |-- [pending] TC-E2E-007: Editar registro
  |-- [pending] TC-E2E-008: Excluir registro (com confirmacao)
  |-- [pending] TC-E2E-009: Filtros funcionais
  |-- [pending] TC-E2E-010: Paginacao funcional
  |-- [pending] TC-E2E-011: Ordenacao funcional
  |-- [pending] TC-E2E-012: Responsividade (desktop/tablet/mobile)
  |-- [pending] TC-E2E-013: Traducoes (pt-BR/en-US/es-ES)
  |-- [pending] TC-E2E-014: Permissoes (401/403 tratados)
  |-- [pending] Para cada FA-XX do UC:
  |     +-- [pending] TC-E2E-0XX: Testar fluxo alternativo
  |-- [pending] Para cada FE-XX do UC:
  |     +-- [pending] TC-E2E-0XX: Testar fluxo de excecao
  +-- [pending] TC-E2E-FINAL: Criar registro evidencia (NAO excluir)

[pending] Executar Checklist de Conformidade Visual
  |-- [pending] Layout segue padrao aprovado (/management/users)?
  |-- [pending] Componentes Fuse reutilizados corretamente?
  |-- [pending] Estados visuais implementados (Loading/Vazio/Erro)?
  |-- [pending] Responsividade funcional (desktop/tablet/mobile)?
  |-- [pending] Icones e cores consistentes com tema?
  |-- [pending] Spacing e alignment seguem Material Design?
  |-- [pending] Acessibilidade basica (labels, ARIA)?
  +-- [pending] Performance aceitavel (< 3s carregamento)?

[pending] Executar Checklist de Integracao
  |-- [pending] i18n: pt-BR completo?
  |-- [pending] i18n: en-US completo?
  |-- [pending] i18n: es-ES completo?
  |-- [pending] DiagnosticsLogger: eventos logados?
  |-- [pending] Guards: permissoes verificadas?
  |-- [pending] Backend: DTOs alinhados?
  |-- [pending] Backend: Erros estruturados tratados?
  |-- [pending] Seeds: dados minimos disponiveis?
  +-- [pending] Central de Modulos: registrado?

[pending] VALIDACAO 16: Data-test Attributes Completos (BLOQUEANTE)
  |-- [pending] Ler UC-RFXXX.yaml e extrair TODOS os data_test esperados
  |-- [pending] Executar: npm run audit-data-test RFXXX
  |-- [pending] Analisar resultado da auditoria
  |-- [pending] Verificar exit code 0 (PASS) ou 1 (FAIL)
  |-- [pending] Se FAIL: identificar data-test ausentes
  |-- [pending] Se FAIL: identificar inconsistencias de nomenclatura
  |-- [pending] Validar 100% dos data-test do UC presentes no HTML
  +-- [pending] Se < 100%: REPROVAR frontend (BLOQUEIO)

[pending] VALIDACAO 17: Material Dialog Backdrop Cleanup (BLOQUEANTE)
  |-- [pending] Identificar operacoes assincronas com dialog no codigo
  |-- [pending] Validar padrao de cleanup: await firstValueFrom(dialogRef.afterClosed())
  |-- [pending] Validar testes E2E usam: import { waitForDialogToClosed } from '../helpers'
  |-- [pending] Executar validacao manual (Developer Console):
  |     +-- [pending] document.querySelectorAll('.cdk-overlay-backdrop').length === 0
  |-- [pending] Verificar codigo possui comentarios de padrao
  |-- [pending] Verificar STATUS.yaml documenta aplicacao do padrao
  |-- [pending] Taxa de conformidade = 100% (TODAS operacoes com cleanup)
  +-- [pending] Se < 100%: REPROVAR frontend (BLOQUEIO)

[pending] Executar Testes E2E
  |-- [pending] npm run e2e -- RFXXX
  |-- [pending] Coletar evidencias de sucesso
  |-- [pending] Coletar screenshots de estados
  |-- [pending] Identificar falhas (se houver)
  +-- [pending] Registrar taxa de cobertura UC

[pending] Analise de Resultados
  |-- [pending] Se UC coberto 100%: APROVADO
  |-- [pending] Se algum fluxo UC nao coberto: REPROVADO (BLOQUEIO)
  |-- [pending] Se estados obrigatorios ausentes: REPROVADO
  |-- [pending] Se i18n incompleto: REPROVADO
  +-- [pending] Gerar relatorio de conformidade frontend

[pending] Atualizar STATUS.yaml (SE aprovado 100%)
  |-- [pending] validacao.frontend = passed
  |-- [pending] validacao.cobertura_uc = 100%
  |-- [pending] validacao.testes_e2e_executados = XX
  +-- [pending] validacao.data_validacao = YYYY-MM-DD

[pending] Git Operations (SOMENTE SE aprovado 100%)
  |-- [pending] Verificar se branch feature/RFXXX-frontend existe
  |-- [pending] Se NAO existir: git checkout -b feature/RFXXX-frontend
  |-- [pending] git add .
  |-- [pending] git commit -m "feat(RFXXX): frontend validado 100%"
  |-- [pending] git checkout dev && git pull origin dev
  |-- [pending] git merge feature/RFXXX-frontend
  |-- [pending] git push origin dev
  +-- [pending] git branch -d feature/RFXXX-frontend

[pending] Sincronizar DevOps (SE aprovado 100%)
  +-- [pending] python tools/devops-sync/sync-rf.py RFXXX

[pending] Verificar resultado final
  +-- [pending] Board atualizado com status de validacao frontend
```

---

## ESCOPO PERMITIDO

O agente PODE:

- Ler codigo frontend implementado
- Analisar documentacao funcional (RF, UC, WF)
- Criar matriz de cobertura UC
- Implementar testes E2E Playwright
- Executar testes
- Validar conformidade visual (manual)
- Validar integracao (i18n, diagnosticos, permissoes)
- Coletar evidencias (screenshots, logs)
- Atualizar STATUS.yaml
- **BLOQUEAR merges** se cobertura UC < 100% ou estados obrigatorios ausentes

---

## ESCOPO PROIBIDO (ABSOLUTO)

E **EXPRESSAMENTE PROIBIDO**:

- Alterar codigo de producao (frontend)
- Corrigir bugs encontrados
- Criar seeds ou permissoes
- Ajustar codigo para "fazer testes passarem"
- Simplificar ou remover testes E2E
- Assumir comportamento implicito
- Inventar regras nao documentadas

**Gaps devem ser reportados, NAO corrigidos.**

---

## TRATAMENTO DE ERROS EXTERNOS (OBRIGATORIO)

### Cenario: Build Quebrado FORA do Escopo do RF

Se durante a validacao o agente encontrar erros de compilacao, testes falhando ou problemas **EXTERNOS ao RF sendo validado**, o agente DEVE:

#### 1. REPROVAR o RF Imediatamente

Nao e possivel validar um RF em ambiente quebrado.

**Status:** ❌ REPROVADO

#### 2. DOCUMENTAR os Erros Externos

Criar arquivo:

**Localizacao:** `D:\IC2\.temp_ia\RELATORIO-ERROS-EXTERNOS-RFXXX.md`

**Template obrigatorio:**

```markdown
# RELATORIO DE VALIDACAO - RFXXX

**Status:** ❌ REPROVADO

**Motivo:** Ambiente quebrado com erros EXTERNOS ao RFXXX

**Data:** YYYY-MM-DD HH:MM

**Validador:** Agente de Validacao Frontend

---

## ⚠️ DISTINCAO CRITICA: RFXXX vs ERROS EXTERNOS

### ✅ Erros do RFXXX (escopo do agente de execucao)

**Status:** <✅ Sem erros / ❌ Com erros>

**Erros encontrados no RFXXX:**
- <Listar erros especificos do RFXXX, se houver>
- <Se nao houver: "✅ Nenhum erro encontrado no RFXXX - codigo aprovado">

**Acao:**
- Se houver erros: "❌ Agente de execucao deve corrigir antes de re-validar"
- Se nao: "✅ RFXXX sera aprovado assim que ambiente externo for corrigido"

---

### ❌ ERROS EXTERNOS (fora do escopo do RFXXX)

**IMPORTANTE:** Os erros abaixo NAO pertencem ao RFXXX e DEVEM ser corrigidos ANTES.

#### Erro Externo #1: <Nome do modulo>

**Modulo:** `<Caminho/componente ou namespace>`

**RF responsavel:** <RFYYY>
- Identificado por: <git blame / analise de commits / STATUS.yaml / estrutura de pastas>
- Se nao identificado: "⚠️ RF NAO identificado - verificar `git log` manualmente"

**Tipo de erro:** <Build Frontend / Build Backend / Testes E2E / Runtime / Compilacao TypeScript>

**Erros completos:**

\```typescript
<Cole TODOS os erros aqui>
Exemplo:
Error: NG8001: 'app-categoria-list' is not a known element
  at src/app/modules/categorias/list/list.component.ts:12
Error: TS2304: Cannot find name 'Categoria'
  at src/app/core/models/categoria.model.ts:5
\```

**Arquivos afetados:**
- `D:\IC2\frontend\icontrolit-app/src/app/modules/categorias/list/list.component.ts:12`
- `D:\IC2\frontend\icontrolit-app/src/app/core/models/categoria.model.ts:5`

**Impacto:** Impossivel validar RFXXX em ambiente quebrado

---

## 🔧 PROMPT PRONTO PARA CORRECAO (COPIAR E COLAR)

**⚠️ COPIE O BLOCO ABAIXO E EXECUTE EM UM NOVO AGENTE:**

\```
Conforme CONTRATO-MANUTENCAO-CORRECAO-CONTROLADA,
corrija os seguintes erros no modulo <Nome do modulo>:

ERROS IDENTIFICADOS:
<Cole os erros completos aqui com numeros de linha>

CONTEXTO:
- RF afetado: <RFYYY>
- Modulo: <Nome>
- Tipo de erro: <Build Frontend/Backend/E2E/Runtime>
- Relatorio completo: D:\IC2\.temp_ia\RELATORIO-ERROS-EXTERNOS-RFXXX.md

ARQUIVOS COM ERRO:
- <arquivo1.ts:linha>
- <arquivo2.component.ts:linha>

CRITERIO DE PRONTO:
- `npm run build` deve passar 100% (frontend)
- `dotnet build` deve passar 100% (backend, se aplicavel)
- Nenhum novo erro introduzido
- Funcionalidade original deve continuar funcionando
- RFXXX podera ser validado apos correcao
\```

---

## 📊 RESUMO EXECUTIVO

| Item | Status |
|------|--------|
| **RFXXX (codigo proprio)** | <✅ Sem erros / ❌ Com erros> |
| **Ambiente externo** | ❌ QUEBRADO |
| **Erros externos identificados** | <Numero> |
| **RFs externos afetados** | <RFYYY, RFZZZ> |
| **Validacao do RFXXX** | ⏸️ BLOQUEADA ate correcao externa |

---

## 📋 PROXIMOS PASSOS (ORDEM OBRIGATORIA)

1. ✅ **PARAR** validacao do RFXXX
2. ✅ **COPIAR** o prompt de correcao acima
3. ✅ **COLAR** em novo agente (com contrato de manutencao)
4. ✅ **AGUARDAR** correcao dos erros externos
5. ✅ **VALIDAR** que builds passaram (frontend + backend)
6. ✅ **RE-VALIDAR** RFXXX apos ambiente corrigido
7. ❌ **NAO** prosseguir enquanto ambiente quebrado

---

## 🔍 DETALHES DA IDENTIFICACAO DO RF

**Metodo de identificacao:**
- [ ] `git blame` nos arquivos com erro
- [ ] Analise de commits recentes (`git log`)
- [ ] Padrao de nomenclatura de branch (`feature/RFYYY-*`)
- [ ] STATUS.yaml do RF externo
- [ ] Estrutura de pastas/modulos
- [ ] Comentarios no codigo
- [ ] Nao foi possivel identificar

**Evidencia:**
<Explicar como o RF responsavel foi identificado>

Exemplo:
\```bash
$ git blame frontend/.../categoria.model.ts
a1b2c3d4 (RF024-frontend 2026-01-01) export interface Categoria {
\```

---

**IMPORTANTE:**
- Este relatorio foi gerado automaticamente pelo validador
- Todos os erros foram confirmados por builds reais (npm/dotnet)
- O validador NAO corrige erros externos (fora do escopo)
```

#### 3. NAO CORRIGIR os Erros

Erros externos estao **fora do escopo** deste contrato.

O validador **NAO DEVE**:
- Tentar corrigir o codigo de outros RFs
- Modificar codigo fora do escopo
- "Adiantar" correcoes

#### 4. NAO FAZER COMMIT

RF reprovado **NAO** deve ser commitado.

#### 5. INFORMAR o Usuario

Declarar explicitamente:

> "❌ RFXXX REPROVADO: Ambiente quebrado com erros externos.
>
> Verifique RELATORIO-ERROS-EXTERNOS-RFXXX.md para detalhes.
>
> Utilize CONTRATO-MANUTENCAO-CORRECAO-CONTROLADA para corrigir os erros do modulo <Nome> antes de validar RFXXX."

### Criterio de Re-Validacao

Somente apos:
- ✅ Erros externos corrigidos
- ✅ Build backend passando 100%
- ✅ Build frontend passando 100%
- ✅ Testes E2E do ambiente passando

O RFXXX pode ser **re-validado**.

---

## ARTEFATOS OBRIGATORIOS

O agente DEVE gerar/manter os seguintes artefatos:

### 1. Matriz de Cobertura UC

**Localizacao:** `tests/e2e/RFXXX/coverage.matrix.md`

**Conteudo obrigatorio:**

Para cada UC, documentar:

| UC | Fluxo | Descricao | Teste E2E | Status |
|----|-------|-----------|-----------|--------|
| UC00 | FP | Listar todos os registros | TC-E2E-002 | PASS |
| UC00 | FA-01 | Filtrar por nome | TC-E2E-009 | PASS |
| UC00 | FE-01 | Erro ao carregar (500) | TC-E2E-005 | PASS |
| UC01 | FP | Criar novo registro | TC-E2E-006 | PASS |
| UC01 | FA-01 | Criar com campos opcionais | TC-E2E-015 | PASS |
| UC01 | FE-01 | Validacao falha (400) | TC-E2E-016 | PASS |

**Totalizar:**
- Total de fluxos UC: XX
- Total de testes E2E: XX
- Cobertura: XX%

**Esta matriz se torna o mapa de validacao funcional.**

### 2. Testes E2E Playwright

**Estrutura obrigatoria:**
```
tests/e2e/RFXXX/
  ├── setup.spec.ts (criar dependencias)
  ├── list.spec.ts (UC00: Listar)
  ├── create.spec.ts (UC01: Criar)
  ├── edit.spec.ts (UC02: Editar)
  ├── delete.spec.ts (UC03: Excluir)
  ├── states.spec.ts (Loading/Vazio/Erro)
  ├── i18n.spec.ts (pt-BR/en-US/es-ES)
  ├── permissions.spec.ts (401/403)
  └── evidence.spec.ts (registro final)
```

**Foco dos testes:**
- Cobrir 100% dos fluxos UC (FP, FA-XX, FE-XX)
- Validar estados obrigatorios
- Validar i18n completo
- Validar tratamento de erros
- Validar responsividade funcional

### 3. Relatorio de Conformidade Visual

**Localizacao:** `.temp_ia/CONFORMIDADE-VISUAL-RFXXX.md`

**Conteudo obrigatorio:**

```markdown
# Conformidade Visual - RFXXX

## Layout Aprovado

- [x] Segue padrao /management/users
- [x] Header com titulo + botao criar
- [x] Tabela com Mat-Table
- [x] Filtros em linha
- [x] Paginacao
- [x] Ordenacao
- [x] Acoes por linha (editar/excluir)

## Estados Visuais

- [x] Loading: Spinner centralizado
- [x] Vazio: Mensagem + ilustracao
- [x] Erro: Mensagem + botao retry
- [x] Dados: Tabela populada

## Componentes Fuse

- [x] FuseCardComponent (usado no header)
- [x] FuseConfirmationService (usado no delete)
- [ ] FuseAlertComponent (nao usado - OPCIONAL)

## Responsividade

- [x] Desktop (>1280px): Tabela completa
- [x] Tablet (768-1280px): Tabela adaptada
- [x] Mobile (<768px): Cards verticais

## Acessibilidade

- [x] Labels em formularios
- [x] ARIA labels em icones
- [ ] Navegacao por teclado (nao testado)

## Performance

- [x] Carregamento inicial < 3s
- [x] Filtros com debounce
- [x] Lazy loading de imagens
```

---

## CHECKLIST DE CONFORMIDADE VISUAL (OBRIGATORIO)

Antes de APROVAR, o agente DEVE validar visualmente:

### Layout Aprovado

- [ ] Segue padrao de paginas aprovadas?
- [ ] Header com titulo + botao criar?
- [ ] Tabela com Mat-Table + Sort + Pagination?
- [ ] Acoes por linha (editar, excluir)?

### Estados Obrigatorios

- [ ] **Loading:** Spinner centralizado durante carregamento?
- [ ] **Vazio:** Mensagem + ilustracao quando sem dados?
- [ ] **Erro:** Mensagem + botao retry quando falha?
- [ ] **Dados:** Tabela populada quando sucesso?

### Componentes Fuse

- [ ] Reutiliza FuseCardComponent?
- [ ] Reutiliza FuseConfirmationService?
- [ ] Reutiliza FuseAlertComponent (se aplicavel)?
- [ ] NAO cria componentes genericos desnecessarios?

### Responsividade

- [ ] Desktop (>1280px): Layout completo funcional?
- [ ] Tablet (768-1280px): Layout adaptado funcional?
- [ ] Mobile (<768px): Layout mobile funcional?

### Acessibilidade

- [ ] Labels em formularios?
- [ ] ARIA labels em icones?
- [ ] Navegacao por teclado funcional?

### Performance

- [ ] Carregamento inicial < 3s?
- [ ] Filtros com debounce?
- [ ] Paginacao nao trava?

**Se qualquer item for NAO:**
➡️ O agente PARA, documenta e abre gap critico.

---

## CHECKLIST DE INTEGRACAO (OBRIGATORIO)

Antes de APROVAR, o agente DEVE validar:

### i18n (Transloco)

- [ ] pt-BR: Todas as chaves registradas?
- [ ] en-US: Todas as chaves registradas?
- [ ] es-ES: Todas as chaves registradas?
- [ ] Console: ZERO warnings de traducao?
- [ ] Fallback: pt-BR → en → es funcional?

### Diagnosticos

- [ ] DiagnosticsLoggerService injetado?
- [ ] Eventos de navegacao logados?
- [ ] Eventos de acao logados (criar/editar/excluir)?
- [ ] Erros logados com contexto?

### Permissoes

- [ ] Guards de permissao configurados?
- [ ] 401 tratado (redirect para login)?
- [ ] 403 tratado (mensagem de acesso negado)?
- [ ] Diretiva HasPermission funcional?

### Backend

- [ ] DTOs alinhados com backend?
- [ ] Erros estruturados tratados?
- [ ] Loading states durante requests?
- [ ] Retry em caso de falha?

### Seeds

- [ ] Dados minimos disponiveis sem reset manual?
- [ ] Dependencias criadas automaticamente?
- [ ] Permissoes associadas ao perfil developer?

### Central de Modulos

- [ ] Funcionalidade registrada?
- [ ] Menu navegavel?
- [ ] Rota protegida por guard?

**Se qualquer item for NAO:**
➡️ O agente PARA, documenta e abre gap critico.

---

## CRITERIO DE BLOQUEIO

O agente **DEVE BLOQUEAR** o merge se:

1. Cobertura UC < 100%
2. Algum estado obrigatorio ausente (Loading/Vazio/Erro)
3. i18n incompleto (faltando pt-BR, en-US ou es-ES)
4. Testes E2E com falhas
5. Layout aprovado nao preservado
6. Permissoes nao configuradas (401/403 nao tratados)
7. Responsividade nao funcional

**Bloqueio e OBRIGATORIO. NAO e negociavel.**

---

## AUTORIDADE FORMAL

O Validador de Frontend e um CONTRATO BLOQUEADOR da cadeia de execucao.

Isso significa que:

- Nenhum contrato posterior pode prosseguir sem sua aprovacao
- Nenhum merge e considerado valido sem sua validacao
- Nenhum status COMPLETED pode ser registrado sem sua assinatura no EXECUTION-MANIFEST

A reprovacao do Validador de Frontend invalida automaticamente:
- A execucao corrente
- O manifesto associado
- Qualquer tentativa de continuidade

---

## INTEGRACAO COM EXECUTION-MANIFEST

Toda execucao do Validador de Frontend DEVE:

1. Registrar resultado no EXECUTION-MANIFEST.md
2. Marcar explicitamente:
   - APROVADO ou REPROVADO
3. Incluir referencia aos artefatos gerados:
   - coverage.matrix.md
   - CONFORMIDADE-VISUAL-RFXXX.md
   - testes E2E executados

Execucoes sem registro no manifesto sao consideradas INVALIDAS.

---

## PROIBICAO DE NEGOCIACAO DE ESCOPO

O Validador de Frontend:

- NAO negocia escopo
- NAO executa tarefas fora do contrato
- NAO aceita solicitacoes implicitas
- NAO faz excecoes
- NAO continua execucao em caso de gap critico

Qualquer solicitacao fora do escopo DEVE ser recusada imediatamente,
com orientacao para ajuste formal do contrato.

---

## CRITERIO DE COBERTURA 100% (OBRIGATORIO)

Este contrato DEVE validar que:

- [ ] **100% dos UCs foram implementados**
- [ ] **100% dos fluxos foram testados** (FP, FA-XX, FE-XX)
- [ ] Frontend funcionalmente completo (nao parcial)
- [ ] Estados obrigatorios presentes (Loading, Vazio, Erro, Dados)
- [ ] i18n completo (todos os idiomas do projeto)

⚠️ **ATENCAO CRITICA:**

**Cobertura UC < 100% = REPROVACAO AUTOMATICA**

**Qualquer ressalva = REPROVACAO**

---

## SAIDA OBRIGATORIA

Ao final da execucao, o agente DEVE entregar:

1. **Matriz de Cobertura UC** (`coverage.matrix.md`) com status PASS/FAIL
2. **Testes E2E Playwright** (executaveis via ferramenta de teste E2E do projeto)
3. **Relatorio de Conformidade Visual** (`CONFORMIDADE-VISUAL-RFXXX.md`)
4. **Relatorio Final:**
   - Total de fluxos UC: XX
   - Total de testes E2E: XX
   - **Cobertura UC: XX%** (DEVE ser 100%)
   - Estados obrigatorios: OK/FALTANDO
   - i18n completo: OK/FALTANDO
   - Layout aprovado: PRESERVADO/VIOLADO
   - Status final: APROVADO / REPROVADO
5. **STATUS.yaml atualizado**

---

## ATUALIZACAO DO ANTI-ESQUECIMENTO (QUANDO REPROVADO)

Caso o contrato seja **REPROVADO**, o agente DEVE:

1. **Identificar** os erros mais comuns encontrados
2. **Atualizar** o arquivo de anti-esquecimento de frontend do projeto
3. **Adicionar** observacoes genericas (nao muito especificas)
4. **Verificar** se a observacao ja existe antes de incluir
5. **Seguir** o padrao que ja esta no documento

### Regras de Atualizacao

- Observacoes devem ser genericas e reutilizaveis
- Nao duplicar observacoes existentes
- Seguir numeracao e formato do documento
- Focar em "esquecimentos" comuns, nao casos especificos

### Exemplo de Observacao

```markdown
## #XX: Estados Visuais Obrigatorios

**Esquecimento comum:** Implementar telas sem estados de Loading, Vazio ou Erro.

**Como evitar:** Sempre implementar os 4 estados visuais obrigatorios: Loading (spinner), Vazio (mensagem + ilustracao), Erro (mensagem + retry), Dados (conteudo).
```

Desta forma, quando um contrato e reprovado, alimentamos a base de conhecimento para evitar repeticao de erros.

---

## CRITERIO DE AMBIGUIDADE

Se durante a analise, o agente identificar que o UC ou WF e **ambiguo**:

1. **PARAR** imediatamente
2. **DOCUMENTAR** a ambiguidade encontrada
3. **PROPOR** ajuste no UC ou WF oficial
4. **NAO INVENTAR** comportamento esperado

**Ambiguidade bloqueia validacao.**

---

## AUTORIDADE DO AGENTE

Este agente tem **AUTORIDADE PARA BLOQUEAR MERGES**.

Se gaps criticos forem encontrados:
➡️ O merge para `dev` **NAO PODE** ser realizado.
➡️ O RF **NAO PODE** avançar.
➡️ CONTRATO DE MANUTENCAO ou CONTRATO DE ADEQUACAO deve ser ativado para correcao.

**Este contrato e a ultima linha de defesa da qualidade do frontend.**

---

## REGRA FINAL

**Frontend que passa build mas nao cobre 100% do UC e considerado frontend invalido.**

**Nenhum teste E2E pode ser simplificado sem justificativa.**

**Testes devem cobrir todos os fluxos UC (FP, FA-XX, FE-XX).**

**Estados obrigatorios sao INEGOCIAVEIS (Loading/Vazio/Erro).**

**i18n incompleto e GAP CRITICO.**

**Layout aprovado deve ser PRESERVADO.**

**Qualquer gap critico bloqueia aprovacao.**

---

**Este contrato e vinculante.**
**Gaps devem ser reportados, NAO corrigidos.**
**O agente Validador de Frontend tem autoridade para bloquear merges.**

---

## REGRA DE NEGACAO ZERO

Se uma solicitacao:
- nao estiver explicitamente prevista no contrato ativo, ou
- conflitar com qualquer regra do contrato

ENTAO:

- A execucao DEVE ser NEGADA
- Nenhuma acao parcial pode ser realizada
- Nenhum "adiantamento" e permitido
