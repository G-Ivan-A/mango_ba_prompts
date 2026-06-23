---
status: draft
version: 0.1
updated: 2026-06-23
ai-generated: true
type: validation-note
scope: governance
issue: "https://github.com/G-Ivan-A/mango_ba_prompts/issues/193"
contract: "governance/contracts/approval-contract.md"
tested_document: "docs/analysis/rfc-industry-taxonomy-improvement.md"
---

# Тест контракта согласования: RFC Industry Taxonomy

Этот документ фиксирует сухой прогон
[`governance/contracts/approval-contract.md`](../../governance/contracts/approval-contract.md)
на текущем RFC
[`docs/analysis/rfc-industry-taxonomy-improvement.md`](rfc-industry-taxonomy-improvement.md).
Цель теста — проверить, что AI-агент читает реальный документ, строит карту
разделов, формирует один атомарный пакет согласования и останавливается до
решения фаундера.

Тест не утверждает RFC и не меняет Industry Taxonomy artifacts.

## 1. Тестовый запуск

Триггер, эквивалентный пользовательскому запросу:

> Проведи атомарное согласование RFC Industry по контракту
> `governance/contracts/approval-contract.md`.

Вход:

| Поле | Значение |
| --- | --- |
| `document_ref` | `docs/analysis/rfc-industry-taxonomy-improvement.md` |
| `approval_goal` | Подготовить первый пакет согласования по разделу 1 |
| `related_context` | `docs/analysis/taxonomy-convergence-test.md`, `docs/analysis/mango-taxonomy-convergence-test.md`, `standards/industry-taxonomy-standard.md`, `standards/decisions/ADR-011-industry-taxonomy.md` |

Источник чтения: локальный файл репозитория
`docs/analysis/rfc-industry-taxonomy-improvement.md`.

## 2. Проверка структуры документа

В документе найдено 9 верхнеуровневых разделов:

| Раздел | Название | Роль в RFC |
| --- | --- | --- |
| 1 | Статус путей после PR #173 | Фиксирует актуальные пути и scope после path refactor |
| 2 | Входные факты | Даёт метрики двух convergence tests и состояние registry |
| 3 | Корневые причины | Объясняет источники расхождений |
| 4 | Предлагаемые изменения | Перечисляет change requests R1-R8 |
| 5 | Ожидаемый measurable effect | Формулирует ожидаемый эффект согласования |
| 6 | Влияние на артефакты | Показывает, какие файлы затрагиваются после approval |
| 7 | Implementation plan after approval | Описывает порядок реализации после решения |
| 8 | Risks | Фиксирует риски RFC |
| 9 | Approval request | Формулирует запрос к фаундеру |

Основные зависимости:

- раздел 1 задаёт path/scope baseline для разделов 4, 6 и 7;
- раздел 2 обосновывает причины из раздела 3;
- раздел 3 обосновывает предложения R1-R8 из раздела 4;
- разделы 5-9 зависят от принятия или доработки предложений раздела 4;
- внешние документы: `standards/industry-taxonomy-standard.md`,
  `standards/decisions/ADR-011-industry-taxonomy.md`,
  `docs/analysis/taxonomy-convergence-test.md`,
  `docs/analysis/mango-taxonomy-convergence-test.md`.

## 3. Пакет согласования для раздела 1

### A. Общее резюме раздела

Раздел 1 фиксирует, что RFC должен использовать актуальные пути после
переименования taxonomy-каталогов: `kb/industry-taxonomy/` и
`kb/mango-taxonomy/`. Роль раздела — снять риск работы поверх устаревших путей и
зафиксировать, что PR #173 уже merged в `upstream/main`, а дальнейшие изменения
не должны выходить за scope issue #178.

### B. Конкретные предложения в разделе

В разделе есть конкретика:

1. Для реализации после approval использовать только текущие taxonomy
   directories: `kb/industry-taxonomy/` и `kb/mango-taxonomy/`.
2. Считать path refactor завершённой зависимостью.
3. Не предлагать новое переименование каталогов внутри этого RFC.
4. Держать дальнейшие изменения внутри утверждённого scope issue #178.

Контроль обработки отсутствующей конкретики: для раздела 1 маркер
«В разделе конкретных предложений НЕТ» не применяется, потому что конкретика
есть. Этот маркер остаётся обязательным для разделов без предложений.

### C. Вопросы для согласования

1. Подтверждаем ли, что `kb/industry-taxonomy/` и `kb/mango-taxonomy/` являются
   единственными рабочими taxonomy paths для реализации этого RFC?
2. Согласен ли фаундер считать path refactor после PR #173 закрытой зависимостью,
   чтобы RFC не возвращался к переименованию каталогов?
3. Правильно ли ограничить будущую реализацию scope issue #178 без добавления
   новых path refactor tasks?

### D. Зависимости

- Зависимость от PR #173 как завершённого path refactor.
- Зависимость от `docs/analysis/taxonomy-convergence-test.md` и
  `docs/analysis/mango-taxonomy-convergence-test.md`: эти отчёты дают входные
  данные для следующих разделов.
- Зависимость от `standards/industry-taxonomy-standard.md`: будущие изменения
  должны остаться совместимыми с действующим стандартом до явного approval.
- Связь с разделом 4 RFC: предложения R1-R8 должны использовать paths,
  зафиксированные в разделе 1.

### Статус

Ожидается решение фаундера по разделу 1: approve / rework / blocked.

Стоп-условие атомарности: агент не переходит к разделу 2 до фиксации решения по
разделу 1.

## 4. Результат проверки контракта

Контракт прошёл тестовую проверку на RFC Industry Taxonomy:

- полное содержимое документа прочитано из локального файла;
- структура RFC выделена до начала согласования;
- первый пакет содержит резюме, конкретные предложения, вопросы и зависимости;
- статус раздела отделён от статуса всего RFC;
- атомарность соблюдена: тест остановлен после раздела 1.

Регрессионная проверка закреплена в
[`scripts/validate_issue_193_approval_contract.py`](../../scripts/validate_issue_193_approval_contract.py).
