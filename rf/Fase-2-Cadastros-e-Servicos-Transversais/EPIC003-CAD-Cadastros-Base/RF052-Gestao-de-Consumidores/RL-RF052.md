# RL-RF052 — Referência ao Legado (Gestão de Consumidores)

**Versão:** 1.0
**Data:** 2025-12-30
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF-052
**Sistema Legado:** VB.NET + ASP.NET Web Forms
**Objetivo:** Documentar o comportamento do legado relacionado à gestão de consumidores/usuários, servindo de base para a refatoração e garantindo rastreabilidade histórica.

---

## 1. CONTEXTO DO LEGADO

O sistema legado IControlIT gerenciava consumidores de telecomunicações através de funcionalidades distribuídas em múltiplas telas ASPX, stored procedures SQL Server e webservices VB.NET.

- **Arquitetura:** Monolítica Web Forms (ASP.NET 4.x)
- **Linguagem / Stack:** VB.NET, ASP.NET Web Forms, SQL Server 2014+
- **Banco de Dados:** SQL Server (múltiplos bancos por cliente, sem multi-tenancy unificado)
- **Multi-tenant:** Parcial (bancos separados por cliente, sem Row-Level Security)
- **Auditoria:** Parcial (algumas operações logadas em tabelas de auditoria, outras sem registro)
- **Configurações:** Web.config (connection strings, appSettings), Banco de Dados (tabelas de configuração)

**Problemas Arquiteturais Identificados:**
- Ausência de multi-tenancy unificado (cada cliente = 1 banco SQL Server)
- Regras de negócio espalhadas entre code-behind, stored procedures e webservices
- Falta de padronização de nomenclatura (tabelas como `Usuario`, `Usuario_Linha`, `Usuario_Aparelho`)
- Auditoria inconsistente (algumas operações sem log)
- Validações duplicadas (frontend + stored procedures, sem camada única)
- Soft delete não padronizado (algumas tabelas com `Ativo` bit, outras sem exclusão lógica)
- Hierarquia organizacional fraca (vínculos departamento/cargo inconsistentes)

---

## 2. TELAS DO LEGADO

### Tela: Usuario.aspx

- **Caminho:** `ic1_legado/IControlIT/Cadastros/Usuario.aspx`
- **Responsabilidade:** CRUD básico de consumidores (chamados de "usuários" no legado)

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|------|------|-------------|-------------|
| Nome | TextBox | Sim | Validação apenas no submit (postback) |
| CPF | TextBox | Sim para Funcionário | Validação de formato via JavaScript |
| Matricula | TextBox | Sim para Funcionário | Sem validação de unicidade no frontend |
| Email | TextBox | Não | Validação de formato via RegEx no code-behind |
| Departamento | DropDownList | Sim | Carregado via webservice |
| Cargo | DropDownList | Não | Carregado via webservice |
| Status | DropDownList | Sim | Valores: Ativo, Inativo, Bloqueado |
| TipoUsuario | DropDownList | Sim | Valores: Funcionário, Prestador, Visitante |

#### Comportamentos Implícitos

- CPF validado apenas no frontend (JavaScript), backend aceitava CPF inválido
- Matrícula sem validação de unicidade (permitia duplicatas até stored procedure rejeitar)
- E-mail sem validação de unicidade (permitia múltiplos usuários com mesmo e-mail)
- Mudança de Departamento não gerava histórico (registro sobrescrito)
- Inativação não implementava soft delete consistente (campo `Ativo` bit, mas sem auditoria)
- Alocação de linhas/aparelhos feita em telas separadas (sem wizards de onboarding)
- Sem workflow de admissão/demissão (operações manuais)

**Destino:** SUBSTITUÍDO

**Justificativa:** Funcionalidade central do RF052 redesenhada com arquitetura moderna (CQRS, Clean Architecture), validações consistentes em todos os layers, auditoria completa, workflows automatizados de onboarding/offboarding e dashboard 360°.

---

