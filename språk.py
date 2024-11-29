import sys



# Läser indata från stdin eller argument
def läs_indata():
    # Kontrollera om indata ges genom standardinmatning (t.ex. från en fil eller också en pipe, som är fallet här)
    if not sys.stdin.isatty(): #sys.stdin.isatty() returnerar True om standardingången är terminalen
        return sys.stdin.read().strip() #denna läser all indata från standardingången och tar bort alla mellanslag etc. Dvs. man får en rensad version av filen
    else:
        message = input("Skriv något att översätta (eller 'meny' för att öppna den avancerade menyn): ").strip()
        if message.lower() == "meny":
            avancerad_meny()  #avancerad meny anropas om användaren skriver "meny"
            return None #inget returneras om den avancerade menyn aktiveras
        return message 
#denna funktion aktiveras även om ingen text att översätta anges: ex. "python3 sprak.py -f"


#Funktionen för stjärnspråket:
def stjarnsprak2(inrad):
    """Returnerar inrad där vartannat tecken är en stjärna."""
    letters = ['*']
    for tkn in inrad:
        letters.append(tkn) 
        letters.append('*') #det appendas alltid ett tecken och därefter en stjärna
    return "".join(letters) #listan med flera strängar sätts ihop till en sträng



#Funktionen för viskspråket:
def viskspråket(inrad):
    """Returnerar inraden utan vokaler."""
    vokaler = {'a', 'e', 'i', 'o', 'u', 'y', 'å', 'ä', 'ö', 'A', 'E', 'I', 'O', 'U', 'Y', 'Å', 'Ä', 'Ö'} #här definieras en uppsättning av alla vokaler, detta är en ordnad uppradning av element
    resultat = []
    for tkn in inrad:
        if tkn not in vokaler:
            resultat.append(tkn)  #Här läggs bara konsonanter till
    
    return "".join(resultat) #listan sätts ihop till en sträng



#Funktionen för rövarspråket:
def rövarspråket(inrad):
    """alla konsonanter dubbleras och ett o läggs till emellan konsonanterna"""
    konsonanter = {'b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'z', 
               'B', 'C', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'X', 'Z'}
    tillägg = "o"
    resultat = []
    for tkn in inrad:
        if tkn in konsonanter: #om tecknet är en konsonnant genomförs append nedan
            resultat.append(tkn)
            resultat.append(tillägg)
            resultat.append(tkn)
        elif tkn  not in konsonanter:
            resultat.append(tkn)
        
    return "".join(resultat) #listan sätts ihop till en sträng     



#Funktionen för översättning av rövarspråket:
def översätt_rövarspråket(inrad):
    """något som står på rövarspråket ska översättas tillbaka till svenska"""
    konsonanter = {'b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'z', 
               'B', 'C', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'X', 'Z'}
    resultat = []
    i = 0
    while i < len(inrad):
        if inrad[i] in konsonanter and i + 2 < len(inrad) and inrad[i] == inrad[i+2] and inrad[i+1] == "o":
            resultat.append(inrad[i]) #konsonanten läggs tille en gång om det ovan stämmer
            i += 3 #här hoppas konsonanten över
        else:
            resultat.append(inrad[i]) #bokstaven läggs till en gång om det ovan inte stämmer
            i += 1

    return "".join(resultat) #listan sätts ihop till en sträng 
  


#Funktionen för Bebisspråket:
def bebisspråket(inrad):
    """ordet skrivs fram till och med första vokalen och denna del upprepas tre gånger"""
    vokaler = {'a', 'e', 'i', 'o', 'u', 'y', 'å', 'ä', 'ö', 'A', 'E', 'I', 'O', 'U', 'Y', 'Å', 'Ä', 'Ö'}
    resultat = []

    for ord in inrad.split(): #orden delas upp i en lista med mellanslagsseparerade ord
        #sedan söker vi efter första vokalen och delar upp ordet i före och efter vokalen
        for index, tkn in enumerate(ord): #med hjälp av enumerate funktionen kann vi iterera över alla tecken i strängen och hålla koll på dess position
            if tkn in vokaler:
                prefix = ord[:index + 1]  #om vi hittar en vokal slicear vi ordet, +1 läggs till eftersom vokalen ska vara med
                resultat.append(prefix * 3)  #sen upprepar vi prefixet tre gånger
                break
        else:
            resultat.append(ord)  #om inga vokaler finns behålls ordet som det är

    return " ".join(resultat) #listan sätts ihop till en sträng 


#Funktionen för allspråket;
def allspråket(inrad):
    """Flyttar bokstäverna före den första vokalen till slutet av ordet och lägger till 'all'."""
    vokaler = {'a', 'e', 'i', 'o', 'u', 'y', 'å', 'ä', 'ö', 'A', 'E', 'I', 'O', 'U', 'Y', 'Å', 'Ä', 'Ö'}
    resultat = []

    for ord in inrad.split():  #Vi delar upp strängen i ord
        for index, tkn in enumerate(ord): #med hjälp av enumerate funktionen kann vi iterera över alla tecken i strängen och hålla koll på dess position
            if tkn in vokaler:
                #skapar ordet med vokal-delen först, sedan konsonant-prefix och 'all'
                resultat.append(ord[index:] + ord[:index] + "all")
                break
        else:
            #Om inga vokaler hittas läggs all till ordet ändå
            resultat.append(ord + "all")

    return " ".join(resultat)


            
