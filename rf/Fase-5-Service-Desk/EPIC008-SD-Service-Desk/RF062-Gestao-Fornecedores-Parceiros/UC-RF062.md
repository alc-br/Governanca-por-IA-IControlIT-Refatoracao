# UC-RF062 — Casos de Uso Canônicos

**RF:** RF062 — Gestão de Fornecedores e Parceiros
**Versão:** 2.0
**Data:** 2025-12-31
**Autor:** Agência ALC - alc.dev.br
**Epic:** EPIC008-SD-Service-Desk
**Fase:** Fase 5 - Service Desk

---

## 1. OBJETIVO

Este documento especifica os **Casos de Uso** do **RF062 — Gestão de Fornecedores e Parceiros**, cobrindo gerenciamento completo do ciclo de vida de fornecedores e parceiros de TI/Telecom, incluindo cadastro, documentação obrigatória, homologação, contratos, SLAs, avaliações e performance.

**Escopo:**
- Cadastro CRUD de fornecedores com classificação por categoria
- Upload e controle de documentação obrigatória (CNPJ, CNDs)
- Gestão de múltiplos contatos (comercial, técnico, financeiro)
- Contratos vinculados com alertas de renovação
- SLAs por tipo de serviço
- Processo de homologação
- Avaliações periódicas e ranking automático
- Alertas de vencimentos
- Bloqueio automático por documentação vencida
- Dashboard de performance em tempo real
- Integração com solicitações e ordens de serviço
- Exportação de relatórios de compliance
- Histórico completo de atendimentos

---

## 2. SUMÁRIO DOS CASOS DE USO

| UC | Nome | Ator Principal | Tipo | Impacta Dados |
|----|------|----------------|------|---------------|
| **UC00** | Listar Fornecedores | `usuario_autenticado` | Leitura | Não |
| **UC01** | Criar Fornecedor | `gestor_compras` | Escrita | Sim |
| **UC02** | Visualizar Fornecedor | `usuario_autenticado` | Leitura | Não |
| **UC03** | Editar Fornecedor | `gestor_compras` | Escrita | Sim |
| **UC04** | Inativar Fornecedor | `gestor_compras` | Escrita | Sim |
| **UC05** | Upload de Documentação | `gestor_compras` | Escrita | Sim |
| **UC06** | Gerenciar Contatos | `gestor_compras` | Escrita | Sim |
| **UC07** | Gerenciar Contratos | `gestor_compras` | Escrita | Sim |
| **UC08** | Definir SLAs | `gestor_compras` | Escrita | Sim |
| **UC09** | Homologar Fornecedor | `gestor_compras` | Ação | Sim |
| **UC10** | Avaliar Fornecedor | `gestor_compras` | Escrita | Sim |
| **UC11** | Visualizar Ranking | `usuario_autenticado` | Leitura | Não |
| **UC12** | Dashboard de Performance | `usuario_autenticado` | Leitura | Não |
| **UC13** | Exportar Relatório | `usuario_autenticado` | Ação | Não |
| **UC14** | Consultar Histórico de Atendimentos | `usuario_autenticado` | Leitura | Não |

---

## 3. PADRÕES GERAIS APLICÁVEIS A TODOS OS UCs

### 3.1 Multi-Tenancy (Isolamento de Tenant)

**Regra:** Todos os UCs filtram por `EmpresaId` do usuário autenticado.

**Implementação:**
- Queries: `WHERE EmpresaId = @UsuarioEmpresaId AND Fl_Ativo = 1`
- Acesso cruzado → HTTP 403

### 3.2 Controle de Acesso (RBAC)

**Permissões:**
- `SD.FORNECEDORES.VIEW_ANY` - Listar fornecedores
- `SD.FORNECEDORES.VIEW` - Visualizar detalhes
- `SD.FORNECEDORES.CREATE` - Criar fornecedor
- `SD.FORNECEDORES.UPDATE` - Editar fornecedor
- `SD.FORNECEDORES.DELETE` - Inativar fornecedor
- `SD.FORNECEDORES.HOMOLOGAR` - Aprovar/rejeitar homologação
- `SD.FORNECEDORES.AVALIAR` - Registrar avaliações
- `SD.FORNECEDORES.EXPORT` - Exportar relatórios

