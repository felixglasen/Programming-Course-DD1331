#denna kod ber användaren ange en storlek på en kortlek och anger hur många
#gånger kortleken måste blandas för att återgå till ursprungskombinationen



with open("ordlista.utf8", "r", encoding="utf8") as handle: 
    ord_lista = []
    for line in handle:
        for ord in line.split(): #varje rad delas upp i en lista av alla ord. Dessa ord är mellanslagsseparerade
            ord = ord.strip()  #extra white space i början eller slutet av ordet tas bort
            ord_lista.append(ord)


    

def kuperade_ord(v, sokfunktion):
    """denna funktion tar in en lista och en sökfunktion och returnerar en lista av alla ord som är kuperingar av varandra"""
    kupering_dictionary = {} #vi skapar först ett dictionary för att sortera alla kuperingar

    for ord in v: #för varje ord i v skapar vi en lista med kuperingar
        kuperingar = generera_kuperingar(ord)

        for kupering in kuperingar:
            if sokfunktion(v, kupering): #om en ord finnns i listan (vilket granskas med linjär- eller binärsökning) går vi vidare till if-satsen
                if ord not in kupering_dictionary: #om ordet inte är en nyckel i dictionaryt skapas en lista som värde för detta ord
                    kupering_dictionary[ord] = [] #[ord] refererar till att vi skapar en lista åt denhär nyckeln i ordboken
                kupering_dictionary[ord].append(kupering) #nu när nyckeln finns kan vi lägga till ord i listan

    resultat = []
    unika_kuperingar = set() #skapar en uppsättning och håller reda på unika tupler. Vi använder set eftersom dem inte använder dubletter.

    #nedan tar vi alla kombinationer av kuperingar och rensar dubletter
    for ord, kuperingar in kupering_dictionary.items():
        #i kommande del lägger vi till alla kuperingar av ett ord i en tupel med ordet. Detta läggs in i kupering_lista. 
        #Sedan kontrollerar vi om kombinationen redan finns i unika_kuperingar, om inte läggs den  till i resultat och unika_kuperingar
        if kuperingar:
            kupering_lista = tuple(sorted([ord] + kuperingar)) 
            if kupering_lista not in unika_kuperingar:
                resultat.append([ord] + kuperingar)
                unika_kuperingar.add(kupering_lista) 

    return resultat




def generera_kuperingar(ord):
    """denna funktion skapar alla möjliga kuperingar av ett ord"""
    kuperingar = []
    ordets_längd = len(ord)

    for i in range(1, ordets_längd):  #vi börjar från den första bokstaven till den sista
        kupering = ord[i:] + ord[:i]
        kuperingar.append(kupering)

    return kuperingar



def linjarsok(v, ord):
    """Denna funktion linjärsöker genom att loopa igenom varje element i v"""
    for item in v:
        if item == ord: #Vi jämför varje ord i listan
            return True
    return False



def binarsok(v, ord):
    """Returnerar True om word finns i v.
    Denna implementation använder binärsökning"""
    low = 0
    high = len(v) - 1
    while low <= high:
        mid = (low + high)//2
        if ord < v[mid]:
            high = mid - 1
        elif ord > v[mid]:
            low = mid + 1
        else:
            return True
    return False



def testbinarsok():
    """genomför ett test för om binärsökning är möjlig"""
    for i in range(10):
        v = list(range(i))
        for j in range(i):
            if not binarsok(v, j):
                print("Jag hittade inte", j, "inuti", v)
    print("Vi klarade alla tester.")



def funktionsval(listan, användarens_funktion):
    if användarens_funktion == '-l':
        print(kuperade_ord(listan, linjarsok))
    elif användarens_funktion == '-b':
        print(kuperade_ord(listan, binarsok))
    else:
        print("Ditt val av funktion är inte giltigt, försök igen.")
        return False



def main():
    #denna del befattar sig med binarsok funktionen 
    användarens_funktion = input("Välj antingen '-l' för linjärsökning eller '-b' för binärsökning: ")
   
    kuperade_ord = ["alpin", "abc", "cab", "pinal", "gurka", "agurk", "okuperbart", "kagur"]
    kuperade_ord.sort() #Detta görs eftersom binärsökningen kräver det
    ord_lista.sort()
    listan = ord_lista
    funktionsval(listan, användarens_funktion)



if __name__ == '__main__':
    #först körs ett test och sedan anropas main
    testbinarsok()
    main()