# GUIA-LAYOUT.md

Guia de padronização de layout e uso de componentes visuais do IControlIT.

**Última Atualização:** 2025-01-18

---

## 1. Visão Geral

O IControlIT utiliza o **Fuse Admin Template** (Angular 19) como base para o frontend. Este guia documenta os padrões de layout estabelecidos e orienta sobre como utilizar os componentes disponíveis de forma consistente.

---

## 2. Leitura Obrigatória

Antes de desenvolver qualquer tela, é **OBRIGATÓRIO** navegar e ler completamente:

| Recurso | URL | Descrição |
|---------|-----|-----------|
| **Guia de Introdução** | http://localhost:4200/docs/guides/getting-started/introduction | Conceitos fundamentais do Fuse |
| **Material Components** | http://localhost:4200/ui/material-components | Todos os componentes Angular Material |
| **Other Components** | http://localhost:4200/ui/other-components/common/overview | Componentes adicionais disponíveis |
| **Fuse Components** | http://localhost:4200/ui/fuse-components/libraries/mock-api | Componentes exclusivos do Fuse |

---

## 3. Padrões de Layout Estabelecidos

### 3.1 Estrutura Base de Página

Toda página de listagem deve seguir este padrão:

```html
<div class="flex w-full flex-auto flex-col">
    <div class="mx-auto flex w-full flex-wrap p-6 md:p-8">
        <!-- Conteúdo da página -->
    </div>
</div>
```

**Regras:**
- **NÃO usar** `max-w-screen-xl` - permite que o conteúdo ocupe toda a largura
- Padding responsivo: `p-6` mobile, `md:p-8` desktop

### 3.2 Cabeçalho de Página (Título + Ações)

```html
<div class="flex w-full flex-col gap-4 md:flex-row md:items-center md:justify-between">
    <div>
        <!-- Breadcrumb (opcional) -->
        <div class="flex flex-wrap items-center text-sm font-medium text-secondary mb-2">
            <span class="whitespace-nowrap text-primary-500">Admin</span>
            <mat-icon class="mx-1 icon-size-4 text-secondary" [svgIcon]="'heroicons_mini:chevron-right'"></mat-icon>
            <span class="whitespace-nowrap">Página Atual</span>
        </div>

        <!-- Título -->
        <h2 class="text-3xl font-semibold leading-tight tracking-tight">
            {{ 'pagina.titulo' | transloco }}
        </h2>

        <!-- Subtítulo -->
        <div class="text-secondary font-medium tracking-tight">
            {{ 'pagina.subtitulo' | transloco }}
        </div>
    </div>

    <!-- Botões de ação -->
    <div class="flex items-center gap-2">
        <button mat-flat-button color="primary">
            <mat-icon [svgIcon]="'heroicons_outline:plus'"></mat-icon>
            <span class="ml-2">{{ 'pagina.criar' | transloco }}</span>
        </button>
    </div>
</div>
```

### 3.3 Cards de Conteúdo

```html
<div class="bg-card flex flex-col overflow-hidden rounded-2xl shadow">
    <!-- Header do card -->
    <div class="flex items-center justify-between border-b border-surface-200/60 px-6 py-5">
        <div>
            <div class="text-lg font-medium leading-6 tracking-tight">
                Título do Card
            </div>
            <div class="text-secondary text-sm">
                Descrição ou contagem
            </div>
        </div>
    </div>

    <!-- Conteúdo -->
    <div class="p-6">
        <!-- Conteúdo aqui -->
    </div>
</div>
```

### 3.4 Tabelas

```html
<div class="overflow-x-auto mx-6">
    <table
        mat-table
        [dataSource]="dataSource"
        class="w-full min-w-[720px] bg-transparent"
    >
        <!-- Colunas -->
        <ng-container matColumnDef="nome">
            <th mat-header-cell *matHeaderCellDef>Nome</th>
            <td mat-cell *matCellDef="let item">{{ item.nome }}</td>
        </ng-container>

        <tr mat-header-row *matHeaderRowDef="displayedColumns"></tr>
        <tr mat-row *matRowDef="let row; columns: displayedColumns"
            class="h-16 hover:bg-primary-50/40 dark:hover:bg-primary-500/10"></tr>
    </table>
</div>
```

### 3.5 Campos de Busca

Use tamanho compacto (`w-56`) para não empurrar outros elementos:

```html
<mat-form-field class="w-56" appearance="outline">
    <mat-label>Buscar</mat-label>
    <input matInput [(ngModel)]="searchTerm">
    <mat-icon matPrefix>search</mat-icon>
</mat-form-field>
```

### 3.6 Status Badges

```html
<span class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-bold uppercase tracking-wide"
    [ngClass]="{
        'bg-green-200 text-green-800 dark:bg-green-600 dark:text-green-50': item.ativo,
        'bg-red-200 text-red-800 dark:bg-red-600 dark:text-red-50': !item.ativo
    }">
    {{ item.ativo ? 'Ativo' : 'Inativo' }}
</span>
```

