---
status: ready
version: 0.2
updated: 2026-11-27
temperature: 0.1
owner: G-Ivan-A
type: contract
scope: ssot-stage1-handoff
related_artifacts:
  - "docs/contracts/ssot-stage1-handoff-manifest.json"
  - "docs/contracts/ssot-stage1-link-map.json"
  - "docs/rfc/2026-11-runtime-ide-orchestrator.md"
  - "docs/audit/2026-11-18-runtime-dependencies-ssot-handoff.md"
  - "standards/bcreq-runtime-references.md"
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/492"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/506"
---

# Манифест передачи SSOT этапа 1 в mango-ba-ai-runtime (issue #492)

Сгенерировано `experiments/issue_492/build_ssot_manifest.py` из [JSON-манифеста](ssot-stage1-handoff-manifest.json); не править вручную.
Редакция 0.2, статус: ready: передача №1 выставлена в runtime (M2). Заменяет редакцию 0.1 (`7dea8f71`, merge PR #491): Байты 0.1 устарели: после 7dea8f71 изменились 112 из 133 артефактов; в 0.1 нет карты гейтов IDE и ручного процесса, без которых оркестратор runtime отвечает ACCESS_GAP; правило 5 противоречило побайтной копии (Р-RT-7). Runtime этой задачей не менялся.

- Источник: `G-Ivan-A/mango_ba_prompts` на коммите `40ef5edd0938b9a5e961dec2e46e625b6c7a2576` (merge PR #514).
- Получатель: `G-Ivan-A/mango-ba-ai-runtime`; SHA реестра справочников `68ad8fcffd47439fc3051852d9a2fbbe23815855`, наблюдавшийся main `4bd5597f82ba00c5494ee8825f01257c0ba4acef`.
- Хэш: sha256 байтов файла на source_commit. Клиентские данные и вложения не включаются: только пути, версии, хэши и метаданные; пути runs/, kb/, inputs/, attachments/ запрещены.
- Артефактов: 135; контрактов шагов A-IN: 24; уже есть в runtime побайтно: 0.
- Статусы цепочки: архив — 6, действует — 123, заменён — 6.

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
| `ide-gates` | Карта гейтов IDE и ручной процесс этапа 1 (RFC-RT-003, M2) | 2 | действует 2 | BL-188 |

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
5. Байты ссылок не переписываются (Р-RT-7, вариант 7а). Копия лежит в `ssot/mango_ba_prompts/` с путями источника, поэтому относительная ссылка на перенесённую цель работает без правки. Цель вне передачи разрешается по карте ссылок `docs/contracts/ssot-stage1-link-map.json` на permalink спицы на `source_commit`; агент без доступа к спице отвечает `ACCESS_GAP`, а не восстанавливает цель по памяти. Нормативные цели вне передачи — кандидаты следующей передачи.
6. Тексты промптов в спице ради передачи не меняются; замена ссылок (б) в спице — отдельная задача BL-190.

Прецеденты:

- `G-Ivan-A/mango_ba_prompts`: ADR-0004 и scripts/sync_from_hub.py: рабочие копии Хаба на `source_sha`, локальные правки запрещены, обновление — следующим синком; .hub-profile.json хранит last_sync и sync_history.
- `G-Ivan-A/mango-ba-ai-runtime`: compilation-manifest.yaml: база знаний скопирована из спицы на 8cbf82aa73129ec5747af07f790aaf438b0fb6e9, каталог продуктов — на e3597fd74da9c4f631ca46697c643462e2cf0b85; `hub_access_required_at_runtime: false`.

Приём манифеста — задача runtime M2 (BL-185…BL-188), выставлена по поручению владельца в PR #514; раздел 12 RFC-RT-003.

Р-RT-7 → 7а (RFC-RT-002, раздел 9): правило 5 редакции 0.1 требовало переписывать ссылки, а правила 1, 2 и 4 — побайтную копию со сверкой sha256; оба требования вместе невыполнимы. 7а сохраняет сверку sha256 и требование ФТ-3 #492 о нормативных ссылках.

Передача №1 (M2 (RFC-RT-003, раздел 8), BL-185, BL-186, BL-187, BL-188): каталог `ssot/mango_ba_prompts/`, путь артефакта в runtime = target_dir + путь в спице; в target_dir нет других файлов. Журнал передач — `ssot/TRANSFERS.md`, копия манифеста — `ssot/mango_ba_prompts.manifest.json`, копия карты ссылок — `ssot/mango_ba_prompts.link-map.json`. Постановка — docs/rfc/2026-11-runtime-ide-orchestrator.md, раздел 12.

## 4. Маршрут A-IN: 24 контракта шагов

| Шаг | Название | Операция | Дальше | Версия маршрута | Промпт | Версия | sha256 промпта | sha256 инструкции |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AIN-01 | Правила и версия | К-36 | AIN-02 | 0.3 | [`bcreq-ain-01-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-01-understanding-stepwise.md) | 0.5 | `67aa58094ade7557…` | `68479e59c47fb36b…` |
| AIN-02 | Данные у БА | К-01 | AIN-03 | 0.3 | [`bcreq-ain-02-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-02-understanding-stepwise.md) | 0.5 | `abec309597578bc8…` | `70b56c9a5aff565c…` |
| AIN-03 | Реестр источников | К-01, К-09 | AIN-04 | 0.3 | [`bcreq-ain-03-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-03-understanding-stepwise.md) | 0.5 | `023362c6bfbe016e…` | `4c3881f82aad0681…` |
| AIN-04 | Атомизация | К-02 | AIN-05 | 0.3 | [`bcreq-ain-04-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-04-understanding-stepwise.md) | 0.5 | `104034ee90517bb0…` | `2204d5929d3998ac…` |
| AIN-05 | Качество и смысл | К-03 | AIN-06 | 0.3 | [`bcreq-ain-05-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-05-understanding-stepwise.md) | 0.5 | `e609974971956ba5…` | `c7a28844d8fca958…` |
| AIN-06 | Кандидаты продуктов | К-05 | AIN-07 | 0.3 | [`bcreq-ain-06-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-06-understanding-stepwise.md) | 0.5 | `b31146da36d44512…` | `ef730c9baa03b21f…` |
| AIN-07 | План retrieval | К-07, К-08, К-11 | AIN-08 | 0.3 | [`bcreq-ain-07-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-07-understanding-stepwise.md) | 0.5 | `cd035e2a62779a08…` | `335ef7159596546b…` |
| AIN-08 | Веб-извлечение | К-07 | AIN-09 | 0.3 | [`bcreq-ain-08-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-08-understanding-stepwise.md) | 0.5 | `c190df682d773846…` | `cb1f85a5f8c889ea…` |
| AIN-09 | Извлечение БЗ | К-08 | AIN-10 | 0.3 | [`bcreq-ain-09-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-09-understanding-stepwise.md) | 0.5 | `45d29da0dfa40162…` | `1692094c330c82d1…` |
| AIN-10 | Замыкание зависимостей | К-11 | AIN-11 | 0.3 | [`bcreq-ain-10-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-10-understanding-stepwise.md) | 0.5 | `4ac6c4e1d85429d0…` | `29c17487cbea798c…` |
| AIN-11 | Сверка противоречий | К-10 | AIN-12 | 0.3 | [`bcreq-ain-11-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-11-understanding-stepwise.md) | 0.5 | `adb796213c27f719…` | `894d1f6b18b858e9…` |
| AIN-12 | Исполнимость сейчас | К-05, К-06 | AIN-13 | 0.3 | [`bcreq-ain-12-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-12-understanding-stepwise.md) | 0.5 | `0654f0d721309750…` | `a9bfe0b3e01e0bac…` |
| AIN-13 | Согласование пула | К-05, К-34 | AIN-14 | 0.3 | [`bcreq-ain-13-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-13-understanding-stepwise.md) | 0.5 | `064d8dfced880a47…` | `11606b8c6de6db4b…` |
| AIN-14 | Словарь — раздел 1 | К-14 | AIN-15 | 0.3 | [`bcreq-ain-14-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-14-understanding-stepwise.md) | 0.5 | `ac269d0d720bd1ee…` | `4dcc12043810d7df…` |
| AIN-15 | Остаточные пробелы | К-03 | AIN-16 | 0.3 | [`bcreq-ain-15-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-15-understanding-stepwise.md) | 0.5 | `4faad889d3f5f4da…` | `390981a385d62e3a…` |
| AIN-16 | Вопросы Заказчику | К-04 | AIN-17 | 0.3 | [`bcreq-ain-16-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-16-understanding-stepwise.md) | 0.5 | `14686e81c8826b8b…` | `86ec756d44b7fb5f…` |
| AIN-17 | Решение БА по вопросам | К-34 | AIN-18 | 0.3 | [`bcreq-ain-17-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-17-understanding-stepwise.md) | 0.5 | `0f84b032ba1ab29d…` | `6436b56866875409…` |
| AIN-18 | Новые данные | К-09 | AIN-19 | 0.3 | [`bcreq-ain-18-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-18-understanding-stepwise.md) | 0.5 | `62ae2ab2dc1f4ed1…` | `a3389f6a625c794d…` |
| AIN-19 | Повторная нормализация | К-02, К-29 | AIN-20 | 0.3 | [`bcreq-ain-19-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-19-understanding-stepwise.md) | 0.5 | `54a923a598413218…` | `56ca7f90c829df03…` |
| AIN-20 | Снимок памяти | К-13, К-35 | AIN-21 | 0.3 | [`bcreq-ain-20-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-20-understanding-stepwise.md) | 0.5 | `cc3e3c00f4a46e53…` | `f30223a430bbad7a…` |
| AIN-21 | Гейт до раздела 2 | К-20, К-34 | AIN-22 | 0.3 | [`bcreq-ain-21-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-21-understanding-stepwise.md) | 0.5 | `e430040b9a187961…` | `db225e1987661eb8…` |
| AIN-22 | Сборка раздела 2 | К-15 | AIN-23 | 0.3 | [`bcreq-ain-22-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-22-understanding-stepwise.md) | 0.5 | `1fc5aad251ecd5e8…` | `29aba58506be90e3…` |
| AIN-23 | Проверка раздела 2 | К-28, К-31 | AIN-24 | 0.3 | [`bcreq-ain-23-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-23-understanding-stepwise.md) | 0.5 | `cef91f02cee6ca9b…` | `bda63703cbff2f0a…` |
| AIN-24 | Г-IN и передача | К-35 | A-CORE или CS по решению БА | 0.3 | [`bcreq-ain-24-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-24-understanding-stepwise.md) | 0.5 | `d551ede6cffe5f06…` | `e7148459193e4ba5…` |

## 5. Артефакты

Полные sha256 и коммиты последнего изменения — в JSON.

| Путь | Группа | Версия | Статус цепочки | sha256 | Последнее изменение | Карточка |
| --- | --- | --- | --- | --- | --- | --- |
| [`docs/ba-processes/bcreq-a-in-common.md`](../../docs/ba-processes/bcreq-a-in-common.md) | `ain-route` | 0.5 | действует | `660e3f923ab840b1…` | `b7bd94c7` | BL-186 |
| [`docs/ba-processes/bcreq-a-in-execution.md`](../../docs/ba-processes/bcreq-a-in-execution.md) | `ain-route` | 0.5 | действует | `936cd3ac27e78624…` | `b7bd94c7` | BL-186 |
| [`docs/ba-processes/bcreq-a-in-instructions.json`](../../docs/ba-processes/bcreq-a-in-instructions.json) | `ain-route` | — | действует | `3bef884db6a9b5df…` | `b7bd94c7` | BL-186 |
| [`docs/ba-processes/bcreq-a-in-route.json`](../../docs/ba-processes/bcreq-a-in-route.json) | `ain-route` | 0.3 | действует | `5cec366507d980c0…` | `4ef8e45c` | BL-186 |
| [`docs/rfc/2026-11-a-in-decomposition.md`](../../docs/rfc/2026-11-a-in-decomposition.md) | `ain-route` | 0.7 | действует | `27e32db65fac4606…` | `4ef8e45c` | BL-186 |
| [`prompts/drafts/a-in/bcreq-ain-01-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-01-understanding-stepwise.md) | `ain-route` | 0.5 | действует | `67aa58094ade7557…` | `b7bd94c7` | BL-186 |
| [`prompts/drafts/a-in/bcreq-ain-02-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-02-understanding-stepwise.md) | `ain-route` | 0.5 | действует | `abec309597578bc8…` | `b7bd94c7` | BL-186 |
| [`prompts/drafts/a-in/bcreq-ain-03-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-03-understanding-stepwise.md) | `ain-route` | 0.5 | действует | `023362c6bfbe016e…` | `b7bd94c7` | BL-186 |
| [`prompts/drafts/a-in/bcreq-ain-04-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-04-understanding-stepwise.md) | `ain-route` | 0.5 | действует | `104034ee90517bb0…` | `b7bd94c7` | BL-186 |
| [`prompts/drafts/a-in/bcreq-ain-05-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-05-understanding-stepwise.md) | `ain-route` | 0.5 | действует | `e609974971956ba5…` | `b7bd94c7` | BL-186 |
| [`prompts/drafts/a-in/bcreq-ain-06-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-06-understanding-stepwise.md) | `ain-route` | 0.5 | действует | `b31146da36d44512…` | `b7bd94c7` | BL-186 |
| [`prompts/drafts/a-in/bcreq-ain-07-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-07-understanding-stepwise.md) | `ain-route` | 0.5 | действует | `cd035e2a62779a08…` | `b7bd94c7` | BL-186 |
| [`prompts/drafts/a-in/bcreq-ain-08-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-08-understanding-stepwise.md) | `ain-route` | 0.5 | действует | `c190df682d773846…` | `b7bd94c7` | BL-186 |
| [`prompts/drafts/a-in/bcreq-ain-09-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-09-understanding-stepwise.md) | `ain-route` | 0.5 | действует | `45d29da0dfa40162…` | `b7bd94c7` | BL-186 |
| [`prompts/drafts/a-in/bcreq-ain-10-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-10-understanding-stepwise.md) | `ain-route` | 0.5 | действует | `4ac6c4e1d85429d0…` | `b7bd94c7` | BL-186 |
| [`prompts/drafts/a-in/bcreq-ain-11-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-11-understanding-stepwise.md) | `ain-route` | 0.5 | действует | `adb796213c27f719…` | `b7bd94c7` | BL-186 |
| [`prompts/drafts/a-in/bcreq-ain-12-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-12-understanding-stepwise.md) | `ain-route` | 0.5 | действует | `0654f0d721309750…` | `b7bd94c7` | BL-186 |
| [`prompts/drafts/a-in/bcreq-ain-13-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-13-understanding-stepwise.md) | `ain-route` | 0.5 | действует | `064d8dfced880a47…` | `b7bd94c7` | BL-186 |
| [`prompts/drafts/a-in/bcreq-ain-14-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-14-understanding-stepwise.md) | `ain-route` | 0.5 | действует | `ac269d0d720bd1ee…` | `b7bd94c7` | BL-186 |
| [`prompts/drafts/a-in/bcreq-ain-15-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-15-understanding-stepwise.md) | `ain-route` | 0.5 | действует | `4faad889d3f5f4da…` | `b7bd94c7` | BL-186 |
| [`prompts/drafts/a-in/bcreq-ain-16-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-16-understanding-stepwise.md) | `ain-route` | 0.5 | действует | `14686e81c8826b8b…` | `b7bd94c7` | BL-186 |
| [`prompts/drafts/a-in/bcreq-ain-17-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-17-understanding-stepwise.md) | `ain-route` | 0.5 | действует | `0f84b032ba1ab29d…` | `b7bd94c7` | BL-186 |
| [`prompts/drafts/a-in/bcreq-ain-18-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-18-understanding-stepwise.md) | `ain-route` | 0.5 | действует | `62ae2ab2dc1f4ed1…` | `b7bd94c7` | BL-186 |
| [`prompts/drafts/a-in/bcreq-ain-19-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-19-understanding-stepwise.md) | `ain-route` | 0.5 | действует | `54a923a598413218…` | `b7bd94c7` | BL-186 |
| [`prompts/drafts/a-in/bcreq-ain-20-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-20-understanding-stepwise.md) | `ain-route` | 0.5 | действует | `cc3e3c00f4a46e53…` | `b7bd94c7` | BL-186 |
| [`prompts/drafts/a-in/bcreq-ain-21-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-21-understanding-stepwise.md) | `ain-route` | 0.5 | действует | `e430040b9a187961…` | `b7bd94c7` | BL-186 |
| [`prompts/drafts/a-in/bcreq-ain-22-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-22-understanding-stepwise.md) | `ain-route` | 0.5 | действует | `1fc5aad251ecd5e8…` | `b7bd94c7` | BL-186 |
| [`prompts/drafts/a-in/bcreq-ain-23-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-23-understanding-stepwise.md) | `ain-route` | 0.5 | действует | `cef91f02cee6ca9b…` | `b7bd94c7` | BL-186 |
| [`prompts/drafts/a-in/bcreq-ain-24-understanding-stepwise.md`](../../prompts/drafts/a-in/bcreq-ain-24-understanding-stepwise.md) | `ain-route` | 0.5 | действует | `d551ede6cffe5f06…` | `b7bd94c7` | BL-186 |
| [`prompts/drafts/system/bcreq-context-understanding-system.md`](../../prompts/drafts/system/bcreq-context-understanding-system.md) | `system-format` | 0.5 | действует | `4919b4d3177fe3bb…` | `b7bd94c7` | BL-185 |
| [`prompts/drafts/system/bcreq-intake-questionnaire-system.md`](../../prompts/drafts/system/bcreq-intake-questionnaire-system.md) | `system-format` | 0.5 | действует | `4e040d46390b74a7…` | `b7bd94c7` | BL-185 |
| [`prompts/drafts/system/bcreq-products-impact-analysis-system.md`](../../prompts/drafts/system/bcreq-products-impact-analysis-system.md) | `system-format` | 0.5 | действует | `5dbed9cf2bd58e71…` | `b7bd94c7` | BL-185 |
| [`prompts/archive/a-in-v2.7.0/README.md`](../../prompts/archive/a-in-v2.7.0/README.md) | `archive-2.7.0` | — | архив | `52ffb824f46ec727…` | `95a6dfe6` | BL-185 |
| [`prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md`](../../prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md) | `archive-2.7.0` | 0.3 | архив | `73808f55708e07cc…` | `ff37f10c` | BL-185 |
| [`prompts/archive/a-in-v2.7.0/bcreq-in-understanding-oneshot.md`](../../prompts/archive/a-in-v2.7.0/bcreq-in-understanding-oneshot.md) | `archive-2.7.0` | 0.2 | архив | `9b1291785c3f862b…` | `9a2a20a4` | BL-185 |
| [`prompts/archive/a-in-v2.7.0/bcreq-intake-questionnaire-stepwise.md`](../../prompts/archive/a-in-v2.7.0/bcreq-intake-questionnaire-stepwise.md) | `archive-2.7.0` | 0.1 | архив | `14edd82b28af0301…` | `ff37f10c` | BL-185 |
| [`prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md`](../../prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md) | `archive-2.7.0` | 0.2 | архив | `2e6854bb7c7b62b7…` | `ff37f10c` | BL-185 |
| [`prompts/archive/a-in-v2.7.0/manifest.json`](../../prompts/archive/a-in-v2.7.0/manifest.json) | `archive-2.7.0` | 2.7.0 | архив | `0efeec829a8e2535…` | `95a6dfe6` | BL-185 |
| [`prompts/drafts/bcreq-constitution-governance-oneshot.md`](../../prompts/drafts/bcreq-constitution-governance-oneshot.md) | `drafts` | 0.5 | действует | `304d078988767866…` | `b7bd94c7` | BL-185 |
| [`prompts/drafts/bcreq-constraints-documentation-stepwise.md`](../../prompts/drafts/bcreq-constraints-documentation-stepwise.md) | `drafts` | 0.5 | действует | `71ed530aa176ce89…` | `b7bd94c7` | BL-185 |
| [`prompts/drafts/bcreq-context-understanding-stepwise.md`](../../prompts/drafts/bcreq-context-understanding-stepwise.md) | `drafts` | 0.5 | заменён | `476086276b842776…` | `b7bd94c7` | BL-185 |
| [`prompts/drafts/bcreq-extra-risk-analysis-stepwise.md`](../../prompts/drafts/bcreq-extra-risk-analysis-stepwise.md) | `drafts` | 0.5 | действует | `aac7ab3221cddca6…` | `b7bd94c7` | BL-185 |
| [`prompts/drafts/bcreq-fr-documentation-stepwise.md`](../../prompts/drafts/bcreq-fr-documentation-stepwise.md) | `drafts` | 0.5 | действует | `66abd8a73eb21deb…` | `b7bd94c7` | BL-185 |
| [`prompts/drafts/bcreq-intake-questionnaire-stepwise.md`](../../prompts/drafts/bcreq-intake-questionnaire-stepwise.md) | `drafts` | 0.5 | заменён | `746cc97b50b41750…` | `b7bd94c7` | BL-185 |
| [`prompts/drafts/bcreq-nfr-documentation-stepwise.md`](../../prompts/drafts/bcreq-nfr-documentation-stepwise.md) | `drafts` | 0.5 | действует | `de639330e5ba61e8…` | `b7bd94c7` | BL-185 |
| [`prompts/drafts/bcreq-orr-solution-design-stepwise.md`](../../prompts/drafts/bcreq-orr-solution-design-stepwise.md) | `drafts` | 0.5 | действует | `cf3b2c4d3d051ed6…` | `b7bd94c7` | BL-185 |
| [`prompts/drafts/bcreq-products-impact-analysis-stepwise.md`](../../prompts/drafts/bcreq-products-impact-analysis-stepwise.md) | `drafts` | 0.5 | заменён | `fa891268f3238732…` | `b7bd94c7` | BL-185 |
| [`prompts/drafts/bcreq-release-readiness-oneshot.md`](../../prompts/drafts/bcreq-release-readiness-oneshot.md) | `drafts` | 0.5 | действует | `21d7b97efc110210…` | `b7bd94c7` | BL-185 |
| [`prompts/drafts/bcreq-review-validation-oneshot.md`](../../prompts/drafts/bcreq-review-validation-oneshot.md) | `drafts` | 0.4 | действует | `1c665fcdee03e98f…` | `af5b34da` | BL-185 |
| [`prompts/drafts/bcreq-scenarios-modeling-oneshot.md`](../../prompts/drafts/bcreq-scenarios-modeling-oneshot.md) | `drafts` | 0.3 | действует | `6dd1f7eb34dc312b…` | `af5b34da` | BL-185 |
| [`prompts/drafts/bcreq-uc-modeling-stepwise.md`](../../prompts/drafts/bcreq-uc-modeling-stepwise.md) | `drafts` | 0.5 | действует | `dcaebc13c0b4e6d6…` | `b7bd94c7` | BL-185 |
| [`prompts/drafts/manifest.json`](../../prompts/drafts/manifest.json) | `drafts` | — | действует | `4820add6abbb87fc…` | `af5b34da` | BL-185 |
| [`docs/ba-processes/bcreq-run-kit.md`](../../docs/ba-processes/bcreq-run-kit.md) | `prompts-v0.1` | 0.13 | действует | `ecaf6022b85e96ef…` | `b7bd94c7` | BL-185 |
| [`prompts/bcreq-constitution-governance-oneshot.md`](../../prompts/bcreq-constitution-governance-oneshot.md) | `prompts-v0.1` | 0.6 | действует | `794b4df122dca054…` | `af5b34da` | BL-185 |
| [`prompts/bcreq-constraints-documentation-stepwise.md`](../../prompts/bcreq-constraints-documentation-stepwise.md) | `prompts-v0.1` | 0.3 | действует | `b11e8c4429ce4136…` | `af5b34da` | BL-185 |
| [`prompts/bcreq-context-understanding-stepwise.md`](../../prompts/bcreq-context-understanding-stepwise.md) | `prompts-v0.1` | 0.6 | заменён | `8183dd1872fcef66…` | `af5b34da` | BL-185 |
| [`prompts/bcreq-core-documentation-oneshot.md`](../../prompts/bcreq-core-documentation-oneshot.md) | `prompts-v0.1` | 0.5 | действует | `fed8629940bfff37…` | `af5b34da` | BL-185 |
| [`prompts/bcreq-extra-risk-analysis-stepwise.md`](../../prompts/bcreq-extra-risk-analysis-stepwise.md) | `prompts-v0.1` | 0.3 | действует | `16f581591b9ad0a4…` | `af5b34da` | BL-185 |
| [`prompts/bcreq-fr-documentation-stepwise.md`](../../prompts/bcreq-fr-documentation-stepwise.md) | `prompts-v0.1` | 0.6 | действует | `27dfe183a84460de…` | `af5b34da` | BL-185 |
| [`prompts/bcreq-in-understanding-oneshot.md`](../../prompts/bcreq-in-understanding-oneshot.md) | `prompts-v0.1` | 0.5 | заменён | `6dee2a0cfd201d26…` | `af5b34da` | BL-185 |
| [`prompts/bcreq-nfr-documentation-stepwise.md`](../../prompts/bcreq-nfr-documentation-stepwise.md) | `prompts-v0.1` | 0.3 | действует | `af1acb878a87497a…` | `af5b34da` | BL-185 |
| [`prompts/bcreq-orr-solution-design-stepwise.md`](../../prompts/bcreq-orr-solution-design-stepwise.md) | `prompts-v0.1` | 0.4 | действует | `a3625617be079c43…` | `af5b34da` | BL-185 |
| [`prompts/bcreq-products-impact-analysis-stepwise.md`](../../prompts/bcreq-products-impact-analysis-stepwise.md) | `prompts-v0.1` | 0.5 | заменён | `59babf58f4e8ba88…` | `af5b34da` | BL-185 |
| [`prompts/bcreq-review-validation-oneshot.md`](../../prompts/bcreq-review-validation-oneshot.md) | `prompts-v0.1` | 0.4 | действует | `46466fdb6608aa46…` | `af5b34da` | BL-185 |
| [`prompts/bcreq-scenarios-modeling-oneshot.md`](../../prompts/bcreq-scenarios-modeling-oneshot.md) | `prompts-v0.1` | 0.3 | действует | `5bc6187a97807c86…` | `af5b34da` | BL-185 |
| [`prompts/bcreq-uc-modeling-stepwise.md`](../../prompts/bcreq-uc-modeling-stepwise.md) | `prompts-v0.1` | 0.3 | действует | `5ed17d013e50e514…` | `af5b34da` | BL-185 |
| [`prompts/bcreq-work-solution-design-oneshot.md`](../../prompts/bcreq-work-solution-design-oneshot.md) | `prompts-v0.1` | 0.3 | действует | `7ec116ca037a1ef2…` | `af5b34da` | BL-185 |
| [`docs/ba-processes/bcreq-step-handoff.md`](../../docs/ba-processes/bcreq-step-handoff.md) | `step-handoff` | 0.3 | действует | `fb624f5bbeb5ee9d…` | `b7bd94c7` | BL-186 |
| [`standards/bcreq-prompt-base-standard.md`](../../standards/bcreq-prompt-base-standard.md) | `base-standard` | 0.1.3 | действует | `41fdd64f6cc480cf…` | `d2e95b65` | BL-187 |
| [`standards/bcreq-prompt-profiles.md`](../../standards/bcreq-prompt-profiles.md) | `base-standard` | 0.1.3 | действует | `a7480eef8ab57c25…` | `3ed187b8` | BL-187 |
| [`standards/bcreq-manual-classes/01-intake.md`](../../standards/bcreq-manual-classes/01-intake.md) | `catalog-39` | 0.1.3 | действует | `c183b8d5cfdde5a9…` | `9a2a20a4` | BL-187 |
| [`standards/bcreq-manual-classes/02-normalize.md`](../../standards/bcreq-manual-classes/02-normalize.md) | `catalog-39` | 0.1.2 | действует | `729b63c8dac040da…` | `9a2a20a4` | BL-187 |
| [`standards/bcreq-manual-classes/03-ambiguity.md`](../../standards/bcreq-manual-classes/03-ambiguity.md) | `catalog-39` | 0.1.2 | действует | `d807e3ec6654b819…` | `9a2a20a4` | BL-187 |
| [`standards/bcreq-manual-classes/04-questions.md`](../../standards/bcreq-manual-classes/04-questions.md) | `catalog-39` | 0.1.2 | действует | `c14e209cc14e70ef…` | `9a2a20a4` | BL-187 |
| [`standards/bcreq-manual-classes/05-taxonomy.md`](../../standards/bcreq-manual-classes/05-taxonomy.md) | `catalog-39` | 0.1.2 | действует | `62fac640ba44e0a0…` | `3ed187b8` | BL-187 |
| [`standards/bcreq-manual-classes/06-scope.md`](../../standards/bcreq-manual-classes/06-scope.md) | `catalog-39` | 0.1.2 | действует | `49f6974bfb8758c2…` | `9a2a20a4` | BL-187 |
| [`standards/bcreq-manual-classes/07-web-evidence.md`](../../standards/bcreq-manual-classes/07-web-evidence.md) | `catalog-39` | 0.1.2 | действует | `6d62d11c9a90242e…` | `9a2a20a4` | BL-187 |
| [`standards/bcreq-manual-classes/08-document-evidence.md`](../../standards/bcreq-manual-classes/08-document-evidence.md) | `catalog-39` | 0.1.2 | действует | `d06af9db0733b206…` | `9a2a20a4` | BL-187 |
| [`standards/bcreq-manual-classes/09-ba-enrichment.md`](../../standards/bcreq-manual-classes/09-ba-enrichment.md) | `catalog-39` | 0.1.2 | действует | `e596b5e0806eb27f…` | `9a2a20a4` | BL-187 |
| [`standards/bcreq-manual-classes/10-source-conflicts.md`](../../standards/bcreq-manual-classes/10-source-conflicts.md) | `catalog-39` | 0.1.2 | действует | `0430d08093b67ff4…` | `9a2a20a4` | BL-187 |
| [`standards/bcreq-manual-classes/11-dependency-check.md`](../../standards/bcreq-manual-classes/11-dependency-check.md) | `catalog-39` | 0.1.2 | действует | `731d44e04a648c01…` | `9a2a20a4` | BL-187 |
| [`standards/bcreq-manual-classes/12-phase-assembly.md`](../../standards/bcreq-manual-classes/12-phase-assembly.md) | `catalog-39` | 0.1.2 | действует | `06ae712594a48e02…` | `9a2a20a4` | BL-187 |
| [`standards/bcreq-manual-classes/13-handoff-check.md`](../../standards/bcreq-manual-classes/13-handoff-check.md) | `catalog-39` | 0.1.2 | действует | `0ee6c6360d71b874…` | `9a2a20a4` | BL-187 |
| [`standards/bcreq-manual-classes/14-glossary.md`](../../standards/bcreq-manual-classes/14-glossary.md) | `catalog-39` | 0.1.3 | действует | `039e60219d51c5ac…` | `9a2a20a4` | BL-187 |
| [`standards/bcreq-manual-classes/15-business-context.md`](../../standards/bcreq-manual-classes/15-business-context.md) | `catalog-39` | 0.1.3 | действует | `761aeb03bb1b19f2…` | `9a2a20a4` | BL-187 |
| [`standards/bcreq-manual-classes/16-fr-delta.md`](../../standards/bcreq-manual-classes/16-fr-delta.md) | `catalog-39` | 0.1.3 | действует | `9c3defb8c41bd0de…` | `9a2a20a4` | BL-187 |
| [`standards/bcreq-manual-classes/17-fr-new.md`](../../standards/bcreq-manual-classes/17-fr-new.md) | `catalog-39` | 0.1.3 | действует | `53f7935a4f0fce5e…` | `9a2a20a4` | BL-187 |
| [`standards/bcreq-manual-classes/18-nfr.md`](../../standards/bcreq-manual-classes/18-nfr.md) | `catalog-39` | 0.1.2 | действует | `fc6bf0d3b38dbcd4…` | `9a2a20a4` | BL-187 |
| [`standards/bcreq-manual-classes/19-uc-coverage.md`](../../standards/bcreq-manual-classes/19-uc-coverage.md) | `catalog-39` | 0.1.2 | действует | `55dc8e130787fda0…` | `9a2a20a4` | BL-187 |
| [`standards/bcreq-manual-classes/20-gate-evidence.md`](../../standards/bcreq-manual-classes/20-gate-evidence.md) | `catalog-39` | 0.1.2 | действует | `235c630ae2036ac2…` | `9a2a20a4` | BL-187 |
| [`standards/bcreq-manual-classes/21-solution-l1.md`](../../standards/bcreq-manual-classes/21-solution-l1.md) | `catalog-39` | 0.1.3 | действует | `3c1f1b8fa6248dc5…` | `9a2a20a4` | BL-187 |
| [`standards/bcreq-manual-classes/22-solution-l2.md`](../../standards/bcreq-manual-classes/22-solution-l2.md) | `catalog-39` | 0.1.3 | действует | `a097ec77f027e155…` | `9a2a20a4` | BL-187 |
| [`standards/bcreq-manual-classes/23-constraints.md`](../../standards/bcreq-manual-classes/23-constraints.md) | `catalog-39` | 0.1.3 | действует | `c1b06ab13e13f192…` | `9a2a20a4` | BL-187 |
| [`standards/bcreq-manual-classes/24-uc-boundaries.md`](../../standards/bcreq-manual-classes/24-uc-boundaries.md) | `catalog-39` | 0.1.2 | действует | `d0c04f1e9c5a18b0…` | `9a2a20a4` | BL-187 |
| [`standards/bcreq-manual-classes/25-risks.md`](../../standards/bcreq-manual-classes/25-risks.md) | `catalog-39` | 0.1.2 | действует | `7cc94f1873bca514…` | `9a2a20a4` | BL-187 |
| [`standards/bcreq-manual-classes/26-delivery-dependencies.md`](../../standards/bcreq-manual-classes/26-delivery-dependencies.md) | `catalog-39` | 0.1.2 | действует | `4e8ca39b41b087db…` | `9a2a20a4` | BL-187 |
| [`standards/bcreq-manual-classes/27-acceptance.md`](../../standards/bcreq-manual-classes/27-acceptance.md) | `catalog-39` | 0.1.2 | действует | `bcae9ef4bf96fc5b…` | `9a2a20a4` | BL-187 |
| [`standards/bcreq-manual-classes/28-independent-review.md`](../../standards/bcreq-manual-classes/28-independent-review.md) | `catalog-39` | 0.1.2 | действует | `9d68f886e57256e2…` | `9a2a20a4` | BL-187 |
| [`standards/bcreq-manual-classes/29-impact.md`](../../standards/bcreq-manual-classes/29-impact.md) | `catalog-39` | 0.1.2 | действует | `9a85586791fcabb5…` | `9a2a20a4` | BL-187 |
| [`standards/bcreq-manual-classes/30-targeted-edit.md`](../../standards/bcreq-manual-classes/30-targeted-edit.md) | `catalog-39` | 0.1.2 | действует | `eb8d64166c00c17b…` | `9a2a20a4` | BL-187 |
| [`standards/bcreq-manual-classes/31-conformance.md`](../../standards/bcreq-manual-classes/31-conformance.md) | `catalog-39` | 0.1.2 | действует | `becaf13d4c694925…` | `9a2a20a4` | BL-187 |
| [`standards/bcreq-manual-classes/32-audience-projection.md`](../../standards/bcreq-manual-classes/32-audience-projection.md) | `catalog-39` | 0.1.2 | действует | `a7aed943fdddd16d…` | `9a2a20a4` | BL-187 |
| [`standards/bcreq-manual-classes/33-release-audit.md`](../../standards/bcreq-manual-classes/33-release-audit.md) | `catalog-39` | 0.1.2 | действует | `f30ef7605dc255d9…` | `9a2a20a4` | BL-187 |
| [`standards/bcreq-manual-classes/34-human-record.md`](../../standards/bcreq-manual-classes/34-human-record.md) | `catalog-39` | 0.1.2 | действует | `b2a45c25a093186d…` | `9a2a20a4` | BL-187 |
| [`standards/bcreq-manual-classes/35-baseline-handover.md`](../../standards/bcreq-manual-classes/35-baseline-handover.md) | `catalog-39` | 0.1.2 | действует | `e15a5aa5791c4500…` | `9a2a20a4` | BL-187 |
| [`standards/bcreq-manual-classes/36-rule-bundle.md`](../../standards/bcreq-manual-classes/36-rule-bundle.md) | `catalog-39` | 0.1.3 | действует | `d13a0af1b944f514…` | `9a2a20a4` | BL-187 |
| [`standards/bcreq-manual-classes/37-user-story.md`](../../standards/bcreq-manual-classes/37-user-story.md) | `catalog-39` | 0.1.2 | действует | `1a2ee63391da6d1d…` | `9a2a20a4` | BL-187 |
| [`standards/bcreq-manual-classes/38-requested-uc.md`](../../standards/bcreq-manual-classes/38-requested-uc.md) | `catalog-39` | 0.1.2 | действует | `ba86dab6e19c2c0e…` | `9a2a20a4` | BL-187 |
| [`standards/bcreq-manual-classes/39-manifest-alignment.md`](../../standards/bcreq-manual-classes/39-manifest-alignment.md) | `catalog-39` | 0.1.2 | действует | `ac5e9e91592ae0f0…` | `9a2a20a4` | BL-187 |
| [`standards/bcreq-manual-classes/README.md`](../../standards/bcreq-manual-classes/README.md) | `catalog-39` | 0.2.2 | действует | `ba284fe195e9c309…` | `c423d078` | BL-187 |
| [`standards/bcreq-manual-classes/catalog.json`](../../standards/bcreq-manual-classes/catalog.json) | `catalog-39` | 0.2 | действует | `48b01189f72b7d87…` | `3ed187b8` | BL-187 |
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
| [`docs/ba-processes/bcreq-evidence-normalization.md`](../../docs/ba-processes/bcreq-evidence-normalization.md) | `evidence-normalization` | 0.2 | действует | `cb904b8854a427e6…` | `b7bd94c7` | BL-186 |
| [`standards/bcreq-lessons/README.md`](../../standards/bcreq-lessons/README.md) | `lessons` | 1.0 | действует | `dc8b255c38bf2224…` | `cbbf4a0d` | BL-187 |
| [`standards/bcreq-lessons/coverage.json`](../../standards/bcreq-lessons/coverage.json) | `lessons` | — | действует | `af8ada9a3ae2bd68…` | `049faf1f` | BL-187 |
| [`standards/bcreq-lessons/golden-set-bcreq-stage1.md`](../../standards/bcreq-lessons/golden-set-bcreq-stage1.md) | `lessons` | 0.1 | действует | `fff8b8c1af9d5d59…` | `6d3aa075` | BL-187 |
| [`standards/bcreq-lessons/lessons.json`](../../standards/bcreq-lessons/lessons.json) | `lessons` | 1.0 | действует | `568b68c3d01ffc7d…` | `cbbf4a0d` | BL-187 |
| [`standards/bcreq-lessons/rubric-bcreq-stage1.md`](../../standards/bcreq-lessons/rubric-bcreq-stage1.md) | `lessons` | 0.1 | действует | `4507a990a879df5e…` | `6377e5dd` | BL-187 |
| [`standards/bcreq-runtime-references.md`](../../standards/bcreq-runtime-references.md) | `runtime-references` | 0.5 | действует | `2cd35fc1e64033b9…` | `af5b34da` | BL-187 |
| [`standards/bcreq-composition-standard.md`](../../standards/bcreq-composition-standard.md) | `execution-norms` | 0.2 | действует | `28acb16f0ae0cdc6…` | `09979430` | BL-187 |
| [`standards/bcreq-prompt-architecture.md`](../../standards/bcreq-prompt-architecture.md) | `execution-norms` | 0.1.1 | действует | `78e2fcc4d3027b53…` | `cbbf4a0d` | BL-187 |
| [`standards/product-classification-contract.md`](../../standards/product-classification-contract.md) | `execution-norms` | 0.1 | действует | `312f599b56f66a3e…` | `01fae51c` | BL-187 |
| [`docs/ba-processes/cs-flow-stub.md`](../../docs/ba-processes/cs-flow-stub.md) | `gates-and-cs` | 0.1 | действует | `ce37ef29da3bf07a…` | `632007c0` | BL-188 |
| [`docs/contracts/bcreq-stage-gates.md`](../../docs/contracts/bcreq-stage-gates.md) | `gates-and-cs` | 0.3.0 | действует | `327c22bbda4bf79d…` | `cf9de728` | BL-188 |
| [`docs/ba-processes/bcreq-ide-gates.json`](../../docs/ba-processes/bcreq-ide-gates.json) | `ide-gates` | 0.1 | действует | `d1e02b92cc1eb732…` | `e3270aa6` | BL-188 |
| [`docs/ba-processes/bcreq-manual-process.md`](../../docs/ba-processes/bcreq-manual-process.md) | `ide-gates` | 0.3 | действует | `d7035373aba2ef38…` | `b7bd94c7` | BL-188 |
