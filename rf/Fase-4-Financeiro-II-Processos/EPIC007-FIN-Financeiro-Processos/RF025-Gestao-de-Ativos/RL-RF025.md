# RL-RF025 — Referência ao Legado: Gestão de Ativos

**Versão:** 1.0
**Data:** 2025-12-30
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF-025
**Sistema Legado:** VB.NET + ASP.NET Web Forms (IControlIT v1)
**Objetivo:** Documentar o comportamento do legado que serviu de base para a modernização, garantindo rastreabilidade, entendimento histórico e mitigação de riscos de migração.

---

## 1. CONTEXTO DO LEGADO

Sistema legado VB.NET/ASP.NET Web Forms utilizado para gestão rudimentar de ativos com problemas críticos de rastreamento e compliance. Empresa mantinha paralelamente planilha Excel (fonte da verdade) devido à desconfiança no sistema legado, criando duplicidade de trabalho e inconsistências.

### Stack Tecnológica

- **Arquitetura:** Monolítica WebForms hospedada em IIS
- **Linguagem / Stack:** VB.NET (code-behind) + ASP.NET Web Forms (.aspx)
- **Banco de Dados:** SQL Server (múltiplos bancos por cliente - SEM multi-tenancy unificado)
- **Autenticação:** Windows Authentication (NTLM/Kerberos)
- **Web Services:** SOAP 1.1 (.asmx)
- **Multi-tenant:** NÃO (um banco por cliente físico)
- **Auditoria:** Inexistente (apenas snapshot do estado atual)
- **Configurações:** Web.config (conexões hardcoded por ambiente)

### Problemas Arquiteturais Identificados

1. **Sem Histórico de Movimentações**: Tabela `Ativo` tinha apenas snapshot do estado atual - impossível rastrear quem usou ativo antes ou quando foi transferido
2. **Etiquetas Papel Ineficientes**: Etiquetas impressas descolavam ou ficavam ilegíveis - taxa de falha 30% após 6 meses
3. **Depreciação Manual em Excel**: Controlador baixava dados mensalmente e calculava depreciação em planilha - erros frequentes de fórmula e versões desatualizadas
4. **Sem Alertas de Garantia**: Descobriam garantia vencida apenas quando precisavam acionar suporte técnico (perda de ~R$80k/ano em reparos fora garantia)
5. **Inventário Manual Doloroso**: 2 colaboradores levavam 2 semanas para inventariar 800 ativos - checklist papel, digitar depois no sistema
6. **Localização Texto Livre**: Campo `Localizacao` aceitava texto livre ("sala do João", "depósito do 2º andar") - impossível gerar mapas ou relatórios confiáveis
7. **Sem Status Workflow**: Status era apenas "Ativo" ou "Inativo" - não diferenciava "em manutenção", "alocado", "disponível para reuso"
8. **Integração Manual com ERP**: Controlador exportava CSV mensalmente e importava no SAP manualmente - esquecimento causava descompasso contábil

---

## 2. TELAS DO LEGADO

### Tela: Ativo.aspx

**Caminho:** `D:\IC2\ic1_legado\IControlIT\IControlIT\Cadastro\Ativo.aspx`

**Responsabilidade:** Tela de cadastro/edição de ativos (equipamentos, linhas telefônicas, chips, etc.) usando ASP.NET Web Forms. Tela complexa com gestão de atribuições de ativos a consumidores, termos de responsabilidade e dados complementares dinâmicos.

#### Modais da Tela

1. **pnlConfirmacao** - Modal "Lixeira" para restaurar ativo desativado
   - Mensagem: "Este Ativo está desativado. Deseja restaurar antes de continuar?"
   - Botões: Não (btContinuar), Sim (btRestaurar)
   - **DESTINO:** SUBSTITUÍDO - Soft delete moderno com reativação via API

2. **pnlObservacao** - Modal de observação obrigatória
   - Campo: Observação (txtObservacaoObrigarotia) - TextBox MultiLine, MaxLength=300, Height=350px
   - Validação: RequiredFieldValidator
   - Botões: Fechar (btCancela), Confirmar (btOk)
   - **DESTINO:** ASSUMIDO - Justificativa obrigatória em baixas/perdidos (RN-RF025-010)

