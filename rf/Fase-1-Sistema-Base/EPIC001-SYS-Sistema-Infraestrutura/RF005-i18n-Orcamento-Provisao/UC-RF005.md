# UC-RF005 — Casos de Uso Canônicos

**RF:** RF005
**Versão:** 2.0
**Data:** 2025-12-29
**Autor:** Agência ALC - alc.dev.br
**Epic:** EPIC001-SYS-Sistema-Infraestrutura
**Fase:** Fase-1-Sistema-Base

---

## 1. OBJETIVO DESTE DOCUMENTO

Este documento define os **Casos de Uso Canônicos** do RF-005 (Internacionalização).

Cada UC cobre funcionalidades e regras de negócio do sistema moderno, garantindo **cobertura 100% de todas as 22 Regras de Negócio (RN-RF005-001 a RN-RF005-022)**.

---

## 2. SUMÁRIO DE CASOS DE USO

| ID | Nome | Ator Principal | Story Points | RNs Cobertas |
|----|------|----------------|--------------|--------------|
| UC00 | Listar Idiomas Disponíveis | Admin, Tradutor | 3 | RN-RF005-001, RN-RF005-002, RN-RF005-022 |
| UC01 | Adicionar Novo Idioma | Administrador Sistema | 5 | RN-RF005-005, RN-RF005-006, RN-RF005-022 |
| UC02 | Baixar Template de Tradução | Admin, Tradutor | 8 | RN-RF005-008, RN-RF005-009, RN-RF005-011, RN-RF005-021 |
| UC03 | Upload de Traduções | Admin, Tradutor | 13 | RN-RF005-010, RN-RF005-012, RN-RF005-013, RN-RF005-014, RN-RF005-016 |
| UC04 | Ativar/Desativar Idioma | Administrador Sistema | 5 | RN-RF005-001, RN-RF005-007, RN-RF005-019 |
| UC05 | Visualizar Histórico de Versões | Admin, Tradutor | 5 | RN-RF005-015 |
| UC06 | Restaurar Versão Anterior (Rollback) | Administrador Sistema | 8 | RN-RF005-015, RN-RF005-016 |
| UC07 | Validar Integridade de Traduções | Sistema | 8 | RN-RF005-009, RN-RF005-010, RN-RF005-012 |
| UC08 | Tradução Automática via Azure Translator | Administrador Sistema | 13 | RN-RF005-018 |
| UC09 | Exportar Traduções | Admin, Tradutor | 5 | RN-RF005-011 |
| UC10 | Selecionar Idioma (Usuário Final) | Usuário Autenticado | 3 | RN-RF005-002, RN-RF005-003, RN-RF005-004, RN-RF005-017, RN-RF005-020 |

**Total Story Points**: 76
**Cobertura de RNs**: 22/22 (100%) ✅

---

## UC00 — Listar Idiomas Disponíveis

### Objetivo

Permitir que administradores e tradutores visualizem todos os idiomas cadastrados no sistema, com status, progresso de tradução e ações disponíveis.

### Atores

- **Ator Principal**: Administrador Sistema, Tradutor
- **Ator Secundário**: Sistema

### Pré-condições

- Usuário autenticado no sistema
- Permissão: `SYS.I18N.READ`
- Multi-tenancy ativo (ClienteId válido)

### Pós-condições

- Lista de idiomas exibida com informações completas
- Operação registrada em auditoria (READ)

### Fluxo Principal

| Passo | Ação |
|-------|------|
| 1 | Usuário acessa menu **Sistema → Configurações → Internacionalização** |
| 2 | Sistema valida permissão `SYS.I18N.READ` |
| 3 | Sistema busca cache Redis (`i18n:languages:list`) |
| 4 | Se cache HIT: retorna lista do cache (TTL 24h) |
| 5 | Se cache MISS: executa query no banco (SistemaIdiomas) |
| 6 | Sistema calcula progresso de tradução para cada idioma (chaves traduzidas / total) |
| 7 | Sistema renderiza grid com colunas: Bandeira, Nome, Código, Status (Ativo/Inativo), Progresso (%), Ações |
| 8 | Sistema destaca idioma padrão (pt-BR) com ícone de cadeado (não pode ser desativado) |
| 9 | Sistema armazena resultado no cache Redis |
| 10 | Usuário visualiza lista completa de idiomas |

### Fluxos Alternativos

**FA-UC00-001: Filtrar por Status**

- 2a. Usuário seleciona filtro: Ativo / Inativo / Todos
- 2b. Sistema aplica filtro client-side (Angular)
- 2c. Grid atualizado dinamicamente
- 2d. Retorna ao passo 10

**FA-UC00-002: Ordenar por Progresso**

- 2a. Usuário clica em coluna "Progresso"
- 2b. Sistema ordena lista por % (crescente ou decrescente)
- 2c. Grid reordenado
- 2d. Retorna ao passo 10

**FA-UC00-003: Buscar Idioma por Nome ou Código**

- 2a. Usuário digita texto na busca
- 2b. Sistema filtra lista em tempo real
- 2c. Exibe apenas idiomas que correspondem
- 2d. Retorna ao passo 10

### Fluxos de Exceção

**FE-UC00-001: Usuário Sem Permissão**

- 2a. Sistema detecta falta de permissão `SYS.I18N.READ`
- 2b. Sistema retorna HTTP 403 Forbidden
- 2c. Exibe mensagem: "Você não tem permissão para visualizar idiomas"
- 2d. Redireciona para dashboard
- 2e. UC encerrado

**FE-UC00-002: Erro ao Carregar Idiomas**

- 5a. Falha na query ou cache
- 5b. Sistema retorna HTTP 500
- 5c. Exibe mensagem: "Erro ao carregar idiomas. Tente novamente."
- 5d. Permite recarregar página
- 5e. UC encerrado

**FE-UC00-003: Nenhum Idioma Cadastrado**

- 7a. Sistema não encontra idiomas (banco vazio)
- 7b. Exibe estado vazio: "Nenhum idioma cadastrado. Crie o primeiro idioma."
- 7c. Exibe botão [+ Novo Idioma]
- 7d. Retorna ao passo 10

### Regras de Negócio

- **RN-RF005-001**: Idioma padrão pt-BR SEMPRE presente e ativo (não pode ser desativado)
- **RN-RF005-002**: Detecção automática de idioma do usuário (header Accept-Language)
- **RN-RF005-022**: Bandeiras e ícones de idiomas exibidos (emoji ou flag-icons)

---

## UC01 — Adicionar Novo Idioma

### Objetivo

Permitir que administradores criem novos idiomas no sistema, configurando código ISO, bandeira e idioma de referência.

### Atores

- **Ator Principal**: Administrador Sistema
- **Ator Secundário**: Sistema

### Pré-condições

- Usuário autenticado no sistema
- Permissão: `SYS.I18N.MANAGE_LANGUAGES`
- Multi-tenancy ativo (ClienteId válido)

### Pós-condições

- Novo idioma criado com Status: Inativo, Progresso: 0%
- Operação registrada em auditoria (CREATE)
- Cache Redis invalidado (`i18n:languages:*`)

### Fluxo Principal

