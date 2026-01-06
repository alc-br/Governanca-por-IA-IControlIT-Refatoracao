# RL-RF068 — Referência ao Legado - Inventário Cíclico e Auditoria de Estoque

**Versão:** 1.0
**Data:** 2025-12-30
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF-068
**Sistema Legado:** VB.NET + ASP.NET Web Forms + SQL Server
**Objetivo:** Documentar o comportamento do legado que serve de base para a refatoração, garantindo rastreabilidade, entendimento histórico e mitigação de riscos.

---

## 1. CONTEXTO DO LEGADO

Descreve o cenário geral do sistema legado de inventário.

- **Arquitetura:** Monolítica WebForms
- **Linguagem / Stack:** VB.NET + ASP.NET Web Forms + SQL Server + stored procedures
- **Banco de Dados:** SQL Server (tabelas `Estoque_Inventario`, `Estoque_Inventario_Item`)
- **Multi-tenant:** Parcial (campo `Id_Fornecedor` ausente em tabelas de inventário)
- **Auditoria:** Inexistente (sem campos Created, CreatedBy, LastModified)
- **Classificação ABC:** Inexistente (manual em planilhas Excel, não automatizado)
- **Contagem:** 100% manual via planilhas Excel, sem app mobile
- **Bloqueio de almoxarifado:** Não implementado (movimentações permitidas durante inventário)
- **Aprovação de ajustes:** Inexistente (ajustes aplicados diretamente sem workflow)
- **Integração ERP:** Inexistente (lançamentos contábeis manuais)
- **Relatórios:** PDF genérico, não compatível com ISO 9001
- **Configurações:** Web.config, stored procedures no banco

---

## 2. TELAS DO LEGADO

### Tela: TelaInventario.aspx

- **Caminho:** `D:\IC2\ic1_legado\IControlIT\Estoque\TelaInventario.aspx`
- **Responsabilidade:** CRUD básico de inventários (Create, Read, Update, Delete)

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|------|------|-------------|-------------|
| `Id_Almoxarifado` | DropDownList | Sim | Almoxarifado sem validação de status ativo |
| `Tipo_Inventario` | DropDownList | Sim | Geral, Parcial (sem "Cíclico") |
| `Dt_Inicio` | TextBox (Calendar) | Sim | Data de início |
| `Dt_Fim` | TextBox (Calendar) | Não | Data de fim (preenchida manualmente) |
| `Status` | Label | Não | "Em_Andamento", "Concluido" (sem validação) |

#### Comportamentos Implícitos

- **Tipo "Cíclico" inexistente:** Legado não implementa inventário cíclico ABC
- **Sem bloqueio de almoxarifado:** Permite movimentações durante inventário (inconsistência)
- **Sem validação de almoxarifado inativo:** Permite criar inventário para almoxarifado descontinuado
- **Deleção física:** Delete remove registro do banco (perda de histórico)
- **Status manual:** Status não atualizado automaticamente (usuário altera via combo)

---

### Tela: TelaInventario_Contar.aspx

- **Caminho:** `D:\IC2\ic1_legado\IControlIT\Estoque\TelaInventario_Contar.aspx`
- **Responsabilidade:** Registrar contagem manual de itens

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|------|------|-------------|-------------|
| `Id_Ativo` | DropDownList | Sim | Seleção manual, sem barcode scan |
| `Qtd_Sistema` | TextBox (ReadOnly) | - | Quantidade no sistema (exibição) |
| `Qtd_Contada` | TextBox | Sim | Quantidade contada manualmente |
| `Observacao` | TextArea | Não | Observação livre |

#### Comportamentos Implícitos

- **Sem barcode scan:** Contagem 100% manual (seleção em dropdown)
- **Sem app mobile:** Contagem via navegador web desktop (lento, propenso a erro)
- **Sem contagem dupla cega:** Um único usuário conta (erro humano não detectado)
- **Sem validação de divergência > 5%:** Aceita qualquer divergência sem recontagem
- **Histórico não preservado:** Editar contagem sobrescreve valor anterior (sem auditoria)
- **Aprovação inexistente:** Divergências aplicadas diretamente ao estoque sem aprovação

---

### Tela: TelaInventario_Divergencias.aspx

- **Caminho:** `D:\IC2\ic1_legado\IControlIT\Estoque\TelaInventario_Divergencias.aspx`
- **Responsabilidade:** Listar divergências identificadas (Qtd_Contada ≠ Qtd_Sistema)

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|------|------|-------------|-------------|
| Grid de divergências | GridView | - | Código Ativo, Qtd Sistema, Qtd Contada, Diferença |
| Botão "Aplicar Ajustes" | Button | - | Aplica TODAS divergências sem aprovação |

