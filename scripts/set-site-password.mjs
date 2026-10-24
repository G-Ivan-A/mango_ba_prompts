#!/usr/bin/env node
// Смена системного пароля сайта (issue #388).
//
// Пароль берётся из переменной окружения SITE_PASSWORD или из stdin и в
// репозиторий не пишется: в site/password-hashes.json попадают только новая
// соль и SHA-256(salt + пароль) под ключом "site". Порядок смены —
// docs/site-access.md.
//
//   SITE_PASSWORD='<новый пароль>' node scripts/set-site-password.mjs
//   printf '%s' '<новый пароль>' | node scripts/set-site-password.mjs
import crypto from "node:crypto";
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const HASHES = path.join(ROOT, "site", "password-hashes.json");
const KEY = "site";

// Та же нормализация, что в site/gate.js: пробелы по краям не важны, регистр
// не важен.
export function normalizePassword(value) {
  return String(value || "").trim().toUpperCase();
}

export function hashPassword(salt, password) {
  return crypto.createHash("sha256").update(salt + normalizePassword(password), "utf8").digest("hex");
}

async function readStdin() {
  if (process.stdin.isTTY) {
    return "";
  }
  const chunks = [];
  for await (const chunk of process.stdin) {
    chunks.push(chunk);
  }
  return Buffer.concat(chunks).toString("utf8");
}

async function main() {
  const password = normalizePassword(process.env.SITE_PASSWORD || (await readStdin()));
  if (!password) {
    console.error("Пароль не задан: передайте SITE_PASSWORD или строку в stdin.");
    return 1;
  }
  const hashes = JSON.parse(await fs.readFile(HASHES, "utf8"));
  const salt = crypto.randomBytes(8).toString("hex");
  hashes[KEY] = {
    algorithm: "SHA-256(salt + UPPERCASE(trim(password)))",
    salt,
    hash: hashPassword(salt, password),
  };
  await fs.writeFile(HASHES, `${JSON.stringify(hashes, null, 2)}\n`, "utf8");
  console.log(`site/password-hashes.json: ключ "${KEY}" обновлён (новая соль ${salt}).`);
  return 0;
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  process.exitCode = await main();
}
