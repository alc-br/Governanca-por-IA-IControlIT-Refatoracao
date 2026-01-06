# Aditivo RFXXX - Adicionar Nova Funcionalidade

Ele fica nesse endereço D:\IC2\rf\Fase*\EPIC*\RF*

**Instruções:** Altere RFXXX acima para o RF desejado (ex: RF001, RF025, RF028).

---

Executar **ADITIVO** para o RF informado acima conforme D:/IC2_Governanca/contracts/documentacao/execucao/aditivo.md.
Seguir D:\IC2\CLAUDE.md.

## 📋 FUNCIONALIDADE A ADICIONAR

[Descreva aqui a nova funcionalidade que deseja adicionar ao RF]

Exemplo:
```
Adicionar funcionalidade de "Exportação em PDF" para permitir que usuários
exportem a lista de clientes em formato PDF com logo da empresa e filtros aplicados.
```

---

## 🔄 WORKFLOW DE EXECUÇÃO

### FASE 1: BACKUP AUTOMÁTICO (6 passos)

1. Criar RFXXX_old.md e RFXXX_old.yaml (backup do RF)
2. Criar UC-RFXXX_old.md e UC-RFXXX_old.yaml (backup dos UCs)
3. Criar WF-RFXXX_old.md e WF-RFXXX_old.yaml (backup dos WFs)
4. Criar MD-RFXXX_old.md e MD-RFXXX_old.yaml (backup do MD)
5. Criar MT-RFXXX_old.yaml (backup das massas de teste)
6. Criar TC-RFXXX_old.yaml (backup dos casos de teste)

**Checkpoint:** ✅ Todos os 10 arquivos `_old` criados

---

### FASE 2: EVOLUÇÃO INCREMENTAL (4 passos)

#### Passo 7: Adicionar ao RF

**Ações:**
- Ler RFXXX.md e RFXXX.yaml (versões originais)
- Adicionar nova funcionalidade ao catálogo (Seção 4)
- Adicionar mínimo 3 RNs para nova funcionalidade (Seção 5)
- Adicionar permissões necessárias (Seção 7)
- Adicionar endpoints da API (Seção 8) - se aplicável
- Documentar mudanças no modelo de dados (Seção 9) - se aplicável
- Atualizar integrações obrigatórias (Seção 11) - chaves i18n, auditoria, etc.
- Sincronizar RFXXX.md ↔ RFXXX.yaml

**Checkpoint:** ✅ RF atualizado com nova funcionalidade (mínimo 3 RNs)

#### Passo 8: Adicionar ao UC

**Ações:**
- Comparar RFXXX.md vs RFXXX_old.md (identificar delta)
- Ler UC-RFXXX.md e UC-RFXXX.yaml (versões originais)
- Criar novos UCs cobrindo 100% da nova funcionalidade
- Garantir que TODAS as novas RNs estejam cobertas
- Sincronizar UC-RFXXX.md ↔ UC-RFXXX.yaml
- Validar: `python tools/docs/validator-rf-uc.py RFXXX` (exit code 0)

**Checkpoint:** ✅ UCs criados cobrindo 100% do delta RF

#### Passo 9: Adicionar ao WF

**Ações:**
- Comparar UC-RFXXX.yaml vs UC-RFXXX_old.yaml (identificar novos UCs)
- Ler WF-RFXXX.md e WF-RFXXX.yaml (versões originais)
- Criar novos WFs cobrindo 100% dos novos UCs
- Documentar telas, componentes, eventos, estados (Loading, Vazio, Erro, Dados)
- Documentar responsividade (Mobile, Tablet, Desktop)
- Documentar acessibilidade WCAG AA
- Sincronizar WF-RFXXX.md ↔ WF-RFXXX.yaml

**Checkpoint:** ✅ WFs criados cobrindo 100% dos novos UCs

#### Passo 10: Adicionar ao MD

**Ações:**
- Comparar RFXXX.md vs RFXXX_old.md (identificar mudanças no modelo)
- Ler MD-RFXXX.md e MD-RFXXX.yaml (versões originais)
- Adicionar novas tabelas (se necessário)
- Adicionar novos campos a tabelas existentes (se necessário)
- Garantir multi-tenancy (cliente_id ou empresa_id)
- Garantir auditoria (5 campos obrigatórios)
- Garantir soft delete (deleted_at)
- Sincronizar MD-RFXXX.md ↔ MD-RFXXX.yaml

**Checkpoint:** ✅ MD atualizado com suporte à nova funcionalidade

---

### FASE 3: TESTES (2 passos)

#### Passo 11: Adicionar ao MT

**Ações:**
- Comparar UC-RFXXX.yaml vs UC-RFXXX_old.yaml (identificar novos UCs)
- Ler MT-RFXXX.yaml (versão original)
- Criar massas de teste para cada novo UC
- Garantir cenários: caminho feliz, triste, edge cases
- Formato CSV conforme template

**Checkpoint:** ✅ Massas de teste criadas para novos UCs

#### Passo 12: Adicionar ao TC

**Ações:**
- Comparar UC-RFXXX.yaml vs UC-RFXXX_old.yaml (identificar novos UCs)
- Ler TC-RFXXX.yaml (versão original)
- Criar casos de teste para cada novo UC
- Cobrir: Backend, Frontend, Segurança, Integração
- Garantir mínimo 30-50 TCs por novo UC

**Checkpoint:** ✅ Casos de teste criados para novos UCs

---

### FASE 4: RELATÓRIO (1 passo)

#### Passo 13: Gerar Relatório de Delta

