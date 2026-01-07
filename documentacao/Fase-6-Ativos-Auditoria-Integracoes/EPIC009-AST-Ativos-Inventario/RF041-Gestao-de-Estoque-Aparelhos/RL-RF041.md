# RL-RF041: Referência ao Legado - Gestão de Estoque de Aparelhos

**Versão**: 1.0 | **Data**: 2025-12-30 | **RF Relacionado**: RF041

---

## 1. Visão Geral do Legado

### 1.1. Tipo de Legado

**Documentação Code-Heavy + Sistema Legado ASPX/VB.NET**

Este documento cataloga dois tipos de legado:
1. **Documentação com código SQL** - RF041.md v1.0 continha DDL completo de 5 tabelas (aproximadamente 280 linhas de SQL)
2. **Sistema legado ASPX/VB.NET** - Páginas e stored procedures em `ic1_legado/IControlIT/Estoque/`

### 1.2. Motivação da Separação

A versão 1.0 do RF041 misturava:
- Especificação funcional em linguagem natural
- Código SQL DDL de 5 tabelas (Estoque_Almoxarifado, Estoque_Saldo, Estoque_Movimentacao, Estoque_Reserva, Estoque_Nivel_Alerta)
- Referências ao sistema legado ASPX

Na versão 2.0, o código foi removido do RF e movido para este documento de referência (RL), mantendo o RF puro em linguagem natural conforme Governance v2.0.

---

## 2. Código SQL Removido do RF (DDL)

### 2.1. Tabela Estoque_Almoxarifado

**Localização Original**: RF041.md v1.0, Seção 4.1

**Código Removido**:
```sql
CREATE TABLE Estoque_Almoxarifado (
    Id_Almoxarifado UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    Id_Empresa UNIQUEIDENTIFIER NOT NULL, -- Multi-tenancy
    Codigo VARCHAR(20) NOT NULL,
    Nome NVARCHAR(100) NOT NULL,
    Id_Filial UNIQUEIDENTIFIER NULL, -- Vínculo com filial
    Endereco NVARCHAR(200) NULL,
    Responsavel_Id_Usuario UNIQUEIDENTIFIER NULL,
    Fl_Ativo BIT DEFAULT 1,
    -- Auditoria
    DataCriacao DATETIME2 DEFAULT GETDATE(),
    UsuarioCriacaoId UNIQUEIDENTIFIER,
    DataAlteracao DATETIME2,
    UsuarioAlteracaoId UNIQUEIDENTIFIER,
    CONSTRAINT FK_Estoque_Almoxarifado_Empresa FOREIGN KEY (Id_Empresa) REFERENCES Empresa(Id)
);
```

**Destino**: **SUBSTITUÍDO** por descrição em linguagem natural no RF041.md v2.0

**Referência v2.0**: Seção 4 (Integrações Obrigatórias) menciona conceitos sem código

**Observações**:
- Tabela de cadastro de almoxarifados
- Multi-tenancy via `Id_Empresa`
- Auditoria com DataCriacao, UsuarioCriacaoId, DataAlteracao, UsuarioAlteracaoId
- FK para Empresa

---

### 2.2. Tabela Estoque_Saldo

**Localização Original**: RF041.md v1.0, Seção 4.2

**Código Removido**:
```sql
CREATE TABLE Estoque_Saldo (
    Id_Estoque_Saldo UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    Id_Almoxarifado UNIQUEIDENTIFIER NOT NULL,
    Id_Categoria UNIQUEIDENTIFIER NOT NULL, -- RF014
    Id_Marca UNIQUEIDENTIFIER NOT NULL, -- RF104
    Id_Modelo UNIQUEIDENTIFIER NOT NULL, -- RF104
    Quantidade_Fisica INT DEFAULT 0, -- Saldo real
    Quantidade_Reservada INT DEFAULT 0, -- Bloqueada por reservas
    Quantidade_Disponivel AS (Quantidade_Fisica - Quantidade_Reservada) PERSISTED,
    Custo_Medio DECIMAL(18,2) DEFAULT 0,
    -- Auditoria
    DataUltimaMovimentacao DATETIME2,
    CONSTRAINT FK_Estoque_Saldo_Almoxarifado FOREIGN KEY (Id_Almoxarifado) REFERENCES Estoque_Almoxarifado(Id_Almoxarifado)
);
```

