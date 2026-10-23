---
status: draft
version: 0.2
updated: 2026-10-23
temperature: 0.1
analysis-subtype: inventory
source: "https://github.com/G-Ivan-A/mango_ba_prompts/issues/384"
scope: repo
based_on: "prompts/ @ dbf1d3c5, экспорт чата «Проект: СПЛИТ (БА)» за 21–23.10.2026 (р. 744–779, SHA-256 a6a75cfe), docs/analysis/2026-10-20-bcreq-fr-section-prompts.md, standards/bcreq-process-standard.md, docs/ba-processes/00-index.md, runs/2026/RUN-0073, runs/2026/RUN-0074, runs/2026/RUN-0075, runs/2026/RUN-0076"
related_artifacts:
  - "experiments/issue_384_prompts_inventory.py"
  - "experiments/issue_384/inventory.json"
  - "experiments/issue_384_prompt_provenance.py"
  - "experiments/issue_384/prompt-provenance.json"
  - "experiments/issue_384/chat-2026-10-22-23-register.md"
  - "experiments/issue_384_verify_chat_quotes.py"
  - "experiments/issue_384/chat-quote-check.json"
  - "experiments/issue_384_chat_window_dump.py"
  - "scripts/validate_issue_384_prompts_audit.py"
  - "docs/analysis/2026-10-20-bcreq-fr-section-prompts.md"
---

# Аудит каталога `prompts/`: инвентаризация и расхождения с целевой структурой BCREQ

## Summary / BLUF

Каталог [`prompts/`](https://github.com/G-Ivan-A/mango_ba_prompts/tree/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts) на снимке `dbf1d3c5` содержит 34 файла. По статусу
аудита: **оставить — 9**, **доработать — 11**, **удалить — 12**, **промпт для
расшифровки — 2**. «Удалить» и «доработать» читаются как «кандидат на удаление» и
«кандидат на доработку» [р. 779, Ч-61](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L94): решение принимает Пользователь. «Удалить» означает
вывод из активного набора: файл становится legacy или переходит в архив, когда
появится замена. Физически удалить предлагается только избыточный
`archive/.gitkeep`.

Версия 0.2 учитывает контекст чата «Проект: СПЛИТ (БА)» за 21–23.10.2026
([экспорт](https://github.com/user-attachments/files/33873099/chat-export-.json),
36 реплик р. 744–779; 21.10 реплик нет). Он изменил три вывода версии 0.1:

1. **Структура 2.1–2.14 найдена и сопоставлена с каталогом (§3.7).** Пункты
   2.1–2.13 БА перечислил в р. 752 [р. 752, Ч-20](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L53), пункт 2.14 предложила модель в р. 753
   [р. 753, Ч-37](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L70), состав закреплён в плане р. 763 [р. 763, Ч-46](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L79). По решению БА это предложение,
   а не жёсткий стандарт [р. 778, Ч-59](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L92). В аудите структура только информационная [р. 778, Ч-60](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L93),
   жёстко маппить на неё файлы нельзя [р. 779, Ч-62](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L95). Поэтому §3.7 содержит
   информационную матрицу и 12 наблюдений для Задачи 2, а статусы файлов от
   пунктов 2.x не зависят.
2. **Промпты а)/б)/в) анализа 2026-10-20 перестали быть эталоном.** БА назвал их
   неполными и построенными только на статистике прогонов [р. 750, Ч-08](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L41) и согласился, что
   их надо дорабатывать [р. 752, Ч-19](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L52). Статус «удалить» теперь обоснован критерием БА
   «конкурирующие с новыми или с процессом BCREQ» [р. 752, Ч-34](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L67), а не заменой промптами
   а)/б)/в).
3. **Целевая модель документа — восемь разделов, а не семь.** 3 — ФТ, 4 — НФТ,
   5 — описание разрабатываемого решения (ОРР: ФДТ и ТС), 6 — особенности
   разработки и ограничения, 7 — UC и матрица покрытия (внутренний), 8 —
   дополнительные разделы [р. 752, Ч-11](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L44), [р. 752, Ч-12](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L45), [р. 752, Ч-13](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L46), [р. 752, Ч-14](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L47), [р. 752, Ч-15](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L48), [р. 752, Ч-16](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L49). Разделы
   1–6 БА пересматривать не предлагает [р. 766, Ч-64](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L97).

Главный проверенный вывод по каталогу не изменился. Активные промпты
формирования документа реализуют **старую модель «ТЗ»**. В ней ФТ — это раздел 4,
пункт 2.3 — «Задачи», раздел 7 детализирует пункты 4.x, роль задана через
CBAP/TM Forum, а модель сама объявляет контекст валидным. В чатах прогонов
RUN-0074…RUN-0076 это зафиксировано как дефекты. **18 инцидентов** с
происхождением `prompt` дословно совпадают с текстом двух файлов каталога:
[`glossary-context-understanding-stepwise.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/glossary-context-understanding-stepwise.md)
(16) и [`fr-documentation-stepwise.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/fr-documentation-stepwise.md) (4). Часть
инцидентов совпадает с обоими файлами.

> **Главный риск 1 — старая модель каталога несовместима с восемью разделами и
> структурой 2.1–2.14.** В каталоге ФТ — раздел 4, а раздел 7 — заметки к 4.x. В
> новой структуре раздел 4 — НФТ [р. 752, Ч-12](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L45), решение описывает раздел 5 [р. 752, Ч-13](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L46), а
> раздел 7 — внутренние UC [р. 752, Ч-15](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L48). Ни один файл темы А нельзя «переименовать» в
> пункт 2.x. Если строить промпты 2.x поверх этих файлов, вместе с ними переедут
> дефекты, которые БА уже отклонил в трёх чатах (§3.4). Процессу BCREQ структура
> 2.1–2.14 принципиально не противоречит: она повторяет конвейер разделов и
> точку согласования 1 [р. 752, Ч-10](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L43). Но в ней есть логические дыры (§3.7.3). Главная —
> нумерация разделов в самом чате неустойчива. Раздел 4 назван то
> «Функциональным дизайном» [р. 746, Ч-02](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L35), то НФТ [р. 752, Ч-12](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L45). Через сутки модель отнесла НФТ
> к разделу 5 [р. 765, Ч-52](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L85), а раздел 4 назвала «Дизайном» [р. 765, Ч-68](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L101).
>
> **Главный риск 2 — нет проверенного эталона.** Промпты а)/б)/в) БА как эталон
> отклонил [р. 750, Ч-08](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L41), [р. 765, Ч-53](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L86). Промпты 2.x появятся только в Задаче 3, в отдельном
> подкаталоге [р. 767, Ч-65](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L98). До этого у кандидатов на удаление нет замены, и выводить их
> из набора раньше нельзя. Удаление устаревших промптов план чата и так отводит в
> бэклог [р. 767, Ч-66](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L99). **Вектор для Задачи 2** описан в §3.8: промпты 2.x писать заново,
> текущие файлы считать донорами отдельных механик (§3.6), а не основой.

