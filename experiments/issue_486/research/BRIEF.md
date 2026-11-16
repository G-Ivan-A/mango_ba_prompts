# Research brief — RUN-0094 v2.0 (issue #486): оценка исполнимости атомарных требований BCREQ-1199 v2

Issue #486 reworks RUN-0094 (issue #484): every source row with several requirements is split
into fragments, and each fragment is a separate report row with its own assessment. The
assessment rules are those of issue #484 **without changes**; read
`experiments/issue_484/research/BRIEF.md` (SSOT priority, KB doc codes, verdict scale, Skillaz
rule, base-engine rule, overpromising risks, card format, hard requirements). Only the
differences are listed here.

## Unit of assessment

- Your file `research/<BATCH>_rows.txt` lists fragments `### <fid> [req]` — the verbatim text of
  one report row (`decompose.py`). Assess **only the fragment's own wording**, not the whole
  source row. Lines `НЕ ОЦЕНИВАТЬ (lead|heading)` are headings, the generator fills them.
- `[req top]` — the generalising lead phrase of a complex requirement that is read as a
  top-level requirement (e.g. «Система должна предоставить функционал транскрибации и речевой
  аналитики:»). Assess what the phrase itself requires (the product/function exists, plus any
  own conditions such as «выгрузка в excel», «передача по API», «подтверждается демонстрацией»);
  its sub-items are assessed in their own rows — do not repeat them. Mention in `why` that the
  detailed items are assessed in the following rows of the same «№».
- `Частично` — only when the fragment's own wording splits into atomic parts (several functions,
  a function plus a numeric threshold, …) and only some are confirmed; name confirmed and
  unconfirmed parts: «Подтверждено: … [1]; не подтверждено: …». A fragment with one atomic
  part is `Да` or `Нет` (or empty when out of contour).
- Numeric thresholds remain separate atomic parts and are confirmed only by a literal SSOT
  statement (issue #484 rule).
- `| v4: п/п X (s)` — similarity of the fragment with the template item. If s > 0.9: verdict
  `Да`, `why` starts «Не требует обоснования: совпадение с ТЗ-тендеров-v4 > 90 % (п/п X) [1]»,
  ref `tv4:X` with a verbatim quote of the item; differences of wording (stricter conditions)
  go to `audit`.
- Organisational fragments (presentation/demonstration, implementations, references, licences,
  training, documentation on request, support process, fines, reaction/resolution terms) —
  empty verdict, `why` contains «вне функционального контура» (issue #484 rule).
- The prior card of the whole source row (RUN-0094 v1.0) is given after each row as material:
  its refs and quotes are already verified verbatim — reuse those relevant to the fragment, and
  search the SSOT for more when a fragment needs it. Do not copy a whole-row `why`: rewrite it
  for the fragment. Never use general LLM knowledge.

## Output

Write ONLY `experiments/issue_486/research/<BATCH>.json` — an object keyed by fid (exactly the
`### <fid>` of your rows file, every `req` fid, no others), values in the issue #484 card format
(`verdict`, `why`, `refs`, `quotes`, `audit`). Check with

    MANGO_BA_RUNTIME_MAIN=/tmp/runtime python3 -I experiments/issue_486/verify_cards.py <BATCH>

until it reports 0 discrepancies (расхождений: 0).
