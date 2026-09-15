# Views/BlockView.py
from typing import  cast
from customtkinter import *
from abc import ABC, abstractmethod
import tkinter as Tk

from Interfaces.IClickable import IClickable
from Views.InNode import View as InNodeView
from Views.OutNode import View as OutNodeView
from ViewModels.MainViewModel import ViewModel as MainViewModel
from ViewModels.BlockViewModel import ViewModel

class View(IClickable):
    def __init__(self, viewmodel: MainViewModel, id: int, workspace: CTkCanvas, diagramTag: str) -> None:
        super().__init__()
        self.nodesIn: list[InNodeView] = []
        self.nodesOut: list[OutNodeView] = []
        self.label: int
        self.lastX: int
        self.lastY: int

        self.normalWidth: float = 240
        self.normalHeight: float = 160

        self.mainViewmodel: MainViewModel = viewmodel
        self.workspace: CTkCanvas = workspace
        self.diagramTag: str = diagramTag
        self.blockTag: str = f'block_{id}'
        self.blockId: int = id

    def Instantiate(self, posX: int, posY: int) -> None:
        self.viewmodel: ViewModel = ViewModel(posX, posY)

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
        # accepts int,int for how many inputs and outputs
        for input in range(numInputs):
            node = InNodeView(self, input, self.mainViewmodel, self.workspace, self.diagramTag)
            node.Instantiate(round(posX-self.normalWidth/2), round(posY-self.normalHeight/2 + (input+1) * self.normalHeight/(numInputs+1)))
            self.nodesIn.append(node)
        for output in range(numOutputs):
            node = OutNodeView(self, output, self.mainViewmodel, self.workspace, self.diagramTag)
            node.Instantiate(round(posX+self.normalWidth/2), round(posY-self.normalHeight/2 + (output+1) * self.normalHeight/(numOutputs+1)))
            self.nodesOut.append(node)

    def MakeLabels(self) -> None:
        pass

    def OnDrag(self, event: Tk.Event) -> None:
        scale = self.mainViewmodel.scale.get()
        if cast(int, event.state) & 0x0004:
            absX: float = (event.x - self.mainViewmodel.offsetX.get()) / scale
            absY: float = (event.y - self.mainViewmodel.offsetY.get()) / scale
            self.viewmodel.absPosX = round(absX / self.normalWidth) * self.normalWidth
            self.viewmodel.absPosY = round(absY / self.normalHeight) * self.normalHeight
        else:
            self.viewmodel.absPosX += (event.x - self.lastX) / scale
            self.viewmodel.absPosY += (event.y - self.lastY) / scale

        self.lastX = event.x
        self.lastY = event.y
        self.UpdatePosition()
        self.UpdateConnectionsPositions()

    def OnZoom(self) -> None:
        self.workspace.itemconfigure(self.label, font=("Arial", round(self.mainViewmodel.labelFont.get()), "bold"))

    def UpdateConnectionsPositions(self):
        for node in self.nodesOut:
            for connection in node.connections:
                connection.UpdatePosition()

        for node in self.nodesIn:
            if node.connection:
                node.connection.UpdatePosition()

    def UpdatePosition(self) -> None:
        scale = self.mainViewmodel.scale.get()
        dx: float = (self.viewmodel.absPosX - self.viewmodel.worldPosX) * scale
        dy: float = (self.viewmodel.absPosY - self.viewmodel.worldPosY) * scale 

        self.workspace.move(
            self.blockTag, 
            dx, 
            dy
        )

        self.viewmodel.worldPosX = self.viewmodel.absPosX
        self.viewmodel.worldPosY = self.viewmodel.absPosY

    def OnClick(self, event: Tk.Event) -> None | str:
        print("Block clicked")
        self.lastX = event.x
        self.lastY = event.y

        if not self.isDown:
            self.OnSelected()
        else:
            self.OnDeselected()
    
    def OnSelected(self) -> None:
        self.workspace.itemconfig(self.bg, fill="#4F4F4F")
        self.isDown = True
        selected: tuple[str, IClickable] | None = self.mainViewmodel.selected
        if selected:
            selected[1].OnDeselected()

        self.mainViewmodel.selected = ("Block", self)
    
    def OnDeselected(self) -> None:
        self.workspace.itemconfig(self.bg, fill="#1F1F1F")
        self.isDown = False
        self.mainViewmodel.selected = None