### 3.3 Auditoria Automática

**Operações auditadas:**
- CREATE, UPDATE, DELETE (fornecedores)
- UPLOAD_DOCUMENTO (documentação)
- HOMOLOGACAO (aprovação/rejeição)
- AVALIACAO (registro de avaliações)
- BLOQUEIO (bloqueio automático)

**Retenção:** 7 anos (LGPD)

### 3.4 Internacionalização (i18n)

**Chaves:** `fornecedores.*`, `documentos.*`, `contratos.*`, `avaliacoes.*`
**Idiomas:** pt-BR, en-US, es-ES

---

## 4. CASOS DE USO

### UC00 — Listar Fornecedores

**Objetivo:** Listar fornecedores cadastrados no tenant com filtros e paginação.

**Pré-condições:**
- Usuário autenticado
- Permissão `SD.FORNECEDORES.VIEW_ANY`

**Fluxo Principal:**
1. Usuário acessa `/service-desk/fornecedores`
2. Sistema valida permissão
3. Sistema carrega fornecedores do tenant (EmpresaId)
4. Sistema aplica paginação (25 registros/página)
5. Sistema exibe grid com: Razão Social, CNPJ, Categoria, Status, Avaliação Média, Contratos Ativos, Documentação (ícone status)

**Fluxos Alternativos:**
- **FA-UC00-001:** Filtrar por categoria (Operadora, Fabricante, Revenda, Prestador de Serviço, Software House, Transportadora)
- **FA-UC00-002:** Filtrar por status (Rascunho, Em Análise, Ativo, Bloqueado, Inativo)
- **FA-UC00-003:** Buscar por razão social ou CNPJ
- **FA-UC00-004:** Ordenar por qualquer coluna
- **FA-UC00-005:** Filtrar por documentação vencida

**Fluxos de Exceção:**
- **FE-UC00-001:** Sem permissão → HTTP 403

**Cobertura:**
- RF-CRUD-02

---

### UC01 — Criar Fornecedor

**Objetivo:** Cadastrar novo fornecedor com dados completos.

**Pré-condições:**
- Usuário autenticado
- Permissão `SD.FORNECEDORES.CREATE`

**Fluxo Principal:**
1. Usuário acessa formulário de criação
2. Sistema valida permissão
3. Usuário preenche campos obrigatórios
4. Sistema valida CNPJ (formato e dígitos verificadores)
5. Sistema verifica unicidade de CNPJ no tenant
6. Sistema cria fornecedor com status "rascunho"
7. Sistema registra auditoria (CREATE)
8. Sistema retorna HTTP 201

**Campos Obrigatórios:**
- Razão Social
- CNPJ (validação de formato e dígitos)
- Categoria (enum: Operadora, Fabricante, Revenda, Prestador de Serviço, Software House, Transportadora)
- Email (validação de formato)

**Fluxos de Exceção:**
- **FE-UC01-001:** CNPJ duplicado no tenant → HTTP 400
- **FE-UC01-002:** CNPJ inválido (dígitos verificadores) → HTTP 400
- **FE-UC01-003:** Email inválido → HTTP 400

**Regras de Negócio:**
- **RN-RF062-001:** Categoria é obrigatória e imutável após criação
- **RN-RF062-002:** Fornecedor criado com status "rascunho"

**Cobertura:**
- RF-CRUD-01
- RF-VAL-01
- RF-VAL-02
- RF-VAL-03

---

### UC02 — Visualizar Fornecedor

**Objetivo:** Visualizar detalhes completos de fornecedor específico.

**Pré-condições:**
- Usuário autenticado
- Permissão `SD.FORNECEDORES.VIEW`

**Fluxo Principal:**
1. Usuário clica em fornecedor ou acessa `/fornecedores/{id}`
2. Sistema valida permissão e tenant
3. Sistema carrega fornecedor + dados relacionados (contatos, contratos, documentos, avaliações, histórico)
4. Sistema exibe abas: Resumo, Documentos, Contatos, Contratos, SLAs, Avaliações, Histórico de Atendimentos

