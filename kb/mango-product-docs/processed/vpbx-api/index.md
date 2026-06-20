---
type: kb-source-index
doc_code: VPBXAPI
doc_title: "API Mango Office"
doc_version: "1.9"
status: extracted
ai-generated: true
---

# API Mango Office — индекс БЗ (карта разделов)

> Источник: `kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf` · извлечено: pdfplumber 0.11.10 ·
> токены: tiktoken:cl100k_base. Это **карта поиска** для агента (замена
> retrieval-шага до RAG, ADR-007 R2): найди раздел по колонке «Когда
> обращаться», открой только его файл, процитируй стабильным адресом.

## Как цитировать

`[VPBXAPI, §<номер>, с.<страница>]` — формат проекта (issue #109);
плюс адрес чанка `kb/mango-product-docs/processed/<doc>/sections/<file>#<якорь>` (ADR-007 R3).

## Разделы

| № PDF | Раздел | Файл | Стр. | Источник | Токены | Когда обращаться |
| --- | --- | --- | --- | --- | ---: | --- |
| — | Титульная часть | [sections/00-titulnaya-chast.md](sections/00-titulnaya-chast.md) | 1-6 | ч.1 с.1-6 | 3848 | API MANGO OFFICE |
| — | Определения и сокращения | [sections/01-opredeleniya-i-sokrascheniya.md](sections/01-opredeleniya-i-sokrascheniya.md) | 7 | ч.1 с.7 | 557 | АК — адресная книга MANGO OFFICE, используется в Контакт-центр, M.TALKER. |
| 1 | Основные сведения | [sections/02-osnovnye-svedeniya.md](sections/02-osnovnye-svedeniya.md) | 8 | ч.1 с.8 | 65 | — |
| 1.1 | Назначение | [sections/03-naznachenie.md](sections/03-naznachenie.md) | 8 | ч.1 с.8 | 463 | API MANGO OFFICE (далее по тексту – API) позволяет внешним клиентским системам, |
| 1.2 | Требования совместимости и список поддерживаемых протоколов | [sections/04-trebovaniya-sovmestimosti-i-spisok-podde.md](sections/04-trebovaniya-sovmestimosti-i-spisok-podde.md) | 8 | ч.1 с.8 | 259 | Чтобы взаимодействовать с API, внешняя система должна обеспечивать: |
| 1.3 | Ограничения | [sections/05-ogranicheniya.md](sections/05-ogranicheniya.md) | 8 | ч.1 с.8 | 174 | 1) Не поддерживается протокол TLS версий 1.0, 1.1, 1.3. |
| 1.4 | Лимиты количества запросов к API | [sections/06-limity-kolichestva-zaprosov-k-api.md](sections/06-limity-kolichestva-zaprosov-k-api.md) | 9 | ч.1 с.9 | 128 | В API существуют ограничения на максимальное число запросов в секунду. |
| 1.4.1 | О неверных запросах к API. Ошибка 401 | [sections/07-o-nevernyh-zaprosah-k-api-oshibka-401.md](sections/07-o-nevernyh-zaprosah-k-api-oshibka-401.md) | 9 | ч.1 с.9 | 235 | Если ваш запрос к API MANGO OFFICE неверный, вы получаете код ошибки 3ХХХ. |
| 1.4.2 | API ВАТС | [sections/08-api-vats.md](sections/08-api-vats.md) | 9-10 | ч.1 с.9-10 | 757 | Устанавливаются следующие лимиты запросов в секунду: |
| 1.4.3 | API КЦ | [sections/09-api-kc.md](sections/09-api-kc.md) | 10 | ч.1 с.10 | 243 | Устанавливаются следующие лимиты запросов в секунду: |
| 1.4.4 | Что делать, если получили ошибку 503 и/или 5008? | [sections/10-chto-delat-esli-poluchili-oshibku-503-i.md](sections/10-chto-delat-esli-poluchili-oshibku-503-i.md) | 10 | ч.1 с.10 | 126 | Сделайте паузу или уменьшите интенсивность передачи запросов, или удалите лишние |
| 2 | Общие положения о взаимодействии систем | [sections/11-obschie-polozheniya-o-vzaimodeystvii-sis.md](sections/11-obschie-polozheniya-o-vzaimodeystvii-sis.md) | 11 | ч.1 с.11 | 73 | — |
| 2.1 | Модель авторизации | [sections/12-model-avtorizacii.md](sections/12-model-avtorizacii.md) | 11 | ч.1 с.11 | 296 | API предоставляет внешней системе доступ к своим функциям без ограничений. |
| 2.2 | Модель взаимодействия | [sections/13-model-vzaimodeystviya.md](sections/13-model-vzaimodeystviya.md) | 11 | ч.1 с.11 | 72 | — |
| 2.1.1 | API ВАТС | [sections/14-api-vats.md](sections/14-api-vats.md) | 11-12 | ч.1 с.11-12 | 1441 | Описание модели |
| 2.1.2 | API КЦ | [sections/15-api-kc.md](sections/15-api-kc.md) | 13 | ч.1 с.13 | 271 | Модель взаимодействия API КЦ с внешними системами практически полностью повторяет |
| 2.3 | Работа с услугами Виртуальной АТС | [sections/16-rabota-s-uslugami-virtualnoy-ats.md](sections/16-rabota-s-uslugami-virtualnoy-ats.md) | 13 | ч.1 с.13 | 252 | API предоставляет внешней системе доступ к подключению услуг. |
| 2.4 | Уникальный код вашей ВАТС, ключ для создания подписи и параметр "sign" | [sections/17-unikalnyy-kod-vashey-vats-klyuch-dlya-so.md](sections/17-unikalnyy-kod-vashey-vats-klyuch-dlya-so.md) | 14 | ч.1 с.14 | 89 | "sign" |
| 2.4.1 | Уникальный код вашей ВАТС | [sections/18-unikalnyy-kod-vashey-vats.md](sections/18-unikalnyy-kod-vashey-vats.md) | 14 | ч.1 с.14 | 183 | Уникальный код вашей ВАТС представляет собой строку вида: |
| 2.4.2 | Ключ создания подписи | [sections/19-klyuch-sozdaniya-podpisi.md](sections/19-klyuch-sozdaniya-podpisi.md) | 14 | ч.1 с.14 | 169 | При отправке запросов к API ВАТС используется ключ создания подписи. |
| 2.4.3 | О параметре "sign" | [sections/20-o-parametre-sign.md](sections/20-o-parametre-sign.md) | 14 | ч.1 с.14 | 235 | Данные, которыми обмениваются системы, как правило, будут передаваться в теле POST- |
| 2.4.4 | Поле json | [sections/21-pole-json.md](sections/21-pole-json.md) | 15 | ч.1 с.15 | 256 | Поле json можно рассматривать как ассоциативный массив любой вложенности и размера |
| 2.4.5 | Как узнать свой уникальный код ВАТС и ключ создания подписи? | [sections/22-kak-uznat-svoy-unikalnyy-kod-vats-i-klyu.md](sections/22-kak-uznat-svoy-unikalnyy-kod-vats-i-klyu.md) | 15 | ч.1 с.15 | 263 | Для этого в Личном кабинете MANGO OFFICE следует: |
| 2.5 | Эмулятор API Виртуальной АТС | [sections/23-emulyator-api-virtualnoy-ats.md](sections/23-emulyator-api-virtualnoy-ats.md) | 15 | ч.1 с.15 | 119 | Для удобства знакомства с API ВАТС разработан и размещен на сайте Эмулятор API |
| 3 | Описание методов API Виртуальной АТС MANGO OFFICE | [sections/24-opisanie-metodov-api-virtualnoy-ats-mang.md](sections/24-opisanie-metodov-api-virtualnoy-ats-mang.md) | 16 | ч.1 с.16 | 75 | — |
| 3.1 | API Realtime | [sections/25-api-realtime.md](sections/25-api-realtime.md) | 16 | ч.1 с.16 | 65 | — |
| 3.1.1 | Общее | [sections/26-obschee.md](sections/26-obschee.md) | 16 | ч.1 с.16 | 270 | API Realtime представляет собой набор запросов (уведомлений), которые направляются |
| 3.1.2 | Уведомление о вызове | [sections/27-uvedomlenie-o-vyzove.md](sections/27-uvedomlenie-o-vyzove.md) | 16-22 | ч.1 с.16-22 | 5271 | POST https://external-system.com/events/call |
| 3.1.3 | Уведомление о результате отправки SMS | [sections/28-uvedomlenie-o-rezultate-otpravki-sms.md](sections/28-uvedomlenie-o-rezultate-otpravki-sms.md) | 22 | ч.1 с.22 | 388 | POST https://external-system.com/events/sms |
| 3.1.4 | Уведомление о записи разговора | [sections/29-uvedomlenie-o-zapisi-razgovora.md](sections/29-uvedomlenie-o-zapisi-razgovora.md) | 22-26 | ч.1 с.22-26 | 1982 | POST https://external-system.com/events/recording |
| 3.1.5 | Уведомление о нажатиях DTMF клавиш | [sections/30-uvedomlenie-o-nazhatiyah-dtmf-klavish.md](sections/30-uvedomlenie-o-nazhatiyah-dtmf-klavish.md) | 26 | ч.1 с.26 | 734 | POST https://external-system.com/events/dtmf |
| 3.1.5 | О параметре location | [sections/31-o-parametre-location.md](sections/31-o-parametre-location.md) | 26-27 | ч.1 с.26-27 | 526 | Параметр location состоит из двух определителей и имеет следующий формат: |
| 3.1.6 | Уведомление о завершении вызова | [sections/32-uvedomlenie-o-zavershenii-vyzova.md](sections/32-uvedomlenie-o-zavershenii-vyzova.md) | 27-31 | ч.1 с.27-31 | 3054 | POST https://external-system.com/events/summary |
| 3.1.7 | Событие о завершении процесса распознавания тематик в разговорах | [sections/33-sobytie-o-zavershenii-processa-raspoznav.md](sections/33-sobytie-o-zavershenii-processa-raspoznav.md) | 31-32 | ч.1 с.31-32 | 602 | POST https://external-system.com/events/record/tagged |
| 3.1.8 | Событие о помещении записи разговора в облачное хранилище | [sections/34-sobytie-o-pomeschenii-zapisi-razgovora-v.md](sections/34-sobytie-o-pomeschenii-zapisi-razgovora-v.md) | 32 | ч.1 с.32 | 609 | POST https://external-system.com/events/record/added |
| 3.2 | API Команды | [sections/35-api-komandy.md](sections/35-api-komandy.md) | 33 | ч.1 с.33 | 234 | API Команды представляет собой набор запросов, которые инициирует внешняя система и |
| 3.2.1 | Инициирование вызова от имени сотрудника | [sections/36-iniciirovanie-vyzova-ot-imeni-sotrudnika.md](sections/36-iniciirovanie-vyzova-ot-imeni-sotrudnika.md) | 33-36 | ч.1 с.33-36 | 1832 | POST /vpbx/commands/callback |
| 3.2.2 | Инициирование вызова от имени группы | [sections/37-iniciirovanie-vyzova-ot-imeni-gruppy.md](sections/37-iniciirovanie-vyzova-ot-imeni-gruppy.md) | 36-38 | ч.1 с.36-38 | 1355 | POST /vpbx/commands/callback_group |
| 3.2.3 | Завершение вызова | [sections/38-zavershenie-vyzova.md](sections/38-zavershenie-vyzova.md) | 38-39 | ч.1 с.38-39 | 898 | POST /vpbx/commands/call/hangup |
| 3.2.4 | Отправка SMS | [sections/39-otpravka-sms.md](sections/39-otpravka-sms.md) | 39-41 | ч.1 с.39-41 | 1460 | POST /vpbx/commands/sms |
| 3.2.5 | Включение записи разговора | [sections/40-vklyuchenie-zapisi-razgovora.md](sections/40-vklyuchenie-zapisi-razgovora.md) | 41-43 | ч.1 с.41-43 | 1438 | POST /vpbx/commands/recording/start |
| 3.2.6 | Включение воспроизведения звукового файла | [sections/41-vklyuchenie-vosproizvedeniya-zvukovogo-f.md](sections/41-vklyuchenie-vosproizvedeniya-zvukovogo-f.md) | 43-45 | ч.1 с.43-45 | 1658 | POST /vpbx/commands/play/start |
| 3.2.7 | Маршрутизация вызова | [sections/42-marshrutizaciya-vyzova.md](sections/42-marshrutizaciya-vyzova.md) | 45-46 | ч.1 с.45-46 | 837 | POST /vpbx/commands/route |
| 3.2.7 | О параметре route | [sections/43-o-parametre-route.md](sections/43-o-parametre-route.md) | 46-49 | ч.1 с.46-49 | 1066 | Команда route может работать в следующих режимах: |
| 3.2.8 | Перевод вызова | [sections/44-perevod-vyzova.md](sections/44-perevod-vyzova.md) | 50-55 | ч.1 с.50-55 | 1977 | POST /vpbx/commands/transfer |
| 3.2.9 | Соединение вызова в режиме OnHold и вызова в режиме Connected | [sections/45-soedinenie-vyzova-v-rezhime-onhold-i-vyz.md](sections/45-soedinenie-vyzova-v-rezhime-onhold-i-vyz.md) | 55-56 | ч.1 с.55-56 | 1213 | POST /commands/calls_connect |
| 3.2.10 | Отмена перевода вызова | [sections/46-otmena-perevoda-vyzova.md](sections/46-otmena-perevoda-vyzova.md) | 57-58 | ч.1 с.57-58 | 888 | POST /commands/transfer_cancel |
| 3.2.11 | Постановка вызова на удержание | [sections/47-postanovka-vyzova-na-uderzhanie.md](sections/47-postanovka-vyzova-na-uderzhanie.md) | 58 | ч.1 с.58 | 79 | — |
| 3.2.11.1 | Описание запроса на удержание вызова | [sections/48-opisanie-zaprosa-na-uderzhanie-vyzova.md](sections/48-opisanie-zaprosa-na-uderzhanie-vyzova.md) | 58 | ч.1 с.58 | 568 | POST /commands/call/hold/on |
| 3.2.11.2 | Получение результата выполнения запроса | [sections/49-poluchenie-rezultata-vypolneniya-zaprosa.md](sections/49-poluchenie-rezultata-vypolneniya-zaprosa.md) | 58-59 | ч.1 с.58-59 | 531 | POST /result/call/hold/on |
| 3.3 | Методы работы с правилами переадресации | [sections/50-metody-raboty-s-pravilami-pereadresacii.md](sections/50-metody-raboty-s-pravilami-pereadresacii.md) | 59 | ч.1 с.59 | 131 | Служат для работы со списком переадресации в ЛК ВАТС из внешней системы. |
| 3.3.1 | Получить список правил переадресации | [sections/51-poluchit-spisok-pravil-pereadresacii.md](sections/51-poluchit-spisok-pravil-pereadresacii.md) | 59-61 | ч.1 с.59-61 | 1829 | POST /vpbx/forwarding/numbers |
| 3.3.2 | Добавление нового правила переадресации | [sections/52-dobavlenie-novogo-pravila-pereadresacii.md](sections/52-dobavlenie-novogo-pravila-pereadresacii.md) | 62-63 | ч.1 с.62-63 | 1711 | POST /vpbx/forwarding/number/add |
| 3.3.3 | Изменение правила переадресации | [sections/53-izmenenie-pravila-pereadresacii.md](sections/53-izmenenie-pravila-pereadresacii.md) | 64-65 | ч.1 с.64-65 | 1586 | POST /vpbx/forwarding/number/change |
| 3.3.4 | Удаление правила переадресации | [sections/54-udalenie-pravila-pereadresacii.md](sections/54-udalenie-pravila-pereadresacii.md) | 65-66 | ч.1 с.65-66 | 461 | POST /vpbx/forwarding/number/remove |
| 3.4 | API Статистика | [sections/55-api-statistika.md](sections/55-api-statistika.md) | 66 | ч.1 с.66 | 138 | Позволяет получить данные истории вызовов с помощью асинхронных запросов. |
| 3.4.1 | Запрос базовой статистики | [sections/56-zapros-bazovoy-statistiki.md](sections/56-zapros-bazovoy-statistiki.md) | 66 | ч.1 с.66 | 125 | Получение базовой статистики состоит из следующих этапов: |
| 3.4.1.1 | Запуск формирования статистики | [sections/57-zapusk-formirovaniya-statistiki.md](sections/57-zapusk-formirovaniya-statistiki.md) | 66-69 | ч.1 с.66-69 | 1805 | POST /vpbx/stats/request |
| 3.4.1.2 | Получение статистики вызовов | [sections/58-poluchenie-statistiki-vyzovov.md](sections/58-poluchenie-statistiki-vyzovov.md) | 69-71 | ч.1 с.69-71 | 1820 | Подготовленные данные хранятся до обращения за ними не менее 1 минуты. |
| 3.4.2 | Запрос расширенной статистики | [sections/59-zapros-rasshirennoy-statistiki.md](sections/59-zapros-rasshirennoy-statistiki.md) | 71 | ч.1 с.71 | 79 | — |
| 3.4.2.1 | Обзор | [sections/60-obzor.md](sections/60-obzor.md) | 71 | ч.1 с.71 | 242 | Запрос расширенной статистики – это новый вид запроса, обработка которого оптимизирована |
| 3.4.2.2 | Запуск формирования статистики | [sections/61-zapusk-formirovaniya-statistiki.md](sections/61-zapusk-formirovaniya-statistiki.md) | 71-72 | ч.1 с.71-72 | 1365 | POST /vpbx/stats/calls/request |
| 3.4.2.3 | Получение статистики вызовов | [sections/62-poluchenie-statistiki-vyzovov.md](sections/62-poluchenie-statistiki-vyzovov.md) | 72-88 | ч.1 с.72-88 | 9001 | Подготовленные данные хранятся до обращения за ними не менее 1 минуты. |
| 3.5 | API Записи разговоров, Речевая Аналитика | [sections/63-api-zapisi-razgovorov-rechevaya-analitik.md](sections/63-api-zapisi-razgovorov-rechevaya-analitik.md) | 88-89 | ч.1 с.88-89 | 552 | Речевая Аналитика (далее по тексту – РА) – это сервис, который позволяет расшифровывать и |
| 3.5.1 | Получение записи разговора посредством POST запроса | [sections/64-poluchenie-zapisi-razgovora-posredstvom.md](sections/64-poluchenie-zapisi-razgovora-posredstvom.md) | 89-90 | ч.1 с.89-90 | 466 | POST /vpbx/queries/recording/post |
| 3.5.2 | Получение записи разговора посредством GET запроса без авторизации | [sections/65-poluchenie-zapisi-razgovora-posredstvom.md](sections/65-poluchenie-zapisi-razgovora-posredstvom.md) | 90-91 | ч.1 с.90-91 | 729 | GET |
| 3.5.3 | Прямая ссылка на запись разговора с авторизацией через Личный кабинет | [sections/66-pryamaya-ssylka-na-zapis-razgovora-s-avt.md](sections/66-pryamaya-ssylka-na-zapis-razgovora-s-avt.md) | 91 | ч.1 с.91 | 639 | GET /vpbx/queries/recording/issa/[recording_id]/[action] |
| 3.5.4 | Получение тематик разговора (Speech2Text) | [sections/67-poluchenie-tematik-razgovora-speech2text.md](sections/67-poluchenie-tematik-razgovora-speech2text.md) | 91-93 | ч.1 с.91-93 | 1482 | POST /vpbx/queries/recording_categories |
| 3.5.5 | Получение списка расшифровок распознанных разговоров | [sections/68-poluchenie-spiska-rasshifrovok-raspoznan.md](sections/68-poluchenie-spiska-rasshifrovok-raspoznan.md) | 93-95 | ч.1 с.93-95 | 956 | POST /vpbx/queries/recording_transcripts |
| 3.5.6 | Запрос информации о конспекте разговора | [sections/69-zapros-informacii-o-konspekte-razgovora.md](sections/69-zapros-informacii-o-konspekte-razgovora.md) | 95 | ч.1 с.95 | 627 | POST /s2t/queries/recording_summary |
| 3.5.7 | Запрос записей с расшифровками звонков | [sections/70-zapros-zapisey-s-rasshifrovkami-zvonkov.md](sections/70-zapros-zapisey-s-rasshifrovkami-zvonkov.md) | 96-97 | ч.1 с.96-97 | 1019 | POST /s2t/queries/records |
| 3.6 | Сквозная аналитика. | [sections/71-skvoznaya-analitika.md](sections/71-skvoznaya-analitika.md) | 98 | ч.1 с.98 | 102 | Методы данного раздела работают только если используется Динамический коллтрекинг |
| 3.6.1 | Запрос информации о посетителе сайта по динамическому номеру | [sections/72-zapros-informacii-o-posetitele-sayta-po.md](sections/72-zapros-informacii-o-posetitele-sayta-po.md) | 98-99 | ч.1 с.98-99 | 1348 | POST /vpbx/queries/user_info_by_dct_number |
| 3.6.2 | Запрос истории навигации посетителя сайта по динамическому номеру | [sections/73-zapros-istorii-navigacii-posetitelya-say.md](sections/73-zapros-istorii-navigacii-posetitelya-say.md) | 99-100 | ч.1 с.99-100 | 512 | POST /vpbx/queries/user_history_by_dct_number |
| 3.7 | API Конфигурация | [sections/74-api-konfiguraciya.md](sections/74-api-konfiguraciya.md) | 100 | ч.1 с.100 | 117 | API Конфигурация — служит для управления параметрами Виртуальной АТС, а также |
| 3.7.1 | Запрос списка сотрудников ВАТС | [sections/75-zapros-spiska-sotrudnikov-vats.md](sections/75-zapros-spiska-sotrudnikov-vats.md) | 101-109 | ч.1 с.101-109 | 3838 | POST /vpbx/config/users/request |
| 3.7.2 | Получить список групп | [sections/76-poluchit-spisok-grupp.md](sections/76-poluchit-spisok-grupp.md) | 109-112 | ч.1 с.109-112 | 2092 | POST /vpbx/groups |
| 3.7.3 | Добавить группу | [sections/77-dobavit-gruppu.md](sections/77-dobavit-gruppu.md) | 112-114 | ч.1 с.112-114 | 1840 | POST /vpbx/group/create |
| 3.7.4 | Редактировать группу | [sections/78-redaktirovat-gruppu.md](sections/78-redaktirovat-gruppu.md) | 114-116 | ч.1 с.114-116 | 2159 | POST /vpbx/group/update |
| 3.7.5 | Удалить группу | [sections/79-udalit-gruppu.md](sections/79-udalit-gruppu.md) | 116-117 | ч.1 с.116-117 | 530 | POST /vpbx/group/delete |
| 3.7.6 | Получение баланса | [sections/80-poluchenie-balansa.md](sections/80-poluchenie-balansa.md) | 117-118 | ч.1 с.117-118 | 411 | POST /vpbx/account/balance |
| 3.7.7 | Получение списка номеров ВАТС | [sections/81-poluchenie-spiska-nomerov-vats.md](sections/81-poluchenie-spiska-nomerov-vats.md) | 118-119 | ч.1 с.118-119 | 854 | POST /vpbx/incominglines |
| 3.7.8 | Получение списка мелодий и звуковых сообщений | [sections/82-poluchenie-spiska-melodiy-i-zvukovyh-soo.md](sections/82-poluchenie-spiska-melodiy-i-zvukovyh-soo.md) | 119-120 | ч.1 с.119-120 | 590 | POST /vpbx/audiofiles |
| 3.7.9 | Получение списка схем переадресаций | [sections/83-poluchenie-spiska-shem-pereadresaciy.md](sections/83-poluchenie-spiska-shem-pereadresaciy.md) | 120-122 | ч.1 с.120-122 | 1118 | POST /vpbx/schemas |
| 3.7.10 | Установить схему на входящем номере | [sections/84-ustanovit-shemu-na-vhodyaschem-nomere.md](sections/84-ustanovit-shemu-na-vhodyaschem-nomere.md) | 122-124 | ч.1 с.122-124 | 721 | POST /vpbx/schema/set |
| 3.7.11 | Получить список ролей | [sections/85-poluchit-spisok-roley.md](sections/85-poluchit-spisok-roley.md) | 124-125 | ч.1 с.124-125 | 593 | POST /vpbx/roles |
| 3.7.12 | Создать сотрудника | [sections/86-sozdat-sotrudnika.md](sections/86-sozdat-sotrudnika.md) | 125-127 | ч.1 с.125-127 | 1606 | POST /vpbx/member/create |
| 3.7.13 | Редактировать сотрудника | [sections/87-redaktirovat-sotrudnika.md](sections/87-redaktirovat-sotrudnika.md) | 127 | ч.1 с.127 | 155 | Метод позволяет редактировать данные сотрудника Виртуальной АТС. |
| 3.7.13.1 | Ограничения | [sections/88-ogranicheniya.md](sections/88-ogranicheniya.md) | 127 | ч.1 с.127 | 309 | Необходимо учитывать следующие факторы: |
| 3.7.13.2 | Описание метода | [sections/89-opisanie-metoda.md](sections/89-opisanie-metoda.md) | 127-129 | ч.1 с.127-129 | 1734 | POST /vpbx/member/update |
| 3.7.14 | Удалить сотрудника | [sections/90-udalit-sotrudnika.md](sections/90-udalit-sotrudnika.md) | 130 | ч.1 с.130 | 419 | POST /vpbx/member/delete |
| 3.7.15 | Получить список индивидуальных правил автосекретаря для сотрудников | [sections/91-poluchit-spisok-individualnyh-pravil-avt.md](sections/91-poluchit-spisok-individualnyh-pravil-avt.md) | 130-133 | ч.1 с.130-133 | 1903 | POST /vpbx/autosecretary/rules |
| 3.7.16 | Изменить статус индивидуальных правил автосекретаря сотрудника | [sections/92-izmenit-status-individualnyh-pravil-avto.md](sections/92-izmenit-status-individualnyh-pravil-avto.md) | 133 | ч.1 с.133 | 547 | POST /vpbx/autosecretary/status/change |
| 3.7.17 | Получить sip учетные записи сотрудников | [sections/93-poluchit-sip-uchetnye-zapisi-sotrudnikov.md](sections/93-poluchit-sip-uchetnye-zapisi-sotrudnikov.md) | 134 | ч.1 с.134 | 506 | POST /vpbx/sips |
| 3.7.18 | Получить настроенные домены | [sections/94-poluchit-nastroennye-domeny.md](sections/94-poluchit-nastroennye-domeny.md) | 135 | ч.1 с.135 | 351 | POST /vpbx/domains |
| 3.7.19 | Создать sip-учетку | [sections/95-sozdat-sip-uchetku.md](sections/95-sozdat-sip-uchetku.md) | 135-136 | ч.1 с.135-136 | 608 | POST /vpbx/sip/create |
| 3.7.20 | Редактировать sip-учетку | [sections/96-redaktirovat-sip-uchetku.md](sections/96-redaktirovat-sip-uchetku.md) | 136-137 | ч.1 с.136-137 | 733 | POST /vpbx/sip/update |
| 3.7.21 | Удалить sip-учетку | [sections/97-udalit-sip-uchetku.md](sections/97-udalit-sip-uchetku.md) | 137-138 | ч.1 с.137-138 | 404 | POST /vpbx/sip/delete |
| 3.7.22 | Запрос номеров sip-trunk'ов | [sections/98-zapros-nomerov-sip-trunk-ov.md](sections/98-zapros-nomerov-sip-trunk-ov.md) | 138-139 | ч.1 с.138-139 | 583 | POST /vpbx/trunks/numbers |
| 3.8 | API запрещенных направлений вызова | [sections/99-api-zapreschennyh-napravleniy-vyzova.md](sections/99-api-zapreschennyh-napravleniy-vyzova.md) | 139 | ч.1 с.139 | 75 | — |
| 3.8.1 | Общее | [sections/100-obschee.md](sections/100-obschee.md) | 139 | ч.1 с.139 | 360 | При помощи данных методов API вы можете ограничить прием и совершение вызовов через |
| 3.8.2 | Ограничение входящих коммуникаций | [sections/101-ogranichenie-vhodyaschih-kommunikaciy.md](sections/101-ogranichenie-vhodyaschih-kommunikaciy.md) | 139 | ч.1 с.139 | 83 | — |
| 3.8.2.1 | Получение текущего режима работы ч/б списка | [sections/102-poluchenie-tekuschego-rezhima-raboty-ch.md](sections/102-poluchenie-tekuschego-rezhima-raboty-ch.md) | 139-140 | ч.1 с.139-140 | 506 | POST /vpbx/bwlists/state/ |
| 3.8.2.2 | Получнение списка номеров, входящих в ч/б списки ВАТС | [sections/103-poluchnenie-spiska-nomerov-vhodyaschih-v.md](sections/103-poluchnenie-spiska-nomerov-vhodyaschih-v.md) | 140-142 | ч.1 с.140-142 | 993 | POST /vpbx/bwlists/numbers/ |
| 3.8.2.3 | Добавление номера в ч/б список ВАТС | [sections/104-dobavlenie-nomera-v-ch-b-spisok-vats.md](sections/104-dobavlenie-nomera-v-ch-b-spisok-vats.md) | 142-143 | ч.1 с.142-143 | 725 | POST /vpbx/bwlists/number/add/ |
| 3.8.2.4 | Удаление номера из ч/б списка ВАТС | [sections/105-udalenie-nomera-iz-ch-b-spiska-vats.md](sections/105-udalenie-nomera-iz-ch-b-spiska-vats.md) | 143 | ч.1 с.143 | 430 | POST /vpbx/bwlists/number/delete/ |
| 3.8.3 | Ограничение исходящих коммуникаций | [sections/106-ogranichenie-ishodyaschih-kommunikaciy.md](sections/106-ogranichenie-ishodyaschih-kommunikaciy.md) | 143 | ч.1 с.143 | 84 | — |
| 3.8.3.1 | Получение списка номеров, включенных в "черный" список ИО | [sections/107-poluchenie-spiska-nomerov-vklyuchennyh-v.md](sections/107-poluchenie-spiska-nomerov-vklyuchennyh-v.md) | 144-145 | ч.1 с.144-145 | 1164 | POST /vpbx/outbound_blacklist/get |
| 3.8.3.2 | Добавление номера в "черный" список ИО | [sections/108-dobavlenie-nomera-v-chernyy-spisok-io.md](sections/108-dobavlenie-nomera-v-chernyy-spisok-io.md) | 145-147 | ч.1 с.145-147 | 1143 | POST /vpbx/outbound_blacklist/add |
| 3.8.3.3 | Обновление описания номера в "черном" списке ИО | [sections/109-obnovlenie-opisaniya-nomera-v-chernom-sp.md](sections/109-obnovlenie-opisaniya-nomera-v-chernom-sp.md) | 147-148 | ч.1 с.147-148 | 711 | POST /vpbx/outbound_blacklist/update_description |
| 3.8.3.4 | Блокировка номера, внесенного в "черный" список ИО | [sections/110-blokirovka-nomera-vnesennogo-v-chernyy-s.md](sections/110-blokirovka-nomera-vnesennogo-v-chernyy-s.md) | 148-149 | ч.1 с.148-149 | 839 | POST /vpbx/outbound_blacklist/enable_mode |
| 3.8.3.5 | Разблокировка номера, внесенного в "черный" список ИО | [sections/111-razblokirovka-nomera-vnesennogo-v-cherny.md](sections/111-razblokirovka-nomera-vnesennogo-v-cherny.md) | 149-150 | ч.1 с.149-150 | 812 | POST /vpbx/outbound_blacklist/disable_mode |
| 3.8.3.6 | Удаление номера из "черного" списка ИО | [sections/112-udalenie-nomera-iz-chernogo-spiska-io.md](sections/112-udalenie-nomera-iz-chernogo-spiska-io.md) | 150-151 | ч.1 с.150-151 | 643 | POST /vpbx/outbound_blacklist/delete |
| 3.8.3.7 | Включение запрета на все исходящие коммуникации | [sections/113-vklyuchenie-zapreta-na-vse-ishodyaschie.md](sections/113-vklyuchenie-zapreta-na-vse-ishodyaschie.md) | 151 | ч.1 с.151 | 484 | POST /vpbx/outbound_blacklist/enable |
| 3.8.3.8 | Выключение запрета на все исходящие коммуникации | [sections/114-vyklyuchenie-zapreta-na-vse-ishodyaschie.md](sections/114-vyklyuchenie-zapreta-na-vse-ishodyaschie.md) | 151-152 | ч.1 с.151-152 | 368 | POST /vpbx/outbound_blacklist/disable |
| 3.9 | API для работы с адресной книгой | [sections/115-api-dlya-raboty-s-adresnoy-knigoy.md](sections/115-api-dlya-raboty-s-adresnoy-knigoy.md) | 152 | ч.1 с.152 | 168 | Возможности API, указанные в данном разделе, служат для управления адресной книгой |
| 3.9.1 | Организации | [sections/116-organizacii.md](sections/116-organizacii.md) | 152 | ч.1 с.152 | 71 | — |
| 3.9.1.1 | Получить организацию по id | [sections/117-poluchit-organizaciyu-po-id.md](sections/117-poluchit-organizaciyu-po-id.md) | 152-153 | ч.1 с.152-153 | 463 | POST /vpbx/ab/organization |
| 3.9.1.2 | Получить список организаций, инициация отчета | [sections/118-poluchit-spisok-organizaciy-iniciaciya-o.md](sections/118-poluchit-spisok-organizaciy-iniciaciya-o.md) | 153-155 | ч.1 с.153-155 | 1383 | POST /vpbx/ab/organizations/init |
| 3.9.1.3 | Получить список организаций, постраничное получение | [sections/119-poluchit-spisok-organizaciy-postranichno.md](sections/119-poluchit-spisok-organizaciy-postranichno.md) | 155-157 | ч.1 с.155-157 | 1406 | POST /vpbx/ab/organizations/cursor |
| 3.9.1.4 | Добавить организацию | [sections/120-dobavit-organizaciyu.md](sections/120-dobavit-organizaciyu.md) | 157-158 | ч.1 с.157-158 | 688 | POST /vpbx/ab/organizations/create |
| 3.9.1.5 | Редактировать организацию | [sections/121-redaktirovat-organizaciyu.md](sections/121-redaktirovat-organizaciyu.md) | 158-159 | ч.1 с.158-159 | 695 | POST /vpbx/ab/organizations/update |
| 3.9.1.6 | Удалить организацию | [sections/122-udalit-organizaciyu.md](sections/122-udalit-organizaciyu.md) | 159-160 | ч.1 с.159-160 | 493 | POST /vpbx/ab/organizations/delete |
| 3.9.2 | Группы | [sections/123-gruppy.md](sections/123-gruppy.md) | 160 | ч.1 с.160 | 69 | — |
| 3.9.2.1 | Получить группу по id | [sections/124-poluchit-gruppu-po-id.md](sections/124-poluchit-gruppu-po-id.md) | 160-161 | ч.1 с.160-161 | 451 | POST /vpbx/ab/group |
| 3.9.2.2 | Получить список групп, инициация отчета | [sections/125-poluchit-spisok-grupp-iniciaciya-otcheta.md](sections/125-poluchit-spisok-grupp-iniciaciya-otcheta.md) | 161-162 | ч.1 с.161-162 | 1351 | POST /vpbx/ab/groups/init |
| 3.9.2.3 | Получить список групп, постраничное получение | [sections/126-poluchit-spisok-grupp-postranichnoe-polu.md](sections/126-poluchit-spisok-grupp-postranichnoe-polu.md) | 162-164 | ч.1 с.162-164 | 1437 | POST /vpbx/ab/groups/cursor |
| 3.9.2.4 | Добавить группу | [sections/127-dobavit-gruppu.md](sections/127-dobavit-gruppu.md) | 164-165 | ч.1 с.164-165 | 613 | POST /vpbx/ab/groups/create/ |
| 3.9.2.5 | Редактировать группу | [sections/128-redaktirovat-gruppu.md](sections/128-redaktirovat-gruppu.md) | 165-166 | ч.1 с.165-166 | 668 | POST /vpbx/ab/groups/update |
| 3.9.2.6 | Удалить группу | [sections/129-udalit-gruppu.md](sections/129-udalit-gruppu.md) | 166-167 | ч.1 с.166-167 | 397 | POST /vpbx/ab/groups/delete |
| 3.9.3 | Контакты | [sections/130-kontakty.md](sections/130-kontakty.md) | 167 | ч.1 с.167 | 70 | — |
| 3.9.3.1 | Получить список контактов, инициация отчета | [sections/131-poluchit-spisok-kontaktov-iniciaciya-otc.md](sections/131-poluchit-spisok-kontaktov-iniciaciya-otc.md) | 167-172 | ч.1 с.167-172 | 3651 | POST /vpbx/ab/contact/init |
| 3.9.3.2 | Получить список контактов, постраничное получение | [sections/132-poluchit-spisok-kontaktov-postranichnoe.md](sections/132-poluchit-spisok-kontaktov-postranichnoe.md) | 172-176 | ч.1 с.172-176 | 3539 | POST /vpbx/ab/contact/cursor |
| 3.9.3.3 | Получить контакт по id | [sections/133-poluchit-kontakt-po-id.md](sections/133-poluchit-kontakt-po-id.md) | 176-179 | ч.1 с.176-179 | 2582 | POST /vpbx/ab/contact |
| 3.9.3.4 | Добавить контакт | [sections/134-dobavit-kontakt.md](sections/134-dobavit-kontakt.md) | 179-186 | ч.1 с.179-186 | 3759 | POST /vpbx/ab/contacts/create/ |
| 3.9.3.5 | Редактировать контакт | [sections/135-redaktirovat-kontakt.md](sections/135-redaktirovat-kontakt.md) | 186-190 | ч.1 с.186-190 | 3756 | POST /vpbx/ab/contacts/update |
| 3.9.3.6 | Удалить контакт | [sections/136-udalit-kontakt.md](sections/136-udalit-kontakt.md) | 190-191 | ч.1 с.190-191 | 398 | POST /vpbx/ab/contacts/delete |
| 3.9.4 | Уведомление об операциях с адресной книгой | [sections/137-uvedomlenie-ob-operaciyah-s-adresnoy-kni.md](sections/137-uvedomlenie-ob-operaciyah-s-adresnoy-kni.md) | 191 | ч.1 с.191 | 81 | — |
| 3.9.4.1 | Обзор | [sections/138-obzor.md](sections/138-obzor.md) | 191 | ч.1 с.191 | 164 | POST https://external-system.com/events/ab/ |
| 3.9.4.2 | Для организаций | [sections/139-dlya-organizaciy.md](sections/139-dlya-organizaciy.md) | 191-192 | ч.1 с.191-192 | 659 | Параметры: |
| 3.9.4.3 | Для групп | [sections/140-dlya-grupp.md](sections/140-dlya-grupp.md) | 192-194 | ч.1 с.192-194 | 901 | Параметры: |
| 3.9.4.4 | Для контактов | [sections/141-dlya-kontaktov.md](sections/141-dlya-kontaktov.md) | 194-196 | ч.1 с.194-196 | 2361 | Параметры запроса: |
| 3.9.5 | Получение набора пользовательских полей | [sections/142-poluchenie-nabora-polzovatelskih-poley.md](sections/142-poluchenie-nabora-polzovatelskih-poley.md) | 196-198 | ч.1 с.196-198 | 1184 | POST /vpbx/ab/custom_fields/ |
| 3.10 | API для работы с записями и метаданными, полученными из оффлайн-источников | [sections/143-api-dlya-raboty-s-zapisyami-i-metadannym.md](sections/143-api-dlya-raboty-s-zapisyami-i-metadannym.md) | 198-199 | ч.1 с.198-199 | 157 | оффлайн-источников |
| 3.10.1 | Загрузка и распознавание речи в WAV-файле с привязкой к сотруднику | [sections/144-zagruzka-i-raspoznavanie-rechi-v-wav-fay.md](sections/144-zagruzka-i-raspoznavanie-rechi-v-wav-fay.md) | 199 | ч.1 с.199 | 100 | — |
| 3.10.1.1 | Обзор | [sections/145-obzor.md](sections/145-obzor.md) | 199 | ч.1 с.199 | 452 | Метод обеспечивает загрузку в ВАТС и распознавание речи в звуковом файле, который |
| 3.10.1.2 | Требования и рекомендации | [sections/146-trebovaniya-i-rekomendacii.md](sections/146-trebovaniya-i-rekomendacii.md) | 199 | ч.1 с.199 | 296 | Чтобы использовать данный метод, необходимо в вашей ВАТС подключить услуги: |
| 3.10.1.3 | Описание метода | [sections/147-opisanie-metoda.md](sections/147-opisanie-metoda.md) | 199-201 | ч.1 с.199-201 | 1585 | POST /vpbx/offline_record/recognize |
| 3.10.2 | Загрузка и распознавание речи в WAV-файле без сохранения в ВАТС и без привязки к сотруднику | [sections/148-zagruzka-i-raspoznavanie-rechi-v-wav-fay.md](sections/148-zagruzka-i-raspoznavanie-rechi-v-wav-fay.md) | 201 | ч.1 с.201 | 121 | привязки к сотруднику |
| 3.10.2.1 | Обзор | [sections/149-obzor.md](sections/149-obzor.md) | 201-202 | ч.1 с.201-202 | 488 | Метод обеспечивает загрузку в ВАТС и распознавание речи в звуковом файле, при этом |
| 3.10.2.2 | Описание метода | [sections/150-opisanie-metoda.md](sections/150-opisanie-metoda.md) | 202-203 | ч.1 с.202-203 | 825 | POST /vpbx/record/recognize |
| 3.10.3 | Событие о завершении распознавания речи в WAV-файле | [sections/151-sobytie-o-zavershenii-raspoznavaniya-rec.md](sections/151-sobytie-o-zavershenii-raspoznavaniya-rec.md) | 203 | ч.1 с.203 | 462 | POST /events/recognized/offline |
| 3.10.4 | Получение результата распознавания речи в WAV-файле | [sections/152-poluchenie-rezultata-raspoznavaniya-rech.md](sections/152-poluchenie-rezultata-raspoznavaniya-rech.md) | 204-206 | ч.1 с.204-206 | 1134 | POST /vpbx/transcribes/tasks/ |
| 4 | Описание методов API Контакт-центра MANGO OFFICE | [sections/153-opisanie-metodov-api-kontakt-centra-mang.md](sections/153-opisanie-metodov-api-kontakt-centra-mang.md) | 207 | ч.1 с.207 | 75 | — |
| 4.1 | Основное | [sections/154-osnovnoe.md](sections/154-osnovnoe.md) | 207 | ч.1 с.207 | 398 | 1) Этот API позволяет обращаться к некоторым функциям и данными Контакт-центра |
| 4.2 | Подключение и настройка API КЦ | [sections/155-podklyuchenie-i-nastroyka-api-kc.md](sections/155-podklyuchenie-i-nastroyka-api-kc.md) | 208-209 | ч.1 с.208-209 | 569 | Чтобы у вас появилась возможность работы с API КЦ, нужно подключить услугу "Открытое |
| 4.3 | Управление задачей на автоперезвон | [sections/156-upravlenie-zadachey-na-avtoperezvon.md](sections/156-upravlenie-zadachey-na-avtoperezvon.md) | 210 | ч.1 с.210 | 76 | — |
| 4.3.1 | Создание задачи на автоперезвон | [sections/157-sozdanie-zadachi-na-avtoperezvon.md](sections/157-sozdanie-zadachi-na-avtoperezvon.md) | 210-211 | ч.1 с.210-211 | 1327 | POST /cc/task/add |
| 4.3.2 | Изменение задачи на автоперезвон | [sections/158-izmenenie-zadachi-na-avtoperezvon.md](sections/158-izmenenie-zadachi-na-avtoperezvon.md) | 211-213 | ч.1 с.211-213 | 1607 | POST /cc/task/update |
| 4.3.3 | Получение задачи по ID | [sections/159-poluchenie-zadachi-po-id.md](sections/159-poluchenie-zadachi-po-id.md) | 213-214 | ч.1 с.213-214 | 1150 | POST /cc/task/get |
| 4.3.4 | Получение списка задач | [sections/160-poluchenie-spiska-zadach.md](sections/160-poluchenie-spiska-zadach.md) | 215-217 | ч.1 с.215-217 | 1830 | POST /cc/task/list |
| 4.3.5 | Завершение задачи | [sections/161-zavershenie-zadachi.md](sections/161-zavershenie-zadachi.md) | 217 | ч.1 с.217 | 378 | POST /cc/task/done |
| 4.3.6 | Отмена задачи | [sections/162-otmena-zadachi.md](sections/162-otmena-zadachi.md) | 218 | ч.1 с.218 | 377 | POST /cc/task/cancel |
| 4.4 | Управление статусами и сессиями пользователя | [sections/163-upravlenie-statusami-i-sessiyami-polzova.md](sections/163-upravlenie-statusami-i-sessiyami-polzova.md) | 218 | ч.1 с.218 | 75 | — |
| 4.4.1 | Статусы | [sections/164-statusy.md](sections/164-statusy.md) | 218 | ч.1 с.218 | 71 | — |
| 4.4.1.1 | Что означает статус пользователя | [sections/165-chto-oznachaet-status-polzovatelya.md](sections/165-chto-oznachaet-status-polzovatelya.md) | 218-219 | ч.1 с.218-219 | 461 | Статус - это атрибут пользователя, который определяет его готовность к приему вызовов. |
| 4.4.1.2 | Коды статусов | [sections/166-kody-statusov.md](sections/166-kody-statusov.md) | 219 | ч.1 с.219 | 227 | Здесь перечислены коды статусов пользователей, которые можно использовать при запросах |
| 4.4.1.3 | Смена статуса сессии пользователя | [sections/167-smena-statusa-sessii-polzovatelya.md](sections/167-smena-statusa-sessii-polzovatelya.md) | 219-221 | ч.1 с.219-221 | 1700 | POST /cc/set_session_status |
| 4.4.1.2 | Смена статуса пользователя | [sections/168-smena-statusa-polzovatelya.md](sections/168-smena-statusa-polzovatelya.md) | 221-222 | ч.1 с.221-222 | 622 | POST /cc/set_abonent_status |
| 4.4.1.3 | Статусы пользователей продукта | [sections/169-statusy-polzovateley-produkta.md](sections/169-statusy-polzovateley-produkta.md) | 222-224 | ч.1 с.222-224 | 878 | POST /cc/get_presence |
| 4.4.1.4 | Статусы на продукте | [sections/170-statusy-na-produkte.md](sections/170-statusy-na-produkte.md) | 224-225 | ч.1 с.224-225 | 616 | POST /cc/get_statuses |
| 4.4.2 | События | [sections/171-sobytiya.md](sections/171-sobytiya.md) | 225 | ч.1 с.225 | 69 | — |
| 4.4.2.1 | Изменение статуса пользователя | [sections/172-izmenenie-statusa-polzovatelya.md](sections/172-izmenenie-statusa-polzovatelya.md) | 225 | ч.1 с.225 | 426 | POST /events/user/status_changed |
| 4.4.2.2 | Завершение сессии | [sections/173-zavershenie-sessii.md](sections/173-zavershenie-sessii.md) | 226 | ч.1 с.226 | 384 | POST /events/user/session_end |
| 4.5 | Работа со сделками | [sections/174-rabota-so-sdelkami.md](sections/174-rabota-so-sdelkami.md) | 226 | ч.1 с.226 | 71 | — |
| 4.5.1 | Создание сделки | [sections/175-sozdanie-sdelki.md](sections/175-sozdanie-sdelki.md) | 226-228 | ч.1 с.226-228 | 1392 | POST /cc/deal/create |
| 4.5.2 | Изменение сделки | [sections/176-izmenenie-sdelki.md](sections/176-izmenenie-sdelki.md) | 228-229 | ч.1 с.228-229 | 1289 | POST /cc/deal/update |
| 4.5.3 | Получение сделки по ID | [sections/177-poluchenie-sdelki-po-id.md](sections/177-poluchenie-sdelki-po-id.md) | 230-231 | ч.1 с.230-231 | 1264 | POST /cc/deal/get |
| 4.5.4 | Получение списка сделок | [sections/178-poluchenie-spiska-sdelok.md](sections/178-poluchenie-spiska-sdelok.md) | 231-234 | ч.1 с.231-234 | 2111 | POST /cc/deal/list |
| 4.5.5 | Получение списка пользовательских полей | [sections/179-poluchenie-spiska-polzovatelskih-poley.md](sections/179-poluchenie-spiska-polzovatelskih-poley.md) | 234-237 | ч.1 с.234-237 | 1355 | POST /cc/deal/custom_fields.list |
| 4.5.6 | Получение списка документов сделки | [sections/180-poluchenie-spiska-dokumentov-sdelki.md](sections/180-poluchenie-spiska-dokumentov-sdelki.md) | 237-238 | ч.1 с.237-238 | 685 | POST /cc/deal/documents.list |
| 4.5.7 | Добавление документов к сделке | [sections/181-dobavlenie-dokumentov-k-sdelke.md](sections/181-dobavlenie-dokumentov-k-sdelke.md) | 238-239 | ч.1 с.238-239 | 617 | POST /cc/deal/documents.add |
| 4.5.8 | Получение списка воронок | [sections/182-poluchenie-spiska-voronok.md](sections/182-poluchenie-spiska-voronok.md) | 239-240 | ч.1 с.239-240 | 974 | POST /cc/deal/funnels.list |
| 4.6 | Кампании исходящего обзвона | [sections/183-kampanii-ishodyaschego-obzvona.md](sections/183-kampanii-ishodyaschego-obzvona.md) | 241 | ч.1 с.241 | 77 | — |
| 4.6.1 | Общее | [sections/184-obschee.md](sections/184-obschee.md) | 241 | ч.1 с.241 | 153 | Возможности API КЦ, указанные в данном разделе, служат для управления кампаниями ИО и |
| 4.6.2 | Получение списка задач и подзадач кампаний | [sections/185-poluchenie-spiska-zadach-i-podzadach-kam.md](sections/185-poluchenie-spiska-zadach-i-podzadach-kam.md) | 241-245 | ч.1 с.241-245 | 3205 | POST /vpbx/v2/campaign/tasks |
| 4.6.3 | Получение списка кампаний ИО | [sections/186-poluchenie-spiska-kampaniy-io.md](sections/186-poluchenie-spiska-kampaniy-io.md) | 245-254 | ч.1 с.245-254 | 6323 | POST /vpbx/campaign/list |
| 4.6.4 | Получение информации о кампании | [sections/187-poluchenie-informacii-o-kampanii.md](sections/187-poluchenie-informacii-o-kampanii.md) | 254-259 | ч.1 с.254-259 | 4806 | POST /vpbx/campaign |
| 4.6.4 | Важная информация | [sections/188-vazhnaya-informaciya.md](sections/188-vazhnaya-informaciya.md) | 259 | ч.1 с.259 | 401 | При создании кампании ИО необходимо использовать данные о: |
| 4.6.4 | Описание запроса на создание кампании ИО | [sections/189-opisanie-zaprosa-na-sozdanie-kampanii-io.md](sections/189-opisanie-zaprosa-na-sozdanie-kampanii-io.md) | 259-263 | ч.1 с.259-263 | 4200 | POST /vpbx/campaign/add |
| 4.6.6 | Обновление кампании | [sections/190-obnovlenie-kampanii.md](sections/190-obnovlenie-kampanii.md) | 263-266 | ч.1 с.263-266 | 4114 | POST /vpbx/campaign/update |
| 4.6.7 | Добавление нескольких заданий в кампанию (асинхронный метод) | [sections/191-dobavlenie-neskolkih-zadaniy-v-kampaniyu.md](sections/191-dobavlenie-neskolkih-zadaniy-v-kampaniyu.md) | 267-269 | ч.1 с.267-269 | 1666 | POST /vpbx/tasks/push |
| 4.6.8 | Добавление одного задания в кампанию (синхронный метод) | [sections/192-dobavlenie-odnogo-zadaniya-v-kampaniyu-s.md](sections/192-dobavlenie-odnogo-zadaniya-v-kampaniyu-s.md) | 269-270 | ч.1 с.269-270 | 1539 | POST /vpbx/task/add |
| 4.6.9 | Запуск кампании | [sections/193-zapusk-kampanii.md](sections/193-zapusk-kampanii.md) | 271 | ч.1 с.271 | 406 | POST /vpbx/campaign/start |
| 4.6.10 | Остановка кампании | [sections/194-ostanovka-kampanii.md](sections/194-ostanovka-kampanii.md) | 271-272 | ч.1 с.271-272 | 506 | POST /vpbx/campaign/stop |
| 4.6.11 | Удаление кампании | [sections/195-udalenie-kampanii.md](sections/195-udalenie-kampanii.md) | 272 | ч.1 с.272 | 448 | POST /vpbx/campaign/delete |
| 4.6.12 | Получение информации для генерации отчёта исходящего обзвона | [sections/196-poluchenie-informacii-dlya-generacii-otc.md](sections/196-poluchenie-informacii-dlya-generacii-otc.md) | 273-276 | ч.1 с.273-276 | 2631 | POST /vpbx/campaign-report/create |
| 4.6.13 | Получение информации о задаче кампании ИО | [sections/197-poluchenie-informacii-o-zadache-kampanii.md](sections/197-poluchenie-informacii-o-zadache-kampanii.md) | 277-279 | ч.1 с.277-279 | 2523 | POST /vpbx/task |
| 4.6.14 | Запуск задания кампании ИО | [sections/198-zapusk-zadaniya-kampanii-io.md](sections/198-zapusk-zadaniya-kampanii-io.md) | 279-280 | ч.1 с.279-280 | 330 | POST /vpbx/task/start |
| 4.6.15 | Остановка задания | [sections/199-ostanovka-zadaniya.md](sections/199-ostanovka-zadaniya.md) | 280 | ч.1 с.280 | 394 | POST /vpbx/task/stop |
| 4.6.16 | Удаление задания | [sections/200-udalenie-zadaniya.md](sections/200-udalenie-zadaniya.md) | 280-281 | ч.1 с.280-281 | 327 | POST /vpbx/task/delete |
| 4.6.17 | Обновление задания кампании ИО | [sections/201-obnovlenie-zadaniya-kampanii-io.md](sections/201-obnovlenie-zadaniya-kampanii-io.md) | 281-282 | ч.1 с.281-282 | 691 | POST /vpbx/task/update |
| 4.6.18 | Получение информации о завершенных заданиях кампании ИО | [sections/202-poluchenie-informacii-o-zavershennyh-zad.md](sections/202-poluchenie-informacii-o-zavershennyh-zad.md) | 282 | ч.1 с.282 | 86 | — |
| 4.6.18 | Важная информация | [sections/203-vazhnaya-informaciya.md](sections/203-vazhnaya-informaciya.md) | 282 | ч.1 с.282 | 298 | Этот метод позволяет получить информацию о завершенных заданиях кампании исходящего |
| 4.6.18 | Описание метода | [sections/204-opisanie-metoda.md](sections/204-opisanie-metoda.md) | 282-285 | ч.1 с.282-285 | 2575 | POST /vpbx/tasks/finished |
| 4.6.19 | Сброс попыток выполнения задания кампании ИО | [sections/205-sbros-popytok-vypolneniya-zadaniya-kampa.md](sections/205-sbros-popytok-vypolneniya-zadaniya-kampa.md) | 286 | ч.1 с.286 | 367 | POST /vpbx/tasks/reset |
| 4.6.20 | Получение списка пользовательских полей | [sections/206-poluchenie-spiska-polzovatelskih-poley.md](sections/206-poluchenie-spiska-polzovatelskih-poley.md) | 286-287 | ч.1 с.286-287 | 763 | POST /vpbx/custom-type/list |
| 4.7 | Данные Контакт-центра для звонка | [sections/207-dannye-kontakt-centra-dlya-zvonka.md](sections/207-dannye-kontakt-centra-dlya-zvonka.md) | 287 | ч.1 с.287 | 78 | — |
| 4.7.1 | Получение данных Контакт-центра для звонка | [sections/208-poluchenie-dannyh-kontakt-centra-dlya-zv.md](sections/208-poluchenie-dannyh-kontakt-centra-dlya-zv.md) | 287-291 | ч.1 с.287-291 | 2377 | POST /vpbx/cc/call/ |
| 4.7.2 | Получение списка тематик по продукту | [sections/209-poluchenie-spiska-tematik-po-produktu.md](sections/209-poluchenie-spiska-tematik-po-produktu.md) | 291-293 | ч.1 с.291-293 | 1288 | POST /vpbx/cc/tags/ |
| 4.7.3 | Метод получения информации по скрипту(сценарию) КЦ | [sections/210-metod-polucheniya-informacii-po-skriptu.md](sections/210-metod-polucheniya-informacii-po-skriptu.md) | 293-294 | ч.1 с.293-294 | 689 | POST /vpbx/script/ |
| 4.7.4 | Вопрос для оценки качества работы операторов по обработке вызовов | [sections/211-vopros-dlya-ocenki-kachestva-raboty-oper.md](sections/211-vopros-dlya-ocenki-kachestva-raboty-oper.md) | 294-295 | ч.1 с.294-295 | 789 | POST /vpbx/quality/control/question/ |
| 4.8 | Работа с обращениями в Контакт-центре | [sections/212-rabota-s-obrascheniyami-v-kontakt-centre.md](sections/212-rabota-s-obrascheniyami-v-kontakt-centre.md) | 295 | ч.1 с.295 | 81 | — |
| 4.8.1 | Общее | [sections/213-obschee.md](sections/213-obschee.md) | 295 | ч.1 с.295 | 150 | В этом разделе описаны методы, которые позволяют разово передавать информацию об |
| 4.8.2 | Создание закрытого обращения | [sections/214-sozdanie-zakrytogo-obrascheniya.md](sections/214-sozdanie-zakrytogo-obrascheniya.md) | 296-298 | ч.1 с.296-298 | 1670 | /cc/appeals/create-closed-appeals |
| 4.8.3 | События | [sections/215-sobytiya.md](sections/215-sobytiya.md) | 298 | ч.1 с.298 | 69 | — |
| 4.8.3.1 | Общение закрыто | [sections/216-obschenie-zakryto.md](sections/216-obschenie-zakryto.md) | 298-301 | ч.1 с.298-301 | 2844 | /events/md/onAppealClose |
| 4.9 | Управление задачами | [sections/217-upravlenie-zadachami.md](sections/217-upravlenie-zadachami.md) | 301 | ч.1 с.301 | 68 | — |
| 4.9.1 | Методы | [sections/218-metody.md](sections/218-metody.md) | 301 | ч.1 с.301 | 69 | — |
| 4.9.1.1 | Создание задачи | [sections/219-sozdanie-zadachi.md](sections/219-sozdanie-zadachi.md) | 301-302 | ч.1 с.301-302 | 1472 | POST /cc/task/add |
| 4.9.1.2 | Изменение задачи | [sections/220-izmenenie-zadachi.md](sections/220-izmenenie-zadachi.md) | 303-304 | ч.1 с.303-304 | 1566 | POST /cc/task/update |
| 4.9.1.3 | Получение задачи по ID | [sections/221-poluchenie-zadachi-po-id.md](sections/221-poluchenie-zadachi-po-id.md) | 304-306 | ч.1 с.304-306 | 1163 | POST /cc/task/get |
| 4.9.1.4 | Получение списка задач | [sections/222-poluchenie-spiska-zadach.md](sections/222-poluchenie-spiska-zadach.md) | 306-308 | ч.1 с.306-308 | 1859 | POST /cc/task/list |
| 4.9.1.5 | Завершение задачи | [sections/223-zavershenie-zadachi.md](sections/223-zavershenie-zadachi.md) | 308-309 | ч.1 с.308-309 | 402 | POST /cc/task/done |
| 4.9.1.6 | Отмена задачи | [sections/224-otmena-zadachi.md](sections/224-otmena-zadachi.md) | 309 | ч.1 с.309 | 378 | POST /cc/task/cancel |
| 4.9.2 | События | [sections/225-sobytiya.md](sections/225-sobytiya.md) | 310 | ч.1 с.310 | 69 | — |
| 4.9.2.1 | Задача создана | [sections/226-zadacha-sozdana.md](sections/226-zadacha-sozdana.md) | 310 | ч.1 с.310 | 772 | Событие, вызываемое при создании задачи. |
| 4.9.2.2 | Задача изменена | [sections/227-zadacha-izmenena.md](sections/227-zadacha-izmenena.md) | 310-311 | ч.1 с.310-311 | 761 | Событие, вызываемое при изменении задачи. |
| 4.10 | API Мобильное приложение | [sections/228-api-mobilnoe-prilozhenie.md](sections/228-api-mobilnoe-prilozhenie.md) | 311 | ч.1 с.311 | 70 | — |
| 4.10.1 | Общее | [sections/229-obschee.md](sections/229-obschee.md) | 311 | ч.1 с.311 | 242 | API предназначен для отправки текстовых сообщений, изображений, файлов. |
| 4.10.2 | Методы | [sections/230-metody.md](sections/230-metody.md) | 311 | ч.1 с.311 | 69 | — |
| 4.10.2.1 | Отправка сообщения, либо файла, либо оценки обслуживания | [sections/231-otpravka-soobscheniya-libo-fayla-libo-oc.md](sections/231-otpravka-soobscheniya-libo-fayla-libo-oc.md) | 311-313 | ч.1 с.311-313 | 2009 | POST /cc/send_message |
| 4.10.2.2 | Отправка уведомления о наборе текста | [sections/232-otpravka-uvedomleniya-o-nabore-teksta.md](sections/232-otpravka-uvedomleniya-o-nabore-teksta.md) | 314 | ч.1 с.314 | 477 | POST /cc/user_typing |
| 4.10.2.3 | Отправка уведомления о прочитанном сообщении | [sections/233-otpravka-uvedomleniya-o-prochitannom-soo.md](sections/233-otpravka-uvedomleniya-o-prochitannom-soo.md) | 314-315 | ч.1 с.314-315 | 513 | POST /cc/event_message_read |
| 4.10.2.4 | Отправка уведомления о доставленном сообщении | [sections/234-otpravka-uvedomleniya-o-dostavlennom-soo.md](sections/234-otpravka-uvedomleniya-o-dostavlennom-soo.md) | 315-316 | ч.1 с.315-316 | 522 | POST /cc/event_message_received |
| 4.10.2.5 | Получение истории сообщений | [sections/235-poluchenie-istorii-soobscheniy.md](sections/235-poluchenie-istorii-soobscheniy.md) | 316-318 | ч.1 с.316-318 | 1121 | POST /cc/get_chat_history |
| 4.10.3 | События | [sections/236-sobytiya.md](sections/236-sobytiya.md) | 318 | ч.1 с.318 | 111 | В данном разделе описаны события, отправляемые Контакт-центром MANGO OFFICE в |
| 4.10.3.1 | Общие параметры для каждого события | [sections/237-obschie-parametry-dlya-kazhdogo-sobytiya.md](sections/237-obschie-parametry-dlya-kazhdogo-sobytiya.md) | 318 | ч.1 с.318 | 234 | Перечень общих параметров события: |
| 4.10.3.2 | Отправка сообщения | [sections/238-otpravka-soobscheniya.md](sections/238-otpravka-soobscheniya.md) | 318-319 | ч.1 с.318-319 | 483 | В данном разделе описано событие "Отправка сообщения", отправляемое Контакт-центром |
| 4.10.3.3 | Оповещение о том, что пользователь набирает текст | [sections/239-opoveschenie-o-tom-chto-polzovatel-nabir.md](sections/239-opoveschenie-o-tom-chto-polzovatel-nabir.md) | 319 | ч.1 с.319 | 213 | В данном разделе описано событие "Оповещение о том, что пользователь что-то печатает", |
| 4.10.3.4 | Оповещение о том, что сообщение прочитано | [sections/240-opoveschenie-o-tom-chto-soobschenie-proc.md](sections/240-opoveschenie-o-tom-chto-soobschenie-proc.md) | 319 | ч.1 с.319 | 257 | В данном разделе описано событие "Оповещение о том, что сообщение прочитано", |
| 4.10.3.5 | Оповещение о том, что обращение закрыто и нужно оценить работу оператора | [sections/241-opoveschenie-o-tom-chto-obraschenie-zakr.md](sections/241-opoveschenie-o-tom-chto-obraschenie-zakr.md) | 319-320 | ч.1 с.319-320 | 598 | В данном разделе описано событие, отправляемое Контакт-центром MANGO OFFICE в ваше |
| 4.10.4 | Как найти channelId | [sections/242-kak-nayti-channelid.md](sections/242-kak-nayti-channelid.md) | 320-321 | ч.1 с.320-321 | 622 | Если вы хотите использовать методы для получения сообщений из внешних приложений в |
| — | Список кодов результатов | [sections/243-spisok-kodov-rezultatov.md](sections/243-spisok-kodov-rezultatov.md) | 322-327 | ч.1 с.322-327 | 7338 | Ниже приведен список кодов результатов выполнения команд или запросов, завершения |
| — | Примеры поведения | [sections/244-primery-povedeniya.md](sections/244-primery-povedeniya.md) | 328 | ч.1 с.328 | 61 | — |
| — | Уведомление о вызове | [sections/245-uvedomlenie-o-vyzove.md](sections/245-uvedomlenie-o-vyzove.md) | 328-329 | ч.1 с.328-329 | 508 | Сотрудник ВАТС с внутренним номером "1234" вызывает с номера "74955404444" внешнего |
| — | Инициирование исходящего вызова | [sections/246-iniciirovanie-ishodyaschego-vyzova.md](sections/246-iniciirovanie-ishodyaschego-vyzova.md) | 329-331 | ч.1 с.329-331 | 1194 | Вешняя система отправляет команду инициирования вызова сотрудником ВАТС с внутренним |
| — | Маршрутизация вызова | [sections/247-marshrutizaciya-vyzova.md](sections/247-marshrutizaciya-vyzova.md) | 331-333 | ч.1 с.331-333 | 1144 | Вызов поступает на номер DID 7800123456789, попадает в IVR. |
| — | Перевод вызова с консультацией | [sections/248-perevod-vyzova-s-konsultaciey.md](sections/248-perevod-vyzova-s-konsultaciey.md) | 334-337 | ч.1 с.334-337 | 1513 | Входящий вызов с номера "74955404444" на номер сотрудника ВАТС "12345678" с |
| — | Перевод вызова без консультации | [sections/249-perevod-vyzova-bez-konsultacii.md](sections/249-perevod-vyzova-bez-konsultacii.md) | 337-340 | ч.1 с.337-340 | 1303 | Входящий вызов с номера "74955404444" на номер сотрудника ВАТС "44332211" с |
| — | Обработка нажатий DTMF-клавиш | [sections/250-obrabotka-nazhatiy-dtmf-klavish.md](sections/250-obrabotka-nazhatiy-dtmf-klavish.md) | 340-343 | ч.1 с.340-343 | 1839 | Пример: |
| — | Приложение 1 – Описание поля sip-headers | [sections/251-prilozhenie-1-opisanie-polya-sip-headers.md](sections/251-prilozhenie-1-opisanie-polya-sip-headers.md) | 344 | ч.1 с.344 | 620 | Опциональный параметр, содержащий вложенные SIP заголовки и их значения. |
| — | История документа | [sections/252-istoriya-dokumenta.md](sections/252-istoriya-dokumenta.md) | 345-363 | ч.1 с.345-363 | 12966 | Обновление 02.06.2026 |
| | **ИТОГО** | | | | **258672** | весь документ |

## Источники

- Источник БЗ, часть 1: `kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf`
- Стандарт цитирования: [`standards/kb-standard.md`](../../../../standards/kb-standard.md), [ADR-007](../../../../docs/adr/007-kb-standard.md)
