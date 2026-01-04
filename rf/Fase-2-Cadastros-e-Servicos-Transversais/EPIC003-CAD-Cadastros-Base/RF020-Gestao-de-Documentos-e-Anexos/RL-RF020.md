# RL-RF020 — Referência ao Legado

**Versão:** 1.0
**Data:** 2025-12-30
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF-020 - Gestão de Documentos e Anexos
**Sistema Legado:** IControlIT (ASP.NET Web Forms + VB.NET)
**Objetivo:** Documentar o comportamento do sistema legado de gestão de arquivos que serve de base para a refatoração do DMS moderno, garantindo rastreabilidade, entendimento histórico e mitigação de riscos durante a migração.

---

## 1. CONTEXTO DO LEGADO

### Cenário Geral

O sistema legado IControlIT implementava uma gestão simplificada de arquivos sem funcionalidades avançadas de segurança, versionamento ou controle granular de acesso.

**Características Técnicas:**
- **Arquitetura:** Monolítica Web Forms (ASP.NET)
- **Linguagem:** VB.NET (code-behind .aspx.vb)
- **Banco de Dados:** SQL Server (tabela `Arquivo` com campos básicos)
- **Armazenamento:** FileSystem local (D:\Arquivos\)
- **Multi-tenant:** Parcial (Id_Conglomerado existia, mas sem row-level security)
- **Auditoria:** Inexistente (sem log de uploads, downloads, exclusões)
- **Versionamento:** Inexistente (sobrescrever arquivo perdia versão anterior)
- **Scan Antivírus:** Inexistente (risco de malware)
- **OCR:** Inexistente (impossível buscar texto em PDFs escaneados)
- **Compartilhamento:** Inexistente (sem links temporários seguros)
- **Permissões:** Baseadas apenas em perfis globais (não granular por documento)

### Limitações Críticas Identificadas

1. **Segurança:** Upload sem scan antivírus permitia envio de malware
2. **Integridade:** Sem hash SHA-256, impossível validar integridade do arquivo
3. **Rastreabilidade:** Sem auditoria, impossível saber quem acessou documentos sensíveis (violação LGPD/GDPR)
4. **Recuperação:** Hard delete impedia recuperação de documentos excluídos acidentalmente
5. **Escalabilidade:** FileSystem local sem backup automático e sem escalabilidade horizontal
6. **Busca:** Impossível buscar conteúdo textual em PDFs escaneados

### Estrutura de Banco Legado

**Tabela `Arquivo` (Simplificada)**
```sql
CREATE TABLE Arquivo (
    Id_Arquivo INT PRIMARY KEY IDENTITY,
    Id_Conglomerado INT NOT NULL, -- Multi-tenancy básico
    Nm_Arquivo VARCHAR(255) NOT NULL,
    Caminho VARCHAR(500) NOT NULL, -- Caminho físico no FileSystem
    Tamanho INT, -- Bytes
    Dt_Upload DATETIME DEFAULT GETDATE(),
    Id_Usuario_Upload INT
    -- SEM: Hash, Versão, ACL, OCR, Auditoria, Soft Delete
)
```

**Problemas:**
- Sem campo `Hash_SHA256` (integridade não verificável)
- Sem campo `Versao` (versionamento inexistente)
- Sem tabela de permissões (ACL inexistente)
- Sem tabela de auditoria (compliance impossível)
- Sem soft delete (`Fl_Ativo`) (exclusão era definitiva)
- Sem campos de OCR (`Texto_OCR`, `Fl_OCR_Processado`)

---

## 2. TELAS DO LEGADO

### Nota Importante

No sistema legado, **não havia tela dedicada para gestão de documentos**. A funcionalidade de upload/download estava **distribuída** em diversas páginas `.aspx` relacionadas a diferentes módulos:

- **Ativo.aspx** - Upload de fotos e manuais de ativos
- **Contrato.aspx** - Upload de contratos escaneados
- **Fornecedor.aspx** - Upload de certificados e documentos fiscais
- **Fatura.aspx** - Upload de notas fiscais e recibos

**Problema:** Código de upload duplicado em múltiplas páginas, sem componente reutilizável, aumentando risco de inconsistências e bugs.

### Exemplo de Implementação Legada (Ativo.aspx)

**Caminho:** `D:\IC2\ic1_legado\IControlIT\Ativo.aspx.vb`

