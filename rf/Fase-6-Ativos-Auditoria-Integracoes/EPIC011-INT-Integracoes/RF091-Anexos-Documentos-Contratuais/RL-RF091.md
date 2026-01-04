# RL-RF091 — Referência ao Legado: Gestão de Anexos e Documentos Contratuais

**Versão:** 1.0
**Data:** 2025-12-31
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF091
**Sistema Legado:** IControlIT VB.NET + ASP.NET Web Forms
**Objetivo:** Documentar o comportamento do sistema legado de gestão de anexos, garantindo rastreabilidade, entendimento histórico e mitigação de riscos durante a migração.

---

## 1. CONTEXTO DO LEGADO

Descreve o cenário geral do sistema legado de gestão de anexos.

- **Arquitetura:** Monolítica ASP.NET Web Forms + VB.NET
- **Linguagem / Stack:** VB.NET, ASP.NET 4.5, SQL Server
- **Banco de Dados:** SQL Server (banco `ic1_legado`)
- **Armazenamento:** File System local (servidor físico)
- **Multi-tenant:** Parcial (coluna ClienteId em algumas tabelas)
- **Auditoria:** Parcial (apenas timestamp e usuário de upload/download)
- **Criptografia:** Inexistente (dados em texto plano)
- **Controle de Acesso:** Verificação no code-behind (VB)
- **Versionamento:** Nenhum (upload sobrescreve arquivo anterior)
- **Scan de Vírus:** Inexistente
- **Assinatura Digital:** Inexistente

---

## 2. TELAS DO LEGADO

### Tela: GerenciarAnexos.aspx

- **Caminho:** `D:\IC2\ic1_legado\IControlIT\Contratos\GerenciarAnexos.aspx`
- **Responsabilidade:** Upload e listagem de anexos associados a contratos

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|------|------|-------------|-------------|
| IdContrato | INT (hidden) | Sim | ID do contrato vinculado |
| FileUpload | File Input | Sim | Controle de upload de arquivo |
| TipoAnexo | Dropdown | Não | Categorias: "Proposta", "Termo", "Aditivo" |
| GridAnexos | GridView | N/A | Lista de anexos existentes com botões Download/Excluir |

#### Comportamentos Implícitos

- **DESTINO: ASSUMIDO** - Validação de tipo de arquivo apenas por extensão (sem verificação de MIME type)
- **DESTINO: SUBSTITUÍDO** - Tamanho máximo controlado por web.config (100MB) sem mensagem clara ao usuário
- **DESTINO: ASSUMIDO** - Arquivo armazenado em `D:\IControlIT\Anexos\{IdContrato}\{NomeArquivo}`
- **DESTINO: DESCARTADO** - Botão "Excluir" remove fisicamente o arquivo (sem soft delete)
- **DESTINO: ASSUMIDO** - Nenhuma auditoria de visualização (apenas upload/download)
- **DESTINO: SUBSTITUÍDO** - Upload com mesmo nome sobrescreve arquivo anterior (sem versionamento)

---

### Tela: VisualizarAnexo.aspx

- **Caminho:** `D:\IC2\ic1_legado\IControlIT\Contratos\VisualizarAnexo.aspx`
- **Responsabilidade:** Visualização de PDF em nova aba

#### Comportamentos Implícitos

- **DESTINO: SUBSTITUÍDO** - Abre arquivo diretamente via URL física (`/Anexos/{IdContrato}/{NomeArquivo}`)
- **DESTINO: SUBSTITUÍDO** - Sem controle de acesso (qualquer usuário com URL pode acessar)
- **DESTINO: SUBSTITUÍDO** - Sem auditoria de visualização
- **DESTINO: DESCARTADO** - Sem watermark ou marca de rastreamento

---

### Tela: DownloadAnexo.aspx

- **Caminho:** `D:\IC2\ic1_legado\IControlIT\Contratos\DownloadAnexo.aspx`
- **Responsabilidade:** Download de arquivo com validação mínima de acesso

#### Comportamentos Implícitos

- **DESTINO: ASSUMIDO** - Valida se usuário pertence ao mesmo ClienteId do contrato
- **DESTINO: ASSUMIDO** - Registra download em `tblHistoricoDownload` (apenas usuário, data, IP)
- **DESTINO: SUBSTITUÍDO** - Sem token temporário (URL permanente se conhecida)
- **DESTINO: DESCARTADO** - Sem watermark em PDFs

