from lxml import etree
from csv import DictReader

def UtworzPlikXML(nazwa_pliku, firma, dane_wejsciowe):

    namespace="http://crd.gov.pl/wzor/2022/11/09/11890/"

    Deklaracja = etree.Element("Deklaracja", nsmap={None:namespace})
    Plik_XML = etree.ElementTree(Deklaracja)

    Naglowek = etree.SubElement(Deklaracja, "Naglowek")
    etree.SubElement(Naglowek, "KodFormularza", kodSystemowy="PIT-11 (29)", kodPodatku="PIT", rodzajZobowiazania="Z", wersjaSchemy="1-1E").text="PIT-11"
    etree.SubElement(Naglowek, "WariantFormularza").text = "29"
    etree.SubElement(Naglowek, "CelZlozenia", poz="P_7").text = "1"
    if firma["Rok"] != "":
        etree.SubElement(Naglowek, "Rok").text = firma["Rok"]
    if dane_wejsciowe["KodUrzedu"] != "":
        etree.SubElement(Naglowek, "KodUrzedu").text = dane_wejsciowe["KodUrzedu"]

    Podmiot1 = etree.SubElement(Deklaracja, "Podmiot1", rola="Płatnik/Składający")
    OsobaNiefizyczna = etree.SubElement(Podmiot1, "OsobaNiefizyczna")
    if firma["NIP"] != "":
        etree.SubElement(OsobaNiefizyczna, "NIP").text = firma["NIP"]
    if firma["PelnaNazwa"] != "":
        etree.SubElement(OsobaNiefizyczna,"PelnaNazwa").text = firma["PelnaNazwa"]

    Podmiot2 = etree.SubElement(Deklaracja, "Podmiot2", rola="Podatnik")
    OsobaFizyczna = etree.SubElement(Podmiot2, "OsobaFizyczna")
    if dane_wejsciowe["PESEL"] != "":
        etree.SubElement(OsobaFizyczna, "PESEL").text = dane_wejsciowe["PESEL"]
    if dane_wejsciowe["ImiePierwsze"] != "":
        etree.SubElement(OsobaFizyczna, "ImiePierwsze").text = dane_wejsciowe["ImiePierwsze"]
    if dane_wejsciowe["Nazwisko"] != "":
        etree.SubElement(OsobaFizyczna, "Nazwisko").text = dane_wejsciowe["Nazwisko"]
    if dane_wejsciowe["DataUrodzenia"] != "":
        etree.SubElement(OsobaFizyczna, "DataUrodzenia").text = dane_wejsciowe["DataUrodzenia"]
    if "NrId" in dane_wejsciowe.keys():
        if dane_wejsciowe["NrId"] != "":
            etree.SubElement(OsobaFizyczna, "NrId", poz="P_13").text = dane_wejsciowe["NrId"]
    if "RodzajNrId" in dane_wejsciowe.keys():
        if dane_wejsciowe["RodzajNrId"] != "":
            etree.SubElement(OsobaFizyczna, "RodzajNrId", poz="P_14").text = dane_wejsciowe["RodzajNrId"]
    if "KodKrajuWydania" in dane_wejsciowe.keys():
        if dane_wejsciowe["KodKrajuWydania"] != "":
            etree.SubElement(OsobaFizyczna, "KodKrajuWydania", poz="P_15A").text = dane_wejsciowe["KodKrajuWydania"]    

    AdresZamieszkania = etree.SubElement(Podmiot2, "AdresZamieszkania", rodzajAdresu="RAD")
    if dane_wejsciowe["KodKraju"] != "":
        etree.SubElement(AdresZamieszkania, "KodKraju", poz="P_19A").text = dane_wejsciowe["KodKraju"]
    if dane_wejsciowe["Wojewodztwo"] != "":    
        etree.SubElement(AdresZamieszkania, "Wojewodztwo").text = dane_wejsciowe["Wojewodztwo"]
    if dane_wejsciowe["Powiat"] != "":        
        etree.SubElement(AdresZamieszkania, "Powiat").text = dane_wejsciowe["Powiat"]
    if dane_wejsciowe["Gmina"] != "":        
        etree.SubElement(AdresZamieszkania, "Gmina").text = dane_wejsciowe["Gmina"]
    if dane_wejsciowe["Ulica"] != "":
        etree.SubElement(AdresZamieszkania, "Ulica", poz="P_23").text = dane_wejsciowe["Ulica"]
    if dane_wejsciowe["NrDomu"] != "":
        etree.SubElement(AdresZamieszkania, "NrDomu", poz="P_24").text = dane_wejsciowe["NrDomu"]
    if dane_wejsciowe["NrLokalu"] != "":
        etree.SubElement(AdresZamieszkania, "NrLokalu", poz="P_25").text = dane_wejsciowe["NrLokalu"]
    if dane_wejsciowe["Miejscowosc"] != "":
        etree.SubElement(AdresZamieszkania, "Miejscowosc", poz="P_26").text = dane_wejsciowe["Miejscowosc"]
    if dane_wejsciowe["KodPocztowy"] != "":
        etree.SubElement(AdresZamieszkania, "KodPocztowy", poz="P_27").text = dane_wejsciowe["KodPocztowy"]

    PozycjeSzczegolowe = etree.SubElement(Deklaracja, "PozycjeSzczegolowe")
    if dane_wejsciowe["P_11"] != "":
        etree.SubElement(PozycjeSzczegolowe, "P_11").text = dane_wejsciowe["P_11"]
    for i in range(28,121):
        if f"P_{str(i)}" in dane_wejsciowe.keys():
            if dane_wejsciowe[f"P_{str(i)}"] != "":
               etree.SubElement(PozycjeSzczegolowe, f"P_{str(i)}").text = dane_wejsciowe[f"P_{str(i)}"]
    etree.SubElement(PozycjeSzczegolowe, "P_121").text = "2"
    etree.SubElement(Deklaracja, "Pouczenie").text = "1"

    Plik_XML.write(nazwa_pliku, pretty_print=True, xml_declaration=True, encoding="UTF-8")

def WczytajPlikCSV(schema, firma, dane):
    try:
        with open(firma, encoding="UTF-8") as f:
            slownik = DictReader(f, delimiter=';')
            slownik_firma = [x for x in slownik][0]
        try:
            xmlschema_doc = etree.parse(schema)
            xmlschema = etree.XMLSchema(xmlschema_doc)
            try:
                with open(dane, encoding="UTF-8") as f:
                    slownik = DictReader(f, delimiter=';')
                    i = 1
                    for slownik_dane in slownik:
                        plik = f"./PIT-11/PIT-11_{str(i)}.xml"
                        UtworzPlikXML(plik, slownik_firma, slownik_dane)
                        xml_doc = etree.parse(plik)
                        if xmlschema.validate(xml_doc):
                            print(f"Plik {plik} utworzony poprawnie")
                        else:
                            print(f"Plik {plik} niezgodny ze schematem XSD")
                        i += 1
            except:
                print(f"Nieudana próba wczytania danych z pliku {dane}")
        except:
            print(f"Nieudana próba wczytania schemy {schema}")
    except:
        print(f"Nieudana próba wczytania danych z pliku {firma}")

if __name__ == "__main__":

    WczytajPlikCSV("PIT-11.xsd", "firma.csv", "dane.csv")
    input("Naciśnij Enter aby zakończyć...")