#### Comportamentos Implícitos

- **Sem filtro por classificação ABC:** Divergências não priorizadas por valor/importância
- **Aplicação em lote sem aprovação:** Botão "Aplicar Ajustes" altera estoque sem workflow de aprovação
- **Sem justificativa obrigatória:** Ajustes sem campo de justificativa (compliance fraco)
- **Sem integração ERP:** Ajustes não enviados para lançamento contábil (inconsistência)
- **Sem relatório de auditoria:** Divergências não geram relatório rastreável

---

### Tela: TelaInventario_Relatorio.aspx

- **Caminho:** `D:\IC2\ic1_legado\IControlIT\Estoque\TelaInventario_Relatorio.aspx`
- **Responsabilidade:** Gerar relatório PDF de inventário

#### Comportamentos Implícitos

- **PDF genérico:** Não compatível com ISO 9001 (faltam assinaturas digitais, cabeçalho formal)
- **Sem armazenamento obrigatório:** PDF não salvo automaticamente no DMS
- **Sem criptografia:** PDF não assinado digitalmente (compliance fraco)
- **Formatação inconsistente:** Layout varia entre inventários

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

### EstoqueInventarioService.asmx

| Método | Local | Responsabilidade | Observações |
|------|-------|------------------|-------------|
| `IniciarInventario(idAlmoxarifado)` | `D:\IC2\ic1_legado\IControlIT\Estoque\WebService\EstoqueInventarioService.asmx` | Cria registro de inventário sem validações | **Destino:** SUBSTITUÍDO por `CreateInventarioCommand` com validações completas |
| `ObterItensInventario(idInventario)` | Mesma | Retorna lista de itens do inventário | **Destino:** SUBSTITUÍDO por `GET /api/inventarios/{id}/itens` |
| `RegistrarContagem(idItem, qtdContada)` | Mesma | Registra contagem sem validações | **Destino:** SUBSTITUÍDO por `POST /api/inventarios/{id}/itens/{itemId}/contar` com validação de divergência |
| `AplicarAjustes(idInventario)` | Mesma | Aplica ajustes sem aprovação | **Destino:** SUBSTITUÍDO por workflow com aprovação obrigatória |

---

## 4. TABELAS LEGADAS

### Estoque_Inventario

**Schema:** `[dbo].[Estoque_Inventario]`

| Coluna | Tipo | Observação | Problema Identificado |
|--------|------|------------|----------------------|
| `Id_Estoque_Inventario` | UNIQUEIDENTIFIER | PK | ✅ Mantido |
| `Id_Almoxarifado` | UNIQUEIDENTIFIER | FK | ✅ Mantido |
| `Tipo_Inventario` | VARCHAR(20) | 'Geral', 'Parcial' | ❌ Falta 'Ciclico' |
| `Dt_Inicio` | DATE | Data de início | ✅ Mantido |
| `Dt_Fim` | DATE NULL | Data de fim | ✅ Mantido |
| `Status` | VARCHAR(20) | 'Em_Andamento', 'Concluido', 'Cancelado' | ⚠️ Faltam estados intermediários |
| `Qtd_Itens_Contados` | INT | Total de itens contados | ✅ Mantido |
| `Qtd_Divergencias` | INT | Total de divergências | ✅ Mantido |
| `Vl_Divergencias` | DECIMAL(18,2) | Valor total das divergências | ✅ Mantido |

**Problemas Identificados:**
- ❌ **Falta multi-tenancy:** Sem campo `ClienteId` (todos os Fornecedores compartilham mesma tabela)
- ❌ **Falta auditoria:** Sem `Created`, `CreatedBy`, `LastModified`, `LastModifiedBy`
- ❌ **Falta soft delete:** Sem `Fl_Excluido` (deleção física)
- ❌ **Falta classificação ABC:** Sem campo para tipo de inventário cíclico

**Destino:** SUBSTITUÍDO por tabela redesenhada `EstoqueInventario` com multi-tenancy e auditoria completa

---

### Estoque_Inventario_Item

**Schema:** `[dbo].[Estoque_Inventario_Item]`

