# PROCESSO DE SINCRONIZAÇÃO MT ↔ SEEDS

**Versão:** 1.0
**Data:** 2026-01-09
**Responsável:** Agente de Documentação / Agente de Testes
**Aplicável a:** Criação e manutenção de Massa de Teste (MT)

---

## 1. OBJETIVO

Garantir que massa de teste (MT) esteja **sempre sincronizada** com:
- Seeds do backend (credenciais, dados iniciais)
- Routing do frontend (URLs de navegação)
- UC (data-test attributes, timeouts)

**Problema que resolve:**
- RF006 Problema 1/6: 100% de falhas E2E por credenciais erradas
- RF006 Problema 2/6: 32 falhas E2E por URLs 404
- RF006 Problema 3/6: 32 falhas E2E por seletores não encontrados
- RF006 Problema 5/6: 15 falhas E2E por timeout insuficiente

---

## 2. FREQUÊNCIA DE EXECUÇÃO

### Obrigatório

- **ANTES de criar MT pela primeira vez**
  - Após UC/TC validados
  - Antes de criar MT-RFXXX.data.ts

- **ANTES de executar testes E2E**
  - Checklist pré-execução de testes
  - Validação automática obrigatória

### Recomendado

- **Sempre que seeds forem atualizados**
  - Backend: ApplicationDbContextInitialiser.cs modificado
  - Executar sincronização imediatamente

- **Sempre que routing for alterado**
  - Frontend: *-routing.module.ts modificado
  - Executar sincronização imediatamente

- **Sempre que UC for atualizado**
  - UC-RFXXX.yaml modificado (data-test, timeouts)
  - Executar sincronização imediatamente

---

## 3. PROCESSO COMPLETO (4 ETAPAS)

### ETAPA 1: Sincronizar Credenciais (MT ↔ Backend Seeds)

**Objetivo:** Garantir que credenciais de teste batem com seeds do backend

#### Passo 1.1: Ler Seeds do Backend

**Arquivo:** `backend/Infrastructure/Persistence/ApplicationDbContextInitialiser.cs`

**Localizar:**
- Seção de seeds de usuários (geralmente linhas 150-250)
- Usuário de teste (perfil: Admin, Developer, ou Usuario)

**Exemplo:**
```csharp
// ApplicationDbContextInitialiser.cs (linhas 180-190)
var adminUser = new ApplicationUser
{
    UserName = "admin@localhost",
    Email = "admin@localhost",
    EmailConfirmed = true
};

await _userManager.CreateAsync(adminUser, "Administrator1!");
```

**Extrair:**
- Email: `admin@localhost`
- Password: `Administrator1!`
- Perfil: `Admin` (inferido do nome da variável ou comentário)

---

#### Passo 1.2: Atualizar MT

**Arquivo:** `frontend/icontrolit-app/e2e/data/MT-RFXXX.data.ts`

**Localizar seção:**
```typescript
export const CREDENCIAIS_TESTE = {
  // ...
};
```

**Atualizar:**
```typescript
/**
 * Credenciais de teste
 *
 * FONTE: ApplicationDbContextInitialiser.cs (linhas 180-190)
 * ÚLTIMA SINCRONIZAÇÃO: 2026-01-09
 * VALIDAÇÃO: Execute `npm run validate-credentials RFXXX` antes de rodar E2E
 */
export const CREDENCIAIS_TESTE = {
  admin_teste: {
    email: 'admin@localhost',           // Backend seed linha 185
    password: 'Administrator1!',         // Backend seed linha 190
    perfil: 'Admin'
  }
};
```

**Campos obrigatórios:**
- `email`: Email exato do seed
- `password`: Senha exata do seed
- `perfil`: Perfil do usuário (Admin, Developer, Usuario)

**Comentários obrigatórios:**
- `FONTE`: Arquivo e linhas do seed
- `ÚLTIMA SINCRONIZAÇÃO`: Data da sincronização
- `VALIDAÇÃO`: Comando para validar sincronização

