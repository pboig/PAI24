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
    
   
"""La fonction  concatenationDonnees prend deux tableaux mData1 et mData2 et ajoute les données d'une commune de mData2 dans la commune correspondante de mData1. 
En pratique, on concatène les pourcentage de modalités de chaque communes (mData1 issu de regroupeParCommune) et le nombre d'emplois par communes (mData2 issu de loadXlsEmploi).
Pour chaque commune de mData1, on parcourt toutes les communes de mData2 et on ajoute alors le nombre d'emplois de la commune comme nouveau champ d'indice 1 de la ligne i de mData1.
A la fin de l'execution de la fonction, mData1 est de la forme : [ indice de la commune, nombre d'emplois, [%CSP = 0, %CSP = 1, %CSP = 2, %CSP = 3, %CSP = 4], [%indiceLieuTravail = 0, %indiceLieuTravail = 1] ]
Par ailleurs, on stocke toutes les communes de mData1 dont on n'a pas de données sur le nombre d'emplois dans une variable notFound que l'on renvoit à la fin."""

# mData1 : tableau issu de la fonction loadData pour un iData donné et un iDep donné. Dans notre utilisation mData1 représente le résultat de la fonction regroupeParCommune. Il comporte donc une liste de nom de commune et de pourcentage de chaque modalités dans la commune.
        # une ligne de mData1 a la forme [ indice de la commune, [%CSP = 0, %CSP = 1, %CSP = 2, %CSP = 3, %CSP = 4], [%indiceLieuTravail = 0, %indiceLieuTravail = 1] ]
# mData2 : tableau issu de la fonction loadData pour un iData donné et un iDep donné. Dans notre utilisation mData2 représente le résultat de la fonction loadXlsEmplois. Il comporte donc une liste avec pour chaque commune le nombre d'emplois dans cette commune.
        # une ligne de mData2 a la forme [ ID_commune ; nb_emplois ]

def concatenationDonnees(mData1, mData2):
    N1, N2 = len(mData1), len(mData2)                                   # N1 : nombre de communes dans mData1   ;    N2 : nombre de communes dans mData2
    notFound, idNF = [], []                                             # On repère les indices des communes non trouvées dans mData 2
    for i1 in range(N1):                                                # On parcourt toutes les communes de mData1
        i2 = 0
        while i2 < N2 and int(mData1[i1][0]) != int(mData2[i2][0]):     # On parcourt toutes les communes de mData2 et on cherche celle correspondant à la commune de la ligne i1 de mData1
            i2 += 1
        if i2 == N2:                                                    # Si mData2 ne comprend pas la commune de la ligne i1 de mData1 on la stoche dans notFound ainsi que son indice dans idNF
            notFound.append(mData1[i1][0])
            idNF.append(i1)
        else:                                                           # Le cas où la commune de la ligne i1 de mData1 est la même que celle de la ligne i2 de mData2
            mData1[i1].insert(1, mData2[i2][1])                         # On ajoute un nouveau champ à mData égal au nombre d'emplois dans la commune
    if len(idNF) != 0:
        for i in range(len(idNF)):                                      # On supprime toutes les communes de mData1 dans lesquelles on a pas le nombre d'emplois
            del(mData1[idNF[i]-i])
    del(mData2)
    return(notFound)                                                    # On renvoit les communes de mData1 dont on ne dispose pas du nombre d'emplois
    
    
    
    
"""La fonction ConcatenationDonneesWNumpy réalise la même opération que la fonction concatenationDonnees en prenant compte du format de données de mDataN.
Ainsi, pour chaque commune de mData on ajoute les données GPS de la commune GPS de mDataN en indice 1 de mData ou alors on la stocke dans notFound si on ne dispose pas de données GPS. En renvoit alors les communes dont on ne connait pas de données GPS
A la fin de l'execution, mData a la forme :  [ indice de la commune,[ X (km), Y (km) ],  nombre d'emplois, [%CSP = 0, %CSP = 1, %CSP = 2, %CSP = 3, %CSP = 4], [%indiceLieuTravail = 0, %indiceLieuTravail = 1] ]"""

# mData : tableau issu de la fonction loadData pour un iData donné et un iDep donné. Dans notre utilisation mData1 représente le résultat de la fonction regroupeParCommune après exécution de concatenationDonnees. Il comporte donc une liste de nom de commune et de pourcentage de chaque modalités dans la commune ainsi que le nombre d'emplois dans la commune.
        # une ligne de mData a la forme [ indice de la commune, nombre d'emplois, [%CSP = 0, %CSP = 1, %CSP = 2, %CSP = 3, %CSP = 4], [%indiceLieuTravail = 0, %indiceLieuTravail = 1] ]
# mDataN : tableau au format Numpy soit une matrice. Dans notre utilisation, mDataN représente la matrice issue de la fonction loadDataGPS. Elle comporte donc le numéro de la commune et ses données GPS
        # un champ de la matrice a la forme [ ID_commune ; distance_X(km) ; distance_Y(km) ]

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