**Ações:**
- Criar `.temp_ia/aditivo-RFXXX-delta-report.md`
- Documentar EXATAMENTE o que foi adicionado em cada nível:
  - RF: quantas RNs, endpoints, permissões
  - UC: quantos UCs novos
  - WF: quantos WFs novos
  - MD: quantas tabelas, campos
  - MT: quantas massas de teste
  - TC: quantos casos de teste
- Listar validações executadas (12/12 PASS)
- Declarar veredicto final: ✅ APROVADO ou ❌ REPROVADO

**Checkpoint:** ✅ Relatório de delta completo

---

## ✅ CRITÉRIOS DE APROVAÇÃO

**APROVADO (100%):**
- ✅ 12/12 validações PASS
- ✅ Todas as versões `_old` criadas (10 arquivos)
- ✅ Cobertura total (RF → UC → WF → MD → MT → TC)
- ✅ Zero gaps identificados
- ✅ Relatório de delta completo

**REPROVADO (<100%):**
- ❌ Qualquer validação FAIL
- ❌ Qualquer gap de cobertura
- ❌ Inconsistências entre .md e .yaml
- ❌ Relatório de delta incompleto

**⚠️ NÃO EXISTE "APROVADO COM RESSALVAS"**

---

## 📊 VALIDAÇÕES OBRIGATÓRIAS

| # | Validação | Critério |
|---|-----------|----------|
| 1 | Backups `_old` criados | 10/10 arquivos |
| 2 | RF atualizado (mín. 3 RNs) | ≥3 RNs novas |
| 3 | RF.md ↔ RF.yaml sincronizado | 100% |
| 4 | UC cobre 100% delta RF | validator-rf-uc.py: exit code 0 |
| 5 | UC.md ↔ UC.yaml sincronizado | 100% |
| 6 | WF cobre 100% novos UCs | Todos cobertos |
| 7 | WF.md ↔ WF.yaml sincronizado | 100% |
| 8 | MD atualizado | Tabelas/campos adicionados |
| 9 | MD.md ↔ MD.yaml sincronizado | 100% |
| 10 | MT cobre novos UCs | Massas criadas |
| 11 | TC cobre novos UCs | ≥30 TCs por UC |
| 12 | Relatório de delta gerado | Arquivo existe |

---

## 🚨 REGRAS IMPORTANTES

- **SEMPRE** criar backups `_old` ANTES de modificar originais
- **SEMPRE** sobrescrever versões `_old` (não acumular)
- **SEMPRE** propagar mudanças em cascata (RF → UC → WF → MD → MT → TC)
- **SEMPRE** validar cobertura 100% em cada nível
- **NUNCA** aprovar com ressalvas (0% ou 100%)
- **SEMPRE** gerar relatório de delta
- **SEMPRE** manter sincronização .md ↔ .yaml

---

## 📂 ARQUIVOS QUE SERÃO MODIFICADOS

**Backups criados (_old):**
- RFXXX_old.md
- RFXXX_old.yaml
- UC-RFXXX_old.md
- UC-RFXXX_old.yaml
- WF-RFXXX_old.md
- WF-RFXXX_old.yaml
- MD-RFXXX_old.md
- MD-RFXXX_old.yaml
- MT-RFXXX_old.yaml
- TC-RFXXX_old.yaml

**Documentos atualizados:**
- RFXXX.md (adições)
- RFXXX.yaml (adições)
- UC-RFXXX.md (novos UCs)
- UC-RFXXX.yaml (novos UCs)
- WF-RFXXX.md (novos WFs)
- WF-RFXXX.yaml (novos WFs)
- MD-RFXXX.md (novas tabelas/campos)
- MD-RFXXX.yaml (novas tabelas/campos)
- MT-RFXXX.yaml (novas massas)
- TC-RFXXX.yaml (novos TCs)

**Relatório:**
- `.temp_ia/aditivo-RFXXX-delta-report.md`

---

## 🔄 PRÓXIMOS PASSOS

**Após aprovação deste prompt:**
1. Executar validação: `prompts/documentacao/validacao/aditivo.md`
2. Se aprovado: Commit e merge
3. Executar backend-aditivo: `D:/IC2_Governanca/contracts/desenvolvimento/execucao/backend-aditivo.md`
4. Executar frontend-aditivo: `D:/IC2_Governanca/contracts/desenvolvimento/execucao/frontend-aditivo.md`

---

## 💡 EXEMPLO PRÁTICO

```markdown
# Aditivo RF028 - Adicionar Nova Funcionalidade

## FUNCIONALIDADE A ADICIONAR

Adicionar funcionalidade de "Exportação em PDF" para permitir que usuários
exportem a lista de clientes em formato PDF com logo da empresa e filtros aplicados.

---

Conforme D:/IC2_Governanca/contracts/documentacao/execucao/aditivo.md para RF028.
Seguir D:\IC2\CLAUDE.md.
```

**Resultado esperado:**
- ✅ RF028 atualizado com RN-CLI-028-15, RN-CLI-028-16, RN-CLI-028-17
- ✅ RF028 com endpoint GET /api/v1/clientes/export/pdf
- ✅ UC-RF028 com UC-12: Exportar Lista de Clientes em PDF
- ✅ WF-RF028 com WF-12: Tela de Exportação PDF
- ✅ MD-RF028 sem mudanças (não requer novas tabelas)
- ✅ MT-RF028 com 12 massas de teste para UC-12
- ✅ TC-RF028 com 40 TCs para UC-12
- ✅ Relatório de delta gerado

---

**Contrato:** D:/IC2_Governanca/contracts/documentacao/execucao/aditivo.md
**Modo:** Governança rígida
**Aprovação:** 100% ou REPROVADO
