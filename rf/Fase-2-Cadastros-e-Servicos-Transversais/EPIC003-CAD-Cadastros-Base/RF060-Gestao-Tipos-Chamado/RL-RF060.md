# RL-RF060 - Referência ao Legado: Gestão de Tipos de Chamado

**Versão:** 2.0
**Data de Criação:** 2025-12-30
**Governança:** v2.0 (Separação RF/RL)
**Status:** Não Aplicável

---

## 1. RESUMO DO SISTEMA LEGADO

### 1.1 Contexto Histórico

O **RF060 - Gestão de Tipos de Chamado** é uma **funcionalidade NOVA** que **NÃO possui correspondente no sistema legado** IControlIT (ASP.NET Web Forms + VB.NET).

Este RF foi projetado desde o início seguindo as melhores práticas de ITIL v4, Clean Architecture e padrões modernos de desenvolvimento.

### 1.2 Ausência de Sistema Legado

**NÃO EXISTE** nenhuma tela ASPX, stored procedure, tabela legada ou webservice ASMX relacionado a esta funcionalidade no sistema legado localizado em:
```
D:\IC2\ic1_legado\IControlIT\
```

### 1.3 Motivo da Ausência

O sistema legado **não possuía** gestão estruturada de tipos de chamado com:
- Classificação ITIL v4
- SLAs configuráveis por tipo/prioridade
- Formulários dinâmicos
- Templates de resolução (knowledge base)
- Escalonamento automático
- Métricas ITIL (MTTR, MTBF, FCR)
- Aprovação CAB para mudanças
- Integração com CMDB

Esta funcionalidade foi identificada como **necessidade crítica** durante a modernização do sistema, sendo projetada inteiramente do zero com base em:
- Framework ITIL v4 oficial
- Melhores práticas de Service Desk
- Requisitos de compliance e auditoria
- Necessidade de padronização de atendimento

---

## 2. INVENTÁRIO DE ARTEFATOS LEGADOS

### 2.1 Telas ASPX

**NENHUMA** tela ASPX corresponde a esta funcionalidade.

### 2.2 Code-Behind (VB.NET)

**NENHUM** arquivo `.aspx.vb` corresponde a esta funcionalidade.

### 2.3 Stored Procedures

**NENHUMA** stored procedure T-SQL corresponde a esta funcionalidade.

### 2.4 Tabelas do Banco de Dados

**NENHUMA** tabela do banco legado corresponde diretamente a esta funcionalidade.

**Observação:** Embora o banco legado possua tabelas genéricas como `Solicitacao` (chamados), estas **não possuem** tipificação estruturada, SLAs, formulários dinâmicos ou quaisquer características do RF060.

### 2.5 WebServices ASMX

**NENHUM** webservice ASMX corresponde a esta funcionalidade.

### 2.6 Integrações Externas

**NENHUMA** integração externa legada corresponde a esta funcionalidade.

---

## 3. ANÁLISE COMPARATIVA: LEGADO vs. MODERNO

### 3.1 Comparação de Funcionalidades

| Funcionalidade | Sistema Legado | RF060 Moderno |
|----------------|----------------|---------------|
| Classificação ITIL v4 | ❌ NÃO EXISTE | ✅ 4 categorias ITIL |
| SLA por tipo/prioridade | ❌ NÃO EXISTE | ✅ SLA configurável |
| Formulários dinâmicos | ❌ NÃO EXISTE | ✅ Campos customizados |
| Templates de resolução | ❌ NÃO EXISTE | ✅ Knowledge base |
| Escalonamento automático | ❌ NÃO EXISTE | ✅ Hangfire jobs |
| Matriz prioridade ITIL | ❌ NÃO EXISTE | ✅ Impacto × Urgência |
| Aprovação CAB | ❌ NÃO EXISTE | ✅ Workflow CAB |
| Vinculação incidente→problema | ❌ NÃO EXISTE | ✅ Análise causa raiz |
| Categorização hierárquica | ❌ NÃO EXISTE | ✅ 3 níveis |
| Especialistas preferenciais | ❌ NÃO EXISTE | ✅ Atribuição inteligente |
| Métricas ITIL | ❌ NÃO EXISTE | ✅ MTTR, MTBF, FCR |
| Integração CMDB | ❌ NÃO EXISTE | ✅ Vinculação com CIs |
| Janelas de mudança | ❌ NÃO EXISTE | ✅ Agendamento |
| Custos por tipo | ❌ NÃO EXISTE | ✅ Budget vs. Real |
| Relatórios gerenciais | ❌ NÃO EXISTE | ✅ Dashboards ITIL |

### 3.2 Conclusão da Análise

O **RF060 é 100% novo**, sem nenhuma correspondência no sistema legado. Toda a funcionalidade foi projetada do zero com base em:
- ITIL v4
- Melhores práticas de mercado
- Necessidades identificadas pelos stakeholders
- Padrões modernos de desenvolvimento

---

## 4. PROBLEMAS IDENTIFICADOS NO LEGADO

### 4.1 Ausência de Tipificação Estruturada

**Problema:** Sistema legado não possuía tipificação estruturada de chamados, dificultando:
- Priorização correta
- Atribuição de SLAs
- Estatísticas por categoria
- Identificação de problemas recorrentes

**Impacto:** Baixa eficiência no atendimento, SLA não cumprido, retrabalho.

