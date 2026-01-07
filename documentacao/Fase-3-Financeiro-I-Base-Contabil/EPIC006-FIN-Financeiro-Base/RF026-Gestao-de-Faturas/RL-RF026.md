# RL-RF026 — Referência ao Legado: Gestão de Faturas

**Versão:** 1.0
**Data:** 2025-12-30
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF-026 (Gestão Completa de Faturas de Telecom e TI)
**Sistema Legado:** VB.NET + ASP.NET Web Forms
**Objetivo:** Documentar o comportamento do sistema legado de gestão de faturas que serve de base para a refatoração, garantindo rastreabilidade, entendimento histórico e mitigação de riscos durante a migração para arquitetura moderna (.NET 10 + Angular 19).

---

## 1. CONTEXTO DO SISTEMA LEGADO

### Stack Tecnológica

- **Arquitetura:** Monolítica ASP.NET Web Forms
- **Linguagem:** VB.NET (Visual Basic .NET)
- **Framework:** .NET Framework 4.5
- **Banco de Dados:** SQL Server 2008 R2
- **Servidor Web:** IIS 7.5
- **Autenticação:** Windows Authentication (Active Directory)
- **Frontend:** ASP.NET Server Controls (ViewState pesado)
- **Integração:** Web Services SOAP (arquivos .asmx)

### Arquitetura Geral

O sistema legado era um monolito sem separação clara de camadas:

- **Presentation:** Arquivos .aspx + code-behind .aspx.vb misturando HTML com lógica de negócio
- **Business Logic:** Regras de negócio embutidas em code-behind + Helpers VB.NET
- **Data Access:** ADO.NET com queries SQL inline (sem ORM)
- **Integration:** WebServices SOAP com processamento síncrono (timeout em arquivos grandes)

### Problemas Arquiteturais Identificados

1. **Falta de Separação de Responsabilidades:** Lógica de negócio misturada com code-behind de telas
2. **Processamento Síncrono:** Upload de faturas grandes (>5MB) causava timeout HTTP
3. **Sem Conciliação Automática:** Controlador comparava manualmente fatura com contratos em planilha Excel (40 horas/mês de trabalho repetitivo)
4. **Sem Auditoria Pré-Pagamento:** Checklist em papel impresso executado APÓS aprovar pagamento (descoberta tardia de erros)
5. **Rateio Manual em Excel:** Planilhas com VLOOKUP complexos que quebravam frequentemente (recalcular = 8 horas de trabalho)
6. **Sem Workflow Formal:** Aprovação por email/telefone sem rastreamento de histórico ou SLA
7. **Layout de Importação Fixo:** Apenas 1 template CSV que quebrava a cada mudança de layout da operadora
8. **Sem OCR:** Faturas em PDF exigiam digitação manual completa
9. **Sem Integração com APIs de Operadoras:** Download manual de faturas mensalmente
10. **Sem Alertas Preditivos:** Descoberta de estouro de budget apenas ao fechar o mês (tarde demais para ação corretiva)
11. **Sem Versionamento:** Correções de faturas sobrescreviam dados anteriores (perda de histórico)
12. **Sem Soft Delete:** DELETE físico impedia auditorias retroativas

### Multi-Tenancy

**Não implementado** - Sistema legado era **single-tenant** com bancos SQL Server separados por cliente (ex: `IControlIT_Cliente01`, `IControlIT_Cliente02`). Mudança para multi-tenancy com Row-Level Security foi decisão crítica do sistema moderno.

### Auditoria

**Parcial** - Apenas log de texto (`Log.txt`) com timestamp e usuário, sem estrutura JSON. Não registrava valores ANTES/DEPOIS de alterações (impossível reverter mudanças).

---

## 2. TELAS DO LEGADO

### Tela: Fatura\Upload.aspx

- **Caminho:** `ic1_legado/IControlIT/Fatura/Upload.aspx`
- **Responsabilidade:** Upload manual de arquivo CSV com layout fixo

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| FileUpload_Fatura | ASP:FileUpload | Sim | Apenas arquivos .csv aceitos |
| DropDownList_Operadora | ASP:DropDownList | Sim | Lista hard-coded de 6 operadoras (Vivo, Claro, TIM, Oi, Embratel, Level 3) |
| TextBox_Periodo | ASP:TextBox | Sim | Formato MM/YYYY sem validação (aceitava "13/2025") |

#### Comportamentos Implícitos