**Responsabilidade:** Permitir upload de fotos/manuais de ativos.

#### Campos (Fragmento)

| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| FileUpload1 | FileUpload Control | Não | Controle ASP.NET padrão |
| btnUpload | Button | - | Evento Click chama lógica de upload |

#### Comportamentos Implícitos Críticos

1. **Sem Validação de MIME Type:** Apenas extensão do arquivo era verificada (facilmente burlável renomeando `malware.exe` → `malware.pdf.exe`)
2. **Sem Scan Antivírus:** Arquivo salvo diretamente no FileSystem sem varredura
3. **Upload Síncrono Bloqueante:** Timeout para arquivos > 50MB (sem upload assíncrono)
4. **Sem Tratamento de Erro Robusto:** Se upload falhava, registro órfão ficava no banco apontando para arquivo inexistente
5. **Sem Limite de Tamanho Configurável:** Limite fixo de 10MB (hardcoded), impossível ajustar sem recompilar
6. **Caminho Físico Hardcoded:** `D:\Arquivos\` sem configuração via Web.config (problema em ambientes diferentes)

**Código Legado Representativo (VB.NET):**
```vb
' Upload simples sem validação de segurança
Dim nomeArquivo As String = FileUpload1.FileName
Dim caminhoDestino As String = "D:\Arquivos\" & nomeArquivo
FileUpload1.SaveAs(caminhoDestino) ' Salva direto, sem scan antivírus!

