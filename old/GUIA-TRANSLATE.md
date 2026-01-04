# GUIA COMPLETO DE TRADUÇÃO (i18n)

**Versão:** 1.1
**Data:** 2025-01-17
**Baseado em:** Funcionalidade `/management/users` (RF-006)

---

## 🎯 Objetivo

Este guia documenta **TODOS** os pontos que devem ser traduzidos para garantir uma funcionalidade **100% internacionalizada** em português (pt-BR), inglês (en) e espanhol (es).

**Análise baseada em:** Funcionalidade de Gestão de Usuários (`/management/users`)

**Funcionalidade de referência:**
- **Código:** `frontend/icontrolit-app/src/app/modules/admin/management/users/`
- **Traduções:** Busque por `"users"` nos arquivos `public/i18n/*.json`
- **Exemplo completo:** Esta funcionalidade implementa TODOS os pontos deste guia

---

## 📋 CHECKLIST COMPLETO DE TRADUÇÃO

Use este checklist para garantir que NENHUM ponto foi esquecido:

- [ ] **1. Templates HTML** - Todos os textos visíveis (títulos, labels, botões, placeholders)
- [ ] **2. Mensagens TypeScript** - Confirmações, diálogos, tooltips
- [ ] **3. Validações Frontend** - Mensagens de erro de formulário
- [ ] **4. Validações Backend** - Mensagens de erro da API (.NET)
- [ ] **5. Toasts e Notificações** - Mensagens de sucesso/erro
- [ ] **6. Tooltips e Hints** - Ajudas contextuais
- [ ] **7. Badges e Status** - Labels de status, badges visuais
- [ ] **8. Breadcrumbs e Navegação** - Títulos de navegação
- [ ] **9. Tabelas e Grid** - Cabeçalhos de colunas, mensagens "sem dados"
- [ ] **10. Paginação** - Labels do MatPaginator
- [ ] **11. Filtros** - Labels e opções de filtros
- [ ] **12. Diálogos de Confirmação** - Títulos, mensagens, botões
- [ ] **13. Mensagens de Erro HTTP** - Tratamento de erros da API
- [ ] **14. Pluralização** - Textos que mudam com quantidade (1 usuário vs 2 usuários)
- [ ] **15. Interpolação** - Textos com variáveis dinâmicas
- [ ] **16. Componentes do Angular Material** - MatPaginator, MatDatepicker, etc.

---

## 📁 ESTRUTURA DE ARQUIVOS DE TRADUÇÃO

### Localização dos Arquivos

```
frontend/icontrolit-app/public/i18n/
├── pt.json     ← Português (Brasil) - IDIOMA PRINCIPAL
├── en.json     ← Inglês
└── es.json     ← Espanhol
```

### Estrutura Hierárquica no JSON

```json
{
  "users": {
    "title": "...",
    "subtitle": "...",
    "new-user": "...",
    "fields": {
      "email": "...",
      "name": "..."
    },
    "errors": {
      "createError": "...",
      "loadError": "..."
    },
    "tooltips": {
      "blocked": "...",
      "mfa": "..."
    },
    "dialogs": {
      "delete": {
        "title": "...",
        "message": "..."
      }
    }
  }
}
```

**Convenção de nomenclatura:**
- Use **kebab-case** para chaves (ex: `new-user`, `clear-filters`)
- Hierarquia: `modulo.submodulo.chave` (ex: `users.fields.email`)
- Prefixos comuns:
  - `field-*` - Campos de formulário
  - `error-*` - Mensagens de erro
  - `button-*` - Botões
  - `tooltip-*` - Tooltips
  - `badge-*` - Badges
  - `action-*` - Ações de menu
  - `dialog-*` - Elementos de diálogo

---

## 1️⃣ TEMPLATES HTML - TRADUÇÃO COMPLETA

### 1.1. Títulos e Subtítulos

**Onde:** Cabeçalhos de página, seções

```html
<!-- ❌ ERRADO (texto hardcoded) -->
<h2 class="text-3xl font-semibold">Usuários</h2>
<div class="text-secondary">Gerencie os usuários do sistema</div>

<!-- ✅ CORRETO (com pipe transloco) -->
<h2 class="text-3xl font-semibold">{{ 'users.title' | transloco }}</h2>
<div class="text-secondary">{{ 'users.subtitle' | transloco }}</div>
```

**Arquivo i18n:**
```json
{
  "users": {
    "title": "Usuários",
    "subtitle": "Gerencie os usuários do sistema"
  }
}
```

---

### 1.2. Botões e Ações

**Onde:** Botões de ação, botões de formulário

```html
<!-- ❌ ERRADO -->
<button mat-flat-button>Novo Usuário</button>
<button mat-stroked-button>Cancelar</button>
<button mat-flat-button>Salvar</button>

<!-- ✅ CORRETO -->
<button mat-flat-button>{{ 'users.new-user' | transloco }}</button>
<button mat-stroked-button>{{ 'users.button-cancel' | transloco }}</button>
<button mat-flat-button>{{ 'users.button-save' | transloco }}</button>
```

**Arquivo i18n:**
```json
{
  "users": {
    "new-user": "Novo Usuário",
    "button-cancel": "Cancelar",
    "button-save": "Salvar",
    "button-edit": "Editar",
    "button-delete": "Excluir"
  }
}
```

---

### 1.3. Labels de Formulário

**Onde:** `<mat-label>`, labels de campos

```html
<!-- ❌ ERRADO -->
<mat-form-field>
  <mat-label>Email</mat-label>
  <input matInput formControlName="email" />
</mat-form-field>

<!-- ✅ CORRETO -->
<mat-form-field>
  <mat-label>{{ 'users.field-email' | transloco }}</mat-label>
  <input matInput formControlName="email" />
</mat-form-field>
```

**Arquivo i18n:**
```json
{
  "users": {
    "field-email": "Email",
    "field-name": "Nome",
    "field-phone": "Telefone",
    "field-cpf": "CPF",
    "field-birth-date": "Data de Nascimento",
    "field-password": "Senha",
    "field-roles": "Perfis de acesso",
    "field-active": "Usuário ativo",
    "field-company": "Empresa"
  }
}
```

---

### 1.4. Mensagens de Validação (Frontend)

**Onde:** `<mat-error>` em formulários

