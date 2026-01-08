Para o RF003

Crie os documentos de Casos de Uso (UC) conforme contracts/documentacao/execucao/CONTRATO-GERACAO-DOCS-UC.md.

Se já houver um documento de UC criado, você precisa validar se está dentro dos padrões do template e se foi levantado todos os cenários para cobrir todo o requisito funcional.

Modo governanca rigida. Nao negociar escopo. Nao extrapolar.

Seguir D:\IC2\CLAUDE.md.

Preste MUITA atencao ao checklist obrigatorio, pois e essencial que voce o siga.

IMPORTANTE:
1. Leia os templates em templates/:
   - UC.md
   - UC.yaml

2. Analise o RFXXX.md e RFXXX.yaml para extrair tudo o que for necessário para os Casos de Uso.

3. Esses documentos são únicos, então não pode automatizar de nenhuma forma, tudo deve ser criado de forma personalizada garantindo a cobertura total do requisito.

NAO invente dados e informações. Tudo deve vir do RFXXX.md e RFXXX.yaml.

---

## WORKFLOW OBRIGATÓRIO - VALIDAÇÃO E CORREÇÃO ITERATIVA

### Fase 1: Criação/Leitura Inicial
- Criar UC-RFXXX.md e UC-RFXXX.yaml OU ler os existentes (se já criados)

### Fase 2: Validação (1ª Rodada)
- Execute OBRIGATORIAMENTE: "\docs\tools\docs\validator-docs.py --rf RFXXX --doc UC"
- Este comando irá gerar o arquivo: \relatorios\rfxxx\uc\auditoria.json

### Fase 3: Análise e Correção (ITERATIVA)

**Se houver gaps/warnings/erros no auditoria.json:**

**PROIBIDO:**
- ❌ Parar apenas por identificar gaps
- ❌ Declarar falha sem corrigir
- ❌ Atualizar STATUS.yaml com validação falhando

**OBRIGATÓRIO:**
1. **Identificar gaps** - Analisar auditoria.json para entender o que falta
2. **Corrigir/Complementar UCs** - Adicionar UCs faltantes, ajustar fluxos, completar regras de negócio
3. **Revalidar** - Executar validator-docs.py novamente
4. **Repetir** - Se ainda houver gaps, repetir passos 1-3
5. **Prosseguir** - Apenas quando auditoria.json indicar 100% de conformidade

**Critério de Falha Definitiva:**
- Apenas se após 3 iterações de correção ainda houver falhas (indica problema estrutural no RF)
- Se RF for inconsistente/contraditório
- Se tentar criar funcionalidades fora do escopo do RF

### Fase 4: Finalização
- Atualize STATUS.yaml **APENAS** se validação passar (100% PASS, sem warnings)
- Se o STATUS.yaml ainda não tiver sido criado, crie de acordo com o template e em seguida atualize

---

IMPORTANTE:

Se o UC já estiver criado:
1. Valide se está dentro dos padrões dos templates \docs\templates
2. Se não estiver, ajuste-o para que entre nos padrões
3. **Se faltar UCs para cobrir 100% do RF:** CRIE os UCs faltantes imediatamente
4. Revalide até atingir 100% de conformidade

**Regra de Ouro:** Gaps de cobertura são **GATILHOS DE CORREÇÃO**, não motivo de parada imediata.

Ao final, caso tudo esteja completo (auditoria.json 100% PASS, sem warnings), escreva em letra grande:
# ✅ RFXXX 100% Pronto