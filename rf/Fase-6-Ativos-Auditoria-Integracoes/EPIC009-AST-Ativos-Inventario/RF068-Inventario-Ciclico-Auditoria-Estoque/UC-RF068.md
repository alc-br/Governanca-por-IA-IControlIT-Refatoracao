# Casos de Uso - RF068

**Versão:** 1.0
**Data:** 2025-12-17
**RF Relacionado:** [RF068 - Inventario-Ciclico-Auditoria-Estoque](./RF068.md)

---

## Índice de Casos de Uso

| UC | Nome | Descrição |
|----|------|-----------|
| UC00 | UC00 - Listar Notificações | Caso de uso |
| UC02 | UC02 - Configurar Preferências de Notificação | Caso de uso |
| UC03 | UC03 - Enviar Notificação Multi-Canal | Caso de uso |
| UC05 | UC05 - Agrupar Notificações Similares | Caso de uso |
| UC08 | UC08 - Visualizar Analytics de Notificações | Caso de uso |
| UC09 | UC09 - Integrar com Microsoft Teams e Slack | Caso de uso |
| UC10 | UC10 - Enviar Push Notifications para Dispositivos Móveis | Caso de uso |
| UC11 | UC11 - Opt-out e Unsubscribe de Notificações | Caso de uso |

---

# UC00 - Listar Notificações

**RF**: RF-021 - Notificações e Alertas
**Complexidade**: Baixa
**Estimativa**: 2h Backend + 3h Frontend

---

## 📋 Objetivo

Listar notificações do usuário com filtros, badge de não lidas, marcação em lote

---

## 📝 Fluxo Principal

1. Sistema exibe sidebar com **badge** de não lidas (tempo real via SignalR)
2. Usuário clica em ícone de sino
3. Sistema lista notificações: Últimas 50, ordenadas por data decrescente
4. **Filtros**: Todas/Não lidas/Lidas, Categoria (Sistema/Aprovação/Financeiro/Operacional)
5. **Grid**: Ícone prioridade, Título, Mensagem (truncada 100 chars), Data, Status lido
6. **Ações em lote**: Marcar todas como lidas, Arquivar todas

---

## ✅ Validações

Não há validações específicas - apenas consulta

---

## 📐 Regras de Negócio

- **RN-UC00-001**: Badge atualizado em tempo real via SignalR (latência < 100ms)
- **RN-UC00-002**: Query `VW_Notificacao_Nao_Lidas` (indexada, rápida)
- **RN-UC00-003**: Notificações > 30 dias movidas para histórico automaticamente

---

## 🎨 Interface UI

```
┌─────────────────────────────────────────────────────────┐
│ Notificações (23) 🔔                           [Marcar Todas] │
├─────────────────────────────────────────────────────────┤
│ 🔴 URGENTE: Fatura #1234 venceu hoje            [👁️][✓]│
│ 📋 Você tem 3 aprovações pendentes              [👁️][✓]│
│ ✅ Backup concluído com sucesso                 [👁️][✓]│
│ ⚠️  Budget atingiu 90% (R$ 450k/R$ 500k)        [👁️][✓]│
├─────────────────────────────────────────────────────────┤
│ Filtros: ⚫ Todas  ⚪ Não Lidas  ⚪ Lidas              │
│ Categoria: [Todas ▼]                                    │
└─────────────────────────────────────────────────────────┘
```

---

## 🔍 Observações Técnicas

**SignalR Integration:**
- Hub: `notificationHub`
- Evento: `NewNotificationReceived`
- Badge atualizado em tempo real

---

# UC02 - Configurar Preferências de Notificação

**RF**: RF-021 - Notificações e Alertas
**Complexidade**: Média
**Estimativa**: 4h Backend + 5h Frontend

---

## 📋 Objetivo

Usuário configura quais notificações receber, em quais canais, em quais horários

---

## 📝 Fluxo Principal

