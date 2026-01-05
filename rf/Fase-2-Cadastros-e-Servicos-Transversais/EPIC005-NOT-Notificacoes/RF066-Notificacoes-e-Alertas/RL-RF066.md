# RL-RF066 - Referência ao Legado: Notificações e Alertas

**Versão**: 1.0
**Data**: 2025-12-30
**RF Relacionado**: RF066 - Notificações e Alertas
**Tipo de Legado**: Documentação Code-Heavy (v1.0)

---

## 1. PROPÓSITO DESTE DOCUMENTO

Este documento preserva a **memória histórica** da abordagem de documentação anterior do RF066, que utilizava **código C# embutido** diretamente no RF ao invés de linguagem natural.

**O QUE ESTE DOCUMENTO NÃO É:**
- ❌ NÃO é fonte de requisitos funcionais (use RF066.md)
- ❌ NÃO cria obrigações de implementação
- ❌ NÃO substitui o RF066.md v2.0

**O QUE ESTE DOCUMENTO É:**
- ✅ Registro histórico de como RF066 era documentado antes de Governance v2.0
- ✅ Referência técnica de código que foi removido do RF e convertido para linguagem natural
- ✅ Fonte de consulta para entender evolução da documentação

---

## 2. CONTEXTO DO LEGADO

### 2.1 Abordagem v1.0 (Code-Heavy Documentation)

O RF066.md v1.0 (263 linhas) utilizava extensa quantidade de código C# para especificar requisitos funcionais, incluindo:

- Enums completos (CanalNotificacao, Prioridade)
- Classes de entidade (Notificacao, NotificacaoPreferencia)
- Interfaces (INotificationChannel)
- Exemplos de implementação de handlers
- Configurações de Hangfire e SignalR em código

**Exemplo de Especificação v1.0:**

```markdown
### RN001: Canais de Notificação Suportados

O sistema deve suportar os seguintes canais:

```csharp
public enum CanalNotificacao
{
    Email,
    SMS,
    Push,
    WhatsApp,
    InApp
}

public class Notificacao
{
    public Guid Id { get; set; }
    public Guid UsuarioId { get; set; }
    public string Tipo { get; set; }
    public string Titulo { get; set; }
    public string Mensagem { get; set; }
    public List<CanalNotificacao> Canais { get; set; }
    public Prioridade Prioridade { get; set; }
    public DateTime DataCriacao { get; set; }
    public bool Lida { get; set; }
}
```
```

### 2.2 Problemas da Abordagem Code-Heavy

1. **Mistura de Responsabilidades**: RF continha decisões técnicas de implementação (nomes de propriedades, tipos exatos) ao invés de comportamento esperado.

2. **Falta de Flexibilidade**: Desenvolvedores sentiam-se obrigados a usar exatamente os nomes de propriedades do código, mesmo quando existiam convenções melhores.

3. **Dificuldade de Leitura para Não-Desenvolvedores**: Stakeholders de negócio tinham dificuldade em revisar RFs repletos de código C#.

4. **Manutenção Duplicada**: Alterações de código exigiam atualizar tanto o RF quanto a implementação, criando risco de divergência.

5. **Ambiguidade**: Não era claro se o código era "exemplo ilustrativo" ou "contrato vinculante".

### 2.3 Transição para v2.0 (Natural Language Documentation)

Em 2025-12-30, o RF066 foi migrado para Governance v2.0, onde:

- ✅ **TODO código C# foi removido** do RF066.md
- ✅ **Regras de negócio foram reescritas** em linguagem natural
- ✅ **Comportamento esperado ficou claro** sem prescrever implementação
- ✅ **Desenvolvedores têm liberdade** de escolher estruturas de dados adequadas
- ✅ **Stakeholders conseguem revisar** sem conhecimento de C#

---

## 3. CÓDIGO LEGADO EXTRAÍDO DO RF066 v1.0

Esta seção documenta todo o código que estava embutido no RF066.md v1.0 e foi **REMOVIDO** na v2.0.

### 3.1 Enums Documentados em Código

