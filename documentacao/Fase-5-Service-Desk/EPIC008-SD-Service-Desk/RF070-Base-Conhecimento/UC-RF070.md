# UC-RF070 - Casos de Uso - Base de Conhecimento

## UC01: Listar e Buscar Artigos com ElasticSearch Full-Text

### 1. Descrição

Este caso de uso permite que usuários autenticados (analistas, gestores, usuários finais) busquem artigos da base de conhecimento usando motor de busca full-text ElasticSearch com ranking inteligente multi-critério (relevância TF-IDF 40%, score de utilidade 25%, popularidade 20%, atualidade 15%), filtros facetados (categoria, data, autor, tags), correção ortográfica automática (did you mean?), highlighting de termos buscados e paginação server-side. O sistema retorna resultados ordenados por score composto, exibe resumo com highlights e permite drill-down por categorias hierárquicas.

### 2. Atores

- Usuário autenticado (Analista Service Desk, Gestor Conhecimento, Usuário Final)
- Sistema (Backend .NET 10, ElasticSearch, Redis Cache)

### 3. Pré-condições

- Usuário autenticado no sistema
- Permissão: `service-desk:base-conhecimento:ler`
- Multi-tenancy ativo (ClienteId válido)
- ElasticSearch indexado e online
- Feature flag `SERVICE_DESK_BASE_CONHECIMENTO` habilitada

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa rota `/base-conhecimento` | - |
| 2 | - | Frontend verifica feature flag `SERVICE_DESK_BASE_CONHECIMENTO` → Se desabilitada: redireciona para 404 |
| 3 | - | Frontend renderiza tela com campo de busca, filtros (categoria, data, autor), lista de categorias hierárquicas (tree view) |
| 4 | Digita termo de busca "vpn cisco timeout" no campo de busca | - |
| 5 | - | Frontend envia `GET /api/base-conhecimento/artigos?q=vpn+cisco+timeout&page=1&size=20&clienteId={clienteId}` |
| 6 | - | Backend valida permissão RBAC: `User.HasPermission("service-desk:base-conhecimento:ler")` → Se negado: HTTP 403 |
| 7 | - | Backend valida multi-tenancy: `artigos.Where(a => a.ClienteId == request.ClienteId)` |
| 8 | - | **ElasticSearch Query**: Backend executa `BuscarArtigosHandler` que invoca ElasticSearch com `MultiMatch` query sobre campos `Titulo` (boost 3.0), `Resumo` (boost 2.0), `Problema` (boost 1.5), `Solucao` (boost 1.0), `Tags` (boost 2.5) |
| 9 | - | ElasticSearch aplica Fuzziness.Auto (tolera erros ortográficos: "vpnn" → "vpn") |
| 10 | - | **ScriptScore Customizado**: ElasticSearch executa script painless que calcula score composto: `relevancia * 0.40 + utilidade * 0.25 + log10(popularidade+1)/5 * 0.20 + atualidade * 0.15` |
| 11 | - | ElasticSearch retorna documentos ordenados por score, com highlighting `<mark>vpn</mark>`, `<mark>cisco</mark>`, `<mark>timeout</mark>` |
| 12 | - | Backend mapeia resultados para `ArtigoSearchDto` com Id, Titulo, Resumo, ScoreUtilidade, TotalAcessos, DataPublicacao, Highlights |
| 13 | - | Backend retorna JSON com 20 artigos (page 1), total de resultados (ex: 147), paginação (hasNext, hasPrevious) |
| 14 | - | Frontend renderiza lista de artigos com resumo + highlights, score de utilidade (barra de progresso), total de acessos (ícone 👁️) |
| 15 | Clica em artigo "Como resolver timeout VPN Cisco AnyConnect" | - |
| 16 | - | Frontend navega para `/base-conhecimento/artigos/{id}` (UC04 - Visualizar Artigo) |

### 5. Fluxos Alternativos

**FA01: Nenhum Resultado Encontrado - Sugestão Ortográfica**

- No passo 11, ElasticSearch não encontra documentos (0 hits)
- Backend invoca `_elasticSearch.SuggestAsync("vpnn cysco")` (método Term Suggester)
- ElasticSearch analisa termos e retorna sugestão: `{ "vpnn" → "vpn", "cysco" → "cisco" }`
- Backend retorna HTTP 400 com body: `{ "error": "KB_SEM_RESULTADOS", "message": "Nenhum resultado encontrado. Você quis dizer 'vpn cisco'?", "suggestion": "vpn cisco" }`
- Frontend exibe mensagem com link clicável "Você quis dizer 'vpn cisco'?" → Ao clicar, reexecuta busca com termo corrigido

**FA02: Filtro por Categoria Aplicado**

- No passo 5, usuário seleciona categoria "Redes > VPN" no filtro lateral (tree view)
- Frontend envia `GET /api/base-conhecimento/artigos?q=timeout&categoriaId=42&page=1&size=20`
- Backend adiciona filtro ao ElasticSearch query: `.Filter(f => f.Term(t => t.Field(a => a.CategoriaIds).Value(42)))`
- ElasticSearch retorna apenas artigos da categoria 42 e suas subcategorias
- Frontend exibe breadcrumb: "Categorias > Redes > VPN (23 artigos)"

**FA03: Exportação de Resultados para PDF**

- No passo 14, usuário clica em botão "Exportar resultados (PDF)"
- Frontend envia `POST /api/base-conhecimento/artigos/exportar` com body: `{ "query": "vpn cisco", "formato": "PDF", "artigoIds": [12, 45, 78, ...] }`
- Backend gera PDF com QuestPDF contendo lista de artigos (titulo, resumo, score, total acessos)
- Backend retorna stream de bytes com Content-Type: `application/pdf`, Content-Disposition: `attachment; filename="artigos-vpn-cisco-2025-12-28.pdf"`
- Frontend dispara download automático do arquivo

**FA04: Cache Redis Hit (Busca Recente)**

- No passo 8, antes de invocar ElasticSearch, backend verifica Redis cache: `_cache.GetStringAsync($"kb_search_{clienteId}_{queryHash}")`
- Se cache hit (TTL 5min): Backend desserializa JSON do cache e retorna diretamente (bypassa ElasticSearch)
- Frontend recebe resposta <50ms (vs 200ms sem cache)
- Backend registra métrica: `CacheHitRate` para monitoramento

### 6. Exceções

**EX01: Usuário Sem Permissão de Leitura**

- No passo 6, backend valida permissão e detecta que usuário não tem `service-desk:base-conhecimento:ler`
- Backend retorna HTTP 403 com body: `{ "error": "FORBIDDEN", "message": "Você não tem permissão para acessar a Base de Conhecimento" }`
- Frontend exibe toast de erro: "Acesso negado - Contate o administrador"

**EX02: ElasticSearch Offline/Timeout**

- No passo 8, backend tenta conectar ao ElasticSearch mas serviço está indisponível ou timeout (>5s)
- Backend captura exceção `ElasticsearchClientException` ou `OperationCanceledException`
- Backend faz **fallback para SQL Server**: Executa query LIKE '%termo%' com ranking básico (apenas por Total_Acessos DESC)
- Backend registra log WARNING: "ElasticSearch indisponível, usando fallback SQL"
- Frontend recebe resultados (mais lentos, sem score composto) mas funcionalidade não quebra
- Backend dispara alerta para DevOps via Application Insights

**EX03: Termo de Busca Muito Curto**

- No passo 5, usuário digita apenas "vp" (2 caracteres)
- Backend valida tamanho mínimo: `if (request.TermoBusca.Length < 3)`
- Backend retorna HTTP 400 com body: `{ "error": "KB_TERMO_MUITO_CURTO", "message": "Digite pelo menos 3 caracteres para buscar" }`
- Frontend exibe mensagem de validação abaixo do campo de busca

**EX04: Multi-Tenancy Violation (Tentativa de Acesso Cross-Tenant)**

- No passo 7, usuário com ClienteId=10 tenta acessar artigos com `?clienteId=20` manipulando URL
- Backend detecta divergência: `request.ClienteId != User.GetClienteId()`
- Backend retorna HTTP 403 com body: `{ "error": "MULTI_TENANCY_VIOLATION", "message": "Você não pode acessar artigos de outro cliente" }`
- Backend registra evento de auditoria de segurança: `SecurityEventType.MultiTenancyViolationAttempt`

### 7. Pós-condições

- Resultados de busca retornados e exibidos ao usuário
- Cache Redis atualizado com resultados (se aplicável)
- Métricas de busca registradas (termo buscado, total de resultados, tempo de resposta)
- Nenhuma alteração de estado no banco de dados (operação read-only)

### 8. Regras de Negócio Aplicáveis

- **RN-KB-070-07**: Busca Full-Text com Ranking Inteligente (TF-IDF 40%, Utilidade 25%, Popularidade 20%, Atualidade 15%)
- **RN-KB-070-01**: Titulo Unico por Categoria (validado ao criar artigo, não afeta busca)
- **RN-KB-070-11**: Auditoria Completa de Acessos (triggada ao visualizar artigo no UC04, não nesta busca)

---

## UC02: Criar Artigo com Editor WYSIWYG e Workflow de Aprovação

### 1. Descrição

Este caso de uso permite que usuários com permissão (Analista Sênior, Especialista Técnico, Gestor de Conhecimento) criem novos artigos de conhecimento utilizando editor rico WYSIWYG (Quill.js) com suporte a formatação avançada, imagens inline (upload para Azure Blob), syntax highlighting para código, anexos múltiplos (até 500MB), seleção de 1-5 categorias hierárquicas, tags automáticas via NLP (Azure Cognitive Services), workflow de aprovação automático para artigos críticos (2 níveis: Revisor Técnico + Gestor), validação de conteúdo mínimo (titulo 10-200 chars, resumo 50-500 chars, problema ≥100 chars, solução ≥200 chars) e versionamento inicial (v1.0).

