# Research brief — RUN-0072 (issue #371, задача 1117), L0 feasibility of «Телефония ТЗ 0710 1026 года»

Joint view of System analyst + BA + Tech Lead. Verdicts ONLY from SSOT facts; general LLM
knowledge and invented architecture are forbidden.

Customer document: «Телефония ТЗ 0710 1026 года в анализ.pdf» — tender ТЗ «Предоставление доступа к
программному обеспечению расширенной IP-телефонии» (VATS + contact centre: up to 500 telephony users,
desktop app for up to 55 concurrent operators/supervisors, own CRM, GrandStream PBX via SIP trunk,
customer's own speech analytics service). Rows R001–R097 (sections 1–7 and Приложение 2).
Your rows: `experiments/issue_371/research/<BATCH>_rows.txt` (TSV: id, №, requirement, page).
Full list (context; read neighbouring rows to understand bullets under a heading):
`experiments/issue_371/source_transcription.json`.
Glossary of the ТЗ (not assessed, context only): the `excluded` list in the same JSON
(«Десктопное приложение – омниканальное приложение … (MACOS,WIN,LINUX)», «Система», «ВАТС», «Контроль качества» etc.).

## SSOT (in priority order)
1. Tender template v4 («ТЗ-тендеров-v4», highest priority, indisputable — what the Mango system
   definitely fulfils): `experiments/issue_367/tender_index.json` (п/п -> [page, text]; the text
   ends with " наличие" + maybe a following heading — quote only the part BEFORE "наличие").
   Whole text by page: `/tmp/dl371/tender.txt`.
   Unnumbered general requirements on p.5 («2. Общие требования к оказанию услуг Исполнителем»:
   24 h/day operation, quarterly availability ≥ 99,9 %, ≤ 4 h/month maintenance windows, Russian
   software registry) are cited as `tv4:p5`.
   Key items: 9.1 (SaaS model, cloud software on servers in RF), 9.2 (availability 99,9 %),
   9.3 (RTO ≤ 240 min), 9.4 (RPO ≤ 180 min), section 4 (support), sections 2.x (VATS / contact centre,
   2.14 text channels, 2.15 WFM planning 2.15.1–2.15.20 (forecast, schedules, shift exchange, notifications), 2.16 robots), 3.x (speech analytics), 8.x (integrations/API),
   10.x–11.x (security, logging), 12.x (records). Search the index yourself.
   Similarity of every row to tender items: `experiments/issue_371/tender_similarity.json`
   (rid -> [raw, п/п, core, п/п, dice, п/п]). Rows with a metric > 0,90 (rule «>90 % -> Да, confirm by
   the п/п number without further justification»): R029 -> 2.2, R030 -> 2.16.10 (core 0,911),
   R032 -> 1.2, R034 -> 2.14.28, R035 -> 2.14.35. For these rows: verdict `Да`, `why` = "Совпадение с
   шаблоном ТЗ-тендеров-v4 > 90 % (п/п X) [1]", ref `tv4:X`, quote = item text before "наличие",
   audit = similarity figure + any literal difference worth noting (e.g. "FTS" vs "FTPS").
   For all other rows the rule does not apply; tender items are cited as supporting components with
   a verbatim quote and a probabilistic estimate in `audit`
   (e.g. "Вероятностная оценка по компонентам шаблона v4: высокая (~90%)").
2. KB: `/tmp/rt-main/docs/kb/<dir>/sections/*.md` (runtime commit 91406e43; `index.md` per dir
   lists sections). Doc codes: ROBOTFIL=cov-robot-fil (voice robots + chat-bots), LK=mango-lk-manual,
   CC=mango-cc-manual (contact centre incl. «График работы», «Планирование входящих», «Контроль
   сотрудников», reports), ROLES=rolevaya-model-vats, VPBXAPI=vpbx-api, MDAPI=mdialogi-api,
   QM=quality-management, SIPT=sip-trunk, SA-VATS-SCORE=speech-analytics/vats-offline-scoring,
   SA=speech-analytics/user-guide, SA-KATS=speech-analytics/kats, SA-SCORE=speech-analytics/offline-scoring,
   LKSSO=lk-vats-sso, INTB24=integration-bitrix24, INTAMO=integration-amocrm, INTBPM=integration-bpmsoft,
   INT1C=integration-1c, MTALKER-*=mtalker (desktop/mobile app «MANGO Talker»; check the `doc_code` in
   each section's frontmatter and use it). Ref format: `kb:<DOC_CODE>/<section-file>.md`.
   Use grep -ril over `/tmp/rt-main/docs/kb` for keywords (Astra, macOS, Linux, iOS, Android, MAX,
   Авито, статус, смен, прогноз, FTP, SFTP, SIP, транскриб, API, черн, ACD …).
3. Web — ONLY Mango Office domains (mango-office.ru and its subdomains), only if KB and tender are
   silent. Avoid if possible. Ref format `portal:<url>|<page title>`. The quote must be copied
   verbatim from the fetched page; record the exact URL.

## Verdict scale (column 3) — exactly one of
- `Да` — fully confirmed.
- `Частично` — only if the row splits into atomic parts, some confirmed and some not (name which).
- `Нет` — not confirmed / contradicts docs / needs development / no data ("Нет данных: ...").
- `` (empty) — not a Mango product matter -> "вне функционального контура": pure section headings
  that only introduce sub-items (incl. «3.2. Система должна:», «3.17. API должно содержать…:» is NOT
  pure if it carries content — judge), the «Не оценивается» rows (the customer itself excluded the
  section from assessment: why = "Раздел помечен заказчиком «Не оценивается» — вне функционального
  контура."), customer-side/contractual obligations (appointing a contact person within 1 day, SLA
  regulation approval terms, acceptance procedure, references to the Contract/appendices, legal
  territory clauses), service/consulting items that are not product functions.
If a requirement is ambiguous and can be read in Mango's favour, raise the verdict and STATE the
interpretation explicitly in `audit`.

Rules:
- Mango is delivered as SaaS (tv4 9.1). Requirements contradicting that -> `Нет` with tv4 9.1 quote.
- Numeric service levels: compare with tv4 (99,9 % per quarter -> tv4:p5 / 9.2 -> Да; RTO 240 min vs a
  required 120 min recovery -> SSOT guarantees only 240 -> `Нет`/`Частично` with the explicit numbers;
  15-minute reaction time not in SSOT -> "Нет данных"). Support items: check tv4 section 4.
- Integrations with third-party systems that have no ready connector in SSOT (customer's own CRM,
  customer's own speech-analytics service, GrandStream PBX): check whether a generic mechanism exists
  (VPBXAPI, MDAPI, SIPT, HTTP requests — tv4 8.x). If only a generic API exists, the concrete integration
  needs development on the customer/integrator side -> verdict per rule "required development = Нет",
  unless the requirement can reasonably be read as "the platform provides an API/SIP trunk for
  integration" (then raise and state the interpretation). «полноценное отображение всего функционала
  [внешнего сервиса] внутри десктопного приложения» is NOT confirmable by an API alone. Do not overpromise.
- Platform lists (MACOS / WINDOWS / Astra Linux; iOS / Android): confirm each OS separately; an OS absent
  in SSOT -> that atomic part is not confirmed (-> `Частично`). «бесплатного мобильного приложения» —
  confirm the price only from SSOT, otherwise flag in audit.
- Base-engine rule "Да (базовая функция Yandex SpeechKit)" is allowed only for speech analytics /
  robots and only with an official vendor source — the KB/Mango domains do not contain one, so do NOT
  use it.
- Do not substitute a similar-but-different feature (e.g. QM blank ≠ SA checklist; a 15-minute
  planning grid ≠ a 15-minute minimum exchange interval); say "не подменять". Check every atomic
  condition of a row (e.g. exchange approval by BOTH employees AND the supervisor vs tv4 2.15.18).
- Overpromising risks (limits, paid options, required modules/tariffs) must be stated in `audit`.
- Messenger «МАХ» (MAX) — confirm only if SSOT literally mentions MAX; tv4 2.14 lists Telegram/WhatsApp,
  not MAX. «иные каналы … используемые Заказчиком» is open-ended -> not confirmable as a whole.

## Output (write ONLY your JSON file `experiments/issue_371/research/<BATCH>.json`, do not touch any other file)
JSON object keyed by row id ("R024"...), each value:
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
Every marker [i] in `why` must have refs[i-1], and every ref must have its marker.
Write the comment and audit in Russian. Keep `why` ≤ 300 chars, `audit` ≤ 300 chars.
Validate your JSON with `python3 -m json.tool` and check each quote with grep before finishing.
