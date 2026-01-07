# RL-RF063 — Referência ao Legado

**Versão:** 1.0
**Data:** 2025-12-30
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF063 - Motor de Templates (Template Engine)
**Sistema Legado:** VB.NET + ASP.NET Web Forms
**Objetivo:** Documentar que o Motor de Templates é uma funcionalidade NOVA sem equivalente direto no sistema legado.

---

## 1. CONTEXTO DO LEGADO

O sistema legado (VB.NET + ASP.NET Web Forms) **NÃO possuía** um motor de templates unificado e reutilizável.

### Características do Legado

- **Arquitetura:** Monolítica WebForms
- **Linguagem / Stack:** VB.NET, ASP.NET Web Forms, SQL Server
- **Templates de E-mail:** Hardcoded em código VB.NET ou strings concatenadas
- **Relatórios:** Gerados via código ou ferramentas externas (Crystal Reports)
- **Multi-tenant:** Não (cada cliente tinha instância separada)
- **Auditoria:** Inexistente para templates
- **Versionamento:** Inexistente

### Problemas Identificados no Legado

1. **Templates Hardcoded:** Conteúdo de e-mails e relatórios embutidos diretamente no código VB.NET, dificultando manutenção e customização.
2. **Falta de Versionamento:** Nenhum histórico de alterações em templates, impossibilitando rollback.
3. **Customização por Cliente:** Para customizar templates, era necessário alterar código e fazer deploy (alto risco).
4. **Sem Preview:** Não havia forma de visualizar templates antes de enviar (erros descobertos em produção).
5. **Multi-idioma Manual:** Tradução de textos via arquivos .resx, sem suporte dinâmico em templates.
6. **Sem Reutilização:** Código duplicado em múltiplos pontos (header, footer, assinatura).

---

## 2. TELAS DO LEGADO

### Conclusão: NÃO EXISTE equivalente direto

O sistema legado **não possuía** tela dedicada para gestão de templates.

Templates de e-mail eram configurados de 3 formas:
1. **Código VB.NET:** Strings concatenadas diretamente no código.
2. **Stored Procedures:** Alguns templates armazenados como TEXT em tabelas SQL.
3. **Arquivos .html:** Templates estáticos em pasta do servidor (sem versionamento).

**Destino:** SUBSTITUÍDO por RF063 (Motor de Templates moderno)

**Justificativa:** Implementação moderna com sintaxe Liquid, versionamento, preview, multi-idioma e isolamento por tenant.

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

Não há webservices legados relacionados a gestão de templates.

Alguns webservices enviavam e-mails, mas o conteúdo era hardcoded:

| Método | Local | Responsabilidade | Destino |
|------|-------|------------------|---------|
| EnviarEmailSolicitacao | WebService/Email.asmx | Enviar e-mail de notificação de solicitação | SUBSTITUÍDO |
| EnviarRelatorio | WebService/Relatorios.asmx | Gerar e enviar relatório por e-mail | SUBSTITUÍDO |

**Destino:** SUBSTITUÍDO - E-mails agora utilizam templates dinâmicos gerenciados pelo RF063.

---

## 4. TABELAS LEGADAS

Não há tabelas legadas dedicadas a templates.

Alguns templates eram armazenados em:

| Tabela | Finalidade | Problemas Identificados | Destino |
|-------|------------|-------------------------|---------|
| ConfiguracaoSistema (TEXT) | Armazenar alguns templates como texto puro | Sem versionamento, sem auditoria, sem multi-tenant, sem validação | DESCARTADO |

**Nova Tabela Moderna:** `Template` (com versionamento, auditoria, multi-tenant, validação Liquid)

---

## 5. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

### RL-RN-001: E-mail de Aprovação de Solicitação (Hardcoded)

**Fonte:** `ic1_legado/IControlIT/Solicitacoes/Aprovar.aspx.vb` - Linha 145

**Regra Implícita:**
> Ao aprovar solicitação, enviar e-mail com assunto "Solicitação #[NUMERO] - Aprovada" e corpo contendo: nome do solicitante, número da solicitação, data de aprovação, aprovador.

**Destino:** ASSUMIDO

**Justificativa:** Regra migrada para template Liquid (`email-aprovacao-solicitacao.liquid`) com variáveis dinâmicas.

**Rastreabilidade:** RN-RF063-001, RN-RF063-002 (Sintaxe Liquid + Contexto Tipado)

---

### RL-RN-002: Formatação de Valores Monetários (Helper VB.NET)

**Fonte:** `ic1_legado/IControlIT/Helpers/FormatHelper.vb` - Linha 23

**Regra Implícita:**
> Valores monetários devem ser formatados como "R$ 1.234,56" (cultura pt-BR).

**Destino:** ASSUMIDO

**Justificativa:** Migrado para filtro Liquid customizado `{{ valor | currency }}`.

**Rastreabilidade:** RN-RF063-003 (Filtros Customizados)

---

### RL-RN-003: Assinatura Padrão de E-mails (Duplicação de Código)

**Fonte:** Múltiplos arquivos `.aspx.vb` (Aprovar.aspx.vb, Rejeitar.aspx.vb, Notificar.aspx.vb)

**Regra Implícita:**
> Todo e-mail deve conter assinatura padrão:
> ```
> Atenciosamente,
> Equipe [NOME_EMPRESA]
> [ENDERECO]
> [TELEFONE]
> ```

