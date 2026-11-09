import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import {test} from 'node:test';
import {parseFrontmatter, stripFrontmatter} from '../../scripts/generate-pages-data.mjs';

const archive = new URL('../../prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md', import.meta.url);
const source = await fs.readFile(archive, 'utf8');
const expected = parseFrontmatter(source);
assert.equal(expected.operation, 'understanding');
const variants = {
  LF: source,
  CRLF: source.replace(/\n/g, '\r\n'),
  'BOM + LF': '\uFEFF' + source,
  'BOM + CRLF': '\uFEFF' + source.replace(/\n/g, '\r\n'),
  mixed: source.replace(/\n/, '\r\n'),
};
for (const [name, text] of Object.entries(variants)) {
  test(`real archive metadata and copied body survive ${name}`, {timeout: 5000}, () => {
    assert.deepEqual(parseFrontmatter(text), expected);
    assert.equal(stripFrontmatter(text).replace(/\r\n/g, '\n'), stripFrontmatter(source));
    assert.ok(!stripFrontmatter(text).includes('runtime_sha:'));
  });
}
test('absent/unclosed frontmatter is not guessed; body separators stay intact', () => {
  for (const text of ['plain text\n', '---\noperation: understanding\n', '---\noperation: understanding\n---invalid\nbody\n']) {
    assert.deepEqual(parseFrontmatter(text), {});
    assert.equal(stripFrontmatter(text), text);
  }
  const text = '---\r\noperation: understanding\r\n---\r\nbody\r\n---\r\nlast\r\n';
  assert.equal(stripFrontmatter(text), 'body\r\n---\r\nlast\n');
});
test('all historical frontmatter types and unknown values remain visible', () => {
  const text = '\uFEFF---\r\noperation: obsolete\r\nsteps: [Ш-А]\r\nprocesses: ["Приём и контекст"]\r\nexecutable: true\r\ncanonical: false\r\n---';
  assert.deepEqual(parseFrontmatter(text), {
    operation: 'obsolete', steps: ['Ш-А'], processes: ['Приём и контекст'], executable: true, canonical: false,
  });
  assert.equal(stripFrontmatter(text), '\n');
});
