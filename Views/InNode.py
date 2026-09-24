# Views/InNode.py
from customtkinter import *
import tkinter as Tk

from Interfaces.IClickable import IClickable
from Views.OutNode import View as OutNodeView
from Views.Connection import View as ConnectionView
from Presenters.MainPresenter import Presenter as MainPresenter

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Views.Block import View as BlockView

class View(IClickable):
    def __init__(self, parent: BlockView, id: int, mainPresenter: MainPresenter) -> None:
        super().__init__()

        self.connection: ConnectionView | None = None
        self.radius: float = 14

        self.mainPresenter: MainPresenter = mainPresenter
        self.parent: BlockView = parent
        self.workspace: CTkCanvas = mainPresenter.workspace
        self.nodeTag: str = f"InNode {parent.blockId}, {id}"
        self.id: int = id

    def Instantiate(self, posX: int, posY: int) -> None:
        self.bg = self.workspace.create_oval(
            posX-self.radius, 
            posY-self.radius, 
            posX+self.radius, 
            posY+self.radius,
            fill = self.mainPresenter.accentColor,
            outline = "#4F4F4F",
            tags=(self.nodeTag, self.parent.blockTag, self.mainPresenter.diagramTag)
        )
        self.workspace.tag_bind(self.bg,"<Button-1>", self.OnClick)

    def OnClick(self, event: Tk.Event) -> None:
        selectedItems: list[IClickable] = self.mainPresenter.selected
        
        self.MakeConnection()
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

    def MakeConnection(self) -> None:
        selectedItems: list[IClickable] = self.mainPresenter.selected

        if self.connection is not None:
            self.connection.Delete()

        if len(selectedItems) != 1 or type(selectedItems[0]) is not OutNodeView:
            return
        
        self.connection = ConnectionView(self.mainPresenter, selectedItems[0], self)
        self.connection.Instantiate()

        selectedItems[0].parent.presenter.outputs[selectedItems[0].id].append((self.parent.presenter,self.id))
        self.parent.presenter.SetInVal(
            self.id,
            selectedItems[0].parent.presenter.outVals[selectedItems[0].id]
        )
        selectedItems[0].connections.append(self.connection)
        self.parent.HideEntry(self.id)