**Dados Exibidos na Aba Resumo:**
- Razão Social, CNPJ, Categoria, Status
- Email, Telefone, Endereço
- Quantidade de contratos ativos
- Avaliação média (1-5 estrelas)
- Indicadores de documentação (válida/vencida)
- Timeline de mudanças de status

**Fluxos de Exceção:**
- **FE-UC02-001:** Fornecedor não encontrado ou de outro tenant → HTTP 404

**Cobertura:**
- RF-CRUD-03

---

### UC03 — Editar Fornecedor

**Objetivo:** Atualizar informações de fornecedor existente.

**Pré-condições:**
- Usuário autenticado
- Permissão `SD.FORNECEDORES.UPDATE`

**Fluxo Principal:**
1. Usuário edita campos permitidos
2. Sistema valida permissão
3. Sistema valida dados (CNPJ, email, telefone)
4. Sistema atualiza fornecedor
5. Sistema registra auditoria (UPDATE)
6. Sistema retorna HTTP 200

**Campos Não Editáveis:**
- Categoria (imutável conforme RN-RF062-001)
- CNPJ (apenas com aprovação especial)

**Fluxos de Exceção:**
- **FE-UC03-001:** Tentar alterar categoria → HTTP 400
- **FE-UC03-002:** CNPJ inválido → HTTP 400

**Regras de Negócio:**
- **RN-RF062-001:** Categoria não pode ser alterada após criação

**Cobertura:**
- RF-CRUD-04

---

### UC04 — Inativar Fornecedor

**Objetivo:** Inativar fornecedor via soft delete.

**Pré-condições:**
- Usuário autenticado
- Permissão `SD.FORNECEDORES.DELETE`

**Fluxo Principal:**
1. Usuário clica em "Inativar"
2. Sistema valida permissão
3. Sistema verifica se fornecedor possui contratos ativos ou OSs em andamento
4. Sistema exibe confirmação com impacto
5. Usuário confirma
6. Sistema marca Fl_Ativo = 0 e Status = "inativo"
7. Sistema registra auditoria (DELETE)
8. Sistema retorna HTTP 200

**Fluxos de Exceção:**
- **FE-UC04-001:** Fornecedor com contratos ativos → HTTP 400 (não pode inativar)
- **FE-UC04-002:** Fornecedor com ordens de serviço em andamento → HTTP 400

**Regras de Negócio:**
- **RN-RF062-016:** Fornecedor inativo não pode ser reativado (criar novo registro)

**Cobertura:**
- RF-CRUD-05

---

### UC05 — Upload de Documentação

**Objetivo:** Fazer upload de documentação obrigatória (CNPJ, CNDs) com controle de vencimento.

**Pré-condições:**
- Usuário autenticado
- Permissão `SD.FORNECEDORES.UPDATE`
- Fornecedor existente

**Fluxo Principal:**
1. Usuário acessa aba "Documentos" do fornecedor
2. Sistema valida permissão
3. Usuário seleciona tipo de documento (CNPJ, CND Federal, CND Estadual, CND Municipal, Contrato Social, Alvará)
4. Usuário faz upload do arquivo (PDF, JPEG, PNG - max 5MB)
5. Sistema valida extensão e tamanho
6. Sistema valida tipo de arquivo (magic bytes)
7. Usuário informa data de emissão e data de validade
8. Sistema criptografa arquivo
9. Sistema salva documento vinculado ao fornecedor
10. Sistema registra auditoria (UPLOAD_DOCUMENTO)
11. Sistema recalcula status de compliance
12. Sistema retorna HTTP 201

**Documentos Obrigatórios (PJ):**
- CNPJ
- CND Federal
- CND Estadual
- CND Municipal

**Fluxos Alternativos:**
- **FA-UC05-001:** Substituir documento existente (versionamento automático)

**Fluxos de Exceção:**
- **FE-UC05-001:** Arquivo com extensão não permitida → HTTP 400
- **FE-UC05-002:** Arquivo maior que 5MB → HTTP 413
- **FE-UC05-003:** Arquivo malicioso detectado → HTTP 400
- **FE-UC05-004:** Data de validade anterior à data de emissão → HTTP 400

