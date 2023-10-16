from __future__ import annotations

from decimal import Decimal

from pyrl.engine.creature.creature_picker import CreaturePicker
from pyrl.game_data.pyrl_creatures import PyrlCreature

def test_speciation_mult() -> None:
    assert CreaturePicker._speciation_mult(-6) == Decimal(0)
    assert CreaturePicker._speciation_mult(-5) == Decimal(0)
    assert CreaturePicker._speciation_mult(-4) == Decimal("0.008")
    assert CreaturePicker._speciation_mult(-3) == Decimal("0.064")
    assert CreaturePicker._speciation_mult(-2) == Decimal("0.216")
    assert CreaturePicker._speciation_mult(-1) == Decimal("0.512")
    assert CreaturePicker._speciation_mult(+0) == Decimal(1)
    assert CreaturePicker._speciation_mult(+1) == Decimal(1)
    assert CreaturePicker._speciation_mult(+2) == Decimal(1)
    assert CreaturePicker._speciation_mult(+3) == Decimal(1)
    assert CreaturePicker._speciation_mult(+4) == Decimal(1)
    assert CreaturePicker._speciation_mult(+5) == Decimal(1)
    assert CreaturePicker._speciation_mult(+6) == Decimal(1)
    assert CreaturePicker._speciation_mult(+7) == Decimal(1)
    assert CreaturePicker._speciation_mult(+8) == Decimal(1)
    assert CreaturePicker._speciation_mult(+9) == Decimal(1)
    assert CreaturePicker._speciation_mult(10) == Decimal(1)
    assert CreaturePicker._speciation_mult(11) == Decimal("0.999")
    assert CreaturePicker._speciation_mult(12) == Decimal("0.992")
    assert CreaturePicker._speciation_mult(13) == Decimal("0.973")
    assert CreaturePicker._speciation_mult(14) == Decimal("0.936")
    assert CreaturePicker._speciation_mult(15) == Decimal("0.875")
    assert CreaturePicker._speciation_mult(16) == Decimal("0.784")
    assert CreaturePicker._speciation_mult(17) == Decimal("0.657")
    assert CreaturePicker._speciation_mult(18) == Decimal("0.488")
    assert CreaturePicker._speciation_mult(19) == Decimal("0.271")
    assert CreaturePicker._speciation_mult(20) == Decimal(0)

def test_pyrl_creature_weights() -> None:
    assert CreaturePicker._picking_weight(0, PyrlCreature.GWORM.value)     == 1000 *  200
    assert CreaturePicker._picking_weight(0, PyrlCreature.GBAT.value)      == 512  * 1000
    assert CreaturePicker._picking_weight(0, PyrlCreature.IMP.value)       == 216  *  400
    assert CreaturePicker._picking_weight(0, PyrlCreature.GOBLIN.value)    == 64   * 1000
    assert CreaturePicker._picking_weight(0, PyrlCreature.KOBOLD.value)    == 8    * 1000
    assert CreaturePicker._picking_weight(0, PyrlCreature.SKELETON.value)  == 0    * 1000
    assert CreaturePicker._picking_weight(0, PyrlCreature.ZOMBIE.value)    == 0    *  500
    assert CreaturePicker._picking_weight(0, PyrlCreature.GNOLL.value)     == 0    * 1000
    assert CreaturePicker._picking_weight(0, PyrlCreature.GSPIDER.value)   == 0    * 1000
    assert CreaturePicker._picking_weight(0, PyrlCreature.ORC.value)       == 0    * 1000
    assert CreaturePicker._picking_weight(0, PyrlCreature.GHOST.value)     == 0    * 1000
    assert CreaturePicker._picking_weight(0, PyrlCreature.FIMP.value)      == 0    * 1000

    assert CreaturePicker._picking_weight(20, PyrlCreature.GWORM.value)    == 0   *  200
    assert CreaturePicker._picking_weight(20, PyrlCreature.GBAT.value)     == 271 * 1000
    assert CreaturePicker._picking_weight(20, PyrlCreature.IMP.value)      == 488 *  400
    assert CreaturePicker._picking_weight(20, PyrlCreature.GOBLIN.value)   == 657 * 1000
    assert CreaturePicker._picking_weight(20, PyrlCreature.KOBOLD.value)   == 784 * 1000
    assert CreaturePicker._picking_weight(20, PyrlCreature.SKELETON.value) == 875 * 1000
    assert CreaturePicker._picking_weight(20, PyrlCreature.ZOMBIE.value)   == 875 *  500
    assert CreaturePicker._picking_weight(20, PyrlCreature.GNOLL.value)    == 936 * 1000
    assert CreaturePicker._picking_weight(20, PyrlCreature.GSPIDER.value)  == 973 * 1000
    assert CreaturePicker._picking_weight(20, PyrlCreature.ORC.value)      == 992 * 1000
    assert CreaturePicker._picking_weight(20, PyrlCreature.GHOST.value)    == 999 * 1000
    assert CreaturePicker._picking_weight(20, PyrlCreature.FIMP.value)     == 1000 * 1000
