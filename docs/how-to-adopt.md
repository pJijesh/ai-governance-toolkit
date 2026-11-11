# How to adopt this toolkit: a 90-day plan

For a mid-size organisation (a few hundred to a few thousand staff) that uses AI, mostly bought from suppliers, and has no formal AI governance yet. Written for a manager who is not a specialist. This is general information and not legal advice. The time estimates are indicative and will vary.

## What you will have at day 90

- A short AI policy approved by leadership, and an acceptable use policy that staff have read.
- A complete inventory of AI systems with an owner and a risk tier for each.
- Impact assessments and supplier reviews for the highest-risk systems.
- A risk register, an incident route and a quarterly governance meeting that actually happens.
- A list of what you have not done yet, with owners and dates.

You will not have certification, and you do not need it to start. If you later pursue ISO/IEC 42001 certification, this work is a sound base. The toolkit does not guarantee it.

## Principles

1. Start with what exists. Find the AI already in use before writing rules about AI you might buy.
2. Be proportionate. Spend effort on the few systems that affect people's lives and livelihoods. Keep the rest light.
3. Make one person accountable for the programme and one person accountable for each system.
4. Prefer short documents that people use over long ones that sit in a folder.
5. Write down what you decided and why. That record is your evidence.

## Roles

You may combine roles in a smaller organisation. Name a role holder for each, with a deputy.

| Role | What they do |
|---|---|
| Executive sponsor | Approves the policy and the risk appetite, removes obstacles, receives the quarterly report |
| AI governance lead | Runs the programme, keeps the inventory and register, chairs the governance meeting. Often sits in IT, risk or compliance |
| Legal or compliance lead | Interprets the law, classifies systems, advises on regulator and customer duties |
| Data protection officer or privacy lead | Links AI work to data protection impact assessments and breach handling |
| IT and security lead | Finds AI in the estate, controls tools and accounts, supports logging and monitoring |
| HR lead | Owns training and the use of AI in employment decisions, consults staff representatives |
| Procurement lead | Adds AI questions to buying, runs supplier reviews, manages contract terms |
| System owners | Business leaders accountable for each AI system's use and outcomes |
| Internal audit (or an independent reviewer) | Checks that the system works and reports to the sponsor |

## RACI for the first 90 days

R = does the work, A = accountable (one per row), C = consulted, I = informed.

| Activity | Sponsor | Gov lead | Legal | DPO | IT/Sec | HR | Procurement | System owners |
|---|---|---|---|---|---|---|---|---|
| Approve AI policy and risk appetite | A | R | C | C | C | C | I | I |
| Build the inventory | I | A | C | C | R | C | R | R |
| Classify systems and record the EU role | I | R | A | C | C | I | I | C |
| Acceptable use policy and staff training | I | A | C | C | C | R | I | I |
| Impact assessments for high-risk and sensitive systems | I | A | C | C | C | C | I | R |
| Supplier reviews and contract terms | I | C | C | C | C | I | A | R |
| Risk register and treatment plans | I | A | C | C | C | C | C | R |
| Incident route and log | I | A | C | C | R | C | I | R |
| Human oversight checks for systems that affect people | I | A | C | I | C | C | I | R |
| Quarterly report and review | I | A | C | C | C | C | C | C |
| Independent check of the programme | A | C | I | I | I | I | I | I |

## Days 1 to 30: foundations

| Week | Actions | Output | Toolkit |
|---|---|---|---|
| 1 | Brief the sponsor. Agree scope, roles and a weekly 30 minute check-in. Read the [timeline note](eu-ai-act-timeline.md) and confirm dates with your legal adviser | Named roles; scope statement | TK-GOV-02, TK-GOV-03, TK-GOV-04 |
| 1 to 3 | Find AI in use. Ask every department. Check procurement records, software licences and browser extensions. Ask IT for the list of AI features enabled in major platforms | First draft inventory | [Inventory template](../templates/ai-system-inventory.md) |
| 2 to 3 | Screen each use case against the banned practices. Stop anything that looks prohibited and take advice | Screening record | TK-INV-03 |
| 3 to 4 | Draft the AI policy (one or two pages) and the acceptable use policy. Decide the approved tools list | Draft policies | [Acceptable use starter](../templates/ai-acceptable-use-policy.md) |
| 4 | Sponsor approves the policy. Publish the approved tools list. Set up the reporting route | Approved policy; reporting route | TK-GOV-01, TK-GOV-07, TK-USE-01 |

