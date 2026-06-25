---
status: draft
version: 0.4
updated: 2026-06-24
ai-generated: true
---

# Changelog — mango_ba_prompts

Все значимые изменения проекта документируются здесь. Формат основан на
[Keep a Changelog](https://keepachangelog.com/ru/1.1.0/); проект придерживается
[Semantic Versioning](https://semver.org/lang/ru/).

## Unreleased

### Added — Issue #233 структурный анализ БА-процессов и артефактов с опорой на индустрию

- Добавлен аналитический документ
  [`docs/analysis/ba-processes-industry-analysis.md`](docs/analysis/ba-processes-industry-analysis.md),
  выполняющий структурный анализ БА-процессов и артефактов репозитория с опорой
  на индустриальные практики телекома и фреймворки бизнес-анализа.
- Документ проходит обязательную последовательность (Этапы 1-10) тремя ролями
  (Архитектор БА-методологий, AI-инженер, BA-эксперт) и содержит все 12
  разделов: введение, текущее состояние БА-процессов, индустриальные практики
  телекома (16 компаний с источниками), фреймворки БА (BABOK, IREB, BCS, PMI-PBA,
  Agile BA/SAFe + ISO/IEC/IEEE 29148), таксономию артефактов (комплексные vs
  атомарные, маппинг на онтологию `A01`-`A31`), сравнительный анализ
  (процесс→индустрия, артефакт→индустрия, пробелы `G1`-`G5`, излишества
  `E1`-`E4`), SWOT и рекомендации `R1`-`R7`, проверку стандартов проекта
  (L1-L3, контракты vs стандарты, неправильно отнесённые документы), полный
  список артефактов по уровням и типам, вход для RFC (`RFC-IN-1`..`RFC-IN-8`),
  дополнительные исследования и заключение.
- Ключевые находки: гипотезы `H1`-`H6` с уровнями доказательности
  (`[CONFIRMED]`/`[INFERRED]`/`[HYPOTHESIS]`/`NOT FOUND`); граница
  composite/atomic совпадает с индустриальной парой Requirements Document vs
  Singular/atomic requirement; универсальный де-факто «контракт» телекома —
  OpenAPI/TM Forum Open API; полоса $400-600M публично почти не населена;
  фокус-компания «Манго Телеком» сама ниже полосы и проходит переход «длинные
  ТЗ → User Stories». Эмпирическая база с источниками по каждой компании — в
  [`docs/analysis/telecom-vendors-ba-practices-research.md`](docs/analysis/telecom-vendors-ba-practices-research.md).
- Добавлены две Mermaid-диаграммы (таксономия артефактов и проверка
  классификации L1-L3).
- Документ носит характер «только анализ»: процессы, артефакты и стандарты
  ([`standards/ba-ontology.md`](standards/ba-ontology.md),
  [`standards/executable-contract-standard.md`](standards/executable-contract-standard.md),
  [`governance/bcreq-fr-generation-contract.md`](governance/bcreq-fr-generation-contract.md),
  [`runs/CONTRACT.md`](runs/CONTRACT.md)) процитированы по функции, но не
  изменены; решения не принимаются.
- Добавлен регрессионный валидатор
  [`scripts/validate_issue_233_ba_processes_industry_analysis.py`](scripts/validate_issue_233_ba_processes_industry_analysis.py),
  подключённый к GitHub Pages workflow.

### Added — Issue #231 структурный анализ применения контракта BCREQ-FR

- Добавлен аналитический документ
  [`docs/analysis/bcreq-fr-contract-process-analysis.md`](docs/analysis/bcreq-fr-contract-process-analysis.md),
  отвечающий на вопрос, применяется ли контракт
  [`governance/bcreq-fr-generation-contract.md`](governance/bcreq-fr-generation-contract.md)
  как единый монолитный промпт или как последовательность специализированных
  промптов, и фиксирующий максимальный набор проблем процессов генерации.
- Документ проходит обязательный 7-этапный разбор тремя ролями (Архитектор
  процессов, AI-инженер, BA-эксперт): гипотезы `H1`..`H7`, структурный анализ
  трёх режимов применения, причинно-следственный анализ (`5 почему`), тесты
  «контракт-как-промпт против последовательности» на естественном эксперименте
  `RUN-0014` против `RUN-0010`/`RUN-0011`, каталог проблем `PA-1`..`PA-6`,
  `AIE-1`..`AIE-6`, `BA-1`..`BA-5`, `VER-1`..`VER-3` и восемь граничных кейсов
  `EC-1`..`EC-8`.
- Документ носит характер «только анализ»: контракт BCREQ-FR и
  [`runs/CONTRACT.md`](runs/CONTRACT.md) не изменялись, решения не принимаются.
- Добавлен регрессионный валидатор
  [`scripts/validate_issue_231_bcreq_fr_contract_process_analysis.py`](scripts/validate_issue_231_bcreq_fr_contract_process_analysis.py),
  подключённый к GitHub Pages workflow.

### Added — Issue #229 исследование трассируемости промптов в runs

- Добавлен исследовательский отчёт
  [`docs/analysis/runs-observability-research.md`](docs/analysis/runs-observability-research.md)
  по проблемам трассируемости промптов в `runs/` и внешним практикам контроля
  проходов (триггер — лог `runs/2026/RUN-0014/logs/business-task-log.md`).
- Отчёт фиксирует проблемы `P1`–`P5` с доказательствами, сопоставляет пять
  внешних практик (LLM observability, experiment tracking, distributed tracing,
  prompt engineering, contract testing) с источниками, разбирает восемь
  граничных кейсов, восемь областей дополнительного анализа (четыре волны) и
  формулирует рекомендации `R-LOG-*`, `R-TRACE-*`, `R-VER-*`, `R-NAME-*`,
  `R-MAP-*` с обоснованием и приоритетами.
- Документ остаётся research-задачей: контракт `runs/CONTRACT.md` не изменён,
  существующие run-артефакты не тронуты, решения не приняты — только анализ и
  рекомендации.
- Добавлен регрессионный валидатор
  [`scripts/validate_issue_229_runs_observability_research.py`](scripts/validate_issue_229_runs_observability_research.py),
  подключённый к GitHub Pages workflow.

### Added — Issue #225 исследование цепочки артефактов

- Добавлен исследовательский отчёт
  [`docs/analysis/artifact-chain-hypothesis-research.md`](docs/analysis/artifact-chain-hypothesis-research.md)
  по гипотезе `research → analytics → report → rfc/adr → standard → artifact`.
- Отчёт сопоставляет видение Фаундера с международными практиками ADR, RFC,
  стандартов и design documents, фиксирует роли экспертов, риски `R-1`..`R-7`,
  возможности `O-1`..`O-7`, анализ текущего RFC-процесса и ответы на вопросы
  issue #225.
- Добавлены четыре BPMN-like Mermaid-диаграммы: основная цепочка артефактов,
  процесс RFC, процесс ADR и процесс согласования; RFC, ADR, стандарты,
  контракты и процессы не изменялись.
- Добавлен регрессионный валидатор
  [`scripts/validate_issue_225_artifact_chain_research.py`](scripts/validate_issue_225_artifact_chain_research.py),
### Added — Issue #226 контракт генерации RFC

- Добавлен L1-контракт
  [`governance/rfc-generation-contract.md`](governance/rfc-generation-contract.md)
  в 100% YAML для генерации L3 RFC-документов: полный набор входов,
  frontmatter, разделы 1-8, YAML problem list с `RFC-NNN-Pn`, proposal index
  с `RFC-NNN-Rn`, traceability, style rules и validation checks.
- Provenance и исследовательская база зарегистрированы в
  [`governance/contracts-registry.md`](governance/contracts-registry.md), а
  проверка реального сценария и edge cases записана в
  [`runs/2026/RUN-0015/outputs/rfc-generation-contract-test-report.md`](runs/2026/RUN-0015/outputs/rfc-generation-contract-test-report.md).
- Добавлен регрессионный валидатор
  [`scripts/validate_issue_226_rfc_generation_contract.py`](scripts/validate_issue_226_rfc_generation_contract.py),
  подключённый к GitHub Pages workflow.

### Fixed — Issue #219 область ФТ RUN-0012

- ФТ
  [`runs/2026/RUN-0012/outputs/2026-06-22-bcreq-180-mt-group-video-call-ft.md`](runs/2026/RUN-0012/outputs/2026-06-22-bcreq-180-mt-group-video-call-ft.md)
  актуализировано по вложениям issue #219: из раздела 4 исключены требования,
  описывающие текущую функциональность ВКС, включая список участников,
  администрирование участников и подключение по ссылке.
- В scope оставлена дельта: быстрый старт группового звонка без общего чата и
  ручной рассылки ссылки, личные группы и звуковые сигналы подключения/
  отключения; обоснование исключений записано в `RUN-0012` business-task log.
- Добавлен регрессионный валидатор
  [`scripts/validate_issue_219_bcreq_fr_scope.py`](scripts/validate_issue_219_bcreq_fr_scope.py),
  подключённый к GitHub Pages workflow.
### Added — Issue #221 аудит naming convention

- Добавлен аудит
  [`docs/analysis/naming-convention-audit.md`](docs/analysis/naming-convention-audit.md)
  по uppercase, camelCase/PascalCase, snake_case и special-character случаям в
  tracked paths репозитория; отчёт сопоставляет каждый случай с регулирующим
  контрактом и гипотезой причины.
- Добавлен воспроизводимый scan helper
  [`experiments/issue-221/naming-audit-scan.py`](experiments/issue-221/naming-audit-scan.py)
  для повторной проверки инвентаря без переименования файлов и без изменения
  стандартов.
### Added — Issue #220 BCREQ-FR группировки номеров ВАТС по направлениям (BCREQ-1040)

- Добавлен прогон
  [`runs/2026/RUN-0014/`](runs/2026/RUN-0014/) (`run_type: business-task`,
  `process: bcreq-1040`): по контракту
  [`governance/bcreq-fr-generation-contract.md`](governance/bcreq-fr-generation-contract.md)
  сгенерирован BCREQ-FR
  [`outputs/2026-06-24-bcreq-1040-speech-analytics-direction-grouping-fr.md`](runs/2026/RUN-0014/outputs/2026-06-24-bcreq-1040-speech-analytics-direction-grouping-fr.md)
  для речевой аналитики: группировка номеров ВАТС по 3 направлениям
  (мини-брус, ПРЕКАТ, ПРЕФАБ), фильтрация «Анализа по чек-листам» и «Ловца
  инсайтов» по направлению и единый дашборд с фильтром по категории.
- Обоснование границ scope (правила `BCREQ-FR-GEN-SCOPE-01/02`) вынесено в
  [`outputs/analysis-bcreq-1040-scope-2026-06-24.md`](runs/2026/RUN-0014/outputs/analysis-bcreq-1040-scope-2026-06-24.md);
  входные данные и извлечения из базы знаний — в `inputs/`.
- Обновлены реестр `runs/REGISTRY.md` и статистика `runs/stats/*`;
  регрессионные валидаторы issue #123/#133/#207 синхронизированы с новым
  прогоном.

### Fixed — Issue #217 контракт logs для runs

- `runs/CONTRACT.md` получил kebab-case идентификатор `runs-contract`, явный
  заголовок таблицы `Типы run'ов (run_type)` и MUST-правило: каждый факт
  прохода создаёт основной Markdown-лог в `logs/`, а `.gitkeep` не считается
  логом.
- Все существующие `RUN-0001`..`RUN-0013` получили канонический Markdown-лог по
  `run_type`, а `metadata.yaml` теперь содержит `logs:` со ссылкой на основной
  лог; `runs/REGISTRY.md` показывает отдельную колонку `Лог`.
- Исследование контрактов записано в
  [`docs/analysis/runs-contract-log-policy-audit.md`](docs/analysis/runs-contract-log-policy-audit.md);
  добавлен регрессионный валидатор
  [`scripts/validate_issue_217_runs_log_contract.py`](scripts/validate_issue_217_runs_log_contract.py),
  подключённый к GitHub Pages workflow.

### Fixed — Issue #215 контракт BCREQ-FR в 100% YAML

- Контракт
  [`governance/bcreq-fr-generation-contract.md`](governance/bcreq-fr-generation-contract.md)
  переписан как валидный YAML stream: metadata document + machine-readable
  rule index первым блоком body; Markdown-проза, таблицы и fenced blocks
  удалены.
- Provenance issues/PR вынесен в новый YAML-реестр
  [`governance/contracts-registry.md`](governance/contracts-registry.md);
  в runtime-контракте оставлен только `contract_registry_id` без гиперссылок
  на issue/PR.
- Добавлен регрессионный валидатор
  [`scripts/validate_issue_215_bcreq_fr_yaml_contract.py`](scripts/validate_issue_215_bcreq_fr_yaml_contract.py),
  подключённый к GitHub Pages workflow; валидаторы issue #196/#208/#211
  обновлены под новую YAML-структуру.

### Added — Issue #212 стандарт создания исполнимых контрактов

- Добавлен L3-стандарт
  [`standards/executable-contract-standard.md`](standards/executable-contract-standard.md):
  критерии L1/L2/L3, combat/management/data, разделение форматов
  L1=100% YAML / L2=JSON/YAML или Markdown / L3=Markdown with YAML frontmatter,
  YAML-шаблон L1-контракта, placement rules и жёсткий инвариант L1 runtime
  inputs без L3-зависимостей.
- Добавлен L2-реестр source/provenance контрактов
  [`governance/contracts-registry.md`](governance/contracts-registry.md);
  L1-контракт хранит только `contract_registry_id`, без direct L3 hyperlinks и
  embedded provenance.
- В стандарте выполнена самостоятельная классификация артефактов из
  `standards/`, `governance/`, `prompts/`, `runs/` и data-near контрактов
  `kb/`; шаблон проверен на `governance/bcreq-fr-generation-contract.md`,
  `runs/CONTRACT.md` и `standards/prompt-standard.md`.
- Добавлен регрессионный валидатор
  [`scripts/validate_issue_212_executable_contract_standard.py`](scripts/validate_issue_212_executable_contract_standard.py),
  подключённый к GitHub Pages workflow.

### Added — Issue #211 контракт Golden Examples

- Создан каталог [`kb/golden-examples/`](kb/golden-examples/) с
  [`kb/golden-examples/README.md`](kb/golden-examples/README.md),
  подкаталогами `bcreq-fr/`, `rfc/`, `adr/` и YAML-контрактом
  [`kb/golden-examples/CONTRACT.md`](kb/golden-examples/CONTRACT.md) для
  lifecycle будущих Golden Examples.
- В
  [`governance/bcreq-fr-generation-contract.md`](governance/bcreq-fr-generation-contract.md)
  временная трассировка вложений заменена на `source_attachments` со
  `status: "no-golden-standard"`; замена на `path + sha` требует
  2-факторное подтверждение через approval process.
- Добавлен регрессионный валидатор
  [`scripts/validate_issue_211_golden_examples_contract.py`](scripts/validate_issue_211_golden_examples_contract.py),
  подключённый к GitHub Pages workflow.

### Fixed — Issue #207 структура RUN-0013 и API VPBX для BCREQ-1027

- BCREQ-1027 перенесён в канонический run
  [`runs/2026/RUN-0013/`](runs/2026/RUN-0013/) с `metadata.yaml`, входом,
  логом, feedback и артефактом
  [`runs/2026/RUN-0013/outputs/section-4-3-api.md`](runs/2026/RUN-0013/outputs/section-4-3-api.md).
- Раздел 4.3 скорректирован на основе API ВАТС
  `POST /vpbx/stats/calls/result`: прежняя привязка к другому API удалена из
  артефакта, а структура запроса/ответа описана по
  `kb/mango-product-docs/processed/vpbx-api/sections/62-poluchenie-statistiki-vyzovov.md`.
- `runs/REGISTRY.md`, `runs/stats/`, валидаторы issue #199/#205 и новый
  [`scripts/validate_issue_207_bcreq_1027_vpbx_run.py`](scripts/validate_issue_207_bcreq_1027_vpbx_run.py)
  обновлены и подключены к GitHub Pages workflow.
### Fixed — Issue #208 L3-утечки в контракте BCREQ-FR

- Контракт
  [`governance/bcreq-fr-generation-contract.md`](governance/bcreq-fr-generation-contract.md)
  переведён в `active` v0.3: `integrates:` и §2 теперь используют только L2
  registry inputs `kb/industry-taxonomy/registry.json` и
  `kb/mango-taxonomy/registry.json`; правила RFC-184 оставлены как локальные
  `BCREQ-FR-GEN-SCOPE-01/02` в machine-readable index.
- Нестабильные `github.com/user-attachments` в `source_attachments:` удалены;
  lifecycle placeholder/permalink для Golden Examples закреплён в issue #211.
- Добавлены регрессионный валидатор
  [`scripts/validate_issue_208_bcreq_fr_l3_boundary.py`](scripts/validate_issue_208_bcreq_fr_l3_boundary.py)
  и dry-run evidence
  [`experiments/issue-208/bcreq-1027-l3-boundary-dry-run.md`](experiments/issue-208/bcreq-1027-l3-boundary-dry-run.md);
  проверка подключена к GitHub Pages workflow.

### Added — Issue #203 поиск и трассировка API VPBX

- Улучшен конвейер генерации `kb/mango-product-docs/processed/vpbx-api`:
  metadata из source manifest теперь сохраняет aliases `API VPBX`/`VPBX API`
  и Mango Taxonomy traceability к `vats-core` в `meta.json`, `index.md` и
  frontmatter каждого section chunk.
- Индекс `vpbx-api` теперь явно сопоставляет запрос `event onAppealClose` с
  событием `/events/md/onAppealClose` и сохраняет endpoint-ключи для методов
  API VPBX, включая `/cc/appeals/create-closed-appeals`.
- Добавлен регрессионный валидатор
  `scripts/validate_issue_203_vpbx_api_retrieval.py`, подключённый к
  `make kb-validate` и KB workflow.

### Fixed — Issue #205 структура runs для BCREQ-1027

- Предыдущая промежуточная структура BCREQ-1027 заменена канонической записью
  [`RUN-0013`](runs/2026/RUN-0013/metadata.yaml) согласно `runs/CONTRACT.md`.
- Проверки issue #205 сохранены как регрессионные проверки отсутствия старого
  размещения и корректной регистрации артефакта в `runs/REGISTRY.md`.

### Added — Issue #199 раздел 4.3 API-методов BCREQ-1027

- Актуальный артефакт раздела 4.3 расположен в
  [`runs/2026/RUN-0013/outputs/section-4-3-api.md`](runs/2026/RUN-0013/outputs/section-4-3-api.md)
  и после исправления issue #207 описывает метод API ВАТС
  `POST /vpbx/stats/calls/result`.
- В артефакте зафиксированы delta-резюме, источники, taxonomy traceability и
  проверка соблюдения `RFC-184-S1`/`RFC-184-S2`: раздел 3 не формируется,
  As-Is и исторический контекст не переносятся в результат.
- Добавлен валидатор
  [`scripts/validate_issue_199_bcreq_1027_section_4_3.py`](scripts/validate_issue_199_bcreq_1027_section_4_3.py),
  подключённый к GitHub Pages workflow.
### Added — Issue #198 систематизация проблем исполнимых контрактов и RFC

- Добавлен аналитический отчёт
  [`docs/analysis/executable-contracts-and-rfc-problems.md`](docs/analysis/executable-contracts-and-rfc-problems.md):
  сквозная инвентаризация дефектов исполнимых контрактов (P1-P5) и RFC (P6) по
  всему проекту с привязкой каждой проблемы к `file:line` и подробным планом
  исправления (25 действий). Отчёт формализует трёхуровневую модель L1/L2/L3,
  разделение классов правил (управление vs боевой), правило выбора формата
  (текст vs YAML/JSON) и единую рекомендуемую структуру RFC.
- Только анализ и предложения: контракты, промпты и RFC не изменялись и не
  создавались (ограничение задачи #198).
### Added — Issue #192 аналитическое исследование структуры каталогов

- Добавлен аналитический отчёт
  [`docs/analysis/repository-structure-analysis.md`](docs/analysis/repository-structure-analysis.md):
  обоснование архитектуры каталогов проекта на эмпирике 15+ международных
  проектов (структуры проверены через `gh api` git-trees на закреплённых SHA) и
  международных стандартах (COBIT 2019, ISO/IEC 38500, TOGAF, ISO/IEC/IEEE
  42010, Diátaxis, DAMA-DMBOK, IETF BCP 14, TM Forum).
- Отчёт отвечает на 6 исследовательских вопросов (правила исполнения процессов,
  структура `docs/`, размещение стандартов, границы governance, нужен ли
  отдельный `artifact/`, масштабирование на код и агентов), приводит As-Is/To-Be
  Mermaid-диаграммы, сводную матрицу trade-offs, migration roadmap и рекомендации
  по синхронизации с Хабом.
- Creative mode: создан только аналитический отчёт; файлы репозитория не
  перемещались и не переименовывались, новые каталоги не вводились. Решения с
  trade-offs вынесены на утверждение Пользователя (ADR), а не внедрены.

### Added — Issue #196 контракт генерации BCREQ-FR

- Добавлен исполнимый контракт AI-агента
  [`governance/bcreq-fr-generation-contract.md`](governance/bcreq-fr-generation-contract.md)
  для генерации комплексного BCREQ-FR: правила разделов 1-7, машинно-читаемый
  индекс, заглушки разделов 5 и 7, стиль кратких 4.x.x/4.x.x.x формулировок,
  taxonomy/product-doc traceability и финальный блок валидации.
- В контракт встроены ссылки на `RFC-184-S1` и `RFC-184-S2` из
  [`governance/rfc/bcreq-ft-scope-formation-rules-proposal.md`](governance/rfc/bcreq-ft-scope-formation-rules-proposal.md):
  BCREQ-FR описывает доработку, не текущую функциональность; закрытые явно или
  альтернативно потребности исключаются из результирующего документа.
- Добавлен валидатор
  [`scripts/validate_issue_196_bcreq_fr_contract.py`](scripts/validate_issue_196_bcreq_fr_contract.py),
  подключённый к GitHub Pages workflow; README и artifact map дополнены новой
  точкой входа.

### Added — Issue #193 контракт AI-агента для согласования документов

- Добавлен исполнимый governance-контракт
  [`governance/approval-contract.md`](governance/approval-contract.md):
  подготовка к согласованию, атомарное ревью по разделам, обработка отсутствующей
  конкретики, завершение, особые случаи, роль AI и применимость к RFC/ADR/
  standards/research/analysis documents.
- Контракт уточнён по обратной связи из PR #194: размещён в корне
  `governance/`, выбирает блок согласования на уровне H1/H2, требует загрузки
  читаемых документов в рабочий контекст, запрещает галлюцинации разделов и
  добавляет критическую оценку с рекомендацией согласовать / не согласовать.
- Контракт протестирован сухим прогоном на RFC Industry Taxonomy:
  [`docs/analysis/approval-contract-test-industry-rfc.md`](docs/analysis/approval-contract-test-industry-rfc.md).
  Тест формирует первый пакет согласования и останавливается до раздела 2, чтобы
  сохранить атомарность процесса.
- Добавлен валидатор
  [`scripts/validate_issue_193_approval_contract.py`](scripts/validate_issue_193_approval_contract.py),
  подключённый к GitHub Pages workflow.

### Changed — Issue #190 унификация имён файлов taxonomy registry

- Файлы Industry Taxonomy и Mango Taxonomy переименованы к единому паттерну
  `registry.json` / `registry.schema.json`:
  [`kb/industry-taxonomy/registry.json`](kb/industry-taxonomy/registry.json),
  [`kb/industry-taxonomy/registry.schema.json`](kb/industry-taxonomy/registry.schema.json),
  [`kb/mango-taxonomy/registry.json`](kb/mango-taxonomy/registry.json) и
  [`kb/mango-taxonomy/registry.schema.json`](kb/mango-taxonomy/registry.schema.json).
- Обновлены ссылки в README, стандартах, ADR, аналитических документах,
  валидаторах, workflow и экспериментах; добавлена регрессионная проверка
  [`scripts/validate_issue_190_taxonomy_registry_filenames.py`](scripts/validate_issue_190_taxonomy_registry_filenames.py),
  подключённая к `make kb-validate` и KB workflow.
### Added — Issue #186 RFC Rules Registry System

- Добавлен RFC
  [`docs/analysis/rfc-rules-registry-system.md`](docs/analysis/rfc-rules-registry-system.md)
  с анализом существующих rule-like источников, предложением atomic rule model,
  process/operation bindings, AI-agent contract, lifecycle, validation approach
  и вопросами на founder approval. Реестр правил, новые governance-контракты,
  изменения промптов и validator не внедрялись до явного approval.

### Changed — Issue #184 доработка ФТ RUN-0012 по ревью БА (чистка скоупа)

- По итогам ревью БА (issue
  [#184](https://github.com/G-Ivan-A/mango_ba_prompts/issues/184)) доработан ФТ
  [`2026-06-22-bcreq-180-mt-group-video-call-ft.md`](runs/2026/RUN-0012/outputs/2026-06-22-bcreq-180-mt-group-video-call-ft.md):
  из Раздела 2.1 удалён исторический контекст про аудиоконференции; из ФТ
  исключены все требования по вертикальной прокрутке списка участников (закрыты
  альтернативно — постраничным переключением ВКС), пункты перенумерованы,
  перекрёстные ссылки выверены. Артефакт приведён к чистому виду: только предмет
  доработки, без исторических данных и без требований, закрытых текущей
  функциональностью.
- Добавлен RFC
  [`governance/rfc/bcreq-ft-scope-formation-rules-proposal.md`](governance/rfc/bcreq-ft-scope-formation-rules-proposal.md)
  с правилами формирования скоупа bcreq-ФТ — **RFC-184-S1** (ФТ описывает
  доработку, а не текущую функциональность; исключение — зависимость от настроек /
  gross-layer классов и функций) и **RFC-184-S2** (принцип масштаба: запрос
  одного пользователя не основание менять закрытую функциональность; отделение
  исторического контекста). RFC зарегистрирован в
  [`governance/rfc-register.md`](governance/rfc-register.md) (статус `proposed`,
  промпты не изменялись).
- Все комментарии ревью и обоснования исключений сведены в резюме прогона
  [`summary-bcreq-180-2026-06-22.md`](runs/2026/RUN-0012/outputs/summary-bcreq-180-2026-06-22.md)
  (раздел «Доработка по обратной связи issue #184») и лог
  [`logs/experiment-log.md`](runs/2026/RUN-0012/logs/experiment-log.md).

### Added — Issue #180 ФТ группового звонка Mango Talker (на основе ВКС)

- Добавлен прогон [`runs/2026/RUN-0012/`](runs/2026/RUN-0012/) (тип
  `business-task`, процесс `bcreq-180-mt-group-video-call`) с комплексным
  документом функциональных требований на согласование заказчика
  [`2026-06-22-bcreq-180-mt-group-video-call-ft.md`](runs/2026/RUN-0012/outputs/2026-06-22-bcreq-180-mt-group-video-call-ft.md)
  (разделы 1, 2, 4, 6). Документ переориентирует ранее согласованный ФТ по
  аудиоконференциям на решение, основанное на видеоконференциях Mango Talker
  (`talker-video-meeting-service`), с сохранением стиля и терминологии исходного
  документа: быстрый старт группового звонка из раздела «Встречи», прозрачное
  отображение и управление составом участников, личные группы в адресной книге,
  инвертированные звуковые сигналы подключения/отключения, переподключение по
  ссылке из истории.
- Добавлены резюме с метаданными
  [`summary-bcreq-180-2026-06-22.md`](runs/2026/RUN-0012/outputs/summary-bcreq-180-2026-06-22.md)
  и лог эксперимента
  [`logs/experiment-log.md`](runs/2026/RUN-0012/logs/experiment-log.md)
  (ядро из 6 метрик); процесс прогона зафиксирован также в
  [`experiments/issue-180/`](experiments/issue-180/).
- Обновлены реестр и статистика runs/ (`REGISTRY.md`, `stats/by-type.md`,
  `stats/by-date.md`, `stats/by-process.md`) и регрессионные проверки
  [`scripts/validate_issue_123_runs_contract.py`](scripts/validate_issue_123_runs_contract.py)
  и [`scripts/validate_issue_133_runs_restructure.py`](scripts/validate_issue_133_runs_restructure.py)
  с учётом RUN-0012.

### Changed — Issue #172 переименование taxonomy namespaces

- Два прежних дочерних taxonomy-каталога `industry` и `mango` внутри `kb/`
  переименованы через `git mv` в
  [`kb/industry-taxonomy/`](kb/industry-taxonomy/) и
  [`kb/mango-taxonomy/`](kb/mango-taxonomy/), чтобы явно отделить
  machine-readable taxonomy registries от остальных KB-материалов.
- Обновлены ссылки в README, стандартах, ADR, аудитах, валидаторах, workflow и
  экспериментах; `kb/mango-product-docs/` оставлен без переименования как
  отдельный product-docs namespace.
- Добавлена регрессионная проверка
  [`scripts/validate_issue_172_taxonomy_path_refactor.py`](scripts/validate_issue_172_taxonomy_path_refactor.py),
  которая проверяет наличие новых каталогов, отсутствие retired exact-path
  references и подключение проверки к `make kb-validate`/KB workflow.
### Added — Issue #174 тест на сходимость классификации (Industry Taxonomy)

- Проведён тест на сходимость (inter-rater reliability) классификации 25
  атомарных функций по [`standards/industry-taxonomy-standard.md`](standards/industry-taxonomy-standard.md)
  и [`kb/industry-taxonomy/registry.json`](kb/industry-taxonomy/registry.json).
  Дизайн: два независимых классификатора — эталон из документированного
  `industry_ref` в [`kb/mango-taxonomy/registry.json`](kb/mango-taxonomy/registry.json)
  (построен в #168/#170) и изолированный AI-агент, видевший **только** стандарт и
  industry-реестр (без эталона и mango-реестра). Все 25 выданных агентом node-id —
  канонические.
- Добавлен отчёт
  [`docs/analysis/taxonomy-convergence-test.md`](docs/analysis/taxonomy-convergence-test.md):
  полная сходимость **68%** (17/25), по уровням — Domain **96%**, Capability **76%**,
  Feature **60%**, Function **25%**, function_type **84%**. 8 расхождений разобраны
  до первопричин: структурная избыточность узлов (5), пробелы покрытия (3),
  неоднозначность `function_type` (4); побочно выявлен 1 дефект эталонного mapping
  (#21). Поскольку **68% < 80%**, рекомендация — **не фиксировать v1.0**, сначала
  доработать стандарт (дедупликация capability/feature, новые узлы blacklist/
  call-transfer/conversation-tagging, уточнение §7.2) и повторить тест.
- Добавлены воспроизводимые артефакты теста в
  [`experiments/issue-174/`](experiments/issue-174/): вход слепой классификации,
  эталон, выход AI-агента, пофункциональное сравнение и скрипт подсчёта
  `score_convergence.py` (валидирует каноничность всех id). Стандарты и реестры
  **не изменялись** (ограничение постановки).

### Added — Issue #176 тест на сходимость маппинга Mango → Industry Taxonomy

- Проведён inter-rater-reliability тест: 27 репрезентативных сущностей Mango
  Taxonomy (все 5 уровней, 8 кластеров, 3 типа функций) слепо размаплены шестью
  независимыми AI-агентами по стандартам и `registry.json`, без доступа
  к эталону, затем сопоставлены с `maps_to.industry_alignment` из реестра.
- Добавлен отчёт
  [`docs/analysis/mango-taxonomy-convergence-test.md`](docs/analysis/mango-taxonomy-convergence-test.md):
  корректность по формуле ДоД (точный полный путь) **37 %**, префиксная **63 %**,
  Domain **81 %**, Capability **67 %**, резолвимость узлов **100 %** (ноль
  галлюцинаций), `alignment_type` **100 %**. Расхождения сгруппированы в 4
  воспроизводимые причины (дубли id-узлов Industry, отсутствие boundary-правил
  CPaaS/UC↔digital-channels, гранулярность capability, недомаппленная глубина
  реестра против §7.3).
- **Рекомендация:** НЕ фиксировать Mango Taxonomy v1.0 (37 % < 80 %); выполнить
  4 точечные доработки (R1–R4) и повторить тест. Стандарты и реестры этим тестом
  не изменялись (по ограничению issue).
- Добавлены воспроизводимые артефакты в
  [`experiments/issue-176-convergence/`](experiments/issue-176-convergence/):
  `gold.json`, `blind-inputs.json`, `chunk-A..F.json`, `ai-predictions.json`,
  `score.py` (stdlib-only) и `scored.json`.

### Added — Issue #168 дозаполнение реестра Industry Taxonomy

- Дозаполнен machine-readable реестр
  [`kb/industry-taxonomy/registry.json`](kb/industry-taxonomy/registry.json)
  (version `1.0.0` → `1.1.0`, additive MINOR по §10.4): добавлены 8 capabilities
  (`ai-automation/conversation-summaries`, `analytics/real-time-reporting`,
  `contact-center/interaction-routing`, `contact-center/supervisor-workspace`,
  `digital-channels/team-messaging`, `hardware/device-management`,
  `security/access-control`, `voice-ucaas/call-routing`), 9 features и 13
  functions, завершающие каскад `Domain → Capability → Feature → Function` для
  каждого узла. Каждая сущность несёт явный `parent`, `evidence_refs`,
  `lifecycle_status` и (для functions) `function_type` + `parameters`.
- Смоделированы два alias на существующие canonical nodes вместо дубликатов
  (§10.2): `communications-apis` → [`platform/cpaas`](kb/industry-taxonomy/registry.json),
  `webhook-management` → `platform/open-api/webhooks`. После дозаполнения все 316
  внешних `industry_ref` из [`kb/mango-taxonomy/`](kb/mango-taxonomy/README.md) резолвятся по
  parent-chain (было 98 неразрешённых).
- Добавлен аналитический change request
  [`docs/analysis/industry-inventory.md`](docs/analysis/industry-inventory.md) с
  industry-landscape research и per-entity обоснованием каждой добавленной
  сущности (Task 0).
- Добавлена registry-backed регрессионная проверка
  [`scripts/validate_issue_168_industry_reference_integrity.py`](scripts/validate_issue_168_industry_reference_integrity.py),
  подключённая к `make kb-validate` и KB workflow: она резолвит каждый
  `industry_ref` из
  [`kb/mango-taxonomy/registry.json`](kb/mango-taxonomy/registry.json)
  против реестра (alias-aware, §4.5) и
  проверяет §11.2-подмножество (parent-chain, `alignment_type`, channel-facet
  enums, slug pattern, free-text-key rejection, evidence resolution, lifecycle
  severity). Неразрешённая ссылка — ошибка, кроме случая документированного
  `mapping_gap` (§8.4), который понижается до warning. JSON Schema реестра
  изменений не потребовала.

### Changed — Issue #170 единый JSON-реестр Mango Taxonomy

- Три YAML-файла Mango-реестра (`official-products.yaml`,
  `internal-registry.yaml` и crosswalk `product-mapping.yaml`) свёрнуты в единый
  JSON-документ
  [`kb/mango-taxonomy/registry.json`](kb/mango-taxonomy/registry.json) по §8.1
  стандарта: корень — единственный ключ `taxonomy` с `version` (SemVer) и пятью
  плоскими массивами `official_products` / `products` / `internal_services` /
  `modules` / `functions`. Дублирующий crosswalk-файл удалён — каждая сущность
  уже несёт `maps_to.industry_alignment`, поэтому отдельный mapping больше не
  нужен и не может рассинхронизироваться с реестром.
- Добавлена JSON Schema
  [`kb/mango-taxonomy/registry.schema.json`](kb/mango-taxonomy/registry.schema.json)
  (draft 2020-12), зеркалящая контракт §8.1 `MangoTaxonomyDocument`: закрытые
  `additionalProperties` / `unevaluatedProperties`, lifecycle без `removed`,
  восемь кластеров, `function_type`, `interaction_surface`, channel-facet и
  `mapping_gap`.
- Восстановлена ссылочная целостность с Industry Taxonomy: все `industry_ref`
  (18 ранее битых уникальных цепочек в 49 alignment'ах) перевыровнены так, чтобы
  резолвиться против живого
  [`kb/industry-taxonomy/registry.json`](kb/industry-taxonomy/registry.json);
  недостающие отраслевые узлы зафиксированы через `mapping_gap`, а не выдуманы.
- Добавлена регрессионная проверка
  [`scripts/validate_issue_170_mango_registry.py`](scripts/validate_issue_170_mango_registry.py)
  (stdlib-only): валидирует JSON Schema, 30 правил §11.2, резолвинг каждого
  `industry_ref` и `evidence_refs`, согласованность ссылок родитель/ребёнок в обе
  стороны и floors полноты иерархии. Подключена к `make kb-validate` и KB
  workflow; ретирована
  `scripts/validate_issue_160_mango_registry.py` (использовала замороженный
  hardcoded-срез Industry-таксономии и потому не видела битые `industry_ref`).
- Обновлён [`kb/mango-taxonomy/README.md`](kb/mango-taxonomy/README.md) под единый JSON-реестр и
  новый валидатор.
- Дозаполнена иерархия `Продукт → Сервис → Модуль → Функция` сверху вниз из
  реальной документации в
  [`kb/mango-product-docs/processed/`](kb/mango-product-docs/processed/):
  реестр вырос с 32 модулей / 64 функций до **61 модуля / 160 функций**
  (+29 модулей и +96 функций по всем восьми кластерам), каждая новая сущность
  привязана к проверенной секции через `evidence_refs`. Состав 10 официальных
  продуктов, 8 внутренних продуктов и 32 сервисов сохранён без изменений; ни
  одна сущность из старых YAML не удалена. Аддитивный билдер —
  [`experiments/cascade_fill.py`](experiments/cascade_fill.py) (идемпотентен:
  повторный запуск на уже заполненном реестре — no-op).
- Добавлен аналитический документ
  [`docs/analysis/issue-170-mango-inventory.md`](docs/analysis/issue-170-mango-inventory.md)
  с полным деревом `Продукт → Сервис → Модуль → Функция`, сравнением со старой
  YAML-структурой, разбивкой дозаполнения по кластерам и фиксацией пробелов
  (качество извлечения `sip-trunk`, 14 сервисов с одним модулем, недоиспользованные
  крупные корпуса, сущности со слабым evidence). Документ генерируется из живого
  реестра скриптом
  [`experiments/gen_inventory_doc.py`](experiments/gen_inventory_doc.py).

### Changed — Issue #166 синхронизация ADR-011/ADR-012

- Синхронизированы решения
  [`standards/decisions/ADR-011-industry-taxonomy.md`](standards/decisions/ADR-011-industry-taxonomy.md)
  и
  [`standards/decisions/ADR-012-mango-taxonomy.md`](standards/decisions/ADR-012-mango-taxonomy.md):
  оба ADR теперь симметрично фиксируют единый приоритет источников
  «ADR-011 имеет приоритет над ADR-012», согласованный с §1.3 обоих стандартов,
  и ссылаются на canonical registry
  [`kb/industry-taxonomy/registry.json`](kb/industry-taxonomy/registry.json).
- Унифицированы имена полей в machine-readable примерах ADR-012: черновые
  `layer` / `public_urls` / `internal_services` / `kb_refs` / `evidence_level`
  заменены на canonical `level` / `official_urls` / `supported_by_services` /
  `evidence_refs`, а industry-выравнивание обёрнуто в
  `maps_to.industry_alignment[]`.
- Устранён cross-standard drift slug'ов и `alignment_type`: пример
  `select-wallboard-widget` выровнен на canonical chain
  `contact-center/supervisor-assist/live-monitoring/manage-live-monitoring`
  (`primary`) с supporting `analytics/product-analytics/demand-analysis`, а
  webhook-пример использует canonical `platform/open-api/webhooks/webhook-subscription`.
  Исправлен невалидный пример chain в ADR-011 на
  `contact-center/omnichannel-contact-center/omnichannel-desktop/unified-agent-desktop`.
- Добавлена регрессионная проверка
  [`scripts/validate_issue_166_adr_sync.py`](scripts/validate_issue_166_adr_sync.py),
  подключённая к `make kb-validate` и KB workflow: она проверяет симметрию
  приоритета, canonical имена полей и резолвинг всех `industry_ref` примеров
  обоих ADR против Industry registry.

### Changed — Issue #164 исправления аудита Mango Taxonomy Standard

- Обновлён
  [`standards/mango-taxonomy-standard.md`](standards/mango-taxonomy-standard.md)
  по независимому аудиту: зафиксирован приоритет ADR-011 над ADR-012 для
  `industry_ref`, добавлена граница Mango vs Industry, canonical registry
  [`kb/industry-taxonomy/registry.json`](kb/industry-taxonomy/registry.json),
  `confidence`, `secondary_clusters`, `module_extraction_status`,
  `supported_by_services[]`, SemVer `taxonomy.version`, закрытые facets
  `security_compliance` / `geography_region` и текущие registry-resolving
  mapping examples.
- Уточнён validator contract: текущие проверки issue #154/#160 отделены от
  not yet implemented generic mapping-file validation, а отсутствие evidence в
  draft registry теперь считается ошибкой.
- Расширена регрессионная проверка
  [`scripts/validate_issue_154_mango_taxonomy_standard.py`](scripts/validate_issue_154_mango_taxonomy_standard.py),
  чтобы фиксировать issue #164 audit regressions и проверять примеры
  `industry_ref` against Industry registry.

### Changed — Issue #162 исправления аудита Industry Taxonomy Standard

- Обновлён
  [`standards/industry-taxonomy-standard.md`](standards/industry-taxonomy-standard.md)
  по находкам аудита: стандарт теперь явно ссылается на canonical registry
  [`kb/industry-taxonomy/registry.json`](kb/industry-taxonomy/registry.json)
  и schema
  [`kb/industry-taxonomy/registry.schema.json`](kb/industry-taxonomy/registry.schema.json),
  фиксирует boundary Industry vs Mango, статус `platform` как
  `cross_domain_layers`, canonical facet names `security_compliance` /
  `geography_region`, словарь `interaction_surface`, правило
  `direction x synchronicity`, JSON Schema contract для `industry_ref` и
  обязательное использование `mapping_gap` для неканонических source terms.
- Уточнён validator contract: текущие проверки issue #152/#156 отделены от
  not yet implemented generic mapping-file validation, чтобы зелёный CI не
  трактовался как полная проверка всех mapping artifacts.
- Расширена регрессионная проверка
  [`scripts/validate_issue_152_industry_taxonomy_standard.py`](scripts/validate_issue_152_industry_taxonomy_standard.py),
  чтобы фиксировать audit-regression tokens для Industry Taxonomy Standard.

### Added — Issue #160 Mango Taxonomy Registry

- Добавлен machine-readable namespace [`kb/mango-taxonomy/`](kb/mango-taxonomy/README.md) с
  реестром Mango Taxonomy: Official Layer
  [`kb/mango-taxonomy/official-products.yaml`](kb/mango-taxonomy/official-products.yaml),
  Internal Layer
  [`kb/mango-taxonomy/internal-registry.yaml`](kb/mango-taxonomy/internal-registry.yaml) и
  crosswalk
  [`kb/mango-taxonomy/product-mapping.yaml`](kb/mango-taxonomy/product-mapping.yaml) к Industry
  Taxonomy.
- Реестр покрывает публичные продукты Mango Office, 8 внутренних кластеров,
  иерархию `Product -> Service -> Module -> Function`, evidence refs из
  `kb/mango-product-docs/processed/`, `function_type`, `interaction_surface`,
  `maps_to.industry_alignment` и явные `mapping_gap` для отсутствующих
  отраслевых Feature/Function.
- Добавлена документация [`kb/mango-taxonomy/README.md`](kb/mango-taxonomy/README.md), helper
  [`experiments/issue-160-generate-mango-registry.py`](experiments/issue-160-generate-mango-registry.py)
  и регрессионная проверка
  [`scripts/validate_issue_160_mango_registry.py`](scripts/validate_issue_160_mango_registry.py),
  подключённая к `make kb-validate` и KB workflow.

### Added — Issue #158 независимый аудит стандартов таксономии

- Добавлен независимый аудиторский отчёт
  [`docs/audit/taxonomy-standards-independent-review.md`](docs/audit/taxonomy-standards-independent-review.md):
  команда из пяти экспертных ролей (системный архитектор, бизнес-аналитик,
  инженер знаний, эксперт по AI-governance, доменный эксперт) провела
  независимый сквозной аудит [`standards/industry-taxonomy-standard.md`](standards/industry-taxonomy-standard.md),
  [`standards/mango-taxonomy-standard.md`](standards/mango-taxonomy-standard.md)
  и связанных ADR-011/ADR-012 по шести направлениям (внутренняя
  согласованность, межстандартная согласованность, соответствие ADR,
  машиночитаемость, готовность к использованию, качество контракта).
  Зафиксировано 68 находок (9 критических), выполнена независимая
  кросс-проверка с выводами команды Q (приняты 5 дополнительных схемных
  находок), вынесен вердикт **NEEDS REVISION** с явными условиями перевода в
  v1.0. Аудитируемые стандарты и ADR этим отчётом не изменялись.

### Added — Issue #154 стандарт Mango Taxonomy

- ADR-012 переведён в `status: canonical`, `version: 1.0` и связан с
  [`standards/mango-taxonomy-standard.md`](standards/mango-taxonomy-standard.md),
  ADR-011 canonical v1.0, Industry Taxonomy Standard и решением по
  `voice-channel` / facet `channel`.
- Добавлен machine-readable стандарт
  [`standards/mango-taxonomy-standard.md`](standards/mango-taxonomy-standard.md):
  двухслойная архитектура Official Layer + Internal Layer, иерархия
  `Product -> Service -> Module -> Function`, 8 внутренних кластеров,
  атрибуты по уровням, `function_type`, нормализация Component -> Module и
  Operation -> Function, `maps_to.industry_alignment`, JSON Schema, YAML
  contract, граничные кейсы, validator contract, AI-agent contract и процесс
  эволюции.
- Добавлена регрессионная проверка
  [`scripts/validate_issue_154_mango_taxonomy_standard.py`](scripts/validate_issue_154_mango_taxonomy_standard.py),
  подключённая к `make kb-validate` и KB workflow.

### Added — Issue #156 реестр Industry Taxonomy

- Добавлен machine-readable реестр
  [`kb/industry-taxonomy/registry.json`](kb/industry-taxonomy/registry.json):
  зафиксированы семь canonical domains ADR-011, cross-domain layer `platform`,
  capabilities/features/functions, lifecycle статусы, `function_type`,
  `evidence_refs` и cross-cutting facets включая `channel`.
- Добавлены локальная schema
  [`kb/industry-taxonomy/registry.schema.json`](kb/industry-taxonomy/registry.schema.json)
  и README
  [`kb/industry-taxonomy/README.md`](kb/industry-taxonomy/README.md) для namespace `kb/industry-taxonomy/`;
  продуктовые Mango mappings в реестр не включались.
- Добавлена регрессионная проверка
  [`scripts/validate_issue_156_industry_taxonomy_registry.py`](scripts/validate_issue_156_industry_taxonomy_registry.py),
  подключённая к `make kb-validate` и KB workflow.
- Обновлена проверка Issue #144, чтобы root KB README описывал рабочий
  `kb/industry-taxonomy/` namespace после добавления Industry Taxonomy registry.

### Added — Issue #152 стандарт Industry Taxonomy

- Добавлен формальный стандарт
  [`standards/industry-taxonomy-standard.md`](standards/industry-taxonomy-standard.md):
  зафиксированы строгие правила применения модели
  `Domain -> Capability -> Feature -> Function`, canonical slugs, lifecycle
  статусы, `function_type`, cross-cutting facets включая `channel`, правила
  маппинга через `industry_ref`, граничные кейсы, процесс эволюции и контракт
  для будущего валидатора.
- Добавлена регрессионная проверка
  [`scripts/validate_issue_152_industry_taxonomy_standard.py`](scripts/validate_issue_152_industry_taxonomy_standard.py),
  подключённая к `make kb-validate` и KB workflow.

### Changed — Issue #150 доисследование асимметрии голосовых и текстовых каналов

- ADR-011 переведён в `status: canonical`, `version: 1.0` после закрытия
  доисследования асимметрии каналов: добавлены секция-решение «Голосовой канал vs
  текстовые каналы», cross-cutting facet `channel`
  (`channel_kind`/`synchronicity`/`direction`), first-class capability
  `voice-channel` внутри `voice-ucaas` и пример маппинга голосового канала.
- Принято решение «уточнённая (обоснованная) асимметрия»: домены не делятся
  (число доменов не меняется), инфраструктурная асимметрия `voice-ucaas`
  обоснована фактами, канальный артефакт устранён через `voice-channel` + facet.
- Добавлена сравнительная аналитика
  [`docs/analysis/voice-digital-channels-comparison.md`](docs/analysis/voice-digital-channels-comparison.md):
  трёхслойная рамка (infrastructure/channel/orchestration), отраслевые
  свидетельства (Twilio, МТС Exolve, RingCentral, Cisco, Amazon Connect, Genesys,
  TM Forum), trade-offs симметрии vs практичности и влияние на маппинг Mango.

### Changed — Issue #148 доработка taxonomy ADR

- Обновлены ADR-011 и ADR-012: добавлены правила strict mapping на Industry
  Taxonomy, `function_type` для Function (`business`, `configuration`,
  `ui-action`), алиасы Component=Module и Operation=Function, а также YAML/JSON
  формат `industry_ref` без свободных taxonomy tags.
- Аудит
  [`docs/audit/issue-146-mango-taxonomy-validation.md`](docs/audit/issue-146-mango-taxonomy-validation.md)
  переведён в `canonical` и связан с issue #148.
- Добавлена регрессионная проверка
  [`scripts/validate_issue_148_taxonomy_extensions.py`](scripts/validate_issue_148_taxonomy_extensions.py),
  подключённая к `make kb-validate` и KB workflow.

### Changed — Issue #146 validation Mango Taxonomy on real processed docs

- Валидирована Mango Taxonomy на 12 processed guides из
  [`kb/mango-product-docs/processed/`](kb/mango-product-docs/processed/):
  Contact Center, LK/VATS, Mango Talker, Bitrix24, SIP Trunk, API, Dialogi API,
  speech analytics, quality management и Wallboard.
- Унифицирован leaf-level термин `Atomic Function → Function`: ADR-011 теперь
  использует `Domain -> Capability -> Feature -> Function`, а ADR-012 —
  `Product -> Service -> Module -> Function`.
- Добавлен аудит evidence
  [`docs/audit/issue-146-mango-taxonomy-validation.md`](docs/audit/issue-146-mango-taxonomy-validation.md)
  и регрессионная проверка
  [`scripts/validate_issue_146_mango_taxonomy.py`](scripts/validate_issue_146_mango_taxonomy.py),
  подключённая к `make kb-validate` и KB workflow.

### Added — Issue #142 ADR по Mango Taxonomy

- Добавлен proposed ADR
  [`standards/decisions/ADR-012-mango-taxonomy.md`](standards/decisions/ADR-012-mango-taxonomy.md):
  выбрана двухслойная Mango Taxonomy с Official Layer и Internal Layer,
  иерархией `Product -> Service -> Module`, many-to-many связями с processed
  KB и явным выравниванием на ADR-011 Industry Taxonomy; сам стандарт,
  KB-реестр, research-копия и дополнительные артефакты не создавались.
### Fixed — Issue #144 целостность структуры `kb/` после миграции product docs

- Обновлён [`kb/README.md`](kb/README.md): описаны `kb/mango-product-docs/`,
  `kb/fragments/`, `kb/practices/` и taxonomy namespaces
  `kb/industry-taxonomy/`, `kb/mango-taxonomy/`.
- Добавлены README для продуктовой БЗ и ручных практик:
  [`kb/mango-product-docs/README.md`](kb/mango-product-docs/README.md) и
  [`kb/practices/README.md`](kb/practices/README.md).
- Зафиксирован аудит истории
  [`docs/audit/issue-144-kb-structure.md`](docs/audit/issue-144-kb-structure.md):
  `fragments/` и `practices/` оставлены в `kb/` как независимые материалы, без
  переносов.
- Добавлена регрессионная проверка
  [`scripts/validate_issue_144_kb_structure_readmes.py`](scripts/validate_issue_144_kb_structure_readmes.py),
  подключённая к `make kb-validate` и KB workflow.

### Added — Issue #139 ADR по Industry Taxonomy

- Добавлен proposed ADR
  [`standards/decisions/ADR-011-industry-taxonomy.md`](standards/decisions/ADR-011-industry-taxonomy.md):
  выбран hybrid reference taxonomy на базе Hub classification и сверки с Cisco,
  MTS Exolve, Twilio, RingCentral, Amazon Connect, Genesys, Microsoft Teams и
  8x8; сам стандарт, Mango Taxonomy, KB-данные и `research/` не создавались.

### Changed — Issue #137 миграция product docs в `kb/mango-product-docs/`

- Product documentation KB перенесена из прежних корневых product-docs
  каталогов источников/результатов и guide-файлов в нейтральный namespace
  [`kb/mango-product-docs/`](kb/mango-product-docs/).
- Makefile, KB workflow, scripts, validators, документация и generated trace
  metadata переведены на новые стабильные пути.
- Добавлена регрессионная проверка
  [`scripts/validate_issue_137_kb_product_docs_migration.py`](scripts/validate_issue_137_kb_product_docs_migration.py),
  которая фиксирует новую раскладку и запрещает возврат старых path literals.

### Added — Issue #134 стандарт README для репозитория

- Добавлен стандарт
  [`standards/readme-standard.md`](standards/readme-standard.md): четыре канона
  README, обязательная структура, запреты на смешивание с журналами/контрактами/
  реестрами, разделение ответственности и примеры хорошего/плохого README.
- Добавлен шаблон
  [`templates/readme-template.md`](templates/readme-template.md) для быстрого
  создания новых README по стандарту.
- Добавлена регрессионная проверка
  [`scripts/validate_issue_134_readme_standard.py`](scripts/validate_issue_134_readme_standard.py),
  подключённая к GitHub Pages workflow.

### Fixed — Issue #131 KB pipeline: новые источники должны попадать в `kb/mango-product-docs/processed`

- Добавлена короткая инструкция [`kb/mango-product-docs/UPLOAD-GUIDE.md`](kb/mango-product-docs/UPLOAD-GUIDE.md):
  загрузка нового документа, обновление существующего, сценарии `single`,
  `multi_part`, `multi_document`, запуск pipeline и проверка результата.
- Добавлена регрессионная проверка
  [`scripts/validate_issue_131_kb_processed_outputs.py`](scripts/validate_issue_131_kb_processed_outputs.py):
  фиксирует, что все processable `kb/mango-product-docs/sources/*/meta.json` имеют
  закоммиченные `kb/mango-product-docs/processed`-деливераблы с трассировкой и реальными LFS PDF
  payloads.
- Workflow KB pipeline теперь на push в `main` с изменениями источников или
  конвейера запускает `process_sources.py --all`, валидирует результат и
  коммитит `kb/mango-product-docs/processed` обратно в ветку; PR по-прежнему проверяет, что
  результат уже включён в diff.
- Новые источники из `kb/mango-product-docs/sources/` регенерируются в соответствующие каталоги
  `kb/mango-product-docs/processed/` через manifest-driven runner.

### Added — Issue #127 синхронизация БА-онтологии с Hub RFC C1/C2/C3

- В [`standards/ba-ontology.md`](standards/ba-ontology.md) и executable-слое
  добавлена ортогональная ось `requirement_level` для C1: `business`, `user`,
  `functional`, `non-functional`, без замены классификации
  Domain→Capability→Feature→Atomic Function.
- В реестр артефактов добавлен `business-rule` для C2 с категориями Wiegers:
  Facts, Constraints, Operation activators, Inferences, Computations.
- Создан crosswalk C3
  [`docs/requirements-engineering-crosswalk.md`](docs/requirements-engineering-crosswalk.md):
  процессы Вигерса ↔ операции mango ↔ подпроцессы BCREQ.
- ADR-003, ADR-004, [`docs/taxonomy.md`](docs/taxonomy.md),
  [`README.md`](README.md) и [`docs/hub-research-dependencies.md`](docs/hub-research-dependencies.md)
  синхронизированы с Hub RFC
  `requirements-engineering-ai-era-2026.md` и
  `ai-classifications-formalization-2026-06.md`.
- Добавлена регрессионная проверка
  [`scripts/validate_issue_127_hub_rfc_sync.py`](scripts/validate_issue_127_hub_rfc_sync.py),
  подключённая к GitHub Pages workflow.

### Added — Issue #125 cascading context loading

- Добавлен стандарт
  [`standards/cascading-context-loading-standard.md`](standards/cascading-context-loading-standard.md):
  naming `.executable.md`, LLM Loading Contract, deterministic escalation
  triggers и правила замера экономии токенов.
- Для критичных full-файлов созданы executable-companions:
  [`AI_SESSION_HANDOVER_PROMPT.executable.md`](AI_SESSION_HANDOVER_PROMPT.executable.md),
  [`governance/agent-onboarding-protocol.executable.md`](governance/agent-onboarding-protocol.executable.md),
  [`prompts/README.executable.md`](prompts/README.executable.md),
  [`docs/ba-processes/00-index.executable.md`](docs/ba-processes/00-index.executable.md)
  и [`standards/ba-ontology.executable.md`](standards/ba-ontology.executable.md).
- В full-файлы добавлен `LLM Loading Contract`, а prompt
  [`prompts/session-debug-documentation-oneshot.md`](prompts/session-debug-documentation-oneshot.md)
  теперь ссылается на executable-слой `prompts/README`.
- Добавлена регрессионная проверка
  [`scripts/validate_issue_125_cascading_context.py`](scripts/validate_issue_125_cascading_context.py),
  подключённая к GitHub Pages workflow.

### Added — Issue #123 единый каталог `runs/`

- Добавлен единый каталог результатов выполнения процессов `runs/YYYY/RUN-XXXX/`
  с обязательными `metadata.yaml`, `inputs/`, `outputs/`, `feedback/` и `logs/`.
- Существующие результаты из `prompts/experiments/`,
  `docs/ba-process/multichannel-agent-workload/` и
  `governance/analysis-bcreq-1025-2026-06-17.md` перенесены в `runs/2026/`
  с сохранением истории через `git mv`.
- Добавлены [`runs/README.md`](runs/README.md),
  [`standards/runs-contract-standard.md`](standards/runs-contract-standard.md)
  и регрессионная проверка
  [`scripts/validate_issue_123_runs_contract.py`](scripts/validate_issue_123_runs_contract.py),
  подключённая к GitHub Pages workflow.
- GitHub Pages checks теперь собирают evidence из `runs/`, а не из бывшего
  каталога `prompts/experiments/`.

### Added — Issue #121 KB pipeline: multi-file сценарии и обновление документов

- Добавлен manifest-driven runner
  [`scripts/kb/process_sources.py`](scripts/kb/process_sources.py): читает
  `kb/mango-product-docs/sources/<slug>/meta.json`, различает `single`, `multi_part` и
  `multi_document`, строит extraction jobs и защищает локальный запуск от LFS
  pointer-файлов вместо PDF bytes.
- В `meta.json` источников КЦ, ЛК и Mango Talker добавлены явные
  `processing_mode`, `output_slug`, `doc_code` и/или `source_files`; для Mango
  Talker выбран гибридный режим: общий product collection `kb/mango-product-docs/processed/mtalker/`
  и отдельные вложенные БЗ для каждого независимого руководства.
- Добавлены Make targets `kb-source-plan`, `kb-source-extract`, `kb-mtalker` и
  workflow input `source_dir`, чтобы ручной KB pipeline мог запускаться по
  source manifest, а не только по raw списку PDF-путей.
- Добавлена stdlib-проверка
  [`scripts/validate_issue_121_kb_multi_file.py`](scripts/validate_issue_121_kb_multi_file.py):
  фиксирует реальные манифесты, synthetic сценарии `single`, `multi_part`,
  `multi_document`, обновления 1→N, N→1, добавление и удаление документов.
- Обновлена инструкция [`kb/mango-product-docs/sources/README.md`](kb/mango-product-docs/sources/README.md): примеры
  `meta.json`, сценарии 1–6, правила обновления и troubleshooting для Git LFS.

### Fixed — Issue #119 KB pipeline: multi-part PDF и Git LFS

- Workflow KB pipeline обновлён для LFS-aware checkout (`lfs: true`) и текущих
  major-версий `actions/checkout`, `actions/setup-python` и `actions/upload-artifact`.
- `make kb-mango`, workflow defaults и регрессионная проверка
  `validate_issue_115_kb_mango_pipeline.py` переведены с удалённого
  `CC_manual_1.26.23_compressed.pdf` на 6 PDF-частей руководства КЦ.
- БЗ `kb/mango-product-docs/processed/mango-cc-manual/` регенерирована как multi-part документ со
  сквозной пагинацией и `source_refs` на конкретные LFS-части.
- Документация пополнения БЗ описывает обновление PDF через Git LFS, Codespace
  или локальный Git и обновление `meta.json` при замене одного файла частями.

### Fixed — Issue #117 KB pipeline: трассировка разделов и multi-part PDF

- `scripts/kb/extract.py` теперь принимает один или несколько PDF одного
  документа, обрабатывает split-руководства со сквозной пагинацией и сохраняет
  точную привязку каждого раздела к PDF-части и локальным страницам.
- В `meta.json` и frontmatter разделов добавлены `sources`, `source_pdfs`,
  `part_count`, `pdf_section`, `pdf_heading`, `source_part`, `source_pages` и
  `source_refs`; в каждом разделе выводится человекочитаемая строка
  `Трассировка`.
- Добавлена сформированная БЗ
  [`kb/mango-product-docs/processed/mango-lk-manual/`](kb/mango-product-docs/processed/mango-lk-manual/) для 5 частей
  руководства ЛК ВАТС v1.21: 568 сквозных страниц, 348 разделов, 1545
  изображений.
- Добавлен `make kb-lk` и регрессионная проверка
  [`scripts/validate_issue_117_kb_traceability.py`](scripts/validate_issue_117_kb_traceability.py),
  подключённая к workflow KB pipeline.

### Fixed — Issue #115 KB pipeline: реальное руководство не попадало в `kb/mango-product-docs/processed/`

- Диагностирован KB Pipeline #11: успешный `workflow_dispatch` запуск извлекал
  только синтетическую фикстуру `contact-center-manual-sample`, выгружал результат
  артефактом и не обрабатывал загруженный
  `kb/mango-product-docs/sources/mango-cc-manual/CC_manual_1.26.23_compressed.pdf`.
- Добавлена сформированная БЗ
  [`kb/mango-product-docs/processed/mango-cc-manual/`](kb/mango-product-docs/processed/mango-cc-manual/) для реального
  руководства v1.26.23: `index.md`, `meta.json`, `sections/`, `images/`.
- `Makefile` и workflow KB pipeline параметризованы (`SRC`, `OUT`, `doc_code`,
  `doc_title`, `doc_version`); ручной GitHub Actions запуск теперь по умолчанию
  обрабатывает `mango-cc-manual`, а не фикстуру.
- `extract.py` использует встроенное PDF outline/bookmarks, если оно есть, чтобы
  не превращать жирные нумерованные пункты списков в отдельные разделы.
- Добавлена регрессионная проверка
  [`scripts/validate_issue_115_kb_mango_pipeline.py`](scripts/validate_issue_115_kb_mango_pipeline.py):
  фиксирует наличие реальной БЗ, корректный источник, outline-нарезку и
  параметризованный workflow.

### Added — Issue #111 машиночитаемая БЗ из PDF: эксперимент + инфраструктура + методология (Creative)

- Построен сквозной конвейер **«источник → machine-readable БЗ»**
  [`scripts/kb/extract.py`](scripts/kb/extract.py) (pdfplumber + PyMuPDF +
  tiktoken): извлекает текст со структурой, картинки и таблицы, режет документ на
  разделы-чанки (`index.md` + `sections/NN-*.md` + `images/` + `meta.json`),
  считает токены. Нарезка — детерминированная (regex+кегли), **без LLM** по
  умолчанию (LLM — задокументированный fallback для неструктурированных текстов,
  **ФТ-3**). Вспомогательные скрипты: [`tokens.py`](scripts/kb/tokens.py),
  [`make_sample_pdf.py`](scripts/kb/make_sample_pdf.py) (фикстура, т.к. реальный
  `CC_manual_1.26.23.pdf` не загрузился в issue).
- Создана **нейтральная** структура БЗ [`kb/`](kb/README.md) (**не** `mango-kc`,
  **ФТ-4**) с **обязательным каталогом ручного ввода** [`kb/mango-product-docs/sources/`](kb/mango-product-docs/sources/README.md):
  `sources/` (вход человека) → `processed/` (генерируется) → `fragments/`
  (задел под RAG). Человекочитаемая инструкция пополнения (**ФТ-7**) —
  [`kb/mango-product-docs/sources/README.md`](kb/mango-product-docs/sources/README.md); источники-ссылки —
  [`kb/mango-product-docs/sources/web-links/`](kb/mango-product-docs/sources/web-links/README.md).
- Добавлены **5 конкретных примеров** обращения промпта к БЗ на реальных данных
  (индекс → выбор раздела → загрузка чанка → цитата `[CC, §4.2, с.5]` → сравнение
  токенов 1587 vs 378) — [`kb/mango-product-docs/USAGE.md`](kb/mango-product-docs/USAGE.md) (**ФТ-6**).
- Зафиксирован **отчёт по эксперименту** (**ФТ-8**)
  [`docs/kb-experiment-report.md`](docs/kb-experiment-report.md): описание PDF и
  оговорка о незагрузившемся файле, результаты и оценка качества извлечения
  (ловушка кириллицы), иерархия разделов, сравнение инструментов
  marker/nougat/MinerU **vs** pdfplumber с обоснованием выбора (**ФТ-2**,
  качество > токенов), скрипты-vs-LLM, предложение структуры, оценка
  автоматизации, устойчивость к драйфу ADR/промптов и явное указание, что БЗ —
  **эволюционный шаг к векторной БЗ и RAG**.
- Автоматизация (**ФТ-5**): [`Makefile`](Makefile) (`make kb-all` / `kb-sample` /
  `kb-extract` / `kb-validate` / `kb-tokens`) и GitHub-native workflow
  [`.github/workflows/kb.yml`](.github/workflows/kb.yml): лёгкая проверка на
  каждый PR/push (stdlib-only) + ручной (`workflow_dispatch`) прогон полного
  извлечения с выгрузкой артефакта.
- Добавлена локальная/CI-проверка
  [`scripts/validate_issue_111_kb_pipeline.py`](scripts/validate_issue_111_kb_pipeline.py)
  (stdlib-only): наличие деливераблов и нейтрального имени, согласованность
  `meta.json` ↔ разделы ↔ индекс ↔ токены ↔ картинки, наличие 5 примеров и
  обязательных пунктов отчёта.

### Added — Issue #109 dogfooding-эксперимент «Многоканальная нагрузка агента» (Creative + Structured)

- Добавлен полный прогон цепочки промптов на сыром требовании заказчика
  (одновременная работа агента с обращениями голос/чат/e-mail, лимит 3, приоритет) —
  каталог [`runs/2026/RUN-0011/`](runs/2026/RUN-0011/outputs/README.md)
  (**ФТ-1…ФТ-4**): вход ([`inputs/`](runs/2026/RUN-0011/inputs/)),
  обоснованная цепочка ([`prompts-chain.md`](runs/2026/RUN-0011/outputs/prompts-chain.md)),
  промежуточные результаты по шагам ([`steps/`](runs/2026/RUN-0011/outputs/steps/):
  глоссарий+As-Is, нормализация+5 Whys+gap, вопросы заказчику, US/UC, варианты
  доработки/Раздел 3) и [`final-artifact.md`](runs/2026/RUN-0011/outputs/final-artifact.md).
- Зафиксирована выжимка БЗ из 2 PDF-руководств (КЦ + ЛК ВАТС) с цитатами
  `[Документ, §Раздел, с.Страница]` и явными пометками «не найдено в документации»
  ([`inputs/kb-files.md`](runs/2026/RUN-0011/inputs/kb-files.md), по ADR-007).
- Добавлен лог эксперимента по [`standards/experiment-log-standard.md`](standards/experiment-log-standard.md)
  ([`experiment-log.md`](runs/2026/RUN-0011/logs/experiment-log.md), 6 метрик, verdict `works-with-edits`).
- Добавлен индекс каталога прогонов BA-процесса
  [`docs/ba-process/README.md`](docs/ba-process/README.md) (**ФТ-6**).
- Подготовлен RFC по улучшению промптов (**ФТ-5**, промпты **не изменены**):
  [`governance/rfc/prompt-improvement-multichannel-proposal.md`](governance/rfc/prompt-improvement-multichannel-proposal.md)
  (RFC-MCH-P1…P3); реестр [`governance/rfc-register.md`](governance/rfc-register.md)
  дополнен записями RFC-MCH-*. RFC-MCH-P1 — повтор паттернов Б1/Б5 из BCREQ-1025.

### Added — Issue #105 синхронизация контрактов с Хабом (Research + Structured)

- Добавлен аудит контрактов спока
  [`governance/audit-contracts-mango-2026-06-17.md`](governance/audit-contracts-mango-2026-06-17.md)
  (**ФТ-1**): ревизия ADR #003–#010, 12 стандартов и governance-/root-контрактов с
  классификацией (локальный / Smart Sync ← / сверить → RFC / передача знаний →).
- Добавлен аудит ключевых документов Хаба
  [`governance/audit-hub-2026-06-17.md`](governance/audit-hub-2026-06-17.md)
  (**ФТ-2**): RFC, стандарты и governance Хаба с **полными permalink-URL** на снимок
  `6ddffdf`, применимостью к Mango и пробелами.
- Добавлена матрица синхронизации
  [`governance/sync-matrix-2026-06-17.md`](governance/sync-matrix-2026-06-17.md)
  (**ФТ-3**): соответствие контрактов спок ↔ Хаб, реестр RFC-сверки и передачи знаний.
- Интегрирован RFC-процесс Хаба (**ФТ-4**):
  [`governance/rfc-process.md`](governance/rfc-process.md) **ссылается** на
  `knowledge-lifecycle-proposal.md` Хаба (не дублирует), отображает жизненный цикл
  знаний на артефакты спока; реестр [`governance/rfc-register.md`](governance/rfc-register.md)
  дополнен RFC-SYNC-* и RFC-HUB-*. Подготовлен RFC в Хаб о процессе отладки промптов
  [`governance/rfc-to-hub-002-prompt-debugging-process.md`](governance/rfc-to-hub-002-prompt-debugging-process.md).
- Подготовлена передача знаний в Хаб (**ФТ-5**):
  каталог [`governance/knowledge-transfer-to-hub/`](governance/knowledge-transfer-to-hub/)
  (онтология БА #003, таксономия операций #004, процесс BCREQ #009, UX Pages #010) и
  umbrella-RFC [`governance/rfc-to-hub-001-knowledge-transfer.md`](governance/rfc-to-hub-001-knowledge-transfer.md).
- Контракты спока в этом PR **не изменены**: расхождения с Хабом оформлены как RFC
  `proposed`, уникальные практики — как документы передачи знаний (правило «не менять
  сразу, а создать RFC»).

### Added — Issue #101 разбор эксперимента «Задача 1027» и стандарт фиксации экспериментов

- Добавлен анализ первой реальной сессии БА
  [`docs/analysis/experiment-1027-analysis.md`](docs/analysis/experiment-1027-analysis.md):
  вердикты по 4 гипотезам БА с цитатами из стенограммы, **предложения** правок
  промптов (P1–P5) как кандидаты в RFC и рекомендации по онтологии (без её
  изменения). Сами промпты в этом PR **не меняются** — правки выносятся через
  процесс отладки (см. ниже).
- Добавлен легковесный стандарт фиксации экспериментов (Draft v0.1)
  [`standards/experiment-log-standard.md`](standards/experiment-log-standard.md):
  два уровня фиксации (GitHub Issue / лёгкий Markdown) и ядро из 6 метрик.
- Добавлен первый прогон по стандарту (dogfood на сессии 1027)
  [`runs/2026/RUN-0007/outputs/fr-generation-1027-live_2026-06-16.md`](runs/2026/RUN-0007/outputs/fr-generation-1027-live_2026-06-16.md).
- Добавлен аудит контрактов
  [`governance/audit-contracts-2026-06-17.md`](governance/audit-contracts-2026-06-17.md):
  ревизия `AI_GOVERNANCE.md`, `CONTRIBUTING.md` и стандарта логирования,
  выявленные пробелы (нет процесса отладки/RFC/критериев приёмки правок промптов).
- Добавлен аудит исследования
  [`governance/audit-research-1027.md`](governance/audit-research-1027.md):
  проверка полноты разбора гипотез H1–H4, обоснованности рекомендаций O1–O3 и
  передачи онтологии (ADR #3–#8).
- Добавлен черновик процесса отладки промптов
  [`governance/prompt-debugging-process.md`](governance/prompt-debugging-process.md)
  и реестр RFC [`governance/rfc-register.md`](governance/rfc-register.md):
  порядок «эксперимент → RFC → согласование с пользователем → изменение».

### Added — Issue #97 формализация онтологии БА и стандартов (Creative + Research)

- Формализована онтология БА (артефакт ↔ процесс ↔ операция) и выпущен набор
  стандартов в виде ADR: [ADR-003](docs/adr/003-ba-ontology.md) (онтология),
  [ADR-004](docs/adr/004-operations-taxonomy.md) (таксономия 13 операций,
  `risk_analysis` сохранён), [ADR-005](docs/adr/005-artifact-team-naming.md)
  (нейминг артефактов/команд), [ADR-006](docs/adr/006-prompt-naming.md) (нейминг
  промптов, запрет перегрузки), [ADR-007](docs/adr/007-kb-standard.md) (KB до
  настоящего RAG), [ADR-008](docs/adr/008-industry-standards-standard.md)
  (отраслевые стандарты и best practices),
  [ADR-009](docs/adr/009-bcreq-formation-process.md) (многоуровневый процесс
  BCREQ, механизм незавершённых подпроцессов),
  [ADR-010](docs/adr/010-pages-ux.md) (UX GitHub Pages). Все ADR содержат
  обязательные разделы ФТ-9 (Title, Status, Context, Decision, Consequences,
  References, Examples).
- Добавлены «живые» контракты-стандарты с нормативным словарём RFC 2119 / BCP 14
  и блоком DoD: [`standards/ba-ontology.md`](standards/ba-ontology.md),
  [`standards/artifact-naming-standard.md`](standards/artifact-naming-standard.md),
  [`standards/team-directory.md`](standards/team-directory.md) (ровно две команды
  `BCREQ` и `CCMO` + механизм добавления),
  [`standards/kb-standard.md`](standards/kb-standard.md),
  [`standards/industry-standards-standard.md`](standards/industry-standards-standard.md),
  [`standards/bcreq-process-standard.md`](standards/bcreq-process-standard.md),
  [`standards/pages-ux-standard.md`](standards/pages-ux-standard.md).
- **ФТ-8 (GitHub Pages):** на странице «Процессы» SPA (рядом с карточками
  процессов из issue #99) добавлена секция «Процессы и подпроцессы с промптами».
  Генератор [`scripts/generate-pages-data.mjs`](scripts/generate-pages-data.mjs)
  строит полный список процессов/подпроцессов в
  [`site/data/process-tree.json`](site/data/process-tree.json) (с флагом
  `hasPrompts` и типом покрытия `kind`), а интерфейс
  ([`site/index.html`](site/index.html), [`site/app.js`](site/app.js),
  [`site/styles.css`](site/styles.css)) по жёсткому требованию выводит **только**
  процессы/подпроцессы с промптами. При > 20 показанных подпроцессах используется
  раскрывающееся дерево (`<details>`/`<summary>`). Прототип (скриншоты) — в
  [ADR-010](docs/adr/010-pages-ux.md).
- Доказательная база: эксперименты
  [`runs/2026/RUN-0009/outputs/standards-applied-ab-2026-06-16.md`](runs/2026/RUN-0009/outputs/standards-applied-ab-2026-06-16.md)
  и
  [`runs/2026/RUN-0008/outputs/kb-citation-check-2026-06-16.md`](runs/2026/RUN-0008/outputs/kb-citation-check-2026-06-16.md).
- Добавлена локальная проверка
  [`scripts/validate_issue_97_ontology_standards.py`](scripts/validate_issue_97_ontology_standards.py)
  (ADR-разделы ФТ-9, RFC 2119/DoD стандартов, инварианты `process-tree.json`,
  две команды, отсутствие выдуманных кодов, сохранность `risk_analysis`) и шаг в
  workflow [`.github/workflows/github-pages.yml`](.github/workflows/github-pages.yml).

### Fixed — Issue #103 корректировки UI каталога промптов

- **ФТ-1. Карточка промпта.** Убрана стрелка (↗) из верхней части карточки;
  нижняя стрелка заменена кнопкой «📁 Перейти в репо», ведущей на файл промпта
  в GitHub репозитории.
- **ФТ-2. Фильтр статуса удалён.** Блок «СТАТУС» убран из панели фильтров;
  удалены связанные обработчики и генерация токенов `status:*`.
- **ФТ-3. Визуальное разделение групп фильтров.** Каждая группа фильтров
  получила рамку, тонированный фон и жирные заголовки: процессы — голубой фон,
  операции — зелёный, режимы — фиолетовый (вариант D из предложений).
- **ФТ-4. Сортировка по убыванию даты.** Опция «По дате» отображается со
  стрелкой ↓, сортировка по умолчанию — последние обновлённые сверху.
- **ФТ-5. Тулбар.** Сортировка и кнопка экспорта перемещены выше поля поиска;
  кнопка экспорта получила явный текстовый ярлык «📥 Скачать».
- **ФТ-6. Кнопки очистки.** Добавлены кнопки «✕ Очистить поиск» и
  «↺ Сбросить фильтры» справа от строки поиска; видимы только при активных
  фильтрах или заполненном поиске.

### Added — Issue #99 оптимизация GitHub Pages (многостраничность и UX)

- **ФТ-1. Многостраничность.** Сайт [`site/index.html`](site/index.html) разбит на
  пять разделов с верхним меню: **Каталог** (главная, URL `/`), **Дашборд**,
  **Roadmap**, **Процессы**, **Паттерны**. Переключение реализовано клиентским
  hash-роутером в [`site/app.js`](site/app.js) (SPA), порядок секций сохранён.
- **ФТ-2. Оптимизация карточек.** Из карточки убраны путь к файлу и хэш рядом с
  «Копировать»; вместо хэша показаны версия (`v…`), дата обновления и статус
  тестов (`✅ N тест(ов)`); ID вынесен мелким шрифтом под названием; добавлена
  кнопка «Ссылка» (↗) — копирует deep-link `#prompt=<id>` на карточку; теги
  процессов получили эмодзи-иконки; описания расширены до 150-300 символов
  (генерируются динамически в [`scripts/generate-pages-data.mjs`](scripts/generate-pages-data.mjs)).
- **ФТ-3. Дашборд.** Блок «Проверки» показывает всего проверок, разбивку
  **по процессам БА** (динамически из frontmatter, с бакетом «Прочее»),
  обратную связь (`prompt:feedback`) и покрытие тестами (X/Y, %). Добавлен блок
  «Активность» — топ-5 промптов. Дублирование метрик убрано.
- **ФТ-4. UX.** Быстрый поиск с автодополнением (по названию/ID/описанию/тегам),
  сортировка (дата, популярность, алфавит, статус), фильтр по статусу
  (Draft/Canonical/Archived), карточка процесса по клику (описание, операции,
  связанные промпты, паттерны, known gaps), экспорт каталога в Markdown по
  текущим фильтрам и переключатель тёмной темы (сохраняется в `localStorage`).
- **ФТ-5. Генерация данных.** Генератор формирует дополнительно
  `site/data/processes.json` и `site/data/patterns.json`, расширенные
  `checks.json` (по процессам, покрытие тестами) и длинные описания промптов;
  процессы и эмодзи назначаются динамически — без хардкода типов артефактов.
- **ФТ-6.** Обновлены README и этот CHANGELOG.
- Добавлена локальная проверка
  [`scripts/validate_issue_99_pages_optimization.py`](scripts/validate_issue_99_pages_optimization.py)
  и шаг в workflow [`.github/workflows/github-pages.yml`](.github/workflows/github-pages.yml).

### Fixed — Issue #95 добавить ID промпта в копируемый текст

- Кнопка «Копировать» в карточке промпта теперь добавляет HTML-комментарий с ID
  в начало копируемого текста: формат `<!-- {prompt.id} -->\n\n{body}`.
- HTML-комментарий добавляется **только при копировании** — в отображаемой карточке
  он не появляется (изменения только в [`site/app.js`](site/app.js)).
- LLM игнорирует HTML-комментарий, при этом ID виден в истории чата и позволяет
  отследить, какой промпт был использован.
- Добавлена локальная проверка
  [`scripts/validate_issue_95_prompt_id_in_copy.py`](scripts/validate_issue_95_prompt_id_in_copy.py)
  и шаг в workflow [`.github/workflows/github-pages.yml`](.github/workflows/github-pages.yml).

### Changed — Issue #92 метаданные промптов (`id` + `title`), удаление EXPERIMENTAL

- В обязательный frontmatter всех 30 промптов (`prompts/` и `prompts/archive/`)
  добавлены поля `id` (уникальный токен `mango-[операция]-[режим]`) и `title`
  (человекочитаемое название на русском).
- Из всех 24 активных промптов удалён маркер
  `<!-- EXPERIMENTAL: DO NOT USE IN PRODUCTION -->`: экспериментальность уже
  отражает `status: draft`.
- Обновлён стандарт промптов: ADR-001
  [`docs/adr/001-prompt-standard.md`](docs/adr/001-prompt-standard.md) и контракт
  [`standards/prompt-standard.md`](standards/prompt-standard.md) теперь требуют
  6 обязательных полей frontmatter (добавлены `id` и `title`).
- Генератор [`scripts/generate-pages-data.mjs`](scripts/generate-pages-data.mjs)
  берёт `id`/`title` из frontmatter и формирует поле `body` — текст промпта без
  frontmatter и маркеров для чистого копирования.
- В интерфейсе GitHub Pages ([`site/app.js`](site/app.js),
  [`site/styles.css`](site/styles.css)) карточка промпта выводит `title` жирным
  заголовком и `id` мелкой меткой; кнопка «Копировать» копирует чистый текст без
  frontmatter.
- В матрицу [`prompts/README.md`](prompts/README.md) добавлены колонки
  «Название» (title) и «Токен» (id); парсер матрицы в генераторе переведён на
  поиск колонок по заголовку.
### Changed — Issue #91 улучшение GitHub Pages (порядок, фильтры, аналитика)

- Изменён порядок секций в [`site/index.html`](site/index.html): **Каталог →
  Дашборд → Проверки → Roadmap**. Каталог промптов теперь основной контент и
  виден сразу (ФТ-1).
- Переупорядочены фильтры каталога в [`site/app.js`](site/app.js): **Процессы БА
  → Операции → Режимы**. Внутри одного фильтра действует логика **ИЛИ**, между
  фильтрами — **И** (ФТ-2).
- Реализована умная каскадная фильтрация: при выборе процесса(ов) фильтр
  «Операции» сужается до операций выбранных процессов (недоступные операции
  подсвечиваются как неактивные), а фильтры «Процессы» и «Режимы» не
  сокращаются (ФТ-3).
- Добавлен модуль **«Проверки»** вместо карточки «Мультиагенты»: статус отладки
  (`draft` / `canonical` / `archived`), число зафиксированных тестов в
  [`prompts/experiments/`](prompts/experiments), обратная связь по лейблу
  `prompt:feedback` и активность использования промптов по процессам БА (ФТ-4).
- [`scripts/generate-pages-data.mjs`](scripts/generate-pages-data.mjs) генерирует
  новый артефакт [`site/data/checks.json`](site/data/checks.json) на основе
  тестовых логов и статического среза
  [`governance/prompt-feedback.json`](governance/prompt-feedback.json) (ФТ-6).
- Решение по `experiments/` vs `scripts/`: корневой `experiments/` отсутствует
  (Python-валидаторы уже консолидированы в `scripts/`), `prompts/experiments/`
  сохранён как каноничное место тестовых логов промптов. Назначение директорий
  задокументировано (ФТ-5).
- Добавлена локальная проверка
  [`scripts/validate_issue_91_pages_enhancements.py`](scripts/validate_issue_91_pages_enhancements.py)
  и шаг в workflow
  [`.github/workflows/github-pages.yml`](.github/workflows/github-pages.yml).

### Added — Issue #86 Mango Office Multichannel widget

- В GitHub Pages шаблон [`site/index.html`](site/index.html) добавлен виджет
  Mango Office Multichannel с `id: 23303`: чат поддержки и заказ обратного
  звонка загружаются перед закрывающим тегом `</body>`.
- Добавлена локальная проверка
  [`scripts/validate_issue_86_mango_widget.py`](scripts/validate_issue_86_mango_widget.py),
  закрепляющая наличие скрипта виджета, идентификатора `23303`, расположение
  перед `</body>` и запись в changelog.
- Workflow [`.github/workflows/github-pages.yml`](.github/workflows/github-pages.yml)
  теперь запускает проверку интеграции виджета вместе с проверкой артефакта
  GitHub Pages.
### Added — Issue #85 библиотека MVP-паттернов БА

- Созданы 7 MVP-паттернов в `patterns/`: `glossary-context-generation`,
  `fr-generation`, `fr-validation`, `user-story-generation`,
  `usecase-generation`, `asr-ingestion` и `meeting-summary-generation`. Каждый
  паттерн содержит 8 полей ADR-002, Product Layer, Commercial Layer, правила
  адаптации, LLM-агностичный `prompt_template`, quality gates, output schema,
  обезличенный пример и ссылки на существующие prompt-реализации.
- Обновлён [`patterns/README.md`](patterns/README.md): добавлены навигация по
  MVP-паттернам, матрица "паттерн ↔ процесс ↔ операция ↔ промпты", пример
  маршрута использования и полные URL связанных PR/репозиториев.
- В [`docs/ba-processes/00-index.md`](docs/ba-processes/00-index.md) заполнена
  колонка "Паттерн" для процессов, покрытых MVP-библиотекой, сохранив
  parser-compatible структуру центрального реестра.
- Добавлена локальная проверка
  [`scripts/validate_issue_85_patterns_library.py`](scripts/validate_issue_85_patterns_library.py)
  для воспроизведения требований issue #85: наличие 7 директорий, 8 секций,
  Product/Commercial Layer, примеров, ссылок на существующие prompts, навигации
  и центрального registry mapping.

### Added — Issue #83 карта процессов БА

- Развёрнут центральный индекс
  [`docs/ba-processes/00-index.md`](docs/ba-processes/00-index.md) в детальную
  карту 9 процессов БА с входами, выходами, workflow, cognitive operations,
  direct links на prompt-файлы и явными manual gaps.
- Добавлены рекомендации по режимам `stepwise` / `oneshot` / `legacy`, связь
  маршрутов с Product Layer и Commercial Layer, 3 сценария запуска процессов с
  Mermaid-диаграммами и полный traceability-блок по связанным PR/репозиториям.
- Добавлена локальная проверка
  [`scripts/validate_issue_83_ba_process_map.py`](scripts/validate_issue_83_ba_process_map.py)
  для воспроизведения требований issue #83: наличие 9 процессов, 13 операций,
  ссылок на 24 активных и 6 архивных prompts, known gaps и навигации.

### Added — Issue #78 промпт-суммаризатор сессий БА

- Создан промпт
  [`prompts/session-debug-documentation-oneshot.md`](prompts/session-debug-documentation-oneshot.md):
  one-shot суммаризация длинной сессии работы с LLM в структурированное резюме
  (контекст, ключевые решения с обоснованием, проблемы и обходные пути,
  применённые промпты, открытые вопросы, следующие шаги). Формат совместим с
  шаблоном блока суммарии в
  [`governance/session-digests.md`](governance/session-digests.md).
- Имя файла приведено к схеме ADR-001 `[домен]-[операция]-[режим].md`
  (`session-debug` / `documentation` / `oneshot`) вместо запрошенного в issue
  рабочего названия `session-debug-summarizer.md`, не соответствующего схеме.
- Промпт добавлен в матрицу
  [`prompts/README.md`](prompts/README.md) (новый раздел «Отладка и
  суммаризация сессий», счётчик активных промптов 23 → 24) и в маппинг процесса
  «Помощь ПО/ПМ»
  [`docs/ba-processes/00-index.md`](docs/ba-processes/00-index.md).
- Добавлен зафиксированный прогон
  [`runs/2026/RUN-0006/outputs/session-debug-summarizer-2026-06-13.md`](runs/2026/RUN-0006/outputs/session-debug-summarizer-2026-06-13.md),
  подтверждающий получение структурированного резюме за один запуск.
- Обновлены контрольные счётчики в
  [`scripts/validate_issue_74_github_pages.py`](scripts/validate_issue_74_github_pages.py)
  (24 активных промпта, 30 всего).

### Added — Issue #74 GitHub Pages interface

- Создан dependency-free GitHub Pages интерфейс в [`site/`](site/): дашборд
  фаз внедрения, каталог 23 активных промптов и 6 архивных файлов, OR-фильтры по
  когнитивным операциям / процессам БА / режимам, поиск и копирование prompt
  content в буфер.
- Добавлен генератор [`scripts/generate-pages-data.mjs`](scripts/generate-pages-data.mjs):
  он читает Markdown source of truth (`prompts/*.md`,
  [`prompts/README.md`](prompts/README.md),
  [`docs/taxonomy.md`](docs/taxonomy.md),
  [`docs/ba-processes/00-index.md`](docs/ba-processes/00-index.md),
  [`docs/ba-ecosystem.md`](docs/ba-ecosystem.md)) и формирует статические
  [`site/data/prompts.json`](site/data/prompts.json),
  [`site/data/stats.json`](site/data/stats.json),
  [`site/data/roadmap.json`](site/data/roadmap.json).
- Настроен workflow
  [`.github/workflows/github-pages.yml`](.github/workflows/github-pages.yml):
  при PR выполняется генерация и проверка, при push в `main` артефакт `site/`
  публикуется в ветку `gh-pages` через `GITHUB_TOKEN`, без PAT и без GitHub API
  в клиентском коде.
- Добавлена локальная проверка
  [`scripts/validate_issue_74_github_pages.py`](scripts/validate_issue_74_github_pages.py)
  для воспроизведения и валидации требований issue #74.
### Added — Issue #76 суммария синхронизации сессий Хаба

- structured: зафиксировать суммарию синхронизации сессий Хаба в
  [`governance/session-digests.md`](governance/session-digests.md): добавлены
  индексная запись `2026-06-14` и блок `#2026-06-14` для передачи контекста
  между Чатом Хаба и Чатом БА Манго.
- Локальная проверка [`scripts/validate_issue_72_hub_sync.py`](scripts/validate_issue_72_hub_sync.py)
  больше не требует пустой индекс `session-digests.md`, так как первая суммария
  теперь сохранена.

### Changed — Issue #72 Smart Sync последних обновлений Хаба

- [`AI_SESSION_HANDOVER_PROMPT.md`](AI_SESSION_HANDOVER_PROMPT.md) синхронизирован
  с Hub PR #226 (`templates/htom/AI_SESSION_HANDOVER_PROMPT.md`, SHA
  `f3e8b265b1577d0ee1fe173dbe16728cc3c7e31b`): добавлен механизм периодической
  суммаризации сессий через `governance/session-digests.md`, сохранены локальные
  правила issue #48/#61 про канал работы через Конарда и task template.
- [`governance/agent-onboarding-protocol.md`](governance/agent-onboarding-protocol.md)
  обновлён по source SHA `f3e8b265b1577d0ee1fe173dbe16728cc3c7e31b`: встроенный
  копируемый prompt теперь соответствует handover v0.5 и указывает на
  `governance/session-digests.md`.
- Созданы [`governance/session-digests.md`](governance/session-digests.md) как
  пустой локальный индекс суммарий для `mango_ba_prompts` и
  [`governance/artifact-map.md`](governance/artifact-map.md) как локальная карта
  активных артефактов, адаптированная из хабовой карты PR #224/#226.
- Обновлены [`README.md`](README.md), [`.hub-profile.json`](.hub-profile.json) и
  [`governance/migration-manifest.md`](governance/migration-manifest.md), чтобы
  зафиксировать Smart Sync snapshot, source SHA и терминологию
  Пользователь / Исполнитель.
- Добавлена локальная проверка
  [`scripts/validate_issue_72_hub_sync.py`](scripts/validate_issue_72_hub_sync.py)
  для воспроизведения и валидации требований issue #72.
- Досинхронизированы релевантные части Hub PR #229 и Hub PR #230, latest Hub SHA
  `b683341d22d4f518618917a02d9c7c394658b156`.
- Hub PR #229: Base Registry внешних источников
  `research/external-knowledge/external-sources-registry.md` оставлен
  reference-only в Хабе; для Mango в
  [`docs/hub-research-dependencies.md`](docs/hub-research-dependencies.md)
  зарегистрированы строки `ext-003` (Spec-Driven Development) и `ext-007`
  (Контекст-инжиниринг), без создания локального `research/`.
- Hub PR #230: терминология активных guidance-файлов выровнена на
  `Пользователь / Исполнитель` в [`AI_GOVERNANCE.md`](AI_GOVERNANCE.md),
  [`CONTRIBUTING.md`](CONTRIBUTING.md), [`README.md`](README.md),
  [`docs/task-for-konard-template.md`](docs/task-for-konard-template.md) и
  связанных ADR/исторических ссылках; traceability contracts, Framework vs
  Template и Scope Resolver-а задокументированы как Hub-governance контракты,
  не требующие локальных артефактов в `mango_ba_prompts`.

### Added — Issue #65 README для `prompts/`

- Создан [`prompts/README.md`](prompts/README.md): навигация по 23 активным
  промптам и 6 архивным legacy-файлам, матрица назначение ↔ режим ↔ статус ↔
  версия ↔ когнитивная операция ↔ процесс БА, описание структур Hub-style и
  Mango BA workflow, токенов `stepwise` / `oneshot` / `legacy`, процесса
  отладки и ссылок на таксономию, индекс процессов, стандарты и шаблон фидбека.

### Added — Issue #64 ADR на стандарт паттернов

- Создан [`docs/adr/002-pattern-standard.md`](docs/adr/002-pattern-standard.md):
  ADR фиксирует directory-first структуру `patterns/[operation-name]/README.md`,
  8 обязательных полей паттерна, связь с 13 когнитивными операциями и 9
  процессами БА, маппинг паттерн ↔ prompt только через
  [`docs/ba-processes/00-index.md`](docs/ba-processes/00-index.md),
  LLM-агностичность `prompt_template`, правила создания новых паттернов,
  критерии зрелости, semver-версионирование и совместимость с
  [`docs/adr/001-prompt-standard.md`](docs/adr/001-prompt-standard.md).
- [`patterns/README.md`](patterns/README.md) и
  [`standards/pattern-standard.md`](standards/pattern-standard.md) согласованы
  с ADR: README остаётся краткой справкой, стандарт — операционным контрактом
  для review.
- Добавлена локальная проверка
  [`scripts/validate_issue_64_pattern_adr.py`](scripts/validate_issue_64_pattern_adr.py)
  для воспроизведения и валидации требований issue #64.

### Added — Issue #66 экосистема работы БА с графами связей и картой процессов

- Создан [`docs/ba-ecosystem.md`](docs/ba-ecosystem.md) — единая карта
  экосистемы работы БА Mango: методология на основе research Хаба, Mermaid-граф
  связей, определения сущностей, классификации направлений разработки, стилей и
  пакетов документов, правила/практики, матрицы процесс ↔ операция ↔ промпт,
  направление ↔ стиль ↔ шаблон и артефакт ↔ стиль.
- В документ добавлена подробная карта 9 процессов БА: цель, входы, выходы,
  workflow по когнитивным операциям, рекомендуемые промпты и known gaps по
  каждому процессу. Зафиксированы 3 сценария запуска: клиентский заказ,
  внутренняя доработка продукта и тендерное ТЗ.
- Описана стратегия перехода от библиотеки промптов к системным промптам с
  БЗ/RAG, агентам и мультиагентному контуру, включая критерии перехода между
  уровнями и сохранение human gates.
- [`README.md`](README.md) и
  [`docs/ba-processes/00-index.md`](docs/ba-processes/00-index.md) дополнены
  навигацией на экосистемную карту; реестр
  [`docs/hub-research-dependencies.md`](docs/hub-research-dependencies.md)
  отмечает новый документ как consumer релевантных research-якорей Хаба.
- Удалён авто-сгенерированный корневой `.gitkeep`, созданный только для
  открытия draft PR.
### Added — Issue #63 ADR стандарта промптов

- Создан [`docs/adr/001-prompt-standard.md`](docs/adr/001-prompt-standard.md):
  ADR фиксирует две допустимые структуры промптов (Hub-style и Mango BA workflow),
  токены режимов `stepwise` / `oneshot` / `legacy` с обоснованием отказа от
  `expert` / `express`, 4 обязательных поля frontmatter, правила именования
  `[домен]-[операция]-[режим].md`, суффиксы `-legacy` / `-v2` / `-alt` и процессы
  `draft` -> `canonical` / архивации. Существующие промпты не изменялись.

### Changed — Issue #61 Creative-mode governance без архитектурного долга

- [`AI_GOVERNANCE.md`](AI_GOVERNANCE.md), [`AI_QUICK_RULES.md`](AI_QUICK_RULES.md)
  и [`CONTRIBUTING.md`](CONTRIBUTING.md) обновлены: `Structured` сохраняет
  fail-closed semantics, а `Creative` допускает обоснованный обход scope или
  локального правила, если обход нужен для цели задачи и явно описан в PR.
- Зафиксирована специфика работы с Конардом: **молчание = согласие** при merge
  без комментариев; комментарий + ручной перезапуск задачи = итерация в той же
  ветке PR; close PR = отказ от решения.
- [`docs/rfc-hub-integration.md`](docs/rfc-hub-integration.md) переформулирован
  как рекомендательный маршрут передачи практик в Хаб: Хаб — источник лучших
  практик и обмена опытом, не ограничитель локальных решений `mango_ba_prompts`.
- Созданы [`docs/task-for-konard-template.md`](docs/task-for-konard-template.md)
  и [`docs/adr/0003-creative-mode-governance.md`](docs/adr/0003-creative-mode-governance.md):
  шаблон задачи фиксирует WHAT/WHY без пошагового HOW, ADR описывает практику,
  примеры было/стало, обоснованные обходы и self-test на кейсе PR #57.
- [`AI_SESSION_HANDOVER_PROMPT.md`](AI_SESSION_HANDOVER_PROMPT.md) обновлён до
  локального шаблона постановки задач для Конарда.

### Added — Issue #52 фундамент: концепция, таксономия, RFC Хаба и базовая структура

- Создан [`docs/taxonomy.md`](docs/taxonomy.md) — таксономия **13 когнитивных
  операций** (9 базовых + 4 расширенных: `impact_analysis`,
  `reverse_requirements`, `risk_analysis`, `release_readiness`) и **9 процессов
  БА** с маппингом процессов на операции.
- Создан [`docs/rfc-hub-integration.md`](docs/rfc-hub-integration.md) — RFC
  (сознательно **не** ADR) о стратегическом направлении переноса лучших практик
  спока в Хаб: критерии C1–C5, процесс из 6 шагов, provenance
  `source_spoke`/`source_sha`.
- Создан каталог [`patterns/`](patterns/) с README (паттерн = 8 полей:
  `purpose`, `process_stage`, `context_requirements`, `prompt_template`,
  `quality_gates`, `examples`, `output_schema`, `governance_rules`); сами
  паттерны создаются отдельными задачами.
- Создан [`docs/ba-processes/00-index.md`](docs/ba-processes/00-index.md) —
  централизованный маппинг процесс ↔ операции ↔ паттерн ↔ промпты
  (вместо хранения маппинга во frontmatter).
- Создан шаблон таблицы открытых вопросов (дата | автор | суть | статус |
  решение) с правилом автоматической очистки решённых строк Конардом при
  закрытии связанного issue. В issue #80 механизм заменён единым трекером в
  [`governance/BACKLOG.md`](governance/BACKLOG.md#5-открытые-вопросы).
- Созданы контракты [`standards/prompt-standard.md`](standards/prompt-standard.md)
  (ровно 4 обязательных поля frontmatter: `status` со значениями
  `draft`/`canonical`/`archived`, `version`, `updated`, `temperature`;
  именование `[домен]-[операция]-[режим].md`; RAG-формат ссылок
  `См. [Глоссарий](standards/GLOSSARY.md)`; фиксация прогонов в
  `prompts/experiments/`) и
  [`standards/pattern-standard.md`](standards/pattern-standard.md)
  (8 обязательных полей паттерна, универсальный `prompt_template`).
- Создан шаблон issue
  [`.github/ISSUE_TEMPLATE/prompt-feedback.yml`](.github/ISSUE_TEMPLATE/prompt-feedback.yml)
  для фидбека БА: 2 обязательных поля (имя промпта + результат), чек-боксы
  типовых проблем, явный запрет ссылок на закрытые корпоративные документы;
  label `prompt:feedback` проставляется автоматически.
- `README.md` (v2.1): добавлен раздел «Стратегия и тактика» (цель —
  автоматизация БА Mango; тактика — библиотека паттернов и промптов; ссылка
  на RFC), исправлена повреждённая таблица структуры, таблица frontmatter
  приведена к 4 обязательным полям, обновлена навигация.

### Changed — Issue #56 разбиение draft-файла на 23 промпта со стандартизованной схемой именования

- Файл `prompts/drafts/Промпт+для+БА (1).md` (созданный в issue #54 как единый
  draft) разбит на **23 отдельных промпта** по схеме `[домен]-[операция]-[режим].md`
  (kebab-case). **18 новых** промптов размещены в [`prompts/`](prompts/)
  (`status: draft`, `version: 0.1`); **5 legacy-промптов из PDF** также размещены
  в [`prompts/`](prompts/) с суффиксом `-legacy` (`status: draft`, `version: 1.0`),
  так как продолжают использоваться; **6 старых canonical-промптов** перенесены в
  [`prompts/archive/`](prompts/archive/) с суффиксом `-legacy` (`status: archived`,
  `version: 1.0`). Текст каждого промпта скопирован **дословно** (проверено
  побайтово против исходного среза); добавлены обязательный frontmatter (`status`,
  `version`, `updated: 2026-06-11`, `temperature: 0.1`) и experimental marker сразу
  после него.
- **Операции** взяты из таксономии 13 когнитивных операций БА: `understanding`
  (контекст/глоссарий §2, уточняющие вопросы §9.1), `documentation` (ФТ §3.1,
  ограничения §4, резюме встреч §7–8, сопроводительное письмо §9.2), `validation`
  (валидация ФТ §3.2), `solution-design` (системно-технические требования §5),
  `modeling` (User Story §6.1, Use Case §6.2), `ingestion` (пост-обработка ASR §10).
- **Режимы.** Токены `stepwise` (Экспертный, пошаговое согласование) / `oneshot`
  (Экспресс, one-shot) / `legacy` (архивный) выбраны по результатам международного
  исследования (Пользователь допустил «другой режим по результатам исследования»):
  `expert`/`express` не являются стандартной терминологией, а «expert» коллидирует
  с role-prompting-идиомой «act as an expert»; `stepwise` уже используется в
  репозитории (`usecase-stepwise-generator-simple.md`) и совпадает с формулировками
  источника («пошаговый» / «one-shot»). Обоснование и ссылки — в описании PR #57.
- **Removed.** Исходный файл `prompts/drafts/Промпт+для+БА (1).md` удалён **только
  после** успешного создания и побайтовой верификации всех 23 файлов; опустевший
  каталог `prompts/drafts/` удалён. Запись CHANGELOG issue #54 о создании draft
  сохранена как исторический факт — данный шаг её сознательно замещает.

### Added — Issue #54 миграция прикреплённого файла промптов в `prompts/drafts/`

- Создан [`prompts/drafts/Промпт+для+БА (1).md`](prompts/drafts/) — миграция
  единственного файла, прикреплённого к issue #54 (`Промпт+для+БА (1).pdf`, СПИСОК
  ПРОМПТОВ для бизнес-анализа в Телеком SaaS). По правилу issue «один прикреплённый
  файл = один файл в репозитории» PDF перенесён как один draft без разбиения на
  отдельные промпты. Текст промптов скопирован из PDF без изменений; добавлены
  обязательный frontmatter (`status: draft`, `version: 0.1`, `updated: 2026-06-10`,
  `temperature: 0.1`) и experimental marker `<!-- EXPERIMENTAL: DO NOT USE IN PRODUCTION -->`.
- Для draft-файла требуется issue `prompt:review` (labels `prompt:review`, `draft`).
  Создание выполняется мейнтейнером: у автоматизации нет прав `triage`/`push` на
  upstream для применения labels (заготовка issue приведена в описании PR).

### Changed — Issue #48 обогащение `AI_SESSION_HANDOVER_PROMPT.md` (роль члена команды и проверка шаблонов)

- [`AI_SESSION_HANDOVER_PROMPT.md`](AI_SESSION_HANDOVER_PROMPT.md) дополнен командной
  рамкой (issue #48), `version` 0.3 → 0.4. Готовый prompt теперь открывается рамкой
  «ИИ в чате — **член команды** (C, Q, G, D, O), а не «исполнитель без доступа»;
  прямые изменения в репо — через Конарда». В Шаг 2 (ЧЕК-ЛИСТ КОНТЕКСТА) добавлена
  проверка предыдущего контекста чата; в Шаг 3 (READBACK) — учёт канала взаимодействия
  с репо и проверки шаблонов. Добавлены разделы «💬 Контекст чата диалога»,
  «🤝 Роль и канал взаимодействия с репо», «🔍 Проверка шаблонов» и «📝 Формат
  постановки задач для Конарда».
- **Осознанное расхождение с Хабом.** Правки внесены локально поверх базового шаблона
  Хаба [`templates/htom/AI_SESSION_HANDOVER_PROMPT.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/117e4a553815af9b05d841c81dd725dd4a4c4d44/templates/htom/AI_SESSION_HANDOVER_PROMPT.md)
  (SHA `117e4a55`), который этих разделов пока не содержит (проверено: шаблон в `main`
  Хаба идентичен закреплённому SHA). По политике source-of-truth расширение подлежит
  переносу в Хаб с последующей синхронизацией сюда. Ссылка на `templates/task-for-konard.md`
  указывает на ещё не созданный артефакт Хаба (см. PR-описание и issue #48). Провенанс
  (`source_hub`/`source_sha`) и структура EXECUTION/EXPLANATION сохранены.
- Создан [`docs/adr/0002-issue48-handover-local-enrichment.md`](docs/adr/0002-issue48-handover-local-enrichment.md):
  ADR фиксирует осознанные отклонения от буквы issue #48 (аддитивное обогащение вместо
  замены файла, реализация намерения в фактической структуре, условные ссылки на
  отсутствующие шаблоны) и follow-up на перенос расширения в Хаб (Hub-first).

### Added — Issue #46 governance sync with Hub (PR #208)

- Создан корневой артефакт онбординга
  [`AI_SESSION_HANDOVER_PROMPT.md`](AI_SESSION_HANDOVER_PROMPT.md) — готовый к
  копированию *Handover Prompt* для запуска ИИ-агента в новой сессии. Источник —
  Хаб `templates/htom/AI_SESSION_HANDOVER_PROMPT.md`, закреплён permalink-ом на
  merge-SHA PR #208 `117e4a553815af9b05d841c81dd725dd4a4c4d44`. Плейсхолдеры
  `{{REPO_NAME}}`/`{{project_name}}`/`{{hub_url}}` инстанцированы под mango; Шаг 1
  читает реально присутствующие локальные контракты команды, фундаментальные
  governance-контракты Хаба — по permalink-ам.
- Создан протокол онбординга
  [`governance/agent-onboarding-protocol.md`](governance/agent-onboarding-protocol.md)
  (kebab-case, адаптированная копия канонического протокола Хаба v1.2): семантическое
  разделение «артефакт ↔ протокол» из PR #208. Раздел Design Rationale сжат,
  полная история вынесена ссылкой на Хаб.
- Создан профиль Smart Sync [`.hub-profile.json`](.hub-profile.json) с ключами,
  которые фактически читает `tools/sync-from-hub.sh` Хаба
  (`target_type` / `phase` / `stack` / `hub_url` / `last_sync`).
- Создан [`docs/adr/0001-hub-sync-pr208.md`](docs/adr/0001-hub-sync-pr208.md):
  ADR фиксирует 8 осознанных отклонений от буквы issue (схема профиля, путь
  онбординга, терминология HTOM, подстановка `{{REPO_NAME}}`, Anti-Inflation по
  `tools/`, DoD без валидатора, исправление пути глоссария, permalink-провенанс) и
  сохранённые mango-специфичные правила.
- Добавлены строки навигации в [`README.md`](README.md) на оба новых
  онбординг-файла.

### Changed — sync `AI_GOVERNANCE.md` / `AI_QUICK_RULES.md` from `templates/htom/`

- [`AI_GOVERNANCE.md`](AI_GOVERNANCE.md) синхронизирован с Хабом
  `templates/htom/AI_GOVERNANCE.md` (SHA `117e4a55`): принята терминология
  **«HTOM-команда»**, добавлен provenance (`source_hub`/`source_sha`). Сохранена
  mango-специфичная taxonomy **«Capability Boundaries»** (с реальными путями и
  ссылкой на fail-closed) поверх общей хабовой рубрики. Исправлен стэйл-путь
  `kb/glossary.md` → `standards/GLOSSARY.md`. Строка DoD про
  `./tools/validate-repository-structure.sh` заменена на ориентир
  `docs/audit/initial-state-2026-06.md` (валидатора в mango нет — Anti-Inflation).
- [`AI_QUICK_RULES.md`](AI_QUICK_RULES.md) синхронизирован с Хабом
  `templates/htom/AI_QUICK_RULES.md` (SHA `117e4a55`): терминология
  **«HTOM-команда»**, provenance, различение HTOM-команда ↔ spoke-репозиторий.
  Сохранена явная секция **«Fail-Closed Semantics (КРИТИЧНО)»** (шаблон Хаба её
  свернул), чтобы оставалась резолвимой перекрёстная ссылка из `AI_GOVERNANCE.md`.

### Added — M-009 migration manifest

- Создан живой снимок миграции `governance/migration-manifest.md` (творческое
  улучшение C6 RFC). Содержит таблицу «артефакт → категория → действие → статус →
  назначение в споке» (RFC §5.1) и чек-лист-трекер «Перенесено / Осталось в
  Хабе / Требует уточнения» (RFC §5.3). Зафиксированы 6 промптов, 2 стандарта и
  5 экспериментов как `migrated`, 11 research-артефактов как `referenced`,
  монорепо-`README.md` как `archived` (E3) и 4 пустых плейсхолдера как
  `not-migrated` (P5). Все ссылки на Хаб закреплены permalink-ом на snapshot
  `038868dd125b4e2d849ff73604890f1d2787ac0f` (C3). Манифест ведётся по ходу
  Фаз 0–3 и закрывается в Фазе 3.
### Added — M-007 hub research dependency registry

- Создан единый реестр зависимостей от research Хаба
  `docs/hub-research-dependencies.md` (заголовок «Реестр зависимостей от
  исследований Хаба»). Файл-дубль `hub-research-links.md` не создаётся
  (запрет RFC §3.5).
- Заведены якоря на каждый артефакт `research/mango/*` (`#classification`,
  `#classification-tz`, `#taxonomy-concept`, `#requirements-flow`,
  `#requirements-lifecycle`, `#capability-decomposition`, `#rag-mapping`,
  `#research-readme`) с полным permalink на SHA
  `038868dd125b4e2d849ff73604890f1d2787ac0f` и списком consumers. Промпты и
  контракт классификации резолвят `research_dep` через эти якоря (E1, E8).

### Added — M-006 prompt frontmatter normalization

- Перенесены и нормализованы 6 prompt assets Mango в `prompts/`:
  `tz-stats-generator.md`, `tz-stats-generator-simple.md`,
  `user-story-generator.md`, `user-story-generator-simple.md`,
  `usecase-stepwise-generator.md` и `usecase-stepwise-generator-simple.md`.
  Каждый файл получил 7 обязательных frontmatter-полей, provenance
  (`source_hub`, `source_sha`, `based_on`), явные настройки запуска
  (`temperature: 0.1`, `output_format: markdown`) и отметку
  `migration_status: migrated` после self-test gate.
- Для `_exp`/canonical-вариантов добавлен явный раздел «ФОРМАТ ВЫВОДА»; для
  standalone `_simple`-вариантов с `research_dep: none` добавлен комментарий о
  бизнес-задаче и отсутствии формальной research-зависимости.

### Added — M-004 product classification contract

- Перенесён Mango-only контракт классификации из Хаба в
  `standards/product-classification-contract.md` (переименование из
  `projects/mango/standards/classification-glossary.md`, snapshot
  `038868dd125b4e2d849ff73604890f1d2787ac0f`). Контракт отделён от
  `standards/GLOSSARY.md`, содержит provenance (`source_hub`, `source_sha`) и
  использует `research_dep`-якоря будущего реестра
  `docs/hub-research-dependencies.md` вместо Hub-relative research-ссылок.

### Added — Phase 1 migration scaffold

- Перенесены 5 продуктовых экспериментов Mango из зафиксированного snapshot
  Хаба (`038868dd125b4e2d849ff73604890f1d2787ac0f`) в
  `prompts/experiments/` для M-005: прототип ТЗ-статистики, stepwise alignment
  use-case генератора, генератор user story из raw request, аудит промптов и
  self-test сценарий `prompts-selftest-2026-05-26.md`.
- Создан базовый каркас каталогов Фазы 1 (`prompts/`,
  `prompts/experiments/`, `prompts/archive/`, `standards/`, `kb/`, `docs/`,
  `docs/adr/`, `docs/audit/`) с поясняющими `.gitkeep`-файлами для M-002.
- Скопирован `standards/GLOSSARY.md` из Хаба для M-003: файл закреплён за
  permalink на SHA `038868dd125b4e2d849ff73604890f1d2787ac0f`, содержит
  `source_hub`/`source_sha` и фиксирует, что source of truth остаётся в Хабе,
  а синхронизация выполняется явным действием спока.

### Added — Initial repository structure based on hybrid-Intelligence-lab templates

- Инициализация спока `mango_ba_prompts` из «ДНК-шаблона» Хаба
  (`templates/spoke/`): базовый геном (governance, quick rules, навигация,
  каркасы `docs/adr/`, `docs/audit/`, база знаний `kb/glossary.md`).
- «Бесплатные» улучшения из анализа рекомендаций команд C и Q:
  fail-closed semantics в `AI_QUICK_RULES.md` и capability taxonomy в
  `AI_GOVERNANCE.md`.
- RFC стратегии миграции проекта Mango из Хаба в спок
  (`docs/analysis/migration-strategy-rfc.md`, issue #8): аудит 23 артефактов
  Хаба по полным URL, фазовая стратегия (Mermaid), edge cases, креативные
  улучшения и триггеры эволюции. Стоп-фактор: физический перенос — после
  Human Review.

### Changed

- Добавлен временный workflow создания промптов в `CONTRIBUTING.md` (issue #35,
  M-008): ровно 5 шагов `draft → frontmatter → marker → prompt:review →
  canonical`, capability boundary `prompts/drafts/` и минимальный пример
  frontmatter для черновика без введения матрицы или ADR-процесса.
- Переписан корневой `README.md` под standalone-спок (issue #28, M-001, v2.0):
  README теперь описывает `mango_ba_prompts` как **библиотеку промптов для
  бизнес-аналитиков** (ТЗ-статистика, use-case, user story), а не как базу
  знаний. Добавлены quickstart по чтению frontmatter промптов, структура
  `prompts/` и `standards/`, навигация на `CONTRIBUTING.md` и контакты/роли.
  Удалены унаследованные из «ДНК-шаблона» Хаба прямые и hub-относительные
  ссылки; единственный мост в Хаб — через `docs/hub-research-dependencies.md`.
- Уточнён RFC стратегии миграции (`docs/analysis/migration-strategy-rfc.md`,
  issue #10): добавлена таблица файлов Фазы 1, чек-лист нормализации промптов,
  единый реестр research-зависимостей, корректное разделение
  `standards/GLOSSARY.md` и `standards/product-classification-contract.md`,
  а также правила переноса продуктовых экспериментов.
- Зафиксированы решения Пользователя по Q1–Q4 в RFC миграции
  (`docs/analysis/migration-strategy-rfc.md`, issue #21): таблица Фазы 1
  утверждена, Hub-ссылки должны быть permalink на SHA, self-test стал
  обязательным gate для статуса `migrated`, а стандарты, промпты, эксперименты и
  `hub-research-dependencies.md` идут одним PR Фазы 1.
- Завершена доработка RFC (`docs/analysis/migration-strategy-rfc.md`,
  issue #12, v0.3, блоки 3–8): реестр зависимостей от исследований Хаба (§3.5),
  переписка README.md как обязательная задача Фазы 1, согласованные формулировки
  edge cases E5 (все эксперименты — часть продукта) и E6 (разделение
  глоссария и контракта классификации, §4.1), временный workflow промптов P0
  для `CONTRIBUTING.md` (§5.2) и шаблон Migration Manifest (§5.3).
- Human Review доработанного RFC миграции
  (`docs/reviews/migration-rfc-human-review-2026-06.md`, issue #13): сверка
  v0.3 против чек-листа из 11 пунктов (архитектурная целостность, операционная
  готовность, трассируемость) — все пункты пройдены; зафиксированы открытые
  вопросы Q1–Q4 на решение Пользователя перед стартом Фазы 0.
- Сформирован операционный бэклог Фазы 1 миграции
  (`governance/BACKLOG.md`, issue #14): 9 атомарных задач (M-001…M-009) с
  приоритетами, зависимостями, DoD и трассировкой на разделы утверждённого RFC,
  плюс Mermaid-диаграмма критического пути. Бэклог = один файл (Anti-Inflation);
  выполнение задач не начато.
- Материализован бэклог Фазы 1 в 9 готовых к созданию GitHub Issues
  (`governance/migration-phase1-issues.md`, issue #23): каждый пункт M-001…M-009
  оформлен по стандарту Хаба `ISSUE_WORKFLOW.md` (шаблон `task.yml`) с явным
  Operating Mode (`Creative`/`Structured`), приоритетом, зависимостями, DoD,
  трассировкой на RFC/бэклог и полными permalink-ссылками на Хаб (SHA
  `038868dd…`, решение Q2). Live-Issues создаёт человек при ревью (среда
  AI-агента имеет только `pull`-доступ; создание Issues — fail-closed,
  outward-facing). Сами задачи бэклога не выполняются.

### Removed

- Удалён `kb/glossary.md`: каталог `kb/` сохранён для практик, примеров и
  справочников; глоссарий будет заменён стандартом `standards/GLOSSARY.md` в
  M-003.
- Удалён placeholder `prompts/.gitkeep`: каталог `prompts/` теперь содержит
  реальные нормализованные prompt assets.
- Удалён placeholder `standards/.gitkeep`: каталог `standards/` теперь содержит
  реальный стандарт `standards/GLOSSARY.md`.
- Удалён технический корневой `.gitkeep`, созданный только для bootstrap PR.
