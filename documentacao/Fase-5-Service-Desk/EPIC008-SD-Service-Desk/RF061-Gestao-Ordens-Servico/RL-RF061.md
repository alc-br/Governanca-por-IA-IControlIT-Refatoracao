# RL-RF061 — Referência ao Legado (Gestão de Ordens de Serviço)

**Versão:** 1.0
**Data:** 2025-12-30
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF061 - Gestão de Ordens de Serviço (OS)
**Sistema Legado:** ASP.NET Web Forms + VB.NET + SQL Server
**Objetivo:** Documentar o comportamento do sistema legado de Ordens de Serviço que serve de base para a modernização, garantindo rastreabilidade, entendimento histórico e mitigação de riscos.

---

## 1. CONTEXTO DO LEGADO

### 1.1 Arquitetura Geral

- **Arquitetura:** Monolítica WebForms com acoplamento entre UI e lógica de negócio
- **Linguagem / Stack:** VB.NET, ASP.NET Web Forms 4.x, jQuery
- **Banco de Dados:** SQL Server 2012+ (múltiplos bancos por cliente)
- **Multi-tenant:** NÃO (cada cliente tinha banco separado)
- **Auditoria:** PARCIAL (apenas tabela de log genérica, sem rastreabilidade completa)
- **Configurações:** Web.config + tabelas de configuração no banco

### 1.2 Problemas Arquiteturais Identificados

1. **Lógica de negócio misturada com UI:** Code-behind VB.NET continha validações e regras de negócio
2. **Falta de API REST:** Webservices SOAP (.asmx) com contratos rígidos e sem versionamento
3. **Ausência de isolamento multi-tenant:** Cada cliente exigia instância separada do sistema
4. **Auditoria insuficiente:** Não rastreava todas as operações (ex: visualizações, alterações de status)
5. **Sem controle de concorrência:** Possibilidade de edição simultânea sem controle otimista
6. **Stored Procedures com lógica complexa:** Regras de negócio espalhadas entre código VB e SQL
7. **Sem versionamento de API:** Mudanças quebravam integrações existentes
8. **Falta de validação centralizada:** Validações duplicadas entre cliente e servidor

---

## 2. TELAS DO LEGADO

### Tela: ListaOrdensServico.aspx

- **Caminho:** `ic1_legado/IControlIT/ServiceDesk/OrdensServico/ListaOrdensServico.aspx`
- **Responsabilidade:** Listar ordens de serviço com filtros (status, técnico, período, cliente)

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| ddlStatus | DropDownList | Não | Filtro por status da OS |
| ddlTecnico | DropDownList | Não | Filtro por técnico responsável |
| txtDataInicio | TextBox (DatePicker) | Não | Filtro por data inicial |
| txtDataFim | TextBox (DatePicker) | Não | Filtro por data final |
| txtCliente | TextBox | Não | Filtro por nome do cliente |
| gvOrdensServico | GridView | - | Grid com OSs (paginação de 50 registros) |

#### Comportamentos Implícitos

- **Filtro de empresa hard-coded:** Code-behind filtrava automaticamente por `Id_Empresa` da sessão do usuário
- **Ordenação padrão:** OSs ordenadas por data de criação DESC (mais recentes primeiro)
- **Paginação fixa:** 50 registros por página sem opção de alteração
- **Status coloridos:** Grid exibia cores diferentes por status (verde=finalizada, amarelo=agendada, vermelho=atrasada)
- **Sem refresh automático:** Usuário precisava atualizar página manualmente (F5)

---

### Tela: CadastroOrdemServico.aspx

- **Caminho:** `ic1_legado/IControlIT/ServiceDesk/OrdensServico/CadastroOrdemServico.aspx`
- **Responsabilidade:** Criar ou editar ordem de serviço

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| ddlCliente | DropDownList | Sim | Cliente solicitante |
| ddlTipoOS | DropDownList | Sim | Tipo de serviço (manutenção, instalação, etc.) |
| ddlTecnico | DropDownList | Não | Técnico responsável (opcional na criação) |
| txtDataAgendada | TextBox (DatePicker) | Não | Data/hora de agendamento |
| txtDescricao | TextBox (MultiLine) | Sim | Descrição do serviço |
| txtObservacoes | TextBox (MultiLine) | Não | Observações adicionais |
| chkPrioridade | CheckBox | Não | Marcar como prioritária |

