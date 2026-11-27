"""Experiment: does a mock-model tool call hit the permission rules of the IDE layer?"""
import json, os, shutil, subprocess, sys, tempfile, threading, time
from http.server import ThreadingHTTPServer
sys.path.insert(0, "/tmp/rt/tests")
import opencode_smoke as s

calls = []
class Probe(s.MockModel):
    def do_POST(self):
        raw = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        req = json.loads(raw or b"{}"); s.MockModel.requests.append(req)
        base = {"id": "p", "created": int(time.time()), "model": "m"}
        msgs = req.get("messages", [])
        tools = {t["function"]["name"]: t["function"] for t in req.get("tools", [])}
        has_result = any(m.get("role") == "tool" for m in msgs)
        if "write" in tools and not has_result and req.get("stream"):
            props = tools["write"]["parameters"]["properties"]
            calls.append(sorted(props))
            key = "filePath" if "filePath" in props else ("path" if "path" in props else sorted(props)[0])
            proj = os.environ["PROBE_PROJECT"]
            tcs = []
            for i, rel in enumerate(["AGENTS.md", "work/SMOKE-1/probe.md"]):
                args = {key: os.path.join(proj, rel), "content": "probe\n"}
                tcs.append({"index": i, "id": f"call_{i}", "type": "function", "function": {"name": "write", "arguments": json.dumps(args)}})
            chunks = [{**base, "object": "chat.completion.chunk", "choices": [{"index": 0, "delta": {"role": "assistant", "tool_calls": tcs}, "finish_reason": None}]},
                      {**base, "object": "chat.completion.chunk", "choices": [{"index": 0, "delta": {}, "finish_reason": "tool_calls"}]},
                      {**base, "object": "chat.completion.chunk", "choices": [], "usage": {"prompt_tokens": 1, "completion_tokens": 1, "total_tokens": 2}}]
            body = b"".join(b"data: " + json.dumps(c).encode() + b"\n\n" for c in chunks) + b"data: [DONE]\n\n"
            return self._send(200, "text/event-stream", body)
        return super().do_POST.__func__(self) if False else s.MockModel.do_POST(self._replay(raw))
    def _replay(self, raw):
        import io
        self.rfile = io.BytesIO(raw); s.MockModel.requests.pop(); return self

oc, major = sys.argv[1], int(sys.argv[2])
srv = ThreadingHTTPServer(("127.0.0.1", 0), Probe); threading.Thread(target=srv.serve_forever, daemon=True).start()
home = __import__("pathlib").Path(tempfile.mkdtemp(prefix="probe-home-"))
env = s.isolated_env(home, srv.server_address[1])
proj = tempfile.mkdtemp(prefix="probe-proj-")
files = subprocess.run(["git", "ls-files", "-co", "--exclude-standard"], cwd="/tmp/rt", capture_output=True, text=True).stdout.split()
for f in files:
    d = os.path.join(proj, f); os.makedirs(os.path.dirname(d), exist_ok=True); shutil.copy2(os.path.join("/tmp/rt", f), d)
subprocess.run(["git", "init", "-q", proj]); env["PROBE_PROJECT"] = proj; os.environ["PROBE_PROJECT"] = proj
before = open(os.path.join(proj, "AGENTS.md"), "rb").read()
if major >= 2:
    cmd = [oc, "run", "--standalone", "--archived", "-m", "smoke/m", "--agent", "bcreq-orchestrator", "SMOKE probe"]
else:
    cmd = [oc, "run", "--pure", "-m", "smoke/m", "--command", "a-in", "SMOKE-1"]
p = subprocess.run(cmd, cwd=proj, env={**env, "PWD": proj}, capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=240)
print("rc", p.returncode); print("OUT", p.stdout[-1500:]); print("ERR", p.stderr[-1500:])
print("write props", calls)
print("AGENTS unchanged", open(os.path.join(proj, "AGENTS.md"), "rb").read() == before)
print("work probe exists", os.path.exists(os.path.join(proj, "work/SMOKE-1/probe.md")))
for r in s.MockModel.requests:
    names = [t["function"]["name"] for t in r.get("tools", [])]
    print("tools", names)
    for m in r.get("messages", []):
        if m.get("role") == "tool": print("toolresult", str(m.get("content"))[:300])
sysp = "\n".join(s.system_of(r) for r in s.MockModel.requests)
print("orchestrator prompt in system", "# Оркестратор процессов этапа 1" in sysp)
print("command text", any("Процесс: A-IN. Ключ задачи: SMOKE-1" in s.text_of(r) for r in s.MockModel.requests))
srv.shutdown(); shutil.rmtree(home, ignore_errors=True); shutil.rmtree(proj, ignore_errors=True)
