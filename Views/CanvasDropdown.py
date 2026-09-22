# Views/CanvasDropdown.py
from collections.abc import Callable
from customtkinter import *

from Presenters.MainPresenter import Presenter as MainPresenter

class CanvasDropdown:
    def __init__(
        self,
        blockTag: str,
        values: list[str],
        posX: float,
        posY: float,
        onChange: Callable[[str], None],
        mainPresenter: MainPresenter
    ) -> None:
        self.itemWidth: int = 106
        self.itemHeight: int = 24

        self.values: list[str] = values
        self.mainPresenter: MainPresenter = mainPresenter
        self.workspace: CTkCanvas = mainPresenter.workspace
        self.onChange: Callable[[str], None] = onChange
        self.diagramTag: str = mainPresenter.diagramTag
        self.blockTag: str = blockTag

        self.dropdown: CTkOptionMenu = CTkOptionMenu(
            self.workspace,
            values=self.values,
            width=self.itemWidth,
            height=self.itemHeight,
            command=self.OnChange
        )
        # self.dropdown.set(self.value)
        self.window: int = self.workspace.create_window(
            posX + 14,
            posY,
            window=self.dropdown,
            anchor="w",
            tags=(blockTag, self.diagramTag)
        )

    def OnChange(self, value: str) -> None:
        self.onChange(value)

    def OnZoom(self) -> None:
        scale: float = self.mainPresenter.scale

        self.dropdown.configure(
            width=int(self.itemWidth * scale),
            height=int(self.itemHeight * scale)
        )

    def Delete(self) -> None:
        self.workspace.delete(self.window)
        self.dropdown.destroy()