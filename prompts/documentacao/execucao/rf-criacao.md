Para o RFXXX...

Criar Requisito Funcional (RF) NOVO conforme D:/IC2_Governanca/contracts/documentacao/execucao/rf-criacao.md.

Modo governanca rigida. Nao negociar escopo. Nao extrapolar.

Seguir D:\IC2\CLAUDE.md.

---

## PRE-REQUISITOS BLOQUEANTES:

1. RF DEVE ser NOVO (sem legado ASPX/WebServices/SQL)
2. Pasta rf/[Fase]/[EPIC]/RFXXX/ DEVE existir
3. Templates RF.md e RF.yaml DEVEM estar acessiveis
4. STATUS.yaml NAO deve existir (RF novo)

**Se RF tem legado:** Usar rf-rl-criacao.md (cria RF + RL juntos)

---

## WORKFLOW DE EXECUCAO:

1. **Analisar requisitos fornecidos:**
   - Identificar tipo de RF (crud | leitura | integracao | batch)
   - Identificar entidades principais
   - Extrair regras de negocio (minimo 10)
   - Definir permissoes RBAC
   - Definir endpoints da API

2. **Gerar RFXXX.md (11 secoes obrigatorias):**
   - Secao 1: Objetivo
   - Secao 2: Escopo
   - Secao 3: Conceitos de Negocio
   - Secao 4: Funcionalidades (catalogo RF-CRUD, RF-VAL, RF-SEC)
   - Secao 5: Regras de Negocio (minimo 10 RNs)
   - Secao 6: Estados e Transicoes
   - Secao 7: Permissoes (RBAC)
   - Secao 8: Endpoints da API
   - Secao 9: Modelo de Dados
   - Secao 10: Dependencias
   - Secao 11: Integracoes Obrigatorias (i18n, auditoria, RBAC, Central)

3. **Gerar RFXXX.yaml:**
   - rf: { id, nome, versao, data, fase, epic, status, tipo_rf }
   - descricao
   - escopo
   - entidades
   - regras_negocio (minimo 10)
   - estados
   - transicoes
   - permissoes
   - integracoes
   - seguranca
   - rastreabilidade
   - catalog

4. **Criar STATUS.yaml:**
   - documentacao.rf = true
   - validacoes.rf_yaml_sincronizado = true
   - validacoes.rf_11_secoes_completas = true
   - validacoes.rf_minimo_10_regras = true
   - validacoes.rf_integracoes_obrigatorias = true

5. **Validar automaticamente:**
   ```bash
   python tools/docs/validator-docs.py RFXXX
   ```
   - Exit code 0 = APROVADO
   - Exit code != 0 = REPROVADO (corrigir e revalidar)

6. **Atualizar documentacao-funcional.md** (se existir)

---

## INTEGRACOES OBRIGATORIAS (Secao 11):

1. **i18n (Internacionalizacao):**
   - Chaves de traducao: rf.xxx.campo, rf.xxx.validacao.erro
   - Idiomas: pt-BR, en-US, es-ES

2. **Auditoria:**
   - Campos obrigatorios: created_at, created_by, updated_at, updated_by, deleted_at
   - Soft delete obrigatorio

3. **RBAC (Permissoes):**
   - Matriz de permissoes: view_any, view, create, update, delete
   - Escopo: Developer/Sistema/Cliente/Fornecedor

4. **Central de Funcionalidades:**
   - Cadastro da funcionalidade
   - Icone, ordem, menu pai
   - Permissoes associadas

---

## VALIDACOES OBRIGATORIAS:

1. RF.md tem 11 secoes completas
2. RF.md tem minimo 10 regras de negocio
3. RF.md tem Secao 11 (integracoes obrigatorias) completa
4. RF.md NAO tem referencias a legado (ASPX, WebServices, SQL)
5. RF.yaml sincronizado 100% com RF.md
6. STATUS.yaml criado com documentacao.rf = true
7. validator-docs.py passou (exit code 0)

---

## CRITERIO DE APROVACAO:

- ✅ APROVADO = TODAS as validacoes PASS + validator-docs.py exit code 0
- ❌ REPROVADO = QUALQUER validacao FAIL OU validator-docs.py exit code != 0

NAO EXISTE APROVACAO COM RESSALVAS.

---

## PROXIMO PASSO:

Apos RF criado e aprovado:

```
Conforme D:/IC2_Governanca/contracts/documentacao/execucao/uc-criacao.md para RFXXX.
Seguir D:\IC2\CLAUDE.md.
```

---

## IMPORTANTE:

- Este prompt cria RF NOVO (sem legado)
- Se RF tem legado (ASPX/WebServices/SQL), usar rf-rl-criacao.md
- Commit e push: responsabilidade do usuario (nao automatizado)
