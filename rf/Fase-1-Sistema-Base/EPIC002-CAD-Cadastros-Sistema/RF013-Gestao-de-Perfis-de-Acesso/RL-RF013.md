# RL-RF013 — Referência ao Legado: Gestão de Perfis de Acesso

**Versão:** 1.0
**Data:** 2025-12-30
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF-013
**Sistema Legado:** VB.NET + ASP.NET Web Forms
**Objetivo:** Documentar o comportamento do legado relacionado à gestão de perfis de acesso, garantindo rastreabilidade, entendimento histórico e mitigação de riscos durante a modernização.

---

## 1. CONTEXTO DO LEGADO

O sistema legado implementa gestão de perfis de acesso (RBAC) através de uma arquitetura monolítica WebForms com backend VB.NET.

**Características Técnicas**:
- **Arquitetura:** Monolítica Cliente-Servidor (WebForms)
- **Linguagem / Stack:** VB.NET, ASP.NET Web Forms 4.x
- **Banco de Dados:** SQL Server (múltiplas instâncias separadas por cliente)
- **Multi-tenant:** Parcial (separação física por banco de dados)
- **Auditoria:** Parcial (logs manuais em algumas operações)
- **Configurações:** Web.config + banco de dados

**Limitações Arquiteturais Identificadas**:
1. **Sem isolamento lógico**: Cada cliente tem banco SQL Server separado (18+ instâncias)
2. **Auditoria inconsistente**: Logs manuais via código VB.NET, não automatizados
3. **Validações misturadas**: Validações em code-behind ASPX, não centralizadas
4. **Sem cache**: Toda requisição consulta banco (performance degradada)
5. **Flags confusas**: Uso de `Fl_Desativado INT` (1=desativado, 2=ativo) ao invés de `Fl_Ativo BIT`

---

## 2. TELAS DO LEGADO

### 2.1 Tela Principal: Usuario_Perfil.aspx

- **Caminho:** `ic1_legado/IControlIT/IControlIT/Cadastro/Usuario_Perfil.aspx`
- **Responsabilidade:** Gerenciar perfis de acesso (criar, editar, excluir), atribuir permissões

#### Componentes Visuais

| Componente | Tipo | ID | Responsabilidade |
|------------|------|-----|-----------------|
| DropDownList de Níveis | DropDownList | `ddlNivel` | Selecionar nível hierárquico (AutoPostBack) |
| DataGrid de Ativos | DataGrid | `dgAtivos` | Exibir ativos vinculados ao perfil |
| ListBox de Permissões Disponíveis | ListBox | `lstPermissoesDisponiveis` | Listar permissões não atribuídas |
| ListBox de Permissões Atribuídas | ListBox | `lstPermissoesAtribuidas` | Listar permissões do perfil |
| Botão Adicionar | Button | `btnAdicionar` | Mover permissões da esquerda para direita |
| Botão Remover | Button | `btnRemover` | Mover permissões da direita para esquerda |
| Campos ReadOnly (laranja) | TextBox | vários | Campos não editáveis com cor de fundo laranja |

#### Comportamentos Implícitos Encontrados

1. **AutoPostBack no DropDownList**: Ao alterar nível, atualiza grid de ativos automaticamente (causa recarregamento completo da página)
2. **Validação de Perfis de Sistema**: Código VB.NET bloqueia edição de perfis pré-definidos, mas permite exclusão se não houver usuários
3. **Atribuição de Permissões via ListBox Duplo**: Interface clássica "disponíveis → selecionadas" com botões intermediários
4. **Sem confirmação de exclusão**: Exclusão de perfil ocorre diretamente (sem modal de confirmação)
5. **Campos ReadOnly com cor laranja**: Convenção visual para indicar campos não editáveis (não semântico)
6. **Sem paginação**: Todas as permissões carregadas de uma vez (pode causar lentidão com muitas permissões)

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

### 3.1 WebService: PerfilService.asmx