#### Comportamentos Implícitos

- **Número da OS gerado automaticamente:** Formato `OS-{ID_SEQUENCIAL}` (sem ano)
- **Status inicial fixo:** Sempre criava com status "AGUARDANDO_AGENDAMENTO"
- **Validação de técnico disponível:** NÃO EXISTIA no legado (podia agendar em horário ocupado)
- **Sem integração com solicitações:** OS criada sempre manualmente, não havia criação automática
- **Sem checklist:** Não existia conceito de checklist obrigatório por tipo
- **Sem notificações:** Cliente não era notificado sobre agendamento

---

### Tela: ExecutarOrdemServico.aspx

- **Caminho:** `ic1_legado/IControlIT/ServiceDesk/OrdensServico/ExecutarOrdemServico.aspx`
- **Responsabilidade:** Registrar execução da OS pelo técnico

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| txtDataInicio | TextBox (DatePicker) | Sim | Data/hora de início (manual) |
| txtDataFim | TextBox (DatePicker) | Sim | Data/hora de fim (manual) |
| txtRelatorioExecucao | TextBox (MultiLine) | Sim | Relatório do técnico |
| gvPecasUtilizadas | GridView | Não | Lista de peças usadas |
| btnAdicionarPeca | Button | - | Adicionar peça à lista |
| fuFotoAntes | FileUpload | Não | Upload de foto antes |
| fuFotoDepois | FileUpload | Não | Upload de foto depois |

#### Comportamentos Implícitos

- **Data/hora manual:** Técnico digitava data/hora de início e fim (sem check-in/check-out automático)
- **Sem geolocalização:** Não capturava GPS do técnico
- **Cálculo de tempo manual:** Sistema não calculava automaticamente tempo de atendimento
- **Baixa de estoque manual:** Técnico adicionava peças mas baixa no estoque era processo separado
- **Sem assinatura digital:** Não havia captura de assinatura do cliente
- **Fotos limitadas:** Apenas 2 fotos (antes/depois), sem descrição ou timestamp automático
- **Sem validação de SLA:** Sistema não alertava se OS estava atrasada

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

### Webservice: OrdemServicoService.asmx

| Método | Local | Responsabilidade | Observações |
|--------|-------|------------------|-------------|
| CriarOrdemServico | `/Services/OrdemServicoService.asmx` | Criar nova OS via integração | SOAP, sem validação de disponibilidade de técnico |
| ConsultarOrdemServico | `/Services/OrdemServicoService.asmx` | Consultar OS por ID | Retornava todos os campos (sem DTOs específicos) |
| ListarOrdensServico | `/Services/OrdemServicoService.asmx` | Listar OSs com filtros | Sem paginação (retornava todos os registros) |
| AgendarOrdemServico | `/Services/OrdemServicoService.asmx` | Definir técnico e data | Sem validação de conflito de agenda |
| FinalizarOrdemServico | `/Services/OrdemServicoService.asmx` | Marcar OS como finalizada | Não validava se checklist estava completo |

**Problemas identificados:**
- Sem autenticação JWT (apenas validação de API Key simples)
- Sem versionamento (mudanças quebravam integrações)
- Sem throttling ou rate limiting
- Erros genéricos (sempre HTTP 200 com erro no XML)

---

## 4. STORED PROCEDURES

### SP: sp_CriarOrdemServico

- **Caminho:** `ic1_legado/Database/Procedures/sp_CriarOrdemServico.sql`
- **Parâmetros de entrada:**
  - `@Id_Cliente INT`
  - `@Id_TipoOS INT`
  - `@Descricao VARCHAR(500)`
  - `@Id_Usuario_Criacao INT`
- **Parâmetros de saída:**
  - `@Id_OS INT OUTPUT`

**Lógica principal (em linguagem natural):**
1. Gera número sequencial da OS consultando MAX(Id_OS) + 1
2. Insere registro na tabela `OrdemServico` com status "AGUARDANDO_AGENDAMENTO"
3. Insere log genérico na tabela `AuditLog` (apenas operação "CREATE")
4. Retorna ID da OS criada

**Problemas:**
- Vulnerável a race condition (MAX+1 pode gerar duplicatas em alta concorrência)
- Não valida se cliente existe
- Não valida se tipo de OS existe
- Auditoria insuficiente (não registra valores dos campos)

