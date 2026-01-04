# Casos de Uso - RF018

**Versão:** 1.0
**Data:** 2025-12-17
**Autor:** Agência ALC - alc.dev.br
**Epic:** EPIC003-CAD-Cadastros-Base
**Fase:** Fase 2 - Cadastros e Serviços Transversais
**RF Relacionado:** [RF018 - Gestao-de-Cargos](./RF018.md)

---

## Índice de Casos de Uso

| UC | Nome | Descrição |
|----|------|-----------|
| UC00 | UC00 - Listar Cargos | Caso de uso |
| UC01 | UC01 - Criar Cargo | Caso de uso |
| UC02 | UC02 - Visualizar Cargo | Caso de uso |
| UC03 | UC03 - Editar Cargo | Caso de uso |
| UC04 | UC04 - Inativar Cargo | Caso de uso |
| UC06 | UC06 - Registrar Manutenção de Ativo | Caso de uso |
| UC08 | UC08 - Inventário Mobile com GPS | Caso de uso |
| UC09 | UC09 - Visualizar/Imprimir QR Code | Caso de uso |
| UC10 | UC10 - Calcular Depreciação Automática | Caso de uso |

---

# UC00 - Listar Cargos

**ID do Caso de Uso**: UC00
**Nome do Caso de Uso**: Listar Cargos
**Requisito Funcional**: RF-CAD-009
**Autor**: Equipe IControlIT
**Status**: Em Desenvolvimento

---

## Índice

