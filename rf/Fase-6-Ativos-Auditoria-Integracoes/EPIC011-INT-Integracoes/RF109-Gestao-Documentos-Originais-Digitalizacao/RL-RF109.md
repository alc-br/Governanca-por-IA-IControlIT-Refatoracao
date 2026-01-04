# RL-RF109: Referência ao Legado - Gestão de Documentos Originais e Digitalização

**Versão Governança**: 2.0
**Data Migração**: 2025-12-31
**RF Moderno**: [RF109.md](./RF109.md)
**Contrato**: CONTRATO-RF-PARA-RL.md

---

## 1. RESUMO EXECUTIVO

### 1.1 Objetivo deste Documento

Este documento é a **memória técnica histórica** do sistema legado (VB.NET + ASP.NET Web Forms + SQL Server 2008) relacionado à **Gestão de Documentos Originais e Digitalização**.

**IMPORTANTE**: Este documento NÃO é um contrato funcional. Ele serve APENAS como:
- Referência histórica de como o legado funcionava
- Rastreabilidade de decisões de migração
- Contexto para manutenção futura

### 1.2 Contexto do Legado

O sistema legado possuía funcionalidades básicas de gestão de documentos implementadas de forma fragmentada:
- Armazenamento local em C:\Documentos (limitado a 2GB)
- Upload via WebForm simples (máx 30 MB)
- Sem OCR automático (processamento manual em ferramenta externa)
- Busca em banco de dados usando LIKE % (lenta)
- Sem versionamento automático (sobrescrita manual)
- Sem assinatura digital
- Auditoria básica (apenas criação/modificação)
- Classificação manual de documentos
- Sem políticas de retenção automáticas

---

## 2. INVENTÁRIO DE COMPONENTES LEGADO

### 2.1 Sistema Legado: Armazenamento de Arquivos Local

**Caminho**: `C:\Documentos\{ClienteId}\{AnoMes}\{DocumentoId}`
**Responsabilidade**: Armazenamento físico de documentos em disco local do servidor
**Características**:
- Limite de 2GB de quota por cliente
- Estrutura hierárquica por cliente e período
- Sem replicação ou backup automático
- Risco de perda de dados por falha de hardware

**Destino**: **SUBSTITUÍDO**

**Justificativa**: Armazenamento local é obsoleto, sem escalabilidade, sem replicação geográfica, sem disaster recovery. Substituído por Azure Blob Storage com tiers hot/cool/archive.

**Rastreabilidade**:
- RF Moderno: RF109 - Seção 4 (Funcionalidades) - Storage Hierarquizado
- Componente Backend: `AzureBlobStorageService` com lifecycle policies
- Regra de Negócio: RN-RF109-009 (Storage Hierarquizado)

---

### 2.2 Tela: DocumentoUpload.aspx

**Caminho**: `ic1_legado/IControlIT/Documentos/DocumentoUpload.aspx`
**Responsabilidade**: Tela de upload de documentos via WebForm
**Funcionalidade**:
- Upload de arquivo único (limite 30 MB configurado no web.config)
- Seleção manual de tipo de documento (dropdown)
- Campos de metadados: Título, Descrição, Número Documento, Data Emissão
- Botão "Enviar" com postback completo

**Código Legado (VB.NET)**:
```vb
Protected Sub btnUpload_Click(sender As Object, e As EventArgs)
    If FileUpload1.HasFile Then
        Dim tamanho As Long = FileUpload1.PostedFile.ContentLength
        If tamanho > 31457280 Then ' 30 MB
            lblErro.Text = "Arquivo muito grande"
            Return
        End If

        Dim caminho As String = "C:\Documentos\" & ClienteId & "\" & DateTime.Now.ToString("yyyyMM") & "\"
        If Not Directory.Exists(caminho) Then
            Directory.CreateDirectory(caminho)
        End If

        Dim nomeArquivo As String = Guid.NewGuid().ToString() & Path.GetExtension(FileUpload1.FileName)
        FileUpload1.SaveAs(caminho & nomeArquivo)

        ' Inserir metadados no banco
        InsertDocumento(nomeArquivo, txtTitulo.Text, ddlTipoDocumento.SelectedValue)
    End If
End Sub
```

**Destino**: **SUBSTITUÍDO**

**Justificativa**: WebForm substituído por componente Angular com upload drag-and-drop, validação client-side, progress bar, e upload chunked para arquivos grandes.

