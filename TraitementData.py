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



"""  Convertit une donnée texte d'un fichier INSEE en un entier  """
def cint(txt):                                                             
    if (txt == 'Z') or (txt == 'ZZ') or (txt == 'ZZZ') or (txt == 'ZZZZ'):  # A étudier (fichier MobPro)
        return(0)
    else:
        return(round(float(txt)))


"""  Charge les données d'un fichier text sous forme de lignes  """
def readfile(nomFichier):
    with open(nomFichier, 'r') as f:
        data = f.readlines() 
    return(data)



"""La fonction add_ligne renvoit uniquement les champs de txtLigne qui nous intéressent. A partir du fichier txtDataBrut, en aplliquant la fonction add_ligne à toutes les lignes du fichier, on obtient une liste de listes où chacun des champs de la liste primaire correspond à une personne ayant complété l'étude avec uniquement les données qui nous intéressent.
On crée tout d'abord a ligne à renvoyer sous forme de liste converted_ligne.
On commence par séparer les numéros des communes pour obtenir le numéro du département d'une part et le numéro de la commune d'aute part. On ajoute le tout dans les champs correspondant dans converted_ligne à renvoyer.
Enfin, on complète converted_ligne par le reste des données à extraire.
Dans la suite la variable iData sera définie dans la fonction extractUsefulData"""

# indicesExtract = indices à extraire du fichier (suivant que l'on regarde les mobilités pro ou les flux de mobilité)
# J = len(indicesExtract) : nombre d'indices à etraire
# txtLigne = une ligne de la variable txtDataBrut
#nbIdComm représente le nombre de communes à séparer dans les champs. Si iData = 1 on ne s'intéresse qu'à la commune de résidence. A l'inverse, si iData = 2 on s'intéresse à la commune de résidence et à celle de travail. on veut donc dans les deux cas s"parer le numéro du département de celui de la commune.

def add_ligne(txtLigne, indicesExtract, nbIdComm, J, iDep, res):
    converted_ligne = [0]*(J+nbIdComm)                              # converted_ligne est la nouvelle ligne du fichier textDataBrut où l'on ne garde que les indices qui nous intéressent. Elle fait la taille de indicesExtract + nbIdComm car on divise IDcommune en deux : le département et la commune.
    ligne = txtLigne.split(";")                                     # Sépare les différents champs de la ligne txtLigne. Renvoit une liste avec où chaque champ sous format txt
    onlyDep = 0                                                     # Si le iDep est l'une des communes de la ligne alors onlyDep > 0 et on rajoute la ligne  à res, sinon on ne fait rien
    
    i_r = 0                                                         # Indice lecture    (dans indicesExtract)
    i_w = 0                                                         # Indice écriture   (dans converted_ligne)
    
    """ On commence par séparer les numéros des communes en deux.
    Si iData = 1 : nbIdComm = 1 et on ne sépare que le nom de la commune de résidence en 2 avec i_r = 0 et i_w = 0
    Si iData = 2 : nbIdComm = 2 et on sépare d'abord le nom de la commune de résidence en 2 avec i_r = 0 puis on sépare le nom de la commune de travail en 2 avec i_r = 1 et i_w = 2"""
    while i_r < nbIdComm:
        idCommune = ligne[indicesExtract[i_r]]                      # On récupère le numéro département+commune à séparer dans la ligne de textDataBrut
        converted_ligne[i_w:i_w+2] = idCommune[:2], idCommune[2:]   # Séparation département - commune
        if (iDep == None) or (converted_ligne[i_w] == iDep):        # On ne renvoit une ligne que si le département correspendant à la ligne est celui que l'on veut
            onlyDep += 1
        i_r += 1
        i_w += 2
            
    if not(onlyDep):                                                # On renvoit une liste vide [] si la ligne correspond à un département autre que iDep
        return(res)
        
    """ On ajoute ensuite dans res les champs de indicesExtract qui reste.
    SI iData = 1 : Il reste à ajouter les CSP et l'indice du lieu de travail
    Si iData = 2 : il reste à ajouter les conditions d'emploi"""
    for i in indicesExtract[i_r:]:                                  #On parcourt les indices restant de indicesExtract
        converted_ligne[i_w] = cint(ligne[i])                       # On ajoute les champs d'indicesExtract manquants
        i_w += 1
        
    res.append(converted_ligne)
    return()
    



""" la fonction extractUsefulData a pour but de ne prendre que les indices du fichier textDataBrut qui nous intéressent et les renvoit sous forme de liste.
Si l'on s'intéresse qu'aux mobilités pro on renvoit une liste ( IDcommune ; CSP ; lieu de travail ) où chaque champ correspond à un individu résident dans iDep.
Si l'on s'intéresse qu'aux flux de mobilité pro on renvoit une liste ( IDcommune ; arondissement municipal de résidence ; condition d'emploi (salarié, CDI, CDD...) ) où chaque champ correspond à un individu résident dans iDep."""

