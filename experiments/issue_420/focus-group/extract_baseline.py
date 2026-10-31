#!/usr/bin/env python3
"""Issue #420: extract the current Standards page text (site/index.html, read-only) to Markdown.

    python3 experiments/issue_420/focus-group/extract_baseline.py

Output: experiments/issue_420/focus-group/baseline-page.md — the text a reader sees on the page
today, with headings, list items and collapsed <details> kept. Used as the baseline stimulus for
the synthetic focus group, so both variants are judged as plain text with the same structure cues.
"""
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SRC = ROOT / "site/index.html"
OUT = Path(__file__).resolve().parent / "baseline-page.md"
BLOCK = {"h1": "# ", "h2": "## ", "h3": "### ", "p": "", "li": "- ", "dt": "**", "dd": "", "summary": "▸ ", "strong": None, "span": None, "a": None}


class Extract(HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth = 0  # depth inside section#standards
        self.lines: list[str] = []
        self.buf = ""
        self.stack: list[str] = []

    def flush(self, prefix=""):
        text = " ".join(self.buf.split())
        if text:
            if prefix == "**":
                text = f"**{text}**"
                prefix = ""
            self.lines.append(prefix + text)
        self.buf = ""

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "section" and attrs.get("id") == "standards":
            self.depth = 1
            return
        if not self.depth:
            return
        if tag in ("section", "div", "article", "nav", "aside", "ul", "dl", "details"):
            self.depth += 1
        if tag in ("h1", "h2", "h3", "p", "li", "dt", "dd", "summary", "div"):
            self.flush()
        if tag == "a" and self.stack and False:
            pass
        self.stack.append(tag)

    def handle_endtag(self, tag):
        if not self.depth:
            return
        if tag in ("section", "div", "article", "nav", "aside", "ul", "dl", "details"):
            self.depth -= 1
        if tag in ("h1", "h2", "h3", "p", "li", "dt", "dd", "summary", "a") and tag in BLOCK:
            prefix = BLOCK[tag]
            if tag == "a":
                # Navigation links are separate lines; inline links stay in the paragraph.
                if any(t == "nav" for t in self.stack):
                    self.flush("- ")
            else:
                self.flush(prefix or "")
        if tag == "div":
            self.flush()
        if self.stack:
            self.stack.pop()
        if tag in ("article", "aside", "nav", "details") or (tag == "div" and not self.buf):
            if self.lines and self.lines[-1] != "":
                self.lines.append("")

    def handle_data(self, data):
        if self.depth:
            self.buf += data


def main():
    parser = Extract()
    parser.feed(SRC.read_text(encoding="utf-8"))
    parser.flush()
    text = "\n".join(parser.lines)
    while "\n\n\n" in text:
        text = text.replace("\n\n\n", "\n\n")
    OUT.write_text(text.strip() + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}: {len(text.split())} words")


if __name__ == "__main__":
    main()
