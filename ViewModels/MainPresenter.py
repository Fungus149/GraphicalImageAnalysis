# ViewModels/MainViewModel.py
from Interfaces.IClickable import IClickable

class Presenter:
    def __init__(self) -> None:
        # self.accentColor: str = "#004141"
        # self.accentHighlights: str = "#00F1F1"
        self.accentColor: str = "#004141"
        self.accentHighlights: str = "#00F1F1"
        self.selected: list[IClickable] = []
        self.offsetX: float = 0
        self.offsetY: float = 0
        self.scale: float =1
        self.labelFont: float = 14

    def ChangeOffset(self, dx: float, dy: float) -> None:
        self.offsetX = round(self.offsetX+dx, 2)
        self.offsetY = round(self.offsetY+dy, 2)

    def OnZoom(self, zoom: float, anchorX: float, anchorY: float) -> None:
        self.offsetX = anchorX - (anchorX - self.offsetX) * zoom
        self.offsetY = anchorY - (anchorY - self.offsetY) * zoom
        self.scale = self.scale * zoom
        self.labelFont = self.labelFont * zoom