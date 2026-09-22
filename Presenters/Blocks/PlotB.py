#Presenters/Blocks/ConstantB
from Presenters.Blocks.Block import Presenter as BlockPresenter
from Utilities.BlockRequestor import InNodeRequest, OutNodeRequest

class Presenter(BlockPresenter):
    def __init__(self) -> None:
        self.title = "Plot"
        self.inStruct = [
            InNodeRequest("", "label")
        ]
        self.outStruct = []
        
        super().__init__()
        self.normalWidth = 240.0
        self.normalHeight = 240.0
        self.Update()

    def Update(self):
        self.outVals = self.inVals
        super().Update()