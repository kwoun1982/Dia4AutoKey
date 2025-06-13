from pydantic import ValidationError

from models import KeyAction, MacroProfile

def test_keyaction_validation():
    action = KeyAction(type="key", code="a", delay_ms=100)
    assert action.code == "a"
    try:
        KeyAction(type="key", code="", delay_ms=0)
    except ValidationError:
        pass
    else:
        assert False, "Validation should fail for empty code"

def test_macroprofile_loop_default():
    mp = MacroProfile(hotkey="F1", actions=[KeyAction(type="key", code="a")])
    assert mp.loop == 1
