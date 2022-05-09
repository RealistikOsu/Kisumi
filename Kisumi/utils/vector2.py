from typing import Union
import math

VectorLike = Union["Vector2", int, float]

class Vector2:
    """A class representing a point on a 2D grid."""

    __slots__ = ("x", "y")
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"Vector2({self.x}, {self.y})"
    
    def __str__(self) -> str:
        return f"({self.x}, {self.y})"
    
    # Operator overloads.
    def __add__(self, o: VectorLike) -> "Vector2":
        x, y = _get_alterers(o)
        return Vector2(self.x + x, self.y + y)
    
    def __sub__(self, o: VectorLike) -> "Vector2":
        x, y = _get_alterers(o)
        return Vector2(self.x - x, self.y - y)
    
    def __mul__(self, o: VectorLike) -> "Vector2":
        x, y = _get_alterers(o)
        return Vector2(self.x * x, self.y * y)
    
    def __truediv__(self, o: VectorLike) -> "Vector2":
        x, y = _get_alterers(o)
        return Vector2(self.x / x, self.y / y)
    
    def __floordiv__(self, o: VectorLike) -> "Vector2":
        x, y = _get_alterers(o)
        return Vector2(self.x // x, self.y // y)
    
    def __mod__(self, o: VectorLike) -> "Vector2":
        x, y = _get_alterers(o)
        return Vector2(self.x % x, self.y % y)
    
    def __pow__(self, o: VectorLike) -> "Vector2":
        x, y = _get_alterers(o)
        return Vector2(self.x ** x, self.y ** y)
    
    def __neg__(self) -> "Vector2":
        return Vector2(-self.x, -self.y)
    
    def __pos__(self) -> "Vector2":
        return Vector2(+self.x, +self.y)
    
    # Comparison overloads.
    def __eq__(self, o: "Vector2") -> bool:
        return self.x == o.x and self.y == o.y
    
    def __ne__(self, o: "Vector2") -> bool:
        return self.x != o.x or self.y != o.y
    
    def __lt__(self, o: "Vector2") -> bool:
        return self.x < o.x or self.y < o.y
    
    def __le__(self, o: "Vector2") -> bool:
        return self.x <= o.x or self.y <= o.y
    
    def __gt__(self, o: "Vector2") -> bool:
        return self.x > o.x or self.y > o.y
    
    def __ge__(self, o: "Vector2") -> bool:
        return self.x >= o.x or self.y >= o.y
    
    # Comparison functions.
    def distance(self, vec: "Vector2") -> float:
        """Returns the distance between this vector and another."""

        vec_delta = self - vec
        return math.sqrt(vec_delta.x ** 2 + vec_delta.y ** 2)


def _get_alterers(o: Union[int, Vector2]) -> tuple[float, float]:
    """Returns the x, y values that should affect the vector."""

    if isinstance(o, Vector2):
        y = o.y
        x = o.x
    elif isinstance(o, (int, float)):
        y = x = float(o)
    else:
        raise TypeError("Vector2 operations only work with Vector2, "
                        "int and float")
    
    return x, y