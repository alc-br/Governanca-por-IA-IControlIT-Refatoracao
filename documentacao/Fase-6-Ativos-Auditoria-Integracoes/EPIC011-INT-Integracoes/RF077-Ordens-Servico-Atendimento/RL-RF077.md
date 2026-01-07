# RL-RF077 — Referência ao Legado: Ordens de Serviço e Atendimento

**Versão:** 1.0
**Data:** 2025-01-14
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF-077
**Sistema Legado:** IControlIT VB.NET (ASP.NET Web Forms)
**Objetivo:** Documentar o comportamento do sistema legado de ordens de serviço que serve de base para a modernização, garantindo rastreabilidade, entendimento histórico e mitigação de riscos de migração.

---

## 1. CONTEXTO DO LEGADO

### Arquitetura Geral

- **Arquitetura:** Monolítica baseada em ASP.NET Web Forms (VB.NET)
- **Linguagem / Stack:** VB.NET + ASP.NET 4.7.2 + SQL Server
- **Banco de Dados:** SQL Server 2016+ (multi-database por cliente)
- **Multi-tenant:** Parcial (bancos separados por cliente: `SC_<OPERADORA>_<CLIENTE>`)
- **Auditoria:** Parcial (campos `Id_Usuario_Criacao`, `Dt_Ultima_Atualizacao`, sem histórico completo)
- **Configurações:** Web.config com connection strings criptografadas

### Stack Tecnológica Legado

- **Backend:** ASP.NET Web Forms com code-behind VB.NET
- **Webservices:** SOAP (.asmx) - `WSOrdensSevico.asmx.vb`
- **Banco:** SQL Server com stored procedures (`pa_*`, `sp_*`)
- **Frontend:** Controles ASP.NET (DataGrid, DropDownList, TextBox)
- **JavaScript:** jQuery 3.5.1 para validações client-side básicas

### Problemas Arquiteturais Identificados

1. **Sem Assinatura Digital:** Sistema legado não possui captura de assinatura, apenas checkbox manual
2. **Validação EXIF Ausente:** Fotos são aceitas sem validação de metadados (data de captura inexistente)
3. **Agendamento Manual:** Não verifica conflitos de técnico automaticamente
4. **Checklist Estático:** HTML hard-coded em telas, não baseado em tipo de OS
5. **Rastreamento de Tempo Impreciso:** Registros manuais sem timer automático
6. **Auditoria Incompleta:** Apenas campos básicos (`Usuario_Criacao`, `Dt_Atualizacao`), sem histórico de mudanças
7. **Multi-tenancy Fraco:** Isolamento por banco, não por ClienteId em tabelas

---

## 2. TELAS DO LEGADO

### Tela: OrdensSevico.aspx

- **Caminho:** `ic1_legado/IControlIT/[Modulo]/OrdensSevico.aspx`
- **Responsabilidade:** Listagem de ordens de serviço com filtros por status, técnico e data

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| Filtro Status | DropDownList | Não | Valores: "Todos", "Rascunho", "Pendente", "Aprovada", "Agendada", "Em Execução", "Concluída", "Cancelada" |
| Filtro Técnico | DropDownList | Não | Carregado de `tblUsuarios` |
| Filtro Data Início | TextBox (DatePicker) | Não | Formato dd/MM/yyyy |
| Filtro Data Fim | TextBox (DatePicker) | Não | Formato dd/MM/yyyy |
| Grid Resultados | DataGrid | - | Colunas: ID, Tipo, Ativo, Status, Técnico, Data Agendada, Ações |

#### Comportamentos Implícitos

- Paginação manual via ViewState (performance ruim com >1000 registros)
- Filtro de data usa stored procedure que não valida range máximo (pode travar com grandes períodos)
- Ações (Editar, Visualizar) abrem popup modal com JavaScript
- Sem validação de permissão por status (qualquer usuário pode editar qualquer OS)

**DESTINO:** SUBSTITUÍDO (tela moderna em Angular com paginação server-side e RBAC)