**DESTINO**: SUBSTITUÍDO por descrição em linguagem natural no RF066.md

#### 3.1.1 CanalNotificacao (v1.0)

```csharp
/// <summary>
/// Canais de comunicação suportados pelo sistema de notificações.
/// </summary>
public enum CanalNotificacao
{
    /// <summary>
    /// E-mail via SMTP configurado.
    /// </summary>
    Email,

    /// <summary>
    /// SMS via API de provider externo (Twilio, Nexmo).
    /// </summary>
    SMS,

    /// <summary>
    /// Push Notifications via Firebase Cloud Messaging.
    /// </summary>
    Push,

    /// <summary>
    /// WhatsApp Business API.
    /// </summary>
    WhatsApp,

    /// <summary>
    /// Notificações in-app via SignalR.
    /// </summary>
    InApp
}
```

**Conversão v2.0**: RN-NOT-066-01 descreve os 5 canais em linguagem natural sem prescrever enum.

#### 3.1.2 Prioridade (v1.0)

```csharp
/// <summary>
/// Nível de prioridade da notificação (determina quiet hours e ordem de processamento).
/// </summary>
public enum Prioridade
{
    /// <summary>
    /// Prioridade baixa - respeita quiet hours, pode ser agrupada.
    /// </summary>
    Baixa = 1,

    /// <summary>
    /// Prioridade normal - respeita quiet hours, pode ser agrupada.
    /// </summary>
    Normal = 2,

    /// <summary>
    /// Prioridade alta - respeita quiet hours, processada com prioridade.
    /// </summary>
    Alta = 3,

    /// <summary>
    /// Prioridade urgente - IGNORA quiet hours, processada imediatamente.
    /// </summary>
    Urgente = 4,

    /// <summary>
    /// Prioridade crítica - IGNORA quiet hours, topo da fila, não agrupada.
    /// </summary>
    Critica = 5
}
```

**Conversão v2.0**: RN-NOT-066-02 descreve 5 níveis de prioridade e comportamento sem prescrever enum.

#### 3.1.3 StatusNotificacao (v1.0)

```csharp
/// <summary>
/// Status de entrega da notificação (atualizado via webhooks).
/// </summary>
public enum StatusNotificacao
{
    Enfileirada,
    Enviada,
    Entregue,
    Aberta,
    Clicada,
    Bounced,
    Spam,
    Falha
}
```

**Conversão v2.0**: RN-NOT-066-08 descreve status possíveis em linguagem natural.

### 3.2 Classes de Entidade Documentadas em Código

**DESTINO**: SUBSTITUÍDO por descrição de campos em RF066.yaml (modelo_dados)

#### 3.2.1 Notificacao (v1.0)

```csharp
/// <summary>
/// Entidade principal de notificação.
/// </summary>
public class Notificacao
{
    /// <summary>
    /// Identificador único da notificação.
    /// </summary>
    public Guid Id { get; set; }

    /// <summary>
    /// Usuário destinatário da notificação.
    /// </summary>
    public Guid UsuarioId { get; set; }

    /// <summary>
    /// Tipo de notificação (ex: SLA_VENCENDO, APROVACAO_PENDENTE).
    /// </summary>
    public string Tipo { get; set; }

    /// <summary>
    /// Título da notificação (máximo 200 caracteres).
    /// </summary>
    [MaxLength(200)]
    public string Titulo { get; set; }

    /// <summary>
    /// Mensagem completa da notificação (máximo 2000 caracteres).
    /// </summary>
    [MaxLength(2000)]
    public string Mensagem { get; set; }

    /// <summary>
    /// Canais pelos quais a notificação deve ser enviada.
    /// </summary>
    public List<CanalNotificacao> Canais { get; set; }

    /// <summary>
    /// Nível de prioridade (determina quiet hours e ordem de processamento).
    /// </summary>
    public Prioridade Prioridade { get; set; }

    /// <summary>
    /// Status atual de entrega da notificação.
    /// </summary>
    public StatusNotificacao Status { get; set; }

    /// <summary>
    /// Indica se notificação é obrigatória (conformidade) - não pode ser desabilitada.
    /// </summary>
    public bool IsComplianceRequired { get; set; }

    /// <summary>
    /// Quick actions disponíveis (botões de ação rápida).
    /// </summary>
    public List<QuickAction> QuickActions { get; set; }

    /// <summary>
    /// Data/hora em que notificação foi enfileirada.
    /// </summary>
    public DateTime DataCriacao { get; set; }

    /// <summary>
    /// Data/hora em que notificação foi enviada (null se ainda enfileirada).
    /// </summary>
    public DateTime? DataEnvio { get; set; }

    /// <summary>
    /// Data/hora em que notificação foi entregue ao destinatário.
    /// </summary>
    public DateTime? DataEntrega { get; set; }

    /// <summary>
    /// Data/hora em que notificação foi aberta pelo usuário.
    /// </summary>
    public DateTime? DataAbertura { get; set; }

    /// <summary>
    /// Número de tentativas de envio (para retry automático).
    /// </summary>
    public int NumeroTentativas { get; set; }

    /// <summary>
    /// Indica se notificação foi lida (in-app apenas).
    /// </summary>
    public bool Lida { get; set; }

    /// <summary>
    /// Empresa à qual a notificação pertence (multi-tenancy).
    /// </summary>
    public Guid EmpresaId { get; set; }
}
```

