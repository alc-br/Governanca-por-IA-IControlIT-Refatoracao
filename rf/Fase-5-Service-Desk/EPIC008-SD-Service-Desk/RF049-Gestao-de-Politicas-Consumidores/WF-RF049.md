# WF-RF049 - Wireframes Gestão de Políticas Consumidores

**Versão:** 1.0
**Data:** 18/12/2025
**RF Relacionado:** [RF049 - Gestão de Políticas Consumidores](./RF049.md)
**UC Relacionado:** [UC-RF049 - Casos de Uso](./UC-RF049.md)

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
┌──────┐
│ Card │             - Card/Container
└──────┘
≡ Menu               - Menu hamburguer
🔍 Buscar            - Busca
```

---

## Navegação do RF049

```
Menu Principal → Gestão → Políticas de Consumidores
```

**Breadcrumb:** Home > Gestão > Políticas de Consumidores > [Tela Atual]

---

## Tela 01 - Listagem de Políticas (Desktop)

**Rota:** `/gestao/politicas-consumidores`
**Permissão:** `POLITICAS_CONSUMIDORES.LISTAR`
**UC:** UC00

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ ≡ IControlIT                    🔍 Buscar  📊  🔔  👤 João Silva            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│ Home > Gestão > Políticas de Consumidores                                   │
│                                                                              │
│ ┌────────────────────────────────────────────────────────────────────────┐ │
│ │                                                                          │ │
│ │  Gestão de Políticas de Consumidores   [📊 Relatório] [+ Nova Política]│ │
│ │                                                                          │ │
│ │  ┌─────────────────────────────────────────────────────────────────┐   │ │
│ │  │ 🔍 Buscar política, descrição...                  🎲 📊 ⚙️      │   │ │
│ │  └─────────────────────────────────────────────────────────────────┘   │ │
│ │                                                                          │ │
│ │  ┌──────────────┬──────────────┬──────────────┐                        │ │
│ │  │  Categoria▼  │   Status▼    │   Empresa▼   │                        │ │
│ │  ├──────────────┼──────────────┼──────────────┤                        │ │
│ │  │[Todas      ▼]│[Ativa      ▼]│[Todas      ▼]│                        │ │
│ │  └──────────────┴──────────────┴──────────────┘                        │ │
│ │                                                                          │ │
│ │  ┌────────────────────────────────────────────────────────────────┐    │ │
│ │  │ 📊 Resumo de Políticas                                         │    │ │
│ │  ├────────────┬────────────┬────────────┬────────────┐           │    │ │
│ │  │Total Políti│  Ativas    │  Inativos  │Consumidores│           │    │ │
│ │  ├────────────┼────────────┼────────────┼────────────┤           │    │ │
│ │  │     22     │     18     │      4     │   1.580    │           │    │ │
│ │  └────────────┴────────────┴────────────┴────────────┘           │    │ │
│ │  └────────────────────────────────────────────────────────────────┘    │ │
│ │                                                                          │ │
│ │  Exibindo 22 políticas de consumidores                                  │ │
│ │                                                                          │ │
│ │  ┌──────────────────────────────────────────────────────────────────┐  │ │
│ │  │Código│Política/Nome     │Categoria  │Consumidores│Vigência │📍│⋮│  │ │
│ │  ├──────┼──────────────────┼───────────┼────────────┼─────────┼──┼──┤  │ │
│ │  │PL-001│🔐 Acesso Total   │Permissões │    1.185   │Vitalícia│✅│⋮│  │ │
│ │  │      │                  │           │            │         │  │  │  │ │
│ │  ├──────┼──────────────────┼───────────┼────────────┼─────────┼──┼──┤  │ │
│ │  │PL-002│💻 Limite 5 Ativos│Ativos     │    1.250   │Vitalícia│✅│⋮│  │ │
│ │  │      │                  │           │            │         │  │  │  │ │
│ │  ├──────┼──────────────────┼───────────┼────────────┼─────────┼──┼──┤  │ │
│ │  │PL-003│🏖️ Férias Auto    │Workflow   │     320    │Vitalícia│  │⋮│  │ │
│ │  │      │Aprovação         │           │            │         │  │  │  │ │
│ │  ├──────┼──────────────────┼───────────┼────────────┼─────────┼──┼──┤  │ │
│ │  │PL-004│📱 BYOD Permitido │Segurança  │     180    │31/12/25 │  │⋮│  │ │
│ │  │      │                  │           │            │         │  │  │  │ │
│ │  ├──────┼──────────────────┼───────────┼────────────┼─────────┼──┼──┤  │ │
│ │  │PL-005│🚫 Bloqueio Noturno│Segurança  │     850    │Vitalícia│  │⋮│  │ │
│ │  │      │22h-6h            │           │            │         │  │  │  │ │
│ │  └──────┴──────────────────┴───────────┴────────────┴─────────┴──┴──┘  │ │
│ │                                                                          │ │
│ │  [◀ Anterior]  Página 1 de 2  [Próximo ▶]                              │ │
│ │                                                                          │ │
│ └────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Categorias de Políticas:**
- 🔐 Permissões = Controle de acesso a sistemas
- 💻 Ativos = Limites e regras de atribuição
- 🏖️ Workflow = Aprovações e processos
- 📱 Segurança = Bloqueios, restrições, BYOD
- 📅 Temporalidade = Renovação, vigência
- 💰 Financeiro = Aprovação de custos

**Política Padrão (📍):**
- ✅ = Política aplicada automaticamente a novos consumidores

**Menu de Ações (⋮):**
- 👁️ Visualizar Detalhes
- ✏️ Editar
- 🗑️ Inativar
- 📋 Listar Consumidores
- 📍 Definir como Padrão
- 🧪 Testar Política

---

## Tela 02 - Detalhes da Política (Desktop)

**Rota:** `/gestao/politicas-consumidores/:id`
**Permissão:** `POLITICAS_CONSUMIDORES.VISUALIZAR`
**UC:** UC02

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ ≡ IControlIT                    🔍 Buscar  📊  🔔  👤 João Silva            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│ Home > Gestão > Políticas > PL-002 - Limite 5 Ativos                        │
│                                                                              │
│ ┌────────────────────────────────────────────────────────────────────────┐ │
│ │                                                                          │ │
│ │  [← Voltar]  💻 PL-002 - Limite 5 Ativos (Padrão) [✏️ Editar] [🧪 Test]│ │
│ │                                                                          │ │
│ │  Categoria: Ativos  •  Status: ✅ Ativa  •  Atualizado: 10/01/2024      │ │
│ │                                                                          │ │
│ │  ┌────────────────────────────────────────────────────────────────┐    │ │
│ │  │ 📋 Informações Gerais                                          │    │ │
│ │  ├────────────────────────────────────────────────────────────────┤    │ │
│ │  │                                                                 │    │ │
│ │  │  Código:           PL-002                                      │    │ │
│ │  │  Nome:             Limite 5 Ativos                             │    │ │
│ │  │  Categoria:        💻 Ativos                                   │    │ │
│ │  │  Prioridade:       Alta (10/10)                                │    │ │
│ │  │  Vigência:         Vitalícia (sem data de término)             │    │ │
│ │  │  Política Padrão:  ✅ Sim                                      │    │ │
│ │  │                                                                 │    │ │
│ │  │  Descrição:                                                    │    │ │
│ │  │  Limita atribuição de até 5 ativos simultâneos por            │    │ │
│ │  │  consumidor. Exceções para diretoria (até 10 ativos).         │    │ │
│ │  │                                                                 │    │ │
│ │  └────────────────────────────────────────────────────────────────┘    │ │
│ │                                                                          │ │
│ │  ┌────────────────────────────────────────────────────────────────┐    │ │
│ │  │ 🎯 Regras Configuradas                                         │    │ │
│ │  ├────────────────────────────────────────────────────────────────┤    │ │
│ │  │                                                                 │    │ │
│ │  │  ✅ Limite Máximo de Ativos: 5                                 │    │ │
│ │  │  ✅ Bloqueia atribuição ao atingir limite                      │    │ │
│ │  │  ✅ Notifica gestor quando atingir 4 ativos (80%)              │    │ │
│ │  │  ✅ Permite override para perfil "Diretoria" (até 10)          │    │ │
│ │  │  ❌ NÃO permite auto-atribuição sem aprovação                  │    │ │
│ │  │  ✅ Requer justificativa para exceder limite                   │    │ │
│ │  │                                                                 │    │ │
│ │  │  Exceções Configuradas:                                        │    │ │
│ │  │  • Perfil "Diretoria": até 10 ativos                          │    │ │
│ │  │  • Perfil "TI - Suporte": até 8 ativos                        │    │ │
│ │  │  • Home Office: +1 ativo (notebook adicional)                 │    │ │
│ │  │                                                                 │    │ │
│ │  └────────────────────────────────────────────────────────────────┘    │ │
│ │                                                                          │ │
│ │  ┌────────────────────────────────────────────────────────────────┐    │ │
│ │  │ 📊 Estatísticas de Aplicação                                   │    │ │
│ │  ├────────────────────────────────────────────────────────────────┤    │ │
│ │  │                                                                 │    │ │
│ │  │  Consumidores Afetados:     1.250                              │    │ │
│ │  │  Taxa de Conformidade:      98.5% (1.231 em conformidade)      │    │ │
│ │  │                                                                 │    │ │
│ │  │  Distribuição de Uso:                                          │    │ │
│ │  │  • 0-2 ativos:    420 consumidores (33.6%)                     │    │ │
│ │  │  • 3-4 ativos:    680 consumidores (54.4%)                     │    │ │
│ │  │  • 5 ativos:      131 consumidores (10.5%) ← No limite         │    │ │
│ │  │  • 6+ ativos:      19 consumidores (1.5%)  ← Exceções          │    │ │
│ │  │                                                                 │    │ │
│ │  │  Violações (últimos 30 dias):                                  │    │ │
│ │  │  • Tentativas bloqueadas:  28 (política funcionando)           │    │ │
│ │  │  • Overrides aprovados:     5 (diretoria)                      │    │ │
│ │  │  • Violações ativas:        0 (100% conformidade)              │    │ │
│ │  │                                                                 │    │ │
│ │  └────────────────────────────────────────────────────────────────┘    │ │
│ │                                                                          │ │
│ │  ┌────────────────────────────────────────────────────────────────┐    │ │
│ │  │ 🏢 Consumidores no Limite (131)               [Ver Todos]      │    │ │
│ │  ├────────────────────────────────────────────────────────────────┤    │ │
│ │  │                                                                 │    │ │
│ │  │  ┌───────────────┬──────────┬───────┬──────────────────────┐  │    │ │
│ │  │  │Consumidor     │Setor     │Ativos │Última Atribuição     │  │    │ │
│ │  │  ├───────────────┼──────────┼───────┼──────────────────────┤  │    │ │
│ │  │  │João Silva     │TI        │  5/5  │15/01/2025 (notebook) │  │    │ │
│ │  │  ├───────────────┼──────────┼───────┼──────────────────────┤  │    │ │
│ │  │  │Maria Santos   │Financeiro│  5/5  │10/01/2025 (celular)  │  │    │ │
│ │  │  ├───────────────┼──────────┼───────┼──────────────────────┤  │    │ │
│ │  │  │Pedro Costa    │RH        │  5/5  │05/01/2025 (tablet)   │  │    │ │
│ │  │  └───────────────┴──────────┴───────┴──────────────────────┘  │    │ │
│ │  │                                                                 │    │ │
│ │  │  Exibindo top 3 de 131 no limite                               │    │ │
│ │  │                                                                 │    │ │
│ │  └────────────────────────────────────────────────────────────────┘    │ │
│ │                                                                          │ │
│ │  ┌────────────────────────────────────────────────────────────────┐    │ │
│ │  │ 📈 Gráfico de Conformidade (Últimos 12 meses)                  │    │ │
│ │  ├────────────────────────────────────────────────────────────────┤    │ │
│ │  │                                                                 │    │ │
│ │  │100%┤████████████████████████████████████████████████████       │    │ │
│ │  │    │                                                            │    │ │
│ │  │ 95%┤                                                            │    │ │
│ │  │    │                                                            │    │ │
│ │  │ 90%┤                                                            │    │ │
│ │  │    │                                                            │    │ │
│ │  │ 85%└─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─   │    │ │
│ │  │    J  F  M  A  M  J  J  A  S  O  N  D                        │    │ │
│ │  │                                                                 │    │ │
│ │  │  ─ Taxa de Conformidade (%) ─ Meta: 95%                        │    │ │
│ │  │                                                                 │    │ │
│ │  └────────────────────────────────────────────────────────────────┘    │ │
│ │                                                                          │ │
│ │  ┌────────────────────────────────────────────────────────────────┐    │ │
│ │  │ 📝 Auditoria                                                   │    │ │
│ │  ├────────────────────────────────────────────────────────────────┤    │ │
│ │  │  Criado em: 10/01/2024 às 09:00 por Admin Sistema             │    │ │
│ │  │  Última atualização: Nunca alterado (política original)       │    │ │
│ │  └────────────────────────────────────────────────────────────────┘    │ │
│ │                                                                          │ │
│ └────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Tela 03 - Formulário de Criação/Edição (Desktop)

**Rota:** `/gestao/politicas-consumidores/novo` ou `/gestao/politicas-consumidores/:id/editar`
**Permissão:** `POLITICAS_CONSUMIDORES.CRIAR` / `POLITICAS_CONSUMIDORES.EDITAR`
**UC:** UC01 / UC03

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ ≡ IControlIT                    🔍 Buscar  📊  🔔  👤 João Silva            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│ Home > Gestão > Políticas de Consumidores > Nova Política                   │
│                                                                              │
│ ┌────────────────────────────────────────────────────────────────────────┐ │
│ │                                                                          │ │
│ │  [← Voltar]  Nova Política de Consumidor                                │ │
│ │                                                                          │ │
│ │  ┌────────────────────────────────────────────────────────────────┐    │ │
│ │  │ 📋 Informações Básicas                                         │    │ │
│ │  ├────────────────────────────────────────────────────────────────┤    │ │
│ │  │                                                                 │    │ │
│ │  │  Código da Política *                                          │    │ │
│ │  │  [PL-______]  (gerado automaticamente)                        │    │ │
│ │  │                                                                 │    │ │
│ │  │  Nome da Política *                                            │    │ │
│ │  │  [_______________________________________________]             │    │ │
│ │  │  Ex: Limite 5 Ativos, Bloqueio Noturno, BYOD Permitido        │    │ │
│ │  │                                                                 │    │ │
│ │  │  Categoria *                                                   │    │ │
│ │  │  [Ativos                                         ▼]            │    │ │
│ │  │  Opções:                                                       │    │ │
│ │  │  • Permissões - Controle de acesso a sistemas                 │    │ │
│ │  │  • Ativos - Limites e regras de atribuição                    │    │ │
│ │  │  • Workflow - Aprovações e processos                          │    │ │
│ │  │  • Segurança - Bloqueios, restrições, BYOD                    │    │ │
│ │  │  • Temporalidade - Renovação, vigência                        │    │ │
│ │  │  • Financeiro - Aprovação de custos                           │    │ │
│ │  │                                                                 │    │ │
│ │  │  Prioridade *                                                  │    │ │
│ │  │  [Alta (10/10)                                   ▼]            │    │ │
│ │  │  1=Baixa, 5=Média, 10=Alta (aplicação em conflito)            │    │ │
│ │  │                                                                 │    │ │
│ │  │  Empresa *                                                     │    │ │
│ │  │  [Acme Corp - 12.345.678/0001-90                ▼]            │    │ │
│ │  │                                                                 │    │ │
│ │  │  Descrição *                                                   │    │ │
│ │  │  [_______________________________________________]             │    │ │
│ │  │  [_______________________________________________]             │    │ │
│ │  │  [_______________________________________________]             │    │ │
│ │  │                                                                 │    │ │
│ │  └────────────────────────────────────────────────────────────────┘    │ │
│ │                                                                          │ │
│ │  ┌────────────────────────────────────────────────────────────────┐    │ │
│ │  │ 🎯 Regras da Política (varia conforme categoria)               │    │ │
│ │  ├────────────────────────────────────────────────────────────────┤    │ │
│ │  │                                                                 │    │ │
│ │  │  (Exemplo para categoria "Ativos")                             │    │ │
│ │  │                                                                 │    │ │
│ │  │  Tipo de Restrição:                                            │    │ │
│ │  │  (•) Limite de quantidade de ativos                           │    │ │
│ │  │  ( ) Tipos de ativos permitidos                               │    │ │
│ │  │  ( ) Valor máximo de ativos                                   │    │ │
│ │  │  ( ) Prazo de devolução obrigatório                           │    │ │
│ │  │                                                                 │    │ │
│ │  │  Limite Máximo de Ativos *                                     │    │ │
│ │  │  [_____] ativos simultâneos                                   │    │ │
│ │  │                                                                 │    │ │
│ │  │  Ação ao Atingir Limite:                                       │    │ │
│ │  │  [✓] Bloquear novas atribuições                               │    │ │
│ │  │  [✓] Notificar gestor                                         │    │ │
│ │  │  [✓] Exigir justificativa para override                       │    │ │
│ │  │  [ ] Permitir override automático para certos perfis          │    │ │
│ │  │                                                                 │    │ │
│ │  │  Alertas:                                                      │    │ │
│ │  │  [ ] Notificar ao atingir [___%] do limite                    │    │ │
│ │  │  [ ] Enviar relatório semanal de consumidores próximos        │    │ │
│ │  │                                                                 │    │ │
│ │  └────────────────────────────────────────────────────────────────┘    │ │
│ │                                                                          │ │
│ │  ┌────────────────────────────────────────────────────────────────┐    │ │
│ │  │ 🎭 Exceções (Opcional)                                         │    │ │
│ │  ├────────────────────────────────────────────────────────────────┤    │ │
│ │  │                                                                 │    │ │
│ │  │  [+ Adicionar Exceção]                                         │    │ │
│ │  │                                                                 │    │ │
│ │  │  ┌────────────────────────────────────────────────────────┐   │    │ │
│ │  │  │ Exceção 1                                         [X]  │   │    │ │
│ │  │  ├────────────────────────────────────────────────────────┤   │    │ │
│ │  │  │                                                         │   │    │ │
│ │  │  │  Perfil/Grupo:  [Diretoria                       ▼]    │   │    │ │
│ │  │  │  Novo Limite:   [10] ativos                            │   │    │ │
│ │  │  │  Justificativa: [Diretores possuem mais equipamentos] │   │    │ │
│ │  │  │                                                         │   │    │ │
│ │  │  └────────────────────────────────────────────────────────┘   │    │ │
│ │  │                                                                 │    │ │
│ │  │  ┌────────────────────────────────────────────────────────┐   │    │ │
│ │  │  │ Exceção 2                                         [X]  │   │    │ │
│ │  │  ├────────────────────────────────────────────────────────┤   │    │ │
│ │  │  │                                                         │   │    │ │
│ │  │  │  Perfil/Grupo:  [TI - Suporte                    ▼]    │   │    │ │
│ │  │  │  Novo Limite:   [8] ativos                             │   │    │ │
│ │  │  │  Justificativa: [Equipe TI precisa de + equipamentos] │   │    │ │
│ │  │  │                                                         │   │    │ │
│ │  │  └────────────────────────────────────────────────────────┘   │    │ │
│ │  │                                                                 │    │ │
│ │  └────────────────────────────────────────────────────────────────┘    │ │
│ │                                                                          │ │
│ │  ┌────────────────────────────────────────────────────────────────┐    │ │
│ │  │ 📅 Vigência                                                    │    │ │
│ │  ├────────────────────────────────────────────────────────────────┤    │ │
│ │  │                                                                 │    │ │
│ │  │  Tipo de Vigência:                                             │    │ │
│ │  │  (•) Vitalícia (sem data de término)                          │    │ │
│ │  │  ( ) Temporária (com data de término)                         │    │ │
│ │  │                                                                 │    │ │
│ │  │  (Se Temporária)                                               │    │ │
│ │  │  Data de Início:   [__/__/____] 📅                            │    │ │
│ │  │  Data de Término:  [__/__/____] 📅                            │    │ │
│ │  │                                                                 │    │ │
│ │  │  [ ] Notificar 30 dias antes do término                       │    │ │
│ │  │  [ ] Renovar automaticamente ao vencer                        │    │ │
│ │  │                                                                 │    │ │
│ │  └────────────────────────────────────────────────────────────────┘    │ │
│ │                                                                          │ │
│ │  ┌────────────────────────────────────────────────────────────────┐    │ │
│ │  │ 🎯 Aplicação                                                   │    │ │
│ │  ├────────────────────────────────────────────────────────────────┤    │ │
│ │  │                                                                 │    │ │
│ │  │  Aplicar a:                                                    │    │ │
│ │  │  (•) Todos os consumidores                                    │    │ │
│ │  │  ( ) Tipos específicos de consumidores                        │    │ │
│ │  │  ( ) Setores específicos                                      │    │ │
│ │  │  ( ) Consumidores específicos                                 │    │ │
│ │  │                                                                 │    │ │
│ │  │  (Campos de seleção aparecem conforme opção)                  │    │ │
│ │  │                                                                 │    │ │
│ │  │  [ ] Aplicar retroativamente a consumidores existentes        │    │ │
│ │  │  [✓] Aplicar automaticamente a novos consumidores             │    │ │
│ │  │                                                                 │    │ │
│ │  └────────────────────────────────────────────────────────────────┘    │ │
│ │                                                                          │ │
│ │  ┌────────────────────────────────────────────────────────────────┐    │ │
│ │  │ ⚙️ Configurações                                               │    │ │
│ │  ├────────────────────────────────────────────────────────────────┤    │ │
│ │  │                                                                 │    │ │
│ │  │  Status                                                        │    │ │
│ │  │  (•) Ativa    ( ) Inativa                                     │    │ │
│ │  │                                                                 │    │ │
│ │  │  [ ] Definir como política padrão                             │    │ │
│ │  │  [✓] Permitir overrides com justificativa                     │    │ │
│ │  │  [✓] Auditar todas as violações                               │    │ │
│ │  │  [ ] Modo de teste (não bloqueia, apenas alerta)              │    │ │
│ │  │                                                                 │    │ │
│ │  │  Observações                                                   │    │ │
│ │  │  [_______________________________________________]             │    │ │
│ │  │  [_______________________________________________]             │    │ │
│ │  │                                                                 │    │ │
│ │  └────────────────────────────────────────────────────────────────┘    │ │
│ │                                                                          │ │
│ │  [Cancelar]                      [🧪 Testar Política]  [Salvar]        │ │
│ │                                                                          │ │
│ └────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Tela 04 - Dashboard de Conformidade (Desktop)

**Rota:** `/gestao/politicas-consumidores/dashboard-conformidade`
**Permissão:** `POLITICAS_CONSUMIDORES.RELATORIOS`
**UC:** Custom

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ ≡ IControlIT                    🔍 Buscar  📊  🔔  👤 João Silva            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│ Home > Gestão > Políticas > Dashboard de Conformidade                       │
│                                                                              │
│ ┌────────────────────────────────────────────────────────────────────────┐ │
│ │                                                                          │ │
│ │  Dashboard de Conformidade de Políticas         [📊 Relatório] [🖨️]   │ │
│ │                                                                          │ │
│ │  Período: [Últimos 30 dias  ▼]  [Este Mês] [Últimos 12 Meses]          │ │
│ │                                                                          │ │
│ │  ┌──────────────────┬──────────────────┬──────────────────┐            │ │
│ │  │ Taxa Geral       │ Violações Ativas │ Overrides Aprovad│            │ │
│ │  ├──────────────────┼──────────────────┼──────────────────┤            │ │
│ │  │   98.2% 🟢       │        5         │       28         │            │ │
│ │  │   (+0.3% vs mês) │   (↘️ -2)         │   (↗️ +8)        │            │ │
│ │  └──────────────────┴──────────────────┴──────────────────┘            │ │
│ │                                                                          │ │
│ │  ┌────────────────────────────────────────────────────────────────┐    │ │
│ │  │ 📊 Conformidade por Política                  [🔍 Filtrar]     │    │ │
│ │  ├────────────────────────────────────────────────────────────────┤    │ │
│ │  │                                                                 │    │ │
│ │  │  ┌──────────────────────────────────────────────────────────┐ │    │ │
│ │  │  │Política        │Consumid│Conform│Violações│Taxa │Tendência│ │    │ │
│ │  │  ├────────────────┼────────┼───────┼─────────┼─────┼─────────┤ │    │ │
│ │  │  │Limite 5 Ativos │  1.250 │ 1.231 │    0    │98.5%│   🟢    │ │    │ │
│ │  │  ├────────────────┼────────┼───────┼─────────┼─────┼─────────┤ │    │ │
│ │  │  │Acesso Total    │  1.185 │ 1.185 │    0    │ 100%│   🟢    │ │    │ │
│ │  │  ├────────────────┼────────┼───────┼─────────┼─────┼─────────┤ │    │ │
│ │  │  │Bloqueio Noturno│   850  │  847  │    3    │99.6%│   🟢    │ │    │ │
│ │  │  ├────────────────┼────────┼───────┼─────────┼─────┼─────────┤ │    │ │
│ │  │  │BYOD Permitido  │   180  │  178  │    2    │98.9%│   🟡    │ │    │ │
│ │  │  ├────────────────┼────────┼───────┼─────────┼─────┼─────────┤ │    │ │
│ │  │  │Férias Auto Aprov│  320  │  320  │    0    │ 100%│   🟢    │ │    │ │
│ │  │  └────────────────┴────────┴───────┴─────────┴─────┴─────────┘ │    │ │
│ │  │                                                                 │    │ │
│ │  └────────────────────────────────────────────────────────────────┘    │ │
│ │                                                                          │ │
│ │  ┌──────────────────────────┐ ┌──────────────────────────────────┐    │ │
│ │  │ 📈 Evolução de Conform.  │ │ 🔴 Violações por Categoria       │    │ │
│ │  ├──────────────────────────┤ ├──────────────────────────────────┤    │ │
│ │  │                          │ │                                  │    │ │
│ │  │  100%┤████████████████   │ │  Ativos:      3 violações (60%)  │    │ │
│ │  │      │                   │ │  Segurança:   2 violações (40%)  │    │ │
│ │  │   95%┤                   │ │  Permissões:  0 violações        │    │ │
│ │  │      │                   │ │  Workflow:    0 violações        │    │ │
│ │  │   90%└─┴─┴─┴─┴─┴─┴─┴─   │ │                                  │    │ │
│ │  │      J F M A M J J A S O │ │  [Detalhamento]                  │    │ │
│ │  │                          │ │                                  │    │ │
│ │  └──────────────────────────┘ └──────────────────────────────────┘    │ │
│ │                                                                          │ │
│ │  ┌────────────────────────────────────────────────────────────────┐    │ │
│ │  │ 🚨 Violações Ativas (5)                       [Resolver Todas]  │    │ │
│ │  ├────────────────────────────────────────────────────────────────┤    │ │
│ │  │                                                                 │    │ │
│ │  │  ┌──────────────────────────────────────────────────────────┐ │    │ │
│ │  │  │Consumidor │Política      │Violação        │Desde   │Ações│ │    │ │
│ │  │  ├───────────┼──────────────┼────────────────┼────────┼─────┤ │    │ │
│ │  │  │João Silva │Bloqueio 22h  │Acesso 23:15    │18/01   │[⋮]  │ │    │ │
│ │  │  ├───────────┼──────────────┼────────────────┼────────┼─────┤ │    │ │
│ │  │  │Ana Costa  │BYOD Proibido │Device não autor│17/01   │[⋮]  │ │    │ │
│ │  │  ├───────────┼──────────────┼────────────────┼────────┼─────┤ │    │ │
│ │  │  │Pedro Lima │Bloqueio 22h  │Acesso 22:45    │17/01   │[⋮]  │ │    │ │
│ │  │  ├───────────┼──────────────┼────────────────┼────────┼─────┤ │    │ │
│ │  │  │Maria Dias │BYOD Proibido │Device não autor│16/01   │[⋮]  │ │    │ │
│ │  │  ├───────────┼──────────────┼────────────────┼────────┼─────┤ │    │ │
│ │  │  │Carlos Neto│Bloqueio 22h  │Acesso 01:30    │15/01   │[⋮]  │ │    │ │
│ │  │  └───────────┴──────────────┴────────────────┴────────┴─────┘ │    │ │
│ │  │                                                                 │    │ │
│ │  └────────────────────────────────────────────────────────────────┘    │ │
│ │                                                                          │ │
│ │  ┌────────────────────────────────────────────────────────────────┐    │ │
│ │  │ 💡 Insights e Recomendações                                    │    │ │
│ │  ├────────────────────────────────────────────────────────────────┤    │ │
│ │  │                                                                 │    │ │
│ │  │  🟢 Excelente Conformidade:                                    │    │ │
│ │  │  • 98.2% de conformidade geral (meta: 95%)                     │    │ │
│ │  │  • 2 políticas com 100% de conformidade                        │    │ │
│ │  │                                                                 │    │ │
│ │  │  🟡 Pontos de Atenção:                                         │    │ │
│ │  │  • 3 violações de bloqueio noturno (investigar urgência)      │    │ │
│ │  │  • 2 dispositivos BYOD não autorizados (risco segurança)      │    │ │
│ │  │                                                                 │    │ │
│ │  │  📊 Recomendações:                                             │    │ │
│ │  │  1. Revisar política de bloqueio noturno (muitas violações)   │    │ │
│ │  │  2. Implementar MFA para acessos fora de horário              │    │ │
│ │  │  3. Treinar usuários sobre políticas de BYOD                  │    │ │
│ │  │                                                                 │    │ │
│ │  └────────────────────────────────────────────────────────────────┘    │ │
│ │                                                                          │ │
│ └────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Modal 01 - Testar Política

**Trigger:** Botão [🧪 Testar Política]
**UC:** UC01

```
┌──────────────────────────────────────────────────────────────┐
│  Testar Política - PL-002 Limite 5 Ativos              [X]  │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  Simule a aplicação desta política em um cenário real.      │
│                                                               │
│  Consumidor de Teste                                         │
│  [João Silva - 001234                            ▼]          │
│                                                               │
│  Ativos Atuais: 4/5                                          │
│  • Notebook Dell Latitude                                    │
│  • Celular Samsung S21                                       │
│  • Desktop HP Elite                                          │
│  • Ramal 1001                                                │
│                                                               │
│  Ação de Teste:                                              │
│  (•) Tentar atribuir novo ativo                             │
│  ( ) Tentar exceder limite                                  │
│  ( ) Simular override de diretoria                          │
│                                                               │
│  Novo Ativo para Teste:                                      │
│  [Tablet iPad Pro                                 ▼]         │
│                                                               │
│  [Executar Teste]                                            │
│                                                               │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ 📊 Resultado do Teste:                                 │  │
│  ├────────────────────────────────────────────────────────┤  │
│  │                                                         │  │
│  │  ✅ PERMITIDO                                          │  │
│  │                                                         │  │
│  │  Consumidor possui 4 ativos, limite é 5.              │  │
│  │  Atribuição do Tablet seria permitida.                │  │
│  │  Após atribuição: 5/5 (no limite)                     │  │
│  │                                                         │  │
│  │  ⚠️ Alertas que seriam disparados:                     │  │
│  │  • Notificação ao gestor (limite 80% atingido)        │  │
│  │  • E-mail ao consumidor (você está no limite)         │  │
│  │                                                         │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                               │
│  [Fechar]                             [Executar Novo Teste]  │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

