from __future__ import annotations

from decimal import Decimal

from pyrl.engine.creature.creature_picker import CreaturePicker

def test_speciation_mult() -> None:
    picker = CreaturePicker()
    assert picker._speciation_mult(0, -6) == Decimal(0)
    assert picker._speciation_mult(0, -5) == Decimal(0)
    assert picker._speciation_mult(0, -4) == Decimal("0.008")
    assert picker._speciation_mult(0, -3) == Decimal("0.064")
    assert picker._speciation_mult(0, -2) == Decimal("0.216")
    assert picker._speciation_mult(0, -1) == Decimal("0.512")
    assert picker._speciation_mult(0, 0) == Decimal(1)
    assert picker._speciation_mult(0, 1) == Decimal(1)
    assert picker._speciation_mult(0, 2) == Decimal(1)
    assert picker._speciation_mult(0, 3) == Decimal(1)
    assert picker._speciation_mult(0, 4) == Decimal(1)
    assert picker._speciation_mult(0, 5) == Decimal(1)
    assert picker._speciation_mult(0, 6) == Decimal(1)
    assert picker._speciation_mult(0, 7) == Decimal(1)
    assert picker._speciation_mult(0, 8) == Decimal(1)
    assert picker._speciation_mult(0, 9) == Decimal(1)
    assert picker._speciation_mult(0, 10) == Decimal(1)
    assert picker._speciation_mult(0, 11) == Decimal("0.999")
    assert picker._speciation_mult(0, 12) == Decimal("0.992")
    assert picker._speciation_mult(0, 13) == Decimal("0.973")
    assert picker._speciation_mult(0, 14) == Decimal("0.936")
    assert picker._speciation_mult(0, 15) == Decimal("0.875")
    assert picker._speciation_mult(0, 16) == Decimal("0.784")
    assert picker._speciation_mult(0, 17) == Decimal("0.657")
    assert picker._speciation_mult(0, 18) == Decimal("0.488")
    assert picker._speciation_mult(0, 19) == Decimal("0.271")
    assert picker._speciation_mult(0, 20) == Decimal(0)
