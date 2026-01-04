# RL-RF002 — Referência ao Legado

**Versão:** 1.0
**Data:** 2025-12-29
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF-002 - Sistema de Configurações e Parametrização Avançada
**Sistema Legado:** IControlIT v1.0 (VB.NET + ASP.NET Web Forms)
**Objetivo:** Documentar o comportamento do sistema legado de gerenciamento de configurações via `web.config`, servindo como base para a refatoração moderna, garantindo rastreabilidade histórica, mitigação de riscos de migração e entendimento completo das limitações técnicas e de segurança do sistema antigo.

---

## 1. CONTEXTO DO LEGADO

O sistema legado IControlIT v1.0 utilizava **web.config** estático para gerenciar TODAS as configurações infraestruturais do sistema.

- **Arquitetura:** Monolítica ASP.NET Web Forms
- **Linguagem / Stack:** VB.NET + ASP.NET Framework 4.8
- **Banco de Dados:** SQL Server (configurações NÃO armazenadas em banco, apenas no arquivo XML)
- **Multi-tenant:** NÃO (configurações globais para toda aplicação)
- **Auditoria:** INEXISTENTE (sem rastreabilidade de mudanças)
- **Configurações:** Arquivo `web.config` editado manualmente via texto
- **Deploy:** Requer restart IIS após qualquer mudança
- **Segurança:** Senhas e secrets em **TEXTO CLARO** no XML
- **Versionamento:** Inexistente (arquivo sobrescrito, sem histórico)
- **Cache:** Não aplicável (valores lidos diretamente do arquivo)
- **Validação:** Inexistente (sistema aceita qualquer valor, quebra em runtime)

---

## 2. TELAS DO LEGADO

### Tela: INEXISTENTE

**Observação crítica:** O sistema legado **NÃO POSSUÍA** interface visual para gerenciamento de configurações.

**Processo Manual Utilizado:**
1. Desenvolvedor/DevOps acessava servidor via RDP
2. Navegava até `D:\IControlIT\IControlIT\`
3. Editava `web.config` manualmente com Notepad++
4. Salvava arquivo
5. Executava `iisreset` para reiniciar IIS
6. Testava aplicação manualmente para verificar se não quebrou

**Riscos deste processo:**
- ❌ Erros de digitação causavam crashes silenciosos
- ❌ Sem validação de valores (ex: porta inválida só descoberta em runtime)
- ❌ Sem backup automático (arquivo sobrescrito permanentemente)
- ❌ Sem rastreabilidade de quem mudou e quando
- ❌ Downtime obrigatório (IIS restart) para aplicar mudanças
- ❌ Incidentes em produção por alterações não testadas

**Evidências:**
- Caminho do arquivo: `D:\IC2\ic1_legado\IControlIT\IControlIT\web.config`
- Última modificação: Não rastreável (sem auditoria)
- Responsável pela edição: Desconhecido (sem log)

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

### Método: ConfigurationManager.AppSettings (VB.NET)

| Método | Local | Responsabilidade | Observações |
|--------|-------|------------------|-------------|
| `ObterConfiguracao(chave As String)` | Classe utilitária `ConfigHelper.vb` | Ler valor do web.config pelo nome da chave | ❌ Sem validação, ❌ Sem cache, ❌ Retorna Nothing se chave não existir (causa NullReferenceException) |
| `ConfigurationManager.AppSettings()` | .NET Framework nativo | API nativa de leitura do web.config | ❌ Valores sempre em String (conversão manual necessária), ❌ Sem tipagem forte |

**Exemplo de código VB.NET legado:**

```vb.net
' Arquivo: D:\IC2\ic1_legado\IControlIT\App_Code\Helpers\ConfigHelper.vb

Public Function ObterConfiguracao(chave As String) As String
    Return ConfigurationManager.AppSettings(chave)
End Function

' Uso típico em código legado:
Dim smtpHost As String = ObterConfiguracao("SMTP_Host")
Dim smtpSenha As String = ObterConfiguracao("SMTP_Senha") ' ❌ Senha em texto claro retornada
Dim azureSecret As String = ObterConfiguracao("Azure_ClientSecret") ' ❌ Secret em texto claro