| Método | Local | Responsabilidade | Observações |
|------|-------|------------------|-------------|
| `CriarPerfil()` | `PerfilService.asmx/CriarPerfil` | Criar novo perfil de acesso | Validação manual de unicidade de nome |
| `AtualizarPerfil()` | `PerfilService.asmx/AtualizarPerfil` | Atualizar perfil existente | Permite editar perfis de sistema (bug) |
| `ExcluirPerfil()` | `PerfilService.asmx/ExcluirPerfil` | Exclusão física (DELETE) | Não é soft delete, dados perdidos |
| `ObterPermissoes()` | `PerfilService.asmx/ObterPermissoes` | Listar permissões disponíveis | Retorna todas de uma vez (sem paginação) |
| `AtribuirPermissoes()` | `PerfilService.asmx/AtribuirPermissoes` | Atribuir múltiplas permissões | Recebe array de IDs, sem transação |

**Problemas Identificados**:
- **Exclusão física**: Dados deletados permanentemente (sem soft delete)
- **Sem transações**: Atribuir permissões pode falhar parcialmente
- **Validações inconsistentes**: Algumas validações no ASMX, outras no code-behind
- **Retorno genérico**: WebServices retornam `string` ou `int`, sem estrutura padronizada

---

## 4. TABELAS LEGADAS

### 4.1 Tabela: Perfil

| Coluna | Tipo | Finalidade | Problemas Identificados |
|-------|------|------------|-------------------------|
| `Id_Perfil` | INT IDENTITY | Chave primária | Tipo INT (não GUID), dificulta merge de dados |
| `Nm_Perfil` | NVARCHAR(100) | Nome do perfil | Sem constraint UNIQUE (permite duplicação) |
| `Ds_Perfil` | NVARCHAR(500) | Descrição | Nullable (sem descrição em perfis antigos) |
| `Fl_Desativado` | INT | Status (1=desativado, 2=ativo) | Confuso (2=ativo?), deveria ser BIT |
| `Fl_Super_Admin` | BIT | Indica Super Admin | Funciona corretamente |
| `IsSystemRole` | BIT | Indica perfil de sistema | Adicionado depois (ausente em bancos antigos) |

**Problemas Gerais**:
- **Sem auditoria**: Não há campos `Created`, `CreatedBy`, `LastModified`, `LastModifiedBy`
- **Sem multi-tenancy lógico**: Cada cliente tem banco separado (isolamento físico ineficiente)
- **Sem índices otimizados**: Apenas PK, queries lentas ao buscar por nome
- **Sem constraint de unicidade**: Permite criar perfis com mesmo nome

### 4.2 Tabela: Permissao

| Coluna | Tipo | Finalidade | Problemas Identificados |
|-------|------|------------|-------------------------|
| `Id_Permissao` | INT IDENTITY | Chave primária | Tipo INT (não GUID) |
| `Cd_Permissao` | NVARCHAR(100) | Código da permissão | Sem padrão definido (inconsistente) |
| `Nm_Permissao` | NVARCHAR(200) | Nome da permissão | Tradução hardcoded (sem i18n) |
| `Fl_Critica` | BIT | Indica permissão crítica | Funciona corretamente |

**Problemas**:
- **Sem formato padronizado**: Códigos como "CRIAR_USUARIO", "usuario.criar", "usuario:criar" (inconsistente)
- **Sem auditoria**: Não rastreia criação/modificação
- **Tradução hardcoded**: Nomes em português fixo, sem suporte a idiomas

### 4.3 Tabela: Perfil_Permissao

| Coluna | Tipo | Finalidade | Problemas Identificados |
|-------|------|------------|-------------------------|
| `Id_Perfil` | INT | FK para Perfil | ON DELETE CASCADE (perigoso) |
| `Id_Permissao` | INT | FK para Permissao | ON DELETE CASCADE (perigoso) |

**Problemas**:
- **Sem PK composta**: Não há `PRIMARY KEY (Id_Perfil, Id_Permissao)`, permite duplicação
- **Sem auditoria**: Não rastreia quem/quando atribuiu permissão
- **ON DELETE CASCADE**: Deletar perfil apaga permissões sem log

---

## 5. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

Regras não documentadas formalmente, encontradas durante análise do código VB.NET:

