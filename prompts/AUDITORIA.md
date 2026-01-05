# PROMPT DE AUDITORIA DE CONFORMIDADE

Este prompt ativa o **CONTRATO-AUDITORIA-CONFORMIDADE.md** para validar se a implementação está conforme a especificação técnica.

---

## PROMPT BÁSICO

### Auditoria Completa (Backend + Frontend)

```
Auditar o RF-XXX (backend e frontend) conforme CONTRATO DE AUDITORIA.

Camada: COMPLETO
RF: RF-XXX
Objetivo: Identificar todas as divergências entre especificação (RF, UC, MD, WF) e código implementado.
```

---

### Auditoria Backend

```
Auditar o backend do RF-XXX conforme CONTRATO DE AUDITORIA.

Camada: BACKEND
RF: RF-XXX
Verificar: Entidades, Commands, Queries, Validators, DTOs, Handlers, Endpoints, Seeds, Configurations
Objetivo: Identificar gaps críticos que bloqueiam implementação do frontend.
```

---

### Auditoria Frontend

```
Auditar o frontend do RF-XXX conforme CONTRATO DE AUDITORIA.

Camada: FRONTEND
RF: RF-XXX
Verificar: Componentes, Formulários, Services, Rotas, Traduções, Models
Objetivo: Identificar divergências entre wireframes/UCs e implementação Angular.
```

---

## PROMPT AVANÇADO

### Auditoria com Foco Específico

```
Auditar o RF-XXX conforme CONTRATO DE AUDITORIA.

Camada: BACKEND
RF: RF-XXX
Foco prioritário:
- Validar se todos os campos do MD-RF-XXX.md estão implementados
- Verificar se regras RN-XXX-YYY estão aplicadas nos Validators
- Confirmar se seeds de entidades lookup estão presentes
- Validar integração com Central de Funcionalidades

Gerar relatório em: D:\IC2\relatorios\AAAA-MM-DD-RFXXX-BACKEND-Gaps.md
```

---

### Auditoria Pré-Conclusão de RF

```
Auditar o RF-XXX (backend e frontend) conforme CONTRATO DE AUDITORIA antes de marcar como concluído.

Camada: COMPLETO
RF: RF-XXX
Objetivo: Validar conformidade total antes de merge em dev.
Atenção especial a:
- Campos obrigatórios do UC implementados
- Validações críticas (RN-XXX) aplicadas
- Traduções i18n completas (pt, en, es)
- Seeds funcionais presentes
- Endpoints protegidos com Policy correta

Classificar gaps por severidade e indicar se RF pode ser marcado como concluído.
```

---

### Re-auditoria Pós-Correção

```
Re-auditar o RF-XXX conforme CONTRATO DE AUDITORIA após correções aplicadas.

Camada: BACKEND
RF: RF-XXX
Relatório anterior: D:\IC2\relatorios\AAAA-MM-DD-RFXXX-BACKEND-Gaps.md
Objetivo: Confirmar que todos os gaps críticos e importantes foram corrigidos.

Comparar com relatório anterior e validar se:
- GAP 1 (Entidade EnderecoEntregaTipo) foi corrigido ✅
- GAP 2 (Campos de Contato) foi corrigido ✅
- GAP 3 (FlPadrao) foi corrigido ✅
[... listar todos os gaps do relatório anterior]

Gerar novo relatório confirmando conformidade total.
```

---

## PROMPT SIMPLIFICADO (MÍNIMO)

### Uso Rápido

```
Auditar RF-XXX conforme CONTRATO DE AUDITORIA
```

**O agente irá:**
1. Detectar automaticamente se backend/frontend estão implementados
2. Ler documentação (RF, UC, MD, WF)
3. Comparar com código
4. Gerar relatório em `D:\IC2\relatorios\`

---

## VARIAÇÕES DE USO

### Auditoria Durante Code Review

```
Fazer code review do RF-XXX conforme CONTRATO DE AUDITORIA.

Verificar:
- Conformidade com especificação
- Conformidade com ARCHITECTURE.md
- Conformidade com CONVENTIONS.md
- Ausência de over-engineering
- Ausência de escopo não especificado

Gerar relatório de gaps e sugestões de melhoria.
```

---

### Auditoria de Integrações Obrigatórias

```
Auditar integrações obrigatórias do RF-XXX conforme CONTRATO DE AUDITORIA.

Focar exclusivamente em:
- Central de Funcionalidades (registro + permissões)
- i18n (pt, en, es completos)
- Auditoria (campos CreatedBy, UpdatedBy, etc.)
- Multi-Tenancy (ClienteId, EmpresaId)
- Permissões RBAC (Policy vs Role)

Classificar divergências por severidade.
```

---

### Auditoria de Dependências Funcionais

```
Auditar dependências funcionais do RF-XXX conforme CONTRATO DE AUDITORIA.

Camada: BACKEND
RF: RF-XXX
Objetivo: Identificar FKs e entidades dependentes faltantes.

