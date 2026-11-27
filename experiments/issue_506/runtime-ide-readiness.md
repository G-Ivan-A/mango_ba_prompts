# Аудит готовности runtime к этапу 2 (IDE), issue #506

Сгенерировано `experiments/issue_506/audit_runtime_ide_readiness.py`. Только чтение.

## Срез `main` — `fe623c6b` (fe623c6b190ca987127c3ff1de36ed8b7eb3e24f)

`AGENTS.md`: 12070 байт, версия 0.7.

| ID | Что проверяется | Есть | Свидетельство | Локатор |
| --- | --- | --- | --- | --- |
| RT-01 | AGENTS.md в корне | да | AGENTS.md, 12070 байт | `AGENTS.md:1` |
| RT-02 | Навыки, плоский каталог skills/<имя>.md | да | 11 файлов | `skills/` |
| RT-03 | Нативные навыки .agents/skills/<имя>/SKILL.md | **нет** | 0 файлов | `.agents/skills/` |
| RT-04 | Конфигурация клиента opencode.json | **нет** | нет | `opencode.json` |
| RT-05 | Агенты OpenCode (оркестратор primary, исполнители subagent) | **нет** | нет .opencode/agents/ | `.opencode/agents/` |
| RT-06 | Входные команды /a-in, /a-core, /a-work, /a-release | **нет** | /a-in: нет; /a-core: нет; /a-work: нет; /a-release: нет | `.opencode/commands/` |
| RT-07 | Конфигурация MCP (Jira, Confluence, веб) | **нет** | нет | `opencode.json#mcp` |
| RT-08 | Маршрут потока: шаги BCREQ этапа 1 (Ш-*, AIN-01…24) в runtime | **нет** | маршрут RG-BCREQ-v1: 12 узлов n1…n12; AIN-01 в исполнимых файлах: нет | `routes/rg-bcreq-v1.yaml, routes/run-sheet-template.yaml` |
| RT-09 | Карта автономных шагов и гейтов (Г-IN, Г-С1, Г-W, Выпуск, AIN-21) | **нет** | Г-IN: нет; Г-С1: нет; Г-W: нет; AIN-21: нет; Р-09: нет | `AGENTS.md, routes/` |
| RT-10 | Маркер ACCESS_GAP и BLOCKED (Р-19) | **нет** | нет в AGENTS.md | `AGENTS.md` |
| RT-11 | Оркестратор: контракт в AGENTS.md или агент OpenCode | **нет** | упоминания вне контракта: routes/run-sheet-template.yaml:1 | `AGENTS.md, .opencode/agents/` |
| RT-12 | Абсолютные URL репозиториев G-Ivan-A в исполнимых файлах | **нет** | 1 URL в 1 файлах | `docs/guides/00-quick-start.md:13` |
| RT-13 | Относительные пути AGENTS.md разрешаются в клоне | да | 16 из 16 | `AGENTS.md` |
| RT-14 | Локальная БЗ docs/kb | да | 6931 файлов; README: да; MAP.json: да; USAGE.md: да | `docs/kb/` |
| RT-15 | Таксономии и контракты | да | taxonomy: 11; contracts: 5 | `taxonomy/, contracts/` |
| RT-16 | Smoke runtime не запрещает .agents/.opencode | **нет** | упоминания .agents/.opencode в tests/runtime-smoke.sh: строка 46 | `tests/runtime-smoke.sh` |

URL репозиториев в исполнимых файлах:

- `docs/guides/00-quick-start.md`: строка 13

## Срез `pr29` — `9421edad` (pr29)

`AGENTS.md`: 14262 байт, версия 0.8.

| ID | Что проверяется | Есть | Свидетельство | Локатор |
| --- | --- | --- | --- | --- |
| RT-01 | AGENTS.md в корне | да | AGENTS.md, 14262 байт | `AGENTS.md:1` |
| RT-02 | Навыки, плоский каталог skills/<имя>.md | да | 11 файлов | `skills/` |
| RT-03 | Нативные навыки .agents/skills/<имя>/SKILL.md | да | 11 файлов | `.agents/skills/` |
| RT-04 | Конфигурация клиента opencode.json | **нет** | нет | `opencode.json` |
| RT-05 | Агенты OpenCode (оркестратор primary, исполнители subagent) | **нет** | нет .opencode/agents/ | `.opencode/agents/` |
| RT-06 | Входные команды /a-in, /a-core, /a-work, /a-release | **нет** | /a-in: нет; /a-core: нет; /a-work: нет; /a-release: нет | `.opencode/commands/` |
| RT-07 | Конфигурация MCP (Jira, Confluence, веб) | **нет** | нет | `opencode.json#mcp` |
| RT-08 | Маршрут потока: шаги BCREQ этапа 1 (Ш-*, AIN-01…24) в runtime | **нет** | маршрут RG-BCREQ-v1: 12 узлов n1…n12; AIN-01 в исполнимых файлах: нет | `routes/rg-bcreq-v1.yaml, routes/run-sheet-template.yaml` |
| RT-09 | Карта автономных шагов и гейтов (Г-IN, Г-С1, Г-W, Выпуск, AIN-21) | **нет** | Г-IN: нет; Г-С1: нет; Г-W: нет; AIN-21: нет; Р-09: нет | `AGENTS.md, routes/` |
| RT-10 | Маркер ACCESS_GAP и BLOCKED (Р-19) | да | ACCESS_GAP в AGENTS.md: строка 99 | `AGENTS.md` |
| RT-11 | Оркестратор: контракт в AGENTS.md или агент OpenCode | **нет** | упоминания вне контракта: routes/run-sheet-template.yaml:1 | `AGENTS.md, .opencode/agents/` |
| RT-12 | Абсолютные URL репозиториев G-Ivan-A в исполнимых файлах | **нет** | 1 URL в 1 файлах | `docs/guides/00-quick-start.md:13` |
| RT-13 | Относительные пути AGENTS.md разрешаются в клоне | да | 19 из 19 | `AGENTS.md` |
| RT-14 | Локальная БЗ docs/kb | да | 6931 файлов; README: да; MAP.json: да; USAGE.md: да | `docs/kb/` |
| RT-15 | Таксономии и контракты | да | taxonomy: 11; contracts: 5 | `taxonomy/, contracts/` |
| RT-16 | Smoke runtime не запрещает .agents/.opencode | да | упоминания .agents/.opencode в tests/runtime-smoke.sh: строка 53 | `tests/runtime-smoke.sh` |

URL репозиториев в исполнимых файлах:

- `docs/guides/00-quick-start.md`: строка 13

## Спица: исполнимые промпты

- Исполнимых промптов (без архива и README): 62.
- С URL репозиториев G-Ivan-A: 30; по репозиториям: `ba-ai-metamodel` — 27, `mango-ba-ai-runtime` — 130.
- С общим вопросом «Продолжаем?/идти дальше?»: 0 файлов.
- Закреплённые цели URL, которые есть в клоне `fe623c6b` и заменяются относительным путём: 14 целей, 130 ссылок.
- Цели, которых в клоне runtime нет (пробел передачи): 1 целей, 27 ссылок; `ba-ai-metamodel@e1f67e26:research/mango/2026-05-22-classification.md` — 27.
- Маршрут A-IN: RFC-AIN-001 v0.3 `accepted`, шагов 24; `advance_while_paused=False`, `resume_requires_ba_instruction=True`.

