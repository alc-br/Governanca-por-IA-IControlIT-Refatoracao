/**
 * TEMPLATE PADRÃO PARA CONFIGURAÇÃO DE TESTBED
 *
 * Versão: 1.0
 * Data: 2026-01-10
 * Contexto: Criado após análise do RF006 onde 1 problema (2%) foi causado por TestBed
 *           incompleto - falta de providers para HttpClient, Router, FUSE_CONFIG
 *
 * **Quando usar este template:**
 * - TODOS os testes unitários de componentes Angular
 * - Testes que injetam services (HttpClient, Router, etc.)
 * - Testes que usam bibliotecas externas (Transloco, Material, etc.)
 *
 * **Problema que resolve:**
 * - `NullInjectorError: No provider for HttpClient`
 * - `NullInjectorError: No provider for FUSE_APP_CONFIG`
 * - `TypeError: this.router.serializeUrl is not a function`
 *
 * **Referências:**
 * - ANALISE-GAPS-GOVERNANCA-RF006-COMPLETA.md → GAP 5
 * - CONVENTIONS.md → seção 6.X (Convenções de Testes) - ADICIONAR
 */

import { ComponentFixture, TestBed } from '@angular/core/testing';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { provideHttpClient } from '@angular/common/http';
import { provideRouter, Router } from '@angular/router';
import { provideAnimations } from '@angular/platform-browser/animations';
import { TranslocoTestingModule } from '@ngneat/transloco';

// =============================================
// EXEMPLO DE USO COMPLETO
// =============================================

describe('MeuComponente', () => {
  let component: MeuComponente;
  let fixture: ComponentFixture<MeuComponente>;
  let httpMock: HttpTestingController;
  let router: Router;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      // ===== COMPONENTE TESTADO (Standalone) =====
      imports: [
        MeuComponente,  // Componente standalone deve estar em imports, não declarations
      ],

      // ===== PROVIDERS OBRIGATÓRIOS =====
      providers: [
        // HTTP
        provideHttpClient(),
        provideHttpClientTesting(),

        // ROUTER
        provideRouter([]),  // Rotas vazias para testes

        // ANIMAÇÕES (desabilitar para testes mais rápidos)
        provideAnimations(),

        // FUSE CONFIG (se aplicável - projeto IControlIT)
        {
          provide: 'FUSE_APP_CONFIG',
          useValue: {
            layout: 'classic',
            theme: 'theme-default'
          }
        },

        // SERVICES MOCKADOS (se necessário)
        // Exemplo de mock de service customizado:
        // {
        //   provide: MeuService,
        //   useValue: {
        //     getData: jasmine.createSpy('getData').and.returnValue(of([]))
        //   }
        // }
      ]
    }).compileComponents();

    // Injetar dependências necessárias
    httpMock = TestBed.inject(HttpTestingController);
    router = TestBed.inject(Router);

    // Criar componente
    fixture = TestBed.createComponent(MeuComponente);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  afterEach(() => {
    // Validar que não há requisições HTTP pendentes
    httpMock.verify();
  });

  it('deve criar o componente', () => {
    expect(component).toBeTruthy();
  });

  // Mais testes aqui...
});

// =============================================
// TEMPLATE MÍNIMO (SEM HTTP/ROUTER)
// =============================================

/**
 * Use este template se o componente NÃO usa:
 * - HttpClient
 * - Router
 * - FUSE_CONFIG
 */
/*
describe('ComponenteSimples', () => {
  let component: ComponenteSimples;
  let fixture: ComponentFixture<ComponenteSimples>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ComponenteSimples],
      providers: [provideAnimations()]
    }).compileComponents();

    fixture = TestBed.createComponent(ComponenteSimples);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('deve criar o componente', () => {
    expect(component).toBeTruthy();
  });
});
*/

// =============================================
// TEMPLATE COM TRANSLOCO (TRADUÇÕES)
// =============================================

/**
 * Use este template se o componente usa:
 * - TranslocoService
 * - Pipes de tradução (transloco)
 */
/*
import translations from '../../../assets/i18n/pt-BR.json';
import translationsEn from '../../../assets/i18n/en.json';

describe('ComponenteComTraducao', () => {
  let component: ComponenteComTraducao;
  let fixture: ComponentFixture<ComponenteComTraducao>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [
        ComponenteComTraducao,
        TranslocoTestingModule.forRoot({
          langs: { 'pt-BR': translations, 'en': translationsEn },
          translocoConfig: {
            availableLangs: ['pt-BR', 'en'],
            defaultLang: 'pt-BR'
          }
        })
      ],
      providers: [provideAnimations()]
    }).compileComponents();

    fixture = TestBed.createComponent(ComponenteComTraducao);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('deve traduzir textos corretamente', () => {
    const compiled = fixture.nativeElement;
    expect(compiled.querySelector('h1').textContent).toContain('Bem-vindo');
  });
});
*/

