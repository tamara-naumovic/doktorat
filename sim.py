from timeit import repeat
from opcije_simulacije import OpcijeSimulacije
from csmp_blok import CSMPBlok, from_dict_to_dataclass
from math import sqrt, sin, cos, atan, exp, floor, ceil
from random import randint
# import numpy as np
# import matplotlib.pyplot as plt
# import scipy as sp
# from scipy.integrate import solve_ivp
import json, csv
from copy import copy




niz_izlaza:list = None
sifre = {
    "A": 1, #ArkusTangens
    "B": 2, #Signum
    "C": 3, #Kosinus
    "D": 4, #MrtvaZona
    "/": 5, #Delitelj
    "E": 6, #Eksponent
    "F": 7, #GeneratorFja
    "G": 8, #Pojacanje
    "H": 9, #KvadKoren
    "I": 10, #Integrator
    "J": 11, #GeneratorSlucBrojeva
    "K": 12, #Konstanta
    "L": 13, #Ogranicavac
    "M": 14, #ApsolutnaVrednost
    "-": 15, #Invertor
    "N": 16, #NegOgranicavac
    "O": 17, #Offset
    "P": 18, #PozOgranicavac
    "Q": 19, #KrajSimulacije
    "R": 20, #Relej
    "S": 21, #Sinus
    "T": 22, #GenImpulsa
    "U": 23, #JedinicnoKasnjenje
    "V": 24, #Vacuous
    "-t>": 25, #Vreme
    "W": 26, #Sabirac
    "X": 27, #Mnozac
    "Y": 28, #Wye
    "Z": 0, #KoloZadrske
}


def podesi_sifru():
    '''
    realizacija ove metode zavisi od nacina prosledjivanja tabele konfiguracije
    ako je u tabeli tip podesen kako sifra onda je metoda suvisna
    ako je u tabeli tip podesen kao karakter potrebno je deifnisati metodu
    tako da zavisno od tipa (cija lista postoji gore) kreira sifru
    '''
    pass



def sabirac(p1,p2,p3,u1,u2,u3,brojac):
    # print("usao u sabirac")

    izlaz = p1*u1+p2*u2+p3*u3


def mnozac(u1,u2,brojac):
    # print("usao u mnozac")

    izlaz=u1*u2


def apsolutnavrednost(u1,brojac):
    izlaz=abs(u1)


def delitelj(u1,u2,brojac):
    # print("usao u delitelj")
    izlaz=u1/u2


def invertor(u1,brojac):
    izlaz=-u1


def kvadratniKoren(u1,brojac):
    izlaz=sqrt(u1)


def offset(p1,u1,brojac):
    izlaz=p1+u1


def pojacanje(p1,u1,brojac):
    izlaz=p1*u1


def relej(u1,u2,u3,brojac):
    if u1<0:
        izlaz=u3
    else:
        izlaz=u2


def signum(u1,brojac):
    izlaz = None
    if u1<0:
        izlaz = -1
    elif u1>0:
        izlaz=1
    elif u1==0:
        izlaz=0


def sinus(p1,p2,p3,u1,brojac):
    izlaz=p1*sin(p2*u1 + p3)


def kosinus(p1,p2,p3,u1,brojac):
    # print("usao u kosinus")

    izlaz=p1*cos(p2*u1+p3)


def arkusTanges(p1,p2,p3,u1,brojac):

    izlaz=p1*atan(p2*u1+p3)


def eksponent(p1,p2,p3,u1,brojac):
    izlaz=p1*exp(p2*u1+p3)


def mrtvaZona(p1,p2,u1,brojac):
    #p1 donja granica, p2 gornja granica
    if u1>p1 and u1<p2:
        izlaz=0
    else:
        izlaz= u1


def generatorSlucajnihBrojeva( brojac):
    izlaz = randint(1,99999)


def ogranicavac(p1,p2,u1,brojac):
    #p1 donja granica, p2 gornja granica
    if u1<p1:
        izlaz=p1
    else:
        if u1>p2:
            izlaz=p2
        else:
            izlaz=u1


def negativniOgranicavac(u1,brojac):
    if u1<0:
        izlaz=0
    else:
        izlaz=u1


