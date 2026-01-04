# Base de Conhecimento - Backend e Frontend

Este diretório contém **bases de conhecimento acumuladas** de problemas, soluções e boas práticas encontradas durante o desenvolvimento do IControlIT.

## Arquivos

| Arquivo | Descrição |
|---------|-----------|
| [backend.yaml](backend.yaml) | Problemas, soluções e padrões para backend (.NET 8 + EF Core) |
| [frontend.yaml](frontend.yaml) | Problemas, soluções e padrões para frontend (Angular 18 + PrimeNG) |

---

## Propósito

Estes arquivos funcionam como **memória institucional** do projeto:

- **Antes de criar**: Consultar padrões e boas práticas
- **Antes de corrigir**: Verificar se problema já foi resolvido antes
- **Antes de adequar**: Validar se há soluções conhecidas
- **Após resolver**: Documentar problema e solução para futuras referências

---

## Como Usar

### 1. Consulta Pré-Execução

**Antes de executar qualquer contrato (criação, adequação, correção):**

```bash
# Backend
cat docs/base-conhecimento/backend.yaml

# Frontend
cat docs/base-conhecimento/frontend.yaml
```

**O que procurar:**
- Problemas similares ao que você está resolvendo
- Erros comuns relacionados à tecnologia que vai usar
- Padrões obrigatórios para a funcionalidade
- Checklist pré-execução

### 2. Durante Correção/Manutenção

**Ao enfrentar um erro:**

1. Procurar em `erros_comuns:` se o erro já é conhecido
2. Verificar `troubleshooting:` para soluções rápidas
3. Se encontrar solução, aplicar
4. Se não encontrar, resolver e **documentar** (ver seção abaixo)

### 3. Documentar Novo Problema

**Após resolver um problema novo, adicionar ao YAML:**

```yaml
problemas:
  - problema: "Descrição clara e concisa"
    contexto: "RF específico ou cenário genérico"
    sintoma: "Como o erro apareceu (mensagem, comportamento)"
    causa_raiz: "Por que aconteceu (análise técnica)"
    solucao: |
      Passo a passo da solução aplicada:
      1. Primeiro passo
      2. Segundo passo
      3. Código exemplo (se aplicável)
    arquivos_afetados:
      - "caminho/arquivo1.cs"
      - "caminho/arquivo2.ts"
    data_registro: "YYYY-MM-DD"
    tags: [categoria1, categoria2, categoria3]
```

---

## Estrutura dos Arquivos

### backend.yaml

```yaml
problemas:         # Problemas conhecidos e soluções
padroes:           # Padrões e boas práticas obrigatórias
erros_comuns:      # Erros frequentes e fix rápido
checklist_pre_execucao:  # Validações antes de iniciar
troubleshooting:   # Soluções rápidas por categoria
referencias:       # Links para docs, comandos, URLs
notas:             # Regras importantes (SEMPRE/NUNCA)
```

### frontend.yaml

```yaml
problemas:         # Problemas conhecidos e soluções
padroes:           # Padrões e boas práticas obrigatórias
erros_comuns:      # Erros frequentes e fix rápido
checklist_pre_execucao:  # Validações antes de iniciar
troubleshooting:   # Soluções rápidas por categoria
layout_padrao:     # Estrutura UI padrão (card, botões, cores)
referencias:       # Links para docs, comandos, URLs
notas:             # Regras importantes (SEMPRE/NUNCA)
```

---

## Exemplos de Uso

### Exemplo 1: Erro de AutoMapper no Backend

**Situação:** Erro ao mapear DTO com propriedades de multi-tenancy

**Consulta:**
```bash
grep -A 20 "AutoMapper" docs/base-conhecimento/backend.yaml
```

**Resultado:** Encontra problema conhecido com solução pronta

### Exemplo 2: Rota 404 no Frontend

**Situação:** Nova rota não carrega após adicionar ao menu

**Consulta:**
```bash
grep -A 20 "404" docs/base-conhecimento/frontend.yaml
```

**Resultado:** Encontra checklist de validação de rotas

### Exemplo 3: Novo Padrão Obrigatório

**Situação:** Time define que todo handler deve validar permissões

**Ação:** Adicionar em `padroes:` do backend.yaml para futuras referências

---

## Boas Práticas de Documentação

### O que documentar

✅ **SIM - Documentar:**
- Erros que demoraram > 30min para resolver
- Problemas que se repetiram em múltiplos RFs
- Soluções não óbvias ou contra-intuitivas
- Padrões técnicos definidos pela equipe
- Erros de configuração (EF Core, Angular, etc.)

❌ **NÃO - Não documentar:**
- Erros triviais (typo, import faltando)
- Problemas específicos de um RF único
- Soluções óbvias (ler documentação oficial)
- Erros já cobertos em ARCHITECTURE.md ou CONVENTIONS.md

### Como escrever

**BOM:**
```yaml
- problema: "Migration falha com erro de FK constraint"
  contexto: "Criação de tabela com relacionamento 1:N"
  sintoma: "DbUpdateException ao executar dotnet ef database update"
  causa_raiz: "FK aponta para tabela que ainda não existe (ordem errada)"
  solucao: |
    1. Reordenar migrations (CreateTable da tabela pai ANTES da tabela filha)
    2. Ou remover migration e recriar com ordem correta
```

**RUIM:**
```yaml
- problema: "Erro no banco"
  solucao: "Arrumar migration"
```

---

## Integração com Contratos

Estes arquivos **complementam** os contratos de execução:

| Contrato | Base de Conhecimento | Relação |
|----------|---------------------|---------|
| `backend-criacao.md` | `backend.yaml` | Consultar padrões obrigatórios antes de criar |
| `backend-adequacao.md` | `backend.yaml` | Consultar erros comuns antes de adequar |
| `manutencao-controlada.md` | `backend.yaml` ou `frontend.yaml` | Consultar problemas conhecidos antes de corrigir |
| `frontend-criacao.md` | `frontend.yaml` | Consultar layout padrão e boas práticas |
| `frontend-adequacao.md` | `frontend.yaml` | Consultar erros comuns de Angular/PrimeNG |

---

## Comandos Úteis

### Buscar por tag

```bash
# Backend - buscar por tag "multi-tenancy"
grep -B 5 "multi-tenancy" docs/base-conhecimento/backend.yaml

# Frontend - buscar por tag "routing"
grep -B 5 "routing" docs/base-conhecimento/frontend.yaml
```

### Listar todos os problemas

```bash
# Backend
grep "problema:" docs/base-conhecimento/backend.yaml

# Frontend
grep "problema:" docs/base-conhecimento/frontend.yaml
```

### Verificar erros comuns

```bash
# Backend
sed -n '/erros_comuns:/,/^$/p' docs/base-conhecimento/backend.yaml

# Frontend
sed -n '/erros_comuns:/,/^$/p' docs/base-conhecimento/frontend.yaml
```

---

## Manutenção

### Periodicidade

- **Semanal**: Revisar se há problemas recorrentes não documentados
- **Mensal**: Consolidar problemas similares
- **Trimestral**: Remover problemas obsoletos (tecnologia mudou)

### Critério de Remoção

Remover problema se:
- Tecnologia foi atualizada e problema não existe mais
- Problema foi corrigido na arquitetura (não pode mais ocorrer)
- Solução foi incorporada em ARCHITECTURE.md ou CONVENTIONS.md

---

## Changelog

| Data | Mudança |
|------|---------|
| 2026-01-04 | Criação inicial dos arquivos backend.yaml e frontend.yaml |

---

**Mantido por:** Time de Desenvolvimento IControlIT
**Última Atualização:** 2026-01-04
