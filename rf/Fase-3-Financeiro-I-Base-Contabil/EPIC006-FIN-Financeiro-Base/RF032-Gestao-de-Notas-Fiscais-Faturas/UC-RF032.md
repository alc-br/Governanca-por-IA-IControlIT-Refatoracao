# UC-RF032 — Casos de Uso Canônicos

**RF:** RF032 — Gestão de Notas Fiscais e Faturas
**Versão:** 2.0
**Data:** 2025-12-31
**Autor:** Agência ALC - alc.dev.br
**Epic:** EPIC006-FIN-Financeiro-Base
**Fase:** Fase 3 - Financeiro I (Base Contábil)

---

## 1. OBJETIVO DO DOCUMENTO

Este documento descreve **todos os Casos de Uso (UC)** derivados do **RF032**, cobrindo integralmente o comportamento funcional esperado para gestão do ciclo completo de Notas Fiscais Eletrônicas (NF-e).

Os UCs aqui definidos servem como **contrato comportamental**, sendo a **fonte primária** para geração de:
- Casos de Teste (TC-RF032.yaml)
- Massas de Teste (MT-RF032.yaml)
- Evidências de auditoria e validação funcional
- Execução por agentes de IA (tester, QA, E2E)

---

## 2. SUMÁRIO DE CASOS DE USO

| ID | Nome | Ator Principal |
|----|------|----------------|
| UC00 | Listar Notas Fiscais | Usuário Autenticado |
| UC01 | Importar Nota Fiscal (XML/DANFE/CSV) | Usuário Autenticado |
| UC02 | Visualizar Nota Fiscal | Usuário Autenticado |
| UC03 | Validar Assinatura Digital | Sistema |
| UC04 | Conciliar Nota Fiscal com Pedido | Usuário Autenticado |

---

## 3. PADRÕES GERAIS APLICÁVEIS A TODOS OS UCs

- Todos os acessos respeitam **isolamento por tenant (FornecedorId)**
- Todas as ações exigem **permissão explícita (RBAC)**
- Erros não devem vazar informações sensíveis
- Auditoria deve registrar **quem**, **quando** e **qual ação**
- Mensagens devem ser claras, previsíveis e rastreáveis
- XMLs e DANFE armazenados em **Azure Blob Storage (7 anos)**
- Validação de assinatura digital **RSA-2048 com SHA-256 (ICP-Brasil)**

---

## UC00 — Listar Notas Fiscais

### Objetivo
Permitir que o usuário visualize todas as notas fiscais do seu tenant com filtros avançados.

### Pré-condições
- Usuário autenticado
- Permissão `fin:notasfiscais:read`

### Pós-condições
- Lista exibida conforme filtros e paginação

### Fluxo Principal
- **FP-UC00-001:** Usuário acessa funcionalidade Notas Fiscais
- **FP-UC00-002:** Sistema valida permissão
- **FP-UC00-003:** Sistema carrega notas do tenant (FornecedorId)
- **FP-UC00-004:** Sistema aplica paginação (50 registros/página)
- **FP-UC00-005:** Sistema exibe lista

### Fluxos Alternativos
- **FA-UC00-001:** Filtrar por período (data emissão/entrada)
- **FA-UC00-002:** Filtrar por status (aguardando, autorizada, rejeitada, cancelada, conciliada, paga)
- **FA-UC00-003:** Filtrar por emitente (CNPJ)
- **FA-UC00-004:** Filtrar por chave de acesso
- **FA-UC00-005:** Ordenar por coluna (data, valor, status)
- **FA-UC00-006:** Exportar para Excel/CSV

### Fluxos de Exceção
- **FE-UC00-001:** Usuário sem permissão → HTTP 403
- **FE-UC00-002:** Nenhuma nota cadastrada → estado vazio

### Regras de Negócio
- RN-NFE-032-01: Validação de estrutura XML (schema XSD 4.00 SEFAZ)
- RN-NFE-032-08: Armazenamento permanente em Azure Blob Storage (7 anos)

### Critérios de Aceite
- **CA-UC00-001:** A lista DEVE exibir apenas notas do tenant do usuário
- **CA-UC00-002:** Notas soft-deleted NÃO aparecem
- **CA-UC00-003:** Paginação DEVE ser aplicada (50 registros/página)
- **CA-UC00-004:** Sistema DEVE permitir ordenação por data, valor, status
- **CA-UC00-005:** Filtros DEVEM ser acumuláveis

---

## UC01 — Importar Nota Fiscal (XML/DANFE/CSV)

### Objetivo
Permitir importação de NF-e via XML, DANFE PDF (OCR) ou lote CSV.

### Pré-condições
- Usuário autenticado
- Permissão `fin:notasfiscais:importar`

### Pós-condições
- Nota importada e armazenada
- XML/DANFE salvos em Azure Blob Storage
- Auditoria registrada

