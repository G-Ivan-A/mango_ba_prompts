---
name: bcreq-c12
description: Assemble a complete BCREQ phase snapshot from baseline and all ordered slices; use for FULL output and handoff, never for approval.
status: draft
version: 0.1
updated: 2026-10-30
temperature: 0.1
---

# C12 — wrapper для review

Нативное имя файла при установке: SKILL.md. Здесь файл не активирован.
Он не содержит scripts. Прочитай полные rules/constitution.md,
rules/state-contract.md и rules/classes/12-phase-assembly.md; не продолжай
без обязательных текстов и совместимого rule receipt C36. Полный стандарт
имеет приоритет над этим сокращённым wrapper. Этот wrapper не заменяет
доставку его алгоритма/стопов/контекста/checks.

1. Проверь task/phase/revision и обязательные именованные inputs C12 из
   полного стандарта. Получи base_snapshot и всю цепь ordered_slices.
2. Сверь parent_revision, ID, зависимости, источники и разрешения tombstones.
   Не бери только последний slice. Несвязная цепь → WAITING с missing input.
3. Собери все живые полные тела и все required phase sections. Сохрани
   source_register, decisions, unresolved, exceptions, preserved/stale IDs.
4. Выдай BCREQ_OUTPUT с полями общего контракта, mode FULL, точным
   receipt.live_ids; не выдавай ссылки вместо тел. Части INCOMPLETE до
   завершения всего списка. Самопроверка не меняет human approval.
5. Перед записью предъяви путь candidate и diff, сохрани только разрешённое,
   перечитай результат. Порекомендуй C39/C20/C13 с причиной, верни управление БА.