- **Validação de Layout Fixo:** Sistema assumia ordem fixa de colunas no CSV: `NumeroLinha;Descricao;Valor;Quantidade;Data`. Se operadora mudasse ordem, importação quebrava silenciosamente (linhas puladas sem alerta).
- **Timeout em Arquivos Grandes:** Upload de CSV com >1000 linhas causava timeout HTTP 30s do IIS. Usuário precisava quebrar arquivo manualmente em múltiplos CSVs menores.
- **Sem Preview:** Dados importados diretamente no banco sem confirmação do usuário. Se CSV estava errado, precisava deletar manualmente todas as linhas.
- **Encoding Fixo:** Assumia UTF-8. Arquivos em ISO-8859-1 (comum em operadoras) importavam com caracteres corrompidos (ex: "São Paulo" → "S�o Paulo").

**DESTINO:** SUBSTITUÍDO (RF moderno tem engine multi-layout com 15+ templates + auto-detect encoding + preview antes de confirmar)

---

### Tela: Fatura\Lista.aspx

- **Caminho:** `ic1_legado/IControlIT/Fatura/Lista.aspx`
- **Responsabilidade:** Listar faturas importadas sem paginação

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| GridView_Faturas | ASP:GridView | N/A | Sem paginação (carregava TODAS as faturas em memória) |
| DropDownList_Filtro_Operadora | ASP:DropDownList | Não | Filtro client-side (JavaScript) - ineficiente |
| TextBox_Filtro_Periodo | ASP:TextBox | Não | Filtro client-side (JavaScript) - ineficiente |

#### Comportamentos Implícitos

- **Sem Paginação:** Query SQL `SELECT * FROM Fatura` carregava TODAS as faturas (>2.400 registros) em GridView. Com 500+ faturas, página levava 15+ segundos para carregar.
- **Filtros Client-Side:** Filtros aplicados via JavaScript após carregar TODOS os dados. Ineficiente e lento.
- **Sem Ordenação Configurável:** Ordem fixa por `Dt_Emissao DESC`. Usuário não podia ordenar por outras colunas.
- **Sem Status Workflow:** Coluna "Status" mostrava apenas "Paga" ou "Pendente" (sem estados intermediários como "Conciliação", "Auditoria", "Aprovação").

**DESTINO:** SUBSTITUÍDO (RF moderno tem paginação cursor-based server-side + filtros avançados server-side + ordenação configurável + status workflow detalhado)

---

### Tela: Fatura\Detalhes.aspx

- **Caminho:** `ic1_legado/IControlIT/Fatura/Detalhes.aspx`
- **Responsabilidade:** Visualizar detalhes de fatura (cabeçalho + linhas)

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| Label_NumeroFatura | ASP:Label | N/A | Apenas exibição |
| Label_Operadora | ASP:Label | N/A | Apenas exibição |
| Label_ValorTotal | ASP:Label | N/A | Apenas exibição |
| GridView_Linhas | ASP:GridView | N/A | Linhas da fatura sem ordenação |
| TextBox_Observacao | ASP:TextBox | Não | Campo livre sem validação (aceitava SQL injection) |

#### Comportamentos Implícitos

- **Sem Conciliação Visual:** Linhas exibidas sem indicação de quais estavam conciliadas com contratos (usuário precisava verificar manualmente em outra tela).
- **Sem Resultado de Auditoria:** Não exibia se fatura foi auditada ou quais regras falharam.
- **Sem Histórico de Versões:** Se fatura fosse reimportada/corrigida, dados antigos eram sobrescritos (perda de histórico).
- **Sem Timeline de Eventos:** Não mostrava quando fatura foi importada, aprovada, paga (datas dispersas em diferentes campos).

**DESTINO:** SUBSTITUÍDO (RF moderno tem resultado conciliação visual + resultado auditoria destacado + histórico de versões com diff + timeline de eventos completa)

---

### Tela: Fatura\Rateio.aspx

- **Caminho:** `ic1_legado/IControlIT/Fatura/Rateio.aspx`
- **Responsabilidade:** Rateio manual de custos de fatura por centro de custo

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| GridView_Linhas_Fatura | ASP:GridView | N/A | Lista linhas da fatura |
| DropDownList_CentroCusto | ASP:DropDownList | Sim | Seleção manual para cada linha |
| TextBox_Percentual | ASP:TextBox | Sim | Sem validação de soma 100% |
| Button_Salvar | ASP:Button | N/A | Salva rateio sem validar soma percentuais |

#### Comportamentos Implícitos