| Passo | Ação |
|-------|------|
| 1 | Usuário clica em botão [+ Novo Idioma] |
| 2 | Sistema abre modal "Adicionar Novo Idioma" |
| 3 | Sistema carrega dropdown com idiomas ISO 639-1 (200+ idiomas) |
| 4 | Usuário seleciona idioma da lista (ex: Français - fr-FR) |
| 5 | Sistema auto-preenche campos: Código (fr-FR), Nome (Français), Bandeira (🇫🇷) |
| 6 | Usuário confirma ou altera bandeira sugerida |
| 7 | Usuário seleciona idioma de referência para template (padrão: pt-BR) |
| 8 | Usuário clica em [Criar Idioma] |
| 9 | Sistema valida permissão `SYS.I18N.MANAGE_LANGUAGES` |
| 10 | Sistema valida formato do código (Regex: `^[a-z]{2}-[A-Z]{2}$`) |
| 11 | Sistema valida unicidade do código no banco |
| 12 | Sistema executa `POST /api/i18n/languages` |
| 13 | Sistema cria registro em SistemaIdiomas (Status: Inativo, Progresso: 0%) |
| 14 | Sistema registra operação em auditoria (CREATE) |
| 15 | Sistema invalida cache Redis (`i18n:languages:*`) |
| 16 | Sistema exibe mensagem de sucesso: "Idioma criado! Próximo passo: baixe o template de tradução" |
| 17 | Sistema fecha modal e atualiza lista de idiomas |

### Fluxos Alternativos

**FA-UC01-001: Código de Idioma Duplicado**

- 11a. Sistema detecta que código já existe no banco
- 11b. Sistema retorna HTTP 400 Bad Request
- 11c. Exibe mensagem: "Idioma {código} já cadastrado"
- 11d. Destaca campo "Código do Idioma" em vermelho
- 11e. Retorna ao passo 4

**FA-UC01-002: Selecionar Bandeira Customizada**

- 6a. Usuário clica em [Alterar Bandeira]
- 6b. Sistema exibe seletor de bandeiras (flag-icons library)
- 6c. Usuário seleciona bandeira manualmente
- 6d. Retorna ao passo 7

**FA-UC01-003: Cancelar Criação**

- 8a. Usuário clica em [Cancelar]
- 8b. Sistema exibe confirmação: "Descartar criação de idioma?"
- 8c. Usuário confirma
- 8d. Sistema fecha modal sem salvar
- 8e. UC encerrado

### Fluxos de Exceção

**FE-UC01-001: Usuário Sem Permissão**

- 9a. Sistema detecta falta de permissão `SYS.I18N.MANAGE_LANGUAGES`
- 9b. Sistema retorna HTTP 403 Forbidden
- 9c. Exibe mensagem: "Você não tem permissão para criar idiomas"
- 9d. Fecha modal
- 9e. UC encerrado

**FE-UC01-002: Código com Formato Inválido**

- 10a. Sistema detecta código fora do padrão ISO 639-1 + ISO 3166-1
- 10b. Sistema retorna HTTP 400 Bad Request
- 10c. Exibe mensagem: "Código inválido. Formato esperado: xx-XX (ex: pt-BR, en-US)"
- 10d. Destaca campo em vermelho
- 10e. Retorna ao passo 4

**FE-UC01-003: Erro ao Criar Idioma**

- 13a. Falha ao criar registro no banco (constraint, timeout)
- 13b. Sistema retorna HTTP 500
- 13c. Exibe mensagem: "Erro ao criar idioma. Tente novamente."
- 13d. Permite tentar novamente ou cancelar
- 13e. UC encerrado

### Regras de Negócio

- **RN-RF005-005**: Validação de código de idioma (ISO 639-1 + ISO 3166-1, formato: `xx-XX`)
- **RN-RF005-006**: Código de idioma único (unicidade validada no banco)
- **RN-RF005-022**: Bandeiras e ícones de idiomas (auto-sugeridos ou customizáveis)

---

## UC02 — Baixar Template de Tradução

### Objetivo

Permitir que administradores e tradutores baixem arquivos modelo contendo todas as chaves de tradução do sistema em formatos JSON, PO ou XLSX para tradução offline.

### Atores

- **Ator Principal**: Administrador Sistema, Tradutor
- **Ator Secundário**: Sistema

### Pré-condições

- Usuário autenticado no sistema
- Permissão: `SYS.I18N.DOWNLOAD_TEMPLATE`
- Multi-tenancy ativo (ClienteId válido)
- Idioma de destino já criado no sistema

### Pós-condições

- Arquivo template gerado e baixado (formato selecionado)
- Arquivo contém todas as chaves ativas (1.247+)
- Operação registrada em auditoria (DOWNLOAD)

### Fluxo Principal

| Passo | Ação |
|-------|------|
| 1 | Usuário seleciona idioma na lista |
| 2 | Usuário clica em botão [📥 Baixar Template] |
| 3 | Sistema abre modal "Baixar Template de Tradução" |
| 4 | Sistema exibe idioma selecionado (ex: 🇫🇷 Français - fr-FR) |
| 5 | Usuário seleciona tipo: **Template Vazio** OU **Tradução Atual** |
| 6 | Usuário seleciona formato: **JSON** / **PO (Gettext)** / **XLSX (Excel)** |
| 7 | Usuário marca opções: ☑ Comentários/Contexto, ☑ Exemplos, ☑ Traduções de referência |
| 8 | Sistema exibe estatísticas: Total de chaves (1.247), Namespaces (47), Tamanho estimado (~250 KB) |
| 9 | Usuário clica em [📥 Baixar] |
| 10 | Sistema valida permissão `SYS.I18N.DOWNLOAD_TEMPLATE` |
| 11 | Sistema executa `GET /api/i18n/languages/{code}/download?format={format}&type={type}` |
| 12 | Sistema busca todas as chaves ativas em SistemaTraducaoChaves |
| 13 | Se tipo = Current: busca traduções existentes em SistemaTraducoes para o idioma |
| 14 | Sistema busca traduções de referência (pt-BR padrão) |
| 15 | Sistema gera arquivo no formato selecionado (JSON/PO/XLSX) |
| 16 | Sistema inclui metadata, comentários, contexto conforme opções marcadas |
| 17 | Sistema registra download em auditoria (DOWNLOAD) |
| 18 | Sistema envia arquivo para download no navegador |
| 19 | Usuário recebe arquivo: `{idioma}-template.{formato}` |

### Fluxos Alternativos

**FA-UC02-001: Download de Tradução Atual para Atualização**

- 5a. Usuário seleciona "Tradução Atual"
- 5b. Sistema busca traduções já existentes para o idioma
- 5c. Sistema preenche arquivo com traduções atuais (progresso: 85%)
- 5d. Continua no passo 6

**FA-UC02-002: Download em Formato XLSX (Excel)**

- 6a. Usuário seleciona formato XLSX
- 6b. Sistema gera planilha Excel com colunas: Chave | {idioma} | Referência (pt-BR) | Contexto | Categoria
- 6c. Sistema aplica formatação: cabeçalho em negrito, cores, autofit, freeze header
- 6d. Sistema destaca chaves com interpolação em azul itálico
- 6e. Continua no passo 8

**FA-UC02-003: Download em Formato JSON**

- 6a. Usuário seleciona formato JSON
- 6b. Sistema gera estrutura hierárquica (namespaces: common.buttons.save)
- 6c. Sistema adiciona comentários como campos `_comment_{chave}` se opção marcada
- 6d. Sistema adiciona referências como campos `_ref_{chave}` se opção marcada
- 6e. Sistema formata com indentação (pretty-print)
- 6f. Continua no passo 8

