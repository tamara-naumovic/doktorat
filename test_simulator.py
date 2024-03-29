from opcije_simulacije import OpcijeSimulacije, DecimalEncoder
from time import sleep
import sim, json, pprint, time, decimal

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
    interv_s = decimal.Decimal(input("Unesi interval štampanja: "))
    # interv_i = decimal.Decimal('0.1')
    interv_i = decimal.Decimal(input("Unesi interval integracije: "))
    # duzina_s = decimal.Decimal('10')
    duzina_s = decimal.Decimal(input("Unesi dužinu simulacije: "))
    preciznost = int(input("Na kojoj decimali je potrebna preciznost: "))
    # tabela_konf = "testPodaci/termostat.csv"
    tabela_konf = input("Unesi putanju do tabele konfiguracije: ")
    opcije = OpcijeSimulacije(tabela_konfiguracije=tabela_konf, interval_stampanja= interv_s, interval_integracije= interv_i, duzina_simulacije= duzina_s, preciznost=preciznost)
    print("----------------Niz blokova-------------------")
    sim.ucitaj_blokove(opcije)
    print(json.dumps(opcije.niz_blokova, default=print,cls=DecimalEncoder))
    # pprint.pprint(opcije.niz_blokova)
    print("----------------Obradjen niz blokova-------------------")
    sim.obradi_niz_blokova(opcije)
    print(json.dumps(opcije.niz_obradjen, default=print,cls=DecimalEncoder))
    
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

    nit = sim.pokreni_simulaciju(opcije)
    sleep(2)
    sim.pauziraj_simulaciju()
    sleep(1)
    sim.nastavi_simulaciju()
    
    nit.join()
    
    # print(json.dumps(opcije.matrica_izlaza, indent=4))
    print("----------------Matrica izlaza-------------------")
    print(json.dumps(opcije.matrica_izlaza, indent=4,cls=DecimalEncoder))
    if "\\" in opcije.tabela_konfiguracije:

        file_name = opcije.tabela_konfiguracije.split("\\")[-1][:-4]
    else:
        file_name = opcije.tabela_konfiguracije.split("/")[-1][:-4]

    result_file_name = f"rezultati/result-{file_name}.json"
    print(f"naziv fajla: {result_file_name}")
    with open(result_file_name, 'w') as fp:
        json.dump(opcije.matrica_izlaza, fp,cls=DecimalEncoder)
    kraj = time.time()
    print(f"Duzina simulacije: {kraj-pocetak}")
    # print("----------------Izlazi-------------------")
    # print(opcije.niz_izlaza)    
    
    # print("----------------Rb integratora-------------------")
    # print(opcije.niz_rb_integratora)

    

    

if __name__ == "__main__":
    main()
