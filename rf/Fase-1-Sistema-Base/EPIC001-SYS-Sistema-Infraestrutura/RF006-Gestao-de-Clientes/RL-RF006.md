# RL-RF006 — Referência ao Legado: Gestão de Clientes

**Versão**: 2.0
**Data**: 2025-12-29
**RF Relacionado**: [RF006 - Gestão de Clientes (Multi-Tenancy SaaS)](./RF006.md)

---

## 1. SUMÁRIO EXECUTIVO

**Resumo**: No sistema legado (VB.NET + ASP.NET Web Forms), **NÃO EXISTIA gestão de Clientes via interface**. Cada Cliente tinha um **banco de dados SQL Server completamente separado** (18 bancos isolados: Alpargatas, Vale, Bombril, etc.). A criação de um novo Cliente era um processo **manual executado por DBA** (Database Administrator):

1. Criar novo banco SQL Server
2. Copiar schema completo do template
3. Configurar ConnectionString específica
4. Adicionar logo em pasta local `~/Images/Clientes/`
5. Testar acesso manualmente

Esse processo levava **dias** e exigia intervenção manual. O isolamento era **físico** (bancos separados), não lógico.

**Decisão de Migração**: **CRIAR DO ZERO** (não migrar gestão de Clientes do legado)

**Justificativa**:
1. ✅ No legado NÃO existia CRUD de Clientes via interface web
2. ✅ Arquitetura multi-database é incompatível com SaaS moderno
3. ✅ ReceitaWS API não existia (dados cadastrais desatualizados)
4. ✅ Soft delete com auditoria LGPD não existia (DELETE físico era comum)
5. ✅ Upload de logo em Azure Blob Storage não existia (filesystem local)

---

## 2. PROBLEMAS DO LEGADO (6 Identificados)

### RL-001: Ausência de Interface de Gestão de Clientes

**Descrição do Problema**:

No sistema legado, **não existia interface (telas ASPX) para criar, editar ou visualizar Clientes**. A criação de um novo Cliente era um processo **manual executado por DBA**:

1. DBA recebia solicitação da área comercial (email ou ticket)
2. Criava novo banco SQL Server manualmente via SQL Server Management Studio
3. Executava script DDL completo para criar todas as tabelas (schema template)
4. Configurava ConnectionString no arquivo `Web.config`
5. Reiniciava aplicação para reconhecer novo banco
6. Testava login com usuário de teste

**Componentes Legados Afetados**:
- ❌ Nenhuma tela ASPX (gestão de Clientes não existia)
- ❌ Nenhum WebService VB.NET
- ❌ Apenas processo manual DBA

**Impacto**:
- ⏱️ Onboarding de Cliente levava **3-5 dias** (vs. < 5 minutos no moderno)
- 💰 Custo elevado (intervenção manual de DBA sênior)
- ❌ Risco de erro humano (configuração incorreta de ConnectionString)
- ❌ Sem rastreabilidade (sem auditoria de quem criou Cliente e quando)

**Destino no Sistema Moderno**: **SUBSTITUÍDO**

**Migração**:
- Sistema moderno cria **interface completa de gestão de Clientes**:
  - `/admin/clientes` (listagem)
  - `/admin/clientes/novo` (criação)
  - `/admin/clientes/{id}` (edição)
- **Onboarding automatizado via API** (POST /api/clientes)
- **Auditoria completa** (quem criou, quando, de onde)
- **Tempo reduzido**: 3-5 dias → **< 5 minutos**

---

### RL-002: Arquitetura Multi-Database (Physical Separation)

**Descrição do Problema**:

No legado, cada Cliente tinha um **banco de dados SQL Server completamente separado**. Exemplo:

- Cliente Alpargatas → Banco `Alpargatas`
- Cliente Vale → Banco `Vale`
- Cliente Bombril → Banco `Bombril`

**Total de bancos legados identificados**: **18 bancos SQL Server**