---

#### Passo 1.3: Validar Sincronização

**Executar:**
```bash
npm run validate-credentials RFXXX
```

**Resultado esperado:**
```
✅ Credenciais sincronizadas
   Email: admin@localhost (MATCH)
   Password: ********** (MATCH)
   Perfil: Admin (MATCH)

Exit code: 0
```

**Se FALHAR:**
```
❌ Credenciais desatualizadas
   Email: admin@localhost (MATCH)
   Password: ********** (DIVERGENTE)
      MT: Administrator1!
      Seed: NewPassword123!
      Linha: 190

Exit code: 1
```

**Ação:**
- Corrigir divergências em MT-RFXXX.data.ts
- Re-executar validação até exit code 0

---

### ETAPA 2: Sincronizar URLs (MT ↔ Frontend Routing)

**Objetivo:** Garantir que URLs de teste batem com rotas configuradas no Angular

#### Passo 2.1: Ler Arquivo Routing

**Arquivo:** Referenciado em UC-RFXXX.yaml → `navegacao.referencia_routing`

**Exemplo:** `src/app/management/management-routing.module.ts`

**Localizar:**
```typescript
const routes: Routes = [
  {
    path: 'management',
    children: [
      {
        path: 'clientes',
        component: ClientesComponent,
        canActivate: [AuthGuard],
        data: { permission: 'CAD.CLIENTES.VISUALIZAR' }
      }
    ]
  }
];
```

**Extrair rota completa:**
- Base: `management`
- Sub-rota: `clientes`
- Rota completa: `management/clientes`

---

#### Passo 2.2: Atualizar MT

**Arquivo:** `frontend/icontrolit-app/e2e/data/MT-RFXXX.data.ts`

**Atualizar:**
```typescript
/**
 * URLs do frontend
 *
 * FONTE: src/app/management/management-routing.module.ts
 * ÚLTIMA SINCRONIZAÇÃO: 2026-01-09
 * VALIDAÇÃO: Execute `npm run validate-routes` antes de rodar E2E
 */
export const FRONTEND_URLS = {
  signIn: 'http://localhost:4200/sign-in',
  clientes: 'http://localhost:4200/management/clientes'  // Rota completa extraída
};
```

**Campos obrigatórios:**
- URL completa: `http://localhost:4200/[rota-completa]`
- Rota deve bater EXATAMENTE com routing

**Comentários obrigatórios:**
- `FONTE`: Arquivo routing
- `ÚLTIMA SINCRONIZAÇÃO`: Data da sincronização
- `VALIDAÇÃO`: Comando para validar sincronização

---

#### Passo 2.3: Validar Sincronização

**Executar:**
```bash
npm run validate-routes
```

**Resultado esperado:**
```
✅ URLs sincronizadas
   signIn: http://localhost:4200/sign-in (MATCH)
   clientes: http://localhost:4200/management/clientes (MATCH)

Exit code: 0
```

**Se FALHAR:**
```
❌ URLs desatualizadas
   signIn: http://localhost:4200/sign-in (MATCH)
   clientes: http://localhost:4200/admin/clientes (DIVERGENTE)
      MT: http://localhost:4200/admin/clientes
      Routing: http://localhost:4200/management/clientes

Exit code: 1
```

**Ação:**
- Corrigir URLs divergentes em MT-RFXXX.data.ts
- Re-executar validação até exit code 0

---

### ETAPA 3: Sincronizar Data-test (MT ↔ UC)

**Objetivo:** Garantir que seletores de teste batem com especificações do UC

#### Passo 3.1: Ler UC-RFXXX.yaml

**Arquivo:** `documentacao/Fase-*/[EPIC]/RFXXX/UC-RFXXX.yaml`

**Extrair TODOS os `data_test`:**

