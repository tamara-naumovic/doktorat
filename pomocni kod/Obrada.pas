unit Obrada;

interface

uses
  Classes, CSMPBlok, unVeza, Dialogs, SysUtils, Math;

type
  FazaRada = (NemaRac, PrvaPol, DrugaPol, GreskaObrade, KrajQuit);

  TBlok = record
    UlazI, UlazII, UlazIII: integer;
    ParI, ParII, ParIII: real;
    IzlaznaVrednost: real;
    Sortiran: boolean;
    Sifra: byte;
    RbBloka: integer;
    RbInteg: integer; // ako je blok integrator ovo je njegov redni broj
  end;

  IVslog = record
    k1: Extended;
    k2: Extended;
    k3: Extended;
  end;

  TNizK = array of IVslog; // sluzi kod simulacije metodom Runge-Kuta IV reda

  ArrayBlok  = array of TBlok;
  ArrayInt   = array of integer;
  ArrayReal  = array of real;
  MatrixReal = array of array of real;

  TVrstaPrekida = record
    Tip: FazaRada;  // tip prekida
    Poruka: string; // poruka o nastaloj gresci
  end;

  TSimulacija = class
  private
    VektorX, VektorY, VektorZ: ArrayReal;

    procedure PolaIntervala;
    procedure Izracunaj(SledeciBlok: integer);

    procedure Integrator(Par2, Par3, Ulaz1, Ulaz2, Ulaz3: Extended;
      Brojac: integer);
    procedure Sabirac(Par1, Par2, Par3, Ulaz1, Ulaz2, Ulaz3: Extended;
      Brojac: integer);
    procedure ArkusTangens(Par1, Par2, Par3, Ulaz1: Extended; Brojac: integer);
    procedure Kosinus(Par1, Par2, Par3, Ulaz1: Extended; Brojac: integer);
    procedure Sinus(Par1, Par2, Par3, Ulaz1: Extended; Brojac: integer);
    procedure Eksponent(Par1, Par2, Par3, Ulaz1: Extended; Brojac: integer);
    procedure GeneratorFja(Par1, Par2, Par3, Ulaz1: Extended; Brojac: integer);
    procedure KoloZadrske(Par1, Par2, Ulaz1, Ulaz2: Extended; Brojac: integer);
    procedure MrtvaZona(Par1, Par2, Ulaz1: Extended; Brojac: integer);
    procedure Ogranicavac(Par1, Par2, Ulaz1: Extended; Brojac: integer);
    procedure JedinicnoKasnjenje(Par1, Par2, Ulaz1: Extended; Brojac: integer);
    procedure Wye(Par1, Par2, Ulaz1, Ulaz2: Extended; Brojac, PomUl1: integer;
      var SledeciBlok: integer);
    procedure Pojacanje(Par1, Ulaz1: Extended; Brojac: integer);
    procedure Offset(Par1, Ulaz1: Extended; Brojac: integer);
    procedure GenImpulsa(Par1, Ulaz1: Extended; Brojac: integer);
    procedure Signum(Ulaz1: Extended; Brojac: integer);
    procedure KvadKoren(Ulaz1: Extended; Brojac: integer);
    procedure NegOgranicavac(Ulaz1: Extended; Brojac: integer);
    procedure PozOgranicavac(Ulaz1: Extended; Brojac: integer);
    procedure ApsolutnaVrednost(Ulaz1: Extended; Brojac: integer);
    procedure KrajSimulacije(Ulaz1, Ulaz2: Extended);
    procedure GeneratorSlucBrojeva(Brojac: integer);
    procedure Relej(Ulaz1, Ulaz2, Ulaz3: Extended; Brojac: integer);
    procedure Mnozac(Ulaz1, Ulaz2: Extended; Brojac: integer);
    procedure Delitelj(Ulaz1, Ulaz2: Extended; Brojac: integer);
    procedure Vacuous(SledeciBlok, Brojac: integer);
    procedure Invertor(Ulaz1: Extended; Brojac: integer);

  protected
    ObradjenNiz: ArrayBlok;    // PrevedenNiz sredjen u oblik pogodan za dalji rad
    SortiranNiz: ArrayInt;     // niz indeksa sortiranih blokova
    BrojBlokova: integer;      // broj blokova u modelu
    BrojIntegratora: byte;
    BrojSortiranih: integer;
    NizRBIntegratora: ArrayInt; // niz koji cuva redne brojeve integratora u obradjenom nizu
    BrKonst: integer;           // broj konstanti u modelu
    IntervalInteg: real;
    PolaIntIntegracije: real;
    NizIzlaza: ArrayReal;    // niz u koji se pamti izlaz iz svakog bloka u svakom trenutku
    VrstaPrekida: TVrstaPrekida;
    TekVremeSim: real;
    FunkGener: array [1..4, 1..11] of real;
    TekIzlaz: Extended;
    NizZaStampu: ArrayReal;

    function ProveraGresaka(PrevedenNiz: TList; var BrKonst: integer): boolean;
    procedure ObradiNiz(NizZaObradu: TList; var ObradjenNiz: ArrayBlok;
      var BrInteg: byte; var NizRbInteg: ArrayInt; var BrBlokova: integer);
    procedure SortirajNiz(ObradjenNiz: ArrayBlok; var BrSortiranih: integer;
      const BrBlokova: integer; var SortNiz: ArrayInt);
    procedure Simulacija(var Matrica: MatrixReal);
    procedure Racunaj(var NizIzlaza: ArrayReal; var VrstaPrekida: TVrstaPrekida;
      var TekVremeSim: real; KorakStampe, TrenutniBlok: integer);
    procedure ZabeleziIzlaz(var broj: integer; TrenutniBlok: integer);

  public
    SimulacijaOdradjena: boolean;
    DuzinaSimulacije: real;
    IntervalStampanja: real;

    procedure Pocetak(PrevedenNiz: TList;  var Matrix: MatrixReal);
  end;

