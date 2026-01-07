# RL-RF040 — Referência ao Legado

**Versão:** 1.0
**Data:** 2025-12-30
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF040 - Gestão de Troncos Telefônicos
**Sistema Legado:** IControlIT v1 (VB.NET + ASP.NET Web Forms)
**Objetivo:** Documentar a **ausência** de funcionalidade equivalente no sistema legado, garantindo rastreabilidade e entendimento de que RF040 é uma funcionalidade 100% nova sem base legada.

---

## 1. CONTEXTO DO LEGADO

O sistema legado **IControlIT v1** não possuía módulo dedicado de gestão de troncos telefônicos. O controle de infraestrutura de telefonia era realizado de forma **manual e externa** ao sistema, com as seguintes características:

- **Arquitetura:** Monolítica WebForms + VB.NET
- **Linguagem / Stack:** VB.NET, ASP.NET Web Forms, SQL Server
- **Banco de Dados:** SQL Server (sem tabelas relacionadas a troncos)
- **Multi-tenant:** Não implementado para telefonia
- **Auditoria:** Inexistente para eventos de telefonia
- **Configurações:** Gerenciadas manualmente no PABX (Asterisk CLI ou interface web do gateway)
- **Monitoramento:** Manual, verificação esporádica por equipe de TI
- **Métricas de QoS:** Não coletadas ou armazenadas
- **Failover:** Manual, requer intervenção técnica
- **Custeio:** Controle via planilhas Excel separadas do sistema

**Conclusão:** RF040 representa uma **evolução funcional completa** sem base no sistema legado. Toda a lógica de monitoramento, failover, QoS e custeio é nova.

---

## 2. TELAS DO LEGADO

### Análise de Telas Relacionadas a Telefonia

**Resultado da Busca:** Não foram identificadas telas específicas para gestão de troncos telefônicos no sistema legado.

#### Telas Indiretamente Relacionadas:

**Possível relação com RF039 (Gestão de Bilhetes Telefônicos):**
- O legado pode ter telas de visualização de bilhetes telefônicos (CDR - Call Detail Records)
- Essas telas exibiam custos de chamadas mas **não gerenciavam troncos**
- Troncos eram apenas referenciados indiretamente nos registros de chamadas

**Caminho provável (não confirmado):**
- `ic1_legado/IControlIT/Telefonia/Relatorios/BilhetesTelefonicos.aspx` (possível)
- `ic1_legado/IControlIT/Telefonia/Consultas/ChamadasRealizadas.aspx` (possível)

**Observação:** Essas telas (se existirem) são escopo de RF039, não de RF040.

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

| Método | Local | Responsabilidade | Observações |
|--------|-------|------------------|-------------|
| **Nenhum identificado** | N/A | N/A | Sistema legado não possuía WebServices para gestão de troncos |

**Análise de Serviços de Telefonia:**
- Não foram encontrados serviços `.asmx` ou classes VB.NET relacionados a troncos
- Possível existência de serviços de consulta de bilhetes (escopo RF039)
- Integração com PABX (se existia) era feita diretamente pelo PABX, não pelo IControlIT

---

## 4. TABELAS LEGADAS

| Tabela | Finalidade | Problemas Identificados |
|--------|------------|-------------------------|
| **Nenhuma identificada** | N/A | Não havia tabelas de troncos no banco de dados legado |

**Análise de Esquema de Banco de Dados:**
- Não foram encontradas tabelas como `Tronco`, `TroncoTelefonico`, `LinhasTelefonicas`, `MetricasQoS`
- Possível existência de tabelas de bilhetes (escopo RF039): `BilheteTelefonico`, `RegistroChamada`
- Informações de troncos (se existiam) estavam **apenas na configuração do PABX**, não no banco IControlIT

**Implicação:**
- RF040 requer criação completa de schema de banco de dados (MD-RF040.yaml)
- Sem migração de dados legados (não há dados a migrar)

---

## 5. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

**Resultado:** Nenhuma regra de negócio relacionada a gestão de troncos foi identificada no código legado.

### Possíveis Regras Implícitas em Processos Manuais:

Embora não implementadas no sistema, a equipe de TI pode ter seguido procedimentos manuais:

- **RL-RN-001:** Verificação diária manual de status de troncos (CLI do Asterisk: `sip show peers`)
- **RL-RN-002:** Failover manual em caso de falha (reconfiguração de rotas no PABX)
- **RL-RN-003:** Análise mensal de custos via planilha Excel (fora do IControlIT)
- **RL-RN-004:** Relatórios de disponibilidade gerados manualmente a partir de logs do PABX

**Observação:** Essas "regras" eram **processos operacionais**, não regras de sistema. RF040 automatiza completamente esses processos.

---

## 6. GAP ANALYSIS (LEGADO x RF MODERNO)

| Item | Legado | RF Moderno (RF040) | Observação |
|------|--------|---------------------|------------|
| **Cadastro de Troncos** | ❌ Não existe | ✅ CRUD completo | Funcionalidade 100% nova |
| **Monitoramento em Tempo Real** | ❌ Manual (CLI) | ✅ Polling 30s automático | Automação completa |
| **Métricas de QoS** | ❌ Não coletadas | ✅ Jitter, latência, packet loss, MOS | Nova funcionalidade |
| **Failover Automático** | ❌ Manual (>1h) | ✅ Automático (<5s) | Ganho de 99,86% em velocidade |
| **Balanceamento de Carga** | ❌ Não existe | ✅ Least Call Count | Nova funcionalidade |
| **Custeio por Tronco** | ❌ Planilha Excel | ✅ Automatizado + rateio | Integração com ERP |
| **Dashboard de QoS** | ❌ Não existe | ✅ Tempo real + histórico | Nova funcionalidade |
| **Relatórios MTBF/MTTR** | ❌ Não existe | ✅ Análise de confiabilidade | Nova funcionalidade |
| **Simulador de Economia** | ❌ Não existe | ✅ ROI SIP vs E1 | Ferramenta de decisão nova |
| **Detecção de Anomalias** | ❌ Não existe | ✅ Loops, fraudes | Segurança nova |
| **Integração com PABX** | ❌ Manual | ✅ API REST + SNMP | Automação completa |
| **Alertas Proativos** | ❌ Reativos (usuário reclama) | ✅ SMS/e-mail/push | Proatividade |
| **Auditoria de Telefonia** | ❌ Inexistente | ✅ Completa (7 anos) | Compliance LGPD |
| **Multi-Tenancy** | ❌ Não suportado | ✅ Isolamento por tenant | Adequação arquitetural |

**Resumo do Gap:**
- **14 funcionalidades novas** sem equivalente no legado
- **0 funcionalidades migradas** (não há base legada)
- **100% de inovação funcional**

---

## 7. DECISÕES DE MODERNIZAÇÃO

### Decisão 1: Criar Funcionalidade Completamente Nova

**Descrição:** RF040 será implementado do zero sem base no sistema legado.

**Motivo:**
- Sistema legado não possuía gestão de troncos
- Processos eram 100% manuais e externos ao IControlIT
- Impossibilidade de migração de dados (não há dados a migrar)

**Impacto:** **Alto**
- Requer análise de requisitos completa
- Desenvolvimento full-stack (backend + frontend + integrações)
- Curva de aprendizado para usuários (funcionalidade inédita)

**Benefícios:**
- Liberdade arquitetural (sem débito técnico do legado)
- Aplicação de padrões modernos (Clean Architecture, CQRS, DDD)
- Oportunidade de implementar melhores práticas desde o início

---

### Decisão 2: Integração com PABX via API REST e SNMP

**Descrição:** Implementar integração bidirecional com PABX (Asterisk, FreePBX, Elastix, 3CX) usando protocolos modernos.

**Motivo:**
- Legado não tinha integração automatizada
- Tecnologias modernas (API REST) são mais confiáveis que CLI
- SNMP é padrão de mercado para monitoramento

**Impacto:** **Alto**
- Requer desenvolvimento de adaptadores para múltiplos modelos de PABX
- Necessidade de autenticação segura (API Key + IP Whitelist)
- Testes de integração complexos (ambientes de PABX)

