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

Installare pipenv
> pip3 install pipenv

Spostarsi nella cartella ./mygym/
> cd ./mygym/

Installare i pacchetti richiesti per il funzionamento
> pipenv install -r requirements.txt

Infine aprire la shell ed avviare il server
> pipenv shell
> python manage.py runserver

Per eseguire i test
> python manage.py test gym