### Tela: UsuarioLinha.aspx

- **Caminho:** `ic1_legado/IControlIT/Cadastros/UsuarioLinha.aspx`
- **Responsabilidade:** Associar linhas móveis a usuários (consumidores)

#### Comportamentos Implícitos

- Associação de linha criava registro na tabela `Usuario_Linha` com data de início
- Desassociação atualizava campo `DataFim` (implementação correta de histórico)
- Não validava se linha já estava alocada a outro usuário (permitia duplicação)
- Custo da linha não era calculado automaticamente (job separado, batch noturno)
- Sem notificação ao gestor quando linha era alocada/desalocada

**Destino:** SUBSTITUÍDO

**Justificativa:** Substituído por endpoints REST `/api/gestao/consumidores/{id}/alocar-ativo` e `/api/gestao/consumidores/{id}/desalocar-ativo` com validações de disponibilidade, auditoria completa e notificações automáticas.

---

### Tela: UsuarioAparelho.aspx

- **Caminho:** `ic1_legado/IControlIT/Cadastros/UsuarioAparelho.aspx`
- **Responsabilidade:** Associar aparelhos (smartphones, tablets) a usuários

#### Comportamentos Implícitos

- Permitia associar múltiplos aparelhos ao mesmo usuário
- Sem validação de disponibilidade (aparelho podia estar alocado a múltiplos usuários)
- Histórico de alocações registrado na tabela `Usuario_Aparelho_Historico`
- Custo de depreciação do aparelho não considerado no custo total do usuário
- Devolução de aparelho não validava estado do aparelho (quebrado, danificado)

**Destino:** SUBSTITUÍDO

**Justificativa:** Substituído por endpoints unificados de alocação de ativos (linhas, ramais, aparelhos) com validação de disponibilidade, cálculo automático de custos e integração com controle de inventário (RF025).

---

### Tela: UsuarioCusto.aspx

- **Caminho:** `ic1_legado/IControlIT/Relatorios/UsuarioCusto.aspx`
- **Responsabilidade:** Exibir custos mensais por usuário

#### Comportamentos Implícitos

- Relatório gerado via stored procedure `sp_CalculaCustoUsuario`
- Dados pré-calculados em tabela `Usuario_Custo_Mensal` (job noturno)
- Histórico de apenas 12 meses (limitação de armazenamento)
- Sem comparação com média do departamento
- Exportação apenas para Excel (via componente terceiro `EPPlus`)

**Destino:** SUBSTITUÍDO

**Justificativa:** Substituído por dashboard 360° (RF052 - RN11) com histórico de 7 anos (LGPD), comparação com média departamental, gráficos interativos (ApexCharts) e múltiplos formatos de exportação (Excel, PDF, CSV).

---

### Tela: UsuarioMovimentacao.aspx

- **Caminho:** `ic1_legado/IControlIT/RH/UsuarioMovimentacao.aspx`
- **Responsabilidade:** Registrar mudanças de departamento/cargo

#### Comportamentos Implícitos

- Mudança de departamento registrada na tabela `Usuario_Movimentacao` com data e motivo
- Mudança de cargo NÃO registrava histórico (campo sobrescrito diretamente)
- Movimentação não disparava atualização automática de políticas
- Sem workflow de aprovação (qualquer RH podia movimentar sem alçada)
- Relatório de movimentações disponível apenas para Super Admin

**Destino:** SUBSTITUÍDO

**Justificativa:** Substituído por sistema de histórico completo (RF052 - RN13) que registra todas as movimentações (departamento, cargo, gestor, centro de custo) com auditoria, aplicação automática de políticas e workflows de aprovação.

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

