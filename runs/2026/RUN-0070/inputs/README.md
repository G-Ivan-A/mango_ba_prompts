---
status: draft
updated: 2026-10-01
ai-generated: true
type: evidence
---

# Входы RUN-0070

Источник — DOCX «Техническое задание -очиен в анализ.docx» (BCREQ-1115), вложенный в
issue [#367](https://github.com/G-Ivan-A/mango_ba_prompts/issues/367)
([файл](https://github.com/user-attachments/files/32930629/-.docx)); SSOT высшего
приоритета — «ТЗ-тендеров-v4.pdf»
([файл](https://github.com/user-attachments/files/32929383/-.-v4.pdf)).
По контракту прогонов исходные файлы в репозитории не хранятся, фиксируются контрольные суммы.

| Файл | SHA-256 | Размер |
| --- | --- | --- |
| Техническое задание -очиен в анализ.docx | `0464e9e4027fcf3b76490048e451f7caa1bd75f0de1f235aa25009ddd260bc1f` | 25 439 байт |
| ТЗ-тендеров-v4.pdf | `612e5e0938b9d4edad8e341f7fb03ba8498f7ec12dea0fe88f71e6817169d4cc` | 572 501 байт |

Транскрипция исходника (эталон колонок 1–2):
[`experiments/issue_367/source_transcription.json`](../../../../experiments/issue_367/source_transcription.json)
— генерируется `make_transcription.py` (python-docx), независимо сверяется с
`word/document.xml` скриптом `check_source.py`.

Индекс шаблона ТЗ v4 (п/п → страница, текст):
[`experiments/issue_367/tender_index.json`](../../../../experiments/issue_367/tender_index.json)
— `tender_index.py` (pymupdf, 301 пункт).

## Ограничения исходника

- DOCX без автонумерации (`numPr` отсутствует): номера `1.`…`18.` и маркеры `•` —
  литеральный текст абзацев, перенесены как есть.
- В разделе «Общие технические характеристики услуг» нет пункта `13.` (после `12.`
  идут шесть маркированных подпунктов и `14.`) — нумерация не исправлялась.
- Раздел «Термины и определения» (абзацы 13–36) требованиями не является — исключён;
  пустые абзацы пропущены. Итого 172 строки.
