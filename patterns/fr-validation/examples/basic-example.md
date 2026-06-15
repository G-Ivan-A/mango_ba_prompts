# Basic Example

## Input

```text
4.2 Система должна уведомлять ответственного сотрудника о просрочке.
Commercial Layer: client-order.
Product Layer: CCaaS.
```

## Expected Output Fragment

| ID | Location | Type | Severity | Evidence | Recommended action |
| --- | --- | --- | --- | --- | --- |
| D-1 | 4.2 | ambiguity | high | Нет определения "ответственный сотрудник" | Указать роль или правило выбора получателя |
| D-2 | 4.2 | not-testable | high | Не определено событие просрочки | Зафиксировать условие и момент наступления просрочки |
| D-3 | 4.2 | incomplete | medium | Нет канала уведомления | Задать вопрос заказчику или указать default channel |

Status: blocked until D-1 and D-2 are resolved.
