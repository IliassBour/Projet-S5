import numpy as np

class Constant(object):
    rayon= 1 #métre
    angle_max=8.21 #degrée
    pourcentage_angle=0.75

    largeur_roue = 0.134 #métre (track_withd)
    longueur_roue = 0.25 #métre (wheelbase)

def vitesseMax(a_max):
    d1 = 0.3
    d2 = 0.1
    s= np.sqrt((d1-d2)/a_max)
    return (d1-d2)/s

def rayonRoue(a_max):
    angle_int = np.arctan(Constant.longueur_roue/(Constant.rayon-Constant.largeur_roue/2))
    angle_ext = np.arctan(Constant.longueur_roue/(Constant.rayon+Constant.largeur_roue/2))
    moy_angle = (angle_int+angle_ext)/2
    return np.rad2deg(moy_angle)

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