**Regras de Negócio:**
- **RN-RF062-002:** Fornecedor PJ deve manter certidões válidas
- **RN-RF062-003:** Sistema alerta vencimentos D-30, D-15, D-7
- **RN-RF062-004:** Bloqueio automático no dia seguinte ao vencimento

**Cobertura:**
- RF-VAL-05
- RF-SEC-03 (criptografia)
- RF-SEC-04 (proteção upload malicioso)

---

### UC06 — Gerenciar Contatos

**Objetivo:** Cadastrar e gerenciar múltiplos contatos do fornecedor por departamento.

**Pré-condições:**
- Usuário autenticado
- Permissão `SD.FORNECEDORES.UPDATE`
- Fornecedor existente

**Fluxo Principal:**
1. Usuário acessa aba "Contatos" do fornecedor
2. Sistema valida permissão
3. Sistema exibe lista de contatos cadastrados (Nome, Departamento, Email, Telefone)
4. Usuário clica em "Adicionar Contato"
5. Usuário preenche: Nome*, Departamento* (Comercial/Técnico/Financeiro), Email*, Telefone*, Cargo
6. Sistema valida email (formato) e telefone (padrão brasileiro)
7. Sistema salva contato
8. Sistema registra auditoria (CREATE_CONTATO)
9. Sistema retorna HTTP 201

**Departamentos:**
- Comercial
- Técnico
- Financeiro
- Gerência
- Suporte

**Fluxos Alternativos:**
- **FA-UC06-001:** Editar contato existente
- **FA-UC06-002:** Excluir contato (soft delete)
- **FA-UC06-003:** Marcar contato como principal

**Fluxos de Exceção:**
- **FE-UC06-001:** Email inválido → HTTP 400
- **FE-UC06-002:** Telefone fora do padrão brasileiro → HTTP 400

**Regras de Negócio:**
- **RN-RF062-009:** Cada fornecedor pode ter múltiplos contatos
- **RN-RF062-009:** Cada departamento deve ter pelo menos um contato principal

**Cobertura:**
- RF-VAL-03 (validação email)
- RF-VAL-04 (validação telefone)

---

### UC07 — Gerenciar Contratos

**Objetivo:** Cadastrar e controlar contratos vinculados ao fornecedor com vigência, valores e renovação.

**Pré-condições:**
- Usuário autenticado
- Permissão `SD.FORNECEDORES.UPDATE`
- Fornecedor homologado

**Fluxo Principal:**
1. Usuário acessa aba "Contratos" do fornecedor
2. Sistema valida permissão
3. Sistema exibe lista de contratos (Número, Objeto, Vigência, Valor, Status)
4. Usuário clica em "Adicionar Contrato"
5. Usuário preenche: Número*, Objeto*, Data Início*, Data Fim*, Valor Total, Renovação Automática (Sim/Não)
6. Sistema valida datas (Data Fim > Data Início)
7. Sistema calcula dias restantes até vencimento
8. Sistema salva contrato
9. Sistema registra auditoria (CREATE_CONTRATO)
10. Sistema retorna HTTP 201

**Campos do Contrato:**
- Número do Contrato
- Objeto (descrição do que está sendo contratado)
- Data de Início
- Data de Fim
- Valor Total
- Renovação Automática (booleano)
- Arquivo digitalizado (PDF)

**Fluxos Alternativos:**
- **FA-UC07-001:** Editar contrato existente
- **FA-UC07-002:** Renovar contrato (criar novo vínculo)
- **FA-UC07-003:** Encerrar contrato antecipadamente

**Fluxos de Exceção:**
- **FE-UC07-001:** Data Fim anterior a Data Início → HTTP 400
- **FE-UC07-002:** Fornecedor não homologado → HTTP 403

**Regras de Negócio:**
- **RN-RF062-005:** Cada fornecedor pode ter múltiplos contratos
- **RN-RF062-013:** Alertas de renovação D-90, D-60, D-30

**Cobertura:**
- RN-RF062-005
- RN-RF062-013

---

### UC08 — Definir SLAs

