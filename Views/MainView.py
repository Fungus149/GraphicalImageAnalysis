# Views/MainView.py
from typing import cast

from customtkinter import *
import tkinter as Tk

from Interfaces.IClickable import IClickable
from Utilities.CustomWidgets import CustomWidgets
from Utilities.WidgetsUtilities import WidgetsUtilities

from Views.ContextMenusView import View as contextView
from Views.BlockView import View as blocksViews
from ViewModels.MainViewModel import ViewModel

class View():
    def __init__(self, viewmodel: ViewModel, contextMenus: contextView, root: CTk) -> None:
        self.menuFrame: CTkFrame
        self.addMenu: CTkFrame
        self.fileMenu: CTkFrame
        self.editMenu: CTkFrame
        self.workspace: CTkCanvas
        self.fileBtn: CTkButton
        self.editBtn: CTkButton
        self.addBtn: CTkButton
        self.lastX: float
        self.lastY: float

        self.blocks: list[blocksViews] = []
        self.diagramTag: str = "diagram"
        self.lastBlockId: int = 0

        self.viewmodel: ViewModel = viewmodel
        self.contextMenus: contextView = contextMenus
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
   
    # def Resize(self):

    def CreateMenuBar(self) -> None:
        self.menuFrame: CTkFrame = CTkFrame(self.root, fg_color="#4F4F4F")

        self.fileBtn: CTkButton = CustomWidgets.CreateMenuButton(self.menuFrame, "File", self.OnFileMenu)
        self.fileMenu: CTkFrame = self.contextMenus.CreateFilesMenu(self.root)
        self.editBtn: CTkButton = CustomWidgets.CreateMenuButton(self.menuFrame, "Edit", self.OnEditMenu)
        self.editMenu: CTkFrame = self.contextMenus.CreateEditMenu(self.root)
        self.addBtn: CTkButton = CustomWidgets.CreateMenuButton(self.menuFrame, "Add", self.OnAddMenu)
        self.addMenu: CTkFrame = self.contextMenus.CreateAddMenu(self.root)
        
        self.fileBtn.pack(side="left")
        self.editBtn.pack(side="left")
        self.addBtn.pack(side="left")

    def OnFileMenu(self) -> None:
        if self.fileMenu.winfo_ismapped():
            self.fileMenu.place_forget()
            return
        self.fileMenu.place(
            x=self.fileBtn.winfo_x(), 
            y=self.fileBtn.winfo_y() + self.fileBtn.winfo_height()
        )
        
    def OnEditMenu(self) -> None:
        if self.editMenu.winfo_ismapped():
            self.editMenu.place_forget()
            return
        self.editMenu.place(
            x=self.editBtn.winfo_x(), 
            y=self.editBtn.winfo_y() + self.editBtn.winfo_height()
        )

    def OnAddMenu(self) -> None:
        if self.addMenu.winfo_ismapped():
            self.addMenu.place_forget()
            return
        self.addMenu.place(
            x=self.addBtn.winfo_x(), 
            y=self.addBtn.winfo_y() + self.addBtn.winfo_height()
        )

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

        if not WidgetsUtilities.IsChildOf(widget, (self.editBtn, self.editMenu)):
            self.editMenu.place_forget()
        
        if not WidgetsUtilities.IsChildOf(widget, (self.fileBtn, self.fileMenu)):
            self.fileMenu.place_forget()

        if not WidgetsUtilities.IsChildOf(widget, (self.addBtn, self.addMenu)):
            self.addMenu.place_forget()

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
        self.workspace.scale(self.diagramTag, event.x, event.y, zoom, zoom )
        for block in self.blocks:
            block.OnZoom()

        self.viewmodel.OnZoom(zoom, event.x, event.y)
        