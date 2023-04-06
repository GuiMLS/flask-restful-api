FROM python:3.11.3-slim-bullseye

WORKDIR /src

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

RUN python models.py
RUN python utils.py

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]

EXPOSE 5000