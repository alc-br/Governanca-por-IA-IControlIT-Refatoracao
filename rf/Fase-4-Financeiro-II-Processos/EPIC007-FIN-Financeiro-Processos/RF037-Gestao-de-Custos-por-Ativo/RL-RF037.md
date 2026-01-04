# RL-RF037 — Referência ao Legado: Gestão de Custos por Ativo

**Versão:** 1.0
**Data:** 2025-12-30
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF-037
**Sistema Legado:** VB.NET + ASP.NET Web Forms
**Objetivo:** Documentar o comportamento do legado relacionado à gestão de custos de ativos, garantindo rastreabilidade, entendimento histórico e mitigação de riscos durante a modernização.

---

## 1. CONTEXTO DO LEGADO

### Cenário Geral

**Importante:** O sistema legado **NÃO possui um módulo específico** de Gestão de Custos por Ativo (TCO). O controle de custos está **disperso** em múltiplos módulos e é feito predominantemente de forma **manual** via planilhas externas.

- **Arquitetura:** Monolítica ASP.NET Web Forms com código VB.NET
- **Linguagem/Stack:** VB.NET, ASP.NET Web Forms, JavaScript, WebServices (.asmx)
- **Banco de Dados:** SQL Server com schema fragmentado
- **Multi-tenant:** Não (controle manual por empresa)
- **Auditoria:** Inexistente para custos
- **Configurações:** Web.config e tabelas de configuração dispersas

### Características Identificadas

1. **Controle de Custos Disperso:**
   - Custos de aquisição: registrados em cadastro de ativos (valor único)
   - Custos de manutenção: registrados em ordens de serviço (sem agregação por ativo)
   - Custos de licenças: registrados em contratos (sem link direto com ativo)
   - Consumíveis: sem rastreamento sistemático

2. **Cálculo de TCO:**
   - Não existe cálculo automático de TCO
   - Gestores usam planilhas Excel para consolidar custos manualmente
   - Não há histórico de evolução de custos por ativo

3. **Depreciação:**
   - Sem cálculo automático
   - Depreciação feita manualmente pelo setor contábil
   - Não está integrada ao sistema de ativos

4. **Análise de ROI:**
   - Não existe no sistema
   - Decisões de substituição baseadas em intuição ou vida útil genérica

---

## 2. TELAS DO LEGADO

### Conclusão da Análise

**Após análise completa do código legado (ic1_legado/IControlIT/), não foram identificadas telas específicas para gestão de custos por ativo.**

O que existe de forma relacionada:

| Módulo | Telas Relacionadas | Observações |
|--------|-------------------|-------------|
| **Gestão de Ativos** | `Ativo.aspx` | Cadastro de ativos com campo "ValorAquisicao" (custo inicial único) |
| **Ordens de Serviço** | `OrdemServico.aspx` | Registro de custos de manutenção, mas sem agregação por ativo |
| **Contratos** | `Contrato.aspx` | Custos de licenças/suporte, sem link explícito com ativo beneficiado |
| **Relatórios** | Não encontrado | Nenhum relatório de TCO ou análise de custos de ativos |

### Comportamento Implícito Identificado

Da análise do código existente:

1. **Ativo.aspx (Cadastro de Ativos):**
   - Campo `ValorAquisicao` armazena custo de aquisição (CAPEX)
   - Sem campos para custos operacionais (OPEX)
   - Sem campos para TCO total ou depreciação acumulada
   - Sem relacionamento com outras tabelas de custo

2. **OrdemServico.aspx:**
   - Registra custos de manutenção corretiva/preventiva
   - Campo `ValorTotal` da OS inclui mão de obra + peças
   - FK `AtivoId` existe mas não há agregação/consulta de custos por ativo
   - Sem classificação CAPEX vs. OPEX

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

### Análise de WebServices

**Não foram identificados WebServices específicos para gestão de custos de ativos.**

Possíveis serviços relacionados:

| Serviço | Localização | Responsabilidade | Status |
|---------|-------------|------------------|--------|
| `AtivoService.asmx` | (se existir) | CRUD de ativos com valor aquisição | Não localizado |
| `RelatorioService.asmx` | (se existir) | Relatórios gerenciais | Não localizado |

### Observação Crítica

A ausência de WebServices para custos indica que:
- Não havia integração sistêmica de custos
- Consolidação era feita manualmente
- Dados ficavam em planilhas fora do sistema

---

## 4. TABELAS LEGADAS

### Tabelas Identificadas

| Tabela | Finalidade | Problemas Identificados |
|--------|------------|-------------------------|
| `Custo_Ativo` | (possível) Registro de custos por ativo | ❌ Não localizada no schema legado - pode não existir |
| `Ativo` | Cadastro de ativos | ⚠️ Apenas campo `Valor_Aquisicao` - sem OPEX, sem TCO |
| `Ordem_Servico` | Ordens de serviço | ⚠️ Tem custo mas sem agregação por ativo |
| `Contrato` | Contratos de licenças | ⚠️ Sem FK direta para ativo beneficiado |
| `Contrato_Item` | Itens do contrato | ⚠️ FK para ativo pode existir mas sem agregação de custo |

