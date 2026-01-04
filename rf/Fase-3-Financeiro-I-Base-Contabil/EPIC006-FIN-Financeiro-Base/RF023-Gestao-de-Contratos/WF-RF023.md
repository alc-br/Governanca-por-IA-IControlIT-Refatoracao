# Wireframes - RF023 - Gestão de Contratos

**Versao:** 1.0
**Data:** 2025-12-18
**RF Relacionado:** [RF023 - Gestão de Contratos](./RF023.md)
**UC Relacionado:** [UC-RF023](./UC-RF023.md)
**Plataforma:** Web (Desktop Only)
**Framework UI:** Fuse Admin Template (Angular 19 + Material 19)

---

## ⚠️ Nota Importante sobre o Fuse

Este projeto utiliza o **Fuse Admin Template**, que já possui:
- ✅ **Header fixo** (toolbar superior com logo, busca, notificações, perfil)
- ✅ **Sidebar/Menu fixo** (navegação lateral com menu expansível)
- ✅ **Footer** (rodapé com copyright e versão)

**Os wireframes neste documento mostram APENAS a área de conteúdo central (content area).**

### Estrutura Geral do Fuse:
```
┌─────────────────────────────────────────────────────┐
│  [Header - Fixo do Fuse]                            │
├─────────────┬───────────────────────────────────────┤
│             │                                       │
│  [Sidebar   │  ┌─────────────────────────────────┐ │
│   Menu      │  │                                 │ │
│   Fixo      │  │  ÁREA DE CONTEÚDO              │ │
│   do Fuse]  │  │  (Wireframes deste documento)   │ │
│             │  │                                 │ │
│             │  └─────────────────────────────────┘ │
│             │                                       │
├─────────────┴───────────────────────────────────────┤
│  [Footer - Fixo do Fuse]                            │
└─────────────────────────────────────────────────────┘
```

---

## Legenda de Símbolos

### Bordas e Estrutura
```
┌─┬─┐  Cantos e divisórias
├─┼─┤  Linhas horizontais/verticais
└─┴─┘  Estrutura de tabela
```

### Componentes de UI
```
[Botão]           Botão clicável
[_________]       Campo de texto
[Dropdown ▼]      Select/Dropdown
☑ Checkbox        Checkbox marcado
☐ Checkbox        Checkbox desmarcado
◉ Radio           Radio button selecionado
○ Radio           Radio button não selecionado
[🔍 Buscar]       Botão com ícone
```

### Ícones Comuns
```
☰  Menu hamburguer
►  Expandir/Próximo
▼  Dropdown aberto
▲  Dropdown fechado
🔍 Buscar
+  Adicionar
×  Fechar/Deletar
✓  Sucesso
✗  Erro
●  Ativo
○  Inativo
⚠  Alerta
ℹ  Informação
← → ↑ ↓  Navegação
📄 Contrato
📊 Dashboard
💰 Valores
📅 Datas
🏢 Fornecedor
```

---

## Navegação entre Telas

### Fluxo Principal
```
[Tela 01 - Dashboard Contratos]
         │
         ├─→ [+ Novo Contrato] ──→ [Tela 02 - Criar Contrato]
         │                                 │
         │                                 └─→ [Salvar] ──→ [Tela 01]
         │
         ├─→ [Ver Detalhes] ──→ [Tela 03 - Detalhes Contrato]
         │                             │
         │                             ├─→ [Editar] ──→ [Tela 04 - Editar]
         │                             │                      │
         │                             │                      └─→ [Salvar] ──→ [Tela 03]
         │                             │
         │                             ├─→ [Ver Anexos] ──→ [Tela 05 - Anexos]
         │                             │
         │                             ├─→ [Ver Aditivos] ──→ [Tela 06 - Aditivos]
         │                             │
         │                             └─→ [Ver Histórico] ──→ [Tela 07 - Histórico]
         │
         └─→ [Alertas] ──→ [Tela 08 - Alertas de Vencimento]
```

---

## Tela 01 - Dashboard de Contratos

### UC Relacionado
- **UC00:** Listar Contratos
- **Ator:** Administrador, Gestor de Contratos, Financeiro

### Layout Desktop (Área de Conteúdo - Fuse)

**Nota:** Header e Sidebar são do Fuse (fixos). Este wireframe mostra apenas a área de conteúdo central.

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│  ÁREA DE CONTEÚDO (Content Area)                                                                │
├─────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                  │
│  Breadcrumb: Home > Gestão > Contratos                                     [+ Novo Contrato]   │
│                                                                                                  │
│  ┌──────────────────────────────────────────────────────────────────────────────────────────┐  │
│  │ 📊 Resumo de Contratos                                                                   │  │
│  ├──────────────────────────────────────────────────────────────────────────────────────────┤  │
│  │                                                                                          │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │  │
│  │  │ 📄 Total    │  │ ● Vigentes  │  │ ⚠ Vencendo  │  │ ○ Vencidos  │  │ 💰 Custo    │  │  │
│  │  │ Contratos   │  │             │  │ (30 dias)   │  │             │  │ Mensal      │  │  │
│  │  │             │  │             │  │             │  │             │  │             │  │  │
│  │  │     45      │  │      38     │  │      5      │  │      2      │  │ R$ 125.450  │  │  │
│  │  │  contratos  │  │   ativos    │  │   alertas   │  │  vencidos   │  │   /mês      │  │  │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘  │  │
│  │                                                                                          │  │
│  └──────────────────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                                  │
│  ┌──────────────────────────────────────────────────────────────────────────────────────────┐  │
│  │ Filtros                                                                              [×] │  │
│  ├──────────────────────────────────────────────────────────────────────────────────────────┤  │
│  │                                                                                          │  │
│  │  Número: [_____________]  Nome: [_______________________]  Fornecedor: [Todos     ▼]    │  │
│  │                                                                                          │  │
│  │  Tipo: [Todos ▼]          Status: ● Vigentes  ○ Vencidos  ○ Todos                       │  │
│  │                                                                                          │  │
│  │  Vencimento: De [__/__/____] Até [__/__/____]        Valor: R$ [______] a R$ [______]   │  │
│  │                                                                                          │  │
│  │  [Limpar Filtros]                                      [📊 Dashboard] [📄 Exportar]     │  │
│  │                                                                                          │  │
│  └──────────────────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                                  │
│  Resultados: 45 contratos encontrados                                  [Visualização: ☰ Lista] │
│                                                                                                  │
│  ┌──────────────────────────────────────────────────────────────────────────────────────────┐  │
│  │ Número   │ Nome Contrato            │ Fornecedor       │ Vigência      │ Valor   │ Ações   │  │
│  ├──────────┼──────────────────────────┼──────────────────┼───────────────┼─────────┼─────────┤  │
│  │CONT-2024 │ Link Internet 1Gbps      │ Vivo Empresas    │ ● 12/25-12/26│ R$ 8.500│ [👁️][✏️]│  │
│  │CONT-2023 │ Telefonia Móvel Corporat │ Claro Brasil     │ ● 01/25-01/26│ R$ 12.30│ [👁️][✏️]│  │
│  │CONT-2022 │ AWS Cloud Services       │ Amazon Web Serv. │ ⚠ 01/25-02/25│ R$ 45.00│ [👁️][✏️]│  │
│  │CONT-2021 │ Microsoft 365 E5         │ Microsoft Corp.  │ ● 03/25-03/26│ R$ 18.50│ [👁️][✏️]│  │
│  │CONT-2020 │ Licenças Adobe Creative  │ Adobe Inc.       │ ⚠ 02/25-02/25│ R$ 6.750│ [👁️][✏️]│  │
│  │CONT-2019 │ Suporte SAP              │ SAP Brasil       │ ● 06/24-06/26│ R$ 25.00│ [👁️][✏️]│  │
│  │CONT-2018 │ Data Center Colocation   │ Equinix Brasil   │ ● 09/24-09/27│ R$ 15.20│ [👁️][✏️]│  │
│  │CONT-2017 │ Outsourcing Service Desk │ Stefanini IT     │ ○ 11/23-11/24│ R$ 22.00│ [👁️][✏️]│  │
│  └──────────────────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                                  │
│  [Ações em lote ▼]                                        « [1] [2] »                           │
│                                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### Estados da Tela