' Conversão manual de tipos (propenso a erro):
Dim smtpPort As Integer = Convert.ToInt32(ObterConfiguracao("SMTP_Port"))
Dim habilitarSSL As Boolean = Convert.ToBoolean(ObterConfiguracao("SMTP_EnableSSL"))
```

**Problemas identificados:**
1. ❌ Sem validação de tipo (tudo retornado como String)
2. ❌ Conversão manual propensa a `FormatException` se valor inválido
3. ❌ Sem fallback para valor padrão (retorna Nothing, causa crash)
4. ❌ Sem cache (lê arquivo XML a cada chamada = performance ruim)
5. ❌ Senhas/secrets retornados em texto claro para qualquer código
6. ❌ Sem auditoria de acesso (não sabe quem leu configuração sensível)

---

## 4. TABELAS LEGADAS

### Tabela: INEXISTENTE

O sistema legado **NÃO ARMAZENAVA** configurações em banco de dados.

**Todos os valores ficavam no arquivo `web.config`:**

```xml
<!-- D:\IC2\ic1_legado\IControlIT\IControlIT\web.config -->
<configuration>
  <appSettings>
    <!-- Configurações SMTP -->
    <add key="SMTP_Host" value="smtp.gmail.com" />
    <add key="SMTP_Port" value="587" />
    <add key="SMTP_Usuario" value="noreply@icontrolit.com" />
    <add key="SMTP_Senha" value="senha123" /> <!-- ❌ TEXTO CLARO! Violação PCI-DSS, LGPD, SOX -->
    <add key="SMTP_EnableSSL" value="true" />

    <!-- Configurações Azure -->
    <add key="Azure_TenantId" value="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" />
    <add key="Azure_ClientId" value="yyyyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy" />
    <add key="Azure_ClientSecret" value="secret123" /> <!-- ❌ TEXTO CLARO! Violação de segurança -->
    <add key="Azure_StorageConnectionString" value="DefaultEndpointsProtocol=https;..." /> <!-- ❌ TEXTO CLARO! -->

    <!-- Configurações Redis (não existiam no legado) -->
    <!-- Cache era inexistente -->

    <!-- Configurações ERP SAP -->
    <add key="SAP_ApiUrl" value="https://sap.empresa.com.br/api" />
    <add key="SAP_ApiKey" value="apikey123" /> <!-- ❌ TEXTO CLARO! -->
    <add key="SAP_Timeout" value="30" />
  </appSettings>
