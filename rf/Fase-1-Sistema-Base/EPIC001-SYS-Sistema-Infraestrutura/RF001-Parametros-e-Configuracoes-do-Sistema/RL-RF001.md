# RL-RF001: Referência ao Legado - Sistema de Parâmetros e Configurações

**RF Relacionado**: RF-001 - Sistema de Parâmetros e Configurações Centralizadas
**Versão**: 1.0
**Data**: 2025-12-29
**Autor**: Agência ALC - alc.dev.br

---

## 1. SISTEMA LEGADO

**Tecnologia**: VB.NET + ASP.NET Web Forms
**Arquitetura**: Monolítica WebForms
**Banco de Dados**: SQL Server
**Multi-tenant**: Não suportado
**Auditoria**: Parcial (apenas logs em `tbl_Parametros_Log`)

---

## 2. TABELAS LEGADO → MODERNAS

| Tabela Legado | Tabela Moderna | Mudanças Principais |
|---------------|----------------|---------------------|
| `tbl_Parametros` | `Sistema_Parametro` | Adiciona suporte a múltiplos tipos de dados, criptografia AES-256, validações robustas (regex, min/max, opções válidas) |
| `tbl_Config_Email` | `Sistema_Configuracao_Email` | Adiciona suporte a múltiplos providers (SendGrid, AWS SES), criptografia de senha, teste de envio |
| N/A | `Sistema_Feature_Flag` | Tabela nova (inexistente no legado) |
| N/A | `Sistema_Limite_Uso` | Tabela nova (inexistente no legado) |
| `tbl_Parametros_Log` | `Sistema_Parametro_Historico` | Adiciona campos de auditoria avançada (IP, User-Agent, motivo da alteração, diff JSON) |

---

## 3. MUDANÇAS DE COMPORTAMENTO CRÍTICAS

### 3.1 Criptografia

**Legado**: Dados sensíveis (senhas, API keys) armazenados em **texto plano** (vulnerabilidade crítica de segurança)

**Moderno**: Todos os dados sensíveis criptografados com **AES-256**
- Criptografia transparente ao salvar
- Descriptografia apenas quando necessário
- Valores mascarados (`*****`) na interface
- Acesso descriptografado apenas para Super Admin com permissão `SYS.PARAMETROS.VIEW_SENSITIVE`

**Destino**: SUBSTITUÍDO (por questão de segurança crítica)

---

### 3.2 Feature Flags

**Legado**: Funcionalidade **inexistente**. Ativação/desativação de features requeria deploy de nova versão.

**Moderno**: Sistema completo de Feature Flags com:
- Rollout gradual (por % usuários, lista específica, período)
- Ativação/desativação em runtime (sem restart)
- Multi-tenant (flags globais ou específicas por conglomerado)

**Destino**: NOVA FUNCIONALIDADE (não há equivalente legado)

---

### 3.3 Validação de Tipo

**Legado**: **Tudo armazenado como string** (campo `Vl_Parametro varchar(MAX)`)
- Sem validação de tipo
- Conversão implícita no código
- Erros de conversão em runtime

**Moderno**: Tipos de dados tipados com validação estrita
- String, Integer, Decimal, Boolean, Date, JSON
- Validação antes de persistir (fail-fast)
- Mensagens de erro claras por tipo
- Campos separados por tipo (`Vl_String`, `Vl_Inteiro`, `Vl_Decimal`, `Vl_Boolean`, `Vl_Data`, `Vl_Json`)

**Destino**: SUBSTITUÍDO (elimina erros de conversão)

---

### 3.4 Cache

**Legado**: **Sem cache** (consulta banco de dados a cada acesso ao parâmetro)
- Alto impacto de performance
- Load desnecessário no SQL Server

**Moderno**: Cache distribuído (Redis) com invalidação automática
- Cache de 1 hora por padrão
- Invalidação ao alterar parâmetro
- Reduz latência de 50ms → 2ms

**Destino**: SUBSTITUÍDO (otimização crítica de performance)

---

### 3.5 Limites de Uso

**Legado**: **Funcionalidade inexistente**. Sem controle de quantidades máximas por cliente.

**Moderno**: Sistema completo de Limites de Uso para SaaS multi-tenant
- Limites configuráveis: usuários, ativos, storage (MB), API calls/dia
- Monitoramento em tempo real (`Uso_Atual`)
- Alertas automáticos ao atingir percentual de alerta
- Bloqueio de operações ao atingir 100% do limite

