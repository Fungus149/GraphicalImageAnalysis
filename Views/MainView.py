# Views/MainView.py
from typing import cast

from customtkinter import *
import tkinter as Tk

from Views.MenuBar import View as MenuBarView
from Views.Workspace import View as WorkspaceView
from Presenters.MainPresenter import Presenter as MainPresenter

class View():
    def __init__(self, mainPresenter: MainPresenter, root: CTk) -> None:
        self.menu: MenuBarView
        self.menuFrame: CTkFrame
        self.workspaceCanvas: CTkCanvas

        self.mainPresenter: MainPresenter = mainPresenter
        self.root: CTk = root

    def Execute(self) -> None:
        self.root.title("Graphical Image Analysis Tool")
        
        self.CreateMainFrame()
        self.CreateMenuBar()
        
        self.menuFrame.pack(fill="x")
        self.workspaceCanvas.pack(fill="both", expand=True)

        self.root.after(100, lambda: self.root.state("zoomed"))
        self.root.bind("<Button-1>", self.OnGlobalClick)
   
    # def Resize(self):

    def CreateMenuBar(self) -> None:
        self.menu = MenuBarView(self.root)
        self.menuFrame = self.menu.CreateMenuBar()

    def CreateMainFrame(self) -> None:
        workspace = WorkspaceView(self.root, self.mainPresenter)
        self.workspaceCanvas = workspace.CreateWorkspace() 
        # self.mainPresenter.workspace = 

    def OnGlobalClick(self, event: Tk.Event) -> None:
        widget: CTkFrame = cast(CTkFrame, event.widget)
        self.menu.OnGlobalClick(widget)