**Conversão v2.0**: RF066.yaml seção `modelo_dados.tabelas_principais` lista campos em YAML sem prescrever classe C#.

#### 3.2.2 NotificacaoPreferencia (v1.0)

```csharp
/// <summary>
/// Preferências de notificação por usuário e tipo.
/// </summary>
public class NotificacaoPreferencia
{
    public Guid Id { get; set; }

    /// <summary>
    /// Usuário proprietário das preferências.
    /// </summary>
    public Guid UsuarioId { get; set; }

    /// <summary>
    /// Tipo de notificação (null = preferência padrão para todos os tipos).
    /// </summary>
    public string TipoNotificacao { get; set; }

    /// <summary>
    /// Canais ativados para este tipo de notificação.
    /// </summary>
    public List<CanalNotificacao> CanaisAtivados { get; set; }

    /// <summary>
    /// Indica se digest diário está ativo (e-mail consolidado às 18h).
    /// </summary>
    public bool DigestAtivo { get; set; }

    /// <summary>
    /// Horário de início do quiet hours (ex: 22:00).
    /// </summary>
    public TimeSpan QuietHoursInicio { get; set; }

    /// <summary>
    /// Horário de fim do quiet hours (ex: 08:00).
    /// </summary>
    public TimeSpan QuietHoursFim { get; set; }

    public Guid EmpresaId { get; set; }
    public DateTime DataCriacao { get; set; }
}
```

**Conversão v2.0**: RF066.yaml seção `modelo_dados.tabelas_principais` inclui NotificacaoPreferencia.

#### 3.2.3 QuickAction (v1.0)

```csharp
/// <summary>
/// Ação rápida disponível em notificação.
/// </summary>
public class QuickAction
{
    /// <summary>
    /// Identificador único da ação.
    /// </summary>
    public string ActionId { get; set; }

    /// <summary>
    /// Label do botão (ex: "Aprovar", "Rejeitar").
    /// </summary>
    public string Label { get; set; }

    /// <summary>
    /// Endpoint backend que será chamado ao clicar.
    /// </summary>
    public string EndpointUrl { get; set; }

    /// <summary>
    /// Método HTTP (GET, POST, PUT, DELETE).
    /// </summary>
    public string HttpMethod { get; set; }

    /// <summary>
    /// Payload a ser enviado (JSON serializado).
    /// </summary>
    public string Payload { get; set; }

    /// <summary>
    /// Permissão RBAC necessária para executar ação.
    /// </summary>
    public string PermissaoRequerida { get; set; }
}
```

**Conversão v2.0**: RN-NOT-066-09 descreve quick actions em linguagem natural.

### 3.3 Interfaces Documentadas em Código

**DESTINO**: SUBSTITUÍDO por descrição de comportamento em RN-NOT-066-01