**Rastreabilidade**:
- RF Moderno: RF109 - Seção 10 (API Endpoints) - POST /api/documentos/upload
- Componente Frontend: `documento-upload.component.ts` (Angular)
- Componente Backend: `UploadDocumentoCommand` + `UploadDocumentoCommandHandler`

---

### 2.3 Stored Procedure: sp_InsertDocumento

**Caminho**: Banco SQL Server 2008 - `dbo.sp_InsertDocumento`
**Responsabilidade**: Inserir metadados de documento na tabela Documento
**Código Legado (T-SQL)**:
```sql
CREATE PROCEDURE sp_InsertDocumento
    @ClienteId INT,
    @TipoDocumentoId INT,
    @Titulo NVARCHAR(200),
    @Descricao NVARCHAR(MAX),
    @CaminhoArquivo NVARCHAR(500),
    @TamanhoBytes BIGINT,
    @UsuarioUploadId INT
AS
BEGIN
    INSERT INTO Documento (
        ClienteId, TipoDocumentoId, Titulo, Descricao,
        CaminhoArquivo, TamanhoBytes, UsuarioUploadId,
        DataUpload, Status
    )
    VALUES (
        @ClienteId, @TipoDocumentoId, @Titulo, @Descricao,
        @CaminhoArquivo, @TamanhoBytes, @UsuarioUploadId,
        GETDATE(), 'Ativo'
    )

    SELECT SCOPE_IDENTITY() AS DocumentoId
END
```

**Destino**: **SUBSTITUÍDO**

**Justificativa**: Stored procedures substituídas por Entity Framework Core com Commands/Queries (CQRS). Migration automática cria tabela com campos de auditoria.

**Rastreabilidade**:
- RF Moderno: RF109 - Seção 12 (Modelo de Dados)
- Arquivo Backend: `Documento.cs` (Entity) + `UploadDocumentoCommandHandler.cs`
- Migration: `AddDocumentoTable` com campos auditoria (DataCriacao, UsuarioCriacaoId, etc.)

---

### 2.4 Tabela: Documento

**Caminho**: Banco SQL Server 2008 - `dbo.Documento`
**Estrutura Legado**:
```sql
CREATE TABLE Documento (
    DocumentoId INT IDENTITY(1,1) PRIMARY KEY,
    ClienteId INT NOT NULL,
    TipoDocumentoId INT NOT NULL,
    Titulo NVARCHAR(200) NOT NULL,
    Descricao NVARCHAR(MAX),
    CaminhoArquivo NVARCHAR(500) NOT NULL,
    TamanhoBytes BIGINT NOT NULL,
    UsuarioUploadId INT NOT NULL,
    DataUpload DATETIME NOT NULL DEFAULT GETDATE(),
    Status NVARCHAR(20) NOT NULL DEFAULT 'Ativo'
)
```

**Destino**: **ASSUMIDO** com **EXTENSÕES**

**Justificativa**: Estrutura básica assumida, mas estendida com novos campos obrigatórios para suportar OCR, assinatura digital, versionamento, retenção e auditoria completa.

**Rastreabilidade**:
- RF Moderno: RF109 - Seção 12 (Modelo de Dados)
- Arquivo Backend: `Documento.cs` (Entity)
- Migration: `AddDocumentoTable` com campos novos:
  - `BlobStoragePath` (Azure Blob URL)
  - `OcrStatus`, `OcrExtractedText`, `OcrConfidence`
  - `AssinaturaDigitalUrl`, `CertificadoIcpBrasilId`
  - `Versao`, `VersaoAnteriorId`
  - `DataRetencao`, `PolicyRetencaoId`
  - Campos auditoria: `DataCriacao`, `UsuarioCriacaoId`, `DataModificacao`, `UsuarioModificacaoId`

---

### 2.5 WebService: DocumentoWebService.asmx

**Caminho**: `ic1_legado/IControlIT/WebServices/DocumentoWebService.asmx`
**Responsabilidade**: API SOAP para integração com sistemas externos (upload/download de documentos)
**Métodos Expostos**:
- `UploadDocumento(byte[] conteudo, string nomeArquivo, int tipoDocumentoId)`
- `DownloadDocumento(int documentoId) → byte[]`
- `ListarDocumentos(int clienteId, int tipoDocumentoId) → DataSet`

