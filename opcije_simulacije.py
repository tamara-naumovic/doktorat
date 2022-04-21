from dataclasses import dataclass

@dataclass
class OpcijeSimulacije():

    tabela_konfiguracije:str = ""
    interval_integracije:int = 0
    interval_stampanja:int = 0 
    duzina_simulacije:int = 0
    niz_blokova:list = None
    niz_sortiran:list = None
    niz_obradjen:list = None
    niz_izlaza: list = None #ovo bi trebalo da bude matrica
    br_konstanti:int = 0
    br_blokova:int= 0
    br_integratora:int = 0
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
