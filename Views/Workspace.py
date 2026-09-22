# Views/Workspace.py
from customtkinter import *
import tkinter as Tk

from Interfaces.IClickable import IClickable
from Views.Connection import View as ConnectionView
from Views.Block import View as BlockView
from Presenters.MainPresenter import Presenter as MainPresenter
from Presenters.Blocks.ConstantB import Presenter as ConstantPresenter
from Presenters.Blocks.PlotB import Presenter as PlotPresenter

class View():
    def __init__(self, root: CTk, mainPresenter: MainPresenter) -> None:
        self.workspace: CTkCanvas
        self.lastX: float
        self.lastY: float
        self.selectionStartX: float
        self.selectionStartY: float

        self.blocks: list[BlockView] = []
        self.lastBlockId: int = 0
        self.selectionBox: int | None = None

        self.mainPresenter: MainPresenter = mainPresenter
        self.root: CTk = root
    
    def CreateWorkspace(self) -> CTkCanvas:
        self.workspace = CTkCanvas(
            self.root,
            bg="#0F0F0F",
            bd = 0,
            highlightthickness = 0
        )
        self.mainPresenter.workspace = self.workspace

        self.workspace.bind("<Button-1>", self.OnWorkspaceClick)
        self.workspace.bind("<B1-Motion>", self.OnSelectionDrag)
        self.workspace.bind("<ButtonRelease-1>", self.OnSelectionEnd)
        self.workspace.bind("<Button-2>", self.OnPanStart)
        self.workspace.bind("<B2-Motion>", self.OnPan)
        self.workspace.bind("<MouseWheel>", self.OnZoom)
        self.workspace.bind("<KeyRelease-Delete>", self.OnDelete)

        presenter = ConstantPresenter()
        block = BlockView(presenter, self.mainPresenter,self.lastBlockId)
        block.Instantiate(200,200)
        self.blocks.append(block)
        self.lastBlockId+=1

        presenter = ConstantPresenter()
        block2 = BlockView(presenter, self.mainPresenter,self.lastBlockId)
        block2.Instantiate(400,200)
        self.blocks.append(block2)
        self.lastBlockId+=1

        presenter = PlotPresenter()
        block3 = BlockView(presenter, self.mainPresenter,self.lastBlockId)
        block3.Instantiate(400,400)
        self.blocks.append(block3)
        self.lastBlockId+=1

        return self.workspace

    def OnWorkspaceClick(self, event: Tk.Event) -> None:
        items = self.workspace.find_overlapping(
            event.x, event.y,
            event.x, event.y
        )
        if items:
            return
        
        selectedItems: list[IClickable] = self.mainPresenter.selected
        self.selectionStartX = event.x
        self.selectionStartY = event.y

        self.selectionBox = self.workspace.create_rectangle(
            event.x,
            event.y,
            event.x,
            event.y,
            outline="#00F1F1",
            dash=(4, 4),
            tags=("selectionBox",)
        )
        for selected in selectedItems.copy():
            selected.OnDeselected()

    def OnSelectionDrag(self, event: Tk.Event) -> None:
        if self.selectionBox is None:
            return

        self.workspace.coords(
            self.selectionBox,
            self.selectionStartX,
            self.selectionStartY,
            event.x,
            event.y
        )

    def OnSelectionEnd(self, event: Tk.Event) -> None:
        if self.selectionBox is None:
            return

        x0: float = min(self.selectionStartX, event.x)
        y0: float = min(self.selectionStartY, event.y)
        xf: float = max(self.selectionStartX, event.x)
        yf: float = max(self.selectionStartY, event.y)

        items: tuple[int, ...] = self.workspace.find_overlapping(x0, y0, xf, yf)
        if items:
            self.mainPresenter.selected = []
            for item in items:
                for block in self.blocks:
                    if block.bg == item:
                        block.OnSelected()

        self.workspace.delete(self.selectionBox)
        self.selectionBox = None

    def OnPanStart(self, event: Tk.Event) -> None:
        self.lastX = self.workspace.canvasx(event.x)
        self.lastY = self.workspace.canvasy(event.y)

    def OnPan(self, event: Tk.Event) -> None:
        x: float = self.workspace.canvasx(event.x)
        y: float = self.workspace.canvasy(event.y)

        dx: float = x - self.lastX
        dy: float = y - self.lastY
        self.workspace.move(self.mainPresenter.diagramTag, dx, dy)

        self.lastX = x
        self.lastY = y
        self.mainPresenter.ChangeOffset(dx,dy)

    def OnZoom(self, event: Tk.Event) -> None:
        zoom: float = 1 + 0.1 * round(event.delta / 120)

        scale: float = self.mainPresenter.scale * zoom
        if scale > 0.1 and scale < 10:
            self.workspace.scale(self.mainPresenter.diagramTag, event.x, event.y, zoom, zoom )
            for block in self.blocks:
                block.OnZoom()

            self.mainPresenter.OnZoom(zoom, event.x, event.y)

    def OnDelete(self, event: Tk.Event) -> None:
        selectedItems: list[IClickable] = self.mainPresenter.selected
        for item in selectedItems.copy():
            if isinstance(item, BlockView):
                item.OnDeselected()
                self.blocks.remove(item)
                item.Delete()
            elif type(item) is ConnectionView:
                item.OnDeselected()
                item.Delete()
