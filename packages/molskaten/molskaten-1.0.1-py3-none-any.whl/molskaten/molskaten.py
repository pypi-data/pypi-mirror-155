from datetime import datetime
from typing import List

import requests
import xmltodict


class Lunch:
    def __init__(self, food: str, date: datetime):
        self._food = food
        self._date = date

    def __repr__(self) -> str:
        return f"Lunch: {self.date} @ {self._food}"

    @property
    def food(self) -> str:
        return self._food

    @property
    def date(self) -> str:
        return datetime.strftime(self._date, "%Y-%m-%d")


class Molskaten:
    def __init__(self, school: str, baseUrl: str = "https://skolmaten.se"):
        self._endpoint = "{}/{}/rss".format(baseUrl, school)
        self._school = school

    def getData(self) -> List[Lunch]:
        r = requests.get(self._endpoint)
        food = []

        if r.status_code == 200:
            # First we need to parse the xml data from the request
            data = xmltodict.parse(r.text)
            items = data["rss"]["channel"]["item"]

            for i in items:
                # This parses the date from the rss.
                pubDate = i["pubDate"].split(" ")

                # This fixes the date parsed to "DAY MONTH YEAR".
                fixedDate = "{} {} {}".format(pubDate[1], pubDate[2], pubDate[3])

                # Then this makes it eaiser to use the date.
                date = datetime.strptime(fixedDate, "%d %b %Y")

                # Then we append it to the food array.
                # food.append({"date": date, "food": i["description"].split("<br/>")})
                food.append(Lunch(i["description"].split("<br/>"), date))

            return food
        else:
            return []
