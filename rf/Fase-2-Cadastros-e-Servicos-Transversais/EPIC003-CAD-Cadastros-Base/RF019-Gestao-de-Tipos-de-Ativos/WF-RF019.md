# Wireframes - RF019: Gestão de Tipos de Ativos

**Requisito Funcional:** RF019 - Gestão de Tipos de Ativos
**EPIC:** EPIC003-GES - Gestão
**Fase:** Fase 2 - Serviços Essenciais
**Versão:** 1.0
**Data:** 2025-01-18
**Responsável:** Architect Agent

---

## 1. Informações do Documento

### 1.1 Objetivo
Apresentar wireframes em ASCII art para todas as telas do RF019 - Gestão de Tipos de Ativos, demonstrando taxonomia de ativos, hierarquia, atributos customizáveis e templates.

### 1.2 Escopo
- CRUD completo de tipos de ativos
- Taxonomia hierárquica (Categoria → Subcategoria → Tipo → Subtipo)
- Tipos principais: Hardware, Software, Licenças, Serviços, Contratos, Consumíveis
- Atributos customizáveis por tipo (campos dinâmicos)
- Templates de tipos pré-configurados
- Regras de depreciação por tipo
- Vinculação com fornecedores e fabricantes
- Relatórios de tipos de ativos e inventário

### 1.3 Casos de Uso Cobertos
- UC00 - Listar Tipos de Ativos
- UC01 - Criar Tipo de Ativo
- UC02 - Visualizar Tipo de Ativo
- UC03 - Editar Tipo de Ativo
- UC04 - Inativar Tipo de Ativo
- UC05 - Árvore Hierárquica de Tipos

---

## 2. Wireframes das Telas

### 2.1 Tela Principal - Lista de Tipos de Ativos (UC00)