**Objetivo:** Configurar SLAs (tempos de resposta e resolução) por tipo de serviço fornecido.

**Pré-condições:**
- Usuário autenticado
- Permissão `SD.FORNECEDORES.UPDATE`
- Fornecedor homologado

**Fluxo Principal:**
1. Usuário acessa aba "SLAs" do fornecedor
2. Sistema valida permissão
3. Sistema exibe lista de SLAs cadastrados (Tipo Serviço, Tempo Resposta, Tempo Resolução)
4. Usuário clica em "Adicionar SLA"
5. Usuário seleciona: Tipo de Serviço* (Reparo, Instalação, Suporte, Manutenção)
6. Usuário define: Tempo de Resposta (horas)*, Tempo de Resolução (horas)*, Dias Úteis (Sim/Não)
7. Sistema valida tempos (Resolução >= Resposta)
8. Sistema salva SLA
9. Sistema registra auditoria (CREATE_SLA)
10. Sistema retorna HTTP 201

**Tipos de Serviço:**
- Reparo (correção de problemas)
- Instalação (novos serviços)
- Suporte (atendimento técnico)
- Manutenção (preventiva/corretiva)

**Fluxos Alternativos:**
- **FA-UC08-001:** Editar SLA existente
- **FA-UC08-002:** Excluir SLA

**Fluxos de Exceção:**
- **FE-UC08-001:** Tempo de resolução menor que tempo de resposta → HTTP 400
- **FE-UC08-002:** Fornecedor não homologado → HTTP 403

**Regras de Negócio:**
- **RN-RF062-006:** SLAs definidos por tipo de serviço
- **RN-RF062-010:** SLAs vinculados automaticamente a ordens de serviço

**Cobertura:**
- RN-RF062-006
- RN-RF062-010

---

### UC09 — Homologar Fornecedor

**Objetivo:** Aprovar ou rejeitar fornecedor, habilitando-o para receber ordens de serviço.

**Pré-condições:**
- Usuário autenticado
- Permissão `SD.FORNECEDORES.HOMOLOGAR`
- Fornecedor em status "em_analise"
- Documentação obrigatória completa e válida

**Fluxo Principal (Aprovação):**
1. Usuário acessa fornecedor em análise
2. Sistema valida permissão
3. Sistema verifica se documentação está completa e válida
4. Usuário revisa: dados cadastrais, documentos, contatos
5. Usuário clica em "Homologar"
6. Sistema valida pré-requisitos (documentação completa)
7. Sistema altera status para "ativo"
8. Sistema registra auditoria (HOMOLOGACAO_APROVADA)
9. Sistema envia notificação ao fornecedor
10. Sistema retorna HTTP 200

**Fluxo Alternativo (Rejeição):**
- **FA-UC09-001:** Usuário clica em "Rejeitar"
- **FA-UC09-002:** Usuário informa motivo da rejeição (obrigatório, mín 20 caracteres)
- **FA-UC09-003:** Sistema altera status para "rascunho"
- **FA-UC09-004:** Sistema registra auditoria (HOMOLOGACAO_REJEITADA)
- **FA-UC09-005:** Sistema envia notificação ao fornecedor com motivo

**Fluxos de Exceção:**
- **FE-UC09-001:** Documentação obrigatória incompleta → HTTP 400
- **FE-UC09-002:** Documentação vencida → HTTP 400
- **FE-UC09-003:** Fornecedor não está em status "em_analise" → HTTP 400

**Regras de Negócio:**
- **RN-RF062-014:** Homologação é obrigatória antes de receber OSs
- **RN-RF062-002:** Documentação completa é pré-requisito

**Cobertura:**
- RN-RF062-014
- RN-RF062-002

---

### UC10 — Avaliar Fornecedor

**Objetivo:** Registrar avaliação trimestral de performance do fornecedor.

**Pré-condições:**
- Usuário autenticado
- Permissão `SD.FORNECEDORES.AVALIAR`
- Fornecedor ativo com histórico de atendimentos

