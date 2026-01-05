# 🧪 GUIA DO AGENTE TESTER (TESTADOR)

**Versão:** 1.0
**Data:** 2025-01-12
**Público:** Agente Tester (Testador/QA)

---

## 🎯 Seu Papel

Como **agente tester**, você é responsável por:

1. **Criar documentação de testes** (CNs, TCs, MTs)
2. **Criar robôs de teste** automatizados (Python, Playwright)
3. **Executar testes** nas 3 camadas (Backend, Outros, Sistema)
4. **Capturar evidências** (screenshots, logs, relatórios)
5. **Gerar relatórios** de execução consolidados
6. **Garantir qualidade** antes de ir para produção

---

## 📚 Documentos Obrigatórios para Você

### LEIA PRIMEIRO (ordem de prioridade):

1. **[REGRAS-CRITICAS.md](./REGRAS-CRITICAS.md)** ⚠️ OBRIGATÓRIO
   - Regras que se aplicam a TODOS os agentes

2. **[MANUAL-DE-EXECUCAO.md](./MANUAL-DE-EXECUCAO.md)** ⭐ PRINCIPAL
   - Processo completo de execução de testes
   - Ordem obrigatória (Backend → Outros → Sistema)
   - Criação automática de robôs
   - Captura de evidências

3. **[MANUAL-DE-DOCUMENTACAO.md](./MANUAL-DE-DOCUMENTACAO.md)** 📋 ESTRUTURA
   - Tipos de documentos de teste (CN, TC, MT)
   - Estrutura de pastas (Testes/Sistema, Backend, Outros)
   - Nomenclatura padronizada
   - Templates

4. **RF e UC da funcionalidade** 🎯 REQUISITOS
   - Ler RF para entender regras de negócio
   - Ler UCs para entender fluxos
   - Criar CNs e TCs baseados nos UCs

---

## 🛠️ Suas Principais Tarefas

### 1. Criar Documentação de Testes

**Quando:** Após RF e UCs estarem prontos

**Processo:**

```
1. Ler RF completo
   ↓
2. Ler todos os UCs
   ↓
3. Para cada UC, criar:
   ├── CN-UC##-nome.md (Cenário de Negócio)
   ├── TC-UC##-nome.md (Teste de Caso)
   └── MT01-TC-UC##.csv (Massa de Teste)
   ↓
4. Criar em 3 camadas (quando aplicável):
   ├── Testes/Sistema/
   ├── Testes/Backend/
   └── Testes/Outros/
```

**Estrutura de pastas:**
```
docs/Fases/Fase-X/EPIC-XXX/RF-XXX-NNN/
└── Testes/
    ├── Sistema/              ← E2E (frontend + backend)
    │   ├── CN-UC01-criar-usuario.md
    │   ├── TC-UC01-criar-usuario.md
    │   ├── MT01-TC-UC01.csv
    │   └── EX-TC-UC01.md     ← Evidências após execução
    ├── Backend/              ← API isolada
    │   ├── CN-UC01-criar-usuario.md
    │   ├── TC-UC01-criar-usuario.md
    │   └── MT01-TC-UC01.csv
    └── Outros/               ← Performance, Segurança, etc.
        ├── CN-UC01-criar-usuario.md
        └── TC-UC01-criar-usuario.md
```

**⚠️ IMPORTANTE:** A nomenclatura é a MESMA em todas as camadas!
- ✅ `CN-UC01-criar-usuario.md` (em Sistema, Backend, Outros)
- ❌ `CN-API-UC01` ou `CN-SISTEMA-UC01` (NUNCA use prefixos de camada)

**Templates:**
- `docs/99-Templates/TEMPLATE-CENARIO-NEGOCIO.md`
- `docs/99-Templates/TEMPLATE-TESTE-CASO.md`
- `docs/99-Templates/TEMPLATE-MASSA-TESTE.csv`

**Documentação:**
- [MANUAL-DE-DOCUMENTACAO.md](./MANUAL-DE-DOCUMENTACAO.md) - Seção "Camadas de Testes"

---

### 2. Criar Robôs de Teste

**Quando:** Antes de executar testes (criação automática se não existir)

