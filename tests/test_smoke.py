"""Smoke checks for the offline strategy; no competition SDK is substituted."""

import json
from pathlib import Path
import subprocess
import sys
import unittest

from strategy import choose_card_to_reveal, get_bid, record_auction_result


class StrategySmokeTests(unittest.TestCase):
    def test_demo_runs_as_a_standalone_program(self) -> None:
        root: Path = Path(__file__).resolve().parents[1]
        result: subprocess.CompletedProcess[str] = subprocess.run(
            [sys.executable, "demo.py"], cwd=root, capture_output=True, text=True,
            check=True, timeout=10,
        )
        output: dict[str, object] = json.loads(result.stdout)
        self.assertIsInstance(output, dict)
        self.assertEqual(output["reveal_color"], "green")
        bids: object = output["bids"]
        self.assertIsInstance(bids, dict)
        if not isinstance(bids, dict):
            raise TypeError("The offline example must emit a bids object.")
        self.assertEqual(bids["treasure_2"], 5)
        self.assertEqual(bids["loan_20"], 6)

    def test_auction_results_feed_the_reveal_decision_without_mutation(self) -> None:
        initial: dict[int, tuple[str, ...]] = {0: ("green",), 1: (), 2: (), 3: ()}
        updated: dict[int, tuple[str, ...]] = record_auction_result(
            initial, 1, ("green", "green")
        )
        hand: tuple[str, ...] = ("green", "blue")
        self.assertEqual(choose_card_to_reveal(
            hand, updated[0], (updated[1], updated[2], updated[3]), {}
        ), 1)
        self.assertEqual(initial[1], ())
        self.assertEqual(updated[1], ("green", "green"))
        self.assertEqual(choose_card_to_reveal(
            hand, updated[0], (updated[1], updated[2], updated[3]), {"green": 5}
        ), 0)

    def test_funding_limits_and_invalid_inputs(self) -> None:
        self.assertEqual(get_bid("treasure_1", None, 0), 0)
        self.assertEqual(get_bid("treasure_2", None, 3), 3)
        self.assertEqual(get_bid("loan", 10, 0), 3)
        self.assertEqual(get_bid("invest", 10, 0), 0)
        with self.assertRaises(ValueError):
            get_bid("loan", None, 5)
        with self.assertRaises(ValueError):
            choose_card_to_reveal((), (), ((),), {})
        with self.assertRaises(ValueError):
            record_auction_result({0: ()}, 1, ("green",))


if __name__ == "__main__":
    unittest.main()