```html
<!-- ❌ ERRADO -->
<mat-error *ngIf="usuarioForm.get('email')?.hasError('required')">
  Email é obrigatório
</mat-error>
<mat-error *ngIf="usuarioForm.get('email')?.hasError('email')">
  Informe um email válido
</mat-error>

<!-- ✅ CORRETO -->
<mat-error *ngIf="usuarioForm.get('email')?.hasError('required')">
  {{ 'users.error-email-required' | transloco }}
</mat-error>
<mat-error *ngIf="usuarioForm.get('email')?.hasError('email')">
  {{ 'users.error-email-invalid' | transloco }}
</mat-error>
```

**Arquivo i18n:**
```json
{
  "users": {
    "error-email-required": "Email é obrigatório",
    "error-email-invalid": "Informe um email válido",
    "error-name-required": "Nome é obrigatório",
    "error-cpf-invalid": "CPF inválido",
    "error-password-required": "Senha é obrigatória",
    "error-password-minlength": "Mínimo de 6 caracteres",
    "error-roles-required": "Selecione pelo menos um perfil",
    "error-company-required": "Empresa é obrigatória"
  }
}
```

---

### 1.5. Placeholders

**Onde:** Inputs, campos de busca

```html
<!-- ❌ ERRADO -->
<input matInput [(ngModel)]="filters.searchTerm" placeholder="Nome, email ou CPF">

<!-- ✅ CORRETO -->
<input matInput [(ngModel)]="filters.searchTerm" [placeholder]="'users.search-placeholder' | transloco">
```

**Arquivo i18n:**
```json
{
  "users": {
    "search-placeholder": "Nome, email ou CPF",
    "placeholder-new-password": "Digite a nova senha"
  }
}
```

---

### 1.6. Tooltips

**Onde:** `[matTooltip]`

```html
<!-- ❌ ERRADO -->
<span matTooltip="Usuário bloqueado">Bloqueado</span>

<!-- ✅ CORRETO -->
<span [matTooltip]="'users.tooltip-blocked' | transloco">
  {{ 'users.badge-blocked' | transloco }}
</span>
```

**Arquivo i18n:**
```json
{
  "users": {
    "tooltip-blocked": "Usuário bloqueado",
    "tooltip-mfa": "Autenticação de dois fatores ativa",
    "tooltip-ad": "Usuário sincronizado com Active Directory",
    "tooltip-password-expired": "Senha expirada - usuário deve alterar no próximo login",
    "tooltip-anonymized": "Dados pessoais removidos (LGPD Art. 18)"
  }
}
```

---

### 1.7. Badges e Status

**Onde:** Chips, badges de status

```html
<!-- ❌ ERRADO -->
<span class="badge">Ativo</span>
<span class="badge">Bloqueado</span>

<!-- ✅ CORRETO -->
<span class="badge">{{ usuario.ativo ? ('users.active' | transloco) : ('users.inactive' | transloco) }}</span>
<span class="badge" *ngIf="usuario.bloqueado">{{ 'users.badge-blocked' | transloco }}</span>
```

**Arquivo i18n:**
```json
{
  "users": {
    "active": "Ativo",
    "inactive": "Inativo",
    "badge-blocked": "Bloqueado",
    "badge-mfa": "MFA",
    "badge-ad": "AD",
    "badge-password-expired": "Senha Expirada",
    "badge-anonymized": "Anonimizado"
  }
}
```

---

### 1.8. Cabeçalhos de Tabela

**Onde:** `<th mat-header-cell>`

```html
<!-- ❌ ERRADO -->
<ng-container matColumnDef="name">
  <th mat-header-cell *matHeaderCellDef>Nome</th>
</ng-container>

<!-- ✅ CORRETO -->
<ng-container matColumnDef="name">
  <th mat-header-cell *matHeaderCellDef>{{ 'users.name' | transloco }}</th>
</ng-container>
```

**Arquivo i18n:**
```json
{
  "users": {
    "name": "Nome",
    "company": "Empresa",
    "phone": "Telefone",
    "roles": "Perfis",
    "status": "Status",
    "actions-column": "Ações"
  }
}
```

---

### 1.9. Pluralização

**Onde:** Contadores, listagens

```html
<!-- ❌ ERRADO (não trata plural) -->
<div>{{usuarios?.length || 0}} usuários cadastrados</div>

<!-- ✅ CORRETO (usa expressão ternária para singular/plural) -->
<div>
  {{usuarios?.length || 0}}
  {{ (usuarios?.length === 1 ? 'users.user-count-singular' : 'users.user-count-plural') | transloco }}
</div>
```

**Arquivo i18n:**
```json
{
  "users": {
    "user-count-singular": "usuário cadastrado",
    "user-count-plural": "usuários cadastrados"
  }
}
```

---

### 1.10. Seções e Agrupamentos

**Onde:** Títulos de seções, divisórias

```html
<!-- ❌ ERRADO -->
<div class="text-md font-medium mb-4">Preferências</div>
<div class="text-md font-medium mb-4">Segurança</div>

<!-- ✅ CORRETO -->
<div class="text-md font-medium mb-4">{{ 'users.section-preferences' | transloco }}</div>
<div class="text-md font-medium mb-4">{{ 'users.section-security' | transloco }}</div>
```

**Arquivo i18n:**
```json
{
  "users": {
    "section-preferences": "Preferências",
    "section-security": "Segurança"
  }
}
```

---

### 1.11. Hints (mat-hint)

**Onde:** Dicas em campos de formulário

```html
<!-- ❌ ERRADO -->
<mat-hint>Mínimo 6 caracteres</mat-hint>
<mat-hint>Selecione uma empresa primeiro</mat-hint>

<!-- ✅ CORRETO -->
<mat-hint>{{ 'users.hint-min-characters' | transloco }}</mat-hint>
<mat-hint>{{ 'users.hint-select-company-first' | transloco }}</mat-hint>
```

**Arquivo i18n:**
```json
{
  "users": {
    "hint-min-characters": "Mínimo 6 caracteres",
    "hint-select-company-first": "Selecione uma empresa primeiro"
  }
}
```

---

### 1.12. Opções de Select/Dropdown

**Onde:** `<mat-option>`, dropdowns

```html
<!-- ❌ ERRADO -->
<mat-select formControlName="idioma">
  <mat-option value="pt-BR">Português (Brasil)</mat-option>
  <mat-option value="en">English</mat-option>
  <mat-option value="es">Español</mat-option>
</mat-select>

<!-- ✅ CORRETO -->
<mat-select formControlName="idioma">
  <mat-option value="pt-BR">{{ 'users.lang-pt-br' | transloco }}</mat-option>
  <mat-option value="en">{{ 'users.lang-en' | transloco }}</mat-option>
  <mat-option value="es">{{ 'users.lang-es' | transloco }}</mat-option>
</mat-select>
```