**Localização dos robôs:**
```
docs/Fases/Fase-X/EPIC-XXX/RF-XXX-NNN/
└── Testes/
    ├── Sistema/
    │   └── ROBO01-TC-UC01-criar-usuario.py  ← Playwright
    ├── Backend/
    │   └── ROBO01-TC-UC01-criar-usuario.py  ← requests
    └── Outros/
        ├── ROBO01-PERF-UC01.py              ← Performance (Locust)
        └── ROBO01-SEG-UC01.py               ← Segurança (OWASP ZAP)
```

**Tipos de robôs:**

#### 2.1. Robô Backend (API)
```python
# ROBO01-TC-UC01-criar-usuario.py
import requests
import json
import csv

API_URL = "http://localhost:5000/api"
TOKEN = ""  # Obtido via login

def test_criar_usuario():
    """Testa criação de usuário via API"""

    # Ler massa de teste
    with open('MT01-TC-UC01.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Executar teste
            response = requests.post(
                f"{API_URL}/usuarios",
                headers={"Authorization": f"Bearer {TOKEN}"},
                json={
                    "nome": row['nome'],
                    "email": row['email'],
                    "login": row['login'],
                    "senha": row['senha']
                }
            )

            # Validar resultado
            assert response.status_code == 200
            print(f"✅ Usuário {row['nome']} criado com sucesso")

if __name__ == "__main__":
    test_criar_usuario()
```

#### 2.2. Robô Sistema (E2E)
```python
# ROBO01-TC-UC01-criar-usuario.py
from playwright.sync_api import sync_playwright
import csv

def test_criar_usuario_e2e():
    """Testa criação de usuário via interface web"""

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Login
        page.goto("http://localhost:4200/sign-in")
        page.fill('input[name="email"]', 'admin@test.com')
        page.fill('input[name="password"]', 'Test@123')
        page.click('button[type="submit"]')
        page.wait_for_url("**/dashboard")

        # Navegar para Gestão de Usuários
        page.goto("http://localhost:4200/admin/users")

        # Ler massa de teste
        with open('MT01-TC-UC01.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Clicar em "Novo Usuário"
                page.click('button:has-text("Novo Usuário")')

                # Preencher formulário
                page.fill('input[name="nome"]', row['nome'])
                page.fill('input[name="email"]', row['email'])
                page.fill('input[name="login"]', row['login'])
                page.fill('input[name="senha"]', row['senha'])

                # Salvar
                page.click('button:has-text("Salvar")')

                # Capturar evidência
                page.screenshot(path=f"evidencias/{row['login']}_OK.png")

                print(f"✅ Usuário {row['nome']} criado com sucesso (E2E)")

        browser.close()

if __name__ == "__main__":
    test_criar_usuario_e2e()
```

#### 2.3. Teste de Autorização (Backend)

⚠️ **IMPORTANTE:** Sempre testar autorização para garantir que erros 403 não ocorram.

**Ver:** [ERROS-A-EVITAR.md](../ERROS-A-EVITAR.md) - Erro #3 (Confusão entre Policy e Roles)

**Exemplo de teste de autorização:**
```python
import requests
import jwt

def test_authorization_403():
    """Testa se endpoint com permissão incorreta retorna 403"""

    # 1. Login com usuário Developer
    login_response = requests.post(
        "http://localhost:5000/api/auth/login",
        json={"email": "dev@test.com", "password": "Test@123"}
    )
    token = login_response.json()['accessToken']

    # 2. Verificar permissões no token
    decoded = jwt.decode(token, options={"verify_signature": False})
    print("Permissões no token:", decoded.get('permission', []))

    # 3. Testar endpoint que requer permissão específica
    response = requests.delete(
        "http://localhost:5000/api/empresas/123e4567-e89b-12d3-a456-426614174000/permanent",
        headers={"Authorization": f"Bearer {token}"}
    )

    # 4. Verificar resultado
    if response.status_code == 403:
        print("❌ ERRO 403: Verificar autorização no Command")
        print("   - Endpoint configurado:", "AuthorizationPolicies.CompaniesPermanentDelete")
        print("   - Command deve usar: [Authorize(Roles = 'Developer,Super Admin')]")
        print("   - NÃO usar: [Authorize(Policy = ...)] no Command!")
        return False
    elif response.status_code == 204:
        print("✅ Autorização OK: Empresa deletada")
        return True
    else:
        print(f"⚠️ Status inesperado: {response.status_code}")
        return False

if __name__ == "__main__":
    test_authorization_403()
```

