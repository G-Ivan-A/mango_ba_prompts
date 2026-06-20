# KB ingestion pipeline (issue #111) — PDF/источник → machine-readable БЗ.
# Конвейер и оценка качества: docs/kb-experiment-report.md
# Человеку: как пополнять БЗ — kb/sources/README.md
#
# Быстрый старт (нужны зависимости из scripts/kb/requirements.txt):
#   make kb-all       # фикстура → извлечение → проверка
#   make kb-validate  # только проверка (stdlib-only, как в CI)

PYTHON ?= python3

SAMPLE_PDF  := kb/sources/contact-center-manual-sample/CC_manual_sample.fixture.pdf
SAMPLE_OUT  := kb/processed/contact-center-manual-sample
DOC_CODE    := CC
DOC_TITLE   := Контакт-центр MANGO OFFICE
DOC_VERSION := 1.26.23-sample
NOTE        := Синтетическая фикстура: реальный CC_manual_1.26.23.pdf не загрузился в issue 111. Структура воспроизводит реальное руководство (issue 109). Замените PDF и перезапустите для реальных данных.

MANGO_SRCS    := kb/sources/mango-cc-manual/CC_manual_1.26.23-part-1.pdf \
                 kb/sources/mango-cc-manual/CC_manual_1.26.23-part-2.pdf \
                 kb/sources/mango-cc-manual/CC_manual_1.26.23-part-3.pdf \
                 kb/sources/mango-cc-manual/CC_manual_1.26.23-part-4.pdf \
                 kb/sources/mango-cc-manual/CC_manual_1.26.23-part-5.pdf \
                 kb/sources/mango-cc-manual/CC_manual_1.26.23-part-6.pdf
MANGO_SRC     := $(MANGO_SRCS)
MANGO_OUT     := kb/processed/mango-cc-manual
MANGO_TITLE   := Контакт-центр MANGO OFFICE - Руководство пользователя
MANGO_VERSION := 1.26.23
MANGO_NOTE    := Multi-part руководство КЦ из issue 119; 6 PDF частей обработаны как один документ со сквозной пагинацией.

LK_SRCS     := kb/sources/mango-lk-manual/LK_manual_v-121часть-1.pdf \
               kb/sources/mango-lk-manual/LK_manual_v-121часть-2.pdf \
               kb/sources/mango-lk-manual/LK_manual_v-121часть-3.pdf \
               kb/sources/mango-lk-manual/LK_manual_v-121часть-4.pdf \
               kb/sources/mango-lk-manual/LK_manual_v-121часть-5.pdf
LK_OUT      := kb/processed/mango-lk-manual
LK_TITLE    := Виртуальная АТС MANGO OFFICE - Справочник абонента
LK_VERSION  := 1.21
LK_NOTE     := Multi-part руководство ЛК из issue 117; 5 PDF частей обработаны как один документ со сквозной пагинацией.

SRC     ?= $(SAMPLE_PDF)
SRCS    ?= $(SRC)
OUT     ?= $(SAMPLE_OUT)
CODE    ?= $(DOC_CODE)
TITLE   ?= $(DOC_TITLE)
VERSION ?= $(DOC_VERSION)
SOURCE_DIR ?= kb/sources/mango-cc-manual

.PHONY: help kb-all kb-sample kb-extract kb-source-plan kb-source-extract kb-mango kb-lk kb-mtalker kb-validate kb-tokens kb-clean