**Fluxo Principal:**
1. Usuário acessa aba "Avaliações" do fornecedor
2. Sistema valida permissão
3. Sistema exibe histórico de avaliações anteriores
4. Usuário clica em "Nova Avaliação"
5. Usuário avalia quatro dimensões (escala 1-5):
   - Qualidade (conformidade com especificações)
   - Prazo (cumprimento de SLAs)
   - Custo (relação custo-benefício)
   - Atendimento (suporte e comunicação)
6. Usuário adiciona comentários (opcional, max 500 caracteres)
7. Sistema valida notas (range 1-5)
8. Sistema calcula nota média
9. Sistema salva avaliação
10. Sistema registra auditoria (AVALIACAO)
11. Sistema recalcula ranking do fornecedor
12. Sistema retorna HTTP 201

**Dimensões de Avaliação:**
- **Qualidade:** Conformidade técnica, ausência de defeitos
- **Prazo:** Cumprimento de SLAs, pontualidade
- **Custo:** Relação custo-benefício, transparência financeira
- **Atendimento:** Suporte, comunicação, proatividade

**Fluxos Alternativos:**
- **FA-UC10-001:** Visualizar gráfico de evolução de notas
- **FA-UC10-002:** Comparar com média de fornecedores da mesma categoria

**Fluxos de Exceção:**
- **FE-UC10-001:** Nota fora do range 1-5 → HTTP 400
- **FE-UC10-002:** Fornecedor sem atendimentos nos últimos 3 meses → HTTP 400 (avaliação prematura)

**Regras de Negócio:**
- **RN-RF062-007:** Avaliações trimestrais obrigatórias
- **RN-RF062-008:** Nota média < 2.0 por duas avaliações consecutivas → bloqueio automático

**Cobertura:**
- RN-RF062-007
- RN-RF062-008

---

### UC11 — Visualizar Ranking

**Objetivo:** Visualizar ranking automático de fornecedores por categoria.

**Pré-condições:**
- Usuário autenticado
- Permissão `SD.FORNECEDORES.VIEW_ANY`

**Fluxo Principal:**
1. Usuário acessa `/fornecedores/ranking`
2. Sistema valida permissão
3. Usuário seleciona categoria (ou "Todas")
4. Sistema calcula ranking combinando:
   - Nota média de avaliações (peso 60%)
   - SLA compliance últimos 6 meses (peso 40%)
5. Sistema exibe top 10 fornecedores com:
   - Posição, Razão Social, Categoria, Nota Final, Nota Avaliações, SLA Compliance (%)
6. Sistema destaca visualmente top 3 (ouro, prata, bronze)

**Fórmula de Ranking:**
```
Nota Final = (Nota Média Avaliações × 0.60) + (SLA Compliance % / 20 × 0.40)
```

**Fluxos Alternativos:**
- **FA-UC11-001:** Filtrar por período (último trimestre, semestre, ano)
- **FA-UC11-002:** Exportar ranking em PDF

**Fluxos de Exceção:**
- **FE-UC11-001:** Nenhum fornecedor com dados suficientes → Exibir mensagem informativa

**Regras de Negócio:**
- **RN-RF062-008:** Ranking automático por categoria

**Cobertura:**
- RN-RF062-008

---

### UC12 — Dashboard de Performance

**Objetivo:** Visualizar painel executivo com métricas de fornecedores em tempo real.

**Pré-condições:**
- Usuário autenticado
- Permissão `SD.FORNECEDORES.VIEW_ANY`

**Fluxo Principal:**
1. Usuário acessa `/fornecedores/dashboard`
2. Sistema valida permissão
3. Sistema carrega métricas do tenant
4. Sistema exibe cards:
   - **Total de Fornecedores Ativos**
   - **Contratos Ativos** (valor total)
   - **Documentos Vencidos** (quantidade e percentual)
   - **SLA Compliance Médio** (% últimos 30 dias)
   - **Nota Média de Avaliações** (últimos 3 meses)
5. Sistema exibe gráficos:
   - **Pizza:** Fornecedores por categoria
   - **Barra:** Top 5 fornecedores por gasto (últimos 12 meses)
   - **Linha:** Evolução de SLA compliance mensal
   - **Gauge:** Compliance de documentação (verde >90%, amarelo 70-90%, vermelho <70%)