---

### Tela: NovaOS.aspx

- **Caminho:** `ic1_legado/IControlIT/[Modulo]/NovaOS.aspx`
- **Responsabilidade:** Criação e edição de ordens de serviço

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| Tipo OS | DropDownList | Sim | Carregado de `tblTipoOS` |
| Ativo | DropDownList | Sim | Carregado de `tblAtivos` |
| Locação | DropDownList | Não | Carregado de `tblLocacoes` |
| Técnico | DropDownList | Sim | Carregado de `tblUsuarios WHERE Perfil = 'Tecnico'` |
| Descrição | TextBox (MultiLine) | Sim | MaxLength ilimitado (risco de SQL injection) |
| Data Agendada | TextBox (DatePicker) | Não | Sem validação de data futura |
| Hora Início | TextBox | Não | Formato HH:mm (sem validação) |
| Duração Estimada | TextBox (Numeric) | Não | Em minutos |
| Observações | TextBox (MultiLine) | Não | - |

#### Comportamentos Implícitos

- Salvar chama `WSOrdensSevico.CriarOrdem()` via AJAX
- Validação de campos obrigatórios apenas no client-side (jQuery)
- Sem validação de disponibilidade de técnico (permite dupla alocação)
- Campos de auditoria (`Id_Usuario_Criacao`, `Dt_Criacao`) preenchidos via code-behind
- Sem validação de transição de estado (pode salvar OS concluída com status rascunho)

**DESTINO:** SUBSTITUÍDO (formulário reativo Angular com validações server-side obrigatórias)

---

### Tela: AgendaOS.aspx

- **Caminho:** `ic1_legado/IControlIT/[Modulo]/AgendaOS.aspx`
- **Responsabilidade:** Calendário de agendamentos de OS por técnico

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| Técnico | DropDownList | Sim | Filtro por técnico |
| Mês/Ano | Calendar Control | - | ASP.NET Calendar |
| Grid Agendamentos | DataGrid | - | Horários ocupados do técnico |

#### Comportamentos Implícitos

- Não permite drag-and-drop para reagendar
- Não mostra conflitos visualmente (apenas lista de OS)
- Atualização manual via postback (sem AJAX)
- Sem validação de conflitos ao agendar (permite sobreposição)

**DESTINO:** SUBSTITUÍDO (NgxBootstrap Calendar com drag-drop e validação automática de conflitos)

---

### Tela: ExecutarOS.aspx

- **Caminho:** `ic1_legado/IControlIT/[Modulo]/ExecutarOS.aspx`
- **Responsabilidade:** Painel de execução em tempo real (preencher checklist, registrar tempo, anexar fotos)

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| Checklist Items | CheckBoxList | Sim | Lista estática hard-coded no HTML |
| Observações Item | TextBox (para cada item) | Não | - |
| Hora Início | TextBox (readonly) | - | Preenchido ao clicar "Iniciar" |
| Hora Fim | TextBox (readonly) | - | Preenchido ao clicar "Concluir" |
| Upload Foto | FileUpload | Não | Aceita qualquer imagem sem validação EXIF |
| Assinatura | CheckBox | Não | Apenas checkbox manual (sem captura digital) |
| Nome Signatário | TextBox | Não | Campo livre de texto |

#### Comportamentos Implícitos

- Checklist é HTML estático, não dinâmico baseado em tipo de OS
- Não há timer automático (técnico digita manualmente hora início/fim)
- Sem registro de pausas (almoço, deslocamento)
- Upload de foto sem validação de tamanho, EXIF ou tipo MIME (risco de segurança)
- Assinatura é apenas checkbox + campo texto (sem imagem ou hash)
- Conclusão sem validação de checklist completo (permite concluir com itens vazios)

**DESTINO:** SUBSTITUÍDO (tela mobile-responsive com timer automático, pausa/retomada, assinatura digital real e validação EXIF)

---

### Tela: RelatorioTecnico.aspx