**Arquivo i18n:**
```json
{
  "users": {
    "lang-pt-br": "Português (Brasil)",
    "lang-en": "English",
    "lang-es": "Español",
    "theme-light": "Claro",
    "theme-dark": "Escuro",
    "theme-auto": "Automático",
    "timezone-sao-paulo": "São Paulo (GMT-3)",
    "timezone-new-york": "Nova York (GMT-5)",
    "timezone-los-angeles": "Los Angeles (GMT-8)"
  }
}
```

---

### 1.13. Filtros

**Onde:** Labels de filtros, opções

```html
<!-- ❌ ERRADO -->
<mat-form-field>
  <mat-label>Status</mat-label>
  <mat-select [(ngModel)]="filters.ativo">
    <mat-option [value]="null">Todos</mat-option>
    <mat-option [value]="true">Ativo</mat-option>
    <mat-option [value]="false">Inativo</mat-option>
  </mat-select>
</mat-form-field>

<!-- ✅ CORRETO -->
<mat-form-field>
  <mat-label>{{ 'users.status-label' | transloco }}</mat-label>
  <mat-select [(ngModel)]="filters.ativo">
    <mat-option [value]="null">{{ 'users.all' | transloco }}</mat-option>
    <mat-option [value]="true">{{ 'users.active' | transloco }}</mat-option>
    <mat-option [value]="false">{{ 'users.inactive' | transloco }}</mat-option>
  </mat-select>
</mat-form-field>
```

**Arquivo i18n:**
```json
{
  "users": {
    "filters": "Filtros",
    "clear-filters": "Limpar Filtros",
    "status-label": "Status",
    "all": "Todos",
    "blocking-label": "Bloqueio",
    "blocked": "Bloqueados",
    "not-blocked": "Não Bloqueados",
    "mfa-label": "MFA",
    "with-mfa": "Com MFA",
    "without-mfa": "Sem MFA",
    "ad-label": "Active Directory",
    "ad-users": "Usuários AD",
    "local-users": "Usuários Locais",
    "lgpd-label": "LGPD",
    "anonymized": "Anonimizados",
    "not-anonymized": "Não Anonimizados",
    "password-label": "Senha",
    "expired-passwords": "Expiradas",
    "valid-passwords": "Válidas"
  }
}
```

---

### 1.14. Menu de Ações

**Onde:** `<mat-menu>`, menus contextuais

```html
<!-- ❌ ERRADO -->
<mat-menu #userMenu="matMenu">
  <button mat-menu-item (click)="editUsuario(usuario)">Editar</button>
  <button mat-menu-item (click)="deleteUsuario(usuario)">Excluir</button>
</mat-menu>

<!-- ✅ CORRETO -->
<mat-menu #userMenu="matMenu">
  <button mat-menu-item (click)="editUsuario(usuario)">
    <span>{{ 'users.action-edit' | transloco }}</span>
  </button>
  <button mat-menu-item (click)="deleteUsuario(usuario)">
    <span>{{ 'users.action-deactivate' | transloco }}</span>
  </button>
</mat-menu>
```

**Arquivo i18n:**
```json
{
  "users": {
    "action-edit": "Editar",
    "action-reactivate": "Reativar",
    "action-deactivate": "Desativar",
    "action-anonymize": "Anonimizar (LGPD)"
  }
}
```

---

### 1.15. Títulos de Diálogo

**Onde:** `<div mat-dialog-title>`

```html
<!-- ❌ ERRADO (lógica complexa no template) -->
<div mat-dialog-title>
  {{ usuario ? (editMode ? 'Editar usuário' : 'Detalhes do usuário') : 'Novo usuário' }}
</div>

<!-- ✅ CORRETO -->
<div mat-dialog-title>
  {{ usuario ? (editMode ? ('users.dialog-title-edit' | transloco) : ('users.dialog-title-details' | transloco)) : ('users.dialog-title-new' | transloco) }}
</div>
```

**Arquivo i18n:**
```json
{
  "users": {
    "dialog-title-new": "Novo usuário",
    "dialog-title-edit": "Editar usuário",
    "dialog-title-details": "Detalhes do usuário"
  }
}
```

---

## 2️⃣ TYPESCRIPT - TRADUÇÃO PROGRAMÁTICA

### 2.1. Mensagens de Confirmação (FuseConfirmationService)

**Onde:** Diálogos de confirmação no TypeScript

```typescript
// ❌ ERRADO (mensagens hardcoded)
const confirmation = this._fuseConfirmationService.open({
  title: 'Excluir usuário',
  message: `Tem certeza que deseja excluir o usuário <strong>${usuario.nome}</strong>?`,
  actions: {
    confirm: { label: 'Excluir' },
    cancel: { label: 'Cancelar' }
  }
});

// ✅ CORRETO (usando TranslocoService)
const confirmation = this._fuseConfirmationService.open({
  title: this._translocoService.translate('users.dialog-delete-title'),
  message: this._translocoService.translate('users.dialog-delete-message', { nome: usuario.nome }),
  actions: {
    confirm: {
      label: this._translocoService.translate('users.button-delete')
    },
    cancel: {
      label: this._translocoService.translate('users.button-cancel')
    }
  }
});
```

**Injeção obrigatória:**
```typescript
import { TranslocoService } from '@jsverse/transloco';

export class UsersListComponent {
  private _translocoService = inject(TranslocoService);
}
```

**Arquivo i18n:**
```json
{
  "users": {
    "dialog-delete-title": "Excluir usuário",
    "dialog-delete-message": "Tem certeza que deseja excluir o usuário <strong>{{nome}}</strong>?",
    "button-delete": "Excluir",
    "button-cancel": "Cancelar"
  }
}
```

---

### 2.2. Interpolação de Variáveis

**Sintaxe:** Use `{{variavel}}` no JSON e passe objeto no `translate()`

```typescript
// ✅ CORRETO
this._translocoService.translate('users.dialog-delete-message', {
  nome: usuario.nome || usuario.email
})

// Mensagem com múltiplas variáveis
this._translocoService.translate('users.confirm-anonymize', {
  nome: usuario.nome,
  email: usuario.email
})
```

**Arquivo i18n:**
```json
{
  "users": {
    "dialog-delete-message": "Tem certeza que deseja excluir o usuário <strong>{{nome}}</strong>?<br><br>Esta ação não pode ser desfeita.",
    "confirm-anonymize": "Anonimizar dados de <strong>{{nome}}</strong> ({{email}})?"
  }
}
```

---

### 2.3. Mensagens de Erro HTTP