3. **pnlRegistro** - Modal "Dados Adicionais"
   - Observação ReadOnly (txtObservacao) - ForeColor=#FF9900
   - Finalidade (txtFinalidade) - TextBox editável
   - Chave do banco (txtIdentificacao) - ReadOnly, ForeColor=#FF9900
   - **DESTINO:** DESCARTADO - Substituído por formulário dinâmico JSON Schema

#### Campos da Tela Principal

1. **Número do ativo** (txtNumeroAtivo) - TextBox obrigatório, MaxLength=50, ForeColor=#006600, TabIndex=1
   - Validação: RequiredFieldValidator + ValidatorCalloutExtender
   - **DESTINO:** SUBSTITUÍDO - Número patrimônio gerado automaticamente (RN-RF025-001: PAT-{TipoAbrev}-{Ano}-{Sequencial})

2. **Tipo do ativo** (cboAtivoTipo) - DropDownList obrigatório, TabIndex=3, AutoPostBack=True
   - Cascata: Ao mudar, atualiza campo Modelo e Dados Complementares
   - **DESTINO:** ASSUMIDO - Enum Tipo_Ativo mantido (Notebook, Desktop, Smartphone, etc.)

3. **Fornecedor** (cboFornecedor) - DropDownList obrigatório, TabIndex=4
   - Operadora/fornecedor do ativo
   - **DESTINO:** ASSUMIDO - Mantido como Id_Marca/Id_Modelo (normalização)

4. **Modelo do ativo** (cboAtivoModelo) - DropDownList opcional, TabIndex=5
   - Depende de Tipo do ativo (filtrado)
   - **DESTINO:** ASSUMIDO - Mantido como Id_Modelo (FK para tabela Modelo)

5. **Status do ativo** (cboAtivoStatus) - DropDownList opcional, TabIndex=6
   - Ex: Ativo, Inativo, Em Manutenção, Disponível
   - **DESTINO:** SUBSTITUÍDO - Enum moderno (Disponivel, Alocado, Manutencao, Baixado, Perdido, Reservado) com grafo de transições válidas (RN-RF025-003)

6. **Entrega do termo** (txtDataAtivacao) - TextBox com máscara de data, MaxLength=19, TabIndex=7
   - Máscara: `99/99/9999` (MaskedEditExtender + MaskedEditValidator)
   - Data de ativação/entrega do ativo ao consumidor
   - **DESTINO:** ASSUMIDO - Dt_Alocacao em tabela Ativo_Movimentacao (chain of custody)

7. **Retorno Suspensão** (txtSuspenssao) - TextBox com máscara de data
   - Data prevista para retorno de suspensão temporária
   - **DESTINO:** DESCARTADO - Funcionalidade não existirá no sistema moderno

8. **Equipamento** (txtEquipamento) - TextBox MultiLine, ReadOnly, ForeColor=#006600
   - Campo somente leitura (preenchido automaticamente)
   - **DESTINO:** DESCARTADO - Substituído por DTOs estruturados

9. **Endereço** (txtEndereco) - TextBox, ForeColor=#006600
   - Endereço do ativo (se aplicável)
   - **DESTINO:** SUBSTITUÍDO - Localização hierárquica (Localizacao: Edificio → Andar → Sala) + GPS

10. **Numero Sim Card** (txtSimCard) - TextBox, ForeColor=#006600
    - Para ativos de telefonia móvel
    - **DESTINO:** ASSUMIDO - Mantido como campo Numero_Sim_Card

11. **Valor do contrato** (txtVlrContrato) - TextBox, ForeColor=#006600
    - Valor mensal do contrato/aluguel do ativo
    - **DESTINO:** DESCARTADO - Gestão de contratos em RF separado (RF-CTR-001)

12. **Plano do contrato** (txtPlanoContrato) - TextBox, ForeColor=#006600
    - Descrição do plano contratado (ex: 5GB, 1000 minutos)
    - **DESTINO:** ASSUMIDO - Mantido como Tipo_Plano (para ativos Telecom)

13. **Velocidade** (txtVelocidade) - TextBox, ForeColor=#006600
    - Para ativos de internet/rede (ex: 100 Mbps)
    - **DESTINO:** DESCARTADO - Não aplicável ao escopo moderno

#### Grid de Consumidores (dtgUsuario)

DataGrid para vincular ativo a múltiplos consumidores ao longo do tempo