1. Usuário acessa "Configurações → Notificações"
2. Sistema exibe preferências por categoria:
   - **Sistema**: Atualizações, manutenções
   - **Aprovações**: Pendentes, aprovadas, rejeitadas
   - **Financeiro**: Faturas, budget
   - **Operacional**: Tarefas, manutenções
3. Para cada categoria, usuário define:
   - **Canais habilitados**: ✅ In-App | ✅ E-mail | ❌ SMS | ✅ Push
   - **Horário permitido**: 08:00 - 18:00 (fora desse horário só urgentes)
   - **Frequência máxima**: Imediata, Resumo diário (09:00), Resumo semanal (segunda 09:00)
4. **Pausar notificações**: Checkbox "Não perturbe" (pausar por 1h, 4h, 24h)
5. Salva em `Notificacao_Preferencia`
6. Mensagem: "Preferências atualizadas. Você receberá notificações conforme configurado."

---

## ✅ Validações

| Campo | Regra |
|-------|-------|
| Horário início | < Horário fim |
| Ao menos 1 canal | Pelo menos 1 canal ativo por categoria |
| Telefone (se SMS) | Formato `+55 11 99999-9999` válido |
| Device token (se Push) | Token FCM/APNS registrado |

---

## 📐 Regras de Negócio

- **RN-UC02-001**: Cobrança sempre envia e-mail (regulatório, ignorar preferência)
- **RN-UC02-002**: "Não perturbe" não bloqueia notificações críticas de segurança
- **RN-UC02-003**: Telefone inválido = desabilitar SMS automaticamente

---

## 🎨 Interface UI

```
┌──────────────────────────────────────────────────────────┐
│ Preferências de Notificação                             │
├──────────────────────────────────────────────────────────┤
│ 📋 Aprovações                                            │
│   Canais: ✅ In-App  ✅ E-mail  ❌ SMS  ✅ Push           │
│   Horário: [08:00] até [18:00]                           │
│   Frequência: ⚫ Imediata  ⚪ Resumo Diário  ⚪ Semanal  │
├──────────────────────────────────────────────────────────┤
│ 💰 Financeiro                                            │
│   Canais: ✅ In-App  ✅ E-mail  ✅ SMS  ❌ Push           │
│   Horário: [00:00] até [23:59] (24h)                     │
│   Frequência: ⚫ Imediata                                │
├──────────────────────────────────────────────────────────┤
│ ⏸️  Não Perturbe: ❌ Desativado                          │
│   [ ] Pausar por 1 hora  [ ] 4 horas  [ ] 24 horas      │
├──────────────────────────────────────────────────────────┤
│              [Cancelar] [Salvar Preferências]            │
└──────────────────────────────────────────────────────────┘
```

---

# UC03 - Enviar Notificação Multi-Canal

**RF**: RF-021 - Notificações e Alertas
**Complexidade**: Alta
**Estimativa**: 8h Backend + 4h Frontend

---

## 📋 Objetivo

Processar envio de notificação através de múltiplos canais (In-App, E-mail, SMS, Push) com retry automático

---

## 📝 Fluxo Principal

1. **Background Service** (Hangfire) processa fila de notificações pendentes
2. Para cada canal habilitado:
   - **In-App**: Cria registro visível, envia via SignalR (tempo real), badge +1
   - **E-mail**: Envia via SendGrid com tracking de abertura/clique
   - **SMS**: Envia via Twilio (valida número, só texto sem dados sensíveis)
   - **Push**: Envia via FCM (Android/Web) ou APNS (iOS)
3. Registra tentativa em `Data_Envio`, atualiza `Status`
4. **Se falha**:
   - 1ª retry: Após 5min
   - 2ª retry: Após 15min
   - 3ª retry: Após 30min
   - Após 4 falhas: Marca `Status = 'Erro_Permanente'`, alerta admin
