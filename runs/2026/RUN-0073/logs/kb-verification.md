---
status: draft
version: 0.1
updated: 2026-10-19
ai-generated: true
type: log
scope: mango-only
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/373"
related_artifacts:
  - "https://github.com/G-Ivan-A/mango-ba-ai-runtime/blob/91406e430aeb70dabf20548eee0ea95127f42690/docs/kb"
---

# Журнал сверки с базой знаний — RUN-0073

> Файл **порождён** скриптом [`experiments/issue_373_golden_set.py`](../../../../experiments/issue_373_golden_set.py) из разметки [`experiments/issue_373_golden_data.py`](../../../../experiments/issue_373_golden_data.py) — не редактируйте вручную. Каждая цитата сверена с экспортом чата ([`../logs/quote-verification.md`](../logs/quote-verification.md)).

База знаний — `docs/kb` mango-ba-ai-runtime на SHA `91406e430aeb70dabf20548eee0ea95127f42690`. Локатор — код документа, раздел и файл раздела КБ.

## Локаторы

| Локатор | Файл раздела КБ |
| --- | --- |
| VPBXAPI §2.4.3 | [`docs/kb/vpbx-api/sections/20-o-parametre-sign.md (с. 14)`](https://github.com/G-Ivan-A/mango-ba-ai-runtime/blob/91406e430aeb70dabf20548eee0ea95127f42690/docs/kb/vpbx-api/sections/20-o-parametre-sign.md) |
| VPBXAPI §2.1.1 | [`docs/kb/vpbx-api/sections/14-api-vats.md (с. 11–12)`](https://github.com/G-Ivan-A/mango-ba-ai-runtime/blob/91406e430aeb70dabf20548eee0ea95127f42690/docs/kb/vpbx-api/sections/14-api-vats.md) |
| VPBXAPI §3.1.4 | [`docs/kb/vpbx-api/sections/29-uvedomlenie-o-zapisi-razgovora.md (с. 22–26)`](https://github.com/G-Ivan-A/mango-ba-ai-runtime/blob/91406e430aeb70dabf20548eee0ea95127f42690/docs/kb/vpbx-api/sections/29-uvedomlenie-o-zapisi-razgovora.md) |
| VPBXAPI §3.5.2 | [`docs/kb/vpbx-api/sections/65-poluchenie-zapisi-razgovora-posredstvom.md (с. 88–89)`](https://github.com/G-Ivan-A/mango-ba-ai-runtime/blob/91406e430aeb70dabf20548eee0ea95127f42690/docs/kb/vpbx-api/sections/65-poluchenie-zapisi-razgovora-posredstvom.md) |
| ROBOTFIL §5.6 | [`docs/kb/cov-robot-fil/sections/24-blok-otpravit-http-zapros.md (с. 71–77)`](https://github.com/G-Ivan-A/mango-ba-ai-runtime/blob/91406e430aeb70dabf20548eee0ea95127f42690/docs/kb/cov-robot-fil/sections/24-blok-otpravit-http-zapros.md) |
| ROBOTFIL §5.20 | [`docs/kb/cov-robot-fil/sections/39-blok-rabota-s-pamyatyu.md (с. 130–132)`](https://github.com/G-Ivan-A/mango-ba-ai-runtime/blob/91406e430aeb70dabf20548eee0ea95127f42690/docs/kb/cov-robot-fil/sections/39-blok-rabota-s-pamyatyu.md) |
| ROBOTFIL §7 | [`docs/kb/cov-robot-fil/sections/57-peremennye.md (с. 161–166)`](https://github.com/G-Ivan-A/mango-ba-ai-runtime/blob/91406e430aeb70dabf20548eee0ea95127f42690/docs/kb/cov-robot-fil/sections/57-peremennye.md) |

## Вхождения, сверенные с КБ

| ID | Р. | Кат. | Продукт | Цитата модели | Локатор | Что показывает КБ |
| --- | --- | --- | --- | --- | --- | --- |
| I-036 | 11 | C09 | `vpbx` | «Webhook `events/recording` содержит только `extension`.» | VPBXAPI §3.1.4 | уведомление о записи содержит recording_id, recording_state, seq, entry_id, call_id, extension, timestamp, completion_code, recipient, command_id; `extension` может не передаваться |
| I-037 | 15 | C09 | `vpbx` | «содержит только `extension` (внутренний номер), `entry_id` и `recording_id`» | VPBXAPI §3.1.4 | — |
| I-038 | 19 | C15 | `vpbx` | «интеграции с REST API/Webhook Mango Office» | VPBXAPI §2.1.1 | — |
| I-064 | 51 | C15 | `vpbx` | «вычисляет HMAC-подпись» | VPBXAPI §2.4.3 | подпись VPBX API — sha256(vpbx_api_key + json + vpbx_api_salt), не HMAC |
| I-065 | 51 | C09 | `vpbx` | «часто содержит только факт записи» | VPBXAPI §3.1.4 | — |
| I-087 | 71 | C18 | `vpbx` | «Ссылка запрашивается у API Mango Office непосредственно перед отправкой пакета в CallMentor (синхронное обогащение)» | VPBXAPI §3.5.2 | ссылка временная и недействительна после первого обращения; повторный запрос ссылки CallMentor не описан |
| I-092 | 73 | C15 | `vpbx` | «Валидация HMAC-подписи» | VPBXAPI §2.4.3 | — |
| I-101 | 75 | C10 | `vpbx` | «Структуры данных строго сверены с официальной документацией REST API MANGO OFFICE» | VPBXAPI §2.4.3 | в том же ответе — HMAC, которого нет в документации |
| I-103 | 75 | C15 | `vpbx` | «HMAC» | VPBXAPI §2.4.3 | — |
| I-104 | 77 | C15 | `vpbx` | «валидация HMAC-подписи по параметрам» | VPBXAPI §2.4.3 | раздел 7 допускает технику, дефект — неверный механизм |
| I-105 | 77 | C15 | `vpbx` | «Событие без обязательных атрибутов» | VPBXAPI §3.1.4 | — |
| I-120 | 81 | C18 | `vpbx` | «Фильтрация по группам Операторов (по `extension` из webhook).» | VPBXAPI §3.1.4 | `extension` не передаётся, если ВАТС не идентифицировала сотрудника |
| I-128 | 87 | C09 | `vpbx` | «Mango доставляет вебхуки по принципу at-least-once» | VPBXAPI §3.1.4 | КБ не формулирует гарантию доставки; БА принял формулировку без источника |
| I-136 | 99 | C18 | `vpbx` | «3.8. Срок скачивания записи» | VPBXAPI §3.5.2 | вопрос о сроке без учёта того, что ссылка недействительна после первого обращения |
| I-137 | 101 | C18 | `vpbx` | «при истечении мы можем пер» | VPBXAPI §3.5.2 | — |
| I-140 | 103 | C09 | `robot-fil` | «нет собственного REST API» | ROBOTFIL §5.6 | у робота есть блок «Отправить http-запрос» (§5.6); вывод о REST API не подкреплён локатором |
| I-141 | 103 | C09 | `robot-fil` | «Согласно документации, оно имеет» | ROBOTFIL §7 | «жёсткий лимит» в документации назван как пример («например, 3 из 10 000») |
| I-142 | 103 | C09 | `robot-fil` | «При объеме 2 000 звонков в сутки хранилище переполнится за 5 дней, и старые записи будут безвозвратно затерты.» | ROBOTFIL §5.20 | в КБ нет утверждения о перезаписи старых значений; объём 2 000 не назван |
| I-144 | 103 | C09 | `vpbx` | «В вебхуке `events/recording` приходит только `extension`.» | VPBXAPI §3.1.4 | — |