### Problemas Estruturais

1. **Falta de Tabela Unificada de Custos:**
   - Não há tabela central `CustosAtivo` ou similar
   - Custos dispersos em múltiplas tabelas sem agregação

2. **Ausência de Campos de TCO:**
   - Tabela `Ativo` não tem campos `TCOTotal`, `TCOManutencao`, `TCOLicencas`, etc.
   - Sem campo `DataUltimaAtualizacaoTCO`

3. **Sem Histórico de Depreciação:**
   - Nenhuma tabela `HistoricoDepreciacao` ou `CustoDepreciacao`
   - Sem campos `ValorDepreciado`, `FlDepreciadoTotalmente`

4. **Auditoria Inexistente:**
   - Tabelas não têm campos de auditoria (quem/quando alterou custos)

---

## 5. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

### Regras Identificadas (ou Ausência Delas)

#### RL-RN-001: Custo de aquisição único e imutável
**Descrição:** Ativo tinha apenas um campo `ValorAquisicao` que não era atualizado após cadastro inicial.

**Fonte:** Análise de `Ativo.aspx` e estrutura da tabela `Ativo`

**Problema:** Não permitia registrar custos adicionais de aquisição (frete, instalação, configuração).

**Destino no RF Moderno:** **SUBSTITUÍDO** - RF037 permite múltiplos custos de categoria "Aquisição" com datas diferentes.

---

#### RL-RN-002: Custos de manutenção sem link forte com ativo
**Descrição:** Ordens de serviço registravam custos mas não consolidavam por ativo automaticamente.

**Fonte:** Análise de `OrdemServico.aspx` e estrutura da tabela `Ordem_Servico`

**Problema:** Gestores não sabiam quanto gastaram em manutenção de um ativo específico ao longo do tempo.

**Destino no RF Moderno:** **SUBSTITUÍDO** - RN-RF037-06 obriga vinculação de custos de manutenção a OrdemServicoId + agregação automática no TCO.

---

#### RL-RN-003: Ausência de categorização CAPEX vs. OPEX
**Descrição:** Sistema não diferenciava investimento (CAPEX) de despesa operacional (OPEX).

**Fonte:** Ausência de campos de categorização em todas as tabelas

**Problema:** Impossível gerar relatórios contábeis corretos separando investimentos de despesas.

**Destino no RF Moderno:** **SUBSTITUÍDO** - RN-RF037-07 implementa categorização obrigatória (enum CustoCategoriaEnum).

---

#### RL-RN-004: Depreciação manual e desconectada
**Descrição:** Depreciação era calculada manualmente pelo setor contábil em planilhas, sem integração com sistema de ativos.

**Fonte:** Entrevistas com usuários (não documentado em código)

**Problema:** Valor contábil do ativo no sistema não refletia depreciação acumulada.

**Destino no RF Moderno:** **SUBSTITUÍDO** - RN-RF037-03 implementa depreciação automática mensal via job.

---

#### RL-RN-005: Decisões de substituição baseadas em intuição
**Descrição:** Gestores decidiam substituir ativos baseados em "tempo de uso" genérico (ex: "notebook com 3 anos substitui") sem análise de custo real.

**Fonte:** Observação de processos e ausência de ferramentas analíticas

**Problema:** Substituição prematura (custo de manutenção ainda baixo) ou tardia (custo de manutenção já muito alto).

**Destino no RF Moderno:** **SUBSTITUÍDO** - RN-RF037-14 implementa recomendação automática baseada em TCO anual vs. valor de ativo novo.

---

## 6. GAP ANALYSIS (LEGADO × RF MODERNO)

| Funcionalidade | Legado | RF Moderno (RF037) | Observação |
|----------------|--------|-------------------|------------|
| **Registro de Custos por Ativo** | ❌ Inexistente (disperso) | ✅ Centralizado em `CustosAtivo` | Gap crítico - funcionalidade nova |
| **Cálculo de TCO Total** | ❌ Manual (planilhas) | ✅ Automático em tempo real | Gap crítico - automação obrigatória |
| **Cálculo de TCO por Categoria** | ❌ Inexistente | ✅ Agregação automática (CAPEX, OPEX, etc.) | Gap crítico - visibilidade gerencial |
| **Depreciação Automática** | ❌ Manual (contabilidade) | ✅ Job mensal automático | Gap crítico - compliance contábil |
| **Análise de ROI** | ❌ Inexistente | ✅ Cálculo automático com benefícios | Gap alto - decisões estratégicas |
| **Projeção de Custos Futuros** | ❌ Inexistente | ✅ Baseada em média histórica (12 meses) | Gap médio - planejamento orçamentário |
| **Comparação entre Ativos (Benchmarking)** | ❌ Inexistente | ✅ Comparação automática entre ativos do mesmo tipo | Gap médio - identificação de outliers |
| **Alertas de Custos Anormais** | ❌ Inexistente | ✅ Alerta automático se TCO > 130% da média | Gap médio - detecção proativa |
| **Recomendação de Substituição** | ❌ Baseada em intuição | ✅ Baseada em TCO anual vs. valor novo | Gap alto - otimização de gastos |
| **Dashboard de TCO** | ❌ Inexistente | ✅ Gráficos interativos (evolução, breakdown) | Gap médio - visualização executiva |
| **Exportação de Relatórios TCO** | ❌ Inexistente | ✅ Excel/PDF com breakdown completo | Gap médio - relatórios gerenciais |
| **Auditoria de Custos** | ❌ Inexistente | ✅ Auditoria completa (7 anos LGPD) | Gap crítico - compliance legal |
| **Multi-tenancy** | ⚠️ Controle manual | ✅ Automático (ConglomeradoId) | Melhoria - segurança e isolamento |
| **Permissões Granulares** | ⚠️ Perfil genérico | ✅ RBAC com 7 permissões específicas | Melhoria - controle de acesso fino |