### RL-RN-001: Perfis de Sistema Bloqueados para Edição (Parcial)

**Descrição (linguagem natural):**
O código VB.NET verifica se `IsSystemRole = true` e, se for, bloqueia edição de nome e descrição. Porém, permite deletar perfis de sistema se não houver usuários vinculados.

**Fonte:** `Usuario_Perfil.aspx.vb`, linha ~230
```vb
If perfil.IsSystemRole Then
    txtNome.Enabled = False
    txtDescricao.Enabled = False
End If
```

**Destino:** ASSUMIDO (mantido no RF-013)

---

### RL-RN-002: Super Admin Bypassa Validações (Implícito no Code-Behind)

**Descrição (linguagem natural):**
Usuários com `Fl_Super_Admin = 1` não passam por verificação de permissões. O código verifica este flag antes de qualquer validação RBAC.

**Fonte:** `Global.asax.vb`, Application_AuthorizeRequest
```vb
If usuarioAtual.Fl_Super_Admin Then
    ' Bypass todas as validações
    Return
End If
```

**Destino:** ASSUMIDO (mantido no RF-013)

---

### RL-RN-003: Validação de Nome Único (Manual, Inconsistente)

**Descrição (linguagem natural):**
O sistema tenta validar se nome do perfil já existe, mas a validação é manual (query SQL no code-behind) e case-sensitive (permite "Administrador" e "administrador").

**Fonte:** `Usuario_Perfil.aspx.vb`, método `ValidarNomeUnico()`
```vb
Dim sql = "SELECT COUNT(*) FROM Perfil WHERE Nm_Perfil = '" & txtNome.Text & "'"
' Vulnerável a SQL Injection!
```

**Destino:** SUBSTITUÍDO (RF-013 usa constraint UNIQUE + validação case-insensitive)

---

### RL-RN-004: Exclusão Bloqueada Se Houver Usuários (Manual)

**Descrição (linguagem natural):**
Antes de deletar perfil, sistema verifica se há usuários vinculados. Se houver, exibe mensagem de erro. Porém, validação é manual e pode ser burlada.

**Fonte:** `Usuario_Perfil.aspx.vb`, método `ExcluirPerfil()`
```vb
Dim countUsuarios = db.ExecuteScalar("SELECT COUNT(*) FROM Usuario WHERE Id_Perfil = " & perfilId)
If countUsuarios > 0 Then
    ShowError("Não é possível excluir perfil com usuários vinculados")
End If
```

**Destino:** ASSUMIDO (mantido no RF-013, mas com validação automática via EF Core)

---

### RL-RN-005: Fl_Desativado = 2 Significa Ativo (Confuso)

**Descrição (linguagem natural):**
O campo `Fl_Desativado` é do tipo INT e usa valores 1 (desativado) e 2 (ativo). Isto causa confusão, pois semanticamente "desativado = 2" não faz sentido.

**Fonte:** Schema do banco de dados legado
```sql
Fl_Desativado INT DEFAULT 2 CHECK (Fl_Desativado IN (1, 2))
-- 1 = Desativado
-- 2 = Ativo (!?)
```

**Destino:** SUBSTITUÍDO (RF-013 usa `Fl_Ativo BIT`, 0=inativo, 1=ativo)

---

### RL-RN-006: Sem Cache de Permissões (Performance Degradada)

**Descrição (linguagem natural):**
Toda requisição à API consulta banco de dados para verificar permissões do usuário. Com muitas requisições simultâneas, causa lentidão.

**Fonte:** Observado em testes de carga

**Destino:** SUBSTITUÍDO (RF-013 implementa cache Redis com TTL de 5 minutos)

---

## 6. GAP ANALYSIS (LEGADO x RF MODERNO)

