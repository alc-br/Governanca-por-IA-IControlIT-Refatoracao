MODO AUTONOMIA TOTAL: DETECTAR E EXECUTAR CONTRATO CORRETO AUTOMATICAMENTE

PASSO 1 (AUTOMÁTICO): LER STATUS.yaml DO RFXXX

Ler STATUS.yaml e verificar campo execucao.backend:

```yaml
execucao:
  backend: ???  # Pode estar vazio, null, ou com dados
```

PASSO 2 (AUTOMÁTICO): DECIDIR CONTRATO CORRETO

REGRA DE DETECÇÃO AUTOMÁTICA:

IF execucao.backend está VAZIO, NULL ou NÃO EXISTE:
  → BACKEND NOVO (primeira vez)
  → LER E EXECUTAR: D:/IC2_Governanca/contracts/desenvolvimento/execucao/backend-criacao.md
  → Criar backend completo do zero
  → NÃO PERGUNTAR, EXECUTAR DIRETAMENTE

ELSE IF execucao.backend JÁ TEM DADOS (data, status, commit, etc.):
  → ADEQUAÇÃO (backend já existe)
  → LER E EXECUTAR: D:/IC2_Governanca/contracts/desenvolvimento/execucao/backend-adequacao.md
  → Ajustar backend existente
  → NÃO PERGUNTAR, EXECUTAR DIRETAMENTE

IMPORTANTE:
- NÃO perguntar ao usuário qual contrato usar
- NÃO solicitar confirmação
- DETECTAR automaticamente pela presença de dados em execucao.backend
- EXECUTAR imediatamente o contrato correto
- DECLARAR qual contrato foi selecionado (para transparência)

EXEMPLO DE DECLARAÇÃO:
"STATUS.yaml verificado: execucao.backend está vazio → BACKEND NOVO detectado.
Executando D:/IC2_Governanca/contracts/desenvolvimento/execucao/backend-criacao.md automaticamente."

OU

"STATUS.yaml verificado: execucao.backend tem dados → ADEQUAÇÃO detectada.
Executando D:/IC2_Governanca/contracts/desenvolvimento/execucao/backend-adequacao.md automaticamente."

---

Modo governanca rigida. Nao negociar escopo. Nao extrapolar.
Seguir D:\IC2\CLAUDE.md.

Preste MUITA atencao ao checklist obrigatorio, pois e essencial que voce o siga.

PRE-REQUISITOS OBRIGATORIOS (BLOQUEANTES):
Antes de QUALQUER acao, validar:

1. UC-RFXXX.md DEVE existir
2. STATUS.yaml DEVE ter documentacao.uc = true
3. MD-RFXXX.md DEVE existir OU STATUS.yaml ter md: false com justificativa valida
4. WF-RFXXX.md DEVE existir OU STATUS.yaml ter wf: false com justificativa valida

VALIDACAO DE PRE-REQUISITOS:
1. Verificar se MD-RFXXX.md existe
   - Se NAO existir:
     * Verificar STATUS.yaml campo md
     * Se md = false, validar se ha justificativa
     * Justificativas validas: "tabela unica sem complexidade", "CRUD simples sem relacionamentos", "nao aplicavel"
     * Se justificativa ausente ou invalida: BLOQUEAR execucao
   - Se existir: prosseguir

2. Verificar se WF-RFXXX.md existe
   - Se NAO existir:
     * Verificar STATUS.yaml campo wf
     * Se wf = false, validar se ha justificativa
     * Justificativas validas: "gestao administrativa backend-only", "CRUD simples", "nao aplicavel"
     * Se justificativa ausente ou invalida: BLOQUEAR execucao
   - Se existir: prosseguir

3. Se QUALQUER pre-requisito falhar:
   - PARAR imediatamente
   - REPROVAR com mensagem clara
   - NAO prosseguir com backend

Execute apenas os testes previstos neste contrato
(smoke tests e caminho feliz).
NAO validar violacoes de contrato.
NAO assumir comportamento implicito.