from dataclasses import dataclass
import numpy as np

@dataclass
class IDCardData:
    name:str
    address:str
    id_number:str
    factory_number:str
    gender:str
    birth_date:str
    english_id_number:str
    photo:np.ndarray

@dataclass
class InputData:
    path:str