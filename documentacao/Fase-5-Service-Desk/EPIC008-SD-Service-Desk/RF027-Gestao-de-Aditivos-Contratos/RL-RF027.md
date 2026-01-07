# RL-RF027 — Referência ao Legado: Gestão de Aditivos de Contratos

**Versão:** 1.0
**Data:** 2025-12-30
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** [RF-027](./RF027.md)
**Sistema Legado:** IControlIT VB.NET + ASP.NET Web Forms
**Objetivo:** Documentar o comportamento do legado que serve de base para a refatoração, garantindo rastreabilidade, entendimento histórico e mitigação de riscos de migração.

---

## 1. CONTEXTO DO LEGADO

### Arquitetura e Stack Técnica

- **Arquitetura:** Cliente-Servidor com ASP.NET Web Forms
- **Linguagem / Stack:** VB.NET + ASP.NET Web Forms (.NET Framework 4.5)
- **Banco de Dados:** SQL Server 2012 (tabela única para aditivos)
- **Multi-tenant:** Não (dados misturados sem isolamento adequado)
- **Auditoria:** Inexistente (sem rastreamento de alterações)
- **Configurações:** Web.config + banco de dados
- **Documentos:** Rede compartilhada (sem versionamento, PDFs perdidos frequentemente)

### Problemas Críticos do Legado

1. **Sobrescrevia Contrato Original**
   - Cada aditivo modificava diretamente o registro do contrato base
   - Histórico completamente perdido
   - Impossível saber valores anteriores ou quem alterou

2. **Sem Workflow de Aprovação**
   - Aprovação via email manual
   - Sem rastreamento formal
   - Sem SLA ou escalação
   - Aditivos eram criados e entravam em vigor imediatamente

3. **Cálculo Manual de Impacto Financeiro**
   - Planilha Excel separada do sistema
   - Desatualizada constantemente
   - Levava 4-6 horas por aditivo complexo
   - Erros de cálculo frequentes

4. **Documentos Perdidos**
   - PDFs salvos em `\\servidor\shared\contratos\aditivos\` (rede compartilhada)
   - Sem controle de versão
   - Sem backup adequado
   - Arquivos perdidos após reorganizações de pastas
   - Sem OCR ou extração de dados

5. **Tipos de Aditivo Inconsistentes**
   - Campo texto livre permitia: "acrescimo", "Acresc.", "add linhas", "adicionar", "+"
   - Impossível gerar relatórios confiáveis por tipo
   - Queries SQL complexas com múltiplos LIKE

6. **Sem Alertas de Vencimento**
   - Descobria-se que aditivo venceu somente após o fato
   - Renovações automáticas não eram detectadas
   - Oportunidades de renegociação perdidas

7. **Comparação Manual de Versões**
   - Track Changes do Word usado manualmente
   - Formatação quebrava constantemente
   - Processo demorado e propenso a erros

---

## 2. TELAS DO LEGADO

### Tela 1: Contrato\Aditivo.aspx

- **Caminho:** `ic1_legado/IControlIT/Contrato/Aditivo.aspx`
- **Responsabilidade:** Cadastro básico de aditivo contratual

#### Campos da Tela

| Campo | Tipo | Obrigatório | Observações |
|------|------|-------------|-------------|
| Id_Contrato | DropDownList | Sim | Lista todos os contratos (sem filtro, lento) |
| Tipo_Aditivo | TextBox | Sim | Texto livre → fonte de inconsistência |
| Descricao | TextBox (multiline) | Não | Máximo 500 caracteres |
| Valor_Alteracao | TextBox (decimal) | Sim | Sem contexto (mensal/anual?) |
| Dt_Inicio | TextBox + Calendar | Sim | Sem validação vs. contrato base |
| Dt_Fim | TextBox + Calendar | Não | Podia ser vazio (indefinido) |
| Fl_Ativo | CheckBox | Não | Default = True |
| Btn_Salvar | Button | - | Sem validações backend |

#### Comportamentos Implícitos

- **Validação de Data Ausente:** Permitia Dt_Inicio anterior a Dt_Inicio do contrato base
- **Sem Validação de Sobreposição:** Podia criar 2 aditivos do mesmo tipo vigentes simultaneamente
- **Sem Workflow:** Botão "Salvar" criava aditivo direto como "Ativo"
- **Sem Cálculo Automático:** Usuário preenchia Valor_Alteracao manualmente (propenso a erros)
- **Sem Upload de Documento:** Campo documento não existia na tela

### Tela 2: Contrato\ListaAditivos.aspx

- **Caminho:** `ic1_legado/IControlIT/Contrato/ListaAditivos.aspx`
- **Responsabilidade:** Listagem básica de aditivos por contrato

#### Campos da Tela

| Campo | Tipo | Obrigatório | Observações |
|------|------|-------------|-------------|
| Id_Contrato | DropDownList | Sim | Filtro principal |
| GridView_Aditivos | GridView | - | Sem paginação (lento com >50 aditivos) |

#### Comportamentos Implícitos

- **Query Lenta:** `SELECT *` sem paginação (>3 segundos com 50 aditivos)
- **Sem Filtros Avançados:** Só podia filtrar por contrato
- **Sem Ordenação:** Sempre ordenado por Id_Aditivo (não por data)
- **Edição Inline Perigosa:** Podia editar aditivo vigente sem validações
- **Sem Auditoria:** Não registrava quem editou ou quando

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

**Endpoint Base:** `http://servidor/IControlIT/Contrato.asmx`

