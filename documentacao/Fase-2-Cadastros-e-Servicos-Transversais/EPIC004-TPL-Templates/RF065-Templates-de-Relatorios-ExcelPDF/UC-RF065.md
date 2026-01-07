# Casos de Uso - RF065: Templates de Relatórios (Excel/PDF)

**Versão:** 2.0
**Data:** 2025-12-31
**Autor:** Agência ALC - alc.dev.br
**Epic:** EPIC004-TPL - Templates
**Fase:** Fase 2 - Cadastros e Serviços Transversais
**RF Relacionado:** [RF065.yaml](./RF065.yaml)

---

## Índice de Casos de Uso

| UC | Nome | Tipo | Complexidade |
|----|------|------|--------------|
| UC00 | Listar Templates de Relatórios | Leitura | Média |
| UC01 | Criar Template de Relatório | CRUD | Muito Alta |
| UC02 | Visualizar Template de Relatório | Leitura | Baixa |
| UC03 | Editar Template de Relatório | CRUD | Alta |
| UC04 | Excluir Template de Relatório | CRUD | Baixa |
| UC05 | Gerar Relatório | Ação | Muito Alta |
| UC06 | Agendar Relatório | Ação | Alta |
| UC07 | Visualizar Métricas de Uso | Leitura | Média |

---

# UC00 - Listar Templates de Relatórios

## Objetivo

Permitir que usuários autenticados visualizem lista paginada de templates de relatórios disponíveis no tenant, com filtros por categoria, formato, status e busca textual.

## Pré-condições

- Usuário autenticado com permissão `TPL.RELATORIOS.VIEW`
- Tenant ativo no sistema

## Pós-condições

- Lista de templates exibida com indicadores visuais de status (draft, active, inactive, archived)
- Filtros aplicados conforme seleção do usuário
- Paginação configurada (50 registros por página)

## Fluxo Principal

**FP-UC00-001:** Usuário acessa a funcionalidade Templates de Relatórios pelo menu
**FP-UC00-002:** Sistema valida permissão TPL.RELATORIOS.VIEW
**FP-UC00-003:** Sistema carrega templates do tenant com filtro de permissão
**FP-UC00-004:** Sistema aplica paginação (50 registros por página)
**FP-UC00-005:** Sistema exibe lista com cards contendo:
- Nome do template
- Categoria
- Formato (Excel/PDF/CSV)
- Status (draft, active, inactive, archived)
- Data última geração
- Quantidade de gerações (métrica de uso)
- Botões de ação (Gerar, Editar, Visualizar, Excluir)

## Fluxos Alternativos

**FA-UC00-001:** Buscar por nome ou categoria
- Usuário digita termo no campo de busca
- Sistema filtra templates por nome ou descrição (contains)
- Lista atualizada em tempo real (debounce 300ms)

**FA-UC00-002:** Filtrar por formato (Excel/PDF/CSV)
- Usuário seleciona formato no dropdown
- Sistema filtra templates pelo FormatoRelatorio
- Lista atualizada

**FA-UC00-003:** Filtrar por status (draft/active/inactive/archived)
- Usuário seleciona status no dropdown
- Sistema filtra templates pelo Status
- Lista atualizada

**FA-UC00-004:** Ordenar por coluna (nome, data criação, quantidade gerações)
- Usuário clica no cabeçalho da coluna
- Sistema ordena ascendente/descendente
- Lista atualizada

## Fluxos de Exceção

**FE-UC00-001:** Usuário sem permissão
- Sistema retorna HTTP 403 Forbidden
- Exibe mensagem: "Você não tem permissão para visualizar templates de relatórios"
- Usuário redirecionado para página anterior

**FE-UC00-002:** Nenhum template encontrado
- Sistema exibe estado vazio: "Nenhum template cadastrado"
- Botão "Criar Novo Template" destacado
- Sugestão: "Comece criando seu primeiro template de relatório"

## Regras de Negócio

**RN-UC00-001:** Multi-tenancy obrigatório
- Sistema DEVE filtrar templates por EmpresaId automaticamente
- Templates de outros tenants não podem ser visualizados

**RN-UC00-002:** Templates arquivados (status=archived) não aparecem na listagem padrão
- Usuário deve marcar checkbox "Exibir Arquivados" para vê-los
- Templates arquivados exibem label visual "ARQUIVADO"

**RN-UC00-003:** Indicador visual de métricas de uso
- Templates com >100 gerações: Badge "Popular"
- Templates não usados em >90 dias: Badge "Inativo"

## Critérios de Aceite

- Lista carrega em <2 segundos
- Filtros aplicados em <500ms
- Paginação funcional (anterior/próxima)
- Busca textual com debounce de 300ms
- Cards responsivos (mobile/tablet/desktop)
- Isolamento de tenant validado (não vaza dados)

---

# UC01 - Criar Template de Relatório

## Objetivo

Criar template de relatório definindo query SQL/MDX, formato de saída (Excel/PDF/CSV), configurações visuais (gráficos Chart.js, agrupamentos, formatação condicional), parâmetros dinâmicos, cabeçalho/rodapé customizados, marca d'água, assinatura digital e proteção de planilhas.

## Pré-condições

- Usuário autenticado com permissão `TPL.RELATORIOS.CREATE`
- Tenant ativo no sistema

## Pós-condições

- Template criado com status "draft"
- Registro em tabela RelatorioTemplate
- Auditoria registrada (CREATE)
- Versionamento inicial (1.0.0) criado

## Fluxo Principal

**FP-UC01-001:** Usuário clica em "Novo Template"
**FP-UC01-002:** Sistema valida permissão TPL.RELATORIOS.CREATE
**FP-UC01-003:** Sistema exibe wizard de criação em 5 passos

**Passo 1 - Dados Básicos:**
**FP-UC01-004:** Usuário preenche:
- Nome do template (3-100 caracteres, único por tenant)
- Descrição (opcional, máx 500 caracteres)
- Categoria (Financeiro, Operacional, Gerencial, Auditoria)
- Formato de saída (Excel, PDF, CSV)
- Status (draft ou active)

**Passo 2 - Query/Dados:**
**FP-UC01-005:** Usuário escolhe fonte de dados:
- SQL Query (padrão)
- MDX Query (OLAP - opcional se RN-RF065-012)

**FP-UC01-006:** Usuário escreve query no editor de código com syntax highlighting
**FP-UC01-007:** Usuário define parâmetros dinâmicos (se RN-RF065-006):
- Nome do parâmetro (@DataInicio, @CentroCustoId)
- Tipo (DATE, TEXT, NUMBER, SELECT)
- Valor padrão
- Obrigatório (true/false)

**FP-UC01-008:** Usuário clica em "Executar Preview"
**FP-UC01-009:** Sistema valida sintaxe SQL/MDX
**FP-UC01-010:** Sistema executa query com parâmetros padrão
**FP-UC01-011:** Sistema retorna primeiras 100 linhas de preview
**FP-UC01-012:** Sistema exibe estrutura de colunas retornadas

**Passo 3 - Configurações Visuais:**
**FP-UC01-013:** Usuário configura gráficos (se RN-RF065-002):
- Adiciona gráfico Chart.js (Linha, Barra, Pizza, Área)
- Define campo X, campo Y, título, cores
- Preview do gráfico renderizado

