---
status: draft
version: 0.1
updated: 2026-10-19
ai-generated: true
type: input
scope: mango-only
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/375"
---

# Вход прогона RUN-0074 — провенанс

Тема: **задача 1106 — генерация BCREQ-ФТ «Информационное сообщение Абоненту о записи разговора при целевых исходящих контактах» (ЛК ВАТС, Mango Talker; прямые исходящие, ЗОЗ, АПП)**. БА шаблоном-промптом (реплика 0) запустил генерацию документа по разделам и в течение двух с половиной недель правил ответы двух моделей. В конце диалога по запросу БА модель вывела стандарт формирования BCREQ-документации (реплика 207). Прогон фиксирует диалог ради статистики ошибок ИИ и золотых наборов для промптов и навыков генерации BCREQ-ФТ по разделам.

## Источники

| Поле | Значение |
| --- | --- |
| Вложение issue | [`chat-export-1106.json`](https://github.com/user-attachments/files/33668084/chat-export-1106.json) |
| Размер, байт | 4911244 |
| SHA-256 | `5eddd393276aa3e6e95088d2cf5bacb7464aee22da2cf5b3ce6b4f5da87f54b7` |
| Заголовок чата в экспорте | `1106` |
| Окно диалога, UTC | 2026-09-15 10:24:13 — 2026-10-01 17:56:35 |
| Реплик в линейной ветке | 214 (107 БА, 107 модели) |
| Модели | qwen3.7-plus, qwen3.8-max |
| SSOT продуктовой принадлежности | [mango-ba-ai-runtime @ `91406e4`](https://github.com/G-Ivan-A/mango-ba-ai-runtime/tree/91406e430aeb70dabf20548eee0ea95127f42690): `taxonomy/products.yaml`, `AGENTS.md`, `golden/cases.yaml`, `docs/kb` |

## Вложения внутри диалога

Перечислены только имена файлов: ссылки на вложения в экспорте содержат подписанные токены CDN и в репозиторий не переносятся.

| Файл | Реплика | Что это |
| --- | --- | --- |
| `UserGuide_Windows_mTalker_ch1_Working.11.06.26.pdf`, `UserGuide_mTalker_4Mobile 11.06.26.pdf`, `LK_manual_v-123.pdf` | 8 | руководства Mango Talker (Windows, мобильный) и ЛК ВАТС; руководство ЛК разобрано в КБ runtime `docs/kb/mango-lk-manual` |
| `CC_manual_1.26.28.1.pdf` | 10, 18, 28 | руководство Контакт-центра; в КБ runtime — `docs/kb/mango-cc-manual` |
| `BCREQ-765.pdf`, `BCREQ-1069.pdf` | 60, 62 | документы BCREQ других задач — образцы формы |
| `image.png` | 134 | изображение |
| `Запись клиентского плеча.jpg` | 138, 182 | изображение (по имени — макет записи клиентского плеча) |
| `Mango_office_integration_BPMSoft.pdf` | 152 | руководство интеграции с BPMSoft; в КБ runtime — `docs/kb/integration-bpmsoft` |
| `Снимок экрана 2025-10-01 105105.jpg` | 182 | снимок экрана |

## Почему исходного JSON нет в репозитории

По правилу, принятому в issue [#309](https://github.com/G-Ivan-A/mango_ba_prompts/issues/309), сырые экспорты чатов в репозитории не остаются: вход прогона описан провенансом (ссылка, размер, контрольная сумма), а все производные артефакты порождаются из него детерминированно. Цитаты в записи — дословные фрагменты экспорта, каждая сверена с ним ([`../logs/quote-verification.md`](../logs/quote-verification.md)).

## Воспроизведение

Экспорт — недоверенные данные: он скачивается в отдельный пустой каталог, а скрипты, которые его читают, запускаются из репозитория с `python3 -I`.

```bash
mkdir -p /tmp/dl375
curl -L -o /tmp/dl375/chat-export-1106.json \
  https://github.com/user-attachments/files/33668084/chat-export-1106.json
sha256sum /tmp/dl375/chat-export-1106.json
# ожидается: 5eddd393276aa3e6e95088d2cf5bacb7464aee22da2cf5b3ce6b4f5da87f54b7

mkdir -p experiments/issue_375
python3 -I experiments/issue_309_run_stats.py /tmp/dl375/chat-export-1106.json \
  --json experiments/issue_375/stats.json
python3 -I experiments/issue_375_dump.py /tmp/dl375/chat-export-1106.json

python3 -I experiments/issue_375_verify_quotes.py /tmp/dl375/chat-export-1106.json
python3 -I experiments/issue_375_section_prompts_check.py /tmp/dl375/chat-export-1106.json
python3 -I experiments/issue_375_golden_set.py
```

В репозитории остаются `experiments/issue_375/stats.json`, `experiments/issue_375/quote-check.json` и `experiments/issue_375/section-prompts-check.json` (числа и контрольные суммы без текста переписки и без ссылок на вложения): по ним генератор и валидатор `scripts/validate_issue_375_run.py` воспроизводят запись без исходного экспорта. Реплики, которые пишет `experiments/issue_375_dump.py` (`experiments/issue_375/turns/`), в репозиторий не коммитятся.

## Чего во входе нет

- нет сырого JSON-экспорта и полной стенограммы: прогон фиксирует статистику и дословные цитаты, а не всю переписку;
- нет принятого итогового документа BCREQ-ФТ: последняя редакция БА (реплики 196 и 200) не сопровождается приёмкой, после неё БА запросил стандарт генерации (реплики 202–207);
- нет содержимого вложений: PDF и изображения при фиксации не открывались; утверждения модели о ЛК ВАТС, Контакт-центре и BPMSoft сверены с разборами тех же руководств в КБ runtime.