---

### SP: sp_AgendarOrdemServico

- **Caminho:** `ic1_legado/Database/Procedures/sp_AgendarOrdemServico.sql`
- **Parâmetros de entrada:**
  - `@Id_OS INT`
  - `@Id_Tecnico INT`
  - `@Data_Agendada DATETIME`
  - `@Id_Usuario_Alteracao INT`
- **Parâmetros de saída:** Nenhum

**Lógica principal:**
1. Atualiza campos `Id_Tecnico` e `Data_Agendada` na tabela `OrdemServico`
2. Altera status para "AGENDADA"
3. Registra log de alteração
4. **NÃO verifica se técnico está disponível** (problema crítico)

---

### SP: sp_FinalizarOrdemServico

- **Caminho:** `ic1_legado/Database/Procedures/sp_FinalizarOrdemServico.sql`
- **Parâmetros de entrada:**
  - `@Id_OS INT`
  - `@Data_Inicio DATETIME`
  - `@Data_Fim DATETIME`
  - `@Relatorio_Execucao VARCHAR(MAX)`
  - `@Id_Usuario_Alteracao INT`
- **Parâmetros de saída:** Nenhum

**Lógica principal:**
1. Atualiza campos de data de início, fim, relatório
2. Altera status para "FINALIZADA"
3. Calcula tempo de atendimento (minutos) = DATEDIFF(minute, @Data_Inicio, @Data_Fim)
4. Registra log de finalização
5. **NÃO valida se checklist foi preenchido** (não existia checklist)
6. **NÃO valida se assinatura foi coletada** (não existia assinatura digital)

---

## 5. TABELAS LEGADAS

### Tabela: OrdemServico

| Campo | Tipo | Problema Identificado |
|-------|------|----------------------|
| Id_OS | INT IDENTITY | Chave primária sequencial (vulnerável a race condition) |
| Numero_OS | VARCHAR(50) | Gerado como "OS-{ID}", sem padrão de ano |
| Id_Cliente | INT | **SEM FOREIGN KEY** (possível órfão) |
| Id_TipoOS | INT | **SEM FOREIGN KEY** (possível órfão) |
| Id_Tecnico | INT | **SEM FOREIGN KEY** (possível órfão) |
| Data_Agendada | DATETIME | **NULLABLE** (deveria ser obrigatório quando status=AGENDADA) |
| Data_Inicio | DATETIME | Informado manualmente (não automático) |
| Data_Fim | DATETIME | Informado manualmente (não automático) |
| Tempo_Atendimento | INT | Minutos calculados, mas sem validação |
| Status | VARCHAR(50) | **SEM CONSTRAINT** (valores livres, sem enum) |
| Prioridade | BIT | Flag de prioridade sem impacto em SLA |
| Descricao | VARCHAR(500) | Campo limitado (500 chars) |
| Relatorio_Execucao | VARCHAR(MAX) | Apenas texto, sem checklist estruturado |
| Id_Usuario_Criacao | INT | Auditoria parcial |
| Dt_Criacao | DATETIME | Auditoria parcial |
| Id_Usuario_Alteracao | INT | Auditoria parcial |
| Dt_Alteracao | DATETIME | Auditoria parcial |

**Problemas gerais:**
- Sem campo `EmpresaId` (multi-tenancy não existia)
- Sem soft delete (exclusão era física)
- Sem campos de auditoria completos (faltava IP, User Agent, etc.)
- Sem versionamento de registro (concorrência não controlada)

---

### Tabela: PecaUtilizadaOS

| Campo | Tipo | Problema Identificado |
|-------|------|----------------------|
| Id_PecaUtilizada | INT IDENTITY | Chave primária |
| Id_OS | INT | **SEM FOREIGN KEY** (possível órfão) |
| Id_Peca | INT | **SEM FOREIGN KEY** (possível órfão) |
| Quantidade | INT | **SEM VALIDAÇÃO** (podia ser negativo) |
| Valor_Unitario | DECIMAL(10,2) | Sem validação de range |
| Valor_Total | DECIMAL(10,2) | **Calculado manualmente** (vulnerável a inconsistência) |

