from elma.models.data.data import Data


class DataItem:
    def __init__(self, name: str = None, value: str = None, data: Data = None, data_array: [] = None) -> None:
        if data_array is None:
            data_array = []
        self.name = name
        self.value = value
        self.data = data
        self.data_array = data_array

    def __str__(self) -> str:
        from elma.models.data.data_serializer import data_item_to_json_str
        return data_item_to_json_str(self)

    @staticmethod
    def from_json(json: dict):
        from elma.models.data.data_serializer import dict_to_data_item
        return dict_to_data_item(json)
