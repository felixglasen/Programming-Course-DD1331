from tkinter import *
from math import sqrt

BREDD = 800
HÖJD = 600



def normaliserad_till_pixel(n: float) -> int:
    """funktionen konverterar ett normaliserat värde "n" som exempelvis "0.2" till ett pixelvärde"""
    return int(n * BREDD)



def normaliserad_till_pixel_y(n: float) -> int:
    """funktionen konverterar ett normaliserat värde "n" som exempelvis "0.2" till ett pixelvärde"""
    return int(n * HÖJD)



def ifylld_rektangel(img, övre_vänster_hörn: tuple[float, float], nedre_höger_hörn: tuple[float, float], färg: str="#ffffff"): #här används typhantering. tjockleken ska vara en int och färgen en string
    """Denna funktione ritar en ifylld rektangel i img. Mata funktionen med imagen, dem normaliserade koordinaterna och en färg"""

#nedan används en for loop för att loopa igenom varje pixel på y-planet för varje pixel på x-planet och sedan fylla i den med den givna färgen
    for x_koordinat in range(normaliserad_till_pixel(övre_vänster_hörn[0]), normaliserad_till_pixel(nedre_höger_hörn[0])):
        for y_koordinat in range(normaliserad_till_pixel_y(övre_vänster_hörn[1]), normaliserad_till_pixel_y(nedre_höger_hörn[1])):
            img.put(färg, (x_koordinat, y_koordinat))



def ram_till_rektangel(img, övre_vänster_hörn: tuple[float, float], nedre_höger_hörn: tuple[float, float], tjocklek: int=1, färg: str="#000000"):
    """"Denna funktion ritar en ram i rektangelform"""
    
    #först och främst konverteras alla normaliserade värden till pixelvärden
    övre_vänster_x = normaliserad_till_pixel(övre_vänster_hörn[0])
    övre_vänster_y = normaliserad_till_pixel_y(övre_vänster_hörn[1])
    nedre_höger_x = normaliserad_till_pixel(nedre_höger_hörn[0])
    nedre_höger_y = normaliserad_till_pixel_y(nedre_höger_hörn[1])

    #denna loop ritar dem horisontella delarna av ramen
    for x_koordinat in range(övre_vänster_x, nedre_höger_x):
        for x_ram in range(tjocklek):
            img.put(färg, (x_koordinat, övre_vänster_y + x_ram)) #övre delen
            img.put(färg, (x_koordinat, nedre_höger_y - x_ram - 1)) #undre delen #-1 för att vi vill att ramen inte ska överlappas med rektangeln

    #denna loop ritar dem vertikala delarna av ramen
    for y_koordinat in range(övre_vänster_y, nedre_höger_y):
        for y_ram in range(tjocklek):
            img.put(färg, (övre_vänster_x + y_ram, y_koordinat)) #vänstra delen
            img.put(färg, (nedre_höger_x - y_ram - 1, y_koordinat)) #högra delen #-1 för att vi vill att ramen inte ska överlappas med rektangeln






def triangelns_area(hörn_1, hörn_2, hörn_3):
    """denna funktion beräknar trinagelns area utifrån koordinaterna för hörnen"""
    #vi beräknar först triangelns sidor a, b och c för att kunna sätta in dessa i herons formel
    #för att beräkna a, b och c används avståndsformeln (från pythagoras sats)
    a = sqrt((hörn_1[0] - hörn_2[0])**2 + (hörn_1[1] - hörn_2[1])**2)
    b = sqrt((hörn_2[0] - hörn_3[0])**2 + (hörn_2[1] - hörn_3[1])**2)
    c = sqrt((hörn_3[0] - hörn_1[0])**2 + (hörn_3[1] - hörn_1[1])**2)
  
    #nu tillämpar vi herons formel och returnerar ytan
    s = (a + b + c) / 2
    ytan = sqrt(s * abs(s - a) * abs(s - b) * abs(s - c)) #här används absolutbeloppet eftersom eftersom sträckorna ska vara positiva och riktningen inte ska spela roll
    return ytan #ytan returneras och skickas till "punkt_i_triangel" funktionen



def punkt_i_triangel_gran(punkt, hörn_1, hörn_2, hörn_3, eps=0.0001):
    """Funktionen kontrollerar om en punkt ligger i triangeln. Funktionenn matas med hörnen och en punkt."""
    #i det första steget används funktionen "triangelns_area" för att beräkna dem olika delytorna
    A = triangelns_area(hörn_1, hörn_2, hörn_3) 
    A1 = triangelns_area(punkt, hörn_2, hörn_3)
    A2 = triangelns_area(hörn_1, punkt, hörn_3)
    A3 = triangelns_area(hörn_1, hörn_2, punkt)

    #i det andra steget jämförs A med dem övriga areorna
    if abs(A - A1 - A2 - A3) < eps: 
       return True  
    else: 
        return False



def rita_trianglar(img, hörn_1, hörn_2, hörn_3, barrens_färg):
    """Ritar en ifylld triangel för granen"""
    #vi börjar med att loopa genom varje punkt i canvasen
    for x_koordinat in range(BREDD):
        for y_koordinat in range(HÖJD):
            punkt = (x_koordinat / BREDD, y_koordinat / HÖJD) #här konverteras pixelvärdet till det normaliserade värdet för att kunna användas i "punkt_i_triangel" funktionen
            if punkt_i_triangel_gran(punkt, hörn_1, hörn_2, hörn_3): #punkt_i_triangel returnerar true om punkte är i triangeln och annars false. För True får dne pixeln en färg
                img.put(barrens_färg, (x_koordinat, y_koordinat))






