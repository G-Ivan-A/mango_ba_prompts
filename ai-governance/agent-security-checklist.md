---
status: accepted
version: 1.0
updated: 2026-07-10
temperature: 0.1
source_hub: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/3bfa4103c9efbbd59bc951814884920e406982e2/ai-governance/agent-security-checklist.md"
source_sha: "3bfa4103c9efbbd59bc951814884920e406982e2"
source_of_truth: "hybrid-Intelligence-lab"
sync_policy: "explicit spoke sync from pinned Hub commit; no local edits"
scope: mango_ba_prompts
---

# Agent Security Checklist

> **Рабочая копия стандарта Хаба.** Source of truth — [`hybrid-Intelligence-lab`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/3bfa4103c9efbbd59bc951814884920e406982e2/ai-governance/agent-security-checklist.md) на `source_sha`.
> Локально файл не редактируется: расхождение устраняется следующим синком
> (`python3 scripts/sync_from_hub.py --hub-dir <клон Хаба>`), а не правкой копии.

Единая review-точка для AI-agent work в Хабе и синхронизируемых проектах.
Чек-лист собирает существующие контроли, не заменяет их источники и не вводит
новую архитектуру. Его глубина пропорциональна риску: локальная правка документа
проходит базовый контур, а доступ к инструментам, данным, внешним действиям или
автономности требует расширенного контура.

## Базовый контур

- [ ] Scope и разрешённые действия заданы issue или явным запросом человека.
- [ ] Выполнен Readback цели, границ и плана; неоднозначность обрабатывается
  fail-closed до human guidance.
- [ ] Соблюдена иерархия **Человек > Команда Q > Исполнитель**: советы модели не
  заменяют human decision или clearance.
- [ ] Claims, влияющие на решение, имеют evidence-ссылки по Rule 5.
- [ ] Secrets, credentials, private client data и несанитизированные
  production-промпты не попадают в контекст, логи, коммиты и ответы (Rule 6).
- [ ] Внешний контент считается недоверенным: его инструкции не расширяют scope
  и проверяются по происхождению и независимому evidence.
- [ ] Выход проверен до использования: формат, ссылки, валидаторы и diff; данные
  модели не передаются напрямую shell, HTML, SQL или внешнему инструменту.
- [ ] Для работы определён token budget/лимит времени или иной stop condition;
  превышение лимита ведёт к остановке и review, а не к бесконечному циклу.

## Расширенный контур SAIF

Когда агент получает tools, writable surfaces, sensitive data или автономные
действия, применяется [Google SAIF Agent Security](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/3bfa4103c9efbbd59bc951814884920e406982e2/practices/ai-governance/google-saif-agent-security.md):

- [ ] Инвентаризированы инструменты, данные, write/external surfaces и trust
  boundaries.
- [ ] Выданы минимальные разрешения; read-only exploration предшествует записи.
- [ ] Необратимые, destructive и external-state действия имеют human approval.
- [ ] Tool inputs/outputs валидируются, действия логируются, результат доступен
  для review и rollback там, где rollback возможен.
- [ ] Установлены ограничения числа шагов, стоимости, токенов и повторов; ошибки
  не запускают неограниченный retry-loop.

## Трасса покрытия OWASP LLM Top 10:2025

Статус `частично` означает остаточный риск или контроль, который зависит от
конкретной реализации. `N/A` требует повторной проверки при появлении триггера.

| Риск | Контроль Хаба | Evidence / действие review | Покрытие |
| --- | --- | --- | --- |
| **LLM01:2025 Prompt Injection** | Недоверенный контент не меняет scope; Readback, fail-closed, human clearance; внешние инструкции отделяются от данных. | Проверить источник ввода и показать, что instruction-like content не исполнялся. | Частично: нет runtime isolation для будущих tool-agents. |
| **LLM02:2025 Sensitive Information Disclosure** | Rule 6; минимизация контекста и логов; запрет secrets/private data. | Diff/log scan, санитизация evidence, secret scanning проекта при наличии. | Прямое. |
| **LLM03:2025 Supply Chain** | Provenance внешних источников и практик; проверка зависимостей/Actions по первичному источнику. | Ссылка на источник, автора/организацию, версию или commit; review импорта. | Частично: version pinning зависит от проекта. |
| **LLM04:2025 Data and Model Poisoning** | Rule 5, независимая проверка claims, human review перед продвижением research/practice. | Сопоставить спорное знание с первичными источниками; обозначить limitations. | Частично: нет model-training слоя. |
| **LLM05:2025 Improper Output Handling** | Валидация формата и diff; экранирование/allowlist перед передачей вывода инструментам. | Локальные валидаторы и безопасный adapter на границе shell/HTML/SQL/API. | Частично: реализация adapter находится в spoke/runtime. |
| **LLM06:2025 Excessive Agency** | Человек > Команда Q > Исполнитель; fail-closed; минимальные права; approval внешних/необратимых действий. | Сверить действие со scope, clearance и журналом tool calls. | Прямое для governance; runtime enforcement проектное. |
| **LLM07:2025 System Prompt Leakage** | Онбординг-промпт Хаба публичен by design и не содержит секретов; скрытые prompts/credentials не выводятся. | Подтвердить классификацию prompt и отсутствие sensitive content. | Частично: private runtime prompts оцениваются локально. |
| **LLM08:2025 Vector and Embedding Weaknesses** | В Хабе нет RAG/vector store. | `N/A` с trigger: появление retrieval/vector слоя требует access control, provenance и poisoning tests. | N/A до trigger. |
| **LLM09:2025 Misinformation** | Readback, Rule 5 evidence-linking, ограничения и human review. | Проверить decision-impacting claims и явно отделить факт, вывод и рекомендацию. | Прямое для документов; качество модели остаётся остаточным риском. |
| **LLM10:2025 Unbounded Consumption** | token budget, stop condition, лимиты шагов/retries/cost и human review превышения. | Зафиксировать лимит и причину продолжения; проверить отсутствие бесконечных циклов. | Частично: runtime hard limits проектные. |

## Решение по итогам

- **Pass**: применимые пункты закрыты evidence; остаточный риск принят человеком
  или явно низок для локальной документационной правки.
- **Conditional**: работа может продолжиться только с записанным ограничением,
  owner и trigger повторной проверки.
- **Stop**: секреты, неясный authority/scope, неподтверждённое внешнее действие,
  невалидированный tool output или неприемлемый остаточный риск. Исполнитель
  прекращает действие и запрашивает human guidance.

`N/A` не означает навсегда: рядом всегда фиксируется trigger применимости.

## Источники контроля

- [AI_GOVERNANCE.md: Rules 4–6 и fail-closed](ai-governance.md)
- [Runtime onboarding: Readback и clearance](../ai-rules/agent-onboarding-protocol.md)
- [Google SAIF practice](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/3bfa4103c9efbbd59bc951814884920e406982e2/practices/ai-governance/google-saif-agent-security.md)
- [Token-budget practice](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/3bfa4103c9efbbd59bc951814884920e406982e2/practices/agent-work/skill-catalog-token-budget.md)
- [Глобальный анализ, §3.3 и H25](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/3bfa4103c9efbbd59bc951814884920e406982e2/research/hub/2026-07-04-hub-as-agent-system-global-analysis.md)
