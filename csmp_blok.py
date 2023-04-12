from dataclasses import dataclass
import inspect
from decimal import Decimal
@dataclass
class CSMPBlok():
    
    ulaz1:int = 0
    ulaz2:int = 0
    ulaz3:int = 0
    par1:Decimal = Decimal('0')
    par2:Decimal = Decimal('0')
    par3:Decimal = Decimal('0')
    sifra_bloka:int = -1
    rb_bloka:int = -1
    sortiran:bool = False
    rb_integratora:int = False
    izlaz:Decimal = Decimal('0')
    tip:str = None

def from_dict_to_dataclass(cls, data)->CSMPBlok:
    return cls(
        **{
            key: (data[key] if val.default == val.empty else data.get(key, val.default))
            for key, val in inspect.signature(CSMPBlok).parameters.items()
        }
    )



