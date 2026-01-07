# RL-RF111 — Referência ao Legado

**Versão:** 1.0
**Data:** 2025-12-31
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF-111
**Sistema Legado:** IControlIT v1 (ASP.NET Web Forms + VB.NET)
**Objetivo:** Documentar a ausência de implementação de backup/recuperação/DR no sistema legado, justificando a criação greenfield do RF111 moderno.

---

## 1. CONTEXTO DO LEGADO

### 1.1 Arquitetura Geral

- **Arquitetura:** Monolítica Cliente-Servidor
- **Linguagem / Stack:** ASP.NET Web Forms 4.8 + VB.NET + SQL Server
- **Banco de Dados:** SQL Server (múltiplos bancos, um por cliente)
- **Multi-tenant:** Sim (via múltiplos bancos de dados separados)
- **Auditoria:** Parcial (apenas tabelas críticas)
- **Configurações:** Web.config + tabelas de configuração no banco

### 1.2 Estado do Backup no Legado

**AUSÊNCIA TOTAL DE IMPLEMENTAÇÃO FUNCIONAL**

O sistema legado IControlIT v1 **NÃO possui módulo de backup, recuperação ou disaster recovery implementado** dentro da aplicação. As práticas de backup eram:

1. **Backups manuais via SQL Server Management Studio** - DBA executava backups sob demanda
2. **SQL Server Maintenance Plans** - Configurados no nível de SQL Server Agent, não controlados pela aplicação
3. **Scripts .bat agendados no Windows Task Scheduler** - Cópias de arquivos para servidor de rede
4. **Sem interface de gerenciamento** - Nenhuma tela ASPX para backup/restore
5. **Sem auditoria de backups** - Não havia registro de quando backups foram criados ou restaurados
6. **Sem validação de integridade** - Checksum não era calculado ou validado
7. **Sem plano formal de DR** - Recuperação era manual, lenta e sem SLA garantido

### 1.3 Problemas Arquiteturais Identificados

| Problema | Severidade | Impacto |
|----------|------------|---------|
| **Ausência total de módulo de backup** | CRÍTICA | Sem controle centralizado, dependência de DBA, sem rastreabilidade |
| **Multi-database sem consolidação** | ALTA | Cada cliente tinha banco próprio, dificultando backup unificado |
| **Backups sem criptografia** | CRÍTICA | Dados sensíveis sem proteção em trânsito ou repouso |
| **Sem validação de integridade** | ALTA | Risco de restaurar backups corrompidos |
| **Sem política de retenção automática** | MÉDIA | Acumulação indefinida de backups, desperdício de espaço |
| **Dependência de scripts .bat manuais** | ALTA | Frágil, sem tratamento de erro, difícil de auditar |
| **Sem testes de DR** | CRÍTICA | Plano de DR nunca foi testado, risco de falha real |
| **RPO/RTO não definidos** | ALTA | Sem SLA garantido para recuperação |

---

## 2. TELAS DO LEGADO

### 2.1 Telas Relacionadas

**NENHUMA TELA ASPX ENCONTRADA**

Não existem telas ASPX no legado relacionadas a backup, recuperação ou disaster recovery.

**Justificativa da ausência:**
- Backup era responsabilidade da equipe de infraestrutura/DBA
- Não havia demanda de negócio para interface de backup no sistema
- Operações de backup eram consideradas "técnicas" e não "funcionais"

**Consequência:**
- Usuários não tinham visibilidade de backups
- Não era possível agendar backups pela aplicação
- Não era possível restaurar dados sem intervenção de DBA

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

### 3.1 WebServices Relacionados

**NENHUM WEBSERVICE ENCONTRADO**

Não existem webservices (.asmx) no legado relacionados a backup ou DR.

**Justificativa da ausência:**
- Backup não era exposto como funcionalidade da aplicação
- Não havia integrações externas que demandassem backup via API

---

## 4. STORED PROCEDURES LEGADAS

### 4.1 Procedures Relacionadas

**NENHUMA STORED PROCEDURE DE BACKUP ENCONTRADA**