**FP-UC01-014:** Usuário configura agrupamentos (se RN-RF065-003):
- Seleciona campos de agrupamento (1 ou mais)
- Define campos para subtotais (soma, média)
- Preview com agrupamento aplicado

**FP-UC01-015:** Usuário configura formatação condicional (se RN-RF065-004):
- Adiciona regra: campo, operador (>, <, =, BETWEEN), valor
- Define formatação: cor de fundo, cor de texto, negrito
- Preview com formatação aplicada

**FP-UC01-016:** Usuário configura múltiplas abas Excel (se RN-RF065-005 e formato=Excel):
- Adiciona aba: nome (máx 31 caracteres), query SQL independente
- Configura gráficos e agrupamento por aba

**Passo 4 - Layout (PDF/Excel):**
**FP-UC01-017:** Usuário configura cabeçalho (se RN-RF065-008):
- Upload de logo (PNG/JPG, máx 500KB)
- Título do relatório (suporta variáveis: {NomeSistema}, {DataGeracao})
- Subtítulo (opcional)

**FP-UC01-018:** Usuário configura rodapé (se RN-RF065-008):
- Paginação (Página X de Y)
- Timestamp ({Usuario} - {DataGeracao})
- Texto customizado

**FP-UC01-019:** Usuário configura marca d'água em PDF (se RN-RF065-011):
- Texto (máx 30 caracteres)
- Posição (diagonal, horizontal)
- Opacidade (0-100%)
- Cor

**Passo 5 - Segurança:**
**FP-UC01-020:** Usuário configura proteção Excel (se RN-RF065-009 e formato=Excel):
- Habilitar proteção contra edição (somente leitura)
- Senha de proteção (opcional, mín 6 caracteres)

**FP-UC01-021:** Usuário configura assinatura digital PDF (se RN-RF065-010 e formato=PDF):
- Requerer assinatura digital (true/false)
- Sistema valida certificado X.509 configurado
- Timestamp automático
- Hash SHA-256

**FP-UC01-022:** Usuário clica em "Salvar Template"
**FP-UC01-023:** Sistema valida todos os campos obrigatórios
**FP-UC01-024:** Sistema valida unicidade do nome por tenant
**FP-UC01-025:** Sistema valida query SQL/MDX
**FP-UC01-026:** Sistema sanitiza query (prevenir SQL injection - RN-RF065 seg)
**FP-UC01-027:** Sistema valida whitelist de tabelas permitidas
**FP-UC01-028:** Sistema cria registro em RelatorioTemplate
**FP-UC01-029:** Sistema cria versão inicial 1.0.0 em RelatorioTemplateVersao
**FP-UC01-030:** Sistema registra auditoria (CREATE)
**FP-UC01-031:** Sistema exibe mensagem: "Template '[Nome]' criado com sucesso! Versão 1.0.0"
**FP-UC01-032:** Sistema redireciona para visualização do template

## Fluxos Alternativos

**FA-UC01-001:** Importar query de arquivo SQL
- Usuário clica em "Importar SQL"
- Sistema abre dialog de upload
- Usuário seleciona arquivo .sql
- Sistema carrega conteúdo no editor
- Usuário valida e ajusta se necessário

**FA-UC01-002:** Salvar como rascunho (draft)
- Usuário clica em "Salvar Rascunho"
- Sistema salva com status=draft
- Template não aparece para outros usuários
- Usuário pode continuar editando depois

**FA-UC01-003:** Testar parâmetros dinâmicos
- Usuário clica em "Testar Parâmetros"
- Sistema exibe modal com campos de parâmetros
- Usuário preenche valores de teste
- Sistema executa query com valores informados
- Preview atualizado com dados reais

## Fluxos de Exceção

**FE-UC01-001:** Query SQL/MDX inválida
- Sistema retorna HTTP 400 Bad Request
- Exibe mensagem: "Erro de sintaxe na linha [X]: [Mensagem]"
- Editor destaca linha com erro
- Salvamento bloqueado

**FE-UC01-002:** Nome duplicado
- Sistema retorna HTTP 400 Bad Request
- Exibe mensagem: "Já existe um template com o nome '[Nome]' neste tenant"
- Campo nome destacado em vermelho
- Sugestão: "Escolha outro nome ou edite o template existente"

**FE-UC01-003:** Query retorna muitas colunas (>100)
- Sistema exibe aviso (não bloqueia)
- Mensagem: "Query retorna [N] colunas. Excel suporta máx 16.384. Recomendado: <50 colunas para melhor performance."

**FE-UC01-004:** Query muito lenta (>30s)
- Sistema timeout no preview
- Exibe mensagem: "Query demorou >30s. Otimize com índices ou filtre mais dados antes de gerar."

**FE-UC01-005:** Query contém comando perigoso (UPDATE, DELETE, DROP)
- Sistema retorna HTTP 400 Bad Request
- Exibe mensagem: "Query deve começar com SELECT. Comandos UPDATE/DELETE/DROP não são permitidos."
- Salvamento bloqueado

**FE-UC01-006:** Logo muito grande (>500KB)
- Sistema retorna HTTP 413 Payload Too Large
- Exibe mensagem: "Logo deve ter máximo 500KB. Reduza o tamanho da imagem."

**FE-UC01-007:** Certificado X.509 inválido ou expirado (para assinatura PDF)
- Sistema retorna HTTP 400 Bad Request
- Exibe mensagem: "Certificado digital inválido ou expirado. Configure um certificado válido."

**FE-UC01-008:** Nome de aba Excel duplicado
- Sistema retorna HTTP 400 Bad Request
- Exibe mensagem: "Nome da aba '[Nome]' já existe. Nomes de abas devem ser únicos."

## Regras de Negócio

**RN-UC01-001:** Formato de saída obrigatório (RN-RF065-001)
- Sistema DEVE suportar 3 formatos: Excel (.xlsx), PDF, CSV
- Enum FormatoRelatorio {Excel, PDF, CSV}
- Validação obrigatória antes de salvar

**RN-UC01-002:** Gráficos Chart.js (RN-RF065-002)
- Sistema DEVE suportar 4 tipos: Linha, Barra, Pizza, Área
- Cada gráfico tem: tipo, campoX, campoY, título, cores
- Excel exporta gráficos como imagens PNG embebadas

**RN-UC01-003:** Agrupamentos e subtotais (RN-RF065-003)
- Sistema permite agrupar por 1 ou mais campos
- Subtotais calculados: soma, média
- Total geral ao final do relatório

**RN-UC01-004:** Formatação condicional (RN-RF065-004)
- Regras: campo, operador (>, <, =, !=, BETWEEN), valor, formatação
- Formatação aplicada em Excel e PDF
- Múltiplas regras podem coexistir (ordem de prioridade)

**RN-UC01-005:** Múltiplas abas Excel (RN-RF065-005)
- Cada aba: nome (máx 31 chars, único), query SQL independente
- Máximo 10 abas por template
- Navegação entre abas funcional

**RN-UC01-006:** Parâmetros dinâmicos (RN-RF065-006)
- Tipos suportados: DATE, TEXT, NUMBER, SELECT (dropdown)
- Parâmetros obrigatórios bloqueiam geração se não preenchidos
- Valor padrão aplicado automaticamente

**RN-UC01-007:** Cabeçalho e rodapé customizados (RN-RF065-008)
- Header: Logo empresa (PNG/JPG, máx 500KB), título, data geração
- Footer: Página X de Y, usuário, timestamp
- Suporta variáveis: {NomeSistema}, {DataGeracao}, {Usuario}