var
  Simulacija: TSimulacija;

implementation

uses
  OpcijeSim;

{ TSimulacija }

procedure TSimulacija.ArkusTangens(Par1, Par2, Par3, Ulaz1: Extended;
  Brojac: integer);
var
  Pom: real;
begin
  Pom := Par2 * Ulaz1 + Par3;
  if (Pom > 0.0) then
    NizIzlaza[Brojac] := Par1 * ArcTan(Pom)
  else
  begin
    VrstaPrekida.Tip := GreskaObrade;
    VrstaPrekida.Poruka := 'Vrednost za ArcTan je negativna!';
  end;
end;

procedure TSimulacija.KoloZadrske(Par1, Par2, Ulaz1, Ulaz2: Extended;
  Brojac: integer);
begin
  if (VrstaPrekida.Tip = NemaRac) then
  begin
    ObradjenNiz[Brojac].ParII := Par1;
    Par2 := Par1
  end;
  if (Ulaz2 < 0.0) then
    NizIzlaza[Brojac] := 0
  else
    if (Ulaz2 = 0.0) then
      NizIzlaza[Brojac] := Par2
    else
    begin
      ObradjenNiz[Brojac].ParII := Ulaz1;
      NizIzlaza[Brojac] := Ulaz1;
    end;
end;

procedure TSimulacija.Signum(Ulaz1: Extended; Brojac: integer);
begin
  NizIzlaza[Brojac] := sign(Ulaz1)
end;

procedure TSimulacija.Kosinus(Par1, Par2, Par3, Ulaz1: Extended;
  Brojac: integer);
begin
  NizIzlaza[Brojac] := Par1 * Cos(Par2 * Ulaz1 + Par3);
end;

procedure TSimulacija.MrtvaZona(Par1, Par2, Ulaz1: Extended; Brojac: integer);
begin
  if ((Ulaz1 > Par1) and (Ulaz1 < Par2)) then
    NizIzlaza[Brojac] := 0
  else
    NizIzlaza[Brojac] := Ulaz1;
end;

procedure TSimulacija.Eksponent(Par1, Par2, Par3, Ulaz1: Extended;
  Brojac: integer);
begin
  NizIzlaza[Brojac] := Par1 * Exp(Par2 * Ulaz1 + Par3);
end;

procedure TSimulacija.GeneratorFja(Par1, Par2, Par3, Ulaz1: Extended;
  Brojac: integer);
var
  PomA, PomB: integer;
