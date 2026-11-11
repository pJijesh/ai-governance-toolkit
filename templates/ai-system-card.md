# AI system documentation card

> General information only, not legal advice. Fernhill Building Supplies Ltd is a fictional company and every example in this file is invented.

Supports controls TK-LIF-01 to TK-LIF-08 (requirements, testing, bias, security, deployment approval, monitoring, logging, documentation), TK-INV-04 (resource documentation), TK-INV-05 (retirement), TK-DAT-01 and TK-DAT-02 (data), TK-USE-02 (disclosure), TK-INC-03 (post-market monitoring) and TK-RSK-07 (change management). Related framework items: ISO/IEC 42001 A.6.2.3, A.6.2.7 and A.4.2, EU AI Act Art 11 and Art 13, NIST AI RMF MAP 2.2 and MEASURE 2.9.

## Purpose

A system card is a short, plain-language record of what a system is for, how it was built or bought, how it was tested, what it cannot do, and how it is watched in use. It is shorter than the technical documentation that Art 11 and Annex IV of the Act require from providers of high-risk systems. Providers of such systems need the full technical file. For everyone else the card is a practical minimum, and it is useful to deployers who need to brief reviewers and auditors.

This card is also the place where most lifecycle controls leave their evidence, so keep it current.

## How to use it

1. Create a card when a system enters the inventory at the `proposed` stage, and fill it in as facts become known.
2. Mark unknown items as "Unknown" with a date to find out. Do not leave them blank. Unknowns are risks.
3. Ask the supplier for the supplier-owned sections where you bought the system.
4. Review the card at each release, each material change and at least annually.
5. Keep a change log at the bottom.

## Template

### 1. Identification

| Field | Entry |
|---|---|
| System ID | |
| Name and version | |
| Card version and date | |
| System owner (role) | |
| Supplier / builder | |
| Our role under the EU AI Act | |
| Risk tier and annex area | |

### 2. Intended use and limits

- Intended purpose:
- Intended users:
- People affected:
- Out of scope uses (what it must not be used for):
- Known limitations:
- Conditions where it performs poorly:

### 3. How it works (plain language)

- Type of system (for example classification model, ranking model, language model with retrieval):
- Main inputs and outputs:
- Third-party models or components used:
- Human role in the process:

### 4. Data

| Item | Entry |
|---|---|
| Training or reference data and source | |
| Rights to use the data | |
| Personal or special category data | |
| Known gaps or biases in the data | |
| Data quality checks | |
| Retention of inputs and outputs | |

### 5. Testing and performance

| Item | Entry |
|---|---|
| Test approach and date | |
| Metrics and results | |
| Testing on groups affected by the system | |
| Security and misuse testing | |
| Acceptance threshold and who approved | |

### 6. Infrastructure and resources

- Hosting and location:
- Tooling and dependencies:
- Compute and cost notes:
- Skills needed to run it:

### 7. Transparency

- What users are told, and where:
- How content or interactions are marked as AI-generated, if required:
- Where instructions for use are kept:

### 8. Operation and monitoring

| Item | Entry |
|---|---|
| Metrics monitored in use | |
| Thresholds that trigger action | |
| Review frequency | |
| Logs kept and retention period | |
| Incident route | |
| Fallback if switched off | |

### 9. Change and retirement

- Changes that need a new assessment (for example new data, new purpose, new model version):
- Retirement criteria:
- Retirement steps (access removal, data disposal, notification):

### 10. Approval and change log

| Date | Change | Approved by |
|---|---|---|
| | | |

---

## Worked example: Ask Fern customer assistant (fictional)

System FH-AI-001, card reference FH-SC-001. Invented content.

### 1. Identification

| Field | Entry |
|---|---|
| System ID | FH-AI-001 |
| Name and version | Ask Fern, supplier release 4.2 |
| Card version and date | 1.2, 2026-10-20 |
| System owner | Head of Customer Service |
| Supplier / builder | ChatServe Ltd (fictional) |
| Role under the EU AI Act | Deployer |
| Risk tier and annex area | Transparency (Art 50); no Annex III area |

### 2. Intended use and limits

- Intended purpose: answer questions about delivery, returns, opening hours and product availability on the Fernhill website.
- Users: retail and trade customers.
- Affected: the same people.
- Out of scope: legal or safety advice on building work; complaints handling; discussion of orders for named third parties.
- Known limitations: may give out-of-date answers if the policy source changes; weak on unusual product codes.
- Poor performance: queries with several questions in one message; slang for trade products.

### 3. How it works

- Type: language model with retrieval from Fernhill policy and product pages.
- Inputs and outputs: customer text message in, text answer and link out.
- Components: supplier-hosted language model from a third-party model provider; supplier retrieval service.
- Human role: a customer service agent takes over on request or after two unanswered questions.

### 4. Data

| Item | Entry |
|---|---|
| Reference data | Public product pages and published policy pages. No customer records |
| Rights | Fernhill content; supplier licence covers model |
| Personal data | Customers may type personal details into chat |
| Known gaps | Pages for discontinued products are removed after seven days |
| Quality checks | Daily synchronisation with an alert when policy pages change (added after incident FH-INC-001) |
| Retention | 30 days in supplier systems under the data processing agreement (actions pending, risk FH-R-003) |

### 5. Testing and performance

| Item | Entry |
|---|---|
| Test approach | 150 test questions written by customer service staff, run before launch on 2026-02-18 |
| Metrics | Correct and complete answer rate recorded by two staff reviewers; handover rate |
| Groups | Questions in plain and informal English checked. Accessibility testing with a screen reader |
| Security | Supplier penetration test summary reviewed; Fernhill tried ten prompt injection attempts |
| Acceptance | Threshold agreed by the Head of Customer Service and signed on 2026-02-25 |

### 6. Infrastructure and resources

- Hosting: supplier cloud, EU region.
- Dependencies: Fernhill content management system feed; third-party model provider.
- Skills: content owner in customer service; IT contact for the feed.

### 7. Transparency

- Banner and first message state that Ask Fern is an automated assistant. Link to a short explanation.
- Instructions for use are held in the supplier portal and summarised for staff in the knowledge base.

### 8. Operation and monitoring

| Item | Entry |
|---|---|
| Metrics | Handover rate; unanswered rate; weekly sample of 50 transcripts reviewed |
| Thresholds | Handover above an agreed limit for two weeks triggers a content review |
| Review frequency | Weekly sample; quarterly report to the AI governance meeting |
| Logs | Conversation logs and handover events kept 30 days |
| Incident route | Customer service lead logs in the incident log; see FH-INC-001 |
| Fallback | Contact form and telephone queue staffed during opening hours |

### 9. Change and retirement

- New assessment needed for: a change of model provider, adding order lookup or account data, any use outside the website.
- Retirement: remove website embed, revoke supplier access, request deletion confirmation within 30 days.

### 10. Approval and change log

| Date | Change | Approved by |
|---|---|---|
| 2026-02-25 | Initial approval for launch | Head of Customer Service |
| 2026-05-06 | Daily synchronisation added after incident FH-INC-001 | Digital Services Manager |
| 2026-10-20 | Retention action recorded against risk FH-R-003 | AI governance lead |