1. **De `passos[].elemento.data_test`:**
   ```yaml
   passos:
     - numero: 3
       acao: "Clicar em 'Novo Cliente'"
       elemento:
         tipo: button
         data_test: "RF006-criar-cliente"
   ```

2. **De `estados_ui`:**
   ```yaml
   estados_ui:
     loading:
       data_test: "loading-spinner"
     vazio:
       data_test: "empty-state"
     erro:
       data_test: "error-message"
   ```

3. **De `tabela` (se aplicável):**
   ```yaml
   tabela:
     data_test_container: "clientes-list"
     data_test_row: "cliente-row"
   ```

4. **De `formulario` (se aplicável):**
   ```yaml
   formulario:
     data_test_form: "RF006-form"
     campos:
       - nome: "Razão Social"
         data_test: "RF006-input-razaosocial"
   ```

---

#### Passo 3.2: Atualizar MT

**Arquivo:** `frontend/icontrolit-app/e2e/data/MT-RFXXX.data.ts`

**Criar seção:**
```typescript
/**
 * Seletores data-test
 *
 * FONTE: UC-RFXXX.yaml (passos, estados_ui, tabela, formulario)
 * ÚLTIMA SINCRONIZAÇÃO: 2026-01-09
 * VALIDAÇÃO: Execute `npm run audit-data-test RFXXX` antes de rodar E2E
 */
export const DATA_TEST_SELECTORS = {
  // Botões de Ação (de passos)
  btnNovoCliente: 'RF006-criar-cliente',
  btnEditarCliente: 'RF006-editar-cliente',
  btnExcluirCliente: 'RF006-excluir-cliente',
  btnSalvar: 'RF006-salvar-cliente',
  btnCancelar: 'RF006-cancelar-cliente',

  // Estados UI
  loadingSpinner: 'loading-spinner',
  emptyState: 'empty-state',
  errorMessage: 'error-message',

  // Tabela
  clientesList: 'clientes-list',
  clienteRow: 'cliente-row',

  // Formulário
  form: 'RF006-form',
  inputRazaoSocial: 'RF006-input-razaosocial',
  inputCNPJ: 'RF006-input-cnpj',

  // Mensagens de Erro
  errorRazaoSocial: 'RF006-input-razaosocial-error',
  errorCNPJ: 'RF006-input-cnpj-error'
};
```

**Regras:**
- Mapear TODOS os data-test do UC para constantes TypeScript
- Nomenclatura: camelCase para constantes, kebab-case para valores
- Organizar por categorias (botões, estados UI, tabela, formulário)

---

#### Passo 3.3: Validar Sincronização

**Executar:**
```bash
npm run audit-data-test RFXXX
```

**Resultado esperado:**
```
✅ Data-test sincronizados
   Total em UC: 15
   Total em MT: 15
   Divergências: 0

Exit code: 0
```

**Se FALHAR:**
```
❌ Data-test desatualizados
   Total em UC: 15
   Total em MT: 12
   Ausentes em MT: 3

   Data-test ausentes:
   - RF006-input-cnpj (UC passo 5)
   - RF006-input-razaosocial-error (UC formulario validações)
   - cliente-row (UC tabela)

Exit code: 1
```

**Ação:**
- Adicionar data-test ausentes em MT-RFXXX.data.ts
- Re-executar validação até exit code 0

---

### ETAPA 4: Sincronizar Timeouts (MT ↔ UC)

**Objetivo:** Garantir que timeouts de teste batem com especificações do UC

#### Passo 4.1: Ler UC-RFXXX.yaml

**Arquivo:** `documentacao/Fase-*/[EPIC]/RFXXX/UC-RFXXX.yaml`

**Extrair seções:**

1. **`performance`:**
   ```yaml
   performance:
     tempo_carregamento_maximo: 30000   # 30s
     tempo_operacao_crud: 10000         # 10s
     timeout_api_externa: 15000         # 15s (se aplicável)
   ```