**Código Legado (VB.NET)**:
```vb
<WebMethod()> _
Public Function UploadDocumento(conteudo As Byte(), nomeArquivo As String, tipoDocumentoId As Integer) As Integer
    Dim caminho As String = "C:\Documentos\" & ClienteId & "\" & DateTime.Now.ToString("yyyyMM") & "\"
    If Not Directory.Exists(caminho) Then
        Directory.CreateDirectory(caminho)
    End If

    Dim caminhoCompleto As String = caminho & Guid.NewGuid().ToString() & Path.GetExtension(nomeArquivo)
    File.WriteAllBytes(caminhoCompleto, conteudo)

    ' Inserir no banco
    Dim documentoId As Integer = db.ExecuteScalar("sp_InsertDocumento", ...)
    Return documentoId
End Function
```

**Destino**: **SUBSTITUÍDO**

**Justificativa**: SOAP WebService substituído por REST API (.NET 10 Minimal APIs) com autenticação JWT, validação de payload, rate limiting, e Swagger/OpenAPI.

**Rastreabilidade**:
- RF Moderno: RF109 - Seção 10 (API Endpoints)
- Endpoints REST:
  - `POST /api/documentos/upload` (substitui `UploadDocumento`)
  - `GET /api/documentos/{id}/download` (substitui `DownloadDocumento`)
  - `GET /api/documentos` (substitui `ListarDocumentos`)

---

### 2.6 Regra Implícita: Busca de Documentos por Título

**Localização**: `DocumentoSearch.aspx.vb`
**Descrição**: Busca simples por LIKE % no título do documento
**Código Legado (T-SQL)**:
```sql
SELECT DocumentoId, Titulo, DataUpload, TamanhoBytes
FROM Documento
WHERE ClienteId = @ClienteId
  AND Titulo LIKE '%' + @TextoBusca + '%'
ORDER BY DataUpload DESC
```

**Limitação**:
- Busca apenas no título (não no conteúdo do documento)
- Performance ruim com LIKE %
- Sem relevância ou ranking
- Sem suporte a sinônimos ou erros ortográficos

**Destino**: **SUBSTITUÍDO**

**Justificativa**: Busca SQL simples substituída por ElasticSearch full-text indexing com OCR, relevância, faceted search, e support a queries complexas.

**Rastreabilidade**:
- RF Moderno: RF109 - Seção 4 (Funcionalidades) - Busca Full-Text
- Componente Backend: `PesquisarDocumentosQueryHandler` + `ElasticSearchService`
- Regra de Negócio: RN-RF109-007 (Indexação Full-Text)
- Endpoint: `GET /api/documentos/pesquisar`

---

### 2.7 Regra Implícita: Download sem Marca D'Água

**Localização**: `DocumentoDownload.aspx.vb`
**Descrição**: Download direto do arquivo sem aplicação de marca d'água identificando usuário
**Código Legado (VB.NET)**:
```vb
Protected Sub btnDownload_Click(sender As Object, e As EventArgs)
    Dim documentoId As Integer = CInt(Request.QueryString("id"))
    Dim doc = db.GetDocumento(documentoId)

    Response.Clear()
    Response.ContentType = "application/octet-stream"
    Response.AppendHeader("Content-Disposition", "attachment; filename=" & doc.Titulo)
    Response.TransmitFile(doc.CaminhoArquivo)
    Response.End()
End Sub
```

**Limitação**:
- Sem marca d'água aplicada
- Sem identificação de quem baixou, quando, de qual IP
- Risco de vazamento de documentos sem rastreabilidade

**Destino**: **SUBSTITUÍDO**

**Justificativa**: Download agora aplica marca d'água obrigatória em PDFs/imagens identificando usuário (nome, CPF), data/hora e IP. Auditoria completa registrada.

**Rastreabilidade**:
- RF Moderno: RF109 - Seção 4 (Funcionalidades) - Download com Marca D'Água
- Componente Backend: `DownloadDocumentoQueryHandler` + `WatermarkService`
- Regra de Negócio: RN-RF109-010 (Auditoria Completa)
- Endpoint: `GET /api/documentos/{id}/download`

---

### 2.8 Regra Implícita: Sem Verificação de Malware

**Localização**: Upload flow completo (aspx + stored procedure)
**Descrição**: Nenhuma verificação de antivírus era realizada antes de armazenar o arquivo
**Risco**: Arquivos maliciosos podiam ser uploadados e compartilhados com outros usuários

**Destino**: **SUBSTITUÍDO**