**Onde:** Tratamento de erros em `.subscribe()`

```typescript
// ❌ ERRADO
this._usersService.deleteUsuario(request).subscribe({
  error: (error) => {
    this._fuseConfirmationService.open({
      title: 'Erro ao excluir usuário',
      message: error.error?.detail || 'Ocorreu um erro ao excluir o usuário.'
    });
  }
});

// ✅ CORRETO
this._usersService.deleteUsuario(request).subscribe({
  error: (error) => {
    this._fuseConfirmationService.open({
      title: this._translocoService.translate('users.error-delete-title'),
      message: error.error?.detail || this._translocoService.translate('users.error-delete-message')
    });
  }
});
```

**Arquivo i18n:**
```json
{
  "users": {
    "error-delete-title": "Erro ao excluir usuário",
    "error-delete-message": "Ocorreu um erro ao excluir o usuário.",
    "error-update-title": "Erro ao atualizar usuário",
    "error-create-title": "Erro ao criar usuário"
  }
}
```

---

### 2.4. Função Dedicada para Traduções Dinâmicas

**Exemplo:** Força de senha

```typescript
// ✅ CORRETO (método dedicado)
getPasswordStrengthText(): string {
  switch (this.passwordStrength) {
    case "weak":
      return this._translocoService.translate("users.password-strength-weak");
    case "medium":
      return this._translocoService.translate("users.password-strength-medium");
    case "strong":
      return this._translocoService.translate("users.password-strength-strong");
    case "very-strong":
      return this._translocoService.translate("users.password-strength-very-strong");
    default:
      return "";
  }
}
```

**Uso no template:**
```html
<div class="text-xs">{{ getPasswordStrengthText() }}</div>
```

**Arquivo i18n:**
```json
{
  "users": {
    "password-strength-weak": "Fraca - use letras, números e símbolos",
    "password-strength-medium": "Média - adicione mais variedade de caracteres",
    "password-strength-strong": "Forte",
    "password-strength-very-strong": "Muito forte"
  }
}
```

---

### 2.5. Mensagens de Diálogo Complexas (HTML)

**Onde:** Mensagens longas com formatação HTML

```typescript
// ✅ CORRETO (mensagem com HTML e múltiplas linhas)
const confirmation = this._fuseConfirmationService.open({
  title: this._translocoService.translate('users.anonymize-title'),
  message: this._translocoService.translate('users.anonymize-message', {
    nome: usuario.nome || usuario.email
  }),
  icon: {
    show: true,
    name: 'heroicons_outline:exclamation-triangle',
    color: 'warn'
  },
  actions: {
    confirm: {
      show: true,
      label: this._translocoService.translate('users.anonymize-confirm'),
      color: 'warn'
    },
    cancel: {
      show: true,
      label: this._translocoService.translate('users.button-cancel')
    }
  }
});
```

**Arquivo i18n:**
```json
{
  "users": {
    "anonymize-title": "Anonimizar usuário (LGPD)",
    "anonymize-message": "<strong>ATENÇÃO: Esta ação é IRREVERSÍVEL!</strong><br><br>Todos os dados pessoais de <strong>{{nome}}</strong> serão permanentemente removidos conforme LGPD Art. 18.<br><br>Dados que serão removidos:<br>• Nome, Email, CPF, Telefone<br>• Data de Nascimento<br>• Configurações de MFA<br>• Avatar<br><br>O usuário NÃO poderá mais ser reativado após esta ação.",
    "anonymize-confirm": "Anonimizar Permanentemente"
  }
}
```

---

## 3️⃣ VALIDAÇÕES BACKEND (.NET)

### 3.1. Mensagens de Validação (FluentValidation)

**Onde:** `CreateUsuarioCommandValidator.cs`, `UpdateUsuarioCommandValidator.cs`

```csharp
// ❌ ERRADO (mensagens hardcoded em português)
public CreateUsuarioCommandValidator()
{
    RuleFor(v => v.Nome)
        .NotEmpty().WithMessage("Nome é obrigatório.")
        .MaximumLength(200).WithMessage("Nome não pode exceder 200 caracteres.");

    RuleFor(v => v.Email)
        .NotEmpty().WithMessage("Email é obrigatório.")
        .EmailAddress().WithMessage("Email deve ser válido.");
}

// ✅ CORRETO (mensagens traduzíveis - usar resource files ou API de tradução)
// NOTA: FluentValidation não suporta Transloco diretamente, mas as mensagens
// devem seguir o mesmo padrão de nomenclatura
public CreateUsuarioCommandValidator()
{
    RuleFor(v => v.Nome)
        .NotEmpty().WithMessage("validation.users.name-required")
        .MaximumLength(200).WithMessage("validation.users.name-max-length");

    RuleFor(v => v.Email)
        .NotEmpty().WithMessage("validation.users.email-required")
        .EmailAddress().WithMessage("validation.users.email-invalid");

    RuleFor(v => v.Password)
        .NotEmpty().WithMessage("validation.users.password-required")
        .MinimumLength(6).WithMessage("validation.users.password-min-length")
        .Matches(@"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)")
        .WithMessage("validation.users.password-complexity");
}
```

**IMPORTANTE:** No contexto atual do projeto, as mensagens do backend estão em **português hardcoded**. Para tradução completa, seria necessário implementar:

1. **Opção 1:** Resource Files (.resx)
2. **Opção 2:** Middleware de tradução que intercepta erros de validação
3. **Opção 3:** Retornar códigos de erro e traduzir no frontend

**Arquivo i18n (frontend trata erros do backend):**
```json
{
  "validation": {
    "users": {
      "name-required": "Nome é obrigatório.",
      "name-max-length": "Nome não pode exceder 200 caracteres.",
      "email-required": "Email é obrigatório.",
      "email-invalid": "Email deve ser válido.",
      "password-required": "Senha é obrigatória.",
      "password-min-length": "Senha deve ter no mínimo 6 caracteres.",
      "password-complexity": "Senha deve conter pelo menos uma letra maiúscula, uma minúscula e um número.",
      "cpf-invalid": "CPF inválido.",
      "roles-required": "É obrigatório atribuir pelo menos um perfil de acesso."
    }
  }
}
```

---

### 3.2. Mensagens de Erro de Negócio

**Onde:** Handlers, lógica de negócio

```csharp
// ❌ ERRADO
if (existingUser != null)
{
    throw new ValidationException("Este email já está cadastrado");
}

// ✅ CORRETO (com código de erro)
if (existingUser != null)
{
    throw new ValidationException("users.email-already-exists");
}
```