**Solução no RF060:** Classificação obrigatória em 4 categorias ITIL v4 com SLA específico por tipo/prioridade.

### 4.2 Ausência de Knowledge Base

**Problema:** Sistema legado não possuía base de conhecimento integrada, obrigando técnicos a:
- Resolver problemas do zero sempre
- Consultar documentação externa
- Redigitar soluções conhecidas

**Impacto:** Tempo médio de resolução (MTTR) elevado, baixo First Call Resolution (FCR).

**Solução no RF060:** Templates de resolução reutilizáveis com controle de taxa de sucesso e quantidade de usos.

### 4.3 Ausência de Escalonamento Automático

**Problema:** Sistema legado não possuía escalonamento automático, dependendo de ação manual do técnico.

**Impacto:** Chamados críticos não atendidos no prazo, violação de SLA.

**Solução no RF060:** Job Hangfire a cada 5 minutos escalona automaticamente chamados não atendidos.

### 4.4 Ausência de Métricas ITIL

**Problema:** Sistema legado não calculava métricas ITIL (MTTR, MTBF, FCR).

**Impacto:** Impossibilidade de medir eficiência do Service Desk, falta de dados para tomada de decisão.

**Solução no RF060:** Cálculo automático de métricas ITIL com dashboards e trending.

---

## 5. JUSTIFICATIVA PARA AUSÊNCIA DE MIGRAÇÃO

### 5.1 Por Que Não Houve Migração de Dados

**NÃO HÁ DADOS** para migrar, pois:
- Sistema legado não possuía tipos de chamado estruturados
- Não existem SLAs configurados no legado
- Não existem formulários dinâmicos no legado
- Não existem templates de resolução no legado

### 5.2 Abordagem de Implementação

O RF060 será implementado **do zero**, seguindo as fases:

1. **Fase 1 - Backend**:
   - Criar entidades (TipoChamado, SLATipoChamado, FormularioTipoChamado, etc.)
   - Criar Commands e Queries (CQRS)
   - Criar Validators (FluentValidation)
   - Criar Endpoints (Minimal APIs)
   - Criar Jobs Hangfire (escalonamento, notificações SLA)

2. **Fase 2 - Frontend**:
   - Criar componentes Angular 19 (list, form, detail)
   - Criar formulários dinâmicos renderizados por JSON
   - Criar dashboards com métricas ITIL
   - Criar wizard de configuração de tipos

3. **Fase 3 - Testes**:
   - Testes unitários (backend)
   - Testes E2E (Playwright)
   - Testes de carga (formulários dinâmicos)
   - Testes de SLA (cálculo de deadline)

4. **Fase 4 - Seed Inicial**:
   - Criar tipos de chamado padrão ITIL (Incidente, Requisição, Mudança, Problema)
   - Configurar SLAs básicos
   - Criar templates de resolução comuns
   - Configurar escalonamento padrão (N1 → N2 → N3)

---

## 6. REGRAS DE NEGÓCIO LEGADAS

### 6.1 Regras Identificadas

**NENHUMA** regra de negócio legada foi identificada para esta funcionalidade.

### 6.2 Regras Assumidas vs. Descartadas

Como não há sistema legado, **não há regras assumidas ou descartadas**.

Todas as 15 regras de negócio (RN-RF060-001 a RN-RF060-015) do RF060 foram criadas **do zero** com base em:
- ITIL v4 oficial
- Melhores práticas de Service Desk
- Requisitos de stakeholders
- Necessidades de compliance

---

## 7. DECISÕES DE TRANSIÇÃO

### 7.1 Estratégia de Corte

**NÃO APLICÁVEL** - Não há sistema legado para descontinuar.

O RF060 será **novo** e coexistirá com o módulo de chamados do sistema moderno (RF061, RF062, etc.).

### 7.2 Cronograma de Desativação

**NÃO APLICÁVEL** - Não há funcionalidade legada para desativar.

### 7.3 Plano de Rollback

Em caso de problemas na implementação do RF060:

1. **Rollback de Código**: Reverter para branch anterior
2. **Rollback de Banco**: Remover migrations do RF060
3. **Fallback Operacional**: Operar temporariamente sem tipificação estruturada (criar todos os chamados como "Incidente" genérico)

**Observação:** Como não há legado, não há "sistema anterior" para voltar.

---

## 8. CONCLUSÃO

### 8.1 Situação Atual

- ✅ **RF060.md v2.0** criado (11 seções canônicas)
- ✅ **RF060.yaml** criado (sincronizado com RF.md)
- ✅ **RL-RF060.md** criado (documenta ausência de legado)
- 🔄 **RL-RF060.yaml** será criado (com seção `referencias` vazia)

### 8.2 Próximos Passos

1. Criar RL-RF060.yaml (estrutura válida com `referencias: []`)
2. Executar validator-rl.py RF060 (deve passar mesmo com referências vazias)
3. Atualizar STATUS.yaml (marcar v2.0 completo)
4. Commit Git de todos os artefatos

### 8.3 Status de Governança

- **Governança v2.0:** ✅ Aderente
- **Separação RF/RL:** ✅ Completa (RL documenta ausência de legado)
- **Rastreabilidade:** ✅ Total (documentado que não há legado)
- **Validação Pendente:** 🔄 Executar validator-rl.py

---

**Documento controlado pela Governança v2.0 - IControlIT**
**Última revisão:** 2025-12-30
