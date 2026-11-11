# Research brief — RUN-0093 (issue #482, задача BCREQ-1140), L0 feasibility of «ТЗ газификация ХХХ области.pdf»

Joint view of System analyst + BA + Tech Lead. Verdicts ONLY from SSOT facts; general LLM
knowledge and invented architecture are forbidden. Do not guess how the system works inside.

## Source
PDF of 33 pages with Word tracked changes. Two documents:
- Doc 1 (pp.4–31) — telephony / contact-centre TZ built on the Mango tender template v4
  (same numbering 1.x…12.x). Most rows match v4 > 90 % and are generated automatically.
- Doc 2 (pp.32–33) — embedded TZ «на оказание услуг по автоматизации рабочих процессов по
  выполнению технического обслуживания (ТО) внутридомового (ВДГО) и внутриквартирного (ВКГО)
  газового оборудования, а также выполнения ремонтных заявок». The customer is a regional gas
  distribution company; «Исполнитель» = the supplier (Mango Office), «Заказчик» = the customer,
  «Клиент» = the customer's subscriber (gas consumer), «бригада» / «работник Заказчика» = the
  customer's field staff. «Этикетка» = a service that shows the called person that the call
  comes from the customer (caller-name display) — check SSOT for a Mango analogue, do not assume.

Your rows: `experiments/issue_482/research/<BATCH>_rows.txt` (TSV: id, №, requirement text
after accepting tracked changes (line breaks shown as `<br>`), visible text with deletions
`~~…~~` (only when different), page). Assess the ACCEPTED text (3rd column).
Full list (context): `experiments/issue_482/source_transcription.json` (rows: id, №, visible,
page, accepted, «Требуемое значение», doc).

## SSOT (in priority order)
1. Tender template v4 («ТЗ-тендеров-v4», highest priority, indisputable — what the Mango system
   definitely fulfils): `experiments/issue_367/tender_index.json` (п/п -> [page, text]; the text
   ends with " наличие" and sometimes the following item/heading is glued after it — quote only
   the item's own text BEFORE its final "наличие"; 2.14.8 contains 2.14.8.1 and 2.14.8.2, which
   are cited as `tv4:2.14.8.1` / `tv4:2.14.8.2`). Whole text by page: `/tmp/dl482/tz-v4.txt`.
   Unnumbered general requirements on p.5 are cited as `tv4:p5`.
   Key sections: 1.x (records, remote work), 2.x (VATS / contact centre: routing, queues,
   2.6 outbound calls / autodialer, statuses, monitoring, 2.14 text channels incl. 2.14.8 auto
   SMS, 2.15 WFM, 2.16 robots), 3.x (reports), 4.x admin, 8.x (integrations/API), 9.x (SaaS,
   availability). Search the index yourself (grep the JSON / tz-v4.txt).
   If a row is close to a template item but < 90 %, cite the template components with a verbatim
   quote and give a probabilistic estimate in `audit`
   (e.g. "Вероятностная оценка по компонентам шаблона v4: высокая (~90%)").
