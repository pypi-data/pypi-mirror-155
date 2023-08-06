import cv2
import numpy
from utilspy_g4 import addExt


class PolyFiller:

    def __init__(self, ext = 'fill', color = 0):
        """
        :param ext: Added ext
        :param color: Fill color
        """

        self._ext = ext
        self._color = color
        self._polygons = []

    def addPolygon(self, polygon: list) -> None:
        """
        Add polygon to polygon list

        :param polygon: Added polygon
        :rtype: None
        :return: None
        """

        self._polygons.append(polygon)

    def fill(self, framePath: str) -> None:
        frame = cv2.imread(framePath)
        for row in self._polygons:
            polygon = numpy.array([row], dtype=numpy.int32)
            cv2.fillPoly(frame, polygon, self._color)
        cv2.imwrite(addExt(framePath, self._ext), frame)