5. **Se sucesso**: Marca `Status = 'Enviada'`, registra `Data_Entrega`

---

## ✅ Validações

| Canal | Validação | Ação em Falha |
|-------|-----------|---------------|
| **In-App** | Usuário ativo | Pular canal |
| **E-mail** | E-mail válido RFC 5322 | Marcar erro, não tentar |
| **SMS** | Telefone formato `+55 XX XXXXX-XXXX` | Marcar erro, não tentar |
| **Push** | Device token ativo (< 90 dias) | Desativar token, pular |

---

## 📐 Regras de Negócio

- **RN-UC03-001**: Retry com backoff exponencial (5min, 15min, 30min)
- **RN-UC03-002**: SMS não contém dados sensíveis (validar template)
- **RN-UC03-003**: Push só para tokens ativos (`Data_Ultimo_Acesso` < 90 dias)
- **RN-UC03-004**: In-App sempre sucede (não depende de serviço externo)

---

## 🎨 Fluxo de Retry

```
Tentativa 1 (Imediata)
   ↓ Falha
Aguarda 5min → Tentativa 2
   ↓ Falha
Aguarda 15min → Tentativa 3
   ↓ Falha
Aguarda 30min → Tentativa 4
   ↓ Falha
Marca "Erro Permanente" → Alerta Admin
```

---

## 🔍 Observações Técnicas

**Integrações:**
- SendGrid para e-mail
- Twilio para SMS
- FCM/APNS para Push
- SignalR para In-App

---

# UC05 - Agrupar Notificações Similares

**RF**: RF-021 - Notificações e Alertas
**Complexidade**: Média
**Estimativa**: 4h Backend + 4h Frontend

---

## 📋 Objetivo

Agrupar notificações similares em um único item para evitar spam visual

---

## 📝 Fluxo Principal

1. Sistema detecta notificações similares (mesmo `Codigo_Template`, criadas < 1h)
2. Agrupa em uma única exibição:
   - **Título**: "3 aprovações pendentes"
   - **Corpo**: "Você tem 3 itens aguardando aprovação. Clique para ver todos."
3. Usuário clica na notificação agrupada
4. Sistema expande lista detalhada:
   - Solicitação #123 - Compra de notebook
   - Solicitação #124 - Licença software
   - Solicitação #125 - Upgrade servidor
5. Usuário pode:
   - Marcar todas como lidas
   - Abrir uma específica
   - Aprovar/Rejeitar em lote (se suportado)

---

## ✅ Validações

Não há validações específicas - agrupamento automático

---

## 📐 Regras de Negócio

- **RN-UC05-001**: Agrupamento automático para templates com `Fl_Agrupar = 1`
- **RN-UC05-002**: Notificações urgentes nunca são agrupadas
- **RN-UC05-003**: Badge conta grupo como 1 (não inflaciona contador)

---

## 🎨 Interface UI

**Regras de Agrupamento:**

| Condição | Descrição |
|----------|-----------|
| **Mesmo template** | `Codigo_Template` idêntico |
| **Mesmo destinatário** | `Destinatario_Id` idêntico |
| **Intervalo < 1h** | Criadas nos últimos 60 minutos |
| **Máx 50 notificações** | Grupos > 50 ficam "50+ aprovações pendentes" |

**Interface Agrupada:**

```
┌─────────────────────────────────────────────────────────┐
│ 🔔 Notificações (5)                                     │
├─────────────────────────────────────────────────────────┤
│ 📋 3 aprovações pendentes            [Expandir ▼][✓]   │
│    ↳ Solicitação #123 - Compra notebook                │
│    ↳ Solicitação #124 - Licença software               │
│    ↳ Solicitação #125 - Upgrade servidor               │
├─────────────────────────────────────────────────────────┤
│ 💰 5 faturas a vencer nos próximos 7 dias [Expandir ▼] │
│ ⚠️  Budget atingiu 90%                       [👁️][✓]   │
└─────────────────────────────────────────────────────────┘
```

