---
status: draft
version: 0.1
updated: 2026-08-21
ai-generated: true
type: index
scope: mango-only
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/279"
---

# Вход прогона RUN-0029 — провенанс

## Файл, приложенный к issue #279

| Вложение | Размер | MD5 | SHA-256 |
| --- | --- | --- | --- |
| [`994-chat-export-1787301559767.json`](https://github.com/user-attachments/files/31298354/994-chat-export-1787301559767.json) | 170 977 Б | `1f5fcfeff231dfc13c04f7d209e29ef8` | `13ee745d…b4e9c7a9` |

Метаданные выгрузки: `title: "994"`, `chat_id 3e47eff2-03cb-46a5-8278-bec774fcdb60`,
`created_at 1778660660`, `updated_at 1778667697`, активная ветка от
`currentId 1c7ed1d2-2c68-4964-8af2-6ad4a5715ca4` — **18 сообщений** (9 эпизодов
«БА → модель»), модель всех ответов `qwen3.6-plus`.

Проверка воспроизводима:

```bash
curl -sL -o 994-chat.json https://github.com/user-attachments/files/31298354/994-chat-export-1787301559767.json
md5sum 994-chat.json     # 1f5fcfeff231dfc13c04f7d209e29ef8
sha256sum 994-chat.json  # 13ee745db4598d5c168b37a26a7ae756ee80e18a116c6a1a833a5667b4e9c7a9
```

## Что сохранено в репозитории

| Файл | Что это | Как получен |
| --- | --- | --- |
| [`chat-transcript.md`](./chat-transcript.md) | Дословная стенограмма активной ветки диалога, 18 сообщений | `python3 scripts/chat_export_to_markdown.py 994-chat.json --transcript …` |
| [`../logs/turn-metrics.md`](../logs/turn-metrics.md) | Пореплико́вая таблица usage платформы (in/out/reasoning, UTC, вложения) | тот же скрипт, ключ `--metrics` |

Полная команда воспроизведения из корня репозитория:

```bash
python3 scripts/chat_export_to_markdown.py 994-chat.json \
  --transcript runs/2026/RUN-0029/inputs/chat-transcript.md \
  --metrics    runs/2026/RUN-0029/logs/turn-metrics.md
```

Исходный JSON в репозиторий не копируется: 167 КБ на бо́льшую часть состоят из
служебных полей платформы (`user_id`, `chat_id`,
`content_list[phase=thinking_summary]`, `usage`). Прямая ссылка на вложение
issue сохранена выше — контракт `runs/` это допускает («входные данные
корректно сохранены **или** на них есть прямая ссылка»).

## Внешние источники, переданные внутри диалога

| Реплика | Вложение | Статус в репозитории |
| --- | --- | --- |
| 0 | `Mango_office_integration_Bitrix24_compressed.pdf` — руководство по интеграции Mango Office с Битрикс24 | не копируется (продуктовая документация) |
| 0 | `image.png` — скриншот Заказчика с отметкой, где в Битрикс24 должны появиться записи | не копируется (данные Заказчика) |
| 6 | `LK_manual_v-119_compressed.pdf` — справочник абонента ВАТС Mango Office v1.19 | не копируется (продуктовая документация) |

Следствие для чтения метрик: на репликах 0–5 в контексте было только
руководство по интеграции с Битрикс24; справочник ВАТС появился на реплике 6.
Скачок входных токенов платформы на реплике 7 (49 587 → 205 638, см.
[`../logs/turn-metrics.md`](../logs/turn-metrics.md)) — момент загрузки второго
PDF в контекст. Ссылки на разделы ВАТС/КЦ, данные моделью **до** реплики 6
(дефекты Г1 и Г2 в [`../feedback/review-notes.md`](../feedback/review-notes.md)),
опираться на приложенный источник не могли.

## Важно о статусе данных

Согласно постановке issue #279 данные диалога могут представлять как финальные,
так и промежуточные результаты. **Итоговый список вопросов
([`../outputs/final-artifact.md`](../outputs/final-artifact.md)) не является
согласованным шаблоном или golden case** — он не был отправлен Заказчику в
рамках зафиксированного диалога. Прогон зафиксирован как `run_type: statistics`
— ради сбора эмпирических данных о коммуникации «БА ↔ ИИ», о результативности и
о галлюцинациях.