begin
  // ako je trenutni blok I, PomA je njegov redni broj u nizu integratora
  PomA := ObradjenNiz[Brojac].RbInteg;

  Par3 := Par1 - Par2;
  if (Par3 > 0.0) then
  begin
    Par1 := 10 * (Ulaz1-Par2)/Par3;
    PomB := trunc(Par1);
    if (Par1 <= 0.0) then
      NizIzlaza[Brojac] := FunkGener[PomA, 1]
    else
      if(PomB >= 10) then
        NizIzlaza[Brojac] := FunkGener[PomA, 11]
      else
      begin
        Par2 := PomB;
        Par3 := Par1 - Par2;
        Par1 := FunkGener[PomA, PomB+1];
        Par2 := FunkGener[PomA, PomB+2];
        NizIzlaza[Brojac] := Par1 + Par3*(Par2-Par1);
      end;
  end
  else
  begin
    VrstaPrekida.Tip := GreskaObrade;
    VrstaPrekida.Poruka := 'Kod generatora f-ja razlika prvog i drugog parametra mora biti pozitivna!';
  end;
end;

procedure TSimulacija.Pojacanje(Par1, Ulaz1: Extended; Brojac: integer);
begin
  NizIzlaza[Brojac] := Par1 * Ulaz1;
end;

procedure TSimulacija.KvadKoren(Ulaz1: Extended; Brojac: integer);
begin
  if (Ulaz1 >= 0) then
    NizIzlaza[Brojac] := Sqrt(Ulaz1)
  else
  begin
    VrstaPrekida.Tip := GreskaObrade;
    VrstaPrekida.Poruka := 'Ulaz u kvadratni koren je negativan!';
  end;
end;

procedure TSimulacija.Integrator(Par2, Par3, Ulaz1, Ulaz2, Ulaz3: Extended;
  Brojac: integer);
var
  PomBrX: integer;
begin
  PomBrX := ObradjenNiz[Brojac].RbInteg;
  VektorX[PomBrX] := Ulaz1 + Par2*Ulaz2 + Par3*Ulaz3;
end;

procedure TSimulacija.GeneratorSlucBrojeva(Brojac: integer);
begin
  Randomize;
  NizIzlaza[Brojac] := Random;
end;

procedure TSimulacija.Ogranicavac(Par1, Par2, Ulaz1: Extended;
  Brojac: integer);
begin
  if (Ulaz1 < Par1) then
    NizIzlaza[Brojac] := Par1
  else
    if (Ulaz1 > Par2) then
      NizIzlaza[Brojac] := Par2
    else
      NizIzlaza[Brojac] := Ulaz1;
end;

procedure TSimulacija.ApsolutnaVrednost(Ulaz1: Extended; Brojac: integer);
begin
  NizIzlaza[Brojac] := Abs(Ulaz1);
end;

procedure TSimulacija.NegOgranicavac(Ulaz1: Extended; Brojac: integer);
begin
  if (Ulaz1 < 0.0) then
    NizIzlaza[Brojac] := 0.0
  else
    NizIzlaza[Brojac] := Ulaz1;
end;

procedure TSimulacija.Offset(Par1, Ulaz1: Extended; Brojac: integer);
begin
  NizIzlaza[Brojac] := Ulaz1 + Par1;
end;

procedure TSimulacija.PozOgranicavac(Ulaz1: Extended; Brojac: integer);
begin
  if (Ulaz1 > 0.0) then
    NizIzlaza[Brojac] := 0.0
  else
    NizIzlaza[Brojac] := Ulaz1;
end;

procedure TSimulacija.KrajSimulacije(Ulaz1, Ulaz2: Extended);
begin
  if (Ulaz2 < Ulaz1) then
  begin
    VrstaPrekida.Tip := KrajQuit;
    VrstaPrekida.Poruka := 'Kraj simulacije od strane Quit elementa.';
  end;
end;

procedure TSimulacija.Relej(Ulaz1, Ulaz2, Ulaz3: Extended;
  Brojac: integer);
begin
  if (Ulaz1 < 0.0) then
    NizIzlaza[Brojac] := Ulaz3
  else
    NizIzlaza[Brojac] := Ulaz2;
end;

procedure TSimulacija.Sinus(Par1, Par2, Par3, Ulaz1: Extended;
  Brojac: integer);
begin
  NizIzlaza[Brojac] := Par1 * Sin(Par2*Ulaz1 + Par3);
end;

