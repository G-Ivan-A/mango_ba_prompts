# Basic Example

## Input

```text
... надо чтобы супервайзер видел красные звонки когда оператор не отзвонился,
ну вроде пятнадцать минут, клиент потом жалуется ...
```

## Expected Output Fragment

| Type | Content | Verification |
| --- | --- | --- |
| Fact | Нужен контроль обратных звонков оператора | Medium |
| Assumption | "красные звонки" означает просроченные callback-задачи в интерфейсе | Requires verification |
| Question | Срок нарушения SLA равен 15 минутам или это пример? | Blocks FR |
| Question | Кто должен видеть уведомление: супервизор, руководитель группы или оба? | Blocks FR |

Routing: next pattern is `glossary-context-generation`, then `fr-generation` after
questions are resolved.
