---
status: draft
version: 0.1
updated: 2026-10-23
temperature: 0.1
analysis-subtype: inventory
source: "https://github.com/G-Ivan-A/mango_ba_prompts/issues/384"
scope: repo
based_on: "prompts/ @ dbf1d3c5, docs/analysis/2026-10-20-bcreq-fr-section-prompts.md, standards/bcreq-process-standard.md, docs/ba-processes/00-index.md, runs/2026/RUN-0073, runs/2026/RUN-0074, runs/2026/RUN-0075, runs/2026/RUN-0076"
related_artifacts:
  - "experiments/issue_384_prompts_inventory.py"
  - "experiments/issue_384/inventory.json"
  - "experiments/issue_384_prompt_provenance.py"
  - "experiments/issue_384/prompt-provenance.json"
  - "scripts/validate_issue_384_prompts_audit.py"
  - "docs/analysis/2026-10-20-bcreq-fr-section-prompts.md"
---

# Аудит каталога `prompts/`: инвентаризация и расхождения с целевой структурой BCREQ

## Summary / BLUF

Каталог [`prompts/`](https://github.com/G-Ivan-A/mango_ba_prompts/tree/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts) на снимке `dbf1d3c5` содержит 34 файла. По статусу
аудита: **оставить — 9**, **доработать — 11**, **удалить — 12**, **промпт для
расшифровки — 2**. «Удалить» означает вывод из активного набора: файл становится
legacy или переходит в архив, когда появится замена. Физически удалить предлагается
только избыточный `archive/.gitkeep`. Главный проверенный вывод: активные промпты
формирования документа реализуют **старую модель «ТЗ»**. В ней ФТ — это раздел 4,
пункт 2.3 — «Задачи», раздел 7 детализирует пункты 4.x, роль задана через
CBAP/TM Forum, а модель сама объявляет контекст валидным. Эта модель противоречит
структуре BCREQ-ФТ из анализа 2026-10-20. В чатах прогонов RUN-0074…RUN-0076 это
зафиксировано как дефекты. **18 инцидентов** с происхождением `prompt` дословно
совпадают с текстом двух файлов каталога:
[`glossary-context-understanding-stepwise.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/glossary-context-understanding-stepwise.md)
(16) и [`fr-documentation-stepwise.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/fr-documentation-stepwise.md) (4). Часть
инцидентов совпадает с обоими файлами. **Сравнение со структурой 2.1–2.14 не
выполнено (BLOCKED).** Экспорт чата за 21–23.10.2026, где эта структура описана, к
задаче не приложен. Поэтому сравнение сделано с моделью, которую можно проверить в
репозитории: разделы BCREQ-ФТ, конвейер П1–П6 с гейтами G1–G3 и известные пробелы
карты процессов. Для сравнения с 2.1–2.14 подготовлена пустая матрица.

> **Главный риск 1 — нет источника 2.1–2.14.** В issue сказано, что структура
> описана в «прикреплённом файле экспорта чата». Такого вложения нет ни в
> [issue #384](https://github.com/G-Ivan-A/mango_ba_prompts/issues/384), ни в
> комментариях к нему, ни в [PR #385](https://github.com/G-Ivan-A/mango_ba_prompts/pull/385).
> В репозитории нет экспорта, окно которого попадает в 21–23.10.2026. Последнее
> окно — RUN-0073, оно заканчивается 2026-10-19 10:56:30 UTC
> ([inputs RUN-0073](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/runs/2026/RUN-0073/inputs/README.md)). Совпадения строки
> «2.14» в репозитории относятся к пункту шаблона тендерного ТЗ «текстовые каналы»
> ([BRIEF issue #382, L40](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/experiments/issue_382/research/BRIEF.md?plain=1#L40)),
> а не к структуре промптов. Пока экспорта нет, нельзя проверить, противоречит ли
> 2.1–2.14 каталогу или процессу BCREQ. Это требует правило отклонений issue.
>
> **Главный риск 2 — каталог противоречит BCREQ-ФТ (проверено).** Если новую
> структуру собрать «поверх» существующих файлов, вместе с ними переедут дефекты,
> которые БА уже отклонил в трёх чатах (§3.4). **Альтернативный вектор для
> Задачи 2** описан в §3.8. Строить стандарт от конвейера
> [П1–П6](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/standards/bcreq-process-standard.md?plain=1#L58) и разделов BCREQ-ФТ
> (промпты а)/б)/в) анализа 2026-10-20). Структуру 2.1–2.14 использовать как
> чек-лист полноты после того, как экспорт будет приложен. Текущие файлы считать
> донорами отдельных механик, а не основой.

## 1. Context / Scope

- **Предмет учёта:** все файлы каталога `prompts/`, включая `prompts/archive/`,
  README и служебные промпты.
- **Снимок:** коммит
  [`dbf1d3c5`](https://github.com/G-Ivan-A/mango_ba_prompts/tree/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d)
  (`main` на 2026-10-23). Все ссылки на файлы закреплены за этим коммитом, поэтому
  номера строк не «уедут». Аудит только читал файлы: в `prompts/` ничего не
  изменено, не удалено и не перемещено.
- **Дата и автор:** 2026-10-23, исполнитель issue #384 (режим Hybrid). Решения по
  статусам принимает Пользователь.
- **Источники:**
  - метаданные и текст файлов — их собрал скрипт
    [`issue_384_prompts_inventory.py`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384_prompts_inventory.py),
    результат в [`inventory.json`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/inventory.json);
  - атрибуция дефектов шаблонов к файлам каталога — скрипт
    [`issue_384_prompt_provenance.py`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384_prompt_provenance.py),
    результат в [`prompt-provenance.json`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/prompt-provenance.json);
  - целевая модель разделов и правил — [анализ 2026-10-20](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/docs/analysis/2026-10-20-bcreq-fr-section-prompts.md);
  - процесс — [`bcreq-process-standard.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/standards/bcreq-process-standard.md);
  - карта процессов — [`00-index.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/docs/ba-processes/00-index.md);
  - журналы чатов — реестры инцидентов и критериев успеха RUN-0073…RUN-0076.
- **Как ссылаться на сообщения чатов.** Экспорты чатов — JSON-вложения GitHub, у
  отдельных сообщений нет своих URL. Поэтому сообщение адресуется тремя
  элементами: URL экспорта, номер реплики («р. N» — сквозной номер сообщения в
  экспорте) и абсолютная ссылка на строку реестра. В строке реестра реплика
  процитирована дословно.

  | Прогон | Экспорт чата | Окно, UTC | Реплик |
  | --- | --- | --- | --- |
  | RUN-0073 | [chat-export-1123.json](https://github.com/user-attachments/files/33662573/chat-export-1123.json) | 2026-10-16 — 2026-10-19 | 106 |
  | RUN-0074 | [chat-export-1106.json](https://github.com/user-attachments/files/33668084/chat-export-1106.json) | 2026-09-15 — 2026-10-01 | 214 |
  | RUN-0075 | [chat-export-1104.json](https://github.com/user-attachments/files/33669481/chat-export-1104.json) | 2026-09-16 — 2026-09-28 | 118 |
  | RUN-0076 | [chat-export-1110.json](https://github.com/user-attachments/files/33669255/chat-export-1110.json) | 2026-10-01 — 2026-10-13 | 156 |

- **Критерии статуса аудита:**

  | Статус | Критерий |
  | --- | --- |
  | оставить | Файл исправно выполняет свою функцию, и новая структура BCREQ-ФТ его не заменяет. Либо это архив, на который ссылаются зафиксированные прогоны. |
  | доработать | Функция нужна в новой модели, и замены в анализе 2026-10-20 нет. При этом в тексте есть дефекты, подтверждённые чатами или стандартом. |
  | удалить | Функцию заменяют промпты а)/б)/в) или проверка второй ролью из анализа 2026-10-20. Либо файл дублирует более новый вариант. Либо файл избыточен (`.gitkeep`). Удалить — значит вывести из активного набора, сделать legacy или перенести в архив. |
  | промпт для расшифровки | Обработка расшифровки ASR — отдельный вход конвейера П1. |

- **Тематика** — по функции файла:

  | Тема | Функция |
  | --- | --- |
  | А | формирование документа ФТ/ТЗ |
  | Б | валидация |
  | В | элицитация и коммуникация |
  | Г | моделирование UC/US |
  | Д | расшифровка ASR |
  | Е | служебные и governance |
  | Ж | навигация |
  | З | архив |

- **Противоречие в постановке.** Этап 3 issue говорит «отчёт — исключительно
  анализ без рекомендаций и оценок». DoD и «Зоны свободы» требуют
  аргументированных списков «что удалить / доработать / оставить» и
  профессиональной оценки. Принятое решение: Findings (§2–§3) содержат только
  установленные факты и их интерпретацию. Списки находятся в Recommendations (§4)
  и **не задают обязательности применения**: это входные данные Задачи 2, решение
  за Пользователем.
- **Вне охвата:** финальный стандарт структуры промптов (Задача 2) и содержание
  2.1–2.14 (см. главный риск 1).

## 2. Findings: инвентаризация

### 2.1. Сводная таблица

Легенда маркеров. Маркеры — лексические совпадения, которые нашёл скрипт
инвентаризации. Это не вердикт: доказательства с номерами строк приведены в §3.

| Код | Значение |
| --- | --- |
| R | роль задана через методологию: CBAP / TM Forum / ODA / ITIL |
| S | старая модель разделов: ФТ = раздел 4, «2.3. Задачи», 4.x/7.x |
| Б | запрет «Система должна» |
| C | модель сама себя сертифицирует: ✅, «Отчет валидации», «Контекст валиден» |
| К | «креативная» генерация |
| E | английские метки |
| Н | правило «не выдумывай» или плейсхолдер уточнения |
| G | стоп-гейты |
| F | поле статуса `ready \| draft \| needs-clarification` |

Столбец «Пр.» — процессы [00-index](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/docs/ba-processes/00-index.md?plain=1#L110)
(1 ФТ/ТЗ, 2 Валидация, 3 Тендер, 4 UC/US, 5 UML/BPMN, 6 ПО/ПМ, 7 Статистика,
8 Impact, 9 Risk). Столбец «Прогоны» — каталоги
[`runs/2026/`](https://github.com/G-Ivan-A/mango_ba_prompts/tree/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/runs/2026), где упоминается файл.

<!-- inventory:table -->
| № | Файл | Тема | Пр. | fm status / version | Прогоны | Маркеры | Статус аудита | Обоснование |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [AI_SESSION_HANDOVER_PROMPT.executable.md](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/AI_SESSION_HANDOVER_PROMPT.executable.md) | Е | — | draft / 0.2 | — | Н | доработать | Governance-промпт онбординга чата, а не БА-операция. Нет `id`/`title`, ключи `type`/`layer`/`full_version` — схема executable-слоя. Не входит в карту процессов и README. Блок «Периодическая суммаризация» ([L66](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/AI_SESSION_HANDOVER_PROMPT.executable.md?plain=1#L66)) пересекается с session-debug. |
| 2 | [README.executable.md](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/README.executable.md) | Ж | — | draft / 0.1 | — | S | доработать | Быстрый выбор направляет «Раздел 4 ФТ» на fr-documentation ([L41](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/README.executable.md?plain=1#L41)), то есть закрепляет старую нумерацию. Во frontmatter `ai-generated: true`. |
| 3 | [README.md](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/README.md) | Ж | — | draft / 0.1 | — | — | доработать | Полная матрица промптов. Устареет вместе с маршрутизацией. Во frontmatter `ai-generated: true`. |
| 4 | [archive/.gitkeep](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/archive/.gitkeep) | З | — | — | — | — | удалить | Избыточен: в каталоге 6 файлов. |
| 5 | [archive/tz-stats-generator-legacy.md](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/archive/tz-stats-generator-legacy.md) | З | 7 | archived / 1.0 | 0001 | Н | оставить | Исторический источник; на него ссылается RUN-0001. |
| 6 | [archive/tz-stats-generator-simple-legacy.md](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/archive/tz-stats-generator-simple-legacy.md) | З | 7 | archived / 1.0 | 0001 | — | оставить | То же. Суффикс `-simple` и перегруженный frontmatter (`source_hub`, `selftest_*`) — следы миграции. |
| 7 | [archive/usecase-stepwise-generator-legacy.md](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/archive/usecase-stepwise-generator-legacy.md) | З | 4 | archived / 1.0 | 0003 | — | оставить | Предшественник uc-modeling; RUN-0003. |
| 8 | [archive/usecase-stepwise-generator-simple-legacy.md](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/archive/usecase-stepwise-generator-simple-legacy.md) | З | 4 | archived / 1.0 | 0003 | — | оставить | То же. |
| 9 | [archive/user-story-generator-legacy.md](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/archive/user-story-generator-legacy.md) | З | 4 | archived / 1.0 | 0002 | E | оставить | Предшественник us-modeling; RUN-0002. |
| 10 | [archive/user-story-generator-simple-legacy.md](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/archive/user-story-generator-simple-legacy.md) | З | 4 | archived / 1.0 | 0002 | E Н | оставить | То же. |
| 11 | [asr-ingestion-legacy.md](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/asr-ingestion-legacy.md) | Д | 1 | draft / 1.0 | — | — | промпт для расшифровки | Блоки по ~5000 знаков ([L41](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/asr-ingestion-legacy.md?plain=1#L41)), глобальный словарь подтверждённых замен ([L13](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/asr-ingestion-legacy.md?plain=1#L13)), обязательное подтверждение замен ([L141](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/asr-ingestion-legacy.md?plain=1#L141)). Нет секции формата вывода. Прогонов нет. |
| 12 | [asr-ingestion-oneshot.md](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/asr-ingestion-oneshot.md) | Д | 1, 6, 9 | draft / 0.1 | — | E Н F | промпт для расшифровки | Есть формат вывода со статусом ([L43](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/asr-ingestion-oneshot.md?plain=1#L43)) и блоком «Требует проверки» ([L48](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/asr-ingestion-oneshot.md?plain=1#L48)). Прогонов нет. |
| 13 | [constraints-documentation-oneshot.md](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/constraints-documentation-oneshot.md) | А | 1, 9 | draft / 0.1 | 0007 | R | удалить | Раздел 6 закрывает промпт в) анализа 2026-10-20. Требует 4–6 «сгенерированных» ограничений ([L31](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/constraints-documentation-oneshot.md?plain=1#L31)). |
| 14 | [constraints-documentation-stepwise.md](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/constraints-documentation-stepwise.md) | А | 1, 2, 9 | draft / 0.1 | 0007, 0010, 0012, 0013, 0016 | R S К G | удалить | Раздел 6 закрывает промпт в). Вход — «Раздел 4 (ФТ)» ([L32](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/constraints-documentation-stepwise.md?plain=1#L32)), «Майнинг ограничений (Креативный анализ границ)» ([L39](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/constraints-documentation-stepwise.md?plain=1#L39)). |
| 15 | [fr-documentation-oneshot.md](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/fr-documentation-oneshot.md) | А | 1 | draft / 0.1 | 0026 | R S C | удалить | ФТ закрывает промпт б). Генерирует «Раздел 4» ([L10](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/fr-documentation-oneshot.md?plain=1#L10)) и «Отчет валидации» по ODA ([L30](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/fr-documentation-oneshot.md?plain=1#L30)). |
| 16 | [fr-documentation-stepwise.md](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/fr-documentation-stepwise.md) | А | 1, 2, 4, 9 | draft / 0.1 | 0006, 0007, 0010, 0012, 0013, 0016, 0017, 0026 | R S К G | удалить | ФТ закрывает промпт б). Дословный источник 4 инцидентов RUN-0074/0075 (§3.4). |
| 17 | [fr-validation-legacy.md](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/fr-validation-legacy.md) | Б | 1, 2, 3 | draft / 1.0 | 0023, 0028 | R | удалить | Дубль fr-validation-stepwise: TM Forum Frameworx/ITIL ([L16](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/fr-validation-legacy.md?plain=1#L16)), «сертифицированные бизнес-аналитики (cisco)» ([L18](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/fr-validation-legacy.md?plain=1#L18)), температура задана в тексте ([L29](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/fr-validation-legacy.md?plain=1#L29)). Перенести в архив: на него ссылаются прогоны. |
| 18 | [fr-validation-oneshot.md](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/fr-validation-oneshot.md) | Б | 1, 2, 3, 8, 9 | draft / 0.1 | 0006 | R S | удалить | Экспресс-аудит заменяет проверка второй ролью отдельным вызовом (§5.4 анализа 2026-10-20). |
| 19 | [fr-validation-stepwise.md](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/fr-validation-stepwise.md) | Б | 1, 2, 3, 4, 8, 9 | draft / 0.1 | 0013, 0015, 0018, 0021, 0022, 0023, 0025, 0027 | R S G | доработать | Ценная структура аудита «пункт → проблема → вариант». Но она привязана к 4.x, и встретив `...`, модель сама «формулирует требование на основе контекста» ([L25](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/fr-validation-stepwise.md?plain=1#L25)). |
| 20 | [glossary-context-understanding-oneshot.md](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/glossary-context-understanding-oneshot.md) | А | 1, 3, 4 | draft / 0.1 | — | Б S Н | удалить | Разделы 1–2 закрывает промпт а). «Задачи: 3–5 пунктов» ([L31](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/glossary-context-understanding-oneshot.md?plain=1#L31)) вместо «Границ». |
| 21 | [glossary-context-understanding-stepwise.md](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/glossary-context-understanding-stepwise.md) | А | 1, 3, 4, 9 | draft / 0.1 | 0007, 0010, 0011, 0012, 0013, 0014, 0017, 0020, 0021, 0025, 0027 | R Б S К C G | удалить | Разделы 1–2 закрывает промпт а). Дословный источник 16 инцидентов RUN-0074…0076 (§3.4). Механики-доноры перечислены в §3.6. |
| 22 | [letter-customer-documentation-legacy.md](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/letter-customer-documentation-legacy.md) | В | 6 | draft / 1.0 | — | — | доработать | Единственный промпт письма, поэтому метка режима `legacy` вводит в заблуждение. Формат вывода дан простым текстом ([L35](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/letter-customer-documentation-legacy.md?plain=1#L35)). Прогонов нет. |
| 23 | [meeting-customer-documentation-stepwise.md](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/meeting-customer-documentation-stepwise.md) | В | 6 | draft / 0.1 | 0013 | R E Н F G | оставить | Процесс 6 структура BCREQ-ФТ не заменяет. Стоп-гейты ([L20](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/meeting-customer-documentation-stepwise.md?plain=1#L20)), поле статуса ([L46](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/meeting-customer-documentation-stepwise.md?plain=1#L46)). Роль CBAP ([L11](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/meeting-customer-documentation-stepwise.md?plain=1#L11)) — косметика. |
| 24 | [meeting-team-documentation-stepwise.md](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/meeting-team-documentation-stepwise.md) | В | 6 | draft / 0.1 | — | R E Н F G | оставить | Почти дубль № 23: тот же скелет из шагов 1–4. Отличается блоком «Оценка и зависимости» ([L40](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/meeting-team-documentation-stepwise.md?plain=1#L40)) и «Не определено» ([L66](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/meeting-team-documentation-stepwise.md?plain=1#L66)). Прогонов нет. |
| 25 | [questions-customer-understanding-legacy.md](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/questions-customer-understanding-legacy.md) | В | 1, 3, 6 | draft / 1.0 | 0024 | R C Н | удалить | Заменён stepwise-версией. «Команда сертифицированных» ([L11](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/questions-customer-understanding-legacy.md?plain=1#L11)), чек-лист ✅ ([L50](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/questions-customer-understanding-legacy.md?plain=1#L50)). Перенести в архив: на него ссылается RUN-0024. |
| 26 | [questions-customer-understanding-stepwise.md](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/questions-customer-understanding-stepwise.md) | В | 1, 3, 6, 9 | draft / 0.1 | 0011, 0012, 0013, 0019, 0024 | R E Н F G | доработать | Сильный донор: «Заявленное решение vs Заявленная боль» ([L24](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/questions-customer-understanding-stepwise.md?plain=1#L24)), 5 Whys ([L49](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/questions-customer-understanding-stepwise.md?plain=1#L49)), проверка существующих решений ([L60](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/questions-customer-understanding-stepwise.md?plain=1#L60)), «⚠️ Требует проверки у ПО» ([L27](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/questions-customer-understanding-stepwise.md?plain=1#L27)). Требует согласования с реестром вопросов раздела 7. |
| 27 | [session-debug-documentation-oneshot.md](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/session-debug-documentation-oneshot.md) | Е | 6 | draft / 0.2 | 0006 | R Н F | оставить | Работает (RUN-0006). Правило «Не выдумывай» ([L31](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/session-debug-documentation-oneshot.md?plain=1#L31)). Роль CBAP ([L11](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/session-debug-documentation-oneshot.md?plain=1#L11)) не нужна служебному промпту. |
| 28 | [technical-details-solution-design-legacy.md](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/technical-details-solution-design-legacy.md) | А | 1 | draft / 1.0 | — | R S | удалить | Дубль stepwise-версии. TM Forum Frameworx (eTOM, ODA) ([L13](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/technical-details-solution-design-legacy.md?plain=1#L13)). Перенести в архив. |
| 29 | [technical-details-solution-design-oneshot.md](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/technical-details-solution-design-oneshot.md) | А | 1, 8 | draft / 0.1 | — | R S Н | удалить | Пункты 7.x жёстко связаны с 4.x. Плейсхолдер `[ТРЕБУЕТСЯ УТОЧНЕНИЕ…]` ([L21](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/technical-details-solution-design-oneshot.md?plain=1#L21)) есть и в stepwise-версии. Прогонов нет. |
| 30 | [technical-details-solution-design-stepwise.md](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/technical-details-solution-design-stepwise.md) | А | 1, 8, 9 | draft / 0.1 | 0011 | R S C Н G | доработать | Раздел 7 «для разработчиков» в BCREQ остаётся (правило П3, SC-31). Но 7.x ↔ 4.x ([L17](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/technical-details-solution-design-stepwise.md?plain=1#L17)), право добавлять пункты 7.x ([L18](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/technical-details-solution-design-stepwise.md?plain=1#L18)), самопроверка «Dev Readiness Check» ([L62](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/technical-details-solution-design-stepwise.md?plain=1#L62)). |
| 31 | [uc-modeling-oneshot.md](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/uc-modeling-oneshot.md) | Г | 1, 4, 5 | draft / 0.1 | — | R E Н F C | доработать | Процесс 4 BCREQ-ФТ не заменяет. Самооценка «Полнота: ✅/⚠️» ([L53](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/uc-modeling-oneshot.md?plain=1#L53)), роль CBAP ([L11](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/uc-modeling-oneshot.md?plain=1#L11)). |
| 32 | [uc-modeling-stepwise.md](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/uc-modeling-stepwise.md) | Г | 1, 4, 5, 9 | draft / 0.1 | 0011, 0013 | R Н F C G | доработать | То же; есть стоп-гейты по шагам. |
| 33 | [us-modeling-oneshot.md](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/us-modeling-oneshot.md) | Г | 1, 4 | draft / 0.1 | — | R E Н F C | доработать | «JOB STORY» с английскими метками INVEST/BDD ([L27](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/us-modeling-oneshot.md?plain=1#L27)), «Independent: ✅/⚠️» ([L49](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/us-modeling-oneshot.md?plain=1#L49)). |
| 34 | [us-modeling-stepwise.md](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/us-modeling-stepwise.md) | Г | 1, 4, 9 | draft / 0.1 | 0011, 0013 | R E Н F C G | доработать | Шаг «Формирование Job Story» просит «Сформируй User Story» ([L37](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/us-modeling-stepwise.md?plain=1#L37)) — смешаны две техники. Самооценка ✅ ([L68](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/us-modeling-stepwise.md?plain=1#L68)). |
<!-- /inventory:table -->

Итоги таблицы:

| Статус аудита | Файлов | Номера |
| --- | --- | --- |
| оставить | 9 | 5–10, 23, 24, 27 |
| доработать | 11 | 1–3, 19, 22, 26, 30–34 |
| удалить | 12 | 4, 13–18, 20, 21, 25, 28, 29 |
| промпт для расшифровки | 2 | 11, 12 |

| Тема | А | Б | В | Г | Д | Е | Ж | З |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Файлов | 9 | 3 | 5 | 4 | 2 | 2 | 2 | 7 |

### 2.2. Метаданные корпуса

- **Даты.** 23 из 25 файлов-промптов датированы 2026-06-11; session-debug —
  2026-06-20, handover — 2026-08-21. Анализ 2026-10-20 со структурой
  BCREQ-ФТ на четыре месяца новее. Ни один активный промпт не переведён в
  `canonical`, все имеют статус `draft`. При этом пять файлов с меткой `legacy`
  имеют `version: 1.0` и тот же статус `draft`. Это №№ 11, 17, 22, 25, 28.
- **Маркеры.** Ниже частоты маркеров по 27 активным файлам; архив и `.gitkeep`
  не учитываются.

  | Маркер | Файлов |
  | --- | --- |
  | R | 20 |
  | Н | 14 |
  | S | 11 |
  | G | 10 |
  | F | 9 |
  | C | 8 |
  | E | 7 |
  | К | 3 |
  | Б | 2 |

- **Формат вывода.** Лексическая проверка не нашла заголовка формата вывода или
  ответа в 15 из 25 файлов-промптов. У letter-legacy формат дан простым текстом
  ([L35](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/letter-customer-documentation-legacy.md?plain=1#L35)). Без формата
  вывода остались все промпты темы А (9), темы Б (3), а также asr-legacy, handover
  и letter-legacy.
- **Прогоны.** У десяти файлов-промптов нет ни одного зафиксированного прогона:
  №№ 1, 11, 12, 20, 22, 24, 28, 29, 31, 33. Чаще всего встречаются glossary-stepwise
  (11 прогонов), fr-documentation-stepwise и fr-validation-stepwise (по 8).

### 2.3. Дубли и близкие варианты

| Группа | Файлы (№) | Характер пересечения |
| --- | --- | --- |
| Триплеты по режиму | 17/18/19 (fr-validation), 28/29/30 (technical-details), 25/26 (questions), 20/21 (glossary), 13/14 (constraints), 15/16 (fr-documentation), 31/32 (uc), 33/34 (us), 11/12 (asr) | Варианты одной операции расходятся по содержанию, а не только по режиму. Например, oneshot-глоссарий прячет блок «АНАЛИЗ КОНТЕКСТА» ([L20](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/glossary-context-understanding-oneshot.md?plain=1#L20)) и разрешает термины «[Предложено ИИ]» ([L27](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/glossary-context-understanding-oneshot.md?plain=1#L27)); в stepwise-версии этих правил нет. |
| Встречи по аудитории | 23 / 24 | Одинаковый скелет шагов 1–4 и формата вывода; отличаются 1–2 блоками. |
| Сессии LLM | 1 / 27 | Handover содержит блок периодической суммаризации ([L66](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/AI_SESSION_HANDOVER_PROMPT.executable.md?plain=1#L66)), а это функция session-debug. |
| Архив ↔ активные | 7–8 ↔ 31–32, 9–10 ↔ 33–34 | Ожидаемое наследование, не дефект. |
| README | 2 / 3 | Каскадные слои по [cascading-context-loading-standard](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/standards/cascading-context-loading-standard.md), не дубль. Но оба нужно обновлять синхронно. |

## 3. Findings: архитектурные наблюдения

### 3.1. Покрытие разделов BCREQ-ФТ

Целевая структура разделов взята из анализа 2026-10-20: промпт а) — разделы 1–2
([L543](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/docs/analysis/2026-10-20-bcreq-fr-section-prompts.md?plain=1#L543)), б) — 3 и 5 ([L613](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/docs/analysis/2026-10-20-bcreq-fr-section-prompts.md?plain=1#L613)), в) — 4 и 6 ([L678](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/docs/analysis/2026-10-20-bcreq-fr-section-prompts.md?plain=1#L678)). Раздел 7
формируется только по запросу БА: правило П3 ([L783](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/docs/analysis/2026-10-20-bcreq-fr-section-prompts.md?plain=1#L783)) и правило О11
([L530](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/docs/analysis/2026-10-20-bcreq-fr-section-prompts.md?plain=1#L530)). Нумерацию подтвердил сам БА в RUN-0076, р. 10: «1-4 - да, 5 будет
НФТ (обычно пустой), 6 - ограничения» ([реестр L66](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/runs/2026/RUN-0076/outputs/incident-register.md?plain=1#L66),
[экспорт](https://github.com/user-attachments/files/33669255/chat-export-1110.json)).

| Раздел BCREQ-ФТ | Что есть в `prompts/` | Разрыв |
| --- | --- | --- |
| 1 Термины | 20, 21: раздел 1 «Терминология» с защитой глоссария ([L20](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/glossary-context-understanding-stepwise.md?plain=1#L20)) | Промпт предлагает модели придумать новые термины: «предложи 1-2 новых термина» ([L41](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/glossary-context-understanding-stepwise.md?plain=1#L41)). БА это отклонил: RUN-0076 I-005, р. 12. |
| 2 Бизнес-контекст и границы (2.1 Проблема, 2.2 Цель, 2.3 Границы) | 20, 21: «2.3. Задачи» ([L50](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/glossary-context-understanding-stepwise.md?plain=1#L50)), «Укажи бизнес-последствия» ([L48](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/glossary-context-understanding-stepwise.md?plain=1#L48)) | Нет пункта «Границы». Модель придумывает риски и последствия (RUN-0076 I-004, р. 12: «Не придумывать риски, если они явно не заданы заказчиком»). |
| 3 ФТ («Система должна») | 15, 16 производят ФТ как «Раздел 4» ([L12](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/fr-documentation-stepwise.md?plain=1#L12)). Промпт 21 запрещает «Система должна» и называет её «уровнем Раздела 4» ([L15–L16](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/glossary-context-understanding-stepwise.md?plain=1#L15)) | Номер раздела сдвинут. Запрет на «Систему должна» БА снял: RUN-0074 р. 52, RUN-0076 р. 10. |
| 4 Описание решения | нет | Пробел: в старой модели раздел 4 — это ФТ. |
| 5 НФТ | нет | Пробел. Модель сама пропускала НФТ (RUN-0076 I-022, [L85](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/runs/2026/RUN-0076/outputs/incident-register.md?plain=1#L85)). |
| 6 Ограничения | 13, 14: фиксированные 6.1.1–6.1.3 MANGO OFFICE ([L15](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/constraints-documentation-stepwise.md?plain=1#L15)) и «майнинг» новых | Модель генерирует ограничения, которые не следуют из источника. Внешнюю разработку ограничения не учитывают (RUN-0073 I-012, р. 6: «ЭТО РАЗРАБОТКА НЕ НА СТОРОНЕ МАНГО», [L73](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/runs/2026/RUN-0073/outputs/incident-register.md?plain=1#L73)). |
| 7 Заметки разработчикам и реестр вопросов (по запросу БА) | 28–30 — раздел 7 «Список доработок»; 25, 26 — вопросы | Раздел 7 нужен (SC-31, RUN-0076 р. 66: «Можно в разделе 7 комментарием указать то, что для разработчиков», [L80](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/runs/2026/RUN-0076/outputs/success-criteria.md?plain=1#L80)). Но связь 7.x ↔ 4.x устарела. Реестра вопросов как части документа нет. |

### 3.2. Покрытие конвейера П1–П6 и гейтов

| Этап ([стандарт](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/standards/bcreq-process-standard.md?plain=1#L58)) | Файлы | Разрыв |
| --- | --- | --- |
| П1 Приём и нормализация ([L58](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/standards/bcreq-process-standard.md?plain=1#L58)) | 11, 12, 20, 21, 25, 26 | Покрыт, но в старой модели. Нет правила сносок на источник (RUN-0074 SC-02, р. 16: «Все утверждения размечайте сносками», [L25](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/runs/2026/RUN-0074/outputs/success-criteria.md?plain=1#L25)). |
| П2 Декомпозиция на уровни BCREQ, гейт G1 ([L59](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/standards/bcreq-process-standard.md?plain=1#L59)) | нет; 34 разбивает только составную story | **Пробел:** нет промпта для построения дерева BCREQ. |
| П3 Моделирование ([L60](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/standards/bcreq-process-standard.md?plain=1#L60)) | 31–34 | Покрыт. |
| П4 Документирование и solution design ([L61](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/standards/bcreq-process-standard.md?plain=1#L61)) | 13–16, 20, 21, 28–30 | Покрыт по старой нумерации. Нет раздела 4 «Описание решения» и раздела 5 НФТ. |
| П5 Валидация и риски, гейт G2 ([L62](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/standards/bcreq-process-standard.md?plain=1#L62)) | 17–19 | Только валидация. Нет `risk_analysis` и `quality`; проверки второй ролью отдельным вызовом ([§5.4, L746](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/docs/analysis/2026-10-20-bcreq-fr-section-prompts.md?plain=1#L746)) тоже нет. |
| П6 Утверждение и baselining, гейт G3 ([L63](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/standards/bcreq-process-standard.md?plain=1#L63)) | нет | **Пробел.** |
| Правило B3: гейты не проходятся LLM автоматически ([L89](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/standards/bcreq-process-standard.md?plain=1#L89)) | 15, 21, 30, 31–34 | **Нарушается.** Промпты сами объявляют контекст валидным: «Контекст валиден и готов к формированию Раздела 4» ([L64](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/glossary-context-understanding-stepwise.md?plain=1#L64)), «Dev Readiness Check», чек-листы ✅. БА ставит статус «согласовано» сам (RUN-0073 SC-04, р. 26, [L27](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/runs/2026/RUN-0073/outputs/success-criteria.md?plain=1#L27)). |
| Правила B4–B7: `needs-clarification` ([L94](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/standards/bcreq-process-standard.md?plain=1#L94)) | поле статуса в 9 файлах (F) | Статус ставится, но нет причины, owner'а, точки останова и возврата в конвейер. Этого требуют B4 и B7. |

### 3.3. Известные пробелы карты процессов

[Known gaps 00-index](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/docs/ba-processes/00-index.md?plain=1#L276) перечисляет
11 пробелов. Ни один не закрыт в `prompts/`:

- оркестратор цепочки ФТ/ТЗ ([L284](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/docs/ba-processes/00-index.md?plain=1#L284));
- quality и статистика дефектов (L285);
- приём тендерных DOCX/PDF/XLSX (L286);
- tender-fit и no-bid (L287);
- UML/BPMN/Mermaid (L288);
- decision log и stakeholder map (L289);
- reverse requirements и impact (L290);
- risk register и release readiness (L291);
- RAG-навигатор (L292);
- compliance-триггеры (L293);
- границы Product Layer и Commercial Layer (L294).

Процессы 3, 5, 7, 8 и 9 обслуживаются только «чужими» промптами, у которых эти
процессы стоят во вторичном маршруте. Для процесса 7 есть только архив.

### 3.4. Происхождение дефектов шаблонов

Скрипт provenance взял из реестров инцидентов RUN-0073…RUN-0077 все строки с
происхождением `prompt` (дефект шаблона БА) и поискал цитату шаблона дословно в
текстах `prompts/`. Результат:

| Прогон | Инцидентов `prompt` | Совпали с `prompts/` | Чем объясняется |
| --- | --- | --- | --- |
| RUN-0073 | 18 | 0 | Шаблон «бизнес-аналитик (CBAP) и API-архитектор» ([L62](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/runs/2026/RUN-0073/outputs/incident-register.md?plain=1#L62)) в каталоге отсутствует. |
| RUN-0074 | 3 | 3 | I-001…I-003 ([L68–L70](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/runs/2026/RUN-0074/outputs/incident-register.md?plain=1#L68)) |
| RUN-0075 | 7 | 7 | I-001…I-005 ([L58–L62](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/runs/2026/RUN-0075/outputs/incident-register.md?plain=1#L58)), I-113, I-114 ([L170–L171](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/runs/2026/RUN-0075/outputs/incident-register.md?plain=1#L170)) |
| RUN-0076 | 8 | 8 | I-001…I-008 ([L64–L71](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/runs/2026/RUN-0076/outputs/incident-register.md?plain=1#L64)) |
| RUN-0077 | 0 | 0 | Реестра инцидентов нет. |
| **Итого** | **36** | **18** | |

Из 18 совпавших инцидентов 16 пришлись на glossary-stepwise, 4 — на
fr-documentation-stepwise. Цитата о TM Forum есть в обоих файлах. В метаданных
прогонов путь `prompts/` не указан, но текст шаблонов совпадает дословно. Значит,
БА вставлял эти файлы в чат вручную. Ещё 31 строка реестра RUN-0076 относится к
дефектам в промптах, которые модель сама написала в диалоге (сессии 9–16). Эти
строки к `prompts/` не относятся.

Ключевые цитаты БА в ответ на текст шаблонов:

| Что в шаблоне | Строка в `prompts/` | Реакция БА (реплика, реестр, экспорт) |
| --- | --- | --- |
| Роль «CBAP … методологиях TM Forum (eTOM/ODA)» | [glossary L10–L11](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/glossary-context-understanding-stepwise.md?plain=1#L10) | RUN-0074 р. 80: «нет доступа к архитектуре ПО, мы не може м придумыватит» ([L68](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/runs/2026/RUN-0074/outputs/incident-register.md?plain=1#L68), [экспорт](https://github.com/user-attachments/files/33668084/chat-export-1106.json)). RUN-0075 р. 26: «мы не можем диктовать заказчику его бизнес-процессы» ([L58](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/runs/2026/RUN-0075/outputs/incident-register.md?plain=1#L58), [экспорт](https://github.com/user-attachments/files/33669481/chat-export-1104.json)). |
| «Категорический запрет на формулировки «Система должна»» | [glossary L15](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/glossary-context-understanding-stepwise.md?plain=1#L15) | RUN-0074 р. 52: «полная хрень» ([L69](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/runs/2026/RUN-0074/outputs/incident-register.md?plain=1#L69)). RUN-0076 р. 10: «1. да», то есть запрет снят ([L65](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/runs/2026/RUN-0076/outputs/incident-register.md?plain=1#L65), [экспорт](https://github.com/user-attachments/files/33669255/chat-export-1110.json)). |
| «2.3. Задачи» | [glossary L50](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/glossary-context-understanding-stepwise.md?plain=1#L50) | RUN-0076 р. 10: «1-4 - да, 5 будет НФТ (обычно пустой), 6 - ограничения» ([L66](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/runs/2026/RUN-0076/outputs/incident-register.md?plain=1#L66)). |
| «Укажи бизнес-последствия проблемы» | [glossary L48](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/glossary-context-understanding-stepwise.md?plain=1#L48) | RUN-0076 р. 12: «Не придумывать риски, если они явно не заданы заказчиком» ([L67](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/runs/2026/RUN-0076/outputs/incident-register.md?plain=1#L67)). |
| «Безопасная работа с документацией (PDF/ссылки)» — правила «не придумывать» нет | [glossary L23](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/glossary-context-understanding-stepwise.md?plain=1#L23) | RUN-0075 р. 8: «Помним, придумывать и додумывать нельзя, текущий функционал - только строго по документации» ([L62](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/runs/2026/RUN-0075/outputs/incident-register.md?plain=1#L62)). |
| «Контекст валиден и готов к формированию Раздела 4» | [glossary L64](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/glossary-context-understanding-stepwise.md?plain=1#L64) | Инцидент зафиксирован при разборе: RUN-0074 I-003 ([L70](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/runs/2026/RUN-0074/outputs/incident-register.md?plain=1#L70)), RUN-0076 I-007 ([L70](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/runs/2026/RUN-0076/outputs/incident-register.md?plain=1#L70)). Затем модель объявила «Разделы 1, 2, 4 и 6 сформированы и проверены» (RUN-0075 I-150, р. 94, [L207](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/runs/2026/RUN-0075/outputs/incident-register.md?plain=1#L207)). |
| «ШАГ 4. Валидация через ODA Capability Map» | [fr-documentation L56](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/fr-documentation-stepwise.md?plain=1#L56) | RUN-0075 I-114 ([L171](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/runs/2026/RUN-0075/outputs/incident-register.md?plain=1#L171)). |
| Раздел 7 жёстко связан с 4.x | [technical-details L17](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/technical-details-solution-design-stepwise.md?plain=1#L17) | RUN-0073 р. 8: «пункт в разделе 7 предусмотреть» ([L78](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/runs/2026/RUN-0073/outputs/incident-register.md?plain=1#L78), [экспорт](https://github.com/user-attachments/files/33662573/chat-export-1123.json)). Шаблон RUN-0073 не из `prompts/`, но реплика показывает: раздел 7 нужен как заметки по запросу БА, а не как зеркало 4.x. |

### 3.5. Антипаттерны

| № | Антипаттерн | Где | Доказательство |
| --- | --- | --- | --- |
| АП1 | Роль задана через методологию или сертификат (CBAP, TM Forum, ODA, ITIL, «cisco») | 20 из 27 активных файлов (R) | Модель начинает «диктовать» процессы и архитектуру (§3.4). Правило П1 анализа 2026-10-20 ([L781](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/docs/analysis/2026-10-20-bcreq-fr-section-prompts.md?plain=1#L781)) запрещает называть методологии в роли. |
| АП2 | Модель сама сертифицирует результат: ✅, «Отчет валидации», «Контекст валиден», «Dev Readiness» | 8 файлов (C) | Нарушает правило B3. В RUN-0076 модель выдала «Отчет валидации (Эксперт-Архитектор)» (I-150, [L213](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/runs/2026/RUN-0076/outputs/incident-register.md?plain=1#L213)). Анализ 2026-10-20 запрещает самооценку правилом О13 ([L532](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/docs/analysis/2026-10-20-bcreq-fr-section-prompts.md?plain=1#L532)), вводит блок «Проверка решений» с источниками (О14, [L533](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/docs/analysis/2026-10-20-bcreq-fr-section-prompts.md?plain=1#L533)) и проверкой второй ролью. |
| АП3 | Старая модель разделов: ФТ = 4, «2.3 Задачи», 7.x ↔ 4.x | 11 файлов (S), включая README.executable | §3.1. RUN-0073 р. 76: «Вообще по правилам раздел 4 - Функциональный дизайн решения» ([L62](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/runs/2026/RUN-0073/outputs/incident-register.md?plain=1#L62)). |
| АП4 | «Креативная» генерация: майнинг ограничений, новые термины, сценарии | 3 файла (К) | RUN-0074 SC-10, р. 62: доработки не додумываются ([L33](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/runs/2026/RUN-0074/outputs/success-criteria.md?plain=1#L33)). |
| АП5 | Варианты одной операции по режимам (stepwise/oneshot/legacy) расходятся по содержанию | 9 групп (§2.3) | Исправление в одном варианте не доходит до других. Метка `legacy` значит то «старая версия» (17, 25, 28), то «единственная» (22). |
| АП6 | Нет формата вывода | 15 из 25 файлов-промптов | §2.2. Для BCREQ-ФТ формат ответа задан общей частью анализа ([§5.0, L503](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/docs/analysis/2026-10-20-bcreq-fr-section-prompts.md?plain=1#L503)). |
| АП7 | Английские метки (Job Story, INVEST, Normalized Terms) в русскоязычном артефакте; Job Story названа User Story | 7 файлов (E) | [us-modeling-stepwise L36–L37](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/us-modeling-stepwise.md?plain=1#L36) |
| АП8 | Служебные промпты лежат вместе с БА-операциями; frontmatter неоднороден | 1, 27; README с `ai-generated: true` | Handover вне карты процессов и без `id`/`title`. Для документов класса Analysis [analysis-standard](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/standards/analysis-standard.md?plain=1#L155) запрещает `ai-generated`. |
| АП9 | Нет правила локатора и сноски на источник | все файлы темы А | Правило О1 ([L520](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/docs/analysis/2026-10-20-bcreq-fr-section-prompts.md?plain=1#L520)). RUN-0074 SC-02, р. 16 ([L25](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/runs/2026/RUN-0074/outputs/success-criteria.md?plain=1#L25)); RUN-0075 SC-03, р. 42: цитата и источник ([L26](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/runs/2026/RUN-0075/outputs/success-criteria.md?plain=1#L26)). |

### 3.6. Удачные решения, которые можно переиспользовать

| № | Решение | Где | Подтверждение в чатах и стандартах |
| --- | --- | --- | --- |
| У1 | Шаг 0: сбор As-Is до генерации, дайджест длинного документа | [glossary L24–L31](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/glossary-context-understanding-stepwise.md?plain=1#L24) | RUN-0074 SC-04, р. 42: «Значит нужен гейт рераг» ([L27](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/runs/2026/RUN-0074/outputs/success-criteria.md?plain=1#L27)). RUN-0076 SC-58, р. 128: не продолжать, пока источник не прочитан ([L106](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/runs/2026/RUN-0076/outputs/success-criteria.md?plain=1#L106)). Шаг 0 есть в промпте а) ([L584](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/docs/analysis/2026-10-20-bcreq-fr-section-prompts.md?plain=1#L584)). |
| У2 | Пошаговая генерация со стоп-гейтами и ожиданием ответа | 10 файлов (G), например [glossary L44](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/glossary-context-understanding-stepwise.md?plain=1#L44) | RUN-0076 SC-54, р. 122: «сначала раздел 1, после соглаосвания, расздел 2 и так далее» ([L104](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/runs/2026/RUN-0076/outputs/success-criteria.md?plain=1#L104)). |
| У3 | Защита глоссария: базовые термины пользователя приоритетны | [glossary L20](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/glossary-context-understanding-stepwise.md?plain=1#L20) | RUN-0076 SC-07, р. 12 ([L26](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/runs/2026/RUN-0076/outputs/success-criteria.md?plain=1#L26)). |
| У4 | Плейсхолдер `[ТРЕБУЕТСЯ УТОЧНЕНИЕ…]` вместо выдумки | [technical-details L25](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/technical-details-solution-design-stepwise.md?plain=1#L25), [oneshot L21](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/technical-details-solution-design-oneshot.md?plain=1#L21) | RUN-0074 SC-10 ([L33](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/runs/2026/RUN-0074/outputs/success-criteria.md?plain=1#L33)); правило О1 анализа: без локатора утверждение уходит в «Вопросы» ([L520](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/docs/analysis/2026-10-20-bcreq-fr-section-prompts.md?plain=1#L520)). |
| У5 | Поле статуса `ready \| draft \| needs-clarification` | 9 файлов (F), например [uc-modeling-oneshot L24](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/uc-modeling-oneshot.md?plain=1#L24) | Совпадает со словарём правила B4 ([L94](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/standards/bcreq-process-standard.md?plain=1#L94)). |
| У6 | Декомпозиция «Заявленное решение vs Заявленная боль», 5 Whys, проверка существующих решений | [questions-stepwise L24, L49, L60](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/questions-customer-understanding-stepwise.md?plain=1#L24) | Используется в 5 прогонах (§2.1, № 26). |
| У7 | Механика ASR: блоки по ~5000 знаков, словарь подтверждённых замен, подтверждение перед следующим блоком | [asr-legacy L13, L41, L66, L141](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/asr-ingestion-legacy.md?plain=1#L13) | Единственная в каталоге механика накопления подтверждённых решений между шагами. |
| У8 | Правила «не выдумывай», «Не определено» | 14 файлов (Н), например [session-debug L31](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/session-debug-documentation-oneshot.md?plain=1#L31) | Там, где правила не было (glossary-stepwise), БА добавлял его вручную (RUN-0075 р. 8). |
| У9 | Навигация: карта процессов, README в два слоя, фиксация прогонов | [00-index](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/docs/ba-processes/00-index.md?plain=1#L54), [README.executable](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/README.executable.md?plain=1#L33) | Каждый промпт связан с процессом, и у 21 из 34 файлов есть прогоны: это позволило сделать атрибуцию в §3.4. |
| У10 | Структура аудита «пункт → проблема → вариант» | [fr-validation-stepwise](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/fr-validation-stepwise.md) | Используется в 8 прогонах. |

### 3.7. Структура 2.1–2.14: BLOCKED

Матрица оставлена пустой. Заполнять её по догадкам нельзя: формулировки пунктов
известны только из экспорта чата за 21–23.10.2026, а его нет (главный риск 1).

| Пункт | Формулировка (URL экспорта, реплика) | Покрытие в `prompts/` (№) | Разрыв | Тип разрыва |
| --- | --- | --- | --- | --- |
| 2.1 … 2.14 | не доступна | — | — | — |

Как заполнить матрицу, когда экспорт будет приложен:

1. Выделить реплики с метками 2.1–2.14 за 21–23.10.2026.
2. Для каждого пункта найти номера файлов из §2.1 и сравнить с §3.1–§3.3.
3. Пометить тип разрыва: дубль, пропущенный этап или устаревший подход.
4. Проверить пункты на противоречие с правилами B1–B7 и с разделами 1–7
   BCREQ-ФТ. При противоречии вынести его в главный риск.

### 3.8. Альтернативный вектор для Задачи 2

1. Взять за основу уже согласованные элементы:
   - конвейер П1–П6 с гейтами G1–G3;
   - механизм `needs-clarification` (правила B4–B7);
   - разделы 1–7 BCREQ-ФТ и правила О/А/Б/В/П анализа 2026-10-20.
2. Новые промпты разделов а)/б)/в) и проверку второй ролью оформить как новые
   файлы каталога. Файлы со статусом «удалить» перевести в legacy или архив
   одновременно, чтобы ссылки прогонов не сломались.
3. Пробелы П2/G1 (дерево BCREQ), П5 (риски) и П6/G3 (baselining) и 11 known gaps
   ставить отдельными задачами, а не встраивать в существующие файлы.
4. Структуру 2.1–2.14 применять как чек-лист полноты (§3.7). Если она
   противоречит правилу B3 или разделам 1–7, это решение Пользователя, а не
   исполнителя.

Ограничение: новые промпты анализа 2026-10-20 сами ещё не проверены прогоном
модели ([§7, L864](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/docs/analysis/2026-10-20-bcreq-fr-section-prompts.md?plain=1#L864)).

## 4. Recommendations

Рекомендации **не обязательны к применению** (см. §1): это входные данные для
Задачи 2. Номера даны по §2.1.

**Удалить из активного набора (12):**

- **4 `archive/.gitkeep`** — удалить физически: файл избыточен.
- **20, 21 (glossary), 15, 16 (fr-documentation), 13, 14 (constraints), 29
  (technical-details-oneshot)** — сделать legacy, когда в каталоге появятся промпты
  а)/б)/в). Их функцию закрывают новые промпты (§3.1). Два из этих файлов —
  дословный источник 18 инцидентов (§3.4).
- **18 (fr-validation-oneshot)** — сделать legacy. Его заменяет проверка второй
  ролью ([§5.4](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/docs/analysis/2026-10-20-bcreq-fr-section-prompts.md?plain=1#L746)).
- **17, 25, 28 (fr-validation-legacy, questions-legacy, technical-details-legacy)**
  — перенести в архив. У каждого есть более новый вариант. Файлы 17 и 25 упомянуты
  в прогонах, поэтому их нужно сохранить, а не стирать.

**Доработать (11):**

- **19 fr-validation-stepwise** — убрать привязку к 4.x и правило «сформулируй
  требование на основе контекста». Сохранить структуру «пункт → проблема →
  вариант».
- **30 technical-details-stepwise** — заменить связь 7.x ↔ 4.x на заметки к
  разделу 3 по запросу БА (П3, О11). Убрать роль CBAP/TM Forum и Dev Readiness
  Check.
- **26 questions-stepwise** — встроить в реестр вопросов раздела 7 и в правило
  B4: owner и ссылка на `customer-questions`. Убрать роль CBAP и английские
  метки.
- **31–34 uc/us-modeling** — убрать роль CBAP и самооценку ✅. Развести Job
  Story и User Story. Связать статус с правилами B4–B7.
- **22 letter** — снять метку `legacy`, добавить явный формат вывода и правило
  «не выдумывай».
- **1 handover** — привести frontmatter к остальным промптам (`id`/`title`) или
  вынести из каталога БА-промптов. Убрать дубль функции session-debug.
- **2, 3 README** — обновить маршрутизацию под разделы BCREQ-ФТ после Задачи 2.
  Убрать `ai-generated`.

**Оставить (9):**

- **5–10 архив** — оставить: на них ссылаются RUN-0001…RUN-0003.
- **23, 24 meeting** — оставить как есть. Объединять ли их в один файл с
  параметром аудитории — решение Задачи 2.
- **27 session-debug** — оставить. Роль CBAP избыточна, но на работу не влияет.

**Промпт для расшифровки (2):**

- **11, 12 asr-ingestion** — сохранить как отдельный вход П1. Механика словаря и
  подтверждений из файла 11 — донор (У7). Формат вывода — из файла 12.

**Перед Задачей 2:** приложить экспорт чата за 21–23.10.2026 и заполнить
матрицу §3.7.

## 5. Related Artifacts

- Issue: [#384](https://github.com/G-Ivan-A/mango_ba_prompts/issues/384); PR:
  [#385](https://github.com/G-Ivan-A/mango_ba_prompts/pull/385).
- Предварительный анализ: [2026-10-20-bcreq-fr-section-prompts.md](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/docs/analysis/2026-10-20-bcreq-fr-section-prompts.md).
- Стандарты:
  - [bcreq-process-standard.md](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/standards/bcreq-process-standard.md);
  - [analysis-standard.md](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/standards/analysis-standard.md);
  - [prompt-standard.md](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/standards/prompt-standard.md).
- Карта процессов: [00-index.md](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/docs/ba-processes/00-index.md).
- Evidence этого аудита:
  - [issue_384_prompts_inventory.py](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384_prompts_inventory.py);
  - [inventory.json](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/inventory.json);
  - [issue_384_prompt_provenance.py](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384_prompt_provenance.py);
  - [prompt-provenance.json](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/prompt-provenance.json);
  - валидатор [validate_issue_384_prompts_audit.py](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/scripts/validate_issue_384_prompts_audit.py).
- Реестры чатов:
  - RUN-0073: [инциденты](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/runs/2026/RUN-0073/outputs/incident-register.md), [критерии успеха](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/runs/2026/RUN-0073/outputs/success-criteria.md);
  - RUN-0074: [инциденты](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/runs/2026/RUN-0074/outputs/incident-register.md), [критерии успеха](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/runs/2026/RUN-0074/outputs/success-criteria.md);
  - RUN-0075: [инциденты](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/runs/2026/RUN-0075/outputs/incident-register.md), [критерии успеха](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/runs/2026/RUN-0075/outputs/success-criteria.md);
  - RUN-0076: [инциденты](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/runs/2026/RUN-0076/outputs/incident-register.md), [критерии успеха](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/runs/2026/RUN-0076/outputs/success-criteria.md).
