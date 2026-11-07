"""Сквозная типизация гейтов (BL-159, issue #433).

Точные замены «human gate» / «решение человека» на формулировки с типом
гейта (`человек`, `гибрид`, `llm`, `код`) и ключевостью по словарю потока
BCREQ, раздел 3. Скрипт идемпотентен: замена применяется, только если
старой строки нет в новой редакции; повторный запуск ничего не меняет.

Запуск: python3 experiments/issue_433/apply_gate_typing.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TODAY = "2026-11-03"
GLOSSARY_FROM_DOCS = "../standards/bcreq-flow-glossary.md#33-типы-гейта"

SILENCE_STD = (
    "Gate'ы привязаны к операциям с исполнителем `человек`\n"
    "([ba-ontology.md §3](ba-ontology.md), С3). Молчание — не согласие:\n"
    "решение на ключевом гейте — явный ответ человека (правило 4\n"
    "[словаря потока](bcreq-flow-glossary.md#33-типы-гейта), поправка 0.4\n"
    "RFC #427). Модель «молчание = согласие»\n"
    "([ADR-0003](../docs/adr/0003-creative-mode-governance.md)) относится к\n"
    "приёмке изменений репозитория и к решению на гейте не применяется;\n"
    "определение гейта в онтологии выравнивает решение владельца Р-16 (BL-162)."
)

SILENCE_ADR009 = (
    "Три обязательных ключевых гейта `человек` привязаны к операциям-исполнителям `человек`\n"
    "([ba-ontology.md §3](../../standards/ba-ontology.md), С3). Молчание — не\n"
    "согласие: решение на ключевом гейте — явный ответ человека (правило 4\n"
    "[словаря потока](../../standards/bcreq-flow-glossary.md#33-типы-гейта),\n"
    "поправка 0.4 RFC #427). Модель «молчание = согласие»\n"
    "([ADR-0003](0003-creative-mode-governance.md)) относится к приёмке\n"
    "изменений репозитория и к решению на гейте не применяется. Понятие\n"
    "«gate» соответствует gateway/точке решения процессной нотации OMG BPMN 2.0."
)

# (файл, старая строка, новая строка)
REPLACEMENTS: list[tuple[str, str, str]] = [
    # --- Стандарт процесса BCREQ ---
    ("standards/bcreq-process-standard.md",
     "| **human gate G1**: структура уровней согласована |",
     "| **ключевой гейт G1** (`человек`): структура уровней согласована |"),
    ("standards/bcreq-process-standard.md",
     "| **human gate G2**: high/compliance-риски имеют owner-review |",
     "| **ключевой гейт G2** (`человек`): high/compliance-риски имеют owner-review |"),
    ("standards/bcreq-process-standard.md",
     "| **human gate G3**: Пользователь утверждает |",
     "| **ключевой гейт G3** (`человек`): Пользователь утверждает |"),
    ("standards/bcreq-process-standard.md",
     "  подпроцессы, несущие human gate (П2, П5, П6).",
     "  подпроцессы, несущие ключевой гейт `человек` (П2, П5, П6)."),
    ("standards/bcreq-process-standard.md",
     "> разместить 3 обязательных human gate (структура, риск, утверждение). Верхняя",
     "> разместить 3 обязательных ключевых гейта `человек` (структура, риск,\n"
     "> утверждение). Верхняя"),
    ("standards/bcreq-process-standard.md",
     "Gate'ы привязаны к операциям с исполнителем `человек`\n"
     "([ba-ontology.md §3](ba-ontology.md), С3) и governance-модели «молчание =\n"
     "согласие» ([ADR-0003](../docs/adr/0003-creative-mode-governance.md)).",
     SILENCE_STD),
    ("standards/bcreq-process-standard.md",
     "- [ ] Human gates G1/G2/G3 пройдены человеком, не LLM (B3).",
     "- [ ] Ключевые гейты G1/G2/G3 (тип `человек`) пройдены человеком, не LLM (B3)."),

    # --- ADR-009 ---
    ("docs/adr/009-bcreq-formation-process.md",
     "# ADR-009: Многоуровневый процесс формирования BCREQ — подпроцессы, human gates, механизм незавершённых подпроцессов",
     "# ADR-009: Многоуровневый процесс формирования BCREQ — подпроцессы, ключевые гейты (`человек`), механизм незавершённых подпроцессов"),
    ("docs/adr/009-bcreq-formation-process.md",
     "BCREQ, где стоят **human gates** и как процесс ведёт себя, когда **часть дерева",
     "BCREQ, где стоят **гейты** (ключевые — тип `человек`) и как процесс ведёт\n"
     "себя, когда **часть дерева"),
    ("docs/adr/009-bcreq-formation-process.md",
     "  обязательных human gate (структура декомпозиции, приёмка рисков, утверждение).",
     "  обязательных ключевых гейта `человек` (структура декомпозиции, приёмка\n"
     "  рисков, утверждение)."),
    ("docs/adr/009-bcreq-formation-process.md",
     "`baselined`, несущий все human gate на различных границах и остающийся далеко",
     "`baselined`, несущий все ключевые гейты `человек` на различных границах и\n"
     "  остающийся далеко"),
    ("docs/adr/009-bcreq-formation-process.md",
     "  (П3 при отсутствии сценариев), но не подпроцессы с human gate (B2).",
     "  (П3 при отсутствии сценариев), но не подпроцессы с ключевым гейтом (B2)."),
    ("docs/adr/009-bcreq-formation-process.md",
     "Три обязательных human gate привязаны к операциям-исполнителям `человек`\n"
     "([ba-ontology.md §3](../../standards/ba-ontology.md), С3) и governance-модели\n"
     "«молчание = согласие» ([ADR-0003](0003-creative-mode-governance.md)). Понятие\n"
     "«gate» соответствует gateway/точке решения процессной нотации OMG BPMN 2.0.",
     SILENCE_ADR009),
    ("docs/adr/009-bcreq-formation-process.md",
     "Правило B3: G1/G2/G3 **НЕ ДОЛЖНЫ** проходиться автоматически LLM; прочие\n"
     "границы — operation gate.",
     "Правило B3: G1/G2/G3 **НЕ ДОЛЖНЫ** проходиться автоматически LLM; прочие\n"
     "границы — operation gate типа `llm` или `гибрид`. Типы гейта и критерии\n"
     "ключевого гейта — [словарь потока BCREQ, раздел 3](../../standards/bcreq-flow-glossary.md#33-типы-гейта)."),
    ("docs/adr/009-bcreq-formation-process.md",
     "**Дерево уровней (результат П2, после human gate G1):**",
     "**Дерево уровней (результат П2, после ключевого гейта G1, `человек`):**"),
    ("docs/adr/009-bcreq-formation-process.md",
     "- Исполняемый, проверяемый многоуровневый процесс с явными human gate на",
     "- Исполняемый, проверяемый многоуровневый процесс с явными ключевыми\n"
     "  гейтами `человек` на"),

    # --- ADR-011, ADR-015, ADR-016, ADR-017 ---
    ("docs/adr/2026-08-adr-011-integration-task-artifacts.md",
     "| Human Gate | Ревьюер подтверждает выборку вердиктов | **Нет** |",
     "| Human Gate (тип `человек`) | Ревьюер подтверждает выборку вердиктов | **Нет** |"),
    ("docs/adr/2026-08-adr-011-integration-task-artifacts.md",
     "*О Human Gate.* Гейт не блокирует прогон:",
     "*О Human Gate.* Тип гейта — `человек` ([словарь потока BCREQ, раздел\n"
     "3.3](../../standards/bcreq-flow-glossary.md#33-типы-гейта)). Гейт не блокирует прогон:"),
    ("docs/adr/2026-10-adr-015-bcreq-manual-classes.md",
     "модели. Существующие промпты, восемь мета-стандартов, runtime и human gates\n"
     "сохраняются.",
     "модели. Существующие промпты, восемь мета-стандартов, runtime и гейты с\n"
     "решением человека (`человек`, `гибрид`) сохраняются."),
    ("docs/adr/2026-10-adr-016-ide-client-process.md",
     "и скрытая память способны обойти сохранение требований и human gates.",
     "и скрытая память способны обойти сохранение требований и гейты с решением\n"
     "человека (`человек`, `гибрид`)."),
    ("docs/adr/2026-10-adr-017-four-stages-n8n-orchestration.md",
     "шаги, хранит состояние исполнения, ждёт решения человека на гейтах и\n"
     "   вызывает модели.",
     "шаги, хранит состояние исполнения, ждёт решения человека на гейтах\n"
     "   `человек` и `гибрид` и вызывает модели."),
    ("docs/adr/2026-10-adr-017-four-stages-n8n-orchestration.md",
     "| Человек в цикле | Гейт — узел ожидания решения человека (форма или Wait).",
     "| Человек в цикле | Гейт `человек` или `гибрид` — узел ожидания решения человека (форма или Wait); машинных гейтов этот ADR не вводит: перевод — решение владельца (BL-161)."),

    # --- governance и экосистема ---
    ("ai-governance/ai-governance.md",
     "| Human-in-the-loop gate | Явное подтверждение человеком перед сменой статуса артефакта. |",
     "| Human-in-the-loop gate | Явное подтверждение человеком перед сменой статуса артефакта. Тип гейта — `человек` или `гибрид` ([словарь потока BCREQ, раздел 3.3](../standards/bcreq-flow-glossary.md#33-типы-гейта)); `llm` и `код` — машинные проверки, не этот механизм. |"),
    ("ai-governance/ai-governance.md",
     "| Human-in-the-loop gate | **Есть.** Смена статусов `draft → canonical` и merge PR — решение человека. |",
     "| Human-in-the-loop gate | **Есть.** Смена статусов `draft → canonical` и merge PR — решение человека (тип `человек`). |"),
    ("docs/ba-ecosystem.md",
     "| Human-in-the-loop gate | Подтверждение человеком перед сменой статуса (`covered / validated / approved / released`). |",
     "| Human-in-the-loop gate | Подтверждение человеком перед сменой статуса (`covered / validated / approved / released`). Тип гейта — `человек` или `гибрид` ([словарь потока BCREQ, раздел 3.3](../standards/bcreq-flow-glossary.md#33-типы-гейта)). |"),
    ("docs/architecture.md",
     "| Гейты | Решение БА в чате | Остановка агента, решение БА | Узел ожидания решения человека |",
     "| Гейты `человек` и `гибрид` | Решение БА в чате | Остановка агента, решение БА | Узел ожидания решения человека |"),

    # --- Стратегия, видение, дорожная карта ---
    ("docs/rfc/2026-10-ba-automation-strategy.md",
     "а процесс, правила и решения человека остаются прежними.",
     "а процесс, правила и решения человека на ключевых гейтах остаются прежними."),
    ("docs/rfc/2026-10-ba-automation-strategy.md",
     "базы знаний продукта или решения человека. Решения на гейтах принимают\n"
     "люди.",
     "базы знаний продукта или решения человека. Решения на ключевых гейтах\n"
     "принимают люди; тип остальных гейтов — по словарю потока BCREQ."),
    ("docs/rfc/2026-10-ba-automation-strategy.md",
     "| Гейты | Решение БА в чате | Остановка агента, решение БА | Узел ожидания и веб-интерфейс гейтов |",
     "| Гейты `человек` и `гибрид` | Решение БА в чате | Остановка агента, решение БА | Узел ожидания и веб-интерфейс гейтов |"),
    ("docs/rfc/2026-10-ba-automation-strategy.md",
     "  - есть узел ожидания решения человека.",
     "  - есть узел ожидания решения человека на гейтах `человек` и `гибрид`."),
    ("docs/rfc/2026-10-ba-automation-strategy.md",
     "запускают шаги, хранят состояние, вызывают модель, ждут решения человека.",
     "запускают шаги, хранят состояние, вызывают модель, ждут решения человека на гейтах `человек` и `гибрид`."),
    ("docs/rfc/2026-10-ba-automation-strategy.md",
     "процесс возобновляется без двойных решений, гейт ждёт решения человека.",
     "процесс возобновляется без двойных решений, гейт `человек` или `гибрид` ждёт решения человека."),
    ("docs/rfc/2026-10-ba-automation-strategy.md",
     "| Решение человека на каждом гейте и неизменная статистика `runs/` |",
     "| Решение человека на каждом гейте `человек`/`гибрид` (ключевые — всегда `человек`; перевод остальных — решение владельца, BL-161) и неизменная статистика `runs/` |"),
    ("docs/vision.md",
     "сервер. Шаги процесса, правила и решения человека при этом остаются\n"
     "прежними.",
     "сервер. Шаги процесса, правила и решения человека на ключевых гейтах при\n"
     "этом остаются прежними."),
    ("docs/roadmap.md",
     "вызывает модель, ждёт решения человека на гейтах и подключает почту и трекер.",
     "вызывает модель, ждёт решения человека на гейтах `человек` и `гибрид` и подключает почту и трекер."),
    # docs/rfc/2026-10-standards-page.md не правим: строка этапа 3 лежит
    # в приложении, которое порождает experiments/issue_420/site-v2/build.py
    # (валидатор #420 сверяет его побайтно), см. исключение в валидаторе #433.

    # --- Контракт гейтов, RFC потока, бэклог ---
    ("docs/contracts/bcreq-stage-gates.md",
     "  и выдаёт рекомендацию «стадия · шаг · причина»; возврат выполняется после\n"
     "  решения человека (B3).",
     "  и выдаёт рекомендацию «стадия · шаг · причина»; возврат выполняется после\n"
     "  решения человека на гейте (`человек` или `гибрид`, B3)."),
    ("docs/rfc/2026-11-bcreq-flow-processes-prompts.md",
     "ждёт решения человека во внешнем интерфейсе. Модель от этого не меняется.",
     "ждёт решения человека (гейт `человек` или `гибрид`) во внешнем интерфейсе.\n"
     "Модель от этого не меняется."),
    ("docs/rfc/2026-11-bcreq-flow-processes-prompts.md",
     "контракт состояния, стоп-краны, receipt, человеческие гейты, порядок источников,",
     "контракт состояния, стоп-краны, receipt, гейты с решением человека (`человек`, `гибрид`), порядок источников,"),
    ("pr-ops/backlog-ba-model.md",
     "часть 39 стандартов классов (контракт состояния, стоп-краны, receipt,\n"
     "человеческие гейты, порядок источников, правило ссылок на runtime и\n"
     "заглушек).",
     "часть 39 стандартов классов (контракт состояния, стоп-краны, receipt,\n"
     "гейты с решением человека (`человек`, `гибрид`), порядок источников,\n"
     "правило ссылок на runtime и заглушек). Тип гейта обязателен с первой\n"
     "редакции (BL-159)."),

    # --- Архитектура промптов ---
    ("standards/bcreq-prompt-architecture.md",
     "| Пересекает человеческий гейт Согласование 1 (B3);",
     "| Пересекает ключевой гейт `человек` Согласование 1 (B3);"),

    # --- К-33: стоп выпуска ---
    ("standards/bcreq-manual-classes/catalog.json",
     "выпуск заблокирован до исправления и решения человека.\"",
     "выпуск заблокирован до исправления и решения человека на гейте выпуска (`человек`).\""),
    ("standards/bcreq-manual-classes/33-release-audit.md",
     "выпуск заблокирован до исправления и решения человека.",
     "выпуск заблокирован до исправления и решения человека на гейте выпуска (`человек`)."),
    ("docs/ba-processes/bcreq-manual-process.md",
     "выпуск заблокирован до исправления и решения человека;",
     "выпуск заблокирован до исправления и решения человека на гейте выпуска (`человек`);"),
]

# Файлы, у которых поднимается версия: (старая, новая).
VERSIONS: dict[str, tuple[str, str]] = {
    "standards/bcreq-process-standard.md": ("0.1.1", "0.1.2"),
    "docs/adr/009-bcreq-formation-process.md": ("0.1", "0.1.1"),
    "docs/adr/2026-08-adr-011-integration-task-artifacts.md": ("0.1", "0.1.1"),
    "docs/adr/2026-10-adr-015-bcreq-manual-classes.md": ("0.1", "0.1.1"),
    "docs/adr/2026-10-adr-016-ide-client-process.md": ("0.1", "0.1.1"),
    "docs/adr/2026-10-adr-017-four-stages-n8n-orchestration.md": ("1.0", "1.0.1"),
    "ai-governance/ai-governance.md": ("0.8", "0.8.1"),
    "docs/ba-ecosystem.md": ("0.4", "0.4.1"),
    "docs/architecture.md": ("1.0", "1.0.1"),
    "docs/rfc/2026-10-ba-automation-strategy.md": ("0.2", "0.2.1"),
    "docs/vision.md": ("1.0", "1.0.1"),
    "docs/roadmap.md": ("1.0", "1.0.1"),
    "docs/rfc/2026-11-bcreq-flow-processes-prompts.md": ("0.4", "0.4.1"),
    "standards/bcreq-prompt-architecture.md": ("0.1", "0.1.1"),
    "docs/ba-processes/00-index.md": ("0.2", "0.2.1"),
}

# Карта процессов: тип гейта строки = исполнитель операции (онтология, С3).
EXECUTOR = {
    "ingestion": "llm", "understanding": "гибрид", "validation": "гибрид",
    "modeling": "llm", "solution_design": "гибрид", "documentation": "llm",
    "quality": "гибрид", "research": "гибрид", "governance": "человек",
    "impact_analysis": "гибрид", "reverse_requirements": "гибрид",
    "risk_analysis": "человек", "release_readiness": "человек",
}
STRICT = ["человек", "гибрид", "llm"]
INDEX_NOTE = (
    "Колонка «Gate / gap»: тип гейта (`человек`, `гибрид`, `llm`, `код`) равен\n"
    "исполнителю операции строки ([онтология БА, раздел 3](../../standards/ba-ontology.md),\n"
    "С3; [словарь потока BCREQ, раздел 3.3](../../standards/bcreq-flow-glossary.md#33-типы-гейта)).\n"
    "Ключевые гейты процесса BCREQ — G1/G2/G3\n"
    "([стандарт процесса, раздел 3](../../standards/bcreq-process-standard.md#3-human-gates-в-ключевых-точках));\n"
    "перевод гейта в другой тип — решение владельца (BL-161).\n"
)


def bump_frontmatter(text: str, old: str, new: str) -> str:
    head, sep, body = text.partition("\n---\n")
    if f"\nversion: {new}\n" in head + "\n":
        return text
    assert f"\nversion: {old}\n" in head + "\n", f"version {old} not found"
    head = head.replace(f"\nversion: {old}", f"\nversion: {new}", 1)
    head = re.sub(r"\nupdated: [0-9-]+", f"\nupdated: {TODAY}", head, count=1)
    return head + sep + body


def type_index(text: str) -> str:
    out = []
    for line in text.split("\n"):
        cells = line.split("|")
        if line.startswith("| ") and len(cells) >= 7 and cells[-2].strip().startswith("Gate:"):
            ops = re.findall(r"`([a-z_]+)`", cells[2])
            types = [EXECUTOR[o] for o in ops if o in EXECUTOR]
            assert types, line
            gtype = min(types, key=STRICT.index)
            cells[-2] = cells[-2].replace("Gate:", f"Gate (`{gtype}`):", 1)
            line = "|".join(cells)
        out.append(line)
    text = "\n".join(out)
    anchor = "## Known gaps"
    if INDEX_NOTE not in text:
        # Примечание — перед первой таблицей шагов процесса.
        first = text.index("| Шаг | Операция | Что получить | Промпты | Gate / gap |")
        text = text[:first] + INDEX_NOTE + "\n" + text[first:]
    assert anchor in text
    return text


def main() -> int:
    errors = []
    touched: dict[str, str] = {}
    for rel, old, new in REPLACEMENTS:
        text = touched.get(rel) or (ROOT / rel).read_text(encoding="utf-8")
        if new in text:
            touched[rel] = text
            continue
        if old not in text:
            errors.append(f"{rel}: not found: {old[:80]!r}")
            continue
        text = text.replace(old, new)
        touched[rel] = text
    rel = "docs/ba-processes/00-index.md"
    touched[rel] = type_index(touched.get(rel) or (ROOT / rel).read_text(encoding="utf-8"))
    if errors:
        print("\n".join(errors))
        return 1
    for rel, text in touched.items():
        if rel in VERSIONS:
            original = (ROOT / rel).read_text(encoding="utf-8")
            if text != original:
                text = bump_frontmatter(text, *VERSIONS[rel])
        if text != (ROOT / rel).read_text(encoding="utf-8"):
            (ROOT / rel).write_text(text, encoding="utf-8")
            print("updated", rel)
    return 0


if __name__ == "__main__":
    sys.exit(main())
