"""Issue #466 overlay for the reproducible #423 → #464 site source pipeline.

Only wraps the existing BCREQ and industry content; their approved text stays
owned by issue_464/site_standards.py. This module owns the proposed TTZ view.
"""
from __future__ import annotations

REPO = "https://github.com/G-Ivan-A/mango_ba_prompts/blob/main"
RFC = f"{REPO}/docs/rfc/2026-11-ttz-feasibility-flow.md"

TTZ = f'''        <details class="standards-group" id="standards-ttz">
          <summary><h2>ТТЗ — оценка исполнимости тендерных ТЗ</h2></summary>
          <article class="standard-card v2-card ttz-card" id="standard-ttz" tabindex="-1" aria-labelledby="standard-title-ttz">
            <p class="eyebrow">Проект потока · RFC-TTZ-001 · на рассмотрении</p>
            <h3 id="standard-title-ttz">От внешнего требования к проверяемому решению</h3>
            <p>БА оценивает тендерное ТЗ в его исходных формулировках: что исполнимо сейчас, при каких условиях, что не подтверждено и что требует разработки. Пробный поток подготовлен к рассмотрению; новая оценка ТЗ и автоматизация ещё не проводились.</p>
            <h3>Как проходит оценка</h3>
            <ol class="v2-list">
              <li><strong>Принять ТЗ.</strong> Зафиксировать версию, область оценки, среду и принимающего.</li>
              <li><strong>Разобрать пункты.</strong> Сохранить исходные строки, выделить части составных требований, заголовки и дубли.</li>
              <li><strong>Выбрать маршрут.</strong> Сопоставить внешний термин с одним или несколькими продуктами Mango; различить альтернативы и совместную работу.</li>
              <li><strong>Собрать основания.</strong> Для каждой части — применимый источник, версия, цитата, ограничения. Если подтверждения нет, так и записать.</li>
              <li><strong>Принять оценку.</strong> БА проверяет вывод, спорные пункты и риски; коммерческие и договорные условия передаются их владельцам.</li>
              <li><strong>Собрать отчёт.</strong> Записка, матрица, вопросы, доказательства и статистика из одной версии данных; публикация после решения человека.</li>
            </ol>
            <h3>Что важно в матрице</h3>
            <dl class="v2-composition">
              <div><dt>Продукт и сценарий</dt><dd>Название раздела заказчика не определяет продукт Mango. «Речевая аналитика» может требовать проверки РА, Роботов или их границ; запись и живой диалог — разные режимы.</dd></div>
              <div><dt>Оценка и основание</dt><dd>Да / Частично / Нет / Не подтверждено / б/о. Отсутствие найденной цитаты не доказывает отсутствие функции. Общий API не доказывает наличие готового коннектора.</dd></div>
              <div><dt>Решение БА</dt><dd>Оценка ИИ, итог БА и комментарий хранятся отдельно. Готовность разработать показывается отдельным сценарием.</dd></div>
              <div><dt>Проверенное знание</dt><dd>Повтор комментария не делает его правилом. Для эталонного случая нужны независимое первичное основание и явное подтверждение вторым компетентным человеком.</dd></div>
            </dl>
            <h3>Следующий шаг</h3>
            <p>Рассмотреть проект, затем провести ручную пробу с БА. Автоматизацию планируем по результатам: агентный маршрут → n8n → серверный поток при подтверждённой потребности.</p>
            <p class="standard-sources"><a href="{RFC}" target="_blank" rel="noreferrer">Подробный RFC: постановка, восемь RUN, практика БА, мета-модель и план</a> · <a href="{REPO}/pr-ops/BACKLOG.md#поток-ттз-issue-466" target="_blank" rel="noreferrer">Бэклог ТТЗ и статусы</a></p>
          </article>
        </details>
'''

