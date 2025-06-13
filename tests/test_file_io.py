import json
import tempfile
from pathlib import Path

from models import KeyAction, MacroProfile


def test_save_and_load_tmp_file(tmp_path: Path):
    macros = [MacroProfile(hotkey="F2", actions=[KeyAction(type="key", code="b")])]
    path = tmp_path / "macros.json"
    path.write_text(json.dumps([m.dict() for m in macros], ensure_ascii=False))

    data = json.loads(path.read_text())
    loaded = [MacroProfile(**m) for m in data]
    assert loaded[0].hotkey == "F2"
