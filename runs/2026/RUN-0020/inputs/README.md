---
status: draft
version: 0.1
updated: 2026-08-21
ai-generated: true
type: input
scope: mango-only
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/273"
---

# Вход прогона: история чата по задаче 1065

> **Источник.** Файл, приложенный к
> [issue #273](https://github.com/G-Ivan-A/mango_ba_prompts/issues/273):
> `1065-chat-export-1787301452625.json` (экспорт диалога БА с LLM).
> Прогон **не воспроизводился заново**: фиксируется реально состоявшийся диалог
> (Proof of Execution), артефакты собраны из его содержимого.

## Состав входа

| Файл | Что это |
| --- | --- |
| [`1065-chat-export-1787301452625.json`](1065-chat-export-1787301452625.json) | Дословный экспорт истории чата (1 622 278 байт), как приложен к issue #273. Не редактировался. |
| [`transcript.md`](transcript.md) | Линейный транскрипт 78 сообщений, полученный из экспорта детерминированным скриптом. Промежуточный артефакт для чтения и цитирования. |

## Как получен транскрипт (воспроизводимо)

```bash
python3 scripts/chat_export_to_markdown.py \
  runs/2026/RUN-0020/inputs/1065-chat-export-1787301452625.json \
  --transcript runs/2026/RUN-0020/inputs/transcript.md \
  --metrics runs/2026/RUN-0020/logs/turn-metrics.md
```

> **Статус скрипта.** `scripts/chat_export_to_markdown.py` — **локальный
> инструмент воспроизводимости, а не артефакт прогона**. Он запускается вручную,
> не вызывается из GitHub Actions и не входит в CI. Зависимостей, кроме
> стандартной библиотеки Python 3, нет. Общее правило — в [`runs/README.md` →
> «Локальные инструменты
> воспроизводимости»](../../../README.md#локальные-инструменты-воспроизводимости).

Транскрипт и `logs/turn-metrics.md` — производные файлы: их можно пересобрать из
JSON в любой момент, frontmatter в них намеренно не добавляется, чтобы
пересборка была побайтово детерминированной. Особенности формата экспорта
(ветка восстанавливается от `currentId` по `parentId`, текст ответа лежит в
`content_list[*]` с `phase == "answer"`, метрики — в `content_list[*].usage`)
описаны в [`RUN-0017/inputs/README.md`](../../RUN-0017/inputs/README.md).

## Бизнес-вход диалога (кратко)

Задача 1065 — **пресейл-анализ запроса ООО «А7-А»**: заказчик ведёт внутренний
тендер на телефонию, использует связку MANGO OFFICE + Битрикс24 в двух регионах
(Ярославль, Москва) и хочет прийти к единому решению. Цель диалога — сформировать
**БЛОК 1 (Контекст)** и **БЛОК 2 (Вопросы на уточнение Заказчику)**.

БА подал в диалог:

- промпт `mango-glossary-context-understanding-stepwise` дословно, с маркером
  `<!-- mango-glossary-context-understanding-stepwise -->`
  ([`prompts/glossary-context-understanding-stepwise.md`](../../../../prompts/glossary-context-understanding-stepwise.md));
- собственный глоссарий (Система, КЦ, ЛК, Клиент КЦ, Wallboard и др.) — по
  правилу «защита глоссария» из промпта;
- документацию продукта: `CC_manual_1.26.23_compressed.pdf` (Руководство КЦ),
  `LK_manual_v-121_compressed.pdf` (Руководство ЛК ВАТС),
  `Programma-dlya-EVM-Wallboard-Mango-Office_v7.22.25.pdf`,
  `Mango_office_integration_Bitrix24.pdf`;
- документы **Заказчика** (формулировки заказчика, не факты о продукте):
  `Тематики.pdf`, `Запрос по настройке статусов А7.pdf`,
  `ТЗ ООО А7-А на доработки дашборд.pdf`;
- скриншоты интерфейса (`image.png`) для сверки полей карточки обращения и
  ролевой модели.

Сами PDF/PNG в экспорт не попали и в репозитории не хранятся: доступны только
цитаты из них внутри диалога. Это ограничивает верификацию фактов документацией
(см. [`../outputs/quality-findings.md`](../outputs/quality-findings.md)).
