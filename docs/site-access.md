---
status: draft
version: 0.1
updated: 2026-10-24
ai-generated: true
type: guide
scope: site-access
related_artifacts:
  - "site/gate.js"
  - "site/password-hashes.json"
  - "scripts/set-site-password.mjs"
related_issues:
  - 388
---

# Парольный вход на сайт

Документ для владельца репозитория: как устроен вход на
[сайт каталога](https://g-ivan-a.github.io/mango_ba_prompts/) и как сменить
системный пароль. Сам пароль здесь не публикуется: его выдаёт владелец
репозитория.

## 1. Как работает вход

- Уровень защиты — «чтобы совсем чужие не смотрели». Это не авторизация и не
  шифрование контента.
- Пароль один на весь сайт. Учётных записей нет.
- Скрипт
  [`site/gate.js`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/site/gate.js)
  подключён в `<head>` каждой HTML-страницы сайта: каталога, списка отчётов и
  страниц отчёта run-0060. Пока пароль не введён, страница скрыта, а каталог не
  загружает данные.
- Пароль сверяется с записью `"site"` в
  [`site/password-hashes.json`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/site/password-hashes.json):
  `SHA-256(salt + UPPERCASE(trim(пароль)))`. Регистр букв и пробелы по краям
  не важны.
- После входа браузер помнит доступ в `localStorage` (ключ
  `mango-site-access`). Кнопка «⏻» в верхнем меню каталога сбрасывает доступ.
- После смены пароля старый доступ перестаёт действовать: в браузере хранится
  хэш, а он меняется вместе с солью.

## 2. Как сменить пароль

1. Выбрать новый пароль. Не записывать его в issue, PR, коммит и документацию.
2. В корне репозитория выполнить одну из команд:

   ```bash
   SITE_PASSWORD='<новый пароль>' node scripts/set-site-password.mjs
   printf '%s' '<новый пароль>' | node scripts/set-site-password.mjs
   ```

   Скрипт
   [`scripts/set-site-password.mjs`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/scripts/set-site-password.mjs)
   генерирует новую соль и перезаписывает только запись `"site"`. Запись
   `"run-0060"` (отдельный пароль отчёта run-0060) не меняется.
3. Проверить локально:

   ```bash
   python3 -m http.server 8000 --directory site
   ```

   Открыть `http://localhost:8000/`, ввести новый пароль. Неверный пароль даёт
   сообщение «Неверный пароль».
4. Закоммитить `site/password-hashes.json` и влить PR в `main`. Workflow
   [`github-pages.yml`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/.github/workflows/github-pages.yml)
   опубликует сайт.
5. Передать новый пароль команде по закрытому каналу.

## 3. Ограничения

- Данные сайта (`site/data/*.json`) и исходники промптов на GitHub доступны по
  прямой ссылке без пароля. Пароль закрывает интерфейс сайта, а не файлы.
- Хэш с солью лежит в открытом репозитории. Короткий пароль подбирается
  перебором. Для уровня «чтобы совсем чужие не смотрели» это допустимо.
- Без JavaScript страница не откроется: проверка пароля идёт в браузере.
- Для настоящего ограничения доступа нужен приватный хостинг или
  авторизация на стороне сервера. Варианты —
  [`ai-governance/ai-governance.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/ai-governance/ai-governance.md#веб-ресурс-app-после-приватизации).
