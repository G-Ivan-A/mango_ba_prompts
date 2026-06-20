---
status: experimental
version: 0.1
updated: 2026-05-26
ai-generated: false
type: prompt-experiment
scope: mango-only
related_artifacts:
  - "research/mango/classification-tz.md"
  - "research/mango/classification.md"
---

# Прототип промпта генерации статистики по ТЗ

Версия: 0.1

Дата: 2026-05-26

## Назначение

Этот эксперимент проверяет, можно ли стабильно генерировать отчет по новому
ТЗ: сопоставлять фрагменты ТЗ с классами Mango из
`research/mango/classification.md`, добавлять результаты к накопленной
статистике и сохранять вывод в формате, который можно прочитать человеком и
распарсить автоматикой.

Эксперимент не заменяет классификатор и не меняет правила движения требований.
Он задает прототип системного промпта, формат хранения истории и ручную
проверку на двух ТЗ из корпуса `classification-tz.md`.

## Входные артефакты

| Артефакт | Роль |
| --- | --- |
| `research/mango/classification.md` | Эталонный каталог `Domain -> Capability -> Feature -> Atomic Function`, Product Layer и Commercial Layer. |
| `research/mango/classification-tz.md` | Корпус 30 ТЗ, временные классы A/B/C, сопоставление с эталоном и рекомендации по дополнениям. |
| Текст текущего ТЗ | Новый вход для классификации. В тесте использованы TZ #15 и TZ #22 из исходного корпуса. |
| Предыдущий отчет | Опциональный накопительный отчет с уже посчитанными значениями. Если его нет, счетчики начинаются с нуля. |

## Структура хранения истории

Рекомендуемый каталог для эксперимента:

```text
projects/mango/
└── experiments/
    └── tz-stats/
        ├── prompts/
        │   └── tz-stats-generator.md
        ├── reports/
        │   ├── stats-2026-05-26.md
        │   ├── stats-2026-05-26.json
        │   └── logs/
        │       └── parse-errors.log
        └── runs/
            └── 2026-05-26-tz-15.jsonl
```

Выбор: для прототипа хранить человекочитаемый Markdown и машинный JSON рядом.
Markdown нужен для review в PR, JSON - для накопления счетчиков без повторного
парсинга таблиц. `runs/*.jsonl` сохраняет историю отдельных итераций, чтобы
можно было пересчитать сводный отчет после изменения классификатора.

## Контракт отчета

### Вход

```json
{
  "classification-path": "research/mango/classification.md",
  "previous-report-path": "projects/mango/experiments/tz-stats/reports/stats-2026-05-26.json",
  "current-tz-id": "TZ #15",
  "current-tz-text": "<plain text>",
  "iteration-date": "2026-05-26",
  "classification-version": "3.0"
}
```

`previous-report-path` может отсутствовать. В этом случае агент обязан записать
в лог событие `previous-report-missing` и начать накопление с нуля.

### Основная таблица

| Поле | Тип | Правило |
| --- | --- | --- |
| `class-code` | string | Нормализованный путь `domain.capability` из `classification.md`. |
| `class-name` | string | Русское название класса из Product Layer или Commercial Layer. |
| `total-occurrences` | integer | Предыдущее значение плюс `current-iteration-delta`. |
| `current-iteration-delta` | integer | Для стабильного прототипа: `1`, если класс подтвержден хотя бы одним фрагментом текущего ТЗ; иначе `0`. |
| `source-tz-ids` | array/string | Уникальный список TZ, где класс встречался. |
| `evidence-summary` | string | Короткое описание фрагмента без длинных цитат. |
| `confidence` | enum | `high`, `medium`, `low`. |
| `mapping-status` | enum | `matched`, `partial`, `not-found`, `needs-review`. |

### Машинный блок

После Markdown-таблицы агент выводит JSON с теми же данными:

```json
{
  "report-version": "0.1",
  "classification-version": "3.0",
  "iteration": {
    "current-tz-id": "TZ #15",
    "iteration-date": "2026-05-26"
  },
  "class-stats": [
    {
      "class-code": "voice-ucaas.call-recording",
      "class-name": "Запись разговоров и журналирование",
      "total-occurrences": 1,
      "current-iteration-delta": 1,
      "source-tz-ids": ["TZ #15"],
      "evidence-summary": "ТЗ требует запись всех входящих и исходящих разговоров и хранение записей.",
      "confidence": "high",
      "mapping-status": "matched"
    }
  ],
  "logs": []
}
```

