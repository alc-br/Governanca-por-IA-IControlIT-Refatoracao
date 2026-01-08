Seguindo o contrato D:\IC2_Governanca\governanca\contracts\manutencao\manutencao-controlada.md.
Modo governanca rigida. Nao negociar escopo. Nao extrapolar.
Seguir D:\IC2\CLAUDE.md.

Para corrigir o seguinte problema:

---
## PROBLEMA IDENTIFICADO

**Descrição:** {DESCRIÇÃO_BREVE_DO_PROBLEMA}

**RF Afetado:** {RF_ID} (se aplicável, ou "N/A")

**Arquivo(s) Afetado(s):**
- {CAMINHO_ARQUIVO_1} (linha aproximada: {LINHA})
- {CAMINHO_ARQUIVO_2} (linha aproximada: {LINHA}, se aplicável)

**Causa Raiz:**
{EXPLICAÇÃO_TÉCNICA_DA_CAUSA}

---
## CORREÇÃO NECESSÁRIA

**O que precisa ser feito:**
1. {AÇÃO_ESPECÍFICA_1}
2. {AÇÃO_ESPECÍFICA_2}
3. {AÇÃO_ESPECÍFICA_3}

**Escopo estimado:** Cirúrgico (1-3 arquivos, 1 camada)

---
## VALIDAÇÃO DA CORREÇÃO

**Após correção, validar que:**
- [ ] {VALIDAÇÃO_TÉCNICA_1}
- [ ] {VALIDAÇÃO_TÉCNICA_2}
- [ ] {VALIDAÇÃO_TÉCNICA_3}
- [ ] Backend compila sem erros (se aplicável)
- [ ] Frontend compila sem erros (se aplicável)
- [ ] Testes passam (se aplicável)

---

## EXEMPLO CONCRETO

```
Seguindo o contrato D:\IC2_Governanca\governanca\contracts\manutencao\manutencao-controlada.md.
Modo governanca rigida. Nao negociar escopo. Nao extrapolar.
Seguir D:\IC2\CLAUDE.md.

Para corrigir o seguinte problema:

---
## PROBLEMA IDENTIFICADO

**Descrição:** Incompatibilidade de tipo Int64 → Int32 em RolePermissions

**RF Afetado:** N/A (problema de infraestrutura)

**Arquivo(s) Afetado(s):**
- D:\IC2\backend\src\Infrastructure\Data\ApplicationDbContextInitialiser.cs (linha 1217)

**Causa Raiz:**
Coluna RolePermissions.PermissionId é BIGINT (Int64) no banco de dados, mas código usa int (Int32) causando falha no seed de dados.

---
## CORREÇÃO NECESSÁRIA

**O que precisa ser feito:**
1. Alterar tipo de PermissionId de int para long na linha 1217
2. Validar que não há outros usos de PermissionId como int no mesmo arquivo
3. Recompilar backend

**Escopo estimado:** Cirúrgico (1 arquivo, 1 camada - Infrastructure)

---
## VALIDAÇÃO DA CORREÇÃO

**Após correção, validar que:**
- [ ] Backend compila sem erros de tipo
- [ ] Backend inicia sem exceptions no ApplicationDbContextInitialiser
- [ ] Endpoint /health responde com status 200
- [ ] Seed de dados executa completamente (verificar logs)
```