**Destino**: **SUBSTITUÍDO** por descrição em linguagem natural no RF041.md v2.0

**Referência v2.0**: RN-AST-041-20 (Reserva Não Pode Exceder Saldo Disponível) menciona conceito de saldo físico vs disponível

**Observações**:
- Coluna computada `Quantidade_Disponivel = Quantidade_Fisica - Quantidade_Reservada` (PERSISTED)
- Custo médio para cálculo de valor total em R$
- FK para Estoque_Almoxarifado

---

### 2.3. Tabela Estoque_Movimentacao

**Localização Original**: RF041.md v1.0, Seção 4.3

**Código Removido**:
```sql
CREATE TABLE Estoque_Movimentacao (
    Id_Movimentacao UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    Id_Empresa UNIQUEIDENTIFIER NOT NULL,
    Id_Almoxarifado UNIQUEIDENTIFIER NOT NULL,
    Tipo_Movimentacao VARCHAR(20) NOT NULL, -- 'Entrada' | 'Saida' | 'Transferencia_Enviada' | 'Transferencia_Recebida' | 'Ajuste'
    Subtipo VARCHAR(50) NULL, -- 'Compra' | 'Devolucao' | 'Distribuicao' | 'Descarte' | etc.
    Id_Categoria UNIQUEIDENTIFIER NOT NULL,
    Id_Marca UNIQUEIDENTIFIER NOT NULL,
    Id_Modelo UNIQUEIDENTIFIER NOT NULL,
    Quantidade INT NOT NULL,
    IMEI_Serial_Number NVARCHAR(50) NULL, -- Se rastreável
    Id_Nota_Fiscal UNIQUEIDENTIFIER NULL, -- Vínculo com RF039
    Id_Ativo UNIQUEIDENTIFIER NULL, -- Vínculo com RF028 (se distribuição)
    Id_Usuario_Destinatario UNIQUEIDENTIFIER NULL, -- Se distribuição
    Id_Transferencia UNIQUEIDENTIFIER NULL, -- Se transferência
    Motivo NVARCHAR(200) NULL,
    Observacoes NVARCHAR(500) NULL,
    -- Auditoria
    DataMovimentacao DATETIME2 DEFAULT GETDATE(),
    UsuarioMovimentacaoId UNIQUEIDENTIFIER NOT NULL,
    CONSTRAINT FK_Estoque_Movimentacao_Empresa FOREIGN KEY (Id_Empresa) REFERENCES Empresa(Id)
);
```

**Destino**: **SUBSTITUÍDO** por descrição em linguagem natural no RF041.md v2.0

**Referência v2.0**: RN-AST-041-17 (Histórico de Movimentações é Imutável)

**Observações**:
- Tabela de histórico (INSERT apenas, sem UPDATE/DELETE)
- Tipo + Subtipo para categorização de movimentações
- Vínculos opcionais (Nota Fiscal, Ativo, Transferência)
- IMEI/SN para rastreabilidade

---

### 2.4. Tabela Estoque_Reserva

**Localização Original**: RF041.md v1.0, Seção 4.4