### Fluxo Principal
- **FP-UC01-001:** Usuário seleciona arquivo (XML/PDF/CSV)
- **FP-UC01-002:** Sistema valida permissão
- **FP-UC01-003:** Sistema valida formato do arquivo
- **FP-UC01-004:** Sistema valida estrutura XML (schema XSD 4.00 SEFAZ)
- **FP-UC01-005:** Sistema extrai metadados (emitente, destinatário, itens, impostos)
- **FP-UC01-006:** Sistema valida chave de acesso (44 dígitos, unicidade)
- **FP-UC01-007:** Sistema salva XML/DANFE em Azure Blob Storage
- **FP-UC01-008:** Sistema cria registro NotaFiscal com FornecedorId automático
- **FP-UC01-009:** Sistema agenda validação de assinatura (UC03)
- **FP-UC01-010:** Sistema registra auditoria
- **FP-UC01-011:** Sistema confirma sucesso

### Fluxos Alternativos
- **FA-UC01-001:** Importar lote de XMLs (múltiplos arquivos)
- **FA-UC01-002:** Importar DANFE PDF → OCR (Azure Cognitive Services + Tesseract fallback)
- **FA-UC01-003:** Importar CSV com múltiplas chaves de acesso → download automático SEFAZ

### Fluxos de Exceção
- **FE-UC01-001:** Estrutura XML inválida → HTTP 400
- **FE-UC01-002:** Chave de acesso duplicada → HTTP 409
- **FE-UC01-003:** Assinatura digital inválida → HTTP 422
- **FE-UC01-004:** CNPJ emitente/destinatário inválido → HTTP 400
- **FE-UC01-005:** Arquivo corrompido → HTTP 400
- **FE-UC01-006:** OCR falhou (DANFE ilegível) → HTTP 422

### Regras de Negócio
- RN-NFE-032-01: Importação com validação XSD 4.00 SEFAZ
- RN-NFE-032-02: Validação de assinatura digital RSA-2048 SHA-256
- RN-NFE-032-08: Armazenamento em Azure Blob Storage (7 anos)
- RN-NFE-032-09: OCR de DANFE quando XML indisponível
- RN-NFE-032-10: Auditoria completa (7 anos)

### Critérios de Aceite
- **CA-UC01-001:** FornecedorId DEVE ser preenchido automaticamente
- **CA-UC01-002:** Chave de acesso DEVE ser única por tenant
- **CA-UC01-003:** XML e DANFE DEVEM ser salvos em Azure Blob Storage
- **CA-UC01-004:** Sistema DEVE agendar validação de assinatura
- **CA-UC01-005:** Auditoria DEVE ser registrada APÓS sucesso
- **CA-UC01-006:** Importação em lote DEVE processar até 100 XMLs/lote
- **CA-UC01-007:** OCR DEVE tentar Azure Cognitive Services primeiro, fallback Tesseract

---

## UC02 — Visualizar Nota Fiscal

### Objetivo
Permitir visualização completa de uma nota fiscal com todos metadados, impostos, divergências e histórico.

### Pré-condições
- Usuário autenticado
- Permissão `fin:notasfiscais:read`

### Pós-condições
- Dados exibidos corretamente

### Fluxo Principal
- **FP-UC02-001:** Usuário seleciona nota na listagem
- **FP-UC02-002:** Sistema valida permissão
- **FP-UC02-003:** Sistema valida tenant (FornecedorId)
- **FP-UC02-004:** Sistema carrega dados completos (cabeçalho, itens, impostos)
- **FP-UC02-005:** Sistema carrega divergências (se houver)
- **FP-UC02-006:** Sistema carrega histórico de aprovações
- **FP-UC02-007:** Sistema carrega rateios (se houver)
- **FP-UC02-008:** Sistema exibe dados formatados

### Fluxos Alternativos
- **FA-UC02-001:** Download XML original
- **FA-UC02-002:** Download DANFE PDF
- **FA-UC02-003:** Visualizar pedido vinculado (se conciliada)
- **FA-UC02-004:** Visualizar organograma de rateio
- **FA-UC02-005:** Consultar status SEFAZ (atualização em tempo real)

### Fluxos de Exceção
- **FE-UC02-001:** Nota não encontrada → HTTP 404
- **FE-UC02-002:** Nota de outro tenant → HTTP 404
- **FE-UC02-003:** Erro ao consultar SEFAZ → exibir último status conhecido

### Regras de Negócio
- RN-NFE-032-03: Consulta automática de status SEFAZ
- RN-NFE-032-05: Cálculo automático de impostos

### Critérios de Aceite
- **CA-UC02-001:** Usuário SÓ pode visualizar notas do próprio tenant
- **CA-UC02-002:** Informações de auditoria DEVEM ser exibidas
- **CA-UC02-003:** Tentativa de acessar nota de outro tenant → HTTP 404
- **CA-UC02-004:** Sistema DEVE exibir status SEFAZ atualizado
- **CA-UC02-005:** Downloads XML/DANFE DEVEM vir de Azure Blob Storage

---

## UC03 — Validar Assinatura Digital

### Objetivo
Validar assinatura digital RSA-2048 com SHA-256 conforme ICP-Brasil.

### Pré-condições
- Nota fiscal importada
- XML disponível

### Pós-condições
- Assinatura validada ou rejeitada
- Status atualizado
- Auditoria registrada