**FA-UC02-004: Download em Formato PO (Gettext)**

- 6a. Usuário seleciona formato PO
- 6b. Sistema gera arquivo .po padrão Gettext
- 6c. Sistema adiciona campos msgid (chave) e msgstr (tradução)
- 6d. Sistema inclui metadata e headers
- 6e. Continua no passo 8

### Fluxos de Exceção

**FE-UC02-001: Usuário Sem Permissão**

- 10a. Sistema detecta falta de permissão `SYS.I18N.DOWNLOAD_TEMPLATE`
- 10b. Sistema retorna HTTP 403 Forbidden
- 10c. Exibe mensagem: "Você não tem permissão para baixar templates de tradução"
- 10d. Fecha modal
- 10e. UC encerrado

**FE-UC02-002: Idioma Não Encontrado**

- 12a. Sistema não encontra idioma com código informado
- 12b. Sistema retorna HTTP 404 Not Found
- 12c. Exibe mensagem: "Idioma não encontrado"
- 12d. Retorna ao UC00
- 12e. UC encerrado

**FE-UC02-003: Erro ao Gerar Arquivo**

- 15a. Falha ao gerar arquivo (memória, processamento, timeout)
- 15b. Sistema retorna HTTP 500
- 15c. Exibe mensagem: "Erro ao gerar template. Tente novamente ou selecione outro formato."
- 15d. Permite tentar novamente
- 15e. UC encerrado

### Regras de Negócio

- **RN-RF005-008**: Estrutura hierárquica de chaves (common.buttons.save)
- **RN-RF005-009**: Suporte a interpolação de variáveis ({{username}}, {{count}})
- **RN-RF005-011**: Formatos de arquivo suportados (JSON, PO, XLSX)
- **RN-RF005-021**: Tratamento de pluralização (zero, one, other)

---

## UC03 — Upload de Traduções

### Objetivo

Permitir que administradores e tradutores façam upload de arquivos de tradução preenchidos (JSON, PO ou XLSX), com validação automática de estrutura, interpolações e integridade antes de importar.

### Atores

- **Ator Principal**: Administrador Sistema, Tradutor
- **Ator Secundário**: Sistema

### Pré-condições

- Usuário autenticado no sistema
- Permissão: `SYS.I18N.UPLOAD_TRANSLATION`
- Multi-tenancy ativo (ClienteId válido)
- Arquivo de tradução preenchido disponível
- Idioma de destino já criado no sistema

### Pós-condições

- Traduções importadas e armazenadas no banco
- Progresso de tradução atualizado (ex: 85% → 95%)
- Backup da versão anterior criado (SistemaTraducaoVersoes)
- Nova versão registrada no histórico
- Cache Redis invalidado (`i18n:{lang}:*`)
- Operação registrada em auditoria (UPLOAD)

### Fluxo Principal

| Passo | Ação |
|-------|------|
| 1 | Usuário seleciona idioma de destino na lista |
| 2 | Usuário clica em botão [📤 Atualizar] |
| 3 | Sistema abre modal "Enviar Arquivo de Tradução" |
| 4 | Sistema exibe idioma selecionado (ex: 🇫🇷 Français - fr-FR) |
| 5 | Sistema exibe área de drag & drop para arquivo |
| 6 | Usuário arrasta arquivo OU clica para selecionar |
| 7 | Sistema valida formato do arquivo (extensão: .json / .po / .xlsx) |
| 8 | Sistema valida encoding (UTF-8 obrigatório) |
| 9 | Sistema valida tamanho (máximo 5 MB) |
| 10 | Sistema exibe pré-visualização: nome, tamanho, formato válido ✅ |
| 11 | Usuário marca opções: ☑ Sobrescrever existentes, ☑ Validar interpolações, ☑ Gerar relatório |
| 12 | Usuário clica em [📤 Enviar] |
| 13 | Sistema valida permissão `SYS.I18N.UPLOAD_TRANSLATION` |
| 14 | Sistema executa `POST /api/i18n/languages/{code}/upload` (multipart/form-data) |
| 15 | Sistema cria BACKUP da versão atual em SistemaTraducaoVersoes |
| 16 | Sistema faz parse do arquivo conforme formato (JSON/PO/XLSX) |
| 17 | Sistema valida estrutura de chaves (namespaces corretos) |
| 18 | Sistema valida interpolações: `{{variavel}}` presentes e corretas |
| 19 | Sistema valida chaves obrigatórias presentes |
| 20 | Sistema valida HTML balanceado (`<b>Texto</b>` válido) |
| 21 | Sistema detecta avisos: traduções longas (> 500 chars), traduções idênticas ao pt-BR |
| 22 | Sistema importa traduções para SistemaTraducoes (INSERT/UPDATE) |
| 23 | Sistema calcula novo progresso de tradução (chaves traduzidas / total) |
| 24 | Sistema registra nova versão em SistemaTraducaoVersoes (metadata completa) |
| 25 | Sistema registra operação em auditoria (UPLOAD) |
| 26 | Sistema invalida cache Redis (`i18n:{lang}:*`) |
| 27 | Sistema gera relatório detalhado de importação |
| 28 | Sistema exibe modal de resultado com estatísticas |

### Fluxos Alternativos

**FA-UC03-001: Upload com Avisos Não-Críticos**

- 21a. Sistema detecta avisos (traduções longas, idênticas)
- 21b. Sistema continua importação normalmente
- 21c. Sistema inclui avisos no relatório final
- 21d. Sistema exibe lista de avisos no modal de resultado
- 21e. Permite revisão posterior
- 21f. Continua no passo 22

**FA-UC03-002: Ativar Idioma Automaticamente se 100%**

- 23a. Progresso atinge 100% (todas as chaves traduzidas)
- 23b. Opção "Ativar automaticamente se 100%" estava marcada
- 23c. Sistema ativa idioma automaticamente (Status: Ativo)
- 23d. Sistema invalida cache de idiomas ativos
- 23e. Notifica usuário: "Idioma ativado automaticamente (100% completo)"
- 23f. Continua no passo 24

**FA-UC03-003: Cancelar Upload**

- 12a. Usuário clica em [Cancelar]
- 12b. Sistema descarta arquivo selecionado
- 12c. Sistema fecha modal sem importar
- 12d. UC encerrado

### Fluxos de Exceção

**FE-UC03-001: Usuário Sem Permissão**

- 13a. Sistema detecta falta de permissão `SYS.I18N.UPLOAD_TRANSLATION`
- 13b. Sistema retorna HTTP 403 Forbidden
- 13c. Exibe mensagem: "Você não tem permissão para fazer upload de traduções"
- 13d. Fecha modal
- 13e. UC encerrado

**FE-UC03-002: Arquivo com Formato Inválido**

- 7a. Sistema detecta extensão não suportada (ex: .txt, .doc)
- 7b. Exibe mensagem: "Formato inválido. Formatos aceitos: .json, .po, .xlsx"
- 7c. Permite selecionar outro arquivo
- 7d. Retorna ao passo 6

**FE-UC03-003: Arquivo com Encoding Incorreto**

- 8a. Sistema detecta encoding diferente de UTF-8 (ex: ISO-8859-1)
- 8b. Exibe mensagem: "Encoding inválido. O arquivo deve estar em UTF-8"
- 8c. Permite selecionar outro arquivo
- 8d. Retorna ao passo 6

**FE-UC03-004: Arquivo Muito Grande**