- **Caminho:** `ic1_legado/IControlIT/[Modulo]/RelatorioTecnico.aspx`
- **Responsabilidade:** Dashboard de produtividade de técnico

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| Técnico | DropDownList | Sim | - |
| Data Início | TextBox (DatePicker) | Sim | - |
| Data Fim | TextBox (DatePicker) | Sim | - |
| Grid Estatísticas | DataGrid | - | Total OS, Tempo Médio, SLA Violado |

#### Comportamentos Implícitos

- Relatório gerado via stored procedure `pa_RelatorioProduividadeMensal`
- Sem exportação para PDF/Excel (apenas visualização em tela)
- Sem gráficos (apenas tabela)
- Cálculo de tempo médio inclui pausas (impreciso)

**DESTINO:** SUBSTITUÍDO (dashboard com Charts.js, exportação PDF/Excel e cálculo preciso de tempo efetivo)

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

| Método | Local | Responsabilidade | Observações |
|--------|-------|------------------|-------------|
| `ObterOrdens(filtro)` | `WSOrdensSevico.asmx.vb` | Retorna lista de OS com filtros | Retorna DataSet sem paginação (risco de timeout) |
| `CriarOrdem(dados)` | `WSOrdensSevico.asmx.vb` | Cria nova OS | Validação apenas de campos obrigatórios (sem regras de negócio) |
| `AtualizarOrdem(id, dados)` | `WSOrdensSevico.asmx.vb` | Atualiza OS existente | Sem validação de transição de estado |
| `ConcluirOrdem(id, assinatura)` | `WSOrdensSevico.asmx.vb` | Finaliza OS com "assinatura" (texto) | Assinatura é string simples, sem hash ou timestamp |
| `ObterRelatorio(dataInicio, dataFim, tecnicoId)` | `WSOrdensSevico.asmx.vb` | Gera relatório de produtividade | Chama stored procedure, retorna DataSet |

**DESTINO:** SUBSTITUÍDO (endpoints REST API com validações completas, DTOs tipados e CQRS)

---

## 4. TABELAS LEGADAS

| Tabela | Finalidade | Problemas Identificados |
|--------|------------|-------------------------|
| `tblOrdensSevico` | Tabela principal de OS | ❌ Campo `St_OS` é VARCHAR (deveria ser ENUM), ❌ Sem ClienteId (multi-tenancy fraco), ❌ Campos de auditoria incompletos (sem LastModifiedBy) |
| `tblChecklistOS` | Items do checklist | ❌ Não existe (checklist é HTML estático nas telas) |
| `tblRegistroPausaOS` | Registro de pausas | ❌ Não existe (pausas não são rastreadas) |
| `tblMaterialConsumidoOS` | Materiais consumidos | ❌ Não existe (consumo de materiais não rastreado por OS) |
| `tblAssinaturaOS` | Assinatura digital | ❌ Não existe (assinatura é apenas checkbox) |
| `tblFotosOS` | Fotos/evidências | ❌ Caminho de arquivo em VARCHAR (sem blob storage), ❌ Sem metadados EXIF |

**Mapeamento para Tabelas Modernas:**

| Legado | Moderno | Observações |
|--------|---------|-------------|
| `tblOrdensSevico` | `OrdensSevico` | Adicionar ClienteId, enum Status, auditoria completa |
| (inexistente) | `ChecklistItems` | Tabela nova para checklist dinâmico |
| (inexistente) | `RegistroPausaRetomada` | Tabela nova para rastrear pausas |
| (inexistente) | `MaterialConsumido` | Tabela nova para materiais por OS |
| (inexistente) | `AssinaturaDigital` | Tabela nova para assinatura com hash |
| `tblFotosOS` | `FotosEvidencia` | Migrar para blob storage, adicionar metadados EXIF |

---

## 5. STORED PROCEDURES LEGADAS

