from decimal import Decimal

from csmp_blok import CSMPBlok
from opcije_simulacije import OpcijeSimulacije


def json_u_csmp_blok(json_data):
    csmp_blok = CSMPBlok()
    csmp_blok.ulaz1 = json_data["ulaz1"]
    csmp_blok.ulaz2 = json_data["ulaz2"]
    csmp_blok.ulaz3 = json_data["ulaz3"]
    csmp_blok.par1 = Decimal(json_data["par1"])
    csmp_blok.par2 = Decimal(json_data["par2"])
    csmp_blok.par3 = Decimal(json_data["par3"])
    csmp_blok.sifra_bloka = json_data["sifra_bloka"]
    csmp_blok.rb_bloka = json_data["rb_bloka"]
    csmp_blok.sortiran = json_data["sortiran"]
    csmp_blok.rb_integratora = json_data["rb_integratora"]
    csmp_blok.izlaz = Decimal(json_data["izlaz"])
    csmp_blok.tip = json_data["tip"]
    return csmp_blok

def json_u_opcije_simulacije(opcije):
    opcije_simulacije = OpcijeSimulacije()
    opcije_simulacije.tabela_konfiguracije = opcije.get("tabela_konfiguracije")
    opcije_simulacije.interval_integracije = Decimal(opcije.get("interval_integracije"))
    opcije_simulacije.interval_stampanja = Decimal(opcije.get("interval_stampanja"))
    opcije_simulacije.pola_intervala_integracije = Decimal(opcije.get("pola_intervala_integracije"))
    opcije_simulacije.duzina_simulacije = Decimal(opcije.get("duzina_simulacije"))
    opcije_simulacije.trenutno_vreme = Decimal(opcije.get("trenutno_vreme"))

    if opcije.get("niz_blokova"):
        opcije_simulacije.niz_blokova = {}
        for k, v in opcije.get("niz_blokova").items():
            if not v: opcije_simulacije.niz_blokova[int(k)] = None
            else: opcije_simulacije.niz_blokova[int(k)] = json_u_csmp_blok(v)

    if opcije.get("niz_sortiran"):
        opcije_simulacije.niz_sortiran = {}
        for k, v in opcije.get("niz_sortiran").items():
            if not v: opcije_simulacije.niz_sortiran[int(k)] = None
            else: opcije_simulacije.niz_sortiran[int(k)] = json_u_csmp_blok(v)

    if opcije.get("niz_obradjen"):
        opcije_simulacije.niz_obradjen = {}
        for k, v in opcije.get("niz_obradjen").items():
            if not v:
                opcije_simulacije.niz_obradjen[int(k)] = None
            else:
                opcije_simulacije.niz_obradjen[int(k)] = json_u_csmp_blok(v)

    if opcije.get("niz_izlaza"):
        opcije_simulacije.niz_izlaza = {}
        for k, v in opcije.get("niz_izlaza").items():
            if not v: opcije_simulacije.niz_izlaza[int(k)] = None
            else: opcije_simulacije.niz_izlaza[int(k)] = Decimal(v)

    opcije_simulacije.matrica_izlaza = opcije.get("matrica_izlaza")

    opcije_simulacije.br_konstanti = opcije.get("br_konstanti")
    opcije_simulacije.br_blokova = opcije.get("br_blokova")
    opcije_simulacije.br_integratora = opcije.get("br_integratora")

    opcije_simulacije.niz_rb_integratora = {}
    if opcije.get("niz_rb_integratora"):
        for k, v in opcije.get("niz_rb_integratora").items():
            if not v:
                opcije_simulacije.niz_rb_integratora[int(k)] = None
            else:
                opcije_simulacije.niz_rb_integratora[int(k)] = int(v)

    opcije_simulacije.vektorX = {}
    opcije_simulacije.vektorY = {}
    opcije_simulacije.vektorZ = {}

    if opcije.get("vektorX"):
        for k, v in opcije.get("vektorX").items():
            if not v: opcije_simulacije.vektorX[int(k)] = None
            else: opcije_simulacije.vektorX[int(k)] = Decimal(v)

    if opcije.get("vektorY"):
        for k, v in opcije.get("vektorY").items():
            if not v: opcije_simulacije.vektorY[int(k)] = None
            else: opcije_simulacije.vektorY[int(k)] = Decimal(v)

    if opcije.get("vektorZ"):
        for k, v in opcije.get("vektorZ").items():
            if not v: opcije_simulacije.vektorZ[int(k)] = None
            else: opcije_simulacije.vektorZ[int(k)] = Decimal(v)

    opcije_simulacije.nizK = opcije.get("nizK")

    opcije_simulacije.faza_rada = {}
    if opcije.get("faza_rada"):
        for k, v in opcije.get("faza_rada").items():
            if not v: opcije_simulacije.faza_rada[int(k)] = None
            else: opcije_simulacije.faza_rada[int(k)] = v

    opcije_simulacije.preciznost = opcije.get("preciznost")
    opcije_simulacije.vrsta_prekida = opcije.get("vrsta_prekida")

    return opcije_simulacije
