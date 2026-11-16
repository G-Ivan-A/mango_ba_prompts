# Research brief — RUN-0094 (issue #484, задача BCREQ-1199 v2), L0 feasibility of «SoC_внешний 29-10.xlsx»

Joint view of System analyst + BA + Tech Lead. Verdicts ONLY from SSOT facts; general LLM
knowledge and invented architecture are forbidden. Do not guess how the system works inside.
Never substitute a similar-but-different feature for the required one.

## Source

Excel file of the customer (ВымпелКом / Билайн, HR recruiting contact centre) with two visible
sheets, assessed as two documents of one source:

- `Требования к системе` — 18 numbered requirements (№ 1–18) about the cloud telephony /
  contact-centre system: autodialing (incl. predictive), admin panel, integration with the
  recruiting system **Skillaz** (external third-party system of the customer), routing,
  reporting, numbering capacity, quality management, transcription and speech analytics, voice
  robots, operator work-schedule planning (WFM), call transfer.
- `SLA` — availability / support requirements and «Таблица 1: SLA тех поддержки».

Terms: «Исполнитель» = the supplier (Mango Office), «ВымпелКом»/«заказчик» = the customer,
«кандидат» = the person being called (job candidate), «оператор» = the customer's agent,
«кампания обзвона» = outbound campaign, «профиль должности»/«вакансия» = the customer's own
HR entities, Skillaz = the customer's recruiting system (a third-party product).
The source is the customer's OWN form, it is NOT built on the Mango tender template: only 7 of
137 atomic parts match a template item by more than 90 %. Therefore almost every verdict needs
an explicit SSOT citation.

Your rows: `experiments/issue_484/research/<BATCH>_rows.txt` — one block per row:
`### <row id>` then `№: <number>`, then the requirement text (line breaks shown as `<br>`), then
the atomic parts `[1] …` as split by `experiments/issue_484/atomize.py`, then, where it exists,
`v4: <atom no> ~ <п/п> (<max similarity>)` — a hint about the closest template item.
Full list of all rows (context): `experiments/issue_484/source_transcription.json`
(per sheet: `rows` = [row number, «№ пункта», «Требования», …]).

Assess the WHOLE row as one verdict, but justify it part by part (the atoms are the atomic
parts of the «Частично» rule).

## SSOT (in priority order)