### 3.7 Menu de Ações

```html
<button mat-icon-button [matMenuTriggerFor]="actionsMenu">
    <mat-icon class="icon-size-5" [svgIcon]="'heroicons_mini:ellipsis-vertical'"></mat-icon>
</button>
<mat-menu #actionsMenu="matMenu">
    <button mat-menu-item (click)="editar(item)">
        <mat-icon class="mr-3 icon-size-5" [svgIcon]="'heroicons_outline:pencil-square'"></mat-icon>
        <span>Editar</span>
    </button>
    <mat-divider></mat-divider>
    <button mat-menu-item (click)="excluir(item)">
        <mat-icon class="mr-3 icon-size-5 text-warn" [svgIcon]="'heroicons_outline:trash'"></mat-icon>
        <span class="text-warn">Excluir</span>
    </button>
</mat-menu>
```

### 3.8 Estado Vazio

```html
<div *ngIf="!items.length" class="flex h-64 items-center justify-center">
    <div class="text-center">
        <mat-icon class="icon-size-8 text-secondary" [svgIcon]="'heroicons_outline:inbox'"></mat-icon>
        <div class="mt-3 text-lg font-semibold">
            Nenhum item encontrado
        </div>
        <div class="text-secondary mt-1 text-sm">
            Clique em "Criar" para adicionar o primeiro item
        </div>
    </div>
</div>
```

---

## 4. Componentes e Páginas de Referência do Fuse

O Fuse possui dezenas de componentes prontos e páginas exemplo que devemos usar como referência.

### 4.1 Dashboards (Exemplos de Layout Complexo)

| Página | URL | O que aprender |
|--------|-----|----------------|
| Project | http://localhost:4200/dashboards/project | Cards de estatísticas, gráficos, listas |
| Analytics | http://localhost:4200/dashboards/analytics | Visualizações de dados, charts |
| Finance | http://localhost:4200/dashboards/finance | Tabelas financeiras, indicadores |
| Crypto | http://localhost:4200/dashboards/crypto | Cards com dados em tempo real |

### 4.2 Aplicações (Funcionalidades Completas)

| Página | URL | O que aprender |
|--------|-----|----------------|
| Chat | http://localhost:4200/apps/chat | Conversas, listas, sidebar |
| Help Center | http://localhost:4200/apps/help-center | FAQs, acordeões, busca |
| Mailbox | http://localhost:4200/apps/mailbox/inbox/1 | Lista/detalhe, seleção múltipla |
| Scrumboard | http://localhost:4200/apps/scrumboard | Drag & drop, kanban |
| Board Detail | http://localhost:4200/apps/scrumboard/2c82225f-2a6c-45d3-b18a-1132712a4234 | Cards editáveis, modais |

### 4.3 Páginas de Sistema

| Página | URL | O que aprender |
|--------|-----|----------------|
| Settings | http://localhost:4200/pages/settings | Formulários de configuração, tabs |
| Profile | http://localhost:4200/pages/profile | Página de perfil, avatar, timeline |

---

## 5. Componentes UI Disponíveis

### 5.1 Componentes Base

| Componente | URL | Descrição |
|------------|-----|-----------|
| Cards | http://localhost:4200/ui/cards | Variações de cards para conteúdo |
| Colors | http://localhost:4200/ui/colors | Paleta de cores disponíveis |
| Confirmation Dialog | http://localhost:4200/ui/confirmation-dialog | Diálogos de confirmação |
| Datatable | http://localhost:4200/ui/datatable | Tabelas avançadas com sort/filter |
| Typography | http://localhost:4200/ui/typography | Estilos de texto padronizados |
| Animations | http://localhost:4200/ui/animations | Animações prontas para uso |

### 5.2 Formulários

| Componente | URL | Descrição |
|------------|-----|-----------|
| Form Layouts | http://localhost:4200/ui/forms/layouts | Layouts de formulário |
| Form Wizards | http://localhost:4200/ui/forms/wizards | Formulários em etapas (wizard) |

### 5.3 Ícones

| Biblioteca | URL | Descrição |
|------------|-----|-----------|
| Heroicons Outline | http://localhost:4200/ui/icons/heroicons-outline | Ícones linha (principal) |
| Heroicons Solid | http://localhost:4200/ui/icons/heroicons-solid | Ícones preenchidos |
| Heroicons Mini | http://localhost:4200/ui/icons/heroicons-mini | Ícones pequenos |
| Material | http://localhost:4200/ui/icons/material-outline | Ícones Material Design |

---

## 6. Page Layouts Disponíveis

O Fuse oferece layouts pré-definidos para diferentes necessidades:

### 6.1 Overview

- **URL:** http://localhost:4200/ui/page-layouts/overview
- **Quando usar:** Para entender todas as opções disponíveis

### 6.2 Empty Layouts

- **URL:** http://localhost:4200/ui/page-layouts/empty/overview
- **Quando usar:** Páginas simples sem estrutura complexa