2. **`timeouts_e2e`:**
   ```yaml
   timeouts_e2e:
     navegacao: 30000
     loading_spinner: 30000
     dialog: 10000
     operacao_crud: 15000
   ```

---

#### Passo 4.2: Atualizar MT

**Arquivo:** `frontend/icontrolit-app/e2e/data/MT-RFXXX.data.ts`

**Criar seção:**
```typescript
/**
 * Timeouts para testes E2E
 *
 * FONTE: UC-RFXXX.yaml (performance, timeouts_e2e)
 * ÚLTIMA SINCRONIZAÇÃO: 2026-01-09
 * VALIDAÇÃO: Execute `python tools/validate-timeouts.py RFXXX` antes de rodar E2E
 */
export const TIMEOUTS = {
  // Valores de UC.timeouts_e2e
  navegacao: 30000,
  loadingSpinner: 30000,
  dialog: 10000,
  operacaoCRUD: 15000,

  // Valores de UC.performance (se aplicável)
  tempoCarregamentoMaximo: 30000,
  tempoOperacaoCRUD: 10000,
  timeoutAPIExterna: 15000
};
```

**Regras:**
- Copiar valores EXATOS de UC
- Não "ajustar" timeouts (usar valores de UC)

---

#### Passo 4.3: Validar Sincronização

**Executar:**
```bash
python tools/validate-timeouts.py RFXXX
```

**Resultado esperado:**
```
✅ Timeouts sincronizados
   navegacao: 30000 (MATCH)
   loadingSpinner: 30000 (MATCH)
   dialog: 10000 (MATCH)
   operacaoCRUD: 15000 (MATCH)

Exit code: 0
```

**Se FALHAR:**
```
❌ Timeouts divergentes
   navegacao: 30000 (MATCH)
   dialog: 10000 (DIVERGENTE)
      MT: 5000
      UC: 10000

Exit code: 1
```

**Ação:**
- Corrigir timeouts divergentes em MT-RFXXX.data.ts
- Re-executar validação até exit code 0

---

## 4. CHECKLIST DE SINCRONIZAÇÃO COMPLETA

**Marque após executar cada etapa:**

- [ ] **ETAPA 1: Credenciais**
  - [ ] Seeds backend lidos
  - [ ] MT atualizado (email, password, perfil)
  - [ ] Comentários de sincronização adicionados
  - [ ] Validação executada: `npm run validate-credentials RFXXX`
  - [ ] Exit code 0 (PASS)

- [ ] **ETAPA 2: URLs**
  - [ ] Routing frontend lido
  - [ ] MT atualizado (URLs completas)
  - [ ] Comentários de sincronização adicionados
  - [ ] Validação executada: `npm run validate-routes`
  - [ ] Exit code 0 (PASS)

- [ ] **ETAPA 3: Data-test**
  - [ ] UC lido (passos, estados_ui, tabela, formulario)
  - [ ] MT atualizado (todos os seletores)
  - [ ] Comentários de sincronização adicionados
  - [ ] Validação executada: `npm run audit-data-test RFXXX`
  - [ ] Exit code 0 (PASS)

- [ ] **ETAPA 4: Timeouts**
  - [ ] UC lido (performance, timeouts_e2e)
  - [ ] MT atualizado (todos os timeouts)
  - [ ] Comentários de sincronização adicionados
  - [ ] Validação executada: `python tools/validate-timeouts.py RFXXX`
  - [ ] Exit code 0 (PASS - se script existir)

**Critério de Aprovação:**
- ✅ TODAS as 4 etapas executadas
- ✅ TODAS as validações retornaram exit code 0

---

## 5. RESPONSABILIDADES

### Criador de MT (Agente de Documentação)
- Garantir sincronização inicial ao criar MT-RFXXX.data.ts
- Executar TODAS as 4 etapas
- Validar TODAS as sincronizações antes de aprovar MT

