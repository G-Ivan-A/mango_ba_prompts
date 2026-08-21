---
status: draft
version: 0.1
updated: 2026-08-21
ai-generated: true
type: index
scope: mango-only
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/274"
---

# Вход прогона RUN-0020 — провенанс

## Файл, приложенный к issue #274

| Вложение | Размер | MD5 | SHA-256 |
| --- | --- | --- | --- |
| [`975-chat-export-1787301467390.json`](https://github.com/user-attachments/files/31298283/975-chat-export-1787301467390.json) | 1 187 019 Б | `c8d0142e2b989bec0b00958c131770a0` | `8c1b3387…1a0d049` |

Метаданные выгрузки: `title: "975"`, `chat_id 7db106d7-a9f9-4bc6-b41d-cd55a4abd7fe`,
`created_at 1783611420`, `updated_at 1783677279`, активная ветка от
`currentId 03db9281-ad75-4b38-9383-04fd80257435` — **76 сообщений** (38 эпизодов
«БА → модель»), модель всех ответов `qwen3.7-plus`.

Проверка воспроизводима:

```bash
curl -sL -o 975-chat.json https://github.com/user-attachments/files/31298283/975-chat-export-1787301467390.json
md5sum 975-chat.json     # c8d0142e2b989bec0b00958c131770a0
sha256sum 975-chat.json  # 8c1b3387141a89cf2b9c584290f186a454586984d17f8c6b5bf3f88941a0d049
```

## Что сохранено в репозитории

| Файл | Что это | Как получен |
| --- | --- | --- |
| [`chat-transcript.md`](./chat-transcript.md) | Дословная стенограмма активной ветки диалога, 76 сообщений | `python3 scripts/chat_export_to_markdown.py 975-chat.json --transcript …` |
| [`../logs/turn-metrics.md`](../logs/turn-metrics.md) | Пореплико́вая таблица usage платформы (in/out/reasoning, UTC, вложения) | тот же скрипт, ключ `--metrics` |

Полная команда воспроизведения из корня репозитория:

```bash
python3 scripts/chat_export_to_markdown.py 975-chat.json \
  --transcript runs/2026/RUN-0020/inputs/chat-transcript.md \
  --metrics    runs/2026/RUN-0020/logs/turn-metrics.md
```

Исходный JSON в репозиторий не копируется: 1,13 МБ на бо́льшую часть состоят из
служебных полей платформы (`user_id`, `chat_id`,
`content_list[phase=thinking_summary]`, `usage`). Прямая ссылка на вложение
issue сохранена выше — контракт `runs/` это допускает («входные данные
корректно сохранены **или** на них есть прямая ссылка»).

## Внешний источник, переданный внутри диалога

На реплике №10 БА приложил к чату файл **`CC_manual_1.26.23_compressed.pdf`** —
руководство пользователя Контакт-центра Mango Office v1.26.23. Файл принадлежит
продуктовой документации Заказчика, в репозиторий не копируется. Следствие для
чтения метрик: реплики 0–9 модель отвечала **без** доступа к руководству
(отсюда дефекты достоверности Г2 и Г3, см.
[`../feedback/review-notes.md`](../feedback/review-notes.md)), реплики 11–75 — с
доступом. Скачок входных токенов на реплике 11 (10 393 → 244 231 по данным
платформы) — момент загрузки PDF в контекст.

## Важно о статусе данных

Согласно постановке issue #274 данные диалога могут представлять как финальные,
так и промежуточные результаты. **Итоговый документ
([`../outputs/final-artifact.md`](../outputs/final-artifact.md), ФТ v1.5) не
является согласованным шаблоном или golden case.** Прогон зафиксирован как
`run_type: statistics` — ради сбора эмпирических данных о применении промптов,
о коммуникации «пользователь ↔ ИИ», о результативности и о галлюцинациях.