| Método | Local | Responsabilidade | Observações |
|------|-------|------------------|-------------|
| **CriarAditivo()** | Contrato.asmx | Criar aditivo básico | SOAP. Entrada: IdContrato, TipoAditivo (texto livre), Descricao, Valor. Sem validações (permitia datas inválidas, tipos inconsistentes). Sem workflow. |
| **ListarAditivos()** | Contrato.asmx | Listar aditivos de um contrato | SOAP. Entrada: IdContrato. Saída: Array AditivoDto (sem paginação). Query lenta >3s com 50 aditivos. |
| **AprovarAditivo()** | Contrato.asmx | Aprovar aditivo | SOAP. Entrada: IdAditivo, IdUsuario. Saída: Boolean. Aprovação direta (sem níveis), sem rastreabilidade, sem DocuSign. |

### Problemas Identificados

1. **SOAP (obsoleto):** Tecnologia descontinuada, verbosa
2. **Sem Paginação:** ListarAditivos retorna todos os aditivos (performance ruim)
3. **Sem Validações:** CriarAditivo aceita qualquer entrada
4. **Aprovação Primitiva:** AprovarAditivo não valida permissões ou níveis
5. **Sem Versionamento:** Não cria versão do contrato após aditivo

---

## 4. TABELAS LEGADAS

| Tabela | Finalidade | Problemas Identificados |
|-------|------------|-------------------------|
| **Contrato_Aditivo** | Armazenar aditivos contratuais | 1. Tipo_Aditivo texto livre (inconsistência). 2. Valor_Alteracao sem contexto (mensal/anual?). 3. Sem FK para documentos (PDFs perdidos). 4. Sem campos workflow (aprovador, data aprovação, justificativa). 5. Sem versionamento. 6. Sem auditoria (quem criou/editou). 7. Sem multi-tenancy (dados misturados). 8. Sem soft delete (DELETE físico perde dados). |

### Estrutura da Tabela Legada `Contrato_Aditivo`

```sql
CREATE TABLE Contrato_Aditivo (
    Id_Aditivo INT PRIMARY KEY IDENTITY(1,1),
    Id_Contrato INT NOT NULL,  -- FK para Contrato
    Tipo_Aditivo NVARCHAR(100), -- ❌ Texto livre
    Descricao NVARCHAR(500),
    Valor_Alteracao DECIMAL(18,2), -- ❌ Sem contexto
    Dt_Inicio DATE NOT NULL,
    Dt_Fim DATE, -- ❌ Pode ser NULL
    Fl_Ativo BIT DEFAULT 1 -- ❌ Sem soft delete
    -- ❌ SEM: workflow, versão, documentos, auditoria, multi-tenancy
)
```

### Problemas Críticos

1. **Tipo_Aditivo Texto Livre:** Valores encontrados no banco: "acrescimo", "Acresc.", "add linhas", "adicionar", "+", "Acresimo" (com erro ortográfico), "acréscimo" (com acento), "Acrescimos", "ADD", "Insert", "NEW". Total: 15+ variações para o mesmo conceito.

