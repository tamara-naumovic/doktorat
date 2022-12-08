from dataclasses import dataclass
from csmp_blok import CSMPBlok

@dataclass
class OpcijeSimulacije():

    tabela_konfiguracije:str = ""
    interval_integracije:float = 0
    interval_stampanja:float = 0 
    pola_intervala_integracije:float = 0
    duzina_simulacije:float = 0.0
    trenutno_vreme:float =0
    niz_blokova:dict[int,list[CSMPBlok]] = None
    niz_sortiran:dict[int,list[CSMPBlok]] = None
    niz_obradjen:dict[int,list[CSMPBlok]] = None
    niz_izlaza: dict[int,float] = None #pomocni izlazi za neki interval integracije
    matrica_izlaza:dict[str,list] = None #matrica svih izlaza za sve intervale intergracije
    # matrica_izlaza:list = None #matrica svih izlaza za sve intervale intergracije
    br_konstanti:int = 0
    br_blokova:int= 0
    br_integratora:int = 0
    niz_rb_integratora:dict[int,int] = None #niz rbintg:rbblok
    #vektori postavljeni na dict da bi imali vrednosti od 1 do br intergratora, umesto da 0 preskacemo
    vektorX:dict[int,float] = None #cuva vrednosti svih integratora
    vektorY:dict[int,float] = None # y(n+1)
    vektorZ:dict[int,float] = None # y(n)
    nizK:dict[int,list] = None
    vrsta_prekida:dict[int,str] = None
    # vrsta_prekida = {
    # 0:nemarac,
    # 1:prvapol
    # 2:drugapol
    # 3:quit
    # 4:greska
    # }
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