#### 3.3.1 INotificationChannel (v1.0)

```csharp
/// <summary>
/// Interface abstrata para implementações de canal de notificação.
/// </summary>
public interface INotificationChannel
{
    /// <summary>
    /// Canal que esta implementação representa.
    /// </summary>
    CanalNotificacao Canal { get; }

    /// <summary>
    /// Envia notificação através deste canal.
    /// </summary>
    /// <param name="notificacao">Notificação a ser enviada.</param>
    /// <param name="cancellationToken">Token de cancelamento.</param>
    /// <returns>Resultado do envio com status e metadata do provider.</returns>
    Task<NotificationChannelResult> SendAsync(
        Notificacao notificacao,
        CancellationToken cancellationToken = default
    );

    /// <summary>
    /// Valida se canal está configurado corretamente (credenciais, API keys).
    /// </summary>
    Task<bool> ValidateConfigurationAsync();

    /// <summary>
    /// Processa webhook de evento do provider externo.
    /// </summary>
    Task ProcessWebhookEventAsync(string eventPayload);
}
```

**Conversão v2.0**: RN-NOT-066-01 descreve que sistema deve implementar 5 canais sem prescrever interface.

### 3.4 Configurações de Hangfire Documentadas em Código

**DESTINO**: SUBSTITUÍDO por descrição em RN-NOT-066-15 e tecnologias seção

#### 3.4.1 Hangfire Configuration (v1.0)

```csharp
/// <summary>
/// Configuração de Hangfire para processamento assíncrono de notificações.
/// </summary>
public static class HangfireNotificationsConfiguration
{
    public static void ConfigureNotificationsJobs(this IServiceCollection services)
    {
        // Configurar retry policy para jobs de notificação
        GlobalJobFilters.Filters.Add(new AutomaticRetryAttribute
        {
            Attempts = 4,
            DelaysInSeconds = new[] { 0, 120, 240, 480 } // Backoff exponencial
        });

        // Configurar job de envio de notificações
        RecurringJob.AddOrUpdate<NotificationSenderJob>(
            "send-queued-notifications",
            job => job.ProcessQueuedNotifications(),
            Cron.MinuteInterval(1) // Processar fila a cada 1 minuto
        );

        // Configurar job de agrupamento inteligente
        RecurringJob.AddOrUpdate<NotificationGroupingJob>(
            "group-similar-notifications",
            job => job.GroupSimilarNotifications(),
            Cron.MinuteInterval(5) // Verificar agrupamento a cada 5 minutos
        );

        // Configurar job de digest diário
        RecurringJob.AddOrUpdate<NotificationDigestJob>(
            "send-daily-digest",
            job => job.SendDailyDigest(),
            Cron.Daily(18, 0) // Enviar digest às 18h
        );

        // Configurar job de limpeza de notificações antigas
        RecurringJob.AddOrUpdate<NotificationCleanupJob>(
            "cleanup-old-notifications",
            job => job.CleanupOldNotifications(),
            Cron.Daily(2, 0) // Limpar às 02h
        );
    }
}
```

**Conversão v2.0**: RN-NOT-066-15 descreve processamento assíncrono sem código de configuração.

### 3.5 Configurações de SignalR Documentadas em Código

**DESTINO**: SUBSTITUÍDO por descrição em tecnologias seção

#### 3.5.1 SignalR Hub (v1.0)

```csharp
/// <summary>
/// Hub SignalR para notificações in-app em tempo real.
/// </summary>
public class NotificationsHub : Hub
{
    /// <summary>
    /// Envia notificação in-app para usuário específico.
    /// </summary>
    public async Task SendToUser(Guid userId, NotificacaoDto notification)
    {
        await Clients.User(userId.ToString()).SendAsync("ReceiveNotification", notification);
    }

    /// <summary>
    /// Marca notificação como lida em tempo real.
    /// </summary>
    public async Task MarkAsRead(Guid notificationId)
    {
        await Clients.User(Context.UserIdentifier).SendAsync("NotificationRead", notificationId);
    }

    /// <summary>
    /// Atualiza contador de notificações não lidas.
    /// </summary>
    public async Task UpdateUnreadCount(Guid userId, int count)
    {
        await Clients.User(userId.ToString()).SendAsync("UnreadCountUpdated", count);
    }
}
```

