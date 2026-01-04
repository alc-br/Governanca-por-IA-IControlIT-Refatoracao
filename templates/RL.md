# RL-RFXXX — Referência ao Legado

**Versão:** 1.0  
**Data:** YYYY-MM-DD  
**Autor:** Agência ALC - alc.dev.br  

**RF Moderno Relacionado:** RF-XXX  
**Sistema Legado:** [Nome do Sistema / Tecnologia]  
**Objetivo:** Documentar o comportamento do legado que serve de base para a refatoração, garantindo rastreabilidade, entendimento histórico e mitigação de riscos.

---

## 1. CONTEXTO DO LEGADO

Descreve o cenário geral do sistema legado.

- Arquitetura: [Monolítica / Cliente-Servidor / WebForms / etc.]
- Linguagem / Stack: [VB.NET, ASP.NET, etc.]
- Banco de Dados: [SQL Server, Oracle, etc.]
- Multi-tenant: [Sim/Não]
- Auditoria: [Inexistente / Parcial / Completa]
- Configurações: [Web.config, arquivos, banco, etc.]

---

## 2. TELAS DO LEGADO

### Tela: [Nome do Arquivo]

- **Caminho:** [Path completo]
- **Responsabilidade:** [O que a tela faz]

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|------|------|-------------|-------------|

#### Comportamentos Implícitos

- [Comportamento não documentado]
- [Validação ausente]
- [Regra escondida no código]

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

| Método | Local | Responsabilidade | Observações |
|------|-------|------------------|-------------|

---

## 4. TABELAS LEGADAS

| Tabela | Finalidade | Problemas Identificados |
|-------|------------|-------------------------|

---

## 5. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

Liste regras que não estavam documentadas formalmente.

- RL-RN-001: [Descrição da regra]
- RL-RN-002: [Descrição da regra]

---

## 6. GAP ANALYSIS (LEGADO x RF MODERNO)

| Item | Legado | RF Moderno | Observação |
|-----|--------|------------|------------|

---

## 7. DECISÕES DE MODERNIZAÇÃO

Explique decisões tomadas durante a refatoração.

- Decisão: [Descrição]
- Motivo: [Justificativa]
- Impacto: [Alto / Médio / Baixo]

---

## 8. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Mitigação |
|------|---------|-----------|

---

## 9. RASTREABILIDADE

| Elemento Legado | Referência RF |
|----------------|---------------|

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|------|------|----------|------|
| 1.0 | YYYY-MM-DD | Template inicial de referência ao legado | Agência ALC - alc.dev.br |