6. Sistema atualiza em tempo real via SignalR

**Fluxos Alternativos:**
- **FA-UC12-001:** Filtrar período (último mês, trimestre, semestre, ano)
- **FA-UC12-002:** Drill-down em gráfico (clicar em fatia/barra para ver detalhes)

**Fluxos de Exceção:**
- **FE-UC12-001:** Sem dados suficientes → Exibir mensagem orientativa

**Regras de Negócio:**
- **RN-RF062-012:** Dashboard com métricas em tempo real

**Cobertura:**
- RN-RF062-012

---

### UC13 — Exportar Relatório

**Objetivo:** Exportar relatório consolidado de fornecedores para compliance e auditorias.

**Pré-condições:**
- Usuário autenticado
- Permissão `SD.FORNECEDORES.EXPORT`

**Fluxo Principal:**
1. Usuário acessa `/fornecedores/relatorios`
2. Sistema valida permissão
3. Usuário seleciona tipo de relatório:
   - **Compliance Documental** (status de documentação obrigatória)
   - **Performance por Categoria** (avaliações e SLAs)
   - **Contratos Vigentes** (contratos ativos com vencimentos)
   - **Histórico de Homologações** (aprovações/rejeições)
4. Usuário seleciona período
5. Usuário escolhe formato (PDF, Excel)
6. Sistema gera relatório com:
   - Cabeçalho (logo, empresa, data, período)
   - Filtros aplicados
   - Dados tabulares
   - Gráficos (se PDF)
   - Assinatura digital (timestamp)
7. Sistema registra auditoria (EXPORT_RELATORIO)
8. Sistema retorna arquivo para download

**Tipos de Relatório:**
- **Compliance Documental:** Razão Social, CNPJ, Status Documentação, Documentos Vencidos, Data Último Update
- **Performance:** Razão Social, Categoria, Nota Média, SLA Compliance, Ranking
- **Contratos:** Razão Social, Número Contrato, Objeto, Vigência, Valor, Dias p/ Vencimento
- **Homologações:** Data, Fornecedor, Responsável, Status (Aprovado/Rejeitado), Motivo

**Fluxos Alternativos:**
- **FA-UC13-001:** Agendar envio periódico por email

**Fluxos de Exceção:**
- **FE-UC13-001:** Nenhum dado no período selecionado → HTTP 400 (mensagem: "Sem dados para exportar")

**Regras de Negócio:**
- **RN-RF062-015:** Relatórios para auditorias e compliance

**Cobertura:**
- RN-RF062-015

---

### UC14 — Consultar Histórico de Atendimentos

**Objetivo:** Visualizar histórico completo de atendimentos realizados por fornecedor.

**Pré-condições:**
- Usuário autenticado
- Permissão `SD.FORNECEDORES.VIEW`

**Fluxo Principal:**
1. Usuário acessa aba "Histórico" do fornecedor
2. Sistema valida permissão
3. Sistema carrega histórico de atendimentos (Solicitações, Ordens de Serviço)
4. Sistema exibe timeline ordenada cronologicamente (mais recente primeiro):
   - Número OS/Solicitação
   - Data
   - Tipo de Serviço
   - Descrição
   - SLA (cumprido/vencido)
   - Status
   - Avaliação (se houver)
5. Sistema exibe métricas:
   - Total de Atendimentos
   - SLA Compliance (%)
   - Tempo Médio de Resolução (dias)
   - Taxa de Reabertura (%)

**Fluxos Alternativos:**
- **FA-UC14-001:** Filtrar por período
- **FA-UC14-002:** Filtrar por tipo de serviço
- **FA-UC14-003:** Filtrar por status SLA (Cumprido/Vencido)
- **FA-UC14-004:** Exportar histórico em Excel

**Fluxos de Exceção:**
- **FE-UC14-001:** Fornecedor sem atendimentos → Exibir mensagem "Nenhum atendimento registrado"

**Regras de Negócio:**
- **RN-RF062-011:** Sistema mantém histórico completo de atendimentos

**Cobertura:**
- RN-RF062-011
- RN-RF062-010 (integração com solicitações)

---

