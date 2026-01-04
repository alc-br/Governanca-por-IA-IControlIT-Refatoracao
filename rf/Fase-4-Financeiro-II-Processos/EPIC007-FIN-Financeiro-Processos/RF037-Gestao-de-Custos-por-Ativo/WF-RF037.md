# WF-RF037 - Wireframes Gestão de Custos por Ativo

**Versão:** 1.0
**Data:** 18/12/2025
**RF Relacionado:** [RF037 - Gestão de Custos por Ativo](./RF037.md)
**UC Relacionado:** [UC-RF037 - Casos de Uso](./UC-RF037.md)

---

## Nota sobre Template Fuse

Todos os wireframes utilizam **Fuse Admin Template (Angular 19)** como base:
- Layout: Modern (sidebar + top navigation)
- Componentes: Angular Material 19
- Cores: Primary (indigo-500), Accent (pink-500)
- Ícones: Material Icons + Heroicons

---

## Legenda de Símbolos

```
[Botão]               - Botão clicável
(•) Radio            - Radio button
[ ] Checkbox         - Checkbox
[Dropdown ▼]         - Select/Dropdown
[______]             - Input text
[====== ]            - Progress bar
┌──────┐
│ Card │             - Card/Container
└──────┘
≡ Menu               - Menu hamburguer
🔍 Buscar            - Busca
⚙️ Config            - Configurações
📊 Dashboard         - Dashboard
🔔 Notif             - Notificações
```

---

## Navegação do RF037

```
Menu Principal → Gestão → Custos por Ativo
```

**Breadcrumb:** Home > Gestão > Custos por Ativo > [Tela Atual]

---

## Tela 01 - Listagem de Custos por Ativo (Desktop)

**Rota:** `/gestao/custos-ativo`
**Permissão:** `CUSTOS_ATIVO.LISTAR`
**UC:** UC00

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ ≡ IControlIT                    🔍 Buscar  📊  🔔  👤 João Silva            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│ Home > Gestão > Custos por Ativo                                             │
│                                                                              │
│ ┌────────────────────────────────────────────────────────────────────────┐ │
│ │                                                                          │ │
│ │  Gestão de Custos por Ativo           [TCO Dashboard] [+ Novo Custo]   │ │
│ │                                                                          │ │
│ │  ┌─────────────────────────────────────────────────────────────────┐   │ │
│ │  │ 🔍 Buscar ativo ou custo...                              🎲 📊 │   │ │
│ │  └─────────────────────────────────────────────────────────────────┘   │ │
│ │                                                                          │ │
│ │  ┌──────────────┬──────────────┬──────────────┬──────────────────┐    │ │
│ │  │ Ativo      ▼ │ Tipo Custo▼  │   Período▼   │ Fornecedor▼      │    │ │
│ │  ├──────────────┼──────────────┼──────────────┼──────────────────┤    │ │
│ │  │ [Todos    ▼] │[Todos     ▼] │[Últimos 12m▼]│[Todos         ▼] │    │ │
│ │  └──────────────┴──────────────┴──────────────┴──────────────────┘    │ │
│ │                                                                          │ │
│ │  ┌────────────────────────────────────────────────────────────────┐    │ │
│ │  │ 📊 Cards Resumo - 2025                                         │    │ │
│ │  ├────────────┬────────────┬────────────┬────────────┐           │    │ │
│ │  │ Total      │ Aquisição  │ Manutenção │ TCO Médio  │           │    │ │
│ │  │ Custos     │            │            │ por Ativo  │           │    │ │
│ │  ├────────────┼────────────┼────────────┼────────────┤           │    │ │
│ │  │   1.250    │ R$ 1.8M    │ R$ 450k    │ R$ 8.500   │           │    │ │
│ │  └────────────┴────────────┴────────────┴────────────┘           │    │ │
│ │  └────────────────────────────────────────────────────────────────┘    │ │
│ │                                                                          │ │
│ │  Exibindo 1.250 custos de ativos                                        │ │
│ │                                                                          │ │
│ │  ┌───────────────────────────────────────────────────────────────────┐ │ │
│ │  │ Ativo         │Tipo Custo│Valor      │Data      │Fornecedor │Ações│ │ │
│ │  ├───────────────┼──────────┼───────────┼──────────┼───────────┼─────┤ │ │
│ │  │ SRV-WEB-01    │ Aquisição│ R$ 45.000 │15/01/2025│ Dell Inc  │ [⋮] │ │ │
│ │  │ (Servidor)    │          │           │          │           │     │ │ │
│ │  ├───────────────┼──────────┼───────────┼──────────┼───────────┼─────┤ │ │
│ │  │ SRV-WEB-01    │Manutenção│ R$ 3.200  │10/02/2025│ Dell Inc  │ [⋮] │ │ │
│ │  │               │          │           │          │           │     │ │ │
│ │  ├───────────────┼──────────┼───────────┼──────────┼───────────┼─────┤ │ │
│ │  │ NB-DEV-045    │ Aquisição│ R$ 8.500  │20/01/2025│ Lenovo    │ [⋮] │ │ │
│ │  │ (Notebook)    │          │           │          │           │     │ │ │
│ │  ├───────────────┼──────────┼───────────┼──────────┼───────────┼─────┤ │ │
│ │  │ NB-DEV-045    │ Licença  │ R$ 1.200  │25/01/2025│ Microsoft │ [⋮] │ │ │
│ │  │               │  Win Pro │           │          │           │     │ │ │
│ │  ├───────────────┼──────────┼───────────┼──────────┼───────────┼─────┤ │ │
│ │  │ SW-CORE-01    │Depreciação│R$ 2.400  │01/03/2025│ (Auto)    │ [⋮] │ │ │
│ │  │ (Switch)      │ Mensal   │           │          │           │     │ │ │
│ │  └───────────────┴──────────┴───────────┴──────────┴───────────┴─────┘ │ │
│ │                                                                          │ │
│ │  [◀ Anterior]  Página 1 de 125  [Próxima ▶]                            │ │
│ │                                                                          │ │
│ └────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘

Menu ações [⋮]:
- Visualizar Detalhes
- Editar Custo
- Ver TCO do Ativo
- Anexar Documento
- Excluir (soft delete)
```

---

## Tela 02 - Criar/Editar Custo de Ativo (Desktop)

**Rota:** `/gestao/custos-ativo/novo` ou `/gestao/custos-ativo/:id/editar`
**Permissão:** `CUSTOS_ATIVO.CRIAR` ou `CUSTOS_ATIVO.EDITAR`
**UC:** UC01 (Criar) / UC03 (Editar)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ ≡ IControlIT                    🔍 Buscar  📊  🔔  👤 João Silva            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│ Home > Gestão > Custos por Ativo > Novo Custo de Ativo                      │
│                                                                              │
│ ┌────────────────────────────────────────────────────────────────────────┐ │
│ │                                                                          │ │
│ │  Cadastrar Novo Custo de Ativo                      [Salvar] [Cancelar] │ │
│ │                                                                          │ │
│ │  ┌──────────────────────────────────────────────────────────────────┐  │ │
│ │  │ [Dados Principais] [Anexos]                                      │  │ │
│ │  └──────────────────────────────────────────────────────────────────┘  │ │
│ │                                                                          │ │
│ │  ┌──────────────────────────────────────────────────────────────────┐  │ │
│ │  │ 📋 Seleção do Ativo                                              │  │ │
│ │  │                                                                   │  │ │
│ │  │  Ativo *                                                         │  │ │
│ │  │  ┌──────────────────────────────────────────────────────────┐   │  │ │
│ │  │  │ 🔍 [Buscar ativo... (código, descrição, tag)          ▼] │   │  │ │
│ │  │  └──────────────────────────────────────────────────────────┘   │  │ │
│ │  │  (Autocomplete com ativos cadastrados)                          │  │ │
│ │  │                                                                   │  │ │
│ │  │  ✅ Selecionado: SRV-WEB-01 - Dell PowerEdge R740               │  │ │
│ │  │  • Categoria: Servidor                                          │  │ │
│ │  │  • Localização: Data Center SP                                  │  │ │
│ │  │  • Data Aquisição: 15/01/2025                                   │  │ │
│ │  │                                                                   │  │ │
│ │  └──────────────────────────────────────────────────────────────────┘  │ │
│ │                                                                          │ │
│ │  ┌──────────────────────────────────────────────────────────────────┐  │ │
│ │  │ 💰 Informações do Custo                                          │  │ │
│ │  │                                                                   │  │ │
│ │  │  Tipo de Custo *                                                 │  │ │
│ │  │  ┌────────────────────────────────────────────────────────────┐ │  │ │
│ │  │  │ (•) Aquisição    ( ) Manutenção   ( ) Licença             │ │  │ │
│ │  │  │ ( ) Depreciação  ( ) Upgrade      ( ) Outro                │ │  │ │
│ │  │  └────────────────────────────────────────────────────────────┘ │  │ │
│ │  │                                                                   │  │ │
│ │  │  ⚠️ Aquisição pode ser registrada apenas 1x por ativo (RN-037-002)│ │
│ │  │                                                                   │  │ │
│ │  │  Valor *                  Data do Custo *                        │  │ │
│ │  │  ┌────────────────────┐  ┌────────────────────┐                 │  │ │
│ │  │  │ R$ [45000.00      ]│  │ [15/01/2025      📅]│                 │  │ │
│ │  │  └────────────────────┘  └────────────────────┘                 │  │ │
│ │  │                                                                   │  │ │
│ │  │  Fornecedor                                                      │  │ │
│ │  │  ┌──────────────────────────────────────────────────────────┐   │  │ │
│ │  │  │ [Selecione fornecedor (RF024)                         ▼] │   │  │ │
│ │  │  └──────────────────────────────────────────────────────────┘   │  │ │
│ │  │  (Opcional para alguns tipos de custo)                          │  │ │
│ │  │                                                                   │  │ │
│ │  │  Descrição                                                       │  │ │
│ │  │  ┌──────────────────────────────────────────────────────────┐   │  │ │
│ │  │  │ [Aquisição servidor Dell PowerEdge R740 para ambiente    ]│   │  │ │
│ │  │  │  produção. Inclui garantia 3 anos on-site.               │   │  │ │
│ │  │  │                                                           │   │  │ │
│ │  │  └──────────────────────────────────────────────────────────┘   │  │ │
│ │  │                                                                   │  │ │
│ │  └──────────────────────────────────────────────────────────────────┘  │ │
│ │                                                                          │ │
│ │  ┌──────────────────────────────────────────────────────────────────┐  │ │
│ │  │ 📎 Anexos (Opcional)                                             │  │ │
│ │  │                                                                   │  │ │
│ │  │  [Upload de Arquivos]                                            │  │ │
│ │  │  (Nota fiscal, orçamento, contrato, recibos)                    │  │ │
│ │  │                                                                   │  │ │
│ │  │  Formatos aceitos: PDF, JPG, PNG, Excel                          │  │ │
│ │  │  Tamanho máximo: 10 MB por arquivo                               │  │ │
│ │  │                                                                   │  │ │
│ │  └──────────────────────────────────────────────────────────────────┘  │ │
│ │                                                                          │ │
│ │  ⚙️ Impacto no TCO: +R$ 45.000 (atualizado automaticamente)             │ │
│ │                                                                          │ │
│ │  [Cancelar]  [Salvar e Ver TCO]                                         │ │
│ │                                                                          │ │
│ └────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Tela 03 - Dashboard TCO (Custo Total de Propriedade) (Desktop)

**Rota:** `/gestao/custos-ativo/:ativo_id/tco`
**Permissão:** `CUSTOS_ATIVO.CALCULAR_TCO`
**UC:** UC05

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ ≡ IControlIT                    🔍 Buscar  📊  🔔  👤 João Silva            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│ Home > Gestão > Custos por Ativo > SRV-WEB-01 > TCO                         │
│                                                                              │
│ ┌────────────────────────────────────────────────────────────────────────┐ │
│ │                                                                          │ │
│ │  TCO - Custo Total de Propriedade                   [Exportar] [Voltar]│ │
│ │  SRV-WEB-01 - Dell PowerEdge R740                                       │ │
│ │                                                                          │ │
│ │  ┌────────────────────────────────────────────────────────────────┐    │ │
│ │  │ 📊 TCO Consolidado                                             │    │ │
│ │  │                                                                 │    │ │
│ │  │ ┌──────────────┬──────────────┬──────────────┬──────────────┐│    │ │
│ │  │ │ TCO Total    │ TCO/Mês      │ TCO/Usuário  │ vs Média Cat ││    │ │
│ │  │ ├──────────────┼──────────────┼──────────────┼──────────────┤│    │ │
│ │  │ │ R$ 58.400    │ R$ 4.867     │ R$ 97        │ +12% 🔴      ││    │ │
│ │  │ │ (12 meses)   │              │ (60 users)   │ (acima média)││    │ │
│ │  │ └──────────────┴──────────────┴──────────────┴──────────────┘│    │ │
│ │  │                                                                 │    │ │
│ │  └────────────────────────────────────────────────────────────────┘    │ │
│ │                                                                          │ │
│ │  ┌────────────────────────────────────────────────────────────────┐    │ │
│ │  │ 📊 Breakdown por Categoria (Gráfico Pizza)                     │    │ │
│ │  │                                                                 │    │ │
│ │  │         ╱───╲                                                   │    │ │
│ │  │        ╱ 77% ╲                                                  │    │ │
│ │  │       │Aquis. │                                                 │    │ │
│ │  │        ╲     ╱ 8%                                               │    │ │
│ │  │         ╲───╱ Manutenção                                        │    │ │
│ │  │          7% Licença                                             │    │ │
│ │  │          5% Depreciação                                         │    │ │
│ │  │          3% Operacional                                         │    │ │
│ │  │                                                                 │    │ │
│ │  │  • Aquisição:     R$ 45.000 (77%)                              │    │ │
│ │  │  • Manutenção:    R$ 4.800 (8%)                                │    │ │
│ │  │  • Licenças:      R$ 4.200 (7%)                                │    │ │
│ │  │  • Depreciação:   R$ 3.000 (5%)                                │    │ │
│ │  │  • Operacional:   R$ 1.400 (3%) - rateio energia/suporte      │    │ │
│ │  │                                                                 │    │ │
│ │  └────────────────────────────────────────────────────────────────┘    │ │
│ │                                                                          │ │
│ │  ┌────────────────────────────────────────────────────────────────┐    │ │
│ │  │ 📈 Histórico de Custos (Timeline)                              │    │ │
│ │  │                                                                 │    │ │
│ │  │ R$                                                              │    │ │
│ │  │ 60k ●───────────────────────────────────────────────────────●  │    │ │
│ │  │ 50k   ↑                                                      │  │    │ │
│ │  │ 40k   │ Aquisição                                            │  │    │ │
│ │  │ 30k   │ R$ 45k                                               │  │    │ │
│ │  │ 20k   │      ●       ●         ●        ●                    │  │    │ │
│ │  │ 10k   │    Manut   Licença   Manut   Deprec                 │  │    │ │
│ │  │  0  ──┼──────┼───────┼────────┼────────┼────────────────────┼─ │    │ │
│ │  │     Jan/25 Fev/25  Mar/25  Abr/25  Mai/25 ... Dez/25         │    │ │
│ │  │                                                                 │    │ │
│ │  └────────────────────────────────────────────────────────────────┘    │ │
│ │                                                                          │ │
│ │  ┌────────────────────────────────────────────────────────────────┐    │ │
│ │  │ 📋 Detalhamento de Custos                                      │    │ │
│ │  │                                                                 │    │ │
│ │  │ Data       │ Tipo        │ Valor      │ Fornecedor  │ Status  │    │ │
│ │  ├────────────┼─────────────┼────────────┼─────────────┼─────────┤    │ │
│ │  │ 15/01/2025 │ Aquisição   │ R$ 45.000  │ Dell Inc    │ ✅      │    │ │
│ │  │ 20/02/2025 │ Manutenção  │ R$ 3.200   │ Dell Inc    │ ✅      │    │ │
│ │  │ 05/03/2025 │ Licença SO  │ R$ 1.200   │ Microsoft   │ ✅      │    │ │
│ │  │ 10/04/2025 │ Manutenção  │ R$ 1.600   │ Dell Inc    │ ✅      │    │ │
│ │  │ 01/05/2025 │ Depreciação │ R$ 750/mês │ (Auto)      │ ✅      │    │ │
│ │  └────────────┴─────────────┴────────────┴─────────────┴─────────┘    │ │
│ │                                                                          │ │
│ │  [Adicionar Novo Custo] [Comparar com Outros Ativos] [Exportar PDF]    │ │
│ │                                                                          │ │
│ └────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Tela 04 - Comparar TCO entre Ativos (Desktop)

**Rota:** `/gestao/custos-ativo/comparar`
**Permissão:** `CUSTOS_ATIVO.COMPARAR`
**UC:** UC06

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ ≡ IControlIT                    🔍 Buscar  📊  🔔  👤 João Silva            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│ Home > Gestão > Custos por Ativo > Comparar TCO                             │
│                                                                              │
│ ┌────────────────────────────────────────────────────────────────────────┐ │
│ │                                                                          │ │
│ │  Comparação de TCO entre Ativos                         [Exportar Excel]│ │
│ │                                                                          │ │
│ │  ┌──────────────────────────────────────────────────────────────────┐  │ │
│ │  │ Selecione Ativos para Comparar (mesma categoria)                │  │ │
│ │  │                                                                   │  │ │
│ │  │  Categoria: [Servidor                                         ▼] │  │ │
│ │  │                                                                   │  │ │
│ │  │  Ativos Selecionados (max 5):                                    │  │ │
│ │  │  [✓] SRV-WEB-01 - Dell PowerEdge R740                           │  │ │
│ │  │  [✓] SRV-WEB-02 - HP ProLiant DL380                             │  │ │
│ │  │  [✓] SRV-DB-01 - Dell PowerEdge R840                            │  │ │
│ │  │  [ ] SRV-APP-01 - Lenovo ThinkSystem SR650                      │  │ │
│ │  │                                                                   │  │ │
│ │  │  [Gerar Comparação]                                              │  │ │
│ │  │                                                                   │  │ │
│ │  └──────────────────────────────────────────────────────────────────┘  │ │
│ │                                                                          │ │
│ │  ┌──────────────────────────────────────────────────────────────────┐  │ │
│ │  │ 📊 Comparação TCO - Servidores                                   │  │ │
│ │  │                                                                   │  │ │
│ │  │ Ativo       │TCO Total│TCO/Mês │Aquisição│Manut│Lic│Depr│Status │  │ │
│ │  ├─────────────┼─────────┼────────┼─────────┼─────┼───┼────┼───────┤  │ │
│ │  │ SRV-WEB-01  │R$ 58.4k │R$ 4.9k │R$ 45k   │R$ 5k│R$ 4k│R$ 3k│🔴+12%││ │
│ │  │ (Dell R740) │         │        │         │     │   │    │ acima │  │ │
│ │  ├─────────────┼─────────┼────────┼─────────┼─────┼───┼────┼───────┤  │ │
│ │  │ SRV-WEB-02  │R$ 52.1k │R$ 4.3k │R$ 38k   │R$ 6k│R$ 4k│R$ 2k│🟢-5% ││ │
│ │  │ (HP DL380)  │         │        │         │     │   │    │ abaixo│  │ │
│ │  ├─────────────┼─────────┼────────┼─────────┼─────┼───┼────┼───────┤  │ │
│ │  │ SRV-DB-01   │R$ 95.2k │R$ 7.9k │R$ 78k   │R$ 8k│R$ 5k│R$ 4k│🔴+82%││ │
│ │  │ (Dell R840) │         │        │         │     │   │    │ acima │  │ │
│ │  ├─────────────┼─────────┼────────┼─────────┼─────┼───┼────┼───────┤  │ │
│ │  │ MÉDIA       │R$ 68.6k │R$ 5.7k │R$ 53.7k │R$ 6k│R$ 4k│R$ 3k│  -   ││ │
│ │  │ (Categoria) │         │        │         │     │   │    │       │  │ │
│ │  └─────────────┴─────────┴────────┴─────────┴─────┴───┴────┴───────┘  │ │
│ │                                                                          │ │
│ │  ┌──────────────────────────────────────────────────────────────────┐  │ │
│ │  │ 📈 Comparação Gráfica (Barras Empilhadas)                        │  │ │
│ │  │                                                                   │  │ │
│ │  │ TCO (R$)                                                          │  │ │
│ │  │ 100k ┌──────┐                                                     │  │ │
│ │  │  90k │ Depr │                                                     │  │ │
│ │  │  80k │ Lic  │         ┌──────┐                                   │  │ │
│ │  │  70k │ Manut│         │ Depr │                                   │  │ │
│ │  │  60k │Aquis │┌──────┐ │ Lic  │                                   │  │ │
│ │  │  50k └──────┘│ Depr │ │ Manut│                                   │  │ │
│ │  │  40k         │ Lic  │ │Aquis │                                   │  │ │
│ │  │  30k         │ Manut│ └──────┘                                   │  │ │
│ │  │  20k         │Aquis │                                            │  │ │
│ │  │  10k         └──────┘                                            │  │ │
│ │  │   0  ────────────────────────────                                │  │ │
│ │  │        SRV-WEB-01  SRV-WEB-02  SRV-DB-01                          │  │ │
│ │  │                                                                   │  │ │
│ │  └──────────────────────────────────────────────────────────────────┘  │ │
│ │                                                                          │ │
│ │  ⚠️ Alertas de Custo Excessivo:                                          │ │
│ │  • SRV-WEB-01: +12% acima da média (threshold 20%)                     │ │
│ │  • SRV-DB-01: +82% acima da média ❗ Revisar (RN-037-008)               │ │
│ │                                                                          │ │
│ │  [Exportar Comparação] [Gerar Relatório Detalhado]                     │ │
│ │                                                                          │ │
│ └────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Tela 05 - Histórico de Custos do Ativo (Desktop)

**Rota:** `/gestao/custos-ativo/:ativo_id/historico`
**Permissão:** `CUSTOS_ATIVO.VISUALIZAR_HISTORICO`
**UC:** UC08

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ ≡ IControlIT                    🔍 Buscar  📊  🔔  👤 João Silva            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│ Home > Gestão > Custos por Ativo > SRV-WEB-01 > Histórico                   │
│                                                                              │
│ ┌────────────────────────────────────────────────────────────────────────┐ │
│ │                                                                          │ │
│ │  Histórico de Custos - SRV-WEB-01                       [Exportar] [⋮]  │ │
│ │  Dell PowerEdge R740 - Servidor Web Produção                            │ │
│ │                                                                          │ │
│ │  ┌────────────────────────────────────────────────────────────────┐    │ │
│ │  │ 📊 Resumo do Ativo                                             │    │ │
│ │  │                                                                 │    │ │
│ │  │ Data Aquisição:  15/01/2025                                    │    │ │
│ │  │ Idade:           10 meses                                      │    │ │
│ │  │ Total Custos:    R$ 58.400 (12 lançamentos)                    │    │ │
│ │  │ TCO Acumulado:   R$ 58.400                                     │    │ │
│ │  │ Depreciação:     R$ 3.000 (20% vida útil)                      │    │ │
│ │  │                                                                 │    │ │
│ │  └────────────────────────────────────────────────────────────────┘    │ │
│ │                                                                          │ │
│ │  ┌────────────────────────────────────────────────────────────────┐    │ │
│ │  │ 📅 Timeline Completa de Custos                                 │    │ │
│ │  │                                                                 │    │ │
│ │  │  ●──────●────────●────────●────────●────────●────────●──────── │    │ │
│ │  │  │      │        │        │        │        │        │         │    │ │
│ │  │  Jan    Fev      Mar      Abr      Mai      Jun      ...       Dez  │    │ │
│ │  │  2025   2025     2025     2025     2025     2025              2025  │    │ │
│ │  │                                                                 │    │ │
│ │  │  ┌──────────────────────────────────────────────────────────┐ │    │ │
│ │  │  │ 15/01/2025 - Aquisição                   R$ 45.000 ✅     │ │    │ │
│ │  │  │ ├─ Dell PowerEdge R740                                    │ │    │ │
│ │  │  │ ├─ Fornecedor: Dell Inc                                   │ │    │ │
│ │  │  │ └─ NF: 123456 [📄 Ver Anexo]                              │ │    │ │
│ │  │  └──────────────────────────────────────────────────────────┘ │    │ │
│ │  │                                                                 │    │ │
│ │  │  ┌──────────────────────────────────────────────────────────┐ │    │ │
│ │  │  │ 20/02/2025 - Manutenção                  R$ 3.200 ✅      │ │    │ │
│ │  │  │ ├─ Troca HD defeituoso + atualização firmware             │ │    │ │
│ │  │  │ ├─ Fornecedor: Dell Inc                                   │ │    │ │
│ │  │  │ └─ OS: 78901 [📄 Ver Anexo]                               │ │    │ │
│ │  │  └──────────────────────────────────────────────────────────┘ │    │ │
│ │  │                                                                 │    │ │
│ │  │  ┌──────────────────────────────────────────────────────────┐ │    │ │
│ │  │  │ 05/03/2025 - Licença                     R$ 1.200 ✅      │ │    │ │
│ │  │  │ ├─ Windows Server 2022 Standard                           │ │    │ │
│ │  │  │ ├─ Fornecedor: Microsoft                                  │ │    │ │
│ │  │  │ └─ Licença: WS2022-STD-001                                │ │    │ │
│ │  │  └──────────────────────────────────────────────────────────┘ │    │ │
│ │  │                                                                 │    │ │
│ │  │  ┌──────────────────────────────────────────────────────────┐ │    │ │
│ │  │  │ 10/04/2025 - Manutenção                  R$ 1.600 ✅      │ │    │ │
│ │  │  │ ├─ Upgrade memória RAM 128GB → 256GB                      │ │    │ │
│ │  │  │ ├─ Fornecedor: Dell Inc                                   │ │    │ │
│ │  │  │ └─ OS: 89012                                              │ │    │ │
│ │  │  └──────────────────────────────────────────────────────────┘ │    │ │
│ │  │                                                                 │    │ │
│ │  │  ┌──────────────────────────────────────────────────────────┐ │    │ │
│ │  │  │ 01/05/2025 - Depreciação (Auto)          R$ 750/mês ✅    │ │    │ │
│ │  │  │ ├─ Depreciação mensal automática (vida útil 5 anos)       │ │    │ │
│ │  │  │ ├─ Base cálculo: R$ 45.000 / 60 meses                     │ │    │ │
│ │  │  │ └─ Acumulado: R$ 3.000 (4 meses)                          │ │    │ │
│ │  │  └──────────────────────────────────────────────────────────┘ │    │ │
│ │  │                                                                 │    │ │
│ │  │  ┌──────────────────────────────────────────────────────────┐ │    │ │
│ │  │  │ 15/06/2025 - Upgrade                     R$ 2.800 ❌      │ │    │ │
│ │  │  │ ├─ [CANCELADO] Upgrade SSD cancelado por orçamento        │ │    │ │
│ │  │  │ ├─ Excluído em: 18/06/2025                                │ │    │ │
│ │  │  │ └─ Justificativa: "Substituído por modelo superior"       │ │    │ │
│ │  │  └──────────────────────────────────────────────────────────┘ │    │ │
│ │  │                                                                 │    │ │
│ │  └────────────────────────────────────────────────────────────────┘    │ │
│ │                                                                          │ │
│ │  ℹ️ Custos cancelados incluídos no histórico (RN-037-009)               │ │
│ │                                                                          │ │
│ │  [Adicionar Novo Custo] [Filtrar Timeline] [Exportar PDF]              │ │
│ │                                                                          │ │
│ └────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Modais

### Modal 01 - Confirmação Excluir Custo

**Trigger:** Usuário clica "Excluir" (UC04)

```
┌─────────────────────────────────────────┐
│ ⚠️  Confirmar Exclusão                  │
├─────────────────────────────────────────┤
│                                         │
│ Deseja excluir este custo?              │
│                                         │
│ • Soft delete: Mantido no histórico     │
│ • TCO será recalculado automaticamente  │
│ • Marcado como "Cancelado"              │
│ • Requer justificativa obrigatória      │
│                                         │
│ Custo: Manutenção - R$ 3.200            │
│ Ativo: SRV-WEB-01                       │
│                                         │
│ Justificativa *                         │
│ ┌─────────────────────────────────────┐ │
│ │ [Lançamento duplicado...           ]│ │
│ └─────────────────────────────────────┘ │
│                                         │
│ ⚠️ Aquisição NÃO pode ser excluída      │
│    (RN-037-005)                         │
│                                         │
│     [Cancelar]  [Confirmar Exclusão]   │
│                                         │
└─────────────────────────────────────────┘
```

### Modal 02 - Sucesso Criar Custo

**Trigger:** Após criar custo com sucesso (UC01)

```
┌─────────────────────────────────────────┐
│ ✅ Custo Registrado com Sucesso         │
├─────────────────────────────────────────┤
│                                         │
│ Custo adicionado ao ativo SRV-WEB-01!   │
│                                         │
│ • Tipo: Aquisição                       │
│ • Valor: R$ 45.000                      │
│ • TCO atualizado: R$ 45.000             │
│ • Depreciação iniciada (R$ 750/mês)     │
│                                         │
│ Próximos passos:                        │
│ - Anexar nota fiscal (recomendado)      │
│ - Depreciação calculada automaticamente │
│ - Disponível no TCO Dashboard           │
│                                         │
│     [Ver TCO do Ativo]  [Fechar]       │
│                                         │
└─────────────────────────────────────────┘
```

### Modal 03 - Alerta Custo Excessivo

**Trigger:** Sistema detecta custo > 120% média (UC07)

```
┌─────────────────────────────────────────┐
│ ⚠️ Alerta de Custo Excessivo            │
├─────────────────────────────────────────┤
│                                         │
│ O TCO deste ativo está acima da média!  │
│                                         │
│ Ativo: SRV-DB-01                        │
│ TCO Atual: R$ 95.200                    │
│ Média Categoria: R$ 52.300              │
│ Diferença: +82% 🔴                      │
│                                         │
│ Possíveis causas:                       │
│ • Manutenções frequentes                │
│ • Hardware de alto custo                │
│ • Licenças especializadas               │
│                                         │
│ Ações recomendadas:                     │
│ - Revisar histórico de custos           │
│ - Comparar com ativos similares         │
│ - Avaliar substituição do ativo         │
│                                         │
│ Ticket automático criado: #45678        │
│                                         │
│     [Ver Histórico]  [Fechar]          │
│                                         │
└─────────────────────────────────────────┘
```

### Modal 04 - Aprovar Alteração Aquisição

**Trigger:** Editar custo tipo Aquisição (UC03 + RN-037-004)

```
┌─────────────────────────────────────────┐
│ 🔐 Aprovação Necessária                 │
├─────────────────────────────────────────┤
│                                         │
│ Alteração de custo de Aquisição requer  │
│ aprovação do gestor.                    │
│                                         │
│ Ativo: SRV-WEB-01                       │
│ Valor Atual: R$ 45.000                  │
│ Novo Valor: R$ 47.500                   │
│ Diferença: +R$ 2.500                    │
│                                         │
│ Motivo da Alteração *                   │
│ ┌─────────────────────────────────────┐ │
│ │ [Ajuste valor nota fiscal correta  ]│ │
│ └─────────────────────────────────────┘ │
│                                         │
│ Solicitação será enviada para:          │
│ • Carlos Souza (Gerente TI)             │
│                                         │
│ ⏱️ Aguardando aprovação...               │
│                                         │
│     [Cancelar]  [Solicitar Aprovação]  │
│                                         │
└─────────────────────────────────────────┘
```

---

## Estados da Interface

### Estado 01 - Sem Custos no Ativo

**Quando:** Ativo sem custos registrados

```
┌────────────────────────────────────────────────────┐
│                                                    │
│                   💰                               │
│                                                    │
│          Nenhum custo registrado neste ativo       │
│                                                    │
│   Registre custos para calcular TCO e controlar    │
│   o custo total de propriedade do ativo.           │
│                                                    │
│   Tipos de custo:                                  │
│   • Aquisição (obrigatório, registra apenas 1x)   │
│   • Manutenção, Licença, Upgrade, Depreciação     │
│                                                    │
│            [+ Registrar Primeiro Custo]            │
│                                                    │
└────────────────────────────────────────────────────┘
```

### Estado 02 - Calculando TCO

**Quando:** Sistema está processando TCO

```
┌────────────────────────────────────────────────────┐
│                                                    │
│                   ⏳                               │
│                                                    │
│       Calculando TCO do ativo...                   │
│                                                    │
│   [==================================      ] 75%   │
│                                                    │
│   Somando custos diretos                           │
│   Calculando depreciação                           │
│   Aplicando rateio custos indiretos                │
│   Gerando comparação com categoria                 │
│                                                    │
│   Processando 12 lançamentos...                    │
│                                                    │
└────────────────────────────────────────────────────┘
```

### Estado 03 - Erro Aquisição Duplicada

**Quando:** Tentar registrar 2ª aquisição (RN-037-002)

```
┌────────────────────────────────────────────────────┐
│                                                    │
│                   ❌                               │
│                                                    │
│         Custo de Aquisição Duplicado               │
│                                                    │
│   Este ativo já possui custo de Aquisição          │
│   registrado.                                      │
│                                                    │
│   Aquisição atual:                                 │
│   • Data: 15/01/2025                               │
│   • Valor: R$ 45.000                               │
│   • Fornecedor: Dell Inc                           │
│                                                    │
│   Apenas 1 custo de Aquisição permitido            │
│   por ativo (RN-037-002).                          │
│                                                    │
│   Se necessário corrigir, edite o custo            │
│   existente.                                       │
│                                                    │
│              [Editar Existente] [Fechar]           │
│                                                    │
└────────────────────────────────────────────────────┘
```

---

## Toast Notifications

### Notificação 01 - TCO Calculado

```
┌─────────────────────────────────────┐
│ ✅ TCO calculado com sucesso        │
│ Total: R$ 58.400 | +12% vs média    │
└─────────────────────────────────────┘
(Auto-dismiss: 4s)
```

### Notificação 02 - Depreciação Iniciada

```
┌─────────────────────────────────────┐
│ ✅ Depreciação automática iniciada  │
│ R$ 750/mês (vida útil 5 anos)       │
└─────────────────────────────────────┘
(Auto-dismiss: 3s)
```

### Notificação 03 - Custo Excluído

```
┌─────────────────────────────────────┐
│ ✅ Custo excluído (soft delete)     │
│ Marcado como cancelado no histórico │
└─────────────────────────────────────┘
(Auto-dismiss: 3s)
```

---

## Notas Técnicas de Implementação

### Componentes Fuse Utilizados

- **FuseCardComponent** - Cards de conteúdo
- **FuseAlertComponent** - Alertas e mensagens

### Componentes Angular Material

- **MatTableModule** - Tabela de listagem
- **MatPaginatorModule** - Paginação
- **MatSortModule** - Ordenação
- **MatFormFieldModule** - Campos de formulário
- **MatInputModule** - Inputs
- **MatSelectModule** - Selects/Dropdowns
- **MatAutocompleteModule** - Autocomplete de ativos
- **MatButtonModule** - Botões
- **MatIconModule** - Ícones
- **MatDialogModule** - Modais
- **MatCheckboxModule** - Checkboxes
- **MatDatepickerModule** - Seletor de datas
- **MatChipsModule** - Tags de status
- **MatProgressBarModule** - Barra de progresso
- **MatTooltipModule** - Tooltips
- **MatSnackBarModule** - Toast notifications
- **MatDividerModule** - Divisores
- **MatTabsModule** - Abas de navegação
- **MatExpansionModule** - Accordion timeline

### Bibliotecas Especializadas

- **ApexCharts** - Gráficos (pizza, barras empilhadas, linha)
- **date-fns** - Manipulação de datas e idade do ativo

### Validações

- **Reactive Forms** com validadores customizados
- **FluentValidation** no backend
- **RN-037-002:** Aquisição apenas 1x por ativo
- **RN-037-004:** Alteração Aquisição requer aprovação
- **RN-037-005:** Aquisição não pode ser excluída
- **RN-037-008:** Threshold custo excessivo (120%)

### Jobs Background

- **Hangfire** - Cálculo automático de depreciação mensal
- **Hangfire** - Job diário análise custos excessivos

### Responsividade

- Desktop: Layout completo (min-width: 1024px)
- Timeline adaptativa com scroll horizontal

### Acessibilidade (a11y)

- Labels ARIA em todos os controles
- Navegação via teclado
- Contraste WCAG AA
- Screen reader friendly

---

## Histórico de Alterações

| Versão | Data       | Autor            | Descrição                              |
|--------|------------|------------------|----------------------------------------|
| 1.0    | 18/12/2025 | Architect Agent  | Versão inicial concisa - 5 telas + 4 modais |

---

**Próximos Passos:**
1. Developer implementa telas usando wireframes como referência
2. Tester valida fluxos e regras de negócio (RN-037-*)
3. UX/UI aplica identidade visual final