#### Estado: Loading
```
┌─────────────────────────────────┐
│                                 │
│         ⏳ Carregando...        │
│                                 │
│     [████████░░░░] 60%          │
│                                 │
└─────────────────────────────────┘
```

#### Estado: Vazio (Sem Dados)
```
┌─────────────────────────────────┐
│                                 │
│      📄                         │
│  Nenhum contrato cadastrado     │
│                                 │
│   [+ Cadastrar Primeiro         │
│      Contrato]                  │
│                                 │
└─────────────────────────────────┘
```

#### Estado: Erro
```
┌─────────────────────────────────┐
│                                 │
│   ✗ Erro ao carregar dados      │
│                                 │
│   Mensagem: [Detalhes do erro]  │
│                                 │
│   [Tentar Novamente]            │
│                                 │
└─────────────────────────────────┘
```

---

## Tela 02 - Criar Novo Contrato

### UC Relacionado
- **UC01:** Criar Contrato
- **Ator:** Administrador, Gestor de Contratos

### Layout Desktop (Área de Conteúdo - Fuse)

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│  ÁREA DE CONTEÚDO                                                                                │
├─────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                  │
│  Breadcrumb: Home > Gestão > Contratos > Novo Contrato                                         │
│                                                                                                  │
│  ┌──────────────────────────────────────────────────────────────────────────────────────────┐  │
│  │ Novo Contrato                                                                        [×] │  │
│  ├──────────────────────────────────────────────────────────────────────────────────────────┤  │
│  │                                                                                          │  │
│  │  ⚠️ Campos marcados com * são obrigatórios                                              │  │
│  │                                                                                          │  │
│  │  ┌────────────────────────────────────────────────────────────────────────────┐         │  │
│  │  │ 📄 Informações Básicas                                                     │         │  │
│  │  ├────────────────────────────────────────────────────────────────────────────┤         │  │
│  │  │                                                                            │         │  │
│  │  │  Número do Contrato *                                                      │         │  │
│  │  │  [CONT-_______________________]                                            │         │  │
│  │  │  ℹ️ Número único de identificação do contrato                              │         │  │
│  │  │                                                                            │         │  │
│  │  │  Nome do Contrato *                                                        │         │  │
│  │  │  [_________________________________________________________________]       │         │  │
│  │  │                                                                            │         │  │
│  │  │  Tipo de Contrato *                     Categoria                          │         │  │
│  │  │  [Selecione tipo           ▼]          [Selecione categoria      ▼]       │         │  │
│  │  │  (Telecom, Cloud, Software...)          (Link Dados, VPN, etc.)            │         │  │
│  │  │                                                                            │         │  │
│  │  │  Descrição                                                                 │         │  │
│  │  │  [_________________________________________________________________]       │         │  │
│  │  │  [_________________________________________________________________]       │         │  │
│  │  │  [_________________________________________________________________]       │         │  │
│  │  │                                                                            │         │  │
│  │  └────────────────────────────────────────────────────────────────────────────┘         │  │
│  │                                                                                          │  │
│  │  ┌────────────────────────────────────────────────────────────────────────────┐         │  │
│  │  │ 🏢 Fornecedor e Vinculações                                                │         │  │
│  │  ├────────────────────────────────────────────────────────────────────────────┤         │  │
│  │  │                                                                            │         │  │
│  │  │  Fornecedor *                                   [🔍 Buscar Fornecedor]     │         │  │
│  │  │  [Selecione fornecedor                                              ▼]     │         │  │
│  │  │                                                                            │         │  │
│  │  │  Empresa Principal *                    Filial (Opcional)                  │         │  │
│  │  │  [Selecione empresa             ▼]    [Selecione filial            ▼]     │         │  │
│  │  │                                                                            │         │  │
│  │  │  Gestor Responsável *                   E-mail Gestor *                    │         │  │
│  │  │  [Selecione gestor              ▼]    [gestor@empresa.com.br______]       │         │  │
│  │  │                                                                            │         │  │
│  │  └────────────────────────────────────────────────────────────────────────────┘         │  │
│  │                                                                                          │  │
│  │  ┌────────────────────────────────────────────────────────────────────────────┐         │  │
│  │  │ 📅 Vigência e Renovação                                                    │         │  │
│  │  ├────────────────────────────────────────────────────────────────────────────┤         │  │
│  │  │                                                                            │         │  │
│  │  │  Data de Início *                       Data de Fim *                      │         │  │
│  │  │  [__/__/____]                           [__/__/____]                       │         │  │
│  │  │                                                                            │         │  │
│  │  │  Prazo Calculado: __ meses             [🔄 Recalcular]                    │         │  │
│  │  │                                                                            │         │  │
│  │  │  Renovação Automática:                                                     │         │  │
│  │  │  ◉ Sim (Renovar automaticamente ao vencer)                                │         │  │
│  │  │  ○ Não (Exigir aprovação manual para renovação)                           │         │  │
│  │  │                                                                            │         │  │
│  │  │  Prazo para Notificação de Vencimento:  [30_] dias antes                  │         │  │
│  │  │  ℹ️ Sistema enviará alerta aos gestores quando faltar este prazo          │         │  │
│  │  │                                                                            │         │  │
│  │  └────────────────────────────────────────────────────────────────────────────┘         │  │
│  │                                                                                          │  │
│  │  ┌────────────────────────────────────────────────────────────────────────────┐         │  │
│  │  │ 💰 Valores e Pagamento                                                     │         │  │
│  │  ├────────────────────────────────────────────────────────────────────────────┤         │  │
│  │  │                                                                            │         │  │
│  │  │  Valor Mensal *                         Valor Total *                      │         │  │
│  │  │  R$ [__________,__]                     R$ [__________,__]                 │         │  │
│  │  │                                         (Calculado: Mensal × Prazo)        │         │  │
│  │  │                                                                            │         │  │
│  │  │  Multa Rescisória                       Dia de Vencimento                  │         │  │
│  │  │  R$ [__________,__]                     [__] (1 a 31)                      │         │  │
│  │  │                                                                            │         │  │
│  │  │  Forma de Pagamento *                   Centro de Custo *                  │         │  │
│  │  │  [Selecione forma       ▼]             [Selecione centro custo    ▼]      │         │  │
│  │  │  (Boleto, Transferência, Cartão)                                           │         │  │
│  │  │                                                                            │         │  │
│  │  │  Reajuste Anual:                                                           │         │  │
│  │  │  Índice: [IGPM            ▼]           Percentual: [____,__]%              │         │  │
│  │  │                                                                            │         │  │
│  │  └────────────────────────────────────────────────────────────────────────────┘         │  │
│  │                                                                                          │  │
│  │  ┌────────────────────────────────────────────────────────────────────────────┐         │  │
│  │  │ ⚙️ SLA e Configurações Adicionais                                          │         │  │
│  │  ├────────────────────────────────────────────────────────────────────────────┤         │  │
│  │  │                                                                            │         │  │
│  │  │  Possui SLA?                                                               │         │  │
│  │  │  ◉ Sim                                                                     │         │  │
│  │  │  ○ Não                                                                     │         │  │
│  │  │                                                                            │         │  │
│  │  │  [Exibido se "Sim"]                                                        │         │  │
│  │  │  Tempo de Resposta SLA:  [__] horas                                        │         │  │
│  │  │  Percentual de Disponibilidade: [__,__]%                                   │         │  │
│  │  │  Penalidade por Descumprimento: R$ [__________,__]                         │         │  │
│  │  │                                                                            │         │  │
│  │  │  Observações Internas:                                                     │         │  │
│  │  │  [_________________________________________________________________]       │         │  │
│  │  │  [_________________________________________________________________]       │         │  │
│  │  │                                                                            │         │  │
│  │  └────────────────────────────────────────────────────────────────────────────┘         │  │
│  │                                                                                          │  │
│  │  [Cancelar]                                                          [Salvar Contrato]  │  │
│  │                                                                                          │  │
│  └──────────────────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### Validações da Tela

