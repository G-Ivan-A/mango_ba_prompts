#!/usr/bin/env python3
"""Проекция текста репозитория в исполнимый текст промпта (issue #495).

Стандарт ``standards/bcreq-prompt-purity.md``: промпт исполняет модель без
доступа к приватному репозиторию, поэтому в исполнимом тексте нет

* ссылок на приватный репозиторий и относительных ссылок на его файлы —
  ``delink`` оставляет подпись ссылки как имя артефакта;
* служебных HTML-комментариев — ``strip_comments`` удаляет их строки.

Ссылки на runtime (``mango-ba-ai-runtime``), внешние источники и якоря
внутри промпта сохраняются: их читают при исполнении.

Модуль используют сборщики промптов (правила стандартов попадают в промпт
без ссылок на репозиторий) и разовая чистка исходников
``experiments/issue_495/clean_sources.py``. LLM не вызывается.
"""
import re

PRIVATE = "github.com/G-Ivan-A/mango_ba_prompts"
LINK = re.compile(r"\[((?:[^\[\]]|\[[^\]]*\])*)\]\(([^)\s]+)\)")
COMMENT_LINE = re.compile(r"(?m)^[ \t]*<!--(?:(?!-->).)*-->[ \t]*\n", re.S)
COMMENT = re.compile(r"<!--.*?-->", re.S)
#: Комментарий отдельным абзацем (пустая строка до и после) уходит вместе с одной
#: пустой строкой, чтобы не оставлять двойной пропуск.
COMMENT_PARA = re.compile(r"(?<=\n\n)[ \t]*<!--(?:(?!-->).)*-->[ \t]*\n\n", re.S)


def is_executable_target(target):
    """Ссылка, которую исполнитель промпта может открыть."""
    if PRIVATE in target:
        return False
    return target.startswith(("http://", "https://", "#", "mailto:"))


def delink(text):
    """``[подпись](приватный или относительный путь)`` → ``подпись``.

    Подпись-код (`` `path` ``) остаётся кодом: это имя артефакта, а не ссылка.
    Голый URL приватного репозитория без подписи удаляется вместе с
    обрамляющими скобками.
    """
    def repl(match):
        label, target = match.group(1), match.group(2)
        return match.group(0) if is_executable_target(target) else label

    text = LINK.sub(repl, text)
    text = re.sub(r"\s*\(?<?https?://" + re.escape(PRIVATE) + r"[^\s)>]*>?\)?", "", text)
    return text


def strip_comments(text):
    """Удалить служебные HTML-комментарии: целые строки — вместе с переводом строки."""
    text = COMMENT_PARA.sub("", text)
    text = COMMENT_LINE.sub("", text)
    return COMMENT.sub("", text)


def project(text):
    """Исполнимая проекция: без приватных/относительных ссылок и HTML-комментариев.

    Хвост из переводов строк сохраняется как во входе: удалённый комментарий в
    конце файла не оставляет пустую строку.
    """
    out = strip_comments(delink(text))
    if not out.strip():
        return out
    trail = len(text) - len(text.rstrip("\n"))
    return out.rstrip("\n") + "\n" * trail


def protected_counts(text, patterns, exempt=()):
    """Число защищённых маркеров (стандарт чистоты, раздел 4) по видам.

    ``exempt`` — ID правил, которые не считаются (исключённые правила базового
    стандарта, названные в манифесте черновиков).
    """
    out = {}
    for kind, regex in patterns.items():
        found = re.findall(regex, text)
        out[kind] = len([m for m in found if m not in exempt]) if kind == "rule_id" else len(found)
    return out
