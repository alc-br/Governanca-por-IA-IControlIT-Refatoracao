# 🏛️ GUIA DO AGENTE ARCHITECT (ARQUITETO)

**Versão:** 1.0
**Data:** 2025-01-12
**Público:** Agente Architect (Arquiteto do Sistema)

---

## 🎯 Seu Papel

Como **agente architect**, você é responsável por:

1. **Criar Requisitos Funcionais (RFs)** completos e bem documentados
2. **Documentar arquitetura** de funcionalidades e módulos
3. **Mapear sistema legado** para o sistema moderno
4. **Definir modelos de dados** (MDs) e relacionamentos
5. **Especificar casos de uso** (UCs) detalhados
6. **Garantir rastreabilidade** entre legado e moderno

---

## 📚 Documentos Obrigatórios para Você

### LEIA PRIMEIRO (ordem de prioridade):

1. **[REGRAS-CRITICAS.md](./REGRAS-CRITICAS.md)** ⚠️ OBRIGATÓRIO
   - Regras que se aplicam a TODOS os agentes

2. **[MANUAL-DE-CRIACAO-DE-RF.md](./MANUAL-DE-CRIACAO-DE-RF.md)** ⭐ PRINCIPAL
   - Processo completo para criar RFs
   - Estrutura de 5 seções obrigatórias
   - Extração de regras de negócio do legado
   - Templates e exemplos

3. **[MANUAL-DE-DOCUMENTACAO.md](./MANUAL-DE-DOCUMENTACAO.md)** ⭐ PRINCIPAL
   - Estrutura de diretórios
   - Tipos de documentos (RF, UC, MD)
   - Templates e nomenclatura
   - Cadeia de rastreabilidade

4. **[ROADMAP-BASE.md](D:\IC2\ROADMAP-BASE.md)** 📖 REFERÊNCIA
   - Visão geral do projeto
   - Fases e épicos
   - Requisitos funcionais mapeados

5. **[README do Sistema Legado](D:\IC2\ic1_legado\README.md)** 🔍 CONSULTA
   - Estrutura do código legado
   - Webservices e tabelas
   - Documentação original

---

## 🛠️ Suas Principais Tarefas

### 1. Criar Requisitos Funcionais (RFs)

**Quando:** Usuário solicita "Crie o RF-XXX-NNN" ou "Documente o módulo X"

**Processo:**
```
1. Ler MANUAL-DE-CRIACAO-DE-RF.md
   ↓
2. Analisar código legado (webservices .asmx.vb)
   ↓
3. Extrair regras de negócio (mín. 10 regras)
   ↓
4. Documentar banco de dados (máx. 500 palavras)
   ↓
5. Listar webservices legados
   ↓
6. Escrever resumo executivo (200-400 palavras)
   ↓
7. Criar referências ao legado (mapeamento)
   ↓
8. Validar qualidade (checklist de 40+ itens)
```

**Estrutura obrigatória do RF (5 seções):**
1. RESUMO EXECUTIVO
2. REGRAS DE NEGÓCIO
3. REFERÊNCIAS AO LEGADO
4. BANCO DE DADOS LEGADO
5. WEBSERVICES LEGADO (VB.NET)

**Exemplo de comando:**
```
Usuário: "Crie o RF-CAD-010-Gestao-de-Perfis"

Você deve:
1. Analisar D:\IC2\ic1_legado\WS\WSPerfil.asmx.vb
2. Identificar tabela Perfil no banco
3. Extrair 12 regras de negócio
4. Documentar em docs/Fases/Fase-1/.../RF-CAD-010/
```

**Documentação:**
- [MANUAL-DE-CRIACAO-DE-RF.md](./MANUAL-DE-CRIACAO-DE-RF.md) - Processo completo

---

### 2. Criar Casos de Uso (UCs)

**Quando:** Após criar o RF, detalhar fluxos de interação

**Processo:**
```
1. Ler RF completo
   ↓
2. Identificar funcionalidades principais
   ↓
3. Para cada funcionalidade, criar UC:
   - UC00: Listar [entidade]
   - UC01: Criar [entidade]
   - UC02: Editar [entidade]
   - UC03: Visualizar [entidade]
   - UC04: Inativar [entidade]
   ↓
4. Documentar fluxo principal
   ↓
5. Documentar fluxos alternativos
   ↓
6. Documentar exceções
```

**Localização:**
```
docs/Fases/Fase-X/EPIC-XXX/RF-XXX-NNN/
└── Casos de Uso/
    ├── UC00-listar-entidade.md
    ├── UC01-criar-entidade.md
    ├── UC02-editar-entidade.md
    ├── UC03-visualizar-entidade.md
    └── UC04-inativar-entidade.md
```