- 9a. Sistema detecta arquivo > 5 MB
- 9b. Exibe mensagem: "Arquivo muito grande (máximo 5 MB)"
- 9c. Permite selecionar outro arquivo
- 9d. Retorna ao passo 6

**FE-UC03-005: Arquivo com Erros Críticos**

- 17a-20a. Sistema detecta erros críticos: chaves inválidas, interpolações incorretas, HTML não balanceado
- 17b. Sistema rejeita importação
- 17c. Sistema retorna HTTP 400 Bad Request
- 17d. Sistema exibe lista detalhada de erros
- 17e. Permite corrigir arquivo e reenviar
- 17f. UC encerrado

**FE-UC03-006: Erro ao Importar Traduções**

- 22a. Falha ao importar no banco (constraint, deadlock, timeout)
- 22b. Sistema executa ROLLBACK da transação
- 22c. Sistema restaura backup criado no passo 15
- 22d. Sistema retorna HTTP 500
- 22e. Exibe mensagem: "Erro ao importar traduções. Nenhuma alteração foi feita."
- 22f. UC encerrado

### Regras de Negócio

- **RN-RF005-010**: Validação de interpolações no upload ({{var}} presentes e corretas)
- **RN-RF005-012**: Validação de HTML balanceado (`<b>Texto</b>`)
- **RN-RF005-013**: Limite de tamanho de tradução (aviso > 500 caracteres)
- **RN-RF005-014**: Detecção de traduções idênticas ao original (aviso, não bloqueante)
- **RN-RF005-016**: Backup automático antes de sobrescrever

---

## UC04 — Ativar/Desativar Idioma

### Objetivo

Permitir que administradores alterem o status de um idioma entre Ativo (disponível para usuários) e Inativo (oculto do seletor), com validações de progresso mínimo e proteção do idioma padrão (pt-BR).

### Atores

- **Ator Principal**: Administrador Sistema
- **Ator Secundário**: Sistema

### Pré-condições

- Usuário autenticado no sistema
- Permissão: `SYS.I18N.MANAGE_LANGUAGES`
- Multi-tenancy ativo (ClienteId válido)
- Idioma já criado no sistema
- Para ativar: Recomendado progresso >= 80% (não bloqueante)

### Pós-condições

**Pós-condições da Ativação**:
- Status do idioma alterado para Ativo
- Idioma aparece no seletor de idiomas para todos os usuários
- Cache Redis invalidado (`i18n:languages:active`)
- Operação registrada em auditoria (UPDATE - Ativação)

**Pós-condições da Desativação**:
- Status do idioma alterado para Inativo
- Idioma removido do seletor de idiomas
- Usuários que estavam usando esse idioma: redirecionados automaticamente para pt-BR
- Cache Redis invalidado (`i18n:languages:active`)
- Operação registrada em auditoria (UPDATE - Desativação)

### Fluxo Principal - Ativar Idioma

| Passo | Ação |
|-------|------|
| 1 | Usuário seleciona idioma inativo na lista |
| 2 | Usuário clica em botão [✅ Ativar] |
| 3 | Sistema valida permissão `SYS.I18N.MANAGE_LANGUAGES` |
| 4 | Sistema verifica progresso de tradução do idioma |
| 5 | Se progresso >= 80%: permite ativação direta |
| 6 | Se progresso < 80%: exibe aviso de incompletude |
| 7 | Usuário confirma ativação (se aviso exibido) |
| 8 | Sistema executa `PUT /api/i18n/languages/{code}/activate` |
| 9 | Sistema atualiza Status para Ativo em SistemaIdiomas |
| 10 | Sistema invalida cache Redis (`i18n:languages:active`) |
| 11 | Sistema registra operação em auditoria (UPDATE - Ativação) |
| 12 | Sistema exibe mensagem de sucesso: "Idioma ativado com sucesso" |
| 13 | Sistema atualiza lista de idiomas |
| 14 | Idioma aparece no seletor de idiomas para todos os usuários |

### Fluxo Principal - Desativar Idioma

| Passo | Ação |
|-------|------|
| 1 | Usuário seleciona idioma ativo na lista |
| 2 | Usuário clica em botão [🔴 Desativar] |
| 3 | Sistema valida permissão `SYS.I18N.MANAGE_LANGUAGES` |
| 4 | Sistema verifica se idioma é pt-BR (padrão do sistema) |
| 5 | Se pt-BR: bloqueia desativação |
| 6 | Se outro idioma: permite desativação |
| 7 | Sistema exibe confirmação: "Desativar idioma {nome}? Usuários usando este idioma serão redirecionados para pt-BR" |
| 8 | Usuário confirma desativação |
| 9 | Sistema executa `PUT /api/i18n/languages/{code}/deactivate` |
| 10 | Sistema atualiza Status para Inativo em SistemaIdiomas |
| 11 | Sistema remove idioma do seletor |
| 12 | Sistema redireciona usuários atualmente usando este idioma para pt-BR (fallback) |
| 13 | Sistema invalida cache Redis (`i18n:languages:active`) |
| 14 | Sistema registra operação em auditoria (UPDATE - Desativação) |
| 15 | Sistema exibe mensagem de sucesso: "Idioma desativado com sucesso" |
| 16 | Sistema atualiza lista de idiomas |

### Fluxos Alternativos

**FA-UC04-001: Ativar com Progresso < 80%**

- 6a. Progresso do idioma é < 80%
- 6b. Sistema exibe aviso: "Idioma com {X}% de tradução. Algumas mensagens aparecerão em português. Ativar mesmo assim?"
- 6c. Usuário confirma ativação
- 6d. Sistema ativa idioma com fallback pt-BR para chaves faltantes
- 6e. Continua no passo 8

**FA-UC04-002: Cancelar Ativação/Desativação**

- 7a/8a. Usuário clica em [Cancelar]
- 7b/8b. Sistema fecha confirmação sem alterar status
- 7c/8c. UC encerrado

### Fluxos de Exceção

**FE-UC04-001: Usuário Sem Permissão**

- 3a. Sistema detecta falta de permissão `SYS.I18N.MANAGE_LANGUAGES`
- 3b. Sistema retorna HTTP 403 Forbidden
- 3c. Exibe mensagem: "Você não tem permissão para ativar/desativar idiomas"
- 3d. UC encerrado

**FE-UC04-002: Tentativa de Desativar pt-BR (Idioma Padrão)**

- 5a. Usuário tenta desativar pt-BR
- 5b. Sistema bloqueia operação
- 5c. Exibe mensagem: "Não é possível desativar o idioma padrão (pt-BR)"
- 5d. Botão [🔴 Desativar] permanece desabilitado
- 5e. UC encerrado

**FE-UC04-003: Idioma Não Encontrado**

- 8a/9a. Sistema não encontra idioma com código informado
- 8b/9b. Sistema retorna HTTP 404 Not Found
- 8c/9c. Exibe mensagem: "Idioma não encontrado"
- 8d/9d. UC encerrado

**FE-UC04-004: Erro ao Atualizar Status**

- 9a/10a. Falha ao atualizar status no banco
- 9b/10b. Sistema retorna HTTP 500
- 9c/10c. Exibe mensagem: "Erro ao atualizar status do idioma. Tente novamente."
- 9d/10d. Permite tentar novamente
- 9e/10e. UC encerrado

### Regras de Negócio

