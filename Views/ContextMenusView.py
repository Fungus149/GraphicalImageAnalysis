# Views/ContextMenusView.py
from typing import Callable

from customtkinter import *
from Utilities.CustomWidgets import CustomWidgets
from ViewModels.MainViewModel import ViewModel

class View():
    def __init__(self, viewmodel: ViewModel):
        self.viewmodel: ViewModel = viewmodel

    def CreateFilesMenu(self, parent: CTkFrame | CTk) -> CTkFrame:
        options: dict[str, Callable] = dict()
        options["New"] = self.OnNewFile
        options["Open"] = self.OnOpenFile
        options["Save [ctr+S]"] = self.OnSaveFile
        options["Import"] = self.OnImportFile
        options["Export"] = self.OnExportFile

        return CustomWidgets.CreateContextMenu(parent, options)

    def OnNewFile(self):
        print("New file created.")

    def OnOpenFile(self):
        print("Open file dialog.")

    def OnSaveFile(self):
        print("Save file dialog.")

    def OnImportFile(self):
        print("Import file.")

    def OnExportFile(self):
        print("Export file.")

    def CreateEditMenu(self, parent: CTkFrame | CTk) -> CTkFrame:
        options: dict[str, Callable] = dict()
        options["Undo [ctr+C]"] = self.OnUndo
        options["Redo [ctr+V]"] = self.OnRedo
        options["Cut [ctr+X]"] = self.OnCut
        options["Copy [ctr+C]"] = self.OnCopy
        options["Paste [ctr+V]"] = self.OnPaste
        options["Duplicate [ctr+D]"] = self.OnDuplicate

        return CustomWidgets.CreateContextMenu(parent, options)

    def OnUndo(self):
        print("Undo action.")

    def OnRedo(self):
        print("Redo action.")

    def OnCut(self):
        print("Cut action.")

    def OnCopy(self):
        print("Copy action.")

    def OnPaste(self):
        print("Paste action.")

    def OnDuplicate(self):
        print("Duplicate action.")

    def CreateAddMenu(self, parent: CTkFrame | CTk) -> CTkFrame:
        options: dict[str, Callable] = dict()
        options["Input blocks"] = self.OnInputBlocks
        options["Conversions blocks"] = self.OnConversionsBlocks
        options["Output blocks"] = self.OnOutputBlocks

        return CustomWidgets.CreateContextMenu(parent, options)

    def OnInputBlocks(self):
        print("Input blocks menu")

    def OnConversionsBlocks(self):
        print("Conversions blocks menu")

    def OnOutputBlocks(self):
        print("Output blocks menu")