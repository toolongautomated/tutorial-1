FROM python:3.10-slim

EXPOSE 80
ENV FLASK_APP=main.py

COPY . /app
WORKDIR /app/src

RUN pip install --no-cache-dir -r /app/requirements.txt

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:80", "main:app"]

# dummy comment
