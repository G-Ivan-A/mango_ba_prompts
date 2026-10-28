"""Rebuild selected public evidence; raw exports remain local and ignored."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

from extract import BASE, answer_text, messages

# Whole Founder turns preserve the evolution without inventing a shorter mandate.
FOUNDER = [89,109,119,141,443,549,647,649,743,751,765,767,779,827,829,
           861,871,873,937,941,943,947,949,951,955,965,967]
# Only methodological excerpts of the task chat: no customer brief or solution.
EXCERPTS = {
    4: [('**Часть 3. Конституция**', '**Источники и режим**'),
        ('- Прочитанные URL/вложения:', '**Часть 4.')],
    55: [(None, None)],
    56: [('Вы абсолютно правы.', 'Проверю документацию'),
         ('## Вопросы для уточнения у Заказчика', '\n---')],
    57: [(None, None)],
    58: [('P.S.', None)],
    70: [('Смена статусов', '\n3.')],
    71: [(None, None)],
    93: [(None, None)],
    95: [('теперь', 'Вот черновик')],
    96: [('Принято.', '---'), ('**1.1.', '**1.3.')],
    97: [(None, None)],
    99: [('(отклонение', 'Я указал в секундах, значит в текущей итерации  - в секундах!!!')],
    101: [('а теперь', 'черновик:')],
    103: [(None, None)],
    104: [('Нет, противоречий нет.', '\n\nЭти вопросы'),
          ('### 1. Проверка', '\n\n*'),
          ('*   **Массив', '*   **Разделение')],
    107: [(None, None)],
}


def excerpt(text, start, end):
    left = text.index(start) if start else 0
    right = text.index(end, left) if end else len(text)
    if end and end.endswith('!!!'):
        right += len(end)
    value = text[left:right].strip()
    if not value:
        raise ValueError('Empty excerpt')
    return value


def main():
    evidence = {'schema': 1, 'exports': {}, 'entries': []}
    for chat in ['split', '1131']:
        path = BASE / 'raw' / f'chat-export-{chat}.json'
        title, items = messages(path)
        evidence['exports'][chat] = {
            'url': 'https://github.com/user-attachments/files/' +
                   ('34074559/chat-export-.json' if chat == 'split' else '34074560/chat-export-1131.json'),
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'bytes': path.stat().st_size, 'title': title,
            'visible_messages': sum(visible for _, visible in items),
            'history_only_messages': sum(not visible for _, visible in items),
        }
        for n in FOUNDER if chat == 'split' else EXCERPTS:
            message, visible = items[n-1]
            content = answer_text(message)
            spans = ([content[:content.index('Вот пример промпта:')].strip()]
                     if chat == 'split' and n == 861 else
                     [content.strip()]) if chat == 'split' else [
                excerpt(content, a, b) for a, b in EXCERPTS[n]]
            evidence['entries'].append({
                'key': ('S' if chat == 'split' else 'X') + f'{n:03d}',
                'chat': chat, 'turn': n, 'message_id': message['id'],
                'role': message['role'], 'visible': visible,
                'utc': datetime.fromtimestamp(message['timestamp'], timezone.utc).isoformat(),
                'answer_sha256': hashlib.sha256(content.encode()).hexdigest(),
                'quotes': spans,
            })
    target = BASE / 'evidence.json'
    target.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + '\n')
    lines = ['# Issue 397 — проверяемые выдержки', '',
             'Отобраны требования и методологические эпизоды. Полные клиентские',
             'переписки не публикуются. Орфография оригинала сохранена. Номер —',
             'позиция в видимом `chat.messages` (с единицы), не номер сообщения модели.',
             'Assistant цитируется как наблюдаемое поведение, а не источник истины о продукте.', '',
             '## Экспорты и метод', '']
    for chat, source in evidence['exports'].items():
        lines += [f"- **{chat}**: [вложение]({source['url']}), SHA-256 `{source['sha256']}`;",
                  f"  {source['bytes']} байт; видимых {source['visible_messages']},",
                  f"  только в history {source['history_only_messages']}."]
    lines += ['', 'Извлечение: `extract.py` сначала отделяет видимую ветку от history-only,',
              'индексирует user/assistant и фильтрует СПЛИТ по темам с 2026-08-01.',
              'У assistant пустое `content` не значит пустой ответ: читаются только',
              '`content_list[].phase=answer`, без thinking summaries. History-only не',
              'склеивается с основной веткой; все цитаты ниже — из видимой ветки.',
              'Имена участников как формальное удостоверение авторства экспортом не',
              'подтверждаются: Founder — роль постановщика в СПЛИТ согласно issue.',
              'Точные ID, UTC и SHA-256 полного опубликованного ответа — в evidence.json.',
              'В Markdown удалены только концевые пробелы строк; JSON хранит точные выдержки.',
              'Байты вложений и вхождение каждой цитаты проверяет `verify.py`.', '']
    for row in evidence['entries']:
        lines += [f"## {row['key']}", '',
                  f"{row['chat']} · {row['role']} · {row['utc']} · turn {row['turn']}",
                  f"ID: `{row['message_id']}`. [Исходное вложение]({evidence['exports'][row['chat']]['url']}).", '']
        for quote in row['quotes']:
            lines += ['> ' + line.rstrip() if line.rstrip() else '>'
                      for line in quote.splitlines()] + ['']
    (BASE / 'evidence.md').write_text('\n'.join(lines))
    print(f"Curated {len(evidence['entries'])} entries")


if __name__ == '__main__':
    main()
