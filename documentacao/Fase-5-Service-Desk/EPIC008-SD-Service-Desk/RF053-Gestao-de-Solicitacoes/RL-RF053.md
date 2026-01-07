# RL-RF053 — Referência ao Legado

**Versão:** 1.0
**Data:** 2025-12-30
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF053 - Gestão de Solicitações
**Sistema Legado:** Não aplicável (RF novo, sem equivalente legado)
**Objetivo:** Documentar ausência de legado e registrar que RF053 é funcionalidade nova sem migração.

---

## 1. CONTEXTO DO LEGADO

**IMPORTANTE:** RF053 - Gestão de Solicitações é uma **funcionalidade completamente nova** no sistema IControlIT modernizado. Não existe equivalente no sistema legado VB.NET + ASP.NET Web Forms.

### Razões para ausência de legado:

1. **Escopo Expandido**: O sistema legado não possuía módulo estruturado de service desk interno
2. **Funcionalidade Nova**: Workflow de aprovação multi-nível, SLA automático, chat interno e aprovação mobile são inovações
3. **Modernização Completa**: Requisito criado do zero com base em melhores práticas modernas

### Informações do Sistema Legado Geral:

- **Arquitetura**: Monolítica WebForms
- **Linguagem / Stack**: VB.NET, ASP.NET Web Forms 4.8
- **Banco de Dados**: SQL Server 2016
- **Multi-tenant**: Não (isolamento manual via queries)
- **Auditoria**: Parcial (apenas tabelas críticas)
- **Configurações**: Web.config e tabelas parametrizadas

---

## 2. TELAS DO LEGADO

### AUSÊNCIA DE TELAS EQUIVALENTES

Não existem telas no legado que correspondam ao RF053. O sistema legado **não possuía**:

- Portal de abertura de solicitações
- Workflow de aprovação configurável
- Dashboard de solicitações em tempo real
- Chat interno por solicitação
- Pesquisa de satisfação automática

### Possíveis Funcionalidades Parciais (Não Documentadas):

Embora não haja um módulo de "Gestão de Solicitações", é possível que existam:

1. **Formulários Ad-Hoc**: Páginas ASPX isoladas para solicitação de ativos específicos (celular, notebook)
   - **Status**: Não mapeado (não localizado no código legado disponível)
   - **Destino**: Substituído pelo RF053 completo

2. **E-mails Manuais**: Processo via e-mail direto para TI (não sistematizado)
   - **Status**: Processo manual, sem código
   - **Destino**: Substituído pelo portal self-service

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

### AUSÊNCIA DE WEBSERVICES EQUIVALENTES

Não foram identificados WebServices (.asmx) ou APIs (.ashx) no sistema legado relacionados a gestão de solicitações.

| Método | Local | Responsabilidade | Observações |
|--------|-------|------------------|-------------|
| N/A | - | - | Nenhum serviço legado identificado |

---

## 4. TABELAS LEGADAS

### AUSÊNCIA DE TABELAS EQUIVALENTES

Não existem tabelas no banco de dados legado que armazenem solicitações estruturadas.

| Tabela | Finalidade | Problemas Identificados |
|--------|------------|-------------------------|
| N/A | - | Nenhuma tabela legada identificada |

### Possível Rastreamento Manual:

É possível que solicitações fossem rastreadas em:

1. **Planilhas Excel**: Controle manual de solicitações por equipe de TI (fora do sistema)
2. **E-mails**: Histórico em caixas de e-mail (não sistematizado)
3. **Tabelas de Auditoria Genéricas**: Logs de ações sem estrutura específica

**Destino**: Todos substituídos pelo modelo de dados completo do RF053

---

## 5. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

### AUSÊNCIA DE REGRAS FORMALIZADAS

Não há regras de negócio documentadas no legado para gestão de solicitações, pois a funcionalidade não existia.

**Possíveis regras informais (não sistematizadas):**

- **RL-RN-001**: Solicitações de celular exigem aprovação do gestor (processo manual via e-mail)
  - **Destino**: Assumido e formalizado em RN-RF053-03 (Workflow de Aprovação Multi-Nível)

- **RL-RN-002**: Prazo informal de atendimento de 5 dias úteis (não monitorado)
  - **Destino**: Assumido e formalizado em RN-RF053-04 (SLA Automático com Pausas)

- **RL-RN-003**: Solicitações de alto valor (> R$ 5.000) requerem aprovação da diretoria (processo manual)
  - **Destino**: Assumido e formalizado em RN-RF053-03 (Workflow configurável por valor)

---

## 6. GAP ANALYSIS (LEGADO x RF MODERNO)

