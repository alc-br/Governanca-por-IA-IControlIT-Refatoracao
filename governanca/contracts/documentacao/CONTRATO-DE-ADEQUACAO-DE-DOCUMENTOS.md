# CONTRATO-DE-ADEQUACAO-DE-DOCUMENTOS

Versão: 2.0
Data: 2025-12-31
Status: Ativo

================================================================
OBJETIVO
================================================================

Este contrato define as regras obrigatórias para ADEQUAÇÃO, CORREÇÃO e NORMALIZAÇÃO
dos documentos existentes de um Requisito Funcional (RFXXX) aos templates
oficiais atualizados do projeto.

Este contrato NÃO autoriza:
- Criação de novos requisitos
- Expansão de escopo
- Inferência funcional
- Implementação de código

================================================================
ESCOPO
================================================================

Este contrato se aplica exclusivamente aos documentos já existentes do RFXXX:

- RFXXX.md
- RFXXX.yaml
- UC-RFXXX.md
- UC-RFXXX.yaml
- WF-RFXXX.md
- MD-RFXXX.yaml
- STATUS.yaml

================================================================
REGRA CENTRAL
================================================================

O objetivo é garantir que TODOS os documentos estejam 100% aderentes
aos templates atualizados, sem exceções.

Qualquer divergência entre documentos é considerada falha grave.

================================================================
PAPEL DO VALIDADOR AUTOMÁTICO (validator-docs.py)
================================================================

O validador automático (validator-docs.py) é a FERRAMENTA OFICIAL de conformidade.

### O que o validador GARANTE

✅ Conformidade estrutural:
- Existência de arquivos obrigatórios
- Estrutura de seções em arquivos .md
- Estrutura de campos em arquivos .yaml
- Sintaxe YAML válida
- Metadados obrigatórios em cabeçalhos .md

✅ Conformidade sintática:
- Parsing YAML sem erros
- Formato de cabeçalhos Markdown
- Campos obrigatórios presentes

✅ Detecção de problemas:
- Arquivos duplicados (.backup, .old, etc)
- Arquivos extras não permitidos
- Gaps classificados por severidade (CRÍTICO, IMPORTANTE, MENOR)

### O que o validador NÃO GARANTE

❌ Semântica de negócio:
- Qualidade textual das descrições
- Coerência lógica entre regras de negócio
- Completude funcional do RF

❌ Rastreabilidade semântica:
- Se UC cobre corretamente o RF (use validator-rf-uc.py)
- Se MD atende todos os UCs
- Se WF reflete corretamente os fluxos

❌ Criação de conteúdo:
- O validador NÃO cria documentos
- O validador NÃO corrige documentos
- O validador NÃO infere conteúdo faltante

### Quando confiar no validador

✅ Estrutura e sintaxe → confiança total
✅ Conformidade com templates → confiança total
✅ Detecção de gaps → confiança total

❌ Qualidade semântica → validação humana obrigatória
❌ Cobertura funcional → usar validadores específicos (validator-rf-uc.py)

================================================================
CLASSIFICAÇÃO DE GAPS (SEVERIDADE)
================================================================

O validador classifica gaps em 3 níveis de severidade:

### CRÍTICO

Bloqueia conclusão do contrato.

Exemplos:
- Arquivo obrigatório não existe
- Sintaxe YAML inválida
- Arquivo não pode ser lido

Ação obrigatória:
- Corrigir imediatamente
- Re-executar validador
- NÃO pode avançar com gaps CRÍTICOS

### IMPORTANTE

Bloqueia conclusão do contrato.

Exemplos:
- Seção do template não encontrada em .md
- Campo obrigatório ausente em .yaml

Ação obrigatória:
- Corrigir imediatamente
- Re-executar validador
- NÃO pode avançar com gaps IMPORTANTES

### MENOR

Bloqueia conclusão SE afetar rastreabilidade.

Exemplos:
- Metadado do cabeçalho ausente
- Campo não obrigatório do template ausente

Ação obrigatória:
- Corrigir se afetar rastreabilidade
- Justificar se não for corrigir (registrar em STATUS.yaml ou observação)
- Gaps MENOR recorrentes = dívida técnica