**Checklist de Teste de Autorização:**

- [ ] Token JWT contém a permissão necessária (`permission` claim)
- [ ] Token JWT contém a role necessária (`role` claim)
- [ ] Endpoint usa policy-based authorization (`.RequireAuthorization(Policy)`)
- [ ] Command usa role-based authorization (`[Authorize(Roles = "...")]`)
- [ ] NÃO usar `[Authorize(Policy = ...)]` em Commands (causa erro 403!)
- [ ] Testar com usuário SEM permissão (deve retornar 403)
- [ ] Testar com usuário COM permissão (deve retornar sucesso)

---

### 3. Executar Baterias de Testes (Ordem Obrigatória)

**⚠️ ORDEM CRÍTICA:** Backend → Frontend → Outros (NUNCA outra ordem!)

**Estrutura de Baterias:**

Executamos **3 baterias de testes** sequenciais, uma para cada camada:

1. **Bateria de Testes Backend** - Testa TODOS os TCs em `Testes/Backend/`
2. **Bateria de Testes Frontend** - Testa TODOS os TCs em `Testes/Sistema/`
3. **Bateria de Outros Testes** - Testa TODOS os TCs em `Testes/Outros/`

**Regra de Ouro:** Cada bateria DEVE ter 100% de sucesso antes de prosseguir para a próxima. Não existe aprovação parcial.

**Processo de execução:**

```
┌──────────────────────────────────────────────────┐
│ BATERIA DE TESTES BACKEND                        │
├──────────────────────────────────────────────────┤
│ Camada: Testes/Backend/                          │
│ Para cada TC-*.md encontrado:                    │
│ 1. Verificar se robô existe                      │
│ 2. Se NÃO → Criar robô                           │
│ 3. Executar teste do TC                          │
│ 4. Capturar evidências (JSON)                    │
│ 5. Registrar resultado                           │
│                                                   │
│ Análise Final:                                   │
│ - Se 100% PASS → Prosseguir para Frontend       │
│ - Se <100% → Corrigir bugs e re-executar bateria│
│ - NUNCA prosseguir com menos de 100%            │
└──────────────────────────────────────────────────┘
         ↓ (SOMENTE se Backend = 100%)
┌──────────────────────────────────────────────────┐
│ BATERIA DE TESTES FRONTEND                       │
├──────────────────────────────────────────────────┤
│ Camada: Testes/Sistema/                          │
│ Para cada TC-*.md encontrado:                    │
│ 1. Verificar se robô existe                      │
│ 2. Se NÃO → Criar robô (Playwright)             │
│ 3. Executar teste E2E do TC                      │
│ 4. Capturar evidências (screenshots, logs)       │
│ 5. Registrar resultado                           │
│                                                   │
│ Análise Final:                                   │
│ - Se 100% PASS → Prosseguir para Outros         │
│ - Se <100% → Corrigir bugs e re-executar bateria│
│ - NUNCA prosseguir com menos de 100%            │
└──────────────────────────────────────────────────┘
         ↓ (SOMENTE se Frontend = 100%)
┌──────────────────────────────────────────────────┐
│ BATERIA DE OUTROS TESTES                         │
├──────────────────────────────────────────────────┤
│ Camada: Testes/Outros/                           │
│ Para cada TC-*.md encontrado:                    │
│ 1. Verificar se robô existe                      │
│ 2. Se NÃO → Criar robô (perf/seg)               │
│ 3. Executar teste do TC                          │
│ 4. Capturar evidências (relatórios)              │
│ 5. Registrar resultado                           │
│                                                   │
│ Análise Final:                                   │
│ - Se 100% PASS → APROVADO PARA PRODUÇÃO         │
│ - Se <100% → Corrigir bugs e re-executar bateria│
│ - NUNCA aprovar com menos de 100%               │
└──────────────────────────────────────────────────┘
         ↓ (SOMENTE se Outros = 100%)
┌──────────────────────────────────────────────────┐
│ GERAR RELATÓRIOS POR BATERIA                     │
├──────────────────────────────────────────────────┤
│ - RESUMO-BACKEND.md                              │
│ - RESUMO-FRONTEND.md                             │
│ - RESUMO-OUTROS.md                               │
│ - RESUMO-GERAL.md (consolidado)                  │
│ - relatorio_bateria_backend.json                 │
│ - relatorio_bateria_frontend.json                │
│ - relatorio_bateria_outros.json                  │
└──────────────────────────────────────────────────┘
```

