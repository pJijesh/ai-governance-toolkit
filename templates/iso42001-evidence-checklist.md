# ISO/IEC 42001 evidence checklist

> General information only, not legal advice. Fernhill Building Supplies Ltd is a fictional company and every example in this file is invented. No text from ISO/IEC 42001 is reproduced; descriptions are short paraphrases.

Supports the ISO/IEC 42001 mapped controls in [the control matrix](../docs/control-matrix.md). Related framework items: all 65 items in [the ISO/IEC 42001 framework list](../data/frameworks/iso42001_items.csv), covering clauses 4 to 10 and Annex A. The `Requirement` column matches that list; the `Toolkit control(s)` column points to the relevant control.

## Purpose

An audit is easier when the evidence is gathered before it is asked for. This template gives one row for each framework item in scope, with a short description, an example of the kind of evidence an auditor might ask to see, and a suggested owner. It is a starting checklist, not a certification result.

## How to use it

1. Confirm the scope of the management system and which systems are in it.
2. Confirm the owner for each row. Owners are roles, not named people; the listed role is a suggestion from the control matrix.
3. For each row, look for the example evidence or other evidence that shows the same thing. Mark the row **In place**, **Gap** or **Not applicable**. Give a reason for **Not applicable**.
4. Record where the evidence is kept and the date it was checked. A document ID or link is enough; do not paste confidential content into this file.
5. Agree actions and dates for gaps with the AI governance lead. Where a gap affects an AI system, add it to the risk register or corrective action log.
6. Repeat before an audit and after a significant change to the management system or an in-scope system.

One example does not prove that a requirement is met across the whole scope. An auditor will also ask how the evidence is kept up to date and how it links to practice.

## Checklist

The descriptions below are short paraphrases, not standard wording. The evidence column gives one typical example; other evidence may be equally valid.

### Clauses 4 to 10

| Requirement | Short description (paraphrased) | Example evidence an auditor may ask for | Owner (role) | Toolkit control(s) | Status | Evidence reference |
|---|---|---|---|---|---|---|
| 4.1 | Understanding the organisation and its context | Register of obligations with dates and owners | Legal or compliance lead | TK-GOV-03 | | |
| 4.2 | Needs and expectations of interested parties | Consultation notes and the obligations register | AI governance lead | TK-GOV-03; TK-GOV-12 | | |
| 4.3 | Scope of the AI management system | Scope statement | AI governance lead | TK-GOV-04 | | |
| 4.4 | The AI management system itself | Scope statement and procedure index | AI governance lead | TK-GOV-04; TK-CON-01 | | |
| 5.1 | Leadership and commitment | Minutes showing leadership approval and review | Board sponsor | TK-GOV-01 | | |
| 5.2 | AI policy | Approved policy with version history | Board sponsor | TK-GOV-01 | | |
| 5.3 | Roles responsibilities and authorities | RACI chart and role descriptions | AI governance lead | TK-GOV-02 | | |
| 6.1.1 | Addressing risks and opportunities (general) | Risk method and obligations register with owners | AI governance lead | TK-GOV-03; TK-INV-02 | | |
| 6.1.2 | AI risk assessment (planning) | Written risk method with scales and a completed assessment | AI governance lead | TK-RSK-01 | | |
| 6.1.3 | AI risk treatment (planning) | Treatment plans and signed residual risk acceptance | Risk owner | TK-RSK-02 | | |
| 6.1.4 | AI system impact assessment (planning) | Completed impact assessment with sign-off | System owner | TK-RSK-03 | | |
| 6.2 | AI objectives and how to achieve them | Objectives with measures, dates and an owner | Board sponsor | TK-GOV-05 | | |
| 6.3 | Planning of changes | Change records and re-assessment trigger list | System owner | TK-RSK-07; TK-INV-05 | | |
| 7.1 | Resources | Budget or time allocation approved by the sponsor | AI governance lead | TK-GOV-04 | | |
| 7.2 | Competence | Training matrix and completion records | HR lead | TK-GOV-06 | | |
| 7.3 | Awareness | Staff briefing notes and acknowledgement records | HR lead | TK-GOV-06 | | |
| 7.4 | Communication | Communication matrix and issued notices | AI governance lead | TK-GOV-09 | | |
| 7.5 | Documented information | Document register and retention schedule | AI governance lead | TK-GOV-08 | | |
| 8.1 | Operational planning and control | Inventory and go-live approval record | AI governance lead | TK-INV-01; TK-LIF-05 | | |
| 8.2 | AI risk assessment (operation) | Completed risk register entries for live systems | AI governance lead | TK-RSK-01 | | |
| 8.3 | AI risk treatment (operation) | Treatment plans with dates and status | Risk owner | TK-RSK-02 | | |
| 8.4 | AI system impact assessment (operation) | Impact assessment reviewed on change and at set intervals | System owner | TK-RSK-03 | | |
| 9.1 | Monitoring measurement analysis and evaluation | Monitoring report and review notes | AI governance lead | TK-LIF-06; TK-GOV-10 | | |
| 9.2 | Internal audit | Audit plan and reports | Internal audit | TK-GOV-10 | | |
| 9.3 | Management review | Management review minutes and decisions | Board sponsor | TK-GOV-10 | | |
| 10.1 | Continual improvement | Corrective action log with closed items | AI governance lead | TK-GOV-11 | | |
| 10.2 | Nonconformity and corrective action | Incident log and corrective action record | AI governance lead | TK-GOV-11; TK-INC-01 | | |

### Annex A controls

