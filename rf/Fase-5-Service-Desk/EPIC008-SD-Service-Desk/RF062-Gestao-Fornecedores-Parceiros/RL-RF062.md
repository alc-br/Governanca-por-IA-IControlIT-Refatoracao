# RL-RF062 — Referência ao Legado

**Versão:** 1.0
**Data:** 2025-12-30
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF062 - Gestão de Fornecedores e Parceiros
**Sistema Legado:** VB.NET + ASP.NET Web Forms
**Objetivo:** Documentar análise do legado para identificar funcionalidades relacionadas e fundamentar decisões de modernização.

---

## 1. CONTEXTO DO LEGADO

### Visão Geral

O sistema legado IControlIT v1.0 **não possuía módulo dedicado à gestão de fornecedores e parceiros**. Esta é uma funcionalidade **NOVA** no sistema modernizado, criada para atender demandas identificadas durante o processo de modernização.

### Stack Tecnológica Original

- **Arquitetura:** Monolítica ASP.NET Web Forms
- **Linguagem:** VB.NET (.NET Framework 4.7.2)
- **Banco de Dados:** SQL Server (multi-database por cliente)
- **Interface:** WebForms com master pages
- **Serviços:** SOAP WebServices (.asmx)
- **Multi-tenant:** Segregação por banco de dados separados
- **Auditoria:** Parcial (apenas algumas tabelas críticas)
- **Configurações:** web.config com strings criptografadas (algoritmo proprietário)

### Análise de Funcionalidades Relacionadas no Legado

Durante a análise do código legado, foram identificadas as seguintes funcionalidades que **tangenciam** o conceito de fornecedores, mas não constituem um módulo formal:

1. **Contratos (módulo Contrato):**
   - Telas: `Contrato\Contrato.aspx`, `Contrato\Contrato_SLA_Operacao.aspx`
   - Contratos eram cadastrados **sem vínculo formal com fornecedores**
   - Não havia controle de documentação de fornecedores
   - Não havia processo de homologação

2. **Solicitações e Chamados:**
   - Telas: `Chamado\Solicitacao.aspx`, `Chamado\Fila_Atendimento.aspx`
   - OSs eram atribuídas a **técnicos internos**, sem opção de atribuir a fornecedores externos
   - Não havia rastreamento de fornecedores atendendo chamados

3. **Estoque e Notas Fiscais:**
   - Telas: `Estoque\Nota_Fiscal.aspx`
   - Notas fiscais eram cadastradas, mas sem vínculo estruturado com fornecedores
   - Não havia validação de CNPJ ou documentação do fornecedor

### Problemas Arquiteturais Identificados

1. **Ausência de entidade Fornecedor:**
   - Informações de fornecedores eram armazenadas como texto livre em diversos lugares
   - CNPJ e Razão Social duplicados em múltiplas tabelas
   - Impossibilidade de rastrear histórico de atendimentos por fornecedor

2. **Falta de compliance documental:**
   - Nenhum controle de certidões obrigatórias (CND Federal, Estadual, Municipal)
   - Risco legal por contratação de fornecedores sem documentação válida

3. **Gestão de contratos descentralizada:**
   - Contratos cadastrados sem vínculo com fornecedor
   - Alertas de vencimento inexistentes
   - SLA não monitorado automaticamente

4. **Avaliação manual e não estruturada:**
   - Performance de fornecedores avaliada informalmente
   - Decisões de contratação baseadas em memória individual dos gestores
   - Ausência de ranking ou métricas objetivas

---

## 2. TELAS DO LEGADO

### Análise: Nenhuma tela específica encontrada

**Status:** ❌ **Não existente no legado**

**Conclusão:** O módulo de Gestão de Fornecedores e Parceiros é uma **funcionalidade nova**, sem equivalente direto no sistema legado.

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

### Análise: Nenhum webservice específico encontrado

| Método | Local | Responsabilidade | Observações |
|------|-------|------------------|-------------|
| N/A | N/A | N/A | Nenhum webservice dedicado a fornecedores identificado |