**Rota:** `/gestao/tipos-ativos`
**Permissão:** `GES.TIPOS_ATIVOS.VIEW`

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ SIDEBAR (240px)              HEADER (altura: 64px)                                                                                      │
├──────────────────────────────┬──────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                              │  🏢 IControlIT                      👤 João Silva (Super Admin)  🔔 [3]  ⚙️  🌐 PT-BR  ❓               │
│ 📊 Dashboard                 ├──────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ 📁 Cadastros ▼               │                                                                                                          │
│   • Empresas                 │  ┌────────────────────────────────────────────────────────────────────────────────────────────────────┐ │
│   • Usuários                 │  │ GESTÃO DE TIPOS DE ATIVOS                                                                          │ │
│   • Fornecedores             │  │                                                                                                    │ │
│ 🏗️ Gestão ▼                  │  │ [🔙 Voltar]  📋 Gestão > Tipos de Ativos                                                          │ │
│   • Locais                   │  └────────────────────────────────────────────────────────────────────────────────────────────────────┘ │
│   • Categorias               │                                                                                                          │
│   • Hierarquia               │  ┌────────────────────────────────────────────────────────────────────────────────────────────────────┐ │
│   • Cargos                   │  │  🔍 Pesquisar tipo, categoria...                    [🌳 Árvore Hierárquica]  [📊 Lista]  ◄ ativo  │ │
│   ► Tipos de Ativos ◄        │  │                                                                                                    │ │
│ 🔧 Configurações             │  │  [➕ Novo Tipo]  [📁 Templates]  [📥 Importar]  [📤 Exportar]  [⚙️ Configurações]                 │ │
│ 📈 Relatórios                │  └────────────────────────────────────────────────────────────────────────────────────────────────────┘ │
│                              │                                                                                                          │
│                              │  ┌────────────────────────────────────────────────────────────────────────────────────────────────────┐ │
│                              │  │ FILTROS                                                                         [🔽 Expandir]       │ │
│                              │  ├────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│                              │  │ Categoria: [Todas ▼]  Subcategoria: [Todas ▼]  Status: [Ativos ▼]  Depreciável: [Todos ▼]        │ │
│                              │  └────────────────────────────────────────────────────────────────────────────────────────────────────┘ │
│                              │                                                                                                          │
│                              │  ┌────────────────────────────────────────────────────────────────────────────────────────────────────┐ │
│                              │  │ ESTATÍSTICAS                                                                                       │ │
│                              │  ├────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│                              │  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐              │ │
│                              │  │  │   285    │  │    12    │  │  3.250   │  │    180   │  │    95%   │  │    42    │              │ │
│                              │  │  │  Tipos   │  │ Categorias│  │  Ativos  │  │  Tipos   │  │  Tipos   │  │  Tipos   │              │ │
│                              │  │  │  Ativos  │  │ Principais│  │Cadastrados│  │Depreciáv.│  │ em Uso   │  │ Inativos │              │ │
│                              │  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘              │ │
│                              │  └────────────────────────────────────────────────────────────────────────────────────────────────────┘ │
│                              │                                                                                                          │
│                              │  ┌────────────────────────────────────────────────────────────────────────────────────────────────────┐ │
│                              │  │ TIPOS DE ATIVOS                                                    Exibindo 1-20 de 285 tipos      │ │
│                              │  ├────┬────────────────────────────┬─────────────────┬────────────┬──────────┬─────────┬────────────┤ │
│                              │  │Cód.│ Tipo de Ativo              │ Categoria       │ Subcategoria│ Qtd Ativos│ Status │ Ações      │ │
│                              │  ├────┼────────────────────────────┼─────────────────┼────────────┼──────────┼─────────┼────────────┤ │
│                              │  │T001│ 💻 Notebook Dell Latitude  │ 🖥️ Hardware     │ Computadores│ 245      │ ✅ Ativo│[👁️][✏️][🗑️]│ │
│                              │  │    │ [5 atributos customizados] │                 │            │ 12 vagas │         │            │ │
│                              │  ├────┼────────────────────────────┼─────────────────┼────────────┼──────────┼─────────┼────────────┤ │
│                              │  │T002│ 📱 iPhone 14 Pro           │ 🖥️ Hardware     │ Smartphones│ 180      │ ✅ Ativo│[👁️][✏️][🗑️]│ │
│                              │  │    │ [6 atributos]              │                 │            │ 0 vagas  │         │            │ │
│                              │  ├────┼────────────────────────────┼─────────────────┼────────────┼──────────┼─────────┼────────────┤ │
│                              │  │T003│ 💾 Microsoft Office 365    │ 💿 Software     │ Produtividade│ 420    │ ✅ Ativo│[👁️][✏️][🗑️]│ │
│                              │  │    │ [3 atributos]              │                 │            │ 0 vagas  │         │            │ │
│                              │  ├────┼────────────────────────────┼─────────────────┼────────────┼──────────┼─────────┼────────────┤ │
│                              │  │T004│ 🔑 Licença Adobe Creative  │ 📜 Licenças     │ Design      │ 85       │ ✅ Ativo│[👁️][✏️][🗑️]│ │
│                              │  │    │ [4 atributos]              │                 │            │ 5 vagas  │         │            │ │
│                              │  ├────┼────────────────────────────┼─────────────────┼────────────┼──────────┼─────────┼────────────┤ │
│                              │  │T005│ 🖨️ Impressora HP LaserJet  │ 🖥️ Hardware     │ Periféricos│ 42       │ ✅ Ativo│[👁️][✏️][🗑️]│ │
│                              │  │    │ [7 atributos]              │                 │            │ 0 vagas  │         │            │ │
│                              │  ├────┼────────────────────────────┼─────────────────┼────────────┼──────────┼─────────┼────────────┤ │
│                              │  │T006│ ☁️ AWS Cloud Hosting        │ 🌐 Serviços     │ Cloud      │ 12       │ ✅ Ativo│[👁️][✏️][🗑️]│ │
│                              │  │    │ [8 atributos]              │                 │            │ 0 vagas  │         │            │ │
│                              │  ├────┼────────────────────────────┼─────────────────┼────────────┼──────────┼─────────┼────────────┤ │
│                              │  │T007│ 📄 Contrato de Telefonia   │ 📋 Contratos    │ Telecom    │ 8        │ ✅ Ativo│[👁️][✏️][🗑️]│ │
│                              │  │    │ [12 atributos]             │                 │            │ 0 vagas  │         │            │ │
│                              │  ├────┼────────────────────────────┼─────────────────┼────────────┼──────────┼─────────┼────────────┤ │
│                              │  │T008│ 🔌 Switch Cisco 48 portas  │ 🖥️ Hardware     │ Rede       │ 28       │ ✅ Ativo│[👁️][✏️][🗑️]│ │
│                              │  │    │ [9 atributos]              │                 │            │ 2 vagas  │         │            │ │
│                              │  ├────┼────────────────────────────┼─────────────────┼────────────┼──────────┼─────────┼────────────┤ │
│                              │  │T009│ 🖱️ Mouse Logitech MX Master│ 🖥️ Hardware     │ Periféricos│ 320      │ ✅ Ativo│[👁️][✏️][🗑️]│ │
│                              │  │    │ [3 atributos]              │                 │            │ 0 vagas  │         │            │ │
│                              │  ├────┼────────────────────────────┼─────────────────┼────────────┼──────────┼─────────┼────────────┤ │
│                              │  │T010│ ✏️ Toner HP Q2612A         │ 📦 Consumíveis  │ Impressão  │ 150      │ ✅ Ativo│[👁️][✏️][🗑️]│ │
│                              │  │    │ [2 atributos]              │                 │            │ 0 vagas  │         │            │ │
│                              │  │... (mais 10 tipos)                                                                                │ │
│                              │  └────┴────────────────────────────┴─────────────────┴────────────┴──────────┴─────────┴────────────┘ │
│                              │                                                                                                          │
│                              │  [◄◄ Primeira] [◄ Anterior] Página 1 de 15 [Próxima ►] [Última ►►]   Exibir: [20 ▼] por página       │
│                              │                                                                                                          │
│                              │  ℹ️ Dica: Use [🌳 Árvore Hierárquica] para visualizar a taxonomia completa de tipos.                    │
│                              └────────────────────────────────────────────────────────────────────────────────────────────────────────┘ │
│                              │  FOOTER: © 2025 IControlIT - Versão 2.0.0                                                               │
└──────────────────────────────┴──────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

