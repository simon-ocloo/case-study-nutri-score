# Study on the Nutri-Score
# Brice MAYAG & Simon OCLOO - 2022
# University Paris Dauphine PSL

from abc import ABC, abstractstaticmethod
from typing import Any, Dict

from ..component import Product


class AbstractNormalizer(ABC):

    @abstractstaticmethod
    def run(product: Product, **kwargs: Dict[str, Any]) -> Dict[str, int]:
        pass
