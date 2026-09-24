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
            onChange: Callable[[list[list[float | int | str]]], None], 
            mainPresenter: MainPresenter
        ) -> None:

        self.tooltip: CTkToplevel | None = None
        self.tooltipAfter: str | None = None
        self.itemWidth: int = 106
        self.itemHeight: int = 24

        self.onChange: Callable[[list[list[float | int | str]]], None] = onChange
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
        self.entry.bind("<Enter>", self.OnMouseEnter)
        self.entry.bind("<Leave>", self.OnMouseLeave)

    def OnEnter(self, event: Tk.Event) -> None:
        self.entry.selection_clear()
        self.workspace.focus_set()

    def OnFocusOut(self, event: Tk.Event) -> None:
        self.Commit()

    def Disable(self):
        self.entry.configure(
            text_color = "#888888",
            state='disabled',
        )
        self.entry.delete(0, "end")
        self.entry.insert(0, self.label)

    def Enable(self):
        self.entry.configure(
            text_color = "#D9E1EC",
            state='normal',
        )

    def Commit(self) -> None:
        value: float | int | str

        text: str = self.entry.get()

        try:
            match self.type:
                case "float":
                    value = float(text)
                case "int":
                    value = int(text)
                case "str":
                    value = text
        except ValueError:
            self.entry.delete(0, "end")
            self.entry.insert(0, self.label)
            return

        self.onChange([[value]])

    def OnMouseEnter(self, event: Tk.Event) -> None:
        self.tooltipAfter = self.entry.after(
            500,
            self.ShowTooltip
        )

    def OnMouseLeave(self, event: Tk.Event) -> None:
        if self.tooltipAfter is not None:
            self.entry.after_cancel(self.tooltipAfter)
            self.tooltipAfter = None

        if self.tooltip is not None:
            self.tooltip.destroy()
            self.tooltip = None

    def ShowTooltip(self) -> None:
        x: int = self.entry.winfo_rootx()
        y: int = self.entry.winfo_rooty()

        self.tooltip = CTkToplevel(self.entry)
        self.tooltip.overrideredirect(True)

        CTkLabel(
            self.tooltip,
            text=self.label
        ).pack(padx=5, pady=3)

        self.tooltip.update_idletasks()
        self.tooltip.geometry(f"+{x}+{y}")

    def OnZoom(self) -> None:
        scale = self.mainPresenter.scale
        self.entry.configure(
            width=int(self.itemWidth * scale),
            height=int(self.itemHeight * scale)
        )

    def Delete(self) -> None:
        self.workspace.delete(self.window)
        self.entry.destroy()