- **RN-RF005-001**: Idioma padrão pt-BR NÃO pode ser desativado (bloqueio absoluto)
- **RN-RF005-007**: Ativação requer >= 80% de tradução (recomendado, não bloqueante)
- **RN-RF005-019**: Permissões RBAC aplicadas (`SYS.I18N.MANAGE_LANGUAGES`)

---

## UC05 — Visualizar Histórico de Versões

### Objetivo

Permitir que administradores e tradutores visualizem o histórico completo de uploads de traduções, incluindo data, usuário, quantidade de chaves e possibilidade de restaurar versões anteriores.

### Atores

- **Ator Principal**: Administrador Sistema, Tradutor
- **Ator Secundário**: Sistema

### Pré-condições

- Usuário autenticado no sistema
- Permissão: `SYS.I18N.READ`
- Multi-tenancy ativo (ClienteId válido)
- Idioma com histórico de uploads

### Pós-condições

- Histórico de versões exibido
- Operação registrada em auditoria (READ)

### Fluxo Principal

| Passo | Ação |
|-------|------|
| 1 | Usuário seleciona idioma na lista |
| 2 | Usuário clica em botão [📜 Histórico] |
| 3 | Sistema abre modal "Histórico de Versões - {idioma}" |
| 4 | Sistema valida permissão `SYS.I18N.READ` |
| 5 | Sistema executa `GET /api/i18n/languages/{code}/versions` |
| 6 | Sistema busca registros em SistemaTraducaoVersoes (ordenado por DataCriacao DESC) |
| 7 | Sistema renderiza grid com colunas: Versão, Data/Hora, Usuário, Chaves Atualizadas, Progresso (%), Ações |
| 8 | Sistema destaca versão atual com badge "ATUAL" |
| 9 | Para cada versão anterior: exibe botão [↶ Restaurar] |
| 10 | Usuário visualiza histórico completo de versões |

### Fluxos Alternativos

**FA-UC05-001: Filtrar por Período**

- 2a. Usuário seleciona filtro de data (Última semana / Último mês / Tudo)
- 2b. Sistema aplica filtro na query
- 2c. Grid atualizado com versões do período
- 2d. Retorna ao passo 10

**FA-UC05-002: Ver Detalhes de uma Versão**

- 10a. Usuário clica em linha da versão
- 10b. Sistema expande linha com detalhes: arquivo original, hash MD5, IP do upload, observações
- 10c. Usuário visualiza metadados completos
- 10d. Retorna ao passo 10

### Fluxos de Exceção

**FE-UC05-001: Usuário Sem Permissão**

- 4a. Sistema detecta falta de permissão `SYS.I18N.READ`
- 4b. Sistema retorna HTTP 403 Forbidden
- 4c. Exibe mensagem: "Você não tem permissão para visualizar histórico de versões"
- 4d. Fecha modal
- 4e. UC encerrado

**FE-UC05-002: Nenhuma Versão Encontrada**

- 7a. Sistema não encontra versões em SistemaTraducaoVersoes
- 7b. Exibe estado vazio: "Nenhuma versão encontrada. Faça o primeiro upload de traduções."
- 7c. Exibe botão [📤 Fazer Upload]
- 7d. Retorna ao passo 10

**FE-UC05-003: Erro ao Carregar Versões**

- 6a. Falha na query ou timeout
- 6b. Sistema retorna HTTP 500
- 6c. Exibe mensagem: "Erro ao carregar histórico. Tente novamente."
- 6d. Permite recarregar
- 6e. UC encerrado

### Regras de Negócio

- **RN-RF005-015**: Versionamento completo de uploads (toda atualização cria nova versão)

---

## UC06 — Restaurar Versão Anterior (Rollback)

### Objetivo

Permitir que administradores restaurem uma versão anterior de traduções, desfazendo uploads recentes em caso de erro ou regressão.

### Atores

- **Ator Principal**: Administrador Sistema
- **Ator Secundário**: Sistema

### Pré-condições

- Usuário autenticado no sistema
- Permissão: `SYS.I18N.MANAGE_TRANSLATIONS`
- Multi-tenancy ativo (ClienteId válido)
- Idioma com histórico de versões (>= 2 versões)

### Pós-condições

- Traduções restauradas para versão anterior
- Progresso de tradução recalculado
- Nova versão de rollback registrada no histórico
- Cache Redis invalidado
- Operação registrada em auditoria (ROLLBACK)

### Fluxo Principal

| Passo | Ação |
|-------|------|
| 1 | Usuário visualiza histórico de versões (UC05) |
| 2 | Usuário seleciona versão anterior desejada |
| 3 | Usuário clica em botão [↶ Restaurar] |
| 4 | Sistema exibe confirmação: "Restaurar versão de {data}? A versão atual será salva no histórico." |
| 5 | Usuário confirma restauração |
| 6 | Sistema valida permissão `SYS.I18N.MANAGE_TRANSLATIONS` |
| 7 | Sistema executa `POST /api/i18n/languages/{code}/versions/{id}/restore` |
| 8 | Sistema cria BACKUP da versão atual (antes de restaurar) |
| 9 | Sistema busca traduções da versão selecionada em SistemaTraducaoVersoes |
| 10 | Sistema substitui traduções atuais em SistemaTraducoes pela versão anterior |
| 11 | Sistema recalcula progresso de tradução (%) |
| 12 | Sistema registra nova versão no histórico (tipo: ROLLBACK) |
| 13 | Sistema invalida cache Redis (`i18n:{lang}:*`) |
| 14 | Sistema registra operação em auditoria (ROLLBACK) com versão restaurada |
| 15 | Sistema exibe mensagem de sucesso: "Versão restaurada com sucesso. Progresso: {X}%" |
| 16 | Sistema fecha modal e atualiza lista de idiomas |

### Fluxos Alternativos

**FA-UC06-001: Cancelar Restauração**

- 5a. Usuário clica em [Cancelar]
- 5b. Sistema fecha confirmação sem restaurar
- 5c. UC encerrado

**FA-UC06-002: Restaurar Versão Muito Antiga**

- 4a. Versão selecionada tem mais de 30 dias
- 4b. Sistema exibe aviso adicional: "Restaurar versão antiga pode causar regressões. Confirma?"
- 4c. Usuário confirma ou cancela
- 4d. Continua no passo 6 ou UC encerrado

### Fluxos de Exceção

**FE-UC06-001: Usuário Sem Permissão**

- 6a. Sistema detecta falta de permissão `SYS.I18N.MANAGE_TRANSLATIONS`
- 6b. Sistema retorna HTTP 403 Forbidden
- 6c. Exibe mensagem: "Você não tem permissão para restaurar versões"
- 6d. UC encerrado

**FE-UC06-002: Versão Não Encontrada**

- 9a. Sistema não encontra dados da versão selecionada
- 9b. Sistema retorna HTTP 404 Not Found
- 9c. Exibe mensagem: "Versão não encontrada ou corrompida"
- 9d. UC encerrado

**FE-UC06-003: Erro ao Restaurar Versão**

- 10a. Falha ao restaurar traduções (constraint, timeout)
- 10b. Sistema executa ROLLBACK da transação
- 10c. Sistema mantém versão atual (nenhuma alteração)
- 10d. Sistema retorna HTTP 500
- 10e. Exibe mensagem: "Erro ao restaurar versão. Nenhuma alteração foi feita."
- 10f. UC encerrado

### Regras de Negócio

