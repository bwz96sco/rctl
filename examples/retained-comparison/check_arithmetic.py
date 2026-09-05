"""Verify the synthetic example's declared arithmetic, without rctl."""

import json
from decimal import Decimal
from pathlib import Path


def main() -> None:
    root = Path(__file__).resolve().parent
    metrics = json.loads((root / "evidence/metrics.json").read_text())
    derived = json.loads((root / "evidence/derived.json").read_text())
    assert metrics["synthetic"] is True and derived["synthetic"] is True
    assert metrics["direction"] == "lower_is_better"
    gain = Decimal(metrics["baseline"]) - Decimal(metrics["candidate"])
    assert Decimal(derived["gain"]) == gain, "Derived gain differs from input arithmetic"
    assert derived["promote"] is (gain >= Decimal(metrics["minimum_gain"])), "Promotion contradicts the frozen threshold"
    print(f"PASS synthetic arithmetic: gain={gain}; promote={derived['promote']}")


if __name__ == "__main__":
    main()
