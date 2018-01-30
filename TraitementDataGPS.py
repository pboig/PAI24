# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 18:28:50 2018

@author: perez
"""
import xlrd
import numpy as np

#nomFichier = 'communes_gps.xlsx'

def loadDataGPS(nomFichier, iDep):
    donnees_brutes = xlrd.open_workbook(nomFichier)
    
    data = donnees_brutes.sheet_by_name('alldata')
    dataGPS = data.col_values(10), data.col_values(11), data.col_values(12) # idCommune | Latitude | Longitude
    
    m = len(dataGPS[0])
    n = 0
    for i in range(1,m):
        if type(dataGPS[0][i]==float):                                              # Problème potentiel avec la Corse (convertion txt en int)
            iD = str(int(dataGPS[0][i])); k = len(iD);
            dep = int(iD[0:(k-3)]); comm = int(iD[k-3:k]);
            if dep == int(iDep):
                a = dataGPS[1][i]; b = dataGPS[2][i];                               # On ne récupère les pos GPS que des communes du département iDep[txt]
                if (type(a)==float or len(a)>0) and (type(b)==float or len(b)>0):   # Problème si données non-renseignées
                        n += 1
                        
    mDataGPS = np.zeros((n,3))                                                      # Matrice renvoyée : ligne = commune : idCommune | X (km) | Y (km)
    j = 0
    for i in range(1,m):
        if type(dataGPS[0][i]==float):                                              # Problème potentiel avec la Corse (convertion txt en int)
            iD = str(int(dataGPS[0][i])); k = len(iD);
            dep = int(iD[0:(k-3)]); comm = int(iD[k-3:k]);
            if (dep == int(iDep) and (type(dataGPS[1][i])== float or len(dataGPS[1][i])>0)
            and (type(dataGPS[2][i])==float or len(dataGPS[2][i])>0)):              # On ne récupère les pos GPS que des communes du département iDep[txt]
                mDataGPS[j,0] = comm
                mDataGPS[j,1] = 111.16*float(dataGPS[2][i])                         # X (km) = 111.16*Longitude (°)
                mDataGPS[j,2] = 111.16*float(dataGPS[1][i])                         # Y (km) = 111.16*Latitude  (°)  
                j += 1
        else:
            mDataGPS[i,0] = -1                                                      # Le cas ne devrait normalement pas se présenter
        
    return(mDataGPS)
