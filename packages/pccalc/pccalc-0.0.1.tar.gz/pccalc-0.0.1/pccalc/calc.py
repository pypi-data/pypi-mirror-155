#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import tkinter as tk: 

def calc (): 
    
    measurement_gL = 0
    concentration_mL = 0 
    mol_concentration_uM = 0
    stock_amount = 0
    water_amount = 0 
    
    def show_entry_fields():
        print("Quantification (ug/mL): %s\nStock Molar Mass (g/mol): %s\nDesired Concentration (uM): %s\nDesired Volume (uL): %s" % (e1.get(), e2.get(), e3.get(), e4.get()))

    def primer_calculations (): 
        #measurement - original value in (ug/mL) from the QIAExpert 
        #weight - molecular weight (g/mol) 
        #desired concentration - (uM) 
        #final volume - (uL) 
        measurement = float(e1.get())
        weight = float(e2.get())
        desired_concentration = float(e3.get())
        desired_volume = float(e4.get())
        measurement_gL = float(measurement) * 10 ** -3 #changes units to g/L 
        concentration_mL = measurement_gL / weight #finds Molar Concentration (mol/L) 
        mol_concentration_uM = concentration_mL / (10 ** -6)
        stock_amount = (desired_concentration * desired_volume) / mol_concentration_uM 
        water_amount = desired_volume - stock_amount
        print("The molar concentration of primers in your solute is " + str(round(concentration_mL, 9)) + " mols/L")
        print("Add " + str(round(stock_amount, 3)) + " uL stock and " + str(round(water_amount, 3)) + " uL water.")


    master = tk.Tk()
    tk.Label(master, 
             text="Quantification (ug/mL)").grid(row=0)
    tk.Label(master, 
             text="Stock Molar Mass (g/mol)").grid(row=1)
    tk.Label(master, 
             text="Desired Concentration (uM)").grid(row=2)
    tk.Label(master, 
             text="Desired Volume (uL)").grid(row=3)


    e1 = tk.Entry(master)
    e2 = tk.Entry(master)
    e3 = tk.Entry(master)
    e4 = tk.Entry(master)

    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)
    e3.grid(row=2, column=1)
    e4.grid(row=3, column=1)


    tk.Button(master, 
              text='Show Inputs', command=show_entry_fields).grid(row=4, 
                                                           column=0, 
                                                           sticky=tk.W, 
                                                           pady=4)

    tk.Button(master, 
              text='Calculate', command=primer_calculations).grid(row=4, 
                                                           column=1, 
                                                           sticky=tk.W, 
                                                           pady=4)

    tk.mainloop()


calc ()