## 1. Context / Scope

- **Предмет учёта:** все файлы каталога `prompts/`, включая `prompts/archive/`,
  README и служебные промпты.
- **Снимок:** коммит
  [`dbf1d3c5`](https://github.com/G-Ivan-A/mango_ba_prompts/tree/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d)
  (`main` на 2026-10-23). Все ссылки на файлы закреплены за этим коммитом, поэтому
  номера строк не «уедут». Аудит только читал файлы: в `prompts/` ничего не
  изменено, не удалено и не перемещено.
- **Дата и автор:** 2026-10-23, исполнитель issue #384 (режим Hybrid [р. 776, Ч-58](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L91)).
  Решения по статусам принимает Пользователь. Версия 0.2 — по
  [комментарию Пользователя к PR #385](https://github.com/G-Ivan-A/mango_ba_prompts/pull/385#issuecomment-6365671972):
  применить к аудиту контекст чата за 21–23.10.2026.
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
  - журналы чатов — реестры инцидентов и критериев успеха RUN-0073…RUN-0076;
  - контекст чата за 21–23.10.2026 (структура 2.1–2.14, восемь разделов, план
    задач) — [реестр дословных цитат](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md)
    Ч-01…Ч-70. Скрипт
    [`issue_384_verify_chat_quotes.py`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384_verify_chat_quotes.py)
    сверяет каждую цитату, роль и время с репликой экспорта и SHA-256 экспорта с
    провенансом реестра. Итог в
    [`chat-quote-check.json`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-quote-check.json):
    70 из 70 цитат найдены в заявленных репликах окна. Сам экспорт в репозиторий
    не попадает (правило #309).
- **Как ссылаться на сообщения чатов.** Экспорты чатов — JSON-вложения GitHub, у
  отдельных сообщений нет своих URL. Поэтому сообщение адресуется тремя
  элементами: URL экспорта, номер реплики («р. N» — сквозной номер сообщения в
  линейной ветке экспорта) и абсолютная ссылка на строку реестра. В строке
  реестра реплика процитирована дословно. Для чата 21–23.10.2026 ссылка вида
  [р. 752, Ч-20](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L53) ведёт на строку реестра цитат; URL экспорта — в таблице ниже.

  | Прогон / чат | Экспорт чата | Окно, UTC | Реплик |
  | --- | --- | --- | --- |
  | Чат «Проект: СПЛИТ (БА)», 21–23.10.2026 | [chat-export-промптба.json](https://github.com/user-attachments/files/33873099/chat-export-.json) | 2026-10-22 — 2026-10-23 | 36 (р. 744–779) |
  | RUN-0073 | [chat-export-1123.json](https://github.com/user-attachments/files/33662573/chat-export-1123.json) | 2026-10-16 — 2026-10-19 | 106 |
  | RUN-0074 | [chat-export-1106.json](https://github.com/user-attachments/files/33668084/chat-export-1106.json) | 2026-09-15 — 2026-10-01 | 214 |
  | RUN-0075 | [chat-export-1104.json](https://github.com/user-attachments/files/33669481/chat-export-1104.json) | 2026-09-16 — 2026-09-28 | 118 |
  | RUN-0076 | [chat-export-1110.json](https://github.com/user-attachments/files/33669255/chat-export-1110.json) | 2026-10-01 — 2026-10-13 | 156 |

- **Критерии статуса аудита:**

  | Статус | Критерий |
  | --- | --- |
  | оставить | Файл исправно выполняет свою функцию, и восемь разделов BCREQ со структурой 2.1–2.14 его не заменяют. Либо это архив, на который ссылаются зафиксированные прогоны. |
  | доработать | «Кандидат на доработку» [р. 779, Ч-61](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L94). Функция нужна в процессе BCREQ или вне его, и с процессом файл не конкурирует. При этом в тексте есть дефекты, подтверждённые чатами или стандартом. |
  | удалить | «Кандидат на удаление» [р. 779, Ч-61](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L94). Файл конкурирует с процессом BCREQ или с будущими промптами 2.x [р. 752, Ч-34](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L67): реализует старую модель разделов «ТЗ» или самопроверку, которую процесс выносит в отдельный вызов. Либо файл дублирует более новый вариант. Либо файл избыточен (`.gitkeep`). Удалить — значит вывести из активного набора, сделать legacy или перенести в архив, когда появится замена. |
  | промпт для расшифровки | Обработка расшифровки ASR — отдельный вход конвейера П1. Решение БА: оставить [р. 752, Ч-33](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L66). |

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
- **Структура 2.1–2.14 в аудите.** Это предложение БА, которое Задача 2
  подтвердит или заменит [р. 778, Ч-59](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L92), [р. 778, Ч-60](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L93). Поэтому аудит не маппит файлы на пункты
  [р. 779, Ч-62](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L95). Статусы опираются на критерии БА [р. 752, Ч-33](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L66), [р. 752, Ч-34](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L67) и на дефекты,
  подтверждённые чатами (§3.4). Номер близкого пункта 2.x в обосновании §2.1 —
  информационный: он показывает, с каким будущим промптом файл конкурирует.
  Расхождения со структурой зафиксированы как наблюдения [р. 779, Ч-63](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L96) (§3.7.3).
- **Вне охвата:** финальный стандарт структуры промптов, подтверждение или
  альтернативы для 2.1–2.14 (Задача 2 [р. 767, Ч-57](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L90)). Также вне охвата реплики чата за
  пределами окна 21–23.10.2026 и содержимое экспортов, вложенных в реплики окна:
  они перечислены в провенансе реестра, но не разбирались.

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
| 13 | [constraints-documentation-oneshot.md](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/constraints-documentation-oneshot.md) | А | 1, 9 | draft / 0.1 | 0007 | R | удалить | Конкурирует с пунктом 2.8 (раздел 6 к разделу 5) [р. 752, Ч-27](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L60). Требует 4–6 «сгенерированных» ограничений ([L31](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/constraints-documentation-oneshot.md?plain=1#L31)). |
| 14 | [constraints-documentation-stepwise.md](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/constraints-documentation-stepwise.md) | А | 1, 2, 9 | draft / 0.1 | 0007, 0010, 0012, 0013, 0016 | R S К G | удалить | Конкурирует с 2.8 [р. 752, Ч-27](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L60): вход — «Раздел 4 (ФТ)» ([L32](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/constraints-documentation-stepwise.md?plain=1#L32)), а не раздел 5; «Майнинг ограничений (Креативный анализ границ)» ([L39](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/constraints-documentation-stepwise.md?plain=1#L39)). |
| 15 | [fr-documentation-oneshot.md](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/fr-documentation-oneshot.md) | А | 1 | draft / 0.1 | 0026 | R S C | удалить | Конкурирует с 2.3 (раздел 3 ФТ) [р. 752, Ч-22](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L55). Генерирует «Раздел 4» ([L10](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/fr-documentation-oneshot.md?plain=1#L10)) и «Отчет валидации» по ODA ([L30](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/fr-documentation-oneshot.md?plain=1#L30)). |
| 16 | [fr-documentation-stepwise.md](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/fr-documentation-stepwise.md) | А | 1, 2, 4, 9 | draft / 0.1 | 0006, 0007, 0010, 0012, 0013, 0016, 0017, 0026 | R S К G | удалить | Конкурирует с 2.3 [р. 752, Ч-22](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L55): ФТ как «Раздел 4». Дословный источник 4 инцидентов RUN-0074/0075 (§3.4). |
| 17 | [fr-validation-legacy.md](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/fr-validation-legacy.md) | Б | 1, 2, 3 | draft / 1.0 | 0023, 0028 | R | удалить | Дубль fr-validation-stepwise: TM Forum Frameworx/ITIL ([L16](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/fr-validation-legacy.md?plain=1#L16)), «сертифицированные бизнес-аналитики (cisco)» ([L18](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/fr-validation-legacy.md?plain=1#L18)), температура задана в тексте ([L29](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/fr-validation-legacy.md?plain=1#L29)). Перенести в архив: на него ссылаются прогоны. |
| 18 | [fr-validation-oneshot.md](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/fr-validation-oneshot.md) | Б | 1, 2, 3, 8, 9 | draft / 0.1 | 0006 | R S | удалить | Экспресс-аудит по старой нумерации 4.x конкурирует с процессом BCREQ [р. 752, Ч-34](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L67): проверку процесс выносит в отдельный вызов второй ролью (§5.4 анализа 2026-10-20, правило B3). Пункта проверки в 2.1–2.14 нет (§3.7.3, Н8). |
| 19 | [fr-validation-stepwise.md](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/fr-validation-stepwise.md) | Б | 1, 2, 3, 4, 8, 9 | draft / 0.1 | 0013, 0015, 0018, 0021, 0022, 0023, 0025, 0027 | R S G | доработать | Ценная структура аудита «пункт → проблема → вариант». Но она привязана к 4.x, и встретив `...`, модель сама «формулирует требование на основе контекста» ([L25](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/fr-validation-stepwise.md?plain=1#L25)). |
| 20 | [glossary-context-understanding-oneshot.md](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/glossary-context-understanding-oneshot.md) | А | 1, 3, 4 | draft / 0.1 | — | Б S Н | удалить | Конкурирует с 2.1 (разделы 1, 2) [р. 752, Ч-20](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L53). «Задачи: 3–5 пунктов» ([L31](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/glossary-context-understanding-oneshot.md?plain=1#L31)) вместо «Границ». |
| 21 | [glossary-context-understanding-stepwise.md](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/glossary-context-understanding-stepwise.md) | А | 1, 3, 4, 9 | draft / 0.1 | 0007, 0010, 0011, 0012, 0013, 0014, 0017, 0020, 0021, 0025, 0027 | R Б S К C G | удалить | Конкурирует с 2.1 [р. 752, Ч-20](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L53). Дословный источник 16 инцидентов RUN-0074…0076 (§3.4). Механики-доноры перечислены в §3.6. |
| 22 | [letter-customer-documentation-legacy.md](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/letter-customer-documentation-legacy.md) | В | 6 | draft / 1.0 | — | — | доработать | Единственный промпт письма, поэтому метка режима `legacy` вводит в заблуждение. Формат вывода дан простым текстом ([L35](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/letter-customer-documentation-legacy.md?plain=1#L35)). Прогонов нет. |
| 23 | [meeting-customer-documentation-stepwise.md](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/meeting-customer-documentation-stepwise.md) | В | 6 | draft / 0.1 | 0013 | R E Н F G | оставить | Процесс 6 структура 2.1–2.14 не заменяет. Стоп-гейты ([L20](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/meeting-customer-documentation-stepwise.md?plain=1#L20)), поле статуса ([L46](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/meeting-customer-documentation-stepwise.md?plain=1#L46)). Роль CBAP ([L11](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/meeting-customer-documentation-stepwise.md?plain=1#L11)) — косметика. |
| 24 | [meeting-team-documentation-stepwise.md](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/meeting-team-documentation-stepwise.md) | В | 6 | draft / 0.1 | — | R E Н F G | оставить | Почти дубль № 23: тот же скелет из шагов 1–4. Отличается блоком «Оценка и зависимости» ([L40](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/meeting-team-documentation-stepwise.md?plain=1#L40)) и «Не определено» ([L66](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/meeting-team-documentation-stepwise.md?plain=1#L66)). Прогонов нет. |
| 25 | [questions-customer-understanding-legacy.md](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/questions-customer-understanding-legacy.md) | В | 1, 3, 6 | draft / 1.0 | 0024 | R C Н | удалить | Заменён stepwise-версией. «Команда сертифицированных» ([L11](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/questions-customer-understanding-legacy.md?plain=1#L11)), чек-лист ✅ ([L50](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/questions-customer-understanding-legacy.md?plain=1#L50)). Перенести в архив: на него ссылается RUN-0024. |
| 26 | [questions-customer-understanding-stepwise.md](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/questions-customer-understanding-stepwise.md) | В | 1, 3, 6, 9 | draft / 0.1 | 0011, 0012, 0013, 0019, 0024 | R E Н F G | доработать | Сильный донор: «Заявленное решение vs Заявленная боль» ([L24](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/questions-customer-understanding-stepwise.md?plain=1#L24)), 5 Whys ([L49](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/questions-customer-understanding-stepwise.md?plain=1#L49)), проверка существующих решений ([L60](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/questions-customer-understanding-stepwise.md?plain=1#L60)), «⚠️ Требует проверки у ПО» ([L27](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/questions-customer-understanding-stepwise.md?plain=1#L27)). Места для реестра вопросов в восьми разделах нет (§3.7.3, Н10). |
| 27 | [session-debug-documentation-oneshot.md](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/session-debug-documentation-oneshot.md) | Е | 6 | draft / 0.2 | 0006 | R Н F | оставить | Работает (RUN-0006). Правило «Не выдумывай» ([L31](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/session-debug-documentation-oneshot.md?plain=1#L31)). Роль CBAP ([L11](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/session-debug-documentation-oneshot.md?plain=1#L11)) не нужна служебному промпту. |
| 28 | [technical-details-solution-design-legacy.md](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/technical-details-solution-design-legacy.md) | А | 1 | draft / 1.0 | — | R S | удалить | Дубль stepwise-версии. TM Forum Frameworx (eTOM, ODA) ([L13](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/technical-details-solution-design-legacy.md?plain=1#L13)). Перенести в архив. |
| 29 | [technical-details-solution-design-oneshot.md](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/technical-details-solution-design-oneshot.md) | А | 1, 8 | draft / 0.1 | — | R S Н | удалить | Пункты 7.x жёстко связаны с 4.x, а в новой структуре решение детализирует раздел 5 (2.6, 2.7) [р. 752, Ч-25](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L58). Плейсхолдер `[ТРЕБУЕТСЯ УТОЧНЕНИЕ…]` ([L21](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/technical-details-solution-design-oneshot.md?plain=1#L21)) есть и в stepwise-версии. Прогонов нет. |
| 30 | [technical-details-solution-design-stepwise.md](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/technical-details-solution-design-stepwise.md) | А | 1, 8, 9 | draft / 0.1 | 0011 | R S C Н G | доработать | Функция нужна: детализация решения — раздел 5 ОРР, пункты 2.6 и 2.7 [р. 752, Ч-25](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L58), [р. 752, Ч-26](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L59). Здесь она оформлена как раздел 7 «для разработчиков» и связана 7.x ↔ 4.x ([L17](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/technical-details-solution-design-stepwise.md?plain=1#L17)), право добавлять пункты 7.x ([L18](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/technical-details-solution-design-stepwise.md?plain=1#L18)), самопроверка «Dev Readiness Check» ([L62](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/technical-details-solution-design-stepwise.md?plain=1#L62)). |
| 31 | [uc-modeling-oneshot.md](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/uc-modeling-oneshot.md) | Г | 1, 4, 5 | draft / 0.1 | — | R E Н F C | доработать | Функция нужна: UC — раздел 7 (2.4, 2.9) и независимый 2.13 [р. 752, Ч-32](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L65). Нет матрицы покрытия [р. 752, Ч-15](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L48). Самооценка «Полнота: ✅/⚠️» ([L53](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/uc-modeling-oneshot.md?plain=1#L53)), роль CBAP ([L11](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/uc-modeling-oneshot.md?plain=1#L11)). |
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
  BCREQ-ФТ на четыре месяца новее, а модель из восьми разделов (р. 752) — ещё на
  два дня. Ни один активный промпт не переведён в
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

### 3.1. Покрытие восьми разделов BCREQ

В версии 0.1 целевой была модель из семи разделов анализа 2026-10-20: промпт а) —
разделы 1–2 ([L543](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/docs/analysis/2026-10-20-bcreq-fr-section-prompts.md?plain=1#L543)), б) — 3 и 5 ([L613](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/docs/analysis/2026-10-20-bcreq-fr-section-prompts.md?plain=1#L613)), в) — 4 и 6
([L678](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/docs/analysis/2026-10-20-bcreq-fr-section-prompts.md?plain=1#L678)), раздел 7 — по запросу БА (правила П3 [L783](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/docs/analysis/2026-10-20-bcreq-fr-section-prompts.md?plain=1#L783) и О11
[L530](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/docs/analysis/2026-10-20-bcreq-fr-section-prompts.md?plain=1#L530)). Эту нумерацию БА подтверждал в RUN-0076, р. 10: «1-4 - да, 5 будет
НФТ (обычно пустой), 6 - ограничения» ([реестр L66](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/runs/2026/RUN-0076/outputs/incident-register.md?plain=1#L66),
[экспорт](https://github.com/user-attachments/files/33669255/chat-export-1110.json)).

Чат 22.10.2026 заменил её моделью из восьми разделов [р. 752, Ч-10](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L43). НФТ переехали из
раздела 5 в раздел 4 [р. 752, Ч-12](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L45), описание решения — из раздела 4 в раздел 5 [р. 752, Ч-13](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L46).
Раздел 6 получил «Особенности разработки» [р. 752, Ч-14](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L47). Раздел 7 стал внутренним разделом
UC, заказчику его не показывают [р. 748, Ч-04](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L37), [р. 752, Ч-15](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L48). Добавлен раздел 8 [р. 752, Ч-16](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L49). Точка
согласования 1 делит документ на разделы 1–4 (верхнеуровневая оценка) и 5–8
(детализированная) [р. 752, Ч-10](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L43). Таблица сравнивает каталог с восемью разделами.

| Раздел (р. 752) | Что есть в `prompts/` | Разрыв |
| --- | --- | --- |
| 1 Термины [р. 752, Ч-20](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L53) | 20, 21: раздел 1 «Терминология» с защитой глоссария ([L20](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/glossary-context-understanding-stepwise.md?plain=1#L20)) | Промпт предлагает модели придумать новые термины: «предложи 1-2 новых термина» ([L41](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/glossary-context-understanding-stepwise.md?plain=1#L41)). БА это отклонил: RUN-0076 I-005, р. 12. |
| 2 Контекст (Контекст и Проблема [р. 764, Ч-49](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L82); ограничения, известные на входе, — в 2.3.2 [р. 761, Ч-45](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L78)) | 20, 21: «2.3. Задачи» ([L50](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/glossary-context-understanding-stepwise.md?plain=1#L50)), «Укажи бизнес-последствия» ([L48](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/glossary-context-understanding-stepwise.md?plain=1#L48)) | Нет пункта «Границы» и деления на Контекст и Проблему. Модель придумывает риски и последствия (RUN-0076 I-004, р. 12: «Не придумывать риски, если они явно не заданы заказчиком»). |
| 3 ФТ: 5±2 верхнеуровневых, только дельта [р. 752, Ч-11](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L44); BABOK или IREB [р. 752, Ч-17](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L50) | 15, 16 производят ФТ как «Раздел 4» ([L12](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/fr-documentation-stepwise.md?plain=1#L12)). Промпт 21 запрещает «Система должна» и называет её «уровнем Раздела 4» ([L15–L16](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/glossary-context-understanding-stepwise.md?plain=1#L15)) | Номер раздела сдвинут. Правил 5±2 [р. 749, Ч-07](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L40) и «только дельта» нет. Запрет на «Систему должна» БА снял: RUN-0074 р. 52, RUN-0076 р. 10. |
| 4 НФТ [р. 752, Ч-12](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L45) | нет | Пробел. Модель сама пропускала НФТ (RUN-0076 I-022, [L85](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/runs/2026/RUN-0076/outputs/incident-register.md?plain=1#L85)). |
| 5 ОРР: ФДТ и ТС [р. 752, Ч-13](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L46); Arc42 + C4 + OpenAPI [р. 752, Ч-18](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L51) | 28–30: раздел 7 «Список доработок» с UI/UX- и техническими деталями к 4.x ([L12–L14](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/technical-details-solution-design-stepwise.md?plain=1#L12)) | Функция есть, но под номером 7 и в связке 7.x ↔ 4.x. ФДТ и ТС не разделены. Стандарты раздела в каталоге не упоминаются; вместо них TM Forum (маркер R). |
| 6 Особенности разработки + Ограничения [р. 752, Ч-14](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L47) | 13, 14: фиксированные 6.1.1–6.1.3 MANGO OFFICE ([L15](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/constraints-documentation-stepwise.md?plain=1#L15)) и «майнинг» новых | Особенностей разработки нет. Модель генерирует ограничения, которые не следуют из источника. Внешнюю разработку ограничения не учитывают (RUN-0073 I-012, р. 6: «ЭТО РАЗРАБОТКА НЕ НА СТОРОНЕ МАНГО», [L73](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/runs/2026/RUN-0073/outputs/incident-register.md?plain=1#L73)). |
| 7 UC + матрица покрытия + граничные кейсы, внутренний [р. 752, Ч-15](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L48) | 31, 32: UC как отдельный процесс 4, вход — «сырое описание» ([L18–L20](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/uc-modeling-stepwise.md?plain=1#L18)) | Нет матрицы покрытия ФТ ↔ UC и граничных кейсов. UC не привязаны к разделам 3 и 5. |
| 8 Дополнительные: риски, зависимости, план приёмки [р. 752, Ч-16](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L49) | нет | Пробел. Совпадает с пробелом П5 (§3.2) и known gap «risk register» (§3.3). |

Заметки разработчикам и реестр вопросов в старой модели жили в разделе 7 (25, 26,
28–30). БА просил: «Можно в разделе 7 комментарием указать то, что для
разработчиков» (RUN-0076 SC-31, р. 66,
[L80](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/runs/2026/RUN-0076/outputs/success-criteria.md?plain=1#L80)). В восьми разделах места для них нет:
это наблюдение Н10 (§3.7.3).

### 3.2. Покрытие конвейера П1–П6 и гейтов

| Этап ([стандарт](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/standards/bcreq-process-standard.md?plain=1#L58)) | Файлы | Разрыв |
| --- | --- | --- |
| П1 Приём и нормализация ([L58](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/standards/bcreq-process-standard.md?plain=1#L58)) | 11, 12, 20, 21, 25, 26 | Покрыт, но в старой модели. Нет правила сносок на источник (RUN-0074 SC-02, р. 16: «Все утверждения размечайте сносками», [L25](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/runs/2026/RUN-0074/outputs/success-criteria.md?plain=1#L25)). |
| П2 Декомпозиция на уровни BCREQ, гейт G1 ([L59](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/standards/bcreq-process-standard.md?plain=1#L59)) | нет; 34 разбивает только составную story | **Пробел:** нет промпта для построения дерева BCREQ. |
| П3 Моделирование ([L60](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/standards/bcreq-process-standard.md?plain=1#L60)) | 31–34 | Покрыт. |
| П4 Документирование и solution design ([L61](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/standards/bcreq-process-standard.md?plain=1#L61)) | 13–16, 20, 21, 28–30 | Покрыт по старой нумерации. Нет раздела 4 НФТ и раздела 8; описание решения стоит в разделе 7 вместо раздела 5 (§3.1). |
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
| Раздел 7 жёстко связан с 4.x | [technical-details L17](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/technical-details-solution-design-stepwise.md?plain=1#L17) | RUN-0073 р. 8: «пункт в разделе 7 предусмотреть» ([L78](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/runs/2026/RUN-0073/outputs/incident-register.md?plain=1#L78), [экспорт](https://github.com/user-attachments/files/33662573/chat-export-1123.json)). Шаблон RUN-0073 не из `prompts/`, но реплика показывает: раздел 7 нужен как заметки по запросу БА, а не как зеркало 4.x. В восьми разделах раздел 7 — внутренние UC [р. 752, Ч-15](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L48), а для заметок места нет (Н10). |

### 3.5. Антипаттерны

| № | Антипаттерн | Где | Доказательство |
| --- | --- | --- | --- |
| АП1 | Роль задана через методологию или сертификат (CBAP, TM Forum, ODA, ITIL, «cisco») | 20 из 27 активных файлов (R) | Модель начинает «диктовать» процессы и архитектуру (§3.4). Правило П1 анализа 2026-10-20 ([L781](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/docs/analysis/2026-10-20-bcreq-fr-section-prompts.md?plain=1#L781)) запрещает называть методологии в роли. В черновиках чата роль «(CBAP)» вернулась [р. 757, Ч-41](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L74) (Н9). |
| АП2 | Модель сама сертифицирует результат: ✅, «Отчет валидации», «Контекст валиден», «Dev Readiness» | 8 файлов (C) | Нарушает правило B3. В RUN-0076 модель выдала «Отчет валидации (Эксперт-Архитектор)» (I-150, [L213](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/runs/2026/RUN-0076/outputs/incident-register.md?plain=1#L213)). Анализ 2026-10-20 запрещает самооценку правилом О13 ([L532](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/docs/analysis/2026-10-20-bcreq-fr-section-prompts.md?plain=1#L532)), вводит блок «Проверка решений» с источниками (О14, [L533](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/docs/analysis/2026-10-20-bcreq-fr-section-prompts.md?plain=1#L533)) и проверкой второй ролью. |
| АП3 | Старая модель разделов: ФТ = 4, «2.3 Задачи», 7.x ↔ 4.x | 11 файлов (S), включая README.executable | §3.1. В новой модели раздел 4 — НФТ [р. 752, Ч-12](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L45). RUN-0073 р. 76: «Вообще по правилам раздел 4 - Функциональный дизайн решения» ([L62](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/runs/2026/RUN-0073/outputs/incident-register.md?plain=1#L62)). |
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

### 3.7. Структура 2.1–2.14 (информационно)

**Источник.** Пункты 2.1–2.13 и решения по составу БА дал одной репликой р. 752
[р. 752, Ч-20](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L53)…[р. 752, Ч-34](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L67). В р. 753 модель нашла опечатку в 2.5 [р. 753, Ч-35](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L68), конфликт 2.10 с
правилом дельты [р. 753, Ч-36](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L69) и пересечение 2.9 с 2.13 [р. 753, Ч-38](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L71), а также предложила пункт
2.14 [р. 753, Ч-37](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L70). В р. 754 БА добавил «промпт нулевой» [р. 754, Ч-39](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L72) и ограничил генерацию
средой чата [р. 754, Ч-69](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L102). План р. 763 закрепил состав [р. 763, Ч-46](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L79), архитектуру [р. 763, Ч-47](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L80) и
порядок блоков A-IN, A-CORE, A-WORK [р. 763, Ч-48](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L81). В р. 778 БА уточнил статус структуры:
это его предложение, которое ждёт подтверждения или альтернатив [р. 778, Ч-59](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L92), а в
аудите она только информационная [р. 778, Ч-60](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L93).

**Как читать матрицу.** Столбец «Близкие по функции файлы» — не маппинг и не
основание статуса [р. 779, Ч-62](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L95). Он показывает, где в каталоге есть материал (доноры
§3.6 и дефекты §3.4), который Задача 2 может учесть. Номера файлов — по §2.1.

#### 3.7.1. Пункты структуры и каталог

| Пункт | Формулировка (чат) | Близкие по функции файлы | Наблюдение |
| --- | --- | --- | --- |
| Промпт 0 | Структура документа, верхнеуровневые правила и шаги [р. 754, Ч-39](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L72); «конституция» [р. 763, Ч-47](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L80) | нет: 2, 3 — навигация для человека, 1 — передача сессии | Пробел. Н12. |
| 2.1 | Разделы 1, 2 (контекст, глоссарий) [р. 752, Ч-20](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L53) | 20, 21 | Старая модель разделов (§3.1, §3.4). Доноры: У1, У3, У6. |
| 2.2 | Продуктовая принадлежность по таксономии и продуктовая команда [р. 752, Ч-21](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L54) | нет | Пробел; связан с known gap «границы Product Layer и Commercial Layer» (§3.3). |
| 2.3 | Раздел 3 (ФТ) [р. 752, Ч-22](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L55) | 15, 16 | ФТ — раздел 4, нет 5±2 и дельты (§3.1). Н7. |
| 2.4 | Раздел 7, первый прогон к разделу 3 [р. 752, Ч-23](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L56) | 31, 32 | Нет матрицы покрытия. Н6. |
| 2.5 | «раздел 4 (ФТ)» [р. 752, Ч-24](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L57) | нет | Пробел НФТ (§3.1). Н2. |
| 2.6 | Раздел 5 (ОРР), детализация ФДТ [р. 752, Ч-25](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L58) | 28–30 частично | ФДТ и ТС не разделены, привязка к 4.x (§3.1). |
| 2.7 | Раздел 5 (ОРР), детализация ТС [р. 752, Ч-26](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L59) | 28–30 частично | То же. |
| 2.8 | Раздел 6 к разделу 5 [р. 752, Ч-27](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L60) | 13, 14 | Вход — раздел 4 (ФТ), а не раздел 5; нет «Особенностей разработки». |
| 2.9 | Раздел 7, второй прогон к разделам 3 и 5 [р. 752, Ч-28](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L61) | 31, 32 | Н4. |
| 2.10 | Независимые ФТ на разработку без дельты по продуктовой таксономии, вход — артефакт 2.1 [р. 752, Ч-29](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L62) | 15, 16 частично | Н3. |
| 2.11 | «(не делать)» [р. 752, Ч-30](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L63) | — | Исключён из состава [р. 763, Ч-46](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L79). |
| 2.12 | Независимые US, вход — артефакт 2.1 [р. 752, Ч-31](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L64) | 33, 34 | Вход в файлах — «сырой запрос» ([L18–L20](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/prompts/us-modeling-stepwise.md?plain=1#L18)), не артефакт 2.1. |
| 2.13 | Независимые UC, вход — артефакт 2.1 [р. 752, Ч-32](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L65) | 31, 32 | Н4. |
| 2.14 | Раздел 8, вход — артефакты 2.6/2.7 (предложение модели) [р. 753, Ч-37](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L70) | нет | Пробел (§3.1, П5 в §3.2). Н5. |

#### 3.7.2. Тематическая принадлежность к процессу BCREQ

Группировка по смыслу [р. 779, Ч-67](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L100), без маппинга на пункты 2.x [р. 779, Ч-62](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L95). Все 34 файла:
к процессу BCREQ относятся 20, не относятся 14.

| Группа | Файлы (№) | Процесс BCREQ | Место в структуре 2.1–2.14 |
| --- | --- | --- | --- |
| Генерация разделов документа (тема А) | 13–16, 20, 21, 28–30 | относится (П4) | Близкие пункты есть (§3.7.1), но файлы реализуют старую модель. |
| Моделирование UC и US (тема Г) | 31–34 | относится (П3) | Близкие пункты есть (§3.7.1). |
| Валидация (тема Б) | 17–19 | относится (П5) | Места нет. Н8. |
| Вопросы заказчику (тема В) | 25, 26 | относится (П1, правило B4) | Места нет. Н10. |
| Расшифровки ASR (тема Д) | 11, 12 | относится как вход П1 | Вне структуры по решению БА: «оставить» [р. 752, Ч-33](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L66). |
| Встречи и письма (тема В) | 22–24 | не относится: коммуникация вне конвейера П1–П6 | — |
| Служебные (тема Е) | 1, 27 | не относится | — |
| Навигация (тема Ж) | 2, 3 | не относится | — |
| Архив (тема З) | 4–10 | не относится | — |

#### 3.7.3. Наблюдения для Задачи 2

Наблюдения о расхождениях каталога с предложенной структурой и о логических
дырах в ней самой [р. 779, Ч-63](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L96). Это вход для подтверждения или альтернатив
структуры, а не решения.

| № | Наблюдение | Доказательство | Вопрос для Задачи 2 |
| --- | --- | --- | --- |
| Н1 | Нумерация разделов в самом чате неустойчива. Раздел 4 назван «Функциональным дизайном решения» [р. 746, Ч-02](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L35), затем НФТ [р. 752, Ч-12](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L45). В р. 764 БА относит раздел 4 и к «чётким коротким формулировкам» [р. 764, Ч-50](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L83), и к разделам «по BABOK» [р. 764, Ч-51](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L84). Модель в р. 765 сдвигает НФТ в раздел 5 [р. 765, Ч-52](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L85), а раздел 4 называет «Дизайном» [р. 765, Ч-68](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L101). До окна НФТ были разделом 5 (RUN-0076 р. 10, §3.1). | [р. 746, Ч-02](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L35), [р. 752, Ч-12](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L45), [р. 764, Ч-50](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L83), [р. 764, Ч-51](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L84), [р. 765, Ч-52](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L85), [р. 765, Ч-68](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L101) | Закрепить нумерацию одним документом до написания промптов. Наличие разделов 1–6 БА вывел из-под альтернатив [р. 766, Ч-64](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L97), поэтому их нумерация должна быть зафиксирована первой. |
| Н2 | Пункт 2.5 генерирует «раздел 4 (ФТ)», но раздел 4 — НФТ. Модель отметила это как опечатку. | [р. 752, Ч-24](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L57), [р. 752, Ч-12](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L45), [р. 753, Ч-35](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L68) | Исправить формулировку 2.5. |
| Н3 | Пункт 2.10 требует ФТ «без дельты», а раздел 3 — «только дельта». | [р. 752, Ч-29](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L62), [р. 752, Ч-11](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L44), [р. 753, Ч-36](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L69) | 2.10 — это другой тип документа со своим стандартом или исключение из правила дельты? |
| Н4 | Второй прогон UC (2.9) пересекается с независимым промптом UC (2.13). В каталоге то же дублирование: файлы 31 и 32 — одна функция в двух режимах (АП5). | [р. 752, Ч-28](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L61), [р. 752, Ч-32](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L65), [р. 753, Ч-38](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L71) | Один промпт UC с двумя видами входа или явное разграничение 2.9 и 2.13. |
| Н5 | Пункт 2.14 (раздел 8) предложила модель. Своей формулировки 2.14 БА не дал, но называет структуру «2.1-2.14» целиком. Раздел 8 без промпта — тот же пробел, что П5 и risk register (§3.2, §3.3). | [р. 753, Ч-37](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L70), [р. 763, Ч-46](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L79), [р. 776, Ч-70](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L103) | Подтвердить 2.14 и его вход явно. |
| Н6 | Блок A-CORE ставит 2.4 (раздел 7) до согласования 1 и после 2.5. Согласование 1 охватывает разделы 1–4, а разделы 5–8 идут после него. Раздел 7 внутренний, поэтому заказчику это не мешает. Но номер пункта не совпадает с порядком исполнения. | [р. 763, Ч-48](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L81), [р. 752, Ч-10](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L43), [р. 748, Ч-04](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L37) | Нумеровать пункты по порядку исполнения или явно описать первый прогон UC как внутренний вход оценки. |
| Н7 | Номера пунктов 2.x совпадают с номерами подразделов документа. «2.3» — и промпт раздела 3, и подраздел 2.3 раздела 2: в черновике модели есть «2.3.2. Исключено из доработки», туда же относятся ограничения на входе. Похожая путаница уже дала дефект «2.3. Задачи» (§3.4). | [р. 752, Ч-22](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L55), [р. 757, Ч-43](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L76), [р. 761, Ч-45](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L78) | Отдельное пространство имён для промптов. |
| Н8 | Нет пункта для валидации и проверки второй ролью (П5, гейт G2). Правило B3 запрещает LLM проходить гейты самой, а §5.4 анализа 2026-10-20 выносит проверку в отдельный вызов ([L746](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/docs/analysis/2026-10-20-bcreq-fr-section-prompts.md?plain=1#L746)). Файлам 17–19 места нет. | §3.2, §3.7.2 | Нужен ли отдельный пункт проверки или проверка входит в каждый пункт 2.x? |
| Н9 | Черновики промптов в чате повторяют антипаттерны каталога. Роль «(CBAP)» (АП1) вернулась. Пример группирует по TM Forum ODA и использует «Control Plane», хотя БА назвал TM Forum закрытой методологией, модель предложила замену на Arc42, а БА оставил TM Forum только альтернативой. | [р. 757, Ч-41](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L74), [р. 755, Ч-40](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L73), [р. 759, Ч-44](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L77), [р. 748, Ч-03](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L36), [р. 749, Ч-06](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L39), [р. 766, Ч-54](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L87) | Проверять промпты 2.x на АП1–АП9 (§3.5) до приёмки. |
| Н10 | Нет места для реестра вопросов к заказчику и заметок разработчикам. Раньше их место было в разделе 7 (RUN-0076 SC-31, р. 66, [L80](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/runs/2026/RUN-0076/outputs/success-criteria.md?plain=1#L80)), теперь раздел 7 — UC. Файлы 25, 26 и owner вопроса по правилу B4 остаются без пункта. | [р. 752, Ч-15](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L48), §3.1, §3.2 | Где живут вопросы: в разделе 8, в отдельном артефакте или в каждом пункте 2.x? |
| Н11 | Гипотеза БА о совместимости доменных стандартов разных продуктов в одном документе не проверена. Правила композиции объединены с мета-стандартами в одну задачу, а кросс-модельные прогоны ушли в бэклог. | [р. 750, Ч-09](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L42), [р. 767, Ч-57](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L90), [р. 766, Ч-56](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L89) | Проверочный кейс на два продукта в Задаче 2. |
| Н12 | Промпт 0 задаёт структуру и все шаги, генерация идёт только в чате. В каталоге нет промпта-«конституции». Варианты oneshot и stepwise (АП5) при Промпте 0 избыточны: шаги задаёт он. | [р. 754, Ч-39](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L72), [р. 763, Ч-47](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L80), [р. 754, Ч-69](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L102) | Нужны ли режимы oneshot/stepwise для промптов 2.x? |

### 3.8. Вектор для Задачи 2

Фундаментального противоречия между структурой 2.1–2.14 и процессом BCREQ аудит не
нашёл (BLUF). Поэтому вектор не альтернативный, а уточняющий:

1. **Задача 2 (мета-стандарты разделов 1–8 и правила композиции [р. 767, Ч-57](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L90)).**
   - Начать с нумерации разделов (Н1); наличие разделов 1–6 не обсуждается [р. 766, Ч-64](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L97).
   - Стандарты из чата: BABOK или IREB для раздела 3 [р. 752, Ч-17](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L50), Arc42 + C4 + OpenAPI
     для раздела 5 [р. 752, Ч-18](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L51), TM Forum — альтернатива [р. 766, Ч-54](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L87).
   - Наблюдения Н1–Н12 — вход для подтверждения или альтернатив 2.1–2.14 [р. 778, Ч-59](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L92).
     Правило 20%: если практика отличается в его пределах, развивать
     предложенное БА [р. 766, Ч-55](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L88).
   - Правила анализа 2026-10-20 (О/А/Б/В/П, проверка второй ролью) — источник
     идей, а не эталон [р. 750, Ч-08](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L41), [р. 765, Ч-53](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L86). Уже согласованное в процессе — конвейер
     П1–П6, гейты G1–G3, правила B3–B7 — сохранить.
2. **Задача 3 (промпты 2.x).** Писать заново в `/prompts/bcreq/` [р. 767, Ч-65](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L98). Текущие
   файлы — доноры отдельных механик (У1–У10, §3.6), а не основа. Не переносить
   АП1–АП9 (Н9).
3. **Кандидаты на удаление.** Переводить в legacy только после появления замены,
   чтобы ссылки прогонов не сломались. Физическое удаление и обновление README —
   в бэклоге [р. 767, Ч-66](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L99), [р. 766, Ч-56](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L89).
4. **Пробелы П2/G1 (дерево BCREQ), П6/G3 (baselining) и 11 known gaps** — ставить
   отдельными задачами, а не встраивать в существующие файлы.

Ограничение: прогоном модели не проверены ни промпты анализа 2026-10-20
([§7, L864](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/docs/analysis/2026-10-20-bcreq-fr-section-prompts.md?plain=1#L864)), ни черновики промптов из чата [р. 757, Ч-41](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L74).

## 4. Recommendations

Рекомендации **не обязательны к применению** (см. §1): это входные данные для
Задачи 2. Статусы «удалить» и «доработать» — кандидаты [р. 779, Ч-61](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L94). Номера даны по
§2.1.

**Удалить из активного набора (12):**

- **4 `archive/.gitkeep`** — удалить физически: файл избыточен.
- **20, 21 (glossary), 15, 16 (fr-documentation), 13, 14 (constraints), 29
  (technical-details-oneshot)** — сделать legacy, когда в `/prompts/bcreq/`
  появится замена [р. 767, Ч-65](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L98). Файлы конкурируют с процессом BCREQ [р. 752, Ч-34](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L67): реализуют
  старую модель разделов (§3.1). Два из них — дословный источник 18 инцидентов
  (§3.4).
- **18 (fr-validation-oneshot)** — сделать legacy, когда появится проверка второй
  ролью отдельным вызовом ([§5.4](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/docs/analysis/2026-10-20-bcreq-fr-section-prompts.md?plain=1#L746), Н8).
- **17, 25, 28 (fr-validation-legacy, questions-legacy, technical-details-legacy)**
  — перенести в архив. У каждого есть более новый вариант. Файлы 17 и 25 упомянуты
  в прогонах, поэтому их нужно сохранить, а не стирать.

**Доработать (11):**

- **19 fr-validation-stepwise** — убрать привязку к 4.x и правило «сформулируй
  требование на основе контекста». Сохранить структуру «пункт → проблема →
  вариант».
- **30 technical-details-stepwise** — донор для раздела 5 ОРР [р. 752, Ч-13](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L46): заменить
  связь 7.x ↔ 4.x на раздел 5, развести ФДТ и ТС [р. 752, Ч-25](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L58), [р. 752, Ч-26](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L59). Убрать роль
  CBAP/TM Forum и Dev Readiness Check.
- **26 questions-stepwise** — сохранить механику У6. Место реестра вопросов
  определит Задача 2 (Н10). Добавить owner и ссылку на `customer-questions` по
  правилу B4. Убрать роль CBAP и английские метки.
- **31–34 uc/us-modeling** — убрать роль CBAP и самооценку ✅. Развести Job
  Story и User Story. Связать статус с правилами B4–B7. Для UC добавить матрицу
  покрытия и граничные кейсы [р. 752, Ч-15](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L48).
- **22 letter** — снять метку `legacy`, добавить явный формат вывода и правило
  «не выдумывай».
- **1 handover** — привести frontmatter к остальным промптам (`id`/`title`) или
  вынести из каталога БА-промптов. Убрать дубль функции session-debug.
- **2, 3 README** — после Задачи 3 обновить маршрутизацию под восемь разделов и
  `/prompts/bcreq/`. Убрать `ai-generated`.

**Оставить (9):**

- **5–10 архив** — оставить: на них ссылаются RUN-0001…RUN-0003.
- **23, 24 meeting** — оставить как есть. Объединять ли их в один файл с
  параметром аудитории — решение Задачи 2.
- **27 session-debug** — оставить. Роль CBAP избыточна, но на работу не влияет.

**Промпт для расшифровки (2):**

- **11, 12 asr-ingestion** — оставить по решению БА [р. 752, Ч-33](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L66) как отдельный вход П1.
  Механика словаря и подтверждений из файла 11 — донор (У7). Формат вывода — из
  файла 12.

**Для Задачи 2:** подтвердить или заменить структуру 2.1–2.14 по наблюдениям
Н1–Н12 (§3.7.3).

## 5. Related Artifacts

- Issue: [#384](https://github.com/G-Ivan-A/mango_ba_prompts/issues/384); PR:
  [#385](https://github.com/G-Ivan-A/mango_ba_prompts/pull/385) (версия 0.1);
  [комментарий Пользователя с экспортом чата](https://github.com/G-Ivan-A/mango_ba_prompts/pull/385#issuecomment-6365671972)
  (версия 0.2).
- Экспорт чата «Проект: СПЛИТ (БА)»: [chat-export-промптба.json](https://github.com/user-attachments/files/33873099/chat-export-.json)
  (в репозиторий не коммитится, правило #309).
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
  - реестр цитат чата 21–23.10.2026 [chat-2026-10-22-23-register.md](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-2026-10-22-23-register.md);
  - сверка цитат [issue_384_verify_chat_quotes.py](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384_verify_chat_quotes.py),
    итог [chat-quote-check.json](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384/chat-quote-check.json);
  - разворот окна для локального чтения [issue_384_chat_window_dump.py](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_384_chat_window_dump.py)
    (вывод в `experiments/issue_384/turns/` игнорируется git);
  - валидатор [validate_issue_384_prompts_audit.py](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/scripts/validate_issue_384_prompts_audit.py).
- Реестры чатов:
  - RUN-0073: [инциденты](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/runs/2026/RUN-0073/outputs/incident-register.md), [критерии успеха](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/runs/2026/RUN-0073/outputs/success-criteria.md);
  - RUN-0074: [инциденты](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/runs/2026/RUN-0074/outputs/incident-register.md), [критерии успеха](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/runs/2026/RUN-0074/outputs/success-criteria.md);
  - RUN-0075: [инциденты](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/runs/2026/RUN-0075/outputs/incident-register.md), [критерии успеха](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/runs/2026/RUN-0075/outputs/success-criteria.md);
  - RUN-0076: [инциденты](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/runs/2026/RUN-0076/outputs/incident-register.md), [критерии успеха](https://github.com/G-Ivan-A/mango_ba_prompts/blob/dbf1d3c58ca5a4c145929e644b2b31803b0ea11d/runs/2026/RUN-0076/outputs/success-criteria.md).
