# Human oversight checklist

> General information only, not legal advice. Fernhill Building Supplies Ltd is a fictional company and every example in this file is invented.

Supports controls TK-LIF-09 (human oversight), TK-LIF-10 (safe failure and fallback) and TK-USE-04 (appeals, complaints and redress). Related framework items: ISO/IEC 42001 A.9.2, EU AI Act Art 14 and Art 26(2), NIST AI RMF MAP 3.5, MAP 3.4 and GOVERN 3.2.

## Purpose

Putting a person "in the loop" does not by itself make a system safe. If the person lacks time, information, training or authority, oversight is a label and not a control. This checklist tests whether oversight works in practice.

Use it for any system whose output affects a person, and always for systems in a high-risk tier. Art 14 sets design requirements for high-risk systems, and Art 26(2) requires deployers to give oversight to people with the necessary competence, training and authority. The checklist is a practical test of those ideas and is not a legal compliance test.

## How to use it

1. Complete it before go-live, with the system owner and the person who will carry out oversight. Do not complete it from a desk.
2. Observe a real or simulated session. Watch what the reviewer does, not what the procedure says.
3. Mark each item **Yes**, **Partly** or **No** and record evidence.
4. Any **No** on a starred item (*) blocks go-live until fixed or formally accepted by the approver.
5. Repeat after significant changes and at least annually.

## Checklist

### A. People and authority

| Item | Yes / Partly / No | Evidence |
|---|---|---|
| Named roles carry out oversight, and cover for absence exists * | | |
| Reviewers have received training on the system, its limits and automation bias * | | |
| Reviewers have the authority to disagree with the system, with no penalty for doing so * | | |
| Reviewers have enough time per case to review properly | | |
| Workload and targets do not push reviewers to accept outputs without checking | | |

### B. Information available to the reviewer

| Item | Yes / Partly / No | Evidence |
|---|---|---|
| The reviewer can see the inputs the system used | | |
| The reviewer is shown confidence levels or uncertainty where they exist | | |
| The reviewer is told what the system cannot do (documented limits) | | |
| The reviewer can see why the system produced the output at a level useful for the decision | | |
| Known failure patterns are described in plain language | | |

### C. Ability to intervene

| Item | Yes / Partly / No | Evidence |
|---|---|---|
| The reviewer can override or ignore the output * | | |
| The reviewer can stop the system, and the stop control is tested * | | |
| A decision can be reversed after the fact | | |
| Overrides are recorded with a reason | | |
| Override rates are reviewed to detect both over-reliance (very low) and distrust (very high) | | |

### D. Affected people

| Item | Yes / Partly / No | Evidence |
|---|---|---|
| People are told that AI supports the decision where this matters to them | | |
| People can ask for a human review or an explanation * | | |
| Appeals are handled by someone who did not make the original decision | | |
| Appeals and their outcomes are logged and analysed | | |

### E. Fallback

| Item | Yes / Partly / No | Evidence |
|---|---|---|
| A manual process exists if the system is unavailable or switched off * | | |
| The manual process was tested within the last twelve months | | |
| Staff know who can authorise suspending the system | | |

### F. Result

| Item | Entry |
|---|---|
| Overall result | Ready / Ready with actions / Not ready |
| Actions and dates | |
| Approver (role) | |
| Date | |
| Next review | |

---

## Worked example: TalentLens CV shortlisting (fictional)

System FH-AI-002, reference FH-HO-002, tested on 2026-09-02 with the Recruitment lead during a simulated session of ten applications. Invented content.

| Section | Result | Observations |
|---|---|---|
| A People and authority | Partly | Five recruiters trained for one hour. The observation showed that two recruiters accepted the top ten rankings without opening the CVs. A target of 40 applications per hour had been set for the pilot |
| B Information | Partly | Reviewers see the score but not the factors behind it. Supplier asked to provide a factor view |
| C Intervention | Yes | Recruiters can move any applicant onto the shortlist. Overrides require a reason code. No automatic rejection exists |
| D Affected people | Partly | Careers page notice drafted but not yet live. Manual review route agreed |
| E Fallback | Yes | Recruiters can run the process without the tool. Last tested on 2026-09-02 |

**Overall result: Ready with actions.**

Actions:

1. Remove the throughput target for the pilot (HR Director, 2026-09-10). Done 2026-09-09.
2. Publish the careers page notice before go-live (Recruitment lead, 2026-09-13). Done 2026-09-12.
3. Obtain a factor view from the supplier (Procurement lead, 2026-12-11). Open. Tracked as part of risk FH-R-005.
4. Add a monthly check on override rates (HR Systems Analyst, 2026-10-15).

What the example shows: the written procedure said oversight existed. Observing a session revealed that the throughput target made real review unlikely. That finding led to a management decision that no document review would have produced.
