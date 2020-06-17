# mygym

Repository per il progetto di tecnologie web 2020.

Per runnare il progetto in locale seguire quanto riportato in questo file:
Creare una cartella che ospiti il progetto
> mkdir progetto

> cd ./progetto

Se non ancora presente, installare python 3.7
> sudo apt-get install python3.7

Clonare la repository
> git clone https://github.com/septo198/mygym.git

Spostarsi nella cartella ./mygym/
> cd ./mygym/

Creare virtual env ed attivarlo
> python -m virtualenv venv

> source venv/bin/activate

Installare i pacchetti richiesti per il funzionamento
> pip install -r requirements.txt

Infine avviare il server
> python manage.py runserver

Per eseguire i test
> python manage.py test gym