**Problemas:**
- Baixa de estoque não automática (processo separado)
- Sem validação de estoque disponível
- Sem rastreabilidade de onde a peça foi retirada (almoxarifado)

---

### Tabela: FotoOS

| Campo | Tipo | Problema Identificado |
|-------|------|----------------------|
| Id_Foto | INT IDENTITY | Chave primária |
| Id_OS | INT | **SEM FOREIGN KEY** |
| Tipo_Foto | VARCHAR(10) | Valores: "ANTES", "DEPOIS" (sem constraint) |
| Caminho_Arquivo | VARCHAR(500) | Caminho físico no servidor (vulnerável) |
| Dt_Upload | DATETIME | Data de upload |

**Problemas:**
- Fotos armazenadas em pasta do servidor (não em blob storage)
- Sem compressão automática (arquivos grandes)
- Sem validação de tipo de arquivo (aceitava qualquer extensão)
- Sem descrição da foto

---

## 6. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

### RL-RN-001: Número da OS Sequencial Simples

**Localização:** `ic1_legado/Database/Procedures/sp_CriarOrdemServico.sql - Linha 15-20`

**Descrição (linguagem natural):**
O número da OS era gerado automaticamente no formato "OS-{ID_SEQUENCIAL}", onde ID_SEQUENCIAL era apenas o ID numérico do registro. Não incluía ano, mês ou identificador de empresa, causando duplicatas em migrações multi-cliente.

**Destino:** SUBSTITUÍDO

**Justificativa:** Sistema moderno usa formato "OS-YYYY-NNNNN" com ano para melhor organização e evitar conflitos em multi-tenancy.

**Rastreabilidade:**
- RF Moderno: RN-RF061-001
- UC Moderno: UC01-RF061 (Criar OS)

---

### RL-RN-002: Agendamento Sem Validação de Disponibilidade

**Localização:** `ic1_legado/Database/Procedures/sp_AgendarOrdemServico.sql - Linha 8-12`

**Descrição:**
O sistema permitia agendar OS para qualquer técnico em qualquer horário, sem verificar se o técnico já tinha outra OS agendada no mesmo período. Isso causava conflitos de agenda e sobrecarga de técnicos.

**Destino:** SUBSTITUÍDO

**Justificativa:** Sistema moderno valida disponibilidade de técnico antes de permitir agendamento, evitando conflitos.

**Rastreabilidade:**
- RF Moderno: RN-RF061-002
- UC Moderno: UC03-RF061 (Agendar OS)

---

### RL-RN-003: Data/Hora de Execução Informada Manualmente

**Localização:** `ic1_legado/IControlIT/ServiceDesk/OrdensServico/ExecutarOrdemServico.aspx.vb - Linha 45-60`

**Descrição:**
Técnico digitava manualmente data/hora de início e fim do atendimento. Não havia check-in/check-out automático com timestamp do servidor, permitindo manipulação de dados e falta de rastreabilidade.

**Destino:** SUBSTITUÍDO

**Justificativa:** Sistema moderno captura automaticamente timestamp no momento do check-in/check-out do técnico, garantindo integridade dos dados.

**Rastreabilidade:**
- RF Moderno: RN-RF061-007, RN-RF061-008
- UC Moderno: UC02-RF061 (Executar OS)

---

### RL-RN-004: Baixa de Estoque Manual

**Localização:** `ic1_legado/IControlIT/ServiceDesk/OrdensServico/ExecutarOrdemServico.aspx.vb - Linha 120-135`

**Descrição:**
Após finalizar OS, técnico informava peças utilizadas mas a baixa no estoque era processo manual separado (executado por almoxarifado). Causava inconsistências e atrasos no controle de estoque.

**Destino:** SUBSTITUÍDO

**Justificativa:** Sistema moderno dá baixa automática no estoque ao finalizar OS, garantindo sincronização em tempo real.

**Rastreabilidade:**
- RF Moderno: RN-RF061-005
- UC Moderno: UC02-RF061 (Executar OS)

---

### RL-RN-005: Sem Assinatura Digital

**Localização:** Não existia no legado

**Descrição:**
Sistema legado não coletava assinatura digital do cliente. Comprovação de execução do serviço era apenas através do relatório do técnico, sem validação do cliente.

**Destino:** A_REVISAR (funcionalidade nova)