**Arquivo i18n:**
```json
{
  "users": {
    "email-already-exists": "Este e-mail já está cadastrado",
    "cpf-already-exists": "Este CPF já está cadastrado",
    "cannot-delete-self": "Você não pode excluir seu próprio usuário",
    "cannot-delete-last-admin": "Não é possível excluir o último Super Administrador do sistema"
  }
}
```

---

## 4️⃣ TRADUÇÃO DE COMPONENTES DO ANGULAR MATERIAL

### 4.1. MatPaginator - Paginador de Tabelas

**Componentes do Material que precisam de tradução global:**
- MatPaginator (paginador de tabelas)
- MatDatepicker (seletor de data - idioma e formato)
- MatSort (ordenação de colunas)

---

### 4.2. Implementação Completa: MatPaginator

**Passo 1: Criar serviço customizado**

**Arquivo:** `src/app/core/transloco/mat-paginator-intl.service.ts`

```typescript
import { Injectable, inject } from '@angular/core';
import { MatPaginatorIntl } from '@angular/material/paginator';
import { TranslocoService } from '@jsverse/transloco';

@Injectable()
export class CustomMatPaginatorIntl extends MatPaginatorIntl {
    private translocoService = inject(TranslocoService);

    constructor() {
        super();

        // Wait for translations to be loaded before initializing
        this.translocoService.events$.subscribe((event) => {
            if (event.type === 'translationLoadSuccess') {
                this.updateLabels();
            }
        });

        // Subscribe to language changes (reage à troca de idioma)
        this.translocoService.langChanges$.subscribe(() => {
            this.updateLabels();
        });

        // Initialize labels
        this.updateLabels();
    }

    private updateLabels(): void {
        // Labels simples (texto fixo)
        this.itemsPerPageLabel = this.translocoService.translate('paginator.items-per-page');
        this.nextPageLabel = this.translocoService.translate('paginator.next-page');
        this.previousPageLabel = this.translocoService.translate('paginator.previous-page');
        this.firstPageLabel = this.translocoService.translate('paginator.first-page');
        this.lastPageLabel = this.translocoService.translate('paginator.last-page');

        // Trigger change detection (força atualização visual)
        this.changes.next();
    }

    // Método que gera o texto "1 - 10 de 100"
    override getRangeLabel = (page: number, pageSize: number, length: number): string => {
        if (length === 0 || pageSize === 0) {
            return this.translocoService.translate('paginator.range-page-label-1', { length });
        }

        length = Math.max(length, 0);
        const startIndex = page * pageSize;
        const endIndex = startIndex < length
            ? Math.min(startIndex + pageSize, length)
            : startIndex + pageSize;

        return this.translocoService.translate('paginator.range-page-label-2', {
            startIndex: startIndex + 1,
            endIndex,
            length
        });
    };
}
```

**Passo 2: Registrar no app.config.ts**

**Arquivo:** `src/app/app.config.ts`

```typescript
import { ApplicationConfig } from '@angular/core';
import { MatPaginatorIntl } from '@angular/material/paginator';
import { CustomMatPaginatorIntl } from './core/transloco/mat-paginator-intl.service';

export const appConfig: ApplicationConfig = {
    providers: [
        // ... outros providers
        {
            provide: MatPaginatorIntl,
            useClass: CustomMatPaginatorIntl,
        },
    ],
};
```

**Passo 3: Adicionar chaves de tradução**

**Arquivo: `public/i18n/pt.json`**
```json
{
  "paginator": {
    "items-per-page": "Itens por página:",
    "next-page": "Próxima página",
    "previous-page": "Página anterior",
    "first-page": "Primeira página",
    "last-page": "Última página",
    "range-page-label-1": "0 de {{length}}",
    "range-page-label-2": "{{startIndex}} - {{endIndex}} de {{length}}"
  }
}
```

**Arquivo: `public/i18n/en.json`**
```json
{
  "paginator": {
    "items-per-page": "Items per page:",
    "next-page": "Next page",
    "previous-page": "Previous page",
    "first-page": "First page",
    "last-page": "Last page",
    "range-page-label-1": "0 of {{length}}",
    "range-page-label-2": "{{startIndex}} - {{endIndex}} of {{length}}"
  }
}
```

**Arquivo: `public/i18n/es.json`**
```json
{
  "paginator": {
    "items-per-page": "Elementos por página:",
    "next-page": "Página siguiente",
    "previous-page": "Página anterior",
    "first-page": "Primera página",
    "last-page": "Última página",
    "range-page-label-1": "0 de {{length}}",
    "range-page-label-2": "{{startIndex}} - {{endIndex}} de {{length}}"
  }
}
```

**Passo 4: Uso no template (nenhuma alteração necessária)**

```html
<!-- O MatPaginator agora já está traduzido automaticamente -->
<mat-paginator
  [pageSizeOptions]="[10, 25, 50, 100]"
  [pageSize]="10"
  [showFirstLastButtons]="true">
</mat-paginator>
```

**Benefícios:**
✅ Tradução automática em TODAS as tabelas do sistema
✅ Reage à troca de idioma (sem refresh de página)
✅ Mantém formatação consistente
✅ Configuração única, uso global

---

### 4.3. Outros Componentes do Material que Podem Precisar de Tradução

**MatDatepicker:**
```typescript
// Configurar locale do DateAdapter
import { MAT_DATE_LOCALE } from '@angular/material/core';

providers: [
  { provide: MAT_DATE_LOCALE, useValue: 'pt-BR' }
]
```

**MatSort:**
- Geralmente não precisa de tradução adicional
- Os cabeçalhos de coluna já são traduzidos via `{{ 'key' | transloco }}`

**MatDialog, MatSnackBar:**
- Traduzir mensagens via `TranslocoService.translate()` (já coberto na seção 2)

---

## 5️⃣ ORGANIZAÇÃO DOS ARQUIVOS DE TRADUÇÃO

### 5.1. Estrutura Hierárquica Completa

**Arquivo: `public/i18n/pt.json`**

