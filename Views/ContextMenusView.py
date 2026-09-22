# Views/ContextMenusView.py
from typing import Callable

from customtkinter import *
from Utilities.CustomWidgets import CustomWidgets
class View():
    def __init__(self) -> None:
        pass

    def CreateFilesMenu(self, parent: CTkFrame | CTk) -> CTkFrame:
        options: dict[str, Callable] = dict()
        options["New"] = self.OnNewFile
        options["Open"] = self.OnOpenFile
        options["Save [ctr+S]"] = self.OnSaveFile
        options["Import"] = self.OnImportFile
        options["Export"] = self.OnExportFile

        return CustomWidgets.CreateContextMenu(parent, options)

    def OnNewFile(self) -> None:
        print("New file created.")

    def OnOpenFile(self) -> None:
        print("Open file dialog.")

    def OnSaveFile(self) -> None:
        print("Save file dialog.")

    def OnImportFile(self) -> None:
        print("Import file.")

    def OnExportFile(self) -> None:
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

    def OnUndo(self) -> None:
        print("Undo action.")

    def OnRedo(self) -> None:
        print("Redo action.")

    def OnCut(self) -> None:
        print("Cut action.")

    def OnCopy(self) -> None:
        print("Copy action.")

    def OnPaste(self) -> None:
        print("Paste action.")

    def OnDuplicate(self) -> None:
        print("Duplicate action.")

    def CreateAddMenu(self, parent: CTkFrame | CTk) -> CTkFrame:
        options: dict[str, Callable] = dict()
        options["Input blocks"] = self.OnInputBlocks
        options["Conversions blocks"] = self.OnConversionsBlocks
        options["Output blocks"] = self.OnOutputBlocks

        return CustomWidgets.CreateContextMenu(parent, options)

    def OnInputBlocks(self) -> None:
        print("Input blocks menu")

    def OnConversionsBlocks(self) -> None:
        print("Conversions blocks menu")

    def OnOutputBlocks(self) -> None:
        print("Output blocks menu")