| Procedure | Responsabilidade | Lógica Principal (Linguagem Natural) | DESTINO |
|-----------|------------------|--------------------------------------|---------|
| `pa_ObterOrdensPorTecnico` | Lista OS de um técnico | Faz SELECT em `tblOrdensSevico WHERE Id_TecnicoResponsavel = @tecnicoId AND Fl_Deletado = 0`, retorna todas as colunas sem paginação | SUBSTITUÍDO (query LINQ com paginação) |
| `pa_CalcularTempoTotalOS` | Soma durações de OS | Faz `SUM(Vl_Duracao_Real)` agrupado por técnico. **Problema:** Inclui pausas no cálculo (impreciso) | SUBSTITUÍDO (query LINQ com exclusão de pausas) |
| `pa_RelatorioProduividadeMensal` | Consolidação mensal | Calcula Total OS, Tempo Médio, Taxa de Conclusão usando GROUP BY por técnico e mês. **Problema:** Não calcula SLA violado corretamente | SUBSTITUÍDO (query LINQ com cálculo correto de SLA) |
| `pa_ValidarConflitoriosAgendamento` | Verifica conflito técnico | **NÃO EXISTE** - Validação de conflitos não é feita no legado | DESCARTADO (regra implementada em RN-RF077-004) |

---

## 6. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

Regras identificadas no código VB.NET que **não estavam documentadas formalmente**:

### RL-RN-001: Status de OS é String Livre

**Descrição:** Campo `St_OS` aceita qualquer string, não é ENUM. Code-behind valida apenas valores esperados ("Rascunho", "Pendente", etc.), mas banco permite qualquer valor.

**Problema:** Dados inconsistentes (ex: "Em Execucao" vs "Em Execução" com acento), dificuldade de queries.

**DESTINO:** SUBSTITUÍDO (enum `OrdemServicoStatus` tipado no backend)

---

### RL-RN-002: Transição de Estado Sem Validação

**Descrição:** Qualquer OS pode ser salva com qualquer status, sem validação de fluxo. Code-behind não valida se transição é permitida (ex: pode salvar OS "Concluída" direto de "Rascunho").

**Problema:** Estados inválidos no banco, falta de integridade de processo.

**DESTINO:** SUBSTITUÍDO (RN-RF077-001 implementa validação estrita de transições)

---

### RL-RN-003: Checklist Completude Não Validada

**Descrição:** Tela `ExecutarOS.aspx` permite conclusão mesmo com itens de checklist vazios. Validação é opcional no client-side (JavaScript), pode ser bypassada.

**Problema:** OS marcadas como concluídas sem todas as atividades executadas.

**DESTINO:** SUBSTITUÍDO (RN-RF077-002 bloqueia conclusão com checklist incompleto no backend)

---

### RL-RN-004: Assinatura é Apenas Checkbox

**Descrição:** Campo "Assinatura" é CheckBox + TextField (nome do signatário). Não há captura de imagem, timestamp ou hash de verificação.

**Problema:** Sem comprovação legal, fácil falsificação.

**DESTINO:** SUBSTITUÍDO (RN-RF077-003 exige assinatura digital com hash SHA-256)

---

### RL-RN-005: Disponibilidade de Técnico Não Verificada

**Descrição:** Agendamento permite selecionar técnico sem verificar se ele já tem outra OS no mesmo horário. Stored procedure `pa_ValidarConflitoriosAgendamento` não existe.

**Problema:** Dupla alocação de técnicos, conflitos de agenda.

**DESTINO:** SUBSTITUÍDO (RN-RF077-004 valida disponibilidade automaticamente)

---

### RL-RN-006: Tempo Real Inclui Pausas

**Descrição:** Campo `Vl_Duracao_Real` é calculado como diferença entre `Hr_Inicio` e `Hr_Fim`, sem descontar pausas (que não são rastreadas).

**Problema:** Cálculo de custos impreciso, não reflete tempo efetivo de trabalho.

**DESTINO:** SUBSTITUÍDO (RN-RF077-008 rastreia pausas e calcula tempo efetivo)

---

### RL-RN-007: Fotos Sem Validação EXIF

**Descrição:** Upload de fotos aceita qualquer imagem sem verificar metadados EXIF (data de captura, GPS). Fotos antigas podem ser reutilizadas sem detecção.