**Por que esta ordem?**

1. **Bateria Backend primeiro:** Valida APIs isoladamente antes de testes E2E
   - Se Backend < 100% → INTERROMPER (não faz sentido testar frontend quebrado)
   - Feedback imediato para desenvolvedores
   - TCs localizados em `Testes/Backend/TC-*.md`

2. **Bateria Frontend em seguida:** Testa integração completa (UI + API)
   - Depende de Backend 100% funcional
   - Se Frontend < 100% → Corrigir e re-executar bateria
   - TCs localizados em `Testes/Sistema/TC-*.md`
   - Mais lento (renderização, navegação)

3. **Bateria Outros por último:** Performance, segurança, carga
   - Depende de Backend e Frontend funcionais
   - Se Outros < 100% → Corrigir e re-executar bateria
   - TCs localizados em `Testes/Outros/TC-*.md`
   - Testes especializados (OWASP ZAP, Locust, etc.)

**Documentação:**
- [MANUAL-DE-EXECUCAO.md](./MANUAL-DE-EXECUCAO.md) - Seção "Ordem de Execução Obrigatória"

---

### 4. Capturar Evidências

**Evidências obrigatórias para cada camada:**

#### Backend (API)
- ✅ Request JSON enviado
- ✅ Response JSON recebido
- ✅ Status code HTTP
- ✅ Headers
- ✅ Tempo de resposta

**Formato:** `evidencias/request-UC01-01.json`, `response-UC01-01.json`

#### Sistema (E2E)
- ✅ Screenshot OK (sucesso)
- ✅ Screenshot NOK (erro)
- ✅ Logs do navegador
- ✅ Network logs
- ✅ Vídeo da execução (opcional)

**Formato:** `evidencias/UC01-criar-usuario_OK.png`, `UC01-criar-usuario_NOK.png`

#### Outros (Perf/Seg)
- ✅ Relatório HTML de performance (Locust)
- ✅ Relatório HTML de segurança (ZAP)
- ✅ Métricas (tempo de resposta, throughput)

**Formato:** `evidencias/performance-UC01.html`, `security-UC01.html`

---

### 5. Gerar Relatórios por Bateria

**Após execução de todas as baterias (com 100% em cada):**

Criar relatórios individuais e consolidado:

#### RESUMO-BACKEND.md
```markdown
# Relatório - Bateria de Testes Backend - RF-XXX-NNN

**Data:** 2025-01-12
**Bateria:** Backend
**Camada:** Testes/Backend/
**Executado por:** Agente Tester

---

## Resumo da Bateria

| Métrica | Valor |
|---------|-------|
| Total de TCs | 5 |
| TCs OK | 5 |
| TCs NOK | 0 |
| % Sucesso | 100% |
| Status Final | ✅ APROVADO |

---

## Testes Executados

### ✅ TC-UC01-criar-usuario
- **Status:** PASS
- **Tempo:** 234ms
- **Evidências:** request-UC01-01.json, response-UC01-01.json

### ✅ TC-UC02-editar-usuario
- **Status:** PASS
- **Tempo:** 189ms
- **Evidências:** request-UC02-01.json, response-UC02-01.json

[... demais TCs ...]

---

## Conclusão

✅ Bateria de Testes Backend: 100% APROVADA
```

#### RESUMO-FRONTEND.md
```markdown
# Relatório - Bateria de Testes Frontend - RF-XXX-NNN

**Data:** 2025-01-12
**Bateria:** Frontend
**Camada:** Testes/Sistema/
**Executado por:** Agente Tester

---

## Resumo da Bateria

| Métrica | Valor |
|---------|-------|
| Total de TCs | 5 |
| TCs OK | 5 |
| TCs NOK | 0 |
| % Sucesso | 100% |
| Status Final | ✅ APROVADO |

---

## Testes Executados

### ✅ TC-UC01-criar-usuario
- **Status:** PASS
- **Tempo:** 3.2s
- **Evidências:** UC01-criar-usuario_OK.png

### ✅ TC-UC02-editar-usuario
- **Status:** PASS
- **Tempo:** 2.8s
- **Evidências:** UC02-editar-usuario_OK.png

[... demais TCs ...]

---

## Conclusão

✅ Bateria de Testes Frontend: 100% APROVADA
```