## Правила накопления

1. Читать предыдущий JSON-отчет, если путь передан и файл доступен.
2. Индексировать предыдущие строки по `class-code`.
3. Для текущего ТЗ искать классы сначала в Product Layer, затем в Commercial
   Layer. Временные коды A/B/C из `classification-tz.md` использовать как
   дополнительную подсказку, но не как финальный `class-code`.
4. Если класс найден в текущем ТЗ, выставлять `current-iteration-delta: 1` и
   добавлять `current-tz-id` в `source-tz-ids`.
5. Если один фрагмент подходит к нескольким классам, выбирать ближайший
   функциональный класс, а второй фиксировать как `needs-review`.
6. Если класс не найден в эталоне, не останавливать отчет: создать строку
   `mapping-status: not-found` и записать событие в лог.
7. Не суммировать повторяющиеся фразы внутри одного ТЗ как отдельные
   вхождения, пока не согласована более точная метрика `evidence-count`.

## Формат логирования

`parse-errors.log` ведется построчно:

```text
timestamp | run-id | tz-id | severity | code | message | evidence
```

Коды событий:

| Код | Когда писать |
| --- | --- |
| `previous-report-missing` | Предыдущий отчет не передан или файл недоступен. |
| `previous-report-invalid` | Предыдущий отчет не распарсился как JSON или не содержит `class-stats`. |
| `classification-version-mismatch` | Предыдущий отчет построен по другой версии классификатора. |
| `class-not-found` | В ТЗ найден устойчивый класс, но его нет в `classification.md`. |
| `ambiguous-class` | Фрагмент одинаково подходит нескольким классам. |
| `source-tz-unrecognized` | Не удалось определить номер или источник ТЗ. |

## Системный промпт-прототип

```text
Ты Mango TZ Stats Analyst. Твоя задача - классифицировать новое техническое
задание по эталонному классификатору Mango и обновить накопленную статистику.

Operating mode: structured. Не придумывай классы, если их нет в
classification.md. Если класс явно нужен, но отсутствует, добавь строку со
статусом not-found и событие class-not-found в logs.

Вход:
1. classification-path - путь к research/mango/classification.md.
2. previous-report-path - опциональный путь к предыдущему JSON-отчету.
3. current-tz-id - идентификатор текущего ТЗ, например TZ #15.
4. current-tz-text - полный текст текущего ТЗ.
5. iteration-date - дата запуска.

Порядок работы:
1. Прочитай classification.md и извлеки Product Layer и Commercial Layer.
2. Если previous-report-path доступен, прочитай class-stats; иначе начни с
   пустого списка и добавь log previous-report-missing.
3. Разбей current-tz-text на фрагменты требований: функциональные,
   нефункциональные, интеграционные, compliance и коммерческие.
4. Для каждого фрагмента выбери ближайший class-code формата
   domain.capability или commercial.<field-id>.
5. Для каждого class-code в текущем ТЗ выставь current-iteration-delta = 1.
6. total-occurrences = предыдущее total-occurrences + current-iteration-delta.
7. source-tz-ids = уникальный отсортированный список TZ.
8. Верни Markdown-таблицу и JSON-блок с одинаковыми значениями.

Обязательные поля таблицы:
class-code | class-name | total-occurrences | current-iteration-delta |
source-tz-ids | evidence-summary | confidence | mapping-status

Правила качества:
- evidence-summary должен быть коротким и ссылаться на смысл фрагмента, а не
  копировать длинный текст ТЗ;
- confidence = high только при прямом совпадении термина или устойчивого
  паттерна из classification.md/classification-tz.md;
- confidence = medium при косвенном совпадении;
- не удаляй прежние source-tz-ids;
- не блокируй отчет из-за отсутствующих данных, но логируй проблему;
- после таблицы добавь краткий раздел improvement-suggestions, если видишь
  полезные изменения метрик или процесса.
```

## Тест промпта на TZ #15 и TZ #22

### Тестовые входные данные

Источник TZ #15: `classification-tz.md`, строка корпуса "ВАТС, WFM,
аналитика, коллтрекинг"; исходный файл из issue #9 - "ТЗ пример 15.docx".

