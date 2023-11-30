# Project-Diabetes-130-US-hospitals-1999-20

## Description

Le dataset représente dix années (1999-2008) de soins cliniques dans 130 hôpitaux américains et réseaux de distribution intégrés. Chaque ligne concerne les dossiers hospitaliers de patients diagnostiqués diabétiques, qui ont subi des examens de laboratoire, pris des médicaments et séjourné jusqu'à 14 jours. L'objectif est de déterminer la réadmission précoce du patient dans les 30 jours suivant sa sortie de l'hôpital. Le problème est important pour les raisons suivantes. Malgré des preuves de haute qualité montrant une amélioration des résultats cliniques pour les patients diabétiques qui bénéficient de diverses interventions préventives et thérapeutiques, de nombreux patients n'en bénéficient pas. Cette situation peut être partiellement attribuée à une gestion arbitraire du diabète en milieu hospitalier, où le contrôle de la glycémie n'est pas pris en compte. L'absence de prise en charge adéquate du diabète augmente non seulement les coûts de gestion pour les hôpitaux (car les patients sont réadmis), mais a également un impact sur la morbidité et la mortalité des patients, qui peuvent être confrontés à des complications associées au diabète.

## Installation

Ce projet nécessite Python 3.10.12. Assurez-vous que vous avez la bonne version de Python installée sur votre système.

## Configuration de l'Environnement

Il est recommandé d'utiliser un environnement virtuel pour éviter les conflits de dépendances avec d'autres projets. Pour créer et activer un environnement virtuel :

Sur Unix ou MacOS :
python3 -m venv mon_env
source mon_env/bin/activate

Sur Windows :
python -m venv mon_env
mon_env\Scripts\activate

## Installation des Dépendances

Installez toutes les dépendances nécessaires en exécutant :
pip install -r requirements.txt

## Utilisation

Pour lancer notre WebApp, naviguez jusqu'au répertoire du projet et lancez la commande suivante :
streamlit run .\app\Home.py

## Fonctionnalités

🆕 Evaluate the readmission risk for a new patient based on clinical data

📈 View statistical insights from our training dataset to understand broader trends

📑 See more details about how we built this model

👥 Meet and discover the team that worked on this project
