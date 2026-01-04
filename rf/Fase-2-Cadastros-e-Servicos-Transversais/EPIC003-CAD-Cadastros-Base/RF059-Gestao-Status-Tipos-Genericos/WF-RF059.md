# WF-RF059 - Wireframes - Gestão de Status e Tipos Genéricos

**Versão:** 1.0
**Data:** 2025-12-18
**RF:** [RF059 - Gestão de Status e Tipos Genéricos](./RF059.md)
**Template UI:** Fuse Admin (Angular Material 19)

---

## 1. TELA: Listagem de Domínios (UC00)

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ ☰ Menu               IControlIT v2 - Gestão de Status e Tipos Genéricos                🔔 👤 Admin    │
├─────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                         │
│  ⚙️ Configurações > Status e Tipos Genéricos                                                           │
│                                                                                                         │
│  ┌───────────────────────────────────────────────────────────────────────────────────────────────────┐ │
│  │  Domínios Parametrizáveis - Gestão Centralizada de Tipos e Status                                 │ │
│  │                                                                                                     │ │
│  │  ╔═══════════════════════════════════════════════════════════════════════════════════════════════╗ │ │
│  │  ║ 📊 VISÃO GERAL DOS DOMÍNIOS                                                                  ║ │ │
│  │  ╠═══════════════════════════════════════════════════════════════════════════════════════════════╣ │ │
│  │  ║                                                                                               ║ │ │
│  │  ║  📋 TOTAL DOMÍNIOS     🔧 CUSTOMIZÁVEIS      🔒 SISTEMA          ✅ ITENS ATIVOS              ║ │ │
│  │  ║  ┌────────────────┐    ┌────────────────┐    ┌───────────────┐   ┌──────────────┐           ║ │ │
│  │  ║  │      42        │    │      28        │    │      14       │   │     856      │           ║ │ │
│  │  ║  │  domínios      │    │  67%           │    │  33%          │   │  itens       │           ║ │ │
│  │  ║  └────────────────┘    └────────────────┘    └───────────────┘   └──────────────┘           ║ │ │
│  │  ║                                                                                               ║ │ │
│  │  ║  🔄 ÚLTIMA ATUALIZAÇÃO: 18/12/2025 14:30  |  👤 Admin User  |  ⚡ Cache: 99,8% hit rate      ║ │ │
│  │  ╚═══════════════════════════════════════════════════════════════════════════════════════════════╝ │ │
│  │                                                                                                     │ │
│  │  ┌─────────────────────────────────────────────────────────────────────────────────────────────┐   │ │
│  │  │ FILTROS                                                                                      │   │ │
│  │  ├─────────────────────────────────────────────────────────────────────────────────────────────┤   │ │
│  │  │                                                                                               │   │ │
│  │  │  🔍 Pesquisar domínio...              [Categoria ▼] [Tipo ▼]      [Status ▼]    [Limpar]    │   │ │
│  │  │  ┌──────────────────────────────┐                                                            │   │ │
│  │  │  │ STATUS                       │     ◉ Todas       ◉ Todos       ◉ Todos                    │   │ │
│  │  │  └──────────────────────────────┘     ○ Chamados    ○ Sistema     ○ Ativos                   │   │ │
│  │  │                                        ○ Ativos      ○ Customiz.  ○ Inativos                 │   │ │
│  │  │  ☑ Exibir apenas customizáveis        ○ Financeiro  ○ Global                                │   │ │
│  │  │  ☑ Mostrar workflows visuais          ○ Projetos                                             │   │ │
│  │  │                                                                                               │   │ │
│  │  └─────────────────────────────────────────────────────────────────────────────────────────────┘   │ │
│  │                                                                                                     │ │
│  │  [+ Novo Domínio]  [📥 Importar Config]  [📤 Exportar Config]  [🔄 Limpar Cache]  [⚙️ Avançado] │ │
│  │                                                                                                     │ │
│  │  ┌───────────────────────────────────────────────────────────────────────────────────────────────┐ │ │
│  │  │ DOMÍNIOS PARAMETRIZÁVEIS                                      42 domínios | 28 customizáveis  │ │ │
│  │  ├───┬────────────────────┬────────────────┬──────────┬──────────┬──────────┬──────────┬────────┤ │ │
│  │  │ ⭐ │   CÓDIGO           │  NOME          │ CATEGORIA│  ITENS   │   TIPO   │  STATUS  │ AÇÕES  │ │ │
│  │  ├───┼────────────────────┼────────────────┼──────────┼──────────┼──────────┼──────────┼────────┤ │ │
│  │  │ ⭐ │ STATUS_CHAMADO     │Status Chamado  │📞 Chamados│   8     │🔧 Custom │🟢 Ativo  │ 👁️ ✏️ 🔄│ │ │
│  │  │   │                    │                │          │ ativos   │          │          │        │ │ │
│  │  │   │                    │                │          │ 1.234 usos│         │          │        │ │ │
│  │  ├───┼────────────────────┼────────────────┼──────────┼──────────┼──────────┼──────────┼────────┤ │ │
│  │  │   │ PRIORIDADE         │Prioridade      │📞 Chamados│   5     │🔒 Sistema│🟢 Ativo  │ 👁️ 🔄  │ │ │
│  │  │   │                    │                │          │ ativos   │          │          │        │ │ │
│  │  │   │                    │                │          │   892 usos│         │          │        │ │ │
│  │  ├───┼────────────────────┼────────────────┼──────────┼──────────┼──────────┼──────────┼────────┤ │ │
│  │  │ ⭐ │ TIPO_ATIVO         │Tipo de Ativo   │💻 Ativos │  15     │🔧 Custom │🟢 Ativo  │ 👁️ ✏️ 🔄│ │ │
│  │  │   │                    │                │          │ ativos   │          │          │        │ │ │
│  │  │   │                    │                │          │ 3.456 usos│         │          │        │ │ │
│  │  ├───┼────────────────────┼────────────────┼──────────┼──────────┼──────────┼──────────┼────────┤ │ │
│  │  │ ⭐ │ STATUS_FATURA      │Status Fatura   │💰 Financeiro│  6   │🔧 Custom │🟢 Ativo  │ 👁️ ✏️ 🔄│ │ │
│  │  │   │                    │                │          │ ativos   │          │          │        │ │ │
│  │  │   │                    │                │          │   567 usos│         │          │        │ │ │
│  │  ├───┼────────────────────┼────────────────┼──────────┼──────────┼──────────┼──────────┼────────┤ │ │
│  │  │   │ CATEGORIA_DESPESA  │Cat. Despesa    │💰 Financeiro│ 12   │🔧 Custom │🟢 Ativo  │ 👁️ ✏️ 🔄│ │ │
│  │  │   │                    │                │          │ ativos   │          │          │        │ │ │
│  │  │   │                    │                │          │   789 usos│         │          │        │ │ │
│  │  ├───┼────────────────────┼────────────────┼──────────┼──────────┼──────────┼──────────┼────────┤ │ │
│  │  │ ⭐ │ TIPO_PROJETO       │Tipo Projeto    │📊 Projetos│   4    │🔧 Custom │🟢 Ativo  │ 👁️ ✏️ 🔄│ │ │
│  │  │   │                    │                │          │ ativos   │          │          │        │ │ │
│  │  │   │                    │                │          │   123 usos│         │          │        │ │ │
│  │  ├───┼────────────────────┼────────────────┼──────────┼──────────┼──────────┼──────────┼────────┤ │ │
│  │  │   │ STATUS_CONTRATO    │Status Contrato │📋 Contratos│  7    │🔒 Sistema│🟢 Ativo  │ 👁️ 🔄  │ │ │
│  │  │   │                    │                │          │ ativos   │          │          │        │ │ │
│  │  │   │                    │                │          │   456 usos│         │          │        │ │ │
│  │  ├───┼────────────────────┼────────────────┼──────────┼──────────┼──────────┼──────────┼────────┤ │ │
│  │  │ ⭐ │ TIPO_SOLICITACAO   │Tipo Solicitação│📞 Chamados│  10    │🔧 Custom │🟢 Ativo  │ 👁️ ✏️ 🔄│ │ │
│  │  │   │                    │                │          │ ativos   │          │          │        │ │ │
│  │  │   │                    │                │          │ 2.345 usos│         │          │        │ │ │
│  │  ├───┼────────────────────┼────────────────┼──────────┼──────────┼──────────┼──────────┼────────┤ │ │
│  │  │   │ IDIOMA_SISTEMA     │Idiomas Sistema │⚙️ Sistema │   3    │🔒 Sistema│🟢 Ativo  │ 👁️      │ │ │
│  │  │   │                    │                │          │ ativos   │          │          │        │ │ │
│  │  │   │                    │                │          │    15 usos│         │          │        │ │ │
│  │  ├───┼────────────────────┼────────────────┼──────────┼──────────┼──────────┼──────────┼────────┤ │ │
│  │  │ ⭐ │ MOTIVO_RECUSA      │Motivo Recusa   │💰 Financeiro│  8   │🔧 Custom │🟢 Ativo  │ 👁️ ✏️ 🔄│ │ │
│  │  │   │                    │                │          │ ativos   │          │          │        │ │ │
│  │  │   │                    │                │          │   234 usos│         │          │        │ │ │
│  │  └───┴────────────────────┴────────────────┴──────────┴──────────┴──────────┴──────────┴────────┘ │ │
│  │                                                                                                     │ │
│  │  ◀️ Anterior  [1] 2 3 4 5  Próximo ▶️                          [10 ▼] itens por página            │ │
│  │                                                                                                     │ │
│  │  💡 LEGENDA: ⭐ = Possui transições de workflow | 🔧 = Customizável | 🔒 = Apenas Sistema          │ │
│  │                                                                                                     │ │
│  └─────────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                         │
│  ┌───────────────────────────────────────────────────────────────────────────────────────────────────┐ │
│  │ 📈 ANÁLISES RÁPIDAS                                                                                │ │
│  ├───────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│  │                                                                                                     │ │
│  │  DOMÍNIOS MAIS USADOS             ÚLTIMAS MODIFICAÇÕES            CACHE PERFORMANCE                │ │
│  │  ┌──────────────────────────┐     ┌──────────────────────────┐    ┌────────────────────────────┐ │ │
│  │  │ 1. TIPO_ATIVO   3.456    │     │ 18/12 STATUS_CHAMADO     │    │ Hit Rate:    99,8%         │ │ │
│  │  │ 2. TIPO_SOLICITACAO 2.345│     │ 17/12 PRIORIDADE         │    │ Misses:      12            │ │ │
│  │  │ 3. STATUS_CHAMADO 1.234  │     │ 15/12 TIPO_ATIVO         │    │ Invalidações: 3            │ │ │
│  │  │ 4. STATUS_FATURA 567     │     │ 12/12 MOTIVO_RECUSA      │    │ Memória:     2,3 MB        │ │ │
│  │  │ 5. PRIORIDADE 892        │     │ [Ver Todas]              │    │ [Limpar Agora]             │ │ │
│  │  │ [Ver Ranking Completo]   │     │                          │    │                            │ │ │
│  │  └──────────────────────────┘     └──────────────────────────┘    └────────────────────────────┘ │ │
│  └───────────────────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

