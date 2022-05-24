# Contributeurs
Audrey et Jaouad 

# Présentation générale :

Notre projet Datascientest, en data engineering, a pour but de prédire l'adhésion d'un individu à un nouveau produit bancaire.
En plus de la phase de modèlisation, nous avons été amenés à mettre en production notre algorithme de classification.
Pour se faire, dans un premier temps,  nous avons construit une Api avec FastAPI que nous avons accompagné de tests unitaires de sorte à nous assurer de son bon fonctionnement. Par la suite, nous avons déployé l'Api ainsi que les tests unitaires associés en utilisant Kubernetes. 


# Prérequis
*  Notebook "Bank_Project_P2" : notebook ayant permis de selectionner le modèle optimal à déployer.
* Kubernetes : doit être installé sur la machine.

# Deploiement du modèle sur Kubernetes 

Afin de pouvoir accéder à notre API, après avoir installé Kubernetes, il faut exécuter les commandes suivantes :
* kubectl create -f my-secret.yml
* kubectl create -f my-deployment-env.yml
* kubectl create -f my-service.yml
* minikube addons enable ingress
  * kubectl create -f my-ingress.yml

A présent, pour se connecter à l'API,  il faut suivre les étapes suivantes: 
* kubectl get ingress : Récuperer  l'adresse IP du service "my-service". 
* Vous devez passer par un tunnel ssh, entre le port 80 du service et le port 8000 de la machine machine, pour pouvoir y accéder depuis le navigateur web:
LocalForward  127.0.0.1:8000 192.168.49.2:80 (commande VS code dans le fichier config pour se connecter à la machine virtuelle)
L'API sera donc accesible à l'adresse : 127.0.0.1:8000

# Utilisation de l'API :

Pour pouvoir accéder à la documentation de l'API, vous devez vous rendre à l'adresse suivante : 127.0.0.1:8000/docs
