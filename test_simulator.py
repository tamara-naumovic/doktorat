from opcije_simulacije import OpcijeSimulacije
import sim, json, pprint

def main():
    opcije = OpcijeSimulacije("test_data/tk2_2.csv", 0.1, 0.1, 10)
    print("----------------Niz blokova-------------------")
    sim.ucitaj_blokove(opcije)
    print(json.dumps(opcije.niz_blokova, default=print))
    # pprint.pprint(opcije.niz_blokova)
    print("----------------Obradjen niz blokova-------------------")
    sim.obradi_niz_blokova(opcije)
    print(json.dumps(opcije.niz_obradjen, default=print))
    
    print("----------------Niz Rb integratora-------------------")
    print(opcije.niz_rb_integratora)
    
    print("----------------Sortiran niz blokova-------------------")
    sim.sortiraj_niz(opcije)
    print(json.dumps(opcije.niz_sortiran, default=print))
    # print("----------------Niz izlaza-------------------")

    # sim.generisi_izlaz_indekse(opcije)
    # # # print(json.dumps(opcije.niz_izlaza, indent=2))

    print("----------------Pocetni izlazi-------------------")
    sim.postavi_pocetne_izlaze(opcije)
    print(opcije.niz_izlaza,sep="\n")
    
    print("----------------Vektory Y-------------------")
    print(opcije.vektorY)

    # print("----------------Izlazi-------------------")
    # print(opcije.niz_izlaza)    
    
    # print("----------------Rb integratora-------------------")
    # print(opcije.niz_rb_integratora)

    

    

if __name__ == "__main__":
    main()