' Inserir registro no banco - campos mínimos
Dim sql As String = "INSERT INTO Arquivo (Nm_Arquivo, Caminho, Tamanho) VALUES (@Nome, @Caminho, @Tamanho)"
' Sem hash, sem versionamento, sem permissões granulares
```

**Vulnerabilidades:**
- Path Traversal: Nome de arquivo `../../etc/passwd` poderia sobrescrever arquivos do sistema
- XSS: Nome de arquivo `<script>alert('XSS')</script>.pdf` não era sanitizado
- Zip Bomb: Arquivo compactado malicioso com GB descompactados não era validado

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

**Arquivo:** `WSDocumentos.asmx.vb`
**Localização:** `D:\IC2\ic1_legado\IControlIT\WS_IControlIT\WSDocumentos.asmx.vb`

| Método | Responsabilidade | Observações |
|--------|-----------------|-------------|
| `UploadArquivo(nomeArquivo, bytesArquivo, idEntidade, tipoEntidade)` | Receber arquivo como byte array (base64) e salvar no FileSystem | ❌ Sem scan antivírus<br>❌ Sem validação robusta de MIME type<br>❌ Sem hash SHA-256<br>❌ Upload síncrono bloqueante |
| `DownloadArquivo(idArquivo)` | Buscar arquivo no banco e retornar byte array | ❌ Sem validação de permissões (qualquer usuário autenticado podia baixar qualquer arquivo)<br>❌ Sem auditoria de download |
| `ListarDocumentos(idEntidade, tipoEntidade)` | Listar documentos vinculados a uma entidade | ❌ Sem paginação (crash se muitos documentos)<br>✅ Retornava: ID, nome, tamanho, data upload |
| `ExcluirArquivo(idArquivo)` | Deletar registro do banco + arquivo físico | ❌ Hard delete (impossível recuperar)<br>❌ Sem log de quem deletou ou motivo<br>❌ Se delete no banco falhasse mas arquivo físico fosse deletado, ficava inconsistente |

### Problemas Críticos Identificados

**Autenticação:**
- Baseada em session-based token `pPakage` validado por `cls_Config.Validar_Pakage()`
- Sem JWT Bearer moderno
- Token não expirava automaticamente (risco de session hijacking)

**Performance:**
- Upload síncrono bloqueava thread do IIS (timeout >50MB)
- Sem suporte a multipart/form-data chunked (upload de arquivos grandes falhava)
- Sem SignalR para progress tracking (usuário não sabia se upload estava funcionando)

**Armazenamento:**
- FileSystem local `D:\Arquivos\` sem backup automático
- Sem suporte a Azure Blob Storage ou AWS S3
- Sem geo-replicação (se servidor pegasse fogo, documentos perdidos)

**Logging:**
- Sem auditoria de quem fez upload, download, exclusão
- Compliance LGPD/GDPR impossível (não conseguia rastrear acesso a dados sensíveis)

---

## 4. TABELAS LEGADAS

| Tabela | Finalidade | Problemas Identificados |
|--------|-----------|-------------------------|
| `Arquivo` | Armazenar metadados básicos de arquivos | ❌ Campos insuficientes (sem hash, versão, OCR)<br>❌ Sem tabela de permissões (ACL)<br>❌ Sem tabela de auditoria<br>❌ Sem soft delete<br>❌ Sem foreign key para versionamento |

### DDL Legado Reconstruído

```sql
CREATE TABLE Arquivo (
    Id_Arquivo INT PRIMARY KEY IDENTITY,
    Id_Conglomerado INT NOT NULL,
    Nm_Arquivo VARCHAR(255) NOT NULL,
    Caminho VARCHAR(500) NOT NULL, -- Ex: D:\Arquivos\contrato_001.pdf
    Tamanho INT, -- Bytes
    Dt_Upload DATETIME DEFAULT GETDATE(),
    Id_Usuario_Upload INT,
    CONSTRAINT FK_Arquivo_Conglomerado FOREIGN KEY (Id_Conglomerado) REFERENCES Conglomerado(Id_Conglomerado)
)
```

**Ausências Críticas:**
- Sem índice em `Hash_SHA256` (detecção de duplicatas impossível)
- Sem Full-Text Index (busca em conteúdo impossível)
- Sem campo `Fl_Ativo` (soft delete inexistente)
- Sem campo `Versao` (versionamento inexistente)

---

## 5. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

Regras que existiam no comportamento do sistema, mas **não estavam documentadas formalmente**:

### RL-RN-001: Upload Sem Validação de Tipo de Arquivo

**Descrição:** Sistema legado aceitava qualquer tipo de arquivo desde que extensão estivesse em whitelist hardcoded.

**Problema:** Whitelist era verificada apenas pela extensão do arquivo, não pelo MIME type real. Atacante podia renomear `malware.exe` → `documento.pdf.exe` e sistema aceitava se `.pdf` estivesse permitido.

**Destino no RF Moderno:** **SUBSTITUÍDO** por RN-RF020-010 (validação de extensão E MIME type).

---

### RL-RN-002: Exclusão Definitiva de Arquivos

**Descrição:** Comando de exclusão deletava registro do banco E arquivo físico do FileSystem imediatamente, sem possibilidade de recuperação.

**Problema:** Usuários excluíam documentos importantes por acidente sem forma de restaurar. Suporte recebia chamados recorrentes para "recuperar arquivo deletado ontem".

**Destino no RF Moderno:** **SUBSTITUÍDO** por RN-RF020-008 (soft delete com recuperação em 30 dias).

---

### RL-RN-003: Sobrescrita de Arquivos Sem Versionamento

**Descrição:** Se usuário fizesse upload de arquivo com mesmo nome de arquivo existente, sistema sobrescrevia sem criar versão anterior.

**Problema:** Perda de histórico de alterações. Usuários não conseguiam reverter para versão anterior de contrato ou documento.

**Destino no RF Moderno:** **SUBSTITUÍDO** por RN-RF020-003 (versionamento automático com linked list de versões).

---

### RL-RN-004: Download Sem Validação de Integridade

**Descrição:** Download retornava byte array do arquivo sem validar se arquivo foi corrompido ou modificado maliciosamente.

**Problema:** Se arquivo no FileSystem fosse corrompido ou alterado por ransomware, usuário baixava arquivo corrompido sem perceber.

**Destino no RF Moderno:** **SUBSTITUÍDO** por RN-RF020-002 (hash SHA-256 validado antes de download).

---

### RL-RN-005: Permissões Globais por Perfil

**Descrição:** Permissões de acesso a documentos eram baseadas apenas em perfis globais (Admin, Gestor, Usuário). Não havia controle granular por documento.

**Problema:** Gestor de TI podia ver contratos confidenciais de RH. Não havia como restringir documento específico para grupo específico.

**Destino no RF Moderno:** **SUBSTITUÍDO** por RN-RF020-004 (ACL granular por documento com Deny sobrescrevendo Allow).

---

### RL-RN-006: Limite de Tamanho Fixo (Hardcoded)

**Descrição:** Limite de 10MB por arquivo estava hardcoded no código VB.NET. Alterar exigia recompilação e deploy.

**Problema:** Impossível fazer upload de vídeos de treinamento, apresentações grandes ou backups. Usuários tinham que compactar arquivos excessivamente, perdendo qualidade.

**Destino no RF Moderno:** **SUBSTITUÍDO** por RN-RF020-009 (limites configuráveis por tipo de arquivo via appsettings.json).

---

## 6. GAP ANALYSIS (LEGADO x RF MODERNO)

| Item | Legado | RF Moderno | Observação |
|------|--------|------------|------------|
| **Scan Antivírus** | ❌ Inexistente | ✅ Obrigatório (ClamAV/VirusTotal) | Gap crítico de segurança |
| **Hash SHA-256** | ❌ Inexistente | ✅ Calculado em todo upload | Gap de integridade |
| **Versionamento** | ❌ Sobrescrita destrutiva | ✅ Automático com linked list | Gap de rastreabilidade |
| **ACL Granular** | ❌ Permissões globais por perfil | ✅ Por documento (usuário/perfil/departamento) | Gap de segurança |
| **OCR** | ❌ Inexistente | ✅ Automático (Tesseract/Azure) | Gap de usabilidade |
| **Compartilhamento Seguro** | ❌ Inexistente | ✅ Links temporários com expiração/senha | Gap de colaboração |
| **Auditoria** | ❌ Inexistente | ✅ Completa (7 anos LGPD) | Gap de compliance |
| **Soft Delete** | ❌ Hard delete | ✅ Recuperação em 30 dias | Gap de recuperação |
| **Armazenamento** | ❌ FileSystem local | ✅ Azure Blob / AWS S3 | Gap de escalabilidade |
| **Upload Assíncrono** | ❌ Síncrono bloqueante | ✅ Assíncrono com SignalR | Gap de performance |
| **Full-Text Search** | ❌ Inexistente | ✅ Nome, descrição, tags, OCR | Gap de usabilidade |
| **Metadados Customizados** | ❌ Campos fixos | ✅ JSON Schema flexível | Gap de extensibilidade |
| **Alertas de Validade** | ❌ Inexistente | ✅ Job diário (30, 15, 7, 1 dia) | Gap de gestão |
| **Criptografia** | ❌ Arquivos em texto claro | ✅ AES-256 para confidenciais | Gap de segurança |

---

## 7. DECISÕES DE MODERNIZAÇÃO

### Decisão 1: Migração de FileSystem Local para Blob Storage

**Motivo:** FileSystem local não escala horizontalmente, não tem backup automático, não permite geo-replicação.

**Impacto:** **ALTO**
- Código de upload/download deve ser refatorado completamente
- Migração de arquivos existentes deve ser planejada (≈500GB estimados)
- Custo mensal de storage cloud deve ser aprovado (≈$50-200/mês dependendo volume)

**Estratégia:** Migração faseada com convivência dual (legado + moderno acessando mesmo blob via adapter pattern).

---

### Decisão 2: Implementação de Scan Antivírus Obrigatório

**Motivo:** Legado permitia upload de malware sem verificação. Risco inaceitável para ambiente corporativo.

**Impacto:** **ALTO**
- Adiciona latência ao upload (3-30s por arquivo dependendo tamanho)
- Exige integração com ClamAV (on-premise) ou VirusTotal (cloud)
- Arquivos grandes (>500MB) podem timeout durante scan

**Estratégia:** Upload em duas etapas: (1) salvar em quarentena, (2) scan assíncrono via Hangfire, (3) mover para storage definitivo se clean.

---

### Decisão 3: Versionamento Automático com Linked List

**Motivo:** Legado sobrescrevia arquivos perdendo histórico. Usuários não conseguiam reverter alterações indesejadas.

**Impacto:** **MÉDIO**
- Aumenta uso de storage (cada versão ocupa espaço)
- Complexidade no modelo de dados (campo `Id_Documento_Anterior` forma linked list)
- UI deve mostrar timeline de versões com diff visual

**Estratégia:** Versões antigas arquivadas automaticamente após 90 dias para cold storage (custo reduzido).

---

### Decisão 4: ACL Granular com Deny Override

**Motivo:** Legado tinha permissões globais por perfil. Impossível restringir documento confidencial para grupo específico.

**Impacto:** **MÉDIO**
- Aumenta complexidade de autorização (verificar ACL antes de cada operação)
- UI deve permitir configurar permissões facilmente (não pode ser complexo demais)
- Performance: queries devem otimizar joins com `Documento_Permissao`

**Estratégia:** Tabela `Documento_Permissao` com índices otimizados. Cache de permissões em Redis para usuários frequentes.

---

### Decisão 5: OCR Automático para PDFs Escaneados

**Motivo:** Legado não permitia busca em conteúdo de PDFs escaneados. Usuários não encontravam documentos importantes.

**Impacto:** **MÉDIO**
- Processamento OCR é lento (10-60s por página dependendo qualidade)
- Exige integração com Tesseract (on-premise) ou Azure Computer Vision (cloud)
- Custo: Azure Computer Vision cobra por página processada (≈$1.50/1000 páginas)

**Estratégia:** OCR processado assíncronamente via Hangfire background job. Prioridade: documentos críticos (contratos, notas fiscais) primeiro.

---

### Decisão 6: Soft Delete com Recuperação em 30 Dias

**Motivo:** Legado fazia hard delete irreversível. Usuários excluíam documentos importantes por acidente.

**Impacto:** **BAIXO**
- Apenas adicionar campo `Fl_Ativo` e lógica de soft delete
- Hangfire job para hard delete após 30 dias
- UI deve ter tela "Lixeira" para admins restaurarem documentos

**Estratégia:** Implementação padrão de soft delete já existente em outras entidades do sistema.

---

## 8. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| **Perda de arquivos durante migração FileSystem → Blob** | CRÍTICO | MÉDIA | Backup completo antes, migração em horário baixo uso, validação hash pós-migração |
| **Scan antivírus causar timeout em uploads grandes** | ALTO | ALTA | Upload em chunks, scan assíncrono via job, aumentar timeout IIS para 10min |
| **Custo de storage cloud ultrapassar orçamento** | MÉDIO | MÉDIA | Monitoramento de custos mensal, lifecycle policy (mover versões antigas para cold storage) |
| **OCR não funcionar bem em PDFs de baixa qualidade** | MÉDIO | ALTA | Pré-processamento de imagem (deskew, denoise), permitir OCR manual se automático falhar |
| **Usuários não conseguirem acessar documentos após migração ACL** | ALTO | MÉDIA | Mapeamento automático de permissões legado → ACL moderno, período de convivência dual |
| **Performance degradada por queries complexas em ACL** | MÉDIO | BAIXA | Índices otimizados, cache Redis de permissões, profile queries antes deploy |

---

## 9. RASTREABILIDADE

| Elemento Legado | Referência RF Moderno | Destino |
|----------------|-----------------------|---------|
| `WSDocumentos.asmx::UploadArquivo()` | `POST /api/v1/documents/upload` (RF-020 Funcionalidade #1) | SUBSTITUÍDO |
| `WSDocumentos.asmx::DownloadArquivo()` | `GET /api/v1/documents/{id}/download` (RF-020 Funcionalidade #5) | SUBSTITUÍDO |
| `WSDocumentos.asmx::ListarDocumentos()` | `GET /api/v1/documents?entityId={id}` (RF-020 Funcionalidade #4) | SUBSTITUÍDO |
| `WSDocumentos.asmx::ExcluirArquivo()` | `DELETE /api/v1/documents/{id}` com soft delete (RF-020 Funcionalidade #8) | SUBSTITUÍDO |
| Tabela `Arquivo` | Tabela `Documento` (expandida com 20+ campos adicionais) | SUBSTITUÍDO |
| RL-RN-001 (Upload sem validação) | RN-RF020-010 (Validação extensão + MIME) | SUBSTITUÍDO |
| RL-RN-002 (Hard delete) | RN-RF020-008 (Soft delete com recuperação) | SUBSTITUÍDO |
| RL-RN-003 (Sobrescrita sem versão) | RN-RF020-003 (Versionamento automático) | SUBSTITUÍDO |
| RL-RN-004 (Download sem validação) | RN-RF020-002 (Hash SHA-256) | SUBSTITUÍDO |
| RL-RN-005 (Permissões globais) | RN-RF020-004 (ACL granular) | SUBSTITUÍDO |
| RL-RN-006 (Limite hardcoded) | RN-RF020-009 (Limites configuráveis) | SUBSTITUÍDO |

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|--------|------|-----------|-------|
| 1.0 | 2025-12-30 | Documentação completa da referência ao legado RF-020 | Agência ALC - alc.dev.br |