---

### Tela: HistoricoAnexos.aspx

- **Caminho:** `D:\IC2\ic1_legado\IControlIT\Contratos\HistoricoAnexos.aspx`
- **Responsabilidade:** Exibir histórico de uploads de um contrato

#### Comportamentos Implícitos

- **DESTINO: ASSUMIDO** - GridView com colunas: NomeArquivo, DataUpload, UsuarioUpload
- **DESTINO: SUBSTITUÍDO** - Sem histórico de versões (apenas último upload)
- **DESTINO: SUBSTITUÍDO** - Sem rastreamento de exclusões

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

| Método | Local | Responsabilidade | Observações | Destino |
|------|-------|------------------|-------------|---------|
| `UploadAnexo(idContrato, arquivo)` | `WSAnexos.asmx.vb` (hipotético) | Upload de arquivo | Salva em file system, registra em banco | **SUBSTITUÍDO** (agora usa Azure Blob + Command) |
| `ListarAnexosPorContrato(idContrato)` | `WSAnexos.asmx.vb` | Listar documentos | Retorna DataTable com anexos | **SUBSTITUÍDO** (agora Query com DTO) |
| `DownloadAnexo(idAnexo)` | `WSAnexos.asmx.vb` | Download com acesso local | Retorna byte[] do arquivo | **SUBSTITUÍDO** (agora SAS token do Azure) |
| `ExcluirAnexo(idAnexo)` | `WSAnexos.asmx.vb` | Exclusão lógica | Marca Ativo=0 | **ASSUMIDO** (soft delete mantido) |
| `GetHistoricoDownloads(idAnexo)` | `WSAnexos.asmx.vb` | Auditoria de downloads | Retorna histórico simples | **SUBSTITUÍDO** (auditoria completa com metadados) |

---

## 4. TABELAS LEGADAS

| Tabela | Finalidade | Problemas Identificados | Destino |
|-------|------------|-------------------------|---------|
| `tblAnexos` | Armazenar metadados de anexos | Caminho físico hardcoded, sem versionamento, sem hash de integridade | **SUBSTITUÍDO** (nova tabela `DocumentAttachment` com Azure Blob) |
| `tblCategoriaDocumento` | Categorias de documento | Sem controle de obrigatoriedade por tipo de contrato | **ASSUMIDO** (estrutura mantida com melhorias) |
| `tblHistoricoDownload` | Auditoria de downloads | Dados mínimos (sem User-Agent, sem geolocalização) | **SUBSTITUÍDO** (nova tabela `AuditLog` completa) |

### DDL Legado - tblAnexos

```sql
CREATE TABLE [dbo].[tblAnexos](
    [IdAnexo] [int] IDENTITY(1,1) NOT NULL,
    [IdContrato] [int] NOT NULL,
    [NomeArquivo] [varchar](255) NOT NULL,
    [CaminhoArquivo] [varchar](500) NOT NULL,  -- PROBLEMA: Path físico
    [TipoAnexo] [varchar](50) NULL,
    [DataUpload] [datetime] NOT NULL,
    [UsuarioUpload] [varchar](100) NOT NULL,  -- PROBLEMA: Apenas nome, sem GUID
    [Ativo] [bit] DEFAULT (1),
    CONSTRAINT [PK_tblAnexos] PRIMARY KEY CLUSTERED ([IdAnexo] ASC)
);
```

**Destino:** **SUBSTITUÍDO** - Nova tabela `DocumentAttachment` com:
- BlobUri (Azure Blob Storage)
- Sha256Hash (integridade)
- VersionNumber (versionamento)
- ClienteId (multi-tenancy)
- UploadedBy (GUID do usuário)

---

### DDL Legado - tblCategoriaDocumento

```sql
CREATE TABLE [dbo].[tblCategoriaDocumento](
    [IdCategoria] [int] IDENTITY(1,1) NOT NULL,
    [NomeCategoria] [varchar](100) NOT NULL,
    [Descricao] [text] NULL,
    [Obrigatoria] [bit] DEFAULT (0),  -- PROBLEMA: Flag global, não por tipo de contrato
    CONSTRAINT [PK_tblCategoriaDocumento] PRIMARY KEY CLUSTERED ([IdCategoria] ASC)
);
```

