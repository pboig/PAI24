# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 16:39:59 2017

@author: perez
"""

"""
===========================================================================================================
                                        LECTURE DES FICHIERS
===========================================================================================================
"""
def cint(txt):      # Convertit une donnée texte d'un fichier INSEE en un entier
    if (txt == 'Z') or (txt == 'ZZ') or (txt == 'ZZZ') or (txt == 'ZZZZ'):  # A étudier (fichier MobPro)
        return(0)
    else:
        return(round(float(txt)))

def readfile(nomFichier):
    with open(nomFichier, 'r') as f:
        data = f.readlines() #ou f.read().splitlines()
    return(data)

def add_ligne(txtLigne, indicesExtract, nbIdComm, J, iDep, res):
    converted_ligne = [0]*(J+nbIdComm)
    ligne = txtLigne.split(";")
    onlyDep = 0 # si le iDep est l'une des communes de la ligne alors onlyDep > 0 et on rajoute la ligne  à res, sinon on ne fait rien
    
    i_r = 0     # indice lecture    (dans indicesExtract)
    i_w = 0     # indice écriture   (dans converted_ligne)
    while i_r < nbIdComm:
        idCommune = ligne[indicesExtract[i_r]]
        converted_ligne[i_w:i_w+2] = idCommune[:2], idCommune[2:]
        if (iDep == None) or (converted_ligne[i_w] == iDep):
            onlyDep += 1
        i_r += 1
        i_w += 2
            
    if not(onlyDep):
        return(res)
    for i in indicesExtract[i_r:]:
        converted_ligne[i_w] = cint(ligne[i])
        i_w += 1
        
    res.append(converted_ligne)
    return()
     
def extractUsefulData(txtDataBrut, iData, iDep = None):
    """ 
    Paramètre iData = type de fichier lu
        si iData = 1 : mobilités pro
        si iData = 2 : flux mobilité pro
        ...
    --------------------------------------------
    Paramètre iDep = extraction des données du département n° iDep
    """
    if iData == 1:
        indicesExtract = [0,5,9]
        nbIdComm = 1
    elif iData == 2:
        indicesExtract = [0,2,4]
        nbIdComm = 2
    J = len(indicesExtract)
    N = len(txtDataBrut)
    res = []
    for i in range(1,N):
        add_ligne(txtDataBrut[i], indicesExtract, nbIdComm, J, iDep, res)
    return(res)

def loadData(txtNomFichier, iData, iDep = None):
    txtDataBrut = readfile(txtNomFichier)
    return(extractUsefulData(txtDataBrut, iData, iDep))

def normalisationModalites(mData):
    for ligne in mData:
        if ligne[2] not in [3,4,5,6]:   # CSP = Autre, Cadre, Pro. intermédiaire, Employé, Ouvrier
            ligne[2] = 2
        ligne[2] -= 2   #Indice commençant à 0
        if ligne[3] != 1:               # Lieu de travail = 1 si travaille dans la commune de résidence et 0 sinon
            ligne[3] = 0
    return()

    
