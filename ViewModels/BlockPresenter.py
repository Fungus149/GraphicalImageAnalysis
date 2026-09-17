class Presenter():

    inVals: tuple
    outVals: tuple

    def __init__(self, posX: float, posY: float) -> None:
        self.absPosX = posX
        self.absPosY = posY

        self.worldPosX = posX
        self.worldPosY = posY

    def ChangePosition(self, dx: float, dy: float):
        self.absPosX += dx
        self.absPosY += dy