| Método | Local | Responsabilidade | Observações | Destino |
|------|-------|------------------|-------------|---------|
| `GetUsuarios()` | `UsuarioService.asmx` | Listar todos os usuários | Sem paginação, retornava todos os registros (performance ruim para >1000 usuários) | SUBSTITUÍDO |
| `GetUsuarioById(int id)` | `UsuarioService.asmx` | Obter usuário por ID | Retornava objeto complexo com linhas, aparelhos, custos (N+1 query problem) | SUBSTITUÍDO |
| `CreateUsuario(UsuarioDto dto)` | `UsuarioService.asmx` | Criar usuário | Validações básicas, sem workflow de onboarding | SUBSTITUÍDO |
| `UpdateUsuario(UsuarioDto dto)` | `UsuarioService.asmx` | Atualizar usuário | Sem histórico de alterações, sem auditoria de campos modificados | SUBSTITUÍDO |
| `InativarUsuario(int id)` | `UsuarioService.asmx` | Inativar usuário | Soft delete simples (campo `Ativo = 0`), sem workflow de offboarding | SUBSTITUÍDO |
| `AlocarLinha(int usuarioId, int linhaId)` | `UsuarioService.asmx` | Alocar linha a usuário | Sem validação de disponibilidade da linha | SUBSTITUÍDO |
| `DesalocarLinha(int usuarioId, int linhaId)` | `UsuarioService.asmx` | Desalocar linha | Registrava `DataFim`, mas não calculava custos proporcionais | SUBSTITUÍDO |
| `CalcularCustoMensal(int usuarioId)` | `UsuarioService.asmx` | Calcular custo mensal | Cálculo síncrono (lento), sem cache | SUBSTITUÍDO |

**Justificativa de Substituição (Webservices):**
Todos os webservices ASMX foram substituídos por API REST com:
- Paginação obrigatória (performance)
- DTOs otimizados (sem N+1 queries)
- Workflows automatizados (onboarding/offboarding via Hangfire)
- Auditoria completa (RF003)
- Cálculos assíncronos (jobs background)
- Cache inteligente (1 hora para relatórios)

---

## 4. TABELAS LEGADAS

| Tabela | Finalidade | Problemas Identificados | Destino |
|-------|------------|-------------------------|---------|
| `Usuario` | Cadastro principal de usuários/consumidores | Sem campos de auditoria (`Created`, `CreatedBy`), sem multi-tenancy (`ConglomeradoId`), sem soft delete consistente | SUBSTITUÍDO |
| `Usuario_Linha` | Associação usuário-linha móvel | Sem validação de unicidade (permitia múltiplas alocações da mesma linha), sem campo `ConglomeradoId` | SUBSTITUÍDO |
| `Usuario_Aparelho` | Associação usuário-aparelho | Histórico em tabela separada (complexidade desnecessária), sem soft delete | SUBSTITUÍDO |
| `Usuario_Custo_Mensal` | Custos mensais pré-calculados | Retenção de apenas 12 meses (insuficiente para LGPD - 7 anos), sem criptografia | SUBSTITUÍDO |
| `Usuario_Movimentacao` | Histórico de movimentações | Apenas departamento (cargo sem histórico), sem campo `Justificativa` | SUBSTITUÍDO |
| `Usuario_Perfil` | Perfis de uso (Executivo, Colaborador, etc.) | Tabela de domínio hard-coded (sem flexibilidade), sem vínculo com políticas | SUBSTITUÍDO |

**Problemas Comuns:**
- Ausência de `ConglomeradoId` (multi-tenancy)
- Ausência de campos de auditoria (`CreatedBy`, `Created`, `LastModifiedBy`, `LastModified`)
- Soft delete inconsistente (algumas tabelas com `Ativo` bit, outras sem)
- Nomes inconsistentes (algumas `Usuario_X`, outras `UsuarioX`)
- Relacionamentos sem Foreign Keys (integridade referencial fraca)

---

## 5. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

### RL-RN-001: Validação de CPF apenas no Frontend

**Descrição:** CPF era validado apenas via JavaScript no navegador. Backend (stored procedures) aceitava CPF inválido.

**Fonte:** `Usuario.aspx` (JavaScript inline), `sp_InserirUsuario` (sem validação)

**Destino:** SUBSTITUÍDO

