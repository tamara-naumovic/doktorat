from timeit import repeat
from opcije_simulacije import OpcijeSimulacije
from csmp_blok import CSMPBlok, from_dict_to_dataclass
from math import sqrt, sin, cos, atan, exp, copysign, trunc
from random import uniform
import urllib.request
import json, csv
import decimal
from copy import copy

dec_zero = decimal.Decimal('0.00')

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
    "Z": 0, #KoloZadrske,
    "uiot":29,
    "oiot":30
}
    
def podesi_sifru():
    '''
    realizacija ove metode zavisi od nacina prosledjivanja tabele konfiguracije
    ako je u tabeli tip podesen kao sifra onda je metoda suvisna
    ako je u tabeli tip podesen kao karakter potrebno je deifnisati metodu
    tako da zavisno od tipa (cija lista postoji gore) kreira sifru
    '''
    pass

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
    if u1>=0:
        izlaz=sqrt(u1)
        return izlaz
    else:
        return False

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
    izlaz=p1*decimal.Decimal(str(sin(p2*u1 + p3)))
    return izlaz

def kosinus(p1,p2,p3,u1):
    izlaz=p1*cos(p2*u1+p3)
    return izlaz

def arkusTanges(p1,p2,p3,u1, opcije):
    if (p2*u1+p3)>=0.0:
        izlaz=p1*atan(p2*u1+p3)
        return izlaz
    else:
        opcije.vrsta_prekida = {"tip": opcije.faza_rada[4], "poruka":"Vrednost za ArcTan je negativna!"}
        return False

def eksponent(p1,p2,p3,u1):
    izlaz=p1*exp(p2*u1+p3)
    return izlaz

def mrtvaZona(p1,p2,u1):
    #p1 donja granica, p2 gornja granica
    izlaz=0 if p1<u1<p2 else u1
    return izlaz

def generatorSlucajnihBrojeva():
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
#integratoru treba opcije jer upisuje u vektorY
def integrator(p2:decimal.Decimal,p3:decimal.Decimal,u1:decimal.Decimal,u2:decimal.Decimal,u3:decimal.Decimal, opcije:OpcijeSimulacije, rbInteg):
    opcije.vektorX[rbInteg] = u1+p2*u2+p3*u3

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
def jedinicnoKasnjenje(u1, opcije:OpcijeSimulacije):
    #izlaz iz bloka je izlaz u1 za vreme t-dt/2
    rbr_ulaznog_bloka = u1
    izlaz = 0
    if opcije.trenutno_vreme!=dec_zero:
        vreme = opcije.trenutno_vreme-opcije.pola_intervala_integracije
        izlaz = opcije.matrica_izlaza[str(vreme)][rbr_ulaznog_bloka]
    return izlaz
    

def kolozadrske(u1,u2):
    if u2>0:
        return u1
    else:
        return 0

def krajSimulacije(u1,u2, opcije:OpcijeSimulacije):
    if (u2<u1):
        opcije.vrsta_prekida = {"tip": opcije.faza_rada[3], "poruka":"Kraj simulacije od strane Quit elementa."}
        return True
    else:
        return False
    
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

def oiot(p1,p2,p3,u1):
    url = f'{p1}?{p2}={u1}'
    webUrl = urllib.request.urlopen(url)
    data_json = json.loads(webUrl.read().decode('utf-8'))
    if p3 in data_json:
        izlaz = data_json[p3]
        return izlaz
    else:
        return 0

def uiot(p1,p2):
    # uiot je iot blok  ulaznog tipa
    # to znači da ima daje input u simulaciju
    # p1 - api link
    # p2 - api data key
    
    webUrl = urllib.request.urlopen(p1)
    data_json = json.loads(webUrl.read().decode('utf-8'))
    while data_json.get('error'):
        webUrl = urllib.request.urlopen(p1)
        data_json = json.loads(webUrl.read().decode('utf-8'))
    izlaz = data_json[p2]
    return izlaz