**Destino**: NOVA FUNCIONALIDADE (requisito de SaaS multi-tenant)

---

## 4. COMPARATIVO LEGADO VS MODERNO

| Aspecto | Legado | Moderno |
|---------|--------|---------|
| **Multi-Tenant** | ❌ Não suportado | ✅ Configuração por conglomerado |
| **Tipos de Dados** | ❌ Apenas strings | ✅ String, Integer, Decimal, Boolean, Date, JSON |
| **Validação** | ❌ Sem validação | ✅ Regex, min/max, opções válidas, tipo |
| **Criptografia** | ❌ Senhas em texto plano | ✅ AES-256 para dados sensíveis |
| **Feature Flags** | ❌ Não existe | ✅ Feature flags com rollout gradual |
| **Auditoria** | ⚠️ Parcial (sem histórico completo) | ✅ Histórico completo de alterações (7 anos LGPD) |
| **Interface** | ❌ Edição manual de arquivo Web.config | ✅ UI administrativa com validação |
| **Hot Reload** | ❌ Requer restart da aplicação | ✅ Configuração dinâmica em runtime |
| **Versionamento** | ❌ Sem controle de versões | ✅ Histórico de versões com rollback |
| **Cache** | ❌ Sem cache (consulta banco sempre) | ✅ Redis com invalidação automática |
| **Segurança** | ⚠️ Permissões básicas | ✅ RBAC com matriz de permissões detalhada |

---

## 5. RISCOS DE MIGRAÇÃO

### 5.1 Migração de Dados Sensíveis

**Risco**: Dados sensíveis no legado estão em **texto plano**. Migração pode expor credenciais.

**Mitigação**:
1. Executar migração em ambiente isolado
2. Criptografar TODOS os valores sensíveis antes de inserir no banco moderno
3. Validar que NENHUM valor sensível permaneceu descriptografado
4. Deletar dados sensíveis do banco legado após migração confirmada

---

### 5.2 Validação de Tipos

**Risco**: Parâmetros legado armazenados como string podem conter valores inválidos para tipo declarado (ex: "ABC" para tipo Integer).

**Mitigação**:
1. Executar script de validação pré-migração
2. Identificar parâmetros com valores incompatíveis com tipo esperado
3. Corrigir manualmente ou marcar como `Tipo_Dado = String` (fallback)
4. Re-validar após migração

---

### 5.3 Compatibilidade de Código

**Risco**: Código legado pode estar lendo parâmetros de `tbl_Parametros` diretamente. Após migração, código legado quebrará.

**Mitigação**:
1. Identificar TODOS os pontos no código legado que consultam `tbl_Parametros`
2. Criar VIEW no SQL Server: `CREATE VIEW tbl_Parametros AS SELECT * FROM Sistema_Parametro` (compatibilidade temporária)
3. Planejar refatoração gradual do código legado para usar API moderna
4. Manter VIEW por 6 meses até refatoração completa

---

## 6. FUNCIONALIDADES DESCARTADAS DO LEGADO

### 6.1 Edição Manual de Web.config

**Descrição**: No legado, alguns parâmetros eram editados manualmente no arquivo `Web.config`.

**Motivo do Descarte**:
- Requer acesso ao servidor (violação de segurança)
- Requer restart da aplicação
- Sem auditoria (não sabemos quem alterou)
- Sem versionamento

**Alternativa no Moderno**: UI administrativa com auditoria completa, hot reload, validação e controle de acesso.

**Destino**: DESCARTADO (prática insegura e não escalável)

---

### 6.2 Parâmetros Hard-coded

**Descrição**: Alguns parâmetros estavam fixos no código VB.NET (ex: `Const TIMEOUT_SEGUNDOS = 30`).

**Motivo do Descarte**:
- Impossível alterar sem recompilação
- Diferentes valores por ambiente (dev, staging, prod) requer branches de código

**Alternativa no Moderno**: Todos os parâmetros gerenciáveis via UI ou API, sem necessidade de deploy.

**Destino**: DESCARTADO (anti-pattern)

---

## 7. SCRIPT DE MIGRAÇÃO DE DADOS