2. **Valor_Alteracao Ambíguo:** Não se sabe se é valor mensal, anual, total, incremental. Exemplos reais: R$ 5.000 (era mensal ou anual? incremento ou valor total?)

3. **Sem Documentos Vinculados:** Nenhuma FK para tabela documentos. PDFs salvos em `\\servidor\shared\contratos\aditivos\{Id_Aditivo}\` (pasta frequentemente reorganizada).

4. **Sem Workflow:** Campos de aprovação inexistentes. Email manual era enviado, mas sem registro no sistema.

5. **Sem Versionamento:** Cada UPDATE em `Contrato_Aditivo` sobrescrevia dados anteriores sem histórico.

---

## 5. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

Regras descobertas analisando código VB.NET e procedimentos armazenados:

- **RL-RN-001:** Se Tipo_Aditivo contém "supress" ou "cancel", calcula multa rescisória baseada em meses de fidelização restantes (código VB.NET hardcoded, não documentado)

- **RL-RN-002:** Se Tipo_Aditivo contém "prorrog" ou "extend", atualiza Dt_Fim do contrato base (sobrescreve sem criar versão)

- **RL-RN-003:** Se Valor_Alteracao > 20% do valor contrato base, cria entry no log application (mas não bloqueia a operação)

- **RL-RN-004:** Aditivos com Dt_Inicio no passado são permitidos (retroativos sem justificativa)

- **RL-RN-005:** Fl_Ativo = 0 era usado como "exclusão lógica" (mas queries não filtravam, retornavam inativos também)

- **RL-RN-006:** Upload de PDF era feito via FileUpload control, salvando em `\\servidor\shared\contratos\aditivos\{Id_Aditivo}\{GUID}.pdf` (sem OCR, sem hash, sem validação tipo arquivo)

- **RL-RN-007:** Se 2 aditivos tinham Dt_Inicio e Dt_Fim sobrepostos, o sistema não validava (permitia inconsistência)

---

## 6. GAP ANALYSIS (LEGADO × RF MODERNO)

| Item | Legado | RF Moderno (RF-027) | Observação |
|-----|--------|---------------------|------------|
| **Tipo de Aditivo** | Texto livre (15+ variações) | Enum 8 tipos estruturados | Consistência garantida |
| **Versionamento Contrato** | Sobrescrevia (histórico perdido) | Versionamento completo (Contrato_Versao) | Histórico preservado |
| **Workflow Aprovação** | Email manual (sem rastreamento) | Workflow BPM 3 níveis + SLA + DocuSign | Rastreável + compliance |
| **Impacto Financeiro** | Excel manual (6h cálculo) | Motor automático <5s (4 métricas + waterfall) | Eficiência 99% |
| **Documentos** | Rede compartilhada (PDFs perdidos) | Azure Blob + versionamento + OCR + hash SHA-256 | Nunca perdidos |
| **Alertas Vencimento** | Nenhum (descobria após vencer) | ML preditivo 90/60/30 dias + probabilidade renovação | Proativo |
| **Comparação Versões** | Track Changes Word (manual) | Diff engine visual (Myers' algorithm) | Automático + preciso |
| **Library Cláusulas** | Copiar/colar Word (formatação quebra) | 50+ templates + builder drag-and-drop | Reutilizável + consistente |
| **Dashboard** | Nenhum | Kanban pipeline + 5 gráficos executivos | Visibilidade gerencial |
| **Multi-tenancy** | Inexistente (dados misturados) | Row-Level Security com ClienteId | Segurança + isolamento |
| **Auditoria** | Inexistente | Log completo (quem, quando, antes/depois) | Compliance SOX/LGPD |
| **Soft Delete** | DELETE físico (dados perdidos) | FlExcluido = TRUE (preserva auditoria) | Rastreabilidade total |
| **API** | SOAP 3 métodos | REST 30+ endpoints (CQRS) | Moderno + escalável |
| **Validações** | Frontend only (bypass fácil) | Backend rigoroso (FluentValidation) | Segurança + integridade |

---

## 7. DECISÕES DE MODERNIZAÇÃO

### Decisão 1: Enum Estruturado vs. Texto Livre

- **Decisão:** Substituir campo texto livre `Tipo_Aditivo` por Enum com 8 tipos
- **Motivo:** Eliminar inconsistência (15+ variações no legado), facilitar relatórios, validações rigorosas
- **Impacto:** **ALTO** - Requer migração de dados legados (normalizar texto livre → enum)
- **Mitigação:** Script SQL de migração com mapeamento fuzzy (`LIKE '%supress%' → SUPRESSAO_LINHAS`)

### Decisão 2: Versionamento Completo de Contratos

- **Decisão:** Criar tabela `Contrato_Versao` com snapshot completo + diff visual
- **Motivo:** Legado sobrescrevia contrato (histórico perdido), auditorias exigem rastreabilidade total
- **Impacto:** **MÉDIO** - Aumento storage (~10MB por versão com JSON snapshot)
- **Mitigação:** Compressão JSON, Azure Blob Storage Cool Tier para versões antigas (>1 ano)

### Decisão 3: Workflow Multi-Nível com DocuSign

- **Decisão:** Substituir email manual por workflow BPM 3 níveis + assinatura digital
- **Motivo:** Compliance (SOX, LGPD), rastreabilidade jurídica, SLA automático, escalação
- **Impacto:** **ALTO** - Mudança processo de negócio (requer treinamento usuários)
- **Mitigação:** Fase piloto com 1 departamento, documentação completa, videos treinamento

### Decisão 4: Motor Cálculo Automático

- **Decisão:** Substituir Excel manual por motor automático (4 métricas + waterfall)
- **Motivo:** Eficiência (de 6h para <5s), elimina erros cálculo, gráficos automáticos
- **Impacto:** **MÉDIO** - Requer validação intensa (comparar resultados manual vs. automático)
- **Mitigação:** Testes com 100 aditivos reais, validação paralela 3 meses (manual + auto)

### Decisão 5: Azure Blob Storage vs. Rede Compartilhada

- **Decisão:** Migrar PDFs de `\\servidor\shared\` para Azure Blob Storage
- **Motivo:** PDFs perdidos frequentemente, sem versionamento, sem backup adequado
- **Impacto:** **BAIXO** - Custo storage ~R$50/mês, migração simples
- **Mitigação:** Script PowerShell migra PDFs preservando estrutura, mantém rede shared como backup temporário (6 meses)

### Decisão 6: ML Preditivo para Renovações

- **Decisão:** Implementar modelo ML.NET para prever renovação automática
- **Motivo:** 70% contratos renovam automaticamente sem renegociação (oportunidade perdida de economia)
- **Impacto:** **BAIXO** - Requer histórico mínimo 100 contratos (já temos 500+)
- **Mitigação:** Modelo simples (5 features), retreinamento mensal, fallback para alertas padrão se modelo falhar

---

## 8. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Probabilidade | Mitigação |
|------|---------|---------------|-----------|
| **Perda de Dados na Migração** | CRÍTICO | BAIXA | Backup completo DB legado, script migração testado em ambiente staging, validação row-by-row pós-migração |
| **Normalização Tipo_Aditivo Incorreta** | ALTO | MÉDIA | Script fuzzy matching com conferência manual, casos ambíguos marcados para revisão humana |
| **Resistência Workflow (email → BPM)** | MÉDIO | ALTA | Treinamento intensivo, fase piloto 1 departamento, champions identificados, documentação completa |
| **Cálculo Automático Difere do Manual** | ALTO | MÉDIA | Validação paralela 3 meses (manual + auto), ajustes fórmula baseados em feedback, auditoria aprovação CFO |
| **Indisponibilidade Azure Blob** | MÉDIO | BAIXA | Redundância geo-replicada (LRS → GRS), fallback para rede shared temporário (6 meses), monitoramento 24x7 |
| **ML Modelo Impreciso** | BAIXO | MÉDIA | Precisão mínima 70% validada antes de ativar, fallback para alertas padrão, retreinamento mensal automático |
| **Queries Legadas Quebradas** | MÉDIO | ALTA | Manter view compatibilidade `vw_Contrato_Aditivo_Legacy` (mapeia nova estrutura → antiga) por 12 meses |
| **DocuSign Callback Falha** | MÉDIO | BAIXA | Retry policy Polly (3 tentativas), DLQ Azure Service Bus, alerta Ops se >10 falhas/dia |

---

## 9. RASTREABILIDADE

### Telas Legado → RF Moderno

| Tela Legado | RF Moderno | Observação |
|-------------|------------|------------|
| Contrato\Aditivo.aspx | RF-027 (Wizard 5 etapas) | Evoluído - validações + workflow |
| Contrato\ListaAditivos.aspx | RF-027 (Dashboard pipeline Kanban) | Evoluído - filtros + KPIs + gráficos |
| (Inexistente) | RF-027 (Diff visual versões) | Funcionalidade nova |
| (Inexistente) | RF-027 (Library cláusulas) | Funcionalidade nova |
| (Inexistente) | RF-027 (ML alertas) | Funcionalidade nova |

### Webservices Legado → Endpoints REST

| Método SOAP Legado | Endpoint REST Moderno | Observação |
|--------------------|----------------------|------------|
| CriarAditivo() | POST /api/v1/aditivos | Evoluído - wizard + validações |
| ListarAditivos() | GET /api/v1/aditivos | Evoluído - paginação + filtros |
| AprovarAditivo() | POST /api/v1/aditivos/{id}/aprovar | Evoluído - workflow multi-nível |
| (Inexistente) | GET /api/v1/aditivos/{id}/impacto | Funcionalidade nova |
| (Inexistente) | GET /api/v1/contratos/{id}/versoes | Funcionalidade nova |
| (Inexistente) | POST /api/v1/aditivos/{id}/docusign | Funcionalidade nova |

### Tabelas Legado → Modelo Moderno

| Tabela Legado | Tabela(s) Moderna(s) | Observação |
|--------------|---------------------|------------|
| Contrato_Aditivo | Aditivo (evoluída com 50+ campos) | + Contrato_Versao, Aditivo_Aprovacao, Aditivo_Documento, Aditivo_Impacto_Financeiro, Clausula_Template, Aditivo_Alerta, Aditivo_Auditoria_Log |

### Regras Implícitas Legado → Regras Formais RF

| Regra Implícita Legado | Regra Formal RF | Observação |
|----------------------|-----------------|------------|
| RL-RN-001 (multa rescisória hardcoded) | RN-RF027-014 (cálculo automático multa) | Formalizada + auditável |
| RL-RN-002 (prorrogação sobrescreve) | RN-RF027-004 (versionamento) + RN-RF027-011 (validação datas) | Histórico preservado |
| RL-RN-003 (log se >20% variação) | RN-RF027-002 (wizard etapa 3 - justificativa obrigatória) | Formalizada + bloqueante |
| RL-RN-004 (retroativo permitido) | RN-RF027-011 (retroatividade exige justificativa + aprovação diretoria) | Controle rigoroso |
| RL-RN-005 (Fl_Ativo como soft delete) | RN-RF027-013 (FlExcluido + Query Filter global) | Implementação correta |
| RL-RN-006 (upload sem validação) | RN-RF027-007 (gestão documental completa - OCR + hash + tipos) | Segurança + integridade |
| RL-RN-007 (sobreposição permitida) | RN-RF027-011 (validação sobreposição - não permite 2 aditivos mesmo tipo) | Consistência garantida |

---

## 10. COMPATIBILIDADE E MIGRAÇÃO

### Script de Migração de Dados

```sql
-- Migração Contrato_Aditivo (legado) → Aditivo (moderno)
-- Executado em staging antes de produção

