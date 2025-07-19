FROM ubuntu:20.04
ARG DEBIAN_FRONTEND=noninteractive

ENV FLAG=wxmctf{p4rAm373r_P0lLU7IOn}

EXPOSE 5000

RUN apt-get update \
    && apt-get install -y \
        apache2 \
        php \
        libapache2-mod-php \
        python3 \
        python3-pip

WORKDIR /var/www/html
COPY . .

RUN pip install -r requirements.txt
RUN chmod 777 -R /var/www/html

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]