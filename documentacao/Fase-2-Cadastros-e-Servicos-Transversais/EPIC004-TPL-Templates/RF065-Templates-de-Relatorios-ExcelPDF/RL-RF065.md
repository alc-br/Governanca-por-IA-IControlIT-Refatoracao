# RL-RF065 - Referência ao Legado: Templates de Relatórios (Excel/PDF)

**Versão:** 2.0
**Data de Criação:** 2025-12-30
**Governança:** v2.0 (Separação RF/RL)
**Status:** Não Aplicável

---

## 1. RESUMO DO SISTEMA LEGADO

### 1.1 Contexto Histórico

O **RF065 - Templates de Relatórios (Excel/PDF)** é uma **funcionalidade NOVA** que **NÃO possui correspondente no sistema legado** IControlIT (ASP.NET Web Forms + VB.NET).

Este RF foi projetado desde o início seguindo as melhores práticas de geração de relatórios modernos, Clean Architecture e padrões de mercado.

### 1.2 Ausência de Sistema Legado

**NÃO EXISTE** nenhuma tela ASPX, stored procedure, tabela legada ou webservice ASMX relacionado a esta funcionalidade no sistema legado localizado em:
```
D:\IC2\ic1_legado\IControlIT\
```

### 1.3 Motivo da Ausência

O sistema legado **não possuía** sistema estruturado de templates de relatórios com:
- Templates reutilizáveis parametrizados
- Múltiplos formatos de exportação (Excel .xlsx, PDF moderno, CSV)
- Gráficos dinâmicos Chart.js
- Agrupamentos e subtotais automáticos
- Formatação condicional por regras
- Múltiplas abas em Excel
- Agendamento de exportações via Hangfire
- Cabeçalho/rodapé customizados
- Proteção de planilhas Excel
- Assinatura digital PDF
- Marca d'água em PDFs
- Integração com cubos OLAP
- Cache de relatórios pesados (Redis)
- Compactação ZIP de múltiplos relatórios
- Métricas de uso de templates

Esta funcionalidade foi identificada como **necessidade crítica** durante a modernização do sistema, sendo projetada inteiramente do zero com base em:
- Bibliotecas modernas (.NET 10: EPPlus, QuestPDF, CsvHelper)
- Melhores práticas de geração de relatórios
- Requisitos de compliance e auditoria
- Necessidade de padronização de relatórios gerenciais

---

## 2. INVENTÁRIO DE ARTEFATOS LEGADOS

### 2.1 Telas ASPX

**NENHUMA** tela ASPX corresponde a esta funcionalidade.

**Observação:** Embora o sistema legado possua telas genéricas de relatórios (ex: `Relatorios.aspx`), estas **não possuem** templates reutilizáveis, gráficos dinâmicos, múltiplos formatos ou quaisquer características do RF065.

### 2.2 Code-Behind (VB.NET)

**NENHUM** arquivo `.aspx.vb` corresponde a esta funcionalidade.

### 2.3 Stored Procedures

**NENHUMA** stored procedure T-SQL corresponde a esta funcionalidade.

**Observação:** O legado pode ter SPs de extração de dados, mas **não há** lógica de templates, formatação ou geração de Excel/PDF estruturado.

### 2.4 Tabelas do Banco de Dados

**NENHUMA** tabela do banco legado corresponde diretamente a esta funcionalidade.

**Observação:** Não existem tabelas como `TemplateRelatorio`, `ParametroTemplate`, `AgendamentoRelatorio` ou similares no banco legado.

### 2.5 WebServices ASMX

**NENHUM** webservice ASMX corresponde a esta funcionalidade.

### 2.6 Integrações Externas

**NENHUMA** integração externa legada corresponde a esta funcionalidade.

---

## 3. ANÁLISE COMPARATIVA: LEGADO vs. MODERNO

### 3.1 Comparação de Funcionalidades