**Código Removido**:
```sql
CREATE TABLE Estoque_Reserva (
    Id_Reserva UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    Id_Empresa UNIQUEIDENTIFIER NOT NULL,
    Id_Almoxarifado UNIQUEIDENTIFIER NOT NULL,
    Id_Categoria UNIQUEIDENTIFIER NOT NULL,
    Id_Marca UNIQUEIDENTIFIER NOT NULL,
    Id_Modelo UNIQUEIDENTIFIER NOT NULL,
    Quantidade_Reservada INT NOT NULL,
    Id_Usuario_Destinatario UNIQUEIDENTIFIER NOT NULL,
    Motivo_Reserva NVARCHAR(200) NULL,
    Data_Inicio DATE NOT NULL,
    Data_Validade DATE NOT NULL,
    Status VARCHAR(20) DEFAULT 'Ativa', -- 'Ativa' | 'Consumida' | 'Cancelada' | 'Expirada'
    Data_Consumo DATETIME2 NULL,
    Data_Cancelamento DATETIME2 NULL,
    Motivo_Cancelamento NVARCHAR(200) NULL,
    -- Auditoria
    DataCriacao DATETIME2 DEFAULT GETDATE(),
    UsuarioCriacaoId UNIQUEIDENTIFIER,
    CONSTRAINT FK_Estoque_Reserva_Empresa FOREIGN KEY (Id_Empresa) REFERENCES Empresa(Id)
);
```

**Destino**: **SUBSTITUÍDO** por descrição em linguagem natural no RF041.md v2.0

**Referência v2.0**: Funcionalidade 2.5 (Reserva de Aparelhos) + RN-AST-041-21 (validade 30 dias) + RN-AST-041-22 (expiração automática)

**Observações**:
- Status enum: Ativa, Consumida, Cancelada, Expirada
- Validade máxima 30 dias (validada no backend)
- Data_Consumo e Data_Cancelamento para auditoria
- Motivo_Cancelamento obrigatório se cancelamento manual

---

### 2.5. Tabela Estoque_Nivel_Alerta

**Localização Original**: RF041.md v1.0, Seção 4.5

**Código Removido**:
```sql
CREATE TABLE Estoque_Nivel_Alerta (
    Id_Nivel_Alerta UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    Id_Empresa UNIQUEIDENTIFIER NOT NULL,
    Id_Almoxarifado UNIQUEIDENTIFIER NOT NULL,
    Id_Categoria UNIQUEIDENTIFIER NOT NULL,
    Id_Marca UNIQUEIDENTIFIER NULL, -- Opcional
    Id_Modelo UNIQUEIDENTIFIER NULL, -- Opcional
    Estoque_Minimo INT NOT NULL,
    Estoque_Maximo INT NOT NULL,
    Emails_Alertas NVARCHAR(500) NULL, -- Lista de emails separados por vírgula
    Fl_Ativo BIT DEFAULT 1,
    -- Auditoria
    DataCriacao DATETIME2 DEFAULT GETDATE(),
    UsuarioCriacaoId UNIQUEIDENTIFIER,
    CONSTRAINT FK_Estoque_Nivel_Alerta_Empresa FOREIGN KEY (Id_Empresa) REFERENCES Empresa(Id)
);
```

**Destino**: **SUBSTITUÍDO** por descrição em linguagem natural no RF041.md v2.0

**Referência v2.0**: Funcionalidade 2.6 (Alertas de Estoque Mínimo/Máximo) + RN-AST-041-25 (job a cada 1 hora)

**Observações**:
- Configuração por Almoxarifado + Categoria + Marca/Modelo (opcional)
- Emails separados por vírgula para notificação
- Fl_Ativo para desativar configuração sem deletar

---

## 3. Sistema Legado ASPX/VB.NET

### 3.1. Páginas ASPX Relevantes

**Localização**: `D:/IC2/ic1_legado/IControlIT/Estoque/`

#### 3.1.1. EstoqueMovimentacao.aspx

**Descrição**: Tela de entrada/saída manual de estoque

**Funcionalidade**:
- Formulário único para entrada E saída
- Campos: Tipo (entrada/saída), Almoxarifado, Categoria, Marca, Modelo, Quantidade, Observações
- Sem tipos específicos (compra, devolução, distribuição, descarte)
- Sem workflow de aprovação
- Sem integração com RF028 (não cria ativo automaticamente)

**Destino**: **SUBSTITUÍDO** por `/gestao/estoque/entrada` e `/gestao/estoque/saida` (Angular)