```
┌──────────────────────────────────────────────────────────┐
│ ⚠️ Erros de Validação                                    │
├──────────────────────────────────────────────────────────┤
│                                                          │
│ • Número do Contrato: Campo obrigatório                 │
│ • Data de Fim: Deve ser posterior à Data de Início      │
│ • Valor Mensal: Deve ser maior que zero                 │
│ • Fornecedor: Selecione um fornecedor válido            │
│ • Dia de Vencimento: Deve estar entre 1 e 31            │
│                                                          │
│ Corrija os erros acima para continuar.                   │
│                                                          │
│                                        [OK, Entendi]     │
└──────────────────────────────────────────────────────────┘
```

---

## Tela 03 - Detalhes do Contrato

### UC Relacionado
- **UC02:** Visualizar Contrato
- **Ator:** Administrador, Gestor de Contratos, Financeiro

### Layout Desktop (Área de Conteúdo - Fuse)

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│  ÁREA DE CONTEÚDO                                                                                │
├─────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                  │
│  Breadcrumb: Home > Gestão > Contratos > CONT-2024-001                                         │
│                                                                                                  │
│  ┌──────────────────────────────────────────────────────────────────────────────────────────┐  │
│  │ [← Voltar]    CONT-2024-001 - Link Internet 1Gbps       [✏️ Editar] [📎 Anexos] [🗑️ Excl] │  │
│  ├──────────────────────────────────────────────────────────────────────────────────────────┤  │
│  │                                                                                          │  │
│  │  ┌───────────────────────────────────┐  ┌──────────────────────────────────────────┐   │  │
│  │  │ 📄 Informações do Contrato        │  │ 💰 Valores e Financeiro                 │   │  │
│  │  ├───────────────────────────────────┤  ├──────────────────────────────────────────┤   │  │
│  │  │                                   │  │                                          │   │  │
│  │  │ Número:     CONT-2024-001         │  │ Valor Mensal:   R$ 8.500,00             │   │  │
│  │  │ Nome:       Link Internet 1Gbps   │  │ Valor Total:    R$ 102.000,00           │   │  │
│  │  │ Status:     ● VIGENTE              │  │ Prazo:          12 meses                │   │  │
│  │  │                                   │  │                                          │   │  │
│  │  │ 🏢 Fornecedor:                    │  │ Forma Pgto:     Boleto Bancário         │   │  │
│  │  │ Vivo Empresas                     │  │ Vencimento:     Dia 10                  │   │  │
│  │  │ CNPJ: 02.558.157/0001-62          │  │ Centro Custo:   TI - Infraestrutura     │   │  │
│  │  │                                   │  │                                          │   │  │
│  │  │ 📋 Tipo/Categoria:                │  │ Multa Rescisão: R$ 17.000,00            │   │  │
│  │  │ Telecom > Link de Dados           │  │ Reajuste:       IGPM (5,2% a.a.)        │   │  │
│  │  │                                   │  │                                          │   │  │
│  │  │ 🏢 Empresa:                       │  │ ⚠️ Próximo Vencimento:                  │   │  │
│  │  │ IControlIT Ltda (Matriz)          │  │    10/01/2026 - Faltam 15 dias          │   │  │
│  │  │                                   │  │                                          │   │  │
│  │  │ 👤 Gestor Responsável:            │  └──────────────────────────────────────────┘   │  │
│  │  │ João Silva                        │                                                 │  │
│  │  │ joao.silva@icontrolit.com.br      │  ┌──────────────────────────────────────────┐   │  │
│  │  │                                   │  │ 📅 Vigência e Renovação                 │   │  │
│  │  └───────────────────────────────────┘  ├──────────────────────────────────────────┤   │  │
│  │                                         │                                          │   │  │
│  │  ┌───────────────────────────────────┐  │ Início:         12/12/2024              │   │  │
│  │  │ ⚙️ SLA e Configurações            │  │ Fim:            12/12/2025              │   │  │
│  │  ├───────────────────────────────────┤  │ Prazo:          12 meses                │   │  │
│  │  │                                   │  │                                          │   │  │
│  │  │ Possui SLA:      ✓ Sim            │  │ Renovação Auto: ✓ Sim                   │   │  │
│  │  │                                   │  │ Notificação:    30 dias antes           │   │  │
│  │  │ Tempo Resposta:  4 horas          │  │                                          │   │  │
│  │  │ Disponibilidade: 99,9%            │  │ [📊 Ver Timeline]                       │   │  │
│  │  │ Penalidade:      R$ 500/hora      │  │                                          │   │  │
│  │  │                                   │  └──────────────────────────────────────────┘   │  │
│  │  └───────────────────────────────────┘                                                 │  │
│  │                                                                                          │  │
│  │  ┌──────────────────────────────────────────────────────────────────────────┐           │  │
│  │  │ 📎 Anexos (3 arquivos)                                                   │           │  │
│  │  ├──────────────────────────────────────────────────────────────────────────┤           │  │
│  │  │                                                                          │           │  │
│  │  │  • contrato-vivo-assinado.pdf (1.2 MB) - 12/12/2024  [⬇️] [👁️] [🗑️]    │           │  │
│  │  │  • proposta-comercial.pdf (850 KB) - 01/12/2024      [⬇️] [👁️] [🗑️]    │           │  │
│  │  │  • sla-acordo.pdf (450 KB) - 12/12/2024              [⬇️] [👁️] [🗑️]    │           │  │
│  │  │                                                                          │           │  │
│  │  │  [+ Adicionar Anexo]                                                     │           │  │
│  │  │                                                                          │           │  │
│  │  └──────────────────────────────────────────────────────────────────────────┘           │  │
│  │                                                                                          │  │
│  │  ┌──────────────────────────────────────────────────────────────────────────┐           │  │
│  │  │ 📝 Aditivos Contratuais (2 aditivos)                                     │           │  │
│  │  ├──────────────────────────────────────────────────────────────────────────┤           │  │
│  │  │                                                                          │           │  │
│  │  │  • Aditivo 001 - Upgrade de banda 500Mbps → 1Gbps                       │           │  │
│  │  │    Data: 15/03/2025 | Valor: +R$ 2.500/mês | [Ver Detalhes]             │           │  │
│  │  │                                                                          │           │  │
│  │  │  • Aditivo 002 - Extensão de prazo 6 meses                               │           │  │
│  │  │    Data: 01/06/2025 | Prazo: +6 meses | [Ver Detalhes]                  │           │  │
│  │  │                                                                          │           │  │
│  │  │  [+ Adicionar Aditivo]                                                   │           │  │
│  │  │                                                                          │           │  │
│  │  └──────────────────────────────────────────────────────────────────────────┘           │  │
│  │                                                                                          │  │
│  │  ┌──────────────────────────────────────────────────────────────────────────┐           │  │
│  │  │ 📊 Observações e Notas Internas                                          │           │  │
│  │  ├──────────────────────────────────────────────────────────────────────────┤           │  │
│  │  │                                                                          │           │  │
│  │  │  Contrato negociado com desconto de 15% sobre tabela.                   │           │  │
│  │  │  IP fixo dedicado incluso no valor mensal.                               │           │  │
│  │  │  Equipe técnica disponível 24x7 para suporte.                            │           │  │
│  │  │                                                                          │           │  │
│  │  │  [✏️ Editar Observações]                                                 │           │  │
│  │  │                                                                          │           │  │
│  │  └──────────────────────────────────────────────────────────────────────────┘           │  │
│  │                                                                                          │  │
│  │  ┌──────────────────────────────────────────────────────────────────────────┐           │  │
│  │  │ 📋 Auditoria                                                             │           │  │
│  │  ├──────────────────────────────────────────────────────────────────────────┤           │  │
│  │  │                                                                          │           │  │
│  │  │  Criado em:          12/12/2024 às 14:30 por João Silva                 │           │  │
│  │  │  Última atualização: 15/12/2024 às 10:15 por Maria Santos               │           │  │
│  │  │                                                                          │           │  │
│  │  │  [Ver Histórico Completo]                                                │           │  │
│  │  │                                                                          │           │  │
│  │  └──────────────────────────────────────────────────────────────────────────┘           │  │
│  │                                                                                          │  │
│  └──────────────────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Tela 04 - Editar Contrato