```json
{
  "users": {
    // Títulos e navegação
    "title": "Usuários",
    "subtitle": "Gerencie os usuários do sistema",
    "breadcrumb": "Administração",

    // Ações principais
    "new-user": "Novo Usuário",
    "all-users": "Todos os Usuários",
    "clear-filters": "Limpar Filtros",
    "search": "Pesquisar",
    "search-placeholder": "Nome, email ou CPF",

    // Contadores (pluralização)
    "user-count-singular": "usuário cadastrado",
    "user-count-plural": "usuários cadastrados",

    // Campos de formulário
    "field-email": "Email",
    "field-name": "Nome",
    "field-phone": "Telefone",
    "field-cpf": "CPF",
    "field-birth-date": "Data de Nascimento",
    "field-password": "Senha",
    "field-new-password": "Nova senha",
    "field-roles": "Perfis de acesso",
    "field-active": "Usuário ativo",
    "field-company": "Empresa",
    "field-language": "Idioma",
    "field-theme": "Tema",
    "field-timezone": "Fuso Horário",
    "field-must-change-password": "Forçar troca de senha no primeiro login",
    "field-force-change-password": "Forçar usuário a trocar a senha no próximo login",

    // Validações (frontend)
    "error-email-required": "Email é obrigatório",
    "error-email-invalid": "Informe um email válido",
    "error-name-required": "Nome é obrigatório",
    "error-cpf-invalid": "CPF inválido",
    "error-password-required": "Senha é obrigatória",
    "error-password-minlength": "Mínimo de 6 caracteres",
    "error-roles-required": "Selecione pelo menos um perfil",
    "error-company-required": "Empresa é obrigatória",

    // Status e badges
    "active": "Ativo",
    "inactive": "Inativo",
    "badge-blocked": "Bloqueado",
    "badge-mfa": "MFA",
    "badge-ad": "AD",
    "badge-password-expired": "Senha Expirada",
    "badge-anonymized": "Anonimizado",

    // Tooltips
    "tooltip-blocked": "Usuário bloqueado",
    "tooltip-mfa": "Autenticação de dois fatores ativa",
    "tooltip-ad": "Usuário sincronizado com Active Directory",
    "tooltip-password-expired": "Senha expirada - usuário deve alterar no próximo login",
    "tooltip-anonymized": "Dados pessoais removidos (LGPD Art. 18)",

    // Filtros
    "filters": "Filtros",
    "status-label": "Status",
    "all": "Todos",
    "blocking-label": "Bloqueio",
    "blocked": "Bloqueados",
    "not-blocked": "Não Bloqueados",
    "mfa-label": "MFA",
    "with-mfa": "Com MFA",
    "without-mfa": "Sem MFA",
    "ad-label": "Active Directory",
    "ad-users": "Usuários AD",
    "local-users": "Usuários Locais",
    "lgpd-label": "LGPD",
    "anonymized": "Anonimizados",
    "not-anonymized": "Não Anonimizados",
    "password-label": "Senha",
    "expired-passwords": "Expiradas",
    "valid-passwords": "Válidas",

    // Tabela
    "name": "Nome",
    "company": "Empresa",
    "phone": "Telefone",
    "roles": "Perfis",
    "status": "Status",
    "actions-column": "Ações",

    // Menu de ações
    "action-edit": "Editar",
    "action-reactivate": "Reativar",
    "action-deactivate": "Desativar",
    "action-anonymize": "Anonimizar (LGPD)",

    // Diálogos
    "dialog-title-new": "Novo usuário",
    "dialog-title-edit": "Editar usuário",
    "dialog-title-details": "Detalhes do usuário",

    // Seções
    "section-preferences": "Preferências",
    "section-security": "Segurança",

    // Opções de select
    "lang-pt-br": "Português (Brasil)",
    "lang-en": "English",
    "lang-es": "Español",
    "theme-light": "Claro",
    "theme-dark": "Escuro",
    "theme-auto": "Automático",
    "timezone-sao-paulo": "São Paulo (GMT-3)",
    "timezone-new-york": "Nova York (GMT-5)",
    "timezone-los-angeles": "Los Angeles (GMT-8)",
    "timezone-london": "Londres (GMT+0)",
    "timezone-paris": "Paris (GMT+1)",
    "timezone-tokyo": "Tóquio (GMT+9)",

    // Botões
    "button-generate-temp-password": "Gerar senha temporária",
    "button-toggle-password-show": "Ocultar",
    "button-toggle-password-hide": "Definir",
    "button-toggle-password-suffix": "senha manualmente",
    "button-change-password": "Alterar senha",
    "button-delete": "Excluir",
    "button-cancel": "Cancelar",
    "button-save": "Salvar",
    "button-edit": "Editar",

    // Placeholders e hints
    "placeholder-new-password": "Digite a nova senha",
    "hint-min-characters": "Mínimo 6 caracteres",
    "hint-select-company-first": "Selecione uma empresa primeiro",

    // Força de senha
    "password-strength-label": "Força da senha:",
    "password-strength-weak": "Fraca - use letras, números e símbolos",
    "password-strength-medium": "Média - adicione mais variedade de caracteres",
    "password-strength-strong": "Forte",
    "password-strength-very-strong": "Muito forte",

    // Mensagens de erro/sucesso
    "email-already-exists": "Este e-mail já está cadastrado",
    "cpf-already-exists": "Este CPF já está cadastrado",
    "cannot-delete-self": "Você não pode excluir seu próprio usuário",
    "cannot-delete-last-admin": "Não é possível excluir o último Super Administrador do sistema"
  }
}
```

---

## 6️⃣ BOAS PRÁTICAS E CONVENÇÕES

### ✅ SEMPRE FAZER

1. **Usar pipe `transloco` em templates HTML**
   ```html
   {{ 'users.title' | transloco }}
   ```

2. **Usar `TranslocoService.translate()` em TypeScript**
   ```typescript
   this._translocoService.translate('users.error-message')
   ```

3. **Nomenclatura consistente de chaves**
   - `field-*` para campos de formulário
   - `error-*` para mensagens de erro
   - `button-*` para botões
   - `tooltip-*` para tooltips
   - `badge-*` para badges
   - `action-*` para ações de menu
   - `dialog-*` para elementos de diálogo

4. **Interpolar variáveis corretamente**
   ```json
   "message": "Usuário {{nome}} foi excluído"
   ```
   ```typescript
   translate('users.message', { nome: usuario.nome })
   ```

5. **Tratar pluralização explicitamente**
   ```html
   {{ (count === 1 ? 'users.singular' : 'users.plural') | transloco }}
   ```

6. **Organizar hierarquicamente no JSON**
   ```json
   {
     "users": {
       "fields": { ... },
       "errors": { ... },
       "tooltips": { ... }
     }
   }
   ```

7. **Sempre traduzir os 3 idiomas (pt, en, es)**

---

### ❌ NUNCA FAZER

1. **Texto hardcoded em templates**
   ```html
   <!-- ERRADO -->
   <h2>Usuários</h2>
   ```