- **RN-RF005-015**: Versionamento completo (restauração usa dados históricos)
- **RN-RF005-016**: Backup automático antes de sobrescrever (rollback também cria backup)

---

## UC07 — Validar Integridade de Traduções

### Objetivo

Executar validação automática de integridade em traduções existentes, detectando interpolações incorretas, HTML não balanceado e chaves faltantes.

### Atores

- **Ator Principal**: Sistema (execução automática ou manual)
- **Ator Secundário**: Administrador Sistema

### Pré-condições

- Idioma com traduções cadastradas
- Job agendado no Hangfire OU execução manual

### Pós-condições

- Relatório de integridade gerado
- Avisos e erros detectados e listados
- Operação registrada em auditoria (VALIDATION)

### Fluxo Principal

| Passo | Ação |
|-------|------|
| 1 | Job Hangfire executa diariamente às 03:00 AM |
| 2 | Sistema busca todos os idiomas ativos |
| 3 | Para cada idioma: sistema busca todas as traduções em SistemaTraducoes |
| 4 | Sistema busca traduções de referência (pt-BR) |
| 5 | Sistema executa validações: |
|   | 5a. Interpolações consistentes: `{{var}}` em pt-BR deve ter `{{var}}` em tradução |
|   | 5b. HTML balanceado: `<b>Texto</b>` válido, `<b>Texto` inválido |
|   | 5c. Chaves obrigatórias presentes: common.buttons.*, menu.*, validation.* |
|   | 5d. Detecção de traduções muito longas (> 500 chars) |
|   | 5e. Detecção de traduções idênticas ao pt-BR |
| 6 | Sistema gera relatório com erros e avisos |
| 7 | Se erros críticos detectados: sistema envia email para administradores |
| 8 | Sistema registra relatório em auditoria (VALIDATION) |
| 9 | Sistema armazena relatório em SistemaTraducaoRelatorios |

### Fluxos Alternativos

**FA-UC07-001: Execução Manual pelo Admin**

- 1a. Admin acessa menu "Internacionalização"
- 1b. Admin clica em [🔍 Validar Integridade]
- 1c. Sistema executa validação sob demanda
- 1d. Sistema exibe relatório em modal
- 1e. Continua no passo 2

**FA-UC07-002: Nenhum Erro Detectado**

- 6a. Validação não detecta erros ou avisos
- 6b. Sistema gera relatório com status: "Integridade OK"
- 6c. Sistema NÃO envia email (sem erros)
- 6d. Continua no passo 8

### Fluxos de Exceção

**FE-UC07-001: Erro ao Executar Validação**

- 5a. Falha ao processar validações (timeout, memória)
- 5b. Sistema registra erro em log
- 5c. Sistema tenta novamente em 1 hora (retry)
- 5d. UC encerrado

### Regras de Negócio

- **RN-RF005-009**: Suporte a interpolação de variáveis (validado)
- **RN-RF005-010**: Validação de interpolações no upload (validado diariamente)
- **RN-RF005-012**: Validação de HTML balanceado (validado diariamente)

---

## UC08 — Tradução Automática via Azure Translator

### Objetivo

Permitir que administradores utilizem o Azure Translator API para traduzir automaticamente chaves faltantes, reduzindo esforço manual de tradução.

### Atores

- **Ator Principal**: Administrador Sistema
- **Ator Secundário**: Sistema, Azure Translator API

### Pré-condições

- Usuário autenticado no sistema
- Permissão: `SYS.I18N.AUTO_TRANSLATE`
- Multi-tenancy ativo (ClienteId válido)
- Azure Translator API configurado (chave válida)
- Idioma de destino já criado com progresso < 100%

### Pós-condições

- Traduções automáticas geradas e importadas
- Traduções marcadas como `FoiTraduzidoPorMaquina = True`
- Progresso de tradução atualizado (ex: 60% → 95%)
- Custo estimado registrado
- Operação registrada em auditoria (AUTO_TRANSLATE)
- Cache Redis invalidado

### Fluxo Principal

| Passo | Ação |
|-------|------|
| 1 | Usuário seleciona idioma na lista |
| 2 | Usuário clica em botão [🤖 Traduzir Automaticamente] |
| 3 | Sistema abre modal "Tradução Automática - Azure Translator" |
| 4 | Sistema exibe idioma selecionado (ex: 🇫🇷 Français - fr-FR) |
| 5 | Sistema calcula chaves faltantes: Total (1.247) - Traduzidas (750) = 497 chaves |
| 6 | Sistema estima custo: 497 chaves × 50 chars médio = ~25.000 chars → $0.25 USD |
| 7 | Sistema exibe estimativa: "Traduzir 497 chaves faltantes. Custo estimado: $0.25 USD. Continuar?" |
| 8 | Usuário confirma tradução automática |
| 9 | Sistema valida permissão `SYS.I18N.AUTO_TRANSLATE` |
| 10 | Sistema executa `POST /api/i18n/languages/{code}/auto-translate` |
| 11 | Sistema busca chaves faltantes (pt-BR traduzido, {idioma} vazio) |
| 12 | Sistema divide em lotes de 100 chaves (rate limit Azure: 1M chars/min) |
| 13 | Para cada lote: sistema chama Azure Translator API |
|     | `POST https://api.cognitive.microsofttranslator.com/translate` |
|     | Headers: Subscription-Key, Content-Type: application/json |
|     | Body: [{"Text": "Bem-vindo"}, {"Text": "Salvar"}] |
|     | Params: from=pt-BR, to=fr-FR |
| 14 | Sistema recebe traduções automáticas do Azure |
| 15 | Sistema insere traduções em SistemaTraducoes com `FoiTraduzidoPorMaquina = True` |
| 16 | Sistema recalcula progresso de tradução (%) |
| 17 | Sistema registra custo real em metadata |
| 18 | Sistema invalida cache Redis (`i18n:{lang}:*`) |
| 19 | Sistema registra operação em auditoria (AUTO_TRANSLATE) |
| 20 | Sistema exibe mensagem de sucesso: "497 chaves traduzidas automaticamente. Progresso: 95%. Revisão humana recomendada." |

### Fluxos Alternativos

**FA-UC08-001: Selecionar Apenas Namespace Específico**

- 5a. Usuário marca opção: "Traduzir apenas namespace: common.buttons.*"
- 5b. Sistema filtra chaves faltantes pelo namespace
- 5c. Sistema recalcula estimativa (ex: 20 chaves → $0.02 USD)
- 5d. Continua no passo 7

**FA-UC08-002: Cancelar Tradução Automática**

- 8a. Usuário clica em [Cancelar]
- 8b. Sistema fecha modal sem traduzir
- 8c. UC encerrado

**FA-UC08-003: Custo Excede Limite Configurado**

- 6a. Custo estimado > $5.00 USD (limite configurável)
- 6b. Sistema exibe aviso: "Custo estimado excede limite. Entre em contato com administrador."
- 6c. Sistema bloqueia tradução automática
- 6d. UC encerrado

### Fluxos de Exceção

**FE-UC08-001: Usuário Sem Permissão**

- 9a. Sistema detecta falta de permissão `SYS.I18N.AUTO_TRANSLATE`
- 9b. Sistema retorna HTTP 403 Forbidden
- 9c. Exibe mensagem: "Você não tem permissão para traduzir automaticamente"
- 9d. UC encerrado

**FE-UC08-002: Azure Translator API Não Configurado**