Backups eram executados via comando `BACKUP DATABASE` nativo do SQL Server, não via stored procedures customizadas.

**Evidência:**
```sql
-- Comando executado manualmente pelo DBA (não automatizado)
BACKUP DATABASE [IControlIT_Cliente01]
TO DISK = 'D:\Backups\IControlIT_Cliente01_20251231.bak'
WITH INIT, COMPRESSION;
```

**Características:**
- Executado manualmente ou via Maintenance Plans
- Sem auditoria de execução
- Sem validação de integridade
- Sem criptografia

---

## 5. TABELAS LEGADAS

### 5.1 Tabelas Relacionadas

**NENHUMA TABELA DE BACKUP ENCONTRADA**

O legado não possuía tabelas para rastrear backups, políticas de retenção ou histórico de restaurações.

**Consequência:**
- Sem rastreabilidade de backups
- Sem auditoria de quem/quando executou backup
- Sem histórico de restaurações
- Sem métricas de RPO/RTO

---

## 6. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

### RL-RN-001: Backup Manual Sob Demanda

**Descrição:** DBA executava backups manualmente quando solicitado ou em horários definidos informalmente.

**Localização:** Não estava no código, era processo operacional.

**Justificativa:** Não havia demanda de negócio para backups programados dentro da aplicação.

**Destino:** **SUBSTITUÍDO** por RN-RF111-001 (Backup Completo Diário em Horário de Baixa Demanda)

---

### RL-RN-002: Múltiplos Bancos sem Consolidação

**Descrição:** Cada cliente tinha banco de dados separado, dificultando backup unificado.

**Localização:** Arquitetura multi-database (um banco por cliente).

**Justificativa:** Isolamento de dados entre clientes (multi-tenancy via múltiplos bancos).

**Destino:** **SUBSTITUÍDO** por RN-RF111-011 (Isolamento por Tenant em banco único com Row-Level Security)

---

### RL-RN-003: Retenção Indefinida de Backups

**Descrição:** Backups acumulavam indefinidamente até que espaço em disco ficasse crítico.

**Localização:** Não havia política definida.

**Justificativa:** Falta de planejamento e governança.

**Destino:** **SUBSTITUÍDO** por RN-RF111-003 (Política de Retenção Configurável)

---

### RL-RN-004: Sem Criptografia de Backups

**Descrição:** Backups eram armazenados em texto claro (sem criptografia).

**Localização:** Comando `BACKUP DATABASE` sem opção `WITH ENCRYPTION`.

**Justificativa:** Desconhecimento de requisitos de segurança (LGPD não existia na época).

**Destino:** **SUBSTITUÍDO** por RN-RF111-004 (Criptografia Obrigatória com Chaves Gerenciadas)

---

### RL-RN-005: Sem Validação de Integridade

**Descrição:** Backups não tinham checksum calculado ou validado.

**Localização:** Ausente no processo de backup/restore.

**Justificativa:** Confiança na integridade do SQL Server sem validação adicional.

**Destino:** **SUBSTITUÍDO** por RN-RF111-005 (Validação de Integridade Obrigatória)

---

### RL-RN-006: Sem Plano Formal de DR

**Descrição:** Não havia plano documentado de disaster recovery. Recuperação era manual e ad-hoc.

**Localização:** Ausente.

**Justificativa:** Falta de planejamento e investimento em resiliência.

**Destino:** **SUBSTITUÍDO** por RN-RF111-008 (Failover Automático) e RN-RF111-009 (Teste de DR Obrigatório)

---

## 7. GAP ANALYSIS (LEGADO × RF MODERNO)

### 7.1 Funcionalidades do Legado que NÃO Serão Migradas

| Funcionalidade | Motivo da Remoção |
|----------------|-------------------|
| **Backups manuais via SSMS** | Substituído por backups automáticos programados |
| **Scripts .bat no Task Scheduler** | Substituído por jobs de background gerenciados pela aplicação |
| **Múltiplos bancos por cliente** | Consolidado em banco único com multi-tenancy via Row-Level Security |
| **Ausência de auditoria** | Substituído por auditoria completa obrigatória |

