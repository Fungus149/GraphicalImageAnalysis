# Presenters/Blocks/Block.py
from abc import ABC
from typing import Callable, Any

from Utilities.BlockRequestor import InNodeRequest,OutNodeRequest

class Presenter(ABC):
    def __init__(self) -> None:
        self.inStruct: list[InNodeRequest]
        self.outStruct: list[OutNodeRequest]
        self.raiseError: Callable[[str], None]
        self.title: str

        self.options: list[str] | None = None
        self.absPosX: float = 0
        self.absPosY: float = 0
        self.worldPosX: float = 0
        self.worldPosY: float = 0
        self.normalWidth: float = 240.0
        self.normalHeight: float = 160.0

        self.outputs: list[list[tuple[Presenter,int]]] = [[] for _ in self.outStruct]
        self.inVals: list[Any] = [[[0.0]] for _ in self.inStruct]
        self.outVals: list[Any] = [[[0.0]] for _ in self.outStruct]

    def Update(self):
        for targets, outVal in zip(self.outputs,self.outVals):
            for target, id in targets:
                target.inVals[id] = outVal
                target.Update()

    def ChangePosition(self, dx: float, dy: float):
        self.absPosX += dx
        self.absPosY += dy

    def UpdateWorldPos(self):
        self.worldPosX = self.absPosX
        self.worldPosY = self.absPosY

    def SetInVal(self, id: int, value: list[list[float | int | str]]) -> None:
        self.inVals[id] = value
        self.Update()

    def SetOperation(self, value: str) -> None:
        self.operation = value