def incijalizuj_sve(opcije:OpcijeSimulacije, brElemenata):
    #inicijalizacija niz_blokova, niz_obradjen, niz_sortiran
    decimal.getcontext().prec = opcije.preciznost

    opcije.niz_blokova = {}
    opcije.niz_obradjen = {}
    opcije.niz_sortiran = {}
    for i in range(brElemenata):
        if i ==0:
            opcije.niz_blokova[i] = None
            opcije.niz_obradjen[i] = None
            opcije.niz_sortiran[i] = None
        opcije.niz_blokova[i+1] = []
        opcije.niz_obradjen[i+1] = []
        opcije.niz_sortiran[i+1] = []
    #postavljen br_blokovana na brElemenata
    opcije.br_blokova = brElemenata
    #inicijalizacija matrice izlaza
    opcije.matrica_izlaza = {}
    #inicijalizacija niza izlaza
    opcije.niz_izlaza = {}
    for i in range(1, opcije.br_blokova+1):
        opcije.niz_izlaza[i]=dec_zero
    #inicijalizacije vektora X Y Z
    opcije.vektorX = {}
    opcije.vektorY = {}
    opcije.vektorZ = {}
    for i in range(1, opcije.br_integratora+1):
        opcije.vektorX[i] = decimal.Decimal('0')
        opcije.vektorY[i] = decimal.Decimal('0')
        opcije.vektorZ[i] = decimal.Decimal('0')
    opcije.nizK = {}
    opcije.faza_rada = {
        0: "nemarac",
        1: "prvapol",
        2: "drugapol",
        3: "quit",
        4: "greska",
    }
    opcije.vrsta_prekida = {"tip":-1, "poruka":"Nema greske"}
    

def ucitaj_blokove( opcije:OpcijeSimulacije):
    '''
    funkcija koja ucitava blokove iz tabele konfiguracije koja je zapamcena u OpcijeSimulacije
    i kreira CSMP blokove u formatu recnika koje pamti u opcije.niz_blokova.
    opcije.niz_blokova se dalje koristi za obradu
    '''
    lista_dict = []
    with open(opcije.tabela_konfiguracije, mode='r') as csv_file:
        reader = csv.DictReader(csv_file,delimiter=',',quotechar='|')
        for row in reader:
            if row["tip"]=="uiot" or row["tip"]=="oiot":
               p1 =  row["p1"]
               p2 =  row["p2"]
               p3 =  row["p3"]
            else:
                p1 =  decimal.Decimal(row["p1"])
                p2 =  decimal.Decimal(row["p2"])
                p3 =  decimal.Decimal(row["p3"])

            red = {
                'ulaz1':int(row["u1"]),
                'ulaz2':int(row["u2"]),
                'ulaz3':int(row["u3"]),
                'par1':p1,
                'par2':p2,
                'par3':p3,
                'sortiran':False,
                'tip':row["tip"],
                'rb_bloka':int(row["rbr"]),
                'rb_integratora':-1,
                'sifra_bloka': sifre[str(row["tip"])]
            }
            lista_dict.append(red)

    #inicijalizacija 
    incijalizuj_sve(opcije, len(lista_dict))

    for element in lista_dict:
        csmpblok = from_dict_to_dataclass(CSMPBlok,element)
        opcije.niz_blokova[csmpblok.rb_bloka] = csmpblok
    # return lista_dict