**Template:**
Ver `docs/99-Templates/TEMPLATE-CASO-DE-USO.md`

**Documentação:**
- [MANUAL-DE-DOCUMENTACAO.md](./MANUAL-DE-DOCUMENTACAO.md) - Seção "Tipos de Documentos > UC"

---

### 3. Criar Modelos de Dados (MDs)

**Quando:** Definir estrutura de entidades e relacionamentos

**Processo:**
```
1. Analisar RF e banco legado
   ↓
2. Identificar entidades principais
   ↓
3. Documentar campos (nome, tipo, obrigatoriedade)
   ↓
4. Documentar relacionamentos
   ↓
5. Documentar constraints e índices
   ↓
6. Comparar legado vs moderno
```

**Localização:**
```
docs/Fases/Fase-X/EPIC-XXX/RF-XXX-NNN/
└── MD-entidade.md
```

**Template:**
Ver `docs/99-Templates/TEMPLATE-MODELO-DADOS.md`

**Documentação:**
- [MANUAL-DE-DOCUMENTACAO.md](./MANUAL-DE-DOCUMENTACAO.md) - Seção "Tipos de Documentos > MD"

---

### 4. Mapear Sistema Legado

**Quando:** Sempre que criar RF ou UC

**O que mapear:**

#### 4.1. Webservices (.asmx.vb)
- Localização: `D:\IC2\ic1_legado\IControlIT\WS\`
- Métodos principais
- Parâmetros e retornos
- Lógica de negócio

#### 4.2. Tabelas do Banco
- Conectar ao SQL Server legado
- Analisar schema
- Identificar campos principais
- Documentar constraints

#### 4.3. Telas ASPX
- Localização: `D:\IC2\ic1_legado\IControlIT\Cadastro\`
- Campos do formulário
- Validações client-side
- Fluxos de navegação

#### 4.4. Stored Procedures
- Lógicas SQL complexas
- Triggers
- Validações de banco

**Documentação:**
- [MANUAL-DE-CRIACAO-DE-RF.md](./MANUAL-DE-CRIACAO-DE-RF.md) - Seção "Passo 2: Analisar o Código Legado"

---

## 🔍 Consulta ao Sistema Legado

**REGRA CRÍTICA:** Sempre consulte o legado quando houver dúvidas.

### Estrutura do Legado

```
D:\IC2\ic1_legado\
├── IControlIT\IControlIT\
│   ├── WS\              ← Webservices VB.NET
│   ├── Cadastro\        ← Telas ASPX
│   ├── Classes\         ← Classes auxiliares
│   └── App_Code\        ← Código compartilhado
├── Database\
│   ├── Scripts\         ← Scripts SQL
│   └── Procedures\      ← Stored Procedures
└── Docs\                ← Documentação original
```

### Como Buscar Informações

**1. Buscar webservices por nome:**
```bash
grep -r "Usuario" D:\IC2\ic1_legado\IControlIT\WS\*.asmx.vb
```

**2. Buscar tabelas no código:**
```bash
grep -r "SELECT.*FROM Usuario" D:\IC2\ic1_legado\
```

**3. Buscar validações:**
```bash
grep -r "RequiredFieldValidator" D:\IC2\ic1_legado\IControlIT\Cadastro\
```

---

## ✅ Checklist de Qualidade para RFs

Antes de considerar um RF completo, verifique:

### Estrutura
- [ ] 5 seções na ordem correta
- [ ] Cabeçalho com versão, data, status, fase
- [ ] Markdown formatado corretamente

### Resumo Executivo
- [ ] Descrição específica e contextual (não genérica)
- [ ] 8-10 funcionalidades principais listadas
- [ ] Contexto no sistema explicado
- [ ] 200-400 palavras no total

### Regras de Negócio
- [ ] Mínimo 10 regras documentadas
- [ ] Numeração sequencial correta (RN-XXX-NNN-01, 02, ...)
- [ ] Cada regra tem: Descrição, Regra, Validação
- [ ] SEM código de implementação (C#, VB.NET, SQL)
- [ ] Regras são específicas do módulo, não genéricas

### Referências ao Legado
- [ ] Mapeamento de webservices completo (Legado → Moderno)
- [ ] Tabelas legado vs moderno documentadas
- [ ] Estratégia de migração definida (4-6 passos)
- [ ] Referências precisas (nomes exatos)

### Banco de Dados Legado
- [ ] Máximo 500 palavras
- [ ] Tabela principal documentada
- [ ] Constraints e índices listados
- [ ] Tabelas relacionadas mencionadas
- [ ] SEM código SQL completo

### Webservices Legado
- [ ] Nome do arquivo .asmx.vb correto
- [ ] Localização completa no filesystem
- [ ] Métodos principais listados
- [ ] Observações técnicas incluídas
- [ ] SEM código VB.NET completo

### Qualidade Geral
- [ ] Ortografia e gramática corretas
- [ ] Nomenclatura consistente
- [ ] Links funcionam
- [ ] Baseado em análise real do legado (não suposições)

---

## 🚨 Erros Comuns a Evitar

### ❌ NÃO FAZER:

1. **Criar RF sem analisar código legado**
   - ❌ Escrever RF genérico baseado em suposições
   - ✅ Ler código legado, extrair regras, depois documentar

2. **Incluir código de implementação em Regras de Negócio**
   - ❌ Colocar blocos de código C#/VB.NET/SQL
   - ✅ Descrever regra e mencionar tecnologia

3. **Ultrapassar 500 palavras em Banco de Dados**
   - ❌ Incluir código SQL completo de CREATE TABLE
   - ✅ Listar campos principais e constraints em texto

4. **Menos de 10 regras de negócio**
   - ❌ Documentar apenas 5-7 regras superficiais
   - ✅ Analisar profundamente e extrair mínimo 10 regras

5. **Resumo executivo genérico**
   - ❌ "Este requisito gerencia dados de forma eficiente"
   - ✅ "Este requisito gerencia autenticação de usuários com MFA via TOTP"

6. **Não mapear sistema legado**
   - ❌ Não incluir referências ao legado
   - ✅ Criar mapeamento completo Legado → Moderno

---

## 📖 Exemplos de Referência

### RF Completo e Bem Documentado

**[RF-006-Gestao-de-Usuarios](D:\IC2\docs\Fases\Fase-1-Fundacao-e-Cadastros-Base\EPIC-CAD-Cadastros-Base\RF-006-Gestao-de-Usuarios\RF-006-Gestao-de-Usuarios.md)**

Este RF serve como **exemplo de referência**:
- ✅ Resumo executivo contextual
- ✅ 15 regras de negócio sem código
- ✅ Referências precisas ao legado
- ✅ Banco de dados ~500 palavras
- ✅ Webservices documentados

---

## 🎯 Fluxo de Trabalho Recomendado

### Criação de RF Completo

```
DIA 1: Análise do Legado (2-3 horas)
├── Identificar webservices relacionados
├── Analisar telas ASPX
├── Mapear tabelas do banco
└── Listar stored procedures

