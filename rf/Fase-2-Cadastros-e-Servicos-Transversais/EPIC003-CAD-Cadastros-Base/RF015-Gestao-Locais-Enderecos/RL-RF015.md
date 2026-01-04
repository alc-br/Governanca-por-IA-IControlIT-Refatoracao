# RL-RF015 — Referência ao Legado: Gestão de Locais e Endereços

**Versão:** 1.0
**Data:** 2025-12-30
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF-015
**Sistema Legado:** VB.NET + ASP.NET Web Forms
**Objetivo:** Documentar o comportamento do sistema legado de gestão de locais e endereços, servindo de base para a refatoração e garantindo rastreabilidade histórica e mitigação de riscos.

---

## 1. CONTEXTO DO LEGADO

**Descrição Geral**: O sistema legado implementava gestão de endereços e locais físicos através de múltiplas tabelas separadas sem relacionamento claro. A hierarquia de locais era mantida manualmente através de campos de tipo (Edificio, Andar, Sala, Rack, Posicao) sem validação de integridade referencial adequada.

### Características Gerais

- **Arquitetura**: Monolítica WebForms + VB.NET
- **Linguagem / Stack**: VB.NET, ASP.NET Web Forms, SQL Server
- **Banco de Dados**: SQL Server 2016+ (database `IControlIT`)
- **Multi-tenant**: Sim (campo `Id_Conglomerado` em todas as tabelas)
- **Auditoria**: Parcial (campos `Dt_Atualizacao` e `Id_Usuario_Atualizacao`, sem histórico imutável)
- **Configurações**: Web.config para connection strings e APIs externas
- **Validação de CEP**: Manual, sem integração com APIs externas
- **Geolocalização**: Armazenamento manual de coordenadas, sem geocodificação automática

### Problemas Identificados

1. **Hierarquia fraca**: Tabelas separadas sem FKs claras, permitindo criação de registros órfãos
2. **Validação manual**: CEP e UF validados em code-behind VB.NET, propenso a erros
3. **Sem geocodificação automática**: Coordenadas inseridas manualmente, alta taxa de erro
4. **Controle de racks ineficiente**: Posições duplicadas, sobreposição não detectada
5. **Histórico editável**: Tabela de movimentações permite UPDATE/DELETE, violando auditoria
6. **Performance ruim**: Queries N+1 sem índices otimizados, carregamento lento
7. **Sem circuit breaker**: Chamadas externas sem timeout ou retry logic
8. **Interface desacoplada**: Telas ASPX com postbacks completos, experiência lenta

---

## 2. TELAS DO LEGADO

### Tela: Endereco.aspx

- **Caminho:** `D:\IC2\ic1_legado\IControlIT\Cadastros\Endereco.aspx`
- **Responsabilidade:** CRUD de endereços com validação manual de CEP
- **Code-behind:** `Endereco.aspx.vb`

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|------|------|-------------|-------------|
| txtLogradouro | TextBox | Sim | Sem validação de comprimento máximo |
| txtNumero | TextBox | Sim | Aceita texto livre, sem validação numérica |
| txtComplemento | TextBox | Não | Opcional |
| txtBairro | TextBox | Não | Preenchido manualmente (sem integração ViaCEP) |
| txtCidade | TextBox | Sim | Sem autocomplete |
| ddlEstado | DropDownList | Sim | Lista hardcoded em code-behind |
| txtCEP | TextBox | Sim | Validação manual via regex `^\d{5}-\d{3}$` |
| txtLatitude | TextBox | Não | Entrada manual, sem geocodificação automática |
| txtLongitude | TextBox | Não | Entrada manual, sem geocodificação automática |
| chkPrincipal | CheckBox | Não | Sem validação de unicidade no frontend |

#### Comportamentos Implícitos

