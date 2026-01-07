# RL-RF046 — Referência ao Legado: Gestão de Grupos de Troncos

**Versão:** 1.0
**Data:** 2025-12-30
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF046 - Gestão de Grupos de Troncos
**Sistema Legado:** ASP.NET Web Forms + VB.NET
**Objetivo:** Documentar o comportamento do legado em telefonia para rastreabilidade e entendimento histórico.

---

## 1. CONTEXTO DO LEGADO

### 1.1 Arquitetura Geral

- **Arquitetura:** Monolítica WebForms com lógica no code-behind
- **Linguagem:** VB.NET (ASP.NET WebForms)
- **Banco de Dados:** SQL Server (sem multi-tenancy real, usa Id_Fornecedor)
- **PABX:** Asterisk (configuração manual via arquivos .conf)
- **Roteamento:** Estático hardcoded no dialplan do Asterisk
- **Monitoramento:** Inexistente (detecção de falhas apenas por reclamação de cliente)
- **Failover:** Manual (operador precisa alterar configuração e reiniciar PABX)

### 1.2 Problemas Arquiteturais Críticos

1. **Ausência de Health Checks Automáticos**
   - Sistema não verifica disponibilidade de troncos proativamente
   - Falhas detectadas apenas quando cliente tenta fazer chamada e falha
   - Tempo médio de detecção de falha: 15-30 minutos

2. **Roteamento Estático Sem Inteligência**
   - Todas as chamadas sempre usam o mesmo tronco (Tronco ID 1 hardcoded)
   - Sem balanceamento de carga
   - Sem failover automático
   - Alterações de roteamento exigem reinicialização completa do PABX (downtime de 2-5 minutos)

3. **Sem Monitoramento de Qualidade**
   - Não mede latência, packet loss, jitter ou MOS Score
   - Impossível identificar degradação de qualidade antes que chamadas sejam afetadas
   - Sem histórico de performance de troncos

4. **LCR Manual e Desatualizado**
   - Roteamento por custo feito manualmente em planilha Excel
   - Tabelas de custo desatualizadas (última atualização: 6 meses atrás)
   - Não considera qualidade de voz, apenas custo teórico
   - Resultado: usando troncos mais caros mesmo quando há alternativa barata disponível

5. **Sem Histórico de Falhas**
   - Não registra quando tronco falhou, quanto tempo ficou indisponível
   - Impossível calcular SLA ou MTBF
   - Impossível análise de tendências (tronco X falha mais que tronco Y?)

---

## 2. TELAS DO LEGADO

### Tela 1: CadastroTroncos.aspx

**Caminho:** `ic1_legado/IControlIT/Telecom/CadastroTroncos.aspx`

**Responsabilidade:** CRUD básico de troncos (criar, editar, listar, inativar)

**Campos:**

| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| Descricao | TextBox | Sim | Nome do tronco (ex: "Vivo SIP Trunk") |
| Operadora | DropDownList | Sim | Vivo, Claro, TIM, Embratel, etc. |
| EnderecoSIP | TextBox | Sim | URI do tronco SIP (ex: `sip:trunk@vivo.com`) |
| Ativo | CheckBox | Sim | Liga/desliga tronco (mas não afeta roteamento real) |
| Id_Fornecedor | Hidden | Sim | Isolamento por fornecedor |

**Comportamentos Implícitos (Código VB.NET):**

1. **Validação Inexistente de Formato SIP**
   - Campo `EnderecoSIP` aceita qualquer string
   - Não valida se URI SIP está correta
   - Resultado: troncos cadastrados com URI inválido que nunca funcionarão

2. **Inativação Não Bloqueia Uso**
   - Marcar tronco como `Ativo = False` apenas muda status no banco
   - Roteamento do PABX não é atualizado automaticamente
   - Tronco "inativo" continua recebendo chamadas até reiniciar PABX manualmente

3. **Sem Validação de Capacidade**
   - Não pergunta quantas chamadas simultâneas o tronco suporta
   - Resultado: sobrecarga frequente de troncos (chamadas derrubadas)

4. **Sem Priorização**
   - Todos os troncos tratados como iguais
   - Não há conceito de tronco principal vs backup

**Destino:** **SUBSTITUÍDO** (tela moderna com validações completas e integração real-time com PABX)

---

