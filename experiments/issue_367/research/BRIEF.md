# Research brief — RUN-0070 (issue #367), L0 feasibility of ТЗ BCREQ-1115

Joint view of System analyst + BA + Tech Lead. Verdicts ONLY from SSOT facts; general LLM
knowledge and invented architecture are forbidden.

## SSOT (in priority order)
1. Tender template v4 ("ТЗ-тендеров-v4", highest priority, indisputable — what the Mango system
   definitely fulfils): `experiments/issue_367/tender_index.json` (п/п -> [page, text]; the text
   ends with " наличие" + maybe a following heading — quote only the part BEFORE "наличие").
   Pages 1-6 full text (incl. unnumbered general requirements on p.5): `/tmp/i367/tender_p1_6.txt`;
   whole text `/tmp/i367/tender.txt`.
2. KB: `/tmp/rt-main/docs/kb/<dir>/sections/*.md` (runtime commit 91406e43). Doc codes:
   ROBOTFIL=cov-robot-fil (voice robots + chat-bots), LK=mango-lk-manual, CC=mango-cc-manual,
   ROLES=rolevaya-model-vats, VPBXAPI=vpbx-api, MDAPI=mdialogi-api, QM=quality-management,
   SIPT=sip-trunk, SA-VATS-SCORE=speech-analytics/vats-offline-scoring, SA=speech-analytics/user-guide,
   SA-KATS=speech-analytics/kats, SA-SCORE=speech-analytics/offline-scoring, LKSSO=lk-vats-sso,
   INTB24/INTAMO/INTBPM/INT1C = CRM integrations, MTALKER-* = MANGO Talker app.
3. Web — ONLY Mango Office domains (mango-office.ru and subdomains), only if KB is silent. Avoid if possible.

## Verdict scale (column 3) — exactly one of
- `Да` — fully confirmed.
- `Частично` — only if the row splits into atomic parts, some confirmed and some not (name which).
- `Нет` — not confirmed / contradicts docs / needs development / no data ("Нет данных").
- `` (empty) — not a Mango product matter (contract/legal/organizational obligations of the customer,
  pure section headings that only introduce sub-items) -> "вне функционального контура".
If a requirement is ambiguous and can be read in Mango's favour, raise the verdict and STATE the
interpretation explicitly in `audit`.

Rules:
- Tender >90% rule: only R123 matches tender п/п 6.7 at >90% (Dice 0.933) -> `Да`, confirmed without
  justification, cite п/п. For every other row tender items may be cited as supporting components
  (<90%): put a verbatim quote and give a probabilistic feasibility estimate in `audit`
  (e.g. "Вероятностная оценка по компонентам шаблона v4: высокая (~90%)").
- Prefer KB citations; add tender items where they cover the row.
- Base-engine rule "Да (базовая функция Yandex SpeechKit)" is allowed only for speech analytics /
  robots and only with an official vendor source — the KB/Mango domains do not contain one, so do NOT
  use it (just note when SpeechKit is mentioned).
- Do not substitute a similar-but-different feature (e.g. QM blank ≠ SA checklist); say "не подменять".
- Overpromising risks (limits, paid options, required modules/tariffs) must be stated in `audit`.

## Output (write ONLY your JSON file, do not touch any other file in the repo)
JSON object keyed by row id ("R081"...), each value:
{
  "verdict": "Да" | "Частично" | "Нет" | "",
  "why":   "Short comment in Russian with footnote markers [1], [2] ... placed where the source link goes
            (the generator inserts the link right after each marker). For no data write 'Нет данных: ...'.
            For headings: 'Раздел-заголовок к пп. ... (оцениваются отдельно) — вне функционального контура.'",
  "refs":  ["kb:ROBOTFIL/09-kartochka-robota.md", "tv4:2.16.4", "portal:<url>|<page title>"],   // ref i <-> marker [i+1]
  "quotes":["verbatim quote from ref 1", "verbatim quote from ref 2"],   // same length as refs
  "audit": "Russian critic-gate comment: trace check, overpromising risks, interpretation. Use exactly
            'OK' if there are no issues."
}
Quotes MUST be copied verbatim (whitespace may differ) from the referenced KB section body or the
tender item text, 30-250 chars, no «» inside, no '|' characters. Use `…` only to join two verbatim
fragments of the SAME ref. Every row id in your range must be present. Write the comment and audit
in Russian. Keep `why` ≤ 300 chars, `audit` ≤ 300 chars.
Validate your JSON with `python3 -m json.tool` and check each quote with grep before finishing.