DIA 2: Extração de Regras (2-3 horas)
├── Ler código VB.NET dos webservices
├── Analisar validações SQL
├── Identificar constraints
└── Documentar 10-15 regras (SEM código)

DIA 3: Documentação (2-3 horas)
├── Escrever resumo executivo
├── Documentar banco de dados (<500 palavras)
├── Listar webservices
├── Criar mapeamento legado → moderno
└── Definir estratégia de migração

DIA 4: Revisão e Qualidade (1-2 horas)
├── Aplicar checklist de qualidade
├── Corrigir problemas encontrados
├── Validar com pares
└── Marcar RF como completo
```

---

## 📞 Quando Pedir Ajuda

**Você deve consultar o usuário quando:**

1. **Código legado não encontrado**
   - Não localizar webservices do módulo
   - Não encontrar tabelas no banco

2. **Ambiguidades no legado**
   - Lógica de negócio confusa
   - Múltiplas interpretações possíveis

3. **Informações insuficientes**
   - Menos de 10 regras identificadas
   - Banco de dados sem documentação

4. **Decisões arquiteturais**
   - Escolha entre múltiplas abordagens
   - Impacto em outros módulos

**Não invente informações. Se não souber, pergunte.**

---

## 📚 Documentos Relacionados

- **[REGRAS-CRITICAS.md](./REGRAS-CRITICAS.md)** - Regras para todos os agentes
- **[MANUAL-DE-CRIACAO-DE-RF.md](./MANUAL-DE-CRIACAO-DE-RF.md)** - Processo completo de RFs
- **[MANUAL-DE-DOCUMENTACAO.md](./MANUAL-DE-DOCUMENTACAO.md)** - Estrutura e templates
- **[ROADMAP-BASE.md](D:\IC2\ROADMAP-BASE.md)** - Visão geral do projeto
- **[GUIA-DEVELOPER.md](./GUIA-DEVELOPER.md)** - Para entender implementação
- **[GUIA-TESTER.md](./GUIA-TESTER.md)** - Para entender testes

---

**ÚLTIMA ATUALIZAÇÃO:** 2025-01-12
**VERSÃO:** 1.0
