from pathlib import Path
import sys
import tempfile
import unittest

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from analysis import apply_sla_policy, load_sla_policy


class SlaPolicyTests(unittest.TestCase):
    def test_load_sla_policy_and_apply_team_override(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "sla_policy.json"
            path.write_text(
                '{"priority_hours": {"Critical": 5}, "team_priority_hours": {"Support": {"Critical": 2}}}',
                encoding="utf-8",
            )

            policy = load_sla_policy(path)
            df = pd.DataFrame(
                [
                    {"team": "Support", "priority": "Critical", "sla_target_hours": 4},
                    {"team": "Training", "priority": "Critical", "sla_target_hours": 4},
                ]
            )
            updated = apply_sla_policy(df, policy)

        self.assertEqual(updated.loc[0, "sla_target_hours"], 2)
        self.assertEqual(updated.loc[1, "sla_target_hours"], 5)


if __name__ == "__main__":
    unittest.main()
