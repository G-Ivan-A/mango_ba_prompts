#!/usr/bin/env python3
"""Render the issue #353 RCA report and its generated 65-row table."""

from __future__ import annotations

from pathlib import Path

from analyze_runs import build_sample, markdown


ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / "docs/report/2026-09-01-run-0065-vs-0066-ab-rca.md"


def percent(value: float | int) -> str:
    return f"{value:.1f}%"


def main() -> int:
    sample, metrics = build_sample()
    old, new = metrics["RUN-0065"], metrics["RUN-0066"]
    body = f"""---
status: complete
updated: 2026-09-01
ai-generated: true
type: analysis
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/353"
related_runs:
  - RUN-0065
  - RUN-0066
---

# A/B-RCA RUN-0065 vs RUN-0066 для task-1099

## Результат

Провал RUN-0065 вызван не переполнением окна и не другой версией БЗ. Механизм
сбоя наблюдаем в исходниках и raw trace: gpt-5.6-sol записала номера страниц в
ручной словарь `EVIDENCE`, затем генератор тиражировал одну выбранную строку по
лексическому правилу. Поздняя выборочная сверка исправила часть словаря, но не
`record`, а порядок правил направил требование «Авито Работа» в более ранний
класс `address`. Валидатор проверял наличие похожей на атомарную ссылки, но не
сопоставлял её с frontmatter, поэтому принял результат.

На выборке из **{len(sample)} строк** RUN-0065 совпал с эталонными вердиктами в
{percent(old['accuracy_verdict_percent'])} случаев и дал галлюцинированную
пагинацию (Δ > 2) в {percent(old['hallucination_rate_percent'])} строк. RUN-0066
дал {percent(new['accuracy_verdict_percent'])} совпадений и 0 таких сдвигов.

## Данные и воспроизводимость

- RUN-0065 зафиксирован именно из commit `acb6c7bc`; blob отчёта:
  `36c3283c848107fa8922f987e65aec79ea0ac1d5`.
- RUN-0066 взят из commit `e0f4ba55`; blob отчёта:
  `845fd2887b99ef2ddf0e6a44d99921d62f96306a`.
- Полная структурированная выборка и признаки находятся в
  [`data/2026-09-01-run-0065-vs-0066-sample.json`](data/2026-09-01-run-0065-vs-0066-sample.json).
- Выборка и метрики повторяются командой
  `python3 experiments/issue_353/analyze_runs.py`.
- Три решения генератора commit `acb6c7bc` повторяются без нового LLM-вызова
  командой `python3 experiments/issue_353/replay_acb_generator.py`.
- Полный дополнительно обезличенный trace и его provenance описаны в
  [`evidence/README.md`](evidence/README.md).

RUN-0066 используется как эталон по прямому требованию issue #353 и по
пользовательской валидации >95%, а не как независимая абсолютная истина.
`Accuracy_verdict` — совпадение с его вердиктом. `Accuracy_page` считается среди
строк, где модель эмитировала локальную нумерованную ссылку: все ссылки строки
должны совпасть с frontmatter с допуском ≤2. `Hallucination_rate` — доля всех 65
строк, где хотя бы одна ссылка имеет Δ >2. `Decomposition_quality` — бинарный
операционный proxy: для RUN-0065 нужны одновременно совпавший вердикт, валидная
пагинация и пересечение с эталонным атомарным разделом; RUN-0066 — эталонный
класс. Этот proxy измеряет трассируемую декомпозицию, а не стиль текста.

## Метрики

| Метрика | RUN-0065 | RUN-0066 |
| --- | ---: | ---: |
| `Accuracy_verdict` | {old['accuracy_verdict_count']}/{old['rows']} = {percent(old['accuracy_verdict_percent'])} | {new['accuracy_verdict_count']}/{new['rows']} = {percent(new['accuracy_verdict_percent'])} |
| `Accuracy_page` (eligible rows, допуск ≤2) | {old['accuracy_page_count']}/{old['accuracy_page_eligible_rows']} = {percent(old['accuracy_page_percent'])} | {new['accuracy_page_count']}/{new['accuracy_page_eligible_rows']} = {percent(new['accuracy_page_percent'])} |
| `Hallucination_rate` (Δ >2 / все строки) | {old['hallucination_count']}/{old['rows']} = {percent(old['hallucination_rate_percent'])} | {new['hallucination_count']}/{new['rows']} = {percent(new['hallucination_rate_percent'])} |
| `Decomposition_quality` (атомарно) | {old['atomic_decomposition_count']}/{old['rows']} = {percent(old['decomposition_quality_percent'])} | {new['atomic_decomposition_count']}/{new['rows']} = {percent(new['decomposition_quality_percent'])} |

RUN-0066 не содержит ссылки в строке №173, где документированный численный порог
85% отсутствует; поэтому знаменатель `Accuracy_page` для него равен 64, а не 65.
Отсутствие страницы не классифицируется как галлюцинация.

## Построчное сравнение

Включены все сопоставленные строки, где хотя бы один прогон ссылался на один из
пяти обязательных разделов: §4.5.3.4, §4.5.11.2.2, §4.5.19, §4.6.3.5 или §5.
Колонка «Факт» показывает эталон RUN-0066, но страницы в ней независимо
перечитаны из frontmatter связанного файла.

<!-- issue-353-sample-start -->
{markdown(sample)}<!-- issue-353-sample-end -->

## Наблюдаемый процесс генерации трёх ссылок

Задача просит «цепочку рассуждений». Скрытая chain-of-thought не публикуется и не
реконструируется: в доступном trace её нет, а придумывать её запретил сам issue.
Ниже приведена проверяемая action/tool trace — команды, входные значения,
патчи, token telemetry и детерминированное поведение кода. Этого достаточно для
механистического RCA без утверждений о приватном внутреннем рассуждении модели.

### Общая последовательность

1. Контекст был настроен на 200 000 токенов
   ([trace L391](evidence/2026-09-01-run-0065-acb6c7bc-redacted.txt#L391)).
2. Широкий поиск БЗ вернул 301 244 символа и был усечён инструментом
   (`output_truncated=true`), то есть retrieval был неограниченным и шумным
   ([trace L5712](evidence/2026-09-01-run-0065-acb6c7bc-redacted.txt#L5712)).
3. Следующий ответ при `input_token_count=84571` создал ручной словарь страниц
   ([trace L5795](evidence/2026-09-01-run-0065-acb6c7bc-redacted.txt#L5795)).
4. Только примерно через шесть минут агент напрямую прочитал frontmatter
   `252-karusel-nomerov.md` и `138-nastroyki.md`
   ([trace L8421](evidence/2026-09-01-run-0065-acb6c7bc-redacted.txt#L8421)).
5. Последующий патч исправил несколько ключей словаря, но не `record`
   ([trace L8711-L8722](evidence/2026-09-01-run-0065-acb6c7bc-redacted.txt#L8711)).

### §4.5.3.4 «Настройки»

Первичная эмиссия записала `с.226–231` в `EVIDENCE["record"]`
([trace L5823](evidence/2026-09-01-run-0065-acb6c7bc-redacted.txt#L5823)).
Frontmatter связанного `138-nastroyki.md` содержит `pages: 209-213`. Поздний патч
не изменил ключ `record`, поэтому commit `acb6c7bc` и повтор
`replay_acb_generator.py` стабильно выдают `226–231`: Δ начала 17, конца 18.
Это воспроизводит дефект без предположения о внутреннем ходе мыслей.

### §4.5.11.2.2 «Авито Работа»

В первичном патче действительно наблюдается указанная в issue ошибка:
`§4.5.11.8, с.348–354`
([trace L5828](evidence/2026-09-01-run-0065-acb6c7bc-redacted.txt#L5828)); факт
frontmatter — `§4.5.11.2.2, с.339-345`. Перед commit словарный литерал исправлен
на факт ([trace L8722](evidence/2026-09-01-run-0065-acb6c7bc-redacted.txt#L8722)).
Однако итоговый отчёт всё равно не использовал его: строка содержит слово
«контакт», а правило `address` расположено раньше правила `avito`; генератор
берёт `matches[0]`. Точный replay commit поэтому выдаёт §4.5.10, с.275–276.
Итак, первичная галлюцинация воспроизводится trace, а финальный дефект — это
детерминированное shadowing правил, не сохранённый сдвиг 9 страниц.

### §4.5.19 «Карусель номеров»

Первичная эмиссия была `с.406–414` вместо `414-416`
([trace L5822](evidence/2026-09-01-run-0065-acb6c7bc-redacted.txt#L5822)). После
прямого чтения frontmatter литерал исправлен
([trace L8640](evidence/2026-09-01-run-0065-acb6c7bc-redacted.txt#L8640)), и replay
commit выдаёт корректные `414–416`. Финальная галлюцинация здесь **не
воспроизводится**; согласно circuit breaker issue это evidence в пользу H3/H4:
правильность зависела от необязательной ручной сверки и не была защищена gate.

## Проверка H1–H5

| ID | Итог | Evidence и механистическое объяснение |
| --- | --- | --- |
| H1 | **Опровергнута как причина** | Ошибки не локализованы в середине одной большой главы: первичный словарь ошибался также в §5, §4.6.3.5, мобильном приложении и адресной книге. В commit страницы являются литералами кода, а не вычисленной «семантической памятью». Психологический механизм по trace установить нельзя. |
| H2 | **Опровергнута** | Ошибочные литералы появились при 84 571/200 000 входных токенов; автокомпактация была настроена на 150 000 и не происходила до этой точки. Было усечение одного 301 244-символьного tool output, но это retrieval-дефект, не переполнение контекстного окна. |
| H3 | **Подтверждена** | Prompt #349 требовал формат атомарной ссылки, но не требовал перечитывать frontmatter непосредственно перед эмиссией. RUN-0065 хардкодил страницы; RUN-0066 `cite.py` хранит только путь и извлекает `doc_code/pdf_section/title/pages` из frontmatter. |
| H4 | **Подтверждена** | `validate_issue_349_critical_fix.py` в commit проверял regex `[файл, §, с.]`, ширину таблицы и маркеры, но не открывал linked section и не сравнивал факты. Поэтому `226–231` прошло CI. Новый `validate_pagination_shift.py` делает именно такое разрешение и сравнение. |
| H5 | **Опровергнута для доступной БЗ; PDF-слой непроверяем** | Git tree `kb/processed` в обоих commits одинаков: `d3bc053cfc5102ff1868167631e4bedaccf3081f`; blob `mango-lk-manual/meta.json` одинаков: `b23eff3ae192e44b7c9e9fc4258a21efa3b49730` (SHA-256 содержимого `179c9f44…5487`). Сам `LK_manual_v-123.pdf` отсутствует в обоих деревьях по policy `.gitignore`, поэтому честно вычислить его SHA-256 нельзя. Доступные артефакты не поддерживают версию о разных БЗ. |

## Корневая причина и контрмеры

Первичная причина — **отсутствие обязательного resolver boundary** между
семантическим выбором evidence и эмиссией библиографических полей. Её усилили
широкий усечённый поиск, страницы в ручном словаре, `matches[0]` без проверки
специфичности и validator, проверявший форму вместо истины.

Контракт [`docs/contracts/kb-citations.md`](../contracts/kb-citations.md) вводит:

1. точный системный prompt с обязательным frontmatter anchor;
2. retrieval-порции ≤12 000 входных токенов (защитное правило, хотя H2
   опровергнута);
3. запрет страниц в ручных evidence maps;
4. проверяемый page-less fallback `[файл, §]`, когда `pages` недоступно;
5. блокирующий post-processing gate `scripts/validate_pagination_shift.py`.

Gate сравнивает linked path с document alias, разделом, заголовком и страницами.
Он допускает page-less fallback, но не позволяет замаскировать ошибку `n/a`.
`scripts/validate_issue_353_ab_rca.py` запускает его на RUN-0066 через
автообнаружение `make validate-full`.

## Рекомендация модели

Из двух наблюдавшихся конфигураций для следующего RUN с атомарными ссылками
следует выбрать **Claude Opus 5 / workflow RUN-0066**: на этой выборке он дал
100% эталонных вердиктов, 100% корректных page-bearing ссылок и нулевой
`Hallucination_rate`. Это не доказывает универсальное превосходство модели:
решающий архитектурный фактор — `cite.py`, который извлекает поля из
frontmatter. Поэтому production-рекомендация двухчастная: использовать
наблюдавшийся успешный Opus workflow сейчас и не допускать ни одну модель,
включая Opus, в merge без общего resolver + CI gate. gpt-5.6-sol можно повторно
рассматривать только после прохождения того же 65-строчного benchmark и gate.
"""
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(body, encoding="utf-8")
    print(f"rendered {REPORT.relative_to(ROOT)} with {len(sample)} comparison rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