**Status:** ❌ **Não existente no legado**

**Funcionalidades Parciais Identificadas:**
- `WSContrato.asmx`: Cadastro de contratos sem vínculo formal com fornecedores
- `WSCadastro.asmx`: CRUD de entidades genéricas, sem fornecedor

---

## 4. STORED PROCEDURES

### Análise: Nenhuma procedure específica encontrada

| Procedure | Finalidade | Problemas Identificados |
|-------|------------|-------------------------|
| N/A | N/A | Nenhuma procedure dedicada a fornecedores identificada |

**Status:** ❌ **Não existente no legado**

---

## 5. TABELAS LEGADAS

### Análise: Nenhuma tabela dedicada identificada

| Tabela | Finalidade | Problemas Identificados |
|-------|------------|-------------------------|
| `Contrato` | Armazenamento de contratos | Sem FK para fornecedor (dados em texto livre) |
| `Nota_Fiscal` | Armazenamento de NFs | CNPJ e Razão Social em campos texto (sem validação) |
| `Solicitacao` | Solicitações e chamados | Sem suporte a atribuição para fornecedores externos |

**Problemas Identificados:**
- Informações de fornecedores espalhadas em múltiplas tabelas como texto livre
- Falta de normalização e integridade referencial
- Impossibilidade de rastrear histórico consolidado por fornecedor
- Ausência de auditoria específica para operações com fornecedores

---

## 6. REGRAS DE NEGÓCIO IMPLÍCITAS

### Análise: Regras não documentadas encontradas no código

**RL-RN-001: Contratos tinham campo texto para "Fornecedor"**
- **Fonte:** `Contrato\Contrato.aspx.vb` (linha ~150)
- **Descrição:** Campo `txtFornecedor` (TextBox) permitia entrada livre sem validação de CNPJ
- **Problema:** Dados inconsistentes, duplicação de fornecedores com grafias diferentes
- **Decisão Moderna:** Criar entidade Fornecedor com CNPJ validado e tabela normalizada

**RL-RN-002: Notas fiscais armazenavam CNPJ sem validação**
- **Fonte:** `Estoque\Nota_Fiscal.aspx.vb` (linha ~200)
- **Descrição:** CNPJ armazenado como VARCHAR(18) sem validação de dígitos verificadores
- **Problema:** CNPJs inválidos cadastrados, impossibilidade de consolidar por fornecedor
- **Decisão Moderna:** Validar CNPJ com algoritmo de dígitos verificadores no backend

**RL-RN-003: Sem controle de documentação vencida**
- **Fonte:** Nenhuma implementação encontrada
- **Descrição:** Sistema não controlava validade de certidões ou documentos de fornecedores
- **Problema:** Risco legal e de compliance
- **Decisão Moderna:** Implementar controle de vencimentos com alertas automáticos (D-30, D-15, D-7)

**RL-RN-004: SLA de contratos não monitorado**
- **Fonte:** `Contrato\Contrato_SLA_Operacao.aspx.vb`
- **Descrição:** SLA era cadastrado, mas não havia medição automática de cumprimento
- **Problema:** Impossibilidade de avaliar performance contratual objetivamente
- **Decisão Moderna:** Implementar medição automática de SLA com base em atendimentos reais

**RL-RN-005: Alertas de renovação manuais**
- **Fonte:** Nenhuma implementação automatizada encontrada
- **Descrição:** Gestores eram alertados manualmente sobre vencimentos de contratos
- **Problema:** Atrasos em renovações, perda de prazos de negociação
- **Decisão Moderna:** Implementar job diário com alertas em D-90, D-60 e D-30

---

## 7. GAP ANALYSIS (LEGADO x RF MODERNO)

