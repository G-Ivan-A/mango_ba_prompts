# Basic Example

## Input

```text
Встреча по callback SLA. Обсудили, что супервизору нужен список просроченных
обратных звонков. Срок 15 минут звучал как рабочая гипотеза. Канал уведомления
не выбрали. БА уточнит источник SLA у заказчика.
```

## Expected Output Fragment

```markdown
## Decisions
| Decision | Owner | Source | External-safe |
| --- | --- | --- | --- |
| Нужен контроль просроченных обратных звонков | TBD | Meeting notes | Да |

## Open questions
| Question | Owner | Blocks | Audience |
| --- | --- | --- | --- |
| 15 минут - утверждённый SLA или пример? | БА | FR | Customer |
| Какой канал уведомления нужен супервизору? | Customer | FR | Customer |

## Action items
| Action | Owner | Due date | Status |
| --- | --- | --- | --- |
| Уточнить источник SLA | БА | TBD | Open |
```
