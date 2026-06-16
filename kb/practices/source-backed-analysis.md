---
id: kb-source-backed-analysis
status: draft
version: 0.1
updated: 2026-06-16
ai-generated: true
type: kb-practice
scope: kb
sources:
  - "https://www.iiba.org/career-resources/a-business-analysis-professionals-foundation-for-success/babok/"
  - "https://www.iso.org/standard/72089.html"
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/97"
---

# Практика: анализ с опорой на источники (source-backed analysis)

> Запись KB. Регулируется [kb-standard.md](../../standards/kb-standard.md).
> Это **практика**, не стандарт: её можно адаптировать, но цитировать —
> по правилам C1-C4.

## Правило

<a id="правило"></a>
Каждое **нормативное** утверждение (что-то «должно/обязано/опирается на …»)
сопровождается проверяемой цитатой и **проверкой существования** источника до
ссылки на него. Если источник не находится — утверждение не выпускается как
факт, а помечается `needs-clarification`.

## Чек-лист проверки источника

1. Источник реально существует (открывается по URL/шифру)?
2. Указанная редакция/год существует именно в этом виде?
3. Полный URL приведён (НФТ доказуемости)?
4. Утверждение действительно следует из источника (а не «звучит похоже»)?

## Почему (обоснование)

- BABOK Guide v3 требует прослеживаемости требований к проверяемым источникам:
  <https://www.iiba.org/career-resources/a-business-analysis-professionals-foundation-for-success/babok/>
- ISO/IEC/IEEE 29148:2018 включает «verifiable» и «traceable» в характеристики
  качества требований: <https://www.iso.org/standard/72089.html>

## Анти-пример (реальный)

Шифр **«ГОСТ 34.602-2015» не существует** — есть редакции -89 и -2020. Цитата на
несуществующую редакцию проходит шаг 2 чек-листа со статусом «не найдено» и
**отклоняется**. Действующая редакция:
[ГОСТ 34.602-2020](https://docs.cntd.ru/document/1200181804).

## Источники

- BABOK Guide v3: <https://www.iiba.org/career-resources/a-business-analysis-professionals-foundation-for-success/babok/>
- ISO/IEC/IEEE 29148:2018: <https://www.iso.org/standard/72089.html>
- ГОСТ 34.602-2020: <https://docs.cntd.ru/document/1200181804>
