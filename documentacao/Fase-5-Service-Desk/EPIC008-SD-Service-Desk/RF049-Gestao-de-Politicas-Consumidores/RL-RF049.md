# RL-RF049 — Referência ao Legado: Gestão de Políticas de Consumidores

**Versão:** 1.0
**Data:** 2025-12-30
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF-049 - Gestão de Políticas de Consumidores
**Sistema Legado:** IControlIT v1 (VB.NET + ASP.NET Web Forms)
**Objetivo:** Documentar ausência de funcionalidade equivalente no legado e justificar necessidade de desenvolvimento completo do zero.

---

## 1. CONTEXTO DO LEGADO

### 1.1 Cenário Geral

O sistema legado IControlIT v1 **NÃO possui** funcionalidade estruturada de gestão de políticas de consumidores. O controle de consumo era feito de forma:

- **Arquitetura:** Monolítica WebForms
- **Linguagem / Stack:** VB.NET, ASP.NET Web Forms
- **Banco de Dados:** SQL Server
- **Multi-tenant:** Parcial (campo IdEmpresa em algumas tabelas)
- **Auditoria:** Inexistente para políticas
- **Configurações:** Valores fixos em código ou Web.config

### 1.2 Como o Controle de Consumo Funcionava no Legado

1. **Limites Manuais**: Gestores configuravam limites manualmente em contratos/faturas
2. **Alertas Reativos**: Alertas enviados DEPOIS do consumo (via análise de faturas mensais)
3. **Bloqueios Manuais**: Operador bloqueava manualmente consumidores que excediam limites
4. **Sem Automação**: Não havia motor de políticas ou aplicação automática
5. **Sem Histórico**: Não havia rastreamento de quem aplicou/removeu restrições

### 1.3 Problemas Identificados no Legado

- ❌ **Controle Reativo**: Alertas só após fatura fechada (30-60 dias depois)
- ❌ **Sem Prevenção**: Não bloqueava consumo em tempo real
- ❌ **Trabalho Manual**: Gestor precisava revisar faturas e bloquear manualmente
- ❌ **Sem Auditoria**: Não rastreava quem bloqueou/desbloqueou ou por quê
- ❌ **Sem Conformidade**: Não registrava histórico para LGPD
- ❌ **Sem Templates**: Cada limite configurado individualmente
- ❌ **Sem Simulação**: Impossível prever impacto de limites antes de aplicar

---

## 2. TELAS DO LEGADO

### ⚠️ INEXISTENTE NO LEGADO

Não há telas dedicadas para gestão de políticas de consumidores no sistema legado.

O controle era feito através de:
- Tela de contratos (configuração manual de limites por contrato)
- Tela de consumidores (bloqueio manual via dropdown de status)
- Relatórios de faturas (revisão manual mensal)

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

### ⚠️ INEXISTENTE NO LEGADO

Não há webservices ou métodos relacionados a políticas de consumidores.

A lógica existente estava dispersa em:
- Code-behind de páginas ASPX
- Stored procedures de faturamento
- Validações em helpers genéricos

---

## 4. TABELAS LEGADAS

### ⚠️ SEM ESTRUTURA FORMAL

Não há tabelas dedicadas para políticas. O controle era feito através de:

| Tabela | Finalidade no Legado | Problemas Identificados |
|--------|----------------------|-------------------------|
| Contrato | Armazena limite mensal fixo | Sem histórico, sem tipos de limite, sem aplicação automática |
| Consumidor | Status manual (ativo/bloqueado) | Bloqueio manual, sem rastreamento de motivo, sem auditoria |
| Fatura | Análise de consumo mensal | Reativo (30-60 dias de atraso), sem alertas proativos |

**Nota:** Sistema legado usava apenas `valor_limite_mensal` no contrato, sem diferenciação de tipos (dados/voz/SMS), sem limiares de alerta, sem histórico de aplicações.

---

## 5. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

### RL-RN-001: Limite Único por Contrato

