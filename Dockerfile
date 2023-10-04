FROM python:3.10-slim

WORKDIR /usr/src/app/

COPY requirements.txt ./
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD python ./trassir_exporter.py --config /usr/src/app/trassir.yml