### 7.2 Funcionalidades Novas do Sistema Moderno

| Funcionalidade | Justificativa |
|----------------|---------------|
| **Interface de gerenciamento de backups** | Permite usuários agendar, monitorar e restaurar backups sem DBA |
| **Backup incremental automático** | Garante RPO de 6 horas |
| **Criptografia AES-256 obrigatória** | Conformidade LGPD e segurança de dados |
| **Validação de integridade via checksum** | Previne restauração de dados corrompidos |
| **Política de retenção automática** | Otimiza custos de armazenamento |
| **Point-in-Time Recovery (PITR)** | Restaurar para qualquer momento nos últimos 7 dias |
| **Plano de DR com failover automático** | RTO de 4 horas, failover em < 15 min |
| **Testes trimestrais de DR** | Validação periódica que DR funciona |
| **Monitoramento e alertas** | Notificações de falhas, violações de RPO/RTO |
| **Auditoria completa** | Rastreabilidade de todas as operações |

### 7.3 Mudanças de Comportamento

| Aspecto | Legado | Moderno |
|---------|--------|---------|
| **Execução** | Manual, sob demanda | Automática, programada |
| **Criptografia** | Ausente | Obrigatória (AES-256) |
| **Validação** | Ausente | Checksum SHA-256 obrigatório |
| **Retenção** | Indefinida | Política configurável (7d/4w/12m) |
| **DR** | Sem plano formal | Plano com failover automático |
| **Auditoria** | Ausente | Completa e obrigatória |
| **RPO** | Não definido | 6 horas |
| **RTO** | 24+ horas | 4 horas |

### 7.4 Riscos de Migração

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| **Curva de aprendizado de usuários** | ALTA | MÉDIO | Treinamento obrigatório e documentação completa |
| **Dependência de nova infraestrutura** | MÉDIA | ALTO | Testes extensivos em ambiente de staging |
| **Aumento de custos de storage** | BAIXA | MÉDIO | Política de retenção otimizada |
| **Falha de failover automático** | BAIXA | CRÍTICO | Testes trimestrais obrigatórios |

---

## 8. DECISÕES DE MODERNIZAÇÃO

### Decisão 1: Implementação Greenfield vs Migração

**Descrição:** Implementar módulo de backup completamente do zero (greenfield) em vez de migrar inexistente funcionalidade do legado.

**Motivo:** Legado não possui nenhuma implementação de backup/DR dentro da aplicação. Qualquer solução seria nova.

**Impacto:** ALTO - Requer design completo de arquitetura, mas permite aplicar melhores práticas modernas sem dívida técnica.

---

### Decisão 2: Banco Único com Multi-Tenancy vs Múltiplos Bancos

**Descrição:** Consolidar múltiplos bancos (um por cliente) em banco único com Row-Level Security.

**Motivo:** Facilita backup unificado, reduz complexidade operacional, melhora performance de backups.

**Impacto:** ALTO - Requer migração de dados de múltiplos bancos para único banco. Implementação de Row-Level Security obrigatória.

---

### Decisão 3: Criptografia Obrigatória

**Descrição:** Todos os backups devem ser criptografados com AES-256 antes de armazenamento.

**Motivo:** Conformidade LGPD (Lei Geral de Proteção de Dados), proteção contra vazamento de dados.

**Impacto:** MÉDIO - Requer integração com cofre de chaves (Azure Key Vault ou similar), leve overhead de performance.

---

### Decisão 4: Failover Automático vs Manual

**Descrição:** Implementar failover automático em caso de indisponibilidade de região primária.

**Motivo:** Reduzir RTO de 24+ horas para 4 horas. Minimizar dependência de intervenção humana.

**Impacto:** ALTO - Requer arquitetura multi-região, sincronização de dados, orquestração complexa.

---

### Decisão 5: Testes de DR Obrigatórios

**Descrição:** Executar testes trimestrais de disaster recovery automaticamente.

