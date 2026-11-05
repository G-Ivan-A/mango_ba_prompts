#!/usr/bin/env python3
"""Issue #464: composition, sections README, source register. One-shot, not idempotent."""
from pathlib import Path
def sub(path, pairs):
    p = Path(path); t = p.read_text()
    for a, b in pairs:
        assert a in t, f"{path}: нет фрагмента: {a[:70]}"
        t = t.replace(a, b, 1)
    p.write_text(t)

sub("standards/bcreq-composition-standard.md", [
("| ODA-3 | Явный выбор БА для сравнительного прогона (тестирование стандарта как замещающего). | Прогон «arc42 + C4» против «ODA» на одной задаче. |",
 "| ODA-3 | Явный выбор БА на шаге Ш-А: для этой задачи или для сравнительного прогона. | БА считает модель ODA понятнее для задачи; прогон «C4» против «ODA» на одной задаче. |"),
("""**Что заменяется:** только L2 раздела 5 — компоненты ODA и TMF Open API вместо
C4 L2 и собственной дельты OpenAPI. Словарь D9 подключается к сверке
глоссария. **Что не заменяется:** разделы 1–4, 6–8 и L1 раздела 5.""",
"""**Что заменяется (issue #464):** структура раздела 5. L1 строится по функциональным
блокам ODA, L2 — по компонентам ODA и TMF Open API вместо C4 L2 и собственной дельты
OpenAPI. Правила вывода структуры — в
[индустриальных стандартах](bcreq-industry-practice.md#3-раздел-5-выбор-между-c4-и-tm-forum-oda).
Словарь D9 подключается к сверке глоссария. **Что не заменяется:** разделы 1–4 и 6–8.
Нумерация раздела 5 не зависит от номеров ФТ при любом стандарте."""),
("- [ ] TM Forum ODA применён только при ODA-1…ODA-3 и только к L2; выбор записан в 8.5.",
 "- [ ] TM Forum ODA применён только при ODA-1…ODA-3 и только к разделу 5; выбор записан в 8.5."),
])

sub("standards/bcreq-sections/README.md", [
("2.4 Границы, ＋2.5 Продукты и стейкхолдеры |", "2.4 Границы, 2.5 Продукты и стейкхолдеры |"),
("""> ФТ нумеруются ФТ-01, ФТ-02 … и формулируются по BABOK; пункты раздела 5 —
> «5.N Название (ФТ-01, ФТ-02)»; НФТ — 4.1, 4.2 …, одно НФТ — один пункт.""",
"""> ФТ нумеруются ФТ-01, ФТ-02 … и формулируются по BABOK; НФТ — 4.1, 4.2 …, одно НФТ —
> один пункт. Пункты раздела 5 — «5.х Название (ФТ-01, ФТ-03)»: структуру задаёт
> выбранный стандарт, скобки показывают покрытие, номера ФТ нумерацию не определяют
> (уточнение issue #464, [стандарт раздела 5](05-solution-description.md#структура-по-стандарту-а-не-по-фт))."""),
])

sub("standards/industry-standards-standard.md", [
("## Критерии соответствия (DoD)", """### 3.2. Дополнение по issue #464 (индустриальные стандарты на странице «Стандарты»)

> Добавлено по правилу И6 через issue #464. Проверка 2026-11-05. `tmforum.org` отвечает
> 403 автоматическим запросам, состав блоков ODA сверен по вторичному источнику.
> BABOK v3 платный: номера пунктов сверены по вторичным учебным материалам.
> Применение — в [индустриальных стандартах BCREQ](bcreq-industry-practice.md).

| Источник | Tier | Норм/Инф | Сверенный URL | Где применяется (issue #464) |
| --- | --- | --- | --- | --- |
| IREB, M. Glinz, A Glossary of Requirements Engineering Terminology, v2.1.0 | framework/best practice | информативный | <https://cpre.ireb.org/en/downloads-and-resources/glossary> · <https://gasq.org/files/content/gasq/downloads/certification/IREB/ireb_cpre_glossary_en_2.1.pdf> | отраслевой словарь по умолчанию, раздел 1 |
| C4 model: System Context, abstractions | de facto | информативный | <https://c4model.com/diagrams/system-context> · <https://c4model.com/abstractions> | структура раздела 5 по умолчанию |
| TM Forum ODA: components, GB1022 | de facto | информативный | <https://www.tmforum.org/oda/implementation/components-canvas/> (403) · <https://tmforum.org/resources/standard/gb1022-oda-functional-architecture-guidebook-v1-1-0> (403) | структура раздела 5 по выбору БА |
| GÉANT, SURFnet OAV Architecture Analysis (вторичный источник блоков ODA) | best practice | информативный | <https://resources.geant.org/wp-content/uploads/2022/02/GN4-3_White-Paper_SURFnet-OAV-Architecture-Analysis.pdf> | сверка блоков ODA |

## Критерии соответствия (DoD)"""),
("version: 0.2\nupdated: 2026-10-23", "version: 0.3\nupdated: 2026-11-05"),
])
