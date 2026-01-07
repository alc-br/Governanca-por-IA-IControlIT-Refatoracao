# RL-RF072 — Referência ao Legado: Escalação Automática

**Versão:** 1.0
**Data:** 2025-12-30
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF-072
**Sistema Legado:** ASP.NET Web Forms + VB.NET
**Objetivo:** Documentar a ausência de funcionalidade equivalente no legado e mapear escalações manuais realizadas via email/telefone.

---

## 1. CONTEXTO DO LEGADO

### Stack Tecnológica
- **Arquitetura:** Monolítica WebForms (ASP.NET 4.x)
- **Linguagem:** VB.NET (code-behind)
- **Banco de Dados:** SQL Server multi-database (1 banco por cliente)
- **Multi-tenant:** Não (cada cliente = banco separado)
- **Auditoria:** Inexistente para escalações
- **Configurações:** Web.config + tabelas de configuração

### Problemas Arquiteturais Identificados

1. **Ausência Total de Escalação Automática**: Sistema legado NÃO possui engine de escalação automática. Escalações eram feitas manualmente via:
   - Email entre analistas (sem registro)
   - Telefone/chat interno (sem rastreabilidade)
   - Reatribuição manual de chamados na UI

2. **Sem Rastreabilidade**: Não há log de quem escalou para quem, quando, por quê. Impossível auditar ou analisar padrões.

3. **Sem Skill-Based Routing**: Escalações aleatórias ou baseadas em conhecimento pessoal (não sistematizado).

4. **Sem SLA Triggers**: Sistema não verifica SLA automaticamente. Analistas tinham que monitorar manualmente.

5. **Sem Multi-Canal de Notificação**: Apenas email manual. Analistas não eram notificados sobre novas atribuições.

---

## 2. TELAS DO LEGADO

### Ausência de Telas Específicas

**Não existem telas ASPX dedicadas à escalação automática no sistema legado.**

O sistema possui apenas:
- `ChamadoDetalhe.aspx` - Permite reatribuir chamado manualmente (dropdown de analistas)
- `ChamadoLista.aspx` - Lista chamados sem indicação de escalação

**Destino:** `FUNCIONALIDADE_NOVA` (não existe equivalente legado)

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

### Ausência de Webservices Específicos

Não foram encontrados webservices (.asmx) relacionados a:
- Escalação automática
- Triggers de SLA
- Skill-based routing
- Notificações de escalação

**Destino:** `FUNCIONALIDADE_NOVA`

---

## 4. TABELAS LEGADAS

### Tabelas Relacionadas (com problemas)

| Tabela | Finalidade | Problemas Identificados | Destino |
|--------|------------|------------------------|---------|
| `Chamado` | Registro de chamados/tickets | Sem campo `AnalistaAtribuidoAnterior`, `HistoricoEscalacao`, `SLAConsumido` | `SUBSTITUÍDO` por `Escalacao` + `EscalacaoAuditoria` |
| `Usuario` | Cadastro de analistas | Sem skills, sem nível de escalação, sem capacidade de carga | `ASSUMIDO` + campos adicionais (Skills, NivelAcesso, ChamadosAtivos) |
| `Nenhuma` | Auditoria de escalação | **NÃO EXISTE** | `CRIADO` - `EscalacaoAuditoria` (7 anos retenção) |

**Observações:**
- Campo `AnalistaResponsavelId` em `Chamado` era sobrescrito sem histórico
- Sem FK constraints entre `Chamado` e `Usuario` (integridade frágil)
- Sem campos de auditoria (Created, CreatedBy, Modified, ModifiedBy)

---

## 5. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

### RL-RN-001: Reatribuição Manual via UI

**Descrição:** Analistas podiam reatribuir chamados manualmente via dropdown em `ChamadoDetalhe.aspx`. Ação NÃO registrada em auditoria.

**Localização:** `ic1_legado/IControlIT/ServiceDesk/ChamadoDetalhe.aspx.vb` - Linha ~450

**Destino:** `SUBSTITUÍDO` por escalação automática + escalação manual com auditoria (RF-072)

---

### RL-RN-002: Notificação Manual via Email

**Descrição:** Após reatribuir, analista origem enviava email manual (BCC frequente, não-rastreável) informando analista destino.

**Localização:** `ic1_legado/IControlIT/Helpers/EmailHelper.vb` - Linha ~230

**Destino:** `SUBSTITUÍDO` por notificações multi-canal automáticas (email + SMS + in-app + Teams)

---

### RL-RN-003: SLA Verificado Manualmente

**Descrição:** Sistema exibia tempo decorrido, mas NÃO disparava ações automáticas. Gestores checavam relatórios 2x/dia.

**Localização:** `ic1_legado/IControlIT/ServiceDesk/ChamadoLista.aspx.vb` - Cálculo de SLA

**Destino:** `SUBSTITUÍDO` por triggers automáticos de SLA (50%, 75%, 90%, 100%)

