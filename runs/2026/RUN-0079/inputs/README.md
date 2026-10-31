---
status: draft
version: 0.1
updated: 2026-10-31
temperature: 0.1
---

# Вход RUN-0079

## Что проверяется

Один и тот же промпт проверки фрагмента (шаг Ш-В) в двух версиях:

| Метка | Версия | Коммит | Размер | Отличие |
| --- | --- | --- | --- | --- |
| A | 0.1 | `34e07b06` (родитель коммита реестра уроков `2b6820a4`) | 18 754 байт | Нормы конституции BCREQ, правила АД-1…АД-11 |
| B | 0.2 | `5cef7bac` | 63 603 байт | То же плюс сгенерированный блок «Уроки прогонов» из `standards/bcreq-lessons/lessons.json` |

Кроме блока уроков, A и B отличаются только полями `version` и `updated` во
frontmatter. Промпты в прогон не копируются. Их можно восстановить из git:

```bash
git show 34e07b06:prompts/bcreq-review-validation-oneshot.md   # A
git show 5cef7bac:prompts/bcreq-review-validation-oneshot.md   # B
```

## Кейсы

- [`cases-batch1.md`](cases-batch1.md) и [`cases-batch2.md`](cases-batch2.md):
  62 кейса golden set 0.1 (52 дефектных и 10 негативных) по 31 в пакете.
  Исполнитель видит только «Вход» и «Контекст».
- ID кейсов заменены на T-01…T-62 в случайном порядке (seed 79), чтобы номер
  не подсказывал урок. Эталонный вердикт, урок и обоснование исполнитель не
  видит.
- [`mapping.json`](mapping.json) — карта T-NN → ID кейса golden set и ссылки
  на версии промпта. Исполнителю и судье карта не передавалась.

Подготовка: `python3 experiments/issue_411/run0079/prepare.py /tmp/run79`.