### UC Relacionado
- **UC03:** Editar Contrato
- **Ator:** Administrador, Gestor de Contratos

### Layout Desktop (Área de Conteúdo - Fuse)

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│  ÁREA DE CONTEÚDO                                                                                │
├─────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                  │
│  Breadcrumb: Home > Gestão > Contratos > Editar - CONT-2024-001                                │
│                                                                                                  │
│  ┌──────────────────────────────────────────────────────────────────────────────────────────┐  │
│  │ Editar Contrato                                                                      [×] │  │
│  ├──────────────────────────────────────────────────────────────────────────────────────────┤  │
│  │                                                                                          │  │
│  │  ⚠️ Campos marcados com * são obrigatórios                                              │  │
│  │                                                                                          │  │
│  │  ┌────────────────────────────────────────────────────────────────────────────┐         │  │
│  │  │ 📄 Informações Básicas                                                     │         │  │
│  │  ├────────────────────────────────────────────────────────────────────────────┤         │  │
│  │  │                                                                            │         │  │
│  │  │  Número do Contrato *                                                      │         │  │
│  │  │  [CONT-2024-001_______________]                                            │         │  │
│  │  │                                                                            │         │  │
│  │  │  Nome do Contrato *                                                        │         │  │
│  │  │  [Link Internet 1Gbps______________________________________________]       │         │  │
│  │  │                                                                            │         │  │
│  │  │  Tipo de Contrato *                     Categoria                          │         │  │
│  │  │  [Telecom                  ▼]          [Link de Dados            ▼]       │         │  │
│  │  │                                                                            │         │  │
│  │  │  Descrição                                                                 │         │  │
│  │  │  [Link dedicado 1Gbps com IP fixo_________________________________]       │         │  │
│  │  │  [SLA 99,9% de disponibilidade_____________________________________]       │         │  │
│  │  │  [_______________________________________________________________]       │         │  │
│  │  │                                                                            │         │  │
│  │  └────────────────────────────────────────────────────────────────────────────┘         │  │
│  │                                                                                          │  │
│  │  ┌────────────────────────────────────────────────────────────────────────────┐         │  │
│  │  │ 🏢 Fornecedor e Vinculações                                                │         │  │
│  │  ├────────────────────────────────────────────────────────────────────────────┤         │  │
│  │  │                                                                            │         │  │
│  │  │  Fornecedor *                                   [🔍 Buscar]                │         │  │
│  │  │  [Vivo Empresas                                                     ▼]     │         │  │
│  │  │                                                                            │         │  │
│  │  │  Empresa Principal *                    Filial (Opcional)                  │         │  │
│  │  │  [IControlIT Ltda           ▼]        [Nenhuma                    ▼]      │         │  │
│  │  │                                                                            │         │  │
│  │  │  Gestor Responsável *                   E-mail Gestor *                    │         │  │
│  │  │  [João Silva                ▼]        [joao.silva@icontrolit.com.br]      │         │  │
│  │  │                                                                            │         │  │
│  │  └────────────────────────────────────────────────────────────────────────────┘         │  │
│  │                                                                                          │  │
│  │  ┌────────────────────────────────────────────────────────────────────────────┐         │  │
│  │  │ 📅 Vigência e Renovação                                                    │         │  │
│  │  ├────────────────────────────────────────────────────────────────────────────┤         │  │
│  │  │                                                                            │         │  │
│  │  │  Data de Início *                       Data de Fim *                      │         │  │
│  │  │  [12/12/2024]                           [12/12/2025]                       │         │  │
│  │  │                                                                            │         │  │
│  │  │  Prazo Calculado: 12 meses             [🔄 Recalcular]                    │         │  │
│  │  │                                                                            │         │  │
│  │  │  Renovação Automática:                                                     │         │  │
│  │  │  ◉ Sim                                                                     │         │  │
│  │  │  ○ Não                                                                     │         │  │
│  │  │                                                                            │         │  │
│  │  │  Prazo para Notificação:  [30_] dias antes do vencimento                  │         │  │
│  │  │                                                                            │         │  │
│  │  └────────────────────────────────────────────────────────────────────────────┘         │  │
│  │                                                                                          │  │
│  │  ┌────────────────────────────────────────────────────────────────────────────┐         │  │
│  │  │ 💰 Valores e Pagamento                                                     │         │  │
│  │  ├────────────────────────────────────────────────────────────────────────────┤         │  │
│  │  │                                                                            │         │  │
│  │  │  Valor Mensal *                         Valor Total *                      │         │  │
│  │  │  R$ [8.500,00]                          R$ [102.000,00]                    │         │  │
│  │  │                                                                            │         │  │
│  │  │  Multa Rescisória                       Dia de Vencimento                  │         │  │
│  │  │  R$ [17.000,00]                         [10]                               │         │  │
│  │  │                                                                            │         │  │
│  │  │  Forma de Pagamento *                   Centro de Custo *                  │         │  │
│  │  │  [Boleto Bancário       ▼]             [TI - Infraestrutura      ▼]       │         │  │
│  │  │                                                                            │         │  │
│  │  │  Reajuste Anual:                                                           │         │  │
│  │  │  Índice: [IGPM            ▼]           Percentual: [5,20]%                 │         │  │
│  │  │                                                                            │         │  │
│  │  └────────────────────────────────────────────────────────────────────────────┘         │  │
│  │                                                                                          │  │
│  │  ┌────────────────────────────────────────────────────────────────────────────┐         │  │
│  │  │ ⚙️ SLA e Configurações                                                     │         │  │
│  │  ├────────────────────────────────────────────────────────────────────────────┤         │  │
│  │  │                                                                            │         │  │
│  │  │  Possui SLA?                                                               │         │  │
│  │  │  ◉ Sim                                                                     │         │  │
│  │  │  ○ Não                                                                     │         │  │
│  │  │                                                                            │         │  │
│  │  │  Tempo de Resposta SLA:  [4__] horas                                       │         │  │
│  │  │  Percentual de Disponibilidade: [99,90]%                                   │         │  │
│  │  │  Penalidade por Descumprimento: R$ [500,00]/hora                           │         │  │
│  │  │                                                                            │         │  │
│  │  │  Status do Contrato:                                                       │         │  │
│  │  │  ◉ Ativo                                                                   │         │  │
│  │  │  ○ Inativo                                                                 │         │  │
│  │  │  ○ Suspenso                                                                │         │  │
│  │  │                                                                            │         │  │
│  │  └────────────────────────────────────────────────────────────────────────────┘         │  │
│  │                                                                                          │  │
│  │  [Cancelar]                                                        [Salvar Alterações]  │  │
│  │                                                                                          │  │
│  └──────────────────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Tela 05 - Gerenciar Anexos

