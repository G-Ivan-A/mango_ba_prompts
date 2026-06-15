---
status: draft
version: 0.1.0
updated: 2026-06-15
---

# ASR Ingestion

## purpose

**Name.** ASR Ingestion / Нормализация ASR-расшифровки.

**Intent.** Паттерн помогает БА превратить сырую ASR-расшифровку встречи,
созвона или голосовой заметки в читаемый вход для дальнейшего анализа: очищенный
текст, decisions, questions, факты, assumptions, action items и фрагменты,
требующие проверки.

Применяйте паттерн, когда исходный вход шумный: есть ошибки распознавания,
повторы, неполные фразы, несколько участников, смешение решений и обсуждений.

Не применяйте паттерн как замену протоколу встречи: если решение юридически или
коммерчески значимо, очищенный результат требует подтверждения участника или
owner review.

Полный URL репозитория: <https://github.com/G-Ivan-A/mango_ba_prompts>.

## process_stage

- **Process**: Формирование ФТ/ТЗ; Помощь ПО/ПМ.
- **Operation**: `ingestion`.
- **Pattern registry source of truth**:
  [docs/ba-processes/00-index.md](../../docs/ba-processes/00-index.md).
- **Taxonomy**: [docs/taxonomy.md](../../docs/taxonomy.md).
- **Prompt matrix**: [prompts/README.md](../../prompts/README.md).
- **Ecosystem map**: [docs/ba-ecosystem.md](../../docs/ba-ecosystem.md).
- **Related prompt implementations**:
  [`asr-ingestion-oneshot.md`](../../prompts/asr-ingestion-oneshot.md),
  [`asr-ingestion-legacy.md`](../../prompts/asr-ingestion-legacy.md).

Issue #85 также упоминает `asr-ingestion-stepwise.md`, но такого файла нет в
текущем каталоге `prompts/` на 2026-06-15. Поэтому паттерн ссылается только на
существующие prompt-файлы и фиксирует stepwise-вариант как future gap, а не как
исполняемую ссылку.

## context_requirements

**Context.** Паттерн применяется до смыслового анализа, когда вход ещё шумный и
не готов для glossary, FR или meeting summary.

- **Product Layer**: затронутый продукт или capability, если он звучит во
  встрече. Если продукт не ясен, результат должен сохранить фрагменты для
  последующего [`glossary-context-generation`](../glossary-context-generation/).
- **Commercial Layer**:
  - `client-order`: сохранить договорные ограничения, обещания, scope boundaries
    и вопросы к заказчику.
  - `internal-product`: сохранить decisions, hypotheses, metrics, owners and
    roadmap constraints.
  - `tender-rfp`: сохранить формулировки источника и не сглаживать юридически
    значимые слова.
- **Правила адаптации**: для клиентских встреч важнее точность decisions и
  обещаний; для внутренних встреч - owners and next steps; для тендера - дословно
  сохранять спорные термины и source fragments.

Обязательные входы: ASR-текст или заметки, дата/тип встречи, список известных
участников или ролей, цель обработки и ограничения приватности. Стоп-фактор:
ASR содержит sensitive data, которые нельзя коммитить или публиковать.

## prompt_template

LLM-агностичный шаблон:

```markdown
Ты помогаешь бизнес-аналитику Mango нормализовать ASR-расшифровку.

Вход:
- ASR transcript: {{asr_transcript}}
- Meeting type: {{meeting_type}}
- Known participants/roles: {{participants}}
- Product Layer hint: {{product_layer}}
- Commercial Layer: {{commercial_layer}}
- Privacy constraints: {{privacy_constraints}}

Сделай:
1. Очисти повторы, шум и явные ASR-ошибки без потери смысла.
2. Раздели факты, decisions, open questions, assumptions and action items.
3. Сохрани спорные фрагменты как "requires verification".
4. Отметь Product Layer and Commercial Layer, если они видны из входа.
5. Подготовь next step: glossary, FR, meeting summary or owner review.

Не делай:
- Не исправляй смысл спорной фразы без пометки.
- Не добавляй решения, которых нет во входе.
- Не публикуй персональные данные или закрытый контекст.
```

## quality_gates

**Forces.** Главные ограничения: не потерять смысл в очистке, не исправить
сомнительный фрагмент без пометки и не опубликовать sensitive data.

- Decisions отделены от обсуждения и assumptions.
- Непонятные ASR-фрагменты сохранены как requires verification, а не исправлены
  молча.
- Product Layer и Commercial Layer указаны явно или помечены как unknown.
- Action items содержат owner, если owner есть во входе; иначе owner = TBD.
- Sensitive data удалены или заменены обезличенными placeholders.
- Результат готов для следующего паттерна: glossary, meeting summary, FR or
  validation.

## examples

Минимальный few-shot пример:

- **Вход**: шумная фраза "ну надо там чтобы супервизор видел эти красные звонки
  когда оператор не отзвонился".
- **Выход**: normalized fact "нужно показать супервизору callback-задачи с
  нарушенным сроком"; requires verification "красные звонки" = UI status?; open
  question "какой срок считать нарушением?".

Расширенный пример: [examples/basic-example.md](examples/basic-example.md).

## output_schema

**Solution.** Результат паттерна - ASR Ingestion Pack, который отделяет clean
summary, facts, decisions, questions, action items and uncertain fragments.

```markdown
# ASR Ingestion Pack

## Clean transcript summary

## Facts
| Fact | Source fragment | Confidence |

## Decisions
| Decision | Owner | Source fragment | Verification |

## Questions
| Question | Owner | Blocks |

## Action items
| Action | Owner | Due date | Source fragment |

## Requires verification
| Fragment | Why uncertain | Suggested check |

## Routing
- Next pattern:
- Product Layer:
- Commercial Layer:
```

## governance_rules

- Статус `draft` допускает применение как preprocessing step; `canonical` требует
  review и подтверждённого применения на обезличенной расшифровке.
- source of truth для связей процесс -> паттерн -> prompt находится в
  [docs/ba-processes/00-index.md](../../docs/ba-processes/00-index.md).
- Паттерн не заменяет официальный протокол встречи и не утверждает решения без
  human review.
- `asr-ingestion-stepwise.md` не указан как связанный prompt, пока файл не
  появится в `prompts/` и центральном реестре.
- Версионирование следует SemVer из
  [ADR-002](../../docs/adr/002-pattern-standard.md).
