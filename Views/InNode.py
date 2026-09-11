# Views/InNode.py
from customtkinter import *
import tkinter as Tk

from Interfaces.IClickable import IClickable
from ViewModels.MainViewModel import ViewModel as MainViewModel

class View(IClickable):
    def __init__(self, mainViewmodel: MainViewModel, workspace: CTkCanvas, parentTag: str, diagramTag: str) -> None:
        self.bg: int

        self.workspace: CTkCanvas = workspace
        self.mainViewmodel: MainViewModel = mainViewmodel
        self.parentTag: str = parentTag
        self.diagramTag: str = diagramTag
        self.radius: float = 14
        self.isDown: bool = False

    def Instantiate(self, posX: int, posY: int) -> None:
        self.bg = self.workspace.create_oval(
            posX-self.radius, 
            posY-self.radius, 
            posX+self.radius, 
            posY+self.radius,
            fill = "#004141",
            outline = "#4F4F4F",
            tags=(self.parentTag, self.diagramTag)
        )
        self.workspace.tag_bind(self.bg,"<Button-1>", self.OnClick)

    def OnClick(self, event: Tk.Event | None = None) -> None | str:
        if not self.isDown:
            self.OnSelected()
        else:
            self.OnDeselected()

    def OnSelected(self) -> None:
        print("Selected InNode")
        self.workspace.itemconfig(self.bg, fill="#00F1F1")
        self.isDown = True
        selected: tuple[str, IClickable] | None = self.mainViewmodel.selected
        if selected:
            selected[1].OnDeselected()

        self.mainViewmodel.selected = ("InNode", self)

    def OnDeselected(self) -> None:
        print("Deselected InNode")
        self.workspace.itemconfig(self.bg, fill="#004141")
        self.isDown = False
        self.mainViewmodel.selected = None