#!/usr/bin/env python3
"""Тесты правил шаблонов задач `runs` (issue #323) на синтетике.

Валидатор `validate_issue_323_issue_forms.py` проверяет реальные шаблоны — и
молчит, если оба файла корректны. Эти тесты проверяют сами правила: что
валидатор действительно падает на нарушениях (жёсткий dropdown вместо
свободного текста, textarea без placeholder, потерянное поле, битый YAML), и
что встроенный парсер YAML разбирает конструкции Issue Forms так же, как
PyYAML.

Запуск: ``python3 scripts/test_issue_323_issue_forms.py``
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from validate_issue_323_issue_forms import (  # noqa: E402
    EXPECTED,
    check_text,
    parse_yaml,
)

SPEC = {"labels": {"runs", "execution"}, "ids": {"process_description"}}

VALID = """\
name: "Прогон"
description: "Описание"
labels:
  - "runs"
  - "execution"
body:
  - type: markdown
    attributes:
      value: |
        Вступление.
  - type: textarea
    id: process_description
    attributes:
      label: "Процесс"
      placeholder: "Указывается вручную"
    validations:
      required: true
"""


def errors_for(text: str, spec: dict = SPEC) -> list[str]:
    return check_text(Path("synthetic.yml"), text, spec)


class TemplateRulesTest(unittest.TestCase):
    def test_valid_template_passes(self) -> None:
        self.assertEqual(errors_for(VALID), [])

    def test_freeform_field_as_dropdown_fails(self) -> None:
        broken = VALID.replace("  - type: textarea", "  - type: dropdown").replace(
            '      placeholder: "Указывается вручную"',
            '      options:\n        - "Разработка ФТ"\n        - "Разработка ТЗ"',
        )
        self.assertTrue(any("textarea" in e for e in errors_for(broken)))

    def test_textarea_without_placeholder_fails(self) -> None:
        broken = VALID.replace('      placeholder: "Указывается вручную"\n', "")
        self.assertTrue(any("placeholder" in e for e in errors_for(broken)))

    def test_missing_required_field_fails(self) -> None:
        broken = VALID.replace("    id: process_description\n", "    id: other\n")
        self.assertTrue(any("обязательные поля" in e for e in errors_for(broken)))

    def test_missing_label_fails(self) -> None:
        broken = VALID.replace('  - "execution"\n', "")
        self.assertTrue(any("метки" in e for e in errors_for(broken)))

    def test_duplicate_id_fails(self) -> None:
        broken = VALID + (
            "  - type: input\n    id: process_description\n"
            '    attributes:\n      label: "Дубль"\n'
        )
        self.assertTrue(any("дублирующийся" in e for e in errors_for(broken)))

    def test_unknown_block_type_fails(self) -> None:
        broken = VALID.replace("  - type: markdown", "  - type: slider")
        self.assertTrue(any("недопустимый type" in e for e in errors_for(broken)))

    def test_broken_indentation_fails(self) -> None:
        broken = VALID.replace('      label: "Процесс"', '     label: "Процесс"')
        self.assertTrue(errors_for(broken))


class ParserTest(unittest.TestCase):
    def test_matches_pyyaml_on_real_templates(self) -> None:
        try:
            import yaml
        except ImportError:
            self.skipTest("PyYAML недоступен")
        directory = Path(__file__).resolve().parents[1] / ".github" / "ISSUE_TEMPLATE"
        for name in EXPECTED:
            text = (directory / name).read_text(encoding="utf-8")
            self.assertEqual(parse_yaml(text), yaml.safe_load(text), name)

    def test_block_scalar_and_nested_lists(self) -> None:
        parsed = parse_yaml(VALID)
        self.assertEqual(parsed["labels"], ["runs", "execution"])
        self.assertEqual(parsed["body"][0]["attributes"]["value"], "Вступление.\n")
        self.assertIs(parsed["body"][1]["validations"]["required"], True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
