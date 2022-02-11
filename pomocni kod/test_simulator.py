from opcije_simulacije import OpcijeSimulacije
from simulator import Simulator
import sim

def main():
    opcije = OpcijeSimulacije("tk1.csv",0.1,0.1,10)

    # Simulator.ucitaj_blokove(opcije)
    # print(opcije.niz_blokova)
    # Simulator.kreiraj_blokove( opcije)
    # print(opcije.niz_blokova)
    # Simulator.obradi_niz_blokova(opcije)
    # print(opcije.niz_obradjen)    
    sim.ucitaj_blokove(opcije)
    print(opcije.niz_blokova)
    sim.kreiraj_blokove( opcije)
    print(opcije.niz_blokova)
    sim.obradi_niz_blokova(opcije)
    print(opcije.niz_obradjen)


if __name__=="__main__":
    main()