#Funktionen för fiksonspråket:
def fikonspråket(inrad):
    """ordet kuperas efter den första vokalen och "fi" läggs till i början och "kon" läggs till i slutet på det nya ordet"""
    vokaler = {'a', 'e', 'i', 'o', 'u', 'y', 'å', 'ä', 'ö', 'A', 'E', 'I', 'O', 'U', 'Y', 'Å', 'Ä', 'Ö'}
    resultat = []
    for ord in inrad.split():  #Vi delar upp strängen i ord
        for index, tkn in enumerate(ord): #med hjälp av enumerate funktionen kann vi iterera över alla tecken i strängen och hålla koll på dess position
            if tkn in vokaler:
                #skapar ordet med vokal-delen först, sedan konsonant-prefix och 'all'
                prefix = ord[:index + 1]
                suffix = ord[1 + index:]
                resultat.append("fi" + suffix + prefix + "kon")
                break
        else:
            #Om inga vokaler hittas läggs fi och kon till ordet ändå
            resultat.append("fi" + ord + "kon")

    return " ".join(resultat)



#Den avancerade menyn inbegrips i följande funktion: 
def avancerad_meny():
    """denna funktion är en meny som gör att användare kan välja språk. 
    Dena kan anropas antingen genom att skriva -m som argument där man vanligtvis anger 
    språket eller att skriva meny om man inte har angivit någon text"""

    while True: #while loopen läggs till eftersom användaren inte ska behöva starta om programmete varje gång han ska överesätta något nytt
        print("\nVälj Språk:")
        print("1. Stjärnspråket")
        print("2. Viskspråket")
        print("3. Rövarspråket")
        print("4. Översätt rövarspråket")
        print("5. Bebisspråket")
        print("6. Allspråket")
        print("7. Fikonspråket")
        print("8. Avsluta")

        användarens_val = input("Ange ditt val (1-8): ").strip() #användaren ska bestämma vilket språk som ska översättas till

        if användarens_val in [str(i) for i in range(1, 9)]: #vi ser till att vi bara fortsätter om användaren skriver ett tal från 1 till 8
            if användarens_val == "8":
                print("Avslutar menyn.")
                break

            sträng_att_översätta = input("Ange en sträng att översätta: ") #användar promptas om en sträng att översätta

            if användarens_val == "1":
                print(stjarnsprak2(sträng_att_översätta))
            elif användarens_val == "2":
                print(viskspråket(sträng_att_översätta))
            elif användarens_val == "3":
                print(rövarspråket(sträng_att_översätta))
            elif användarens_val == "4":
                print(översätt_rövarspråket(sträng_att_översätta))
            elif användarens_val == "5":
                print(bebisspråket(sträng_att_översätta))
            elif användarens_val == "6":
                print(allspråket(sträng_att_översätta))
            elif användarens_val == "7":
                print(fikonspråket(sträng_att_översätta))
        else:
            print("Ogiltigt val, försök igen.")
 


#Huvudfunktion som hanterar kommandoradsargumenten och kör det valda språket
def main():

    #skriver användaren -m så aktiveras den avancerade menyn
    if sys.argv[1] == "-m":
        avancerad_meny()
        return
    #om användaren inte förser funktionen med några giltiga argument händer följande:
    if len(sys.argv[1]) < 2:
        print("\nAnvänd programmet på det här sättet:")
        print("\n  -s  för stjärnspråket")
        print("  -v  för viskspråket")
        print("  -r  för rövarspråket")
        print("  -ö  för att översätta tillbaka rövarspråket")
        print("  -b  för bebisspråket")
        print("  -a  för allspråket")
        print("  -f  för fikonspråket")
        print("  -m  för avancerad meny (radera även frasen du vill översätta)\n")
        return
    
    #indata definieras över funktionen läs_indata()
    indata = läs_indata()

    #språket väljs baserat på användarens val i kommandot. Här tillkallas sedan funktionerna 1. "läs_indata()"" och 2.språkfunktionerna
    if sys.argv[1] == "-s": #sys.argv[0] hade returnerat filens namn
        print(stjarnsprak2(indata))
    elif sys.argv[1] == "-v":
        print(viskspråket(indata))
    elif sys.argv[1] == "-r":
        print(rövarspråket(indata))
    elif sys.argv[1] == "-ö":
        print(översätt_rövarspråket(indata))
    elif sys.argv[1] == "-b":
        print(bebisspråket(indata))
    elif sys.argv[1] == "-a":
        print(allspråket(indata))
    elif sys.argv[1] == "-f":
        print(fikonspråket(indata))
    else:
        print("\nDu angav ett okänt språk. Använd programmet på det här sättet:")
        print("\n  -s  för stjärnspråket")
        print("  -v  för viskspråket")
        print("  -r  för rövarspråket")
        print("  -ö  för att översätta tillbaka rövarspråket")
        print("  -b  för bebisspråket")
        print("  -a  för allspråket")
        print("  -f  för fikonspråket")
        print("  -m  för avancerad meny (radera även frasen du vill översätta)\n")

    

#Huvudfunktionen aktiveras direkt
if __name__ == "__main__":
    main()
