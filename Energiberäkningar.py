import math
import random
import statistics
import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from scipy.interpolate import UnivariateSpline


class Solcell: 
    """Denna klass returnerar en lista som kallas månadsdata som innehåller 12 listor med W-värden för varje dag. Denna lista används för att beräkna statistik. För att skapa denna lista behövs
    arean, soltalet och latituden."""
    def __init__(self, area, soltal, latitud):
        self.area = area
        self.soltal = soltal
        self.latitud = latitud

    def generera_W(self, dag):
        """Genererar energin per dag W som används i funktionerna för årsmedelproduktion och tabellen."""
        solighetsfaktor = round(random.uniform(0, 1), 1)
        W = round(self.area * self.soltal * solighetsfaktor * f(dag, self.latitud, "solkraftverk"), 2)
        return W

    def returnerar_månadsdata(self):
        """Returnerar en lista med tolv månadslistor, där varje lista innehåller W-värden för varje dag i månaden."""
        månadsdata = [] #den övergripande listan skapas först
        for månad in range(1, 13):
            månad_lista = []
            start_dag = (månad - 1) * 30 + 1
            slut_dag = månad * 30
            for dag in range(start_dag, slut_dag + 1): #man loopar igenom varje dag i en given månad
                W = self.generera_W(dag)
                månad_lista.append(W)
            månadsdata.append(månad_lista)
        return månadsdata


class Vindturbin:
    """Denna klass returnerar en lista som kallas månadsdata som innehåller 12 listor med W-värden för varje dag. Denna lista används för att beräkna statistik. För att skapa denna lista behövs
    rotordiametern och latituden"""
    def __init__(self, rotordiameter, latitud):
        self.rotordiameter = rotordiameter
        self.latitud = latitud

    def generera_W(self, dag):
        """Genererar energin per dag W baserat på vindfaktor och årstidsfaktor."""
        vindfaktor = round(random.uniform(0, 1), 1)
        W = round(self.rotordiameter * vindfaktor * self.årstidsfaktor(dag) * f(dag, self.latitud, "vindkraftverk") * 100, 2)
        return W
    
    def årstidsfaktor(self, dag):
        """beräknar årstidsfaktorn baserat på dagen"""
        if 60 <= dag < 150 or 240 <= dag <= 330:  #vår och höst
            return 1
        return 0.5  #sommar och vinter
    
    def returnerar_månadsdata(self):
        """Returnerar en lista med tolv månadslistor där varje lista innehåller W-värden för varje dag i månaden."""
        månadsdata = []
        for månad in range(1, 13):
            månad_lista = []
            start_dag = (månad - 1) * 30 + 1
            slut_dag = månad * 30
            for dag in range(start_dag, slut_dag + 1):
                W = self.generera_W(dag)
                månad_lista.append(W)
            månadsdata.append(månad_lista)
        return månadsdata


def beräkna_statistik(månadsdata, alternativ):
    """Returnerar specifik statistik (medelvärde, standardavvikelse, min, max) för varje månad baserat på valt alternativ."""
    resultat = []
    for månadslista in månadsdata:
        if alternativ == "medelvärde":
            resultat.append(round(statistics.mean(månadslista), 2)) #medelvärdet av alla tal i listan, rundat till 2 decimaler
        elif alternativ == "standardavvikelse":
            resultat.append(round(statistics.stdev(månadslista), 2))
        elif alternativ == "min":
            resultat.append(round(min(månadslista), 2))
        elif alternativ == "max":
            resultat.append(round(max(månadslista), 2))
    return resultat


def f(dag, latitud, kraftverk): 
    """Tar in vilken dag och latitud som anges av användaren"""
    v = (23.5 * math.sin(math.pi * (int(dag)-80) / 180) + 90 - latitud) / 90
    if kraftverk == "solkraftverk": #se metoden generera_W i båda klasser ovan, dessa ger antingen värdet solkraft eller vindkraft
        if 0 < v < 1:
            return round(v**2, 4)
        elif v >= 1:
            return 1
        elif v <= 0:
            return 0
    elif kraftverk == "vindkraftverk": 
        v_inverted = 1 - v #inverteringen görs eftersom det blåser mer runt polerna än ekvatorn
        if 0 < v_inverted < 1:
            return round(v_inverted**2, 4)
        elif v_inverted >= 1:
            return 1
        elif v_inverted <= 0:
            return 0



