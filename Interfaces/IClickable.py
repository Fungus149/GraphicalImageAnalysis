# Interfaces/IClickable.py
from abc import ABC, abstractmethod
import tkinter as Tk


class IClickable(ABC):
    def __init__(self):
        self.isDown: bool = False
        self.bg: int

    @abstractmethod
    def OnClick(self, event: Tk.Event) -> None | str:
        pass

    @abstractmethod
    def OnSelected(self) -> None:
        pass

    @abstractmethod
    def OnDeselected(self) -> None:
        pass