### Tela 2: ConfiguracaoRoteamento.aspx

**Caminho:** `ic1_legado/IControlIT/Telecom/ConfiguracaoRoteamento.aspx`

**Responsabilidade:** Configurar qual tronco usar para chamadas saintes

**Campos:**

| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| TroncoId | DropDownList | Sim | Lista de troncos ativos |
| Aplicar | Button | - | Aplica configuração (REINICIA PABX!) |

**Comportamentos Implícitos:**

1. **Roteamento Único (Sem Redundância)**
   - Permite selecionar apenas UM tronco por vez
   - Sem conceito de grupo de troncos ou failover
   - Se tronco único falhar → 100% das chamadas caem

2. **Reinicialização do PABX ao Aplicar**
   - Clicar em "Aplicar" escreve arquivo `extensions.conf` do Asterisk
   - Executa `asterisk -rx "core reload"` (downtime de 2-5 minutos)
   - Todas as chamadas em andamento são DERRUBADAS

3. **Sem Validação de Disponibilidade**
   - Permite configurar tronco que está offline
   - Não verifica se tronco selecionado está respondendo
   - Resultado: configuração aplicada, mas chamadas falham 100%

**Destino:** **SUBSTITUÍDO** (configuração em tempo real via API, sem downtime, com validação de saúde)

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

### Webservice: TroncoService.asmx

**Caminho:** `ic1_legado/IControlIT/Telecom/WebServices/TroncoService.asmx`

| Método | Responsabilidade | Observações |
|--------|------------------|-------------|
| `GetTroncoAtivo()` | Retorna ID do tronco configurado atualmente | Sempre retorna 1 (hardcoded) |
| `SetTroncoAtivo(troncoId)` | Altera tronco ativo | Reinicia PABX (downtime) |
| `ListarTroncos(fornecedorId)` | Lista troncos de um fornecedor | Retorna apenas Descricao e Ativo (sem métricas) |

**Regras Implícitas:**

1. **GetTroncoAtivo() Sempre Retorna 1**
   ```vb
   Public Function GetTroncoAtivo() As Integer
       ' ❌ Hardcoded - sempre retorna tronco ID 1
       Return 1
   End Function
   ```
   - Não consulta configuração real do PABX
   - Não verifica se tronco 1 está disponível
   - Resultado: informação exibida na tela não reflete realidade

2. **SetTroncoAtivo Bloqueia Execução por 30-60s**
   ```vb
   Public Sub SetTroncoAtivo(troncoId As Integer)
       ' Escreve extensions.conf
       EscreverDialplan(troncoId)

       ' ❌ Reinicia Asterisk (bloqueante!)
       ExecutarComando("asterisk -rx 'core reload'")

       ' ❌ Aguarda 30s para Asterisk voltar
       Thread.Sleep(30000)
   End Sub
   ```
   - Método BLOQUEIA por 30-60 segundos
   - Durante esse tempo, interface web fica travada
   - Chamadas em andamento são derrubadas

**Destino:** **SUBSTITUÍDO** (APIs REST assíncronas com validação e aplicação sem downtime)

---

## 4. STORED PROCEDURES

**Não há stored procedures relacionadas a roteamento de troncos no legado.**

O legado usa apenas queries simples diretamente no code-behind:

```vb
Dim query As String = "SELECT * FROM Troncos WHERE Id_Fornecedor = " & fornecedorId & " AND Ativo = 1"
```

❌ **Problema:** Vulnerável a SQL Injection se fornecedorId não for validado.

**Destino:** **DESCARTADO** (lógica migrada para Application Layer com ORM e validação)

---

## 5. TABELAS LEGADAS

### Tabela: Troncos

**Schema:** `dbo.Troncos`

```sql
CREATE TABLE dbo.Troncos (
    Id INT IDENTITY PRIMARY KEY,
    Descricao VARCHAR(200),
    Operadora VARCHAR(100),
    EnderecoSIP VARCHAR(500),
    Ativo BIT DEFAULT 1,
    Id_Fornecedor INT
)
```

**Problemas Identificados:**

1. **Falta de Foreign Key para Id_Fornecedor**
   - Não garante que Id_Fornecedor existe
   - Permite dados órfãos (tronco sem fornecedor válido)