- **Rateio Item por Item:** Usuário precisava selecionar centro de custo E percentual para CADA linha da fatura manualmente (fatura com 500 linhas = 500 seleções).
- **Sem Validação Soma 100%:** Sistema aceitava rateio com soma ≠ 100% (ex: 60% + 30% = 90%). Descoberta apenas na contabilização (erro contábil).
- **Sem Regras Reutilizáveis:** Rateio precisava ser refeito do zero para cada fatura nova (sem memória de regras anteriores).
- **Sem Dimensões Múltiplas:** Apenas 1 dimensão (Centro Custo). Não suportava rateio por Projeto, Departamento, Geolocalização simultaneamente.
- **Exportação Manual para ERP:** Após salvar, usuário exportava CSV manualmente e importava no ERP (processo propenso a erros).

**DESTINO:** SUBSTITUÍDO (RF moderno tem rateio multi-dimensional automático com 5 dimensões + validação soma 100% + regras reutilizáveis + exportação automática para ERP com retry policy)

---

## 3. WEBSERVICES LEGADOS (.asmx)

### Web Service: Fatura.asmx

- **Caminho:** `ic1_legado/IControlIT/WebServices/Fatura.asmx`
- **Protocolo:** SOAP 1.1
- **Autenticação:** Windows Authentication

#### Método: ImportarFatura()

**Assinatura:**
```vb
Public Function ImportarFatura(ByVal arquivoBase64 As String, ByVal idOperadora As Integer) As Integer
```

**Parâmetros:**
- `arquivoBase64` (String) - Arquivo CSV codificado em Base64
- `idOperadora` (Integer) - ID hard-coded da operadora (1=Vivo, 2=Claro, 3=TIM, 4=Oi, 5=Embratel, 6=Level 3)

**Retorno:**
- `Integer` - ID da fatura criada ou -1 se erro

**Lógica Implícita:**
1. Decodificar Base64 → string CSV
2. Split por linhas (`vbCrLf`)
3. Para cada linha: Split por `;` → parse valores → `INSERT INTO Fatura_Detalhe`
4. Calcular soma total → `INSERT INTO Fatura`
5. Retornar `@@IDENTITY`

**Problemas:**
- **Layout Fixo Assumido:** Ordem fixa de colunas (`NumeroLinha;Descricao;Valor;Qtde;Data`). Mudança de layout quebrava silenciosamente.
- **Sem Validação de Dados:** Aceitava valores inválidos (ex: `Valor = "abc"`). Exception causava rollback parcial (algumas linhas inseridas, outras não).
- **Processamento Síncrono:** Arquivo com >1000 linhas demorava >30s → timeout SOAP.
- **Sem Transação Atômica:** Se falha na linha 500 de 1000, primeiras 499 linhas já estavam no banco (estado inconsistente).
- **Sem Log de Erros:** Exception retornava apenas `-1` sem mensagem específica (usuário não sabia o que deu errado).

**DESTINO:** SUBSTITUÍDO (RF moderno tem endpoint REST `POST /api/v1/faturas/importar` assíncrono com Hangfire + validação FluentValidation + transação atômica EF Core + log estruturado)

---

#### Método: ConsultarFaturas()

**Assinatura:**
```vb
Public Function ConsultarFaturas(ByVal idOperadora As Integer, ByVal periodo As String, ByVal status As String) As DataSet
```

**Parâmetros:**
- `idOperadora` (Integer) - Filtro por operadora (0 = todas)
- `periodo` (String) - Formato "MM/YYYY" sem validação
- `status` (String) - "Paga" ou "Pendente" (case sensitive)

**Retorno:**
- `DataSet` - Tabela com colunas: Id_Fatura, Num_Fatura, Dt_Emissao, Dt_Vencimento, Valor_Total, Status

**Lógica Implícita:**
1. Construir query SQL dinâmica com concatenação de strings (vulnerável a SQL injection)
2. Executar `SqlDataAdapter.Fill(DataSet)`
3. Retornar DataSet completo (sem paginação)

**Problemas:**
- **SQL Injection:** Query construída com concatenação de strings. Parâmetro `status = "'; DROP TABLE Fatura; --"` executaria comando malicioso.
- **Sem Paginação:** Retornava TODAS as faturas que atendem filtro (query lenta com >500 faturas).
- **Sem Ordenação Configurável:** Ordem hard-coded por `Dt_Emissao DESC`.
- **DataSet Pesado:** Serialização SOAP de DataSet com 500+ linhas gerava XML >5MB (lento na rede).
- **Case Sensitive:** Filtro `status = "paga"` (lowercase) retornava 0 resultados (esperava "Paga" com P maiúsculo).

**DESTINO:** SUBSTITUÍDO (RF moderno tem endpoint REST `GET /api/v1/faturas` com paginação cursor-based + filtros parametrizados (protegido contra SQL injection) + ordenação configurável + JSON leve)

---

#### Método: AprovarFatura()

**Assinatura:**
```vb
Public Function AprovarFatura(ByVal idFatura As Integer, ByVal idUsuario As Integer) As Boolean
```