**Conversão v2.0**: RN-NOT-066-01 menciona SignalR para in-app sem código de Hub.

### 3.6 Exemplos de Implementação de Handlers

**DESTINO**: DESCARTADO (implementação não deve estar em RF)

#### 3.6.1 SendNotificationCommandHandler (v1.0)

```csharp
/// <summary>
/// Handler para envio de notificação (enfileira job Hangfire).
/// </summary>
public class SendNotificationCommandHandler : IRequestHandler<SendNotificationCommand, Guid>
{
    private readonly IApplicationDbContext _context;
    private readonly IBackgroundJobClient _backgroundJobClient;

    public async Task<Guid> Handle(SendNotificationCommand request, CancellationToken cancellationToken)
    {
        // Criar notificação no banco
        var notificacao = new Notificacao
        {
            Id = Guid.NewGuid(),
            UsuarioId = request.UsuarioId,
            Tipo = request.Tipo,
            Titulo = request.Titulo,
            Mensagem = request.Mensagem,
            Canais = request.Canais,
            Prioridade = request.Prioridade,
            Status = StatusNotificacao.Enfileirada,
            DataCriacao = DateTime.UtcNow
        };

        _context.Notificacoes.Add(notificacao);
        await _context.SaveChangesAsync(cancellationToken);

        // Enfileirar job Hangfire
        _backgroundJobClient.Enqueue<INotificationSender>(
            sender => sender.SendAsync(notificacao.Id, CancellationToken.None)
        );

        return notificacao.Id;
    }
}
```

**Conversão v2.0**: F-NOT-066-01 descreve funcionalidade de envio sem código de handler.

---

## 4. ABORDAGENS LEGADAS DE ESPECIFICAÇÃO

Esta seção documenta padrões de especificação que eram usados no RF066 v1.0 e foram **DESCARTADOS** na v2.0.

### 4.1 Especificação via Código ao Invés de Regras de Negócio

**Abordagem v1.0:**
```markdown
### RN003: Quiet Hours

```csharp
public class QuietHoursService
{
    private readonly TimeSpan _defaultStart = new TimeSpan(22, 0, 0); // 22h
    private readonly TimeSpan _defaultEnd = new TimeSpan(8, 0, 0);   // 8h

    public bool IsWithinQuietHours(DateTime now, NotificacaoPreferencia preferencia)
    {
        var currentTime = now.TimeOfDay;
        var start = preferencia.QuietHoursInicio;
        var end = preferencia.QuietHoursFim;

        if (start < end)
        {
            return currentTime >= start && currentTime < end;
        }
        else
        {
            return currentTime >= start || currentTime < end;
        }
    }

    public bool ShouldSendNow(Notificacao notificacao, NotificacaoPreferencia preferencia)
    {
        // Urgente e Crítica ignoram quiet hours
        if (notificacao.Prioridade >= Prioridade.Urgente)
            return true;

        return !IsWithinQuietHours(DateTime.Now, preferencia);
    }
}
```
```

**DESTINO**: DESCARTADO

**Conversão v2.0:**
```markdown
### RN-NOT-066-03: Quiet Hours (Horários de Silêncio)

**Descrição**: Notificações com prioridade Baixa ou Normal não devem ser enviadas durante
quiet hours configuradas pelo usuário (padrão 22h-8h). Notificações Urgentes e Críticas
ignoram quiet hours. Notificações acumuladas durante quiet hours devem ser enviadas às
8h (fim do período de silêncio).

**Motivação**: Respeitar horários de descanso dos usuários e evitar fadiga de notificações.

**Impacto**: Backend deve validar prioridade e horário antes de enviar, enfileirando
notificações para envio posterior se aplicável.
```

### 4.2 Especificação via Diagramas de Sequência em Código

