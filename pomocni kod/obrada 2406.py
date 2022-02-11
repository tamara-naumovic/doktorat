import math, csv, random, json
import numpy as np


FazaRada = ["NemaRac", "PrvaPol", "DrugaPol", "GreskaObrade", "KrajQuit"]
tBlok = {
    'ulazI':-1,
    'ulazII':-1,
    'ulazIII':-1,
    'parI':-1.0,
    'parII':-1.0,
    'parIII':-1.0,
    'sortiran':False,
    'sifra':-1,
    'rbBloka':0,
    'rbIntegratora':-1,
    'tip':-1
}
#slog za Runge Kutta IV reda
IVslog={
    'k1':'',
    'k2':'',
    'k3':''
}

tNizK = [] #niz IVslog
arrayBlok = [] #niz blokova
arrayInt = [] #niz int
arrayReal = [] #niz real
matrixReal = [] #matrica realnih brojeva

tVrstaPrekida = {
    'tip':FazaRada[0],
    'poruka':'poruka o grešci'
}

class tSimulacija:
    OpcijeSimulacije = {
        'duzinaSimulacije':5,
        'intervalInteg':0.1,
        'intervalStampanja':0.1
    }
    SimulacijaOdradjena = False

    VektorX, VektorY, VektorZ= [], [], []
    ObradjenNiz = [] # PrevedenNiz sredjen u oblik pogodan za dalji rad
    SortiranNiz = [] # niz indeksa sortiranih blookova
    BrojBlokova = 0 # broj blokova u modelu
    BrojIntegratora = 0
    BrojSortiranih = 0
    NizRBIntegratora = [] # niz koji cuva redne brojeve integratora u obradjenom nizu
    BrKonst = 0 # broj konstanti u modelu
    IntervalInteg = 0.0
    PolaIntIntegracije = 0.0
    NizIzlaza = [] # niz u koji se pamti izlaz iz svakog bloka u svakom trenutku
    VrstaPrekida = tVrstaPrekida
    TekVremeSim = 0.0
    FunkGener = [] #matrica realnih brojeva 4x11, kojih realnih brojeva? nigde nije napravljena inicijalizacija
    TekIzlaz = ''
    NizZaStampu = []

    
    def podesiSifru(self,tip):
        # print("usao u podesiSifru")

        if(tip=='A'):
            return 1
        elif(tip=='B'):
            return 2
        elif(tip=='C'):
            return 3
        elif(tip=='D'):
            return 4
        elif(tip=='/'):
            return 5
        elif(tip=='E'):
            return 6
        elif(tip=='F'):
            return 7
        elif(tip=='G'):
            return 8
        elif(tip=='H'):
            return 9
        elif(tip=='I'):
            return 10
        elif(tip=='J'):
            return 11
        elif(tip=='K'):
            return 12
        elif(tip=='L'):
            return 13
        elif(tip=='M'):
            return 14
        elif(tip=='-'):
            return 15
        elif(tip=='M'):
            return 16
        elif(tip=='O'):
            return 17
        elif(tip=='P'):
            return 18
        elif(tip=='Q'):
            return 19
        elif(tip=='R'):
            return 20
        elif(tip=='S'):
            return 21
        elif(tip=='T'):
            return 22
        elif(tip=='U'):
            return 23
        elif(tip=='V'):
            return 24
        elif(tip=='-t>'):
            return 25
        elif(tip=='W'):
            return 26
        elif(tip=='X'):
            return 27
        elif(tip=='|'):
            return 28
        elif(tip=='Z'):
            return 0
        else:
            return None   
    
    def ucitajCSV(self, tabelaKonfiguracije):
        # print("usao u ucitajCSV")
        lista = []
        with open(tabelaKonfiguracije, mode='r') as csv_file:
            reader = csv.DictReader(csv_file,delimiter=',',quotechar='|')
            for row in reader:
                red = {
                    'ulazI':int(row["u1"]),
                    'ulazII':int(row["u2"]),
                    'ulazIII':int(row["u3"]),
                    'parI':int(row["p1"]),
                    'parII':int(row["p2"]),
                    'parIII':int(row["p3"]),
                    'sortiran':False,
                    'tip':row["tip"],
                    'rbBloka':int(row["rbr"]),
                    'rbIntegratora':-1,
                    'sifra': -1
                }
                lista.append(red)
        for item in lista:
            item['sifra']=self.podesiSifru(self,item['tip'])
        with open("test.json", 'w') as outfile:
            json.dump(lista,outfile )
        return lista    
    
    #jesmo
    @classmethod
    def izracunaj(self, sledeciBlok):
        
        Par1, Par2, Par3, Ulaz1, Ulaz2, Ulaz3=0,0,0,0,0,0
        PomUl1, PomUl2, PomUl3, Brojac = 0,0,0,0

        Brojac = self.SortiranNiz[sledeciBlok]

        Par1 = self.ObradjenNiz[Brojac]['parI']
        Par2 = self.ObradjenNiz[Brojac]['parII']
        Par3 = self.ObradjenNiz[Brojac]['parIII']

        
        fajl_izlaz= open("nizizlaza.txt",mode="a", newline="\r\n")
        fajl_izlaz.write(str(self.NizIzlaza))
        fajl_izlaz.write("\r\n")
        fajl_izlaz.close()  

        PomUl1 = self.ObradjenNiz[Brojac]['ulazI']

        if PomUl1==0:
            Ulaz1=0.0
        else:
            Ulaz1=self.NizIzlaza[PomUl1]
        
        f = open("terminal.txt", mode="a")
        f.write("usao u izracunaj")
        f.write("\r\n")
        f.write("brojac "+ str(Brojac))
        f.write("\r\n")
        f.write("pomu1 "+ str(PomUl1))
        f.write("\r\n")
        f.write("Ulaz1 "+ str(Ulaz1))
        f.write("\r\n")
        f.close()
        
        PomUl2 = self.ObradjenNiz[Brojac]['ulazII']
        if PomUl2==0:
            Ulaz2=0.0
        else:
            Ulaz2=self.NizIzlaza[PomUl2]

        PomUl3 = self.ObradjenNiz[Brojac]['ulazIII']
        if PomUl3==0:
            Ulaz3=0.0
        else:
            Ulaz3=self.NizIzlaza[PomUl3]
        f = open('rez.txt', 'a')
        rez ="rez: {},{},{},{},{} '\n'".format(Brojac,Par1,Par2,Par3,PomUl1)
        f.write(rez)
        f.close()
        if self.ObradjenNiz[Brojac]['sifra']==0:
            self.kolozadrske(Par1,Par2,Ulaz1,Ulaz2,Brojac)
        elif self.ObradjenNiz[Brojac]['sifra']==1:
            self.arkusTanges(Par1,Par2,Par3,Ulaz1,Brojac)
        elif self.ObradjenNiz[Brojac]['sifra']==2:
            self.signum(Ulaz1,Brojac)
        elif self.ObradjenNiz[Brojac]['sifra']==3:
            self.kosinus(Par1,Par2,Par3,Ulaz1,Brojac)
        elif self.ObradjenNiz[Brojac]['sifra']==4:
            self.mrtvaZona(Par1,Par2,Ulaz1,Brojac)
        elif self.ObradjenNiz[Brojac]['sifra']==5:
            self.delitelj(Ulaz1,Ulaz2,Brojac)
        elif self.ObradjenNiz[Brojac]['sifra']==6:
            self.eksponent(Par1,Par2,Par3,Ulaz1,Brojac)
        elif self.ObradjenNiz[Brojac]['sifra']==7:
            self.generatorFja(Par1,Par2,Par3,Ulaz1, Brojac)
        elif self.ObradjenNiz[Brojac]['sifra']==8:
            self.pojacanje(Par3,Ulaz1,Brojac)
        elif self.ObradjenNiz[Brojac]['sifra']==9:
            self.kvadratniKoren(Ulaz1,Brojac)
        elif self.ObradjenNiz[Brojac]['sifra']==10:
            f = open("terminal.txt", mode="a")
            f.write("usao u integrator sju ")
            f.write("\r\n")
            f.close()
            self.integrator(Par2,Par3,Ulaz1,Ulaz2,Ulaz3,Brojac)
        elif self.ObradjenNiz[Brojac]['sifra']==11:
            self.generatorSlucajnihBrojeva(Brojac)
        elif self.ObradjenNiz[Brojac]['sifra']==13:
            self.ogranicavac(Par1,Par2,Ulaz1,Brojac)
        elif self.ObradjenNiz[Brojac]['sifra']==14:
            self.apsolutnavrednost(Ulaz1,Brojac)
        elif self.ObradjenNiz[Brojac]['sifra']==15:
            self.invertor(Ulaz1,Brojac)
        elif self.ObradjenNiz[Brojac]['sifra']==16:
            self.negativniOgranicavac(Ulaz1,Brojac)
        elif self.ObradjenNiz[Brojac]['sifra']==17:
            self.offset(Par1,Ulaz1,Brojac)
        elif self.ObradjenNiz[Brojac]['sifra']==18:
            self.pozitivniOgranicavac(Ulaz1,Brojac)
        elif self.ObradjenNiz[Brojac]['sifra']==19:
            self.krajSimulacije(Ulaz1,Ulaz2,Brojac)
        elif self.ObradjenNiz[Brojac]['sifra']==20:
            self.relej(Ulaz1,Ulaz2,Ulaz3,Brojac)
        elif self.ObradjenNiz[Brojac]['sifra']==21:
            self.sinus(Par1,Par2,Par3,Ulaz2,Brojac)
        elif self.ObradjenNiz[Brojac]['sifra']==22:
            self.generatorImpulsa(Par1,Ulaz1,Brojac)
        elif self.ObradjenNiz[Brojac]['sifra']==23:
            self.jedinicnoKasnjenje(Par1,Par2,Ulaz1,Brojac)
        elif self.ObradjenNiz[Brojac]['sifra']==24:
            self.vacuous(sledeciBlok, Brojac)
        elif self.ObradjenNiz[Brojac]['sifra']==26:
            self.sabirac(Par1,Par2,Par3,Ulaz1,Ulaz2,Ulaz3,Brojac)
        elif self.ObradjenNiz[Brojac]['sifra']==27:
            self.mnozac(Ulaz1,Ulaz2,Brojac)
        elif self.ObradjenNiz[Brojac]['sifra']==28:
            self.wye(Par1,Par2,Ulaz1,Ulaz2,Brojac,PomUl1,sledeciBlok)

        if sledeciBlok<self.BrojSortiranih:
            sledeciBlok+=1

            self.izracunaj(sledeciBlok)

        else:
            if sledeciBlok>self.BrojSortiranih:
                self.VrstaPrekida['tip']= "GreskaObrade"
                self.VrstaPrekida['poruka'] = "Greska obrade" 
    #jesmo
    @classmethod
    def racunaj(self, korakStampe, trenutniBlok ):
        f = open("terminal.txt", mode="a")
        f.write("usao u racunaj ")
        f.write("\r\n")
        f.close()
        

        PomProm, PomA, PomM= 0,0,0
        PomEP=0.0
        BrTacStampe= 0.0

        NizK = [IVslog]*(self.BrojIntegratora+1)
        self.VektorX = [None]*(self.BrojIntegratora+1)
        self.VektorY = [None]*(self.BrojIntegratora+1)
        self.VektorZ = [None]*(self.BrojIntegratora+1)
        # print("vekX",len(self.VektorX))
        # print("vekY",len(self.VektorY))
        # print("vekZ",len(self.VektorZ))
        print("sortiranih br" ,self.BrojSortiranih)
        for PomProm in range (0,self.BrojSortiranih):
            #videti koliki je brojSortiranih
            PomA = self.SortiranNiz[PomProm+1]
            f = open("terminal.txt", mode="a")
            f.write("poma "+ str(PomA))
            f.write("\r\n")
            f.close()
            
            self.NizIzlaza[PomA] = self.ObradjenNiz[PomA]["parI"]

        for PomProm in range (1, self.BrojIntegratora):
            PomA = self.NizRBIntegratora[PomProm]
            # print('Obradjeni PomaA ',self.ObradjenNiz[PomA])
            self.VektorY[PomProm] = self.ObradjenNiz[PomA]["parI"]
        # print(self.VektorY)
        # j1 se racuna f(xn, yn)
        self.TekVremeSim = 0.0
        PomEP = self.PolaIntIntegracije/(self.OpcijeSimulacije["intervalStampanja"] * 2.0)
        self.VrstaPrekida["tip"] = "NemaRac"
        BrTacStampe = round(self.TekVremeSim/self.OpcijeSimulacije["intervalStampanja"] + 1)
        self.polaIntervala()
        #kraj f(xn,yn)
        self.zabeleziIzlaz(korakStampe, trenutniBlok)


        while True:
            #k2 se racuna
            # PRVA POLOVINA INTERVALA: racuna se f(Xn+1/2*h, Yn+1/2*k1)
            self.VrstaPrekida["tip"] = "PrvaPol"
            for PomProm in range(1,self.BrojIntegratora):
    
                self.VektorZ[PomProm] = self.VektorY[PomProm]
                NizK[PomProm]['k1'] = self.OpcijeSimulacije["intervalInteg"] * self.VektorX[PomProm]
                self.VektorY[PomProm] = self.VektorZ[PomProm] + 1/2 * NizK[PomProm]['k1']
            
            self.TekVremeSim += self.PolaIntIntegracije
            self.NizIzlaza[self.BrojBlokova] = self.TekVremeSim
            self.polaIntervala()
            #k2 kraj

            #k3 se racuna
            #DRUGA POLOVINA INTERVALA: racuna se f(Xn+1/2*h, Yn+1/2*k2)
            self.VrstaPrekida['tip'] = 'DrugaPol'
            for PomProm in range(1, self.BrojIntegratora):
                NizK[PomProm]['k2'] = self.OpcijeSimulacije["intervalInteg"] * self.VektorX[PomProm]
                self.VektorY[PomProm] = self.VektorZ[PomProm] + 1/2 * NizK[PomProm]['k2']
            self.polaIntervala()
            #k3 kraj

            #k4 se racuna
            #racuna se f(Xn+h, Yn+k3)
            #trebalo bi hk3, ali to nije definisano
            for PomProm in range(1, self.BrojIntegratora):
                NizK[PomProm]['k3'] = self.OpcijeSimulacije["intervalInteg"] * self.VektorX[PomProm]
                self.VektorY[PomProm] = self.VektorZ[PomProm] + NizK[PomProm]['k3']
            self.TekVremeSim += self.PolaIntIntegracije
            self.NizIzlaza[self.BrojBlokova] = self.TekVremeSim
            print("tekuce vreme ", self.TekVremeSim)
            self.polaIntervala()
            #k4 kraj

            for PomProm in range(1, self.BrojIntegratora):
                # print(PomProm)
                # print(self.VektorZ)
                # print(self.VektorX)
                # print(self.VektorY)

                # print(self.VektorZ[PomProm])
                # print(type(NizK[PomProm]['k1']))
                # print(type(NizK[PomProm]['k2']))
                # print(type(NizK[PomProm]['k3']))
                # print(type(self.OpcijeSimulacije["intervalInteg"]))
                # print(type(self.VektorX[PomProm]))
                self.VektorY[PomProm] = self.VektorZ[PomProm] + 1/6 *(NizK[PomProm]['k1'] + 2*NizK[PomProm]['k2'] + 2*NizK[PomProm]['k3'] + self.OpcijeSimulacije["intervalInteg"]*self.VektorX[PomProm])
            self.polaIntervala()

            #kraj runge kutta

            if (self.VrstaPrekida["tip"] in ["GreskaObrade", "KrajQuit"]):
                if (self.VrstaPrekida["tip"] == "KrajQuit"):
                    self.SimulacijaOdradjena = True
                else:
                    self.SimulacijaOdradjena  = False
                exit()
            else:
                PomM = round(self.TekVremeSim/self.OpcijeSimulacije["intervalStampanja"] + PomEP)
                if (BrTacStampe <= PomM):
                    self.zabeleziIzlaz(korakStampe, trenutniBlok)
                    BrTacStampe = PomM + 1
            #ovaj if prekida while (repeat-until)
            if self.TekVremeSim>= (self.OpcijeSimulacije['duzinaSimulacije']+self.PolaIntIntegracije):
                return        
    #jesmo
    @classmethod
    def obradiNiz(self):
        # print("usao u obradi")

        tabelaKonfiguracije = "test simple.csv"
        nizZaObradu=self.ucitajCSV(self, tabelaKonfiguracije)
        self.BrojBlokova = len(nizZaObradu)+1
        self.ObradjenNiz = []
        self.ObradjenNiz.append(tBlok)
        for el in nizZaObradu:
            self.ObradjenNiz.append(el)
        
        brInteg = 0
        self.NizRBIntegratora.append(brInteg)
        for el in self.ObradjenNiz:
            # print(el)
            if el['sifra']==10:
                brInteg+=1
                self.NizRBIntegratora.append(el['rbBloka'])
                el['rbIntegratora']=brInteg
            elif el['sifra']!=7: 
                #sta se desava sa rbInteg ako jeste 7
                el['rbIntegratora']=0
        with open("obradjeni.json", mode='w') as obrada_out:
            json.dump(self.ObradjenNiz, obrada_out)
        self.NizRBIntegratora[0]=brInteg
        self.BrojIntegratora = brInteg
    
    #jesmo    
    @classmethod
    def pocetak(self):
        # print("usao u pocetak")

        self.SimulacijaOdradjena=True
        if self.proveraGresaka():
            self.obradiNiz()
            self.sortirajNiz()
            # duzinaSim = int(input("Unesi duzinu simulacije> "))
            # intervalIntg = float(input("Unesi interval integracije> "))
            # intervalStamp = float(input("Unesi interval stampanja> "))
            # self.OpcijeSimulacije['duzinaSimulacije']=duzinaSim
            # self.OpcijeSimulacije['intervalInteg']=intervalIntg
            # self.OpcijeSimulacije['intervalStampanja']=intervalStamp
            self.PolaIntIntegracije = self.OpcijeSimulacije['intervalInteg']/2

            self.simulacija()

        else:
            self.SimulacijaOdradjena=False
    #jesmo
    @classmethod
    def polaIntervala(self):
        sledeciBlok = -1
        pomBrojac = -1

        for pomBrInteg in range(1, self.BrojIntegratora):
            pomBrojac=self.NizRBIntegratora[pomBrInteg]
            self.NizIzlaza[pomBrojac]=self.VektorY[pomBrInteg]
        sledeciBlok= self.BrKonst+2
        self.izracunaj(sledeciBlok)
    
    #jesmo
    @classmethod
    def proveraGresaka(self):
        # print("usao u proveragresaka")

        PrevedenNiz = self.ucitajCSV(self,"test simple.csv")
        brojInteg =0
        for el in PrevedenNiz:
            if el['sifra']==10:
                brojInteg+=1
        
        if len(PrevedenNiz)<1:
            print("Model mora imati najmanje jedan blok")
            return False
        elif brojInteg<1:
            print("Model mora imati najmanje 1 integrator")
            return False
        else:
            for el in PrevedenNiz:
                if el['sifra']==7:
                    if el['parII']>el['parI']:
                        print("Kod generatora fja prvi ulaz mora biti veci od drugog")
                        return False
            return True
    #jesmo            
    @classmethod
    def simulacija(self):
        # print("usao u simulacija")

        #broj kolona u izlazu
        # print(self.OpcijeSimulacije['duzinaSimulacije'])
        # print(self.OpcijeSimulacije['intervalStampanja'])

        pom = round(self.OpcijeSimulacije['duzinaSimulacije']/self.OpcijeSimulacije['intervalStampanja'])+1
        #brBlokova ima jedan visak, zato je minus 1
        self.matrixReal = np.zeros((pom+2,self.BrojBlokova-1),dtype=float)
        korakStampe, trenutniBlok = 0,0
        for i in range(self.BrojBlokova-2):
            korakStampe = 0
            trenutniBlok = i+1
            self.NizZaStampu=[None]*(pom+2)
            for j in range(pom+1):
                self.NizZaStampu[j]=0
            self.NizIzlaza=[None]*(self.BrojBlokova+1)
            #None - broj elemenata - None
            for j in range(1,self.BrojBlokova):
                self.NizIzlaza[j]=0
            
            self.racunaj(korakStampe, trenutniBlok)

            if self.SimulacijaOdradjena==True:
                for j in range(pom+1):
                    self.matrixReal.itemset((j,i),self.NizZaStampu[j+1])
                    np.savetxt('test.txt', self.matrixReal)
            else:
                return
    #jesmo
    @classmethod
    def sortirajNiz(self):

        #ovo mozda obrisati      
        self.BrojBlokova=len(self.ObradjenNiz)
        #sortirani niz ima 2 vise
        #broj blokova ima 1 vise
        self.SortiranNiz=[self.BrojBlokova]
        for i in range(1,self.BrojBlokova):
            self.SortiranNiz.insert(i,0)
        with open("sortiran.json", mode="a") as sortiran_out:
            json.dump(self.SortiranNiz, sortiran_out)
        for i in range(1,self.BrojBlokova):
            if self.ObradjenNiz[i]['rbBloka']!=0 and self.ObradjenNiz[i]['sifra']==12:
                self.BrojSortiranih+=1
                self.SortiranNiz[self.BrojSortiranih]=self.ObradjenNiz[i]['rbBloka']
                self.ObradjenNiz[i]['sortiran']=True
        with open("obradjeni.json", mode="a") as obrout:
            json.dump(self.ObradjenNiz, obrout)
        #sortiranje ostalih blokova
        while True:
            i=1
            ponovo=False
            while i<=self.BrojBlokova-1 and not ponovo:
                # print(self.ObradjenNiz[i]['sortiran'])
                if self.ObradjenNiz[i]['sortiran']!=True and self.ObradjenNiz[i]['rbBloka']!=0:
                    ulaz1=self.ObradjenNiz[i]['ulazI']
                    ulaz2=self.ObradjenNiz[i]['ulazII']
                    ulaz3=self.ObradjenNiz[i]['ulazIII']
                    # print(ulaz1,ulaz2,ulaz3)
                    
                    if (((self.ObradjenNiz[ulaz1]['sifra'] in [10,23]) or (self.ObradjenNiz[ulaz1]['sortiran']) or (ulaz1 in [0,self.BrojBlokova])) and ((self.ObradjenNiz[ulaz2]['sifra'] in [10,23]) or (self.ObradjenNiz[ulaz2]['sortiran']) or (ulaz2 in [0,self.BrojBlokova])) and ((self.ObradjenNiz[ulaz3]['sifra'] in [10,23]) or (self.ObradjenNiz[ulaz3]['sortiran']) or (ulaz3 in [0,self.BrojBlokova]))):
                        # print('Usao !!!')
                        ponovo=True
                        self.BrojSortiranih+=1
                        self.SortiranNiz[self.BrojSortiranih]=self.ObradjenNiz[i]['rbBloka']
                        # print(self.SortiranNiz[self.BrojSortiranih])
                        self.ObradjenNiz[i]['sortiran']=True

                    else:
                        # print('else Usao !!!')
                        ponovo=False
                if not ponovo:
                    i+=1
                
            if i>self.BrojBlokova-1 and not ponovo:
                with open("obradjeni.json", mode="w") as obrout:
                    json.dump(self.ObradjenNiz, obrout)
                with open("sortiran.json", mode="w") as sortout:
                    json.dump(self.SortiranNiz, sortout)

                break 

    #jesmo
    @classmethod
    def zabeleziIzlaz(self, korakStampe, trenutniBlok ):
        # print("usao u zabeleziizlaz")

        korakStampe+=1
        self.NizZaStampu[korakStampe]=self.NizIzlaza[trenutniBlok]

    
    @classmethod
    def sabirac(self,p1,p2,p3,u1,u2,u3,brojac):
        # print("usao u sabirac")

        self.NizIzlaza[brojac]= p1*u1+p2*u2+p3*u3
    
    @classmethod
    def mnozac(self,u1,u2,brojac):
        # print("usao u mnozac")

        self.NizIzlaza[brojac]=u1*u2
    
    @classmethod
    def apsolutnavrednost(self,u1,brojac):
        self.NizIzlaza[brojac]=abs(u1)
    
    @classmethod
    def delitelj(self,u1,u2,brojac):
        # print("usao u delitelj")

        if(u2!=0):
            self.NizIzlaza[brojac]=u1/u2
        else:
            self.VrstaPrekida['tip'] = 'GreskaObrade'
            self.VrstaPrekida['poruka'] = 'Drugi ulaz u delitelj je 0!'
    
    @classmethod
    def invertor(self,u1,brojac):
        self.NizIzlaza[brojac]=-u1
    
    @classmethod
    def kvadratniKoren(self,u1,brojac):
        if(u1>=0):
            self.NizIzlaza[brojac]=math.sqrt(u1)
        else:
            self.VrstaPrekida['tip'] = 'GreskaObrade'
            self.VrstaPrekida['poruka'] = 'Ulaz u kvadratni koren je negativan!'
    
    @classmethod
    def offset(self,p1,u1,brojac):
        self.NizIzlaza[brojac]=p1+u1

    @classmethod
    def pojacanje(self,p1,u1,brojac):
        self.NizIzlaza[brojac]=p1*u1

    @classmethod
    def relej(self,u1,u2,u3,brojac):
        if u1<0:
            self.NizIzlaza[brojac]=u3
        else:
            self.NizIzlaza[brojac]=u2

    @classmethod
    def signum(self,u1,brojac):
        self.NizIzlaza[brojac]=np.sign(u1)
    
    @classmethod
    def sinus(self,p1,p2,p3,u1,brojac):
        self.NizIzlaza[brojac]=p1*math.sin(p2*u1 + p3)
    
    @classmethod
    def kosinus(self,p1,p2,p3,u1,brojac):
        # print("usao u kosinus")

        self.NizIzlaza[brojac]=p1*math.cos(p2*u1+p3)
    
    @classmethod
    def arkusTanges(self,p1,p2,p3,u1,brojac):
        pom = p2*u1+p3
        if pom>0:
            self.NizIzlaza[brojac]=p1*math.atan(p2*u1+p3)
        else:
            self.VrstaPrekida['tip'] = 'GreskaObrade'
            self.VrstaPrekida['poruka'] = 'Vrednost za ArcTan je negativna!'

    @classmethod
    def eksponent(self,p1,p2,p3,u1,brojac):
        self.NizIzlaza[brojac]=p1*np.exp(p2*u1+p3)
        
    @classmethod
    def mrtvaZona(self,p1,p2,u1,brojac):
        #p1 donja granica, p2 gornja granica
        if u1>p1 and u1<p2:
            self.NizIzlaza[brojac]=0
        else:
            self.NizIzlaza[brojac]= u1
    
    @classmethod
    def generatorSlucajnihBrojeva(self, brojac):
        self.NizIzlaza[brojac] = random.randint(1,99999)

    @classmethod
    def ogranicavac(self,p1,p2,u1,brojac):
        #p1 donja granica, p2 gornja granica
        if u1<p1:
            self.NizIzlaza[brojac]=p1
        else:
            if u1>p2:
                self.NizIzlaza[brojac]=p2
            else:
                self.NizIzlaza[brojac]=u1
    
    @classmethod
    def negativniOgranicavac(self,u1,brojac):
        if u1<0:
            self.NizIzlaza[brojac]=0
        else:
            self.NizIzlaza[brojac]=u1
    
    @classmethod
    def pozitivniOgranicavac(self,u1,brojac):
        if u1>0:
            self.NizIzlaza[brojac]= 0
        else:
            self.NizIzlaza[brojac]=u1
    
    @classmethod
    def generatorFja(self,p1,p2,p3,u1,brojac):
        pomaA, pomB = 0,0
        pomA = p1-p2
        p3=p1-p2
        if(p3>0):
            par1=10*(u1-p2)/p3
            pomb = math.floor(par1)
            if p1<0:
               self.NizIzlaza[brojac]= self.FunkGener[pomA][1]
            else:
                if pomb>=10:
                    self.NizIzlaza[brojac]=self.FunkGener[pomaA][11]
                p2=pomB
                p3=p1-p2
                p1=self.FunkGener[pomaA][pomB+1]
                p2=self.FunkGener[pomaA][pomB+2]
                self.NizIzlaza[brojac]=p1+p3(p2-p1)
        else:
            self.VrstaPrekida['tip'] = "GreskaObrade"
            self.VrstaPrekida['poruka'] ='Kod generatora f-ja razlika prvog i drugog parametra mora biti pozitivna!'
            
    @classmethod
    def generatorImpulsa(self,p1,u1,brojac):
        if self.VrstaPrekida['tip']=="NemaRac":
            self.ObradjenNiz[brojac]["parII"]=-p1
            if u1<0:
                self.NizIzlaza[brojac]=0
            else:
                self.NizIzlaza[brojac]=1
        else:
            if u1> 0:
                self.ObradjenNiz[brojac]["parII"] = -p1
                self.NizIzlaza[brojac]= 1
            else:
                if u1<0:
                    self.NizIzlaza[brojac]= 0
                else:
                    self.NizIzlaza[brojac]=1

    @classmethod
    def jedinicnoKasnjenje(self,p1,p2,u1,brojac):
        
        if self.VrstaPrekida['tip'] == "NemaRac":
            self.NizIzlaza[brojac]=p1
        else:
            self.NizIzlaza[brojac]=p2
        self.ObradjenNiz[brojac]['parII'] = u1

    @classmethod
    def integrator(self,p2,p3,u1,u2,u3,brojac):
        # print("usao u integrator")

        pomocnoBrx = self.ObradjenNiz[brojac]["rbIntegratora"]
        print("pomocnoBrx ", pomocnoBrx)
        self.VektorX[pomocnoBrx] = u1+p2*u2+p3*u3
        print("vektor ", u1+p2*u2+p3*u3)
        
    
    @classmethod
    def kolozadrske(self,p1,p2,u1,u2,brojac):
        if self.VrstaPrekida['tip'] == 'NemaRac':
            self.ObradjenNiz[brojac]["parII"] = p1
            p2=p1
        if u2<0:
            self.NizIzlaza[brojac]=0
        elif u2==0:
            self.NizIzlaza[brojac]=p2
        else:
            self.ObradjenNiz[brojac]["parII"]=u1
            self.NizIzlaza[brojac]=u1
    
    @classmethod
    def krajSimulacije(self,u1,u2,brojac):
        if u2<u1:
            self.VrstaPrekida['tip'] = "KrajQuit"
            self.VrstaPrekida['poruka'] = "Kraj simulacije od strane Quit elementa."
    
    @classmethod
    def vacuous(self,sledeciblok, brojac):
        if self.VrstaPrekida['tip'] == "NemaRac":
            self.ObradjenNiz[brojac]["rbIntegratora"] = sledeciblok
    
    @classmethod
    def wye(self,p1,p2,u1,u2,brojac,pomUl1,sledeciBlok):
        pomA = 0.0
        if u1==0:
            self.VrstaPrekida['tip'] = 'GreskaObrade'
            self.VrstaPrekida['poruka'] = 'Prvi ulaz u Wye element je jednak nuli ili ne postoji!'
        else:
            pomA=abs(1-u2/u1)
            if pomA<p1:
                self.NizIzlaza[brojac]=u1
            else:
                self.NizIzlaza[pomUl1] = (1-p2)*u1+p2*u2
                sledeciBlok=self.ObradjenNiz[pomUl1]["rbIntegratora"]
                self.izracunaj(sledeciBlok)


simulacija = tSimulacija()
simulacija.pocetak()