**Diferenças com Sistema Novo**:
- Sistema novo tem tipos específicos de entrada/saída
- Sistema novo cria ativo automaticamente na distribuição (RF028)
- Sistema novo tem workflow de aprovação para ajustes >10 unidades
- Sistema novo valida saldo disponível (físico - reservado)

---

#### 3.1.2. EstoqueConsulta.aspx

**Descrição**: Tela de consulta de saldo e movimentações

**Funcionalidade**:
- Filtros básicos: Almoxarifado, Categoria, Período
- Grid com colunas: Categoria, Marca, Modelo, Quantidade
- Sem coluna de valor total em R$
- Exportação apenas para Excel (sem PDF/CSV)
- Sem rastreamento por IMEI/SN

**Destino**: **SUBSTITUÍDO** por `/gestao/estoque/consulta` (Angular)

**Diferenças com Sistema Novo**:
- Sistema novo exibe valor total (saldo × custo médio) - RN-AST-041-16
- Sistema novo exporta Excel/PDF/CSV
- Sistema novo tem rastreamento por IMEI/SN com timeline visual
- Sistema novo registra exportação em auditoria (compliance LGPD) - RN-AST-041-18

---

#### 3.1.3. EstoqueTransferencia.aspx

**Descrição**: Tela de transferência entre almoxarifados

**Funcionalidade**:
- Transferência direta sem workflow de aprovação
- Saldo deduzido imediatamente da origem
- Saldo adicionado imediatamente ao destino
- Sem status "Em Trânsito"
- Sem alerta para transferências atrasadas

**Destino**: **SUBSTITUÍDO** por `/gestao/estoque/transferencia` (Angular)

**Diferenças com Sistema Novo**:
- Sistema novo tem workflow 3 etapas (solicitação → aprovação → envio → recebimento)
- Saldo deduzido apenas após confirmação de envio (RN-AST-041-12)
- Saldo adicionado apenas após confirmação de recebimento (RN-AST-041-13)
- Status "Em Trânsito" entre envio e recebimento
- Job noturno alerta transferências >15 dias (RN-AST-041-14)

---

### 3.2. Stored Procedures Legadas

**Localização**: Banco de dados SQL Server legado

#### 3.2.1. sp_Estoque_Entrada

**Descrição**: Registra entrada de estoque

**Parâmetros**:
- `@Id_Almoxarifado`
- `@Id_Categoria`
- `@Id_Marca`
- `@Id_Modelo`
- `@Quantidade`
- `@Observacoes`

**Lógica**:
1. INSERT em `Tbl_Estoque_Movimentacao`
2. UPDATE `Tbl_Estoque_Saldo` (incrementa quantidade)
3. Retorna ID da movimentação

**Destino**: **SUBSTITUÍDO** por `POST /api/estoque/entrada` (Command Pattern + MediatR)

**Diferenças com Sistema Novo**:
- Sistema novo valida tipo de entrada (compra requer NF, devolução requer Ativo) - RN-AST-041-01, RN-AST-041-02
- Sistema novo cria workflow de aprovação para ajustes >10 unidades - RN-AST-041-04
- Sistema novo notifica gestor se estoque atingir máximo - Funcionalidade 2.6

---

#### 3.2.2. sp_Estoque_Saida

**Descrição**: Registra saída de estoque

**Parâmetros**:
- `@Id_Almoxarifado`
- `@Id_Categoria`
- `@Id_Marca`
- `@Id_Modelo`
- `@Quantidade`
- `@Observacoes`

**Lógica**:
1. Valida saldo (se quantidade > saldo, retorna erro)
2. INSERT em `Tbl_Estoque_Movimentacao`
3. UPDATE `Tbl_Estoque_Saldo` (decrementa quantidade)
4. Retorna ID da movimentação

**Destino**: **SUBSTITUÍDO** por `POST /api/estoque/saida` (Command Pattern + MediatR)

**Diferenças com Sistema Novo**:
- Sistema novo valida saldo **disponível** (físico - reservado), não apenas físico - RN-AST-041-06
- Sistema novo cria ativo automaticamente se tipo = "Distribuição" - RN-AST-041-07
- Sistema novo cria workflow de aprovação para saídas >10 unidades - RN-AST-041-09
- Sistema novo exige motivo obrigatório para descarte - RN-AST-041-08