### UC Relacionado
- **UC02:** Visualizar Contrato - Gerenciar Anexos
- **Ator:** Administrador, Gestor de Contratos

### Layout Desktop (Área de Conteúdo - Fuse)

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│  ÁREA DE CONTEÚDO                                                                                │
├─────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                  │
│  Breadcrumb: Home > Gestão > Contratos > CONT-2024-001 > Anexos                                │
│                                                                                                  │
│  ┌──────────────────────────────────────────────────────────────────────────────────────────┐  │
│  │ [← Voltar]         Anexos do Contrato CONT-2024-001              [+ Upload Anexo]        │  │
│  ├──────────────────────────────────────────────────────────────────────────────────────────┤  │
│  │                                                                                          │  │
│  │  ┌────────────────────────────────────────────────────────────────────────────┐         │  │
│  │  │ 📎 Anexos do Contrato (3 arquivos - 2.5 MB total)                         │         │  │
│  │  ├────────────────────────────────────────────────────────────────────────────┤         │  │
│  │  │                                                                            │         │  │
│  │  │  ┌──────────────────────────────────────────────────────────────────┐     │         │  │
│  │  │  │ 📄 contrato-vivo-assinado.pdf                                    │     │         │  │
│  │  │  ├──────────────────────────────────────────────────────────────────┤     │         │  │
│  │  │  │ Tamanho: 1.2 MB                                                  │     │         │  │
│  │  │  │ Tipo: Contrato Assinado                                          │     │         │  │
│  │  │  │ Uploaded em: 12/12/2024 14:45 por João Silva                     │     │         │  │
│  │  │  │                                                                  │     │         │  │
│  │  │  │ [⬇️ Download] [👁️ Visualizar] [✏️ Renomear] [🗑️ Excluir]        │     │         │  │
│  │  │  └──────────────────────────────────────────────────────────────────┘     │         │  │
│  │  │                                                                            │         │  │
│  │  │  ┌──────────────────────────────────────────────────────────────────┐     │         │  │
│  │  │  │ 📄 proposta-comercial.pdf                                        │     │         │  │
│  │  │  ├──────────────────────────────────────────────────────────────────┤     │         │  │
│  │  │  │ Tamanho: 850 KB                                                  │     │         │  │
│  │  │  │ Tipo: Proposta Comercial                                         │     │         │  │
│  │  │  │ Uploaded em: 01/12/2024 09:30 por Maria Santos                   │     │         │  │
│  │  │  │                                                                  │     │         │  │
│  │  │  │ [⬇️ Download] [👁️ Visualizar] [✏️ Renomear] [🗑️ Excluir]        │     │         │  │
│  │  │  └──────────────────────────────────────────────────────────────────┘     │         │  │
│  │  │                                                                            │         │  │
│  │  │  ┌──────────────────────────────────────────────────────────────────┐     │         │  │
│  │  │  │ 📄 sla-acordo.pdf                                                │     │         │  │
│  │  │  ├──────────────────────────────────────────────────────────────────┤     │         │  │
│  │  │  │ Tamanho: 450 KB                                                  │     │         │  │
│  │  │  │ Tipo: SLA                                                        │     │         │  │
│  │  │  │ Uploaded em: 12/12/2024 14:50 por João Silva                     │     │         │  │
│  │  │  │                                                                  │     │         │  │
│  │  │  │ [⬇️ Download] [👁️ Visualizar] [✏️ Renomear] [🗑️ Excluir]        │     │         │  │
│  │  │  └──────────────────────────────────────────────────────────────────┘     │         │  │
│  │  │                                                                            │         │  │
│  │  └────────────────────────────────────────────────────────────────────────────┘         │  │
│  │                                                                                          │  │
│  │  ┌────────────────────────────────────────────────────────────────────────────┐         │  │
│  │  │ ➕ Upload de Novo Anexo                                                    │         │  │
│  │  ├────────────────────────────────────────────────────────────────────────────┤         │  │
│  │  │                                                                            │         │  │
│  │  │  Tipo de Anexo *                                                           │         │  │
│  │  │  [Selecione tipo                                                    ▼]     │         │  │
│  │  │  (Contrato Assinado, Proposta, SLA, Aditivo, Nota Fiscal, Outros)          │         │  │
│  │  │                                                                            │         │  │
│  │  │  Descrição (Opcional)                                                      │         │  │
│  │  │  [_________________________________________________________________]       │         │  │
│  │  │                                                                            │         │  │
│  │  │  ┌────────────────────────────────────────────────────────────┐           │         │  │
│  │  │  │                                                            │           │         │  │
│  │  │  │         [📁 Clique ou arraste arquivos aqui]               │           │         │  │
│  │  │  │                                                            │           │         │  │
│  │  │  │   Formatos aceitos: PDF, DOC, DOCX, XLS, XLSX              │           │         │  │
│  │  │  │   Tamanho máximo: 10 MB por arquivo                        │           │         │  │
│  │  │  │                                                            │           │         │  │
│  │  │  └────────────────────────────────────────────────────────────┘           │         │  │
│  │  │                                                                            │         │  │
│  │  │  [Cancelar]                                              [Upload Arquivo]  │         │  │
│  │  │                                                                            │         │  │
│  │  └────────────────────────────────────────────────────────────────────────────┘         │  │
│  │                                                                                          │  │
│  └──────────────────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Tela 06 - Aditivos Contratuais

