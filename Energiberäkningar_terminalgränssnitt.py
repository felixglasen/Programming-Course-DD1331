import math
import random
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Solcell: 
    """klassen matas med dagen, area, soltalet och latituden och på filen skrivs alla väsentliga värden"""
    def __init__(self, area, soltal, latitud):
        """de viktiga variablerna definieras"""
        self.area = area
        self.soltal = soltal
        self.latitud = latitud



    def generera_W(self, dag):
        """här genereras energin per dag W som används i funktionerna för årsmedelproduktionen och filen med tabellen"""
        solighetsfaktor = round(random.uniform(0, 1), 1)
        W = round(self.area * self.soltal * solighetsfaktor * f(dag, self.latitud), 2)
        return solighetsfaktor, W



    def arsmedelproduktion(self):
        """Den årliga medelproduktionen returneras utifrån alla värden kopplade till self"""
        W_värden = []
        for dag in range(1, 361): 
            solighetsfaktor, W = self.generera_W(dag)
            W_värden.append(W)
        return round(sum(W_värden) / len(W_värden), 2)
    


    def fil_med_tabell(self):
        """Denna funktion skapar enn fil och matar den med en tabell"""
        månader = ["Januari", "Februari", "Mars", "April", "Maj", "Juni", "Juli", "Augusti", "September", "Oktober", "November", "December", "Januari"]
        with open("solkraftverk_data.txt", "w") as file:
            file.write("\nFormat: \nArea, soltal, latitud, dag, solighetsfaktor, f(t, latitud), W(t)\n-----------------------------------------------------------------\nJanuari")
            for dag in range(1, 361): 
                solighetsfaktor, W = self.generera_W(dag)
                if dag % 30 == 0: #denna implementering skapar en avgränsning i form utan månadens namn efter 30 dagar
                    månad_index = (dag // 30)
                    file.write(f"\n{månader[månad_index]}:")
                file.write(f"\n{self.area} {self.soltal} {self.latitud} {dag} {solighetsfaktor} {f(dag, self.latitud)} {W}")



class Vindturbin:
    """klassen matas med dagen, rotordiamtern och latituden och på filen skrivs alla väsentliga värden"""
    def __init__(self, rotordiameter, latitud):
        """definierar alla viktiga parametrar"""
        self.rotordiameter = rotordiameter
        self.latitud = latitud

        
    def generera_W(self, dag):
        """här genereras energin per dag W som används i funktionerna för årsmedelproduktionen och filen med tabellen"""
        vindfaktor = round(random.uniform(0, 1), 1)
        W = round(self.rotordiameter * vindfaktor * self.årstidsfaktor(dag) * f(dag, self.latitud) * 100, 2)
        return vindfaktor, W
    

    def årstidsfaktor(self, dag):
        """Beräknar årstidsfaktorn baserat på dagen"""
        if 60 <= dag < 150 or 240 <= dag <= 330:  # vår och höst
            return 1
        return 0.5  # sommar och vinter
            

    
    def arsmedelproduktion(self):
        """Den årliga medelproduktionen returneras utifrån alla värden kopplade till self"""
        W_värden = []
        for dag in range(1, 361): 
            vindfaktor, W = self.generera_W(dag)
            W_värden.append(W)
        return round(sum(W_värden) / len(W_värden), 2)
    


    def fil_med_tabell(self):
        """Denna funktion skapar enn fil och matar den med en tabell"""
        månader = ["Januari", "Februari", "Mars", "April", "Maj", "Juni", "Juli", "Augusti", "September", "Oktober", "November", "December", "Januari"]

        with open("vindkraftverk_data.txt", "w") as file:
            file.write("\nFormat: \nrotordiameter, latitud, dag, vindfaktor, årstidsfaktor, f(t, latitud), W(t)\n-----------------------------------------------------------------\nJanuari")
            for dag in range(1, 361): 
                vindfaktor, W = self.generera_W(dag)
                if dag % 30 == 0:
                    månad_index = (dag // 30)
                    file.write(f"\n{månader[månad_index]}:")
                file.write(f"\n{self.rotordiameter} {self.latitud} {dag} {vindfaktor} {f(dag, self.latitud)} {W}")




def användarens_latitud(latitud):
    """Denna funktion kontroller latitud inputen"""
    return 0 <= latitud <= 90



def användarens_rotordiameter(rotordiamter):
    """Denna funktion kontrollerar rotordiamter inputen"""
    return 25 <= rotordiamter <= 50


def f(dag, latitud): 
    """Denna funktion tar in vilken dag det är och latituden som anges av användaren"""
    v = (23.5 * math.sin(math.pi * (int(dag)-80) / 180) + 90 - latitud) / 90
    if 0 < v < 1:
        return round(v**2, 4)
    elif v >= 1:
        return 1
    elif v <= 0:
        return 0



def val_solcell():
    """om solcellen väljs ber programmet användaren om mer data och därefter genereas filen och årsmedelproduktionen"""
    while True:
        try:
            area = int(input(f"Ange area för solkraftverket (kvm): "))
            soltal = int(input("Ange soltal för solkraftverket (kWh/kvm): "))
            latitud = int(input("Ange en latitud för solkraftverket (mellan 0-90): "))
            if not användarens_latitud(latitud):
                print("Ange en latitud mellan 0-90")
                continue


            solcell = Solcell(area, soltal, latitud)
            print(f"Årsmedelproduktionen är: {solcell.arsmedelproduktion()} kW/dag")
            solcell.fil_med_tabell()
            print("Data har sparats i filen 'solkraftverk_data.txt'")
            break

        except ValueError:
            print("Var god ange arean, soltalet och latituden som heltal")



def val_vindturbin():
    """om vindturbinen väljs ber programmet användaren om mer data och därefter genereas filen och årsmedelproduktionen"""
    while True:
        try:
            rotordiameter = int(input(f"Ange rotordiameter (mellan 25m-50m): "))
            if not användarens_rotordiameter(rotordiameter):
                print("Ange en rotordiameter mellan (25m-50m): ")
                continue 

    
            latitud = int(input("Ange en latitud för vindturbinen (mellan 0-90): "))
            if not användarens_latitud(latitud):
                print("Ange en latitud mellan 0-90")
                continue

            vindturbin = Vindturbin(rotordiameter, latitud)
            print(f"Årsmedelproduktionen är: {vindturbin.arsmedelproduktion()} kW/dag")
            vindturbin.fil_med_tabell()
            print("Data har sparats i filen 'vindkraftverk_data.txt'")
            break

        except ValueError:
            print("Var god ange rotordiametern och latituden som heltal")
    




def main():
    """Huvudfunktion som hanterar val av kraftverkstyp"""
    while True:
        val_av_kraftverk = input("Ange '-s' för solkraftverk och '-v' för vindkraftverk: ")
        
        if val_av_kraftverk == "-s":
            val_solcell()
            break
        elif val_av_kraftverk == "-v":
            val_vindturbin()
            break
        else:
            print("Ogiltigt val. Försök igen.")



if __name__ == '__main__':
    main()