**Destino:** SUBSTITUÍDO

**Justificativa:** Código duplicado em 15+ arquivos. Migrado para parcial reutilizável (`{% include 'email-footer' %}`).

**Rastreabilidade:** RN-RF063-009 (Parciais Reutilizáveis)

---

### RL-RN-004: Texto Multi-idioma (Arquivos .resx)

**Fonte:** `ic1_legado/IControlIT/Resources/Messages.pt-BR.resx`

**Regra Implícita:**
> Textos de interface devem suportar pt-BR, en-US, es-ES via arquivos .resx.

**Destino:** SUBSTITUÍDO

**Justificativa:** Arquivos .resx funcionam apenas em código compilado. Migrado para helper Liquid `{{ 't' "chave" }}` com integração ao sistema de i18n moderno (Transloco).

**Rastreabilidade:** RN-RF063-010 (Internacionalização)

---

## 6. GAP ANALYSIS (LEGADO x RF MODERNO)

| Item | Legado | RF Moderno | Observação |
|-----|--------|------------|------------|
| Motor de Templates | NÃO EXISTE | Liquid.NET | Funcionalidade completamente nova |
| Versionamento | NÃO EXISTE | Sim (histórico completo) | Permite rollback |
| Preview de Templates | NÃO EXISTE | Sim (tempo real) | Reduz erros em produção |
| Testes A/B | NÃO EXISTE | Sim | Experimentação de conteúdo |
| Herança de Templates | NÃO EXISTE | Sim (layout base) | Evita duplicação |
| Parciais Reutilizáveis | CÓDIGO DUPLICADO | Sim (header, footer) | Manutenção centralizada |
| Multi-idioma em Templates | .resx (estático) | Helper `{{ 't' }}` (dinâmico) | Tradução sem recompilação |
| Sanitização XSS | NÃO EXISTE | Sim (automático) | Segurança |
| Cache de Templates | NÃO EXISTE | Redis | Performance |
| Auditoria de Uso | NÃO EXISTE | Sim (7 anos LGPD) | Compliance |

---

## 7. DECISÕES DE MODERNIZAÇÃO

### Decisão 1: Adotar Liquid como Sintaxe Padrão

**Motivo:** Liquid é amplamente adotado (Shopify, Jekyll), maduro, seguro (sandbox) e possui biblioteca .NET oficial (Fluid/Liquid.NET).

**Alternativas Avaliadas:**
- Handlebars.NET (menos seguro, sem sandbox)
- Razor (muito acoplado a ASP.NET MVC, difícil isolamento)
- Scriban (menos adoção, documentação limitada)

**Impacto:** Alto

**Data:** 2025-01-14

---

### Decisão 2: Versionamento Obrigatório de Templates

**Motivo:** No legado, alterações em templates causavam problemas sem possibilidade de rollback. Versionamento garante rastreabilidade e auditoria.

**Impacto:** Médio

**Data:** 2025-01-14

---

### Decisão 3: Cache Redis de Templates Compilados

**Motivo:** Parsing de templates a cada renderização é custoso (200-500ms). Cache reduz para <10ms.

**Impacto:** Alto (performance)

**Data:** 2025-01-14

---

### Decisão 4: Sanitização Automática Contra XSS

**Motivo:** Templates podem ser criados por usuários. Sanitização automática previne injeção de scripts maliciosos.

**Impacto:** Crítico (segurança)

**Data:** 2025-01-14

---

## 8. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Probabilidade | Mitigação |
|------|---------|---------------|-----------|
| Templates legados hardcoded não identificados | Alto | Média | Busca em todo código VB.NET por padrões de concatenação de strings |
| Resistência de usuários a nova sintaxe Liquid | Médio | Baixa | Treinamento + documentação + editor com autocomplete |
| Performance de renderização em massa | Alto | Média | Cache Redis + testes de carga antes de produção |
| Quebra de templates existentes ao migrar | Alto | Média | Conversão automatizada + testes paralelos |

---

## 9. RASTREABILIDADE

| Elemento Legado | Referência RF |
|----------------|---------------|
| E-mail hardcoded (Aprovação) | RN-RF063-001, RN-RF063-002 |
| Formatação de valores (FormatHelper.vb) | RN-RF063-003 |
| Assinatura duplicada | RN-RF063-009 |
| Tradução .resx | RN-RF063-010 |
| Nenhuma sanitização XSS | RN-RF063-011 |
| Nenhum versionamento | RN-RF063-005 |
| Nenhum cache | RN-RF063-012 |
| Nenhuma auditoria | RN-RF063-014 |

---

## 10. FUNCIONALIDADES NOVAS (SEM EQUIVALENTE LEGADO)

As seguintes funcionalidades são COMPLETAMENTE NOVAS (não existiam no legado):

1. **Motor de Templates Unificado:** RF063 cria infraestrutura central para todos os templates do sistema.
2. **Preview em Tempo Real:** Impossível no legado (templates hardcoded).
3. **Testes A/B:** Conceito inexistente no legado.
4. **Herança de Templates:** Conceito inexistente no legado.
5. **Documentação Automática de Variáveis:** Conceito inexistente no legado.
6. **Isolamento Multi-Tenant:** Sistema legado não era multi-tenant.

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|------|------|----------|------|
| 1.0 | 2025-12-30 | Referência ao legado - Motor de Templates é funcionalidade NOVA | Agência ALC - alc.dev.br |
