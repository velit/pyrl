from pyrl.engine.enums.mods import Mod

def test_mods() -> None:
    for mod in Mod:
        assert f"~{round(mod.mod, 2):.2f}" == mod.approximation, "approximation must match actual mod"
