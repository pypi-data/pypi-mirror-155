from elma.models.data.data import Data
from elma.models.data.util.data_serializer import DataSerializable


class StartProcess(DataSerializable):
    # Поля для наследников класса DataSerializable следует называть так, как они будут передаваться в Json,
    # так как данный класс будет трансформирован в вид Data на основе названий полей в данном классе.
    def __init__(self, context_vars: Data = Data(), process_name=None,
                 process_token: str = None, process_header_id: int = None) -> None:
        self.Context = context_vars
        self.ProcessName = process_name
        self.ProcessToken = process_token
        self.ProcessHeaderId = process_header_id
        super().__init__()