**INTERAÇÕES:**
- [🌳 Árvore Hierárquica] / [📊 Lista] → Toggle de visualização
- [➕ Novo Tipo] → Abre modal de criação (UC01)
- [📁 Templates] → Abre modal com templates pré-configurados
- [👁️] → Abre painel lateral com detalhes (UC02)
- [✏️] → Abre modal de edição (UC03)
- [🗑️] → Abre modal de inativação (UC04)

---

### 2.2 Visualização em Árvore Hierárquica (UC05)

**Rota:** `/gestao/tipos-ativos?view=tree`
**Permissão:** `GES.TIPOS_ATIVOS.VIEW`

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  ┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐│
│  │ 🔍 Pesquisar tipo...                                          [🌳 Árvore Hierárquica] ◄ ativo  [📊 Lista]                          ││
│  │                                                                                                                                    ││
│  │ [➕ Novo Tipo]  [🔍 Expandir Tudo]  [📁 Recolher Tudo]  [📤 Exportar Taxonomia]                                                   ││
│  └────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘│
│                                                                                                                                        │
│  ┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐│
│  │ TAXONOMIA DE TIPOS DE ATIVOS                                                                                                      ││
│  ├────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤│
│  │                                                                                                                                    ││
│  │  ▼ 🖥️ HARDWARE (520 ativos)                                                                                                       ││
│  │    ▼ Computadores (245 ativos)                                                                                                    ││
│  │      • 💻 Notebook Dell Latitude (120 ativos) [👁️][✏️]                                                                            ││
│  │      • 💻 Notebook HP EliteBook (85 ativos) [👁️][✏️]                                                                              ││
│  │      • 🖥️ Desktop Dell OptiPlex (40 ativos) [👁️][✏️]                                                                              ││
│  │    ▼ Smartphones (180 ativos)                                                                                                     ││
│  │      • 📱 iPhone 14 Pro (95 ativos) [👁️][✏️]                                                                                       ││
│  │      • 📱 Samsung Galaxy S23 (65 ativos) [👁️][✏️]                                                                                  ││
│  │      • 📱 iPhone 13 (20 ativos) [👁️][✏️]                                                                                           ││
│  │    ▼ Periféricos (95 ativos)                                                                                                      ││
│  │      • 🖱️ Mouse Logitech MX Master (50 ativos) [👁️][✏️]                                                                            ││
│  │      • ⌨️ Teclado Mecânico (25 ativos) [👁️][✏️]                                                                                    ││
│  │      • 🖨️ Impressora HP LaserJet (20 ativos) [👁️][✏️]                                                                              ││
│  │    ▶ Rede (28 ativos)                                                                                                             ││
│  │                                                                                                                                    ││
│  │  ▼ 💿 SOFTWARE (420 ativos)                                                                                                        ││
│  │    ▼ Produtividade (320 ativos)                                                                                                   ││
│  │      • 💾 Microsoft Office 365 (250 ativos) [👁️][✏️]                                                                               ││
│  │      • 💾 Google Workspace (70 ativos) [👁️][✏️]                                                                                    ││
│  │    ▼ Design (85 ativos)                                                                                                           ││
│  │      • 🎨 Adobe Creative Cloud (60 ativos) [👁️][✏️]                                                                                ││
│  │      • 🎨 Figma (25 ativos) [👁️][✏️]                                                                                               ││
│  │    ▶ Desenvolvimento (15 ativos)                                                                                                  ││
│  │                                                                                                                                    ││
│  │  ▼ 📜 LICENÇAS (185 ativos)                                                                                                        ││
│  │    ▼ Sistema Operacional (100 ativos)                                                                                             ││
│  │      • 🪟 Windows 11 Pro (80 ativos) [👁️][✏️]                                                                                      ││
│  │      • 🍎 macOS Ventura (20 ativos) [👁️][✏️]                                                                                       ││
│  │    ▼ Antivírus (85 ativos)                                                                                                        ││
│  │      • 🛡️ Kaspersky Total Security (60 ativos) [👁️][✏️]                                                                           ││
│  │      • 🛡️ Norton 360 (25 ativos) [👁️][✏️]                                                                                          ││
│  │                                                                                                                                    ││
│  │  ▼ 🌐 SERVIÇOS (32 ativos)                                                                                                         ││
│  │    ▼ Cloud (20 ativos)                                                                                                            ││
│  │      • ☁️ AWS Cloud Hosting (12 ativos) [👁️][✏️]                                                                                   ││
│  │      • ☁️ Azure Cloud (8 ativos) [👁️][✏️]                                                                                          ││
│  │    ▶ Suporte (12 ativos)                                                                                                          ││
│  │                                                                                                                                    ││
│  │  ▼ 📋 CONTRATOS (25 ativos)                                                                                                        ││
│  │    ▼ Telecom (15 ativos)                                                                                                          ││
│  │      • 📞 Contrato Vivo (8 ativos) [👁️][✏️]                                                                                        ││
│  │      • 📞 Contrato Claro (7 ativos) [👁️][✏️]                                                                                       ││
│  │    ▶ Manutenção (10 ativos)                                                                                                       ││
│  │                                                                                                                                    ││
│  │  ▶ 📦 CONSUMÍVEIS (350 ativos)                                                                                                     ││
│  │                                                                                                                                    ││
│  │  TOTAIS: 6 categorias, 18 subcategorias, 285 tipos, 1.532 ativos                                                                  ││
│  │                                                                                                                                    ││
│  │  ℹ️ Clique em ▶/▼ para expandir/recolher. Clique no tipo para ver detalhes.                                                       ││
│  └────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘│
└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

