---
status: canonical
version: 1.0
updated: 2026-08-21
temperature: 0.1
owner: G-Ivan-A
source_of_truth: "hybrid-Intelligence-lab"
sync_policy: "explicit spoke sync from pinned Hub commit; локальные дельты помечены комментарием в коде"
scope: mango_ba_prompts
---

# Tools — локальные валидаторы Хаба

Рабочие копии валидаторов Хаба
[`hybrid-Intelligence-lab`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab)
на `source_sha` `6c57eae8a2713566878be715856884b660dd2a16` (issue
[#267](https://github.com/G-Ivan-A/mango_ba_prompts/issues/267)). Source of
truth — Хаб; расхождения устраняются синком, а не свободной правкой копии.
Каждая локальная дельта помечена в коде блоком
`--- Локальная дельта спицы (issue #267) ---` и объяснена ниже.

## Запуск

```bash
make validate                 # оба валидатора в области спицы
./tools/validate-file-naming.sh
./tools/validate-frontmatter.sh <файл|каталог> [...]
```

## Артефакты

| Файл | Источник в Хабе | Назначение |
| --- | --- | --- |
| [`validate-frontmatter.sh`](validate-frontmatter.sh) | [`tools/validate-frontmatter.sh`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/6c57eae8a2713566878be715856884b660dd2a16/tools/validate-frontmatter.sh) | Проверка frontmatter по [`frontmatter-docs-standard.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/6c57eae8a2713566878be715856884b660dd2a16/standards/frontmatter-docs-standard.md). |
| [`validate-file-naming.sh`](validate-file-naming.sh) | [`templates/spoke/tools/validate-file-naming.sh`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/6c57eae8a2713566878be715856884b660dd2a16/templates/spoke/tools/validate-file-naming.sh) (spoke-вариант) | Проверка имён хронологических артефактов по [`file-naming.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/6c57eae8a2713566878be715856884b660dd2a16/standards/file-naming.md). |
| [`file-naming-legacy-allowlist.txt`](file-naming-legacy-allowlist.txt) | — (локальный) | Замороженный список легаси-файлов, созданных до принятия стандарта. |

## Локальные дельты и почему они не противоречат канону

| Дельта | Что сделано | Обоснование |
| --- | --- | --- |
| `validate-frontmatter.sh`: расширен список допустимых полей класса `default` (`owner`, `research_deps`, `source_hub`, `source_sha`, `source_of_truth`, `sync_policy`, `layer`, `full_version`, `related_standard`, `related_issue`). | Только добавление полей; ни одна проверка не ослаблена. | Каждое поле потребляется локальной механикой (`scripts/sync_from_hub.py`, `docs/hub-research-dependencies.md`, `standards/cascading-context-loading-standard.md`), а `frontmatter-docs-standard.md` прямо разрешает поля, которые «a validator, index, template, executable contract, provenance rule or document class consumes». В Хабе этих полей нет, потому что спицевая провенанс-метадата существует только в спице. |
| `validate-file-naming.sh`: allowlist легаси-файлов. | Замороженный список из 26 файлов `docs/adr`, `docs/rfc`, `docs/analysis`, созданных до принятия стандарта. | Для любого нового файла правило действует в полную силу. Переименование легаси-корпуса ломает десятки внутренних и внешних ссылок и вынесено в [`pr-ops/BACKLOG.md`](../pr-ops/BACKLOG.md). Хаб применяет тот же приём к собственному RFC-корпусу. |

## Область проверки frontmatter

`make validate` проверяет корневые файлы, `ai-rules/` и `tools/` — область,
приведённую в соответствие в issue #267. Остальной корпус (`standards/`,
`docs/`, `prompts/`, `kb/`) содержит унаследованный технический долг по
frontmatter; он зафиксирован задачей в [`pr-ops/BACKLOG.md`](../pr-ops/BACKLOG.md)
и не блокирует текущую работу.
