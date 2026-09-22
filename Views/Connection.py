# Views/Connection.py
from customtkinter import *
import tkinter as Tk

from Interfaces.IClickable import IClickable
from Presenters.MainPresenter import Presenter as MainPresenter

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Views.OutNode import View as OutNodeView
    from Views.InNode import View as InNodeView

class View(IClickable):
    def __init__(self, mainPresenter: MainPresenter, parent: OutNodeView, child: InNodeView) -> None:
        super().__init__()
        self.bg1: int
        self.bg2: int
        self.bg3: int

        self.mainPresenter: MainPresenter = mainPresenter
        self.parent: OutNodeView = parent
        self.child: InNodeView = child
        self.workspace: CTkCanvas = mainPresenter.workspace

    def Instantiate(self) -> None:
        outX0, outY0, outXf, outYf = self.workspace.coords(self.child.nodeTag)
        x0: float = (outX0 + outXf) / 2
        y0: float = (outY0 + outYf) / 2

        inX0, inY0, inXf, inYf = self.workspace.coords(self.parent.nodeTag)
        xf: float = (inX0 + inXf) / 2
        yf: float = (inY0 + inYf) / 2

        midX: float = round((x0 + xf) / 2)
        self.bg1 = self.workspace.create_line(
            x0, y0,
            midX, y0,
            fill=self.mainPresenter.accentColor,
            width=4,
            tags=(self.mainPresenter.diagramTag)
        )
        self.bg2 = self.workspace.create_line(
            midX, y0,
            midX, yf,
            fill=self.mainPresenter.accentColor,
            width=4,
            tags=(self.mainPresenter.diagramTag)
        )
        self.bg3 = self.workspace.create_line(
            midX, yf,
            xf, yf,
            fill=self.mainPresenter.accentColor,
            width=4,
            tags=(self.mainPresenter.diagramTag)
        )
        self.workspace.tag_lower(self.bg1)
        self.workspace.tag_lower(self.bg2)
        self.workspace.tag_lower(self.bg3)

        self.workspace.tag_bind(self.bg1,"<Button-1>", self.OnClick)
        self.workspace.tag_bind(self.bg2,"<Button-1>", self.OnClick)
        self.workspace.tag_bind(self.bg3,"<Button-1>", self.OnClick)

    def OnClick(self, event: Tk.Event) -> None:
        selectedItems: list[IClickable] = self.mainPresenter.selected
        for item in selectedItems.copy():
            if item != self:
                item.OnDeselected()

        if not self.isDown:
            self.OnSelected()
        else:
            self.OnDeselected()
    
    def OnSelected(self) -> None:
        self.workspace.itemconfig(self.bg1, fill=self.mainPresenter.accentHighlights)
        self.workspace.itemconfig(self.bg2, fill=self.mainPresenter.accentHighlights)
        self.workspace.itemconfig(self.bg3, fill=self.mainPresenter.accentHighlights)

        self.mainPresenter.selected.append(self)
        self.isDown = True
    
    def OnDeselected(self) -> None:
        self.workspace.itemconfig(self.bg1, fill=self.mainPresenter.accentColor)
        self.workspace.itemconfig(self.bg2, fill=self.mainPresenter.accentColor)
        self.workspace.itemconfig(self.bg3, fill=self.mainPresenter.accentColor)
        
        self.mainPresenter.selected.remove(self)
        self.isDown = False

    def UpdatePosition(self):
        outX0, outY0, outXf, outYf = self.workspace.coords(self.child.nodeTag)
        x0: float = (outX0 + outXf) / 2
        y0: float = (outY0 + outYf) / 2

        inX0, inY0, inXf, inYf = self.workspace.coords(self.parent.nodeTag)
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

    def Delete(self):
        self.parent.connections.remove(self)
        self.child.connection = None
        self.workspace.delete(self.bg1)
        self.workspace.delete(self.bg2)
        self.workspace.delete(self.bg3)