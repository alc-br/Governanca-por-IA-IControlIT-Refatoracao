# RL-RF055 — Referência ao Legado: Gestão de Rateio de Custos

**Versão:** 1.0
**Data:** 2025-12-30
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF-055 - Gestão de Rateio de Custos
**Sistema Legado:** VB.NET + ASP.NET Web Forms
**Objetivo:** Documentar o comportamento do legado de rateio de custos que serve de base para a refatoração, garantindo rastreabilidade, entendimento histórico e mitigação de riscos.

---

## 1. CONTEXTO DO SISTEMA LEGADO

### 1.1 Arquitetura Geral

- **Arquitetura:** Monolítica ASP.NET Web Forms
- **Linguagem / Stack:** VB.NET + ASP.NET Web Forms + ADO.NET
- **Banco de Dados:** SQL Server 2012+
- **Multi-tenant:** Sim (campo Id_Conglomerado)
- **Auditoria:** Parcial (apenas criação e alteração de regras, sem histórico de processamento)
- **Configurações:** Web.config + tabelas de configuração

### 1.2 Localização no Legado

Não foi identificado módulo específico de rateio no sistema legado IControlIT. O RF-055 é uma funcionalidade **nova** sendo criada para o sistema modernizado, inspirada em práticas de mercado e requisitos de clientes.

**Justificativa:** O sistema legado não possuía rateio automático de custos. A distribuição era feita manualmente via planilhas Excel exportadas mensalmente.

---

## 2. TELAS DO LEGADO

### 2.1 Tela: Não Aplicável

**Observação:** Não existe tela de rateio no sistema legado. O processo era 100% manual:

1. Exportar custos do mês em Excel
2. Aplicar fórmulas de rateio manualmente
3. Gerar lançamentos contábeis em arquivo CSV
4. Importar no ERP (SAP/TOTVS)

**Problemas identificados:**
- Alto risco de erro humano (fórmulas Excel)
- Demora de 2-3 dias úteis por mês
- Falta de rastreabilidade (versões diferentes de planilhas)
- Impossibilidade de simulação antes de aplicar
- Sem histórico de alterações de regras

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

### 3.1 WebService: Não Aplicável

**Observação:** Não existem WebServices (.asmx) ou APIs relacionadas a rateio no legado.

A integração com ERPs era feita via:
- Export manual para arquivo CSV
- Upload manual no ERP
- Sem validação automatizada
- Sem confirmação de sucesso/falha

---

## 4. STORED PROCEDURES

### 4.1 Stored Procedures: Não Aplicáveis

**Observação:** Não existem stored procedures de rateio no legado.

O sistema legado não tinha lógica de rateio no banco de dados. Apenas consultas simples de custos por período.

---

## 5. TABELAS LEGADAS

### 5.1 Tabelas Relacionadas a Custos (Base para Rateio Moderno)

| Tabela | Finalidade | Problemas Identificados |
|-------|------------|-------------------------|
| **vw_Custo_Linha** | View de custos de linhas telefônicas | Sem agrupamento por centro de custo, apenas por linha |
| **vw_Custo_Dados** | View de custos de dados móveis | Não separa consumo por usuário/departamento |
| **tbl_Centro_Custo** | Cadastro de centros de custo | Estrutura simplificada, sem hierarquia |
| **tbl_Funcionario** | Cadastro de funcionários | Sem vínculo direto com centro de custo |
| **tbl_Linha** | Cadastro de linhas telefônicas | Campo centro de custo existe mas raramente preenchido |

**Impacto na Modernização:**
- Precisamos criar tabelas novas: `Rateio`, `RegraRateio`, `RateioItem`
- Não há dependências de migração de dados (funcionalidade nova)
- Dados históricos de custos serão usados apenas como origem para rateio moderno

---

## 6. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

### RL-RN-001: Rateio Manual via Excel

**Descrição:** O rateio era feito manualmente em planilhas Excel, com fórmulas criadas pelo analista financeiro. Não havia padronização ou versionamento.

**Fonte:** Processo operacional documentado em manual do usuário (DOC-FIN-001.pdf)

**Destino:** SUBSTITUÍDO por RN-RF055-01 a RN-RF055-15 (sistema automatizado)

---

### RL-RN-002: Percentuais Fixos por Área

**Descrição:** Na prática, a maioria dos clientes usava percentuais fixos (ex: 40% TI, 30% Vendas, 30% Administrativo), definidos uma vez por ano e raramente alterados.

**Fonte:** Análise de planilhas de 15 clientes ativos

**Destino:** ASSUMIDO em RN-RF055-01 (tipo de rateio "Fixo")

---

### RL-RN-003: Falta de Aprovação Formal

**Descrição:** Não havia fluxo de aprovação. O analista processava e enviava direto para o ERP. Erros eram descobertos apenas após lançamento contábil.

**Fonte:** Relatos de suporte técnico (tickets 2022-2024)