#### RESUMO-OUTROS.md
```markdown
# Relatório - Bateria de Outros Testes - RF-XXX-NNN

**Data:** 2025-01-12
**Bateria:** Outros
**Camada:** Testes/Outros/
**Executado por:** Agente Tester

---

## Resumo da Bateria

| Métrica | Valor |
|---------|-------|
| Total de TCs | 3 |
| TCs OK | 3 |
| TCs NOK | 0 |
| % Sucesso | 100% |
| Status Final | ✅ APROVADO |

---

## Testes Executados

### ✅ TC-PERF-listar-usuarios
- **Status:** PASS
- **Tempo médio:** 145ms
- **Evidências:** performance-listar.html

### ✅ TC-SEG-sql-injection
- **Status:** PASS
- **Vulnerabilidades:** 0
- **Evidências:** security-report.html

[... demais TCs ...]

---

## Conclusão

✅ Bateria de Outros Testes: 100% APROVADA
```

#### RESUMO-GERAL.md (Consolidado)
```markdown
# Relatório Consolidado de Testes - RF-XXX-NNN

**Data:** 2025-01-12
**Executado por:** Agente Tester
**Ambiente:** Desenvolvimento

---

## Resumo Geral das Baterias

| Bateria | Total TCs | OK | NOK | % Sucesso | Status |
|---------|-----------|----|----|-----------|---------|
| **Backend** | 5 | 5 | 0 | 100% | ✅ APROVADO |
| **Frontend** | 5 | 5 | 0 | 100% | ✅ APROVADO |
| **Outros** | 3 | 3 | 0 | 100% | ✅ APROVADO |
| **TOTAL** | **13** | **13** | **0** | **100%** | ✅ **APROVADO** |

---

## Detalhamento por Bateria

### 📋 Bateria de Testes Backend
- ✅ 100% de sucesso (5/5 TCs)
- 📁 Evidências: relatorio_bateria_backend.json
- 📝 Detalhes: RESUMO-BACKEND.md

### 📋 Bateria de Testes Frontend
- ✅ 100% de sucesso (5/5 TCs)
- 📁 Evidências: relatorio_bateria_frontend.json
- 📝 Detalhes: RESUMO-FRONTEND.md

### 📋 Bateria de Outros Testes
- ✅ 100% de sucesso (3/3 TCs)
- 📁 Evidências: relatorio_bateria_outros.json
- 📝 Detalhes: RESUMO-OUTROS.md

---

## Conclusão Final

✅ **RF-XXX-NNN APROVADO PARA PRODUÇÃO**

- Todas as 3 baterias atingiram 100% de sucesso
- 13 TCs executados com sucesso
- 0 bugs encontrados
- Sistema validado e pronto para deploy
```

---

## ✅ Checklist de Testes

Antes de considerar testes completos:

### Documentação
- [ ] CNs criados para todos os UCs
- [ ] TCs criados para todos os UCs
- [ ] MTs (massa de teste) criadas
- [ ] Documentação em 3 camadas (quando aplicável)

### Robôs
- [ ] Robô Backend criado (robo-testes-rf-XXX-backend.py)
- [ ] Robô Frontend criado (robo-testes-rf-XXX-frontend.py)
- [ ] Robô Outros criado (robo-testes-rf-XXX-outros.py)
- [ ] Todos os robôs testados individualmente

### Execução de Baterias
- [ ] **Bateria Backend** executada primeiro
  - [ ] 100% de sucesso em TODOS os TCs de Testes/Backend/
  - [ ] relatorio_bateria_backend.json gerado
- [ ] **Bateria Frontend** executada em seguida
  - [ ] 100% de sucesso em TODOS os TCs de Testes/Sistema/
  - [ ] relatorio_bateria_frontend.json gerado
- [ ] **Bateria Outros** executada por último
  - [ ] 100% de sucesso em TODOS os TCs de Testes/Outros/
  - [ ] relatorio_bateria_outros.json gerado