- **Validação de UF hardcoded**: Lista de 27 UFs brasileiras hardcoded em `Private Sub PopularEstados()`, sem enum ou tabela
- **CEP sem integração**: Validação apenas de formato, sem consulta a ViaCEP
- **Endereço principal duplicado**: Permite marcar múltiplos endereços como principal (bug no legado)
- **Postback completo**: Cada alteração de dropdown recarrega página inteira
- **Coordenadas manuais**: Sem mapa interativo ou validação de lat/lon
- **Sem soft delete**: Botão "Excluir" executa DELETE direto no banco

---

### Tela: Local.aspx

- **Caminho:** `D:\IC2\ic1_legado\IControlIT\Cadastros\Local.aspx`
- **Responsabilidade:** Gestão de hierarquia de locais (Edifício → Andar → Sala)
- **Code-behind:** `Local.aspx.vb`

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|------|------|-------------|-------------|
| txtNomeLocal | TextBox | Sim | Nome do local |
| ddlTipo | DropDownList | Sim | Valores: Edificio, Andar, Sala |
| ddlLocalPai | DropDownList | Não | Permite selecionar qualquer local (sem validação de hierarquia) |
| ddlEndereco | DropDownList | Sim | Lista todos os endereços do conglomerado |
| txtDescricao | TextBox | Não | Texto livre |

#### Comportamentos Implícitos

- **Hierarquia não validada**: Permite criar Sala sem Andar, Andar sem Edifício (órfãos)
- **Loop permitido**: Local pode ser pai de si mesmo (bug crítico)
- **Sem cascata**: Excluir Edifício não desativa Andares/Salas automaticamente
- **Tipo enum hardcoded**: Tipos de local em string sem enum ou constraint CHECK
- **Performance ruim**: Query recursiva manual sem CTE, timeout em hierarquias grandes

---

### Tela: Rack.aspx

- **Caminho:** `D:\IC2\ic1_legado\IControlIT\Infraestrutura\Rack.aspx`
- **Responsabilidade:** Cadastro de racks e controle de posições (Us)
- **Code-behind:** `Rack.aspx.vb`

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|------|------|-------------|-------------|
| txtNomeRack | TextBox | Sim | Identificação do rack |
| txtAlturaUs | TextBox | Sim | Validação manual 1-48 |
| ddlProfundidade | DropDownList | Sim | Valores fixos: 600mm, 800mm, 1000mm |
| txtPesoMaximo | TextBox | Sim | Em kg, validação manual |
| txtPotenciaMaxima | TextBox | Sim | Em watts, validação manual |

#### Comportamentos Implícitos

- **Sobreposição permitida**: Sistema permite instalar equipamento em U10-U12 mesmo com U11-U13 já ocupado (bug crítico)
- **Capacidade não validada**: Permite instalar equipamento que excede peso/potência máxima
- **Sala não validada**: Permite criar rack em sala tipo "Escritório" (violação de regra de negócio)
- **Visualização manual**: Não há grid visual de Us ocupadas/disponíveis
- **Sem alertas**: Nenhuma notificação quando rack atinge 80% de ocupação

---

### Tela: RackVisual.aspx

- **Caminho:** `D:\IC2\ic1_legado\IControlIT\Infraestrutura\RackVisual.aspx`
- **Responsabilidade:** Visualização de rack com Us ocupadas
- **Code-behind:** `RackVisual.aspx.vb`

#### Comportamentos Implícitos

- **Visualização estática**: Renderiza tabela HTML fixa, sem interatividade
- **Cores hardcoded**: Verde (disponível), vermelho (ocupado), sem legenda
- **Sem zoom/detalhes**: Não mostra qual equipamento está em cada U
- **Performance ruim**: Carrega todos os 48Us mesmo se rack tiver 12Us

---

### Tela: MapaLocais.aspx

- **Caminho:** `D:\IC2\ic1_legado\IControlIT\Relatorios\MapaLocais.aspx`
- **Responsabilidade:** Visualização de locais em mapa (Google Maps)
- **Code-behind:** `MapaLocais.aspx.vb`

#### Comportamentos Implícitos

