# Study on the Nutri-Score
# Brice MAYAG & Simon OCLOO - 2022
# University Paris Dauphine PSL

from .abstract_model import AbstractModel
from ..component import Product
from ..constant import EN, FI, FR, PR, SA, SO, SU
from ..normalizer import AbstractNormalizer, NutriScoreNormalizer


class NutriScoreModel(AbstractModel):

    def __init__(self, normalizer: AbstractNormalizer = NutriScoreNormalizer) -> None:
        super().__init__(normalizer)

    def run(self, product: Product) -> float:
        data = self._normalizer.run(product)
        negative_points = (data[EN] + data[SA] + data[SO] + data[SU])
        positive_points = (data[FI] + data[FR])

        if not (negative_points >= 11 and data[FR] <= 2):
            positive_points += data[PR]
        else:
            print(f"[Special case for : {product.name}]")
        return (negative_points - positive_points)
