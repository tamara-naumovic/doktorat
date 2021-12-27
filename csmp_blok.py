from dataclasses import dataclass
import inspect
@dataclass
class CSMPBlok():
    
    ulaz1:int = -1
    ulaz2:int = -1
    ulaz3:int = -1
    par1:int = -1
    par2:int = -1
    par3:int = -1
    sifra_bloka:int = -1
    rb_bloka:int = -1
    sortiran:int = False
    rb_integratora:int = False
    izlaz:int = None
    tip:str = None

def from_dict_to_dataclass(cls, data):
    return cls(
        **{
            key: (data[key] if val.default == val.empty else data.get(key, val.default))
            for key, val in inspect.signature(CSMPBlok).parameters.items()
        }
    )