---

# UC08 - Visualizar Analytics de Notificações

**RF**: RF-021 - Notificações e Alertas
**Complexidade**: Média
**Estimativa**: 5h Backend + 6h Frontend

---

## 📋 Objetivo

Dashboard de métricas de entrega, abertura, cliques, engajamento por canal

---

## 📝 Fluxo Principal

1. Admin acessa "Relatórios → Analytics de Notificações"
2. **Filtros**:
   - Período: [Últimos 7 dias ▼]
   - Template: [Todos ▼] ou específico
   - Canal: [Todos ▼] ou In-App/E-mail/SMS/Push
3. **Métricas Gerais**:
   - Total enviadas: 12.450
   - Taxa entrega: 98,5% (12.263/12.450)
   - Taxa abertura: 42,3% (5.187/12.263)
   - Taxa clique: 12,1% (628/5.187)
   - Tempo médio até leitura: 2h 15min
4. **Breakdown por Canal**:
   - **In-App**: 99,9% entrega | 65% abertura | 18% clique
   - **E-mail**: 98% entrega | 38% abertura | 8% clique
   - **SMS**: 97% entrega | 25% abertura | - (sem tracking)
   - **Push**: 95% entrega | 55% abertura | 15% clique
5. **Gráficos**:
   - Evolução temporal (linha)
   - Distribuição por template (pizza)
   - Heatmap de melhor horário (grid 24h x 7 dias)
6. **Top Templates**:
   - "Fatura Vencida" → 4.200 envios | 48% abertura
   - "Aprovação Pendente" → 3.100 envios | 72% abertura
7. Exportar para Excel (últimos 30 dias)

---

## ✅ Validações

Não há validações específicas - apenas consulta

---

## 📐 Regras de Negócio

- **RN-UC08-001**: Dados atualizados em tempo real (cache de 5min)
- **RN-UC08-002**: Heatmap mostra melhor dia/hora para cada tipo de notificação
- **RN-UC08-003**: Exportação limitada a 100.000 registros (evitar timeout)

---

## 🎨 Interface UI

```
┌──────────────────────────────────────────────────────────┐
│ Analytics de Notificações                  [Exportar XLS]│
├──────────────────────────────────────────────────────────┤
│ Período: [Últimos 7 dias ▼]  Template: [Todos ▼]        │
│ Canal: [Todos ▼]                                         │
├──────────────────────────────────────────────────────────┤
│ 📊 Métricas Gerais (Últimos 7 dias)                      │
│ ┌────────────┬────────────┬────────────┬────────────┐    │
│ │ Enviadas   │ Entrega    │ Abertura   │ Clique     │    │
│ │ 12.450     │ 98,5%      │ 42,3%      │ 12,1%      │    │
│ └────────────┴────────────┴────────────┴────────────┘    │
│                                                          │
│ 📈 Breakdown por Canal                                   │
│ ┌─────────┬─────────┬──────────┬─────────┐              │
│ │ Canal   │ Entrega │ Abertura │ Clique  │              │
│ ├─────────┼─────────┼──────────┼─────────┤              │
│ │ In-App  │ 99,9%   │ 65%      │ 18%     │              │
│ │ E-mail  │ 98%     │ 38%      │ 8%      │              │
│ │ SMS     │ 97%     │ 25%      │ -       │              │
│ │ Push    │ 95%     │ 55%      │ 15%     │              │
│ └─────────┴─────────┴──────────┴─────────┘              │
│                                                          │
│ 🔥 Top Templates (por abertura)                          │
│ 1. Aprovação Pendente → 72% (3.100 envios)              │
│ 2. Fatura Vencida → 48% (4.200 envios)                  │
│ 3. Backup Completo → 12% (1.800 envios)                 │
└──────────────────────────────────────────────────────────┘
```

---

## 🔍 Observações Técnicas