**RN-UC01-008:** Proteção Excel (RN-RF065-009)
- Planilha bloqueada por padrão (somente leitura)
- Usuário pode filtrar/ordenar mas não editar células
- Senha opcional (mín 6 caracteres)

**RN-UC01-009:** Assinatura digital PDF (RN-RF065-010)
- Certificado X.509 obrigatório
- Timestamp de geração automático
- Hash SHA-256 do documento

**RN-UC01-010:** Marca d'água PDF (RN-RF065-011)
- Texto máx 30 caracteres
- Posição: diagonal ou horizontal
- Opacidade 0-100%
- Aplicada em todas as páginas

**RN-UC01-011:** Consulta OLAP via MDX (RN-RF065-012)
- Flag "Usar OLAP" habilita editor MDX
- Query MDX em vez de SQL
- Validação de sintaxe MDX obrigatória

**RN-UC01-012:** Sanitização de SQL (segurança)
- Sistema DEVE prevenir SQL injection
- Whitelist de tabelas permitidas
- Validação de caracteres especiais
- Parametrização obrigatória

**RN-UC01-013:** Versionamento automático
- Primeira versão: 1.0.0
- Registro em RelatorioTemplateVersao
- Histórico de alterações rastreado

## Critérios de Aceite

- Wizard de 5 passos funcional
- Preview de query com primeiras 100 linhas
- Validação de SQL/MDX em tempo real
- Gráficos Chart.js renderizados corretamente
- Formatação condicional aplicada no preview
- Upload de logo funcional (<500KB)
- Proteção Excel aplicada
- Assinatura PDF com certificado válido
- Multi-tenancy isolado (EmpresaId)
- Auditoria registrada

---

# UC02 - Visualizar Template de Relatório

## Objetivo

Visualizar detalhes completos de um template: query SQL/MDX, configurações visuais, parâmetros, histórico de versões, últimas gerações e métricas de uso.

## Pré-condições

- Usuário autenticado com permissão `TPL.RELATORIOS.VIEW`
- Template existe e pertence ao tenant do usuário

## Pós-condições

- Detalhes do template exibidos em abas organizadas
- Histórico de versões disponível
- Métricas de uso calculadas e exibidas

## Fluxo Principal

**FP-UC02-001:** Usuário clica em "Visualizar" (ícone olho) em um template da listagem
**FP-UC02-002:** Sistema valida permissão TPL.RELATORIOS.VIEW
**FP-UC02-003:** Sistema valida que template pertence ao tenant do usuário
**FP-UC02-004:** Sistema carrega dados completos do template
**FP-UC02-005:** Sistema exibe tela com 6 abas:

**Aba Detalhes:**
**FP-UC02-006:** Sistema exibe:
- Nome do template
- Descrição
- Categoria
- Formato (Excel/PDF/CSV)
- Status (draft/active/inactive/archived)
- Versão atual
- Data criação
- Última modificação
- Usuário criador

**Aba Query:**
**FP-UC02-007:** Sistema exibe:
- Query SQL/MDX em editor read-only com syntax highlighting
- Botão "Copiar Query"
- Parâmetros definidos (nome, tipo, valor padrão, obrigatório)

**Aba Configurações Visuais:**
**FP-UC02-008:** Sistema exibe:
- Gráficos configurados (tipo, eixos, título, cores)
- Preview dos gráficos com dados de exemplo
- Agrupamentos configurados (campos, subtotais)
- Formatação condicional (regras definidas)
- Múltiplas abas Excel (se aplicável)

**Aba Layout:**
**FP-UC02-009:** Sistema exibe:
- Cabeçalho customizado (logo preview, título)
- Rodapé customizado (paginação, timestamp)
- Marca d'água PDF (se configurada)
- Proteção Excel (se aplicável)
- Assinatura digital PDF (se aplicável)

**Aba Versões:**
**FP-UC02-010:** Sistema exibe histórico de versões:
- Número da versão (1.0.0, 1.1.0, 2.0.0)
- Data da versão
- Usuário que criou a versão
- Mensagem de commit
- Tipo de mudança (Major/Minor/Patch)
- Botão "Ver Diff" para comparar com versão anterior

**Aba Histórico de Gerações:**
**FP-UC02-011:** Sistema exibe últimas 100 gerações:
- Data/hora de geração
- Usuário que gerou
- Formato gerado (Excel/PDF/CSV)
- Tamanho do arquivo
- Tempo de geração (segundos)
- Status (sucesso/falha)
- Link para download (se disponível)

**FP-UC02-012:** Sistema exibe métricas de uso (RN-RF065-015):
- Total de gerações
- Formato mais popular (Excel vs PDF vs CSV)
- Top 5 usuários que mais usam
- Tempo médio de geração
- Horário de pico (hora do dia com mais gerações)

## Fluxos Alternativos

**FA-UC02-001:** Comparar versões (Diff)
- Usuário clica em "Ver Diff" em uma versão
- Sistema exibe modal com comparação lado a lado
- Query anterior vs Query atual
- Configurações alteradas destacadas

**FA-UC02-002:** Gerar relatório de teste
- Usuário clica em "Gerar Agora" na aba Detalhes
- Sistema redireciona para UC05 - Gerar Relatório
- Parâmetros preenchidos com valores padrão

**FA-UC02-003:** Exportar configuração do template
- Usuário clica em "Exportar JSON"
- Sistema gera arquivo JSON com toda configuração
- Download automático do arquivo

## Fluxos de Exceção

**FE-UC02-001:** Template não encontrado
- Sistema retorna HTTP 404 Not Found
- Exibe mensagem: "Template não encontrado"
- Usuário redirecionado para listagem

**FE-UC02-002:** Acesso negado por permissão
- Sistema retorna HTTP 403 Forbidden
- Exibe mensagem: "Você não tem permissão para visualizar este template"

**FE-UC02-003:** Template de outro tenant
- Sistema retorna HTTP 403 Forbidden
- Exibe mensagem: "Template não encontrado" (não vaza informação de existência)

## Regras de Negócio

**RN-UC02-001:** Visualização read-only
- Sistema NÃO permite edição direta na visualização
- Botão "Editar" redireciona para UC03

**RN-UC02-002:** Métricas de uso calculadas (RN-RF065-015)
- Total de gerações: contador em RelatorioExecucao
- Tempo médio: AVG(TempoGeracao) where Status=Sucesso
- Formato mais popular: COUNT() GROUP BY Formato
- Top usuários: COUNT() GROUP BY UsuarioId

**RN-UC02-003:** Histórico limitado a 100 gerações
- Gerações mais recentes aparecem primeiro (ORDER BY DataGeracao DESC)
- Paginação se >100 registros

## Critérios de Aceite

- Todas as 6 abas carregam corretamente
- Query exibida com syntax highlighting
- Gráficos renderizados no preview
- Histórico de versões ordenado
- Métricas de uso calculadas corretamente
- Diff de versões funcional
- Multi-tenancy validado (não vaza dados)

---

# UC03 - Editar Template de Relatório

## Objetivo

Editar template existente modificando query, configurações visuais, parâmetros, layout ou segurança. Cada edição gera nova versão com registro de diff e mensagem de commit.

## Pré-condições

