# Research brief — RUN-0071 (issue #369), L0 feasibility of ТЗ BCREQ-1116

Joint view of System analyst + BA + Tech Lead. Verdicts ONLY from SSOT facts; general LLM
knowledge and invented architecture are forbidden.

Two customer documents (pharmacy chain contact centre, 25→40→50 concurrent operators):
- `DOC` — «ТЕХНИЧЕСКОЕ ЗАДАНИЕ.doc», rows D001–D125 (sections 1–2.7, Приложение 1 SLA table,
  Приложение 2 availability terms). Table rows are cells joined by `<br>` (first cell = parameter/system).
- `XLSX` — «Требования к ПО КЦ (4).xlsx», rows X001–X074 (column A of sheet «функционал»; the
  customer expects «да/нет» per row; bold rows = group headings, `|b` in the loc column).
Your rows: `experiments/issue_369/research/<BATCH>_rows.txt` (TSV: id, №, requirement, loc).
Full list of both documents (context): `experiments/issue_369/source_transcription.json`.

## SSOT (in priority order)
1. Tender template v4 («ТЗ-тендеров-v4», highest priority, indisputable — what the Mango system
   definitely fulfils): `experiments/issue_367/tender_index.json` (п/п -> [page, text]; the text
   ends with " наличие" + maybe a following heading — quote only the part BEFORE "наличие").
   Whole text by page: `/tmp/i369/tender.txt`; pages 1-6: `/tmp/i369/tender_p1_6.txt`.
   Unnumbered general requirements on p.5 («2. Общие требования к оказанию услуг Исполнителем»:
   24 h/day operation, quarterly availability ≥ 99,9 %, ≤ 4 h/month maintenance windows, Russian
   software registry) are cited as `tv4:p5`.
   Key items for this ТЗ: 9.1 (SaaS model, cloud software on servers in RF — i.e. Mango is NOT an
   on-premise product), 9.2 (availability 99,9 %), 9.3 (RTO ≤ 240 min), 9.4 (RPO ≤ 180 min),
   section 4 (support), sections 2.x (VATS / contact centre), 3.x (speech analytics), 8.x (integrations),
   10.x–11.x (security, logging), 12.x (records).
   Similarity of every row to tender items: `experiments/issue_369/tender_similarity.json`
   (rid -> [raw, п/п, core, п/п, dice, п/п]) — NO row reaches 90 %, so the ">90 % -> Да without
   justification" rule does not apply anywhere; tender items are cited as supporting components with
   a verbatim quote and a probabilistic estimate in `audit`
   (e.g. "Вероятностная оценка по компонентам шаблона v4: высокая (~90%)").
