---
type: kb-source-index
doc_code: CC
doc_title: "Контакт-центр MANGO OFFICE"
doc_version: "1.26.23-sample"
status: extracted
ai-generated: true
---

# Контакт-центр MANGO OFFICE — индекс БЗ (карта разделов)

> Источник: `kb/sources/contact-center-manual-sample/CC_manual_sample.fixture.pdf` · извлечено: pdfplumber 0.11.10 ·
> токены: tiktoken:cl100k_base. Это **карта поиска** для агента (замена
> retrieval-шага до RAG, ADR-007 R2): найди раздел по колонке «Когда
> обращаться», открой только его файл, процитируй стабильным адресом.

## Как цитировать

`[CC, §<номер>, с.<страница>]` — формат проекта (issue #109);
плюс адрес чанка `kb/processed/<doc>/sections/<file>#<якорь>` (ADR-007 R3).

## Разделы

| № | Раздел | Файл | Стр. | Токены | Когда обращаться |
| --- | --- | --- | --- | ---: | --- |
| — | Титульная часть | [sections/00-titulnaya-chast.md](sections/00-titulnaya-chast.md) | 1 | 62 | Контакт-центр MANGO OFFICE |
| 1 | Введение | [sections/01-vvedenie.md](sections/01-vvedenie.md) | 2 | 208 | Назначение документа; Системные требования и ограничения |
| 2 | Рабочее место оператора | [sections/02-rabochee-mesto-operatora.md](sections/02-rabochee-mesto-operatora.md) | 3 | 301 | Статусы оператора; Очередь обращений |
| 3 | Каналы коммуникации | [sections/03-kanaly-kommunikacii.md](sections/03-kanaly-kommunikacii.md) | 4 | 294 | Голосовые вызовы; Текстовые каналы; Электронная почта (e-mail) |
| 4 | Обработка обращений | [sections/04-obrabotka-obrascheniy.md](sections/04-obrabotka-obrascheniy.md) | 5 | 378 | Контроль обращений; Правила распределения; Каналы обращений |
| 5 | Роли и права доступа | [sections/05-roli-i-prava-dostupa.md](sections/05-roli-i-prava-dostupa.md) | 6 | 253 | Права на модуль «Обращения» и вкладки очереди настраиваются в ЛК ВАТС → |
| 6 | Отчёты и аналитика | [sections/06-otchety-i-analitika.md](sections/06-otchety-i-analitika.md) | 7 | 91 | Отчёты строятся по вызовам и текстовым обращениям: длительность, время ожидания, |
| | **ИТОГО** | | | **1587** | весь документ |

## Источники

- Источник БЗ: `kb/sources/contact-center-manual-sample/CC_manual_sample.fixture.pdf`
- Стандарт цитирования: [`standards/kb-standard.md`](../../../standards/kb-standard.md), [ADR-007](../../../docs/adr/007-kb-standard.md)