### Regra de bloqueio por severidade

```
Gap CRÍTICO → BLOQUEIA SEMPRE
Gap IMPORTANTE → BLOQUEIA SEMPRE
Gap MENOR → BLOQUEIA SE:
  - Afetar rastreabilidade
  - For recorrente (>3 ocorrências)
  - Não tiver justificativa registrada
```

================================================================
DEFINIÇÃO TÉCNICA DE "CONFORME"
================================================================

Um RF é considerado CONFORME quando:

```python
conforme = (
    all(v.existe and v.valido for v in arquivos_esperados.values()) and
    len(arquivos_duplicados) == 0 and
    total_gaps == 0
)
```

Traduzindo:

✅ Todos os arquivos esperados:
- existem (v.existe = True)
- são válidos (v.valido = True)
- têm estrutura conforme (v.estrutura_conforme = True)

✅ NÃO existem arquivos duplicados:
- Sem .backup
- Sem .old
- Sem .temp

✅ Total de gaps = 0:
- Nenhum gap CRÍTICO
- Nenhum gap IMPORTANTE
- Nenhum gap MENOR (ou todos justificados)

================================================================
ARQUIVOS EXTRAS - REGRA FORMAL
================================================================

O validador detecta arquivos extras que não estão no template.

### Arquivos extras PERMITIDOS

✅ README.md → sempre permitido (navegação)
✅ user-stories.yaml → sempre permitido (integração DevOps)

### Qualquer outro arquivo extra

❌ É considerado falha bloqueante
❌ Deve ser removido ou movido para pasta Apoio/
❌ NÃO pode existir na raiz do RF

Regra de ouro:
```
Se não está no template E não é README.md ou user-stories.yaml
  → É arquivo extra inválido
```

================================================================
INEXISTÊNCIA DE DOCUMENTOS
================================================================

Quando um documento NÃO existir, o agente DEVE:

1. PARAR este contrato
2. Executar o contrato de criação correspondente
3. Validar o documento criado
4. Retornar a este contrato

Contratos de criação disponíveis:

- UC
  - \D:\IC2_Governanca\contracts\documentacao\CONTRATO-GERACAO-DOCS-UC.md
  - \docs\checklists\checklist-documentacao-uc.yaml

- WF
  - \D:\IC2_Governanca\contracts\documentacao\CONTRATO-GERACAO-DOCS-WF.md
  - \docs\checklists\checklist-documentacao-wf.yaml

- MD
  - \D:\IC2_Governanca\contracts\documentacao\CONTRATO-GERACAO-DOCS-MD.md
  - \docs\checklists\checklist-documentacao-md.yaml

- MT
  - \D:\IC2_Governanca\contracts\documentacao\CONTRATO-GERACAO-DOCS-MT.md
  - \docs\checklists\checklist-documentacao-mt.yaml

- TC
  - \D:\IC2_Governanca\contracts\documentacao\CONTRATO-GERACAO-DOCS-TC.md
  - \docs\checklists\checklist-documentacao-tc.yaml

Proibições:
- NÃO pode continuar com documento faltante
- NÃO pode criar "provisório" ou "placeholder"
- NÃO pode inferir conteúdo sem template

================================================================
WORKFLOW OBRIGATÓRIO
================================================================

1. Executar validador (primeira vez):
   python D:\IC2_Governanca\tools\docs\validator-docs.py RFXXX

2. Abrir auditoria.json:
   D:\IC2\relatorios\rfxxx\auditoria.json

3. Ler TODOS os gaps:
   - Identificar severidade (CRÍTICO, IMPORTANTE, MENOR)
   - Ler mensagem completa
   - Ler template_original
   - Ler documento_analisado
   - Ler acao_necessaria

4. Executar EXATAMENTE a ação necessária descrita:
   - NÃO criar solução alternativa
   - NÃO "resolver de outro jeito"
   - Seguir o que o JSON indica

5. Corrigir documentos:
   - Usar Edit tool (nunca Write)
   - Preservar conteúdo existente
   - Adicionar apenas o que está faltando

6. Re-executar validador:
   python D:\IC2_Governanca\tools\docs\validator-docs.py RFXXX