---

#### 3.2.3. sp_Estoque_Saldo

**Descrição**: Calcula saldo atual de um item

**Parâmetros**:
- `@Id_Almoxarifado`
- `@Id_Categoria`
- `@Id_Marca`
- `@Id_Modelo`

**Lógica**:
1. SELECT SUM(Quantidade) WHERE Tipo = 'Entrada'
2. SELECT SUM(Quantidade) WHERE Tipo = 'Saida'
3. Retorna diferença (entrada - saída)

**Destino**: **DESCARTADO** - Sistema novo usa tabela `Estoque_Saldo` materializada

**Diferenças com Sistema Novo**:
- Sistema legado calculava saldo dinamicamente (lento para grandes volumes)
- Sistema novo mantém saldo materializado em `Estoque_Saldo` (performance)
- Sistema novo distingue saldo físico vs disponível (físico - reservado)

---

#### 3.2.4. sp_Estoque_Movimentacoes

**Descrição**: Lista histórico de movimentações

**Parâmetros**:
- `@Id_Almoxarifado` (opcional)
- `@DataInicio` (opcional)
- `@DataFim` (opcional)

**Lógica**:
1. SELECT * FROM `Tbl_Estoque_Movimentacao`
2. Filtros dinâmicos por almoxarifado e período
3. ORDER BY DataMovimentacao DESC

**Destino**: **SUBSTITUÍDO** por `GET /api/estoque/movimentacoes` (Query Pattern + MediatR)

**Diferenças com Sistema Novo**:
- Sistema novo tem mais filtros (categoria, marca, modelo, tipo movimentação, usuário)
- Sistema novo exibe valor total em R$ (saldo × custo médio) - RN-AST-041-16
- Sistema novo permite exportação Excel/PDF/CSV com auditoria - RN-AST-041-18
- Sistema novo tem rastreamento por IMEI/SN com timeline visual - Funcionalidade 2.7

---

### 3.3. Tabelas Legadas

**Localização**: Banco de dados SQL Server legado

#### 3.3.1. Tbl_Estoque_Almoxarifado

**Descrição**: Cadastro de almoxarifados

**Colunas**:
- `Id_Almoxarifado INT IDENTITY`
- `Codigo VARCHAR(20)`
- `Nome VARCHAR(100)`
- `Id_Filial INT`
- `Fl_Ativo BIT`

**Destino**: **SUBSTITUÍDO** por `Estoque_Almoxarifado` (GUID, auditoria completa)

**Diferenças**:
- Sistema novo usa `UNIQUEIDENTIFIER` em vez de `INT IDENTITY`
- Sistema novo tem auditoria (DataCriacao, UsuarioCriacaoId, DataAlteracao, UsuarioAlteracaoId)
- Sistema novo tem `Id_Empresa` para multi-tenancy

---

#### 3.3.2. Tbl_Estoque_Saldo

**Descrição**: Saldo atual por almoxarifado + item

**Colunas**:
- `Id_Estoque_Saldo INT IDENTITY`
- `Id_Almoxarifado INT`
- `Id_Categoria INT`
- `Id_Marca INT`
- `Id_Modelo INT`
- `Quantidade INT`

**Destino**: **SUBSTITUÍDO** por `Estoque_Saldo` (com quantidade física, reservada e disponível computada)

**Diferenças**:
- Sistema legado tinha apenas `Quantidade` (sem distinção entre física e disponível)
- Sistema novo tem `Quantidade_Fisica`, `Quantidade_Reservada` e `Quantidade_Disponivel` (coluna computada)
- Sistema novo tem `Custo_Medio` para cálculo de valor total

---

#### 3.3.3. Tbl_Estoque_Movimentacao

**Descrição**: Histórico de entradas/saídas