**Parâmetros:**
- `idFatura` (Integer) - ID da fatura a aprovar
- `idUsuario` (Integer) - ID do usuário que aprova

**Retorno:**
- `Boolean` - `True` se aprovado, `False` se erro

**Lógica Implícita:**
1. `UPDATE Fatura SET Fl_Paga = 1, Id_Usuario_Aprovacao = @idUsuario, Dt_Aprovacao = GETDATE() WHERE Id_Fatura = @idFatura`
2. Retornar `True`

**Problemas:**
- **Sem Workflow Multi-Nível:** Aprovação direta sem validar se usuário tem permissão (qualquer usuário podia aprovar qualquer valor).
- **Sem Assinatura Digital:** Aprovação sem validade legal (não auditável em processos jurídicos).
- **Sem Validação de Estado:** Permitia aprovar fatura já paga (dupla aprovação sem bloqueio).
- **Sem Auditoria de Quem Aprovou:** Campo `Id_Usuario_Aprovacao` não rastreava QUEM foi o responsável final (apenas último usuário que tocou).
- **Sem Notificação:** Aprovação silenciosa (gestor não recebia email/push notification).

**DESTINO:** SUBSTITUÍDO (RF moderno tem endpoint REST `POST /api/v1/faturas/{id}/aprovar` com workflow multi-nível + validação de permissões RBAC + assinatura digital DocuSign + auditoria completa + notificações push)

---

#### Método: RatearFatura()

**Assinatura:**
```vb
Public Function RatearFatura(ByVal idFatura As Integer, ByVal rateios As List(Of RateioDto)) As Boolean
```

**DTO:**
```vb
Public Class RateioDto
    Public Id_Linha_Fatura As Integer
    Public Id_Centro_Custo As Integer
    Public Percentual As Decimal
End Class
```

**Parâmetros:**
- `idFatura` (Integer) - ID da fatura
- `rateios` (List) - Lista de rateios por linha

**Retorno:**
- `Boolean` - `True` se sucesso, `False` se erro

**Lógica Implícita:**
1. Para cada `RateioDto`: `INSERT INTO Fatura_Rateio (Id_Fatura, Id_Linha, Id_Centro_Custo, Percentual, Valor) VALUES (...)`
2. Retornar `True`

**Problemas:**
- **Sem Validação Soma 100%:** Aceitava rateio com soma ≠ 100% (erro contábil).
- **Rateio Linha por Linha:** Exigia DTO para CADA linha da fatura (fatura 500 linhas = 500 DTOs no payload SOAP → XML >10MB).
- **Sem Regras Reutilizáveis:** Não salvava regras para reutilizar em faturas futuras.
- **Sem Dimensões Múltiplas:** Apenas 1 dimensão (Centro Custo). Não suportava Projeto + Departamento simultaneamente.
- **Sem Exportação para ERP:** Rateio salvo no banco mas não exportado automaticamente para sistema financeiro (processo manual posterior).

**DESTINO:** SUBSTITUÍDO (RF moderno tem endpoint REST `POST /api/v1/faturas/{id}/ratear` com validação soma 100% + regras reutilizáveis automáticas + rateio multi-dimensional (5 dimensões) + exportação automática ERP com retry policy + DLQ)

---

## 4. STORED PROCEDURES

### Procedure: sp_CalcularTotalFatura

- **Caminho:** `ic1_legado/Database/Procedures/sp_CalcularTotalFatura.sql`
- **Parâmetros Entrada:** `@Id_Fatura INT`
- **Parâmetros Saída:** `@Valor_Total DECIMAL(18,2) OUTPUT`

**Lógica (em linguagem natural):**
1. Somar todos os valores de `Fatura_Detalhe` onde `Id_Fatura = @Id_Fatura`
2. Retornar soma via parâmetro OUTPUT

**Problemas:**
- **Sem Tratamento de Exceção:** Se `Fatura_Detalhe` vazia, retorna NULL (não `0.00`). Code-behind VB.NET não tratava NULL → crash.
- **Sem Validação de Dados:** Aceitava valores negativos em `Fatura_Detalhe` (bug permitia faturas com total negativo).

**DESTINO:** SUBSTITUÍDO (RF moderno tem propriedade computada `ValorTotal` na entidade Fatura com LINQ `_detalhes.Sum(d => d.Valor)` + validação FluentValidation bloqueando valores negativos)

---

### Procedure: sp_BuscarFaturasAtrasadas

- **Caminho:** `ic1_legado/Database/Procedures/sp_BuscarFaturasAtrasadas.sql`
- **Parâmetros Entrada:** `@Dias_Atraso INT`
- **Parâmetros Saída:** N/A (retorna tabela)