### 2. Atores

- Usuário autenticado (Analista Sênior, Especialista Técnico, Gestor de Conhecimento)
- Sistema (Backend .NET 10, Azure Cognitive Services, Azure Blob Storage, Hangfire)

### 3. Pré-condições

- Usuário autenticado no sistema
- Permissão: `service-desk:base-conhecimento:criar`
- Multi-tenancy ativo (ClienteId válido)
- Feature flag `SERVICE_DESK_BASE_CONHECIMENTO` habilitada
- Azure Cognitive Services disponível (para tags automáticas)
- Azure Blob Storage configurado (para anexos)

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa rota `/base-conhecimento/artigos/novo` | - |
| 2 | - | Frontend valida permissão local (token JWT): `hasPermission('service-desk:base-conhecimento:criar')` → Se negado: redireciona para lista |
| 3 | - | Frontend carrega componente `ArtigoFormComponent` com editor Quill.js configurado (toolbar: bold, italic, heading, list, code-block, image, link) |
| 4 | - | Frontend carrega categorias hierárquicas via `GET /api/base-conhecimento/categorias?clienteId={clienteId}` → Renderiza TreeSelect com 3 níveis (ex: TI > Redes > VPN) |
| 5 | Preenche formulário: Titulo "Como resolver erro 0x80070005 ao instalar Windows Update", Resumo "Erro de permissão ao executar Windows Update", Criticidade "Normal" | - |
| 6 | No editor Quill, escreve seção "Problema": "Usuario recebe mensagem 'Erro 0x80070005 - Acesso Negado' ao tentar..." (250 chars) | - |
| 7 | No editor Quill, escreve seção "Solução" com passos numerados, código CMD destacado: "1. Abrir CMD como Admin\n2. Executar: `net stop wuauserv`\n3. ..." (600 chars) | - |
| 8 | Clica em botão "Inserir Imagem" do Quill → Frontend abre dialog de upload | - |
| 9 | Seleciona arquivo `erro-screenshot.png` (2.3MB) | - |
| 10 | - | Frontend envia `POST /api/base-conhecimento/artigos/upload-imagem` com FormData multipart |
| 11 | - | Backend valida: tamanho ≤50MB, tipo MIME `image/png|jpeg|gif`, filename sanitizado (sem caracteres especiais) |
| 12 | - | Backend faz upload para Azure Blob Storage: container `kb-images`, path `{clienteId}/{artigoId-temp}/{filename}` |
| 13 | - | Backend retorna URL pública da CDN: `https://cdn.icontrolit.com/kb-images/10/temp-abc123/erro-screenshot.png` |
| 14 | - | Frontend insere tag `<img src="https://cdn..." />` no editor Quill na posição do cursor |
| 15 | Seleciona 3 categorias: "Windows > Atualizações", "Troubleshooting", "Erros Comuns" (3 de max 5) | - |
| 16 | - | Frontend valida: `categoriasSelecionadas.length >= 1 && <= 5` → Se exceder: desabilita seleção e exibe toast warning |
| 17 | Clica em botão "Salvar Rascunho" | - |
| 18 | - | Frontend envia `POST /api/base-conhecimento/artigos` com body JSON: `{ titulo, resumo, problema, solucao, categoriaIds: [5,12,18], criticidade: "Normal", status: "Rascunho", clienteId }` |
| 19 | - | **Backend - FluentValidation**: `ArtigoValidator` valida tamanhos mínimos/máximos (titulo 10-200, resumo 50-500, problema ≥100, solução ≥200) → Se falhar: HTTP 400 com erros |
| 20 | - | **Backend - RN-KB-070-01**: Valida titulo único por categoria: `_context.Artigos.Any(a => a.ClienteId == request.ClienteId && a.Categorias.Any(c => request.CategoriaIds.Contains(c.Id)) && EF.Functions.Like(a.Titulo.ToLower(), request.Titulo.ToLower()))` → Se duplicado: HTTP 400 "KB_TITULO_DUPLICADO" |
| 21 | - | Backend cria entidade `Artigo` com Status = `StatusArtigo.Rascunho`, VersaoAtual = 1, AutorId = User.Id, DataCriacao = DateTime.UtcNow |
| 22 | - | Backend salva no banco: `_context.Artigos.Add(artigo); await _context.SaveChangesAsync();` |
| 23 | - | **Backend - Event**: Publica evento `ArtigoCriadoEvent` com ArtigoId |
| 24 | - | **Handler - Tags Automáticas NLP**: `ExtrairTagsAutomaticasHandler` recebe evento, concatena texto: `"{titulo} {problema} {solucao}"` |
| 25 | - | Handler invoca Azure Cognitive Services: `_cognitiveService.ExtrairEntidades(textoCompleto)` → Retorna entidades: `[{ "Windows", "Product" }, { "0x80070005", "Code" }, { "instalar", "Action" }]` |
| 26 | - | Handler extrai tags: tecnologias (Windows), códigos de erro (0x80070005), verbos (instalar) → `tagsSugeridas = ["Windows", "Windows Update", "0x80070005", "instalar", "erro"]` |
| 27 | - | Handler salva tags sugeridas: `artigo.TagsSugeridas = tagsSugeridas; await _context.SaveChangesAsync();` |
| 28 | - | Handler cria notificação para autor: "5 tags foram sugeridas automaticamente. Revise e aprove." com link `/base-conhecimento/artigos/{id}/tags` |
| 29 | - | **Handler - Workflow Aprovação**: `AplicarWorkflowAprovacaoHandler` verifica se artigo é crítico: `artigo.Criticidade == CriticidadeArtigo.Critico || artigo.Categorias.Any(c => c.RequereAprovacao)` |
| 30 | - | Como Criticidade = "Normal" e categorias não requerem aprovação: Handler NÃO cria workflow, artigo permanece "Rascunho" aguardando publicação manual |
| 31 | - | Backend retorna HTTP 201 Created com body: `ArtigoDto` contendo Id, Titulo, Status, VersaoAtual, TagsSugeridas, Link header: `/api/base-conhecimento/artigos/{id}` |
| 32 | - | Frontend exibe toast de sucesso: "Artigo salvo como rascunho" e redireciona para `/base-conhecimento/artigos/{id}/editar` |
| 33 | - | Frontend carrega tags sugeridas em seção "Tags Recomendadas" com checkboxes: ☑ Windows, ☑ Windows Update, ☑ 0x80070005, ☐ instalar, ☐ erro |
| 34 | Seleciona 3 tags sugeridas (Windows, Windows Update, 0x80070005) e clica "Aplicar Tags Selecionadas" | - |
| 35 | - | Frontend envia `PATCH /api/base-conhecimento/artigos/{id}/tags` com body: `{ tagsAceitas: ["Windows", "Windows Update", "0x80070005"] }` |
| 36 | - | Backend atualiza: `artigo.Tags = request.TagsAceitas; artigo.TagsSugeridas = null;` (limpa sugeridas) |
| 37 | Clica em botão "Publicar Artigo" | - |
| 38 | - | Frontend envia `PATCH /api/base-conhecimento/artigos/{id}/status` com body: `{ status: "Publicado" }` |
| 39 | - | Backend valida conteúdo completo: tags aplicadas (≥1), categorias (≥1), conteúdo mínimo → Se OK: `artigo.Status = StatusArtigo.Publicado; artigo.DataPublicacao = DateTime.UtcNow;` |
| 40 | - | Backend publica evento `ArtigoPublicadoEvent` → Triggera handler de notificação de subscritores (RN-KB-070-12) |
| 41 | - | Backend retorna HTTP 200 OK |
| 42 | - | Frontend exibe toast de sucesso: "Artigo publicado com sucesso!" e redireciona para visualização `/base-conhecimento/artigos/{id}` |

### 5. Fluxos Alternativos

**FA01: Artigo Crítico - Workflow de Aprovação Obrigatório**

- No passo 5, usuário seleciona Criticidade "Crítico" OU seleciona categoria "Segurança" (que tem flag `RequereAprovacao = true`)
- No passo 29, Handler detecta criticidade: `artigo.Criticidade == CriticidadeArtigo.Critico` → true
- Handler cria `WorkflowAprovacao` com 2 níveis: Nível 1 (Revisor Técnico, prazo 24h), Nível 2 (Gestor Conhecimento, prazo 48h)
- Handler atualiza: `artigo.Status = StatusArtigo.AguardandoAprovacao`
- Handler notifica revisor nível 1 via e-mail + notificação in-app: "Artigo #{id} aguarda sua revisão"
- Backend retorna status "AguardandoAprovacao" ao invés de "Rascunho"
- Frontend exibe badge amarelo: "⏳ Aguardando Aprovação - Nível 1" e desabilita botão "Publicar" (será publicado automaticamente após 2 aprovações)

**FA02: Upload de Anexo (PDF, DOCX)**

- Após passo 15, usuário clica em botão "Adicionar Anexo"
- Frontend abre dialog com drag-and-drop, usuário seleciona `manual-instalacao.pdf` (12MB)
- Frontend valida: tamanho ≤500MB, extensões permitidas (.pdf, .docx, .xlsx, .png, .jpg, .mp4)
- Frontend envia `POST /api/base-conhecimento/artigos/{id}/anexos` com FormData multipart
- Backend faz upload para Azure Blob Storage: container `kb-attachments`, path `{clienteId}/{artigoId}/{filename-sanitized}`
- Backend cria registro: `INSERT INTO ArtigoAnexo (ArtigoId, NomeArquivo, CaminhoBlob, TamanhoBytes, DataUpload)`
- Backend retorna HTTP 201 com `AnexoDto` contendo Id, Nome, Tamanho, UrlDownload
- Frontend exibe anexo na lista com ícone 📎, tamanho (12MB), botão preview (se PDF)

