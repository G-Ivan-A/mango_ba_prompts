#!/usr/bin/env python3
"""Генератор представительного PDF-фикстуры «Контакт-центр MANGO OFFICE».

Зачем это нужно. Реальный файл ``CC_manual_1.26.23.pdf`` из issue #111 **не
загрузился** (в теле issue стоит маркер ``<!-- Failed to upload ... -->``), а
комментариев с файлом нет. Чтобы провести воспроизводимый сквозной эксперимент
извлечения (текст → разделы → изображения → токены) с **реальными измеримыми**
числами, а не абстракциями, мы генерируем синтетический PDF, структурно
повторяющий реальное руководство КЦ.

Структура и факты взяты из уже зафиксированной в репозитории выжимки As-Is по
двум руководствам (issue #109):
``docs/ba-process/multichannel-agent-workload/inputs/kb-files.md`` — нумерация
разделов (§1 Введение, §2 Рабочее место, §4 Обработка обращений, …), таблица
ролей, диаграмма маршрутизации. Это синтетический стенд-ин, НЕ сам документ
вендора (никаких проблем с лицензией), но методология извлечения проверяется на
нём один-в-один.

Когда пользователь положит реальный ``CC_manual_1.26.23.pdf`` в
``kb/sources/contact-center-manual/`` и запустит тот же ``scripts/kb/extract.py``,
конвейер даст ``kb/processed/contact-center-manual/`` тем же способом.

Запуск::

    python3 scripts/kb/make_sample_pdf.py [output.pdf]

По умолчанию пишет в
``kb/sources/contact-center-manual-sample/CC_manual_sample.fixture.pdf``.
Текстовое содержание фиксировано в коде → извлечение из фикстуры воспроизводимо.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT = (
    ROOT
    / "kb"
    / "sources"
    / "contact-center-manual-sample"
    / "CC_manual_sample.fixture.pdf"
)

# Детерминированные метаданные PDF (одинаковый текст при каждом запуске).
os.environ.setdefault("SOURCE_DATE_EPOCH", "1700000000")


# Кандидаты TTF с поддержкой кириллицы (иначе текст извлекается как «мусор» —
# дефолтный Helvetica reportlab не несёт ToUnicode-карту для кириллицы).
_FONT_CANDIDATES = [
    (
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    ),
    (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ),
    (
        "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
    ),
    (
        "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
        "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
    ),
]


def _register_font() -> tuple[str, str]:
    """Регистрирует кириллический TTF, возвращает (regular_name, bold_name).

    Без этого pdfplumber извлёк бы кириллицу как «nnnn» — это и есть реальная
    ловушка извлечения PDF, которую конвейер должен обходить (см. отчёт).
    """
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont

    for regular, bold in _FONT_CANDIDATES:
        if Path(regular).exists() and Path(bold).exists():
            pdfmetrics.registerFont(TTFont("KBSans", regular))
            pdfmetrics.registerFont(TTFont("KBSans-Bold", bold))
            return "KBSans", "KBSans-Bold"
    raise RuntimeError(
        "Не найден TTF с кириллицей. Установите шрифты, например:\n"
        "  sudo apt-get install -y fonts-liberation\n"
        "или укажите путь к .ttf в _FONT_CANDIDATES."
    )


def _pil_font(size: int):
    """TTF с кириллицей для подписей на диаграмме (иначе PIL рисует «тофу»).

    PIL по умолчанию использует растровый шрифт без кириллических глифов, поэтому
    подписи на картинке надо явно грузить из TTF — тем же набором, что и для PDF.
    """
    from PIL import ImageFont

    for regular, _bold in _FONT_CANDIDATES:
        if Path(regular).exists():
            return ImageFont.truetype(regular, size)
    return ImageFont.load_default()


def _build_diagram(path: Path) -> None:
    """Рисует простую диаграмму маршрутизации обращения (имитация скриншота)."""
    from PIL import Image, ImageDraw

    width, height = 760, 280
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    font = _pil_font(14)
    caption_font = _pil_font(13)

    boxes = [
        (20, 110, 180, 170, "Клиент\n(канал)"),
        (240, 110, 400, 170, "Очередь\nобращений"),
        (460, 60, 620, 120, "Правила\nраспределения"),
        (460, 160, 620, 220, "Оператор\n(статус)"),
    ]
    for x0, y0, x1, y1, label in boxes:
        draw.rectangle((x0, y0, x1, y1), outline="black", width=2)
        lines = label.split("\n")
        for index, line in enumerate(lines):
            tx = x0 + 12
            ty = y0 + 12 + index * 18
            draw.text((tx, ty), line, fill="black", font=font)

    # Стрелки между блоками (упрощённо — линиями).
    draw.line((180, 140, 240, 140), fill="black", width=2)
    draw.line((400, 140, 460, 90), fill="black", width=2)
    draw.line((400, 140, 460, 190), fill="black", width=2)
    draw.text(
        (20, 16),
        "Рис. 1. Маршрутизация обращения: канал → очередь → распределение → оператор",
        fill="black",
        font=caption_font,
    )

    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path)


def build(out_path: Path) -> Path:
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import cm
    from reportlab.platypus import (
        Image,
        PageBreak,
        Paragraph,
        SimpleDocTemplate,
        Spacer,
        Table,
        TableStyle,
    )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    diagram_path = out_path.parent / "_diagram.png"
    _build_diagram(diagram_path)

    font, font_bold = _register_font()

    styles = getSampleStyleSheet()
    # Заголовки с увеличенным кеглем — чтобы детектор заголовков по размеру
    # шрифта (а не только по нумерации) тоже срабатывал.
    h1 = ParagraphStyle("H1", parent=styles["Heading1"], fontName=font_bold, fontSize=18, spaceAfter=10)
    h2 = ParagraphStyle("H2", parent=styles["Heading2"], fontName=font_bold, fontSize=14, spaceAfter=8)
    body = ParagraphStyle("Body", parent=styles["BodyText"], fontName=font, fontSize=10.5, leading=15)
    title = ParagraphStyle("Title", parent=styles["Title"], fontName=font_bold, fontSize=24, alignment=TA_CENTER)
    subtitle = ParagraphStyle("Subtitle", parent=styles["Normal"], fontName=font, fontSize=12, alignment=TA_CENTER, textColor=colors.grey)

    story = []

    # --- Титульная страница ---
    story.append(Spacer(1, 6 * cm))
    story.append(Paragraph("Контакт-центр MANGO OFFICE", title))
    story.append(Spacer(1, 0.5 * cm))
    story.append(Paragraph("Руководство пользователя", subtitle))
    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph("Версия 1.26.23 (синтетическая фикстура для эксперимента issue #111)", subtitle))
    story.append(PageBreak())

    def h(level_style, number, text):
        # Нумерованный заголовок: "2.1 Статусы оператора".
        story.append(Paragraph(f"{number} {text}", level_style))

    def p(text):
        story.append(Paragraph(text, body))
        story.append(Spacer(1, 0.15 * cm))

    # --- 1. Введение ---
    h(h1, "1.", "Введение")
    h(h2, "1.1", "Назначение документа")
    p(
        "Документ описывает рабочее место оператора контакт-центра (КЦ): обработку "
        "обращений, очередь, распределение и статусы. Руководство предназначено для "
        "операторов, супервизоров и администраторов."
    )
    h(h2, "1.2", "Системные требования и ограничения")
    p(
        "Лимит одновременно работающих пользователей КЦ ограничен версией продукта и "
        "настраивается в Личном кабинете ВАТС. При достижении лимита подключение новых "
        "операторов блокируется до освобождения сессии."
    )
    story.append(PageBreak())

    # --- 2. Рабочее место оператора ---
    h(h1, "2.", "Рабочее место оператора")
    h(h2, "2.1", "Статусы оператора")
    p(
        "Статус определяет, какие обращения распределяются на оператора. Статус «Все "
        "звонки» позволяет одновременно обрабатывать очередь входящих вызовов и вызовы "
        "кампаний исходящего обзвона: алгоритм назначает освободившемуся сотруднику "
        "либо входящий вызов, либо вызов из кампании. Это одновременность в рамках "
        "одного канала (голос), не межканальная."
    )
    h(h2, "2.3", "Очередь обращений")
    p(
        "Панель «Очередь обращений» содержит раздельные вкладки: «Вызовы», «Текст» и "
        "«Заказы обратного звонка». Очередь текстовых обращений и звонков не зависимы "
        "друг от друга; на их обработку может быть назначена одна или разные группы."
    )
    story.append(PageBreak())

    # --- 3. Каналы коммуникации ---
    h(h1, "3.", "Каналы коммуникации")
    h(h2, "3.1", "Голосовые вызовы")
    p("Входящие и исходящие вызовы, кампании обзвона, заказы обратного звонка с сайта.")
    h(h2, "3.2", "Текстовые каналы")
    p(
        "Текстовые каналы подключаются через омни-/мультиканальные виджеты MANGO "
        "Диалоги и мессенджеры: Telegram, VK, WhatsApp, Max, Авито. Все они образуют "
        "единую «текстовую» очередь."
    )
    h(h2, "3.3", "Электронная почта (e-mail)")
    p(
        "E-mail обрабатывается как текстовый канал в редакторе писем КЦ. Если в письме "
        "распознан адрес сотрудника ВАТС — обращение сразу переходит в «В работе»; "
        "иначе попадает в очередь. E-mail-обращение, не распределённое за заданное "
        "время, автоматически закрывается."
    )
    story.append(PageBreak())

    # --- 4. Обработка обращений (с диаграммой) ---
    h(h1, "4.", "Обработка обращений")
    h(h2, "4.1", "Контроль обращений")
    p("Контроль ведётся в разрезе вызовов и текстовых обращений на панели очереди.")
    h(h2, "4.2", "Правила распределения")
    p(
        "Задаётся максимальное количество текстовых обращений, которые может "
        "обрабатывать один сотрудник. При достижении показателя обращения не "
        "распределяются на сотрудника, пока он не закроет одно из текущих. Если указан "
        "0 — обращения распределяются всегда. Доступны алгоритмы «на наименее "
        "загруженного оператора» и «равномерное распределение»."
    )
    p(
        "Чекбокс «Не распределять текстовые обращения на операторов, которые находятся "
        "в звонке» — единственная сегодня кросс-канальная связь между голосом и "
        "текстом. Сквозного межканального счётчика и приоритета каналов нет."
    )
    story.append(Spacer(1, 0.2 * cm))
    story.append(Image(str(diagram_path), width=15 * cm, height=5.5 * cm))
    story.append(Spacer(1, 0.2 * cm))
    h(h2, "4.3", "Каналы обращений")
    p("Перечень подключённых каналов и их настройки задаются в Личном кабинете ВАТС.")
    story.append(PageBreak())

    # --- 5. Роли и права доступа (таблица) ---
    h(h1, "5.", "Роли и права доступа")
    p(
        "Права на модуль «Обращения» и вкладки очереди настраиваются в ЛК ВАТС → "
        "Безопасность и ограничения → Настройка доступа. Базовая матрица ролей:"
    )
    table_data = [
        ["Роль", "Очередь", "Распределение", "Отчёты", "Настройки доступа"],
        ["Оператор", "Да", "Нет", "Свои", "Нет"],
        ["Супервизор", "Да", "Частично", "Группы", "Нет"],
        ["Администратор", "Да", "Да", "Все", "Да"],
        ["Руководитель компании", "Да", "Да", "Все", "Да"],
    ]
    table = Table(table_data, hAlign="LEFT", colWidths=[4.5 * cm, 2.2 * cm, 3 * cm, 2.3 * cm, 3.4 * cm])
    table.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("FONTNAME", (0, 0), (-1, -1), font),
                ("FONTNAME", (0, 0), (-1, 0), font_bold),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )
    story.append(table)
    p("")
    p(
        "Настройка автоматического распределения обращений доступна только ролям "
        "«Руководитель компании» и «Администратор»."
    )
    story.append(PageBreak())

    # --- 6. Отчёты и аналитика ---
    h(h1, "6.", "Отчёты и аналитика")
    p(
        "Отчёты строятся по вызовам и текстовым обращениям: длительность, время "
        "ожидания, число обращений на оператора, соблюдение лимитов. Доступ к отчётам "
        "зависит от роли (см. §5)."
    )

    doc = SimpleDocTemplate(
        str(out_path),
        pagesize=A4,
        title="Контакт-центр MANGO OFFICE — Руководство пользователя (фикстура)",
        author="mango_ba_prompts (synthetic fixture, issue #111)",
        subject="Contact Center manual sample for KB extraction experiment",
    )
    doc.build(story)

    # Подчищаем временную картинку диаграммы (она уже встроена в PDF; реальная
    # извлечённая версия появится в kb/processed/.../images/ при экстракции).
    try:
        diagram_path.unlink()
    except OSError:
        pass

    return out_path


def main(argv: list[str]) -> int:
    out = Path(argv[1]).resolve() if len(argv) > 1 else DEFAULT_OUT
    built = build(out)
    size = built.stat().st_size
    print(f"Сгенерирован фикстура-PDF: {built} ({size} байт)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