**Lógica (em linguagem natural):**
1. Selecionar faturas onde `Dt_Vencimento < GETDATE() - @Dias_Atraso` E `Fl_Paga = 0`
2. Retornar tabela com colunas: Id_Fatura, Num_Fatura, Dt_Vencimento, Dias_Atraso_Calculado

**Problemas:**
- **Sem Índice na Query:** Query fazia full table scan em `Fatura` (lento com >5000 faturas).
- **Lógica de Negócio em Procedure:** Regra "considerado atrasado se >X dias" estava hard-coded em procedure (difícil alterar).

**DESTINO:** SUBSTITUÍDO (RF moderno tem query LINQ com índice composto (Fl_Paga, Dt_Vencimento) + regra de negócio em Application Layer configurável via appsettings.json)

---

## 5. TABELAS LEGADAS

### Tabela: Fatura

**Schema:** `[dbo].[Fatura]`

**Problemas Identificados:**
1. **Falta Foreign Key para Operadora:** Campo `Id_Operadora` INT sem FK → permitia referências órfãs (ID inexistente)
2. **Sem Campos de Auditoria:** Faltavam `Created`, `CreatedBy`, `LastModified`, `LastModifiedBy` (impossível rastrear quem criou/alterou)
3. **Sem Multi-Tenancy:** Faltava `ClienteId` (banco separado por cliente → migração para multi-tenancy complexa)
4. **DELETE Físico:** Sistema fazia `DELETE FROM Fatura` → perda de histórico (violação compliance fiscal 7 anos)
5. **Sem Soft Delete:** Faltava `FlExcluido` → impossível recuperar faturas deletadas acidentalmente
6. **Campo Status Limitado:** Apenas `Fl_Paga` (0/1) → sem estados intermediários (Conciliação, Auditoria, Aprovação)
7. **Sem Versionamento:** Reimportação sobrescrevia dados → perda de histórico de alterações

**Mapeamento para Tabela Moderna:**
`[dbo].[Fatura]` (legado) → `Fatura` (moderno) com adição de 40+ campos:
- Multi-tenancy: `ClienteId`
- Auditoria: `Created`, `CreatedBy`, `LastModified`, `LastModifiedBy`
- Soft Delete: `FlExcluido`, `DeletedAt`, `DeletedBy`
- Workflow: `Status` (Enum: Rascunho, AguardandoConciliacao, AguardandoAuditoria, AguardandoAprovacao, Aprovada, Paga, Contestada, Cancelada)
- OCR: `OCR_Confidence_Score`, `OCR_Raw_JSON`
- Importação: `Template_Id`, `Arquivo_Original_Blob_URL`
- Integração: `ERP_Sincronizado`, `ERP_Documento_Numero`, `ERP_Data_Sync`
- Versionamento: `Numero_Versao`, `Versao_Atual_Flag`

**DESTINO:** SUBSTITUÍDO (tabela redesenhada com multi-tenancy, auditoria completa, soft delete, workflow estados, versionamento, OCR metadata, integração ERP)

---

### Tabela: Fatura_Detalhe

**Schema:** `[dbo].[Fatura_Detalhe]`

**Problemas Identificados:**
1. **Sem Conciliação:** Faltavam `Conciliado`, `Id_Contrato_Item`, `Id_Ativo`, `Match_Score` → conciliação manual em Excel
2. **Sem Resultado Auditoria:** Faltavam `Auditoria_Status`, `Auditoria_Regras_Falhas_JSON` → auditoria manual em papel
3. **Sem Rateio Vinculado:** Faltavam `Rateio_Centro_Custo`, `Rateio_Projeto`, `Rateio_Departamento` → rateio em planilha separada
4. **DELETE Físico:** Permitia deletar linhas individuais → perda de histórico
5. **Sem Soft Delete:** Faltava `FlExcluido`

**Mapeamento para Tabela Moderna:**
`[dbo].[Fatura_Detalhe]` (legado) → `Fatura_Detalhe` (moderno) com adição de campos de conciliação, auditoria, rateio, soft delete

**DESTINO:** SUBSTITUÍDO (tabela redesenhada com conciliação automática, auditoria vinculada, rateio multi-dimensional vinculado, soft delete)

---

### Tabela: Fatura_Rateio

**Schema:** `[dbo].[Fatura_Rateio]`