INSERT INTO Aditivo (
    Id_Contrato,
    Tipo, -- ← Enum normalizado
    Descricao,
    Valor_Incremental_Mensal, -- ← Assumido como mensal (validar manual)
    Dt_Inicio_Vigencia,
    Dt_Termino_Vigencia,
    Status, -- ← 'Vigente' se Fl_Ativo=1 E Dt_Fim >= GETDATE()
    FlExcluido, -- ← Mapeado de Fl_Ativo
    ClienteId, -- ← Inferido de Contrato.ClienteId (multi-tenancy)
    DataCriacao, -- ← GETDATE() (não existia no legado)
    UsuarioCriacao -- ← 'MIGRACAO_LEGADO' (não existia)
)
SELECT
    Id_Contrato,
    -- Normalização Tipo_Aditivo (fuzzy matching)
    CASE
        WHEN Tipo_Aditivo LIKE '%supress%' OR Tipo_Aditivo LIKE '%cancel%' THEN 'SUPRESSAO_LINHAS'
        WHEN Tipo_Aditivo LIKE '%acr%sc%' OR Tipo_Aditivo LIKE '%add%' OR Tipo_Aditivo LIKE '%+%' THEN 'ACRESCIMO_LINHAS'
        WHEN Tipo_Aditivo LIKE '%prorrog%' OR Tipo_Aditivo LIKE '%extend%' THEN 'PRORROGACAO_PRAZO'
        WHEN Tipo_Aditivo LIKE '%tarif%' OR Tipo_Aditivo LIKE '%pre%o%' THEN 'ALTERACAO_TARIFARIA'
        WHEN Tipo_Aditivo LIKE '%sla%' THEN 'MUDANCA_SLA'
        WHEN Tipo_Aditivo LIKE '%servi%' THEN 'INCLUSAO_SERVICOS'
        WHEN Tipo_Aditivo LIKE '%reajust%' OR Tipo_Aditivo LIKE '%ipca%' OR Tipo_Aditivo LIKE '%igp%' THEN 'REAJUSTE_INFLACIONARIO'
        WHEN Tipo_Aditivo LIKE '%garantia%' THEN 'TROCA_GARANTIAS'
        ELSE 'OUTROS' -- ← Casos ambíguos marcados para revisão manual
    END AS Tipo,
    Descricao,
    Valor_Alteracao, -- ← ASSUMIDO como mensal (requer validação manual posterior)
    Dt_Inicio,
    Dt_Fim,
    -- Status inferido
    CASE
        WHEN Fl_Ativo = 1 AND Dt_Fim >= GETDATE() THEN 'Vigente'
        WHEN Fl_Ativo = 1 AND Dt_Fim < GETDATE() THEN 'Encerrado'
        ELSE 'Cancelado'
    END AS Status,
    CASE WHEN Fl_Ativo = 0 THEN 1 ELSE 0 END AS FlExcluido,
    C.ClienteId, -- ← Multi-tenancy
    GETDATE() AS DataCriacao,
    'MIGRACAO_LEGADO' AS UsuarioCriacao