**Colunas:**
1. **Ações** - ImageButton Adicionar/Excluir
2. **Colaborador ou Login** (cboConsumidor / txtDescricao) - DropDownList + TextBox, AutoPostBack=True
3. **Ativação** (txtLote_Ativacao) - TextBox com CalendarExtender (formato: dd/MM/yyyy HH:mm:ss)
4. **Termo Ativação** (btTermo) - ImageButton (ícone Word) para gerar termo de responsabilidade
5. **Devolução** (txtLote_Devolucao) - TextBox com CalendarExtender
6. **Termo Devolução** (btDevolucao) - ImageButton (ícone Word)
7. **Id_Consumidor** - Coluna oculta (Visible=False)
8. **Lupa/Editar** (btLupa / btVoltar) - ImageButtons para buscar consumidor ou editar

**DESTINO:** SUBSTITUÍDO
- Substituído por tabela `Ativo_Movimentacao` (chain of custody) imutável
- Termo de responsabilidade digital via DocuSign/Clicksign API (RN-RF025-004)
- Timeline visual no frontend Angular com todas as movimentações
- Notificação automática ao usuário responsável (email/push)

#### Grid de Dados Complementares (dtgDadosComplemento)

DataGrid dinâmico sem cabeçalho (ShowHeader=False)

**Comportamento:**
- Exibe campos customizados conforme tipo de ativo
- Exemplo: Para computadores (RAM, HD, Processador), para linhas (DDD, Ramal)
- Cada linha do grid exibe: Label (Nm_Ativo_Complemento) + TextBox (Descricao)

**DESTINO:** SUBSTITUÍDO
- Substituído por validação condicional FluentValidation (RN-RF025-008)
- Campos obrigatórios variam por Tipo_Ativo
- TI: Numero_Serie, Marca, Modelo, Valor_Aquisicao, Dt_Aquisicao
- Telecom: Numero_Linha, Operadora, Tipo_Plano
- Atributos técnicos: Sistema_Operacional, Processador, Memoria_RAM_GB, MAC_Address, Hostname

#### Botões de Ação

- **Voltar** (btVoltar) → ASSUMIDO
- **Novo** (btLimpar) → ASSUMIDO
- **Salvar** (btSalvar) → ASSUMIDO (API REST POST/PUT)
- **Excluir** (btDesativar) - Inativação lógica → SUBSTITUÍDO (Soft delete RN-RF025-013)
- **Config** (btConfiguracao) → DESCARTADO
- **PDF** (btPDF) → ASSUMIDO (gerar PDF lote QR Codes)
- **Dados** (btAbrir) - Abre modal "Dados Adicionais" → DESCARTADO

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

### Contexto

Sistema legado VB.NET utilizava Web Services SOAP básicos hospedados em IIS com autenticação Windows integrada. Estrutura monolítica sem separação de camadas dificultava manutenção e testes.

**Endpoint Base**: `http://servidor/IControlIT/Ativo.asmx`
**Protocolo**: SOAP 1.1
**Autenticação**: Windows Authentication (NTLM/Kerberos)

### Métodos Principais

#### 1. CadastrarAtivo()

- **Entrada**: TipoAtivo, NumeroSerie, IdMarca, IdModelo, ValorAquisicao, DataAquisicao
- **Saída**: IdAtivo (INT) ou Exception
- **Lógica**: INSERT na tabela Ativo com validação básica (campos obrigatórios). Não gerava QR Code nem registrava movimentação inicial.
- **Problema**: Sem validação de número patrimônio único - duplicatas possíveis
- **DESTINO:** SUBSTITUÍDO - `POST /api/ativos` com geração automática QR Code (RN-RF025-002)

#### 2. AlocarAtivo()

- **Entrada**: IdAtivo, IdUsuario, Observacao
- **Saída**: Boolean (sucesso) ou Exception
- **Lógica**: UPDATE Ativo SET Usuario_Atual = @IdUsuario. Não validava se ativo estava disponível nem enviava notificação ao usuário.
- **Problema**: Sem registro de histórico - impossível saber quem usou antes
- **DESTINO:** SUBSTITUÍDO - `POST /api/ativos/{id}/alocar` com validação de transição, termo digital, notificação automática e registro imutável em Ativo_Movimentacao (RN-RF025-004 + RN-RF025-005)

#### 3. ConsultarAtivos()

- **Entrada**: Filtros opcionais (TipoAtivo, Status, IdMarca)
- **Saída**: Array de AtivoDto
- **Lógica**: SELECT com filtros dinâmicos. Query sem paginação - retornava todos os registros.
- **Problema**: Performance horrível com >500 ativos (timeout frequente)
- **DESTINO:** SUBSTITUÍDO - `GET /api/ativos?page=1&size=50` com paginação cursor-based, cache Redis 5min, filtros avançados