### UC Relacionado
- **UC02:** Visualizar Contrato - Gerenciar Aditivos
- **Ator:** Administrador, Gestor de Contratos

### Layout Desktop (Área de Conteúdo - Fuse)

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│  ÁREA DE CONTEÚDO                                                                                │
├─────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                  │
│  Breadcrumb: Home > Gestão > Contratos > CONT-2024-001 > Aditivos                              │
│                                                                                                  │
│  ┌──────────────────────────────────────────────────────────────────────────────────────────┐  │
│  │ [← Voltar]       Aditivos do Contrato CONT-2024-001           [+ Novo Aditivo]           │  │
│  ├──────────────────────────────────────────────────────────────────────────────────────────┤  │
│  │                                                                                          │  │
│  │  ┌────────────────────────────────────────────────────────────────────────────┐         │  │
│  │  │ 📝 Aditivos Contratuais (2 aditivos registrados)                          │         │  │
│  │  ├────────────────────────────────────────────────────────────────────────────┤         │  │
│  │  │                                                                            │         │  │
│  │  │  ┌──────────────────────────────────────────────────────────────────┐     │         │  │
│  │  │  │ 📄 Aditivo 001 - Upgrade de Banda                                │     │         │  │
│  │  │  ├──────────────────────────────────────────────────────────────────┤     │         │  │
│  │  │  │                                                                  │     │         │  │
│  │  │  │ Número:      ADIT-001/2025                                       │     │         │  │
│  │  │  │ Data:        15/03/2025                                          │     │         │  │
│  │  │  │ Tipo:        Alteração de Escopo                                │     │         │  │
│  │  │  │                                                                  │     │         │  │
│  │  │  │ Descrição:                                                       │     │         │  │
│  │  │  │ Upgrade de banda de 500Mbps para 1Gbps.                         │     │         │  │
│  │  │  │ Aumento de valor mensal em R$ 2.500,00.                         │     │         │  │
│  │  │  │                                                                  │     │         │  │
│  │  │  │ Impacto Financeiro:                                              │     │         │  │
│  │  │  │ • Valor Anterior:  R$ 6.000,00/mês                              │     │         │  │
│  │  │  │ • Novo Valor:      R$ 8.500,00/mês                              │     │         │  │
│  │  │  │ • Variação:        +R$ 2.500,00/mês (+41,7%)                    │     │         │  │
│  │  │  │                                                                  │     │         │  │
│  │  │  │ Responsável:  João Silva                                         │     │         │  │
│  │  │  │ Aprovador:    Carlos Diretor                                     │     │         │  │
│  │  │  │                                                                  │     │         │  │
│  │  │  │ [👁️ Ver Detalhes] [📎 Anexos (1)] [✏️ Editar] [🗑️ Excluir]     │     │         │  │
│  │  │  └──────────────────────────────────────────────────────────────────┘     │         │  │
│  │  │                                                                            │         │  │
│  │  │  ┌──────────────────────────────────────────────────────────────────┐     │         │  │
│  │  │  │ 📄 Aditivo 002 - Extensão de Prazo                               │     │         │  │
│  │  │  ├──────────────────────────────────────────────────────────────────┤     │         │  │
│  │  │  │                                                                  │     │         │  │
│  │  │  │ Número:      ADIT-002/2025                                       │     │         │  │
│  │  │  │ Data:        01/06/2025                                          │     │         │  │
│  │  │  │ Tipo:        Prorrogação de Vigência                            │     │         │  │
│  │  │  │                                                                  │     │         │  │
│  │  │  │ Descrição:                                                       │     │         │  │
│  │  │  │ Prorrogação do contrato por 6 meses adicionais.                 │     │         │  │
│  │  │  │ Mantido mesmo valor mensal.                                      │     │         │  │
│  │  │  │                                                                  │     │         │  │
│  │  │  │ Impacto de Vigência:                                             │     │         │  │
│  │  │  │ • Data Fim Anterior:  12/12/2025                                │     │         │  │
│  │  │  │ • Nova Data Fim:      12/06/2026                                │     │         │  │
│  │  │  │ • Extensão:           +6 meses                                   │     │         │  │
│  │  │  │                                                                  │     │         │  │
│  │  │  │ Valor Total Adicional: R$ 51.000,00 (6 × R$ 8.500,00)          │     │         │  │
│  │  │  │                                                                  │     │         │  │
│  │  │  │ Responsável:  Maria Santos                                       │     │         │  │
│  │  │  │ Aprovador:    Carlos Diretor                                     │     │         │  │
│  │  │  │                                                                  │     │         │  │
│  │  │  │ [👁️ Ver Detalhes] [📎 Anexos (0)] [✏️ Editar] [🗑️ Excluir]     │     │         │  │
│  │  │  └──────────────────────────────────────────────────────────────────┘     │         │  │
│  │  │                                                                            │         │  │
│  │  └────────────────────────────────────────────────────────────────────────────┘         │  │
│  │                                                                                          │  │
│  └──────────────────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Tela 07 - Histórico de Alterações

### UC Relacionado
- **UC02:** Visualizar Contrato - Auditoria
- **Ator:** Administrador, Gestor de Contratos, Auditor

