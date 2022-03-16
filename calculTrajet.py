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
    v= np.sqrt(2*(d1-d2)*a_max)
    return v

def rayonRoue(a_max):
    angle_int = np.arctan(Constant.longueur_roue/(Constant.rayon-Constant.largeur_roue/2))
    angle_ext = np.arctan(Constant.longueur_roue/(Constant.rayon+Constant.largeur_roue/2))
    moy_angle = (angle_int+angle_ext)/2
    return np.rad2deg(moy_angle)

def getAccelerationMax():
    return 9.8 * np.cos(np.pi/2 - Constant.angle_max * Constant.pourcentage_angle * np.pi/180)/np.cos(Constant.angle_max * Constant.pourcentage_angle * np.pi/180)

def getAccelerationTournant(rayon, accMax):
    accTot = 0
    accTanFinal = 0
    for accTan in range(0, 200):
        acc = accTan*0.01
        accTotTemp = np.sqrt(acc^2 + acc^4/rayon^2)
        if accTotTemp < accMax :
            accTot = accTot
            accTanFinal = acc
        else :
            break
    accNormFinal = accTanFinal^2/rayon
    return accTanFinal, accNormFinal

def ligneDroiteAvance(xInital, yInitial, vInitial, distance):
    accMax = getAccelerationMax()
    vMax = vitesseMax(accMax)
    array = [[xInital], [yInitial]]
    d = 0;
    vitesseActuel = vInitial
    xPosActuel = xInital
    yPosActuel = yInitial
    deltaT = 0.01
    while d < distance:

        if vitesseActuel > vMax:
            if (vitesseActuel - vMax)/deltaT > accMax:
                vitesseActuel = vitesseActuel - accMax*deltaT
            else:
                vitesseActuel = vMax

        elif vitesseActuel < vMax:
            if (vMax-vitesseActuel)/deltaT > accMax:
                vitesseActuel = vitesseActuel + accMax*deltaT
            else:
                vitesseActuel = vMax

        d += vitesseActuel*deltaT
        xPosActuel += vitesseActuel*deltaT
        array[0].append(xPosActuel)
        array[1].append(yPosActuel)

    return array, vitesseActuel

def ligneDroiteArreter(pos_init, axe):
    a_max = getAccelerationMax()
    v_max = vitesseMax(a_max)
    vitesseActuel = v_max
    distance = [[], []] # [x, y]
    index = 0
    deltaT = 0.01

    while vitesseActuel > 0:
        distance[np.mod(axe + 1, 2)].append(pos_init[np.mod(axe + 1, 2)])
        vitesseActuel = vitesseActuel - a_max * deltaT

        if index == 0:
            distance[axe].append(pos_init[axe])
        else:
            distance[axe].append(distance[axe][index - 1] - a_max * np.power(deltaT, 2) / 2 + vitesseActuel * deltaT)
        index += 1

    return distance



def calculTrajet():
    #Avance
    d = []
    t = [] #seconde

    #Arret

    #Tournant droit

    #Tournant gauche

    return 0

if __name__ == '__main__':
    calculTrajet()
    ligneDroiteArreter([0, 0], 0)