| Funcionalidade | Existe no Legado | Existe no RF Moderno | Observação |
|-----|--------|------------|------------|
| Cadastro formal de Fornecedores | ❌ Não | ✅ Sim | **NOVA**: Entidade dedicada com CNPJ, categoria, status |
| Upload de documentação obrigatória | ❌ Não | ✅ Sim | **NOVA**: Controle de CNDs com validação de vencimentos |
| Processo de homologação | ❌ Não | ✅ Sim | **NOVA**: Workflow de aprovação formal |
| Múltiplos contatos por fornecedor | ❌ Não | ✅ Sim | **NOVA**: Contatos por departamento (comercial, técnico, financeiro) |
| Contratos vinculados a fornecedores | ⚠️ Parcial | ✅ Sim | **MODERNIZADO**: No legado, fornecedor era texto livre |
| SLA por fornecedor | ⚠️ Parcial | ✅ Sim | **MODERNIZADO**: No legado, SLA não era medido automaticamente |
| Avaliação periódica de fornecedores | ❌ Não | ✅ Sim | **NOVA**: Avaliações trimestrais com notas 1-5 |
| Ranking de fornecedores | ❌ Não | ✅ Sim | **NOVA**: Score automático (avaliação 60% + SLA 40%) |
| Alertas de vencimento de documentos | ❌ Não | ✅ Sim | **NOVA**: Jobs diários com alertas D-30, D-15, D-7 |
| Alertas de renovação de contratos | ❌ Não | ✅ Sim | **NOVA**: Jobs diários com alertas D-90, D-60, D-30 |
| Bloqueio automático por doc vencida | ❌ Não | ✅ Sim | **NOVA**: Bloqueio automático + flag visível |
| Dashboard de performance | ❌ Não | ✅ Sim | **NOVA**: Métricas em tempo real |
| Histórico de atendimentos | ❌ Não | ✅ Sim | **NOVA**: Rastreamento completo por fornecedor |
| Export para compliance | ❌ Não | ✅ Sim | **NOVA**: Relatórios Excel/PDF para auditoria |
| Integração com Solicitações/OSs | ❌ Não | ✅ Sim | **NOVA**: Vínculo automático ao atribuir OS |
| Multi-tenancy moderno | ⚠️ Parcial | ✅ Sim | **MODERNIZADO**: No legado, segregação por banco; moderno usa EmpresaId |
| Auditoria completa | ⚠️ Parcial | ✅ Sim | **MODERNIZADO**: No legado, auditoria parcial; moderno audita tudo |

### Legenda:
- ✅ **Sim**: Funcionalidade completa
- ⚠️ **Parcial**: Funcionalidade incompleta ou implementada de forma diferente
- ❌ **Não**: Funcionalidade não existente

---

## 8. DECISÕES DE MODERNIZAÇÃO

### Decisão 1: Criar módulo completo de Fornecedores (NOVO)

**Motivo:** O legado não possuía gestão formal de fornecedores. Informações eram espalhadas e inconsistentes, causando:
- Duplicação de dados
- Impossibilidade de rastreamento histórico
- Risco de compliance legal (documentação não controlada)
- Decisões de contratação sem embasamento objetivo

**Impacto:** **ALTO**
- Nova entidade no domínio
- Novas tabelas no banco de dados
- Novos endpoints de API
- Novas telas no frontend
- Jobs de alertas automáticos (Hangfire)

---

### Decisão 2: Implementar controle de documentação obrigatória com criptografia

**Motivo:** Atender requisitos de compliance (LGPD, auditoria legal) e proteger documentos sensíveis (CNDs, CNPJ).

**Impacto:** **ALTO**
- Upload de arquivos com validação de tipo (whitelist: PDF, JPEG, PNG)
- Armazenamento com criptografia AES-256
- Controle de vencimentos com job diário
- Alertas automáticos D-30, D-15, D-7

---

### Decisão 3: Implementar processo de homologação formal

**Motivo:** Garantir que apenas fornecedores qualificados e com documentação completa sejam habilitados para receber ordens de serviço.