#txtDataBrut : tableau contenant toutes les lignes du fichier insee. Une ligne correspond à une personne ayant complété l'étude.
#Paramètre iData = type de fichier lu
    # Si iData = 1 : mobilités pro
    # Si iData = 2 : flux mobilité pro
#Paramètre iDep = extraction des données du département n° iDep
    
def extractUsefulData(txtDataBrut, iData, iDep = None):    
    if iData == 1:
        indicesExtract = [0,5,9]    #0 : commune de résidence, 5 : CSP, 9: indice du lieu de travail
        nbIdComm = 1
    elif iData == 2:
        indicesExtract = [0,3,8]    #0 : commune de résidence, 3 : département et commune de travail, 8 : condition d'emploi(salarié, CDD, CDI...)
        nbIdComm = 2
    J = len(indicesExtract)         # J : nombre d'indices à extraires du fichier txtDataBrut
    N = len(txtDataBrut)            # N : nombre total de lignes dans le fichier txtDataBrut = nombre de personnes ayant complété l'étude
    res = []                        # On renvoit une nouvelle liste avec uniquemeent les indices de txtDataBrut qui nous intéressent
    
    """ On parcourt tout le fichier textDataBrut et on ne récupère que les indices qui nous intéressent que l'on stock dans 'res' """
    for i in range(1,N):
        add_ligne(txtDataBrut[i], indicesExtract, nbIdComm, J, iDep, res)
    return(res)


"""La focntion loadData renvoit un tableau contenant les champs qui nous intéressent, correspondant à iData, pour les résidents de iDep"""

def loadData(txtNomFichier, iData, iDep = None):
    txtDataBrut = readfile(txtNomFichier)
    return(extractUsefulData(txtDataBrut, iData, iDep))




"""
===========================================================================================================
                                        TRAITEMENT DES FICHIERS
===========================================================================================================
"""

""" la fonction normalisationModalites a pour but de réorganiser les valeurs des modalités des variables CSP et indice du lieu de travail.
Changements :
    CSP : (1 Agriculteurs ; 2 Artisants, commercants ; 3 cadres ; 4 prefessions intermédiares ; 5 Employés ; 6 Ouvriers ; 7 retraités ; 8 Autres) -> (0 Autres ; 1 Cadre; 2 Pro. intermédiaire; 3 Employé; 4 Ouvrier )
    Indice du lieu de travail : (1 commune de résidence ; 2 autre commune ; 3 autre département ; 4 hors région mais en métropole ; 5 hors région et dans DOM ; 6 hors région et dans COM ; 7 à l'étranger) -> (0 Hors commune résidence; 1 commune résidence)
La fonction renvoit le nombre de modalités des variables 'CSP' et 'indice du lieu de travail'."""

# mData : tableau issu de la fonction loadData pour un iData donné et un iDep donné.

def normalisationModalites(mData):
    nbModalites = [5, 2]                # Nombre de modalités de chaque variable
    for ligne in mData:
        """ On passe à : CSP = (0 Autre; 1 Cadre; 2 Pro. intermédiaire; 3 Employé; 4 Ouvrier)"""
        if ligne[2] not in [3,4,5,6]:   # ligne[2] : CSP de la ligne
            ligne[2] = 2
        ligne[2] -= 2   
        
        """On passe à : Lieu de travail = (0 Hors commune résidence; 1 commune résidence)"""
        if ligne[3] != 1:               # ligne [3] : indice du lieu de travail de la ligne
            ligne[3] = 0
    return(nbModalites)


"""La fonction regroupeParCommune a pour but de compter les pourcentage de chaque modalité dans toutes les communes du fichier mData.
On crée ainsi une liste comportant le numéro de la commune, les pourcentages de chaque modalité de CSP puis le pourcentage de chaque modalité d'indice du lieu de travail. le tout pour chaque commune et normalisé par le nombre d'habitant de la commune donnée.
Ainsi, on pour chaque commun de mData on renvoit une liste du type : [ indice de la commune, [%CSP = 0, %CSP = 1, %CSP = 2, %CSP = 3, %CSP = 4], [%indiceLieuTravail = 0, %indiceLieuTravail = 1] ].    EX : res = [['001', [0.25, 0.16666666666666666, 0.16666666666666666, 0.3333333333333333, 0.08333333333333333], [0.0, 1.0]]]
Finalement, la fonction renvoit une liste comportant pour chaque commune de mData, une liste du type précédent.""" 

