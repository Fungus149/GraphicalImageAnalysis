# Views/MenuBar.py

from customtkinter import *

from Utilities.CustomWidgets import CustomWidgets
from Utilities.WidgetsUtilities import WidgetsUtilities
from Views.ContextMenusView import View as contextView
from ViewModels.MainViewModel import ViewModel as mainViewModel

class View():
    def __init__(self, root: CTk, viewmodel: mainViewModel) -> None:
        self.menuFrame: CTkFrame
        self.fileBtn: CTkButton
        self.fileMenu: CTkFrame
        self.editBtn: CTkButton
        self.editMenu: CTkFrame
        self.addBtn: CTkButton
        self.addMenu: CTkFrame

        self.root: CTk = root
        self.mainViewmodel: mainViewModel = viewmodel
        self.contextMenus: contextView = contextView(viewmodel)

    def CreateMenuBar(self) -> CTkFrame:
        self.menuFrame = CTkFrame(self.root, fg_color="#4F4F4F")

        self.fileBtn = CustomWidgets.CreateMenuButton(self.menuFrame, "File", self.OnFileMenu)
        self.fileMenu = self.contextMenus.CreateFilesMenu(self.root)
        self.editBtn = CustomWidgets.CreateMenuButton(self.menuFrame, "Edit", self.OnEditMenu)
        self.editMenu = self.contextMenus.CreateEditMenu(self.root)
        self.addBtn = CustomWidgets.CreateMenuButton(self.menuFrame, "Add", self.OnAddMenu)
        self.addMenu = self.contextMenus.CreateAddMenu(self.root)
        
        self.fileBtn.pack(side="left")
        self.editBtn.pack(side="left")
        self.addBtn.pack(side="left")
    
        return self.menuFrame

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

    def OnGlobalClick(self, widget: CTkFrame) -> None:
        if not WidgetsUtilities.IsChildOf(widget, (self.editBtn, self.editMenu)):
            self.editMenu.place_forget()

        if not WidgetsUtilities.IsChildOf(widget, (self.fileBtn, self.fileMenu)):
            self.fileMenu.place_forget()
            
        if not WidgetsUtilities.IsChildOf(widget, (self.addBtn, self.addMenu)):
            self.addMenu.place_forget()
