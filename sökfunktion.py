#Denna kod undersöker om ett ord som användar anger i terminalgränssnittet är befintligt i en lista



with open("ordlista.utf8", "r", encoding="utf8") as handle: 
    ord_lista = []
    for line in handle:
        for ord in line.split(): #varje rad delas upp i en lista av alla ord. Dessa ord är mellanslagsseparerade
            ord = ord.strip()  #extra white space i början eller slutet av ordet tas bort
            ord_lista.append(ord)



def linjarsok(v, ord):
    """Denna funktion linjärsöker genom att loopa igenom varje element i v"""
    for item in v:
        if item == ord: #Vi jämför varje ord i listan
            print(f"Ordet '{ord}' finns i listan.")
            return True
        
    #Om slutet av loopen nås men ordet inte hittas printas detta meddelande
    print(f"Ordet '{ord}' finns inte i listan.")
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



def funktionsval(användarens_ord, listan, användarens_funktion):
    """denna funktionn behandlar valet av funktionn för sökningen"""
    if användarens_funktion == '-l':
        linjarsok(listan, användarens_ord)
    elif användarens_funktion == '-b':
        if binarsok(listan, användarens_ord):
            print(f"Ordet '{användarens_ord}' finns i listan.")
        else:
            print(f"Ordet '{användarens_ord}' finns inte i listan.")
    else:
        print("Ditt val av funktion är inte giltigt, försök igen.")
        return False



def main():
    #denna del befattar sig med binarsok funktionen 
    användarens_ord = input("Ditt ord: ")
    användarens_funktion = input("Välj antingen '-l' för linjärsökning eller '-b' för binärsökning: ")
    ord_lista.sort() #Detta görs eftersom binärsökningen kräver det
    listan = ord_lista
    funktionsval(användarens_ord, listan, användarens_funktion)



if __name__ == '__main__':
    #först körs ett test och sedan anropas main
    testbinarsok()
    main()