# AI incident log

> General information only, not legal advice. Fernhill Building Supplies Ltd is a fictional company and every example in this file is invented.

Supports controls TK-INC-01 (incident detection and response), TK-INC-02 (external reporting and authority liaison), TK-GOV-07 (channel for raising concerns) and TK-GOV-11 (corrective action and improvement). Related framework items: ISO/IEC 42001 A.8.3, A.8.4 and 10.2, EU AI Act Art 20, Art 26(5), Art 73 and Art 87, NIST AI RMF MANAGE 4.3, MANAGE 2.3 and GOVERN 4.3.

## Purpose

AI systems fail in ways that ordinary IT incident processes do not always capture: a wrong answer is not an outage, and a biased ranking may never trigger an alert. This log records AI-related incidents, near misses and concerns in one place so patterns become visible and lessons are acted on.

## Files

- [`ai-incident-log.csv`](ai-incident-log.csv): the blank header.
- [`examples/fernhill/ai-incident-log.csv`](../examples/fernhill/ai-incident-log.csv): four worked entries.

## What counts as an incident

Record it if any of these is true:

- An AI system produced an output that caused, or could have caused, harm to a person or to the organisation.
- A system behaved outside its documented limits or intended use.
- Data was exposed to or through an AI tool in a way the policy does not allow.
- Someone raised a concern about unfair or discriminatory outcomes.
- A system stopped working in a way that affects people.

Near misses belong in the log. They are the cheapest source of lessons.

## Handling steps

1. **Detect and record.** Anyone can raise it through the reporting route. The system owner or the AI governance lead logs it the same day.
2. **Contain.** Pause or restrict the system if people may be harmed. Use the fallback process.
3. **Assess severity.** Use the table below.
4. **Decide on external reporting.** Ask the data protection officer and the legal or compliance lead. Consider personal data breach rules, the provider notification duty and any serious incident reporting duty. Record the reasoning even when the answer is no.
5. **Investigate root cause.** Look at data, model, process and people, not only the tool.
6. **Correct and prevent.** Record the corrective action, link to the control it strengthens, and set an owner and date.
7. **Close and learn.** Close only when the corrective action is evidenced. Record lessons and update the risk register and system card.

## Severity guide

| Severity | Typical features |
|---|---|
| low | No person harmed. Easily corrected. Contained within one team |
| medium | Limited harm or exposure to a small number of people. Correction needed with some effort |
| high | Harm or likely harm to individuals, possible discrimination, or possible legal duty to notify |
| critical | Serious harm to people, wide exposure, or loss of trust requiring leadership action |

## External reporting: points to check

- **Serious incidents under the Act.** The Act defines serious incidents (Art 3) and requires providers of high-risk systems to report them to market surveillance authorities (Art 73). Deployers must inform the provider and, in certain cases, the authorities (Art 26(5)). Check the current guidance and deadlines with your legal adviser.
- **Personal data breaches.** Data protection law has its own notification tests and time limits. Involve the data protection officer at once.
- **Contractual duties.** Customer and supplier contracts may require notification.
- **Sector rules.** Regulated sectors may have further reporting duties.

## Column guide

| Column | Entry |
|---|---|
| incident_id | `XX-INC-000` format |
| system_id | Must exist in the inventory |
| date_detected | `YYYY-MM-DD` |
| description | What happened, in facts |
| category | `harmful-output`, `bias-discrimination`, `data-leak`, `security-breach`, `outage`, `misuse`, `drift-degradation`, `other` |
| severity | `low`, `medium`, `high`, `critical` |
| affected_people | Who and roughly how many |
| immediate_action | What was done to contain it |
| root_cause | Confirmed cause, or "Under investigation" |
| corrective_action | Required for a closed incident |
| related_controls | Control IDs from the [control matrix](../docs/control-matrix.md), separated by semicolons |
| reportable_externally | `yes`, `no`, `under-assessment` |
| external_report_date | Required when `yes` |
| status | `open`, `investigating`, `closed` |
| closed_date | Required when closed, not earlier than detection |
| lessons | What will be different next time |

## Worked example

The Fernhill log contains four entries:

| ID | System | Category | Severity | Status | Teaching point |
|---|---|---|---|---|---|
| FH-INC-001 | Ask Fern customer assistant | drift-degradation | low | closed | A wrong answer is an incident even when no system is down. The fix was a daily content refresh |
| FH-INC-002 | GenAssist staff assistant | data-leak | medium | closed | The root cause was missing provision, not a careless individual. The decision not to report externally was recorded with reasons |
| FH-INC-003 | TalentLens CV shortlisting | bias-discrimination | high | investigating | An open incident with an external reporting decision still under assessment, the pilot paused and the risk register and impact assessment reopened |
| FH-INC-004 | Stock demand forecasting model | outage | low | closed | The fallback to the previous plan worked as designed |

Open the [example log](../examples/fernhill/ai-incident-log.csv) and run `python tools/validate_and_report.py` to see the checks the validator applies: valid system and control references, dates in order, and a corrective action on every closed incident.