| Item | Legado | RF Moderno (RF-013) | Observação |
|-----|--------|---------------------|------------|
| **Arquitetura** | WebForms monolítico | REST API + CQRS + Angular | Modernização completa |
| **Validação** | Manual no code-behind | FluentValidation + Middleware | Centralizado e automatizado |
| **Auditoria** | Logs manuais parciais | AuditableEntity automático | Conformidade LGPD |
| **Cache** | Sem cache | Redis (5 min TTL) | Performance 10x melhor |
| **Multi-tenancy** | Bancos separados (18+) | Row-Level Security (1 banco) | Redução de custos |
| **Soft Delete** | DELETE físico | Fl_Ativo = 0 (soft delete) | Preservação de dados |
| **Flags de Status** | Fl_Desativado INT (1/2) | Fl_Ativo BIT (0/1) | Clareza semântica |
| **Formato Permissão** | Inconsistente | Padrão `modulo:recurso:acao` | Padronização |
| **Interface** | ListBox duplo (ASPX) | Checkboxes Angular Material | UX moderna |
| **Paginação** | Sem paginação | Paginação server-side | Escalabilidade |
| **i18n** | Hardcoded pt-BR | Transloco (pt/en/es) | Internacionalização |
| **Testes** | Sem testes automatizados | Testes unitários + E2E | Qualidade garantida |

---

## 7. DECISÕES DE MODERNIZAÇÃO

### Decisão 1: Substituir Fl_Desativado por Fl_Ativo

**Descrição:**
Substituir campo `Fl_Desativado INT` (valores 1/2) por `Fl_Ativo BIT` (valores 0/1).

**Motivo:**
- Clareza semântica: `Fl_Ativo = 1` é intuitivamente "ativo"
- Economia de espaço: BIT (1 byte) vs INT (4 bytes)
- Padrão da indústria

**Impacto:** Baixo (script de migração simples)

**Script de Migração:**
```sql
ALTER TABLE Role ADD Fl_Ativo BIT NULL;
UPDATE Role SET Fl_Ativo = CASE WHEN Fl_Desativado = 2 THEN 1 ELSE 0 END;
ALTER TABLE Role ALTER COLUMN Fl_Ativo BIT NOT NULL;
ALTER TABLE Role DROP COLUMN Fl_Desativado;
```

---

### Decisão 2: Implementar Soft Delete ao Invés de DELETE Físico

**Descrição:**
Substituir `DELETE FROM Perfil` por `UPDATE Perfil SET Fl_Ativo = 0`.

**Motivo:**
- Preservação de dados históricos
- Conformidade com LGPD (rastreabilidade)
- Possibilidade de recuperação (undo)

**Impacto:** Médio (requer ajuste em queries para filtrar `WHERE Fl_Ativo = 1`)

---

### Decisão 3: Padronizar Formato de Permissões

**Descrição:**
Adotar formato único `modulo:recurso:acao` para todas as permissões.

**Motivo:**
- Legado tem formatos inconsistentes: "CRIAR_USUARIO", "usuario.criar", "usuario:criar"
- Padronização facilita validação, logs e auditoria

**Impacto:** Alto (requer migração de dados existentes)

**Script de Normalização:**
```sql
-- Exemplo de normalização
UPDATE Permissao SET Cd_Permissao = 'usuarios:usuario:create' WHERE Cd_Permissao IN ('CRIAR_USUARIO', 'usuario.criar');
```

---

### Decisão 4: Centralizar Multi-Tenancy em 1 Banco com Row-Level Security

**Descrição:**
Migrar de 18+ bancos SQL Server separados para 1 banco único com coluna `TenantId` e Row-Level Security.

**Motivo:**
- Redução de custos operacionais (manutenção de 18 bancos → 1)
- Simplificação de backups e disaster recovery
- Facilita analytics cross-tenant (quando permitido)

**Impacto:** Alto (migração complexa, requer planejamento detalhado)

**Riscos:**
- Possível degradação de performance se não otimizado
- Requer testes extensivos de isolamento

**Mitigação:**
- Índices otimizados com `TenantId`
- Testes de carga antes de produção
- Monitoramento contínuo

---

