---
status: draft
version: 0.1
updated: 2026-10-30
temperature: 0.1
---

# Неактивные примеры доставки

Это проектные шаблоны для review, не установленный агент. В репозитории нет
новых активных AGENTS/hints/skills, ключей, hooks или shell-узлов процесса БА.
Python в соседнем validator — только офлайн-проверка исследования в CI.

| Файл | Назначение | Перед применением |
| --- | --- | --- |
| [rule-template.md](rule-template.md) | Общее ядро для выбранного клиентского механизма rules | Поставить все полные правила и реальные версии; проверить global/local конфликты. |
| [skill-template.md](skill-template.md) | Native wrapper C12 без scripts | Перенести в SKILL.md выбранного клиента, поставить стандарт C12 по указанному пути. Для других классов использовать точные I/O/stop/checks из catalog, не переименовывать C12. |
| [goose-review.json](goose-review.json) | Recipe обсуждения без extensions | Вставить весь проверяемый материал вручную: этот recipe не читает ФС, не загружает skills и не проверяет файлы. Не является основным профилем работы с ФС. |
| [opencode-v1.json](opencode-v1.json) | Проектный профиль V1 с запретом bash/task/web и reviewer без edit | Сверить версию/schema и итоговое слияние global/project/agent policies. Создать указанные rules; пустой список plugins/MCP не очищает все глобальные настройки. |
| [contract-fixture.json](contract-fixture.json) | Конечный синтетический baseline, SLICE, FULL, решения и два фактора | Используется только reference probes; `verified-in-fixture` не аутентификация пользователя. |

В Goose ядро передаётся через проектный `.goosehints` с явным включением
полного тела `@rules/constitution.md` и `@rules/state-contract.md`;
Developer включён, shell Never Allow, editor Ask Before. Неактивный
Goose recipe намеренно имеет `extensions: []`: не расширять его скрыто
до filesystem-профиля. Рабочий профиль описан в учебной инструкции.

В OpenCode AGENTS содержит ядро, `instructions` добавляет полные тексты.
В Cline выбран один rules-каталог, skill устанавливается в
`.cline/skills/bcreq-c12/SKILL.md`. UI Plan для read/review; Act и отдельное
подтверждение для записи, auto-approve/YOLO выключены. JSON OpenCode нельзя
импортировать как настройки Cline или Goose.

Пробы перед корпоративным включением: обнаружение и чтение skill body;
отказ shell и внешнего пути; запись только после tool approval; FULL после
compaction; WAITING при missing parent; старый approval не переносится;
инструкция внутри source не исполняется. Зафиксировать tool calls/results
и отличия версий. Ни один результат runtime этих проб здесь не симулируется.
