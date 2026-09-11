# Interfaces/IClickable.py
from abc import ABC, abstractmethod
import tkinter as Tk


class IClickable(ABC):

    @abstractmethod
    def OnClick(self, event: Tk.Event | None = None) -> None | str:
        pass

    @abstractmethod
    def OnSelected(self) -> None:
        pass

    @abstractmethod
    def OnDeselected(self) -> None:
        pass