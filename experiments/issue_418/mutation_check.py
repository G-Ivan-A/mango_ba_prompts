"""Мутационная проверка валидатора бэклога issue #418.

Каждая мутация портит одну вещь в копии репозитория (git worktree) и
ожидает, что scripts/validate_issue_418_backlog.py упадёт.

    python3 experiments/issue_418/mutation_check.py
"""
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

MUTATIONS = [
    ("цитата не из источника", "pr-ops/backlog-ba-model.md",
     "“Промпты в части уроков не правятся вручную.”", "“Промпты правятся вручную.”"),
    ("цитата длиннее 100 символов", "pr-ops/backlog-ba-model.md",
     "“Промпты в части уроков не правятся вручную.”", "“" + "а" * 101 + "”"),
    ("битый якорь", "pr-ops/backlog-repository.md",
     "roadmap.md#этапы", "roadmap.md#нет-такого-раздела"),
    ("неизвестное решение", "pr-ops/backlog-ba-model.md",
     "**Решение владельца.** Р-12.\n", "**Решение владельца.** Р-99.\n"),
    ("неизвестный статус", "pr-ops/BACKLOG.md",
     "| P0 | BL-202; Р-02 | TODO |", "| P0 | BL-202; Р-02 | ГОТОВО |"),
    ("строка без карточки", "pr-ops/backlog-ba-model.md",
     "### BL-104. ", "### BL-199. "),
    ("порядок этапов", "pr-ops/BACKLOG.md",
     "Порядок владельца: Этап 1 → ревизия мета-модели БА Хаба → этап 2 на OpenCode.",
     "Порядок: OpenCode, мета-модель, Этап 1."),
    ("нет ответа о мета-модели", "pr-ops/BACKLOG.md",
     "Критических предпосылок для её изменения нет.", "Предпосылки есть."),
    ("запрещённое поле frontmatter", "pr-ops/backlog-instruction.md",
     "type: backlog\n", "type: backlog\nai-generated: true\n"),
    ("потерян маркер issue #263", "pr-ops/BACKLOG.md",
     "evals и golden-set отсутствуют", "evals отсутствуют"),
    ("карточка без поля", "pr-ops/backlog-repository.md",
     "**Готово, когда.** Генератор читает", "Генератор читает"),
]


def main():
    failures = 0
    with tempfile.TemporaryDirectory() as tmp:
        tree = Path(tmp) / "wt"
        subprocess.run(["git", "worktree", "add", "-q", "--detach", str(tree), "HEAD"],
                       cwd=ROOT, check=True)
        try:
            for name, rel, old, new in MUTATIONS:
                path = tree / rel
                original = path.read_text(encoding="utf-8")
                if old not in original:
                    print(f"SKIP  {name}: образец не найден")
                    failures += 1
                    continue
                path.write_text(original.replace(old, new, 1), encoding="utf-8")
                run = subprocess.run([sys.executable, "scripts/validate_issue_418_backlog.py"],
                                     cwd=tree, capture_output=True, text=True)
                path.write_text(original, encoding="utf-8")
                caught = run.returncode != 0
                failures += not caught
                print(f"{'CAUGHT' if caught else 'MISSED'}  {name}")
            clean = subprocess.run([sys.executable, "scripts/validate_issue_418_backlog.py"],
                                   cwd=tree, capture_output=True, text=True)
            print(f"{'OK' if clean.returncode == 0 else 'FAIL'}  чистое дерево")
            failures += clean.returncode != 0
        finally:
            subprocess.run(["git", "worktree", "remove", "--force", str(tree)], cwd=ROOT)
    print(f"итог: {failures} проблем")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