- **API Key hardcoded**: Chave do Google Maps no JavaScript (risco de segurança)
- **Sem agrupamento**: Exibe todos os marcadores individualmente (lento com 1000+ locais)
- **Sem filtros**: Não permite filtrar por tipo de local ou região
- **Coordenadas inválidas**: Marcadores com lat/lon = 0 aparecem no oceano Atlântico

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

| Método | Local | Responsabilidade | Observações |
|------|-------|------------------|-------------|
| `CadastrarEndereco` | `WSLocal.asmx.vb` | Criar novo endereço | Validação manual de CEP, sem ViaCEP |
| `AtualizarEndereco` | `WSLocal.asmx.vb` | Atualizar endereço | Permite alterar endereço principal sem desmarcar anterior |
| `ListarEnderecos` | `WSLocal.asmx.vb` | Listar todos endereços do conglomerado | Query sem paginação, retorna até 10.000 registros |
| `BuscarEnderecoPorCEP` | `WSLocal.asmx.vb` | Buscar endereço por CEP | Consulta tabela local de CEPs (desatualizada) |
| `CadastrarLocal` | `WSLocal.asmx.vb` | Criar local/andar/sala | Sem validação de hierarquia |
| `ListarLocalHierarquia` | `WSLocal.asmx.vb` | Obter árvore de locais | Query recursiva manual (lenta) |
| `CadastrarRack` | `WSLocal.asmx.vb` | Criar rack | Sem validação de tipo de sala |
| `RegistrarMovimentacao` | `WSLocal.asmx.vb` | Registrar movimentação de ativo | Permite UPDATE/DELETE (violação de auditoria) |

---

## 4. TABELAS LEGADAS

| Tabela | Finalidade | Problemas Identificados |
|-------|------------|-------------------------|
| `Endereco` | Armazenar endereços completos | Campo `Nm_Tipo` genérico (Empresa, Filial, Fornecedor), sem FK específica |
| `Local` | Hierarquia de locais | FK `Id_Local_Pai` permite NULL (cria órfãos), sem CHECK constraint para tipos |
| `Rack` | Racks de TI | Sem validação de profundidade/altura, permite valores inválidos |
| `RackPosicao` | Posições em racks | Falta constraint UNIQUE em `(Id_Rack, Nr_Posicao_U)`, permite duplicação |
| `Local_Historico_Movimentacao` | Histórico de movimentações | Permite UPDATE/DELETE (violação de auditoria imutável) |

### DDL Legado (Endereco)

```sql
CREATE TABLE [dbo].[Endereco](
    [Id_Endereco] [int] IDENTITY(1,1) NOT NULL,
    [Id_Conglomerado] [int] NOT NULL,
    [Nm_Tipo] [varchar](50) NOT NULL,  -- 'Empresa', 'Filial', 'Fornecedor', 'Consumidor'
    [Id_Referencia] [int] NOT NULL,     -- FK genérica (problema: sem FK real)
    [Nm_Logradouro] [varchar](255) NOT NULL,
    [Nr_Numero] [varchar](10) NOT NULL,
    [Ds_Complemento] [varchar](255) NULL,
    [Nm_Bairro] [varchar](100) NULL,
    [Nm_Cidade] [varchar](100) NOT NULL,
    [Sg_Estado] [char](2) NOT NULL,
    [Nr_CEP] [varchar](10) NOT NULL,
    [Ds_Pais] [varchar](100) NOT NULL DEFAULT 'Brasil',
    [Nr_Latitude] [decimal](11, 8) NULL,
    [Nr_Longitude] [decimal](11, 8) NULL,
    [Fl_Principal] [bit] NOT NULL DEFAULT 0,
    [Fl_Excluido] [bit] NOT NULL DEFAULT 0,
    [Dt_Atualizacao] [datetime] NOT NULL DEFAULT GETUTCDATE(),
    [Id_Usuario_Atualizacao] [int] NULL,
    CONSTRAINT [PK_Endereco] PRIMARY KEY CLUSTERED ([Id_Endereco] ASC)
);
```