- Usuário autenticado com permissão `TPL.RELATORIOS.UPDATE`
- Template existe e pertence ao tenant do usuário
- Template não está em status "archived"

## Pós-condições

- Template atualizado com nova versão
- Registro de diff em RelatorioTemplateVersao
- Auditoria registrada (UPDATE)
- Mensagem de commit salva

## Fluxo Principal

**FP-UC03-001:** Usuário clica em "Editar" (ícone lápis) em um template
**FP-UC03-002:** Sistema valida permissão TPL.RELATORIOS.UPDATE
**FP-UC03-003:** Sistema valida que template pertence ao tenant do usuário
**FP-UC03-004:** Sistema valida que template não está arquivado (status≠archived)
**FP-UC03-005:** Sistema carrega wizard de edição preenchido com dados atuais
**FP-UC03-006:** Usuário modifica campos desejados em qualquer passo do wizard
**FP-UC03-007:** Sistema permite preview com dados reais a cada modificação
**FP-UC03-008:** Usuário clica em "Salvar Alterações"
**FP-UC03-009:** Sistema exibe modal de versionamento com campos:
- Mensagem de commit (obrigatório, 10-500 caracteres)
- Tipo de mudança (Major/Minor/Patch)
  - Major: mudanças quebram compatibilidade (query alterada significativamente)
  - Minor: novas funcionalidades compatíveis (novos gráficos, formatação)
  - Patch: correções pequenas (typo no título, ajuste de cor)

**FP-UC03-010:** Usuário preenche mensagem de commit e seleciona tipo de mudança
**FP-UC03-011:** Sistema valida campos obrigatórios
**FP-UC03-012:** Sistema valida query SQL/MDX se foi modificada
**FP-UC03-013:** Sistema calcula diff entre versão atual e nova
**FP-UC03-014:** Sistema incrementa versão:
- Major: 1.0.0 → 2.0.0
- Minor: 1.0.0 → 1.1.0
- Patch: 1.0.0 → 1.0.1

**FP-UC03-015:** Sistema cria novo registro em RelatorioTemplateVersao com:
- Número da versão
- Diff JSON
- Mensagem de commit
- Tipo de mudança
- Usuário que editou
- Timestamp

**FP-UC03-016:** Sistema atualiza registro em RelatorioTemplate
**FP-UC03-017:** Sistema registra auditoria (UPDATE)
**FP-UC03-018:** Sistema exibe mensagem: "Template atualizado para versão [X.Y.Z]"
**FP-UC03-019:** Sistema redireciona para visualização do template

## Fluxos Alternativos

**FA-UC03-001:** Preview com dados reais antes de salvar
- Usuário clica em "Preview com Dados Reais"
- Sistema executa query modificada com parâmetros padrão
- Preview atualizado com dados do banco
- Usuário valida resultado antes de salvar

**FA-UC03-002:** Comparar diff antes de salvar
- Usuário clica em "Ver Alterações"
- Sistema exibe modal com diff lado a lado
- Query anterior vs Query nova
- Configurações alteradas destacadas
- Usuário decide se continua ou cancela

**FA-UC03-003:** Reverter para versão anterior
- Usuário clica em "Reverter para Versão X.Y.Z" na aba Versões (UC02)
- Sistema carrega dados da versão selecionada
- Usuário confirma reversão
- Sistema cria nova versão com conteúdo da versão antiga (não deleta histórico)

**FA-UC03-004:** Cancelar edição
- Usuário clica em "Cancelar"
- Sistema exibe confirmação: "Descartar alterações?"
- Se confirmar: redireciona para visualização sem salvar
- Se cancelar: volta para edição

## Fluxos de Exceção

**FE-UC03-001:** Query SQL/MDX inválida
- Sistema retorna HTTP 400 Bad Request
- Exibe mensagem: "Erro de sintaxe na linha [X]: [Mensagem]"
- Salvamento bloqueado

**FE-UC03-002:** Nome duplicado (se foi alterado)
- Sistema retorna HTTP 400 Bad Request
- Exibe mensagem: "Já existe outro template com o nome '[Nome]'"
- Campo nome destacado em vermelho

**FE-UC03-003:** Mensagem de commit vazia ou muito curta
- Sistema retorna HTTP 400 Bad Request
- Exibe mensagem: "Mensagem de commit é obrigatória (mínimo 10 caracteres)"
- Modal de versionamento permanece aberto

**FE-UC03-004:** Template arquivado
- Sistema retorna HTTP 400 Bad Request
- Exibe mensagem: "Templates arquivados não podem ser editados. Crie um novo template."

**FE-UC03-005:** Concorrência (outro usuário editou)
- Sistema retorna HTTP 409 Conflict
- Exibe mensagem: "Este template foi modificado por outro usuário. Atualize a página e tente novamente."

## Regras de Negócio

**RN-UC03-001:** Versionamento automático obrigatório (RN-UC01-013)
- Toda edição DEVE criar nova versão
- Não é permitido editar sem mensagem de commit
- Histórico de versões é imutável (não pode deletar)

**RN-UC03-002:** Multi-tenancy imutável
- NÃO é permitido transferir template entre tenants
- EmpresaId do template permanece fixo
- Validação obrigatória antes de salvar

**RN-UC03-003:** Validação de query ao editar
- Se query foi modificada, validação completa é obrigatória
- Sintaxe SQL/MDX
- Sanitização (SQL injection)
- Whitelist de tabelas
- Timeout de 30s no preview

**RN-UC03-004:** Incremento de versão baseado em tipo de mudança
- Major: mudanças quebram compatibilidade
- Minor: novas funcionalidades compatíveis
- Patch: correções pequenas

**RN-UC03-005:** Templates em uso podem ser editados
- Sistema NÃO bloqueia edição de templates ativos
- Agendamentos continuam usando nova versão automaticamente
- Aviso exibido: "Este template está em uso por [N] agendamentos. Alterações afetarão próximas gerações."

## Critérios de Aceite

- Wizard de edição preenchido com dados atuais
- Modal de versionamento obrigatório
- Diff calculado corretamente
- Versão incrementada conforme tipo de mudança
- Query validada antes de salvar
- Auditoria registrada
- Multi-tenancy validado

---

# UC04 - Excluir Template de Relatório

## Objetivo

Excluir template (soft delete) não mais utilizado, impedindo geração de novos relatórios mas preservando histórico de gerações e auditoria.

## Pré-condições

- Usuário autenticado com permissão `TPL.RELATORIOS.DELETE`
- Template existe e pertence ao tenant do usuário
- Template não está em status "archived"

## Pós-condições

- Template marcado como deletado (soft delete - Fl_Deletado=1)
- Agendamentos vinculados desativados
- Histórico de gerações preservado
- Auditoria registrada (DELETE)
- Template não aparece mais em listagens

## Fluxo Principal

**FP-UC04-001:** Usuário clica em "Excluir" (ícone lixeira) em um template
**FP-UC04-002:** Sistema valida permissão TPL.RELATORIOS.DELETE
**FP-UC04-003:** Sistema valida que template pertence ao tenant do usuário
**FP-UC04-004:** Sistema verifica se template possui agendamentos ativos
**FP-UC04-005:** Sistema exibe modal de confirmação com detalhes:
- "Tem certeza que deseja excluir '[Nome do Template]'?"
- Se tem agendamentos: "ATENÇÃO: Este template está vinculado a [N] agendamento(s) ativo(s). Todos serão desativados."
- Checkbox: "Confirmo que desejo excluir este template"
- Botões: [Cancelar] [Excluir]

