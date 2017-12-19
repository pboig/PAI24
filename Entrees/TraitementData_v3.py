# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 16:39:59 2017

@author: perez
"""
import numpy as np

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
        indicesExtract = [0,4,24,7,5,8,27,29,21,19,9,28]
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
    
def extractDepartementData(mData, idDep):
    res = []
    for x in mData:
        if x[0] == idDep:
            res.append(x[1:])
    return(np.array(res))

def normalisationModalites(mData):
    (I,J) = np.shape(mData)
    for i in range(I):
        mData[i,2] = min(mData[i,2]//5,14)  #Mise en classe en tranche de 5 ans
        mData[i,4] = max(mData[i,4],10)
    minim = mData[:,2:].min(0)
    minim = np.tile(minim,(I,1))
    mData[:,2:] = mData[:,2:] - minim+1     #Numéro de classe commençant à 1
    return()
"""
===========================================================================================================
                                        TRAITEMENT DES DONNEES
===========================================================================================================
"""  
def freqGlobales(mData):
    (I,J) = np.shape(mData[:,2:])
    maxim = mData[:,2:].max(0)
    
    res = [[0]*j for j in maxim]
    tot = [0]*J
    for k in range(I):
        for p in range(J):
            j = mData[k,p+2]-1
            res[p][j] += 1
            tot[p] += 1
    for p in range(J):
        for j in range(maxim[p]):
            res[p][j] /= tot[p]
    return(res)

def freqCommunes(mData):
    (I,J) = np.shape(mData[:,2:])
    res = []
    k = 0
    while k<I:
        k0 = k
        n1,n2 = mData[k0,0], mData[k0,1]
        while (k<I) and (mData[k,0] == n1) and (mData[k,1] == n2):
            k += 1
        k += 1
        res.append(freqGlobales(mData[k0:k,:]))
    return(res)
    
def VarXVarData(mData):
    studyData = mData[:,2:]
    (I,J) = np.shape(studyData)
    maxim = studyData.max(0)
    p10 = maxim[9]; p11 = maxim[10] #9 LdTravail; 10 Transport
    q = maxim[:9].sum()
    res = np.zeros((p10+p11,q))
    npa = np.zeros(J-2, dtype = 'int')
    for j in range(1,J-2):
        npa[j] = npa[j-1]+maxim[j-1]
    for i in range(I):
        for j in range(J-2):
            res[studyData[i,9]-1, npa[j]+studyData[i,j]-1] += 1
            res[p10+studyData[i,10]-1, npa[j]+studyData[i,j]-1] += 1
    res[:p10,:] /= res[:p10,:].sum()
    res[p10:,:] /= res[p10:,:].sum()
    return(res)
            
    