- [ ] Ordem obrigatória respeitada (Backend → Frontend → Outros)

### Evidências
- [ ] Screenshots OK capturados (Frontend)
- [ ] Screenshots NOK capturados (se houver bugs)
- [ ] Logs de API salvos (Backend)
- [ ] Relatórios de performance/segurança gerados (Outros)
- [ ] Evidências organizadas por bateria

### Relatórios
- [ ] RESUMO-BACKEND.md criado
- [ ] RESUMO-FRONTEND.md criado
- [ ] RESUMO-OUTROS.md criado
- [ ] RESUMO-GERAL.md consolidado criado
- [ ] Bugs documentados (se houver)
- [ ] 100% de sucesso em TODAS as 3 baterias

---

## 🚨 Erros Comuns a Evitar

### ❌ ERRO #1: Executar baterias em ordem errada

**Ordem errada:**
```
Bateria Frontend → Bateria Backend → Bateria Outros  ❌
Bateria Outros → Bateria Backend → Bateria Frontend  ❌
```

**Ordem correta:**
```
Bateria Backend → Bateria Frontend → Bateria Outros  ✅
```

**Por quê?** Backend deve estar 100% antes de testar Frontend (E2E depende de APIs funcionais).

---

### ❌ ERRO #2: Prosseguir com menos de 100% na bateria

**Errado:**
```
Bateria Backend: 8/10 TCs OK (80%) → Prosseguir para Frontend  ❌
```

**Correto:**
```
Bateria Backend: 8/10 TCs OK (80%) → Corrigir bugs → Re-executar bateria
Bateria Backend: 10/10 TCs OK (100%) → Prosseguir para Frontend  ✅
```

**Regra de Ouro:** Só prossegue para próxima bateria com 100% na atual.

---

### ❌ ERRO #3: Não testar TODOS os TCs da camada

**Errado:**
```python
# Testes/Backend/ tem 10 TCs, mas robô testa só 5
def test_backend():
    test_tc01()
    test_tc02()
    test_tc03()
    test_tc04()
    test_tc05()
    # Faltam TC06-TC10!  ❌
```

**Correto:**
```python
# Descobrir TODOS os TCs dinamicamente
def test_backend():
    tcs = glob.glob("Testes/Backend/TC-*.md")  # Descobre todos
    for tc_file in tcs:
        test_tc(tc_file)  ✅ Testa TODOS os TCs!
```

---

### ❌ ERRO #4: Usar nomenclatura errada

**Nomenclatura errada:**
```
CN-API-UC01-criar-usuario.md  ❌
TC-SISTEMA-UC01.md            ❌
relatorio_bateria1.json       ❌
```

**Nomenclatura correta:**
```
CN-UC01-criar-usuario.md          ✅ (em Backend/)
CN-UC01-criar-usuario.md          ✅ (em Sistema/)
relatorio_bateria_backend.json    ✅
relatorio_bateria_frontend.json   ✅
```

---

### ❌ ERRO #5: Não capturar evidências NOK

**Errado:**
```python
# Teste falhou, mas não capturou evidência
assert response.status_code == 200  # Falha aqui, sem screenshot  ❌
```

**Correto:**
```python
try:
    assert response.status_code == 200
    page.screenshot(path="UC01_OK.png")  ✅
except AssertionError:
    page.screenshot(path="UC01_NOK.png")  ✅ Captura NOK!
    raise
```

---

## 📚 Documentos Relacionados

- **[REGRAS-CRITICAS.md](./REGRAS-CRITICAS.md)** - Regras para todos os agentes
- **[MANUAL-DE-EXECUCAO.md](./MANUAL-DE-EXECUCAO.md)** - Processo completo de execução
- **[MANUAL-DE-DOCUMENTACAO.md](./MANUAL-DE-DOCUMENTACAO.md)** - Estrutura e templates
- **[GUIA-ARCHITECT.md](./GUIA-ARCHITECT.md)** - Para entender RFs e UCs
- **[GUIA-DEVELOPER.md](./GUIA-DEVELOPER.md)** - Para entender implementação

---

**ÚLTIMA ATUALIZAÇÃO:** 2025-01-12
**VERSÃO:** 1.0
