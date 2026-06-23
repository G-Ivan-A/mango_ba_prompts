# Contract Issues

## Проверка `runs/CONTRACT.md`

- Контракт определяет канонический путь `runs/YYYY/RUN-XXXX/`, обязательные каталоги `inputs/`, `outputs/`, `feedback/`, `logs/` и обязательный `metadata.yaml`.
- Контракт перечисляет тип `business-task`; BCREQ-1027 классифицирован как `business-task`, потому что создает BCREQ-FR артефакт.
- Контракт разрешает дополнительные поля metadata, поэтому `api_reference` и `corrections_applied` добавлены без изменения контракта.

## Зафиксированные проблемы без изменения контрактов

- `runs/CONTRACT.md` дублирует `standards/runs-contract-standard.md`; эта проблема уже описана в `docs/analysis/executable-contracts-and-rfc-problems.md` как K-P4.2.
- `runs/CONTRACT.md` не формализует отдельным машинно-проверяемым правилом автоматическое исправление ошибочного пути постановки задачи.
- `runs/CONTRACT.md` не содержит явного правила, что изменение контрактов runs требует 2-факторного подтверждения human+LLM.

Контракты не изменялись, потому что issue #207 требует только зафиксировать проблемы без изменения contracts до 2-факторного согласования.