2. **Mensagens hardcoded em TypeScript**
   ```typescript
   // ERRADO
   title: 'Excluir usuário'
   ```

3. **Misturar idiomas**
   ```json
   // ERRADO
   {
     "title": "Users",      // inglês
     "subtitle": "Usuarios" // espanhol
   }
   ```

4. **Esquecer de traduzir tooltips ou hints**

5. **Usar concatenação de strings traduzidas**
   ```typescript
   // ERRADO
   const msg = translate('users.hello') + ' ' + usuario.nome;

   // CORRETO
   const msg = translate('users.hello-user', { nome: usuario.nome });
   ```

6. **Deixar chaves sem tradução em algum idioma**
   - Se `pt.json` tem 100 chaves, `en.json` e `es.json` DEVEM ter as mesmas 100 chaves

---

## 7️⃣ CHECKLIST FINAL DE VALIDAÇÃO

Antes de considerar uma funcionalidade **100% traduzida**, verifique:

- [ ] **1. Todos os textos visíveis no template usam pipe `| transloco`**
- [ ] **2. Todas as mensagens TypeScript usam `TranslocoService.translate()`**
- [ ] **3. Todas as chaves existem nos 3 arquivos (pt.json, en.json, es.json)**
- [ ] **4. Validações de formulário estão traduzidas**
- [ ] **5. Tooltips e hints estão traduzidos**
- [ ] **6. Mensagens de erro HTTP estão traduzidas**
- [ ] **7. Diálogos de confirmação estão traduzidos**
- [ ] **8. Badges e status estão traduzidos**
- [ ] **9. Filtros e opções de select estão traduzidos**
- [ ] **10. Cabeçalhos de tabela estão traduzidos**
- [ ] **11. Botões e ações de menu estão traduzidos**
- [ ] **12. Placeholders estão traduzidos**
- [ ] **13. Pluralização está implementada**
- [ ] **14. Interpolação de variáveis funciona corretamente**
- [ ] **15. MatPaginator está traduzido (CustomMatPaginatorIntl configurado)**
- [ ] **16. Outros componentes Material traduzidos (MatDatepicker, etc.)**
- [ ] **17. Seções e agrupamentos estão traduzidos**
- [ ] **18. Não há texto hardcoded em nenhum lugar**
- [ ] **19. Teste manual nos 3 idiomas (pt, en, es)**
- [ ] **20. Teste de troca de idioma em tempo real (sem refresh)**

---

## 8️⃣ SCRIPT DE VALIDAÇÃO

**Script PowerShell para verificar chaves faltantes:**

```powershell
# Validar consistência de traduções
$ptFile = "frontend/icontrolit-app/public/i18n/pt.json"
$enFile = "frontend/icontrolit-app/public/i18n/en.json"
$esFile = "frontend/icontrolit-app/public/i18n/es.json"

$pt = Get-Content $ptFile | ConvertFrom-Json
$en = Get-Content $enFile | ConvertFrom-Json
$es = Get-Content $esFile | ConvertFrom-Json

$ptKeys = $pt.users.PSObject.Properties.Name
$enKeys = $en.users.PSObject.Properties.Name
$esKeys = $es.users.PSObject.Properties.Name

$missingInEn = $ptKeys | Where-Object { $_ -notin $enKeys }
$missingInEs = $ptKeys | Where-Object { $_ -notin $esKeys }

if ($missingInEn) {
  Write-Host "Chaves faltando em en.json:" -ForegroundColor Red
  $missingInEn | ForEach-Object { Write-Host "  - $_" }
}

if ($missingInEs) {
  Write-Host "Chaves faltando em es.json:" -ForegroundColor Red
  $missingInEs | ForEach-Object { Write-Host "  - $_" }
}

if (-not $missingInEn -and -not $missingInEs) {
  Write-Host "✓ Todas as traduções estão consistentes!" -ForegroundColor Green
}
```

---

## 9️⃣ EXEMPLO COMPLETO: ANTES E DEPOIS

### ANTES (sem tradução)

**list.component.html:**
```html
<h2 class="text-3xl">Usuários</h2>
<div class="text-secondary">Gerencie os usuários do sistema</div>
<button mat-flat-button>Novo Usuário</button>

<mat-form-field>
  <mat-label>Status</mat-label>
  <mat-select [(ngModel)]="filters.ativo">
    <mat-option [value]="null">Todos</mat-option>
    <mat-option [value]="true">Ativo</mat-option>
    <mat-option [value]="false">Inativo</mat-option>
  </mat-select>
</mat-form-field>
```

**list.component.ts:**
```typescript
deleteUsuario(usuario: Usuario): void {
  const confirmation = this._fuseConfirmationService.open({
    title: 'Excluir usuário',
    message: `Tem certeza que deseja excluir ${usuario.nome}?`,
    actions: {
      confirm: { label: 'Excluir' },
      cancel: { label: 'Cancelar' }
    }
  });
}
```

---

### DEPOIS (100% traduzido)

**list.component.html:**
```html
<h2 class="text-3xl">{{ 'users.title' | transloco }}</h2>
<div class="text-secondary">{{ 'users.subtitle' | transloco }}</div>
<button mat-flat-button>{{ 'users.new-user' | transloco }}</button>

<mat-form-field>
  <mat-label>{{ 'users.status-label' | transloco }}</mat-label>
  <mat-select [(ngModel)]="filters.ativo">
    <mat-option [value]="null">{{ 'users.all' | transloco }}</mat-option>
    <mat-option [value]="true">{{ 'users.active' | transloco }}</mat-option>
    <mat-option [value]="false">{{ 'users.inactive' | transloco }}</mat-option>
  </mat-select>
</mat-form-field>
```

**list.component.ts:**
```typescript
private _translocoService = inject(TranslocoService);

deleteUsuario(usuario: Usuario): void {
  const confirmation = this._fuseConfirmationService.open({
    title: this._translocoService.translate('users.dialog-delete-title'),
    message: this._translocoService.translate('users.dialog-delete-message', {
      nome: usuario.nome
    }),
    actions: {
      confirm: {
        label: this._translocoService.translate('users.button-delete')
      },
      cancel: {
        label: this._translocoService.translate('users.button-cancel')
      }
    }
  });
}
```

**pt.json:**
```json
{
  "users": {
    "title": "Usuários",
    "subtitle": "Gerencie os usuários do sistema",
    "new-user": "Novo Usuário",
    "status-label": "Status",
    "all": "Todos",
    "active": "Ativo",
    "inactive": "Inativo",
    "dialog-delete-title": "Excluir usuário",
    "dialog-delete-message": "Tem certeza que deseja excluir {{nome}}?",
    "button-delete": "Excluir",
    "button-cancel": "Cancelar"
  }
}
```