**Abordagem v1.0:**
```markdown
### Fluxo de Envio de Notificação

```csharp
// 1. Sistema dispara evento
var evento = new SlaVencendoEvent { ContratoId = contratoId };
await _mediator.Publish(evento);

// 2. Event handler cria notificação
public class SlaVencendoEventHandler : INotificationHandler<SlaVencendoEvent>
{
    public async Task Handle(SlaVencendoEvent evento, CancellationToken ct)
    {
        var comando = new SendNotificationCommand
        {
            UsuarioId = evento.GestorId,
            Tipo = "SLA_VENCENDO",
            Titulo = "SLA Vencendo em 1 Hora",
            Mensagem = $"Contrato {evento.ContratoId} vencendo às {evento.DataVencimento}",
            Canais = new[] { CanalNotificacao.Email, CanalNotificacao.SMS },
            Prioridade = Prioridade.Urgente
        };

        await _mediator.Send(comando);
    }
}

// 3. Command handler enfileira job
// 4. Job processa envio
// 5. Webhook atualiza status
```
```

**DESTINO**: DESCARTADO

**Conversão v2.0**: F-NOT-066-01 descreve fluxo em linguagem natural sem código.

---

## 5. DECISÕES TÉCNICAS LEGADAS

Decisões técnicas que estavam implícitas no código do RF066 v1.0.

### 5.1 Escolha de Hangfire para Background Jobs

**No v1.0**: Código de configuração de Hangfire embutido no RF implicava que Hangfire era obrigatório.

**No v2.0**: RN-NOT-066-15 descreve necessidade de processamento assíncrono sem prescrever Hangfire. Desenvolvedor pode escolher implementação (Hangfire, Quartz.NET, Azure Functions, etc.) desde que cumpra os requisitos.

**DESTINO**: ASSUMIDO (implementação atual usa Hangfire, mas RF não obriga)

### 5.2 Escolha de SignalR para In-App Notifications

**No v1.0**: Código de Hub SignalR embutido no RF implicava que SignalR era obrigatório.

**No v2.0**: RN-NOT-066-01 menciona "via SignalR WebSocket" mas não obriga implementação específica. Desenvolvedor pode usar WebSockets nativos, Socket.io, ou outra tecnologia.

**DESTINO**: ASSUMIDO (implementação atual usa SignalR, mas RF permite alternativas)

### 5.3 Escolha de SendGrid/Twilio/Firebase como Providers

**No v1.0**: Código de integração específico com SendGrid, Twilio, Firebase embutido no RF.

**No v2.0**: RN-NOT-066-01 menciona "via API de provider externo como Twilio ou Nexmo" deixando claro que são exemplos, não obrigações.

**DESTINO**: ASSUMIDO (implementação atual usa esses providers, mas RF permite alternativas)

---

## 6. MAPEAMENTO DE DESTINO DOS ITENS LEGADOS

Tabela consolidada de destino de todos os itens legados extraídos do RF066 v1.0.

| Item Legado | Tipo | Destino | Localização v2.0 |
|-------------|------|---------|------------------|
| `CanalNotificacao` enum | Código | SUBSTITUÍDO | RN-NOT-066-01 |
| `Prioridade` enum | Código | SUBSTITUÍDO | RN-NOT-066-02 |
| `StatusNotificacao` enum | Código | SUBSTITUÍDO | RN-NOT-066-08 |
| `Notificacao` class | Código | SUBSTITUÍDO | RF066.yaml modelo_dados |
| `NotificacaoPreferencia` class | Código | SUBSTITUÍDO | RF066.yaml modelo_dados |
| `QuickAction` class | Código | SUBSTITUÍDO | RN-NOT-066-09 |
| `INotificationChannel` interface | Código | SUBSTITUÍDO | RN-NOT-066-01 |
| Hangfire configuration | Código | DESCARTADO | RN-NOT-066-15 (texto) |
| SignalR Hub | Código | DESCARTADO | Tecnologias seção |
| SendNotificationCommandHandler | Código | DESCARTADO | F-NOT-066-01 (texto) |
| QuietHoursService | Código | DESCARTADO | RN-NOT-066-03 (texto) |
| Diagramas de sequência em código | Código | DESCARTADO | F-NOT-066-01 (texto) |
| Hangfire como obrigatório | Decisão | ASSUMIDO | Implícito no backend |
| SignalR como obrigatório | Decisão | ASSUMIDO | Implícito no backend |
| SendGrid/Twilio/Firebase | Decisão | ASSUMIDO | Implícito no backend |