Common trap: trying to be complete before moving on. A 70 per cent inventory in week three is more useful than a perfect one in week ten.

## Days 31 to 60: assess

| Week | Actions | Output | Toolkit |
|---|---|---|---|
| 5 | Classify each system: EU risk tier and your role, plus an internal rating. List the top five by risk | Classified inventory; priority list | TK-INV-02 |
| 5 to 7 | Complete an impact assessment for each system that affects decisions about people, and link to any data protection assessment | Impact assessments | [Impact assessment](../templates/ai-impact-assessment.md) |
| 5 to 8 | Review the suppliers of your priority systems. Request documentation. Note contract gaps | Supplier reviews | [Vendor checklist](../templates/ai-vendor-review-checklist.md) |
| 6 to 8 | Agree the scoring method and open the risk register with the top risks from the assessments and reviews | Risk register v1 | [Risk register](../templates/ai-risk-register.md) |
| 7 to 8 | Test human oversight in practice for systems that affect people. Watch a real session | Oversight checks | [Oversight checklist](../templates/human-oversight-checklist.md) |
| 8 | Start training for staff who use or buy AI. Make it role-based and short | Training plan; first sessions | TK-GOV-06 |

## Days 61 to 90: embed

| Week | Actions | Output | Toolkit |
|---|---|---|---|
| 9 | Run a table-top incident exercise using a realistic case, such as a biased output or a data leak into a public tool | Exercise notes; fixes to the process | [Incident log](../templates/ai-incident-log.md) |
| 9 to 10 | Create a system card for each priority system. Record monitoring measures, owners and review dates | System cards | [System card](../templates/ai-system-card.md) |
| 10 to 11 | Hold the first AI governance meeting: inventory changes, top risks, open incidents, supplier actions, legal changes | Minutes; decisions | TK-GOV-10 |
| 11 | Run the validator over your registers if you keep them as CSV. Fix errors | Clean data | `tools/validate_and_report.py` |
| 12 | Write the first quarterly report for the sponsor: what you found, what you did, what remains. Be candid about gaps | Report; backlog for the next quarter | TK-GOV-09 |
| 13 | Ask internal audit or an independent reviewer to sample the work. Plan the next quarter | Review note; plan | TK-GOV-10 |

## Weekly rhythm

- Governance lead: 30 minute check-in with the sponsor.
- Governance lead and system owners: review new tools and requests.
- Once a month: review of open high risks and incidents.
- Once a quarter: governance meeting and report.

## What "good enough" looks like at day 90

Use these as a self-check, not a score.

- Can you list every AI system in use and name its owner? If not, find the gaps next quarter.
- Can you say which systems are high-risk or sensitive, and why?
- For each, is there an impact assessment, a supplier review and a person who can override?
- Do staff know what they may and may not enter into an AI tool?
- If an AI system caused harm tomorrow, would you know who to call and what to record?
- Has leadership seen the risks in plain language?

## Common pitfalls

- **Policy without technical backing.** If personal accounts remain open, the rule relies on goodwill. Pair policies with controls.
- **Treating the supplier as the owner of the risk.** Contracts shift some cost. The duty to people affected usually stays with you.
- **Oversight in name only.** Time targets and incentives can defeat a human review. Test it.
- **Assessing once and forgetting.** Models, data and use change. Set review dates and triggers.
- **Counting documents as results.** Ask what changed in how decisions are made.

## When to bring in specialists

Take advice before proceeding if you find a use that may be a banned practice, a system that may fall under Annex III, personal data used in new ways, a plan to build or rebrand a system for sale, or an incident that may be reportable. This toolkit helps you organise the work and ask better questions. It does not replace legal advice.

## After day 90

- Extend impact assessments and system cards to the remaining systems.
- Plan for the Annex III date (see the [timeline note](eu-ai-act-timeline.md)).
- Decide whether a formal management system standard such as ISO/IEC 42001 suits your customers and sector. If so, use the [control matrix](control-matrix.md) as a starting point for a gap assessment, with a qualified adviser.
