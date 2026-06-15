# Basic Example

## Input

```text
User Story: Я как супервизор контакт-центра хочу получать уведомление, если
оператор не перезвонил VIP-клиенту за 15 минут, чтобы контролировать SLA.

Commercial Layer: client-order.
Product Layer: CCaaS notifications and callback control.
```

## Expected Output Fragment

```markdown
## 4.1 Контроль нарушения срока обратного звонка
- Requirement: Система должна определять случай, когда оператор не выполнил
  обратный звонок VIP-клиенту в течение 15 минут после пропущенного звонка.
- Source: User Story, SLA condition from client-order context.
- Acceptance hints: нарушение фиксируется только после истечения 15 минут.

## 4.2 Уведомление супервизора
- Requirement: Система должна отправлять супервизору уведомление о нарушении SLA
  обратного звонка.
- Open questions: канал уведомления требует уточнения.
```