**Métricas Calculadas:**
```sql
-- Taxa de Entrega
(COUNT(Status = 'Enviada') / COUNT(*)) * 100

-- Taxa de Abertura
(COUNT(Data_Leitura IS NOT NULL) / COUNT(Status = 'Enviada')) * 100

-- Taxa de Clique
(COUNT(Data_Clique IS NOT NULL) / COUNT(Data_Leitura IS NOT NULL)) * 100

-- Tempo Médio até Leitura
AVG(DATEDIFF(MINUTE, Data_Envio, Data_Leitura))
```

---

# UC09 - Integrar com Microsoft Teams e Slack

**RF**: RF-021 - Notificações e Alertas
**Complexidade**: Alta
**Estimativa**: 8h Backend + 3h Frontend

---

## 📋 Objetivo

Enviar notificações para canais do Teams/Slack configurados pela empresa

---

## 📝 Fluxo Principal

1. Admin acessa "Configurações → Integrações → Teams/Slack"
2. Configura webhook:
   - **Teams**: Incoming Webhook URL (`https://outlook.office.com/webhook/...`)
   - **Slack**: Webhook URL (`https://hooks.slack.com/services/...`)
3. Define regras de envio:
   - **Canal padrão**: `#geral`, `#aprovacoes`, `#alertas-ti`
   - **Tipos de notificação**: Aprovações, Alertas de Budget, Falhas de Sistema
4. Testa conexão: Envia mensagem de teste
5. Salva configuração
6. **Quando notificação criada**:
   - Se template configurado para Teams/Slack
   - Formata mensagem (Adaptive Card para Teams, Block Kit para Slack)
   - Envia POST para webhook
   - Registra entrega em `Notificacao` (`Canal = 'Teams'` ou `'Slack'`)

---

## ✅ Validações