| Coluna | Tipo | Observação | Problema Identificado |
|--------|------|------------|----------------------|
| `Id_Inventario_Item` | UNIQUEIDENTIFIER | PK | ✅ Mantido |
| `Id_Estoque_Inventario` | UNIQUEIDENTIFIER | FK | ✅ Mantido |
| `Id_Ativo` | UNIQUEIDENTIFIER | FK | ⚠️ Deveria ser `ProdutoId` (genérico) |
| `Qtd_Sistema` | INT | Quantidade no sistema | ✅ Mantido |
| `Qtd_Contada` | INT NULL | Quantidade contada | ✅ Mantido |
| `Divergencia` | INT COMPUTED | `Qtd_Contada - Qtd_Sistema` | ✅ Mantido |
| `Status_Item` | VARCHAR(20) | 'Pendente', 'Contado' | ⚠️ Faltam estados ('Divergente', 'RecontagemSolicitada', 'Ajustado') |
| `Observacao` | NVARCHAR(500) NULL | Observação livre | ✅ Mantido |
| `Dt_Contagem` | DATETIME NULL | Data/hora da contagem | ✅ Mantido |
| `Id_Usuario_Contador` | UNIQUEIDENTIFIER NULL | FK para usuário | ✅ Mantido |

**Problemas Identificados:**
- ❌ **Falta campo classificação ABC:** Sem campo para identificar A, B, C
- ❌ **Falta campo contagem dupla:** Sem campo para `Id_Usuario_Contador_2` (contagem cega)
- ❌ **Falta campo aprovação ajuste:** Sem FK para usuário aprovador
- ❌ **Falta histórico de contagens:** Editar contagem sobrescreve valor (sem auditoria)
- ❌ **Status_Item incompleto:** Faltam estados críticos do workflow

**Destino:** SUBSTITUÍDO por `EstoqueInventarioItem` com campos adicionais e histórico de contagens

---

### Stored Procedures

| Stored Procedure | Responsabilidade | Problema Identificado | Destino |
|------------------|------------------|----------------------|---------|
| `sp_ObterItensParaInventario` | Gera lista de itens a contar | ❌ Não filtra por classificação ABC | SUBSTITUÍDO por query LINQ com filtro ABC |
| `sp_CalcularDivergencias` | Calcula divergências | ✅ Lógica válida | ASSUMIDO (movido para Application Layer) |
| `sp_AplicarAjustesInventario` | Aplica ajustes ao estoque | ❌ Sem validação de aprovação | SUBSTITUÍDO por workflow com aprovação |
| `sp_GerarRelatorioInventario` | Gera dados para relatório | ⚠️ Formato não ISO 9001 | SUBSTITUÍDO por geração de PDF assinado |

---

## 5. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

Liste regras que não estavam documentadas formalmente, mas foram encontradas no código.

### RL-RN-001: Inventário Sem Bloqueio de Almoxarifado

**Localização:** `TelaInventario.aspx.vb` - Linha 145

**Descrição:**
No legado, ao iniciar um inventário, o almoxarifado NÃO é bloqueado. Usuários podem continuar requisitando, recebendo e transferindo itens durante a contagem. Isso causa inconsistência entre a quantidade registrada no sistema no momento da contagem e a quantidade real ao finalizar o inventário.

**Destino:** SUBSTITUÍDO
**Justificativa:** Sistema moderno bloqueia almoxarifado automaticamente ao iniciar inventário (RN-RF068-005)

---

### RL-RN-002: Divergência Aplicada Sem Aprovação

**Localização:** `TelaInventario_Divergencias.aspx.vb` - Linha 78

**Descrição:**
Botão "Aplicar Ajustes" atualiza quantidade no estoque diretamente, sem workflow de aprovação. Qualquer usuário com acesso à tela pode aplicar ajustes. Não há registro de quem aprovou ou justificativa.

**Destino:** DESCARTADO
**Justificativa:** Sistema moderno implementa workflow de aprovação obrigatório (RN-RF068-004)

---

### RL-RN-003: Contagem Manual Sem Barcode

**Localização:** `TelaInventario_Contar.aspx.vb` - Linha 56

**Descrição:**
Usuário seleciona item em dropdown manual (pesquisa por código ou nome). Processo lento e propenso a erro (selecionar item errado). Sem suporte para leitura de código de barras.

**Destino:** SUBSTITUÍDO
**Justificativa:** Sistema moderno implementa app mobile PWA com barcode/QR scan

---

### RL-RN-004: Classificação ABC Inexistente

**Localização:** Todo o módulo de inventário

**Descrição:**
Legado não implementa classificação ABC. Inventários são sempre gerais (contar todos os itens) ou parciais (filtro manual por categoria). Não há periodicidade diferenciada por valor/importância de item. Classificação ABC feita manualmente em planilhas Excel fora do sistema.

