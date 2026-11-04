---
status: draft
version: 0.1
updated: 2026-11-04
temperature: 0.1
---

# Вход RUN-0082

## Что проверяется

Те же два текста шага Ш-В, что в RUN-0081, байт в байт. Меняется только
число замеров: три независимых повтора вместо одного (issue #446, BL-156б,
Р-03).

| Метка | Редакция | Файл | Коммит | SHA-256 |
| --- | --- | --- | --- | --- |
| A (A1) | 0.1 с типом гейта и ссылками по SHA | `prompts/bcreq-review-validation-oneshot.md` | `36799e9e` (сейчас восстанавливается `apply_typing()` из текущего v0.1) | `adf82663…` |
| D | 0.1 «по тесту» (черновик на реестре 0.4, типизированный v0.1) | `prompts/drafts/bcreq-review-validation-oneshot.md` | `36799e9e` | `2e839172…` |

Сценарий [`run.py`](../../../../experiments/issue_446/run0082/run.py)
собирает A функцией `apply_typing()` из текущего v0.1, а D берёт из git
(`git show 36799e9e:prompts/drafts/bcreq-review-validation-oneshot.md`).
Оба SHA-256 сверяются с RUN-0081; при расхождении сценарий
останавливается. Текущий черновик Ш-В собран на нетипизированном v0.1 и
отличается от D одной строкой и полем `based_on_sha256`: поэтому меряется
версия RUN-0081, а не текущий черновик.

## Кейсы

Кейсы RUN-0079 (62, seed раскладки 79), байт в байт:

- [`../../RUN-0079/inputs/cases-batch1.md`](../../RUN-0079/inputs/cases-batch1.md);
- [`../../RUN-0079/inputs/cases-batch2.md`](../../RUN-0079/inputs/cases-batch2.md).

Карта T-NN в [`mapping.json`](mapping.json) (повтор r1; у r2 и r3 карта та
же, отличаются поля `replicate` и `judge_seed`).

## Правило решения

Записано до запуска подагентов:
[`preregistration.md`](../../../../experiments/issue_446/run0082/preregistration.md)
(коммит `24e97e83`).

Подготовка: `python3 experiments/issue_446/run0082/run.py prepare /tmp/run82`.
