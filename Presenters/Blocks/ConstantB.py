#Presenters/Blocks/ConstantB
from Presenters.Blocks.Block import Presenter as BlockPresenter
from Utilities.BlockRequestor import InNodeRequest, OutNodeRequest

class Presenter(BlockPresenter):
    def __init__(self) -> None:
        self.title = "Constant"

        self.inStruct = [
            InNodeRequest("constant", "entry", "float")
        ]
        self.outStruct = [
            OutNodeRequest("")
        ]
        super().__init__()

        self.Update()

    def Update(self):
        self.outVals = self.inVals
        super().Update()