FROM Contrato_Aditivo CA
INNER JOIN Contrato C ON CA.Id_Contrato = C.Id_Contrato
WHERE CA.Id_Aditivo NOT IN (SELECT Id_Aditivo_Legado FROM Aditivo WHERE Id_Aditivo_Legado IS NOT NULL)
-- Evita duplicatas se script for reexecutado
```

### View de Compatibilidade (Manter 12 Meses)

```sql
-- View para queries legadas continuarem funcionando
CREATE VIEW vw_Contrato_Aditivo_Legacy AS
SELECT
    Id AS Id_Aditivo,
    Id_Contrato,
    -- Tipo Enum → texto (reverso da migração)
    CASE Tipo
        WHEN 'SUPRESSAO_LINHAS' THEN 'Supressão'
        WHEN 'ACRESCIMO_LINHAS' THEN 'Acréscimo'
        WHEN 'PRORROGACAO_PRAZO' THEN 'Prorrogação'
        WHEN 'ALTERACAO_TARIFARIA' THEN 'Alteração Tarifária'
        WHEN 'MUDANCA_SLA' THEN 'Mudança SLA'
        WHEN 'INCLUSAO_SERVICOS' THEN 'Inclusão Serviços'
        WHEN 'REAJUSTE_INFLACIONARIO' THEN 'Reajuste'
        WHEN 'TROCA_GARANTIAS' THEN 'Troca Garantias'
        ELSE 'Outros'
    END AS Tipo_Aditivo,
    Descricao,
    Valor_Incremental_Mensal AS Valor_Alteracao,
    Dt_Inicio_Vigencia AS Dt_Inicio,
    Dt_Termino_Vigencia AS Dt_Fim,
    CASE WHEN FlExcluido = 0 AND Status = 'Vigente' THEN 1 ELSE 0 END AS Fl_Ativo
FROM Aditivo
WHERE FlExcluido = 0 -- Não retornar excluídos logicamente
```

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|------|------|----------|------|
| 1.0 | 2025-12-30 | Documentação completa do legado RF-027. Análise de telas ASP.NET, webservices SOAP, tabela Contrato_Aditivo. Identificação de 7 regras implícitas. Gap analysis com 15 itens. 6 decisões de modernização. 8 riscos de migração. Script migração + view compatibilidade. | Agência ALC - alc.dev.br |
