# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 17:23:15 2017

@author: Augustin Ardon
"""

import xlrd

#nomFichier = 'EFF_APE_AUVERGNE_RHONE_ALPES.xls'

"""Le fichier 'EFF_APE_AUVERGNE_RHONE_ALPES.xls' a la forme suivante :
Il s'agit d'un excel avec les feuilles correspoondant aux départements de la région Auvergne - Rhône Alpes. Ex : 01, 03, 07, 15, 26, 38, 42, 43...
Une feuille a la structure suivante : ( commune (numéro + nom) ; domaine d'activité ; nombre d'établissements 2008 ; ... ; nombre d'établissements 2016 ; effectif disponible 2008 ; ... ; effectif disponible 2016 )
Chaque ligne correspond à un secteur d'activité dans une commune donnée. on passe donc en revu tous les secteurs d'activité par commune."""

#iDep = '69'

"""Cette fontion a pour but de construire un tableau qui regroupe les numéro insee des communes et le nombre d'emplois disponibles dans cette communes 
quels que soient les secteurs d'activité. Pour cela on commence par charger les données d'emploi de l'institut Acoss puis on ne garde que les données 
du département iDep, enfin, on somme les nombres d'emplois disponibles suivant les secteurs d'activités.
On renvoit ainsi un tableau de la forme ( ID_commune ; nb_emplois ) propres au département iDep"""

def loadXlsEmplois(nomFichier, iDep):
    donnees_brutes = xlrd.open_workbook(nomFichier)                                             # Chargement des données brutes du fichier excel
    commune69 = donnees_brutes.sheet_by_name(iDep)                                              # Chargement des données de la feuille de calcul correspondant à la commune iDep
    commune2016 = commune69.col_values(0),commune69.col_values(10),commune69.col_values(19)     # On ne conserve que les données ( ID_commune ; nombre établissements 2016 ; nb effectif 2016 )
    
    emplois=[]                                                                                  # On renvoit un tableau (liste de liste) avec les communes et le nombre d'emplois par commune
    m2 = 0
    for i in range (1,len(commune2016[0])-1):                                                   # On somme les nombres d'emplois dans une commune quel que soit le secteur d'activité
        if commune2016[2][i]!='':                                                               # On test que le champ n'est pas vide
            m2+=int(commune2016[2][i])                                                          # On ajoute tous les emplois dans une commune quel que soit le secteur d'activité
        if commune2016[0][i]==commune2016[0][i+1]:                                              # lorsque l'on a épuisé tous les secteurs d'activités, le nom de la commune change
            continue
        else :
            nom_commune = commune2016[0][i]
            j=0
            while j < len(nom_commune):                                                         # On sépare le numéro insee de la commune de son nom
                if nom_commune[j] !='-':                                                        # Le champ [0] est de la forme '38001 - ABRETS' La délimitattion entre IDcommune et son nom est ' '
                    j+=1
                else:
                    num_commune=int(nom_commune[0:j-1])                                         # On ne garde que IDcommune
                    break
            emplois.append([num_commune,m2])
            m2 = 0
    j=0
    nom_commune = commune2016[0][i]                                                             # On recommence l'opération pour la dernière commune pour des raisons d'indexation dans i ligne 31
    while j < len(nom_commune):
        if nom_commune[j] !='-':
            j+=1
        else:
            num_commune=int(nom_commune[0:j-1])
            break
    emplois.append([num_commune,m2])
    for i in range(len(emplois)):                                                               # Dans IDcommune on ne garde que le numéro insee propre à la commune sans le numéro propre à iDep
        emplois[i][0] = str(emplois[i][0])[2:]
    return(emplois)                                                                             # On renvoit le tableau des (IDcommune ; nb emplois)
               