#### 4. BaixarAtivo()

- **Entrada**: IdAtivo, Motivo
- **Saída**: Boolean (sucesso)
- **Lógica**: UPDATE Ativo SET Status = 'Inativo', MotivoInativacao = @Motivo
- **Problema**: Sem workflow de aprovação - qualquer usuário podia baixar patrimônio de R$10k+
- **DESTINO:** SUBSTITUÍDO - `POST /api/ativos/{id}/baixar` com workflow aprovação 2 níveis (Gestor + Controller), justificativa mínima 50 chars, anexos obrigatórios (RN-RF025-010)

#### 5. GerarRelatorioInventario()

- **Entrada**: DataInicio, DataFim
- **Saída**: XML com lista de ativos e movimentações (se existissem)
- **Lógica**: Gerava XML malformado frequentemente (encoding UTF-8 quebrado)
- **Problema**: Frontend tinha que parsear XML manualmente - erros frequentes
- **DESTINO:** SUBSTITUÍDO - `GET /api/ativos/inventario/relatorio` retorna JSON estruturado + export PDF com gráficos Chart.js

### Limitações Críticas Identificadas

1. **Windows Auth Apenas**: Impossível usar de mobile apps ou sistemas externos (B2B)
   - **SOLUÇÃO MODERNA:** JWT Bearer authentication stateless
2. **SOAP Verboso**: Payloads 10-15x maiores que JSON equivalente
   - **SOLUÇÃO MODERNA:** REST API com compressão Gzip/Brotli (reduz 70%)
3. **Sem Versionamento**: Mudanças no WSDL quebravam clientes sem aviso
   - **SOLUÇÃO MODERNA:** OpenAPI v1/v2 com backward compatibility
4. **Processamento Síncrono**: Operações longas (relatórios, importações) causavam timeout HTTP
   - **SOLUÇÃO MODERNA:** Hangfire jobs background para operações longas
5. **Sem Retry Logic**: Falhas temporárias (rede, DB deadlock) resultavam em erro final
   - **SOLUÇÃO MODERNA:** Polly policy retry 3x com backoff exponencial
6. **Logs Insuficientes**: Impossível debug de problemas em produção
   - **SOLUÇÃO MODERNA:** Serilog logging estruturado JSON
7. **Sem Rate Limiting**: Cliente mal comportado podia derrubar servidor
   - **SOLUÇÃO MODERNA:** Rate limiting (100 req/min usuário, 500 req/min IP)

---

## 4. TABELAS LEGADAS

### Estrutura Legado Existente

Sistema legado tinha apenas 3 tabelas básicas:

#### Tabela: Ativo (Principal)

**Finalidade:** Armazenar dados básicos de ativos

**Campos:**
- Id_Ativo (INT, PK)
- Tipo (VARCHAR(50)) - Ex: Notebook, Smartphone
- Numero_Patrimonio (VARCHAR(50))
- Numero_Serie (VARCHAR(100))
- Marca (VARCHAR(100)) - SEM FK (denormalizado)
- Modelo (VARCHAR(100)) - SEM FK (denormalizado)
- Valor_Aquisicao (DECIMAL(18,2))
- Dt_Aquisicao (DATETIME)
- Status (VARCHAR(20)) - Apenas 'Ativo' ou 'Inativo'
- Usuario_Atual (VARCHAR(100)) - SEM FK (denormalizado)

**Problemas Identificados:**
- ❌ Sem campos de garantia (Dt_Garantia_Fim, Tipo_Garantia)
- ❌ Sem campos GPS (Latitude, Longitude)
- ❌ Sem QR Code (QR_Code_URL, QR_Code_Base64)
- ❌ Sem campos de depreciação (Metodo_Depreciacao, Valor_Atual_Depreciado, Dt_Ultima_Depreciacao)
- ❌ Sem multi-tenancy (Id_Fornecedor ausente)
- ❌ Sem auditoria (Created, CreatedBy, LastModified, LastModifiedBy ausentes)
- ❌ DELETE físico permitido (sem Fl_Ativo)

