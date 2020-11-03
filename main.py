# import matplotlib.pyplot as plt
#import pandas as ps
import numpy as np
import random
# from numba import jit, cuda
from timeit import default_timer as timer
from organisms import* # Imports all classes

# This script will be the master script


# All the treatments, being the total number of wolves re introduced
#treatments = [31, 11,  21, 41, 51]   
firstEvent  = [14,  5,  10, 18, 23]                # Numbers of wolves introduced on month 1 
secondEvent = [17,  6,  11, 23, 28]                # Numbers of wolves intoduced in the coming years 




# First thing we need to do is initialize the ecosystem to imitate the 1995 Greater Yellowstone ecosystem
# FIXME: Update function to fix where the things are pointing
def setInitState(fEvent):
    # First step in that, is creating all of the Aspen trees and Elk
    # The problem with that, is that as far as I can tell, no one counted all the aspen trees in yellowstone in 1995
    # That means I have to guess, and tune by parameters to make it acurate to real life
    # 190000 Aspen 
    # 19000 elk    742659 
    for _ in range(190000):
        Aspen()
    for _ in range(19000):
        Elk() 
    release(fEvent)

    # This whole block of code is for setting up the Aspen stats 
    for a in Aspen.aPopulation:
        height = round(np.random.normal(35, 10))
        while height < 0:                               # If the value is a negative, it's re rolled until positive
            height = round(np.random.normal(35, 10))
        a.height = height 

    # This block of code sets up the stats for the elk
    for a in Elk.ePopulation:
        age = round(np.random.normal(78, 40))
        while age < 0:                                  # If the value is negative, it's re rolled until positive
            age = round(np.random.normal(78, 40))
        a.ageM = age
        # The ages of the elk is a normal distribution, with a guesstimate standard deviation.
        


def release(q):
    j = len(Wolf.packs) 
    packQ = round(q / 7)
    while len(Wolf.packs) < packQ:
        Wolf.packs.append([])
    i = 0
    for _ in range(q):
        t = i % packQ
        h = t + j
        if len(Wolf.packs[h]) > 1: # FIXME: IndexError: list index out of range
            Wolf.packs[h].append(Wolf(h, 36, True, True))
        else:
            age = rdm.randint(9, 60)
            if age > 24:
                fertile = True
            else: 
                fertile = False
            Wolf.packs[h].append(Wolf(h, age, fertile, False))

        


def runMonth():
    for i in Aspen.aPopulation:
        i.nextMonth()
    print("\n\nASPEN DONE\n\n")
    for i in Elk.ePopulation:
        i.nextMonth()
    print("\n\nElk DONE\n\n")
    for pack in Wolf.packs:
        for w in pack:
            w.nextMonth()



    #TODO: Figure out how to run the Wolves, possibly utilise a dump list like Organism.population

# Resets the populations
def popsClear():
    Aspen.aPopulation.clear()
    Elk.ePopulation.clear()
    Wolf.packs.clear()
    Wolf.packs.append([])

# FIXME: use the real numbers to pix totals of initial and trickle wolves
# Also, pretend it took 13 months
# https://bit.ly/3kBDagl



# This version seems to give stable Elk numbers
# TODO: Start logging data and produce graphs for quick tweaking, 
# or at lease start writing to a file so I can graph as the program is running
for treatment in firstEvent:
    p2 = secondEvent[firstEvent.index(treatment)]
    for trials in range(3):                             # Number of trials per initial conditions
        popsClear()
        setInitState(treatment)
        for years in range(10):                         # Controls duration of years in experiment
            if years == 1:
                nIndex = firstEvent.index(treatment)
                sQ = secondEvent[nIndex]
                release(sQ)
            for months in range(12):                    # Makes it so theres 12 months in the year
                print('SUCESS')
                Organism.elapsedM += 1
                print ("month", Organism.elapsedM)
                start = timer()
                runMonth()
                print("There are currently ",len(Aspen.aPopulation), " Aspen")
                print("There are currently ", len(Elk.ePopulation), " Elk")
                print(round(timer()-start))
                


# There are currently  221842  Aspen
# There are currently  31040  Elk
# 226
# SUCESS
# month 20







# for i in Organism.population:
#     i.reproduce()

# # # mu, sigma = 35, 10
# s = np.random.normal(78, 40, 1000)

# count, bins, ignored = plt.hist(s, 30, density=True)
# # # # plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) *
# # # #                np.exp( - (bins - mu)**2 / (2 * sigma**2) ),
# # # #          linewidth=2, color='r')
# # # plt.plot(count)
# plt.show()
