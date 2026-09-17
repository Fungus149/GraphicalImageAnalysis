# Views/OutNode.py
from customtkinter import *
import tkinter as Tk

from Interfaces.IClickable import IClickable
from Views.Connection import View as ConnectionView
from ViewModels.MainPresenter import Presenter as MainPresenter

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Views.Block import View as BlockView

class View(IClickable):
    def __init__(self, parent: BlockView, id: int, mainPresenter: MainPresenter, workspace: CTkCanvas, diagramTag: str) -> None:
        super().__init__()
        
        self.connections: list[ConnectionView]  = []
        self.mainPresenter: MainPresenter = mainPresenter
        self.parent: BlockView = parent
        self.workspace: CTkCanvas = workspace
        self.diagramTag: str = diagramTag
        self.nodeTag: str = f"OutNode {parent.blockId}, {id}"
        self.radius: float = 14
        self.id: int = id

    def Instantiate(self, posX: int, posY: int) -> None:
        self.bg = self.workspace.create_oval(
            posX-self.radius, 
            posY-self.radius, 
            posX+self.radius, 
            posY+self.radius,
            fill = self.mainPresenter.accentColor,
            outline = "#4F4F4F",
            tags=(self.nodeTag, self.parent.blockTag, self.diagramTag)
        )
        self.workspace.tag_bind(self.bg, "<Button-1>", self.OnClick)

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
        self.workspace.itemconfig(self.bg, fill=self.mainPresenter.accentHighlights)

        self.mainPresenter.selected.append(self)
        self.isDown = True

    def OnDeselected(self) -> None:
        self.workspace.itemconfig(self.bg, fill=self.mainPresenter.accentColor)
        
        self.mainPresenter.selected.remove(self)
        self.isDown = False