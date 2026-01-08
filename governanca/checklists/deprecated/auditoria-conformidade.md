# CHECKLIST DE AUDITORIA DE CONFORMIDADE

Este checklist é um guia rápido para executar auditorias conforme **CONTRATO-AUDITORIA-CONFORMIDADE.md**.

---

## AUDITORIA BACKEND

### 1. ENTIDADES (Domain/Entities/)

**Comparar:** `MD-RFXXX.md` (Modelo de Dados) vs `NomeDaEntidade.cs`

- [ ] Todos os campos especificados no MD estão presentes na entidade
- [ ] Tipos de dados correspondem (string, int, Guid, decimal, bool, DateTime)
- [ ] Propriedades obrigatórias marcadas como `required` ou sem `?`
- [ ] Propriedades opcionais marcadas com `?`
- [ ] MaxLength configurado conforme especificação
- [ ] Campos de auditoria presentes (CreatedBy, CreatedAt, UpdatedBy, UpdatedAt)
- [ ] Campos de multi-tenancy presentes (ClienteId, EmpresaId)
- [ ] Campos de soft-delete presentes (FlExcluido)
- [ ] Navigation Properties configuradas para FKs
- [ ] Nenhum campo extra não especificado (ou justificado)

**Gaps Comuns:**
- Campo `TipoId` (FK) ausente
- Campos de contato (Contato, Telefone, Email) ausentes
- Campos booleanos (FlPadrao, FlValidado) ausentes
- Campos de geocodificação (Latitude, Longitude) ausentes

---

### 2. CONFIGURATIONS (Infrastructure/Data/Configurations/)

**Comparar:** `MD-RFXXX.md` vs `NomeDaEntidadeConfiguration.cs`

- [ ] Tabela nomeada corretamente (plural: `EnderecoEntregas`)
- [ ] Primary Key configurada (`HasKey(e => e.Id)`)
- [ ] Campos obrigatórios marcados com `IsRequired()`
- [ ] MaxLength aplicado conforme MD
- [ ] Índices únicos criados conforme especificação
- [ ] Foreign Keys configuradas com `HasOne().WithMany().HasForeignKey()`
- [ ] `OnDelete` configurado corretamente (Restrict/Cascade)
- [ ] Precision configurada para decimais (ex: Latitude/Longitude)
- [ ] Filtros únicos aplicados (ex: `HasFilter("[FlPadrao] = 1")`)

**Gaps Comuns:**
- FK não configurada no EF Core
- Índice único faltando
- OnDelete incorreto (Cascade quando deveria ser Restrict)

---

### 3. COMMANDS (Application/.../Commands/)

**Comparar:** `UC-RFXXX.md` (Casos de Uso) vs `CreateXCommand.cs`, `UpdateXCommand.cs`

- [ ] Todos os campos do formulário (UC01) estão no Command
- [ ] Campos obrigatórios marcados com `required` ou validação
- [ ] Tipos de dados corretos
- [ ] Nenhum campo sensível exposto (ex: senha sem hash)

**Gaps Comuns:**
- Campo TipoId ausente no CreateCommand
- Campos de contato ausentes

---

### 4. VALIDATORS (Application/.../Commands/)

**Comparar:** Regras de Negócio (RN-XXX) no RF vs `XCommandValidator.cs`

- [ ] Todas as regras RN-XXX estão implementadas
- [ ] Validação de campos obrigatórios (`NotEmpty()`)
- [ ] Validação de MaxLength (`MaximumLength()`)
- [ ] Validação de formatos (Email, Telefone, CPF, CNPJ, CEP)
- [ ] Validação de ranges (InclusiveBetween para Latitude/Longitude)
- [ ] Validações customizadas (ex: apenas 1 endereço padrão por tipo)
- [ ] Mensagens de erro em português

**Gaps Comuns:**
- Regra RN-XXX especificada mas não validada no código
- Validação de formato ausente (ex: Telefone deve ser `(00) 00000-0000`)
- Validação de unicidade ausente

---

### 5. DTOs (Application/.../Queries/)

**Comparar:** `UC-RFXXX.md` (Campos de listagem) vs `XDto.cs`

- [ ] Todos os campos necessários para exibição estão no DTO
- [ ] Campos de navegação incluídos (ex: `TipoNome` ao invés de apenas `TipoId`)
- [ ] Campos sensíveis NÃO expostos
- [ ] Tipos de dados corretos

**Gaps Comuns:**
- DTO retorna apenas `TipoId` mas tela precisa mostrar `TipoNome`
- Campos calculados ausentes

---

### 6. HANDLERS (Application/.../Commands/ e Queries/)

**Comparar:** Regras de Negócio (RN-XXX) vs lógica no Handler