### Executor de Testes (Agente de Testes)
- Validar sincronização ANTES de executar testes E2E
- Executar checklist pré-execução de testes
- Reportar divergências se validação FALHAR

### Mantenedor de Backend
- AVISAR quando ApplicationDbContextInitialiser.cs for modificado
- Executar sincronização de credenciais imediatamente

### Mantenedor de Frontend
- AVISAR quando *-routing.module.ts for modificado
- Executar sincronização de URLs imediatamente

### Mantenedor de UC
- AVISAR quando UC-RFXXX.yaml for modificado (data-test, timeouts)
- Executar sincronização de data-test/timeouts imediatamente

---

## 6. FERRAMENTAS DE VALIDAÇÃO

### validate-credentials RFXXX
**Caminho:** `npm run validate-credentials RFXXX`
**Criado em:** Sprint 3 - Task 3
**Objetivo:** Validar credenciais MT vs backend seeds
**Exit codes:**
- 0: Credenciais sincronizadas
- 1: Credenciais desatualizadas

---

### validate-routes
**Caminho:** `npm run validate-routes`
**Criado em:** Sprint 3 - Task 4
**Objetivo:** Validar URLs MT vs frontend routing
**Exit codes:**
- 0: URLs sincronizadas
- 1: URLs desatualizadas (404)

---

### audit-data-test RFXXX
**Caminho:** `npm run audit-data-test RFXXX`
**Criado em:** Sprint 1 (planejado), Sprint 3 (referenciado)
**Objetivo:** Validar data-test MT vs UC
**Exit codes:**
- 0: Data-test sincronizados
- 1: Data-test desatualizados

---

### validate-timeouts RFXXX
**Caminho:** `python tools/validate-timeouts.py RFXXX`
**Criado em:** Sprint 4 (planejado)
**Objetivo:** Validar timeouts MT vs UC
**Exit codes:**
- 0: Timeouts sincronizados
- 1: Timeouts divergentes

---

## 7. FLUXOGRAMA DO PROCESSO

```
┌─────────────────────────────────────┐
│  INÍCIO: Criar/Atualizar MT         │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  ETAPA 1: Sincronizar Credenciais   │
│  - Ler backend seeds                │
│  - Atualizar MT (email, password)   │
│  - Validar: validate-credentials    │
└──────────────┬──────────────────────┘
               │
               ▼
           [PASS?] ──NO──> Corrigir divergências ──┐
               │                                     │
              YES                                    │
               │◄────────────────────────────────────┘
               ▼
┌─────────────────────────────────────┐
│  ETAPA 2: Sincronizar URLs          │
│  - Ler frontend routing             │
│  - Atualizar MT (URLs)              │
│  - Validar: validate-routes         │
└──────────────┬──────────────────────┘
               │
               ▼
           [PASS?] ──NO──> Corrigir URLs ──────────┐
               │                                     │
              YES                                    │
               │◄────────────────────────────────────┘
               ▼
┌─────────────────────────────────────┐
│  ETAPA 3: Sincronizar Data-test     │
│  - Ler UC (passos, estados_ui, etc) │
│  - Atualizar MT (seletores)         │
│  - Validar: audit-data-test         │
└──────────────┬──────────────────────┘
               │
               ▼
           [PASS?] ──NO──> Adicionar seletores ────┐
               │                                     │
              YES                                    │
               │◄────────────────────────────────────┘
               ▼
┌─────────────────────────────────────┐
│  ETAPA 4: Sincronizar Timeouts      │
│  - Ler UC (performance, timeouts)   │
│  - Atualizar MT (timeouts)          │
│  - Validar: validate-timeouts       │
└──────────────┬──────────────────────┘
               │
               ▼
           [PASS?] ──NO──> Corrigir timeouts ──────┐
               │                                     │
              YES                                    │
               │◄────────────────────────────────────┘
               ▼
┌─────────────────────────────────────┐
│  FIM: MT Sincronizado (APROVADO)    │
│  - Executar testes E2E              │
│  - Expectativa: Taxa inicial ≥ 80%  │
└─────────────────────────────────────┘
```

