# Frontend Aditivo RFXXX - Implementar Delta no Frontend

Ele fica nesse endereço \docs\rf\Fase*\EPIC*\RF*

**Instruções:** Altere RFXXX acima para o RF desejado (ex: RF001, RF025, RF028).

---

Executar **FRONTEND ADITIVO** para o RF informado acima conforme docs/contracts/desenvolvimento/execucao/frontend-aditivo.md.
Seguir CLAUDE.md.

## 📋 PRÉ-REQUISITOS OBRIGATÓRIOS

Antes de executar este prompt, você **DEVE** ter:

1. ✅ Executado aditivo de documentação: `docs/prompts/documentacao/execucao/aditivo.md`
2. ✅ Validado aditivo de documentação: `docs/prompts/documentacao/validacao/aditivo.md` (APROVADO)
3. ✅ Executado backend aditivo: `docs/prompts/desenvolvimento/execucao/backend-aditivo.md`
4. ✅ Validado backend aditivo: `docs/contracts/desenvolvimento/validacao/backend-aditivo.md` (APROVADO)
5. ✅ Endpoints backend disponíveis
6. ✅ Branch correto: `feature/RFXXX-aditivo-*`

**Se qualquer pré-requisito falhar:**
➡️ **BLOQUEIO TOTAL**. Execute os passos anteriores primeiro.

---

## 🔄 WORKFLOW DE EXECUÇÃO

### FASE 1: ANÁLISE DE DELTA

1. **Comparar WF originais vs `_old`**
   ```bash
   diff WF-RFXXX.yaml WF-RFXXX_old.yaml
   ```

2. **Comparar UC originais vs `_old`**
   ```bash
   diff UC-RFXXX.yaml UC-RFXXX_old.yaml
   ```

3. **Ler relatórios**
   - `.temp_ia/aditivo-RFXXX-delta-report.md` (delta de documentação)
   - `.temp_ia/backend-aditivo-RFXXX-relatorio.md` (endpoints implementados)

4. **Identificar o que implementar**
   - Novos WFs → novos Components
   - Novos UCs → novas telas/formulários
   - Novos endpoints → novos Services
   - Novas chaves i18n

---

### FASE 2: IMPLEMENTAÇÃO INCREMENTAL

#### Passo 1: Criar/Atualizar Services

**Para cada novo endpoint identificado:**

Exemplo (endpoint GET /api/v1/clientes/export/pdf):
```typescript
// src/app/core/services/cliente-exportacao.service.ts
@Injectable({ providedIn: 'root' })
export class ClienteExportacaoService {
  constructor(private http: HttpClient) {}

  exportarPdf(filtros: ClienteFiltro): Observable<Blob> {
    return this.http.get('/api/v1/clientes/export/pdf', {
      params: { ...filtros },
      responseType: 'blob'
    });
  }
}
```

---

#### Passo 2: Criar Components

**Para cada WF novo identificado:**

Exemplo (WF-12: Tela de Exportação PDF):
```typescript
// src/app/features/clientes/components/exportacao-pdf/exportacao-pdf.component.ts
@Component({
  selector: 'app-cliente-exportacao-pdf',
  templateUrl: './exportacao-pdf.component.html',
  styleUrls: ['./exportacao-pdf.component.scss']
})
export class ClienteExportacaoPdfComponent implements OnInit {
  form: FormGroup;

  constructor(
    private exportacaoService: ClienteExportacaoService,
    private fb: FormBuilder
  ) {}

  ngOnInit(): void {
    this.form = this.fb.group({
      dataInicio: [null],
      dataFim: [null]
    });
  }

  exportar(): void {
    // RN-CLI-028-15: Gerar PDF com logo
    // RN-CLI-028-16: Aplicar filtros
    // RN-CLI-028-17: Validar permissão
    this.exportacaoService.exportarPdf(this.form.value).subscribe(
      (blob) => {
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `clientes-${new Date().toISOString().split('T')[0]}.pdf`;
        link.click();
      }
    );
  }
}
```

```html
<!-- exportacao-pdf.component.html -->
<div class="exportacao-pdf-container" *ixHasPermission="'cliente.export_pdf'">
  <h2>{{ 'cliente.exportacao.titulo' | translate }}</h2>

  <form [formGroup]="form" (ngSubmit)="exportar()">
    <mat-form-field>
      <mat-label>{{ 'cliente.exportacao.dataInicio' | translate }}</mat-label>
      <input matInput [matDatepicker]="pickerInicio" formControlName="dataInicio">
      <mat-datepicker-toggle matSuffix [for]="pickerInicio"></mat-datepicker-toggle>
      <mat-datepicker #pickerInicio></mat-datepicker>
    </mat-form-field>

    <mat-form-field>
      <mat-label>{{ 'cliente.exportacao.dataFim' | translate }}</mat-label>
      <input matInput [matDatepicker]="pickerFim" formControlName="dataFim">
      <mat-datepicker-toggle matSuffix [for]="pickerFim"></mat-datepicker-toggle>
      <mat-datepicker #pickerFim></mat-datepicker>
    </mat-form-field>

    <button mat-raised-button color="primary" type="submit">
      {{ 'cliente.exportacao.botaoExportar' | translate }}
    </button>
  </form>
</div>
```

---

#### Passo 3: Adicionar Routes

Adicionar em `src/app/app.routes.ts`:

```typescript
{
  path: 'clientes/exportar-pdf',
  component: ClienteExportacaoPdfComponent,
  canActivate: [PermissionGuard],
  data: { permission: 'cliente.export_pdf' }
}
```

---

#### Passo 4: Criar Forms com Validações

**Validar RNs nos formulários:**

