# AI risk register

> General information only, not legal advice. Fernhill Building Supplies Ltd is a fictional company and every example in this file is invented.

Supports controls TK-RSK-01 (risk assessment method), TK-RSK-02 (risk treatment and residual risk acceptance) and TK-GOV-05 (objectives and risk appetite). Related framework items: ISO/IEC 42001 6.1.2, 6.1.3, 8.2 and 8.3, EU AI Act Art 9, NIST AI RMF MAP 5.1, MANAGE 1.2 and MANAGE 1.3.

## Purpose

The register records what could go wrong with each AI system, how serious it would be, what is being done, and who owns the answer. It is a living record. A register nobody reviews is worse than none because it gives false comfort.

## Files

- [`ai-risk-register.csv`](ai-risk-register.csv): the blank header.
- [`examples/fernhill/ai-risk-register.csv`](../examples/fernhill/ai-risk-register.csv): fifteen worked entries for the fictional company.

## Scoring method

Score likelihood and impact from 1 to 5. The score is the product of the two.

| Score | Likelihood | Impact |
|---|---|---|
| 1 | Rare. Not expected in the next two years | Negligible. Handled in normal work |
| 2 | Unlikely. Could happen once in two years | Minor. Small cost or inconvenience, no lasting effect |
| 3 | Possible. Could happen in the next year | Moderate. Complaints, rework or a short disruption |
| 4 | Likely. Expected in the next year | Major. Harm to individuals, regulatory attention or significant cost |
| 5 | Almost certain. Expected within months | Severe. Serious harm to people, major legal exposure or loss of trust |

Adapt the wording to your organisation and have leadership approve it. The bands below are used by the validator.

| Score | Rating |
|---|---|
| 1 to 4 | low |
| 5 to 9 | medium |
| 10 to 16 | high |
| 20 to 25 | critical |

With a 5 by 5 grid, scores of 17 to 19 cannot occur, so the bands leave no gap.

Score twice: once for the **inherent** risk (before the controls you plan) and once for the **residual** risk (after them). If you choose to accept a risk, the residual score equals the inherent score.

## Column guide

| Column | Entry |
|---|---|
| risk_id | `XX-R-000` format |
| system_id | Must exist in the inventory. The validator rejects orphan risks |
| risk_title | A short statement of what could go wrong |
| description | The cause and the consequence |
| category | `bias-fairness`, `privacy`, `security`, `accuracy-reliability`, `transparency`, `legal-regulatory`, `third-party`, `operational`, `misuse`, `human-oversight` |
| likelihood, impact | Whole numbers 1 to 5 |
| inherent_score, inherent_rating | Product and band. The validator recomputes both |
| existing_controls | Control IDs from the [control matrix](../docs/control-matrix.md), separated by semicolons |
| treatment | `mitigate`, `accept`, `transfer`, `avoid` |
| treatment_actions | Specific actions, not intentions |
| risk_owner | A role with authority to act |
| target_date | When the actions complete |
| residual_likelihood, residual_impact, residual_score, residual_rating | After treatment |
| status | `open`, `mitigating`, `accepted`, `closed` |
| last_reviewed | `YYYY-MM-DD` |

## Treatment choices in plain terms

- **Mitigate**: reduce the likelihood or the impact with controls.
- **Transfer**: share the risk, for example through contract terms or insurance. This rarely removes the risk entirely and the organisation stays accountable to the people affected.
- **Avoid**: stop the activity or switch off the feature.
- **Accept**: decide knowingly to live with the risk. A person with the authority to accept it should sign. Set a stricter approval level for high and critical risks.

## Review rhythm

- Monthly for the owner of each open high or critical risk.
- Quarterly for the whole register at the AI governance meeting.
- Whenever an incident, a system change or a new regulation affects a risk.

## Worked example

The Fernhill register includes entries chosen to show each treatment type:

| Entry | Treatment | What it shows |
|---|---|---|
| FH-R-004 supplier outage | transfer | Contract terms and service credits, with a fallback queue because the duty to customers stays |
| FH-R-009 emotion analysis feature | avoid | Switching off a feature that would be a banned practice in the workplace |
| FH-R-013 extraction error | accept | Accepted because existing checks are enough; residual equals inherent |
| FH-R-005 biased ranking | mitigate | Multiple controls with measurable follow-up |

Entries FH-R-005 to FH-R-009 relate to the same system as the [impact assessment example](ai-impact-assessment.md). The register records the organisation's risk while the assessment records effects on people.