**Justificativa:** RF052 implementa validação de CPF em todos os layers (frontend, backend/Command, banco de dados via FluentValidation).

---

### RL-RN-002: Cálculo de Custo Mensal via Job Noturno

**Descrição:** Custos mensais eram calculados por job batch que rodava às 3h da manhã, somando custos de linhas, aparelhos e consumo variável. Dados armazenados em `Usuario_Custo_Mensal`.

**Fonte:** Job SQL Server Agent `Job_CalcularCustoUsuarios`, stored procedure `sp_CalculaCustoMensal`

**Destino:** ASSUMIDO

**Justificativa:** RF052 mantém estratégia de cálculo via job mensal (Hangfire) mas com melhorias: histórico de 7 anos, criptografia de dados sensíveis, auditoria completa.

---

### RL-RN-003: Mudança de Departamento sem Atualização Automática de Políticas

**Descrição:** Quando usuário mudava de departamento, políticas aplicadas NÃO eram atualizadas automaticamente. Gestores precisavam manualmente reconfigurar políticas.

**Fonte:** `UsuarioMovimentacao.aspx` (code-behind VB.NET), sem integração com sistema de políticas

**Destino:** SUBSTITUÍDO

**Justificativa:** RF052 implementa aplicação automática de políticas baseadas em perfil de uso (RN-RF052-06) e departamento, com Domain Events disparando reavaliação de políticas ao mudar departamento.

---

### RL-RN-004: Inativação de Usuário não Desalocava Ativos

**Descrição:** Ao inativar usuário (campo `Ativo = 0`), linhas e aparelhos alocados NÃO eram automaticamente desalocados. Gestor precisava manualmente desalocar antes de inativar.

**Fonte:** `Usuario.aspx` (botão Inativar), `sp_InativarUsuario` (UPDATE Usuario SET Ativo = 0)

**Destino:** SUBSTITUÍDO

**Justificativa:** RF052 implementa workflow de offboarding (RN-RF052-09) que automatiza desalocação de ativos, cancelamento de acessos e cálculo de custos finais antes de inativar.

---

### RL-RN-005: Matrícula sem Validação de Unicidade

**Descrição:** Matrícula de funcionário não tinha validação de unicidade no frontend. Stored procedure `sp_InserirUsuario` possuía constraint UNIQUE que gerava erro genérico ao tentar inserir matrícula duplicada.

**Fonte:** `Usuario.aspx` (sem validação), `Usuario` table (UNIQUE constraint `UK_Usuario_Matricula`)

**Destino:** SUBSTITUÍDO

**Justificativa:** RF052 valida unicidade de matrícula em todos os layers (frontend com mensagem clara, backend com FluentValidation customizada, banco com UNIQUE constraint).

---

### RL-RN-006: Relatório de Custos sem Comparação com Média Departamental

**Descrição:** Relatório de custos (`UsuarioCusto.aspx`) exibia apenas custos absolutos por usuário. Não havia comparação com média do departamento ou identificação de outliers.

**Fonte:** `UsuarioCusto.aspx`, stored procedure `sp_RelatorioCustoUsuario`

**Destino:** SUBSTITUÍDO

**Justificativa:** RF052 implementa comparação automática de consumo individual vs média departamental (RN-RF052-12) com alertas para gestores quando usuário excede 150% da média por 3 meses.

---

### RL-RN-007: Ausência de Workflow de Onboarding

**Descrição:** Admissão de novo funcionário era manual em múltiplas telas: criar usuário, alocar linha, alocar aparelho, configurar perfil, enviar e-mail de boas-vindas. Sem workflow automatizado ou checklist.

**Fonte:** Processo manual descrito em `Manual_Procedimentos_RH.docx`

**Destino:** SUBSTITUÍDO

**Justificativa:** RF052 implementa workflow de onboarding automatizado em 6 etapas (RN-RF052-08) com aprovações, notificações e execução via Hangfire.

---

