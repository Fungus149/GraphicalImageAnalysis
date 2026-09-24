# Views/PlotBlockView.py
import math
import tkinter as Tk
from typing import Any

from Views.Block import View as BlockView
from Presenters.MainPresenter import Presenter as MainPresenter
from Presenters.Blocks.PlotB import Presenter

class PlotBlockView(BlockView):
    def __init__(self, presenter: Presenter, mainPresenter: MainPresenter, blockId: int) -> None:

        super().__init__(presenter, mainPresenter, blockId)
        self.plotLastX: float
        self.plotLastY: float

        self.plotItems: list[int] = []
        self.plotScale: float = 1.0
        self.plotOffsetX: float = 0.0
        self.plotOffsetY: float = 0.0
        self.plotWidth: float = 200.0
        self.plotHeight: float = 200.0
        self.dotRadius: float = 3.0

        self.plotPresenter: Presenter = presenter

        self.plotPresenter.viewUpdate = self.Update

    def Instantiate(self, posX: int, posY: int) -> None:
        self.plotTag: str = f'plot_{self.blockTag}'
        super().Instantiate(posX, posY)
        self.DrawPlotArea()

        self.Update()
        self.workspace.tag_bind(self.plotTag, "<Button-1>", self.OnPlotPanStart)
        self.workspace.tag_bind(self.plotTag, "<B1-Motion>", self.OnPlotPan)
        self.workspace.tag_bind(self.plotTag, "<Enter>", self.OnPlotEnter)
        self.workspace.tag_bind(self.plotTag, "<Leave>", self.OnPlotLeave)

    def DrawPlotArea(self):
        x0, y0, x1, y1 = self.workspace.coords(self.bg)

        centerX: float = (x0 + x1) / 2
        centerY: float = (y0 + y1) / 2
        left: float = centerX - self.plotWidth / 2
        right: float = centerX + self.plotWidth / 2
        top: float = centerY - self.plotHeight / 2
        bottom: float = centerY + self.plotHeight / 2
        self.plotArea: int = self.workspace.create_rectangle(
            left,
            top,
            right,
            bottom,
            fill="#202020",
            outline="#505050",
            tags=(self.blockTag, self.plotTag, self.diagramTag)
        )

    def Update(self) -> None:
        layers: int

        inputData: Any = self.presenter.inVals[0]
        entries: int = len(inputData)

        self.ClearPlot()
        if not isinstance(inputData, list) or len(inputData) == 0:
            return

        try:
            layers = len(inputData[0][0])
        except (TypeError, IndexError):
            return

        if layers > 4:
            self.RaiseError(
                f"{layers} layers of data were given.\n"
                "Maximally 4 can be displayed."
            )
            return

        if entries == 0:
            return

        self.CalculateInitialScale(inputData, entries, layers)
        self.DrawPlot(inputData, entries, layers)

    def CalculateInitialScale(self, inputData: list[Any], entries: int, layers: int) -> None:
        maxY: float = 0.0

        for i in range(entries):
            for layer in range(layers):
                print(f"{inputData = }")
                value: float = inputData[i][0][layer]

                if math.isfinite(value):
                    maxY = max(maxY, abs(value))

        if entries <= 1:
            xScale: float = self.plotWidth
        else:
            xScale = self.plotWidth / (entries - 1)

        if maxY == 0:
            yScale: float = self.plotHeight / 2
        else:
            yScale = (self.plotHeight / 2) / maxY

        self.plotScale = min(xScale, yScale)

        if self.plotScale < 1:
            self.plotScale = 1

    def DrawPlot(self, inputData: list[Any], entries: int, layers: int) -> None:
        x0, y0, x1, y1 = self.workspace.coords(self.bg)

        centerX: float = (x0 + x1) / 2
        centerY: float = (y0 + y1) / 2
        left: float = centerX - self.plotWidth * self.mainPresenter.scale / 2
        right: float = centerX + self.plotWidth * self.mainPresenter.scale / 2
        top: float = centerY - self.plotHeight * self.mainPresenter.scale / 2
        bottom: float = centerY + self.plotHeight * self.mainPresenter.scale / 2
        originX: float = left + self.plotOffsetX
        originY: float = centerY + self.plotOffsetY
        colors: tuple[str, str, str, str] = (
            "red",
            "green",
            "blue",
            "black"
        )
        self.DrawAxes(left, top, right, bottom, originX, originY)

        for layer in range(layers):
            for i in range(entries):
                value: float = inputData[i][0][layer]
                x: float = originX + i * self.plotScale

                if not math.isfinite(value):
                    self.DrawAsymptote(
                        x,
                        top,
                        bottom,
                        left,
                        right,
                        colors[layer]
                    )
                    continue

                y: float = originY - value * self.plotScale
                if x < left or x > right or y < top or y > bottom:
                    continue

                dot: int = self.workspace.create_oval(
                    x - self.dotRadius,
                    y - self.dotRadius,
                    x + self.dotRadius,
                    y + self.dotRadius,
                    fill=colors[layer],
                    outline="",
                    tags=(self.blockTag, self.plotTag, self.diagramTag)
                )
                self.plotItems.append(dot)

    def DrawAxes(self, left: float, top: float, right: float, bottom: float, originX: float, originY: float) -> None:
        if top <= originY <= bottom:
            axis: int = self.workspace.create_line(
                left,
                originY,
                right,
                originY,
                tags=(self.blockTag, self.plotTag, self.diagramTag)
            )
            self.plotItems.append(axis)

        if left <= originX <= right:
            axis = self.workspace.create_line(
                originX,
                top,
                originX,
                bottom,
                tags=(self.blockTag, self.plotTag, self.diagramTag)
            )
            self.plotItems.append(axis)

    def DrawAsymptote(self, x: float, top: float, bottom: float, left: float, right: float, color: str) -> None:
        if x < left or x > right:
            return

        line: int = self.workspace.create_line(
            x,
            top,
            x,
            bottom,
            fill=color,
            dash=(4, 4),
            tags=(self.blockTag, self.plotTag, self.diagramTag)
        )
        self.plotItems.append(line)

    def ClearPlot(self) -> None:
        for item in self.plotItems:
            self.workspace.delete(item)

        self.plotItems.clear()

    def OnPlotZoom(self, event: Tk.Event) -> str:
        direction: int = 1 if event.delta > 0 else -1

        zoom: float = 1.1 if direction > 0 else 1 / 1.1
        if int(event.state) & 0x0001:
            zoom = 1.02 if direction > 0 else 1 / 1.02

        self.plotScale *= zoom
        if self.plotScale < 0.001:
            self.plotScale = 0.001

        self.RedrawPlot()
        return "cumcumcuumcum"

    def RedrawPlot(self) -> None:
        inputData: Any = self.presenter.inVals[0]

        self.ClearPlot()
        if not isinstance(inputData, list) or len(inputData) == 0:
            return

        layers: int = len(inputData[0][0])
        self.DrawPlot(inputData, len(inputData), layers)

    def OnPlotPanStart(self, event: Tk.Event) -> None:
        self.plotLastX = event.x
        self.plotLastY = event.y

    def OnPlotPan(self, event: Tk.Event) -> None:
        dx: float = event.x - self.plotLastX
        dy: float = event.y - self.plotLastY

        self.plotOffsetX += dx
        self.plotOffsetY += dy
        self.plotLastX = event.x
        self.plotLastY = event.y

        self.RedrawPlot()

    def OnPlotEnter(self, event: Tk.Event) -> None:
        self.mainPresenter.scrollHandler = self.OnPlotZoom

    def OnPlotLeave(self, event: Tk.Event) -> None:
        self.mainPresenter.scrollHandler = None