**FA03: Conteúdo Mínimo Não Atingido - Erro de Validação**

- No passo 19, usuário tenta salvar com Solução de apenas 80 caracteres (mínimo 200)
- FluentValidation detecta: `RuleFor(x => x.Solucao).MinimumLength(200)` → falha
- Backend retorna HTTP 400 com body: `{ "errors": { "solucao": ["KB_SOLUCAO_MUITO_CURTA: A solução deve ter no mínimo 200 caracteres. Atual: 80"] } }`
- Frontend exibe erro inline abaixo do editor Quill de Solução: "⚠️ A solução deve ter no mínimo 200 caracteres (faltam 120)"

**FA04: Titulo Duplicado na Mesma Categoria**

- No passo 20, já existe artigo ativo "Como resolver erro 0x80070005 ao instalar Windows Update" na categoria "Windows > Atualizações"
- Backend detecta duplicação: `tituloJaExiste == true`
- Backend retorna HTTP 400 com body: `{ "error": "KB_TITULO_DUPLICADO", "message": "Já existe um artigo ativo com este título nesta categoria. Por favor, escolha um título diferente ou inative o artigo existente.", "artigoExistenteId": 1234 }`
- Frontend exibe erro com link: "⚠️ Já existe um artigo com este título. [Ver artigo existente](/base-conhecimento/artigos/1234)"

### 6. Exceções

**EX01: Usuário Sem Permissão de Criação**

- No passo 2, frontend valida permissão local e detecta que usuário não tem `service-desk:base-conhecimento:criar`
- Frontend redireciona para `/base-conhecimento` com toast: "Você não tem permissão para criar artigos"
- Se usuário bypassar frontend e chamar API diretamente no passo 18:
- Backend valida: `User.HasPermission("service-desk:base-conhecimento:criar")` → false
- Backend retorna HTTP 403 com body: `{ "error": "FORBIDDEN", "message": "Você não tem permissão para criar artigos" }`

**EX02: Azure Cognitive Services Offline - Tags Não Geradas**

- No passo 25, Handler tenta invocar `_cognitiveService.ExtrairEntidades()` mas serviço retorna timeout ou HTTP 503
- Handler captura exceção `HttpRequestException`
- Handler registra log WARNING: "Azure Cognitive Services indisponível, tags automáticas não geradas"
- Handler continua fluxo SEM gerar tags (TagsSugeridas permanece vazio)
- Artigo é criado normalmente, mas autor não recebe sugestões de tags (terá que inserir manualmente)

**EX03: Upload de Imagem Excede Tamanho Máximo**

- No passo 11, usuário tenta fazer upload de `erro-screenshot.png` com 60MB (máximo 50MB)
- Backend valida: `file.Length > 50 * 1024 * 1024` → true
- Backend retorna HTTP 413 Payload Too Large com body: `{ "error": "KB_IMAGEM_MUITO_GRANDE", "message": "A imagem deve ter no máximo 50MB. Tamanho enviado: 60MB" }`
- Frontend exibe toast de erro: "Imagem muito grande (60MB). Máximo permitido: 50MB"

**EX04: Limite de Categorias Excedido (Tentativa de Associar 6 Categorias)**

- No passo 16, usuário tenta selecionar 6ª categoria após já ter 5 selecionadas
- Frontend valida: `this.categoriasSelecionadas.length >= this.maxCategorias` → true
- Frontend desabilita tree view (todas checkboxes ficam disabled exceto as já selecionadas)
- Frontend exibe toast warning: "Você pode selecionar no máximo 5 categorias"
- Se usuário manipular request no passo 18 enviando `categoriaIds: [1,2,3,4,5,6]`:
- Backend FluentValidation detecta: `RuleFor(x => x.CategoriaIds).Must(ids => ids.Count <= 5)` → falha
- Backend retorna HTTP 400 com body: `{ "error": "KB_LIMITE_CATEGORIAS_EXCEDIDO", "message": "Você pode associar no máximo 5 categorias por artigo" }`

### 7. Pós-condições

- Artigo criado no banco de dados com Status "Rascunho" ou "AguardandoAprovacao"
- Tags automáticas sugeridas via Azure Cognitive Services (se disponível)
- Workflow de aprovação criado (se artigo crítico)
- Versionamento inicial registrado (v1.0)
- Imagens/anexos armazenados no Azure Blob Storage
- Notificações enviadas (tags sugeridas, workflow aprovação)
- Evento `ArtigoCriadoEvent` publicado e processado
- Auditoria registrada: `UsuarioId`, `DataCriacao`, `IpOrigem`

### 8. Regras de Negócio Aplicáveis

- **RN-KB-070-01**: Titulo Unico por Categoria (validado no passo 20)
- **RN-KB-070-02**: Conteúdo Mínimo Obrigatório (titulo 10-200, resumo 50-500, problema ≥100, solução ≥200, ≥1 categoria)
- **RN-KB-070-03**: Workflow de Aprovação por Criticidade (artigos críticos ou categorias sensíveis requerem 2 aprovações)
- **RN-KB-070-04**: Versionamento Automático em Toda Alteração (versão inicial v1.0 criada, futuras edições geram v2.0, v3.0...)
- **RN-KB-070-08**: Limite de Categorias por Artigo (mínimo 1, máximo 5)
- **RN-KB-070-09**: Tags Automáticas via NLP (Azure Cognitive Services extrai tecnologias, códigos de erro, verbos de ação)

---

## UC03: Editar Artigo com Versionamento Temporal Tables

### 1. Descrição

Este caso de uso permite que usuários com permissão (Autor Original, Gestor de Conhecimento, Revisor) editem artigos existentes com versionamento automático completo usando SQL Server Temporal Tables, preservando histórico de todas as versões (before/after), metadata de alteração (quem, quando, IP origem, motivo obrigatório), comparação visual diff entre versões, rollback para versão anterior, e reativação de workflow de aprovação se artigo for crítico e houver alteração estrutural (titulo, problema, solução). O sistema detecta automaticamente se alteração é "major" (estrutural) ou "minor" (cosmética) e incrementa número de versão adequadamente.

### 2. Atores

- Usuário autenticado (Autor Original, Gestor de Conhecimento, Revisor)
- Sistema (Backend .NET 10, SQL Server Temporal Tables, Azure Blob Storage)

### 3. Pré-condições