2. KB: `/tmp/rt-main/docs/kb/<dir>/sections/*.md` (runtime commit 91406e43; `index.md` per dir
   lists sections). Doc codes: ROBOTFIL=cov-robot-fil (voice robots + chat-bots), LK=mango-lk-manual,
   CC=mango-cc-manual, ROLES=rolevaya-model-vats, VPBXAPI=vpbx-api, MDAPI=mdialogi-api,
   QM=quality-management, SIPT=sip-trunk, SA-VATS-SCORE=speech-analytics/vats-offline-scoring,
   SA=speech-analytics/user-guide, SA-KATS=speech-analytics/kats, SA-SCORE=speech-analytics/offline-scoring,
   LKSSO=lk-vats-sso, INTB24=integration-bitrix24, INTAMO=integration-amocrm, INTBPM=integration-bpmsoft,
   INT1C=integration-1c, MTALKER-*=mtalker (check the `doc_code` in each section's frontmatter and use it).
   Ref format: `kb:<DOC_CODE>/<section-file>.md`.
3. Web — ONLY Mango Office domains (mango-office.ru and subdomains, mango.ru), only if KB and tender are
   silent. Avoid if possible. Ref format `portal:<url>|<page title>`.

## Verdict scale (column 3) — exactly one of
- `Да` — fully confirmed.
- `Частично` — only if the row splits into atomic parts, some confirmed and some not (name which).
- `Нет` — not confirmed / contradicts docs / needs development / no data ("Нет данных: ...").
- `` (empty) — not a Mango product matter -> "вне функционального контура": pure section/group headings
  that only introduce sub-items, table header rows (e.g. «Параметр<br>Значение»), project goals that are
  business outcomes of the customer, customer-side/contractual obligations and liability terms
  (warranty period counted from acts, exclusions from SLA calculation, how incidents are attributed),
  questions to the bidder that are not product functions (e.g. implementation deadline).
If a requirement is ambiguous and can be read in Mango's favour, raise the verdict and STATE the
interpretation explicitly in `audit`.

Rules:
- Mango is delivered as SaaS (tv4 9.1). Requirements of perpetual licences, installation on the
  customer's infrastructure, storing data/records only inside the customer's perimeter, an isolated
  network segment contradict the SSOT -> `Нет` (or `Частично` when the row also contains confirmable
  atomic parts). Quote tv4 9.1 as the contradicting fact. Do not invent on-premise editions.
- Numeric service levels: compare with tv4 (99,9 % ≥ 98 % -> Да; RTO 240 min ≤ 5 раб. ч. -> Да;
  RPO 180 min ≤ 3 раб. д. -> Да). Support/incident response times, incident percentages not present in
  SSOT -> `Нет` with "Нет данных: ...".
- Integrations with third-party systems that have no ready connector in SSOT (Mindbox, Talkme,
  stream telecom, «Робот Мия», customer's 1С configuration, site): check whether a generic mechanism
  exists (VPBXAPI, MDAPI, HTTP requests from robot/IVR — tv4 8.6, 8.7, INT1C). If only a generic API
  exists, the concrete integration needs development on the customer/integrator side -> verdict per
  rule "required development = Нет", unless the requirement can reasonably be read as "the platform
  provides an API for integration" (then raise and state the interpretation). Do not overpromise.
- Base-engine rule "Да (базовая функция Yandex SpeechKit)" is allowed only for speech analytics /
  robots and only with an official vendor source — the KB/Mango domains do not contain one, so do NOT
  use it (just note when SpeechKit is mentioned).
- Do not substitute a similar-but-different feature (e.g. QM blank ≠ SA checklist); say "не подменять".
- Overpromising risks (limits, paid options, required modules/tariffs) must be stated in `audit`.

## Output (write ONLY your JSON file `experiments/issue_369/research/<BATCH>.json`, do not touch any other file)
JSON object keyed by row id ("D024"...), each value:
{
  "verdict": "Да" | "Частично" | "Нет" | "",
  "why":   "Short comment in Russian with footnote markers [1], [2] ... placed where the source link goes
            (the generator inserts the link right after each marker). For no data write 'Нет данных: ...'.
            For headings: 'Заголовок раздела: вводит перечень подпунктов ниже, каждый оценивается отдельной
            строкой — вне функционального контура.' For other empty verdicts the text must contain
            'вне функционального контура'.",
  "refs":  ["kb:CC/21-obrascheniya.md", "tv4:2.16.4", "tv4:p5", "portal:<url>|<page title>"],   // ref i <-> marker [i+1]
  "quotes":["verbatim quote from ref 1", "verbatim quote from ref 2"],   // same length as refs
  "audit": "Russian critic-gate comment: trace check, overpromising risks, interpretation. Use exactly
            'OK' if there are no issues."
}
Quotes MUST be copied verbatim (whitespace may differ) from the referenced KB section body or the
tender item text, 30-250 chars, no «» inside, no '|' characters. Use `…` only to join two verbatim
fragments of the SAME ref. Every row id in your range must be present. Every `Да`/`Частично` row needs
at least one ref; a `Нет` row needs a ref when it contradicts a document (no-data rows may have none).
Write the comment and audit in Russian. Keep `why` ≤ 300 chars, `audit` ≤ 300 chars.
Validate your JSON with `python3 -m json.tool` and check each quote with grep before finishing.
