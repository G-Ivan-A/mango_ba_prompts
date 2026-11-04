"""Apply owner decision Р-17 (PR #437 comment): 74 portal nodes review -> accepted.

Updates RFC-RT-001, BACKLOG Р-17 and the issue-434 validator. Idempotent asserts:
each replaced fragment must exist exactly as written.
"""
U = "https://github.com/G-Ivan-A/mango_ba_prompts/pull/437#issuecomment-6605372609"


def ed(p, pairs):
    s = open(p, encoding="utf-8").read()
    for a, b in pairs:
        assert a in s, (p, a)
        s = s.replace(a, b)
    open(p, "w", encoding="utf-8").write(s)


R = "docs/rfc/2026-11-runtime-product-catalog-golden-set.md"
ed(R, [
    ("""6. **Решение владельца Р-17.** Принять каталог 2026-10-28.1 (статус
   `review`) целиком как таксономию runtime с сохранением `lifecycle`.
   Без этого решения половина функций контакт-центра (33 из 66) остаётся
   вне каталога.""",
     f"""6. **Решение владельца Р-17 принято** ([комментарий владельца]({U}),
   2026-11-03). 74 узла с портала переведены из `added-for-review` в
   `lifecycle: accepted`, каталог 2026-10-28.1 получил `status: accepted`.
   Условие по таксономии для запуска РТ-1 в runtime выполнено."""),
    ("из них `retained` / `added-for-review` |", "из них `retained` / `accepted` |"),
    ("74 добавлены с портала со статусом `review` (Р-17)",
     "74 добавлены с портала и приняты владельцем (`accepted`, Р-17)"),
    ("""5. Узел с `lifecycle: added-for-review` используй, но пометь «функция на
   ревью каталога».""",
     """5. Узлы с `lifecycle: retained` и `lifecycle: accepted` равноправны:
   оба утверждены владельцем (Р-17)."""),
    ("каталог 2026-10-28.1 переносится целиком, `lifecycle` сохраняется;",
     "каталог 2026-10-28.1 (`status: accepted`) переносится целиком, `lifecycle` сохраняется, 74 узла с портала приняты (`accepted`);"),
    ("| Р-17 | Принять каталог `docs/taxonomy/products.json` 2026-10-28.1 (статус `review`) целиком как таксономию runtime, с `lifecycle` и разрешением привязки к `added-for-review` | [BACKLOG, раздел 2](../../pr-ops/BACKLOG.md) | ждёт |",
     f"| Р-17 | Принять каталог `docs/taxonomy/products.json` 2026-10-28.1 целиком как таксономию runtime; 74 узла с портала — из `added-for-review` в `accepted` | [BACKLOG, раздел 2](../../pr-ops/BACKLOG.md), [комментарий владельца]({U}) | принято 2026-11-03 |"),
    ("""Почему Р-17, а не молчаливый перенос:

- каталог в статусе `review`;
- у класса `contact-center` 33 из 66 функций — `added-for-review`;""",
     """Почему Р-17 понадобилось (до решения 2026-11-03):

- каталог был в статусе `review`;
- у класса `contact-center` 33 из 66 функций были `added-for-review`;"""),
    ("""Это выбор владельца. Рекомендация — перенос целиком с полем `lifecycle`,
чтобы промпт помечал ревью-узлы (раздел 4, шаг 5).""",
     """Владелец выбрал перенос целиком и принял 74 узла с портала
(`lifecycle: accepted`, каталог `status: accepted`)."""),
])
ed("pr-ops/BACKLOG.md", [(
    "(статус `review`) целиком как таксономию runtime | Принять целиком с полем `lifecycle`; привязка к узлам `added-for-review` разрешена с пометкой в выходе; РТ-1 и РТ-3 владелец создаёт в runtime | BL-163 | ждёт |",
    f"целиком как таксономию runtime | Принято 2026-11-03 ([комментарий владельца]({U})): 74 узла с портала переведены из `added-for-review` в `accepted`, каталог `status: accepted`; условие по таксономии для РТ-1 выполнено; РТ-1 и РТ-3 владелец создаёт в runtime | BL-163 | принято |",
)])
ed("scripts/validate_issue_434_runtime_tasks.py", [
    ('self.assertIn("added-for-review", sample)', 'self.assertIn("lifecycle: accepted", sample)'),
    ("{life['added-for-review']} |", "{life['accepted']} |"),
])