**Destino:** SUBSTITUÍDO
**Justificativa:** Sistema moderno implementa classificação ABC automática com job Hangfire (RN-RF068-001, RN-RF068-007)

---

### RL-RN-005: Histórico de Contagens Não Preservado

**Localização:** `EstoqueInventarioService.asmx.vb` - Método `RegistrarContagem` - Linha 120

**Descrição:**
Ao registrar contagem, código executa `UPDATE` na tabela `Estoque_Inventario_Item`. Se usuário recontar o item, valor anterior é sobrescrito. Não há tabela de histórico de contagens. Impossível auditar quem contou, quando e qual foi o resultado de cada contagem.

**Destino:** SUBSTITUÍDO
**Justificativa:** Sistema moderno implementa histórico imutável de contagens (RN-RF068-008)

---

### RL-RN-006: Integração ERP Inexistente

**Localização:** Todo o módulo de inventário

**Descrição:**
Ajustes de estoque (perdas ou sobras) não são enviados automaticamente para ERP. Lançamentos contábeis feitos manualmente pela equipe financeira com base em relatório Excel exportado do sistema. Alto risco de erro e perda de dados.

**Destino:** SUBSTITUÍDO
**Justificativa:** Sistema moderno integra com ERP via evento domain `EstoqueAjustadoEvent` (RN-RF068-010)

---

### RL-RN-007: Relatório Não Compatível ISO 9001

**Localização:** `TelaInventario_Relatorio.aspx.vb` - Linha 200

**Descrição:**
Relatório gerado em PDF genérico sem assinatura digital, cabeçalho formal, ou campos exigidos por ISO 9001 (data, responsáveis, assinaturas). PDF não armazenado automaticamente (usuário baixa e salva manualmente).

**Destino:** SUBSTITUÍDO
**Justificativa:** Sistema moderno gera relatório ISO 9001 com assinatura digital e armazenamento obrigatório por 7 anos (RN-RF068-011)

---

## 6. GAP ANALYSIS (LEGADO x RF MODERNO)

| Item | Legado | RF Moderno | Observação |
|-----|--------|------------|------------|
| **Classificação ABC** | Inexistente (manual em Excel) | Automática com job Hangfire | Melhoria significativa: Inventário cíclico otimizado |
| **Contagem** | Manual via dropdown web | App mobile PWA com barcode scan | Melhoria: Redução de 80% no tempo de contagem |
| **Contagem Dupla Cega** | Inexistente | Obrigatória para itens A | Melhoria: Redução de erro humano em itens críticos |
| **Bloqueio Almoxarifado** | Inexistente | Automático ao iniciar inventário | Melhoria: Elimina inconsistência durante contagem |
| **Aprovação de Ajustes** | Inexistente | Workflow com Supervisor obrigatório | Melhoria: Compliance e auditoria |
| **Recontagem > 5%** | Inexistente | Obrigatória | Melhoria: Reduz erro de contagem |
| **Histórico de Contagens** | Sobrescrito (não preservado) | Imutável | Melhoria: Rastreabilidade total |
| **Dashboard Tempo Real** | Inexistente | SignalR com latência < 2s | Melhoria: Gestão de equipes de contagem |
| **Integração ERP** | Inexistente (manual) | Automática com retry | Melhoria: Consistência contábil |
| **Relatório ISO 9001** | PDF genérico | PDF assinado digitalmente, armazenamento 7 anos | Melhoria: Compliance |
| **Multi-tenancy** | Parcial (sem ClienteId em tabelas) | Completo (ClienteId em todas as tabelas) | Melhoria: Isolamento de dados |
| **Auditoria** | Inexistente | Completa (Created, CreatedBy, LastModified) | Melhoria: Compliance LGPD |
| **App Mobile Offline** | Inexistente | PWA offline-first com sincronização | Melhoria: Funciona sem internet |

---

## 7. DECISÕES DE MODERNIZAÇÃO

Explique decisões tomadas durante a refatoração.

### Decisão 1: Implementar Classificação ABC Automática

**Descrição:** Substituir classificação ABC manual (planilhas Excel) por cálculo automático baseado em valor acumulado (Quantidade × Custo Unitário).

**Motivo:**
- Otimiza recursos de contagem (80% do valor em 20% dos itens)
- Reduz tempo total de inventário em 60%
- Elimina trabalho manual em Excel
- Compliance com ISO 9001

**Impacto:** ALTO - Mudança de processo operacional (equipe precisa ser treinada)

---

### Decisão 2: App Mobile PWA com Barcode Scan