**FP-UC04-006:** Usuário marca checkbox e clica em "Excluir"
**FP-UC04-007:** Sistema marca Fl_Deletado=1 em RelatorioTemplate (soft delete)
**FP-UC04-008:** Sistema desativa agendamentos vinculados (se existirem)
**FP-UC04-009:** Sistema registra auditoria (DELETE) com:
- TemplateId
- UsuarioId
- Timestamp
- Quantidade de agendamentos desativados

**FP-UC04-010:** Sistema exibe mensagem: "Template '[Nome]' excluído com sucesso"
**FP-UC04-011:** Sistema redireciona para listagem de templates

## Fluxos Alternativos

**FA-UC04-001:** Reativar template excluído
- Administrador acessa listagem com filtro "Exibir Excluídos"
- Clica em "Reativar" em template excluído
- Sistema marca Fl_Deletado=0
- Template volta para listagem normal
- Agendamentos NÃO são reativados automaticamente (usuário deve configurar novamente)

**FA-UC04-002:** Arquivar em vez de excluir
- Usuário clica em "Arquivar"
- Sistema muda status para "archived"
- Template não aparece em listagens
- Histórico preservado
- Pode ser reativado mudando status para "active"

## Fluxos de Exceção

**FE-UC04-001:** Template não encontrado
- Sistema retorna HTTP 404 Not Found
- Exibe mensagem: "Template não encontrado"

**FE-UC04-002:** Acesso negado por permissão
- Sistema retorna HTTP 403 Forbidden
- Exibe mensagem: "Você não tem permissão para excluir templates"

**FE-UC04-003:** Template já excluído
- Sistema retorna HTTP 400 Bad Request
- Exibe mensagem: "Este template já foi excluído"

**FE-UC04-004:** Template de outro tenant
- Sistema retorna HTTP 403 Forbidden
- Exibe mensagem: "Template não encontrado"

## Regras de Negócio

**RN-UC04-001:** Soft delete obrigatório
- Sistema NUNCA deleta fisicamente (DELETE FROM)
- Sempre usa Fl_Deletado=1
- Preserva histórico de gerações
- Preserva versionamento
- Preserva auditoria

**RN-UC04-002:** Templates excluídos não podem gerar novos relatórios
- Endpoint de geração bloqueia se Fl_Deletado=1
- Exibe mensagem: "Template não disponível"

**RN-UC04-003:** Agendamentos vinculados devem ser desativados
- Sistema marca agendamentos como Ativo=0
- Hangfire Job não executa mais
- Usuário recebe notificação por e-mail

**RN-UC04-004:** Templates arquivados NÃO podem ser excluídos
- Sistema bloqueia exclusão se status=archived
- Exibe mensagem: "Templates arquivados não podem ser excluídos. Reative primeiro."

## Critérios de Aceite

- Modal de confirmação obrigatório
- Soft delete aplicado (Fl_Deletado=1)
- Agendamentos desativados automaticamente
- Histórico preservado
- Auditoria registrada
- Template não aparece em listagens
- Reativação funcional (para administradores)

---

# UC05 - Gerar Relatório

## Objetivo

Gerar relatório a partir de template configurado, aplicando parâmetros dinâmicos, executando query, aplicando formatação condicional, gráficos, agrupamentos e exportando em formato selecionado (Excel/PDF/CSV) com proteção e assinatura (se aplicável).

## Pré-condições

- Usuário autenticado com permissão `TPL.RELATORIOS.GENERATE`
- Template existe, está ativo e pertence ao tenant do usuário
- Template não está excluído (Fl_Deletado=0)

## Pós-condições

- Relatório gerado e disponível para download
- Arquivo armazenado no Azure Blob Storage
- Registro de execução em RelatorioExecucao
- Auditoria registrada
- Métricas de uso atualizadas
- Cache criado (se relatório pesado - RN-RF065-013)

## Fluxo Principal

**FP-UC05-001:** Usuário clica em "Gerar Relatório" em um template
**FP-UC05-002:** Sistema valida permissão TPL.RELATORIOS.GENERATE
**FP-UC05-003:** Sistema valida que template está ativo (Fl_Deletado=0, Status=active)
**FP-UC05-004:** Sistema verifica se template possui parâmetros obrigatórios (RN-RF065-006)
**FP-UC05-005:** Se sim, sistema exibe modal com campos de parâmetros:
- Nome do parâmetro
- Tipo (DATE picker, TEXT input, NUMBER input, SELECT dropdown)
- Valor padrão preenchido
- Indicador de obrigatório (*)

**FP-UC05-006:** Usuário preenche parâmetros obrigatórios
**FP-UC05-007:** Usuário clica em "Gerar"
**FP-UC05-008:** Sistema valida que parâmetros obrigatórios foram preenchidos
**FP-UC05-009:** Sistema verifica cache Redis (RN-RF065-013):
- Key: TemplateId + Hash(Parâmetros)
- Se existe e TTL válido (<15 min), retorna do cache
- Exibe indicador: "Gerado às HH:MM (cache)" + botão "Regenerar"

**FP-UC05-010:** Se não há cache ou usuário clicou "Regenerar":
**FP-UC05-011:** Sistema executa query SQL/MDX com parâmetros informados
**FP-UC05-012:** Sistema mede tempo de execução da query
**FP-UC05-013:** Sistema aplica agrupamentos e subtotais (RN-RF065-003)
**FP-UC05-014:** Sistema aplica formatação condicional (RN-RF065-004)
**FP-UC05-015:** Sistema gera gráficos Chart.js (RN-RF065-002):
- Frontend renderiza gráficos
- Converte para imagem PNG
- Embeda no Excel/PDF

**FP-UC05-016:** Sistema escolhe gerador conforme formato:
- Excel: EPPlus library
- PDF: QuestPDF library
- CSV: CsvHelper library

**FP-UC05-017:** Sistema aplica configurações de layout:
- Cabeçalho customizado (logo, título, data)
- Rodapé (paginação, usuário, timestamp)
- Marca d'água (se PDF - RN-RF065-011)

**FP-UC05-018:** Sistema aplica segurança:
- Proteção Excel (somente leitura - RN-RF065-009)
- Assinatura digital PDF (certificado X.509 - RN-RF065-010)

**FP-UC05-019:** Sistema gera arquivo final
**FP-UC05-020:** Sistema faz upload para Azure Blob Storage
**FP-UC05-021:** Sistema cria registro em RelatorioExecucao:
- TemplateId
- UsuarioId
- Formato
- Tamanho arquivo (bytes)
- Tempo de geração (segundos)
- Status (Sucesso)
- Parâmetros utilizados (JSON)
- URL Blob Storage

**FP-UC05-022:** Sistema registra auditoria (GENERATE)
**FP-UC05-023:** Sistema atualiza métricas de uso (RN-RF065-015):
- Incrementa contador de gerações
- Atualiza tempo médio
- Atualiza formato mais popular

**FP-UC05-024:** Se relatório pesado (>1000 linhas ou >5s), sistema salva no cache Redis (TTL 15 min)
**FP-UC05-025:** Sistema exibe mensagem: "Relatório gerado com sucesso! Tempo: [X] segundos"
**FP-UC05-026:** Sistema oferece download automático do arquivo
**FP-UC05-027:** Botão "Enviar por E-mail" disponível