"""La fonction delNotFoundCommNumpy a pour but de supprimer toutes les données des communes de mDataN qui ne sont pas dans mData
On comence par lister toutes les communes qui ne sont dans mDataN et pas dans mDataN. On crée ensuite une nouvelle matrice qui comporte autant de champs qu'il y a de communes communes à mData et mDataN
On parcourt ensuite toute la matrice mDatan et on remplit la nouvelle matrice ainsi créée. On renvoit au final cette nouvelle matrice complétée des communes et de leurs données GPS"""

# mData : tableau issu de la fonction loadData pour un iData donné et un iDep donné. Dans notre utilisation mData1 représente le résultat de la fonction regroupeParCommune après exécution de concatenationDonnees et de concatenationDonneesWNumpy. 
# Il comporte donc une liste de nom de commune et de pourcentage de chaque modalités dans la commune ainsi que le nombre d'emplois dans la commune et les données GPS de la commune.
        # une ligne de mData a la forme  [ indice de la commune,[ X (km), Y (km) ],  nombre d'emplois, [%CSP = 0, %CSP = 1, %CSP = 2, %CSP = 3, %CSP = 4], [%indiceLieuTravail = 0, %indiceLieuTravail = 1] ]
# mDataN : tableau au format Numpy soit une matrice. Dans notre utilisation, mDataN représente la matrice issue de la fonction loadDataGPS. Elle comporte donc le numéro de la commune et ses données GPS
        # un champ de la matrice a la forme [ ID_commune ; distance_X(km) ; distance_Y(km) ]

def delNotFoundCommNumpy(mData,mDataN):         # Suppression des communes de la matrice numpy mDataN non trouvées dans mData
    N1, N2 = len(mData), mDataN.shape[0]                            # N1 : nombre de communes dans mData   ;    N2 : nombre de communes dans mDataN 
    notFound = []
    for i2 in range(N2):                                            # On parcourt toutes les communes de mDataN
        i1 = 0
        while i1 < N1 and int(mData[i1][0]) != int(mDataN[i2,0]):   # On parcourt toutes les communes de mData
            i1 += 1
        if i1 == N1:                                                # Si la communes d'indice i2 de mDataN n'est pas dans mData1
            notFound.append(mDataN[i2,0])                           # On stocke les donnes GPS de la commune d'indice i2 et son numéro dans notFound
    p = N2-len(notFound); q = mDataN.shape[1]                       # p : nombre de communes communes à mData et mDataN    ;    q : nombre de champ de chaque composante de la matrice. ie : Idcommune, x , Y
    if p < N2:
        newDataN = np.zeros((p,q))                                  # On crée une nouvelle matrice avec autant de composantes qu'il y a de communes communes à mData et mDataN
        j = 0
        for i in range(N2):                                         # On parcourt toutes les communes de mDataN pour compléter newDataN avec celles qui sont communes à mData et mDataN
            if not(mDataN[i,0] in notFound):                        # On s'assure que la commune d'indice i est bien dans les deux fichiers
                newDataN[j,:] = mDataN[i,:]                         # On complète newDataN
                j += 1
    return(newDataN)                                                # On renvoit une matrice ne comportant que les communes et leurs données GPS qui sont dans mData.



"""La fontion splitSet sépare les valeurs de y dans les matrices trainingSet et validationSet avec une probabilité de 0.8 pour trainingSet.
Ainsi, pour chaque champ de y, on a une chance de 0.8 de le stocker dans trainingSet. on ne stock toutefois que les indices des champs de y dans les deux nouvelles matrices créées.
On renvoit ainsi les matrices trainingSet et validationSet."""

# y : matrice contenant des données issues de regroupeParCommune converties au format numpy pour les opérations de modélisation et d'optimisation.
                     
def splitSet(y):
    N = y.shape[0]                                                  # N : taille de la matrice y
    sets = np.random.binomial(1,0.8,N)                              # On renvoit une matrice contenant N essais d'une variable binomiale de probabilité 0.8 (constitué de 0 et de 1)
    uniq, count = np.unique(sets, return_counts=True)               # uniq : renvoit une matrice contenant tous les nombres de sets qui sont uniques dans l'odre croissant     ;     count : renvoit une matrice contenant le nombre d'apparition de chaque nombre de uniq dans sets et le type des variables
    trainingSet = np.zeros(count[1], dtype = 'int')                 # On crée une matrice aussi grande qu'il y a de fois 1 dans sets
    validationSet = np.zeros(count[0], dtype = 'int')               # On crée une matrice aussi grande qu'il y a de fois 0 dans sets       
    p, q = 0, 0
    for i in range(N):                                              # On parcourt tous les essais de la variable sets
        if sets[i]:                                                 # Si sets[i] = 1                   
            trainingSet[p] = i                                      # On ajoute l'indice i à trainingSet
            p += 1
        else:                                                       # Si stes[i] = 0
            validationSet[q] = i                                    # On ajoute l'indice i à validationSet
            q += 1
    return(trainingSet, validationSet)
        



""" La fonction checkComm renvoit un tableau contenant les numéros des communes de mDataComm"""
   
def checkComm(mDataComm):
    res = []
    for i in range(len(mDataComm)):
        res.append(mDataComm[i][0])
    return(res)
    
    
    
    
