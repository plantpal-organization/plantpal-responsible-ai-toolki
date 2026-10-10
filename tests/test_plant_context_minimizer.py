"""Unit tests for the educational plant-context minimizer."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "examples"))

from plant_context_minimizer import (  # noqa: E402
    build_report,
    minimize_plant_context,
)


EXAMPLES = ROOT / "examples" / "example_inputs.json"
SECRET_MARKERS = (
    "gardener@example.com",
    "hidden@example.com",
    "+96170111222",
    "+1 202 555 0148",
    "33.8938",
    "35.5018",
    "12 Example Street",
    "SOIL-1",
    "spring-pots",
    "user-example-100",
    "Example Nursery",
)


class MinimizePlantContextTests(unittest.TestCase):
    def test_usable_basil_context_is_preserved(self):
        raw = {
            "plant_species": "  Sweet basil  ",
            "light_conditions": "Morning sun",
            "soil_and_drainage": "Pot with drainage holes",
            "care_goals": ["Kitchen herb"],
            "observations": ["Pale lower leaves"],
            "recent_care_history": [
                {"action": "Watered", "observed_on": "2026-10-08", "note": "Soil was dry."}
            ],
            "experience_level": "Beginner",
        }
        result = minimize_plant_context(raw)

        self.assertTrue(result.ready_to_send)
        self.assertEqual(result.context_quality, "usable")
        self.assertEqual(result.payload["plant_species"], "Sweet basil")
        self.assertEqual(result.payload["experience_level"], "beginner")
        self.assertEqual(result.payload["recent_care_history"][0]["action"], "watered")
        self.assertEqual(raw["experience_level"], "Beginner")

    def test_sensitive_and_commercial_fields_are_removed_without_echoing_values(self):
        raw = json.loads(EXAMPLES.read_text(encoding="utf-8"))["cases"][1]["input"]
        result = minimize_plant_context(raw)
        encoded = json.dumps(result.to_dict())

        self.assertTrue(result.ready_to_send)
        self.assertEqual(result.payload["plant_species"], "Epipremnum aureum")
        self.assertNotIn("email", result.payload)
        self.assertNotIn("vendor_commission", result.payload)
        self.assertTrue(any(item.endswith("(excluded)") for item in result.removed_fields))
        self.assertTrue(any("nickname" in item for item in result.removed_fields))
        for marker in SECRET_MARKERS:
            self.assertNotIn(marker, encoded)

    def test_free_text_contact_details_are_redacted_and_invalid_fields_block_sending(self):
        raw = json.loads(EXAMPLES.read_text(encoding="utf-8"))["cases"][2]["input"]
        result = minimize_plant_context(raw)
        encoded = json.dumps(result.to_dict())

        self.assertFalse(result.ready_to_send)
        self.assertEqual(result.context_quality, "incomplete")
        self.assertEqual(
            result.payload["observations"][0],
            "Leaves droop by evening. Contact [redacted-email] or [redacted-phone].",
        )
        self.assertIn("[redacted-location]", result.payload["recent_care_history"][0]["note"])
        self.assertNotIn("email", result.payload["recent_care_history"][0])
        self.assertNotIn("dose_ml", result.payload["recent_care_history"][0])
        self.assertTrue(any("experience_level" in error for error in result.errors))
        self.assertTrue(any("plant_species" in error for error in result.errors))
        for marker in ("gardener@example.com", "+1 202 555 0148", "33.8938", "hidden@example.com"):
            self.assertNotIn(marker, encoded)

    def test_species_only_context_is_thin_but_sendable(self):
        result = minimize_plant_context({"plant_species": "Basil", "care_goals": "   "})

        self.assertTrue(result.ready_to_send)
        self.assertEqual(result.context_quality, "thin")
        self.assertEqual(list(result.payload), ["plant_species"])
        self.assertTrue(any("thin" in notice.lower() for notice in result.notices))

    def test_non_object_input_is_rejected(self):
        result = minimize_plant_context(["basil"])  # type: ignore[arg-type]

        self.assertFalse(result.ready_to_send)
        self.assertEqual(result.payload, {})

    def test_history_requires_a_known_action_and_a_real_date(self):
        result = minimize_plant_context(
            {
                "plant_species": "Basil",
                "light_conditions": "Bright window",
                "recent_care_history": [
                    {"action": "apply-pesticide", "observed_on": "yesterday", "note": "See label"}
                ],
            }
        )

        self.assertFalse(result.ready_to_send)
        self.assertNotIn("recent_care_history", result.payload)
        self.assertTrue(any("action" in error for error in result.errors))
        self.assertTrue(any("observed_on" in error for error in result.errors))

    def test_long_observation_is_shortened_and_extra_items_are_dropped(self):
        observations = [f"Leaf note {index}" for index in range(14)]
        observations[0] = "x" * 400
        result = minimize_plant_context(
            {
                "plant_species": "Basil",
                "light_conditions": "Bright window",
                "soil_and_drainage": "Drains freely",
                "observations": observations,
            }
        )

        self.assertEqual(len(result.payload["observations"]), 12)
        self.assertTrue(result.payload["observations"][0].endswith("…"))
        self.assertLessEqual(len(result.payload["observations"][0]), 250)
        self.assertTrue(any("over limit" in item for item in result.removed_fields))

    def test_nested_commercial_field_cannot_survive_inside_history(self):
        result = minimize_plant_context(
            {
                "plant_species": "Mint",
                "soil_and_drainage": "Moist, with drainage",
                "observations": ["Stems are upright"],
                "recent_care_history": [
                    {
                        "action": "checked_soil",
                        "observed_on": "2026-10-01",
                        "sponsorship": "paid placement",
                        "note": "Soil was damp.",
                    }
                ],
            }
        )
        encoded = json.dumps(result.payload)

        self.assertNotIn("sponsorship", encoded)
        self.assertNotIn("paid placement", encoded)
        self.assertIn("recent_care_history[0].sponsorship (excluded)", result.removed_fields)

    def test_example_file_report_hides_sensitive_values(self):
        document = json.loads(EXAMPLES.read_text(encoding="utf-8"))
        encoded = json.dumps(build_report(document))

        for marker in SECRET_MARKERS:
            self.assertNotIn(marker, encoded)
        names = [item["name"] for item in build_report(document)]
        self.assertIn("basil_usable_context", names)
        self.assertIn("species_only_thin_context", names)

    def test_command_line_example_exits_cleanly(self):
        completed = subprocess.run(
            [sys.executable, str(ROOT / "examples" / "plant_context_minimizer.py"), str(EXAMPLES)],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        report = json.loads(completed.stdout)
        self.assertEqual(len(report), 4)
        self.assertTrue(report[0]["ready_to_send"])
        self.assertEqual(report[0]["context_quality"], "usable")
        self.assertFalse(report[2]["ready_to_send"])
        for marker in SECRET_MARKERS:
            self.assertNotIn(marker, completed.stdout)


if __name__ == "__main__":
    unittest.main()