**Descrição:** Substituir contagem via dropdown web desktop por app mobile PWA com leitura de barcode/QR code.

**Motivo:**
- Reduz tempo de contagem em 80% (scan instantâneo vs busca manual)
- Elimina erro de seleção de item errado
- Funciona offline (almoxarifados com sinal fraco)
- UX moderna e intuitiva

**Impacto:** ALTO - Exige desenvolvimento de PWA + integração com câmera de dispositivos móveis

---

### Decisão 3: Workflow de Aprovação de Ajustes

**Descrição:** Implementar workflow obrigatório com Supervisor antes de aplicar ajustes ao estoque.

**Motivo:**
- Compliance (ajustes têm impacto contábil/fiscal)
- Rastreabilidade (quem aprovou, quando, por quê)
- Reduz fraudes (usuário não pode aprovar próprio ajuste)
- Exigência ISO 9001

**Impacto:** MÉDIO - Mudança de processo (ajustes não são mais instantâneos)

---

### Decisão 4: Bloqueio de Almoxarifado Durante Inventário

**Descrição:** Bloquear automaticamente movimentações de estoque ao iniciar inventário.

**Motivo:**
- Elimina inconsistência entre contagem física e sistema
- Evita retrabalho (recontar itens que foram movimentados)
- Garante que Qtd_Sistema no momento da contagem = Qtd_Sistema ao finalizar

**Impacto:** MÉDIO - Mudança operacional (almoxarifados precisam planejar inventário para períodos de baixa movimentação)

---

### Decisão 5: Histórico Imutável de Contagens

**Descrição:** Preservar todas as contagens (primeira, segunda, recontagem) sem permitir edição ou deleção.

**Motivo:**
- Rastreabilidade total (compliance SOX, ISO 9001)
- Evidência em auditoria externa
- Identificação de padrões de erro por contador

**Impacto:** BAIXO - Apenas mudança técnica (storage adicional insignificante)

---

## 8. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Mitigação |
|------|---------|-----------|
| **Resistência de usuários a app mobile** | ALTO - Equipe acostumada com web desktop pode rejeitar mudança | Treinamento obrigatório + período de transição (1 mês com ambos sistemas) |
| **Almoxarifados sem internet para PWA** | MÉDIO - PWA offline mitiga, mas sincronização pode atrasar | Garantir que sincronização ocorra ao final do dia (conectar em rede Wi-Fi) |
| **Divergências históricas não migradas** | MÉDIO - Dados de inventários antigos (< 2020) sem histórico de contagens | Migrar apenas inventários dos últimos 3 anos (2022-2025) |
| **Impacto operacional de bloqueio de almoxarifado** | ALTO - Operação pode parar se inventário não for planejado | Comunicação prévia obrigatória (15 dias antes de iniciar inventário) |
| **Classificação ABC inicial incorreta** | MÉDIO - Primeiros inventários cíclicos podem ter itens mal classificados | Revisão manual da classificação ABC antes do primeiro inventário cíclico |

---

## 9. RASTREABILIDADE

| Elemento Legado | Referência RF Moderno |
|----------------|---------------|
| `TelaInventario.aspx` | RF068 - Seção 4 (Funcionalidades 1-3) |
| `TelaInventario_Contar.aspx` | RF068 - Seção 5 (RN-RF068-002, RN-RF068-003) |
| `TelaInventario_Divergencias.aspx` | RF068 - Seção 5 (RN-RF068-004) |
| `TelaInventario_Relatorio.aspx` | RF068 - Seção 5 (RN-RF068-011) |
| `EstoqueInventarioService.asmx.IniciarInventario` | RF068 - Seção 8 (POST /api/inventarios) |
| `EstoqueInventarioService.asmx.RegistrarContagem` | RF068 - Seção 8 (POST /api/inventarios/{id}/itens/{itemId}/contar) |
| `sp_ObterItensParaInventario` | RF068 - Seção 5 (RN-RF068-001 - Classificação ABC) |
| `sp_AplicarAjustesInventario` | RF068 - Seção 8 (POST /api/inventarios/{id}/ajustes/{ajusteId}/aprovar) |
| Tabela `Estoque_Inventario` | MD-RF068 - Tabela `EstoqueInventario` (com multi-tenancy) |
| Tabela `Estoque_Inventario_Item` | MD-RF068 - Tabela `EstoqueInventarioItem` (com estados adicionais) |

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|------|------|----------|------|
| 1.0 | 2025-12-30 | Criação do documento de referência ao legado com 7 seções completas | Agência ALC - alc.dev.br |