- Usuário autenticado no sistema
- Permissão: `service-desk:base-conhecimento:editar` OU ser o autor original do artigo
- Multi-tenancy ativo (ClienteId válido)
- Artigo existe e não está excluído
- Feature flag `SERVICE_DESK_BASE_CONHECIMENTO_VERSIONAMENTO` habilitada
- SQL Server Temporal Tables configuradas (`SysStartTime`, `SysEndTime`, tabela histórico `Artigo_History`)

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa rota `/base-conhecimento/artigos/{id}/editar` | - |
| 2 | - | Frontend envia `GET /api/base-conhecimento/artigos/{id}?clienteId={clienteId}` |
| 3 | - | Backend valida permissão: `User.HasPermission("service-desk:base-conhecimento:editar") || artigo.AutorId == User.Id` → Se negado: HTTP 403 |
| 4 | - | Backend valida multi-tenancy: `artigo.ClienteId == request.ClienteId` → Se divergência: HTTP 403 "MULTI_TENANCY_VIOLATION" |
| 5 | - | Backend retorna `ArtigoDto` completo com Titulo, Resumo, Problema, Solucao, CausaRaiz, Prevencao, Tags, Categorias, VersaoAtual (ex: 2), TotalVersoes (ex: 2) |
| 6 | - | Frontend carrega formulário com dados atuais, editor Quill.js com conteúdo existente, categorias selecionadas, tags aplicadas |
| 7 | Altera conteúdo: modifica Solução de "Execute comando A" para "Execute comando B" (alteração estrutural) | - |
| 8 | Adiciona campo "Causa Raiz": "Permissão de arquivo incorreta no diretório System32" (novo conteúdo) | - |
| 9 | Preenche campo obrigatório "Motivo da Alteração": "Procedimento anterior estava obsoleto, atualizado para Windows 11" | - |
| 10 | Clica em botão "Salvar Alterações" | - |
| 11 | - | Frontend envia `PUT /api/base-conhecimento/artigos/{id}` com body JSON: `{ titulo, resumo, problema, solucao, causaRaiz, prevencao, categoriaIds, tags, motivoAlteracao, ehCorrecaoCosmetica: false, clienteId, usuarioId, ipOrigem }` |
| 12 | - | **Backend - Validação Básica**: FluentValidation valida campos obrigatórios (titulo 10-200, resumo 50-500, problema ≥100, solução ≥200, motivoAlteracao required) |
| 13 | - | Backend carrega artigo atual do banco: `var artigo = await _context.Artigos.Include(a => a.Categorias).FirstAsync(a => a.Id == request.Id);` |
| 14 | - | **Backend - Detecção de Alteração Estrutural**: Compara campos críticos: `alteracaoEstruturalDetectada = (artigo.Titulo != request.Titulo || artigo.Resumo != request.Resumo || artigo.Problema != request.Problema || artigo.Solucao != request.Solucao)` → true (Solucao mudou) |
| 15 | - | Como `alteracaoEstruturalDetectada == true`: Backend cria snapshot da versão anterior ANTES de modificar |
| 16 | - | **Backend - Criação de Snapshot Manual**: `var versaoAnterior = new ArtigoVersao { ArtigoId = artigo.Id, NumeroVersao = artigo.VersaoAtual, Titulo = artigo.Titulo, Resumo = artigo.Resumo, Problema = artigo.Problema, Solucao = artigo.Solucao, CausaRaiz = artigo.CausaRaiz, Prevencao = artigo.Prevencao, Tags = JsonSerializer.Serialize(artigo.Tags), AlteradoPorId = request.UsuarioId, DataAlteracao = DateTime.UtcNow, IpOrigem = request.IpOrigem, MotivoAlteracao = request.MotivoAlteracao, TipoVersao = TipoVersao.Major }` |
| 17 | - | Backend salva snapshot: `_context.ArtigoVersoes.Add(versaoAnterior);` |
| 18 | - | Backend incrementa versão: `artigo.VersaoAtual++;` → VersaoAtual passa de 2 para 3 |
| 19 | - | **Backend - Temporal Tables Automático**: SQL Server detecta UPDATE na tabela `Artigo` e automaticamente copia registro antigo para `Artigo_History` com `SysStartTime` = data anterior, `SysEndTime` = DateTime.UtcNow (momento do UPDATE) |
| 20 | - | Backend aplica alterações: `artigo.Titulo = request.Titulo; artigo.Resumo = request.Resumo; artigo.Problema = request.Problema; artigo.Solucao = request.Solucao; artigo.CausaRaiz = request.CausaRaiz; artigo.Prevencao = request.Prevencao; artigo.Tags = request.Tags; artigo.DataUltimaAtualizacao = DateTime.UtcNow;` |
| 21 | - | Backend atualiza categorias (many-to-many): Remove associações antigas e adiciona novas conforme `request.CategoriaIds` |
| 22 | - | **Backend - RN-KB-070-03**: Verifica se artigo é crítico: `if (artigo.Criticidade == CriticidadeArtigo.Critico)` → Se sim: `artigo.Status = StatusArtigo.AguardandoAprovacao` e triggera workflow novamente |
| 23 | - | Backend salva alterações: `await _context.SaveChangesAsync(cancellationToken);` → Commit da transação |
| 24 | - | **Backend - Event**: Publica evento `ArtigoAtualizadoEvent` com ArtigoId, VersaoAnterior, VersaoNova |
| 25 | - | Backend retorna HTTP 200 OK com `ArtigoDto` atualizado contendo nova VersaoAtual (3), DataUltimaAtualizacao, TotalVersoes (3) |
| 26 | - | Frontend exibe toast de sucesso: "Artigo atualizado para versão 3.0" |
| 27 | - | Frontend exibe badge de versão: "📝 Versão 3.0 (atualizado há 2 segundos)" |
| 28 | Clica em link "Ver Histórico de Versões" no canto superior direito | - |
| 29 | - | Frontend navega para `/base-conhecimento/artigos/{id}/versoes` |
| 30 | - | Frontend envia `GET /api/base-conhecimento/artigos/{id}/versoes?clienteId={clienteId}` |
| 31 | - | **Backend - Query Temporal Tables**: Executa `SELECT * FROM Artigo FOR SYSTEM_TIME ALL WHERE Id = @id ORDER BY SysStartTime DESC` → Retorna todas as versões históricas com timestamps |
| 32 | - | Backend combina dados de `ArtigoVersao` (snapshot manual) com `Artigo_History` (Temporal Tables automático) |
| 33 | - | Backend retorna lista com 3 versões: v3.0 (atual), v2.0 (28/12/2025 14:30), v1.0 (15/12/2025 09:00) |
| 34 | - | Frontend renderiza timeline vertical com cards de versão: cada card mostra número versão, data, autor, motivo, badge (MAJOR/MINOR) |
| 35 | Clica em botão "Comparar v2.0 vs v3.0" | - |
| 36 | - | Frontend abre modal split-screen com diff visual: coluna esquerda (v2.0), coluna direita (v3.0), diferenças destacadas em vermelho (deletado) e verde (adicionado) |
| 37 | - | Frontend usa biblioteca `diff-match-patch` para calcular diferenças: "Execute comando <span class='deleted'>A</span><span class='added'>B</span>" |

### 5. Fluxos Alternativos

**FA01: Correção Cosmética (Minor Version) - Apenas Ortografia**

- No passo 7, usuário apenas corrige erro ortográfico: "instalar o programma" → "instalar o programa"
- No passo 11, frontend marca `ehCorrecaoCosmetica: true`
- No passo 14, backend detecta alteração NÃO estrutural (apenas Solucao mudou, mas é correção minor)
- No passo 16, backend cria snapshot com `TipoVersao = TipoVersao.Minor`
- No passo 18, backend incrementa versão minor: `artigo.VersaoAtual = 2.1` (ao invés de 3.0)
- Artigo NÃO volta para workflow de aprovação mesmo se crítico (correção cosmética não requer reaprovação)
- Frontend exibe toast: "Artigo atualizado para versão 2.1 (correção minor)"

**FA02: Rollback para Versão Anterior**

- No passo 35, usuário clica em botão "Reverter para v2.0" na timeline de versões
- Frontend exibe confirmação: "Tem certeza que deseja reverter para versão 2.0? A versão atual (3.0) será preservada no histórico."
- Usuário confirma
- Frontend envia `POST /api/base-conhecimento/artigos/{id}/rollback` com body: `{ versaoDestino: 2, motivoRollback: "Procedimento da v3 causou incidentes" }`
- Backend carrega dados da v2.0: `var versaoAnterior = await _context.ArtigoVersoes.FirstAsync(v => v.ArtigoId == artigo.Id && v.NumeroVersao == 2);`
- Backend cria snapshot da v3.0 atual (antes de reverter)
- Backend restaura campos da v2.0: `artigo.Titulo = versaoAnterior.Titulo; artigo.Solucao = versaoAnterior.Solucao; ...`
- Backend incrementa versão: `artigo.VersaoAtual = 4` (rollback cria nova versão, não sobrescreve)
- Backend adiciona flag: `artigo.EhRollback = true; artigo.VersaoOrigemRollback = 2;`
- Frontend exibe badge especial: "↩️ Versão 4.0 (revertido da v2.0)"

**FA03: Edição com Conflito de Concorrência (Outro Usuário Editou Simultaneamente)**

- No passo 1, usuário A carrega artigo v2.0 às 14:30
- Às 14:35, usuário B salva edição do mesmo artigo → versão passa para v3.0
- Às 14:40, usuário A tenta salvar sua edição (ainda baseada em v2.0)
- No passo 23, backend detecta `DbUpdateConcurrencyException` (RowVersion/Timestamp mudou)
- Backend retorna HTTP 409 Conflict com body: `{ "error": "CONCURRENT_EDIT_DETECTED", "message": "Este artigo foi editado por outro usuário. Recarregue a página para ver a versão mais recente.", "versaoEsperada": 2, "versaoAtual": 3, "editorConflitante": "maria.silva@empresa.com" }`
- Frontend exibe modal de conflito: "⚠️ Conflito detectado - Maria Silva editou este artigo há 5 minutos. [Recarregar página] [Salvar como novo artigo]"

**FA04: Visualizar Diff Detalhado Lado a Lado**

- No passo 36, ao invés de diff inline, usuário clica "Ver diff detalhado"
- Frontend renderiza comparação field-by-field em tabela:
  | Campo | v2.0 | v3.0 |
  |-------|------|------|
  | Titulo | Como resolver erro... | Como resolver erro... (sem mudança) |
  | Solucao | Execute comando A | Execute comando B (✏️ ALTERADO) |
  | Causa Raiz | (vazio) | Permissão incorreta... (➕ ADICIONADO) |
- Frontend destaca em amarelo campos alterados, verde campos adicionados, vermelho campos removidos

### 6. Exceções

**EX01: Usuário Sem Permissão de Edição (Não é Autor nem Gestor)**

- No passo 3, backend valida permissão e detecta que usuário não tem `service-desk:base-conhecimento:editar` E não é o autor original (AutorId ≠ User.Id)
- Backend retorna HTTP 403 com body: `{ "error": "FORBIDDEN", "message": "Você não tem permissão para editar este artigo. Apenas o autor original ou gestores de conhecimento podem editar." }`
- Frontend exibe toast de erro e redireciona para visualização read-only

**EX02: Motivo de Alteração Não Informado (Campo Obrigatório)**

- No passo 9, usuário NÃO preenche campo "Motivo da Alteração" (deixa em branco)
- No passo 12, FluentValidation detecta: `RuleFor(x => x.MotivoAlteracao).NotEmpty()` → falha
- Backend retorna HTTP 400 com body: `{ "errors": { "motivoAlteracao": ["KB_MOTIVO_OBRIGATORIO: O motivo da alteração é obrigatório para alterações estruturais"] } }`
- Frontend exibe erro inline abaixo do campo: "⚠️ Informe o motivo da alteração (obrigatório para versionamento)"

**EX03: SQL Server Temporal Tables Não Configuradas**

- No passo 19, backend tenta fazer UPDATE mas tabela `Artigo` não tem Temporal Tables habilitadas (coluna `SysStartTime` não existe)
- SQL Server lança exceção: `SqlException: Invalid column name 'SysStartTime'`
- Backend captura exceção, registra log CRITICAL: "Temporal Tables não configuradas - versionamento histórico não funcionará"
- Backend continua execução usando APENAS snapshot manual em `ArtigoVersao` (fallback)
- Histórico parcial é preservado, mas sem versionamento automático do SQL Server
- Backend dispara alerta para DevOps via Application Insights

