# ESQUECIMENTOS OU ERROS COMUNS DE VALIDAÇÃO DE CONTRATO FRONTEND

> ⚠️ **IMPORTANTE**: Este é apenas um documento de **LEMBRETE** do que pode ocorrer e de como não errar. **NÃO é uma diretriz** nem substitui os contratos oficiais. Consulte sempre:
- \docs\contracts\desenvolvimento\execucao\frontend-criacao.md
- \docs\contracts\desenvolvimento\execucao\frontend-adequacao.md
- \docs\contracts\desenvolvimento\validacao\frontend.md

---

## 🔴 TOP 50 - ERROS MAIS COMUNS

### 1. Esquecer de traduzir textos (i18n com Transloco)
**Sintoma:** Textos hardcoded em português no template ou TypeScript

**Fix rápido:**
```html
<!-- ❌ ERRADO -->
<h2>Usuários</h2>

<!-- ✅ CORRETO -->
<h2>{{ 'users.title' | transloco }}</h2>
```

```typescript
// ❌ ERRADO
title: 'Excluir usuário'

// ✅ CORRETO
title: this._translocoService.translate('users.dialog-delete-title')
```

**16 PONTOS OBRIGATÓRIOS:** Templates, TypeScript, Validações, Toasts, Tooltips, Badges, Breadcrumbs, Tabelas, Paginação, Filtros, Diálogos, Erros HTTP, Pluralização, Interpolação, Material Components

**Referência:** [PARTICULARIDADES-DO-SISTEMA.md](./PARTICULARIDADES-DO-SISTEMA.md) - Seção 2, [GUIA-TRANSLATE.md](./GUIA-TRANSLATE.md)

---

### 2. Criar NgModules ao invés de Standalone Components
**Sintoma:** `@NgModule` no código Angular 19

**Fix rápido:**
```typescript
// ❌ ERRADO
@NgModule({
    declarations: [ListComponent],
    imports: [CommonModule]
})
export class UsersModule {}

// ✅ CORRETO
@Component({
    selector: 'app-users-list',
    standalone: true,  // ← SEMPRE standalone!
    imports: [CommonModule, MatTableModule, TranslocoModule]
})
export class ListComponent {}
```

**Referência:** [PARTICULARIDADES-DO-SISTEMA.md](./PARTICULARIDADES-DO-SISTEMA.md) - Seção 9, [ERROS-COMUNS-ANGULAR.md](./ERROS-COMUNS-ANGULAR.md) - Erro #1

---

### 3. Importar FuseModule ao invés de componentes diretos
**Sintoma:** `import { FuseModule } from '@fuse'`

**Fix rápido:**
```typescript
// ❌ ERRADO
import { FuseModule } from '@fuse';

// ✅ CORRETO
import { FuseCardComponent } from '@fuse/components/card';
```

**Referência:** [PARTICULARIDADES-DO-SISTEMA.md](./PARTICULARIDADES-DO-SISTEMA.md) - Seção 9

---

### 4. Usar @ngx-translate ao invés de @jsverse/transloco
**Sintoma:** `import { TranslateModule } from '@ngx-translate/core'`

**Fix rápido:**
```typescript
// ❌ ERRADO
import { TranslateModule } from '@ngx-translate/core';

// ✅ CORRETO
import { TranslocoModule } from '@jsverse/transloco';
```

**Referência:** [ERROS-COMUNS-ANGULAR.md](./ERROS-COMUNS-ANGULAR.md) - Erro #2

---

### 5. Esquecer de verificar permissões com *hasPermission
**Sintoma:** Botões aparecem para usuários sem permissão

**Fix rápido:**
```html
<!-- ❌ ERRADO -->
<button mat-raised-button>Criar Usuário</button>

<!-- ✅ CORRETO -->
<button mat-raised-button *hasPermission="'Users.Create'">
    Criar Usuário
</button>
```

**Referência:** [PARTICULARIDADES-DO-SISTEMA.md](./PARTICULARIDADES-DO-SISTEMA.md) - Seção 3

---

### 6. Não seguir padrões do Fuse Template
**Sintoma:** Telas com layout diferente do resto do sistema

**Fix rápido:**
- Ler http://localhost:4200/docs antes de implementar
- Usar estrutura base de página (sem max-w-screen-xl)
- Cards com `bg-card` e `rounded-2xl`
- Ícones `heroicons_outline`

**Referência:** [PARTICULARIDADES-DO-SISTEMA.md](./PARTICULARIDADES-DO-SISTEMA.md) - Seção 6, [GUIA-LAYOUT.md](./GUIA-LAYOUT.md)

---

### 7. Esquecer de imports obrigatórios
**Sintoma:** `NG8001: 'x' is not a known element`

