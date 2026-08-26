---
status: draft
version: 0.1
updated: 2026-08-26
ai-generated: true
type: input
scope: mango-only
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/329"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/315"
related_artifacts:
  - "runs/2026/RUN-0056/outputs/L2-gap-matrix.md"
---

# Вход прогона RUN-0058 — провенанс исходных данных

Тема прогона: **повторный gap-анализ (re-evaluation) интеграции чатов HH.ru с контакт-центром Mango Office на основе новой документации API**.

Прогон переоценивает выводы [`RUN-0056`](../../RUN-0056/metadata.yaml), сделанные в условиях недоступности OpenAPI-спецификации hh.ru. Старый прогон **не перезаписывается**: он сохраняет ценность как фиксация оценки при отсутствующих данных (требование постановки [#329](https://github.com/G-Ivan-A/mango_ba_prompts/issues/329)).

## Источник 1 — постановка задачи (переоценка)

| Поле | Значение |
| --- | --- |
| Issue | [#329 «[runs] Повторный прогон (Re-evaluation): Gap-анализ интеграции с чатами HH.ru на основе новой документации API»](https://github.com/G-Ivan-A/mango_ba_prompts/issues/329) |
| Что задаёт | Три пути получения сообщений для проверки (отклик → `chat_id`; список чатов; вебхук `CHAT_MESSAGE_CREATED`) и ⚠️ Caveat: чат заводится только у ответственного за вакансию менеджера. |
| Требуемый результат | Обновлённый документ оценки, явный выбор предпочтительного пути, ограничение «ответственный менеджер» отдельным High Risk Gap. |

## Источник 2 — предыдущий прогон RUN-0056

| Поле | Значение |
| --- | --- |
| Прогон | [`runs/2026/RUN-0056`](../../RUN-0056/metadata.yaml) (issue [#315](https://github.com/G-Ivan-A/mango_ba_prompts/issues/315)) |
| Что взято | Формулировки ФТ-01…ФТ-10, вердикты покрытия, разрывы GAP-1…GAP-7, риски R1–R6, вопросы Заказчику. |
| Основание переоценки | [`RUN-0056/feedback/review-notes.md`](../../RUN-0056/feedback/review-notes.md): «Если hh.ru опубликует API чатов, GAP-1, GAP-2 и GAP-7 подлежат переоценке, и вердикт по ФТ-06 может измениться с "Нет" на "Да"». |

Построчная сверка старых и новых вердиктов — [`../logs/delta-vs-RUN-0056.md`](../logs/delta-vs-RUN-0056.md).

## Источник 3 — действующая OpenAPI-спецификация hh.ru (SSOT постановки)

| Поле | Значение |
| --- | --- |
| Точка входа документации | https://api.hh.ru/openapi/redoc (разделы `#tag/Chaty`, `#tag/Webhook-API`) |
| Фактический URL спецификации | https://api.hh.ru/openapi/specification/public (адрес взят из бутстрапа Redoc: `Redoc.init('https://api.hh.ru/openapi/specification/public', …)`) |
| Формат | YAML, `openapi: 3.0.3` |
| Размер на момент прогона, байт | 1266582 |
| SHA-256 на момент прогона | `4349900b6398d462954fadee691305d719e96f3018de929ce069df0e516d383d` |
| Что прочитано | 14 операций тега «Чаты», 23 схемы `ChatsCommon*`, раздел «Webhook API» (9 типов событий, схемы `WebhookAction*`, `WebhookPayload*`, envelope `WebhookSendObjectBaseUser`), операции `get-negotiation-item`, `get-collection-negotiations-list`, `change-negotiation-action`, `put-negotiations-collection-to-next-state`, `get-employer-managers`, `get-manager-accounts-mine` |

Спецификация в репозиторий **не переносится**: это внешний документ объёмом 1,2 МБ, версионируемый на стороне hh.ru. В артефактах прогона цитируются только точечные фрагменты с указанием операции или схемы.

## Источник 4 — ФТ Заказчика (вложение задачи #315)

| Поле | Значение |
| --- | --- |
| Наименование | `765 ФТ Интеграция чатов из HH.ru в КЦ.pdf` |
| Вложение issue | https://github.com/user-attachments/files/31380601/765.HH.ru.pdf |
| Размер, байт | 500386 |
| SHA-256 | `854430ae10754ef205dfa420377e7f0cc5c6e90e6040eaffa5eff156e7369377` (совпал с зафиксированным в RUN-0056) |
| Страниц | 10 |

Файл в репозитории **не хранится** (требование постановки #315: хранение локально на АРМ Пользователя). Использован для дословной сверки формулировок ФТ-01…ФТ-10 и пунктов §4.5.2, §4.6.2, §4.7.2, §4.7.3, §4.8.1.

## Источник 5 — база знаний Mango Office (в репозитории)

| Раздел БЗ | Что взято |
| --- | --- |
| [`kb/processed/mango-lk-manual/sections/186-nastroyka-kanalov-kommunikacii.md`](../../../../kb/processed/mango-lk-manual/sections/186-nastroyka-kanalov-kommunikacii.md) | Перечень каналов МД; канала HeadHunter нет. |
| [`kb/processed/mango-lk-manual/sections/210-avito-rabota.md`](../../../../kb/processed/mango-lk-manual/sections/210-avito-rabota.md) | Паттерн канала «Авито Работа»: OAuth-подключение, приём обращений на сотрудника/группу, переключатель «только отклики с сообщениями», автозавершение диалога. |
| [`kb/processed/mango-cc-manual/sections/26-istoriya-obrascheniy.md`](../../../../kb/processed/mango-cc-manual/sections/26-istoriya-obrascheniy.md) | Отчёт «История обращений» и фильтр по каналу — вход для ФТ-10. |

## Воспроизведение

```bash
# 1. Точка входа документации и фактический URL спецификации
curl -sS https://api.hh.ru/openapi/redoc          # содержит Redoc.init('https://api.hh.ru/openapi/specification/public', …)
curl -sS -o spec.yaml https://api.hh.ru/openapi/specification/public
sha256sum spec.yaml   # 4349900b6398d462954fadee691305d719e96f3018de929ce069df0e516d383d на момент прогона

# 2. Операции раздела «Чаты»
python3 - <<'PY'
import yaml
s = yaml.safe_load(open('spec.yaml'))
for path, item in s['paths'].items():
    for method, op in item.items():
        if isinstance(op, dict) and 'Чаты' in (op.get('tags') or []):
            print(method.upper(), path, op['operationId'])
PY

# 3. ФТ Заказчика
curl -L -o 765-ft-hh.pdf "https://github.com/user-attachments/files/31380601/765.HH.ru.pdf"
sha256sum 765-ft-hh.pdf   # 854430ae10754ef205dfa420377e7f0cc5c6e90e6040eaffa5eff156e7369377
```

## Чего во входе нет

- Нет боевого доступа работодателя к API hh.ru: ни один запрос к чатам не выполнялся, все утверждения — из спецификации, а не из наблюдаемого поведения.
- Нет подтверждения, что метод `put-participant-list` вызывается менеджером, который сам не является участником чата: спецификация описывает `404 «Чат не найден или не доступен текущему пользователю»`, но не определяет, к каким чатам менеджер имеет доступ. Это ключевая непроверенная гипотеза прогона (Г1 в [`../outputs/L3-integration-architecture-notes.md`](../outputs/L3-integration-architecture-notes.md)).
- Нет лимитов и квот на методы чатов: `429` в спецификации описан только для черновиков вакансий и просмотров резюме.
- Нет НФТ: §5 ФТ Заказчика по-прежнему пуст.
