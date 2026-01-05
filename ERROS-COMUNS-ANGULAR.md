# 🚨 Erros Comuns em Angular e Suas Soluções

**Versão:** 1.0
**Data:** 2025-01-12
**Público:** Desenvolvedores Angular
**Origem:** Erros reais encontrados durante implementações no projeto IControlIT

---

## ⚠️ LEITURA OBRIGATÓRIA

**ANTES de começar qualquer desenvolvimento em Angular, LEIA este documento!**

Esta seção documenta **8 erros reais** encontrados durante implementações e como foram resolvidos. Usar esta referência irá **evitar horas de debugging**.

---

## 📋 Índice de Erros

1. [FuseAlertModule/FuseCardModule Não Encontrado](#-erro-1-fusealertmodulefusecardmodule-não-encontrado)
2. [Biblioteca de Tradução Incorreta](#-erro-2-biblioteca-de-tradução-incorreta)
3. [Arrow Functions em Templates Angular](#-erro-3-arrow-functions-em-templates-angular)
4. [RouterLink Não Reconhecido](#-erro-4-routerlink-não-reconhecido-em-standalone-component)
5. [mat-divider Não Reconhecido](#-erro-5-mat-divider-não-reconhecido)
6. [Type Mismatch em Parâmetros](#-erro-6-type-mismatch-em-parâmetros-de-serviço)
7. [Imports Duplicados](#-erro-7-imports-duplicados)
8. [Interface Faltando no Types](#-erro-8-interface-faltando-no-types)

---

## ❌ Erro 1: FuseAlertModule/FuseCardModule Não Encontrado

### Erro de compilação:
```
TS2305: Module '"@fuse/components/alert"' has no exported member 'FuseAlertModule'
TS2305: Module '"@fuse/components/card"' has no exported member 'FuseCardModule'
```

### Causa:
Os componentes Fuse são **Standalone Components**, não NgModules.

### ❌ Código ERRADO:
```typescript
@Component({
    standalone: true,
    imports: [
        FuseAlertModule,  // ❌ Não existe
        FuseCardModule    // ❌ Não existe
    ]
})
```

### ✅ Código CORRETO:
```typescript
@Component({
    standalone: true,
    imports: [
        FuseAlertComponent,  // ✅ Correto
        FuseCardComponent    // ✅ Correto
    ]
})
```

### Solução rápida (bash):
```bash
# Substituir em todos os arquivos TypeScript
sed -i 's/FuseAlertModule/FuseAlertComponent/g;s/FuseCardModule/FuseCardComponent/g' *.ts
```

---

## ❌ Erro 2: Biblioteca de Tradução Incorreta

### Erro de compilação:
```
TS2307: Cannot find module '@ngx-translate/core'
NG8004: No pipe found with name 'translate'
```

### Causa:
O projeto usa **@jsverse/transloco**, NÃO **@ngx-translate/core**.

### ❌ Código ERRADO:
```typescript
import { TranslateModule } from '@ngx-translate/core';  // ❌ Biblioteca errada

@Component({
    imports: [TranslateModule]  // ❌ Errado
})
```

```html
<!-- ❌ Pipe errado -->
{{ 'users.title' | translate }}
```

### ✅ Código CORRETO:
```typescript
import { TranslocoModule } from '@jsverse/transloco';  // ✅ Correto

@Component({
    imports: [TranslocoModule]  // ✅ Correto
})
```

```html
<!-- ✅ Pipe correto -->
{{ 'users.title' | transloco }}
```

### Solução rápida (bash):
```bash
# Substituir pipe nos templates HTML
find . -name "*.html" -type f -exec sed -i 's/| translate/| transloco/g' {} +

# Substituir imports nos TypeScript
find . -name "*.ts" -type f -exec sed -i "s/@ngx-translate\/core/@jsverse\/transloco/g" {} +
find . -name "*.ts" -type f -exec sed -i 's/TranslateModule/TranslocoModule/g' {} +
```

---

## ❌ Erro 3: Arrow Functions em Templates Angular

### Erro de compilação:
```
NG5002: Parser Error: Bindings cannot contain assignments at column 25 in
[{{ featureFlags.filter(f => f.flEnabled).length }}]
```

### Causa:
Templates Angular **não suportam arrow functions** diretamente.

### ❌ Código ERRADO:
```html
<!-- ❌ Arrow function em template -->
<span>{{ featureFlags.filter(f => f.flEnabled).length }}</span>
<span>{{ usuarios.map(u => u.nome).join(', ') }}</span>
```

### ✅ Código CORRETO - Opção 1: Getter (Recomendado)
```typescript
// No component.ts
export class FeatureFlagsComponent {
    featureFlags: FeatureFlag[] = [];

    // ✅ Getter em vez de arrow function
    get countFeaturesAtivas(): number {
        return this.featureFlags.filter(f => f.flEnabled).length;
    }

    get countFeaturesInativas(): number {
        return this.featureFlags.filter(f => !f.flEnabled).length;
    }
}
```

```html
<!-- ✅ Usar getter -->
<span>{{ countFeaturesAtivas }}</span>
<span>{{ countFeaturesInativas }}</span>
```

### ✅ Código CORRETO - Opção 2: Método
```typescript
// No component.ts
export class FeatureFlagsComponent {
    countAtivas(features: FeatureFlag[]): number {
        return features.filter(f => f.flEnabled).length;
    }
}
```

```html
<!-- ✅ Chamar método -->
<span>{{ countAtivas(featureFlags) }}</span>
```

### ✅ Código CORRETO - Opção 3: Pipe Customizado
```typescript
// count-filter.pipe.ts
@Pipe({ name: 'countFilter', standalone: true })
export class CountFilterPipe implements PipeTransform {
    transform(items: any[], property: string, value: any): number {
        return items.filter(item => item[property] === value).length;
    }
}
```

```html
<!-- ✅ Usar pipe -->
<span>{{ featureFlags | countFilter:'flEnabled':true }}</span>
```

---

## ❌ Erro 4: RouterLink Não Reconhecido em Standalone Component

### Erro de compilação:
```
NG8002: Can't bind to 'routerLink' since it isn't a known property of 'a'
```

### Causa:
Standalone components precisam importar **RouterModule** explicitamente para usar `routerLink`.

### ❌ Código ERRADO:
```typescript
@Component({
    standalone: true,
    imports: [
        CommonModule,
        MatButtonModule
        // ❌ Falta RouterModule
    ]
})
```

```html
<!-- ❌ routerLink não funciona -->
<a [routerLink]="['/configuracoes/lista']">Voltar</a>
```

### ✅ Código CORRETO:
```typescript
import { RouterModule } from '@angular/router';  // ✅ Importar RouterModule

@Component({
    standalone: true,
    imports: [
        CommonModule,
        RouterModule,  // ✅ Adicionar RouterModule
        MatButtonModule
    ]
})
```

```html
<!-- ✅ routerLink funciona -->
<a [routerLink]="['/configuracoes/lista']">Voltar</a>
```

---

## ❌ Erro 5: mat-divider Não Reconhecido

### Erro de compilação:
```
NG8001: 'mat-divider' is not a known element
```

### Causa:
Standalone components precisam importar **MatDividerModule** explicitamente.

### ❌ Código ERRADO:
```typescript
@Component({
    standalone: true,
    imports: [
        MatDialogModule,
        MatButtonModule
        // ❌ Falta MatDividerModule
    ]
})
```

### ✅ Código CORRETO:
```typescript
import { MatDividerModule } from '@angular/material/divider';  // ✅ Importar

@Component({
    standalone: true,
    imports: [
        MatDialogModule,
        MatButtonModule,
        MatDividerModule  // ✅ Adicionar
    ]
})
```

### Regra geral:
**Cada componente Material usado requer seu módulo importado!**

```typescript
// Imports comuns de Material
MatButtonModule      → <button mat-button>
MatIconModule        → <mat-icon>
MatFormFieldModule   → <mat-form-field>
MatInputModule       → <input matInput>
MatSelectModule      → <mat-select>
MatCheckboxModule    → <mat-checkbox>
MatRadioModule       → <mat-radio-button>
MatDialogModule      → MatDialog, mat-dialog-*
MatTableModule       → <mat-table>
MatPaginatorModule   → <mat-paginator>
MatSortModule        → matSort
MatDividerModule     → <mat-divider>
MatChipsModule       → <mat-chip>
MatTooltipModule     → [matTooltip]
MatMenuModule        → <mat-menu>
MatCardModule        → <mat-card>
```

---

## ❌ Erro 6: Type Mismatch em Parâmetros de Serviço

### Erro de compilação:
```
TS2345: Argument of type 'ImportOptions' is not assignable to parameter
of type '"Sobrescrever" | "Ignorar" | "Merge"'
```

### Causa:
Service espera um tipo literal específico, mas recebe um objeto ou tipo diferente.

### ❌ Código ERRADO:
```typescript
// Service espera: 'Sobrescrever' | 'Ignorar' | 'Merge'
// Mas recebe: { modo: 'merge', flValidar: true, ... }

const options: ImportOptions = this.form.value;
this.service.importar(file, options);  // ❌ Tipo errado
```

### ✅ Código CORRETO - Opção 1: Mapear Valores
```typescript
// Criar mapa de conversão
const modo = this.form.value.modo as 'merge' | 'replace' | 'add';

const estrategiaMap: Record<string, 'Sobrescrever' | 'Ignorar' | 'Merge'> = {
    'merge': 'Merge',
    'replace': 'Sobrescrever',
    'add': 'Ignorar'
};

// ✅ Passar valor mapeado
this.service.importar(file, estrategiaMap[modo]);
```

### ✅ Código CORRETO - Opção 2: Alterar Interface do Service
```typescript
// Se possível, alterar service para aceitar o tipo correto
export interface ImportOptions {
    estrategia: 'Sobrescrever' | 'Ignorar' | 'Merge';
    validar?: boolean;
    backup?: boolean;
}

// No service
importar(file: File, options: ImportOptions): Observable<void> {
    // ...
}
```

---

## ❌ Erro 7: Imports Duplicados

### Erro de compilação:
```
TS2300: Duplicate identifier 'FuseAlertComponent'
```

### Causa:
Script de substituição em massa adicionou imports duplicados.

### ❌ Código ERRADO:
```typescript
import { FuseAlertComponent } from '@fuse/components/alert';
import { FuseAlertComponent } from '@fuse/components/alert';  // ❌ Duplicado

@Component({
    imports: [
        FuseAlertComponent,
        FuseAlertComponent  // ❌ Duplicado
    ]
})
```

### ✅ Solução: Script PowerShell para Remover Duplicados
```powershell
# Script: remove-duplicate-imports.ps1
$dialogsPath = "D:\IC2\frontend\icontrolit-app\src\app\modules\configuracoes\dialogs"

Get-ChildItem -Path $dialogsPath -Filter "*.ts" | ForEach-Object {
    $content = Get-Content $_.FullName -Raw

    # Remove duplicate imports
    $lines = $content -split "`n"
    $uniqueLines = @()
    $seenImports = @{}

    foreach ($line in $lines) {
        if ($line -match "^import .* from") {
            if (-not $seenImports.ContainsKey($line.Trim())) {
                $uniqueLines += $line
                $seenImports[$line.Trim()] = $true
            }
        } else {
            $uniqueLines += $line
        }
    }

    $newContent = $uniqueLines -join "`n"
    Set-Content -Path $_.FullName -Value $newContent -NoNewline

    Write-Host "✅ Processado: $($_.Name)"
}
```

---

## ❌ Erro 8: Interface Faltando no Types

### Erro de compilação:
```
TS2724: '"../configuracoes.types"' has no exported member named 'ImportOptions'
```

### Causa:
Tentando importar uma interface que não existe no arquivo types.

### ✅ Solução:
```typescript
// configuracoes.types.ts

// ✅ Adicionar interface faltante
export interface ImportOptions {
    modo: 'merge' | 'replace' | 'add';
    flValidarAntesImportar?: boolean;
    flBackupAntes?: boolean;
    flNotificarUsuarios?: boolean;
}

// Outras interfaces...
export interface ExportOptions {
    formato: 'json' | 'csv' | 'yaml' | 'xml';
    categoriaId?: string;
    flIncluirCriptografados?: boolean;
    flIncluirSomenteLeitura?: boolean;
    flIncluirInativos?: boolean;
}
```

---

## ✅ Checklist: Evitando Erros em Standalone Components

Use este checklist ao criar um novo standalone component:

```typescript
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';  // ✅ 1. CommonModule (sempre)
import { RouterModule } from '@angular/router';  // ✅ 2. Se usar routerLink
import { FormsModule, ReactiveFormsModule } from '@angular/forms';  // ✅ 3. Se usar formulários

// ✅ 4. Material Modules (um para cada diretiva/componente usado)
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatDialogModule } from '@angular/material/dialog';
import { MatDividerModule } from '@angular/material/divider';
// ... outros conforme necessário

// ✅ 5. Fuse Components (não Modules!)
import { FuseCardComponent } from '@fuse/components/card';
import { FuseAlertComponent } from '@fuse/components/alert';

// ✅ 6. Transloco (não Translate!)
import { TranslocoModule } from '@jsverse/transloco';

@Component({
    selector: 'app-example',
    templateUrl: './example.component.html',
    standalone: true,  // ✅ 7. standalone: true
    imports: [
        // ✅ 8. Todos os imports acima listados aqui
        CommonModule,
        RouterModule,
        FormsModule,
        ReactiveFormsModule,
        MatButtonModule,
        MatIconModule,
        MatFormFieldModule,
        MatInputModule,
        MatDialogModule,
        MatDividerModule,
        FuseCardComponent,
        FuseAlertComponent,
        TranslocoModule
    ]
})
export class ExampleComponent {
    // ✅ 9. Getters em vez de arrow functions em templates
    get itemsAtivos(): number {
        return this.items.filter(i => i.ativo).length;
    }

    // ✅ 10. TrackBy para *ngFor
    trackById(index: number, item: any): string {
        return item.id;
    }
}
```

---

## 🎯 Dicas de Produtividade

### 1. Comandos para Verificar Erros Comuns:

```bash
# Verificar se há FuseAlertModule/FuseCardModule (devem ser Component)
grep -r "FuseAlertModule\|FuseCardModule" --include="*.ts"

# Verificar se há @ngx-translate (deve ser @jsverse/transloco)
grep -r "@ngx-translate" --include="*.ts"

# Verificar se há pipe translate (deve ser transloco)
grep -r "| translate" --include="*.html"
```

### 2. Template de Standalone Component:

```bash
# Criar novo componente já como standalone
ng generate component meu-componente --standalone
```

### 3. Conversão de NgModule para Standalone:

Se você herdou um component NgModule e precisa converter:

```typescript
// ANTES (NgModule)
@NgModule({
    declarations: [MeuComponent],
    imports: [CommonModule, MatButtonModule],
    exports: [MeuComponent]
})
export class MeuModule {}

// DEPOIS (Standalone)
@Component({
    selector: 'app-meu',
    standalone: true,
    imports: [CommonModule, MatButtonModule],
    template: '...'
})
export class MeuComponent {}
```

Atualize rotas:
```typescript
// ANTES
{
    path: 'meu',
    loadChildren: () => import('./meu/meu.module').then(m => m.MeuModule)
}

// DEPOIS
{
    path: 'meu',
    loadComponent: () => import('./meu/meu.component').then(m => m.MeuComponent)
}
```

---

## 📚 Referências

- **[GUIA-DEVELOPER.md](./GUIA-DEVELOPER.md)** - Guia completo para desenvolvedores
- **[MANUAL-DE-CODIFICACAO.md](./MANUAL-DE-CODIFICACAO.md)** - Padrões de codificação
- **[PADROES-CODIFICACAO-FRONTEND.md](./PADROES-CODIFICACAO-FRONTEND.md)** - Padrões Angular

---

## 🔄 Histórico

| Data | Descrição |
|------|-----------|
| 2025-01-12 | Extraído do MANUAL-DE-CODIFICACAO.md para documento independente |
| 2024-2025 | Erros documentados durante implementações do projeto |

---

**ÚLTIMA ATUALIZAÇÃO:** 2025-01-12
**VERSÃO:** 1.0
**SEMPRE LEIA ANTES DE DESENVOLVER EM ANGULAR!** ⚠️