## Fluxos Alternativos

**FA-UC05-001:** Gerar múltiplos relatórios em ZIP (RN-RF065-014)
- Usuário seleciona N templates (máx 10)
- Clica em "Gerar em Lote"
- Sistema exibe modal com parâmetros de todos templates
- Usuário preenche parâmetros
- Sistema gera todos em paralelo (tasks assíncronas)
- Sistema compacta em arquivo .zip
- Nome do ZIP: "Relatorios-YYYYMMDD-HHMMSS.zip"
- Download automático

**FA-UC05-002:** Enviar relatório por e-mail
- Usuário clica em "Enviar por E-mail" após geração
- Sistema exibe modal com campos:
  - Destinatários (múltiplos e-mails separados por vírgula)
  - Assunto (pré-preenchido com nome do template)
  - Mensagem (opcional)
- Usuário preenche e confirma
- Sistema envia e-mail via SMTP com arquivo anexo
- Exibe mensagem: "E-mail enviado com sucesso para [N] destinatários"

**FA-UC05-003:** Regenerar forçando atualização de cache
- Usuário clica em "Regenerar" quando relatório vem do cache
- Sistema executa query novamente
- Sobrescreve cache com novos dados
- Download automático do arquivo atualizado

## Fluxos de Exceção

**FE-UC05-001:** Parâmetros obrigatórios não preenchidos
- Sistema retorna HTTP 400 Bad Request
- Exibe mensagem: "Parâmetro '@DataInicio' é obrigatório"
- Modal permanece aberto

**FE-UC05-002:** Query retorna erro de execução
- Sistema retorna HTTP 500 Internal Server Error
- Registra em RelatorioExecucao (Status=Falha)
- Exibe mensagem: "Erro ao executar query: [Mensagem do DB]"
- Sugestão: "Verifique parâmetros ou contate TI"

**FE-UC05-003:** Query muito lenta (timeout >2 minutos)
- Sistema cancela execução
- Registra em RelatorioExecucao (Status=Timeout)
- Exibe mensagem: "Query demorou >2 minutos. Otimize o template ou filtre mais dados."

**FE-UC05-004:** Erro ao fazer upload para Azure Blob Storage
- Sistema retorna HTTP 500 Internal Server Error
- Registra em RelatorioExecucao (Status=Falha_Upload)
- Exibe mensagem: "Erro ao salvar arquivo. Tente novamente."

**FE-UC05-005:** Certificado X.509 expirado (para assinatura PDF)
- Sistema retorna HTTP 400 Bad Request
- Exibe mensagem: "Certificado digital expirado. Configure um certificado válido."

**FE-UC05-006:** Máximo de 10 relatórios por ZIP excedido
- Sistema retorna HTTP 400 Bad Request
- Exibe mensagem: "Máximo 10 relatórios por ZIP. Selecione menos templates."

**FE-UC05-007:** Query retorna 0 linhas (dataset vazio)
- Sistema gera relatório com estado vazio
- Exibe mensagem: "Relatório gerado, mas a query não retornou dados"
- Arquivo contém cabeçalho/rodapé mas sem linhas de dados

## Regras de Negócio

**RN-UC05-001:** Formato de saída obrigatório (RN-RF065-001)
- Excel: .xlsx via EPPlus
- PDF: via QuestPDF
- CSV: via CsvHelper

**RN-UC05-002:** Gráficos Chart.js (RN-RF065-002)
- Frontend renderiza com Chart.js
- Converte para PNG via canvas.toBlob()
- Embeda imagem no Excel/PDF

**RN-UC05-003:** Cache de relatórios pesados (RN-RF065-013)
- Critérios: >1000 linhas OU >5s de execução
- Cache Redis com TTL 15 minutos
- Key: md5(TemplateId + Parâmetros JSON)
- Indicador visual para usuário

**RN-UC05-004:** Proteção Excel (RN-RF065-009)
- Planilha bloqueada por padrão
- EPPlus: worksheet.Protection.IsProtected = true
- Senha opcional

**RN-UC05-005:** Assinatura digital PDF (RN-RF065-010)
- Certificado X.509 obrigatório
- QuestPDF: document.Metadata.Sign(certificate)
- Timestamp automático

**RN-UC05-006:** Marca d'água PDF (RN-RF065-011)
- Texto diagonal em todas as páginas
- Opacidade 20-30% para não obstruir leitura
- QuestPDF: page.Watermark(text)

**RN-UC05-007:** Compactação ZIP de múltiplos relatórios (RN-RF065-014)
- Máximo 10 relatórios por ZIP
- Geração paralela (await Task.WhenAll)
- Nome do ZIP: Relatorios-YYYYMMDD-HHMMSS.zip

**RN-UC05-008:** Métricas de uso (RN-RF065-015)
- Incrementar QuantidadeGeracoes em RelatorioTemplate
- Atualizar TempoMedioGeracao: (TempoMedioAntigo * N + TempoNovo) / (N+1)
- Registrar FormatoUtilizado para estatísticas

**RN-UC05-009:** Auditoria obrigatória
- Toda geração DEVE ser auditada
- Campos: TemplateId, UsuarioId, Formato, Tamanho, Tempo, Parâmetros

## Critérios de Aceite

- Parâmetros dinâmicos funcionais (DATE, TEXT, NUMBER, SELECT)
- Query executada com parâmetros informados
- Gráficos Chart.js renderizados e embedados
- Formatação condicional aplicada
- Agrupamentos e subtotais calculados
- Arquivo gerado no formato selecionado
- Upload para Azure Blob Storage bem-sucedido
- Cache Redis funcional (TTL 15 min)
- Proteção Excel aplicada
- Assinatura PDF funcional (se configurada)
- Marca d'água aplicada (se configurada)
- Métricas de uso atualizadas
- Download automático funcional
- Envio por e-mail funcional

---

# UC06 - Agendar Relatório

## Objetivo

Criar agendamento de geração automática de relatório com frequência diária, semanal ou mensal via Hangfire, aplicando parâmetros dinâmicos, enviando por e-mail aos destinatários e registrando log de execuções.

## Pré-condições

- Usuário autenticado com permissão `TPL.RELATORIOS.SCHEDULE`
- Template existe, está ativo e pertence ao tenant do usuário
- Hangfire configurado e funcional

## Pós-condições

- Agendamento criado em RelatorioAgendamento
- Hangfire Job configurado com cron expression
- Destinatários de e-mail salvos
- Auditoria registrada
- Job executado conforme frequência configurada

## Fluxo Principal

**FP-UC06-001:** Usuário clica em "Agendar" em um template
**FP-UC06-002:** Sistema valida permissão TPL.RELATORIOS.SCHEDULE
**FP-UC06-003:** Sistema valida que template está ativo
**FP-UC06-004:** Sistema exibe wizard de agendamento em 3 passos:

**Passo 1 - Configuração Básica:**
**FP-UC06-005:** Usuário preenche:
- Nome do agendamento (3-100 caracteres, único por tenant)
- Descrição (opcional, máx 500 caracteres)
- Formato de saída (Excel, PDF, CSV)
- Status (Ativo ou Inativo)