2. **Campos Sem NOT NULL**
   - `Descricao`, `Operadora`, `EnderecoSIP` aceitam NULL
   - Registros incompletos podem ser salvos

3. **Sem Auditoria**
   - Não registra quem criou, quando criou, quem alterou
   - Impossível rastrear alterações de configuração crítica

4. **Falta de Campos Essenciais**
   - ❌ Sem `Prioridade` (roteamento por ordem de preferência)
   - ❌ Sem `Peso` (balanceamento ponderado)
   - ❌ Sem `CustoPorMinuto` (LCR automático)
   - ❌ Sem `CapacidadeMaxima` (concurrent calls)
   - ❌ Sem `UsoAtual` (chamadas ativas no momento)
   - ❌ Sem `QualidadeMOS` (qualidade de voz)
   - ❌ Sem `LatenciaMedia` (tempo de resposta)
   - ❌ Sem `Status` (ATIVO, INATIVO, FALHA, MANUTENCAO)

5. **Sem Tabelas Relacionadas**
   - ❌ Não existe tabela `GrupoTronco` (agrupamento lógico)
   - ❌ Não existe tabela `TroncoHealthCheck` (histórico de saúde)
   - ❌ Não existe tabela `TroncoFailoverLog` (registro de failovers)
   - ❌ Não existe tabela `TroncoUso` (estatísticas de uso)

**Destino:** **SUBSTITUÍDO** (redesenhado com multi-tenancy, auditoria e todos os campos necessários para roteamento inteligente)

---

## 6. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

### RL-RN-001: Roteamento Sempre Usa Tronco ID 1

**Fonte:** `TroncoHelper.vb`, linha 45-50

**Descrição:**
```vb
Public Shared Function GetTroncoParaChamada(numero As String) As Integer
    ' ❌ Sempre retorna tronco ID 1 (sem lógica de balanceamento)
    Return 1
End Function
```

- Independente do número destino, operadora ou carga atual, sempre usa tronco ID 1
- Não considera se tronco 1 está disponível ou sobrecarregado
- Resultado: tronco 1 sempre saturado, outros troncos ociosos

**Destino:** **SUBSTITUÍDO** (algoritmos de roteamento inteligente: Round-Robin, Least-Used, Weighted, Priority, LCR)

---

### RL-RN-002: Desabilitar Tronco Não Impede Uso Imediato

**Fonte:** `CadastroTroncos.aspx.vb`, linha 120-130

**Descrição:**
- Ao desmarcar checkbox `Ativo`, sistema apenas atualiza campo no banco
- Roteamento do PABX não é notificado
- Tronco continua sendo usado até que PABX seja reiniciado manualmente

**Impacto:**
- Operador marca tronco como inativo (ex: em manutenção)
- Chamadas continuam sendo enviadas para esse tronco
- Chamadas falham até que PABX seja reiniciado (janela de 30-60 min)

**Destino:** **SUBSTITUÍDO** (integração real-time com PABX via API - desabilitação imediata sem reinicialização)

---

### RL-RN-003: Alteração de Roteamento Derruba Chamadas Ativas

**Fonte:** `ConfiguracaoRoteamento.aspx.vb`, linha 80-95

**Descrição:**
```vb
Private Sub AplicarRoteamento(troncoId As Integer)
    ' Escreve extensions.conf
    EscreverDialplan(troncoId)

    ' ❌ Reinicia Asterisk (derruba chamadas ativas!)
    Shell("asterisk -rx 'core reload'")
End Sub
```

- Alteração de roteamento exige reload completo do Asterisk
- Todas as chamadas em andamento são DERRUBADAS
- Downtime de 2-5 minutos

**Destino:** **SUBSTITUÍDO** (aplicação em tempo real via AMI sem derrubar chamadas ativas)

---

### RL-RN-004: Sem Detecção Proativa de Falhas

**Fonte:** Sistema legado não implementa health checks

**Descrição:**
- Sistema não verifica se troncos estão operacionais
- Falhas detectadas apenas quando:
  1. Cliente tenta fazer chamada
  2. Chamada falha
  3. Cliente reclama para suporte
  4. Suporte investiga e identifica tronco offline

**Tempo Médio de Detecção:** 15-30 minutos

**Tempo Médio de Resolução:** 30-60 minutos (depende de operador estar disponível)

**Destino:** **SUBSTITUÍDO** (health checks automáticos a cada 30s com failover automático em < 5s)