**DESTINO:** SUBSTITUÍDO
- Tabela redesenhada com 30+ campos novos (QR Code, GPS, Garantia, Depreciação, Características Técnicas)
- Multi-tenancy obrigatório (Id_Fornecedor)
- Auditoria completa (Created, CreatedBy, LastModified, LastModifiedBy)
- Soft delete (Fl_Ativo)
- FK normalizadas (Id_Marca, Id_Modelo, Id_Usuario_Responsavel)

#### Tabela: Marca

**Finalidade:** Normalização de marcas (Dell, HP, Lenovo)

**Campos:**
- Id_Marca (INT, PK)
- Nm_Marca (VARCHAR(100))

**Problemas:** Estrutura básica OK, mas sem multi-tenancy

**DESTINO:** ASSUMIDO
- Mantida com adição de Id_Fornecedor (multi-tenancy)
- Adição de auditoria (Created, CreatedBy)
- Soft delete (Fl_Ativo)

#### Tabela: Modelo

**Finalidade:** Normalização de modelos (Latitude 5420, ProBook 450)

**Campos:**
- Id_Modelo (INT, PK)
- Id_Marca (INT, FK) - Relacionamento com Marca
- Nm_Modelo (VARCHAR(100))

**Problemas:** Estrutura básica OK, mas sem multi-tenancy

**DESTINO:** ASSUMIDO
- Mantida com adição de Id_Fornecedor (multi-tenancy)
- Adição de auditoria (Created, CreatedBy)
- Soft delete (Fl_Ativo)

### Tabelas Ausentes no Legado (Criadas no Moderno)

1. **Ativo_Movimentacao** - Histórico completo (chain of custody) - NOVA
2. **Ativo_Depreciacao** - Log de cálculos mensais - NOVA
3. **Ativo_Inventario** - Registros de inventários físicos - NOVA
4. **Ativo_Garantia_Alerta** - Log de notificações de garantia - NOVA
5. **Ativo_Anexos** - Fotos, NFs, laudos técnicos - NOVA
6. **Ativo_Integracao_ERP** - Fila de sincronização SAP/TOTVS - NOVA
7. **Localizacao** - Hierarquia (Edifício → Andar → Sala) - NOVA

---

## 5. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

Regras NÃO documentadas encontradas no código VB.NET:

### RL-RN-001: Validação de Número de Série Opcional

**Localização:** Ativo.aspx.vb - Método btnSalvar_Click
**Descrição:** Campo Numero_Serie era opcional no legado, mas recomendado. Sistema permitia salvar ativo sem número de série, gerando duplicatas e dificuldade de rastreamento.
**DESTINO:** SUBSTITUÍDO
- Sistema moderno: Numero_Serie obrigatório para ativos TI (RN-RF025-008)
- Validação FluentValidation condicional baseada em Tipo_Ativo

### RL-RN-002: Atribuição Múltipla Permitida

**Localização:** Ativo.aspx.vb - Grid dtgUsuario
**Descrição:** Grid de consumidores permitia criar múltiplas linhas SEM validar se ativo já estava alocado. Resultado: mesmo ativo aparecia como "em uso" por 2 pessoas simultaneamente.
**DESTINO:** SUBSTITUÍDO
- Sistema moderno: Validação de transições de status (RN-RF025-003)
- Status "Alocado" impede nova alocação até devolução
- Histórico imutável em Ativo_Movimentacao garante chain of custody

### RL-RN-003: Status Binário Sem Workflow

**Localização:** Ativo.aspx.vb - Campo cboAtivoStatus
**Descrição:** Status era apenas "Ativo" ou "Inativo". Não diferenciava "em manutenção", "reservado", "perdido", "baixado". Causava confusão: ativo "inativo" poderia estar em manutenção (temporário) ou baixado (permanente).
**DESTINO:** SUBSTITUÍDO
- Sistema moderno: Enum com 6 estados (Disponivel, Alocado, Manutencao, Reservado, Perdido, Baixado)
- Grafo de transições válidas (RN-RF025-003)
- Estado "Baixado" é final (irreversível exceto para admin)

### RL-RN-004: Localização Texto Livre

**Localização:** Ativo.aspx - Campo txtEndereco
**Descrição:** Campo aceitava texto livre ("sala do João", "depósito do 2º andar", "filial SP"). Impossível gerar relatórios geográficos ou mapas. Buscas por localização eram manuais (LIKE '%sala%').
**DESTINO:** SUBSTITUÍDO
- Sistema moderno: Tabela Localizacao hierárquica (Edificio → Andar → Sala → Estacao)
- Geolocalização GPS (Latitude, Longitude) capturada via mobile app
- Validação obrigatória de GPS para inventário mobile (RN-RF025-009)