- 13a. Sistema detecta falta de chave de API no appsettings.json
- 13b. Sistema retorna HTTP 500
- 13c. Exibe mensagem: "Azure Translator API não configurado. Configure a chave de API."
- 13d. UC encerrado

**FE-UC08-003: Erro ao Chamar Azure Translator API**

- 13a. API retorna HTTP 401 (chave inválida) OU HTTP 429 (rate limit)
- 13b. Sistema tenta novamente em 60 segundos (retry)
- 13c. Se falha persiste: sistema retorna HTTP 500
- 13d. Exibe mensagem: "Erro ao conectar com Azure Translator. Tente novamente mais tarde."
- 13e. UC encerrado

**FE-UC08-004: Quota Excedida (Azure)**

- 13a. Azure retorna HTTP 403 (quota mensal excedida)
- 13b. Sistema interrompe tradução
- 13c. Exibe mensagem: "Quota de tradução excedida. Aguarde renovação mensal ou aumente o plano."
- 13d. UC encerrado

### Regras de Negócio

- **RN-RF005-018**: Tradução automática via Azure Translator (custo $10/1M chars, marca traduções como automáticas, revisão humana obrigatória)

---

## UC09 — Exportar Traduções

### Objetivo

Permitir que administradores e tradutores exportem traduções atuais de um idioma para formatos JSON, PO ou XLSX, para compartilhamento, backup ou análise.

### Atores

- **Ator Principal**: Administrador Sistema, Tradutor
- **Ator Secundário**: Sistema

### Pré-condições

- Usuário autenticado no sistema
- Permissão: `SYS.I18N.DOWNLOAD_TEMPLATE`
- Multi-tenancy ativo (ClienteId válido)
- Idioma com traduções cadastradas

### Pós-condições

- Arquivo de exportação gerado e baixado
- Operação registrada em auditoria (EXPORT)

### Fluxo Principal

| Passo | Ação |
|-------|------|
| 1 | Usuário seleciona idioma na lista |
| 2 | Usuário clica em botão [📤 Exportar] |
| 3 | Sistema abre modal "Exportar Traduções - {idioma}" |
| 4 | Sistema exibe idioma selecionado (ex: 🇫🇷 Français - fr-FR) |
| 5 | Usuário seleciona formato: JSON / PO / XLSX |
| 6 | Usuário marca opções: ☑ Incluir apenas traduzidas, ☑ Incluir metadata, ☑ Incluir comentários |
| 7 | Usuário clica em [📤 Exportar] |
| 8 | Sistema valida permissão `SYS.I18N.DOWNLOAD_TEMPLATE` |
| 9 | Sistema executa `GET /api/i18n/languages/{code}/export?format={format}` |
| 10 | Sistema busca traduções atuais em SistemaTraducoes |
| 11 | Se opção "Incluir apenas traduzidas": filtra chaves com tradução não vazia |
| 12 | Sistema gera arquivo no formato selecionado (JSON/PO/XLSX) |
| 13 | Se opção "Incluir metadata": adiciona data de exportação, versão, progresso |
| 14 | Sistema registra exportação em auditoria (EXPORT) |
| 15 | Sistema envia arquivo para download no navegador |
| 16 | Usuário recebe arquivo: `{idioma}-export-{data}.{formato}` |

### Fluxos Alternativos

**FA-UC09-001: Exportar Apenas Namespace Específico**

- 6a. Usuário marca opção: "Exportar apenas namespace: common.buttons.*"
- 6b. Sistema filtra traduções pelo namespace
- 6c. Continua no passo 7

**FA-UC09-002: Cancelar Exportação**

- 7a. Usuário clica em [Cancelar]
- 7b. Sistema fecha modal sem exportar
- 7c. UC encerrado

### Fluxos de Exceção

**FE-UC09-001: Usuário Sem Permissão**

- 8a. Sistema detecta falta de permissão `SYS.I18N.DOWNLOAD_TEMPLATE`
- 8b. Sistema retorna HTTP 403 Forbidden
- 8c. Exibe mensagem: "Você não tem permissão para exportar traduções"
- 8d. UC encerrado

**FE-UC09-002: Erro ao Gerar Arquivo**

- 12a. Falha ao gerar arquivo (memória, timeout)
- 12b. Sistema retorna HTTP 500
- 12c. Exibe mensagem: "Erro ao gerar exportação. Tente novamente."
- 12d. Permite tentar novamente
- 12e. UC encerrado

### Regras de Negócio

- **RN-RF005-011**: Formatos de arquivo suportados (JSON, PO, XLSX)

---

## UC10 — Selecionar Idioma (Usuário Final)

### Objetivo

Permitir que usuários finais (qualquer perfil autenticado) selecionem o idioma de sua preferência na interface, com suporte a detecção automática, fallback e cache.

### Atores

- **Ator Principal**: Usuário Autenticado (qualquer perfil)
- **Ator Secundário**: Sistema

### Pré-condições

- Usuário autenticado no sistema
- Pelo menos 1 idioma ativo além de pt-BR

### Pós-condições

- Idioma do usuário atualizado
- Interface recarregada no idioma selecionado
- Preferência salva no banco (Usuarios.IdiomaPreferido)
- Cache Redis carregado com traduções do idioma

### Fluxo Principal

| Passo | Ação |
|-------|------|
| 1 | Usuário faz login no sistema (primeiro acesso) |
| 2 | Sistema detecta idioma preferido automaticamente: |
|   | 2a. Verifica Usuarios.IdiomaPreferido no banco |
|   | 2b. Se vazio: lê header HTTP Accept-Language do navegador |
|   | 2c. Se header vazio: tenta geolocalização via IP (GeoIP) |
|   | 2d. Se tudo vazio: usa pt-BR (idioma padrão) |
| 3 | Sistema valida se idioma detectado está ATIVO |
| 4 | Se ativo: aplica idioma detectado |
| 5 | Se inativo ou não encontrado: aplica pt-BR (fallback) |
| 6 | Sistema carrega traduções do idioma do cache Redis (`i18n:{lang}:*`) |
| 7 | Se cache MISS: busca traduções do banco e popula cache (TTL 24h) |
| 8 | Sistema renderiza interface no idioma selecionado |
| 9 | Usuário visualiza seletor de idiomas no header (bandeira + nome) |
| 10 | Usuário clica no seletor de idiomas |
| 11 | Sistema exibe dropdown com idiomas ativos (bandeira + nome) |
| 12 | Usuário seleciona novo idioma (ex: 🇫🇷 Français) |
| 13 | Sistema executa `PUT /api/users/me/language` (body: {"CodigoIdioma": "fr-FR"}) |
| 14 | Sistema atualiza Usuarios.IdiomaPreferido = "fr-FR" |
| 15 | Sistema invalida cache de sessão do usuário |
| 16 | Sistema carrega traduções do novo idioma do cache Redis |
| 17 | Sistema recarrega interface (navegador atualiza traduções) |
| 18 | Sistema exibe notificação: "Idioma alterado para Français" |
| 19 | Todas as telas do sistema agora exibem textos em francês |

### Fluxos Alternativos

**FA-UC10-001: Idioma com Progresso < 100% (Fallback)**

- 6a. Idioma selecionado tem 85% de tradução (150 chaves faltantes)
- 6b. Sistema carrega traduções disponíveis do idioma
- 6c. Para chaves faltantes: sistema aplica fallback hierárquico:
|     | - Se fr-FR faltando → tenta en-US → se faltando → usa pt-BR (padrão) |
- 6d. Sistema renderiza interface com mix de idiomas (prioridade: fr-FR > en-US > pt-BR)
- 6e. Continua no passo 8

