class Data:
    def __init__(self, items: [] = None, value: str = None) -> None:
        if items is None:
            items = []
        self.items = items
        self.value = value

    def __str__(self) -> str:
        from elma.models.data.data_serializer import data_to_json_str
        return data_to_json_str(self)

    @staticmethod
    def from_json(json: dict):
        from elma.models.data.data_serializer import dict_to_data
        return dict_to_data(json)
