---
status: draft
updated: 2026-11-26
ai-generated: true
type: evidence
---

# Входы RUN-0096

| Вход | Что это | Где |
| --- | --- | --- |
| Issue #505 «Прогон задачи 1143 и корректировка промптов» | Задачи: RUN, проблемы для отладки, RFC с анализом избыточности, issue на исполнение; постусловие о бэклоге | https://github.com/G-Ivan-A/mango_ba_prompts/issues/505 |
| Чат 1143 | Копия страницы чата DeepSeek, текст без ролей, вложение issue; sha256 `ecfc81cfff4f50a9d4bdb0a9eaa314e8e9d30fbeeec69a1c010020e1768fb2ac` | https://github.com/user-attachments/files/35459115/1143.txt |
| Метрики чата | Маркеры шагов и счётчики сигналов по строкам | [`chat-1143-metrics.md`](chat-1143-metrics.md) |
| Черновики промптов | AIN-01…24, Ш-0, Ш-3…Ш-5 из `prompts/drafts/` на коммите `623573e4` — для замера избыточности (в чате их текста нет) | [`../logs/prompt-redundancy.json`](../logs/prompt-redundancy.json) |
| Постановка | Полная постановка исполнителя по шаблону задачи | [`task-statement-505.md`](task-statement-505.md) |

## Почему расшифровка чата не лежит в репозитории

Чат содержит пересказ ТЗ Заказчика и рабочие комментарии БА. Для отладки
промптов нужны не детали ТЗ, а реплики БА о работе модели и места, где
модель нарушила правило промпта. Поэтому, как в RUN-0095, в репозиторий идут
sha256, счётчики, номера строк и короткие цитаты в анализе. Вывод
`chat_signals.py` содержит только числа и номера строк.

## Как воспроизвести

```bash
mkdir -p /tmp/chat-1143 && cd /tmp/chat-1143   # отдельный пустой каталог
curl -L -o 1143.txt "https://github.com/user-attachments/files/35459115/1143.txt"
sha256sum 1143.txt   # ecfc81cf…b2ac
cd <корень репозитория>
python3 -I experiments/issue_505/chat_signals.py /tmp/chat-1143/1143.txt \
  | cmp - runs/2026/RUN-0096/logs/chat-signals.json
git checkout 623573e4 -- prompts/drafts   # срез черновиков, на котором делался замер
python3 -I experiments/issue_505/prompt_redundancy.py \
  | cmp - runs/2026/RUN-0096/logs/prompt-redundancy.json
git checkout HEAD -- prompts/drafts
```

Оба `cmp` молчат: вывод совпадает побайтно. Номера строк — по разбиению на
строки (`splitlines`), поэтому совпадают для CRLF-оригинала и LF-копии.