**Problema:** Sem autenticidade temporal, facilita fraude.

**DESTINO:** SUBSTITUÍDO (RN-RF077-009 valida EXIF obrigatoriamente)

---

### RL-RN-008: Consumo de Material Não Rastreado por OS

**Descrição:** Não há tabela `tblMaterialConsumidoOS`. Consumo de materiais é registrado manualmente em sistema separado, sem vínculo automático com OS.

**Problema:** Sem rastreabilidade de consumo, sem redução automática de estoque.

**DESTINO:** SUBSTITUÍDO (RN-RF077-006 vincula materiais a OS e reduz estoque automaticamente)

---

### RL-RN-009: SLA Violado Calculado Manualmente

**Descrição:** Flag `Fl_SLA_Violado` é preenchido manualmente pelo usuário ou via job noturno. Não há verificação em tempo real durante transições de estado.

**Problema:** Atrasos não detectados imediatamente, métricas imprecisas.

**DESTINO:** SUBSTITUÍDO (RN-RF077-007 calcula SLA automaticamente ao iniciar execução)

---

### RL-RN-010: Relatórios Baseados em Stored Procedures Lentas

**Descrição:** Relatórios usam stored procedures que fazem SELECT sem índices otimizados. Com >10.000 OS, relatório trava por timeout.

**Problema:** Performance ruim, timeouts frequentes.

**DESTINO:** SUBSTITUÍDO (queries LINQ otimizadas com índices apropriados)

---

## 7. GAP ANALYSIS (LEGADO × RF MODERNO)

| Item | Legado | RF Moderno | Observação |
|------|--------|------------|------------|
| **Assinatura Digital** | Checkbox + campo texto | Captura de assinatura com hash SHA-256 | **CRÍTICO** - Funcionalidade completamente nova |
| **Validação EXIF** | Inexistente | Obrigatória em fotos | **ALTO** - Previne fraude |
| **Checklist Dinâmico** | HTML estático | Baseado em tipo de OS, banco de dados | **ALTO** - Flexibilidade operacional |
| **Rastreamento de Pausas** | Inexistente | Registro completo com motivos | **MÉDIO** - Precisão de custos |
| **Validação de Conflitos** | Inexistente | Automática ao agendar | **MÉDIO** - Evita dupla alocação |
| **Transição de Estados** | Sem validação | Validação estrita de fluxo | **ALTO** - Integridade de processo |
| **Consumo de Materiais** | Não rastreado por OS | Vínculo automático + redução de estoque | **ALTO** - Rastreabilidade financeira |
| **Cálculo de SLA** | Manual/Job noturno | Automático em tempo real | **MÉDIO** - Visibilidade operacional |
| **Multi-tenancy** | Bancos separados | ClienteId em tabelas | **ALTO** - Arquitetura moderna |
| **Auditoria** | Parcial (Created, Updated) | Completa com histórico de mudanças | **MÉDIO** - Conformidade regulatória |

---

## 8. DECISÕES DE MODERNIZAÇÃO

### Decisão 1: Criar Tabelas Auxiliares (Checklist, Pausas, Materiais)

- **Descrição:** Implementar tabelas que não existiam no legado (`ChecklistItems`, `RegistroPausaRetomada`, `MaterialConsumido`)
- **Motivo:** Funcionalidades essenciais estavam ausentes ou implementadas manualmente
- **Impacto:** **Alto** - Novas funcionalidades completas
- **Benefício:** Rastreabilidade, precisão de custos, flexibilidade operacional

---

### Decisão 2: Substituir Assinatura Checkbox por Assinatura Digital Real

- **Descrição:** Implementar captura de assinatura com imagem, timestamp e hash SHA-256
- **Motivo:** Assinatura legado (checkbox) não tem validade legal
- **Impacto:** **Crítico** - Mudança fundamental de processo
- **Benefício:** Comprovação legal, conformidade ISO 27001 (não repúdio)

---

