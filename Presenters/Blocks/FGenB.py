#Presenters/Blocks/ConstantB
from Presenters.Blocks.Block import Presenter as BlockPresenter
from Utilities.BlockRequestor import InNodeRequest, OutNodeRequest
from UseCases.Math import SampleFunction

class Presenter(BlockPresenter):
    def __init__(self) -> None:
        self.title = "Function Generator"

        self.inStruct = [
            InNodeRequest("Formula", "entry", "str", False),
            InNodeRequest("Samples", "entry", "int"),
            InNodeRequest("Lower x", "entry", "float"),
            InNodeRequest("Upper x", "entry", "float"),
        ]
        self.outStruct = [
            OutNodeRequest()
        ]
        super().__init__()

    def Update(self) -> None:
        formula: str = self.inVals[0][0][0]
        samples: int = self.inVals[1][0][0]
        minimum: float = self.inVals[2][0][0]
        maximum: float = self.inVals[3][0][0]

        self.outVals[0] = SampleFunction(
            formula,
            samples,
            minimum,
            maximum,
            self.raiseError
        )
        super().Update()