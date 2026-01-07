# RL-RF039 — Referência ao Legado: Gestão de Bilhetes

**Versão:** 1.0
**Data:** 2025-12-30
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF-039 - Gestão de Bilhetes Telefônicos
**Sistema Legado:** IC1_Sistema_Producao (ASP.NET Web Forms + VB.NET + SQL Server)
**Objetivo:** Documentar a ausência de módulo legado específico de gestão de bilhetes e o processo manual que era utilizado, garantindo rastreabilidade do que existia vs o que será implementado.

---

## 1. CONTEXTO DO LEGADO

### Stack Tecnológica Geral

- **Arquitetura:** Monolítica com WebServices ASMX
- **Linguagem:** VB.NET (Code-behind ASPX)
- **Framework:** ASP.NET Web Forms (.NET Framework 4.5)
- **Banco de Dados:** SQL Server 2012 (banco `IC1_Sistema_Producao`)
- **Frontend:** ASPX Server-Side Rendering (ViewState, PostBack)
- **Webservices:** ASMX (XML/SOAP)
- **Relatórios:** Crystal Reports hospedado em servidor dedicado

### Características do Sistema Legado (Geral)

- **Multi-tenant:** ❌ Não existia. Todos os dados visíveis a todos os usuários.
- **Auditoria:** ⚠️ Parcial. Logs textuais em arquivo `text.log` sem estrutura.
- **Soft Delete:** ❌ Inexistente. Hard delete físico no banco.
- **Validações:** ⚠️ Mínimas. Apenas validações básicas de campos obrigatórios.
- **Segurança:** ⚠️ Básica. Sem isolamento por tenant, sem RBAC robusto.

### Gestão de Bilhetes no Legado

**⚠️ IMPORTANTE:** O sistema legado IControlIT **NÃO possuía módulo dedicado de gestão de bilhetes telefônicos**.

O controle era feito através de:
- **Importação manual de arquivos CSV** em planilhas Excel separadas (fora do sistema)
- **Relatórios pivot manuais** criados pelos usuários em Excel
- **Envio de resumos mensais** por e-mail para gestores (cópia/cola de planilhas)
- **Sem integração com ERP** - lançamentos contábeis manuais
- **Sem alertas automáticos** - verificação visual esporádica de gastos elevados
- **Sem detecção de anomalias** - identificação manual de problemas
- **Sem rateio automático** - cálculos em Excel com fórmulas manuais

### Problemas Identificados

1. **Ausência de Automação:** Processo 100% manual, suscetível a erros humanos
2. **Falta de Rastreabilidade:** Planilhas em pastas locais, sem versionamento ou auditoria
3. **Sem Alertas em Tempo Real:** Problemas (roaming, números premium) detectados apenas na fatura fechada
4. **Rateio Manual Demorado:** Fechamento mensal levava 3-5 dias de trabalho
5. **Sem Validação de Números:** Números mal formatados, dificultando análises
6. **Sem OCR:** Faturas em PDF escaneado exigiam digitação manual
7. **Sem Machine Learning:** Anomalias não detectadas proativamente
8. **Integração ERP Manual:** Exportação de dados para importação manual no ERP

---

## 2. TELAS DO LEGADO

### ❌ NÃO APLICÁVEL

O sistema legado **não possuía telas ASPX** dedicadas à gestão de bilhetes telefônicos.

Todo o processo era realizado fora do sistema, em planilhas Excel.

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

### ❌ NÃO APLICÁVEL

O sistema legado **não possuía webservices (.asmx)** para gestão de bilhetes.

Não havia APIs ou serviços automatizados relacionados a telefonia.

---

## 4. TABELAS LEGADAS

### ❌ NÃO APLICÁVEL

O sistema legado **não possuía tabelas no SQL Server** para armazenar bilhetes telefônicos.

