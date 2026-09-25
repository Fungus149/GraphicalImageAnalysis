# Views/Tooltip.py
from customtkinter import *

class View:
    def __init__(self, parent) -> None:
        self.parent = parent
        self.tooltip: CTkToplevel | None = None
        self.tooltipAfter: str | None = None

    def Show(self, text: str, posX: int, posY: int, delay: int = 500) -> None:
        self.Hide()
        self.tooltipAfter = self.parent.after(delay,
            lambda: self.Create(text, posX, posY)
        )

    def Create(self, text: str, posX: int, posY: int) -> None:
        self.tooltip = CTkToplevel(self.parent)
        self.tooltipAfter = None

        self.tooltip.overrideredirect(True)
        mainLabel = CTkLabel(self.tooltip, text=text)
        self.tooltip.update_idletasks()
        self.tooltip.geometry(f"+{posX}+{posY}")

        mainLabel.pack(padx=5, pady=3)

    def Hide(self) -> None:
        if self.tooltipAfter is not None:
            self.parent.after_cancel(self.tooltipAfter)
            self.tooltipAfter = None

        if self.tooltip is not None:
            self.tooltip.destroy()
            self.tooltip = None