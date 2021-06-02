from typing import List, Any
from lsp_types import EACFunctionType
from error import EACNotDefineError
from numpy import ones, vstack
from numpy.linalg import lstsq

class EAC:
    def __init__(self, funcType: str = EACFunctionType.LINEAR, funcs: List[Any] = [], breakValues: List[float] = []) -> "EAC":
        self.funcType = funcType
        self.funcs = funcs
        self.breakValues = breakValues
    def define(self, breakValues: List[float]):
        for i in range(1, len(breakValues)):
            points = [breakValues[i - 1], breakValues[i]]
            x_coords, y_coords = zip(*points)
            A = vstack([x_coords,ones(len(x_coords))]).T
            m, c = lstsq(A, y_coords, rcond=None)[0]
            self.funcs.append((m, c))
        self.breakValues = breakValues
    def solve(self, value: float) -> float:
        if len(self.funcs) == 0 or len(self.breakValues) == 0:
            raise EACNotDefineError()
        if value <= self.breakValues[0][0]:
            return self.breakValues[0][1]
        elif value >= self.breakValues[-1][0]:
            return self.breakValues[-1][1]
        else:
            index = self._binarySearch(value)
            return self.funcs[index][0] * value + self.funcs[index][1]
    def _binarySearch(self, target: float) -> int:
        l, r = 0, len(self.breakValues) - 1
        while l < r:
            mid = (l + r) >> 1
            if self.breakValues[mid][0] < target:
                l = mid + 1
            else:
                r = mid
        return l - 1 if l != 0 else 0