def pozitivniOgranicavac(u1,brojac):
    if u1>0:
        izlaz= 0
    else:
        izlaz=u1

#
# def generatorFja(p1,p2,p3,u1,brojac):
#     pomaA, pomB = 0,0
#     pomA = p1-p2
#     p3=p1-p2
#     if(p3>0):
#         par1=10*(u1-p2)/p3
#         pomb = floor(par1)
#         if p1<0:
#            izlaz= self.FunkGener[pomA][1]
#         else:
#             if pomb>=10:
#                 izlaz=self.FunkGener[pomaA][11]
#             p2=pomB
#             p3=p1-p2
#             p1=self.FunkGener[pomaA][pomB+1]
#             p2=self.FunkGener[pomaA][pomB+2]
#             izlaz=p1+p3(p2-p1)
#     else:
#         self.VrstaPrekida['tip'] = "GreskaObrade"
#         self.VrstaPrekida['poruka'] ='Kod generatora f-ja razlika prvog i drugog parametra mora biti pozitivna!'


def generatorImpulsa(p1,u1,brojac):
    izlaz = 1 if u1>0 else 0

#
# def jedinicnoKasnjenje(p1,p2,u1,brojac):

#     if self.VrstaPrekida['tip'] == "NemaRac":
#         izlaz=p1
#     else:
#         izlaz=p2
#     self.ObradjenNiz[brojac]['parII'] = u1


def integrator(p2,p3,u1,u2,u3):
    # print("usao u integrator")
    izlaz = u1+p2*u2+p3*u3
    return izlaz



#
# def kolozadrske(p1,p2,u1,u2,brojac):
#     if self.VrstaPrekida['tip'] == 'NemaRac':
#         self.ObradjenNiz[brojac]["parII"] = p1
#         p2=p1
#     if u2<0:
#         izlaz=0
#     elif u2==0:
#         izlaz=p2
#     else:
#         self.ObradjenNiz[brojac]["parII"]=u1
#         izlaz=u1

#
# def krajSimulacije(u1,u2,brojac):
#     if u2<u1:
#         self.VrstaPrekida['tip'] = "KrajQuit"
#         self.VrstaPrekida['poruka'] = "Kraj simulacije od strane Quit elementa."

#
# def vacuous(sledeciblok, brojac):
#     if self.VrstaPrekida['tip'] == "NemaRac":
#         self.ObradjenNiz[brojac]["rbIntegratora"] = sledeciblok

#
# def wye(p1,p2,u1,u2,brojac,pomUl1,sledeciBlok):
#     pomA = 0.0
#     if u1==0:
#         self.VrstaPrekida['tip'] = 'GreskaObrade'
#         self.VrstaPrekida['poruka'] = 'Prvi ulaz u Wye element je jednak nuli ili ne postoji!'
#     else:
#         pomA=abs(1-u2/u1)
#         if pomA<p1:
#             izlaz=u1
#         else:
#             self.NizIzlaza[pomUl1] = (1-p2)*u1+p2*u2
#             sledeciBlok=self.ObradjenNiz[pomUl1]["rbIntegratora"]
#             self.izracunaj(sledeciBlok)


def izracunaj_izlaz():
    pass


def ucitaj_blokove( opsim:OpcijeSimulacije):
    lista_dict = []
    with open(opsim.tabela_konfiguracije, mode='r') as csv_file:
        reader = csv.DictReader(csv_file,delimiter=',',quotechar='|')
        for row in reader:
            red = {
                'ulaz1':int(row["u1"]),
                'ulaz2':int(row["u2"]),
                'ulaz3':int(row["u3"]),
                'par1':float(row["p1"]),
                'par2':float(row["p2"]),
                'par3':float(row["p3"]),
                'sortiran':False,
                'tip':row["tip"],
                'rb_bloka':int(row["rbr"]),
                'rb_integratora':-1,
                'sifra_bloka': sifre[str(row["tip"])]
            }
            lista_dict.append(red)

    with open("test.json", 'w') as outfile:
        json.dump(lista_dict,outfile )
    opsim.niz_blokova = lista_dict
    # return lista_dict