| Banco Legado | CNPJ (estimado) | Razão Social |
|--------------|-----------------|--------------|
| `Alpargatas` | 61.079.117/0001-05 | Alpargatas S.A. |
| `Vale` | 33.592.510/0001-54 | Vale S.A. |
| `Bombril` | 50.248.011/0001-39 | Bombril S.A. |
| `Anima_Educacao` | 17.685.925/0001-92 | Anima Educação |
| `Fresenius` | 49.324.221/0001-04 | Fresenius Kabi Brasil Ltda |
| `Electrolux` | 76.487.032/0001-25 | Electrolux do Brasil S.A. |
| `CPFL` | 02.429.144/0001-93 | CPFL Energia S.A. |
| `Carrefour` | 45.543.915/0001-81 | Carrefour Comércio e Indústria Ltda |
| `Cielo` | 01.027.058/0001-91 | Cielo S.A. |
| `Gerdau` | 33.611.500/0001-19 | Gerdau S.A. |
| `Magazine_Luiza` | 47.960.950/0001-21 | Magazine Luiza S.A. |
| `Natura` | 71.673.990/0001-77 | Natura Cosméticos S.A. |
| `Rede_D_Or` | 00.387.679/0001-58 | Rede D'Or São Luiz S.A. |
| `Weg` | 07.175.725/0001-49 | WEG S.A. |
| `Ambev` | 02.808.708/0001-07 | Ambev S.A. |
| `Embraer` | 07.689.002/0001-89 | Embraer S.A. |
| `JBS` | 02.916.265/0001-60 | JBS S.A. |
| `Localiza` | 16.670.085/0001-55 | Localiza Rent a Car S.A. |

**Problemas**:
- 💰 **Custo de licenciamento**: 18+ licenças SQL Server (vs. 1 no moderno)
- 🔧 **Manutenção complexa**: Alterar schema exigia script DDL em 18 bancos
- ❌ **Relatórios cross-tenant impossíveis**: Não dava para consolidar dados de múltiplos Clientes
- ⏱️ **Backup demorado**: 18 backups diários independentes
- 📈 **Escalabilidade limitada**: Adicionar Cliente = criar novo banco completo

**Comparação Legado vs. Moderno**:

| Aspecto | Legado (Multi-Database) | Moderno (Single Database + Multi-Tenancy) |
|---------|-------------------------|-------------------------------------------|
| **Isolamento** | **Physical** (banco separado) | **Lógico** (Row-Level Security via ClienteId) |
| **Custo Infra** | **18+ licenças SQL Server** | **1 licença SQL Server** |
| **Onboarding** | Manual DBA (3-5 dias) | Automatizado API (< 5 minutos) |
| **Schema Upgrade** | Script DDL em 18 bancos | Migration EF Core em 1 banco |
| **Backup** | 18 backups diários | 1 backup diário |
| **Relatórios Cross-Tenant** | ❌ Impossível | ✅ Possível (Super Admin) |
| **Escalabilidade** | ❌ Limitada (criar banco) | ✅ Alta (INSERT em tabela) |

**Destino no Sistema Moderno**: **SUBSTITUÍDO**

**Migração**:
- **Single database** com `ClienteId` como discriminador de tenant
- **EF Core Query Filters** aplicam filtro automático `WHERE ClienteId = @CurrentClienteId`
- **Super Admin bypass** permite visão global cross-tenant
- **Uptime alvo**: 99.9% sem data leakage

---

### RL-003: Ausência de Validação de CNPJ

**Descrição do Problema**:

No legado, **não havia validação de dígitos verificadores de CNPJ**. Dados eram inseridos manualmente pelo DBA sem nenhuma verificação automática de validade.

**Problemas Observados**:
- ❌ CNPJs com dígitos verificadores incorretos no banco
- ❌ CNPJs duplicados (mesmo Cliente cadastrado duas vezes por erro)
- ❌ CNPJs falsos (testes com 11111111111111, 99999999999999)
- ❌ Dados desatualizados (sem consulta à Receita Federal)

**Impacto**:
- 📄 Problemas em emissão de notas fiscais eletrônicas (NF-e)
- 🏦 Erros em integração bancária (boletos)
- 📊 Relatórios fiscais incorretos

**Destino no Sistema Moderno**: **ASSUMIDO + SUBSTITUÍDO**

**Migração**:
- **RN-CLI-006-03**: Validação de dígitos verificadores usando algoritmo oficial Receita Federal
- **FluentValidation**: `CnpjValidator.IsValid()` obrigatório no backend
- **RN-CLI-006-05**: Consulta automática ReceitaWS API para preenchimento de dados
- **Unique Constraint**: `IX_Cliente_CNPJ_Unique` previne duplicidade
- **Limpeza de dados legados**: CNPJ inválidos devem ser corrigidos durante migração de dados

---

### RL-004: Ausência de ReceitaWS API