| Campo | Regra |
|-------|-------|
| Webhook URL | URL válida HTTPS |
| Canal | Nome válido (ex: #aprovacoes) |
| Tipos notificação | Ao menos 1 tipo selecionado |

---

## 📐 Regras de Negócio

- **RN-UC09-001**: Webhooks armazenados criptografados (Azure Key Vault)
- **RN-UC09-002**: Retry automático 3x em caso de falha (5min, 15min, 30min)
- **RN-UC09-003**: Rate limiting: Máx 10 mensagens/minuto por canal (evitar spam)
- **RN-UC09-004**: Mensagens formatadas como Adaptive Card (Teams) ou Block Kit (Slack)

---

## 🎨 Interface UI

```
┌──────────────────────────────────────────────────────────┐
│ Integração Microsoft Teams                         [x] │
├──────────────────────────────────────────────────────────┤
│ Webhook URL*:                                            │
│ [https://outlook.office.com/webhook/abc123__________]    │
│                                                          │
│ Canal Padrão*: [#aprovacoes__________]                  │
│                                                          │
│ Tipos de Notificação a Enviar:                          │
│ ✅ Aprovações Pendentes                                 │
│ ✅ Alertas de Budget                                    │
│ ✅ Falhas de Sistema                                    │
│ ❌ Notificações Gerais                                  │
│                                                          │
│ [Testar Conexão]                                         │
│ ✅ Mensagem de teste enviada com sucesso!               │
│                                                          │
│              [Cancelar] [Salvar Configuração]            │
└──────────────────────────────────────────────────────────┘
```

---

## 🔍 Observações Técnicas

**Formato Teams (Adaptive Card):**
```json
{
  "@type": "MessageCard",
  "summary": "Aprovação Pendente",
  "sections": [{
    "activityTitle": "Solicitação #123 aguarda aprovação",
    "activitySubtitle": "João Silva - R$ 4.500,00",
    "facts": [
      {"name": "Valor:", "value": "R$ 4.500,00"},
      {"name": "Centro de Custo:", "value": "TI"}
    ]
  }],
  "potentialAction": [{
    "@type": "OpenUri",
    "name": "Visualizar",
    "targets": [{"os": "default", "uri": "https://app.com/aprovacoes/123"}]
  }]
}
```

**Formato Slack (Block Kit):**
```json
{
  "text": "Aprovação Pendente",
  "blocks": [
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*Solicitação #123 aguarda aprovação*\nJoão Silva - R$ 4.500,00"
      }
    },
    {
      "type": "actions",
      "elements": [{
        "type": "button",
        "text": {"type": "plain_text", "text": "Visualizar"},
        "url": "https://app.com/aprovacoes/123"
      }]
    }
  ]
}
```

---

# UC10 - Enviar Push Notifications para Dispositivos Móveis

**RF**: RF-021 - Notificações e Alertas
**Complexidade**: Alta
**Estimativa**: 10h Backend + 8h Frontend (Mobile)

---

## 📋 Objetivo

Enviar notificações push para apps iOS/Android via Firebase Cloud Messaging (FCM) e Apple Push Notification Service (APNS)

---

## 📝 Fluxo Principal

**Setup Inicial:**
1. Admin configura credenciais FCM (arquivo `google-services.json`)
2. Configura APNS (certificado `.p12` ou Auth Key `.p8`)

**Registro de Dispositivo:**
3. Usuário faz login no app móvel
4. App obtém device token (FCM/APNS)
5. Envia `POST /api/notifications/devices/register`:
   ```json
   {
     "deviceToken": "fK3n...",
     "platform": "iOS",
     "appVersion": "1.2.3",
     "osVersion": "iOS 17.2"
   }
   ```
6. Backend salva em `Notificacao_Dispositivo` com `Fl_Ativo = 1`

**Envio de Push:**
7. Notificação criada com canal `Push` habilitado
8. Backend consulta dispositivos ativos do usuário:
   ```sql
   SELECT Device_Token, Plataforma
   FROM Notificacao_Dispositivo
   WHERE Destinatario_Id = @IdUsuario
     AND Fl_Ativo = 1
     AND Data_Ultimo_Acesso >= DATEADD(DAY, -90, GETDATE())
   ```
9. Para cada device:
   - **iOS (APNS)**: Envia payload APNs
   - **Android (FCM)**: Envia payload FCM

**Tratamento de Erros:**
10. Token inválido retornado → Marca `Fl_Ativo = 0`
11. App desinstalado → FCM/APNS retorna erro → Desativa token

**Desativação Automática:**
12. Job noturno desativa dispositivos inativos > 90 dias

---

## ✅ Validações

| Campo | Regra |
|-------|-------|
| Device Token | String não vazia, único |
| Platform | iOS ou Android |
| Limite dispositivos | Máx 5 por usuário |

---

## 📐 Regras de Negócio

- **RN-UC10-001**: Desativar tokens inativos > 90 dias automaticamente
- **RN-UC10-002**: Tokens inválidos retornados por FCM/APNS = desativar imediatamente
- **RN-UC10-003**: Limite de 5 dispositivos ativos por usuário (evitar abuso)
- **RN-UC10-004**: Badge count sincronizado com notificações não lidas

---

## 🔍 Observações Técnicas

**Payload FCM (Android/Web):**
```json
{
  "to": "fK3nL7pQ...",
  "notification": {
    "title": "Fatura Vencida",
    "body": "Fatura #1234 no valor de R$ 10.000,00 venceu hoje.",
    "icon": "ic_notification",
    "sound": "default"
  },
  "data": {
    "click_action": "FLUTTER_NOTIFICATION_CLICK",
    "id": "123",
    "type": "fatura_vencida",
    "link": "/faturas/1234"
  }
}
```

**Payload APNS (iOS):**
```json
{
  "aps": {
    "alert": {
      "title": "Fatura Vencida",
      "body": "Fatura #1234 no valor de R$ 10.000,00 venceu hoje."
    },
    "sound": "default",
    "badge": 1
  },
  "data": {
    "id": "123",
    "type": "fatura_vencida",
    "link": "/faturas/1234"
  }
}
```

---

# UC11 - Opt-out e Unsubscribe de Notificações

**RF**: RF-021 - Notificações e Alertas
**Complexidade**: Baixa
**Estimativa**: 3h Backend + 3h Frontend

---

## 📋 Objetivo

Permitir usuário desabilitar categorias específicas de notificações ou pausar temporariamente

---

## 📝 Fluxo Principal

**Opt-out de Categoria:**
1. Usuário acessa "Configurações → Notificações"
2. Desmarca categoria: ❌ Marketing | ✅ Aprovações | ✅ Financeiro
3. Sistema atualiza `Notificacao_Preferencia` → `Fl_Ativo = 0` para categoria
4. Notificações dessa categoria não são mais enviadas

**Unsubscribe via E-mail:**
5. E-mail contém link: `https://app.com/unsubscribe?token=abc123`
6. Usuário clica no link (sem login necessário)
7. Página exibe opções:
   ```
   Você não receberá mais notificações de "Newsletter Mensal"
   [ ] Desabilitar esta categoria
   [ ] Desabilitar todas as notificações de marketing
   [ ] Pausar todas as notificações por 30 dias
   [Confirmar]
   ```
8. Confirma → Desabilita categoria específica

**Pausar Temporariamente:**
9. Usuário marca "Não perturbe" por 1h/4h/24h/30 dias
10. Sistema registra `Data_Pausa_Ate = DATEADD(HOUR, 4, GETDATE())`
11. Durante pausa: Apenas notificações críticas de segurança são enviadas

**Reativar:**
12. Pausa expira automaticamente
13. Ou usuário clica "Reativar notificações" manualmente

---

## ✅ Validações

| Campo | Regra |
|-------|-------|
| Token unsubscribe | Token válido, não expirado (30 dias) |
| Período pausa | 1h, 4h, 24h ou 30 dias |

---

## 📐 Regras de Negócio

- **RN-UC11-001**: Cobrança e segurança ignoram opt-out (regulatório)
- **RN-UC11-002**: Unsubscribe link com token assinado (HMAC-SHA256, expira 30 dias)
- **RN-UC11-003**: "Pausar" não afeta notificações críticas de segurança
- **RN-UC11-004**: Histórico de opt-outs auditado (compliance LGPD)

---

## 🎨 Interface UI

**Página Unsubscribe:**

```
┌──────────────────────────────────────────────────────────┐
│ Gerenciar Preferências de Notificação                   │
├──────────────────────────────────────────────────────────┤
│ Você recebeu este e-mail porque está inscrito em         │
│ "Newsletter Mensal" do IControlIT.                       │
│                                                          │
│ Escolha uma opção:                                       │
│ ⚪ Desabilitar apenas "Newsletter Mensal"               │
│ ⚪ Desabilitar todas as notificações de Marketing       │
│ ⚪ Pausar todas as notificações por:                    │
│    ⚫ 24 horas  ⚪ 7 dias  ⚪ 30 dias                    │
│                                                          │
│ ℹ️  Você continuará recebendo notificações críticas de  │
│    segurança e cobrança (obrigatório por lei).          │
│                                                          │
│              [Cancelar] [Confirmar Preferências]         │
└──────────────────────────────────────────────────────────┘
```

**Link Unsubscribe em E-mail:**

```html
<p style="font-size: 10px; color: #666; text-align: center;">
  Não deseja mais receber esses e-mails?
  <a href="https://app.icontrolit.com/unsubscribe?token={{unsubscribe_token}}">
    Clique aqui para gerenciar suas preferências
  </a>
</p>
```

---

## Histórico de Alterações

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 1.0 | 2025-12-17 | Sistema | Consolidação de 8 casos de uso |