**en.json:**
```json
{
  "users": {
    "title": "Users",
    "subtitle": "Manage system users",
    "new-user": "New User",
    "status-label": "Status",
    "all": "All",
    "active": "Active",
    "inactive": "Inactive",
    "dialog-delete-title": "Delete user",
    "dialog-delete-message": "Are you sure you want to delete {{nome}}?",
    "button-delete": "Delete",
    "button-cancel": "Cancel"
  }
}
```

**es.json:**
```json
{
  "users": {
    "title": "Usuarios",
    "subtitle": "Gestionar usuarios del sistema",
    "new-user": "Nuevo Usuario",
    "status-label": "Estado",
    "all": "Todos",
    "active": "Activo",
    "inactive": "Inactivo",
    "dialog-delete-title": "Eliminar usuario",
    "dialog-delete-message": "¿Está seguro de que desea eliminar {{nome}}?",
    "button-delete": "Eliminar",
    "button-cancel": "Cancelar"
  }
}
```

---

## 🔟 FERRAMENTAS E COMANDOS ÚTEIS

### Validar chaves de tradução

```bash
# Rodar validação de i18n (se configurado)
npm run i18n:validate
```

### Encontrar textos hardcoded

```bash
# Buscar textos em português no código (pode indicar hardcoding)
grep -r "usuário\|Usuário\|senha\|Senha" src/app/modules/admin/management/users --include="*.html" --include="*.ts"
```

### Comparar arquivos de tradução

```bash
# Verificar se en.json tem todas as chaves de pt.json
# (Usar script PowerShell da seção 8)
```

---

## 📚 REFERÊNCIAS

- **Transloco Docs:** https://ngneat.github.io/transloco/
- **Angular i18n:** https://angular.io/guide/i18n-overview
- **Material Paginator i18n:** https://material.angular.io/components/paginator/overview#internationalization

---

## 📝 RESUMO EXECUTIVO

Para garantir **tradução 100% completa** de uma funcionalidade:

1. **Templates HTML:** Use `| transloco` em TODOS os textos visíveis
2. **TypeScript:** Injete `TranslocoService` e use `.translate()` em TODAS as mensagens
3. **Validações:** Traduza mensagens de erro (frontend e backend)
4. **Componentes Material:** Configure `CustomMatPaginatorIntl` e outros providers globais
5. **Três idiomas:** Sempre pt.json, en.json, es.json
6. **Checklist:** Use o checklist de 20 itens da seção 7
7. **Teste:** Troque o idioma no sistema e navegue pela funcionalidade inteira
8. **Referência:** Consulte `/management/users` como exemplo completo

**Regra de ouro:** Se você vê um texto em português/inglês/espanhol no código-fonte (HTML ou TS), ele DEVE estar em um arquivo de tradução.

**Componentes do Material:** São traduzidos uma única vez no `app.config.ts` e funcionam em TODO o sistema.

---

---

## 🎓 LIÇÕES APRENDIDAS E BOAS PRÁTICAS

### Erros Comuns a Evitar

1. **NÃO usar prefixos [EN] ou [ES] nos textos**
   - ERRADO: `"title": "[ES] Título en español"`
   - CORRETO: `"title": "Título en español"`

2. **Garantir que TODAS as chaves existam nos 3 idiomas**
   - Sempre que criar uma chave em pt.json, criar também em en.json e es.json
   - Usar ferramenta de validação: `npm run i18n:validate`

3. **Não esquecer dos modais e dialogs**
   - Modais de criação/edição têm muitos textos
   - Criar seção `.details` para cada módulo com modal
   - Incluir: títulos, labels, placeholders, erros, botões

4. **Verificar chaves COMMON reutilizáveis**
   - Antes de criar nova chave, verificar se já existe em COMMON
   - Chaves comuns: SEARCH, SAVE, CANCEL, DELETE, EDIT, ALL, ACTIVE, INACTIVE

---

### Checklist de Tradução Completa

Para cada módulo/página, verificar:

- [ ] Título e subtítulo da página
- [ ] Botões de ação (Novo, Editar, Excluir, etc.)
- [ ] Filtros (labels, placeholders, opções de select)
- [ ] Colunas de tabela
- [ ] Ações do menu
- [ ] Badges e chips de status
- [ ] Estados vazios (nenhum registro encontrado)
- [ ] Contadores (X registros encontrados)
- [ ] **MODAIS/DIALOGS:**
  - [ ] Títulos (Novo, Editar, Visualizar)
  - [ ] Labels de campos
  - [ ] Placeholders
  - [ ] Mensagens de erro de validação
  - [ ] Botões (Salvar, Cancelar, etc.)
  - [ ] Tooltips
  - [ ] Mensagens informativas

---

### Estrutura Recomendada de Chaves para Módulos

```json
{
  "modulo": {
    "title": "Título da Página",
    "subtitle": "Subtítulo",
    "new": "Novo Item",
    "filters": "Filtros",
    "clear-filters": "Limpar Filtros",
    "field-*": "Labels de campos",
    "search-placeholder": "Placeholder de busca",
    "column-*": "Colunas de tabela",
    "action-*": "Ações de menu",
    "count-singular": "registro encontrado",
    "count-plural": "registros encontrados",
    "empty": "Nenhum registro encontrado",
    "details": {
      "title-new": "Novo Item",
      "title-edit": "Editar Item",
      "title-view": "Visualizar Item",
      "field-*": "Labels dos campos do modal",
      "placeholder-*": "Placeholders",
      "error-*": "Mensagens de erro",
      "button-*": "Botões"
    }
  }
}
```

---

### Comandos Úteis

```bash
# Validar traduções (verifica chaves faltantes)
npm run i18n:validate

# Corrigir problemas automaticamente
npm run i18n:fix

# Buscar chaves não traduzidas no console do browser
# Procurar por "Missing translation for"
```

---

**Última Atualização:** 2025-01-18
**Versão:** 1.2
**Baseado em:** RF-006 - Gestão de Usuários, RF-008 - Empresas e Filiais

**Arquivos de Referência:**
- **Frontend:** `frontend/icontrolit-app/src/app/modules/admin/management/users/`
- **Traduções:** Busque por `"users"`, `"roles"`, `"empresas"` e `"paginator"` em `public/i18n/*.json`
- **Componentes:** `src/app/core/transloco/mat-paginator-intl.service.ts`
- **Config:** `src/app/app.config.ts`
