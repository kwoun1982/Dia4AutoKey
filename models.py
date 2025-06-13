from __future__ import annotations

from pydantic import BaseModel, Field, validator
from typing import List, Literal, Optional

class KeyAction(BaseModel):
    """Represents a single keyboard or mouse action."""

    type: Literal["key", "mouse"] = Field(..., description="Action type")
    code: str = Field(..., description="Key name or mouse button")
    delay_ms: int = Field(0, ge=0, description="Delay after action in milliseconds")

    @validator("code")
    def validate_code(cls, v: str) -> str:
        if not v:
            raise ValueError("code must not be empty")
        return v

class MacroProfile(BaseModel):
    """Profile describing a macro bound to a hotkey."""

    hotkey: str = Field(..., description="Global hotkey")
    description: Optional[str] = Field(None, description="Macro description")
    actions: List[KeyAction] = Field(default_factory=list, description="Action sequence")
    loop: int = Field(1, ge=1, description="Number of repetitions")
    delay_between_loops_ms: int = Field(0, ge=0, description="Delay between loops")
