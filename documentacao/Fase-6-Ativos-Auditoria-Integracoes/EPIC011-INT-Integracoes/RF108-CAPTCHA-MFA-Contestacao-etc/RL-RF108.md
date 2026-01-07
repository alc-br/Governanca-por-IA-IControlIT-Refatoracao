# RL-RF108 — Referência ao Legado (CAPTCHA, MFA, Contestação e Segurança)

**Versão:** 1.0
**Data:** 2025-12-31
**Autor:** Claude Code

**RF Moderno Relacionado:** RF108 - CAPTCHA, MFA, Contestação e Segurança Avançada
**Sistema Legado:** IControlIT VB.NET / ASP.NET Web Forms
**Objetivo:** Documentar o comportamento do legado relacionado a segurança, CAPTCHA e contestações.

---

## 1. CONTEXTO DO LEGADO

- **Arquitetura:** Monolítica ASP.NET Web Forms + VB.NET
- **CAPTCHA:** reCAPTCHA v2 (checkbox visível)
- **MFA:** Apenas SMS manual (sem TOTP)
- **Rate Limiting:** Não implementado
- **Device Fingerprinting:** Não existia
- **UEBA:** Logs manuais sem análise automatizada
- **Contestação:** Formulário simples sem workflow

### Problemas Arquiteturais
1. CAPTCHA v2 é intrusivo (checkbox)
2. MFA apenas por SMS (custo alto)
3. Sem proteção contra DDoS
4. Sem device fingerprinting
5. Sem análise comportamental automatizada

---

## 2. TELAS DO LEGADO

### login.aspx
- **Caminho:** `ic1_legado/IControlIT/login.aspx`
- **Responsabilidade:** Login com reCAPTCHA v2
- **DESTINO:** SUBSTITUÍDO (Angular `/auth/login` com reCAPTCHA v3)

### contestacao.aspx  
- **Caminho:** `ic1_legado/IControlIT/contestacao.aspx`
- **Responsabilidade:** Contestação de fatura
- **DESTINO:** SUBSTITUÍDO (Angular `/contestacoes` com workflow)

### ip-bloqueados.aspx
- **Caminho:** `ic1_legado/IControlIT/ip-bloqueados.aspx`
- **Responsabilidade:** Gestão manual de IPs
- **DESTINO:** SUBSTITUÍDO (Angular `/seguranca/ips-bloqueados`)

---

## 3. WEBSERVICES

### WSSeguranca.asmx.vb
- **Caminho:** `ic1_legado/WebService/WSSeguranca.asmx.vb`
- **Métodos:** ValidarCaptcha, GerarCodigoMfa, ListarIpsBloqueados
- **DESTINO:** SUBSTITUÍDO (REST API `/api/seguranca`)

---

## 4. STORED PROCEDURES

### pa_USER_LOGIN
- Autentica usuário (sem MFA)
- **DESTINO:** SUBSTITUÍDO (AuthenticationService com MFA)

### pa_AUDIT_LOG_INSERT
- Registra auditoria manual
- **DESTINO:** SUBSTITUÍDO (AuditRepository automático)

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|--------|------|-----------|-------|
| 1.0 | 2025-12-31 | RL-RF108 criado | Claude Code |