- [ ] Todas as regras RN-XXX estão implementadas no Handler
- [ ] Validação de endereço padrão único (se aplicável)
- [ ] Autorização verificada (ClienteId, EmpresaId)
- [ ] Soft-delete ao invés de DELETE físico
- [ ] Auditoria preenchida automaticamente (CreatedBy, UpdatedAt)

**Gaps Comuns:**
- Regra de negócio RN-043-001 (apenas 1 padrão por tipo) não implementada
- Soft-delete não aplicado (usa `Remove()` ao invés de `FlExcluido = true`)

---

### 7. ENDPOINTS (Web/Endpoints/)

**Comparar:** `UC-RFXXX.md` (Operações) vs `Xs.cs`

- [ ] Endpoint GET (listar) implementado
- [ ] Endpoint GET/{id} (buscar por ID) implementado
- [ ] Endpoint POST (criar) implementado
- [ ] Endpoint PUT/{id} (atualizar) implementado
- [ ] Endpoint DELETE/{id} (excluir) implementado
- [ ] Autenticação exigida (`RequireAuthorization()`)
- [ ] Política de autorização correta (Policy vs Role)
- [ ] Swagger documentado (`WithSummary()`)
- [ ] Respostas HTTP corretas (200, 201, 404, 401, 403, 500)

**Gaps Comuns:**
- Endpoint de tipos (ex: `GET /enderecos-entrega-tipos`) ausente
- Autorização usando Role ao invés de Policy

---

### 8. SEEDS (Infrastructure/Data/ApplicationDbContextInitialiser.cs)

**Comparar:** `RFXXX.md` (Dados Iniciais) vs código de seed

- [ ] Entidades de lookup semeadas (ex: EnderecoEntregaTipo)
- [ ] Permissões criadas e nomeadas corretamente
- [ ] Permissões associadas ao perfil Developer
- [ ] Funcionalidade registrada na Central de Módulos
- [ ] Seeds idempotentes (verificam existência antes de criar)
- [ ] Nenhum seed hardcoded (usar constantes/configurações)

**Gaps Comuns:**
- Tabela de tipos (EnderecoEntregaTipo) sem seed
- Permissões criadas mas NÃO associadas ao perfil Developer
- Central de Módulos não atualizada

---

## AUDITORIA FRONTEND

### 1. COMPONENTES (src/app/.../components/)

**Comparar:** `WF-RFXXX.md` (Wireframes) vs componentes `.ts` e `.html`

- [ ] Componente de listagem implementado
- [ ] Componente de formulário (criar/editar) implementado
- [ ] Componente de detalhes (se especificado) implementado
- [ ] Todos os campos do wireframe estão presentes no template
- [ ] Tipos de input corretos (text, number, select, checkbox, date)

**Gaps Comuns:**
- Campo `Tipo` (dropdown) ausente no formulário
- Checkbox `FlPadrao` ausente

---

### 2. FORMULÁRIOS E VALIDAÇÕES

**Comparar:** `UC-RFXXX.md` (Campos obrigatórios) vs `form.component.ts`

- [ ] FormGroup criado com todos os campos
- [ ] Validações obrigatórias (`Validators.required`)
- [ ] Validações de formato (email, pattern para telefone/CEP)
- [ ] Validações de range (min, max para números)
- [ ] Mensagens de erro exibidas em português
- [ ] Mensagens de erro traduzidas (i18n)
- [ ] Desabilitar campos quando aplicável (ex: CEP validado auto-preenche)

**Gaps Comuns:**
- Campo obrigatório sem `Validators.required`
- Validação de telefone ausente (deveria validar formato `(00) 00000-0000`)
- Mensagens de erro hardcoded ao invés de i18n

---

### 3. SERVICES (src/app/.../services/)

**Comparar:** Endpoints do backend vs chamadas HTTP no service

- [ ] Método `getAll()` implementado
- [ ] Método `getById(id)` implementado
- [ ] Método `create(dto)` implementado
- [ ] Método `update(id, dto)` implementado
- [ ] Método `delete(id)` implementado
- [ ] Método para buscar tipos/lookups (ex: `getTipos()`)
- [ ] Headers corretos (Subscription-Key, Authorization)
- [ ] Tratamento de erros (catchError)

**Gaps Comuns:**
- Método `getTipos()` ausente (dropdown não carrega)
- Subscription-Key não enviado no header

---

### 4. ROTAS E GUARDS

**Comparar:** `WF-RFXXX.md` (Navegação) vs `app-routing.module.ts`

- [ ] Rota de listagem configurada
- [ ] Rota de criação configurada
- [ ] Rota de edição configurada (com parâmetro `:id`)
- [ ] Guard de autenticação aplicado
- [ ] Guard de permissão aplicado (PolicyGuard)
- [ ] Lazy loading configurado

