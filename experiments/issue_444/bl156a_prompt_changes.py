"""Обратимые правки BL-156а (issue #444) в 14 промптах v0.1 потока BCREQ.

BL-156а применяет к `prompts/bcreq-*.md` ровно две правки:

1. типизацию гейтов — 15 подстановок `before` → `after` из
   `experiments/issue_438/prompt-typing.json` (словарь потока, раздел 3.3);
2. закрепление ссылок на runtime: `blob/main/` → `blob/<SHA реестра>/`
   (ТС-1, раздел 7 реестра справочников 0.4).

Регрессии сохранности промптов (#391, #393, #395) не переписывают свои
эталоны: они вызывают `revert()` и сверяют оставшиеся байты с эталоном.
Так доказано, что, кроме этих двух правок, в промптах ничего не менялось.
"""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]
TYPING = ROOT / "experiments/issue_438/prompt-typing.json"
RUNTIME_SHA = "f31dcde33f0bc120244128faab98fc0162e45701"
RUNTIME_MAIN = "github.com/G-Ivan-A/mango-ba-ai-runtime/blob/main/"
RUNTIME_PINNED = RUNTIME_MAIN.replace("/main/", f"/{RUNTIME_SHA}/")


def substitutions(path=None):
    items = json.loads(TYPING.read_text(encoding="utf-8"))["substitutions"]
    return [s for s in items if path is None or s["path"] == path]


def revert(path, text):
    """Вернуть текст промпта `path` (repo-relative) к виду до BL-156а.

    Каждая подстановка обязана встретиться ровно один раз, иначе
    AssertionError: правка потеряна или задублирована.
    """
    for s in substitutions(path):
        assert text.count(s["after"]) == 1, (path, s["line"], text.count(s["after"]))
        text = text.replace(s["after"], s["before"])
    return text.replace(RUNTIME_PINNED, RUNTIME_MAIN)


def revert_bytes(path, data):
    return revert(path, data.decode("utf-8")).encode("utf-8")
