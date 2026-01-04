# Casos de Uso - RF020

**Versão:** 1.0
**Data:** 2025-12-17
**RF Relacionado:** [RF020 - Gestao-de-Documentos-e-Anexos](./RF020.md)

---

## Índice de Casos de Uso

| UC | Nome | Descrição |
|----|------|-----------|
| UC00 | UC00 - Listar Documentos | Caso de uso |
| UC01 | UC01 - Fazer Upload de Documento | Caso de uso |
| UC02 | UC02 - Visualizar Documento | Caso de uso |
| UC03 | UC03 - Editar Metadados de Documento | Caso de uso |
| UC04 | UC04 - Excluir Documento | Caso de uso |
| UC05 | UC05 - Gerar Documento a partir de Template | Caso de uso |
| UC05 | UC05 - Gerenciar Versões de Documento | Caso de uso |
| UC06 | UC06 - Compartilhar Documento via Link Seguro | Caso de uso |
| UC07 | UC07 - Processar OCR em Documentos | Caso de uso |

---

# UC00 - Listar Documentos

**RF**: RF-020 - Gestão de Documentos e Anexos
**Complexidade**: Baixa
**Estimativa**: 2h Backend + 3h Frontend

---

## 📋 Objetivo

Listar documentos com filtros por tipo, categoria, data upload, vinculo (ativo/fornecedor/contrato)

---

## 📝 Fluxo Principal

1. Usuário acessa "Documentos"
2. Sistema exibe grid com colunas:
   - Nome
   - Tipo
   - Tamanho
   - Upload por
   - Data
   - Validade
   - Ações
3. Usuário pode filtrar por:
   - Tipo arquivo (PDF/IMG/DOC)
   - Categoria
   - Data
   - Vínculo
4. Sistema aplica filtros e exibe resultados paginados

---

## ✅ Validações

Não há validações específicas para listagem

---

## 📐 Regras de Negócio

- **RN-UC00-001**: Multi-tenancy aplicado em todos os resultados
- **RN-UC00-002**: Paginação padrão 10-100 itens por página

---

## 🎨 Interface UI

```
┌──────────────────────────────────────────────────────────┐
│ Documentos                                    [+ Upload] │
├──────────────────────────────────────────────────────────┤
│ Filtros:                                                 │
│ Tipo: [Todos ▼]  Categoria: [Todas ▼]  Data: [▼]        │
│ Vínculo: [Todos ▼]                                       │
├────────┬──────┬──────────┬──────────┬──────────┬────────┤
│ Nome   │ Tipo │ Tamanho  │ Upload   │ Data     │ Ações  │
├────────┼──────┼──────────┼──────────┼──────────┼────────┤
│ Cont...│ PDF  │ 2.5 MB   │ João     │ 20/01/25 │[👁️][📝]│
│ Manual │ DOCX │ 1.8 MB   │ Maria    │ 19/01/25 │[👁️][📝]│
└────────┴──────┴──────────┴──────────┴──────────┴────────┘
```

---

# UC01 - Fazer Upload de Documento

**RF**: RF-020 - Gestão de Documentos e Anexos
**Complexidade**: Alta
**Estimativa**: 8h Backend + 10h Frontend

---

## 📋 Objetivo

Upload seguro com drag-and-drop, scan antivírus, validação, versionamento

---

## 📝 Fluxo Principal

1. Usuário arrasta arquivo ou clica "Selecionar"
2. Sistema valida: Tamanho (<100MB), Extensão permitida (.pdf/.jpg/.png/.docx/.xlsx)
3. Envia multipart/form-data
4. Backend: Scan antivírus (ClamAV/VirusTotal)
5. Se malware: Rejeita, notifica admin
6. Calcula hash SHA-256
7. Verifica duplicata por hash
8. Upload para Azure Blob / AWS S3
9. Cria registro em `Documento`
10. Mensagem: "Documento '{nome}' enviado com sucesso"

---

## ✅ Validações

| Campo | Regra |
|-------|-------|
| Arquivo | Max 100MB, extensões permitidas |
| Nome | 3-200 chars |
| Categoria | Enum válido |
| Validade | Data futura (opcional) |

---

## 📐 Regras de Negócio