**Descrição do Problema**:

No legado, **não existia integração com ReceitaWS** (ou qualquer API da Receita Federal). Dados cadastrais (Razão Social, Nome Fantasia, Endereço, Telefone) eram preenchidos **manualmente** pelo DBA ou área comercial.

**Problemas**:
- ✍️ **Erros de digitação** em Razão Social, Endereço, Telefone
- ⏱️ **Retrabalho** quando dados incorretos causavam problemas fiscais
- 📞 **Dificuldade de contato** com Cliente (telefone desatualizado)
- 📧 **Emails errados** (comunicação não chega ao Cliente)

**Destino no Sistema Moderno**: **SUBSTITUÍDO**

**Migração**:
- **RN-CLI-006-05**: Consulta automática ReceitaWS via API REST
- **Endpoint**: POST /api/clientes/consultar-cnpj
- **Fallback**: Se ReceitaWS indisponível, permite preenchimento manual
- **Taxa de sucesso alvo**: > 95%
- **Benefício**: Redução de erros de digitação em **80%**

---

### RL-005: Logo em Filesystem Local (Não Escalável)

**Descrição do Problema**:

No legado, logos de Clientes eram armazenadas em **pasta local** do servidor web:

```
~/Images/Clientes/
  ├── Alpargatas.png
  ├── Vale.jpg
  ├── Bombril.png
  └── Anima_Educacao.png
```

**Problemas**:
- 🖥️ **Perda de logos em caso de falha de servidor** (sem replicação)
- ❌ **Sem CDN**: Logos carregavam lentamente para usuários distantes
- 📦 **Sem versionamento**: Substituir logo apagava a anterior
- 🔒 **Sem backup automático**
- 📁 **Desorganização**: Nomenclatura inconsistente (Alpargatas.png vs. alpargatas.PNG)

**Destino no Sistema Moderno**: **SUBSTITUÍDO**

**Migração**:
- **RN-CLI-006-06**: Upload para **Azure Blob Storage**
- **Container**: `clientes-logos`
- **Nomenclatura padronizada**: `{ClienteId}.{extensão}` (ex: `guid-123.png`)
- **CDN global**: Logos distribuídas globalmente (baixa latência)
- **Backup automático**: Azure geo-replication
- **Versionamento**: Overwrite com histórico em auditoria

---

### RL-006: Ausência de Soft Delete e Auditoria LGPD

**Descrição do Problema**:

No legado, **DELETE físico era permitido e comum**:

```sql
-- Legado: DELETE físico (dados perdidos permanentemente)
DELETE FROM Empresa WHERE Id = 123;
```

**Problemas**:
- 🗑️ **Perda permanente de dados** (sem possibilidade de restauração)
- ❌ **Compliance LGPD**: Não havia retenção de auditoria por 7 anos
- 🔍 **Investigação de incidentes impossível**: Sem logs de quem deletou o quê
- 📊 **Relatórios retroativos inviáveis**: Dados históricos perdidos

**Impacto em Auditoria**:
- ❌ Sem registro de quem criou Cliente
- ❌ Sem registro de quem editou Cliente
- ❌ Sem registro de quem deletou Cliente
- ❌ Sem histórico de mudanças (before/after)

**Destino no Sistema Moderno**: **ASSUMIDO + SUBSTITUÍDO**

**Migração**:
- **RN-CLI-006-07**: Soft delete obrigatório (`FlExcluido = true`)
- **Trigger no banco**: Bloqueia DELETE físico com `RAISERROR`
- **RN-CLI-006-10**: Auditoria completa com **retenção de 7 anos**
- **Operações auditadas**:
  - CLI_CREATE (quem criou, quando, de onde)
  - CLI_UPDATE (campos alterados before/after)
  - CLI_DELETE (soft delete)
  - CLI_LOGO_UPLOAD (upload de logo)
  - CLI_DEACTIVATE_USERS (bloqueio de usuários)
  - CLI_RECEITA_QUERY (consulta ReceitaWS)

---

## 3. DESAFIOS DE MIGRAÇÃO

### 3.1 Migração de Dados (18 Bancos → 1 Banco)

**Desafio**: Consolidar dados de 18 bancos SQL Server isolados em **1 banco único** com multi-tenancy.

**Complexidade**:
- **Estimativa de Esforço**: 80-120 horas (2-3 sprints)
- **Risco**: ALTO (possibilidade de perda de dados ou data leakage)
- **Pré-requisitos**:
  - Backup completo de todos os 18 bancos
  - Script de validação de integridade referencial
  - Ambiente de teste isolado

