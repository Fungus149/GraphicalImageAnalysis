# Utilities/CanvasUtilities.py
from customtkinter import *

class CanvasUtilities():
    @staticmethod
    def GetCenter(bg: int, workspace: CTkCanvas) -> tuple[float, float]:
        x0, y0, xf, yf = workspace.coords(bg)
        midX: float = (x0 + xf) / 2
        midY: float = (y0 + yf) / 2
        return (midX, midY)

    # @staticmethod
    # def GetBBox(bg: int, workspace: CTkCanvas) -> tuple[float, float, float, float]:
