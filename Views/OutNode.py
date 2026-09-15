# Views/OutNode.py
from customtkinter import *
import tkinter as Tk

from Interfaces.IClickable import IClickable
from Views.Connection import View as ConnectionView
from ViewModels.MainViewModel import ViewModel as MainViewModel

from typing import TYPE_CHECKING, Any
if TYPE_CHECKING:
    from Views.BlockView import View as blockView

class View(IClickable):
    def __init__(self, parent: blockView, id: int, mainViewmodel: MainViewModel, workspace: CTkCanvas, diagramTag: str) -> None:
        super().__init__()
        
        self.connections: list[ConnectionView]  = []
        self.mainViewmodel: MainViewModel = mainViewmodel
        self.parent: blockView = parent
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
            fill = self.mainViewmodel.accentColor,
            outline = "#4F4F4F",
            tags=(self.nodeTag, self.parent.blockTag, self.diagramTag)
        )
        self.workspace.tag_bind(self.bg, "<Button-1>", self.OnClick)

    def OnClick(self, event: Tk.Event) -> None | str:
        if not self.isDown:
            self.OnSelected()
        else:
            self.OnDeselected()

    def OnSelected(self) -> None:
        print("selecting out node")
        self.workspace.itemconfig(self.bg, fill=self.mainViewmodel.accentHighlights)
        self.isDown = True
        selected: tuple[str, IClickable] | None = self.mainViewmodel.selected
        if selected:
            selected[1].OnDeselected()

        self.mainViewmodel.selected = ("OutNode", self)

    def OnDeselected(self) -> None:
        self.workspace.itemconfig(self.bg, fill=self.mainViewmodel.accentColor)
        self.isDown = False
        self.mainViewmodel.selected = None