**Problemas**:
- Campo `Nm_Tipo` + `Id_Referencia` cria FK "polimórfica" (anti-pattern)
- Falta constraint CHECK para validar `Sg_Estado` em lista de UFs
- Falta constraint UNIQUE para garantir 1 principal por conglomerado
- Falta índice em `(Id_Conglomerado, Fl_Excluido, Fl_Principal)`

### DDL Legado (Local)

```sql
CREATE TABLE [dbo].[Local](
    [Id_Local] [int] IDENTITY(1,1) NOT NULL,
    [Id_Conglomerado] [int] NOT NULL,
    [Id_Endereco] [int] NOT NULL,
    [Nm_Local] [varchar](200) NOT NULL,
    [Nm_Tipo] [varchar](50) NOT NULL,  -- 'Edificio', 'Andar', 'Sala', 'Rack', 'Posicao'
    [Id_Local_Pai] [int] NULL,
    [Nr_Sequencia] [int] NULL,
    [Ds_Descricao] [varchar](500) NULL,
    [Nr_Capacidade_Racks] [int] NULL,
    [Tipo_Sala] [varchar](50) NULL,    -- 'Datacenter', 'Sala_Servidores', etc
    [Fl_Excluido] [bit] NOT NULL DEFAULT 0,
    [Dt_Criacao] [datetime] NOT NULL DEFAULT GETUTCDATE(),
    [Dt_Atualizacao] [datetime] NULL,
    CONSTRAINT [PK_Local] PRIMARY KEY CLUSTERED ([Id_Local] ASC),
    CONSTRAINT [FK_Local_Pai] FOREIGN KEY([Id_Local_Pai])
        REFERENCES [dbo].[Local]([Id_Local])  -- ON DELETE CASCADE ausente!
);
```

**Problemas**:
- FK `Id_Local_Pai` permite NULL (cria órfãos sem raiz)
- Falta constraint CHECK para validar `Nm_Tipo` em enum
- Falta constraint CHECK para validar `Tipo_Sala` em enum
- Falta validação de loops (Local não pode ser pai de si mesmo)
- Sem ON DELETE CASCADE (excluir pai não propaga)

### DDL Legado (Rack)

```sql
CREATE TABLE [dbo].[Rack](
    [Id_Rack] [int] IDENTITY(1,1) NOT NULL,
    [Id_Conglomerado] [int] NOT NULL,
    [Id_Local] [int] NOT NULL,
    [Nm_Rack] [varchar](100) NOT NULL,
    [Nr_Altura_Us] [int] NOT NULL,           -- 1-48
    [Nr_Profundidade_Mm] [int] NOT NULL,     -- 600, 800, 1000
    [Nr_Peso_Maximo_Kg] [decimal](10, 2) NOT NULL,
    [Nr_Potencia_Maxima_Watts] [int] NOT NULL,
    [Nr_Peso_Atual_Kg] [decimal](10, 2) NOT NULL DEFAULT 0,
    [Nr_Potencia_Atual_Watts] [int] NOT NULL DEFAULT 0,
    [Fl_Excluido] [bit] NOT NULL DEFAULT 0,
    [Dt_Criacao] [datetime] NOT NULL DEFAULT GETUTCDATE(),
    CONSTRAINT [PK_Rack] PRIMARY KEY CLUSTERED ([Id_Rack] ASC)
);
```

**Problemas**:
- Falta constraint CHECK para validar `Nr_Altura_Us` entre 1-48
- Falta constraint CHECK para validar `Nr_Profundidade_Mm` em lista de valores
- Falta trigger para validar `Nr_Peso_Atual_Kg <= Nr_Peso_Maximo_Kg`
- Falta trigger para validar `Nr_Potencia_Atual_Watts <= Nr_Potencia_Maxima_Watts`

### DDL Legado (RackPosicao)