```sql
-- Migração de tbl_Parametros → Sistema_Parametro
-- ATENÇÃO: Executar APÓS validação de tipos

INSERT INTO Sistema_Parametro (
    Id,
    Id_Conglomerado,
    Cd_Parametro,
    Nm_Parametro,
    Ds_Parametro,
    Tipo_Dado,
    Categoria,
    Vl_String,
    Fl_Sensivel,
    Fl_Sistema,
    Fl_Obrigatorio,
    Dt_Criacao,
    Id_Usuario_Criacao
)
SELECT
    NEWID() AS Id,
    1 AS Id_Conglomerado, -- Conglomerado padrão (ajustar conforme necessário)
    Cd_Parametro,
    Nm_Parametro,
    ISNULL(Ds_Parametro, '') AS Ds_Parametro,
    'String' AS Tipo_Dado, -- Legado só tinha strings
    'Sistema' AS Categoria, -- Categoria padrão (ajustar conforme necessário)
    CASE
        WHEN Fl_Sensivel = 1 THEN dbo.fn_CriptografarAES256(Vl_Parametro) -- Criptografar sensíveis
        ELSE Vl_Parametro
    END AS Vl_String,
    ISNULL(Fl_Sensivel, 0) AS Fl_Sensivel,
    ISNULL(Fl_Sistema, 0) AS Fl_Sistema,
    1 AS Fl_Obrigatorio, -- Assumir todos obrigatórios por segurança
    Dt_Criacao,
    Id_Usuario_Criacao
FROM tbl_Parametros
WHERE Fl_Excluido = 0; -- Não migrar excluídos

-- Verificar se há valores sensíveis não criptografados
SELECT Cd_Parametro, Vl_String
FROM Sistema_Parametro
WHERE Fl_Sensivel = 1
  AND Vl_String NOT LIKE 'ENC:%'; -- Prefixo de valores criptografados
-- Se retornar algum registro → ERRO CRÍTICO, não prosseguir

-- Migração de tbl_Config_Email → Sistema_Configuracao_Email
INSERT INTO Sistema_Configuracao_Email (
    Id,
    Id_Conglomerado,
    Provedor,
    Servidor_Smtp,
    Porta_Smtp,
    Usuario,
    Senha,
    Fl_Usar_Ssl,
    Email_Remetente,
    Nome_Remetente,
    Fl_Principal,
    Dt_Criacao,
    Id_Usuario_Criacao
)
SELECT
    NEWID() AS Id,
    1 AS Id_Conglomerado,
    'SMTP' AS Provedor, -- Legado só tinha SMTP
    Servidor_Smtp,
    Porta_Smtp,
    Usuario,
    dbo.fn_CriptografarAES256(Senha) AS Senha, -- Criptografar senha
    ISNULL(Fl_Usar_Ssl, 1) AS Fl_Usar_Ssl,
    Email_Remetente,
    Nome_Remetente,
    1 AS Fl_Principal, -- Assumir única configuração como principal
    Dt_Criacao,
    Id_Usuario_Criacao
FROM tbl_Config_Email
WHERE Fl_Excluido = 0;

-- Não há migração para Sistema_Feature_Flag e Sistema_Limite_Uso (funcionalidades novas)
```

---

## 8. CHECKLIST DE VALIDAÇÃO PÓS-MIGRAÇÃO

- [ ] Todos os parâmetros sensíveis estão criptografados (verificar prefixo `ENC:`)
- [ ] Nenhum parâmetro sensível aparece em logs
- [ ] VIEW `tbl_Parametros` criada para compatibilidade com código legado
- [ ] Código legado consegue ler parâmetros via VIEW (teste em staging)
- [ ] UI moderna consegue listar, criar, editar e excluir parâmetros
- [ ] Auditoria funcionando (histórico registra todas as alterações)
- [ ] Cache funcionando (verificar Redis)
- [ ] Feature flags criadas para funcionalidades críticas
- [ ] Limites de uso configurados para todos os conglomerados
- [ ] Alertas de limite de uso sendo enviados corretamente
- [ ] Backup do banco legado realizado antes de deletar dados

---

## 9. PLANO DE ROLLBACK

Se a migração falhar ou apresentar problemas críticos:

1. **Imediato** (até 1 hora após migração):
   - Restaurar backup do banco legado
   - Reverter deploy do código moderno
   - Reativar aplicação legada

2. **Parcial** (após 1 hora, identificando problema específico):
   - Manter código moderno
   - Criar dados faltantes via API moderna
   - Executar script de correção de dados

3. **Não permitir rollback** (após 7 dias):
   - Dados sensíveis já descriptografados (legado inseguro)
   - Rollback exigiria re-criptografia (risco de perda de dados)

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|------|------|----------|------|
| 1.0 | 2025-12-29 | Criação da referência ao legado durante migração para nova governança | Agência ALC - alc.dev.br |
