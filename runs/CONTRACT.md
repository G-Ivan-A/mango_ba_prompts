---
status: draft
version: 0.3
updated: 2026-06-24
ai-generated: true
type: contract
scope: runs
contract_id: runs-contract
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/123"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/133"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/217"
related_artifacts:
  - "standards/runs-contract-standard.md"
---

# runs-contract

Контракт записи `runs/`.

Каждая запись живёт по схеме `runs/YYYY/RUN-XXXX/`.

```text
runs/
└── YYYY/
    └── RUN-XXXX/
        ├── metadata.yaml
        ├── inputs/
        ├── outputs/
        ├── feedback/
        └── logs/
            └── <run-type>-log.md
```

## metadata.yaml

`metadata.yaml` содержит минимальный набор полей:

| Поле | Обязательное | Значение |
| --- | --- | --- |
| `run_id` | да | Идентификатор вида `RUN-XXXX`, совпадает с именем папки. |
| `process` | да | Процесс или сценарий, который выполнялся. |
| `run_type` | да | Тип run'а: `experiment`, `generation`, `validation`, `documentation`, `business-task`. |
| `version` | да | Версия записи или основного результата. |
| `date` | да | Дата выполнения или фиксации результата в формате `YYYY-MM-DD`. |
| `author` | да | Автор фиксации результата: БА, человек+LLM или агент. |
| `model` | да | Использованная модель; если не записана, указывается `not-recorded`. |
| `status` | да | Состояние результата: например `draft`, `experimental`, `success`, `partial-success`, `works-with-edits`. |

Дополнительные поля разрешены: `source_paths`, `inputs`, `outputs`, `logs`,
`related_issues`, `related_artifacts`, `related_runs`.

## Типы run'ов (`run_type`)

| `run_type` | Назначение | Канонический Markdown-лог | Примеры |
| --- | --- | --- | --- |
| `experiment` | Проверка гипотез, A/B тесты. | `logs/experiment-log.md` | `RUN-0001`, `RUN-0009` |
| `generation` | Создание артефактов: ТЗ, US, UC, FR. | `logs/generation-log.md` | `RUN-0002`, `RUN-0003`, `RUN-0007` |
| `validation` | Аудит и проверка качества. | `logs/validation-log.md` | `RUN-0004`, `RUN-0005`, `RUN-0008` |
| `documentation` | Фиксация сессий и отладка. | `logs/documentation-log.md` | `RUN-0006` |
| `business-task` | Решение конкретных BCREQ-задач. | `logs/business-task-log.md` | `RUN-0010`, `RUN-0011`, `RUN-0012`, `RUN-0013` |

## Обязательное логирование

Markdown-лог обязателен для каждого факта прохода: успешного, неуспешного или частично успешного.
Лог создаётся в `logs/` сразу при фиксации run'а, даже если основной результат
не был получен.

Правила:

- имя основного лога выбирается по таблице `run_type`;
- основной лог MUST быть Markdown-файлом `.md`;
- `metadata.yaml` MUST содержать `logs:` со ссылкой на основной Markdown-лог;
- лог MUST фиксировать ход выполнения, ключевые действия, блокеры и итоговый
  статус;
- `.gitkeep` не считается логом и не заменяет Markdown-лог;
- дополнительные технические журналы (`.log`, `.json`, трассировки) разрешены,
  но не заменяют основной Markdown-лог.

## Назначение подкаталогов

| Подкаталог | Что хранится |
| --- | --- |
| `inputs/` | Сырой вход, выдержки БЗ, исходные данные, которые можно хранить в репозитории. |
| `outputs/` | Итоговые и промежуточные артефакты выполнения процесса. |
| `feedback/` | Комментарии ревью, обратная связь, решения по результату. |
| `logs/` | Обязательный Markdown-лог прохода, метрики, трассировка выполнения, технические журналы. |

Если подкаталог пока пустой, он сохраняется через `.gitkeep`, чтобы структура
каждого run была одинаковой.

## Валидация

```bash
python3 scripts/validate_issue_123_runs_contract.py
python3 scripts/validate_issue_133_runs_restructure.py
python3 scripts/validate_issue_217_runs_log_contract.py
```