**Descrição:** Cada contrato tinha apenas UM valor de limite mensal em R$, aplicado a TODO tipo de consumo (dados + voz + SMS combinados).

**Fonte:** Tabela `Contrato.ValorLimite` + análise de código

**Problema:** Sem granularidade. Impossível limitar apenas dados ou apenas voz separadamente.

**Destino:** SUBSTITUÍDO por RN-RF049-01 (múltiplos tipos de políticas)

---

### RL-RN-002: Alerta Manual Mensal

**Descrição:** Gestor recebia relatório mensal de faturas e identificava manualmente consumidores acima do limite.

**Fonte:** Processo manual documentado em treinamento de usuários

**Problema:** Atraso de 30-60 dias. Consumo excessivo já tinha ocorrido.

**Destino:** SUBSTITUÍDO por RN-RF049-04 (alertas proativos em 50%, 80%, 100%)

---

### RL-RN-003: Bloqueio Manual via Status

**Descrição:** Operador alterava status do consumidor para "Bloqueado" manualmente através de dropdown.

**Fonte:** Tela `Consumidores.aspx`, método `AlterarStatus()`

**Problema:** Sem auditoria de quem bloqueou, quando e por quê. Sem integração com políticas.

**Destino:** SUBSTITUÍDO por RN-RF049-05 (bloqueio automático por violação)

---

### RL-RN-004: Sem Diferenciação de Perfil

**Descrição:** Todos os consumidores tinham o mesmo tipo de limite, independente de cargo (executivo vs estagiário).

**Fonte:** Análise de dados históricos

**Problema:** Gestão rígida. Sem flexibilidade para perfis diferentes.

**Destino:** SUBSTITUÍDO por RN-RF049-02 (aplicação automática por perfil)

---

### RL-RN-005: Sem Histórico de Mudanças

**Descrição:** Não havia registro de quando limites foram alterados, quem alterou ou por quê.

**Fonte:** Análise de tabelas (sem campos de auditoria)

**Problema:** Violação de LGPD. Impossível rastrear decisões.

**Destino:** SUBSTITUÍDO por RN-RF049-07 (histórico imutável 7 anos)

---

## 6. GAP ANALYSIS (LEGADO x RF MODERNO)

| Funcionalidade | Legado | RF049 Moderno | Observação |
|----------------|--------|---------------|------------|
| Motor de Políticas | ❌ Inexistente | ✅ Motor com avaliação em tempo real (≤100ms) | Nova funcionalidade |
| Tipos de Política | ❌ Apenas limite monetário total | ✅ 8 tipos (monetário, dados, voz, SMS, horário, destino, roaming, tipo de serviço) | Expansão significativa |
| Aplicação Automática | ❌ Manual | ✅ Automática por perfil/status via Domain Events | Automação completa |
| Alertas Proativos | ❌ Inexistente (apenas reativo mensal) | ✅ Alertas em 50%, 80%, 100% | Prevenção vs reação |
| Bloqueio Automático | ❌ Manual | ✅ Automático ao atingir 100% | Automação |
| Histórico de Aplicações | ❌ Inexistente | ✅ Histórico imutável 7 anos (LGPD) | Conformidade legal |
| Histórico de Violações | ❌ Inexistente | ✅ Registro automático de violações | Análise e auditoria |
| Dashboard de Conformidade | ❌ Inexistente | ✅ Dashboard em tempo real via SignalR | Visibilidade gerencial |
| Simulador de Impacto | ❌ Inexistente | ✅ Simulador antes de aplicar | Redução de risco |
| Templates de Políticas | ❌ Inexistente | ✅ Templates pré-configurados | Agilidade |
| Processamento em Lote | ❌ Inexistente | ✅ Aplicação em lote assíncrona | Escalabilidade |
| Importação/Exportação | ❌ Inexistente | ✅ Importar/Exportar JSON | Portabilidade |
| Cálculo de Economia | ❌ Inexistente | ✅ Cálculo automático com baseline | ROI mensurável |
| API de Avaliação | ❌ Inexistente | ✅ API para verificação prévia | Integração |
| Multi-tenancy | ⚠️ Parcial | ✅ Completo (Id_Fornecedor) | Segurança |
| Auditoria | ❌ Inexistente | ✅ Auditoria completa (CREATE, UPDATE, DELETE, APPLY, REMOVE) | Rastreabilidade |

