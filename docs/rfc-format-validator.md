---
status: draft
version: 0.1
updated: 2026-06-26
ai-generated: true
---

# Валидатор формата RFC

Документ описывает проверку из Issue #248: RFC, созданный по
[`governance/rfc-generation-contract.md`](../governance/rfc-generation-contract.md),
должен быть читаемым Markdown + YAML frontmatter документом, а не YAML-heavy
контрактом.

## Что проверяется

[`scripts/validate_rfc_format.py`](../scripts/validate_rfc_format.py)
проверяет contract-style RFC:

- frontmatter содержит поля `id`, `status`, `title`, `author`, `created`,
  `updated`, `layer`, `type`, `related_contracts`, `target_artifacts` в порядке
  из контракта;
- `id` имеет формат `RFC-NNN`, `layer: L3`, `type: rfc`, а
  `related_contracts` содержит `governance/rfc-generation-contract.md`;
- тело содержит разделы `## 1. Context and motivation` ...
  `## 8. Canonical criteria` в правильном порядке;
- разделы начинаются с читаемого Markdown, а не с fenced YAML;
- YAML-блоки не доминируют над текстом и не кодируют `context:`, `problems:`,
  `alternatives:`, `rationale:` как top-level тело RFC;
- problem/proposal/alternative/criteria ID идут без пропусков;
- предложения связаны с проблемами, canonical criteria покрывают все proposals;
- impact явно содержит `requires_adr`, `requires_standard` и
  `target_artifacts`.

## Как запускать

Проверить все contract-style RFC, которые валидатор находит по умолчанию:

```bash
python3 scripts/validate_rfc_format.py
```

Проверить конкретный RFC:

```bash
python3 scripts/validate_rfc_format.py governance/rfc/ba-processes-observability-implementation-proposal.md
```

Посмотреть, какие файлы попадут в default scan:

```bash
python3 scripts/validate_rfc_format.py --list
```

Проверить Markdown из stdin:

```bash
git show cc3b3996:governance/rfc/ba-processes-observability-implementation-proposal.md \
  | python3 scripts/validate_rfc_format.py -
```

Команда выше демонстрирует исходный дефект RFC-243: версия из `cc3b3996`
содержит Markdown-заголовки, но большинство разделов начинается с больших
YAML-блоков, поэтому документ плохо читается человеком.

## Scope default scan

По умолчанию валидатор проверяет только RFC, которые уже выглядят как новые
contract-style RFC: frontmatter содержит `id: RFC-NNN`, `type: rfc` и ссылку на
`governance/rfc-generation-contract.md`.

Старые RFC-like документы без этого frontmatter не мигрируются в рамках issue
#248 и не проверяются автоматически. Их можно проверить явно, передав путь
файла, либо запустить расширенный режим:

```bash
python3 scripts/validate_rfc_format.py --all
```

## CI и regression

GitHub Pages workflow запускает два шага:

- `python3 scripts/validate_rfc_format.py` - reusable validator для актуальных
  RFC;
- `python3 scripts/validate_issue_248_rfc_format.py` - regression check issue
  #248.

Regression check подтверждает два состояния:

- текущий
  [`governance/rfc/ba-processes-observability-implementation-proposal.md`](../governance/rfc/ba-processes-observability-implementation-proposal.md)
  проходит reusable validator;
- историческая YAML-heavy версия RFC-243 из `cc3b3996` отклоняется именно по
  признакам нарушения читабельного Markdown-формата.