| Requirement | Short description (paraphrased) | Example evidence an auditor may ask for | Owner (role) | Toolkit control(s) | Status | Evidence reference |
|---|---|---|---|---|---|---|
| A.2.2 | Organisational AI policy | Approved AI policy with version history | Board sponsor | TK-GOV-01 | | |
| A.2.3 | Fit with other organisational policies | Cross-reference from the AI policy to other policies | AI governance lead | TK-GOV-01; TK-USE-01 | | |
| A.2.4 | Review cycle for the AI policy | Minutes showing the review date and decision | Board sponsor | TK-GOV-01 | | |
| A.3.2 | Allocation of AI roles and responsibilities | RACI chart and role descriptions | AI governance lead | TK-GOV-02 | | |
| A.3.3 | Channel for raising concerns | Published reporting route and log of concerns | AI governance lead | TK-GOV-07 | | |
| A.4.2 | Documenting the resources a system needs | System card sections on data and infrastructure | System owner | TK-INV-01; TK-INV-04 | | |
| A.4.3 | Data resources | Data description in the system card and data quality checks | Data owner | TK-INV-04; TK-DAT-01 | | |
| A.4.4 | Tooling resources | List of tools used with the system | System owner | TK-INV-04 | | |
| A.4.5 | System and computing resources | Infrastructure notes and security test report | System owner | TK-INV-04; TK-LIF-04 | | |
| A.4.6 | People and skills | Training matrix and role-based guidance | HR lead | TK-GOV-06 | | |
| A.5.2 | Impact assessment procedure | Written impact assessment method | System owner | TK-RSK-03 | | |
| A.5.3 | Recording impact assessment results | Completed impact assessments with sign-off | System owner | TK-RSK-03 | | |
| A.5.4 | Effects on individuals and groups | Impact assessment section on people plus fairness results | System owner | TK-RSK-03; TK-RSK-04; TK-LIF-03 | | |
| A.5.5 | Effects on society | Impact assessment section on wider effects | System owner | TK-RSK-03 | | |
| A.6.1.2 | Goals for responsible development | Objectives with measures and dates | Board sponsor | TK-GOV-05 | | |
| A.6.1.3 | Responsible design and development process | Design process procedure and requirements document | System owner | TK-LIF-01 | | |
| A.6.2.2 | Requirements and specification | Requirements document with intended use and limits | System owner | TK-LIF-01 | | |
| A.6.2.3 | Design and development records | Completed system card | System owner | TK-LIF-08 | | |
| A.6.2.4 | Verification and validation | Test plan and results with acceptance sign-off | System owner | TK-LIF-02; TK-LIF-04 | | |
| A.6.2.5 | Deployment | Go-live checklist and approval record | AI governance lead | TK-LIF-05 | | |
| A.6.2.6 | Operation and monitoring | Monitoring report and review cadence | System owner | TK-LIF-06; TK-INC-03 | | |
| A.6.2.7 | Technical documentation | Current system card with design, data and limits | System owner | TK-LIF-08 | | |
| A.6.2.8 | Recording of event logs | Log configuration and retention rule | Head of IT security | TK-LIF-07 | | |
| A.7.2 | Data for development and improvement | Data description and quality checks | Data owner | TK-DAT-01 | | |
| A.7.3 | Obtaining data | Data source register and licence evidence | Data owner | TK-DAT-02; TK-DAT-03 | | |
| A.7.4 | Data quality | Data quality checks and documented limits | Data owner | TK-DAT-01; TK-LIF-03 | | |
| A.7.5 | Data provenance | Data source register | Data owner | TK-DAT-02 | | |
| A.7.6 | Data preparation | Preparation steps recorded in the system card | Data owner | TK-DAT-01 | | |
| A.8.2 | User documentation and information | Interface notices and user guidance | System owner | TK-USE-02; TK-USE-03 | | |
| A.8.3 | External reporting | Reporting decision records and contact list | Legal or compliance lead | TK-INC-02 | | |
| A.8.4 | Communication of incidents | Incident log with notification entries | AI governance lead | TK-INC-01 | | |
| A.8.5 | Information for interested parties | Communication matrix and issued notices | AI governance lead | TK-GOV-09; TK-RSK-05; TK-USE-02; TK-USE-03; TK-USE-04 | | |
| A.9.2 | Processes for responsible use | Acceptable use policy and approved tools list | AI governance lead | TK-INV-03; TK-LIF-09; TK-USE-01 | | |
| A.9.3 | Objectives for responsible use | Objectives with measures and acknowledged policy | Board sponsor | TK-GOV-05; TK-USE-01 | | |
| A.9.4 | Intended use | Intended purpose statement in the inventory and system card | System owner | TK-INV-02; TK-LIF-01 | | |
| A.10.2 | Allocating responsibilities | Contract clause checklist and responsibility split | Procurement lead | TK-THR-02 | | |
| A.10.3 | Suppliers | Completed vendor review and supplier review notes | Procurement lead | TK-THR-01; TK-THR-02; TK-THR-03 | | |
| A.10.4 | Customers | Customer documentation and support commitments | Product owner | TK-THR-04 | | |

---

## Worked example (fictional)

At Fernhill Building Supplies Ltd, the Head of IT security checked A.6.2.8 for system FH-AI-002 on 2026-10-01. The row was marked **In place** and the evidence reference recorded "Log configuration and 90-day retention rule, FH-SC-001, section 8". The system card was updated on the same date.

What the example shows: the evidence reference tells a reviewer what to ask for and where to find it. A status on its own does not show whether the evidence exists.