class Diagram:
    def __init__(self, area, soltal, latitud, rotordiameter=None, representation=0):
        """Denna klass definierar alla viktiga värden med hjälp av Solcells-klassen och Vindturbin-klassen och skapar diagrammet"""
        self.representation = representation
        #vi skapar Solcell eller Vindturbin objekt beroende på om rotordiameter är definierad
        if rotordiameter:
            self.vindturbin = Vindturbin(rotordiameter, latitud)
            self.solcell = None 
        else:
            self.solcell = Solcell(area, soltal, latitud)
            self.vindturbin = None  #om rotordiameter inte finns med definieras inte self.vindturbin

        #figuren och axlarna skapas först
        self.fig, self.ax = plt.subplots()
        plt.subplots_adjust(bottom=0.3) #figuren förskjuts också uppåt

        #metoderna anropas
        self.skapa_sliders()

        self.skapa_staplar()



    def skapa_sliders(self):
        """Denna funktion skapar alla sliders som ser till att man kan justera alla parametrar"""
        #positionen för sliders bestäms så att dem kan infogas i nästa steg
        ax_latitud = plt.axes([0.17, 0.15, 0.65, 0.03])
        ax_area = plt.axes([0.17, 0.10, 0.65, 0.03]) if self.solcell else None  # Om det är en vindturbin, ingen area-slider
        ax_rotordiameter = plt.axes([0.17, 0.05, 0.65, 0.03]) if self.vindturbin else None
        ax_soltal = plt.axes([0.17, 0.05, 0.65, 0.03]) if self.solcell else None

        #om det är en vindturbin, skapa en rotordiametern-slider istället för area
        #när en sliders värde ändras så anropas metoden uppdater som flörnyar diagrammet
        if self.vindturbin:
            self.rotordiameter_slider = Slider(ax_rotordiameter, 'Rotordiameter', 25, 50, valinit=37, valstep=1)
            self.rotordiameter_slider.on_changed(self.uppdatera)
        else:
            self.area_slider = Slider(ax_area, 'Area (m²) ', 1, 1000, valinit=500, valstep=1)
            self.soltal_slider = Slider(ax_soltal, 'Soltal', 1, 10, valinit=5, valstep=1)
            self.area_slider.on_changed(self.uppdatera)
            self.soltal_slider.on_changed(self.uppdatera)

        self.latitud_slider = Slider(ax_latitud, 'Latitud (°)', 1, 89, valinit=45, valstep=1)
        self.latitud_slider.on_changed(self.uppdatera)



    def skapa_staplar(self):
        """Skapar staplar för att visa medelvärde, min och max."""
        #först hämtar vi datat för medelvärde, min och max
        if self.solcell:
            månadsdata = self.solcell.returnerar_månadsdata()
        else:
            månadsdata = self.vindturbin.returnerar_månadsdata()

        #sedan beräknas all statistik med detta medelvärde
        medelvärden = beräkna_statistik(månadsdata, "medelvärde")
        minimum = beräkna_statistik(månadsdata, "min")
        maximum = beräkna_statistik(månadsdata, "max")

        #här definieras stapeldiagrammet med alla tre staplar.
        bar_width = 0.4
        self.stapel_plot = self.ax.bar(range(1, 13), medelvärden, bar_width, color='skyblue', label="Medelvärde")
        self.min_stapel = self.ax.bar(np.arange(1, 13) - bar_width / 2, minimum, bar_width / 4, color='#B0B0B0', label="Min")
        self.max_stapel = self.ax.bar(np.arange(1, 13) + bar_width / 2, maximum, bar_width / 4, color='grey', label="Max")

        self.ax.set_ylim(0, 1500)

        self.ax.set_xlabel('Månad') #vi skapar också en titel för varje del i figuren
        self.ax.set_ylabel('Energiproduktion (W)')
        if self.solcell:
            self.ax.set_title('Energiproduktion för en Solkraftverk')
        else: 
            self.ax.set_title('Energiproduktion för en Vindkraftverk')
        self.ax.legend()



    def uppdatera(self, val):
        """Uppdaterar diagrammet när någon slider ändras."""
        if self.solcell:
            self.solcell.area = self.area_slider.val #utifrån vilket värde som väljs med sliderna matas solcells funktionen med olika värden
            self.solcell.soltal = self.soltal_slider.val
            self.solcell.latitud = self.latitud_slider.val
            månadsdata = self.solcell.returnerar_månadsdata() #Igenom Solcells-klassen hämtas månadsdatan (W-värdena) och sedan används berkna statistik funktionen för att skapa all data för diagrammet
        else:
            self.vindturbin.rotordiameter = self.rotordiameter_slider.val
            self.vindturbin.latitud = self.latitud_slider.val
            månadsdata = self.vindturbin.returnerar_månadsdata() 

        medelvärden = beräkna_statistik(månadsdata, "medelvärde")
        standardavvikelse = beräkna_statistik(månadsdata, "standardavvikelse")
        minimum = beräkna_statistik(månadsdata, "min")
        maximum = beräkna_statistik(månadsdata, "max")

        #för varje element i stapel_plot, min_stapel, och max stapel sätts höjden till medelvärde min och max
        if self.representation == 0: #om användaren har valt diagram, så körs följande kod
            for i, bar in enumerate(self.stapel_plot):
                bar.set_height(medelvärden[i])
            for i, bar in enumerate(self.min_stapel):
                bar.set_height(minimum[i])
            for i, bar in enumerate(self.max_stapel):
                bar.set_height(maximum[i])
            for artist in self.ax.collections:
                artist.remove()
            self.ax.set_ylim(0, 1500) #vi definierar y-axelns skalering
            self.fig.canvas.draw_idle()

        else: 
            for i, månad in enumerate(range(12)): #om användaren har valt tabell körs följande kod
                self.table._cells[(i + 1, 1)]._text.set_text(f"{medelvärden[månad]:.2f}")
                self.table._cells[(i + 1, 2)]._text.set_text(f"{standardavvikelse[månad]:.2f}")
                self.table._cells[(i + 1, 3)]._text.set_text(f"{minimum[månad]:.2f}")
                self.table._cells[(i + 1, 4)]._text.set_text(f"{maximum[månad]:.2f}")
        
            self.fig.canvas.draw_idle()


    def show(self):
        """Till sist visas det skapade diagrammet"""
        plt.show()


