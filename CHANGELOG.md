# Changelog

All notable changes to this project are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses
[Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added

- A second worked example, `examples/larkspur/`: a fictional energy supplier using AI in customer service, with an inventory, risk register, incident log, a completed impact assessment and a control mapping.
- The validator now checks every folder under `examples/` with the same rules, and the register health report can be run on any of them.
- An ISO/IEC 42001 evidence checklist (`templates/iso42001-evidence-checklist.md`): one row per framework item with a short paraphrase, example evidence and an owner role.

## [1.0.0] - 2026-11-12

### Added

- First public release: control matrix mapping ISO/IEC 42001, the EU AI Act and NIST AI RMF, with templates, worked examples and a validator.
- Register health report (`tools/register_health.py`): nine date-aware rules over the inventory, risk register and incident log, with a generated example and 37 tests.
- Related work section linking the companion repositories.
- Community health files: security policy, code of conduct, issue forms and a pull request template.
- Citation metadata (`CITATION.cff`) so the repository can be cited from GitHub.
- Dependabot configuration for GitHub Actions.
- Requires Python 3.10 or later; CI tests it on current supported versions.
- See the README for scope, what has and has not been verified, and the roadmap.