1. [Informações Gerais](#1-informações-gerais)
2. [Fluxo Principal](#2-fluxo-principal)
3. [Fluxos Alternativos](#3-fluxos-alternativos)
4. [Fluxos de Exceção](#4-fluxos-de-exceção)
5. [Regras de Negócio](#5-regras-de-negócio)
6. [Especificação de Testes](#6-especificação-de-testes)
7. [Matriz de Permissões](#7-matriz-de-permissões)
8. [Casos de Teste Detalhados](#8-casos-de-teste-detalhados)

---

## 1. Informações Gerais

### 1.1. Descrição

Este caso de uso permite que usuários autorizados listem e visualizem todos os cargos cadastrados no sistema IControlIT, com recursos de filtros avançados, paginação, ordenação e busca. A listagem respeita o contexto multi-tenant (Id_Conglomerado) e exibe informações completas sobre cada cargo, incluindo sua hierarquia, competências associadas, benefícios e dados salariais.

### 1.2. Atores

- **Ator Principal**: Usuário Autenticado com permissão `cadastros:cargo:read`
- **Atores Secundários**:
  - Sistema de Auditoria (registra acessos)
  - Sistema de Cache (otimiza consultas)
  - API Backend (.NET 10)

### 1.3. Pré-condições

| ID | Descrição |
|----|-----------|
| PRE-01 | Usuário deve estar autenticado no sistema |
| PRE-02 | Usuário deve possuir permissão `cadastros:cargo:read` |
| PRE-03 | Conexão com banco de dados deve estar disponível |
| PRE-04 | Id_Conglomerado do usuário deve estar definido no contexto da sessão |
| PRE-05 | Sistema de auditoria deve estar operacional |

### 1.4. Pós-condições

| ID | Descrição |
|----|-----------|
| POS-01 | Lista de cargos é exibida conforme filtros aplicados |
| POS-02 | Operação de listagem é registrada no log de auditoria |
| POS-03 | Dados são armazenados em cache para otimização |
| POS-04 | Contadores de paginação são atualizados corretamente |
| POS-05 | Estado dos filtros é preservado na sessão do usuário |

### 1.5. Requisitos Não-Funcionais

| ID | Tipo | Descrição | Meta |
|----|------|-----------|------|
| RNF-01 | Performance | Tempo de resposta da listagem | < 2 segundos para até 10.000 registros |
| RNF-02 | Usabilidade | Interface responsiva e intuitiva | Compatível com desktop, tablet e mobile |
| RNF-03 | Segurança | Isolamento multi-tenant | 100% dos registros filtrados por Id_Conglomerado |
| RNF-04 | Disponibilidade | Sistema deve estar disponível | 99.5% uptime |
| RNF-05 | Escalabilidade | Suporte a crescimento de dados | Até 100.000 cargos por conglomerado |
| RNF-06 | Auditoria | Registro de todas as operações | 100% das consultas auditadas |
| RNF-07 | Cache | Utilização de cache distribuído | Cache de 5 minutos para consultas repetidas |

---

## 2. Fluxo Principal

**Trigger**: Usuário acessa o menu "Cadastros > Cargos" ou navega para `/cadastros/cargos`

| Passo | Ator | Descrição | Sistema |
|-------|------|-----------|---------|
| 1 | Usuário | Acessa a página de listagem de cargos | Sistema valida autenticação |
| 2 | Sistema | Valida permissão `cadastros:cargo:read` do usuário | Middleware de autorização |
| 3 | Sistema | Recupera Id_Conglomerado do contexto do usuário | TenantContext |
| 4 | Sistema | Verifica existência de cache válido para a consulta | Redis/MemoryCache |
| 5 | Sistema | Se não há cache, executa query no banco de dados | EF Core + SQL Server |
| 6 | Sistema | Aplica filtro WHERE Fl_Ativo = 1 AND Id_Conglomerado = @IdConglomerado | Query SQL |
| 7 | Sistema | Recupera dados relacionados: Cargo_Superior, Competências, Benefícios | Eager Loading |
| 8 | Sistema | Aplica ordenação padrão por Nm_Cargo ASC | OrderBy |
| 9 | Sistema | Aplica paginação (padrão: 20 registros por página) | Skip/Take |
| 10 | Sistema | Calcula total de registros e total de páginas | Count query |
| 11 | Sistema | Formata resposta JSON com dados dos cargos | DTO Serialization |
| 12 | Sistema | Armazena resultado em cache por 5 minutos | Cache Set |
| 13 | Sistema | Registra operação no log de auditoria | AuditLog.Create |
| 14 | Sistema | Retorna response com status 200 OK | HTTP Response |
| 15 | Frontend | Renderiza tabela com lista de cargos | Angular DataTable |
| 16 | Frontend | Exibe paginação, filtros e controles de ordenação | UI Components |
| 17 | Frontend | Habilita ações por registro (visualizar, editar, inativar) | Action Buttons |
| 18 | Sistema | Monitora performance da operação | Application Insights |

---

## 3. Fluxos Alternativos

### FA01 - Aplicar Filtro por Nome

**Trigger**: Usuário digita texto no campo de busca por nome

| Passo | Descrição |
|-------|-----------|
| FA01.1 | Usuário digita texto no campo "Buscar por Nome" |
| FA01.2 | Sistema aguarda 500ms após última digitação (debounce) |
| FA01.3 | Sistema adiciona cláusula WHERE com LIKE '%@termo%' |
| FA01.4 | Sistema executa nova consulta com filtro aplicado |
| FA01.5 | Sistema invalida cache anterior |
| FA01.6 | Sistema retorna ao passo 10 do Fluxo Principal |

### FA02 - Aplicar Filtro por Código

**Trigger**: Usuário digita código no campo de busca por código

| Passo | Descrição |
|-------|-----------|
| FA02.1 | Usuário digita código no campo "Buscar por Código" |
| FA02.2 | Sistema aguarda 500ms após última digitação (debounce) |
| FA02.3 | Sistema adiciona cláusula WHERE Cd_Cargo LIKE '@codigo%' |
| FA02.4 | Sistema executa nova consulta com filtro aplicado |
| FA02.5 | Sistema retorna ao passo 10 do Fluxo Principal |

### FA03 - Aplicar Ordenação Customizada

**Trigger**: Usuário clica em cabeçalho de coluna para ordenar

| Passo | Descrição |
|-------|-----------|
| FA03.1 | Usuário clica no cabeçalho de uma coluna (Nome, Código, Salário, etc) |
| FA03.2 | Sistema identifica coluna clicada e direção atual (ASC/DESC) |
| FA03.3 | Sistema inverte direção se coluna já estava ordenada por ela |
| FA03.4 | Sistema adiciona ORDER BY @coluna @direcao na query |
| FA03.5 | Sistema invalida cache |
| FA03.6 | Sistema retorna ao passo 5 do Fluxo Principal |

### FA04 - Alterar Quantidade de Registros por Página

**Trigger**: Usuário seleciona nova quantidade no seletor de paginação

| Passo | Descrição |
|-------|-----------|
| FA04.1 | Usuário seleciona nova quantidade (10, 20, 50, 100) no dropdown |
| FA04.2 | Sistema atualiza parâmetro pageSize |
| FA04.3 | Sistema recalcula número total de páginas |
| FA04.4 | Sistema ajusta página atual se necessário (para não ultrapassar total) |
| FA04.5 | Sistema invalida cache |
| FA04.6 | Sistema retorna ao passo 5 do Fluxo Principal |

### FA05 - Navegar entre Páginas

**Trigger**: Usuário clica em botão de navegação ou número de página

| Passo | Descrição |
|-------|-----------|
| FA05.1 | Usuário clica em botão (Anterior, Próxima, Primeira, Última) ou número |
| FA05.2 | Sistema valida se página solicitada existe |
| FA05.3 | Sistema atualiza parâmetro pageNumber |
| FA05.4 | Sistema ajusta Skip() na query conforme nova página |
| FA05.5 | Sistema verifica cache para nova página |
| FA05.6 | Sistema retorna ao passo 5 do Fluxo Principal |

### FA06 - Filtrar por Faixa Salarial

**Trigger**: Usuário define faixa salarial mínima e/ou máxima

| Passo | Descrição |
|-------|-----------|
| FA06.1 | Usuário insere valores em "Salário Mínimo" e/ou "Salário Máximo" |
| FA06.2 | Sistema valida que valores são numéricos positivos |
| FA06.3 | Sistema valida que salário mínimo <= salário máximo (se ambos preenchidos) |
| FA06.4 | Sistema adiciona cláusulas WHERE para Vl_Salario_Base_Min e Vl_Salario_Base_Max |
| FA06.5 | Sistema executa nova consulta com filtros aplicados |
| FA06.6 | Sistema retorna ao passo 10 do Fluxo Principal |

### FA07 - Filtrar por Cargo Superior

**Trigger**: Usuário seleciona cargo superior específico

| Passo | Descrição |
|-------|-----------|
| FA07.1 | Usuário clica no dropdown "Cargo Superior" |
| FA07.2 | Sistema carrega lista de cargos disponíveis para seleção |
| FA07.3 | Usuário seleciona um cargo |
| FA07.4 | Sistema adiciona cláusula WHERE Id_Cargo_Superior = @idCargo |
| FA07.5 | Sistema executa nova consulta filtrada |
| FA07.6 | Sistema retorna ao passo 10 do Fluxo Principal |

### FA08 - Exportar Lista para Excel

**Trigger**: Usuário clica no botão "Exportar para Excel"

| Passo | Descrição |
|-------|-----------|
| FA08.1 | Usuário clica no botão "Exportar" > "Excel" |
| FA08.2 | Sistema valida permissão `cadastros:cargo:export` |
| FA08.3 | Sistema executa query sem paginação (todos os registros filtrados) |
| FA08.4 | Sistema gera arquivo XLSX usando EPPlus/ClosedXML |
| FA08.5 | Sistema aplica formatação (cabeçalhos, bordas, cores) |
| FA08.6 | Sistema registra exportação na auditoria |
| FA08.7 | Sistema retorna arquivo para download no navegador |
| FA08.8 | Frontend inicia download automático do arquivo |

### FA09 - Visualizar Apenas Cargos Raiz (Sem Superior)

**Trigger**: Usuário marca checkbox "Apenas Cargos Raiz"

| Passo | Descrição |
|-------|-----------|
| FA09.1 | Usuário marca checkbox "Apenas Cargos Raiz" |
| FA09.2 | Sistema adiciona cláusula WHERE Id_Cargo_Superior IS NULL |
| FA09.3 | Sistema executa nova consulta filtrada |
| FA09.4 | Sistema retorna ao passo 10 do Fluxo Principal |

### FA10 - Limpar Todos os Filtros

**Trigger**: Usuário clica no botão "Limpar Filtros"

| Passo | Descrição |
|-------|-----------|
| FA10.1 | Usuário clica no botão "Limpar Filtros" |
| FA10.2 | Sistema reseta todos os parâmetros de filtro para valores padrão |
| FA10.3 | Sistema reseta ordenação para padrão (Nm_Cargo ASC) |
| FA10.4 | Sistema reseta paginação para primeira página |
| FA10.5 | Sistema invalida cache |
| FA10.6 | Sistema retorna ao passo 5 do Fluxo Principal |

---

## 4. Fluxos de Exceção

### FE01 - Usuário Sem Permissão

**Trigger**: Usuário não possui permissão `cadastros:cargo:read`

| Passo | Descrição |
|-------|-----------|
| FE01.1 | Sistema detecta ausência de permissão no passo 2 |
| FE01.2 | Sistema retorna HTTP 403 Forbidden |
| FE01.3 | Sistema registra tentativa de acesso não autorizado na auditoria |
| FE01.4 | Frontend exibe mensagem: "Você não tem permissão para acessar esta página" |
| FE01.5 | Frontend redireciona para dashboard após 3 segundos |
| FE01.6 | Caso de uso é encerrado |

### FE02 - Erro de Conexão com Banco de Dados

**Trigger**: Banco de dados está indisponível ou timeout

| Passo | Descrição |
|-------|-----------|
| FE02.1 | Sistema tenta executar query e recebe exceção de conexão |
| FE02.2 | Sistema tenta reconectar (retry pattern - 3 tentativas) |
| FE02.3 | Se todas as tentativas falharem, sistema retorna HTTP 503 Service Unavailable |
| FE02.4 | Sistema registra erro detalhado no log (Application Insights) |
| FE02.5 | Frontend exibe mensagem: "Serviço temporariamente indisponível. Tente novamente em alguns instantes." |
| FE02.6 | Sistema envia alerta para equipe de operações |
| FE02.7 | Caso de uso é encerrado |

### FE03 - Erro no Sistema de Cache

**Trigger**: Redis ou cache distribuído está indisponível

| Passo | Descrição |
|-------|-----------|
| FE03.1 | Sistema tenta acessar cache e recebe exceção |
| FE03.2 | Sistema registra warning no log |
| FE03.3 | Sistema continua operação consultando diretamente o banco (fallback) |
| FE03.4 | Sistema retorna ao passo 5 do Fluxo Principal (ignorando cache) |
| FE03.5 | Sistema não interrompe a operação do usuário |

### FE04 - Nenhum Registro Encontrado

**Trigger**: Query retorna 0 registros

| Passo | Descrição |
|-------|-----------|
| FE04.1 | Sistema executa query e recebe resultset vazio |
| FE04.2 | Sistema retorna HTTP 200 OK com array vazio |
| FE04.3 | Sistema registra operação na auditoria normalmente |
| FE04.4 | Frontend exibe mensagem: "Nenhum cargo encontrado com os filtros aplicados" |
| FE04.5 | Frontend exibe botão "Limpar Filtros" em destaque |
| FE04.6 | Frontend mantém filtros e paginação no estado atual |

### FE05 - Página Solicitada Fora do Intervalo

**Trigger**: Usuário tenta acessar página que não existe (ex: página 999 quando há apenas 10)

| Passo | Descrição |
|-------|-----------|
| FE05.1 | Sistema detecta que pageNumber > totalPages |
| FE05.2 | Sistema ajusta automaticamente para última página válida |
| FE05.3 | Sistema retorna HTTP 200 OK com dados da última página |
| FE05.4 | Sistema registra warning no log |
| FE05.5 | Frontend atualiza número da página atual na UI |
| FE05.6 | Sistema retorna ao passo 10 do Fluxo Principal |

### FE06 - Parâmetros de Filtro Inválidos

**Trigger**: Usuário envia parâmetros com formato inválido

| Passo | Descrição |
|-------|-----------|
| FE06.1 | Sistema valida parâmetros recebidos (pageSize, pageNumber, etc) |
| FE06.2 | Sistema detecta valor inválido (ex: pageSize = -10 ou "abc") |
| FE06.3 | Sistema retorna HTTP 400 Bad Request |
| FE06.4 | Sistema inclui detalhes do erro no response body |
| FE06.5 | Sistema registra erro de validação no log |
| FE06.6 | Frontend exibe mensagem: "Parâmetros de busca inválidos" |
| FE06.7 | Frontend reseta filtros para valores padrão |
| FE06.8 | Caso de uso é encerrado |

### FE07 - Timeout na Consulta

**Trigger**: Query demora mais que o timeout configurado (30 segundos)

| Passo | Descrição |
|-------|-----------|
| FE07.1 | Sistema executa query e atinge timeout |
| FE07.2 | Sistema cancela operação e libera recursos |
| FE07.3 | Sistema retorna HTTP 504 Gateway Timeout |
| FE07.4 | Sistema registra erro detalhado com query executada |
| FE07.5 | Frontend exibe mensagem: "A consulta demorou muito. Tente aplicar filtros para reduzir os resultados." |
| FE07.6 | Sistema envia alerta para DBA avaliar performance |
| FE07.7 | Caso de uso é encerrado |

### FE08 - Erro de Serialização JSON

**Trigger**: Erro ao serializar objetos para JSON

| Passo | Descrição |
|-------|-----------|
| FE08.1 | Sistema recupera dados do banco com sucesso |
| FE08.2 | Sistema tenta serializar para JSON e recebe exceção |
| FE08.3 | Sistema retorna HTTP 500 Internal Server Error |
| FE08.4 | Sistema registra stack trace completo no log |
| FE08.5 | Sistema registra dados problemáticos para análise |
| FE08.6 | Frontend exibe mensagem: "Erro ao processar dados. Contate o suporte." |
| FE08.7 | Caso de uso é encerrado |

---

## 5. Regras de Negócio

### RN-CAD-009-01: Isolamento Multi-tenant

**Descrição**: Todos os cargos listados devem pertencer ao conglomerado do usuário autenticado.

**Criticidade**: CRÍTICA

**Implementação**:
- WHERE Id_Conglomerado = @IdConglomerado em todas as queries
- Validação no middleware TenantContext
- Auditoria de violações

**Teste**:
- Verificar que usuário do conglomerado A não vê cargos do conglomerado B
- Verificar que tentativa de manipular Id_Conglomerado na request é bloqueada

### RN-CAD-009-02: Soft Delete

**Descrição**: Apenas cargos ativos (Fl_Ativo = 1) devem ser exibidos na listagem padrão.

**Criticidade**: ALTA

**Implementação**:
- WHERE Fl_Ativo = 1 em todas as queries de listagem
- Filtro separado "Exibir Inativos" para usuários com permissão especial

**Teste**:
- Verificar que cargo inativado não aparece na listagem padrão
- Verificar que cargo inativado aparece quando filtro "Exibir Inativos" é marcado (se usuário tem permissão)

### RN-CAD-009-03: Ordenação Padrão

**Descrição**: A listagem deve ser ordenada por nome do cargo (alfabética crescente) por padrão.

**Criticidade**: MÉDIA

**Implementação**:
- ORDER BY Nm_Cargo ASC como padrão
- Permitir customização pelo usuário

**Teste**:
- Verificar que ao acessar página pela primeira vez, lista está ordenada por nome
- Verificar que ordenação pode ser alterada pelo usuário

### RN-CAD-009-04: Paginação Obrigatória

**Descrição**: Listagens devem sempre ser paginadas para evitar sobrecarga.

**Criticidade**: ALTA

**Implementação**:
- Paginação padrão: 20 registros por página
- Opções: 10, 20, 50, 100 registros por página
- Máximo absoluto: 100 registros por página

**Teste**:
- Verificar que não é possível requisitar mais de 100 registros por página
- Verificar que paginação funciona corretamente com diferentes tamanhos

### RN-CAD-009-05: Cache de Consultas

**Descrição**: Consultas idênticas devem ser servidas do cache por 5 minutos.

**Criticidade**: MÉDIA

**Implementação**:
- Cache key: hash(Id_Conglomerado + filtros + ordenação + paginação)
- TTL: 5 minutos
- Invalidação: ao criar, editar ou inativar cargo

**Teste**:
- Verificar que segunda consulta idêntica é mais rápida (vem do cache)
- Verificar que cache é invalidado após alteração de dados

### RN-CAD-009-06: Hierarquia na Listagem

**Descrição**: A listagem deve exibir o nome do cargo superior quando existir.

**Criticidade**: MÉDIA

**Implementação**:
- Eager loading de Cargo_Superior
- Exibição de "Cargo Raiz" quando não há superior
- Link clicável para cargo superior

**Teste**:
- Verificar que cargo com superior exibe nome corretamente
- Verificar que cargo raiz exibe indicação apropriada

### RN-CAD-009-07: Auditoria de Acesso

**Descrição**: Toda operação de listagem deve ser registrada na auditoria.

**Criticidade**: ALTA

**Implementação**:
- Registro de: usuário, data/hora, filtros aplicados, quantidade de registros retornados
- Não registrar conteúdo completo dos dados (apenas metadados)

**Teste**:
- Verificar que após listar cargos, há registro na auditoria
- Verificar que registro contém informações corretas

### RN-CAD-009-08: Performance

**Descrição**: A listagem deve responder em menos de 2 segundos para até 10.000 registros.

**Criticidade**: ALTA

**Implementação**:
- Índices no banco: (Id_Conglomerado, Fl_Ativo, Nm_Cargo)
- Paginação obrigatória
- Cache distribuído
- Query optimization (SELECT apenas campos necessários)

**Teste**:
- Teste de carga com 10.000 registros
- Verificar tempo de resposta < 2 segundos no percentil 95

### RN-CAD-009-09: Filtros Múltiplos

**Descrição**: Usuário pode aplicar múltiplos filtros simultaneamente (AND lógico).

**Criticidade**: MÉDIA

**Implementação**:
- Todos os filtros são combinados com AND
- Filtros vazios são ignorados na query

**Teste**:
- Aplicar filtro de nome + faixa salarial e verificar que ambos são respeitados
- Verificar que resultado atende a TODOS os critérios simultaneamente

### RN-CAD-009-10: Segurança - Proteção contra SQL Injection

**Descrição**: Todos os parâmetros devem ser sanitizados e usar prepared statements.

**Criticidade**: CRÍTICA

**Implementação**:
- Uso de Entity Framework Core (proteção nativa)
- Validação de input com Data Annotations
- Sanitização de strings de busca

**Teste**:
- Tentar injetar SQL através de campos de busca
- Verificar que tentativas são bloqueadas e registradas

---

## 6. Especificação de Testes

### 6.1. Cenários de Teste Backend

| ID | Cenário | Tipo | Prioridade |
|----|---------|------|------------|
| CN-UC00-001 | Listar cargos com sucesso sem filtros | Positivo | Alta |
| CN-UC00-002 | Listar cargos aplicando filtro por nome | Positivo | Alta |
| CN-UC00-003 | Listar cargos aplicando filtro por código | Positivo | Alta |
| CN-UC00-004 | Listar cargos aplicando filtro por faixa salarial | Positivo | Média |
| CN-UC00-005 | Listar cargos com paginação customizada | Positivo | Alta |
| CN-UC00-006 | Listar cargos com ordenação customizada | Positivo | Média |
| CN-UC00-007 | Listar cargos sem permissão | Negativo | Alta |
| CN-UC00-008 | Listar cargos com banco de dados indisponível | Exceção | Alta |
| CN-UC00-009 | Listar cargos com parâmetros inválidos | Negativo | Média |
| CN-UC00-010 | Verificar isolamento multi-tenant | Segurança | Crítica |

### 6.2. Casos de Teste Sistema (E2E)

| ID | Caso de Teste | Tipo | Prioridade |
|----|---------------|------|------------|
| TC-UC00-001 | Acessar página e visualizar lista padrão | Funcional | Alta |
| TC-UC00-002 | Aplicar filtros e verificar resultados | Funcional | Alta |
| TC-UC00-003 | Navegar entre páginas | Funcional | Alta |
| TC-UC00-004 | Alterar ordenação clicando em colunas | Funcional | Média |
| TC-UC00-005 | Exportar lista para Excel | Funcional | Média |
| TC-UC00-006 | Limpar filtros aplicados | Funcional | Média |
| TC-UC00-007 | Verificar responsividade mobile | UI/UX | Baixa |

### 6.3. Testes de Performance

| ID | Teste | Meta | Prioridade |
|----|-------|------|------------|
| PERF-UC00-001 | Tempo de resposta para 1.000 registros | < 1s | Alta |
| PERF-UC00-002 | Tempo de resposta para 10.000 registros | < 2s | Alta |
| PERF-UC00-003 | Tempo de resposta com cache | < 200ms | Média |
| PERF-UC00-004 | Carga concorrente (100 usuários) | < 3s (p95) | Média |

---

## 7. Matriz de Permissões

| Permissão | Descrição | Permite Listagem | Permite Filtros | Permite Exportação |
|-----------|-----------|------------------|-----------------|-------------------|
| `cadastros:cargo:read` | Leitura básica de cargos | ✅ Sim | ✅ Sim | ❌ Não |
| `cadastros:cargo:export` | Exportação de dados | ✅ Sim | ✅ Sim | ✅ Sim |
| `cadastros:cargo:admin` | Administração completa | ✅ Sim | ✅ Sim | ✅ Sim |
| `cadastros:cargo:view_inactive` | Visualizar inativos | ✅ Sim | ✅ Sim + Inativos | ❌ Não |

**Herança de Permissões**:
- `cadastros:cargo:admin` inclui automaticamente todas as permissões acima
- `cadastros:cargo:export` requer `cadastros:cargo:read` como pré-requisito

---

## 8. Casos de Teste Detalhados

### CT-001: Listar Cargos com Sucesso

**Pré-condições**:
- Usuário autenticado com permissão `cadastros:cargo:read`
- Existem 50 cargos ativos no conglomerado do usuário

**Dados de Entrada**:
- Nenhum filtro aplicado
- Paginação padrão (página 1, 20 registros)

**Passos**:
1. Fazer requisição GET para `/api/v1/cadastros/cargos`
2. Aguardar resposta

**Resultado Esperado**:
- Status: 200 OK
- Body contém array com 20 cargos
- Header `X-Total-Count` = 50
- Header `X-Total-Pages` = 3
- Cada cargo contém: Id, Código, Nome, Salário Base Min/Max, Cargo Superior
- Tempo de resposta < 2 segundos

### CT-002: Filtrar por Nome Parcial

**Pré-condições**:
- Usuário autenticado com permissão `cadastros:cargo:read`
- Existem cargos com nomes: "Analista de Sistemas", "Analista de Suporte", "Gerente de TI"

**Dados de Entrada**:
- Filtro: `nome=Analista`
- Paginação padrão

**Passos**:
1. Fazer requisição GET para `/api/v1/cadastros/cargos?nome=Analista`
2. Aguardar resposta

**Resultado Esperado**:
- Status: 200 OK
- Body contém apenas cargos com "Analista" no nome (2 registros)
- "Gerente de TI" NÃO aparece na lista
- Header `X-Total-Count` = 2

### CT-003: Tentativa Sem Permissão

**Pré-condições**:
- Usuário autenticado SEM permissão `cadastros:cargo:read`

**Dados de Entrada**:
- Nenhum filtro

**Passos**:
1. Fazer requisição GET para `/api/v1/cadastros/cargos`
2. Aguardar resposta

**Resultado Esperado**:
- Status: 403 Forbidden
- Body contém mensagem de erro clara
- Operação registrada na auditoria como "acesso negado"
- Frontend exibe mensagem amigável

### CT-004: Verificar Isolamento Multi-tenant

**Pré-condições**:
- Usuário A autenticado (Id_Conglomerado = 1)
- Existem 10 cargos no conglomerado 1
- Existem 15 cargos no conglomerado 2

**Dados de Entrada**:
- Nenhum filtro

**Passos**:
1. Fazer requisição GET para `/api/v1/cadastros/cargos` como Usuário A
2. Aguardar resposta
3. Verificar todos os registros retornados

**Resultado Esperado**:
- Status: 200 OK
- Body contém apenas 10 cargos (do conglomerado 1)
- Nenhum cargo do conglomerado 2 é retornado
- Tentativa de manipular Id_Conglomerado na request é ignorada/bloqueada

---

## 9. Notas Técnicas

### 9.1. Endpoint da API

```
GET /api/v1/cadastros/cargos
```

### 9.2. Parâmetros de Query String

| Parâmetro | Tipo | Obrigatório | Descrição | Exemplo |
|-----------|------|-------------|-----------|---------|
| `pageNumber` | int | Não | Número da página (padrão: 1) | `pageNumber=2` |
| `pageSize` | int | Não | Registros por página (padrão: 20, max: 100) | `pageSize=50` |
| `nome` | string | Não | Filtro por nome (busca parcial) | `nome=Analista` |
| `codigo` | string | Não | Filtro por código (busca por prefixo) | `codigo=ANA` |
| `salarioMin` | decimal | Não | Salário base mínimo | `salarioMin=3000` |
| `salarioMax` | decimal | Não | Salário base máximo | `salarioMax=8000` |
| `cargoSuperiorId` | int | Não | ID do cargo superior | `cargoSuperiorId=5` |
| `somenteRaiz` | bool | Não | Apenas cargos sem superior | `somenteRaiz=true` |
| `orderBy` | string | Não | Campo para ordenação | `orderBy=nome` |
| `orderDir` | string | Não | Direção (asc/desc) | `orderDir=desc` |

### 9.3. Estrutura do Response

```json
{
  "data": [
    {
      "id": 1,
      "codigo": "ANALISTA_SISTEMAS_SENIOR",
      "nome": "Analista de Sistemas Sênior",
      "descricao": "Responsável por...",
      "salarioBaseMin": 8000.00,
      "salarioBaseMax": 12000.00,
      "cboCode": "2124-05",
      "cargoSuperior": {
        "id": 5,
        "codigo": "COORDENADOR_TI",
        "nome": "Coordenador de TI"
      },
      "totalConsumidores": 15,
      "totalCompetencias": 8,
      "totalBeneficios": 5,
      "dataCriacao": "2025-01-15T10:30:00Z",
      "dataAtualizacao": "2025-03-20T14:45:00Z"
    }
  ],
  "pageNumber": 1,
  "pageSize": 20,
  "totalRecords": 50,
  "totalPages": 3,
  "hasPreviousPage": false,
  "hasNextPage": true
}
```

### 9.4. Headers de Response

```
X-Total-Count: 50
X-Total-Pages: 3
X-Page-Number: 1
X-Page-Size: 20
Cache-Control: private, max-age=300
```

---

## 10. Histórico de Alterações

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 1.0 | 2025-01-10 | Equipe IControlIT | Versão inicial |
| 2.0 | 2025-11-04 | Equipe IControlIT | Adequação ao padrão de documentação |

---

**Revisado por**: Equipe de Arquitetura
**Aprovado por**: Product Owner
**Data de Aprovação**: 2025-11-04

---

# UC01 - Criar Cargo

**ID do Caso de Uso**: UC01
**Nome do Caso de Uso**: Criar Cargo
**Requisito Funcional**: RF-CAD-009
**Autor**: Equipe IControlIT
**Status**: Em Desenvolvimento

---

## Índice

1. [Informações Gerais](#1-informações-gerais)
2. [Fluxo Principal](#2-fluxo-principal)
3. [Fluxos Alternativos](#3-fluxos-alternativos)
4. [Fluxos de Exceção](#4-fluxos-de-exceção)
5. [Regras de Negócio](#5-regras-de-negócio)
6. [Especificação de Testes](#6-especificação-de-testes)
7. [Matriz de Permissões](#7-matriz-de-permissões)
8. [Casos de Teste Detalhados](#8-casos-de-teste-detalhados)

---

## 1. Informações Gerais

### 1.1. Descrição

Este caso de uso permite que usuários autorizados criem novos cargos no sistema IControlIT. O processo inclui preenchimento de informações obrigatórias e opcionais, validação de dados, verificação de unicidade de código, validação de hierarquia, associação de competências e benefícios, e registro completo da operação na auditoria. Todos os cargos criados são isolados por conglomerado (multi-tenancy).

### 1.2. Atores

- **Ator Principal**: Usuário Autenticado com permissão `cadastros:cargo:create`
- **Atores Secundários**:
  - Sistema de Validação (valida dados de entrada)
  - Sistema de Auditoria (registra criação)
  - Sistema de Notificações (notifica gestores quando configurado)
  - API Backend (.NET 10)

### 1.3. Pré-condições

| ID | Descrição |
|----|-----------|
| PRE-01 | Usuário deve estar autenticado no sistema |
| PRE-02 | Usuário deve possuir permissão `cadastros:cargo:create` |
| PRE-03 | Conexão com banco de dados deve estar disponível |
| PRE-04 | Id_Conglomerado do usuário deve estar definido no contexto da sessão |
| PRE-05 | Sistema de validação deve estar operacional |
| PRE-06 | Sistema de auditoria deve estar operacional |

### 1.4. Pós-condições

| ID | Descrição |
|----|-----------|
| POS-01 | Novo cargo é criado no banco de dados |
| POS-02 | Cargo é criado com Fl_Ativo = 1 (ativo) |
| POS-03 | Id_Conglomerado é automaticamente definido com o do usuário |
| POS-04 | Operação de criação é registrada no log de auditoria |
| POS-05 | Cache de listagem de cargos é invalidado |
| POS-06 | Notificação é enviada (se configurado) |
| POS-07 | Usuário é redirecionado para página de visualização do cargo criado |

### 1.5. Requisitos Não-Funcionais

| ID | Tipo | Descrição | Meta |
|----|------|-----------|------|
| RNF-01 | Performance | Tempo de resposta da criação | < 3 segundos |
| RNF-02 | Usabilidade | Interface intuitiva com validações em tempo real | Validação inline < 500ms |
| RNF-03 | Segurança | Validação rigorosa de dados | 100% dos inputs validados |
| RNF-04 | Auditoria | Registro completo da operação | 100% das criações auditadas |
| RNF-05 | Integridade | Garantia de unicidade de código | 0% duplicados |
| RNF-06 | Consistência | Transações ACID | Rollback em caso de erro |
| RNF-07 | Disponibilidade | Sistema disponível para criação | 99.5% uptime |

---

## 2. Fluxo Principal

**Trigger**: Usuário clica no botão "Novo Cargo" na página de listagem de cargos

| Passo | Ator | Descrição | Sistema |
|-------|------|-----------|---------|
| 1 | Usuário | Clica no botão "Novo Cargo" | Sistema valida permissão |
| 2 | Sistema | Valida permissão `cadastros:cargo:create` do usuário | Middleware de autorização |
| 3 | Sistema | Exibe formulário de criação vazio | Angular Form Component |
| 4 | Sistema | Carrega dados auxiliares: lista de cargos disponíveis para superior, competências, benefícios | API Calls |
| 5 | Usuário | Preenche campo "Código" (obrigatório, UPPER_SNAKE_CASE) | Input com máscara |
| 6 | Sistema | Valida formato do código em tempo real (regex) | Validação inline |
| 7 | Sistema | Verifica unicidade do código via API (debounce 500ms) | Async Validator |
| 8 | Usuário | Preenche campo "Nome" (obrigatório, 3-150 caracteres) | Input text |
| 9 | Usuário | Preenche campo "Descrição" (opcional, até 1000 caracteres) | Textarea |
| 10 | Usuário | Seleciona "Cargo Superior" (opcional) | Dropdown/Autocomplete |
| 11 | Sistema | Se cargo superior selecionado, valida que não cria ciclo hierárquico | Validação de hierarquia |
| 12 | Usuário | Preenche "Código CBO" (opcional, formato: 9999-99) | Input com máscara |
| 13 | Usuário | Preenche "Salário Base Mínimo" (obrigatório, > 0) | Input currency |
| 14 | Usuário | Preenche "Salário Base Máximo" (obrigatório, >= salário mínimo) | Input currency |
| 15 | Sistema | Valida que salário máximo >= salário mínimo | Validação inline |
| 16 | Usuário | Seleciona competências associadas (opcional, multi-seleção) | Multi-select dropdown |
| 17 | Usuário | Seleciona benefícios associados (opcional, multi-seleção) | Multi-select dropdown |
| 18 | Usuário | Preenche campos adicionais opcionais (observações, requisitos, etc) | Textarea |
| 19 | Usuário | Clica no botão "Salvar" | Submit form |
| 20 | Sistema | Valida todos os campos do formulário (client-side) | Angular Validators |
| 21 | Sistema | Exibe loader/spinner e desabilita botão "Salvar" | UI Feedback |
| 22 | Sistema | Envia requisição POST para API com dados do cargo | HTTP Request |
| 23 | Sistema | Valida permissão novamente (server-side) | Authorization Filter |
| 24 | Sistema | Valida todos os dados recebidos (server-side) | FluentValidation |
| 25 | Sistema | Verifica unicidade do código no banco (with lock) | Database Query |
| 26 | Sistema | Valida hierarquia se cargo superior informado | Recursive query |
| 27 | Sistema | Recupera Id_Conglomerado do contexto do usuário | TenantContext |
| 28 | Sistema | Inicia transação no banco de dados | BeginTransaction |
| 29 | Sistema | Cria registro na tabela Cargo | INSERT INTO Cargo |
| 30 | Sistema | Insere relacionamentos com competências | INSERT INTO Cargo_Competencia |
| 31 | Sistema | Insere relacionamentos com benefícios | INSERT INTO Cargo_Beneficio |
| 32 | Sistema | Define Fl_Ativo = 1, Dt_Cadastro = NOW() | Audit fields |
| 33 | Sistema | Registra operação na tabela de auditoria | INSERT INTO AuditLog |
| 34 | Sistema | Invalida cache de listagem de cargos | Cache.Remove |
| 35 | Sistema | Comita transação | COMMIT |
| 36 | Sistema | Envia notificação (se configurado) | Notification Service |
| 37 | Sistema | Retorna HTTP 201 Created com dados do cargo criado | JSON Response |
| 38 | Frontend | Exibe mensagem de sucesso: "Cargo criado com sucesso!" | Toast notification |
| 39 | Frontend | Redireciona para página de visualização do cargo | Navigation |
| 40 | Sistema | Registra métrica de sucesso | Application Insights |

---

## 3. Fluxos Alternativos

### FA01 - Copiar de Cargo Existente

**Trigger**: Usuário clica em "Copiar" na lista de cargos ou botão "Criar a partir de..." no formulário

| Passo | Descrição |
|-------|-----------|
| FA01.1 | Usuário seleciona "Copiar Cargo" e escolhe cargo origem |
| FA01.2 | Sistema carrega todos os dados do cargo origem EXCETO código |
| FA01.3 | Sistema preenche formulário com dados copiados |
| FA01.4 | Sistema adiciona sufixo "_COPIA" ao nome para diferenciação |
| FA01.5 | Sistema marca campos como "dados copiados" visualmente |
| FA01.6 | Usuário ajusta código (obrigatório, não pode ser igual ao original) |
| FA01.7 | Usuário ajusta outros campos conforme necessário |
| FA01.8 | Sistema retorna ao passo 19 do Fluxo Principal |

### FA02 - Salvar como Rascunho (Futuro)

**Trigger**: Usuário clica em "Salvar como Rascunho"

| Passo | Descrição |
|-------|-----------|
| FA02.1 | Usuário clica em "Salvar como Rascunho" |
| FA02.2 | Sistema valida apenas campos obrigatórios mínimos (código e nome) |
| FA02.3 | Sistema cria cargo com Fl_Ativo = 0 e Fl_Rascunho = 1 |
| FA02.4 | Sistema registra operação na auditoria |
| FA02.5 | Sistema exibe mensagem: "Rascunho salvo com sucesso" |
| FA02.6 | Usuário pode retornar depois para completar |

### FA03 - Cancelar Criação

**Trigger**: Usuário clica em "Cancelar" ou botão "Voltar"

| Passo | Descrição |
|-------|-----------|
| FA03.1 | Usuário clica em "Cancelar" |
| FA03.2 | Se há dados preenchidos, sistema exibe confirmação: "Deseja descartar alterações?" |
| FA03.3 | Se usuário confirma, sistema descarta dados |
| FA03.4 | Sistema redireciona para página de listagem |
| FA03.5 | Nenhum dado é salvo no banco |

### FA04 - Adicionar Nova Competência Durante Criação

**Trigger**: Usuário clica em "+" ao lado do campo de competências

| Passo | Descrição |
|-------|-----------|
| FA04.1 | Usuário clica no botão "Adicionar Nova Competência" |
| FA04.2 | Sistema abre modal de criação rápida de competência |
| FA04.3 | Usuário preenche dados da nova competência |
| FA04.4 | Sistema valida e cria competência |
| FA04.5 | Sistema fecha modal e atualiza lista de competências disponíveis |
| FA04.6 | Sistema seleciona automaticamente a competência recém-criada |
| FA04.7 | Usuário continua preenchimento do cargo |

### FA05 - Adicionar Novo Benefício Durante Criação

**Trigger**: Usuário clica em "+" ao lado do campo de benefícios

| Passo | Descrição |
|-------|-----------|
| FA05.1 | Usuário clica no botão "Adicionar Novo Benefício" |
| FA05.2 | Sistema abre modal de criação rápida de benefício |
| FA05.3 | Usuário preenche dados do novo benefício |
| FA05.4 | Sistema valida e cria benefício |
| FA05.5 | Sistema fecha modal e atualiza lista de benefícios disponíveis |
| FA05.6 | Sistema seleciona automaticamente o benefício recém-criado |
| FA05.7 | Usuário continua preenchimento do cargo |

### FA06 - Buscar Código CBO Online

**Trigger**: Usuário clica em "Buscar CBO" ao lado do campo

| Passo | Descrição |
|-------|-----------|
| FA06.1 | Usuário clica em "Buscar CBO Online" |
| FA06.2 | Sistema abre modal com busca integrada ao site do MTE/CBO |
| FA06.3 | Usuário busca e seleciona código CBO adequado |
| FA06.4 | Sistema preenche automaticamente código e descrição do CBO |
| FA06.5 | Sistema fecha modal |
| FA06.6 | Usuário continua preenchimento |

### FA07 - Visualizar Hierarquia Antes de Salvar

**Trigger**: Usuário clica em "Visualizar Hierarquia" após selecionar cargo superior

| Passo | Descrição |
|-------|-----------|
| FA07.1 | Usuário seleciona cargo superior |
| FA07.2 | Usuário clica em "Visualizar Hierarquia" |
| FA07.3 | Sistema exibe árvore hierárquica mostrando onde o novo cargo se posicionará |
| FA07.4 | Sistema destaca em cor diferente a posição do novo cargo |
| FA07.5 | Usuário fecha visualização |
| FA07.6 | Usuário continua preenchimento |

---

## 4. Fluxos de Exceção

### FE01 - Usuário Sem Permissão

**Trigger**: Usuário não possui permissão `cadastros:cargo:create`

| Passo | Descrição |
|-------|-----------|
| FE01.1 | Sistema detecta ausência de permissão no passo 2 |
| FE01.2 | Sistema retorna HTTP 403 Forbidden |
| FE01.3 | Sistema registra tentativa de acesso não autorizado na auditoria |
| FE01.4 | Frontend exibe mensagem: "Você não tem permissão para criar cargos" |
| FE01.5 | Frontend redireciona para listagem (somente leitura) |
| FE01.6 | Caso de uso é encerrado |

### FE02 - Código Já Existe

**Trigger**: Código informado já existe no conglomerado (violação de unicidade)

| Passo | Descrição |
|-------|-----------|
| FE02.1 | Sistema detecta código duplicado no passo 25 |
| FE02.2 | Sistema executa rollback da transação |
| FE02.3 | Sistema retorna HTTP 409 Conflict |
| FE02.4 | Sistema inclui mensagem específica: "Código 'XXX' já está em uso" |
| FE02.5 | Sistema registra tentativa na auditoria |
| FE02.6 | Frontend exibe erro no campo "Código" |
| FE02.7 | Frontend sugere códigos alternativos (código_2, codigo_v2, etc) |
| FE02.8 | Usuário corrige código e tenta salvar novamente |

### FE03 - Formato de Código Inválido

**Trigger**: Código não está em UPPER_SNAKE_CASE

| Passo | Descrição |
|-------|-----------|
| FE03.1 | Sistema detecta formato inválido na validação (passo 6 ou 24) |
| FE03.2 | Sistema retorna HTTP 400 Bad Request |
| FE03.3 | Sistema inclui mensagem: "Código deve estar em UPPER_SNAKE_CASE (ex: ANALISTA_SISTEMAS)" |
| FE03.4 | Frontend exibe erro inline no campo "Código" |
| FE03.5 | Frontend oferece botão "Corrigir Automaticamente" |
| FE03.6 | Se usuário clica, sistema converte código automaticamente |
| FE03.7 | Usuário revisa e salva novamente |

### FE04 - Faixa Salarial Inválida

**Trigger**: Salário máximo < salário mínimo

| Passo | Descrição |
|-------|-----------|
| FE04.1 | Sistema detecta inconsistência no passo 15 ou 24 |
| FE04.2 | Sistema retorna HTTP 400 Bad Request |
| FE04.3 | Sistema inclui mensagem: "Salário máximo deve ser maior ou igual ao salário mínimo" |
| FE04.4 | Frontend exibe erro nos campos de salário |
| FE04.5 | Frontend destaca ambos os campos em vermelho |
| FE04.6 | Usuário corrige valores e tenta salvar novamente |

### FE05 - Ciclo Hierárquico Detectado

**Trigger**: Seleção de cargo superior cria ciclo na hierarquia

| Passo | Descrição |
|-------|-----------|
| FE05.1 | Sistema detecta ciclo no passo 11 ou 26 |
| FE05.2 | Sistema retorna HTTP 400 Bad Request |
| FE05.3 | Sistema inclui mensagem: "Não é possível criar hierarquia circular" |
| FE05.4 | Sistema fornece detalhes do ciclo detectado |
| FE05.5 | Frontend exibe erro no campo "Cargo Superior" |
| FE05.6 | Frontend remove opção problemática da lista |
| FE05.7 | Usuário seleciona cargo superior válido |

### FE06 - Erro de Conexão com Banco de Dados

**Trigger**: Banco de dados está indisponível durante criação

| Passo | Descrição |
|-------|-----------|
| FE06.1 | Sistema tenta criar cargo e recebe exceção de conexão (passo 29) |
| FE06.2 | Sistema executa rollback automático da transação |
| FE06.3 | Sistema tenta reconectar (retry pattern - 3 tentativas) |
| FE06.4 | Se todas as tentativas falharem, retorna HTTP 503 Service Unavailable |
| FE06.5 | Sistema registra erro detalhado no log |
| FE06.6 | Frontend exibe mensagem: "Serviço temporariamente indisponível. Seus dados foram preservados. Tente novamente em alguns instantes." |
| FE06.7 | Frontend mantém dados preenchidos no formulário |
| FE06.8 | Sistema envia alerta para equipe de operações |

### FE07 - Timeout na Criação

**Trigger**: Operação demora mais que timeout configurado (30 segundos)

| Passo | Descrição |
|-------|-----------|
| FE07.1 | Sistema atinge timeout durante criação |
| FE07.2 | Sistema tenta verificar se cargo foi criado (query de verificação) |
| FE07.3 | Se cargo foi criado, retorna sucesso com warning |
| FE07.4 | Se cargo não foi criado, executa rollback |
| FE07.5 | Sistema retorna HTTP 504 Gateway Timeout |
| FE07.6 | Sistema registra evento detalhado no log |
| FE07.7 | Frontend exibe mensagem: "Operação demorou muito. Verificando status..." |
| FE07.8 | Frontend faz polling para verificar se cargo foi criado |

### FE08 - Erro de Validação de Campos Obrigatórios

**Trigger**: Usuário tenta salvar sem preencher campos obrigatórios

| Passo | Descrição |
|-------|-----------|
| FE08.1 | Sistema detecta campos obrigatórios vazios no passo 20 ou 24 |
| FE08.2 | Sistema retorna HTTP 400 Bad Request (se server-side) |
| FE08.3 | Sistema lista todos os campos obrigatórios não preenchidos |
| FE08.4 | Frontend exibe erro em cada campo obrigatório vazio |
| FE08.5 | Frontend scrolls automaticamente para primeiro erro |
| FE08.6 | Frontend exibe resumo: "Preencha 3 campos obrigatórios" |
| FE08.7 | Usuário preenche campos e tenta salvar novamente |

### FE09 - Erro ao Criar Relacionamentos

**Trigger**: Erro ao inserir competências ou benefícios associados

| Passo | Descrição |
|-------|-----------|
| FE09.1 | Cargo é criado com sucesso (passo 29) |
| FE09.2 | Erro ocorre ao inserir relacionamentos (passo 30 ou 31) |
| FE09.3 | Sistema executa rollback de toda a transação |
| FE09.4 | Cargo não é criado (mantém integridade) |
| FE09.5 | Sistema retorna HTTP 500 Internal Server Error |
| FE09.6 | Sistema registra stack trace completo |
| FE09.7 | Frontend exibe mensagem: "Erro ao processar relacionamentos. Tente novamente." |
| FE09.8 | Frontend mantém dados preenchidos |

### FE10 - Dados Inválidos em Campos Adicionais

**Trigger**: Validação falha em campos opcionais (ex: CBO com formato errado)

| Passo | Descrição |
|-------|-----------|
| FE10.1 | Sistema detecta formato inválido em campo opcional |
| FE10.2 | Sistema retorna HTTP 400 Bad Request |
| FE10.3 | Sistema especifica qual campo e qual problema |
| FE10.4 | Frontend exibe erro no campo específico |
| FE10.5 | Frontend oferece exemplos de formato correto |
| FE10.6 | Usuário corrige e tenta salvar novamente |

---

## 5. Regras de Negócio

### RN-CAD-009-01: Código Único por Conglomerado

**Descrição**: O código do cargo deve ser único dentro do conglomerado. Não pode haver dois cargos com o mesmo código no mesmo conglomerado, mesmo que um esteja inativo.

**Criticidade**: CRÍTICA

**Implementação**:
- Validação assíncrona no frontend (debounce 500ms)
- Validação server-side antes de INSERT
- Unique constraint no banco: (Id_Conglomerado, Cd_Cargo)
- Lock otimista durante validação

**Teste**:
- Tentar criar cargo com código existente
- Verificar que erro é retornado antes de INSERT
- Verificar que mensagem é clara e sugere alternativas

### RN-CAD-009-02: Formato de Código (UPPER_SNAKE_CASE)

**Descrição**: O código deve estar no formato UPPER_SNAKE_CASE: letras maiúsculas, números e underscores, sem espaços ou caracteres especiais. Exemplos válidos: ANALISTA_SISTEMAS, GERENTE_TI_SENIOR, DEV_BACKEND_PL.

**Criticidade**: ALTA

**Implementação**:
- Regex: `^[A-Z0-9]+(_[A-Z0-9]+)*$`
- Validação inline no frontend
- Validação server-side com FluentValidation
- Opção de conversão automática

**Teste**:
- Tentar criar com "analista sistemas" (inválido)
- Tentar criar com "Analista-Sistemas" (inválido)
- Verificar que "ANALISTA_SISTEMAS" é aceito

### RN-CAD-009-03: Faixa Salarial Válida

**Descrição**: O salário base máximo deve ser maior ou igual ao salário base mínimo. Ambos devem ser valores positivos maiores que zero.

**Criticidade**: ALTA

**Implementação**:
- Validação inline quando usuário preenche/altera qualquer campo de salário
- Validação server-side: Vl_Salario_Base_Max >= Vl_Salario_Base_Min
- Validação: Vl_Salario_Base_Min > 0 AND Vl_Salario_Base_Max > 0

**Teste**:
- Tentar criar com max < min
- Tentar criar com valores negativos ou zero
- Verificar que faixa válida é aceita

### RN-CAD-009-04: Não Criar Ciclo Hierárquico

**Descrição**: Ao definir cargo superior, o sistema deve garantir que não será criado um ciclo na hierarquia (A -> B -> C -> A).

**Criticidade**: CRÍTICA

**Implementação**:
- Validação recursiva: percorrer hierarquia do cargo superior até raiz
- Query: WITH RECURSIVE para verificar ciclo
- Bloquear seleção de cargo que criaria ciclo

**Teste**:
- Criar cargo A com superior B
- Tentar editar B para ter superior A (deve falhar)
- Verificar que hierarquias válidas são aceitas

### RN-CAD-009-05: Isolamento Multi-tenant

**Descrição**: O cargo criado deve pertencer ao conglomerado do usuário autenticado. Não é permitido criar cargo para outro conglomerado.

**Criticidade**: CRÍTICA

**Implementação**:
- Id_Conglomerado obtido do TenantContext (token JWT)
- Campo não enviável pelo frontend
- Definido automaticamente no backend
- Validação: usuário não pode manipular Id_Conglomerado

**Teste**:
- Tentar enviar Id_Conglomerado diferente no payload
- Verificar que valor é ignorado e substituído pelo do usuário
- Verificar que cargo é criado no conglomerado correto

### RN-CAD-009-06: Campos Obrigatórios

**Descrição**: Os seguintes campos são obrigatórios:
- Código (Cd_Cargo)
- Nome (Nm_Cargo)
- Salário Base Mínimo (Vl_Salario_Base_Min)
- Salário Base Máximo (Vl_Salario_Base_Max)

**Criticidade**: ALTA

**Implementação**:
- Validação client-side: required validator
- Validação server-side: NotEmpty validator
- UI: campos marcados com asterisco (*)

**Teste**:
- Tentar criar cargo sem código (deve falhar)
- Tentar criar cargo sem nome (deve falhar)
- Tentar criar cargo sem salários (deve falhar)

### RN-CAD-009-07: Limites de Caracteres

**Descrição**:
- Código: 3-100 caracteres
- Nome: 3-150 caracteres
- Descrição: 0-1000 caracteres
- Código CBO: exatamente formato 9999-99 (7 caracteres) se preenchido
- Observações: 0-2000 caracteres

**Criticidade**: MÉDIA

**Implementação**:
- Validação client-side: minlength, maxlength
- Validação server-side: Length(min, max)
- UI: contador de caracteres em campos longos

**Teste**:
- Tentar criar com código de 2 caracteres (falha)
- Tentar criar com nome de 151 caracteres (falha)
- Verificar que limites corretos são aceitos

### RN-CAD-009-08: Cargo Superior Válido

**Descrição**: Se cargo superior for informado, deve ser um cargo ativo do mesmo conglomerado.

**Criticidade**: ALTA

**Implementação**:
- Dropdown carrega apenas cargos ativos do conglomerado
- Validação server-side:
  - EXISTS (SELECT 1 FROM Cargo WHERE Id = @IdCargoSuperior AND Id_Conglomerado = @IdConglomerado AND Fl_Ativo = 1)

**Teste**:
- Tentar definir cargo inativo como superior (deve falhar)
- Tentar definir cargo de outro conglomerado (deve falhar)
- Verificar que cargo válido é aceito

### RN-CAD-009-09: Código CBO Válido

**Descrição**: Se código CBO for informado, deve estar no formato 9999-99 (4 dígitos, hífen, 2 dígitos). É um campo opcional.

**Criticidade**: BAIXA

**Implementação**:
- Regex: `^\d{4}-\d{2}$`
- Validação apenas se campo preenchido
- Máscara no input: ____-__

**Teste**:
- Criar cargo sem CBO (deve funcionar)
- Criar cargo com CBO "2124-05" (deve funcionar)
- Tentar criar com CBO "123" (deve falhar)

### RN-CAD-009-10: Auditoria Completa

**Descrição**: Toda criação de cargo deve ser registrada na auditoria com: usuário responsável, data/hora, todos os dados criados, IP origem.

**Criticidade**: ALTA

**Implementação**:
- AuditLog.Create() chamado após INSERT bem-sucedido
- Payload completo serializado em JSON
- Registro inclui: Id_Usuario, Dt_Operacao, Tipo_Operacao="CREATE", Entidade="Cargo", Id_Registro, Dados_Anteriores=null, Dados_Novos=JSON

**Teste**:
- Criar cargo e verificar registro na auditoria
- Verificar que todos os dados estão presentes
- Verificar que usuário e timestamp estão corretos

### RN-CAD-009-11: Invalidação de Cache

**Descrição**: Após criação de cargo, o cache de listagem deve ser invalidado para garantir que novo cargo apareça imediatamente.

**Criticidade**: MÉDIA

**Implementação**:
- Cache.Remove("cargo_list_" + Id_Conglomerado + "*")
- Invalidação de todas as variações de cache (diferentes filtros/ordenações)

**Teste**:
- Criar cargo
- Listar cargos imediatamente
- Verificar que novo cargo aparece na lista

### RN-CAD-009-12: Transação Atômica

**Descrição**: A criação do cargo e todos os relacionamentos (competências, benefícios) devem ocorrer em uma única transação. Se qualquer parte falhar, toda operação deve ser revertida.

**Criticidade**: CRÍTICA

**Implementação**:
- using (var transaction = db.BeginTransaction())
- Rollback automático em caso de exceção
- Commit apenas se todas as operações forem bem-sucedidas

**Teste**:
- Simular erro ao inserir relacionamento
- Verificar que cargo não foi criado (rollback completo)

---

## 6. Especificação de Testes

### 6.1. Cenários de Teste Backend

| ID | Cenário | Tipo | Prioridade |
|----|---------|------|------------|
| CN-UC01-001 | Criar cargo com sucesso com todos os campos obrigatórios | Positivo | Alta |
| CN-UC01-002 | Criar cargo com sucesso incluindo campos opcionais | Positivo | Alta |
| CN-UC01-003 | Criar cargo com competências e benefícios associados | Positivo | Alta |
| CN-UC01-004 | Tentar criar cargo com código duplicado | Negativo | Alta |
| CN-UC01-005 | Tentar criar cargo com código em formato inválido | Negativo | Alta |
| CN-UC01-006 | Tentar criar cargo com faixa salarial inválida (max < min) | Negativo | Alta |
| CN-UC01-007 | Tentar criar cargo sem permissão | Negativo | Alta |
| CN-UC01-008 | Tentar criar cargo que criaria ciclo hierárquico | Negativo | Crítica |
| CN-UC01-009 | Tentar criar cargo sem campos obrigatórios | Negativo | Alta |
| CN-UC01-010 | Criar cargo e verificar auditoria | Auditoria | Alta |
| CN-UC01-011 | Criar cargo e verificar invalidação de cache | Performance | Média |
| CN-UC01-012 | Criar cargo e verificar isolamento multi-tenant | Segurança | Crítica |

### 6.2. Casos de Teste Sistema (E2E)

| ID | Caso de Teste | Tipo | Prioridade |
|----|---------------|------|------------|
| TC-UC01-001 | Preencher formulário e criar cargo com sucesso | Funcional | Alta |
| TC-UC01-002 | Validações inline de campos (código, salários) | Funcional | Alta |
| TC-UC01-003 | Validação assíncrona de código duplicado | Funcional | Alta |
| TC-UC01-004 | Criar cargo com cargo superior | Funcional | Média |
| TC-UC01-005 | Adicionar competências e benefícios | Funcional | Média |
| TC-UC01-006 | Cancelar criação com dados preenchidos | Funcional | Média |
| TC-UC01-007 | Copiar cargo existente | Funcional | Média |
| TC-UC01-008 | Verificar responsividade do formulário | UI/UX | Baixa |

### 6.3. Testes de Performance

| ID | Teste | Meta | Prioridade |
|----|-------|------|------------|
| PERF-UC01-001 | Tempo de resposta para criação simples | < 2s | Alta |
| PERF-UC01-002 | Tempo de resposta para criação com muitos relacionamentos | < 3s | Média |
| PERF-UC01-003 | Validação assíncrona de código | < 500ms | Média |

---

## 7. Matriz de Permissões

| Permissão | Descrição | Permite Criação | Permite Associar Competências | Permite Associar Benefícios |
|-----------|-----------|-----------------|------------------------------|----------------------------|
| `cadastros:cargo:create` | Criação básica de cargos | ✅ Sim | ✅ Sim | ✅ Sim |
| `cadastros:cargo:admin` | Administração completa | ✅ Sim | ✅ Sim | ✅ Sim |

**Herança de Permissões**:
- `cadastros:cargo:admin` inclui automaticamente `cadastros:cargo:create`

---

## 8. Casos de Teste Detalhados

### CT-001: Criar Cargo com Sucesso (Campos Obrigatórios)

**Pré-condições**:
- Usuário autenticado com permissão `cadastros:cargo:create`
- Código "ANALISTA_SISTEMAS_SENIOR" não existe no conglomerado

**Dados de Entrada**:
```json
{
  "codigo": "ANALISTA_SISTEMAS_SENIOR",
  "nome": "Analista de Sistemas Sênior",
  "salarioBaseMin": 8000.00,
  "salarioBaseMax": 12000.00
}
```

**Passos**:
1. Fazer requisição POST para `/api/v1/cadastros/cargos`
2. Aguardar resposta

**Resultado Esperado**:
- Status: 201 Created
- Header `Location` aponta para `/api/v1/cadastros/cargos/{id}`
- Body contém cargo criado com:
  - Id gerado
  - Fl_Ativo = 1
  - Dt_Cadastro = timestamp atual
  - Id_Conglomerado = conglomerado do usuário
- Registro na auditoria existe
- Cache invalidado
- Tempo de resposta < 2 segundos

### CT-002: Tentar Criar com Código Duplicado

**Pré-condições**:
- Usuário autenticado com permissão `cadastros:cargo:create`
- Código "GERENTE_TI" JÁ EXISTE no conglomerado

**Dados de Entrada**:
```json
{
  "codigo": "GERENTE_TI",
  "nome": "Gerente de TI Novo",
  "salarioBaseMin": 10000.00,
  "salarioBaseMax": 15000.00
}
```

**Passos**:
1. Fazer requisição POST para `/api/v1/cadastros/cargos`
2. Aguardar resposta

**Resultado Esperado**:
- Status: 409 Conflict
- Body contém mensagem: "Código 'GERENTE_TI' já está em uso"
- Body contém sugestões: ["GERENTE_TI_2", "GERENTE_TI_V2"]
- Nenhum registro é criado no banco
- Tentativa é registrada na auditoria
- Cache não é invalidado

### CT-003: Tentar Criar com Faixa Salarial Inválida

**Pré-condições**:
- Usuário autenticado com permissão `cadastros:cargo:create`

**Dados de Entrada**:
```json
{
  "codigo": "CARGO_TESTE",
  "nome": "Cargo Teste",
  "salarioBaseMin": 10000.00,
  "salarioBaseMax": 5000.00
}
```

**Passos**:
1. Fazer requisição POST para `/api/v1/cadastros/cargos`
2. Aguardar resposta

**Resultado Esperado**:
- Status: 400 Bad Request
- Body contém erro de validação específico:
  ```json
  {
    "errors": {
      "salarioBaseMax": ["Salário máximo deve ser maior ou igual ao salário mínimo"]
    }
  }
  ```
- Nenhum registro é criado

### CT-004: Criar Cargo com Hierarquia Válida

**Pré-condições**:
- Usuário autenticado com permissão `cadastros:cargo:create`
- Existe cargo "GERENTE_TI" (Id=5) no conglomerado

**Dados de Entrada**:
```json
{
  "codigo": "ANALISTA_TI_JUNIOR",
  "nome": "Analista de TI Júnior",
  "salarioBaseMin": 4000.00,
  "salarioBaseMax": 6000.00,
  "cargoSuperiorId": 5
}
```

**Passos**:
1. Fazer requisição POST para `/api/v1/cadastros/cargos`
2. Aguardar resposta
3. Fazer GET para buscar cargo criado

**Resultado Esperado**:
- Status: 201 Created
- Cargo criado com Id_Cargo_Superior = 5
- GET retorna cargo com dados de cargo superior incluídos:
  ```json
  {
    "cargoSuperior": {
      "id": 5,
      "codigo": "GERENTE_TI",
      "nome": "Gerente de TI"
    }
  }
  ```

### CT-005: Criar Cargo com Competências e Benefícios

**Pré-condições**:
- Usuário autenticado com permissão `cadastros:cargo:create`
- Existem competências: Id=1 ("Java"), Id=2 ("SQL")
- Existem benefícios: Id=1 ("Vale Refeição"), Id=2 ("Plano de Saúde")

**Dados de Entrada**:
```json
{
  "codigo": "DEV_FULLSTACK",
  "nome": "Desenvolvedor Full Stack",
  "salarioBaseMin": 7000.00,
  "salarioBaseMax": 11000.00,
  "competenciasIds": [1, 2],
  "beneficiosIds": [1, 2]
}
```

**Passos**:
1. Fazer requisição POST para `/api/v1/cadastros/cargos`
2. Aguardar resposta
3. Fazer GET para buscar cargo com relacionamentos

**Resultado Esperado**:
- Status: 201 Created
- Cargo criado com sucesso
- Relacionamentos criados nas tabelas:
  - Cargo_Competencia: 2 registros
  - Cargo_Beneficio: 2 registros
- GET retorna:
  ```json
  {
    "competencias": [
      {"id": 1, "nome": "Java"},
      {"id": 2, "nome": "SQL"}
    ],
    "beneficios": [
      {"id": 1, "nome": "Vale Refeição"},
      {"id": 2, "nome": "Plano de Saúde"}
    ]
  }
  ```

### CT-006: Tentar Criar Sem Permissão

**Pré-condições**:
- Usuário autenticado SEM permissão `cadastros:cargo:create`

**Dados de Entrada**:
```json
{
  "codigo": "CARGO_TESTE",
  "nome": "Cargo Teste",
  "salarioBaseMin": 3000.00,
  "salarioBaseMax": 5000.00
}
```

**Passos**:
1. Fazer requisição POST para `/api/v1/cadastros/cargos`
2. Aguardar resposta

**Resultado Esperado**:
- Status: 403 Forbidden
- Body contém mensagem: "Você não tem permissão para criar cargos"
- Nenhum registro é criado
- Tentativa é registrada na auditoria como "acesso negado"

### CT-007: Verificar Isolamento Multi-tenant

**Pré-condições**:
- Usuário A autenticado (Id_Conglomerado = 1)
- Usuário B autenticado (Id_Conglomerado = 2)

**Dados de Entrada** (Usuário A):
```json
{
  "codigo": "CARGO_CONGLOM_1",
  "nome": "Cargo Conglomerado 1",
  "salarioBaseMin": 3000.00,
  "salarioBaseMax": 5000.00,
  "idConglomerado": 2
}
```

**Passos**:
1. Fazer requisição POST como Usuário A tentando criar cargo no conglomerado 2
2. Aguardar resposta
3. Verificar conglomerado do cargo criado
4. Tentar buscar cargo como Usuário B

**Resultado Esperado**:
- Status: 201 Created (cargo é criado)
- Cargo é criado com Id_Conglomerado = 1 (do Usuário A, IGNORA o valor enviado)
- Usuário B não consegue visualizar o cargo (pertence ao conglomerado 1)
- Tentativa de manipular Id_Conglomerado é registrada na auditoria como suspeita

---

## 9. Notas Técnicas

### 9.1. Endpoint da API

```
POST /api/v1/cadastros/cargos
```

### 9.2. Estrutura do Request Body

```json
{
  "codigo": "string (required, 3-100 chars, UPPER_SNAKE_CASE)",
  "nome": "string (required, 3-150 chars)",
  "descricao": "string (optional, 0-1000 chars)",
  "cargoSuperiorId": "int (optional)",
  "cboCode": "string (optional, format: 9999-99)",
  "salarioBaseMin": "decimal (required, > 0)",
  "salarioBaseMax": "decimal (required, >= salarioBaseMin)",
  "competenciasIds": "int[] (optional)",
  "beneficiosIds": "int[] (optional)",
  "observacoes": "string (optional, 0-2000 chars)"
}
```

### 9.3. Estrutura do Response

**Sucesso (201 Created)**:
```json
{
  "id": 123,
  "codigo": "ANALISTA_SISTEMAS_SENIOR",
  "nome": "Analista de Sistemas Sênior",
  "descricao": "Responsável por...",
  "salarioBaseMin": 8000.00,
  "salarioBaseMax": 12000.00,
  "cboCode": "2124-05",
  "cargoSuperior": {
    "id": 5,
    "codigo": "COORDENADOR_TI",
    "nome": "Coordenador de TI"
  },
  "competencias": [
    {"id": 1, "nome": "Java", "nivel": "Avançado"}
  ],
  "beneficios": [
    {"id": 1, "nome": "Vale Refeição", "valor": 30.00}
  ],
  "idConglomerado": 1,
  "flAtivo": 1,
  "dataCriacao": "2025-11-04T10:30:00Z",
  "dataAtualizacao": "2025-11-04T10:30:00Z",
  "usuarioCriacao": {
    "id": 10,
    "nome": "João Silva"
  }
}
```

**Erro (400 Bad Request)**:
```json
{
  "type": "ValidationError",
  "title": "Erro de validação",
  "status": 400,
  "errors": {
    "codigo": ["Código já está em uso"],
    "salarioBaseMax": ["Deve ser maior ou igual ao salário mínimo"]
  },
  "traceId": "00-abc123-def456-01"
}
```

### 9.4. Headers de Response

**Sucesso**:
```
Location: /api/v1/cadastros/cargos/123
Content-Type: application/json
```

---

## 10. Histórico de Alterações

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 1.0 | 2025-01-10 | Equipe IControlIT | Versão inicial |
| 2.0 | 2025-11-04 | Equipe IControlIT | Adequação ao padrão de documentação completo |

---

**Revisado por**: Equipe de Arquitetura
**Aprovado por**: Product Owner
**Data de Aprovação**: 2025-11-04

---

# UC02 - Visualizar Cargo

**ID do Caso de Uso**: UC02
**Nome do Caso de Uso**: Visualizar Cargo
**Requisito Funcional**: RF-CAD-009
**Autor**: Equipe IControlIT
**Status**: Em Desenvolvimento

---

## Índice

1. [Informações Gerais](#1-informações-gerais)
2. [Fluxo Principal](#2-fluxo-principal)
3. [Fluxos Alternativos](#3-fluxos-alternativos)
4. [Fluxos de Exceção](#4-fluxos-de-exceção)
5. [Regras de Negócio](#5-regras-de-negócio)
6. [Especificação de Testes](#6-especificação-de-testes)
7. [Matriz de Permissões](#7-matriz-de-permissões)
8. [Casos de Teste Detalhados](#8-casos-de-teste-detalhados)

---

## 1. Informações Gerais

### 1.1. Descrição

Este caso de uso permite que usuários autorizados visualizem todos os detalhes de um cargo específico no sistema IControlIT. A visualização inclui informações completas: dados básicos, hierarquia (cargo superior e subordinados), competências associadas, benefícios, lista de consumidores que ocupam o cargo, histórico de alterações, e dados de auditoria. A visualização respeita o contexto multi-tenant (Id_Conglomerado).

### 1.2. Atores

- **Ator Principal**: Usuário Autenticado com permissão `cadastros:cargo:read`
- **Atores Secundários**:
  - Sistema de Auditoria (registra acesso)
  - Sistema de Cache (otimiza consultas)
  - API Backend (.NET 10)

### 1.3. Pré-condições

| ID | Descrição |
|----|-----------|
| PRE-01 | Usuário deve estar autenticado no sistema |
| PRE-02 | Usuário deve possuir permissão `cadastros:cargo:read` |
| PRE-03 | Cargo a ser visualizado deve existir |
| PRE-04 | Cargo deve pertencer ao conglomerado do usuário |
| PRE-05 | Conexão com banco de dados deve estar disponível |
| PRE-06 | Id do cargo deve ser válido (numérico inteiro positivo) |

### 1.4. Pós-condições

| ID | Descrição |
|----|-----------|
| POS-01 | Dados completos do cargo são exibidos |
| POS-02 | Acesso é registrado no log de auditoria |
| POS-03 | Dados são armazenados em cache para otimização |
| POS-04 | Botões de ação são habilitados conforme permissões do usuário |
| POS-05 | Histórico de alterações é carregado (se usuário tem permissão) |

### 1.5. Requisitos Não-Funcionais

| ID | Tipo | Descrição | Meta |
|----|------|-----------|------|
| RNF-01 | Performance | Tempo de resposta da visualização | < 1 segundo |
| RNF-02 | Usabilidade | Interface clara e organizada | Informações agrupadas por seções |
| RNF-03 | Segurança | Isolamento multi-tenant | 100% dos acessos validados |
| RNF-04 | Disponibilidade | Sistema disponível para consulta | 99.5% uptime |
| RNF-05 | Auditoria | Registro de todos os acessos | 100% das visualizações auditadas |
| RNF-06 | Cache | Utilização de cache | Cache de 5 minutos para dados detalhados |
| RNF-07 | Acessibilidade | Interface acessível (WCAG 2.1 AA) | Compatível com leitores de tela |

---

## 2. Fluxo Principal

**Trigger**: Usuário clica em um cargo na listagem ou acessa URL direta `/cadastros/cargos/{id}`

| Passo | Ator | Descrição | Sistema |
|-------|------|-----------|---------|
| 1 | Usuário | Clica em "Visualizar" ou no nome do cargo | Sistema captura ID do cargo |
| 2 | Sistema | Valida que ID é numérico inteiro positivo | Input validation |
| 3 | Sistema | Valida permissão `cadastros:cargo:read` do usuário | Middleware de autorização |
| 4 | Sistema | Recupera Id_Conglomerado do contexto do usuário | TenantContext |
| 5 | Sistema | Verifica existência de cache válido para o cargo | Redis/MemoryCache |
| 6 | Sistema | Se não há cache, executa query no banco de dados | EF Core + SQL Server |
| 7 | Sistema | Aplica filtro WHERE Id = @Id AND Id_Conglomerado = @IdConglomerado | Query SQL |
| 8 | Sistema | Verifica se cargo foi encontrado | Result validation |
| 9 | Sistema | Carrega dados relacionados via eager loading | Include() |
| 10 | Sistema | Carrega Cargo_Superior (se existir) | Navigation property |
| 11 | Sistema | Carrega lista de cargos subordinados | Reverse navigation |
| 12 | Sistema | Carrega competências associadas | Many-to-many |
| 13 | Sistema | Carrega benefícios associados | Many-to-many |
| 14 | Sistema | Conta total de consumidores ativos no cargo | Count query |
| 15 | Sistema | Se usuário tem permissão, carrega histórico de alterações | AuditLog query |
| 16 | Sistema | Formata resposta JSON com todos os dados | DTO Serialization |
| 17 | Sistema | Armazena resultado em cache por 5 minutos | Cache Set |
| 18 | Sistema | Registra acesso no log de auditoria | AuditLog.Create |
| 19 | Sistema | Retorna response com status 200 OK | HTTP Response |
| 20 | Frontend | Renderiza página de visualização | Angular Component |
| 21 | Frontend | Exibe dados básicos em seção principal | UI Rendering |
| 22 | Frontend | Exibe hierarquia (superior e subordinados) em árvore | Tree component |
| 23 | Frontend | Exibe competências em cards/badges | UI Components |
| 24 | Frontend | Exibe benefícios em cards/badges | UI Components |
| 25 | Frontend | Exibe estatísticas (total de consumidores) | Stats cards |
| 26 | Frontend | Habilita botões de ação conforme permissões | Button states |
| 27 | Frontend | Exibe abas: Detalhes, Hierarquia, Consumidores, Histórico | Tab navigation |
| 28 | Sistema | Monitora performance da operação | Application Insights |

---

## 3. Fluxos Alternativos

### FA01 - Visualizar Hierarquia Expandida

**Trigger**: Usuário clica na aba "Hierarquia"

| Passo | Descrição |
|-------|-----------|
| FA01.1 | Usuário clica na aba "Hierarquia" |
| FA01.2 | Sistema carrega árvore hierárquica completa |
| FA01.3 | Sistema destaca cargo atual na árvore |
| FA01.4 | Sistema exibe cargo superior (se existir) |
| FA01.5 | Sistema exibe todos os cargos subordinados diretos |
| FA01.6 | Sistema permite expansão/colapso de nós da árvore |
| FA01.7 | Sistema exibe links clicáveis para navegar na hierarquia |

### FA02 - Visualizar Lista de Consumidores

**Trigger**: Usuário clica na aba "Consumidores" ou no card de estatísticas

| Passo | Descrição |
|-------|-----------|
| FA02.1 | Usuário clica na aba "Consumidores" |
| FA02.2 | Sistema carrega lista de consumidores com este cargo |
| FA02.3 | Sistema aplica paginação (20 por página) |
| FA02.4 | Sistema exibe: nome, matrícula, departamento, data admissão |
| FA02.5 | Sistema permite busca e filtros na lista |
| FA02.6 | Sistema permite ordenação por colunas |
| FA02.7 | Usuário pode clicar em consumidor para ver detalhes |

### FA03 - Visualizar Histórico de Alterações

**Trigger**: Usuário com permissão clica na aba "Histórico"

| Passo | Descrição |
|-------|-----------|
| FA03.1 | Sistema valida permissão `cadastros:cargo:audit` |
| FA03.2 | Sistema carrega histórico da auditoria |
| FA03.3 | Sistema exibe timeline com todas as alterações |
| FA03.4 | Para cada alteração, sistema exibe: data/hora, usuário, campos alterados |
| FA03.5 | Sistema permite expandir para ver detalhes (valores antes/depois) |
| FA03.6 | Sistema destaca criação do cargo no início da timeline |
| FA03.7 | Sistema permite filtrar histórico por tipo de operação |

### FA04 - Editar Cargo

**Trigger**: Usuário com permissão clica em "Editar"

| Passo | Descrição |
|-------|-----------|
| FA04.1 | Usuário clica no botão "Editar" |
| FA04.2 | Sistema valida permissão `cadastros:cargo:update` |
| FA04.3 | Sistema redireciona para página de edição |
| FA04.4 | Sistema pré-preenche formulário com dados atuais |
| FA04.5 | Usuário segue UC03 (Editar Cargo) |

### FA05 - Inativar Cargo

**Trigger**: Usuário com permissão clica em "Inativar"

| Passo | Descrição |
|-------|-----------|
| FA05.1 | Usuário clica no botão "Inativar" |
| FA05.2 | Sistema valida permissão `cadastros:cargo:delete` |
| FA05.3 | Sistema exibe confirmação com avisos |
| FA05.4 | Sistema verifica se há consumidores ativos |
| FA05.5 | Se houver consumidores, sistema bloqueia e exibe mensagem |
| FA05.6 | Se não houver consumidores, usuário confirma |
| FA05.7 | Sistema segue UC04 (Inativar Cargo) |

### FA06 - Exportar Detalhes para PDF

**Trigger**: Usuário clica em "Exportar PDF"

| Passo | Descrição |
|-------|-----------|
| FA06.1 | Usuário clica no botão "Exportar" > "PDF" |
| FA06.2 | Sistema valida permissão `cadastros:cargo:export` |
| FA06.3 | Sistema gera PDF com todos os detalhes visíveis |
| FA06.4 | Sistema inclui logo, cabeçalho, data de geração |
| FA06.5 | Sistema registra exportação na auditoria |
| FA06.6 | Sistema retorna PDF para download |
| FA06.7 | Frontend inicia download automático |

### FA07 - Copiar para Novo Cargo

**Trigger**: Usuário com permissão clica em "Copiar"

| Passo | Descrição |
|-------|-----------|
| FA07.1 | Usuário clica no botão "Copiar" |
| FA07.2 | Sistema valida permissão `cadastros:cargo:create` |
| FA07.3 | Sistema redireciona para formulário de criação |
| FA07.4 | Sistema pré-preenche formulário com dados do cargo atual (exceto código) |
| FA07.5 | Usuário segue UC01 (Criar Cargo) ajustando dados |

### FA08 - Visualizar Competências Detalhadas

**Trigger**: Usuário clica em uma competência específica

| Passo | Descrição |
|-------|-----------|
| FA08.1 | Usuário clica em card/badge de competência |
| FA08.2 | Sistema abre modal com detalhes da competência |
| FA08.3 | Sistema exibe: nome, descrição, nível requerido, categoria |
| FA08.4 | Sistema lista outros cargos que requerem esta competência |
| FA08.5 | Usuário fecha modal e continua visualização |

### FA09 - Visualizar Benefícios Detalhados

**Trigger**: Usuário clica em um benefício específico

| Passo | Descrição |
|-------|-----------|
| FA09.1 | Usuário clica em card/badge de benefício |
| FA09.2 | Sistema abre modal com detalhes do benefício |
| FA09.3 | Sistema exibe: nome, descrição, valor/tipo, fornecedor |
| FA09.4 | Sistema lista outros cargos que têm este benefício |
| FA09.5 | Usuário fecha modal e continua visualização |

### FA10 - Navegar para Cargo Superior

**Trigger**: Usuário clica no link do cargo superior

| Passo | Descrição |
|-------|-----------|
| FA10.1 | Usuário clica no nome/link do cargo superior |
| FA10.2 | Sistema valida permissão de leitura |
| FA10.3 | Sistema carrega visualização do cargo superior |
| FA10.4 | Sistema mantém histórico de navegação (breadcrumb) |
| FA10.5 | Usuário pode voltar usando breadcrumb ou botão "Voltar" |

### FA11 - Navegar para Cargo Subordinado

**Trigger**: Usuário clica em cargo subordinado na árvore

| Passo | Descrição |
|-------|-----------|
| FA11.1 | Usuário clica em cargo subordinado |
| FA11.2 | Sistema valida permissão de leitura |
| FA11.3 | Sistema carrega visualização do cargo subordinado |
| FA11.4 | Sistema atualiza breadcrumb com navegação |
| FA11.5 | Usuário pode navegar livremente pela hierarquia |

---

## 4. Fluxos de Exceção

### FE01 - Usuário Sem Permissão

**Trigger**: Usuário não possui permissão `cadastros:cargo:read`

| Passo | Descrição |
|-------|-----------|
| FE01.1 | Sistema detecta ausência de permissão no passo 3 |
| FE01.2 | Sistema retorna HTTP 403 Forbidden |
| FE01.3 | Sistema registra tentativa de acesso não autorizado na auditoria |
| FE01.4 | Frontend exibe mensagem: "Você não tem permissão para visualizar cargos" |
| FE01.5 | Frontend redireciona para dashboard |
| FE01.6 | Caso de uso é encerrado |

### FE02 - Cargo Não Encontrado

**Trigger**: ID fornecido não corresponde a nenhum cargo

| Passo | Descrição |
|-------|-----------|
| FE02.1 | Sistema executa query e não encontra registro (passo 8) |
| FE02.2 | Sistema retorna HTTP 404 Not Found |
| FE02.3 | Sistema registra tentativa de acesso na auditoria |
| FE02.4 | Frontend exibe mensagem: "Cargo não encontrado" |
| FE02.5 | Frontend oferece botões: "Voltar" ou "Ver todos os cargos" |
| FE02.6 | Caso de uso é encerrado |

### FE03 - ID Inválido

**Trigger**: ID fornecido não é numérico inteiro válido

| Passo | Descrição |
|-------|-----------|
| FE03.1 | Sistema detecta formato inválido no passo 2 |
| FE03.2 | Sistema retorna HTTP 400 Bad Request |
| FE03.3 | Sistema inclui mensagem: "ID de cargo inválido" |
| FE03.4 | Frontend exibe mensagem de erro |
| FE03.5 | Frontend redireciona para listagem |
| FE03.6 | Caso de uso é encerrado |

### FE04 - Cargo de Outro Conglomerado

**Trigger**: Usuário tenta acessar cargo que não pertence ao seu conglomerado

| Passo | Descrição |
|-------|-----------|
| FE04.1 | Sistema executa query com filtro de Id_Conglomerado (passo 7) |
| FE04.2 | Query não retorna resultado (cargo existe mas é de outro conglomerado) |
| FE04.3 | Sistema trata como "não encontrado" (HTTP 404) |
| FE04.4 | Sistema registra tentativa suspeita na auditoria com flag de segurança |
| FE04.5 | Sistema envia alerta para equipe de segurança (tentativa de acesso cross-tenant) |
| FE04.6 | Frontend exibe mensagem genérica: "Cargo não encontrado" |
| FE04.7 | Caso de uso é encerrado |

### FE05 - Erro de Conexão com Banco de Dados

**Trigger**: Banco de dados está indisponível

| Passo | Descrição |
|-------|-----------|
| FE05.1 | Sistema tenta executar query e recebe exceção de conexão |
| FE05.2 | Sistema tenta reconectar (retry pattern - 3 tentativas) |
| FE05.3 | Se todas as tentativas falharem, retorna HTTP 503 Service Unavailable |
| FE05.4 | Sistema registra erro detalhado no log |
| FE05.5 | Frontend exibe mensagem: "Serviço temporariamente indisponível. Tente novamente em alguns instantes." |
| FE05.6 | Frontend oferece botão "Tentar Novamente" |
| FE05.7 | Sistema envia alerta para equipe de operações |

### FE06 - Erro no Sistema de Cache

**Trigger**: Redis ou cache distribuído está indisponível

| Passo | Descrição |
|-------|-----------|
| FE06.1 | Sistema tenta acessar cache e recebe exceção |
| FE06.2 | Sistema registra warning no log |
| FE06.3 | Sistema continua operação consultando diretamente o banco (fallback) |
| FE06.4 | Sistema retorna ao passo 6 do Fluxo Principal |
| FE06.5 | Sistema não interrompe a operação do usuário |
| FE06.6 | Performance pode ser levemente degradada mas funcionalidade mantida |

### FE07 - Timeout na Consulta

**Trigger**: Query demora mais que timeout configurado (10 segundos)

| Passo | Descrição |
|-------|-----------|
| FE07.1 | Sistema executa query e atinge timeout |
| FE07.2 | Sistema cancela operação e libera recursos |
| FE07.3 | Sistema retorna HTTP 504 Gateway Timeout |
| FE07.4 | Sistema registra erro com detalhes da query |
| FE07.5 | Frontend exibe mensagem: "A consulta demorou muito. Tente novamente." |
| FE07.6 | Sistema envia alerta para DBA avaliar performance |
| FE07.7 | Caso de uso é encerrado |

### FE08 - Erro ao Carregar Relacionamentos

**Trigger**: Erro ao carregar dados relacionados (competências, benefícios, etc)

| Passo | Descrição |
|-------|-----------|
| FE08.1 | Dados básicos são carregados com sucesso |
| FE08.2 | Erro ocorre ao carregar relacionamentos (passos 10-15) |
| FE08.3 | Sistema registra erro no log |
| FE08.4 | Sistema retorna dados básicos com indicação de erro parcial |
| FE08.5 | Frontend exibe cargo com dados disponíveis |
| FE08.6 | Frontend exibe avisos nas seções com erro: "Dados não disponíveis no momento" |
| FE08.7 | Frontend oferece botão "Recarregar" em cada seção com erro |

### FE09 - Erro de Serialização JSON

**Trigger**: Erro ao serializar objetos para JSON

| Passo | Descrição |
|-------|-----------|
| FE09.1 | Sistema recupera dados do banco com sucesso |
| FE09.2 | Sistema tenta serializar para JSON e recebe exceção |
| FE09.3 | Sistema retorna HTTP 500 Internal Server Error |
| FE09.4 | Sistema registra stack trace completo no log |
| FE09.5 | Frontend exibe mensagem: "Erro ao processar dados. Contate o suporte." |
| FE09.6 | Caso de uso é encerrado |

### FE10 - Cargo Inativo

**Trigger**: Cargo está inativo (Fl_Ativo = 0) e usuário não tem permissão especial

| Passo | Descrição |
|-------|-----------|
| FE10.1 | Sistema detecta que cargo está inativo |
| FE10.2 | Sistema verifica se usuário tem permissão `cadastros:cargo:view_inactive` |
| FE10.3 | Se não tem permissão, trata como "não encontrado" (HTTP 404) |
| FE10.4 | Se tem permissão, carrega dados normalmente |
| FE10.5 | Frontend exibe banner de aviso: "Este cargo está inativo" |
| FE10.6 | Frontend desabilita botão "Inativar" e habilita "Reativar" |

---

## 5. Regras de Negócio

### RN-CAD-009-01: Isolamento Multi-tenant

**Descrição**: Usuário só pode visualizar cargos do seu próprio conglomerado.

**Criticidade**: CRÍTICA

**Implementação**:
- WHERE Id_Conglomerado = @IdConglomerado em todas as queries
- Tentativa de acessar cargo de outro conglomerado é tratada como 404
- Tentativas suspeitas são registradas e alertadas

**Teste**:
- Usuário do conglomerado A tenta acessar cargo do conglomerado B
- Verificar que 404 é retornado e alerta é gerado

### RN-CAD-009-02: Permissão de Leitura Obrigatória

**Descrição**: Usuário deve ter permissão `cadastros:cargo:read` para visualizar qualquer cargo.

**Criticidade**: ALTA

**Implementação**:
- Validação em middleware de autorização
- Verificação também no controller (defense in depth)

**Teste**:
- Usuário sem permissão tenta acessar
- Verificar que 403 é retornado

### RN-CAD-009-03: Cargos Inativos

**Descrição**: Cargos inativos só são visíveis para usuários com permissão especial `cadastros:cargo:view_inactive`.

**Criticidade**: MÉDIA

**Implementação**:
- Query padrão filtra Fl_Ativo = 1
- Usuários com permissão especial veem também inativos
- UI indica claramente quando cargo está inativo

**Teste**:
- Usuário comum tenta acessar cargo inativo (404)
- Usuário com permissão especial acessa com sucesso

### RN-CAD-009-04: Auditoria de Acesso

**Descrição**: Toda visualização de cargo deve ser registrada na auditoria.

**Criticidade**: MÉDIA

**Implementação**:
- Registro inclui: usuário, data/hora, ID do cargo, IP
- Não registra conteúdo completo (apenas metadados)
- Registro assíncrono para não impactar performance

**Teste**:
- Visualizar cargo e verificar registro na auditoria
- Verificar que dados estão corretos

### RN-CAD-009-05: Cache de Visualização

**Descrição**: Dados detalhados do cargo devem ser cacheados por 5 minutos para otimizar performance.

**Criticidade**: MÉDIA

**Implementação**:
- Cache key: "cargo_detail_" + Id + "_" + Id_Conglomerado
- TTL: 5 minutos
- Invalidação: ao editar ou inativar cargo

**Teste**:
- Primeira visualização consulta banco
- Segunda visualização em 1 minuto vem do cache (mais rápida)
- Após edição, cache é invalidado

### RN-CAD-009-06: Eager Loading de Relacionamentos

**Descrição**: Todos os relacionamentos devem ser carregados em uma única consulta para evitar problema N+1.

**Criticidade**: ALTA (Performance)

**Implementação**:
- .Include(c => c.CargoSuperior)
- .Include(c => c.CargosSubordinados)
- .Include(c => c.Competencias)
- .Include(c => c.Beneficios)

**Teste**:
- Verificar no log SQL que apenas 1 query é executada
- Medir performance (deve ser < 1 segundo)

### RN-CAD-009-07: Botões de Ação Baseados em Permissões

**Descrição**: Botões de ação (Editar, Inativar, Exportar) devem ser exibidos apenas se usuário tem a permissão correspondente.

**Criticidade**: MÉDIA

**Implementação**:
- Frontend verifica permissões do usuário (do token JWT)
- Backend valida novamente ao executar ação (não confia no frontend)

**Teste**:
- Usuário com read-only: vê apenas botões de visualização
- Usuário com update: vê também botão Editar
- Usuário com delete: vê também botão Inativar

### RN-CAD-009-08: Hierarquia Navegável

**Descrição**: Links para cargo superior e subordinados devem ser clicáveis e permitir navegação fluida pela hierarquia.

**Criticidade**: BAIXA

**Implementação**:
- Links usam routerLink do Angular
- Breadcrumb mantém histórico de navegação
- Validação de permissão ao navegar

**Teste**:
- Clicar em cargo superior e verificar navegação
- Verificar que breadcrumb está correto
- Voltar usando breadcrumb

### RN-CAD-009-09: Contagem de Consumidores

**Descrição**: Sistema deve exibir quantos consumidores ativos possuem este cargo atualmente.

**Criticidade**: MÉDIA

**Implementação**:
- Count query: SELECT COUNT(*) FROM Consumidor WHERE Id_Cargo = @Id AND Fl_Ativo = 1
- Resultado cacheado junto com dados do cargo

**Teste**:
- Criar cargo e verificar que contador = 0
- Atribuir cargo a 5 consumidores
- Verificar que contador = 5

### RN-CAD-009-10: Histórico Detalhado

**Descrição**: Usuários com permissão `cadastros:cargo:audit` podem ver histórico completo de alterações com valores antes/depois.

**Criticidade**: BAIXA

**Implementação**:
- Query na tabela AuditLog filtrando por Entidade='Cargo' e Id_Registro
- Ordenação DESC por data (mais recente primeiro)
- Deserialização de JSON com dados antes/depois

**Teste**:
- Criar cargo, editar 3 vezes, visualizar histórico
- Verificar que 4 registros aparecem (1 criação + 3 edições)
- Verificar que valores antes/depois estão corretos

---

## 6. Especificação de Testes

### 6.1. Cenários de Teste Backend

| ID | Cenário | Tipo | Prioridade |
|----|---------|------|------------|
| CN-UC02-001 | Visualizar cargo existente com sucesso | Positivo | Alta |
| CN-UC02-002 | Visualizar cargo com todos os relacionamentos | Positivo | Alta |
| CN-UC02-003 | Visualizar cargo e verificar cache | Performance | Média |
| CN-UC02-004 | Tentar visualizar cargo de outro conglomerado | Segurança | Crítica |
| CN-UC02-005 | Tentar visualizar cargo sem permissão | Negativo | Alta |
| CN-UC02-006 | Tentar visualizar cargo inexistente | Negativo | Alta |
| CN-UC02-007 | Visualizar cargo com ID inválido | Negativo | Média |
| CN-UC02-008 | Visualizar cargo inativo sem permissão especial | Negativo | Média |
| CN-UC02-009 | Visualizar cargo inativo com permissão especial | Positivo | Baixa |
| CN-UC02-010 | Verificar auditoria de acesso | Auditoria | Alta |

### 6.2. Casos de Teste Sistema (E2E)

| ID | Caso de Teste | Tipo | Prioridade |
|----|---------------|------|------------|
| TC-UC02-001 | Acessar página e visualizar dados básicos | Funcional | Alta |
| TC-UC02-002 | Navegar entre abas (Detalhes, Hierarquia, etc) | Funcional | Média |
| TC-UC02-003 | Clicar em cargo superior e navegar | Funcional | Média |
| TC-UC02-004 | Visualizar lista de consumidores | Funcional | Média |
| TC-UC02-005 | Visualizar histórico de alterações | Funcional | Baixa |
| TC-UC02-006 | Exportar detalhes para PDF | Funcional | Baixa |
| TC-UC02-007 | Verificar botões habilitados conforme permissões | Autorização | Alta |

### 6.3. Testes de Performance

| ID | Teste | Meta | Prioridade |
|----|-------|------|------------|
| PERF-UC02-001 | Tempo de carregamento inicial | < 1s | Alta |
| PERF-UC02-002 | Tempo de carregamento com cache | < 200ms | Média |
| PERF-UC02-003 | Carregamento de aba Consumidores | < 2s | Média |

---

## 7. Matriz de Permissões

| Permissão | Pode Visualizar | Vê Botão Editar | Vê Botão Inativar | Vê Histórico | Pode Exportar |
|-----------|----------------|----------------|-------------------|--------------|---------------|
| `cadastros:cargo:read` | ✅ Sim | ❌ Não | ❌ Não | ❌ Não | ❌ Não |
| `cadastros:cargo:update` | ✅ Sim | ✅ Sim | ❌ Não | ❌ Não | ❌ Não |
| `cadastros:cargo:delete` | ✅ Sim | ✅ Sim | ✅ Sim | ❌ Não | ❌ Não |
| `cadastros:cargo:audit` | ✅ Sim | ❌ Não | ❌ Não | ✅ Sim | ❌ Não |
| `cadastros:cargo:export` | ✅ Sim | ❌ Não | ❌ Não | ❌ Não | ✅ Sim |
| `cadastros:cargo:admin` | ✅ Sim | ✅ Sim | ✅ Sim | ✅ Sim | ✅ Sim |

---

## 8. Casos de Teste Detalhados

### CT-001: Visualizar Cargo com Sucesso

**Pré-condições**:
- Usuário autenticado com permissão `cadastros:cargo:read`
- Existe cargo com Id=10 no conglomerado do usuário

**Dados de Entrada**:
- ID do cargo: 10

**Passos**:
1. Fazer requisição GET para `/api/v1/cadastros/cargos/10`
2. Aguardar resposta

**Resultado Esperado**:
- Status: 200 OK
- Body contém dados completos do cargo
- Cargo tem todas as propriedades preenchidas
- Relacionamentos estão incluídos (competências, benefícios, superior)
- Header `ETag` presente para cache
- Tempo de resposta < 1 segundo
- Registro na auditoria criado

### CT-002: Tentar Visualizar Cargo de Outro Conglomerado

**Pré-condições**:
- Usuário A autenticado (Id_Conglomerado = 1)
- Existe cargo com Id=20 no conglomerado 2

**Dados de Entrada**:
- ID do cargo: 20

**Passos**:
1. Fazer requisição GET para `/api/v1/cadastros/cargos/20` como Usuário A
2. Aguardar resposta

**Resultado Esperado**:
- Status: 404 Not Found
- Body contém mensagem: "Cargo não encontrado"
- Tentativa é registrada na auditoria com flag de segurança
- Alerta é enviado para equipe de segurança
- Nenhum dado do cargo é retornado

### CT-003: Visualizar Cargo e Verificar Cache

**Pré-condições**:
- Usuário autenticado com permissão `cadastros:cargo:read`
- Existe cargo com Id=10
- Cache está vazio/invalidado

**Dados de Entrada**:
- ID do cargo: 10

**Passos**:
1. Fazer primeira requisição GET para `/api/v1/cadastros/cargos/10`
2. Medir tempo de resposta (T1)
3. Aguardar 10 segundos
4. Fazer segunda requisição GET para `/api/v1/cadastros/cargos/10`
5. Medir tempo de resposta (T2)

**Resultado Esperado**:
- Primeira requisição: T1 ≈ 800ms (consulta banco)
- Segunda requisição: T2 < 200ms (vem do cache)
- T2 deve ser significativamente menor que T1
- Dados retornados devem ser idênticos
- Ambas as requisições retornam Status 200

### CT-004: Visualizar Hierarquia Completa

**Pré-condições**:
- Usuário autenticado com permissão `cadastros:cargo:read`
- Existe hierarquia: DIRETOR_TI (Id=1) > GERENTE_DEV (Id=5) > ANALISTA_SENIOR (Id=10)
- Queremos visualizar GERENTE_DEV (Id=5)

**Dados de Entrada**:
- ID do cargo: 5

**Passos**:
1. Fazer requisição GET para `/api/v1/cadastros/cargos/5`
2. Verificar dados de hierarquia no response

**Resultado Esperado**:
- Status: 200 OK
- Campo `cargoSuperior` contém:
  ```json
  {
    "id": 1,
    "codigo": "DIRETOR_TI",
    "nome": "Diretor de TI"
  }
  ```
- Campo `cargosSubordinados` contém array com:
  ```json
  [
    {
      "id": 10,
      "codigo": "ANALISTA_SENIOR",
      "nome": "Analista Sênior"
    }
  ]
  ```

### CT-005: Tentar Visualizar Sem Permissão

**Pré-condições**:
- Usuário autenticado SEM permissão `cadastros:cargo:read`
- Existe cargo com Id=10

**Dados de Entrada**:
- ID do cargo: 10

**Passos**:
1. Fazer requisição GET para `/api/v1/cadastros/cargos/10`
2. Aguardar resposta

**Resultado Esperado**:
- Status: 403 Forbidden
- Body contém mensagem: "Você não tem permissão para visualizar cargos"
- Tentativa é registrada na auditoria como "acesso negado"
- Nenhum dado é retornado

### CT-006: Visualizar Cargo Inexistente

**Pré-condições**:
- Usuário autenticado com permissão `cadastros:cargo:read`
- NÃO existe cargo com Id=99999

**Dados de Entrada**:
- ID do cargo: 99999

**Passos**:
1. Fazer requisição GET para `/api/v1/cadastros/cargos/99999`
2. Aguardar resposta

**Resultado Esperado**:
- Status: 404 Not Found
- Body contém mensagem: "Cargo não encontrado"
- Tentativa é registrada na auditoria
- Nenhum erro de servidor ocorre

### CT-007: Visualizar com ID Inválido

**Pré-condições**:
- Usuário autenticado com permissão `cadastros:cargo:read`

**Dados de Entrada**:
- ID do cargo: "abc" (string não numérica)

**Passos**:
1. Fazer requisição GET para `/api/v1/cadastros/cargos/abc`
2. Aguardar resposta

**Resultado Esperado**:
- Status: 400 Bad Request
- Body contém mensagem: "ID de cargo inválido"
- Erro de validação é retornado
- Nenhum processamento adicional ocorre

---

## 9. Notas Técnicas

### 9.1. Endpoint da API

```
GET /api/v1/cadastros/cargos/{id}
```

### 9.2. Parâmetros

| Parâmetro | Tipo | Local | Obrigatório | Descrição |
|-----------|------|-------|-------------|-----------|
| `id` | int | Path | Sim | ID do cargo a visualizar |
| `includeInactive` | bool | Query | Não | Incluir dados mesmo se inativo (requer permissão) |

### 9.3. Estrutura do Response

```json
{
  "id": 10,
  "codigo": "ANALISTA_SISTEMAS_SENIOR",
  "nome": "Analista de Sistemas Sênior",
  "descricao": "Responsável por desenvolvimento e arquitetura de sistemas complexos",
  "salarioBaseMin": 8000.00,
  "salarioBaseMax": 12000.00,
  "cboCode": "2124-05",
  "cargoSuperior": {
    "id": 5,
    "codigo": "COORDENADOR_TI",
    "nome": "Coordenador de TI"
  },
  "cargosSubordinados": [
    {
      "id": 15,
      "codigo": "ANALISTA_SISTEMAS_PLENO",
      "nome": "Analista de Sistemas Pleno"
    },
    {
      "id": 20,
      "codigo": "ANALISTA_SISTEMAS_JUNIOR",
      "nome": "Analista de Sistemas Júnior"
    }
  ],
  "competencias": [
    {
      "id": 1,
      "nome": "Java",
      "nivel": "Avançado",
      "categoria": "Linguagem de Programação"
    },
    {
      "id": 2,
      "nome": "SQL",
      "nivel": "Avançado",
      "categoria": "Banco de Dados"
    }
  ],
  "beneficios": [
    {
      "id": 1,
      "nome": "Vale Refeição",
      "valor": 30.00,
      "tipo": "Alimentação"
    },
    {
      "id": 2,
      "nome": "Plano de Saúde",
      "tipo": "Saúde",
      "fornecedor": "Unimed"
    }
  ],
  "estatisticas": {
    "totalConsumidoresAtivos": 15,
    "totalConsumidoresInativos": 3,
    "totalSubordinados": 2
  },
  "idConglomerado": 1,
  "flAtivo": 1,
  "dataCriacao": "2025-01-15T10:30:00Z",
  "dataAtualizacao": "2025-03-20T14:45:00Z",
  "usuarioCriacao": {
    "id": 10,
    "nome": "João Silva"
  },
  "usuarioUltimaAlteracao": {
    "id": 12,
    "nome": "Maria Santos"
  }
}
```

### 9.4. Headers de Response

```
Content-Type: application/json
ETag: "abc123def456"
Cache-Control: private, max-age=300
Last-Modified: Wed, 20 Mar 2025 14:45:00 GMT
```

---

## 10. Histórico de Alterações

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 1.0 | 2025-01-10 | Equipe IControlIT | Versão inicial |
| 2.0 | 2025-11-04 | Equipe IControlIT | Adequação ao padrão de documentação completo |

---

**Revisado por**: Equipe de Arquitetura
**Aprovado por**: Product Owner
**Data de Aprovação**: 2025-11-04

---

# UC03 - Editar Cargo

**ID do Caso de Uso**: UC03
**Nome do Caso de Uso**: Editar Cargo
**Requisito Funcional**: RF-CAD-009
**Autor**: Equipe IControlIT
**Status**: Em Desenvolvimento

---

## Índice

1. [Informações Gerais](#1-informações-gerais)
2. [Fluxo Principal](#2-fluxo-principal)
3. [Fluxos Alternativos](#3-fluxos-alternativos)
4. [Fluxos de Exceção](#4-fluxos-de-exceção)
5. [Regras de Negócio](#5-regras-de-negócio)
6. [Especificação de Testes](#6-especificação-de-testes)
7. [Matriz de Permissões](#7-matriz-de-permissões)
8. [Casos de Teste Detalhados](#8-casos-de-teste-detalhados)

---

## 1. Informações Gerais

### 1.1. Descrição

Este caso de uso permite que usuários autorizados editem e atualizem informações de cargos existentes no sistema IControlIT. O processo inclui validação de permissões, verificação de unicidade de código (se alterado), validação de hierarquia, atualização de relacionamentos (competências e benefícios), controle de concorrência, e registro completo na auditoria com comparação antes/depois. Todos os cargos editados respeitam o contexto multi-tenant (Id_Conglomerado).

### 1.2. Atores

- **Ator Principal**: Usuário Autenticado com permissão `cadastros:cargo:update`
- **Atores Secundários**:
  - Sistema de Validação (valida dados de entrada)
  - Sistema de Auditoria (registra alterações)
  - Sistema de Controle de Concorrência (evita conflitos)
  - Sistema de Notificações (notifica gestores quando configurado)
  - API Backend (.NET 10)

### 1.3. Pré-condições

| ID | Descrição |
|----|-----------|
| PRE-01 | Usuário deve estar autenticado no sistema |
| PRE-02 | Usuário deve possuir permissão `cadastros:cargo:update` |
| PRE-03 | Cargo a ser editado deve existir e estar ativo |
| PRE-04 | Cargo deve pertencer ao conglomerado do usuário |
| PRE-05 | Conexão com banco de dados deve estar disponível |
| PRE-06 | Sistema de validação deve estar operacional |
| PRE-07 | Sistema de auditoria deve estar operacional |

### 1.4. Pós-condições

| ID | Descrição |
|----|-----------|
| POS-01 | Cargo é atualizado no banco de dados |
| POS-02 | Dt_Atualizacao é atualizada para timestamp atual |
| POS-03 | Id_Usuario_Atualizacao é definido como o usuário responsável |
| POS-04 | Operação de edição é registrada no log de auditoria com diff |
| POS-05 | Cache de listagem e visualização é invalidado |
| POS-06 | Notificação é enviada (se configurado) |
| POS-07 | Usuário visualiza dados atualizados na tela |
| POS-08 | Versão do registro é incrementada (controle otimista) |

### 1.5. Requisitos Não-Funcionais

| ID | Tipo | Descrição | Meta |
|----|------|-----------|------|
| RNF-01 | Performance | Tempo de resposta da edição | < 3 segundos |
| RNF-02 | Usabilidade | Validações em tempo real | Validação inline < 500ms |
| RNF-03 | Segurança | Validação rigorosa de dados | 100% dos inputs validados |
| RNF-04 | Auditoria | Registro completo com before/after | 100% das edições auditadas |
| RNF-05 | Integridade | Controle de concorrência otimista | 0% sobrescritas acidentais |
| RNF-06 | Consistência | Transações ACID | Rollback em caso de erro |
| RNF-07 | Disponibilidade | Sistema disponível para edição | 99.5% uptime |

---

## 2. Fluxo Principal

**Trigger**: Usuário clica no botão "Editar" na página de visualização do cargo

| Passo | Ator | Descrição | Sistema |
|-------|------|-----------|---------|
| 1 | Usuário | Clica no botão "Editar" na página de visualização | Sistema captura ID e RowVersion |
| 2 | Sistema | Valida permissão `cadastros:cargo:update` do usuário | Middleware de autorização |
| 3 | Sistema | Valida que cargo pertence ao conglomerado do usuário | TenantContext validation |
| 4 | Sistema | Carrega dados atuais do cargo | Database query |
| 5 | Sistema | Armazena snapshot dos dados originais (para auditoria) | In-memory storage |
| 6 | Sistema | Exibe formulário de edição pré-preenchido | Angular Form Component |
| 7 | Sistema | Carrega dados auxiliares: lista de cargos, competências, benefícios | API Calls |
| 8 | Usuário | Modifica campo "Nome" | Input text |
| 9 | Sistema | Valida formato em tempo real | Inline validation |
| 10 | Usuário | Modifica campo "Código" (se necessário) | Input com máscara |
| 11 | Sistema | Se código alterado, verifica unicidade via API (debounce 500ms) | Async Validator |
| 12 | Usuário | Ajusta "Salário Base Mínimo" e "Salário Base Máximo" | Input currency |
| 13 | Sistema | Valida que máximo >= mínimo em tempo real | Validação inline |
| 14 | Usuário | Altera "Cargo Superior" (se necessário) | Dropdown/Autocomplete |
| 15 | Sistema | Se cargo superior alterado, valida que não cria ciclo | Validação de hierarquia |
| 16 | Usuário | Atualiza competências associadas (adiciona/remove) | Multi-select |
| 17 | Usuário | Atualiza benefícios associados (adiciona/remove) | Multi-select |
| 18 | Usuário | Ajusta outros campos opcionais (descrição, observações, etc) | Textarea |
| 19 | Usuário | Clica no botão "Salvar" | Submit form |
| 20 | Sistema | Valida todos os campos do formulário (client-side) | Angular Validators |
| 21 | Sistema | Exibe loader/spinner e desabilita botão "Salvar" | UI Feedback |
| 22 | Sistema | Envia requisição PUT para API com dados + RowVersion | HTTP Request |
| 23 | Sistema | Valida permissão novamente (server-side) | Authorization Filter |
| 24 | Sistema | Valida todos os dados recebidos (server-side) | FluentValidation |
| 25 | Sistema | Verifica RowVersion para controle de concorrência | Optimistic locking |
| 26 | Sistema | Se código alterado, verifica unicidade no banco | Database Query |
| 27 | Sistema | Se cargo superior alterado, valida hierarquia | Recursive query |
| 28 | Sistema | Recupera Id_Conglomerado e valida isolamento | TenantContext |
| 29 | Sistema | Inicia transação no banco de dados | BeginTransaction |
| 30 | Sistema | Atualiza registro na tabela Cargo | UPDATE Cargo SET ... |
| 31 | Sistema | Remove relacionamentos antigos com competências | DELETE FROM Cargo_Competencia |
| 32 | Sistema | Insere novos relacionamentos com competências | INSERT INTO Cargo_Competencia |
| 33 | Sistema | Remove relacionamentos antigos com benefícios | DELETE FROM Cargo_Beneficio |
| 34 | Sistema | Insere novos relacionamentos com benefícios | INSERT INTO Cargo_Beneficio |
| 35 | Sistema | Define Dt_Atualizacao = NOW(), Id_Usuario_Atualizacao | Audit fields |
| 36 | Sistema | Incrementa RowVersion (controle de concorrência) | Versioning |
| 37 | Sistema | Calcula diff (diferenças entre antes e depois) | Data comparison |
| 38 | Sistema | Registra operação na tabela de auditoria com diff | INSERT INTO AuditLog |
| 39 | Sistema | Invalida cache de listagem e visualização | Cache.Remove |
| 40 | Sistema | Comita transação | COMMIT |
| 41 | Sistema | Envia notificação (se configurado) | Notification Service |
| 42 | Sistema | Retorna HTTP 200 OK com dados atualizados | JSON Response |
| 43 | Frontend | Exibe mensagem de sucesso: "Cargo atualizado com sucesso!" | Toast notification |
| 44 | Frontend | Atualiza visualização com dados mais recentes | Data refresh |
| 45 | Frontend | Muda modo de edição para visualização | UI State change |
| 46 | Sistema | Registra métrica de sucesso | Application Insights |

---

## 3. Fluxos Alternativos

### FA01 - Editar Apenas Nome e Descrição

**Trigger**: Usuário altera apenas campos textuais básicos

| Passo | Descrição |
|-------|-----------|
| FA01.1 | Usuário modifica apenas nome e descrição |
| FA01.2 | Sistema mantém todos os outros campos inalterados |
| FA01.3 | Sistema não recalcula relacionamentos (não foram alterados) |
| FA01.4 | Sistema atualiza apenas campos modificados |
| FA01.5 | Auditoria registra apenas alterações em nome e descrição |
| FA01.6 | Performance é otimizada (menos operações) |

### FA02 - Alterar Faixa Salarial

**Trigger**: Usuário ajusta salários base mínimo e/ou máximo

| Passo | Descrição |
|-------|-----------|
| FA02.1 | Usuário altera salário base mínimo de R$ 5.000 para R$ 6.000 |
| FA02.2 | Sistema valida que novo valor > 0 |
| FA02.3 | Usuário altera salário base máximo de R$ 8.000 para R$ 10.000 |
| FA02.4 | Sistema valida que máximo >= mínimo (R$ 10.000 >= R$ 6.000) ✅ |
| FA02.5 | Sistema permite salvar |
| FA02.6 | Sistema registra alteração salarial na auditoria |
| FA02.7 | Sistema pode disparar notificação para RH (se configurado) |

### FA03 - Alterar Cargo Superior

**Trigger**: Usuário muda posição do cargo na hierarquia

| Passo | Descrição |
|-------|-----------|
| FA03.1 | Usuário seleciona novo cargo superior no dropdown |
| FA03.2 | Sistema valida que novo superior não criará ciclo |
| FA03.3 | Sistema executa query recursiva para verificar toda a hierarquia |
| FA03.4 | Se válido, sistema permite alteração |
| FA03.5 | Sistema atualiza Id_Cargo_Superior |
| FA03.6 | Sistema registra mudança hierárquica na auditoria |
| FA03.7 | Sistema atualiza visualizações de árvore hierárquica |

### FA04 - Remover Cargo Superior (Tornar Raiz)

**Trigger**: Usuário remove cargo superior, tornando cargo em raiz da hierarquia

| Passo | Descrição |
|-------|-----------|
| FA04.1 | Usuário clica em "X" ou "Remover" no campo cargo superior |
| FA04.2 | Sistema define Id_Cargo_Superior = NULL |
| FA04.3 | Sistema valida que cargo pode ser raiz (sem restrições) |
| FA04.4 | Sistema salva alteração |
| FA04.5 | Cargo agora aparece como "Cargo Raiz" nas listagens |

### FA05 - Adicionar/Remover Competências

**Trigger**: Usuário modifica lista de competências requeridas

| Passo | Descrição |
|-------|-----------|
| FA05.1 | Usuário abre multi-select de competências |
| FA05.2 | Usuário desmarca "JavaScript", adiciona "TypeScript" e "React" |
| FA05.3 | Sistema valida que competências selecionadas existem |
| FA05.4 | Sistema salva alterações |
| FA05.5 | Sistema executa DELETE dos relacionamentos antigos |
| FA05.6 | Sistema executa INSERT dos novos relacionamentos |
| FA05.7 | Auditoria registra competências adicionadas e removidas |

### FA06 - Adicionar/Remover Benefícios

**Trigger**: Usuário modifica lista de benefícios associados

| Passo | Descrição |
|-------|-----------|
| FA06.1 | Usuário abre multi-select de benefícios |
| FA06.2 | Usuário adiciona "Home Office" e remove "Vale Transporte" |
| FA06.3 | Sistema valida que benefícios existem |
| FA06.4 | Sistema atualiza relacionamentos |
| FA06.5 | Auditoria registra mudanças em benefícios |

### FA07 - Cancelar Edição

**Trigger**: Usuário decide não salvar alterações

| Passo | Descrição |
|-------|-----------|
| FA07.1 | Usuário clica em "Cancelar" ou "Voltar" |
| FA07.2 | Se há alterações, sistema exibe confirmação: "Descartar alterações?" |
| FA07.3 | Se usuário confirma, sistema descarta mudanças |
| FA07.4 | Sistema retorna para modo de visualização com dados originais |
| FA07.5 | Nenhuma alteração é salva no banco |

### FA08 - Salvar e Continuar Editando

**Trigger**: Usuário quer salvar mas continuar fazendo ajustes

| Passo | Descrição |
|-------|-----------|
| FA08.1 | Usuário clica em "Salvar e Continuar Editando" |
| FA08.2 | Sistema salva alterações normalmente |
| FA08.3 | Sistema mantém formulário em modo de edição |
| FA08.4 | Sistema atualiza RowVersion para nova versão |
| FA08.5 | Sistema exibe toast: "Alterações salvas" |
| FA08.6 | Usuário pode continuar fazendo ajustes |

### FA09 - Editar com Validação de Código em Tempo Real

**Trigger**: Usuário altera código do cargo

| Passo | Descrição |
|-------|-----------|
| FA09.1 | Usuário modifica código de "ANALISTA_TI" para "ANALISTA_TI_SENIOR" |
| FA09.2 | Sistema aguarda 500ms após última digitação (debounce) |
| FA09.3 | Sistema valida formato UPPER_SNAKE_CASE |
| FA09.4 | Sistema verifica unicidade via API assíncrona |
| FA09.5 | Se código já existe, exibe erro inline imediatamente |
| FA09.6 | Se código é único, exibe check verde de validação |
| FA09.7 | Usuário só pode salvar se validação passar |

### FA10 - Reverter para Versão Anterior (Histórico)

**Trigger**: Usuário quer desfazer alterações recentes

| Passo | Descrição |
|-------|-----------|
| FA10.1 | Usuário acessa aba "Histórico" |
| FA10.2 | Usuário visualiza timeline de alterações |
| FA10.3 | Usuário clica em "Reverter para esta versão" em um registro |
| FA10.4 | Sistema exibe confirmação com diff mostrando o que será alterado |
| FA10.5 | Usuário confirma |
| FA10.6 | Sistema restaura dados daquela versão |
| FA10.7 | Sistema registra operação de reversão na auditoria |

---

## 4. Fluxos de Exceção

### FE01 - Usuário Sem Permissão

**Trigger**: Usuário não possui permissão `cadastros:cargo:update`

| Passo | Descrição |
|-------|-----------|
| FE01.1 | Sistema detecta ausência de permissão no passo 2 |
| FE01.2 | Sistema retorna HTTP 403 Forbidden |
| FE01.3 | Sistema registra tentativa de acesso não autorizado na auditoria |
| FE01.4 | Frontend exibe mensagem: "Você não tem permissão para editar cargos" |
| FE01.5 | Frontend mantém página em modo somente leitura |
| FE01.6 | Botão "Editar" permanece desabilitado |

### FE02 - Código Duplicado (ao alterar código)

**Trigger**: Novo código já existe no conglomerado

| Passo | Descrição |
|-------|-----------|
| FE02.1 | Sistema detecta código duplicado no passo 26 |
| FE02.2 | Sistema executa rollback da transação |
| FE02.3 | Sistema retorna HTTP 409 Conflict |
| FE02.4 | Sistema inclui mensagem: "Código 'XXX' já está em uso" |
| FE02.5 | Frontend exibe erro no campo "Código" |
| FE02.6 | Frontend sugere manter código original ou escolher outro |
| FE02.7 | Usuário corrige código e tenta salvar novamente |

### FE03 - Conflito de Concorrência (Optimistic Locking)

**Trigger**: Outro usuário editou o cargo simultaneamente

| Passo | Descrição |
|-------|-----------|
| FE03.1 | Sistema detecta que RowVersion não corresponde (passo 25) |
| FE03.2 | Sistema retorna HTTP 409 Conflict |
| FE03.3 | Sistema inclui mensagem: "Este cargo foi modificado por outro usuário" |
| FE03.4 | Sistema envia dados da versão atual do banco |
| FE03.5 | Frontend exibe modal comparando:  - Sua versão (não salva)  - Versão atual no banco  - Diferenças destacadas |
| FE03.6 | Frontend oferece opções:  - "Sobrescrever" (descarta alterações do outro usuário)  - "Mesclar" (tenta merge inteligente)  - "Descartar minhas alterações" |
| FE03.7 | Usuário escolhe ação |
| FE03.8 | Sistema processa conforme escolha |

### FE04 - Ciclo Hierárquico Detectado

**Trigger**: Alteração de cargo superior cria ciclo

| Passo | Descrição |
|-------|-----------|
| FE04.1 | Sistema detecta ciclo no passo 15 ou 27 |
| FE04.2 | Sistema retorna HTTP 400 Bad Request |
| FE04.3 | Sistema inclui mensagem: "Não é possível criar hierarquia circular" |
| FE04.4 | Sistema detalha o ciclo: "A → B → C → A" |
| FE04.5 | Frontend exibe erro no campo "Cargo Superior" |
| FE04.6 | Frontend remove opção problemática da lista |
| FE04.7 | Usuário seleciona cargo superior válido ou remove |

### FE05 - Faixa Salarial Inválida

**Trigger**: Salário máximo < salário mínimo

| Passo | Descrição |
|-------|-----------|
| FE05.1 | Sistema detecta inconsistência no passo 13 ou 24 |
| FE05.2 | Sistema retorna HTTP 400 Bad Request |
| FE05.3 | Sistema inclui mensagem: "Salário máximo deve ser maior ou igual ao salário mínimo" |
| FE05.4 | Frontend exibe erro nos campos de salário |
| FE05.5 | Frontend destaca ambos os campos em vermelho |
| FE05.6 | Usuário corrige valores e tenta salvar novamente |

### FE06 - Cargo Não Encontrado

**Trigger**: Cargo foi excluído/inativado entre carregar e salvar

| Passo | Descrição |
|-------|-----------|
| FE06.1 | Sistema tenta atualizar e não encontra cargo (passo 30) |
| FE06.2 | Sistema retorna HTTP 404 Not Found |
| FE06.3 | Sistema inclui mensagem: "Cargo não encontrado ou foi removido" |
| FE06.4 | Frontend exibe erro |
| FE06.5 | Frontend redireciona para listagem após 3 segundos |
| FE06.6 | Caso de uso é encerrado |

### FE07 - Cargo de Outro Conglomerado

**Trigger**: Tentativa de editar cargo que não pertence ao conglomerado do usuário

| Passo | Descrição |
|-------|-----------|
| FE07.1 | Sistema valida Id_Conglomerado no passo 3 ou 28 |
| FE07.2 | Sistema detecta mismatch |
| FE07.3 | Sistema retorna HTTP 404 Not Found (não revela existência) |
| FE07.4 | Sistema registra tentativa suspeita com flag de segurança |
| FE07.5 | Sistema envia alerta para equipe de segurança |
| FE07.6 | Frontend exibe mensagem genérica: "Cargo não encontrado" |
| FE07.7 | Caso de uso é encerrado |

### FE08 - Erro de Conexão com Banco de Dados

**Trigger**: Banco de dados está indisponível durante edição

| Passo | Descrição |
|-------|-----------|
| FE08.1 | Sistema tenta atualizar e recebe exceção de conexão |
| FE08.2 | Sistema executa rollback automático da transação |
| FE08.3 | Sistema tenta reconectar (retry pattern - 3 tentativas) |
| FE08.4 | Se todas as tentativas falharem, retorna HTTP 503 Service Unavailable |
| FE08.5 | Sistema registra erro detalhado no log |
| FE08.6 | Frontend exibe mensagem: "Serviço temporariamente indisponível. Suas alterações foram preservadas. Tente novamente em alguns instantes." |
| FE08.7 | Frontend mantém dados preenchidos no formulário |
| FE08.8 | Frontend oferece botão "Tentar Novamente" |

### FE09 - Timeout na Atualização

**Trigger**: Operação demora mais que timeout configurado

| Passo | Descrição |
|-------|-----------|
| FE09.1 | Sistema atinge timeout durante atualização |
| FE09.2 | Sistema tenta verificar se cargo foi atualizado |
| FE09.3 | Se foi atualizado, retorna sucesso com warning |
| FE09.4 | Se não foi atualizado, executa rollback |
| FE09.5 | Sistema retorna HTTP 504 Gateway Timeout |
| FE09.6 | Sistema registra evento no log |
| FE09.7 | Frontend exibe mensagem e oferece re-tentativa |

### FE10 - Erro ao Atualizar Relacionamentos

**Trigger**: Erro ao atualizar competências ou benefícios

| Passo | Descrição |
|-------|-----------|
| FE10.1 | Cargo principal é atualizado (passo 30) |
| FE10.2 | Erro ocorre ao atualizar relacionamentos (passo 31-34) |
| FE10.3 | Sistema executa rollback de toda a transação |
| FE10.4 | Cargo não é atualizado (mantém integridade) |
| FE10.5 | Sistema retorna HTTP 500 Internal Server Error |
| FE10.6 | Sistema registra stack trace completo |
| FE10.7 | Frontend exibe mensagem: "Erro ao processar relacionamentos. Tente novamente." |
| FE10.8 | Frontend mantém dados preenchidos |

---

## 5. Regras de Negócio

### RN-CAD-009-01: Código Único por Conglomerado

**Descrição**: Se código for alterado, o novo código deve ser único no conglomerado (não pode existir outro cargo com esse código).

**Criticidade**: CRÍTICA

**Implementação**:
- Validação assíncrona no frontend (apenas se código alterado)
- Validação server-side antes de UPDATE
- Query: SELECT COUNT(*) WHERE Cd_Cargo = @novoCodigo AND Id != @idCargo AND Id_Conglomerado = @IdConglomerado

**Teste**:
- Tentar alterar código para um existente (deve falhar)
- Manter código original (deve funcionar sem validação extra)

### RN-CAD-009-02: Formato de Código (UPPER_SNAKE_CASE)

**Descrição**: Se código for alterado, deve manter formato UPPER_SNAKE_CASE.

**Criticidade**: ALTA

**Implementação**:
- Validação inline se código for modificado
- Regex: `^[A-Z0-9]+(_[A-Z0-9]+)*$`

**Teste**:
- Alterar para "analista_ti" (inválido) - deve falhar
- Alterar para "ANALISTA_TI_SENIOR" (válido) - deve funcionar

### RN-CAD-009-03: Faixa Salarial Válida

**Descrição**: Salário base máximo >= salário base mínimo. Ambos > 0.

**Criticidade**: ALTA

**Implementação**:
- Validação inline em tempo real
- Validação server-side antes de UPDATE

**Teste**:
- Alterar mínimo para R$ 10.000 e máximo para R$ 5.000 (inválido)
- Alterar ambos para faixa válida

### RN-CAD-009-04: Não Criar Ciclo Hierárquico

**Descrição**: Se cargo superior for alterado, não pode criar ciclo.

**Criticidade**: CRÍTICA

**Implementação**:
- Validação recursiva apenas se cargo superior foi modificado
- Query WITH RECURSIVE para verificar ciclo

**Teste**:
- Cargo A tem superior B. Tentar alterar B para ter superior A (ciclo)
- Alterar cargo superior para hierarquia válida

### RN-CAD-009-05: Controle de Concorrência Otimista

**Descrição**: Sistema deve detectar se outro usuário editou o cargo simultaneamente e prevenir sobrescrita acidental.

**Criticidade**: ALTA

**Implementação**:
- Campo RowVersion (timestamp ou GUID)
- WHERE clause: UPDATE ... WHERE Id = @Id AND RowVersion = @RowVersionOriginal
- Se @@ROWCOUNT = 0, significa que registro foi alterado por outro usuário

**Teste**:
- Dois usuários editam mesmo cargo simultaneamente
- Primeiro salva com sucesso
- Segundo recebe erro de concorrência

### RN-CAD-009-06: Isolamento Multi-tenant

**Descrição**: Usuário só pode editar cargos do seu conglomerado.

**Criticidade**: CRÍTICA

**Implementação**:
- Validação de Id_Conglomerado antes de UPDATE
- WHERE clause sempre inclui: AND Id_Conglomerado = @IdConglomerado
- Tentativas suspeitas são alertadas

**Teste**:
- Usuário do conglomerado A tenta editar cargo do conglomerado B
- Sistema bloqueia e alerta

### RN-CAD-009-07: Auditoria Completa com Diff

**Descrição**: Toda edição deve registrar na auditoria com comparação antes/depois de TODOS os campos alterados.

**Criticidade**: ALTA

**Implementação**:
- Snapshot dos dados originais capturado antes de editar
- Após UPDATE, sistema compara snapshot com dados atualizados
- Registra apenas campos que realmente mudaram
- JSON estruturado: `{"antes": {...}, "depois": {...}, "diff": [...]}`

**Teste**:
- Editar cargo e verificar registro na auditoria
- Verificar que apenas campos alterados estão no diff

### RN-CAD-009-08: Invalidação de Cache

**Descrição**: Após edição, cache de listagem e visualização deve ser invalidado.

**Criticidade**: MÉDIA

**Implementação**:
- Cache.Remove("cargo_list_" + Id_Conglomerado + "*")
- Cache.Remove("cargo_detail_" + Id)
- Invalidação em todas as variações

**Teste**:
- Editar cargo
- Listar/visualizar imediatamente
- Verificar que dados atualizados aparecem

### RN-CAD-009-09: Campos Não Editáveis

**Descrição**: Alguns campos não podem ser editados: Id, Id_Conglomerado, Dt_Cadastro, Id_Usuario_Criacao.

**Criticidade**: ALTA

**Implementação**:
- Campos não enviáveis pelo frontend
- Backend ignora se enviados (não atualiza)
- Validação: campos de auditoria são set automaticamente

**Teste**:
- Tentar enviar Id_Conglomerado diferente no payload
- Verificar que valor é ignorado

### RN-CAD-009-10: Transação Atômica

**Descrição**: Atualização do cargo e relacionamentos deve ser atômica. Se qualquer parte falhar, rollback completo.

**Criticidade**: CRÍTICA

**Implementação**:
- using (var transaction = db.BeginTransaction())
- Rollback automático em caso de exceção
- Commit apenas se tudo bem-sucedido

**Teste**:
- Simular erro ao atualizar relacionamento
- Verificar que cargo principal também não foi atualizado

### RN-CAD-009-11: Validação de Campos Obrigatórios

**Descrição**: Campos obrigatórios não podem ser removidos/esvaziados durante edição.

**Criticidade**: ALTA

**Implementação**:
- Validação client-side: required validator
- Validação server-side: NotEmpty validator
- Campos: Código, Nome, Salário Base Min/Max

**Teste**:
- Tentar esvaziar campo "Nome" e salvar (deve falhar)
- Tentar alterar salário para 0 (deve falhar)

### RN-CAD-009-12: Notificação de Alterações Críticas

**Descrição**: Alterações em faixa salarial, hierarquia ou competências podem disparar notificações (se configurado).

**Criticidade**: BAIXA

**Implementação**:
- Sistema compara campos críticos no diff
- Se houver alteração relevante, envia notificação assíncrona
- Destinatários: RH, gestores da área

**Teste**:
- Alterar faixa salarial significativamente (ex: aumento > 20%)
- Verificar que notificação é enviada (se configurado)

---

## 6. Especificação de Testes

### 6.1. Cenários de Teste Backend

| ID | Cenário | Tipo | Prioridade |
|----|---------|------|------------|
| CN-UC03-001 | Editar cargo com sucesso alterando nome e descrição | Positivo | Alta |
| CN-UC03-002 | Editar cargo alterando código (único) | Positivo | Alta |
| CN-UC03-003 | Editar cargo alterando faixa salarial | Positivo | Alta |
| CN-UC03-004 | Editar cargo alterando cargo superior | Positivo | Alta |
| CN-UC03-005 | Editar cargo adicionando/removendo competências | Positivo | Alta |
| CN-UC03-006 | Editar cargo adicionando/removendo benefícios | Positivo | Média |
| CN-UC03-007 | Tentar editar com código duplicado | Negativo | Alta |
| CN-UC03-008 | Tentar editar criando ciclo hierárquico | Negativo | Crítica |
| CN-UC03-009 | Tentar editar com faixa salarial inválida | Negativo | Alta |
| CN-UC03-010 | Tentar editar sem permissão | Negativo | Alta |
| CN-UC03-011 | Tentar editar cargo de outro conglomerado | Segurança | Crítica |
| CN-UC03-012 | Editar simultaneamente (conflito de concorrência) | Concorrência | Alta |
| CN-UC03-013 | Editar e verificar auditoria com diff | Auditoria | Alta |
| CN-UC03-014 | Editar e verificar invalidação de cache | Performance | Média |

### 6.2. Casos de Teste Sistema (E2E)

| ID | Caso de Teste | Tipo | Prioridade |
|----|---------------|------|------------|
| TC-UC03-001 | Acessar modo edição e alterar campos | Funcional | Alta |
| TC-UC03-002 | Validações inline (código, salários) | Funcional | Alta |
| TC-UC03-003 | Salvar alterações com sucesso | Funcional | Alta |
| TC-UC03-004 | Cancelar edição com dados preenchidos | Funcional | Média |
| TC-UC03-005 | Conflito de concorrência com 2 usuários | Concorrência | Alta |
| TC-UC03-006 | Alterar hierarquia e visualizar árvore atualizada | Funcional | Média |

### 6.3. Testes de Performance

| ID | Teste | Meta | Prioridade |
|----|-------|------|------------|
| PERF-UC03-001 | Tempo de resposta para edição simples | < 2s | Alta |
| PERF-UC03-002 | Tempo de resposta para edição com muitos relacionamentos | < 3s | Média |

---

## 7. Matriz de Permissões

| Permissão | Pode Editar | Pode Alterar Código | Pode Alterar Hierarquia | Pode Alterar Salários |
|-----------|------------|-------------------|------------------------|----------------------|
| `cadastros:cargo:update` | ✅ Sim | ✅ Sim | ✅ Sim | ✅ Sim |
| `cadastros:cargo:admin` | ✅ Sim | ✅ Sim | ✅ Sim | ✅ Sim |

---

## 8. Casos de Teste Detalhados

### CT-001: Editar Cargo com Sucesso (Nome e Descrição)

**Pré-condições**:
- Usuário autenticado com permissão `cadastros:cargo:update`
- Existe cargo "ANALISTA_TI" (Id=10)

**Dados de Entrada**:
```json
{
  "id": 10,
  "codigo": "ANALISTA_TI",
  "nome": "Analista de TI Pleno",
  "descricao": "Descrição atualizada",
  "salarioBaseMin": 5000.00,
  "salarioBaseMax": 8000.00,
  "rowVersion": "AAAAAABcd=="
}
```

**Passos**:
1. Fazer requisição PUT para `/api/v1/cadastros/cargos/10`
2. Aguardar resposta

**Resultado Esperado**:
- Status: 200 OK
- Cargo atualizado no banco
- Apenas campos "nome" e "descricao" alterados
- Dt_Atualizacao atualizado
- RowVersion incrementado
- Registro na auditoria com diff mostrando apenas alterações em nome/descrição
- Cache invalidado

### CT-002: Tentar Editar com Código Duplicado

**Pré-condições**:
- Usuário autenticado com permissão `cadastros:cargo:update`
- Existe cargo "ANALISTA_TI" (Id=10)
- Existe outro cargo "GERENTE_TI" (Id=5)

**Dados de Entrada**:
```json
{
  "id": 10,
  "codigo": "GERENTE_TI",
  "nome": "Analista de TI",
  "salarioBaseMin": 5000.00,
  "salarioBaseMax": 8000.00,
  "rowVersion": "AAAAAABcd=="
}
```

**Passos**:
1. Fazer requisição PUT para `/api/v1/cadastros/cargos/10`
2. Aguardar resposta

**Resultado Esperado**:
- Status: 409 Conflict
- Mensagem: "Código 'GERENTE_TI' já está em uso"
- Nenhuma alteração no banco
- Tentativa registrada na auditoria

### CT-003: Conflito de Concorrência

**Pré-condições**:
- Dois usuários (A e B) editam mesmo cargo simultaneamente
- Cargo "ANALISTA_TI" (Id=10, RowVersion="v1")

**Passos**:
1. Usuário A carrega cargo para edição (RowVersion="v1")
2. Usuário B carrega cargo para edição (RowVersion="v1")
3. Usuário A altera nome para "Analista Sênior" e salva (sucesso, novo RowVersion="v2")
4. Usuário B altera descrição e tenta salvar com RowVersion="v1"

**Resultado Esperado (para Usuário B)**:
- Status: 409 Conflict
- Mensagem: "Este cargo foi modificado por outro usuário"
- Body inclui versão atual do banco (com alterações do Usuário A)
- Frontend exibe modal de resolução de conflito
- Usuário B pode:  - Sobrescrever (descarta mudanças do A)  - Mesclar (tenta merge)  - Descartar suas mudanças

### CT-004: Alterar Cargo Superior Criando Ciclo

**Pré-condições**:
- Cargo A (Id=1) tem superior B (Id=2)
- Cargo B (Id=2) tem superior C (Id=3)
- Usuário quer alterar cargo C para ter superior A

**Dados de Entrada** (editar cargo C):
```json
{
  "id": 3,
  "codigo": "CARGO_C",
  "nome": "Cargo C",
  "cargoSuperiorId": 1,
  "salarioBaseMin": 3000.00,
  "salarioBaseMax": 5000.00,
  "rowVersion": "AAAAAABcd=="
}
```

**Passos**:
1. Fazer requisição PUT para `/api/v1/cadastros/cargos/3`
2. Sistema detecta ciclo: C → A → B → C

**Resultado Esperado**:
- Status: 400 Bad Request
- Mensagem: "Não é possível criar hierarquia circular"
- Detalhes do ciclo: "C → A → B → C"
- Nenhuma alteração no banco

---

## 9. Notas Técnicas

### 9.1. Endpoint da API

```
PUT /api/v1/cadastros/cargos/{id}
```

### 9.2. Estrutura do Request Body

```json
{
  "id": 10,
  "codigo": "string",
  "nome": "string",
  "descricao": "string",
  "cargoSuperiorId": "int?",
  "cboCode": "string?",
  "salarioBaseMin": "decimal",
  "salarioBaseMax": "decimal",
  "competenciasIds": "int[]",
  "beneficiosIds": "int[]",
  "observacoes": "string?",
  "rowVersion": "string (Base64)"
}
```

### 9.3. Estrutura do Response

**Sucesso (200 OK)**: Igual ao response de criação, mas com campos de auditoria atualizados.

**Erro de Concorrência (409 Conflict)**:
```json
{
  "type": "ConcurrencyError",
  "title": "Conflito de concorrência",
  "status": 409,
  "message": "Este cargo foi modificado por outro usuário",
  "currentData": {
    "id": 10,
    "codigo": "ANALISTA_TI_SENIOR",
    "nome": "Analista de TI Sênior",
    "...": "..."
  },
  "traceId": "00-abc123-def456-01"
}
```

---

## 10. Histórico de Alterações

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 1.0 | 2025-01-10 | Equipe IControlIT | Versão inicial |
| 2.0 | 2025-11-04 | Equipe IControlIT | Adequação ao padrão de documentação completo |

---

**Revisado por**: Equipe de Arquitetura
**Aprovado por**: Product Owner
**Data de Aprovação**: 2025-11-04

---

# UC04 - Inativar Cargo

**ID do Caso de Uso**: UC04
**Nome do Caso de Uso**: Inativar Cargo (Soft Delete)
**Requisito Funcional**: RF-CAD-009
**Autor**: Equipe IControlIT
**Status**: Em Desenvolvimento

---

## Índice

1. [Informações Gerais](#1-informações-gerais)
2. [Fluxo Principal](#2-fluxo-principal)
3. [Fluxos Alternativos](#3-fluxos-alternativos)
4. [Fluxos de Exceção](#4-fluxos-de-exceção)
5. [Regras de Negócio](#5-regras-de-negócio)
6. [Especificação de Testes](#6-especificação-de-testes)
7. [Matriz de Permissões](#7-matriz-de-permissões)
8. [Casos de Teste Detalhados](#8-casos-de-teste-detalhados)

---

## 1. Informações Gerais

### 1.1. Descrição

Este caso de uso permite que usuários autorizados inativem cargos no sistema IControlIT, utilizando o padrão soft delete (exclusão lógica). A inativação preserva todos os dados do cargo no banco de dados para fins de auditoria, compliance e histórico, mas impede que o cargo seja utilizado em novas atribuições. O sistema valida que o cargo não possui consumidores (colaboradores) ativos antes de permitir a inativação, garantindo integridade referencial e evitando inconsistências operacionais.

### 1.2. Atores

- **Ator Principal**: Usuário Autenticado com permissão `cadastros:cargo:delete`
- **Atores Secundários**:
  - Sistema de Validação (verifica se há consumidores ativos)
  - Sistema de Auditoria (registra inativação)
  - Sistema de Notificações (notifica gestores quando configurado)
  - API Backend (.NET 10)

### 1.3. Pré-condições

| ID | Descrição |
|----|-----------|
| PRE-01 | Usuário deve estar autenticado no sistema |
| PRE-02 | Usuário deve possuir permissão `cadastros:cargo:delete` |
| PRE-03 | Cargo a ser inativado deve existir e estar ativo (Fl_Ativo = 1) |
| PRE-04 | Cargo deve pertencer ao conglomerado do usuário |
| PRE-05 | Cargo NÃO deve ter consumidores ativos associados |
| PRE-06 | Conexão com banco de dados deve estar disponível |
| PRE-07 | Sistema de auditoria deve estar operacional |

### 1.4. Pós-condições

| ID | Descrição |
|----|-----------|
| POS-01 | Fl_Ativo do cargo é definido como 0 (inativo) |
| POS-02 | Dt_Inativacao é definida com timestamp atual |
| POS-03 | Id_Usuario_Inativacao é definido como o usuário responsável |
| POS-04 | Motivo da inativação é registrado (se fornecido) |
| POS-05 | Operação de inativação é registrada no log de auditoria |
| POS-06 | Cache de listagem e visualização é invalidado |
| POS-07 | Cargo não aparece mais em listagens padrão (apenas com filtro especial) |
| POS-08 | Cargo não pode mais ser selecionado em novos cadastros |
| POS-09 | Notificação é enviada (se configurado) |
| POS-10 | Dados históricos e relacionamentos são preservados |

### 1.5. Requisitos Não-Funcionais

| ID | Tipo | Descrição | Meta |
|----|------|-----------|------|
| RNF-01 | Performance | Tempo de resposta da inativação | < 2 segundos |
| RNF-02 | Usabilidade | Confirmação clara com avisos | Prevenção de erros acidentais |
| RNF-03 | Segurança | Validação rigorosa de permissões | 100% dos acessos validados |
| RNF-04 | Auditoria | Registro completo da operação | 100% das inativações auditadas |
| RNF-05 | Integridade | Preservação de dados históricos | 0% perda de dados |
| RNF-06 | Consistência | Transações ACID | Rollback em caso de erro |
| RNF-07 | Compliance | Conformidade com LGPD | Dados preservados para auditoria |

---

## 2. Fluxo Principal

**Trigger**: Usuário clica no botão "Inativar" na página de visualização ou listagem do cargo

| Passo | Ator | Descrição | Sistema |
|-------|------|-----------|---------|
| 1 | Usuário | Clica no botão "Inativar" | Sistema captura ID do cargo |
| 2 | Sistema | Valida permissão `cadastros:cargo:delete` do usuário | Middleware de autorização |
| 3 | Sistema | Valida que cargo pertence ao conglomerado do usuário | TenantContext validation |
| 4 | Sistema | Carrega dados atuais do cargo | Database query |
| 5 | Sistema | Verifica se cargo já está inativo (Fl_Ativo = 0) | Status validation |
| 6 | Sistema | Conta total de consumidores ativos com este cargo | Count query |
| 7 | Sistema | Verifica se existem consumidores ativos (COUNT > 0) | Business rule validation |
| 8 | Sistema | Se há consumidores ativos, bloqueia inativação (vai para FE02) | Constraint validation |
| 9 | Sistema | Carrega lista de cargos subordinados (se houver) | Hierarchy query |
| 10 | Sistema | Exibe modal de confirmação com informações críticas | UI Dialog |
| 11 | Modal | Exibe título: "Inativar Cargo?" | Confirmation header |
| 12 | Modal | Exibe aviso: "Cargo: [CODIGO] - [NOME]" | Cargo details |
| 13 | Modal | Exibe aviso: "Este cargo não poderá mais ser atribuído a novos consumidores" | Warning message |
| 14 | Modal | Exibe info: "Consumidores atuais: 0 ativos" | Validation info |
| 15 | Modal | Se há subordinados, exibe: "X cargos subordinados serão mantidos (não afetados)" | Hierarchy info |
| 16 | Modal | Exibe campo opcional: "Motivo da inativação" (textarea) | Optional input |
| 17 | Modal | Exibe botões: "Cancelar" (secondary) e "Confirmar Inativação" (danger) | Action buttons |
| 18 | Usuário | Preenche motivo (opcional) e clica em "Confirmar Inativação" | Confirm action |
| 19 | Sistema | Fecha modal e exibe loader | UI Feedback |
| 20 | Sistema | Envia requisição DELETE para API | HTTP Request |
| 21 | Sistema | Valida permissão novamente (server-side) | Authorization Filter |
| 22 | Sistema | Valida que cargo pertence ao conglomerado | TenantContext |
| 23 | Sistema | Verifica novamente se há consumidores ativos (race condition) | Final validation |
| 24 | Sistema | Se passou validações, inicia transação no banco | BeginTransaction |
| 25 | Sistema | Executa UPDATE: SET Fl_Ativo = 0 | Soft delete |
| 26 | Sistema | Define Dt_Inativacao = NOW() | Timestamp |
| 27 | Sistema | Define Id_Usuario_Inativacao = @IdUsuario | User tracking |
| 28 | Sistema | Armazena motivo em campo Motivo_Inativacao (se fornecido) | Optional field |
| 29 | Sistema | Registra operação na tabela de auditoria | INSERT INTO AuditLog |
| 30 | Sistema | Auditoria inclui: usuário, data/hora, motivo, dados completos do cargo | Audit details |
| 31 | Sistema | Invalida cache de listagem e visualização | Cache.Remove |
| 32 | Sistema | Comita transação | COMMIT |
| 33 | Sistema | Envia notificação (se configurado) | Notification Service |
| 34 | Sistema | Retorna HTTP 200 OK com mensagem | JSON Response |
| 35 | Frontend | Exibe toast de sucesso: "Cargo inativado com sucesso" | Toast notification |
| 36 | Frontend | Remove cargo da listagem (se estava visível) | UI Update |
| 37 | Frontend | Se estava na página de visualização, redireciona para listagem | Navigation |
| 38 | Sistema | Registra métrica de sucesso | Application Insights |

---

## 3. Fluxos Alternativos

### FA01 - Reativar Cargo Inativo

**Trigger**: Usuário com permissão especial clica em "Reativar" em cargo inativo

| Passo | Descrição |
|-------|-----------|
| FA01.1 | Usuário visualiza cargo inativo (badge "INATIVO" visível) |
| FA01.2 | Sistema valida permissão `cadastros:cargo:reactivate` |
| FA01.3 | Sistema exibe botão "Reativar" |
| FA01.4 | Usuário clica em "Reativar" |
| FA01.5 | Sistema exibe confirmação: "Reativar cargo [CODIGO]?" |
| FA01.6 | Usuário confirma |
| FA01.7 | Sistema executa UPDATE: SET Fl_Ativo = 1 |
| FA01.8 | Sistema define Dt_Reativacao = NOW() |
| FA01.9 | Sistema limpa Dt_Inativacao e Motivo_Inativacao |
| FA01.10 | Sistema registra reativação na auditoria |
| FA01.11 | Sistema invalida cache |
| FA01.12 | Sistema exibe toast: "Cargo reativado com sucesso" |
| FA01.13 | Cargo volta a aparecer em listagens padrão |

### FA02 - Cancelar Inativação

**Trigger**: Usuário decide não inativar após abrir modal

| Passo | Descrição |
|-------|-----------|
| FA02.1 | Modal de confirmação está aberto |
| FA02.2 | Usuário clica em "Cancelar" ou pressiona ESC |
| FA02.3 | Sistema fecha modal |
| FA02.4 | Nenhuma alteração é feita no banco |
| FA02.5 | Usuário permanece na tela atual |
| FA02.6 | Cargo continua ativo |

### FA03 - Inativar Cargo com Subordinados

**Trigger**: Cargo a ser inativado tem cargos subordinados na hierarquia

| Passo | Descrição |
|-------|-----------|
| FA03.1 | Sistema detecta que cargo tem subordinados (passo 9) |
| FA03.2 | Sistema exibe aviso no modal: "Este cargo possui X cargos subordinados" |
| FA03.3 | Sistema lista cargos subordinados no modal |
| FA03.4 | Sistema esclarece: "Subordinados NÃO serão inativados automaticamente" |
| FA03.5 | Sistema esclarece: "Subordinados terão cargo superior = NULL (raiz)" |
| FA03.6 | Usuário confirma ciente das consequências |
| FA03.7 | Sistema inativa cargo principal |
| FA03.8 | Sistema atualiza subordinados: SET Id_Cargo_Superior = NULL |
| FA03.9 | Sistema registra ajuste de hierarquia na auditoria |

### FA04 - Visualizar Lista de Consumidores Antes de Inativar

**Trigger**: Usuário quer ver quem está no cargo antes de inativar

| Passo | Descrição |
|-------|-----------|
| FA04.1 | Modal de confirmação está aberto |
| FA04.2 | Usuário clica em link "Ver consumidores" (se houver) |
| FA04.3 | Sistema expande seção com lista de consumidores |
| FA04.4 | Sistema exibe: nome, matrícula, departamento de cada consumidor |
| FA04.5 | Sistema diferencia ativos de inativos |
| FA04.6 | Usuário revisa lista |
| FA04.7 | Usuário decide se prossegue ou cancela |

### FA05 - Inativação em Lote (Múltiplos Cargos)

**Trigger**: Usuário seleciona múltiplos cargos na listagem e clica "Inativar Selecionados"

| Passo | Descrição |
|-------|-----------|
| FA05.1 | Usuário marca checkboxes de 3 cargos |
| FA05.2 | Usuário clica em "Ações em Lote" > "Inativar Selecionados" |
| FA05.3 | Sistema valida que todos pertencem ao conglomerado |
| FA05.4 | Sistema verifica consumidores ativos em CADA cargo |
| FA05.5 | Sistema identifica que 1 cargo tem consumidores (bloqueado) |
| FA05.6 | Sistema exibe modal: "2 de 3 cargos podem ser inativados" |
| FA05.7 | Sistema lista cargo bloqueado com motivo |
| FA05.8 | Usuário confirma inativação parcial |
| FA05.9 | Sistema inativa os 2 cargos válidos |
| FA05.10 | Sistema exibe resultado: "2 inativados, 1 bloqueado" |

### FA06 - Adicionar Motivo Detalhado

**Trigger**: Usuário fornece motivo detalhado da inativação

| Passo | Descrição |
|-------|-----------|
| FA06.1 | Modal de confirmação está aberto |
| FA06.2 | Usuário preenche campo "Motivo": "Cargo substituído por ANALISTA_SENIOR_V2" |
| FA06.3 | Sistema valida tamanho (máx 500 caracteres) |
| FA06.4 | Usuário confirma inativação |
| FA06.5 | Sistema armazena motivo em campo Motivo_Inativacao |
| FA06.6 | Motivo fica visível em: auditoria, histórico, visualização do cargo inativo |
| FA06.7 | Facilita compreensão futura do porquê da inativação |

---

## 4. Fluxos de Exceção

### FE01 - Usuário Sem Permissão

**Trigger**: Usuário não possui permissão `cadastros:cargo:delete`

| Passo | Descrição |
|-------|-----------|
| FE01.1 | Sistema detecta ausência de permissão no passo 2 |
| FE01.2 | Sistema retorna HTTP 403 Forbidden |
| FE01.3 | Sistema registra tentativa de acesso não autorizado na auditoria |
| FE01.4 | Frontend exibe mensagem: "Você não tem permissão para inativar cargos" |
| FE01.5 | Botão "Inativar" permanece oculto/desabilitado na UI |
| FE01.6 | Caso de uso é encerrado |

### FE02 - Cargo Possui Consumidores Ativos

**Trigger**: Cargo tem colaboradores ativos associados (regra de negócio mais importante)

| Passo | Descrição |
|-------|-----------|
| FE02.1 | Sistema detecta consumidores ativos no passo 7 ou 23 |
| FE02.2 | Sistema conta total: COUNT(*) FROM Consumidor WHERE Id_Cargo = @Id AND Fl_Ativo = 1 |
| FE02.3 | Sistema retorna HTTP 400 Bad Request |
| FE02.4 | Sistema inclui mensagem: "Não é possível inativar cargo com consumidores ativos" |
| FE02.5 | Sistema inclui detalhes: "Este cargo possui X consumidores ativos" |
| FE02.6 | Sistema sugere ações:  - "Reatribua os consumidores para outro cargo"  - "Ou inative os consumidores primeiro" |
| FE02.7 | Frontend exibe modal de erro com lista de consumidores |
| FE02.8 | Frontend oferece botão "Ver Consumidores" que redireciona para lista filtrada |
| FE02.9 | Cargo NÃO é inativado |
| FE02.10 | Caso de uso é encerrado |

### FE03 - Cargo Já Está Inativo

**Trigger**: Tentativa de inativar cargo que já está inativo

| Passo | Descrição |
|-------|-----------|
| FE03.1 | Sistema detecta que Fl_Ativo = 0 no passo 5 |
| FE03.2 | Sistema retorna HTTP 400 Bad Request |
| FE03.3 | Sistema inclui mensagem: "Este cargo já está inativo" |
| FE03.4 | Sistema fornece detalhes: inativado em [DATA] por [USUARIO] |
| FE03.5 | Frontend exibe mensagem informativa |
| FE03.6 | Frontend oferece botão "Reativar" (se usuário tem permissão) |
| FE03.7 | Caso de uso é encerrado |

### FE04 - Cargo Não Encontrado

**Trigger**: ID fornecido não corresponde a cargo existente

| Passo | Descrição |
|-------|-----------|
| FE04.1 | Sistema tenta carregar cargo no passo 4 |
| FE04.2 | Query não retorna resultado |
| FE04.3 | Sistema retorna HTTP 404 Not Found |
| FE04.4 | Sistema inclui mensagem: "Cargo não encontrado" |
| FE04.5 | Sistema registra tentativa na auditoria |
| FE04.6 | Frontend exibe mensagem de erro |
| FE04.7 | Frontend redireciona para listagem |
| FE04.8 | Caso de uso é encerrado |

### FE05 - Cargo de Outro Conglomerado

**Trigger**: Tentativa de inativar cargo que não pertence ao conglomerado do usuário

| Passo | Descrição |
|-------|-----------|
| FE05.1 | Sistema valida Id_Conglomerado no passo 3 ou 22 |
| FE05.2 | Sistema detecta mismatch (cargo não pertence ao conglomerado) |
| FE05.3 | Sistema retorna HTTP 404 Not Found (não revela existência) |
| FE05.4 | Sistema registra tentativa suspeita com flag de segurança |
| FE05.5 | Sistema envia alerta para equipe de segurança |
| FE05.6 | Frontend exibe mensagem genérica: "Cargo não encontrado" |
| FE05.7 | Caso de uso é encerrado |

### FE06 - Erro de Conexão com Banco de Dados

**Trigger**: Banco de dados está indisponível durante inativação

| Passo | Descrição |
|-------|-----------|
| FE06.1 | Sistema tenta executar UPDATE e recebe exceção de conexão |
| FE06.2 | Sistema executa rollback automático da transação |
| FE06.3 | Sistema tenta reconectar (retry pattern - 3 tentativas) |
| FE06.4 | Se todas as tentativas falharem, retorna HTTP 503 Service Unavailable |
| FE06.5 | Sistema registra erro detalhado no log |
| FE06.6 | Frontend exibe mensagem: "Serviço temporariamente indisponível. Tente novamente em alguns instantes." |
| FE06.7 | Frontend oferece botão "Tentar Novamente" |
| FE06.8 | Sistema envia alerta para equipe de operações |

### FE07 - Race Condition (Consumidores Adicionados Durante Processo)

**Trigger**: Entre validação inicial e UPDATE, consumidor é atribuído ao cargo

| Passo | Descrição |
|-------|-----------|
| FE07.1 | Sistema valida: 0 consumidores ativos (passo 6) |
| FE07.2 | Usuário confirma inativação |
| FE07.3 | Outro usuário, simultaneamente, atribui cargo a 1 consumidor |
| FE07.4 | Sistema executa validação final (passo 23) |
| FE07.5 | Sistema detecta 1 consumidor ativo agora |
| FE07.6 | Sistema executa rollback |
| FE07.7 | Sistema retorna HTTP 409 Conflict |
| FE07.8 | Sistema inclui mensagem: "Consumidor foi atribuído a este cargo durante o processo" |
| FE07.9 | Frontend exibe erro e sugere recarregar dados |
| FE07.10 | Cargo NÃO é inativado |

### FE08 - Timeout na Inativação

**Trigger**: Operação demora mais que timeout configurado

| Passo | Descrição |
|-------|-----------|
| FE08.1 | Sistema atinge timeout durante UPDATE |
| FE08.2 | Sistema tenta verificar se cargo foi inativado |
| FE08.3 | Se foi inativado, retorna sucesso com warning |
| FE08.4 | Se não foi inativado, executa rollback |
| FE08.5 | Sistema retorna HTTP 504 Gateway Timeout |
| FE08.6 | Sistema registra evento no log |
| FE08.7 | Frontend exibe mensagem e oferece re-tentativa |

### FE09 - Erro ao Ajustar Subordinados

**Trigger**: Erro ao atualizar cargo superior dos subordinados

| Passo | Descrição |
|-------|-----------|
| FE09.1 | Cargo principal é inativado (passo 25-28) |
| FE09.2 | Erro ocorre ao atualizar subordinados (FA03.8) |
| FE09.3 | Sistema executa rollback de toda a transação |
| FE09.4 | Cargo NÃO é inativado (mantém integridade) |
| FE09.5 | Sistema retorna HTTP 500 Internal Server Error |
| FE09.6 | Sistema registra stack trace completo |
| FE09.7 | Frontend exibe mensagem: "Erro ao processar hierarquia. Tente novamente." |

### FE10 - Erro ao Registrar Auditoria

**Trigger**: Falha ao gravar log de auditoria

| Passo | Descrição |
|-------|-----------|
| FE10.1 | Cargo é inativado com sucesso (passo 25-28) |
| FE10.2 | Erro ocorre ao registrar na auditoria (passo 29) |
| FE10.3 | Sistema executa rollback de toda a transação |
| FE10.4 | Cargo NÃO é inativado (auditoria é obrigatória) |
| FE10.5 | Sistema retorna HTTP 500 Internal Server Error |
| FE10.6 | Sistema registra erro crítico no log |
| FE10.7 | Sistema envia alerta para equipe técnica |
| FE10.8 | Frontend exibe mensagem: "Erro ao registrar auditoria. Operação cancelada." |

---

## 5. Regras de Negócio

### RN-CAD-009-01: Não Inativar Cargo com Consumidores Ativos

**Descrição**: Um cargo NÃO pode ser inativado se possuir consumidores (colaboradores) ativos associados. Esta é a regra de negócio mais importante deste caso de uso.

**Criticidade**: CRÍTICA

**Implementação**:
- Validação no frontend antes de abrir modal
- Validação no backend antes de UPDATE (double-check)
- Query: `SELECT COUNT(*) FROM Consumidor WHERE Id_Cargo = @Id AND Fl_Ativo = 1`
- Se COUNT > 0, bloquear inativação

**Teste**:
- Criar cargo e atribuir a 3 consumidores ativos
- Tentar inativar cargo
- Verificar que erro é retornado com mensagem clara
- Reatribuir consumidores para outro cargo
- Tentar inativar novamente (deve funcionar)

### RN-CAD-009-02: Soft Delete (Exclusão Lógica)

**Descrição**: Cargos NUNCA são deletados fisicamente do banco. Inativação define Fl_Ativo = 0 mas preserva todos os dados.

**Criticidade**: CRÍTICA

**Implementação**:
- UPDATE em vez de DELETE
- SET Fl_Ativo = 0, Dt_Inativacao = NOW(), Id_Usuario_Inativacao = @IdUsuario
- Dados históricos preservados: nome, código, salários, relacionamentos
- Compliance: LGPD permite manter dados para fins de auditoria

**Teste**:
- Inativar cargo e verificar que registro ainda existe no banco
- Verificar que campos de auditoria foram preenchidos
- Verificar que dados originais estão intactos

### RN-CAD-009-03: Isolamento Multi-tenant

**Descrição**: Usuário só pode inativar cargos do seu próprio conglomerado.

**Criticidade**: CRÍTICA

**Implementação**:
- WHERE clause sempre inclui: AND Id_Conglomerado = @IdConglomerado
- Validação no middleware
- Tentativas suspeitas são alertadas

**Teste**:
- Usuário do conglomerado A tenta inativar cargo do conglomerado B
- Verificar que 404 é retornado e alerta é gerado

### RN-CAD-009-04: Permissão Específica Obrigatória

**Descrição**: Usuário deve ter permissão `cadastros:cargo:delete` para inativar cargos. Esta é permissão mais restritiva que `read` ou `update`.

**Criticidade**: ALTA

**Implementação**:
- Validação em middleware de autorização
- Botão "Inativar" só aparece na UI se usuário tem permissão
- Backend valida novamente (não confia no frontend)

**Teste**:
- Usuário com apenas `cargo:read` não vê botão "Inativar"
- Usuário com `cargo:delete` vê botão e pode inativar

### RN-CAD-009-05: Auditoria Obrigatória

**Descrição**: Toda inativação DEVE ser registrada na auditoria com: usuário responsável, data/hora, motivo (se fornecido), dados completos do cargo.

**Criticidade**: ALTA

**Implementação**:
- INSERT INTO AuditLog dentro da mesma transação
- Se auditoria falhar, rollback de tudo (inativação também falha)
- Registro inclui snapshot completo do cargo

**Teste**:
- Inativar cargo e verificar registro na auditoria
- Verificar que dados estão completos e corretos

### RN-CAD-009-06: Motivo de Inativação (Opcional mas Recomendado)

**Descrição**: Sistema permite (mas não obriga) usuário a fornecer motivo da inativação. Motivo é armazenado e exibido em histórico.

**Criticidade**: MÉDIA

**Implementação**:
- Campo opcional no modal: "Motivo da inativação"
- Armazenado em coluna Motivo_Inativacao (varchar(500), nullable)
- Exibido em: auditoria, histórico, visualização de cargo inativo

**Teste**:
- Inativar sem motivo (deve funcionar)
- Inativar com motivo "Cargo descontinuado" (motivo deve ser salvo)
- Visualizar cargo inativo e verificar que motivo aparece

### RN-CAD-009-07: Cargos Inativos Não Aparecem em Listagens Padrão

**Descrição**: Após inativação, cargo não aparece em listagens padrão nem em dropdowns de seleção. Apenas usuários com permissão especial conseguem visualizar inativos.

**Criticidade**: ALTA

**Implementação**:
- Query padrão: WHERE Fl_Ativo = 1
- Filtro especial: "Exibir Inativos" (requer permissão `cargo:view_inactive`)
- Dropdowns de seleção NUNCA incluem inativos

**Teste**:
- Inativar cargo e verificar que sumiu da listagem
- Ativar filtro "Exibir Inativos" (com permissão adequada)
- Verificar que cargo inativo aparece com badge "INATIVO"

### RN-CAD-009-08: Invalidação de Cache

**Descrição**: Após inativação, cache de listagem e visualização deve ser invalidado.

**Criticidade**: MÉDIA

**Implementação**:
- Cache.Remove("cargo_list_" + Id_Conglomerado + "*")
- Cache.Remove("cargo_detail_" + Id)

**Teste**:
- Inativar cargo e listar imediatamente
- Verificar que cargo não aparece mais (cache foi invalidado)

### RN-CAD-009-09: Ajuste de Hierarquia (Subordinados)

**Descrição**: Se cargo inativado possui subordinados, estes têm Id_Cargo_Superior definido como NULL (tornam-se raiz).

**Criticidade**: MÉDIA

**Implementação**:
- Antes de inativar, sistema identifica subordinados
- UPDATE Cargo SET Id_Cargo_Superior = NULL WHERE Id_Cargo_Superior = @IdCargoInativado
- Operação dentro da mesma transação
- Ajuste é registrado na auditoria

**Teste**:
- Criar hierarquia: A > B > C
- Inativar B
- Verificar que C agora é raiz (Id_Cargo_Superior = NULL)

### RN-CAD-009-10: Impossível Inativar Cargo Já Inativo

**Descrição**: Sistema valida que cargo está ativo antes de permitir inativação.

**Criticidade**: BAIXA

**Implementação**:
- Validação: IF Fl_Ativo = 0 THEN retornar erro
- Mensagem clara: "Este cargo já está inativo"

**Teste**:
- Inativar cargo pela primeira vez (sucesso)
- Tentar inativar novamente (erro)

### RN-CAD-009-11: Preservação de Relacionamentos

**Descrição**: Relacionamentos do cargo (competências, benefícios) são preservados mesmo após inativação.

**Criticidade**: MÉDIA

**Implementação**:
- Relacionamentos N:N permanecem intactos no banco
- Dados históricos completos para auditoria
- Não há DELETE em tabelas de relacionamento

**Teste**:
- Inativar cargo com 5 competências
- Query direta no banco: verificar que 5 relacionamentos existem
- Reativar cargo e verificar que competências voltam automaticamente

### RN-CAD-009-12: Notificação de Inativação (Configurável)

**Descrição**: Sistema pode enviar notificações quando cargo é inativado (se configurado por conglomerado).

**Criticidade**: BAIXA

**Implementação**:
- Após commit bem-sucedido, sistema verifica configuração
- Se notificações ativadas, envia para: RH, gestores, administradores
- Notificação assíncrona (não bloqueia operação)

**Teste**:
- Ativar notificações nas configurações
- Inativar cargo
- Verificar que email/notificação foi enviada (se configurado)

---

## 6. Especificação de Testes

### 6.1. Cenários de Teste Backend

| ID | Cenário | Tipo | Prioridade |
|----|---------|------|------------|
| CN-UC04-001 | Inativar cargo sem consumidores com sucesso | Positivo | Alta |
| CN-UC04-002 | Inativar cargo fornecendo motivo | Positivo | Média |
| CN-UC04-003 | Inativar cargo com subordinados (ajuste hierarquia) | Positivo | Média |
| CN-UC04-004 | Tentar inativar cargo com consumidores ativos | Negativo | Crítica |
| CN-UC04-005 | Tentar inativar cargo já inativo | Negativo | Média |
| CN-UC04-006 | Tentar inativar cargo sem permissão | Negativo | Alta |
| CN-UC04-007 | Tentar inativar cargo de outro conglomerado | Segurança | Crítica |
| CN-UC04-008 | Verificar soft delete (dados preservados) | Validação | Alta |
| CN-UC04-009 | Verificar auditoria de inativação | Auditoria | Alta |
| CN-UC04-010 | Verificar invalidação de cache | Performance | Média |
| CN-UC04-011 | Race condition: consumidor adicionado durante processo | Concorrência | Alta |
| CN-UC04-012 | Inativação em lote (múltiplos cargos) | Funcional | Média |

### 6.2. Casos de Teste Sistema (E2E)

| ID | Caso de Teste | Tipo | Prioridade |
|----|---------------|------|------------|
| TC-UC04-001 | Clicar em "Inativar" e confirmar no modal | Funcional | Alta |
| TC-UC04-002 | Tentar inativar cargo com consumidores (bloqueio) | Funcional | Crítica |
| TC-UC04-003 | Cancelar inativação no modal | Funcional | Média |
| TC-UC04-004 | Inativar com motivo detalhado | Funcional | Baixa |
| TC-UC04-005 | Verificar que cargo sumiu da listagem após inativar | Funcional | Alta |
| TC-UC04-006 | Reativar cargo inativo | Funcional | Média |

### 6.3. Testes de Performance

| ID | Teste | Meta | Prioridade |
|----|-------|------|------------|
| PERF-UC04-001 | Tempo de resposta para inativação | < 2s | Alta |
| PERF-UC04-002 | Inativação em lote (10 cargos) | < 5s | Média |

---

## 7. Matriz de Permissões

| Permissão | Pode Inativar | Vê Botão Inativar | Pode Reativar | Vê Cargos Inativos |
|-----------|--------------|-------------------|---------------|-------------------|
| `cadastros:cargo:read` | ❌ Não | ❌ Não | ❌ Não | ❌ Não |
| `cadastros:cargo:delete` | ✅ Sim | ✅ Sim | ❌ Não | ❌ Não |
| `cadastros:cargo:reactivate` | ✅ Sim | ✅ Sim | ✅ Sim | ✅ Sim |
| `cadastros:cargo:admin` | ✅ Sim | ✅ Sim | ✅ Sim | ✅ Sim |

---

## 8. Casos de Teste Detalhados

### CT-001: Inativar Cargo Sem Consumidores (Sucesso)

**Pré-condições**:
- Usuário autenticado com permissão `cadastros:cargo:delete`
- Existe cargo "ANALISTA_TI_JUNIOR" (Id=15)
- Cargo está ativo (Fl_Ativo = 1)
- Cargo tem 0 consumidores ativos

**Dados de Entrada**:
- ID do cargo: 15
- Motivo (opcional): "Cargo descontinuado"

**Passos**:
1. Fazer requisição DELETE para `/api/v1/cadastros/cargos/15`
2. Body: `{"motivo": "Cargo descontinuado"}`
3. Aguardar resposta

**Resultado Esperado**:
- Status: 200 OK
- Cargo atualizado no banco: Fl_Ativo = 0
- Dt_Inativacao preenchido com timestamp atual
- Id_Usuario_Inativacao = ID do usuário autenticado
- Motivo_Inativacao = "Cargo descontinuado"
- Registro na auditoria criado
- Cache invalidado
- Cargo não aparece mais em GET `/api/v1/cadastros/cargos` (listagem padrão)
- Toast de sucesso exibido no frontend

### CT-002: Tentar Inativar Cargo com Consumidores Ativos (Bloqueio)

**Pré-condições**:
- Usuário autenticado com permissão `cadastros:cargo:delete`
- Existe cargo "GERENTE_TI" (Id=5)
- Cargo tem 3 consumidores ativos

**Dados de Entrada**:
- ID do cargo: 5

**Passos**:
1. Fazer requisição DELETE para `/api/v1/cadastros/cargos/5`
2. Aguardar resposta

**Resultado Esperado**:
- Status: 400 Bad Request
- Body contém mensagem: "Não é possível inativar cargo com consumidores ativos"
- Body contém detalhes: `{"totalConsumidoresAtivos": 3}`
- Body contém lista de consumidores (opcional, para exibir no frontend)
- Nenhuma alteração no banco (Fl_Ativo continua = 1)
- Tentativa registrada na auditoria
- Frontend exibe modal de erro listando os 3 consumidores
- Frontend oferece ação: "Ver Consumidores" (link para página filtrada)

### CT-003: Inativar Cargo com Subordinados

**Pré-condições**:
- Usuário autenticado com permissão `cadastros:cargo:delete`
- Hierarquia: GERENTE_SENIOR (Id=10) > GERENTE_PLENO (Id=20) > GERENTE_JUNIOR (Id=30)
- Queremos inativar GERENTE_PLENO (Id=20)
- GERENTE_PLENO tem 0 consumidores ativos

**Dados de Entrada**:
- ID do cargo: 20

**Passos**:
1. Fazer requisição DELETE para `/api/v1/cadastros/cargos/20`
2. Aguardar resposta
3. Query para verificar subordinados: `SELECT Id_Cargo_Superior FROM Cargo WHERE Id = 30`

**Resultado Esperado**:
- Status: 200 OK
- GERENTE_PLENO (Id=20) inativado: Fl_Ativo = 0
- GERENTE_JUNIOR (Id=30) ajustado: Id_Cargo_Superior = NULL (agora é raiz)
- Auditoria registra ambas as operações:  1. Inativação de GERENTE_PLENO  2. Ajuste de hierarquia de GERENTE_JUNIOR
- GERENTE_SENIOR (Id=10) não é afetado
- Cache invalidado

### CT-004: Tentar Inativar Cargo Já Inativo

**Pré-condições**:
- Usuário autenticado com permissão `cadastros:cargo:delete`
- Cargo "CARGO_ANTIGO" (Id=100) está inativo (Fl_Ativo = 0)

**Dados de Entrada**:
- ID do cargo: 100

**Passos**:
1. Fazer requisição DELETE para `/api/v1/cadastros/cargos/100`
2. Aguardar resposta

**Resultado Esperado**:
- Status: 400 Bad Request
- Body contém mensagem: "Este cargo já está inativo"
- Body contém detalhes da inativação original:  - Data: quando foi inativado  - Por quem: usuário responsável  - Motivo: se foi fornecido
- Nenhuma alteração no banco
- Frontend exibe mensagem informativa
- Frontend oferece botão "Reativar" (se usuário tem permissão)

### CT-005: Race Condition - Consumidor Adicionado Durante Processo

**Pré-condições**:
- Cargo "ANALISTA_DADOS" (Id=50) com 0 consumidores
- Dois processos simultâneos:  - Usuário A: inativando cargo  - Usuário B: atribuindo cargo a consumidor

**Passos**:
1. Usuário A inicia processo de inativação (validação inicial: 0 consumidores)
2. Durante processo, Usuário B atribui cargo a 1 consumidor
3. Sistema de Usuário A tenta executar UPDATE para inativar

**Resultado Esperado**:
- Sistema de Usuário A executa validação final antes de UPDATE
- Detecta 1 consumidor ativo agora (race condition)
- Rollback automático
- Status: 409 Conflict
- Mensagem: "Consumidor foi atribuído a este cargo durante o processo"
- Cargo NÃO é inativado
- Frontend de Usuário A exibe erro e oferece "Recarregar Dados"

### CT-006: Verificar Soft Delete (Dados Preservados)

**Pré-condições**:
- Cargo "TESTE_SOFTDELETE" (Id=99) com:  - 3 competências associadas  - 2 benefícios associados  - Histórico de 5 alterações na auditoria

**Dados de Entrada**:
- ID do cargo: 99

**Passos**:
1. Anotar dados completos do cargo ANTES da inativação
2. Fazer requisição DELETE para `/api/v1/cadastros/cargos/99`
3. Query direta no banco: `SELECT * FROM Cargo WHERE Id = 99`
4. Query relacionamentos: `SELECT * FROM Cargo_Competencia WHERE Id_Cargo = 99`
5. Query auditoria: `SELECT * FROM AuditLog WHERE Entidade='Cargo' AND Id_Registro=99`

**Resultado Esperado**:
- Registro do cargo EXISTE no banco (não foi deletado fisicamente)
- Fl_Ativo = 0 (inativo)
- Dt_Inativacao preenchido
- Todos os outros campos intactos: nome, código, salários, descrição
- Relacionamentos preservados: 3 linhas em Cargo_Competencia, 2 em Cargo_Beneficio
- Auditoria preservada: 5 registros históricos + 1 novo (inativação)
- Compliance: dados disponíveis para auditoria e análises históricas

---

## 9. Notas Técnicas

### 9.1. Endpoint da API

```
DELETE /api/v1/cadastros/cargos/{id}
```

### 9.2. Estrutura do Request Body (Opcional)

```json
{
  "motivo": "string (optional, max 500 chars)"
}
```

### 9.3. Estrutura do Response

**Sucesso (200 OK)**:
```json
{
  "message": "Cargo inativado com sucesso",
  "cargo": {
    "id": 15,
    "codigo": "ANALISTA_TI_JUNIOR",
    "nome": "Analista de TI Júnior",
    "flAtivo": 0,
    "dtInativacao": "2025-11-04T15:30:00Z",
    "usuarioInativacao": {
      "id": 10,
      "nome": "João Silva"
    },
    "motivoInativacao": "Cargo descontinuado"
  }
}
```

**Erro - Cargo com Consumidores (400 Bad Request)**:
```json
{
  "type": "BusinessRuleViolation",
  "title": "Não é possível inativar cargo",
  "status": 400,
  "message": "Não é possível inativar cargo com consumidores ativos",
  "details": {
    "totalConsumidoresAtivos": 3,
    "consumidores": [
      {"id": 100, "nome": "Maria Santos", "matricula": "12345"},
      {"id": 101, "nome": "Pedro Oliveira", "matricula": "12346"},
      {"id": 102, "nome": "Ana Silva", "matricula": "12347"}
    ]
  },
  "suggestedActions": [
    "Reatribua os consumidores para outro cargo",
    "Ou inative os consumidores primeiro"
  ],
  "traceId": "00-abc123-def456-01"
}
```

---

## 10. Histórico de Alterações

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 1.0 | 2025-01-10 | Equipe IControlIT | Versão inicial |
| 2.0 | 2025-11-04 | Equipe IControlIT | Adequação ao padrão de documentação completo |

---

**Revisado por**: Equipe de Arquitetura
**Aprovado por**: Product Owner
**Data de Aprovação**: 2025-11-04

---

# UC06 - Registrar Manutenção de Ativo

**RF**: RF-022 - Gestão de Ativos
**Complexidade**: Média
**Estimativa**: 6h Backend + 5h Frontend

---

## 📋 Objetivo

Registrar entrada/saída de ativo em manutenção com OS (Ordem de Serviço), fornecedor, prazos, custos e controle de SLA.

---

## 📝 Fluxo Principal

**Abertura de OS**:
1. Usuário acessa ativo com status "Alocado" ou "Disponível"
2. Clica "Enviar para Manutenção" (🔧)
3. Modal Ordem de Serviço (OS):
   - **Número OS**: `OS-2025-0042` (gerado automático)
   - **Tipo Manutenção***: [Preventiva ▼] ou Corretiva/Garantia/Upgrade
   - **Problema Relatado***: Descrição detalhada (min 20 chars)
   - **Fornecedor/Técnico***: [Dell Assistência Técnica ▼]
   - **Data Entrada***: `20/01/2025` (default hoje)
   - **Prazo Previsto**: `27/01/2025` (7 dias úteis)
   - **Custo Estimado**: R$ `850,00`
   - **Garantia**: ☑ Coberto por garantia (zera custo se marcado)
   - **Número Protocolo**: `DELL-123456789` (do fornecedor)
   - **Anexos**: [📎 Upload orçamento, fotos do defeito]
4. Sistema atualiza Status="Manutencao" e cria registro em Ativo_Ordem_Servico

**Conclusão da Manutenção**:
1. Técnico/Admin acessa OS-2025-0042
2. Clica "Concluir Manutenção"
3. Preenche:
   - **Data Retorno***: `25/01/2025`
   - **Serviço Realizado***: Descrição do que foi feito
   - **Custo Real***: R$ `0,00` (coberto por garantia)
   - **Status Final***: Disponível / Alocado / Baixa
4. Sistema atualiza ativo e fecha OS

---

## 📐 Regras de Negócio

- **RN-UC06-001**: Ativo em manutenção não pode ser alocado
- **RN-UC06-002**: Prazo vencido (>Prazo Previsto) gera alerta diário
- **RN-UC06-003**: Custo > R$ 50% do valor atual → Sugerir baixa
- **RN-UC06-004**: Garantia zera custo automaticamente
- **RN-UC06-005**: Dashboard de OSs abertas/atrasadas (gestão)

---

---

# UC08 - Inventário Mobile com GPS

**RF**: RF-022 - Gestão de Ativos
**Complexidade**: Alta
**Estimativa**: 12h Backend + 14h Frontend + 8h Mobile

---

## 📋 Objetivo

App mobile (Android/iOS) para inventário físico com leitura de QR Code, captura GPS e modo offline-first.

---

## 📝 Fluxo Principal

1. Usuário abre app mobile "IControlIT Inventário"
2. Login com credenciais corporativas (JWT)
3. Dashboard mobile:
   - Total de ativos cadastrados: 1.245
   - Inventariados hoje: 87 (7%)
   - Pendentes: 1.158
   - Divergências: 3
4. Clica "Iniciar Inventário"
5. Sistema solicita permissões: Câmera, GPS, Armazenamento
6. Usuário escaneia QR Code do ativo
7. App decodifica QR e faz GET para API
8. API retorna dados do ativo (número patrimônio, tipo, modelo, status, responsável)
9. App exibe tela de conferência:
   - **Status no Sistema**: Alocado / João Silva / Edifício A
   - **Situação Encontrada**:
     - Responsável: [João Silva ▼] ✅
     - Local: [Ed. A - Sala 201 ▼] ✅
     - Estado: [Bom ▼]
   - **GPS Capturado**: Lat: -23.550520 / Long: -46.633308 / ±5m ✅
   - **Foto** (opcional): [📷 Tirar Foto]
   - **Situação**: ⚫ Conforme (OK) / ⚪ Divergência
10. Usuário valida e clica "Registrar ✅"
11. App envia para API (com modo offline-first se sem internet)
12. Sistema registra em Ativo_Inventario e atualiza Data_Ultimo_Inventario

**Divergências detectadas**:
- Se Responsável diverge → Notifica gestor
- Se Status = "Baixado" mas encontrado → Alerta crítico

**Modo Offline**:
- App armazena dados localmente (SQLite mobile)
- Sincroniza quando houver internet (queue)
- Indicador visual: 🔵 Online | 🔴 Offline | ⏳ Sincronizando

---

## 📐 Regras de Negócio

- **RN-UC08-001**: GPS obrigatório com precisão ≤ 20m
- **RN-UC08-002**: Divergências geram notificação automática
- **RN-UC08-003**: Modo offline armazena até 500 registros localmente
- **RN-UC08-004**: Sincronização automática a cada 5 minutos (se online)
- **RN-UC08-005**: Relatório de inventário exportável (Excel, PDF)
- **RN-UC08-006**: Dashboard de progresso em tempo real (SignalR)

---

## 🔍 Tecnologias Mobile

- **Framework**: .NET MAUI (Android + iOS)
- **QR Code**: ZXing.Net.Maui
- **GPS**: Xamarin.Essentials.Geolocation
- **Câmera**: Microsoft.Maui.Controls.Camera
- **Offline**: SQLite-net-pcl
- **API**: HttpClient com Polly (retry)

---

---

# UC09 - Visualizar/Imprimir QR Code

**RF**: RF-022 - Gestão de Ativos
**Complexidade**: Média
**Estimativa**: 5h Backend + 6h Frontend

---

## 📋 Objetivo

Visualizar, reimprimir, baixar QR Code de ativos para etiquetagem física com suporte a impressoras Zebra.

---

## 📝 Fluxo Principal

1. Usuário acessa ativo PAT-NB-2025-0012
2. Clica "QR Code" (📱)
3. Modal QR Code:
   - **Visualização**: QR Code 300x300px centralizado
   - **Informações**:
     ```
     Número Patrimônio: PAT-NB-2025-0012
     Ativo: Dell Inspiron 15 (Notebook)
     Número Série: SN123456789ABC
     URL: https://api.icontrolit.com.br/ativos/qr/{Guid}
     Gerado em: 20/01/2025 14:32
     ```
   - **Formato de Impressão**:
     - ⚫ Etiqueta 30x30mm (zebra printer)
     - ⚪ A4 com 24 etiquetas (Pimaco A4360)
     - ⚪ A4 individual (grande)
   - **Opções**:
     - [⬇️ Baixar PNG] - Imagem 300x300px
     - [⬇️ Baixar PDF] - Pronto para impressão
     - [🖨️ Imprimir] - Direto para impressora
     - [🔄 Regenerar] - Gera novo QR (caso danificado)

**Ações disponíveis**:

**1. Baixar PNG**: Request `GET /api/v1/ativos/{id}/qrcode?format=png&size=300`

**2. Baixar PDF**: Sistema gera PDF A4 com layout completo (QR + Dados)

**3. Imprimir Etiqueta Zebra**: Gera ZPL (Zebra Programming Language) e envia para impressora de rede

**4. Regenerar QR Code**: Gera novo GUID, invalida QR antigo, registra em auditoria

**Impressão em Lote**:
- Usuário seleciona múltiplos ativos (checkbox)
- Clica "Imprimir QR Codes em Lote"
- Sistema gera PDF A4 com grid 4x6 (24 etiquetas por folha)
- Limitado a 100 ativos por vez

---

## 📐 Regras de Negócio

- **RN-UC09-001**: QR Code gerado com QRCoder .NET, correção High (30%)
- **RN-UC09-002**: URL pública acessível sem autenticação (redireciona para login)
- **RN-UC09-003**: Regeneração invalida QR antigo mas mantém histórico
- **RN-UC09-004**: Impressão em lote limitada a 100 ativos por vez
- **RN-UC09-005**: Layout PDF configurável por empresa (template personalizado)

---

---

# UC10 - Calcular Depreciação Automática

**RF**: RF-022 - Gestão de Ativos
**Complexidade**: Alta
**Estimativa**: 8h Backend + 4h Frontend

---

## 📋 Objetivo

Calcular depreciação automática mensal com 3 métodos (Linear, Acelerada, Soma de Dígitos) via job Hangfire.

---

## 📝 Fluxo Automático (Job Hangfire Mensal)

1. Job executa dia 1 de cada mês às 03:00 AM
2. Query ativos ativos (Fl_Ativo = 1, Status != 'Baixado')
3. Para cada ativo, calcula depreciação conforme método:

**Método 1: Linear** (padrão, 80% dos ativos):
```csharp
decimal CalcularDepreciacaoLinear(
    decimal valorAquisicao,
    DateTime dataAquisicao,
    decimal taxaAnual,  // Ex: 20% = 0.20
    decimal valorResidual
) {
    var mesesPassados = (DateTime.Now - dataAquisicao).Days / 30;
    var taxaMensal = taxaAnual / 12;  // 20% / 12 = 1.67% ao mês
    var depreciacaoTotal = (valorAquisicao - valorResidual) * taxaMensal * mesesPassados;

    var valorAtual = valorAquisicao - depreciacaoTotal;
    return Math.Max(valorAtual, valorResidual);  // Nunca menor que residual
}
```

**Método 2: Acelerada** (depreciação maior nos primeiros anos):
```csharp
// Tabela acelerada: Ano 1: 40%, Ano 2: 30%, Ano 3: 20%, Ano 4: 10%
```

**Método 3: Soma de Dígitos** (progressivo decrescente):
```csharp
// Soma dos dígitos: 5 anos = 5+4+3+2+1 = 15
// Ano 1: (valorAquisicao - residual) * 5/15
// Ano 2: (valorAquisicao - residual) * 4/15
```

4. Atualiza `Ativo.Valor_Atual_Depreciado`
5. Cria histórico `Ativo_Historico_Depreciacao`
6. Gera relatório mensal

**Consulta Manual (UC)**:
- Usuário acessa ativo e clica "Ver Depreciação" (📉)
- Modal exibe: Método, Valor Aquisição, Depreciação Acumulada, Valor Atual
- Gráfico de projeção (5 anos)
- Botão "Simular Outro Método" permite comparar Linear vs Acelerada vs Soma Dígitos

---

## 📐 Regras de Negócio

- **RN-UC10-001**: Job executa dia 1 do mês às 03:00 AM (Hangfire CRON)
- **RN-UC10-002**: Valor nunca menor que Residual
- **RN-UC10-003**: Histórico mantido por 7 anos (compliance fiscal)
- **RN-UC10-004**: Método configurável por tipo de ativo (default Linear)
- **RN-UC10-005**: Dashboard contábil com total depreciado no mês

---

---

## Histórico de Alterações

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 1.0 | 2025-12-17 | Sistema | Consolidação de 9 casos de uso |
