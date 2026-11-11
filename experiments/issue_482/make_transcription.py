#!/usr/bin/env python3
"""Транскрипция колонок 1–2 ТЗ BCREQ-1140 (issue #482) -> source_transcription.json.

Исходник — «ТЗ газификация ХХХ области.pdf» (Word 2013 -> PDF, текстовый слой, 33 страницы,
SHA-256 7dd330a8…). В PDF сохранён режим рецензирования Word: удалённый текст напечатан
цветом правки и перечёркнут, вставленный — подчёркнут / выделен. Скрипт работает по
символам текстового слоя pymupdf и по векторным линиям правки:

- символ **удалён**, если через его середину (0,3…0,65 высоты рамки символа) проходит
  тонкая горизонтальная линия цвета правки (#B5082E — красный, #2E97D3 — синий на с.32);
  линия на уровне базовой линии (≥ 0,65 высоты) — подчёркивание вставки, текст остаётся;
- в колонке 2 удалённые фрагменты оформлены как `~~…~~` (Markdown-зачёркивание —
  так же, как они видны в исходнике); пробелы на краях фрагмента вынесены за маркеры,
  чтобы Markdown отрисовал зачёркивание; оценивается текст после принятия правок
  (`accepted` — без удалённых фрагментов);
- выноска на поле «Отформатировано: русский» (с.12, x > 405) — служебная пометка Word,
  не текст ТЗ; не переносится.
- 19 глифов маркера списка U+F0B7 (SymbolMT, x = 119,9, с.18–20, 28) лежат вне области
  отсечения ячейки и на рендере не видны: в колонку 2 не переносятся, но строка рядом с
  таким маркером — начало абзаца списка (`<br>`); так 8.3 получает 5 пунктов, а не 3;
- всё, что не попало в строки, записано в `excluded` с причиной (глоссарий — с `~~…~~`,
  шапки таблицы, маркеры «o», невидимые маркеры, титул ТЗ-2, выноска) — по ним
  `check_source.py` сводит баланс символов.

Структура:

- с.1–4 «1. Термины и определения» — глоссарий, не требования (как в RUN-0070/0072);
- с.4 «2. Общие требования к оказанию услуг Исполнителем» — заголовок и 4 пункта с
  маркером «o» без номера: колонка 1 пустая (номера в исходнике нет); пустой абзац с
  маркером U+F0B7 без текста не переносится;
- с.4–31 таблица «Функциональные требования» (№ п/п / Требование / Требуемое значение):
  строка начинается номером в колонке «№ п/п» (x < 125), продолжение строки на
  следующей странице приклеивается к ней, шапка таблицы на каждой странице пропускается.
  Колонка 1 — номер как в исходнике (с точкой или без: «2.14.8.1», «10.1»), колонка 2 —
  текст колонки «Требование». «Требуемое значение» («наличие») сохраняется в поле
  `value` — это не оценка поставщика и в колонку 3 не переносится;
- с.32–33 вложенный документ «Техническое задание на оказание услуг по автоматизации …
  ТО ВДГО/ВКГО …»: титул — разделитель документа (не требование), вводная фраза и
  нумерованные абзацы 1, 1.1 … 5.3; пункты списка «−» (глиф SymbolMT U+F02D = минус, как в
  RUN-0072) продолжают предложение предыдущего пункта, заканчивающееся двоеточием
  (2.3, 3.2), и входят в него через `<br>`.

Переносы строк внутри ячейки: строка PDF, после которой следующее слово поместилось бы
в ширину колонки, — твёрдый разрыв (`<br>`); иначе это мягкий перенос вёрстки Word,
строки склеиваются одним пробелом (хвостовой пробел снимается), перенос после дефиса
(«аудио-», «чат-») — склейка без пробела. Перед маркером списка «·» и после увеличенного
межабзацного интервала — всегда `<br>`. Опечатки, регистр, пунктуация, пробелы внутри
строки, кириллические «МАХ» и латинские «MAX» не меняются.

Запуск: python3 -I experiments/issue_482/make_transcription.py /path/to/tz-1140.pdf
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

import pymupdf

HERE = Path(__file__).resolve().parent
TITLE = "ТЗ газификация ХХХ области.pdf"
EDIT_COLORS = ((0.71, 0.031, 0.18), (0.18, 0.592, 0.827))
MARGIN_X = 405.0
NUM = re.compile(r"^\d+(?:\.\d+)*\.?$")
DOC2_PAGE = 32
SYMBOL_MAP = {"": "−"}


def close(a: tuple, b: tuple) -> bool:
    return all(abs(x - y) < 0.01 for x, y in zip(a, b))


def edit_lines(page) -> list[tuple[float, float, float]]:
    out = []
    for dr in page.get_drawings():
        c = dr.get("fill") or dr.get("color")
        r = dr["rect"]
        if c and r.height < 2 and r.width > 1 and any(close(c, e) for e in EDIT_COLORS):
            out.append((r.x0, r.x1, (r.y0 + r.y1) / 2))
    return out


def hidden_bullets(page) -> list[tuple[float, float, float]]:
    """Глифы маркера U+F0B7, обрезанные областью отсечения ячейки (на рендере не видны).

    pymupdf с флагом TEXT_CLIP (входит в TEXTFLAGS_TEXT) их не возвращает; без флага —
    возвращает. Это маркеры абзацев списка Word: символа в колонке 2 нет, но строка рядом
    с таким маркером — начало нового абзаца (твёрдый разрыв `<br>`)."""
    def bullets(flags):
        out = []
        for b in page.get_text("rawdict", flags=flags)["blocks"]:
            for ln in b.get("lines", []):
                for sp in ln["spans"]:
                    for ch in sp["chars"]:
                        if ch["c"] == "\uf0b7":
                            x0, y0, x1, y1 = ch["bbox"]
                            out.append((round(x0, 1), round(y0, 1), round(y1, 1)))
        return out
    visible = set(bullets(pymupdf.TEXTFLAGS_TEXT))
    return [b for b in bullets(pymupdf.TEXTFLAGS_TEXT & ~pymupdf.TEXT_CLIP) if b not in visible]


def page_lines(page) -> list[dict]:
    """Строки страницы: [{x0, x1, y0, y1, chars: [(c, deleted, x0, x1)]}] (поля исключены)."""
    marks = edit_lines(page)
    hidden = hidden_bullets(page)
    res = []
    raw = page.get_text("rawdict", flags=pymupdf.TEXTFLAGS_TEXT)
    for b in raw["blocks"]:
        for ln in b.get("lines", []):
            chars = []
            for sp in ln["spans"]:
                for ch in sp["chars"]:
                    x0, y0, x1, y1 = ch["bbox"]
                    cx, h = (x0 + x1) / 2, (y1 - y0) or 1
                    deleted = any(
                        mx0 - 0.3 <= cx <= mx1 + 0.3 and 0.3 <= (my - y0) / h < 0.65
                        for mx0, mx1, my in marks
                    )
                    chars.append((ch["c"], deleted, x0, x1))
            text = "".join(c for c, *_ in chars)
            if not text.strip():
                continue
            x0, y0, x1, y1 = ln["bbox"]
            if x0 > MARGIN_X:
                res.append({"margin": True, "text": text, "y0": y0})
                continue
            hb = any(bx < x0 and abs((by0 + by1) / 2 - (y0 + y1) / 2) < 3 for bx, by0, by1 in hidden)
            res.append({"x0": x0, "x1": x1, "y0": y0, "y1": y1, "chars": chars, "text": text,
                        "hidden_bullet": hb})
    for bx, by0, by1 in hidden:
        res.append({"hidden": True, "text": "\uf0b7", "y0": by0, "y1": by1, "x0": bx})
    res.sort(key=lambda l: (round(l.get("y1", l["y0"])), l.get("x0", 999)))
    return res


def segs(chars) -> list[list]:
    """[(text, deleted)] — смежные символы с одинаковым признаком удаления."""
    out: list[list] = []
    for c, d, *_ in chars:
        c = SYMBOL_MAP.get(c, c)
        if out and out[-1][1] == d:
            out[-1][0] += c
        else:
            out.append([c, d])
    return out


def render(parts: list[list]) -> tuple[str, str]:
    """(visible-with-~~, accepted) из списка сегментов; пробелы выносятся за маркеры."""
    merged: list[list] = []
    for t, d in parts:
        if merged and merged[-1][1] == d:
            merged[-1][0] += t
        else:
            merged.append([t, d])
    vis, acc = "", ""
    for t, d in merged:
        if d and t.strip():
            lead = t[: len(t) - len(t.lstrip())]
            trail = t[len(t.rstrip()):]
            vis += lead + "~~" + t.strip() + "~~" + trail
        else:
            vis += t
        if not d:
            acc += t
    return vis, re.sub(r" {2,}", lambda m: m.group(0), acc)


class Cell:
    """Текст ячейки как последовательность строк PDF с решением о разрыве между ними."""

    def __init__(self, right: float):
        self.right = right
        self.parts: list[list] = []  # сегменты (text, deleted), разделители — ("\n", None)
        self.last = None

    def add(self, line: dict, chars) -> None:
        sg = segs(chars)
        if self.last is not None:
            prev = self.last
            first = "".join(c for c, *_ in chars).lstrip()
            word = first.split(" ")[0]
            # ширина первого слова следующей строки
            wchars = [ch for ch in chars if ch[0].strip()]
            ww = 0.0
            if wchars:
                n = len(word)
                ww = wchars[min(n, len(wchars)) - 1][3] - wchars[0][2]
            gap = line["y0"] - prev["y1"]
            fits = prev["rx"] + 2.5 + ww < self.right
            bullet = first[:1] in ("·", "", "−", "") or line.get("hidden_bullet")
            hard = bullet or gap > 3.0 or fits
            self._strip_trailing()
            prev_vis = "".join(t for t, d in self.parts if d is not None)
            if hard:
                self.parts.append(["<br>", None])
            elif re.search(r"[A-Za-zА-Яа-яЁё]-$", prev_vis):
                pass
            else:
                self.parts.append([" ", self._last_del()])
            sg = self._lstrip(sg)
        self.parts.extend(sg)
        ink = [ch for ch in chars if ch[0].strip()]
        self.last = {"y1": line["y1"], "rx": ink[-1][3] if ink else line["x1"]}

    def _last_del(self):
        for t, d in reversed(self.parts):
            if d is not None:
                return d
        return False

    def _strip_trailing(self) -> None:
        while self.parts and self.parts[-1][1] is not None:
            t = self.parts[-1][0].rstrip(" ")
            if t:
                self.parts[-1][0] = t
                return
            self.parts.pop()

    @staticmethod
    def _lstrip(sg):
        while sg:
            t = sg[0][0].lstrip(" ")
            if t:
                sg[0][0] = t
                return sg
            sg.pop(0)
        return sg

    def result(self) -> tuple[str, str]:
        self._strip_trailing()
        parts, out = [], []
        for t, d in self.parts:
            if d is None:
                out.append(parts)
                parts = []
            else:
                parts.append([t, d])
        out.append(parts)
        vis, acc = [], []
        for p in out:
            v, a = render(p)
            vis.append(v.strip(" ") if v.strip() else v)
            acc.append(a.strip(" "))
        acc_text = "<br>".join(x for x in acc if x)
        return "<br>".join(vis), acc_text


def is_header(text: str) -> bool:
    return text.strip() in ("№ п/п", "Требование", "Требуемое", "значение")


def main() -> None:
    pdf = Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/dl482/tz-1140.pdf")
    data = pdf.read_bytes()
    doc = pymupdf.open(pdf)
    rows: list[dict] = []
    excluded: list[dict] = []
    state = "terms"
    cur = None
    value_cell = None

    def flush():
        nonlocal cur
        if cur is not None:
            vis, acc = cur["cell"].result()
            num_vis, num_acc = render(cur["num"]) if cur["num"] else ("", "")
            rows.append({
                "doc": cur["doc"], "num": num_vis.strip(), "num_accepted": num_acc.strip(),
                "req": vis, "accepted": acc, "value": cur.get("value", "").strip(),
                "page": cur["page"],
            })
        cur = None

    for pno, page in enumerate(doc, start=1):
        for ln in page_lines(page):
            if ln.get("hidden"):
                excluded.append({"page": pno, "reason": "невидимый маркер списка U+F0B7 (вне области отсечения ячейки; учтён как начало абзаца — `<br>`)", "text": ln["text"]})
                continue
            if ln.get("margin"):
                excluded.append({"page": pno, "reason": "выноска на поле (служебная пометка Word)", "text": ln["text"].strip()})
                continue
            text = ln["text"]
            s = text.strip()
            if state == "terms":
                if s.startswith("2. Общие требования"):
                    state = "general"
                    cur = {"doc": 1, "num": segs(ln["chars"][:2]), "cell": Cell(402.5), "page": pno}
                    cur["cell"].add(ln, ln["chars"][3:])
                    flush()
                    continue
                excluded.append({"page": pno, "reason": "раздел «1. Термины и определения» — глоссарий",
                                 "text": render(segs(ln["chars"]))[0].strip()})
                continue
            if state == "general":
                if s == "Функциональные требования":
                    flush()
                    state = "table"
                    excluded.append({"page": pno, "reason": "заголовок таблицы", "text": s})
                    continue
                if s in ("",):
                    excluded.append({"page": pno, "reason": "пустой абзац списка (маркер U+F0B7 без текста)", "text": s})
                    continue
                if s == "o":
                    excluded.append({"page": pno, "reason": "маркер списка «o» (номера в источнике нет)", "text": s})
                    flush()
                    cur = {"doc": 1, "num": [], "cell": Cell(402.5), "page": pno, "marker_y": ln["y0"]}
                    continue
                cur["cell"].add(ln, ln["chars"])
                continue
            if state == "table":
                if pno >= DOC2_PAGE:
                    flush()
                    state = "doc2"
                elif is_header(s):
                    excluded.append({"page": pno, "reason": "повтор шапки таблицы", "text": s})
                    continue
                else:
                    x0 = ln["x0"]
                    if x0 < 125:
                        flush()
                        cur = {"doc": 1, "num": segs(ln["chars"]), "cell": Cell(336.0), "page": pno, "value": ""}
                        cur["num"] = [[t.rstrip() if i == len(cur["num"]) - 1 else t, d] for i, (t, d) in enumerate(cur["num"])]
                        continue
                    if x0 > 345:
                        cur["value"] = (cur.get("value", "") + " " + "".join(
                            ("~~" + c + "~~") if d else c for c, d in segs(ln["chars"]))).strip()
                        continue
                    cur["cell"].add(ln, ln["chars"])
                    continue
            if state == "doc2":
                if ln["y0"] < 232 and pno == DOC2_PAGE:
                    vis, _ = render(segs(ln["chars"]))
                    excluded.append({"page": pno, "reason": "титул вложенного документа (разделитель)", "text": vis.strip()})
                    continue
                x0 = ln["x0"]
                if x0 < 75 and NUM.match(s):
                    flush()
                    cur = {"doc": 2, "num": [[s, False]], "cell": Cell(402.5), "page": pno}
                    continue
                if x0 < 75 and s == "":
                    cur["pending_bullet"] = True
                    continue
                m = re.match(r"^(\d+\.\d+\.\d+)\s+(.*)$", s)
                if x0 < 75 and m and not cur.get("pending_bullet"):
                    flush()
                    cur = {"doc": 2, "num": [[m.group(1), False]], "cell": Cell(402.5), "page": pno}
                    n = len(text) - len(text.lstrip())
                    rest = ln["chars"][n + len(m.group(1)):]
                    cur["cell"].add(ln, rest)
                    continue
                if cur is None:
                    cur = {"doc": 2, "num": [], "cell": Cell(402.5), "page": pno}
                if cur.get("pending_bullet"):
                    cur["pending_bullet"] = False
                    chars = [("", False, ln["x0"] - 20, ln["x0"] - 14), (" ", False, ln["x0"] - 14, ln["x0"] - 12)] + ln["chars"]
                    cur["cell"].add(ln, chars)
                    continue
                # первая строка вводной фразы закрывает предыдущую строку с пустым номером
                cur["cell"].add(ln, ln["chars"])
    flush()
    out = {
        "title": TITLE,
        "sha256": hashlib.sha256(data).hexdigest(),
        "size": len(data),
        "pages": doc.page_count,
        "excluded": excluded,
        "rows": [
            [f"R{i:03d}", r["num"], r["req"], f"p{r['page']}", r["accepted"], r["value"], r["doc"]]
            for i, r in enumerate(rows, start=1)
        ],
    }
    (HERE / "source_transcription.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"rows: {len(rows)}, excluded lines: {len(excluded)}, sha256 {out['sha256']}")


if __name__ == "__main__":
    main()
