---
status: draft
version: 0.1
updated: 2026-08-21
ai-generated: true
type: experiment
scope: runs
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/269"
related_artifacts:
  - "runs/2026/RUN-0014/metadata.yaml"
---

# Рендер экспорта чата в артефакты прогона (RUN-0014)

> **Зачем.** Прогон [`RUN-0014`](../../runs/2026/RUN-0014/metadata.yaml) зафиксирован
> не в репозитории, а во внешнем веб-интерфейсе LLM. Единственный Proof of Execution —
> JSON-экспорт чата, приложенный к
> [issue #269](https://github.com/G-Ivan-A/mango_ba_prompts/issues/269).
> Скрипт переводит его в стенограмму и в измеренные метрики, чтобы `metadata.yaml`
> содержал наблюдаемые числа, а не оценки «на глаз».

## Почему нужен отдельный рендер

В экспорте поле `content` у сообщений ассистента **пустое**: текст ответа лежит в
`content_list[]` в фазе `phase: "answer"`, рядом с фазами `thinking_summary`,
`web_search` и `web_extractor`. Наивное чтение `content` даёт пустую стенограмму —
именно поэтому «прогон не воспроизводится» без этого шага. Там же лежат `usage`
(токены по каждому ответу, включая `reasoning_tokens` и `cached_tokens`) и перечень
веб-источников, реально показанных модели, — это позволяет отличить цитату по
документу от неподтверждённого утверждения.

## Воспроизведение

```bash
python3 experiments/run-0014-chat-export/render_chat_export.py \
    runs/2026/RUN-0014/inputs/chat-export-1075.json \
    --transcript runs/2026/RUN-0014/logs/chat-transcript.md \
    --front-matter experiments/run-0014-chat-export/transcript-front-matter.yaml \
    --metrics-json -
```

Скрипт stdlib-only, сети не требует. Стенограмма собирается по активной ветке
диалога (от `currentId` вверх по `parentId`); альтернативная ветка регенерации
первого ответа в неё не входит и учтена отдельно в
[`../../runs/2026/RUN-0014/logs/metrics.md`](../../runs/2026/RUN-0014/logs/metrics.md).
