# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 10:03:55 2017

@author: perez
"""

"""
Méthodologie :
1) PRE-TRAITEMENT :  Conversion matrice données en une matrice numpy
                        > 'dataToNumpy' (Entrée = whole Data Set)
2) OPTIMISATION   :  Regression non-linéaire avec la matrice numpy 
                        > 'optimisation' (Entrée = Training Set)
                            > 'hypFunction' (Entrée = une commune - numpy)
3) CALCUL RESULTAT:  Calcul des résultats à partir des paramètres optimisés - en passant par numpy 
                        > hypFunction (Entrée = une ou des commune(s))
4) POST-TRAITEMENT:  Validation de la fonction hypothèse 
                        > fonction4 (Entrée = Validation Set)
                        
Data format classique (instinctif, facile à manipuler) VS Data format numpy (facile pour calculer)
    > Ou bien tout le temps classique (nécessite de créer ses propres fonction d'optimisation)
    > Ou bien tout le temps numpy (mais besoin de connaître les indices de chaque variable/modalité, pas pratique)
    > Ou bien transition de classique à numpy : SOLUTION RETENUE ?!
"""



import numpy as np
import scipy 



""" =================================== PRE-TRAITEMENT =================================== """


"""La fonction length renvoit la taille de x si c'est une liste ou 1 si ce n'en est pas une """
def length(x):
    if type(x) == list:
        return(len(x))
    return(1)


"""Le but de la fonction dataToNumpy est de changer le format de la fonction mData pour que l'on puisse faire des opérations dessus.
Elle opère donc de façon à mettre les modalités de chaque variable de la ligne i de mData bout-à-bout.
On renvoit dont deux matrices numpy : l'une avec les informations d'indice iOut, et l'autre avec toutes les autres informations de mData """

# mData : tableau issu de la fonction loadData pour un iData donné et un iDep donné. Dans notre utilisation mData1 représente le résultat de la fonction regroupeParCommune. Il comporte donc une liste de nom de commune et de pourcentage de chaque modalités dans la commune.
        # une ligne de mData1 a la forme [ indice de la commune, [%CSP = 0, %CSP = 1, %CSP = 2, %CSP = 3, %CSP = 4], [%indiceLieuTravail = 0, %indiceLieuTravail = 1] ]
# iOut = indices des sorties dans mData

def dataToNumpy(mData, iOut = []):

    # Met les modalités des variables bout-à-bout
    """ On calcule les tailles des matrices que l'on veut renvoyer : autant de lignes que mData et autant de coordonnées que l'on souhaite renvoyer d'information dans dataOutNumpy d'une part, et toutes les autres d'autre part """
    I, M, J, K = len(mData), len(mData[0]), 0, 0        # I : nombre de lignes de mData   ;   M : nombre de champs sur une ligne de mData
    for m in range(1,M):                                # On parcourt tous les champs d'une ligne de mData
        x = mData[0][m]                                 # On va chercher l'information de la commune d'indice m
        if m in iOut:                                   # Si l'on cherche l'information d'indice m
            K += length(x)                              
        else:
            J += length(x)
        
    dataInNumpy = np.zeros((I,J))                       # On crée une matrice avec autant de lignes que mData et chaque ligne comporte autant de champs que les lignes initiales moins celles que l'on veut renvoyer dans iOut
    dataOutNumpy = np.zeros((I,K))                      # On crée une matrice avec autant de lignes que mData et chaque ligne comporte le nombre de champ que l'on désire renvoyer dans iOut
   
    """On remplit ensuite les matrices dataInNumpy et dataOutNumpy avec les informations de mData correspondantes au format Numpy """
    for i in range(I):                                  # On parcourt toutes les lignes de mData
        j, k = 0, 0
        for m in range(1,M):                            # On parcourt tous les champs de la ligne i
            x = mData[i][m]                             # On s'intéresse au champ d'indice m de la ligne i
            n = length(x)
            if m in iOut:                               # Si l'on veut renvoyer cette information
                if n == 1:                              # Si le champ d'indice m de la ligne i est un nombre
                    dataOutNumpy[i,k] = x               # On l'ajoute à dataOutNumpy
                    k += 1
                else:
                    for y in range(n):                  # Si le champ d'indice m de la ligne i est une liste
                        dataOutNumpy[i,k] = x[y]        # On ajoute tous les termes de la liste à la suite
                        k += 1
            else:                                       # Si on ne veut pas renvoyer cette information, on fait les mêmes opérations que précédemment mais en ajoutant les données à dataInNumpy                             
                if n ==1:
                    dataInNumpy[i,j] = x
                    j += 1
                else:
                    for y in range(n):
                        dataInNumpy[i,j] = x[y]
                        j += 1
    return(dataInNumpy, dataOutNumpy)                   # On renvoit les données que l'on veut (dataOutNumpy) et les autres (dataInNumpy)
    
    
    
    
""" =================================== OPTIMISATION =================================== """


""" Renvoit une sigmoïd de la forme 1/(1+exp(-x)) """
def sigmoid(X):
    return(1./(1+np.exp(-X)))
    
    
    
"""La fonction hypFunction a pour but de créer un polynome des données de mDataX.
On modifie donc mDataX de façon à avoir un polynome de chacune de ses données initiales des degrés 0 à degPoly"""

# mDataX : tableau issu de la fonction loadData pour un iData donné et un iDep donné. Dans notre utilisation mDataX représente le résultat de la fonction regroupeParCommune après execution de la fonction splitSet. 
#Il comporte donc une liste de de données avec uniquement les champs qui nous intéressent du fichier txt original. Chaque ligne de mDataX correspond à une commune

def hypFunction(mDataX, Theta, degPoly):                                    ##### Ne marche actuellement pas si mDataX contient une seule commune
    X = np.concatenate((np.ones((mDataX.shape[0],1)), mDataX), axis = 1)    # On ajoute un 1 devant toutes les lignes de mDataX
    for i in range(2, degPoly+1):
        X = np.concatenate((X, mDataX**i), axis = 1)                        # On ajoute à chaque champ de mDataX la suite de ses puissance de 1 à degPoly
    return(X.dot(Theta.T))                                                  # On renvoit le produit matriciel entre X et Theta.T



"""La fonction error a pour but de calculer l'erreur entre le résultat de la fonction hypFunction calculée sur un echantillon de mData par rapport au reste de mData.
Ainsi on réalise un calcule polynomial sur un échantillon constitué de 80% de mData que l'on conpare aux reste des 20% de mData.
Error renvoit une matrice correspondant au éléments diagonaux de la matrice des moyennes pondérées des résidus de la fonction hypFunction. """

# hypFunction, Theta : voir précédemment
# dataX : tableaux de valeurs issues de mData après exécution de regroupeParCommune et de splitSet. On obtient donc 80% des communes de mData dans dataX. Ce tableau sert au calcul du polynôme de notre modélisation.
# dataY : tableaux de valeurs issues de mData après exécution de regroupeParCommune et de splitSet. On obtient donc 20% des communes de mData dans dataY. Ce tableau sert à la vérification du polynôme sur un échantillon de valeurs vraies.
# degPoly : degré du polynôme d'interpolation choisi

def error(hypFunction, Theta, dataX, dataY, degPoly):
    n = dataX.shape[0]                                  # Nombre de lignes de mDataX
    w = np.zeros(n)                                     # Poids des individus, pondérés par le nombre d'habitants/commune X[i,0]
    for i in range(n):                                  # On parcourt toutes les lignes de mDataX
        w[i] = dataX[i,0]                               # dataX[i,0] représente le nombre d'individus résidant dans la commune i
    weight = np.diag(w/np.sum(w))                       # Poids sous forme matricielle diagonale et normalisés
    guess = hypFunction(dataX, Theta, degPoly)          # Polynome issu de l'execution de hypFunction
    residu = (guess-dataY)/(1E-10+guess+dataY/2)        # Ecart entre la fonction calculée et les valeurs vraies issues d'un echantillon de mData : mDataY
    square_Erreur = residu.T.dot(weight.dot(residu))    # Moyenne pondérée des carrés des résidus
    k = square_Erreur.shape[0]      
    erreur = np.zeros(k)                                # Eléments diagonaux de la matrice square_Erreur
    for i in range(k):
        erreur[i] = square_Erreur[i,i]   
    return(np.sqrt(erreur))

  
  
def costFunction(Theta, X, y, Lambda):
    m = y.shape[0]
    J = 0
    X_aux = np.dot(X,Theta.T)
    J = (0.5/m)*np.dot((X_aux-y).T,X_aux-y)+(Lambda/(2*m))*(np.dot(Theta,Theta.T)-Theta[0]**2) #cf le document EtudeModélisation sur le drive
    return(J)

def gradientCostFunction(Theta, X, y, Lambda):
    m = y.shape[0]
    X_aux = np.dot(X,Theta.T)
    grad = (1/m)*np.dot(X.T, X_aux-y)+(Lambda/m)*Theta
    grad[0] = grad[0] - (Lambda/m)*Theta[0]
    return(grad)

""" ================================== Ne pas modifier ============================================== """
def optimisation(mDataX, mDataY, degPoly, Lambda = 1.):
    # Mise en forme du problème comme d'un système linéaire
    K = mDataY.shape[1] # Nombre de fonction hypothesis OneVsAll à entraîner
    X = np.concatenate((np.ones((mDataX.shape[0],1)), mDataX), axis = 1)
    for i in range(2, degPoly+1):
        X = np.concatenate((X, mDataX**i), axis = 1)
    
    L = X.shape[1]
    allTheta = np.ones((K,L))  # Theta(k,:) = paramètres de la fonction hypothesis de la k-ième sortie
    for k in range(K):
        y = mDataY[:,k]
        resOptim = scipy.optimize.minimize(fun=costFunction, x0=np.ones(L), args=(X,y,Lambda), jac = gradientCostFunction)
        allTheta[k,:] = resOptim.x
    return(allTheta)

#################################
# NORMALISER LE NOMBRE DE TRAVAIL SUR LA REGION ?? lE DEPARTEMENT ?? ET/OU LOCALEMENT ??
#   Car sortie = pourcentage => besoin de données normalisées
    
    
    
"""    
from scipy.cluster.vq import kmeans2
centroids, clust_ind = kmeans2(mFact[:,:2], nb_classes)
    
"""    
    
    
