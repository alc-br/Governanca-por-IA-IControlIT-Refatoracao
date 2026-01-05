Conforme CONTRATO DE DOCUMENTACAO-ESSENCIAL para RF070.
Modo governanca rigida. Nao negociar escopo. Nao extrapolar.
Seguir CLAUDE.md.

Preste MUITA atencao ao checklist obrigatorio, pois e essencial que voce o siga.

IMPORTANTE:
1. Primeiro leia os documentos fonte em docs/inicial/:
   - CartorioFin_Pro_Especificacao_Funcional_v1.1.md
   - CartorioFin_Pro_BPD_v1.1.md

2. Depois leia os templates em docs/templates/:
   - RF.md
   - RF.yaml
   - UC.md
   - UC.yaml
   - MD.md
   - MD.yaml
   - WF.md

3. Extraia do documento fonte todas as informacoes do RF citado acima e documente conforme os templates.

NAO invente requisitos. Todos devem vir dos documentos fonte.

Após criar RF, UC e MD:
- Execute OBRIGATORIAMENTE o validator-rf-uc.py
- Interprete o resultado
- Atualize STATUS.yaml apenas se PASS