class Tabell(Diagram):
    def __init__(self, area, soltal, latitud, rotordiameter=None, representation=1):
        """Tabellklass som ärver från Diagramm, visar data i tabellform istället för diagram. Tabelklassen har tillgång till alla metoder som finns i basklassen"""
        self.representation = representation
        super().__init__(area, soltal, latitud, rotordiameter) #initfunktionen hämtas från Diagramklassen
        representation = "tabell"
        self.skapa_tabell()

    def skapa_tabell(self):
        """Skapar en tabell som visar medelvärde, standardavvikelse, max och min värden för varje månad"""
        #först hämtar vi datat för medelvärde, min och max
        if self.solcell:
            månadsdata = self.solcell.returnerar_månadsdata()
        else:
            månadsdata = self.vindturbin.returnerar_månadsdata()
        
        #sedan beräknas all statistik med detta medelvärde
        medelvärden = beräkna_statistik(månadsdata, "medelvärde")
        standardavvikelse = beräkna_statistik(månadsdata, "standardavvikelse")
        minimum = beräkna_statistik(månadsdata, "min")
        maximum = beräkna_statistik(månadsdata, "max")
        
        #vi skapar tabellens innehåll med titlar för varje kolumn
        kolumn_titlar = ["Månad", "Medelvärde (W)", "Standardavvikelse (W)", "Min (W)", "Max (W)"]
        kolumn_data = []
        månader = ["Januari", "Februari", "Mars", "April", "Maj", "Juni", "Juli", "Augusti", "September", "Oktober", "November", "December"]

        #loopa igenom varje månad och bygg tabellen, i är indexet som representerar månaden
        for i, månad in enumerate(månader):
            månadens_data = [månad, medelvärden[i], standardavvikelse[i], minimum[i], maximum[i]]
            kolumn_data.append(månadens_data)


        
        #vi rensar alla gamla objekt och skapar sedan nya
        self.ax.clear()
        self.ax.axis("tight") #justerar axlarnas gränser
        self.ax.axis("off") #tar bort axlarna och koordinater
        
        #här skapas tabellen med dess specifikationer
        self.table = self.ax.table(cellText=kolumn_data, colLabels=kolumn_titlar, loc="center", bbox=[-0.12, -0.06, 1.2, 1])

                           
        #denna for loop justerar dem enskilda cellernas storlek
        for cell in self.table.get_celld().values():
            cell.set_width(0.25) 
            cell.set_height(0.1)
        #vi skapar också en titel
        if self.solcell:
            self.ax.set_title('Energiproduktion för ett Solkraftverk')
        else: 
            self.ax.set_title('Energiproduktion för ett Vindkraftverk')
        self.fig.canvas.draw_idle() #med denna implementering ritar vi om canvasen efter att tabellen har skapats


    def uppdatera(self, val):
        """Anropas via Diagramklassens uppdatera-metod"""
        super().uppdatera(val) #vi anropar uppdatera metoden i basklassen Diagram

        #skapa_tabell anropas för att uppdatera tabellens data
        self.skapa_tabell()
        
    def show(self):
        """Visar tabellen."kan """
        plt.show()