**Destino:** **ASSUMIDO** - Estrutura mantida com adição de:
- FK para TipoContrato (obrigatoriedade contextual)
- ClienteId (multi-tenancy)

---

### DDL Legado - tblHistoricoDownload

```sql
CREATE TABLE [dbo].[tblHistoricoDownload](
    [IdHistorico] [int] IDENTITY(1,1) NOT NULL,
    [IdAnexo] [int] NOT NULL,
    [UsuarioDownload] [varchar](100) NOT NULL,
    [DataDownload] [datetime] NOT NULL,
    [IPAddress] [varchar](15) NULL,  -- PROBLEMA: Apenas IP, sem User-Agent
    CONSTRAINT [PK_tblHistoricoDownload] PRIMARY KEY CLUSTERED ([IdHistorico] ASC),
    CONSTRAINT [FK_HistoricoDownload_Anexos] FOREIGN KEY ([IdAnexo])
        REFERENCES [dbo].[tblAnexos]([IdAnexo])
);
```

**Destino:** **SUBSTITUÍDO** - Nova tabela `AuditLog` com:
- Action (DOC_UPLOAD, DOC_DOWNLOAD, DOC_DELETE, DOC_SIGN)
- UserId (GUID)
- Timestamp (UTC)
- IpAddress, UserAgent, Geolocalização
- Metadata (JSON com dados contextuais)

---

## 5. STORED PROCEDURES LEGADAS

| Procedure | Descrição | Problemas | Destino |
|-----------|-----------|----------|---------|
| `sp_UploadAnexo` | Registra novo anexo no banco | Sem validação de tipo, sem hash | **SUBSTITUÍDO** (Command `UploadDocumentCommand`) |
| `sp_ListarAnexosPorContrato` | Lista anexos de um contrato | Queries N+1, sem paginação | **SUBSTITUÍDO** (Query `GetDocumentsByContractQuery`) |
| `sp_ExcluirAnexo` | Marca anexo como inativo | Não remove arquivo físico (orphan data) | **SUBSTITUÍDO** (Command `DeleteDocumentCommand`) |
| `sp_AtualizarStatusAnexo` | Atualiza status (ativo/inativo) | Lógica duplicada em code-behind | **SUBSTITUÍDO** (integrado em handlers CQRS) |

---

## 6. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

Liste regras que não estavam documentadas formalmente.

- **RL-RN-001**: Validação de tipo de arquivo apenas por extensão (.pdf, .docx, .xlsx permitidos)
  - **DESTINO: SUBSTITUÍDO** - Validação dupla (extensão + MIME type) em RN-RF091-001

- **RL-RN-002**: Tamanho máximo de arquivo controlado por web.config (100MB)
  - **DESTINO: SUBSTITUÍDO** - Limite de 50MB em RN-RF091-002

- **RL-RN-003**: Upload com mesmo nome sobrescreve arquivo anterior (sem versionamento)
  - **DESTINO: SUBSTITUÍDO** - Versionamento imutável em RN-RF091-005

- **RL-RN-004**: Exclusão marca Ativo=0 mas não remove arquivo físico
  - **DESTINO: ASSUMIDO** - Soft delete mantido, mas arquivo removido do Azure Blob (opcional)

- **RL-RN-005**: Acesso validado apenas por ClienteId (sem RBAC granular)
  - **DESTINO: SUBSTITUÍDO** - RBAC completo + políticas temporárias em RN-RF091-007

- **RL-RN-006**: Histórico de download registra apenas IP e timestamp
  - **DESTINO: SUBSTITUÍDO** - Auditoria completa em RN-RF091-013

- **RL-RN-007**: Categorias de documento são globais (não contextuais por tipo de contrato)
  - **DESTINO: ASSUMIDO** - Categorias contextuais por tipo de contrato em RN-RF091-012

- **RL-RN-008**: Sem scan de antivírus em arquivos uploadados
  - **DESTINO: SUBSTITUÍDO** - Scan ClamAV obrigatório em RN-RF091-003

- **RL-RN-009**: Sem criptografia de arquivos em repouso
  - **DESTINO: SUBSTITUÍDO** - AES-256 em Azure Blob em RN-RF091-006

