---
status: draft
version: 0.1
updated: 2026-10-31
temperature: 0.1
---

# Журнал RUN-0079

## Цель

Проверить, удерживает ли промпт этапа 1 правила, выведенные из прошлых
прогонов, после того как реестр уроков сгенерировал в нём блок «Уроки
прогонов». Сравнение: тот же промпт до блока (A) и после (B).

## Почему этот промпт

`bcreq-review-validation-oneshot.md` (шаг Ш-В) — проверка одного фрагмента.
Это единственный шаг, где один кейс golden set — это один законченный вызов
модели. Остальные 13 промптов генерируют разделы и требуют полного входа
задачи; их проверяет режим генерации (RFC, «Режимы прогона»).

## Процедура

1. **Подготовка** — `python3 experiments/issue_411/run0079/prepare.py /tmp/run79`:
   - промпт A и B извлекаются через `git show <ref>:prompts/bcreq-review-validation-oneshot.md`;
   - 62 кейса golden set перемешиваются (seed 79), получают метки T-01…T-62 и
     делятся на 2 пакета по 31;
   - исполнителю остаются только «Вход» и «Контекст»;
   - карта T-NN → кейс пишется в `mapping.json` и исполнителю не передаётся.
2. **Исполнение** — 4 изолированных подагента `claude-opus-5-5` (A×2 пакета,
   B×2 пакета). Каждому разрешено прочитать ровно два файла (свой промпт и
   свой пакет) и записать один файл. Инструкция исполнителю (одинаковая для
   A и B, кроме имён файлов):

   > You are the model under test in a controlled prompt experiment. ALLOWED
   > ACTIONS: use the Read tool on exactly two files, and the Write tool on
   > exactly one output file. Do NOT use Bash, Grep, Glob, git, web, or read
   > any other file. 1. Read prompt-{V}.md in full. This is your system prompt…
   > 2. Read cases-batchN.md… 3. For each fragment independently decide whether
   > it contains a defect according to your system prompt. Do not assume every
   > fragment is defective; do not assume every fragment is clean. 4. Write a
   > JSON array … {"case", "verdict": "дефект" | "дефекта нет", "violation",
   > "quote", "fix"}.

   Каждый исполнитель сделал ровно 3 вызова инструментов (2 Read и 1 Write).
   Это подтверждает, что изоляция соблюдена.
3. **Слепая подготовка судьи** — `python3 experiments/issue_411/run0079/judge_prepare.py /tmp/run79`:
   - для каждого кейса A и B случайно (seed 7979) становятся X или Y;
   - ключ сохраняется в `judge-key.json`;
   - номера уроков `L-NN` в ответах маскируются: B цитировал их из блока
     уроков и иначе выдал бы версию. После маскировки в файлах судьи нет ни
     одного `L-NN`;
   - судье показываются вход, контекст, эталонный вердикт, тип кейса,
     правило урока, обоснование эталона и два выхода.
4. **Оценка** — 2 изолированных подагента-судьи `claude-opus-5-5`. Каждому
   разрешено прочитать только рубрику, правила реестра
   ([`judge-rules.md`](judge-rules.md)) и свой пакет
   ([`judge-input-batch1.md`](judge-input-batch1.md),
   [`judge-input-batch2.md`](judge-input-batch2.md)). Определения K1–K6 в
   инструкции судье совпадают с рубрикой. Отдельно сказано: «Do not try to
   work out which prompt version produced X or Y» и «Judge X and Y
   independently by the same standard». Судья мог проверить, что его JSON
   парсится.
5. **Пересчёт** — `python3 experiments/issue_411/run0079/score.py /tmp/run79`:
   раскрывает ключ и считает критерии, сданные кейсы, ядро, ложные
   срабатывания и разницу версий.
6. **Фиксация** — `python3 experiments/issue_411/run0079/fixate.py /tmp/run79`:
   копирует входы, логи и выходы в этот каталог.

## Затраты

| Шаг | Токены (subagent_tokens) | Время |
| --- | --- | --- |
| Исполнитель A, пакет 1 / 2 | 28 498 / 27 112 | 64,5 / 54,2 с |
| Исполнитель B, пакет 1 / 2 | 39 293 / 39 942 | 49,6 / 55,9 с |
| Судья, пакет 1 / 2 | 48 796 / 47 212 | 98,1 / 86,8 с |
| **Итого A / B / судья** | 55 610 / 79 235 / 96 008 | 119 / 105 / 185 с |

Токены и время взяты из отчёта Claude Code о каждом подагенте. Они включают
чтение промпта и пакета, поэтому разница A и B в основном отражает
размер промпта: 18 754 байт против 63 603 байт.

## Воспроизведение

Команды из шагов 1, 3, 5 и 6 детерминированы. Шаги 2 и 4 повторяются с теми
же инструкциями. Ответы модели при повторе могут отличаться: температура
подагентов не управляется.