- **RN-UC01-001**: Scan antivírus obrigatório
- **RN-UC01-002**: Hash SHA-256 calculado
- **RN-UC01-003**: Detecção de duplicatas por hash
- **RN-UC01-004**: Versionamento se arquivo existente substituído

---

## 🎨 Interface UI

```
┌──────────────────────────────────────────────────────────┐
│ Upload de Documento                              [x]    │
├──────────────────────────────────────────────────────────┤
│                                                          │
│          ┌────────────────────────────────┐             │
│          │  Arraste arquivos aqui ou      │             │
│          │  [Clique para selecionar]      │             │
│          │                                │             │
│          │  PDF, DOC, XLS, IMG - Max 100MB│             │
│          └────────────────────────────────┘             │
│                                                          │
│ Nome*: [Contrato_Prestacao_Servicos_______]             │
│ Categoria*: [Contratos ▼]                               │
│ Validade: [__/__/____] (opcional)                       │
│                                                          │
│              [Cancelar] [Fazer Upload]                   │
└──────────────────────────────────────────────────────────┘
```

---

## 🔍 Observações Técnicas

**Segurança:**
- Scan antivírus obrigatório antes de aceitar arquivo
- Hash SHA-256 para integridade e detecção de duplicatas
- Armazenamento em cloud (Azure Blob Storage ou AWS S3)

---

# UC02 - Visualizar Documento

**RF**: RF-020 - Gestão de Documentos e Anexos
**Complexidade**: Média
**Estimativa**: 4h Backend + 6h Frontend

---

## 📋 Objetivo

Visualizar documento embutido no sistema (PDF/IMG) ou baixar (DOC/XLS)

---

## 📝 Fluxo Principal

1. Usuário clica em "Visualizar" (👁️)
2. **Se PDF/IMG**: Visualizador embutido (iframe)
3. **Se DOC/XLS**: Download automático
4. Sistema registra visualização em auditoria
5. Valida permissão de leitura
6. Verifica integridade (hash)

---

## ✅ Validações

Não há validações específicas para visualização além de permissões

---

## 📐 Regras de Negócio

- **RN-UC02-001**: Permissão granular (usuário/perfil/departamento)
- **RN-UC02-002**: Auditoria de visualizações
- **RN-UC02-003**: Validação de integridade por hash

---

## 🎨 Interface UI