**Passo 2 - Frequência e Parâmetros:**
**FP-UC06-006:** Usuário seleciona frequência (RN-RF065-007):
- DIARIO: Executa todos os dias
- SEMANAL: Executa semanalmente (selecionar dia da semana)
- MENSAL: Executa mensalmente (selecionar dia do mês 1-31)

**FP-UC06-007:** Usuário seleciona horário de execução (00:00 - 23:59)
**FP-UC06-008:** Se SEMANAL, usuário seleciona dia da semana (Segunda a Domingo)
**FP-UC06-009:** Se MENSAL, usuário seleciona dia do mês (1-31)
**FP-UC06-010:** Sistema exibe parâmetros dinâmicos do template (se existirem)
**FP-UC06-011:** Usuário preenche parâmetros com valores fixos ou variáveis:
- Valor fixo: "2025-01-01"
- Variável: "{MesAtual}", "{AnoAtual}", "{PrimeiroDiaMes}", "{UltimoDiaMes}"

**Passo 3 - Destinatários:**
**FP-UC06-012:** Usuário preenche lista de destinatários de e-mail:
- Campo multi-input com validação de e-mail
- Suporta múltiplos e-mails separados por vírgula ou Enter
- Mínimo 1, máximo 20 destinatários

**FP-UC06-013:** Usuário preenche assunto do e-mail (suporta variáveis):
- Exemplo: "Relatório {NomeTemplate} - {DataGeracao}"

**FP-UC06-014:** Usuário preenche corpo do e-mail (opcional, HTML suportado):
- Editor rich text
- Suporta variáveis: {NomeTemplate}, {DataGeracao}, {Usuario}

**FP-UC06-015:** Usuário clica em "Salvar Agendamento"
**FP-UC06-016:** Sistema valida campos obrigatórios
**FP-UC06-017:** Sistema valida e-mails dos destinatários (formato válido)
**FP-UC06-018:** Sistema cria registro em RelatorioAgendamento:
- TemplateId
- EmpresaId
- Nome
- Frequencia (DIARIO/SEMANAL/MENSAL)
- DiaSemana (se SEMANAL)
- DiaMes (se MENSAL)
- Horario
- Formato
- Parametros (JSON)
- Destinatarios (JSON array)
- AssuntoEmail
- CorpoEmail
- Ativo (true)

**FP-UC06-019:** Sistema calcula cron expression conforme frequência:
- DIARIO: `0 {Horario} * * *`
- SEMANAL: `0 {Horario} * * {DiaSemana}`
- MENSAL: `0 {Horario} {DiaMes} * *`

**FP-UC06-020:** Sistema registra Hangfire Job:
- JobId: Guid único
- Cron expression calculada
- Method: `GerarRelatorioAgendado(agendamentoId)`

**FP-UC06-021:** Sistema registra auditoria (CREATE_AGENDAMENTO)
**FP-UC06-022:** Sistema exibe mensagem: "Agendamento '[Nome]' criado com sucesso! Próxima execução: [Data/Hora]"
**FP-UC06-023:** Sistema redireciona para lista de agendamentos

## Fluxos Alternativos

**FA-UC06-001:** Visualizar próximas execuções
- Sistema calcula próximas 5 datas de execução com base no cron
- Exibe em tabela: Data, Hora, Dia da Semana
- Usuário visualiza para validar configuração

**FA-UC06-002:** Executar agendamento manualmente agora
- Usuário clica em "Executar Agora" em agendamento existente
- Sistema executa geração imediatamente (sem aguardar cron)
- Relatório gerado e enviado por e-mail
- Log de execução registrado

**FA-UC06-003:** Pausar agendamento temporariamente
- Usuário clica em "Pausar" em agendamento ativo
- Sistema marca Ativo=false
- Hangfire Job removido
- Agendamento permanece salvo (pode ser reativado)

**FA-UC06-004:** Reativar agendamento pausado
- Usuário clica em "Reativar" em agendamento pausado
- Sistema marca Ativo=true
- Hangfire Job recriado com cron original
- Próxima execução calculada

## Fluxos de Exceção

**FE-UC06-001:** Nome duplicado
- Sistema retorna HTTP 400 Bad Request
- Exibe mensagem: "Já existe um agendamento com o nome '[Nome]'"

**FE-UC06-002:** E-mail inválido
- Sistema retorna HTTP 400 Bad Request
- Exibe mensagem: "E-mail '[Email]' é inválido. Use formato: usuario@dominio.com"
- Campo destacado em vermelho

**FE-UC06-003:** Dia do mês inválido (>31)
- Sistema retorna HTTP 400 Bad Request
- Exibe mensagem: "Dia do mês deve ser entre 1 e 31"

**FE-UC06-004:** Parâmetro obrigatório não preenchido
- Sistema retorna HTTP 400 Bad Request
- Exibe mensagem: "Parâmetro '@DataInicio' é obrigatório"

**FE-UC06-005:** Hangfire Job falha ao criar
- Sistema retorna HTTP 500 Internal Server Error
- Exibe mensagem: "Erro ao criar agendamento. Tente novamente."
- Log técnico: stacktrace do Hangfire

**FE-UC06-006:** Máximo de 20 destinatários excedido
- Sistema retorna HTTP 400 Bad Request
- Exibe mensagem: "Máximo 20 destinatários permitidos. Remova alguns e-mails."

## Regras de Negócio

**RN-UC06-001:** Frequências suportadas (RN-RF065-007)
- DIARIO: Executa todos os dias no horário configurado
- SEMANAL: Executa semanalmente (dia da semana obrigatório)
- MENSAL: Executa mensalmente (dia do mês obrigatório)
- Enum obrigatório: {DIARIO, SEMANAL, MENSAL}

**RN-UC06-002:** Variáveis dinâmicas em parâmetros
- {MesAtual}: Número do mês (1-12)
- {AnoAtual}: Ano com 4 dígitos (2025)
- {PrimeiroDiaMes}: 01/MM/YYYY
- {UltimoDiaMes}: 28-31/MM/YYYY
- {DataOntem}: Data do dia anterior
- Sistema substitui variáveis na hora da execução

**RN-UC06-003:** Hangfire Job configuration
- Cron expression calculada automaticamente
- Job executado em fila background
- Retry automático: 3 tentativas em caso de falha
- Timeout por execução: 30 minutos

**RN-UC06-004:** Log de execuções
- Toda execução gera registro em RelatorioExecucao
- Status: Sucesso, Falha, Timeout
- Erro registrado se falha
- Link para arquivo gerado (se sucesso)

**RN-UC06-005:** E-mail automático
- Enviado via SMTP configurado
- Assunto suporta variáveis
- Corpo suporta HTML
- Arquivo anexado (máx 25MB)
- Se arquivo >25MB, envia link para download (Azure Blob)

**RN-UC06-006:** Multi-tenancy obrigatório
- Agendamento isolado por EmpresaId
- Templates de outros tenants não podem ser agendados

## Critérios de Aceite

- Wizard de 3 passos funcional
- Frequências (DIARIO, SEMANAL, MENSAL) funcionais
- Cron expression calculada corretamente
- Hangfire Job criado e executado
- Parâmetros dinâmicos com variáveis funcionais
- E-mail enviado com arquivo anexado
- Log de execuções registrado
- Pausar/Reativar agendamento funcional
- Executar manualmente funcional
- Multi-tenancy isolado
- Auditoria registrada

---

# UC07 - Visualizar Métricas de Uso

## Objetivo