---

## Modal 02 - Adicionar Exceção

**Trigger:** Botão [+ Adicionar Exceção]
**UC:** UC01/UC03

```
┌──────────────────────────────────────────────────────────────┐
│  Adicionar Exceção à Política                           [X]  │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  Perfil ou Grupo *                                           │
│  [Diretoria                                       ▼]         │
│  Opções: Diretoria, Gerência, TI, RH, Comercial, etc.       │
│                                                               │
│  Tipo de Exceção *                                           │
│  (•) Alterar limite numérico                                │
│  ( ) Remover restrição completamente                        │
│  ( ) Alterar comportamento                                  │
│                                                               │
│  Novo Valor/Limite *                                         │
│  [10] ativos (política padrão: 5)                           │
│                                                               │
│  Justificativa *                                             │
│  [_______________________________________________]            │
│  [_______________________________________________]            │
│  Ex: Diretores necessitam de mais equipamentos para          │
│      atender múltiplas demandas corporativas.                │
│                                                               │
│  Vigência da Exceção                                         │
│  (•) Permanente                                             │
│  ( ) Temporária (até [__/__/____] 📅)                       │
│                                                               │
│  [ ] Requerer aprovação para aplicar esta exceção           │
│                                                               │
│  [Cancelar]                                     [Adicionar]  │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

---

## Modal 03 - Resolver Violação

**Trigger:** Menu ações (⋮) em violação ativa
**UC:** Custom

```
┌──────────────────────────────────────────────────────────────┐
│  Resolver Violação de Política                         [X]  │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  Violação:                                                   │
│  Consumidor: João Silva (001234)                             │
│  Política: PL-005 - Bloqueio Noturno 22h-6h                  │
│  Violação: Acesso às 23:15 do dia 18/01/2025                │
│  Desde: 18/01/2025 23:15                                     │
│                                                               │
│  Detalhes:                                                   │
│  • IP: 192.168.1.50                                          │
│  • Sistema: Portal Web - Chrome                             │
│  • Localização: São Paulo, SP                               │
│  • Duração: 45 minutos                                       │
│                                                               │
│  Como resolver?                                              │
│  (•) Aprovar acesso excepcional (justificado)               │
│  ( ) Bloquear conta até esclarecimento                      │
│  ( ) Notificar gestor para decisão                          │
│  ( ) Registrar como falso positivo                          │
│                                                               │
│  Justificativa *                                             │
│  [_______________________________________________]            │
│  [_______________________________________________]            │
│                                                               │
│  Ações Adicionais:                                           │
│  [ ] Notificar consumidor sobre a violação                  │
│  [✓] Registrar no histórico de auditoria                    │
│  [ ] Criar exceção permanente para este consumidor          │
│                                                               │
│  [Cancelar]                                       [Resolver] │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