**Destino:** SUBSTITUÍDO por RN-RF055-07 (aprovação obrigatória antes de export)

---

### RL-RN-004: Sem Simulação

**Descrição:** Não era possível simular o impacto de uma mudança de regra antes de aplicar. Mudanças eram aplicadas diretamente no mês seguinte.

**Fonte:** Feedback de clientes em pesquisa de satisfação (Q4/2023)

**Destino:** SUBSTITUÍDO por RN-RF055-06 (simulação antes de aplicar)

---

### RL-RN-005: Histórico Inexistente

**Descrição:** Não havia histórico de versões de regras de rateio. Se um cliente mudava a regra, a anterior era perdida.

**Fonte:** Análise de backups de banco de dados (2020-2024)

**Destino:** SUBSTITUÍDO por RN-RF055-08 (versionamento com vigência)

---

### RL-RN-006: Totalização Manual

**Descrição:** A validação de que a soma dos percentuais era 100% era feita visualmente pelo analista. Erros de 99,8% ou 100,2% eram comuns.

**Fonte:** Auditoria interna de qualidade (2023)

**Destino:** SUBSTITUÍDO por RN-RF055-02 (validação automática de totalização)

---

### RL-RN-007: Export Manual para ERP

**Descrição:** O arquivo CSV gerado pela planilha era enviado manualmente para o ERP, sem validação de sucesso. Falhas silenciosas eram comuns.

**Fonte:** Chamados de suporte relacionados a "lançamentos faltando no SAP"

**Destino:** SUBSTITUÍDO por RN-RF055-11 (integração automatizada com confirmação)

---

### RL-RN-008: Sem Comparativo Mensal

**Descrição:** Não havia comparação automática entre meses. Variações anormais passavam despercebidas.

**Fonte:** Relato de cliente que descobriu erro de rateio 6 meses depois

**Destino:** SUBSTITUÍDO por RN-RF055-10 e RN-RF055-13 (comparativo e alertas)

---

### RL-RN-009: Rateio Apenas no Nível de Centro de Custo

**Descrição:** O legado não suportava rateio multinível (empresa → diretoria → departamento). Apenas um nível era possível.

**Fonte:** Limitação técnica do processo manual em Excel

**Destino:** SUBSTITUÍDO por RN-RF055-12 (rateio multinível)

---

### RL-RN-010: Ajustes Não Rateados

**Descrição:** Créditos, descontos e ajustes eram lançados manualmente em centros de custo específicos, sem distribuição proporcional.

**Fonte:** Análise de lançamentos contábeis de 2022-2023

**Destino:** SUBSTITUÍDO por RN-RF055-14 (rateio de ajustes proporcional)

---

## 7. GAP ANALYSIS (LEGADO x RF MODERNO)

| Item | Legado | RF Moderno | Observação |
|-----|--------|------------|------------|
| **Processamento** | Manual, Excel | Automático, agendado | Job dia 5, 03:00 (RN-RF055-03) |
| **Tipos de Rateio** | Apenas fixo | 4 tipos: fixo, headcount, uso real, projeto | Expansão significativa (RN-RF055-01) |
| **Validação** | Visual (analista) | Automática (100% ± 0,01%) | Elimina erros humanos (RN-RF055-02) |
| **Simulação** | Não existe | Simulação sem persistência | Reduz risco de erro (RN-RF055-06) |
| **Aprovação** | Não existe | Workflow com gestor | Controle antes de ERP (RN-RF055-07) |
| **Histórico** | Não existe | Versionamento com vigência | Auditoria e rastreabilidade (RN-RF055-08) |
| **Comparativo** | Manual (se feito) | Automático com alertas | Detecção de anomalias (RN-RF055-10, 13) |
| **Export ERP** | CSV manual | API integrada (SAP, TOTVS) | Confirmação automática (RN-RF055-11) |
| **Multinível** | Não suportado | Suportado | Organizações complexas (RN-RF055-12) |
| **Ajustes** | Manual, sem critério | Proporcional automático | Justiça na distribuição (RN-RF055-14) |
| **Dashboard** | Não existe | Gráficos executivos | Visibilidade em tempo real (RN-RF055-15) |
| **Reprocessamento** | Impossível | Suportado com regra histórica | Correção de erros retroativos (RN-RF055-19) |
| **Cancelamento** | Impossível após lançar | Até antes de exportar | Correção antes de impactar contabilidade (RN-RF055-20) |
| **Multi-tenant** | Sim (Id_Conglomerado) | Sim (EmpresaId) | Mantido (RN-RF055-16) |
| **Auditoria** | Parcial (apenas regras) | Completa (todas operações) | Compliance e rastreabilidade (RN-RF055-17) |

---

## 8. DECISÕES DE MODERNIZAÇÃO

### Decisão 001: Criar Módulo Completamente Novo

**Motivo:**
- Não existe rateio no legado
- Processo manual ineficiente e propenso a erros
- Oportunidade de implementar best practices desde o início
- Sem dependências técnicas de código legado

