"""
Synchronise vers la base SQLite locale les clôtures (paris réels ET analyses)
décidées manuellement depuis l'espace admin du site, AVANT le reste du
pipeline quotidien.

Pourquoi ce script existe : 4.Dashboard_MAJResultats.py exporte la liste des
paris/analyses non clôturés automatiquement (paris_non_clotures.json, lu par
5.Envoi_Rapport.py) en se basant sur CETTE base locale. Si une clôture faite
depuis l'admin n'a pas encore été rapatriée ici, elle est encore vue comme
"En cours" par le script 4 — alors qu'elle est déjà résolue côté site —, d'où
un match qui apparaît à tort comme "non clôturé" dans le mail du lendemain.

Ce script se contente d'appeler les deux fonctions de synchronisation déjà
présentes dans update_site.py, sans dupliquer leur logique.

update_site.py calcule désormais son chemin de base de données à partir de son
propre emplacement (et non plus du répertoire d'exécution courant), donc ce
script peut être lancé depuis n'importe quel répertoire — plus besoin du
pushd/popd de TWO_FULL_AUTO.bat pour ce cas précis.

Usage :
    python synchroniser_clotures_admin.py
"""

import importlib.util
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CHEMIN_UPDATE_SITE = os.path.join(SCRIPT_DIR, "update_site.py")

spec = importlib.util.spec_from_file_location("update_site", CHEMIN_UPDATE_SITE)
update_site = importlib.util.module_from_spec(spec)
spec.loader.exec_module(update_site)

if __name__ == "__main__":
    update_site.appliquer_clotures_admin()
    update_site.appliquer_clotures_admin_analyses()