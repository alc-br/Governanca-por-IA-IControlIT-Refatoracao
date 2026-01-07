# RL-RF005: Referência ao Legado — Internacionalização

**RF Relacionado:** RF-005 — Internacionalização (i18n) e Localização
**Versão:** 2.0
**Data:** 2025-12-29
**Autor:** Agência ALC - alc.dev.br

---

## 1. OBJETIVO DESTE DOCUMENTO

Este documento registra **referências ao sistema legado VB.NET/ASP.NET Web Forms** relacionadas à internacionalização (ou ausência dela). Serve como **memória técnica histórica** para contexto de migração.

**IMPORTANTE**: Este documento NÃO define comportamento moderno. O contrato funcional está em **RF005.md**.

---

## 2. PROBLEMAS IDENTIFICADOS NO LEGADO

### ❌ PROBLEMA 1: Textos Hardcoded em Português

**Descrição**: Textos em português diretamente no código VB.NET e markup ASPX.

**Exemplo - VB.NET**:
```vb.net
' Código legado (VB.NET)
lblMensagem.Text = "Bem-vindo ao sistema"
btnSalvar.Text = "Salvar"
btnCancelar.Text = "Cancelar"
lblTitulo.Text = "Gestão de Ativos de TI"

' Mensagens de validação hardcoded
If String.IsNullOrEmpty(txtNome.Text) Then
    MsgBox("Campo Nome é obrigatório")
End If
```

**Exemplo - ASPX**:
```aspx
<asp:Label ID="lblTitulo" runat="server" Text="Cadastro de Usuários"></asp:Label>
<asp:Button ID="btnSalvar" runat="server" Text="Salvar" />
<asp:Button ID="btnCancelar" runat="server" Text="Cancelar" />
```

**Impacto**: Impossível internacionalizar sem reescrever código.

**Destino**: **SUBSTITUÍDO** - Sistema moderno usa chaves i18n (`common.buttons.save`).

---

### ❌ PROBLEMA 2: Formatação de Datas/Moedas Fixa em pt-BR

**Descrição**: Formatação hardcoded sem suporte a diferentes culturas.

**Exemplo**:
```vb.net
' Data sempre dd/MM/yyyy
lblData.Text = DateTime.Now.ToString("dd/MM/yyyy")

' Moeda sempre R$
lblValor.Text = String.Format("R$ {0:N2}", valor)

' Número sempre vírgula decimal
lblQuantidade.Text = quantidade.ToString("N2")  ' 1.234,56
```

**Impacto**: Usuários internacionais veem formato brasileiro.

**Destino**: **SUBSTITUÍDO** - Sistema moderno usa `CultureInfo` dinâmico.

---

### ❌ PROBLEMA 3: Emails Apenas em Português

**Descrição**: Templates de email hardcoded em português.

**Exemplo**:
```vb.net
' Email de boas-vindas
Dim corpo As String = "<h1>Bem-vindo ao IControlIT</h1>" & _
                      "<p>Seu cadastro foi realizado com sucesso.</p>" & _
                      "<p>Clique no link abaixo para ativar sua conta:</p>"

EnviarEmail(usuario.Email, "Bem-vindo ao IControlIT", corpo)
```

**Impacto**: Usuários internacionais recebem emails em português.

**Destino**: **SUBSTITUÍDO** - Templates multi-idioma em backend moderno.

---

### ❌ PROBLEMA 4: Relatórios Não Traduzíveis

**Descrição**: Relatórios Crystal Reports com labels fixos em português.

**Exemplo - Crystal Reports**:
```
Relatório: "Relatório de Ativos"
Colunas: "Nome", "Tipo", "Valor", "Data de Aquisição"
Rodapé: "Total de Ativos: {count}"
```

**Impacto**: Relatórios sempre em português.

**Destino**: **SUBSTITUÍDO** - Relatórios modernos com suporte i18n.

---

### ❌ PROBLEMA 5: Nenhuma Biblioteca de Internacionalização

**Descrição**: Sistema legado não utiliza nenhuma biblioteca i18n (.NET Resources, Gettext, etc).

**Constatação**:
- NÃO usa arquivos `.resx`
- NÃO usa `ResourceManager`
- NÃO usa `CultureInfo` dinâmico
- NÃO tem estrutura de tradução

**Destino**: **DESCARTADO** - Implementação do zero no sistema moderno.

---

### ❌ PROBLEMA 6: Impossibilidade de Adicionar Idiomas

**Descrição**: Não há interface ou mecanismo para adicionar novos idiomas sem modificar código.

**Barreira Técnica**: Textos hardcoded em centenas de arquivos .aspx e .vb.

**Destino**: **DESCARTADO** - Sistema moderno tem gestão visual de idiomas.

---

## 3. COMPONENTES LEGADO COM TEXTOS HARDCODED

### 3.1. Telas ASPX Principais

