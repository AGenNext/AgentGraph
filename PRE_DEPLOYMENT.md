# Enterprise SaaS Production Hardening Checklist

---

## 1. Authentication & Authorization

### Identity Management
- [ ] WaltID integration configured
- [ ] Verified credentials (VC) issued
- [ ] DID (Decentralized Identifier) registry set up
- [ ] Multi-factor authentication (MFA) enabled
- [ ] SSO / SAML configured
- [ ] OAuth 2.0 / OIDC provider configured

### Password & Session
- [ ] Password policy enforced (12+ chars, complexity)
- [ ] Account lockout after 5 failed attempts
- [ ] Session timeout: 15 minutes idle
- [ ] Secure HTTP-only cookies
- [ ] CSRF tokens implemented

---

## 2. Data Protection

### Encryption
- [ ] TLS 1.3 required
- [ ] Certificate pinning enabled
- [ ] Data at rest encrypted (AES-256)
- [ ] Database encryption enabled
- [ ] Backup encryption enabled

### Keys & Secrets
- [ ] Secrets manager (Vault/AWS Secrets)
- [ ] API keys rotated every 90 days
- [ ] Private keys in HSM
- [ ] No secrets in code
- [ ] Environment variables encrypted

---

## 3. API Security

### Endpoints
- [ ] Rate limiting: 100 req/min
- [ ] Request validation (schema)
- [ ] Input sanitization
- [ ] Output encoding
- [ ] SQL injection prevention
- [ ] XSS protection headers

### Headers
- [ ] Strict-Transport-Security
- [ ] Content-Security-Policy
- [ ] X-Content-Type-Options: nosniff
- [ ] X-Frame-Options: DENY
- [ ] X-XSS-Protection: 1
- [ ] Referrer-Policy: strict-origin

---

## 4. Infrastructure

### Container Security
- [ ] Non-root user in Docker
- [ ] Read-only filesystem
- [ ] No privileged containers
- [ ] Image signing (Cosign)
- [ ] Vulnerability scanning
- [ ] Minimal base image

### Network
- [ ] Firewall rules
- [ ] VPN for internal
- [ ] Network segmentation
- [ ] WAF configured
- [ ] DDoS protection
- [ ] Private subnets only

---

## 5. Database Security

### PostgreSQL
- [ ] SSL required
- [ ] Row-level security
- [ ] Column-level encryption
- [ ] Audit logging
- [ ] Connection pooling
- [ ] Query allowlist

### Redis
- [ ] ACL enabled
- [ ] Password required
- [ ] TLS enabled
- [ ] Max memory policy
- [ ] Persistence encrypted

---

## 6. Monitoring & Logging

### Observability
- [ ] Distributed tracing
- [ ] Metrics (Prometheus)
- [ ] Logs (structured JSON)
- [ ] Health endpoints
- [ ] Readiness probes
- [ ] Liveness probes

### Alerting
- [ ] PagerDuty / OpsGenie
- [ ] Anomaly detection
- [ ] Alert on 5xx errors
- [ ] Alert on latency spike
- [ ] Alert on memory/CPU
- [ ] Backup failure alert

---

## 7. Secrets Management

### OPA (Open Policy Agent)
- [ ] Policy bundled
- [ ] Base policies defined
- [ ] Role policies defined
- [ ] Resource policies defined
- [ ] Audit logging
- [ ] Decision logging

### Key Management
- [ ] Key rotation schedule
- [ ] Key recovery process
- [ ] Key escrow
- [ ] HSM integration
- [ ] Key ceremony documented

---

## 8. Compliance

### Data Privacy
- [ ] GDPR compliance
- [ ] Data retention policy
- [ ] Right to delete
- [ ] Data portability
- [ ] Consent management

### Auditing
- [ ] Audit trail enabled
- [ ] Log retention 1 year
- [ ] Immutable logs
- [ ] Quarterly reviews
- [ ] Annual penetration test

---

## 9. Backup & Recovery

### Backup
- [ ] Daily automated backups
- [ ] Cross-region replication
- [ ] Backup encryption
- [ ] Backup testing
- [ ] Backup retention 30 days

### Recovery
- [ ] RTO < 4 hours
- [ ] RPO < 1 hour
- [ ] Runbook documented
- [ ] Recovery tested quarterly
- [ ] Failover tested

---

## 10. Incident Response

### Process
- [ ] IR plan documented
- [ ] Contact list updated
- [ ] Escalation path defined
- [ ] Forensic procedures
- [ ] Post-incident review

### Tools
- [ ] SIEM integration
- [ ] Threat intelligence
- [ ] Automated blocking
- [ ] Auto-healing
- [ ] Canary deployments

---

# Marketing Website Hardening Checklist

---

## 1. Production Readiness

