---
status: pending-source-file
version: 0.1
updated: 2026-06-18
ai-generated: true
type: kb-source-manifest
doc_code: CC
doc_title: "Контакт-центр MANGO OFFICE — Руководство пользователя"
doc_version: "1.26.23"
source_file: "CC_manual_1.26.23.pdf"
web_url: ""
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/111"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/109"
---

# Источник: Контакт-центр MANGO OFFICE (CC)

Манифест документа-источника. Описывает, **что** за документ, и служит шаблоном
для будущих источников. Один каталог `kb/sources/<slug>/` = один документ.

## Статус файла

> ⚠️ **Реальный `CC_manual_1.26.23.pdf` не загрузился в issue #111** (в теле
> задачи стоит маркер `<!-- Failed to upload "CC_manual_1.26.23.pdf" -->`,
> вложения в комментариях нет). Поэтому эксперимент проведён на **синтетической
> фикстуре** того же класса документа — генератор
> [`scripts/kb/make_sample_pdf.py`](../../../scripts/kb/make_sample_pdf.py)
> (её извлечение удалено из `kb/processed/` в issue #310: `make kb-sample`
> пишет стенд в некоммитируемый `.kb-sample/`), —
> структурно воспроизводящей реальное руководство (нумерация разделов, таблица
> ролей, диаграмма маршрутизации) по уже зафиксированной выжимке из issue #109:
> [`runs/2026/RUN-0011/inputs/kb-files.md`](../../../runs/2026/RUN-0011/inputs/kb-files.md).

## Как подключить реальный документ

1. Положите файл сюда: `kb/sources/contact-center-manual/CC_manual_1.26.23.pdf`.
2. При необходимости обновите поля выше (`doc_version`, `web_url`).
3. Запустите тот же конвейер в «настоящий» каталог результата:

   ```bash
   make kb-extract SRC=kb/sources/contact-center-manual/CC_manual_1.26.23.pdf \
                   OUT=kb/processed/contact-center-manual \
                   CODE=CC TITLE="Контакт-центр MANGO OFFICE" VERSION=1.26.23
   ```

4. Проверьте `kb/processed/contact-center-manual/index.md` и `make kb-validate`.

Методология и скрипты те же, что отработаны на фикстуре, — менять ничего не нужно.

## О документе

Руководство пользователя модуля «Контакт-центр» MANGO OFFICE: рабочее место
оператора, статусы, очередь обращений, каналы (голос/текст/e-mail), правила
распределения, роли и права, отчёты. Используется как БЗ для BA-анализа
(см. issue #109).

## Источники

- Веб-оригинал: _(укажите ссылку при наличии)_
- Выжимка As-Is: [`runs/2026/RUN-0011/inputs/kb-files.md`](../../../runs/2026/RUN-0011/inputs/kb-files.md)