---

## 8. EXEMPLO COMPLETO: MT-RF006.data.ts

```typescript
/**
 * MASSA DE TESTE - RF006: Cadastro de Clientes
 *
 * Este arquivo contém todos os dados necessários para testes E2E do RF006.
 * CRÍTICO: Manter sincronizado com backend seeds, frontend routing e UC.
 */

// =============================================
// CREDENCIAIS (SINCRONIZADAS COM BACKEND)
// =============================================

/**
 * Credenciais de teste
 *
 * FONTE: ApplicationDbContextInitialiser.cs (linhas 180-190)
 * ÚLTIMA SINCRONIZAÇÃO: 2026-01-09
 * VALIDAÇÃO: Execute `npm run validate-credentials RF006` antes de rodar E2E
 */
export const CREDENCIAIS_TESTE = {
  admin_teste: {
    email: 'admin@localhost',
    password: 'Administrator1!',
    perfil: 'Admin'
  }
};

// =============================================
// URLS FRONTEND (SINCRONIZADAS COM ROUTING)
// =============================================

/**
 * URLs do frontend
 *
 * FONTE: src/app/management/management-routing.module.ts
 * ÚLTIMA SINCRONIZAÇÃO: 2026-01-09
 * VALIDAÇÃO: Execute `npm run validate-routes` antes de rodar E2E
 */
export const FRONTEND_URLS = {
  signIn: 'http://localhost:4200/sign-in',
  clientes: 'http://localhost:4200/management/clientes'
};

// =============================================
// SELETORES E2E (SINCRONIZADOS COM UC)
// =============================================

/**
 * Seletores data-test
 *
 * FONTE: UC-RF006.yaml (passos, estados_ui, tabela, formulario)
 * ÚLTIMA SINCRONIZAÇÃO: 2026-01-09
 * VALIDAÇÃO: Execute `npm run audit-data-test RF006` antes de rodar E2E
 */
export const DATA_TEST_SELECTORS = {
  btnNovoCliente: 'RF006-criar-cliente',
  btnSalvar: 'RF006-salvar-cliente',
  btnCancelar: 'RF006-cancelar-cliente',

  loadingSpinner: 'loading-spinner',
  emptyState: 'empty-state',
  errorMessage: 'error-message',

  clientesList: 'clientes-list',
  clienteRow: 'cliente-row',

  form: 'RF006-form',
  inputRazaoSocial: 'RF006-input-razaosocial',
  errorRazaoSocial: 'RF006-input-razaosocial-error'
};

// =============================================
// TIMEOUTS (SINCRONIZADOS COM UC)
// =============================================

/**
 * Timeouts para testes E2E
 *
 * FONTE: UC-RF006.yaml (performance, timeouts_e2e)
 * ÚLTIMA SINCRONIZAÇÃO: 2026-01-09
 */
export const TIMEOUTS = {
  navegacao: 30000,
  loadingSpinner: 30000,
  dialog: 10000,
  operacaoCRUD: 15000
};

// =============================================
// MASSA DE TESTE (DADOS)
// =============================================

export const MT_RF006_CLIENTES = [
  {
    id: 'MT-RF006-001',
    razaoSocial: 'Cliente Teste Ltda',
    cnpj: '12.345.678/0001-90'
  }
];
```

---

## 9. CHANGELOG

### v1.0 (2026-01-09)
- Criação do processo de sincronização MT ↔ Seeds
- 4 etapas de sincronização: Credenciais, URLs, Data-test, Timeouts
- Ferramentas de validação documentadas
- Responsabilidades definidas
- Fluxograma do processo
- Exemplo completo de MT sincronizado

---

**Mantido por:** Time de Arquitetura IControlIT
**Última Atualização:** 2026-01-09
**Versão:** 1.0