```typescript
// Validações baseadas nas RNs
this.form = this.fb.group({
  dataInicio: [null, Validators.required], // RN-CLI-028-16
  dataFim: [null, [Validators.required, this.validarDataFimDepoisDeInicio()]]
});

validarDataFimDepoisDeInicio(): ValidatorFn {
  return (control: AbstractControl): ValidationErrors | null => {
    const dataInicio = this.form?.get('dataInicio')?.value;
    const dataFim = control.value;

    if (dataInicio && dataFim && dataFim < dataInicio) {
      return { dataFimInvalida: true };
    }

    return null;
  };
}
```

---

#### Passo 5: Atualizar i18n

Adicionar chaves em `src/assets/i18n/pt.json` e `en.json`:

```json
// pt.json
{
  "cliente": {
    "exportacao": {
      "titulo": "Exportar Clientes em PDF",
      "dataInicio": "Data Início",
      "dataFim": "Data Fim",
      "botaoExportar": "Exportar PDF"
    }
  }
}
```

```json
// en.json
{
  "cliente": {
    "exportacao": {
      "titulo": "Export Clients to PDF",
      "dataInicio": "Start Date",
      "dataFim": "End Date",
      "botaoExportar": "Export PDF"
    }
  }
}
```

---

#### Passo 6: Aplicar Permissões

**Usar `*ixHasPermission` nos componentes:**

```html
<div *ixHasPermission="'cliente.export_pdf'">
  <!-- Conteúdo visível apenas para usuários com permissão -->
</div>
```

---

#### Passo 7: Criar Testes

**Para cada componente novo:**

```typescript
// exportacao-pdf.component.spec.ts
describe('ClienteExportacaoPdfComponent', () => {
  let component: ClienteExportacaoPdfComponent;
  let fixture: ComponentFixture<ClienteExportacaoPdfComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ClienteExportacaoPdfComponent]
    }).compileComponents();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should call exportacaoService.exportarPdf when exportar is called', () => {
    const exportarPdfSpy = spyOn(component['exportacaoService'], 'exportarPdf').and.returnValue(of(new Blob()));
    component.exportar();
    expect(exportarPdfSpy).toHaveBeenCalled();
  });

  it('should validate dataFim is after dataInicio', () => {
    component.form.patchValue({
      dataInicio: new Date('2026-01-10'),
      dataFim: new Date('2026-01-05')
    });
    expect(component.form.get('dataFim')?.hasError('dataFimInvalida')).toBe(true);
  });
});
```

---

### FASE 3: VALIDAÇÃO E BUILD

#### Passo 8: Build

```bash
cd frontend/icontrolit-app
npm run build
```

**Resultado esperado:** ✅ Build PASS (0 erros)

---

#### Passo 9: Executar Testes

```bash
npm run test
```

**Resultado esperado:** ✅ Testes PASS (100%)

---

#### Passo 10: Verificar Funcionamento (manual)

```bash
npm start
```

Abrir `http://localhost:4200` e testar:
- Acesso à rota `/clientes/exportar-pdf`
- Permissão aplicada
- Formulário validando corretamente
- Exportação funcionando

---

### FASE 4: RELATÓRIO

#### Passo 11: Gerar Relatório

Criar `.temp_ia/frontend-aditivo-RFXXX-relatorio.md`:

```markdown
# RELATÓRIO DE IMPLEMENTAÇÃO - FRONTEND ADITIVO RFXXX

**Data:** YYYY-MM-DD
**RF:** RFXXX
**Funcionalidade:** [Nome da funcionalidade adicionada]

---

## DELTA IMPLEMENTADO

### Services
- ✅ ClienteExportacaoService (método exportarPdf)

### Components
- ✅ ClienteExportacaoPdfComponent

### Routes
- ✅ `/clientes/exportar-pdf`

### Forms
- ✅ Formulário de exportação com validações (RN-CLI-028-16)

### i18n
- ✅ 5 chaves adicionadas (pt.json, en.json)

### Permissions
- ✅ `*ixHasPermission="'cliente.export_pdf'"` aplicado

### Tests
- ✅ 12 testes criados (exportacao-pdf.component.spec.ts)

---

## VALIDAÇÕES

- ✅ Build: PASS (0 erros)
- ✅ Testes: 12/12 PASS (100%)
- ✅ Funcionamento manual: PASS

---

## VEREDICTO FINAL

✅ **FRONTEND ADITIVO IMPLEMENTADO COM SUCESSO**

Todos os itens do delta foram implementados com sucesso.
Build, testes e funcionamento manual passaram sem erros.
```

---

## ✅ CRITÉRIOS DE APROVAÇÃO

**APROVADO:**
- ✅ Build PASS (0 erros)
- ✅ Testes PASS (100%)
- ✅ Relatório completo

**REPROVADO:**
- ❌ Build FAIL
- ❌ Qualquer teste FAIL
- ❌ Relatório incompleto

---

## 🚨 REGRAS IMPORTANTES

- **SEMPRE** comparar WF/UC originais vs `_old`
- **SEMPRE** criar componentes para TODOS os WFs novos
- **SEMPRE** adicionar chaves i18n
- **SEMPRE** aplicar permissões (RBAC)
- **SEMPRE** criar testes unitários
- **SEMPRE** garantir build e testes PASS

---

## 🔄 PRÓXIMOS PASSOS

**Após aprovação deste prompt:**
1. Executar validação frontend: `docs/contracts/desenvolvimento/validacao/frontend-aditivo.md`
2. Se aprovado: Commit e merge
3. Executar testes E2E completos

---

**Contrato:** docs/contracts/desenvolvimento/execucao/frontend-aditivo.md
**Modo:** Governança rígida
**Aprovação:** Build PASS + Testes PASS + Relatório completo