def rita_gran(img, granens_övre_vänster_hörn: tuple[float, float], granens_höjd: (float), granens_bredd: (float), barrens_färg: str="#008000", fotens_färg: str="#8B4513"):
    """denna funktion ritar en gran utifrån koordinaterna för granens övre hörn, som ligger utanför granen, granens höjd, bredd och färg. Granen ritas igenom att sammanfoga tre trianglar och en rektangel"""
    #nedan definieras rektangelns hörn utifrån granens hörn, höjd och bredd. Sedan anropas ifylld_rektangel funktionen
    rektangel_övre_hörn = (granens_övre_vänster_hörn[0] + granens_bredd * 0.3, granens_övre_vänster_hörn[1] + granens_höjd * 0.75)
    rektangel_undre_hörn = (granens_övre_vänster_hörn[0] + granens_bredd * 0.7, granens_övre_vänster_hörn[1] + granens_höjd * 1.25)
    ifylld_rektangel(img, rektangel_övre_hörn, rektangel_undre_hörn, fotens_färg)

    #sedan bestämmer vi tupler för koordinaterna av trianglarnas hörn
    for i in range(0, 3):  #ritar tre trianglar för granen

        #och definierar dem tre hörnen av triangeln utifrån granens hörn, bredden och höjden:
        vänster_hörn = (granens_övre_vänster_hörn[0]), granens_övre_vänster_hörn[1] + granens_höjd * (i/3+0.25)
        mitten_hörn = (granens_övre_vänster_hörn[0] + granens_bredd / 2, granens_övre_vänster_hörn[1] + granens_höjd * 0.15 * i)
        höger_hörn = (granens_övre_vänster_hörn[0]) + granens_bredd, granens_övre_vänster_hörn[1] + granens_höjd * (i/3+0.25)
        #notera att värden 0.33 används istället för 0.25 eftersom 0.25*0.75 = 0.33, mitt fönster är i y led begränsat till 0.75

        #dessa värden skickas vidare till rita_trianglar funktionen
        rita_trianglar(img, vänster_hörn, mitten_hörn, höger_hörn, barrens_färg)






def punkt_i_cirkel(mittpunkt_x, mittpunkt_y, radie, x_koordinat, y_koordinat):
    """Funktionen kontrollerar om en punkt ligger i cirkeln. Funktionenn matas mned cirkelns mittpunkt, radien och en x och y koordinat."""
    
    #cirkelns formel avnänds för kontrollen
    if ((x_koordinat - mittpunkt_x)**2 + (y_koordinat - mittpunkt_y)**2) <= radie**2:
       return True  
    else: 
        return False
    


def ifylld_cirkel(img, cirkelns_mittpunkt: tuple[float, float], radie: int=1, färg: str="#ffffff"):
    """denna funktion ritar en cirkel utifrån koordinaterna för cirkelns mittpunkt, readien och färgen"""

    #först konverteras normaliserade värdet till pixelvärdet för att sedan kunna mata "punkt_i_cirkel" funktionen
    mittpunkt_x = int(cirkelns_mittpunkt[0] * BREDD)
    mittpunkt_y = int(cirkelns_mittpunkt[1] * HÖJD)

    for x_koordinat in range(BREDD): 
        for y_koordinat in range(HÖJD):
            punkt = (x_koordinat / BREDD, y_koordinat / HÖJD) #här konverteras pixelvärdet till det normaliserade värdet för att kunna användas i "punkt_i_" funktionen
            if punkt_i_cirkel(mittpunkt_x, mittpunkt_y, radie, x_koordinat, y_koordinat): #punkt_i_cirkel returnerar true om punkte är i cirkeln och annars false. För True får den pixeln en färg
                img.put(färg, (x_koordinat, y_koordinat))






def main():
    """denna funktion skapar ett fönster och beskriver logiken för att fylla i den geometriska formen"""
    window = Tk() #detta anropar Tkinter-biblioteket att skapa fönstret
    canvas = Canvas(window, width=BREDD, height=HÖJD, bg="#000000") #detta skapar en rityta, här är window fönstret där ritytan placeras
    canvas.pack() #ritytan placeras här i fönstret, så den är synlig
    img = PhotoImage(width=BREDD, height=HÖJD) #PhotoImage skapar ett bildobjekt som lagras i variabeln imgber
    canvas.create_image((BREDD // 2 , HÖJD // 2), image=img, state="normal") #img ritas i mitten av canvasen. State=normal innebär att bilden modifieras normalt, när rektangeln ritas på den. 

    #nedan andropas samtliga funktioner för att rita bilden
    ifylld_rektangel(img, (0.0, 0.0), (1.0, 0.5), "#000435") #gräset
    ifylld_rektangel(img, (0.0, 0.5), (1.0, 1.0), "#004038") #himlen
    ifylld_cirkel(img, (0.85, 0.20), 80, "#F6F1D5") #månen, den synbara delen
    ifylld_cirkel(img, (0.80, 0.24), 80, "#000435") #månen, den delen med samma färg som himlen
    ifylld_rektangel(img, (0.6, 0.4), (0.9, 0.7), "#801818") #huset 
    rita_trianglar(img, (0.6, 0.4), (0.75, 0.25), (0.9, 0.4), "#000000") #taket
    ram_till_rektangel(img, (0.63, 0.45), (0.73, 0.53), 4, "#000000") #fönstret
    ifylld_rektangel(img, (0.77, 0.45), (0.87, 0.68), "#422013") #dörren
    rita_gran(img, (0.15, 0.05), 0.4, 0.2, "#004038", "#422013" ) #granen

    mainloop() #startar en händelseloop som ser till att fönstret hålls öppet i Tkinter



if __name__ == '__main__': #detta ser till att filen inte körs när den importeras som modul. Då sätts inte __name__ till '__main__' som när den körs i terminalen
    main() #main-funktionen anropas