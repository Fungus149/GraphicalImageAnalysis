# ViewModels/MainViewModel.py
from typing import Callable
from Interfaces.IClickable import IClickable

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from customtkinter import *
    import tkinter as Tk

class Presenter:
    def __init__(self) -> None:
        self.workspace: CTkCanvas
        self.diagramTag: str = "diagram"

        self.selected: list[IClickable] = []
        self.scrollHandler: Callable[[Tk.Event], str] | None = None
        self.accentColor: str = "#004141"
        self.accentHighlights: str = "#00F1F1"
        self.offsetX: float = 0
        self.offsetY: float = 0
        self.scale: float = 1
        self.labelFont: float = 14
        self.headerFont: float = 10

    def ChangeOffset(self, dx: float, dy: float) -> None:
        self.offsetX = round(self.offsetX+dx, 2)
        self.offsetY = round(self.offsetY+dy, 2)

    def OnZoom(self, zoom: float, anchorX: float, anchorY: float) -> None:
        self.offsetX = anchorX - (anchorX - self.offsetX) * zoom
        self.offsetY = anchorY - (anchorY - self.offsetY) * zoom
        self.scale = self.scale * zoom
        self.labelFont = self.labelFont * zoom
        self.headerFont = self.headerFont * zoom