- **RL-RN-010**: Sem OCR ou busca full-text em documentos
  - **DESTINO: SUBSTITUÍDO** - OCR + Elasticsearch em RN-RF091-010

---

## 7. GAP ANALYSIS (LEGADO x RF MODERNO)

| Item | Legado | RF Moderno (RF091 v2.0) | Observação |
|-----|--------|------------|------------|
| **Armazenamento** | File System local | Azure Blob Storage com AES-256 | Migração requer script de upload para blob |
| **Validação de Tipo** | Apenas extensão | Extensão + MIME type (dupla) | Maior segurança contra bypass |
| **Tamanho Máximo** | 100MB (web.config) | 50MB (validação explícita) | Redução para otimizar performance |
| **Scan de Vírus** | Inexistente | ClamAV obrigatório | Nova dependência de infraestrutura |
| **Versionamento** | Sobrescreve arquivo | Versionamento imutável | Requer nova estrutura de dados |
| **Controle de Acesso** | Verificação VB (code-behind) | RBAC + Policies (centralizado) | Maior granularidade e auditoria |
| **Download** | URL física permanente | SAS token temporário (15 min) | Maior segurança e rastreabilidade |
| **Watermark** | Inexistente | Watermark visual em PDFs | Nova funcionalidade |
| **OCR** | Inexistente | Azure Cognitive Services | Nova integração |
| **Assinatura Digital** | Inexistente | DocuSign integrado | Nova integração |
| **Auditoria** | Parcial (IP + timestamp) | Completa (UserId, IP, User-Agent, Metadata) | Conformidade LGPD |
| **Busca** | Like em banco de dados | Elasticsearch full-text | Performance e relevância |

---

## 8. DECISÕES DE MODERNIZAÇÃO

### Decisão 1: Migrar de File System para Azure Blob Storage

- **Motivo:** Escalabilidade, redundância geográfica, criptografia nativa, integração com SAS tokens
- **Impacto:** ALTO - Requer script de migração de arquivos existentes, alteração de todas queries
- **Mitigação:** Script de migração batch com validação de integridade (SHA-256) antes/depois

---

### Decisão 2: Reduzir Tamanho Máximo de 100MB para 50MB

- **Motivo:** Otimizar tempo de upload/download, reduzir custos de armazenamento, melhorar performance de visualizadores
- **Impacto:** MÉDIO - Arquivos > 50MB no legado precisarão ser reprocessados ou mantidos como exceção
- **Mitigação:** Análise prévia de tamanhos de arquivo existentes, notificação de usuários sobre novo limite

---

### Decisão 3: Introduzir Versionamento Imutável

- **Motivo:** Atender requisitos de auditoria, permitir rollback, preservar histórico forense
- **Impacto:** MÉDIO - Aumento de armazenamento (múltiplas versões), nova estrutura de dados
- **Mitigação:** Policy de retenção (ex: manter apenas 5 versões mais recentes, ou versões dos últimos 2 anos)

---

### Decisão 4: Implementar Scan de Antivírus Obrigatório (ClamAV)

- **Motivo:** Segurança da informação, conformidade ISO 27001, prevenir distribuição de malware
- **Impacto:** ALTO - Nova dependência de infraestrutura, aumento de tempo de upload
- **Mitigação:** ClamAV em container Docker, processamento assíncrono, cache de assinaturas de vírus

---

### Decisão 5: Substituir URLs Físicas por SAS Tokens Temporários

- **Motivo:** Segurança (URLs não podem ser compartilhadas indefinidamente), auditoria de cada acesso
- **Impacto:** MÉDIO - Frontend precisa requisitar novo token a cada 15 minutos, maior complexidade
- **Mitigação:** Implementar refresh automático de token no frontend antes de expiração

---

### Decisão 6: Integrar OCR para Busca Full-Text

- **Motivo:** Melhorar experiência de busca, permitir localizar documentos por conteúdo
- **Impacto:** MÉDIO - Custo de Azure Cognitive Services, processamento assíncrono, índice Elasticsearch
- **Mitigação:** OCR apenas para documentos novos (não retroativo), feature flag para desabilitar se custo for alto

---

### Decisão 7: Integrar DocuSign para Assinatura Digital

- **Motivo:** Validade legal de assinaturas (Lei 14.063/2020), evidência forense
- **Impacto:** ALTO - Nova integração complexa, custo de licença DocuSign, webhook handling
- **Mitigação:** Feature flag para habilitar apenas para clientes que contratarem DocuSign

---

## 9. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Mitigação |
|------|---------|-----------|
| **Perda de arquivos durante migração para Azure Blob** | CRÍTICO | Script de migração com validação SHA-256 antes/depois, backup completo do file system |
| **Arquivos > 50MB existentes não podem ser migrados** | MÉDIO | Análise prévia, notificação de usuários, exceção temporária para arquivos legados |
| **Quebra de URLs físicas existentes (bookmarks, documentação)** | MÉDIO | Manter redirecionamento temporário (6 meses) de URLs antigas para geração de SAS token |
| **Custo de OCR e DocuSign inviável para alguns clientes** | MÉDIO | Feature flags para habilitar/desabilitar por cliente, planos diferenciados |
| **Processamento de OCR muito lento (gargalo)** | MÉDIO | Processamento assíncrono com fila (Azure Queue), retry automático em falhas |
| **ClamAV bloqueia upload legítimo (falso positivo)** | BAIXO | Processo de quarentena revisável, whitelist de hashes conhecidos |
| **Elasticsearch fora de sincronia com banco** | MÉDIO | Job noturno de reindexação completa, monitoramento de consistência |
| **Versionamento consome muito armazenamento** | MÉDIO | Policy de retenção configurável, compressão de versões antigas |

---

## 10. RASTREABILIDADE

### Elementos Legado → RF Moderno

| Elemento Legado | Referência RF091 v2.0 |
|----------------|---------------|
| `tblAnexos.CaminhoArquivo` | RN-RF091-006 (Azure Blob Storage) |
| `GerenciarAnexos.aspx` (upload) | RN-RF091-001, RN-RF091-002, RN-RF091-003 |
| `DownloadAnexo.aspx` | RN-RF091-008 (SAS token), RN-RF091-009 (watermark) |
| `tblHistoricoDownload` | RN-RF091-013 (auditoria completa) |
| `sp_UploadAnexo` | RN-RF091-001 a RN-RF091-006 (processo de upload moderno) |
| `sp_ListarAnexosPorContrato` | RN-RF091-014 (isolamento multi-tenant) |
| Validação de extensão apenas | RN-RF091-001 (validação dupla) |
| Upload sobrescreve versão | RN-RF091-005 (versionamento imutável) |
| Sem scan de vírus | RN-RF091-003 (ClamAV obrigatório) |
| Sem OCR/busca | RN-RF091-010 (OCR + Elasticsearch) |
| Sem assinatura digital | RN-RF091-011 (DocuSign) |

---

### Stored Procedures → Commands/Queries

| Stored Procedure Legada | Command/Query Moderno |
|------------------------|----------------------|
| `sp_UploadAnexo` | `UploadDocumentCommand` + `UploadDocumentCommandHandler` |
| `sp_ListarAnexosPorContrato` | `GetDocumentsByContractQuery` + `GetDocumentsByContractQueryHandler` |
| `sp_ExcluirAnexo` | `DeleteDocumentCommand` + `DeleteDocumentCommandHandler` |
| `sp_AtualizarStatusAnexo` | Integrado em `UpdateDocumentCommand` |
| `sp_GetHistoricoDownloads` | `GetDocumentAuditLogQuery` + `GetDocumentAuditLogQueryHandler` |

---

### Telas Legadas → Endpoints REST API

| Tela Legada | Endpoint Moderno |
|------------|-----------------|
| `GerenciarAnexos.aspx` (upload) | `POST /api/documents/upload` |
| `GerenciarAnexos.aspx` (listagem) | `GET /api/documents?contractId={id}` |
| `VisualizarAnexo.aspx` | `POST /api/documents/{id}/download-url` (SAS token) |
| `DownloadAnexo.aspx` | `POST /api/documents/{id}/download-url` |
| `HistoricoAnexos.aspx` | `GET /api/documents/{id}/audit-log` |

---

## 11. CÓDIGO LEGADO REPRESENTATIVO

### Exemplo: Upload com Validação Mínima (VB.NET)