Dados de telefonia eram mantidos em:
- Planilhas Excel (.xlsx) em pastas compartilhadas (`\\server\telefonia\`)
- Arquivos CSV baixados manualmente dos portais das operadoras
- Nenhum dado estruturado no banco de dados

---

## 5. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

Apesar de não haver sistema automatizado, o processo manual seguia algumas regras implícitas:

### Processo Manual de Gestão de Bilhetes (Planilhas Excel)

1. **Download Manual de Faturas**
   - Responsável: Analista de TI
   - Frequência: Mensal (após recebimento de e-mail da operadora)
   - Ação: Acessar portal da operadora → Baixar arquivo CSV → Salvar em `\\server\telefonia\{ano}\{mes}\`

2. **Importação em Excel**
   - Responsável: Analista de TI
   - Ferramenta: Excel com macros VBA personalizadas
   - Ação: Abrir arquivo CSV → Aplicar filtros e formatação → Salvar como XLSX

3. **Análise Manual de Custos**
   - Responsável: Analista de TI + Gestor Financeiro
   - Ferramenta: Tabela dinâmica (pivot) do Excel
   - Métricas calculadas:
     - Total de custos por ramal
     - Total de minutos por ramal
     - Custo médio por minuto
     - Comparação mês a mês (fórmula `=(B2-A2)/A2`)

4. **Identificação Manual de Anomalias**
   - Responsável: Analista de TI
   - Método: Ordenação decrescente por custo, verificação visual de outliers
   - Critérios subjetivos:
     - Custo >R$ 500 por ramal → Investigar
     - Ligações para números 0900/0300 → Destacar em vermelho
     - Ligações internacionais não justificadas → Consultar gestor

5. **Rateio Manual por Centro de Custo**
   - Responsável: Analista Financeiro
   - Ferramenta: Excel com VLOOKUP para vincular ramal → centro de custo
   - Tempo médio: 3-5 dias (dependendo da quantidade de ramais)
   - Problemas:
     - Ramais sem centro de custo vinculado → Rateio proporcional genérico
     - Erros de digitação em fórmulas → Rateio incorreto
     - Sem validação de soma 100% → Divergências contábeis frequentes

6. **Integração Manual com ERP**
   - Responsável: Analista Financeiro
   - Método: Exportar resumo do Excel → Importar manualmente no ERP (SAP)
   - Tempo médio: 2 horas
   - Problemas:
     - Erro de importação → Retrabalho
     - Lançamentos duplicados → Ajustes manuais
     - Sem rastreabilidade (qual lançamento veio de qual bilhete)

7. **Relatórios Mensais para Gestores**
   - Responsável: Analista de TI
   - Ferramenta: Gráficos do Excel copiados para PowerPoint
   - Entrega: E-mail com anexo PPT
   - Conteúdo:
     - Total de custos do mês
     - Comparação com mês anterior
     - Top 5 ramais com maior custo (sem drill-down, apenas valores totais)

### Regras Implícitas Extraídas do Processo Manual

- **RL-RN-001:** Fatura só era processada após e-mail da operadora (sem FTP automático)
- **RL-RN-002:** Apenas faturas em CSV eram processadas (PDFs escaneados ignorados)
- **RL-RN-003:** Rateio era feito apenas 1x por mês (fechamento mensal, sem rateio incremental)
- **RL-RN-004:** Anomalias eram identificadas por verificação visual (sem score de risco quantitativo)
- **RL-RN-005:** Alertas de roaming eram enviados manualmente após fechamento da fatura (não em tempo real)
- **RL-RN-006:** Números não eram normalizados (formatos variados: "(11) 9876-5432", "11 98765432", etc.)
- **RL-RN-007:** Sem histórico de alterações (versões da planilha substituíam anteriores)

---

## 6. GAP ANALYSIS (LEGADO x RF MODERNO)

| Funcionalidade | Legado | RF Moderno | Observação |
|---------------|--------|------------|------------|
| **Importação de Faturas** | Manual, download via portal operadora | Automática via FTP/API, job agendado | Redução de 5h de trabalho/mês |
| **Formatos Suportados** | Apenas CSV (TIM) | CSV, XLS, PDF (todas operadoras) | Suporte multi-operadora |
| **Parser de Formato** | N/A (Excel abria direto) | Inteligente, detecta operadora automaticamente | Elimina configuração manual |
| **Normalização de Números** | ❌ Não existia | ✅ Formato E.164 padrão | Consistência de dados |
| **OCR de PDFs** | ❌ PDFs ignorados | ✅ Azure Cognitive Services/Tesseract | Permite processar qualquer fatura |
| **Análise de Custos** | Manual em Excel pivot | Dashboard interativo em tempo real | Visibilidade imediata |
| **Detecção de Anomalias** | Visual, subjetiva | Machine learning com score de risco | Detecção proativa |
| **Alertas Números Premium** | Manual após fechamento | Automático em tempo real (SignalR + e-mail) | Prevenção de custos indevidos |
| **Alertas Roaming** | ❌ Não existia | ✅ SMS imediato + e-mail gestor | Controle proativo |
| **Rateio de Custos** | Planilha Excel (3-5 dias) | Automático via FK centro de custo | Redução de 98% do tempo |
| **Validação Rateio 100%** | ❌ Não validava | ✅ Validação matemática obrigatória | Elimina divergências |
| **Comparação Uso vs Plano** | ❌ Não existia | ✅ Classificação sub-uso/adequado/excesso | Otimização de planos |
| **Simulador de Planos** | ❌ Não existia | ✅ Comparação com mercado | Economia identificada |
| **Top 10 Consumidores** | Manual, apenas valores | Automático com drill-down completo | Análise detalhada |
| **Evolução de Custos** | Gráfico estático Excel | Dashboard dinâmico com tendência | Projeções futuras |
| **Horário de Pico** | ❌ Não existia | ✅ Heatmap para dimensionamento troncos | Otimização de infraestrutura |
| **Integração ERP** | Manual (2h) | Automática via API REST | Eliminação de retrabalho |
| **Política de Uso** | ❌ Não existia | ✅ Score de conformidade automático | Governança de uso |
| **Multi-tenancy** | ❌ Dados misturados | ✅ Isolamento por ClienteId | Segurança e privacidade |
| **Auditoria** | ❌ Não existia | ✅ Log completo 7 anos | Conformidade LGPD |

---

## 7. DECISÕES DE MODERNIZAÇÃO

### Decisão 1: Importação Automatizada vs Manual

**Escolhido:** Importação Automatizada via FTP/API com job Hangfire diário

**Motivo:**
- Eliminar trabalho manual repetitivo (5h/mês)
- Garantir pontualidade (dados disponíveis no mesmo dia do fechamento)
- Reduzir erros humanos (esquecimento de download, arquivo errado)

**Impacto:** Alto - Core do sistema, essencial para todo o fluxo

---

### Decisão 2: Machine Learning vs Regras Estáticas para Anomalias

**Escolhido:** Machine Learning com score de risco (0-100)

**Motivo:**
- Detecção mais precisa (baseline de 90 dias, padrão individual)
- Adaptação automática (aprende comportamento normal de cada número)
- Redução de falsos positivos (thresholds personalizados)

**Impacto:** Alto - Diferencial competitivo, previne fraudes

---

### Decisão 3: OCR vs Apenas CSV/XLS

**Escolhido:** Suporte a OCR (Azure Cognitive Services)

**Motivo:**
- Algumas operadoras menores ainda enviam PDF escaneado
- Elimina barreira de entrada (qualquer fatura pode ser processada)
- Flexibilidade para clientes com múltiplas operadoras

**Impacto:** Médio - Aumenta compatibilidade, mas OCR tem custo e precisão variável

---

### Decisão 4: Rateio Automático vs Configurável

**Escolhido:** Rateio Automático com FK para centro de custo

**Motivo:**
- Elimina 100% do trabalho manual (3-5 dias → automático)
- Garante soma 100% (validação matemática)
- Rastreabilidade completa (cada bilhete → centro de custo → conta contábil)

**Impacto:** Alto - Economia de tempo significativa, elimina erros

---

### Decisão 5: Alertas em Tempo Real vs Batch Mensal

**Escolhido:** Alertas em Tempo Real (SignalR + e-mail + SMS)

**Motivo:**
- Prevenção proativa (roaming detectado no 1º bilhete, não após R$ 2.000)
- Controle de danos (bloqueio automático evita custos excessivos)
- Compliance (justificativa de números premium em 48h)

**Impacto:** Alto - Redução significativa de custos indevidos

---

## 8. RISCOS DE MIGRAÇÃO

| Risco | Probabilidade | Impacto | Mitigação |
|------|---------------|---------|-----------|
| **Falta de dados históricos** | Alta | Médio | Parser aceita arquivos retroativos (até 24 meses) |
| **Formato de fatura desconhecido** | Média | Médio | Parser genérico + interface de configuração manual |
| **Resistência ao processo automatizado** | Baixa | Baixo | Treinamento + dashboard com benefícios visíveis |
| **Custos de OCR (Azure)** | Média | Baixo | Tesseract como alternativa gratuita (menor precisão) |
| **Complexidade Machine Learning** | Alta | Médio | Baseline de 30 dias (não 90) se histórico insuficiente |
| **Erros de vinculação centro de custo** | Alta | Alto | Validação obrigatória antes da importação, bloqueio se FK ausente |
| **Custo de integração ERP** | Média | Médio | API REST padrão (SAP, TOTVS, Protheus) - mapeamento configurável |

---

## 9. RASTREABILIDADE

| Elemento Legado | Referência RF Moderno | Destino |
|----------------|----------------------|---------|
| **Processo Manual de Download de Faturas** | RF-039 - Seção 4.1 (Importação Automatizada) | SUBSTITUÍDO |
| **Planilhas Excel com Macros VBA** | RF-039 - Seção 4.3 (Parser Inteligente) | SUBSTITUÍDO |
| **Análise Manual de Custos** | RF-039 - Seção 4.6 (Dashboard de Custos) | SUBSTITUÍDO |
| **Rateio Manual em Excel** | RF-039 - Seção 4.10 (Rateio Automático) | SUBSTITUÍDO |
| **Integração Manual com ERP** | RF-039 - Seção 4.17 (Exportação Automática ERP) | SUBSTITUÍDO |
| **Relatórios Mensais por E-mail** | RF-039 - Seção 4.13-14 (Relatórios Gerenciais) | SUBSTITUÍDO |
| **Identificação Visual de Anomalias** | RF-039 - Seção 4.7 (Machine Learning) | SUBSTITUÍDO |
| **Sem Alertas em Tempo Real** | RF-039 - Seção 4.8-9 (Alertas Premium/Roaming) | NOVO (não existia) |
| **Sem Normalização de Números** | RF-039 - Seção 4.5 (Normalização E.164) | NOVO (não existia) |
| **Sem OCR** | RF-039 - Seção 4.4 (OCR de PDFs) | NOVO (não existia) |
| **Sem Simulador de Planos** | RF-039 - Seção 4.12 (Simulador) | NOVO (não existia) |
| **Sem Análise de Pico** | RF-039 - Seção 4.15 (Horário de Pico) | NOVO (não existia) |
| **Sem Política de Uso** | RF-039 - Seção 4.16 (Compliance) | NOVO (não existia) |

---

## 10. FUNCIONALIDADES NOVAS (NÃO EXISTIAM NO LEGADO)

As seguintes funcionalidades são **100% novas** no sistema modernizado:

1. ✅ **Importação Automatizada via FTP/API** - Era manual
2. ✅ **Parser Inteligente Multi-Formato** - Excel abria direto, sem detecção
3. ✅ **Normalização de Números E.164** - Não existia
4. ✅ **OCR de PDFs Escaneados** - PDFs eram ignorados
5. ✅ **Machine Learning para Anomalias** - Detecção manual e subjetiva
6. ✅ **Alertas em Tempo Real (SignalR)** - Não existia
7. ✅ **SMS para Roaming Internacional** - Não existia
8. ✅ **Rateio Automático 100%** - Era manual em Excel
9. ✅ **Comparação Uso vs Plano** - Não existia
10. ✅ **Simulador de Planos Alternativos** - Não existia
11. ✅ **Dashboard de Evolução com Tendências** - Gráficos estáticos
12. ✅ **Análise de Horário de Pico** - Não existia
13. ✅ **Política de Uso Aceitável com Score** - Não existia
14. ✅ **Multi-tenancy** - Dados misturados
15. ✅ **Auditoria 7 anos** - Não existia

---

## 11. RESUMO EXECUTIVO

### Situação Legado

- ❌ **NÃO HAVIA SISTEMA** dedicado a gestão de bilhetes
- ⚠️ **Processo 100% manual** em planilhas Excel
- ⚠️ **Tempo de fechamento:** 3-5 dias/mês
- ⚠️ **Erros frequentes** em rateio (soma ≠ 100%)
- ❌ **Sem alertas em tempo real**
- ❌ **Sem detecção de anomalias**
- ❌ **Sem rastreabilidade**

### Situação Modernizada

- ✅ **Sistema completo** com 17 funcionalidades
- ✅ **Automação 95%** do processo
- ✅ **Tempo de fechamento:** automático (0h)
- ✅ **Rateio validado** matematicamente (100%)
- ✅ **Alertas em tempo real** (latência <30s)
- ✅ **Machine Learning** detecta anomalias
- ✅ **Auditoria completa** 7 anos (LGPD)

### Ganhos Quantificáveis

| Métrica | Legado | Moderno | Ganho |
|---------|--------|---------|-------|
| **Tempo de Fechamento Mensal** | 40h (3-5 dias) | 0h (automático) | 100% redução |
| **Erros de Rateio** | 15-20% das vezes | 0% (validação matemática) | 100% eliminação |
| **Detecção de Anomalias** | Retroativa (após fatura) | Proativa (tempo real) | Economia média R$ 5.000/mês |
| **Formatos Suportados** | 1 (CSV TIM) | 4 (TIM, Vivo, Claro, Oi) + PDF | 400% aumento |
| **Visibilidade de Dados** | Mensal (estática) | Tempo real (dashboard) | Imediata |
| **Rastreabilidade** | ❌ Não existia | ✅ 100% auditado | Compliance |

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|--------|------|-----------|-------|
| 1.0 | 2025-12-30 | Criação da referência ao legado (ausência de sistema dedicado) | Agência ALC - alc.dev.br |
