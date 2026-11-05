// Логирует файлы репозитория, которые читает генератор сайта.
// node --require ./experiments/issue_456/trace-generator.cjs scripts/generate-pages-data.mjs
const fs = require("fs"), path = require("path");
const root = process.cwd(), seen = new Set();
const note = (p) => { const r = path.relative(root, String(p)); if (!r.startsWith("..")) seen.add(r); };
for (const name of ["readFile", "readdir"]) {
  const orig = fs.promises[name];
  fs.promises[name] = function (p, ...a) { note(p); return orig.call(this, p, ...a); };
}
for (const name of ["readFileSync", "readdirSync"]) {
  const orig = fs[name];
  fs[name] = function (p, ...a) { note(p); return orig.call(this, p, ...a); };
}
process.on("exit", () => fs.writeFileSync(process.env.TRACE_OUT, [...seen].sort().join("\n") + "\n"));