### 2.3 Modal - Criar Novo Tipo de Ativo (UC01)

**Acionado por:** Botão [➕ Novo Tipo]
**Permissão:** `GES.TIPOS_ATIVOS.CREATE`

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ CRIAR NOVO TIPO DE ATIVO                                                                   [✖️]     │
├────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                    │
│  [ABA: Informações Básicas] ◄ selecionada  [ABA: Atributos]  [ABA: Depreciação]  [ABA: Fornecedor]│
│                                                                                                    │
│  ┌──────────────────────────────────────────────────────────────────────────────────────────────┐ │
│  │ INFORMAÇÕES BÁSICAS                                                                          │ │
│  ├──────────────────────────────────────────────────────────────────────────────────────────────┤ │
│  │                                                                                              │ │
│  │  Código *                                     Nome do Tipo *                                │ │
│  │  ┌──────────────────┐                         ┌─────────────────────────────────────────┐   │ │
│  │  │ T286             │                         │ Monitor LG UltraWide 34"                │   │ │
│  │  └──────────────────┘                         └─────────────────────────────────────────┘   │ │
│  │  Auto-gerado: [✓]                             50 caracteres máximo                         │ │
│  │                                                                                              │ │
│  │  Categoria *                                  Subcategoria *                                │ │
│  │  ┌────────────────────────────────┐           ┌────────────────────────────────┐           │ │
│  │  │ 🖥️ Hardware                 ▼ │           │ Monitores                   ▼ │           │ │
│  │  └────────────────────────────────┘           └────────────────────────────────┘           │ │
│  │  [➕ Criar nova categoria]                     [➕ Criar nova subcategoria]                  │ │
│  │                                                                                              │ │
│  │  Ícone (emoji)                                Cor de Identificação                          │ │
│  │  ┌──────────────────┐                         ┌────────────────────────────────┐           │ │
│  │  │ 🖥️               │  [📋 Lista]             │ [███] Azul Escuro           ▼ │           │ │
│  │  └──────────────────┘                         └────────────────────────────────┘           │ │
│  │  ℹ️ Usado na interface                         Usado em gráficos e dashboards              │ │
│  │                                                                                              │ │
│  │  Descrição                                                                                   │ │
│  │  ┌──────────────────────────────────────────────────────────────────────────────────────┐   │ │
│  │  │ Monitor ultrawide de 34 polegadas com resolução WQHD (3440x1440), ideal para         │   │ │
│  │  │ produtividade e trabalho multitarefa.                                                │   │ │
│  │  │                                                                                       │   │ │
│  │  └──────────────────────────────────────────────────────────────────────────────────────┘   │ │
│  │  120/500 caracteres                                                                          │ │
│  └──────────────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                                    │
│  ┌──────────────────────────────────────────────────────────────────────────────────────────────┐ │
│  │ CONFIGURAÇÕES DE GESTÃO                                                                      │ │
│  ├──────────────────────────────────────────────────────────────────────────────────────────────┤ │
│  │                                                                                              │ │
│  │  Tipo de Ativo                                Permite Múltiplos?                            │ │
│  │  (•) Tangível (Físico)                        (•) Sim    ( ) Não                            │ │
│  │  ( ) Intangível (Licenças, Serviços)          ℹ️ Um colaborador pode ter múltiplas unidades │ │
│  │  ℹ️ Define se possui localização física                                                      │ │
│  │                                                                                              │ │
│  │  É Depreciável?                               Unidade de Medida                             │ │
│  │  (•) Sim    ( ) Não                           ┌────────────────────────────────┐           │ │
│  │  ℹ️ Calcula depreciação contábil               │ Unidade (un)                ▼ │           │ │
│  │                                                └────────────────────────────────┘           │ │
│  │                                                Opções: un, pç, cx, lt, kg, m, etc.          │ │
│  │                                                                                              │ │
│  │  Requer Número de Série?                      Requer Garantia?                              │ │
│  │  (•) Sim    ( ) Não                           (•) Sim    ( ) Não                            │ │
│  │  ℹ️ Campo obrigatório no cadastro              ℹ️ Exige data de término de garantia          │ │
│  │                                                                                              │ │
│  │  Categoria de Risco                           Criticidade                                   │ │
│  │  ┌────────────────────────────────┐           ┌────────────────────────────────┐           │ │
│  │  │ Baixo                       ▼ │           │ Média                       ▼ │           │ │
│  │  └────────────────────────────────┘           └────────────────────────────────┘           │ │
│  │  Opções: Baixo, Médio, Alto, Crítico          Opções: Baixa, Média, Alta, Crítica          │ │
│  └──────────────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                                    │
│  ┌──────────────────────────────────────────────────────────────────────────────────────────────┐ │
│  │ STATUS E CONTROLE                                                                            │ │
│  ├──────────────────────────────────────────────────────────────────────────────────────────────┤ │
│  │                                                                                              │ │
│  │  Status Inicial                               Permite Vagas?                                │ │
│  │  ┌──────────────────┐                         (•) Sim    ( ) Não                            │ │
│  │  │ ✅ Ativo      ▼ │                         ℹ️ Controla headcount de ativos                │ │
│  │  └──────────────────┘                                                                        │ │
│  │                                                                                              │ │
│  │  Opções Adicionais:                                                                          │ │
│  │  [✓] Exigir aprovação para novos ativos deste tipo                                           │ │
│  │  [✓] Notificar administrador ao cadastrar novo ativo                                         │ │
│  │  [ ] Bloquear exclusão de ativos ativos deste tipo                                           │ │
│  │  [✓] Rastrear movimentações de localização                                                   │ │
│  └──────────────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                                    │
│  ℹ️ Próximo passo: Configure os atributos customizáveis na aba "Atributos".                       │
│                                                                                                    │
│                                                                       [Cancelar]  [💾 Salvar]      │
└────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

