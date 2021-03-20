# BettyCrocker.com scraper
# Written by G.D. Wallters
# Freely released the code to recipe_scraper group
# 18 January, 2020
# =======================================================

from typing import List, Optional

from ._abstract import AbstractScraper
from ._utils import normalize_string


class BettyCrocker(AbstractScraper):
    @classmethod
    def host(cls):
        return "bettycrocker.com"

    def title(self) -> Optional[str]:
        return self.schema.title()

    def total_time(self) -> Optional[int]:
        return self.schema.total_time()

    def yields(self) -> Optional[str]:
        return self.schema.yields()

    def image(self) -> Optional[str]:
        return self.schema.image()

    def ingredients(self) -> Optional[List[str]]:
        ingredients = self.soup.find(
            "div", {"class": "recipePartIngredientGroup"}
        ).ul.findAll("li")

        return [
            normalize_string(
                ingredient.find("div", {"class": "quantity"}).text
                + " "
                + ingredient.find("div", {"class": "description"}).span.text
            )
            for ingredient in ingredients
        ]

    def instructions(self) -> Optional[str]:
        instructions = self.soup.findAll("li", {"class": "recipePartStep"})
        return "\n".join(
            [
                normalize_string(
                    instruction.find(
                        "div", {"class": "recipePartStepDescription"}
                    ).get_text()
                )
                for instruction in instructions
            ]
        )

    def ratings(self) -> Optional[float]:
        r = self.soup.find("span", {"class": "ratingCount"}).get_text()
        if "\xa0Ratings" in r:
            r = r.replace("\xa0Ratings", "")
        return int(r)