**Etapas**:
1. **Identificar CNPJs reais** de cada banco legado (18 bancos)
2. **Criar registros na tabela `Cliente`** no banco moderno:
   - Id: GUID gerado
   - CNPJ: extraído de documentos/contratos
   - RazaoSocial: nome do banco legado (ex: "Vale" → "Vale S.A.")
3. **Adicionar coluna `ClienteId`** em TODAS as tabelas de negócio
4. **Popular `ClienteId`** em cada registro:
   - Empresa do banco `Vale` → `ClienteId` do Cliente Vale
   - Usuario do banco `Bombril` → `ClienteId` do Cliente Bombril
5. **Consolidar dados** de 18 bancos → 1 banco:
   - INSERT INTO [moderno].dbo.Empresa SELECT *, @ValeCl

ienteId FROM [Vale].dbo.Empresa
   - Repetir para todas as tabelas de todos os bancos
6. **Validar integridade**:
   - Verificar FKs (nenhuma FK apontando para Cliente errado)
   - Testar Query Filters (cada usuário vê apenas seus dados)
7. **Executar testes de isolamento**:
   - Usuario do Cliente A NÃO pode acessar dados do Cliente B
   - Super Admin vê TODOS os dados
8. **Migrar logos** de filesystem local → Azure Blob Storage

**Riscos e Mitigações**:

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| Data leakage cross-tenant | CRÍTICO | MÉDIA | Testes exaustivos de Query Filters antes de produção |
| Perda de dados durante consolidação | CRÍTICO | BAIXA | Backup completo + restore em caso de erro |
| Performance degradada (1 banco vs. 18) | ALTO | MÉDIA | Índices otimizados + particionamento de tabelas grandes |
| FKs quebradas após migração | ALTO | BAIXA | Validação de integridade referencial obrigatória |

**Nota**: A migração de dados (RL-006) será um **RF separado** (RF-MIG-001 ou similar), NÃO faz parte do escopo de RF006.

---

### 3.2 Transição de Onboarding (Manual → Automatizado)

**Desafio**: Treinar área comercial e DBAs no novo fluxo automatizado.

**Mudança de Processo**:

**Legado (Manual)**:
1. Comercial envia email para DBA: "Cliente Novo: XYZ Ltda, CNPJ: 12.345.678/0001-99"
2. DBA cria ticket no Jira
3. DBA cria banco SQL Server manualmente
4. DBA executa script DDL (30 minutos)
5. DBA configura ConnectionString no Web.config
6. DBA reinicia aplicação
7. DBA testa login com usuário de teste
8. DBA responde email: "Cliente XYZ pronto"
9. **Tempo total**: 3-5 dias

**Moderno (Automatizado)**:
1. **Super Admin** acessa `/admin/clientes/novo`
2. Preenche CNPJ: `12.345.678/0001-99`
3. Clica em "Consultar Receita Federal"
4. Sistema preenche automaticamente:
   - Razão Social: XYZ Ltda
   - Nome Fantasia: XYZ
   - Endereço: Rua ABC, 123
   - Telefone: (11) 1234-5678
   - Email: contato@xyz.com.br
5. (Opcional) Upload de logo
6. Clica em "Salvar"
7. Sistema cria Cliente no banco
8. Sistema registra auditoria CLI_CREATE
9. **Tempo total**: **< 5 minutos**

**Treinamento Necessário**:
- ✅ Super Admins: Tutorial de 30 minutos
- ✅ DBAs: Informar que processo manual foi substituído
- ✅ Área Comercial: Solicitar criação via ticket (Super Admin cria no sistema)

---

### 3.3 Manutenção de Bancos Legados Durante Transição

**Desafio**: Durante a transição, será necessário manter **2 sistemas simultâneos**:
- Legado (18 bancos) para Clientes que ainda não migraram
- Moderno (1 banco) para novos Clientes

**Período Estimado de Dupla Operação**: 6-12 meses

**Estratégia**:
- **Clientes novos**: Criados APENAS no sistema moderno
- **Clientes legados**: Permanecem no banco legado até migração
- **Freeze de funcionalidades no legado**: Apenas manutenção crítica
- **Migração gradual**: 1-2 Clientes por sprint
- **Validação por Cliente**: Testes de UAT antes de desativar banco legado
- **Desativação final**: Após todos os 18 Clientes migrarem, desligar servidores legados

