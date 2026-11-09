// Reproduce a CRLF checkout without changing any source or generated file.
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import path from 'node:path';
const originalRead = fs.readFile;
fs.readFile = async function (file, ...args) {
  const content = await originalRead.call(this, file, ...args);
  if (typeof content === 'string' && String(file).includes('prompts/archive/a-in-v2.7.0/')) {
    return (process.env.MANGO_PROBE_VARIANT === 'invalid'
      ? content.replace('operation: understanding', 'operation: __invalid__')
      : content).replace(/\r?\n/g, '\r\n');
  }
  return content;
};
const generated = new Map();
fs.writeFile = async (file, content) => {
  generated.set(path.basename(file), JSON.parse(content));
};
fs.rm = async () => {};
const generator = path.resolve('scripts/generate-pages-data.mjs');
process.argv[1] = generator;
await import(generator);

process.on('beforeExit', () => {
  if (process.exitCode) return;
  const catalog = generated.get('prompts.json');
  assert.equal(catalog.prompts.length, 57);
  assert.equal(catalog.prompts.filter(prompt => prompt.archiveInfo).length, 4);
  for (const prompt of catalog.prompts.filter(prompt => prompt.archiveInfo)) {
    assert.ok(prompt.content.includes('\r\n'), prompt.sourcePath);
    assert.ok(!prompt.body.startsWith('---'), prompt.sourcePath);
    assert.ok(prompt.frontmatter.operation, prompt.sourcePath);
  }
  assert.equal(generated.get('a-in-kit.json').steps.length, 24);
});