**Impacto:** **MÉDIO**
- Workflow de aprovação (estados: rascunho → em_analise → ativo)
- Campos de aprovador, data de aprovação, justificativa
- Bloqueio automático para fornecedores não homologados

---

### Decisão 4: Criar sistema de avaliação e ranking

**Motivo:** Fornecer dados objetivos para decisões de contratação e renovação contratual.

**Impacto:** **MÉDIO**
- Avaliações trimestrais (4 dimensões: Qualidade, Prazo, Custo, Atendimento)
- Cálculo de ranking automático (peso avaliação 60% + SLA 40%)
- Job mensal para recálculo de ranking

---

### Decisão 5: Integrar com sistema de Solicitações e OSs

**Motivo:** Rastrear histórico real de atendimentos para alimentar avaliações e SLA.

**Impacto:** **ALTO**
- Modificação no módulo de Solicitações (RF021) para incluir fornecedor
- Vínculo automático ao atribuir OS a fornecedor
- Cálculo de SLA compliance baseado em atendimentos reais

---

## 9. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Probabilidade | Mitigação |
|------|---------|---------------|-----------|
| **Dados de fornecedores espalhados no legado** | Alto | Alta | Criar script de migração para consolidar dados de `Contrato`, `Nota_Fiscal` e outros em entidade `Fornecedor`. Normalizar CNPJs duplicados. |
| **Falta de documentação histórica** | Médio | Alta | Aceitar que fornecedores migrados não terão documentação completa inicialmente. Exigir documentação apenas para novos ou para reativação. |
| **Resistência de usuários ao workflow de homologação** | Médio | Média | Treinar gestores sobre benefícios de compliance e redução de riscos legais. Permitir homologação em lote para fornecedores históricos confiáveis. |
| **Sobrecarga de alertas iniciais** | Baixo | Média | Implementar período de grace (30 dias) após migração antes de ativar alertas automáticos. Comunicar usuários com antecedência. |
| **Performance com 10.000+ fornecedores** | Médio | Baixa | Implementar paginação, índices otimizados e cache de rankings. Validar performance em ambiente de homologação. |

---

## 10. RASTREABILIDADE (LEGADO → MODERNO)

| Elemento Legado | Referência RF Moderno | Status |
|----------------|---------------|--------|
| Campo texto "Fornecedor" em `Contrato.aspx` | RN-RF062-005 (Contratos Vinculados) | **SUBSTITUÍDO** por FK para entidade Fornecedor |
| CNPJ em `Nota_Fiscal` (VARCHAR sem validação) | RN-RF062-002 (Documentação Obrigatória) | **SUBSTITUÍDO** por validação de CNPJ com dígitos verificadores |
| SLA em `Contrato_SLA_Operacao.aspx` (sem medição) | RN-RF062-006 (SLA por Fornecedor) | **SUBSTITUÍDO** por medição automática com base em atendimentos |
| N/A (não existia) | RN-RF062-003 (Alertas de Vencimento) | **NOVO** - Job diário com alertas D-30, D-15, D-7 |
| N/A (não existia) | RN-RF062-014 (Homologação) | **NOVO** - Workflow de aprovação formal |
| N/A (não existia) | RN-RF062-007 (Avaliações Periódicas) | **NOVO** - Avaliações trimestrais estruturadas |
| N/A (não existia) | RN-RF062-008 (Ranking) | **NOVO** - Score automático por categoria |
| N/A (não existia) | RN-RF062-010 (Integração com Solicitações) | **NOVO** - Vínculo automático em OSs |

---

## 11. SCRIPT DE MIGRAÇÃO SUGERIDO

Como o legado **não possui tabela dedicada de fornecedores**, a migração consistirá em:

### Fase 1: Consolidação de Dados Espalhados

