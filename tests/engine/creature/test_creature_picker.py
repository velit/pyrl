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
    assert CreaturePicker._picking_weight(0, PyrlCreature.GWORM.template)    == 1000 *  200
    assert CreaturePicker._picking_weight(0, PyrlCreature.GBAT.template)     == 512  * 1000
    assert CreaturePicker._picking_weight(0, PyrlCreature.IMP.template)      == 216  *  400
    assert CreaturePicker._picking_weight(0, PyrlCreature.GOBLIN.template)   == 64   * 1000
    assert CreaturePicker._picking_weight(0, PyrlCreature.KOBOLD.template)   == 8    * 1000
    assert CreaturePicker._picking_weight(0, PyrlCreature.SKELETON.template) == 0    * 1000
    assert CreaturePicker._picking_weight(0, PyrlCreature.ZOMBIE.template)   == 0    *  500
    assert CreaturePicker._picking_weight(0, PyrlCreature.GNOLL.template)    == 0    * 1000
    assert CreaturePicker._picking_weight(0, PyrlCreature.GSPIDER.template)  == 0    * 1000
    assert CreaturePicker._picking_weight(0, PyrlCreature.ORC.template)      == 0    * 1000
    assert CreaturePicker._picking_weight(0, PyrlCreature.GHOST.template)    == 0    * 1000
    assert CreaturePicker._picking_weight(0, PyrlCreature.FIMP.template)     == 0    * 1000

    assert CreaturePicker._picking_weight(20, PyrlCreature.GWORM.template)    == 0   *  200
    assert CreaturePicker._picking_weight(20, PyrlCreature.GBAT.template)     == 271 * 1000
    assert CreaturePicker._picking_weight(20, PyrlCreature.IMP.template)      == 488 *  400
    assert CreaturePicker._picking_weight(20, PyrlCreature.GOBLIN.template)   == 657 * 1000
    assert CreaturePicker._picking_weight(20, PyrlCreature.KOBOLD.template)   == 784 * 1000
    assert CreaturePicker._picking_weight(20, PyrlCreature.SKELETON.template) == 875 * 1000
    assert CreaturePicker._picking_weight(20, PyrlCreature.ZOMBIE.template)   == 875 *  500
    assert CreaturePicker._picking_weight(20, PyrlCreature.GNOLL.template)    == 936 * 1000
    assert CreaturePicker._picking_weight(20, PyrlCreature.GSPIDER.template)  == 973 * 1000
    assert CreaturePicker._picking_weight(20, PyrlCreature.ORC.template)      == 992 * 1000
    assert CreaturePicker._picking_weight(20, PyrlCreature.GHOST.template)    == 999 * 1000
    assert CreaturePicker._picking_weight(20, PyrlCreature.FIMP.template)     == 1000 * 1000