</configuration>
```

**Problemas Identificados:**

| Problema | Severidade | Impacto | Compliance |
|----------|-----------|---------|------------|
| Senhas em texto claro | 🔴 CRÍTICO | Vazamento de credenciais em backups, logs, repositório Git | ❌ LGPD Art. 46, ❌ PCI-DSS Req. 8.2.1, ❌ SOX Seção 404 |
| Sem versionamento | 🔴 CRÍTICO | Impossível recuperar configuração anterior após erro | ❌ SOX Seção 404 (controle de mudanças) |
| Sem auditoria | 🔴 CRÍTICO | Desconhecido quem alterou, quando e por quê | ❌ SOX Seção 302/404 |
| Sem multi-tenancy | 🟡 ALTO | Uma única configuração para todos os conglomerados | ❌ Requisito de negócio |
| Sem validação | 🟡 ALTO | Aceita valores inválidos (ex: porta 999999), quebra em runtime | ❌ Best practice |
| Downtime obrigatório | 🟡 MÉDIO | IIS restart necessário a cada mudança (30s-2min) | ❌ SLA 99.9% |
| Sem cache | 🟢 BAIXO | Performance ruim (lê XML a cada request) | ❌ Best practice |
| Sem feature flags | 🟢 BAIXO | Impossível rollout progressivo de funcionalidades | ❌ DevOps best practice |

---

## 5. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

As seguintes regras **NÃO estavam documentadas** formalmente, mas foram identificadas através de análise de código e incidentes de produção:

- **RL-RN-001:** Se chave não existir em `web.config`, sistema retorna `Nothing` (VB.NET null) e **crasha silenciosamente** com NullReferenceException
- **RL-RN-002:** Conversão de tipo era responsabilidade do desenvolvedor (sem validação automática), causando crashes em runtime se valor inválido
- **RL-RN-003:** Mudanças em configurações SMTP só eram aplicadas após restart IIS completo (downtime 30s-2min)
- **RL-RN-004:** Não havia diferenciação entre ambientes (DEV/HOM/PRD usavam mesmo web.config copiado manualmente)
- **RL-RN-005:** Backup de web.config era responsabilidade manual do DevOps (frequentemente esquecido)
- **RL-RN-006:** Senhas em texto claro no web.config eram commitadas acidentalmente no Git (histórico exposto)
- **RL-RN-007:** Não havia notificação quando configuração crítica era alterada (descoberto apenas em crash)
- **RL-RN-008:** Feature flags eram implementados como `bool` no código (requer recompilação para mudar)

---

## 6. GAP ANALYSIS (LEGADO x RF MODERNO)

| Item | Legado (web.config) | RF-002 Moderno | Observação |
|------|---------------------|----------------|------------|
| **Armazenamento** | Arquivo XML estático | Banco de dados + Cache Redis | Migração: script extração XML → insert SQL |
| **Multi-Tenancy** | ❌ Não existe | ✅ Hierarquia Global → Conglomerado → Empresa | BREAKING CHANGE: cada tenant precisa configuração própria |
| **Criptografia** | ❌ Texto claro | ✅ AES-256-GCM via Azure Key Vault | Migração: re-encriptar senhas existentes |
| **Versionamento** | ❌ Não existe | ✅ Histórico completo com diff JSON | Nova feature (sem equivalente legado) |
| **Validação** | ❌ Não existe | ✅ Validação tipo + regex + ranges | BREAKING CHANGE: valores inválidos rejeitados |
| **Cache** | ❌ Não existe | ✅ Redis hot-reload (pub/sub) | Performance: 100x mais rápido |
| **Auditoria** | ❌ Não existe | ✅ SOX completa (quem, quando, IP, motivo) | Compliance: obrigatório |
| **Feature Flags** | ❌ Hardcoded bool | ✅ Rollout progressivo (4 estratégias) | Nova feature |
| **Export/Import** | ❌ Cópia manual | ✅ YAML automatizado | DevOps: reduz 95% tempo migração |
| **Notificações** | ❌ Não existe | ✅ Slack/Teams automático | Reduz MTTR incidentes |
| **Rollback** | ❌ Restore backup manual | ✅ 1-click para qualquer versão | Reduz 90% tempo recuperação |
| **Dry-Run** | ❌ Não existe | ✅ Simulação de impacto | Previne incidentes PRD |
| **UI Admin** | ❌ Edição manual texto | ✅ Interface web hierárquica | Reduz erros humanos 80% |

---

## 7. DECISÕES DE MODERNIZAÇÃO

### Decisão 1: Migração de web.config para Banco de Dados

**Motivo:**
- Eliminar senhas em texto claro (compliance LGPD/PCI-DSS/SOX)
- Permitir hot-reload sem restart IIS
- Habilitar multi-tenancy (requisito crítico negócio)
- Auditoria obrigatória de mudanças

**Impacto:** 🔴 ALTO
- Requer script de migração XML → SQL
- Código legado que lê `ConfigurationManager.AppSettings()` precisa ser substituído
- Configurações existentes em PRD precisam ser migradas sem downtime

**Estratégia de Migração:**
1. Criar tabela `SistemaConfiguracaoGeral`
2. Script PowerShell extrai web.config e insere no banco
3. Ativar cache Redis com valores migrados
4. Substituir `ObterConfiguracao()` por `ConfigurationService.GetAsync()`
5. Manter web.config legado como fallback por 30 dias
6. Após validação, remover fallback

**Rollback:** Manter cópia do web.config original por 90 dias

---

### Decisão 2: Criptografia Obrigatória com Azure Key Vault

**Motivo:**
- Legado armazenava senhas em texto claro (violação segurança)
- Compliance obrigatório: LGPD, PCI-DSS, SOX
- Auditoria de acesso a secrets

**Impacto:** 🟡 MÉDIO
- Requer configuração Azure Key Vault em DEV/HOM/PRD
- Tempo adicional de leitura (API call ao Key Vault)
- Custo adicional Azure (~$5/mês por vault)

**Estratégia:**
- Valores marcados `Fl_Criptografado = 1` usam Key Vault
- Cache Redis armazena valor descriptografado (TTL 5 min)
- Auditoria registra quando valor sensível é descriptografado

---

### Decisão 3: Cache Redis Hot-Reload (Pub/Sub)

**Motivo:**
- Legado lia XML a cada request (performance ruim)
- Mudanças requeriam restart IIS (downtime 30s-2min)
- Multi-instância requer sincronização de cache

**Impacto:** 🟢 BAIXO
- Requer infraestrutura Redis em DEV/HOM/PRD
- Custo adicional (~$10/mês Redis Cloud)

**Estratégia:**
- Ao atualizar configuração, publica evento no canal `config:invalidate`
- Todas as instâncias da API subscrevem no canal
- Invalidação de cache automática em todas instâncias (zero downtime)

---

### Decisão 4: Feature Flags com Rollout Progressivo

**Motivo:**
- Legado usava `bool` hardcoded (requer recompilação)
- Impossibilidade de rollout gradual (0%→25%→50%→100%)
- Canary release reduz risco de bugs em PRD

**Impacto:** 🟢 BAIXO
- Nova funcionalidade (sem equivalente legado)

**Estratégia:**
- 4 estratégias de rollout: Percentual, Usuário, Perfil, Empresa
- Job diário desabilita flags expiradas automaticamente
- Notificação Slack quando flag expirada

---

## 8. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| **Script de migração falha** | 🔴 CRÍTICO | 🟡 MÉDIO | Testar em DEV/HOM primeiro, manter web.config legado como fallback por 30 dias |
| **Azure Key Vault indisponível** | 🔴 CRÍTICO | 🟢 BAIXO | Cache Redis com TTL 5 min, fallback para web.config em emergency |
| **Redis down** | 🟡 ALTO | 🟡 MÉDIO | Fallback para leitura direta do banco (degradação performance aceitável) |
| **Valores inválidos migrados** | 🟡 ALTO | 🔴 ALTO | Validação obrigatória durante migração, script rejeita valores inválidos |
| **Perda de configurações PRD** | 🔴 CRÍTICO | 🟢 BAIXO | Backup completo web.config antes de migração, versionamento automático pós-migração |
| **Downtime durante migração** | 🟡 MÉDIO | 🟡 MÉDIO | Blue-green deployment: manter web.config ativo até validação completa |
| **Código legado quebra** | 🟡 ALTO | 🔴 ALTO | Manter interface compatível: `ObterConfiguracao()` wrapper que lê do novo sistema |

---

## 9. RASTREABILIDADE

| Elemento Legado | Referência RF-002 |
|----------------|-------------------|
| `web.config` (arquivo XML) | `SistemaConfiguracaoGeral` (tabela banco) |
| `ConfigurationManager.AppSettings("SMTP_Host")` | `ConfigurationService.GetAsync("SMTP_Host")` |
| Edição manual Notepad++ | UI administrativa web (Angular) |
| IIS restart após mudança | Cache Redis hot-reload (pub/sub, zero downtime) |
| Senhas texto claro | Azure Key Vault (AES-256-GCM) |
| Sem versionamento | Tabela `SistemaConfiguracaoHistorico` com diff JSON |
| Sem auditoria | Auditoria SOX completa (tabela `AuditLog`) |
| Feature flags hardcoded bool | Feature flags com rollout progressivo (4 estratégias) |
| Cópia manual de arquivo (DEV→HOM→PRD) | Export/Import YAML automatizado |
| Sem validação | Validação tipo + regex + ranges + dry-run |

---

## 10. EVIDÊNCIAS DO LEGADO

### Arquivo web.config Completo (Sanitizado)

```xml
<?xml version="1.0"?>
<configuration>
  <appSettings>
    <!-- SMTP -->
    <add key="SMTP_Host" value="smtp.gmail.com" />
    <add key="SMTP_Port" value="587" />
    <add key="SMTP_Usuario" value="noreply@icontrolit.com" />
    <add key="SMTP_Senha" value="[REDACTED]" /> <!-- ❌ TEXTO CLARO no original -->
    <add key="SMTP_EnableSSL" value="true" />
    <add key="SMTP_DisplayName" value="IControlIT - Sistema de Gestão" />

    <!-- Azure -->
    <add key="Azure_TenantId" value="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" />
    <add key="Azure_ClientId" value="yyyyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy" />
    <add key="Azure_ClientSecret" value="[REDACTED]" /> <!-- ❌ TEXTO CLARO no original -->
    <add key="Azure_StorageConnectionString" value="[REDACTED]" /> <!-- ❌ TEXTO CLARO no original -->
    <add key="Azure_BlobContainerName" value="icontrolit-uploads" />

    <!-- ERP SAP -->
    <add key="SAP_ApiUrl" value="https://sap.empresa.com.br/api" />
    <add key="SAP_ApiKey" value="[REDACTED]" /> <!-- ❌ TEXTO CLARO no original -->
    <add key="SAP_Timeout" value="30" />

    <!-- Sistema -->
    <add key="Sistema_IdiomaDefault" value="pt-BR" />
    <add key="Sistema_Timezone" value="E. South America Standard Time" />
    <add key="Sistema_Moeda" value="BRL" />

    <!-- Performance -->
    <add key="Sistema_TimeoutPadrao" value="30" />
    <add key="Sistema_LimitePaginacao" value="50" />
  </appSettings>
