# Study on the Nutri-Score
# Brice MAYAG & Simon OCLOO - 2022
# University Paris Dauphine PSL

from json import load
from typing import Any, Dict, List

from pymongo import MongoClient

from ..constant import EN, FI, FR, GRADE, PR, SA, SCORE, SO, SU

 
class Product:

    def __init__(
        self,
        _id: int,
        category: str,
        name: str,
        nutri_score: Dict[str, Any],
        nutritional_information: Dict[str, Any],
        quantity: int,
        url: str,
    ) -> None:
        self._id = _id
        self._category = category
        self._name = name
        self._nutri_score = nutri_score
        self._nutritional_information = nutritional_information
        self._quantity = quantity
        self._url = url

    def __getitem__(self, key: str) -> float:
        return self._nutritional_information[key]

    def __repr__(self) -> str:
        return "\n".join([
            f"{self._name} - {self._quantity} ({self._category})",
            f"ID  : {self._id}",
            f"URL : {self._url}",
            "",
            "Nutritional information :",
            f"\t• Energy              = {self[EN]:6} kJ",
            f"\t• Fibers              = {self[FI]:6} g",
            f"\t• Fruits / Vegetables = {self[FR]:6} %",
            f"\t• Proteins            = {self[PR]:6} g",
            f"\t• Saturated fat       = {self[SA]:6} g",
            f"\t• Sodium              = {self[SO]:6} mg",
            f"\t• Sugar               = {self[SU]:6} g",
            "",
            f"Nutri-Score : {self._nutri_score[SCORE]} ({self._nutri_score[GRADE]})",
            "===========================================================================================================",
        ])

    @property
    def grade(self):
        return self._nutri_score[GRADE]

    @staticmethod
    def load_from_database(size: int) -> List["Product"]:
        db = MongoClient(host="localhost", port=27017).off
        pipeline = [
            {
                "$sample": {"size": size * 5},
            },
            {
                "$match": {
                    "id": {"$exists": True},
                    "nutriscore_data": {"$exists": True},
                    "nutriscore_data.is_beverage": {"$eq": 0},
                    "product_name": {"$exists": True},
                    "serving_quantity": {"$exists": True}
                }
            },
            {
                "$limit": size
            }
        ]
        products = []

        for raw_product in db.products.aggregate(pipeline):
            products.append(Product(
                raw_product["id"],
                raw_product["categories"],
                raw_product["product_name"],
                {
                    GRADE: raw_product["nutriscore_data"]["grade"].upper(),
                    SCORE: raw_product["nutriscore_data"]["score"],
                },
                {
                    EN: raw_product["nutriscore_data"][EN],
                    FI: raw_product["nutriscore_data"][FI],
                    FR: raw_product["nutriscore_data"][FR],
                    PR: raw_product["nutriscore_data"][PR],
                    SA: raw_product["nutriscore_data"][SA],
                    SO: raw_product["nutriscore_data"][SO],
                    SU: raw_product["nutriscore_data"][SU],
                },
                f"{raw_product['serving_quantity']} g",
                f"https://fr.openfoodfacts.org/produit/{raw_product['id']}"
            ))
        return products

    @staticmethod
    def load_from_json(filepath: str) -> List["Product"]:
        products = []

        with open(filepath, "r") as file:
            for data in load(file):
                products.append(Product(
                    data["ID"],
                    data["Category"],
                    data["Name"],
                    {
                        GRADE: data["Nutri-Score"][GRADE],
                        SCORE: data["Nutri-Score"][SCORE]
                    },
                    {
                        EN: data["Nutritional information"][EN],
                        FI: data["Nutritional information"][FI],
                        FR: data["Nutritional information"][FR],
                        PR: data["Nutritional information"][PR],
                        SA: data["Nutritional information"][SA],
                        SO: data["Nutritional information"][SO],
                        SU: data["Nutritional information"][SU]
                    },
                    data["Quantity"],
                    data["URL"],
                ))
        return products

    @property
    def name(self):
        return self._name

    @property
    def score(self):
        return self._nutri_score[SCORE]