**EX04: Tentativa de Editar Artigo Arquivado**

- No passo 4, backend carrega artigo e detecta: `artigo.Status == StatusArtigo.Arquivado`
- Backend retorna HTTP 400 com body: `{ "error": "KB_ARTIGO_ARQUIVADO", "message": "Este artigo está arquivado e não pode ser editado. Reative o artigo antes de editar." }`
- Frontend exibe modal: "Este artigo foi arquivado em 15/11/2025 (motivo: Sem acessos em 180 dias). [Reativar Artigo] [Cancelar]"
- Se usuário clicar "Reativar": frontend envia `PATCH /api/base-conhecimento/artigos/{id}/reativar` → Status volta para "Publicado" → Edição é liberada

### 7. Pós-condições

- Artigo atualizado com nova versão (major ou minor conforme tipo de alteração)
- Snapshot manual criado em tabela `ArtigoVersao` com metadata completa
- Histórico automático registrado em `Artigo_History` via Temporal Tables
- Workflow de aprovação reativado (se artigo crítico e alteração estrutural)
- Evento `ArtigoAtualizadoEvent` publicado e processado
- Auditoria registrada: `AlteradoPorId`, `DataAlteracao`, `IpOrigem`, `MotivoAlteracao`
- Notificações enviadas (se workflow reativado)

### 8. Regras de Negócio Aplicáveis

- **RN-KB-070-04**: Versionamento Automático em Toda Alteração (snapshot antes de modificar, incremento de versão, metadata completa, retenção 7 anos)
- **RN-KB-070-03**: Workflow de Aprovação por Criticidade (artigo crítico volta para "AguardandoAprovacao" se houver alteração estrutural)
- **RN-KB-070-02**: Conteúdo Mínimo Obrigatório (validado ao editar também)
- **RN-KB-070-01**: Titulo Unico por Categoria (validado ao alterar titulo)

---

## UC04: Visualizar Artigo com Votação e Artigos Relacionados ML

### 1. Descrição

Este caso de uso permite que usuários autenticados e anônimos (portal self-service) visualizem artigo completo com formatação rica, imagens inline, anexos com preview, votação Útil/Não Útil com comentário opcional, sugestão automática de top 5 artigos relacionados via Similarity Score ML (Cosine Similarity sobre vetores TF-IDF), histórico de versões, registro de acesso em auditoria (quem, quando, origem, tempo de leitura), cálculo automático de Score de Utilidade, e integração com chamados (permitir vincular artigo a chamado aberto). O sistema exibe métricas em tempo real (total de acessos, taxa de utilidade, votos úteis) e permite feedback estruturado.

### 2. Atores

- Usuário autenticado (Analista Service Desk, Gestor, Usuário Final)
- Usuário anônimo (portal self-service público)
- Sistema (Backend .NET 10, ElasticSearch, Redis Cache, Azure Blob Storage, SignalR)

### 3. Pré-condições

- Artigo existe e está publicado (Status = "Publicado")
- Feature flag `SERVICE_DESK_BASE_CONHECIMENTO` habilitada
- Multi-tenancy ativo (ClienteId válido para usuários autenticados)
- Para portal self-service: Feature flag `SERVICE_DESK_BASE_CONHECIMENTO_SELF_SERVICE` habilitada

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa rota `/base-conhecimento/artigos/{id}` | - |
| 2 | - | Frontend envia `GET /api/base-conhecimento/artigos/{id}?clienteId={clienteId}` |
| 3 | - | **Backend - Validação Status**: Backend carrega artigo: `var artigo = await _context.Artigos.Include(a => a.Categorias).Include(a => a.Anexos).Include(a => a.Autor).FirstAsync(a => a.Id == request.Id);` |
| 4 | - | Backend valida: `artigo.Status == StatusArtigo.Publicado && !artigo.Excluido` → Se não publicado ou excluído: HTTP 404 |
| 5 | - | Backend valida multi-tenancy: `artigo.ClienteId == request.ClienteId` → Se divergência: HTTP 403 |
| 6 | - | **Backend - Event Registro de Acesso**: Backend publica evento `ArtigoVisualizadoEvent { ArtigoId, UsuarioId, ClienteId, IpOrigem, UserAgent, OrigemAcesso }` |
| 7 | - | **Handler - Auditoria**: `RegistrarAcessoArtigoHandler` cria registro: `INSERT INTO ArtigoAcesso (ArtigoId, UsuarioId, DataHoraAcesso, IpOrigem, UserAgent, OrigemAcesso, ClienteId)` |
| 8 | - | Handler incrementa contador desnormalizado: `artigo.TotalAcessos++; artigo.DataUltimoAcesso = DateTime.UtcNow;` (para performance, evita COUNT em toda visualização) |
| 9 | - | **Backend - Cálculo de Artigos Relacionados**: Backend verifica cache Redis: `_cache.GetStringAsync($"kb_related_{artigoId}")` |
| 10 | - | Se cache miss: Backend busca relacionamentos automáticos ML: `var relacionados = await _context.ArtigoRelacionamentos.Where(r => r.ArtigoOrigemId == artigo.Id && r.TipoRelacionamento == TipoRelacionamento.Automatico).OrderByDescending(r => r.SimilarityScore).Take(5).ToListAsync();` |
| 11 | - | Backend retorna `ArtigoDetalheDto` com: Id, Titulo, Resumo, Problema, Solucao, CausaRaiz, Prevencao, Tags, Categorias, Anexos (com UrlDownload), AutorNome, DataPublicacao, VersaoAtual, TotalAcessos, ScoreUtilidade (ex: 0.853), VotosUtil (35), VotosNaoUtil (5), ArtigosRelacionados (top 5 com Id, Titulo, SimilarityScore) |
| 12 | - | Backend armazena resultado no cache Redis com TTL 10min: `_cache.SetStringAsync($"kb_related_{artigoId}", json, new DistributedCacheEntryOptions { AbsoluteExpirationRelativeToNow = TimeSpan.FromMinutes(10) });` |
| 13 | - | Frontend renderiza artigo com layout estruturado: Título H1, badge de categorias (breadcrumb), metadata (autor, data publicação, versão, 👁️ 1.250 acessos), editor Quill.js read-only com formatação preservada |
| 14 | - | Frontend renderiza seções: "Problema" (background cinza claro), "Solução" (destaque com ícone ✅), "Causa Raiz" (collapsible), "Prevenção" (collapsible) |
| 15 | - | Frontend renderiza seção "Anexos" (se houver): Lista com ícone por tipo (📎 PDF, 📊 XLSX, 🖼️ PNG), tamanho, botão "Download", botão "Preview" (se PDF/imagem) |
| 16 | - | Frontend renderiza barra de utilidade: "Este artigo foi útil? 👍 Útil (35) 👎 Não útil (5)" + barra de progresso verde (85.3% útil) |
| 17 | - | Frontend renderiza seção "Artigos Relacionados" com cards dos top 5: cada card mostra título, resumo (70 chars), score de similaridade (ex: "82% similar"), link para artigo |
| 18 | Lê artigo completo durante 2 minutos e 45 segundos | - |
| 19 | Clica em botão "👍 Útil" | - |
| 20 | - | Frontend exibe modal: "Este artigo resolveu seu problema? ☑ Sim, problema resolvido / ☐ Não resolveu / Comentário opcional (500 chars max)" |
| 21 | Seleciona "Sim, problema resolvido" e adiciona comentário "Procedimento funcionou perfeitamente no Windows 11" | - |
| 22 | - | Frontend envia `POST /api/base-conhecimento/artigos/{id}/votar` com body: `{ ehUtil: true, resolveuProblema: true, comentario: "Procedimento funcionou...", tempoLeituraSegundos: 165 }` |
| 23 | - | Backend cria registro: `INSERT INTO ArtigoVotacao (ArtigoId, UsuarioId, EhUtil, ResolveuProblema, Comentario, DataVotacao)` |
| 24 | - | **Backend - Event Recalculo Score**: Backend publica evento `ArtigoVotadoEvent { ArtigoId }` |
| 25 | - | **Handler - RN-KB-070-05**: `RecalcularScoreUtilidadeHandler` calcula score composto: `scoreUtilidade = (votosUtil/totalVotos) * 0.6 + (acessosComResolucao/totalAcessos) * 0.4` |
| 26 | - | Handler calcula: `(36/41) * 0.6 + (900/1250) * 0.4 = 0.878 * 0.6 + 0.720 * 0.4 = 0.527 + 0.288 = 0.815 (81.5%)` |
| 27 | - | Handler atualiza: `artigo.ScoreUtilidade = 0.815m; artigo.DataUltimaAtualizacaoScore = DateTime.UtcNow;` |
| 28 | - | Como score é ≥60%, artigo NÃO é sinalizado para revisão |
| 29 | - | Backend atualiza registro de acesso com tempo de leitura: `UPDATE ArtigoAcesso SET TempoLeituraSegundos = 165, ResolveuProblema = true WHERE ArtigoId = @id AND UsuarioId = @userId ORDER BY DataHoraAcesso DESC LIMIT 1` |
| 30 | - | Backend retorna HTTP 201 Created com novo score: `{ "scoreUtilidade": 0.815, "votosUtil": 36, "votosNaoUtil": 5 }` |
| 31 | - | Frontend atualiza barra de utilidade em tempo real (animação smooth): "81.5% útil" com barra de progresso verde |
| 32 | - | Frontend exibe toast de agradecimento: "✅ Obrigado pelo seu feedback!" |
| 33 | Clica em artigo relacionado "Configurar timeout VPN Cisco" (similarity 82%) | - |
| 34 | - | Frontend navega para `/base-conhecimento/artigos/{idRelacionado}` e reinicia fluxo de visualização |
| 35 | - | Backend registra origem de acesso: `OrigemAcesso = OrigemAcesso.ArtigoRelacionado` (para medir efetividade de sugestões ML) |