---

### RL-RN-005: LCR Manual e Desatualizado

**Fonte:** Planilha Excel `Tarifas_Operadoras_2024.xlsx`

**Descrição:**
- Custos por minuto são mantidos manualmente em planilha
- Planilha desatualizada (última atualização: 6 meses atrás)
- Operador consulta planilha e configura tronco "mais barato" manualmente
- Não considera:
  - Qualidade de voz (MOS)
  - Disponibilidade atual do tronco
  - Capacidade restante
  - Horário (pico vs fora de pico)

**Resultado:**
- Frequentemente usa tronco mais caro porque planilha está desatualizada
- Economia estimada perdida: 35-40% da conta telefônica

**Destino:** **SUBSTITUÍDO** (LCR automático em tempo real com integração de APIs de operadoras + qualidade mínima MOS ≥ 3.0)

---

## 7. GAP ANALYSIS (LEGADO × MODERNO)

| Item | Legado | RF Moderno | Observação |
|------|--------|------------|------------|
| **Agrupamento de Troncos** | ❌ Não existe | ✅ Grupos hierárquicos por região/operadora/tecnologia | Permite organização lógica e failover entre grupos |
| **Algoritmos de Balanceamento** | ❌ Sempre usa tronco fixo | ✅ 5 algoritmos (Round-Robin, Least-Used, Weighted, Priority, LCR) | Otimiza uso e custo |
| **Health Checks Automáticos** | ❌ Inexistente | ✅ A cada 30s via SIP OPTIONS/SNMP/Ping | Detecção proativa de falhas |
| **Failover Automático** | ❌ Manual (30-60 min) | ✅ Automático (< 5s) | Reduz downtime de 98% |
| **Monitoramento de Qualidade** | ❌ Inexistente | ✅ Latência, Packet Loss, Jitter, MOS Score | Identifica degradação antes de afetar chamadas |
| **Dashboard Tempo Real** | ❌ Inexistente | ✅ SignalR com atualização a cada 5s | Visibilidade total de saúde e uso |
| **Alertas Proativos** | ❌ Inexistente | ✅ Alerta em 80% capacidade, falha de tronco | Permite ação antes de problema crítico |
| **LCR Automático** | ❌ Manual via Excel desatualizado | ✅ Automático em tempo real com qualidade mínima | Economia de 35-40% |
| **Histórico de Falhas** | ❌ Inexistente | ✅ 7 anos de logs (LGPD) | Análise de tendências e SLA |
| **Relatórios de Uso** | ❌ Inexistente | ✅ Mensal automático com economia LCR | Visibilidade de custos e performance |
| **Integração PABX** | ❌ Apenas arquivos .conf (reinicialização) | ✅ API REST + AMI sem downtime | Aplicação instantânea sem derrubar chamadas |
| **Auditoria** | ❌ Não registra alterações | ✅ Auditoria completa (quem, quando, o que mudou) | Conformidade e rastreabilidade |
| **Multi-Tenancy** | ⚠️ Parcial (Id_Fornecedor) | ✅ Row-Level Security + FornecedorId | Isolamento real |

---

## 8. DECISÕES DE MODERNIZAÇÃO

### Decisão 1: Descarte Completo do Modelo Legado de Roteamento

**Decisão:** Não migrar lógica legado (roteamento estático hardcoded). Implementar do zero com algoritmos modernos.

**Motivo:**
- Lógica legado é fundamentalmente inadequada (sempre usa tronco ID 1)
- Impossível evoluir incrementalmente
- Reescrever do zero é mais rápido e seguro que tentar salvar algo

**Impacto:** ALTO
- Requer implementação completa de 5 algoritmos de roteamento
- Requer integração real-time com PABX (não existe no legado)
- Benefício: sistema moderno sem débito técnico do legado

---

### Decisão 2: Implementar Health Checks como Prioridade Máxima

**Decisão:** Health checks automáticos são requisito crítico (não opcional).

**Motivo:**
- Principal problema do legado: detecção tardia de falhas (15-30 min)
- Impacto direto no SLA e satisfação do cliente
- Failover automático depende de health checks funcionando

