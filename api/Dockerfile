FROM debian:latest

# Création d'un espace de travail dans l'image (puis le container...)
# app est ici notre PWD
WORKDIR /app

# je copie tous les documents présent dans le dossier courant (ici c'est api)
# dans l'espace de travail que l'on a créé précédement
COPY . /app

# Mise a jours + installation python et  des requirements
RUN apt update && apt install python3-pip -y && pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn","main:api","--host=0.0.0.0"]