### RL-RN-008: Ausência de Integração com Sistema de RH

**Descrição:** Dados de funcionários (admissões, demissões, mudanças de departamento) eram informados manualmente pelo RH no IControlIT. Sem sincronização automática com sistema de RH corporativo.

**Fonte:** Processo manual sem evidências em código

**Destino:** SUBSTITUÍDO

**Justificativa:** RF052 implementa integração automática com sistema de RH (RN-RF052-10) via API REST ou importação de arquivo CSV com sincronização diária.

---

### RL-RN-009: Histórico de Custos Limitado a 12 Meses

**Descrição:** Tabela `Usuario_Custo_Mensal` mantinha apenas 12 meses de histórico. Dados mais antigos eram purgados por job de limpeza.

**Fonte:** Job SQL Server Agent `Job_LimparHistoricoAntigo`, stored procedure `sp_PurgarCustosAntigos`

**Destino:** SUBSTITUÍDO

**Justificativa:** RF052 mantém histórico de 7 anos (conformidade LGPD) com particionamento de tabela por ano para otimização de performance.

---

### RL-RN-010: Perfis de Uso Hard-coded

**Descrição:** Perfis de uso (Executivo, Gerente, Colaborador, Estagiário) estavam hard-coded em tabela `Usuario_Perfil` sem vínculo com políticas de consumo. Mudança de perfil não aplicava políticas automaticamente.

**Fonte:** Tabela `Usuario_Perfil`, sem stored procedures de aplicação de políticas

**Destino:** SUBSTITUÍDO

**Justificativa:** RF052 implementa perfis de uso vinculados a políticas (RF049) com aplicação automática via Domain Events ao criar/atualizar consumidor (RN-RF052-06).

---

## 6. GAP ANALYSIS (LEGADO x RF MODERNO)

| Item | Legado | RF Moderno | Observação |
|-----|--------|------------|------------|
| Multi-tenancy | Bancos separados por cliente | Row-Level Security unificado (`ConglomeradoId`) | Redução de custos de infraestrutura |
| Auditoria | Parcial (algumas operações) | Completa (todas as operações via RF003) | Conformidade e rastreabilidade |
| Soft Delete | Inconsistente (campo `Ativo` em algumas tabelas) | Padronizado (`Deleted`, `DeletedBy`, `DeletedAt`) | Recuperação de dados, LGPD |
| Validações | Duplicadas (frontend JS + stored procedures) | Camada única (FluentValidation no backend) | Manutenibilidade |
| Workflow Onboarding | Manual (múltiplas telas) | Automatizado (6 etapas via Hangfire) | Eficiência, redução de erros |
| Workflow Offboarding | Manual | Automatizado (5 etapas via Hangfire) | Conformidade, recuperação de ativos |
| Integração RH | Inexistente (entrada manual) | Sincronização diária (API/CSV) | Redução de retrabalho, dados atualizados |
| Dashboard 360° | Inexistente (dados em múltiplas telas) | Completo (7 abas, tempo real via SignalR) | Experiência do usuário |
| Comparação com Média | Inexistente | Implementado (individual vs departamento) | Identificação de outliers |
| Histórico de Custos | 12 meses | 7 anos (LGPD) | Conformidade legal |
| Perfis de Uso | Hard-coded, sem vínculo com políticas | Dinâmico, vínculo com RF049 | Flexibilidade, automação |
| Alocação de Ativos | Telas separadas (linha, aparelho) | Endpoint unificado | Experiência do usuário |
| Relatórios | Apenas Excel (EPPlus) | Excel, PDF, CSV | Flexibilidade |
| Performance | Queries sem paginação, N+1 problems | Paginação obrigatória, DTOs otimizados | Escalabilidade |

---

## 7. DECISÕES DE MODERNIZAÇÃO

### Decisão: Migração de Bancos Separados para Multi-tenancy Unificado

**Motivo:** Reduzir custos de infraestrutura (múltiplos SQL Servers) e facilitar manutenção (1 schema único vs N schemas).