```sql
CREATE TABLE [dbo].[RackPosicao](
    [Id_Posicao] [int] IDENTITY(1,1) NOT NULL,
    [Id_Rack] [int] NOT NULL,
    [Nr_Posicao_U] [int] NOT NULL,
    [Id_Ativo] [int] NULL,
    [Fl_Ocupada] [bit] NOT NULL DEFAULT 0,
    CONSTRAINT [PK_RackPosicao] PRIMARY KEY CLUSTERED ([Id_Posicao] ASC)
    -- FALTA: CONSTRAINT [UQ_Rack_Posicao] UNIQUE ([Id_Rack], [Nr_Posicao_U])
);
```

**Problemas**:
- **Bug crítico**: Falta constraint UNIQUE em `(Id_Rack, Nr_Posicao_U)`, permite criar U10 duplicado no mesmo rack
- Permite `Fl_Ocupada = 0` com `Id_Ativo IS NOT NULL` (inconsistência)
- Sem validação de sobreposição (equipamento pode ocupar 3Us mas só registrar 1)

### DDL Legado (Local_Historico_Movimentacao)

```sql
CREATE TABLE [dbo].[Local_Historico_Movimentacao](
    [Id_Historico] [int] IDENTITY(1,1) NOT NULL,
    [Id_Ativo] [int] NOT NULL,
    [Id_Local_Origem] [int] NOT NULL,
    [Id_Local_Destino] [int] NOT NULL,
    [Id_Usuario_Movimentacao] [int] NOT NULL,
    [Dt_Movimentacao] [datetime] NOT NULL DEFAULT GETUTCDATE(),
    [Ds_Motivo] [varchar](500) NULL,
    [Fl_Validado] [bit] NOT NULL DEFAULT 0,
    [Id_Usuario_Validacao] [int] NULL,
    [Dt_Validacao] [datetime] NULL,
    [Id_Usuario_Criacao] [int] NOT NULL,
    [Dt_Criacao] [datetime] NOT NULL DEFAULT GETUTCDATE(),
    CONSTRAINT [PK_Local_Historico] PRIMARY KEY CLUSTERED ([Id_Historico] ASC)
    -- FALTA: Proteção contra UPDATE/DELETE (deveria ser append-only)
);
```

**Problemas**:
- **Violação de auditoria**: Permite UPDATE e DELETE (histórico deveria ser imutável)
- Falta trigger para bloquear UPDATE/DELETE após INSERT
- Falta índice em `(Id_Ativo, Dt_Movimentacao DESC)` para queries de histórico

---

## 5. STORED PROCEDURES LEGADAS

| Procedure | Descrição | Migração Moderna |
|--|--|--|
| `pa_Endereco_ListarPorConglomerado` | Lista endereços do conglomerado | SUBSTITUÍDO: LINQ query `context.Enderecos.Where(e => e.Id_Conglomerado == id && !e.Fl_Excluido)` |
| `pa_Endereco_BuscarPorCEP` | Busca endereço por CEP em tabela local | SUBSTITUÍDO: Integração com ViaCEP API |
| `pa_Local_ObterHierarquia` | Obtém árvore de locais via recursão manual | SUBSTITUÍDO: CTE recursiva ou query LINQ com `Include` |
| `pa_Rack_ObterOcupacao` | Calcula Us ocupadas em rack | SUBSTITUÍDO: LINQ aggregate query `rackPosicoes.Count(p => p.Fl_Ocupada)` |
| `pa_Movimentacao_Registrar` | Registra histórico de movimento | SUBSTITUÍDO: Insert em tabela append-only com trigger de proteção |

### Exemplo de Stored Procedure Legada

```sql
-- pa_Local_ObterHierarquia (lenta, sem CTE)
CREATE PROCEDURE [dbo].[pa_Local_ObterHierarquia]
    @Id_Local_Raiz INT
AS
BEGIN
    DECLARE @Nivel INT = 0;
    DECLARE @TabelaTemp TABLE (Id_Local INT, Nm_Local VARCHAR(200), Nivel INT);

    -- Inserir raiz
    INSERT INTO @TabelaTemp
    SELECT Id_Local, Nm_Local, @Nivel
    FROM Local
    WHERE Id_Local = @Id_Local_Raiz;

    -- Loop manual (ineficiente)
    WHILE EXISTS (SELECT 1 FROM @TabelaTemp WHERE Nivel = @Nivel)
    BEGIN
        SET @Nivel = @Nivel + 1;
        INSERT INTO @TabelaTemp
        SELECT l.Id_Local, l.Nm_Local, @Nivel
        FROM Local l
        INNER JOIN @TabelaTemp t ON l.Id_Local_Pai = t.Id_Local
        WHERE t.Nivel = @Nivel - 1;
    END

    SELECT * FROM @TabelaTemp ORDER BY Nivel, Nm_Local;
END
```