### 2.4 Aba - Atributos Customizáveis

**Rota:** Modal de criação/edição → Aba "Atributos"
**Permissão:** `GES.TIPOS_ATIVOS.CREATE` ou `UPDATE`

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ CRIAR NOVO TIPO DE ATIVO - Monitor LG UltraWide 34"                                       [✖️]     │
├────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                    │
│  [ABA: Informações Básicas]  [ABA: Atributos] ◄ selecionada  [ABA: Depreciação]  [ABA: Fornecedor]│
│                                                                                                    │
│  ┌──────────────────────────────────────────────────────────────────────────────────────────────┐ │
│  │ ATRIBUTOS CUSTOMIZÁVEIS                                                         [➕ Adicionar] │ │
│  ├──────────────────────────────────────────────────────────────────────────────────────────────┤ │
│  │                                                                                              │ │
│  │  ℹ️ Defina campos adicionais que serão exigidos ao cadastrar ativos deste tipo.              │ │
│  │                                                                                              │ │
│  │  ┌────────────────────────────────────────────────────────────────────────────────────────┐ │ │
│  │  │ 1. Tamanho da Tela                              Tipo: Texto          [🔺][🔻][✏️][🗑️]  │ │ │
│  │  │    Obrigatório: ✅ Sim   |   Exemplo: "34 polegadas"                                   │ │ │
│  │  └────────────────────────────────────────────────────────────────────────────────────────┘ │ │
│  │                                                                                              │ │
│  │  ┌────────────────────────────────────────────────────────────────────────────────────────┐ │ │
│  │  │ 2. Resolução                                    Tipo: Texto          [🔺][🔻][✏️][🗑️]  │ │ │
│  │  │    Obrigatório: ✅ Sim   |   Exemplo: "3440x1440 (WQHD)"                               │ │ │
│  │  └────────────────────────────────────────────────────────────────────────────────────────┘ │ │
│  │                                                                                              │ │
│  │  ┌────────────────────────────────────────────────────────────────────────────────────────┐ │ │
│  │  │ 3. Taxa de Atualização                          Tipo: Número         [🔺][🔻][✏️][🗑️]  │ │ │
│  │  │    Obrigatório: ⚠️ Não   |   Exemplo: "144"   |   Unidade: "Hz"                        │ │ │
│  │  └────────────────────────────────────────────────────────────────────────────────────────┘ │ │
│  │                                                                                              │ │
│  │  ┌────────────────────────────────────────────────────────────────────────────────────────┐ │ │
│  │  │ 4. Conexões                                     Tipo: Lista          [🔺][🔻][✏️][🗑️]  │ │ │
│  │  │    Obrigatório: ✅ Sim   |   Opções: HDMI, DisplayPort, USB-C, VGA                     │ │ │
│  │  │    Permite múltiplas seleções: ✅ Sim                                                   │ │ │
│  │  └────────────────────────────────────────────────────────────────────────────────────────┘ │ │
│  │                                                                                              │ │
│  │  ┌────────────────────────────────────────────────────────────────────────────────────────┐ │ │
│  │  │ 5. Ajuste de Altura                             Tipo: Sim/Não        [🔺][🔻][✏️][🗑️]  │ │ │
│  │  │    Obrigatório: ⚠️ Não   |   Padrão: Não                                               │ │ │
│  │  └────────────────────────────────────────────────────────────────────────────────────────┘ │ │
│  │                                                                                              │ │
│  │  Total: 5 atributos customizados                                                            │ │
│  └──────────────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                                    │
│  ┌──────────────────────────────────────────────────────────────────────────────────────────────┐ │
│  │ ADICIONAR NOVO ATRIBUTO                                                                      │ │
│  ├──────────────────────────────────────────────────────────────────────────────────────────────┤ │
│  │                                                                                              │ │
│  │  Nome do Atributo *                           Tipo de Dado *                                │ │
│  │  ┌────────────────────────────────┐           ┌────────────────────────────────┐           │ │
│  │  │ Marca                           │           │ Texto                       ▼ │           │ │
│  │  └────────────────────────────────┘           └────────────────────────────────┘           │ │
│  │  30 caracteres máximo                         Opções: Texto, Número, Data,                 │ │
│  │                                                        Lista, Sim/Não, Moeda                │ │
│  │                                                                                              │ │
│  │  Obrigatório?                                 Exemplo/Padrão                                │ │
│  │  (•) Sim    ( ) Não                           ┌────────────────────────────────┐           │ │
│  │  ℹ️ Será exigido no cadastro                   │ LG, Samsung, Dell              │           │ │
│  │                                                └────────────────────────────────┘           │ │
│  │                                                                                              │ │
│  │  📝 Se Tipo = Lista, defina as opções separadas por vírgula:                                │ │
│  │  ┌────────────────────────────────────────────────────────────────────────────────────────┐ │ │
│  │  │ LG, Samsung, Dell, HP, AOC, Philips                                                    │ │ │
│  │  └────────────────────────────────────────────────────────────────────────────────────────┘ │ │
│  │                                                                                              │ │
│  │  Permite múltiplas seleções? (Apenas para Tipo = Lista)                                     │ │
│  │  ( ) Sim    (•) Não                                                                          │ │
│  │                                                                                              │ │
│  │                                                                             [✅ Adicionar]     │ │
│  └──────────────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                                    │
│                                                     [◄ Voltar]  [Próxima: Depreciação ►]          │
└────────────────────────────────────────────────────────────────────────────────────────────────────┘