Analisar MD-RF-XXX.md e validar:
- Todas as FKs especificadas estão implementadas
- Navigation Properties configuradas
- Seeds de entidades pai existem
- Endpoints de lookup estão disponíveis

Listar dependências bloqueantes para testes E2E.
```

---

## EXEMPLOS REAIS

### Exemplo 1: RF-043 (Endereços de Entrega)

**Prompt usado:**
```
Auditar backend do RF-043 conforme CONTRATO DE AUDITORIA.
```

**Resultado:**
- 7 gaps identificados (5 críticos, 2 importantes)
- Relatório: `D:\IC2\relatorios\2025-12-25-RF043-BACKEND-Gaps.md`
- Status: ❌ NÃO CONFORME
- Ação: Executar correções sob CONTRATO-EXECUCAO-BACKEND

---

### Exemplo 2: RF-015 (Frontend)

**Prompt usado:**
```
Verificar conformidade do frontend RF-015 conforme CONTRATO DE AUDITORIA.
```

**Resultado:**
- 3 gaps importantes (validações, traduções)
- 0 gaps críticos
- Relatório: `D:\IC2\relatorios\2025-12-25-RF015-FRONTEND-Gaps.md`
- Status: ⚠️ CONFORME COM RESSALVAS
- Ação: RF pode ser concluído, correções incrementais

---

## PARÂMETROS OPCIONAIS

### Nível de Detalhe

```
Auditar RF-XXX conforme CONTRATO DE AUDITORIA.

Nível de detalhe: ALTO
- Incluir referências exatas (arquivo:linha) para cada gap
- Citar trechos de código e especificação
- Estimar esforço de correção
- Sugerir ordem de correção
```

---

### Foco em Severidade Específica

```
Auditar RF-XXX conforme CONTRATO DE AUDITORIA.

Focar exclusivamente em gaps CRÍTICOS que bloqueiam RF.
Ignorar gaps importantes e menores nesta análise.
```

---

## SAÍDA ESPERADA

Após executar o prompt, o agente irá:

1. ✅ Criar todo list de auditoria
2. ✅ Ler documentação (RF, UC, MD, WF)
3. ✅ Ler código (backend e/ou frontend)
4. ✅ Identificar e classificar gaps
5. ✅ Gerar relatório em `D:\IC2\relatorios\AAAA-MM-DD-RFXXX-CAMADA-Gaps.md`
6. ✅ Declarar status: CONFORME / NÃO CONFORME / CONFORME COM RESSALVAS
7. ✅ Sugerir próximos passos

**O agente NÃO irá:**
- ❌ Alterar código
- ❌ Corrigir bugs
- ❌ Implementar funcionalidades faltantes
- ❌ Criar commits

---

## QUANDO USAR ESTE PROMPT

| Situação | Quando Usar |
|----------|-------------|
| **Antes de marcar RF como concluído** | ✅ Sempre |
| **Após implementação de backend** | ✅ Antes de iniciar frontend |
| **Após implementação de frontend** | ✅ Antes de executar testes E2E |
| **Durante code review** | ✅ Para validar conformidade |
| **Em caso de bugs recorrentes** | ✅ Para identificar gaps de validação |
| **Antes de fazer merge em dev** | ✅ Para garantir qualidade |

---

## INTEGRAÇÃO COM OUTROS CONTRATOS

Após auditoria, dependendo do resultado:

### Se GAPS CRÍTICOS identificados:

```
Corrigir gaps críticos do RF-XXX conforme CONTRATO DE MANUTENÇÃO.

Referência: D:\IC2\relatorios\AAAA-MM-DD-RFXXX-BACKEND-Gaps.md
Gaps a corrigir:
- GAP 1: [descrição]
- GAP 2: [descrição]
[...]
```

ou

```
Implementar funcionalidades faltantes do RF-XXX conforme CONTRATO DE EXECUÇÃO - BACKEND.

Referência: D:\IC2\relatorios\AAAA-MM-DD-RFXXX-BACKEND-Gaps.md
Escopo: Implementar apenas os gaps críticos identificados no relatório.
```

---

### Após correções, re-auditar:

```
Re-auditar RF-XXX conforme CONTRATO DE AUDITORIA após correções.

Relatório anterior: D:\IC2\relatorios\AAAA-MM-DD-RFXXX-BACKEND-Gaps.md
Objetivo: Confirmar conformidade total.
```

---

## CHECKLISTS RELACIONADOS

Para auditoria manual, consultar:

- **Markdown:** `D:\IC2\docs\checklists\auditoria-conformidade.md`
- **YAML:** `D:\IC2\docs\checklists\auditoria-conformidade.yaml`

---

## CONTRATO RELACIONADO

- **Contrato:** `D:\IC2\docs\contracts\CONTRATO-AUDITORIA-CONFORMIDADE.md`
- **Governança:** `D:\IC2\CLAUDE.md` (seção: Contrato de Auditoria de Conformidade)

---

**Última atualização:** 2025-12-25
**Versão:** 1.0.0