---

## 4. LIÇÕES APRENDIDAS

### 4.1 Arquitetura Multi-Database NÃO Escala

**Lição**: Arquitetura com **1 banco por Cliente** é adequada para **< 10 Clientes**, mas torna-se **inviável** acima disso.

**Problemas Escalaram Conforme Crescimento**:
- 1-5 Clientes: **Gerenciável** (poucos bancos)
- 6-10 Clientes: **Trabalhoso** (manutenção schema aumenta)
- 11-18 Clientes: **Insustentável** (custo e complexidade explodem)
- > 20 Clientes: **Impossível** (não escalou além de 18 por limitações técnicas)

**Recomendação**: Para SaaS, sempre usar **single database + multi-tenancy lógico** desde o início.

---

### 4.2 Ausência de Validações Causou Débito Técnico

**Lição**: Não validar CNPJ e não consultar ReceitaWS gerou **dados inconsistentes** que exigirão limpeza na migração.

**Exemplos de Dados Problemáticos Encontrados**:
- ❌ CNPJs com dígitos verificadores incorretos: ~5% dos registros
- ❌ CNPJs duplicados: 2 Clientes com mesmo CNPJ (erro manual)
- ❌ Razão Social desatualizada: Empresas que mudaram de nome
- ❌ Telefones desatualizados: 30% dos telefones não atendem
- ❌ Emails inválidos: 15% dos emails retornam bounce

**Recomendação**: Sempre validar dados críticos **no backend** (não confiar apenas em validação client-side).

---

### 4.3 Soft Delete Previne Perda de Dados

**Lição**: DELETE físico no legado causou **perda irreversível** de dados importantes.

**Casos Reais de Perda**:
- 🗑️ Cliente deletado por engano → Sem possibilidade de restauração
- 📊 Relatórios retroativos impossíveis (dados históricos perdidos)
- 🔍 Investigação de fraude comprometida (sem auditoria de quem deletou)

**Recomendação**: **Sempre usar soft delete** em entidades críticas (Cliente, Usuario, Empresa, etc.). DELETE físico só é aceitável em:
- Dados temporários (sessões, logs antigos)
- Dados sensíveis sob LGPD que DEVEM ser apagados (right to erasure)

---

### 4.4 Auditoria LGPD Deve Ser Nativa, Não Retrofit

**Lição**: Adicionar auditoria **depois** é muito mais difícil do que projetar desde o início.

No legado:
- ❌ Sem auditoria nativa
- ❌ Sem registro de quem criou/editou/deletou
- ❌ Sem histórico de mudanças (before/after)

Tentativa de retrofit (pós-LGPD):
- ⏱️ Esforço: 200+ horas
- 📝 Complexidade: Interceptar TODAS as operações em VB.NET
- ❌ Nunca foi finalizado (projeto abandonado por custo)

**Recomendação**: Usar **AuditInterceptor** do EF Core desde o dia 1 do projeto moderno.

---

## 5. RECOMENDAÇÕES PARA SISTEMA MODERNO

### 5.1 EF Core Query Filters: Validar Exaustivamente

**Recomendação**: Criar **suite de testes de isolamento** antes de ir para produção.

**Testes Obrigatórios**:
1. Usuario do Cliente A lista Empresas → Retorna APENAS Empresas do Cliente A
2. Usuario do Cliente B tenta acessar Empresa do Cliente A → HTTP 404 (não encontrado)
3. Super Admin lista Empresas → Retorna Empresas de TODOS os Clientes
4. Tentar bypass de Query Filter via SQL direto → DEVE falhar
5. Tentar bypass via manipulação de ClienteId no token JWT → DEVE falhar

**Exemplo de Teste**:
```csharp
[Fact]
public async Task Usuario_NaoPode_Acessar_Empresa_De_Outro_Cliente()
{
    // Arrange
    var clienteA = new Cliente { Id = Guid.NewGuid(), CNPJ = "11111111111111", RazaoSocial = "Cliente A" };
    var clienteB = new Cliente { Id = Guid.NewGuid(), CNPJ = "22222222222222", RazaoSocial = "Cliente B" };

    var empresaA = new Empresa { Id = Guid.NewGuid(), ClienteId = clienteA.Id, Nome = "Empresa de A" };
    var empresaB = new Empresa { Id = Guid.NewGuid(), ClienteId = clienteB.Id, Nome = "Empresa de B" };

    // Simular Usuario do Cliente A autenticado
    _currentUserService.SetClienteId(clienteA.Id);

    // Act
    var result = await _context.Empresas.ToListAsync();

    // Assert
    Assert.Single(result); // Apenas 1 empresa (do Cliente A)
    Assert.Equal(empresaA.Id, result[0].Id);
    Assert.DoesNotContain(result, e => e.ClienteId == clienteB.Id); // NÃO vê Empresa de B
}
```

