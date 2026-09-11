# Views/BlockView.py
from typing import Any
from customtkinter import *
from abc import ABC, abstractmethod
import tkinter as Tk

from Views.InNode import View as InNodeView
from ViewModels.MainViewModel import ViewModel as MainViewModel
from ViewModels.BlockViewModel import ViewModel

class View():
    def __init__(self, viewmodel: MainViewModel, id: int, workspace: CTkCanvas, diagramTag: str) -> None:
        self.bg: int
        self.label: int
        self.lastX: int
        self.lastY: int

        self.normalWidth: float = 240
        self.normalHeight: float = 160

        self.mainViewmodel: MainViewModel = viewmodel
        self.workspace: CTkCanvas = workspace
        self.diagramTag: str = diagramTag
        self.blockTag: str = f'block_{id}'

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

        self.workspace.tag_bind(self.blockTag,"<Button-1>", self.OnPress)
        self.workspace.tag_bind(self.blockTag,"<B1-Motion>", self.OnDrag)
    
        self.MakeLabel("block",posX,posY)
        self.MakeConnectors(2,0,posX,posY)


    @abstractmethod
    def MakeLabel(self, label: str, posX: int, posY: int) -> None:
        self.label = self.workspace.create_text(
            posX,
            posY - self.normalHeight/2 + 8,
            text = label,
            font = ("Arial", 14, "bold"),
            fill = "#B6B6B6",
            tags = (self.blockTag, self.diagramTag)
        )

    @abstractmethod
    def MakeBody(self, inputs:list[tuple[Any, bool]], outputs: list[tuple]) -> None:
        pass

    @abstractmethod
    def MakeConnectors(self, numInputs: int, numOutputs: int, posX: int, posY: int) -> None:
        # accepts int,int for how many inputs and outputs
        for input in range(numInputs):
            node = InNodeView(self.mainViewmodel, self.workspace, self.blockTag, self.diagramTag)
            node.Instantiate(round(posX-self.normalWidth/2), round(posY-self.normalHeight/2 + (input+1) * self.normalHeight/(numInputs+1)))
        for output in range(numOutputs):
            pass

    @abstractmethod
    def MakeLabels(self) -> None:
        pass

    def OnPress(self, event: Tk.Event) -> None:
        self.lastX = event.x
        self.lastY = event.y

    def OnDrag(self, event: Tk.Event) -> None:
        scale = self.mainViewmodel.scale.get()
        if event.state == 268:
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

    def OnZoom(self) -> None:
        self.workspace.itemconfigure(self.label, font=("Arial", round(self.mainViewmodel.labelFont.get()), "bold"))

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
