---
status: draft
version: 0.1
updated: 2026-11-18
temperature: 0.1
owner: G-Ivan-A
type: contract
scope: ssot-stage1-handoff
related_artifacts:
  - "docs/contracts/ssot-stage1-handoff-manifest.json"
  - "docs/audit/2026-11-18-runtime-dependencies-ssot-handoff.md"
  - "standards/bcreq-runtime-references.md"
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/492"
---

# Манифест передачи SSOT этапа 1 в mango-ba-ai-runtime (issue #492)

Сгенерировано `experiments/issue_492/build_ssot_manifest.py` из [JSON-манифеста](ssot-stage1-handoff-manifest.json); не править вручную.
Статус: черновик, ждёт принятия владельцем и RFC-задачи в runtime. Runtime этой задачей не менялся.

- Источник: `G-Ivan-A/mango_ba_prompts` на коммите `7dea8f716d69e55c183865630d10f40cdb6e46b1` (merge PR #491).
- Получатель: `G-Ivan-A/mango-ba-ai-runtime`; SHA реестра справочников `68ad8fcffd47439fc3051852d9a2fbbe23815855`, наблюдавшийся main `90f082330015634f3a0632cdd31ebfe1c15fd7ae`.
- Хэш: sha256 байтов файла на source_commit. Клиентские данные и вложения не включаются: только пути, версии, хэши и метаданные; пути runs/, kb/, inputs/, attachments/ запрещены.
- Артефактов: 133; контрактов шагов A-IN: 24; уже есть в runtime побайтно: 0.
- Статусы цепочки: архив — 6, действует — 121, заменён — 6.

## 1. Группы и карточки переноса

| Группа | Содержание | Артефактов | Статусы цепочки | Карточка ФТ-4 |
| --- | --- | --- | --- | --- |
| `ain-route` | Маршрут A-IN и 24 контракта шагов | 29 | действует 29 | BL-186 |
| `system-format` | Системный формат шагов (#490) | 3 | действует 3 | BL-185 |
| `archive-2.7.0` | Архив 2.7.0 и его манифест | 6 | архив 6 | BL-185 |
| `drafts` | Черновики Ш-ХХ «по тесту» | 14 | действует 11, заменён 3 | BL-185 |
| `prompts-v0.1` | 14 промптов v0.1 и комплект прогона | 15 | действует 12, заменён 3 | BL-185 |
| `step-handoff` | Итог шага (step-handoff) | 1 | действует 1 | BL-186 |
| `base-standard` | Базовый стандарт и профили | 2 | действует 2 | BL-187 |
| `catalog-39` | Каталог 39 операций | 41 | действует 41 | BL-187 |
| `section-meta-standards` | Мета-стандарты разделов | 9 | действует 9 | BL-187 |
| `industry-practice` | Отраслевая практика | 1 | действует 1 | BL-187 |
| `evidence-normalization` | Нормализация доказательств | 1 | действует 1 | BL-186 |
| `lessons` | Реестр уроков | 5 | действует 5 | BL-187 |
| `runtime-references` | Реестр справочников runtime | 1 | действует 1 | BL-187 |
| `execution-norms` | Прочие нормы исполнения шагов (ФТ-2, класс б) | 3 | действует 3 | BL-187 |
| `gates-and-cs` | Контракт гейтов и поток CS (ФТ-2, класс б) | 2 | действует 2 | BL-188 |

## 2. Цепочка эволюции

| Этап | Что это | Файлов | Что действует, что заменено, что в архиве |
| --- | --- | --- | --- |
| v0.1 | 14 промптов потока BCREQ | 14 | Ш-0, Ш-3…Ш-9, Ш-В, Ш-С действуют в комплекте прогона; Ш-1, Ш-2 и A-IN one-shot в A-IN заменены AIN-01…24, файлы сохранены для библиотеки и истории. |
| по тесту | Черновики Ш-ХХ (BL-156), собраны из v0.1 | 14 | Черновики собираются `scripts/build_bcreq_step_prompts.py` из базового стандарта, профилей, каталога и реестра; Ш-А и Ш-Р существуют только как черновики. |
| 2.7.0 | Комплект сайта 2.7.0 (архив) | 6 | Ш-А, Ш-1, Ш-2 и A-IN one-shot заморожены как полные тексты 2.7.0; замены — в manifest.json архива. |
| AIN v0.3 | 24 отдельных вызова A-IN по RFC-AIN-001 | 24 | Действующий формат по умолчанию: Ш-0 → AIN-01…24 → ФТ после handover AIN-24 и Г-IN. |
| системный формат | Комплексные шаги Ш-А, Ш-1, Ш-2 из архива 2.7.0 | 3 | Альтернатива AIN v0.3 по выбору БА на сайте (#490); остальные шаги общие. |

Замены по манифесту архива 2.7.0 (`prompts/archive/a-in-v2.7.0/manifest.json`):

| Прежний вход | Заменён |
| --- | --- |
| Ш-А | AIN-02 |
| Ш-1 | AIN-01, AIN-02, AIN-03, AIN-04, AIN-05, AIN-06, AIN-07, AIN-08, AIN-09, AIN-10, AIN-11, AIN-12, AIN-13, AIN-14, AIN-15, AIN-16, AIN-17, AIN-18, AIN-19, AIN-20, AIN-21, AIN-22, AIN-23, AIN-24 |
| Ш-2 | AIN-06, AIN-07, AIN-08, AIN-09, AIN-10, AIN-11, AIN-12, AIN-13, AIN-22 |
| A-IN one-shot | AIN-01, AIN-02, AIN-03, AIN-04, AIN-05, AIN-06, AIN-07, AIN-08, AIN-09, AIN-10, AIN-11, AIN-12, AIN-13, AIN-14, AIN-15, AIN-16, AIN-17, AIN-18, AIN-19, AIN-20, AIN-21, AIN-22, AIN-23, AIN-24 |

## 3. Политика синхронизации

1. Runtime хранит побайтную копию артефактов манифеста, закреплённую на `source_commit`; SSOT остаётся в mango_ba_prompts.
2. Локальные правки закреплённых копий в runtime запрещены: расхождение устраняется следующей передачей, а не редактированием копии.
3. Обновление — только новой закреплённой передачей: новый манифест с новым `source_commit`, новыми sha256 и записью в журнале передач runtime.
4. Проверка копии — равенство sha256 файла в runtime значению манифеста; несовпадение — дефект передачи.
5. Ссылки внутри перенесённых файлов переписываются на путь в runtime, если цель тоже перенесена, иначе на permalink спицы с закреплённым SHA (как `scripts/sync_from_hub.py`).
6. Тексты промптов в спице до принятия манифеста не меняются; замена ссылок (б) — отдельная задача BL-190.

Прецеденты:

- `G-Ivan-A/mango_ba_prompts`: ADR-0004 и scripts/sync_from_hub.py: рабочие копии Хаба на `source_sha`, локальные правки запрещены, обновление — следующим синком; .hub-profile.json хранит last_sync и sync_history.
- `G-Ivan-A/mango-ba-ai-runtime`: compilation-manifest.yaml: база знаний скопирована из спицы на 8cbf82aa73129ec5747af07f790aaf438b0fb6e9, каталог продуктов — на e3597fd74da9c4f631ca46697c643462e2cf0b85; `hub_access_required_at_runtime: false`.

Приём манифеста — RFC-задача в runtime; issue в runtime создаёт владелец (раздел 6 реестра справочников).

## 4. Маршрут A-IN: 24 контракта шагов

| Шаг | Название | Операция | Дальше | Версия маршрута | Промпт | Версия | sha256 промпта | sha256 инструкции |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AIN-01 | Правила и версия | К-36 | AIN-02 | 0.3 | [`bcreq-ain-01-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-01-understanding-stepwise.md) | 0.3 | `d140c5e7bf2e1ef6…` | `7916a3eb15bceb08…` |
| AIN-02 | Данные у БА | К-01 | AIN-03 | 0.3 | [`bcreq-ain-02-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-02-understanding-stepwise.md) | 0.3 | `741b17602bf46062…` | `70b56c9a5aff565c…` |
| AIN-03 | Реестр источников | К-01, К-09 | AIN-04 | 0.3 | [`bcreq-ain-03-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-03-understanding-stepwise.md) | 0.3 | `11441407a7590c49…` | `322a4a89a8c0f237…` |
| AIN-04 | Атомизация | К-02 | AIN-05 | 0.3 | [`bcreq-ain-04-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-04-understanding-stepwise.md) | 0.3 | `5a92175e9de01747…` | `e571674b06f2cc89…` |
| AIN-05 | Качество и смысл | К-03 | AIN-06 | 0.3 | [`bcreq-ain-05-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-05-understanding-stepwise.md) | 0.3 | `60cbc7ff7a6c4fe9…` | `c7a28844d8fca958…` |
| AIN-06 | Кандидаты продуктов | К-05 | AIN-07 | 0.3 | [`bcreq-ain-06-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-06-understanding-stepwise.md) | 0.3 | `d8dec02cec33749c…` | `a3f84b5bbecf2569…` |
| AIN-07 | План retrieval | К-07, К-08, К-11 | AIN-08 | 0.3 | [`bcreq-ain-07-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-07-understanding-stepwise.md) | 0.3 | `2cb7309ca4ed3dd1…` | `c752c437d41bcbcc…` |
| AIN-08 | Веб-извлечение | К-07 | AIN-09 | 0.3 | [`bcreq-ain-08-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-08-understanding-stepwise.md) | 0.3 | `386cd61a7d6d53bd…` | `92712e73ed594061…` |
| AIN-09 | Извлечение БЗ | К-08 | AIN-10 | 0.3 | [`bcreq-ain-09-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-09-understanding-stepwise.md) | 0.3 | `e8a46837d882d28e…` | `03634d214f226ecc…` |
| AIN-10 | Замыкание зависимостей | К-11 | AIN-11 | 0.3 | [`bcreq-ain-10-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-10-understanding-stepwise.md) | 0.3 | `1223e3e98febaa95…` | `13841182bf45156f…` |
| AIN-11 | Сверка противоречий | К-10 | AIN-12 | 0.3 | [`bcreq-ain-11-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-11-understanding-stepwise.md) | 0.3 | `125d2b90461a97f7…` | `894d1f6b18b858e9…` |
| AIN-12 | Исполнимость сейчас | К-05, К-06 | AIN-13 | 0.3 | [`bcreq-ain-12-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-12-understanding-stepwise.md) | 0.3 | `a089851d1eef6897…` | `6a3b629a95cf106e…` |
| AIN-13 | Согласование пула | К-05, К-34 | AIN-14 | 0.3 | [`bcreq-ain-13-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-13-understanding-stepwise.md) | 0.3 | `fe6a4a39d581fdc2…` | `11606b8c6de6db4b…` |
| AIN-14 | Словарь — раздел 1 | К-14 | AIN-15 | 0.3 | [`bcreq-ain-14-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-14-understanding-stepwise.md) | 0.3 | `b5187bb8a888707f…` | `4dcc12043810d7df…` |
| AIN-15 | Остаточные пробелы | К-03 | AIN-16 | 0.3 | [`bcreq-ain-15-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-15-understanding-stepwise.md) | 0.3 | `dcc840d45cf6b98d…` | `390981a385d62e3a…` |
| AIN-16 | Вопросы Заказчику | К-04 | AIN-17 | 0.3 | [`bcreq-ain-16-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-16-understanding-stepwise.md) | 0.3 | `90a527e65978fc53…` | `b8bc7a9fc3469983…` |
| AIN-17 | Решение БА по вопросам | К-34 | AIN-18 | 0.3 | [`bcreq-ain-17-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-17-understanding-stepwise.md) | 0.3 | `c48391e68beb86a5…` | `6436b56866875409…` |
| AIN-18 | Новые данные | К-09 | AIN-19 | 0.3 | [`bcreq-ain-18-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-18-understanding-stepwise.md) | 0.3 | `b2e69c96c3e7099c…` | `a3389f6a625c794d…` |
| AIN-19 | Повторная нормализация | К-02, К-29 | AIN-20 | 0.3 | [`bcreq-ain-19-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-19-understanding-stepwise.md) | 0.3 | `cf742963e4d2ea00…` | `56ca7f90c829df03…` |
| AIN-20 | Снимок памяти | К-13, К-35 | AIN-21 | 0.3 | [`bcreq-ain-20-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-20-understanding-stepwise.md) | 0.3 | `88f28b5e5047f986…` | `f30223a430bbad7a…` |
| AIN-21 | Гейт до раздела 2 | К-20, К-34 | AIN-22 | 0.3 | [`bcreq-ain-21-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-21-understanding-stepwise.md) | 0.3 | `46d6f3db1d9a6e11…` | `db225e1987661eb8…` |
| AIN-22 | Сборка раздела 2 | К-15 | AIN-23 | 0.3 | [`bcreq-ain-22-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-22-understanding-stepwise.md) | 0.3 | `141a9778194fbcfa…` | `458ce4ae813bdc8d…` |
| AIN-23 | Проверка раздела 2 | К-28, К-31 | AIN-24 | 0.3 | [`bcreq-ain-23-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-23-understanding-stepwise.md) | 0.3 | `f46856d9268eebce…` | `bda63703cbff2f0a…` |
| AIN-24 | Г-IN и передача | К-35 | A-CORE или CS по решению БА | 0.3 | [`bcreq-ain-24-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-24-understanding-stepwise.md) | 0.3 | `1ab867ba5f88f0ee…` | `c71c88b475313647…` |

## 5. Артефакты

Полные sha256 и коммиты последнего изменения — в JSON.

| Путь | Группа | Версия | Статус цепочки | sha256 | Последнее изменение | Карточка |
| --- | --- | --- | --- | --- | --- | --- |
| [`docs/ba-processes/bcreq-a-in-common.md`](../../docs/ba-processes/bcreq-a-in-common.md) | `ain-route` | 0.3 | действует | `1466a2c7fffadedc…` | `78204858` | BL-186 |
| [`docs/ba-processes/bcreq-a-in-execution.md`](../../docs/ba-processes/bcreq-a-in-execution.md) | `ain-route` | 0.3 | действует | `8949c3ffab25f24f…` | `4e17f741` | BL-186 |
| [`docs/ba-processes/bcreq-a-in-instructions.json`](../../docs/ba-processes/bcreq-a-in-instructions.json) | `ain-route` | — | действует | `90b055c0485c2abd…` | `ae7ea98d` | BL-186 |
| [`docs/ba-processes/bcreq-a-in-route.json`](../../docs/ba-processes/bcreq-a-in-route.json) | `ain-route` | 0.3 | действует | `9aa0140dd900ffd9…` | `cf9de728` | BL-186 |
| [`docs/rfc/2026-11-a-in-decomposition.md`](../../docs/rfc/2026-11-a-in-decomposition.md) | `ain-route` | 0.7 | действует | `6b5dfc1ff2b389d3…` | `b3b985fd` | BL-186 |
| [`prompts/drafts/a-in/bcreq-ain-01-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-01-understanding-stepwise.md) | `ain-route` | 0.3 | действует | `d140c5e7bf2e1ef6…` | `78204858` | BL-186 |
| [`prompts/drafts/a-in/bcreq-ain-02-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-02-understanding-stepwise.md) | `ain-route` | 0.3 | действует | `741b17602bf46062…` | `78204858` | BL-186 |
| [`prompts/drafts/a-in/bcreq-ain-03-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-03-understanding-stepwise.md) | `ain-route` | 0.3 | действует | `11441407a7590c49…` | `78204858` | BL-186 |
| [`prompts/drafts/a-in/bcreq-ain-04-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-04-understanding-stepwise.md) | `ain-route` | 0.3 | действует | `5a92175e9de01747…` | `78204858` | BL-186 |
| [`prompts/drafts/a-in/bcreq-ain-05-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-05-understanding-stepwise.md) | `ain-route` | 0.3 | действует | `60cbc7ff7a6c4fe9…` | `78204858` | BL-186 |
| [`prompts/drafts/a-in/bcreq-ain-06-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-06-understanding-stepwise.md) | `ain-route` | 0.3 | действует | `d8dec02cec33749c…` | `78204858` | BL-186 |
| [`prompts/drafts/a-in/bcreq-ain-07-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-07-understanding-stepwise.md) | `ain-route` | 0.3 | действует | `2cb7309ca4ed3dd1…` | `78204858` | BL-186 |
| [`prompts/drafts/a-in/bcreq-ain-08-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-08-understanding-stepwise.md) | `ain-route` | 0.3 | действует | `386cd61a7d6d53bd…` | `78204858` | BL-186 |
| [`prompts/drafts/a-in/bcreq-ain-09-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-09-understanding-stepwise.md) | `ain-route` | 0.3 | действует | `e8a46837d882d28e…` | `78204858` | BL-186 |
| [`prompts/drafts/a-in/bcreq-ain-10-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-10-understanding-stepwise.md) | `ain-route` | 0.3 | действует | `1223e3e98febaa95…` | `78204858` | BL-186 |
| [`prompts/drafts/a-in/bcreq-ain-11-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-11-understanding-stepwise.md) | `ain-route` | 0.3 | действует | `125d2b90461a97f7…` | `78204858` | BL-186 |
| [`prompts/drafts/a-in/bcreq-ain-12-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-12-understanding-stepwise.md) | `ain-route` | 0.3 | действует | `a089851d1eef6897…` | `78204858` | BL-186 |
| [`prompts/drafts/a-in/bcreq-ain-13-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-13-understanding-stepwise.md) | `ain-route` | 0.3 | действует | `fe6a4a39d581fdc2…` | `78204858` | BL-186 |
| [`prompts/drafts/a-in/bcreq-ain-14-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-14-understanding-stepwise.md) | `ain-route` | 0.3 | действует | `b5187bb8a888707f…` | `78204858` | BL-186 |
| [`prompts/drafts/a-in/bcreq-ain-15-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-15-understanding-stepwise.md) | `ain-route` | 0.3 | действует | `dcc840d45cf6b98d…` | `78204858` | BL-186 |
| [`prompts/drafts/a-in/bcreq-ain-16-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-16-understanding-stepwise.md) | `ain-route` | 0.3 | действует | `90a527e65978fc53…` | `78204858` | BL-186 |
| [`prompts/drafts/a-in/bcreq-ain-17-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-17-understanding-stepwise.md) | `ain-route` | 0.3 | действует | `c48391e68beb86a5…` | `78204858` | BL-186 |
| [`prompts/drafts/a-in/bcreq-ain-18-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-18-understanding-stepwise.md) | `ain-route` | 0.3 | действует | `b2e69c96c3e7099c…` | `78204858` | BL-186 |
| [`prompts/drafts/a-in/bcreq-ain-19-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-19-understanding-stepwise.md) | `ain-route` | 0.3 | действует | `cf742963e4d2ea00…` | `78204858` | BL-186 |
| [`prompts/drafts/a-in/bcreq-ain-20-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-20-understanding-stepwise.md) | `ain-route` | 0.3 | действует | `88f28b5e5047f986…` | `78204858` | BL-186 |
| [`prompts/drafts/a-in/bcreq-ain-21-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-21-understanding-stepwise.md) | `ain-route` | 0.3 | действует | `46d6f3db1d9a6e11…` | `78204858` | BL-186 |
| [`prompts/drafts/a-in/bcreq-ain-22-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-22-understanding-stepwise.md) | `ain-route` | 0.3 | действует | `141a9778194fbcfa…` | `78204858` | BL-186 |
| [`prompts/drafts/a-in/bcreq-ain-23-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-23-understanding-stepwise.md) | `ain-route` | 0.3 | действует | `f46856d9268eebce…` | `78204858` | BL-186 |
| [`prompts/drafts/a-in/bcreq-ain-24-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-24-understanding-stepwise.md) | `ain-route` | 0.3 | действует | `1ab867ba5f88f0ee…` | `78204858` | BL-186 |
| [`prompts/drafts/system/bcreq-context-understanding-system.md`](../../prompts/drafts/system/bcreq-context-understanding-system.md) | `system-format` | 0.3 | действует | `371f39bf07c8cd87…` | `4e17f741` | BL-185 |
| [`prompts/drafts/system/bcreq-intake-questionnaire-system.md`](../../prompts/drafts/system/bcreq-intake-questionnaire-system.md) | `system-format` | 0.1 | действует | `47c35c2e96fa6a60…` | `4e17f741` | BL-185 |
| [`prompts/drafts/system/bcreq-products-impact-analysis-system.md`](../../prompts/drafts/system/bcreq-products-impact-analysis-system.md) | `system-format` | 0.2 | действует | `ff13abe00ae7e6b5…` | `4e17f741` | BL-185 |
| [`prompts/archive/a-in-v2.7.0/README.md`](../../prompts/archive/a-in-v2.7.0/README.md) | `archive-2.7.0` | — | архив | `1b79442c5ed5b16c…` | `ecba9b76` | BL-185 |
| [`prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md`](../../prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md) | `archive-2.7.0` | 0.3 | архив | `277b6577a3adca18…` | `ecba9b76` | BL-185 |
| [`prompts/archive/a-in-v2.7.0/bcreq-in-understanding-oneshot.md`](../../prompts/archive/a-in-v2.7.0/bcreq-in-understanding-oneshot.md) | `archive-2.7.0` | 0.2 | архив | `838e3c5fbae47e8a…` | `ecba9b76` | BL-185 |
| [`prompts/archive/a-in-v2.7.0/bcreq-intake-questionnaire-stepwise.md`](../../prompts/archive/a-in-v2.7.0/bcreq-intake-questionnaire-stepwise.md) | `archive-2.7.0` | 0.1 | архив | `580106bfb3458042…` | `ecba9b76` | BL-185 |
| [`prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md`](../../prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md) | `archive-2.7.0` | 0.2 | архив | `1f9e7c452b256de3…` | `ecba9b76` | BL-185 |
| [`prompts/archive/a-in-v2.7.0/manifest.json`](../../prompts/archive/a-in-v2.7.0/manifest.json) | `archive-2.7.0` | 2.7.0 | архив | `0cf1d23e098ea8ce…` | `ecba9b76` | BL-185 |
| [`prompts/drafts/bcreq-constitution-governance-oneshot.md`](../../prompts/drafts/bcreq-constitution-governance-oneshot.md) | `drafts` | 0.5 | действует | `81652ae24230047d…` | `94cbfb85` | BL-185 |
| [`prompts/drafts/bcreq-constraints-documentation-stepwise.md`](../../prompts/drafts/bcreq-constraints-documentation-stepwise.md) | `drafts` | 0.2 | действует | `5cde0026c92dcb6b…` | `dad6301e` | BL-185 |
| [`prompts/drafts/bcreq-context-understanding-stepwise.md`](../../prompts/drafts/bcreq-context-understanding-stepwise.md) | `drafts` | 0.5 | заменён | `0d92de04d6464866…` | `dad6301e` | BL-185 |
| [`prompts/drafts/bcreq-extra-risk-analysis-stepwise.md`](../../prompts/drafts/bcreq-extra-risk-analysis-stepwise.md) | `drafts` | 0.2 | действует | `d166daa1a4bfae06…` | `dad6301e` | BL-185 |
| [`prompts/drafts/bcreq-fr-documentation-stepwise.md`](../../prompts/drafts/bcreq-fr-documentation-stepwise.md) | `drafts` | 0.5 | действует | `dd8e0102f8b52356…` | `4e17f741` | BL-185 |
| [`prompts/drafts/bcreq-intake-questionnaire-stepwise.md`](../../prompts/drafts/bcreq-intake-questionnaire-stepwise.md) | `drafts` | 0.2 | заменён | `79cb695b441d54e3…` | `dad6301e` | BL-185 |
| [`prompts/drafts/bcreq-nfr-documentation-stepwise.md`](../../prompts/drafts/bcreq-nfr-documentation-stepwise.md) | `drafts` | 0.2 | действует | `3d47e65b7fda55cb…` | `dad6301e` | BL-185 |
| [`prompts/drafts/bcreq-orr-solution-design-stepwise.md`](../../prompts/drafts/bcreq-orr-solution-design-stepwise.md) | `drafts` | 0.3 | действует | `521491281f4e641a…` | `dad6301e` | BL-185 |
| [`prompts/drafts/bcreq-products-impact-analysis-stepwise.md`](../../prompts/drafts/bcreq-products-impact-analysis-stepwise.md) | `drafts` | 0.4 | заменён | `0dd3069fbef22d85…` | `dad6301e` | BL-185 |
| [`prompts/drafts/bcreq-release-readiness-oneshot.md`](../../prompts/drafts/bcreq-release-readiness-oneshot.md) | `drafts` | 0.2 | действует | `2135c6e3cc5c24b5…` | `3fa387e4` | BL-185 |
| [`prompts/drafts/bcreq-review-validation-oneshot.md`](../../prompts/drafts/bcreq-review-validation-oneshot.md) | `drafts` | 0.3 | действует | `2fc1b056be7e8cb0…` | `28f868e1` | BL-185 |
| [`prompts/drafts/bcreq-scenarios-modeling-oneshot.md`](../../prompts/drafts/bcreq-scenarios-modeling-oneshot.md) | `drafts` | 0.2 | действует | `dbbd3f4cbd8ab60f…` | `28f868e1` | BL-185 |
| [`prompts/drafts/bcreq-uc-modeling-stepwise.md`](../../prompts/drafts/bcreq-uc-modeling-stepwise.md) | `drafts` | 0.2 | действует | `cadc34c43ca817e5…` | `dad6301e` | BL-185 |
| [`prompts/drafts/manifest.json`](../../prompts/drafts/manifest.json) | `drafts` | — | действует | `cbe13abae6af09b2…` | `cb19fb69` | BL-185 |
| [`docs/ba-processes/bcreq-run-kit.md`](../../docs/ba-processes/bcreq-run-kit.md) | `prompts-v0.1` | 0.10 | действует | `fc4802dcb5dea177…` | `3fa387e4` | BL-185 |
| [`prompts/bcreq-constitution-governance-oneshot.md`](../../prompts/bcreq-constitution-governance-oneshot.md) | `prompts-v0.1` | 0.5 | действует | `3ffa79cbef350984…` | `ae7ea98d` | BL-185 |
| [`prompts/bcreq-constraints-documentation-stepwise.md`](../../prompts/bcreq-constraints-documentation-stepwise.md) | `prompts-v0.1` | 0.2 | действует | `3b169baa6575267b…` | `09979430` | BL-185 |
| [`prompts/bcreq-context-understanding-stepwise.md`](../../prompts/bcreq-context-understanding-stepwise.md) | `prompts-v0.1` | 0.5 | заменён | `5defc5543698e242…` | `ae7ea98d` | BL-185 |
| [`prompts/bcreq-core-documentation-oneshot.md`](../../prompts/bcreq-core-documentation-oneshot.md) | `prompts-v0.1` | 0.4 | действует | `7fb48b087b63f04b…` | `ae7ea98d` | BL-185 |
| [`prompts/bcreq-extra-risk-analysis-stepwise.md`](../../prompts/bcreq-extra-risk-analysis-stepwise.md) | `prompts-v0.1` | 0.2 | действует | `1b459dc25a66ae44…` | `09979430` | BL-185 |
| [`prompts/bcreq-fr-documentation-stepwise.md`](../../prompts/bcreq-fr-documentation-stepwise.md) | `prompts-v0.1` | 0.5 | действует | `04fb5da191ec844a…` | `ae7ea98d` | BL-185 |
| [`prompts/bcreq-in-understanding-oneshot.md`](../../prompts/bcreq-in-understanding-oneshot.md) | `prompts-v0.1` | 0.4 | заменён | `5d916d68c82160b2…` | `ae7ea98d` | BL-185 |
| [`prompts/bcreq-nfr-documentation-stepwise.md`](../../prompts/bcreq-nfr-documentation-stepwise.md) | `prompts-v0.1` | 0.2 | действует | `bf565bfa0e6138ea…` | `09979430` | BL-185 |
| [`prompts/bcreq-orr-solution-design-stepwise.md`](../../prompts/bcreq-orr-solution-design-stepwise.md) | `prompts-v0.1` | 0.3 | действует | `d8563bea066cb5e4…` | `09979430` | BL-185 |
| [`prompts/bcreq-products-impact-analysis-stepwise.md`](../../prompts/bcreq-products-impact-analysis-stepwise.md) | `prompts-v0.1` | 0.4 | заменён | `235a83909931085e…` | `ae7ea98d` | BL-185 |
| [`prompts/bcreq-review-validation-oneshot.md`](../../prompts/bcreq-review-validation-oneshot.md) | `prompts-v0.1` | 0.3 | действует | `b6a6af0bd8abfa17…` | `ce4fc8aa` | BL-185 |
| [`prompts/bcreq-scenarios-modeling-oneshot.md`](../../prompts/bcreq-scenarios-modeling-oneshot.md) | `prompts-v0.1` | 0.2 | действует | `9b82e301403b1605…` | `09979430` | BL-185 |
| [`prompts/bcreq-uc-modeling-stepwise.md`](../../prompts/bcreq-uc-modeling-stepwise.md) | `prompts-v0.1` | 0.2 | действует | `61ae4645c0db9688…` | `09979430` | BL-185 |
| [`prompts/bcreq-work-solution-design-oneshot.md`](../../prompts/bcreq-work-solution-design-oneshot.md) | `prompts-v0.1` | 0.2 | действует | `204e8abfd5248edf…` | `09979430` | BL-185 |
| [`docs/ba-processes/bcreq-step-handoff.md`](../../docs/ba-processes/bcreq-step-handoff.md) | `step-handoff` | 0.1 | действует | `33e9c4c3db0d9bb0…` | `4740124f` | BL-186 |
| [`standards/bcreq-prompt-base-standard.md`](../../standards/bcreq-prompt-base-standard.md) | `base-standard` | 0.1.3 | действует | `533a37c255f96124…` | `36799e9e` | BL-187 |
| [`standards/bcreq-prompt-profiles.md`](../../standards/bcreq-prompt-profiles.md) | `base-standard` | 0.1.2 | действует | `ac8c46ef07a8a6e4…` | `28f868e1` | BL-187 |
| [`standards/bcreq-manual-classes/01-intake.md`](../../standards/bcreq-manual-classes/01-intake.md) | `catalog-39` | 0.1.3 | действует | `4f4862306d29283e…` | `28f868e1` | BL-187 |
| [`standards/bcreq-manual-classes/02-normalize.md`](../../standards/bcreq-manual-classes/02-normalize.md) | `catalog-39` | 0.1.2 | действует | `ca6d62218451aef4…` | `c4c393f2` | BL-187 |
| [`standards/bcreq-manual-classes/03-ambiguity.md`](../../standards/bcreq-manual-classes/03-ambiguity.md) | `catalog-39` | 0.1.2 | действует | `7cd2704ac0c02094…` | `c4c393f2` | BL-187 |
| [`standards/bcreq-manual-classes/04-questions.md`](../../standards/bcreq-manual-classes/04-questions.md) | `catalog-39` | 0.1.2 | действует | `f8aa022e186a7c62…` | `c4c393f2` | BL-187 |
| [`standards/bcreq-manual-classes/05-taxonomy.md`](../../standards/bcreq-manual-classes/05-taxonomy.md) | `catalog-39` | 0.1.2 | действует | `eb8dd7d7ae57fc91…` | `c4c393f2` | BL-187 |
| [`standards/bcreq-manual-classes/06-scope.md`](../../standards/bcreq-manual-classes/06-scope.md) | `catalog-39` | 0.1.2 | действует | `a01310bbc6e324e0…` | `c4c393f2` | BL-187 |
| [`standards/bcreq-manual-classes/07-web-evidence.md`](../../standards/bcreq-manual-classes/07-web-evidence.md) | `catalog-39` | 0.1.2 | действует | `20b833ad47530924…` | `c4c393f2` | BL-187 |
| [`standards/bcreq-manual-classes/08-document-evidence.md`](../../standards/bcreq-manual-classes/08-document-evidence.md) | `catalog-39` | 0.1.2 | действует | `fe2b74c3bdb25ea0…` | `c4c393f2` | BL-187 |
| [`standards/bcreq-manual-classes/09-ba-enrichment.md`](../../standards/bcreq-manual-classes/09-ba-enrichment.md) | `catalog-39` | 0.1.2 | действует | `ec7596ce708dc6cd…` | `c4c393f2` | BL-187 |
| [`standards/bcreq-manual-classes/10-source-conflicts.md`](../../standards/bcreq-manual-classes/10-source-conflicts.md) | `catalog-39` | 0.1.2 | действует | `5b6803d7cc13567e…` | `c4c393f2` | BL-187 |
| [`standards/bcreq-manual-classes/11-dependency-check.md`](../../standards/bcreq-manual-classes/11-dependency-check.md) | `catalog-39` | 0.1.2 | действует | `e5798fe989f5a6fc…` | `c4c393f2` | BL-187 |
| [`standards/bcreq-manual-classes/12-phase-assembly.md`](../../standards/bcreq-manual-classes/12-phase-assembly.md) | `catalog-39` | 0.1.2 | действует | `abf33a6deb35d904…` | `c4c393f2` | BL-187 |
| [`standards/bcreq-manual-classes/13-handoff-check.md`](../../standards/bcreq-manual-classes/13-handoff-check.md) | `catalog-39` | 0.1.2 | действует | `6bc2bd6f6257a24c…` | `c4c393f2` | BL-187 |
| [`standards/bcreq-manual-classes/14-glossary.md`](../../standards/bcreq-manual-classes/14-glossary.md) | `catalog-39` | 0.1.3 | действует | `3dcd4072f519469b…` | `28f868e1` | BL-187 |
| [`standards/bcreq-manual-classes/15-business-context.md`](../../standards/bcreq-manual-classes/15-business-context.md) | `catalog-39` | 0.1.3 | действует | `e3ad8851afd02417…` | `28f868e1` | BL-187 |
| [`standards/bcreq-manual-classes/16-fr-delta.md`](../../standards/bcreq-manual-classes/16-fr-delta.md) | `catalog-39` | 0.1.3 | действует | `e3ec2a170602398d…` | `28f868e1` | BL-187 |
| [`standards/bcreq-manual-classes/17-fr-new.md`](../../standards/bcreq-manual-classes/17-fr-new.md) | `catalog-39` | 0.1.3 | действует | `fd1af6e009285546…` | `28f868e1` | BL-187 |
| [`standards/bcreq-manual-classes/18-nfr.md`](../../standards/bcreq-manual-classes/18-nfr.md) | `catalog-39` | 0.1.2 | действует | `6dc8f672d9cd8f40…` | `c4c393f2` | BL-187 |
| [`standards/bcreq-manual-classes/19-uc-coverage.md`](../../standards/bcreq-manual-classes/19-uc-coverage.md) | `catalog-39` | 0.1.2 | действует | `cace70bb1018d6fd…` | `c4c393f2` | BL-187 |
| [`standards/bcreq-manual-classes/20-gate-evidence.md`](../../standards/bcreq-manual-classes/20-gate-evidence.md) | `catalog-39` | 0.1.2 | действует | `b8ef1827fb6f225a…` | `c4c393f2` | BL-187 |
| [`standards/bcreq-manual-classes/21-solution-l1.md`](../../standards/bcreq-manual-classes/21-solution-l1.md) | `catalog-39` | 0.1.3 | действует | `9f43908b539b8516…` | `28f868e1` | BL-187 |
| [`standards/bcreq-manual-classes/22-solution-l2.md`](../../standards/bcreq-manual-classes/22-solution-l2.md) | `catalog-39` | 0.1.3 | действует | `03560a933bb4ed5a…` | `28f868e1` | BL-187 |
| [`standards/bcreq-manual-classes/23-constraints.md`](../../standards/bcreq-manual-classes/23-constraints.md) | `catalog-39` | 0.1.3 | действует | `633ee0ab31e8ea93…` | `28f868e1` | BL-187 |
| [`standards/bcreq-manual-classes/24-uc-boundaries.md`](../../standards/bcreq-manual-classes/24-uc-boundaries.md) | `catalog-39` | 0.1.2 | действует | `dbd6e3d20fba46a7…` | `c4c393f2` | BL-187 |
| [`standards/bcreq-manual-classes/25-risks.md`](../../standards/bcreq-manual-classes/25-risks.md) | `catalog-39` | 0.1.2 | действует | `817c715e7df4b110…` | `c4c393f2` | BL-187 |
| [`standards/bcreq-manual-classes/26-delivery-dependencies.md`](../../standards/bcreq-manual-classes/26-delivery-dependencies.md) | `catalog-39` | 0.1.2 | действует | `6ac1b7365c51e706…` | `c4c393f2` | BL-187 |
| [`standards/bcreq-manual-classes/27-acceptance.md`](../../standards/bcreq-manual-classes/27-acceptance.md) | `catalog-39` | 0.1.2 | действует | `508045aca1a56c7e…` | `c4c393f2` | BL-187 |
| [`standards/bcreq-manual-classes/28-independent-review.md`](../../standards/bcreq-manual-classes/28-independent-review.md) | `catalog-39` | 0.1.2 | действует | `bfbf9fbddef01a28…` | `c4c393f2` | BL-187 |
| [`standards/bcreq-manual-classes/29-impact.md`](../../standards/bcreq-manual-classes/29-impact.md) | `catalog-39` | 0.1.2 | действует | `7874eece61b16b23…` | `c4c393f2` | BL-187 |
| [`standards/bcreq-manual-classes/30-targeted-edit.md`](../../standards/bcreq-manual-classes/30-targeted-edit.md) | `catalog-39` | 0.1.2 | действует | `cd149ce2f49ad9e7…` | `c4c393f2` | BL-187 |
| [`standards/bcreq-manual-classes/31-conformance.md`](../../standards/bcreq-manual-classes/31-conformance.md) | `catalog-39` | 0.1.2 | действует | `7e891d41bfca4b39…` | `c4c393f2` | BL-187 |
| [`standards/bcreq-manual-classes/32-audience-projection.md`](../../standards/bcreq-manual-classes/32-audience-projection.md) | `catalog-39` | 0.1.2 | действует | `56c36296d5e8531e…` | `c4c393f2` | BL-187 |
| [`standards/bcreq-manual-classes/33-release-audit.md`](../../standards/bcreq-manual-classes/33-release-audit.md) | `catalog-39` | 0.1.2 | действует | `fdbb7d85a26bec57…` | `086fc47c` | BL-187 |
| [`standards/bcreq-manual-classes/34-human-record.md`](../../standards/bcreq-manual-classes/34-human-record.md) | `catalog-39` | 0.1.2 | действует | `7259f81df7203c10…` | `2f6aed43` | BL-187 |
| [`standards/bcreq-manual-classes/35-baseline-handover.md`](../../standards/bcreq-manual-classes/35-baseline-handover.md) | `catalog-39` | 0.1.2 | действует | `79117175f34816c0…` | `c4c393f2` | BL-187 |
| [`standards/bcreq-manual-classes/36-rule-bundle.md`](../../standards/bcreq-manual-classes/36-rule-bundle.md) | `catalog-39` | 0.1.3 | действует | `63daf04c89abd3cf…` | `28f868e1` | BL-187 |
| [`standards/bcreq-manual-classes/37-user-story.md`](../../standards/bcreq-manual-classes/37-user-story.md) | `catalog-39` | 0.1.2 | действует | `3cd873263d6b9b52…` | `c4c393f2` | BL-187 |
| [`standards/bcreq-manual-classes/38-requested-uc.md`](../../standards/bcreq-manual-classes/38-requested-uc.md) | `catalog-39` | 0.1.2 | действует | `05ad16ea6550826a…` | `c4c393f2` | BL-187 |
| [`standards/bcreq-manual-classes/39-manifest-alignment.md`](../../standards/bcreq-manual-classes/39-manifest-alignment.md) | `catalog-39` | 0.1.2 | действует | `9dded5140dc11193…` | `c4c393f2` | BL-187 |
| [`standards/bcreq-manual-classes/README.md`](../../standards/bcreq-manual-classes/README.md) | `catalog-39` | 0.2.2 | действует | `ba284fe195e9c309…` | `c423d078` | BL-187 |
| [`standards/bcreq-manual-classes/catalog.json`](../../standards/bcreq-manual-classes/catalog.json) | `catalog-39` | 0.2 | действует | `f84a948aec19cdad…` | `93429d00` | BL-187 |
| [`standards/bcreq-sections/01-glossary.md`](../../standards/bcreq-sections/01-glossary.md) | `section-meta-standards` | 0.3 | действует | `7eb9d85072ad69e9…` | `ecba9b76` | BL-187 |
| [`standards/bcreq-sections/02-business-context.md`](../../standards/bcreq-sections/02-business-context.md) | `section-meta-standards` | 0.3 | действует | `20f904bf28e359d8…` | `ecba9b76` | BL-187 |
| [`standards/bcreq-sections/03-functional-requirements.md`](../../standards/bcreq-sections/03-functional-requirements.md) | `section-meta-standards` | 0.2 | действует | `565e214fd87210d4…` | `89f26021` | BL-187 |
| [`standards/bcreq-sections/04-non-functional-requirements.md`](../../standards/bcreq-sections/04-non-functional-requirements.md) | `section-meta-standards` | 0.1 | действует | `684413ea3d16806c…` | `7f492682` | BL-187 |
| [`standards/bcreq-sections/05-solution-description.md`](../../standards/bcreq-sections/05-solution-description.md) | `section-meta-standards` | 0.2 | действует | `20c4a9de81673704…` | `93429d00` | BL-187 |
| [`standards/bcreq-sections/06-implementation-constraints.md`](../../standards/bcreq-sections/06-implementation-constraints.md) | `section-meta-standards` | 0.2 | действует | `7887c8347fc7bd62…` | `0ef70699` | BL-187 |
| [`standards/bcreq-sections/07-use-cases.md`](../../standards/bcreq-sections/07-use-cases.md) | `section-meta-standards` | 0.1 | действует | `44b299133d19189d…` | `e3216943` | BL-187 |
| [`standards/bcreq-sections/08-supplementary.md`](../../standards/bcreq-sections/08-supplementary.md) | `section-meta-standards` | 0.1 | действует | `e30f28e167eee744…` | `0ef70699` | BL-187 |
| [`standards/bcreq-sections/README.md`](../../standards/bcreq-sections/README.md) | `section-meta-standards` | 0.2 | действует | `c1cda832ffbd3c2e…` | `0ef70699` | BL-187 |
| [`standards/bcreq-industry-practice.md`](../../standards/bcreq-industry-practice.md) | `industry-practice` | 0.1 | действует | `7856e6b45f52c9b2…` | `09979430` | BL-187 |
| [`docs/ba-processes/bcreq-evidence-normalization.md`](../../docs/ba-processes/bcreq-evidence-normalization.md) | `evidence-normalization` | 0.1 | действует | `536151695ad208f0…` | `ae7ea98d` | BL-186 |
| [`standards/bcreq-lessons/README.md`](../../standards/bcreq-lessons/README.md) | `lessons` | 1.0 | действует | `dc8b255c38bf2224…` | `cbbf4a0d` | BL-187 |
| [`standards/bcreq-lessons/coverage.json`](../../standards/bcreq-lessons/coverage.json) | `lessons` | — | действует | `af8ada9a3ae2bd68…` | `049faf1f` | BL-187 |
| [`standards/bcreq-lessons/golden-set-bcreq-stage1.md`](../../standards/bcreq-lessons/golden-set-bcreq-stage1.md) | `lessons` | 0.1 | действует | `fff8b8c1af9d5d59…` | `6d3aa075` | BL-187 |
| [`standards/bcreq-lessons/lessons.json`](../../standards/bcreq-lessons/lessons.json) | `lessons` | 1.0 | действует | `568b68c3d01ffc7d…` | `cbbf4a0d` | BL-187 |
| [`standards/bcreq-lessons/rubric-bcreq-stage1.md`](../../standards/bcreq-lessons/rubric-bcreq-stage1.md) | `lessons` | 0.1 | действует | `4507a990a879df5e…` | `6377e5dd` | BL-187 |
| [`standards/bcreq-runtime-references.md`](../../standards/bcreq-runtime-references.md) | `runtime-references` | 0.5 | действует | `7245a80e491dd3e7…` | `519be3ce` | BL-187 |
| [`standards/bcreq-composition-standard.md`](../../standards/bcreq-composition-standard.md) | `execution-norms` | 0.2 | действует | `28acb16f0ae0cdc6…` | `09979430` | BL-187 |
| [`standards/bcreq-prompt-architecture.md`](../../standards/bcreq-prompt-architecture.md) | `execution-norms` | 0.1.1 | действует | `78e2fcc4d3027b53…` | `cbbf4a0d` | BL-187 |
| [`standards/product-classification-contract.md`](../../standards/product-classification-contract.md) | `execution-norms` | 0.1 | действует | `312f599b56f66a3e…` | `01fae51c` | BL-187 |
| [`docs/ba-processes/cs-flow-stub.md`](../../docs/ba-processes/cs-flow-stub.md) | `gates-and-cs` | 0.1 | действует | `ce37ef29da3bf07a…` | `632007c0` | BL-188 |
| [`docs/contracts/bcreq-stage-gates.md`](../../docs/contracts/bcreq-stage-gates.md) | `gates-and-cs` | 0.3.0 | действует | `327c22bbda4bf79d…` | `cf9de728` | BL-188 |