---

## 6. GAP ANALYSIS (LEGADO x RF MODERNO)

| Item | Existe no Legado? | Existe no Moderno (RF-072)? | Observação |
|------|-------------------|------------------------------|------------|
| **Escalação Automática** | ❌ Não | ✅ Sim | Funcionalidade completamente nova |
| **Skill-Based Routing** | ❌ Não | ✅ Sim | Algoritmo com score ponderado |
| **Triggers de SLA** | ❌ Não | ✅ Sim | 50%, 75%, 90%, 100% |
| **Matriz Hierárquica** | ❌ Não | ✅ Sim | Configurável por cliente |
| **Notificações Multi-Canal** | ⚠️ Parcial (só email manual) | ✅ Sim | Email + SMS + in-app + Teams |
| **Auditoria de Escalação** | ❌ Não | ✅ Sim | Log completo (7 anos) |
| **Balanceamento de Carga** | ❌ Não | ✅ Sim | Pausa automática >8 chamados |
| **Dashboard de Escalações** | ❌ Não | ✅ Sim | Real-time com SignalR |
| **Pausas Temporárias** | ❌ Não | ✅ Sim | Integração com AD |
| **Aceite/Rejeição** | ❌ Não | ✅ Sim | Com SLA <5min e registro de motivo |

---

## 7. DECISÕES DE MODERNIZAÇÃO

### Decisão 1: Criar Funcionalidade do Zero

**Motivo:** Sistema legado não possui escalação automática. Implementar do zero permite usar padrões modernos (CQRS, eventos de domínio, SignalR) sem carregar débito técnico.

**Impacto:** Alto (desenvolvimento completo), mas permite arquitetura limpa.

**Data:** 2025-12-28

---

### Decisão 2: Não Migrar Histórico de Reatribuições Manuais

**Motivo:** Legado não registrava escalações (somente sobrescrevia `AnalistaResponsavelId`). Não há dados históricos para migrar.

**Impacto:** Baixo (não há dados para perder).

**Data:** 2025-12-28

---

### Decisão 3: Implementar Multi-Tenancy com Matriz Independente

**Motivo:** Legado tinha bancos separados por cliente. Modernizar permite matriz de escalação configurável por cliente em banco único (Row-Level Security).

**Impacto:** Médio (complexidade de multi-tenancy), mas habilita flexibilidade operacional.

**Data:** 2025-12-28

---

## 8. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Probabilidade | Mitigação |
|------|---------|---------------|-----------|
| **Resistência de Usuários** | Alto | Média | Treinamento intensivo, rollout gradual, manter reatribuição manual por 3 meses |
| **Complexidade de Configuração Inicial** | Médio | Alta | Wizard de configuração de matriz, templates pré-prontos, suporte dedicado |
| **Integração com AD Pode Falhar** | Médio | Baixa | Fallback para pausas manuais, retry automático 5x, alertas se sync falhar |
| **Performance com 1000+ Analistas** | Alto | Baixa | Cache Redis para scores, indexação otimizada, testes de carga obrigatórios |
| **Escalações Incorretas (Score Baixo)** | Médio | Média | Threshold mínimo score 0.3, escala próximo nível se não encontrar match |

---

## 9. RASTREABILIDADE

| Elemento Legado | Referência RF Moderno | Status |
|----------------|-----------------------|--------|
| `ChamadoDetalhe.aspx` (reatribuição manual) | UC01-RF072 (Criar escalação manual) | Substituído |
| `EmailHelper.vb` (email manual) | RN-RF072-007 (Notificações multi-canal) | Substituído |
| Cálculo SLA manual | RN-RF072-001 (Triggers automáticos SLA) | Substituído |
| Tabela `Chamado` | Entidade `Escalacao` + `EscalacaoAuditoria` | Substituído |
| N/A (não existe) | Skill-Based Routing | Funcionalidade Nova |
| N/A (não existe) | Matriz Hierárquica | Funcionalidade Nova |
| N/A (não existe) | Balanceamento de Carga | Funcionalidade Nova |
| N/A (não existe) | Dashboard Real-time | Funcionalidade Nova |

---

## 10. CONHECIMENTO PRESERVADO DO LEGADO

Embora o RF-072 seja funcionalidade nova, conhecimentos preservados do legado incluem:

1. **Conceito de Responsável do Chamado** - Mantido, mas agora com histórico completo de mudanças
2. **Prioridades P1/P2/P3** - Assumidas do legado, agora com triggers automáticos
3. **Estrutura de SLA** - Conceito existente, agora com monitoramento automático
4. **Multi-Tenancy** - Evolução de bancos separados para banco único com `ClienteId`

---

## CHANGELOG

| Versão | Data | Descrição |
|--------|------|-----------|
| 1.0 | 2025-12-30 | Versão inicial - Documentação de ausência de escalação automática no legado |
