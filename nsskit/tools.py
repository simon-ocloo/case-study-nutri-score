from itertools import chain, combinations
from typing import Any, List


def subsets(initial_set: List[Any]):
    return chain.from_iterable(combinations(initial_set, r) for r in range(len(initial_set) + 1))