**Problemas**:
- Loop manual lento (O(n²) complexity)
- Sem paginação (retorna toda a árvore)
- Sem limite de profundidade (pode causar loop infinito se houver ciclo)

**Migração moderna**:
```sql
-- CTE recursiva (eficiente)
WITH HierarquiaLocal AS (
    SELECT Id_Local, Nm_Local, Id_Local_Pai, 0 AS Nivel
    FROM Local
    WHERE Id_Local = @Id_Local_Raiz

    UNION ALL

    SELECT l.Id_Local, l.Nm_Local, l.Id_Local_Pai, h.Nivel + 1
    FROM Local l
    INNER JOIN HierarquiaLocal h ON l.Id_Local_Pai = h.Id_Local
    WHERE h.Nivel < 10  -- Limite de profundidade
)
SELECT * FROM HierarquiaLocal;
```

---

## 6. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

Lista de regras que não estavam documentadas formalmente:

### RL-RN-001: Validação de CEP Manual

**Fonte**: `Endereco.aspx.vb`, linha 245
**Descrição**: O sistema validava CEP através de regex `^\d{5}-\d{3}$` em code-behind VB.NET, sem consulta a API externa. Se CEP estivesse no formato correto mas não existisse (ex: 99999-999), era aceito mesmo sendo inválido.
**Destino**: SUBSTITUÍDO por validação via ViaCEP API

### RL-RN-002: Endereço Principal Duplicado (Bug)

**Fonte**: `WSLocal.asmx.vb`, método `CadastrarEndereco`, linha 123
**Descrição**: Ao marcar novo endereço como principal, o sistema NÃO desmarcava o anterior automaticamente. Era possível ter 2+ endereços principais simultaneamente.
**Destino**: CORRIGIDO - Sistema moderno desmarca automaticamente o anterior

### RL-RN-003: Hierarquia de Locais Não Validada

**Fonte**: `Local.aspx.vb`, linha 189
**Descrição**: Era permitido criar Sala sem Andar, Andar sem Edifício, gerando registros órfãos. O dropdown `ddlLocalPai` permitia selecionar qualquer local sem validação de tipo.
**Destino**: CORRIGIDO - Validação de hierarquia obrigatória com FKs

### RL-RN-004: Loop em Hierarquia (Bug Crítico)

**Fonte**: `WSLocal.asmx.vb`, método `CadastrarLocal`, linha 210
**Descrição**: Local podia ser pai de si mesmo (Id_Local = Id_Local_Pai), causando loop infinito em queries recursivas.
**Destino**: CORRIGIDO - Validação impede loop e ciclos

### RL-RN-005: Posições de Rack Duplicadas

**Fonte**: `Rack.aspx.vb`, linha 312
**Descrição**: Falta de constraint UNIQUE em `(Id_Rack, Nr_Posicao_U)` permitia criar múltiplos registros para U10 no mesmo rack.
**Destino**: CORRIGIDO - Constraint UNIQUE adicionada

### RL-RN-006: Sobreposição de Equipamentos Não Detectada

**Fonte**: `Rack.aspx.vb`, método `InstalarEquipamento`, linha 405
**Descrição**: Sistema permitia instalar equipamento em U10-U12 mesmo se já existisse equipamento em U11-U13 (sobreposição em U11 e U12).
**Destino**: CORRIGIDO - Validação de sobreposição implementada

### RL-RN-007: Histórico de Movimentações Editável (Violação de Auditoria)

