from dataclasses import dataclass
from csmp_blok import CSMPBlok
from decimal import Decimal
import json

@dataclass
class OpcijeSimulacije():

    tabela_konfiguracije: str = ""
    interval_integracije: Decimal = Decimal('0')
    interval_stampanja: Decimal = Decimal('0')
    pola_intervala_integracije: Decimal = Decimal('0')
    duzina_simulacije: Decimal = Decimal('0')
    trenutno_vreme: Decimal = Decimal('0')
    niz_blokova: dict[int, list[CSMPBlok]] = None #int = index bloka
    niz_sortiran: dict[int, list[CSMPBlok]] = None #int = rbr bloka
    niz_obradjen: dict[int, list[CSMPBlok]] = None #int = rbr bloka
    # pomocni izlazi za neki interval integracije
    niz_izlaza: dict[int, Decimal] = None #int = rbr bloka
    # matrica svih izlaza za sve intervale intergracije
    matrica_izlaza: dict[str, list] = None #str = vreme, list je lista vrednosti izlaza za to vreme
    # matrica_izlaza:list = None #matrica svih izlaza za sve intervale intergracije
    br_konstanti: int = 0
    br_blokova: int = 0
    br_integratora: int = 0
    niz_rb_integratora: dict[int, int] = None  # niz rbintg:rbblok
    # vektori postavljeni na dict da bi imali vrednosti od 1 do br intergratora, umesto da 0 preskacemo
    vektorX: dict[int, Decimal] = None  # cuva vrednosti svih integratora
    vektorY: dict[int, Decimal] = None  # y(n+1)
    vektorZ: dict[int, Decimal] = None  # y(n)
    nizK: dict[int, list] = None
    faza_rada: dict[int, str] = None
    preciznost: int = 10
    vrsta_prekida = None

    '''
        tabela_konfiguracije se dobija u vidu csv fajla
        i konvertuje se u listu rečnika
        jedan rečnik predstavlja jedan blok u listi 
        {
            "tip":"I",
            "rb":1,
            "ulaz1" = 2
            "ulaz2" = 0
            "ulaz3" = 0
            "par1" = 0
            "par2" = 0
            "par3" = 0
        }
    '''



class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)