| Item | Legado | RF Moderno | Observação |
|------|--------|------------|------------|
| **Abertura de Solicitações** | E-mail manual | Portal self-service com formulário dinâmico | Novo |
| **Workflow de Aprovação** | E-mail manual, sem rastreio | Multi-nível configurável, auditado | Novo |
| **SLA** | Informal (5 dias), sem alertas | Automático com pausas, alertas proativos | Novo |
| **Atribuição** | Manual (gestor TI) | Automática ou manual com rastreio | Novo |
| **Chat Interno** | Não existia | Chat integrado à solicitação | Novo |
| **Anexos** | Anexos de e-mail | Upload validado (tipo, tamanho, vírus) | Novo |
| **Aprovação Mobile** | Não existia | App mobile com notificação push | Novo |
| **Delegação** | Não existia | Delegação temporária de aprovadores | Novo |
| **Pesquisa de Satisfação** | Não existia | NPS automático ao fechar solicitação | Novo |
| **Dashboard** | Não existia | Tempo real via SignalR | Novo |
| **Relatórios** | Não existia | Excel/PDF com filtros configuráveis | Novo |
| **Auditoria** | Não existia | Completa (7 anos - LGPD) | Novo |

**Conclusão**: RF053 é 100% novo, sem migração de legado.

---

## 7. DECISÕES DE MODERNIZAÇÃO

### Decisão 01: Criar Funcionalidade Nova do Zero

- **Descrição**: Não tentar adaptar processos manuais legados, criar sistema moderno completo
- **Motivo**:
  - Processos manuais via e-mail são ineficientes e não rastreáveis
  - Necessidade de workflow configurável e SLA automático
  - Oportunidade de implementar melhores práticas (SignalR, chat, mobile)
- **Impacto**: Alto (funcionalidade completamente nova, requer treinamento de usuários)
- **Data**: 2025-01-14

### Decisão 02: Implementar Workflow Configurável

- **Descrição**: Não hardcodar fluxos de aprovação, permitir configuração por tipo/valor
- **Motivo**: Flexibilidade para diferentes tipos de solicitação e mudanças futuras
- **Impacto**: Médio (complexidade adicional no backend)
- **Data**: 2025-01-14

### Decisão 03: SLA com Pausas Automáticas

- **Descrição**: Implementar pausas automáticas de SLA em pendências externas
- **Motivo**: Evitar penalizar equipe de TI por fatores fora de controle
- **Impacto**: Médio (requer job Hangfire e lógica de pausa/retomada)
- **Data**: 2025-01-14

### Decisão 04: Aprovação Mobile Nativa

- **Descrição**: Suporte a aprovação via app mobile com notificação push
- **Motivo**: Agilizar aprovações de gestores em viagem/ausentes
- **Impacto**: Alto (requer desenvolvimento de app mobile ou PWA)
- **Data**: 2025-01-14

---

## 8. RISCOS DE MIGRAÇÃO

### IMPORTANTE: Não há migração de dados legados

Como RF053 é funcionalidade nova, **não há riscos de migração de dados**. No entanto, há riscos de **adoção**:

| Risco | Impacto | Mitigação |
|-------|---------|-----------|
| **Resistência de Usuários** | Alto | Treinamento obrigatório, documentação clara, suporte dedicado |
| **Processo manual ignorado** | Médio | Comunicação interna, desabilitar e-mails manuais após go-live |
| **Sobrecarga inicial de solicitações** | Médio | Lançamento gradual (piloto → geral), capacidade de atendimento adequada |
| **Configuração incorreta de workflows** | Alto | Validação de configurações antes de go-live, testes com cenários reais |
| **Falta de integração com gestão de ativos** | Médio | Garantir RF025 (Gestão de Ativos) implementado antes de RF053 |

---

## 9. RASTREABILIDADE

### AUSÊNCIA DE ELEMENTOS LEGADOS

Não há elementos legados para rastrear, pois RF053 é funcionalidade nova.

| Elemento Legado | Referência RF |
|-----------------|---------------|
| N/A | RF053 é funcionalidade nova |

### Dependências de Outros RFs:

RF053 **depende** de:

- **RF025 - Gestão de Ativos**: Integração para criação automática de ativo no inventário (RN-RF053-10)
- **RF001 - Autenticação e Autorização**: RBAC para permissões de solicitações
- **RF002 - Multi-Tenancy**: Isolamento de solicitações por empresa
- **RF003 - Auditoria**: Registro de operações com retenção de 7 anos

---

## 10. NOTAS ADICIONAIS

### Pesquisa no Código Legado

Foi realizada busca no repositório `D:\IC2\ic1_legado\IControlIT\` pelos seguintes termos:

- "solicitação" / "solicitacao"
- "service desk"
- "chamado"
- "ticket"
- "aprovação" / "aprovacao"

**Resultado**: Nenhuma tela, classe ou tabela relacionada foi encontrada.

### Conclusão Final

RF053 - Gestão de Solicitações é uma **funcionalidade 100% nova** sem equivalente no sistema legado. Todas as 15 regras de negócio (RN-RF053-01 a RN-RF053-15) foram criadas com base em:

1. Melhores práticas de ITSM (IT Service Management)
2. Benchmarking com ferramentas de mercado (ServiceNow, Jira Service Desk)
3. Requisitos de negócio levantados com stakeholders
4. Padrões modernos de UX e aprovação mobile

**Não há migração de dados, não há legado a ser substituído, não há código a ser refatorado.**

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|--------|------|-----------|-------|
| 1.0 | 2025-12-30 | Documentação de ausência de legado para RF053 | Agência ALC - alc.dev.br |
