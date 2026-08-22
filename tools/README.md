---
status: canonical
version: 1.1
updated: 2026-08-22
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
make validate                 # оба валидатора Хаба + протокол онбординга
./tools/validate-file-naming.sh
./tools/validate-frontmatter.sh <файл|каталог> [...]
```

Оба скрипта входят и в общий набор валидаторов репозитория — см. следующий
раздел: обычный цикл работы построен вокруг `make validate-fast`.

## Общий раннер валидаторов (issue #299)

[`scripts/validate_all.py`](../scripts/validate_all.py) запускает **все**
валидаторы репозитория: `scripts/validate_issue_*.py`, `scripts/test_*.py` и
`tools/validate-*.sh`. Реестра нет — набор обнаруживается по маске, поэтому
новый валидатор подхватывается и локально, и в CI без правки каких-либо
списков.

### Два уровня проверки

| Уровень | Команда | Когда | Время |
| --- | --- | --- | --- |
| Быстрый (инкрементальный) | `make validate-fast` | перед каждым коммитом, после каждой правки | 0.4 с, если ничего не менялось; 0.6–1.7 с после правки файла |
| Полный | `make validate-full` | перед пушем; так же работает CI | ~10 с (кэш игнорируется) |

Вспомогательное: `make validate-list` — перечень обнаруженных валидаторов,
`make validate-cache-clear` — удалить кэш. У самого скрипта есть флаги
`--only <подстрока>` (повторяемый), `--jobs N`, `-v` (вывод валидаторов),
`--no-cache`.

### Как это работает

Быстрый уровень не угадывает, что перепроверять, и ничего не требует от автора
валидатора. Валидатор запускается под трассировщиком
[`scripts/_validator_trace.py`](../scripts/_validator_trace.py), который
записывает **фактически** прочитанные файлы, проверенные пути и перечисленные
каталоги. Множество этих зависимостей и хэши их содержимого (sha256)
сохраняются в `.validate-cache/entries/<валидатор>.json`. При следующем запуске
валидатор пропускается, только если каждая зависимость совпала по содержимому.

Следствия, о которых стоит знать:

- **Ключ — содержимое, а не `mtime`.** `touch` и `git checkout` туда-обратно не
  вызывают перепрогона; правка файла — вызывает.
- **Кэшируются только успехи.** Упавший валидатор падает при каждом запуске,
  пока причина не устранена: кэш не может замаскировать красный результат.
- **Отсутствие файла — тоже зависимость.** Появление файла, отсутствие которого
  проверял валидатор, инвалидирует запись.
- **Перечень каталога — тоже зависимость.** Новый файл в обходимом каталоге
  инвалидирует тех, кто этот каталог обходит.
- **Файл самого валидатора — его зависимость.** Правка кода проверки
  инвалидирует его запись.
- **Shell-валидаторы непрозрачны** для трассировки: для них объявлен корень
  области (`SH_SCOPES` в `validate_all.py`), который разворачивается
  динамически. Неизвестный дочерний процесс делает прогон «непрозрачным», и
  зависимостью становится отпечаток всего дерева — безопасный отказ в сторону
  лишнего перезапуска.

### Управление кэшем

`.validate-cache/` лежит в корне репозитория и **не версионируется**
(`.gitignore`). Он полностью производный: удаление ничего не ломает, следующий
прогон соберёт его заново.

```bash
make validate-cache-clear              # удалить кэш целиком
python3 scripts/validate_all.py --no-cache   # прогон без чтения и записи кэша
python3 scripts/validate_all.py --full       # игнорировать кэш, но обновить его
```

Испорченный или обрезанный файл кэша трактуется как промах, а не как ошибка:
проверка просто выполняется заново. Записи атомарны (`tmp` + `os.replace`) и
раздельны по валидаторам, поэтому два раннера могут работать одновременно —
например, фоновый прогон и ручной запуск (проверено
[`scripts/test_validate_all.py`](../scripts/test_validate_all.py)).

Полный разбор — что мерялось, какие варианты рассматривались и какие граничные
случаи проверены — в
[`docs/analysis/2026-08-22-validator-optimization.md`](../docs/analysis/2026-08-22-validator-optimization.md).

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
