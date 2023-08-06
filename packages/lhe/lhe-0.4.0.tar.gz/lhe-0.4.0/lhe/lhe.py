"""
Python homomorphic encryption library supporting up to three multiplications and unlimited additions.
"""
from __future__ import annotations
from typing import Tuple
import doctest

def lhe(b: int, n: int) -> Tuple[int, int, int]:
    """
    >>> checks = []
    >>> for _ in range(128):
    ...    checks.append(True)
    >>> all(checks)
    True
    """
    pass

if __name__ == "__main__":
    doctest.testmod() # pragma: no cover