Короткие подтверждающие фрагменты TZ #15:

- "закупку облачного сервиса телефонии (виртуальная АТС)";
- "полную и качественную запись всех входящих и исходящих телефонных разговоров";
- "настройки IVR ... направления клиентов";
- "отправка SMS-сообщений клиентам";
- "функционал коллтрекинга";
- "наличие API для кастомной интеграции";
- "доступность не ниже 99,9%";
- "требования Федерального закона ... N 152-ФЗ".

Источник TZ #22: `classification-tz.md`, строка корпуса "Голос+видео
автоматизация экспедитор-клиент"; исходный файл из issue #9 - "ТЗ пример
22.docx".

Короткие подтверждающие фрагменты TZ #22:

- "Автоматизация звонков между экспедитором и клиентом";
- "управлять сценариями голосовой и видео коммуникации";
- "выделенных местных ... мобильных номеров";
- "Автооповещение/IVR";
- "маскирование номеров курьеров";
- "Сервис делает API запрос";
- "звонок записывается";
- "Период оказания услуг: 24 месяца".

### Итерация 1: TZ #15 без предыдущего отчета

| class-code | class-name | total-occurrences | current-iteration-delta | source-tz-ids | evidence-summary | confidence | mapping-status |
| --- | --- | ---: | ---: | --- | --- | --- | --- |
| `voice-ucaas.cloud-pbx` | Виртуальная / облачная АТС | 1 | 1 | TZ #15 | Закупается облачный сервис телефонии/ВАТС. | high | matched |
| `voice-ucaas.call-recording` | Запись разговоров и журналирование | 1 | 1 | TZ #15 | Требуется запись входящих и исходящих разговоров и хранение записей. | high | matched |
| `voice-ucaas.ivr-voice-menu` | Голосовое меню IVR и автоинформирование | 1 | 1 | TZ #15 | Требуется IVR для маршрутизации клиентов и нерабочего времени. | high | matched |
| `digital-channels.sms-messaging` | SMS-рассылки | 1 | 1 | TZ #15 | Требуется отправка SMS и история отправки. | high | matched |
| `analytics.call-tracking` | Коллтрекинг | 1 | 1 | TZ #15 | Требуется коллтрекинг и уникальные номера по источникам трафика. | high | matched |
| `platform.open-api` | Open API, webhook, API для УВК/CRM | 1 | 1 | TZ #15 | Требуется API для кастомной интеграции. | high | matched |
| `security.information-security` | Информационная безопасность | 1 | 1 | TZ #15 | Есть требования к 152-ФЗ, шифрованию, 2FA, логам и IP whitelist. | high | matched |
| `commercial.contract-duration` | Срок договора | 1 | 1 | TZ #15 | Услуга предоставляется на 2 года. | high | matched |

Лог итерации:

```text
2026-05-26T00:00:00Z | tz-15 | TZ #15 | info | previous-report-missing | Previous report was not provided; counters start from zero. | -
```

Оценка: вывод предсказуем и парсируем, но показывает риск смешения Product
Layer и Commercial Layer. Для review полезно явно отделять `commercial.*`
строки или группировать отчет по слоям.

### Итерация 2: TZ #22 с накоплением после TZ #15

| class-code | class-name | total-occurrences | current-iteration-delta | source-tz-ids | evidence-summary | confidence | mapping-status |
| --- | --- | ---: | ---: | --- | --- | --- | --- |
| `voice-ucaas.call-recording` | Запись разговоров и журналирование | 2 | 1 | TZ #15, TZ #22 | В TZ #22 разговоры записываются и доступны заказчику. | high | matched |
| `voice-ucaas.ivr-voice-menu` | Голосовое меню IVR и автоинформирование | 2 | 1 | TZ #15, TZ #22 | TZ #22 требует автооповещение/IVR и DTMF-логику. | high | matched |
| `voice-ucaas.number-management` | Номерная емкость | 1 | 1 | TZ #22 | Требуются выделенные местные и мобильные номера по регионам. | high | matched |
| `voice-ucaas.number-branding` | Маркировка номера, карусельные номера, защита дозваниваемости | 1 | 1 | TZ #22 | Требуется маскирование номеров курьеров и подменные номера. | high | matched |
| `voice-ucaas.video-conferencing` | Видеоконференции | 1 | 1 | TZ #22 | Указаны сценарии видео коммуникации. | medium | matched |
| `platform.open-api` | Open API, webhook, API для УВК/CRM | 2 | 1 | TZ #15, TZ #22 | TZ #22 описывает API-запросы к backend и историю платформы. | high | matched |
| `commercial.contract-duration` | Срок договора | 2 | 1 | TZ #15, TZ #22 | Период оказания услуг - 24 месяца. | high | matched |
| `commercial.industry-vertical` | Вертикаль / use-case | 1 | 1 | TZ #22 | Логистический сценарий доставки: экспедитор-клиент. | high | not-found |