**Problemas Identificados:**
1. **Apenas 1 Dimensão:** Apenas `Id_Centro_Custo` → não suportava Projeto, Departamento, Geolocalização, Tipo Serviço simultaneamente
2. **Sem Regras Reutilizáveis:** Rateio item por item sem memória de regras → necessário refazer manualmente toda fatura
3. **Sem Validação Soma 100%:** Permitia rateio com soma ≠ 100% → erro contábil
4. **DELETE Físico:** Recalcular rateio deletava anteriores → perda de histórico

**Mapeamento para Tabela Moderna:**
`[dbo].[Fatura_Rateio]` (legado) → `Fatura_Detalhe.Rateio_*` (moderno) com campos JSON multi-dimensionais + nova tabela `Fatura_Rateio_Regra` para regras reutilizáveis

**DESTINO:** SUBSTITUÍDO (estrutura redesenhada com 5 dimensões, regras reutilizáveis, validação soma 100%, histórico de recálculos preservado)

---

## 6. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

### RL-RN-001: Importação Assume Encoding UTF-8

**Fonte:** `ic1_legado/IControlIT/Fatura/Upload.aspx.vb` - Linha 145
```vb
Dim reader As New StreamReader(fileStream, Encoding.UTF8)
```

**Descrição:** Sistema assume que todos os arquivos CSV são UTF-8. Arquivos em ISO-8859-1 (comum em operadoras brasileiras) importam com caracteres corrompidos.

**DESTINO:** SUBSTITUÍDO (RF moderno tem auto-detect de encoding: UTF-8, ISO-8859-1, Windows-1252)

---

### RL-RN-002: Valor Fatura Calculado como Soma de Detalhes

**Fonte:** `ic1_legado/Database/Procedures/sp_CalcularTotalFatura.sql` - Linha 8
```sql
SELECT @Valor_Total = SUM(Valor) FROM Fatura_Detalhe WHERE Id_Fatura = @Id_Fatura
```

**Descrição:** Valor total da fatura é sempre calculado como soma simples de linhas detalhadas. Não considera descontos globais, acréscimos, impostos separados (ICMS, PIS, COFINS).

**DESTINO:** ASSUMIDO (RF moderno mantém cálculo por soma mas adiciona campos separados para descontos, acréscimos, impostos)

---

### RL-RN-003: Aprovação Permitida Apenas se Fl_Paga = 0

**Fonte:** `ic1_legado/IControlIT/WebServices/Fatura.asmx.vb` - Linha 312
```vb
If (fatura.Fl_Paga = True) Then
    Return False ' Já aprovada
End If
```

**Descrição:** Sistema bloqueia dupla aprovação verificando flag `Fl_Paga`. Porém não valida se usuário tem permissão para aprovar valores altos.

**DESTINO:** ASSUMIDO (RF moderno mantém bloqueio de dupla aprovação mas adiciona workflow multi-nível com validação de permissões RBAC por valor)

---

### RL-RN-004: Rateio Permite Soma ≠ 100%

**Fonte:** `ic1_legado/IControlIT/Fatura/Rateio.aspx.vb` - Linha 256
```vb
' Nenhuma validação de soma de percentuais
btnSalvar_Click() ' Salva direto no banco
```

**Descrição:** Sistema não valida se soma de percentuais de rateio = 100%. Permite salvar rateio com soma 90% ou 110% (erro contábil descoberto apenas na contabilização posterior).

**DESTINO:** SUBSTITUÍDO (RF moderno bloqueia salvamento se soma ≠ 100% com validação FluentValidation retornando HTTP 400)

---

### RL-RN-005: Filtro de Operadora é Case Sensitive

**Fonte:** `ic1_legado/IControlIT/WebServices/Fatura.asmx.vb` - Linha 178
```vb
WHERE Status = @status ' Comparação case sensitive no SQL Server
```

**Descrição:** Filtro `status = "paga"` (lowercase) retorna 0 resultados porque comparação SQL Server padrão é case sensitive e banco tem "Paga" com P maiúsculo.

