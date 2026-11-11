# AI system inventory

> General information only, not legal advice. Fernhill Building Supplies Ltd is a fictional company and every example in this file is invented.

Supports controls TK-INV-01 (inventory), TK-INV-02 (risk classification and role check) and TK-INV-03 (prohibited practice screening). Related framework items: ISO/IEC 42001 A.4.2, EU AI Act Art 6 and Art 26, NIST AI RMF GOVERN 1.6.

## Why keep one

You cannot govern what you cannot list. Most organisations find AI in places they did not expect: a feature switched on inside a CRM, a recruitment tool bought by HR, a free browser assistant used by a team. The inventory is the starting point for every other control in this toolkit. It tells you which systems need an impact assessment, which need a supplier review and which need a human oversight check.

## How to use it

1. Copy [`ai-system-inventory.csv`](ai-system-inventory.csv) (header only) to wherever your organisation keeps controlled records. A spreadsheet is fine to begin with.
2. Add one row per system. Include systems that are planned, on trial, bought, built in house or embedded in another product.
3. Fill every column. Use the allowed values below so the file can be checked by the validator in `tools/`.
4. Review the whole inventory every quarter and whenever procurement, IT or a business team reports a new tool.
5. Never delete a row. Set the status to `retired` and keep the history.

## Column guide

| Column | What to enter | Allowed values or format |
|---|---|---|
| system_id | Unique identifier | Prefix, `-AI-`, three digits (for example `FH-AI-001`) |
| name | Short name people recognise | Free text |
| description | One sentence on what the system does | Free text |
| business_owner | The role accountable for outcomes | Role title, not an individual's name |
| technical_owner | The role who runs it | Role title |
| vendor | Supplier name, or blank if built in house | Free text |
| source_type | Where it came from | `bought`, `built`, `embedded`, `open-source`, `hybrid` |
| purpose | The decision or task it supports | Free text |
| affected_people | Who is affected by its outputs | Free text |
| personal_data | Does it process personal data | `yes`, `no`, `unknown` |
| eu_ai_act_role | Your role under the EU AI Act | `deployer`, `provider`, `provider-and-deployer`, `importer`, `distributor`, `not-assessed` |
| eu_risk_tier | Working classification | `prohibited`, `high-risk`, `high-risk-provisional`, `transparency`, `minimal`, `not-assessed` |
| annex_area | For high-risk tiers, the Annex III point or Annex I area | Free text, required for high-risk tiers |
| internal_risk_rating | Your own rating, which may differ from the EU tier | `low`, `medium`, `high`, `critical`, `not-assessed` |
| human_oversight | How a person can review or override | Required for live and pilot systems |
| impact_assessment_ref | Reference to the assessment or screening note | Required for high-risk tiers |
| status | Lifecycle state | `proposed`, `pilot`, `live`, `suspended`, `retired` |
| go_live_date | Date the system went live | `YYYY-MM-DD`, required for live, pilot and suspended |
| next_review_date | Date of next review | `YYYY-MM-DD`, required unless retired |
| notes | Anything a reviewer needs | Free text |

## Classification guidance

- Start with the banned practices in Art 5 of the Act. If a use case appears to fall within one, stop and take legal advice before going further.
- Then check whether the use case sits in an Annex III area (for example recruitment, access to essential services such as credit, education, or biometric identification). If it does, record `high-risk` or `high-risk-provisional` and note the point.
- Then check the transparency duties in Art 50 (for example systems that interact directly with people, or that generate synthetic content).
- Otherwise record `minimal`. Even then, the internal rating may be higher. A free text assistant can be `minimal` under the Act and still `medium` internally because of data leakage risk.
- Your role matters as much as the tier. A deployer using a supplier's system has different duties from the provider who built it. You can become the provider if you put your name on a system, change its intended purpose or make a substantial modification (Art 25).
- Dates for each duty are in the [EU AI Act timeline](../docs/eu-ai-act-timeline.md). Check them against the Official Journal.

## Worked example: Fernhill Building Supplies Ltd (fictional)

The complete worked file is [`examples/fernhill/ai-system-inventory.csv`](../examples/fernhill/ai-system-inventory.csv). A summary:

| ID | System | Role | Tier | Internal rating | Status |
|---|---|---|---|---|---|
| FH-AI-001 | Ask Fern customer assistant | deployer | transparency | medium | live |
| FH-AI-002 | TalentLens CV shortlisting | deployer | high-risk | high | pilot |
| FH-AI-003 | Stock demand forecasting model | provider-and-deployer | minimal | low | live |
| FH-AI-004 | GenAssist staff assistant | deployer | minimal | medium | live |
| FH-AI-005 | Invoice data extraction | deployer | minimal | low | live |
| FH-AI-006 | Trade credit limit recommender | provider-and-deployer | high-risk-provisional | high | proposed |

Points the example is meant to show:

- FH-AI-006 is only `high-risk-provisional`. Sole traders are individuals, so a credit decision about them may fall within the Annex III creditworthiness point. The inventory records the doubt and the row says not to build until the question is settled.
- FH-AI-004 is `minimal` under the Act but `medium` internally, and the notes record that the AI literacy duty and transparency duties may still apply.
- FH-AI-003 is built in house for own use. Fernhill is therefore both provider and deployer, although few obligations follow from a minimal-risk tier.

## Validation

Run `python tools/validate_and_report.py` from the repository root. It checks the example inventory for duplicate IDs, invalid values, missing dates and the rule that high-risk tiers need an annex area and an impact assessment reference.