| Tela | Caminho Legado | Textos Hardcoded | Status |
|------|----------------|------------------|--------|
| Login | `ic1_legado/IControlIT/Login.aspx` | "Entrar", "Usuário", "Senha" | Substituído |
| Dashboard | `ic1_legado/IControlIT/Dashboard.aspx` | "Painel de Controle", "Bem-vindo" | Substituído |
| Usuários | `ic1_legado/IControlIT/Usuarios/Default.aspx` | "Cadastro de Usuários", "Novo", "Editar" | Substituído |
| Ativos | `ic1_legado/IControlIT/Ativos/Default.aspx` | "Gestão de Ativos", Labels de colunas | Substituído |
| Relatórios | `ic1_legado/IControlIT/Relatorios/` | Todos os labels em português | Substituído |

**Total Estimado**: ~150 telas ASPX com textos hardcoded.

---

### 3.2. Master Pages com Menus Hardcoded

**Arquivo**: `ic1_legado/IControlIT/Site.Master`

**Exemplo**:
```aspx
<asp:Menu ID="menuPrincipal" runat="server">
    <Items>
        <asp:MenuItem Text="Início" NavigateUrl="~/Dashboard.aspx" />
        <asp:MenuItem Text="Cadastros" NavigateUrl="#" />
        <asp:MenuItem Text="Relatórios" NavigateUrl="#" />
        <asp:MenuItem Text="Configurações" NavigateUrl="#" />
    </Items>
</asp:Menu>
```

**Destino**: **SUBSTITUÍDO** - Menu moderno usa chaves i18n (`menu.home`, `menu.settings`).

---

### 3.3. Mensagens de Validação no Code-Behind

**Exemplo**:
```vb.net
' Validações em VB.NET
If txtNome.Text.Trim() = "" Then
    lblErro.Text = "Nome é obrigatório"
    Return
End If

If txtEmail.Text.IndexOf("@") = -1 Then
    lblErro.Text = "Email inválido"
    Return
End If

If txtCPF.Text.Length <> 11 Then
    lblErro.Text = "CPF deve ter 11 dígitos"
    Return
End If
```

**Destino**: **SUBSTITUÍDO** - Validações modernas usam `_localizer["validation.email.required"]`.

---

## 4. STORED PROCEDURES COM MENSAGENS HARDCODED

**Exemplo**:
```sql
CREATE PROCEDURE sp_InserirUsuario
    @Nome NVARCHAR(200),
    @Email NVARCHAR(200)
AS
BEGIN
    IF EXISTS (SELECT 1 FROM Usuarios WHERE Email = @Email)
    BEGIN
        RAISERROR('Email já cadastrado', 16, 1)  -- Mensagem em português
        RETURN
    END

    -- Insert...
END
```

**Destino**: **SUBSTITUÍDO** - Mensagens de erro vêm do backend moderno (i18n).

---

## 5. ESTRATÉGIA DE MIGRAÇÃO

### Decisão de Modernização

**NÃO MIGRAR** textos hardcoded do legado.
**CRIAR DO ZERO** estrutura moderna de i18n.

**Razões**:
1. Textos estão espalhados em ~150 arquivos ASPX e VB.NET
2. NÃO há padrão ou consistência
3. Código legado será descontinuado
4. Sistema moderno tem arquitetura diferente (componentes standalone, lazy loading)

### Workflow Moderno

```
1. Identificar todas as chaves necessárias no sistema moderno
2. Criar estrutura de namespaces (common, menu, validation, etc)
3. Adicionar chaves ao sistema (SistemaTraducaoChaves)
4. Traduzir pt-BR manualmente (idioma padrão - 100%)
5. Gerar templates para en-US, es-ES, fr-FR
6. Usar Azure Translator para tradução inicial automática
7. Revisão humana das traduções automáticas
8. Ativação de idiomas quando >= 80% completos
```

---

## 6. MAPEAMENTO DE CONCEITOS LEGADO → MODERNO

| Conceito Legado | Conceito Moderno | Exemplo |
|-----------------|------------------|---------|
| `lblNome.Text = "Nome"` | `{{ 'common.labels.name' \| transloco }}` | Angular Transloco |
| `MsgBox("Erro")` | `_localizer["validation.error"]` | .NET IStringLocalizer |
| `DateTime.ToString("dd/MM/yyyy")` | `{{ data \| date:'short':'':'pt-BR' }}` | Angular DatePipe |
| `String.Format("R$ {0:N2}")` | `{{ valor \| currency:'BRL' }}` | Angular CurrencyPipe |
| Relatório Crystal fixo | Template i18n dinâmico | SSRS/HTML com i18n |

---

## 7. ESTIMATIVA DE ESFORÇO DE TRADUÇÃO

### Chaves Estimadas por Módulo