| Funcionalidade | Sistema Legado | RF065 Moderno |
|----------------|----------------|---------------|
| Templates reutilizáveis | ❌ NÃO EXISTE | ✅ Parametrizados |
| Formatos de exportação | ❌ Excel .xls antigo | ✅ .xlsx, PDF, CSV |
| Gráficos dinâmicos | ❌ NÃO EXISTE | ✅ Chart.js (4 tipos) |
| Agrupamentos automáticos | ❌ Manual | ✅ Configurável |
| Formatação condicional | ❌ NÃO EXISTE | ✅ Por regras |
| Múltiplas abas Excel | ❌ NÃO EXISTE | ✅ Configurável |
| Parâmetros dinâmicos | ❌ Hardcoded | ✅ Obrigatórios |
| Agendamento automático | ❌ NÃO EXISTE | ✅ Hangfire |
| Cabeçalho/rodapé custom | ❌ NÃO EXISTE | ✅ Customizados |
| Proteção planilhas | ❌ NÃO EXISTE | ✅ Senha/somente leitura |
| Assinatura digital PDF | ❌ NÃO EXISTE | ✅ X.509 |
| Marca d'água PDF | ❌ NÃO EXISTE | ✅ Configurável |
| Integração OLAP | ❌ NÃO EXISTE | ✅ MDX queries |
| Cache de relatórios | ❌ NÃO EXISTE | ✅ Redis 15 min |
| Compactação ZIP | ❌ NÃO EXISTE | ✅ Múltiplos relatórios |
| Métricas de uso | ❌ NÃO EXISTE | ✅ Tracking completo |

### 3.2 Conclusão da Análise

O **RF065 é 100% novo**, sem nenhuma correspondência no sistema legado. Toda a funcionalidade foi projetada do zero com base em:
- Bibliotecas .NET modernas (EPPlus, QuestPDF, CsvHelper)
- Chart.js para gráficos dinâmicos
- Hangfire para agendamento
- Redis para cache
- Azure Blob Storage para armazenamento
- SQL Server Analysis Services (OLAP)

---

## 4. PROBLEMAS IDENTIFICADOS NO LEGADO

### 4.1 Ausência de Templates Reutilizáveis

**Problema:** Sistema legado não possuía templates parametrizados, obrigando:
- Criar relatórios do zero sempre
- Duplicar lógica de formatação
- Manter código espalhado em múltiplos arquivos

**Impacto:** Retrabalho, inconsistência visual, dificuldade de manutenção.

**Solução no RF065:** Templates reutilizáveis com parâmetros dinâmicos (data, empresa, status, etc.).

### 4.2 Ausência de Gráficos Dinâmicos

**Problema:** Sistema legado não possuía gráficos dinâmicos integrados aos relatórios.

**Impacto:** Relatórios apenas tabulares, baixa visualização de dados.

**Solução no RF065:** Chart.js com 4 tipos de gráficos (linha, barra, pizza, área) renderizados em Excel e PDF.

### 4.3 Ausência de Agendamento Automático

**Problema:** Sistema legado não possuía agendamento de exportações, dependendo de ação manual do usuário.

**Impacto:** Relatórios gerenciais não eram gerados regularmente, perda de produtividade.

**Solução no RF065:** Job Hangfire permite agendamento diário/semanal/mensal com envio automático por e-mail.

### 4.4 Ausência de Cache de Relatórios Pesados

**Problema:** Sistema legado não possuía cache, re-processando relatórios pesados sempre.

**Impacto:** Timeout em relatórios grandes, sobrecarga do banco de dados.

**Solução no RF065:** Redis cache com TTL 15 minutos reduz carga do banco e acelera geração.

---

## 5. JUSTIFICATIVA PARA AUSÊNCIA DE MIGRAÇÃO

### 5.1 Por Que Não Houve Migração de Dados

**NÃO HÁ DADOS** para migrar, pois:
- Sistema legado não possuía tabelas de templates
- Não existem agendamentos configurados no legado
- Não existem parâmetros dinâmicos no legado
- Não existem configurações de gráficos no legado

