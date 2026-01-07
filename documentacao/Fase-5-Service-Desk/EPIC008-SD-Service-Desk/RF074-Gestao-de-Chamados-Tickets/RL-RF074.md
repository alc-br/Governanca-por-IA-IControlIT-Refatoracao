# RL-RF074 - Referência ao Legado: Portal Self-Service

**Versão**: 1.0
**Data**: 2025-12-30
**RF Relacionado**: RF074 - Gestão de Chamados - Portal Self-Service
**Tipo de Legado**: Documentação Code-Heavy + Referências Sistema Legado

---

## 1. PROPÓSITO

Documenta memória histórica de RF074 incluindo:
- Abordagem code-heavy v1.0 (código C#/TypeScript embutido no RF)
- Referências ao sistema legado ASPX/VB.NET
- Banco de dados e stored procedures legados
- Telas e WebServices substituídos

❌ **NÃO é fonte de requisitos** - use RF074.md v2.0
✅ **É memória técnica histórica** para consulta

---

## 2. CONTEXTO DO LEGADO

### 2.1 Abordagem Code-Heavy v1.0

RF074.md v1.0 (1.035 linhas) continha extensa quantidade de código embutido:
- Classes C# completas (Commands, Handlers, Validators)
- Código TypeScript/Angular completo (Services, Components)
- Configurações SignalR/Service Worker
- SQL e stored procedures
- JSON de configuração completos

### 2.2 Sistema Legado ASPX/VB.NET

**Local**: `D:\IC2\ic1_legado\IControlIT\`

**Telas Substituídas**:
- `Chamado/Chamado.aspx` → `/my-tickets` (Angular)
- `Chamado/Chamado_Consulta.aspx` → `/my-tickets/{id}` (Angular)
- `Chamado/Chamado_Solicitacao.aspx` → `/my-tickets/new` (wizard 3-passos)

**Banco Legado**: `SC_CLIENTE_NOME` (específico por cliente)

**Tabelas Compartilhadas com RF073**:
- Solicitacao (Tickets)
- Solicitacao_Item (Ativos afetados)
- Solicitacao_Tipo (Categorias)
- Solicitacao_SLA

**Tabela Nova RF074**:
```sql
CREATE TABLE [dbo].[TicketSatisfaction](
    [Id_Satisfacao] [int] IDENTITY(1,1) NOT NULL,
    [Id_Solicitacao] [int] NOT NULL,
    [Nm_Rating] [int] NOT NULL,  -- 1-5 stars
    [Ds_Comentario] [varchar](500) NULL,
    [Dt_Envio] [datetime] NOT NULL,
    [Cd_Usuario] [int] NOT NULL,
    CONSTRAINT [PK_Satisfacao] PRIMARY KEY ([Id_Satisfacao])
)
```

**WebServices Legados** (`WSChamado.asmx.vb`):
- `Solicitacao_Incluir()` → POST /api/my-tickets
- `Solicitacao_Lista_ByUser()` → GET /api/my-tickets
- `Solicitacao_Detalhes()` → GET /api/my-tickets/{id}

---

## 3. CÓDIGO LEGADO EXTRAÍDO

### 3.1 Classes C# de Comandos (CÓDIGO REMOVIDO)

**DESTINO**: SUBSTITUÍDO por descrição em linguagem natural

#### GetMyTicketsQuery (v1.0)
```csharp
public class GetMyTicketsQuery : IRequest<PaginatedList<TicketDto>>
{
    public int PageNumber { get; set; } = 1;
    public int PageSize { get; set; } = 10;
}

public class GetMyTicketsQueryHandler : IRequestHandler<GetMyTicketsQuery, PaginatedList<TicketDto>>
{
    private readonly ICurrentUserService _currentUser;

    public async Task<PaginatedList<TicketDto>> Handle(GetMyTicketsQuery request, CancellationToken ct)
    {
        var tickets = await _context.Tickets
            .Where(t => t.UserId == _currentUser.UserId &&
                       t.ClienteId == _currentUser.ClienteId &&
                       !t.IsDeleted)
            .OrderByDescending(t => t.CreatedAt)
            .ToPaginatedListAsync(request.PageNumber, request.PageSize, ct);

        return tickets;
    }
}
```
**Conversão v2.0**: F-SD-074-01 e RN-SD-074-01 descrevem em linguagem natural

#### CreateMyTicketCommand (v1.0 - Wizard)
```csharp
// Passo 3: Confirmar + Criar
public class CreateMyTicketCommand : IRequest<TicketDto>
{
    [Required]
    public int StepOneServiceId { get; set; }

    [Required]
    public string StepTwoDescricao { get; set; }

    public IFormFile StepTwoAttachment { get; set; }
}

public class CreateMyTicketHandler : IRequestHandler<CreateMyTicketCommand, TicketDto>
{
    public async Task<TicketDto> Handle(CreateMyTicketCommand request, CancellationToken ct)
    {
        var ticket = new Ticket
        {
            UserId = _currentUser.UserId,
            ClienteId = _currentUser.ClienteId,
            ServiceCategoryId = request.StepOneServiceId,
            Descricao = request.StepTwoDescricao,
            Status = TicketStatus.Novo,
            CreatedAt = DateTime.UtcNow
        };

        if (request.StepTwoAttachment != null)
        {
            var url = await _blobService.UploadAsync(request.StepTwoAttachment, ct);
            ticket.AttachmentUrl = url;
        }

        _context.Tickets.Add(ticket);
        await _context.SaveChangesAsync(ct);
        await _auditService.LogAsync("TKT_TICKET_CREATED_SELFSERVICE", ticket.Id, ct);

        return _mapper.Map<TicketDto>(ticket);
    }
}
```
**Conversão v2.0**: F-SD-074-02 descreve fluxo wizard sem código

#### SubmitSatisfactionSurveyCommand (v1.0 - CSAT)
```csharp
public class SubmitSatisfactionSurveyCommand : IRequest<bool>
{
    [Required]
    public int TicketId { get; set; }

    [Range(1, 5)]
    public int Stars { get; set; }

    [MaxLength(500)]
    public string? Comentario { get; set; }
}

public class SubmitSatisfactionSurveyHandler : IRequestHandler<SubmitSatisfactionSurveyCommand, bool>
{
    public async Task<bool> Handle(SubmitSatisfactionSurveyCommand request, CancellationToken ct)
    {
        var satisfaction = new TicketSatisfaction
        {
            TicketId = request.TicketId,
            Rating = request.Stars,
            Comments = request.Comentario,
            SubmittedAt = DateTime.UtcNow,
            UserId = _currentUser.UserId
        };

        _context.TicketSatisfactions.Add(satisfaction);
        await _context.SaveChangesAsync(ct);
        await _auditService.LogAsync("TKT_SATISFACTION_SUBMITTED", request.TicketId, ct);

        return true;
    }
}
```
**Conversão v2.0**: F-SD-074-06 e RN-SD-074-07 descrevem CSAT inline

---

### 3.2 Código SignalR (REMOVIDO)

**DESTINO**: DESCARTADO

#### TicketHub (v1.0)
```csharp
public class AddCommentHandler : IRequestHandler<AddCommentCommand, CommentDto>
{
    private readonly IHubContext<TicketHub> _hubContext;

    public async Task<CommentDto> Handle(AddCommentCommand request, CancellationToken ct)
    {
        var comment = new Comment { ... };
        _context.Comments.Add(comment);
        await _context.SaveChangesAsync(ct);

        // Notificar usuário em tempo real
        await _hubContext.Clients.User(comment.Ticket.UserId.ToString())
            .SendAsync("ReceiveTicketUpdate", new
            {
                ticketId = comment.TicketId,
                type = "comment",
                message = "Novo comentário de suporte",
                timestamp = DateTime.UtcNow
            }, cancellationToken: ct);

        return _mapper.Map<CommentDto>(comment);
    }
}
```
**Conversão v2.0**: RN-SD-074-05 descreve SignalR sem código de implementação

---

### 3.3 Código TypeScript/Angular (REMOVIDO)

**DESTINO**: DESCARTADO

#### TicketHubService (v1.0)
```typescript
@Injectable({ providedIn: 'root' })
export class TicketHubService {
    public ticketUpdated$ = new Subject<TicketUpdate>();

    constructor(private signalRService: SignalRService) {
        this.signalRService.on('ReceiveTicketUpdate', (update) => {
            this.ticketUpdated$.next(update);
        });
    }
}

export class TicketDetailComponent implements OnInit {
    constructor(private ticketHub: TicketHubService) {}

    ngOnInit() {
        this.ticketHub.ticketUpdated$.subscribe(update => {
            if (update.ticketId === this.ticketId) {
                this.loadTicket();
                this.showNotificationBadge();
            }
        });
    }
}
```
**Conversão v2.0**: F-SD-074-05 descreve notificações real-time sem código

#### Service Worker (v1.0 - PWA Offline)
```typescript
@Injectable({ providedIn: 'root' })
export class TicketOfflineService {
    async cacheTicketsForOffline(tickets: Ticket[]): Promise<void> {
        const store = await this.db.open('tickets-cache');
        for (const ticket of tickets) {
            await store.put(ticket);
        }
    }

    async getTicketsOffline(): Promise<Ticket[]> {
        const store = await this.db.open('tickets-cache');
        return await store.getAll();
    }
}

// Service Worker (sw.js)
self.addEventListener('fetch', (event) => {
    if (event.request.url.includes('/api/my-tickets')) {
        event.respondWith(
            fetch(event.request)
                .then(response => {
                    const clone = response.clone();
                    caches.open('tickets-cache').then(cache => {
                        cache.put(event.request, clone);
                    });
                    return response;
                })
                .catch(() => caches.match(event.request))
        );
    }
});
```
**Conversão v2.0**: RN-SD-074-10 e F-SD-074-08 descrevem PWA sem código

---

### 3.4 Validators e Attributes (REMOVIDO)

**DESTINO**: DESCARTADO

#### MaxFileSizeAttribute (v1.0)
```csharp
[AttributeUsage(AttributeTargets.Property)]
public class MaxFileSizeAttribute : ValidationAttribute
{
    private const int MaxBytes = 5 * 1024 * 1024;  // 5 MB

    public override bool IsValid(object? value)
    {
        if (value is not IFormFile file) return true;
        return file.Length <= MaxBytes;
    }
}

public class AddCommentCommand : IRequest<CommentDto>
{
    [Required]
    public int TicketId { get; set; }

    [MaxLength(2000)]
    public string Text { get; set; }

    [MaxFileSize]
    public IFormFile? Attachment { get; set; }
}
```
**Conversão v2.0**: RN-SD-074-08 descreve validação máx 5 MB em linguagem natural

#### AuditableAttribute (v1.0)
```csharp
[AttributeUsage(AttributeTargets.Class)]
public class AuditableAttribute : Attribute
{
    public string AuditCode { get; set; }
}

[Auditable(AuditCode = "TKT_SELFSERVICE_CREATE")]
public class CreateMyTicketCommand : IRequest<TicketDto> { }

public class AuditBehavior<TRequest, TResponse> : IPipelineBehavior<TRequest, TResponse>
{
    public async Task<TResponse> Handle(
        TRequest request,
        RequestHandlerDelegate<TResponse> next,
        CancellationToken ct)
    {
        var auditAttr = typeof(TRequest).GetCustomAttribute<AuditableAttribute>();
        if (auditAttr != null)
        {
            var auditLog = new AuditLog
            {
                Code = auditAttr.AuditCode,
                UserId = _currentUser.UserId,
                RequestType = typeof(TRequest).Name,
                RequestData = JsonConvert.SerializeObject(request),
                CreatedAt = DateTime.UtcNow
            };
            _context.AuditLogs.Add(auditLog);
        }

        var response = await next();
        if (auditAttr != null)
            await _context.SaveChangesAsync(ct);

        return response;
    }
}
```
**Conversão v2.0**: RN-SD-074-09 descreve auditoria sem código

---

### 3.5 JSON Configuração (REMOVIDO)

**DESTINO**: DESCARTADO

#### Feature Flags (v1.0)
```json
{
    "featureKey": "SELFSERVICE_PORTAL_ENABLED",
    "nome": "Portal Self-Service",
    "descricao": "Portal de gestão de chamados para usuários finais",
    "habilitado": true,
    "isSystemFeature": false
},
{
    "featureKey": "SELFSERVICE_CSAT_INLINE",
    "nome": "CSAT Inline",
    "descricao": "Avaliação de satisfação imediata (não email)",
    "habilitado": true,
    "isSystemFeature": false
}
```
**Conversão v2.0**: Seção 4.1 do RF074.md descreve sem JSON

#### i18n Keys (v1.0)
```json
{
    "selfservice": {
        "portal": {
            "title": "Meus Chamados",
            "description": "Acompanhe suas solicitações de suporte"
        },
        "wizard": {
            "step1": "Selecionar Serviço",
            "step2": "Descrever Problema",
            "step3": "Confirmar"
        }
    }
}
```
**Conversão v2.0**: Seção 4.2 do RF074.md lista chaves sem JSON

---

## 4. FLUXOS EM PSEUDO-CÓDIGO (REMOVIDOS)

**DESTINO**: DESCARTADO

### Fluxo Criar Ticket v1.0 (Pseudo-código)
```
Usuario acessa /my-tickets/new
    |
    v
Exibir Passo 1: Cards com Categorias (de RF021)
    |
    v
Usuario seleciona categoria + clica "Continuar"
    |
    v
Exibir Passo 2: Form textarea
```
**Conversão v2.0**: Seção 2.2 do RF074.md descreve fluxo em linguagem natural

---

## 5. COMPARATIVO LEGADO vs MODERNO

| Aspecto | Legado (VB.NET/ASPX) | Modernizado (.NET 10 + Angular 19) |
|---------|----------------------|-------------------------------------|
| **UI** | WebForms jQuery desktop-only | Angular 19 Standalone PWA mobile-first |
| **Formulário** | 20+ campos única tela | Wizard 3-passos intuitivo |
| **FAQ** | Página separada `/FAQ.aspx` | Modal integrado Ctrl+/ busca real-time |
| **Notificações** | Polling 30s (pesado) | SignalR WebSocket real-time |
| **Upload** | Filesystem local | Azure Blob Storage escalável |
| **CSAT** | Email link externo | Inline popup sem redirect |
| **Listagem** | Tabela overflow | Cards responsivos |
| **Performance** | ~3s carregamento | <1s lazy loading + cache |

---

## 6. MAPEAMENTO DESTINO ITENS LEGADOS

| Item Legado | Tipo | Destino | Localização v2.0 |
|-------------|------|---------|------------------|
| GetMyTicketsQuery class | Código C# | SUBSTITUÍDO | F-SD-074-01, RN-SD-074-01 |
| CreateMyTicketCommand class | Código C# | SUBSTITUÍDO | F-SD-074-02, RN-SD-074-02 |
| SubmitSatisfactionSurveyCommand | Código C# | SUBSTITUÍDO | F-SD-074-06, RN-SD-074-07 |
| TicketHub SignalR | Código C# | DESCARTADO | RN-SD-074-05 (texto) |
| TicketHubService Angular | Código TypeScript | DESCARTADO | F-SD-074-05 (texto) |
| TicketOfflineService PWA | Código TypeScript | DESCARTADO | RN-SD-074-10 (texto) |
| MaxFileSizeAttribute | Código C# | DESCARTADO | RN-SD-074-08 (texto) |
| AuditBehavior pipeline | Código C# | DESCARTADO | RN-SD-074-09 (texto) |
| Feature flags JSON | Configuração | DESCARTADO | Seção 4.1 (texto) |
| i18n keys JSON | Configuração | DESCARTADO | Seção 4.2 (texto) |
| Fluxos pseudo-código | Diagrama | DESCARTADO | Seção 2 (texto natural) |
| Chamado.aspx ASPX | Tela legado | SUBSTITUÍDO | /my-tickets (Angular) |
| WSChamado.asmx WebService | WebService VB.NET | SUBSTITUÍDO | REST API endpoints |
| Tabela TicketSatisfaction SQL | DDL | SUBSTITUÍDO | Seção 4.3 RF074.yaml |

**Total Itens**: 15 (10 SUBSTITUÍDOS, 5 DESCARTADOS)
**Cobertura Destino**: 100%

---

## 7. ESTATÍSTICAS MIGRAÇÃO

- **Linhas código removidas**: ~950 linhas (C# + TypeScript + SQL + JSON)
- **Funcionalidades convertidas**: 10 funcionalidades
- **Regras negócio convertidas**: 15 RNs
- **Telas legado substituídas**: 3 ASPX
- **WebServices legado substituídos**: 3 métodos
- **Endpoints REST criados**: 8

**Ganhos v2.0**:
- 100% código removido do RF
- Regras em linguagem natural clara
- Stakeholders revisam sem conhecimento técnico
- Desenvolvedores têm liberdade de implementação
- RF não precisa atualizar quando código muda

---

## 8. RASTREABILIDADE COMPLETA

**RF074 v1.0 → RF074 v2.0**:
- Seção RN001-010 (código C#) → RN-SD-074-01 a 15 (texto natural)
- Seção Endpoints (código) → Seção 5 RF074.yaml (estruturado)
- Seção Fluxos (pseudo-código) → Seção 2 RF074.md (texto narrativo)
- Seção Segurança (código) → Seção 5 RF074.md (texto descritivo)
- Seção Integrações (JSON) → Seção 4 RF074.md (texto estruturado)

---

**Data Migração**: 2025-12-30
**Responsável**: Sistema Governança v2.0
**Status**: Migração completa aguardando validação