### Fluxo Principal
- **FP-UC03-001:** Sistema agenda validação (job assíncrono)
- **FP-UC03-002:** Sistema baixa XML de Azure Blob Storage
- **FP-UC03-003:** Sistema extrai certificado digital
- **FP-UC03-004:** Sistema valida certificado ICP-Brasil
- **FP-UC03-005:** Sistema verifica assinatura RSA-2048 SHA-256
- **FP-UC03-006:** Sistema valida cadeia de certificação
- **FP-UC03-007:** Sistema atualiza status (assinatura_validada ou rejeitada)
- **FP-UC03-008:** Sistema registra auditoria
- **FP-UC03-009:** Sistema agenda consulta SEFAZ

### Fluxos Alternativos
- **FA-UC03-001:** Validação manual (se job automático falhar)

### Fluxos de Exceção
- **FE-UC03-001:** Certificado expirado → status = rejeitada
- **FE-UC03-002:** Assinatura corrompida → status = rejeitada
- **FE-UC03-003:** Cadeia de certificação inválida → status = rejeitada
- **FE-UC03-004:** Certificado não é ICP-Brasil → status = rejeitada

### Regras de Negócio
- RN-NFE-032-02: Validação de assinatura digital RSA-2048 SHA-256 ICP-Brasil

### Critérios de Aceite
- **CA-UC03-001:** Assinatura DEVE ser validada em até 30 segundos
- **CA-UC03-002:** Sistema DEVE validar cadeia completa ICP-Brasil
- **CA-UC03-003:** Certificado expirado DEVE rejeitar nota
- **CA-UC03-004:** Auditoria DEVE registrar thumbprint do certificado
- **CA-UC03-005:** Falha na validação DEVE bloquear prosseguimento

---

## UC04 — Conciliar Nota Fiscal com Pedido

### Objetivo
Reconciliar NF-e com pedido (RF026), detectar e classificar divergências.

### Pré-condições
- Usuário autenticado
- Permissão `fin:notasfiscais:conciliar`
- Nota com assinatura validada
- Nota autorizada pela SEFAZ

### Pós-condições
- Nota conciliada ou divergências detectadas
- Workflow de aprovação iniciado (se divergência crítica)

### Fluxo Principal
- **FP-UC04-001:** Usuário solicita conciliação manual OU sistema executa automático
- **FP-UC04-002:** Sistema valida permissão
- **FP-UC04-003:** Sistema localiza pedido vinculado (RF026)
- **FP-UC04-004:** Sistema compara valores (quantidade, valor unitário, valor total)
- **FP-UC04-005:** Sistema compara metadados (CFOP, NCM, CST)
- **FP-UC04-006:** Sistema calcula divergência percentual
- **FP-UC04-007:** Sistema classifica divergência (crítica >5%, importante 1-5%, menor <1%)
- **FP-UC04-008:** Sistema atualiza status (conciliada OU divergencia_detectada)
- **FP-UC04-009:** Sistema registra auditoria

### Fluxos Alternativos
- **FA-UC04-001:** Divergência <1% → auto-ajuste automático → conciliada
- **FA-UC04-002:** Divergência 1-5% → sinaliza warning → permite aprovar
- **FA-UC04-003:** Divergência >5% → status = aprovacao_pendente → workflow

### Fluxos de Exceção
- **FE-UC04-001:** Pedido não encontrado → HTTP 404
- **FE-UC04-002:** Pedido de outro tenant → HTTP 403
- **FE-UC04-003:** Divergência crítica não aprovada → status = bloqueada

### Regras de Negócio
- RN-NFE-032-04: Detecção de divergências (<1% auto, >5% bloqueio)
- RN-NFE-032-06: Bloqueio de pagamento se divergência crítica não aprovada

### Critérios de Aceite
- **CA-UC04-001:** Divergência <1% DEVE ser auto-ajustada
- **CA-UC04-002:** Divergência >5% DEVE bloquear pagamento
- **CA-UC04-003:** Sistema DEVE classificar divergência (crítica, importante, menor)
- **CA-UC04-004:** Divergência crítica DEVE iniciar workflow de aprovação
- **CA-UC04-005:** Auditoria DEVE registrar valores divergentes

---

## 4. MATRIZ DE RASTREABILIDADE

| UC | Regras de Negócio |
|----|------------------|
| UC00 | RN-NFE-032-01, RN-NFE-032-08 |
| UC01 | RN-NFE-032-01, RN-NFE-032-02, RN-NFE-032-08, RN-NFE-032-09, RN-NFE-032-10 |
| UC02 | RN-NFE-032-03, RN-NFE-032-05 |
| UC03 | RN-NFE-032-02 |
| UC04 | RN-NFE-032-04, RN-NFE-032-06 |

---

## CHANGELOG

| Versão | Data | Autor | Descrição |
|------|------|-------|-----------|
| 2.0 | 2025-12-31 | Agência ALC - alc.dev.br | Versão canônica completa com 5 UCs (UC00-UC04) |
| 1.0 | 2025-01-14 | Architect Agent | Versão stub incompleta |
