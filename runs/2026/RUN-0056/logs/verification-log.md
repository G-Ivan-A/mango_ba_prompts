---
status: draft
version: 0.1
updated: 2026-08-25
ai-generated: true
type: log
scope: mango-only
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/317"
related_artifacts:
  - "standards/kb-standard.md"
---

# Лог верификации RUN-0056 (защита от галлюцинаций)

Метод: `cross-engine (pdfplumber -> PyMuPDF re-read of the same pages)`,
реализация — `scripts/kb/verify_extraction.py`. Для каждого раздела берутся
критические токены (числа, версии, URL, идентификаторы, константы) из текста,
извлечённого pdfplumber, и ищутся в независимом чтении тех же страниц PyMuPDF.
Не найденное **не исправляется и не додумывается**, а размечается маркером.

Сверено 5820 критических токенов, не подтверждено 2, страниц без текстового
слоя — 2.

## Найденные расхождения

| Раздел БЗ | Файл раздела | Стр. | Маркер | Что именно |
| --- | --- | ---: | --- | --- |
| `mango-cc-manual` | `sections/00-titulnaya-chast.md` | 1 | ⚠️ ПРОБЕЛ ИЗВЛЕЧЕНИЯ | титульная страница без текстового слоя (изображение) |
| `mango-cc-manual` | `sections/47-ostalnye-parametry-tip-zadachi-opisanie.md` | 211–212 | ❓ ТРЕБУЕТСЯ ПРОВЕРКА | значение `10.30` не подтверждено вторым движком |
| `mango-cc-manual` | `sections/97-otchety-rechevoy-analitiki.md` | 452–457 | ❓ ТРЕБУЕТСЯ ПРОВЕРКА | значение `02.01` не подтверждено вторым движком |
| `mango-lk-manual` | `sections/00-titulnaya-chast.md` | 1 | ⚠️ ПРОБЕЛ ИЗВЛЕЧЕНИЯ | титульная страница без текстового слоя (изображение) |

## Влияние на `confidence_level`

Понижение до `requires_review` выполняется конвейером автоматически при наличии
маркеров:

| Раздел БЗ | `confidence_level` | Причина |
| --- | --- | --- |
| `mango-cc-manual` | `requires_review` | 1 пробел извлечения + 2 неподтверждённых значения |
| `mango-lk-manual` | `requires_review` | 1 пробел извлечения (титул) |
| `mdialogi-api` | `high` | маркеров нет |
| `cov-robot-fil` | `high` | маркеров нет |
| `mtalker/windows-mac-working` | `high` | маркеров нет |
| `mtalker/android-user-guide` | `high` | маркеров нет |

Полный отчёт по каждому документу — `verification.md` внутри соответствующего
каталога `kb/processed/<slug>/`; машиночитаемая копия — блок `verification` в
его `meta.json`.
