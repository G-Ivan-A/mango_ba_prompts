"""Round-7 edits to content.json (issue #420): answers round-6 focus-group remarks
(transitional 2.4.2/6.2 rule stated once in card 6, what the customer sees of a term
divergence, when work starts relative to the customer's signature). The abbreviation
list is rendered expanded by build.py from this round on.
Kept for traceability; run once: python3 experiments/issue_420/prototype/edit_round7.py"""
import json, pathlib
p = pathlib.Path(__file__).with_name("content.json")
c = json.loads(p.read_text())
top = next(v for v in c.values() if isinstance(v, dict) and "summary" in v)
for item in top["customer"]:
    if item[0] == "Сколько времени":
        item[1] = ("Вы участвуете в трёх точках: вопросы, подпись требований, утверждение решения. "
            "Срок ответа в каждой точке БА согласует с вами при запуске задачи; единого срока стандарт пока не задаёт (открытый вопрос RFC-420). "
            "Пока вы не подписали требования, решение не готовят; пока вы не утвердили решение, его не передают в разработку.")
for a in c["intro"]["audiences"]:
    if a["who"] == "Разработка и архитектор":
        a["reads"] = a["reads"].replace("После Г-W разработка работает",
            "После Г-W и утверждения Заказчиком (его отказ возвращает документ на уточнение) разработка работает")
for card in c["cards"]:
    if card["n"] == "1":
        for x in card["composition"]:
            if x["title"].startswith("Расхождение"):
                x["text"] = ("блок после таблицы — только если найдены расхождения С1–С3: рекомендация с классом расхождения; "
                    "менять ли термин, решает БА и записывает решение в журнал 8.5. Блок остаётся в разделе 1, "
                    "поэтому Заказчик видит его, когда подписывает разделы 1–4.")
    if card["n"] == "2":
        card["special"]["lead"] = card["special"]["lead"].replace(
            "Переходное правило для документов, начатых до этого правила, — в стандарте раздела 6.",
            "Исключение для документов, начатых по старой структуре, — в карточке раздела 6.")
    if card["n"] == "6":
        card["special"]["lead"] = card["special"]["lead"].replace(
            "Переходное правило для документов, начатых до этого правила, — в стандарте раздела 6.",
            "Исключение: в документах, начатых по старой структуре, ограничение платформы по решению БА остаётся в 6.2, а в 2.4.2 ставят ссылку «см. 6.2».")
p.write_text(json.dumps(c, ensure_ascii=False, indent=2) + "\n")
