# Research brief — RUN-0076 (issue #382, задача BCREQ-1125), L0 feasibility of five CSV requirement lists

Joint view of System analyst + BA + Tech Lead. Verdicts ONLY from SSOT facts; general LLM
knowledge and invented architecture are forbidden.

Customer context: the customer runs **BPMsoft** (CRM) and selects a contact-centre platform plus a
**connector** between it and BPMsoft. In the requirement texts:
- «Коннектор» / «CTI» / «виджет» = the Mango Office ↔ BPMsoft integration (KB doc `INTBPM`,
  `/tmp/rt-main/docs/kb/integration-bpmsoft`) and the Mango contact centre behind it.
- «Решение» = the Mango Office platform (VATS + contact centre `CC` + Манго Диалоги `MDAPI` +
  speech analytics `SA*` + quality management `QM` + MANGO Talker `MTALKER-*` + robots `ROBOTFIL`).
- «интеракция» = any communication (call, chat, e-mail, messenger message); «ОС» = обратная связь
  (feedback after a quality assessment); «SL» = service level; «матрица оценки» = evaluation form.

Files (all five assessed, one report block each):
- KC1 «КЦ Требования к коннектору.csv» — requirements to the BPMsoft connector (rows KC1-001..065);
- KC2 «КЦ Требования КЦ.csv» — requirements to the contact centre (KC2-001..075);
- FT1 «ФТ - Расшифровка отчетность.csv» — reporting (FT1-001..010);
- FT2 «ФТ - Расшифровки оценка звонков.csv» — call quality assessment (FT2-001..011);
- FT3 «ФТ - Функциональные критерии.csv» — functional criteria (FT3-001..037, incl. two section
  headings FT3-009 «Функционал руководителя» and FT3-023 «Функциональные критерии - To Be»).

Your rows: `experiments/issue_382/research/<BATCH>_rows.txt` (TSV: id, №, requirement (line breaks
shown as `<br>`; for КЦ files «Группа<br>Конкретное требование»), source assessment).
Full list (context): `experiments/issue_382/source_transcription.json`.

**The 4th TSV column («Оценка Внутр» / «Комментарий поставщика») is the customer's/vendor's own
previous assessment. It is shown in the report as-is but is NOT evidence. Never cite it, never
copy its verdict; derive your verdict from SSOT only.** If SSOT contradicts it (e.g. it says «Есть»
but SSOT is silent), state this in `audit`.

## SSOT (in priority order)
1. Tender template v4 («ТЗ-тендеров-v4», highest priority, indisputable — what the Mango system
   definitely fulfils): `experiments/issue_367/tender_index.json` (п/п -> [page, text]; the text
   ends with " наличие" + maybe a following heading — quote only the part BEFORE "наличие").
   Whole text by page: `/tmp/tv4/tender.txt`.
   Unnumbered general requirements on p.5 («2. Общие требования к оказанию услуг Исполнителем»)
   are cited as `tv4:p5`.
   Key sections: 1.x (records, remote work), 2.x (VATS / contact centre: routing, queues, skills,
   statuses, monitoring, reports, 2.14 text channels, 2.15 WFM, 2.16 robots), 3.x (speech analytics),
   8.x (integrations/API), 9.x (SaaS, availability), 10.x–11.x (security, logging), 12.x (records).
   Search the index yourself (grep the JSON / tender.txt).
   Similarity of every row to tender items: `experiments/issue_382/tender_similarity.json`.
   **No row exceeds 0,90 on any metric (max 0,716)** — the «>90 % -> Да + п/п» rule does NOT apply
   to any row; every row needs a full justification. Tender items are cited as supporting
   components with a verbatim quote; you may add a probabilistic estimate in `audit`
   (e.g. "Вероятностная оценка по компонентам шаблона v4: высокая (~90%)").