```
┌─────────────────────────────────────────────────────────┐
│ Documento: Contrato_Prestacao_Servicos.pdf        [x] │
├─────────────────────────────────────────────────────────┤
│                                                         │
│              [Conteúdo do PDF renderizado]              │
│                                                         │
│                                                         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 🔍 Observações Técnicas

**Tipos Suportados:**
- **PDF/Imagens**: Visualizador embutido (iframe/PDF.js)
- **DOC/XLS**: Download direto
- **Vídeos**: Player HTML5 (se implementado)

---

# UC03 - Editar Metadados de Documento

**RF**: RF-020 - Gestão de Documentos e Anexos
**Complexidade**: Média
**Estimativa**: 4h Backend + 5h Frontend

---

## 📋 Objetivo

Editar nome, categoria, descrição, tags, validade (SEM substituir arquivo)

---

## 📝 Fluxo Principal

1. Usuário clica em "Editar" (📝)
2. Sistema exibe modal com campos:
   - Nome
   - Categoria
   - Descrição
   - Tags
   - Data Validade
3. Usuário modifica campos desejados
4. Clica em "Salvar"
5. Sistema registra em auditoria
6. Mensagem: "Metadados atualizados"

---

## ✅ Validações

| Campo | Regra |
|-------|-------|
| Nome | 3-200 chars |
| Categoria | Enum válido |
| Validade | Data futura (opcional) |

---

## 📐 Regras de Negócio

- **RN-UC03-001**: Apenas metadados, arquivo não muda
- **RN-UC03-002**: Nome único por contexto (ex: Ativo#123)

---

## 🎨 Interface UI

```
┌──────────────────────────────────────────────────────────┐
│ Editar Metadados                                   [x]  │
├──────────────────────────────────────────────────────────┤
│ Nome*: [Contrato_Prestacao_Servicos_______]             │
│ Categoria*: [Contratos ▼]                               │
│ Descrição:                                               │
│ ┌────────────────────────────────────────────────────┐  │
│ │Contrato de prestação de serviços entre XYZ...     │  │
│ └────────────────────────────────────────────────────┘  │
│ Tags: [contrato, prestacao, xyz]                        │
│ Data Validade: [31/12/2025]                             │
│                                                          │
│              [Cancelar] [Salvar Alterações]              │
└──────────────────────────────────────────────────────────┘
```

---

## 🔍 Observações Técnicas

**IMPORTANTE**: Esta operação NÃO modifica o arquivo físico, apenas metadados no banco de dados.

Para substituir o arquivo, usar UC05 - Versionar Documento.

---

# UC04 - Excluir Documento

**RF**: RF-020 - Gestão de Documentos e Anexos
**Complexidade**: Baixa
**Estimativa**: 3h Backend + 2h Frontend

---

## 📋 Objetivo

Soft delete de documento preservando histórico e permitindo recuperação

---

## 📝 Fluxo Principal

1. Usuário clica em "Excluir" (🗑️)
2. Sistema exibe modal: "Tem certeza? Documento pode ser recuperado dentro de 30 dias."
3. Usuário confirma
4. Sistema marca `Fl_Excluido = 1`, `Dt_Exclusao = NOW()`
5. Job Hangfire deleta permanentemente após 30 dias
6. Mensagem: "Documento movido para lixeira"

---

## ✅ Validações

Não há validações específicas além de permissões

---

## 📐 Regras de Negócio

- **RN-UC04-001**: Soft delete com período de recuperação (30 dias)
- **RN-UC04-002**: Exclusão permanente após 30 dias

---

## 🎨 Interface UI

```
┌──────────────────────────────────────────────────────────┐
│ ⚠️ Confirmar Exclusão                              [x]  │
├──────────────────────────────────────────────────────────┤
│ Documento: Contrato_Prestacao_Servicos.pdf              │
│                                                          │
│ Tem certeza que deseja excluir este documento?          │
│                                                          │
│ ℹ️ O documento será movido para a lixeira e poderá      │
│   ser recuperado dentro de 30 dias. Após este período,  │
│   será excluído permanentemente.                         │
│                                                          │
│              [Cancelar] [⚠️ Confirmar Exclusão]         │
└──────────────────────────────────────────────────────────┘
```

---

## 🔍 Observações Técnicas

**Fluxos Alternativos:**

**FA-01: Recuperar Documento**
- Listagem de documentos excluídos
- Botão "Restaurar"
- Sistema marca `Fl_Excluido = 0`, limpa `Dt_Exclusao`

**Job Hangfire:**
- Executa diariamente
- Busca documentos com `Fl_Excluido = 1` e `Dt_Exclusao < GETDATE() - 30 dias`
- Deleta permanentemente arquivo e registro

---

# UC05 - Gerar Documento a partir de Template

**RF**: RF-063 | **Ator**: Usuário, Sistema (auto) | **Complexidade**: Alta | **Estimativa**: 15h

## 1. OBJETIVO
Gerar documento finalizado (HTML/PDF) aplicando dados reais às variáveis do template.

## 2. PRÉ-CONDIÇÕES
Autenticado, template ativo, dados de entrada válidos (JSON com variáveis)

## 3. DEPENDÊNCIAS
**Pré-req**: UC00-04 | **Ordem**: Backend RenderCommand → Template engine (Handlebars/Liquid) → PDF generator
**Integra**: RF-020 (salvar documento gerado), RF-003 (audit)

## 4. FLUXO PRINCIPAL
1. Sistema/usuário chama endpoint com templateId + data → 2. Busca template → 3. Valida variáveis → 4. Substitui {{variáveis}} por valores → 5. Renderiza HTML → 6. (Opcional) Converte para PDF → 7. Retorna documento → 8. Auditoria

## 5. FLUXOS ALTERNATIVOS
**FA01**: Gerar apenas HTML (não PDF)
**FA02**: Salvar documento gerado no RF-020
**FA03**: Enviar por email após gerar

## 6. FLUXOS DE EXCEÇÃO
**FE01**: Template não encontrado | **FE02**: Variável faltando nos dados | **FE03**: Erro no PDF generator | **FE04**: Template inválido/corrompido

## 7. VALIDAÇÕES
**Entrada**: templateId (GUID), data (JSON), format (html|pdf)
**Validar**: Todas variáveis do template presentes nos dados

## 8. REGRAS DE NEGÓCIO
**RN01**: Engine Handlebars ou Liquid (configurável)
**RN02**: Sanitizar dados antes de inserir (XSS)
**RN03**: Auditoria de geração
**RN04**: Timeout 30s para geração

## 9. NÃO-FUNCIONAIS
Performance < 5s (HTML), < 10s (PDF) | Segurança sanitizar dados | Escalabilidade fila async para lote

## 10. UI
```
POST /api/templates/{id}/render
Body: {
  "data": {
    "nome_cliente": "João Silva",
    "data_contrato": "20/11/2025",
    "valor": "R$ 1.500,00"
  },
  "format": "pdf"
}
Response: Base64 do PDF ou HTML
```

## 11. RASTREABILIDADE
**RF**: RF-063 §2.6 | **Testes**: CN-UC05-001 a CN-UC05-012 | **API**: POST /api/templates/{id}/render

---

# UC05 - Gerenciar Versões de Documento

**RF**: RF-020 - Gestão de Documentos e Anexos
**Complexidade**: Média
**Estimativa**: 6h Backend + 7h Frontend

---

## 📋 Objetivo

Visualizar histórico de versões, comparar, fazer rollback

---

## 📝 Fluxo Principal

1. Usuário acessa documento e clica em "Versões"
2. Sistema lista todas as versões: v1, v2, v3 (atual)
3. Exibe: Versão, Data, Usuário, Tamanho, Diff (se aplicável)
4. **Ação 1**: Baixar versão específica
5. **Ação 2**: Comparar v2 vs v3 (diff visual se PDF/IMG)
6. **Ação 3**: Rollback para v2 → Cria v4 com conteúdo de v2

---

## ✅ Validações

Não há validações específicas além de permissões

---

## 📐 Regras de Negócio

- **RN-UC05-001**: Versionamento automático ao substituir arquivo
- **RN-UC05-002**: `Fl_Versao_Atual` marca versão ativa
- **RN-UC05-003**: Rollback cria nova versão (não sobrescreve)

---

## 🎨 Interface UI

```
┌──────────────────────────────────────────────────────────┐
│ Histórico de Versões - Contrato.pdf             [x]    │
├──────────────────────────────────────────────────────────┤
│ Versão Atual: v3 (20/01/2025)                           │
├────────┬────────────┬──────────┬──────────┬─────────────┤
│ Versão │ Data       │ Usuário  │ Tamanho  │ Ações       │
├────────┼────────────┼──────────┼──────────┼─────────────┤
│ v3 ⭐  │ 20/01/2025 │ João     │ 2.5 MB   │[⬇️][👁️]    │
│ v2     │ 15/01/2025 │ Maria    │ 2.3 MB   │[⬇️][👁️][↩️]│
│ v1     │ 10/01/2025 │ Pedro    │ 2.1 MB   │[⬇️][👁️][↩️]│
└────────┴────────────┴──────────┴──────────┴─────────────┘
[Comparar Versões]
```

---

## 🔍 Observações Técnicas

**Comparação de Versões:**
- PDFs: Diff visual lado a lado
- Imagens: Overlay com transparência
- Documentos: Diff textual (se OCR disponível)

**Rollback:**
- Não sobrescreve versão antiga
- Cria nova versão com conteúdo antigo
- Preserva histórico completo

---

# UC06 - Compartilhar Documento via Link Seguro

**RF**: RF-020 - Gestão de Documentos e Anexos
**Complexidade**: Alta
**Estimativa**: 8h Backend + 6h Frontend

---

## 📋 Objetivo

Gerar link temporário com senha para compartilhamento externo seguro

---

## 📝 Fluxo Principal

1. Usuário clica em "Compartilhar" (🔗)
2. Sistema exibe modal:
   - **Expiração**: 1h, 24h, 7 dias, 30 dias, customizado
   - **Senha**: Gerar aleatória ou definir manual
   - **Limite de downloads**: 1, 5, 10, ilimitado
3. Sistema gera token único: `https://app.com/share/{token}`
4. Armazena em `Documento_Compartilhamento_Link`
5. Usuário copia link e envia para destinatário
6. Destinatário acessa link, insere senha, baixa
7. Sistema registra download, decrementa contador
8. Ao expirar ou atingir limite: Link inválido

