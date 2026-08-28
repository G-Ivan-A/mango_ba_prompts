---
status: draft
version: 0.1
updated: 2026-08-28
ai-generated: true
type: log
scope: mango-only
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/336"
related_artifacts:
  - "experiments/issue_336_link_audit.py"
  - "runs/2026/RUN-0057/outputs/L0-customer-form-with-assessment.md"
---

# Журнал проверки ссылок прогона RUN-0061

> Файл **порождён** скриптом [`experiments/issue_336_fixate_run.py`](../../../../experiments/issue_336_fixate_run.py) из замеров [`experiments/issue_336_link_audit.py`](../../../../experiments/issue_336_link_audit.py) — не редактируйте вручную.

## 1. Ссылки, выданные моделью в диалоге

Проверена 21 ссылка(и) из ответов модели: HTTP-статус страницы, число заголовков с якорями и сопоставление заявленного раздела («Раздел на странице: …») с реальными заголовками страницы.

| Реплика | URL | HTTP | Заголовков | Заявленный раздел | Исход | Возможный якорь |
| --- | --- | --- | --- | --- | --- | --- |
| 13 | <https://wiki.twin24.ai/scripts/concepts/recognition-timers> | 200 | 4 | — | раздел не указан | — |
| 13 | <https://wiki.twin24.ai/scripts/concepts/recognition-timers> | 200 | 4 | — | раздел не указан | — |
| 13 | <https://wiki.twin24.ai/scripts/concepts/recognition-timers> | 200 | 4 | — | раздел не указан | — |
| 13 | <https://wiki.twin24.ai/scripts/concepts/recognition-timers> | 200 | 4 | — | раздел не указан | — |
| 15 | <https://wiki.twin24.ai/scripts/blocks/starting-block> | 200 | 14 | — | раздел не указан | — |
| 15 | <https://wiki.twin24.ai/scripts/use-cases/error-handling> | 200 | 2 | — | раздел не указан | — |
| 15 | <https://wiki.twin24.ai/bpl/functions/nlu> | 200 | 1 | — | раздел не указан | — |
| 17 | <https://wiki.twin24.ai/scripts/blocks/starting-block> | 200 | 14 | Валидация озвучки» и «Отладка и тестирование | заголовок найден, якорь существует | `#валидация-озвучки` |
| 17 | <https://wiki.twin24.ai/scripts/use-cases/error-handling> | 200 | 2 | — | раздел не указан | — |
| 17 | <https://wiki.twin24.ai/bpl/functions/nlu> | 200 | 1 | Параметры функции `nlu.parse` | на странице не найдено | — |
| 19 | <https://wiki.twin24.ai/bpl/functions/strings> | 200 | 27 | Строковые функции (`str.upper`, `str.lower`) | названо заглавие страницы, а не раздел | — |
| 19 | <https://wiki.twin24.ai/bpl/use-cases/string-title-bpl> | 200 | 3 | Озаглавливание строки | названо заглавие страницы, а не раздел | — |
| 21 | <https://wiki.twin24.ai/scripts/blocks/starting-block> | 200 | 14 | Приведение слов к первой форме | формулировка есть в тексте, но не заголовком | — |
| 23 | <https://wiki.twin24.ai/voice-bots/concepts/stop-words> | 200 | 6 | Уровни настройки стоп-слов» (Иерархия) | на странице не найдено | — |
| 25 | <https://wiki.twin24.ai/voice-bots/blacklist> | 200 | 2 | Чёрный список | названо заглавие страницы, а не раздел | — |
| 25 | <https://wiki.twin24.ai/voice-bots/blacklist> | 200 | 2 | Чёрный список | названо заглавие страницы, а не раздел | — |
| 25 | <https://wiki.twin24.ai/voice-bots/blacklist> | 200 | 2 | Чёрный список | названо заглавие страницы, а не раздел | — |
| 27 | <https://wiki.twin24.ai/scripts/blocks/> | 200 | 0 | Блок «Завершить звонок» (Hang up / Конец сценария) | на странице не найдено | — |
| 29 | <https://wiki.twin24.ai/ru/history/11072025> | 200 | 5 | Релиз от 11.07.2025» → поле «Тип ответившего | названо заглавие страницы, а не раздел | — |
| 29 | <https://wiki.twin24.ai/notifications/use-cases/session-grade> | 200 | 0 | Сохранение оценки сессии в отчет | названо заглавие страницы, а не раздел | — |
| 29 | <https://wiki.twin24.ai/ru/integration/webim/variables> | 200 | 0 | Получение информации о пользователе из Webim | названо заглавие страницы, а не раздел | — |

