from typing import List
from opcije_simulacije import OpcijeSimulacije
from csmp_blok import CSMPBlok, from_dict_to_dataclass
from math import sqrt, sin, cos, atan, exp, floor, ceil
from random import randint
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from scipy.integrate import solve_ivp
import json, csv
from copy import copy


class Simulator():

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

    @classmethod
    def podesi_sifru(cls):
        '''
        realizacija ove metode zavisi od nacina prosledjivanja tabele konfiguracije
        ako je u tabeli tip podesen kako sifra onda je metoda suvisna
        ako je u tabeli tip podesen kao karakter potrebno je deifnisati metodu
        tako da zavisno od tipa (cija lista postoji gore) kreira sifru
        ''' 
        pass

     
    @classmethod
    def sabirac(cls,p1,p2,p3,u1,u2,u3,brojac):
        # print("usao u sabirac")

        izlaz = p1*u1+p2*u2+p3*u3
    
    @classmethod
    def mnozac(cls,u1,u2,brojac):
        # print("usao u mnozac")

        izlaz=u1*u2
    
    @classmethod
    def apsolutnavrednost(cls,u1,brojac):
        izlaz=abs(u1)
    
    @classmethod
    def delitelj(cls,u1,u2,brojac):
        # print("usao u delitelj")
        izlaz=u1/u2

    @classmethod
    def invertor(cls,u1,brojac):
        izlaz=-u1
    
    @classmethod
    def kvadratniKoren(cls,u1,brojac):
        izlaz=sqrt(u1)
   
    @classmethod
    def offset(cls,p1,u1,brojac):
        izlaz=p1+u1

    @classmethod
    def pojacanje(cls,p1,u1,brojac):
        izlaz=p1*u1

    @classmethod
    def relej(cls,u1,u2,u3,brojac):
        if u1<0:
            izlaz=u3
        else:
            izlaz=u2

    @classmethod
    def signum(cls,u1,brojac):
        izlaz = None
        if u1<0:
            izlaz = -1
        elif u1>0:
            izlaz=1
        elif u1==0:
            izlaz=0
    
    @classmethod
    def sinus(cls,p1,p2,p3,u1,brojac):
        izlaz=p1*sin(p2*u1 + p3)
    
    @classmethod
    def kosinus(cls,p1,p2,p3,u1,brojac):
        # print("usao u kosinus")

        izlaz=p1*cos(p2*u1+p3)
    
    @classmethod
    def arkusTanges(cls,p1,p2,p3,u1,brojac):

        izlaz=p1*atan(p2*u1+p3)

    @classmethod
    def eksponent(cls,p1,p2,p3,u1,brojac):
        izlaz=p1*exp(p2*u1+p3)
        
    @classmethod
    def mrtvaZona(cls,p1,p2,u1,brojac):
        #p1 donja granica, p2 gornja granica
        if u1>p1 and u1<p2:
            izlaz=0
        else:
            izlaz= u1
    
    @classmethod
    def generatorSlucajnihBrojeva(cls, brojac):
        izlaz = randint(1,99999)

    @classmethod
    def ogranicavac(cls,p1,p2,u1,brojac):
        #p1 donja granica, p2 gornja granica
        if u1<p1:
            izlaz=p1
        else:
            if u1>p2:
                izlaz=p2
            else:
                izlaz=u1
    
    @classmethod
    def negativniOgranicavac(cls,u1,brojac):
        if u1<0:
            izlaz=0
        else:
            izlaz=u1
    
    @classmethod
    def pozitivniOgranicavac(cls,u1,brojac):
        if u1>0:
            izlaz= 0
        else:
            izlaz=u1
    
    # @classmethod
    # def generatorFja(cls,p1,p2,p3,u1,brojac):
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
            
    @classmethod
    def generatorImpulsa(cls,p1,u1,brojac):
        izlaz = 1 if u1>0 else 0

    # @classmethod
    # def jedinicnoKasnjenje(cls,p1,p2,u1,brojac):
        
    #     if self.VrstaPrekida['tip'] == "NemaRac":
    #         izlaz=p1
    #     else:
    #         izlaz=p2
    #     self.ObradjenNiz[brojac]['parII'] = u1

    @classmethod
    def integrator(cls,p2,p3,u1,u2,u3):
        # print("usao u integrator")
        izlaz = u1+p2*u2+p3*u3
        return izlaz
        
        
    
    # @classmethod
    # def kolozadrske(cls,p1,p2,u1,u2,brojac):
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
    
    # @classmethod
    # def krajSimulacije(cls,u1,u2,brojac):
    #     if u2<u1:
    #         self.VrstaPrekida['tip'] = "KrajQuit"
    #         self.VrstaPrekida['poruka'] = "Kraj simulacije od strane Quit elementa."
    
    # @classmethod
    # def vacuous(cls,sledeciblok, brojac):
    #     if self.VrstaPrekida['tip'] == "NemaRac":
    #         self.ObradjenNiz[brojac]["rbIntegratora"] = sledeciblok
    
    # @classmethod
    # def wye(cls,p1,p2,u1,u2,brojac,pomUl1,sledeciBlok):
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

    @classmethod
    def izracunaj_izlaz(cls):
        pass

    @classmethod
    def ucitaj_blokove(cls, opsim:OpcijeSimulacije):
        lista_dict = []
        with open(opsim.tabela_konfiguracije, mode='r') as csv_file:
            reader = csv.DictReader(csv_file,delimiter=',',quotechar='|')
            for row in reader:
                red = {
                    'ulaz1':int(row["u1"]),
                    'ulaz2':int(row["u2"]),
                    'ulaz3':int(row["u3"]),
                    'par1':int(row["p1"]),
                    'par2':int(row["p2"]),
                    'par3':int(row["p3"]),
                    'sortiran':False,
                    'tip':row["tip"],
                    'rb_bloka':int(row["rbr"]),
                    'rb_integratora':-1,
                    'sifra_bloka': Simulator.sifre[str(row["tip"])]
                }
                lista_dict.append(red)
        
        with open("test.json", 'w') as outfile:
            json.dump(lista_dict,outfile )
        opsim.niz_blokova = lista_dict
        # return lista_dict

    @classmethod
    def kreiraj_blokove(cls, opsim:OpcijeSimulacije):
        lista_blokova=[]
        for el in opsim.niz_blokova:
            csmpblk = from_dict_to_dataclass(CSMPBlok, el)
            lista_blokova.append(csmpblk)
        opsim.niz_blokova = lista_blokova
        # return lista_blokova
    
    @classmethod
    def vrati_blok(cls, lista:list[CSMPBlok], rbr):
        for el in lista:
            if el.rb_bloka==0:
                return None
            elif el.rb_bloka==rbr:
                return el
    
    @classmethod
    def obradi_niz_blokova(cls, opsim:OpcijeSimulacije):
        obradjen_niz = copy(opsim.niz_blokova)
        for blok in obradjen_niz:
            if blok.sifra_bloka != 10:
                blok.rb_integratora = 0
            elif blok.sifra_bloka==10:
                u1_blok = Simulator.vrati_blok(obradjen_niz, blok.ulaz1)
                u2_blok = Simulator.vrati_blok(obradjen_niz, blok.ulaz2)
                u3_blok = Simulator.vrati_blok(obradjen_niz, blok.ulaz3)
                if (u1_blok!=None and u1_blok.sifra_bloka==10) or (u2_blok!=None and u2_blok.sifra_bloka==10) or (u3_blok!=None and u3_blok.sifra_bloka==10):
                    blok.rb_integratora=2
                else:
                    blok.rb_integratora=1
        opsim.niz_obradjen = obradjen_niz


    @classmethod
    def racunaj(cls):
        v0 = 0
        t = np.linspace(0,10,num=100)

        sol_m2 = solve_ivp(Simulator.integrator, t_span=(0,max(t)), y0=[v0], t_eval=t, method="RK45", args=(0,0,10,0,0))
        
        v_sol_m2 = sol_m2.y[0]

        plt.plot(t, v_sol_m2)
        plt.ylabel('$v(t)$', fontsize=22)
        plt.xlabel('$t$', fontsize=22)
        plt.show()
    