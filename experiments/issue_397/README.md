# Issue 397: воспроизводимые доказательства исследования

[Отчёт](https://github.com/konard/G-Ivan-A-mango_ba_prompts/blob/issue-397-97e1903ee376/docs/analysis/2026-10-28-bcreq-evolution-failure-analysis.md)
восстанавливает требования Founder и проверяет пять гипотез на СПЛИТ и 1131.
Это исследовательский пакет: он не меняет действующие политики, промпты,
сайт или runtime и не вызывает LLM/API моделей. Все скрипты — Python stdlib.

## Файлы и границы

- `evidence.md` — читаемые дословные требования и методологические выдержки.
  `evidence.json` — их provenance: ID, UTC, роль, хэш полного ответа,
  SHA-256 и размер двух оригинальных экспортов. 43 записи, 48 выдержек.
  Markdown убирает только концевые пробелы строк; JSON сохраняет точные выдержки.
  В S861 сохранена постановка до вложенного примера промпта; это не полный
  многократно процитированный промпт. Клиентский brief/решение не публикуются.
- `extract.py` — **до чтения человеком** фильтрует СПЛИТ по теме и дате с
  1 августа; индексирует роли/ID/ветви. У assistant читает `phase=answer`,
  не reasoning summaries. Видимая ветка и history-only не склеиваются.
  Рабочие реплики сохраняются как `.txt`: процитированные исторические
  относительные пути не являются Markdown-ссылками текущего репозитория.
  Формально Founder — роль постановщика по issue, не проверенное имя аккаунта.
- `curate.py`, `verify.py` — воспроизводят отбор и сверяют выдержки с
  оригиналами, включая хэши, ID, роли, UTC, размеры и число сообщений.
- `probe.py`, `prompt-probe.json` — полное сравнение скопированных тел
  четырёх промптов с четырьмя закреплёнными git-ревизиями. Убираются только
  copy marker, YAML frontmatter, внешние пробелы; CRLF → LF. Внутренний
  текст не нормализуется. Несовпадение не устанавливает причину публикации.
- `inventory.py`, `run-inventory.json` — прямой пересчёт 137 уникальных
  SC-ID (по RUN) и 200 Golden-кандидатов RUN-0073…76. Статус draft и
  `confirmed_by` сохраняются; это не автоматический promotion в oracle.
- `build_replay_cases.py`, `replay-cases.json` — ручные аннотации наблюдаемых
  эпизодов с S/X-ID и явно помеченные synthetic controls. Признаки
  entailment/relevance/inefficiency/semantic diff **не выводятся** Python
  из текста. Метка `basis` связывает дизайн с эпизодом, не означает, что
  весь JSON-вход дословно находился в чате.
- `replay.py`, `replay-results.json` — 23 детерминированных проверки проекта
  протокола (delivery, baseline, evidence, appeal). `block_disputed`
  останавливает спорную часть, `block_release` — объявление неполной сборки
  готовой. Положительные примеры проверяют разрешённую работу. Это не
  LLM-eval и не замер частоты будущих ошибок.
- `build_report_refs.py` — абсолютные ссылки отчёта; внешние файлы закреплены
  полными SHA. Рабочий checklist и логи остаются локально в `logs/`.

## Проверка без приватных вложений

Из корня репозитория:

```bash
python3 scripts/test_issue_397_evidence.py
python3 experiments/issue_397/inventory.py
python3 experiments/issue_397/build_replay_cases.py
python3 experiments/issue_397/replay.py
make validate-fast
make validate-full
```

Тест проверяет фазу ответа, сохранность текста при сравнении, трассируемость
цитат в отчёт, полный реестр требований/ссылок, пересчёт RUNS и сохранённые
результаты replay. Файл `scripts/test_issue_397_evidence.py` автоматически
обнаруживается общим runner; новые workflows и сетевые зависимости не нужны.

## Повторная сверка оригиналов

Вложения скачиваются авторизованным GitHub CLI/curl в игнорируемый `raw/`.
Не коммитьте `raw/`, `turns/` или `logs/`: там может быть клиентский контекст.
Пример из корня (токен не записывается в файл и не печатается):

```bash
mkdir -p experiments/issue_397/raw experiments/issue_397/logs
curl --fail -L -H "Authorization: token $(gh auth token)" \
  -o experiments/issue_397/raw/chat-export-split.json \
  'https://github.com/user-attachments/files/34074559/chat-export-.json'
curl --fail -L -H "Authorization: token $(gh auth token)" \
  -o experiments/issue_397/raw/chat-export-1131.json \
  'https://github.com/user-attachments/files/34074560/chat-export-1131.json'
python3 experiments/issue_397/verify.py
python3 experiments/issue_397/extract.py > experiments/issue_397/logs/extraction.json
```

`verify.py` до регенерации сравнивает скачанные байты с опубликованными
хэшами. При расхождении остановитесь и исследуйте смену входа. Для
повторного построения производных (после успешной сверки):

```bash
python3 experiments/issue_397/curate.py
python3 experiments/issue_397/verify.py
python3 experiments/issue_397/probe.py > experiments/issue_397/logs/prompt-probe.log
python3 experiments/issue_397/build_report_refs.py
git diff -- experiments/issue_397 docs/analysis/2026-10-28-bcreq-evolution-failure-analysis.md
```

`probe.py` запускается из корня полного git checkout с историей четырёх SHA,
перечисленных в `prompt-probe.json`; shallow clone может их не содержать.
Новый результат не должен молча подменять старое доказательство. Хаб и runtime
проверялись read-only в закреплённых срезах отчёта; полные их копии сюда не
переносятся. Статические тесты не требуют доступа к ним или к вложениям.

## Что считается воспроизведённым

Наблюдаемые отказы — опубликованные ответы 1131 и повторные исправления
постановки в СПЛИТ, а не заново полученная генерация той же модели. Тест
нового extractor написан до реализации `answer_text` и сначала падал из-за
отсутствия этой функции; теперь проверяет phased answer при пустом `content`.
Это проверка инструмента исследования, не воспроизведение бага старого
промпта. Replay проверяет **предложенный** механизм на размеченных
состояниях; его PASS не доказывает правоту продуктовых утверждений или
эффективность будущего prompt patch. Реальное сравнение LLM до/после должно
иметь новые ответы, модель/версию и оценку по критериям; оно здесь не заявлено.