**Impacto:** Alto (requer migração de dados de múltiplos bancos SQL Server para banco unificado com campo `ConglomeradoId`).

---

### Decisão: Workflows de Onboarding/Offboarding Automatizados

**Motivo:** Eliminar processos manuais propensos a erros, garantir que todos os novos consumidores sejam configurados corretamente com acessos, ativos e políticas.

**Impacto:** Médio (requer desenvolvimento de workflows via Hangfire, integração com RF066/RF067 para notificações).

---

### Decisão: Integração Automática com Sistema de RH

**Motivo:** Evitar dessincronia entre RH corporativo e sistema de telecomunicações, garantir que admissões/demissões sejam refletidas automaticamente.

**Impacto:** Alto (requer integração com API externa ou implementação de importador de arquivos CSV, mapeamento de campos).

---

### Decisão: Dashboard 360° com Abas

**Motivo:** Melhorar experiência do usuário eliminando navegação por múltiplas telas (legado tinha 5+ telas para ver dados completos de um consumidor).

**Impacto:** Médio (requer desenvolvimento de componente Angular complexo, integração com múltiplos endpoints backend).

---

### Decisão: Histórico de Custos de 7 Anos

**Motivo:** Conformidade com LGPD (retenção obrigatória de dados de contratos e faturamento por 7 anos).

**Impacto:** Médio (requer particionamento de tabela `ConsumidorCustoMensal` por ano, ajuste de queries para performance).

---

## 8. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Probabilidade | Mitigação |
|------|---------|---------------|-----------|
| Perda de dados durante migração multi-database → unificado | Alto | Média | Backup completo antes de migração, script de validação pós-migração, rollback plan |
| Quebra de integrações com sistemas externos (RH, ERP) | Alto | Alta | Mapeamento detalhado de integrações legado, testes de integração antes de go-live |
| Curva de aprendizado de workflows automatizados | Médio | Alta | Treinamento para gestores/RH, documentação detalhada, suporte dedicado pós-go-live |
| Performance de queries em tabela unificada (todos os clientes) | Alto | Média | Índices otimizados, particionamento, Query Filters EF Core com `ConglomeradoId` |
| Resistência de usuários acostumados com telas legado | Médio | Alta | Change management, demonstrações de benefícios (dashboard 360°, workflows), período de convivência |

---

## 9. RASTREABILIDADE

| Elemento Legado | Referência RF Moderno |
|----------------|---------------|
| `Usuario.aspx` | RF052 - RN01 a RN15, UC01-criar-consumidor, UC02-visualizar-consumidor, UC03-editar-consumidor |
| `UsuarioLinha.aspx` | RF052 - RN04 (Alocação de Ativos), UC05-alocar-ativo |
| `UsuarioAparelho.aspx` | RF052 - RN04 (Alocação de Ativos), UC05-alocar-ativo |
| `UsuarioCusto.aspx` | RF052 - RN05 (Controle de Custos), RN12 (Comparação), RN14 (Relatórios), UC09-dashboard-360 |
| `UsuarioMovimentacao.aspx` | RF052 - RN13 (Movimentação com Histórico) |
| `UsuarioService.asmx` | RF052 - Endpoints REST `/api/gestao/consumidores/*` |
| Tabela `Usuario` | RF052 - Entidade `Consumidor` (backend/Domain/Entities/Gestao/Consumidor.cs) |
| Tabela `Usuario_Custo_Mensal` | RF052 - Entidade `ConsumidorCustoMensal` |
| Tabela `Usuario_Movimentacao` | RF052 - Entidade `ConsumidorHistoricoMovimentacao` |
| Job `Job_CalcularCustoUsuarios` | RF052 - Hangfire Job `CalcularCustosMensaisConsumidoresJob` |

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|------|------|----------|------|
| 1.0 | 2025-12-30 | Documentação inicial de referência ao legado IControlIT (Gestão de Consumidores) | Agência ALC - alc.dev.br |