Итог по исходам:

| Исход | Ссылок |
| --- | --- |
| заголовок найден, якорь существует | 1 |
| названо заглавие страницы, а не раздел | 8 |
| формулировка есть в тексте, но не заголовком | 1 |
| на странице не найдено | 3 |
| раздел не указан | 8 |

## 2. Страницы вики, процитированные отчётом RUN-0057

Проверены все 79 различных страниц, названных токенами `[twin: …]` в [`../../RUN-0057/outputs/L0-customer-form-with-assessment.md`](../../RUN-0057/outputs/L0-customer-form-with-assessment.md). Доступны (HTTP 200): 79. Публикуют якоря заголовков: 71 (всего 345 заголовков).

| Страница | HTTP | Заголовков | Заглавие |
| --- | --- | --- | --- |
| [`ai-agents/elevenlabs-tts-models`](https://wiki.twin24.ai/ai-agents/elevenlabs-tts-models) | 200 | 3 | Сравнение моделей TTS от ElevenLabs | TWIN |
| [`ai-agents/knowledge-base`](https://wiki.twin24.ai/ai-agents/knowledge-base) | 200 | 2 | База знаний AI-агента | TWIN |
| [`ai-agents/optimizing-response-times`](https://wiki.twin24.ai/ai-agents/optimizing-response-times) | 200 | 6 | Оптимизация скорости ответа AI-агента | TWIN |
| [`ai-agents/rag-usage`](https://wiki.twin24.ai/ai-agents/rag-usage) | 200 | 5 | Использование RAG в базе знаний агента | TWIN |
| [`ai-calls/analytics-dialog-data`](https://wiki.twin24.ai/ai-calls/analytics-dialog-data) | 200 | 3 | Аналитика и сбор информации из диалога | TWIN |
| [`bpl/functions/date-time`](https://wiki.twin24.ai/bpl/functions/date-time) | 200 | 18 | Работа с датой и временем | TWIN |
| [`bpl/functions/deepseek`](https://wiki.twin24.ai/bpl/functions/deepseek) | 200 | 1 | Функции DeepSeek | TWIN |
| [`bpl/functions/extracting-substrings`](https://wiki.twin24.ai/bpl/functions/extracting-substrings) | 200 | 4 | Извлечение подстрок из текста | TWIN |
| [`bpl/functions/gigachat`](https://wiki.twin24.ai/bpl/functions/gigachat) | 200 | 1 | Функции GigaChat | TWIN |
| [`bpl/functions/gpt`](https://wiki.twin24.ai/bpl/functions/gpt) | 200 | 5 | Функции GPT | TWIN |
| [`bpl/functions/http`](https://wiki.twin24.ai/bpl/functions/http) | 200 | 8 | Функции для работы с HTTP | TWIN |
| [`bpl/functions/mathematical`](https://wiki.twin24.ai/bpl/functions/mathematical) | 200 | 11 | Математические функции | TWIN |
| [`bpl/functions/nlp-text`](https://wiki.twin24.ai/bpl/functions/nlp-text) | 200 | 3 | Работа с текстом на естественном языке NLP | TWIN |
| [`bpl/functions/nlp-understanding`](https://wiki.twin24.ai/bpl/functions/nlp-understanding) | 200 | 1 | Понимание естественного языка | TWIN |
| [`bpl/functions/nlu`](https://wiki.twin24.ai/bpl/functions/nlu) | 200 | 1 | Функции для работы с NLU | TWIN |
| [`bpl/functions/strings`](https://wiki.twin24.ai/bpl/functions/strings) | 200 | 27 | Строковые функции | TWIN |
| [`bpl/functions/ygpt`](https://wiki.twin24.ai/bpl/functions/ygpt) | 200 | 1 | Функции YandexGPT | TWIN |
| [`bpl/main-concepts/variables`](https://wiki.twin24.ai/bpl/main-concepts/variables) | 200 | 5 | Переменные | TWIN |
| [`bpl/use-cases/callback-time-setting`](https://wiki.twin24.ai/bpl/use-cases/callback-time-setting) | 200 | 2 | Настройка времени перезвона | TWIN |
| [`bpl/use-cases/string-title-bpl`](https://wiki.twin24.ai/bpl/use-cases/string-title-bpl) | 200 | 3 | Озаглавливание строки | TWIN |
| [`crm/amocrm/instructions/handling-variables`](https://wiki.twin24.ai/crm/amocrm/instructions/handling-variables) | 200 | 3 | Передача переменных из amoCRM в сценарий | TWIN |
| [`integration/gpt-integration`](https://wiki.twin24.ai/integration/gpt-integration) | 200 | 1 | Интеграция c GPT-4 | TWIN |
| [`nlu/concepts/nlu`](https://wiki.twin24.ai/nlu/concepts/nlu) | 200 | 5 | Принципы работы NLU | TWIN |
| [`nlu/concepts/system-entities`](https://wiki.twin24.ai/nlu/concepts/system-entities) | 200 | 4 | Список системных сущностей | TWIN |
| [`nlu/instructions/audio-parser`](https://wiki.twin24.ai/nlu/instructions/audio-parser) | 200 | 4 | Разметка диалогов | TWIN |
| [`nlu/instructions/manage-agent`](https://wiki.twin24.ai/nlu/instructions/manage-agent) | 200 | 8 | Управление агентами NLU | TWIN |
| [`nlu/instructions/manage-entities`](https://wiki.twin24.ai/nlu/instructions/manage-entities) | 200 | 4 | Управление сущностями | TWIN |
| [`nlu/instructions/manage-intentions`](https://wiki.twin24.ai/nlu/instructions/manage-intentions) | 200 | 8 | Управление намерениями | TWIN |
| [`nlu/instructions/nlu-testing-guide`](https://wiki.twin24.ai/nlu/instructions/nlu-testing-guide) | 200 | 3 | Оценка обучения NLU-агента | TWIN |
| [`nlu/quick-start`](https://wiki.twin24.ai/nlu/quick-start) | 200 | 7 | Начало работы с NLU | TWIN |
| [`notifications/instructions/distribution-manage`](https://wiki.twin24.ai/notifications/instructions/distribution-manage) | 200 | 4 | Управление рассылками уведомлений | TWIN |
| [`notifications/instructions/manage-templates`](https://wiki.twin24.ai/notifications/instructions/manage-templates) | 200 | 3 | Управление шаблонами уведомлений | TWIN |
| [`notifications/instructions/sender-registration`](https://wiki.twin24.ai/notifications/instructions/sender-registration) | 200 | 1 | Регистрация имени отправителя | TWIN |
| [`notifications/use-cases/session-grade`](https://wiki.twin24.ai/notifications/use-cases/session-grade) | 200 | 0 | Сохранение оценки сессии в отчет | TWIN |
| [`report-master/description-report-master`](https://wiki.twin24.ai/report-master/description-report-master) | 200 | 6 | Работа с отчетами | TWIN |
| [`report-master/export-chat-report`](https://wiki.twin24.ai/report-master/export-chat-report) | 200 | 2 | Экспорт отчета по чатам | TWIN |
| [`report-master/voice-recognition-report`](https://wiki.twin24.ai/report-master/voice-recognition-report) | 200 | 0 | Отчет по распознаванию голоса | TWIN |
| [`scripts/blocks`](https://wiki.twin24.ai/scripts/blocks) | 200 | 0 | Блоки редактора сценариев | TWIN |
| [`scripts/blocks/iterative`](https://wiki.twin24.ai/scripts/blocks/iterative) | 200 | 2 | Порядковый выбор | TWIN |
| [`scripts/blocks/question`](https://wiki.twin24.ai/scripts/blocks/question) | 200 | 18 | Вопрос | TWIN |
| [`scripts/blocks/random`](https://wiki.twin24.ai/scripts/blocks/random) | 200 | 0 | Случайный выбор | TWIN |
| [`scripts/blocks/request-to-server`](https://wiki.twin24.ai/scripts/blocks/request-to-server) | 200 | 6 | Запрос к серверу | TWIN |
| [`scripts/blocks/result`](https://wiki.twin24.ai/scripts/blocks/result) | 200 | 5 | Результат | TWIN |
| [`scripts/blocks/starting-block`](https://wiki.twin24.ai/scripts/blocks/starting-block) | 200 | 14 | Настройки | TWIN |
| [`scripts/blocks/teleport`](https://wiki.twin24.ai/scripts/blocks/teleport) | 200 | 3 | Телепорт | TWIN |
| [`scripts/concepts/active-listening`](https://wiki.twin24.ai/scripts/concepts/active-listening) | 200 | 3 | Активное слушание | TWIN |
| [`scripts/concepts/creating-script`](https://wiki.twin24.ai/scripts/concepts/creating-script) | 200 | 16 | Редактор сценариев | TWIN |
| [`scripts/concepts/formatting-tools-date`](https://wiki.twin24.ai/scripts/concepts/formatting-tools-date) | 200 | 1 | Средства форматирования даты и времени | TWIN |
| [`scripts/concepts/recognition-timers`](https://wiki.twin24.ai/scripts/concepts/recognition-timers) | 200 | 4 | Таймеры и принципы в распознавании речи | TWIN |
| [`scripts/concepts/regular-expressions`](https://wiki.twin24.ai/scripts/concepts/regular-expressions) | 200 | 12 | Регулярные выражения | TWIN |
| [`scripts/concepts/system-variables`](https://wiki.twin24.ai/scripts/concepts/system-variables) | 200 | 2 | Системные переменные в сценарии | TWIN |
| [`scripts/instructions/adding-script`](https://wiki.twin24.ai/scripts/instructions/adding-script) | 200 | 6 | Управление сценариями ботов | TWIN |
| [`scripts/instructions/import-file-to-arrow`](https://wiki.twin24.ai/scripts/instructions/import-file-to-arrow) | 200 | 2 | Импорт условий из шаблона | TWIN |
| [`scripts/instructions/mailing-of-results`](https://wiki.twin24.ai/scripts/instructions/mailing-of-results) | 200 | 2 | Отправка результатов диалога на почту | TWIN |
| [`scripts/use-cases/another-script-transfer`](https://wiki.twin24.ai/scripts/use-cases/another-script-transfer) | 200 | 3 | Переход между сценариями | TWIN |
| [`scripts/use-cases/answer-from-server`](https://wiki.twin24.ai/scripts/use-cases/answer-from-server) | 200 | 3 | Получение информации из ответа сервера | TWIN |
| [`scripts/use-cases/bot-imitator`](https://wiki.twin24.ai/scripts/use-cases/bot-imitator) | 200 | 12 | Работа с ботом-имитатором | TWIN |
| [`scripts/use-cases/date-format-for-calls`](https://wiki.twin24.ai/scripts/use-cases/date-format-for-calls) | 200 | 3 | Изменение формата даты для озвучивания | TWIN |
| [`scripts/use-cases/day-from-date`](https://wiki.twin24.ai/scripts/use-cases/day-from-date) | 200 | 3 | Склонение слова "день" в соответствии с датой | TWIN |
| [`scripts/use-cases/determining-number-gpt`](https://wiki.twin24.ai/scripts/use-cases/determining-number-gpt) | 200 | 0 | Определение числа во фразе с помощью ChatGPT | TWIN |
| [`scripts/use-cases/error-handling`](https://wiki.twin24.ai/scripts/use-cases/error-handling) | 200 | 2 | Поиск ошибки в сценарии | TWIN |
| [`scripts/use-cases/working-nonworking`](https://wiki.twin24.ai/scripts/use-cases/working-nonworking) | 200 | 2 | Определение рабочего дня компании | TWIN |
| [`start/additionally/languages`](https://wiki.twin24.ai/start/additionally/languages) | 200 | 0 | Список доступных языков | TWIN |
| [`tts/tts-markup`](https://wiki.twin24.ai/tts/tts-markup) | 200 | 2 | Разметка синтеза речи | TWIN |
| [`tts/tts-supported-phonemes`](https://wiki.twin24.ai/tts/tts-supported-phonemes) | 200 | 2 | Список поддерживаемых фонем | TWIN |
| [`voice-bots/blacklist`](https://wiki.twin24.ai/voice-bots/blacklist) | 200 | 2 | Черный список | TWIN |
| [`voice-bots/concepts/amd-work`](https://wiki.twin24.ai/voice-bots/concepts/amd-work) | 200 | 3 | AMD в голосовых ботах | TWIN |
| [`voice-bots/concepts/hybrid-synthesis`](https://wiki.twin24.ai/voice-bots/concepts/hybrid-synthesis) | 200 | 3 | Гибридный синтез | TWIN |
| [`voice-bots/concepts/normalization`](https://wiki.twin24.ai/voice-bots/concepts/normalization) | 200 | 2 | Нормализация | TWIN |
| [`voice-bots/concepts/restrictions`](https://wiki.twin24.ai/voice-bots/concepts/restrictions) | 200 | 0 | Ограничения для исходящих вызовов | TWIN |
| [`voice-bots/concepts/stop-words`](https://wiki.twin24.ai/voice-bots/concepts/stop-words) | 200 | 6 | Перебивания | TWIN |
| [`voice-bots/concepts/voicing`](https://wiki.twin24.ai/voice-bots/concepts/voicing) | 200 | 4 | Озвучивание | TWIN |
| [`voice-bots/instructions/manage-templates`](https://wiki.twin24.ai/voice-bots/instructions/manage-templates) | 200 | 4 | Управление шаблонами | TWIN |
| [`voice-bots/instructions/schedule-setting`](https://wiki.twin24.ai/voice-bots/instructions/schedule-setting) | 200 | 3 | Настройка расписания | TWIN |
| [`voice-bots/use-cases/external-telephony-redirect`](https://wiki.twin24.ai/voice-bots/use-cases/external-telephony-redirect) | 200 | 3 | Перевод звонка на оператора (внешняя телефония) | TWIN |
| [`voice-bots/use-cases/hybrid-synthesis`](https://wiki.twin24.ai/voice-bots/use-cases/hybrid-synthesis) | 200 | 5 | Использование гибридного синтеза | TWIN |
| [`voice-bots/use-cases/processing-silence`](https://wiki.twin24.ai/voice-bots/use-cases/processing-silence) | 200 | 0 | Обработка молчания клиента | TWIN |
| [`voice-bots/use-cases/softphone`](https://wiki.twin24.ai/voice-bots/use-cases/softphone) | 200 | 4 | Перевод звонка на оператора через Софтфон | TWIN |
| [`voice-bots/use-cases/voicing`](https://wiki.twin24.ai/voice-bots/use-cases/voicing) | 200 | 5 | Озвучивание сценария с использованием аудиозаписей | TWIN |
