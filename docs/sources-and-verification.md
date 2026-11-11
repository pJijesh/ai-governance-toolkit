# Sources and verification

This page records how the identifiers in the toolkit were checked, what could not be checked, and how to re-verify them. Checks were carried out on 4 November 2026.

## Principles

- **Identifiers are facts; text is not.** Clause numbers, control numbers, article numbers and subcategory IDs appear in the data. Titles in the data are the author's short paraphrases. They are not the wording of the standards. ISO/IEC 42001 is a copyrighted, paid standard, and no standard text is reproduced here.
- **Mappings are judgement.** Which toolkit control relates to which framework item is the author's professional judgement. There is no official crosswalk behind it. Two competent practitioners could map some rows differently.
- **Verification is recorded in the data.** Every framework item has a `verification` value. `secondary-checked` means the ID and a matching topic were found in at least one secondary source. `unchecked` means they were not. At the time of writing no item is `unchecked`, but no item is `primary-checked` either.

## What was checked, and against what

| Framework | Items in data | Checked against | Not checked |
|---|---|---|---|
| ISO/IEC 42001:2023 clauses 4 to 10 | 27 | A published clause listing from a consultancy (Advisera) | The standard itself |
| ISO/IEC 42001:2023 Annex A | 38 controls in 9 areas | A public control listing (riskprofs.com), consistent with the commonly cited structure of nine control areas and 38 controls | The standard itself. Annex B implementation guidance is not mapped |
| EU AI Act | 40 articles chosen as relevant to operators | A public article explorer (artificialintelligenceact.eu) listing article numbers and titles | The Official Journal text. The EUR-Lex page could not be read article by article with the tools available |
| NIST AI RMF 1.0 | 72 subcategories in 19 categories across four functions | A public catalogue of the framework (stigviewer.com), and the author's own knowledge of NIST AI 100-1 | The NIST publication and Playbook text |

## Known discrepancies and cautions

- One blog post that was consulted listed a different structure for ISO/IEC 42001 Annex A, with ID ranges that did not add up to the 38 controls the standard has. It was disregarded.
- The article explorer showed some article numbers with letter suffixes (for example 4a and 75a). These appear to be insertions from the Digital Omnibus amendments. The toolkit uses the original numbering of Regulation (EU) 2024/1689.
- Art 4 and Art 5 were amended according to secondary sources. Treat their wording as needing a fresh check.
- ISO/IEC 42001 has sub-clauses below the level used here (for example 7.5.1 to 7.5.3, 9.2.1 and 9.2.2, 9.3.1 to 9.3.3). They are folded into their parent clause.
- The EU AI Act annexes (Annex I, III, IV) are referred to in notes and are not separate items in the data.
- Dates in the [timeline note](eu-ai-act-timeline.md) come from law firm briefings and trackers. The amending act number is reported by one source only.

## Secondary sources consulted

- Advisera, ISO 42001 clauses and requirements: https://advisera.com/articles/iso-42001-clauses-requirements/
- riskprofs.com, ISO 42001 Annex A controls list: https://riskprofs.com/iso-42001-annex-a-controls-list/
- STIGViewer, NIST AI RMF catalogue: https://www.stigviewer.com/controls/ai-rmf/catalog
- EU AI Act Explorer (artificialintelligenceact.eu): https://artificialintelligenceact.eu/ai-act-explorer/
- Gibson Dunn, EU AI Act Omnibus agreement: https://www.gibsondunn.com/eu-ai-act-omnibus-agreement-postponed-high-risk-deadlines-and-other-key-changes/
- Garrigues, AI Digital Omnibus Regulation published: https://www.garrigues.com/en_GB/garrigues-digital/ai-digital-omnibus-regulation-has-been-published-redefining-deadlines-and

Links were valid when consulted. They are listed as evidence of the checking done and not as endorsements.

## Primary sources to use when you re-verify

- EU AI Act: EUR-Lex, Regulation (EU) 2024/1689, plus the amending act.
- ISO/IEC 42001:2023: purchase from ISO or a national standards body.
- NIST AI RMF 1.0 (NIST AI 100-1) and the AI RMF Playbook: nist.gov and airc.nist.gov.

## How to re-verify

1. Open the primary source.
2. For each row in `data/frameworks/`, confirm that the ID exists and that the paraphrased title describes the same topic.
3. Change `verification` to `primary-checked` only after doing this, and add `primary-checked` to the allowed values in `tools/validate_and_report.py`.
4. Re-run `python tools/validate_and_report.py` and commit the regenerated documents.

## Reporting an error

If you find an incorrect identifier or mapping, open an issue or pull request. See [CONTRIBUTING](../CONTRIBUTING.md).
