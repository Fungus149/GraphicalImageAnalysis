# Views/MainView.py
from typing import cast

from customtkinter import *
import tkinter as Tk

from Interfaces.IClickable import IClickable

from Views.BlockView import View as blocksViews
from Views.MenuBar import View as menuBarView
from ViewModels.MainViewModel import ViewModel

class View():
    def __init__(self, viewmodel: ViewModel, root: CTk) -> None:
        self.menuFrame: CTkFrame
        self.workspace: CTkCanvas
        self.lastX: float
        self.lastY: float

        self.menuBar: menuBarView = menuBarView(root, viewmodel)
        self.blocks: list[blocksViews] = []
        self.diagramTag: str = "diagram"
        self.lastBlockId: int = 0

        self.viewmodel: ViewModel = viewmodel
        self.root: CTk = root

        self.root.bind("<Button-1>", self.OnGlobalClick)

    def Execute(self) -> None:
        self.root.title("Graphical Image Analysis Tool")
        
        self.CreateMainFrame()
        self.CreateMenuBar()
        # self.CreateBlocksMenu()
        
        self.menuFrame.pack(fill="x")
        self.workspace.pack(fill="both", expand=True)

        self.root.after(100, lambda: self.root.state("zoomed"))
        
        self.workspace.bind("<Button-1>", self.OnWorkspaceClick)
        self.workspace.bind("<Button-2>", self.OnPanStart)
        self.workspace.bind("<B2-Motion>", self.OnPan)
        self.workspace.bind("<MouseWheel>", self.OnZoom)

        block = blocksViews(self.viewmodel,self.lastBlockId, self.workspace, self.diagramTag)
        block.Instantiate(200,200)
        self.blocks.append(block)
        self.lastBlockId+=1

        block2 = blocksViews(self.viewmodel,self.lastBlockId, self.workspace, self.diagramTag)
        block2.Instantiate(400,200)
        self.blocks.append(block2)
        self.lastBlockId+=1

        block3 = blocksViews(self.viewmodel,self.lastBlockId, self.workspace, self.diagramTag)
        block3.Instantiate(400,200)
        self.blocks.append(block3)
        self.lastBlockId+=1
   
    # def Resize(self):

    def CreateMenuBar(self) -> None:
        self.menuFrame = self.menuBar.CreateMenuBar()

    def CreateMainFrame(self) -> None:
        self.workspace: CTkCanvas = CTkCanvas(
            self.root,
            bg="#0F0F0F",
            bd = 0,
            highlightthickness = 0
        )

    # def CreateBlocksMenu(self):
    #     inputBlocksBtn: CTkButton = CTkButton

    def OnGlobalClick(self, event: Tk.Event) -> None:
        widget: CTkFrame = cast(CTkFrame, event.widget)
        self.menuBar.OnGlobalClick(widget)

    def OnWorkspaceClick(self, event: Tk.Event) -> None:
        items = self.workspace.find_overlapping(
            event.x, event.y,
            event.x, event.y
        )
        selected: tuple[str,IClickable] | None = self.viewmodel.selected

        if items or not selected:
            return

        selected[1].OnDeselected()
        self.viewmodel.selected = None

    def OnPanStart(self, event: Tk.Event) -> None:
        self.lastX = self.workspace.canvasx(event.x)
        self.lastY = self.workspace.canvasy(event.y)

    def OnPan(self, event: Tk.Event) -> None:
        x = self.workspace.canvasx(event.x)
        y = self.workspace.canvasy(event.y)
        dx = x - self.lastX
        dy = y - self.lastY

        self.workspace.move(self.diagramTag, dx, dy)

        self.lastX = x
        self.lastY = y
        self.viewmodel.ChangeOffset(dx,dy)

    def OnZoom(self, event: Tk.Event) -> None:
        zoom: float = 1 + 0.1 * round(event.delta / 120)
        scale: float = self.viewmodel.scale.get() * zoom
        if scale > 0.1 and scale < 10:
            self.workspace.scale(self.diagramTag, event.x, event.y, zoom, zoom )
            for block in self.blocks:
                block.OnZoom()

            self.viewmodel.OnZoom(zoom, event.x, event.y)
        