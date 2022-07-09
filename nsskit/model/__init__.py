# Study on the Nutri-Score
# Brice MAYAG & Simon OCLOO - 2022
# University Paris Dauphine PSL

from .abstract_model import AbstractModel
from .nutriscore_model import NutriScoreModel
from .two_additive_choquet_integral_model import TwoAdditiveChoquetIntegralModel
from .weighted_sum_model import WeightedSumModel


__all__ = (
    "AbstractModel",
    "NutriScoreModel",
    "TwoAdditiveChoquetIntegralModel",
    "WeightedSumModel",
)