2. KB: `/tmp/rt-main/docs/kb/<dir>/sections/*.md` (runtime commit
   68ad8fcffd47439fc3051852d9a2fbbe23815855; `index.md` per dir lists sections). Doc codes
   (= `doc_code` in each section's frontmatter): CC=mango-cc-manual (contact centre, outbound
   campaigns / autodialer, reports), LK=mango-lk-manual (VATS personal account: numbers, SMS,
   «Текстовые коммуникации», MAX channel sections 187, 195–200), ROBOTFIL=cov-robot-fil (voice
   robots + chat-bots: outbound robot campaigns, HTTP requests, SMS from robot, reports),
   VPBXAPI=vpbx-api (VATS API: calls, SMS sending, statistics), APISC=api-server-client,
   MDAPI=mdialogi-api (Манго Диалоги: channels incl. MAX type 15), QM=quality-management,
   ROLES=rolevaya-model-vats, SIPT=sip-trunk, SA / SA-KATS / SA-SCORE / SA-VATS-SCORE =
   speech-analytics/*, LKSSO=lk-vats-sso, WB=wallboard, MTALKER-MOB / -QS / -ADM / -SET / -WORK =
   mtalker/*, INT1C / INTAMO / INTB24 / INTBPM / INTIDENT (CRM integrations — evidence only for
   their own CRM). Ref format: `kb:<DOC_CODE>/<section-file>.md`.
   Use `grep -ril` over `/tmp/rt-main/docs/kb` (обзвон, кампани, попыт, интервал, SMS, смс,
   шаблон, переменн, робот, HTTP, расписан, отчет, статистик, этикет, имя звонящего, АОН,
   определ, номер, MAX …).
3. Web — ONLY Mango Office domains (mango-office.ru and its subdomains), only if KB and tender are
   silent. Ref format `portal:<url>|<page title>`. The quote must be copied verbatim from the
   fetched page; record the exact URL. Prefer KB.

## Verdict scale (column 3) — exactly one of
- `Да` — fully confirmed (every atomic part).
- `Частично` — only if the row splits into atomic parts, some confirmed and some not (name which
  in `why`).
- `Нет` — not confirmed / contradicts docs / needs development / no data. No-data rows: `why`
  starts with "Нет данных: ..." and the verdict MUST be `Нет`.
- `` (empty) — "вне функционального контура": customer-side / contractual / organisational items
  that are not product functions (e.g. a statement about the customer's own staff). The `why` text
  must contain "вне функционального контура".
If a requirement is ambiguous and can be read in Mango's favour, raise the verdict and STATE the
interpretation explicitly in `audit` (start with "Трактовка в пользу Mango: ...").

Rules:
- Pure section headings are handled by the generator — NOT in your rows.
- Numeric conditions (volumes per day, 20 days / 1–3 days before, 3–4 attempts with 2–3 h
  intervals, within one hour, until 15:00, 3 time slots) are atomic parts: confirm each only by a
  literal SSOT statement (setting / parameter / limit). A volume («не менее 3000 вызовов в день»)
  is confirmed only by a stated capacity/limit; otherwise name it unconfirmed.
- Business logic of the customer (planning by 12 districts, brigades, geozones, shifts, free
  slots of brigades) is not a Mango product function unless SSOT literally describes it; a
  generic mechanism (API, robot HTTP request to an external system) means the scenario requires
  development/integration -> `Нет` or `Частично` with "требуется доработка/интеграция"; do not
  overpromise. Integration «по API программных модулей Исполнителя к базе данных Заказчика»:
  Mango provides APIs (VPBXAPI/APISC/robot HTTP requests) — the concrete integration with the
  customer DB is a project work; judge literally and state the interpretation.
- Messenger «МАХ» / «MAX» (rows of batch C): the source replaced WhatsApp with MAX in a v4
  item. The v4 item (> 90 % textually) confirms the WhatsApp version; MAX must be confirmed
  literally by SSOT FOR THE SPECIFIC FUNCTION of the row (channel connected to the single window,
  voice messages, call-tracking events, files, bot buttons, contact / geolocation reception,
  robots, MTalker app). Confirm every other atomic part from the v4 item (cite it). If MAX for that
  function is not confirmed -> `Частично` (name MAX as the unconfirmed part).
- Base-engine rule "Да (базовая функция Yandex SpeechKit)" is allowed only for speech analytics /
  robots and only with an official vendor source — the KB/Mango domains do not contain one, so do
  NOT use it.
- Do not substitute a similar-but-different feature (e.g. operator call ≠ robot call; SMS from the
  VATS personal account ≠ SMS triggered by a robot after a call; call history ≠ analytic report
  with the required breakdowns); say "не подменять". Check every atomic condition.
- Overpromising risks (limits, paid options, required modules/tariffs, separate products, project
  integration work) must be stated in `audit`.

## Output (write ONLY your JSON file `experiments/issue_482/research/<BATCH>.json`, do not touch any other file)
JSON object keyed by row id ("R323"...), each value:
{
  "verdict": "Да" | "Частично" | "Нет" | "",
  "why":   "Short comment in Russian with footnote markers [1], [2] ... placed where the source link goes
            (the generator inserts the link right after each marker). For no data write 'Нет данных: ...'.",
  "refs":  ["kb:ROBOTFIL/12-....md", "tv4:2.6.3.2", "tv4:p5", "portal:<url>|<page title>"],   // ref i <-> marker [i+1]
  "quotes":["verbatim quote from ref 1", "verbatim quote from ref 2"],   // same length as refs
  "audit": "Russian critic-gate comment: trace check, overpromising risks, interpretation. Use exactly
            'OK' if there are no issues."
}
Quotes MUST be copied verbatim (whitespace may differ) from the referenced KB section body (not the
frontmatter) or the tender item text, 30-250 chars, no «» characters inside, no '|' characters, no
`<br>`. Use `…` only to join two verbatim fragments of the SAME ref. Every row id in your file must be
present. Every `Да`/`Частично` row needs at least one ref; a `Нет` row needs a ref when it
contradicts a document (no-data rows may have none). Every marker [i] in `why` must have refs[i-1],
and every ref must have its marker. Write the comment and audit in Russian. Keep `why` ≤ 300 chars,
`audit` ≤ 300 chars. Do not use the '|' character anywhere.
Validate your JSON with `python3 -m json.tool` and check each quote with grep before finishing.
