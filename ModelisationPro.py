# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 10:03:55 2017

@author: perez
"""

"""
Méthodologie :
1) PRE-TRAITEMENT :  Conversion matrice données en une matrice numpy
                        > dataToNumpy (Entrée = whole Data Set)
2) OPTIMISATION   :  Regression non-linéaire avec la matrice numpy 
                        > fonction2 (Entrée = Training Set)
                            > hypFonction (Entrée = une commune - numpy)
3) CALCUL RESULTAT:  Calcul des résultats à partir des paramètres optimisés - en passant par numpy 
                        > hypothesisFonction (Entrée = une commune)
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
def length(x):
    if type(x) == list:
        return(len(x))
    return(1)

def dataToNumpy(mData, iOut = []):
    # iOut = indices des sorties dans mData
    # Met les modalités des variables bout-à-bout
    I, M, J, K = len(mData), len(mData[0]), 0, 0
    for m in range(1,M):
        x = mData[0][m]
        if m in iOut:
            K += length(x)
        else:
            J += length(x)
        
    dataInNumpy = np.zeros((I,J))
    dataOutNumpy = np.zeros((I,K))
    for i in range(I):
        j, k = 0, 0
        for m in range(1,M):
            x = mData[i][m]
            n = length(x)
            if m in iOut:
                if n == 1:
                    dataOutNumpy[i,k] = x
                    k += 1
                else:
                    for y in range(n):
                        dataOutNumpy[i,k] = x[y]
                        k += 1
            else:
                if n ==1:
                    dataInNumpy[i,j] = x
                    j += 1
                else:
                    for y in range(n):
                        dataInNumpy[i,j] = x[y]
                        j += 1
    return(dataInNumpy, dataOutNumpy)
    
""" =================================== OPTIMISATION =================================== """
def sigmoid(X):
    return(1./(1+np.exp(-X)))

def hypFunction(mDataX, Theta, degPoly):
    X = np.concatenate((np.ones((mDataX.shape[0],1)), mDataX), axis = 1)
    for i in range(2, degPoly+1):
        X = np.concatenate((X, mDataX**i), axis = 1)
    return(X.dot(Theta.T))

def error(hypFunction, Theta, dataX, dataY, degPoly):
    n = dataX.shape[0]
    w = np.zeros(n)                                     # Poids des individus, pondérés par le nombre d'habitants/commune X[i,0]
    for i in range(n):
        w[i] = dataX[i,0]
    weight = np.diag(w/np.sum(w))                       # Poids sous forme matricielle
    guess = hypFunction(dataX, Theta, degPoly)
    residu = (guess-dataY)/(1E-10+guess+dataY/2)        
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
    J = (0.5/m)*np.dot((X_aux-y).T,X_aux-y)+(Lambda/(2*m))*(np.dot(Theta,Theta.T)-Theta[0]**2)
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
    
    
    
    
            
    
    
    
    