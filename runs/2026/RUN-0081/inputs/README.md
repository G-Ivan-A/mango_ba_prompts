---
status: draft
version: 0.1
updated: 2026-11-04
temperature: 0.1
---

# Вход RUN-0081

## Что проверяется

Промпт шага Ш-В (проверка фрагмента второй ролью) в двух редакциях на
коммите BL-156а (issue #444):

| Метка | Редакция | Файл | Коммит | Размер | Отличие от RUN-0080 |
| --- | --- | --- | --- | --- | --- |
| A | 0.1 с типом гейта и ссылками по SHA | `prompts/bcreq-review-validation-oneshot.md` | `36799e9e` | 18 926 байт | Тот же текст, что A RUN-0080 (подстановка типа гейта), плюс ссылки на runtime по SHA `f31dcde3` вместо `blob/main/` |
| D | 0.1 «по тесту» (черновик на реестре 0.4) | `prompts/drafts/bcreq-review-validation-oneshot.md` | `36799e9e` | 41 639 байт | Текст A плюс блок «по тесту», собранный на реестре справочников 0.4: З-3 и З-4 сняты, раздел 2.2 (М-4), runtime `f31dcde3` |

Промпты в прогон не копируются, их восстанавливает git:

```bash
git show 36799e9e:prompts/bcreq-review-validation-oneshot.md          # A
git show 36799e9e:prompts/drafts/bcreq-review-validation-oneshot.md   # D
```

Хэши SHA-256 обоих файлов записаны в [`mapping.json`](mapping.json) и в
`metadata.yaml`. После прогона типизация из `prompts/` снята (см.
[отчёт](../outputs/golden-set-report.md#решение)). Валидатор #438
восстанавливает измеренные тексты из текущих файлов функцией
`apply_typing()` (`experiments/issue_444/bl156a_prompt_changes.py`) и
сверяет хэши байт в байт.

## Кейсы

Кейсы те же, что в RUN-0079 и RUN-0080, байт в байт и в тех же метках
T-01…T-62:

- [`../../RUN-0079/inputs/cases-batch1.md`](../../RUN-0079/inputs/cases-batch1.md);
- [`../../RUN-0079/inputs/cases-batch2.md`](../../RUN-0079/inputs/cases-batch2.md).

Сценарий подготовки пересобирает карту T-NN из golden set с seed 79 и
останавливается, если она отличается от карты RUN-0079. Карта в
[`mapping.json`](mapping.json) равна карте RUN-0079.

Исполнитель видит только «Вход» и «Контекст». Эталонный вердикт, урок и
обоснование он не видит.

Подготовка: `python3 experiments/issue_444/run0081/prepare.py /tmp/run81`.
