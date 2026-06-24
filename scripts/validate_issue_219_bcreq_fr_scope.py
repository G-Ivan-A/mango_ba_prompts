"""Regression check for issue #219 — BCREQ-FR scope against current MTalker docs.

The issue asks to treat the 2026 MTalker guides attached to issue #219 as the
priority source for current behavior. Section 4 of the RUN-0012 FT must therefore
not keep detailed requirements that are already covered by current
videoconference functionality; exclusions belong in the run log.
"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "runs/2026/RUN-0012/outputs/2026-06-22-bcreq-180-mt-group-video-call-ft.md"
LOG = ROOT / "runs/2026/RUN-0012/logs/business-task-log.md"


FORBIDDEN_ARTIFACT_MARKERS = {
    "legacy mobile participant list citation": "[MTALKER-MOB, §63",
    "legacy mobile add participant citation": "[MTALKER-MOB, §64",
    "legacy mobile remove participant citation": "[MTALKER-MOB, §71",
    "legacy mobile join-by-link citation": "[MTALKER-MOB, §42",
    "current participant-list section": "### 4.2. Просмотр списка участников",
    "current participant-management section": "### 4.3. Управление списком участников",
    "current join-by-link-history section": "### 4.8. Переподключение к конференции по ссылке из истории",
    "current participants context-menu flow": "через выбор опции «Участники»",
    "current remove-button detail": "Кнопка «Удалить»",
    "current add-button modal detail": "При нажатии кнопки «Добавить»",
}

REQUIRED_ARTIFACT_MARKERS = {
    "issue 219 source note": "issue #219",
    "2026 mobile guide": "UserGuide_mTalker_4Mobile.11.06.26.pdf",
    "2026 windows guide": "UserGuide_Windows_mTalker_ch1_Working.11.06.26.pdf",
    "new start flow retained": "быстрого старта группового звонка",
    "personal groups retained": "личных групп",
    "sound delta retained": "звуковые сигналы",
}

REQUIRED_LOG_MARKERS = {
    "delta heading": "Дельта issue #219",
    "current docs priority": "приоритетным источником текущей функциональности",
    "participant list exclusion": "просмотр состава участников видеоконференции",
    "participant management exclusion": "удаление участника из видеоконференции",
    "join by link exclusion": "присоединение к видеоконференции по ссылке",
}


def main() -> int:
    artifact_text = ARTIFACT.read_text(encoding="utf-8")
    log_text = LOG.read_text(encoding="utf-8")

    errors: list[str] = []

    for label, marker in FORBIDDEN_ARTIFACT_MARKERS.items():
        if marker in artifact_text:
            errors.append(f"{ARTIFACT.relative_to(ROOT)}: forbidden {label}: {marker!r}")

    for label, marker in REQUIRED_ARTIFACT_MARKERS.items():
        if marker not in artifact_text:
            errors.append(f"{ARTIFACT.relative_to(ROOT)}: missing {label}: {marker!r}")

    for label, marker in REQUIRED_LOG_MARKERS.items():
        if marker not in log_text:
            errors.append(f"{LOG.relative_to(ROOT)}: missing {label}: {marker!r}")

    if errors:
        print("FAIL issue #219 BCREQ-FR scope validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("OK issue #219 BCREQ-FR scope validation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
