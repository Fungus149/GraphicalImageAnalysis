# Utilities/CustomWidgets.py
from typing import Callable

from customtkinter import *

class CustomWidgets():
    @staticmethod    
    def CreateMenuButton(parent: CTkFrame | CTk, btnLabel: str, btnCmd: Callable | None = None) -> CTkButton:
        button = CTkButton(
            parent,
            text=btnLabel, 
            command=btnCmd,
            fg_color="transparent", 
            hover_color="gray", 
            corner_radius=0
        )
        return button

    @staticmethod
    def CreateContextMenu(parent: CTkFrame | CTk, options: dict[str, Callable]) -> CTkFrame:
        contextFrame = CTkFrame(
            parent
        )
        for optionLabel, optionCmd in options.items():
            button = CustomWidgets.CreateMenuButton(contextFrame, optionLabel, optionCmd)
            button.pack(fill="x")

        return contextFrame