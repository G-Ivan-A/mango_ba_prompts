---
status: draft
version: 0.1
updated: 2026-08-25
ai-generated: true
type: input
scope: mango-only
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/315"
---

# Вход прогона RUN-0056 — провенанс исходных данных

Тема прогона: **gap-анализ и оценка технической осуществимости интеграции контакт-центра Mango Office с чатами HH.ru**.

Исходный файл ФТ в репозитории **не хранится** (требование постановки [#315](https://github.com/G-Ivan-A/mango_ba_prompts/issues/315): хранение — локально на АРМ Пользователя; файл удалён из рабочего каталога после прогона). Ниже — наименование, контрольная сумма и суммаризация каждого входа.

## Файл 1 — ФТ Заказчика (вложение задачи)

| Поле | Значение |
| --- | --- |
| Наименование | `765 ФТ Интеграция чатов из HH.ru в КЦ.pdf` |
| Вложение issue | https://github.com/user-attachments/files/31380601/765.HH.ru.pdf |
| Размер, байт | 500386 |
| SHA-256 | `854430ae10754ef205dfa420377e7f0cc5c6e90e6040eaffa5eff156e7369377` |
| Страниц | 10 |
| Текстовый слой | есть (извлекается `pypdf`) |

**Суммаризация по разделам.**

| Раздел ФТ | Содержание |
| --- | --- |
| §1 Глоссарий | Система, КЦ, ЛК, МД (мультиканальный диалог), АК (адресная книга), Внешняя система = HeadHunter, Пользователь, Актор, Чат с клиентом, Обращение, Сессия, Кандидат, Рекрутер. |
| §2 Проблема, цель, задачи | Рекрутеры ведут переписку с кандидатами вне КЦ; цель — завести чаты HH.ru как канал КЦ. |
| §3.1 Перечень ФТ | ФТ-01…ФТ-10 (список требований верхнего уровня). |
| §4.1–4.10 | Детализация каждого ФТ по сценариям (нумерация вида §4.5.2, §4.6.2, §4.7.3, §4.8.2, §4.10.2). |
| §5 НФТ | Пустой («-») — нефункциональных требований Заказчик не задал. |
| §6 Ограничения | Ограничения объёма и охвата интеграции. |
| §7 Макеты | Скриншоты интерфейса существующего канала «Авито Работа» как образец. |

**Что извлечено в прогон.** Формулировки ФТ-01…ФТ-10 и их детализация — они процитированы в [`../outputs/L2-gap-matrix.md`](../outputs/L2-gap-matrix.md) построчно. Полный текст ФТ в репозиторий не переносится.

## Источник 2 — официальная документация API hh.ru

| Поле | Значение |
| --- | --- |
| Репозиторий | https://github.com/hhru/api |
| Коммит на момент прогона | `906d7b6840a5b739cf61465d9b6fbf6391c51341` (2025-12-19) |
| Что прочитано | `README.md`, `docs/authorization.md`, `docs/authorization_for_user.md`, `docs/authorization_for_application.md`, `docs/negotiations.md`, `docs/employer_negotiations.md`, `docs/employer_negotiations_statistics.md`, `docs/employer_managers.md`, `docs/employer_resumes.md`, `docs/errors.md`, `docs/cache.md`, `docs/FAQ.md` |

**Ограничение доступа.** Интерактивная OpenAPI-спецификация (`https://api.hh.ru/openapi/...`), сайт `dev.hh.ru` и база знаний `feedback.hh.ru` из среды выполнения **недоступны по сети** (соединение отвергается на уровне TCP). Протокол проверок — [`../logs/source-availability.md`](../logs/source-availability.md). Анализ выполнен по markdown-документации репозитория `hhru/api`, которой достаточно для вердикта по 7 требованиям из 10; по 3 требованиям вердикт помечен как частичный.

## Источник 3 — база знаний Mango Office (в репозитории)

| Раздел БЗ | Что взято |
| --- | --- |
| [`kb/processed/mango-lk-manual/sections/186-nastroyka-kanalov-kommunikacii.md`](../../../../kb/processed/mango-lk-manual/sections/186-nastroyka-kanalov-kommunikacii.md) | Перечень существующих каналов: MAX, Вконтакте, WhatsApp, Telegram, Клиентское приложение (по API), E-mail, Авито, Авито Работа. Канала HeadHunter нет. |
| [`kb/processed/mango-lk-manual/sections/210-avito-rabota.md`](../../../../kb/processed/mango-lk-manual/sections/210-avito-rabota.md) | Паттерн канала «Авито Работа»: подключение через OAuth-авторизацию, обработчики, переключатель «Отклик кандидата — только отклики с сообщениями», автоответы, «Закрывать неактивный диалог через». |
| [`kb/processed/mango-lk-manual/sections/209-avito.md`](../../../../kb/processed/mango-lk-manual/sections/209-avito.md) | Ограничения канала «Авито»: нельзя инициировать обращение к клиенту; один аккаунт — один виджет. |
| [`kb/processed/mango-lk-manual/sections/207-klientskoe-prilozhenie.md`](../../../../kb/processed/mango-lk-manual/sections/207-klientskoe-prilozhenie.md) | Канал «Клиентское приложение (по API)»: услуги «API-Коннектор» + «Открытое API», передача файлов, автозавершение диалогов. |
| [`kb/processed/mango-cc-manual/sections/26-istoriya-obrascheniy.md`](../../../../kb/processed/mango-cc-manual/sections/26-istoriya-obrascheniy.md) | Отчёт «История обращений» и его фильтр по каналу — вход для ФТ-10. |

## Воспроизведение

```bash
# 1. ФТ Заказчика
curl -L -o 765-ft-hh.pdf "https://github.com/user-attachments/files/31380601/765.HH.ru.pdf"
sha256sum 765-ft-hh.pdf   # 854430ae10754ef205dfa420377e7f0cc5c6e90e6040eaffa5eff156e7369377
python3 -c "from pypdf import PdfReader; r=PdfReader('765-ft-hh.pdf'); print('\n'.join((p.extract_text() or '') for p in r.pages))"

# 2. Документация API hh.ru
git clone https://github.com/hhru/api /tmp/hhapi
git -C /tmp/hhapi rev-parse HEAD   # 906d7b6840a5b739cf61465d9b6fbf6391c51341 на момент прогона
```

## Чего во входе нет

- Нет доступа к интерактивной OpenAPI-спецификации hh.ru и к статье базы знаний hh.ru о новых «чатах» — см. [`../logs/source-availability.md`](../logs/source-availability.md).
- Нет партнёрского/платного доступа работодателя к API hh.ru: часть методов помечена «Методы требуют наличия платного доступа для работодателя», их фактическое поведение не проверялось.
- Нет внутренней документации Mango Office по реализации канала «Авито Работа» — использован только пользовательский справочник из БЗ репозитория.
- Нет НФТ: §5 ФТ пуст, поэтому нефункциональные ограничения в gap-матрице выведены из документации API, а не из требований Заказчика.
