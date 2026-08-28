---
status: draft
version: 0.1
updated: 2026-08-27
ai-generated: true
type: log
scope: mango-only
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/333"
---

# Протокол доступности источника (RUN-0060)

## Спецификация hh.ru

| Параметр | Значение |
| --- | --- |
| URL | `https://api.hh.ru/openapi/specification/public` |
| Дата обращения | 2026-08-27 |
| HTTP | `200 OK` |
| `Content-Type` | `application/x-yaml` — **JSON не отдаётся даже при `Accept: application/json`** |
| Формат | OpenAPI 3.0.3 (YAML) |
| Размер | 1 266 778 байт |
| SHA-256 | `8ea1380bf87d7351cf2f977f9918bbdd03a26a6b9c9e95eb50f3d4ae080a7576` |
| Операций | 131 |
| Разделов (tags) | 47 |

Команда проверки:

```bash
curl -sS -D- -o /tmp/hh-spec.yaml 'https://api.hh.ru/openapi/specification/public'
sha256sum /tmp/hh-spec.yaml
wc -c /tmp/hh-spec.yaml
```

## Существенное наблюдение: спецификация изменилась

RUN-0058 зафиксировал SHA-256 `4349900b…6383d`. На 2026-08-27 контрольная сумма
другая, поэтому **ни один вывод L2 не переносился в L4 без повторной проверки
по свежему файлу**. Результаты проверки — [`l2-validity-recheck.md`](l2-validity-recheck.md).

## Ссылки в документацию

Прямые якоря Redoc строятся по схеме
`https://api.hh.ru/openapi/redoc#tag/<slug(tag)>/operation/<operationId>`.
Алгоритм `slug` (транслитерация по таблице символов → удаление символов вне
`[\w\s$*_+~.()'"!\-:@]` в ASCII-режиме → схлопывание пробелов и дефисов в `-`)
воспроизведён в [`experiments/issue_333_hh_api_source_index.py`](../../../../experiments/issue_333_hh_api_source_index.py).

Корректность проверена так: все 21 внутренних якоря вида `#tag/...`,
встречающихся в самой спецификации (перекрёстные ссылки между методами),
воспроизводятся алгоритмом **посимвольно точно**. Отдельно сверены слаги,
использованные в сносках отчёта: `Chaty`, `Webhook-API`,
`Avtorizaciya-prilozheniya`, `Avtorizaciya-rabotodatelya`,
`Menedzhery-rabotodatelya`, `Vakansii`, `Prosmotr-rezyume`,
`Otklikipriglasheniya-rabotodatelya`.

## Чего проверить не удалось

- Поведение `PUT /common/chats/{chat_id}/participants` на чужом чате (гипотеза
  Г1) — требуется боевой доступ работодателя; в спецификации ответ для этого
  случая не определён.
- Лимиты и квоты методов раздела «Чаты»: `429` в спецификации описан только для
  черновиков вакансий и просмотров резюме (GAP-R10).