**Componentes Fuse:**
- `fuse-card` - Cards de resumo
- `mat-table` - Grid de domínios
- `mat-form-field` - Filtros
- `mat-checkbox` - Opções de exibição
- `mat-chip` - Tags de categoria
- `mat-badge` - Contadores

---

## 2. TELA: Gerenciar Itens de Domínio (UC01/UC03)

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ ☰ Menu          IControlIT v2 - Domínio: Status de Chamado                             🔔 👤 Admin    │
├─────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                         │
│  ⚙️ Configurações > Domínios > STATUS_CHAMADO                            [Voltar] [💾 Salvar] [❌]    │
│                                                                                                         │
│  ┌───────────────────────────────────────────────────────────────────────────────────────────────────┐ │
│  │  ╔═══════════════════════════════════════════════════════════════════════════════════════════════╗ │ │
│  │  ║ 📋 DOMÍNIO: STATUS_CHAMADO                                                                   ║ │ │
│  │  ║ Categoria: Chamados | Tipo: Customizável | Criado em: 15/01/2024 | 8 itens ativos           ║ │ │
│  │  ╚═══════════════════════════════════════════════════════════════════════════════════════════════╝ │ │
│  │                                                                                                     │ │
│  │  ┌─────────────────────────────────────────────────────────────────────────────────────────────┐   │ │
│  │  │ ABAS: [📋 Itens] [🔄 Transições] [🎨 Aparência] [🌍 i18n] [⚙️ Configurações] [📊 Estatísticas]│ │
│  │  └─────────────────────────────────────────────────────────────────────────────────────────────┘   │ │
│  │                                                                                                     │ │
│  │  ═══ ABA: ITENS ═══                                                                                │ │
│  │                                                                                                     │ │
│  │  [+ Novo Item]  [↕️ Reordenar]  [🎨 Cores em Lote]  [📥 Importar]  [📤 Exportar]                  │ │
│  │                                                                                                     │ │
│  │  ┌───────────────────────────────────────────────────────────────────────────────────────────────┐ │ │
│  │  │ ITENS DO DOMÍNIO                                             8 ativos | 2 inativos | Drag&Drop │ │
│  │  ├────┬───────┬─────────────────┬──────────────┬────────┬─────────┬──────────┬──────────┬────────┤ │ │
│  │  │ ☰  │ ORDEM │   CÓDIGO        │  NOME        │  COR   │ ÍCONE   │  PADRÃO  │  STATUS  │ AÇÕES  │ │ │
│  │  ├────┼───────┼─────────────────┼──────────────┼────────┼─────────┼──────────┼──────────┼────────┤ │ │
│  │  │ ⋮⋮ │   1   │ ABERTO          │Aberto        │🔵#2196F3│fa-inbox │    ✓     │🟢 Ativo  │ ✏️ ⚙️  │ │ │
│  │  │    │       │                 │              │        │         │          │          │        │ │ │
│  │  ├────┼───────┼─────────────────┼──────────────┼────────┼─────────┼──────────┼──────────┼────────┤ │ │
│  │  │ ⋮⋮ │   2   │ EM_ATENDIMENTO  │Em Atendimento│🟡#FFC107│fa-user  │          │🟢 Ativo  │ ✏️ ⚙️  │ │ │
│  │  │    │       │                 │              │        │-headset │          │          │        │ │ │
│  │  ├────┼───────┼─────────────────┼──────────────┼────────┼─────────┼──────────┼──────────┼────────┤ │ │
│  │  │ ⋮⋮ │   3   │ AGUARDANDO      │Aguardando    │🟠#FF9800│fa-clock │          │🟢 Ativo  │ ✏️ ⚙️  │ │ │
│  │  │    │       │                 │Cliente       │        │         │          │          │        │ │ │
│  │  ├────┼───────┼─────────────────┼──────────────┼────────┼─────────┼──────────┼──────────┼────────┤ │ │
│  │  │ ⋮⋮ │   4   │ PENDENTE        │Pendente      │🟣#9C27B0│fa-pause │          │🟢 Ativo  │ ✏️ ⚙️  │ │ │
│  │  │    │       │                 │              │        │         │          │          │        │ │ │
│  │  ├────┼───────┼─────────────────┼──────────────┼────────┼─────────┼──────────┼──────────┼────────┤ │ │
│  │  │ ⋮⋮ │   5   │ RESOLVIDO       │Resolvido     │🟢#4CAF50│fa-check │          │🟢 Ativo  │ ✏️ ⚙️  │ │ │
│  │  │    │       │                 │              │        │         │          │          │        │ │ │
│  │  ├────┼───────┼─────────────────┼──────────────┼────────┼─────────┼──────────┼──────────┼────────┤ │ │
│  │  │ ⋮⋮ │   6   │ FECHADO         │Fechado       │⚫#607D8B│fa-check │          │🟢 Ativo  │ ✏️ ⚙️  │ │ │
│  │  │    │       │                 │              │        │-double  │          │          │        │ │ │
│  │  ├────┼───────┼─────────────────┼──────────────┼────────┼─────────┼──────────┼──────────┼────────┤ │ │
│  │  │ ⋮⋮ │   7   │ CANCELADO       │Cancelado     │🔴#F44336│fa-times │          │🟢 Ativo  │ ✏️ ⚙️  │ │ │
│  │  │    │       │                 │              │        │         │          │          │        │ │ │
│  │  ├────┼───────┼─────────────────┼──────────────┼────────┼─────────┼──────────┼──────────┼────────┤ │ │
│  │  │ ⋮⋮ │   8   │ REABERTO        │Reaberto      │🟠#FF5722│fa-redo  │          │🟢 Ativo  │ ✏️ ⚙️  │ │ │
│  │  │    │       │                 │              │        │         │          │          │        │ │ │
│  │  ├────┼───────┼─────────────────┼──────────────┼────────┼─────────┼──────────┼──────────┼────────┤ │ │
│  │  │ ⋮⋮ │   9   │ SPAM            │Spam          │⚫#000000│fa-ban   │          │🔴 Inativo│ ✏️ ⚙️  │ │ │
│  │  │    │       │                 │              │        │         │          │ 90 dias  │        │ │ │
│  │  ├────┼───────┼─────────────────┼──────────────┼────────┼─────────┼──────────┼──────────┼────────┤ │ │
│  │  │ ⋮⋮ │  10   │ DUPLICADO       │Duplicado     │⚫#9E9E9E│fa-copy  │          │🔴 Inativo│ ✏️ ⚙️  │ │ │
│  │  │    │       │                 │              │        │         │          │ 45 dias  │        │ │ │
│  │  └────┴───────┴─────────────────┴──────────────┴────────┴─────────┴──────────┴──────────┴────────┘ │ │
│  │                                                                                                     │ │
│  │  💡 Arraste itens para reordenar. Ordem define exibição em dropdowns.                              │ │
│  │                                                                                                     │ │
│  │  ═══ FORMULÁRIO RÁPIDO: EDITAR ITEM ═══                                                            │ │
│  │                                                                                                     │ │
│  │  ┌─ ITEM SELECIONADO: EM_ATENDIMENTO ────────────────────────────────────────────────────────┐     │ │
│  │  │                                                                                             │     │ │
│  │  │  Código *                      Nome *                                                       │     │ │
│  │  │  ┌────────────────────────┐    ┌──────────────────────────────────────────┐                │     │ │
│  │  │  │ EM_ATENDIMENTO         │    │ Em Atendimento                           │                │     │ │
│  │  │  └────────────────────────┘    └──────────────────────────────────────────┘                │     │ │
│  │  │                                                                                             │     │ │
│  │  │  Cor (Hex) *                   Ícone (FontAwesome) *                                        │     │ │
│  │  │  [#FFC107        ]  🟡        [fa-user-headset ▼        ]  fa-user-headset               │     │ │
│  │  │   Color Picker                  Seletor com preview                                        │     │ │
│  │  │                                                                                             │     │ │
│  │  │  Ordem                         Status                                                       │     │ │
│  │  │  [    2      ]  [↑] [↓]        ◉ Ativo     ○ Inativo                                       │     │ │
│  │  │                                                                                             │     │ │
│  │  │  ☑ Definir como padrão         ☐ Global (todos conglomerados)                              │     │ │
│  │  │                                                                                             │     │ │
│  │  │  [❌ Cancelar]  [💾 Salvar Item]                                                            │     │ │
│  │  └─────────────────────────────────────────────────────────────────────────────────────────────┘     │ │
│  │                                                                                                     │ │
│  │  ═══ ABA: TRANSIÇÕES ═══                                                                           │ │
│  │                                                                                                     │ │
│  │  ┌─ WORKFLOW VISUAL ──────────────────────────────────────────────────────────────────────────┐     │ │
│  │  │                                                                                             │     │ │
│  │  │  💡 Configure quais mudanças de status são permitidas                                      │     │ │
│  │  │                                                                                             │     │ │
│  │  │  ┌────────────────────────────────────────────────────────────────────────────────────┐    │     │ │
│  │  │  │                                                                                      │    │     │ │
│  │  │  │                          ┌─────────────┐                                            │    │     │ │
│  │  │  │                          │   ABERTO    │                                            │    │     │ │
│  │  │  │                          └──────┬──────┘                                            │    │     │ │
│  │  │  │                                 │                                                    │    │     │ │
│  │  │  │                    ┌────────────┼────────────┐                                      │    │     │ │
│  │  │  │                    ↓            ↓            ↓                                      │    │     │ │
│  │  │  │          ┌──────────────┐ ┌──────────────┐ ┌───────────┐                          │    │     │ │
│  │  │  │          │EM_ATENDIMENTO│ │  AGUARDANDO  │ │ CANCELADO │                          │    │     │ │
│  │  │  │          └──────┬───────┘ └──────┬───────┘ └───────────┘                          │    │     │ │
│  │  │  │                 │                │                                                  │    │     │ │
│  │  │  │                 ↓                ↓                                                  │    │     │ │
│  │  │  │          ┌──────────────┐ ┌──────────────┐                                         │    │     │ │
│  │  │  │          │   RESOLVIDO  │ │   PENDENTE   │                                         │    │     │ │
│  │  │  │          └──────┬───────┘ └──────┬───────┘                                         │    │     │ │
│  │  │  │                 │                │                                                  │    │     │ │
│  │  │  │                 └────────┬───────┘                                                  │    │     │ │
│  │  │  │                          ↓                                                          │    │     │ │
│  │  │  │                   ┌──────────────┐         ┌──────────────┐                        │    │     │ │
│  │  │  │                   │   FECHADO    │  ←──────│   REABERTO   │                        │    │     │ │
│  │  │  │                   └──────────────┘         └──────────────┘                        │    │     │ │
│  │  │  │                                                                                      │    │     │ │
│  │  │  │  LEGENDA: ━━ Transição permitida  |  ✓ Justificativa obrigatória  |  ⚠ Aprovação  │    │     │ │
│  │  │  └────────────────────────────────────────────────────────────────────────────────────┘    │     │ │
│  │  │                                                                                             │     │ │
│  │  │  [✏️ Editar Workflow Visual]  [📊 Exportar Diagrama]  [⚙️ Configurar Regras]                │     │ │
│  │  │                                                                                             │     │ │
│  │  └─────────────────────────────────────────────────────────────────────────────────────────────┘     │ │
│  │                                                                                                     │ │
│  │  ┌─ MATRIZ DE TRANSIÇÕES ────────────────────────────────────────────────────────────────────┐     │ │
│  │  │                                                                                             │     │ │
│  │  │  ┌───────────────────────────────────────────────────────────────────────────────────────┐ │     │ │
│  │  │  │ DE \ PARA        │ ABERTO│EM_ATEND│AGUARD│PEND│RESOLV│FECHA│CANCEL│REABER│ JUSTIF│APROV││     │ │
│  │  │  ├──────────────────┼───────┼────────┼──────┼────┼──────┼─────┼──────┼──────┼───────┼─────┤│     │ │
│  │  │  │ ABERTO           │   ━   │   ✅   │  ✅  │ ✅ │  ❌  │ ❌  │  ✅  │  ❌  │       │     ││     │ │
│  │  │  │ EM_ATENDIMENTO   │   ❌  │   ━    │  ✅  │ ✅ │  ✅  │ ❌  │  ✅  │  ❌  │       │     ││     │ │
│  │  │  │ AGUARDANDO       │   ❌  │   ✅   │  ━   │ ✅ │  ✅  │ ❌  │  ✅  │  ❌  │   ✓   │     ││     │ │
│  │  │  │ PENDENTE         │   ❌  │   ✅   │  ✅  │ ━  │  ✅  │ ❌  │  ✅  │  ❌  │   ✓   │     ││     │ │
│  │  │  │ RESOLVIDO        │   ❌  │   ❌   │  ❌  │ ❌ │  ━   │ ✅  │  ❌  │  ✅  │   ✓   │     ││     │ │
│  │  │  │ FECHADO          │   ❌  │   ❌   │  ❌  │ ❌ │  ❌  │ ━   │  ❌  │  ✅  │   ✓   │  ⚠ ││     │ │
│  │  │  │ CANCELADO        │   ❌  │   ❌   │  ❌  │ ❌ │  ❌  │ ❌  │  ━   │  ✅  │   ✓   │  ⚠ ││     │ │
│  │  │  │ REABERTO         │   ❌  │   ✅   │  ✅  │ ✅ │  ✅  │ ❌  │  ✅  │  ━   │   ✓   │     ││     │ │
│  │  │  └──────────────────┴───────┴────────┴──────┴────┴──────┴─────┴──────┴──────┴───────┴─────┘│     │ │
│  │  │                                                                                             │     │ │
│  │  │  💡 Clique nas células para habilitar/desabilitar transições                               │     │ │
│  │  │  ✓ = Justificativa obrigatória  |  ⚠ = Requer aprovação de gestor                         │     │ │
│  │  │                                                                                             │     │ │
│  │  └─────────────────────────────────────────────────────────────────────────────────────────────┘     │ │
│  │                                                                                                     │ │
│  │  ═══ ABA: i18n (INTERNACIONALIZAÇÃO) ═══                                                          │ │
│  │                                                                                                     │ │
│  │  ┌─ TRADUÇÕES ────────────────────────────────────────────────────────────────────────────────┐     │ │
│  │  │                                                                                             │     │ │
│  │  │  💡 Traduza os nomes dos itens para pt-BR, en-US e es-ES                                   │     │ │
│  │  │                                                                                             │     │ │
│  │  │  ┌───────────────────────────────────────────────────────────────────────────────────────┐ │     │ │
│  │  │  │ CÓDIGO           │  🇧🇷 pt-BR         │  🇺🇸 en-US         │  🇪🇸 es-ES         │ AÇÕES  │ │     │ │
│  │  │  ├──────────────────┼────────────────────┼────────────────────┼────────────────────┼───────┤ │     │ │
│  │  │  │ ABERTO           │ Aberto             │ Open               │ Abierto            │  ✏️   │ │     │ │
│  │  │  │ EM_ATENDIMENTO   │ Em Atendimento     │ In Progress        │ En Progreso        │  ✏️   │ │     │ │
│  │  │  │ AGUARDANDO       │ Aguardando Cliente │ Awaiting Customer  │ Esperando Cliente  │  ✏️   │ │     │ │
│  │  │  │ PENDENTE         │ Pendente           │ Pending            │ Pendiente          │  ✏️   │ │     │ │
│  │  │  │ RESOLVIDO        │ Resolvido          │ Resolved           │ Resuelto           │  ✏️   │ │     │ │
│  │  │  │ FECHADO          │ Fechado            │ Closed             │ Cerrado            │  ✏️   │ │     │ │
│  │  │  │ CANCELADO        │ Cancelado          │ Cancelled          │ Cancelado          │  ✏️   │ │     │ │
│  │  │  │ REABERTO         │ Reaberto           │ Reopened           │ Reabierto          │  ✏️   │ │     │ │
│  │  │  └──────────────────┴────────────────────┴────────────────────┴────────────────────┴───────┘ │     │ │
│  │  │                                                                                             │     │ │
│  │  │  [🤖 Auto-Traduzir (IA)]  [📥 Importar CSV]  [📤 Exportar CSV]  [💾 Salvar Traduções]      │     │ │
│  │  │                                                                                             │     │ │
│  │  └─────────────────────────────────────────────────────────────────────────────────────────────┘     │ │
│  │                                                                                                     │ │
│  │  ═══ ABA: ESTATÍSTICAS ═══                                                                         │ │
│  │                                                                                                     │ │
│  │  ┌─ USO POR ITEM ─────────────────────────────────────────────────────────────────────────────┐     │ │
│  │  │                                                                                             │     │ │
│  │  │  📊 GRÁFICO DE BARRAS - ÚLTIMOS 30 DIAS                                                    │     │ │
│  │  │                                                                                             │     │ │
│  │  │  ABERTO           ████████████████████████████████████████ 456 (35%)                       │     │ │
│  │  │  EM_ATENDIMENTO   ████████████████████████████ 312 (24%)                                   │     │ │
│  │  │  FECHADO          ████████████████████ 245 (19%)                                           │     │ │
│  │  │  RESOLVIDO        ███████████████ 167 (13%)                                                │     │ │
│  │  │  AGUARDANDO       ██████████ 89 (7%)                                                       │     │ │
│  │  │  PENDENTE         ████ 23 (2%)                                                             │     │ │
│  │  │  REABERTO         ██ 12 (1%)                                                               │     │ │
│  │  │  CANCELADO        █ 8 (1%)                                                                 │     │ │
│  │  │                                                                                             │     │ │
│  │  │  💡 INSIGHTS:                                                                               │     │ │
│  │  │  • 35% dos chamados estão ABERTOS (alta demanda)                                           │     │ │
│  │  │  • Taxa de resolução: 32% (RESOLVIDO + FECHADO)                                            │     │ │
│  │  │  • Taxa de reincidência: 1% (REABERTO)                                                     │     │ │
│  │  │                                                                                             │     │ │
│  │  └─────────────────────────────────────────────────────────────────────────────────────────────┘     │ │
│  │                                                                                                     │ │
│  │  [⬅️ Voltar]  [💾 Salvar Todas Alterações]                                                         │ │
│  └───────────────────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

**Componentes Fuse:**
- `mat-tab-group` - Sistema de abas
- `fuse-card` - Cards de conteúdo
- `mat-table` - Grid de itens (drag & drop com CDK)
- `mat-color-picker` - Seletor de cores
- `mat-select` - Dropdown de ícones
- Mermaid/D3.js - Diagrama de workflow
- `mat-grid-list` - Matriz de transições
- Chart components - Gráficos de estatísticas

---

## 3. INTEGRAÇÕES OBRIGATÓRIAS

### 3.1 Central de Funcionalidades
```typescript
const funcionalidade = {
  codigo: 'GES.TIPOS_GENERICOS',
  nome: 'Gestão de Status e Tipos',
  modulo: 'Configurações',
  icone: 'settings_applications',
  rota: '/configuracoes/tipos-genericos'
};
```

### 3.2 Internacionalização (i18n)
```json
{
  "tipos_genericos": {
    "titulo": "Gestão de Status e Tipos Genéricos",
    "subtitulo": "Domínios parametrizáveis do sistema",
    "dominios": {
      "status_chamado": "Status de Chamado",
      "prioridade": "Prioridade",
      "tipo_ativo": "Tipo de Ativo"
    },
    "transicoes": {
      "permitida": "Transição permitida",
      "justificativa": "Justificativa obrigatória",
      "aprovacao": "Requer aprovação"
    }
  }
}
```

### 3.3 Auditoria
```typescript
enum TiposGenericosAuditOperations {
  DOMINIO_CRIADO = 'DOMINIO_CRIADO',
  ITEM_CRIADO = 'DOMINIO_ITEM_CRIADO',
  ITEM_EDITADO = 'DOMINIO_ITEM_EDITADO',
  ITEM_INATIVADO = 'DOMINIO_ITEM_INATIVADO',
  TRANSICAO_ALTERADA = 'DOMINIO_TRANSICAO_ALTERADA',
  TRADUCAO_ATUALIZADA = 'DOMINIO_I18N_ATUALIZADA'
}
```

### 3.4 RBAC
```typescript
export const TiposGenericosPermissions = {
  VIEW: 'GES.TIPOS.VIEW',
  CREATE: 'GES.TIPOS.CREATE',
  EDIT: 'GES.TIPOS.EDIT',
  DELETE: 'GES.TIPOS.DELETE',
  CONFIGURE_WORKFLOW: 'GES.TIPOS.CONFIGURE_WORKFLOW',
  MANAGE_I18N: 'GES.TIPOS.MANAGE_I18N'
};
```

---

## 4. CACHE E PERFORMANCE

### 4.1 Cache Strategy
```typescript
@Injectable()
export class TiposGenericosService {
  private cache = new Map<string, Observable<any>>();
  private cacheTimeout = 15 * 60 * 1000; // 15 minutos

  getDominio(codigo: string): Observable<Dominio> {
    const cacheKey = `dominio_${codigo}`;

    if (!this.cache.has(cacheKey)) {
      this.cache.set(cacheKey,
        this.http.get<Dominio>(`/api/dominios/${codigo}`).pipe(
          shareReplay({ bufferSize: 1, refCount: true }),
          catchError(() => {
            this.cache.delete(cacheKey);
            return EMPTY;
          })
        )
      );

      // Auto-invalidação
      setTimeout(() => this.cache.delete(cacheKey), this.cacheTimeout);
    }

    return this.cache.get(cacheKey)!;
  }

  invalidateCache(codigo?: string): void {
    if (codigo) {
      this.cache.delete(`dominio_${codigo}`);
    } else {
      this.cache.clear();
    }
  }
}
```

---

**Wireframes aprovados para implementação.**
**Total de linhas:** 677
