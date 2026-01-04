# RF-XXX: [Nome do Requisito Funcional]

**Versão**: 2.0  
**Data**: YYYY-MM-DD  
**Autor**: Agência ALC - alc.dev.br  
**EPIC**: [EPIC-ID] - [Nome da EPIC]  
**Fase**: [Fase X - Nome da Fase]

---

## 1. OBJETIVO DO REQUISITO

Descrever de forma clara, objetiva e verificável o comportamento esperado do requisito funcional **RF-XXX**, servindo como **contrato oficial** entre negócio, desenvolvimento, testes e agentes de IA.

Este documento **não define implementação**, apenas **o que o sistema deve fazer**, sob quais condições e quais garantias devem ser preservadas.

---

## 2. ESCOPO

### 2.1 O que está dentro do escopo

- [ ] Criação de [entidade]
- [ ] Atualização de [entidade]
- [ ] Listagem de [entidade]
- [ ] Exclusão lógica (se aplicável)
- [ ] Validações funcionais e regras de negócio
- [ ] Controle de acesso e isolamento por tenant
- [ ] Auditoria de operações

### 2.2 Fora do escopo (não objetivos)

- Interface visual específica
- Tecnologia, framework ou linguagem
- Layout, UX ou identidade visual
- Estratégia de deploy ou infraestrutura

---

## 3. CONCEITOS E DEFINIÇÕES

| Termo | Definição |
|-----|---------|
| Entidade | Objeto principal manipulado por este RF |
| Tenant | Unidade lógica de isolamento de dados |
| Usuário | Agente autenticado que executa ações |
| Operação | Ação executável sobre a entidade |

---

## 4. FUNCIONALIDADES COBERTAS

1. Criar entidade
2. Atualizar entidade existente
3. Consultar entidade por ID
4. Listar entidades
5. Excluir entidade (se permitido)

---

## 5. REGRAS DE NEGÓCIO

### RN-RFXXX-01 — Campos obrigatórios

**Descrição**: Campos definidos como obrigatórios devem estar presentes e válidos.

**Justificativa**: Garantir integridade mínima dos dados.

**Critério de Aceite**:
- Campo ausente → rejeição
- Campo vazio ou inválido → rejeição

---

### RN-RFXXX-02 — Isolamento por tenant

**Descrição**: Um usuário só pode acessar dados do seu próprio tenant.

**Critério de Aceite**:
- Tentativa de acesso cruzado → não permitido

---

### RN-RFXXX-03 — Permissões

**Descrição**: Cada operação exige permissão explícita.

| Operação | Permissão |
|-------|---------|
| Criar | entidade.create |
| Atualizar | entidade.update |
| Visualizar | entidade.view |
| Listar | entidade.view_any |
| Excluir | entidade.delete |

---

## 6. ESTADOS DA ENTIDADE

| Estado | Descrição |
|------|-----------|
| draft | Criado, não final |
| active | Ativo |
| inactive | Inativo |
| deleted | Excluído logicamente |

### Transições permitidas

| De | Para |
|---|---|
| draft | active |
| active | inactive |
| inactive | active |

---

## 7. EVENTOS DE DOMÍNIO

| Evento | Quando ocorre |
|------|--------------|
| entidade.criada | Após criação |
| entidade.atualizada | Após atualização |
| entidade.excluida | Após exclusão |

---

## 8. CRITÉRIOS GLOBAIS DE ACEITE

- Nenhuma operação pode violar isolamento de tenant
- Nenhuma regra de negócio pode ser ignorada
- Erros devem ser previsíveis e rastreáveis
- Auditoria deve registrar quem, quando e o que mudou

---

## 9. SEGURANÇA

- Validação de entrada obrigatória
- Proteção contra injeção
- Controle de permissões
- Isolamento multi-tenant

---

## 10. ARTEFATOS DERIVADOS

Este RF é base para:

- UC-RFXXX.md (Casos de Uso)
- MT-RFXXX.yaml (Massas de Teste)
- TC-RFXXX.yaml (Casos de Teste)

---

## 11. RASTREABILIDADE

| Artefato | Gerado |
|--------|-------|
| Casos de Uso | Obrigatório |
| Massas de Teste | Obrigatório |
| Casos de Teste | Obrigatório |

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|------|------|----------|------|
| 2.0 | YYYY-MM-DD | Versão canônica orientada a contrato | Agência ALC - alc.dev.br |