### Conclusão do Gap Analysis

**Funcionalidades Legadas a Preservar:** ❌ **Nenhuma** - Não havia módulo de custos

**Funcionalidades Novas no RF Moderno:** ✅ **100%** - Todas são inovações

**Risco de Migração:** 🟢 **Baixo** - Não há dados legados a migrar, não há processos estabelecidos a quebrar

---

## 7. DECISÕES DE MODERNIZAÇÃO

### Decisão 1: Criar módulo de TCO do zero

**Motivo:**
- Sistema legado não possui controle de custos de ativos
- Ausência de dados históricos estruturados
- Oportunidade de implementar best practices desde o início

**Impacto:** 🟢 Baixo (não quebra processos existentes)

**Benefício:** Alto - funcionalidade completamente nova agrega valor imediato

---

### Decisão 2: Implementar depreciação automática

**Motivo:**
- Depreciação manual é propensa a erros
- Desconexão entre valor contábil e valor no sistema de ativos
- Compliance contábil exige depreciação consistente

**Impacto:** 🟡 Médio (mudança de processo contábil)

**Benefício:** Alto - valor contábil sempre atualizado automaticamente

---

### Decisão 3: Usar Domain Events para recálculo de TCO

**Motivo:**
- Garantir que TCO esteja sempre sincronizado
- Evitar inconsistências entre custos individuais e TCO agregado
- Padrão moderno de Clean Architecture

**Impacto:** 🟢 Baixo (decisão técnica interna)

**Benefício:** Alto - consistência garantida, manutenibilidade

---

### Decisão 4: Criar jobs para alertas e recomendações

**Motivo:**
- Detecção proativa de problemas (custos anormais)
- Automação de decisões (recomendação de substituição)
- Evitar necessidade de monitoramento manual

**Impacto:** 🟢 Baixo

**Benefício:** Alto - gestão proativa vs. reativa

---

### Decisão 5: Não migrar dados legados de custos

**Motivo:**
- Não existem dados estruturados no legado
- Custos históricos estão em planilhas não padronizadas
- Custo de consolidação manual seria alto vs. benefício

**Impacto:** 🟢 Baixo (usuários entendem que é funcionalidade nova)

**Benefício:** Médio - evita esforço de ETL complexo e propenso a erros

**Alternativa:** Permitir importação opcional via CSV se usuário tiver dados históricos organizados

---

## 8. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| **Resistência por mudança de processo (depreciação automática)** | 🟡 Médio | 🟡 Média | Treinamento do setor contábil, demonstrar benefícios de automação |
| **Expectativa de dados históricos** | 🟢 Baixo | 🟢 Baixa | Comunicar claramente que é funcionalidade nova, permitir importação manual se necessário |
| **Curva de aprendizado (múltiplas categorias de custo)** | 🟢 Baixo | 🟡 Média | Tooltips explicativos, exemplos de categorização, documentação clara |
| **Integração com módulos existentes (Ativos, OS, Contratos)** | 🟡 Médio | 🟡 Média | Testes de integração E2E, validar FKs, garantir que módulos dependentes estão funcionais |

---

## 9. RASTREABILIDADE

| Elemento Legado | Referência RF Moderno | Status Migração |
|-----------------|----------------------|----------------|
| `Ativo.Valor_Aquisicao` | RN-RF037-01, RN-RF037-07 (Categoria=Aquisicao) | ✅ Assumido (primeira entrada de custo) |
| Planilhas manuais de TCO | RF037 completo (substitui planilhas) | ✅ Substituído |
| Processo manual de depreciação | RN-RF037-03 (job automático) | ✅ Substituído |
| Decisões de substituição intuitivas | RN-RF037-14 (recomendação baseada em dados) | ✅ Substituído |
| Ordens de Serviço com custos | RN-RF037-06 (vinculação obrigatória) | ✅ Assumido e melhorado |
| Contratos com custos de licenças | RN-RF037-06 (vinculação obrigatória) | ✅ Assumido e melhorado |

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|--------|------|-----------|-------|
| 1.0 | 2025-12-30 | Documentação inicial de referência ao legado - análise completa revelou ausência de módulo TCO no legado | Agência ALC - alc.dev.br |
