import numpy as np

class Constant(object):
    rayon= 0.14
    angle_max=8.21
    pourcentage_angle=0.75


def vitesseMax(a_max):
    d1 = 0.3
    d2 = 0.1
    s= np.sqrt((d1-d2)/a_max)
    return (d1-d2)/s

def rayonRoue():
    return 0

def calculTrajet():
    #Avance
    d = []
    t = []

    #Arret

    #Tournant droit

    #Tournant gauche

    return 0

if __name__ == '__main__':
    calculTrajet()