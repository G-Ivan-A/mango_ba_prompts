---
status: draft
version: 0.2
updated: 2026-08-21
ai-generated: true
type: standard
scope: runs
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/123"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/271"
related_artifacts:
  - "runs/README.md"
---

# Стандарт контракта Run

Run — это единица учёта результата выполнения процесса. Контракт вводится как
Phase 0: минимальная локальная структура без полной реструктуризации репозитория.

## Структура

Каждый Run MUST храниться по пути `runs/YYYY/RUN-XXXX/`.

```text
runs/YYYY/RUN-XXXX/
  metadata.yaml
  inputs/
  outputs/
  feedback/
  logs/
```

Каталог `runs/YYYY/RUN-XXXX/` MUST содержать все четыре подкаталога, даже если
часть из них пока пуста.

## Идентификатор

`RUN-XXXX` — монотонный локальный идентификатор из четырёх цифр. Для первой
фазы используются `RUN-0001`, `RUN-0002` и далее. `run_id` в `metadata.yaml`
MUST совпадать с именем каталога.

Номер не кодирует дату, процесс или тип результата. Год берётся из родительского
каталога `YYYY`, а дата фиксируется в `metadata.yaml`.

## metadata.yaml

Минимальные обязательные поля:

| Поле | Правило |
| --- | --- |
| `run_id` | MUST быть вида `RUN-XXXX` и совпадать с каталогом. |
| `process` | MUST называть процесс, сценарий или эксперимент. |
| `version` | MUST фиксировать версию записи или основного результата. |
| `date` | MUST быть датой `YYYY-MM-DD`. |
| `author` | MUST указывать автора фиксации. |
| `model` | MUST указывать модель или `not-recorded`. |
| `status` | MUST указывать состояние результата. |

Разрешённые дополнительные поля:

- `source_paths` — откуда результат перенесён или чем порождён.
- `inputs`, `outputs`, `logs` — ключевые файлы внутри run.
- `related_issues`, `related_artifacts`, `related_runs` — трассировка.
- `metrics` — измеримые показатели прогона (расширение контракта по
  [issue #271](https://github.com/G-Ivan-A/mango_ba_prompts/issues/271)).

### metrics

Блок `metrics` SHOULD заполняться, когда прогон фиксируется как эмпирические данные
для анализа БА, а не только как артефакт. Issue #271 требует токены, длительность,
`eval`/вердикт и `success_rate`.

| Ключ | Правило |
| --- | --- |
| `verdict` | SHOULD совпадать со значением `verdict` в `logs/experiment-log.md` (`works` / `works-with-edits` / `fails`). |
| `success_rate` | Число `0..1`. Если указано, `success_rate_basis` MUST объяснять, что считалось долей. |
| `tokens_*` | Если указаны токены, `token_method` MUST называть способ подсчёта (например `tiktoken:cl100k_base`). |
| `duration_*` | Длительность в секундах; календарное и активное время SHOULD различаться явно. |
| `eval` | Одно-два предложения: что прогон доказал и чего не доказал. |

Прочие ключи внутри `metrics` свободны — блок описывает конкретный прогон.
Развёрнутое обоснование чисел SHOULD жить в `logs/`, а не в `metadata.yaml`.
Пример: [`runs/2026/RUN-0018/metadata.yaml`](../runs/2026/RUN-0018/metadata.yaml) +
[`runs/2026/RUN-0018/logs/metrics.md`](../runs/2026/RUN-0018/logs/metrics.md).

## Назначение подкаталогов

| Подкаталог | Правило |
| --- | --- |
| `inputs/` | SHOULD содержать входные данные, доступные для хранения в репозитории. |
| `outputs/` | SHOULD содержать результаты и промежуточные артефакты выполнения. |
| `feedback/` | SHOULD содержать обратную связь, review notes и решения по результату. |
| `logs/` | SHOULD содержать экспериментальные логи, метрики и трассировку. |

## Миграция существующих результатов

При переносе существующего результата в `runs/` исполнитель SHOULD использовать
`git mv`, чтобы Git сохранил связь с историей файла. Старый путь не должен
оставаться рабочим местом хранения результата.

Если результат раньше состоял из нескольких файлов одного процесса, он SHOULD
попасть в один Run. Пример: кейс multichannel-agent-workload хранит входы,
промежуточные outputs и `logs/experiment-log.md` в `RUN-0011`.

## Критерии соответствия (DoD)

- `runs/README.md` описывает контракт и индекс текущих записей.
- Каждый Run содержит `metadata.yaml`, `inputs/`, `outputs/`, `feedback/`, `logs/`.
- Все обязательные поля `metadata.yaml` заполнены.
- Перенесённые результаты отсутствуют по старым путям.
- `scripts/generate-pages-data.mjs` читает evidence из `runs/`.
- CI вызывает `scripts/validate_issue_123_runs_contract.py`.

Проверка:

```bash
python3 scripts/validate_issue_123_runs_contract.py
```