def obradi_niz_blokova(opcije:OpcijeSimulacije):
    '''
    funkcija obradjuje opcije.niz_blokova i kreira opcije.niz_obradjen
    prilikom obrade inicijalni parametri bloka vezani za redni broj integratora (-1) se menjaju
    u zavisnosti od toga da li je blok integrator ili ne
    takodje upisuje se opcije.br_integratora na broj integrator blokova
    '''
    obradjen_niz = copy(opcije.niz_blokova)
    opcije.br_integratora = len([obradjen_niz[i] for i in range(1,len(obradjen_niz)) if obradjen_niz[i].sifra_bloka==10])
    opcije.niz_rb_integratora = {}
    brInteg =0
    for i in range(1,opcije.br_integratora+1):
        opcije.niz_rb_integratora[i] = -1 #nije postavljen rbBloka ako je -1 | treba za svaki element u niz_rb_integratora da postoji rbBloka odgovarajuceg bloka
    for blok in obradjen_niz.values():
        if blok==None:
            continue
        if blok.sifra_bloka != 10:
            blok.rb_integratora = 0
        elif blok.sifra_bloka==10: #ako je blok integrator
            brInteg+=1
            blok.rb_integratora = brInteg
            opcije.niz_rb_integratora[brInteg]=blok.rb_bloka

            # u1_blok = obradjen_niz[blok.ulaz1]
            # u2_blok = obradjen_niz[blok.ulaz2]
            # u3_blok = obradjen_niz[blok.ulaz3]
            # if (u1_blok!=None and u1_blok.sifra_bloka==10) or (u2_blok!=None and u2_blok.sifra_bloka==10) or (u3_blok!=None and u3_blok.sifra_bloka==10):
            #     blok.rb_integratora=2
            #     opcije.niz_rb_integratora[blok.rb_integratora]=blok.rb_bloka
            #     #niz_rb_integratora treba da pamti redne brojeve blokova koji su integratori
            # else:
            #     blok.rb_integratora=1
            #     opcije.niz_rb_integratora[blok.rb_integratora]=blok.rb_bloka
    opcije.niz_obradjen = obradjen_niz

def sortiraj_niz(opcije: OpcijeSimulacije):
    '''
    funkcija sortira blokove po zadatom algoritmu, tako da blokovi ciji su ulazi poznati stoje na pocetku
    '''
    br_sortiranih = 0

    #postavljanje konstanti na prvo mesto 
    for blok in opcije.niz_obradjen.values():
        if blok==None:
            continue
        if blok.rb_bloka != 0 and blok.sifra_bloka == sifre["K"]:
            br_sortiranih += 1
            opcije.niz_sortiran[br_sortiranih]= blok
            blok.sortiran = True
    while True:
        i = 1
        ponovo = False
        while i <= opcije.br_blokova and not ponovo:
            if not opcije.niz_obradjen[i].sortiran and opcije.niz_obradjen[i].rb_bloka!=0:
                ulaz1 = opcije.niz_obradjen[i].ulaz1
                ulaz2 = opcije.niz_obradjen[i].ulaz2
                ulaz3 = opcije.niz_obradjen[i].ulaz3
                #kao ulaz se dobije redni br bloka, redni brojevi pocinju od 1 ili nula ako ne postoji
                
                uslov1 = ulaz1 == 0 or opcije.niz_obradjen[ulaz1].sifra_bloka not in [sifre["I"], sifre["U"]] or opcije.niz_obradjen[ulaz1].sortiran  
                uslov2 = ulaz3 == 0 or opcije.niz_obradjen[ulaz2].sifra_bloka not in [sifre["I"], sifre["U"]] or opcije.niz_obradjen[ulaz2].sortiran 
                uslov3 = ulaz3 == 0 or opcije.niz_obradjen[ulaz3].sifra_bloka not in [sifre["I"], sifre["U"]] or opcije.niz_obradjen[ulaz3].sortiran 
                
                if uslov1 and uslov2 and uslov3:
                    ponovo = True
                    br_sortiranih += 1
                    opcije.niz_sortiran[br_sortiranih]=opcije.niz_obradjen[i]
                    opcije.niz_obradjen[i].sortiran = True
                else:
                    ponovo = False
            if not ponovo:
                i += 1
        if br_sortiranih==opcije.br_blokova:
                    break
            

def upisi_izlaz(opcije: OpcijeSimulacije, brojac, izlaz:decimal.Decimal):
    opcije.niz_izlaza[brojac] = izlaz
    