---

## ✅ Validações

| Campo | Regra |
|-------|-------|
| Expiração | Data futura |
| Senha | Mín 8 chars (se manual) |
| Limite downloads | > 0 ou ilimitado |

---

## 📐 Regras de Negócio

- **RN-UC06-001**: Links temporários com expiração obrigatória
- **RN-UC06-002**: Senha obrigatória para documentos sensíveis
- **RN-UC06-003**: Auditoria de acessos via link

---

## 🎨 Interface UI

```
┌──────────────────────────────────────────────────────────┐
│ Compartilhar Documento                             [x]  │
├──────────────────────────────────────────────────────────┤
│ Documento: Contrato_Prestacao_Servicos.pdf              │
│                                                          │
│ Expiração*:                                              │
│ ⚪ 1 hora  ⚪ 24 horas  ⚫ 7 dias  ⚪ 30 dias            │
│ ⚪ Customizado: [__/__/____ __:__]                      │
│                                                          │
│ Senha*:                                                  │
│ ⚫ Gerar aleatória (recomendado)                        │
│ ⚪ Definir manual: [________________]                   │
│                                                          │
│ Limite de Downloads*:                                    │
│ ⚪ 1  ⚪ 5  ⚫ 10  ⚪ Ilimitado                          │
│                                                          │
│ Link Gerado:                                             │
│ [https://app.com/share/abc123xyz____] [📋 Copiar]       │
│                                                          │
│ Senha: dk3n7p2q [👁️] [📋 Copiar]                        │
│                                                          │
│              [Fechar] [Gerar Novo Link]                  │
└──────────────────────────────────────────────────────────┘
```

