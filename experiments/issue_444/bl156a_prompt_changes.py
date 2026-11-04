"""Обратимая правка BL-156а (issue #444) в 14 промптах v0.1 потока BCREQ.

BL-156а применяет к `prompts/bcreq-*.md` одну правку: закрепляет ссылки на
runtime, `blob/main/` → `blob/<SHA реестра>/` (ТС-1, раздел 7 реестра
справочников 0.4). Поведение промпта она не меняет: правило RUN-0080
относит ссылки к правкам без поведения.

Типизация гейтов (15 подстановок `experiments/issue_438/prompt-typing.json`)
в `prompts/` не применена: RUN-0081 измерил A с ней, ядро 9/11 против 10/11
RUN-0079 (DEC-427-11). Подстановка перенесена в BL-156б;
`apply_typing()` восстанавливает измеренный текст для проверок RUN-0080 и
RUN-0081.

Регрессии сохранности промптов (#391, #393, #395) не переписывают свои
эталоны: они вызывают `revert()` и сверяют оставшиеся байты с эталоном.
Так доказано, что, кроме закрепления ссылок, в промптах ничего не менялось.

Issue #448 (RUN-0084): Ш-В опубликован как v0.2 — подстановка типа гейта
Ш-В и правило «правка без добавлений». `revert()` сначала откатывает эту
публикацию (`experiments/issue_448/shv_v02_changes.py`), затем закрепление
ссылок. `apply_typing()` для Ш-В работает только с текстом v0.1 (A0).
"""
from pathlib import Path
import importlib.util
import json

ROOT = Path(__file__).resolve().parents[2]
_V02_SPEC = importlib.util.spec_from_file_location("shv_v02_changes", ROOT / "experiments/issue_448/shv_v02_changes.py")
SHV_V02 = importlib.util.module_from_spec(_V02_SPEC)
_V02_SPEC.loader.exec_module(SHV_V02)
TYPING = ROOT / "experiments/issue_438/prompt-typing.json"
RUNTIME_SHA = "f31dcde33f0bc120244128faab98fc0162e45701"
RUNTIME_MAIN = "github.com/G-Ivan-A/mango-ba-ai-runtime/blob/main/"
RUNTIME_PINNED = RUNTIME_MAIN.replace("/main/", f"/{RUNTIME_SHA}/")


def substitutions(path=None):
    items = json.loads(TYPING.read_text(encoding="utf-8"))["substitutions"]
    return [s for s in items if path is None or s["path"] == path]


def edited(path):
    """True для 14 промптов v0.1, которые правит BL-156а."""
    return any(s["path"] == path for s in substitutions())


def revert(path, text):
    """Вернуть текст промпта `path` (repo-relative) к виду до BL-156а.

    В промпте v0.1 закреплённая ссылка обязана встретиться хотя бы раз, а
    ссылки на main не должно остаться, иначе AssertionError: правка потеряна
    или неполна. Остальные промпты BL-156а не трогает: их текст возвращается
    как есть, закреплённой ссылки в нём быть не должно.
    """
    text = SHV_V02.revert(path, text)
    if not edited(path):
        assert RUNTIME_PINNED not in text, path
        return text
    assert RUNTIME_PINNED in text and RUNTIME_MAIN not in text, path
    return text.replace(RUNTIME_PINNED, RUNTIME_MAIN)


def revert_bytes(path, data):
    return revert(path, data.decode("utf-8")).encode("utf-8")


def apply_typing(path, text):
    """Текст с подстановками типа гейта, как его измерили RUN-0080 и RUN-0081.

    `path` — промпт v0.1, по которому выбираются подстановки. Каждая
    строка `before` должна встретиться ровно один раз.
    """
    subs = substitutions(path)
    assert subs, path
    for s in subs:
        assert text.count(s["before"]) == 1, (path, s["line"], text.count(s["before"]))
        text = text.replace(s["before"], s["after"])
    return text