### RL-RN-005: Termo de Responsabilidade Manual

**Localização:** Ativo.aspx.vb - Botão btTermo
**Descrição:** Termo gerado como documento Word (.doc) baixado localmente. Usuário imprimia, assinava à mão e digitalizava (scanner). Processo lento (2-3 dias) e sem rastreabilidade digital.
**DESTINO:** SUBSTITUÍDO
- Sistema moderno: Termo de responsabilidade digital via DocuSign/Clicksign API
- Assinatura eletrônica com validade jurídica
- Notificação automática ao usuário responsável (RN-RF025-004)
- Rastreamento de aceite em tempo real

### RL-RN-006: Depreciação Manual

**Localização:** N/A (processado fora do sistema em Excel)
**Descrição:** Controlador exportava CSV mensal com ativos, abria planilha Excel com fórmulas de depreciação linear. Erros frequentes: fórmula copiada errada, ativo esquecido, taxa desatualizada.
**DESTINO:** SUBSTITUÍDO
- Sistema moderno: Hangfire job automático mensal (dia 1 às 02:00 UTC)
- 3 métodos de depreciação (Linear, Acelerada, Soma Dígitos)
- Integração automática com ERP (SAP, TOTVS) via API REST
- Log de cálculos em Ativo_Depreciacao para auditoria (RN-RF025-006)

### RL-RN-007: Inventário Físico Manual

**Localização:** N/A (processo offline com checklist papel)
**Descrição:** 2 colaboradores levavam 2 semanas para inventariar 800 ativos. Checklist impresso, conferência física, digitação manual no sistema. Taxa de erro: ~5% (ativos não encontrados mas marcados como OK).
**DESTINO:** SUBSTITUÍDO
- Sistema moderno: App mobile MAUI (Android/iOS) com scan QR Code
- Captura GPS obrigatória (precisão ≤ 20m) para prevenir fraude (RN-RF025-009)
- Foto do ativo no momento do inventário
- Sincronização automática online/offline
- Redução de tempo: 2 semanas → 2 dias (80%)

### RL-RN-008: IMEI Sem Validação

**Localização:** Ativo.aspx - Campo txtSimCard (usado para IMEI)
**Descrição:** Campo aceitava qualquer texto. IMEIs inválidos ou duplicados eram cadastrados. Sem validação de checksum (Luhn) ou consulta Anatel.
**DESTINO:** SUBSTITUÍDO
- Sistema moderno: Validação IMEI obrigatória para smartphones (RN-RF025-011)
- 15 dígitos numéricos
- Algoritmo de Luhn (checksum)
- Consulta API Anatel para verificar blacklist
- Salvar IMEI_Status (Ativo, Bloqueado, Irregular)

---

## 6. GAP ANALYSIS (LEGADO x RF MODERNO)