2. KB: `/tmp/rt-main/docs/kb/<dir>/sections/*.md` (runtime commit 91406e43; `index.md` per dir
   lists sections). **Priority: `integration-bpmsoft` (INTBPM)** — always check it first for KC1 rows
   and for every row that mentions BPMsoft. Other doc codes: CC=mango-cc-manual (contact centre,
   reports, monitoring, statuses, «Контроль сотрудников»), LK=mango-lk-manual, ROLES=rolevaya-model-vats,
   VPBXAPI=vpbx-api, MDAPI=mdialogi-api (Манго Диалоги: chats, messengers, e-mail channel),
   QM=quality-management, SIPT=sip-trunk, SA=speech-analytics/user-guide, SA-KATS=speech-analytics/kats,
   SA-SCORE=speech-analytics/offline-scoring, SA-VATS-SCORE=speech-analytics/vats-offline-scoring,
   LKSSO=lk-vats-sso, INTB24/INTAMO/INT1C (other CRM integrations — NOT evidence for BPMsoft),
   ROBOTFIL=cov-robot-fil (voice robots + chat-bots), MTALKER-*=mtalker (check the `doc_code` in
   each section's frontmatter and use it). Ref format: `kb:<DOC_CODE>/<section-file>.md`.
   Use `grep -ril` over `/tmp/rt-main/docs/kb` for keywords (BPMsoft, статус, виджет, Диалоги,
   WhatsApp, Telegram, MAX, почт, e-mail, шаблон, бот, эмодзи, реакц, прочитан, доставлен, очеред,
   навык, мониторинг, SLA, запис, расшифр, транскриб, оценк, чек-лист, бланк, Excel, выгрузк,
   черн, автоответ, IVR, WFM, смен, экран …).
   Inside INTBPM the index covers: statuses (sections ~61–65), manual binding (66–69), contact/lead
   creation (20), missed calls (21–22), click-to-call (38), transfers/hold (115–119), call recordings
   (123), speech analytics texts/summaries (40–50), WhatsApp/Манго Диалоги (103–107), outbound
   campaigns (108–111). Read `index.md` yourself; numbers are approximate.
3. Web — ONLY Mango Office domains (mango-office.ru and its subdomains), only if KB and tender are
   silent. Avoid if possible. Ref format `portal:<url>|<page title>`. The quote must be copied
   verbatim from the fetched page; record the exact URL.

## Verdict scale (column 3) — exactly one of
- `Да` — fully confirmed (every atomic part).
- `Частично` — only if the row splits into atomic parts, some confirmed and some not (name which).
- `Нет` — not confirmed / contradicts docs / needs development / no data. No-data rows: `why` starts
  with "Нет данных: ..." and the verdict MUST be `Нет`.
- `` (empty) — "вне функционального контура": pure section headings (FT3-009, FT3-023: why =
  "Заголовок раздела: вводит перечень требований ниже, каждое оценивается отдельной строкой — вне
  функционального контура."), customer-side / contractual / organisational items that are not
  product functions. The `why` text must contain "вне функционального контура".
If a requirement is ambiguous and can be read in Mango's favour, raise the verdict and STATE the
interpretation explicitly in `audit` (start with "Трактовка в пользу Mango: ...").

Rules:
- Connector rows (KC1) are about the **ready Mango ↔ BPMsoft integration**. Confirm them only from
  INTBPM (or tender 8.x if it literally covers the BPMsoft connector). A capability that exists in the
  Mango contact centre / Манго Диалоги but is NOT documented as passed to / shown in BPMsoft via the
  integration does not confirm a connector row -> `Нет` (or `Частично` for multi-part rows) and say
  "в SSOT интеграции с BPMsoft не описано". A generic API (VPBXAPI/MDAPI) means the connector feature
  requires development -> `Нет` ("требуется доработка"), unless the wording can reasonably be read as
  "the platform provides an API" (then raise + state the interpretation). Do not overpromise.
- «Указать какие» rows (KC1-006..010): list the events/fields that SSOT literally confirms in `why`.
- Channel rows: voice; chat (Манго Диалоги «Чат на сайте»); e-mail (MDAPI type 8 «Электронная почта»
  exists in Манго Диалоги — check whether the CC/operator side really handles it); messengers
  (Telegram, WhatsApp, VK, Avito in MDAPI; tv4 2.14); **Messenger «МАХ» (MAX) — confirm only if SSOT
  literally mentions MAX** (grep -rn "MAX\|МАКС\|Макс" — check it is the messenger, not "maximum").
- «в едином интерфейсе администратора» — confirm only if SSOT shows the setting is done in the same
  admin interface (ЛК / web interface of the contact centre); if the setting lives in a different
  product (Манго Диалоги vs VATS ЛК) say so — this is a literal condition, judge each row.
- Chat-UI rows (reactions, emoji, markdown bold/italic/lists, edit after sending, spell check, typing
  indicator, read/delivered status, unread counter, auto-close timeout, reconnection) — confirm each
  only with a literal SSOT statement; do not infer from "chat exists".
- Base-engine rule "Да (базовая функция Yandex SpeechKit)" is allowed only for speech analytics /
  robots and only with an official vendor source — the KB/Mango domains do not contain one, so do NOT
  use it.
- Do not substitute a similar-but-different feature (e.g. QM blank ≠ SA checklist; screen recording ≠
  call recording; internal chat ≠ customer chat); say "не подменять". Check every atomic condition.
- Overpromising risks (limits, paid options, required modules/tariffs, separate products) must be
  stated in `audit`.
- FT3-018 / FT3-021 refer to the FT1 / FT2 attachments: assess them as umbrella rows (verdict follows the
  referenced block; say "см. блок «…»" and cite at least one SSOT source).

## Output (write ONLY your JSON file `experiments/issue_382/research/<BATCH>.json`, do not touch any other file)
JSON object keyed by row id ("KC1-001"...), each value:
{
  "verdict": "Да" | "Частично" | "Нет" | "",
  "why":   "Short comment in Russian with footnote markers [1], [2] ... placed where the source link goes
            (the generator inserts the link right after each marker). For no data write 'Нет данных: ...'.",
  "refs":  ["kb:INTBPM/61-....md", "tv4:2.14.28", "tv4:p5", "portal:<url>|<page title>"],   // ref i <-> marker [i+1]
  "quotes":["verbatim quote from ref 1", "verbatim quote from ref 2"],   // same length as refs
  "audit": "Russian critic-gate comment: trace check, overpromising risks, interpretation. Use exactly
            'OK' if there are no issues."
}
Quotes MUST be copied verbatim (whitespace may differ) from the referenced KB section body (not the
frontmatter) or the tender item text, 30-250 chars, no «» characters inside, no '|' characters, no
`<br>`. Use `…` only to join two verbatim fragments of the SAME ref. Every row id in your range must be
present. Every `Да`/`Частично` row needs at least one ref; a `Нет` row needs a ref when it
contradicts a document (no-data rows may have none). Every marker [i] in `why` must have refs[i-1],
and every ref must have its marker. Write the comment and audit in Russian. Keep `why` ≤ 300 chars,
`audit` ≤ 300 chars. Do not use the '|' character anywhere.
Validate your JSON with `python3 -m json.tool` and check each quote with grep before finishing.