**Justificativa:** Sistema moderno exige assinatura digital do cliente para comprovação formal de execução. Regra nova sem equivalente no legado.

**Rastreabilidade:**
- RF Moderno: RN-RF061-004
- UC Moderno: UC02-RF061 (Coletar Assinatura)

---

### RL-RN-006: Sem Geolocalização

**Localização:** Não existia no legado

**Descrição:**
Sistema legado não capturava localização GPS do técnico durante atendimento. Rastreabilidade geográfica inexistente.

**Destino:** A_REVISAR (funcionalidade nova)

**Justificativa:** Sistema moderno captura GPS no check-in/check-out para rastreabilidade e conformidade LGPD. Funcionalidade nova.

**Rastreabilidade:**
- RF Moderno: RN-RF061-007
- UC Moderno: UC02-RF061 (Check-in/Check-out)

---

### RL-RN-007: Sem Checklist Estruturado

**Localização:** Não existia no legado

**Descrição:**
Técnico preenchia apenas campo de texto livre "Relatório de Execução". Não havia checklist estruturado com itens obrigatórios por tipo de OS.

**Destino:** A_REVISAR (funcionalidade nova)

**Justificativa:** Sistema moderno implementa checklist obrigatório por tipo de OS para padronização de procedimentos. Funcionalidade nova.

**Rastreabilidade:**
- RF Moderno: RN-RF061-003
- UC Moderno: UC02-RF061 (Preencher Checklist)

---

### RL-RN-008: Sem Controle de SLA

**Localização:** Não existia no legado

**Descrição:**
Sistema legado não calculava ou monitorava SLA de atendimento. Não havia alertas de atraso ou vencimento de prazo.

**Destino:** A_REVISAR (funcionalidade nova)

**Justificativa:** Sistema moderno implementa controle de SLA com alertas automáticos. Funcionalidade nova.

**Rastreabilidade:**
- RF Moderno: RN-RF061-010
- UC Moderno: UC00-RF061 (Dashboard com SLA)

---

### RL-RN-009: Sem Avaliação NPS

**Localização:** Não existia no legado

**Descrição:**
Cliente não avaliava o serviço prestado. Não havia medição de satisfação ou NPS.

**Destino:** A_REVISAR (funcionalidade nova)

**Justificativa:** Sistema moderno coleta avaliação NPS após finalização para medir satisfação. Funcionalidade nova.

**Rastreabilidade:**
- RF Moderno: RN-RF061-011
- UC Moderno: UC02-RF061 (Avaliar Serviço)

---

### RL-RN-010: Sem Notificações Automáticas

**Localização:** Não existia no legado

**Descrição:**
Cliente não recebia notificações sobre agendamento, reagendamento ou conclusão de OS. Comunicação era manual (telefone/email).

**Destino:** A_REVISAR (funcionalidade nova)

**Justificativa:** Sistema moderno envia notificações automáticas via SMS/WhatsApp/Email. Funcionalidade nova.

**Rastreabilidade:**
- RF Moderno: RN-RF061-014
- UC Moderno: UC03-RF061 (Agendar OS com notificação)

---

## 7. GAP ANALYSIS (LEGADO × MODERNO)

| Funcionalidade | Legado | RF Moderno | Decisão |
|----------------|--------|------------|---------|
| Criação de OS | ✅ Manual apenas | ✅ Manual ou automática (via solicitação) | **EVOLUÍDO** |
| Agendamento | ✅ Sem validação | ✅ Com validação de disponibilidade | **EVOLUÍDO** |
| Check-in/Check-out | ❌ Data/hora manual | ✅ Automático com GPS | **NOVO** |
| Checklist | ❌ Texto livre | ✅ Checklist estruturado obrigatório | **NOVO** |
| Assinatura Digital | ❌ Não existia | ✅ Obrigatória com hash SHA-256 | **NOVO** |
| Geolocalização | ❌ Não existia | ✅ GPS automático (LGPD) | **NOVO** |
| Fotos | ✅ Máx 2 fotos | ✅ Múltiplas fotos com descrição | **EVOLUÍDO** |
| Baixa de Estoque | ✅ Manual | ✅ Automática | **EVOLUÍDO** |
| SLA | ❌ Não existia | ✅ Controle completo com alertas | **NOVO** |
| NPS | ❌ Não existia | ✅ Avaliação obrigatória | **NOVO** |
| Notificações | ❌ Não existia | ✅ Automáticas (SMS/WhatsApp) | **NOVO** |
| Multi-tenancy | ❌ Banco por cliente | ✅ Isolamento por EmpresaId | **EVOLUÍDO** |
| API | ✅ SOAP (.asmx) | ✅ REST (JSON) | **EVOLUÍDO** |
| Auditoria | ✅ Parcial | ✅ Completa (todas operações) | **EVOLUÍDO** |

