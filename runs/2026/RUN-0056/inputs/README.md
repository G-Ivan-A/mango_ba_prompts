---
status: draft
version: 0.1
updated: 2026-08-25
ai-generated: true
type: input
scope: mango-only
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/317"
---

# Вход прогона RUN-0056 — провенанс исходных файлов

Постановка [issue #317](https://github.com/G-Ivan-A/mango_ba_prompts/issues/317)
содержит шесть PDF-вложений. Файлы **не хранятся в репозитории**: по контракту
задачи (раздел «Гигиена репозитория») исходники удалены из рабочего каталога
после извлечения и валидации, Git LFS не используется. Ниже — текстовая
трассировка источников.

| Кластер | Файл вложения | Целевой раздел БЗ | Страниц |
| --- | --- | --- | --- |
| Обновление | `CC_manual_1.26.28.1.pdf` | `kb/processed/mango-cc-manual/` | 614 |
| Обновление | `LK_manual_v-123.pdf` | `kb/processed/mango-lk-manual/` | 565 |
| Обновление | `Модуль ЦОВ Робот Фил 2,0_manual_v7.26.28.pdf` | `kb/processed/cov-robot-fil/` | 195 |
| Обновление | `UserGuide_Windows_mTalker_ch1_Working.11.06.26.pdf` | `kb/processed/mtalker/windows-mac-working/` | 128 |
| Обновление | `UserGuide_mTalker_4Mobile 11.06.26.pdf` | `kb/processed/mtalker/android-user-guide/` | 66 |
| Новые | `Manual_API_Mango_Dialogi.pdf` | `kb/processed/mdialogi-api/` | 96 |

Ссылки на вложения зафиксированы в теле issue #317; точное имя файла
сохраняется в `source_document` фронтматтера каждого `index.md` и в
`meta.json` соответствующего раздела.