def starta_tkinter():
    """Denna funktion öppnar upp ett fönster med radioknappar och en knapp som kör programmet"""

    #vi kallar vårat fönster för "root" och ger det dimensioner och en titel
    root = tk.Tk()
    root.geometry("600x400")
    root.title("Energiberäkningar för Kraftverk")

    #detta är en överskrift över radioknapparna
    label = tk.Label(root, text="Välj ditt kraftverk", font=('Calibri', 18))
    label.pack(padx=20, pady=20)

    #Intvar binder värdet för radioknappen
    kraftverk_var = tk.IntVar(value=0) #värde 0 så att solkraftverk är markerad från början. Detta är godtyckligt och hade kunnat vara 1

    radio1 = tk.Radiobutton(root, text="Solkraftverk", font=('Calibri'), variable=kraftverk_var, value=0) #solkraftverket tillskrivs värdet 0, egentligen bestäms denna förbindelse först i "check" funktionen
    radio1.pack(padx=10, pady=10)
    radio2 = tk.Radiobutton(root, text="Vindkraftverk", font=('Calibri'), variable=kraftverk_var, value=1)
    radio2.pack(padx=10, pady=10)

    label2 = tk.Label(root, text="Välj hur du vill representera din data", font=('Calibri', 18))
    label2.pack(padx=20, pady=20)

    representation_var = tk.IntVar(value=0) 

    radio3 = tk.Radiobutton(root, text="Grafiskt", font=('Calibri'), variable=representation_var, value=0)
    radio3.pack(padx=10, pady=10)
    radio4 = tk.Radiobutton(root, text="Tabellariskt", font=('Calibri'), variable=representation_var, value=1)
    radio4.pack(padx=10, pady=10)

    #skapar en knapp innuti en buttonframe som ligger i root
    buttonframe = tk.Frame(root)
    buttonframe.columnconfigure(0, weight=1) #med denna implementering blir skalering oproblematiskt
    btn3 = tk.Button(buttonframe, text="Kör programmet", font=('Calibri'), 
                     command=lambda: aktivera_matplotlib(representation_var, kraftverk_var)) #med hjälp av lambda körs funktionen check först efter att knappen har klickats
    btn3.grid(row=1, column=0, columnspan=2,)

    #justerar positionen av knappen
    buttonframe.pack(fill='x', padx=30, pady=10)

    root.mainloop() #denna inbyggda funktion öppnar förnstret och håller det öppet



def aktivera_matplotlib(representation_var, kraftverk_var):
    """Beroende på vilka värden som radioknapparna har så anropas olika klasser med olika argument"""
    if representation_var.get() == 0 and kraftverk_var.get() == 0: #grafiskt, solkraftverk #get hämtar värdet för knapparna
        diagram = Diagram(area=500, soltal=5, latitud=45, representation=0)
        diagram.show()
    elif representation_var.get() == 0 and kraftverk_var.get() == 1: #grafiskt, vindkraftverk
        diagram = Diagram(area=None, soltal=None, latitud=45, rotordiameter=37, representation=0)
        diagram.show()
    elif representation_var.get() == 1 and kraftverk_var.get() == 0: #tabellariskt, solkraftverk
        tabell = Tabell(area=500, soltal=5, latitud=45, representation=1)
        tabell.show()
    elif representation_var.get() == 1 and kraftverk_var.get() == 1: #tabellariskt, vindraftverk
        tabell = Tabell(area=None, soltal=None, latitud=45, rotordiameter=37,representation=1)
        tabell.show()
                        


def main():
    """Huvudfunktion som startar tkinter"""
    starta_tkinter()


if __name__ == '__main__':
    main()
    main()