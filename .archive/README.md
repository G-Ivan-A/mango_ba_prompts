---
status: canonical
version: 1.0
updated: 2026-08-21
temperature: 0.1
executable: false
scope: mango_ba_prompts
---

# `.archive/` — скрытый архив спицы

Каталог хранит артефакты со статусом `superseded`: они больше не являются
точками входа для агента и человека, но сохраняются ради traceability
(контракт issue #267: «архив не потерян и не является точкой входа»).

## Почему каталог скрытый

Точка в начале имени убирает архив из обычного `ls`, из визуального верха
дерева на GitHub и из внимания агента при онбординге. Это прямое требование
issue #291 (контракт 5): архив не должен конкурировать за внимание с активными
каталогами. Тот же приём — «архив рядом с активным файлом» — и был причиной
беспорядка: `agent-onboarding-protocol_old.md` лежал в `ai-rules/` вплотную к
актуальному `agent-onboarding-protocol.md` v1.5.

## Правила

| Правило | Норма |
| --- | --- |
| Что кладём | Только файлы с `status: superseded`, у которых есть действующий преемник. |
| Что не кладём | `runs/` и `kb/` — неприкосновенны (контракт 2 issue #291). Активные артефакты любого статуса, кроме `superseded`. |
| Обязательная шапка | Первым блоком после frontmatter — баннер `🗄️ АРХИВ (superseded, issue #NNN)` со ссылкой на актуальный файл. |
| Ссылки | Архив может ссылаться на активные артефакты. Активный артефакт ссылается на архив только в явно помеченной строке «архив/traceability». |
| Удаление | Запрещено без отдельного issue: архив — источник traceability. |

## Содержимое

| Путь | Заменён на | Issue |
| --- | --- | --- |
| [`ai-rules/agent-onboarding-protocol_old.md`](ai-rules/agent-onboarding-protocol_old.md) | [`ai-rules/agent-onboarding-protocol.md`](../ai-rules/agent-onboarding-protocol.md) v1.5 | [#267](https://github.com/G-Ivan-A/mango_ba_prompts/issues/267) |
| [`ai-rules/agent-onboarding-protocol_old.executable.md`](ai-rules/agent-onboarding-protocol_old.executable.md) | [`ai-rules/agent-onboarding-protocol.md`](../ai-rules/agent-onboarding-protocol.md) v1.5 | [#267](https://github.com/G-Ivan-A/mango_ba_prompts/issues/267) |

Аудит, обосновавший вынос: [`docs/audit/2026-08-21-root-structure-audit.md`](../docs/audit/2026-08-21-root-structure-audit.md).