// =============================================
// TEMPLATE COM MOCK DE SERVICE COMPLEXO
// =============================================

/**
 * Use este template se o componente usa:
 * - Services customizados que precisam ser mockados
 * - Comportamentos complexos de services
 */
/*
describe('ComponenteComService', () => {
  let component: ComponenteComService;
  let fixture: ComponentFixture<ComponenteComService>;
  let mockClienteService: jasmine.SpyObj<ClienteService>;

  beforeEach(async () => {
    // Criar mock do service com spies para todos os métodos
    mockClienteService = jasmine.createSpyObj('ClienteService', [
      'getClientes',
      'getClienteById',
      'createCliente',
      'updateCliente',
      'deleteCliente'
    ]);

    // Definir comportamento padrão dos mocks
    mockClienteService.getClientes.and.returnValue(of([
      { id: '1', razaoSocial: 'Cliente Teste' }
    ]));
    mockClienteService.getClienteById.and.returnValue(of(
      { id: '1', razaoSocial: 'Cliente Teste' }
    ));
    mockClienteService.createCliente.and.returnValue(of(
      { id: '2', razaoSocial: 'Novo Cliente' }
    ));
    mockClienteService.updateCliente.and.returnValue(of(
      { id: '1', razaoSocial: 'Cliente Atualizado' }
    ));
    mockClienteService.deleteCliente.and.returnValue(of(void 0));

    await TestBed.configureTestingModule({
      imports: [ComponenteComService],
      providers: [
        provideAnimations(),
        { provide: ClienteService, useValue: mockClienteService }
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(ComponenteComService);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('deve carregar clientes ao inicializar', () => {
    expect(mockClienteService.getClientes).toHaveBeenCalled();
    expect(component.clientes.length).toBe(1);
  });

  it('deve criar novo cliente', () => {
    const novoCliente = { razaoSocial: 'Novo Cliente' };
    component.salvar(novoCliente);

    expect(mockClienteService.createCliente).toHaveBeenCalledWith(novoCliente);
  });
});
*/

// =============================================
// TEMPLATE COM MATERIAL DIALOG
// =============================================

/**
 * Use este template se o componente usa:
 * - MatDialog
 * - MatDialogRef
 * - MAT_DIALOG_DATA
 */
/*
import { MatDialogModule, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';

describe('ComponenteComDialog', () => {
  let component: ComponenteComDialog;
  let fixture: ComponentFixture<ComponenteComDialog>;
  let mockDialogRef: jasmine.SpyObj<MatDialogRef<ComponenteComDialog>>;

  beforeEach(async () => {
    mockDialogRef = jasmine.createSpyObj('MatDialogRef', ['close']);

    await TestBed.configureTestingModule({
      imports: [
        ComponenteComDialog,
        MatDialogModule
      ],
      providers: [
        provideAnimations(),
        { provide: MatDialogRef, useValue: mockDialogRef },
        { provide: MAT_DIALOG_DATA, useValue: { id: '1', nome: 'Teste' } }
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(ComponenteComDialog);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('deve fechar dialog ao confirmar', () => {
    component.confirmar();
    expect(mockDialogRef.close).toHaveBeenCalledWith(true);
  });

  it('deve fechar dialog ao cancelar', () => {
    component.cancelar();
    expect(mockDialogRef.close).toHaveBeenCalledWith(false);
  });
});
*/

// =============================================
// TEMPLATE COM REACTIVE FORMS (FormBuilder)
// =============================================

/**
 * Use este template se o componente usa:
 * - FormBuilder
 * - FormGroup
 * - Validators
 */
/*
import { ReactiveFormsModule, FormBuilder } from '@angular/forms';

describe('ComponenteComForm', () => {
  let component: ComponenteComForm;
  let fixture: ComponentFixture<ComponenteComForm>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [
        ComponenteComForm,
        ReactiveFormsModule
      ],
      providers: [
        provideAnimations(),
        FormBuilder
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(ComponenteComForm);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('deve invalidar form quando campo obrigatório vazio', () => {
    component.form.patchValue({ razaoSocial: '' });
    expect(component.form.get('razaoSocial')?.hasError('required')).toBe(true);
  });

  it('deve validar form quando todos campos preenchidos', () => {
    component.form.patchValue({
      razaoSocial: 'Cliente Teste',
      cnpj: '12345678000199'
    });
    expect(component.form.valid).toBe(true);
  });
});
*/

