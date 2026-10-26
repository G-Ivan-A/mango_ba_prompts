---
status: draft
version: 0.1
updated: 2026-10-26
ai-generated: true
type: review
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/393"
---

# Фильтры BCREQ: маппинг и проверка

Изменение подготовлено в
[PR #394](https://github.com/G-Ivan-A/mango_ba_prompts/pull/394).
Основа —
[контракт стадий](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/contracts/bcreq-stage-gates.md)
и неизменённая
[таксономия 13 операций](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/taxonomy.md).

## Причина и решение

У всех 14 BCREQ-промптов отсутствовали теги процесса и операции во frontmatter.
Генератор брал старые процессы из README/таксономии. Каскад использовал общую
таблицу процессов вместо фактических промптов, работал только в одну сторону,
а счётчики показывали общий размер каталога.

Воспроизведение до изменения: выбрать `Risk Analysis` — счётчик
«Документирование» равен 4 при одном подходящем промпте. Выбрать
«Моделирование» — «Статистика» остаётся доступной, хотя результатов нет.
[Браузерная регрессия](https://github.com/konard/G-Ivan-A-mango_ba_prompts/blob/issue-393-f9f3cbe0f7ca/experiments/issue_393/browser-check.cjs)
с `--before` воспроизводит оба случая на исходном дереве.

Теперь `operation` и `processes` берутся из frontmatter. `processes` — YAML
inline-список в JSON-совместимом формате. Неизвестная операция, пустой список,
дубли и неизвестная стадия останавливают генератор с именем файла. Шесть
текстовых стадий каталога отделены от старой карты процессов: таксономия,
паттерны и прямые hash-маршруты сохранены. Это разрешённое issue #393
исключение для BCREQ к общему правилу центрального маппинга.

Счётчик процесса учитывает операции, поиск, набор и режим; счётчик операции —
процессы, поиск, набор и режим. Собственный выбор группы исключён из подсчёта,
чтобы несколько значений оставались альтернативами (ИЛИ). Между группами — И.
Нулевые неподходящие значения видны, но выключены; выбранное значение всегда
можно снять, включая нулевой результат поиска. Один UC-файл считается один раз
в результатах и в каждой из двух стадий. Блоки «Набор»/«Режимы» и их прежние
счётчики не менялись. Отладка выключена; для трассировки выбора можно задать
`window.MANGO_DEBUG_FILTERS = true` в консоли браузера.

## Аудит операций и стадий

Все 14 прежних **основных** когнитивных операций соответствуют назначению
промптов и контракту стадий. Семантических переименований операций не требуется:
исправлены отсутствующие frontmatter-теги и устаревшее отнесение к процессам.
Фильтр по-прежнему использует основную операцию промпта, включая стадийные
oneshot-промпты; наличие внутренних подопераций не меняет этот контракт.
Промптов без подходящей стадии не найдено.

| Промпт | `processes` | Добавленный `operation` | Основание |
| --- | --- | --- | --- |
| [Ш-0](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md) | Конституция и управление | `governance` | Правила, статусы и жизненный цикл |
| [Ш-1](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-context-understanding-stepwise.md) | Приём и контекст | `understanding` | Глоссарий, цели, границы и вопросы |
| [Ш-2](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-products-impact-analysis-stepwise.md) | Приём и контекст | `impact_analysis` | Затронутые продукты, модули и стейкхолдеры |
| [A-IN](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-in-understanding-oneshot.md) | Приём и контекст | `understanding` | Контекст до Г-IN |
| [Ш-3](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-fr-documentation-stepwise.md) | Требования и предварительное согласование | `documentation` | Раздел ФТ, в том числе вариант `new` |
| [Ш-4](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-nfr-documentation-stepwise.md) | Требования и предварительное согласование | `documentation` | Раздел НФТ |
| [Ш-5/Ш-8](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-uc-modeling-stepwise.md) | Требования и предварительное согласование; Дизайн решения и оценка | `modeling` | Один файл, прогоны 1/2 в разных стадиях |
| [A-CORE](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-core-documentation-oneshot.md) | Требования и предварительное согласование | `documentation` | Документирование ФТ/НФТ/UC до Г-С1 |
| [Ш-6](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-orr-solution-design-stepwise.md) | Дизайн решения и оценка | `solution_design` | Проектирование ОРР L1/L2 |
| [Ш-7](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constraints-documentation-stepwise.md) | Дизайн решения и оценка | `documentation` | Документирование ограничений реализации |
| [Ш-9](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-extra-risk-analysis-stepwise.md) | Дизайн решения и оценка | `risk_analysis` | Риски, зависимости и план приёмки |
| [A-WORK](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-work-solution-design-oneshot.md) | Дизайн решения и оценка | `solution_design` | Решение и оценка до Г-W |
| [Ш-В](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-review-validation-oneshot.md) | Валидация второй ролью | `validation` | Независимая проверка документа |
| [Ш-С](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-scenarios-modeling-oneshot.md) | Сценарии вне документа | `modeling` | Независимые US/UC по контексту |

В меню удалены только три ссылки. Ссылка «Отчёты» не была связана с логикой
входа: общий gate подключается на самих страницах отчётов. Меню содержит
Каталог, Дашборд, Процессы, выход (⏻), тему (◐).

## Проверка

Итог: генератор выполнен; `make validate-full` — 64 валидатора, 0 из кэша,
0 провалов. Регрессии метаданных/каскада и оба способа браузерной проверки
пройдены локально. Actions не включались, workflow-файлы не менялись.

```bash
node scripts/generate-pages-data.mjs
python3 scripts/test_issue_393_site.py
make validate-full
NODE_PATH=/path/to/node_modules node experiments/issue_393/browser-check.cjs
```

Нужны Node.js, Python 3, установленный Playwright и его Chromium. Браузерный
тест использует локальные файлы на перехваченном каноническом origin; тестовый
пароль/хэш существует только в памяти и не меняет конфигурацию сайта.
Сетевые запросы к внешнему виджету изолированы. Каждый тестовый браузер
закрывается в `finally`. Playwright MCP отдельно проверил реальный сервер
`python3 -m http.server 8765 --bind 127.0.0.1 --directory site`: шесть стадий,
обратный каскад, пять элементов меню, два блока, 11 кнопок копирования,
открытие отчёта в сессии и редирект на вход без сессии. Браузер и сервер закрыты.
Внешний Mango-виджет при localhost-проверке выдаёт прежние предупреждения
шрифтов/CORS; код виджета не затронут.

[Автоматические тесты](https://github.com/konard/G-Ivan-A-mango_ba_prompts/blob/issue-393-f9f3cbe0f7ca/scripts/test_issue_393_site.py)
проверяют все 14 маппингов, 13 операций, побайтную сохранность исходников после
удаления только двух новых полей, а также исполняют реальные функции app.js
для прямого/обратного каскада, ИЛИ/И, поиска, режима, набора и снятия нулевого
выбора. Тест автоматически обнаруживается `make validate-full`.
Существующая проверка уроков #391 сохраняет прежние гарантии, исключая только
два новых поля frontmatter. Старые валидаторы обновлены под новые требования
меню и шести стадий; маршруты и gate продолжают проверяться.

Браузерный тест проверяет все шесть процессов и все восемь операций с
промптами, считает ожидаемые результаты по данным, проверяет 14 копирований
каталога и 11 копирований процесса (точный буфер), оба блока «Процессов»,
Дашборд, тему, мобильный viewport, поиск/сброс, BCREQ/режимы, прямые старые
hash-маршруты, выход и три маршрута отчётов с входом/без входа.

Снимки:

| До | После |
| --- | --- |
| ![До](https://github.com/konard/G-Ivan-A-mango_ba_prompts/blob/issue-393-f9f3cbe0f7ca/docs/screenshots/issue-393/before-catalog.png?raw=true) | ![После](https://github.com/konard/G-Ivan-A-mango_ba_prompts/blob/issue-393-f9f3cbe0f7ca/docs/screenshots/issue-393/after-catalog.png?raw=true) |

[Процесс → операции](https://github.com/konard/G-Ivan-A-mango_ba_prompts/blob/issue-393-f9f3cbe0f7ca/docs/screenshots/issue-393/after-process-cascade.png?raw=true),
[операции → процессы](https://github.com/konard/G-Ivan-A-mango_ba_prompts/blob/issue-393-f9f3cbe0f7ca/docs/screenshots/issue-393/after-operation-cascade.png?raw=true),
[два блока](https://github.com/konard/G-Ivan-A-mango_ba_prompts/blob/issue-393-f9f3cbe0f7ca/docs/screenshots/issue-393/after-processes.png?raw=true),
[мобильный вид](https://github.com/konard/G-Ivan-A-mango_ba_prompts/blob/issue-393-f9f3cbe0f7ca/docs/screenshots/issue-393/after-mobile.png?raw=true),
[локальный Playwright MCP](https://github.com/konard/G-Ivan-A-mango_ba_prompts/blob/issue-393-f9f3cbe0f7ca/docs/screenshots/issue-393/after-local-mcp.png?raw=true).

## Ручной деплой владельцем

Публикация не входит в действия агента: issue #393 запрещает push в gh-pages
и включение Actions. В PR передаётся этот чек-лист владельцу:

- [ ] После review выбрать проверенный исходный коммит PR и выполнить генератор,
  `make validate-full` и браузерный тест.
- [ ] В отдельном checkout upstream `gh-pages` заменить содержимое корня
  **содержимым** `site/`, сохранив `data/`, `reports/`, gate и конфигурацию пароля;
  добавить `.nojekyll`.
- [ ] Сверить diff с исходным коммитом, сделать обычный коммит и push в
  `gh-pages` учётной записью владельца, сохранив историю. Actions не включать
  и workflow не запускать.
- [ ] На
  [каноническом сайте](https://g-ivan-a.github.io/mango_ba_prompts/)
  проверить вход, шесть стадий без старых значений, UC в двух стадиях, оба
  направления каскада/счётчики, пять элементов меню, BCREQ/режимы, копирование
  и два блока «Процессов».
- [ ] В сессии и без сессии проверить
  [список отчётов](https://g-ivan-a.github.io/mango_ba_prompts/reports/index.html),
  [RUN-0060](https://g-ivan-a.github.io/mango_ba_prompts/reports/run-0060/index.html)
  и [подробный отчёт](https://g-ivan-a.github.io/mango_ba_prompts/reports/run-0060/detailed-gap-report.html),
  затем выход и тему. Подтвердить публикацию отдельно от локальной проверки.

Общая процедура доступа:
[site-access](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/site-access.md).