| Módulo | Chaves Estimadas | Justificativa |
|--------|------------------|---------------|
| Common (buttons, labels) | ~200 | Botões e labels reutilizáveis |
| Menu principal | ~50 | Menu navegação |
| Validations | ~300 | Mensagens de erro/aviso |
| Dashboard | ~80 | Widgets e métricas |
| Cadastros (CRUD) | ~400 | 20 CRUDs x ~20 chaves cada |
| Relatórios | ~150 | Labels de relatórios |
| Emails | ~50 | Templates de email |
| Help/Tooltips | ~80 | Textos de ajuda |

**Total Estimado**: ~1.310 chaves

**Sistema Atual**: 1.247 chaves (próximo da estimativa) ✅

---

## 8. DESAFIOS IDENTIFICADOS

### D-I18N-001: Pluralização Complexa

**Legado**: NÃO trata pluralização corretamente

```vb.net
' Legado (incorreto)
lblResultado.Text = count & " item(ns) encontrado(s)"
```

**Moderno**: Usa regras de pluralização por idioma

```json
{
  "search.results": {
    "zero": "Nenhum item encontrado",
    "one": "{{count}} item encontrado",
    "other": "{{count}} itens encontrados"
  }
}
```

---

### D-I18N-002: Gênero de Substantivos

**Legado**: NÃO trata gênero (português tem masculino/feminino)

**Moderno**: Requer chaves separadas quando gênero importa

```json
{
  "user.welcome.male": "Bem-vindo, {{name}}",
  "user.welcome.female": "Bem-vinda, {{name}}"
}
```

---

### D-I18N-003: Ordem de Palavras Diferente por Idioma

**Legado**: Assume ordem pt-BR em interpolações

```vb.net
mensagem = "O usuário " & nome & " foi criado com sucesso"
```

**Moderno**: Interpolação permite reordenamento

```json
{
  "pt-BR": "O usuário {{name}} foi criado com sucesso",
  "en-US": "User {{name}} was successfully created"
}
```

---

## 9. LIÇÕES APRENDIDAS DO LEGADO

### ✅ O QUE FUNCIONA

1. **Simplicidade**: Textos diretos são fáceis de entender no código
2. **Performance**: Sem overhead de lookup de tradução

### ❌ O QUE NÃO FUNCIONA

1. **Manutenibilidade**: Alteração de texto requer alteração de código
2. **Escalabilidade**: Impossível adicionar idiomas sem reescrever
3. **Consistência**: Mesma frase traduzida diferente em lugares diferentes
4. **Experiência do Usuário**: Barreira para internacionalização

---

## 10. RECOMENDAÇÕES PARA SISTEMA MODERNO

### R-I18N-001: Chaves Desde o Início

**Recomendação**: NUNCA hardcodar texto. SEMPRE usar chave i18n desde a primeira linha de código.

❌ **ERRADO**:
```typescript
btnSave.text = "Salvar";  // Hardcoded
```

✅ **CORRETO**:
```typescript
btnSave.text = this.transloco.translate('common.buttons.save');
```

---

### R-I18N-002: Namespaces Claros

**Recomendação**: Estrutura hierárquica clara desde o início.

✅ **BOM**:
```
common.buttons.save
common.buttons.cancel
menu.dashboard
menu.users.list
```

❌ **RUIM**:
```
salvar
cancelar
painel
lista_usuarios
```

---

### R-I18N-003: Contexto para Tradutores

**Recomendação**: Sempre adicionar contexto/comentários para tradutores.

```json
{
  "_comment_save": "Botão de salvar formulário (contexto: edição de cadastro)",
  "save": "Salvar"
}
```

---

## 11. RESUMO EXECUTIVO

### Situação do Legado

- ❌ **Textos hardcoded**: ~150 telas ASPX + VB.NET
- ❌ **Formatação fixa**: pt-BR em datas/moedas
- ❌ **Emails/Relatórios**: Apenas português
- ❌ **Nenhuma biblioteca i18n**: Implementação do zero

### Decisão de Modernização

- ✅ **NÃO migrar** textos do legado
- ✅ **Criar do zero** estrutura moderna
- ✅ **Gestão visual** de idiomas
- ✅ **Suporte a 4+ idiomas** (pt-BR, en-US, es-ES, fr-FR)

### Benefícios da Modernização

1. **Expansão Global**: Sistema pronto para mercado internacional
2. **Manutenibilidade**: Alterar textos sem tocar no código
3. **Flexibilidade**: Adicionar idiomas sob demanda
4. **Profissionalismo**: Tradução humana revisada
5. **Performance**: Cache Redis + Lazy Loading

---

## CHANGELOG

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 2.0 | 2025-12-29 | Agência ALC - alc.dev.br | Referência completa ao legado (problemas, estratégia, lições) |

---

**Status**: Referência Completa ao Legado
**Próximo Documento**: RL-RF005.yaml (estruturado)