---

## 🔍 Observações Técnicas

**Segurança:**
- Token único UUID v4
- Senha armazenada com hash bcrypt
- Rate limiting: 5 tentativas senha errada = bloqueio temporário
- Auditoria completa de acessos

---

# UC07 - Processar OCR em Documentos

**RF**: RF-020 - Gestão de Documentos e Anexos
**Complexidade**: Alta
**Estimativa**: 10h Backend + 4h Frontend

---

## 📋 Objetivo

Extração automática de texto de PDFs escaneados e imagens para busca full-text

---

## 📝 Fluxo Principal

1. Sistema detecta upload de PDF/IMG
2. Enfileira job Hangfire para OCR assíncrono
3. Job usa Azure Cognitive Services / Tesseract OCR
4. Extrai texto e armazena em `Documento.Texto_Extraido_OCR`
5. Indexa em Elasticsearch para busca full-text
6. Notifica usuário quando completo
7. Usuário pode buscar: "buscar: CNPJ 12.345.678/0001-99" → Encontra em documentos

---

## ✅ Validações

Não há validações específicas - processo assíncrono

---

## 📐 Regras de Negócio

- **RN-UC07-001**: OCR automático para PDF/PNG/JPG
- **RN-UC07-002**: Indexação full-text em Elasticsearch
- **RN-UC07-003**: Busca por conteúdo OCR + nome arquivo

---

## 🎨 Interface UI

```
┌──────────────────────────────────────────────────────────┐
│ Processamento OCR                                  [x]  │
├──────────────────────────────────────────────────────────┤
│ Documento: Contrato_Escaneado.pdf                       │
│                                                          │
│ Status: Processando...                                  │
│                                                          │
│ ┌────────────────────────────────────────────────────┐  │
│ │ ████████████████████░░░░░░░░░░░░░░░░░░░ 65%       │  │
│ └────────────────────────────────────────────────────┘  │
│                                                          │
│ Tempo estimado: 2 minutos                               │
│                                                          │
│              [Fechar] [Processar Novamente]              │
└──────────────────────────────────────────────────────────┘
```

---

## 🔍 Observações Técnicas

**Fluxo Alternativo FA-01: Re-processar OCR**
- Se texto extraído incorreto
- Usuário clica "Reprocessar"
- Sistema enfileira novamente

**Tecnologias:**
- Azure Cognitive Services (preferencial)
- Tesseract OCR (fallback)
- Elasticsearch para indexação full-text

---

## Histórico de Alterações

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 1.0 | 2025-12-17 | Sistema | Consolidação de 9 casos de uso |