7. Repetir passos 2-6 até:
   conforme = true
   total_gaps = 0

================================================================
USO DO JSON COMO FONTE NORMATIVA
================================================================

O arquivo auditoria.json gerado pelo validador é FONTE NORMATIVA.

Regras:

✅ O agente DEVE:
- Ler TODO o JSON (não apenas resumo)
- Executar EXATAMENTE a ação descrita em cada gap
- NÃO ignorar gaps MENOR sem justificativa
- NÃO criar correções "criativas"

❌ O agente NÃO PODE:
- Resumir gaps sem ler detalhes
- Inventar soluções alternativas
- Corrigir "do seu jeito"
- Ignorar campos template_original ou acao_necessaria

Exemplo de leitura correta:

```json
{
  "tipo": "IMPORTANTE",
  "mensagem": "Seção esperada não encontrada: '## 2. ESCOPO'",
  "template_original": "No template original está assim:\n## 2. ESCOPO\n(deve estar presente no documento)",
  "acao_necessaria": "Adicionar seção '## 2. ESCOPO' no documento"
}
```

Ação obrigatória:
→ Adicionar EXATAMENTE `## 2. ESCOPO` no documento
→ NÃO adicionar `## Escopo` (case diferente)
→ NÃO adicionar `## 2 - ESCOPO` (formato diferente)

================================================================
TRATAMENTO DE GAPS MENOR RECORRENTES
================================================================

Gaps MENOR isolados podem ser justificados.
Gaps MENOR recorrentes são dívida técnica.

Regras:

✅ Se houver 1-2 gaps MENOR:
- Pode justificar em STATUS.yaml
- Pode justificar em observação do commit
- Pode marcar como "aceito com ressalvas"

❌ Se houver >3 gaps MENOR:
- É dívida técnica formal
- Deve ser corrigida
- NÃO pode ser justificada genericamente

Registro de justificativa (STATUS.yaml):

```yaml
validacoes:
  gaps_menor_justificados:
    - tipo: metadado_cabecalho
      arquivo: RF046.md
      motivo: "Metadado 'Autor' não aplicável a RFs legados"
      data: 2025-12-31
      aprovado_por: "Tech Lead"
```

================================================================
VALIDAÇÃO COMPLEMENTAR (RASTREABILIDADE)
================================================================

O validator-docs.py valida estrutura.
Para validar rastreabilidade, use:

```bash
# Cobertura RF → UC → TC
python D:\IC2_Governanca\tools\docs\validator-rf-uc.py RFXXX

# Separação RF / RL
python D:\IC2_Governanca\tools\docs\validator-rl.py RFXXX

# Governança completa
python D:\IC2_Governanca\tools\docs\validator-governance.py RFXXX
```

Ordem de execução obrigatória:

1. validator-docs.py → estrutura OK
2. validator-rf-uc.py → rastreabilidade OK
3. validator-rl.py → separação RF/RL OK
4. validator-governance.py → governança completa OK

================================================================
CRITÉRIO DE CONCLUSÃO
================================================================

Este contrato só é considerado CONCLUÍDO quando:

✅ Execução técnica:
- validator-docs.py executou sem erros de sistema
- auditoria.json foi gerado com sucesso

✅ Conformidade estrutural:
- conforme = true
- total_gaps = 0
- arquivos_duplicados = []
- arquivos_extra = [] (exceto README.md e user-stories.yaml)

✅ Conformidade semântica (se aplicável):
- validator-rf-uc.py passou (exit code 0)
- Todos os gaps MENOR foram corrigidos ou justificados

✅ Rastreabilidade:
- RF → UC → WF → MD completa
- IDs canônicos em todos os documentos
- Nenhuma inferência fora do RF

================================================================
REGRA DE BLOQUEIO
================================================================

Se NÃO for possível atingir conformidade total:

❌ NÃO entregar parcialmente
❌ NÃO marcar como concluído
❌ NÃO criar "conformidade com ressalvas" sem justificativa formal

✅ Registrar o motivo técnico da falha:
- Em arquivo BLOQUEIO-RFXXX.md na pasta do RF
- Incluir saída completa do validador
- Incluir análise de causa raiz
- Propor plano de correção

