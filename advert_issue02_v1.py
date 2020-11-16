import json
from typing import Dict


class ColorizeMixin:
    # def colorize(self, text):
    #     return text + self.repr_color_code

    @staticmethod
    def colorize(text: str, color_code: int):
        return f"\033[0;{color_code};40m {text}"
        # return text + color  # color берем из класса в этом случае


class AdvertAttrs:
    def __init__(self, data: Dict = None):
        if data is not None:
            for key, value in data.items():
                if not isinstance(value, Dict):
                    self.__setattr__(key, value)
                else:
                    self.__setattr__(key, AdvertAttrs(value))


class Advert(ColorizeMixin, AdvertAttrs):
    repr_color_code = 32

    def __init__(self, data: Dict):
        self._price = 0
        super().__init__(data)

    def __repr__(self):
        text = f"{self.title} | {self.price} ₽"
        return self.colorize(text, self.repr_color_code)

    @property
    def price(self) -> int:
        return self._price

    @price.setter
    def price(self, new_price: int) -> None:
        if new_price < 0:
            raise ValueError("price must be >= 0")

        self._price = new_price


def test_empty_price():
    advert_str = '{"title": "python"}'
    advert_json = json.loads(advert_str)
    advert = Advert(advert_json)
    assert hasattr(advert, "price")
    assert advert.price == 0


def test_negative_price():
    advert_str = '{"title": "python", "price": -1}'
    advert_json = json.loads(advert_str)
    try:
        _ = Advert(advert_json)
    except ValueError:
        pass
    else:
        assert ValueError()


def test_not_empty_location():
    advert_str = """{
                    "title": "python",
                    "price": 0,
                    "location": {
                        "address": "город Москва, Лесная, 7",
                        "metro_stations": ["Белорусская"]
                        }
                    }"""
    advert_json = json.loads(advert_str)
    advert = Advert(advert_json)
    assert hasattr(advert, "location")
    assert hasattr(advert.location, "address")
    assert advert.location.address == "город Москва, Лесная, 7"
    print(advert)


def test_multiple_nesting():
    advert_str = """{
                        "title": "python",
                        "price": 0,
                        "location": {
                            "address": "город Москва, Лесная, 7",
                            "metro_stations": ["Белорусская"]
                            },
                        "relationships": {
                            "owner": {
                                    "data": {
                                        "id": 1,
                                        "name": "NoName"
                                    }
                                }
                            }
                        }"""

    advert_json = json.loads(advert_str)
    advert = Advert(advert_json)
    assert hasattr(advert, "relationships")
    assert hasattr(advert.relationships, "owner")
    assert hasattr(advert.relationships.owner, "data")
    assert hasattr(advert.relationships.owner.data, "id")
    assert advert.relationships.owner.data.id == 1


def main():
    test_empty_price()
    test_negative_price()
    test_not_empty_location()
    test_multiple_nesting()


if __name__ == "__main__":
    main()