### Decisão 3: Migrar de Stored Procedures para CQRS + LINQ

- **Descrição:** Substituir stored procedures por Commands/Queries LINQ tipadas
- **Motivo:** Stored procedures lentas, difíceis de manter, sem type-safety
- **Impacto:** **Alto** - Mudança arquitetural completa
- **Benefício:** Performance, manutenibilidade, testabilidade

---

### Decisão 4: Implementar Validação de Transição de Estados no Backend

- **Descrição:** Criar regra de negócio RN-RF077-001 que valida transições permitidas
- **Motivo:** Legado permitia estados inválidos (ex: Rascunho → Concluída direto)
- **Impacto:** **Alto** - Mudança de comportamento
- **Benefício:** Integridade de processo, prevenção de dados inconsistentes

---

### Decisão 5: Adicionar ClienteId para Multi-tenancy Correto

- **Descrição:** Incluir campo `ClienteId` em todas as tabelas de OS
- **Motivo:** Legado usa bancos separados (multi-database), difícil de escalar
- **Impacto:** **Médio** - Mudança de arquitetura de dados
- **Benefício:** Escalabilidade, manutenibilidade, isolamento row-level

---

## 9. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Mitigação |
|-------|---------|-----------|
| **Dados legado com estados inconsistentes** (ex: "Em Execucao" sem acento) | Alto | Script de limpeza pré-migração para normalizar valores de `St_OS` |
| **OS concluídas sem checklist completo** | Médio | Aceitar dados históricos como-is, aplicar validação apenas em novos registros |
| **Fotos sem EXIF** (anexadas antes da modernização) | Médio | Migrar fotos com flag `ValidacaoExifSkipped = true` para dados legados |
| **Assinaturas legado (texto) vs modernas (hash)** | Baixo | Manter campo `AssinaturaLegadoTexto` separado de `AssinaturaDigitalHash` |
| **Técnicos com OS duplicadas no mesmo horário** (dados legado) | Médio | Identificar e resolver conflitos manualmente antes de migração |
| **Performance de migração** (>50.000 OS) | Alto | Migração em lotes de 5.000, validação incremental |
| **Usuários acostumados com checklist HTML estático** | Baixo | Treinamento de mudança de processo (checklist dinâmico) |

---

## 10. RASTREABILIDADE

| Elemento Legado | Referência RF Moderno |
|-----------------|----------------------|
| `tblOrdensSevico` | `OrdensSevico` (Entity) - MD-RF077.md |
| `OrdensSevico.aspx` | Componente Angular `ordens-servico-list` - WF-RF077.md |
| `NovaOS.aspx` | Componente Angular `ordens-servico-form` - WF-RF077.md |
| `ExecutarOS.aspx` | Componente Angular `ordens-servico-executar` - WF-RF077.md |
| `WSOrdensSevico.CriarOrdem()` | `CreateOrdemServicoCommand` - RF077.md Seção 5 |
| `pa_ObterOrdensPorTecnico` | `GetOrdensServicoQuery` - RF077.md Seção 5 |
| Campo `St_OS` (VARCHAR) | `Status` (enum `OrdemServicoStatus`) - RN-RF077-001 |
| Flag `Fl_SLA_Violado` | `IndicadorSlaViolado` (bool) - RN-RF077-007 |
| (inexistente) | `ChecklistItems` (tabela nova) - RN-RF077-002 |
| (inexistente) | `RegistroPausaRetomada` (tabela nova) - RN-RF077-008 |
| (inexistente) | `AssinaturaDigital` (tabela nova) - RN-RF077-003 |

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|--------|------|-----------|-------|
| 1.0 | 2025-01-14 | Referência ao legado criada: 7 seções, 10 regras de negócio implícitas, 9 riscos de migração, gap analysis completo | Agência ALC - alc.dev.br |

---

**Última Atualização:** 2025-01-14
**Autor:** Agência ALC - alc.dev.br
**Status:** Documentação de legado completa - Pronto para criação de RL-RF077.yaml
