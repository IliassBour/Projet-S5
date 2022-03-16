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
        accTotTemp = np.sqrt(np.power(acc, 2) + np.power(acc, 4)/np.power(rayon, 2))
        if accTotTemp < accMax :
            accTot = accTot
            accTanFinal = acc
        else :
            break
    accNormFinal = np.power(accTanFinal, 2)/rayon
    return accTanFinal, accNormFinal

def ligneDroiteAvance(xInital, yInitial, vInitial, distance, axe, signe):
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
        xPosActuel += signe*vitesseActuel*deltaT
        array[axe].append(xPosActuel)
        array[np.mod(axe + 1, 2)].append(yPosActuel)

    return array, vitesseActuel

def ligneDroiteArreter(pos_init, axe, signe):
    a_max = signe*getAccelerationMax()
    v_max = signe*vitesseMax(a_max)
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

def rotation(x, y):
    matricePassage = np.array([[0, 1], [-1, 0]])
    coordonner = np.array([[x], [y]])
    matriceRotation = np.matmul(matricePassage.T, coordonner)
    return matriceRotation[0][0], matriceRotation[1][0]

def getTournant(xInitial, yInitial, vitesseInitial, rayon, sens, orientation):
    accMaxTan, _ = getAccelerationTournant(rayon, getAccelerationMax())
    vitesseMaxTan = vitesseMax(accMaxTan)
    d = 0
    vitesseActuel = vitesseInitial
    deltaT = 0.01
    angleRadiant = 0
    array = [[xInitial], [yInitial]]
    xPosActuel = xInitial
    yPosActuel = yInitial
    dernierX = 0
    dernierY = 0
    while angleRadiant < np.pi / 2:

        derniereVitesse = vitesseActuel
        if vitesseActuel > vitesseMaxTan:
            if (vitesseActuel - vitesseMaxTan) / deltaT > accMaxTan:
                vitesseActuel = vitesseActuel - accMaxTan * deltaT
            else:
                vitesseActuel = vitesseMaxTan

        elif vitesseActuel < vitesseMaxTan:
            if (vitesseMaxTan - vitesseActuel) / deltaT > accMaxTan:
                vitesseActuel = vitesseActuel + accMaxTan * deltaT
            else:
                vitesseActuel = vitesseMaxTan

        angleRadiant += 0.5*(derniereVitesse+vitesseActuel)*deltaT/rayon

        yPosActuel = rayon * np.sin(angleRadiant)+yInitial

        if sens == 1:
            xPosActuel = -1*(rayon - rayon * np.cos(angleRadiant))+xInitial
        else:
            xPosActuel = rayon - rayon * np.cos(angleRadiant)+xInitial

        dernierX = xPosActuel
        dernierY = yPosActuel

        #Changement d'orientation
        if orientation == 1:
            xPos, yPos = rotation(xPosActuel, yPosActuel)
        elif orientation == 2:
            xPos, yPos = rotation(xPosActuel, yPosActuel)
            xPos, yPos = rotation(xPos, yPos)
        elif orientation == 3:
            xPos, yPos = rotation(xPosActuel, yPosActuel)
            xPos, yPos = rotation(xPos, yPos)
            xPos, yPos = rotation(xPos, yPos)
        else:
            xPos = xPosActuel
            yPos = yPosActuel

        array[0].append(xPos)
        array[1].append(yPos)

    return array

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
    ligneDroiteArreter([0, 0], 0, 1)
    getTournant(0,0, 0.65, 1, 0, 3)