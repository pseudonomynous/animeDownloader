# Dockerfile, Image, Container

FROM python:3.8

RUN apt-get update && \
      apt-get -y install sudo

RUN echo Y | sudo apt-get install xvfb

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | tee /etc/apt/sources.list.d/google-chrome.list
RUN apt-get update
RUN echo Y | apt-get install google-chrome-stable 

RUN export PATH="$HOME/.local/bin:$PATH"

ADD ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt

ADD anime.py .

CMD ["python3", "./anime.py" ]