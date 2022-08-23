from opcije_simulacije import OpcijeSimulacije
import sim, json

def main():
    opcije = OpcijeSimulacije("test_data/tk2.csv", 0.1, 0.1, 10)

    # Simulator.ucitaj_blokove(opcije)
    # print(opcije.niz_blokova)
    # Simulator.kreiraj_blokove( opcije)
    # print(opcije.niz_blokova)
    # Simulator.obradi_niz_blokova(opcije)
    # print(opcije.niz_obradjen)
    sim.ucitaj_blokove(opcije)
    print(*opcije.niz_blokova)
    print("----------------Niz blokova-------------------")
    sim.kreiraj_blokove(opcije)
    print(*opcije.niz_blokova,sep="\n")
    print("----------------Obradjen niz blokova-------------------")

    sim.obradi_niz_blokova(opcije)
    print(*opcije.niz_obradjen,sep="\n")
    print("----------------Sortiran niz blokova-------------------")

    sim.sortiraj_niz(opcije)
    print(*opcije.niz_sortiran,sep="\n")
    print("----------------Niz izlaza-------------------")

    sim.generisi_izlaz_indekse(opcije)
    print(json.dumps(opcije.niz_izlaza, indent=2))

if __name__ == "__main__":
    main()