### Layout Desktop (Área de Conteúdo - Fuse)

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│  ÁREA DE CONTEÚDO                                                                                │
├─────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                  │
│  Breadcrumb: Home > Gestão > Contratos > CONT-2024-001 > Histórico                             │
│                                                                                                  │
│  ┌──────────────────────────────────────────────────────────────────────────────────────────┐  │
│  │ [← Voltar]        Histórico de Alterações - CONT-2024-001                    [📄 Export] │  │
│  ├──────────────────────────────────────────────────────────────────────────────────────────┤  │
│  │                                                                                          │  │
│  │  ┌────────────────────────────────────────────────────────────────────────────┐         │  │
│  │  │ 📋 Linha do Tempo de Alterações (8 eventos registrados)                   │         │  │
│  │  ├────────────────────────────────────────────────────────────────────────────┤         │  │
│  │  │                                                                            │         │  │
│  │  │  ● 18/12/2025 14:22 - Maria Santos                                        │         │  │
│  │  │    ▼ Alteração de Valores                                                 │         │  │
│  │  │      • Valor Mensal: R$ 8.000,00 → R$ 8.500,00                            │         │  │
│  │  │      • Motivo: Reajuste anual conforme IGPM (5,2%)                        │         │  │
│  │  │                                                                            │         │  │
│  │  │  ● 01/06/2025 10:15 - João Silva                                          │         │  │
│  │  │    ▼ Aditivo Criado                                                       │         │  │
│  │  │      • Aditivo 002 - Extensão de prazo +6 meses                           │         │  │
│  │  │      • Data Fim: 12/12/2025 → 12/06/2026                                  │         │  │
│  │  │                                                                            │         │  │
│  │  │  ● 15/03/2025 16:30 - João Silva                                          │         │  │
│  │  │    ▼ Aditivo Criado                                                       │         │  │
│  │  │      • Aditivo 001 - Upgrade de banda                                     │         │  │
│  │  │      • Valor: R$ 6.000,00 → R$ 8.000,00/mês                               │         │  │
│  │  │                                                                            │         │  │
│  │  │  ● 20/02/2025 09:45 - Maria Santos                                        │         │  │
│  │  │    ▼ Anexo Adicionado                                                     │         │  │
│  │  │      • sla-acordo.pdf (450 KB)                                            │         │  │
│  │  │                                                                            │         │  │
│  │  │  ● 15/01/2025 11:20 - João Silva                                          │         │  │
│  │  │    ▼ Alteração de Dados                                                   │         │  │
│  │  │      • Gestor Responsável: Pedro Lima → João Silva                        │         │  │
│  │  │      • Centro Custo: TI Geral → TI Infraestrutura                         │         │  │
│  │  │                                                                            │         │  │
│  │  │  ● 12/12/2024 14:50 - João Silva                                          │         │  │
│  │  │    ▼ Anexo Adicionado                                                     │         │  │
│  │  │      • contrato-vivo-assinado.pdf (1.2 MB)                                │         │  │
│  │  │                                                                            │         │  │
│  │  │  ● 12/12/2024 14:45 - João Silva                                          │         │  │
│  │  │    ▼ Status Alterado                                                      │         │  │
│  │  │      • Status: Rascunho → Vigente                                         │         │  │
│  │  │      • Contrato ativado                                                   │         │  │
│  │  │                                                                            │         │  │
│  │  │  ● 12/12/2024 14:30 - João Silva                                          │         │  │
│  │  │    ▼ Contrato Criado                                                      │         │  │
│  │  │      • CONT-2024-001 - Link Internet 1Gbps                                │         │  │
│  │  │      • Fornecedor: Vivo Empresas                                          │         │  │
│  │  │      • Valor: R$ 6.000,00/mês                                             │         │  │
│  │  │                                                                            │         │  │
│  │  └────────────────────────────────────────────────────────────────────────────┘         │  │
│  │                                                                                          │  │
│  │  ┌────────────────────────────────────────────────────────────────────────────┐         │  │
│  │  │ Filtros                                                                    │         │  │
│  │  ├────────────────────────────────────────────────────────────────────────────┤         │  │
│  │  │                                                                            │         │  │
│  │  │  Tipo de Evento: [Todos          ▼]    Período: [Todos         ▼]         │         │  │
│  │  │  Usuário:        [Todos          ▼]                                        │         │  │
│  │  │                                                                            │         │  │
│  │  │  [Aplicar Filtros] [Limpar]                                                │         │  │
│  │  │                                                                            │         │  │
│  │  └────────────────────────────────────────────────────────────────────────────┘         │  │
│  │                                                                                          │  │
│  └──────────────────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Tela 08 - Dashboard de Alertas de Vencimento

### UC Relacionado
- **UC00:** Listar Contratos - Alertas
- **Ator:** Administrador, Gestor de Contratos, Financeiro