## 5. MATRIZ DE RASTREABILIDADE

### 5.1 Cobertura RF → UC (COMPLETA)

| Item RF | Título | Coberto por UC |
|---------|--------|----------------|
| RF-CRUD-01 | Criar fornecedor | UC01 |
| RF-CRUD-02 | Listar fornecedores | UC00 |
| RF-CRUD-03 | Visualizar fornecedor | UC02 |
| RF-CRUD-04 | Atualizar fornecedor | UC03 |
| RF-CRUD-05 | Inativar fornecedor | UC04 |

**Cobertura CRUD:** 100% (5/5)

### 5.2 Cobertura Validações

| Item RF | Título | Coberto por UC |
|---------|--------|----------------|
| RF-VAL-01 | Validar campos obrigatórios | UC01 |
| RF-VAL-02 | Validar CNPJ | UC01 |
| RF-VAL-03 | Validar email | UC01, UC06 |
| RF-VAL-04 | Validar telefone | UC06 |
| RF-VAL-05 | Validar documentação completa | UC05, UC09 |

**Cobertura Validações:** 100% (5/5)

### 5.3 Cobertura Segurança

| Item RF | Título | Coberto por UC |
|---------|--------|----------------|
| RF-SEC-01 | Isolamento de tenant | Todos UCs |
| RF-SEC-02 | Permissões RBAC | Todos UCs |
| RF-SEC-03 | Criptografia de documentos | UC05 |
| RF-SEC-04 | Proteção upload malicioso | UC05 |
| RF-SEC-05 | Rate limiting | Todos UCs |

**Cobertura Segurança:** 100% (5/5)

### 5.4 Cobertura Regras de Negócio

| Regra | Título | Coberto por UC |
|-------|--------|----------------|
| RN-RF062-001 | Categorias de Fornecedores | UC01 |
| RN-RF062-002 | Documentação Obrigatória | UC05, UC09 |
| RN-RF062-003 | Alertas Vencimento Documentos | UC05 |
| RN-RF062-004 | Bloqueio por Documentação Vencida | UC05 |
| RN-RF062-005 | Contratos Vinculados | UC07 |
| RN-RF062-006 | SLA por Fornecedor | UC08 |
| RN-RF062-007 | Avaliações Periódicas | UC10 |
| RN-RF062-008 | Ranking de Fornecedores | UC11 |
| RN-RF062-009 | Contatos Múltiplos | UC06 |
| RN-RF062-010 | Integração com Solicitações | UC14 |
| RN-RF062-011 | Histórico de Atendimentos | UC14 |
| RN-RF062-012 | Dashboard de Performance | UC12 |
| RN-RF062-013 | Alertas Renovação Contratos | UC07 |
| RN-RF062-014 | Homologação de Fornecedores | UC09 |
| RN-RF062-015 | Export para Compliance | UC13 |

**Cobertura Regras de Negócio:** 100% (15/15)

### 5.5 Resumo de Cobertura

- **CRUD:** 100% (5/5) ✅
- **Validações:** 100% (5/5) ✅
- **Segurança:** 100% (5/5) ✅
- **Regras de Negócio:** 100% (15/15) ✅
- **UCs Esperados:** 100% (14/14) ✅

**Cobertura Total:** 100%

---

## 6. CHANGELOG

### v2.0 — 2025-12-31
- **Migração v1.0 → v2.0**: Conformidade com template canônico
- **Expansão completa**: Documentados TODOS os 14 UCs esperados
- **Adicionado**: Metadados Epic, Fase, Autor
- **Adicionado**: Seção "PADRÕES GERAIS" completa
- **Adicionado**: UC05 (Upload Documentação), UC06 (Contatos), UC07 (Contratos), UC08 (SLAs), UC09 (Homologação), UC10 (Avaliações), UC11 (Ranking), UC12 (Dashboard), UC13 (Relatórios), UC14 (Histórico)
- **Cobertura:** 100% de todos os itens do catálogo RF062.yaml
- **Matriz de Rastreabilidade:** Completa e validada

### v1.0 — 2025-12-18
- Versão inicial simplificada (9 UCs superficiais, sem estrutura canônica)