**Fix rápido:**
```typescript
imports: [
    CommonModule,        // ← SEMPRE
    RouterModule,        // Se usar routerLink
    MatTableModule,      // Conforme uso
    TranslocoModule,     // ← SEMPRE
    FuseCardComponent    // Componente direto, não module
]
```

**Referência:** [ERROS-COMUNS-ANGULAR.md](./ERROS-COMUNS-ANGULAR.md) - Erro #3

---

### 8. Arrow functions em templates
**Sintoma:** Change detection travando ou lentidão

**Fix rápido:**
```html
<!-- ❌ ERRADO -->
<button (click)="items.filter(x => x.active)">

<!-- ✅ CORRETO -->
<button (click)="filterActive()">

<!-- TypeScript -->
filterActive() {
    return this.items.filter(x => x.active);
}
```

**Referência:** [ERROS-COMUNS-ANGULAR.md](./ERROS-COMUNS-ANGULAR.md) - Erro #1

---

### 9. Adicionar serviços autenticados em initialDataResolver
**Sintoma:** Login quebrado, erro 401 antes de autenticar

**Fix rápido:**
```typescript
// ❌ ERRADO (causa erro 401)
return forkJoin([
    shortcutsService.getAll(), // ← Requer auth!
]);

// ✅ CORRETO (carregar no componente após login)
ngOnInit() {
    this.shortcutsService.getAll().subscribe();
}
```

**Referência:** [ERROS-COMUNS-ANGULAR.md](./ERROS-COMUNS-ANGULAR.md) - Erro #4

---

### 10. Esquecer de rodar `npm run build` antes de commit
**Sintoma:** Build quebrado no CI/CD ou em outras máquinas

**Fix rápido:**
```bash
cd frontend/icontrolit-app
npm run build
# DEVE retornar: ✔ Compiled successfully.
```

**Regra:** SEMPRE rodar build antes de commit

**Referência:** [PARTICULARIDADES-DO-SISTEMA.md](./PARTICULARIDADES-DO-SISTEMA.md) - Seção 7

---

### 11. Não traduzir os 3 idiomas (pt, en, es)
**Sintoma:** Chaves faltando em en.json ou es.json

**Fix rápido:**
```bash
# Verificar chaves faltantes
npm run i18n:validate

# Corrigir automaticamente
npm run i18n:fix
```

**Regra:** SEMPRE traduzir pt.json, en.json, es.json

**Referência:** [PARTICULARIDADES-DO-SISTEMA.md](./PARTICULARIDADES-DO-SISTEMA.md) - Seção 2

---

### 12. Não configurar CustomMatPaginatorIntl
**Sintoma:** MatPaginator em inglês hardcoded

**Fix rápido:**
1. Criar `src/app/core/transloco/mat-paginator-intl.service.ts`
2. Registrar em `app.config.ts`:
```typescript
{
    provide: MatPaginatorIntl,
    useClass: CustomMatPaginatorIntl,
}
```

**Referência:** [GUIA-TRANSLATE.md](./GUIA-TRANSLATE.md) - Seção 4.2

---

## 📚 LEMBRE-SE SEMPRE

1. **i18n (Transloco)** - Traduzir TODOS os textos em pt-BR, en, es (16 pontos)
2. **Standalone Components** - `standalone: true`, NUNCA NgModules
3. **Fuse Template** - Seguir padrões visuais do Fuse
4. **Imports** - CommonModule + TranslocoModule SEMPRE
5. **Permissões** - Usar `*hasPermission` em botões/ações
6. **Build** - SEMPRE rodar `npm run build` antes de commit
7. **Arrow Functions** - NÃO usar em templates
8. **MatPaginator** - Configurar CustomMatPaginatorIntl
9. **Componentes Fuse** - Importar direto, NÃO FuseModule
10. **Consultar PARTICULARIDADES** - [PARTICULARIDADES-DO-SISTEMA.md](./PARTICULARIDADES-DO-SISTEMA.md)

---

## 🔗 DOCUMENTOS RELACIONADOS

- **[PARTICULARIDADES-DO-SISTEMA.md](./PARTICULARIDADES-DO-SISTEMA.md)** - 10 particularidades obrigatórias
- **[ERROS-COMUNS-ANGULAR.md](./ERROS-COMUNS-ANGULAR.md)** - 8 erros críticos de Angular
- **[GUIA-TRANSLATE.md](./GUIA-TRANSLATE.md)** - Guia completo de i18n (16 pontos)
- **[GUIA-LAYOUT.md](./GUIA-LAYOUT.md)** - Padrões visuais do Fuse Template
- **[GUIA-DEVELOPER.md](./GUIA-DEVELOPER.md)** - Guia completo de desenvolvimento

---