Лог итерации:

```text
2026-05-26T00:00:00Z | tz-22 | TZ #22 | warning | class-not-found | industry-vertical is present in classification-tz.md recommendations but not in the active Commercial Layer catalog. | доставка, экспедитор-клиент
```

Оценка: накопление работает ожидаемо: повторяющиеся классы получают
`total-occurrences: 2`, новые классы - `1`, а отсутствующее поле вертикали не
блокирует отчет. Для следующей итерации нужно согласовать, добавлять ли
`commercial.industry-vertical` в `classification.md` или хранить его только как
аналитический тег отчета.

## Предложения по улучшению

### Улучшения структуры отчета

1. Добавить `coverage-rate`: доля фрагментов текущего ТЗ, сопоставленных с
   классами `classification.md`. Это позволит видеть не только число классов,
   но и полноту покрытия документа.
2. Добавить `new-vs-known`: признак, впервые ли класс появился в текущей
   итерации. Это упростит поиск новых потребностей и gap analysis.
3. Разделить отчет на Product Layer и Commercial Layer, чтобы договорные поля
   не выглядели как продуктовые capabilities.
4. Добавить `evidence-count` после согласования правил подсчета повторов
   внутри одного ТЗ.

### Улучшения процесса

1. Хранить каждый запуск в JSONL, а сводный отчет пересобирать из истории.
   Тогда изменение классификатора можно пересчитать без ручной правки таблиц.
2. Вынести системный промпт в
   `projects/mango/experiments/tz-stats/prompts/tz-stats-generator.md`, а
   отчеты хранить отдельно в `reports/`.
3. Добавить CI-проверку JSON-схемы отчета: обязательные поля, целые счетчики,
   уникальность `class-code`, валидные `mapping-status`.
4. Для GitHub/Jira-интеграции сохранять `source-issue`, `source-attachment` и
   `source-tz-id`, чтобы статистику можно было связать с задачей и файлом.

### Международные практики

| Источник | Как применить в эксперименте |
| --- | --- |
| IIBA BABOK Guide v3, техника Metrics and KPIs: https://www.iiba.org/knowledgehub/business-analysis-body-of-knowledge-babok-guide/10-techniques/10-28-metrics-and-key-performance-indicators-kpis/ | Использовать `coverage-rate`, `new-vs-known`, `confidence` и trend metrics как управляемые метрики БА. |
| ISO/IEC 25010:2023: https://www.iso.org/standard/78176.html | Использовать качественные характеристики продукта как основу для NFR-группировки: надежность, безопасность, удобство, сопровождаемость. |
| TM Forum Open APIs: https://www.tmforum.org/open-digital-architecture/implementation/open-apis/ | Нормализовать интеграционные требования и API-события в отдельный слой, связанный с Product/Service/Customer domains. |
| UNSPSC в UNGM: https://www.ungm.org/Public/UNSPSC | Использовать товарно-сервисные коды для закупочного и внешнего сравнения требований. |

## Вопросы для согласования

1. Подходит ли правило `current-iteration-delta = 1 на класс в одном ТЗ`, или
   нужно считать каждое отдельное evidence-вхождение внутри документа?
2. Нужен ли основной каталог хранения в `projects/mango/experiments/tz-stats/`,
   или отчеты должны жить в `projects/mango/docs/reports/` после стабилизации?
3. Нужно ли добавить `industry-vertical` в активный Commercial Layer
   `classification.md`, или оставить его только аналитическим тегом отчета?
4. Должен ли финальный отчет всегда содержать JSON-блок, или для review
   достаточно Markdown при наличии отдельного `.json` файла?
5. Какие метрики добавить в следующей итерации: `coverage-rate`,
   `evidence-count`, trend by domain, confidence distribution или список
   unresolved mappings?
