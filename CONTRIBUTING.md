# Contributing

Thank you for helping to improve the toolkit. Corrections are the most valuable contribution, especially to identifiers, dates and mappings.

## Ground rules

- **No real organisational data.** Examples must be fictional or synthetic. Do not submit names, systems, incidents or figures from a real employer or client.
- **No copyrighted standard text.** Do not paste text from ISO/IEC 42001 or other paid standards. Use short paraphrases and identifiers.
- **Cite your check.** For any change to an identifier, article number, date or mapping, say what you checked it against (primary source preferred) in the pull request.
- **Keep the CSV as the source of truth.** Edit `data/control_matrix.csv` and the framework files, then regenerate the markdown views. Do not edit `docs/control-matrix.md` or `docs/coverage-report.md` by hand.
- **No legal advice.** Describe what a requirement is about. Do not tell readers what the law requires of them in their circumstances.
- **British English**, plain language, no hype.

## Workflow

1. Fork the repository and create a branch.
2. Make your change.
3. Run the checks from the repository root:

   ```
   python tools/validate_and_report.py
   python tools/register_health.py --as-of 2026-12-20 --output docs/register-health-example.md
   python -m unittest discover -s tests -v
   ```

4. Commit the regenerated documents together with your change.
5. Open a pull request describing the change and the evidence for it.

CI runs the same checks with `--check`, which fails if the generated documents are out of date.

## Reporting a problem

Open an issue with the file, the line or identifier, what is wrong, and the source that shows it. Please do not include confidential information.