**Fonte**: Banco de dados, tabela `Local_Historico_Movimentacao`
**Descrição**: Tabela de histórico permitia UPDATE e DELETE, violando princípio de auditoria imutável. Registros podiam ser alterados ou apagados.
**Destino**: CORRIGIDO - Tabela append-only com trigger de proteção

### RL-RN-008: Coordenadas Geográficas Manuais

**Fonte**: `Endereco.aspx.vb`, linha 278
**Descrição**: Latitude e longitude eram inseridas manualmente pelo usuário, sem geocodificação automática. Alta taxa de erro (coordenadas 0,0 ou inválidas).
**Destino**: SUBSTITUÍDO por geocodificação automática via Google Maps API

### RL-RN-009: Tipo de Sala Não Validado para Racks

**Fonte**: `Rack.aspx.vb`, linha 198
**Descrição**: Sistema permitia criar rack em sala tipo "Escritório" ou "Reunião", violando regra de negócio de que apenas Datacenter/Sala_Servidores/CPD/Sala_Tecnica podem conter racks.
**Destino**: CORRIGIDO - Validação de tipo de sala implementada

### RL-RN-010: Sem Circuit Breaker em Integrações Externas

**Fonte**: Não implementado no legado
**Descrição**: Chamadas para Google Maps (quando habilitadas) não tinham timeout ou retry logic. Se API estivesse indisponível, sistema travava aguardando resposta indefinidamente.
**Destino**: IMPLEMENTADO - Circuit breaker com timeout 5s e retry 3x

---

## 7. GAP ANALYSIS (LEGADO x RF MODERNO)

| Item | Legado | RF Moderno | Observação |
|-----|--------|------------|------------|
| **Validação de CEP** | Manual via regex | Integração ViaCEP API | Gap: API externa não existia no legado |
| **Geocodificação** | Manual (lat/lon) | Automática via Google Maps | Gap: Feature completamente nova |
| **Hierarquia de Locais** | Fraca, permite órfãos | Rígida, FKs obrigatórias | Gap: Validação não existia |
| **Endereço Principal** | Bug (permite múltiplos) | Unicidade garantida | Gap: Correção de bug |
| **Ocupação de Racks** | Sobreposição permitida | Validação de sobreposição | Gap: Validação não existia |
| **Histórico Movimentações** | Editável (UPDATE/DELETE) | Imutável (append-only) | Gap: Auditoria aprimorada |
| **Circuit Breaker** | Inexistente | Implementado (timeout 5s) | Gap: Feature completamente nova |
| **Soft Delete** | Hard delete (DELETE direto) | Soft delete (Fl_Excluido) | Gap: Preservação de dados |
| **Multi-tenant** | Sim (Id_Conglomerado) | Sim (mantido) | Assumido do legado |
| **Auditoria** | Parcial (Dt_Atualizacao) | Completa (quem, quando, o quê) | Gap: Auditoria aprimorada |
| **Performance** | Queries N+1, sem índices | Queries otimizadas, índices compostos | Gap: Otimização nova |
| **Interface** | WebForms (postback) | Angular SPA (interativa) | Gap: Tecnologia completamente nova |

---

## 8. DECISÕES DE MODERNIZAÇÃO

### Decisão 1: Migrar de Validação Manual para ViaCEP API

**Motivo**: Validação manual via regex não garante que CEP existe no cadastro dos correios. ViaCEP API fornece validação real e autocomplete de estado/cidade/bairro.
**Impacto**: Alto - Requer integração com API externa, implementação de circuit breaker, tratamento de fallback.
**Risco**: Médio - Dependência de serviço externo.
**Mitigação**: Circuit breaker, cache de CEPs consultados, fallback para validação manual se API indisponível.

### Decisão 2: Implementar Geocodificação Automática

**Motivo**: Coordenadas manuais têm alta taxa de erro. Geocodificação automática via Google Maps Geocoding API garante precisão.
**Impacto**: Médio - Requer integração com API paga, licença do Google Maps.
**Risco**: Baixo - Feature opcional via feature flag, não bloqueia operação principal.
**Mitigação**: Geocodificação assíncrona (background job), não bloqueia salvamento de endereço.