procedure TSimulacija.GenImpulsa(Par1, Ulaz1: Extended; Brojac: integer);
begin
  if (VrstaPrekida.Tip = NemaRac) then
  begin
    ObradjenNiz[Brojac].ParII := -Par1;
    if (Ulaz1 < 0.0) then
      NizIzlaza[Brojac] := 0
    else NizIzlaza[Brojac] := 1;
  end
  else
    if (Ulaz1 > 0.0) then
    begin
      ObradjenNiz[Brojac].ParII := -Par1;
      NizIzlaza[Brojac] := 1;
    end
    else
      if (Ulaz1 < 0.0) then
        NizIzlaza[Brojac] := 0
      else NizIzlaza[Brojac] := 1;
end;

procedure TSimulacija.JedinicnoKasnjenje(Par1, Par2, Ulaz1: Extended;
  Brojac: integer);
begin
  if (VrstaPrekida.Tip = NemaRac) then
    NizIzlaza[Brojac] := Par1
  else
    NizIzlaza[Brojac] := Par2;
  ObradjenNiz[Brojac].ParII := Ulaz1;
end;

procedure TSimulacija.Vacuous(SledeciBlok, Brojac: integer);
begin
  if (VrstaPrekida.Tip = NemaRac) then
    ObradjenNiz[Brojac].RbInteg := SledeciBlok;
end;

procedure TSimulacija.Sabirac(Par1, Par2, Par3, Ulaz1, Ulaz2, Ulaz3: Extended;
  Brojac: integer);
begin
  NizIzlaza[Brojac] := Par1*Ulaz1 + Par2*Ulaz2 + Par3*Ulaz3;
end;

procedure TSimulacija.Mnozac(Ulaz1, Ulaz2: Extended; Brojac: integer);
begin
  NizIzlaza[Brojac] := Ulaz1 * Ulaz2;
end;

procedure TSimulacija.Wye(Par1, Par2, Ulaz1, Ulaz2: Extended;
  Brojac, PomUl1: integer; var SledeciBlok: integer);
var
  PomA: real;
begin
  if (Ulaz1 = 0) then
  begin
    VrstaPrekida.Tip := GreskaObrade;
    VrstaPrekida.Poruka := 'Prvi ulaz u Wye element je jednak nuli ili ne postoji!';
  end
  else
  begin
    PomA := Abs(1 - Ulaz2/Ulaz1);
    if (PomA < Par1) then
      NizIzlaza[Brojac] := Ulaz1
    else
    begin
      NizIzlaza[PomUl1] := (1 - Par2)*Ulaz1 + Par2*Ulaz2;
      SledeciBlok := ObradjenNiz[PomUl1].RbInteg;
      Izracunaj(SledeciBlok);
    end;
  end;
end;

procedure TSimulacija.Delitelj(Ulaz1, Ulaz2: Extended; Brojac: integer);
begin
  if (Ulaz2 <> 0) then
    NizIzlaza[Brojac] := Ulaz1/Ulaz2
  else
  begin
    VrstaPrekida.Tip := GreskaObrade;
    VrstaPrekida.Poruka := 'Drugi ulaz u delitelj je 0!';
  end;
end;

procedure TSimulacija.Invertor(Ulaz1: Extended; Brojac: integer);
begin
  NizIzlaza[Brojac] := -Ulaz1;
end;

procedure TSimulacija.Izracunaj(SledeciBlok: integer);
var
  Par1, Par2, Par3, Ulaz1, Ulaz2, Ulaz3: Extended;
  PomUl1, PomUl2, PomUl3, Brojac: integer;

