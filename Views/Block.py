# Views/BlockView.py
from customtkinter import *
import tkinter as Tk
from typing import Literal

from Interfaces.IClickable import IClickable
from Views.InNode import View as InNodeView
from Views.OutNode import View as OutNodeView
from Views.CanvasEntry import CanvasEntry
from Views.CanvasDropdown import CanvasDropdown
from Presenters.MainPresenter import Presenter as MainPresenter
from Presenters.Blocks.Block import Presenter
from Utilities.BlockRequestor import InNodeRequest, OutNodeRequest

type AnchorType = Literal[
    "n", "ne", "e", "se",
    "s", "sw", "w", "nw",
    "center"
]

class View(IClickable):
    def __init__(self, presenter: Presenter, mainPresenter: MainPresenter, blockId: int) -> None:
        super().__init__()
        self.label: int
        self.lastX: int
        self.lastY: int

        self.nodesIn: list[InNodeView] = []
        self.nodesOut: list[OutNodeView] = []
        self.entries: dict[int, CanvasEntry] = {}
        self.dropdowns: list = []
        self.headers: list[int] = []
        self.errorBox: CTkToplevel | None = None

        self.mainPresenter: MainPresenter = mainPresenter
        self.presenter: Presenter = presenter
        self.workspace: CTkCanvas = mainPresenter.workspace
        self.diagramTag: str = mainPresenter.diagramTag
        self.blockTag: str = f'block_{blockId}'
        self.normalWidth: float = presenter.normalWidth
        self.normalHeight: float = presenter.normalHeight
        self.blockId: int = blockId

        self.presenter.raiseError = self.RaiseError

    def Instantiate(self, posX: int, posY: int) -> None:
        self.presenter.ChangePosition(posX,posY)
        self.presenter.UpdateWorldPos()
        self.bg: int = self.workspace.create_rectangle(
            posX-self.normalWidth/2, 
            posY-self.normalHeight/2, 
            posX+self.normalWidth/2, 
            posY+self.normalHeight/2,
            fill = "#1F1F1F",
            outline = "#4F4F4F",
            tags=(self.blockTag, self.diagramTag)
        )
        self.MakeLabel(round(posX-self.normalWidth/2),posY)
        self.MakeBody()

        self.workspace.tag_bind(self.bg,"<Button-1>", self.OnClick)
        self.workspace.tag_bind(self.bg,"<B1-Motion>", self.OnDrag)

        self.presenter.Update()
    
    def MakeBody(self):
        i: int = 0

        inStruct: list[InNodeRequest] = self.presenter.inStruct
        outStruct: list[OutNodeRequest] = self.presenter.outStruct
        posX: float = self.presenter.absPosX
        posY: float = self.presenter.absPosY

        leftEdge: int = round(posX-self.normalWidth/2)
        rightEdge: int = round(posX+self.normalWidth/2)
        for request in inStruct:
            currentHeight: int = round(posY-self.normalHeight/2 + (i+1) * self.normalHeight/(len(inStruct)+1))
            
            if request.isVisible:
                node = InNodeView(self, i, self.mainPresenter)
                node.Instantiate(leftEdge, currentHeight)

                self.nodesIn.append(node)
            match request.type:
                case "label":
                    self.MakeNodeHeader(request.label, leftEdge, currentHeight,"w")
                case "entry":
                    if request.entryType:
                        self.MakeNodeEntry(request.label, request.entryType, leftEdge, currentHeight,i)
                    else:
                        print(f"WARNING--- entry \"{request.label}\" on block \"{self.presenter.title}\" did not generate since entryType was not provided ---WARNING")

            i+=1

        i = 0
        for request in outStruct:
            node = OutNodeView(self, i, self.mainPresenter)
            currentHeight: int = round(posY-self.normalHeight/2 + (i+1) * self.normalHeight/(len(outStruct)+1))
            node.Instantiate(rightEdge, currentHeight)

            self.nodesOut.append(node)
            self.MakeNodeHeader(request.label, rightEdge, currentHeight,"e")
            i+=1

    def MakeLabel(self, posX: int, posY: int) -> None:
        self.label = self.workspace.create_text(
            posX,
            posY - self.normalHeight/2 + 8,
            text = self.presenter.title,
            anchor="w",
            font = ("Arial", 14, "bold"),
            fill = "#B6B6B6",
            tags = (self.blockTag, self.diagramTag)
        )
        self.workspace.tag_bind(self.label,"<Button-1>", self.OnClick)

    def MakeNodeHeader(self, label: str, posX: int, posY: int, side: AnchorType) -> None:
        offset: int

        if side == "w":
            offset = 14
        else:
            offset = -14

        self.headers.append(
            self.workspace.create_text(
                posX + offset,
                posY,
                text = label,
                anchor = side,
                font = ("Arial", 10),
                fill = "#B6B6B6",
                tags = (self.blockTag, self.diagramTag)
            )
        )

    def MakeNodeEntry(self, label: str, type: Literal["str", "float", "int"], posX: int, posY: int, id) -> None:
        self.entries[id] = CanvasEntry(
            self.blockTag,
            label,
            type,
            posX,
            posY,
            lambda value: self.presenter.SetInVal(id, value),
            self.mainPresenter
        )

    def MakeNodeDropdown(self, options: list[str], posX: int, posY: int, id) -> None:
        self.dropdown = CanvasDropdown(
            self.blockTag,
            options,
            posX,
            posY,
            self.presenter.SetOperation,
            self.mainPresenter
        )   

    def OnClick(self, event: Tk.Event) -> None:
        selectedItems: list[IClickable] = self.mainPresenter.selected
        self.lastX = event.x
        self.lastY = event.y

        if len(selectedItems) == 1:
            if self in selectedItems:
                self.OnDeselected()
                return

            selectedItems[0].OnDeselected()
            self.OnSelected()
        else:
            if not self.isDown:
                for item in selectedItems.copy():
                    item.OnDeselected()
                self.OnSelected()
        
    def OnSelected(self) -> None:
        self.workspace.itemconfig(self.bg, fill="#4F4F4F")

        self.mainPresenter.selected.append(self)
        self.isDown = True
    
    def OnDeselected(self) -> None:
        self.workspace.itemconfig(self.bg, fill="#1F1F1F")
        
        self.mainPresenter.selected.remove(self)
        self.isDown = False

    def OnDrag(self, event: Tk.Event) -> None:
        dx: float
        dy: float

        selectedItems: list[IClickable] = self.mainPresenter.selected
        scale: float = self.mainPresenter.scale

        if int(event.state) & 0x0004:
            absX: float = (event.x - self.mainPresenter.offsetX) / scale
            absY: float = (event.y - self.mainPresenter.offsetY) / scale
            dx = round(absX / self.normalWidth) * self.normalWidth - self.presenter.absPosX
            dy = round(absY / self.normalHeight) * self.normalHeight - self.presenter.absPosY
        else:
            dx = (event.x - self.lastX) / scale
            dy = (event.y - self.lastY) / scale

        if len(selectedItems) == 0:
            self.OnSelected()
            
        for item in selectedItems:
            if isinstance(item, View):
                item.presenter.ChangePosition(dx, dy)
                item.UpdatePosition()
                item.UpdateConnectionsPositions()

        self.lastX = event.x
        self.lastY = event.y

    def OnZoom(self) -> None:
        self.workspace.itemconfigure(
            self.label, 
            font=("Arial", round(self.mainPresenter.labelFont), "bold")
        )
        for header in self.headers:
           self.workspace.itemconfigure(
                header, 
                font=("Arial", round(self.mainPresenter.headerFont))
            ) 
        for entry in self.entries.values():
            entry.OnZoom()

    def UpdateConnectionsPositions(self) -> None:
        for node in self.nodesOut:
            for connection in node.connections:
                connection.UpdatePosition()

        for node in self.nodesIn:
            if node.connection:
                node.connection.UpdatePosition()

    def UpdatePosition(self) -> None:
        scale: float = self.mainPresenter.scale
        dx: float = (self.presenter.absPosX - self.presenter.worldPosX) * scale
        dy: float = (self.presenter.absPosY - self.presenter.worldPosY) * scale 

        self.workspace.move(
            self.blockTag, 
            dx, 
            dy
        )
        self.presenter.UpdateWorldPos()

    def HideEntry(self, id):
        if id in self.entries.keys():
            self.entries[id].Disable()

    def ShowEntry(self, id):
        if id in self.entries.keys():
            self.entries[id].Enable()

    def Delete(self) -> None:
        for node in self.nodesIn:
            if node.connection is not None:
                node.connection.Delete()
        for node in self.nodesOut:
            for connection in node.connections.copy():
                connection.Delete()

        self.workspace.delete(self.blockTag)

    def RaiseError(self, errorMsg: str) -> None:
        if self.errorBox is not None:
            self.errorBox.destroy()

        x0, y0, xf, yf = self.workspace.coords(self.bg)

        self.errorBox = CTkToplevel(self.workspace)
        errorLabel: CTkLabel = CTkLabel(self.errorBox, text=errorMsg)

        self.errorBox.bind("<FocusOut>", self.OnErrorFocusOut)
        self.errorBox.update_idletasks()

        midX: float = (x0 + xf) / 2
        midY: float = (y0 + yf) / 2
        width: int = self.errorBox.winfo_width()
        height: int = self.errorBox.winfo_height()
        screenX: int = int(self.workspace.winfo_rootx() + midX - width / 2)
        screenY: int = int(self.workspace.winfo_rooty() + midY - height / 2)

        errorLabel.pack(padx=10, pady=10)
        self.errorBox.geometry(f"{width}x{height}+{screenX}+{screenY}")

    def OnErrorFocusOut(self, event: Tk.Event) -> None:
        if self.errorBox is not None:
            self.errorBox.destroy()
            self.errorBox = None