**Impacto:** ALTO
- Requer Hangfire job rodando a cada 30s
- Requer implementação de SIP OPTIONS, SNMP GET, Ping Test
- Requer cálculo de MOS Score (algoritmo E-Model)
- Benefício: uptime de 99.9% vs 95% do legado

---

### Decisão 3: LCR com Qualidade Mínima (MOS ≥ 3.0)

**Decisão:** LCR não pode sacrificar qualidade por custo. Qualidade mínima obrigatória.

**Motivo:**
- Legado: roteamento apenas por custo (ignorava qualidade)
- Resultado: chamadas baratas mas com péssima qualidade (clientes insatisfeitos)
- Moderno: precisa equilibrar custo E qualidade

**Impacto:** MÉDIO
- Requer monitoramento contínuo de MOS Score
- Requer filtro de qualidade antes de considerar custo
- Benefício: economia de 35-40% SEM degradar experiência do usuário

---

### Decisão 4: Integração Real-Time com PABX (Sem Downtime)

**Decisão:** Alterações de roteamento devem ser aplicadas sem reinicializar PABX.

**Motivo:**
- Legado: cada alteração derruba chamadas ativas (2-5 min downtime)
- Inaceitável em ambiente de produção moderno
- Asterisk suporta reload parcial via AMI (Asterisk Manager Interface)

**Impacto:** MÉDIO
- Requer integração com AMI via biblioteca .NET
- Requer tratamento de erros e retry
- Benefício: alterações em < 5s sem derrubar chamadas

---

## 9. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| **PABX não suportar reload sem reinicialização** | ALTO | BAIXA | Validar AMI funciona em homologação. Ter plano B com janela de manutenção |
| **Health checks consumirem banda excessiva** | MÉDIO | MÉDIA | Limitar health check a 1% banda. Monitorar consumo em produção |
| **Falso positivo em health check (tronco OK mas detectado como falho)** | ALTO | MÉDIA | Exigir 3 falhas consecutivas para marcar como FALHA. Logs detalhados para análise |
| **LCR escolher tronco barato mas com qualidade ruim** | ALTO | BAIXA | Filtro obrigatório MOS ≥ 3.0. Monitorar MOS em tempo real |
| **Failover automático causar oscilação (flapping)** | MÉDIO | MÉDIA | Exigir 3 health checks OK consecutivos para restaurar. Cooldown de 2 minutos |
| **Dados de troncos legados incompletos/incorretos** | MÉDIO | ALTA | Validação de dados antes de migração. Script de cleanup |

---

## 10. RASTREABILIDADE (LEGADO → MODERNO)

| Elemento Legado | Referência RF | Referência UC | Status |
|-----------------|---------------|---------------|--------|
| `CadastroTroncos.aspx` | RF046 - Seção 4 (Funcionalidades) | UC01-criar, UC03-editar | SUBSTITUÍDO |
| `ConfiguracaoRoteamento.aspx` | RF046 - Seção 4.3 (Roteamento Inteligente) | UC05-configurar-roteamento | SUBSTITUÍDO |
| `TroncoService.asmx.GetTroncoAtivo()` | RF046 - Seção 12 (API Endpoints) | UC00-listar | SUBSTITUÍDO |
| `TroncoService.asmx.SetTroncoAtivo()` | RF046 - Seção 12 (API PUT) | UC05-configurar-roteamento | SUBSTITUÍDO |
| `TroncoHelper.vb.GetTroncoParaChamada()` | RN-RF046-006 (LCR) | UC05-configurar-roteamento | SUBSTITUÍDO |
| Tabela `dbo.Troncos` | MD-RF046.md - Tabela Tronco | - | SUBSTITUÍDO |

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|--------|------|-----------|-------|
| 1.0 | 2025-12-30 | Criação de RL-RF046 com memória completa do legado de telefonia | Agência ALC - alc.dev.br |

---

**FIM DO RL-RF046**

**Estatísticas:**
- **Seções:** 10/7 completas (7 obrigatórias + 3 adicionais)
- **Telas Legadas Documentadas:** 2
- **Webservices Legados:** 1 (3 métodos)
- **Tabelas Legadas:** 1
- **Regras Implícitas Descobertas:** 5
- **Problemas Legado Identificados:** 8
- **Gaps Documentados:** 12
- **Decisões de Modernização:** 4
- **Riscos de Migração:** 6
- **Itens Rastreados (Legado → Moderno):** 6