### 6.3 Carded Layouts

Layouts com card central:

| Layout | URL |
|--------|-----|
| Fullwidth | http://localhost:4200/ui/page-layouts/carded/fullwidth |
| Left Sidebar 1 | http://localhost:4200/ui/page-layouts/carded/left-sidebar-1/overview |
| Left Sidebar 2 | http://localhost:4200/ui/page-layouts/carded/left-sidebar-2/overview |
| Right Sidebar 1 | http://localhost:4200/ui/page-layouts/carded/right-sidebar-1 |
| Right Sidebar 2 | http://localhost:4200/ui/page-layouts/carded/right-sidebar-2 |

### 6.4 Simple Layouts

Layouts sem card wrapper:

| Layout | URL |
|--------|-----|
| Fullwidth 1 | http://localhost:4200/ui/page-layouts/simple/fullwidth-1/overview |
| Fullwidth 2 | http://localhost:4200/ui/page-layouts/simple/fullwidth-2/overview |
| Left Sidebar 1 | http://localhost:4200/ui/page-layouts/simple/left-sidebar-1/overview |
| Left Sidebar 2 | http://localhost:4200/ui/page-layouts/simple/left-sidebar-2/overview |
| Left Sidebar 3 | http://localhost:4200/ui/page-layouts/simple/left-sidebar-3/overview |
| Right Sidebar 1 | http://localhost:4200/ui/page-layouts/simple/right-sidebar-1/overview |
| Right Sidebar 2 | http://localhost:4200/ui/page-layouts/simple/right-sidebar-2/overview |
| Right Sidebar 3 | http://localhost:4200/ui/page-layouts/simple/right-sidebar-3/overview |

---

## 7. Regras de Padronização

### 7.1 Obrigatórias

1. **Sempre usar Transloco** para textos - nunca hardcoded
2. **Sempre usar heroicons_outline** como padrão de ícones
3. **Nunca usar max-w-screen-xl** - conteúdo deve ocupar largura total
4. **Sempre incluir estados vazios** nas listagens
5. **Sempre incluir loading states** durante carregamento
6. **Sempre usar classes Tailwind** do padrão Fuse (bg-card, text-secondary, etc.)

### 7.2 Imports Obrigatórios em Componentes

```typescript
imports: [
    CommonModule,
    RouterModule,        // Se usar routerLink
    MatButtonModule,     // Se usar mat-button
    MatIconModule,       // Se usar mat-icon
    MatTableModule,      // Se usar tabelas
    MatMenuModule,       // Se usar menus
    MatPaginatorModule,  // Se usar paginação
    TranslocoModule,     // SEMPRE - para traduções
    // ... outros conforme necessidade
]
```

### 7.3 Tamanhos de Ícones

- `icon-size-4` - Muito pequeno (breadcrumbs)
- `icon-size-5` - Padrão (botões, menus)
- `icon-size-6` - Médio (cards)
- `icon-size-8` - Grande (estados vazios)

---

## 8. Criatividade e Inteligência

Este guia estabelece padrões base, mas **é necessário ter criatividade e inteligência** para:

1. **Navegar por todas as páginas de exemplo** do Fuse
2. **Encontrar as melhores combinações** de componentes
3. **Adaptar layouts** às necessidades específicas de cada funcionalidade
4. **Manter consistência visual** enquanto cria interfaces atraentes

O Fuse oferece dezenas de variações - explore todas antes de implementar!

---

## 9. Checklist de Desenvolvimento

Antes de considerar uma tela pronta:

- [ ] Layout segue estrutura base (sem max-w-screen-xl)
- [ ] Título e subtítulo com traduções
- [ ] Campos de busca com tamanho adequado (w-56)
- [ ] Cards com bg-card e rounded-2xl
- [ ] Tabela com hover states
- [ ] Menu de ações com ícones corretos
- [ ] Estado vazio implementado
- [ ] Loading state implementado
- [ ] Paginação quando necessário
- [ ] Responsividade testada (mobile/desktop)
- [ ] Dark mode funcionando

---

## 10. Recursos Adicionais

### 10.1 Documentação

- **Changelog:** http://localhost:4200/docs/changelog
- **Guides:** http://localhost:4200/docs/guides

### 10.2 Arquivos de Estilo

- **Tema base:** `src/@fuse/styles/themes.scss`
- **Cores customizadas:** `src/@fuse/styles/user-themes.scss`
- **Tailwind config:** `src/styles/tailwind.scss`

### 10.3 Guias Relacionados

- [ERROS-COMUNS-ANGULAR.md](./ERROS-COMUNS-ANGULAR.md) - Erros de frontend a evitar
- [GUIA-DEVELOPER.md](./GUIA-DEVELOPER.md) - Guia geral de desenvolvimento
- [GUIA-TRANSLATE.md](./GUIA-TRANSLATE.md) - Internacionalização

---

**Lembre-se:** O objetivo é criar interfaces bonitas, funcionais e consistentes. Use os recursos do Fuse a seu favor!
