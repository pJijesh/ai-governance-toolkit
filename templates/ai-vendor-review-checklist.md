# AI vendor and supplier review checklist

> General information only, not legal advice. Fernhill Building Supplies Ltd and TalentLens Software are fictional and every example in this file is invented.

Supports controls TK-THR-01 (supplier due diligence), TK-THR-02 (contract terms and shared responsibility), TK-THR-03 (supplier monitoring and exit) and TK-THR-04 (obligations to customers). Related framework items: ISO/IEC 42001 A.10.2, A.10.3 and A.10.4, EU AI Act Art 25 and Art 53, NIST AI RMF GOVERN 6.1, GOVERN 6.2, MAP 4.1 and MANAGE 3.1.

## Purpose

Most organisations buy AI rather than build it. Buying does not transfer accountability. This checklist helps a non-specialist buyer ask consistent questions, record the answers and decide whether to proceed, proceed with conditions or walk away.

## How to use it

1. Complete sections 1 and 2 before any demonstration or pilot.
2. Send sections 3 to 8 to the supplier as a questionnaire. Ask for documents, not assurances.
3. Score each answer: **Met**, **Partly met**, **Not met** or **Not applicable**. Record the evidence you saw.
4. Take any "Not met" on a starred item (*) to the AI governance lead before proceeding.
5. Record the decision in section 10 and the follow-up actions with dates.
6. Repeat at renewal and when the supplier announces a significant change to the product or its model providers.

A supplier's marketing claim is not evidence. A certificate is evidence of what it covers, so check its scope, issue date and issuing body.

## Checklist

### 1. Intake

| Item | Entry |
|---|---|
| Supplier legal name and country | |
| Product and version | |
| Business owner (role) | |
| Intended purpose | |
| Inventory ID | |
| Data to be shared | |
| Does the use fall within an Annex III area or a transparency duty? | |

### 2. Role under the EU AI Act

| Question | Answer |
|---|---|
| Who is the provider of the system? | |
| Will we be a deployer only? | |
| Would we rebrand it, change its intended purpose or modify it substantially? If so we may become the provider (Art 25). | |
| Is the supplier established outside the EU, and if so is there an authorised representative? | |
| Does the product rely on a general-purpose AI model from a third party? Which one? | |

### 3. Governance and assurance

| Item | Status | Evidence |
|---|---|---|
| Supplier has a named person accountable for AI governance | | |
| Supplier can describe its AI risk management approach | | |
| Relevant independent assurance (for example an information security or AI management system certificate) and its scope | | |
| Supplier states its classification of the product under the EU AI Act and the reasoning * | | |
| Supplier states whether it has completed any conformity steps for high-risk use * | | |

### 4. Documentation and transparency

| Item | Status | Evidence |
|---|---|---|
| Instructions for use that state intended purpose, accuracy levels and known limits * | | |
| Description of training and testing data sources at a level we can assess | | |
| Information on how outputs should be interpreted | | |
| Description of human oversight measures built into the product * | | |
| For general-purpose models: the technical documentation and copyright policy information that the model provider must make available (Art 53) | | |

### 5. Performance, bias and safety

| Item | Status | Evidence |
|---|---|---|
| Accuracy results on data similar to ours | | |
| Bias or fairness testing method and results for groups relevant to our use * | | |
| Known failure modes and the supplier's guidance on them | | |
| Process for retesting after model updates | | |
| Resilience to misuse, manipulation or prompt attacks | | |

### 6. Data protection and security

| Item | Status | Evidence |
|---|---|---|
| Roles under data protection law are clear (controller, processor) and a data processing agreement is in place * | | |
| Data location and any international transfers | | |
| Our data is not used to train models for others, unless we have agreed to it * | | |
| Retention and deletion periods for our inputs, outputs and logs | | |
| Security controls, access management and encryption | | |
| Sub-processors are listed and changes are notified | | |

### 7. Logging, monitoring and incidents

| Item | Status | Evidence |
|---|---|---|
| Logs available to us, with format and retention period * | | |
| Incident notification commitment, including timing and content * | | |
| Supplier supports us in meeting our own reporting duties | | |
| Service levels and fallback arrangements | | |

### 8. Contract terms to request

| Clause | Status |
|---|---|
| Intended purpose and prohibited uses | |
| Allocation of responsibilities under the Act | |
| Notification of material changes to the model, data or sub-processors | |
| Audit and information rights proportionate to the risk | |
| Cooperation with regulators and with our assessments | |
| Liability and indemnity position | |
| Termination, data return and deletion, and exit assistance | |
| Availability commitment and service credits | |

### 9. Ongoing monitoring plan

- Review frequency:
- Metrics or signals we will watch:
- Who receives supplier change notices:
- Exit plan owner and trigger conditions:

### 10. Decision

| Decision | Proceed / Proceed with conditions / Do not proceed |
|---|---|
| Conditions and dates | |
| Reviewer (role) | |
| Date | |
| Next review | |

---

## Worked example: TalentLens Software (fictional)

Review FH-VR-003, system FH-AI-002, completed 2026-08-12 by the Procurement lead with HR, IT and data protection input. Invented content.

### Summary of findings

| Section | Result | Notes |
|---|---|---|
| 2 Role | Fernhill is a deployer | Fernhill will not rebrand or modify the product. Supplier is established in the UK and says it will appoint an EU representative before offering the product to EU customers |
| 3 Governance | Partly met | The supplier named a responsible officer. It holds an information security certificate but has no AI management system certificate. It classes the product as high-risk (Annex III 4(a)) and says its conformity work is under way |
| 4 Documentation | Partly met * | Instructions for use were supplied in draft. They lack accuracy figures by group |
| 5 Bias and safety | Not met * | Supplier offered a summary statement only and no testing method or results |
| 6 Data protection | Met | Processing agreement signed. Retention 90 days, reduced to 30 on request. No model training on Fernhill data |
| 7 Logging and incidents | Partly met * | Logs available for 12 months on request. Incident notice within 72 hours offered, Fernhill requested 24 hours |
| 8 Contract | Partly met | Change notification and audit rights agreed. Liability cap under negotiation |

### Decision

Proceed with conditions, limited to the pilot.

- Supplier provides bias testing method and results by 2026-10-30 (extended to 2026-12-11; see risk FH-R-005).
- Optional video interview analysis is disabled in contract schedule 3 (risk FH-R-009).
- Final instructions for use and log field descriptions by 2027-01-15 (risk FH-R-007).
- Renewal is conditional on all of the above.

Reviewer: Procurement lead. Next review: 2027-01-15.

What the example shows: a "not met" on a starred item did not block a limited pilot, but it created dated conditions that feed the risk register. Without them, the review would be a form with no consequences.
