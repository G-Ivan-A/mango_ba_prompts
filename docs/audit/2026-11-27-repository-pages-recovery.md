---
status: draft
version: 0.1
updated: 2026-11-27
temperature: 0.1
type: audit
related_issues: [512, 509]
---

# Аудит репозитория и восстановление GitHub Pages

## Постановка и критерии

Владелец и агенты потеряли доступ к веб-каталогу. PR #511 закрывает
первую часть BL-194, а правки по последующим решениям владельца остались
в закрытом PR #510. В режиме **Creative** проверяем оба PR, переносим
недостающие изменения и готовим восстановление сайта из проверяемого
пакета. Источники задачи — [#512](https://github.com/G-Ivan-A/mango_ba_prompts/issues/512),
[PR #510](https://github.com/G-Ivan-A/mango_ba_prompts/pull/510) и
[PR #511](https://github.com/G-Ivan-A/mango_ba_prompts/pull/511).

| Критерий | Доказательство |
| --- | --- |
| §§2.1–2.3 и 2.11 реализованы поверх #511 | Контракт A-IN 0.5, проверки обеих форм и сайта, тест маршрута и итогов. |
| Для 404 установлено состояние сайта, пакет готов к восстановлению | Ответ канонического URL, REST Pages, SHA последнего деплоя, сборка 2.9.6 и [инструкция](../site-access.md#восстановление-после-404-512). |
| За 25–27.11 описаны доступные события, настройки и пробелы доступа | Хронология и снимок ниже. Автор, момент и причина смены видимости требуют записи GitHub. |
| Репозиторий проверен | Полный набор валидаторов, сравнение регрессии с `main`, браузер, состояние серверных проверок. |

Ограничения приёмки — приватность исходного репозитория, явное решение
владельца о публикации и пакетный деплой по ADR-018. Штатные промпты,
архив 2.7.0 и история прогонов проверяются существующими регрессиями.

## Хронология

Время UTC. Проверены история Git, REST API, PR timeline, запуски Actions и
объекты деплоя. Для 25.11 лента событий не показала записей за день. Эта
лента не заменяет журнал безопасности.

| Дата и время | Подтверждённое событие |
| --- | --- |
| 23.11 16:23:08 | Последний найденный успешный [деплой Pages 8004433258](https://github.com/G-Ivan-A/mango_ba_prompts/deployments/github-pages) связывает канонический URL с веткой `gh-pages`, SHA `deed5000e9c7854d72d8e11a0a4f82d1aad29659`, версия 2.9.3. Ветка по-прежнему указывает на этот SHA. |
| 26.11 15:10:24 | REST `GET /repos/…` показывает это значение в `updated_at`. Поле общее, из него нельзя вывести название изменённой настройки. |
| 26.11 21:14:54 | REST events содержит `MemberEvent/added` для текущего collaborator. Сейчас REST показывает роль `write`. Эта запись не показывает операцию снятия доступа или смены видимости. |
| 26.11 21:44 | Три ручных запуска для SHA `372bdee9…` приняты API. На 27.11 у них `queued`, `jobs: []`. При запросе логов GitHub возвращает `run … is still in progress`. [Governance](https://github.com/G-Ivan-A/mango_ba_prompts/actions/runs/45900185953), [Pages](https://github.com/G-Ivan-A/mango_ba_prompts/actions/runs/45900231627), [KB](https://github.com/G-Ivan-A/mango_ba_prompts/actions/runs/45900234755). |
| 27.11 06:50:13 | PR #511 слит в `main` (`70cf31c8`). |
| 27.11 07:16:17 | Timeline #510 одновременно показывает `closed` и `head_ref_force_pushed` к `b7bd94c7`. PR не слит. Известная попытка переоткрыть вернула 422. Репозиторий head сейчас отдельный, `fork: false`, без `parent`. [История #510](https://github.com/G-Ivan-A/mango_ba_prompts/pull/510#issuecomment-7212616980) |
| 27.11 | Канонический URL отвечает 404 с шаблоном GitHub Pages «Site not found». REST репозитория сообщает `private: true`, `has_pages: false`, REST Pages и Pages builds отвечают 404. |

Владелец сообщил об уведомлении GitHub, повторном добавлении collaborator
и ответе интерфейса «This repository is currently private». По этим данным
можно установить текущую видимость. Исторического значения перед
`updated_at`, текста уведомления и записи о самой смене видимости в
доступных источниках нет. GitHub документирует, что при public → private
публичные форки отсоединяются, а сайт Pages на GitHub Free снимается с
публикации автоматически. Это объяснение согласуется с текущими признаками.
Точную причину закрытия #510 и смены видимости определяет только журнал
событий GitHub. [Правила смены видимости](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/managing-repository-settings/setting-repository-visibility)

## Срез доступных настроек

| Область | Проверка и предел наблюдения |
| --- | --- |
| Репозиторий | Владелец — личная учётная запись. Visibility `private`, default `main`, репозиторий активен и не архивирован. Текущий доступ исполнителя `WRITE`, `admin: false`. |
| Ветки и правила | `main` и `gh-pages` существуют, REST показывает `protected: false`. REST защиты `main` — 404. REST rulesets и правил ветки — 403 с предложением GitHub Pro или публичного репозитория. Сообщение говорит о недоступности функции через этот API; точный тариф видит владелец в Billing. |
| Pull requests и функции | Auto-merge и три варианта merge включены. Автоудаление head и обязательная подпись web commit выключены. Issues и Projects включены; Wiki, Discussions и Downloads выключены. REST возвращает `allow_forking: true`. |
| Pages | `has_pages: false`; объект активного сайта и источник не читаются. Отображаемое окружение `github-pages` разрешает ветку `gh-pages`. Окружение и ветка сохранились после последнего деплоя. |
| Actions | Три workflow и служебный `pages-build-deployment` отображаются как `active`. Последние завершённые runs основного репозитория в Actions API — 22.08.2026. Проверки отсутствуют также на #504 и #511. REST настроек Actions, политик, разрешённых действий и раннеров — 404 для текущих прав. |
| Доступ и журнал | Сотрудничество сейчас `write`; admin API приглашений, webhook, deploy keys и code security недоступны. Личный security log и Billing относятся к учётной записи владельца, REST org audit для `G-Ivan-A` вернул 404. |

## Восстановление и приёмка

Активная сессия GitHub позволяет открывать приватные исходники при наличии
прав. Для веб-сайта нужен работающий Pages deployment. GitHub Pro
разрешает Pages из личного приватного репозитория с публичным сайтом.
Закрытые Pages доступны для проектных сайтов организаций на Enterprise
Cloud с другим URL. Клиентская форма пароля не ограничивает скачивание
статики. [Планы Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)
[Закрытые сайты](https://docs.github.com/en/pages/getting-started-with-github-pages/about-privately-published-github-pages-sites)

Исходный CI делал force-push в `gh-pages` с `GITHUB_TOKEN`. GitHub
указывает, что такой push не запускает сборку Pages. Workflow теперь
готовит `pages-dist` из проверенного SHA и на `main` сообщает о
недоступном или неверном источнике Pages. PR и ручная сборка его ветки
выполняются независимо от этой проверки. Публикация пакета через
`gh-pages` остаётся явным шагом BL-232.
[Источники публикации и ограничение токена](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)

Владельцу следует выгрузить свой **Settings → Security log** за 25–27.11
с фильтром репозитория и сверить события изменения видимости и доступа,
время и исполнителя. Сопоставьте с доступным исходным уведомлением GitHub.
Если нужного события в журнале нет, передайте GitHub Support временное
окно, ссылки #510/#511 и идентификатор репозитория `1245388148`.
[Security log личной учётной записи](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/reviewing-your-security-log)

Для CI владелец проверяет **Settings → Actions → General**, разрешённые
actions и доступность GitHub-hosted runners, затем **Billing & licensing**
с квотой, бюджетом и статусом платежей. Наличие `queued` без jobs не
различает эти причины. После восстановления запустите проверки
проверяемого SHA, а для Pages выполните [порядок восстановления](../site-access.md#восстановление-после-404-512).
[Учёт использования Actions](https://docs.github.com/en/billing/concepts/product-billing/github-actions)

**Движение по бэклогу.** BL-193, BL-191 и BL-192 — `DONE` по принятым PR
#507, #494 и runtime #26/#29. BL-194 — `review` в #513. Q1 и BL-232
остаются открытыми до восстановления канала, публикации и приёмки.
После BL-232 предусмотрен прогон БА на двух моделях по RFC §9.
[Сводный бэклог](../../pr-ops/BACKLOG.md#движение-по-цепочке-509-bl-194)
