## Кратко

Issue #444 просит проверить готовность, затем продолжить BL-156 или BL-157.

- **BL-157б не готова.** Ей нужен BL-156а `DONE` и первый прогон BL-111. Для BL-111 пока нет Р-01, задачи и БА.
- **Поэтому исполнен этап BL-156а:**
  - реестр справочников 0.4 на runtime `f31dcde3`;
  - 11 черновиков пересобраны, Ш-2 читает каталог по звену М-4;
  - 14 промптов v0.1 ссылаются на runtime по SHA;
  - прогон golden set Ш-В **RUN-0081**.
- **Тип гейта в `prompts/` не опубликован.** По правилу DEC-427-11, заданному до прогона, A показал ядро 9/11 против 10/11 RUN-0079. Правка перенесена в этап BL-156б.
- **Решения владельца из issue исполнены:**
  - по PR #17 принят строгий вариант PR #21;
  - Human Review кейсов `contact-center` — задача BL-165;
  - маппинг RUN-0074 — задача BL-166.

Ссылки:
- постановка (WBS, 12 граничных случаев, обходы): [`experiments/issue_444/task-statement.md`](https://github.com/konard/G-Ivan-A-mango_ba_prompts/blob/issue-444-be981fac3f23/experiments/issue_444/task-statement.md);
- разбор готовности: [`docs/analysis/2026-11-04-bl-156-readiness-check-444.md`](https://github.com/konard/G-Ivan-A-mango_ba_prompts/blob/issue-444-be981fac3f23/docs/analysis/2026-11-04-bl-156-readiness-check-444.md).

Режим — гибридный (из issue).

## Проверка готовности (RFC-RT-001, раздел 13.1)

| № | Условие | Факт | Итог |
| --- | --- | --- | --- |
| Г-9 | РТ-3, РТ-4, РТ-6 и компиляция ХАБ-1 слиты в runtime | [runtime PR #21](https://github.com/G-Ivan-A/mango-ba-ai-runtime/pull/21) слит 2026-11-04T14:55Z, `f31dcde3` = `main` runtime | Да |
| Г-10 | Пути и версии реестра на SHA (ТС-2, ТС-3) | 13 путей, 11 версий; `docs/kb` не менялась | Да |
| Г-11 | Каталог runtime = каталог спицы | 353 узла, id, уровни и родители совпадают, дрейфа `lifecycle` нет | Да. Раздел 2.1 реестра снят |
| Г-12 | Golden set трёх классов в строгой форме | 7 / 6 / 5 кейсов, `atomic_function` — всегда id каталога, функция вне каталога — в `declared_function` | Да, с оговоркой: `structural_only: true`, `confirmed_by: none` (→ BL-165) |
| Г-13 | Глоссарии РТ-4 | 8 / 6 / 4 пары `confusable_with` | Да |
| Г-14 | PR #439 слит | 2026-11-04T13:36Z | Да |

- Лог: [`runtime-readiness.log`](https://github.com/konard/G-Ivan-A-mango_ba_prompts/blob/issue-444-be981fac3f23/experiments/issue_444/runtime-readiness.log).
- Снимок трёх репозиториев: [`cross-repo-state.log`](https://github.com/konard/G-Ivan-A-mango_ba_prompts/blob/issue-444-be981fac3f23/experiments/issue_444/cross-repo-state.log).
- Перед финалом проверено ещё раз: `main` runtime по-прежнему `f31dcde3` (ГК-12).

## Решение по PR #17 и комментарий к PR #21 (RFC-RT-001, раздел 13.2)

Расхождение кажущееся:
- [комментарий владельца к runtime PR #21](https://github.com/G-Ivan-A/mango-ba-ai-runtime/pull/21#issuecomment-6633420940) просил перенести в #21 недостающую логику #17;
- issue #444 говорит, что логика #17 «не интегрируется».

Сверка по коммитам runtime показывает, что речь о разных частях #17:

- **Перенесено в #21:**
  - норма PT-5 (`09cc684`);
  - проверки `check_taxonomies` 6–11 и `check_golden` 2–8 (`09cc684`, `23d2a4b`);
  - тесты привязки к каталогу `tests/test_catalog_binding.py` (`449d772`);
  - очистка `.pyc` (`11fad36`).
- **Отвергнута только форма #17:** маркер-исключение `# намеренно вне каталога` в `atomic_function`. В #21 функция кейса — всегда id каталога, а объявленная функция вне каталога лежит в `declared_function`.

Спица в runtime ничего не меняет: строгая форма уже в `main`.

## Что изменено

- **Реестр справочников** [`standards/bcreq-runtime-references.md`](https://github.com/konard/G-Ivan-A-mango_ba_prompts/blob/issue-444-be981fac3f23/standards/bcreq-runtime-references.md) 0.4:
  - срез `f31dcde3`;
  - И-5, И-6 — «Да»;
  - З-3, З-4 перенесены в снятые, id не переиспользуются;
  - раздел 2.1 снят;
  - раздел 2.2 — звено М-4: каталог для раздела 2.2 BCREQ;
  - РТ-1, РТ-3, РТ-4, РТ-6 — со ссылками на PR runtime;
  - долг ссылок на `main` (раздел 7) закрыт.
- **Черновики** `prompts/drafts/` пересобраны на реестре 0.4:
  - сборщик вставляет М-4 только в Ш-2;
  - базовый стандарт: БС-21 перечисляет только З-2.
- **14 промптов v0.1** в `prompts/`: три ссылки `blob/main` закреплены SHA. Это правка ссылок без поведения (правило RUN-0080).
- **RUN-0081** — [отчёт](https://github.com/konard/G-Ivan-A-mango_ba_prompts/blob/issue-444-be981fac3f23/runs/2026/RUN-0081/outputs/golden-set-report.md), [`metrics.json`](https://github.com/konard/G-Ivan-A-mango_ba_prompts/blob/issue-444-be981fac3f23/runs/2026/RUN-0081/outputs/metrics.json):

  | Версия | Сдано | Ядро | Ложные дефекты |
  | --- | --- | --- | --- |
  | A: v0.1 + тип гейта + SHA | 56/62 | **9/11** | 0/10 |
  | D: черновик на реестре 0.4 | 51/62 | **9/11** | 0/10 |
  | Опора RUN-0079 | 49/62 | 10/11 | 0/10 |

  - **Решение:** 15 подстановок типа гейта сняты (`prompt-typing.json` — «не применена»), ссылки по SHA остаются, черновики — в `prompts/drafts/`.
  - Провал ядра GS-BCREQ-01 — по K5, на той же фразе, которую судья RUN-0080 зачёл. Это довод в пользу разброса судьи, но оценку меняет человек (Р-03), а не автор правки.
- **RFC-RT-001 0.4**, раздел 13:
  - готовность;
  - решение по PR #17;
  - что исполнено;
  - задачи BL-165, BL-166, BL-156б;
  - статусы шагов раздела 11 обновлены.
- **Бэклог:**
  - BL-156 — `review` (этапы BL-156а / BL-156б);
  - BL-157 — `deferred (triggered)` (BL-157а `DONE`);
  - BL-163 — `DONE`;
  - новые BL-165 и BL-166 с карточками и источниками.
- **Сопутствующее:**
  - отчёт BL-156 0.3, реестр RFC 0.17, карта артефактов 0.15, CHANGELOG 0.27;
  - **сайт 2.1.3**: данные перегенерированы, RUN-0081 в проверках Ш-В;
  - допуск #395 для `standards/README.md` с причиной `#444`.

## Движение по бэклогу

| Шаг | Что | Статус |
| --- | --- | --- |
| Предшествующий | BL-163 (PR #443) и runtime PR #21 (РТ-3, РТ-4, РТ-6) | `review` → `DONE`; `merged` |
| **Закрывается этим PR** | **BL-156а**: реестр 0.4, черновики, ссылки по SHA, RUN-0081 | `TODO` → `review` |
| Открывает | BL-157б: режим `by-test` и первый прогон BL-111 | `deferred (triggered)` до BL-156а `DONE` и BL-111 |
| Открывает | BL-156б: публикация черновиков и типа гейта | `deferred (triggered)` до П-Ш-В и замера с повторами |
| Открывает | BL-165, BL-166 (решения владельца в #444) | `deferred (triggered)` |

## WBS и доказательства (DoD)

| № | Работа | Итог и доказательство |
| --- | --- | --- |
| W-1 | Состояние трёх репозиториев | ✅ [`cross-repo-state.log`](https://github.com/konard/G-Ivan-A-mango_ba_prompts/blob/issue-444-be981fac3f23/experiments/issue_444/cross-repo-state.log) |
| W-2 | Готовность на клоне `f31dcde3` | ✅ [`runtime_readiness.py`](https://github.com/konard/G-Ivan-A-mango_ba_prompts/blob/issue-444-be981fac3f23/experiments/issue_444/runtime_readiness.py), [лог](https://github.com/konard/G-Ivan-A-mango_ba_prompts/blob/issue-444-be981fac3f23/experiments/issue_444/runtime-readiness.log), [разбор](https://github.com/konard/G-Ivan-A-mango_ba_prompts/blob/issue-444-be981fac3f23/docs/analysis/2026-11-04-bl-156-readiness-check-444.md) |
| W-3 | Реестр 0.4 и валидаторы #430, #432, #434 | ✅ реестр, валидаторы зелёные |
| W-4 | RFC-RT-001 0.4: PR #17, шаги раздела 11 | ✅ раздел 13 |
| W-5 | БС-21, М-4 в сборщике, пересборка | ✅ `build_bcreq_step_prompts.py --check` в валидаторе #438 |
| W-6 | Тип гейта и ссылки по SHA в 14 промптах | ✅ ссылки по SHA. ⏭️ тип гейта снят после RUN-0081 → **BL-156б** |
| W-7 | RUN-0081 | ✅ `runs/2026/RUN-0081/`, метрики пересчитывает валидатор #438 |
| W-8 | Сайт 2.1.3 | ✅ `site/data/*.json`, валидаторы #423, #74 |
| W-9 | Бэклог | ✅ BL-156, BL-157, BL-163, BL-165, BL-166; валидаторы #418, #438 |
| W-10 | CHANGELOG, реестр RFC, карта артефактов | ✅ |
| W-11 | Мутации, `validate_all` | ✅ мутации 6/6 ([лог](https://github.com/konard/G-Ivan-A-mango_ba_prompts/blob/issue-444-be981fac3f23/experiments/issue_444/mutation-check.log)); `validate_all --full`: 88/88 ([лог](https://github.com/konard/G-Ivan-A-mango_ba_prompts/blob/issue-444-be981fac3f23/experiments/issue_444/validate-full.log)) |
| W-12 | Описание PR | ✅ |
| W-13 | Публикация 11 черновиков в `prompts/` | ⏭️ **BL-156б**: DEC-427-11 — 10 черновиков не измерены, D в RUN-0081 хуже A |

## Проверки

- `RUNTIME_CLONE=/tmp/rt444 python3 scripts/validate_all.py --full` — 88 валидаторов, 0 провалов.
- Без `RUNTIME_CLONE` проверки клона пропускаются, остальное зелёное.
- `make validate-frontmatter validate-file-naming validate-structure validate-onboarding validate-full` — те же цели, что в `.github/workflows/validate.yml` — зелёные.
- [`mutation_check.py`](https://github.com/konard/G-Ivan-A-mango_ba_prompts/blob/issue-444-be981fac3f23/experiments/issue_444/mutation_check.py) ловит 6 из 6 порч. Каждая из них делает валидатор красным:
  - SHA реестра;
  - М-4 в черновике Ш-2;
  - ссылка промпта на `main`;
  - `TYPING_APPLIED = True` без прогона;
  - ссылка раздела 13 RFC;
  - строка BL-165.
- **CI:** workflow на этом PR не запускался. Последний запуск `validate.yml` в репозитории — 2026-08-22. У слитых #439 и #443 тоже 0 проверок, так что дело, вероятно, в настройке Actions для PR из форка. Локальный прогон тех же целей — выше.

## ⚠️ Экспертные предупреждения (Industry Practice Alert, не блокируют)

1. **Eval before release.**
   - **Запрос:** «Готово, когда 11 промптов „по тесту“ в `prompts/`» (карточка BL-156).
   - **Практика:** изменение промпта выпускают после оценки на эталонном наборе.
   - **Действие:** golden set есть только для Ш-В, поэтому BL-156 разделена на этапы а/б. Если нужна буквальная публикация, напишите «Подтверждаю с учетом риска».
2. **Разброс LLM-судьи.**
   - Три замера A на почти одном тексте: 49, 55, 56; ядро 10, 10, 9.
   - Правило «ядро не меньше» при N = 1 реагирует на смену одного кейса. Практика — повторы или несколько судей и решение по медиане.
   - Правило не отменено задним числом. Требование замера с повторами записано в BL-156б.

## Рекомендуемые следующие шаги

1. **Слить PR #445** (молчание = согласие). После слияния BL-156а → `DONE`, и разблокируется BL-157б.
2. **Р-03 и замер с повторами (BL-156б).** Нужно 3 повтора или 3 судьи на A и D, примерно 0,7 млн токенов. Без этого решение о типе гейта и П-Ш-В остаётся лотереей на одном кейсе.
3. **Второе чтение GS-BCREQ-01 и GS-BCREQ-12 человеком.** Все провалы ядра трёх прогонов — по K5 (правка добавляет поведение). Это дешевле нового прогона и даёт материал для Р-03.
4. **BL-157б — после старта BL-111.** До первого прогона на реальном входе 10 черновиков генерации не с чем сравнивать.
5. **BL-165 и BL-166 — по триггеру,** не сейчас. Кейсы runtime пока не входят ни в одну метрику спицы.

Fixes #444
