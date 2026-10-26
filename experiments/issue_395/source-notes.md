# Source audit for issue 395

## Runtime, inspected 2026-10-26

- https://github.com/G-Ivan-A/mango-ba-ai-runtime/blob/main/docs/kb/README.md
- https://github.com/G-Ivan-A/mango-ba-ai-runtime/blob/main/docs/kb/USAGE.md
- https://github.com/G-Ivan-A/mango-ba-ai-runtime/blob/main/docs/kb/MAP.json
- https://github.com/G-Ivan-A/mango-ba-ai-runtime/blob/main/taxonomy/products.yaml
- Completeness reference:
  https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/mango/2026-05-22-classification.md

README → MAP.documents → product_ids → sections_map → exact section is usable.
USAGE explicitly distinguishes routing classes from Atomic Function binding.
The current closed taxonomy declares three classes: contact-center, voice-ucaas,
analytics-reporting; only contact-center is in_slice. It names four hierarchy
levels but publishes no complete catalog of their concrete values. The reference
has 42 capabilities across product domains and separate commercial fields.
Therefore neither the three classes nor a classification rule establishes full
coverage. Prompts recheck the current version instead of hardcoding this snapshot.

USAGE allows escalation to the full catalog and source tiers. Issue 395 imposes
BA-controlled cross-product reading. The added block explicitly narrows that
retrieval route; normative constitution, circuit breakers and gates remain in force.

## Approval process and historical dialogue

PDF (one page), retrieved with authenticated curl and extracted with pypdf:
https://github.com/user-attachments/files/33892143/KK-289887877-231026-2259-652.pdf

The attachment is located via the existing process source:
https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-manual-process.md

The PDF provides A-IN → A-CORE → A-WORK inputs/outputs, delta requirements,
customer approval before technical design, estimates, UC traceability and returns.
It explicitly leaves acceptance definitions and final structure undetailed. Its
historical seven-section numbering differs from the current eight-section canon.
The site explains this distinction; it does not invent PDF definitions or replace
current standards with obsolete numbering. The existing gate contract selects the
PDF's open option of an early estimate; the page attributes that decision correctly.

Dialogue:
https://github.com/user-attachments/files/33964744/3.txt

Downloaded locally, then filtered by structure/acceptance/stage/delta terms before
reading. Relevant original line ranges: 288–309 (both tasks and retrieval),
601–640 (criteria with definitions, rather than a section-name list).
The assistant's line 623 attributes a metric definition to BABOK 10.23, which is
the glossary technique. The new page uses BABOK 6.2 for goals and observable outcomes,
labels the four-field goal check as an operationalization, and never repeats that
incorrect attribution. Source files were not copied wholesale or published.

## Scope

The task-specific restrictions are sequential: prompt additions first, site second.
CHANGELOG is an explicit exception. Minimal scripts/ and experiments/ additions
and two existing hash-test adaptations keep automated CI coverage and historical
byte comparisons executable. No standards, existing site section markup, gate,
password configuration, workflow, or external repository is edited.