def postavi_pocetne_izlaze(opcije:OpcijeSimulacije):
    niz_blokova = opcije.niz_sortiran
    for blok in niz_blokova.values():
        if blok==None:continue

        p1 = blok.par1
        p2 = blok.par2
        p3 = blok.par3

        #u pomu{N} se upisuje vrednost izlaza za rbr blok ulaza
        pomu1 = opcije.niz_obradjen[blok.rb_bloka].ulaz1
        u1 = dec_zero if pomu1 == 0 else opcije.niz_izlaza[pomu1]
        pomu2 = opcije.niz_obradjen[blok.rb_bloka].ulaz2
        u2 = dec_zero if pomu2 == 0 else opcije.niz_izlaza[pomu2]
        pomu3 = opcije.niz_obradjen[blok.rb_bloka].ulaz3
        u3 = dec_zero if pomu3 == 0 else opcije.niz_izlaza[pomu3]
        izlaz = dec_zero

        match blok.sifra_bloka:
            #sve funkcije koje traze izlaz nekog drugog bloka kao svoj ulaz, koriste funkciju vrati_blok() 
            # u okviru fje se dobija konkretan blok sa njegovim parametrima, pa je moguce dobiti njegov konkretan izlaz 
            case 1:izlaz=arkusTanges(p1, p2,p3,u1, opcije)
            case 2: izlaz=signum(u1)
            case 3: izlaz=kosinus(p1, p2, p3,u1)
            case 4: izlaz=mrtvaZona(p1, p2, u1)
            case 5: 
                izlaz=delitelj(u1, u2)
                if izlaz==False:
                    opcije.vrsta_prekida = {"tip": opcije.faza_rada[4], "poruka":"Drugi ulaz u delitelj je 0!"}

            case 6: izlaz=eksponent(p1, p2, p3, u1)
            case 7: izlaz=generatorFja(p1, p2, p3, u1)
            case 8: izlaz=pojacanje(p1, u1)
            case 9: 
                izlaz=kvadratniKoren(u1)
                if izlaz==False:
                    opcije.vrsta_prekida = {"tip": opcije.faza_rada[4], "poruka":"Ulaz u kvadratni koren je negativan!"}

            case 10: 
                izlaz=p1
                integrator(p2,p3,u1,u2,u3,opcije,blok.rb_integratora)
            case 11: izlaz=generatorSlucajnihBrojeva()
            case 12: izlaz=p1
            case 13: izlaz=ogranicavac(p1, p2, u1)
            case 14: izlaz=apsolutnavrednost(u1)
            case 15: izlaz=invertor(u1)
            case 16: izlaz=negativniOgranicavac(u1)
            case 17: izlaz=offset(p1, u1)
            case 18: izlaz=pozitivniOgranicavac(u1)
            case 19: izlaz=krajSimulacije(u1, u2, opcije)
            case 20: izlaz=relej(u1, u2, u3)
            case 21: izlaz=sinus(p1, p2, p3, u1)
            case 22: izlaz=generatorImpulsa(p1. u1)
            case 23: 
                izlaz=0
                # jedinicnoKasnjenje(p1, p2, u1) 
            case 24: izlaz=vacuous(blok) #proveriti
            case 25: izlaz=opcije.trenutno_vreme
            case 26: izlaz=sabirac(p1, p2, p3,u1, u2, u3 )
            case 27: izlaz=mnozac(u1, u2)
            case 28: izlaz=wye(p1, p2, u1, u2, blok, blok ) #proveriti
            case 29: izlaz=uiot(p1, p2)
            case 30: izlaz=oiot(p1, p2, p3, u1)
            case 0: izlaz=kolozadrske(p1, p2, u1, u2) #proveriti
        upisi_izlaz(opcije, blok.rb_bloka, decimal.Decimal(str(izlaz)))