**Riscos Mitigados:**
- Documentação oficial dos PABXs disponível
- Comunidades ativas (Asterisk, FreePBX)
- Possibilidade de sandbox/ambiente de testes

---

### Decisão 3: Priorizar Automação de Failover (<5 segundos)

**Descrição:** Implementar failover completamente automático com SLA de 5 segundos.

**Motivo:**
- Legado requeria intervenção manual (>1 hora de downtime)
- Alta disponibilidade é requisito crítico de negócio
- SLA de 99,9% uptime é padrão de mercado

**Impacto:** **Médio**
- Arquitetura de jobs background (Hangfire) para monitoramento
- SignalR para notificações em tempo real
- Testes de carga para validar performance

**Riscos Mitigados:**
- Hangfire é tecnologia madura e confiável
- SignalR é padrão .NET para tempo real
- Testes automatizados de failover (TC-RF040.yaml)

---

### Decisão 4: Coletar Métricas de QoS e Calcular MOS Score

**Descrição:** Implementar coleta de jitter, latência, packet loss e cálculo de MOS score (E-Model ITU-T G.107).

**Motivo:**
- Legado não coletava métricas de qualidade
- MOS é padrão da indústria (ITU-T G.107)
- Permite tomada de decisão baseada em dados objetivos

**Impacto:** **Médio**
- Integração com PABX/Gateway para coleta de métricas
- Implementação de algoritmo E-Model (complexidade matemática)
- Armazenamento de histórico (90 dias)

**Riscos Mitigados:**
- Algoritmo E-Model é padronizado (documentação ITU-T)
- Bibliotecas open-source disponíveis
- Validação com ferramentas de mercado (Wireshark, VoIP Monitor)

---

## 8. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| **Ausência de conhecimento de usuários** | Alto | Alta | Treinamento completo + documentação + vídeos tutoriais |
| **Resistência à mudança (processos manuais → automatizados)** | Médio | Média | Demonstração de benefícios (ROI, uptime) + período de adaptação |
| **Complexidade de integração com PABX** | Alto | Média | Suporte a múltiplos modelos + ambiente de testes + sandbox |
| **Falta de dados históricos de troncos** | Baixo | Baixa | Cadastro inicial manual + importação de configuração do PABX |
| **Curva de aprendizado de equipe de desenvolvimento** | Médio | Baixa | Documentação técnica detalhada (RF, UC, MD, TC) + PoC inicial |
| **Dependência de sistemas externos (PABX)** | Alto | Baixa | Modo degradado (visualização sem controle) + retry automático |

**Plano de Mitigação Geral:**
1. **Fase 1 (Piloto):** Implantar em 1 empresa com 2-3 troncos
2. **Fase 2 (Expansão):** Expandir para 5 empresas após validação
3. **Fase 3 (Produção):** Rollout completo com suporte dedicado

---

## 9. RASTREABILIDADE

| Elemento Legado | Referência RF | Status |
|-----------------|---------------|--------|
| **Nenhum** | RF040 (funcionalidade nova) | Não aplicável |

**Rastreabilidade Inversa (RF → Processos Manuais):**

| Processo Manual Legado | RF040 - Funcionalidade Correspondente | Ganho |
|------------------------|---------------------------------------|-------|
| Verificação diária de troncos (CLI) | RN-RF040-01 (Monitoramento automático 30s) | 100% automação |
| Failover manual (>1h) | RN-RF040-03 (Failover automático <5s) | 99,86% redução de tempo |
| Planilha Excel de custos | RN-RF040-07 (Custeio automático + rateio) | Eliminação de planilhas |
| Análise manual de logs | RN-RF040-08 (MTBF/MTTR automatizado) | Decisões baseadas em dados |
| Relatórios manuais mensais | RN-RF040-09 (Relatório automático dia 5) | 100% automação |

**Conclusão de Rastreabilidade:**
- **Não há código legado a rastrear** (funcionalidade inexistente)
- **Rastreamento de processos manuais** para demonstrar evolução
- **100% de implementação nova** seguindo padrões modernos

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|--------|------|-----------|-------|
| 1.0 | 2025-12-30 | Documentação da ausência de funcionalidade equivalente no legado - RF040 é 100% nova | Agência ALC - alc.dev.br |
