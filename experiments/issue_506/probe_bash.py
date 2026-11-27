"""Experiment (#506, BL-192 Э5): can a shell command allowed by the IDE layer overwrite a protected file?

The mock model asks for one shell command; the script reports whether AGENTS.md changed.
Usage: probe_bash.py <opencode> <major> <command> [rt_dir]
"""
import io, json, os, shutil, subprocess, sys, tempfile, threading, time
from http.server import ThreadingHTTPServer
from pathlib import Path
rt = sys.argv[4] if len(sys.argv) > 4 else "/tmp/rt"
sys.path.insert(0, f"{rt}/tests")
import opencode_smoke as s

seen = []
class Probe(s.MockModel):
    def do_POST(self):
        raw = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        req = json.loads(raw or b"{}")
        tools = {t["function"]["name"]: t["function"] for t in req.get("tools", [])}
        shell = next((n for n in ("bash", "shell") if n in tools), None)
        done = any(m.get("role") == "tool" for m in req.get("messages", []))
        if shell and not done and req.get("stream"):
            s.MockModel.requests.append(req)
            props = tools[shell]["parameters"]["properties"]
            seen.append((shell, sorted(props)))
            args = {"command": CMD}
            if "description" in props: args["description"] = "probe"
            base = {"id": "p", "created": int(time.time()), "model": "m"}
            tcs = [{"index": 0, "id": "call_0", "type": "function", "function": {"name": shell, "arguments": json.dumps(args)}}]
            chunks = [{**base, "object": "chat.completion.chunk", "choices": [{"index": 0, "delta": {"role": "assistant", "tool_calls": tcs}, "finish_reason": None}]},
                      {**base, "object": "chat.completion.chunk", "choices": [{"index": 0, "delta": {}, "finish_reason": "tool_calls"}]},
                      {**base, "object": "chat.completion.chunk", "choices": [], "usage": {"prompt_tokens": 1, "completion_tokens": 1, "total_tokens": 2}}]
            body = b"".join(b"data: " + json.dumps(c).encode() + b"\n\n" for c in chunks) + b"data: [DONE]\n\n"
            return self._send(200, "text/event-stream", body)
        if done:
            s.MockModel.requests.append(req)
        self.rfile = io.BytesIO(raw)
        return s.MockModel.do_POST(self)

oc, major, CMD = sys.argv[1], int(sys.argv[2]), sys.argv[3]
srv = ThreadingHTTPServer(("127.0.0.1", 0), Probe); threading.Thread(target=srv.serve_forever, daemon=True).start()
home = Path(tempfile.mkdtemp(prefix="probe-home-"))
env = s.isolated_env(home, srv.server_address[1])
proj = Path(tempfile.mkdtemp(prefix="probe-proj-"))
files = subprocess.run(["git", "ls-files", "-co", "--exclude-standard"], cwd=rt, capture_output=True, text=True).stdout.split()
for f in files:
    if f.startswith("work/"): continue
    d = proj / f; d.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(Path(rt) / f, d)
subprocess.run(["git", "init", "-q", str(proj)])
subprocess.run(["git", "-C", str(proj), "add", "-A"]); subprocess.run(["git", "-C", str(proj), "-c", "user.name=p", "-c", "user.email=probe@localhost", "commit", "-qm", "base"])
before = (proj / "AGENTS.md").read_bytes()
if major >= 2:
    cmd = [oc, "run", "--standalone", "--archived", "-m", "smoke/m", "--agent", "bcreq-orchestrator", "SMOKE-1"]
else:
    cmd = [oc, "run", "--pure", "-m", "smoke/m", "--command", "a-in", "SMOKE-1"]
try:
    p = subprocess.run(cmd, cwd=proj, env={**env, "PWD": str(proj)}, capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=120)
    print("rc", p.returncode); print("ERR", p.stderr[-800:])
except subprocess.TimeoutExpired:
    print("rc timeout (client waits for an answer: ask)")
print("shell tool", seen)
for r in s.MockModel.requests:
    for m in r.get("messages", []):
        if m.get("role") == "tool": print("toolresult", str(m.get("content"))[:300])
after = (proj / "AGENTS.md").read_bytes()
print("COMMAND", CMD)
print("AGENTS.md unchanged", after == before, len(before), len(after))
