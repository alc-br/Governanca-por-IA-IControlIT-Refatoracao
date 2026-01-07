# UC-RF052 — Casos de Uso Canônicos

**RF:** RF052 — Gestão de Consumidores  
**Fase:** Fase 2 - Cadastros e Serviços Transversais  
**Epic:** EPIC003-CAD-Cadastros-Base  
**Versão:** 2.0  
**Data:** 2025-12-31  
**Autor:** Agência ALC - alc.dev.br  

---

## 1. OBJETIVO DO DOCUMENTO

Este documento descreve todos os Casos de Uso (UC) derivados do RF052, cobrindo integralmente o comportamento funcional esperado do sistema de gestão de consumidores.

Os UCs aqui definidos servem como contrato comportamental, sendo a fonte primária para geração de Casos de Teste, Massas de Teste, Evidências de auditoria e Execução por agentes de IA.

---

## 2. SUMÁRIO DE CASOS DE USO

| ID | Nome | Ator Principal |
|----|------|----------------|
| UC00 | Listar Consumidores | Usuário Autenticado |
| UC01 | Criar Consumidor | RH/Admin |
| UC02 | Visualizar Consumidor | Usuário Autenticado |
| UC03 | Editar Consumidor | RH/Admin |
| UC04 | Inativar Consumidor | Admin |

---

## 3. PADRÕES GERAIS APLICÁVEIS A TODOS OS UCs

- Todos os acessos respeitam isolamento por tenant (ClienteId)
- Todas as ações exigem permissão explícita (RBAC)
- Auditoria registra quem, quando e qual ação
- Histórico de 7 anos preservado (LGPD)

---

## CHANGELOG

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 2.0 | 2025-12-31 | Agência ALC - alc.dev.br | Versão canônica v2.0 |
