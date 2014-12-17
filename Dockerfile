FROM debian
 
RUN apt-get update
RUN apt-get install git python-flask python-pip -y --fix-missing
RUN git clone http://github.com/svineet/GCILeaderboard.git /gcil
RUN pip install -r /gcil/requirements.txt

EXPOSE 5000 
CMD cd /gcil; git checkout ignacio-style; sh run.sh

