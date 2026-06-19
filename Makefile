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

MANGO_SRC     := kb/sources/mango-cc-manual/CC_manual_1.26.23_compressed.pdf
MANGO_OUT     := kb/processed/mango-cc-manual
MANGO_TITLE   := Контакт-центр MANGO OFFICE - Руководство пользователя
MANGO_VERSION := 1.26.23
MANGO_NOTE    := Реальное руководство из issue 115; извлечено после диагностики KB Pipeline 11.

SRC     ?= $(SAMPLE_PDF)
OUT     ?= $(SAMPLE_OUT)
CODE    ?= $(DOC_CODE)
TITLE   ?= $(DOC_TITLE)
VERSION ?= $(DOC_VERSION)

.PHONY: help kb-all kb-sample kb-extract kb-mango kb-validate kb-tokens kb-clean

help:
	@echo "KB pipeline (issue #111):"
	@echo "  make kb-all       — kb-sample → kb-extract → kb-validate"
	@echo "  make kb-sample    — собрать синтетическую фикстуру PDF (reportlab+Pillow)"
	@echo "  make kb-extract   — извлечь SRC в OUT (по умолчанию фикстура → $(SAMPLE_OUT))"
	@echo "  make kb-mango     — извлечь реальный mango-cc-manual из issue #115"
	@echo "  make kb-validate  — проверить конвейер БЗ (stdlib-only, как в CI)"
	@echo "  make kb-tokens    — показать расход токенов по OUT/index.md и OUT/sections/*.md"
	@echo "  make kb-clean     — удалить временные файлы (pycache, _diagram.png)"
	@echo ""
	@echo "Зависимости извлечения: pip install -r scripts/kb/requirements.txt"
	@echo "Свой PDF: make kb-extract SRC=kb/sources/<slug>/<file.pdf> OUT=kb/processed/<slug> CODE=XX TITLE='...' VERSION=..."

# Полный прогон конвейера на синтетической фикстуре.
kb-all: kb-sample kb-extract kb-validate

# Собрать синтетический PDF-стенд (пока нет реального CC_manual_1.26.23.pdf).
kb-sample:
	$(PYTHON) scripts/kb/make_sample_pdf.py "$(SAMPLE_PDF)"

# Извлечь PDF в machine-readable БЗ (index.md + sections/ + images/ + meta.json).
kb-extract:
	$(PYTHON) scripts/kb/extract.py "$(SRC)" \
		--out "$(OUT)" \
		--doc-code "$(CODE)" \
		--doc-title "$(TITLE)" \
		--doc-version "$(VERSION)" \
		--note "$(NOTE)"

# Воспроизвести БЗ для реального руководства из issue #115.
kb-mango:
	$(MAKE) kb-extract \
		SRC="$(MANGO_SRC)" \
		OUT="$(MANGO_OUT)" \
		CODE="$(DOC_CODE)" \
		TITLE="$(MANGO_TITLE)" \
		VERSION="$(MANGO_VERSION)" \
		NOTE="$(MANGO_NOTE)"

# Проверка деливераблов issue #111 — stdlib-only, идентична шагу в CI.
kb-validate:
	$(PYTHON) scripts/validate_issue_111_kb_pipeline.py

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