TIPOS DE DADO SUPORTADOS:
- Texto: Campo de texto livre
- Número: Apenas números (com opção de unidade)
- Data: Seletor de data
- Lista: Dropdown com opções pré-definidas
- Sim/Não: Toggle booleano
- Moeda: Campo numérico com formatação de moeda (R$)
```

---

### 2.5 Aba - Depreciação

**Rota:** Modal de criação/edição → Aba "Depreciação"
**Permissão:** `GES.TIPOS_ATIVOS.CREATE` ou `UPDATE`

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ CRIAR NOVO TIPO DE ATIVO - Monitor LG UltraWide 34"                                       [✖️]     │
├────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                    │
│  [ABA: Informações Básicas]  [ABA: Atributos]  [ABA: Depreciação] ◄ selecionada  [ABA: Fornecedor]│
│                                                                                                    │
│  ┌──────────────────────────────────────────────────────────────────────────────────────────────┐ │
│  │ CONFIGURAÇÕES DE DEPRECIAÇÃO                                                                 │ │
│  ├──────────────────────────────────────────────────────────────────────────────────────────────┤ │
│  │                                                                                              │ │
│  │  Este tipo de ativo é depreciável?                                                           │ │
│  │  (•) Sim, aplicar depreciação    ( ) Não, não depreciável                                   │ │
│  │  ℹ️ Ativos depreciáveis têm valor contábil reduzido ao longo do tempo.                       │ │
│  │                                                                                              │ │
│  │  Método de Depreciação *                                                                     │ │
│  │  ┌────────────────────────────────────────────────────────────────────────────────────────┐ │ │
│  │  │ (•) Linear (Mais comum)                                                                │ │ │
│  │  │     ℹ️ Valor distribuído igualmente ao longo da vida útil                              │ │ │
│  │  │                                                                                         │ │ │
│  │  │ ( ) Soma dos Dígitos                                                                   │ │ │
│  │  │     ℹ️ Depreciação maior nos primeiros anos                                            │ │ │
│  │  │                                                                                         │ │ │
│  │  │ ( ) Saldo Decrescente                                                                  │ │ │
│  │  │     ℹ️ Depreciação acelerada (uso intensivo no início)                                 │ │ │
│  │  └────────────────────────────────────────────────────────────────────────────────────────┘ │ │
│  │                                                                                              │ │
│  │  Vida Útil Estimada *                         Taxa de Depreciação Anual *                   │ │
│  │  ┌────────────────┐                           ┌────────────────┐                           │ │
│  │  │ 5              │ anos                      │ 20,00%         │ (calculado automaticamente)│ │
│  │  └────────────────┘                           └────────────────┘                           │ │
│  │  ℹ️ Conforme tabela da Receita Federal         ℹ️ 100 / Vida Útil                           │ │
│  │     (Equipamentos de informática: 5 anos)                                                    │ │
│  │                                                                                              │ │
│  │  Valor Residual (% do valor original)                                                        │ │
│  │  ┌────────────────┐                                                                          │ │
│  │  │ 10,00%         │                                                                          │ │
│  │  └────────────────┘                                                                          │ │
│  │  ℹ️ Valor estimado ao final da vida útil (geralmente 5-10%)                                  │ │
│  └──────────────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                                    │
│  ┌──────────────────────────────────────────────────────────────────────────────────────────────┐ │
│  │ SIMULAÇÃO DE DEPRECIAÇÃO                                                                     │ │
│  ├──────────────────────────────────────────────────────────────────────────────────────────────┤ │
│  │                                                                                              │ │
│  │  Valor de Aquisição (exemplo): R$ 2.500,00                                                  │ │
│  │  Vida Útil: 5 anos                                                                           │ │
│  │  Método: Linear                                                                              │ │
│  │  Valor Residual: R$ 250,00 (10%)                                                             │ │
│  │                                                                                              │ │
│  │  ┌────────┬──────────────┬──────────────────┬──────────────────┬──────────────────┐         │ │
│  │  │ Ano    │ Depreciação  │ Valor Depreciado │ Valor Contábil   │ % Depreciado     │         │ │
│  │  ├────────┼──────────────┼──────────────────┼──────────────────┼──────────────────┤         │ │
│  │  │ 0      │ -            │ R$ 0,00          │ R$ 2.500,00      │ 0%               │         │ │
│  │  │ 1      │ R$ 450,00    │ R$ 450,00        │ R$ 2.050,00      │ 20%              │         │ │
│  │  │ 2      │ R$ 450,00    │ R$ 900,00        │ R$ 1.600,00      │ 40%              │         │ │
│  │  │ 3      │ R$ 450,00    │ R$ 1.350,00      │ R$ 1.150,00      │ 60%              │         │ │
│  │  │ 4      │ R$ 450,00    │ R$ 1.800,00      │ R$ 700,00        │ 80%              │         │ │
│  │  │ 5      │ R$ 450,00    │ R$ 2.250,00      │ R$ 250,00        │ 100% (residual)  │         │ │
│  │  └────────┴──────────────┴──────────────────┴──────────────────┴──────────────────┘         │ │
│  │                                                                                              │ │
│  │  ℹ️ Esta simulação é baseada em um ativo de R$ 2.500,00. Valores reais variarão.            │ │
│  └──────────────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                                    │
│                                                     [◄ Voltar]  [Próxima: Fornecedor ►]           │
└────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

### 2.6 Modal - Templates de Tipos Pré-Configurados

**Acionado por:** Botão [📁 Templates]
**Permissão:** `GES.TIPOS_ATIVOS.CREATE`

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ 📁 TEMPLATES DE TIPOS DE ATIVOS                                                            [✖️]     │
├────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                    │
│  ℹ️ Crie rapidamente tipos de ativos usando nossos templates pré-configurados.                     │
│                                                                                                    │
│  ┌──────────────────────────────────────────────────────────────────────────────────────────────┐ │
│  │ 🖥️ HARDWARE                                                                                   │ │
│  ├──────────────────────────────────────────────────────────────────────────────────────────────┤ │
│  │                                                                                              │ │
│  │  ┌──────────────────────────────────────┐  ┌──────────────────────────────────────┐        │ │
│  │  │ 💻 Notebook                           │  │ 🖥️ Desktop                            │        │ │
│  │  │                                       │  │                                       │        │ │
│  │  │ 7 atributos pré-definidos:            │  │ 6 atributos pré-definidos:            │        │ │
│  │  │ • Marca, Modelo, Processador          │  │ • Marca, Modelo, Processador          │        │ │
│  │  │ • RAM, HD/SSD, Tela, Peso             │  │ • RAM, HD/SSD, Monitor                │        │ │
│  │  │                                       │  │                                       │        │ │
│  │  │ Depreciação: 5 anos (20% a.a.)        │  │ Depreciação: 5 anos (20% a.a.)        │        │ │
│  │  │                                       │  │                                       │        │ │
│  │  │            [✅ Usar Template]          │  │            [✅ Usar Template]          │        │ │
│  │  └──────────────────────────────────────┘  └──────────────────────────────────────┘        │ │
│  │                                                                                              │ │
│  │  ┌──────────────────────────────────────┐  ┌──────────────────────────────────────┐        │ │
│  │  │ 📱 Smartphone                         │  │ 🖨️ Impressora                         │        │ │
│  │  │                                       │  │                                       │        │ │
│  │  │ 6 atributos: Marca, Modelo, SO,       │  │ 5 atributos: Marca, Modelo, Tipo      │        │ │
│  │  │ Armazenamento, Câmera, Operadora      │  │ (jato/laser), Velocidade, Rede        │        │ │
│  │  │                                       │  │                                       │        │ │
│  │  │ Depreciação: 3 anos (33% a.a.)        │  │ Depreciação: 5 anos (20% a.a.)        │        │ │
│  │  │            [✅ Usar Template]          │  │            [✅ Usar Template]          │        │ │
│  │  └──────────────────────────────────────┘  └──────────────────────────────────────┘        │ │
│  └──────────────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                                    │
│  ┌──────────────────────────────────────────────────────────────────────────────────────────────┐ │
│  │ 💿 SOFTWARE                                                                                   │ │
│  ├──────────────────────────────────────────────────────────────────────────────────────────────┤ │
│  │                                                                                              │ │
│  │  ┌──────────────────────────────────────┐  ┌──────────────────────────────────────┐        │ │
│  │  │ 💾 Software de Produtividade          │  │ 🎨 Software de Design                 │        │ │
│  │  │                                       │  │                                       │        │ │
│  │  │ 5 atributos: Fabricante, Versão,      │  │ 6 atributos: Fabricante, Versão,      │        │ │
│  │  │ Tipo Licença, Quantidade, Renovação   │  │ Tipo Licença, Qtd, Renovação, Nível   │        │ │
│  │  │                                       │  │                                       │        │ │
│  │  │ Depreciação: Não depreciável          │  │ Depreciação: Não depreciável          │        │ │
│  │  │            [✅ Usar Template]          │  │            [✅ Usar Template]          │        │ │
│  │  └──────────────────────────────────────┘  └──────────────────────────────────────┘        │ │
│  └──────────────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                                    │
│  ┌──────────────────────────────────────────────────────────────────────────────────────────────┐ │
│  │ 📜 LICENÇAS                                                                                   │ │
│  ├──────────────────────────────────────────────────────────────────────────────────────────────┤ │
│  │                                                                                              │ │
│  │  ┌──────────────────────────────────────┐  ┌──────────────────────────────────────┐        │ │
│  │  │ 🪟 Licença de Sistema Operacional     │  │ 🛡️ Licença de Antivírus               │        │ │
│  │  │                                       │  │                                       │        │ │
│  │  │ 4 atributos: Fabricante, Versão,      │  │ 5 atributos: Fabricante, Versão,      │        │ │
│  │  │ Tipo (OEM/Varejo), Chave de Produto   │  │ Tipo, Chave, Data Vencimento          │        │ │
│  │  │                                       │  │                                       │        │ │
│  │  │ Depreciação: Não depreciável          │  │ Depreciação: Não depreciável          │        │ │
│  │  │            [✅ Usar Template]          │  │            [✅ Usar Template]          │        │ │
│  │  └──────────────────────────────────────┘  └──────────────────────────────────────┘        │ │
│  └──────────────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                                    │
│  ┌──────────────────────────────────────────────────────────────────────────────────────────────┐ │
│  │ 🌐 SERVIÇOS E CONTRATOS                                                                       │ │
│  ├──────────────────────────────────────────────────────────────────────────────────────────────┤ │
│  │                                                                                              │ │
│  │  ┌──────────────────────────────────────┐  ┌──────────────────────────────────────┐        │ │
│  │  │ ☁️ Serviço de Cloud                    │  │ 📞 Contrato de Telefonia              │        │ │
│  │  │                                       │  │                                       │        │ │
│  │  │ 8 atributos: Provedor, Plano, Região, │  │ 12 atributos: Operadora, Tipo Plano,  │        │ │
│  │  │ Recursos, Custo Mensal, SLA, Suporte  │  │ Franquia, Valor, Multa Rescisão, etc. │        │ │
│  │  │                                       │  │                                       │        │ │
│  │  │ Depreciação: Não depreciável          │  │ Depreciação: Não depreciável          │        │ │
│  │  │            [✅ Usar Template]          │  │            [✅ Usar Template]          │        │ │
│  │  └──────────────────────────────────────┘  └──────────────────────────────────────┘        │ │
│  └──────────────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                                    │
│  ℹ️ Ao usar um template, você pode personalizar todos os campos antes de salvar.                  │
│                                                                                                    │
│                                                                                        [Fechar]    │
└────────────────────────────────────────────────────────────────────────────────────────────────────┘

DIMENSÕES: 1200x900px
```

---

## 3. Integrações Obrigatórias (Resumo)

- **i18n:** Todas as chaves (tipos_ativos.*, categorias.*, atributos.*, etc.)
- **Auditoria:** TIPO_ATIVO_CREATED, UPDATED, INACTIVATED
- **Permissões:** GES.TIPOS_ATIVOS.VIEW, CREATE, UPDATE, DELETE
- **Central de Funcionalidades:** Registro FUNC-019

---

## 4. Notas de Implementação

**Pontos Críticos:**
- Atributos customizáveis devem ser armazenados em JSON (flexibilidade)
- Validar dependências antes de inativar tipo (ex: ativos vinculados)
- Templates podem ser customizados pelo administrador do sistema
- Depreciação calculada automaticamente via job (Hangfire)

**Prioridades:**
- Fase 1: CRUD básico + Taxonomia + Atributos
- Fase 2: Depreciação + Templates
- Fase 3: Relatórios avançados + Importação em lote

---

## 5. Changelog

| Versão | Data       | Autor             | Alterações                              |
|--------|------------|-------------------|-----------------------------------------|
| 1.0    | 2025-01-18 | Architect Agent   | Criação inicial do wireframe completo   |

---

**FIM DO DOCUMENTO**
