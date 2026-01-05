# Mapeamento: Código Legado → RFs Modernos

Este documento mapeia componentes do sistema legado (`D:\IC2\ic1_legado\`) para os Requisitos Funcionais modernos.

## Regra

**Seção 3 do RF:** Toda referência ao legado DEVE estar documentada na Seção 3 "REFERENCIAS AO LEGADO" do RF correspondente.

## Mapeamento por Tipo

### Tabelas do Banco de Dados

| Tabela Legada | RFs que Usam | Status | Observações |
|---------------|--------------|--------|-------------|
| Usuario_Global | RF-007, RF-012, RF-014 | Migrado | Usuario_Global → Usuario (com ClienteId) |
| Departamento | RF-027 | Migrado | Adicionar ClienteId + auditoria |
| Centro_Custo | RF-014 | Migrado | Adicionar multi-tenancy |

### Stored Procedures

| SP Legado | RF Equivalente | Status | Observações |
|-----------|----------------|--------|-------------|
| sp_Usuario_Listar | RF-012 UC00 | Substituído | Agora é GetUsuariosQuery |
| sp_Departamento_Inserir | RF-027 UC01 | Substituído | Agora é CreateDepartamentoCommand |

### Páginas ASPX

| Página Legada | RF Equivalente | Status | Observações |
|---------------|----------------|--------|-------------|
| Usuarios.aspx | RF-012 | Modernizado | Agora é /admin/usuarios (Angular) |
| Departamentos.aspx | RF-027 | Modernizado | Agora é /admin/management/departamentos |

### WebServices (.asmx)

| WebService Legado | RF Equivalente | Status | Observações |
|-------------------|----------------|--------|-------------|
| UsuarioService.asmx | RF-012 | Substituído | Agora é API REST /api/usuarios |

---

## Script de Validação

Script: `tools/validate-legacy-mapping.py`

Valida se referências ao legado foram documentadas corretamente.

---

## Versionamento

- **Criado em:** 2025-12-28
- **Última atualização:** 2025-12-28
- **Versão:** 1.0.0