**DESTINO:** DESCARTADO (RF moderno usa Enum C# `FaturaStatus` com valores tipados → impossível erro de case)

---

### RL-RN-006: DELETE Físico Permitido em Faturas

**Fonte:** `ic1_legado/IControlIT/Fatura/Lista.aspx.vb` - Linha 89
```vb
ExecuteNonQuery("DELETE FROM Fatura WHERE Id_Fatura = @id")
```

**Descrição:** Botão "Excluir" fazia DELETE físico no banco sem soft delete. Perda permanente de histórico (violação compliance fiscal que exige 7 anos de retenção).

**DESTINO:** SUBSTITUÍDO (RF moderno usa soft delete obrigatório `FlExcluido = TRUE` + EF Core Query Filter global)

---

### RL-RN-007: Conciliação Manual em Planilha Excel

**Fonte:** Processo manual não documentado no código
**Descrição:** Controlador exportava fatura para Excel, abria planilha de contratos, usava VLOOKUP para tentar conciliar cada linha com contrato correspondente. Processo demorava 40 horas/mês.

**DESTINO:** SUBSTITUÍDO (RF moderno tem conciliação automática com algoritmo fuzzy matching Levenshtein distance 90% + matching exato + sugestões top 3 para match <90%)

---

### RL-RN-008: Auditoria Manual em Checklist Papel

**Fonte:** Processo manual não documentado no código
**Descrição:** Controlador imprimia checklist em papel com 12 itens de verificação (linha sem contrato, valor suspeito, serviço cancelado cobrado, etc.) e verificava manualmente APÓS aprovar pagamento (descoberta tardia).

**DESTINO:** SUBSTITUÍDO (RF moderno tem auditoria automática pré-pagamento com 25+ regras configuráveis + severidade (Alta bloqueia, Média exige justificativa, Baixa alerta))

---

### RL-RN-009: Workflow de Aprovação por Email

**Fonte:** Processo manual não documentado no código
**Descrição:** Controlador enviava email para gestor com PDF da fatura anexado. Gestor respondia email com "Aprovado" ou "Negado". Sem rastreamento formal de histórico ou SLA.

**DESTINO:** SUBSTITUÍDO (RF moderno tem workflow formal 7 etapas + assinatura digital DocuSign + rastreamento SLA + alertas se operadora não responde em 80% do prazo)

---

### RL-RN-010: Sem Alertas de Estouro de Budget

**Fonte:** Funcionalidade inexistente no legado
**Descrição:** Sistema não tinha alertas preditivos. Descoberta de estouro de budget apenas ao fechar mês (tarde demais para ação corretiva).

**DESTINO:** SUBSTITUÍDO (RF moderno tem alertas preditivos ML com 7/15/30 dias antecedência + sugestões automáticas de ação corretiva)

---

## 7. GAP ANALYSIS (LEGADO × MODERNO)

### Funcionalidades Legado NÃO Migradas

| Funcionalidade Legado | Motivo Não Migração | Alternativa Moderna |
|-----------------------|---------------------|---------------------|
| Upload via FTP de servidor | Obsoleto (inseguro) | Upload HTTP com autenticação JWT |
| Impressão de relatórios em papel | Obsoleto (desperdício) | Exportação PDF com assinatura digital |
| Backup manual em fitas magnéticas | Obsoleto (tecnologia antiga) | Backup automático Azure Blob Storage |
| Integração via arquivos TXT em pasta compartilhada | Inseguro e propenso a erros | API REST com autenticação OAuth 2.0 |

### Funcionalidades Novas do Sistema Moderno (Não Existiam no Legado)

| Funcionalidade Moderna | Descrição | Impacto |
|------------------------|-----------|---------|
| OCR de PDF | Extração automática de dados via Azure Form Recognizer | Elimina digitação manual (economia 20h/mês) |
| Conciliação Automática | Algoritmo fuzzy matching 90% | Reduz conciliação de 40h/mês para 2h/mês |
| Auditoria Pré-Pagamento | 25+ regras configuráveis | Recupera 12-18% do valor em cobranças indevidas |
| Workflow Contestação | 7 etapas com rastreamento SLA | Taxa sucesso contestações 70% (antes 40%) |
| Rateio Multi-Dimensional | 5 dimensões, 5 tipos de rateio | Reduz rateio de 8h para <2s |
| Dashboard Executivo | 10+ KPIs Chart.js tempo real SignalR | Visibilidade gerencial instantânea |
| Alertas Preditivos ML | Random Forest prevê estouro 30 dias antes | Ações preventivas (antes impossível) |
| Integração APIs Operadoras | Download automático faturas | Elimina download manual mensal |
| App Mobile MAUI | Aprovação on-the-go | Gestores aprovam em viagem |
| Assinatura Digital DocuSign | Validade legal de aprovações | Compliance SOX |
| Versionamento de Faturas | Histórico completo de alterações | Auditoria retroativa |
| Soft Delete | Preservação 7 anos | Compliance fiscal |

### Mudanças de Comportamento Entre Legado e Moderno

| Comportamento | Legado | Moderno | Impacto |
|---------------|--------|---------|---------|
| Multi-tenancy | Bancos separados por cliente | Row-Level Security | Consolidação infraestrutura |
| Processamento Importação | Síncrono (timeout 30s) | Assíncrono (Hangfire) | Arquivos grandes sem timeout |
| Aprovação | Email sem rastreamento | Workflow + DocuSign | Rastreabilidade total |
| Auditoria | Manual após pagar | Automática antes pagar | Economia 12-18% |
| Rateio | Manual item por item | Automático com regras | Redução 8h → 2s |
| Conciliação | Manual Excel 40h/mês | Automática 2h/mês | Ganho eficiência 95% |

---

## 8. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Mitigação |
|-------|---------|-----------|
| **Perda de dados históricos durante migração** | ALTO | Script de migração com validação 100% integridade + rollback automático se falha |
| **Quebra de integrações com ERPs existentes** | ALTO | Manter endpoints SOAP legados ativos por 6 meses (período transição) + testes integração antes de desligar |
| **Curva de aprendizado usuários** | MÉDIO | Treinamento obrigatório 8 horas + manuais em vídeo + suporte técnico 24/7 primeiro mês |
| **Falha de OCR em faturas com qualidade ruim** | MÉDIO | Fallback para revisão manual com UI side-by-side + re-treinamento modelo ML mensalmente |
| **Resistência a mudança de processo (auditoria pré vs pós-pagamento)** | MÉDIO | Comunicação executiva mostrando ROI (economia 12-18%) + casos de sucesso piloto |
| **Timeout em migração de bancos grandes (>10GB)** | BAIXO | Migração em lotes (1000 faturas por vez) + execução noturna (janela manutenção) |
| **Incompatibilidade de layouts de operadoras não testados** | BAIXO | Fase piloto 3 meses com operadoras principais (Vivo, Claro, TIM) + builder visual para customização |

---

## 9. RASTREABILIDADE (LEGADO → MODERNO)

### Telas Legado → Angular Moderno

| Tela ASP.NET WebForms | Componente Angular | Melhorias |
|-----------------------|-------------------|-----------|
| Fatura\Upload.aspx | /faturas/importar | Multi-layout picker + OCR preview |
| Fatura\Lista.aspx | /faturas | Filtros avançados + paginação server-side + status workflow |
| Fatura\Detalhes.aspx | /faturas/{id} | Timeline versões + auditoria visual + conciliação destacada |
| Fatura\Rateio.aspx | /faturas/{id}/rateio | Regras automáticas + preview rateio + validação soma 100% |
| N/A (não existia) | /faturas/contestacoes | Workflow completo + SLA tracking + histórico completo |
| N/A (Excel estático) | /dashboard/faturas | Chart.js tempo real + drill-down + exportação PDF/Excel |
| N/A (não existia) | /faturas/templates/builder | Visual builder drag-drop para criar layouts customizados |

### WebServices SOAP → REST API

| Método SOAP Legado | Endpoint REST Moderno | Melhorias |
|--------------------|---------------------|-----------|
| ImportarFatura() | POST /api/v1/faturas/importar | Multi-layout + assíncrono Hangfire + validação FluentValidation + transação atômica |
| ConsultarFaturas() | GET /api/v1/faturas | Paginação cursor-based + filtros parametrizados + JSON leve |
| AprovarFatura() | POST /api/v1/faturas/{id}/aprovar | Workflow multi-nível + RBAC + assinatura digital DocuSign |
| RatearFatura() | POST /api/v1/faturas/{id}/ratear | Validação soma 100% + regras reutilizáveis + multi-dimensional |
| N/A | POST /api/v1/faturas/importar/ocr | OCR PDF Azure Form Recognizer |
| N/A | POST /api/v1/faturas/{id}/conciliar | Conciliação automática fuzzy matching |
| N/A | POST /api/v1/faturas/{id}/auditar | Auditoria configurável 25+ regras |
| N/A | POST /api/v1/faturas/{id}/contestacoes | Workflow contestação 7 etapas |
| N/A | GET /api/v1/faturas/dashboard | Dashboard KPIs tempo real SignalR |
| N/A | GET /api/v1/faturas/dashboard/alertas | Alertas preditivos ML |

### Stored Procedures → LINQ Queries

| Procedure SQL Legado | Query LINQ Moderno | Melhorias |
|----------------------|-------------------|-----------|
| sp_CalcularTotalFatura | `_detalhes.Sum(d => d.Valor)` | Propriedade computada + validação valores negativos |
| sp_BuscarFaturasAtrasadas | `Where(f => f.DataVencimento < DateTime.Now.AddDays(-X) && !f.Fl_Paga)` | Índice composto + regra configurável appsettings.json |

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|--------|------|-----------|-------|
| 1.0 | 2025-12-30 | Documentação completa do sistema legado de gestão de faturas VB.NET/ASP.NET Web Forms. Extração de regras implícitas do código, mapeamento de telas/webservices/procedures/tabelas, gap analysis legado×moderno, identificação de riscos de migração. | Agência ALC - alc.dev.br |