| Item | Legado | RF Moderno | Status | Justificativa |
|------|--------|------------|--------|---------------|
| **Número Patrimônio** | Manual, duplicatas possíveis | Gerado automaticamente PAT-{TipoAbrev}-{Ano}-{Sequencial} | SUBSTITUÍDO | Garantir unicidade global (RN-RF025-001) |
| **QR Code** | Etiquetas papel (30% falha 6 meses) | QR Code 300x300px gerado automaticamente | NOVA | Rastreabilidade via mobile app (RN-RF025-002) |
| **Status** | Binário (Ativo/Inativo) | Enum 6 estados com grafo transições | SUBSTITUÍDO | Workflow preciso (RN-RF025-003) |
| **Histórico Movimentações** | Inexistente | Tabela Ativo_Movimentacao imutável | NOVA | Chain of custody completa (RN-RF025-005) |
| **Alocação** | UPDATE direto sem validação | Validação transição + termo digital + notificação | SUBSTITUÍDO | Compliance e rastreabilidade (RN-RF025-004) |
| **Depreciação** | Manual em Excel (erros frequentes) | Hangfire job automático mensal 3 métodos | NOVA | Compliance contábil 100% (RN-RF025-006) |
| **Alertas Garantia** | Inexistente | Job diário 30/60/90 dias Email+Push+In-App | NOVA | Economia R$80k/ano (RN-RF025-007) |
| **Validação IMEI** | Sem validação | Luhn + Anatel API blacklist | NOVA | Prevenir cadastro smartphones roubados (RN-RF025-011) |
| **Inventário** | Manual 2 semanas papel | App mobile MAUI scan QR Code GPS | NOVA | Redução 80% tempo (RN-RF025-009 + RN-RF025-015) |
| **Localização** | Texto livre sem estrutura | Hierarquia Edificio→Andar→Sala + GPS | SUBSTITUÍDO | Mapas interativos e relatórios geográficos |
| **Baixa Patrimonial** | Qualquer usuário, sem aprovação | Workflow 2 níveis Gestor+Controller | NOVA | Compliance (RN-RF025-010) |
| **Multi-Tenancy** | 1 banco por cliente (físico) | Id_Fornecedor em todas tabelas (lógico) | NOVA | Escalabilidade SaaS (RN-RF025-012) |
| **Soft Delete** | DELETE físico | Fl_Ativo (exclusão lógica) | NOVA | Preservação histórico 7 anos (RN-RF025-013) |
| **Integração ERP** | Export CSV manual mensal | Webhook outbound + API REST inbound | NOVA | Sincronização tempo real (RN-RF025-014) |
| **Autenticação** | Windows Auth (NTLM) | JWT Bearer stateless | SUBSTITUÍDO | Compatibilidade mobile/B2B |
| **Web Services** | SOAP 1.1 verboso | REST API JSON comprimido | SUBSTITUÍDO | Performance 70% melhor |
| **Auditoria** | Inexistente | Created, CreatedBy, LastModified, LastModifiedBy | NOVA | Compliance LGPD |

---

## 7. DECISÕES DE MODERNIZAÇÃO

### Decisão 1: QR Code em vez de Etiquetas Papel

**Motivo:** Etiquetas papel descolavam (30% falha após 6 meses), ilegíveis após uso intenso. QR Code permite scan via mobile app, rastreamento GPS, fotos.

**Impacto:** ALTO
- Custo inicial R$2.500 (impressão gráfica 800 QR Codes em material durável)
- ROI em 3 meses (elimina reimpressões constantes)
- Redução 80% tempo inventário (2 semanas → 2 dias)

### Decisão 2: Depreciação Automática via Hangfire

**Motivo:** Depreciação manual em Excel causava erros (fórmulas, ativos esquecidos, taxas desatualizadas). Controlador gastava 8h/mês calculando manualmente.

**Impacto:** ALTO
- Elimina 100% erros de cálculo manual
- Libera 8h/mês do controlador (custo: ~R$1.200/mês)
- Integração automática com ERP (SAP, TOTVS) elimina descompasso contábil

### Decisão 3: Workflow de Aprovação para Baixa Patrimonial

**Motivo:** Qualquer usuário podia baixar ativos de R$10k+ no legado sem aprovação. Casos de baixas indevidas (erro humano ou má-fé).

**Impacto:** MÉDIO
- Compliance contábil
- Auditoria completa (quem aprovou, quando, justificativa)
- Redução fraudes patrimoniais

### Decisão 4: App Mobile MAUI para Inventário

**Motivo:** Inventário manual com checklist papel levava 2 semanas (2 colaboradores). Taxa de erro 5% (ativos marcados OK mas não encontrados).

**Impacto:** MUITO ALTO
- Redução 80% tempo (2 semanas → 2 dias)
- GPS obrigatório previne fraude ("inventário remoto")
- Foto evidencia estado físico do ativo
- Sincronização online/offline

### Decisão 5: Multi-Tenancy Lógico (Id_Fornecedor)

**Motivo:** Legado usava 1 banco SQL Server por cliente (multi-tenant físico). Manutenção custosa (backups, migrations, monitoramento).

**Impacto:** ALTO
- Redução custos infraestrutura (1 banco único vs 50+ bancos)
- Facilita migrations (1 script vs 50+)
- Isolamento garantido por Row-Level Security + Query Filter EF Core

### Decisão 6: Soft Delete Obrigatório

**Motivo:** Legado permitia DELETE físico. Dados perdidos para sempre. Auditorias requeriam backup restauração.

**Impacto:** MÉDIO
- Compliance LGPD (retenção 7 anos)
- Histórico completo para auditorias
- Restauração ativo via API (admin)

### Decisão 7: Validação IMEI para Smartphones

**Motivo:** Cadastro de smartphones roubados (IMEI bloqueado Anatel) causava problemas legais.