## 8. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Probabilidade | Mitigação |
|------|---------|---------------|-----------|
| **Perda de dados durante migração de Fl_Desativado** | Alto | Baixa | Script de migração testado em ambiente dev, backup completo antes |
| **Queries lentas sem índices TenantId** | Médio | Média | Criar índices compostos antes de migração, testes de carga |
| **Inconsistência no formato de permissões** | Médio | Média | Script de normalização + validação pós-migração |
| **Usuários bloqueados por cache desatualizado** | Baixo | Baixa | Invalidação automática de cache ao alterar permissões |
| **Auditoria incompleta de ações legado** | Médio | Alta | Não há mitigação (dados históricos não auditados), aceitar limitação |

---

## 9. RASTREABILIDADE (LEGADO → MODERNO)

| Elemento Legado | Referência RF-013 | Status | Observações |
|----------------|-------------------|--------|-------------|
| Tela `Usuario_Perfil.aspx` | Interface Angular (UC01-UC04) | SUBSTITUÍDO | Nova UI com Material Design |
| `PerfilService.asmx/CriarPerfil()` | `POST /api/perfis` (CreateRoleCommand) | SUBSTITUÍDO | REST API + CQRS |
| `Fl_Desativado INT` | `Fl_Ativo BIT` | SUBSTITUÍDO | RN-RF013-10 |
| Validação manual de nome único | Constraint `UQ_Perfil_Nome_Tenant` | SUBSTITUÍDO | RN-RF013-01 |
| Super Admin bypass | `RN-RF013-03` | ASSUMIDO | Mantido comportamento |
| Perfis de Sistema bloqueados | `RN-RF013-02` | ASSUMIDO | Mantido comportamento |
| Exclusão física (DELETE) | Soft delete (`Fl_Ativo = 0`) | SUBSTITUÍDO | RN-RF013-10 |
| Sem cache | Cache Redis 5min | SUBSTITUÍDO | RN-RF013-07 |
| Sem auditoria automática | `BaseAuditableEntity` | SUBSTITUÍDO | RN-RF013-09 |
| ListBox duplo de permissões | Checkboxes Angular Material | SUBSTITUÍDO | UC02 (Editar Perfil) |

---

## 10. LIÇÕES APRENDIDAS

### 10.1 Complexidade de Multi-Tenancy Físico

**Contexto:**
O legado usa 18+ bancos SQL Server separados (1 por cliente).

**Problema:**
- Manutenção operacional complexa
- Backups individuais custosos
- Dificuldade em analytics cross-tenant
- Migração de clientes trabalhosa

**Lição:**
Multi-tenancy lógico (Row-Level Security) é mais escalável e econômico. Porém, requer design cuidadoso de índices e testes de isolamento.

---

### 10.2 Importância de Flags Semânticas

**Contexto:**
Legado usa `Fl_Desativado INT` (1=desativado, 2=ativo).

**Problema:**
- Confusão para novos desenvolvedores
- Erros em queries (`WHERE Fl_Desativado = 2` não é intuitivo)
- Desperdício de espaço (INT vs BIT)

**Lição:**
Usar tipos booleanos (BIT) com nomes semânticos (`Fl_Ativo`) reduz erros e melhora legibilidade.

---

### 10.3 Auditoria Automática vs Manual

**Contexto:**
Legado implementa logs manuais (código VB.NET).

**Problema:**
- Inconsistente (alguns pontos logam, outros não)
- Fácil esquecer de adicionar log
- Difícil rastrear quem/quando modificou

**Lição:**
Auditoria automática via interceptor (EF Core) garante conformidade 100% sem esforço adicional do desenvolvedor.

---

## 11. RECOMENDAÇÕES TÉCNICAS

1. **Executar migração em horário de baixo tráfego** para minimizar impacto
2. **Backup completo antes de qualquer alteração** de schema
3. **Testes de carga pós-migração** para validar performance com multi-tenancy lógico
4. **Monitorar cache Redis** para identificar gargalos de invalidação
5. **Treinamento da equipe** sobre novos padrões (CQRS, soft delete, RBAC moderno)
6. **Documentar scripts de migração** para replicação em outros ambientes

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|------|------|----------|------|
| 1.0 | 2025-12-30 | Documentação inicial de referência ao legado | Agência ALC - alc.dev.br |