Visualizar métricas consolidadas de uso dos templates de relatórios, incluindo top 10 templates mais gerados, formato mais popular (Excel/PDF/CSV), top 10 usuários, horário de pico e tempo médio de geração.

## Pré-condições

- Usuário autenticado com permissão `TPL.RELATORIOS.VIEW_METRICS`
- Tenant ativo no sistema

## Pós-condições

- Dashboard de métricas exibido com gráficos e tabelas
- Métricas calculadas em tempo real ou cache (se disponível)
- Exportação de relatório de métricas disponível

## Fluxo Principal

**FP-UC07-001:** Usuário acessa a funcionalidade "Métricas de Templates" pelo menu
**FP-UC07-002:** Sistema valida permissão TPL.RELATORIOS.VIEW_METRICS
**FP-UC07-003:** Sistema carrega métricas consolidadas do tenant (RN-RF065-015)
**FP-UC07-004:** Sistema exibe dashboard com 6 seções:

**Seção 1 - Resumo Geral:**
**FP-UC07-005:** Sistema exibe cards com totalizadores:
- Total de templates cadastrados
- Total de gerações (últimos 30 dias)
- Total de agendamentos ativos
- Tempo médio de geração (segundos)

**Seção 2 - Top 10 Templates:**
**FP-UC07-006:** Sistema exibe tabela com:
- Nome do template
- Quantidade de gerações (últimos 30 dias)
- Formato mais utilizado (Excel/PDF/CSV)
- Tempo médio de geração
- Gráfico de barras horizontal

**Seção 3 - Formato Mais Popular:**
**FP-UC07-007:** Sistema exibe gráfico de pizza (Chart.js) com:
- % de gerações em Excel
- % de gerações em PDF
- % de gerações em CSV
- Total de gerações por formato

**Seção 4 - Top 10 Usuários:**
**FP-UC07-008:** Sistema exibe tabela com:
- Nome do usuário
- Quantidade de gerações (últimos 30 dias)
- Templates mais utilizados (top 3)
- Gráfico de barras horizontal

**Seção 5 - Horário de Pico:**
**FP-UC07-009:** Sistema exibe gráfico de linha (Chart.js) com:
- Eixo X: Hora do dia (00h - 23h)
- Eixo Y: Quantidade de gerações
- Linha destacando horário de pico
- Tooltip com quantidade exata

**Seção 6 - Tempo Médio de Geração:**
**FP-UC07-010:** Sistema exibe gráfico de área (Chart.js) com:
- Eixo X: Últimos 30 dias
- Eixo Y: Tempo médio (segundos)
- Linha de tendência
- Indicador de melhoria/piora de performance

## Fluxos Alternativos

**FA-UC07-001:** Filtrar métricas por período
- Usuário seleciona período: Últimos 7 dias, 30 dias, 90 dias, 12 meses
- Sistema recalcula métricas para período selecionado
- Gráficos atualizados

**FA-UC07-002:** Filtrar métricas por categoria
- Usuário seleciona categoria: Financeiro, Operacional, Gerencial, Auditoria
- Sistema filtra templates da categoria selecionada
- Métricas recalculadas

**FA-UC07-003:** Exportar relatório de métricas
- Usuário clica em "Exportar Métricas"
- Sistema gera relatório Excel com:
  - Aba 1: Resumo Geral
  - Aba 2: Top Templates
  - Aba 3: Top Usuários
  - Aba 4: Dados brutos (gerações detalhadas)
- Download automático

**FA-UC07-004:** Visualizar detalhes de template
- Usuário clica em template no Top 10
- Sistema redireciona para UC02 - Visualizar Template
- Aba "Histórico de Gerações" pré-selecionada

## Fluxos de Exceção

**FE-UC07-001:** Usuário sem permissão
- Sistema retorna HTTP 403 Forbidden
- Exibe mensagem: "Você não tem permissão para visualizar métricas"

**FE-UC07-002:** Nenhuma geração nos últimos 30 dias
- Sistema exibe estado vazio: "Nenhuma geração registrada nos últimos 30 dias"
- Sugestão: "Gere relatórios para visualizar métricas"

**FE-UC07-003:** Erro ao calcular métricas
- Sistema retorna HTTP 500 Internal Server Error
- Exibe mensagem: "Erro ao calcular métricas. Tente novamente."
- Log técnico registrado

## Regras de Negócio

**RN-UC07-001:** Métricas de uso (RN-RF065-015)
- Quantidade de gerações: COUNT(*) FROM RelatorioExecucao WHERE Status=Sucesso
- Tempo médio: AVG(TempoGeracao) WHERE Status=Sucesso
- Formato mais popular: COUNT(*) GROUP BY Formato
- Top usuários: COUNT(*) GROUP BY UsuarioId
- Horário de pico: COUNT(*) GROUP BY HOUR(DataGeracao)

**RN-UC07-002:** Cache de métricas (15 minutos)
- Métricas pesadas (>5s de cálculo) são cacheadas no Redis
- TTL: 15 minutos
- Key: `metrics:tenant:{EmpresaId}:period:{Periodo}`
- Indicador visual: "Atualizado às HH:MM (cache)"

**RN-UC07-003:** Multi-tenancy obrigatório
- Métricas filtradas automaticamente por EmpresaId
- Templates e gerações de outros tenants não aparecem

**RN-UC07-004:** Período padrão: últimos 30 dias
- Se usuário não selecionar período, usar 30 dias
- Cálculos: DataGeracao >= DATEADD(DAY, -30, GETDATE())

## Critérios de Aceite

- Dashboard carrega em <3 segundos
- 6 seções exibidas corretamente
- Gráficos Chart.js renderizados
- Top 10 templates calculados corretamente
- Formato mais popular calculado corretamente
- Top 10 usuários calculados corretamente
- Horário de pico identificado
- Tempo médio de geração calculado
- Filtros por período funcionais
- Exportação Excel funcional
- Cache Redis funcionando (TTL 15 min)
- Multi-tenancy isolado

---

## Matriz de Rastreabilidade

| UC | Funcionalidades RF Cobertas | Regras de Negócio Aplicadas |
|----|----------------------------|------------------------------|
| UC00 | RF-CRUD-02 | RN-RF065-015 (métricas de uso) |
| UC01 | RF-CRUD-01, RF-FUNC-01 a RF-FUNC-18, RF-VAL-01 a RF-VAL-05, RF-SEC-01 a RF-SEC-04 | RN-RF065-001 a RN-RF065-015 |
| UC02 | RF-CRUD-03 | RN-RF065-015 (métricas de uso) |
| UC03 | RF-CRUD-04 | Versionamento, Diff, Multi-tenancy |
| UC04 | RF-CRUD-05 | Soft delete, Preservação de histórico |
| UC05 | RF-FUNC-01 a RF-FUNC-18 | RN-RF065-001 a RN-RF065-015 |
| UC06 | RF-FUNC-09, RF-FUNC-10 | RN-RF065-007 (agendamento) |
| UC07 | RF-FUNC-18 | RN-RF065-015 (métricas de uso) |

---

## CHANGELOG

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 1.0 | 2025-12-17 | Sistema | Versão inicial com 4 UCs básicos |
| 2.0 | 2025-12-31 | Claude Code (Agente UC) | Versão completa com 8 UCs, seguindo template oficial, cobrindo 100% do RF065.yaml |