**Impacto:** BAIXO
- Previne compra smartphones irregulares
- Alertas automáticos IMEI bloqueado (permite cadastro mas com flag)

---

## 8. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| **Perda de Histórico de Movimentações** | ALTO | CERTO | Histórico anterior à migração NÃO pode ser recuperado (dados nunca existiram). Flag `Migrado_Legado=TRUE` marca ativos sem histórico completo. |
| **QR Codes Não Gerados Corretamente** | MÉDIO | BAIXO | Job Hangfire gera 800 QR Codes em lote. Validação pós-migração garante 100% gerados. PDF consolidado para impressão. |
| **Depreciação Retroativa Incorreta** | ALTO | MÉDIO | Script calcula depreciação desde `Dt_Aquisicao` com método Linear (default) e taxa 20%. Admin pode recalcular manualmente. |
| **Resistência Usuários ao App Mobile** | MÉDIO | MÉDIO | Treinamento obrigatório 2h. App intuitivo (scan QR Code = 1 tap). Inventário web permitido mas marca flag `InventarioRemoto=TRUE`. |
| **Integração ERP Falhar** | ALTO | BAIXO | Polly retry 3x + DLQ (RabbitMQ). Eventos falhos reprocessados manualmente. Monitoring alertas em tempo real. |
| **GPS Indisponível em Locais Fechados** | MÉDIO | MÉDIO | Inventário web permite localização manual (sem GPS) mas marca flag `InventarioRemoto=TRUE`. Admin pode revisar inventários remotos. |
| **Duplicatas de Número Patrimônio na Migração** | ALTO | BAIXO | Script validação pré-migração detecta duplicatas. Números corrigidos manualmente antes de rodar migração. |
| **Usuários Não Aceitarem Termo Digital** | MÉDIO | BAIXO | Termo enviado automaticamente ao alocar. Reenvio automático se não aceito em 3 dias. Sem aceite = sem ativo. |

---

## 9. RASTREABILIDADE

| Elemento Legado | Referência RF Moderno | Status Migração |
|-----------------|----------------------|-----------------|
| Ativo.aspx (tela cadastro) | RF-025 - Seção 4 (Funcionalidades 1-4) | SUBSTITUÍDO |
| Grid dtgUsuario (atribuições) | RN-RF025-004 + RN-RF025-005 (Ativo_Movimentacao) | SUBSTITUÍDO |
| Grid dtgDadosComplemento (campos dinâmicos) | RN-RF025-008 (Validação FluentValidation condicional) | SUBSTITUÍDO |
| CadastrarAtivo (SOAP) | POST /api/ativos | SUBSTITUÍDO |
| AlocarAtivo (SOAP) | POST /api/ativos/{id}/alocar | SUBSTITUÍDO |
| ConsultarAtivos (SOAP) | GET /api/ativos?page=1&size=50 | SUBSTITUÍDO |
| BaixarAtivo (SOAP) | POST /api/ativos/{id}/baixar | SUBSTITUÍDO |
| GerarRelatorioInventario (SOAP XML) | GET /api/ativos/inventario/relatorio | SUBSTITUÍDO |
| Tabela Ativo (3 tabelas básicas) | Ativo + 7 tabelas novas | SUBSTITUÍDO/EXPANDIDO |
| Tabela Marca | Marca (com multi-tenancy) | ASSUMIDO |
| Tabela Modelo | Modelo (com multi-tenancy) | ASSUMIDO |
| Depreciação manual Excel | Hangfire job automático (RN-RF025-006) | SUBSTITUÍDO |
| Inventário papel 2 semanas | App mobile MAUI (RN-RF025-009 + RN-RF025-015) | SUBSTITUÍDO |
| Etiquetas papel | QR Code 300x300px (RN-RF025-002) | SUBSTITUÍDO |
| Termo responsabilidade Word | Termo digital DocuSign/Clicksign (RN-RF025-004) | SUBSTITUÍDO |

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|--------|------|-----------|-------|
| 1.0 | 2025-12-30 | Criação RL-RF025 com separação completa de memória legado. 7 seções obrigatórias, 100% dos itens com destino definido (ASSUMIDO/SUBSTITUÍDO/DESCARTADO). Documentação de problemas arquiteturais, telas ASPX, webservices SOAP, tabelas legadas, regras implícitas, gap analysis e decisões de modernização. | Agência ALC - alc.dev.br |
