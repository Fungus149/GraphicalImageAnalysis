# ViewModels/MainViewModel.py
from __future__ import annotations
import customtkinter as CTk

from Interfaces.IClickable import IClickable

from typing import TYPE_CHECKING, Any
if TYPE_CHECKING:
    from Views.InNode import View as InNodeView

class ViewModel:
    def __init__(self) -> None:
        # self.accentColor: str = "#004141"
        # self.accentHighlights: str = "#00F1F1"
        self.accentColor: str = "#004100"
        self.accentHighlights: str = "#00F100"
        self.selected: tuple[str,IClickable] | None = None
        self.offsetX: CTk.DoubleVar = CTk.DoubleVar(value=0)
        self.offsetY: CTk.DoubleVar = CTk.DoubleVar(value=0)
        self.scale: CTk.DoubleVar = CTk.DoubleVar(value=1)
        self.labelFont: CTk.DoubleVar = CTk.DoubleVar(value=14)

    def ChangeOffset(self, dx: float, dy: float) -> None:
        self.offsetX.set(round(self.offsetX.get()+dx, 2))
        self.offsetY.set(round(self.offsetY.get()+dy, 2))

    def OnZoom(self, zoom: float, anchorX: float, anchorY: float) -> None:
        self.offsetX.set(anchorX - (anchorX - self.offsetX.get()) * zoom)
        self.offsetY.set(anchorY - (anchorY - self.offsetY.get()) * zoom)
        self.scale.set(self.scale.get()*zoom)
        labelFont = self.labelFont.get()*zoom
        self.labelFont.set(labelFont)