```vb
' Arquivo: GerenciarAnexos.aspx.vb
' DESTINO: SUBSTITUÍDO (lógica migrada para UploadDocumentCommand)

Protected Sub btnUpload_Click(sender As Object, e As EventArgs) Handles btnUpload.Click
    If FileUpload1.HasFile Then
        Dim fileName As String = Path.GetFileName(FileUpload1.FileName)
        Dim extension As String = Path.GetExtension(fileName).ToLower()

        ' PROBLEMA: Validação apenas por extensão (sem MIME type)
        If extension = ".pdf" Or extension = ".docx" Or extension = ".xlsx" Then
            Dim savePath As String = Server.MapPath("~/Anexos/" & IdContrato & "/" & fileName)

            ' PROBLEMA: Cria diretório se não existir (sem controle de permissões)
            If Not Directory.Exists(Path.GetDirectoryName(savePath)) Then
                Directory.CreateDirectory(Path.GetDirectoryName(savePath))
            End If

            ' PROBLEMA: Sobrescreve arquivo se já existe (sem versionamento)
            FileUpload1.SaveAs(savePath)

            ' Registra no banco
            Dim cmd As New SqlCommand("INSERT INTO tblAnexos (IdContrato, NomeArquivo, CaminhoArquivo, DataUpload, UsuarioUpload) VALUES (@IdContrato, @Nome, @Caminho, GETDATE(), @Usuario)", conn)
            cmd.Parameters.AddWithValue("@IdContrato", IdContrato)
            cmd.Parameters.AddWithValue("@Nome", fileName)
            cmd.Parameters.AddWithValue("@Caminho", savePath)  ' PROBLEMA: Path absoluto hardcoded
            cmd.Parameters.AddWithValue("@Usuario", Session("UserName"))
            cmd.ExecuteNonQuery()

            lblMensagem.Text = "Arquivo enviado com sucesso!"
        Else
            lblMensagem.Text = "Tipo de arquivo não permitido!"
        End If
    End If
End Sub
```

**Problemas Identificados:**
1. Validação apenas por extensão (bypass fácil renomeando .exe para .pdf)
2. Path físico absoluto (não portável, não escalável)
3. Sem scan de antivírus
4. Sem versionamento (sobrescreve arquivo)
5. Sem hash de integridade
6. Sem auditoria completa (apenas nome de usuário, sem IP, sem User-Agent)

**DESTINO: SUBSTITUÍDO** - Toda lógica migrada para `UploadDocumentCommandHandler` com:
- Validação dupla (extensão + MIME type)
- Armazenamento em Azure Blob Storage
- Scan ClamAV obrigatório
- Versionamento imutável
- Hash SHA-256
- Auditoria completa (RN-RF091-013)

---

### Exemplo: Download sem Controle de Acesso Granular (VB.NET)

```vb
' Arquivo: DownloadAnexo.aspx.vb
' DESTINO: SUBSTITUÍDO (lógica migrada para GenerateSecureDownloadUrlCommand)

Protected Sub Page_Load(sender As Object, e As EventArgs) Handles Me.Load
    Dim idAnexo As Integer = Request.QueryString("id")

    ' Busca anexo no banco
    Dim cmd As New SqlCommand("SELECT CaminhoArquivo, NomeArquivo FROM tblAnexos WHERE IdAnexo = @Id", conn)
    cmd.Parameters.AddWithValue("@Id", idAnexo)
    Dim dr As SqlDataReader = cmd.ExecuteReader()

    If dr.Read() Then
        Dim filePath As String = dr("CaminhoArquivo").ToString()
        Dim fileName As String = dr("NomeArquivo").ToString()
        dr.Close()

        ' PROBLEMA: Sem validação de permissão (qualquer usuário autenticado pode baixar)
        ' PROBLEMA: URL permanente (não expira)
        ' PROBLEMA: Sem watermark

        ' Registra download (auditoria mínima)
        Dim cmdLog As New SqlCommand("INSERT INTO tblHistoricoDownload (IdAnexo, UsuarioDownload, DataDownload, IPAddress) VALUES (@Id, @Usuario, GETDATE(), @IP)", conn)
        cmdLog.Parameters.AddWithValue("@Id", idAnexo)
        cmdLog.Parameters.AddWithValue("@Usuario", Session("UserName"))
        cmdLog.Parameters.AddWithValue("@IP", Request.UserHostAddress)
        cmdLog.ExecuteNonQuery()

        ' Força download
        Response.ContentType = "application/octet-stream"
        Response.AppendHeader("Content-Disposition", "attachment; filename=" & fileName)
        Response.TransmitFile(filePath)
        Response.End()
    End If
End Sub
```

