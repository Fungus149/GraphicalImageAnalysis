# Utilities/BlockRequestor.py
from typing import Literal

class InNodeRequest():
    def __init__(
            self, 
            label: str, 
            type: Literal["label", "entry"], 
            entryType: Literal["str", "float", "int"] | None = None,
            isVisible: bool = True
        ) -> None:
        self.label: str = label
        self.type: Literal["label", "entry"] = type
        self.entryType: Literal["str", "float", "int"] | None = entryType
        self.isVisible: bool = isVisible
        
class OutNodeRequest():
    def __init__(self, label: str = ""):
        self.label: str = label