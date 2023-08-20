import uuid

from opcije_simulacije import OpcijeSimulacije, DecimalEncoder
from csmp_blok import CSMPBlok
from decimal import Decimal
from time import sleep
import sim, json, pprint, time, decimal
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/ucitaj_blokove', methods=['POST'])
def ucitaj_blokove():
    data = request.json.get('opcije')
    opcije_simulacije: OpcijeSimulacije = json_u_opcije_simulacije(data)
    obradjene_opcije = sim.ucitaj_blokove(opcije_simulacije)
    return jsonify({'opcije' : obradjene_opcije})


@app.route('/obradi_niz_blokova', methods=['POST'])
def obradi_niz_blokova():
    data = request.json.get('opcije')
    opcije_simulacije: OpcijeSimulacije = json_u_opcije_simulacije(data)
    obradjene_opcije = sim.obradi_niz_blokova(opcije_simulacije)
    return jsonify({'opcije': obradjene_opcije})


@app.route('/sortiraj_niz', methods=['POST'])
def sortiraj_niz():
    data = request.json.get('opcije')
    opcije_simulacije: OpcijeSimulacije = json_u_opcije_simulacije(data)
    obradjene_opcije = sim.sortiraj_niz(opcije_simulacije)
    return jsonify({'opcije': obradjene_opcije})


@app.route('/pokreni_simulaciju', methods=['POST'])
def pokreni_simulaciju():
    data = request.json.get('opcije')
    opcije_simulacije: OpcijeSimulacije = json_u_opcije_simulacije(data)
    novi_uuid = sim.pokreni_simulaciju(opcije_simulacije)
    return jsonify({'uuid': novi_uuid})


@app.route('/pauziraj_simulaciju/<nit>', methods=['GET'])
def pauziraj_simulaciju(nit):
    print(f'pauziram {nit}')
    opcije = sim.pauziraj_simulaciju(uuid.UUID(nit))
    return jsonify({'opcije': opcije})


@app.route('/nastavi_simulaciju/<nit>', methods=['GET'])
def nastavi_simulaciju(nit):
    print(f'nastavljam {nit}')

def create_csmp_blok_from_json(json_data):
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
            else: opcije_simulacije.niz_blokova[int(k)] = create_csmp_blok_from_json(v)

    if opcije.get("niz_sortiran"):
        opcije_simulacije.niz_sortiran = {}
        for k, v in opcije.get("niz_sortiran").items():
            if not v: opcije_simulacije.niz_sortiran[int(k)] = None
            else: opcije_simulacije.niz_sortiran[int(k)] = create_csmp_blok_from_json(v)

    if opcije.get("niz_obradjen"):
        opcije_simulacije.niz_obradjen = {}
        for k, v in opcije.get("niz_obradjen").items():
            if not v:
                opcije_simulacije.niz_obradjen[int(k)] = None
            else:
                opcije_simulacije.niz_obradjen[int(k)] = create_csmp_blok_from_json(v)

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


def main():
    pocetak = time.time()
    # opcije = OpcijeSimulacije(tabela_konfiguracije="testPodaci/tk11.csv", interval_stampanja= 0.1, interval_integracije= 0.1, duzina_simulacije= 10)
    # student test
    # interv_s = decimal.Decimal('0.1')
    print("""Pravila simulacije:
    1. Interval integracije i interval štampanja su decimalni zapisi. Npr 0.1 | 0.01
    2. Interval štampanja ne može biti veći od intervala integracije
    3. Dužina simulacije je ceo broj veći od 0
    4. Tabela konfiguracije je relativna ili apsolutna putanja do csv fajla
    """)
    # interv_s = decimal.Decimal(input("Unesi interval štampanja: "))
    interv_s = decimal.Decimal('0.001')
    interv_i = decimal.Decimal('0.1')
    # interv_i = decimal.Decimal(input("Unesi interval integracije: "))
    duzina_s = decimal.Decimal('50')
    # duzina_s = decimal.Decimal(input("Unesi dužinu simulacije: "))
    # preciznost = int(input("Na kojoj decimali je potrebna preciznost: "))
    preciznost = 2
    tabela_konf = "C:\\Users\\milos\\PycharmProjects\\doktorat\\testPodatak\\tk1.csv"
    # tabela_konf = input("Unesi putanju do tabele konfiguracije: ")
    opcije = OpcijeSimulacije(tabela_konfiguracije=tabela_konf, interval_stampanja=interv_s, interval_integracije=interv_i, duzina_simulacije=duzina_s, preciznost=preciznost)
    print("----------------Niz blokova-------------------")
    sim.ucitaj_blokove(opcije)
    print(json.dumps(opcije.niz_blokova, default=print, cls=DecimalEncoder))
    # pprint.pprint(opcije.niz_blokova)
    print("----------------Obradjen niz blokova-------------------")
    sim.obradi_niz_blokova(opcije)
    print(json.dumps(opcije.niz_obradjen, default=print, cls=DecimalEncoder))

    print("----------------Niz Rb integratora-------------------")
    print(opcije.niz_rb_integratora)

    print("----------------Sortiran niz blokova-------------------")
    sim.sortiraj_niz(opcije)
    print(opcije.niz_sortiran)
    # print(json.dumps(opcije.niz_sortiran, default=print,cls=DecimalEncoder))
    # print("----------------Niz izlaza-------------------")

    # sim.generisi_izlaz_indekse(opcije)
    # # # print(json.dumps(opcije.niz_izlaza, indent=2))

    # print("----------------Pocetni izlazi-------------------")
    # sim.postavi_pocetne_izlaze(opcije)
    # print(opcije.niz_izlaza,sep="\n")

    # print("----------------Vektory X-------------------")
    # print(opcije.vektorX)
    print("----------------Br integratora-------------------")
    print(opcije.br_integratora)
    print("----------------Racunaj-------------------")

    id_simulacije = sim.pokreni_simulaciju(opcije)
    sim.pauziraj_simulaciju(id_simulacije)
    sleep(2)
    sim.nastavi_simulaciju(id_simulacije)

    for i in range(7):
        print(i)
        sleep(1)
    # print(json.dumps(opcije.matrica_izlaza, indent=4))
    print("----------------Matrica izlaza-------------------")
    print(json.dumps(opcije.matrica_izlaza, indent=4, cls=DecimalEncoder))
    if "\\" in opcije.tabela_konfiguracije:

        file_name = opcije.tabela_konfiguracije.split("\\")[-1][:-4]
    else:
        file_name = opcije.tabela_konfiguracije.split("/")[-1][:-4]

    result_file_name = f"rezultati/result-{file_name}.json"
    print(f"naziv fajla: {result_file_name}")
    with open(result_file_name, 'w') as fp:
        json.dump(opcije.matrica_izlaza, fp, cls=DecimalEncoder)
    kraj = time.time()
    print(f"Duzina simulacije: {kraj - pocetak}")
    # print("----------------Izlazi-------------------")
    # print(opcije.niz_izlaza)    

    # print("----------------Rb integratora-------------------")
    # print(opcije.niz_rb_integratora)


if __name__ == "__main__":
    # app.run()
    main()