# mData : tableau issu de la fonction loadData pour un iData donné et un iDep donné.
# vNbModalites : résultat de la fonction normalisationModalites ie. vNbModalites = [5, 2]
    
def regroupeParCommune(mData, vNbModalites):
    N = len(mData)                                                      # N : Nombre de personnes résidant dans le département iDep
    J = len(vNbModalites)                                               # J : Nombre de variables ayant plusieurs modalités ('CSP' et 'indice du lieu de travail')
    i = 0
    res = []
    while i < N:
        newCommune = [[0 for kj in range(j)] for j in vNbModalites]     # On crée un tableau comportant deux listes : une liste de 5 champs destinée à recevoir le pourcentage de personnes vivant dans la commune propre à caque modalité de CSP et de même pour l'indice du lieu de travail avec une liste de 2 champs. NewCommune = [[0, 0, 0, 0, 0], [0, 0]]
        newCommune.insert(0, mData[i][1])                               # On ajoute le numéro de la commune devant les listes. EX : NewCommune = ['001', [0, 0, 0, 0, 0], [0, 0]]
        nHabitantCommune = 0                                            # On compte le nombre d'habitants dans la commune pour pouvoir faire un pourcentage et pondérer les modalités           
        while i < N and mData[i][1] == newCommune[0]:                   # On s'assure que la ligne i de mData correspond bien à la commune considérée dans 'newCommune' et on parcourt toutes les lignes de mData
            print('i',i)
            for j in range(1,J+1):                                      # On parcourt toutes les modalités de la ligne i de mData
                print('j',j)
                newCommune[j][mData[i][j+1]] += 1                       # On ajoute 1 personne dans le champ de newCommune qui correspond à la modalité de la ligne i.
            i += 1
            nHabitantCommune += 1
        for j in range(1,J+1):
            for kj in range(vNbModalites[j-1]):                         # On normalise les coefficients de chaque champ de newCommune pour obtenir un pourcentage
                newCommune[j][kj] /= nHabitantCommune
        res.append(newCommune)                                          # On renvoit une liste comportant les pourcentage de chaque modalité dans une commune donnée pour toute les communes
    return(res)
    
def concatenationDonnees(mData1, mData2):
    N1, N2 = len(mData1), len(mData2)
    notFound, idNF = [], []
    for i1 in range(N1):
        i2 = 0
        while i2 < N2 and int(mData1[i1][0]) != int(mData2[i2][0]):
            i2 += 1
        if i2 == N2:
            notFound.append(mData1[i1][0])
            idNF.append(i1)
        else:
            mData1[i1].insert(1, mData2[i2][1])
    if len(idNF) != 0:
        for i in range(len(idNF)):
            del(mData1[idNF[i]-i])
    del(mData2)
    return(notFound)
    
def concatenationDonneesWNumpy(mData, mDataN):
    N1, N2 = len(mData), mDataN.shape[0]
    notFound, idNF = [], []
    for i1 in range(N1):
        i2 = 0
        while i2 < N2 and int(mData[i1][0]) != int(mDataN[i2,0]):
            i2 += 1
        if i2 == N2:
            notFound.append(mData[i1][0])
            idNF.append(i1)
        else:
            mData[i1].insert(1, list(mDataN[i2,1:]))
    if len(idNF) != 0:
        for i in range(len(idNF)):
            del(mData[idNF[i]-i])
    return(notFound)

def delNotFoundCommNumpy(mData,mDataN):         # Suppression des communes de la matrice numpy mDataN non trouvées dans mData
    N1, N2 = len(mData), mDataN.shape[0]
    notFound = []
    for i2 in range(N2):
        i1 = 0
        while i1 < N1 and int(mData[i1][0]) != int(mDataN[i2,0]):
            i1 += 1
        if i1 == N1:
            notFound.append(mDataN[i2,0])
    p = N2-len(notFound); q = mDataN.shape[1]
    if p < N2:
        newDataN = np.zeros((p,q))
        j = 0
        for i in range(N2):
            if not(mDataN[i,0] in notFound):
                newDataN[j,:] = mDataN[i,:]
                j += 1
    return(newDataN)              
                            
def splitSet(y):
    N = y.shape[0]  
    sets = np.random.binomial(1,0.8,N)
    uniq, count = np.unique(sets, return_counts=True)
    trainingSet = np.zeros(count[1], dtype = 'int')
    validationSet = np.zeros(count[0], dtype = 'int')
    p, q = 0, 0
    for i in range(N):
        if sets[i]:
            trainingSet[p] = i
            p += 1
        else:
            validationSet[q] = i
            q += 1
    return(trainingSet, validationSet)
            
def checkComm(mDataComm):
    res = []
    for i in range(len(mDataComm)):
        res.append(mDataComm[i][0])
    return(res)
    
    
    
    