```sql
-- Script conceitual (adaptar conforme bancos legados)

-- 1. Extrair fornecedores únicos de Contratos
INSERT INTO Fornecedor (CNPJ, RazaoSocial, Categoria, EmpresaId, Status, Homologado)
SELECT DISTINCT
    CNPJ_FORNECEDOR,
    RAZAO_SOCIAL_FORNECEDOR,
    'PrestadorServico', -- Categoria padrão (ajustar manualmente depois)
    EMPRESA_ID,
    'ativo', -- Aceitar fornecedores históricos como ativos inicialmente
    true -- Homologar automaticamente fornecedores com contratos ativos
FROM Contrato_Legado
WHERE CNPJ_FORNECEDOR IS NOT NULL AND LEN(CNPJ_FORNECEDOR) = 14;

-- 2. Extrair fornecedores de Notas Fiscais (se ainda não existirem)
INSERT INTO Fornecedor (CNPJ, RazaoSocial, Categoria, EmpresaId, Status, Homologado)
SELECT DISTINCT
    CNPJ_EMISSOR,
    RAZAO_SOCIAL_EMISSOR,
    'Fabricante', -- Categoria padrão
    EMPRESA_ID,
    'ativo',
    false -- Não homologar automaticamente (falta documentação)
FROM Nota_Fiscal_Legado
WHERE CNPJ_EMISSOR IS NOT NULL
  AND LEN(CNPJ_EMISSOR) = 14
  AND NOT EXISTS (SELECT 1 FROM Fornecedor WHERE CNPJ = CNPJ_EMISSOR);

-- 3. Vincular contratos migrados aos fornecedores
UPDATE Contrato_Moderno
SET FornecedorId = F.Id
FROM Fornecedor F
WHERE Contrato_Moderno.CNPJ_Fornecedor_Texto = F.CNPJ;
```

### Fase 2: Limpeza e Validação

```sql
-- 1. Remover fornecedores com CNPJ inválido
DELETE FROM Fornecedor WHERE LEN(CNPJ) <> 14;

-- 2. Consolidar fornecedores duplicados (mesmo CNPJ, grafias diferentes)
-- (Script manual com validação de impacto em contratos)

-- 3. Criar contato padrão para fornecedores sem contato
INSERT INTO ContatoFornecedor (FornecedorId, Nome, Departamento, Email, Telefone, Primario)
SELECT
    Id,
    'Contato Principal',
    'COMERCIAL',
    Email,
    Telefone,
    true
FROM Fornecedor
WHERE NOT EXISTS (SELECT 1 FROM ContatoFornecedor WHERE FornecedorId = Fornecedor.Id);
```

### Fase 3: Comunicação e Treinamento

- Comunicar gestores sobre necessidade de upload de documentação para fornecedores migrados
- Estabelecer período de grace de 30 dias antes de ativar bloqueios automáticos
- Treinar equipe sobre processo de homologação e avaliação

---

## 12. CONCLUSÃO

O RF062 (Gestão de Fornecedores e Parceiros) é uma **funcionalidade majoritariamente NOVA** no sistema modernizado, sem equivalente direto no legado. A análise identificou que:

1. **80% do RF é novo**: Entidade Fornecedor, documentação, homologação, avaliações, ranking, alertas, dashboard
2. **20% do RF substitui funcionalidades parciais**: Contratos (agora vinculados formalmente a fornecedores), SLA (agora medido automaticamente)
3. **Principais benefícios da modernização**:
   - Compliance legal (controle de certidões)
   - Decisões baseadas em dados (avaliações + ranking)
   - Automação de alertas (redução de riscos)
   - Rastreabilidade de histórico (OSs vinculadas a fornecedores)

4. **Principais desafios**:
   - Migração de dados espalhados no legado
   - Treinamento de usuários em novo workflow
   - Upload inicial de documentação de fornecedores históricos

**Recomendação:** Implementar RF062 como módulo independente, com integração progressiva com módulos existentes (Contratos, Solicitações, Estoque).

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|------|------|----------|------|
| 1.0 | 2025-12-30 | Criação do documento de referência ao legado (funcionalidade nova) | Agência ALC - alc.dev.br |