**Gaps Comuns:**
- Rota sem Guard de permissão
- PolicyGuard usando Role ao invés de Policy

---

### 5. TRADUÇÕES (src/assets/i18n/)

**Comparar:** Todos os textos exibidos vs arquivos `pt.json`, `en.json`, `es.json`

- [ ] Título da tela traduzido
- [ ] Labels de campos traduzidos
- [ ] Placeholders traduzidos
- [ ] Mensagens de sucesso traduzidas
- [ ] Mensagens de erro traduzidas
- [ ] Mensagens de confirmação traduzidas
- [ ] Botões traduzidos
- [ ] 3 idiomas (pt, en, es)

**Gaps Comuns:**
- Chaves i18n criadas apenas em `pt.json` (faltam en.json e es.json)
- Texto hardcoded no template ao invés de usar `{{ 'KEY' | translate }}`

---

### 6. MODELS/INTERFACES

**Comparar:** DTOs do backend vs interfaces TypeScript

- [ ] Interface criada para a entidade principal
- [ ] Propriedades correspondem ao DTO do backend
- [ ] Tipos TypeScript corretos (string, number, boolean, Date)
- [ ] Propriedades opcionais marcadas com `?`

**Gaps Comuns:**
- Interface desatualizada (falta propriedade `TipoId`)
- Tipo incorreto (string ao invés de number)

---

## AUDITORIA DE INTEGRAÇÕES OBRIGATÓRIAS

### CENTRAL DE FUNCIONALIDADES

- [ ] Funcionalidade registrada em `CentralDeFuncionalidadesSeeds`
- [ ] Código único (ex: `ENDERECOS_ENTREGA`)
- [ ] Nome, Descrição, Ícone configurados
- [ ] Ordem de exibição definida

---

### I18N (INTERNACIONALIZAÇÃO)

- [ ] Todas as chaves criadas em `pt.json`
- [ ] Todas as chaves criadas em `en.json`
- [ ] Todas as chaves criadas em `es.json`
- [ ] Nenhum texto hardcoded no frontend
- [ ] Nenhum texto hardcoded no backend (mensagens de validação)

---

### AUDITORIA (CAMPOS DE AUDITORIA)

- [ ] Entidade herda de `BaseAuditableGuidEntity`
- [ ] CreatedBy preenchido automaticamente
- [ ] CreatedAt preenchido automaticamente
- [ ] UpdatedBy atualizado automaticamente
- [ ] UpdatedAt atualizado automaticamente

---

### MULTI-TENANCY

- [ ] `ClienteId` presente na entidade
- [ ] `EmpresaId` presente na entidade (se aplicável)
- [ ] Queries filtram por `ClienteId` automaticamente
- [ ] Commands validam `ClienteId` do usuário logado

---

### PERMISSÕES (RBAC)

- [ ] Permissões criadas com nomenclatura correta (ex: `Enderecos.Visualizar`)
- [ ] Permissões associadas ao perfil Developer
- [ ] Endpoints protegidos com Policy (não Role)
- [ ] Frontend protegido com PolicyGuard

---

## RELATÓRIO DE GAPS - TEMPLATE RESUMIDO

```markdown
# GAPS-RFXXX-BACKEND.md

## 🔴 CRÍTICOS (N)
1. [Título] - Arquivo:linha - Impacto

## 🟡 IMPORTANTES (N)
1. [Título] - Arquivo:linha - Impacto

## 🟢 MENORES (N)
1. [Título] - Arquivo:linha - Impacto

## RECOMENDAÇÃO
Contrato: [MANUTENCAO/EXECUCAO-BACKEND/EXECUCAO-FRONTEND]
```

---

## QUANDO USAR ESTE CHECKLIST

1. **Antes de marcar RF como concluído:** Validar conformidade
2. **Durante code review:** Verificar se implementação está completa
3. **Após implementação de backend:** Auditar antes de iniciar frontend
4. **Após implementação de frontend:** Auditar antes de executar testes E2E
5. **Em caso de bugs recorrentes:** Verificar se gap de validação existe

---

## FLUXO COMPLETO DE AUDITORIA

```
1. Ativar CONTRATO-AUDITORIA-CONFORMIDADE.md
2. Criar todo list de auditoria
3. Usar este checklist como guia
4. Identificar gaps
5. Gerar relatório GAPS-RFXXX-*.md
6. Salvar em documentacao/<fase>/<epic>/<RF>/
7. Declarar status: CONFORME / NÃO CONFORME / CONFORME COM RESSALVAS
8. Se gaps críticos existirem → Executar correções sob outro contrato
9. Re-auditar após correções
```

---

**Este checklist complementa o CONTRATO-AUDITORIA-CONFORMIDADE.md e NÃO deve ser usado isoladamente.**