def racunaj(opcije:OpcijeSimulacije):
    '''
    funkcija u kojoj treba da se desi svo racunanje i integracija
    '''
    slog ={
        "k1":decimal.Decimal('0'),
        "k2":decimal.Decimal('0'),
        "k3":decimal.Decimal('0')
    }
    for i in range(1, opcije.br_integratora+1):
        opcije.nizK[i] = copy(slog)
    opcije.pola_intervala_integracije = opcije.interval_integracije/decimal.Decimal('2')
    opcije.trenutno_vreme = dec_zero
    #zaokruzivanje vremena na broj decimala intervala integracije
    if opcije.trenutno_vreme == 0.0:
        postavi_pocetne_izlaze(opcije)
        print("----------------Pocetni izlazi-------------------")
        print(opcije.niz_izlaza,sep="\n")
        opcije.matrica_izlaza[str(opcije.trenutno_vreme)]= (copy(opcije.niz_izlaza))
        print(f"Prva matrica:{opcije.matrica_izlaza} ")

    for i in range(1,opcije.br_integratora+1):
        poma = opcije.niz_rb_integratora[i]
        opcije.vektorY[i] = opcije.niz_obradjen[poma].par1
    

    pomep = (opcije.pola_intervala_integracije)/(opcije.interval_stampanja*2)
    opcije.vrsta_prekida={"tip":opcije.faza_rada[0],"poruka":"Nema rac"}
    #brtacstampe
    brTacStampe = trunc(opcije.trenutno_vreme/opcije.interval_stampanja +1)
    pola_intervala(opcije)
    # { kraj racuna f(Xn,Yn) }
    opcije.matrica_izlaza[str(opcije.trenutno_vreme)]= opcije.niz_izlaza
    while True:
        opcije.vrsta_prekida={"tip":opcije.faza_rada[1],"poruka":"Prva Pol"}

        for pomprom in range(1, opcije.br_integratora+1):
            
            opcije.vektorZ[pomprom] = opcije.vektorY[pomprom]
            # print(opcije.nizK[pomprom]["k1"])
            opcije.nizK[pomprom]["k1"] =opcije.interval_integracije*opcije.vektorX[pomprom]
            opcije.vektorY[pomprom] = opcije.vektorZ[pomprom] + decimal.Decimal('0.5')*opcije.nizK[pomprom]["k1"]
        
        opcije.trenutno_vreme += opcije.pola_intervala_integracije
        pola_intervala(opcije)
        opcije.matrica_izlaza[str(opcije.trenutno_vreme)]= copy(opcije.niz_izlaza)
        #kraj racuna f(Xn+1/2*h, Yn+1/2*k1)
        
        #DRUGA POLOVINA intervala: racuna se f(Xn+1/2*h, Yn+1/2*k2)
        opcije.vrsta_prekida={"tip":opcije.faza_rada[2],"poruka":"Druga Pol"}
        
        for pomprom in range(1, opcije.br_integratora+1):
            opcije.nizK[pomprom]["k2"] = opcije.interval_integracije*opcije.vektorX[pomprom]
            opcije.vektorY[pomprom] = opcije.vektorZ[pomprom] + decimal.Decimal('0.5')*opcije.nizK[pomprom]["k2"]

        pola_intervala(opcije)
        #kraj racuna f(Xn+1/2*h, Yn+1/2*k2)
        # print(f"Trenutno vreme> {opcije.trenutno_vreme}")
        # opcije.matrica_izlaza[str(opcije.trenutno_vreme)]= copy(opcije.niz_izlaza)

        #racuna se f(Xn+h, Yn+k3)
        for pomprom in range(1, opcije.br_integratora+1):
            opcije.nizK[pomprom]["k3"] = opcije.interval_integracije*opcije.vektorX[pomprom]
            opcije.vektorY[pomprom] = opcije.vektorZ[pomprom] + opcije.nizK[pomprom]["k3"]

        opcije.trenutno_vreme += opcije.pola_intervala_integracije
        pola_intervala(opcije)
        #kraj racuna f(Xn+h, Yn+k3)

        for pomprom in range(1, opcije.br_integratora+1):
            opcije.vektorY[pomprom] = opcije.vektorZ[pomprom]+(opcije.nizK[pomprom]["k1"]+decimal.Decimal('2')*opcije.nizK[pomprom]["k2"]+decimal.Decimal('2')*opcije.nizK[pomprom]["k3"]+opcije.interval_integracije*opcije.vektorX[pomprom])/decimal.Decimal('6')

        pola_intervala(opcije)
        #{ kraj metode Runge-Kuta IV reda }
        # opcije.matrica_izlaza[str(opcije.trenutno_vreme)]= copy(opcije.niz_izlaza)
        # print(opcije.niz_izlaza)
        if(opcije.vrsta_prekida["tip"] in [opcije.faza_rada[3],opcije.faza_rada[4]]):
            print("-------------------Kraj----------------")
            print(f"Tip prekida: {opcije.vrsta_prekida['tip']}")   
            print(f"Poruka: {opcije.vrsta_prekida['poruka']}")   
            break
        else:
            pomp = round(opcije.trenutno_vreme/opcije.interval_stampanja + pomep)
            if(brTacStampe<=pomp):
                opcije.matrica_izlaza[str(opcije.trenutno_vreme)]= copy(opcije.niz_izlaza)
                brTacStampe=pomp+1
        if(opcije.trenutno_vreme>opcije.duzina_simulacije):
            print("Kraj simulacije u odnosu na vreme")
            print(f"Tip prekida: {opcije.vrsta_prekida['tip']}")   
            print(f"Poruka: {opcije.vrsta_prekida['poruka']}")   
            break