**Resumo:** RF049 é **100% novo**. Não há código legado para migrar, apenas processo manual para automatizar.

---

## 7. DECISÕES DE MODERNIZAÇÃO

### Decisão 1: Desenvolvimento Completo do Zero

**Descrição:** Implementar RF049 completamente do zero, sem tentar adaptar código legado.

**Motivo:** Sistema legado não possui estrutura ou código reutilizável. Processo era 100% manual.

**Impacto:** Alto (desenvolvimento completo), mas necessário para atingir objetivos de automação e conformidade.

---

### Decisão 2: Motor de Políticas com Fail-Open

**Descrição:** Em caso de falha do motor de políticas, sistema permite operação (com log de alerta).

**Motivo:** Disponibilidade do sistema é prioritária. Melhor permitir temporariamente do que bloquear operação crítica.

**Impacto:** Médio (risco de não bloquear violação durante falha), mitigado por monitoramento intensivo.

---

### Decisão 3: Histórico Imutável Separado

**Descrição:** Criar tabela `PoliticaConsumidorHistorico` separada, apenas com inserts (sem updates/deletes).

**Motivo:** Conformidade com LGPD e rastreabilidade total de decisões.

**Impacto:** Baixo (armazenamento), mas crítico para conformidade legal.

---

### Decisão 4: Alertas em 3 Limiares (50%, 80%, 100%)

**Descrição:** Implementar alertas em múltiplos limiares ao invés de apenas 100%.

**Motivo:** Dar tempo para ação preventiva antes de bloqueio automático.

**Impacto:** Médio (complexidade de monitoramento), mas alto valor para gestores.

---

### Decisão 5: Processamento Assíncrono em Lote

**Descrição:** Usar Hangfire para processar aplicação de políticas em lote de forma assíncrona.

**Motivo:** Aplicar política a milhares de consumidores não pode bloquear interface.

**Impacto:** Baixo (infraestrutura já existente), alto ganho de escalabilidade.

---

## 8. RISCOS DE MIGRAÇÃO

### ⚠️ NÃO SE APLICA

Como não há funcionalidade legada para migrar, não há riscos de migração tradicionais (perda de dados, quebra de funcionalidade, etc.).

Os riscos são de **adoção** (mudança de processo manual para automático):

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| Resistência de usuários (acostumados com controle manual) | Médio | Alta | Treinamento, período de transição com ambos os processos |
| Políticas muito restritivas bloqueando uso legítimo | Alto | Média | Simulador de impacto obrigatório antes de aplicar |
| Falsos positivos em alertas | Baixo | Média | Tuning de limiares durante piloto |
| Sobrecarga de notificações | Médio | Média | Deduplicação de alertas (1 por limiar por período) |

---

## 9. RASTREABILIDADE

### ⚠️ NÃO SE APLICA

Não há elementos legados para rastrear. Toda funcionalidade é nova.

**Processo Manual Legado → RF049 Moderno:**

| Processo Manual Legado | Referência RF049 |
|------------------------|------------------|
| Gestor revisa fatura mensal e identifica excessos | RN-RF049-09 (API de avaliação em tempo real) |
| Gestor bloqueia manualmente consumidor | RN-RF049-05 (bloqueio automático) |
| Gestor define limite por contrato | RN-RF049-01, RN-RF049-02 (múltiplos tipos, aplicação por perfil) |
| Gestor envia e-mail para consumidor sobre excesso | RN-RF049-04 (alertas proativos automáticos) |

---

## CHANGELOG

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 1.0 | 2025-12-30 | Agência ALC - alc.dev.br | Criação inicial - Documentação de ausência de legado e justificativa de desenvolvimento do zero |
