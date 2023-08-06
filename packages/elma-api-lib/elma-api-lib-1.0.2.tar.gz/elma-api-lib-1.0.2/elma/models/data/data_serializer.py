from typing import Optional

from elma.models.data.data import Data
import json

from elma.models.data.dataitem import DataItem


def data_item_to_dict(data_item: DataItem) -> Optional[dict]:
    result = {}
    if data_item is not None:
        transformed_data = data_to_dict(data_item.data)
        transformed_data_array = []
        for data in data_item.data_array:
            jd = data_to_dict(data)
            transformed_data_array.append(jd)
        if data_item.name is not None:
            result["Name"] = data_item.name
        if data_item.value is not None:
            result["Value"] = data_item.value
        if transformed_data is not None:
            result["Data"] = transformed_data
        if transformed_data_array is not None and len(transformed_data_array) > 0:
            result["DataArray"] = transformed_data_array
    else:
        return None
    return result


def data_item_to_json_str(data_item: DataItem) -> str:
    return json.dumps(data_item_to_dict(data_item))


def data_to_dict(data: Data) -> dict:
    result = {}
    if data is not None:
        transformed_data_items = []
        for dataItem in data.items:
            jdi = data_item_to_dict(dataItem)
            transformed_data_items.append(jdi)
        if transformed_data_items is not None and len(transformed_data_items) > 0:
            result["Items"] = transformed_data_items
        if data.value is not None:
            result["Value"] = data.value
    return result


def data_to_json_str(data: Data) -> str:
    return json.dumps(data_to_dict(data))


def dict_to_data(json_data: dict) -> Data:
    result = Data()
    if json_data is not None:
        transformed_data_items = []
        for dataItem in json_data['Items']:
            jdi = dict_to_data_item(dataItem)
            transformed_data_items.append(jdi)
        if transformed_data_items is not None and len(transformed_data_items) > 0:
            result.items = transformed_data_items
        value = json_data['Value']
        if value is not None:
            result.value = value
    return result


def dict_to_data_item(json_item: dict) -> Optional[DataItem]:
    result = DataItem()
    if json_item is not None:
        transformed_data = dict_to_data(json_item['Data'])
        transformed_data_array = []
        for data in json_item['DataArray']:
            jd = dict_to_data(data)
            transformed_data_array.append(jd)
        name = json_item['Name']
        if name is not None:
            result.name = name
        value = json_item['Value']
        if value is not None:
            result.value = value
        if transformed_data is not None:
            result.data = transformed_data
        if transformed_data_array is not None and len(transformed_data_array) > 0:
            result.data_array = transformed_data_array
    else:
        return None
    return result


class DataSerializable:
    def to_Data(self) -> Data:
        items = []
        for k, v in self.__dict__.items():
            data_item = DataItem()
            data_item.name = k
            if v is None:
                data_item = None
            elif isinstance(v, DataItem):
                data_item = v
            elif isinstance(v, Data):
                data_item.data = v
            elif isinstance(v, DataSerializable):
                data_item.data = v.to_Data()
            elif isinstance(v, type([])):
                res = v
                for i in range(0, len(v)):
                    vi = v[i]
                    if isinstance(vi, DataSerializable):
                        res[i] = vi.to_Data()
                data_item.data_array = res
            else:
                data_item.value = v
            if data_item is not None:
                items.append(data_item)
        return Data(items=items)


class DataItemSerializable:
    def to_DataItem(self) -> DataItem:
        name = self.__class__.__name__
        value = None
        data = Data()
        data_array = []
        for k, v in self.__dict__.items():
            name = k
            if v is None:
                pass
            elif isinstance(v, Data):
                data = v
            elif isinstance(v, DataSerializable):
                data = v.to_Data()
            elif isinstance(v, type([])):
                res = v
                for i in range(0, len(v)):
                    vi = v[i]
                    if isinstance(vi, DataSerializable):
                        res[i] = vi.to_Data()
            else:
                value = v
            break
        return DataItem(name=name, value=value, data=data, data_array=data_array)
