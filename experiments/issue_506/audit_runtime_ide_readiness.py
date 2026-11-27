#!/usr/bin/env python3
"""Issue #506: аудит готовности runtime к этапу 2 (OpenCode/IDE).

Только чтение. Ни runtime, ни спица не меняются; сеть не нужна.

Проверяет целевую модель IDE (issue #506, раздел «Целевая модель») по
клону runtime и по спице:

* что есть: ``AGENTS.md``, навыки (плоские и нативные ``<имя>/SKILL.md``),
  БЗ ``docs/kb``, таксономии, контракты, маршрут;
* чего нет: агенты и команды OpenCode, оркестратор, конфигурация MCP,
  карта автономных шагов и гейтов, маркер ``ACCESS_GAP``;
* пути: абсолютные URL в исполнимых файлах runtime и в исполнимых
  промптах спицы, относительные пути ``AGENTS.md`` разрешаются в клоне.

Запуск (один или несколько срезов runtime, каждый ``метка=путь[@ref]``)::

    python3 -I experiments/issue_506/audit_runtime_ide_readiness.py \
        --runtime main=/tmp/rt/rt@fe623c6b --runtime pr29=/tmp/rt/rt@pr29 \
        --out experiments/issue_506

``@ref`` читает файлы через ``git show``/``git ls-tree`` без checkout, так
что рабочее дерево клона не меняется. Выход — ``runtime-ide-readiness.json``
и ``runtime-ide-readiness.md``; журнал — stdout.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

SPOKE = Path(__file__).resolve().parents[2]

# Исполнимые для модели файлы runtime: то, что клиент IDE читает как
# инструкцию. docs/kb — справочный корпус, URL источников в нём допустимы.
RUNTIME_EXEC_PREFIXES = (
    "AGENTS.md", "skills/", ".agents/", ".opencode/", "contracts/", "routes/",
    "templates/", "docs/guides/", "opencode.json", "opencode.jsonc",
)
URL_RE = re.compile(r"https?://[^\s)>\]\"'`]+")
REPO_URL_RE = re.compile(r"https?://(?:github\.com|raw\.githubusercontent\.com)/G-Ivan-A/([A-Za-z0-9_.-]+)")
BACKTICK_PATH_RE = re.compile(r"`((?:skills|contracts|routes|templates|taxonomy|golden|evaluation|docs|tests|\.agents|\.opencode)/[^`\s*<>]*)`")
ENTRY_COMMANDS = ("a-in", "a-core", "a-work", "a-release")


class Tree:
    """Срез runtime: рабочее дерево или коммит без checkout."""

    def __init__(self, root: Path, ref: str | None):
        self.root, self.ref = root, ref
        if ref:
            out = self._git("ls-tree", "-r", "--name-only", ref)
            self.files = sorted(out.splitlines())
            self.sha = self._git("rev-parse", ref).strip()
        else:
            self.files = sorted(
                str(p.relative_to(root)) for p in root.rglob("*")
                if p.is_file() and ".git" not in p.relative_to(root).parts
            )
            self.sha = self._git("rev-parse", "HEAD").strip()

    def _git(self, *args: str) -> str:
        return subprocess.run(["git", "-C", str(self.root), *args], check=True,
                              capture_output=True, text=True).stdout

    def read(self, path: str) -> str:
        if self.ref:
            res = subprocess.run(["git", "-C", str(self.root), "show", f"{self.ref}:{path}"],
                                 capture_output=True, text=True)
            return res.stdout if res.returncode == 0 else ""
        p = self.root / path
        return p.read_text(encoding="utf-8", errors="replace") if p.is_file() else ""

    def exists(self, path: str) -> bool:
        path = path.rstrip("/")
        return path in self.files or any(f.startswith(path + "/") for f in self.files)

    def glob(self, pattern: str) -> list[str]:
        rx = re.compile("^" + re.escape(pattern).replace(r"\*\*/", "(?:.*/)?").replace(r"\*", "[^/]*") + "$")
        return [f for f in self.files if rx.match(f)]


def line_of(text: str, needle: str) -> int | None:
    for i, line in enumerate(text.splitlines(), 1):
        if needle in line:
            return i
    return None


def audit_runtime(label: str, tree: Tree) -> dict:
    agents = tree.read("AGENTS.md")
    flat_skills = tree.glob("skills/*.md")
    native_skills = tree.glob(".agents/skills/*/SKILL.md")
    opencode_cfg = [f for f in ("opencode.json", "opencode.jsonc", ".opencode/opencode.json") if tree.exists(f)]
    oc_agents = tree.glob(".opencode/agents/*.md") + tree.glob(".opencode/agent/*.md")
    oc_commands = tree.glob(".opencode/commands/*.md") + tree.glob(".opencode/command/*.md")
    mcp_files = [f for f in tree.files if re.search(r"(^|/)\.?mcp(\.[a-z]+)?\.jsonc?$", f)]
    cfg_text = "".join(tree.read(f) for f in opencode_cfg)
    exec_files = [f for f in tree.files if f.startswith(RUNTIME_EXEC_PREFIXES)]
    kb_files = [f for f in tree.files if f.startswith("docs/kb/")]

    urls: dict[str, list[dict]] = {}
    for f in exec_files:
        text = tree.read(f)
        for i, line in enumerate(text.splitlines(), 1):
            for m in URL_RE.finditer(line):
                urls.setdefault(f, []).append({"line": i, "url": m.group(0)})
    repo_urls = {
        f: [u for u in lst if REPO_URL_RE.match(u["url"])] for f, lst in urls.items()
    }
    repo_urls = {f: lst for f, lst in repo_urls.items() if lst}

    rel_paths = sorted(set(BACKTICK_PATH_RE.findall(agents)))
    unresolved = []
    for p in rel_paths:
        probe = p.split("<", 1)[0].rstrip("/") if "<" in p else p.rstrip("/")
        if probe and not tree.exists(probe):
            unresolved.append(p)

    route_files = tree.glob("routes/*.yaml")
    route_text = "\n".join(tree.read(f) for f in route_files)
    route_ids = re.findall(r"(?m)^route_graph_id:\s*(\S+)", route_text)
    route_nodes = re.findall(r"\{node:\s*(n\d+)", route_text)

    runtime_text = "\n".join(tree.read(f) for f in exec_files)
    commands_found = {c: [f for f in oc_commands if Path(f).stem == c] for c in ENTRY_COMMANDS}

    def marker(token: str) -> dict:
        hits = [f for f in exec_files if token in tree.read(f)]
        return {"token": token, "files": hits[:10], "count": len(hits)}

    smoke = tree.read("tests/runtime-smoke.sh")
    orch_hits = [f"{f}:{i}" for f in exec_files for i, line in enumerate(tree.read(f).splitlines(), 1)
                 if re.search(r"(?i)orchestrat|оркестратор", line)]
    checks = [
        {"id": "RT-01", "what": "AGENTS.md в корне", "present": bool(agents),
         "evidence": f"AGENTS.md, {len(agents.encode())} байт" if agents else "нет файла",
         "locator": "AGENTS.md:1"},
        {"id": "RT-02", "what": "Навыки, плоский каталог skills/<имя>.md", "present": bool(flat_skills),
         "evidence": f"{len(flat_skills)} файлов", "locator": "skills/"},
        {"id": "RT-03", "what": "Нативные навыки .agents/skills/<имя>/SKILL.md", "present": bool(native_skills),
         "evidence": f"{len(native_skills)} файлов", "locator": ".agents/skills/"},
        {"id": "RT-04", "what": "Конфигурация клиента opencode.json", "present": bool(opencode_cfg),
         "evidence": ", ".join(opencode_cfg) or "нет", "locator": "opencode.json"},
        {"id": "RT-05", "what": "Агенты OpenCode (оркестратор primary, исполнители subagent)", "present": bool(oc_agents),
         "evidence": ", ".join(oc_agents) or "нет .opencode/agents/", "locator": ".opencode/agents/"},
        {"id": "RT-06", "what": "Входные команды /a-in, /a-core, /a-work, /a-release",
         "present": all(commands_found.values()),
         "evidence": "; ".join(f"/{c}: {'есть' if v else 'нет'}" for c, v in commands_found.items()),
         "locator": ".opencode/commands/"},
        {"id": "RT-07", "what": "Конфигурация MCP (Jira, Confluence, веб)",
         "present": bool(mcp_files) or '"mcp"' in cfg_text,
         "evidence": ", ".join(mcp_files) or ('ключ mcp в opencode.json' if '"mcp"' in cfg_text else "нет"),
         "locator": "opencode.json#mcp"},
        {"id": "RT-08", "what": "Маршрут потока: шаги BCREQ этапа 1 (Ш-*, AIN-01…24) в runtime",
         "present": "AIN-01" in runtime_text,
         "evidence": (f"маршрут {', '.join(route_ids)}: {len(route_nodes)} узлов n1…n{len(route_nodes)}; "
                      f"AIN-01 в исполнимых файлах: {'да' if 'AIN-01' in runtime_text else 'нет'}"),
         "locator": ", ".join(route_files) or "routes/"},
        {"id": "RT-09", "what": "Карта автономных шагов и гейтов (Г-IN, Г-С1, Г-W, Выпуск, AIN-21)",
         "present": all(t in runtime_text for t in ("Г-IN", "Г-W", "AIN-21")),
         "evidence": "; ".join(f"{t}: {'да' if t in runtime_text else 'нет'}" for t in ("Г-IN", "Г-С1", "Г-W", "AIN-21", "Р-09")),
         "locator": "AGENTS.md, routes/"},
        {"id": "RT-10", "what": "Маркер ACCESS_GAP и BLOCKED (Р-19)", "present": "ACCESS_GAP" in agents,
         "evidence": f"ACCESS_GAP в AGENTS.md: строка {line_of(agents, 'ACCESS_GAP')}" if "ACCESS_GAP" in agents else "нет в AGENTS.md",
         "locator": "AGENTS.md"},
        {"id": "RT-11", "what": "Оркестратор: контракт в AGENTS.md или агент OpenCode",
         "present": bool(re.search(r"(?i)orchestrat|оркестратор", agents)) or bool(oc_agents),
         "evidence": ("упоминания вне контракта: " + ", ".join(orch_hits)) if orch_hits else "нет ни одного упоминания",
         "locator": "AGENTS.md, .opencode/agents/"},
        {"id": "RT-12", "what": "Абсолютные URL репозиториев G-Ivan-A в исполнимых файлах",
         "present": not repo_urls,
         "evidence": f"{sum(len(v) for v in repo_urls.values())} URL в {len(repo_urls)} файлах" if repo_urls else "0",
         "locator": ", ".join(f"{f}:{lst[0]['line']}" for f, lst in sorted(repo_urls.items())[:6]) or "—"},
        {"id": "RT-13", "what": "Относительные пути AGENTS.md разрешаются в клоне",
         "present": not unresolved,
         "evidence": f"{len(rel_paths) - len(unresolved)} из {len(rel_paths)}" + (f"; не найдены: {', '.join(unresolved[:8])}" if unresolved else ""),
         "locator": "AGENTS.md"},
        {"id": "RT-14", "what": "Локальная БЗ docs/kb", "present": bool(kb_files),
         "evidence": f"{len(kb_files)} файлов; README: {'да' if tree.exists('docs/kb/README.md') else 'нет'}; "
                     f"MAP.json: {'да' if tree.glob('docs/kb/**/MAP.json') else 'нет'}; USAGE.md: {'да' if tree.glob('docs/kb/**/USAGE.md') else 'нет'}",
         "locator": "docs/kb/"},
        {"id": "RT-15", "what": "Таксономии и контракты", "present": bool(tree.glob("taxonomy/*.yaml")) and bool(tree.glob("contracts/*.md")),
         "evidence": f"taxonomy: {len(tree.glob('taxonomy/*.yaml'))}; contracts: {len(tree.glob('contracts/*.md'))}",
         "locator": "taxonomy/, contracts/"},
        {"id": "RT-16", "what": "Smoke runtime не запрещает .agents/.opencode",
         "present": not re.search(r"\.agents|\.opencode", smoke) or "build_skills_mirror" in smoke or "mirror" in smoke,
         "evidence": f"упоминания .agents/.opencode в tests/runtime-smoke.sh: строка {line_of(smoke, '.agents') or line_of(smoke, '.opencode')}"
                     if re.search(r"\.agents|\.opencode", smoke) else "нет упоминаний",
         "locator": "tests/runtime-smoke.sh"},
    ]
    return {
        "label": label, "ref": tree.ref or "worktree", "sha": tree.sha,
        "agents_md_bytes": len(agents.encode()),
        "agents_md_version": (re.search(r"(?m)^version:\s*\"?([\d.]+)", agents) or re.search(r"[Вв]ерси[яи]\s*([\d.]+)", agents) or [None, None])[1],
        "checks": checks,
        "repo_urls": repo_urls,
        "unresolved_paths": unresolved,
        "markers": {t: marker(t) for t in ("Confluence", "Jira", "MCP", "ACCESS_GAP", "Г-IN", "AIN-")},
    }


PINNED_RE = re.compile(r"https?://github\.com/G-Ivan-A/([A-Za-z0-9_.-]+)/(?:blob|tree)/([0-9a-f]{7,40})/([^\s)>\]\"'`#]+)")


def audit_spoke(tree: Tree) -> dict:
    """Исполнимые промпты спицы: удалённые URL и общий вопрос «Продолжаем?».

    URL ``mango-ba-ai-runtime/blob/<sha>/<путь>`` пересчитывается в
    относительный путь клона: путь есть в срезе ``tree`` — замена
    механическая; пути нет — пробел передачи.
    """
    exec_prompts = sorted(
        p for p in (SPOKE / "prompts").rglob("*.md")
        if "archive" not in p.parts and p.name not in ("README.md",)
    )
    remote, generic = {}, {}
    for p in exec_prompts:
        rel = str(p.relative_to(SPOKE))
        text = p.read_text(encoding="utf-8")
        hits = [{"line": i, "repo": m.group(1)} for i, line in enumerate(text.splitlines(), 1)
                for m in REPO_URL_RE.finditer(line)]
        if hits:
            remote[rel] = hits
        g = [i for i, line in enumerate(text.splitlines(), 1) if re.search(r"(?i)продолжаем\?|продолжить\?|идти дальше\?", line)]
        if g:
            generic[rel] = g
    pinned: dict[tuple[str, str, str], int] = {}
    for p in exec_prompts:
        for m in PINNED_RE.finditer(p.read_text(encoding="utf-8")):
            key = (m.group(1), m.group(2)[:8], m.group(3))
            pinned[key] = pinned.get(key, 0) + 1
    convertible, not_in_clone = {}, {}
    for (repo, sha, path), n in sorted(pinned.items()):
        target = convertible if repo == "mango-ba-ai-runtime" and tree.exists(path) else not_in_clone
        target[f"{repo}@{sha}:{path}"] = n
    by_repo: dict[str, int] = {}
    for hits in remote.values():
        for h in hits:
            by_repo[h["repo"]] = by_repo.get(h["repo"], 0) + 1
    route = json.loads((SPOKE / "docs/ba-processes/bcreq-a-in-route.json").read_text(encoding="utf-8"))
    return {
        "exec_prompts": len(exec_prompts),
        "prompts_with_remote_urls": len(remote),
        "remote_urls_by_repo": dict(sorted(by_repo.items())),
        "remote_url_files": {k: v[:3] for k, v in sorted(remote.items())},
        "generic_continue_files": generic,
        "pinned_targets_relative_ok": convertible,
        "pinned_targets_missing_in_clone": not_in_clone,
        "clone_sha": tree.sha,
        "ain_route": {"id": route["id"], "version": route["version"], "status": route["status"],
                      "steps": route["step_count"], "interaction": route["interaction"]},
    }


def render_md(result: dict) -> str:
    out = ["# Аудит готовности runtime к этапу 2 (IDE), issue #506", "",
           "Сгенерировано `experiments/issue_506/audit_runtime_ide_readiness.py`. Только чтение.", ""]
    for rt in result["runtime"]:
        out += [f"## Срез `{rt['label']}` — `{rt['sha'][:8]}` ({rt['ref']})", "",
                f"`AGENTS.md`: {rt['agents_md_bytes']} байт, версия {rt['agents_md_version']}.", "",
                "| ID | Что проверяется | Есть | Свидетельство | Локатор |", "| --- | --- | --- | --- | --- |"]
        for c in rt["checks"]:
            out.append(f"| {c['id']} | {c['what']} | {'да' if c['present'] else '**нет**'} | {c['evidence']} | `{c['locator']}` |")
        out.append("")
        if rt["repo_urls"]:
            out += ["URL репозиториев в исполнимых файлах:", ""]
            for f, lst in sorted(rt["repo_urls"].items()):
                out.append(f"- `{f}`: " + ", ".join(f"строка {u['line']}" for u in lst[:5]) + (f" и ещё {len(lst) - 5}" if len(lst) > 5 else ""))
            out.append("")
    sp = result["spoke"]
    out += ["## Спица: исполнимые промпты", "",
            f"- Исполнимых промптов (без архива и README): {sp['exec_prompts']}.",
            f"- С URL репозиториев G-Ivan-A: {sp['prompts_with_remote_urls']}; по репозиториям: "
            + ", ".join(f"`{k}` — {v}" for k, v in sp["remote_urls_by_repo"].items()) + ".",
            f"- С общим вопросом «Продолжаем?/идти дальше?»: {len(sp['generic_continue_files'])} файлов"
            + ("; " + ", ".join(f"`{k}`:{v[0]}" for k, v in sorted(sp['generic_continue_files'].items())[:6]) if sp['generic_continue_files'] else "") + ".",
            f"- Закреплённые цели URL, которые есть в клоне `{sp['clone_sha'][:8]}` и заменяются относительным путём: "
            f"{len(sp['pinned_targets_relative_ok'])} целей, {sum(sp['pinned_targets_relative_ok'].values())} ссылок.",
            f"- Цели, которых в клоне runtime нет (пробел передачи): {len(sp['pinned_targets_missing_in_clone'])} целей, "
            f"{sum(sp['pinned_targets_missing_in_clone'].values())} ссылок"
            + ("; " + ", ".join(f"`{k}` — {v}" for k, v in sp['pinned_targets_missing_in_clone'].items()) if sp['pinned_targets_missing_in_clone'] else "") + ".",
            f"- Маршрут A-IN: {sp['ain_route']['id']} v{sp['ain_route']['version']} `{sp['ain_route']['status']}`, шагов {sp['ain_route']['steps']}; "
            f"`advance_while_paused={sp['ain_route']['interaction'].get('advance_while_paused')}`, "
            f"`resume_requires_ba_instruction={sp['ain_route']['interaction'].get('resume_requires_ba_instruction')}`.", ""]
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--runtime", action="append", required=True, help="метка=путь[@ref]")
    ap.add_argument("--out", default=str(Path(__file__).resolve().parent))
    args = ap.parse_args()
    runtime = []
    for spec in args.runtime:
        label, _, rest = spec.partition("=")
        path, _, ref = rest.partition("@")
        tree = Tree(Path(path), ref or None)
        res = audit_runtime(label, tree)
        runtime.append(res)
        missing = [c["id"] for c in res["checks"] if not c["present"]]
        print(f"[{label}] {res['sha'][:8]}: проверок {len(res['checks'])}, нет: {len(missing)} ({', '.join(missing)})")
    first = args.runtime[0].partition("=")[2]
    spoke = audit_spoke(Tree(Path(first.partition("@")[0]), first.partition("@")[2] or None))
    print(f"[spoke] промптов {spoke['exec_prompts']}, с URL G-Ivan-A: {spoke['prompts_with_remote_urls']}, "
          f"с «Продолжаем?»: {len(spoke['generic_continue_files'])}")
    result = {"issue": "https://github.com/G-Ivan-A/mango_ba_prompts/issues/506", "runtime": runtime, "spoke": spoke}
    out = Path(args.out)
    (out / "runtime-ide-readiness.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (out / "runtime-ide-readiness.md").write_text(render_md(result) + "\n", encoding="utf-8")
    print(f"выход: {out / 'runtime-ide-readiness.json'}, {out / 'runtime-ide-readiness.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