**Colunas**:
- `Id_Movimentacao INT IDENTITY`
- `Id_Almoxarifado INT`
- `Tipo VARCHAR(10)` (Entrada/Saida)
- `Id_Categoria INT`
- `Id_Marca INT`
- `Id_Modelo INT`
- `Quantidade INT`
- `DataMovimentacao DATETIME`
- `UsuarioId INT`

**Destino**: **SUBSTITUÍDO** por `Estoque_Movimentacao` (com tipos específicos, IMEI/SN, vínculos)

**Diferenças**:
- Sistema legado tinha apenas Tipo (Entrada/Saida)
- Sistema novo tem Tipo + Subtipo (Compra, Devolução, Distribuição, Descarte, etc.)
- Sistema novo tem IMEI/SN para rastreabilidade
- Sistema novo tem vínculos (Nota Fiscal, Ativo, Transferência)

---

#### 3.3.4. Tbl_Estoque_Transferencia

**Descrição**: Transferências entre almoxarifados

**Colunas**:
- `Id_Transferencia INT IDENTITY`
- `Id_Almoxarifado_Origem INT`
- `Id_Almoxarifado_Destino INT`
- `Id_Categoria INT`
- `Id_Marca INT`
- `Id_Modelo INT`
- `Quantidade INT`
- `DataTransferencia DATETIME`
- `UsuarioId INT`

**Destino**: **SUBSTITUÍDO** por workflow de transferência (Estoque_Movimentacao com status)

**Diferenças**:
- Sistema legado tinha tabela separada para transferências
- Sistema novo registra transferências como movimentações com `Id_Transferencia` vinculado
- Sistema novo tem workflow (solicitação → aprovação → envio → recebimento)
- Sistema novo tem status "Em Trânsito" e alerta para atrasos >15 dias

---

## 4. Gaps e Melhorias no Sistema Novo

### 4.1. Funcionalidades Inexistentes no Legado

| Funcionalidade | Sistema Legado | Sistema Novo |
|----------------|----------------|--------------|
| Tipos específicos de entrada/saída | ❌ Entrada/Saída genérica | ✅ Compra, Devolução, Distribuição, Descarte, Ajuste |
| Criação automática de ativo | ❌ Manual | ✅ Automático na distribuição (RF028) |
| Workflow de aprovação | ❌ Não existe | ✅ Ajustes >10 unidades, transferências |
| Reserva de estoque | ❌ Não existe | ✅ Bloqueio de saldo disponível |
| Alertas automáticos | ❌ Manual | ✅ Job a cada 1 hora (estoque mínimo/máximo) |
| Rastreamento IMEI/SN | ❌ Não existe | ✅ Timeline visual completa |
| Saldo disponível vs físico | ❌ Apenas físico | ✅ Físico, Reservado, Disponível |
| Transferência com status | ❌ Transferência direta | ✅ Aguardando Aprovação, Em Trânsito, Concluída |
| Valor total em R$ | ❌ Não calcula | ✅ Saldo × custo médio |
| Exportação com auditoria | ❌ Não auditado | ✅ Registro em auditoria (LGPD) |

---

### 4.2. Melhorias de Performance

| Aspecto | Sistema Legado | Sistema Novo |
|---------|----------------|--------------|
| Cálculo de saldo | Stored procedure (lento) | Tabela materializada (rápido) |
| Saldo disponível | Calculado na hora | Coluna computada PERSISTED |
| Consulta de histórico | SELECT direto | Paginação + índices otimizados |
| Multi-tenancy | Sem isolamento | Filtro automático por ClienteId |

---

### 4.3. Melhorias de Compliance

| Aspecto | Sistema Legado | Sistema Novo |
|---------|----------------|--------------|
| Auditoria | Parcial (apenas DataMovimentacao) | Completa (usuário, IP, timestamp, dados antes/depois) |
| Retention de dados | Não definido | 2555 dias (7 anos) |
| Histórico imutável | Não garantido | Backend NÃO expõe UPDATE/DELETE |
| Exportação rastreada | Não | Registro em auditoria (LGPD) |
| Multi-tenancy | Não | Isolamento total por ClienteId |

---