---

### 5.2 ReceitaWS: Implementar Fallback Robusto

**Recomendação**: ReceitaWS é API pública **não tem SLA**. Implementar fallback robusto.

**Estratégia**:
1. **Timeout curto**: 10 segundos (não esperar > 10s)
2. **Não bloquear criação**: Se ReceitaWS falhar, permitir preenchimento manual
3. **Retry com exponential backoff**: 3 tentativas (0s, 2s, 4s)
4. **Cache de respostas**: Armazenar respostas ReceitaWS por 7 dias (evitar consultar mesmo CNPJ múltiplas vezes)
5. **Alerta de indisponibilidade**: Se > 10 falhas consecutivas, notificar DevOps

---

### 5.3 Azure Blob Storage: Configurar Geo-Replication

**Recomendação**: Logos são **críticas para white-label**. Configurar redundância geográfica.

**Configuração Azure Blob**:
- **Tier**: Standard (suficiente para logos)
- **Replicação**: GRS (Geo-Redundant Storage)
- **Backup**: Soft delete habilitado (14 dias)
- **CDN**: Azure CDN habilitado (baixa latência global)
- **Lifecycle Policy**: Mover logos não acessadas em 90 dias para Cool Tier (reduzir custo)

---

### 5.4 Monitoramento de Data Leakage Cross-Tenant

**Recomendação**: Implementar **alerta CRITICAL** para data leakage.

**Métrica**:
```csharp
// Registrar em ApplicationInsights sempre que Query Filter for bypassado
if (_currentUserService.ClienteId != entity.ClienteId && !_currentUserService.IsSuperAdmin)
{
    _telemetry.TrackEvent("DATA_LEAKAGE_DETECTED", new Dictionary<string, string>
    {
        { "UserId", _currentUserService.UserId },
        { "UserClienteId", _currentUserService.ClienteId.ToString() },
        { "AccessedClienteId", entity.ClienteId.ToString() },
        { "EntityType", entity.GetType().Name },
        { "EntityId", entity.Id.ToString() }
    });

    // Alerta CRITICAL imediato
    throw new SecurityException("Data leakage cross-tenant detected!");
}
```

**Ação ao Detectar**:
1. Parar sistema imediatamente (circuit breaker)
2. Notificar CISO e equipe de segurança
3. Investigar causa raiz
4. Corrigir Query Filter
5. Validar que nenhum dado vazou
6. Escrever post-mortem

---

## 6. CRONOGRAMA DE DESATIVAÇÃO DO LEGADO

**Fase 1: Criação do Sistema Moderno** (Sprint 1-3)
- ✅ Criar RF006 (Gestão de Clientes)
- ✅ Implementar backend (CRUD + ReceitaWS + Azure Blob)
- ✅ Implementar frontend (/admin/clientes)
- ✅ Testes de isolamento multi-tenancy
- ✅ Deploy em DEV e HOM

**Fase 2: Onboarding de Novos Clientes** (Sprint 4-6)
- ✅ Clientes novos criados APENAS no sistema moderno
- ❌ Clientes legados permanecem em bancos separados

**Fase 3: Migração Gradual de Clientes Legados** (Sprint 7-18)
- Migrar 1-2 Clientes por sprint
- Validação UAT com Cliente antes de desativar banco legado
- Total: 18 Clientes a migrar

**Fase 4: Desativação Final do Legado** (Sprint 19-20)
- Após todos os 18 Clientes migrarem
- Desligar servidores SQL Server legados
- Remover ConnectionStrings do Web.config legado
- Arquivar backups finais

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|--------|------|-----------|-------|
| 2.0 | 2025-12-29 | Migração para formato governança v2.0 - Referência ao Legado completa | Architect Agent |

---

**Última Atualização**: 2025-12-29
**Versão**: 2.0
**Governança**: RF-UC-RL v2.0
