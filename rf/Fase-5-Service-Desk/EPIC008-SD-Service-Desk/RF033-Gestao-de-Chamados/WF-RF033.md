# Wireframes - RF033: Gestão de Chamados

**Versão:** 1.0
**Data:** 2025-12-18
**RF Relacionado:** [RF033 - Gestão de Chamados](./RF033.md)
**UC Relacionado:** [UC-RF033 - Casos de Uso](./UC-RF033.md)

---

## ⚠️ NOTA IMPORTANTE - Padrão Fuse Admin Template

Wireframes alinhados ao **Fuse Admin Template (Angular 19)** com Material Design 3.

---

## 📋 Legenda de Símbolos

```
[Botão]   Botão clicável      🎫   Chamado      📎   Anexo
✏️         Editar              🗑️   Excluir       👁️   Visualizar
⏱️         SLA/Tempo           🔔   Notificação  ⚡   Urgente
🟢        OK/Ativo            🟡   Atenção      🔴   Crítico/Vencido
```

---

## 🗂️ Navegação Rápida

| Tela | Descrição | UC Relacionado |
|------|-----------|----------------|
| [WF-033-01](#wf-033-01-listagem-chamados) | Lista com Filtros e SLA | UC00 |
| [WF-033-02](#wf-033-02-criar-chamado) | Abrir Novo Chamado | UC01 |
| [WF-033-03](#wf-033-03-visualizar-chamado) | Detalhes com Timeline | UC02 |
| [WF-033-04](#wf-033-04-atribuir-técnico) | Distribuição Round-Robin | UC08 |
| [WF-033-05](#wf-033-05-dashboard-sla) | Monitoramento SLA | UC09 |

---

## WF-033-01: Listagem Chamados

**Descrição:** Grid de chamados com indicadores visuais de SLA, filtros avançados e priorização.
**UC Relacionado:** UC00 - Listar Chamados

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│ IControlIT                                    👤 João Silva (Técnico N2) 🔔  [Sair]│
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│ 📂 Suporte > Chamados                                                               │
│                                                                                     │
│ ┌───────────────────────────────────────────────────────────────────────────────┐ │
│ │ 🎫 GESTÃO DE CHAMADOS                                                         │ │
│ │                                                                               │ │
│ │ [+ Abrir Chamado]  [🔄 Atualizar]  [📊 Dashboard]  [⚙️ Configurações]         │ │
│ ├───────────────────────────────────────────────────────────────────────────────┤ │
│ │                                                                               │ │
│ │ ┌─ Resumo Rápido ─────────────────────────────────────────────────────────┐   │ │
│ │ │ 🔴 Críticos: 3   🟡 SLA < 20%: 8   🟢 Abertos: 42   ✅ Resolvidos Hoje: 12│   │ │
│ │ └──────────────────────────────────────────────────────────────────────────┘   │ │
│ │                                                                               │ │
│ │ 🔍 Buscar: [____________________]  Status: [Aberto ▼]  Prioridade: [Todas ▼] │ │
│ │                                                                               │ │
│ │ Filtros: ☑ Meus Chamados  ☐ Equipe  ☐ Não Atribuídos  ☐ SLA Vencido         │ │
│ ├───────────────────────────────────────────────────────────────────────────────┤ │
│ │ Mostrando 1-20 de 42 chamados                            [20 ▼] por página   │ │
│ ├───────────────────────────────────────────────────────────────────────────────┤ │
│ │                                                                               │ │
│ │ #        Título                   Solicitante  Técnico   Prior.  SLA  Status │ │
│ │ ────────────────────────────────────────────────────────────────────────────  │ │
│ │                                                                               │ │
│ │ 2025-142 🔴 Servidor travado      Ana Silva    João S.   Urgente 🔴 5%  Aberto│
│ │         Sistema produção parou                                      ⚡ CRÍTICO│
│ │                                                                     [Ver]     │ │
│ │                                                                               │ │
│ │ 2025-141 🟡 Login não funciona    Carlos O.    Maria P.  Alta    🟡15%  Atend.│
│ │         Usuário não consegue                                                  │
│ │                                                                     [Ver]     │ │
│ │                                                                               │ │
│ │ 2025-140    Solicitar acesso VPN  Pedro M.     João S.   Média   🟢75%  Atend.│
│ │         Home office                                                           │
│ │                                                                     [Ver]     │ │
│ │                                                                               │ │
│ │ 2025-139    Instalação Office     Juliana L.   (Não atrib.) Média 🟢60% Aberto│
│ │         Nova estação trabalho                                                 │
│ │                                                                     [Ver]     │ │
│ │                                                                               │ │
│ │ 2025-138 🟡 Lentidão rede         Ricardo S.   Lucas A.  Alta    🟡22%  Atend.│
│ │         Internet oscilando                                                    │
│ │                                                                     [Ver]     │ │
│ │                                                                               │ │
│ │ 2025-137    Impressora offline    Fernanda C.  João S.   Baixa   🟢85%  Atend.│
│ │         Não imprime                                                           │
│ │                                                                     [Ver]     │ │
│ │                                                                               │ │
│ │ 2025-136    Reset senha e-mail    Marcelo F.   Maria P.  Média   🟢40%  Atend.│
│ │         Esqueceu credencial                                                   │
│ │                                                                     [Ver]     │ │
│ │                                                                               │ │
│ │ ... (14 mais)                                                                 │ │
│ │                                                                               │ │
│ ├───────────────────────────────────────────────────────────────────────────────┤ │
│ │                          [◄ Anterior]  Página 1 de 3  [Próximo ►]            │ │
│ └───────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                     │
│ ℹ️ SLA: 🟢 >50% restante  🟡 20-50% restante  🔴 <20% ou vencido                   │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘

INTERAÇÕES:
• Clique em linha → Abre WF-033-03 (Visualizar)
• 🔴/🟡 → Indicador visual de urgência SLA
• [Ver] → Abre detalhes
• Filtros aplicam AND lógico
• Ordenação: Prioridade DESC, Data Abertura DESC (padrão)

VALIDAÇÕES:
• Busca em tempo real (debounce 300ms)
• Auto-refresh a cada 60s (WebSocket/SignalR para atualizações)
• Badge de SLA atualizado em tempo real
```

---

## WF-033-02: Criar Chamado

**Descrição:** Formulário de abertura com sugestão automática de prioridade e cálculo de SLA.
**UC Relacionado:** UC01 - Criar Chamado

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│ 🎫 ABRIR NOVO CHAMADO                                                 [Ajuda] [✕]  │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│ ┌─────────────────────────────────────────────────────────────────────────────┐   │
│ │ 1. DESCRIÇÃO DO PROBLEMA                                                    │   │
│ ├─────────────────────────────────────────────────────────────────────────────┤   │
│ │                                                                             │   │
│ │ Título do Chamado * (mínimo 10 caracteres)                                 │   │
│ │ ┌───────────────────────────────────────────────────────────────────────┐   │   │
│ │ │ Sistema de vendas parado - Urgente                                    │   │   │
│ │ └───────────────────────────────────────────────────────────────────────┘   │   │
│ │ 38 / 100 caracteres                                                         │   │
│ │                                                                             │   │
│ │ Categoria * (afeta cálculo de SLA)                                          │   │
│ │ ┌───────────────────────────────────────────────────────────────────────┐   │   │
│ │ │ [Software                                                        ▼]  │   │   │
│ │ └───────────────────────────────────────────────────────────────────────┘   │   │
│ │ Opções: Hardware, Software, Rede, Acesso, Outro                            │   │
│ │                                                                             │   │
│ │ Descrição Detalhada * (mínimo 30 caracteres)                               │   │
│ │ ┌───────────────────────────────────────────────────────────────────────┐   │   │
│ │ │ O sistema de vendas travou durante fechamento do caixa. Tentei         │   │   │
│ │ │ reiniciar mas continua travado na tela de carregamento. Preciso        │   │   │
│ │ │ urgente pois temos clientes aguardando.                                │   │   │
│ │ │                                                                       │   │   │
│ │ │                                                                       │   │   │
│ │ │                                                                       │   │   │
│ │ └───────────────────────────────────────────────────────────────────────┘   │   │
│ │ 178 / 2000 caracteres                                                       │   │
│ │                                                                             │   │
│ ├─────────────────────────────────────────────────────────────────────────────┤   │
│ │ 2. PRIORIDADE E SLA                                                         │   │
│ ├─────────────────────────────────────────────────────────────────────────────┤   │
│ │                                                                             │   │
│ │ 💡 Sugestão Automática de Prioridade:                                       │   │
│ │ ┌─────────────────────────────────────────────────────────────────────┐     │   │
│ │ │ ⚡ URGENTE                                                            │     │   │
│ │ │ Detectamos palavras-chave: "parado", "urgente", "travado"           │     │   │
│ │ │ SLA: 2 horas (horário comercial)                                    │     │   │
│ │ └─────────────────────────────────────────────────────────────────────┘     │   │
│ │                                                                             │   │
│ │ Prioridade *                                                                │   │
│ │ ○ Baixa (SLA: 72h)  ○ Média (SLA: 24h)  ○ Alta (SLA: 4h)  ● Urgente (SLA: 2h)│   │
│ │                                                                             │   │
│ │ ℹ️ Prazo de atendimento calculado automaticamente com base na matriz        │   │
│ │   Prioridade × Categoria (horário comercial: 8h-18h, seg-sex)               │   │
│ │                                                                             │   │
│ ├─────────────────────────────────────────────────────────────────────────────┤   │
│ │ 3. ANEXOS (Opcional)                                                        │   │
│ ├─────────────────────────────────────────────────────────────────────────────┤   │
│ │                                                                             │   │
│ │ ┌───────────────────────────────────────────────────────────────────────┐   │   │
│ │ │ Arraste arquivos aqui ou clique para selecionar                      │   │   │
│ │ │                      📎 [Anexar Arquivos]                             │   │   │
│ │ │                                                                       │   │   │
│ │ │ Formatos aceitos: .png, .jpg, .pdf, .txt, .log (max 10MB cada)       │   │   │
│ │ │ Máximo: 5 arquivos                                                    │   │   │
│ │ └───────────────────────────────────────────────────────────────────────┘   │   │
│ │                                                                             │   │
│ └─────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                     │
│ ┌─ Preview do Chamado ──────────────────────────────────────────────────────────┐ │
│ │ Número (será gerado): 2025-XXXXXX                                             │ │
│ │ Solicitante: João Silva (joao.silva@empresa.com)                             │ │
│ │ Categoria: Software                                                           │ │
│ │ Prioridade: Urgente ⚡                                                         │ │
│ │ SLA: 2 horas (vencimento estimado: 18/12/2025 17:30)                         │ │
│ │ Status Inicial: Aberto                                                        │ │
│ └───────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                     │
│                                                                                     │
│                              [Cancelar]  [✅ Abrir Chamado]                        │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘

APÓS ENVIO (MODAL SUCESSO):

┌──────────────────────────────────────────────────┐
│ ✅ Chamado Aberto com Sucesso!                   │
├──────────────────────────────────────────────────┤
│                                                  │
│ Número: #2025-000143                             │
│ SLA: 2 horas (vencimento: 18/12 17:30)           │
│                                                  │
│ Técnico será atribuído em breve.                 │
│ Você receberá e-mail com atualizações.           │
│                                                  │
│ [Ver Chamado]  [Abrir Outro]  [Fechar]          │
│                                                  │
└──────────────────────────────────────────────────┘

VALIDAÇÕES:
• Título: 10-100 caracteres
• Descrição: 30-2000 caracteres
• Categoria: Obrigatória
• Prioridade: Obrigatória
• Anexos: Tipos permitidos, max 10MB, 5 arquivos
• Palavras-chave detectadas automaticamente: "parado", "urgente", "travado", "crítico" → Sugestão Alta/Urgente
```

---

## WF-033-03: Visualizar Chamado

**Descrição:** Detalhes completos com timeline de interações, comentários e ações disponíveis.
**UC Relacionado:** UC02 - Visualizar / UC05 - Comentar

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│ IControlIT                                    👤 João Silva (Técnico) 🔔  [Sair]   │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│ 📂 Suporte > Chamados > #2025-000142                                                │
│                                                                                     │
│ ┌───────────────────────────────────────────────────────────────────────────────┐ │
│ │ 🎫 CHAMADO #2025-000142                                                       │ │
│ │                                                                               │ │
│ │ [← Voltar]  [✏️ Editar]  [🔼 Escalar]  [✅ Resolver]  [💬 Comentar]  [📎 Anexar]│ │
│ ├───────────────────────────────────────────────────────────────────────────────┤ │
│ │                                                                               │ │
│ │ ┌─ Cabeçalho ─────────────────────────────────────────────────────────────┐   │ │
│ │ │ 🔴 Servidor travado - Sistema produção parou                            │   │ │
│ │ │                                                                         │   │ │
│ │ │ Status: 🟢 Em Atendimento  |  Prioridade: ⚡ Urgente  |  SLA: 🔴 5% (6min)│   │ │
│ │ └─────────────────────────────────────────────────────────────────────────┘   │ │
│ │                                                                               │ │
│ │ ┌─ Informações Principais ────────────────────────────────────────────────┐   │ │
│ │ │ Número:          #2025-000142                                           │   │ │
│ │ │ Solicitante:     Ana Silva (ana.silva@empresa.com)                      │   │ │
│ │ │ Técnico:         João Silva (N2) [Reatribuir]                           │   │ │
│ │ │ Categoria:       Software                                               │   │ │
│ │ │ Data Abertura:   18/12/2025 15:30                                       │   │ │
│ │ │ SLA Vencimento:  18/12/2025 17:30 (2h)  🔴 CRÍTICO - Resta 6 minutos    │   │ │
│ │ │ Tempo Decorrido: 1h 54min                                               │   │ │
│ │ └─────────────────────────────────────────────────────────────────────────┘   │ │
│ │                                                                               │ │
│ │ ┌─ Descrição ─────────────────────────────────────────────────────────────┐   │ │
│ │ │ O servidor de produção travou durante processo de fechamento de caixa. │   │ │
│ │ │ Sistema não responde. Clientes aguardando atendimento. Preciso urgente!│   │ │
│ │ └─────────────────────────────────────────────────────────────────────────┘   │ │
│ │                                                                               │ │
│ │ ┌─ Anexos (3) ────────────────────────────────────────────────────────────┐   │ │
│ │ │ 📄 screenshot_erro.png (2.5MB) [Baixar] [Preview]                       │   │ │
│ │ │ 📄 log_sistema.txt (150KB) [Baixar]                                      │   │ │
│ │ │ 📄 mensagem_erro.pdf (80KB) [Baixar] [Preview]                          │   │ │
│ │ └─────────────────────────────────────────────────────────────────────────┘   │ │
│ │                                                                               │ │
│ │ ┌─────────────────────────────────────────────────────────────────────────┐   │ │
│ │ │ [TIMELINE] [DETALHES] [HISTÓRICO]                                       │   │ │
│ │ └─────────────────────────────────────────────────────────────────────────┘   │ │
│ │                                                                               │ │
│ │ ▼ ABA: TIMELINE                                                               │ │
│ │                                                                               │ │
│ │ ┌─ Timeline de Ações ─────────────────────────────────────────────────────┐   │ │
│ │ │                                                                         │   │ │
│ │ │ 📅 18/12/2025 17:20 - João Silva (Técnico N2)                           │   │ │
│ │ │ 💬 Comentário Interno                                                   │   │ │
│ │ │    "Identificado problema no banco de dados. Executando script de      │   │ │
│ │ │     correção. Previsão de normalização em 10 minutos."                 │   │ │
│ │ │    ⚪ Interno (solicitante não vê)                                      │   │ │
│ │ │                                                                         │   │ │
│ │ │ 📅 18/12/2025 17:00 - João Silva                                        │   │ │
│ │ │ 📝 Status alterado: Aberto → Em Atendimento                             │   │ │
│ │ │ 💬 "Iniciando diagnóstico do servidor. Aguarde."                        │   │ │
│ │ │                                                                         │   │ │
│ │ │ 📅 18/12/2025 16:45 - Sistema                                           │   │ │
│ │ │ 👤 Técnico atribuído: João Silva (N2)                                   │   │ │
│ │ │ 📧 Notificação enviada                                                  │   │ │
│ │ │                                                                         │   │ │
│ │ │ 📅 18/12/2025 16:30 - Ana Silva (Solicitante)                           │   │ │
│ │ │ 📎 Anexou 3 arquivos (screenshot_erro.png, log_sistema.txt, ...)       │   │ │
│ │ │                                                                         │   │ │
│ │ │ 📅 18/12/2025 15:30 - Ana Silva                                         │   │ │
│ │ │ ✅ Chamado criado - Prioridade: Urgente                                  │   │ │
│ │ │ ⏱️ SLA: 2 horas (vencimento: 17:30)                                      │   │ │
│ │ │                                                                         │   │ │
│ │ └─────────────────────────────────────────────────────────────────────────┘   │ │
│ │                                                                               │ │
│ │ ┌─ Adicionar Comentário ──────────────────────────────────────────────────┐   │ │
│ │ │                                                                         │   │ │
│ │ │ Visibilidade: ● Externo (solicitante vê)  ○ Interno (apenas técnicos)  │   │ │
│ │ │                                                                         │   │ │
│ │ │ ┌───────────────────────────────────────────────────────────────────┐   │   │ │
│ │ │ │ Digite seu comentário aqui...                                     │   │   │ │
│ │ │ │                                                                   │   │   │ │
│ │ │ │                                                                   │   │   │ │
│ │ │ └───────────────────────────────────────────────────────────────────┘   │   │ │
│ │ │                                                                         │   │ │
│ │ │ [📎 Anexar Arquivo]                         [Enviar Comentário]         │   │ │
│ │ │                                                                         │   │ │
│ │ └─────────────────────────────────────────────────────────────────────────┘   │ │
│ │                                                                               │ │
│ └───────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘

INTERAÇÕES:
• [✏️ Editar] → Abre modal edição (prioridade, categoria, técnico)
• [🔼 Escalar] → UC06 - Escalonamento manual
• [✅ Resolver] → UC04 - Marcar como resolvido + solicitar avaliação
• [💬 Comentar] → Adiciona à timeline
• [📎 Anexar] → UC07 - Upload de arquivos
• Comentário Interno → Badge ⚪, não notifica solicitante
• Comentário Externo → Notifica solicitante por email
• Timeline atualizada em tempo real via SignalR
```

---

## WF-033-04: Atribuir Técnico

**Descrição:** Distribuição automática round-robin ou atribuição manual com visualização de carga.
**UC Relacionado:** UC08 - Atribuir Técnico

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│ 👤 ATRIBUIR TÉCNICO AO CHAMADO                                        [Ajuda] [✕]  │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│ ┌─────────────────────────────────────────────────────────────────────────────┐   │
│ │ Chamado: #2025-000139                                                       │   │
│ │ Título: Instalação Office - Nova estação trabalho                           │   │
│ │ Prioridade: Média  |  Categoria: Software  |  Nível: N1                     │   │
│ ├─────────────────────────────────────────────────────────────────────────────┤   │
│ │                                                                             │   │
│ │ Modo de Atribuição:                                                         │   │
│ │ ● Automático (Round-Robin)  ○ Manual (Selecionar Técnico)                  │   │
│ │                                                                             │   │
│ └─────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                     │
│ ┌─────────────────────────────────────────────────────────────────────────────┐   │
│ │ 💡 SUGESTÃO AUTOMÁTICA (Round-Robin)                                        │   │
│ ├─────────────────────────────────────────────────────────────────────────────┤   │
│ │                                                                             │   │
│ │ Algoritmo: Técnico com menor carga de trabalho (N1)                        │   │
│ │                                                                             │   │
│ │ ┌─ Técnico Sugerido ──────────────────────────────────────────────────┐     │   │
│ │ │ 👤 Maria Paula Silva (N1)                                           │     │   │
│ │ │ Carga Atual: 3 chamados abertos                                     │     │   │
│ │ │ Disponibilidade: Online 🟢                                           │     │   │
│ │ │ Taxa de Resolução: 92% (últimos 30 dias)                            │     │   │
│ │ │ Tempo Médio Resposta: 15 minutos                                    │     │   │
│ │ └─────────────────────────────────────────────────────────────────────┘     │   │
│ │                                                                             │   │
│ └─────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                     │
│ ┌─────────────────────────────────────────────────────────────────────────────┐   │
│ │ 📊 DISTRIBUIÇÃO DE CARGA (Técnicos N1)                                      │   │
│ ├─────────────────────────────────────────────────────────────────────────────┤   │
│ │                                                                             │   │
│ │ Técnico               Abertos  Status      Últ. Atribuição  [Selecionar]   │   │
│ │ ──────────────────────────────────────────────────────────────────────────  │   │
│ │ Maria Paula Silva       3      🟢 Online   18/12 15:45      [Atribuir]     │   │
│ │ Lucas Almeida           5      🟢 Online   18/12 17:10      [Atribuir]     │   │
│ │ Rafael Santos           7      🟢 Online   18/12 16:30      [Atribuir]     │   │
│ │ Carla Mendes            8      🔴 Ausente  18/12 14:20      [Atribuir]     │   │
│ │ Pedro Oliveira          10     🟢 Online   18/12 17:15      [Atribuir]     │   │
│ │                                                                             │   │
│ └─────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                     │
│ ℹ️ Dica: Distribuição automática considera carga, disponibilidade e performance     │
│                                                                                     │
│                                                                                     │
│                       [Cancelar]  [✅ Atribuir (Maria Paula)]                      │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘

APÓS ATRIBUIÇÃO (TOAST):

┌───────────────────────────────────────────┐
│ ✅ Chamado atribuído a Maria Paula Silva  │
│ Notificação enviada por e-mail            │
└───────────────────────────────────────────┘

VALIDAÇÕES:
• Round-robin: Menor carga + online + nível compatível
• Manual: Avisar se técnico tem > 10 chamados abertos
• Reatribuição > 3x → Notificar gestor (possível chamado complexo)
• SLA pausa 15min durante reatribuição
```

---

## WF-033-05: Dashboard SLA

**Descrição:** Dashboard gerencial de monitoramento de SLAs com KPIs e gráficos.
**UC Relacionado:** UC09 - Acompanhar SLA

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│ IControlIT                                    👤 Gestor TI  🔔  [Sair]              │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│ 📂 Suporte > Dashboard SLA                                                          │
│                                                                                     │
│ ┌───────────────────────────────────────────────────────────────────────────────┐ │
│ │ 📊 DASHBOARD DE ACOMPANHAMENTO SLA                                            │ │
│ │                                                                               │ │
│ │ Período: [Últimos 30 dias ▼]  [🔄 Atualizar]  [⬇️ Exportar PDF]               │ │
│ ├───────────────────────────────────────────────────────────────────────────────┤ │
│ │                                                                               │ │
│ │ ┌─ KPIs Principais ───────────────────────────────────────────────────────┐   │ │
│ │ │                                                                         │   │ │
│ │ │ ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │   │ │
│ │ │ │ ✅ Cumpridos  │  │ ⚠️ Vencidos   │  │ 🔴 Críticos   │  │ 📈 Taxa SLA  │ │   │ │
│ │ │ │              │  │              │  │              │  │              │ │   │ │
│ │ │ │     142      │  │      25      │  │      3       │  │     85%      │ │   │ │
│ │ │ │   (85%)      │  │    (15%)     │  │   (< 20%)    │  │   ✅ Meta    │ │   │ │
│ │ │ └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘ │   │ │
│ │ │                                                                         │   │ │
│ │ └─────────────────────────────────────────────────────────────────────────┘   │ │
│ │                                                                               │ │
│ │ ┌─ Cumprimento de SLA por Categoria ──────────────────────────────────────┐   │ │
│ │ │                                                                         │   │ │
│ │ │ Categoria         Total  Cumpridos  Vencidos  Taxa   Status            │   │ │
│ │ │ ────────────────────────────────────────────────────────────────────    │   │ │
│ │ │ Hardware           45      41 (91%)    4 (9%)  91%    ✅ Ótimo          │   │ │
│ │ │ Software           62      51 (82%)   11 (18%) 82%    🟡 Atenção        │   │ │
│ │ │ Rede               38      30 (79%)    8 (21%) 79%    🔴 Crítico        │   │ │
│ │ │ Acesso             22      20 (91%)    2 (9%)  91%    ✅ Ótimo          │   │ │
│ │ │ Outro              10      10 (100%)   0 (0%)  100%   ✅ Perfeito       │   │ │
│ │ │                                                                         │   │ │
│ │ └─────────────────────────────────────────────────────────────────────────┘   │ │
│ │                                                                               │ │
│ │ ┌─ Gráfico: Evolução SLA (Últimos 30 Dias) ───────────────────────────────┐   │ │
│ │ │  %                                                                       │   │ │
│ │ │ 100│                                                                     │   │ │
│ │ │  95│              ●─────●─────●─────●                                    │   │ │
│ │ │  90│        ●─────┘                 └─────●                 Meta: 90%   │   │ │
│ │ │  85│  ●─────┘                             └─────●─────●─────●           │   │ │
│ │ │  80│                                                                     │   │ │
│ │ │    └─────────────────────────────────────────────────────────────        │   │ │
│ │ │     Dia 1   5    10   15   20   25   30                                │   │ │
│ │ └─────────────────────────────────────────────────────────────────────────┘   │ │
│ │                                                                               │ │
│ │ ┌─ 🔥 Chamados Críticos (SLA < 20%) ───────────────────────────────────────┐   │ │
│ │ │                                                                         │   │ │
│ │ │ #        Título                   Técnico    SLA      Vence Em         │   │ │
│ │ │ ────────────────────────────────────────────────────────────────────    │   │ │
│ │ │ 2025-142 Servidor travado         João S.    🔴 5%   6 minutos  [Ver]  │   │ │
│ │ │ 2025-138 Login não funciona       Lucas A.   🟡15%   22 minutos [Ver]  │   │ │
│ │ │ 2025-135 Rede instável            Rafael S.  🟡18%   38 minutos [Ver]  │   │ │
│ │ │                                                                         │   │ │
│ │ └─────────────────────────────────────────────────────────────────────────┘   │ │
│ │                                                                               │ │
│ │ ┌─ Performance por Técnico ────────────────────────────────────────────────┐   │ │
│ │ │                                                                         │   │ │
│ │ │ Técnico           Atendidos  Taxa SLA  Tempo Médio  Avaliação          │   │ │
│ │ │ ────────────────────────────────────────────────────────────────────    │   │ │
│ │ │ João Silva           28       93%       2h 15min     ⭐⭐⭐⭐⭐ (4.8)      │   │ │
│ │ │ Maria Paula          35       89%       3h 10min     ⭐⭐⭐⭐⭐ (4.6)      │   │ │
│ │ │ Lucas Almeida        22       78%       4h 20min     ⭐⭐⭐⭐ (4.2)        │   │ │
│ │ │ Rafael Santos        31       82%       3h 45min     ⭐⭐⭐⭐ (4.4)        │   │ │
│ │ │                                                                         │   │ │
│ │ └─────────────────────────────────────────────────────────────────────────┘   │ │
│ │                                                                               │ │
│ └───────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                     │
│ ℹ️ Dashboard atualizado automaticamente a cada 5 minutos                            │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘

RECURSOS:
• Auto-refresh: 5 minutos (WebSocket/SignalR)
• Alertas sonoros quando SLA < 10%
• Drill-down: Clique em categoria → Filtra chamados
• Exportação PDF com timestamp e assinatura digital
• Cache: 5min para performance
```

---

## Modais Comuns

### Modal: Fechar Chamado

```
┌───────────────────────────────────────────────────┐
│ ✅ RESOLVER CHAMADO #2025-000142                  │
├───────────────────────────────────────────────────┤
│                                                    │
│ Solução Aplicada * (mínimo 50 caracteres):        │
│ ┌────────────────────────────────────────────┐    │
│ │ Reiniciado serviço SQL Server. Problema   │    │
│ │ causado por deadlock no banco. Aplicado   │    │
│ │ índice para prevenir recorrência.         │    │
│ │                                            │    │
│ │                                            │    │
│ └────────────────────────────────────────────┘    │
│ 120 / 1000 caracteres                             │
│                                                    │
│ Causa Raiz:                                        │
│ ● Identificada  ○ Não Identificada                │
│                                                    │
│ ☑ Enviar email ao solicitante solicitando         │
│   avaliação (1-5 estrelas)                        │
│                                                    │
│          [Cancelar]  [✅ Resolver Chamado]         │
│                                                    │
└───────────────────────────────────────────────────┘
```

### Toast: SLA Vencido

```
🔴 ALERTA: Chamado #2025-000142 - SLA vencido! [Ver]
```

---

## Estados Especiais

### Estado: Carregando

```
┌─────────────────────────────────┐
│ ⏳ Carregando chamados...       │
│    [████████░░]                 │
└─────────────────────────────────┘
```

### Estado: Vazio

```
┌─────────────────────────────────┐
│       🎫                         │
│  Nenhum chamado encontrado       │
│                                  │
│  [+ Abrir Novo Chamado]          │
└─────────────────────────────────┘
```

---

## Notas de Implementação

### Componentes Angular

```typescript
ChamadosListComponent
  imports: [
    MatTableModule,
    MatBadgeModule,    // Badges SLA
    MatChipModule,     // Status chips
    MatProgressBarModule,
    TranslocoModule,
    FuseCardComponent
  ]
```

### Endpoints API

```
GET    /api/chamados                  - Listar
POST   /api/chamados                  - Criar
GET    /api/chamados/{id}             - Detalhes
PUT    /api/chamados/{id}             - Editar
POST   /api/chamados/{id}/comentar    - Adicionar comentário
POST   /api/chamados/{id}/anexar      - Upload anexo
POST   /api/chamados/{id}/atribuir    - Atribuir técnico
POST   /api/chamados/{id}/escalar     - Escalar
POST   /api/chamados/{id}/resolver    - Resolver
GET    /api/chamados/dashboard-sla    - Dashboard
```

### SignalR Hubs

```typescript
ChamadosHub
  - OnChamadoCriado
  - OnChamadoAtualizado
  - OnComentarioAdicionado
  - OnSLACritico (< 20%)
```

---

## Histórico de Alterações

| Versão | Data       | Autor           | Descrição                      |
|--------|------------|-----------------|--------------------------------|
| 1.0    | 2025-12-18 | Architect Agent | Criação inicial - 5 wireframes |
