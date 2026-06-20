---
type: kb-source-index
doc_code: MDIALOGIAPI
doc_title: "Манго Диалоги. Справочник по API"
doc_version: "27.02.2026"
status: extracted
ai-generated: true
---

# Манго Диалоги. Справочник по API — индекс БЗ (карта разделов)

> Источник: `kb/sources/mdialogi-api/Manual_API_Mango_Dialogi.pdf` · извлечено: pdfplumber 0.11.10 ·
> токены: tiktoken:cl100k_base. Это **карта поиска** для агента (замена
> retrieval-шага до RAG, ADR-007 R2): найди раздел по колонке «Когда
> обращаться», открой только его файл, процитируй стабильным адресом.

## Как цитировать

`[MDIALOGIAPI, §<номер>, с.<страница>]` — формат проекта (issue #109);
плюс адрес чанка `kb/processed/<doc>/sections/<file>#<якорь>` (ADR-007 R3).

## Разделы

| № PDF | Раздел | Файл | Стр. | Источник | Токены | Когда обращаться |
| --- | --- | --- | --- | --- | ---: | --- |
| — | Титульная часть | [sections/00-titulnaya-chast.md](sections/00-titulnaya-chast.md) | 1-6 | ч.1 с.1-6 | 2495 | Манго Диалоги |
| 1 | О Манго Диалогах | [sections/01-o-mango-dialogah.md](sections/01-o-mango-dialogah.md) | 6 | ч.1 с.6 | 65 | — |
| 1.1 | Общее | [sections/02-obschee.md](sections/02-obschee.md) | 6 | ч.1 с.6 | 259 | Система "Манго Диалоги" (далее по тексту - МД) предоставляет сервис |
| 1.2 | Поддерживаемые каналы коммуникации | [sections/03-podderzhivaemye-kanaly-kommunikacii.md](sections/03-podderzhivaemye-kanaly-kommunikacii.md) | 6-7 | ч.1 с.6-7 | 1155 | Каналы коммуникации различаются по средству, которое использует Клиент |
| 1.3 | Принцип текстовых коммуникаций с Клиентом при помощи Манго Диалогов | [sections/04-princip-tekstovyh-kommunikaciy-s-kliento.md](sections/04-princip-tekstovyh-kommunikaciy-s-kliento.md) | 7-8 | ч.1 с.7-8 | 852 | Манго Диалогов |
| 1.4 | Основные сущности | [sections/05-osnovnye-suschnosti.md](sections/05-osnovnye-suschnosti.md) | 8-10 | ч.1 с.8-10 | 1219 | В этом параграфе рассказывается об основных сущностях МД и их |
| 2 | Начало работы с API | [sections/06-nachalo-raboty-s-api.md](sections/06-nachalo-raboty-s-api.md) | 10 | ч.1 с.10 | 62 | — |
| 2.1 | Введение в API | [sections/07-vvedenie-v-api.md](sections/07-vvedenie-v-api.md) | 10 | ч.1 с.10 | 186 | Используя API Манго Диалоги (далее по тексту - API), вы можете связать МД и |
| 2.2 | Несколько шагов и можно приступать к работе | [sections/08-neskolko-shagov-i-mozhno-pristupat-k-rab.md](sections/08-neskolko-shagov-i-mozhno-pristupat-k-rab.md) | 10 | ч.1 с.10 | 301 | 1) Прочитайте общие положения о взаимодействии систем. |
| 2.3 | Общие положения о взаимодействии систем | [sections/09-obschie-polozheniya-o-vzaimodeystvii-sis.md](sections/09-obschie-polozheniya-o-vzaimodeystvii-sis.md) | 10 | ч.1 с.10 | 301 | В этом разделе рассказывается о модели взаимодействия вашей внешней |
| 2.3.1 | Модель авторизации | [sections/10-model-avtorizacii.md](sections/10-model-avtorizacii.md) | 10-11 | ч.1 с.10-11 | 467 | API предоставляет внешней системе доступ к своим функциям без |
| 2.3.2 | Модель взаимодействия | [sections/11-model-vzaimodeystviya.md](sections/11-model-vzaimodeystviya.md) | 11-12 | ч.1 с.11-12 | 782 | Внешняя система и API взаимодействуют по протоколу HTTPS. |
| 2.3.3 | Виды запросов | [sections/12-vidy-zaprosov.md](sections/12-vidy-zaprosov.md) | 12-13 | ч.1 с.12-13 | 354 | Запросы между системами условимся разделять на асинхронные и |
| 2.3.4 | Ограничения | [sections/13-ogranicheniya.md](sections/13-ogranicheniya.md) | 13 | ч.1 с.13 | 175 | 1) Не поддерживается протокол TLS версий 1.0, 1.1, 1.3. |
| 2.3.5 | Лимиты количества запросов к API | [sections/14-limity-kolichestva-zaprosov-k-api.md](sections/14-limity-kolichestva-zaprosov-k-api.md) | 13-14 | ч.1 с.13-14 | 601 | В API существуют ограничения на максимальное число запросов в секунду. |
| 2.3.6 | Разрешенные IP-адреса | [sections/15-razreshennye-ip-adresa.md](sections/15-razreshennye-ip-adresa.md) | 14 | ч.1 с.14 | 269 | При подключении API коннектора в настройках Личного кабинета MANGO |
| 2.3.7 | Об электронной подписи запросов | [sections/16-ob-elektronnoy-podpisi-zaprosov.md](sections/16-ob-elektronnoy-podpisi-zaprosov.md) | 14 | ч.1 с.14 | 75 | — |
| 2.3.7 | Общее | [sections/17-obschee.md](sections/17-obschee.md) | 14-15 | ч.1 с.14-15 | 220 | Данные, которыми обмениваются системы, как правило, будут передаваться в |
| 2.3.7 | Поле json | [sections/18-pole-json.md](sections/18-pole-json.md) | 15 | ч.1 с.15 | 286 | Это поле можно рассматривать как ассоциативный массив любой вложенности |
| 2.3.7 | Уникальный код вашей ВАТС (vpbx_api_key) | [sections/19-unikalnyy-kod-vashey-vats-vpbx-api-key.md](sections/19-unikalnyy-kod-vashey-vats-vpbx-api-key.md) | 15 | ч.1 с.15 | 155 | Представляет собой строку вида: |
| 2.3.7 | Ключ создания подписи (vpbx_api_salt) | [sections/20-klyuch-sozdaniya-podpisi-vpbx-api-salt.md](sections/20-klyuch-sozdaniya-podpisi-vpbx-api-salt.md) | 15-16 | ч.1 с.15-16 | 218 | Для подписания запроса к API используется ключ создания подписи или |
| 2.3.7 | Электронная подпись (sign) | [sections/21-elektronnaya-podpis-sign.md](sections/21-elektronnaya-podpis-sign.md) | 16 | ч.1 с.16 | 226 | Значение sign рассчитывается следующим образом: |
| 2.3.7 | Как узнать свой уникальный код ВАТС (vpbx_api_key) и ключ создания подписи (vpbx_api_salt)? | [sections/22-kak-uznat-svoy-unikalnyy-kod-vats-vpbx-a.md](sections/22-kak-uznat-svoy-unikalnyy-kod-vats-vpbx-a.md) | 16-17 | ч.1 с.16-17 | 336 | подписи (vpbx_api_salt)? |
| 3 | Руководство по API | [sections/23-rukovodstvo-po-api.md](sections/23-rukovodstvo-po-api.md) | 17 | ч.1 с.17 | 63 | — |
| 3.1 | Обмен сообщениями в WhatsApp | [sections/24-obmen-soobscheniyami-v-whatsapp.md](sections/24-obmen-soobscheniyami-v-whatsapp.md) | 17 | ч.1 с.17 | 66 | — |
| 3.1.1 | Общее | [sections/25-obschee.md](sections/25-obschee.md) | 17 | ч.1 с.17 | 352 | Если к Вашей Виртуальной АТС подключена услуга "WhatsApp Business API |
| 3.1.2 | Доступ к методам | [sections/26-dostup-k-metodam.md](sections/26-dostup-k-metodam.md) | 17-18 | ч.1 с.17-18 | 328 | Вы можете использовать методы, описанные в данном разделе, если |
| 3.1.3 | Получение списка HSM-шаблонов | [sections/27-poluchenie-spiska-hsm-shablonov.md](sections/27-poluchenie-spiska-hsm-shablonov.md) | 18-21 | ч.1 с.18-21 | 1628 | Метод позволяет получить список HSM-шаблонов, имеющих статус "APPROVED" |
| 3.1.4 | Отправление HSM | [sections/28-otpravlenie-hsm.md](sections/28-otpravlenie-hsm.md) | 21-23 | ч.1 с.21-23 | 1373 | Метод позволяет отправить Клиенту сообщение в соответствии с тем или иным |
| 3.1.5 | Получение статусов отправленных HSM-сообщений | [sections/29-poluchenie-statusov-otpravlennyh-hsm-soo.md](sections/29-poluchenie-statusov-otpravlennyh-hsm-soo.md) | 23-25 | ч.1 с.23-25 | 768 | Метод позволяет получить статус ранее отправленного HSM-сообщения. |
| 3.2 | Отправление каскада сообщений через WhatsApp и SMS | [sections/30-otpravlenie-kaskada-soobscheniy-cherez-w.md](sections/30-otpravlenie-kaskada-soobscheniy-cherez-w.md) | 25 | ч.1 с.25 | 82 | POST /cc/send_text_message |
| 3.2.1 | Основные сведения | [sections/31-osnovnye-svedeniya.md](sections/31-osnovnye-svedeniya.md) | 25 | ч.1 с.25 | 144 | Метод позволяет выполнять массовую рассылку текстовых сообщений |
| 3.2.2 | Правила работы | [sections/32-pravila-raboty.md](sections/32-pravila-raboty.md) | 25-26 | ч.1 с.25-26 | 959 | Чтобы выполнить массовую рассылку, необходимо комплексно применять |
| 3.2.3 | Ограничения | [sections/33-ogranicheniya.md](sections/33-ogranicheniya.md) | 26-27 | ч.1 с.26-27 | 366 | 1) Текст сообщения (параметр "text") должен быть заключен в кавычки и |
| 3.2.4 | Описание запроса | [sections/34-opisanie-zaprosa.md](sections/34-opisanie-zaprosa.md) | 27-29 | ч.1 с.27-29 | 1238 | Параметры запроса: |
| 3.3 | API работы с виджетами | [sections/35-api-raboty-s-vidzhetami.md](sections/35-api-raboty-s-vidzhetami.md) | 29 | ч.1 с.29 | 66 | — |
| 3.3.1 | Получить список виджетов | [sections/36-poluchit-spisok-vidzhetov.md](sections/36-poluchit-spisok-vidzhetov.md) | 29-33 | ч.1 с.29-33 | 2265 | Метод возвращает список виджетов МД, с подробной информацией о каждом |
| 3.3.2 | Получить список активных сессий | [sections/37-poluchit-spisok-aktivnyh-sessiy.md](sections/37-poluchit-spisok-aktivnyh-sessiy.md) | 33-38 | ч.1 с.33-38 | 3121 | Метод возвращает список сессий, находящихся в статуе "pending" (ожидает |
| 3.4 | API управления сессиями | [sections/38-api-upravleniya-sessiyami.md](sections/38-api-upravleniya-sessiyami.md) | 38 | ч.1 с.38 | 67 | — |
| 3.4.1 | Создать новую сессию | [sections/39-sozdat-novuyu-sessiyu.md](sections/39-sozdat-novuyu-sessiyu.md) | 38-40 | ч.1 с.38-40 | 1148 | Если Клиент ранее уже обращался в вашу компанию и у вас есть уникальный |
| 3.4.2 | Взять сессию в работу | [sections/40-vzyat-sessiyu-v-rabotu.md](sections/40-vzyat-sessiyu-v-rabotu.md) | 40-42 | ч.1 с.40-42 | 839 | Метод позволяет перевести сессию из статуса "pending" в статус "dialog", то есть |
| 3.4.3 | Перевод сессии на другого сотрудника или группу | [sections/41-perevod-sessii-na-drugogo-sotrudnika-ili.md](sections/41-perevod-sessii-na-drugogo-sotrudnika-ili.md) | 42-44 | ч.1 с.42-44 | 1543 | Этот метод позволяет передать диалог с Клиентом от одного оператора к |
| 3.4.4 | Закрыть сессию | [sections/42-zakryt-sessiyu.md](sections/42-zakryt-sessiyu.md) | 44-45 | ч.1 с.44-45 | 686 | Метод позволяет принудительно закрыть сессию в статусе "dialog". |
| 3.4.5 | Отправить сообщение оператора к Клиенту | [sections/43-otpravit-soobschenie-operatora-k-klientu.md](sections/43-otpravit-soobschenie-operatora-k-klientu.md) | 45-48 | ч.1 с.45-48 | 1570 | Метод позволяет отправить Клиенту сообщение от имени оператора. |
| 3.4.6 | Загрузка истории чата | [sections/44-zagruzka-istorii-chata.md](sections/44-zagruzka-istorii-chata.md) | 48-53 | ч.1 с.48-53 | 2618 | Метод возвращает массив сообщений, которыми обменивались Клиент и |
| 3.5 | API Realtime (вебхуки) | [sections/45-api-realtime-vebhuki.md](sections/45-api-realtime-vebhuki.md) | 53 | ч.1 с.53 | 68 | — |
| 3.5.1 | Сессия в состоянии ожидания | [sections/46-sessiya-v-sostoyanii-ozhidaniya.md](sections/46-sessiya-v-sostoyanii-ozhidaniya.md) | 53-57 | ч.1 с.53-57 | 2845 | Данный вебхук отправляется во внешнюю систему после того, как в МД будет |
| 3.5.2 | Сессия взята в работу | [sections/47-sessiya-vzyata-v-rabotu.md](sections/47-sessiya-vzyata-v-rabotu.md) | 57-62 | ч.1 с.57-62 | 2782 | Данный вебхук отправляется во внешнюю систему после того, как сессия будет |
| 3.5.3 | Сессия закрыта | [sections/48-sessiya-zakryta.md](sections/48-sessiya-zakryta.md) | 62-67 | ч.1 с.62-67 | 2860 | Данный вебхук отправляется во внешнюю систему после того, как сессия будет |
| 3.5.4 | HSM-сообщение оператора прочитано клиентом | [sections/49-hsm-soobschenie-operatora-prochitano-kli.md](sections/49-hsm-soobschenie-operatora-prochitano-kli.md) | 67-68 | ч.1 с.67-68 | 566 | В МД существует возможность отправлять Клиентам HSM-сообщения через |
| 3.5.5 | Сообщение оператора не доставлено клиенту | [sections/50-soobschenie-operatora-ne-dostavleno-klie.md](sections/50-soobschenie-operatora-ne-dostavleno-klie.md) | 68-69 | ч.1 с.68-69 | 478 | Данный вебхук отправляется во внешнюю систему в том случае, если |
| 3.5.6 | Сообщение оператора доставлено клиенту | [sections/51-soobschenie-operatora-dostavleno-klientu.md](sections/51-soobschenie-operatora-dostavleno-klientu.md) | 69-70 | ч.1 с.69-70 | 526 | Данный вебхук отправляется во внешнюю систему в том случае, если |
| 3.5.7 | Сообщение оператора прочитано клиентом | [sections/52-soobschenie-operatora-prochitano-kliento.md](sections/52-soobschenie-operatora-prochitano-kliento.md) | 70-71 | ч.1 с.70-71 | 534 | Данный вебхук отправляется во внешнюю систему в том случае, если |
| 3.5.8 | Новое сообщение в чате | [sections/53-novoe-soobschenie-v-chate.md](sections/53-novoe-soobschenie-v-chate.md) | 71-74 | ч.1 с.71-74 | 1504 | Данный вебхук отправляется во внешнюю систему, когда Клиент либо |
| 4 | Коды ошибок | [sections/54-kody-oshibok.md](sections/54-kody-oshibok.md) | 74 | ч.1 с.74 | 60 | — |
| 4.1 | Важная информация | [sections/55-vazhnaya-informaciya.md](sections/55-vazhnaya-informaciya.md) | 74 | ч.1 с.74 | 380 | 1) Если ваш запрос к API неверный, то вы получите ошибку в коде 3ХХХ. |
| 4.2 | Возможные коды ошибок API | [sections/56-vozmozhnye-kody-oshibok-api.md](sections/56-vozmozhnye-kody-oshibok-api.md) | 74-76 | ч.1 с.74-76 | 651 | Манго Диалоги. |
| 5 | Примеры использования API | [sections/57-primery-ispolzovaniya-api.md](sections/57-primery-ispolzovaniya-api.md) | 76 | ч.1 с.76 | 61 | — |
| 5.1 | Прием и обработка обращений Клиента | [sections/58-priem-i-obrabotka-obrascheniy-klienta.md](sections/58-priem-i-obrabotka-obrascheniy-klienta.md) | 76-83 | ч.1 с.76-83 | 2604 | После настройки каналов коммуникации в МД, вы сможете получать |
| 5.2 | Оператор обращается к Клиенту | [sections/59-operator-obraschaetsya-k-klientu.md](sections/59-operator-obraschaetsya-k-klientu.md) | 83-88 | ч.1 с.83-88 | 1902 | Если Клиент ранее уже обращался в вашу компанию по тому или иному |
| 5.3 | Перевод обращения на другого оператора | [sections/60-perevod-obrascheniya-na-drugogo-operator.md](sections/60-perevod-obrascheniya-na-drugogo-operator.md) | 88-91 | ч.1 с.88-91 | 723 | В этом параграфе рассказывается о том, как перевести обработку обращения с |
| — | История документа | [sections/61-istoriya-dokumenta.md](sections/61-istoriya-dokumenta.md) | 91 | ч.1 с.91 | 404 | 27.02.2026 |
| | **ИТОГО** | | | | **51297** | весь документ |

## Источники

- Источник БЗ, часть 1: `kb/sources/mdialogi-api/Manual_API_Mango_Dialogi.pdf`
- Стандарт цитирования: [`standards/kb-standard.md`](../../../standards/kb-standard.md), [ADR-007](../../../docs/adr/007-kb-standard.md)
