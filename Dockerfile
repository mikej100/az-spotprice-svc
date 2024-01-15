FROM python:3.12-bookworm
WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt


COPY . .
COPY ./src ./src
COPY ./log/.gitkeep ./log/.gitkeep
COPY ./logging.yaml ./logging.yaml

EXPOSE 6800

CMD "echo $PATH" 
# CMD ["python3",  "az_spotprice_svc.py", "-i 3"]
# CMD ["kpython3 ./az_spotprice_svc.py --interval 1 --count 5"]