begin
  // Pocinje racunanje
  Brojac := SortiranNiz[SledeciBlok];
  Par1 := ObradjenNiz[Brojac].ParI;
  Par2 := ObradjenNiz[Brojac].ParII;
  Par3 := ObradjenNiz[Brojac].ParIII;

  PomUl1 := ObradjenNiz[Brojac].UlazI;
  if (PomUl1 = 0)
  then Ulaz1 := 0.0
  else Ulaz1 := NizIzlaza[PomUl1];

  PomUl2 := ObradjenNiz[Brojac].UlazII;
  if (PomUl2 = 0)
  then Ulaz2 := 0.0
  else Ulaz2 := NizIzlaza[PomUl2];

  PomUl3 := ObradjenNiz[Brojac].UlazIII;
  if (PomUl3 = 0)
  then Ulaz3 := 0.0
  else Ulaz3 := NizIzlaza[PomUl3];

  case ObradjenNiz[Brojac].Sifra of
     0: KoloZadrske(Par1, Par2, Ulaz1, Ulaz2, Brojac);
     1: ArkusTangens(Par1, Par2, Par3, Ulaz1, Brojac);
     2: Signum(Ulaz1, Brojac);
     3: Kosinus(Par1, Par2, Par3, Ulaz1, Brojac);
     4: MrtvaZona(Par1, Par2, Ulaz1, Brojac);
     5: Delitelj(Ulaz1, Ulaz2, Brojac);
     6: Eksponent(Par1, Par2, Par3, Ulaz1, Brojac);
     7: GeneratorFja(Par1, Par2, Par3, Ulaz1, Brojac);
     8: Pojacanje(Par1, Ulaz1, Brojac);
     9: KvadKoren(Ulaz1, Brojac);
    10: Integrator(Par2, Par3, Ulaz1, Ulaz2, Ulaz3, Brojac);
    11: GeneratorSlucBrojeva(Brojac);
    13: Ogranicavac(Par1, Par2, Ulaz1, Brojac);
    14: ApsolutnaVrednost(Ulaz1, Brojac);
    15: Invertor(Ulaz1, Brojac);
    16: NegOgranicavac(Ulaz1, Brojac);
    17: Offset(Par1, Ulaz1, Brojac);
    18: PozOgranicavac(Ulaz1, Brojac);
    19: KrajSimulacije(Ulaz1, Ulaz2);
    20: Relej(Ulaz1, Ulaz2, Ulaz3, Brojac);
    21: Sinus(Par1, Par2, Par3, Ulaz1, Brojac);
    22: GenImpulsa(Par1, Ulaz1, Brojac);
    23: JedinicnoKasnjenje(Par1, Par2, Ulaz1, Brojac);
    24: Vacuous(SledeciBlok, Brojac);
    26: Sabirac(Par1, Par2, Par3, Ulaz1, Ulaz2, Ulaz3, Brojac);
    27: Mnozac(Ulaz1, Ulaz2, Brojac);
    28: Wye(Par1, Par2, Ulaz1, Ulaz2, Brojac, PomUl1, SledeciBlok);
  end;

  if (SledeciBlok < BrojSortiranih) then
  begin
    inc(SledeciBlok);
    Izracunaj(SledeciBlok);
  end
  else
    if (SledeciBlok > BrojSortiranih) then
    begin
      VrstaPrekida.Tip := GreskaObrade;
      VrstaPrekida.Poruka := 'Greska obrade (modul: Obrada; line: 473)';
    end;
end;

procedure TSimulacija.Racunaj(var NizIzlaza: ArrayReal;
  var VrstaPrekida: TVrstaPrekida; var TekVremeSim: real;
  KorakStampe, TrenutniBlok: integer);
// kompletno racunanje i simulacija se pokrecu u ovoj proceduri
var
  PomProm, PomA, PomM: integer;
  PomEP: real;
  NizK: TNizK;    // koristi se kod metode Runge-Kuta IV reda
  BrTacStampe: real;

