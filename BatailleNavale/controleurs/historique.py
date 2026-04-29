'''
VITTEAU Magdi 12511408
SAIDJ Aghiles 12511222
'''

from controleurs.includes import add_activity
import os

add_activity(SESSION['HISTORIQUE'], "Consultation du journal de bord")

if POST and 'bouton_export' in POST:
    nom_fichier = "journal_bord_session.txt"
    filepath = os.path.join(SESSION['DIRECTORY'], nom_fichier)
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("=== JOURNAL DE BORD - BATAILLE NAVALE ===\n")
            f.write(f"Joueur : {SESSION.get('JOUEUR_COURANT', {}).get('pseudo', 'Anonyme')}\n")
            f.write("-" * 40 + "\n")
            for action in SESSION['HISTORIQUE']:
                date_str = action['date'].strftime('%d/%m/%Y %H:%M')
                f.write(f"[{date_str}] {action['description']}\n")
        
        REQUEST_VARS['message'] = f"Fichier '{nom_fichier}' généré avec succès."
        REQUEST_VARS['message_class'] = "alert-success"
    except Exception as e:
        print(f"Erreur d'export : {e}")
        REQUEST_VARS['message'] = "Erreur technique lors de l'export."
        REQUEST_VARS['message_class'] = "alert-error"