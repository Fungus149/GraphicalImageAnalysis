# Views/BlockView.py
from customtkinter import *
import tkinter as Tk

from Interfaces.IClickable import IClickable
from Views.InNode import View as InNodeView
from Views.OutNode import View as OutNodeView
from ViewModels.MainPresenter import Presenter as MainPresenter
from ViewModels.BlockPresenter import Presenter

class View(IClickable):
    def __init__(self, mainPresenter: MainPresenter, blockId: int, workspace: CTkCanvas, diagramTag: str) -> None:
        super().__init__()
        self.nodesIn: list[InNodeView] = []
        self.nodesOut: list[OutNodeView] = []
        self.label: int
        self.lastX: int
        self.lastY: int

        self.normalWidth: float = 240
        self.normalHeight: float = 160

        self.mainPresenter: MainPresenter = mainPresenter
        self.workspace: CTkCanvas = workspace
        self.diagramTag: str = diagramTag
        self.blockTag: str = f'block_{blockId}'
        self.blockId: int = blockId

    def Instantiate(self, posX: int, posY: int) -> None:
        self.presenter: Presenter = Presenter(posX, posY)

        self.bg: int = self.workspace.create_rectangle(
            posX-self.normalWidth/2, 
            posY-self.normalHeight/2, 
            posX+self.normalWidth/2, 
            posY+self.normalHeight/2,
            fill = "#1F1F1F",
            outline = "#4F4F4F",
            tags=(self.blockTag, self.diagramTag)
        )
        self.MakeLabel("block",posX,posY)
        self.MakeConnectors(2,1,posX,posY)

        self.workspace.tag_bind(self.bg,"<Button-1>", self.OnClick)
        self.workspace.tag_bind(self.bg,"<B1-Motion>", self.OnDrag)
    
    def MakeLabel(self, label: str, posX: int, posY: int) -> None:
        self.label = self.workspace.create_text(
            posX,
            posY - self.normalHeight/2 + 8,
            text = label,
            font = ("Arial", 14, "bold"),
            fill = "#B6B6B6",
            tags = (self.blockTag, self.diagramTag)
        )
        self.workspace.tag_bind(self.label,"<Button-1>", self.OnClick)

    def MakeConnectors(self, numInputs: int, numOutputs: int, posX: int, posY: int) -> None:
        for input in range(numInputs):
            node = InNodeView(self, input, self.mainPresenter, self.workspace, self.diagramTag)
            node.Instantiate(round(posX-self.normalWidth/2), round(posY-self.normalHeight/2 + (input+1) * self.normalHeight/(numInputs+1)))
            self.nodesIn.append(node)
        for output in range(numOutputs):
            node = OutNodeView(self, output, self.mainPresenter, self.workspace, self.diagramTag)
            node.Instantiate(round(posX+self.normalWidth/2), round(posY-self.normalHeight/2 + (output+1) * self.normalHeight/(numOutputs+1)))
            self.nodesOut.append(node)

    def OnClick(self, event: Tk.Event) -> None:
        selectedItems: list[IClickable] = self.mainPresenter.selected
        self.lastX = event.x
        self.lastY = event.y

        if self not in selectedItems:
            for item in selectedItems.copy():
                item.OnDeselected()
        else:
            self.OnDeselected()

        if not self.isDown:
            self.OnSelected()
        else:
            self.OnDeselected()
    
    def OnSelected(self) -> None:
        self.workspace.itemconfig(self.bg, fill="#4F4F4F")

        self.mainPresenter.selected.append(self)
        self.isDown = True
    
    def OnDeselected(self) -> None:
        self.workspace.itemconfig(self.bg, fill="#1F1F1F")
        
        self.mainPresenter.selected.remove(self)
        self.isDown = False

    def OnDrag(self, event: Tk.Event):
        dx: float
        dy: float

        selectedItems: list[IClickable] = self.mainPresenter.selected
        scale: float = self.mainPresenter.scale

        if int(event.state) & 0x0004:
            absX: float = (event.x - self.mainPresenter.offsetX) / scale
            absY: float = (event.y - self.mainPresenter.offsetY) / scale
            dx = round(absX / self.normalWidth) * self.normalWidth - self.presenter.absPosX
            dy = round(absY / self.normalHeight) * self.normalHeight - self.presenter.absPosY
        else:
            dx = (event.x - self.lastX) / scale
            dy = (event.y - self.lastY) / scale

        if len(selectedItems) == 0:
            self.OnSelected()
            
        for item in selectedItems:
            if isinstance(item, View):
                item.presenter.ChangePosition(dx, dy)
                item.UpdatePosition()
                item.UpdateConnectionsPositions()

        self.lastX = event.x
        self.lastY = event.y

    def OnZoom(self) -> None:
        self.workspace.itemconfigure(
            self.label, 
            font=("Arial", round(self.mainPresenter.labelFont), "bold")
        )

    def UpdateConnectionsPositions(self):
        for node in self.nodesOut:
            for connection in node.connections:
                connection.UpdatePosition()

        for node in self.nodesIn:
            if node.connection:
                node.connection.UpdatePosition()

    def UpdatePosition(self) -> None:
        scale: float = self.mainPresenter.scale
        dx: float = (self.presenter.absPosX - self.presenter.worldPosX) * scale
        dy: float = (self.presenter.absPosY - self.presenter.worldPosY) * scale 

        self.workspace.move(
            self.blockTag, 
            dx, 
            dy
        )

        self.presenter.worldPosX = self.presenter.absPosX
        self.presenter.worldPosY = self.presenter.absPosY

    def Delete(self) -> None:
        for node in self.nodesIn:
            if node.connection is not None:
                node.connection.Delete()
        for node in self.nodesOut:
            for connection in node.connections.copy():
                connection.Delete()

        self.workspace.delete(self.blockTag)