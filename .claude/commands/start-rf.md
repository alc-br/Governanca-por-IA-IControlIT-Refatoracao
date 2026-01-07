---
description: Iniciar trabalho em um Requisito Funcional
allowed-tools: Read, Bash, TodoWrite, Task
---

# Iniciar RF

Prepare o ambiente para trabalhar em um Requisito Funcional específico.

## Instruções

1. **Pergunte ao usuário:** Qual RF deseja iniciar? (ex: RF-015)

2. **Valide:** RF existe em `D:\IC2_Governanca\documentacao\Fase-*/EPIC-*/RF-XXX/`
   ```bash
   # Buscar pasta do RF
   find docs/rf -type d -name "RF-015"
   ```

3. **Verifique documentação:**
   - [ ] `RF-XXX.md` existe
   - [ ] `UC-RF-XXX.md` existe
   - [ ] `MD-RF-XXX.md` existe
   - [ ] `user-stories.yaml` existe

4. **Leia STATUS.yaml** para entender estado atual:
   ```yaml
   documentacao:
     documentacao: true/false
     uc: true/false
     md: true/false
     wf: true/false
     user_stories: true/false

   implementacao:
     backend: true/false
     frontend: true/false
   ```

5. **Crie branch apropriado:**
   ```bash
   # Se backend não existe
   git checkout -b feature/RF-XXX-backend

   # Se backend existe, vai fazer frontend
   git checkout -b feature/RF-XXX-frontend

   # Se é manutenção
   git checkout -b feature/RF-XXX-manutencao
   ```

6. **Verifique ambiente:**
   ```bash
   # Backend: porta 5000 livre
   netstat -ano | findstr :5000

   # Frontend: porta 4200 ou 8080 livre
   netstat -ano | findstr :4200
   netstat -ano | findstr :8080
   ```

7. **Crie checklist com TodoWrite:**
   - [ ] Branch criado
   - [ ] Documentação validada
   - [ ] Ambiente preparado
   - [ ] Próximos passos identificados

8. **Informe status ao usuário:**
   ```
   ✅ RF-XXX pronto para desenvolvimento

   📂 Localização: D:\IC2_Governanca\documentacao\Fase-X/EPIC-YYY/RF-XXX/

   📋 Documentação:
   - RF: [completo/incompleto]
   - UC: [completo/incompleto]
   - MD: [completo/incompleto]
   - WF: [completo/incompleto]
   - User Stories: [completo/incompleto]

   🔧 Estado Atual:
   - Backend: [não iniciado/em desenvolvimento/completo]
   - Frontend: [não iniciado/em desenvolvimento/completo]
   - Testes: [não executados/parcial/completo]

   🌿 Branch: feature/RF-XXX-[tipo]

   🎯 Próximos Passos:
   [Listar baseado no STATUS.yaml]
   ```

## Exemplos de Uso

### Exemplo 1: RF novo (backend não existe)

```
Usuário: /start-rf
Agente: Qual RF deseja iniciar?
Usuário: RF-028
Agente:
✅ RF-028 pronto para desenvolvimento

📂 Localização: D:\IC2_Governanca\documentacao\Fase-2-Cadastros-e-Servicos-Transversais/EPIC003-CAD-Cadastros-Base/RF-028/

📋 Documentação:
- RF: completo ✅
- UC: completo ✅
- MD: completo ✅
- WF: completo ✅
- User Stories: completo ✅

🔧 Estado Atual:
- Backend: não iniciado ❌
- Frontend: não iniciado ❌
- Testes: não executados ❌

🌿 Branch: feature/RF-028-backend (criado)

🎯 Próximos Passos:
1. Implementar backend conforme CONTRATO-EXECUCAO-BACKEND
2. Executar validação Tester-Backend
3. Implementar frontend conforme CONTRATO-EXECUCAO-FRONTEND
4. Executar testes E2E
```

### Exemplo 2: RF com backend pronto (vai fazer frontend)

```
Usuário: /start-rf
Agente: Qual RF deseja iniciar?
Usuário: RF-015
Agente:
✅ RF-015 pronto para desenvolvimento de frontend

📂 Localização: D:\IC2_Governanca\documentacao\Fase-2-Cadastros-e-Servicos-Transversais/EPIC003-CAD-Cadastros-Base/RF-015/

📋 Documentação:
- RF: completo ✅
- UC: completo ✅
- MD: completo ✅
- WF: completo ✅
- User Stories: completo ✅

🔧 Estado Atual:
- Backend: completo ✅
- Frontend: não iniciado ❌
- Testes Backend: aprovado ✅ (Tester-Backend)

🌿 Branch: feature/RF-015-frontend (criado)

🎯 Próximos Passos:
1. Implementar frontend conforme CONTRATO-EXECUCAO-FRONTEND
2. Executar testes E2E
3. Deploy HOM
```

## Troubleshooting

### RF não encontrado

Se `find` não retornar nada:
- Verifique se RF existe na documentação
- Confirme número correto (RF-015 vs RF-15)
- Verifique se está na branch correta (dev)

### Porta ocupada

Se porta 5000 ou 4200/8080 estiver ocupada:
- Identificar processo: `netstat -ano | findstr :5000`
- Matar processo se for do projeto: `taskkill /PID <pid> /F`
- Ou usar porta alternativa

### Branch já existe

Se branch `feature/RF-XXX-backend` já existir:
- Verificar se é trabalho anterior incompleto
- Fazer checkout do branch existente ao invés de criar novo
- Atualizar com `git pull origin dev`

## Notas

- Este comando **NÃO executa** implementação, apenas prepara o ambiente
- Para implementar, use prompts de `D:\IC2_Governanca\prompts\novo/` ou `D:\IC2_Governanca\prompts\adequacao/`
- Sempre verifique STATUS.yaml para entender estado atual