**Problemas Identificados:**
1. Sem validação de permissão RBAC (apenas autenticação)
2. Sem isolamento multi-tenant (usuário de ClienteId A pode acessar anexo de ClienteId B se conhecer ID)
3. URL permanente (não expira, pode ser compartilhada indefinidamente)
4. Sem watermark em PDFs
5. Auditoria mínima (sem User-Agent, sem geolocalização)
6. Sem verificação de integridade (hash)

**DESTINO: SUBSTITUÍDO** - Toda lógica migrada para `GenerateSecureDownloadUrlCommandHandler` com:
- Validação RBAC completa (RN-RF091-007)
- Isolamento multi-tenant (RN-RF091-014)
- SAS token temporário (15 min) (RN-RF091-008)
- Watermark em PDFs (RN-RF091-009)
- Auditoria completa (RN-RF091-013)
- Verificação de integridade via hash (RN-RF091-004)

---

## 12. COMPARAÇÃO LEGADO vs MODERNO (TABELAS)

### tblAnexos (Legado) vs DocumentAttachment (Moderno)

| Campo Legado | Campo Moderno | Observação |
|-------------|--------------|------------|
| IdAnexo (INT IDENTITY) | Id (GUID) | GUID para evitar colisão em sistemas distribuídos |
| IdContrato (INT) | ContractId (GUID) | Migração de INT para GUID |
| NomeArquivo (VARCHAR 255) | FileName (NVARCHAR 500) | Suporte a Unicode, tamanho maior |
| CaminhoArquivo (VARCHAR 500) | BlobUri (NVARCHAR 1000) | Azure Blob URI em vez de path físico |
| - | BlobKey (NVARCHAR 500) | Chave interna do blob (ex: `contracts/{contractId}/{documentId}/v{version}`) |
| TipoAnexo (VARCHAR 50) | DocumentCategoryId (GUID) | FK para tabela DocumentCategory |
| - | MimeType (VARCHAR 100) | Tipo MIME armazenado |
| - | FileSize (BIGINT) | Tamanho em bytes |
| - | Sha256Hash (VARCHAR 64) | Hash para integridade |
| - | VersionNumber (INT) | Versionamento imutável |
| - | IsCurrentVersion (BIT) | Flag de versão atual |
| DataUpload (DATETIME) | UploadedAt (DATETIME2) | Precisão de milissegundos |
| UsuarioUpload (VARCHAR 100) | UploadedBy (GUID) | FK para Users |
| Ativo (BIT) | IsDeleted (BIT) | Soft delete (invertido para clareza) |
| - | ClienteId (GUID) | Multi-tenancy obrigatório |
| - | CreatedAt (DATETIME2) | Auditoria automática |
| - | UpdatedAt (DATETIME2) | Auditoria automática |

---

## 13. SCRIPT DE MIGRAÇÃO DE DADOS (EXEMPLO)

