'''
VITTEAU Magdi 12511408
SAIDJ Aghiles 12511222
'''

"""
Ficher initialisation (eg, constantes chargées au démarrage dans la session)
"""

from datetime import datetime
from os import path

SESSION['APP'] = "Bataille Navale"
SESSION['BASELINE'] = "Faites les dormir avec les poissons !"
SESSION['DIR_HISTORIQUE'] = path.join(SESSION['DIRECTORY'], "historiques")
SESSION['HISTORIQUE'] = []
SESSION['CURRENT_YEAR'] = datetime.now().year
SESSION['JOUEUR_COURANT'] = None
