MODO AUTONOMIA TOTAL: DETECTAR E EXECUTAR CONTRATO CORRETO AUTOMATICAMENTE

PASSO 1 (AUTOMÁTICO): LER STATUS.yaml DO RFXXX

Ler STATUS.yaml e verificar campo execucao.frontend:

```yaml
execucao:
  frontend: ???  # Pode estar vazio, null, ou com dados
```

PASSO 2 (AUTOMÁTICO): DECIDIR CONTRATO CORRETO

REGRA DE DETECÇÃO AUTOMÁTICA:

IF execucao.frontend está VAZIO, NULL ou NÃO EXISTE:
  → FRONTEND NOVO (primeira vez)
  → LER E EXECUTAR: docs/contracts/desenvolvimento/execucao/frontend-criacao.md
  → Criar frontend completo do zero
  → NÃO PERGUNTAR, EXECUTAR DIRETAMENTE

ELSE IF execucao.frontend JÁ TEM DADOS (data, status, commit, etc.):
  → ADEQUAÇÃO (frontend já existe)
  → LER E EXECUTAR: docs/contracts/desenvolvimento/execucao/frontend-adequacao.md
  → Ajustar frontend existente
  → NÃO PERGUNTAR, EXECUTAR DIRETAMENTE

IMPORTANTE:
- NÃO perguntar ao usuário qual contrato usar
- NÃO solicitar confirmação
- DETECTAR automaticamente pela presença de dados em execucao.frontend
- EXECUTAR imediatamente o contrato correto
- DECLARAR qual contrato foi selecionado (para transparência)

EXEMPLO DE DECLARAÇÃO:
"STATUS.yaml verificado: execucao.frontend está vazio → FRONTEND NOVO detectado.
Executando docs/contracts/desenvolvimento/execucao/frontend-criacao.md automaticamente."

OU

"STATUS.yaml verificado: execucao.frontend tem dados → ADEQUAÇÃO detectada.
Executando docs/contracts/desenvolvimento/execucao/frontend-adequacao.md automaticamente."

---

Seguir CLAUDE.md.

PRE-REQUISITOS OBRIGATORIOS (BLOQUEANTES):
Antes de QUALQUER acao, validar:

1. UC-RFXXX.md DEVE existir
2. STATUS.yaml DEVE ter documentacao.uc = true
3. Backend DEVE estar aprovado 100% (desenvolvimento.backend.conformidade = "100%")
4. MD-RFXXX.md DEVE existir OU STATUS.yaml ter md: false com justificativa valida
5. WF-RFXXX.md DEVE existir OU STATUS.yaml ter wf: false com justificativa valida

VALIDACAO DE PRE-REQUISITOS:
1. Verificar se backend foi aprovado:
   - STATUS.yaml desenvolvimento.backend.conformidade DEVE ser "100%"
   - Se < 100%: BLOQUEAR execucao frontend
   - Motivo: Frontend depende de contratos de API prontos

2. Verificar se MD-RFXXX.md existe
   - Se NAO existir:
     * Verificar STATUS.yaml campo md
     * Se md = false, validar se ha justificativa
     * Justificativas validas: "tabela unica sem complexidade", "CRUD simples sem relacionamentos", "nao aplicavel"
     * Se justificativa ausente ou invalida: BLOQUEAR execucao
   - Se existir: prosseguir

3. Verificar se WF-RFXXX.md existe
   - Se NAO existir:
     * Verificar STATUS.yaml campo wf
     * Se wf = false, validar se ha justificativa
     * Justificativas validas: "gestao administrativa backend-only", "CRUD simples", "nao aplicavel"
     * Se justificativa ausente ou invalida: BLOQUEAR execucao
   - Se existir: prosseguir

4. Se QUALQUER pre-requisito falhar:
   - PARAR imediatamente
   - REPROVAR com mensagem clara
   - NAO prosseguir com frontend

Antes de qualquer coisa, analise se tudo está implementado no backend e caso falte algo me avise imediatamente.

Preste MUITA atenção ao checklist obrigatório, pois é essencial que voce o siga.

Ao final me diga em qual menu eu posso acessar a funcionalidade desenvolvida.

Fique atento para que o layout siga nosso padrão já existente utilizado em http://localhost:4200/admin/management/sla-operacoes, http://localhost:4200/management/users, http://localhost:4200/management/roles etc.

Lembre de adicionar esse item ao menu.