def pola_intervala(opcije:OpcijeSimulacije):
    #prepisivanje vektorY u niz_izlaza
    for i in range(1,opcije.br_integratora+1):
        pombr = opcije.niz_rb_integratora[i] #ovo mu vrati 3
        opcije.niz_izlaza[pombr] = opcije.vektorY[i]
    #brojac za sledeci blok u sortiranom nizu nakon konstanti
    sledeciBlok = opcije.br_konstanti+1
    izracunaj(sledeciBlok, opcije)


def izracunaj(sledeciBlok, opcije:OpcijeSimulacije):
    if(sledeciBlok>opcije.br_blokova):
        return
    
    blok = opcije.niz_sortiran[sledeciBlok]
    p1 = blok.par1
    p2 = blok.par2
    p3 = blok.par3

    #u pomu{N} se upisuje vrednost izlaza za rbr blok ulaza

    pomu1 = opcije.niz_obradjen[blok.rb_bloka].ulaz1
    u1 = dec_zero if pomu1 == 0 else opcije.niz_izlaza[pomu1]
    pomu2 = opcije.niz_obradjen[blok.rb_bloka].ulaz2
    u2 = dec_zero if pomu2 == 0 else opcije.niz_izlaza[pomu2]
    pomu3 = opcije.niz_obradjen[blok.rb_bloka].ulaz3
    u3 = dec_zero if pomu3 == 0 else opcije.niz_izlaza[pomu3]
    izlaz = dec_zero

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
        case 9: 
                izlaz=kvadratniKoren(u1)
                if izlaz==False:
                    opcije.vrsta_prekida = {"tip": opcije.faza_rada[4], "poruka":"Ulaz u kvadratni koren je negativan!"}

        case 10: 
            integrator(p2,p3,u1,u2,u3,opcije,blok.rb_integratora)
        case 11: izlaz=generatorSlucajnihBrojeva()
        case 12: izlaz=p1
        case 13: izlaz=ogranicavac(p1, p2, u1)
        case 14: izlaz=apsolutnavrednost(u1)
        case 15: izlaz=invertor(u1)
        case 16: izlaz=negativniOgranicavac(u1)
        case 17: izlaz=offset(p1, u1)
        case 18: izlaz=pozitivniOgranicavac(u1)
        case 19: izlaz=krajSimulacije(u1, u2, opcije)
        case 20: izlaz=relej(u1, u2, u3)
        case 21: izlaz=sinus(p1, p2, p3, u1)
        case 22: izlaz=generatorImpulsa(p1. u1)
        case 23: izlaz=jedinicnoKasnjenje(blok.ulaz1, opcije) 
        case 24: izlaz=vacuous(blok) #proveriti
        case 25: izlaz=opcije.trenutno_vreme
        case 26: izlaz=sabirac(p1, p2, p3,u1, u2, u3 )
        case 27: izlaz=mnozac(u1, u2)
        case 28: izlaz=wye(p1, p2, u1, u2, blok, blok ) #proveriti
        case 29: izlaz=uiot(p1, p2) 
        case 30: izlaz=oiot(p1, p2, p3, u1) 
        case 0: izlaz=kolozadrske(p1, p2, u1, u2) #proveriti
    if blok.sifra_bloka!=10:
        upisi_izlaz(opcije, blok.rb_bloka, decimal.Decimal(str(izlaz)))
    
    if(sledeciBlok<=opcije.br_blokova):
        sledeciBlok+=1
        izracunaj(sledeciBlok, opcije)
    else:
        print("Greska. Kraj?")
