---
status: draft
version: 0.6
updated: 2026-08-21
temperature: 0.1
---

# Changelog — mango_ba_prompts

Все значимые изменения проекта документируются здесь. Формат основан на
[Keep a Changelog](https://keepachangelog.com/ru/1.1.0/); проект придерживается
[Semantic Versioning](https://semver.org/lang/ru/).

## Unreleased

### Added — Issue #276 реальный прогон 765 (RUN-0021) как Proof of Execution

- Добавлена запись [`runs/2026/RUN-0021/`](runs/2026/RUN-0021/outputs/README.md) —
  фиксация реально состоявшегося диалога БА с LLM по задаче 765 (ФТ на новый канал
  HeadHunter в МД/КЦ/ЛК): 26 реплик, 13 эпизодов, модель `qwen3.7-plus`, промпт
  [`fr-validation-stepwise`](prompts/fr-validation-stepwise.md). `run_type: statistics`
  — цель issue «зафиксировать прогон и результаты», а не выполнить процесс.
- Вход сохранён дословно
  ([`inputs/765-chat-export-1787301501556.json`](runs/2026/RUN-0021/inputs/765-chat-export-1787301501556.json))
  и развёрнут в транскрипт детерминированным скриптом
  ([`inputs/README.md`](runs/2026/RUN-0021/inputs/README.md)).
- Результат помечен как **промежуточный, не golden case**: финальный рендер ФТ v1.4
  не получен, часть замечаний сверки вынесена БА в отложенные
  ([`outputs/final-artifact.md`](runs/2026/RUN-0021/outputs/final-artifact.md)).
- Ключевая находка анализа
  ([`outputs/quality-findings.md`](runs/2026/RUN-0021/outputs/quality-findings.md)):
  модель заявила «Базы знаний КЦ и ЛК изучены» при том, что переданные ссылки
  (`kb/mango-product-docs/processed/…`) не существуют (реальные пути — `kb/processed/…`),
  а в отчёте аудитора нет ни одной ссылки на источник. Дефект дошёл до результата
  (на нём построен Блок А отчёта) и не был замечен ни одной стороной диалога.
- Метрики измерены по `usage` провайдера без оценок: `output_tokens` 43 425,
  `reasoning_tokens` 26 920, максимальный входной контекст 32 707, время генерации
  927 с, активное время 4 636 с
  ([`logs/metrics.md`](runs/2026/RUN-0021/logs/metrics.md)).
- Добавлен локальный инструмент воспроизводимости
  [`experiments/parse_765_chat_export.py`](experiments/parse_765_chat_export.py)
  (только stdlib, из CI не вызывается).
- Обновлены реестры: [`runs/README.md`](runs/README.md) и `EXPECTED_RUNS`
  в [`scripts/validate_issue_123_runs_contract.py`](scripts/validate_issue_123_runs_contract.py).

### Added — Issue #271 реальный прогон 1079 (RUN-0018) как Proof of Execution

- Добавлена запись [`runs/2026/RUN-0018/`](runs/2026/RUN-0018/outputs/README.md) —
  первый прогон, зафиксированный на **живых данных чата** (8 эпизодов сессии
  2026-07-21, модель `qwen3.7-plus`) вместо формальной пустой записи: дословная
  стенограмма ([`inputs/chat-export.md`](runs/2026/RUN-0018/inputs/chat-export.md)),
  вход ФТ v1.0, разбор по каждому эпизоду
  ([`outputs/steps/`](runs/2026/RUN-0018/outputs/steps/)) и итоговый документ v1.3.
- Прогон **не является** golden case: итоговый артефакт помечен как свидетельство с
  реестром известных дефектов
  ([`outputs/final-artifact.md`](runs/2026/RUN-0018/outputs/final-artifact.md)).
- Зафиксирован реестр галлюцинаций Г1–Г8
  ([`feedback/review-notes.md`](runs/2026/RUN-0018/feedback/review-notes.md)),
  сверенный с БЗ репозитория в формате `[CC, §N, с.NNN]`
  ([`inputs/kb-facts.md`](runs/2026/RUN-0018/inputs/kb-facts.md)). Ключевая находка:
  модель заявила, что термина «Конфиденциальность контактных данных» в документации
  КЦ «не существует», и подменила его голосовой политикой «Скрытие номера клиента» —
  ошибка дошла до финального документа. Корневая причина — прогон без подключённой
  БЗ и отсутствие гейта заземления в промпте
  [`fr-validation-stepwise`](prompts/fr-validation-stepwise.md); предложены правки
  П1–П5 (в этом PR не применяются).
- Измеренные метрики вместо оценочных:
  [`logs/metrics.md`](runs/2026/RUN-0018/logs/metrics.md) — 24 953 диалоговых токена
  + 7 327 «мышления» (`tiktoken:cl100k_base`), 763.6 с генерации, 41 мин активной
  работы. Скрипт разбора выгрузки —
  [`experiments/parse_qwen_chat_export.py`](experiments/parse_qwen_chat_export.py).
- Лог по [стандарту фиксации экспериментов](standards/experiment-log-standard.md):
  `verdict = works-with-edits`, `quality = 3`, `iterations = 8`, `ba_edits = 6`.

### Changed — Issue #271 расширение контракта runs полем `metrics`

- В [`standards/runs-contract-standard.md`](standards/runs-contract-standard.md)
  (v0.3 → v0.4) и [`runs/README.md`](runs/README.md) (v0.3 → v0.4) для уже
  разрешённого поля `metrics` зафиксированы правила ключей: `token_method`
  обязателен при указании токенов, `success_rate_basis` — при `success_rate`,
  `verdict` согласован с `logs/experiment-log.md`.
- [`scripts/validate_issue_123_runs_contract.py`](scripts/validate_issue_123_runs_contract.py):
  в `EXPECTED_RUNS` добавлен `RUN-0018`; регрессия разметки типов дополнена в
  [`scripts/test_runs_contract_run_type.py`](scripts/test_runs_contract_run_type.py).
- По итогам ревью PR #289: номер прогона изменён `RUN-0013 → RUN-0018` (номер
  `RUN-0013` занят в `main` задачей #268, `RUN-0014` — задачей #269, `RUN-0017` —
  задачей #270); перегенерированные файлы `site/data/*.json` откачены к состоянию
  `main` — веб-представление не входит в границы прогона
  (см. раздел «Границы прогона» в [`runs/README.md`](runs/README.md)) и собирается
  в CI (`.github/workflows/github-pages.yml`).
- Прогону присвоен `run_type: statistics`: цель задачи #271 — «собрать
  эмпирические данные для анализа кейсов и формирования Quality Baseline», а не
  получение артефакта.

### Changed — Issue #293 контракт прогонов: явное разделение типов (исполнение vs фиксация статистики)

- Гипотеза о пробеле контракта **подтверждена** и обоснована в
  [`docs/analysis/2026-08-21-runs-type-gap-analysis.md`](docs/analysis/2026-08-21-runs-type-gap-analysis.md):
  в `standards/runs-contract-standard.md` v0.1 нет ни типа прогона, ни разделения
  метрик успеха, ни правил границ; при этом `RUN-0013` смешивает шкалу артефакта
  (`status: works-with-edits`) со статистикой коммуникации (`success_rate` по
  репликам БА), а `RUN-0014` зафиксирован «для статистики», но оценён по шкале
  артефакта.
- [`standards/runs-contract-standard.md`](standards/runs-contract-standard.md)
  расширен до v0.3: разделы «Типы прогонов», «Критерий выбора типа прогона»,
  «Термин «Прогон»» и «Границы прогона», обязательное
  поле `run_type` со словарём `execution` | `statistics` | `legacy`, запрет
  смешивать метрики двух типов в одной выборке.
- Зафиксирован запрет на изменение рабочих артефактов прогонами: прогон создаёт
  файлы только внутри `runs/YYYY/RUN-XXXX/` и не изменяет `prompts/`, `kb/`,
  `site/data/`, `patterns/`; изменения этих каталогов инициирует Пользователь
  отдельными задачами.
- По итогам ревью PR #294 зафиксирован **критерий выбора типа**: тип берётся из
  формулировки цели в постановке задачи («зафиксировать прогон / собрать
  эмпирические данные» → `statistics`; «выполнить процесс / получить артефакт» →
  `execution`), а не из состава файлов в `outputs/`. Наличие ФТ или матрицы UC в
  статистическом прогоне — следствие успешной коммуникации, а не цель задачи.
- Разметка пересмотрена по этому критерию (обоснование по каждому прогону — Ф-5
  анализа): `statistics` — `RUN-0004`, `RUN-0005`, `RUN-0008`, `RUN-0009`,
  `RUN-0010` (issue #107 — сохранить и разобрать лог эксперимента), `RUN-0013`
  (issue #268), `RUN-0014` (issue #269), `RUN-0017` (issue #270 — все три
  «Зафиксировать прогон… собрать эмпирические данные»); `execution` — `RUN-0001`,
  `RUN-0002`, `RUN-0003`, `RUN-0006`, `RUN-0007`, `RUN-0011` (issue #109),
  `RUN-0012` (issue #261).
- Термин «Прогон» **сохранён**: это устоявшийся русскоязычный эквивалент *run*
  (прогон тестов/эксперимента); «запуск» означает инициацию, «проход» — итерацию
  внутри процесса. Обоснование — раздел «Термин «Прогон»» стандарта.
- Обратная совместимость: `metadata.yaml` без `run_type` валиден и читается как
  `execution`; записи Phase 0 без исходной постановки размечаются по
  зафиксированному назначению, при неразрешимой неоднозначности — `legacy`.
- [`runs/README.md`](runs/README.md) v0.2: таблица типов, раздел границ и колонка
  `run_type` в реестре прогонов.
- [`scripts/validate_issue_123_runs_contract.py`](scripts/validate_issue_123_runs_contract.py)
  проверяет словарь `run_type`, совпадение типа в `metadata.yaml` и в реестре, а
  также правило границ (пути `inputs`/`outputs`/`logs`/`feedback`/`source_paths`
  не выходят за каталог прогона). Регрессия дефолта, границ и согласованной
  разметки типов покрыта
  [`scripts/test_runs_contract_run_type.py`](scripts/test_runs_contract_run_type.py).
- В [`pr-ops/BACKLOG.md`](pr-ops/BACKLOG.md) заведён техдолг `S-006` —
  восстановление цепочки анализ → RFC → стандарт для контракта прогонов.

### Added — Issue #269 фиксация прогона RUN-0014 (задача 1075, создание сделки в amoCRM при звонке)

- Добавлена запись [`runs/2026/RUN-0014/`](runs/2026/RUN-0014/metadata.yaml) —
  реальный прогон промпта
  [`glossary-context-understanding-stepwise`](prompts/glossary-context-understanding-stepwise.md)
  по задаче 1075. Прогон **частичный**: целевой артефакт (Разделы 1 и 2 ТЗ) не
  получен, завершён 1 шаг из 4 (`success_rate` 0.25). Данные — промежуточные, не
  golden case; запись сделана для статистики и анализа результативности промптов
  и галлюцинаций.
- Метрики в [`metadata.yaml`](runs/2026/RUN-0014/metadata.yaml) **измерены**, а не
  оценены: 207 499 токенов (вход 195 948 / выход 11 551), 2 114 с ≈ 35,2 мин,
  модель `qwen3.7-plus`. Источник цифр — служебные поля `usage` выгрузки чата;
  воспроизведение — [`experiments/run-0014-chat-export/`](experiments/run-0014-chat-export/README.md).
- Зафиксированы пять дефектов Д-1…Д-5
  ([`feedback/ba-review.md`](runs/2026/RUN-0014/feedback/ba-review.md)), в том
  числе одно проверенное фактическое искажение (утверждение «"Неразобранное" —
  не сделка и не этап воронки» опровергается документацией amoCRM) и переход к
  следующему шагу без подтверждения человека. Отдельно описан конфликт правил 2
  и 5 самого промпта.
- В [`standards/runs-contract-standard.md`](standards/runs-contract-standard.md)
  разрешённые дополнительные поля `metadata.yaml` расширены полями `feedback` и
  `metrics` (токены, длительность, `success_rate`, `eval`) — требование issue #269
  фиксировать метрики прогона.
- Реестры обновлены: [`runs/README.md`](runs/README.md) и
  [`scripts/validate_issue_123_runs_contract.py`](scripts/validate_issue_123_runs_contract.py).

### Added — Issue #268 прогон RUN-0013 (BCREQ-1059, лимиты и приоритеты распределения обращений)

- Зафиксирован реальный прогон БА с LLM по задаче 1059 на основе экспорта
  истории чата, приложенного к
  [issue #268](https://github.com/G-Ivan-A/mango_ba_prompts/issues/268):
  [`runs/2026/RUN-0013/`](runs/2026/RUN-0013/metadata.yaml). Оформлен как один
  комплексный прогон с разделением на 8 эпизодов и отдельным вердиктом по
  каждому (вариант, разрешённый постановкой): эпизоды — стадии одного
  непрерывного диалога с общим глоссарием и сквозной нумерацией ФТ, а не
  независимые кейсы.
- Метрики прогона: 242 сообщения активной ветки (121 итерация БА ↔ модель),
  2026-06-18 — 2026-07-31 (10 рабочих дней), модели `qwen3.7-plus` и
  `qwen3.8-max-preview`, 79 405 522 входных / 543 180 выходных токенов,
  вердикт `works-with-edits`, success_rate ≈ 0.62 (75 из 121 ответов приняты
  БА без явной правки). Подсчёт воспроизводится скриптом
  [`experiments/analyze_chat_metrics.py`](experiments/analyze_chat_metrics.py).
- [`feedback/review-notes.md`](runs/2026/RUN-0013/feedback/review-notes.md)
  заполнен не заглушкой, а разбором с привязкой к номерам реплик: 6 паттернов
  успеха (генерация матриц, сверка терминологии с руководствами ЛК/КЦ,
  критический анализ) и 12 зафиксированных дефектов (придуманные названия
  настроек интерфейса, использование данных устаревшей встречи, перегенерация
  согласованных формулировок, смешение уровней 4.x / 4.x.x).
- Вход сохранён ссылкой на вложение issue с разбором структуры экспорта
  ([`inputs/chat-export.md`](runs/2026/RUN-0013/inputs/chat-export.md)) —
  файл 4,6 МБ в репозиторий не копируется; расширенное ТЗ Заказчика приведено
  дословно в [`inputs/raw-requirement.md`](runs/2026/RUN-0013/inputs/raw-requirement.md).
- Обновлены реестр [`runs/README.md`](runs/README.md) и проверка контракта
  [`scripts/validate_issue_123_runs_contract.py`](scripts/validate_issue_123_runs_contract.py)
  (RUN-0013 добавлен в ожидаемый состав `runs/2026/`).
### Changed — Issue #267 актуализация onboarding-протокола до v1.5 и проверка корневых файлов

- Навигация переведена на актуальный протокол
  [`ai-rules/agent-onboarding-protocol.md`](ai-rules/agent-onboarding-protocol.md)
  (v1.5, рабочая копия Хаба на
  [`3bfa410`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/tree/3bfa4103c9efbbd59bc951814884920e406982e2)):
  обновлены [`README.md`](README.md), [`AI_SESSION_HANDOVER_PROMPT.md`](AI_SESSION_HANDOVER_PROMPT.md)
  (+ `.executable.md`), [`standards/cascading-context-loading-standard.md`](standards/cascading-context-loading-standard.md)
  и [`pr-ops/artifact-map.md`](pr-ops/artifact-map.md). Раньше все точки входа
  вели на архивную v1.2.
- Архив v1.2 сохранён (traceability, файл не удаляется), но переведён в
  `status: superseded`, лишён `entrypoint` и снабжён баннером «АРХИВ»:
  [`ai-rules/agent-onboarding-protocol_old.md`](ai-rules/agent-onboarding-protocol_old.md)
  (+ `.executable.md`). В README он остаётся отдельной строкой как архив.
- В протокол v1.5 добавлена единственная локальная дельта — `owner: G-Ivan-A`:
  `frontmatter-docs-standard.md` Хаба требует `owner` для governance-артефактов,
  а в хабовом оригинале поля нет. Возврат дельты в Хаб — задача S-005 бэклога.

### Added — Issue #267 локальные валидаторы Хаба

- Добавлен каталог [`tools/`](tools/README.md) с рабочими копиями валидаторов
  Хаба на [`6c57eae`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/tree/6c57eae8a2713566878be715856884b660dd2a16):
  [`validate-frontmatter.sh`](tools/validate-frontmatter.sh) и
  [`validate-file-naming.sh`](tools/validate-file-naming.sh) (spoke-вариант из
  `templates/spoke/`). Запуск — `make validate`; в CI —
  [`.github/workflows/validate.yml`](.github/workflows/validate.yml) на каждый
  PR и push в `main`.
- Локальные дельты валидаторов ограничены и задокументированы в
  [`tools/README.md`](tools/README.md): расширен список допустимых полей класса
  `default` (провенанс-поля спицы, которые потребляет
  [`scripts/sync_from_hub.py`](scripts/sync_from_hub.py) и
  `standards/cascading-context-loading-standard.md`) и заморожен
  [`tools/file-naming-legacy-allowlist.txt`](tools/file-naming-legacy-allowlist.txt)
  на 26 легаси-файлов. Ни одна проверка канонического валидатора не ослаблена:
  любой новый файл проверяется в полную силу (проверено контрольным прогоном на
  файле-нарушителе).

### Fixed — Issue #267 frontmatter корневых файлов

- Из корневых файлов удалено поле `ai-generated`, прямо запрещённое
  `frontmatter-docs-standard.md` Хаба, и добавлено обязательное `temperature`:
  [`README.md`](README.md), [`AI_GOVERNANCE.md`](AI_GOVERNANCE.md),
  [`AI_QUICK_RULES.md`](AI_QUICK_RULES.md), [`CONTRIBUTING.md`](CONTRIBUTING.md),
  [`CHANGELOG.md`](CHANGELOG.md), [`AI_SESSION_HANDOVER_PROMPT.md`](AI_SESSION_HANDOVER_PROMPT.md)
  (+ `.executable.md`). Область `make validate` (корень, `ai-rules/`, `tools/`)
  проходит без ошибок.
- Некритические находки не исправлялись «по пути», а зафиксированы задачами
  S-001…S-005 в [`pr-ops/BACKLOG.md`](pr-ops/BACKLOG.md): легаси-именование 26
  хронологических файлов, frontmatter-долг вне области (23 062 ошибки в 1 287
  файлах, преимущественно генерируемые `kb/` и `runs/`), поле `ai-generated` в
  1 243 файлах, расхождение стандарта и валидатора Хаба по классу `ai-rules/`.
### Added — Issue #270 фиксация прогона RUN-0017 (задача 1076)

- Добавлен прогон [`runs/2026/RUN-0017/`](runs/2026/RUN-0017/metadata.yaml) —
  Proof of Execution реальной сессии BA по задаче 1076 (передача Артефактов ВКС
  во Внешнюю систему BPMSoft / конфигурация «Эстейт»), 56 реплик, 11 эпизодов,
  2 536 400 токенов, ~3 ч.
- Состав: [`inputs/`](runs/2026/RUN-0017/inputs/README.md) (исходный экспорт чата
  и воспроизводимый транскрипт), [`outputs/`](runs/2026/RUN-0017/outputs/README.md)
  (разбор по 11 шагам, цепочка промптов, BA-анализ качества, промежуточный
  артефакт), [`logs/`](runs/2026/RUN-0017/logs/experiment-log.md) (лог
  эксперимента и метрики по репликам),
  [`feedback/`](runs/2026/RUN-0017/feedback/ba-review-notes.md) (реальная
  обратная связь BA из диалога).
- Добавлен переиспользуемый конвертер экспорта чата
  [`scripts/chat_export_to_markdown.py`](scripts/chat_export_to_markdown.py)
  (только stdlib) — транскрипт и метрики по репликам воспроизводятся из
  исходного JSON.
- Прогон зарегистрирован в реестре [`runs/README.md`](runs/README.md) и в
  `EXPECTED_RUNS` валидатора
  [`scripts/validate_issue_123_runs_contract.py`](scripts/validate_issue_123_runs_contract.py).
- Оговорка: результат прогона — **промежуточный**, это не эталонный шаблон и не
  golden case; фиксация выполнена для сбора статистики и BA-анализа процессов,
  эффективности промптов, успешных результатов и галлюцинаций.
- По итогам ревью PR #288: номер прогона изменён `RUN-0013 → RUN-0017` (номер
  `RUN-0013` занят в `main` задачей #268, `RUN-0014` — задачей #269, на
  `RUN-0013` также претендуют открытые PR #289 и #290); перегенерированные
  файлы `site/data/*.json` откачены к состоянию `main` — веб-представление не
  входит в границы задачи на прогон и собирается в CI
  (`.github/workflows/github-pages.yml`).
- Добавлен аудит
  [`docs/audit/audit-run-scope-boundary-2026-08-21.md`](docs/audit/audit-run-scope-boundary-2026-08-21.md)
  — пошаговый разбор, почему исполнитель счёл регенерацию `site/data/` частью
  задачи на прогон, и предложения Р-1…Р-6 по ужесточению контрактов Run и
  правил онбординга (правки самих стандартов вынесены в отдельную задачу).
- По итогам ревью PR #288 (решение по файлам вне `runs/`): в
  [`runs/README.md`](runs/README.md) добавлен раздел «Локальные инструменты
  воспроизводимости», а в
  [`runs/2026/RUN-0017/inputs/README.md`](runs/2026/RUN-0017/inputs/README.md) —
  явная оговорка о статусе скриптов
  [`scripts/chat_export_to_markdown.py`](scripts/chat_export_to_markdown.py) и
  [`experiments/chat_export_probe.py`](experiments/chat_export_probe.py): это
  локальные инструменты, запускаемые вручную
  (`python3 scripts/chat_export_to_markdown.py <export.json> ...`), не входящие в
  CI и не зависящие от GitHub Actions.

### Changed — Issue #265 ре-синк базовых стандартов Хаба (T-01)

- Дрейф в 610 коммитов устранён: рабочие копии методологии Хаба перенесены с
  `b683341` (2026-06-13) на
  [`3bfa410`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/tree/3bfa4103c9efbbd59bc951814884920e406982e2)
  (2026-08-17). Перенесены [`ai-rules/`](ai-rules/README.md) (4 файла),
  [`ai-governance/`](ai-governance/README.md) (3 файла),
  [`standards/GLOSSARY.md`](standards/GLOSSARY.md) (v2.1 — появился словарь
  ADR-010: Operating Mode, Экспертное исполнение, Абсолютные границы, Легальный
  выход, Task Type, Method),
  [`standards/evals-contract-standard.md`](standards/evals-contract-standard.md),
  [`standards/analysis-standard.md`](standards/analysis-standard.md),
  [`standards/research-standard.md`](standards/research-standard.md).
- Битые относительные ссылки устранены полностью (было 62 в 19 файлах, включая 23
  в глоссарии). Корневые причины: hub-относительные ссылки в скопированном из
  Хаба глоссарии (`../CONCEPT.md`, `../governance/REPO_MODEL.md`,
  `../governance/proposals/rfc-*.md` — Хаб с тех пор переструктурировался),
  захардкоженная глубина `../../../` в генераторе
  [`scripts/kb/extract.py`](scripts/kb/extract.py) (ломала `index.md` вложенных
  документов БЗ) и устаревшие пути после миграций `prompts/` → `prompts/archive/`
  и `prompts/experiments/` → `runs/`.
- Добавлен воспроизводимый синк
  [`scripts/sync_from_hub.py`](scripts/sync_from_hub.py): перенос по
  декларативному манифесту с переписыванием каждой ссылки (локальный путь, если
  цель тоже перенесена, иначе permalink Хаба на закреплённом SHA); режим
  `--check` сверяет копии с Хабом. Ручное копирование воспроизводило дефект
  «некритично скопированный контекст» при каждом синке.
- Добавлена проверка
  [`scripts/validate_issue_265_hub_sync.py`](scripts/validate_issue_265_hub_sync.py)
  (в CI): ноль битых относительных ссылок, единый `source_sha` у всех рабочих
  копий, отсутствие путей за корень репозитория. Инлайн-код и fenced-блоки не
  проверяются — там ссылка является синтаксическим примером.
- Решение зафиксировано в
  [ADR-0004](docs/adr/0004-hub-resync-2026-08.md): что перенесено, что
  сознательно **не** перенесено (реестр стандартов Хаба, контракты frontmatter и
  именования, `*-structure-standard.md`, клиент Smart Sync `tools/`) и почему;
  политика «рабочие копии локально не редактируются» и запрет прямых
  hub-относительных ссылок в споке.
- Добавлен реестр [`standards/README.md`](standards/README.md), разграничивающий
  рабочие копии Хаба и стандарты спицы с правилом «сужать можно, противоречить
  нельзя». Приоритет норм продублирован в
  [`AI_GOVERNANCE.md`](AI_GOVERNANCE.md) и
  [`ai-rules/agent-onboarding-protocol_old.md`](ai-rules/agent-onboarding-protocol_old.md)
  (там же — разделение ролей двух копий onboarding-протокола).
- Обновлены [`pr-ops/artifact-map.md`](pr-ops/artifact-map.md) (новые
  строки `ai-rules/`, `ai-governance/`, `standards/README.md`,
  `scripts/sync_from_hub.py`; раздел решений по ре-синку) и
  [`docs/hub-research-dependencies.md`](docs/hub-research-dependencies.md)
  (`latest_smart_sync_sha`; точка синка методологии и точка research движутся
  независимо).
- Структура репозитория приведена к базовой структуре Хаба: каталог
  `governance/` расформирован, его содержимое разнесено по
  [`pr-ops/`](pr-ops/artifact-map.md) (операционные записи),
  [`ai-rules/`](ai-rules/agent-onboarding-protocol_old.md) (старый протокол
  онбординга v1.2 под суффиксом `_old`), `docs/rfc/`, `docs/audit/` и
  [`standards/prompt-debugging-process.md`](standards/prompt-debugging-process.md).
  Каталог `research/` не создавался: он специфичен для Хаба, research остаётся
  reference-only. Перенос воспроизводим
  ([`experiments/restructure_governance_dirs.py`](experiments/restructure_governance_dirs.py)):
  22 пути, 63 файла с переписанными путями, 123 пересчитанные относительные
  ссылки; permalink'и Хаба на `governance/` старых SHA не переписаны, чтобы не
  потерять traceability.
- Состав манифеста
  [`scripts/sync_from_hub.py`](scripts/sync_from_hub.py) сверен с итоговым
  (замерженным) видением T-00 (issue #263 / PR #264): расхождений не найдено,
  манифест не изменялся. Таблица сверки — в
  [ADR-0004](docs/adr/0004-hub-resync-2026-08.md).
- В [`.hub-profile.json`](.hub-profile.json) появился `sync_history`: точка синка
  issue #72 сохранена как исторический факт, `last_sync` принадлежит текущему
  синку. Проверка
  [`scripts/validate_issue_72_hub_sync.py`](scripts/validate_issue_72_hub_sync.py)
  читает историческую запись — раньше она пинила «последний» SHA и тем самым
  запрещала любой следующий синк.
### Changed — Issue #263 корректировка видения и концепции проекта

- В [`AI_GOVERNANCE.md`](AI_GOVERNANCE.md) зафиксирован принцип
  «качество системы исполнения > стоимость»: каждая операция БА обязана иметь
  механизм проверки (чек-лист, evals-метрика или human-in-the-loop gate), а
  **операция без процесса проверки считается незавершённой**; норма добавлена в
  Definition of Done и в границы «Никогда не делать».
- Описаны роль проекта и инфраструктурная модель: автоматизация процессов
  бизнес-анализа в проекте Манго (телеком), GitHub как единственная платформа,
  AI-исполнитель как основной инструмент — без серверной инфраструктуры
  и мультиагентной системы; они относятся к `ai-ba-playbooks`.
- Зафиксирован фактический **статус механизмов проверки**: чек-листы и
  human-in-the-loop gate есть, **`evals/` и golden-set отсутствуют**. Пока
  пробел не закрыт, ссылка на evals-метрику не закрывает ДОД; пробел внесён в
  [`pr-ops/BACKLOG.md`](pr-ops/BACKLOG.md).
- Добавлен раздел «Веб-ресурс (app) после приватизации»: GitHub Pages не
  работает для приватных репозиториев на бесплатном плане, поэтому зафиксированы
  варианты A (внешний портал `open-ai.ru`), B (поэтапная миграция с внешним
  билдом) и C (вывод через `ai-ba-playbooks`); выбор — решение Пользователя,
  блокер Q1.
- Добавлен раздел «Подготовка к приватизации» с режимами обращения с
  чувствительными данными (`kb/`, `runs/`, боевые промпты, `governance/`) до
  смены видимости репозитория на Private.
- [`README.md`](README.md) переформулирован под роль автоматизации процессов БА
  в проекте Манго; добавлены разделы «Роль проекта и границы» и «Принцип «качество системы
  исполнения > стоимость»».
- [`docs/ba-ecosystem.md`](docs/ba-ecosystem.md): новый §1.1 «ДОД операции:
  процесс проверки обязателен»; §7 переформулирован как границы автоматизации
  спока (уровни L1–L4 остаются референсной моделью, а не планом работ).
- [`docs/rfc-hub-integration.md`](docs/rfc-hub-integration.md): новый §1.1 «Два
  адресата исходящего потока» — Хаб (методология) и `ai-ba-playbooks`
  (универсальные и специализированные плейбуки, отбор Пользователем по C1–C5,
  развитие в сторону конструктора); поток строго односторонний и
  неавтоматический.
- Из концептуальных документов убраны внутренние термины («фаундер», имя
  AI-исполнителя): субъект решений — **Пользователь**, исполнитель —
  **AI-исполнитель**; регрессионная проверка запрещает возврат этих терминов
  и концептов проекта БИЛД (Proof of Execution, Learning loop, S1–S5).
- [`docs/hub-research-dependencies.md`](docs/hub-research-dependencies.md)
  дополнен якорями `#adr-009-repo-split`, `#ba-process-ontology`,
  `#separation-readiness`: решения Хаба остаются в Хабе и ссылаются через
  единый мост, а не копируются.
- [`pr-ops/artifact-map.md`](pr-ops/artifact-map.md) обновлён под новые
  назначения документов и решения ADR-009 v0.3.
- Добавлена регрессионная проверка
  [`scripts/validate_issue_263_vision_alignment.py`](scripts/validate_issue_263_vision_alignment.py)
  и подключена в `.github/workflows/github-pages.yml`.

### Added — Issue #261 ФТ по BCREQ-1069 (ограниченный API-ключ)

- Добавлен прогон [`runs/2026/RUN-0012`](runs/2026/RUN-0012/metadata.yaml)
  (`bcreq-1069-restricted-api-key`): цепочка промптов формирует финальное ФТ
  (Разделы 1, 2, 4, 6) по сырому требованию из
  [issue #261](https://github.com/G-Ivan-A/mango_ba_prompts/issues/261) —
  дополнительный ограниченный API-ключ для передачи записей разговоров стороннему
  сервису с фильтрацией по сотрудникам/группам.
- Итоговое ФТ, пошаговые артефакты (глоссарий → контекст → вопросы → сценарии →
  ФТ → ограничения), лог эксперимента и вход зафиксированы в контракте `runs/`.
- Реестр `runs/README.md` и регрессионная проверка
  [`scripts/validate_issue_123_runs_contract.py`](scripts/validate_issue_123_runs_contract.py)
  расширены записью RUN-0012.

### Added — Issue #125 cascading context loading

- Добавлен стандарт
  [`standards/cascading-context-loading-standard.md`](standards/cascading-context-loading-standard.md):
  naming `.executable.md`, LLM Loading Contract, deterministic escalation
  triggers и правила замера экономии токенов.
- Для критичных full-файлов созданы executable-companions:
  [`AI_SESSION_HANDOVER_PROMPT.executable.md`](AI_SESSION_HANDOVER_PROMPT.executable.md),
  [`ai-rules/agent-onboarding-protocol_old.executable.md`](ai-rules/agent-onboarding-protocol_old.executable.md),
  [`prompts/README.executable.md`](prompts/README.executable.md),
  [`docs/ba-processes/00-index.executable.md`](docs/ba-processes/00-index.executable.md)
  и [`standards/ba-ontology.executable.md`](standards/ba-ontology.executable.md).
- В full-файлы добавлен `LLM Loading Contract`, а prompt
  [`prompts/session-debug-documentation-oneshot.md`](prompts/session-debug-documentation-oneshot.md)
  теперь ссылается на executable-слой `prompts/README`.
- Добавлена регрессионная проверка
  [`scripts/validate_issue_125_cascading_context.py`](scripts/validate_issue_125_cascading_context.py),
  подключённая к GitHub Pages workflow.

### Added — Issue #123 единый каталог `runs/`

- Добавлен единый каталог результатов выполнения процессов `runs/YYYY/RUN-XXXX/`
  с обязательными `metadata.yaml`, `inputs/`, `outputs/`, `feedback/` и `logs/`.
- Существующие результаты из `prompts/experiments/`,
  `docs/ba-process/multichannel-agent-workload/` и
  `governance/analysis-bcreq-1025-2026-06-17.md` перенесены в `runs/2026/`
  с сохранением истории через `git mv`.
- Добавлены [`runs/README.md`](runs/README.md),
  [`standards/runs-contract-standard.md`](standards/runs-contract-standard.md)
  и регрессионная проверка
  [`scripts/validate_issue_123_runs_contract.py`](scripts/validate_issue_123_runs_contract.py),
  подключённая к GitHub Pages workflow.
- GitHub Pages checks теперь собирают evidence из `runs/`, а не из бывшего
  каталога `prompts/experiments/`.

### Added — Issue #121 KB pipeline: multi-file сценарии и обновление документов

- Добавлен manifest-driven runner
  [`scripts/kb/process_sources.py`](scripts/kb/process_sources.py): читает
  `kb/sources/<slug>/meta.json`, различает `single`, `multi_part` и
  `multi_document`, строит extraction jobs и защищает локальный запуск от LFS
  pointer-файлов вместо PDF bytes.
- В `meta.json` источников КЦ, ЛК и Mango Talker добавлены явные
  `processing_mode`, `output_slug`, `doc_code` и/или `source_files`; для Mango
  Talker выбран гибридный режим: общий product collection `kb/processed/mtalker/`
  и отдельные вложенные БЗ для каждого независимого руководства.
- Добавлены Make targets `kb-source-plan`, `kb-source-extract`, `kb-mtalker` и
  workflow input `source_dir`, чтобы ручной KB pipeline мог запускаться по
  source manifest, а не только по raw списку PDF-путей.
- Добавлена stdlib-проверка
  [`scripts/validate_issue_121_kb_multi_file.py`](scripts/validate_issue_121_kb_multi_file.py):
  фиксирует реальные манифесты, synthetic сценарии `single`, `multi_part`,
  `multi_document`, обновления 1→N, N→1, добавление и удаление документов.
- Обновлена инструкция [`kb/sources/README.md`](kb/sources/README.md): примеры
  `meta.json`, сценарии 1–6, правила обновления и troubleshooting для Git LFS.

### Fixed — Issue #119 KB pipeline: multi-part PDF и Git LFS

- Workflow KB pipeline обновлён для LFS-aware checkout (`lfs: true`) и текущих
  major-версий `actions/checkout`, `actions/setup-python` и `actions/upload-artifact`.
- `make kb-mango`, workflow defaults и регрессионная проверка
  `validate_issue_115_kb_mango_pipeline.py` переведены с удалённого
  `CC_manual_1.26.23_compressed.pdf` на 6 PDF-частей руководства КЦ.
- БЗ `kb/processed/mango-cc-manual/` регенерирована как multi-part документ со
  сквозной пагинацией и `source_refs` на конкретные LFS-части.
- Документация пополнения БЗ описывает обновление PDF через Git LFS, Codespace
  или локальный Git и обновление `meta.json` при замене одного файла частями.

### Fixed — Issue #117 KB pipeline: трассировка разделов и multi-part PDF

- `scripts/kb/extract.py` теперь принимает один или несколько PDF одного
  документа, обрабатывает split-руководства со сквозной пагинацией и сохраняет
  точную привязку каждого раздела к PDF-части и локальным страницам.
- В `meta.json` и frontmatter разделов добавлены `sources`, `source_pdfs`,
  `part_count`, `pdf_section`, `pdf_heading`, `source_part`, `source_pages` и
  `source_refs`; в каждом разделе выводится человекочитаемая строка
  `Трассировка`.
- Добавлена сформированная БЗ
  [`kb/processed/mango-lk-manual/`](kb/processed/mango-lk-manual/) для 5 частей
  руководства ЛК ВАТС v1.21: 568 сквозных страниц, 348 разделов, 1545
  изображений.
- Добавлен `make kb-lk` и регрессионная проверка
  [`scripts/validate_issue_117_kb_traceability.py`](scripts/validate_issue_117_kb_traceability.py),
  подключённая к workflow KB pipeline.

### Fixed — Issue #115 KB pipeline: реальное руководство не попадало в `kb/processed/`

- Диагностирован KB Pipeline #11: успешный `workflow_dispatch` запуск извлекал
  только синтетическую фикстуру `contact-center-manual-sample`, выгружал результат
  артефактом и не обрабатывал загруженный
  `kb/sources/mango-cc-manual/CC_manual_1.26.23_compressed.pdf`.
- Добавлена сформированная БЗ
  [`kb/processed/mango-cc-manual/`](kb/processed/mango-cc-manual/) для реального
  руководства v1.26.23: `index.md`, `meta.json`, `sections/`, `images/`.
- `Makefile` и workflow KB pipeline параметризованы (`SRC`, `OUT`, `doc_code`,
  `doc_title`, `doc_version`); ручной GitHub Actions запуск теперь по умолчанию
  обрабатывает `mango-cc-manual`, а не фикстуру.
- `extract.py` использует встроенное PDF outline/bookmarks, если оно есть, чтобы
  не превращать жирные нумерованные пункты списков в отдельные разделы.
- Добавлена регрессионная проверка
  [`scripts/validate_issue_115_kb_mango_pipeline.py`](scripts/validate_issue_115_kb_mango_pipeline.py):
  фиксирует наличие реальной БЗ, корректный источник, outline-нарезку и
  параметризованный workflow.

### Added — Issue #111 машиночитаемая БЗ из PDF: эксперимент + инфраструктура + методология (Creative)

- Построен сквозной конвейер **«источник → machine-readable БЗ»**
  [`scripts/kb/extract.py`](scripts/kb/extract.py) (pdfplumber + PyMuPDF +
  tiktoken): извлекает текст со структурой, картинки и таблицы, режет документ на
  разделы-чанки (`index.md` + `sections/NN-*.md` + `images/` + `meta.json`),
  считает токены. Нарезка — детерминированная (regex+кегли), **без LLM** по
  умолчанию (LLM — задокументированный fallback для неструктурированных текстов,
  **ФТ-3**). Вспомогательные скрипты: [`tokens.py`](scripts/kb/tokens.py),
  [`make_sample_pdf.py`](scripts/kb/make_sample_pdf.py) (фикстура, т.к. реальный
  `CC_manual_1.26.23.pdf` не загрузился в issue).
- Создана **нейтральная** структура БЗ [`kb/`](kb/README.md) (**не** `mango-kc`,
  **ФТ-4**) с **обязательным каталогом ручного ввода** [`kb/sources/`](kb/sources/README.md):
  `sources/` (вход человека) → `processed/` (генерируется) → `fragments/`
  (задел под RAG). Человекочитаемая инструкция пополнения (**ФТ-7**) —
  [`kb/sources/README.md`](kb/sources/README.md); источники-ссылки —
  [`kb/sources/web-links/`](kb/sources/web-links/README.md).
- Добавлены **5 конкретных примеров** обращения промпта к БЗ на реальных данных
  (индекс → выбор раздела → загрузка чанка → цитата `[CC, §4.2, с.5]` → сравнение
  токенов 1587 vs 378) — [`kb/USAGE.md`](kb/USAGE.md) (**ФТ-6**).
- Зафиксирован **отчёт по эксперименту** (**ФТ-8**)
  [`docs/kb-experiment-report.md`](docs/kb-experiment-report.md): описание PDF и
  оговорка о незагрузившемся файле, результаты и оценка качества извлечения
  (ловушка кириллицы), иерархия разделов, сравнение инструментов
  marker/nougat/MinerU **vs** pdfplumber с обоснованием выбора (**ФТ-2**,
  качество > токенов), скрипты-vs-LLM, предложение структуры, оценка
  автоматизации, устойчивость к драйфу ADR/промптов и явное указание, что БЗ —
  **эволюционный шаг к векторной БЗ и RAG**.
- Автоматизация (**ФТ-5**): [`Makefile`](Makefile) (`make kb-all` / `kb-sample` /
  `kb-extract` / `kb-validate` / `kb-tokens`) и GitHub-native workflow
  [`.github/workflows/kb.yml`](.github/workflows/kb.yml): лёгкая проверка на
  каждый PR/push (stdlib-only) + ручной (`workflow_dispatch`) прогон полного
  извлечения с выгрузкой артефакта.
- Добавлена локальная/CI-проверка
  [`scripts/validate_issue_111_kb_pipeline.py`](scripts/validate_issue_111_kb_pipeline.py)
  (stdlib-only): наличие деливераблов и нейтрального имени, согласованность
  `meta.json` ↔ разделы ↔ индекс ↔ токены ↔ картинки, наличие 5 примеров и
  обязательных пунктов отчёта.

### Added — Issue #109 dogfooding-эксперимент «Многоканальная нагрузка агента» (Creative + Structured)

- Добавлен полный прогон цепочки промптов на сыром требовании заказчика
  (одновременная работа агента с обращениями голос/чат/e-mail, лимит 3, приоритет) —
  каталог [`runs/2026/RUN-0011/`](runs/2026/RUN-0011/outputs/README.md)
  (**ФТ-1…ФТ-4**): вход ([`inputs/`](runs/2026/RUN-0011/inputs/)),
  обоснованная цепочка ([`prompts-chain.md`](runs/2026/RUN-0011/outputs/prompts-chain.md)),
  промежуточные результаты по шагам ([`steps/`](runs/2026/RUN-0011/outputs/steps/):
  глоссарий+As-Is, нормализация+5 Whys+gap, вопросы заказчику, US/UC, варианты
  доработки/Раздел 3) и [`final-artifact.md`](runs/2026/RUN-0011/outputs/final-artifact.md).
- Зафиксирована выжимка БЗ из 2 PDF-руководств (КЦ + ЛК ВАТС) с цитатами
  `[Документ, §Раздел, с.Страница]` и явными пометками «не найдено в документации»
  ([`inputs/kb-files.md`](runs/2026/RUN-0011/inputs/kb-files.md), по ADR-007).
- Добавлен лог эксперимента по [`standards/experiment-log-standard.md`](standards/experiment-log-standard.md)
  ([`experiment-log.md`](runs/2026/RUN-0011/logs/experiment-log.md), 6 метрик, verdict `works-with-edits`).
- Добавлен индекс каталога прогонов BA-процесса
  [`docs/ba-process/README.md`](docs/ba-process/README.md) (**ФТ-6**).
- Подготовлен RFC по улучшению промптов (**ФТ-5**, промпты **не изменены**):
  [`docs/rfc/prompt-improvement-multichannel-proposal.md`](docs/rfc/prompt-improvement-multichannel-proposal.md)
  (RFC-MCH-P1…P3); реестр [`docs/rfc/rfc-register.md`](docs/rfc/rfc-register.md)
  дополнен записями RFC-MCH-*. RFC-MCH-P1 — повтор паттернов Б1/Б5 из BCREQ-1025.

### Added — Issue #105 синхронизация контрактов с Хабом (Research + Structured)

- Добавлен аудит контрактов спока
  [`docs/audit/audit-contracts-mango-2026-06-17.md`](docs/audit/audit-contracts-mango-2026-06-17.md)
  (**ФТ-1**): ревизия ADR #003–#010, 12 стандартов и governance-/root-контрактов с
  классификацией (локальный / Smart Sync ← / сверить → RFC / передача знаний →).
- Добавлен аудит ключевых документов Хаба
  [`docs/audit/audit-hub-2026-06-17.md`](docs/audit/audit-hub-2026-06-17.md)
  (**ФТ-2**): RFC, стандарты и governance Хаба с **полными permalink-URL** на снимок
  `6ddffdf`, применимостью к Mango и пробелами.
- Добавлена матрица синхронизации
  [`pr-ops/sync-matrix-2026-06-17.md`](pr-ops/sync-matrix-2026-06-17.md)
  (**ФТ-3**): соответствие контрактов спок ↔ Хаб, реестр RFC-сверки и передачи знаний.
- Интегрирован RFC-процесс Хаба (**ФТ-4**):
  [`docs/rfc/rfc-process.md`](docs/rfc/rfc-process.md) **ссылается** на
  `knowledge-lifecycle-proposal.md` Хаба (не дублирует), отображает жизненный цикл
  знаний на артефакты спока; реестр [`docs/rfc/rfc-register.md`](docs/rfc/rfc-register.md)
  дополнен RFC-SYNC-* и RFC-HUB-*. Подготовлен RFC в Хаб о процессе отладки промптов
  [`docs/rfc/rfc-to-hub-002-prompt-debugging-process.md`](docs/rfc/rfc-to-hub-002-prompt-debugging-process.md).
- Подготовлена передача знаний в Хаб (**ФТ-5**):
  каталог [`docs/rfc/knowledge-transfer-to-hub/`](docs/rfc/knowledge-transfer-to-hub/)
  (онтология БА #003, таксономия операций #004, процесс BCREQ #009, UX Pages #010) и
  umbrella-RFC [`docs/rfc/rfc-to-hub-001-knowledge-transfer.md`](docs/rfc/rfc-to-hub-001-knowledge-transfer.md).
- Контракты спока в этом PR **не изменены**: расхождения с Хабом оформлены как RFC
  `proposed`, уникальные практики — как документы передачи знаний (правило «не менять
  сразу, а создать RFC»).

### Added — Issue #101 разбор эксперимента «Задача 1027» и стандарт фиксации экспериментов

- Добавлен анализ первой реальной сессии БА
  [`docs/analysis/experiment-1027-analysis.md`](docs/analysis/experiment-1027-analysis.md):
  вердикты по 4 гипотезам БА с цитатами из стенограммы, **предложения** правок
  промптов (P1–P5) как кандидаты в RFC и рекомендации по онтологии (без её
  изменения). Сами промпты в этом PR **не меняются** — правки выносятся через
  процесс отладки (см. ниже).
- Добавлен легковесный стандарт фиксации экспериментов (Draft v0.1)
  [`standards/experiment-log-standard.md`](standards/experiment-log-standard.md):
  два уровня фиксации (GitHub Issue / лёгкий Markdown) и ядро из 6 метрик.
- Добавлен первый прогон по стандарту (dogfood на сессии 1027)
  [`runs/2026/RUN-0007/outputs/fr-generation-1027-live_2026-06-16.md`](runs/2026/RUN-0007/outputs/fr-generation-1027-live_2026-06-16.md).
- Добавлен аудит контрактов
  [`docs/audit/audit-contracts-2026-06-17.md`](docs/audit/audit-contracts-2026-06-17.md):
  ревизия `AI_GOVERNANCE.md`, `CONTRIBUTING.md` и стандарта логирования,
  выявленные пробелы (нет процесса отладки/RFC/критериев приёмки правок промптов).
- Добавлен аудит исследования
  [`docs/audit/audit-research-1027.md`](docs/audit/audit-research-1027.md):
  проверка полноты разбора гипотез H1–H4, обоснованности рекомендаций O1–O3 и
  передачи онтологии (ADR #3–#8).
- Добавлен черновик процесса отладки промптов
  [`standards/prompt-debugging-process.md`](standards/prompt-debugging-process.md)
  и реестр RFC [`docs/rfc/rfc-register.md`](docs/rfc/rfc-register.md):
  порядок «эксперимент → RFC → согласование с пользователем → изменение».

### Added — Issue #97 формализация онтологии БА и стандартов (Creative + Research)

- Формализована онтология БА (артефакт ↔ процесс ↔ операция) и выпущен набор
  стандартов в виде ADR: [ADR-003](docs/adr/003-ba-ontology.md) (онтология),
  [ADR-004](docs/adr/004-operations-taxonomy.md) (таксономия 13 операций,
  `risk_analysis` сохранён), [ADR-005](docs/adr/005-artifact-team-naming.md)
  (нейминг артефактов/команд), [ADR-006](docs/adr/006-prompt-naming.md) (нейминг
  промптов, запрет перегрузки), [ADR-007](docs/adr/007-kb-standard.md) (KB до
  настоящего RAG), [ADR-008](docs/adr/008-industry-standards-standard.md)
  (отраслевые стандарты и best practices),
  [ADR-009](docs/adr/009-bcreq-formation-process.md) (многоуровневый процесс
  BCREQ, механизм незавершённых подпроцессов),
  [ADR-010](docs/adr/010-pages-ux.md) (UX GitHub Pages). Все ADR содержат
  обязательные разделы ФТ-9 (Title, Status, Context, Decision, Consequences,
  References, Examples).
- Добавлены «живые» контракты-стандарты с нормативным словарём RFC 2119 / BCP 14
  и блоком DoD: [`standards/ba-ontology.md`](standards/ba-ontology.md),
  [`standards/artifact-naming-standard.md`](standards/artifact-naming-standard.md),
  [`standards/team-directory.md`](standards/team-directory.md) (ровно две команды
  `BCREQ` и `CCMO` + механизм добавления),
  [`standards/kb-standard.md`](standards/kb-standard.md),
  [`standards/industry-standards-standard.md`](standards/industry-standards-standard.md),
  [`standards/bcreq-process-standard.md`](standards/bcreq-process-standard.md),
  [`standards/pages-ux-standard.md`](standards/pages-ux-standard.md).
- **ФТ-8 (GitHub Pages):** на странице «Процессы» SPA (рядом с карточками
  процессов из issue #99) добавлена секция «Процессы и подпроцессы с промптами».
  Генератор [`scripts/generate-pages-data.mjs`](scripts/generate-pages-data.mjs)
  строит полный список процессов/подпроцессов в
  [`site/data/process-tree.json`](site/data/process-tree.json) (с флагом
  `hasPrompts` и типом покрытия `kind`), а интерфейс
  ([`site/index.html`](site/index.html), [`site/app.js`](site/app.js),
  [`site/styles.css`](site/styles.css)) по жёсткому требованию выводит **только**
  процессы/подпроцессы с промптами. При > 20 показанных подпроцессах используется
  раскрывающееся дерево (`<details>`/`<summary>`). Прототип (скриншоты) — в
  [ADR-010](docs/adr/010-pages-ux.md).
- Доказательная база: эксперименты
  [`runs/2026/RUN-0009/outputs/standards-applied-ab-2026-06-16.md`](runs/2026/RUN-0009/outputs/standards-applied-ab-2026-06-16.md)
  и
  [`runs/2026/RUN-0008/outputs/kb-citation-check-2026-06-16.md`](runs/2026/RUN-0008/outputs/kb-citation-check-2026-06-16.md).
- Добавлена локальная проверка
  [`scripts/validate_issue_97_ontology_standards.py`](scripts/validate_issue_97_ontology_standards.py)
  (ADR-разделы ФТ-9, RFC 2119/DoD стандартов, инварианты `process-tree.json`,
  две команды, отсутствие выдуманных кодов, сохранность `risk_analysis`) и шаг в
  workflow [`.github/workflows/github-pages.yml`](.github/workflows/github-pages.yml).

### Fixed — Issue #103 корректировки UI каталога промптов

- **ФТ-1. Карточка промпта.** Убрана стрелка (↗) из верхней части карточки;
  нижняя стрелка заменена кнопкой «📁 Перейти в репо», ведущей на файл промпта
  в GitHub репозитории.
- **ФТ-2. Фильтр статуса удалён.** Блок «СТАТУС» убран из панели фильтров;
  удалены связанные обработчики и генерация токенов `status:*`.
- **ФТ-3. Визуальное разделение групп фильтров.** Каждая группа фильтров
  получила рамку, тонированный фон и жирные заголовки: процессы — голубой фон,
  операции — зелёный, режимы — фиолетовый (вариант D из предложений).
- **ФТ-4. Сортировка по убыванию даты.** Опция «По дате» отображается со
  стрелкой ↓, сортировка по умолчанию — последние обновлённые сверху.
- **ФТ-5. Тулбар.** Сортировка и кнопка экспорта перемещены выше поля поиска;
  кнопка экспорта получила явный текстовый ярлык «📥 Скачать».
- **ФТ-6. Кнопки очистки.** Добавлены кнопки «✕ Очистить поиск» и
  «↺ Сбросить фильтры» справа от строки поиска; видимы только при активных
  фильтрах или заполненном поиске.

### Added — Issue #99 оптимизация GitHub Pages (многостраничность и UX)

- **ФТ-1. Многостраничность.** Сайт [`site/index.html`](site/index.html) разбит на
  пять разделов с верхним меню: **Каталог** (главная, URL `/`), **Дашборд**,
  **Roadmap**, **Процессы**, **Паттерны**. Переключение реализовано клиентским
  hash-роутером в [`site/app.js`](site/app.js) (SPA), порядок секций сохранён.
- **ФТ-2. Оптимизация карточек.** Из карточки убраны путь к файлу и хэш рядом с
  «Копировать»; вместо хэша показаны версия (`v…`), дата обновления и статус
  тестов (`✅ N тест(ов)`); ID вынесен мелким шрифтом под названием; добавлена
  кнопка «Ссылка» (↗) — копирует deep-link `#prompt=<id>` на карточку; теги
  процессов получили эмодзи-иконки; описания расширены до 150-300 символов
  (генерируются динамически в [`scripts/generate-pages-data.mjs`](scripts/generate-pages-data.mjs)).
- **ФТ-3. Дашборд.** Блок «Проверки» показывает всего проверок, разбивку
  **по процессам БА** (динамически из frontmatter, с бакетом «Прочее»),
  обратную связь (`prompt:feedback`) и покрытие тестами (X/Y, %). Добавлен блок
  «Активность» — топ-5 промптов. Дублирование метрик убрано.
- **ФТ-4. UX.** Быстрый поиск с автодополнением (по названию/ID/описанию/тегам),
  сортировка (дата, популярность, алфавит, статус), фильтр по статусу
  (Draft/Canonical/Archived), карточка процесса по клику (описание, операции,
  связанные промпты, паттерны, known gaps), экспорт каталога в Markdown по
  текущим фильтрам и переключатель тёмной темы (сохраняется в `localStorage`).
- **ФТ-5. Генерация данных.** Генератор формирует дополнительно
  `site/data/processes.json` и `site/data/patterns.json`, расширенные
  `checks.json` (по процессам, покрытие тестами) и длинные описания промптов;
  процессы и эмодзи назначаются динамически — без хардкода типов артефактов.
- **ФТ-6.** Обновлены README и этот CHANGELOG.
- Добавлена локальная проверка
  [`scripts/validate_issue_99_pages_optimization.py`](scripts/validate_issue_99_pages_optimization.py)
  и шаг в workflow [`.github/workflows/github-pages.yml`](.github/workflows/github-pages.yml).

### Fixed — Issue #95 добавить ID промпта в копируемый текст

- Кнопка «Копировать» в карточке промпта теперь добавляет HTML-комментарий с ID
  в начало копируемого текста: формат `<!-- {prompt.id} -->\n\n{body}`.
- HTML-комментарий добавляется **только при копировании** — в отображаемой карточке
  он не появляется (изменения только в [`site/app.js`](site/app.js)).
- LLM игнорирует HTML-комментарий, при этом ID виден в истории чата и позволяет
  отследить, какой промпт был использован.
- Добавлена локальная проверка
  [`scripts/validate_issue_95_prompt_id_in_copy.py`](scripts/validate_issue_95_prompt_id_in_copy.py)
  и шаг в workflow [`.github/workflows/github-pages.yml`](.github/workflows/github-pages.yml).

### Changed — Issue #92 метаданные промптов (`id` + `title`), удаление EXPERIMENTAL

- В обязательный frontmatter всех 30 промптов (`prompts/` и `prompts/archive/`)
  добавлены поля `id` (уникальный токен `mango-[операция]-[режим]`) и `title`
  (человекочитаемое название на русском).
- Из всех 24 активных промптов удалён маркер
  `<!-- EXPERIMENTAL: DO NOT USE IN PRODUCTION -->`: экспериментальность уже
  отражает `status: draft`.
- Обновлён стандарт промптов: ADR-001
  [`docs/adr/001-prompt-standard.md`](docs/adr/001-prompt-standard.md) и контракт
  [`standards/prompt-standard.md`](standards/prompt-standard.md) теперь требуют
  6 обязательных полей frontmatter (добавлены `id` и `title`).
- Генератор [`scripts/generate-pages-data.mjs`](scripts/generate-pages-data.mjs)
  берёт `id`/`title` из frontmatter и формирует поле `body` — текст промпта без
  frontmatter и маркеров для чистого копирования.
- В интерфейсе GitHub Pages ([`site/app.js`](site/app.js),
  [`site/styles.css`](site/styles.css)) карточка промпта выводит `title` жирным
  заголовком и `id` мелкой меткой; кнопка «Копировать» копирует чистый текст без
  frontmatter.
- В матрицу [`prompts/README.md`](prompts/README.md) добавлены колонки
  «Название» (title) и «Токен» (id); парсер матрицы в генераторе переведён на
  поиск колонок по заголовку.
### Changed — Issue #91 улучшение GitHub Pages (порядок, фильтры, аналитика)

- Изменён порядок секций в [`site/index.html`](site/index.html): **Каталог →
  Дашборд → Проверки → Roadmap**. Каталог промптов теперь основной контент и
  виден сразу (ФТ-1).
- Переупорядочены фильтры каталога в [`site/app.js`](site/app.js): **Процессы БА
  → Операции → Режимы**. Внутри одного фильтра действует логика **ИЛИ**, между
  фильтрами — **И** (ФТ-2).
- Реализована умная каскадная фильтрация: при выборе процесса(ов) фильтр
  «Операции» сужается до операций выбранных процессов (недоступные операции
  подсвечиваются как неактивные), а фильтры «Процессы» и «Режимы» не
  сокращаются (ФТ-3).
- Добавлен модуль **«Проверки»** вместо карточки «Мультиагенты»: статус отладки
  (`draft` / `canonical` / `archived`), число зафиксированных тестов в
  `prompts/experiments/` (каталог позже перенесён в [`runs/`](runs), issue #123),
  обратная связь по лейблу
  `prompt:feedback` и активность использования промптов по процессам БА (ФТ-4).
- [`scripts/generate-pages-data.mjs`](scripts/generate-pages-data.mjs) генерирует
  новый артефакт [`site/data/checks.json`](site/data/checks.json) на основе
  тестовых логов и статического среза
  [`pr-ops/prompt-feedback.json`](pr-ops/prompt-feedback.json) (ФТ-6).
- Решение по `experiments/` vs `scripts/`: корневой `experiments/` отсутствует
  (Python-валидаторы уже консолидированы в `scripts/`), `prompts/experiments/`
  сохранён как каноничное место тестовых логов промптов. Назначение директорий
  задокументировано (ФТ-5).
- Добавлена локальная проверка
  [`scripts/validate_issue_91_pages_enhancements.py`](scripts/validate_issue_91_pages_enhancements.py)
  и шаг в workflow
  [`.github/workflows/github-pages.yml`](.github/workflows/github-pages.yml).

### Added — Issue #86 Mango Office Multichannel widget

- В GitHub Pages шаблон [`site/index.html`](site/index.html) добавлен виджет
  Mango Office Multichannel с `id: 23303`: чат поддержки и заказ обратного
  звонка загружаются перед закрывающим тегом `</body>`.
- Добавлена локальная проверка
  [`scripts/validate_issue_86_mango_widget.py`](scripts/validate_issue_86_mango_widget.py),
  закрепляющая наличие скрипта виджета, идентификатора `23303`, расположение
  перед `</body>` и запись в changelog.
- Workflow [`.github/workflows/github-pages.yml`](.github/workflows/github-pages.yml)
  теперь запускает проверку интеграции виджета вместе с проверкой артефакта
  GitHub Pages.
### Added — Issue #85 библиотека MVP-паттернов БА

- Созданы 7 MVP-паттернов в `patterns/`: `glossary-context-generation`,
  `fr-generation`, `fr-validation`, `user-story-generation`,
  `usecase-generation`, `asr-ingestion` и `meeting-summary-generation`. Каждый
  паттерн содержит 8 полей ADR-002, Product Layer, Commercial Layer, правила
  адаптации, LLM-агностичный `prompt_template`, quality gates, output schema,
  обезличенный пример и ссылки на существующие prompt-реализации.
- Обновлён [`patterns/README.md`](patterns/README.md): добавлены навигация по
  MVP-паттернам, матрица "паттерн ↔ процесс ↔ операция ↔ промпты", пример
  маршрута использования и полные URL связанных PR/репозиториев.
- В [`docs/ba-processes/00-index.md`](docs/ba-processes/00-index.md) заполнена
  колонка "Паттерн" для процессов, покрытых MVP-библиотекой, сохранив
  parser-compatible структуру центрального реестра.
- Добавлена локальная проверка
  [`scripts/validate_issue_85_patterns_library.py`](scripts/validate_issue_85_patterns_library.py)
  для воспроизведения требований issue #85: наличие 7 директорий, 8 секций,
  Product/Commercial Layer, примеров, ссылок на существующие prompts, навигации
  и центрального registry mapping.

### Added — Issue #83 карта процессов БА

- Развёрнут центральный индекс
  [`docs/ba-processes/00-index.md`](docs/ba-processes/00-index.md) в детальную
  карту 9 процессов БА с входами, выходами, workflow, cognitive operations,
  direct links на prompt-файлы и явными manual gaps.
- Добавлены рекомендации по режимам `stepwise` / `oneshot` / `legacy`, связь
  маршрутов с Product Layer и Commercial Layer, 3 сценария запуска процессов с
  Mermaid-диаграммами и полный traceability-блок по связанным PR/репозиториям.
- Добавлена локальная проверка
  [`scripts/validate_issue_83_ba_process_map.py`](scripts/validate_issue_83_ba_process_map.py)
  для воспроизведения требований issue #83: наличие 9 процессов, 13 операций,
  ссылок на 24 активных и 6 архивных prompts, known gaps и навигации.

### Added — Issue #78 промпт-суммаризатор сессий БА

- Создан промпт
  [`prompts/session-debug-documentation-oneshot.md`](prompts/session-debug-documentation-oneshot.md):
  one-shot суммаризация длинной сессии работы с LLM в структурированное резюме
  (контекст, ключевые решения с обоснованием, проблемы и обходные пути,
  применённые промпты, открытые вопросы, следующие шаги). Формат совместим с
  шаблоном блока суммарии в
  [`pr-ops/session-digests.md`](pr-ops/session-digests.md).
- Имя файла приведено к схеме ADR-001 `[домен]-[операция]-[режим].md`
  (`session-debug` / `documentation` / `oneshot`) вместо запрошенного в issue
  рабочего названия `session-debug-summarizer.md`, не соответствующего схеме.
- Промпт добавлен в матрицу
  [`prompts/README.md`](prompts/README.md) (новый раздел «Отладка и
  суммаризация сессий», счётчик активных промптов 23 → 24) и в маппинг процесса
  «Помощь ПО/ПМ»
  [`docs/ba-processes/00-index.md`](docs/ba-processes/00-index.md).
- Добавлен зафиксированный прогон
  [`runs/2026/RUN-0006/outputs/session-debug-summarizer-2026-06-13.md`](runs/2026/RUN-0006/outputs/session-debug-summarizer-2026-06-13.md),
  подтверждающий получение структурированного резюме за один запуск.
- Обновлены контрольные счётчики в
  [`scripts/validate_issue_74_github_pages.py`](scripts/validate_issue_74_github_pages.py)
  (24 активных промпта, 30 всего).

### Added — Issue #74 GitHub Pages interface

- Создан dependency-free GitHub Pages интерфейс в [`site/`](site/): дашборд
  фаз внедрения, каталог 23 активных промптов и 6 архивных файлов, OR-фильтры по
  когнитивным операциям / процессам БА / режимам, поиск и копирование prompt
  content в буфер.
- Добавлен генератор [`scripts/generate-pages-data.mjs`](scripts/generate-pages-data.mjs):
  он читает Markdown source of truth (`prompts/*.md`,
  [`prompts/README.md`](prompts/README.md),
  [`docs/taxonomy.md`](docs/taxonomy.md),
  [`docs/ba-processes/00-index.md`](docs/ba-processes/00-index.md),
  [`docs/ba-ecosystem.md`](docs/ba-ecosystem.md)) и формирует статические
  [`site/data/prompts.json`](site/data/prompts.json),
  [`site/data/stats.json`](site/data/stats.json),
  [`site/data/roadmap.json`](site/data/roadmap.json).
- Настроен workflow
  [`.github/workflows/github-pages.yml`](.github/workflows/github-pages.yml):
  при PR выполняется генерация и проверка, при push в `main` артефакт `site/`
  публикуется в ветку `gh-pages` через `GITHUB_TOKEN`, без PAT и без GitHub API
  в клиентском коде.
- Добавлена локальная проверка
  [`scripts/validate_issue_74_github_pages.py`](scripts/validate_issue_74_github_pages.py)
  для воспроизведения и валидации требований issue #74.
### Added — Issue #76 суммария синхронизации сессий Хаба

- structured: зафиксировать суммарию синхронизации сессий Хаба в
  [`pr-ops/session-digests.md`](pr-ops/session-digests.md): добавлены
  индексная запись `2026-06-14` и блок `#2026-06-14` для передачи контекста
  между Чатом Хаба и Чатом БА Манго.
- Локальная проверка [`scripts/validate_issue_72_hub_sync.py`](scripts/validate_issue_72_hub_sync.py)
  больше не требует пустой индекс `session-digests.md`, так как первая суммария
  теперь сохранена.

### Changed — Issue #72 Smart Sync последних обновлений Хаба

- [`AI_SESSION_HANDOVER_PROMPT.md`](AI_SESSION_HANDOVER_PROMPT.md) синхронизирован
  с Hub PR #226 (`templates/htom/AI_SESSION_HANDOVER_PROMPT.md`, SHA
  `f3e8b265b1577d0ee1fe173dbe16728cc3c7e31b`): добавлен механизм периодической
  суммаризации сессий через `pr-ops/session-digests.md`, сохранены локальные
  правила issue #48/#61 про канал работы через Конарда и task template.
- [`ai-rules/agent-onboarding-protocol_old.md`](ai-rules/agent-onboarding-protocol_old.md)
  обновлён по source SHA `f3e8b265b1577d0ee1fe173dbe16728cc3c7e31b`: встроенный
  копируемый prompt теперь соответствует handover v0.5 и указывает на
  `pr-ops/session-digests.md`.
- Созданы [`pr-ops/session-digests.md`](pr-ops/session-digests.md) как
  пустой локальный индекс суммарий для `mango_ba_prompts` и
  [`pr-ops/artifact-map.md`](pr-ops/artifact-map.md) как локальная карта
  активных артефактов, адаптированная из хабовой карты PR #224/#226.
- Обновлены [`README.md`](README.md), [`.hub-profile.json`](.hub-profile.json) и
  [`pr-ops/migration-manifest.md`](pr-ops/migration-manifest.md), чтобы
  зафиксировать Smart Sync snapshot, source SHA и терминологию
  Пользователь / Исполнитель.
- Добавлена локальная проверка
  [`scripts/validate_issue_72_hub_sync.py`](scripts/validate_issue_72_hub_sync.py)
  для воспроизведения и валидации требований issue #72.
- Досинхронизированы релевантные части Hub PR #229 и Hub PR #230, latest Hub SHA
  `b683341d22d4f518618917a02d9c7c394658b156`.
- Hub PR #229: Base Registry внешних источников
  `research/external-knowledge/external-sources-registry.md` оставлен
  reference-only в Хабе; для Mango в
  [`docs/hub-research-dependencies.md`](docs/hub-research-dependencies.md)
  зарегистрированы строки `ext-003` (Spec-Driven Development) и `ext-007`
  (Контекст-инжиниринг), без создания локального `research/`.
- Hub PR #230: терминология активных guidance-файлов выровнена на
  `Пользователь / Исполнитель` в [`AI_GOVERNANCE.md`](AI_GOVERNANCE.md),
  [`CONTRIBUTING.md`](CONTRIBUTING.md), [`README.md`](README.md),
  [`docs/task-for-konard-template.md`](docs/task-for-konard-template.md) и
  связанных ADR/исторических ссылках; traceability contracts, Framework vs
  Template и Scope Resolver-а задокументированы как Hub-governance контракты,
  не требующие локальных артефактов в `mango_ba_prompts`.

### Added — Issue #65 README для `prompts/`

- Создан [`prompts/README.md`](prompts/README.md): навигация по 23 активным
  промптам и 6 архивным legacy-файлам, матрица назначение ↔ режим ↔ статус ↔
  версия ↔ когнитивная операция ↔ процесс БА, описание структур Hub-style и
  Mango BA workflow, токенов `stepwise` / `oneshot` / `legacy`, процесса
  отладки и ссылок на таксономию, индекс процессов, стандарты и шаблон фидбека.

### Added — Issue #64 ADR на стандарт паттернов

- Создан [`docs/adr/002-pattern-standard.md`](docs/adr/002-pattern-standard.md):
  ADR фиксирует directory-first структуру `patterns/[operation-name]/README.md`,
  8 обязательных полей паттерна, связь с 13 когнитивными операциями и 9
  процессами БА, маппинг паттерн ↔ prompt только через
  [`docs/ba-processes/00-index.md`](docs/ba-processes/00-index.md),
  LLM-агностичность `prompt_template`, правила создания новых паттернов,
  критерии зрелости, semver-версионирование и совместимость с
  [`docs/adr/001-prompt-standard.md`](docs/adr/001-prompt-standard.md).
- [`patterns/README.md`](patterns/README.md) и
  [`standards/pattern-standard.md`](standards/pattern-standard.md) согласованы
  с ADR: README остаётся краткой справкой, стандарт — операционным контрактом
  для review.
- Добавлена локальная проверка
  [`scripts/validate_issue_64_pattern_adr.py`](scripts/validate_issue_64_pattern_adr.py)
  для воспроизведения и валидации требований issue #64.

### Added — Issue #66 экосистема работы БА с графами связей и картой процессов

- Создан [`docs/ba-ecosystem.md`](docs/ba-ecosystem.md) — единая карта
  экосистемы работы БА Mango: методология на основе research Хаба, Mermaid-граф
  связей, определения сущностей, классификации направлений разработки, стилей и
  пакетов документов, правила/практики, матрицы процесс ↔ операция ↔ промпт,
  направление ↔ стиль ↔ шаблон и артефакт ↔ стиль.
- В документ добавлена подробная карта 9 процессов БА: цель, входы, выходы,
  workflow по когнитивным операциям, рекомендуемые промпты и known gaps по
  каждому процессу. Зафиксированы 3 сценария запуска: клиентский заказ,
  внутренняя доработка продукта и тендерное ТЗ.
- Описана стратегия перехода от библиотеки промптов к системным промптам с
  БЗ/RAG, агентам и мультиагентному контуру, включая критерии перехода между
  уровнями и сохранение human gates.
- [`README.md`](README.md) и
  [`docs/ba-processes/00-index.md`](docs/ba-processes/00-index.md) дополнены
  навигацией на экосистемную карту; реестр
  [`docs/hub-research-dependencies.md`](docs/hub-research-dependencies.md)
  отмечает новый документ как consumer релевантных research-якорей Хаба.
- Удалён авто-сгенерированный корневой `.gitkeep`, созданный только для
  открытия draft PR.
### Added — Issue #63 ADR стандарта промптов

- Создан [`docs/adr/001-prompt-standard.md`](docs/adr/001-prompt-standard.md):
  ADR фиксирует две допустимые структуры промптов (Hub-style и Mango BA workflow),
  токены режимов `stepwise` / `oneshot` / `legacy` с обоснованием отказа от
  `expert` / `express`, 4 обязательных поля frontmatter, правила именования
  `[домен]-[операция]-[режим].md`, суффиксы `-legacy` / `-v2` / `-alt` и процессы
  `draft` -> `canonical` / архивации. Существующие промпты не изменялись.

### Changed — Issue #61 Creative-mode governance без архитектурного долга

- [`AI_GOVERNANCE.md`](AI_GOVERNANCE.md), [`AI_QUICK_RULES.md`](AI_QUICK_RULES.md)
  и [`CONTRIBUTING.md`](CONTRIBUTING.md) обновлены: `Structured` сохраняет
  fail-closed semantics, а `Creative` допускает обоснованный обход scope или
  локального правила, если обход нужен для цели задачи и явно описан в PR.
- Зафиксирована специфика работы с Конардом: **молчание = согласие** при merge
  без комментариев; комментарий + ручной перезапуск задачи = итерация в той же
  ветке PR; close PR = отказ от решения.
- [`docs/rfc-hub-integration.md`](docs/rfc-hub-integration.md) переформулирован
  как рекомендательный маршрут передачи практик в Хаб: Хаб — источник лучших
  практик и обмена опытом, не ограничитель локальных решений `mango_ba_prompts`.
- Созданы [`docs/task-for-konard-template.md`](docs/task-for-konard-template.md)
  и [`docs/adr/0003-creative-mode-governance.md`](docs/adr/0003-creative-mode-governance.md):
  шаблон задачи фиксирует WHAT/WHY без пошагового HOW, ADR описывает практику,
  примеры было/стало, обоснованные обходы и self-test на кейсе PR #57.
- [`AI_SESSION_HANDOVER_PROMPT.md`](AI_SESSION_HANDOVER_PROMPT.md) обновлён до
  локального шаблона постановки задач для Конарда.

### Added — Issue #52 фундамент: концепция, таксономия, RFC Хаба и базовая структура

- Создан [`docs/taxonomy.md`](docs/taxonomy.md) — таксономия **13 когнитивных
  операций** (9 базовых + 4 расширенных: `impact_analysis`,
  `reverse_requirements`, `risk_analysis`, `release_readiness`) и **9 процессов
  БА** с маппингом процессов на операции.
- Создан [`docs/rfc-hub-integration.md`](docs/rfc-hub-integration.md) — RFC
  (сознательно **не** ADR) о стратегическом направлении переноса лучших практик
  спока в Хаб: критерии C1–C5, процесс из 6 шагов, provenance
  `source_spoke`/`source_sha`.
- Создан каталог [`patterns/`](patterns/) с README (паттерн = 8 полей:
  `purpose`, `process_stage`, `context_requirements`, `prompt_template`,
  `quality_gates`, `examples`, `output_schema`, `governance_rules`); сами
  паттерны создаются отдельными задачами.
- Создан [`docs/ba-processes/00-index.md`](docs/ba-processes/00-index.md) —
  централизованный маппинг процесс ↔ операции ↔ паттерн ↔ промпты
  (вместо хранения маппинга во frontmatter).
- Создан шаблон таблицы открытых вопросов (дата | автор | суть | статус |
  решение) с правилом автоматической очистки решённых строк Конардом при
  закрытии связанного issue. В issue #80 механизм заменён единым трекером в
  [`pr-ops/BACKLOG.md`](pr-ops/BACKLOG.md#5-открытые-вопросы).
- Созданы контракты [`standards/prompt-standard.md`](standards/prompt-standard.md)
  (ровно 4 обязательных поля frontmatter: `status` со значениями
  `draft`/`canonical`/`archived`, `version`, `updated`, `temperature`;
  именование `[домен]-[операция]-[режим].md`; RAG-формат ссылок
  `См. [Глоссарий](standards/GLOSSARY.md)`; фиксация прогонов в
  `prompts/experiments/`) и
  [`standards/pattern-standard.md`](standards/pattern-standard.md)
  (8 обязательных полей паттерна, универсальный `prompt_template`).
- Создан шаблон issue
  [`.github/ISSUE_TEMPLATE/prompt-feedback.yml`](.github/ISSUE_TEMPLATE/prompt-feedback.yml)
  для фидбека БА: 2 обязательных поля (имя промпта + результат), чек-боксы
  типовых проблем, явный запрет ссылок на закрытые корпоративные документы;
  label `prompt:feedback` проставляется автоматически.
- `README.md` (v2.1): добавлен раздел «Стратегия и тактика» (цель —
  автоматизация БА Mango; тактика — библиотека паттернов и промптов; ссылка
  на RFC), исправлена повреждённая таблица структуры, таблица frontmatter
  приведена к 4 обязательным полям, обновлена навигация.

### Changed — Issue #56 разбиение draft-файла на 23 промпта со стандартизованной схемой именования

- Файл `prompts/drafts/Промпт+для+БА (1).md` (созданный в issue #54 как единый
  draft) разбит на **23 отдельных промпта** по схеме `[домен]-[операция]-[режим].md`
  (kebab-case). **18 новых** промптов размещены в [`prompts/`](prompts/)
  (`status: draft`, `version: 0.1`); **5 legacy-промптов из PDF** также размещены
  в [`prompts/`](prompts/) с суффиксом `-legacy` (`status: draft`, `version: 1.0`),
  так как продолжают использоваться; **6 старых canonical-промптов** перенесены в
  [`prompts/archive/`](prompts/archive/) с суффиксом `-legacy` (`status: archived`,
  `version: 1.0`). Текст каждого промпта скопирован **дословно** (проверено
  побайтово против исходного среза); добавлены обязательный frontmatter (`status`,
  `version`, `updated: 2026-06-11`, `temperature: 0.1`) и experimental marker сразу
  после него.
- **Операции** взяты из таксономии 13 когнитивных операций БА: `understanding`
  (контекст/глоссарий §2, уточняющие вопросы §9.1), `documentation` (ФТ §3.1,
  ограничения §4, резюме встреч §7–8, сопроводительное письмо §9.2), `validation`
  (валидация ФТ §3.2), `solution-design` (системно-технические требования §5),
  `modeling` (User Story §6.1, Use Case §6.2), `ingestion` (пост-обработка ASR §10).
- **Режимы.** Токены `stepwise` (Экспертный, пошаговое согласование) / `oneshot`
  (Экспресс, one-shot) / `legacy` (архивный) выбраны по результатам международного
  исследования (Пользователь допустил «другой режим по результатам исследования»):
  `expert`/`express` не являются стандартной терминологией, а «expert» коллидирует
  с role-prompting-идиомой «act as an expert»; `stepwise` уже используется в
  репозитории (`usecase-stepwise-generator-simple.md`) и совпадает с формулировками
  источника («пошаговый» / «one-shot»). Обоснование и ссылки — в описании PR #57.
- **Removed.** Исходный файл `prompts/drafts/Промпт+для+БА (1).md` удалён **только
  после** успешного создания и побайтовой верификации всех 23 файлов; опустевший
  каталог `prompts/drafts/` удалён. Запись CHANGELOG issue #54 о создании draft
  сохранена как исторический факт — данный шаг её сознательно замещает.

### Added — Issue #54 миграция прикреплённого файла промптов в `prompts/drafts/`

- Создан `prompts/drafts/Промпт+для+БА (1).md` (каталог `prompts/drafts/` позже
  расформирован) — миграция
  единственного файла, прикреплённого к issue #54 (`Промпт+для+БА (1).pdf`, СПИСОК
  ПРОМПТОВ для бизнес-анализа в Телеком SaaS). По правилу issue «один прикреплённый
  файл = один файл в репозитории» PDF перенесён как один draft без разбиения на
  отдельные промпты. Текст промптов скопирован из PDF без изменений; добавлены
  обязательный frontmatter (`status: draft`, `version: 0.1`, `updated: 2026-06-10`,
  `temperature: 0.1`) и experimental marker `<!-- EXPERIMENTAL: DO NOT USE IN PRODUCTION -->`.
- Для draft-файла требуется issue `prompt:review` (labels `prompt:review`, `draft`).
  Создание выполняется мейнтейнером: у автоматизации нет прав `triage`/`push` на
  upstream для применения labels (заготовка issue приведена в описании PR).

### Changed — Issue #48 обогащение `AI_SESSION_HANDOVER_PROMPT.md` (роль члена команды и проверка шаблонов)

- [`AI_SESSION_HANDOVER_PROMPT.md`](AI_SESSION_HANDOVER_PROMPT.md) дополнен командной
  рамкой (issue #48), `version` 0.3 → 0.4. Готовый prompt теперь открывается рамкой
  «ИИ в чате — **член команды** (C, Q, G, D, O), а не «исполнитель без доступа»;
  прямые изменения в репо — через Конарда». В Шаг 2 (ЧЕК-ЛИСТ КОНТЕКСТА) добавлена
  проверка предыдущего контекста чата; в Шаг 3 (READBACK) — учёт канала взаимодействия
  с репо и проверки шаблонов. Добавлены разделы «💬 Контекст чата диалога»,
  «🤝 Роль и канал взаимодействия с репо», «🔍 Проверка шаблонов» и «📝 Формат
  постановки задач для Конарда».
- **Осознанное расхождение с Хабом.** Правки внесены локально поверх базового шаблона
  Хаба [`templates/htom/AI_SESSION_HANDOVER_PROMPT.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/117e4a553815af9b05d841c81dd725dd4a4c4d44/templates/htom/AI_SESSION_HANDOVER_PROMPT.md)
  (SHA `117e4a55`), который этих разделов пока не содержит (проверено: шаблон в `main`
  Хаба идентичен закреплённому SHA). По политике source-of-truth расширение подлежит
  переносу в Хаб с последующей синхронизацией сюда. Ссылка на `templates/task-for-konard.md`
  указывает на ещё не созданный артефакт Хаба (см. PR-описание и issue #48). Провенанс
  (`source_hub`/`source_sha`) и структура EXECUTION/EXPLANATION сохранены.
- Создан [`docs/adr/0002-issue48-handover-local-enrichment.md`](docs/adr/0002-issue48-handover-local-enrichment.md):
  ADR фиксирует осознанные отклонения от буквы issue #48 (аддитивное обогащение вместо
  замены файла, реализация намерения в фактической структуре, условные ссылки на
  отсутствующие шаблоны) и follow-up на перенос расширения в Хаб (Hub-first).

### Added — Issue #46 governance sync with Hub (PR #208)

- Создан корневой артефакт онбординга
  [`AI_SESSION_HANDOVER_PROMPT.md`](AI_SESSION_HANDOVER_PROMPT.md) — готовый к
  копированию *Handover Prompt* для запуска ИИ-агента в новой сессии. Источник —
  Хаб `templates/htom/AI_SESSION_HANDOVER_PROMPT.md`, закреплён permalink-ом на
  merge-SHA PR #208 `117e4a553815af9b05d841c81dd725dd4a4c4d44`. Плейсхолдеры
  `{{REPO_NAME}}`/`{{project_name}}`/`{{hub_url}}` инстанцированы под mango; Шаг 1
  читает реально присутствующие локальные контракты команды, фундаментальные
  governance-контракты Хаба — по permalink-ам.
- Создан протокол онбординга
  [`ai-rules/agent-onboarding-protocol_old.md`](ai-rules/agent-onboarding-protocol_old.md)
  (kebab-case, адаптированная копия канонического протокола Хаба v1.2): семантическое
  разделение «артефакт ↔ протокол» из PR #208. Раздел Design Rationale сжат,
  полная история вынесена ссылкой на Хаб.
- Создан профиль Smart Sync [`.hub-profile.json`](.hub-profile.json) с ключами,
  которые фактически читает `tools/sync-from-hub.sh` Хаба
  (`target_type` / `phase` / `stack` / `hub_url` / `last_sync`).
- Создан [`docs/adr/0001-hub-sync-pr208.md`](docs/adr/0001-hub-sync-pr208.md):
  ADR фиксирует 8 осознанных отклонений от буквы issue (схема профиля, путь
  онбординга, терминология HTOM, подстановка `{{REPO_NAME}}`, Anti-Inflation по
  `tools/`, DoD без валидатора, исправление пути глоссария, permalink-провенанс) и
  сохранённые mango-специфичные правила.
- Добавлены строки навигации в [`README.md`](README.md) на оба новых
  онбординг-файла.

### Changed — sync `AI_GOVERNANCE.md` / `AI_QUICK_RULES.md` from `templates/htom/`

- [`AI_GOVERNANCE.md`](AI_GOVERNANCE.md) синхронизирован с Хабом
  `templates/htom/AI_GOVERNANCE.md` (SHA `117e4a55`): принята терминология
  **«HTOM-команда»**, добавлен provenance (`source_hub`/`source_sha`). Сохранена
  mango-специфичная taxonomy **«Capability Boundaries»** (с реальными путями и
  ссылкой на fail-closed) поверх общей хабовой рубрики. Исправлен стэйл-путь
  `kb/glossary.md` → `standards/GLOSSARY.md`. Строка DoD про
  `./tools/validate-repository-structure.sh` заменена на ориентир
  `docs/audit/initial-state-2026-06.md` (валидатора в mango нет — Anti-Inflation).
- [`AI_QUICK_RULES.md`](AI_QUICK_RULES.md) синхронизирован с Хабом
  `templates/htom/AI_QUICK_RULES.md` (SHA `117e4a55`): терминология
  **«HTOM-команда»**, provenance, различение HTOM-команда ↔ spoke-репозиторий.
  Сохранена явная секция **«Fail-Closed Semantics (КРИТИЧНО)»** (шаблон Хаба её
  свернул), чтобы оставалась резолвимой перекрёстная ссылка из `AI_GOVERNANCE.md`.

### Added — M-009 migration manifest

- Создан живой снимок миграции `pr-ops/migration-manifest.md` (творческое
  улучшение C6 RFC). Содержит таблицу «артефакт → категория → действие → статус →
  назначение в споке» (RFC §5.1) и чек-лист-трекер «Перенесено / Осталось в
  Хабе / Требует уточнения» (RFC §5.3). Зафиксированы 6 промптов, 2 стандарта и
  5 экспериментов как `migrated`, 11 research-артефактов как `referenced`,
  монорепо-`README.md` как `archived` (E3) и 4 пустых плейсхолдера как
  `not-migrated` (P5). Все ссылки на Хаб закреплены permalink-ом на snapshot
  `038868dd125b4e2d849ff73604890f1d2787ac0f` (C3). Манифест ведётся по ходу
  Фаз 0–3 и закрывается в Фазе 3.
### Added — M-007 hub research dependency registry

- Создан единый реестр зависимостей от research Хаба
  `docs/hub-research-dependencies.md` (заголовок «Реестр зависимостей от
  исследований Хаба»). Файл-дубль `hub-research-links.md` не создаётся
  (запрет RFC §3.5).
- Заведены якоря на каждый артефакт `research/mango/*` (`#classification`,
  `#classification-tz`, `#taxonomy-concept`, `#requirements-flow`,
  `#requirements-lifecycle`, `#capability-decomposition`, `#rag-mapping`,
  `#research-readme`) с полным permalink на SHA
  `038868dd125b4e2d849ff73604890f1d2787ac0f` и списком consumers. Промпты и
  контракт классификации резолвят `research_dep` через эти якоря (E1, E8).

### Added — M-006 prompt frontmatter normalization

- Перенесены и нормализованы 6 prompt assets Mango в `prompts/`:
  `tz-stats-generator.md`, `tz-stats-generator-simple.md`,
  `user-story-generator.md`, `user-story-generator-simple.md`,
  `usecase-stepwise-generator.md` и `usecase-stepwise-generator-simple.md`.
  Каждый файл получил 7 обязательных frontmatter-полей, provenance
  (`source_hub`, `source_sha`, `based_on`), явные настройки запуска
  (`temperature: 0.1`, `output_format: markdown`) и отметку
  `migration_status: migrated` после self-test gate.
- Для `_exp`/canonical-вариантов добавлен явный раздел «ФОРМАТ ВЫВОДА»; для
  standalone `_simple`-вариантов с `research_dep: none` добавлен комментарий о
  бизнес-задаче и отсутствии формальной research-зависимости.

### Added — M-004 product classification contract

- Перенесён Mango-only контракт классификации из Хаба в
  `standards/product-classification-contract.md` (переименование из
  `projects/mango/standards/classification-glossary.md`, snapshot
  `038868dd125b4e2d849ff73604890f1d2787ac0f`). Контракт отделён от
  `standards/GLOSSARY.md`, содержит provenance (`source_hub`, `source_sha`) и
  использует `research_dep`-якоря будущего реестра
  `docs/hub-research-dependencies.md` вместо Hub-relative research-ссылок.

### Added — Phase 1 migration scaffold

- Перенесены 5 продуктовых экспериментов Mango из зафиксированного snapshot
  Хаба (`038868dd125b4e2d849ff73604890f1d2787ac0f`) в
  `prompts/experiments/` для M-005: прототип ТЗ-статистики, stepwise alignment
  use-case генератора, генератор user story из raw request, аудит промптов и
  self-test сценарий `prompts-selftest-2026-05-26.md`.
- Создан базовый каркас каталогов Фазы 1 (`prompts/`,
  `prompts/experiments/`, `prompts/archive/`, `standards/`, `kb/`, `docs/`,
  `docs/adr/`, `docs/audit/`) с поясняющими `.gitkeep`-файлами для M-002.
- Скопирован `standards/GLOSSARY.md` из Хаба для M-003: файл закреплён за
  permalink на SHA `038868dd125b4e2d849ff73604890f1d2787ac0f`, содержит
  `source_hub`/`source_sha` и фиксирует, что source of truth остаётся в Хабе,
  а синхронизация выполняется явным действием спока.

### Added — Initial repository structure based on hybrid-Intelligence-lab templates

- Инициализация спока `mango_ba_prompts` из «ДНК-шаблона» Хаба
  (`templates/spoke/`): базовый геном (governance, quick rules, навигация,
  каркасы `docs/adr/`, `docs/audit/`, база знаний `kb/glossary.md`).
- «Бесплатные» улучшения из анализа рекомендаций команд C и Q:
  fail-closed semantics в `AI_QUICK_RULES.md` и capability taxonomy в
  `AI_GOVERNANCE.md`.
- RFC стратегии миграции проекта Mango из Хаба в спок
  (`docs/analysis/migration-strategy-rfc.md`, issue #8): аудит 23 артефактов
  Хаба по полным URL, фазовая стратегия (Mermaid), edge cases, креативные
  улучшения и триггеры эволюции. Стоп-фактор: физический перенос — после
  Human Review.

### Changed

- Добавлен временный workflow создания промптов в `CONTRIBUTING.md` (issue #35,
  M-008): ровно 5 шагов `draft → frontmatter → marker → prompt:review →
  canonical`, capability boundary `prompts/drafts/` и минимальный пример
  frontmatter для черновика без введения матрицы или ADR-процесса.
- Переписан корневой `README.md` под standalone-спок (issue #28, M-001, v2.0):
  README теперь описывает `mango_ba_prompts` как **библиотеку промптов для
  бизнес-аналитиков** (ТЗ-статистика, use-case, user story), а не как базу
  знаний. Добавлены quickstart по чтению frontmatter промптов, структура
  `prompts/` и `standards/`, навигация на `CONTRIBUTING.md` и контакты/роли.
  Удалены унаследованные из «ДНК-шаблона» Хаба прямые и hub-относительные
  ссылки; единственный мост в Хаб — через `docs/hub-research-dependencies.md`.
- Уточнён RFC стратегии миграции (`docs/analysis/migration-strategy-rfc.md`,
  issue #10): добавлена таблица файлов Фазы 1, чек-лист нормализации промптов,
  единый реестр research-зависимостей, корректное разделение
  `standards/GLOSSARY.md` и `standards/product-classification-contract.md`,
  а также правила переноса продуктовых экспериментов.
- Зафиксированы решения Пользователя по Q1–Q4 в RFC миграции
  (`docs/analysis/migration-strategy-rfc.md`, issue #21): таблица Фазы 1
  утверждена, Hub-ссылки должны быть permalink на SHA, self-test стал
  обязательным gate для статуса `migrated`, а стандарты, промпты, эксперименты и
  `hub-research-dependencies.md` идут одним PR Фазы 1.
- Завершена доработка RFC (`docs/analysis/migration-strategy-rfc.md`,
  issue #12, v0.3, блоки 3–8): реестр зависимостей от исследований Хаба (§3.5),
  переписка README.md как обязательная задача Фазы 1, согласованные формулировки
  edge cases E5 (все эксперименты — часть продукта) и E6 (разделение
  глоссария и контракта классификации, §4.1), временный workflow промптов P0
  для `CONTRIBUTING.md` (§5.2) и шаблон Migration Manifest (§5.3).
- Human Review доработанного RFC миграции
  (`docs/reviews/migration-rfc-human-review-2026-06.md`, issue #13): сверка
  v0.3 против чек-листа из 11 пунктов (архитектурная целостность, операционная
  готовность, трассируемость) — все пункты пройдены; зафиксированы открытые
  вопросы Q1–Q4 на решение Пользователя перед стартом Фазы 0.
- Сформирован операционный бэклог Фазы 1 миграции
  (`pr-ops/BACKLOG.md`, issue #14): 9 атомарных задач (M-001…M-009) с
  приоритетами, зависимостями, DoD и трассировкой на разделы утверждённого RFC,
  плюс Mermaid-диаграмма критического пути. Бэклог = один файл (Anti-Inflation);
  выполнение задач не начато.
- Материализован бэклог Фазы 1 в 9 готовых к созданию GitHub Issues
  (`pr-ops/migration-phase1-issues.md`, issue #23): каждый пункт M-001…M-009
  оформлен по стандарту Хаба `ISSUE_WORKFLOW.md` (шаблон `task.yml`) с явным
  Operating Mode (`Creative`/`Structured`), приоритетом, зависимостями, DoD,
  трассировкой на RFC/бэклог и полными permalink-ссылками на Хаб (SHA
  `038868dd…`, решение Q2). Live-Issues создаёт человек при ревью (среда
  AI-агента имеет только `pull`-доступ; создание Issues — fail-closed,
  outward-facing). Сами задачи бэклога не выполняются.

### Removed

- Удалён `kb/glossary.md`: каталог `kb/` сохранён для практик, примеров и
  справочников; глоссарий будет заменён стандартом `standards/GLOSSARY.md` в
  M-003.
- Удалён placeholder `prompts/.gitkeep`: каталог `prompts/` теперь содержит
  реальные нормализованные prompt assets.
- Удалён placeholder `standards/.gitkeep`: каталог `standards/` теперь содержит
  реальный стандарт `standards/GLOSSARY.md`.
- Удалён технический корневой `.gitkeep`, созданный только для bootstrap PR.
