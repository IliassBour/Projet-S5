import numpy as np
import pandas as pd
import xlsxwriter

class Constant(object):
    rayon= 1 #métre
    angle_max=8.21 #degrée
    pourcentage_angle=0.75
    rayon_socle = 0.14 #métre
    largeur_roue = 0.134 #métre (track_withd)
    longueur_roue = 0.25 #métre (wheelbase)
    deltaT = 1/60
    coefficient_friction = 0.25

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
    if axe==1:
        xPosActuel = yInitial
        yPosActuel = xInital
    else:
        xPosActuel = xInital
        yPosActuel = yInitial

    deltaT = Constant.deltaT
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

def ligneDroiteArreter(pos_init, axe, signe): #axe entre 0 (x) et 1 (y), signe entre -1 (arière) et 1 (avant)
    a_max = getAccelerationMax()
    v_max = vitesseMax(a_max)
    vitesseActuel = signe*v_max
    a_max *= signe
    distance = [[], []] # [x, y]
    index = 0
    deltaT = Constant.deltaT

    while signe*vitesseActuel > 0:
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
    deltaT = Constant.deltaT
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

        #Changement d'orientation
        if orientation == 1:
            xPos, yPos = rotation(xPosActuel-xInitial, yPosActuel-xInitial)
        elif orientation == 2:
            xPos, yPos = rotation(xPosActuel, yPosActuel)
            xPos, yPos = rotation(xPos, yPos)
        elif orientation == 3:
            xPos, yPos = rotation(xPosActuel-xInitial, yPosActuel+xInitial)
            xPos, yPos = rotation(xPos, yPos)
            xPos, yPos = rotation(xPos, yPos)
        else:
            xPos = xPosActuel
            yPos = yPosActuel

        array[0].append(xPos)
        array[1].append(yPos)

    return array, vitesseActuel

def billeAccelere(xInitial, yInitial, zInitial, acceleration, temps, axe, signe):  #axe entre 0 (x) et 1 (y), signe entre -1 (arière) et 1 (avant)
    g=9.81
    position = [[xInitial], [yInitial], [zInitial]]
    h_max = Constant.rayon_socle-Constant.rayon_socle*np.sin(Constant.angle_max*Constant.pourcentage_angle)
    l=Constant.rayon_socle*np.cos(Constant.angle_max*Constant.pourcentage_angle)
    vitesseActuelle = 0
    vMax = vitesseMax(acceleration)
    if axe == 0:
        if zInitial != 0 or xInitial != 0:
            angle = np.arctan(zInitial / xInitial)
        else:
            angle = 0
    else:
        if zInitial != 0 or yInitial != 0:
            angle = np.arctan(zInitial / xInitial)
        else:
            angle = 0

    for index in range(1, int(temps*60)):
        #x ou y
        if axe == 0:
            position[1].append(yInitial)
        else:
            position[0].append(xInitial)

        if position[2][index - 1] >= h_max:
            position[axe].append(position[axe][index-1])
            position[2].append(h_max)
            break
        else:
            #x ou y
            accB = acceleration - g*np.cos(angle)-np.sin(angle)*Constant.coefficient_friction*g
            if vitesseActuel > vMax:
                if (vitesseActuel - vMax) / Constant.deltaT > accB:
                    vitesseActuel = vitesseActuel - accB * Constant.deltaT
                else:
                    vitesseActuel = vMax

            elif vitesseActuel < vMax:
                if (vMax - vitesseActuel) / Constant.deltaT > accB:
                    vitesseActuel = vitesseActuel + accB * Constant.deltaT
                else:
                    vitesseActuel = vMax
            vitesseActuelle = vitesseActuelle + accB * Constant.deltaT
            position[axe].append(position[axe][index-1] - signe*vitesseActuelle * Constant.deltaT)

            #z
            theta = np.arctan(position[axe][index]/Constant.rayon_socle)
            hauteur_z = Constant.rayon_socle*np.cos(theta)
            position[2].append(Constant.rayon_socle-hauteur_z)

        if position[2][index] != 0 or position[axe][index] != 0:
            angle = np.arctan(position[2][index]/position[axe][index])
        else:
            angle = 0

    return position

def billeDecelere(xInitial, yInitial, zInitial, acceleration, temps, axe, signe):  #axe entre 0 (x) et 1 (y),
    g=9.81
    position = [[xInitial], [yInitial], [zInitial]]
    vitesseActuelle = 0
    if axe == 0:
        if zInitial != 0 or xInitial != 0:
            angle = np.arctan(zInitial/ xInitial)
        else:
            angle = 0
    else:
        if zInitial != 0 or yInitial != 0:
            angle = np.arctan(zInitial/ xInitial)
        else:
            angle = 0


    for index in range(1, int(temps*60)):
            #x ou y
            if axe == 0:
                position[1].append(yInitial)
            else:
                position[0].append(xInitial)

            if position[2][index - 1] == 0:
                t = temps-index/60
                position += billeAccelere(position[0][index-1],position[1][index-1], position[2][index-1], acceleration, t, axe, -signe)
                break
            else:
                # x ou y
                accB = -acceleration - g*np.cos(angle)+np.sin(angle)*Constant.coefficient_friction*g
                vitesseActuelle = vitesseActuelle + accB * Constant.deltaT
                position[axe].append(position[axe][index-1] + signe * vitesseActuelle * Constant.deltaT)

                #z
                theta = np.arctan(position[axe][index] / Constant.rayon_socle)
                hauteur_z = Constant.rayon_socle * np.cos(theta)
                position[2].append(Constant.rayon_socle - hauteur_z)

            if position[2][index] != 0 or position[axe][index] != 0:
                angle = np.arctan(position[2][index] / position[axe][index])
            else:
                angle = 0

    return position

def calculTrajet():
    depla, vitesse = ligneDroiteAvance(0, 0, 0, 0.2, 0, 1)

    depla2, vitesse2 = getTournant(depla[0][len(depla[0])-1], depla[1][len(depla[1])-1], vitesse, 0.5, 0, 3)

    depla3, vitesse = ligneDroiteAvance(depla2[0][len(depla2[0])-1], depla2[1][len(depla2[1])-1], vitesse2, 0.5, 1, -1)

    depla4 = ligneDroiteArreter([depla3[0][len(depla3[0])-1], depla3[1][len(depla3[1])-1]], 1, -1)

    bille1 = billeAccelere(0, 0, 0, getAccelerationMax(), 10, len(depla[0])/60, 0, 1)

    print(depla[0])
    print(depla[1])
    print(" tournant")
    print(depla2[0])
    print(depla2[1])
    print("a")
    print(depla3[0])
    print(depla3[1])
    print("b")
    print(depla4[0])
    print(depla4[1])

    print("\nBille:")
    print(bille1[0])
    print(bille1[2])

    #Save list to excel

    # df = pd.DataFrame(depla)
    # de = pd.DataFrame(depla2)
    # writer = pd.ExcelWriter('trajet.xlsx', engine='xlsxwriter')
    # df.to_excel(writer, sheet_name='deplacement 1', index=False)
    # de.to_excel(writer, sheet_name='deplacement 2', index=False)
    # writer.save()
    return 0

def billeAvance():
    return 0

if __name__ == '__main__':
    calculTrajet()
    ligneDroiteArreter([0, 0], 0, 1)
    getTournant(0,0, 0.65, 1, 0, 3)