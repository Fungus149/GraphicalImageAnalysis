# Views/MainView.py*
from customtkinter import *

from Utilities.CustomWidgets import CustomWidgets
from Utilities.WidgetsUtilities import WidgetsUtilities

from Views.ContextMenusView import View as contextView
from Views.BlockView import View as blocksView
from ViewModels.MainViewModel import ViewModel

class View():
    def __init__(self, viewmodel: ViewModel, contextMenus: contextView, root: CTk):
        self.viewmodel: ViewModel = viewmodel
        self.contextMenus: contextView = contextMenus
        self.root: CTk = root
        self.root.bind("<Button-1>", self.OnGlobalClick)

    def Execute(self):
        self.root.title("Graphical Image Analysis Tool")
        
        self.CreateMainFrame()
        self.CreateMenuBar()
        # self.CreateBlocksMenu()
        
        self.menuFrame.pack(fill="x")
        self.workspace.pack(fill="both", expand=True)

        self.root.after(100, lambda: self.root.state("zoomed"))

        block = blocksView(self.workspace)
        block.Create(100,100)
   
    # def Resize(self):

    def CreateMenuBar(self):
        self.menuFrame: CTkFrame = CTkFrame(self.root)

        self.fileBtn: CTkButton = CustomWidgets.CreateMenuButton(self.menuFrame, "File", self.OnFileMenu)
        self.fileMenu: CTkFrame = self.contextMenus.CreateFilesMenu(self.root)
        self.editBtn: CTkButton = CustomWidgets.CreateMenuButton(self.menuFrame, "Edit", self.OnEditMenu)
        self.editMenu: CTkFrame = self.contextMenus.CreateEditMenu(self.root)
        self.addBtn: CTkButton = CustomWidgets.CreateMenuButton(self.menuFrame, "Add", self.OnAddMenu)
        self.addMenu: CTkFrame = self.contextMenus.CreateAddMenu(self.root)
        
        self.fileBtn.pack(side="left")
        self.editBtn.pack(side="left")
        self.addBtn.pack(side="left")

    def OnFileMenu(self):
        if self.fileMenu.winfo_ismapped():
            self.fileMenu.place_forget()
            return
        self.fileMenu.place(
            x=self.fileBtn.winfo_x(), 
            y=self.fileBtn.winfo_y() + self.fileBtn.winfo_height()
        )
        
    def OnEditMenu(self):
        if self.editMenu.winfo_ismapped():
            self.editMenu.place_forget()
            return
        self.editMenu.place(
            x=self.editBtn.winfo_x(), 
            y=self.editBtn.winfo_y() + self.editBtn.winfo_height()
        )

    def OnAddMenu(self):
        if self.addMenu.winfo_ismapped():
            self.addMenu.place_forget()
            return
        self.addMenu.place(
            x=self.addBtn.winfo_x(), 
            y=self.addBtn.winfo_y() + self.addBtn.winfo_height()
        )

    def CreateMainFrame(self):
        self.workspace: CTkCanvas = CTkCanvas(
            self.root,
            bg="#0F0F0F",
            bd = 0,
            highlightthickness = 0
        )

    # def CreateBlocksMenu(self):
    #     inputBlocksBtn: CTkButton = CTkButton

    def OnGlobalClick(self, event):
        widget: CTkFrame = event.widget

        if not WidgetsUtilities.IsChildOf(widget, (self.editBtn, self.editMenu)):
            self.editMenu.place_forget()
        
        if not WidgetsUtilities.IsChildOf(widget, (self.fileBtn, self.fileMenu)):
            self.fileMenu.place_forget()

        if not WidgetsUtilities.IsChildOf(widget, (self.addBtn, self.addMenu)):
            self.addMenu.place_forget()