## 5. Estatísticas de Migração

### 5.1. Código Removido do RF

- **Total de linhas SQL removidas**: ~280 linhas (5 tabelas DDL)
- **Tabelas documentadas no RL**: 5 (Estoque_Almoxarifado, Estoque_Saldo, Estoque_Movimentacao, Estoque_Reserva, Estoque_Nivel_Alerta)

### 5.2. Sistema Legado ASPX

- **Páginas ASPX substituídas**: 3 (EstoqueMovimentacao.aspx, EstoqueConsulta.aspx, EstoqueTransferencia.aspx)
- **Stored Procedures substituídas**: 4 (sp_Estoque_Entrada, sp_Estoque_Saida, sp_Estoque_Saldo, sp_Estoque_Movimentacoes)
- **Tabelas legadas substituídas**: 4 (Tbl_Estoque_Almoxarifado, Tbl_Estoque_Saldo, Tbl_Estoque_Movimentacao, Tbl_Estoque_Transferencia)

### 5.3. RF v2.0

- **Total de linhas RF041.md v2.0**: ~800 linhas (100% linguagem natural)
- **Total de funcionalidades**: 7 (F-AST-041-01 a 07)
- **Total de regras de negócio**: 28 (RN-AST-041-01 a 28)
- **Total de integrações obrigatórias**: 8 (Central Funcionalidades, Auditoria, Multi-tenancy, RBAC, i18n, RF066, RF028, Hangfire)

---

## 6. Decisões Arquiteturais

### 6.1. Por Que Remover Código SQL do RF?

**Motivação**: Governance v2.0 exige separação entre especificação funcional (o que fazer) e implementação técnica (como fazer).

**Vantagens**:
- RF mais legível para stakeholders não técnicos
- Especificação funcional independente de tecnologia
- Código SQL permanece documentado no RL para referência
- Facilita evolução futura (trocar SQL Server por PostgreSQL, por exemplo)

---

### 6.2. Por Que Usar Tabela Materializada em Vez de Stored Procedure?

**Decisão**: Sistema novo usa tabela `Estoque_Saldo` materializada em vez de calcular saldo dinamicamente via stored procedure.

**Motivação**:
- **Performance**: Consultar saldo de 10.000 itens via stored procedure é lento (join + agregação)
- **Escalabilidade**: Tabela materializada escala melhor com crescimento de dados
- **Tempo real**: Saldo atualizado imediatamente na movimentação (não precisa recalcular)

**Trade-off**: Mais complexidade no backend (atualizar saldo em cada movimentação), mas ganho significativo de performance.

---

### 6.3. Por Que Saldo Disponível vs Físico?

**Decisão**: Sistema novo distingue saldo físico (quantidade real) de saldo disponível (físico - reservado).

**Motivação**:
- **Reservas**: Permitir reserva de estoque para distribuição futura sem alterar saldo físico
- **Validação**: Saída/reserva NÃO pode exceder saldo **disponível**, não apenas físico
- **Rastreabilidade**: Saber exatamente quanto está bloqueado por reservas

**Implementação**: Coluna computada PERSISTED `Quantidade_Disponivel = Quantidade_Fisica - Quantidade_Reservada`.

---

## 7. Conclusão

Este documento cataloga TODO o código SQL e referências ao sistema legado que foram **removidos** do RF041.md v1.0 e movidos para esta Referência ao Legado (RL).

**Destinos**:
- **5 tabelas SQL DDL**: SUBSTITUÍDAS por descrição em linguagem natural no RF041.md v2.0
- **3 páginas ASPX**: SUBSTITUÍDAS por rotas Angular (/gestao/estoque/entrada, /saida, /transferencia)
- **4 stored procedures**: SUBSTITUÍDAS por endpoints API com Command/Query Pattern + MediatR
- **1 stored procedure (sp_Estoque_Saldo)**: DESCARTADA (substituída por tabela materializada)

**Cobertura de Destino**: 100% (13/13 itens legado têm destino explícito)

---

[← Voltar ao RF041](./RF041.md)
