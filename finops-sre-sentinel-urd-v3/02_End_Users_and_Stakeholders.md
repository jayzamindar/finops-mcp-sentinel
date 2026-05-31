# 02 - End Users & Stakeholders

**Document:** finops-sre-sentinel URD v3.0  
**Section:** End Users & Stakeholders  
**Target Audience:** Product Owners, UX Designers  
**Approx Tokens:** ~2,500

## 2.1 Primary End Users

### 2.1.1 On-Call SRE Engineers

**Role:** Primary operators of the system during incident response  
**Profile:** Senior engineers with 5+ years experience in distributed systems  
**Access Level:** Full tool access with human-in-the-loop for destructive actions

**Responsibilities:**
- Monitor dashboards for alerts
- Receive AI-generated incident analysis
- Approve/reject automated remediation actions
- Escalate to senior engineers when needed
- Conduct post-incident reviews

**Pain Points Addressed:**
- Alert fatigue from noisy monitoring systems
- Time-consuming manual log analysis across multiple tools
- Uncertainty about safe remediation actions
- Documentation burden during incidents

**Success Criteria for This User:**
- Can diagnose a payment latency issue in under 5 minutes
- Receives clear, explainable AI recommendations with source citations
- Has full audit trail of every AI decision for post-mortem

### 2.1.2 FinOps Analysts

**Role:** Cloud cost governance and optimization  
**Profile:** Finance/engineering hybrid role focused on cloud ROI  
**Access Level:** Read-only SRE tools, full cost governance tools

**Responsibilities:**
- Monitor cloud spend dashboards
- Review AI-flagged cost anomalies
- Approve cost optimization actions
- Generate monthly cost reports for leadership
- Track FinOps KPIs and SLAs

**Pain Points Addressed:**
- Difficulty correlating Kubernetes costs with business events
- Delayed detection of cost anomalies (often discovered in monthly bills)
- Lack of automated root cause analysis for spend spikes
- No visibility into AI token costs or wasted compute

**Success Criteria for This User:**
- Receives real-time alerts when cloud spend deviates by >20%
- Can see per-incident cost attribution
- Has automated monthly cost report generation
- Views AI token burn rate in real-time dashboard

### 2.1.3 Compliance Officers

**Role:** Regulatory compliance and audit readiness  
**Profile:** Non-technical background with deep regulatory expertise  
**Access Level:** Audit trail read-only, compliance dashboard

**Responsibilities:**
- Review compliance drift alerts
- Audit AI decision rationale
- Generate compliance reports for regulators
- Define and update compliance rules
- Conduct periodic compliance reviews

**Pain Points Addressed:**
- Manual, time-consuming audit trail gathering
- Difficulty proving AI decision fairness/non-bias
- Reactive rather than proactive compliance posture
- No automated drift detection between GitOps and live state

**Success Criteria for This User:**
- One-click export of entire AI session for SOC 2 / PCI DSS auditors
- Real-time compliance score dashboard
- Automated drift detection with remediation steps
- Immutable audit logs with cryptographic verification

## 2.2 Secondary Stakeholders

### 2.2.1 Engineering Managers

**Role:** Team productivity and reliability oversight  
**Access Level:** Read-only dashboards and reports

**Needs:**
- Reliability metrics (SLOs, error budgets)
- Incident history and trends
- On-call burden metrics (pages per night, MTTR)
- Cost-per-feature attribution

### 2.2.2 CTO / VP of Engineering

**Role:** Strategic oversight  
**Access Level:** Executive dashboards, quarterly reports

**Needs:**
- System availability status
- Cost trends and forecasts
- Regulatory compliance status
- Engineering efficiency metrics
- Risk assessment for AI-driven automation

### 2.2.3 Security Team

**Role:** Platform security oversight  
**Access Level:** Security audit logs, RBAC configuration

**Needs:**
- RBAC audit capabilities
- PII redaction verification
- Threat detection integration
- Security incident response
- Prompt injection protection validation

## 2.3 User Personas

| Persona | Name | Role | Goals | Frustrations |
|---------|------|------|-------|--------------|
| **The Veteran SRE** | Marcus Chen | Staff SRE @ Payments Co | Fix incidents fast, go home on time | Noisy alerts, unclear remediation steps |
| **The FinOps Champion** | Sarah Okonkwo | FinOps Lead @ Trading App | Optimize cloud spend, prove ROI | Bills that don't match usage patterns |
| **The Compliance Guardian** | Elena Vasquez | Compliance Officer @ Lending Platform | Stay audit-ready 24/7 | Scrambling for audit data before exams |
| **The Reluctant Manager** | James Park | Engineering Manager @ Banking API | Keep team healthy, systems running | On-call burnout, unclear SLA metrics |

## 2.4 Access Control Matrix

| Role | diagnose | analyze_spend | remediate | verify_compliance | Audit Logs | User Mgmt |
|------|----------|---------------|-----------|-------------------|------------|-----------|
| **admin** | ✅ Execute | ✅ Execute | ✅ Full | ✅ | ✅ | ✅ |
| **senior_sre** | ✅ Execute | ✅ Execute | ✅ (risk 1-7) | ✅ | ✅ Read | ❌ |
| **sre** | ✅ Execute | ✅ Execute | ✅ (risk 1-4) | ✅ | ❌ | ❌ |
| **finops** | ❌ | ✅ Execute | ❌ | ✅ Read | ✅ Read | ❌ |
| **compliance** | ❌ | ❌ | ❌ | ✅ Full | ✅ Full | ❌ |
| **viewer** | ✅ Read | ✅ Read | ❌ | ✅ Read | ❌ | ❌ |

## 2.5 User Onboarding Flow

```
New User
    │
    ▼
1. Runs setup.ps1 (one-click install)
    │
    ▼
2. Opens browser to http://localhost:3001 (UI)
    │
    ▼
3. Authenticates via API Key (X-API-Key header)
    │
    ▼
4. Sees role-based dashboard
    │
    ▼
5. Starts using tools relevant to their role
```

*This section defines who will be using the system and their needs. For functional requirements, proceed to Section 03.*