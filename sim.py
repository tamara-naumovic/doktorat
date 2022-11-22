from timeit import repeat
from opcije_simulacije import OpcijeSimulacije
from csmp_blok import CSMPBlok, from_dict_to_dataclass
from math import sqrt, sin, cos, atan, exp, copysign
from random import uniform
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
    ako je u tabeli tip podesen kao sifra onda je metoda suvisna
    ako je u tabeli tip podesen kao karakter potrebno je deifnisati metodu
    tako da zavisno od tipa (cija lista postoji gore) kreira sifru
    '''
    pass

# def izlaz(izlaz, brojac, opsim:OpcijeSimulacije):
#     if brojac!=0:
#         opsim.niz_izlaza[brojac]=izlaz
#         return 
#     else: return izlaz

def sabirac(p1,p2,p3,u1,u2,u3):
    izlaz=p1*u1+p2*u2+p3*u3
    return izlaz

def mnozac(u1,u2):
    izlaz = u1*u2
    return izlaz

def apsolutnavrednost(u1):
    izlaz=abs(u1)
    return izlaz

def delitelj(u1,u2):
    if u2!=0:
        izlaz=u1/u2
        return izlaz
    else: return False

def invertor(u1):
    izlaz=-u1
    return izlaz

def kvadratniKoren(u1):
    izlaz=sqrt(u1)
    return izlaz

def offset(p1,u1):
    izlaz=p1+u1
    return izlaz

def pojacanje(p1,u1):
    izlaz=p1*u1
    return izlaz

def relej(u1,u2,u3):
    izlaz = u3 if u1<0 else u2
    return izlaz

def signum(u1):
    izlaz = 0 if u1==0 else copysign(1,u1)
    return izlaz

def sinus(p1,p2,p3,u1):
    izlaz=p1*sin(p2*u1 + p3)
    return izlaz

def kosinus(p1,p2,p3,u1):
    izlaz=p1*cos(p2*u1+p3)
    return izlaz

def arkusTanges(p1,p2,p3,u1):
    if (p2*u1+p3)>=0.0:
        izlaz=p1*atan(p2*u1+p3)
        return izlaz
    else: 
        print("Arkus tanges je negativan") #dodati obradu grešaka
        return False

def eksponent(p1,p2,p3,u1):
    izlaz=p1*exp(p2*u1+p3)
    return izlaz

def mrtvaZona(p1,p2,u1,brojac,opsim:OpcijeSimulacije):
    #p1 donja granica, p2 gornja granica
    izlaz=0 if p1<u1<p2 else u1
    return izlaz

def generatorSlucajnihBrojeva(brojac, opsim:OpcijeSimulacije):
    izlaz = uniform(0,1)
    return izlaz

def ogranicavac(p1,p2,u1):
    izlaz = p1 if u1<p1 else p2 if u1<p2 else u1
    return izlaz

def negativniOgranicavac(u1):
    izlaz = 0 if u1<0 else u1
    return izlaz

def pozitivniOgranicavac(u1):
    izlaz = 0 if u1>0 else u1
    return izlaz
#integratoru treba opsim jer upisuje u vektorY
def integrator(p2,p3,u1,u2,u3, opsim:OpcijeSimulacije, rbInteg):
    # blok_intg = opsim.niz_sortiran[brojac]
    opsim.vektorY[rbInteg] = u1+p2*u2+p3*u3
    # return True sta integrator da vrati kao izlaz

#pitati profesora za>

def generatorFja(p1,p2,p3,u1):
    pass
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


def generatorImpulsa(p1,u1):
    izlaz = 1 if u1>0 else 0
    return izlaz

#
def jedinicnoKasnjenje(p1,p2,u1):
    #pogledati validnost potpisa ove funkcije
    pass

#     if self.VrstaPrekida['tip'] == "NemaRac":
#         izlaz=p1
#     else:
#         izlaz=p2
#     self.ObradjenNiz[brojac]['parII'] = u1

def kolozadrske(p1,p2,u1,u2):
    pass
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
def krajSimulacije(u1,u2):
    pass
#     if u2<u1:
#         self.VrstaPrekida['tip'] = "KrajQuit"
#         self.VrstaPrekida['poruka'] = "Kraj simulacije od strane Quit elementa."

#
def vacuous(sledeciblok, brojac):
    pass
#     if self.VrstaPrekida['tip'] == "NemaRac":
#         self.ObradjenNiz[brojac]["rbIntegratora"] = sledeciblok

#
def wye(p1,p2,u1,u2,pomUl1,sledeciBlok):
    pass
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

def incijalizuj_sve(opsim:OpcijeSimulacije, brElemenata):
    #inicijalizacija niz_blokova
    opsim.niz_blokova = {}
    opsim.niz_obradjen = {}
    opsim.niz_sortiran = {}
    for i in range(brElemenata):
        if i ==0:
            opsim.niz_blokova[i] = None
            opsim.niz_obradjen[i] = None
            opsim.niz_sortiran[i] = None
        opsim.niz_blokova[i+1] = []
        opsim.niz_obradjen[i+1] = []
        opsim.niz_sortiran[i+1] = []
    opsim.br_blokova = brElemenata
    

def ucitaj_blokove( opsim:OpcijeSimulacije):
    '''
    funkcija koja ucitava blokove iz tabele konfiguracije koja je zapamcena u OpcijeSimulacije
    i kreira CSMP blokove u formatu recnika koje pamti u opsim.niz_blokova.
    opsim.niz_blokova se dalje koristi za obradu
    '''
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
        json.dump(lista_dict,outfile)
    
    #inicijalizacija 
    incijalizuj_sve(opsim, len(lista_dict))

    for element in lista_dict:
        csmpblok = from_dict_to_dataclass(CSMPBlok,element)
        opsim.niz_blokova[csmpblok.rb_bloka] = csmpblok
    # return lista_dict

def obradi_niz_blokova(opsim:OpcijeSimulacije):
    '''
    funkcija obradjuje opsim.niz_blokova i kreira opsim.niz_obradjen
    prilikom obrade inicijalni parametri bloka vezani za redni broj integratora (-1) se menjaju
    u zavisnosti od toga da li je blok integrator ili ne
    takodje upisuje se opsim.br_integratora na broj integrator blokova
    '''
    obradjen_niz = copy(opsim.niz_blokova)
    opsim.br_integratora = len([obradjen_niz[i] for i in range(1,len(obradjen_niz)) if obradjen_niz[i].sifra_bloka==10])
    opsim.niz_rb_integratora = {}
    for i in range(1,opsim.br_integratora+1):
        opsim.niz_rb_integratora[i] = -1 #nije postavljen rbBloka ako je -1
    opsim
    for blok in obradjen_niz.values():
        if blok==None:
            continue
        if blok.sifra_bloka != 10:
            blok.rb_integratora = 0
        elif blok.sifra_bloka==10: #ako je blok integrator
            u1_blok = obradjen_niz[blok.ulaz1]
            u2_blok = obradjen_niz[blok.ulaz2]
            u3_blok = obradjen_niz[blok.ulaz3]
            if (u1_blok!=None and u1_blok.sifra_bloka==10) or (u2_blok!=None and u2_blok.sifra_bloka==10) or (u3_blok!=None and u3_blok.sifra_bloka==10):
                blok.rb_integratora=2
                opsim.niz_rb_integratora[blok.rb_integratora]=blok.rb_bloka
                #niz_rb_integratora treba da pamti redne brojeve blokova koji su integratori
            else:
                blok.rb_integratora=1
                opsim.niz_rb_integratora[blok.rb_integratora]=blok.rb_bloka
    opsim.niz_obradjen = obradjen_niz

def sortiraj_niz(opsim: OpcijeSimulacije):
    '''
    funkcija sortira blokove po zadatom algoritmu, tako da blokovi ciji su ulazi poznati stoje na pocetku
    '''
    br_sortiranih = 0

    #postavljanje konstanti na prvo mesto 
    for blok in opsim.niz_obradjen.values():
        if blok==None:
            continue
        if blok.rb_bloka != 0 and blok.sifra_bloka == sifre["K"]:
            br_sortiranih += 1
            opsim.niz_sortiran[br_sortiranih]= blok
            blok.sortiran = True
    while True:
        i = 1
        ponovo = False
        while i <= opsim.br_blokova and not ponovo:
            if not opsim.niz_obradjen[i].sortiran and opsim.niz_obradjen[i].rb_bloka!=0:
                ulaz1 = opsim.niz_obradjen[i].ulaz1
                ulaz2 = opsim.niz_obradjen[i].ulaz2
                ulaz3 = opsim.niz_obradjen[i].ulaz3
                #kao ulaz se dobije redni br bloka, redni brojevi pocinju od 1 ili nula ako ne postoji
                if ulaz1!=0:
                    uslov1 = opsim.niz_obradjen[ulaz1].sifra_bloka in [sifre["I"], sifre["U"]] or opsim.niz_obradjen[ulaz1].sortiran or ulaz1 in [0, opsim.br_blokova]
                else: uslov1 = True
                if ulaz2!=0:
                    uslov2 = opsim.niz_obradjen[ulaz2].sifra_bloka in [sifre["I"], sifre["U"]] or opsim.niz_obradjen[ulaz2].sortiran or ulaz2 in [0, opsim.br_blokova]
                else: uslov2=True
                if ulaz3!=0:
                    uslov3 = opsim.niz_obradjen[ulaz3].sifra_bloka in [sifre["I"], sifre["U"]] or opsim.niz_obradjen[ulaz3].sortiran or ulaz3 in [0, opsim.br_blokova]
                else: uslov3 = True

                if uslov1 and uslov2 and uslov3:
                    ponovo = True
                    br_sortiranih += 1
                    opsim.niz_sortiran[br_sortiranih]=opsim.niz_obradjen[i]
                    opsim.niz_obradjen[i].sortiran = True
                else:
                    ponovo = False
            if not ponovo:
                i += 1
        if br_sortiranih==opsim.br_blokova:
                    break
            

def upisi_izlaz(opsim: OpcijeSimulacije, brojac, izlaz):
    opsim.niz_izlaza[brojac] = izlaz
    
def postavi_pocetne_izlaze(opsim:OpcijeSimulacije):
    opsim.matrica_izlaza = {} #inicjalizovana matrica izlaza
    opsim.matrica_izlaza["0"] = [] #prazan niz pocetnih izlaza
    opsim.niz_izlaza = {} #pocetni niz izlaza za jednu vremensku jedinicu
    #inicijalizacija niza na 0, kako ne bi bacao exeption
    for i in range(1, opsim.br_blokova+1):
        opsim.niz_izlaza[i]=0.0 

    #inicijalizacije vektora X Y Z
    opsim.vektorX = {}
    opsim.vektorY = {}
    opsim.vektorZ = {}
    for i in range(1, opsim.br_integratora+1):
        opsim.vektorX[i] = 0.0
        opsim.vektorY[i] = 0.0
        opsim.vektorZ[i] = 0.0

    niz_blokova = opsim.niz_sortiran
    for blok in niz_blokova.values():
        if blok==None:continue
        p1 = blok.par1
        p2 = blok.par2
        p3 = blok.par3

        #u pomu{N} se upisuje vrednost izlaza za rbr blok ulaza
        pomu1 = opsim.niz_obradjen[blok.rb_bloka].ulaz1
        u1 = 0.0 if pomu1 == 0 else opsim.niz_izlaza[pomu1]
        pomu2 = opsim.niz_obradjen[blok.rb_bloka].ulaz2
        u2 = 0.0 if pomu2 == 0 else opsim.niz_izlaza[pomu2]
        pomu3 = opsim.niz_obradjen[blok.rb_bloka].ulaz3
        u3 = 0.0 if pomu3 == 0 else opsim.niz_izlaza[pomu3]
        izlaz = 0

        match blok.sifra_bloka:
            #sve funkcije koje traze izlaz nekog drugog bloka kao svoj ulaz, koriste funkciju vrati_blok() 
            # u okviru fje se dobija konkretan blok sa njegovim parametrima, pa je moguce dobiti njegov konkretan izlaz 
            case 1: izlaz=arkusTanges(p1, p2,p3,u1)
            case 2: izlaz=signum(u1)
            case 3: izlaz=kosinus(p1, p2, p3,u1)
            case 4: izlaz=mrtvaZona(p1, p2, u1)
            case 5: izlaz=delitelj(u1, u2)
            case 6: izlaz=eksponent(p1, p2, p3, u1)
            case 7: izlaz=generatorFja(p1, p2, p3, u1)
            case 8: izlaz=pojacanje(p1, u1)
            case 9: izlaz=kvadratniKoren(u1)
            case 10: 
                izlaz=p1
                integrator(p2,p3,u1,u2,u3,opsim,blok.rb_integratora)
            case 11: izlaz=generatorSlucajnihBrojeva()
            case 12: izlaz=p1
            case 13: izlaz=ogranicavac(p1, p2, u1)
            case 14: izlaz=apsolutnavrednost(u1)
            case 15: izlaz=invertor(u1)
            case 16: izlaz=negativniOgranicavac(u1)
            case 17: izlaz=offset(p1, u1)
            case 18: izlaz=pozitivniOgranicavac(u1)
            case 19: izlaz=krajSimulacije(u1, u2)
            case 20: izlaz=relej(u1, u2, u3)
            case 21: izlaz=sinus(p1, p2, p3, u1)
            case 22: izlaz=generatorImpulsa(p1. u1)
            case 23: izlaz=jedinicnoKasnjenje(p1, p2, u1) #pogledati validnost potpisa ove funkcije
            case 24: izlaz=vacuous(blok) #proveriti
            case 25: izlaz=opsim.trenutno_vreme
            case 26: izlaz=sabirac(p1, p2, p3,u1, u2, u3 )
            case 27: izlaz=mnozac(u1, u2)
            case 28: izlaz=wye(p1, p2, u1, u2, blok, blok ) #proveriti
            case 0: izlaz=kolozadrske(p1, p2, u1, u2)
        upisi_izlaz(opsim, blok.rb_bloka, izlaz)       

def racunaj(opcije:OpcijeSimulacije):
    '''
    funkcija u kojoj treba da se desi svo racunanje i integracija
    '''
    slog ={
        "k1":0,
        "k2":0,
        "k3":0
    }
    opcije.vektorX = [0 for i in range(opcije.br_integratora+1)]
    opcije.vektorY = [0 for i in range(opcije.br_integratora+1)]
    opcije.vektorZ = [0 for i in range(opcije.br_integratora+1)]
    opcije.nizK = [copy(slog) for i in range(opcije.br_integratora+1)]
    opcije.pola_intervala_integracije = opcije.interval_integracije/2

    postavi_pocetne_izlaze(opcije)
    print("----------------Pocetni izlazi-------------------")
    print(*opcije.niz_sortiran,sep="\n")

    for i in range(opcije.br_integratora):
        poma = opcije.niz_rb_integratora[i]
        opcije.vektorY[i] = opcije.niz_obradjen[poma-1].par1
    
    opcije.trenutno_vreme = 0.0

    pomep = (opcije.pola_intervala_integracije)/(opcije.interval_stampanja*2)
    #vrsta prekida
    #brtacstampe
    pola_intervala(opcije)
    pass

def pola_intervala(opsim:OpcijeSimulacije):
    #prepisivanje vektorY u niz_izlaza
    for i in range(opsim.br_integratora):
        pombr = opsim.niz_rb_integratora[i]
        opsim.niz_izlaza[pombr] = opsim.vektorY[pombr]
    #brojac za sledeci blok u sortiranom nizu
    sledeciBlok = opsim.br_konstanti
    izracunaj(sledeciBlok, opsim)

def izracunaj(sledeciBlok, opsim:OpcijeSimulacije):
    blok = opsim.niz_sortiran[sledeciBlok]
    brojac = sledeciBlok
    p1 = blok.par1
    p2 = blok.par2
    p3 = blok.par3

    #u pomu{N} se upisuje vrednost izlaza za rbr blok ulaza
    pomu1 = opsim.niz_obradjen[blok.rb_bloka-1].ulaz1
    u1 = 0.0 if pomu1 == 0 else opsim.niz_izlaza[blok.rb_bloka-1]
    pomu2 = opsim.niz_obradjen[blok.rb_bloka-1].ulaz2
    u2 = 0.0 if pomu2 == 0 else opsim.niz_izlaza[blok.rb_bloka-1]
    pomu3 = opsim.niz_obradjen[blok.rb_bloka-1].ulaz3
    u3 = 0.0 if pomu3 == 0 else opsim.niz_izlaza[blok.rb_bloka-1]

    match blok.sifra_bloka:
            #sve funkcije koje traze izlaz nekog drugog bloka kao svoj ulaz, koriste funkciju vrati_blok() 
            # u okviru fje se dobija konkretan blok sa njegovim parametrima, pa je moguce dobiti njegov konkretan izlaz 
            case 1: izlaz=arkusTanges(p1,p2,p3,u1,u2,u3,brojac,opsim)
            case 2: izlaz= signum(u1,brojac,opsim)
            case 3: izlaz= kosinus(p1,p2,p3,u1,brojac,opsim)
            case 4: izlaz= mrtvaZona(p1,p2,u1,brojac, opsim)
            case 5: izlaz= delitelj(u1,u2,brojac,opsim)
            case 6: izlaz= eksponent(p1,p2,p3,u1,brojac,opsim)
            case 7: izlaz= generatorFja(p1,p2,p3,u1,brojac,opsim)
            case 8: izlaz= pojacanje(p1,u1,brojac,opsim)
            case 9: izlaz= kvadratniKoren(u1, brojac,opsim)
            case 10: izlaz=integrator(p2,p3,u1,u2,u3,brojac,opsim)
            case 11: izlaz= generatorSlucajnihBrojeva(brojac)
            case 12:  p1
            case 13: izlaz= ogranicavac(p1,p2,u1,brojac,opsim)
            case 14: izlaz= apsolutnavrednost(u1,brojac,opsim)
            case 15: izlaz= invertor(u1,brojac,opsim)
            case 16: izlaz= negativniOgranicavac(u1, brojac, opsim)
            case 17: izlaz= offset(p1,u1,brojac,opsim)
            case 18: izlaz= pozitivniOgranicavac(u1,brojac,opsim)
            case 19: izlaz= krajSimulacije(u1,u2,brojac,opsim)
            case 20: izlaz= relej(u1,u2,u3,brojac,opsim)
            case 21: izlaz= sinus(p1,p2,p3,u1,brojac,opsim)
            case 22: izlaz= generatorImpulsa(p1,u1, brojac, opsim)
            case 23: izlaz=jedinicnoKasnjenje(p1,p2,u1,brojac,opsim) #pogledati validnost potpisa ove funkcije
            case 24: izlaz= vacuous(sledeciBlok) #proveriti
            case 25: izlaz= opsim.trenutno_vreme
            case 26: izlaz= sabirac(p1,p2,p3,u1,u2,u3,brojac,opsim)
            case 27: izlaz= mnozac(u1,u2,brojac,opsim)
            case 28: izlaz= wye(p1,p2,u1,u2,pomu1,sledeciBlok,brojac,opsim) #proveriti
            case 0: izlaz= kolozadrske(p1,p2,u1,u2,brojac,opsim)
    pass
