# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 18:28:50 2018

@author: perez
"""
import xlrd
import numpy as np

#nomFichier = 'communes_gps.xlsx'
""" Structure du fichier 'communes_gps.xlsx' :
[EU ciconscription (sud, sud-est...) ; nom région ; chef-lieu région ; numéro département ; préfécture ; numéro circonscription ; code postal ; code insée ; latitude ; longitude ; éloignement]
Chaque ligne correspond à une commune différente, le tout est trié par numéro de département."""


"""La fonction loadDataGPS extrait les données du fichier 'communes_gps.xlsx' et les renvoie sous forme de matrice. On commence par compter le nombre de communes comprises dans le département iDep
puis on charge toutes les données de position et de numéro de commune de chacune d'elles dans une matrice du type ( ID_commune ; distance_X(km) ; distance_Y(km) )"""

def loadDataGPS(nomFichier, iDep):
    donnees_brutes = xlrd.open_workbook(nomFichier)
    
    data = donnees_brutes.sheet_by_name('alldata')                                  # Ouverture du classeur 'alldata'
    dataGPS = data.col_values(10), data.col_values(11), data.col_values(12)         # code insée commune | Latitude | Longitude
    
    m = len(dataGPS[0])                                                             # m : nombre de communes
    n = 0                                                                           # n : nombre de communes dans le département iDep (initialisé à 0)
    
######## On s'assure que les données GPS des communes comprises dans le département iDep sont valides et on les compte #######
    for i in range(1,m):                                                           
        if type(dataGPS[0][i]==float):                                              # Problème potentiel avec la Corse (convertion txt en int). On ne traite pas ici le problème de la Corse
            iD = str(int(dataGPS[0][i])); k = len(iD);                              # colonne 10 du fichier xlsx : code postal de la commune. k : longueur du code postal
            dep = int(iD[0:(k-3)]); comm = int(iD[k-3:k]);                          # On garde ainsi en numéro département les deux premiers chiffres et en numéro de commune les suivants
            if dep == int(iDep):
                a = dataGPS[1][i]; b = dataGPS[2][i];                               # On ne récupère les pos GPS que des communes du département voulu iDep[txt]
                if (type(a)==float or len(a)>0) and (type(b)==float or len(b)>0):   # Problème si données non-renseignées : on passe au suivant
                        n += 1                                                      # On compte le nombre de communes qui nous intéressent
                        
    mDataGPS = np.zeros((n,3))                                                      # Matrice renvoyée : ligne = commune : idCommune | X (km) | Y (km)
    j = 0
    
######## On récupère les données GPS des communes comprises dans le départemeent iDep #######   
    for i in range(1,m):                                                            
        if type(dataGPS[0][i]==float):                                              # Problème potentiel avec la Corse (convertion txt en int). On ne traite pas ici le problème de la Corse
            iD = str(int(dataGPS[0][i])); k = len(iD);                              # colonne 10 du fichier xlsx : code postal de la commune. k : longueur du code postal
            dep = int(iD[0:(k-3)]); comm = int(iD[k-3:k]);                          # On garde ainsi en numéro département les deux premiers chiffres et en numéro de commune les suivants
            if (dep == int(iDep) and (type(dataGPS[1][i])== float or len(dataGPS[1][i])>0)
            and (type(dataGPS[2][i])==float or len(dataGPS[2][i])>0)):              # On ne récupère les pos GPS que des communes du département iDep[txt]
                mDataGPS[j,0] = comm
                mDataGPS[j,1] = 111.16*float(dataGPS[2][i])                         # X (km) = 111.16*Longitude (°)
                mDataGPS[j,2] = 111.16*float(dataGPS[1][i])                         # Y (km) = 111.16*Latitude  (°)  
                j += 1
        else:
            mDataGPS[i,0] = -1                                                      # Le cas (Corse) ne devrait normalement pas se présenter
        
    return(mDataGPS)