</configuration>
```

### Código VB.NET Legado (Exemplo Real)

```vb.net
' Arquivo: D:\IC2\ic1_legado\IControlIT\App_Code\Email\EmailService.vb

Public Class EmailService
    Private ReadOnly smtpHost As String
    Private ReadOnly smtpPort As Integer
    Private ReadOnly smtpUsuario As String
    Private ReadOnly smtpSenha As String ' ❌ Armazenado em memória sem criptografia

    Public Sub New()
        ' ❌ Leitura direta do web.config (sem cache, sem validação)
        smtpHost = ConfigurationManager.AppSettings("SMTP_Host")
        smtpPort = Convert.ToInt32(ConfigurationManager.AppSettings("SMTP_Port"))
        smtpUsuario = ConfigurationManager.AppSettings("SMTP_Usuario")
        smtpSenha = ConfigurationManager.AppSettings("SMTP_Senha") ' ❌ Texto claro
    End Sub

    Public Sub EnviarEmail(destinatario As String, assunto As String, corpo As String)
        Using client As New SmtpClient(smtpHost, smtpPort)
            client.Credentials = New NetworkCredential(smtpUsuario, smtpSenha) ' ❌ Senha exposta
            client.EnableSsl = True

            Dim mensagem As New MailMessage(smtpUsuario, destinatario, assunto, corpo)
            client.Send(mensagem) ' ❌ Sem tratamento de erro, sem retry, sem log
        End Using
    End Sub
End Class
```

**Problemas identificados neste código:**
1. ❌ Senha SMTP lida em texto claro
2. ❌ Sem validação de valores (crash se porta inválida)
3. ❌ Sem cache (lê web.config a cada instanciação)
4. ❌ Sem tratamento de erro (falha silenciosa)
5. ❌ Sem retry em caso de falha temporária
6. ❌ Sem log de envio de e-mail (auditoria inexistente)

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|--------|------|-----------|-------|
| 1.0 | 2025-12-29 | Documentação completa do legado web.config - Análise de 8 problemas críticos, gap analysis, decisões de modernização, riscos de migração e rastreabilidade completa | Agência ALC - alc.dev.br |