// =============================================
// CHECKLIST DE CONFIGURAÇÃO TESTBED
// =============================================

/**
 * Use esta checklist para garantir que seu TestBed está completo:
 *
 * [ ] Componente standalone está em `imports` (não `declarations`)
 * [ ] provideHttpClient() e provideHttpClientTesting() se usa HttpClient
 * [ ] provideRouter([]) se usa Router
 * [ ] provideAnimations() para evitar erros de animação
 * [ ] FUSE_APP_CONFIG se componente usa FUSE (projeto IControlIT)
 * [ ] TranslocoTestingModule se componente usa traduções
 * [ ] Services customizados mockados se necessário
 * [ ] MatDialogRef e MAT_DIALOG_DATA se componente é dialog
 * [ ] FormBuilder se componente usa Reactive Forms
 * [ ] httpMock.verify() no afterEach() se usa HttpClient
 *
 * **ATENÇÃO:**
 * - NÃO importar `HttpClientModule` diretamente (deprecated em Angular 18)
 * - NÃO importar `BrowserAnimationsModule` (usar provideAnimations())
 * - NÃO usar `declarations` em TestBed (componentes standalone usam imports)
 */

// =============================================
// PROVIDERS COMUNS - REFERÊNCIA RÁPIDA
// =============================================

/**
 * HTTP:
 * - provideHttpClient()
 * - provideHttpClientTesting()
 * - httpMock = TestBed.inject(HttpTestingController)
 *
 * ROUTER:
 * - provideRouter([])
 * - router = TestBed.inject(Router)
 *
 * ANIMAÇÕES:
 * - provideAnimations()
 * - OU: provideNoopAnimations() (para testes sem animação)
 *
 * FUSE CONFIG:
 * - { provide: 'FUSE_APP_CONFIG', useValue: { ... } }
 *
 * TRANSLOCO:
 * - TranslocoTestingModule.forRoot({ ... })
 *
 * MATERIAL DIALOG:
 * - { provide: MatDialogRef, useValue: mockDialogRef }
 * - { provide: MAT_DIALOG_DATA, useValue: { ... } }
 *
 * REACTIVE FORMS:
 * - ReactiveFormsModule (em imports)
 * - FormBuilder (em providers)
 */

// =============================================
// ERROS COMUNS E SOLUÇÕES
// =============================================

/**
 * ERRO: "NullInjectorError: No provider for HttpClient"
 * SOLUÇÃO: Adicionar provideHttpClient() e provideHttpClientTesting() em providers
 *
 * ERRO: "NullInjectorError: No provider for FUSE_APP_CONFIG"
 * SOLUÇÃO: Adicionar { provide: 'FUSE_APP_CONFIG', useValue: { layout: 'classic' } }
 *
 * ERRO: "TypeError: this.router.serializeUrl is not a function"
 * SOLUÇÃO: Adicionar provideRouter([]) em providers
 *
 * ERRO: "Can't resolve all parameters for Component: (?)"
 * SOLUÇÃO: Verificar se todos os services injetados estão mockados/provided
 *
 * ERRO: "Expected one matching request for criteria ..., found none"
 * SOLUÇÃO: Verificar se httpMock.expectOne(...).flush(...) está correto
 *
 * ERRO: "Expected spy [methodName] to have been called"
 * SOLUÇÃO: Verificar se o método realmente foi chamado ou se o spy está configurado
 *
 * ERRO: "Component is not standalone"
 * SOLUÇÃO: Usar `imports: [Component]` em vez de `declarations: [Component]`
 */

// =============================================
// REFERÊNCIAS CRUZADAS
// =============================================

/**
 * Documentos relacionados:
 * - CONVENTIONS.md → seção 6 "Convenções de Testes" (ADICIONAR)
 * - base-conhecimento/frontend.yaml → seção testes_falhando
 * - ANALISE-GAPS-GOVERNANCA-RF006-COMPLETA.md → GAP 5 (Mocks TestBed)
 *
 * Comandos úteis:
 * - npm test                    → Executar todos os testes
 * - npm test -- ComponenteName  → Executar testes de um componente específico
 * - npm test -- --coverage      → Gerar relatório de cobertura
 */

export {};  // Tornar este arquivo um módulo TypeScript válido
