# Wireframes - RF036

**Versao:** 1.0
**Data:** 18/12/2025
**RF Relacionado:** [RF036 - Gestão de Custos Fixos](./RF036.md)
**UC Relacionado:** [UC-RF036](./UC-RF036.md)
**Plataforma:** Web (Desktop)
**Framework UI:** Fuse Angular Admin Template

---

## Nota Fuse

Wireframes mostram APENAS a área de conteúdo (header/sidebar/footer são do Fuse).

---

## Legenda

```
[Botão]  ☑ Check  [___] Input  +  ×  ✓  ●
```

---

## Navegação

```
[Tela 01 - Listagem] ─┬─→ [Modal Criar]
                      ├─→ [Tela 02 - Visualizar]
                      ├─→ [Tela 03 - Rateio]
                      └─→ [Tela 04 - Projeção]
```

---

## Tela 01 - Listagem

### UC00 - Listar Custos Fixos

```
┌────────────────────────────────────────────┐
│ Home > Gestão > Custos Fixos  [+ Novo]    │
│                                            │
│ Filtros: [Categoria ▼] [Fornecedor ▼]    │
│ [🔍 Buscar_____________]                   │
│                                            │
│ 23 custos  [Importar] [Exportar] [Dash]   │
│                                            │
│ Nome        │Categoria│Valor   │Status    │
│ Aluguel SP  │Aluguel  │R$ 45k  │● Ativo   │
│  Imobiliária XYZ │ Jan/25-Dez/25          │
│  [👁️] [✏️] [Rateio]                        │
│                                            │
│ KPIs: Total R$ 156k │ Maior R$ 45k        │
│                                            │
└────────────────────────────────────────────┘
```

---

## Tela 02 - Visualizar

### UC02 - Visualizar Custo Fixo

```
┌────────────────────────────────────────────┐
│ Home > Custos Fixos > Aluguel  [← Voltar] │
│                                            │
│ Aluguel SP                [✏️] [🗑️]        │
│                                            │
│ [● Resumo] [Histórico] [Rateio]           │
│                                            │
│ Nome:         Aluguel SP                   │
│ Categoria:    Aluguel                      │
│ Fornecedor:   Imobiliária XYZ              │
│ Status:       ● Ativo                      │
│                                            │
│ Valor Mensal:    R$ 45.000,00              │
│ Periodicidade:   Mensal                    │
│ Vigência:        01/01/2025 a 31/12/2025   │
│                                            │
│ Rateio (3 departamentos):                  │
│ • Administrativo: 50% (R$ 22.500)          │
│ • TI:             30% (R$ 13.500)          │
│ • Comercial:      20% (R$  9.000)          │
│ [Editar Rateio]                            │
│                                            │
│ Projeção Anual: R$ 540.000,00              │
│ [Ver Projeção Detalhada]                   │
│                                            │
└────────────────────────────────────────────┘
```

---

## Tela 03 - Rateio

### UC06 - Calcular Rateio

```
┌────────────────────────────────────────────┐
│ Home > Custos > Rateio       [← Voltar]   │
│                                            │
│ Rateio - Aluguel SP                        │
│ Valor Total: R$ 45.000,00                  │
│                                            │
│ ☑ Habilitar Rateio                         │
│ ◉ Por Departamento ○ Centro Custo          │
│                                            │
│ Departamento     │% Rateio│Valor          │
│ Administrativo   │ [50%]  │R$ 22.500      │
│ TI               │ [30%]  │R$ 13.500      │
│ Comercial        │ [20%]  │R$  9.000      │
│ TOTAL            │ 100% ✓ │R$ 45.000      │
│                                            │
│ [Gráfico Pizza]                            │
│                                            │
│ [+ Adicionar]                              │
│                                            │
│ [Cancelar] [Salvar Template] [Aplicar]    │
│                                            │
└────────────────────────────────────────────┘
```

---

## Tela 04 - Projeção

### UC08 - Projetar Custos Futuros