INDUSTRY_TTZ = '''          <div class="standard-card v2-card ttz-card">
            <h3>Для тендерных ТЗ</h3>
            <p>Внешняя классификация и каталог Mango сопоставляются отдельно. Одно индустриальное понятие может вести к нескольким продуктам; близкие названия не доказывают равенство функций.</p>
            <ul class="v2-list">
              <li><a href="https://www.w3.org/TR/skos-reference/#mapping" target="_blank" rel="noreferrer">W3C SKOS</a> — различать точное, близкое, широкое и узкое соответствие.</li>
              <li><a href="https://www.tmforum.org/oda/information-systems/information-framework-sid/" target="_blank" rel="noreferrer">TM Forum SID</a> — общий язык отрасли для сопоставления.</li>
              <li><a href="https://doi.org/10.6028/NIST.AI.100-1" target="_blank" rel="noreferrer">NIST AI RMF</a> — независимая проверка, документированные тесты и границы применения ИИ.</li>
            </ul>
          </div>
'''


def apply(html: str) -> str:
    start = html.index('      <section class="page-band standards-band"')
    end = html.index('      <section class="page-band v2-glossary-band"', start)
    original = html[start:end]
    industry_start = original.index('            <section class="standard-card v2-card standards-industry"')
    industry_end = original.index('</section>', industry_start) + len('</section>')
    industry = original[industry_start:industry_end]
    bcreq = original[:industry_start] + original[industry_end:]
    layout = bcreq[bcreq.index('        <div class="standards-layout">'):bcreq.rindex('      </section>')]
    layout = layout.replace('id="standard-intro"', 'id="standard-intro" tabindex="-1"')
    replacement = '''      <section class="page-band standards-band" id="standards" data-page="standards" aria-labelledby="standards-title" hidden>
        <div class="standards-intro">
          <h1 id="standards-title">Стандарты</h1>
          <p class="standards-lead">Выберите направление: бизнес-спецификация BCREQ, проект оценки тендерных ТЗ или индустриальная практика. Каждый подраздел раскрывается отдельно.</p>
        </div>
        <details class="standards-group" id="standards-bcreq">
          <summary><h2>BCREQ — стандарт бизнес-спецификации на доработку системы</h2></summary>
          <p class="standards-group-lead">Структура документа из восьми разделов: назначение, состав, правила написания и критерии приёмки.</p>
''' + layout + '        </details>\n' + TTZ + '''        <details class="standards-group" id="standards-industry">
          <summary><h2>Индустриальные стандарты</h2></summary>
''' + industry + '\n' + INDUSTRY_TTZ + '        </details>\n      </section>\n\n'
    return html[:start] + replacement + html[end:]


def app_js_patches(patches: list[tuple[str, str]]) -> list[tuple[str, str]]:
    # Keep the earlier generator's replacement recognisable on reruns.
    return [(old, new.replace('/^[0-9]$/', '/^(?:[0-9]|ttz)$/')
             .replace('9: "standard-industry"', '9: "standard-industry", ttz: "standard-ttz"'))
            for old, new in patches] + [(
                '      const target = document.getElementById(ids[section] || `standard-${section}`);\n'
                '      target.focus({ preventScroll: true });\n'
                '      target.scrollIntoView({ behavior: "instant", block: "start" });',
                '      const target = document.getElementById(ids[section] || `standard-${section}`);\n'
                '      if (target) {\n'
                '        for (let ancestor = target.parentElement; ancestor; ancestor = ancestor.parentElement) {\n'
                '          if (ancestor.tagName === "DETAILS") ancestor.open = true;\n'
                '        }\n'
                '        target.focus({ preventScroll: true });\n'
                '        target.scrollIntoView({ behavior: "instant", block: "start" });\n'
                '      }',
            )]


def prepare_app(js: str) -> str:
    """Accept the already-published #464 route as input as well as #423."""
    return js.replace('/^[0-9]$/', '/^(?:[0-9]|ttz)$/').replace(
        '9: "standard-industry" };', '9: "standard-industry", ttz: "standard-ttz" };')