**FA-UC10-002: Lazy Loading de Traduções por Namespace**

- 6a. Sistema carrega apenas namespaces necessários para a tela atual (ex: `common.*`, `menu.*`)
- 6b. Quando usuário navega para nova tela: sistema carrega namespace adicional sob demanda
- 6c. Exemplo: tela de Relatórios → carrega `reports.*` dinamicamente
- 6d. Reduz payload inicial e melhora performance

**FA-UC10-003: Detecção Automática via Browser Header**

- 2b. Header Accept-Language = "fr-FR,fr;q=0.9,en;q=0.8"
- 2c. Sistema parseia header e identifica fr-FR como primeira preferência
- 2d. Sistema verifica se fr-FR está ativo
- 2e. Se ativo: aplica fr-FR automaticamente
- 2f. Continua no passo 6

### Fluxos de Exceção

**FE-UC10-001: Idioma Selecionado Não Está Ativo**

- 13a. Usuário tenta selecionar idioma inativo (não deveria estar no dropdown, mas validação defensiva)
- 13b. Sistema retorna HTTP 400 Bad Request
- 13c. Exibe mensagem: "Idioma selecionado não está disponível"
- 13d. Mantém idioma atual
- 13e. UC encerrado

**FE-UC10-002: Erro ao Atualizar Preferência**

- 14a. Falha ao atualizar Usuarios.IdiomaPreferido no banco
- 14b. Sistema retorna HTTP 500
- 14c. Exibe mensagem: "Erro ao alterar idioma. Tente novamente."
- 14d. Mantém idioma atual
- 14e. UC encerrado

**FE-UC10-003: Cache Redis Indisponível**

- 6a. Redis offline ou timeout
- 6b. Sistema busca traduções diretamente do banco (fallback)
- 6c. Sistema registra aviso em log (cache miss crítico)
- 6d. Performance degradada, mas funcional
- 6e. Continua no passo 8

### Regras de Negócio

- **RN-RF005-002**: Detecção automática de idioma (header Accept-Language, GeoIP, padrão pt-BR)
- **RN-RF005-003**: Fallback em cascata (fr-FR → en-US → pt-BR)
- **RN-RF005-004**: Formatação regional automática (datas, moedas, números conforme idioma selecionado)
- **RN-RF005-017**: Cache Redis para performance (TTL 24h, invalidação automática)
- **RN-RF005-020**: Lazy loading de traduções por namespace (reduz payload inicial)

---

## 4. MATRIZ DE RASTREABILIDADE (22/22 RNs = 100%)

| RN | Título | UCs que Cobrem | Validação |
|----|--------|----------------|-----------|
| RN-RF005-001 | Idioma Padrão Obrigatório (pt-BR) | UC00, UC04 | pt-BR sempre ativo, bloqueio de desativação ✅ |
| RN-RF005-002 | Detecção Automática de Idioma Preferido | UC00, UC10 | Header Accept-Language, GeoIP, fallback ✅ |
| RN-RF005-003 | Fallback em Cascata (Hierárquico) | UC10 | fr-FR → en-US → pt-BR ✅ |
| RN-RF005-004 | Formatação Regional Automática | UC10 | Datas, moedas, números conforme CultureInfo ✅ |
| RN-RF005-005 | Validação de Código de Idioma (ISO) | UC01 | Regex: `^[a-z]{2}-[A-Z]{2}$` ✅ |
| RN-RF005-006 | Código de Idioma Único | UC01 | Unicidade validada no banco ✅ |
| RN-RF005-007 | Ativação Requer >= 80% Tradução | UC04 | Recomendado, não bloqueante, aviso exibido ✅ |
| RN-RF005-008 | Estrutura Hierárquica de Chaves | UC02 | Namespaces: common.buttons.save ✅ |
| RN-RF005-009 | Suporte a Interpolação de Variáveis | UC02, UC07 | `{{username}}`, `{{count}}` ✅ |
| RN-RF005-010 | Validação de Interpolações no Upload | UC03, UC07 | Mesmo número de `{{var}}` em pt-BR e tradução ✅ |
| RN-RF005-011 | Formatos de Arquivo Suportados | UC02, UC03, UC09 | JSON, PO, XLSX ✅ |
| RN-RF005-012 | Validação de HTML Balanceado | UC03, UC07 | `<b>Texto</b>` válido, `<b>Texto` inválido ✅ |
| RN-RF005-013 | Limite de Tamanho de Tradução (Aviso) | UC03 | Aviso > 500 caracteres, não bloqueante ✅ |
| RN-RF005-014 | Detecção de Traduções Idênticas | UC03 | Aviso se tradução = pt-BR, não bloqueante ✅ |
| RN-RF005-015 | Versionamento Completo de Uploads | UC05, UC06 | Toda atualização cria versão em SistemaTraducaoVersoes ✅ |
| RN-RF005-016 | Backup Automático Antes de Sobrescrever | UC03, UC06 | Backup criado antes de upload e rollback ✅ |
| RN-RF005-017 | Cache Redis para Performance | UC10 | Cache `i18n:{lang}:*`, TTL 24h ✅ |
| RN-RF005-018 | Tradução Automática via Azure Translator | UC08 | Custo $10/1M chars, marca FoiTraduzidoPorMaquina ✅ |
| RN-RF005-019 | Permissões RBAC | UC04 | `SYS.I18N.MANAGE_LANGUAGES`, etc ✅ |
| RN-RF005-020 | Lazy Loading de Traduções | UC10 | Carrega namespaces sob demanda ✅ |
| RN-RF005-021 | Tratamento de Pluralização | UC02 | JSON: zero, one, other ✅ |
| RN-RF005-022 | Bandeiras e Ícones de Idiomas | UC00, UC01 | Emoji ou flag-icons library ✅ |

**Cobertura Total**: 22/22 RNs (100%) ✅

---

## 5. OBSERVAÇÕES FINAIS

### Complexidade dos UCs

- **UC03 (Upload de Traduções)**: Muito complexo - validações múltiplas, backup, versionamento
- **UC08 (Tradução Automática)**: Muito complexo - integração externa, custo, retry logic
- **UC06 (Rollback)**: Complexo - restauração de dados históricos com segurança
- **UC07 (Validação de Integridade)**: Complexo - job automático, múltiplas regras de validação

### Integrações Obrigatórias

- **Cache Redis**: UC00, UC03, UC04, UC10 (performance crítica)
- **Auditoria**: Todos os UCs (registro de operações)
- **Permissões RBAC**: UC01, UC03, UC04, UC06, UC08 (segurança)
- **Multi-tenancy**: Todos os UCs (isolamento de dados)

### Dependências Técnicas

- **Azure Translator API**: UC08 (chave de API obrigatória)
- **Hangfire**: UC07 (job agendado diário)
- **Transloco (Angular)**: UC10 (frontend i18n)
- **IStringLocalizer (.NET)**: UC10 (backend i18n)

---

**CHANGELOG**

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 2.0 | 2025-12-29 | Agência ALC - alc.dev.br | 11 UCs completos cobrindo 22/22 RNs (100%) |

---

**Status**: Casos de Uso Completos (100%)
**Próximo Documento**: UC-RF005.yaml (estruturado)
