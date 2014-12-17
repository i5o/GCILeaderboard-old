FROM debian
 
RUN apt-get update
RUN apt-get install git python-flask python-pip -y --fix-missing
RUN git clone http://github.com/ignaciouy/GCILeaderboard.git /gcil
RUN pip install -r /gcil/requirements.txt

EXPOSE 5000 
CMD cd /gcil; sh run.sh

