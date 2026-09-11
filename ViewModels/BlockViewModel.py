class ViewModel():

    inVals: tuple
    outVals: tuple

    def __init__(self, posX: float, posY: float) -> None:
        self.absPosX = posX
        self.absPosY = posY

        self.worldPosX = posX
        self.worldPosY = posY