```sql
-- Script de migração de tblAnexos (legado) para DocumentAttachment (moderno)
-- EXECUTAR EM AMBIENTE DE STAGING ANTES DE PRODUÇÃO

-- Passo 1: Criar mapeamento de IDs (INT legado → GUID moderno)
CREATE TABLE #MapeamentoContratos (
    IdContratoLegado INT,
    ContractIdModerno UNIQUEIDENTIFIER
);

INSERT INTO #MapeamentoContratos
SELECT c_legado.IdContrato, c_moderno.Id
FROM ic1_legado.dbo.tblContratos c_legado
INNER JOIN IControlIT_Modern.dbo.Contracts c_moderno
    ON c_legado.NumeroContrato = c_moderno.Number;

-- Passo 2: Migrar anexos (metadados apenas, arquivos migrados separadamente via script PowerShell)
INSERT INTO IControlIT_Modern.dbo.DocumentAttachments (
    Id, ContractId, DocumentCategoryId, FileName, BlobUri, BlobKey,
    MimeType, FileSize, Sha256Hash, VersionNumber, IsCurrentVersion,
    UploadedAt, UploadedBy, IsDeleted, ClienteId, CreatedAt, UpdatedAt
)
SELECT
    NEWID() AS Id,
    m.ContractIdModerno AS ContractId,
    cat.Id AS DocumentCategoryId,  -- Assumindo que categorias foram migradas previamente
    a.NomeArquivo AS FileName,
    'https://icontrolit.blob.core.windows.net/documents/' + CAST(NEWID() AS VARCHAR(36)) + '.dat' AS BlobUri,  -- URI temporária, atualizada após upload
    'contracts/' + CAST(m.ContractIdModerno AS VARCHAR(36)) + '/' + a.NomeArquivo AS BlobKey,
    CASE
        WHEN LOWER(RIGHT(a.NomeArquivo, 4)) = '.pdf' THEN 'application/pdf'
        WHEN LOWER(RIGHT(a.NomeArquivo, 5)) = '.docx' THEN 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        WHEN LOWER(RIGHT(a.NomeArquivo, 5)) = '.xlsx' THEN 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        ELSE 'application/octet-stream'
    END AS MimeType,
    0 AS FileSize,  -- Será atualizado após upload para Azure Blob
    '' AS Sha256Hash,  -- Será calculado após upload
    1 AS VersionNumber,  -- Primeira versão (legado não tem versionamento)
    1 AS IsCurrentVersion,
    a.DataUpload AS UploadedAt,
    u.Id AS UploadedBy,  -- FK para Users (assumindo que usuários foram migrados)
    CASE WHEN a.Ativo = 0 THEN 1 ELSE 0 END AS IsDeleted,
    c.ClienteId AS ClienteId,  -- Multi-tenancy
    GETUTCDATE() AS CreatedAt,
    GETUTCDATE() AS UpdatedAt
FROM ic1_legado.dbo.tblAnexos a
INNER JOIN #MapeamentoContratos m ON a.IdContrato = m.IdContratoLegado
INNER JOIN IControlIT_Modern.dbo.DocumentCategories cat ON a.TipoAnexo = cat.Name  -- Mapeamento por nome
LEFT JOIN IControlIT_Modern.dbo.Contracts c ON m.ContractIdModerno = c.Id
LEFT JOIN IControlIT_Modern.dbo.Users u ON a.UsuarioUpload = u.Email  -- Mapeamento por email
WHERE a.NomeArquivo IS NOT NULL;

-- Passo 3: Migrar histórico de downloads
INSERT INTO IControlIT_Modern.dbo.AuditLogs (
    Id, ClienteId, UserId, UserEmail, Action, DocumentId, Timestamp, IpAddress, UserAgent, Description
)
SELECT
    NEWID() AS Id,
    c.ClienteId AS ClienteId,
    u.Id AS UserId,
    u.Email AS UserEmail,
    'DOC_DOWNLOAD' AS Action,
    da.Id AS DocumentId,  -- FK para DocumentAttachments
    h.DataDownload AS Timestamp,
    h.IPAddress AS IpAddress,
    'Legado - User-Agent não disponível' AS UserAgent,
    'Download migrado do sistema legado' AS Description
FROM ic1_legado.dbo.tblHistoricoDownload h
INNER JOIN ic1_legado.dbo.tblAnexos a ON h.IdAnexo = a.IdAnexo
INNER JOIN #MapeamentoContratos m ON a.IdContrato = m.IdContratoLegado
INNER JOIN IControlIT_Modern.dbo.DocumentAttachments da ON a.NomeArquivo = da.FileName AND m.ContractIdModerno = da.ContractId
INNER JOIN IControlIT_Modern.dbo.Users u ON h.UsuarioDownload = u.Email
INNER JOIN IControlIT_Modern.dbo.Contracts c ON m.ContractIdModerno = c.Id;

-- Limpeza
DROP TABLE #MapeamentoContratos;
```

**NOTA:** Arquivos físicos devem ser migrados separadamente via script PowerShell que:
1. Lê arquivo do file system legado (`D:\IControlIT\Anexos\`)
2. Calcula SHA-256
3. Faz upload para Azure Blob Storage
4. Atualiza `BlobUri`, `FileSize` e `Sha256Hash` na tabela `DocumentAttachments`

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|------|------|----------|------|
| 1.0 | 2025-12-31 | Documentação completa de referência ao legado de RF091 | Agência ALC - alc.dev.br |