### Decisão 3: Corrigir Hierarquia de Locais com FKs Obrigatórias

**Motivo**: Hierarquia fraca permitia órfãos e loops, causando bugs críticos.
**Impacto**: Alto - Requer refatoração de DDL, migration de dados existentes.
**Risco**: Médio - Dados legados podem ter órfãos que precisam ser corrigidos manualmente.
**Mitigação**: Script de validação pré-migration, criação de "Local Raiz Padrão" para órfãos.

### Decisão 4: Tornar Histórico de Movimentações Imutável

**Motivo**: Auditoria exige que histórico seja append-only, sem UPDATE/DELETE.
**Impacto**: Baixo - Adicionar trigger de proteção, bloquear UPDATE/DELETE via RBAC.
**Risco**: Baixo - Nenhum, melhoria de conformidade.
**Mitigação**: Nenhuma necessária.

### Decisão 5: Implementar Circuit Breaker para Integrações Externas

**Motivo**: Chamadas sem timeout podem travar sistema se API externa estiver indisponível.
**Impacto**: Médio - Implementar Polly library (.NET), configurar políticas de retry/timeout.
**Risco**: Baixo - Melhoria de resiliência.
**Mitigação**: Nenhuma necessária.

---

## 9. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Mitigação |
|------|---------|-----------|
| **Dados legados com hierarquia órfã** | Alto | Script de validação pré-migration, criação de "Local Raiz Padrão" para corrigir órfãos |
| **CEPs inválidos no banco legado** | Médio | Script de validação via ViaCEP em lote, correção manual de CEPs inválidos |
| **Coordenadas lat/lon erradas** | Médio | Re-geocodificar todos os endereços via Google Maps API após migration |
| **Posições de rack duplicadas** | Alto | Script de limpeza de duplicatas, manter apenas o registro mais recente |
| **Histórico de movimentações editado** | Baixo | Aceitar dados históricos como-estão, garantir imutabilidade apenas no sistema moderno |
| **Endereço principal duplicado** | Médio | Script de correção pré-migration, manter apenas o mais recente marcado como principal |
| **Dependência de APIs externas** | Médio | Implementar circuit breaker, cache local, feature flags para desabilitar se necessário |
| **Performance de migration** | Alto | Migration em lotes (1000 registros por vez), execution em horário de baixo tráfego |

---

## 10. RASTREABILIDADE

| Elemento Legado | Referência RF Moderno |
|----------------|---------------|
| Tabela `Endereco` | Entidade `Endereco`, RN-RF015-01, RN-RF015-02 |
| Tabela `Local` | Entidade `Local`, RN-RF015-03 |
| Tabela `Rack` | Entidade `Rack`, RN-RF015-04, RN-RF015-05 |
| Tabela `RackPosicao` | Entidade `RackPosicao`, RN-RF015-05 |
| Tabela `Local_Historico_Movimentacao` | Entidade `Local_Historico_Movimentacao`, RN-RF015-08 |
| Tela `Endereco.aspx` | UC01 (Criar Novo Endereço), UC03 (Editar Endereço) |
| Tela `Local.aspx` | UC02 (Visualizar Detalhes de Local) |
| Tela `Rack.aspx` | UC01 (Criar Rack) |
| Tela `MapaLocais.aspx` | Feature opcional (fora do escopo v2.0) |
| SP `pa_Endereco_ListarPorConglomerado` | UC00 (Listar Endereços) |
| SP `pa_Local_ObterHierarquia` | UC02 (Visualizar Hierarquia) |
| SP `pa_Movimentacao_Registrar` | Funcionalidade de movimentações |
| WebService `WSLocal.asmx` | Endpoints RESTful `/api/locais/*` |

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|------|------|----------|------|
| 1.0 | 2025-12-30 | Documentação inicial de referência ao legado para RF-015 | Agência ALC - alc.dev.br |