```
┌────────────────────────────────────────────┐
│ Home > Custos > Projeção     [← Voltar]   │
│                                            │
│ Projeção 12 Meses                          │
│                                            │
│ Período: [01/2025 ▼] a [12/2025 ▼]        │
│ ☑ Todas categorias                         │
│ ☑ IPCA (4.5%) ☑ IGP-M (3.8%)               │
│ [Calcular]                                 │
│                                            │
│ Total 12 meses:    R$ 1.876.800            │
│ Média mensal:      R$   156.400            │
│ Pago (Jan-Mar):    R$   469.200 (25%)      │
│ Restante:          R$ 1.407.600 (75%)      │
│                                            │
│ Mês│Base   │Reajuste│Total  │Status       │
│ Jan│156.4k │    0   │156.4k │✓ Realizado  │
│ Fev│156.4k │    0   │156.4k │✓ Realizado  │
│ Mar│156.4k │    0   │156.4k │✓ Realizado  │
│ Abr│156.4k │    0   │156.4k │○ Projetado  │
│ Jul│156.4k │ 7.2k ⚠ │163.6k │○ Reajuste   │
│                                            │
│ [Gráfico Evolução Mensal]                  │
│                                            │
│ [Exportar Excel] [Exportar PDF]            │
│                                            │
└────────────────────────────────────────────┘
```

---

## Modal - Criar

```
┌───────────────────────────┐
│ Novo Custo Fixo      [×]  │
├───────────────────────────┤
│ Nome * [______________]   │
│ Categoria * [Select ▼]    │
│ Valor * R$ [________]     │
│ Periodicidade *           │
│ ◉ Mensal ○ Anual          │
│ Vigência *                │
│ De: [01/01/25 ▼]          │
│ Até: [31/12/25 ▼]         │
│ Fornecedor [Select ▼]     │
│ ☐ Habilitar Rateio        │
├───────────────────────────┤
│ [Cancelar]     [Salvar]   │
└───────────────────────────┘
```

---

## Modal - Importar

```
┌───────────────────────────┐
│ Importar Lote        [×]  │
├───────────────────────────┤
│ Passo 1/3 [███░░░] 33%    │
│                           │
│ ┌───────────────────────┐ │
│ │ 📤 Arraste aqui ou    │ │
│ │ [Clique p/ selecionar]│ │
│ │ CSV, XLSX (max 1k)    │ │
│ └───────────────────────┘ │
│                           │
│ ✓ custos_2025.xlsx (120KB)│
│                           │
│ [📥 Baixar Template]      │
│                           │
│ Colunas obrigatórias:     │
│ • Nome • Categoria        │
│ • Valor • Periodicidade   │
├───────────────────────────┤
│ [Cancelar]   [Próximo →]  │
└───────────────────────────┘
```

---

## Modal - Confirmação

```
┌───────────────────────────┐
│ Confirmar Inativação [×]  │
├───────────────────────────┤
│ ⚠️ Deseja inativar?        │
│                           │
│ • Aluguel SP              │
│ • R$ 45.000/mês           │
│                           │
│ Efeitos:                  │
│ • Para geração automática │
│ • Mantém histórico        │
│ • Pode reativar           │
│                           │
│ Motivo: [___________]     │
├───────────────────────────┤
│ [Cancelar] [Sim, Inativar]│
└───────────────────────────┘
```

---

## Estados

### Loading
```
⏳ Carregando custos...
[████████░░░░] 65%
```

### Vazio
```
📭 Nenhum custo cadastrado
[+ Cadastrar Primeiro]
```

### Erro
```
✗ Erro ao carregar
[Tentar Novamente]
```

---

## Toasts

```
✓ Custo fixo salvo!
✗ Erro: Soma ≠ 100%
⚠ Vigência próxima (30d)
```

---

## Notas Técnicas

- **Framework:** Angular 19 Standalone
- **UI:** Fuse + Angular Material 19
- **Gráficos:** ApexCharts
- **RNs:** RN-036-001 a RN-036-008

---

## Histórico

| Versão | Data | Descrição |
|--------|------|-----------|
| 1.0 | 18/12/2025 | Criação concisa - 4 telas + 4 modais |