help:
	@echo "KB pipeline (issue #111):"
	@echo "  make kb-all       — kb-sample → kb-extract → kb-validate"
	@echo "  make kb-sample    — собрать синтетическую фикстуру PDF (reportlab+Pillow)"
	@echo "  make kb-extract   — извлечь SRC/SRCS в OUT (по умолчанию фикстура → $(SAMPLE_OUT))"
	@echo "  make kb-source-plan SOURCE_DIR=kb/sources/<slug> — показать manifest-driven план"
	@echo "  make kb-source-extract SOURCE_DIR=kb/sources/<slug> — извлечь по meta.json"
	@echo "  make kb-mango     — извлечь multi-part mango-cc-manual из issue #119"
	@echo "  make kb-lk        — извлечь multi-part mango-lk-manual из issue #117"
	@echo "  make kb-mtalker   — извлечь multi-document Mango Talker из issue #121"
	@echo "  make kb-validate  — проверить конвейер БЗ (stdlib-only, как в CI)"
	@echo "  make kb-tokens    — показать расход токенов по OUT/index.md и OUT/sections/*.md"
	@echo "  make kb-clean     — удалить временные файлы (pycache, _diagram.png)"
	@echo ""
	@echo "Зависимости извлечения: pip install -r scripts/kb/requirements.txt"
	@echo "Свой PDF: make kb-extract SRC=kb/sources/<slug>/<file.pdf> OUT=kb/processed/<slug> CODE=XX TITLE='...' VERSION=..."
	@echo "Multi-part PDF: make kb-extract SRCS='kb/sources/<slug>/part-1.pdf kb/sources/<slug>/part-2.pdf' OUT=kb/processed/<slug> CODE=XX"
	@echo "Manifest-driven: make kb-source-extract SOURCE_DIR=kb/sources/<slug>"

# Полный прогон конвейера на синтетической фикстуре.
kb-all: kb-sample kb-extract kb-validate

# Собрать синтетический PDF-стенд (пока нет реального CC_manual_1.26.23.pdf).
kb-sample:
	$(PYTHON) scripts/kb/make_sample_pdf.py "$(SAMPLE_PDF)"

# Извлечь PDF в machine-readable БЗ (index.md + sections/ + images/ + meta.json).
kb-extract:
	$(PYTHON) scripts/kb/extract.py $(SRCS) \
		--out "$(OUT)" \
		--doc-code "$(CODE)" \
		--doc-title "$(TITLE)" \
		--doc-version "$(VERSION)" \
		--note "$(NOTE)"

# Проверить, как meta.json разворачивается в extraction jobs (без чтения PDF).
kb-source-plan:
	$(PYTHON) scripts/kb/process_sources.py "$(SOURCE_DIR)" --dry-run

# Извлечь один каталог kb/sources/<slug>/ по явному source manifest.
kb-source-extract:
	$(PYTHON) scripts/kb/process_sources.py "$(SOURCE_DIR)"

# Воспроизвести БЗ для split-руководства КЦ из issue #119.
kb-mango:
	$(MAKE) kb-extract \
		SRCS="$(MANGO_SRCS)" \
		OUT="$(MANGO_OUT)" \
		CODE="$(DOC_CODE)" \
		TITLE="$(MANGO_TITLE)" \
		VERSION="$(MANGO_VERSION)" \
		NOTE="$(MANGO_NOTE)"

# Воспроизвести БЗ для split-руководства ЛК из issue #117.
kb-lk:
	$(MAKE) kb-extract \
		SRCS="$(LK_SRCS)" \
		OUT="$(LK_OUT)" \
		CODE="LK" \
		TITLE="$(LK_TITLE)" \
		VERSION="$(LK_VERSION)" \
		NOTE="$(LK_NOTE)"

# Воспроизвести multi-document комплект Mango Talker из issue #121.
kb-mtalker:
	$(MAKE) kb-source-extract SOURCE_DIR="kb/sources/mtalker"

# Проверка деливераблов БЗ — stdlib-only, идентична лёгкому шагу CI.
kb-validate:
	$(PYTHON) scripts/validate_issue_111_kb_pipeline.py
	$(PYTHON) scripts/validate_issue_115_kb_mango_pipeline.py
	$(PYTHON) scripts/validate_issue_117_kb_traceability.py
	$(PYTHON) scripts/validate_issue_121_kb_multi_file.py

# Наглядно: токены индекса vs отдельных разделов (метод — см. token_method).
kb-tokens:
	@echo "Расход токенов (метод см. в meta.json → token_method):"
	@for f in "$(OUT)/index.md" "$(OUT)"/sections/*.md; do \
		printf '  %-58s ' "$$f"; $(PYTHON) scripts/kb/tokens.py "$$f"; \
	done

# Удалить только временные артефакты. Фикстура и kb/processed/ — закоммичены и
# воспроизводимы через `make kb-sample kb-extract` (см. отчёт, раздел 9).
kb-clean:
	rm -rf scripts/kb/__pycache__
	rm -f kb/sources/contact-center-manual-sample/_diagram.png