def kreiraj_blokove( opsim:OpcijeSimulacije):
    lista_blokova=[]
    for el in opsim.niz_blokova:
        csmpblk = from_dict_to_dataclass(CSMPBlok, el)
        lista_blokova.append(csmpblk)
    opsim.niz_blokova = lista_blokova
    # return lista_blokova


def vrati_blok( lista:list[CSMPBlok], rbr):
    for el in lista:
        if el.rb_bloka==0:
            return None
        elif el.rb_bloka==rbr:
            return el


def obradi_niz_blokova( opsim:OpcijeSimulacije):
    obradjen_niz = copy(opsim.niz_blokova)
    for blok in obradjen_niz:
        if blok.sifra_bloka != 10:
            blok.rb_integratora = 0
        elif blok.sifra_bloka==10:
            u1_blok = vrati_blok(obradjen_niz, blok.ulaz1)
            u2_blok = vrati_blok(obradjen_niz, blok.ulaz2)
            u3_blok = vrati_blok(obradjen_niz, blok.ulaz3)
            if (u1_blok!=None and u1_blok.sifra_bloka==10) or (u2_blok!=None and u2_blok.sifra_bloka==10) or (u3_blok!=None and u3_blok.sifra_bloka==10):
                blok.rb_integratora=2
            else:
                blok.rb_integratora=1
    opsim.niz_obradjen = obradjen_niz



def racunaj():
    v0 = 0
    t = 0.1

    sol_m2 = solve_ivp(integrator, t_span=(0,t), y0=[v0], t_eval=t, method="RK45", args=(0,0,10,0,0))
    print(sol_m2.y)
    # v_sol_m2 = sol_m2.y[0]

    # plt.plot(t, v_sol_m2)
    # plt.ylabel('$v(t)$', fontsize=22)
    # plt.xlabel('$t$', fontsize=22)
    # plt.show()

def sortiraj_niz(opcije: OpcijeSimulacije):
    
    opcije.br_blokova = len(opcije.niz_obradjen)
    # print(opcije.br_blokova)
    opcije.niz_sortiran = []
    br_sortiranih = 0

    #postavljanje konstanti na prvo mesto 
    for i in range(opcije.br_blokova):
        if opcije.niz_obradjen[i].rb_bloka != 0 and opcije.niz_obradjen[i].sifra_bloka == sifre["K"]:
            br_sortiranih += 1
            opcije.niz_sortiran.append(opcije.niz_obradjen[i])
            opcije.niz_obradjen[i].sortiran = True
    while True:
        if i== opcije.br_blokova and not ponovo:
            break
        i = 0
        ponovo = False
        while i < opcije.br_blokova and not ponovo:
            if not opcije.niz_obradjen[i].sortiran:

                ulaz1 = opcije.niz_obradjen[i].ulaz1
                ulaz2 = opcije.niz_obradjen[i].ulaz2
                ulaz3 = opcije.niz_obradjen[i].ulaz3
                #kao ulaz se dobije redni br bloka, redni brojevi pocinju od 1 
                #indeksi blokova u obradjeni_niz pocinju od 0
                #zato ulazN-1
                uslov1 = opcije.niz_obradjen[ulaz1-1].sifra_bloka in [sifre["I"], sifre["U"]] or opcije.niz_obradjen[ulaz1-1].sortiran or ulaz1 in [0, opcije.br_blokova]
                uslov2 = opcije.niz_obradjen[ulaz2-1].sifra_bloka in [sifre["I"], sifre["U"]] or opcije.niz_obradjen[ulaz2-1].sortiran or ulaz2 in [0, opcije.br_blokova]
                uslov3 = opcije.niz_obradjen[ulaz3-1].sifra_bloka in [sifre["I"], sifre["U"]] or opcije.niz_obradjen[ulaz3-1].sortiran or ulaz3 in [0, opcije.br_blokova]
                if uslov1 and uslov2 and uslov3:
                    ponovo = True
                    br_sortiranih += 1
                    opcije.niz_sortiran.append(opcije.niz_obradjen[i])
                    opcije.niz_obradjen[i].sortiran = True
                else:
                    ponovo = False
            if not ponovo:
                i += 1
        

