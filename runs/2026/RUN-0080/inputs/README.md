---
status: draft
version: 0.1
updated: 2026-11-03
temperature: 0.1
---

# Вход RUN-0080

## Что проверяется

Промпт шага Ш-В (проверка фрагмента второй ролью) в двух редакциях:

| Метка | Редакция | Файл | Коммит | Размер | Отличие |
| --- | --- | --- | --- | --- | --- |
| A | 0.1 (опубликован) | `prompts/bcreq-review-validation-oneshot.md` | `18a98c97` | 18 818 байт | Текст v0.1 RUN-0079 плюс строка типа гейта (BL-156, коммит `f5e0ba2e`) |
| D | 0.1 «по тесту» (черновик BL-156) | `prompts/drafts/bcreq-review-validation-oneshot.md` | `18a98c97` | 41 837 байт | Текст A без изменений (кроме ссылок на runtime по SHA) плюс блок «по тесту»: базовый стандарт, профили ANALYZE, VERIFY, TRANSFORM, контракты операций, справочники И-N, гейты |

Метка D, а не B: B в RUN-0079 — редакция 0.2 с блоком уроков, она не
опубликована (блоки уроков ждут ADR-017). Промпты в прогон не копируются,
их восстанавливает git:

```bash
git show 18a98c97:prompts/bcreq-review-validation-oneshot.md          # A
git show 18a98c97:prompts/drafts/bcreq-review-validation-oneshot.md   # D
```

Хэши SHA-256 обоих файлов записаны в [`mapping.json`](mapping.json) и в
`metadata.yaml`.

## Кейсы

Кейсы те же, что в RUN-0079, байт в байт, и в тех же метках T-01…T-62:

- [`../../RUN-0079/inputs/cases-batch1.md`](../../RUN-0079/inputs/cases-batch1.md);
- [`../../RUN-0079/inputs/cases-batch2.md`](../../RUN-0079/inputs/cases-batch2.md).

Это 62 кейса golden set 0.1: 52 дефектных и 10 негативных, по 31 в пакете.
Сценарий подготовки пересобирает карту T-NN из golden set с тем же seed 79
и останавливается, если она отличается от карты RUN-0079. Совпадение
проверено: карта в [`mapping.json`](mapping.json) равна карте RUN-0079.
Поэтому кейсы сюда не копируются.

Исполнитель видит только «Вход» и «Контекст». Эталонный вердикт, урок и
обоснование он не видит.

Подготовка: `python3 experiments/issue_438/run0080/prepare.py /tmp/run80`.