begin
  SetLength(VektorX, BrojIntegratora + 1);
  SetLength(VektorY, BrojIntegratora + 1);
  SetLength(VektorZ, BrojIntegratora + 1);
  SetLength(NizK, BrojIntegratora + 1);

  for PomProm := 2 to BrojSortiranih do
  begin
    PomA := SortiranNiz[PomProm];
    NizIzlaza[PomA] := ObradjenNiz[PomA].ParI;
  end;

  for PomProm := 1 to BrojIntegratora do
  begin
    PomA := NizRbIntegratora[PomProm];
    VektorY[PomProm] := ObradjenNiz[PomA].ParI;
  end;

  TekVremeSim := 0.0;

  { racuna se f(Xn,Yn) }
  PomEP := PolaIntIntegracije/(IntervalStampanja * 2.0);
  VrstaPrekida.Tip := NemaRac;
  BrTacStampe := trunc(TekVremeSim/IntervalStampanja + 1);
  PolaIntervala;
  { kraj racuna f(Xn,Yn) }
  ZabeleziIzlaz(KorakStampe, TrenutniBlok);

  { simulacija metodom Runge-Kuta IV reda }
  repeat
   // PRVA POLOVINA INTERVALA: racuna se f(Xn+1/2*h, Yn+1/2*k1)
    VrstaPrekida.Tip := PrvaPol;
    for PomProm:=1 to BrojIntegratora do
    begin
      VektorZ[PomProm] := VektorY[PomProm];
      NizK[PomProm].k1 := IntervalInteg * VektorX[PomProm];
      VektorY[PomProm] := VektorZ[PomProm] + 1/2 * NizK[PomProm].k1;
    end;

    TekVremeSim := TekVremeSim + PolaIntIntegracije;
    NizIzlaza[BrojBlokova] := TekVremeSim;
    PolaIntervala;
    // kraj racuna f(Xn+1/2*h, Yn+1/2*k1)

    // DRUGA POLOVINA INTERVALA: racuna se f(Xn+1/2*h, Yn+1/2*k2)
    VrstaPrekida.Tip := DrugaPol;
    for PomProm := 1 to BrojIntegratora do
    begin
      NizK[PomProm].k2 := IntervalInteg * VektorX[PomProm];
      VektorY[PomProm] := VektorZ[PomProm] + 1/2 * NizK[PomProm].k2;
    end;
    PolaIntervala;
    // kraj racuna f(Xn+1/2*h, Yn+1/2*k2)

    // racuna se f(Xn+h, Yn+k3)
    for PomProm := 1 to BrojIntegratora do
    begin
      NizK[PomProm].k3 := IntervalInteg * VektorX[PomProm];
      VektorY[PomProm] := VektorZ[PomProm] + NizK[PomProm].k3;
    end;

    TekVremeSim := TekVremeSim + PolaIntIntegracije;
    NizIzlaza[BrojBlokova] := TekVremeSim;
    PolaIntervala;
    // kraj racuna f(Xn+h, Yn+k3)

    for PomProm := 1 to BrojIntegratora do
      VektorY[PomProm] := VektorZ[PomProm] + 1/6 *
        (NizK[PomProm].k1 + 2*NizK[PomProm].k2 + 2*NizK[PomProm].k3 + IntervalInteg*VektorX[PomProm]);

    PolaIntervala;
 { kraj metode Runge-Kuta IV reda }

    if (VrstaPrekida.Tip in [GreskaObrade, KrajQuit]) then
    begin
      if (VrstaPrekida.Tip = KrajQuit) then
        SimulacijaOdradjena := True
      else
      begin
        MessageDlg(VrstaPrekida.Poruka, mtError, [mbOk],0);
        SimulacijaOdradjena := False;
      end;
      Exit;
    end
    else
    begin
      PomM := round(TekVremeSim/IntervalStampanja + PomEP);
      if (BrTacStampe <= PomM) then
      begin
        ZabeleziIzlaz(KorakStampe, TrenutniBlok);
        BrTacStampe := PomM + 1
      end;
    end;

  until ( (TekVremeSim >= (DuzinaSimulacije + PolaIntIntegracije)));
end;

procedure TSimulacija.ObradiNiz(NizZaObradu: TList;
  var ObradjenNiz: ArrayBlok; var BrInteg: byte; var NizRbInteg: ArrayInt;
  var BrBlokova: integer);
// Prevodi niz blokova sa radne povrsine u niz pogodan za dalju manipilaciju,
// obradjivanje i simulaciju
var
  i: integer;