### Build
- [ ] `npm run build` succeeds
- [ ] No TypeScript errors
- [ ] No ESLint errors
- [ ] Bundle size < 200KB gzipped
- [ ] Tree shaking enabled

### Deploy
- [ ] Static export configured
- [ ] CDN configured
- [ ] Cache headers set
- [ ] Gzip/Brotli enabled
- [ ] Asset versioning

---

## 2. Security Headers

### HTTP Security
- [ ] Content-Security-Policy
- [ ] X-Frame-Options: DENY
- [ ] X-Content-Type-Options
- [ ] Referrer-Policy
- [ ] Permissions-Policy

### CORS
- [ ] Allowlisted origins
- [ ] Credentials: false
- [ ] Safe methods only
- [ ] Max-age set

---

## 3. Performance

### Core Web Vitals
- [ ] LCP < 2.5s
- [ ] FID < 100ms
- [ ] CLS < 0.1
- [ ] FCP < 1.8s
- [ ] TTI < 3.8s

### Optimization
- [ ] Images optimized
- [ ] Fonts preloaded
- [ ] Critical CSS inlined
- [ ] Lazy loading
- [ ] Code splitting

---

## 4. SEO

### Meta Tags
- [ ] Title tag
- [ ] Meta description
- [ ] Canonical URL
- [ ] Open Graph tags
- [ ] Twitter Card tags

### Content
- [ ] Semantic HTML
- [ ] Heading hierarchy
- [ ] Alt text on images
- [ ] Sitemap.xml
- [ ] robots.txt

---

## 5. Accessibility

### WCAG 2.1 AA
- [ ] Color contrast 4.5:1
- [ ] Focus indicators
- [ ] Keyboard navigation
- [ ] ARIA labels
- [ ] Skip links

### Testing
- [ ] Lighthouse > 90
- [ ] Screen reader tested
- [ ] VoiceOver tested
- [ ] NVDA tested
- [ ] axe-core passed

---

## 6. Analytics

### Tracking
- [ ] Google Analytics 4
- [ ] Event tracking
- [ ] Conversion tracking
- [ ] Custom events
- [ ] User properties

### Privacy
- [ ] Cookie consent
- [ ] Privacy policy
- [ ] GDPR banner
- [ ] Data processing agreement
- [ ] IP anonymization

---

## 7. Forms

### Contact Form
- [ ] Client validation
- [ ] Server validation
- [ ] Honeypot field
- [ ] Rate limiting
- [ ] CSRF protection

### Email
- [ ] SPF/DKIM/DMARC
- [ ] Unsubscribe link
- [ ] Plain text version
- [ ] Reply-To header

---

## 8. CDN & Cache

### Caching
- [ ] Static assets: 1 year
- [ ] HTML: no cache
- [ ] API: no cache
- [ ] Fonts: 1 year
- [ ] Images: 1 year

### CDN
- [ ] CloudFlare / Fastly
- [ ] SSL enabled
- [ ] Minification
- [ ] Image optimization
- [ ] Geo-blocking

---

## 9. Domain & DNS

### DNS
- [ ] DNSSEC enabled
- [ ] CAA records
- [ ] TTL: 300s
- [ ] Multi-region
- [ ] ALIAS record

### Domain
- [ ] WHOIS privacy
- [ ] Auto-renewal
- [ ] Registrar lock
- [ ] Transfer lock

---

## 10. Monitoring

### Uptime
- [ ] Pingdom / UptimeRobot
- [ ] 1-minute interval
- [ ] 3 check locations
- [ ] SSL monitoring
- [ ] Domain monitoring

### Performance
- [ ] Real user monitoring
- [ ] Synthetic monitoring
- [ ] Page speed tracking
- [ ] Error tracking
- [ ] Custom dashboards

---

## 11. Compliance

### Legal
- [ ] Privacy policy
- [ ] Terms of service
- [ ] Cookie policy
- [ ] Impressum
- [ ] Accessibility statement

### Security
- [ ] Security.txt
- [ ] robots.txt
- [ ] Humans.txt
- [ ] Open source licenses
- [ ] Third-party audits

---

## 12. Deployment

### CI/CD
- [ ] GitHub Actions
- [ ] Branch protection
- [ ] Required reviews
- [ ] Auto deployments
- [ ] Rollback procedure

### Environment
- [ ] Production branch
- [ ] Staging branch
- [ ] Environment variables
- [ ] Feature flags
- [ ] Canary deploy

---

# Quick Start Commands

```bash
# Build website
cd nextjs-website
npm install
npm run build

# Test locally
npm run start
# Visit: http://localhost:3000

# Deploy to GitHub Pages
# Settings → Pages → Deploy from main branch

# Security check
npm audit
npm audit --fix
```

---

# Sign-Off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| DevOps | | | |
| Security | | | |
| Product | | | |
| Compliance | | | |

---

Last Updated: 2024-05-12