---

## Modal 04 - Conflitos de Políticas

**Trigger:** Sistema detecta conflito ao salvar
**UC:** UC01/UC03

```
┌──────────────────────────────────────────────────────────────┐
│  ⚠️ Conflito de Políticas Detectado                     [X]  │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  A política que você está criando conflita com:             │
│                                                               │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ PL-006 - Limite 3 Ativos para Estagiários             │  │
│  ├────────────────────────────────────────────────────────┤  │
│  │ Prioridade: Média (5/10)                               │  │
│  │ Aplicada a: Tipo "Estagiário"                         │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                               │
│  Nova Política:                                              │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ PL-002 - Limite 5 Ativos                               │  │
│  ├────────────────────────────────────────────────────────┤  │
│  │ Prioridade: Alta (10/10)                               │  │
│  │ Aplicada a: Todos os consumidores                      │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                               │
│  Resolução:                                                  │
│  Como as políticas se aplicam ao mesmo público               │
│  (estagiários estão em "todos"), o sistema usará:           │
│                                                               │
│  ✅ PL-002 (prioridade 10) prevalece sobre PL-006 (prior. 5)│
│                                                               │
│  Resultado para estagiários:                                 │
│  • Limite: 5 ativos (não 3)                                 │
│  • Política aplicada: PL-002                                │
│                                                               │
│  Deseja continuar?                                           │
│  (•) Sim, aplicar com prioridade alta                       │
│  ( ) Não, ajustar configurações                             │
│  ( ) Criar exceção para estagiários                         │
│                                                               │
│  [Cancelar]                                    [Continuar]   │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

---

## Estados da Interface

### Estado 01 - Carregando Lista
```
┌────────────────────────────────────────┐
│  Gestão de Políticas de Consumidores   │
├────────────────────────────────────────┤
│          [===🔄===]                     │
│    Carregando políticas...              │
└────────────────────────────────────────┘
```

### Estado 02 - Nenhuma Política Cadastrada
```
┌────────────────────────────────────────────────────┐
│  Gestão de Políticas de Consumidores               │
├────────────────────────────────────────────────────┤
│              🎯                                     │
│     Nenhuma política cadastrada                    │
│  Crie políticas para controlar limites,            │
│  permissões e comportamentos dos consumidores.     │
│          [+ Nova Política]                         │
└────────────────────────────────────────────────────┘
```

### Estado 03 - Testando Política
```
┌────────────────────────────────────────────────────┐
│  Testar Política                                   │
├────────────────────────────────────────────────────┤
│          [===🔄===]  75%                           │
│    Executando simulação...                         │
│    Validando regras e exceções                     │
└────────────────────────────────────────────────────┘
```

---

## Notificações Toast

### Sucesso - Política Criada
```
┌──────────────────────────────────────┐
│ ✅ Política criada com sucesso!       │
│ PL-002 aplicada a 1.250 consumidores.│
└──────────────────────────────────────┘
```

### Sucesso - Teste Executado
```
┌──────────────────────────────────────┐
│ ✅ Teste concluído!                   │
│ Política funcionando conforme esperado│
└──────────────────────────────────────┘
```

### Aviso - Conflito Detectado
```
┌──────────────────────────────────────┐
│ ⚠️ Conflito com PL-006!               │
│ Verifique prioridades antes de salvar│
└──────────────────────────────────────┘
```

### Erro - Violação Ativa
```
┌──────────────────────────────────────┐
│ ❌ Não é possível inativar            │
│ 5 violações ativas. Resolva primeiro.│
└──────────────────────────────────────┘
```

---

## Notas Técnicas de Implementação

### 1. Categorias de Políticas
- **Permissões:** Acesso a sistemas, recursos, dados
- **Ativos:** Limites de quantidade, tipos, valores
- **Workflow:** Aprovações, processos, notificações
- **Segurança:** Bloqueios horários, BYOD, MFA
- **Temporalidade:** Renovações, vencimentos
- **Financeiro:** Aprovação de custos, limites orçamentários

### 2. Sistema de Prioridades
- Prioridade 1-10 (1=baixa, 10=alta)
- Em conflito, política com maior prioridade prevalece
- Exceções individuais sempre sobrepõem políticas gerais
- Alertar usuário sobre conflitos ao salvar

### 3. Validações Críticas
- Nome único por empresa
- Prioridade obrigatória
- Ao menos uma regra configurada
- Justificativa obrigatória em exceções
- Não pode ter ciclos de dependência

### 4. Motor de Regras
- Avaliação em tempo real
- Cache de políticas ativas (TTL 5 minutos)
- Auditoria de todas as aplicações
- Histórico de violações
- Notificações configuráveis

### 5. Performance
- Índices em: Categoria, Status, Prioridade, EmpresaId
- Cache de políticas por consumidor
- Lazy evaluation de regras
- Async processing de notificações

### 6. Permissões e Segurança
- `POLITICAS_CONSUMIDORES.LISTAR`
- `POLITICAS_CONSUMIDORES.VISUALIZAR`
- `POLITICAS_CONSUMIDORES.CRIAR`
- `POLITICAS_CONSUMIDORES.EDITAR`
- `POLITICAS_CONSUMIDORES.EXCLUIR`
- `POLITICAS_CONSUMIDORES.RESOLVER_VIOLACOES`
- `POLITICAS_CONSUMIDORES.OVERRIDE` (permite ignorar política)

### 7. Auditoria
- Todas as operações auditadas
- Histórico de violações (7 anos)
- Rastreabilidade de overrides
- Conformidade LGPD/GDPR

### 8. Integrações
- Active Directory (bloqueios de acesso)
- Sistema de Ativos (validação de limites)
- Workflow de Aprovação
- Sistema de Notificações (e-mail, SMS, push)

---

**Última Atualização:** 18/12/2025
**Versão:** 1.0
**Status:** ✅ Completo e Pronto para Implementação