Estrutura de BLOQUEIO-RFXXX.md:

```markdown
# BLOQUEIO - RFXXX

## Contexto
Tentativa de adequação sob CONTRATO-DE-ADEQUACAO-DE-DOCUMENTOS

## Causa Raiz
[Descrição técnica do que impediu conformidade]

## Evidência
\`\`\`json
[Trecho relevante do auditoria.json]
\`\`\`

## Tentativas Realizadas
1. [Ação 1] → [Resultado]
2. [Ação 2] → [Resultado]

## Proposta de Resolução
[Plano técnico para desbloqueio]

## Próximos Passos
- [ ] [Ação 1]
- [ ] [Ação 2]
```

================================================================
LINGUAGEM TÉCNICA DO VALIDADOR (GLOSSÁRIO)
================================================================

Para alinhar comunicação entre agente e validador:

### Campos de FileValidation

- `existe` → arquivo foi encontrado no disco
- `valido` → parsing bem-sucedido E sem gaps CRÍTICOS
- `estrutura_conforme` → sem gaps de nenhum tipo (CRÍTICO, IMPORTANTE, MENOR)

### Campos de RFValidationResult

- `conforme` → RF completamente aderente ao template
- `total_gaps` → soma de todos os gaps de todos os arquivos
- `arquivos_duplicados` → lista de .backup, .old, .temp
- `arquivos_extra` → lista de arquivos não permitidos

### Tipos de Gap

- `CRÍTICO` → bloqueia sempre
- `IMPORTANTE` → bloqueia sempre
- `MENOR` → bloqueia condicionalmente

### Categorias de Gap

- `estrutura_md` → seção faltando em Markdown
- `metadados` → cabeçalho YAML faltando em .md
- `sintaxe_yaml` → YAML inválido
- `campos_obrigatorios` → campo obrigatório ausente
- `estrutura_yaml` → campo do template ausente

================================================================
PROIBIÇÕES ABSOLUTAS
================================================================

Durante a adequação é PROIBIDO:

❌ Criar novos casos de uso (UC05+) sem RF correspondente
❌ Adicionar regras de negócio não documentadas no RF
❌ Modificar IDs canônicos (RN-UC-XXX, RN-RF-XXX)
❌ Remover conteúdo existente sem análise de impacto
❌ Criar arquivos fora da estrutura do template
❌ Ignorar gaps CRÍTICOS ou IMPORTANTES
❌ Justificar gaps MENOR genericamente (>3 ocorrências)
❌ Modificar templates para "adequar ao documento"

================================================================
AUTORIZAÇÃO DE CORREÇÃO
================================================================

O agente está AUTORIZADO a:

✅ Adicionar seções faltantes do template
✅ Adicionar campos obrigatórios do template
✅ Corrigir sintaxe YAML
✅ Corrigir formatação de cabeçalhos
✅ Mover arquivos extras para Apoio/
✅ Remover arquivos duplicados (.backup)
✅ Adicionar metadados obrigatórios

O agente NÃO está autorizado a:

❌ Criar conteúdo funcional novo (regras, fluxos)
❌ Modificar regras de negócio existentes
❌ Inferir comportamentos não documentados
❌ Alterar estrutura de pastas do RF
❌ Modificar templates oficiais

================================================================
EVIDÊNCIA DE CONFORMIDADE
================================================================

Ao concluir, o agente DEVE apresentar:

1. Saída do validador:
   ```bash
   python validator-docs.py RFXXX
   # Exit code: 0
   # Output: "✅ RFXXX: CONFORME"
   ```

2. Trecho do auditoria.json:
   ```json
   {
     "rf_id": "RFXXX",
     "conforme": true,
     "total_gaps": 0,
     "arquivos_duplicados": [],
     "arquivos_extra": []
   }
   ```

3. Resumo de correções:
   - Arquivos corrigidos: [lista]
   - Gaps CRÍTICOS corrigidos: N
   - Gaps IMPORTANTES corrigidos: N
   - Gaps MENOR corrigidos: N
   - Gaps MENOR justificados: N

================================================================
FIM DO CONTRATO
================================================================
