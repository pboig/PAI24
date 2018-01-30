# -*- coding: utf-8 -*-
"""
Created on Sun Jan 14 16:42:04 2018

@author: perez
"""
import TraitementData as TD
import numpy as np
from scipy.cluster.vq import kmeans2
import matplotlib.pyplot as plt
""" ======================= Elements de modélisation ===================================== """
# Importer nombre de personnes (actifs dans un 1er temps) par commune
# Regrouper les communes par classes en fonction de la distance (centres mobiles)
# Pour chaque commune : proportion qui travaille dans la comm de résidence
#   et proportion ailleurs : proportion dans la classe et proportion des les classes plus éloignées
#   Proportion dans les classes plus éloignées = NB_emploi_classe^3/(somme_classe des NB_emploi^3) pour que les personnes qui
#                                                   travaillent loin n'aillent que dans les communes où il y a bcp de travail
#   Une fois qu'il vont dans une classe, dans les villes où il y a beaucoup de travail en priorité; 
#                           par expl NB_emploi_comm^2/(somme_comm_de_la_classe des NB_emploi^2)

# Faire évoluer le modèle à l'échelle de la région => raccordement départements avec métropole de Lyon, Grenoble, etc.
idDep = '38'
mDataComm = mDataCommDep  # !! Changer tous les mDataComm en mDataCommDep
listComm = TD.checkComm(mDataComm)

def delNotFound(mDataN, listCommNumpy, commNotFound):
    nbComm = len(listCommNumpy)-len(commNotFound)
    travailInOut = np.zeros((nbComm,2))
    j = 0
    for i in range(len(listCommNumpy)):
        if not(listCommNumpy[i] in commNotFound):
            travailInOut[j,:] = mDataN[i,:]
            j += 1
    return(travailInOut)
travailInOut = delNotFound(mYDep, listCommNumpy, commNotFound2)
mDataGPS = delNotFound(mDataGPS,)
#mDataX, mDataY = mXDep, mYDep
nb_classes = 15
centroids, clust_ind = kmeans2(mDataGPS[:,1:], nb_classes) # Regroupement communes par secteur

nbComm = len(mDataComm)
#travailInOut = MP.hypFunction(mDataX, allTheta, degPoly)   # % personnes travaillant OUT commune et % travaillant IN



nbEmploiComm = np.zeros(nbComm)
for i in range(nbComm):
    nbEmploiComm[i] = mDataComm[i][2]
nbEmploiClass = np.zeros((nb_classes,2))   # Nb emploi dans la classe | Somme des carrés des emplois dans la classe 
for i in range(nbComm):
    nbEmploiClass[clust_ind[i],0] += nbEmploiComm[i]
    nbEmploiClass[clust_ind[i],1] += nbEmploiComm[i]**2

# Assuming parmis ceux qui taf pas dans la comm de résidence :
#           50% travaille dans une comm de la classe et 50% dans une comm éloignée avec beaucoup de d'emplois ...
propCommClass = 0.5; propCommEloignee = 0.5;

""" ========== Calcul des flux pro = proportions de personnes résidant dans Comm_i et travaillant dans Comm_j =========== """   
mProportionGoTaf = np.diag(travailInOut[:,1])  # Matrice de la proportion de personnes habitant i travaillant dans j 
for i in range(nbComm):
    for j in range(i+1,nbComm):
        if clust_ind[i] == clust_ind[j]:
            mProportionGoTaf[i,j] = propCommClass*nbEmploiComm[j]/nbEmploiClass[clust_ind[j],0]   # Proba proportionnelle au nombre d'emploi de la ville de travail
            mProportionGoTaf[j,i] = propCommClass*nbEmploiComm[i]/nbEmploiClass[clust_ind[i],0]
        else:
            coefNormalisation = (nbEmploiClass[:,0]**2).sum()
            propClassJ = propCommEloignee*nbEmploiClass[clust_ind[j],0]**2/coefNormalisation        # Proba d'aller dans la zone j
            propClassI = propCommEloignee*nbEmploiClass[clust_ind[i],0]**2/coefNormalisation        # Proba d'aller dans la zone j                           
            mProportionGoTaf[i,j] = propClassJ*(nbEmploiComm[j]**2)/nbEmploiClass[clust_ind[j],1]   
            mProportionGoTaf[j,i] = propClassI*(nbEmploiComm[i]**2)/nbEmploiClass[clust_ind[i],1]

""" =========================================== Vérification ========================================== """
FluxMob = TD.loadData('Flux_mobpro_2013.txt',2,idDep)
NbTravailleursComm = np.zeros(nbComm+1)     # !! A déterminer à partir des données démographiques en pratique

mReferenceGoTaf = np.zeros((nbComm+1, nbComm+1), dtype = 'int')

# Partie à recoder : besoin d'une fonction qui renvoi l'indice d'une comm 'XXX' et -1 si cette comm n'est pas dans listComm
def returnInd(listComm, idComm):
    i = 0
    while i<len(listComm) and listComm[i] != idComm:
        i += 1
    return(i)

for x in FluxMob:
    if x[0] == idDep:
        i = returnInd(listComm, x[1])
        if x[2] == idDep:
            j = returnInd(listComm, x[3])
        else:
            j = nbComm
        isInDep = True
    elif x[2] == idDep:
        i = nbComm
        j = returnInd(listComm, x[3])
        isInDep = True
    else:
        isInDep = False
    if isInDep:
        NbTravailleursComm[i] += x[4]
        mReferenceGoTaf[i,j] = x[4]            

    # NbGoTaf : rajouter une ligne&colonne "ext"
mProportionGoTaf = np.concatenate((mProportionGoTaf, np.zeros((1,nbComm))),axis = 0)
mProportionGoTaf = np.concatenate((mProportionGoTaf, np.zeros((nbComm+1,1))),axis = 1)
#NbGoTaf = int(mProportionGoTaf*NbTravailleursComm*(np.tile(nbEmploiComm,(nbComm,1)).T))     # Think its wrong
NbGoTaf = mProportionGoTaf*( np.tile(NbTravailleursComm,(nbComm+1,1)).T )   # Nombre de personnes habitant i travaillant à j

errorModele = np.sqrt(((NbGoTaf-mReferenceGoTaf)**2).mean()) # Non pondéré


""" ============= Flux entre classes ============== """
 
fluxClasses = np.zeros((nb_classes+1, nb_classes+1))
for i in range(nbComm):
    for j in range(i,nbComm):
        fluxClasses[clust_ind[i], clust_ind[j]] += NbGoTaf[i,j]
        fluxClasses[clust_ind[j], clust_ind[i]] += NbGoTaf[j,i]
for i in range(nbComm):
        fluxClasses[clust_ind[i], nb_classes] += NbGoTaf[i,nbComm]
        fluxClasses[nb_classes, clust_ind[i]] += NbGoTaf[nbComm,i]
        
plt.figure()
plt.scatter(centroids[:,0], centroids[:,1])
            

for (label, x, y) in zip(clust_ind_labels, centroids[:,0], centroids[:, 1]):
    plt.annotate(label, xy=(x,y), xytext=(4,4), textcoords = 'offset points') 
















