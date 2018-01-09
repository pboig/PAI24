# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 17:23:15 2017

@author: Augustin Ardon
"""

import xlrd

#nomFichier = 'EFF_APE_AUVERGNE_RHONE_ALPES.xls'
#iDep = '69'
def loadXlsEmplois(nomFichier, iDep):
    donnees_brutes = xlrd.open_workbook(nomFichier)
    commune69 = donnees_brutes.sheet_by_name(iDep)
    commune2016 = commune69.col_values(0),commune69.col_values(10),commune69.col_values(19)
    
    emplois=[]
    m1,m2 = 0,0
    for i in range (1,len(commune2016[0])-1):
        if commune2016[2][i]!='':
            m2+=int(commune2016[2][i])
        if commune2016[0][i]==commune2016[0][i+1]:
            continue
        else :
            nom_commune = commune2016[0][i]
            j=0
            while j < len(nom_commune):
                if nom_commune[j] !='-':
                    j+=1
                else:
                    num_commune=int(nom_commune[0:j-1])
                    break
            emplois.append([num_commune,m2])
            m1 = 0
            m2 = 0
    j=0
    nom_commune = commune2016[0][i]
    while j < len(nom_commune):
        if nom_commune[j] !='-':
            j+=1
        else:
            num_commune=int(nom_commune[0:j-1])
            break
    emplois.append([num_commune,m2])
    for i in range(len(emplois)):
        emplois[i][0] = str(emplois[i][0])[2:]
    return(emplois)
               