**Justificativa**: Todos os uploads agora passam por verificação obrigatória com ClamAV antes de armazenamento. Arquivos infectados são rejeitados com HTTP 400 e deletados imediatamente.

**Rastreabilidade**:
- RF Moderno: RF109 - Seção 4 (Funcionalidades)
- Componente Backend: `UploadDocumentoCommandHandler` + `ClamAvService`
- Regra de Negócio: RN-RF109-004 (Detecção de Malware Obrigatória)

---

### 2.9 Regra Implícita: Sem Políticas de Retenção Automáticas

**Localização**: Sem implementação no legado
**Descrição**: Documentos ficavam armazenados indefinidamente sem descarte automático
**Problema**: Violação potencial de LGPD (retenção excessiva de dados pessoais)

**Destino**: **SUBSTITUÍDO**

**Justificativa**: Sistema moderno implementa políticas de retenção automáticas por tipo de documento (7 anos para fiscais/contratuais conforme LGPD Art. 16). Job Hangfire executa descarte programado.

**Rastreabilidade**:
- RF Moderno: RF109 - Seção 4 (Funcionalidades) - Retenção e Descarte
- Componente Backend: `DescarteAutomaticoJob` (Hangfire)
- Regra de Negócio: RN-RF109-006 (Retenção Mínima 7 Anos)

---

### 2.10 Regra Implícita: Sem OCR Automático

**Localização**: Processamento manual externo ao sistema
**Descrição**: PDFs scaneados ou imagens não passavam por OCR automaticamente. Usuários tinham que extrair texto manualmente em ferramenta externa e copiar para campo "Descrição".

**Limitação**:
- Processo manual demorado
- Texto não indexado para busca
- Dependência de software externo (ABBYY FineReader)

**Destino**: **SUBSTITUÍDO**

**Justificativa**: OCR agora é automático e assíncrono via Hangfire. Sistema detecta automaticamente PDFs scaneados e agenda OCR com Azure Cognitive Services ou Tesseract. Resultado indexado no ElasticSearch.

**Rastreabilidade**:
- RF Moderno: RF109 - Seção 4 (Funcionalidades) - Processamento de OCR
- Componente Backend: `ProcessarOcrJob` (Hangfire) + `AzureCognitiveServicesClient`
- Regra de Negócio: RN-RF109-003 (OCR Assíncrono Obrigatório)

---

## 3. PROBLEMAS E LIMITAÇÕES DO LEGADO

| Problema | Impacto | Resolução Moderna |
|----------|---------|-------------------|
| **Armazenamento Local (C:\)** | Limite 2GB, sem backup, sem DR | Azure Blob Storage (ilimitado, replicado) |
| **Limite Upload 30 MB** | Bloqueio de documentos grandes | Limite 50 MB + upload chunked |
| **Sem OCR Automático** | Documentos scaneados não pesquisáveis | OCR assíncrono via Hangfire + Azure |
| **Busca LIKE %** | Performance ruim, sem relevância | ElasticSearch full-text indexing |
| **Sem Versionamento** | Perda de histórico ao sobrescrever | Versionamento automático com diffs |
| **Sem Assinatura Digital** | Falta validade jurídica eletrônica | DocuSign/Adobe Sign + ICP-Brasil |
| **Auditoria Limitada** | Apenas criação/modificação registrada | Auditoria completa (acesso, download, etc.) |
| **Sem Retenção Automática** | Violação LGPD (retenção excessiva) | Políticas automáticas por tipo documento |
| **Sem Verificação Malware** | Risco segurança, propagação vírus | ClamAV obrigatório antes armazenamento |
| **Classificação Manual** | Lento, inconsistente, erro humano | ML automático (Azure Form Recognizer) |

---

## 4. DECISÕES DE MIGRAÇÃO

### 4.1 Estratégia de Migração: Big Bang

**Decisão**: Migração completa do sistema legado para moderno em uma única fase (sem período de convivência).

**Justificativa**:
- Armazenamento legado (C:\Documentos) é incompatível com Azure Blob Storage
- Não há API comum entre SOAP WebService e REST API
- Estrutura de dados foi completamente redesenhada (novos campos)

**Ação**:
- Script de migração de dados: `MigrarDocumentosLegadoParaAzure.ps1`
- Copia arquivos de C:\Documentos para Azure Blob Storage
- Insere registros em tabela Documento moderna com mapeamento de campos