### Layout Desktop (Área de Conteúdo - Fuse)

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│  ÁREA DE CONTEÚDO                                                                                │
├─────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                  │
│  Breadcrumb: Home > Gestão > Contratos > Alertas de Vencimento                                 │
│                                                                                                  │
│  ┌──────────────────────────────────────────────────────────────────────────────────────────┐  │
│  │ ⚠️ Alertas de Vencimento de Contratos                                                    │  │
│  ├──────────────────────────────────────────────────────────────────────────────────────────┤  │
│  │                                                                                          │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                    │  │
│  │  │ ⚠ Próximos  │  │ 🔴 Vencidos │  │ ● Renovados │  │ 💰 Impacto  │                    │  │
│  │  │ 30 dias     │  │             │  │ Este Mês    │  │ Financeiro  │                    │  │
│  │  │             │  │             │  │             │  │             │                    │  │
│  │  │      5      │  │      2      │  │      3      │  │ R$ 45.200   │                    │  │
│  │  │  contratos  │  │  contratos  │  │  contratos  │  │  a renovar  │                    │  │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘                    │  │
│  │                                                                                          │  │
│  └──────────────────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                                  │
│  ┌──────────────────────────────────────────────────────────────────────────────────────────┐  │
│  │ 🔴 Contratos Vencidos (2 contratos - Ação imediata necessária)                          │  │
│  ├──────────────────────────────────────────────────────────────────────────────────────────┤  │
│  │                                                                                          │  │
│  │  • CONT-2023-045 - Suporte SAP Brasil                                                    │  │
│  │    Vencido em: 15/11/2024 (33 dias atrás)                                                │  │
│  │    Valor: R$ 22.000/mês                                                                  │  │
│  │    Gestor: Carlos Diretor                                                                │  │
│  │    [📞 Contatar Fornecedor] [🔄 Renovar] [❌ Encerrar]                                   │  │
│  │                                                                                          │  │
│  │  • CONT-2022-089 - Licenças Adobe Creative                                               │  │
│  │    Vencido em: 01/12/2024 (17 dias atrás)                                                │  │
│  │    Valor: R$ 6.750/mês                                                                   │  │
│  │    Gestor: Maria Santos                                                                  │  │
│  │    [📞 Contatar Fornecedor] [🔄 Renovar] [❌ Encerrar]                                   │  │
│  │                                                                                          │  │
│  └──────────────────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                                  │
│  ┌──────────────────────────────────────────────────────────────────────────────────────────┐  │
│  │ ⚠ Contratos a Vencer (30 dias - 5 contratos)                                            │  │
│  ├──────────────────────────────────────────────────────────────────────────────────────────┤  │
│  │                                                                                          │  │
│  │  • CONT-2024-012 - AWS Cloud Services                                                    │  │
│  │    Vence em: 28/12/2025 (10 dias)                                                        │  │
│  │    Valor: R$ 45.000/mês | Renovação Auto: ✓ Sim                                          │  │
│  │    [Ver Detalhes] [🔄 Renovar Agora]                                                     │  │
│  │                                                                                          │  │
│  │  • CONT-2023-078 - Microsoft 365 E5                                                      │  │
│  │    Vence em: 05/01/2026 (18 dias)                                                        │  │
│  │    Valor: R$ 18.500/mês | Renovação Auto: ✗ Não                                          │  │
│  │    [Ver Detalhes] [🔄 Renovar Agora]                                                     │  │
│  │                                                                                          │  │
│  │  • CONT-2024-089 - Telefonia Móvel Claro                                                 │  │
│  │    Vence em: 12/01/2026 (25 dias)                                                        │  │
│  │    Valor: R$ 12.300/mês | Renovação Auto: ✓ Sim                                          │  │
│  │    [Ver Detalhes] [🔄 Renovar Agora]                                                     │  │
│  │                                                                                          │  │
│  │  [Ver todos os 5 contratos]                                                              │  │
│  │                                                                                          │  │
│  └──────────────────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                                  │
│  ┌──────────────────────────────────────────────────────────────────────────────────────────┐  │
│  │ ● Renovações Concluídas Este Mês (3 contratos)                                          │  │
│  ├──────────────────────────────────────────────────────────────────────────────────────────┤  │
│  │                                                                                          │  │
│  │  ✓ CONT-2023-034 - Link Internet Vivo (Renovado em 02/12/2025)                          │  │
│  │  ✓ CONT-2024-056 - Data Center Equinix (Renovado em 08/12/2025)                         │  │
│  │  ✓ CONT-2022-123 - Outsourcing Stefanini (Renovado em 15/12/2025)                       │  │
│  │                                                                                          │  │
│  └──────────────────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                                  │
│  ┌──────────────────────────────────────────────────────────────────────────────────────────┐  │
│  │ 📊 Gráfico de Vencimentos (Próximos 12 meses)                                           │  │
│  ├──────────────────────────────────────────────────────────────────────────────────────────┤  │
│  │                                                                                          │  │
│  │  Jan  Feb  Mar  Apr  May  Jun  Jul  Aug  Sep  Oct  Nov  Dec                             │  │
│  │   5    3    2    4    6    8    4    3    5    7    4    6                              │  │
│  │  ███  ██   █   ███  ████ █████ ███  ██  ████ █████ ███  ████                             │  │
│  │                                                                                          │  │
│  │  Pico de vencimentos: Junho (8 contratos)                                                │  │
│  │  Valor total a renovar em 2026: R$ 1.254.000,00                                          │  │
│  │                                                                                          │  │
│  └──────────────────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Modal - Confirmação de Exclusão

### Utilizado em: UC04 - Excluir Contrato

```
┌──────────────────────────────────────────────────────────┐
│ ⚠️ Confirmar Exclusão de Contrato                   [×]  │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Contrato: CONT-2024-001 - Link Internet 1Gbps          │
│  Fornecedor: Vivo Empresas                               │
│                                                          │
│  Tem certeza que deseja excluir este contrato?           │
│                                                          │
│  ⚠️ ATENÇÃO: Esta ação NÃO pode ser desfeita!            │
│                                                          │
│  Consequências da exclusão:                              │
│  • Histórico de alterações será mantido para auditoria   │
│  • Anexos serão arquivados                               │
│  • Aditivos vinculados serão inativados                  │
│  • Alertas de vencimento serão cancelados                │
│                                                          │
│  Para confirmar, digite o número do contrato:            │
│  [_____________________]                                 │
│                                                          │
│                            [Cancelar] [Confirmar Exclusão│
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

## Modal - Renovação Rápida de Contrato

### Utilizado em: Alertas de Vencimento

```
┌──────────────────────────────────────────────────────────┐
│ 🔄 Renovar Contrato                                 [×]  │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Contrato: CONT-2024-001 - Link Internet 1Gbps          │
│  Vencimento: 12/12/2025 (15 dias)                        │
│                                                          │
│  Nova Data de Início *                                   │
│  [13/12/2025]                                            │
│                                                          │
│  Prazo da Renovação *                                    │
│  ◉ 12 meses (padrão)                                     │
│  ○ 24 meses                                              │
│  ○ Customizado: [__] meses                               │
│                                                          │
│  Nova Data de Fim: 13/12/2026                            │
│                                                          │
│  Valor Mensal *                                          │
│  R$ [8.500,00]                                           │
│  ℹ️ Valor atual com reajuste IGPM (5,2%)                │
│                                                          │
│  ☑ Aplicar reajuste conforme índice contratual           │
│  ☑ Manter mesmas condições de SLA                        │
│  ☑ Criar aditivo automático para renovação               │
│                                                          │
│                            [Cancelar] [Renovar Contrato] │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

## Responsividade e Acessibilidade

### Notas sobre Mobile
- **Desktop Only:** Este módulo é otimizado apenas para desktop (resolução mínima: 1366x768)
- **Mobile:** Funcionalidade limitada, apenas visualização e consultas básicas

### Acessibilidade (WCAG 2.1)
- ✅ Contraste mínimo de 4.5:1 para textos
- ✅ Navegação completa por teclado (Tab, Enter, Esc)
- ✅ Labels ARIA em todos os campos
- ✅ Mensagens de erro associadas aos campos (aria-describedby)
- ✅ Landmarks semânticos (nav, main, aside)

---

## Componentes Reutilizáveis do Fuse

### Utilizados neste módulo:
- ✅ `fuse-card` - Cards de conteúdo
- ✅ `mat-table` - Tabelas de dados
- ✅ `mat-form-field` - Campos de formulário
- ✅ `mat-select` - Dropdowns
- ✅ `mat-checkbox` - Checkboxes
- ✅ `mat-radio-button` - Radio buttons
- ✅ `mat-button` - Botões
- ✅ `mat-icon` - Ícones Material
- ✅ `mat-dialog` - Modais/Diálogos
- ✅ `mat-datepicker` - Seletor de datas
- ✅ `mat-expansion-panel` - Painéis expansíveis
- ✅ `mat-timeline` - Timeline de eventos (Histórico)
- ✅ `mat-stepper` - Wizard de criação (se aplicável)

---

## Histórico de Alterações

| Versão | Data       | Autor   | Descrição                       |
|--------|------------|---------|---------------------------------|
| 1.0    | 2025-12-18 | Sistema | Criação inicial dos wireframes  |

---

**Wireframes aprovados e prontos para implementação.**
**Equipe Frontend pode iniciar desenvolvimento baseado neste documento.**
