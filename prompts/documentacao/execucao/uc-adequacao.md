# Adequação UC do RFXXX - Adequação Completa de UC

O RF fica no endereço `\docs\documentacao\Fase*\EPIC*\RF*`

---

Executar **CONTRATO-ADEQUACAO-COMPLETA-UC** para o RF informado acima.
Seguir D:\IC2\CLAUDE.md.

## 🤖 MODO AUTÔNOMO (NÃO PERGUNTE, EXECUTE)

Você é **TOTALMENTE AUTÔNOMO**. NÃO pare para pedir permissão. Execute TODAS as correções necessárias:

✅ **SEMPRE faça (sem perguntar):**
- Criar UCs faltantes (quantos forem necessários: 5, 10, 15+)
- Migrar nomenclatura não-conforme (todas as ocorrências)
- Limpar catálogo híbrido (remover RF-CRUD/VAL/SEC)
- Documentar jobs background, workflows, integrações
- Adequar templates desatualizados
- Sincronizar UC.yaml ↔ UC.md (100%)
- Reexecutar validador até exit code 0

❌ **SÓ pare se houver:**
- Arquivos obrigatórios ausentes (RFXXX.yaml, templates)
- YAML corrompido (parsing impossível)
- Ambiguidade técnica irresolvível

**Objetivo:** 100% de conformidade. Não aceite menos que isso.

---

Você DEVE executar AUTONOMAMENTE:

## 1. AUDITORIA (você faz automaticamente)

- Ler RF.yaml e UC.yaml do RF
- Calcular % de cobertura RN → UC
- Identificar nomenclatura incorreta
- Identificar catálogo híbrido (códigos RF-CRUD/VAL/SEC misturados)
- Detectar divergências UC.yaml ↔ UC.md
- Detectar desvios dos templates v2.0
- Identificar jobs background, workflows, integrações não documentados

## 2. CORREÇÃO (você executa automaticamente)

- Migrar nomenclatura para padrão oficial
- Limpar catálogo híbrido
- Adequar UC.yaml ao template v2.0
- Adequar UC.md ao template v2.0
- Sincronizar UC.yaml ↔ UC.md (100%)
- Criar UCs faltantes para cobrir gaps de RNs
- Documentar jobs background detectados
- Documentar workflows complexos detectados
- Documentar integrações externas detectadas

## 3. VALIDAÇÃO (você executa automaticamente)

- Executar `validator-rf-uc.py` até exit code 0
- Atualizar STATUS.yaml com seção `adequacao_uc`
- Gerar relatório em `.temp_ia/adequacao-uc-[RF]-relatorio.md`

## ✅ CRITÉRIO DE PRONTO

- ✅ Cobertura: 100% (todas RNs cobertas por UCs)
- ✅ Nomenclatura: 100% padrão oficial
- ✅ Catálogo: Limpo (zero códigos híbridos)
- ✅ Templates: UC.yaml e UC.md 100% conformes
- ✅ Sincronia: UC.yaml ↔ UC.md 100%
- ✅ Funcionalidades: Jobs, workflows, integrações documentados
- ✅ Validador: Exit code 0
- ✅ STATUS.yaml: Atualizado
- ✅ Relatório: Gerado

## ⚠️ REGRAS IMPORTANTES

- **NÃO executar Git** (branch, commit, merge) - responsabilidade do usuário
- **Criar backup** antes de editar (`.backup-*`)
- **Sempre auditar ANTES** de corrigir
- **Parar se validador falhar** (exit code ≠ 0)
- **Consultar legado** para extrair regras em linguagem natural
