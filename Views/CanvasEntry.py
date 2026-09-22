# Views/CanvasEntry
from typing import Literal
from collections.abc import Callable
from customtkinter import *
import tkinter as Tk

from Presenters.MainPresenter import Presenter as MainPresenter

class CanvasEntry:
    def __init__(
            self, 
            blockTag: str, 
            label: str, 
            type: Literal["str", "float", "int"], 
            posX: float, 
            posY: float, 
            onChange: Callable[[float], None], 
            mainPresenter: MainPresenter
        ) -> None:
        
        self.itemWidth: int = 106
        self.itemHeight: int = 24

        self.onChange: Callable[[float], None] = onChange
        self.mainPresenter: MainPresenter = mainPresenter
        self.workspace: CTkCanvas = mainPresenter.workspace
        self.type: Literal["str", "float", "int"] = type
        self.diagramTag: str = mainPresenter.diagramTag
        self.blockTag: str = blockTag
        self.label: str = label

        self.entry: CTkEntry = CTkEntry(
            self.workspace,
            width=self.itemWidth,
            height=self.itemHeight,
            border_width=1
        )
        self.window: int = self.workspace.create_window(
            posX+14,
            posY,
            window=self.entry,
            anchor="w",
            tags=(blockTag, self.diagramTag)
        )
        self.entry.insert(0, self.label)

        self.entry.bind("<Return>", self.OnEnter)
        self.entry.bind("<FocusOut>", self.OnFocusOut)

    def OnEnter(self, event: Tk.Event) -> None:
        self.entry.selection_clear()
        self.workspace.focus_set()

    def OnFocusOut(self, event: Tk.Event) -> None:
        self.Commit()

    def Commit(self) -> None:
        text: str = self.entry.get()
        try:
            value: float = float(text)
        except ValueError:
            self.entry.delete(0, "end")
            self.entry.insert(0, self.label)
            return

        self.onChange(value)

    def OnZoom(self) -> None:
        scale = self.mainPresenter.scale
        self.entry.configure(
            width=int(self.itemWidth * scale),
            height=int(self.itemHeight * scale)
        )

    def Delete(self) -> None:
        self.workspace.delete(self.window)
        self.entry.destroy()