### 5. Fluxos Alternativos

**FA01: Usuário Vota "Não Útil" com Comentário Negativo**

- No passo 19, usuário clica em "👎 Não útil"
- No passo 21, usuário seleciona "Não resolveu" e adiciona comentário: "Procedimento está desatualizado, não funciona no Windows 11 22H2"
- No passo 23, backend cria votação: `{ ehUtil: false, resolveuProblema: false, comentario: "..." }`
- No passo 26, score recalculado: `(35/41) * 0.6 + (900/1250) * 0.4 = 0.854 * 0.6 + 0.720 * 0.4 = 0.512 + 0.288 = 0.800 (80%)` (score caiu de 81.5% para 80%)
- Backend notifica autor original e gestores de conhecimento: "Artigo #{id} recebeu feedback negativo: 'Procedimento está desatualizado...'" com link para revisar
- Frontend permite que gestor responda ao comentário (botão "Responder feedback" visível apenas para gestores)

**FA02: Score Cai Abaixo de 60% - Sinalização Automática para Revisão**

- No passo 26, após múltiplas votações negativas, score calculado é 0.58 (58%)
- Handler detecta: `artigo.ScoreUtilidade < 0.6m && totalVotos >= 10` → true
- Handler atualiza: `artigo.RequereRevisao = true; artigo.MotivoRevisao = $"Score de utilidade baixo: 58% (Votos Útil: 12/25, Resoluções: 30/100)"`
- Handler cria notificação para "GESTOR_CONHECIMENTO" com tipo `TipoNotificacao.ArtigoRequereRevisao`
- Frontend exibe badge laranja no artigo: "⚠️ Artigo sinalizado para revisão (score baixo: 58%)"
- Gestor acessa dashboard de pendências e vê artigo na lista "Artigos Requerendo Revisão"

**FA03: Download de Anexo PDF com Preview Inline**

- No passo 15, usuário clica em botão "Preview" do anexo `manual-instalacao.pdf`
- Frontend envia `GET /api/base-conhecimento/artigos/{id}/anexos/{anexoId}/preview`
- Backend valida permissão de acesso ao anexo (mesmo cliente)
- Backend gera URL assinada temporária do Azure Blob Storage (SAS token válido por 1 hora): `https://icontrolitstorage.blob.core.windows.net/kb-attachments/10/1234/manual-instalacao.pdf?sv=2021-08-06&se=2025-12-28T15%3A30%3A00Z&sr=b&sp=r&sig=...`
- Backend retorna HTTP 200 com URL assinada
- Frontend abre modal com `<iframe>` ou PDF.js viewer renderizando PDF inline (sem download)
- Usuário pode navegar páginas, zoom, fechar modal

**FA04: Vincular Artigo a Chamado Aberto (Integração RF-073)**

- Após passo 18, usuário analista de service desk identifica que artigo resolve chamado #5678 que está atendendo
- Usuário clica em botão "Vincular a Chamado" no canto superior direito
- Frontend exibe modal: "Vincular a qual chamado?" com autocomplete de chamados abertos do usuário
- Usuário digita "#5678" ou "problema VPN" → Autocomplete retorna "Chamado #5678 - Erro VPN timeout" (busca em título/descrição)
- Usuário seleciona chamado
- Frontend envia `POST /api/service-desk/chamados/{chamadoId}/artigos` com body: `{ artigoId: 1234 }`
- Backend cria vínculo: `INSERT INTO ChamadoArtigo (ChamadoId, ArtigoId, VinculadoPorId, DataVinculo)`
- Backend adiciona comentário automático no chamado: "💡 Artigo sugerido: 'Como resolver erro VPN timeout' - Link: /base-conhecimento/artigos/1234"
- Frontend exibe toast: "Artigo vinculado ao chamado #5678" e atualiza ícone (🔗 Vinculado a 1 chamado)

**FA05: Artigos Relacionados ML Ainda Não Calculados (Artigo Novo)**

- No passo 10, artigo foi publicado há 5 minutos e job noturno de cálculo de similarity ainda não executou
- Backend busca relacionamentos e retorna lista vazia: `relacionados = []`
- No passo 17, frontend exibe mensagem: "Artigos relacionados serão calculados em breve (aguarde processamento)"
- Backend enfileira job Hangfire: `BackgroundJob.Enqueue(() => _similarityService.CalcularRelacionadosAsync(artigoId));`
- Job executa em background, calcula Cosine Similarity, salva relacionamentos
- Após 2 minutos, usuário recarrega página e artigos relacionados aparecem

### 6. Exceções

**EX01: Artigo Não Publicado (Status = Rascunho ou AguardandoAprovacao)**

- No passo 4, backend carrega artigo e detecta: `artigo.Status == StatusArtigo.Rascunho`
- Backend retorna HTTP 404 com body: `{ "error": "KB_ARTIGO_NAO_PUBLICADO", "message": "Este artigo ainda não está disponível para visualização" }`
- Frontend exibe página 404: "Artigo não encontrado ou ainda não publicado"
- Se usuário for o autor original ou gestor: Frontend exibe link "Visualizar rascunho" (permite preview antes de publicar)

**EX02: Votação Duplicada (Usuário Já Votou Anteriormente)**

- No passo 23, backend tenta criar votação mas já existe registro: `SELECT COUNT(*) FROM ArtigoVotacao WHERE ArtigoId = @id AND UsuarioId = @userId` → 1
- Backend retorna HTTP 400 com body: `{ "error": "KB_VOTO_DUPLICADO", "message": "Você já votou neste artigo em 25/12/2025. Seu voto anterior foi: Útil" }`
- Frontend exibe toast: "Você já avaliou este artigo. Obrigado pelo seu feedback anterior!"
- Frontend desabilita botões de votação (👍/👎 ficam cinza)

**EX03: Cache Redis Offline - Fallback para Banco de Dados**

- No passo 9, backend tenta acessar Redis mas serviço está indisponível: `_cache.GetStringAsync()` lança `RedisConnectionException`
- Backend captura exceção, registra log WARNING: "Redis offline, fallback para query SQL"
- Backend executa query direta no banco: `var relacionados = await _context.ArtigoRelacionamentos...` (sem cache)
- Resposta mais lenta (~200ms vs 20ms com cache) mas funcionalidade não quebra
- Backend dispara alerta para DevOps

**EX04: Usuário Anônimo (Portal Self-Service) Tenta Votar Sem Autenticação**

- Usuário acessa portal público `/kb-public/artigos/{id}` (sem login)
- No passo 19, usuário clica em "👍 Útil"
- No passo 22, frontend detecta que usuário não está autenticado (`User == null`)
- Frontend exibe modal: "Para avaliar este artigo, você precisa fazer login. [Fazer Login] [Fechar]"
- Se usuário clicar "Fazer Login": redireciona para `/login?returnUrl=/base-conhecimento/artigos/{id}`
- Após login, retorna para artigo e pode votar normalmente

**EX05: Tentativa de Acesso a Artigo de Outro Cliente (Multi-Tenancy Violation)**

- No passo 5, usuário com ClienteId=10 tenta acessar artigo com ClienteId=20 (manipulou URL)
- Backend detecta: `artigo.ClienteId != request.ClienteId`
- Backend retorna HTTP 403 com body: `{ "error": "MULTI_TENANCY_VIOLATION", "message": "Você não pode acessar artigos de outro cliente" }`
- Backend registra evento de auditoria de segurança: `SecurityEventType.MultiTenancyViolationAttempt`
- Frontend exibe página de erro 403: "Acesso negado - Este artigo não está disponível para sua organização"

### 7. Pós-condições

- Acesso registrado em auditoria com metadata completa (quem, quando, origem, tempo de leitura)
- Contador de acessos incrementado (desnormalizado para performance)
- Votação registrada (se usuário votou)
- Score de Utilidade recalculado em tempo real
- Artigo sinalizado para revisão (se score < 60%)
- Artigos relacionados retornados via ML Similarity Score
- Cache Redis atualizado (se aplicável)
- Métricas de uso registradas para analytics

### 8. Regras de Negócio Aplicáveis

- **RN-KB-070-05**: Cálculo Automático de Score de Utilidade (60% votos + 40% resoluções, recalculado em tempo real, sinalização se < 60%)
- **RN-KB-070-10**: Artigos Relacionados via Similarity Score (Cosine Similarity ≥ 30%, top 5, recalculado ao publicar/atualizar)
- **RN-KB-070-11**: Auditoria Completa de Acessos (quem, quando, origem, tempo de leitura, se resolveu, retenção 7 anos)
- **RN-KB-070-12**: Notificação de Novos Artigos por Subscrição (não aplicável neste UC, mas triggado ao publicar artigo)

---

## UC05: Configurar Workflow de Aprovação e Dashboard de Gestão

### 1. Descrição

Este caso de uso permite que Gestores de Conhecimento configurem workflow de aprovação por categoria (definir quais categorias requerem aprovação obrigatória, quantos níveis, papéis aprovadores, SLA de aprovação), gerenciem artigos pendentes de aprovação através de dashboard visual (lista de pendências, busca, filtros por categoria/criticidade/autor), executem ações de aprovação/rejeição com justificativa obrigatória, monitorem métricas de qualidade da base de conhecimento (artigos publicados vs rascunhos, score médio de utilidade, artigos obsoletos, coverage de chamados, top autores), e configurem detecção automática de artigos obsoletos (critérios: dias sem acesso, score baixo, tecnologias descontinuadas).

### 2. Atores

- Gestor de Conhecimento
- Revisor Técnico (para aprovação nível 1)
- Sistema (Backend .NET 10, Hangfire, SignalR)

### 3. Pré-condições

- Usuário autenticado no sistema
- Permissão: `service-desk:base-conhecimento:gestao`
- Multi-tenancy ativo (ClienteId válido)
- Feature flag `SERVICE_DESK_BASE_CONHECIMENTO_WORKFLOW_APROVACAO` habilitada

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Gestor acessa rota `/base-conhecimento/gestao/workflow` | - |
| 2 | - | Frontend valida permissão local: `hasPermission('service-desk:base-conhecimento:gestao')` → Se negado: redireciona |
| 3 | - | Frontend envia `GET /api/base-conhecimento/categorias?incluirConfigWorkflow=true&clienteId={clienteId}` |
| 4 | - | Backend retorna lista de categorias hierárquicas com configuração de workflow: `CategoriaDto { Id, Nome, CategoriaPaiId, RequereAprovacao, NiveisAprovacao, SlaAprovacaoHoras, PapeisAprovadores }` |
| 5 | - | Frontend renderiza tela com tree view de categorias, cada categoria tem toggle "Requer Aprovação" e botão "Configurar Workflow" |
| 6 | Gestor seleciona categoria "Segurança" e clica em "Configurar Workflow" | - |
| 7 | - | Frontend abre modal "Configuração de Workflow - Segurança" com formulário: "☑ Requer Aprovação Obrigatória", "Número de Níveis: [2 ▼]", "SLA Total: [48] horas" |
| 8 | - | Frontend renderiza seção de níveis: "Nível 1: Papel [REVISOR_TECNICO ▼], Prazo [24h], ☑ Obrigatório" / "Nível 2: Papel [GESTOR_CONHECIMENTO ▼], Prazo [48h], ☑ Obrigatório" |
| 9 | Gestor altera SLA do Nível 1 de 24h para 12h (artigos de segurança precisam aprovação mais rápida) | - |
| 10 | Gestor clica em "Salvar Configuração" | - |
| 11 | - | Frontend envia `PUT /api/base-conhecimento/categorias/{id}/workflow` com body: `{ requereAprovacao: true, niveisAprovacao: [{ ordem: 1, papel: "REVISOR_TECNICO", prazoHoras: 12, obrigatorio: true }, { ordem: 2, papel: "GESTOR_CONHECIMENTO", prazoHoras: 48, obrigatorio: true }] }` |
| 12 | - | Backend valida: soma de prazos ≤ 168h (7 dias max), níveis ordenados sequencialmente (1, 2, ...), papéis existem no RBAC |
| 13 | - | Backend atualiza: `UPDATE Categoria SET RequereAprovacao = true, ConfigWorkflowJson = @json WHERE Id = @id AND ClienteId = @clienteId` |
| 14 | - | Backend retorna HTTP 200 OK |
| 15 | - | Frontend exibe toast de sucesso: "Workflow de aprovação configurado para categoria Segurança" |
| 16 | Gestor navega para `/base-conhecimento/gestao/aprovacoes` (dashboard de pendências) | - |
| 17 | - | Frontend envia `GET /api/base-conhecimento/gestao/aprovacoes-pendentes?clienteId={clienteId}` |
| 18 | - | Backend executa query: `SELECT artigos com Status = AguardandoAprovacao e WorkflowAprovacao.Status = AguardandoRevisao ou EmRevisao, filtra por ClienteId, ordena por DataCriacao ASC (mais antigos primeiro)` |
| 19 | - | Backend retorna lista de 15 artigos pendentes: `AprovacaoPendenteDto { ArtigoId, Titulo, AutorNome, Categoria, Criticidade, DataSubmissao, NivelAtual, AprovadorAtual, SlaRestanteHoras, StatusWorkflow }` |
| 20 | - | Frontend renderiza tabela com colunas: Título, Autor, Categoria, Criticidade, Submetido há, Nível, Aprovador, SLA Restante (colorido: verde >24h, amarelo 12-24h, vermelho <12h), Ações [Revisar] |
| 21 | - | Frontend exibe KPIs no topo: "📋 15 artigos aguardando aprovação", "⏰ 3 artigos com SLA crítico (<12h)", "⚠️ 1 artigo vencido" |
| 22 | Gestor clica em botão "Revisar" do artigo "Procedimento de exclusão de dados LGPD" | - |
| 23 | - | Frontend navega para `/base-conhecimento/gestao/aprovacoes/{artigoId}` |
| 24 | - | Frontend envia `GET /api/base-conhecimento/artigos/{id}?incluirWorkflow=true&clienteId={clienteId}` |
| 25 | - | Backend retorna artigo completo + workflow: `{ artigo: {...}, workflow: { status: "AguardandoRevisao", nivelAtual: 1, aprovacoes: [{ nivel: 1, status: "Pendente", aprovadorNome: null, dataAprovacao: null }] } }` |
| 26 | - | Frontend renderiza artigo em modo preview (read-only) com barra lateral de workflow: "Nível 1 - Revisor Técnico: ⏳ Pendente", "Nível 2 - Gestor Conhecimento: ⏸️ Não iniciado" |
| 27 | Gestor lê artigo, valida procedimento contra documentação LGPD, verifica compliance | - |
| 28 | Gestor clica em botão "✅ Aprovar Nível 1" | - |
| 29 | - | Frontend exibe modal: "Aprovar artigo? Comentário (opcional): [____]", botões [Aprovar] [Cancelar] |
| 30 | Gestor adiciona comentário "Procedimento validado conforme Lei 13.709/2018 (LGPD) e GDPR" e clica "Aprovar" | - |
| 31 | - | Frontend envia `POST /api/base-conhecimento/artigos/{id}/aprovar` com body: `{ nivelAprovacao: 1, aprovado: true, comentario: "Procedimento validado...", aprovadorId, dataAprovacao: DateTime.UtcNow }` |
| 32 | - | Backend carrega workflow: `var workflow = await _context.WorkflowsAprovacao.Include(w => w.Niveis).FirstAsync(w => w.ArtigoId == request.ArtigoId);` |
| 33 | - | Backend valida: usuário tem papel correto para nível 1 (`User.HasRole("REVISOR_TECNICO")` ou `User.HasRole("GESTOR_CONHECIMENTO")`) → OK |
| 34 | - | Backend atualiza nível 1: `niveis[0].Status = StatusNivelAprovacao.Aprovado; niveis[0].AprovadorId = request.AprovadorId; niveis[0].DataAprovacao = request.DataAprovacao; niveis[0].Comentario = request.Comentario;` |
| 35 | - | Backend verifica se há próximo nível: `niveis.Count > 1` → true (existe nível 2) |
| 36 | - | Backend atualiza workflow: `workflow.NivelAtual = 2; workflow.Status = StatusWorkflow.AguardandoRevisao;` (passa para nível 2) |
| 37 | - | **Backend - Notificação Próximo Nível**: Backend busca usuários com papel "GESTOR_CONHECIMENTO" e envia notificação: "Artigo 'Procedimento LGPD' foi aprovado no Nível 1 e aguarda sua aprovação (Nível 2)" |
| 38 | - | Backend salva alterações: `await _context.SaveChangesAsync();` |
| 39 | - | Backend retorna HTTP 200 OK com workflow atualizado |
| 40 | - | Frontend atualiza barra lateral: "Nível 1 - Revisor Técnico: ✅ Aprovado por João Silva em 28/12/2025 14:30", "Nível 2 - Gestor Conhecimento: ⏳ Aguardando aprovação" |
| 41 | - | Frontend exibe toast de sucesso: "Artigo aprovado no Nível 1. Aguardando aprovação do Gestor de Conhecimento (Nível 2)" |
| 42 | 2 horas depois, Gestor com papel "GESTOR_CONHECIMENTO" acessa pendências e aprova nível 2 | - |
| 43 | - | Backend detecta que todos os níveis foram aprovados: `niveis.All(n => n.Status == StatusNivelAprovacao.Aprovado)` → true |
| 44 | - | Backend publica artigo automaticamente: `artigo.Status = StatusArtigo.Publicado; artigo.DataPublicacao = DateTime.UtcNow;` |
| 45 | - | Backend atualiza workflow: `workflow.Status = StatusWorkflow.Concluido; workflow.DataConclusao = DateTime.UtcNow;` |
| 46 | - | **Backend - Event**: Publica evento `ArtigoPublicadoEvent` → Triggera notificações de subscritores (RN-KB-070-12) |
| 47 | - | Backend notifica autor original: "Seu artigo 'Procedimento LGPD' foi aprovado e publicado automaticamente" |
| 48 | Gestor navega para `/base-conhecimento/gestao/dashboard` (métricas de qualidade) | - |
| 49 | - | Frontend envia `GET /api/base-conhecimento/gestao/metricas?periodo=ultimos30dias&clienteId={clienteId}` |
| 50 | - | Backend executa queries agregadas: Total Artigos Publicados, Artigos em Rascunho, Score Médio Utilidade, Artigos Obsoletos (sem acesso 180+ dias), Coverage Chamados (% chamados com artigo vinculado), Top 10 Autores (por qtde artigos + votos positivos) |
| 51 | - | Backend retorna JSON com métricas: `{ totalPublicados: 1.250, totalRascunhos: 45, scoreMedio: 0.823, artigosObsoletos: 78, coverageChamados: 0.65, topAutores: [...] }` |
| 52 | - | Frontend renderiza dashboard com cards KPI: "📚 1.250 artigos publicados (+12% vs mês anterior)", "⭐ 82.3% score médio de utilidade", "🗑️ 78 artigos obsoletos (revisar ou arquivar)", "🎯 65% coverage de chamados" |
| 53 | - | Frontend renderiza gráfico de linha: "Evolução de Artigos (últimos 30 dias)" com eixo temporal |
| 54 | - | Frontend renderiza tabela ranking: "Top 10 Autores - João Silva (45 artigos, 98% útil), Maria Santos (38 artigos, 95% útil), ..." |

