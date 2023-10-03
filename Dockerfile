FROM python:3.10-slim

WORKDIR /usr/src/app/

COPY requirements.txt ./
ADD trassir_exporter.py .

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./trassir_exporter.py --config trassir.yml" ]