begin
  BrBlokova := NizZaObradu.Count + 1;
  SetLength(ObradjenNiz, BrBlokova);

  for i := 0 to (NizZaObradu.Count - 1) do // ObradjenNiz[0] je prazan element!
    with ObradjenNiz[i + 1] do
    begin
      if (TCSMPBlok(NizZaObradu[i]).UlazneVeze[0] <> nil) then
        if (TCSMPBlok( TVeza( TCSMPBlok(NizZaObradu[i]).UlazneVeze[0] ).PocBlok ).Sifra = 25) then
          UlazI := BrBlokova
        else
          UlazI := TCSMPBlok( TVeza( TCSMPBlok( NizZaObradu[i] ).UlazneVeze[0] ).PocBlok ).LokalniBroj
      else
        UlazI := 0;

      if (TCSMPBlok(NizZaObradu[i]).UlazneVeze[1] <> nil) then
        if (TCSMPBlok( TVeza( TCSMPBlok( NizZaObradu[i] ).UlazneVeze[1] ).PocBlok ).Sifra = 25) then
          UlazII := BrBlokova
        else
          UlazII := TCSMPBlok( TVeza( TCSMPBlok(NizZaObradu[i]).UlazneVeze[1] ).PocBlok ).LokalniBroj
      else
        UlazII := 0;

      if (TCSMPBlok(NizZaObradu[i]).UlazneVeze[2] <> nil) then
        if (TCSMPBlok( TVeza( TCSMPBlok( NizZaObradu[i] ).UlazneVeze[2] ).PocBlok ).Sifra = 25) then
          UlazIII := BrBlokova
        else
          UlazIII := TCSMPBlok( TVeza( TCSMPBlok(NizZaObradu[i]).UlazneVeze[2] ).PocBlok ).LokalniBroj
      else
        UlazIII := 0;

      ParI := TCSMPBlok(NizZaObradu[i]).ParI;
      ParII := TCSMPBlok(NizZaObradu[i]).ParII;
      ParIII := TCSMPBlok(NizZaObradu[i]).ParIII;
      RbBloka := i + 1;
      Sifra := TCSMPBlok(NizZaObradu[i]).Sifra;
      Sortiran := False;

      if (Sifra <> 7) then // ako blok nije generator funkcija
        RbInteg := 0;
    end;

  BrInteg := 0;
  for i := 1 to (BrBlokova - 1) do
    if (ObradjenNiz[i].Sifra = 10) then
    begin
      Inc(BrInteg);
      SetLength(NizRbInteg, BrInteg + 1);
      NizRbInteg[BrInteg] := ObradjenNiz[i].RbBloka;
      ObradjenNiz[i].RbInteg := BrInteg;
    end;
end;

procedure TSimulacija.Pocetak(PrevedenNiz: TList; var Matrix: MatrixReal);
begin
  SimulacijaOdradjena := True;
  if ProveraGresaka(PrevedenNiz, BrKonst) then
  begin
    ObradiNiz(PrevedenNiz, ObradjenNiz, BrojIntegratora, NizRBIntegratora, BrojBlokova);
    SortirajNiz(ObradjenNiz, BrojSortiranih, BrojBlokova, SortiranNiz);
    Opcije.ShowModal;
    if Opcije.Ok then
    begin
      DuzinaSimulacije := Opcije.DuzInt;
      IntervalInteg := Opcije.IntInt;
      PolaIntIntegracije := IntervalInteg/2;
      IntervalStampanja := Opcije.IntStamp;
      Simulacija(Matrix);
    end
    else
      SimulacijaOdradjena := False;
  end
  else
    SimulacijaOdradjena := False;
end;

procedure TSimulacija.PolaIntervala;
var
  PomBrInteg, SledeciBlok, PomBrojac: integer;

begin { PolaIntervala }
  for PomBrInteg := 1 to BrojIntegratora do
  begin
    PomBrojac := NizRBIntegratora[PomBrInteg];
    NizIzlaza[PomBrojac] := VektorY[PomBrInteg];
  end;
  SledeciBlok := BrKonst+2;
  Izracunaj(SledeciBlok);
end;

function TSimulacija.ProveraGresaka(PrevedenNiz: TList;
  var BrKonst: integer): boolean;
// Prolazi kroz PrevedenNiz i proverava da li postoje greske
var
  i, Integ: integer;
begin
  if (PrevedenNiz.Count = 0) then
  begin
    Result := False;
    MessageDlg('Model mora da sadrzi bar jedan blok!', mtError, [mbOK], 0);
    SimulacijaOdradjena := False;
    Exit;
  end;

  Result := True;
  Integ := 0;
  BrKonst := 0;

  for i := 0 to PrevedenNiz.Count-1 do
    with TCSMPBlok(PrevedenNiz.Items[i]) do
    begin
      case Sifra of
        10: Inc(Integ);
         7: if (ParII > ParI) then
            begin
              MessageDlg('Kod generatora funkcija ('+IntToStr(LokalniBroj)+') prvi parametar' + #13 +
                        '    mora biti veci od drugog !', mtError, [mbOK], 0);
              Result := False;
              SimulacijaOdradjena := False;
              exit;
            end;

        12: Inc(BrKonst);
      end;
    end; // with

  if (Integ < 1) then
  begin
    Result := False;
    MessageDlg('Model mora da sadrzi bar jedan integrator!', mtError, [mbOK], 0);
    SimulacijaOdradjena := False;
    Exit;
  end;
