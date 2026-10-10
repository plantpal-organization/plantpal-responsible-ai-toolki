"""Minimize plant-care context before it is sent to an AI service.

This is a standalone educational reference for agri-tech developers.
It is not PlantPal's production Leafy implementation, and it is not a
security certification. Use synthetic data when you try the examples.

The helper keeps a small allowlist of care facts, drops contact details,
precise location, purchase history, and commercial fields, and redacts
email addresses, phone numbers, and coordinate pairs that appear inside
free text. It never echoes the removed values.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from copy import deepcopy
from dataclasses import dataclass, field
from pathlib import Path

EXPERIENCE_LEVELS = frozenset({"beginner", "intermediate", "experienced"})
HISTORY_ACTIONS = frozenset(
    {
        "watered",
        "checked_soil",
        "moved",
        "repotted",
        "pruned",
        "observed",
        "other",
    }
)

# Names that must never be forwarded, at any depth.
EXCLUDED_KEYS = frozenset(
    {
        "email",
        "email_address",
        "e_mail",
        "phone",
        "phone_number",
        "mobile",
        "telephone",
        "latitude",
        "longitude",
        "lat",
        "lng",
        "gps",
        "precise_location",
        "location",
        "address",
        "street_address",
        "street",
        "postal_code",
        "zip_code",
        "purchase_history",
        "order_history",
        "orders",
        "vendor_commission",
        "commission",
        "commission_rate",
        "sponsorship",
        "sponsorship_data",
        "sponsor",
        "sponsored",
        "full_name",
        "customer_id",
        "user_id",
        "account_id",
        "national_id",
        "ip_address",
    }
)

ALLOWED_TOP_LEVEL = frozenset(
    {
        "plant_species",
        "light_conditions",
        "soil_and_drainage",
        "care_goals",
        "observations",
        "recent_care_history",
        "experience_level",
    }
)
HISTORY_FIELDS = frozenset({"action", "observed_on", "note"})

EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)
PHONE_RE = re.compile(
    r"(?<!\w)(?:"
    r"\+\d{1,3}[\s.-]?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}"
    r"|\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}"
    r"|\+\d{8,15}"
    r")(?!\w)"
)
COORDINATE_RE = re.compile(
    r"(?<!\d)[-+]?\d{1,3}\.\d{4,}\s*,\s*[-+]?\d{1,3}\.\d{4,}(?!\d)"
)
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

MAX_SPECIES = 80
MAX_SHORT_TEXT = 240
MAX_OBSERVATION = 250
MAX_NOTE = 300
MAX_ACTION = 80
MAX_OBSERVATIONS = 12
MAX_HISTORY = 8
MAX_GOALS = 5


@dataclass
class MinimizationResult:
    """Safe payload plus a report that does not repeat removed secrets."""

    payload: dict
    removed_fields: list[str] = field(default_factory=list)
    redactions: list[str] = field(default_factory=list)
    notices: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    context_quality: str = "incomplete"

    @property
    def ready_to_send(self) -> bool:
        """True when the minimized payload is structurally valid.

        A thin context can still be ready to send. The calling application
        should ask for missing care facts instead of inventing a plan.
        """

        return not self.errors

    def to_dict(self) -> dict:
        return {
            "ready_to_send": self.ready_to_send,
            "context_quality": self.context_quality,
            "payload": self.payload,
            "removed_fields": list(self.removed_fields),
            "redactions": list(self.redactions),
            "notices": list(self.notices),
            "errors": list(self.errors),
        }


def minimize_plant_context(raw: dict) -> MinimizationResult:
    """Return an allowlisted care payload and a non-sensitive report.

    The input is not modified. Excluded values are counted by field path
    only. They are not copied into the result.
    """

    result = MinimizationResult(payload={})
    if not isinstance(raw, dict):
        result.errors.append("Plant context must be a JSON object.")
        return result

    source = deepcopy(raw)
    for key, value in source.items():
        path = str(key)
        normalized = path.strip().lower()
        if normalized in EXCLUDED_KEYS:
            result.removed_fields.append(f"{path} (excluded)")
            continue
        if normalized not in ALLOWED_TOP_LEVEL:
            result.removed_fields.append(f"{path} (not allowlisted)")
            continue
        _copy_allowed_field(normalized, value, result)

    _assess_quality(result)
    return result


def _copy_allowed_field(key: str, value: object, result: MinimizationResult) -> None:
    if key == "plant_species":
        text = _clean_text(value, "plant_species", MAX_SPECIES, result)
        if text:
            result.payload["plant_species"] = text
        elif "plant_species" not in _error_fields(result):
            result.errors.append("plant_species must be a non-empty string.")
        return

    if key in {"light_conditions", "soil_and_drainage"}:
        text = _clean_text(value, key, MAX_SHORT_TEXT, result)
        if text:
            result.payload[key] = text
        return

    if key == "care_goals":
        goals = _clean_goals(value, result)
        if goals:
            result.payload["care_goals"] = goals
        return

    if key == "experience_level":
        if not isinstance(value, str):
            result.errors.append("experience_level must be a string.")
            return
        level = value.strip().lower()
        if level not in EXPERIENCE_LEVELS:
            result.errors.append(
                "experience_level must be beginner, intermediate, or experienced."
            )
            return
        result.payload["experience_level"] = level
        return

    if key == "observations":
        observations = _clean_observations(value, result)
        if observations:
            result.payload["observations"] = observations
        return

    if key == "recent_care_history":
        history = _clean_history(value, result)
        if history:
            result.payload["recent_care_history"] = history


def _clean_text(
    value: object,
    path: str,
    limit: int,
    result: MinimizationResult,
    *,
    required: bool = False,
) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        result.errors.append(f"{path} must be a string.")
        return None
    text = " ".join(value.split())
    if not text:
        if required:
            result.errors.append(f"{path} must be a non-empty string.")
        return None
    text, changed = _redact(text, path, result)
    if len(text) > limit:
        text = text[: limit - 1].rstrip() + "…"
        result.notices.append(f"{path} was shortened to {limit} characters.")
        changed = True
    if changed and not text.replace("[redacted-email]", "").replace(
        "[redacted-phone]", ""
    ).replace("[redacted-location]", "").strip(" .,"):
        result.notices.append(f"{path} had no care information left after redaction.")
        return None
    return text or None


def _redact(text: str, path: str, result: MinimizationResult) -> tuple[str, bool]:
    changed = False

    def mark(label: str, token: str):
        nonlocal changed
        changed = True

        def replace(_match: re.Match[str]) -> str:
            result.redactions.append(f"{path}: {label}")
            return token

        return replace

    text = EMAIL_RE.sub(mark("email", "[redacted-email]"), text)
    text = PHONE_RE.sub(mark("phone", "[redacted-phone]"), text)
    text = COORDINATE_RE.sub(mark("coordinates", "[redacted-location]"), text)
    return text, changed


def _clean_goals(value: object, result: MinimizationResult) -> list[str] | None:
    if isinstance(value, str):
        items = [value]
    elif isinstance(value, list):
        items = value
    else:
        result.errors.append("care_goals must be a string or a list of strings.")
        return None

    cleaned: list[str] = []
    for index, item in enumerate(items[:MAX_GOALS]):
        text = _clean_text(item, f"care_goals[{index}]", 80, result)
        if text:
            cleaned.append(text)
    if len(items) > MAX_GOALS:
        result.notices.append(f"care_goals kept the first {MAX_GOALS} items.")
        result.removed_fields.append(f"care_goals[{MAX_GOALS}:] (over limit)")
    return cleaned or None


def _clean_observations(value: object, result: MinimizationResult) -> list[str] | None:
    if not isinstance(value, list):
        result.errors.append("observations must be a list of strings.")
        return None
    cleaned: list[str] = []
    for index, item in enumerate(value[:MAX_OBSERVATIONS]):
        text = _clean_text(item, f"observations[{index}]", MAX_OBSERVATION, result)
        if text:
            cleaned.append(text)
    if len(value) > MAX_OBSERVATIONS:
        result.notices.append(f"observations kept the first {MAX_OBSERVATIONS} items.")
        result.removed_fields.append(f"observations[{MAX_OBSERVATIONS}:] (over limit)")
    return cleaned or None


def _clean_history(value: object, result: MinimizationResult) -> list[dict] | None:
    if not isinstance(value, list):
        result.errors.append("recent_care_history must be a list.")
        return None

    cleaned: list[dict] = []
    for index, item in enumerate(value[:MAX_HISTORY]):
        path = f"recent_care_history[{index}]"
        if not isinstance(item, dict):
            result.errors.append(f"{path} must be an object.")
            continue
        entry: dict[str, str] = {}
        for key, raw_value in item.items():
            normalized = str(key).strip().lower()
            if normalized in EXCLUDED_KEYS:
                result.removed_fields.append(f"{path}.{key} (excluded)")
                continue
            if normalized not in HISTORY_FIELDS:
                result.removed_fields.append(f"{path}.{key} (not allowlisted)")
                continue
            if normalized == "action":
                if not isinstance(raw_value, str):
                    result.errors.append(f"{path}.action must be a string.")
                    continue
                action = raw_value.strip().lower()
                if action not in HISTORY_ACTIONS:
                    result.errors.append(
                        f"{path}.action must be a care action such as watered, "
                        "checked_soil, moved, repotted, pruned, observed, or other."
                    )
                    continue
                entry["action"] = action
                continue
            if normalized == "observed_on":
                if not isinstance(raw_value, str) or not DATE_RE.match(raw_value.strip()):
                    result.errors.append(f"{path}.observed_on must use YYYY-MM-DD.")
                    continue
                entry["observed_on"] = raw_value.strip()
                continue
            note = _clean_text(raw_value, f"{path}.note", MAX_NOTE, result)
            if note:
                entry["note"] = note
        if "action" in entry:
            cleaned.append(entry)
        elif item:
            result.errors.append(f"{path} needs an action.")
    if len(value) > MAX_HISTORY:
        result.notices.append(f"recent_care_history kept the first {MAX_HISTORY} items.")
        result.removed_fields.append(f"recent_care_history[{MAX_HISTORY}:] (over limit)")
    return cleaned or None


def _assess_quality(result: MinimizationResult) -> None:
    if result.errors or "plant_species" not in result.payload:
        if "plant_species" not in result.payload and not any(
            error.startswith("plant_species") for error in result.errors
        ):
            result.errors.append("plant_species is required before an AI care request.")
        result.context_quality = "incomplete"
        return

    signals = [
        key
        for key in (
            "light_conditions",
            "soil_and_drainage",
            "observations",
            "recent_care_history",
        )
        if result.payload.get(key)
    ]
    if len(signals) >= 2:
        result.context_quality = "usable"
        return

    result.context_quality = "thin"
    result.notices.append(
        "Context is thin. Ask for the missing care facts before recommending an action."
    )


def _error_fields(result: MinimizationResult) -> set[str]:
    return {error.split()[0] for error in result.errors}


def _load_cases(document: object) -> list[dict]:
    if isinstance(document, dict) and isinstance(document.get("cases"), list):
        return document["cases"]
    if isinstance(document, dict):
        return [{"name": "input", "input": document}]
    raise ValueError("Input JSON must be an object or a cases collection.")


def build_report(document: object) -> list[dict]:
    reports = []
    for index, case in enumerate(_load_cases(document)):
        if not isinstance(case, dict) or "input" not in case:
            raise ValueError(f"Case {index} must be an object with an input field.")
        result = minimize_plant_context(case["input"])
        reports.append(
            {
                "name": str(case.get("name") or f"case-{index + 1}"),
                **result.to_dict(),
            }
        )
    return reports


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Minimize synthetic plant-care context before an AI request. "
            "Educational reference only."
        )
    )
    parser.add_argument("input_path", type=Path, help="Path to a JSON object or cases file.")
    args = parser.parse_args(argv)

    try:
        document = json.loads(args.input_path.read_text(encoding="utf-8"))
        reports = build_report(document)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        print(f"Could not minimize context: {exc}", file=sys.stderr)
        return 1

    json.dump(reports, sys.stdout, indent=2, ensure_ascii=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