### 5.2 Abordagem de Implementação

O RF065 será implementado **do zero**, seguindo as fases:

1. **Fase 1 - Backend**:
   - Criar entidades (TemplateRelatorio, ParametroTemplate, AgendamentoRelatorio, etc.)
   - Criar Commands e Queries (CQRS)
   - Criar Validators (FluentValidation)
   - Criar Services (ExcelGeneratorService, PdfGeneratorService, CsvGeneratorService)
   - Criar Jobs Hangfire (agendamento, limpeza cache, notificações)
   - Integrar EPPlus (Excel), QuestPDF (PDF), CsvHelper (CSV)

2. **Fase 2 - Frontend**:
   - Criar componentes Angular 19 (template-list, template-form, template-preview)
   - Criar wizard de criação de templates
   - Criar configurador de parâmetros dinâmicos
   - Criar agendador de exportações
   - Integrar Chart.js para preview de gráficos

3. **Fase 3 - Testes**:
   - Testes unitários (backend)
   - Testes E2E (Playwright)
   - Testes de carga (geração de relatórios pesados)
   - Testes de integridade (Excel/PDF/CSV)

4. **Fase 4 - Seed Inicial**:
   - Criar templates de exemplo (relatório de usuários, relatório de ativos)
   - Configurar parâmetros padrão (período, empresa, status)
   - Criar agendamentos iniciais
   - Gerar relatórios de teste

---

## 6. REGRAS DE NEGÓCIO LEGADAS

### 6.1 Regras Identificadas

**NENHUMA** regra de negócio legada foi identificada para esta funcionalidade.

### 6.2 Regras Assumidas vs. Descartadas

Como não há sistema legado, **não há regras assumidas ou descartadas**.

Todas as 15 regras de negócio (RN-RF065-001 a RN-RF065-015) do RF065 foram criadas **do zero** com base em:
- Melhores práticas de geração de relatórios
- Requisitos de stakeholders
- Bibliotecas modernas (.NET 10)
- Necessidades de compliance

---

## 7. DECISÕES DE TRANSIÇÃO

### 7.1 Estratégia de Corte

**NÃO APLICÁVEL** - Não há sistema legado para descontinuar.

O RF065 será **novo** e coexistirá com outros módulos de relatórios do sistema moderno.

### 7.2 Cronograma de Desativação

**NÃO APLICÁVEL** - Não há funcionalidade legada para desativar.

### 7.3 Plano de Rollback

Em caso de problemas na implementação do RF065:

1. **Rollback de Código**: Reverter para branch anterior
2. **Rollback de Banco**: Remover migrations do RF065
3. **Fallback Operacional**: Operar temporariamente sem templates (gerar relatórios manualmente via SQL/Excel)

**Observação:** Como não há legado, não há "sistema anterior" para voltar.

---

## 8. CONCLUSÃO

### 8.1 Situação Atual

- ✅ **RF065.md v2.0** criado (11 seções canônicas)
- ✅ **RF065.yaml** criado (sincronizado com RF.md)
- ✅ **RL-RF065.md** criado (documenta ausência de legado)
- 🔄 **RL-RF065.yaml** será criado (com seção `referencias` vazia)

### 8.2 Próximos Passos

1. Criar RL-RF065.yaml (estrutura válida com `referencias: []`)
2. Executar validator-rl.py RF065 (deve passar mesmo com referências vazias)
3. Atualizar STATUS.yaml (marcar v2.0 completo)
4. Commit Git de todos os artefatos

### 8.3 Status de Governança

- **Governança v2.0:** ✅ Aderente
- **Separação RF/RL:** ✅ Completa (RL documenta ausência de legado)
- **Rastreabilidade:** ✅ Total (documentado que não há legado)
- **Validação Pendente:** 🔄 Executar validator-rl.py

---

**Documento controlado pela Governança v2.0 - IControlIT**
**Última revisão:** 2025-12-30