end;

procedure TSimulacija.Simulacija(var Matrica: MatrixReal);
var
  i, j, pom: integer;
  KorakStampe, TrenutniBlok: integer;

begin  {Pocetak simulacije}
  Pom := Round(DuzinaSimulacije/IntervalStampanja) + 1;
  SetLength(Matrica, Pom + 2, BrojBlokova - 1);
  // simulacija se izvrsava za svaki blok i sve se pamti u matrici
  for i := 0 to (BrojBlokova - 2) do
  begin
    KorakStampe := 0;
    TrenutniBlok := i + 1;

    SetLength(NizZaStampu, Pom + 2);
    for j := 0 to (Pom + 1) do
      NizZaStampu[j] := 0;

    SetLength(NizIzlaza, BrojBlokova + 1);
    for j := 1 to BrojBlokova do
      NizIzlaza[j] := 0.0;

    Racunaj(NizIzlaza, VrstaPrekida, TekVremeSim, KorakStampe, TrenutniBlok);

    if (SimulacijaOdradjena = True) then
      for j := 0 to (Pom + 1) do
        Matrica[j, i] := NizZaStampu[j + 1]
    else
      Exit;
  end;
end;

procedure TSimulacija.SortirajNiz(ObradjenNiz: ArrayBlok;
  var BrSortiranih: integer; const BrBlokova: integer;
  var SortNiz: ArrayInt);
var
  i: integer;
  Ulaz1, Ulaz2, Ulaz3: integer;
  Ponovo: boolean;

begin
  SetLength(SortNiz, BrBlokova + 1);
  SortNiz[1] := BrBlokova;      // prvi element oznacava broj blokova
  BrSortiranih := 1;
  for i := 2 to (BrBlokova - 1) do
    SortNiz[i] := 0;            // postavi brojeve blokova na 0

  for i := 1 to (BrBlokova - 1) do    // prolazi kroz niz blokova
    if (ObradjenNiz[i].RbBloka <> 0) and (ObradjenNiz[i].Sifra = 12) then
    // na prvo mesto postavlja konstante
    begin
      inc(BrSortiranih);
      SortNiz[BrSortiranih] := ObradjenNiz[i].RbBloka;
      ObradjenNiz[i].Sortiran := True;
    end;

  // sortiranje ostalih blokova
  repeat
    i := 1;
    Ponovo := False;
    while ((i <= BrBlokova - 1) and not Ponovo) do
    begin
      if (not ObradjenNiz[i].Sortiran and (ObradjenNiz[i].RbBloka <> 0)) then
      begin
        Ulaz1 := ObradjenNiz[i].UlazI;
        Ulaz2 := ObradjenNiz[i].UlazII;
        Ulaz3 := ObradjenNiz[i].UlazIII;
        if (((ObradjenNiz[Ulaz1].Sifra in [10, 23]) // ako je integrator ili jedinicno kasnjenje
             or ObradjenNiz[Ulaz1].Sortiran or (Ulaz1 in [0, BrBlokova]))
          and
            ((ObradjenNiz[Ulaz2].Sifra in [10, 23])
             or ObradjenNiz[Ulaz2].Sortiran or (Ulaz2 in [0, BrBlokova]))
          and
            ((ObradjenNiz[Ulaz3].Sifra in [10, 23])
             or ObradjenNiz[Ulaz3].Sortiran or (Ulaz3 in [0, BrBlokova])))
        then
        begin
          Ponovo := True;
          Inc(BrSortiranih);
          SortNiz[BrSortiranih] := ObradjenNiz[i].RbBloka;
          ObradjenNiz[i].Sortiran := True;
        end
        else
          Ponovo := False;
      end;
      if not Ponovo then
        Inc(i);
    end;
  until((i > BrBlokova-1) and (not Ponovo));
end;

procedure TSimulacija.ZabeleziIzlaz(var broj: integer; TrenutniBlok: integer);
begin
  inc(Broj);
  NizZaStampu[broj] := NizIzlaza[TrenutniBlok];
end;

initialization
  Simulacija := TSimulacija.Create;

finalization
  Simulacija.Free;

end.
