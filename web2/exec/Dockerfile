FROM python:3.10.9-slim-buster

ENV FLAG=wxmctf{ok4Y_M4y8e_I_5K1mpED_@_bit}

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]