FROM python:3.9-alpine

WORKDIR /app
COPY db db
COPY static static
COPY templates templates
COPY app.py app.py
COPY requirements.txt requirements.txt
RUN pip install -r ./requirements.txt

EXPOSE 5000
ENTRYPOINT ["flask", "run", "--host=0.0.0.0"]