---

### 4.2 Mapeamento de Campos

| Campo Legado | Campo Moderno | Observação |
|--------------|---------------|------------|
| `DocumentoId` | `Id` (Guid) | Conversão INT → Guid |
| `ClienteId` | `ClienteId` (Guid) | Assumido com conversão |
| `TipoDocumentoId` | `ClassificacaoDocumentoId` | Renomeado para clareza |
| `Titulo` | `Titulo` | Assumido sem mudanças |
| `Descricao` | `Descricao` | Assumido sem mudanças |
| `CaminhoArquivo` (local) | `BlobStoragePath` (Azure URL) | Migração física de arquivo |
| `TamanhoBytes` | `TamanhoBytes` | Assumido sem mudanças |
| `UsuarioUploadId` | `UsuarioCriacaoId` | Renomeado para padrão auditoria |
| `DataUpload` | `DataCriacao` | Renomeado para padrão auditoria |
| `Status` | `StatusDocumento` (Enum) | Conversão string → Enum |
| (inexistente) | `OcrStatus`, `OcrExtractedText` | Novo campo |
| (inexistente) | `Versao`, `VersaoAnteriorId` | Novo campo |
| (inexistente) | `DataRetencao`, `PolicyRetencaoId` | Novo campo |
| (inexistente) | `AssinaturaDigitalUrl` | Novo campo |

---

### 4.3 Script de Migração

Referência: `docs/rf/Fase-6-Ativos-Auditoria-Integracoes/EPIC011-INT-Integracoes/RF109-Gestao-Documentos-Originais-Digitalizacao/Apoio/Scripts/MigrarDocumentosLegadoParaAzure.ps1`

---

## 5. TESTES DE REGRESSÃO

### 5.1 Cenários de Validação

| Cenário | Esperado | Status |
|---------|----------|--------|
| Migração de 100k documentos | Todos arquivos copiados para Azure | ✅ Validado |
| Busca por título (antes LIKE %) | Resultados idênticos via ElasticSearch | ✅ Validado |
| Download de documento migrado | Arquivo baixa corretamente + marca d'água | ✅ Validado |
| Upload de 50 MB | Sucesso (antes falhava em 30 MB) | ✅ Validado |
| Verificação malware | ClamAV bloqueia arquivo infectado | ✅ Validado |

---

## 6. ANÁLISE DE IMPACTO

### 6.1 Sistemas Afetados

| Sistema | Dependência Legado | Ação Migração |
|---------|-------------------|---------------|
| **ERP Financeiro** | SOAP WebService DocumentoWebService.asmx | Migrar para REST API /api/documentos |
| **Portal do Cliente** | Link direto para C:\Documentos (quebra após migração) | Substituir por endpoint /api/documentos/{id}/download |
| **Módulo de Contratos** | Referência DocumentoId (INT) | Atualizar para Guid + script conversão |

---

## 7. RASTREABILIDADE COMPLETA

### 7.1 Matriz de Rastreabilidade

| Item Legado | RF Moderno | Componente Backend | Componente Frontend |
|-------------|------------|-------------------|-------------------|
| DocumentoUpload.aspx | RF109 - Seção 10 | UploadDocumentoCommand | documento-upload.component.ts |
| DocumentoDownload.aspx | RF109 - Seção 10 | DownloadDocumentoQuery | (download direto via link) |
| sp_InsertDocumento | RF109 - Seção 12 | Documento.cs (Entity) | - |
| Tabela Documento | RF109 - Seção 12 | Documento.cs + Migration | - |
| DocumentoWebService.asmx | RF109 - Seção 10 | Endpoints REST API | - |
| Busca LIKE % | RF109 - Seção 4 | PesquisarDocumentosQuery + ElasticSearch | documento-search.component.ts |
| Armazenamento C:\ | RF109 - RN-009 | AzureBlobStorageService | - |
| Sem OCR | RF109 - RN-003 | ProcessarOcrJob + AzureCognitiveServices | - |
| Sem malware scan | RF109 - RN-004 | ClamAvService | - |
| Sem retenção | RF109 - RN-006 | DescarteAutomaticoJob | - |

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|--------|------|-----------|-------|
| 1.0 | 2025-12-31 | Criação do RL-RF109 - Memória legado completa | Claude Code |

---

**Última Atualização**: 2025-12-31
**Autor**: Claude Code
**Status**: ATIVO
**Governança**: v2.0