---

## 8. DECISÕES DE MODERNIZAÇÃO

### Decisão 1: Substituir SOAP por REST API

**Motivo:**
- SOAP é protocolo legado, verboso e rígido
- REST com JSON é padrão moderno, leve e flexível
- Facilita integração com frontend Angular e apps mobile

**Impacto:** ALTO (quebra integrações existentes, requer migração)

---

### Decisão 2: Implementar Check-in/Check-out Automático com GPS

**Motivo:**
- Data/hora manual é vulnerável a manipulação
- GPS garante rastreabilidade geográfica
- Conformidade LGPD (com consentimento)

**Impacto:** MÉDIO (funcionalidade nova, requer educação de usuários)

---

### Decisão 3: Implementar Assinatura Digital com Hash SHA-256

**Motivo:**
- Comprovação formal de execução do serviço
- Integridade garantida por hash criptográfico
- Reduz disputas sobre execução do serviço

**Impacto:** ALTO (funcionalidade crítica nova, requer tablet/smartphone com touch)

---

### Decisão 4: Baixa Automática de Estoque

**Motivo:**
- Eliminar inconsistências entre OS e estoque
- Sincronização em tempo real
- Reduzir trabalho manual de almoxarifado

**Impacto:** MÉDIO (requer integração confiável com RF046 - Estoque)

---

### Decisão 5: Multi-Tenancy por EmpresaId

**Motivo:**
- Eliminar necessidade de bancos separados por cliente
- Reduzir custos de infraestrutura e manutenção
- Facilitar onboarding de novos clientes

**Impacto:** CRÍTICO (mudança arquitetural profunda, requer migração de dados)

---

## 9. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| **Perda de dados históricos** | ALTO | MÉDIA | ETL cuidadoso com validação pós-migração |
| **Quebra de integrações externas** | ALTO | ALTA | Manter webservice SOAP em paralelo (deprecado) por 6 meses |
| **Resistência de técnicos** | MÉDIO | ALTA | Treinamento intensivo e suporte no go-live |
| **Falha na baixa automática de estoque** | ALTO | MÉDIA | Implementar mecanismo de retry e alertas |
| **GPS impreciso em áreas remotas** | MÉDIO | MÉDIA | Permitir justificativa manual quando GPS falhar |
| **Assinaturas não capturadas** | MÉDIO | BAIXA | Validação obrigatória antes de finalizar OS |
| **Performance em multi-tenancy** | MÉDIO | BAIXA | Índices otimizados e caching |

---

## 10. RASTREABILIDADE (LEGADO → MODERNO)

| Elemento Legado | Referência RF | Referência UC |
|-----------------|---------------|---------------|
| ListaOrdensServico.aspx | RN-RF061-015 | UC00-RF061 |
| CadastroOrdemServico.aspx | RN-RF061-001 | UC01-RF061 |
| ExecutarOrdemServico.aspx | RN-RF061-003 a RN-RF061-008 | UC02-RF061 |
| sp_CriarOrdemServico | RN-RF061-001 | UC01-RF061 |
| sp_AgendarOrdemServico | RN-RF061-002 | UC03-RF061 |
| sp_FinalizarOrdemServico | RN-RF061-004 a RN-RF061-008 | UC02-RF061 |
| Tabela OrdemServico | MD-RF061 | - |
| Tabela PecaUtilizadaOS | MD-RF061 | - |
| Tabela FotoOS | MD-RF061 | - |
| OrdemServicoService.asmx | API REST completa | - |

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|--------|------|-----------|-------|
| 1.0 | 2025-12-30 | Documentação completa de referência ao legado do RF061. Extração de 10 regras implícitas. Mapeamento de 3 telas, 1 webservice, 3 SPs, 3 tabelas. Gap Analysis completo. | Agência ALC - alc.dev.br |