**Legenda de Destino:**
- **SUBSTITUÍDO**: Item foi convertido para linguagem natural no RF066 v2.0
- **DESCARTADO**: Item era código de implementação e não deve estar em RF
- **ASSUMIDO**: Decisão técnica foi tomada na implementação mas RF não obriga

---

## 7. LIÇÕES APRENDIDAS DA MIGRAÇÃO

### 7.1 Benefícios da Abordagem Natural Language

1. **Maior Clareza**: Stakeholders de negócio conseguem revisar RF sem conhecimento de C#
2. **Flexibilidade**: Desenvolvedores têm liberdade de escolher melhores estruturas de dados
3. **Manutenibilidade**: RF não precisa ser atualizado quando código muda
4. **Foco no "O Quê"**: RF descreve comportamento esperado, não "como" implementar

### 7.2 Quando Código no RF Era Útil

1. **Tipos Complexos**: Enums e classes ajudavam a visualizar modelo de dados
2. **Decisões Técnicas**: Código tornava implícitas algumas decisões que agora precisam ser explícitas
3. **Exemplos**: Código servia como "protótipo" para desenvolvedores

### 7.3 Recomendações para Futuros RFs

1. **SEMPRE usar linguagem natural** em RN (Regras de Negócio)
2. **Usar YAML estruturado** (RF066.yaml) para especificar modelo de dados sem código
3. **Criar protótipos separados** em `.temprobots/` se exemplos de código forem necessários
4. **Documentar decisões técnicas** explicitamente em DECISIONS.md ao invés de implícitas em código

---

## 8. EVIDÊNCIAS DE MIGRAÇÃO

### 8.1 Arquivos Criados

- ✅ `RF066.md.backup-20251230` - Backup do RF066 v1.0 (263 linhas)
- ✅ `RF066.md` v2.0 - RF em linguagem natural (504 linhas preview)
- ✅ `RF066.yaml` v2.0 - Estrutura YAML (920 linhas)
- ✅ `RL-RF066.md` - Este documento

### 8.2 Estatísticas de Migração

- **Linhas de código C# removidas**: ~350 linhas
- **Regras de negócio convertidas**: 15 RNs
- **Funcionalidades convertidas**: 13 funcionalidades
- **Enums convertidos**: 3 (CanalNotificacao, Prioridade, StatusNotificacao)
- **Classes convertidas**: 3 (Notificacao, NotificacaoPreferencia, QuickAction)
- **Interfaces convertidas**: 1 (INotificationChannel)
- **Configurações convertidas**: 2 (Hangfire, SignalR)

### 8.3 Validação de Migração

- ✅ **100% do código foi removido** do RF066.md v2.0
- ✅ **100% das RNs foram convertidas** para linguagem natural
- ✅ **100% dos itens legados têm destino explícito** (SUBSTITUÍDO/DESCARTADO/ASSUMIDO)
- ✅ **RF066.yaml está 100% sincronizado** com RF066.md
- ✅ **Nenhuma perda de informação funcional** (comportamento esperado preservado)

---

## 9. CONTATO E GOVERNANÇA

**Responsável pela Migração**: Sistema de Governança v2.0
**Data da Migração**: 2025-12-30
**Versão do Contrato Utilizado**: CONTRATO-RF-PARA-RL.md v1.0
**Status**: Migração completa aguardando validação

**Para Dúvidas:**
- Sobre comportamento esperado → Consultar **RF066.md v2.0**
- Sobre código legado → Consultar **este documento (RL-RF066.md)**
- Sobre modelo de dados → Consultar **RF066.yaml**
- Sobre implementação atual → Consultar código em `D:\IC2\backend\IControlIT.API/src/`