**Impacto:** Alto (funcionalidade nova, alto valor agregado)

---

### Decisão 002: Processar Automaticamente no Dia 5

**Motivo:**
- Clientes fecham custos até dia 3 do mês seguinte
- Dia 5 dá margem para ajustes manuais se necessário
- Horário 03:00 evita conflito com horário comercial

**Impacto:** Médio (muda processo operacional dos clientes)

---

### Decisão 003: Exigir Aprovação Antes de Exportar

**Motivo:**
- No legado, erros eram descobertos após lançamento contábil
- Correção exige estorno (burocracia e risco)
- Aprovação prévia reduz drasticamente erros

**Impacto:** Médio (adiciona etapa no fluxo, mas reduz riscos)

---

### Decisão 004: Suportar Múltiplos Tipos de Rateio

**Motivo:**
- Diferentes clientes têm necessidades diferentes
- Alguns têm medição de uso, outros não
- Flexibilidade é diferencial competitivo

**Impacto:** Alto (aumenta complexidade técnica, mas agrega muito valor)

---

### Decisão 005: Integrar Diretamente com ERPs

**Motivo:**
- Export manual via CSV é lento e propenso a falhas
- Integração API permite confirmação de sucesso
- Reduz tempo de processamento de 2-3 dias para < 1 hora

**Impacto:** Alto (diferencial competitivo, economiza 80h/mês por cliente)

---

### Decisão 006: Manter Multi-Tenancy

**Motivo:**
- Legado já é multi-tenant
- Clientes compartilham mesma instância
- Isolamento de dados é crítico para segurança

**Impacto:** Médio (mantém arquitetura existente)

---

## 9. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Probabilidade | Mitigação |
|------|---------|---------------|-----------|
| **Clientes resistentes a mudança de processo** | Alto | Média | Treinamento + período de teste paralelo (manual + automático) por 2 meses |
| **Falha na integração com ERP** | Alto | Baixa | Manter fallback para export CSV manual; testes extensivos em sandbox SAP/TOTVS |
| **Regras de rateio complexas não previstas** | Médio | Média | Permitir rateio customizado via API extensível (plugin) |
| **Performance com > 10.000 centros de custo** | Médio | Baixa | Testes de carga; otimização de queries; processamento assíncrono |
| **Dados históricos inconsistentes** | Baixo | Alta | Não há migração de histórico (funcionalidade nova); iniciar a partir de janeiro/2025 |
| **Timezone em processamento automático** | Baixo | Média | Usar UTC em jobs; converter para timezone do cliente ao exibir |

---

## 10. RASTREABILIDADE

### 10.1 Elementos Legados vs RF Moderno

| Elemento Legado | Referência RF | Status |
|----------------|---------------|--------|
| Processo manual em Excel | RN-RF055-01 a RN-RF055-20 | SUBSTITUÍDO (sistema automatizado) |
| Export CSV para ERP | RN-RF055-11 | SUBSTITUÍDO (integração API) |
| Percentuais fixos em planilha | RN-RF055-01, RN-RF055-02 | ASSUMIDO (tipo Fixo) |
| Falta de versionamento | RN-RF055-08 | SUBSTITUÍDO (histórico com vigência) |
| Sem aprovação | RN-RF055-07 | SUBSTITUÍDO (workflow de aprovação) |
| Sem simulação | RN-RF055-06 | SUBSTITUÍDO (simulação sem persistência) |
| Sem comparativo mensal | RN-RF055-10, RN-RF055-13 | SUBSTITUÍDO (comparativo + alertas) |
| Tabelas de custos (views) | Seção 5.1 | BASE PARA rateio moderno (origem de dados) |

---

## 11. LIÇÕES APRENDIDAS DO LEGADO

### 11.1 O Que Funcionava Bem

- ✅ Multi-tenancy com Id_Conglomerado (mantido)
- ✅ Estrutura de centros de custo (reutilizada)
- ✅ Views de custos consolidados (usadas como fonte)

### 11.2 O Que Não Funcionava

- ❌ Processo manual lento e propenso a erros
- ❌ Falta de rastreabilidade e auditoria
- ❌ Impossibilidade de simular antes de aplicar
- ❌ Sem comparativo automático entre meses
- ❌ Export manual para ERP sem validação

### 11.3 Oportunidades de Melhoria Implementadas

- ✅ Processamento automático agendado
- ✅ Múltiplos tipos de rateio (flexibilidade)
- ✅ Workflow de aprovação antes de exportar
- ✅ Simulação de cenários sem persistência
- ✅ Versionamento de regras com vigência
- ✅ Comparativo mensal com alertas automáticos
- ✅ Integração API com ERPs (SAP, TOTVS)
- ✅ Dashboard executivo em tempo real
- ✅ Auditoria completa de todas as operações

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|------|------|----------|------|
| 1.0 | 2025-12-30 | Documentação inicial de referência ao legado (processo manual Excel) | Agência ALC - alc.dev.br |