1. **Tender template v4** («ТЗ-тендеров-v4», highest priority, indisputable — the list of
   requirements that the Mango product scope definitely fulfils):
   `experiments/issue_484/tender_items.txt` (TSV: п/п, page, text; the item text ends with
   «наличие» — the customer's demand for the function to exist; sometimes the next item or
   heading is glued after it, quote only the item's own text). Grep it first.
   Topics: 1.x call recording and remote work; 2.1–2.5 voice/text channels, own number pool,
   SIM cards, single window, conferences; 2.6 outbound single/mass communications (manual,
   callback, autodialer, predictive, campaigns, attempts, intervals, schedules, lists,
   answering-machine detection, blending — MANY sub-items 2.6.x); 2.7 local time; 2.8 intensity
   regulation; 2.9 number rotation; 2.10–2.11 stopping campaigns; 2.12 storage of records;
   2.13 quality control; 2.14 text channels; 2.15 WFM (schedule planning, sub-items 2.15.x);
   2.16 robots / IVR (sub-items 2.16.x); 2.18 speech analytics (sub-items 2.18.x); 2.19 the
   VATS-integrated communication app; 3.x statistics and reports; 4.x admin panel; 5.x operator
   workplace (АРМ, softphone, statuses, transfers); 6.x role model; 7.x performance;
   8.x API / integrations / LDAP / HTTP requests; 9.x SaaS, availability, RTO/RPO, protocols,
   remote work; 10.x authentication; 11.x documentation; 12.x encryption.
   Ref format: `tv4:2.6.3` (numbered item) or `tv4:p5` / `tv4:p5:3` (unnumbered general
   requirements on p.5).
   - Similarity > 90 % with a template item (the `v4:` hint in your rows file): the function is
     confirmed without further justification — write «Не требует обоснования: совпадение с
     ТЗ-тендеров-v4 > 90 % (п/п X) [n]» and cite the item.
   - Similarity < 90 %: you may still rely on the template's components — cite the item with a
     verbatim quote and give a probabilistic estimate in `audit`, e.g. «Вероятностная оценка по
     составляющим шаблона v4: высокая (~90 %)». Only the parts literally covered by the quoted
     item count as confirmed.
2. **KB**: `/tmp/runtime/docs/kb/<dir>/sections/*.md` (runtime repo `mango-ba-ai-runtime`,
   commit `68ad8fcffd47439fc3051852d9a2fbbe23815855`). Per-document `index.md` and
   `../maps/<doc>.toc.tsv` list the sections. Doc codes (= `doc_code` in a section's
   frontmatter) and directories:

   | code | dir | content |
   | --- | --- | --- |
   | CC | mango-cc-manual | Контакт-центр: ACD-группы, обзвоны/кампании, статусы операторов, мониторинг, отчёты ЦОВ, IVR |
   | LK | mango-lk-manual | ВАТС (справочник абонента): номера, запись разговоров, схемы распределения, чёрный список, SMS, текстовые коммуникации |
   | ROBOTFIL | cov-robot-fil | Робот Фил 2.0: голосовые роботы, сценарии, распознавание, HTTP-запросы, отчёты роботов |
   | QM | quality-management | Контроль качества: формы оценки, шкалы, выборки, апелляции, дашборды |
   | SA | speech-analytics/user-guide | Речевая аналитика: транскрибация, теги, словари, отчёты |
   | SA-KATS | speech-analytics/kats | Речевая аналитика & КАТС |
   | SA-SCORE | speech-analytics/offline-scoring | Офлайн скоринг (загрузка аудиофайлов) |
   | SA-VATS-SCORE | speech-analytics/vats-offline-scoring | ВАТС & офлайн скоринг |
   | WB | wallboard | Wallboard: онлайн-дашборды, период обновления |
   | ROLES | rolevaya-model-vats | Роли и права доступа |
   | VPBXAPI | vpbx-api | API Mango Office: статистика, звонки, управление |
   | APISC | api-server-client | API «Сервер-клиент» (WebSocket, события звонков) |
   | MDAPI | mdialogi-api | Манго Диалоги: API каналов |
   | LKSSO | lk-vats-sso | SSO: аутентификация и авторизация |
   | SIPT | sip-trunk | SIP TRUNK |
   | MTALKER-WORK / -ADM / -SET / -QS / -MOB | mtalker/* | приложение Mango Talker |
   | INT1C / INTAMO / INTB24 / INTBPM / INTIDENT | integration-* | интеграции с конкретными CRM (доказательство только для своей CRM) |

   Ref format: `kb:<DOC_CODE>/<section-file>.md` (e.g. `kb:CC/12-obzvony.md`).
   Search with `grep -ril` / `grep -rn` over `/tmp/runtime/docs/kb` (обзвон, кампани, предиктив,
   автоответчик, попыт, интервал, расписан, карусел, перебор номеров, блендинг, запись
   разговор, стерео, прослуш, суфл, перехват, чёрный список, транскриб, эмоц, молчан,
   перебива, график, статус, отчет, дашборд, API, SSO, oauth, oAuth, трансфер, перевод вызова …).
   The KB is a text extraction of the official Mango manuals — it is a trusted source, but DO
   NOT interpret it: only literal statements count.
3. **Web — ONLY Mango Office domains** (`docs.mango-office.ru`, `mango-office.ru` and
   subdomains), and only when the template and the KB are silent. Ref format
   `portal:<url>|<page title>`; the quote must be copied verbatim from the fetched page.
   Prefer the template and the KB. Do not use any other site.

## Verdict scale (column 3) — exactly one of

- `Да` — every atomic part of the row is confirmed by SSOT and needs no development.
- `Частично` — the row splits into atomic parts and only some of them are confirmed; in `why`
  name which parts are confirmed and which are not.
- `Нет` — not confirmed / contradicts the documentation / requires development / no data in the
  trusted sources. For a no-data row `why` MUST start with «Нет данных: …».
- `` (empty string) — «вне функционального контура»: the item is not a function of the Mango
  product at all (purely contractual, organisational, the customer's own obligations, the
  supplier's references/experience, or a table caption/header). The `why` text MUST contain
  «вне функционального контура».

If a requirement is ambiguous and can be read in Mango's favour, raise the verdict and state the
interpretation explicitly in `audit`, starting with «Трактовка в пользу Mango: …».

Rules:

- Numbers and thresholds are atomic parts of their own: «Abandon rate не более 5 %», «не менее
  80 % определённых автоответчиков», «не менее 95 % записанных звонков», «хранение не менее
  3 месяцев», «обновление раз в 5–15 секунд», «на каждые 15 минут», «отклонения до 5 %»,
  «доступность не ниже 98 %», «100 операторов», «~250 номеров», «за 2 месяца». A threshold is
  confirmed only by a literal SSOT statement (a stated limit, parameter, setting or SLA value);
  otherwise name it as unconfirmed — this usually makes the row `Частично`.
- Requirements about the supplier's organisation (presentations, demonstrations, references,
  implemented projects, training, documentation on request, account manager, support ticket
  system, fines, three-party meetings, licences of partners) are not product functions —
  empty verdict, «вне функционального контура». But if such a row ALSO contains a product
  function (e.g. «предоставить номерную емкость … с возможностью выбора и заказа дополнительных
  номеров» → tv4 2.2), assess the product part and say so.
- Integration with Skillaz, with «внутренним контуром билайна», or changes of Skillaz funnel
  statuses are NOT described in SSOT as a ready function: Mango provides generic API /
  HTTP-request mechanisms (VPBXAPI, APISC, MDAPI, robot HTTP requests). Such a row is at best
  `Частично` (generic mechanism confirmed, the concrete integration requires development), and
  `Нет` when the whole row is about the Skillaz-specific scenario. Never present an existing
  CRM integration (amoCRM, Битрикс24, BPMSoft, 1С, IDENT) as evidence for Skillaz; a different
  CRM may only be cited as evidence of a generic mechanism, and that must be stated in `audit`.
- The base-engine rule («Да (базовая функция Yandex SpeechKit)») is allowed ONLY for speech
  analytics / robots AND only with an official vendor source inside the allowed domains. The KB
  and the Mango domains contain no such vendor page, so do NOT use this rule.
- Overpromising risks must be stated in `audit`: paid options, separate products/modules
  (Контакт-центр, Речевая аналитика, Контроль качества, Робот Фил, Wallboard), tariff limits,
  project integration work, settings available only to an administrator.
- A `Да` verdict does not mean «included in the base tariff» — if the function belongs to a
  separate product or option, say it in `audit`.

## Output

Write ONLY your JSON file `experiments/issue_484/research/<BATCH>.json`; do not touch any other
file. JSON object keyed by row id (exactly as in your rows file, e.g.
`"Требования к системе!4"`, `"SLA!2"`), each value:

```
{
  "verdict": "Да" | "Частично" | "Нет" | "",
  "why":   "Comment in Russian with footnote markers [1], [2] … placed where the source link goes
            (the generator inserts the link right after each marker). Structure it by atomic parts:
            «Подтверждено: … [1]; не подтверждено: …». For no data start with 'Нет данных: …'.",
  "refs":  ["tv4:2.6.3", "kb:CC/12-obzvony.md", "portal:<url>|<page title>"],   // ref i <-> marker [i]
  "quotes":["verbatim quote for ref 1", "verbatim quote for ref 2"],            // same length as refs
  "audit": "Russian critic-gate comment: trace confirmation, hidden risks / overpromising,
            interpretation in Mango's favour. Use exactly 'OK' if there are no issues."
}
```

Hard requirements (a validator script checks all of them):

- Every row id of your rows file must be present, and no other ids.
- `quotes[i]` must be copied **verbatim** (whitespace may differ) from the body of the referenced
  KB section (not from its frontmatter) or from the referenced template item text, length
  30–250 characters, no `«»` characters inside, no `|`, no `<br>`. Use `…` only to join two
  verbatim fragments of the SAME ref.
- Every marker `[i]` in `why` must have `refs[i-1]`, and every ref must have its marker, each
  marker exactly once.
- `Да` / `Частично` rows need at least one ref. A `Нет` row needs a ref when it contradicts a
  document (no-data rows may have none). Empty-verdict rows normally have no refs.
- `why` ≤ 1500 characters, `audit` ≤ 600 characters, both in Russian. Never use the `|`
  character anywhere.
- Validate your file with `python3 -m json.tool` and check each quote with `grep -F` before you
  finish.
