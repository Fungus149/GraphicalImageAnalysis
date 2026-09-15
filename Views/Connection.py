# Views/Connection.py

from customtkinter import *
import tkinter as Tk

from Interfaces.IClickable import IClickable
from ViewModels.MainViewModel import ViewModel as MainViewModel

class View(IClickable):
    def __init__(self, viewmodel: MainViewModel, parentTag: str, childTag: str, workspace: CTkCanvas, diagramTag: str) -> None:
        super().__init__()
        self.bg1: int
        self.bg2: int
        self.bg3: int

        self.mainViewmodel: MainViewModel = viewmodel
        self.workspace: CTkCanvas = workspace
        self.diagramTag: str = diagramTag
        self.parentTag: str = parentTag
        self.childTag: str = childTag

    def Instantiate(self) -> None:
        outX0, outY0, outXf, outYf = self.workspace.coords(self.childTag)
        x0: float = (outX0 + outXf) / 2
        y0: float = (outY0 + outYf) / 2

        inX0, inY0, inXf, inYf = self.workspace.coords(self.parentTag)
        xf: float = (inX0 + inXf) / 2
        yf: float = (inY0 + inYf) / 2

        midX: float = round((x0 + xf) / 2)

        self.bg1 = self.workspace.create_line(
            x0, y0,
            midX, y0,
            fill=self.mainViewmodel.accentColor,
            width=4,
            tags=(self.diagramTag)
        )
        self.bg2 = self.workspace.create_line(
            midX, y0,
            midX, yf,
            fill=self.mainViewmodel.accentColor,
            width=4,
            tags=(self.diagramTag)
        )
        self.bg3 = self.workspace.create_line(
            midX, yf,
            xf, yf,
            fill=self.mainViewmodel.accentColor,
            width=4,
            tags=(self.diagramTag)
        )
        self.workspace.tag_lower(self.bg1)
        self.workspace.tag_lower(self.bg2)
        self.workspace.tag_lower(self.bg3)

        self.workspace.tag_bind(self.bg1,"<Button-1>", self.OnClick)
        self.workspace.tag_bind(self.bg2,"<Button-1>", self.OnClick)
        self.workspace.tag_bind(self.bg3,"<Button-1>", self.OnClick)

    def OnClick(self, event: Tk.Event) -> None | str:
        if not self.isDown:
            self.OnSelected()
        else:
            self.OnDeselected()
    
    def OnSelected(self) -> None:
        self.workspace.itemconfig(self.bg1, fill=self.mainViewmodel.accentHighlights)
        self.workspace.itemconfig(self.bg2, fill=self.mainViewmodel.accentHighlights)
        self.workspace.itemconfig(self.bg3, fill=self.mainViewmodel.accentHighlights)
        self.isDown = True
        selected: tuple[str, IClickable] | None = self.mainViewmodel.selected
        if selected:
            selected[1].OnDeselected()

        self.mainViewmodel.selected = ("Connection", self)
    
    def OnDeselected(self) -> None:
        self.workspace.itemconfig(self.bg1, fill=self.mainViewmodel.accentColor)
        self.workspace.itemconfig(self.bg2, fill=self.mainViewmodel.accentColor)
        self.workspace.itemconfig(self.bg3, fill=self.mainViewmodel.accentColor)
        self.isDown = False
        self.mainViewmodel.selected = None

    def UpdatePosition(self):
        outX0, outY0, outXf, outYf = self.workspace.coords(self.childTag)
        x0: float = (outX0 + outXf) / 2
        y0: float = (outY0 + outYf) / 2

        inX0, inY0, inXf, inYf = self.workspace.coords(self.parentTag)
        xf: float = (inX0 + inXf) / 2
        yf: float = (inY0 + inYf) / 2

        midX: float = round((x0 + xf) / 2)

        self.workspace.coords(
            self.bg1,
            x0, y0,
            midX, y0
        )
        self.workspace.coords(
            self.bg2,
            midX, y0,
            midX, yf
        )
        self.workspace.coords(
            self.bg3,
            midX, yf,
            xf, yf
        )