**Motivo:** Validar que DR não é apenas um plano teórico, mas funciona na prática.

**Impacto:** MÉDIO - Requer ambiente de teste isolado, automação de testes, tempo de execução trimestral.

---

## 9. RASTREABILIDADE

### 9.1 Ausência de Elementos Legado

**Não há itens do legado para rastrear**, pois o RF111 é implementação completamente nova (greenfield).

**Tabela de rastreabilidade vazia:**

| Elemento Legado | Referência RF |
|-----------------|---------------|
| N/A | N/A |

---

## 10. PROBLEMAS LEGADO IDENTIFICADOS

### PROB-RL111-001: Ausência Total de Módulo de Backup

**Severidade:** CRÍTICA

**Descrição:** Sistema legado não possui módulo de backup dentro da aplicação. Backups dependem de processos manuais de DBA.

**Impacto:**
- Sem rastreabilidade de backups
- Sem auditoria de operações
- Sem SLA garantido
- Alto risco de perda de dados

**Solução Moderna:** Implementação completa de módulo de backup com interface de gerenciamento, backups automáticos programados e auditoria obrigatória.

---

### PROB-RL111-002: Múltiplos Bancos de Dados por Cliente

**Severidade:** ALTA

**Descrição:** Arquitetura multi-tenant via múltiplos bancos de dados (um por cliente) dificulta backup unificado.

**Impacto:**
- Backup deve ser executado N vezes (uma por cliente)
- Dificuldade de consolidar backups
- Maior complexidade operacional
- Maior tempo de execução

**Solução Moderna:** Banco único com Row-Level Security (isolamento lógico via TenantId), backup unificado, menor complexidade.

---

### PROB-RL111-003: Backups Sem Criptografia

**Severidade:** CRÍTICA

**Descrição:** Backups armazenados em texto claro, sem criptografia.

**Impacto:**
- Violação de LGPD (dados pessoais sem proteção)
- Risco de vazamento de dados sensíveis
- Dados sensíveis acessíveis se backup for roubado

**Solução Moderna:** Criptografia AES-256 obrigatória com chaves gerenciadas em cofre seguro (Azure Key Vault).

---

### PROB-RL111-004: Ausência de Validação de Integridade

**Severidade:** ALTA

**Descrição:** Backups não têm checksum calculado ou validado.

**Impacto:**
- Risco de restaurar dados corrompidos
- Sem detecção de corrupção em trânsito ou armazenamento
- Piora cenário de falha se backup restaurado estiver corrompido

**Solução Moderna:** Checksum SHA-256 obrigatório calculado na criação e validado antes de restauração.

---

### PROB-RL111-005: Sem Plano Formal de Disaster Recovery

**Severidade:** CRÍTICA

**Descrição:** Não há plano documentado de DR. Recuperação é manual, lenta e sem SLA.

**Impacto:**
- RTO indefinido (pode levar dias)
- RPO indefinido (pode perder dias de dados)
- Sem testes de DR (risco de falha real)
- Dependência de conhecimento tácito de DBAs

**Solução Moderna:** Plano de DR com failover automático, RTO de 4 horas, RPO de 6 horas, testes trimestrais obrigatórios.

---

### PROB-RL111-006: Retenção Indefinida de Backups

**Severidade:** MÉDIA

**Descrição:** Backups acumulam indefinidamente até que espaço em disco fique crítico.

**Impacto:**
- Desperdício de espaço de armazenamento
- Custos crescentes
- Dificuldade de encontrar backups relevantes

**Solução Moderna:** Política de retenção automática configurável (7d daily, 4w weekly, 12m monthly), remoção automática de backups expirados.

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|--------|------|-----------|-------|
| 1.0 | 2025-12-31 | Documentação da ausência de legado para RF111. Implementação greenfield justificada. | Agência ALC - alc.dev.br |

---

**Última Atualização**: 2025-12-31
**Autor**: Agência ALC - alc.dev.br
**Revisão**: Pendente
**RF Relacionado**: RF-111 v2.0