### 5. Fluxos Alternativos

**FA01: Rejeição de Artigo no Workflow**

- No passo 28, ao invés de aprovar, gestor clica em "❌ Rejeitar Nível 1"
- Frontend exige justificativa obrigatória: modal "Rejeitar artigo? Motivo da rejeição (obrigatório): [____]"
- Gestor preenche: "Procedimento não está alinhado com política de segurança corporativa. Revisar item 3.2 antes de republicar"
- Frontend envia `POST /api/base-conhecimento/artigos/{id}/rejeitar` com body: `{ nivelAprovacao: 1, aprovado: false, motivoRejeicao: "...", aprovadorId }`
- Backend atualiza: `niveis[0].Status = StatusNivelAprovacao.Rejeitado; niveis[0].MotivoRejeicao = request.MotivoRejeicao;`
- Backend atualiza artigo: `artigo.Status = StatusArtigo.Rejeitado;`
- Backend atualiza workflow: `workflow.Status = StatusWorkflow.Rejeitado;`
- Backend notifica autor: "Seu artigo foi rejeitado no Nível 1. Motivo: '...' - Revise e resubmeta"
- Frontend exibe badge vermelho: "❌ Rejeitado - Motivo: ..."

**FA02: SLA de Aprovação Vencido - Escalação Automática**

- No passo 19, backend detecta artigo com SLA vencido: `DateTime.UtcNow > workflow.DataSubmissao.AddHours(workflow.Niveis[0].PrazoHoras)`
- Backend executa job Hangfire `MonitorarSLAAprovacaoJob` a cada hora
- Job identifica artigo vencido, atualiza: `niveis[0].SlaVencido = true;`
- Job envia notificação escalada para superior do aprovador: "SLA de aprovação vencido - Artigo #{id} submetido há 30h (prazo: 24h) - Aprovador: João Silva - Aguardando ação"
- Job envia e-mail escalado para gestor sênior
- Frontend exibe badge vermelho no dashboard: "🚨 SLA VENCIDO (6h atrasado)"

**FA03: Configurar Detecção de Artigos Obsoletos**

- No passo 1, gestor acessa `/base-conhecimento/gestao/configuracoes`
- Frontend exibe formulário: "Critérios para Artigos Obsoletos", "Dias sem acesso: [180]", "Score mínimo: [40%]", "Tecnologias descontinuadas: [Windows XP ✖] [Windows Vista ✖] [+ Adicionar]"
- Gestor altera "Dias sem acesso" para 120 (4 meses ao invés de 6)
- Gestor adiciona tecnologia descontinuada: "Office 2010"
- Frontend envia `PUT /api/base-conhecimento/gestao/config-obsolescencia` com body: `{ diasSemAcesso: 120, scoreMinimo: 0.4, tecnologiasDescontinuadas: ["Windows XP", "Windows Vista", "Office 2010"] }`
- Backend atualiza configuração global
- Backend triggera job Hangfire imediatamente: `BackgroundJob.Enqueue(() => DetectarArtigosObsoletosJob.Execute());`
- Job executa, identifica 92 artigos obsoletos (vs 78 com critério anterior de 180 dias)
- Frontend exibe toast: "Configuração salva. 92 artigos obsoletos detectados (job executado)"

**FA04: Visualizar Artigos Obsoletos e Arquivar em Massa**

- No passo 52, gestor clica em card "🗑️ 78 artigos obsoletos"
- Frontend navega para `/base-conhecimento/gestao/obsoletos`
- Frontend envia `GET /api/base-conhecimento/gestao/artigos-obsoletos?clienteId={clienteId}`
- Backend retorna lista de artigos com flags: `{ id, titulo, motivoObsoleto: "Sem acessos desde 15/06/2024", ultimoAcesso, scoreAtual }`
- Frontend renderiza tabela com checkboxes para seleção múltipla
- Gestor seleciona 20 artigos e clica "Arquivar Selecionados"
- Frontend envia `POST /api/base-conhecimento/gestao/arquivar-em-massa` com body: `{ artigoIds: [12, 45, 78, ...], motivo: "Artigos obsoletos - sem acesso em 180+ dias" }`
- Backend atualiza em lote: `UPDATE Artigo SET Status = StatusArtigo.Arquivado, DataArquivamento = @now, MotivoArquivamento = @motivo WHERE Id IN (@ids)`
- Backend retorna HTTP 200 com total arquivado: 20
- Frontend remove artigos da lista, atualiza KPI: "🗑️ 58 artigos obsoletos (20 arquivados)"

**FA05: Dashboard em Tempo Real com SignalR**

- No passo 52, enquanto gestor visualiza dashboard, outro usuário publica novo artigo
- Backend publica evento `ArtigoPublicadoEvent`
- Handler envia notificação SignalR: `_hubContext.Clients.Group($"gestao_{clienteId}").SendAsync("ArtigoPublicado", artigoDto);`
- Frontend (conectado ao hub SignalR) recebe evento em tempo real
- Frontend incrementa KPI "📚 1.250 artigos publicados" para "📚 1.251 artigos publicados" sem reload
- Frontend exibe toast: "Novo artigo publicado por Maria Silva: 'Como configurar MFA'"

### 6. Exceções

**EX01: Usuário Sem Permissão de Gestão**

- No passo 2, frontend valida permissão e detecta que usuário não tem `service-desk:base-conhecimento:gestao`
- Frontend redireciona para `/base-conhecimento` com toast: "Você não tem permissão para acessar Gestão de Conhecimento"
- Se usuário bypassar frontend e chamar API diretamente:
- Backend valida: `User.HasPermission("service-desk:base-conhecimento:gestao")` → false
- Backend retorna HTTP 403 com body: `{ "error": "FORBIDDEN", "message": "Apenas Gestores de Conhecimento podem acessar esta funcionalidade" }`

**EX02: Tentativa de Aprovar Nível Incorreto (Fora de Ordem)**

- No passo 31, usuário tenta aprovar Nível 2 diretamente sem Nível 1 ter sido aprovado
- No passo 33, backend valida: `workflow.NivelAtual == request.NivelAprovacao` → false (workflow está no nível 1, mas request tenta aprovar nível 2)
- Backend retorna HTTP 400 com body: `{ "error": "KB_NIVEL_APROVACAO_INVALIDO", "message": "Este artigo está aguardando aprovação do Nível 1. Você não pode aprovar Nível 2 ainda." }`
- Frontend exibe toast de erro

**EX03: Usuário Sem Papel Correto para Aprovar**

- No passo 33, usuário tenta aprovar nível 1 mas não tem papel "REVISOR_TECNICO" nem "GESTOR_CONHECIMENTO"
- Backend valida: `User.HasRole(workflow.Niveis[0].Papel)` → false
- Backend retorna HTTP 403 com body: `{ "error": "KB_PAPEL_INSUFICIENTE", "message": "Você não tem o papel necessário (REVISOR_TECNICO) para aprovar este nível" }`
- Frontend exibe toast: "Apenas Revisores Técnicos podem aprovar artigos de Segurança"

**EX04: Configuração de Workflow Inválida (SLA Total > 7 dias)**

- No passo 12, gestor tenta configurar workflow com Nível 1: 96h + Nível 2: 120h = 216h total (9 dias)
- Backend valida: `niveisAprovacao.Sum(n => n.PrazoHoras) <= 168` → false (216 > 168)
- Backend retorna HTTP 400 com body: `{ "error": "KB_SLA_WORKFLOW_EXCEDIDO", "message": "SLA total de aprovação não pode exceder 168 horas (7 dias). Total configurado: 216h" }`
- Frontend exibe erro inline: "⚠️ SLA total muito longo (216h). Máximo permitido: 168h (7 dias)"

### 7. Pós-condições

- Workflow de aprovação configurado por categoria (se modificado)
- Artigos aprovados/rejeitados conforme ações do gestor
- Notificações enviadas (autor, próximo aprovador, escalações)
- Artigos publicados automaticamente após última aprovação
- Artigos obsoletos arquivados (se ação em massa executada)
- Métricas de qualidade calculadas e exibidas
- Dashboard atualizado em tempo real via SignalR
- Eventos registrados em auditoria

### 8. Regras de Negócio Aplicáveis

- **RN-KB-070-03**: Workflow de Aprovação por Criticidade (artigos críticos ou categorias sensíveis requerem 2 níveis, SLA configurável, notificações automáticas)
- **RN-KB-070-06**: Detecção de Artigos Obsoletos (critérios: 180 dias sem acesso OU score < 40% OU tecnologia descontinuada, arquivamento automático)
- **RN-KB-070-12**: Notificação de Novos Artigos por Subscrição (triggado ao publicar após aprovação)
- **RN-KB-070-05**: Cálculo Automático de Score de Utilidade (métrica exibida no dashboard)
